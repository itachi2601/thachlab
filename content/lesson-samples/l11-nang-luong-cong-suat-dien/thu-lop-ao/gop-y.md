# Góp ý bài 25 Năng lượng điện và công suất điện (lớp ảo lượt 2)

HS ảo đã đọc chỉ `sach-trong.md` + `de-hs-1..6.md` (không thấy đáp án). Nên chỉ tin các chỗ ghi "đoán/không hiểu" và các lệch tài liệu, không tin tỉ lệ đúng. Mã trang Tập: tr.37–41, ô 37·1…41·4 (đã khớp màn bản src).

| # | file · vị trí | sửa gì | ưu tiên | bằng chứng |
|---|---|---|---|---|
| 1 | `tren-lop-ghi-chu.html` (cả file) | Hiện là ghi chú BÀI 22 (tiêu đề "Cường độ dòng điện", đề 1217, "22 màn", clip đồng hồ USB). Viết lại cho bài 25: 24 màn, 6 điểm dừng, ấm, công tơ, clip đèn xe máy 12 V–21 W, clip hai pin AA, đề 1220 (19 câu), bảng "Đi theo Tập bài 25" tr.37–41 | cao | nhat-ky 1; hs không đọc nhưng thầy bấm ghi chú sẽ đọc nhầm bài |
| 2 | `tren-lop.html` (bản dựng) | Chưa dựng lại: còn mã cũ "tr.1…tr.5 / ô 1·2…5·4", chỉ `tren-lop.src.html` có tr.37–41. Chạy lại `build_tren_lop.py`, rồi kiểm mã trang trên bản dựng | cao | nhat-ky 2; hs-1…hs-6 bám mã 37·x…41·x |
| 3 | Tập 38·3 (hàng $I$), màn 3c clip dừng ① | Bỏ hàng $I$ in sẵn ở 6,0 V (hoặc cả ba mức) để lớp ghi từ clip; hoặc đổi câu dừng ① sang "đèn mờ thì $R$ thế nào" | cao | hs-3 [36]–[41]; phan-hoi-3 |
| 4 | Tập 39·2 (bảng $I$, $U$), màn 4c clip dừng ② | Bỏ hàng $H$ lộ xu hướng: che cột 9,0 Ω hoặc để HS điền $I$, $U$ từ clip; thêm ô "H đạt 100 %?" | cao | hs-4 [59]–[62], D chọn nhờ bảng |
| 5 | Tập 40·1 Bẫy 3, màn 5e | Bỏ chữ "$R$ lớn nhận nhiều hơn" khỏi ô (để HS điền sau khi chọn); bẫy in dạng câu hỏi không mệnh đề sai | cao | hs-5 [79]–[81] "đoán, suy từ P=I²R"; nhat-ky 4 |
| 6 | Tập 39·3 ô [72], màn 5b | Bỏ dòng "(có 5 A, 10 A, 30 A)" hoặc đổi cỡ khác nhau giữa màn và Tập (vd. 5, 10, 16 A) | vừa | hs-5 [72] chọn "5 nhỏ hơn 8,2, 30 quá lớn"; nhat-ky 4 |
| 7 | Tập 40·1 Bẫy 2 ô [76] | Bỏ "lớn hơn $UI$ một phần ▭" (lộ $I^2r$) hoặc đổi thành "chênh lệch EI và UI là ▭" | vừa | hs-5 [76] "(đoán)", phan-hoi-5; nhat-ky 4 |
| 8 | Tập 38·3 ô [44] "dây tóc ▭", màn 3d | Thêm 1 câu dạy "điện trở dây tóc tăng khi nóng" trước ô, hoặc đổi ô thành "vì dây tóc ít ▭ hơn" kèm gợi ý nhiệt độ; chuyển "coi R không đổi" thành ô đã cho | vừa | hs-3 [44],[45] "(đoán)"; nhat-ky 5 |
| 9 | Tập 38·2 [23],[24],[28],[30],[32] (định nghĩa công suất, định mức, J/s) | Cho nửa câu mẫu ("công suất = điện năng ▭ trong 1 giây") và một dòng đời sống cho "định mức" (nhà sản xuất ghi); hoặc dừng ② nói thẳng trước khi điền | vừa | hs-3 màn 3a, 3b nhiều "(đoán)", "định mức" không rõ nghĩa |
| 10 | màn 3e ô [46] | Thêm câu dẫn "so sánh 110/220 rồi bình phương" để HS lập luận P∝U²; ghi cách giải thích ở ghi chú | vừa | hs-3 [46] "đoán, chưa học chắc" |
| 11 | Tập 39·1 ô [47]–[48] | Thêm một dòng "dòng $I$ chạy qua cả nguồn lẫn mạch ngoài ⇒ $q=It$" (bài 24 đã có) trước ô $A_{ng}$ | vừa | hs-4 [47],[48] "(đoán)" |
| 12 | Tập 39·2 [55]–[58], màn 4b | Giải thích bằng 1 hình/ví dụ vì sao [58] khi có quạt/pin sạc không dùng $U/E$ (chỉ dùng $A_{ci}/A_{tp}$); thêm ô ví dụ số | vừa | hs-4 [58] "(đoán; không dùng U/E được)" |
| 13 | Tập 37·4 [9]–[16] | Thêm chú thích nhỏ cho "cơ năng/hoá năng" (quạt/sạc pin); đổi thứ tự [15],[16] để không đoán cặp tương phản; bỏ "(Jun–Len-xơ)" lộ ở dòng 4 | thấp | hs-2 [9]–[16]; nhat-ky 4 |
| 14 | Tập 38·1 ô [22], màn 2d | Thêm phương án hoặc ô "kWh" trên màn (0,22 kWh) hoặc đổi Tập chỉ hỏi kJ | thấp | hs-2 [22] chọn B rồi tự ghi 0,22 kWh; nhat-ky 10 |
| 15 | Màn 3d vs "Về nhà" | Bỏ $R=5{,}8$ Ω khỏi màn 3d hoặc đổi "Về nhà" bỏ dòng 9,0 V; để lớp tự điền | thấp | hs-3 [40]; nhat-ky 9 |
| 16 | Ghi chú điểm dừng 5 + `tren-lop.src.html` m5a–m5e | Tách thành hai điểm dừng (đoản mạch/cầu chì và ba bẫy) hoặc ghi rõ Bẫy 2 cho về nhà; 17 ô trong 8 phút quá dày | vừa | hs-5 (cả điểm dừng); nhat-ky 14 |
| 17 | Tập 41·1 hàng 2 ô [94] | Cho mẫu hàng 2 ("(ngầm) mạch kín → I = E/(R+r)") và để ô trống chỉ ở hàng 3 | thấp | hs-6 [94] "(đoán)" và "Chữ khó hiểu" |
| 18 | `de-hs`/QR đề 1220, màn 6c | Kiểm tay đề 1220 (19 câu) khớp phần đã dạy, QR mở được; soát câu dùng khái niệm chưa dạy | vừa | hs-6 [91]–[93] không có đề; nhat-ky 15 |
| 19 | m4 (hình web nền tối) | Mở màn 4 xem bằng mắt, đổi `fill="#e8ebf2"` còn sót thành màu nền sáng | vừa | nhat-ky 11, 17 |
| 20 | Màn 6b "Quay lại hoá đơn" + ô 37·1 | Thêm chữ trên màn "lật tr.37, tích ba mục tiêu ô 37·1 (20 s)"; chữ "lật về trang 37" ở màn | thấp | hs-6 [90]; nhat-ky 7, 8 |

