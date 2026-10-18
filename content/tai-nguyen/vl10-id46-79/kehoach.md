# Kế hoạch tài nguyên — đợt 4: Vật lí 10 (id 46–79, trừ id 58, 59, 60, 63, 66 đã có PhET)

Nguồn: bài đã đăng (snapshot 17/10/2026). 29 bài xét; chưa bài nào có PhET; chỉ id 57 có 1 clip YouTube (giữ nguyên). Hình trong bài là SVG tự vẽ.
Sim đã mở thật ngày 18/10/2026 bản `_all.html?locale=vi` (HTTP 200, có tiếng Việt).
Không có sim HTML5 khớp (URL 404): chuyển động thẳng (`moving-man`), chuyển động tròn (`ladybug-*`), nên các bài động học 49–56, chuyển động tròn 76–77 không có PhET.

## PhET (Claude làm, nhúng `<details>` sau §II)

| # | Bài (id) | Học sinh vướng ở đâu | Sim | Màn / điều khiển đã thấy | Câu dẫn dắt (dự kiến) | Đã thử |
|---|---|---|---|---|---|---|
| 1 | 3 Tính sai số (48) | Vì sao 5 lần đo chu kì cho 5 số khác nhau | `pendulum-lab` | Màn Giới thiệu: chiều dài, khối lượng, Đồng hồ, Đánh dấu chu kỳ | Đo 10 dao động 5 lần: các lần khác nhau thế nào, lấy giá trị nào? | Mở màn Giới thiệu (đợt 3); chưa thả |
| 2 | 12 Chuyển động ném (57) | Quỹ đạo ném ngang là parabola | `projectile-motion` | Màn Giới thiệu: pháo trên tháp 10 m, tốc độ ban đầu (15 m/s), nút bắn, ô Vector vận tốc/gia tốc, Sức cản không khí; có thêm Vector, Lực cản, Lab | Bắn ngang rồi đổi tốc độ: tầm xa và thời gian rơi thay đổi thế nào? | Đã bắn, thấy quỹ đạo parabola |
| 3 | 19 Lực cản và lực nâng (64) | Không khí cản chuyển động thế nào | `projectile-motion` | Màn Lực cản (thấy tên, chưa mở) | Bắn cùng tốc độ khi có và không có lực cản: quỹ đạo khác thế nào? | Chưa mở màn Lực cản |
| 4 | 22 Thực hành tổng hợp lực (67) | Tổng hợp hai lực theo quy tắc hình bình hành | `vector-addition` | Màn 2 chiều: kéo vector a, b, c ra lưới; ô Tổng, Độ dài, góc θ, Thành phần | Kéo hai vector, ô Tổng cho độ dài và góc: đổi góc giữa hai vector thì tổng đổi sao? | Mở màn 2 chiều; chưa kéo vector |
| 5 | 25 Động năng, thế năng (70) | Chuyển hoá động năng–thế năng | `energy-skate-park-basics` | Màn Giới thiệu: đường trượt hình chữ U, nhân vật, thanh Khối lượng, bảng Năng lượng, Biểu đồ tròn, Lưới, Tốc độ | Thả nhân vật từ các độ cao: ở đáy tốc độ ra sao, cột động năng/thế năng thế nào? | Mở màn Giới thiệu; chưa thả |
| 6 | 26 Cơ năng bảo toàn (71) | Khi nào cơ năng bảo toàn | `energy-skate-park-basics` | Màn Ma sát (thấy tên, chưa mở) | Thả khi có và không có ma sát: tổng cơ năng thay đổi thế nào? | Chưa mở màn Ma sát |
| 7 | 28 Động lượng (73) | Động lượng $p = mv$ | `collision-lab` | Màn Phần giới thiệu (thấy tên, chưa mở): bóng va chạm, vận tốc, động lượng | Đổi khối lượng và vận tốc hai bóng: động lượng mỗi bóng thế nào? | Chưa mở màn Giới thiệu |
| 8 | 29 Bảo toàn động lượng (74) | Va chạm mềm: tổng động lượng trước, sau | `collision-lab` | Màn Không đàn hồi: hai khối lượng chỉnh được, ô Vận tốc, Động lượng, Động năng, nút Dính, Giản đồ động lượng | Chọn Dính, so tổng động lượng trước và sau va chạm; động năng thì sao? | Mở màn Không đàn hồi; chưa chạy |
| 9 | 33 Biến dạng vật rắn (78) | Lực đàn hồi tỉ lệ độ dãn | `hookes-law` | Màn Phần giới thiệu: hệ số đàn hồi 200 N/m (100–1000), lực tác dụng −100…100 N, ô Lực đàn hồi, Độ biến dạng, Vị trí cân bằng | Tăng lực tác dụng từng bước: độ biến dạng thay đổi thế nào? Đổi hệ số đàn hồi | Mở; chưa kéo |
| 10 | 34 KLR, áp suất chất lỏng (79) | Khối lượng riêng của vật liệu | `density` | Màn Phần giới thiệu: chọn vật liệu (Gỗ), thanh Khối lượng, Thể tích; thang so sánh "Mật độ" (kg/L); có màn So sánh, Bí mật | Gỗ thả vào nước: nổi hay chìm? Đổi khối lượng giữ thể tích: tỉ số m/V đổi không? (sim gọi là "Mật độ") | Mở màn Giới thiệu; chưa đổi |
| 11 | 34 KLR, áp suất chất lỏng (79) | Áp suất tăng theo độ sâu | `under-pressure` | Màn Áp suất: áp kế kéo được, thước, Khí quyển Có/Không, đơn vị SI, thanh Mật độ chất lỏng (1000 kg/m³: nước), thanh Trọng lực | Nhúng đầu dò xuống sâu dần: áp suất tăng thế nào? Đổi chất lỏng sang xăng/mật | Mở; chưa nhúng |

Không đề xuất PhET: id 46, 47, 49–56, 61, 62, 65, 68, 69, 72, 75, 76, 77 (không sim HTML5 khớp, hoặc trùng sim đã có ở id 58–66).

## Video (Gemini, `prompts-video.md` làm sau khi duyệt)

| # | Bài | Chỗ cần | Học sinh cần quan sát |
|---|---|---|---|
| V1 | id 46 | Giọt mực trong nước nóng và nước lạnh | Mực lan nhanh trong nước nóng |
| V2 | id 55 | Rơi tự do: ống Newton hoặc búa và lông chim trong chân không | Trong chân không mọi vật rơi như nhau |
| V3 | id 64 | Phễu giấy hoặc người nhảy dù rơi | Lực cản không khí làm vật rơi chậm lại |
| V4 | id 74 | Va chạm trên ray đệm khí | Tổng vận tốc/động lượng trước và sau |
| V5 | id 77 | Nút cao su quay trên đầu ống, hoặc đồng xu trên bàn xoay | Vật văng ra khi lực hướng tâm không đủ |
| V6 | id 79 | Chai nhựa đục lỗ ở ba độ cao | Nước phun xa hơn ở lỗ thấp |

## Hình (Gemini)
Không đề xuất ảnh mới.

## Cần thầy quyết
1. Duyệt/sửa/bỏ từng dòng PhET (11 dòng, 8 sim) và video (6 dòng).
2. Dòng 3, 6, 7 dùng màn chưa mở thử (Lực cản, Ma sát, Phần giới thiệu): giữ và ghi CHƯA thử, hay bỏ?
3. Dòng 10: sim ghi "Mật độ" thay cho "khối lượng riêng"; bước Thử sẽ giải thích hai tên là một. Đồng ý chứ?
