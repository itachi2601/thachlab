-- ============================================================================
-- Vá bảo mật (tiếp rà soát 11/11/2026): record_cnc_learning_result kiểm đầu vào + thôi mở cho anon.
-- Hàm vẫn nhận điểm do máy học sinh gửi (chấm server là việc riêng, cần đổi client) — bản này chỉ chặn số liệu vô lý:
-- điểm âm, điểm > tổng câu, tổng câu > 500, mã bài/mã bài kiểm quá dài hoặc rỗng. Phần ghi giữ nguyên.
-- Chạy lúc nào cũng được: chỉ thay thân hàm, không quét/ghi dữ liệu. Client hiện tại gọi đúng như cũ.
--
-- Rollback: perf/rollback/20261112070000_cnc_learning_result_kiem_dau_vao.down.sql
-- ============================================================================
begin;

create or replace function public.record_cnc_learning_result(
  p_course_id bigint, p_lesson_id text, p_assessment_id text default 'final',
  p_score integer default null, p_total integer default null, p_completed boolean default false)
returns void
language plpgsql security definer set search_path = public
as $function$
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if not exists (
    select 1 from public.course_enrollments
    where course_id = p_course_id and student_id = auth.uid() and status = 'active'
  ) then raise exception 'Bạn chưa được duyệt vào khóa học này.'; end if;

  if coalesce(btrim(p_lesson_id), '') = '' or length(p_lesson_id) > 80
     or coalesce(btrim(p_assessment_id), '') = '' or length(p_assessment_id) > 80 then
    raise exception 'Mã bài không hợp lệ.' using errcode = '22023';
  end if;
  if p_total is not null and (p_total < 0 or p_total > 500) then
    raise exception 'Kết quả không hợp lệ.' using errcode = '22023';
  end if;
  if p_score is not null and (p_score < 0 or p_total is null or p_score > p_total) then
    raise exception 'Kết quả không hợp lệ.' using errcode = '22023';
  end if;

  insert into public.cnc_learning_records (
    course_id, student_id, lesson_id, assessment_id, completed, latest_score, best_score,
    total_questions, attempt_count, last_activity_at
  ) values (
    p_course_id, auth.uid(), p_lesson_id, p_assessment_id, p_completed, p_score, p_score,
    p_total, case when p_score is null then 0 else 1 end, now()
  )
  on conflict (course_id, student_id, lesson_id, assessment_id) do update set
    completed = cnc_learning_records.completed or excluded.completed,
    latest_score = coalesce(excluded.latest_score, cnc_learning_records.latest_score),
    best_score = case
      when excluded.best_score is null then cnc_learning_records.best_score
      else greatest(coalesce(cnc_learning_records.best_score, 0), excluded.best_score)
    end,
    total_questions = coalesce(excluded.total_questions, cnc_learning_records.total_questions),
    attempt_count = cnc_learning_records.attempt_count + case when p_score is null then 0 else 1 end,
    last_activity_at = now();
end;
$function$;

revoke all on function public.record_cnc_learning_result(bigint, text, text, integer, integer, boolean) from public, anon;
grant execute on function public.record_cnc_learning_result(bigint, text, text, integer, integer, boolean) to authenticated;

commit;
