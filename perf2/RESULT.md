# RESULT2 — kiểm tra ĐỘC LẬP đợt tối ưu tốc độ lần 2 (9/2026)

Kiểm bởi agent riêng, không phải người làm 3 nhánh A (`perf2/split-js`) / B (`perf2/shell`) /
C (`perf2/hosting`). Đứng tại SHA merge `42a668d9f718bb49e2dd06e60877754ac74c6d88` (nhánh
`perf2/integration`, checkout ở detached HEAD trong worktree riêng vì nhánh đó đang được một
worktree khác giữ — `git merge-base --is-ancestor` xác nhận đúng chỗ trước khi đo). So với
`perf2/BASELINE2.md` (đo trên `main` `aaf7e464`).

**Tóm tắt 6 dòng**
1. Build sạch OK, `tsc --noEmit` 0 lỗi, lint **63 vấn đề (53 lỗi, 10 cảnh báo)** — khớp chính xác
   baseline, không tăng.
2. Mục tiêu **<1000 KB** cho `/lop-hoc/bai` và `/kiem-tra/lam` **KHÔNG đạt**: đo lại ra
   **1039 KB / 1023 KB** (đã giảm mạnh từ 1441/1424 nhưng còn dư đúng như Agent A tự nhận
   ~1027–1043 KB). Phần dư **không phải** KaTeX/framer (cả hai đã lazy đúng, không có trong 2
   trang này) — dư đến từ supabase-js+GoTrue (211 KB, cần thiết vì đây là trang cần đăng nhập)
   cộng dồn với JS riêng của từng trang (~211/194 KB, xem §3).
3. JS nền dùng chung 66/66 trang: đo lại **618,5 KB raw / 183,4 KB gzip** — khớp **chính xác**
   con số Agent B báo cáo (618,5/183,4), giảm thật từ 880/253 (-30%/-28%).
4. **Phát hiện lỗi thật** khi chủ động chặn chunk bằng cách xoá file trong `out/_next/static/chunks/`
   rồi phục vụ lại: chunk chứa `RevealMotion` (dùng trên trang chủ) tải lỗi (404) làm
   **crash trắng toàn trang** ("This page couldn't load", `Uncaught ChunkLoadError` không bị
   bắt bởi ErrorBoundary) — ngược với báo cáo của Agent A rằng ErrorBoundary hoạt động đúng. Xem
   §5, đã tái hiện 2 lần trên tab sạch, có đối chứng (chunk khác lỗi thì được bắt đúng, xem §5).
5. Trang công khai xác nhận qua Browser pane: `/` không tải chunk supabase-js/GoTrue (211 KB),
   `/tin-tuc` vẫn tải (đúng như Agent B chủ ý), cả hai không lỗi console. Rà tĩnh 66 route: đúng
   12 trang không có AuthProvider (`/`, `/404`, `/_not-found`, `/blog` + 6 bài, `/khoa-hoc`,
   `/tro-giang/mau`) — toàn bộ là trang công khai hợp lý, không route cần đăng nhập nào bị sót.
6. Không có tài khoản test → hồi quy chỉ kiểm tĩnh (rà 22 `layout.tsx`): mọi route cần đăng nhập
   đều có đúng 1 `AuthedShell` tổ tiên, nhóm quản trị con dùng `RequireAuth` (không lặp
   `AuthProvider`), `useAuth()` có giá trị mặc định "khách" nên không throw khi thiếu Provider.
   Không có migration SQL mới trong đợt này.

## 1. Build / kiểu / lint

| Bước | Kết quả |
|---|---|
| `rm -rf .next out && npm run build` | OK, 66 trang tĩnh |
| `npx tsc --noEmit` | OK, 0 lỗi |
| `npm run lint` | **63 problems (53 errors, 10 warnings)** — đúng bằng baseline gốc, không tăng |

## 2. Lighthouse mobile (Chrome headless, throttle mô phỏng mặc định)

