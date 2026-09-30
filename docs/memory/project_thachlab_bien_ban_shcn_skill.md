---
name: project_thachlab_bien_ban_shcn_skill
description: "Skill bien-ban-shcn — 2 bản phải sửa cả hai, 1 bản không lưu vào account; 27/9 bỏ bước tự đăng portal, thêm bước đăng nội dung tuần lên thachlab"
metadata:
  node_type: memory
  type: project
  originSessionId: 982c5db6-c992-4a02-8a78-23638ad5ef23
  modified: 2026-09-27T15:54:33.564Z
---

Skill `anthropic-skills:bien-ban-shcn` (soạn biên bản SHCN hàng tuần) có 2 bản file, giống pattern
của [[project_thachlab_azota_skill]] / [[project_thachlab_ngan_hang_cau_hoi_skill]] — sửa 1 bản
không tự động ra bản kia:

- `~/.claude/skills/synced/f7f31a21.../bien-ban-shcn/SKILL.md` — bản đơn giản, dùng cho Code tab.
  **Cảnh báo của chính tool Edit**: đây là bản cache "synced" từ account claude.ai, sửa ở đây
  KHÔNG lưu về account và có thể bị đè mất ở lần đồng bộ sau. Không có tool nào trong Code tab lưu
  ngược lên account — muốn lưu bền phải vào Settings trên claude.ai.
- `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/f7f31a21.../skills/bien-ban-shcn/SKILL.md`
  — bản nâng cao hơn nhiều (dùng khi chat trực tiếp trong Claude Desktop, không qua Code tab): có
  script `10-Công tác chủ nhiệm/mau/bbshcn.py` xuất Word từ JSON, xuất thêm bản PDF, lưu 2 thư mục
  con `bien-ban/word` + `bien-ban/pdf`, ghi nhật ký tiến độ dạy GDĐĐ&PTNN. Hai bản đã lệch nội dung
  khá nhiều trước khi sửa lần này — mỗi lần sửa skill này phải đọc cả hai, giữ phần nâng cao riêng
  của bản Library, không chỉ copy nguyên bản synced sang.

**Đổi 27/9/2026 (theo yêu cầu thầy)**: bỏ hẳn Bước 3 cũ (tự dùng trình duyệt đăng ký buổi + upload
file lên `portal.caothang.edu.vn/giang_vien/ds_bb_shcn.php`) — thầy tự đăng portal, skill không
đụng vào nữa. Thay bằng Bước 3 mới: đăng lại đúng nội dung tuần lên thachlab, dùng module SHCN đã
có sẵn trong code (xem [[project_thachlab_homeroom]] — module riêng, khác bảng
`homeroom_term_records`): dựng JSON kiểu `tuan-XX.json` từ dữ liệu đã thu thập ở Bước 0-1, chạy
`node scripts/import-shcn-tuan.mjs --lop "<lớp>" file.json` (đọc `SUPABASE_SERVICE_ROLE_KEY` từ
`.env.local`, ghi thẳng bảng `homeroom_weekly_sessions`, upsert theo course_id+week_no). Sinh viên
xem lại ở `/tai-khoan` → tab "Sinh hoạt lớp" (`ShcnWeekList.tsx`).

Module này (`docs/supabase-migration-shcn.sql`, `services/homeroom-shcn.ts`,
`components/dashboard/HomeroomWeeklyEditor.tsx`/`ShcnWeekList.tsx`, `docs/SHCN-MODULE.md`) đã được
code từ 14/9, merge lại vào main 24/9/2026 (commit 322c903d, "khôi phục module" — nhánh cũ từng bị
bỏ sót không merge). **Chưa xác nhận `docs/supabase-migration-shcn.sql` đã chạy trên production**
— không thấy nhắc trong `docs/STATE.md`. Trước khi dùng Bước 3 mới lần đầu, kiểm tra bằng cách vào
`/dashboard` → môn GDĐĐ&PTNN → lớp chủ nhiệm → tab "Sinh hoạt lớp" thử lưu 1 tuần trên web; nếu lỗi
bảng không tồn tại thì cần chạy migration đó trước (theo quy tắc ở AGENTS.md — viết file, để thầy
chạy, không tự `db push`).
