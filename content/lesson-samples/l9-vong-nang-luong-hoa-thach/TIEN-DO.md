# Tiến độ — Bài 16 KHTN 9 (lesson_id 94), Vòng năng lượng trên Trái Đất. Năng lượng hoá thạch

## Ý bắt buộc (YCCĐ KHTN 9) — đối chiếu sau khi viết: đủ
- Vòng năng lượng trên Trái Đất; Mặt Trời là nguồn chính (II.1–II.2, Hình 2) ✓
- Nguồn gốc nhiên liệu hoá thạch: than, dầu mỏ, khí tự nhiên (II.3, Hình 3, mẹo 🧠 Chôn – Ép – Lâu) ✓
- Không tái tạo vì hình thành hàng triệu năm (II.3, Bẫy 2) ✓
- Ưu/nhược điểm khi dùng (II.5) ✓
- Ô nhiễm khi khai thác và sử dụng: SO2, NOx, bụi, CO2, tràn dầu, sụt lún (II.4, Bẫy 3) ✓
- Giá phụ thuộc chi phí khai thác và vận chuyển (II.5, q5) ✓
- Sử dụng tiết kiệm (VI) ✓
- Hai quan niệm sai kinh điển: "dầu mỏ không liên quan Mặt Trời" (Bẫy 1), "hoá thạch tạo lại nhanh / dùng mãi" (Bẫy 2); thêm Bẫy 3 "hiệu ứng nhà kính lúc nào cũng xấu" ✓

## Nhật ký
- 2026-11-18 · Chặng 1 XONG (chưa kiểm chéo): theory.html (2.296 từ hiện ngay, ~16,4 phút → ghi 17; 8 quiz, đáp án đúng 2A/2B/2C/2D; 4 hình; V là Tình huống mẫu theo bảng Câu trong đề | Dữ liệu | Kiến thức), bundle.json (6 câu, validate ok), tn-l9-hoathach-01..03.json (kiểm bằng thi_nghiem.py trên bản sao kho ở scratchpad, KHÔNG ghi index.json).
- Số liệu có nguồn ở chú thích: 30% phản xạ / 70% (tài liệu KHTN 9 KNTT; NASA ghi ~29%), 15 °C vs −18 °C (NASA), năng suất toả nhiệt (bảng tài liệu KNTT).
- Bảng số liệu thí nghiệm nến (tn-02) là số minh hoạ dựng từ mô hình (200 g nước, q = 42 kJ/g, hiệu suất giảm dần) — ghi rõ là số mẫu, không phải đo thật.
- Clip mở bài: CHƯA chèn (chờ thầy chọn). Đề xuất: time-lapse ống khói nhà máy nhiệt điện than (hoặc time-lapse nước bốc hơi → mây → mưa), không lời, 10–20 giây.
- 2026-11-18 · Sửa theo kiểm chéo: dời câu "địa nhiệt, hạt nhân, thuỷ triều không đến từ Mặt Trời" xuống sau Câu 1 (lộ đáp án); Câu 2 đổi ngữ cảnh (bạn Khoa: "năng lượng rau lấy từ đất"); thêm dòng an toàn hộp đốt nến; "5 hình = cả bài" → "Nhớ 5 cảnh trên là nhớ cả bài" (5 cảnh là 5 gạch đầu dòng, không phải số hình); tiêu đề Bẫy 1 trung tính; tn-01 thêm "khoảng 10–15 phút"; chú thích 1 ghi rõ 23% bay hơi theo tài liệu dạy thêm KNTT; chú thích 3 ghi "số liệu gần đúng", nguồn Câu 33 tài liệu dạy thêm (đã đối chiếu: 10·10^6, 14·10^6, 44·10^6 J/kg).
- Bảng nến: build_figs.py dùng nghiệm đúng T = 28 + 50(1 − e^(−K t/50)), K ≈ 1,33 °C/phút làm nguồn sự thật duy nhất → 28,0/30,6/33,0/35,4/37,6 (nghiệm chính xác 30,58/33,03/35,36/37,56). Số 30,65/33,16/35,54/37,80 của kiểm chéo là bước Euler 2 phút (thô), không phải mô hình. Bảng, so_lieu_mau, quan_sat, ket_qua_ky_vong (≈ 9,6 °C) cùng sinh từ một mảng rows2.
- Gọt chữ cho đủ trần: 2.296 từ hiện ngay, 17 phút.

## Treo
- Mẹo mới chờ ghi vào BANG-MEO (không tự sửa): 🧠 "Chôn – Ép – Lâu" (nguồn gốc hoá thạch), 🧠 "Nước – Gió – Cây" (ba nhánh vòng năng lượng). Thêm 2 mẹo 🧠 mới "Chôn – Ép – Lâu", "Nước – Gió – Cây" vào docs/BANG-MEO-TU-KHOA.md (file chung, chưa sửa).
- Chạy thi_nghiem.py trên kho thật khi gom lô để index.json có 3 mục hoathach.
- Bài 94 chưa có lesson_items → đăng lý thuyết bằng upload-lesson.mts (không dùng cap-nhat-ly-thuyet.sh).
- Chưa kiểm chéo kiem-code, chưa commit, chưa đăng DB. Không commit xem-thu/.