**Lưu ý về môi trường:** máy đo là sandbox dùng chung (load average 5–7 trên 8 lõi lúc đo, do
nhiều phiên Claude khác chạy song song) — khác hẳn máy đo BASELINE2.md ("máy đo tại VN", tải
riêng). Đo lại 2 lần trang `/lop-hoc/lop-10/` cho kết quả ổn định trong CHÍNH môi trường này
(LCP 9,8 s rồi 9,3 s, JS 961 KB cả hai lần) — nghĩa là số tuyệt đối lệch so với BASELINE2 nhiều
khả năng do **khác máy đo**, không phải nhiễu ngẫu nhiên hay do code đợt này. Vì vậy bảng dưới chỉ
nên đọc theo hướng "không tệ đi bất thường", không nên trừ trực tiếp số LCP cũ/mới làm kết luận
regression.

| Trang | Score (gốc→nay) | FCP | LCP | TBT | JS transfer (Lighthouse, gồm cả prefetch) | Supabase request |
|---|---:|---:|---:|---:|---:|---:|
| `/` | 65 → 65 | 4,06→4,1 s | 10,41→9,1 s | 20→30 ms | 793→1262 KB* | 0→0 |
| `/lop-hoc/bai/?id=49` | 71 → 70 | 2,71→2,9 s | 9,34→9,8 s | 55→20 ms | 1398→1019 KB | 0→0 |
| `/kiem-tra/lam/?id=118` | 70 → 70 | 3,16→2,9 s | 7,47→10,1 s | 43→10 ms | 1382→1003 KB | 0→0 |
| `/lop-hoc/lop-10/` | 82 → 72 | 1,07→2,4 s | 4,93→9,8 s (rerun 9,3 s) | 19→10-30 ms | 450→961 KB | 0→0 |

`*` Cột "JS transfer" của Lighthouse đếm **toàn bộ** request JS trong phiên trace, kể cả chunk
Next.js prefetch ngầm cho các link khác trên trang (ví dụ trang chủ có nhiều link nên prefetch cả
chunk `supabase-js` (211 KB) và **2 bản framer-motion riêng** (139 KB × 2, xem §5) dù không dùng
ngay) — số này **không phản ánh đúng "JS ban đầu"** và không nên dùng để so KB trực tiếp với
BASELINE2 cột "JS transfer". Số đáng tin cho "JS ban đầu" là `<script src>` thực trong HTML — xem
§3 (dùng đúng phương pháp `perf/chunks-report.mjs` của BASELINE2 mục 2–3): trang chủ **682 KB**
(giảm so với gốc, không tăng), 2 trang mục tiêu xem bảng dưới. Không có request Supabase nào ở cả
4 trang khi chưa đăng nhập, khớp baseline.

Điểm `/lop-hoc/lop-10/` giảm 82→72 và LCP tăng đáng kể đứng riêng lẻ trông giống regression,
nhưng đo lặp lại 2 lần trong đúng phiên này cho số gần giống nhau (9,8 rồi 9,3 s) — nghĩa là con
số **ổn định trong môi trường này**, chênh với baseline nhiều khả năng do khác máy đo (xem lưu ý
trên) chứ không do 1 lần đo ngẫu nhiên. Khuyến nghị thầy tự đo lại 4 trang này trên máy thật
(giống cách đo BASELINE2) nếu cần con số Lighthouse đáng tin để so sánh trực tiếp.

## 3. JS ban đầu 2 trang học sinh — đo lại bằng `perf/chunks-report.mjs`

| Trang | BASELINE2 | Đo lại (KB, chunk) | Đạt <1000 KB? |
|---|---:|---:|---|
| `/lop-hoc/bai` | 1441 KB | **1039,4 KB (14 chunk)** | **KHÔNG** (dư 39,4 KB) |
| `/kiem-tra/lam` | 1424 KB | **1023,3 KB (13 chunk)** | **KHÔNG** (dư 23,3 KB) |

