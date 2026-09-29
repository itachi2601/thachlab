-- ROLLBACK cho supabase/migrations/20260925140000_perf_rls.sql
-- Định nghĩa policy + hàm helper Y NGUYÊN như trên DB ngày 25/9/2026 (dump pg_policies /
-- pg_get_functiondef trước khi sửa). Chạy cả file trong SQL Editor để quay về trạng thái cũ.
begin;

CREATE OR REPLACE FUNCTION public.assists_class(p_class bigint)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select exists (
    select 1
    from public.ta_assistant_classes tac
    join public.ta_assistants a on a.id = tac.assistant_id
    where tac.class_id = p_class and a.user_id = auth.uid() and a.active
  );
$function$;

CREATE OR REPLACE FUNCTION public.can_manage_class(p_class_id bigint)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select public.is_admin() or exists (
    select 1 from public.class_instructors
    where class_id = p_class_id and instructor_id = auth.uid()
  );
$function$;

CREATE OR REPLACE FUNCTION public.can_manage_course(p_course_id bigint)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select public.is_admin() or exists (
    select 1 from public.course_instructors
    where course_id = p_course_id and instructor_id = auth.uid()
  );
$function$;

CREATE OR REPLACE FUNCTION public.get_periodic_rank(p_class_id bigint)
 RETURNS TABLE(rnk integer, total integer, my_avg numeric, class_avg numeric)
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select * from public.get_periodic_rank_of(auth.uid(), p_class_id);
$function$;

CREATE OR REPLACE FUNCTION public.is_admin()
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role = 'admin'
  );
$function$;

CREATE OR REPLACE FUNCTION public.is_course_member(p_course_id bigint)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select exists (
    select 1 from public.course_enrollments
    where course_id = p_course_id and student_id = auth.uid() and status = 'active'
  );
$function$;

CREATE OR REPLACE FUNCTION public.is_homeroom_classmate(p_profile_id uuid)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select exists (
    select 1 from public.course_enrollments e
    join public.homeroom_monitors m on m.course_id = e.course_id
    where e.student_id = p_profile_id and m.student_id = auth.uid()
  );
$function$;

CREATE OR REPLACE FUNCTION public.is_homeroom_monitor(p_course_id bigint)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select exists (
    select 1 from public.homeroom_monitors
    where course_id = p_course_id and student_id = auth.uid()
  );
$function$;

CREATE OR REPLACE FUNCTION public.is_parent_of(p_student uuid)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select exists (
    select 1 from public.parent_links
    where parent_id = auth.uid() and student_id = p_student and claimed_at is not null
  );
$function$;

CREATE OR REPLACE FUNCTION public.manages_class(p_class bigint)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select public.is_admin() or exists (
    select 1 from public.class_instructors ci
    where ci.class_id = p_class and ci.instructor_id = auth.uid()
  );
$function$;

CREATE OR REPLACE FUNCTION public.rank_is_staff()
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select public.is_admin() or exists (
    select 1 from public.profiles p
    where p.id = auth.uid() and p.role = 'instructor' and p.admin_area = 'thpt'
  );
$function$;

CREATE OR REPLACE FUNCTION public.rank_my_status()
 RETURNS jsonb
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$ select public.rank_status_of(auth.uid()); $function$;

CREATE OR REPLACE FUNCTION public.rank_my_titles()
 RETURNS jsonb
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$ select public.rank_titles_of(auth.uid()); $function$;

CREATE OR REPLACE FUNCTION public.student_outcome_gaps(p_students uuid[], p_window integer DEFAULT 2)
 RETURNS TABLE(student_id uuid, parent_topic_id bigint, topic_id bigint, topic_name text, form text, total integer, wrong integer)
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  with students as (
    select s.id
    from unnest(coalesce(p_students, '{}'::uuid[])) as s(id)
    where s.id = auth.uid() or public.teaches_student(s.id) or public.is_parent_of(s.id)
  ),
  recent as (
    select er.student_id, er.exam_id, row_number() over (
             partition by er.student_id order by max(er.created_at) desc
           ) as rn
    from public.exam_results er
    join students s on s.id = er.student_id
    group by er.student_id, er.exam_id
  ),
  last_try as (
    select distinct on (er.student_id, er.exam_id) er.id
    from public.exam_results er
    join recent r on r.student_id = er.student_id and r.exam_id = er.exam_id
    where r.rn <= greatest(p_window, 1)
    order by er.student_id, er.exam_id, er.created_at desc
  )
  select q.student_id,
         coalesce(t.parent_id, q.topic_id) as parent_topic_id,
         q.topic_id,
         coalesce(t.name, q.topic_name) as topic_name,
         coalesce(nullif(q.form, ''), '') as form,
         (count(*))::int as total,
         (count(*) filter (where not q.is_correct))::int as wrong
  from public.exam_question_results q
  join last_try lt on lt.id = q.exam_result_id
  left join public.question_topics t on t.id = q.topic_id
  where q.topic_id is not null
  group by q.student_id, coalesce(t.parent_id, q.topic_id), q.topic_id,
           coalesce(t.name, q.topic_name), coalesce(nullif(q.form, ''), '')
  having count(*) filter (where not q.is_correct) > 0
  order by 1, 2, 7 desc, 6 desc;
