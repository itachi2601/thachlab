# Prompt Claude Code — Tốc độ tải + chạy được trên điện thoại cũ

> Chạy tại thư mục gốc repo ThachLab. Đọc `docs/STATE.md` trước.

---

Bạn là orchestrator. Đợt này có 2 mục tiêu: (A) giảm JS trên 2 trang học sinh dùng nhiều nhất,
(B) làm web hiển thị và chạy được trên điện thoại Android/iPhone đời cũ. 3 agent song song,
mỗi agent một **git worktree** (`isolation: "worktree"`), nhánh `perf2/<tên>`. Cuối cùng 1 agent kiểm tra.

## Luật chung
- Chỉ sửa trong vùng được giao. Cần sửa ngoài vùng thì ghi vào báo cáo.
- **Không đổi giao diện trên máy hiện đại.** Mọi thay đổi chỉ được thêm đường lùi cho máy cũ,
  không được làm máy mới xấu đi. Agent C phải chụp ảnh trước/sau ở viewport 390px để chứng minh.
- Không đổi logic nghiệp vụ. Không `select('*')`, không truy vấn nối tiếp mới.
- Migration (nếu có): chỉ viết file, theo quy tắc ở `AGENTS.md`. Không chạy lên production.
- `npm run build` và `npx tsc --noEmit` phải qua trước khi báo xong.
- Commit nhỏ, message tiếng Việt. Báo cáo cuối: file đã sửa, số liệu trước/sau, rủi ro, việc còn lại.

## Pha 0 — Orchestrator khảo sát (tuần tự, ngắn)
Ghi `perf2/BASELINE2.md`:
1. **Máy thật học sinh đang dùng.** Tìm trong `docs/ANALYTICS-SETUP.md` và dữ liệu analytics/Supabase
   xem có thu user-agent không. Có thì thống kê: top 10 thiết bị, top 10 phiên bản trình duyệt,
   tỉ lệ iOS < 16 và Android WebView/Chrome < 90. **Không có dữ liệu thì ghi rõ "không đo được"
   và hỏi Thạch** — đừng đoán; toàn bộ quyết định ở Agent C phụ thuộc con số này.
2. Build sạch, ghi JS ban đầu của `/lop-hoc/bai/` và `/kiem-tra/lam/` (hiện ~1,4 MB mỗi trang),
   và 10 chunk lớn nhất (dùng lại `perf/chunks-report.mjs`).
3. Liệt kê cú pháp/API trong `out/_next/static/chunks/*.js` mà máy cũ không có
   (`.at(`, `replaceAll`, `flatMap`, `Object.hasOwn`, optional chaining, `??=`).
4. Liệt kê tính năng CSS trong `out/_next/static/chunks/*.css` cần Safari mới:
   `@property`, `color-mix(`, `:has(`, `@supports (-moz-orient:inline)`, `clamp(`, `inset:`.

**Mâu thuẫn đã biết, phải xử lý:** `package.json` khai `browserslist: ["ios_saf >= 12","safari >= 12","chrome >= 70"]`,
nhưng Tailwind v4 đang xuất `@property`, `color-mix()`, `:has()` — những thứ này cần Safari 16.4+.
Nghĩa là **khai báo và thực tế đang lệch nhau**; trên iPhone iOS 12–15 rất có thể màu sắc, khoảng cách,
trạng thái hover/checked bị sai. Agent C xử lý phần này.

---

## Agent A — `perf2/split-katex` · Tách KaTeX và framer-motion
Vùng: `components/lessons/*`, `components/exam/*`, `components/ui/Reveal.tsx`, chỗ import KaTeX/framer.
1. KaTeX (290 KB) và framer-motion (139 KB) hiện nằm trong JS ban đầu của `/lop-hoc/bai/` và `/kiem-tra/lam/`.
   Chuyển sang `next/dynamic`, chỉ tải khi thật sự cần:
   - KaTeX: chỉ tải khi nội dung có công thức (dò `$` hoặc `\(` trong HTML trước khi import).
     Chưa tải xong thì hiện nguyên văn LaTeX trong `<code>`, không hiện skeleton trống.
   - framer-motion: thay các animation đơn giản bằng CSS transition; chỉ giữ framer ở chỗ thật sự cần.
2. Ở `/lop-hoc/*`, KaTeX hiện tải ngay sau hydrate — đổi thành chỉ tải khi accordion được mở.
3. Thêm **error boundary** cho `components/ui/Reveal.tsx`: chunk `RevealMotion` tải hỏng thì nội dung
   phải hiện ở trạng thái cuối (opacity 1), không được kẹt `opacity:0` vĩnh viễn.
4. Đích: JS ban đầu 2 trang đó xuống **dưới 1,0 MB**. Ghi số đo trước/sau.

## Agent B — `perf2/hosting` · Cache, ảnh, dọn phụ thuộc
Vùng: `scripts/deploy.sh`, `next.config.ts`, `package.json`, `scripts/optimize-storage-images.mjs`.
1. `.htaccess` sinh trong `deploy.sh` hiện chỉ cache js/css/woff2 1 năm. Thêm cache 30 ngày cho
   `png|jpe?g|webp|svg|gif`, và bật `mod_deflate`/`mod_brotli` cho html/css/js/json/svg nếu LiteSpeed cho phép.
   Ghi rõ trong `README` rằng sửa ảnh thì phải đổi tên file.
