---
name: project_thachlab_lesson_description
description: Mô tả chương trình lớp + yêu cầu cần đạt từng bài trên trang /lop-hoc
metadata: 
  node_type: memory
  type: project
  originSessionId: 52e5f974-3d3d-4c19-9df0-ba39c3a7acdf
  modified: 2026-09-22T01:52:51.493Z
---

Trang /lop-hoc/[lớp] (THPT/THCS, không phải CTTC) giờ hiện hai loại mô tả ngắn:
- Dưới tiêu đề "Vật lý N" lớn: tái dùng `GRADE_DESCRIPTIONS` có sẵn trong [app/lop-hoc/page.tsx](../../../../Projects/thachlab/app/lop-hoc/page.tsx) — không cần schema mới, không cần migration.
- Dưới mỗi bài học: cột mới `lessons.description` ("yêu cầu cần đạt"), migration [docs/supabase-migration-lessons-description.sql](../../../../Projects/thachlab/docs/supabase-migration-lessons-description.sql) — **đã chạy trên Supabase, đã test end-to-end (nhập/lưu/tải lại) 22/9/2026**. Code: fetch + hiển thị + ô nhập trong [components/admin/LessonsAdmin.tsx](../../../../Projects/thachlab/components/admin/LessonsAdmin.tsx).

**Why:** thầy yêu cầu thêm mô tả chương trình lớp + yêu cầu cần đạt bài để học sinh biết trước nội dung/mục tiêu.
**How to apply:** admin có thể vào trang quản trị Bài học, gõ tay "yêu cầu cần đạt" cho từng bài (ô dưới mỗi dòng bài học), bấm Lưu — hiện ngay dưới tên bài trên trang /lop-hoc/[lớp].

**Backfill tự động 22/9/2026 (đợt 1):** đã điền sẵn 70/118 bài — những bài đã có `question_topics` gắn `lesson_id` (qua cột nhãn Chủ đề:/Dạng: khi đăng đề, xem [[project_thachlab_dang_de_tags]]) thì lấy các dòng YCCĐ con (`parent_id` khác null, cùng lesson_id) nối bằng "; " thành 1 dòng ngắn gọn. Làm qua REST trực tiếp bằng session admin đã đăng nhập trong trình duyệt (không cần service role key). 48 bài còn lại chưa có nhãn Chủ đề/YCCĐ trong ngân hàng câu hỏi nên chưa tự điền được.

**Backfill đợt 2 — 2026-09-22 (từ văn bản gốc Bộ GD, không qua ngân hàng câu hỏi):** thầy gửi 2 file PDF chính thức —
- `~/Documents/THPT/Tài liệu thô/yeu-cau-can-dat-chuong-trinh-gdpt-2018-bo-mon-vat-li_238202415.pdf` (Vật lí THPT, lớp 10/11/12 + chuyên đề)
- `~/Downloads/YEU_CAU_CAN_DAT_MON_KHTN_42a89.pdf` (KHTN THCS, chỉ dùng phần Lớp 9 – Ánh sáng, tr.60-61, cho 2 bài KHTN 9 còn thiếu)

Đọc toàn bộ, đối chiếu với 37 bài `description` rỗng trong DB (`lessons` id qua REST anon key), viết nội dung theo đúng văn phong ngắn gọn/cụm danh từ đã có, bỏ qua 12 mục "Kiểm tra chương"/"Kiểm tra giữa học kì" (không có YCCĐ riêng) và 2 bài KHTN9 lúc đó chưa đọc tới. Script: [scripts/backfill-lessons-description-thpt.mjs](../../../../Projects/thachlab/scripts/backfill-lessons-description-thpt.mjs) (điền đúng 20 id: 18 THPT + 2 KHTN9 lớp 9 Bài 9/10 chương Ánh sáng) — thầy tự chạy với `SUPABASE_SERVICE_ROLE_KEY` (script không có sẵn key, không tự chạy được). Đã xác nhận cả 20 dòng ghi đúng qua REST anon key sau khi thầy chạy xong. **File script này vẫn đang nằm untracked trong working tree, chưa commit** (theo yêu cầu không tự commit) — an toàn để chạy lại (chỉ ghi đè đúng 20 id đó) hoặc commit sau.

Sau đợt 2 này: **118/118 bài THPT** có description; KHTN9 chỉ còn 2 bài Ánh sáng vừa điền, các bài KHTN9 khác (Điện, Điện từ, Năng lượng) đã có sẵn description từ trước (không rõ nguồn — có thể do thầy tự gõ tay).

**⚠ Phát hiện quan trọng — site export tĩnh, ghi Supabase KHÔNG tự lên web:** `next.config.ts` có `output: "export"` — mọi trang build tĩnh 1 lần lúc `npm run build`, sau đó **client fetch Supabase lúc runtime trong trình duyệt** (không phải server, không phải build-time bake — đã xác minh bằng cách gọi thẳng `fetch()` trong console trang đang mở, ra đúng dữ liệu mới, nhưng DOM thực tế không hiện `<small>{lesson.description}</small>` — tức bundle JS đang deploy trên production là bản build **cũ hơn** commit `39e27e31` "feat(lop-hoc): mô tả chương trình lớp..." đã thêm dòng JSX đó). Nói cách khác: sửa Supabase xong KHÔNG đủ — phải `npm run build` + `scripts/deploy.sh` lại thì web mới hiện.

**Đã rebuild + deploy lại 2026-09-22** để đẩy tính năng hiển thị mô tả lên production: vì working tree lúc đó có nhiều WIP dở dang (CNC redesign) không liên quan, đã `git stash push -u` để build từ đúng HEAD sạch (`39e27e31`), `bash scripts/deploy.sh` (push nhánh `deploy`), rồi `git stash pop` khôi phục lại WIP. **Lưu ý: lẽ ra phải dùng cách `git worktree add` an toàn hơn theo [[project_thachlab_concurrent_sessions]] thay vì `git stash` thẳng trên working tree dùng chung — lần này may mắn không mất gì (một phiên khác đã commit xong phần WIP CNC thành `f75023fe` trước khi mình pop lại), nhưng đây là may, không phải quy trình đúng.** Còn chờ: thầy mở lại `/lop-hoc/lop-10`, `/lop-11`, `/lop-12`, `/khtn-9` sau ~10 phút (cron hosting) để xác nhận bằng mắt là dòng mô tả đã hiện dưới tên bài.
