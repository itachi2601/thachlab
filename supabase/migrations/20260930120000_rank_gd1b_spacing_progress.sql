-- ============================================================================
-- GĐ 1b #1 (phần còn thiếu) + #7 — thành tích "Tiến bộ tuần" và giãn cách cho Huyền Thoại (30/9/2026)
--
-- 1. Thành tích mới `tien_bo_tuan` (Tiến bộ Tuần): cấp khi em được thưởng RP "tiến bộ so với chính mình"
--    (rank_eval_progress_week) ở bất kỳ tuần nào. Chỉ cấp thêm, không đổi cách tính RP.
-- 2. Giãn cách: mức Huyền Thoại của danh hiệu chuyên môn chỉ tính khi các câu Khó đúng nằm ở
--    >= legend_min_weeks (mặc định 2, chỉnh qua rank_seasons.config) tuần khác nhau (Thứ Hai–Chủ Nhật giờ VN),
--    tính trên kết quả từng câu còn nguyên (đề + luyện tập). Hết 12 tháng dữ liệu đã gộp (rollup) không còn
--    ngày -> không đếm, nhưng ai đã có huy hiệu thì giữ (rank_grant_title không thu hồi).
--    Danh hiệu ĐÃ CÓ không bị thu hồi. Em đang đủ số câu Khó nhưng dồn vào 1 tuần sẽ thấy "còn thiếu 1 tuần".
-- 3. rank_titles_of trả thêm kho_weeks / kho_weeks_need trong progress của danh hiệu chuyên môn
--    (client cũ bỏ qua khoá lạ).
--
-- Hàm định nghĩa lại (đúng bản 20260928100000 + phần thêm, đánh dấu "GĐ 1b"): rank_eval_titles, rank_titles_of,
-- rank_eval_progress_week (bản 20260929110000). Thêm: rank_title_kho_weeks.
-- Không đổi bảng ngoài 1 dòng dữ liệu rank_titles. Chạy giờ nào cũng được.
-- Rollback: perf/rollback/20260930120000_rank_gd1b_spacing_progress.down.sql
-- ============================================================================

insert into public.rank_titles (code, group_code, kind, name, description, sort) values
  ('tien_bo_tuan', 'thanh_tich', 'achievement', 'Tiến Bộ Tuần', 'Có một tuần tỉ lệ đúng tăng so với 2 tuần trước của chính em', 80)
on conflict (code) do update set group_code = excluded.group_code, kind = excluded.kind, name = excluded.name,
  description = excluded.description, sort = excluded.sort;

-- Số tuần (Thứ Hai–Chủ Nhật, giờ VN) khác nhau mà em giải ĐÚNG >= 1 câu Khó thuộc danh hiệu.
create or replace function public.rank_title_kho_weeks(p_student uuid, p_title text)
returns int
language sql stable set search_path = public
as $$
  with topics as (select tt.topic_id from public.rank_title_topics tt where tt.title_code = p_title),
  hits as (
    select public.rank_week_start(eqr.created_at) as wk
    from public.exam_question_results eqr
    join public.question_topics t on t.id = eqr.topic_id
    where eqr.student_id = p_student and eqr.is_correct and eqr.difficulty = 'kho'
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
    union
    select public.rank_week_start(pqr.created_at)
    from public.practice_question_results pqr
    join public.question_topics t on t.id = pqr.topic_id
    where pqr.student_id = p_student and pqr.is_correct and pqr.difficulty = 'kho'
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
  )
  select count(*)::int from hits;
$$;
revoke all on function public.rank_title_kho_weeks(uuid, text) from public, anon;
grant execute on function public.rank_title_kho_weeks(uuid, text) to authenticated;

-- rank_eval_titles = bản 20260928100000 + giãn cách Huyền Thoại (GĐ 1b)
create or replace function public.rank_eval_titles(p_student uuid, p_season bigint default null)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  t public.rank_titles%rowtype;
  st record;
  v_req_titles text[];
  v_req_level text;
  v_ok boolean;
  v_min_weeks int := coalesce(public.rank_cfg(p_season, 'legend_min_weeks', 2), 2)::int;