2. Chạy `scripts/optimize-storage-images.mjs` ở chế độ dry-run, xuất danh sách ảnh > 150 KB trong
   bucket `lesson-media` kèm kích thước, **không upload**. GIF nặng thì đề xuất đổi sang WebP/video.
3. Đặt `turbopack.root` trong `next.config.ts` để tắt cảnh báo đoán nhầm workspace root.
4. `npm uninstall @xmldom/xmldom` và xoá `services/excel-export.ts` (không file nào import — xác minh lại bằng grep trước khi xoá).
5. `heic2any` (1320 KB) chỉ dùng ở đâu? Nếu chỉ dùng cho ảnh điểm danh phía GV thì xác nhận nó đã lazy
   và không nằm trong bất kỳ chunk nào của trang học sinh.

## Agent C — `perf2/may-cu` · Chạy được trên điện thoại đời cũ
Vùng: `app/globals.css` (hoặc file Tailwind gốc), `postcss.config.mjs`, `package.json` (browserslist),
`app/layout.tsx`, component mới `components/ui/BrowserNotice.tsx`.

**Trước khi sửa, phải chốt mốc hỗ trợ với Thạch** dựa trên số liệu Pha 0. Nếu Pha 0 không có dữ liệu,
dùng mặc định: **iOS Safari 15+, Chrome/Android 90+, và không vỡ (chỉ xấu hơn) trên iOS 12–14.**

1. **CSS** — đây là rủi ro lớn nhất:
   - Thêm `@csstools/postcss-global-data` + `postcss-preset-env` (hoặc `lightningcss` với target theo
     browserslist) vào `postcss.config.mjs` để hạ cấp `@property`, `color-mix()`, `inset:`, `clamp()`.
   - `:has()` không hạ cấp được. Tìm mọi chỗ dùng `:has()` và viết lại bằng class có điều kiện trong
     React, hoặc bọc trong `@supports selector(:has(*))` kèm đường lùi.
   - Kiểm tra `gap` trong flexbox: iOS Safari < 14.1 không hỗ trợ. Chỗ nào dựa vào nó để bố cục
     không vỡ thì thêm `margin` dự phòng.
   - Kiểm tra `position: sticky`, `backdrop-filter`, `aspect-ratio`, `100dvh` — đều có vấn đề trên iOS cũ.
2. **JavaScript**:
   - Đặt lại `browserslist` cho khớp mốc đã chốt, và xác minh output thật sự khớp
     (grep lại `out/**/*.js` cho `.at(`, `replaceAll`, `Object.hasOwn`, `flatMap`).
   - Còn API nào thiếu thì thêm polyfill **có điều kiện**, tải qua `<script nomodule>` hoặc
     kiểm tra tính năng rồi mới import động — tuyệt đối không nhồi polyfill vào bundle của máy mới.
3. **Bộ nhớ và CPU máy yếu**:
   - Mô phỏng con lắc SVG ở trang chủ chạy `requestAnimationFrame` liên tục. Thêm: dừng khi
     `document.hidden`, dừng khi ra khỏi viewport, và tắt hẳn khi `navigator.hardwareConcurrency <= 2`
     hoặc `prefers-reduced-motion` — thay bằng ảnh tĩnh.
   - Kiểm tra các trang danh sách dài (ngân hàng câu hỏi, gradebook) có render hàng nghìn DOM node không.
4. **Thông báo trình duyệt quá cũ**: `components/ui/BrowserNotice.tsx` — kiểm tra một tính năng mốc
   (ví dụ `CSS.supports('color-mix(in srgb, red, blue)')`). Không đạt thì hiện một dải nhỏ trên cùng:
   "Trình duyệt của em hơi cũ nên trang có thể hiển thị chưa đúng. Em thử cập nhật hoặc mở bằng Chrome."
   Chỉ là dải thông báo, **không chặn học sinh dùng web**. Cho phép tắt và nhớ trong `localStorage`.
5. Tự kiểm bằng browser pane ở các viewport 320 / 360 / 390 px và ở chế độ giả lập thiết bị chậm
   (CPU throttle 4×). Chụp ảnh trang chủ, một bài học, một trang làm đề — trước và sau.

---

## Merge (orchestrator)
Thứ tự: **B → A → C**. Sau mỗi lần merge thì build lại.

## Agent D — Kiểm tra độc lập
Bắt buộc đầu phiên: `git merge-base --is-ancestor <sha giao việc> HEAD` để chắc chắn đang kiểm đúng code mới.
- Build sạch, `tsc` qua, lint không tăng lỗi.
- Lighthouse **preset mobile** (không phải desktop như đợt trước) cho `/`, `/lop-hoc/bai/?id=49`,
  `/kiem-tra/lam/?id=118`. So với `perf2/BASELINE2.md`.
- Xác minh JS ban đầu 2 trang học sinh đã dưới 1,0 MB.
- Grep lại `out/**/*.css` và `out/**/*.js`: không còn tính năng vượt mốc đã chốt.
- KaTeX: bài có công thức phải hiện đúng; bài không có công thức phải **không** tải chunk KaTeX.
- Reveal: giả lập chunk lỗi (chặn request trong devtools) — nội dung vẫn phải hiện.
- Mô phỏng con lắc: chuyển tab đi thì rAF phải dừng.
- Hồi quy: làm đề, gradebook, phụ đạo, Rank, `/quan-tri/chu-de`, một trang CNC.
- Ghi `perf2/RESULT.md`: số đo trước/sau, mốc trình duyệt đã chốt, việc còn lại, và
  (theo `AGENTS.md`) lệnh cho Thạch chạy nếu có migration chờ.
