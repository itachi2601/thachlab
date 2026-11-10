Hình 4c — bố cục tham khảo HRW 12e, Fig. 29.4.3, 29.4.2 (ch. 29), vẽ lại bằng svg_lib

## Hình OpenStax (27/10/2026, giai đoạn 2)
- Giấy phép: OpenStax College Physics 2e, CC BY-NC-SA 4.0 (thầy đã chấp nhận điều kiện phi thương mại). Dòng nguồn nằm trong figcaption từng hình.
- Hình 4a (dây thẳng) vẽ lại theo Hình 22.37 · Hình 4b (vòng dây) vẽ lại theo Hình 22.38 · Hình 4c (ống dây) vẽ lại theo Hình 22.39. Cả ba là SVG vẽ lại (nhãn Việt, SI), KHÔNG chèn ảnh raster: hình sách nhiều nhãn Anh (Solenoid, N, S, I in/out, RHR-2) và là sơ đồ.
- Đường sức 4b và 4c tính bằng numpy (Biot–Savart cho chuỗi vòng dây + tích phân RK4 theo hướng B trong mặt phẳng chứa trục), chiếu lên hình nhìn xiên có che khuất; nét đứt + đầu V 30°. 4b: trục + sáu đường khép quanh từng đoạn dây. 4c: ống dài 10R, năm đường song song cách đều trong lòng ống, hai đường sát vách khép kín, ba đường gần trục toả ra hai đầu như nam châm thẳng.
- Hình 1, 2, 3 giữ SVG (xem docs/ra-soat/hinh-openstax-l12.md). Không có ảnh raster nào trong bài này, nên không có ngoại lệ quy tắc SVG tự vẽ.
- Để giữ hạn mức độ dài (≤2500 từ hiện ngay) đã bỏ dòng "5 hình = cả bài" ở phần Mang về, câu thừa trong "Rút ra" của thí nghiệm cân, rút gọn ba gạch đầu dòng/caption quanh Hình 4a–4c.

## Đợt 2 (27/10/2026) — ưu tiên ảnh OpenStax, không vẽ lại
- Quy tắc mới của thầy: lấy thẳng ảnh OpenStax College Physics 2e (CC BY-NC-SA 4.0), không vẽ lại. Ảnh raster là ngoại lệ có chủ đích của quy tắc SVG tự vẽ; đã bỏ toàn bộ mã numpy/Biot–Savart trong build_figs.py.
- Thay bằng ảnh OpenStax: Hình 4a = Hình 22.37a (cắt phần a) → public/assets/openstax/l12-luc-tu-cam-ung-tu/hinh-day-thang-duong-suc-tron.webp · Hình 4b = Hình 22.38b (cắt phần b, đường sức vòng dây) → hinh-vong-day-duong-suc.webp · Hình 4c = Hình 22.39b (cắt phần b, mặt cắt ống dây) → hinh-ong-day-duong-suc.webp. Chỉ cắt, không chỉnh nội dung; nhãn Anh được giải nghĩa trong figcaption (4c: I_in, I_out; chữ N, S giữ nguyên).
- Giữ SVG: Hình 1 (Hình 22.29 vẽ nam châm chữ U nằm ngang, B ngang và bàn tay PHẢI RHR-1, trong khi bài dùng bàn tay TRÁI và B hướng xuống → dễ nhầm quy tắc); Hình 2 (Hình 22.30 cũng RHR-1 tay phải, không thay được quy tắc bàn tay trái); Hình 3 cân dòng điện (OpenStax không có).
- Để giữ hạn mức ≤2500 từ hiện ngay, figcaption ba hình mới viết ngắn (2499 từ).
