-- ============================================================================
-- Phụ đạo chỉ tính câu Dễ và Trung bình (thầy chốt 11/10/2026)
-- Câu Khó (exam_question_results.difficulty = 'kho') không còn được đếm khi MỞ mục phụ đạo (sai >= 50%, tối thiểu 3 câu)
-- lẫn khi ĐÓNG mục (đúng >= 75%). Câu chưa gắn độ khó (difficulty rỗng, ~3%) vẫn tính như cũ.
-- Định nghĩa lại: refresh_tutoring_needs(uuid). Không đụng dữ liệu cũ: các mục đang mở chỉ được đánh giá lại
-- khi em đó nộp bài kế tiếp (hoặc bấm "Rà lại cả lớp"). Mục chỉ mở vì câu khó: xem file dọn riêng (nếu thầy duyệt).
-- Cách chạy: bash scripts/run-migrations.sh — create or replace hàm, chạy sau mỗi lần nộp nên nên ngoài giờ học sinh làm bài.
-- Rollback: perf/rollback/20261011220000_phu_dao_bo_cau_kho.down.sql
-- ============================================================================

CREATE OR REPLACE FUNCTION public.refresh_tutoring_needs(p_student uuid)
 RETURNS void
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
declare
  v_class bigint;
  v_window int := 2;        -- xét 2 bài gần nhất (câu Khó không tính — xem đầu file migration)
  v_min_q int := 3;         -- cần ít nhất 3 câu cùng chủ đề mới dám kết luận
  v_need_pct numeric := 50; -- sai từ 50% -> cần phụ đạo
  v_clear_pct numeric := 25;-- sai ≤ 25% (đúng ≥ 75%) -> coi như đã khắc phục
begin
  select uc.class_id into v_class
  from public.user_classes uc
  where uc.user_id = p_student and uc.status = 'active'
  order by uc.class_id desc
  limit 1;

  -- (a) mở / cập nhật mục còn hổng
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
      and coalesce(q.difficulty, '') <> 'kho'
    group by coalesce(t.parent_id, q.topic_id), coalesce(nullif(q.form, ''), '')
  )
  insert into public.tutoring_needs
    (student_id, class_id, topic_id, form, wrong, total, pct, source, status)
  select p_student, v_class, a.topic_id, a.form, a.wrong, a.total,
         round(a.wrong * 100.0 / a.total)::int, 'auto', 'open'
  from agg a
  where a.total >= v_min_q and a.wrong * 100.0 / a.total >= v_need_pct
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

  -- (b) làm đúng lại -> đóng mục
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
      and coalesce(q.difficulty, '') <> 'kho'
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
$function$;
