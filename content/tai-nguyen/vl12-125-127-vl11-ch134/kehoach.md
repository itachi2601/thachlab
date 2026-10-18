# Kế hoạch tài nguyên — đợt 3: Vật lí 12 (id 125–127) + Vật lí 11 chương 1 (id 20–26), chương 3 (id 35–40), chương 4 (id 41–45)

Nguồn: bài đã đăng (snapshot 17/10/2026). 21 bài; chưa bài nào có PhET; chỉ id 126 đã có 5 clip YouTube (giữ nguyên). Chương 2 của lớp 11 đã có PhET (bỏ qua).
Sim đã mở thật ngày 18/10/2026 bản `_all.html?locale=vi` (HTTP 200, có tiếng Việt). Không có sim HTML5 cho: cộng hưởng (`resonance` 404), điện trường đều giữa hai bản phẳng, sóng điện từ (`radio-waves` 404), máy biến áp.

## PhET (Claude làm, nhúng `<details>` sau §II)

| # | Bài (id) | Học sinh vướng ở đâu | Sim | Màn / điều khiển đã thấy | Câu dẫn dắt (dự kiến) | Đã thử |
|---|---|---|---|---|---|---|
| 1 | L11 Bài 1 Dao động điều hoà (20) | Thấy vật lò xo dao động, chu kì phụ thuộc gì | `masses-and-springs` | Màn Giới thiệu: 2 lò xo, chỉnh hằng số lò xo, các quả cân 50/100/250 g, đồng hồ, trọng lực; có thêm Vector, Năng lượng, Lab | Treo quả nặng khác nhau, kéo xuống thả ra: chu kì đổi thế nào? | Mở màn Giới thiệu; chưa treo quả |
| 2 | L11 Bài 2 Mô tả dao động (21) | Chu kì, tần số, đo bằng đồng hồ | `pendulum-lab` | Màn Giới thiệu: chiều dài 0,1–1 m, khối lượng, trọng lực, ma sát; ô Thước, Đồng hồ, Đánh dấu chu kì | Đổi chiều dài rồi đo chu kì: khối lượng có ảnh hưởng không? | Mở màn Giới thiệu; chưa thả con lắc |
| 3 | L11 Bài 5 Động năng, thế năng DĐĐH (24) | Chuyển hoá động năng–thế năng | `pendulum-lab` | Màn Năng lượng (thấy tên màn, chưa mở) | Ở vị trí nào động năng lớn nhất? | Chưa mở màn Năng lượng |
| 4 | L11 Bài 6 Tắt dần, cộng hưởng (25) | Dao động tắt dần khi có ma sát | `pendulum-lab` | Màn Giới thiệu: thanh trượt Ma sát | Tăng ma sát: biên độ giảm nhanh hay chậm? (phần cộng hưởng không có sim) | Chưa kéo thanh Ma sát |
| 5 | L11 Bài 16 Lực giữa hai điện tích (35) | Lực phụ thuộc điện tích và khoảng cách | `coulombs-law` | Màn Thang đo vĩ mô: Điện tích 1, 2 (−10…10 µC), thước, ô Cường độ lực | Đổi khoảng cách rồi đổi điện tích: lực đổi thế nào? | Mở, thấy lực ≈319 N ở −4 µC và 8 µC; chưa thay đổi |
| 6 | L11 Bài 17 Khái niệm điện trường (36) | Hình dung điện trường quanh điện tích | `charges-and-fields` | Một màn: kéo điện tích +1 nC/−1 nC/đầu đo vào sân; ô Điện trường, Chỉ hiển thị hướng, Hiệu thế, Trị số, Lưới; vôn kế, thước | Đặt một điện tích dương: các mũi tên chỉ đi đâu? Thêm điện tích âm? | Mở, thấy điều khiển; chưa kéo điện tích |
| 7 | L11 Bài 20 Điện thế (39) | Điện thế, hiệu điện thế | `charges-and-fields` | Ô Hiệu thế và vôn kế | Đặt hai điện tích, dùng vôn kế đo hiệu thế giữa hai điểm | Chưa thử vôn kế |
| 8 | L11 Bài 21 Tụ điện (40) | Điện dung phụ thuộc diện tích, khoảng cách | `capacitor-lab-basics` | Màn Điện dung: pin, hai bản tụ, kéo khoảng cách, diện tích đối diện; ô Điện dung (pF), Điện tích bản trên, Năng lượng tích luỹ | Tăng diện tích bản: điện dung đổi thế nào? Giảm khoảng cách? | Mở, thấy 0,30 pF; chưa đổi |
| 9 | L11 Bài 22 Cường độ dòng điện (41) | Đặt ampe kế, dòng ở đâu cũng bằng nhau | `circuit-construction-kit-dc` | Màn Giới thiệu: dây nối, pin, đèn tròn, điện trở, công tắc; Volt kế, Ampere kế; hiển thị dòng electron/quy ước | Dựng mạch pin–đèn, đặt ampe kế ở hai chỗ khác nhau: hai số chỉ ra sao? | Mở; chưa dựng mạch |
| 10 | L11 Bài 23 Điện trở, Ohm (42) | I tỉ lệ thuận U, nghịch R | `ohms-law` | Một màn: thanh trượt Hiệu thế V (4,5 V) và Điện trở R (500 Ω), hiện cường độ (9,0 mA) | Tăng V giữ nguyên R rồi ngược lại: I đổi thế nào? | Mở, thấy 9,0 mA ở 4,5 V và 500 Ω; chưa kéo |
| 11 | L11 Bài 24 Nguồn điện (43) | Hiệu điện thế hai cực tụt khi dòng tăng (điện trở trong) | `circuit-construction-kit-dc` | Màn Lab, mục Cao cấp: thanh Điện trở trong (đến 10 Ω), Điện trở dây nối; Volt kế | Tăng điện trở trong, bật thêm tải: số chỉ vôn kế ở hai cực pin đổi thế nào? | Mở màn Lab, thấy thanh Điện trở trong; chưa dựng mạch |
| 12 | L11 Bài 26 Thực hành đo suất điện động, điện trở trong (45) | Hình dung phép đo ε và r | `circuit-construction-kit-dc` | Như dòng 11 | Dựng mạch như sơ đồ thực hành, đo U–I ở vài tải rồi tìm ε và r | Như dòng 11 |

