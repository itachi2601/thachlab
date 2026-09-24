# Mốc đo trước tối ưu tốc độ — ThachLab

Ngày đo: 25/09/2026 · commit gốc `95976576` (main) · Next.js 16.2.10 (Turbopack) · `output: "export"`, `trailingSlash: true`, `images.unoptimized`.

## 1. Hạ tầng

| Mục | Hiện trạng |
|---|---|
| Supabase project | `fxnqgmfqdbvnjawgnsfi` — region **ap-southeast-2 (Sydney, AWS)** (đọc từ `supabase/.temp/pooler-url`: `aws-1-ap-southeast-2.pooler.supabase.com`). Người dùng ở VN → mỗi round-trip ≈ 100–150 ms. Chuyển sang Singapore (ap-southeast-1) là việc ngoài phạm vi, chỉ ghi nhận. |
| Host phần tĩnh | Shared hosting LiteSpeed (`thachlab.id.vn`, DirectAdmin). `scripts/deploy.sh` build → force-push nhánh `deploy`; cron trên host `git reset --hard origin/deploy` mỗi 10 phút. `.htaccess` cache 1 năm cho `js/css/woff2`; **ảnh (png/jpg/webp) không có cache header**. Không CDN. |
| Thư viện công thức | **KaTeX 0.17** (`katex.renderToString` trong `components/exams/ContentHtml.tsx`, import tĩnh kèm `katex/dist/katex.min.css`). Không dùng MathJax. Fonts KaTeX (woff2) đi theo bundle CSS. |
| Font | `@import url(fonts.googleapis.com/css2?...)` ở dòng 1 `app/globals.css`: Be Vietnam Pro 400–800 (5 weight), Inter 400/500/600, JetBrains Mono 400/500, `display=swap`. Tải qua CSS import → chặn render cho tới khi CSS Google trả về (thêm 1–2 DNS/TLS handshake tới Google trước FCP). Chưa dùng `next/font`. |
| Data client | `@supabase/supabase-js` 2.x, tạo 1 client duy nhất ở `services/supabase.ts`; mọi truy vấn chạy từ trình duyệt bằng anon key + RLS. Không SWR/TanStack Query; không có `next/dynamic` hay `import()` nào ngoài `heic2any`. |
| Migration SQL | Không có `supabase/migrations/`; 99 file `docs/supabase-migration-*.sql` + `docs/supabase-schema.sql` (thầy chạy tay trên Dashboard). 267 chỗ `auth.uid()` trong policy; ~91 dòng `create index` rải rác. |

Lưu ý build: `tsconfig` include `**/*.ts` nên `next build` type-check cả `scripts/`. Trên working tree hiện tại, file WIP `scripts/_tmp_bulk_upload_de_thi_thu.mts` (chưa commit) làm `npm run build` fail; build ở worktree sạch của `main` thì qua. Mọi số liệu dưới đây đo ở worktree sạch.

## 2. Bundle JS (build sạch `main`)

- `out/` = **41 MB** (trong đó `_next/static` 11 MB, `chunks` 10 MB); 64 trang tĩnh.
- Build ~20 s (Turbopack). `@next/bundle-analyzer` đã cài (devDependency) nhưng chỉ dùng cho webpack; với Turbopack dùng `npx next experimental-analyze --output`.

### 10 chunk lớn nhất tải trực tiếp qua `<script>`

