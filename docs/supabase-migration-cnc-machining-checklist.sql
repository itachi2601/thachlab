-- Mở rộng checklist chấm chéo thực hành CNC sang Bài 6 (Gia công tiện, lesson-5)
-- và Bài 7 (Gia công phay, lesson-6) — kiểm tra thực hành gia công (an toàn, quy
-- trình, đo kiểm sản phẩm, 5S), tương tự checklist cài đặt dao/phôi của lesson-4-turn/mill.
-- Áp dụng sau docs/supabase-migration-cnc-checklist.sql và
-- docs/supabase-migration-checklist-validity.sql.

alter table public.checklist_sessions drop constraint if exists checklist_sessions_lesson_id_check;
alter table public.checklist_sessions add constraint checklist_sessions_lesson_id_check
  check (lesson_id in ('lesson-4-turn', 'lesson-4-mill', 'lesson-5', 'lesson-6'));

-- Thay điều kiện được phép chấm chéo cho phù hợp với từng bài: lesson-4-turn/mill vẫn yêu cầu
-- người chấm đã đạt 2 bài lý thuyết (machine-operation, tool-setup); lesson-5/lesson-6 (gia công
-- thực tế) yêu cầu người chấm đã được giảng viên duyệt bản vẽ bài tập tổng hợp (assessment_id='final')
-- của chính bài đó, tức đủ điều kiện tự gia công trước khi được chấm cho bạn học.
create or replace function public.submit_checklist_result(p_course_id bigint,p_code text,p_student_id uuid,p_lesson_id text,p_item_results jsonb,p_score numeric,p_critical_ok boolean,p_zero_tolerance_ok boolean,p_passed boolean)
returns jsonb language plpgsql security definer set search_path=public as $$
declare s public.checklist_sessions%rowtype; w public.checklist_work_starts%rowtype; v_grader_role text; v_now timestamptz:=now(); v_local_time time;
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  if p_student_id=auth.uid() then raise exception 'Không thể tự chấm cho chính mình.'; end if;
  v_local_time:=v_now at time zone 'Asia/Ho_Chi_Minh';
  if v_local_time<time '06:30' or v_local_time>time '11:00' then raise exception 'Checklist chỉ có hiệu lực từ 06:30 đến 11:00 sáng.'; end if;
  select * into s from public.checklist_sessions where course_id=p_course_id and lesson_id=p_lesson_id and code=trim(p_code) and status='open' order by created_at desc limit 1;
  if s.id is null then raise exception 'Mã phiên chấm không đúng hoặc phiên đã đóng.'; end if;
  if v_now<s.starts_at or v_now>s.closes_at then raise exception 'Phiên chấm chưa bắt đầu hoặc đã hết thời gian.'; end if;
  select * into w from public.checklist_work_starts where session_id=s.id and student_id=p_student_id and grader_id=auth.uid();
  if w.started_at is null then raise exception 'Bạn chưa bắt đầu lượt checklist hợp lệ.'; end if;
  if v_now-w.started_at<interval '4 minutes' then raise exception 'Checklist phải được thực hiện tối thiểu 4 phút.'; end if;
  if not exists(select 1 from public.course_enrollments where course_id=p_course_id and student_id=p_student_id and status='active') then raise exception 'Học sinh được chấm không thuộc khóa học này.'; end if;
  if public.is_admin() then v_grader_role:='teacher'; else
    if not exists(select 1 from public.course_enrollments where course_id=p_course_id and student_id=auth.uid() and status='active') then raise exception 'Bạn chưa thuộc khóa học này.'; end if;
    if p_lesson_id in ('lesson-4-turn','lesson-4-mill') then
      if not exists(select 1 from public.cnc_learning_records where course_id=p_course_id and student_id=auth.uid() and lesson_id=p_lesson_id and assessment_id in('machine-operation','tool-setup') and completed=true group by student_id having count(distinct assessment_id)=2) then raise exception 'Bạn cần đạt cả 2 bài kiểm tra vận hành máy và cài đặt dao trước khi được chấm chéo cho bạn khác.'; end if;
    else
      if not exists(select 1 from public.cnc_learning_records where course_id=p_course_id and student_id=auth.uid() and lesson_id=p_lesson_id and assessment_id='final' and completed=true) then raise exception 'Bạn cần được giảng viên duyệt bản vẽ bài tập tổng hợp trước khi được chấm chéo cho bạn khác.'; end if;
    end if;
    v_grader_role:='peer';
  end if;
  insert into public.checklist_attempts(session_id,course_id,lesson_id,student_id,grader_id,grader_role,item_results,score,total,critical_ok,zero_tolerance_ok,passed,started_at,duration_seconds)
  values(s.id,p_course_id,p_lesson_id,p_student_id,auth.uid(),v_grader_role,coalesce(p_item_results,'{}'::jsonb),p_score,10,p_critical_ok,p_zero_tolerance_ok,p_passed,w.started_at,floor(extract(epoch from(v_now-w.started_at))));
  insert into public.cnc_learning_records(course_id,student_id,lesson_id,assessment_id,completed,latest_score,best_score,total_questions,attempt_count,last_activity_at)
  values(p_course_id,p_student_id,p_lesson_id,'checklist',p_passed,round(p_score),round(p_score),10,1,v_now)
  on conflict(course_id,student_id,lesson_id,assessment_id) do update set completed=cnc_learning_records.completed or excluded.completed,latest_score=excluded.latest_score,best_score=greatest(coalesce(cnc_learning_records.best_score,0),excluded.best_score),total_questions=excluded.total_questions,attempt_count=cnc_learning_records.attempt_count+1,last_activity_at=v_now;
  delete from public.checklist_work_starts where session_id=s.id and student_id=p_student_id and grader_id=auth.uid();
  return jsonb_build_object('passed',p_passed,'score',p_score,'grader_role',v_grader_role,'session_title',s.title);
end $$;
revoke all on function public.submit_checklist_result(bigint,text,uuid,text,jsonb,numeric,boolean,boolean,boolean) from public;
grant execute on function public.submit_checklist_result(bigint,text,uuid,text,jsonb,numeric,boolean,boolean,boolean) to authenticated;
