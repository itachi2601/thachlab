# Kế hoạch tài nguyên — đợt 6: khoá HSG KHTN 9 Vật lí (id 150–166)

Nguồn: bài đã đăng (snapshot 17/10/2026). 17 chuyên đề trong DB (CĐ17 Thiên văn chưa đăng). Đã có PhET, không đụng: id 157 (CĐ04), 159 (CĐ03), 165 (CĐ05). Chưa chuyên đề nào có clip YouTube. Nguồn gốc ở `content/hsg9/cd*/theory.src.html`.
Bài viết HSG có cấu trúc tiêu đề khác bài lớp 10–12 (I. Mở bài, II… nhiều mục): chỗ đặt khối PhET chọn sau khi duyệt (mặc định: cuối mục kiến thức liên quan).
Sim đã mở thật ngày 18/10/2026 bản `_all.html?locale=vi` (HTTP 200, có tiếng Việt).
Không đề xuất PhET: id 160 (CĐ00 kỹ năng nền), 161 (CĐ01 công, công suất), 162 (CĐ13 chuyển động, đồ thị; `moving-man` 404), 164 (CĐ16 truyền nhiệt, sự nở vì nhiệt; chưa có sim đã mở khớp).

## PhET (Claude làm, nhúng `<details>`)

| # | Chuyên đề (id) | Học sinh vướng ở đâu | Sim | Màn / điều khiển đã thấy | Câu dẫn dắt (dự kiến) | Đã thử |
|---|---|---|---|---|---|---|
| 1 | CĐ15 Âm thanh (150) | Tần số, biên độ và độ cao, độ to | `sound-waves` | Màn Phần giới thiệu: loa, thanh Tần số (550 Hz), thanh Biên độ, ô Nghe âm thanh | Tăng tần số rồi biên độ: sóng thay đổi thế nào, âm nghe cao hơn hay to hơn? | Mở màn Giới thiệu; chưa kéo thanh |
| 2 | CĐ06 Khúc xạ (151) | Góc khúc xạ, chiết suất | `bending-light` | Màn Giới thiệu: laser, hai môi trường (không khí 1,00, nước 1,33), thước đo góc, Pháp tuyến | Đổi chiết suất môi trường dưới: góc khúc xạ đổi thế nào? | Đã bật laser, thấy tia tới, phản xạ, khúc xạ |
| 3 | CĐ06 Khúc xạ (151) | Lăng kính, tán sắc | `bending-light` | Màn Lăng kính: lăng kính kéo ra, ánh sáng trắng/đơn sắc, thanh bước sóng | Chiếu ánh sáng trắng qua lăng kính: màu nào lệch nhiều nhất? | Mở màn; chưa kéo lăng kính ra |
| 4 | CĐ08 Cảm ứng điện từ (152) | Vì sao đèn sáng khi nam châm chuyển động qua cuộn | `faradays-law` | Cuộn dây nối đèn, nam châm kéo thả, ô Volt kế, Trường tuyến, nút đảo cực | Giữ nam châm yên rồi đẩy vào/ra nhanh chậm: đèn thế nào? | Đã kéo nam châm vào cuộn, đèn sáng hơn |
| 5 | CĐ12 Nhiệt học (153) | Nhiệt dung riêng, cân bằng nhiệt | `energy-forms-and-changes` | Màn Phần giới thiệu: Sắt, Gạch, Nước, Dầu Olive, hai bếp (thanh Nóng–Mát), nhiệt kế, ô Biểu tượng năng lượng | Đun các vật cùng lúc, cùng mức bếp: vật nào nóng lên nhanh nhất? | Mở màn; chưa đun |
| 6 | CĐ11 Cơ học chất lưu (154) | Lực đẩy Archimedes, vì sao vật nổi, chìm | `buoyancy` | Màn So sánh: hai khối cùng khối lượng/thể tích/mật độ, ô Lực (trọng lực, lực nổi, lực tiếp xúc), thanh Lưu chất (nước) | Thả hai khối cùng khối lượng, khác thể tích: lực nổi và độ nổi chìm thế nào? | Mở màn So sánh; chưa thả |
| 7 | CĐ11 Cơ học chất lưu (154) | Áp suất chất lỏng theo độ sâu | `under-pressure` | Màn Áp suất: áp kế kéo được, thước, Khí quyển Có/Không, thanh Mật độ chất lỏng, thanh Trọng lực | Nhúng áp kế xuống sâu dần, đổi chất lỏng: áp suất thay đổi thế nào? | Mở; chưa nhúng |
| 8 | CĐ10 Lực (155) | Tổng hợp hai lực vuông góc | `vector-addition` | Màn 2 chiều: vector a, b, c, ô Tổng, Độ dài, góc θ | Kéo hai vector vuông góc: tổng dài bao nhiêu? Đổi góc | Mở màn 2 chiều; chưa kéo |
| 9 | CĐ10 Lực (155) | Lực đàn hồi tỉ lệ với độ dãn | `hookes-law` | Màn Phần giới thiệu: hệ số đàn hồi (200 N/m), lực tác dụng ±100 N, ô Lực đàn hồi, Độ biến dạng | Tăng lực tác dụng từng bước: độ giãn đổi thế nào? | Mở; chưa kéo |
| 10 | CĐ07 Thấu kính (156) | Dựng ảnh bằng ba tia | `geometric-optics` | Màn Thấu kính: vật bút chì kéo được, tia Biên/Chính/Nhiều, ô Tiêu điểm (F), Ảnh ảo, bán kính cong, chiết suất, đường kính | Kéo vật qua các vùng so với tiêu cự: ảnh thật/ảo, lớn/nhỏ ra sao? | Mở màn; chưa kéo vật |
| 11 | CĐ14 Gương phẳng (158) | Ảnh ảo qua gương, định luật phản xạ | `geometric-optics` | Màn Gương: ba kiểu gương (chọn bằng biểu tượng), vật, ô Ảnh ảo, Tiêu điểm | Chọn gương phẳng, đặt vật ở các khoảng cách khác nhau: ảnh ở đâu? | Mở màn Gương; chưa chọn gương phẳng |
| 12 | CĐ09 Năng lượng với cuộc sống (163) | Các dạng và chuyển hoá năng lượng | `energy-forms-and-changes` | Màn Hệ thống (thấy tên, chưa mở) | Chạy hệ thống nước–tua bin–bóng đèn: năng lượng đi qua những dạng nào? | Chưa mở màn Hệ thống |
| 13 | CĐ02 Động năng, thế năng, cơ năng (166) | Bảo toàn cơ năng, ma sát | `energy-skate-park-basics` | Màn Giới thiệu: đường trượt, nhân vật, bảng Năng lượng, Biểu đồ tròn, Lưới, Tốc độ | Thả từ các độ cao: động năng, thế năng, cơ năng ở đỉnh, đáy ra sao? | Mở màn Giới thiệu; chưa thả |