| Chunk | KB | KB gzip | Trang dùng | Trang tiêu biểu | Chứa gì |
|---|---:|---:|---:|---|---|
| 2y5gmjd2zd2ls.js | 1107 | 295 | 1/64 | /dashboard | exceljs + xlsx + marked + supabase (Teacher Studio CTTC) |
| 20r1oz9jnbft7.js | 352 | 119 | 3/64 | /dashboard-thpt, /dashboard, /quan-tri/hoc-sinh | xlsx (SheetJS) — `ClassRosterImportPanel` bị import tĩnh vào cả dashboard HS THPT |
| 3eokz_dtrsjpk.js | 290 | 80 | 20/64 | /kiem-tra/lam, /tin-tuc, /lop-hoc/cnc | KaTeX |
| 27-boq88eir0-.js | 234 | 59 | 64/64 | mọi trang | supabase-js + GoTrue + next runtime |
| 3--yt5ny8w4d1.js | 222 | 69 | 64/64 | mọi trang | react-dom + framer-motion |
| 3utnuqr-h2goc.js | 148 | 40 | 64/64 | mọi trang | (app shell: AuthProvider, Toast, BugReport…) |
| 0ef-hqu1_n0gl.js | 142 | 39 | 1/64 | /tai-khoan | marked + supabase |
| 3u9fz4l4n3m9e.js | 138 | 45 | 4/64 | /kiem-tra/lam, /, /lop-hoc/xep-hang | framer-motion (ExamRunner, Rank) |
| 0cvw2gy3z-49f.js | 138 | 45 | 7/64 | /lop-hoc/* | framer-motion (Reveal) |
| 0h4vp1o7-7puv.js | 123 | 36 | 1/64 | /lop-hoc/cnc | CNC workspace |

Ngoài ra `187wmq_p7eo-s.js` **1319 KB** (332 KB gzip) là chunk `heic2any` — đã lazy (`await import`), không nằm trong script tag nào.

### JS tải ban đầu theo trang (tổng `<script>` chunk, KB chưa gzip)

| Trang | KB | Số chunk |
|---|---:|---:|
| /dashboard (Teacher Studio) | 2430 | 12 |
| /dashboard-thpt (HS THPT) | 1724 | 13 |
| /kiem-tra/lam | 1399 | 12 |
| /lop-hoc/bai | 1395 | 12 |
| /lop-hoc/ket-qua/chi-tiet | 1387 | 12 |
| /lop-hoc, /lop-hoc/lop-10..12, /khtn-9 | 1387 | 12 |
| /lop-hoc/cnc | 1358 | 12 |
| /quan-tri/nhap-bai | 1318 | 13 |
| /quan-tri/dang-de | 1311 | 13 |
| /quan-tri/hoc-sinh | 1296 | 12 |
| /phu-huynh | 1261 | 11 |
| / (trang chủ) | 1058 | 11 |
| /dang-nhap | 901 | 10 |

Nền dùng chung mọi trang ≈ 27-boq… + 3--yt5… + 3utnu… + vài chunk nhỏ ≈ **~850 KB raw / ~220 KB gzip** trước khi có nội dung trang.

## 3. Ảnh trong `public/` (21 MB)

20 ảnh lớn nhất (KB):

| KB | File |
|---:|---|
| 2408 | images/learning-path/khtn-9-vat-ly.png |
| 2020 | images/blog/co-bap-co-lai-khi-nang-ta-cover.png |
| 1876 | images/blog/co-bap-xuong-khop-don-bay.png |
| 576 | lessons/12-khai-niem-tu-truong/media/tu-pho.png |
| 348 | images/testimonials/thu-tay.jpg |
| 340 | lessons/12-su-chuyen-the/media/fig09.png |
| 284 | images/testimonials/nguoi-cha-thu-hai.jpg |
| 280 | lessons/12-khai-niem-tu-truong/media/dong-dien-thang.png |
| 272 | lessons/12-su-chuyen-the/media/fig05.png |
| 272 | lessons/12-khai-niem-tu-truong/media/ong-day.png |
| 252 | images/cnc/tien_bai4_de.png |
| 244 | lessons/12-thuc-hanh-do-nhiet/media/fig40.png |
| 236 | lessons/12-cd01-su-chuyen-the/media/fig13.png |
| 224 | images/testimonials/loi-tri-an-ca-lop.jpg |
| 208 | images/testimonials/thu-xuan-quynh-khanh-long.jpg |
| 204 | lessons/12-su-chuyen-the/media/fig07.png |
| 204 | lessons/12-khai-niem-tu-truong/media/vn-c28.png |
| 196 | images/testimonials/tuan-anh.jpg |
| 192 | lessons/12-khai-niem-tu-truong/media/vn-c50.png |
| 188 | lessons/12-khai-niem-tu-truong/media/dong-dien-tron.png |

`scripts/gen-image-dimensions.mjs` (prebuild) đã sinh `features/lessons/image-dimensions.json` cho 557 ảnh bài học → có sẵn width/height để chống nhảy layout.

## 4. Truy vấn Supabase

### `select("*")` (11 chỗ, 5 file)

- `app/quan-tri/(chooser)/page.tsx:61–66` — 6 bảng, nhưng chỉ `count`/`head:true` → không tốn băng thông.
- `services/classes.ts:96` — `classes` (`fetchClasses`) — chạy ở /lop-hoc, trang bài học, ThptStudentHome, TeacherThptProgress/Dashboard. **Đáng sửa nhất.**
- `services/rank.ts:264, 283, 380` — rank_tiers / rank_sources / rank_titles (admin).
- `lib/tro-giang/policy.ts:58` — ta_sessions.

### Truy vấn nối tiếp (waterfall) / N+1

**Phía học sinh**
- `app/lop-hoc/bai/page.tsx:307–347` — fetchLesson + fetchLessonItems → (effect 2) fetchExamMetas + scores + progress + fetchMyLearningProgress (bên trong thêm 2 bước) → **3 tầng**; `fetchMyLearningProgress` tải lại lesson_progress/exam_results/exams đã có; tải cả classes/chapters/lessons chỉ để tính bài trước/sau.
- `app/lop-hoc/page.tsx` — fetchLessons → fetchLessonProgressSummaries (2 tầng; kéo toàn bộ lesson_progress + exam_results của user không lọc).
- `app/lop-hoc/ket-qua/chi-tiet/page.tsx` — fetchMyExamResultDetail → fetchResultRpContext (2) + `rank.fetchFixableTopics` (4 nối tiếp: exam_question_results → question_topics → parent → rank_fix_attempts) ≈ 5 tầng.
- `components/dashboard/ThptStudentHome.tsx` — fetchMyNeeds → fetchMyExitAttempts; classes/chapters/lessons → summaries.
- `components/lessons/PracticeSession.tsx` — fetchExamsFull chờ cha tải items xong.
- `services/progress.ts:fetchRawProgressBatch` — Promise.all(5) → exam_result_scores `.in` (2 tầng; dùng cho cả HS lẫn GV).
- `services/analytics.ts:fetchMyWrongQuestions` — exam_question_results → exam_results (2).
- `services/thpt-courses.ts` — thpt_courses → rpc thpt_course_seats (2) ở fetchPublicCourses/fetchCourse/fetchCoursesForClass.
- `services/lessons.ts` — fetchLessons/fetchLesson/fetchExamMetas/fetchLessonItems retry tối đa 3 lần với cột cũ khi thiếu migration (chỉ tốn khi DB thiếu cột).
- Ghi (không ưu tiên): `ExamRunner` submit 4 bước; `savePracticeSession` 4 bước.

**Phía giáo viên / Journey / quản trị**
- Điểm danh N+1: `fetchAttendanceSessions` → 1 query `fetchAttendanceRecords(sessionId)` cho mỗi buổi — lặp ở 9 component: TeacherThptOverview, TeacherThptStudentProfile, HomeroomGradebook, HomeroomAttendancePanel, TeacherFinalGradebook, TeacherOverview, CourseRosterPanel, attendance/TeacherThptAttendancePanel, attendance/TeacherAttendancePanel (gốc: `services/class-attendance.ts`, `services/course-attendance.ts` nhận 1 session id).
- `components/dashboard/CourseRosterPanel.tsx:reloadCourseData` — 5 tầng.
- `components/dashboard/TeacherThptProgress.tsx` — 4 tầng (classes/chapters/lessons → fetchLessonItems → fetchClassLearningProgress).
- `components/dashboard/TeacherThptDashboard.tsx` — classes → fetchClassStudents rồi mọi tab mới chạy.
- `fetchClassExamResults(studentIds)` bị gọi lặp riêng ở TeacherThptOverview / Gradebook / Analysis / StudentProfile (trùng, không phải waterfall) — tính lại từ dòng thô `exam_question_results` ở client.
- `components/tro-giang/AdminMonthlyTable.tsx` — 1 rpc `getMonthlyScore` cho mỗi trợ giảng (N+1).
- `components/admin/ExamPicker.tsx:loadSelected` — vòng lặp `.in` từng 100 id nối tiếp.
- `components/admin/ClassesAdmin.tsx:syncManagedClasses` — vòng lặp update/insert nối tiếp (ghi).

### Thư viện nặng đang import tĩnh

- **exceljs**: `services/homeroom-records.ts` (← HomeroomGradebook), `services/roster-export.ts` (← CourseRosterPanel), `services/excel-export.ts` (không ai import).
- **xlsx**: `services/roster-import.ts` ← `components/dashboard/ClassRosterImportPanel.tsx` ← TeacherThptDashboard, CourseRosterPanel, admin/StudentsAdmin.
- **katex**: `components/exams/ContentHtml.tsx` ← 20 trang (HS: lop-hoc/bai, tin-tuc, QuestionCard, InlineLessonAccordion, WorkedQuestionsGrid, StudentResultsDashboard; CNC: CncCourseWorkspace, CncCourseAnnouncements; GV: TeacherThptAnalysis, ReviewBoard, 6 file admin/*).
- **framer-motion**: ExamRunner, ExamResultSummary, QuestionCard, RankPage, FixQuizModal, TutoringExitQuiz, FormulaPanel, ui/Modal, ui/Reveal.
- **marked**: `lib/blog.ts`. **@xmldom/xmldom**: không ai import (thừa). **heic2any**: đã lazy.
- docx parser (`services/docx-exam-parser`, `docx-reader`, `docx-zip`, `omml-to-latex`) ← `components/admin/ExamSection.tsx`; `latex-converter` ← `admin/LaTexEditor.tsx`, `services/lesson-import.ts`.

## 5. Lighthouse (desktop preset, build tĩnh serve tại localhost, Supabase thật)

Server tĩnh `python -m http.server` (không gzip, không cache) → "JS" là byte thô. Chạy 1 lần, headless Chrome; trang đề id=118 chưa đăng nhập nên chỉ đo shell.

| Trang | Score | FCP | LCP | TBT | CLS | Speed Index | JS tải | Ảnh tải | Font files | Req Supabase | JS không dùng |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `/` trang chủ | **68** | 2.0 s | **4.0 s** | 0 ms | 0 | 2.0 s | 1600 KB | **4618 KB** | 15 | 0 | 961 KB |
| `/lop-hoc/bai/?id=2` | **78** | 0.9 s | **3.8 s** | 0 ms | 0 | 0.9 s | 1690 KB | 1354 KB | 12 | 10 | 1034 KB |
| `/kiem-tra/lam/?id=118` | 90 | 0.9 s | 1.9 s | 0 ms | 0 | 0.9 s | 1693 KB | 0 | 7 | 0 | 1096 KB |

Nhận xét: TBT/CLS đã tốt; vấn đề là **LCP** (trang chủ tải 4.6 MB ảnh; trang bài 10 request Supabase nối tiếp trước khi có nội dung) và **~1 MB JS không dùng** trên mọi trang (xlsx/exceljs/katex/framer vào chunk chung). Lệnh đo lại:

```bash
cd out && python3 -m http.server 8765 &
npx lighthouse http://localhost:8765/ --only-categories=performance --preset=desktop --output=json --output-path=perf/lh-home.json --chrome-flags="--headless=new"
```


## 6. Phân vùng file cho Pha 2 (không giao nhau)

**Vùng HS** (Agent D)
- `app/page.tsx`, `components/home/*`
- `app/lop-hoc/page.tsx`, `app/lop-hoc/bai/page.tsx`, `app/lop-hoc/ket-qua/page.tsx`, `app/lop-hoc/ket-qua/chi-tiet/page.tsx`, `app/lop-hoc/xep-hang/*`
- `app/kiem-tra/**`, `components/exams/ExamRunner.tsx`
- `app/dashboard-thpt/**`, `components/dashboard/ThptStudentHome.tsx`
- `components/lessons/PracticeSession.tsx`, `components/lessons/*` (trừ Cnc*)
- `components/results/StudentResultsDashboard.tsx`, `components/rank/*`
- `services/lessons.ts`, `services/progress.ts`, `services/classes.ts`, `services/rank.ts`, `services/analytics.ts` (phần `fetchMy*`), `services/thpt-courses.ts` (phần public/HS)

**Vùng GV / Journey / Quản trị** (Agent E)
- `app/dashboard/**`, `components/dashboard/Teacher*`, `components/dashboard/Homeroom*`, `components/dashboard/CourseRosterPanel.tsx`, `components/dashboard/ReviewBoard.tsx`
- `components/attendance/*`, `services/class-attendance.ts`, `services/course-attendance.ts`
- `components/competencies/*` (StudentCompetencyCard), Learning Journey
- `app/quan-tri/**`, `components/admin/*`
- `app/tro-giang/**`, `components/tro-giang/*`, `lib/tro-giang/*`
- `services/tutoring.ts`, `services/analytics.ts` (phần `fetchClass*`), `services/student-profile.ts`, `services/homeroom-*.ts`, `services/course-*.ts`, `services/class-*.ts`
- Migration mới trong `supabase/migrations/` (RPC + RLS rewrite)

Không đụng: `app/lop-hoc/cnc/**`, `components/lessons/Cnc*`, `services/cnc-*.ts` (mảng CNC/CTTC), trừ thay đổi dùng chung (font, layout gốc).
