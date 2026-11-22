# Góp ý sau buổi chạy thử bài 21 Tụ điện (học sinh ảo, 6 điểm dừng)

src = `tren-lop.src.html` · ghi chú = `tren-lop-ghi-chu.html` · .mjs = `scripts/ruot-tap/l11-bai21.mjs`. Số [n] theo `sach-trong.md`. Học sinh không thấy clip/hình trong file chữ nên các mục về hình chỉ là điều cần thầy kiểm tận mắt.

| # | file · vị trí | sửa gì | ưu tiên | bằng chứng |
|---|---|---|---|---|
| 1 | src màn 4b + .mjs ô 2·3 [49]–[50] | Thống nhất 350/354: màn hiện cả "≈ 350 pF (làm tròn)" hoặc Tập ghi 354, và 177 ≈ 175 | cao | hs-4 "Lệch"; hs-4 dòng 4b |
| 2 | src màn 2a + .mjs ô 1·4 [5] | Ô "hai ___" chỉ có một đáp án: sửa thành "hai ___ (vật dẫn)" hoặc đổi chữ màn; gạch chân xanh nhìn thấy cả khi không có màu | cao | hs-2 dòng 3; phan-hoi-2 |
| 3 | src màn 1 + ghi chú | Bỏ "A/B/C/D" ở màn 1 (chỉ A, B, C); đổi phương án B bớt chữ "gom ... rồi xả" lộ đáp án | cao | hs-1 "Chữ khó"; hs-1 dòng 1 |
| 4 | src màn 5c + ghi chú | Bỏ "mẹo ghép tụ ngược ghép điện trở" hoặc dạy kèm vì lớp 11 chưa học điện trở; viết rõ [70],[71] ghi gì | cao | hs-5 dòng 5c, "Chữ khó" |
| 5 | .mjs ô 4·1, 5·2 + src màn về nhà | Ghi rõ ô [85]–[92], [104]–[107] làm khi nào; sửa "dòng giải bên dưới" ở [107]; hướng dẫn [91]–[92] | cao | hs-6 "Chữ khó" và dòng 5·2 |
| 6 | src màn 4a | Thêm 1 dòng giải thích ε (hằng số điện môi) và vì sao có $9\cdot10^9\cdot4\pi$ hoặc ghi "hằng số, chưa cần hiểu" | vừa | hs-4 dòng 4a |
| 7 | src màn 2b/2c + .mjs ô 1·5 | Giải thích "điện môi", "đảo LED/đảo chiều", "đồ thị dòng nạp" một câu | vừa | hs-2 "Chữ khó" |
| 8 | src màn 3b + .mjs ô 2·1 [27] | Cho từ "đánh thủng" xuất hiện trên màn trước ô [27] hoặc nhận "hỏng" | vừa | hs-3 "Sau khi xem" |
| 9 | src màn 3c + ghi chú | 4 nhóm bàn, 5 hàng: đổi thành 5 nhóm hoặc 1 nhóm hai hàng; trước biểu quyết hiện 1–2 số để không đoán | vừa | hs-3 dòng 3c, "Chữ khó" |
| 10 | src màn 3d | Phương án C ≈ 480 vs [36] ≈ 481: đồng bộ | thấp | hs-3 "Chữ khó" |
| 11 | src màn 3d, 5a | Nói W là năng lượng khi gặp lần đầu ở hình đồ thị Q–U; "trữ" → "dự trữ" | vừa | hs-3 dòng cuối; hs-5 "Chữ khó" |
| 12 | src màn 5 (cả 5a–5e) + ghi chú | Màn 5 quá dày (30 ô/7 phút): cân nhắc chuyển [54]–[57] về nhà hoặc tách 5c ra điểm dừng riêng | vừa | hs-5 dòng 5a |
| 13 | src màn 4b dừng ① | Câu hỏi A–D nói rõ hỏi về C | thấp | hs-4 "Lệch" |
| 14 | src màn QR, ghi chú | Học sinh ảo không làm đề 1216: đối chiếu đề với phần học (đã ghi trong ghi chú) vẫn chưa làm | vừa | hs-6 "Đề 1216" |
| 15 | src màn flash | Cụm "mạch tăng áp" thêm một câu | thấp | hs-6 dòng flash |
| 16 | ghi chú | Số ô đếm (11 chỗ ô 2·1, 7+6) khớp Tập | thấp | nhat-ky-thay mục 3–4 |

## Đã xử lý