## Video (Gemini, `prompts-video.md` làm sau khi duyệt)

| # | Chuyên đề | Chỗ cần | Học sinh cần quan sát |
|---|---|---|---|
| V1 | CĐ15 (150) | Âm thoa chạm mặt nước | Nước bắn toé, mặt nước gợn khi âm thoa rung |
| V2 | CĐ11 (154) | Cốc úp, tấm nhựa không rơi (áp suất khí quyển) | Tấm nhựa giữ nước, không rơi khi úp ngược |
| V3 | CĐ14 (158) | Vùng tối và nửa tối bằng đèn và vật chắn | Bóng đổi kích thước khi nguồn sáng lớn |
| V4 | CĐ16 (164) | Ba que kim loại gắn đinh bằng sáp, đun một đầu | Đinh rụng theo thứ tự theo độ dẫn nhiệt |
| V5 | CĐ16 (164) | Nở vì nhiệt: bi sắt qua vòng, hơ nóng bi | Bi nở không lọt qua vòng, nguội lại lọt |
| V6 | CĐ10 (155) | Kéo khối gỗ bằng lực kế trên các bề mặt | Lực kế chỉ khi khối bắt đầu trượt, khi chuyển động đều |

## Hình (Gemini)
Không đề xuất ảnh mới.

## Cần thầy quyết
1. Duyệt/sửa/bỏ từng dòng PhET (13 dòng, 11 sim) và video (6 dòng).
2. Dòng 5, 12 và 11 dùng màn chưa thao tác (Hệ thống, chọn gương phẳng): giữ và ghi CHƯA thử, hay bỏ?
3. Bài HSG khó hơn lớp 9 thường: bước Thử chỉ làm "khám phá và dự đoán", không thay phần tự luận nâng cao. Đồng ý?
4. Bản nguồn trong `content/hsg9/` có thể đã lệch DB (thầy sửa trên web); tôi sẽ so từng bài trước khi chèn, bài nào lệch thì dừng hỏi.
