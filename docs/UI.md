# UI — Hệ thiết kế ThachLab

Phong cách **dark "deep space"**: nền tối toàn trang, điểm neon xanh–tím–cyan,
thẻ kính mờ và hiệu ứng phát sáng — hướng thẩm mỹ Gen-Z. Token định nghĩa trong
`app/globals.css` (`@theme` của Tailwind v4).

## Bảng màu

| Token | Giá trị | Dùng cho |
|-------|---------|----------|
| `--color-primary` | `#3B82F6` | Xanh chủ đạo |
| `--color-primary-dark` | `#1D4ED8` | Xanh đậm |
| `--color-violet` | `#8B5CF6` | Tím nhấn |
| `--color-cyan` | `#22D3EE` | Cyan nhấn |
| `--color-accent` | `#FACC15` | Vàng nhấn (trích dẫn, điểm nhìn) |
| `--color-bg` | `#05070B` | Nền trang |
| `--color-panel` | `#0B1020` | Nền panel/thẻ |
| `--color-ink` | `#F1F5F9` | Chữ chính |
| `--color-muted` | `#94A3B8` | Chữ phụ |
| `--color-line` | `rgba(255,255,255,.08)` | Viền mảnh |

## Kiểu chữ

| Token | Font | Dùng cho |
|-------|------|----------|
| `--font-display` | **Be Vietnam Pro** | Tiêu đề |
| `--font-body` | **Inter** | Nội dung |
| `--font-mono` | **JetBrains Mono** | Nhãn/số/eyebrow (uppercase, tracking rộng) |

## Lớp tiện ích đặc trưng (`globals.css`)

- **`.text-gradient`** — chữ gradient thương hiệu (xanh → tím → cyan), dùng cho
  từ khóa nổi bật trong tiêu đề.
- **`.glass`** — thẻ kính mờ (`backdrop-blur`, nền trắng 4%, viền 8%).
- **`.glass-hover`** — nâng nhẹ (`translateY(-6px)`), viền tím + đổ bóng khi hover.
- **`.glow-blob`** — quầng sáng neon nền, blur 90px, trôi nhẹ (`blob-drift` 14s).
- **`.grid-bg`** — lưới nền mờ kiểu "bảng thí nghiệm", mask radial mềm mép.
- **`.marquee`** — dải công thức chạy ngang liên tục (28s linear).
- **`.fade-up` / `.delay-1..3`** — hiện dần khi cuộn tới (dùng với
  `components/ui/Reveal.tsx`).

## Nguyên tắc bố cục

- Nền tối nhất quán; điểm sáng bằng gradient và glow, không dùng khối màu đặc.
- Nội dung trên **thẻ kính mờ** nổi trên nền lưới + quầng neon.
- Eyebrow (nhãn nhỏ) dùng `font-mono`, chữ hoa, `tracking-widest`, màu cyan/muted.
- Tiêu đề dùng `font-display` đậm; từ khóa quan trọng tô `.text-gradient`.
- Trích dẫn: viền trái màu `accent`, chữ nghiêng.
- Chuyển động tinh tế (framer-motion + `fade-up`), tôn trọng cảm giác "vật lý":
  mượt, có quán tính, dùng easing `cubic-bezier`.

## Component UI dùng lại

- `components/ui/Reveal.tsx` — bọc để hiện dần khi cuộn.
- `components/ui/Skeleton.tsx` — trạng thái tải.
- `components/ui/Toast.tsx` — thông báo (`ToastProvider` ở `app/layout.tsx`).
- `components/physics/*` — mô phỏng tương tác (SpringSimulation, DisplacementChart,
  ControlPanel, FormulaPanel, Tooltip) tái sử dụng cho hero và bài giảng.

Tham chiếu thương hiệu & giọng điệu: [`BRAND.md`](./BRAND.md).
