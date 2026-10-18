# Kế hoạch tài nguyên — Vật lí 12, Chương 3 (Từ trường) và Chương 4 (Vật lí hạt nhân), đợt 2

Nguồn: bài đã đăng (id 10–19, snapshot 17/10/2026). Cả 10 bài hiện: 0 PhET, 0 video, 0 ảnh (bài 12 [id 12] có 2 clip YouTube đã nhúng; giữ nguyên). Hình trong bài đều là SVG tự vẽ.
Ngoài đợt này (chương 3 còn id 125–127, bài 14–16) đã có 5 clip ở id 126; chưa xét.
Sim đã mở thật ngày 18/10/2026 trên bản `_all.html?locale=vi` (HTTP 200, có tiếng Việt). Mốc kiểm: đã thao tác thử thế nào ghi ở cột cuối.
Không có sim HTML5 cho: lực từ lên dây (bài 10), năng lượng liên kết (bài 15), phân hạch (bài 16, `nuclear-fission` chỉ có bản Java, URL iframe 404), an toàn phóng xạ (bài 18), `radioactive-dating-game` cũng chỉ Java.

## PhET (Claude làm, nhúng trong `<details>` sau §II)

| # | Bài (id) | Học sinh vướng ở đâu | Sim | Màn / điều khiển đã thấy | Câu dẫn dắt (dự kiến) | Đã thử |
|---|---|---|---|---|---|---|
| 1 | 9 Khái niệm từ trường (10) | Hình dung đường sức và hướng kim la bàn quanh nam châm | `magnet-and-compass` | Nam châm thẳng; ô La bàn, Từ trường (B), Xem bên trong, Trái đất, Đảo cực, Trường kế; thanh Cường độ | Đặt la bàn các chỗ quanh nam châm: kim chỉ hướng nào? Đảo cực thì sao? | Mở, thấy điều khiển; chưa kéo la bàn |
| 2 | 12 Cảm ứng điện từ (13) | Vì sao đèn sáng khi nam châm chuyển động qua cuộn dây | `faradays-law` | Cuộn dây nối bóng đèn, nam châm kéo thả; ô Volt kế, Trường tuyến; chọn cuộn 2 loại; nút Đảo cực | Giữ nam châm đứng yên trong cuộn rồi đẩy vào/ra nhanh chậm: đèn thế nào? | Đã kéo nam châm vào cuộn, đèn sáng hơn |
| 3 | 13 Dòng điện xoay chiều (14) | Từ khung quay ra suất điện động biến thiên | `generator` | Vòi nước + bánh xe quay nam châm (hiện RPM), cuộn dây (đổi số vòng, diện tích), bóng đèn/vôn kế, ô Electrons, La bàn | Tăng số vòng, diện tích vòng, tốc độ quay: số chỉ thay đổi thế nào? | Mở, thấy điều khiển; vòi nước KHÔNG vận hành được bằng chuột giả lập, bước Thử cần thầy bấm thử (ghi "CHƯA thử") |
| 4 | 14 Hạt nhân, mô hình nguyên tử (15) | "Bắn bi mù" và vì sao hạt nhân nhỏ, đặc | `rutherford-scattering` | Màn Mẫu nguyên tử Rutherford: nút đỏ Hạt Alpha, thanh Năng lượng, ô Hiển thị quỹ đạo, chọn số proton/neutron; có thêm màn Bánh pudding | Bắn alpha vào mẫu Rutherford rồi mẫu bánh pudding: hạt bị lệch khác nhau thế nào? | Đã bấm bắn, thấy vệt hạt |
| 5 | 14 Hạt nhân, mô hình nguyên tử (15) | Đồng vị và nguyên tử khối trung bình (neon 20,18) | `isotopes-and-atomic-mass` | Màn Hỗn hợp: bảng tuần hoàn chọn nguyên tố, rổ đồng vị kéo thả, ô Hỗn hợp của tôi / trong thiên nhiên, thang nguyên tử khối trung bình | Chọn neon, chọn "Hỗn hợp trong thiên nhiên": khối lượng trung bình nằm gần đồng vị nào? | Mở màn Hỗn hợp, chưa kéo rổ |
| 6 | 17 Hiện tượng phóng xạ (18) | Chu kì bán rã, tính ngẫu nhiên của từng hạt nhân | `alpha-decay` | Màn Nhiều nguyên tử: Polonium-211 (chu kì 0,52 s), nút thêm hạt nhân, ô số lượng, trục thời gian, Stopwatch, Đồng vị "Điều chỉnh"; màn Tốc độ phân rã | Thêm 10 hạt nhân: sau đúng một chu kì bán rã còn lại bao nhiêu? Thử với 100 hạt | Mở màn Nhiều nguyên tử, chưa bấm thêm hạt |

Bài 10, 11, 15, 16, 18, 19 không có PhET (xem trên). Bài 11 (thực hành đo cảm ứng từ, id 12) giữ nguyên.

## Video (tìm cho thầy dán Gemini, `prompts-video.md` làm sau khi duyệt dòng)

| # | Bài | Chỗ cần | Học sinh cần quan sát |
|---|---|---|---|
| V1 | 9 | Dòng điện làm lệch kim la bàn (Oersted) | Kim lệch khi bật dòng, về chỗ cũ khi tắt |
| V2 | 9 | Mạt sắt quanh nam châm | Đường sức hiện thành các đường cong từ cực này sang cực kia |
| V3 | 10 | Khung/dây có dòng điện trong từ trường (động cơ đơn giản) | Khung quay, đảo chiều dòng thì đảo chiều quay |
| V4 | 12 | Nam châm rơi chậm trong ống nhôm (đã có clip ở id 13, tra trước khi tìm) | Rơi chậm hơn nam châm rơi tự do |
| V5 | 17 | Máy đếm Geiger/buồng sương phát hiện tia | Số đếm nhảy ngẫu nhiên, không đều |
| V6 | 18 | Ba tấm chắn giấy, nhôm, chì | Tia nào bị tấm nào chặn |

## Hình (Gemini)
Không đề xuất ảnh mới: mọi hình cần số liệu/ký hiệu đã là SVG; ảnh đời sống không bắt buộc ở đợt này.

## Cần thầy quyết
1. Duyệt/sửa/bỏ từng dòng PhET (6 dòng), video (6 dòng).
2. Dòng 3 (`generator`): giữ, hay bỏ vì tôi không vận hành được vòi nước? (thầy bấm thử là đủ)
3. Bài 4 hạt nhân: có muốn chèn màn Bánh pudding cho đối chiếu không (đang để chung dòng 4).