$function$;

CREATE OR REPLACE FUNCTION public.ta_current_assistant_id()
 RETURNS uuid
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select id from public.ta_assistants where user_id = auth.uid();
$function$;

CREATE OR REPLACE FUNCTION public.teaches_student(p_student uuid)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select public.is_admin() or exists (
    select 1
    from public.user_classes uc
    join public.class_instructors ci on ci.class_id = uc.class_id
    where uc.user_id = p_student and ci.instructor_id = auth.uid()
  ) or exists (
    select 1
    from public.user_classes uc
    join public.ta_assistant_classes tac on tac.class_id = uc.class_id
    join public.ta_assistants a on a.id = tac.assistant_id
    where uc.user_id = p_student and a.user_id = auth.uid() and a.active
  );
$function$;

CREATE OR REPLACE FUNCTION public.thpt_has_registration(p_course_id bigint)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select auth.uid() is not null and exists (
    select 1 from public.thpt_registrations r
    where r.course_id = p_course_id
      and (r.student_id = auth.uid()
           or r.registered_by = auth.uid()
           or (r.student_id is not null and public.is_parent_of(r.student_id)))
  );
$function$;

CREATE OR REPLACE FUNCTION public.unread_notification_count()
 RETURNS integer
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select count(*)::int from public.notifications where user_id = auth.uid() and read_at is null;
$function$;

drop policy if exists "students read attendance machine photos" on public.attendance_machine_photos;
create policy "students read attendance machine photos" on public.attendance_machine_photos
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM (attendance_sessions s
     JOIN course_enrollments e ON (((e.course_id = s.course_id) AND (e.student_id = auth.uid()) AND (e.status = 'active'::text))))
  WHERE (s.id = attendance_machine_photos.session_id)))));

drop policy if exists "students read attendance machine scores" on public.attendance_machine_scores;
create policy "students read attendance machine scores" on public.attendance_machine_scores
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM (attendance_sessions s
     JOIN course_enrollments e ON (((e.course_id = s.course_id) AND (e.student_id = auth.uid()) AND (e.status = 'active'::text))))
  WHERE (s.id = attendance_machine_scores.session_id)))));

drop policy if exists "students read own attendance" on public.attendance_records;
create policy "students read own attendance" on public.attendance_records
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_admin()));

drop policy if exists "students read course attendance sessions" on public.attendance_sessions;
create policy "students read course attendance sessions" on public.attendance_sessions
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM course_enrollments e
  WHERE ((e.course_id = e.course_id) AND (e.student_id = auth.uid()) AND (e.status = 'active'::text))))));

drop policy if exists "anyone reports bug" on public.bug_reports;
create policy "anyone reports bug" on public.bug_reports
  as permissive
  for insert
  to anon, authenticated
  with check (((user_id IS NULL) OR (user_id = auth.uid())));

drop policy if exists "read own or admin bug reports" on public.bug_reports;
create policy "read own or admin bug reports" on public.bug_reports
  as permissive
  for select
  to authenticated
  using (((user_id = auth.uid()) OR is_admin()));

drop policy if exists "students read own or graded checklist attempts" on public.checklist_attempts;
create policy "students read own or graded checklist attempts" on public.checklist_attempts
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (student_id = auth.uid()) OR (grader_id = auth.uid())));

drop policy if exists "students read course checklist sessions" on public.checklist_sessions;
create policy "students read course checklist sessions" on public.checklist_sessions
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM course_enrollments e
  WHERE ((e.course_id = checklist_sessions.course_id) AND (e.student_id = auth.uid()) AND (e.status = 'active'::text))))));