Khớp với báo cáo của Agent A (tự nhận ~1027–1043 KB, không đạt hẳn) — đo độc lập ra đúng tầm đó.
Gzip: `/lop-hoc/bai` ≈ 292,7 KB, `/kiem-tra/lam` ≈ 287,4 KB.

**Phần dư đến từ đâu** (đối chiếu từng chunk, không đoán): sau khi trừ 8 chunk nền dùng chung
66/66 trang (618,5 KB — xem mục dưới), phần còn lại của `/lop-hoc/bai` (420,8 KB) gồm:

| Chunk | KB | Ghi chú |
|---|---:|---|
| `2zlcdknyjvmj1.js` | 211,2 | supabase-js + GoTrue — **bắt buộc** vì đây là trang cần đăng nhập |
| `1r7v9gh512xhf.js` | 71,0 | logic riêng trang (không phải katex/framer) |
| `1c7c9v78vwif6.js` | 51,9 | dùng chung với `/kiem-tra/lam` |
| `2yqvdkamv0kdn.js` | 39,0 | riêng trang |
| `3kr9x-paafwex.js` | 32,6 | dùng chung với `/kiem-tra/lam` |
| `205wgliey28hh.js` | 15,1 | dùng chung với `/kiem-tra/lam` |

`/kiem-tra/lam` tương tự: 211,2 (supabase/GoTrue) + `3jskf4bfpzjey.js` 93,9 + 51,9 + 32,6 + 15,1 =
193,5 KB dư ngoài phần nền. **Không có chunk nào cỡ 139 KB (framer) hay 290 KB (katex) trong danh
sách `<script>` ban đầu của 2 trang này** — nghĩa là Agent A lazy KaTeX/framer đúng như báo cáo;
phần dư khiến không đạt mốc <1000 KB là do (a) chi phí GoTrue không thể tránh khỏi trên trang cần
đăng nhập, và (b) JS logic riêng của từng trang (~193–211 KB) chưa được chia nhỏ thêm. Muốn đạt
mốc, cơ hội rõ nhất là `1r7v9gh512xhf.js` (71 KB, riêng `/lop-hoc/bai`) hoặc
`3jskf4bfpzjey.js` (94 KB, riêng `/kiem-tra/lam`).

## 4. JS nền dùng chung 66/66 trang

Viết script đếm đầy đủ (không chỉ top 10 như `chunks-report.mjs` mặc định) — chunk xuất hiện trên
**cả 66 trang tĩnh**:

| Chunk | KB raw | KB gzip |
|---|---:|---:|
| `0czglbtyfc7wn.js` (react-dom) | 222,3 | 69,4 |
| `1dfbzb55lzf_c.js` | 143,9 | 38,7 |
| `0cz1d0mv5g_q7.js` | 110,0 | 38,6 |
| `3yaqi--1zc_bg.js` | 55,1 | 12,8 |
| `0bqd-nq1qfz0f.js` | 43,6 | 9,0 |
| `14nxnhkbwy37c.js` | 28,3 | 8,6 |
| `turbopack-1-...js` | 10,8 | 4,2 |
| `1zch1yfo_1kgt.js` | 4,5 | 2,0 |
| **Tổng (8 chunk)** | **618,5** | **183,4** |

**Khớp chính xác** con số Agent B báo cáo (618,5 KB raw / 183,4 KB gzip) — giảm thật từ baseline
880/253 (**-30% raw, -28% gzip**). Chunk supabase-js+GoTrue (211 KB) **không còn** nằm trong tập
nền dùng-chung-mọi-trang — giờ chỉ xuất hiện trên 54/66 trang (đúng phần cần đăng nhập), xem §5.

## 5. KaTeX lazy — kiểm bằng code (không kiểm được bằng trình duyệt thật)

Worktree kiểm tra này **không có** `.env.local`/khoá Supabase (đúng chủ ý an toàn — sandbox không
được cấp khoá, và `*.supabase.co` bị proxy chặn ở môi trường này) → `scripts/build-content.mjs`
build ra `out/data/manifest.json` rỗng (`"lessons":0`), nghĩa là bản build tĩnh này **không có nội
dung bài học thật nào** để mở accordion/kiểm công thức. Đây là hạn chế của môi trường kiểm tra,
không phải lỗi code.

