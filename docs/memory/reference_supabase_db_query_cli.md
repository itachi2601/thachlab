---
name: supabase-db-query-cli
description: "Chạy SQL lên Supabase prod ngay từ terminal: `supabase db query --linked -f file.sql` (CLI đã login + link), không cần psql/mật khẩu DB"
metadata:
  type: reference
---

`supabase db query --linked -f docs/<migration>.sql` (hoặc chuỗi SQL trực tiếp) chạy SQL qua Management API
lên project fxnqgmfqdbvnjawgnsfi. CLI v2.117 đã login (token trong Keychain) và đã link — xác nhận hoạt động 25/9/2026.
Trả JSON rows; lỗi SQL trả `LegacyDbQueryUnexpectedStatusError` kèm message Postgres. `begin; ... rollback;` trong
một file chạy được → dùng để test rollback như `docs/supabase-test-rank-system.sql`. NOTICE không hiện ra,
muốn xem giá trị thì `raise exception` kèm dữ liệu. auth.uid() null → giả lập bằng
`set_config('request.jwt.claims', json_build_object('sub', <uuid>, 'role','authenticated')::text, true)`.
Thay cho cách cũ (psql qua pooler + hỏi mật khẩu, hoặc SQL Editor trong trình duyệt) — xem [[project-supabase-configured]].
