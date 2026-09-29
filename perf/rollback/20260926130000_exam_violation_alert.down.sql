-- Rollback cho supabase/migrations/20260926130000_exam_violation_alert.sql
--
-- Xoá cảnh báo exam_violation đã tạo, khôi phục trigger nộp bài về bản chỉ
-- gọi evaluate_student_alerts, xoá hàm evaluate_exam_violation_alert, và bỏ
-- 'exam_violation' khỏi ràng buộc kind.
--
-- Chạy: supabase db query --linked -f perf/rollback/20260926130000_exam_violation_alert.down.sql

delete from public.student_alerts where kind = 'exam_violation';

create or replace function public.trg_exam_result_alert()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  perform public.evaluate_student_alerts(new.student_id);
  return new;
end;
$$;

drop function if exists public.evaluate_exam_violation_alert(bigint);

alter table public.student_alerts drop constraint if exists student_alerts_kind_check;
alter table public.student_alerts add constraint student_alerts_kind_check
  check (kind in ('low_score_streak', 'missed_assessment'));
