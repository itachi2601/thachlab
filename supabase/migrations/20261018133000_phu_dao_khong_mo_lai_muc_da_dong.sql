-- ============================================================================
-- Sửa lỗi của 20261018120000: cửa sổ trượt 12 câu làm mục ĐÃ ĐÓNG (do đạt bài tự kiểm tra thoát phụ đạo) bị mở lại ngay
-- ở lần refresh kế tiếp dù không có đề kiểm tra mới. Nay mục 'cleared' chỉ mở lại khi có đề kiểm tra mới hơn cleared_at.
-- Khôi phục các mục open mà em đã đạt bài tự kiểm tra và chưa làm đề kiểm tra nào sau đó (phát hiện 18/10/2026: 1 mục).
-- Chạy: bash scripts/run-migrations.sh --only N - lúc nào cũng được. Rollback: perf/rollback/20261018133000_phu_dao_khong_mo_lai_muc_da_dong.down.sql
-- ============================================================================

create or replace function public.refresh_tutoring_needs(p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_class bigint;
  v_window int := 2;          -- phần (b): xét 2 bài gần nhất
  v_roll int := 12;           -- phần (a): cửa sổ trượt 12 câu gần nhất
  v_min_q int := 10;          -- cần >= 10 câu mới dám kết luận
  v_need_pct numeric := 50;   -- sai >= 50% -> cần phụ đạo
  v_fast_q int := 5;          -- đường tắt: >= 5 câu ...
  v_fast_pct numeric := 80;   -- ... mà sai >= 80%
  v_clear_pct numeric := 25;  -- sai <= 25% (đúng >= 75%) -> coi như đã khắc phục
begin
  select uc.class_id into v_class
  from public.user_classes uc
  where uc.user_id = p_student and uc.status = 'active'
  order by uc.class_id desc
  limit 1;

  -- (a) mở / cập nhật mục còn hổng - CHỈ xét đề kiểm tra / BTVN / định kỳ (exam_is_assessment).
  with last_try as (
    select distinct on (er.exam_id) er.id, er.created_at
    from public.exam_results er
    where er.student_id = p_student
      and public.exam_is_assessment(er.exam_id)
    order by er.exam_id, er.created_at desc
  ),
  qs as (
    select lt.created_at, q.question_index, q.is_correct,
           coalesce(t.parent_id, q.topic_id) as topic_id,
           coalesce(nullif(q.form, ''), '') as form
    from last_try lt
    join public.exam_question_results q on q.exam_result_id = lt.id
    join public.question_topics t on t.id = q.topic_id
    where q.student_id = p_student and q.topic_id is not null
  ),
  ranked as (
    select qs.*, row_number() over (partition by topic_id, form
                                    order by created_at desc, question_index) as rn
    from qs
  ),
  agg as (
    select topic_id, form,
           (count(*))::int as total,
           (count(*) filter (where not is_correct))::int as wrong,
           max(created_at) as last_at
    from ranked
    where rn <= v_roll
    group by topic_id, form
  ),
  recent as (
    select exam_id from (
      select er.exam_id, max(er.created_at) as last_at
      from public.exam_results er
      where er.student_id = p_student and public.exam_is_assessment(er.exam_id)
      group by er.exam_id
      order by last_at desc
      limit v_window
    ) x
  ),
  cur_try as (
    select distinct on (er.exam_id) er.id
    from public.exam_results er
    join recent r on r.exam_id = er.exam_id
    where er.student_id = p_student
    order by er.exam_id, er.created_at desc
  ),
  cur as (
    select coalesce(t.parent_id, q.topic_id) as topic_id,
           coalesce(nullif(q.form, ''), '') as form,
           (count(*))::int as total,
           (count(*) filter (where not q.is_correct))::int as wrong
    from public.exam_question_results q
    join cur_try ct on ct.id = q.exam_result_id
    join public.question_topics t on t.id = q.topic_id
    where q.student_id = p_student and q.topic_id is not null
    group by coalesce(t.parent_id, q.topic_id), coalesce(nullif(q.form, ''), '')
  )
  insert into public.tutoring_needs
    (student_id, class_id, topic_id, form, wrong, total, pct, source, status)
  select p_student, v_class, a.topic_id, a.form, a.wrong, a.total,
         round(a.wrong * 100.0 / a.total)::int, 'auto', 'open'
  from agg a
  left join cur c on c.topic_id = a.topic_id and c.form = a.form
  left join public.tutoring_needs tn on tn.student_id = p_student and tn.topic_id = a.topic_id and tn.form = a.form
  where ((a.total >= v_min_q and a.wrong * 100.0 / a.total >= v_need_pct)
      or (a.total >= v_fast_q and a.wrong * 100.0 / a.total >= v_fast_pct))
    and not (c.total >= 2 and c.wrong * 100.0 / c.total <= v_clear_pct)
    -- mục đã đóng (kể cả do đạt bài tự kiểm tra) chỉ mở lại khi có đề kiểm tra MỚI hơn lúc đóng
    and (tn.status is distinct from 'cleared' or a.last_at > coalesce(tn.cleared_at, tn.updated_at))
  on conflict (student_id, topic_id, form) do update set
    wrong = excluded.wrong,
    total = excluded.total,
    pct = excluded.pct,
    class_id = coalesce(excluded.class_id, tutoring_needs.class_id),
    last_seen_at = now(),
    status = case when tutoring_needs.status in ('cleared', 'dismissed')
                  then 'open' else tutoring_needs.status end,
    cleared_at = case when tutoring_needs.status in ('cleared', 'dismissed')
                  then null else tutoring_needs.cleared_at end,
    note = case when tutoring_needs.status in ('cleared', 'dismissed')
                  then '' else tutoring_needs.note end;

  -- (b) làm đúng lại -> đóng mục (giữ nguyên như bản 17/10/2026)
  with recent as (
    select er.exam_id
    from public.exam_results er
    where er.student_id = p_student
    group by er.exam_id
    order by max(er.created_at) desc
    limit v_window
  ),
  last_try as (
    select distinct on (er.exam_id) er.id
    from public.exam_results er
    join recent r on r.exam_id = er.exam_id
    where er.student_id = p_student
    order by er.exam_id, er.created_at desc
  ),
  agg as (
    select coalesce(t.parent_id, q.topic_id) as topic_id,
           coalesce(nullif(q.form, ''), '') as form,
           (count(*))::int as total,
           (count(*) filter (where not q.is_correct))::int as wrong
    from public.exam_question_results q
    join last_try lt on lt.id = q.exam_result_id
    join public.question_topics t on t.id = q.topic_id
    where q.student_id = p_student and q.topic_id is not null
    group by coalesce(t.parent_id, q.topic_id), coalesce(nullif(q.form, ''), '')
  )
  update public.tutoring_needs n
  set status = 'cleared',
      cleared_at = now(),
      last_seen_at = now(),
      wrong = a.wrong,
      total = a.total,
      pct = round(a.wrong * 100.0 / a.total)::int,
      note = case when n.note <> '' then n.note
                  when n.tutored_at is not null then 'đã phụ đạo, bài sau làm đúng lại'
                  else 'tự khắc phục, không cần phụ đạo' end
  from agg a
  where n.student_id = p_student
    and n.topic_id = a.topic_id
    and n.form = a.form
    and n.status in ('open', 'assigned', 'tutored')
    and a.total >= 2
    and a.wrong * 100.0 / a.total <= v_clear_pct;
end;
$$;

update public.tutoring_needs n
set status = 'cleared', cleared_at = now(), updated_at = now(),
    note = 'đạt bài tự kiểm tra thoát phụ đạo (khôi phục 18/10/2026)'
where n.status = 'open'
  and exists (select 1 from public.tutoring_exit_attempts a
              where a.tutoring_need_id = n.id and a.passed
                and not exists (select 1 from public.exam_results er
                                where er.student_id = a.student_id and er.created_at > a.created_at
                                  and public.exam_is_assessment(er.exam_id)));
