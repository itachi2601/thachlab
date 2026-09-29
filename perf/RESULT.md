# RESULT — kiểm tra cuối đợt tối ưu tốc độ 9/2026 (Agent G, nhánh `perf/result`)

Mốc kiểm: `main` 79b40b97 (đã merge perf/assets, bundle, db-index, queries-hs, rpc-gv, static-content) · so với gốc `95976576` (BASELINE) · 29 commit, 122 file, +6950/−351 · ngày 25/9/2026.

**Tóm tắt 5 dòng**
1. Build sạch OK (22,4 s), `tsc --noEmit` OK (9,1 s, 0 lỗi), lint 50 lỗi / 10 cảnh báo (có sẵn từ trước, không tăng).
2. Lighthouse trang chủ **68 → 91** (LCP 4,0 → 1,9 s, ảnh 4,6 MB → 0,6 MB), trang bài học **78 → 83** (LCP 3,8 → 3,0 s, Supabase 10 → 4 request, nội dung tới từ `/data/lessons/*.json`), trang làm đề 90 → 90, `/lop-hoc/lop-12` 90. Không còn request Google Fonts.
3. Smoke test 13 trang trên build tĩnh: **không có lỗi console do code**; ảnh, KaTeX, mô phỏng con lắc, "Không tìm thấy" đều đúng. Duy nhất 1 lỗi console `404 /data/lessons/99999.json` là cơ chế fallback chủ ý (xem §5).
4. Bundle: `out/` 41 → 34 MB; /dashboard 2430 → 931 KB, /dashboard-thpt 1724 → 922 KB, /lop-hoc 1387 → 960 KB, / 1058 → 921 KB. **Nhưng** /lop-hoc/bai và /kiem-tra/lam gần như không giảm (1395 → 1405, 1399 → 1404 KB) vì KaTeX (290 KB) + framer-motion (139 KB) vẫn nằm trong JS ban đầu; JS nền dùng chung mọi trang 880 KB raw / 253 KB gzip — không giảm so với gốc (~850/220).
5. Không sửa code. 3 migration SQL + 1 rollback chờ thầy chạy tay (§6); 11 việc cần thầy quyết (§8). File tĩnh `out/data` không lộ đáp án (0 file khớp `answer/is_correct/solution`; chỉ `ly_thuyet` có `body_html`).

## 1. Build / kiểu / lint

| Bước | Kết quả | Thời gian |
|---|---|---:|
| `rm -rf .next out && npm run build` | OK — prebuild `build-content` (4 lớp · 22 chương · 116 bài · 252 mục → 118 file, 895 KB, 3,0 s) + `gen-image-dimensions` (557 ảnh); Turbopack compile 5,7 s; 64 trang tĩnh | 22,4 s |
| `npx tsc --noEmit` | OK, 0 lỗi | 9,1 s |
| `npm run lint` | 60 vấn đề (50 lỗi, 10 cảnh báo) — có sẵn trước đợt này | — |

Cảnh báo build duy nhất: Next đoán workspace root sai vì có `/Users/MAC/package-lock.json` (đặt `turbopack.root` trong `next.config` nếu muốn tắt; không ảnh hưởng kết quả).

## 2. Lighthouse (desktop preset, serve tĩnh `python -m http.server 8765`, không gzip, Supabase thật, chưa đăng nhập)

Ba cột: **Gốc** (BASELINE) / **Pha 1** (PHASE1_NOTES) / **Cuối** (lần này). JS/ảnh = byte tải thô.

