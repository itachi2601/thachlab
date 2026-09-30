-- Rollback 20260930120000_rank_gd1b_spacing_progress.sql: trả 3 hàm về bản trước, bỏ hàm mới.
-- Danh hiệu tien_bo_tuan đã cấp: xoá hẳn nếu muốn (dòng cuối, mặc định để nguyên).
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
    if st.kho_correct >= t.min_kho then
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
  return public.rank_award(p_season, p_student, 'progress_week', v_week::text, v_rp,
    'Tiến bộ tuần ' || to_char(v_week, 'DD/MM') || ': tỉ lệ đúng '
      || replace(c.acc_now::text, '.', ',') || '% (mốc 2 tuần trước '
      || replace(c.acc_base::text, '.', ',') || '%, +' || replace(c.gain::text, '.', ',') || ' điểm %)', null);
end; $$;
revoke all on function public.rank_eval_progress_week(bigint, uuid, timestamptz) from public, anon, authenticated;

drop function if exists public.rank_title_kho_weeks(uuid, text);
-- delete from public.rank_title_awards where title_code = 'tien_bo_tuan';
-- delete from public.rank_titles where code = 'tien_bo_tuan';
