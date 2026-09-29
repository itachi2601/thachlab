# Prompt Claude Code — Đợt tối ưu tốc độ lần 2

> Chạy tại thư mục gốc repo ThachLab. Đọc `docs/STATE.md` và `perf/RESULT.md` §9 trước.
> Bỏ hoàn toàn phần hỗ trợ điện thoại đời cũ — đợt này chỉ làm tốc độ.

---

Bạn là orchestrator. 3 agent song song, mỗi agent một **git worktree** (`isolation: "worktree"`),
nhánh `perf2/<tên>`. Cuối cùng 1 agent kiểm tra độc lập.

## Bối cảnh — đợt trước đã làm gì
Đợt 9/2026 đã xong: nén ảnh (4,6 MB → 0,6 MB), font tự host (bỏ Google Fonts), lazy các thư viện
nặng ở trang GV, lớp nội dung tĩnh `/data/*.json`, index + RPC + RLS (migration còn chờ chạy).
Lighthouse desktop: trang chủ 68 → 91, trang bài 78 → 83.

**Nút thắt còn lại, theo đúng thứ tự tác động:**
1. `/lop-hoc/bai/` và `/kiem-tra/lam/` — hai trang học sinh dùng nhiều nhất — vẫn **~1,4 MB JS
   ban đầu**, gần như không giảm. Thủ phạm: KaTeX 290 KB + framer-motion 139 KB import tĩnh.
2. JS nền dùng chung cả 64 trang: **880 KB raw / 253 KB gzip**, không giảm so với gốc.
   Trong đó supabase-js + GoTrue 211 KB, react-dom 222 KB.
3. Supabase ở **Sydney** — mỗi round-trip từ VN ~100–150 ms. Mọi trang sau đăng nhập đều chịu.
4. Ảnh png/jpg/webp **không có cache header** (`.htaccess` chỉ cache js/css/woff2).

## Luật chung
- Không đổi giao diện, không đổi logic nghiệp vụ. Chỉ tối ưu.
- Chỉ sửa trong vùng được giao. Cần sửa ngoài vùng thì ghi vào báo cáo.
- Migration (nếu có): chỉ viết file, theo quy tắc ở `AGENTS.md`. **Không chạy lên production.**
- `npm run build` và `npx tsc --noEmit` phải qua; lint không tăng lỗi.
- Commit nhỏ, message tiếng Việt dạng `perf(<vùng>): ...`.
- Báo cáo cuối: file đã sửa, số đo trước/sau, rủi ro, việc còn lại.

## Pha 0 — Orchestrator đo mốc (tuần tự, ngắn)
Build sạch rồi ghi `perf2/BASELINE2.md`:
1. JS ban đầu từng trang (dùng lại `perf/chunks-report.mjs`), nêu rõ 2 trang mục tiêu.
2. Thành phần chunk nền 64/64 trang.
3. **Lighthouse preset mobile** (đợt trước đo desktop nên số đẹp hơn thực tế) cho `/`,
   `/lop-hoc/bai/?id=49`, `/kiem-tra/lam/?id=118`, `/lop-hoc/lop-10/`.
4. Thời gian tới byte đầu và tổng thời gian của từng request Supabase trên trang bài, đo
   ở chế độ throttle "Fast 4G".
Commit rồi spawn 3 agent.

---

## Agent A — `perf2/split-js` · Giảm JS hai trang học sinh
Vùng: `components/lessons/*`, `components/exam/*`, `components/ui/Reveal.tsx`, các file import KaTeX/framer.

1. **KaTeX**: chuyển sang `next/dynamic`. Chỉ import khi nội dung thật sự có công thức — dò `$`,
   `\(`, `\[` trong HTML trước. Trong lúc chờ, hiện nguyên văn LaTeX trong `<code>`, không hiện
   skeleton trống (học sinh đọc được ngay, không thấy trang nhảy).
2. **framer-motion**: thay animation đơn giản (fade, slide, stagger) bằng CSS transition thuần.
   Chỉ giữ framer ở chỗ thật sự cần layout animation. Nếu bỏ được hết thì gỡ khỏi `package.json`.
3. Ở `/lop-hoc/*`, KaTeX hiện tải ngay sau hydrate — đổi thành chỉ tải khi accordion được mở.
4. Thêm **error boundary** cho `components/ui/Reveal.tsx`: chunk tải hỏng thì nội dung phải hiện ở
   trạng thái cuối (opacity 1), không kẹt `opacity:0` vĩnh viễn.
5. **Đích: JS ban đầu của `/lop-hoc/bai/` và `/kiem-tra/lam/` xuống dưới 1,0 MB.** Ghi số trước/sau.