drop policy if exists "staff post announcements" on public.class_announcements;
create policy "staff post announcements" on public.class_announcements
  as permissive
  for insert
  to authenticated
  with check (((created_by = auth.uid()) AND (manages_class(class_id) OR assists_class(class_id) OR is_admin())));

drop policy if exists "students read class announcements" on public.class_announcements;
create policy "students read class announcements" on public.class_announcements
  as permissive
  for select
  to authenticated
  using ((EXISTS ( SELECT 1
   FROM user_classes uc
  WHERE ((uc.user_id = auth.uid()) AND (uc.class_id = class_announcements.class_id) AND (uc.status = 'active'::text)))));

drop policy if exists "instructors read own class assignments" on public.class_instructors;
create policy "instructors read own class assignments" on public.class_instructors
  as permissive
  for select
  to authenticated
  using (((instructor_id = auth.uid()) OR is_admin()));

drop policy if exists "students read own competency permissions" on public.cnc_competency_permissions;
create policy "students read own competency permissions" on public.cnc_competency_permissions
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_admin()));

drop policy if exists "students read own cnc drawings" on public.cnc_drawing_submissions;
create policy "students read own cnc drawings" on public.cnc_drawing_submissions
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_admin()));

drop policy if exists "students resubmit rejected cnc drawings" on public.cnc_drawing_submissions;
create policy "students resubmit rejected cnc drawings" on public.cnc_drawing_submissions
  as permissive
  for update
  to authenticated
  using (((student_id = auth.uid()) AND (status = 'rejected'::text)))
  with check (((student_id = auth.uid()) AND (status = 'pending'::text) AND (reviewed_by IS NULL) AND (reviewed_at IS NULL)));

drop policy if exists "students submit own cnc drawings" on public.cnc_drawing_submissions;
create policy "students submit own cnc drawings" on public.cnc_drawing_submissions
  as permissive
  for insert
  to authenticated
  with check (((student_id = auth.uid()) AND (status = 'pending'::text) AND (reviewed_by IS NULL) AND (reviewed_at IS NULL)));

drop policy if exists "students read own cnc learning records" on public.cnc_learning_records;
create policy "students read own cnc learning records" on public.cnc_learning_records
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_admin()));

drop policy if exists "students read own enrollment" on public.course_enrollments;
create policy "students read own enrollment" on public.course_enrollments
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_admin()));

drop policy if exists "students read own course grade overrides" on public.course_grade_overrides;
create policy "students read own course grade overrides" on public.course_grade_overrides
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_admin()));

drop policy if exists "instructors read own assignments" on public.course_instructors;
create policy "instructors read own assignments" on public.course_instructors
  as permissive
  for select
  to authenticated
  using (((instructor_id = auth.uid()) OR is_admin()));

drop policy if exists "students read joined courses" on public.course_offerings;
create policy "students read joined courses" on public.course_offerings
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM course_enrollments e
  WHERE ((e.course_id = course_offerings.id) AND (e.student_id = auth.uid()))))));

drop policy if exists "students read equipment breakdown reports" on public.equipment_breakdown_reports;
create policy "students read equipment breakdown reports" on public.equipment_breakdown_reports
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM course_enrollments e
  WHERE ((e.course_id = e.course_id) AND (e.student_id = auth.uid()) AND (e.status = 'active'::text))))));

drop policy if exists "student inserts own attempt" on public.exam_attempts;
create policy "student inserts own attempt" on public.exam_attempts
  as permissive
  for insert
  to authenticated
  with check ((student_id = auth.uid()));

drop policy if exists "student reads own attempts" on public.exam_attempts;
create policy "student reads own attempts" on public.exam_attempts
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id)));

drop policy if exists "student updates own open attempt" on public.exam_attempts;
create policy "student updates own open attempt" on public.exam_attempts
  as permissive
  for update
  to authenticated
  using (((student_id = auth.uid()) AND (submitted_at IS NULL)))
  with check ((student_id = auth.uid()));

drop policy if exists "student inserts own question results" on public.exam_question_results;
create policy "student inserts own question results" on public.exam_question_results
  as permissive
  for insert
  to authenticated
  with check ((student_id = auth.uid()));

drop policy if exists "student reads own question results" on public.exam_question_results;
create policy "student reads own question results" on public.exam_question_results
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id)));

