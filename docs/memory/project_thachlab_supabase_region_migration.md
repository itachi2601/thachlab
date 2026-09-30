---
name: project-thachlab-supabase-region-migration
description: "Migrate Supabase Sydney→Singapore để giảm độ trễ — HOÀN TẤT và đã cutover production 2026-09-28; còn treo duy nhất: quyết định Pause/Delete project Sydney cũ"
metadata:
  node_type: memory
  type: project
  originSessionId: 335a09e2-f05a-478a-a367-9d5f83bc8d24
  modified: 2026-09-28T03:06:24.947Z
---

## Mục tiêu
Chuyển toàn bộ backend ThachLab từ Supabase project Sydney (`fxnqgmfqdbvnjawgnsfi`, ap-southeast-2)
sang Singapore (`jgvbdbpvjdntdgzthumv`, ap-southeast-1) để giảm ~3-4x độ trễ cho user Việt Nam.

**Vì sao làm trên máy thầy, không phải cloud sandbox:** proxy cloud chặn `*.supabase.co` (403
CONNECT), không có `SUPABASE_SERVICE_ROLE_KEY`/mật khẩu DB trong sandbox. Chỉ Claude Code chạy trên
macOS của thầy (đã `.env.local` + CLI `link`) mới làm được — quy tắc này ghi trong AGENTS.md gốc
của dự án.

## Đã xong (2026-09-28) — production ĐANG CHẠY trên Singapore

1. **Schema `public`** (99 bảng, 212 hàm, 47 trigger, 270 RLS policy) — khớp 100% cả 2 project,
   đã đối chiếu trực tiếp bằng SQL COUNT, không chỉ tin log script.
2. **Storage** — cả 7 bucket (avatars, bug-report-screenshots, lesson-media 3124 file, cnc-drawings,
   equipment-breakdown-photos, attendance-machine-photos, cnc-lessons) + bucket `exam-images` (80
   file, **bị bỏ sót hoàn toàn** khỏi danh sách BUCKETS gốc trong script — đã bổ sung) khớp 100%.
   Script gốc `migrate-storage.mjs` có bug `.list(prefix,{limit:1000})` không phân trang — bỏ sót
   file khi 1 folder có >1000 file (`lesson-media` có 1 folder 1208 file) — đã vá pagination.
3. **Auth** — 381/381 user, **mật khẩu thật giữ nguyên** (bảng `auth.users` được copy ở mức DB, không
   qua Admin API như script `migrate-auth.mjs` định làm — hash mật khẩu giống hệt byte-for-byte,
   `created_at` khớp chính xác). Không cần bắt ai đổi mật khẩu. `auth.identities`/`sessions`/
   `refresh_tokens` = 0 trên Singapore (không được copy) nhưng **đã test thật**: login bằng
   password-grant vẫn thành công với user không có `identities` — GoTrue không cần bảng này để
   xác thực password. Không cần backfill.
4. **Edge Functions** — cả 4 hàm (`classify-questions`, `draw-figure`, `import-roster`,
   `reset-password`) đã deploy sang Singapore + set lại secret `ANTHROPIC_API_KEY` (secret
   `SUPABASE_*` tự động theo project, không cần copy tay).
5. **Cutover** — `.env.local` + CLI link đã trỏ Singapore, build + deploy production, xác nhận
   trực tiếp bundle JS live chỉ còn ref Singapore.