| Trang | Score | FCP | LCP | TBT | CLS | JS | Ảnh | Font | Google | Supabase | `/data` | JS không dùng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `/` | 68 / 91 / **91** | 2,0 / 0,8 / **0,8 s** | 4,0 / 1,9 / **1,9 s** | 0 | 0,006 | 1600 / 1313 / **1320 KB** | 4618 / 589 / **589 KB** | 15 / 17 / 17 | 0 / 0 / **0** | 0 / 0 / 0 | 0 | 961 / 838 / **841 KB** |
| `/lop-hoc/bai/?id=2` | 78 / 83 / **83** | 0,9 / 0,6 / **0,6 s** | 3,8 / 3,1 / **3,0 s** | 0 | 0 | 1690 / 1547 / **1561 KB** | 1354 / 669 / **669 KB** | 12 / 16 / 16 | 0 | 10 / 10 / **4** | 2 | 1034 / 893 / **902 KB** |
| `/kiem-tra/lam/?id=118` | 90 / 90 / **90** | 0,9 / 0,7 / **0,6 s** | 1,9 / 2,0 / **2,1 s** | 0 | 0 | 1693 / 1550 / **1561 KB** | 0 | 7 / 14 / 13 | 0 | 0 | 0 | 1096 / 956 / **963 KB** |
| `/lop-hoc/lop-12/` | — / — / **90** | **0,5 s** | **2,1 s** | 0 | 0 | **1571 KB** | 0 | 15 | 0 | **4** | 1 | **937 KB** |

Nhận xét:
- Phần thắng lớn nằm ở Pha 1 (ảnh, font tự host). Pha 2 (static-content + gộp truy vấn) giảm Supabase request trang bài 10 → 4 (2 truy vấn thật `lessons` + 2 preflight OPTIONS), LCP 3,1 → 3,0 s trong mô phỏng — nhỏ vì LCP của trang bài giờ bị chặn bởi **~1,5 MB JS** (Lighthouse mô phỏng 10 Mbps → riêng tải JS ≈ 1,2 s), không còn bởi mạng Supabase. Với người dùng thật ở VN (Sydney RTT ~120 ms × 10 request nối tiếp → 4 song song) lợi ích thực sẽ lớn hơn số mô phỏng.
- Số font 15–17 file (nhiều hơn gốc 12–15) là do `next/font` tách theo unicode-range (latin + vietnamese + latin-ext); đổi lại **0 request tới googleapis/gstatic** (gốc: chặn render bằng `@import`).
- JS không dùng vẫn ~840–960 KB / trang: supabase-js + GoTrue (211 KB) và react-dom (222 KB) trong nền, KaTeX + framer trên trang bài/đề.
- Phần tử LCP: `/` = h1 hero (không phải ảnh, tốt); `/lop-hoc/bai` = ô `<th>` bảng trong lý thuyết (render sau khi JS + `/data/lessons/2.json` về).

## 3. Bundle JS (build sạch, `perf/chunks-report.mjs` → `/tmp/chunks-final.md`)

| Trang | Gốc (KB) | Cuối (KB) | Chunk | Ghi chú |
|---|---:|---:|---:|---|
| `/` | 1058 | **921** | 11 | framer-motion đã ra khỏi JS ban đầu (Reveal lazy) |
| `/lop-hoc` (+ lop-10/11/12, khtn-9) | 1387 | **960** | 11 | nhưng KaTeX 290 KB + framer 139 KB **vẫn được tải ngay sau hydrate** (0,10 s, InlineLessonAccordion/ContentHtmlLazy) → tổng JS thực Lighthouse thấy 1571 KB; chỉ lợi ở chỗ hydrate xong trước khi tải |
| `/lop-hoc/bai` | 1395 | **1405** | 13 | KaTeX + framer import tĩnh — không đổi |
| `/kiem-tra/lam` | 1399 | **1404** | 13 | như trên (ExamRunner dùng framer, QuestionCard dùng KaTeX) |
| `/dashboard-thpt` | 1724 | **922** | 11 | xlsx đã lazy |
| `/dashboard` | 2430 | **931** | 11 | exceljs/xlsx/marked lazy, tab tách chunk |
| `/quan-tri/dang-de` | 1311 | **1029** | 13 | |
| `/tin-tuc` | — | **914** | 11 | KaTeX lazy (chunk 2u15lzxx tải sau, 1 lần) |

Tổng: `out/` **41 → 34 MB**; `out/_next/static/chunks` **10,0 → 9,6 MB**; `out/data` **1,3 MB** (mới; catalog 41 KB + 116 file bài + manifest).

