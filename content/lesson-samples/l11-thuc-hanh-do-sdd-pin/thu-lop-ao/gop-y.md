# Góp ý bài 26 (Lượt 2) — SRC=../tren-lop.src.html · GC=../tren-lop-ghi-chu.html · MJS=scripts/ruot-tap/l11-bai26.mjs

Chỉ đề xuất sửa trong SRC/GC/MJS. Lưu ý: hs không xem được clip 4b, 4d.

| # | file | vị trí | sửa gì | ưu tiên | bằng chứng |
|---|---|---|---|---|---|
| 1 | SRC (+ MJS ô 50·2) | màn 3b (dòng 184–185) và ô 50·2 | Số pin mới 1,50 V / 0,30 Ω lệch 1,58 V / 0,26 Ω (4e, clip). Đổi 3b/50·2 sang "pin ví dụ ℰ = 1,50 V, r = 0,30 Ω" (không gọi "pin mới"), hoặc dùng cùng 1,58 V / 0,26 Ω (tính lại 6,1 A và 0,69 A) | cao | hs-5 dòng 10, 39; hs-3 dòng 12; nhat-ky mục 1 |
| 2 | SRC | màn 4e (dòng 281–295) | Thêm vào nút mở bảng 6 cặp (I, U) pin mới (số đúng của clip) để học sinh chép/đối chiếu, giống bảng tĩnh pin cũ ở 4c; kèm A, B gợi ý (lần 1 và lần 6) cho 53·2 | cao | hs-5 dòng 3, 7–13, 26, 27; hs-4 dòng 3 |
| 3 | GC | điểm dừng 5 (dòng 94) | Dặn: ở clip 4d dừng đủ lâu để lớp chép 6 cặp; nếu chép không kịp thì chiếu bảng 4e rồi mới nói "E 1,58 V" | cao | hs-5 dòng 7; nhat-ky Lượt 2 mục 2 |
| 4 | SRC | màn 3a, nút mở a3a (dòng 175) | Thêm bốn hàng còn thiếu: pin nối tiếp mạch kín; Rx nối tiếp, đổi điện trở ngoài; R₀ nối tiếp, hạn dòng; K nối tiếp, đóng/ngắt | cao | hs-3 dòng 3–6, 31 |
| 5 | SRC (+ GC) | màn 6a (dòng 322–337) | Thêm vào nút mở đáp án ô 52·2 (5 hàng nguyên nhân → khắc phục) và hai ☐ ampe kế (ngoài M–N, không cộng vào r); sửa nhãn tap cho đúng nội dung; ghi trong GC | cao | hs-6 dòng 10–16, 40; nhat-ky mục 4 |
| 6 | SRC | màn 4a (dòng 223) | Đổi "Tổng cộng 6 lần đo" thành "Mỗi pin 6 lần đo, cả hai pin 12 lần" | cao | hs-4 dòng 9, 33, 42; sach-hs dòng 85 |
| 7 | SRC | màn 6a / "Về nhà" (dòng 369–374) | Ô 53·2 dòng sai số Δr: thêm một dòng hướng dẫn (Δr/r = tổng hai sai số tỉ đối) và ghi rõ trong "Về nhà" là làm ở nhà theo ví dụ; không để học sinh về nhà tự điền không hướng dẫn | vừa | hs-6 dòng 27, 30; nhat-ky mục 2 |
| 8 | SRC | màn 2a (dòng 140–151) | Chỉ rõ điểm (1), (2): "hai điểm bất kì trên đường thẳng, (1) ở I nhỏ hơn"; thêm một câu: "đường đi xuống nên hệ số góc âm = −r, r là số dương, nên viết U₁ − U₂ ở tử" | vừa | hs-2 dòng 9, 13, 16–17, 20–21 |
| 9 | SRC (+ GC) | màn 4b dừng ① (đáp án B), dòng 238 | Thêm cho GV một câu giải thích bằng chữ: "R_x giảm 100→20→…→0 không đều, I tăng nhanh ở cuối nên Ir tăng nhanh ở cuối"; ghi ở GC để thầy nói sau khi hiện đáp án | vừa | hs-4 dòng 12, 39 |
| 10 | SRC | màn 3b (dòng 185) | Chú thích "R_ngoài = điện trở phần mạch ngoài pin ($R_0+R_x$)" và "thang 2 A = dòng đo tối đa 2 A" | thấp | hs-3 dòng 27, 37 |
| 11 | GC | điểm dừng 5, câu "điều gì làm r tăng" (dòng 94) | Ghi sẵn gợi ý trả lời (pin dùng lâu: chất bên trong cạn, tiếp xúc kém, r tăng) hoặc ghi "để ngỏ, không chấm" | thấp | hs-5 dòng 34, 42 |
| 12 | SRC (+ MJS) | màn 1 / ô 49·2 (dòng 133–134) | Đổi "điện áp ảo" thành cách nói quen hơn ("chỉ còn 1,06 V dù pin vẫn 1,50 V") hoặc giải nghĩa ngay ở màn 1 | thấp | hs-1 dòng 13, 21 |
| 13 | GC | điểm dừng 6 (dòng 105) | Giữ cảnh báo kiểm đề 1221 20 câu hay 6 câu (exam.json 6 câu) trước giờ dạy; ghi nơi tra | vừa | nhat-ky phần soát mục 6; hs-6 dòng 25 |

## Đã xử lý (22/11/2026)
Làm: 1 (màn 3b và ô 50·2 gọi "pin ví dụ"), 2 (màn 4e thêm bảng 6 cặp pin mới + gợi ý A, B), 3, 4 (bốn hàng ở màn 3a), 5 (đáp án ampe kế ngoài M–N ở màn 6a; bảng nguyên nhân 52·2 ghi "làm ở nhà"), 6, 7 (ghi rõ làm ở nhà), 8, 10, 11, 13.
Bỏ: 9 (giải thích bằng lời để thầy nói, chưa thêm vào GC), 12 (chữ "điện áp ảo" y Tập, giữ vì sửa Tập lệch đề cả quyển).
Ruột tập: sửa chữ "Pin mới có"→"Pin ví dụ có" (ô 50·2), đã đổi Bẫy 1/2 thành tiêu đề trung tính và ô 50·4 thành "Đề 1221 (20 câu)". Kiểm máy ĐẠT.