6. **Sự cố phát hiện giữa chừng + đã vá:**
   - Lần đồng bộ cuối trước cutover phát hiện **data drift thật**: production vẫn chạy trên Sydney
     suốt quá trình migrate nên `exams`/`exam_question_results` lệch (200 vs 197, 11578 vs 11532).
     Chạy lại `pg_dump --schema=public | pg_restore --clean --if-exists` để đồng bộ — nhưng script
     `migrate.sh` gốc viết cho **project đích trống**, chạy lại trên project đã có data thì
     `--clean` bị RLS policy trên `storage.objects` + trigger trên `auth.users` (tham chiếu bảng/hàm
     `public`) chặn DROP → 3 bảng (`attendance_sessions`, `cnc_drawing_submissions`,
     `course_enrollments`) bị NHÂN ĐÔI dữ liệu + mất khoá chính. Phát hiện bằng cách tự đối chiếu
     COUNT tất cả 99 bảng sau restore (không tin log "xong"), rồi vá thủ công: xoá sạch 3 bảng,
     chép lại đúng dữ liệu Sydney, khôi phục PK + 5 FK liên quan, cập nhật lại 5 hàm DB
     (`is_admin`, `handle_new_user`, `can_manage_course`, `trg_claim_staff_invite`,
     `trg_claim_parent_link` — dùng `CREATE OR REPLACE` để né vấn đề dependency). Rà lại cả 99
     bảng lần 2 xác nhận 0 lệch.
   - **Ảnh mất sạch sau cutover** — nội dung lưu trong DB (không phải file storage) chứa link ảnh
     TUYỆT ĐỐI trỏ thẳng Sydney (`https://fxnqgmfqdbvnjawgnsfi.supabase.co/storage/...`), khi Sydney
     bị pause thì ảnh 404 hết dù file đã có y hệt bên Singapore. Quét toàn bộ 310 cột text/jsonb
     trong `public`, sửa domain ở 6 bảng: `lesson_items.body_html` (47 dòng), `.questions` (30),
     `exams.questions` (136), `question_bank.question` (1938 — 2062 câu match ban đầu nhưng patch
     chỉ chạm 1938, chưa rõ vì sao lệch, verify lại sau patch = 0 dòng sót nên không truy tiếp),
     `cnc_lesson_files.file_url` (5), `profiles.avatar_url` (9). Bảng backup
     `question_bank_backup_20260925` cũng dính lỗi này nhưng KHÔNG sửa (đang chờ xoá, không hiển
     thị cho HS).
   - **Trang bài học là SSG** (`generateStaticParams`, build-time qua `scripts/build-content.mjs`
     chạy tự động ở `npm run prebuild`) — sửa data ở DB KHÔNG tự lên web, phải `npm run build` +
     `scripts/deploy.sh` lại thì mới thấy. Đã rebuild+deploy 2 lần trong đợt này vì quên điều này
     ở lần đầu.

## Còn treo — CHỈ 1 việc, KHÔNG tự làm
**Pause hoặc Delete project Sydney** (`fxnqgmfqdbvnjawgnsfi`) trên Supabase Dashboard → Settings →
General. Đây là xoá dữ liệu vĩnh viễn (Delete) — nằm trong nhóm hành động agent luôn từ chối tự làm
dù được yêu cầu trực tiếp, đã báo thầy dùng Dashboard tự bấm. Khuyến nghị: bấm **Pause** trước (dừng
gần hết phí, vẫn giữ dữ liệu để rollback vài ngày đầu), Delete hẳn sau khi ổn định.

## Dọn dẹp đã làm
Đã xoá `migrate-auth.mjs`/`migrate-storage.mjs` khỏi `~/Projects/thachlab` (chứa service role key
hardcode, migration đã xong, không cần giữ trong repo).

## Vị trí các file còn lại (KHÔNG trong repo git, chứa secret)
`~/Documents/migration/` — `HANDOFF.md` (bàn giao gốc, chứa cả 2 service role key + DB password
plaintext), `backup.dump`, `migrate.sh` (script pg_dump/restore, viết cho project đích TRỐNG —
không an toàn để chạy lại nguyên trạng khi cả 2 project đã có data, xem "Sự cố" ở trên). Giữ lại vài
ngày phòng cần đối chiếu, sau đó nên xoá cùng lúc quyết định Sydney.

## Công cụ dùng cho migration (không phải quy trình `supabase/migrations/` thường ngày)
`pg_dump`/`pg_restore` không có sẵn trong PATH — nằm ở `/opt/homebrew/opt/libpq/bin/` (Homebrew
libpq keg-only). Dùng Node `pg` client (cài tạm bằng `npm install pg --no-save` trong thư mục
scratchpad, không phải trong repo) để chạy SQL trực tiếp lúc cần đối chiếu/vá dữ liệu — nhanh hơn
CLI `supabase db query --linked` khi cần nhiều câu lệnh liền nhau. Việc dùng service-role key/DB
password trực tiếp qua Bash của agent trong đợt này là NGOẠI LỆ có chủ đích cho đúng tác vụ hạ tầng
một-lần này (AGENTS.md gốc cho phép), KHÔNG áp dụng cho việc sửa nội dung/data thường ngày — xem
[[feedback_lesson_item_edit_via_rest]] cho quy trình đúng khi chỉ sửa 1 bản ghi.

Liên quan: [[project_supabase_configured]], [[feedback_lesson_item_edit_via_rest]]