5 chunk lớn nhất (file, không phải tải ban đầu): `187wmq_p7eo-s.js` 1320 KB (heic2any, lazy), `1f_m__divrppg.js` 910 KB (exceljs + marked, lazy), `3vssgggexoysb.js` 469 KB (xlsx, lazy), `2u15lzxx_hw6k.js` 290 KB (KaTeX, 6/64 trang tải tĩnh), `098t6bnouksse.js` 222 KB (react-dom, mọi trang).

Chunk nền 64/64 trang (10 file): react-dom 222 · supabase-js+GoTrue 211 · next runtime 144 · polyfills 110 · 55 · 44 · 35 · 28 · 19 · turbopack 11 = **880 KB raw / 253 KB gzip** (gốc ước ~850/220 — không giảm; phần "app shell" 148 KB cũ đã tách nhỏ nhưng tổng không đổi).

## 4. Smoke test (Browser pane, `http://localhost:8765`, viewport 1280×900, chưa đăng nhập)

Mỗi trang: `read_console_messages onlyErrors` + kiểm bằng JS (`.katex`, ảnh `complete && naturalWidth>0`, `document.fonts.status`, request tới supabase.co và `/data/`).

| Trang | Kết quả |
|---|---|
| `/` | **OK**. Hero mô phỏng là SVG (không canvas): vị trí vật `translate(97, 146.025…)` → `146.065…` sau 1 s, rAF chạy (31 khung/500 ms dù tab ẩn). Fonts `loaded` (22 face). 0 request Supabase, 0 Google. Cuộn tới cuối: 10/10 ảnh tải (4 .webp testimonials/learning-path OK), khối Reveal hiện nội dung; footer bình thường, không lỗi console. Còn 1 `<figure>` testimonial giữ `opacity:0` sau khi cuộn lướt qua — chỉ xảy ra khi tab ở trạng thái `document.hidden` (IntersectionObserver bị throttle), tab hiện thì các khối khác đều hiện; thầy xem lại bằng mắt (§7). |
| `/lop-hoc/` | **OK**. 4 lớp + CTTC, đọc `/data/catalog.json`; Supabase 2 truy vấn nhẹ (`posts`, `lessons` đối chiếu). Không lỗi. |
| `/lop-hoc/lop-10/` | **OK**. 7 chương (Mở đầu → Biến dạng vật rắn), Chương 1 mở sẵn: 3 bài + Kiểm tra chương, mỗi bài có mô tả/YCCĐ và "3 mục". Không lỗi. |
| `/lop-hoc/bai/?id=49` (Bài 4 Độ dịch chuyển, Chương 2 Động học lớp 10) | **OK**. Nội dung từ `/data/lessons/49.json` + catalog; 5 `.katex`, 0 `.katex-error`; 8/8 ảnh `/lessons/do-dich-chuyen-quang-duong-di-duoc/media/*.png` tải (lazy, cần cuộn); 1 bảng không tràn ngang; 4 mục (Lý thuyết, Bài tập mẫu, Luyện tập…). Supabase 2 truy vấn `lessons`. |
| `/lop-hoc/bai/?id=99999` | **OK** — hiện "Không tìm thấy bài học này." Server trả `404 /data/lessons/99999.json` → trình duyệt ghi 1 dòng lỗi console "Failed to load resource 404" rồi lùi về Supabase (đúng thiết kế). Đây là **lỗi console duy nhất** trong toàn bộ smoke test; các trang sau vẫn thấy dòng này vì console cộng dồn theo tab (log server xác nhận chỉ đúng 1 request 404). |
| `/lop-hoc/bai/?id=2` (Bài 1 Sự chuyển thể, lớp 12) | **OK**. `/data/lessons/2.json`; 2 `.katex`; 10/10 ảnh; không tràn. |
| `/kiem-tra/lam/?id=118` | **OK** — "Em cần đăng nhập để sử dụng tính năng này." + nút Đăng nhập/Đăng ký; 0 request Supabase; không lỗi. |
| `/tin-tuc/` | **OK**. 1 bài "bài 1: Thuyết động học phân tử"; chunk KaTeX tải lazy (1 lần), 0 skeleton còn sót; không lỗi. |
| `/dashboard/`, `/dashboard-thpt/`, `/quan-tri/chu-de/` | **OK** — shell + màn yêu cầu đăng nhập; 0 request Supabase/`/data`; không lỗi. `/quan-tri/chu-de` dùng app shell quản trị riêng (không header công khai). |
| `/lop-hoc/cnc/` | **OK** — "Đăng nhập để học CNC"; không lỗi. |
| `/dang-nhap/` | **OK** — form email + password, nút Học sinh/Giáo viên/Google/Đăng nhập; không nhập gì. |