begin
  -- (a) chuyên môn: Thức Tỉnh (Dễ) · Làm Chủ (Trung bình) · Huyền Thoại (Khó) — độc lập theo độ khó
  for t in select * from public.rank_titles where kind = 'specialist' and enabled and public.rank_title_is_active(code) loop
    select * into st from public.rank_title_stats(p_student, t.code);
    if st.de_correct >= t.min_de then
      perform public.rank_grant_title(p_student, t.code, 'thuc_tinh', p_season, jsonb_build_object('de_correct', st.de_correct, 'need', t.min_de));
    end if;
    if st.tb_correct >= t.min_tb then
      perform public.rank_grant_title(p_student, t.code, 'lam_chu', p_season, jsonb_build_object('tb_correct', st.tb_correct, 'need', t.min_tb));
    end if;
    -- GĐ 1b: Huyền Thoại chỉ tính khi câu Khó đúng rải ở >= legend_min_weeks tuần khác nhau (giãn cách).
    if st.kho_correct >= t.min_kho and public.rank_title_kho_weeks(p_student, t.code) >= v_min_weeks then
      perform public.rank_grant_title(p_student, t.code, 'huyen_thoai', p_season, jsonb_build_object('kho_correct', st.kho_correct, 'need', t.min_kho));
    end if;
  end loop;

  -- (b) bộ sưu tập: mọi danh hiệu thành phần ĐANG ACTIVE đạt từ mức yêu cầu
  for t in select * from public.rank_titles where kind = 'collection' and enabled and (requires ? 'titles') loop
    select array_agg(x) into v_req_titles from jsonb_array_elements_text(t.requires -> 'titles') x;
    v_req_level := coalesce(t.requires ->> 'level', 'lam_chu');
    if not exists (select 1 from unnest(v_req_titles) c where public.rank_title_is_active(c)) then
      continue;
    end if;
    select bool_and(exists (
      select 1 from public.rank_title_awards a
      where a.student_id = p_student and a.title_code = c and public.rank_level_rank(a.level) >= public.rank_level_rank(v_req_level)
    )) into v_ok
    from unnest(v_req_titles) c where public.rank_title_is_active(c);
    if coalesce(v_ok, false) then
      perform public.rank_grant_title(p_student, t.code, 'don', p_season, jsonb_build_object('level', v_req_level));
    end if;
  end loop;

  -- (c) "Kẻ Giải Mã Vũ Trụ": mọi bộ sưu tập đang khả dụng
  for t in select * from public.rank_titles where kind = 'collection' and enabled and coalesce((requires ->> 'collections')::boolean, false) loop
    select bool_and(exists (
      select 1 from public.rank_title_awards a where a.student_id = p_student and a.title_code = c.code
    )) into v_ok
    from public.rank_titles c
    where c.kind = 'collection' and c.enabled and (c.requires ? 'titles')
      and exists (select 1 from jsonb_array_elements_text(c.requires -> 'titles') x where public.rank_title_is_active(x));
    if coalesce(v_ok, false) then
      perform public.rank_grant_title(p_student, t.code, 'don', p_season, '{}'::jsonb);
    end if;
  end loop;
end; $$;

-- rank_titles_of = bản 20260928100000 + kho_weeks (GĐ 1b)
create or replace function public.rank_titles_of(p_student uuid)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_out jsonb := '[]'::jsonb;
  t public.rank_titles%rowtype;
  st record;
  v_levels jsonb;
  v_have text;
  v_visible boolean;
  v_progress jsonb;
  v_req int;
  v_met int;
begin
  if not public.rank_can_view(p_student) then return null; end if;

  for t in select * from public.rank_titles where enabled order by
    case group_code when 'co_hoc' then 1 when 'dao_dong_song' then 2 when 'dien_tu' then 3 when 'nhiet_hoc' then 4 when 'hien_dai' then 5 when 'bo_suu_tap' then 6 else 7 end, sort
  loop
    select coalesce(jsonb_object_agg(a.level, a.awarded_at), '{}'::jsonb) into v_levels
    from public.rank_title_awards a where a.student_id = p_student and a.title_code = t.code;
    select a.level into v_have from public.rank_title_awards a
    where a.student_id = p_student and a.title_code = t.code
    order by public.rank_level_rank(a.level) desc limit 1;

    v_progress := null;
    if t.kind = 'specialist' then
      v_visible := exists (
        select 1 from public.rank_title_topics tt
        join public.question_topics qt on qt.id = tt.topic_id
        left join public.chapter_classes cc on cc.chapter_id = qt.chapter_id
        where tt.title_code = t.code
          and (cc.class_id is null or cc.class_id in (
            select class_id from public.user_classes where user_id = p_student and status = 'active'))
      );
      select * into st from public.rank_title_stats(p_student, t.code);
      v_progress := jsonb_build_object('n', st.n, 'correct', st.correct,
        'de_correct', st.de_correct, 'de_need', t.min_de,
        'tb_correct', st.tb_correct, 'tb_need', t.min_tb,
        'kho_correct', st.kho_correct, 'kho_need', t.min_kho,
        'kho_weeks', public.rank_title_kho_weeks(p_student, t.code), 'kho_weeks_need', 2,
        'topics', (select coalesce(jsonb_agg(jsonb_build_object('id', qt.id, 'name', qt.name, 'lesson_id', qt.lesson_id) order by qt.grade, qt.sort_order), '[]'::jsonb)
                   from public.rank_title_topics tt join public.question_topics qt on qt.id = tt.topic_id where tt.title_code = t.code));
    elsif t.kind = 'collection' and (t.requires ? 'titles') then
      select count(*) filter (where public.rank_title_is_active(x)),
             count(*) filter (where public.rank_title_is_active(x) and exists (
               select 1 from public.rank_title_awards a where a.student_id = p_student and a.title_code = x
                 and public.rank_level_rank(a.level) >= public.rank_level_rank(coalesce(t.requires ->> 'level', 'lam_chu'))))
      into v_req, v_met
      from jsonb_array_elements_text(t.requires -> 'titles') x;
      v_visible := v_req > 0;
      v_progress := jsonb_build_object('required', v_req, 'met', v_met, 'level', coalesce(t.requires ->> 'level', 'lam_chu'),
        'titles', t.requires -> 'titles');
    else
      v_visible := true;
    end if;

    v_out := v_out || jsonb_build_object(
      'code', t.code, 'group', t.group_code, 'kind', t.kind, 'name', t.name, 'description', t.description,
      'visible', v_visible, 'active', case when t.kind = 'specialist' then public.rank_title_is_active(t.code) else v_visible end,
      'level', v_have, 'levels', v_levels, 'progress', v_progress
    );
  end loop;
  return v_out;
