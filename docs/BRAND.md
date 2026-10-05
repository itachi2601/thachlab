# Dấu ThạchLab

Chốt 5/10/2026 từ phác thảo tay của thầy: một **chén cầu** (mặt cắt) nghiêng, đáy chạm mặt bàn thí nghiệm, **nêm** đỡ phía phải, **dây qua ròng rọc** treo quả cân.

Ba máy đơn trong một hình — chén (cân bằng, mô-men), nêm, ròng rọc — đúng câu thương hiệu *sống giữa phương trình và chuyển động*, và đúng cả hai việc thầy dạy: Vật lý THPT và Cơ khí.

## Dùng ở đâu

| Chỗ | File |
|---|---|
| Đầu trang, chân trang | `components/brand/Logo.tsx` — dấu + chữ **ThạchLab** |
| Sidebar quản trị | `components/brand/LogoMark.tsx` |
| Favicon | `app/icon.svg` (ô xanh, nét trắng) |
| Logo schema.org | `public/images/logo.png` |
| File tải ra (nền tối / nền sáng, có chữ Thạch trên miệng chén) | `public/brand/` |

Màu mực đổi theo theme. Footer trang chủ và sidebar quản trị luôn nền tối nên dấu ở đó giữ mực sáng (`surface="dark"`), không lệ thuộc theme sáng/tối của trang.

## Màu

- Nền tối: mực `#E2E8F0`, lòng chén `#F8FAFC`, viền chén `#3B82F6`
- Nền sáng: mực `#0F172A`, lòng chén `#EFF6FF`, viền chén `#1D4ED8` (chữ “Lab” cùng xanh này — `#3B82F6` trên trắng chỉ 3,7:1, trượt chữ)
- Ô favicon: `#1D4ED8`

Một màu nhấn (xanh). Nêm, dây, ròng rọc, quả cân và mặt bàn cùng một mực — không thêm vàng/cyan.

## Chữ trong phác thảo

“Thạch” nằm trên miệng chén ở bản emblem (`public/brand/emblem-on-light.svg`, `emblem-on-dark.svg`) — đúng nét thầy viết.

“Vật lý 10” **không** đóng vào dấu chính. Dấu này đứng cho cả ThạchLab (KHTN 9, Vật lý 10–12, Cơ khí). Lòng chén để trống để còn đọc được ở 32px trên đầu trang. Muốn một biến thể riêng cho lớp 10 thì ghi chữ đó vào lòng chén của emblem, không sửa dấu ở navbar.

Chữ khóa trên website là **ThạchLab** (có dấu), font Be Vietnam Pro sẵn của trang. Tên miền và metadata giữ `ThachLab` không dấu.
