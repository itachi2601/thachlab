# Lỗi và điểm chưa nhất quán trong bản gốc — dịch đúng bản gốc, chú thích, không tự sửa

| # | File | Nguyên văn | Vấn đề | Cách xử lý khi dịch |
|---|---|---|---|---|
| 1 | skill_sets_pre (tr. 3) | "Aluminum 6160 T6" | Mác đúng là 6061-T6 (link đi kèm cũng dẫn tới 6061) | Dịch "nhôm 6160 T6 [Ghi chú dịch: đúng là 6061-T6]" |
| 2 | skill_sets_pre (tr. 3) | "Acetyl (Delrin)" | Đúng là Acetal (POM) | Chú thích |
| 3 | skill_sets_pre | ±0.025 mm, positional ±0.01 mm | Thang điểm thật dùng lắp ghép ISO (85 f8, 20 H8, 12 H8, M24×3 6g) và ±0.15 / ±0.3 cho kích thước khác; chỉ tâm lỗ 75 là ±0.01 | Khi dịch skill sets ghi chú "đã bị thang điểm thật thay thế" |
| 4 | marking_scheme B1 | "498 to 502mm = 0.35 marks, smaller than 498 or above **500**mm = 0 marks" | Lỗi đánh máy, phải là 502 | Dịch nguyên, chú thích |
| 5 | marking_scheme C3 | "M4 x .07 tapped holes" | Đúng là M4×0.7 | Chú thích |
| 6 | marking_scheme C1 | "85 dia f8: Above 84.910 or below 84.964 = zero" | Viết ngược (trên 84.964 hoặc dưới 84.910 = 0); miền đúng 84.910–84.964 | Chú thích |
| 7 | marking_scheme, sheet WSOS | Installations 40, Problem solving 10 | TD ghi 35 và 15; TD mục 2.1 cho phép lệch ≤5% | Ghi chú ở bản dịch TD mục 2.2 |
| 8 | marking_scheme A | "measurent", "Alignement", "Sin Off", "Tigntened", "approperiately", "routered" | Lỗi chính tả tiếng Anh | Bỏ qua, dịch theo nghĩa |
| 9 | MA2 | "Fault's 1, 2, and 3" | Lỗi dấu nháy | Bỏ qua |
| 10 | Pneumatics Build | Rev 11: đổi từ mã 2 chữ sang 3 chữ (EN IEC 81346-2:2019) | Tài liệu phân tích tiếng Việt cũ còn dùng "A+, B+"; đề thật dùng MM1+, MM2+… | Dùng MM1…MM4 trong mọi bản dịch |
| 11 | Industrial_Mechanics_WorldSkills_2026.pdf (bản phân tích VN có sẵn) | Dựa trên skill sets pre-release | Lỗi thời: sai dung sai (xem #3), coi A2 là sửa lỗi mạch vật lý (thực tế trên FluidSIM), chưa biết bộ dụng cụ Module A, chưa có trọng số điểm | Không dùng làm nguồn; chỉ tham khảo cách diễn đạt |
| 12 | TD 1.1.2 | "adaptiable" | Lỗi chính tả | Bỏ qua |
| 13 | Milling machine info | Dịch máy từ tiếng Trung ("defrosting pan", "6-inch flat pliers" = ê-tô 6 inch, "58 combination pressing plates" = bộ 58 chi tiết kẹp) | Không dịch nguyên, chỉ tóm tắt thông số | Bậc 3 |
| 14 | Drawings | Ngày "Date: 26_08_2026" và "JANUARY 2026" trộn; "Dwg No: XX of XX" chưa điền | Không ảnh hưởng kỹ thuật | Bỏ qua |
| 15 | Drawings 201–207 pre-release vs `WSC2026_TP01_CA_200_EN` thật | 201 = 350, 202 = 350, 205 = 310, 206 = 450 (pre) | Bản thật: 201 = 300, 202 = 300, 205 = 275, 206 = 375 | Dùng bản thật; ghi chú ở 03 và 06 |
| 16 | Drawings 401, 404, 405 ghi chú 3 | "TOLERANCE CLASS IS m (MEDIUM) ISO2768-1fk" | Chữ m (medium) mâu thuẫn với ký hiệu f (fine) K | Dịch nguyên, chú thích; luyện theo ±0.15/±0.3 của thang điểm |
| 17 | BOM bản vẽ 400 | Item 1 "401 DIE BLOCK" và item 12 "401 STROKE POSITIONING SCREW"; item 2 "402 CLAMP" và item 7 "402 SPACER" | Trùng mã chi tiết; vít định vị hành trình là Detail 405 theo bản vẽ chi tiết | Chú thích trong 06; bản dịch dùng 405 cho vít |
| 18 | BOM 300, thang điểm D2, bản vẽ pre-release 303–305 | BOM 300 "304 + 305 BENDING PUNCH"; D2 "304 bending wiper left / 305 right"; pre-release: 303 + 304 acetal là má uốn, 305 steel là khối định vị (lỗ Ø24.5) | Số hiệu má uốn không nhất quán | Dịch nguyên theo từng nguồn, chú thích trong 06 và CSV |
| 19 | Pneumatics Build tờ 4 vs tờ 1 / đề A2 / thang điểm F1 | Xi lanh ghi -MMB1…-MMB4 (tờ 4) nhưng chuỗi ghi MM1…MM4 | Cùng phần tử, khác độ dài mã (rev 13) | Dùng MM1…MM4 cho chuỗi, -MMB khi tra bảng linh kiện |
