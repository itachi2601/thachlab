# Chuẩn giao diện — khả năng đọc & tương phản

Chốt 02/10/2026 sau đợt rà WCAG (xem memory `project_thachlab_kha_nang_doc`); **cập nhật 11/10/2026
khi đảo sang nền sáng làm mặc định** (bảng màu đầy đủ + bảng quy đổi idiom: `docs/MAU-NEN-SANG.md`).
Mọi trang/khối mới phải theo bảng này; kiểm bằng `npm run check:a11y` trước khi báo xong (đo tương
phản token + bắt chữ nhỏ hơn sàn). Đổi màu token thì **đo lại** bằng
`node scripts/check-a11y.mjs '#chữ' '#nền'`, không ước lượng bằng mắt.

## 1. Ngưỡng bắt buộc (WCAG 2.1 AA)

| Loại | Tỉ lệ tối thiểu | Ghi chú |
|---|---|---|
| Chữ thường (< 18,66px đậm hoặc < 24px thường) | **4,5:1** | Nút 14px đậm vẫn là chữ thường |
| Chữ lớn, icon có nghĩa, viền ô nhập, vòng focus | 3:1 | viền ô nhập ở nền sáng: `--color-line-strong` `#8b93a1` = 3,2:1 |
| Chữ trạng thái vô hiệu (disabled), trang trí | không bắt buộc | Đừng dùng tông này cho chữ thật |
| Chữ đọc lâu (bài học, đề, kết quả cho phụ huynh) | nên ≥ 7:1 (AAA) | nền sáng đạt 16,6:1 (chữ thân) / 7,6:1 (chữ phụ); khối phụ huynh đạt 8,9:1 |
| Khối phụ huynh 45–60 | **7:1 (AAA)** cho mọi câu cần đọc | P2 — `#3d4653` trên `#f7f7f4` = 8,9:1 |

## 2. Token màu và số đo thật

Nguồn: `app/globals.css` — khối `@theme` là **nền sáng (mặc định)**, khối `html[data-theme="dark"]`
là nền tối (tuỳ chọn). Đo bằng `npm run check:a11y`.

| Token / class | Sáng — mặc định (trên `#f5f7fa` / trắng) | Tối — tuỳ chọn (trên `#05070b` / panel `#0b1020`) |
|---|---|---|
| `--color-ink` chữ thân | `#0f172a` — 16,6 / 17,9 | `#f1f5f9` — 18,4 |
| `--color-muted` chữ phụ | `#475569` — 7,1 / 7,6 | `#94a3b8` — 7,4 |
| `text-slate-500` | `#64748b` — 4,76 (dùng cho mốc thời gian/placeholder) | ⚠ `#7c8ba1` (override) — 5,47; gốc Tailwind v4 `#62748e` chỉ 3,97 nên **không** dùng cho câu cần đọc |
| `--color-primary` (nền nút đặc + chữ trắng) | `#1d4ed8` — 6,7 | `#2563eb` — 5,17 |
| `--color-primary` (chữ/viền trên nền trang) | `#1d4ed8` — 6,24 | `#60a5fa` (override `[class*="text-primary"]`) — 7,93 |
| `--color-line-strong` (viền ô nhập) | `#8b93a1` — 3,2 (đạt 1.4.11) | `rgba(255,255,255,.16)` → `#cbd5e1` — 12,8 |
| `--color-ok` / `--color-warn` / `--color-danger` | `#047857` 5,5 / `#b45309` 5,0 / `#b91c1c` 6,5 | `#34d399` / `#fbbf24` / `#f87171` |
| `--color-cyan`, `--color-violet`, `--color-accent` | `#0e7490` — 5,4 · `#6d28d9` — 7,1 · `#b45309` — 5,0 | `#22d3ee` — 11,2 · `#8b5cf6` · `#facc15` — 13,2 |
| `.text-gradient` (nhấn tiêu đề) | `#1d4ed8` — 6,24 | `--accent-brand-text: #60a5fa` — 7,9 |
| `.text-gradient--warm`, `.cnc-header-grid h1 em` | `#c2410c` — 5,2 | `--accent-warm-text: #fb923c` — 8,9 |
| Khối phụ huynh (`.parent-page`) | nền `#f7f7f4`; chữ `#14181f` 16,6 · phụ `#3d4653` 8,9 · nhấn navy `#1e40af` 8,1 (nút: 8,7 với chữ trắng) | giữ token chung, chữ phụ `#b8c4d6` |
| Dịu mắt (`html.is-dim`, `.lesson-page.is-dim`) | nền kem `#f5efe0`, chữ `#33291a` — 12,4, phụ `#6b5a3e` — 5,8 | — |

