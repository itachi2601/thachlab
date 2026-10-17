-- ============================================================================
-- Phụ đạo không sinh từ đề luyện tập (thầy chốt 17/10/2026)
--
-- Trước: refresh_tutoring_needs xét 2 đề gần nhất BẤT KỂ loại → làm sai một đề luyện 5 câu (không tính RP) là lập tức
-- có mục "Phụ đạo" đứng đầu thẻ Hôm nay. Nghiên cứu trong repo (docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md, SDT;
-- docs/mastery-rules.md) và quy tắc thiết kế: đề luyện là chỗ an toàn để sai, phụ đạo chỉ mở từ bài có tính điểm.
--
-- Đổi:
--   1. exam_is_assessment(exam_id): đề nằm trong mục Kiểm tra / BTVN của bài học, đề định kỳ lớp (class_assessments),
--      BTVN cả lớp (class_announcements.exam_id), BTVN trợ giảng giao riêng (ta_homework_assignments), đề ôn câu sai
--      (class_review_homework). Còn lại (Luyện tập, Kiểm tra nhanh, bài tập mẫu, đề mở từ kệ chưa gắn mục) = luyện.
--   2. refresh_tutoring_needs: phần (a) mở mục chỉ xét 2 đề KIỂM TRA gần nhất; phần (b) đóng mục vẫn xét mọi đề
--      (làm đúng lại ở đề luyện cũng là bằng chứng tốt).
--   3. Dọn một lần: mục 'auto' đang 'open' (chưa giao trợ giảng) → đánh dấu dismissed kèm ghi chú, rồi chạy lại
--      refresh cho từng em: mục nào còn hổng theo đề kiểm tra tự mở lại (note về ''), mục chỉ vì đề luyện thì ở lại dismissed.
--      Mục 'assigned'/'tutored' KHÔNG đụng (trợ giảng đang làm).
-- Chạy: bash scripts/run-migrations.sh --only N — lúc nào cũng được (chỉ thay hàm + cập nhật trạng thái mục phụ đạo).
-- Rollback: perf/rollback/20261017230000_phu_dao_bo_de_luyen_tap.down.sql
-- ============================================================================

create or replace function public.exam_is_assessment(p_exam bigint)
returns boolean
language sql stable security definer set search_path = public
as $$
  select exists (select 1 from public.lesson_items li
                 where li.kind in ('kiem_tra', 'bai_tap_ve_nha') and p_exam = any (li.exam_ids))
      or exists (select 1 from public.class_assessments ca where ca.exam_id = p_exam)
      or exists (select 1 from public.class_announcements an where an.exam_id = p_exam)
      or exists (select 1 from public.ta_homework_assignments ta where ta.exam_id = p_exam)
      or exists (select 1 from public.class_review_homework rh where rh.exam_id = p_exam);
$$;
revoke all on function public.exam_is_assessment(bigint) from public, anon;
grant execute on function public.exam_is_assessment(bigint) to authenticated;

create or replace function public.refresh_tutoring_needs(p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_class bigint;
  v_window int := 2;        -- xét 2 bài gần nhất
  v_min_q int := 3;         -- cần ít nhất 3 câu cùng chủ đề mới dám kết luận
  v_need_pct numeric := 50; -- sai từ 50% -> cần phụ đạo
  v_clear_pct numeric := 25;-- sai ≤ 25% (đúng ≥ 75%) -> coi như đã khắc phục
begin
  select uc.class_id into v_class
  from public.user_classes uc
  where uc.user_id = p_student and uc.status = 'active'
  order by uc.class_id desc
  limit 1;

  -- (a) mở / cập nhật mục còn hổng — CHỈ xét đề kiểm tra / BTVN / định kỳ (exam_is_assessment).
  -- Đề luyện tập, Kiểm tra nhanh lý thuyết, bài tập mẫu là chỗ an toàn để sai (thầy chốt 17/10/2026).
  with recent as (
    select er.exam_id
    from public.exam_results er
    where er.student_id = p_student
      and public.exam_is_assessment(er.exam_id)
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

-- 3. Dọn một lần các mục đang mở chỉ vì đề luyện tập.
do $$
declare r record; v_before int; v_after int;
begin
  select count(*) into v_before from public.tutoring_needs where source = 'auto' and status = 'open';
  update public.tutoring_needs
    set status = 'dismissed', note = 'sinh từ đề luyện tập, bỏ 17/10/2026', updated_at = now()
  where source = 'auto' and status = 'open';
  for r in select distinct student_id from public.tutoring_needs where note = 'sinh từ đề luyện tập, bỏ 17/10/2026' loop
    perform public.refresh_tutoring_needs(r.student_id);
  end loop;
  select count(*) into v_after from public.tutoring_needs where source = 'auto' and status = 'open';
  raise notice 'Mục auto đang mở: trước % → sau % (số còn lại dismissed vì chỉ do đề luyện: %)',
    v_before, v_after, (select count(*) from public.tutoring_needs where note = 'sinh từ đề luyện tập, bỏ 17/10/2026');
end $$;
