-- ============================================================
-- Học sinh quên mật khẩu
--
-- Tài khoản học sinh dùng email giả (mãsố@thachlab.local, xem import-roster) nên
-- Supabase Auth's "gửi email đặt lại mật khẩu" không dùng được — không có hộp thư thật.
-- Hai cách, cùng một bảng mã (giống mô hình lời mời ở supabase-migration-phu-huynh.sql):
--   1. "admin_direct": giáo viên gặp trực tiếp học sinh, bấm đặt thẳng mật khẩu về mã số HS
--      (đúng quy ước mật khẩu ban đầu của roster import). Không cần mã, chạy ngay trong
--      Edge Function reset-password; hàng lưu lại đây chỉ để làm lịch sử/audit.
--   2. "self_service": giáo viên tạo mã, gửi link https://thachlab.id.vn/quen-mat-khau?ma=RSxxxxxx
--      qua Zalo, học sinh tự vào đặt mật khẩu mới — không cần đăng nhập trước (đang bị khoá
--      ngoài tài khoản), nên trang /quen-mat-khau gọi thẳng Edge Function, không qua RPC/RLS.
--
-- Mã bắt đầu "RS" (Reset) — khác tiền tố "PH" (phụ huynh) và mã mời nhân sự (8 hex trần) nên
-- không lẫn giữa các trang nhận mã.
--
-- Chạy SAU: supabase-migration-tutoring-needs.sql hoặc supabase-migration-exam-analytics.sql
--           (một trong hai định nghĩa hàm teaches_student).
-- Idempotent — chạy lại được. Chạy trong Supabase → SQL Editor hoặc supabase db query --linked.
-- ============================================================

create table if not exists public.password_reset_codes (
  id uuid primary key default gen_random_uuid(),
  code text not null unique
    default 'RS' || upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 6)),
  student_id uuid not null references public.profiles (id) on delete cascade,
  method text not null default 'self_service' check (method in ('self_service', 'admin_direct')),
  created_by uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null default now() + interval '24 hours',
  used_at timestamptz
);

create index if not exists password_reset_codes_student_idx on public.password_reset_codes (student_id);

alter table public.password_reset_codes enable row level security;

-- Giáo viên được phân công lớp của em (teaches_student đã gồm admin) tạo/xem/huỷ mã. Việc
-- ĐẶT MẬT KHẨU THẬT chỉ Edge Function (service_role) làm được — RLS ở đây chỉ gác việc
-- đọc/ghi bảng mã, không tự cho phép đổi mật khẩu ai.
drop policy if exists "staff manage password reset codes" on public.password_reset_codes;
create policy "staff manage password reset codes" on public.password_reset_codes
  for all to authenticated
  using (public.teaches_student(student_id))
  with check (public.teaches_student(student_id));