Quy tắc kèm theo:
- **Nền sáng là mặc định** (M1, P5). Nền tối chỉ bật khi người dùng đã tự chọn — không theo
  `prefers-color-scheme`, để màu kiểm soát được. Chi tiết + bảng quy đổi idiom: `docs/MAU-NEN-SANG.md`.
- **Không dùng chữ gradient** (`background-clip: text; color: transparent`): không có giá trị tương phản
  xác định, mất chữ ở `forced-colors`. Dùng `.text-gradient`/`.text-gradient--warm` (nay là màu đặc) hoặc
  `text-primary`.
- Màu cần **hai giá trị theo theme** (tối cần tông sáng, sáng cần tông đậm) — không dùng chung một mã
  cho cả hai (bài học violet `#8b5cf6`: 4,5 tối / 4,2 sáng, trượt cả hai).
- Tailwind **v4**: màu `slate-500` là `oklch(55.4% …)` ≈ `#62748e`, không phải `#64748b` của v3. Đo theo
  `node_modules/tailwindcss/theme.css`.
- Chữ xanh nhỏ trên nền đen là tổ hợp tệ nhất cho người 45+ (thủy tinh thể ngả vàng giảm truyền bước
  sóng ngắn) — nay cả site mặc định sáng nên vấn đề này chỉ còn ở theme tối tuỳ chọn.


## 3. Sàn cỡ chữ

| Loại chữ | Tối thiểu | Ghi chú |
|---|---|---|
| Nhãn, chip, số đếm, chú thích, mono eyebrow | **12px** (`text-[12px]`/`text-xs`) | Script chặn mọi `text-[<12px]` và `font-size: <12px` |
| Chữ đọc được (dòng phụ, mô tả, ô nhập) | 14px (`text-sm`) | Ô nhập trên iOS phải ≥ 16px để không tự zoom |
| Chữ thân bài học / đề | 16px, line-height 1,65–1,75 | `.lesson-prose`, `.exam-content` |
| Điều hướng chính (thanh đáy mobile, tab) | ≥ 12px đậm | `.mobile-tabbar a` = 12px |
| IN HOA + giãn chữ | ≥ 13px, `letter-spacing ≤ .08em` | Viết hoa làm mất hình dạng từ; eyebrow CNC = 13px/.08em |

Ngoại lệ duy nhất: `components/tro-giang/local-preview.css` (xem thử cục bộ, không lên web).

## 4. Công cụ đọc cho người dùng

- `A− / A / A+` (0,94 / 1 / 1,08) và **Dịu mắt** (nền kem, chữ nâu) có ở: trang bài học
  (`app/lop-hoc/bai/page.tsx`, phóng khối nội dung bằng `--lesson-read-scale`), `/phu-huynh` và
  `/kiem-tra/lam` (`components/ui/ReadingZone.tsx`, phóng `font-size` của `<html>` nên mọi chữ rem to
  theo; Dịu mắt = theme sáng + `html.is-dim`). Cùng khoá `localStorage` (`thachlab-read-font`,
  `thachlab-read-dim`) để chỉnh một lần dùng mọi nơi.
- Trang mới có nội dung đọc lâu → bọc bằng `<ReadingZone>`; không tự viết bộ nút mới.
- Tôn trọng `prefers-reduced-motion` (đã có 6 khối), `prefers-contrast: more` (chữ phụ/viền đậm hơn,
  khối cuối `globals.css`), `forced-colors` (chữ nhấn về `CanvasText`).

## 5. Checklist trước khi báo xong một trang/khối mới

1. `npm run check:a11y` đạt.
2. Chữ thật không dùng `text-slate-500` ở theme tối (dùng `text-slate-400`/`text-muted`).
3. Màu mới có hai giá trị theme và số đo ghi trong comment cạnh token.
4. Chụp thử 375px, cả theme sáng và tối (memory `feedback_mobile_first_ui`) **bằng device
   emulation**, không bằng `chrome --screenshot --window-size=375,812`:
   ```bash
   node scripts/do-bo-cuc.mjs http://localhost:3001/lop-hoc --rong=375 --cao=812 \
     --theme=light --anh=/tmp/lop-hoc-375.png
   ```
   Công cụ in `scrollWidth` và danh sách phần tử tràn **thật** (đã loại phần tử bị cha cắt như
   marquee). `--theme=dark` để chụp nền tối. Vì sao không dùng `--window-size`: cửa sổ 375px vẫn
   cho layout viewport ~500px rồi cắt ảnh — ảnh trông như trang tràn ngang trong khi trang không
   tràn (đã mất thời gian vì lỗi giả này, xem `docs/MAU-NEN-SANG.md` §8).
5. Đổi bảng màu → xem thêm `/dev/giao-dien` và `docs/MAU-NEN-SANG.md`.

