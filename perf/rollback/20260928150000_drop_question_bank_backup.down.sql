-- Rollback cho 20260928150000_drop_question_bank_backup.sql
-- KHÔNG khôi phục được dữ liệu cũ (bản chụp 25/9/2026 đã mất khi drop).
-- Chỉ tạo lại một bản chụp MỚI của question_bank nếu cần đối chiếu về sau:
create table if not exists public.question_bank_backup_20260925 as
  select * from public.question_bank;
