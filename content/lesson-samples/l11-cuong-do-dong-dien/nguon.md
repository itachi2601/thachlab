## Hình OpenStax (28/10/2026)
- Giữ SVG cả 4 hình, không thay ảnh OpenStax. Hình 1 (ampe kế nối tiếp): Hình 20.3/20.4 không có ampe kế. Hình 2 (đồ thị q–t, 5 điểm đo 1,50 A) và Hình 3 (dòng không đổi vs một chiều chỉnh lưu): sách không có hình cùng số liệu. Hình 4 (trụ v·Δt): Hình 20.7 cùng ý nhưng ký hiệu A, v_d, x khác bài (S, v, Δt) và SVG đang gắn thí nghiệm tn-l11-cuong-do-dong-dien-03.

## Hình OpenStax đợt 2 (28/10/2026)
- Thay Hình 4 (SVG hình trụ v·Δt trước tiết diện S) bằng ảnh Hình 20.7 (mục 20.1), `public/assets/openstax/l11-cuong-do-dong-dien/hinh-hat-tai-dien-trong-day.webp` (625×329, 12 KB). Figcaption nối ký hiệu: A = S, v_d = v, t = Δt, x = vΔt. Giữ `data-exp="tn-l11-cuong-do-dong-dien-03"` trên figure; thí nghiệm/câu hỏi không nhắc "Hình 4" bằng nhãn riêng.
- Để bù chữ, rút hai câu trùng hình trong theory.src.html: bỏ "thể tích S·v·Δt" ở đoạn dẫn và rút bullet "hình vẽ hạt dương".
- Số chữ hiện ngay: 2485 → 2484. Hình raster là ngoại lệ có chủ đích của quy tắc SVG; build_figs.py còn code SVG Hình 4 cũ không dùng (hàm f dựng chung).