## Đã xử lý (27/11/2026)
Làm: 1 (viết lại tren-lop-ghi-chu.html cho bài 25), 2 (dựng lại tren-lop.html + bản public/dev), 3 (Tập 38·3 bỏ hàng I in sẵn), 4 (Tập 39·2 bỏ hàng I; giữ hàng U, màn 4c ghi "lớp điền I"), 5 (Bẫy 3 không in "R lớn nhận nhiều hơn"), 6 (cầu chì 5/10/16 A, màn + Tập), 7 (Bẫy 2 đổi thành "chênh lệch EI−UI", màn 5d khớp), 8 (thêm gợi ý "nhiệt độ" cạnh ô dây tóc), 11 (dòng "I chạy qua cả nguồn lẫn mạch ngoài" ở 39·1), 19 (fill #e8ebf2 là nền màn công tơ, chữ tối, đọc được: không lỗi), 20 (chữ nhắc lật tr.37 trên màn 6b).
Bỏ/treo: 9, 10, 12, 13, 14, 15, 16 (ghi chú dạy đã ghi "điểm dừng 5 dày, ưu tiên"), 17, 18 (chưa đối chiếu tay đề 1220 với phần dạy; cần DB).
Kiểm máy ĐẠT (24 màn, không tràn, katex-error 0, 375px ok); PDF Tập giữ 12 trang. Lưu ý: HS ảo chỉ đọc sach-trong.md + de-hs-1..6.md.