drop policy if exists "assigned instructors read student results" on public.exam_results;
create policy "assigned instructors read student results" on public.exam_results
  as permissive
  for select
  to authenticated
  using ((EXISTS ( SELECT 1
   FROM (user_classes uc
     JOIN class_instructors ci ON ((ci.class_id = uc.class_id)))
  WHERE ((uc.user_id = exam_results.student_id) AND (ci.instructor_id = auth.uid())))));

drop policy if exists "student inserts own result" on public.exam_results;
create policy "student inserts own result" on public.exam_results
  as permissive
  for insert
  to authenticated
  with check ((student_id = auth.uid()));

drop policy if exists "student reads own results" on public.exam_results;
create policy "student reads own results" on public.exam_results
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_admin()));

drop policy if exists "class members read homeroom monitors" on public.homeroom_monitors;
create policy "class members read homeroom monitors" on public.homeroom_monitors
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_course_member(course_id)));

drop policy if exists "students read own homeroom term records" on public.homeroom_term_records;
create policy "students read own homeroom term records" on public.homeroom_term_records
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_admin()));

drop policy if exists "student manages own progress" on public.lesson_progress;
create policy "student manages own progress" on public.lesson_progress
  as permissive
  for all
  to authenticated
  using (((user_id = auth.uid()) OR is_admin()))
  with check ((user_id = auth.uid()));

drop policy if exists "admin sends messages" on public.messages;
create policy "admin sends messages" on public.messages
  as permissive
  for insert
  to authenticated
  with check ((is_admin() AND (sender_id = auth.uid())));

drop policy if exists "read own messages" on public.messages;
create policy "read own messages" on public.messages
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (recipient_id = auth.uid()) OR ((recipient_id IS NULL) AND ((class_name IS NULL) OR (class_name = ( SELECT profiles.class_name
   FROM profiles
  WHERE (profiles.id = auth.uid())))))));

drop policy if exists "delete own notifications" on public.notifications;
create policy "delete own notifications" on public.notifications
  as permissive
  for delete
  to authenticated
  using ((user_id = auth.uid()));

drop policy if exists "mark own notifications read" on public.notifications;
create policy "mark own notifications read" on public.notifications
  as permissive
  for update
  to authenticated
  using ((user_id = auth.uid()))
  with check ((user_id = auth.uid()));

drop policy if exists "read own notifications" on public.notifications;
create policy "read own notifications" on public.notifications
  as permissive
  for select
  to authenticated
  using ((user_id = auth.uid()));

drop policy if exists "parent reads own links" on public.parent_links;
create policy "parent reads own links" on public.parent_links
  as permissive
  for select
  to authenticated
  using ((parent_id = auth.uid()));

drop policy if exists "student inserts own practice question results" on public.practice_question_results;
create policy "student inserts own practice question results" on public.practice_question_results
  as permissive
  for insert
  to authenticated
  with check ((student_id = auth.uid()));

drop policy if exists "student reads own practice question results" on public.practice_question_results;
create policy "student reads own practice question results" on public.practice_question_results
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id)));

drop policy if exists "student inserts own practice sessions" on public.practice_sessions;
create policy "student inserts own practice sessions" on public.practice_sessions
  as permissive
  for insert
  to authenticated
  with check ((student_id = auth.uid()));

drop policy if exists "student reads own practice sessions" on public.practice_sessions;
create policy "student reads own practice sessions" on public.practice_sessions
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id)));

drop policy if exists "assigned instructors read student profiles" on public.profiles;
create policy "assigned instructors read student profiles" on public.profiles
  as permissive
  for select
  to authenticated
  using ((EXISTS ( SELECT 1
   FROM (user_classes uc
     JOIN class_instructors ci ON ((ci.class_id = uc.class_id)))
  WHERE ((uc.user_id = profiles.id) AND (ci.instructor_id = auth.uid())))));

drop policy if exists "instructors read enrolled student profiles" on public.profiles;
create policy "instructors read enrolled student profiles" on public.profiles
  as permissive
  for select
  to authenticated
  using ((EXISTS ( SELECT 1
   FROM (course_enrollments e
     JOIN course_instructors ci ON ((ci.course_id = e.course_id)))
  WHERE ((e.student_id = profiles.id) AND (ci.instructor_id = auth.uid())))));