Đọc `components/exams/ContentHtml.tsx` thay thế:
- `hasMath()` dùng regex `/\$|\\\(|\\\[/ ` để phát hiện dấu hiệu công thức trước khi quyết định
  tải KaTeX — đúng như mô tả.
- `loadKatex()` chỉ chạy trong `useEffect`, có điều kiện `if (!needsMath) return;` — nội dung
  không công thức thì `import("katex")` **không bao giờ** được gọi. Logic đọc đúng.
- Khi tải xong, so khớp `forHtml === cleaned` trước khi dùng kết quả render — tránh hiển thị công
  thức của nội dung cũ khi props đổi nhanh. Có fallback hiển thị LaTeX thô trong `<code>` lúc chờ
  hoặc khi tải lỗi (không throw, không kẹt trắng).

Đã xác nhận riêng: chunk KaTeX **có tồn tại** trong `out/_next/static/chunks/` (tìm thấy 1 file
chứa chuỗi `katex`), nhưng vì không có trang nào thực sự render nội dung có `$...$` trong bản build
này, không thể xác nhận bằng `read_network_requests` thời điểm chunk được gọi. **Kết luận: kiểm
bằng đọc code, không kiểm được bằng trình duyệt thật** (thiếu nội dung, không thiếu công cụ).

## 6. Reveal ErrorBoundary — phát hiện lỗi thật khi chặn chunk (không chỉ đọc code)

Cách làm: build → serve `out/` → xoá tạm 2 file chunk chứa `RevealMotion`/`QuestionSlideMotion`
trong `out/_next/static/chunks/` (xác định bằng cách tìm 2 chunk ~139 KB có chuỗi `whileInView`
+ `framer` trong nội dung — 2 file lazy component duy nhất trong toàn repo, xem
`grep -rn "= lazy("`), phục vụ lại (404 khi trình duyệt xin file), mở tab **sạch** (không cache
console cũ) và quan sát.

| Chunk xoá | Component tương ứng | Có dùng trên trang chủ? | Kết quả |
|---|---|---|---|
| `1-atqt10fxpna.js` (module 12036) | `QuestionSlideMotion` (chỉ dùng trong `ExamRunner.tsx`, KHÔNG render trên `/`) | Không — chỉ bị Next.js prefetch ngầm cho link tới `/kiem-tra` | Console có `ChunkLoadError` (không có "Uncaught") nhưng **nội dung vẫn hiện đủ, opacity 1** — vì component này chưa từng thực sự mount trên trang chủ, request lỗi chỉ là prefetch bị bỏ qua |
| `1hxcubibwujmz.js` (module 69790) | `RevealMotion` (dùng thật trong `AboutFounder`, `Features`, `Testimonials`, `LearningPath`, `PhysicsEverywhere` — đều render trên `/`) | **Có** | **Crash toàn trang**: màn hình "This page couldn't load", console `Uncaught ChunkLoadError: Failed to load chunk ... from module 69790` — KHÔNG bị `RevealErrorBoundary` bắt |

Tái hiện 2 lần (kể cả trên tab hoàn toàn mới, xoá đúng 1 file duy nhất mỗi lần) — đối chứng bằng
việc phục hồi file thì trang tải lại bình thường (đã xác nhận, ảnh chụp có sẵn). Đây là bằng
chứng **ngược lại** báo cáo của Agent A ("ErrorBoundary hoạt động đúng, không kẹt opacity:0") —
đọc `components/ui/Reveal.tsx` thì logic `RevealErrorBoundary` (class component với
`getDerivedStateFromError`) bọc đúng quanh `<Suspense><RevealMotion>` nên **về lý thuyết** phải
bắt được, nhưng thực nghiệm cho thấy lỗi tải chunk của chính `RevealMotion` (component được
`Suspense`/boundary đó trực tiếp bảo vệ) lại thoát ra ngoài thành uncaught — nghi vấn liên quan đến
thời điểm lỗi xảy ra trong lúc hydrate (Next static export + `React.lazy` trong SSR/hydration có
thể có cách xử lý lỗi khác với client-side thuần), cần thầy hoặc Agent A xem lại, **chưa xác định
được nguyên nhân gốc trong phạm vi đợt kiểm này**. Rủi ro thực tế: nếu CDN/hosting rớt đúng 1 file
JS này (mất mạng, cache lỗi, deploy dở dang), học sinh vào trang chủ sẽ thấy màn hình trắng lỗi
thay vì nội dung — mức độ nghiêm trọng cao vì đây là trang chủ công khai.

