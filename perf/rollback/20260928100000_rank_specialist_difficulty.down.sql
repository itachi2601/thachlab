-- Rollback cho supabase/migrations/20260928100000_rank_specialist_difficulty.sql
--
-- Khôi phục rank_title_stats/rank_eval_titles/rank_titles_of về bản trước
-- migration (xét theo TỔNG số câu + % chính xác + đề thử thách Huyền Thoại).
-- KHÔNG xoá cột difficulty/min_de/min_tb/min_kho đã thêm (dữ liệu vô hại nếu
-- không dùng tới) — chỉ đổi lại hành vi 3 hàm. Danh hiệu đã cấp theo logic mới
-- (rank_title_awards) KHÔNG bị thu hồi — đó là lịch sử, không xoá ngược.
--
-- Chạy: supabase db query --linked -f perf/rollback/20260928100000_rank_specialist_difficulty.down.sql

begin;

drop function if exists public.rank_title_stats(uuid, text);
create function public.rank_title_stats(p_student uuid, p_title text)
returns table(n int, correct int, covered int, total_topics int, acc int)
language sql stable set search_path = public
as $$
  with topics as (
    select tt.topic_id from public.rank_title_topics tt where tt.title_code = p_title
  ),
  rows_ as (
    select coalesce(t.parent_id, t.id) as lesson_topic, eqr.is_correct
    from public.exam_question_results eqr
    join public.question_topics t on t.id = eqr.topic_id
    where eqr.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
  ),
  per_topic as (
    select lesson_topic, count(*) as c from rows_ group by lesson_topic
  )
  select
    (select count(*) from rows_)::int,
    (select count(*) filter (where is_correct) from rows_)::int,
    (select count(*) from per_topic where c >= 3)::int,
    (select count(*) from topics)::int,
    case when (select count(*) from rows_) > 0
      then round((select count(*) filter (where is_correct) from rows_) * 100.0 / (select count(*) from rows_))::int
      else 0 end;
$$;

create or replace function public.rank_eval_titles(p_student uuid, p_season bigint default null)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  t public.rank_titles%rowtype;
  st record;
  v_legend int;
  v_have_master boolean;
  v_level text;
  v_req_titles text[];
  v_req_level text;
  v_ok boolean;
begin
  -- (a) chuyên môn: Thức Tỉnh → Làm Chủ → Huyền Thoại
  for t in select * from public.rank_titles where kind = 'specialist' and enabled and public.rank_title_is_active(code) loop
    select * into st from public.rank_title_stats(p_student, t.code);
    if st.n >= t.min_questions and st.covered * 2 >= st.total_topics and st.acc >= t.awaken_accuracy then
      perform public.rank_grant_title(p_student, t.code, 'thuc_tinh', p_season, jsonb_build_object('n', st.n, 'acc', st.acc, 'covered', st.covered, 'total', st.total_topics));
    end if;
    if st.n >= t.min_questions * 2 and st.covered = st.total_topics and st.acc >= t.master_accuracy then
      perform public.rank_grant_title(p_student, t.code, 'lam_chu', p_season, jsonb_build_object('n', st.n, 'acc', st.acc, 'covered', st.covered, 'total', st.total_topics));
      if t.legend_challenge_exam_id is not null then
        v_legend := public.rank_best_pct(p_student, t.legend_challenge_exam_id);
        if v_legend >= t.legend_accuracy then
          perform public.rank_grant_title(p_student, t.code, 'huyen_thoai', p_season, jsonb_build_object('exam_id', t.legend_challenge_exam_id, 'pct', v_legend));
        end if;
      end if;
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
  v_legend_best int;
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
      v_legend_best := case when t.legend_challenge_exam_id is null then null else public.rank_best_pct(p_student, t.legend_challenge_exam_id) end;
      v_progress := jsonb_build_object('n', st.n, 'correct', st.correct, 'acc', st.acc, 'covered', st.covered,
        'total_topics', st.total_topics, 'min_questions', t.min_questions,
        'awaken_accuracy', t.awaken_accuracy, 'master_accuracy', t.master_accuracy,
        'legend_exam_id', t.legend_challenge_exam_id, 'legend_accuracy', t.legend_accuracy, 'legend_best', v_legend_best,
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

commit;
