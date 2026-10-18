# Kế hoạch tài nguyên — đợt 5: KHTN 9 Vật lí, chương 2 Ánh sáng (id 83–88)

Nguồn: bài đã đăng (snapshot 17/10/2026). Không đụng id 89–91 (đã có PhET) và id 129–131 (bản nháp có PhET nằm trong `content/lesson-samples`, DB hiện vẫn là bản ngắn cũ, chờ thầy duyệt đăng theo `docs/memory/project_thachlab_l9_co_hoc_129_131.md`).
Bài 83–87 đã có 2–4 clip YouTube; bài 88 chưa có. Chưa bài nào có PhET. Hình trong bài là SVG tự vẽ.
Sim đã mở thật ngày 18/10/2026 bản `_all.html?locale=vi` (HTTP 200, có tiếng Việt).

## PhET (Claude làm, nhúng `<details>` sau §II)

| # | Bài (id) | Học sinh vướng ở đâu | Sim | Màn / điều khiển đã thấy | Câu dẫn dắt (dự kiến) | Đã thử |
|---|---|---|---|---|---|---|
| 1 | Bài 5 Khúc xạ ánh sáng (83) | Tia bị gãy khúc ở mặt phân cách, góc khúc xạ phụ thuộc gì | `bending-light` | Màn Giới thiệu: laser (bật bằng nút đỏ), chọn Tia/Sóng, hai môi trường (không khí n = 1,00 và nước n = 1,33, đổi vật chất hoặc kéo chiết suất), thước đo góc, ô Pháp tuyến | Tăng góc tới từng bước: góc khúc xạ đổi thế nào? Đổi nước sang thuỷ tinh | Đã bật laser, thấy tia tới, tia phản xạ mờ, tia khúc xạ |
| 2 | Bài 6 Phản xạ toàn phần (84) | Khi nào tia không còn ló ra | `bending-light` | Màn Giới thiệu như dòng 1; đặt môi trường trên có chiết suất lớn hơn môi trường dưới | Cho tia đi từ môi trường chiết quang hơn sang kém hơn, tăng góc tới đến khi tia khúc xạ biến mất: góc đó là bao nhiêu? | Chưa thử đổi môi trường |
| 3 | Bài 7 Lăng kính (85) | Tia lệch và tán sắc qua lăng kính | `bending-light` | Màn Lăng kính: laser, chọn tia đơn sắc hoặc ánh sáng trắng, thanh bước sóng (650 nm), các hình lăng kính/khối thả ra, chọn vật liệu và chiết suất, ô Phản xạ, Pháp tuyến, Thước đo góc | Chiếu ánh sáng trắng qua lăng kính: màu nào lệch nhiều nhất? Đổi bước sóng | Mở màn Lăng kính; chưa kéo lăng kính ra |
| 4 | Bài 8 Thấu kính (86) | Dựng ảnh bằng ba tia đặc biệt, ảnh thật hay ảo | `geometric-optics` | Màn Thấu kính: vật (bút chì, kéo được), thấu kính hội tụ/phân kì, tia Biên/Chính/Nhiều/Không, bán kính cong, chiết suất, đường kính; ô Tiêu điểm (F), Ảnh ảo, Nhãn; màn bên phải hiện ảnh | Kéo vật ra xa rồi lại gần thấu kính hội tụ: ảnh thay đổi thế nào, khi nào ảnh ngược chiều, cùng chiều? | Mở màn Thấu kính; chưa kéo vật |
| 5 | Bài 9 Thực hành đo tiêu cự (87) | Xác định vị trí vật, ảnh để tính tiêu cự | `geometric-optics` | Như dòng 4; có thể đọc khoảng cách vật, ảnh bằng thước trong sim | Đặt vật ở 5 vị trí, ghi khoảng cách vật và ảnh, tính tiêu cự rồi so với giá trị đặt | Như dòng 4 |
| 6 | Bài 10 Kính lúp (88) | Vật đặt trong tiêu cự cho ảnh ảo lớn hơn | `geometric-optics` | Như dòng 4; ô Ảnh ảo | Đặt vật trong khoảng từ thấu kính tới tiêu điểm: ảnh như thế nào? Dịch vật gần hay xa tiêu điểm thì ảnh to hơn? | Như dòng 4 |

Không đề xuất PhET: không có bài nào khác trong phạm vi. Màn Gương của `geometric-optics` và màn Thêm dụng cụ của `bending-light` không dùng.

## Video (Gemini, `prompts-video.md` làm sau khi duyệt)

Chỉ bài 88 chưa có clip (83–87 đã có 2–4 clip mỗi bài).

| # | Bài | Chỗ cần | Học sinh cần quan sát |
|---|---|---|---|
| V1 | Bài 10 Kính lúp (88) | Soi chữ nhỏ bằng kính lúp, đưa kính gần dần | Chữ phóng to, đưa quá xa thì ảnh đảo ngược |
| V2 | Bài 10 Kính lúp (88) | Đo tiêu cự kính lúp bằng ảnh cửa sổ trên giấy | Khoảng cách từ kính tới ảnh rõ nét là tiêu cự |

## Hình (Gemini)
Không đề xuất ảnh mới.

## Cần thầy quyết
1. Duyệt/sửa/bỏ từng dòng PhET (6 dòng, 3 sim) và video (2 dòng).
2. Dòng 2, 3, 5, 6 chưa thao tác thật (chỉ mở sim): giữ và ghi CHƯA thử, hay bỏ?
3. Sau đợt này còn lại HSG (id 153–166, 17 chuyên đề) và các bài Anh văn chuyên ngành: có cần lập kế hoạch không?
