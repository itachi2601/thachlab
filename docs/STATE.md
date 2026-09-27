# STATE — Hiện trạng ThachLab (cập nhật 26/09/2026)

File này là bản mô tả hiện trạng dùng chung cho mọi phiên Claude. Cập nhật sau mỗi đợt lớn.

## Hạ tầng
- Next.js App Router + TypeScript + Tailwind v4, `output: "export"` (xuất tĩnh), deploy bằng `scripts/deploy.sh` → nhánh `deploy`.
- Supabase project `fxnqgmfqdbvnjawgnsfi`, **region Sydney (ap-southeast-2)** → mỗi round-trip từ VN ~100–150 ms.
- Công thức: **KaTeX 0.17** (không phải MathJax).
- Font tự host qua `next/font` (Be Vietnam Pro 400/600/700/800, Inter 400/500/600, JetBrains Mono 400).
- 56 route `page.tsx`, 69 trang tĩnh khi build.
- Học liệu tĩnh: `scripts/build-content.mjs` chạy ở `prebuild`, xuất `public/data/` (catalog + 116 file bài). Sửa lý thuyết phải **deploy lại** mới lên web.

## Đã hoàn thành
- **Đợt tối ưu tốc độ (perf, 24–25/09)**: Lighthouse trang chủ 68→91, trang bài 78→83; `out/` 41→34 MB; ảnh 4,6 MB→0,6 MB; bỏ Google Fonts; Supabase request trang bài 10→4. Chi tiết: `perf/RESULT.md`.
- **Đợt Giai đoạn 0–1 (feat, 25/09)**: cột `difficulty` + `difficulty_source`, UI chọn mức ở Đăng đề, backfill bằng AI; nạp bundle lý thuyết lớp 12; RPC `get_lesson_mastery` / `get_chapter_mastery` + nhãn Nắm vững / Cần luyện thêm / Chưa đạt. Chi tiết: `feat/RESULT.md`.
- Hệ thống Rank/RP 7 bậc (Tinh Quang → Chí Tôn), nhiệm vụ hằng ngày, chuỗi ngày.
- Danh vị Vô Song (Paragon) trên Chí Tôn: migration `20260926100000_rank_paragon.sql` ĐÃ chạy 26/9/2026 (rollback `perf/rollback/…rank_paragon.down.sql`); chế độ admin "Xem như học sinh" mở khoá hết (features/rank/preview.ts).
- Loại GV/admin khỏi rank RP: migration `20260926110000_rank_exclude_staff.sql` ĐÃ chạy 26/9/2026 — chặn tận gốc (3 hàm) việc tài khoản không phải role='student' bị cộng RP/lọt bảng xếp hạng khi tự test bài, đã dọn sạch dữ liệu rác (rollback `perf/rollback/20260926110000_rank_exclude_staff.down.sql`).
- Vá 2 lỗ hổng RLS tautology + `class_assessments using(true)`: migration `20260926140000_fix_rls_tautology.sql` ĐÃ chạy 26/9/2026 (rollback `perf/rollback/20260926140000_fix_rls_tautology.down.sql`).
- Sửa `find_similar_bank_questions` (quét câu trùng ở `/quan-tri/ngan-hang-cau-hoi`) bị `statement
  timeout` vì self-join O(n²) mỗi topic → nested loop dùng index GIN trigram + set_limit + cap 20
  câu giống/mỗi câu: migration `20260926150000_fix_question_bank_similarity_timeout.sql` ĐÃ chạy
  27/9/2026 (log `scripts/logs/20260927-073246-*`, rollback
  `perf/rollback/20260926150000_fix_question_bank_similarity_timeout.down.sql`). Chưa xác nhận lại
  trên UI thật là mục "Nghi trùng lặp" đã lên danh sách.

## Migration — ĐÃ CHẠY XONG (27/09/2026, 07:32)
Cả 8 file trong `supabase/migrations/` đã chạy lên production qua `bash scripts/run-migrations.sh`:
perf_indexes, perf_rpc_gv, perf_rls, difficulty_source, mastery, lesson_item_draft_publish,
exam_violation_alert, fix_question_bank_similarity_timeout. Cộng rank_paragon, rank_exclude_staff,
fix_rls_tautology chạy trước đó. Rollback từng file ở `perf/rollback/`.

