# Cho phiên Claude Code cloud đăng/sửa bài lên thachlab

Script đăng/sửa (`scripts/upload-lesson.mts`, `update-*.mts`, `publish-theory-quiz.mts`, `apply-theory-content.mjs`)
đọc `NEXT_PUBLIC_SUPABASE_URL` và `SUPABASE_SERVICE_ROLE_KEY` từ biến môi trường. Cloud chỉ thiếu 2 thứ,
cả hai cấu hình ở **môi trường cloud** (claude.ai/code → chọn môi trường → Edit), không nằm trong repo:

1. **Network access**: chọn *Custom*, thêm `jgvbdbpvjdntdgzthumv.supabase.co` (và `*.supabase.co` nếu cần Storage).
   Hiện bị proxy trả 403 CONNECT.
2. **Environment variables**: thêm `NEXT_PUBLIC_SUPABASE_URL=https://jgvbdbpvjdntdgzthumv.supabase.co`
   và `SUPABASE_SERVICE_ROLE_KEY=<khoá service_role>`.

Đổi xong, mở phiên cloud mới: hook `SessionStart` in dòng `Supabase: ...` cho biết đã đăng được chưa.

## Lưu ý an toàn
- Khoá service_role bỏ qua RLS = toàn quyền DB. Biến môi trường cloud ai có quyền sửa môi trường đều đọc được;
  chỉ bật nếu môi trường đó là riêng của thầy. Khi lộ: Supabase → Settings → API → đổi khoá.
- Vẫn **không** chạy migration/DDL từ cloud (quy tắc trong AGENTS.md) — chỉ ghi nội dung (lessons, exams, câu hỏi).
- Ghi thật, không dry-run: sửa bài đã đăng thì đọc bản hiện tại trước, PATCH đúng mục cần đổi.