end; $$;

-- rank_eval_progress_week = bản 20260929110000 + cấp thành tích tien_bo_tuan khi đủ điều kiện thưởng.
create or replace function public.rank_eval_progress_week(p_season bigint, p_student uuid, p_at timestamptz)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_week date := public.rank_week_start(p_at);
  s public.rank_seasons%rowtype;
  v_min_gain numeric := public.rank_cfg(p_season, 'progress_min_gain_pct', 5);
  v_rp_base int := public.rank_cfg(p_season, 'progress_rp', 15)::int;
  v_rp_max int := public.rank_cfg(p_season, 'progress_rp_max', 25)::int;
  v_step_pct numeric := greatest(public.rank_cfg(p_season, 'progress_step_pct', 5), 0.1);
  v_step_rp int := public.rank_cfg(p_season, 'progress_step_rp', 5)::int;
  v_min_q int := public.rank_cfg(p_season, 'progress_min_questions', 15)::int;
  c record;
  v_need numeric;
  v_rp int;
  v_delta int;
begin
  if not public.rank_is_student(p_student) then return 0; end if;
  select * into s from public.rank_seasons where id = p_season;
  if s.id is null or s.status <> 'active' then return 0; end if;
  if public.rank_vn_date(p_at) < s.starts_on or public.rank_vn_date(p_at) > s.ends_on then return 0; end if;

  select * into c from public.rank_progress_calc(p_student, v_week);
  if c.q_now < v_min_q or c.q_base < v_min_q or c.gain is null then return 0; end if;

  v_need := least(v_min_gain, 100 - c.acc_base);
  if c.gain < v_need then return 0; end if;

  v_rp := least(v_rp_max, v_rp_base + (floor(greatest(c.gain - v_min_gain, 0) / v_step_pct)::int) * v_step_rp);
  v_delta := public.rank_award(p_season, p_student, 'progress_week', v_week::text, v_rp,
    'Tiến bộ tuần ' || to_char(v_week, 'DD/MM') || ': tỉ lệ đúng '
      || replace(c.acc_now::text, '.', ',') || '% (mốc 2 tuần trước '
      || replace(c.acc_base::text, '.', ',') || '%, +' || replace(c.gain::text, '.', ',') || ' điểm %)', null);
  -- GĐ 1b: thành tích Tiến Bộ Tuần (một lần, không thu hồi).
  perform public.rank_grant_title(p_student, 'tien_bo_tuan', 'don', p_season,
    jsonb_build_object('week', v_week, 'gain', c.gain, 'acc_now', c.acc_now, 'acc_base', c.acc_base));
  return v_delta;
end; $$;
revoke all on function public.rank_eval_progress_week(bigint, uuid, timestamptz) from public, anon, authenticated;

-- Sau khi chạy (tuỳ chọn): cấp bù thành tích cho em từng được thưởng tiến bộ tuần
-- (dùng not exists vì chưa xác nhận có unique index trên student_id,title_code,level).
-- Đã chạy 30/9/2026: cấp cho 7 em. Rollback: delete from public.rank_title_awards where title_code='tien_bo_tuan' and evidence='{}'::jsonb;
--   insert into public.rank_title_awards (student_id, title_code, level, season_id, evidence)
--   select distinct on (a.student_id) a.student_id, 'tien_bo_tuan', 'don', a.season_id, '{}'::jsonb
--   from public.rank_rp_awards a where a.source_kind = 'progress_week' and a.awarded > 0
--     and not exists (select 1 from public.rank_title_awards t where t.student_id = a.student_id and t.title_code = 'tien_bo_tuan' and t.level = 'don')
--   order by a.student_id, a.season_id;