Ảnh chụp (scale 0,5) đã xem: trang chủ (hero + mô phỏng lò xo–đồ thị), `/lop-hoc/lop-10/`, `/lop-hoc/bai/?id=49` (lý thuyết + hình). Hiển thị đúng, không vỡ layout.

## 5. Kiểm tra tĩnh không lộ đáp án

- `grep -rl '"answer"\|"is_correct"\|"solution"' out/data | wc -l` → **0**. Thêm `answer_key|correct|correct_answer|explanation|answers` → 0.
- `out/data/lessons/*.json`: 252 mục — `ly_thuyet` 81, `luyen_tap` 80, `bai_tap_mau` 60, `kiem_tra` 26, `bai_tap_ve_nha` 5; **chỉ 81 mục `ly_thuyet` có `body_html`**; key `questions` có ở mọi mục nhưng luôn rỗng (0/252 có phần tử). Cột xuất: `id, lesson_id, kind, title, subtitle, video_url, pdf_url, exam_ids, sort_order, due_at, required, quiz_min_correct, practice_pass_score`.
- `catalog.json`: chỉ id/tên/mô tả/thứ tự/`itemRefs` (id + đề gắn). Không có nội dung đề.

## 6. Rà soát mã nguồn (đọc diff có chọn lọc)

| Mục | Phát hiện |
|---|---|
| (a) `next/dynamic` / `React.lazy` | 6 file dùng `dynamic`, đều có `loading`: TeacherCourseDashboard (11 tab) + TeacherThptDashboard (11 tab) → `TabSkeleton`; ContentHtmlLazy → span skeleton; LessonImporter → khối pulse; MistakeReviewPanel, FormulaPanel → `null` (hợp lý, là panel phụ). `components/ui/Reveal.tsx` dùng `lazy` + Suspense với fallback `opacity:0 translateY(28px)` **không có error boundary**: nếu chunk `RevealMotion` tải hỏng (mạng lỗi giữa chừng) thì mọi khối Reveal trên trang chủ / `/lop-hoc/*` ở `opacity:0` vĩnh viễn. Rủi ro thấp (chunk cùng origin, cache 1 năm) — ghi nhận, không sửa. |
| (b) RPC (`services/class-rpc.ts`) | `callClassRpc` trả `null` khi lỗi bất kỳ + cache tên hàm thiếu (PGRST202/42883). 4 hàm gọi qua đó (`fetchExamOverview`, `fetchWrongestQuestions`, `fetchClassTopicMatrix`, `fetchStudentLearningHistory`) đều `?? <đường cũ>`. RPC thứ 5 `ta_monthly_scores` ở `lib/tro-giang/queries.ts:230` không dùng `callClassRpc` nhưng tự fallback `Promise.all(getMonthlyScore)` khi lỗi hoặc thiếu người → OK. Web chạy đúng dù chưa chạy migration RPC. |
| (c) Lớp tĩnh `services/static-content.ts` | Chỉ 4 file HS import: `app/lop-hoc/page.tsx`, `app/lop-hoc/bai/page.tsx`, `components/dashboard/ThptStudentHome.tsx`, `components/lessons/InlineLessonAccordion.tsx`. Không có file nào trong `app/quan-tri`, `app/dashboard`, `components/admin`, `components/dashboard/Teacher*` → đúng. Smoke test xác nhận `/dashboard*`, `/quan-tri/chu-de` không gọi `/data/`. |
| (d) `scripts/deploy.sh` | `npm run build` (prebuild tự chạy build-content + gen-image-dimensions) → ghi `out/.htaccess` (chặn `.git`, cache 1 năm js/css/woff2) → **`out/data/.htaccess` cache 10 phút** (mkdir -p data) → git init nhánh `deploy` → force-push. Đúng như README. Lưu ý: `.htaccess` chỉ sinh lúc deploy, build local không có (bình thường). Ảnh png/jpg/webp vẫn **không** có cache header (§8). |
| (e) `.gitignore` | có `/public/_originals/` (dòng 53) và `/public/data/` (dòng 56), `/out/` (18). |
| (f) Secret | `git grep "SUPABASE_SERVICE_ROLE\|eyJ"` chỉ ra tên biến trong comment hướng dẫn của `scripts/*.mjs|mts` (`SUPABASE_SERVICE_ROLE_KEY=xxx`), 1 hash `integrity` trong package-lock và 1 file PNG nhị phân. **Không có giá trị key nào bị commit.** |
| Khác | `scripts/build-content.mjs` không làm fail build khi thiếu env/Supabase lỗi (giữ file cũ, không có thì manifest rỗng) — đã đọc xác nhận. `app/fonts.ts`: Be Vietnam Pro 400/600/700/800, Inter 400/500/600, JetBrains Mono chỉ 400 (§8 mục JetBrains 500). |

