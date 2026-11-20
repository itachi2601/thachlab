---
name: project-thachlab-ra-soat-website-2026-11-18
description: Rà soát toàn site 18/11/2026 — đợt 1 (giảm lượt gọi Supabase thừa) đã deploy; đợt 2 dọn tồn đọng và đợt 3 nền móng còn chờ thầy chọn
metadata:
  node_type: memory
  type: project
  originSessionId: acbf40de-2fb8-4807-9b39-bc1dfc4fe024
  modified: 2026-11-18T16:04:51.049Z
---

**Mục tiêu:** thầy yêu cầu 2026-11-18 rà soát website thachlab và đề xuất kế hoạch cải tiến. Kế hoạch 3 đợt, thầy đã chọn làm + deploy đợt 1.

**Đã xong — đợt 1 (commit `fa8a41c6f`, vào main, deploy 2026-11-18 17:03, kiểm trang thật 375px bằng tài khoản quản trị):**
- `app/lop-hoc/page.tsx`: effect gọi `get_chapter_mastery` chờ `defaultChapterApplied` (trước đó mọi chương bị coi là đang mở: 5 lượt ở trang lớp, 23 lượt ở màn chọn lớp → nay 1).
- `scripts/build-content.mjs` ghi `staticLessonIds` vào `public/data/catalog.json`; `services/static-content.ts` `loadStaticLesson` chỉ thử tải `/data/lessons/<id>.json` cho bài có trong danh sách (hết 404 mỗi lần mở bài không xem thử). Catalog cũ không có trường này thì vẫn thử tải như trước.
- `services/notifications.ts`: `fetchUnreadCount` dùng chung một lượt RPC trong 3 giây (chuông + thanh tab dưới: 2 → 1), xoá bản nhớ khi `markRead`/`markAllRead`/`deleteNotification`.
- Tiêu đề tab: `document.title` theo tên bài ở `app/lop-hoc/bai/page.tsx`; `app/lop-hoc/ket-qua/layout.tsx` (mới) đặt metadata.

**Còn chờ (thầy chưa chọn):**
- Chưa kiểm đợt 1 bằng tài khoản học sinh thật.
- Đợt 2 — dọn tồn đọng: 23 báo lỗi mới (`/xu-ly-bao-loi`; có báo đề 1354 thiếu hình và bài phản biện việc không hiện đáp án sai ở đề 1297 — khớp việc `ExamDoneLocked` chờ deploy); `npm audit` 7 lỗ hổng (`zod` sửa được bằng `npm audit fix`; `next` 16.2.10 → bản vá, rủi ro thật thấp vì site xuất tĩnh); lint phần web 19/20 cảnh báo (thêm 2 cảnh báo là CI đỏ); `docs/STATE.md` 15,7 KB và `MEMORY.md` 10,2 KB vượt hạn mức; 25 nhánh `claude/*` chưa vào main, 188 worktree.
- Đợt 3 — nền móng: trang bài học còn ~10 lượt Supabase riêng lẻ (cần RPC gộp) và `app/lop-hoc/bai/page.tsx` 2.504 dòng, JS ~1,6 MB; chưa có file test nào (chấm điểm, RP, mastery); chấm điểm CNC/`practice_sessions.score` còn ở máy; CSP đang report-only.
- Việc nhỏ chưa làm: nút nổi che chữ đầu tiêu đề "Mở bài" ở 375px (đã thấy với nút quản trị; nút báo lỗi/ghi chú bên phải cần xem bằng tài khoản HS); trang chủ quản trị gọi 5 truy vấn đếm riêng.

**Ghi chú cách đo (em tự rút ra, không phải lời thầy):**
- Chế độ "Xem như học sinh" lưu ở `sessionStorage` khoá `thachlab_preview_as_student`.
- Đo số request trên trang thật phải dùng tab đang hiện; tab bị đẩy xuống nền đứng ở khung chờ hơn 10 giây, dễ tưởng deploy hỏng.
- Sửa `build-content.mjs` thì chạy lại `node scripts/build-content.mjs` trước khi mở dev server (dev dùng `catalog.json` cũ).
- `bash scripts/deploy.sh` mất khoảng 10 phút; đừng nối `| tail` vì mất hết tiến độ.