drop policy if exists "parent updates own profile" on public.profiles;
create policy "parent updates own profile" on public.profiles
  as permissive
  for update
  to authenticated
  using (((id = auth.uid()) AND (role = 'parent'::text)))
  with check (((id = auth.uid()) AND (role = 'parent'::text)));

drop policy if exists "read own profile" on public.profiles;
create policy "read own profile" on public.profiles
  as permissive
  for select
  to authenticated
  using (((id = auth.uid()) OR is_admin()));

drop policy if exists "update own profile" on public.profiles;
create policy "update own profile" on public.profiles
  as permissive
  for update
  to authenticated
  using ((id = auth.uid()))
  with check (((id = auth.uid()) AND (role = 'student'::text)));

drop policy if exists "staff manage question bank" on public.question_bank;
create policy "staff manage question bank" on public.question_bank
  as permissive
  for all
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM profiles p
  WHERE ((p.id = auth.uid()) AND (p.role = 'instructor'::text) AND (p.admin_area = 'thpt'::text))))))
  with check ((is_admin() OR (EXISTS ( SELECT 1
   FROM profiles p
  WHERE ((p.id = auth.uid()) AND (p.role = 'instructor'::text) AND (p.admin_area = 'thpt'::text))))));

drop policy if exists "student reads exit-quiz bank questions" on public.question_bank;
create policy "student reads exit-quiz bank questions" on public.question_bank
  as permissive
  for select
  to authenticated
  using (((archived = false) AND (EXISTS ( SELECT 1
   FROM tutoring_needs n
  WHERE ((n.student_id = auth.uid()) AND (n.topic_id = question_bank.topic_id) AND (n.status = ANY (ARRAY['open'::text, 'assigned'::text, 'tutored'::text])))))));

drop policy if exists "staff manage question topics" on public.question_topics;
create policy "staff manage question topics" on public.question_topics
  as permissive
  for all
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM profiles p
  WHERE ((p.id = auth.uid()) AND (p.role = 'instructor'::text) AND (p.admin_area = 'thpt'::text))))))
  with check ((is_admin() OR (EXISTS ( SELECT 1
   FROM profiles p
  WHERE ((p.id = auth.uid()) AND (p.role = 'instructor'::text) AND (p.admin_area = 'thpt'::text))))));

drop policy if exists "read own rank_fix_attempts" on public.rank_fix_attempts;
create policy "read own rank_fix_attempts" on public.rank_fix_attempts
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id) OR is_parent_of(student_id)));

drop policy if exists "read own rank_gate_passes" on public.rank_gate_passes;
create policy "read own rank_gate_passes" on public.rank_gate_passes
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id) OR is_parent_of(student_id)));

drop policy if exists "read own rank_rp_awards" on public.rank_rp_awards;
create policy "read own rank_rp_awards" on public.rank_rp_awards
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id) OR is_parent_of(student_id)));

drop policy if exists "read own rank_rp_ledger" on public.rank_rp_ledger;
create policy "read own rank_rp_ledger" on public.rank_rp_ledger
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id) OR is_parent_of(student_id)));

drop policy if exists "read own rank_season_results" on public.rank_season_results;
create policy "read own rank_season_results" on public.rank_season_results
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id) OR is_parent_of(student_id)));

drop policy if exists "read own rank_student_seasons" on public.rank_student_seasons;
create policy "read own rank_student_seasons" on public.rank_student_seasons
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id) OR is_parent_of(student_id)));

drop policy if exists "read own rank_title_awards" on public.rank_title_awards;
create policy "read own rank_title_awards" on public.rank_title_awards
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id) OR is_parent_of(student_id)));

drop policy if exists "students manage own self rubric attempt" on public.rubric_exam_attempts;
create policy "students manage own self rubric attempt" on public.rubric_exam_attempts
  as permissive
  for insert
  to authenticated
  with check (((student_id = auth.uid()) AND (role = 'self'::text) AND (grader_id IS NULL)));

drop policy if exists "students read own rubric exam attempts" on public.rubric_exam_attempts;
create policy "students read own rubric exam attempts" on public.rubric_exam_attempts
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_admin()));

drop policy if exists "students update own self rubric attempt" on public.rubric_exam_attempts;
create policy "students update own self rubric attempt" on public.rubric_exam_attempts
  as permissive
  for update
  to authenticated
  using (((student_id = auth.uid()) AND (role = 'self'::text)))
  with check (((student_id = auth.uid()) AND (role = 'self'::text) AND (grader_id IS NULL)));

