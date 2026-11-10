Hình 3 — bố cục tham khảo HRW 12e, Fig. 30.1.5 (ch. 30), vẽ lại bằng svg_lib

## Hình OpenStax (giai đoạn 2, 27/10/2026)
- Giấy phép: OpenStax *College Physics 2e* (Urone & Hinrichs), CC BY-NC-SA 4.0 (thầy đã chấp nhận điều kiện phi thương mại). Mỗi hình có dòng nguồn trong figcaption.
- Hình 2: chèn trực tiếp ảnh Hình 23.4 (cắt lấy hai phần a, b: nam châm vào / ra, kim điện kế lệch ngược nhau), `public/assets/openstax/l12-cam-ung-dien-tu/hinh-2.webp` (420x372, 13 KB); nhãn tiếng Anh giải nghĩa trong figcaption. Ảnh raster là ngoại lệ có chủ đích của quy tắc SVG tự vẽ.
- Hình 3: bảng chọn "chèn trực tiếp" Hình 23.7, nhưng đã xem ảnh: nhãn B_mag, B_coil, I quá nhỏ ở 375 px (cỡ chữ ~6 px). Giữ SVG tự vẽ (đã có B cảm ứng, B nam châm, chiều i), ghi "Vẽ lại theo OpenStax Hình 23.7".
- Hình 1: giữ SVG (theo bảng).
- Hạn mức độ dài: thêm chú thích nguồn nên đã rút ~30 từ ở mục I, III, IV (câu mở bài, mẹo, cách giảm sai số).

## Đợt 2 (27/10/2026): quy tắc mới, ưu tiên ảnh OpenStax, không vẽ lại
- Hình 1: thay SVG bằng ảnh OpenStax Hình 23.6 (`hinh-tu-thong-dong-gia.webp`, 600x607, 15 KB); θ của sách = α của bài, ghi trong figcaption.
- Hình 3: thay SVG (vẽ lại theo Hình 23.7) bằng ảnh OpenStax Hình 23.7 phần a, cắt bỏ bàn tay RHR-2 (`hinh-lenz-nam-cham-tien-lai.webp`, 700x215, 10 KB); nhãn B_mag, B_coil, I giải nghĩa trong figcaption. Chữ ở 340 px khoảng 9 px (ranh giới đọc được).
- Hình 2: đã là ảnh OpenStax từ đợt 1 (hinh-2.webp). Không còn hình SVG nào trong bài.
- Mã vẽ SVG hình 1, 3 đã xoá khỏi build_figs.py. Rút ~30 từ ở mục II và câu Dự đoán để giữ hạn mức 2500 từ. Ảnh raster là ngoại lệ có chủ đích của quy tắc SVG tự vẽ.