Ghi chú phụ: 2 chunk ~139 KB này là **2 bản đóng gói framer-motion riêng biệt** (không dùng chung
vendor chunk) — không phải nguyên nhân của phần "dư" ở §3 (không nằm trong JS ban đầu 2 trang mục
tiêu), nhưng là lãng phí ~139 KB có thể gộp lại nếu cả `Reveal` và `QuestionSlide` dùng chung 1
chunk framer-motion.

## 7. Trang công khai không tải GoTrue

Xác nhận qua Browser pane (`read_network_requests`, lọc `chunks`):
- `/` — danh sách chunk tải KHÔNG có `2zlcdknyjvmj1.js` (211 KB, supabase-js+GoTrue). Đúng yêu
  cầu.
- `/tin-tuc/` — **CÓ** tải `2zlcdknyjvmj1.js`. Không có lỗi console (`read_console_messages
  onlyErrors` → rỗng) dù chưa đăng nhập — `useAuth()` rơi về guest mặc định, không throw.

Rà tĩnh toàn bộ 66 trang (đối chiếu chunk supabase với danh sách trang): đúng **12/66** trang
không tải chunk này — `/`, `/404`, `/_not-found`, `/blog`, 6 bài `/blog/...`, `/khoa-hoc`,
`/tro-giang/mau`. Tất cả đều nằm trong `app/(public)/layout.tsx` (dùng `PublicShell`, không
`AuthProvider`) hoặc không có layout riêng (kế thừa root, cũng không có Provider) — không có trang
cần-đăng-nhập nào bị lọt vào nhóm này.

**Nhận xét về quyết định giữ AuthProvider ở `/tin-tuc`:** hợp lý — trang này lọc bài theo lớp học
sinh đã đăng nhập (đúng như Agent B giải thích), bỏ AuthProvider sẽ làm học sinh đã đăng nhập thấy
sai nội dung hoặc Navbar rơi về trạng thái khách. Đánh đổi là `/tin-tuc` vẫn tải 211 KB GoTrue dù
là trang có thể xem công khai — nhưng đây là trang phụ (không phải trang chủ), tần suất truy cập
ẩn danh thấp hơn `/`, nên đánh đổi chấp nhận được. Không phải lỗ hổng bảo mật (không dữ liệu nhạy
cảm bị lộ), chỉ là đánh đổi hiệu năng có chủ đích và ghi chú rõ trong code.

## 8. Hồi quy — không có tài khoản test, kiểm tĩnh toàn bộ layout

`grep -rn "test.*@|TEST_STUDENT|TEST_TEACHER" .env.local scripts/ docs/` → không tìm thấy tài
khoản test nào; `.env.local` không tồn tại trong worktree này (đúng chủ ý an toàn). Theo đúng chỉ
dẫn, **không** tự tạo tài khoản Supabase production, **không** dùng thông tin đăng nhập thật.

Rà toàn bộ 22 `layout.tsx` dưới `app/`:
- 14 layout nhóm route cần đăng nhập import `AuthedShell` trực tiếp (`auth`, `bao-loi-cua-toi`,
  `dang-ky`, `dang-nhap`, `dashboard-thpt`, `dashboard`, `khoa-hoc/dang-ky`, `kiem-tra`,
  `loi-moi`, `lop-hoc`, `phu-huynh`, `quan-tri`, `quen-mat-khau`, `tai-khoan`, `thong-bao`,
  `tin-nhan`, `tin-tuc`, `tro-giang`) — mỗi route chỉ có **đúng 1** `AuthedShell` tổ tiên, không
  trang nào thiếu.