Lý do bỏ từng mục ghi ở cột cuối. Chạy lại build + `kiem-tren-lop.mjs`: 23 màn, không màn tràn ở 1280×720 và 1920×1080 (đã mở hết đáp án và từng bước clip), katex-error 0, 375px không cuộn ngang, kết quả ĐẠT. Tập vẫn 12 trang (trang 5 còn dư 16 mm).

| # | xử lý | làm gì / lý do |
|---|---|---|
| 1 | làm | Tập ô 2·3 ghi "gốc ≈ 354 pF" khớp màn 4b và clip; 177 giữ nguyên ở cả hai nơi. |
| 2 | làm | Bỏ "(hai bản)" khỏi dòng Cấu tạo ở màn 2a. Thêm dòng nhỏ: "hai vật dẫn gọi là hai bản · điện môi = chất cách điện". Gạch chân `.o` vốn là gạch chân thật nên vẫn thấy khi không có màu. |
| 3 | làm một phần | Màn 1 đổi "giơ tay A/B/C/D" thành "giơ tay chọn phương án". Giữ chữ phương án B vì Tập đã in y như vậy. Màn 1 chỉ để khơi tò mò, không phải để bẫy: đoán đúng B vẫn phải giải thích được ở dòng "Vì sao?". |
| 4 | làm | Ghi chú bỏ câu "ghép tụ ngược ghép điện trở" vì lớp chưa học ghép điện trở. Hàng "So với" ở màn 5c ghi rõ chữ "**nhỏ hơn** tụ nhỏ nhất" và "**lớn hơn** tụ lớn nhất" (gạch chân). Ghi chú nói rõ ô nào cần tick. |
| 5 | làm | Màn 6c thêm dòng "Câu 1, 3, 4, 6: về nhà; đầu tiết sau bạn cùng bàn kiểm cả 6 câu". Màn về nhà nói rõ cách làm dòng bạn cùng bàn kiểm [91]–[92] và ô 5·2 [104]–[107]. Tập: dòng trống sau Thử sức có nhãn "Giải:". |
| 6 | làm | Màn 4a thêm dòng: ε là hằng số điện môi (không khí ≈ 1); $9\cdot10^9$ và $4\pi$ là hằng số, chỉ cần thay số. |
| 7 | làm | Màn 2a giải thích "điện môi". Clip 2b nói đồ thị là dòng nạp theo thời gian. Bước đảo LED nói lý do: LED chỉ sáng một chiều, dòng phóng ngược chiều dòng nạp. Tập ô 1·5 không sửa vì màn đã giải thích. |
| 8 | làm | Câu hỏi màn 3b đổi thành "Đặt 15 V thì tụ bị…?". Ghi chú dặn thầy nói to "đánh thủng" trước khi lớp điền; em ghi "hỏng" vẫn tính đúng rồi sửa lại. |
| 9 | làm | Ghi chú đổi thành 5 nhóm, mỗi nhóm một hàng U. Nhóm 2 V đã có số 490 từ dừng ① để đọc kiểm. Phần "hiện số trước biểu quyết" thì bỏ: biểu quyết trước clip là dự đoán, hiện số sẽ lộ đáp án. |
| 10 | làm | Phương án C màn 3d sửa thành ≈ 481 μF; ghi chú sửa theo. |
| 11 | làm | Đáp án màn 3d thêm dòng "diện tích dưới đường Q–U là năng lượng W, học ở điểm dừng 5". Màn 5a đổi "trữ" thành "dự trữ", khớp Tập. |
| 12 | làm một phần | Giữ [54]–[57] trên lớp vì năng lượng là kiến thức lõi và có trong đề cuối tiết. Ghi chú thêm phương án thiếu giờ: bỏ màn 5e, Bẫy 3 làm ở nhà. Không tách 5c thành điểm dừng riêng vì tiết đã có 6 điểm dừng, tách nữa thì vượt giờ. |
| 13 | bỏ | Câu ở dừng ① màn 4b đã có sẵn "$C$…". |
| 14 | treo | Chưa đối chiếu được đề 1216: phiên này không đọc được DB. Ghi chú vẫn giữ khung cảnh báo. Thầy hoặc phiên Mac xem đề trước buổi dạy. |
| 15 | làm | Màn flash ghi rõ: mạch tăng áp trong máy biến 3 V của pin thành cỡ 300 V để nạp tụ. |
| 16 | làm | Sửa số chỗ trống trong bảng ghi chú cho khớp Tập: ô 1·4 + 1·5 là 7 + 5 = 12 chỗ; ô 2·1 có 10 chỗ; ô 2·3 có 13 chỗ. |
