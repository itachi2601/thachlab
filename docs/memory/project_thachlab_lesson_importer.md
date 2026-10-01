---
name: project-thachlab-lesson-importer
description: "Upload bài bằng LaTeX" pipeline — plan approved 2026-09-04, being built
metadata:
  type: project
---

Feature: một request "upload bài vào Lớp X / Chương Y / Bài Z" (kèm file .tex + zip ảnh) tự động điền lý thuyết + các dạng bài tập + một đề trắc nghiệm/đúng-sai/trả lời ngắn có chấm điểm vào đúng bài học trên LMS.

TRẠNG THÁI (2026-09-04): code đã viết xong, tsc + lint + build pass, parser đã test bằng Node. CHƯA làm: (1) chạy `docs/supabase-migration-lesson-media.sql` trong Supabase SQL Editor để tạo bucket `lesson-media`; (2) test end-to-end với admin đăng nhập; (3) commit + deploy code. Working tree còn WIP không liên quan → chưa commit.
Đã build: `app/quan-tri/(thpt)/nhap-bai/page.tsx`, `components/admin/LessonImporter.tsx`, `services/lesson-import.ts`, `services/lesson-media.ts`, rewrite `services/exam-latex-parser.ts` + `services/latex-converter.ts` (giờ xuất `$...$` trần, xử lý ngoặc lồng/figure/comment; xóa dead `MathRenderer.tsx`), `scripts/upload-lesson.mjs` (dự phòng service-role), `app/globals.css` (.exam-content figure.fig), nav sidebar.

WIP chưa commit (ghi nhận 2026-09-19, từ phiên khác — không phải phiên tách KT học kì): `components/admin/LessonImporter.tsx` sửa mặc định `examMode` từ `replace` → `keep`, **bỏ hẳn nhánh xóa đề cũ** khi thay liên kết (trước đây `replace` gọi `exams.delete`, giờ chỉ đổi liên kết, đề cũ vẫn nằm trong kho), và thêm dòng giải thích hai chế độ dưới ModePicker. Chưa test, chưa commit, chưa deploy. Untracked kèm theo: `.lesson-import.mjs`, `public/lessons/12-khai-niem-tu-truong/`, `public/lessons/12-luc-tu-cam-ung-tu/`.

Kiến trúc đã chốt (plan: `~/.claude/plans/sparkling-weaving-quokka.md`):
- Trang admin mới `/quan-tri/nhap-bai` (`components/admin/LessonImporter.tsx`) nhận một "gói bài học" JSON (`LessonBundle`, schema `thachlab.lesson-bundle/v1`) do Claude dựng sẵn trong phiên chat → preview + validate → ghi vào Supabase bằng phiên admin đang đăng nhập (không đụng service-role key).
- Thư viện thuần `services/lesson-import.ts` (`validateBundle`, `bundleToRows`, `parseLessonTex`) dùng chung cho trang + script dự phòng `scripts/upload-lesson.mjs`.
- Ảnh: **SVG-first** (vẽ vector inline trong HTML); ảnh chụp thật → bucket Storage `lesson-media` (migration `docs/supabase-migration-lesson-media.sql`, chưa chạy).
- Đề gắn vào `luyen_tap` mặc định, có nút chọn thêm `kiem_tra`; `published=true` ngay; upload lại thì hỏi Thay/Giữ/Bỏ qua đề cũ.
- Rework `services/exam-latex-parser.ts` (nhận `A.` lẫn `A)`, TF, SA numeric, khối `PHẦN I/II/III`) + fix `services/latex-converter.ts` (xuất `$...$` trần thay vì wrapper `data-latex`).
- Viết lại skill [[project-thachlab-lms]] `dang-bai-hoc-thachlab` — phần đề giờ trong phạm vi (trước là "ngoài phạm vi").

Liên quan: [[project-thachlab-cttc-roster-import]] (cùng pattern seed script service-role), [[feedback-thachlab-deploy-scope]].