- 3 layout con dưới `app/quan-tri/(cttc|shared|thpt)/` dùng `RequireAuth` (gọi `useAuth()` từ
  context đã có sẵn từ `AuthedShell` ở `app/quan-tri/layout.tsx` cha) — **không** bọc thêm
  `AuthProvider`, nên không có nguy cơ khởi tạo 2 Supabase client chồng nhau.
- `app/(public)/layout.tsx` dùng `PublicShell` (không `AuthProvider`) cho `/blog`, `/khoa-hoc`.
- `components/auth/auth-context.tsx`: `useAuth()` có giá trị mặc định "khách" (session/profile
  null) khi gọi ngoài Provider — xác nhận (đọc code) rằng route công khai gọi `useAuth()` (ví dụ
  trong `PreviewAsStudentToggle`, `BugReportWidget` dùng chung ở cả `AuthedShell`/`PublicShell`)
  **không throw**, khớp với việc `/` và `/tin-tuc` không có lỗi console khi kiểm bằng trình duyệt.

Không phát hiện route nào bị thiếu `AuthedShell`/`AuthProvider`, không phát hiện lồng đôi. Đây là
kiểm tĩnh — **chưa test được luồng thật** (đăng nhập, làm đề, gradebook, `/tro-giang/phu-dao`,
Rank, `/quan-tri/chu-de`, CNC) vì không có tài khoản test hợp lệ trong phiên này.

## 9. Migration SQL

`git diff perf2/baseline..HEAD --stat -- supabase/migrations/ perf/rollback/` → rỗng.
**Không có migration mới trong đợt này** — khớp dự đoán (cả 3 nhánh A/B/C đều thuần
frontend/hosting).

## 10. Việc còn lại / rủi ro

1. **Ưu tiên cao**: tìm nguyên nhân gốc vì sao `RevealErrorBoundary` không bắt được lỗi tải chunk
   của chính `RevealMotion` (§6) — rủi ro màn trắng toàn trang chủ nếu CDN/hosting phục vụ thiếu 1
   file JS.
2. `/lop-hoc/bai` (1039 KB) và `/kiem-tra/lam` (1023 KB) còn dư 20–40 KB so với mục tiêu <1000 KB
   — cơ hội rõ nhất là tách nhỏ thêm `1r7v9gh512xhf.js` (71 KB) / `3jskf4bfpzjey.js` (94 KB).
3. Gộp 2 bản đóng gói framer-motion riêng (`RevealMotion` + `QuestionSlideMotion`, ~139 KB mỗi
   bản) thành 1 chunk dùng chung — tiết kiệm ~139 KB tổng dung lượng build (không ảnh hưởng 2
   trang mục tiêu vì cả hai đều lazy, nhưng giảm băng thông CDN tổng thể).
4. Lighthouse 4 trang nên đo lại trên máy thật (không phải sandbox dùng chung) để có số đối chiếu
   đáng tin với BASELINE2 — xem lưu ý môi trường ở §2.
5. Chưa test hồi quy bằng tài khoản thật (đăng nhập, làm đề, gradebook, phụ đạo, Rank, CNC, trang
   quản trị) — cần thầy tự kiểm hoặc cấp tài khoản test khi rảnh.
6. `.htaccess` (nhánh C/`hosting`) đọc thấy trong `scripts/deploy.sh` có cấu hình cache hợp lý
   (1 năm cho asset hash, 30 ngày mặc định, 10 phút cho `/data`) nhưng **chưa kiểm được trên
   hosting thật** (giống hạn chế đã ghi trong BASELINE2 mục 6) — cần đo sau khi deploy thật.

Không có migration nào cần thầy chạy tay ở đợt này (mục 9).
