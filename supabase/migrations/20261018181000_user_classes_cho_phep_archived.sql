-- Cho phép user_classes.status = 'archived' (lưu trữ tài khoản HS bị bỏ: em đã có tài khoản mới).
-- Mọi truy vấn xét status = 'active' tự loại em ra; dữ liệu học giữ nguyên. Hoàn tác từng em bằng scripts/luu-tru-tai-khoan-bo.mts --undo.
alter table public.user_classes drop constraint if exists user_classes_status_check;
alter table public.user_classes add constraint user_classes_status_check
  check (status = any (array['pending'::text, 'active'::text, 'rejected'::text, 'archived'::text]));

-- ROLLBACK (chỉ khi không còn dòng 'archived'):
--   alter table public.user_classes drop constraint user_classes_status_check;
--   alter table public.user_classes add constraint user_classes_status_check check (status = any (array['pending'::text, 'active'::text, 'rejected'::text]));