drop policy if exists "student reads own visible alerts" on public.student_alerts;
create policy "student reads own visible alerts" on public.student_alerts
  as permissive
  for select
  to authenticated
  using ((((student_id = auth.uid()) AND (status <> 'open'::text)) OR teaches_student(student_id)));

drop policy if exists "assigned instructors read class learning presence" on public.student_learning_presence;
create policy "assigned instructors read class learning presence" on public.student_learning_presence
  as permissive
  for select
  to authenticated
  using ((EXISTS ( SELECT 1
   FROM (user_classes uc
     JOIN class_instructors ci ON ((ci.class_id = uc.class_id)))
  WHERE ((uc.user_id = student_learning_presence.student_id) AND (ci.instructor_id = auth.uid())))));

drop policy if exists "students manage own learning presence" on public.student_learning_presence;
create policy "students manage own learning presence" on public.student_learning_presence
  as permissive
  for all
  to authenticated
  using ((student_id = auth.uid()))
  with check ((student_id = auth.uid()));

drop policy if exists "ta xem chinh minh" on public.ta_assistants;
create policy "ta xem chinh minh" on public.ta_assistants
  as permissive
  for select
  to authenticated
  using (((user_id = auth.uid()) OR is_admin()));

drop policy if exists "assigned instructors manage thpt attendance records" on public.thpt_attendance_records;
create policy "assigned instructors manage thpt attendance records" on public.thpt_attendance_records
  as permissive
  for all
  to authenticated
  using ((EXISTS ( SELECT 1
   FROM (thpt_attendance_sessions s
     JOIN class_instructors ci ON ((ci.class_id = s.class_id)))
  WHERE ((s.id = thpt_attendance_records.session_id) AND (ci.instructor_id = auth.uid())))))
  with check ((EXISTS ( SELECT 1
   FROM (thpt_attendance_sessions s
     JOIN class_instructors ci ON ((ci.class_id = s.class_id)))
  WHERE ((s.id = thpt_attendance_records.session_id) AND (ci.instructor_id = auth.uid())))));

drop policy if exists "students read own thpt attendance" on public.thpt_attendance_records;
create policy "students read own thpt attendance" on public.thpt_attendance_records
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR is_admin()));

drop policy if exists "assigned instructors manage thpt attendance sessions" on public.thpt_attendance_sessions;
create policy "assigned instructors manage thpt attendance sessions" on public.thpt_attendance_sessions
  as permissive
  for all
  to authenticated
  using ((EXISTS ( SELECT 1
   FROM class_instructors ci
  WHERE ((ci.class_id = thpt_attendance_sessions.class_id) AND (ci.instructor_id = auth.uid())))))
  with check ((EXISTS ( SELECT 1
   FROM class_instructors ci
  WHERE ((ci.class_id = thpt_attendance_sessions.class_id) AND (ci.instructor_id = auth.uid())))));

drop policy if exists "students read own class thpt attendance sessions" on public.thpt_attendance_sessions;
create policy "students read own class thpt attendance sessions" on public.thpt_attendance_sessions
  as permissive
  for select
  to authenticated
  using ((EXISTS ( SELECT 1
   FROM user_classes uc
  WHERE ((uc.class_id = thpt_attendance_sessions.class_id) AND (uc.user_id = auth.uid())))));

drop policy if exists "anyone reads public courses" on public.thpt_courses;
create policy "anyone reads public courses" on public.thpt_courses
  as permissive
  for select
  to public
  using (((is_public AND (status = 'active'::text)) OR ((auth.uid() IS NOT NULL) AND manages_class(class_id)) OR thpt_has_registration(id)));

drop policy if exists "staff read assigned thpt registrations" on public.thpt_registration_requests;
create policy "staff read assigned thpt registrations" on public.thpt_registration_requests
  as permissive
  for select
  to authenticated
  using ((is_admin() OR (EXISTS ( SELECT 1
   FROM class_instructors ci
  WHERE ((ci.class_id = thpt_registration_requests.requested_class_id) AND (ci.instructor_id = auth.uid()))))));

drop policy if exists "students read own thpt registration" on public.thpt_registration_requests;
create policy "students read own thpt registration" on public.thpt_registration_requests
  as permissive
  for select
  to authenticated
  using ((user_id = auth.uid()));

drop policy if exists "own registrations" on public.thpt_registrations;
create policy "own registrations" on public.thpt_registrations
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR (registered_by = auth.uid()) OR ((student_id IS NOT NULL) AND is_parent_of(student_id))));

