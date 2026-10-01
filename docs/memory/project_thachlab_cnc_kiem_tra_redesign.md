---
name: project-thachlab-cnc-kiem-tra-redesign
description: Redesign khu quản trị CNC (bài học/video/đề) — bài học CNC chuyển từ hardcode sang database
metadata: 
  node_type: memory
  type: project
  originSessionId: b69bd0e7-2cb2-4f39-88f4-215061090b51
  modified: 2026-09-22T01:52:19.670Z
---

Thầy yêu cầu (2026-09-21): thiết kế lại phần "kiểm tra" trong môn CNC giống lớp Vật lý, tinh gọn menu quản trị CNC, chỉ giữ 5 việc: đăng bài học (giống THPT), đăng video bài giảng, đăng bài kiểm tra, giữ nguyên checklist, giữ nguyên điều kiện ràng buộc mở bài tự động.

**Phát hiện gốc rễ:** bài học CNC trước đó viết cứng trong `CNC_COURSE_ITEMS` (services/cnc-lms.ts, ~790 dòng) — không phải bảng DB — nên không "đăng" được qua web. Trang admin cũ (`components/admin/CncLmsAdmin.tsx`, đã xoá) chỉnh nội dung/checklist/rule-khoá chỉ là state cục bộ, bấm "Lưu thay đổi" **không ghi gì vào DB**. Đề kiểm tra CNC đã lưu thật vào `exams.cnc_key` nhưng qua trình soạn JSON thô, khác luồng dán-Azota của Vật lý.

## Đã làm (commit `f75023fe`, 2026-09-22)

- Bảng mới `cnc_lessons` — migration docs/supabase-migration-cnc-lessons.sql (đã chạy 2026-09-22, xác nhận qua REST query). **Giữ nguyên id dạng slug cũ** (`lesson-1`…`lesson-6`, `lesson-4-turn`, `lesson-4-mill`, `intro`) — vì checklist, `CNC_ASSESSMENT_PLAN` (services/cnc-progress.ts) và logic khoá/mở bài hardcode trong `components/lessons/CncCourseWorkspace.tsx` đều tham chiếu theo đúng các id này. Nhờ vậy không phải đụng tới checklist/competency/unlock logic.
- Service mới services/cnc-lessons.ts — **cố ý dùng field camelCase** (`shortTitle`, `duration`, `bodyHtml`, `emphasis`, `resources`, `sortOrder`) thay vì snake_case như service khác trong repo, để khớp đúng tên field mà `CncCourseWorkspace.tsx` (1400+ dòng) đã dùng sẵn khắp nơi — tránh phải rename hàng loạt trong file đó.
- 3 trang admin CNC tách riêng (đổi tên 1 lần vì `bai-hoc-cnc`/`video-cnc`/`dang-de-cnc` bị `areaOfPath()` trong components/admin/nav.ts nhận nhầm khu vực THPT do match theo prefix — giờ tất cả route CNC mới đều bắt đầu bằng `cnc-` để tránh trùng prefix với route THPT):
  - `/quan-tri/cnc-bai-hoc` — components/admin/CncLessonsAdmin.tsx: soạn bài qua `LaTexEditor` (component dùng chung với THPT), thêm bài mới tự do, có panel "Điều kiện mở bài (xem trước)" + checklist — **vẫn chỉ là công cụ xem trước cục bộ, không lưu DB**, giữ nguyên hành vi cũ theo đúng ý "giữ checklist" của thầy.
  - `/quan-tri/cnc-video` — components/admin/CncVideoAdmin.tsx: chọn bài rồi đăng nhiều video YouTube (bảng `cnc_lesson_videos` có sẵn từ trước, không đổi).
  - `/quan-tri/cnc-dang-de` — components/admin/CncExamComposer.tsx: dùng lại `ExamSection` (khối dán-Azota dùng chung với `/quan-tri/dang-de` của Vật lý), chọn ngân hàng từ `CNC_QUIZ_BANKS` (services/cnc-exam-bank.ts, giữ nguyên danh sách key/label), Đăng → upsert `exams` theo `cnc_key`.
  - components/admin/CncMediaPanels.tsx: tách `CncFilesAdmin`/`CncVideosAdmin` từ file admin cũ để 2 trang trên dùng chung.
- Xoá: `components/admin/CncLmsAdmin.tsx`, `CncLmsLessonIndex.tsx`, route `/quan-tri/lms-cnc/**`, route `/lop-hoc/cnc/[lessonId]` (route tĩnh `generateStaticParams` — không hợp với bài học thêm sau khi build vì site `output:"export"`; thay bằng pattern `/lop-hoc/cnc/?bai=<id>` **đã có sẵn từ trước**, dùng chung với StudentCompetencyCard/StudentLearningDashboard).
- `components/lessons/CncCourseWorkspace.tsx`: đổi sang fetch `cnc_lessons` qua `fetchCncLessons()` (trước là `const lessons = CNC_COURSE_ITEMS...` cấp module); nội dung lý thuyết render qua `ContentHtml` (component KaTeX+dangerouslySetInnerHTML dùng chung với bài Vật lý) thay cho các field `topics`/`lessonContent`/`coreKnowledge`/`teachingGuidance`/`assessment`/`activities`/`flipped`/`assignment` cũ — **đã audit xác nhận các field này không hiển thị ở đâu trong UI học sinh** (trừ `topics`+`lessonContent` gộp vào `body_html`) nên bỏ hẳn, không cố giữ cấu trúc phức tạp.
- **Phát hiện phụ:** cột `exams.cnc_key` (migration cũ `docs/supabase-migration-cnc-exam-bank.sql`, có sẵn trong repo từ trước) **chưa từng chạy trên Supabase thật** — nghĩa là tính năng ngân hàng đề CNC (cả bản cũ lẫn mới) đều không hoạt động cho tới khi chạy migration này. Thầy đã chạy cùng lúc với migration `cnc_lessons` ngày 2026-09-22, xác nhận qua REST query trực tiếp.

## Đã test

Bật dev server, xác nhận: danh sách 8 bài load đúng ở `/quan-tri/cnc-bai-hoc`; mở Bài 1 nội dung soạn sẵn hiển thị đúng; trang học sinh `/lop-hoc/cnc/?bai=lesson-1` render `body_html` đúng style (giống bài Vật lý); `/quan-tri/cnc-dang-de` đọc được ngân hàng đề thật, hết lỗi 400 (thiếu cột `cnc_key`) sau khi chạy migration. Không còn lỗi console.

## Deploy — xong 2026-09-22

Đã push commit `f073d13` lên nhánh `deploy` (`https://github.com/itachi2601/thachlab.git`) lúc 2026-09-22 — hosting cron kéo về trong ~10 phút. Build từ worktree `/Users/MAC/Projects/thachlab/.claude/worktrees/deploy-build` — có thể xoá: `git worktree remove /Users/MAC/Projects/thachlab/.claude/worktrees/deploy-build --force` (từ repo chính).
