# Prompt Claude Code — Giảm font trên đường tải trang (đợt tốc độ 3)

> Chạy tại thư mục gốc repo ThachLab. Đọc `docs/STATE.md` trước.
> Đợt này nhỏ và tập trung: chỉ xử lý font. Không đụng việc khác.

---

## Bối cảnh — số đo thật trên thachlab.id.vn (26/9/2026, đo bằng Chrome trên site production)

PageSpeed: desktop 100, **mobile 74**. CrUX field (người dùng thật, 28 ngày): **LCP 2,7s — Core Web
Vitals Failed** (ngưỡng đạt là 2,5s, tức chỉ thiếu 0,2s). Lighthouse lab mobile (Moto G Power,
Slow 4G): **LCP 5,5s**, FCP 2,4s, **TBT chỉ 40ms**.

TBT thấp mà LCP cao ⇒ **nghẽn ở mạng, không phải ở CPU.**

Tài nguyên trang chủ, đo bằng `performance.getEntriesByType('resource')`:

| Loại | Số file | Dung lượng gốc | Thực tế qua mạng |
|---|---|---|---|
| **Font** | **20** | 323 KB | **~323 KB** |
| JS | 13 | 856 KB | ~250 KB (brotli) |
| CSS | 2 | 280 KB | ~45 KB (brotli) |

Brotli đã bật trên hosting và chạy đúng (đã xác nhận `content-encoding: br`). Nhưng **woff2 vốn đã
nén sẵn nên brotli không giúp gì** — 323 KB font là con số thật đi qua mạng, và nay là thứ nặng
nhất trên trang chủ.

Nặng hơn nữa: trong log mạng, **15 file font nằm ở request #2–#16, hai file CSS mãi #17–#18**.
`next/font` preload chúng ở mức ưu tiên cao nhất, nên trên mạng chậm font giành băng thông của
chính CSS — thứ quyết định thời điểm vẽ trang đầu tiên.

Nguồn: `app/fonts.ts` nạp **5 họ font ở layout gốc** với 11 độ đậm, mỗi độ đậm lại tách nhiều file
theo bảng mã (vietnamese / latin / latin-ext) → 20 file, preload trên **mọi** trang.

Khảo sát sẵn (đã grep, khỏi làm lại):
- **Cinzel** và **Playfair Display**: chỉ dùng ở `components/rank/TierName.tsx` và
  `components/rank/TierLadder.tsx`. Hai file. Trang chủ không cần.
- **JetBrains Mono** (`font-mono`): dùng ở 61 file khắp nơi → giữ ở root, nhưng xử lý riêng (xem dưới).

## Mục tiêu
**Font trên trang chủ: 20 file / 323 KB → dưới 10 file / dưới 170 KB.** Giao diện không được đổi.

## Luật
- **Không đổi giao diện.** Chữ phải hiện đúng font, đúng độ đậm như hiện tại ở mọi trang.
  Bắt buộc chụp ảnh trước/sau ở viewport 390px cho: trang chủ, một bài học, trang Xếp hạng
  (`/lop-hoc/xep-hang`), một trang có công thức.
- Không đụng việc ngoài font. Không migration.
- `npm run build` và `npx tsc --noEmit` phải qua; lint không tăng lỗi.
- Commit nhỏ, message tiếng Việt dạng `perf(font): ...`.

---

## Việc

### 1. Gỡ Cinzel + Playfair khỏi layout gốc
Hai họ này chỉ phục vụ tên bậc huy hiệu rank. Import `next/font` ngay trong
`components/rank/TierName.tsx` / `TierLadder.tsx` (hoặc một module dùng chung trong
`components/rank/`) và gắn `className` của font lên đúng phần tử ở đó, thay vì để biến CSS ở `<html>`.
Bỏ chúng khỏi `fontClassName`.

Lưu ý: `next/font` preload theo route nơi nó được import. Sau thay đổi, chỉ các trang thật sự
render component rank mới tải 2 họ này. Xác minh bằng cách mở trang chủ và kiểm không còn request
tới file woff2 của Cinzel/Playfair.

### 2. JetBrains Mono — giữ ở root nhưng bỏ preload
61 file dùng `font-mono` nên không tách ra được gọn gàng. Thay vào đó đặt `preload: false` cho họ
này trong `app/fonts.ts`: font vẫn nạp khi cần, nhưng không còn chiếm ưu tiên cao trước lúc vẽ trang.
Chữ mono thường là chi tiết nhỏ, `display: "swap"` đã lo phần hiển thị tạm.

### 3. Cắt subset thừa
Hiện khai `subsets: ["vietnamese", "latin"]` nhưng bản build vẫn sinh cả file `latin-ext`.
Kiểm tra lại: `next/font` tách file theo `unicode-range` của Google, nên có thể không bỏ được
bằng khai báo. Nếu đúng vậy thì ghi vào báo cáo và bỏ qua mục này — **đừng tự chế biến thể tự host
thủ công**, rủi ro cao hơn lợi ích.

### 4. Rà lại độ đậm có thật sự dùng
- Be Vietnam Pro đang nạp 400/600/700/800. Grep `font-semibold`, `font-bold`, `.hub-tile` xem còn
  dùng đủ 4 mức không. Mức nào không còn chỗ nào dùng thì bỏ.
- Inter đang nạp 400/500/600. Tương tự.
- **Chỉ bỏ mức không còn chỗ nào dùng.** Không bỏ mức đang dùng rồi để trình duyệt làm đậm giả —
  đó là đổi giao diện.

### 5. Preload có chọn lọc
Sau 4 bước trên, chỉ nên còn preload các file phục vụ chữ ở **màn hình đầu trang chủ**: Be Vietnam
Pro (tiêu đề) và Inter (chữ thân) ở độ đậm dùng trong hero, subset vietnamese + latin. Phần còn lại
để `preload: false`.

---

## Kiểm tra cuối (agent riêng, không tham gia các bước trên)
- Build sạch, `tsc` qua, lint không tăng lỗi.
- Serve `out/` rồi mở bằng browser pane, chạy đoạn này trên trang chủ và ghi kết quả vào báo cáo:
  ```js
  performance.getEntriesByType('resource')
    .filter(e => /\.woff2/.test(e.name))
    .map(e => ({ f: e.name.split('/').pop(), KB: Math.round(e.decodedBodySize/1024) }))
  ```
  Đích: **dưới 10 file, tổng dưới 170 KB.**
- Xác minh trang chủ **không** còn tải woff2 của Cinzel/Playfair; trang `/lop-hoc/xep-hang` **có**
  tải và tên bậc hiển thị đúng hai kiểu chữ như cũ.
- So ảnh chụp trước/sau ở 390px cho 4 trang đã nêu — không được khác nhau.
- Lighthouse preset mobile cho `/` và `/lop-hoc/bai/?id=49`, ghi LCP/FCP trước và sau.
- Ghi `perf3/RESULT.md`.

## Sau khi merge
Nhắc Thạch chạy `scripts/deploy.sh` rồi đo lại PageSpeed trên site thật. CrUX field cần vài ngày
mới cập nhật, nên dùng số Lighthouse lab để đối chiếu ngay.