**Lỗi phát hiện (build/tsc/console/hiển thị): không có.** Mục cần lưu ý nhưng không phải lỗi: (1) console 404 `/data/lessons/<id>.json` với id không tồn tại — chủ ý; (2) Reveal không có error boundary — rủi ro thấp; (3) KaTeX/framer chưa tách khỏi trang bài/đề — chưa làm, không phải hỏng.

## 7. Thầy tự test bằng tài khoản thật (agent không đăng nhập)

1. **Học sinh THPT** → `/dashboard-thpt`: 3 mục (việc hôm nay · BTVN · phụ đạo) + bảng tuần hiện; mở 1 bài ở `/lop-hoc/bai/?id=2` đã đăng nhập → tiến độ/tick mục hiện đúng; làm `/kiem-tra/lam/?id=118` nộp 1 bài → có điểm, vào `/lop-hoc/ket-qua/chi-tiet` xem câu sai hiện đủ (đường 5 tầng → 2 tầng, commit 6eaf2299).
2. **Giáo viên THPT** → `/dashboard-thpt` (GV): tab Phân tích 1 đề (dùng RPC `get_class_exam_best` / `get_class_exam_question_stats` / `get_class_topic_matrix` nếu đã chạy migration, không thì đường cũ — số liệu phải giống nhau; đối chiếu bằng `npx tsx scripts/perf-compare-rpc.mts --class <id> --exam 118`), tab Hồ sơ HS (lịch sử học — `get_student_learning_history`), tab Điểm danh nhiều phiên (commit b29dc794), tab Phụ đạo, Gradebook.
3. **Giáo viên CTTC** → `/dashboard` (Teacher Studio): bấm lần lượt 11 tab — mỗi tab hiện skeleton rồi nội dung (chunk tách riêng); tab Sổ điểm chủ nhiệm bấm "Xuất Excel" (exceljs lazy), tab Danh sách bấm chọn file Excel (xlsx lazy) — phải mở được hộp thoại và xử lý file.
4. **Trợ giảng/Quản trị** → `/quan-tri/tro-giang` bảng điểm tháng (RPC `ta_monthly_scores`, fallback N lần `ta_monthly_score`); `/quan-tri/chu-de`, `/quan-tri/dang-de` (KaTeX lazy: công thức trong bảng Phân loại câu phải hiện sau ~1 s, không kẹt skeleton); `/quan-tri/nhap-bai` xem trước bài tập mẫu.
5. **Trang chủ** trên máy thật (tab hiện): cuộn chậm tới "Học trò nói gì" — 5 thẻ testimonial đều phải hiện dần (không thẻ nào trắng/ẩn); hero con lắc chạy mượt.
6. **Sau khi sửa lý thuyết một bài** (cùng tên, cùng mục) mà không deploy lại → web **vẫn hiện bản cũ** (tối đa 10 phút cache + tới khi chạy lại `scripts/deploy.sh`). Thầy cần nhớ quy trình mới này (README §"Học liệu tĩnh").

## 8. Migration chờ thầy chạy (KHÔNG `supabase db push` — thư mục `supabase/migrations/` mới, CLI không biết 99 migration cũ; dùng SQL Editor hoặc `supabase db query --linked -f <file>`)