drop policy if exists "read own exit attempts" on public.tutoring_exit_attempts;
create policy "read own exit attempts" on public.tutoring_exit_attempts
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id)));

drop policy if exists "student logs own exit attempt" on public.tutoring_exit_attempts;
create policy "student logs own exit attempt" on public.tutoring_exit_attempts
  as permissive
  for insert
  to authenticated
  with check ((student_id = auth.uid()));

drop policy if exists "student reads own needs" on public.tutoring_needs;
create policy "student reads own needs" on public.tutoring_needs
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id)));

drop policy if exists "student cancels self" on public.tutoring_registrations;
create policy "student cancels self" on public.tutoring_registrations
  as permissive
  for delete
  to authenticated
  using ((student_id = auth.uid()));

drop policy if exists "student reads own registration" on public.tutoring_registrations;
create policy "student reads own registration" on public.tutoring_registrations
  as permissive
  for select
  to authenticated
  using ((student_id = auth.uid()));

drop policy if exists "student registers self" on public.tutoring_registrations;
create policy "student registers self" on public.tutoring_registrations
  as permissive
  for insert
  to authenticated
  with check (((student_id = auth.uid()) AND (EXISTS ( SELECT 1
   FROM (tutoring_slots s
     JOIN user_classes uc ON (((uc.class_id = s.class_id) AND (uc.user_id = auth.uid()) AND (uc.status = 'active'::text))))
  WHERE (s.id = tutoring_registrations.slot_id)))));

drop policy if exists "assistant writes own coverage" on public.tutoring_session_topics;
create policy "assistant writes own coverage" on public.tutoring_session_topics
  as permissive
  for all
  to authenticated
  using (((EXISTS ( SELECT 1
   FROM (ta_sessions s
     JOIN ta_assistants a ON ((a.id = s.assistant_id)))
  WHERE ((s.id = tutoring_session_topics.session_id) AND (a.user_id = auth.uid())))) OR is_admin()))
  with check (((EXISTS ( SELECT 1
   FROM (ta_sessions s
     JOIN ta_assistants a ON ((a.id = s.assistant_id)))
  WHERE ((s.id = tutoring_session_topics.session_id) AND (a.user_id = auth.uid())))) OR is_admin()));

drop policy if exists "read tutoring coverage" on public.tutoring_session_topics;
create policy "read tutoring coverage" on public.tutoring_session_topics
  as permissive
  for select
  to authenticated
  using (((student_id = auth.uid()) OR teaches_student(student_id)));

drop policy if exists "assistant manages own slots" on public.tutoring_slots;
create policy "assistant manages own slots" on public.tutoring_slots
  as permissive
  for all
  to authenticated
  using (((EXISTS ( SELECT 1
   FROM ta_assistants a
  WHERE ((a.id = tutoring_slots.assistant_id) AND (a.user_id = auth.uid())))) OR is_admin()))
  with check (((EXISTS ( SELECT 1
   FROM ta_assistants a
  WHERE ((a.id = tutoring_slots.assistant_id) AND (a.user_id = auth.uid())))) OR is_admin()));

drop policy if exists "class reads own slots" on public.tutoring_slots;
create policy "class reads own slots" on public.tutoring_slots
  as permissive
  for select
  to authenticated
  using (((EXISTS ( SELECT 1
   FROM user_classes uc
  WHERE ((uc.user_id = auth.uid()) AND (uc.class_id = tutoring_slots.class_id) AND (uc.status = 'active'::text)))) OR manages_class(class_id) OR assists_class(class_id) OR is_admin()));

drop policy if exists "read own user classes" on public.user_classes;
create policy "read own user classes" on public.user_classes
  as permissive
  for select
  to authenticated
  using (((user_id = auth.uid()) OR is_admin()));

drop policy if exists "students request own class" on public.user_classes;
create policy "students request own class" on public.user_classes
  as permissive
  for insert
  to authenticated
  with check (((user_id = auth.uid()) AND (status = 'pending'::text)));

drop policy if exists "students resubmit rejected class request" on public.user_classes;
create policy "students resubmit rejected class request" on public.user_classes
  as permissive
  for update
  to authenticated
  using (((user_id = auth.uid()) AND (status = 'rejected'::text)))
  with check (((user_id = auth.uid()) AND (status = 'pending'::text)));

commit;
