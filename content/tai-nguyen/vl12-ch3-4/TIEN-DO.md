# Tiến độ PhET — Vật lí 12 ch3–4 (18/10/2026)

Đã ghi DB + deploy + kiểm web 375px (iframe 311px, không tràn): bài id 10, 13, 14, 15 (2 sim), 18.

| Bài (id) | Sim | Đã thử thật | CHƯA thử, thầy bấm thử |
|---|---|---|---|
| 10 | magnet-and-compass | mở sim, thấy điều khiển | kéo la bàn, Đảo cực, Xem bên trong |
| 13 | faradays-law | kéo nam châm vào cuộn, đèn sáng | Volt kế, đảo cực nam châm |
| 14 | generator | mở sim, thấy điều khiển | MỞ VÒI NƯỚC không vận hành được bằng chuột giả lập; đổi số vòng, diện tích, cường độ |
| 15 | rutherford-scattering | bấm bắn hạt alpha, thấy vệt | màn bánh pudding |
| 15 | isotopes-and-atomic-mass | mở màn Hỗn hợp, thấy bảng tuần hoàn | chọn Ne, thêm nguyên tử vào hộp, "Hỗn hợp trong thiên nhiên" |
| 18 | alpha-decay | mở màn Nhiều nguyên tử, thấy Polonium-211 (0,52 s) | thêm 10/100/1 000 hạt, số lượng tối đa |

Video: `prompts-video.md` chờ thầy dán Gemini. Không có sim HTML5: bài 11, 16, 17, 19 (id) — `nuclear-fission` và `radioactive-dating-game` chỉ Java.

## Bổ sung 25/10/2026 (chương 4, đợt riêng)
Thêm 2 khối PhET, chèn thẳng vào `theory.src.html` và `theory.html` (diff chỉ `+`), chưa ghi DB lúc ghi dòng này (xem commit).

| Bài (id) | Sim | Đã thử (mở thật 25/10) | CHƯA thử |
|---|---|---|---|
| 14 Hạt nhân (15), trước mục III | `build-an-atom` (vi) | Màn Nguyên tử: kéo 1 proton → hiện Hydrogen và "Ion+"; thêm 1 rồi 2 neutron → vẫn Hydrogen; bảng tuần hoàn sáng ô H | Kéo electron vào quỹ đạo (chữ trung hoà/ion), hai ô Điện tích và Số khối (bấm bằng chuột giả lập không mở được), màn Ký hiệu, Game |
| 17 Phóng xạ (18), sau khối `alpha-decay` | `beta-decay` (vi) | Màn Một nguyên tử: Carbon-14 (6 p, 8 n, chu kì 5730 năm) → Thêm nguyên tử → phân rã thành Nitrogen-14 (7 p, 7 n), phương trình $^{14}_{6}C \to {}^{14}_{7}N + {}^{0}_{-1}e + \bar\nu$ | Nút Chậm, nút quay lại, các đồng vị Hydrogen-3/Iod-131, hai màn còn lại |

Video mở bài id 16 và 17: `prompts-video.md` mục V7, V8 chờ thầy dán Gemini.
