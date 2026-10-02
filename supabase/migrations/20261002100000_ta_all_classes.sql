-- Mọi trợ giảng đang hoạt động được coi như hỗ trợ TẤT CẢ khối lớp (không cần gán từng lớp
-- trong ta_assistant_classes). Chỉ đổi 2 hàm helper RLS: assists_class, teaches_student.

CREATE OR REPLACE FUNCTION public.assists_class(p_class bigint)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select exists (
    select 1 from public.ta_assistants a
    where a.user_id = (select auth.uid()) and a.active
  );
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
    where uc.user_id = p_student and ci.instructor_id = (select auth.uid())
  ) or exists (
    select 1 from public.ta_assistants a
    where a.user_id = (select auth.uid()) and a.active
  );
$function$;

-- ROLLBACK: chạy lại 2 định nghĩa cũ ở supabase/migrations/20260925140000_perf_rls.sql
-- (assists_class dòng ~33, teaches_student dòng ~246).
