-- Rà bảo mật 21/10/2026: hàm SECURITY DEFINER không kiểm quyền đang gọi được bởi anon.
-- Nhóm A: hàm nội bộ (trigger/hàm khác gọi, client không gọi) -> chỉ service_role (chủ hàm vẫn chạy được từ trigger).
-- Nhóm B: client đăng nhập có gọi -> bỏ anon, giữ authenticated. (notify_user vẫn cho HS tự gọi: việc kiểm quyền trong thân hàm làm ở đợt sau.)
do $$
declare r record;
begin
  for r in
    select p.oid::regprocedure as f, p.proname
    from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and p.prorettype <> 'trigger'::regtype
      and p.proname in (
        'rank_award','rank_grant_title','rank_on_result','rank_ensure_member','sync_exam_to_bank',
        'apply_staff_invite','apply_parent_link','evaluate_student_alerts','evaluate_exam_violation_alert',
        'refresh_tutoring_needs','rank_refresh_student','rank_seed_tiers','rank_eval_titles','rank_eval_gates',
        'rank_eval_achievements','rank_eval_weekly_goal','rank_eval_daily_streak','rank_daily_streak_len',
        'notify_class_staff','notify_student_side','rl_allow')
  loop
    execute format('revoke execute on function %s from public, anon, authenticated', r.f);
    execute format('grant execute on function %s to service_role', r.f);
  end loop;
  for r in
    select p.oid::regprocedure as f from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and p.proname in ('notify_user','ta_video_topic_suggestions')
  loop
    execute format('revoke execute on function %s from public, anon', r.f);
    execute format('grant execute on function %s to authenticated, service_role', r.f);
  end loop;
end $$;

-- Bảng live quiz CNC: bỏ quyền thừa của anon, đọc chỉ dành cho nhân sự / chính chủ.
-- LƯU Ý: upsert của học sinh chưa đăng nhập dùng ON CONFLICT nên cần thử trên máy trước khi chạy giờ học.
revoke truncate, trigger, references, delete on public.cnc_milling_quiz_attempts from anon;
drop policy if exists "classroom reads live milling attempts" on public.cnc_milling_quiz_attempts;
create policy "staff or owner reads milling attempts" on public.cnc_milling_quiz_attempts
  for select to anon, authenticated
  using (public.is_staff() or student_id = auth.uid());

-- ROLLBACK:
--   grant execute on all functions in schema public to public, anon, authenticated;  -- trở về mặc định cũ
--   drop policy "staff or owner reads milling attempts" on public.cnc_milling_quiz_attempts;
--   create policy "classroom reads live milling attempts" on public.cnc_milling_quiz_attempts for select to anon, authenticated using (true);