Không đề xuất PhET: L12 id 125 (đã nhúng `generator` ở id 14), 126 (đã có 5 clip), 127 (không có sim); L11 id 22, 23, 26, 37, 38, 44.

## Video (Gemini, `prompts-video.md` làm sau khi duyệt)

| # | Bài | Chỗ cần | Học sinh cần quan sát |
|---|---|---|---|
| V1 | L11 id 25 | Cộng hưởng: xích đu hoặc cây cầu rung, ly rượu vỡ | Biên độ lớn khi kích thích đúng tần số riêng |
| V2 | L11 id 35 | Thước nhựa cọ vải hút giấy vụn | Hút rồi bật ra khi chạm |
| V3 | L11 id 37 | Điện phổ: hạt bột trong dầu giữa hai điện cực | Hạt xếp thành đường dọc theo đường sức |
| V4 | L11 id 40 | Tụ nạp rồi xả qua LED | LED sáng rồi tắt dần |
| V5 | L12 id 125 | Máy biến áp tự quấn đo hai điện áp | Điện áp ra tỉ lệ với số vòng |
| V6 | L12 id 127 | Sóng điện từ lan truyền (mô hình điện trường, từ trường vuông góc) | Hai trường dao động vuông góc nhau và vuông góc phương truyền |

## Hình (Gemini)
Không đề xuất ảnh mới.

## Cần thầy quyết
1. Duyệt/sửa/bỏ từng dòng PhET (12 dòng, 8 sim) và video (6 dòng).
2. Dòng 3 và 4 dùng màn của `pendulum-lab` chưa mở thử (Năng lượng, ma sát): giữ và để thầy bấm thử, hay bỏ?
3. L11 id 24 trong tên là Bài 5; id 25 là Bài 6 (có phần cộng hưởng không có sim): giữ dòng 4 chỉ cho phần tắt dần?