| # | File | Mục đích | Khi nào chạy | Kiểm tra sau khi chạy | Rollback |
|---|---|---|---|---|---|
| 1 | `supabase/migrations/20260925120000_perf_indexes.sql` (116 dòng) | 7 index cho truy vấn nóng (question_bank browse, exam_attempts dở, exam_results (HS, đề), question_topics.name, lesson_items covering, essay chờ chấm, attendance machine_code); idempotent | Ngoài giờ HS làm bài (khoá ghi bảng < 100 ms mỗi lệnh) | 5 câu `explain (analyze, buffers)` ở `perf/DB_REPORT.md` §4 — kỳ vọng `Index Scan using idx_…`, không còn `Sort`/`Seq Scan`; so `Buffers: shared hit` trước/sau | Khối comment cuối file (dòng 108–116): 7 lệnh `drop index if exists` |
| 2 | `supabase/migrations/20260925130000_perf_rpc_gv.sql` (205 dòng) | 5 hàm `security invoker` (RLS người gọi vẫn áp dụng): `get_class_exam_best`, `get_class_exam_question_stats`, `get_class_topic_matrix`, `get_student_learning_history`, `ta_monthly_scores` — tính trên server thay vì tải hàng nghìn dòng thô về trình duyệt | Bất kỳ lúc nào (web chạy đúng cả trước và sau — client tự fallback) | `npx tsx scripts/perf-compare-rpc.mts` (chỉ đọc, cần `SUPABASE_SERVICE_ROLE_KEY` trong `.env.local`) — đường cũ và RPC phải ra cùng kết quả; rồi mở tab Phân tích/Hồ sơ HS/điểm tháng TG | Dòng 197–204: 5 lệnh `drop function if exists` (client thấy PGRST202 → về đường cũ) |
| 3 | `supabase/migrations/20260925140000_perf_rls.sql` (980 dòng, 1 transaction `begin…commit`) | 85 policy trên 53 bảng + 18 hàm helper: `auth.uid()` → `(select auth.uid())` (SubPlan mỗi dòng → InitPlan 1 lần); **điều kiện logic không đổi** (script sinh có assert), đã chạy thử trên pglite | Ngoài giờ HS làm bài; chạy sau #1, #2 (độc lập nhưng để tách bạch khi có sự cố) | `select relname, idx_scan from pg_stat_user_tables where relname='profiles'` — idx_scan phải ngừng tăng hàng nghìn/phút; EXPLAIN với `set role authenticated; set request.jwt.claims = '{"sub":"<uuid>","role":"authenticated"}'` phải thấy `InitPlan` thay `SubPlan` (DB_REPORT §4); đăng nhập 3 vai (HS, GV, admin) xem trang vẫn thấy đúng dữ liệu của mình | `perf/rollback/20260925140000_perf_rls.down.sql` (927 dòng, 1 transaction) — dump nguyên định nghĩa cũ ngày 25/9/2026 |

Thứ tự đề nghị: **1 → 2 → 3**, mỗi file một lần, xem kết quả rồi mới chạy file kế. Sau #1 vài ngày: xem `pg_stat_user_indexes.idx_scan` để quyết mục §9(3).

## 9. Việc cần thầy quyết / đề xuất ngoài phạm vi