- Cột `exam_id` trên `class_announcements` (gắn đề vào "Việc cần làm hôm nay", nút "Làm bài" ở
  trang chủ HS): migration `20260927100000_class_announcement_exam.sql` ĐÃ chạy 27/9/2026 (log
  `scripts/logs/20260927-084117-*`, rollback `perf/rollback/20260927100000_class_announcement_exam.down.sql`).
  Code (services/announcements.ts, ClassAnnouncementsPanel, ThptStudentHome) đã deploy 27/9/2026.

- **Báo lỗi gắn vào đúng câu hỏi**: cột `exam_id`/`question_index` trên `bug_reports` + nhãn
  `category='cau_hoi'` — migration `20260927110000_bug_report_question_link.sql` ĐÃ chạy 27/9/2026
  (log `scripts/logs/20260927-104450-*`, rollback
  `perf/rollback/20260927110000_bug_report_question_link.down.sql`). Học sinh bấm "Báo lỗi câu này"
  ở màn Xem lại bài làm ([ReportQuestionButton.tsx](../components/exams/ReportQuestionButton.tsx));
  admin ở `/quan-tri/bao-loi` bấm link "Đề #… · Câu N →" nhảy thẳng vào `/quan-tri/sua-de?exam=&q=`,
  tự mở đúng đề + tô khung vàng đúng câu. Tiện thể vá luôn 1 lỗi nhỏ: nút "Báo lỗi / Góp ý" chung
  (mọi trang) trước làm rớt mất `#hash` của URL nên link báo lỗi lý thuyết chỉ mở tới đầu trang, mất
  luôn đoạn `#theory-sec-…` — đã sửa trong `BugReportWidget.tsx`. Đã deploy 27/9/2026 — **chưa test
  UI thật bằng tài khoản có login**.

**Không còn migration nào chờ.** Cột `lesson_items.summary_html` (Tóm tắt ý
chính cần thuộc) ĐÃ chạy 27/9/2026 (`20260927120000_lesson_item_summary.sql`,
log `scripts/logs/20260927-173722-*`, rollback
`perf/rollback/20260927120000_lesson_item_summary.down.sql`). Backfill đã xong: cả 81/81 mục
`ly_thuyet` có `summary_html` (script `scripts/backfill-lesson-summary.mts` — không rõ ai chạy,
kiểm tra thấy đã có dữ liệu sẵn khi thầy chạy lại 27/9 tối). Đã `bash scripts/deploy.sh` lại
(file tĩnh `public/data/` đã có nội dung mới, 81/81 file có `summary_html`) — khối "📌 Tóm tắt ý
chính" giờ lên web thật.

## Việc tay còn lại
- [ ] **Chấm BTVN trên lớp + BTVN ôn tập tự động sau chữa bài** (27/9/2026) — CODE ĐÃ
  VIẾT XONG nhưng **đã gỡ khỏi bản deploy 27/9** vì SQL còn ở dạng nháp, chưa thành
  migration, chưa chạy: `docs/supabase-migration-homework-check.sql` (bảng
  `class_homework_checks` — trợ giảng ước lượng % học sinh đã làm BTVN, cộng RP) và
  `docs/supabase-migration-class-review-homework.sql` (bảng `class_review_homework` —
  nút "Tạo BTVN ôn tập" ở Trình chiếu chữa bài). Các file component/service đã viết
  (`components/dashboard/HomeworkCheckPanel.tsx`, `components/results/ParentHomeworkNotes.tsx`,
  `services/homework.ts`, `services/homework-checks.ts`) hiện **không được import ở đâu cả**
  (cố ý gỡ dây khỏi `ClassAnnouncementsPanel.tsx`, `app/phu-huynh/page.tsx`,
  `components/dashboard/ThptStudentHome.tsx`, `components/dashboard/ReviewBoard.tsx`) để
  build/deploy các tính năng khác không bị vỡ do bảng chưa tồn tại. Việc còn lại: soạn 2
  file trên thành migration thật trong `supabase/migrations/`, chạy theo quy tắc
  AGENTS.md, rồi nối lại dây vào 4 file trên.
