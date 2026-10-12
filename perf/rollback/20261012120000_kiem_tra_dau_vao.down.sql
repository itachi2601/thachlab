-- Hoàn tác kiểm tra đầu vào: bỏ hàm + bảng. Các mục tutoring_needs đã mở (note 'chẩn đoán đầu vào') giữ nguyên.
drop function if exists public.diagnostic_reset(uuid);
drop function if exists public.diagnostic_submit(uuid, jsonb);
drop function if exists public.diagnostic_get(uuid);
drop function if exists public.diagnostic_can_read(uuid);
drop table if exists public.entry_diagnostics;