| # | Việc | Nguồn | Đề xuất |
|---|---|---|---|
| 1 | **2 policy tautology** `attendance_sessions` "students read course attendance sessions" và `equipment_breakdown_reports` "students read equipment breakdown reports": điều kiện `e.course_id = e.course_id` (luôn đúng) → SV có 1 enrollment active đọc được buổi điểm danh / báo hỏng máy của **mọi** khoá. Migration #3 chép y nguyên (chỉ đổi cú pháp). | DB_REPORT §3.4, RLS_REPORT §3 | Hotfix riêng: đổi thành `e.course_id = attendance_sessions.course_id` / `= equipment_breakdown_reports.course_id`. Nên làm sớm — đây là lỗ hổng đọc chéo, không phải tối ưu. |
| 2 | `class_assessments` — "anyone reads class assessments" `using (true)` cho mọi tài khoản đăng nhập (kể cả lớp khác). `analytics.ts:81` đọc toàn bảng không lọc class_id. | DB_REPORT §3.4 | Xác nhận có chủ ý không; nếu không, thêm điều kiện thành viên lớp + sửa analytics.ts lọc theo class. |
| 3 | Drop `question_bank_grade_idx (subject_code, grade, archived)` — code không lọc `subject_code` trên question_bank. | DB_REPORT §2 | Sau khi chạy #1 vài ngày, nếu `idx_scan` của index cũ = 0 thì `drop index`. |
| 4 | **Cột `updated_at` cho `lessons` / `lesson_items`** (+ trigger) để lớp tĩnh phát hiện lý thuyết sửa tại chỗ; hiện phải deploy lại mới lên web. | README §Học liệu tĩnh, `services/static-content.ts:10` | Migration nhỏ (2 cột + trigger `set updated_at = now()`), rồi thêm `updated_at` vào catalog/đối chiếu. Đây là đổi nghiệp vụ → ngoài phạm vi đợt này. |
| 5 | JetBrains Mono chỉ nạp weight 400; 12 chỗ `font-mono` kèm `font-medium/semibold` sẽ được trình duyệt "làm đậm giả" (faux bold). | `app/fonts.ts` | Chấp nhận (khó nhận ra ở cỡ chữ nhỏ) hoặc thêm `"500"` (+1 file woff2 ~20 KB). |
| 6 | Ảnh trong Supabase Storage bucket `lesson-media` — có GIF/ảnh nặng > 150 KB; `scripts/optimize-storage-images.mjs` mới chỉ dry-run liệt kê. | commit 5c1ea210 | Chạy dry-run xem danh sách; GIF đổi sang video/WebP hoặc nén tay rồi upload đè; không tự động. |
| 7 | **Cache header cho ảnh** `png/jpg/webp` (public/lessons, public/images) trên host — `.htaccess` chỉ cache js/css/woff2 1 năm; ảnh bài học không đổi tên theo hash. | BASELINE §1, `scripts/deploy.sh` | Thêm `FilesMatch "\.(png|jpe?g|webp|svg)$"` cache 30 ngày (ảnh sửa thì đổi tên file). Việc 2 dòng nhưng đụng deploy.sh → thầy quyết. |
| 8 | `@xmldom/xmldom` (dependency) và `services/excel-export.ts` không có ai import. | BASELINE §4 | `npm uninstall @xmldom/xmldom` + xoá file; không ảnh hưởng bundle (không được import) nhưng gọn repo. |
| 9 | Supabase region **Sydney (ap-southeast-2)** → mỗi round-trip từ VN ≈ 100–150 ms. | BASELINE §1 | Chuyển project sang Singapore (ap-southeast-1) = tạo project mới + migrate dữ liệu + đổi URL/key + auth users — dự án riêng, cần kế hoạch downtime. Lợi ~3–4× độ trễ mỗi truy vấn cho mọi trang đăng nhập. |
| 10 | Bỏ `output: "export"` (chuyển sang Node/SSR trên host hỗ trợ Node) để render bài học/danh sách phía server, giảm ~1 MB JS trước nội dung. | BASELINE, kiến trúc | Thay đổi lớn (hosting, auth cookie, RLS phía server). Chỉ cân nhắc nếu số học sinh tăng mạnh; lớp tĩnh `/data` hiện đã giải quyết phần lớn cho khách chưa đăng nhập. |
| 11 | KaTeX vs MathJax | — | **Không áp dụng** — site đã dùng KaTeX 0.17 từ trước (BASELINE §1). |

Đề xuất kỹ thuật cho đợt sau (không cần thầy quyết, agent làm được): tách KaTeX (290 KB) và framer-motion (139 KB) khỏi JS ban đầu của `/lop-hoc/bai` và `/kiem-tra/lam` (hai trang HS dùng nhiều nhất, hiện vẫn 1,4 MB); ở `/lop-hoc/*` chỉ tải KaTeX khi accordion thật sự mở (hiện tải ngay sau hydrate); thêm error boundary cho `Reveal`; đặt `turbopack.root` để tắt cảnh báo build.