- [x] **Trang bài học: 6 mục thu gọn thành danh sách + Tóm tắt ý chính cần thuộc**
  (27/9/2026) — `app/lop-hoc/bai/page.tsx`: cả 6 mục (Lý thuyết/Video/Bài tập mẫu/
  Luyện tập/BTVN/Kiểm tra) giờ hiện dạng danh sách thu gọn, bấm mục nào xổ mục đó
  (mặc định đóng hết, trừ khi có link "Ôn ngay" hoặc "Tiếp tục học" trỏ thẳng vào 1
  mục thì tự mở mục đó). Mỗi mục lý thuyết có thêm khối "📌 Tóm tắt ý chính cần
  thuộc" (nếu có `summary_html`) — tự thu gọn riêng, độc lập với nội dung đầy đủ.
  Code đã deploy 27/9, backfill 81/81 mục xong, đã deploy lại — **đã lên web thật**,
  chưa tự kiểm bằng mắt trên trình duyệt thật.
  ở đâu cả vì `summary_html` chưa có dữ liệu**, chờ backfill (mục trên) rồi deploy lại.
- [x] **Backfill RP cho Kiểm tra lớp 10/11/12** (27/9/2026) — thầy đã chạy
  `docs/supabase-recompute-rank-backfill-20260927.sql`. exam 224/12/205/206/219 đã lên RP đầy đủ (trong
  khung mùa). exam 23 (lớp 10) và exam 9 (lớp 12) vẫn 0 RP vì toàn bộ lượt làm nằm TRƯỚC ngày mở mùa
  (season 5 mở 26/9, season 4 mở 21/9) — `rank_recompute_student` chỉ tính trong khung `starts_on..ends_on`,
  đây là thiết kế đúng, không phải lỗi. exam 214 chỉ có 1 lượt của tài khoản admin Thạch, bị loại đúng
  theo rank_exclude_staff.
- [ ] **Backfill mức độ câu hỏi** — còn ~3541/7223 câu `question_bank.difficulty` rỗng.
  Script **ghi thật ngay, không có dry-run**; tham số chỉ giới hạn số câu:
  `npx tsx scripts/backfill-question-bank-difficulty.mts 20` (thử nhỏ, xem lại
  `/quan-tri/ngan-hang-cau-hoi`, rồi chạy không giới hạn). Tốn API Anthropic (~90 lô × 40 câu).
- [x] **Kiểm hồi quy bằng tài khoản thật** (26/9/2026) — tạo 3 tài khoản test throwaway (student/
  instructor/admin, gán lớp 12) trên local dev server cô lập (git worktree riêng, port 3010, không
  đụng dev server phiên khác), 3 agent song song đăng nhập 3 vai + tự kiểm tay lại vai HS 1 lần
  riêng lẻ. Kết quả: HS làm đề 96 (nộp + chấm điểm đúng) + trang Rank, GV xem gradebook (208 lượt
  làm lớp 12) + phụ đạo (46 HS cần phụ đạo) + phân tích/cảnh báo, admin vào `/quan-tri/dang-de`
  (dropdown Lớp→Chương nạp đúng dữ liệu) + trang CNC `/quan-tri/cnc-bai-hoc` — **tất cả PASS, không
  phát hiện lỗi do AuthProvider mới**. Tài khoản test + dữ liệu liên quan đã xoá sạch sau khi xong.
  Ghi chú phụ (không phải lỗi AuthProvider): 3 agent chạy song song trên cùng origin bị đá phiên
  chéo nhau do Supabase dùng chung `localStorage` theo origin — xác nhận lại bằng cách chạy 1 mình
  thì không xảy ra. Phát hiện thêm (đã tách việc riêng): nút đáp án trong ExamRunner có thể re-render
  quá thường xuyên do đồng hồ đếm ngược, đáng xem lại hiệu năng (không phải lỗi chức năng).
- [x] **Đo lại PageSpeed trên site thật** (26/9/2026) — desktop **100**; mobile **74**; CrUX field
  (người dùng thật, 28 ngày) **LCP 2,7s → Core Web Vitals Failed** (ngưỡng đạt 2,5s, thiếu 0,2s),
  INP 172ms, CLS 0,07, TTFB 0,7s. Lighthouse lab mobile: LCP 5,5s, FCP 2,4s, **TBT chỉ 40ms**.
  Chẩn đoán (đo bằng Chrome trên production): brotli ĐÃ bật và chạy đúng; nghẽn nằm ở **font** —
  trang chủ tải **20 file woff2 = 323 KB**, và woff2 nén sẵn nên brotli không giúp gì. 15 file font
  được preload nằm ở request #2–#16, hai file CSS mãi #17–#18, tức font giành băng thông của CSS
  trước lúc vẽ trang. So sánh: JS 856 KB → ~250 KB sau brotli, CSS 280 KB → ~45 KB.
  → Đợt xử lý: `docs/prompt-toi-uu-font.md` — **ĐÃ XONG + deploy 26/9/2026** (commit `11aed966`).
  Cinzel/Playfair (tên bậc rank) tách khỏi root layout, chỉ trang có component rank mới tải;
  JetBrains Mono bỏ preload. Trang chủ: 20 file/323 KB → 17 file/262 KB (chưa đạt mục tiêu
  <10 file/<170 KB — phần còn lại là ký tự thật, không bỏ được mà không đổi giao diện). Lighthouse
  mobile trang chủ 80→92 điểm (đo lab, kiểm độc lập). Chi tiết: `perf3/RESULT.md`. Đã push nhánh
  `deploy`, hosting cập nhật trong ~10 phút — **chờ đo lại PageSpeed trên site thật**.
