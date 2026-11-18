# Bài 14 KHTN 9 (lesson_id 92) — Cảm ứng điện từ. Nguyên tắc tạo ra dòng điện xoay chiều

## Chặng
- 2026-11-18 · Chặng 1 XONG (chưa kiểm chéo, chưa đăng DB): theory.html (2.261 từ hiện ngay, ~16,1 phút → ghi 16; 8 quiz, đáp án đúng 2A/2B/2C/2D; 4 hình), bundle.json (6 câu, validate ok), tn-l9-camung-01..03.json (kiểm bằng thi_nghiem.py trên bản sao kho ở scratchpad, KHÔNG ghi index.json).
- 2026-11-18 · Sửa theo kiểm chéo: cắt details 'mặt cuộn dây song song' (đếm có dấu, ngoài YCCĐ); quy tắc tăng→giảm chỉ còn cho nam châm lại gần/ra xa, chỗ quay chỉ nêu kết quả 'đổi chiều 2 lần/vòng' (II.3, II.4, IV.5, V.b); Câu 4 đổi tình huống đẩy vào rồi dừng; TN3 thêm dụng cụ (nam châm đất hiếm, cuộn ≥1000 vòng), ngưỡng quay chậm thì LED không sáng; bảng TN1 vào details 📊 có kiểm quy luật i·t và tách sai số hệ thống/ngẫu nhiên; 🔑 II.1, nhiễu D Câu 2, '(Hình 2)', màu chữ nhãn đậm (#0284c7/#059669/#dc2626), nhãn LED sát đèn. 2.269 từ hiện ngay, lint_do_dai 0 lỗi, 1 cảnh báo (tổng > 2000).
- Nguồn: "BÀI 13. CẢM ỨNG ĐIỆN TỪ - GV.docx" + phần máy phát / nguyên tắc của "BÀI 14. DÒNG ĐIỆN XOAY CHIỀU - GV.docx" (lấy ý, không chép, không dùng ảnh). Tác dụng của dòng xoay chiều để bài 93 (chỉ một câu chuyển tiếp).

## Ý bắt buộc (YCCĐ KHTN 9) — so lại sau khi viết
- [x] Thí nghiệm Faraday nam châm – cuộn dây – điện kế (đứng yên / lại gần / ra xa / quay) — II.1, Hình 2, tn-01 (khung 6 ô T1–T12)
- [x] Thí nghiệm nam châm điện đóng/giữ/ngắt công tắc — II.2, tn-02
- [x] Khái niệm dòng điện cảm ứng, hiện tượng cảm ứng điện từ — II.1 🔑
- [x] Điều kiện: số đường sức từ xuyên qua tiết diện cuộn dây kín biến thiên (không dùng từ thông, không Lenz định lượng) — II.3, Hình 3
- [x] Dòng điện xoay chiều = luân phiên đổi chiều; khi nào đổi chiều — II.4, Hình 4, tn-03 (2 LED ngược chiều)
- [x] Nguyên tắc tạo dòng xoay chiều: nam châm quay / cuộn dây quay — II.5
- [x] Máy phát điện xoay chiều: rôto, stato; đinamô xe đạp; cơ năng → điện năng — II.5, bảng 3 cột
- [x] Quan niệm sai: "nam châm đứng yên trong cuộn dây vẫn có dòng", "từ trường mạnh là đủ" — III Bẫy 1; thêm Bẫy 2 "cứ quay là có dòng"
- [x] Thí nghiệm đo có bảng số liệu + nhận xét sai số (đưa nhanh/chậm, 3 lần) — II.1 + details 📊

## Đề xuất clip mở bài (chưa chèn — thầy chọn)
- Cận cảnh đèn đinamô xe đạp: đạp chậm đèn chập chờn, đạp nhanh sáng đều, phanh dừng thì tắt ngay (10–20 s, quay ban đêm). Có thể tự quay bằng xe đạp có đinamô núm tì lốp.

## Treo
- Kiểm chéo nội dung (kiem-code) trước khi đăng.
- Đăng: bài 92 trống lesson_items → dùng upload-lesson.mts (phiên Mac); index.json chưa có 3 mục camung (chạy thi_nghiem.py một lần khi gom lô).
- Số liệu bảng TN1 là minh hoạ (ghi rõ trong bài); có số đo thật thì thay trong build_figs.py (DOC).
- docs/BANG-MEO-TU-KHOA.md: dùng lại "Kín – Đổi – Dòng", "Quay – Đổi – Sinh" (L12) với nghĩa lớp 9 (đổi = số đường sức); chưa thêm dòng lớp 9 vào bảng.
- PhET faradays-law trong details: chưa mở thật lại ở phiên này (đã dùng ở L12).
- lint_do_dai: 1 cảnh báo (tổng 2.269 > 2.000), 0 lỗi cứng.
