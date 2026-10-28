## Hình OpenStax (28/10/2026)
- Thay: Hình 3 → College Physics 2e Hình 27.11 (cùng pha/ngược pha, tổng 2X hoặc 0; sách đặt ở chương 27 Quang sóng); `public/assets/openstax/l11-giao-thoa-song/hinh-cung-pha-nguoc-pha.webp`. bundle.json cập nhật tay từ theory.html (bài không có build_bundle.py).
- Giữ SVG: Hình 1 (hai loa, sách không có), Hình 2 (hypebol AB = 4λ, 7 cực đại/8 cực tiểu, sách Hình 27.12 là ánh sáng qua hai khe, không đếm), Hình 4 (khe Young ký hiệu a, D, i; Hình 27.14 dùng d, θ, Δℓ khác ký hiệu bài), Hình 5 (đếm cực trị số liệu riêng).

## Hình OpenStax đợt 2 (28/10/2026)
- Thay Hình 1 (SVG hai loa) → College Physics 2e Hình 16.41, `hinh-hai-loa-cuc-dai.webp` (400×252): hai loa, vân nén/dãn, chấm đỏ = cực đại. Dời mốc `<!--FIG1-->` xuống SAU hộp "Dự đoán" (trước mục II) để ảnh không lộ đáp án trước câu hỏi; figcaption chỉ ghi "Chấm đỏ: nghe to", nhãn Compression/Rarefaction ở chú thích lề.
- Thêm Hình 5 (mốc mới `<!--FIG4B-->`, ngay sau các gạch đầu dòng của mục 4, trước công thức) → Hình 27.15, `hinh-khe-young-cuong-do.webp` (875×521): hai khe, đồ thị cường độ, ảnh vân thật. Sách ghi d, x, y; bài ghi a, D, x; figcaption nối d = a, x = D. Giữ SVG Hình 4. Hình cũ 5 (đếm cực trị) đánh lại thành Hình 6 (chỉ đổi số trong figcaption, bài không nhắc "Hình N" trong văn bản).
- Tổng 6 hình. Bài không có build_bundle.py: bundle.json cập nhật `theory_html` từ theory.html bằng script thay chuỗi.
- Độ dài (lint_do_dai, chữ hiện ngay): 2000 → 2056 (còn dưới trần 2500).