- **Đợt tối ưu tải số 4 (split-js5 + cache ảnh, 27/9/2026)** — **ĐÃ XONG + verify độc lập +
  deploy** (commit `f068cf95`, kiểm bởi phiên riêng: `perf4/BASELINE.md` + `perf4/RESULT.md`).
  Lần 1 (`6e9d07b3` perf/split-js4) tách JS `ExamRunner`/`PracticeSession`/`LessonMasteryCard`
  bị **revert** (`063a97a4`) vì crash trắng; sau khi có lưới an toàn `app/error.tsx` +
  `LazyErrorBoundary` (`9d22e14c`) mới làm lại an toàn (`f068cf95`), mỗi chunk mới bọc riêng
  `LazyErrorBoundary` cục bộ. Cộng thêm: cache header `Cache-Control` tường minh cho ảnh trong
  `scripts/deploy.sh` (đã kiểm cú pháp Apache `httpd -t` OK). Verify độc lập xác nhận: build/tsc
  sạch, không lỗi console 2 trang mục tiêu, KaTeX/framer-motion vẫn ngoài JS ban đầu (đúng từ
  đợt 2, không phải việc mới). **3 việc cần quyết (xem `perf4/RESULT.md` §6–7)**:
  1. `/lop-hoc/bai` còn dư ~34 KB so với mục tiêu <1000 KB (1033,7 KB) — toàn bộ phần dư là
     `QuestionCard`/`SampleQuestionsGrid` (mục "Bài tập mẫu", nội dung chính hiện ngay khi mở
     bài) — đợt 4 **không động tới** theo đúng phạm vi được giao. Muốn đạt <1000 KB thì phải
     tách `SampleQuestionsGrid` bằng `next/dynamic({ssr:false})` — đổi UX (chớp loading ngắn lúc
     đầu), cần quyết trước khi làm.
  2. **Lỗi nghiêm trọng phát hiện ngoài phạm vi đợt này**: xoá thử chunk `RevealMotion` (mô
     phỏng lỗi tải mạng/CDN) → trang chủ **crash trắng `Uncaught ChunkLoadError`** trong <2s,
     KHÔNG bị `RevealErrorBoundary`/`PendingFallback` bắt được (lỗi nằm trong
     `Promise.all` của runtime nạp chunk Turbopack, ngoài tầm với của ErrorBoundary React
     thường). Tái hiện 2 lần, đã phục hồi file ngay sau khi xác nhận. Đã `spawn_task` gắn cờ
     riêng cho thầy xem xét độc lập, KHÔNG sửa trong đợt 4 (đúng phạm vi được giao).
  3. Chưa tự test được luồng làm bài/nộp bài thật của `/kiem-tra/lam` (cần tài khoản học sinh
     thật, ngoài phạm vi phiên verify).

## CHƯA làm (đợt kế tiếp — prompt `prompt-giai-doan-1-2.md`)
- `/luyen-tap` có bộ lọc Lớp → Chương → Bài → YCCĐ → Dễ/TB/Khó (route chưa tồn tại).
- Thẻ "3 kỹ năng yếu nhất" trên dashboard học sinh + trọng số mức độ trong mastery.
- Bổ sung câu hỏi chương Động học 10 cho đủ ≥30 câu/bài.
- `/lo-trinh` — Learning Journey (route chưa tồn tại).

## Việc ngoài roadmap đang treo
- Chuyển Supabase sang Singapore (lợi ~3–4× độ trễ).
- Cột `updated_at` cho `lessons`/`lesson_items` để lớp tĩnh biết lý thuyết đã sửa.

(KaTeX/framer-motion đã xác nhận ngoài JS ban đầu từ đợt 2; cache header ảnh đã làm ở đợt 4 —
xem mục "Đợt tối ưu tải số 4" ở trên.)