## Agent B — `perf2/shell` · Giảm JS nền và số vòng mạng
Vùng: `lib/supabase*`, `services/*`, `app/layout.tsx`, `next.config.ts`, `package.json`.

1. **supabase-js + GoTrue = 211 KB trên mọi trang, kể cả trang khách chưa đăng nhập.**
   - Tìm xem `AuthProvider` có bị import ở layout gốc khiến trang tĩnh (`/`, `/tin-tuc`, `/blog`,
     `/khoa-hoc`) cũng phải tải không. Nếu có, tách: trang công khai không cần GoTrue.
   - Cân nhắc gọi REST của Supabase bằng `fetch` thuần cho các truy vấn đọc đơn giản ở trang công
     khai, thay vì nạp cả SDK. Chỉ làm nếu không phá RLS và không làm code khó đọc — nếu thấy
     không đáng thì ghi lý do vào báo cáo và bỏ qua, đừng cố.
2. **Preconnect**: thêm `<link rel="preconnect">` tới domain Supabase trong `app/layout.tsx` để
   bắt tay TLS chạy song song thay vì chờ. Với Sydney, riêng việc này tiết kiệm ~150–300 ms.
3. **Preload** file `/data/catalog.json` và `/data/lessons/<id>.json` bằng `<link rel="preload">`
   sinh lúc build cho các trang biết trước id.
4. Đặt `turbopack.root` trong `next.config.ts` để tắt cảnh báo đoán nhầm workspace root.
5. Gỡ phụ thuộc chết: `npm uninstall @xmldom/xmldom`, xoá `services/excel-export.ts`
   (xác minh lại bằng grep trước khi xoá).
6. Xác nhận `heic2any` (1320 KB) không nằm trong bất kỳ chunk nào của trang học sinh.

## Agent C — `perf2/hosting` · Cache, nén, ảnh
Vùng: `scripts/deploy.sh`, `scripts/optimize-storage-images.mjs`, `README.md`.

1. `.htaccess` sinh trong `deploy.sh`: thêm cache 30 ngày cho `png|jpe?g|webp|svg|gif`.
   Ghi rõ trong README rằng sửa ảnh thì phải đổi tên file (không có hash trong tên).
2. Bật nén cho html/css/js/json/svg (`mod_brotli` nếu LiteSpeed có, không thì `mod_deflate`).
   JS nền 880 KB raw / 253 KB gzip — nén là khoản lợi lớn nhất trong agent này.
3. Kiểm tra `out/data/.htaccess` (cache 10 phút) vẫn đúng sau thay đổi.
4. Chạy `scripts/optimize-storage-images.mjs` dry-run, xuất danh sách ảnh > 150 KB trong bucket
   `lesson-media` kèm kích thước. **Không upload.** GIF nặng thì đề xuất đổi sang WebP hoặc video.
5. Thêm `fetchpriority="high"` cho ảnh LCP ở trang chủ nếu có, và `decoding="async"` cho phần còn lại.

---

## Merge (orchestrator)
Thứ tự: **C → B → A**. Sau mỗi lần merge thì build lại.

## Agent D — Kiểm tra độc lập
Bắt buộc đầu phiên: `git merge-base --is-ancestor <sha giao việc> HEAD` để chắc chắn đang kiểm đúng code mới.
- Build sạch, `tsc` qua, lint không tăng lỗi.
- **Lighthouse preset mobile** cho 4 trang ở Pha 0, so với `perf2/BASELINE2.md`.
- Xác minh JS ban đầu 2 trang học sinh dưới 1,0 MB, và JS nền đã giảm.
- KaTeX: bài có công thức hiện đúng; bài **không** có công thức phải không tải chunk KaTeX (kiểm bằng tab Network).
- Reveal: chặn chunk trong devtools — nội dung vẫn phải hiện.
- Trang công khai (`/`, `/tin-tuc`): kiểm xem còn tải GoTrue không.
- Hồi quy: đăng nhập HS làm một đề, gradebook, phụ đạo, Rank, `/quan-tri/chu-de`, một trang CNC.
- Ghi `perf2/RESULT.md`: số đo trước/sau, việc còn lại, và (theo `AGENTS.md`) lệnh cho Thạch chạy
  nếu có migration chờ.

## Ngoài phạm vi (chỉ ghi đề xuất, không làm)
- Chuyển Supabase sang Singapore — việc lớn nhất còn lại, cần kế hoạch riêng và thời gian ngừng ngắn.
- Bỏ `output: "export"` để chuyển sang SSR/ISR.
- Hỗ trợ điện thoại đời cũ (`docs/prompt-toc-do-va-may-cu.md`, Agent C) — tạm gác.
