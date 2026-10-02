# Chuẩn giao diện — khả năng đọc & tương phản

Chốt 02/10/2026 sau đợt rà WCAG (xem memory `project_thachlab_kha_nang_doc`). Mọi trang/khối mới
phải theo bảng này; kiểm bằng `npm run check:a11y` trước khi báo xong (đo tương phản token + bắt
chữ nhỏ hơn sàn). Đổi màu token thì **đo lại** bằng `node scripts/check-a11y.mjs '#chữ' '#nền'`,
không ước lượng bằng mắt.

## 1. Ngưỡng bắt buộc (WCAG 2.1 AA)

| Loại | Tỉ lệ tối thiểu | Ghi chú |
|---|---|---|
| Chữ thường (< 18,66px đậm hoặc < 24px thường) | **4,5:1** | Nút 14px đậm vẫn là chữ thường |
| Chữ lớn, icon có nghĩa, viền ô nhập, vòng focus | 3:1 | |
| Chữ trạng thái vô hiệu (disabled), trang trí | không bắt buộc | Đừng dùng tông này cho chữ thật |
| Chữ đọc lâu (bài học, đề, kết quả cho phụ huynh) | nên ≥ 7:1 (AAA) | Hiện đạt 12–18:1 |

## 2. Token màu và số đo thật

Nguồn: `app/globals.css` (`@theme` + khối `html[data-theme="light"]` + khối "P1/P2 kha-nang-doc").

| Token / class | Tối (trên `#05070b` / panel `#0b1020`) | Sáng (trên `#f8fafc` / trắng) |
|---|---|---|
| `--color-ink` chữ thân | `#f1f5f9` — 18,4 | `#0f172a` — 17,9 |
| `--color-muted` chữ phụ | `#94a3b8` — 7,4 | `#475569` — 7,6 |
| `text-slate-500` | ⚠ `#62748e` (Tailwind v4) — 3,97 trên panel, chỉ dùng cho disabled/icon | `#64748b` — 4,8 (override sẵn) |
| `text-slate-400` | `#90a1b9` — 7,2 | `#475569` — 7,6 (override sẵn) |
| `--color-cyan` / `text-cyan-*` | `#22d3ee` — 11,2 | ép `#0e7490` — 5,4 |
| `--color-accent` vàng / `text-amber-*` | `#facc15` — 13,2 | ép `#a16207` — 4,9 |
| `text-emerald-*` / `text-red-*` / `text-violet-*` | tông 300–400 | ép `#047857` 5,5 / `#b91c1c` 6,5 / `#6d28d9` 7,1 |
| `.text-gradient` (nhấn tiêu đề) | `--accent-brand-text: #60a5fa` — 7,9 | `#1d4ed8` — 6,4 |
| `.text-gradient--warm`, `.cnc-header-grid h1 em` | `--accent-warm-text: #fb923c` — 8,9 | `#c2410c` — 5,2 |
| Dịu mắt (`html.is-dim`, `.lesson-page.is-dim`) | nền kem `#f5efe0`, chữ `#33291a` — 12,4, phụ `#6b5a3e` — 5,8 | |
| Nút đặc `bg-primary` + chữ trắng | xem đợt P0 (token `--color-primary`) — phải ≥ 4,5 | |

Quy tắc kèm theo:
- **Không dùng chữ gradient** (`background-clip: text; color: transparent`): không có giá trị tương phản
  xác định, mất chữ ở `forced-colors`. Dùng `.text-gradient`/`.text-gradient--warm` (nay là màu đặc) hoặc
  `text-cyan-300`.
- Màu cần **hai giá trị theo theme** (tối cần tông sáng, sáng cần tông đậm) — không dùng chung một mã
  cho cả hai (bài học violet `#8b5cf6`: 4,5 tối / 4,2 sáng, trượt cả hai).
- Tailwind **v4**: màu `slate-500` là `oklch(55.4% …)` ≈ `#62748e`, không phải `#64748b` của v3. Đo theo
  `node_modules/tailwindcss/theme.css`.
- Chữ xanh nhỏ trên nền đen là tổ hợp tệ nhất cho người 45+ (thủy tinh thể ngả vàng giảm truyền bước
  sóng ngắn). Trang cho phụ huynh mặc định theme **sáng** (`app/layout.tsx` script inline + `ReadingZone`).

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
4. Chụp thử 375px, cả theme sáng và tối (memory `feedback_mobile_first_ui`).
