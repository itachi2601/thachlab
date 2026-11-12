# Rà soát clip thí nghiệm tự dựng — 11/11/2026

Phạm vi: 105 clip thí nghiệm trong `scripts/video-thi-nghiem/clips/` (không tính 5 clip `bay-ch3-*` và `on-ch3-l12`).
Cách rà: (1) ba cổng tự động trên cả 105 clip (`render.py --kich-ban`, `--do-chu`, `xuat-khung.py --kiem`);
(2) soát mắt 8 clip mẫu chưa từng qua cổng mp4, bằng khung 375 px dựng từ mã hiện tại
(`khung-375.py`), agent `kiem-code` đóng vai học sinh. Chưa sửa clip nào.

## 1. Cổng tự động (105 clip)

- Phụ đề quá 8 từ / 2 dòng: không clip nào.
- Mật độ chữ cả clip > 200 từ/phút: chuyenthe 205, dttruong2 204, hatnhan1 209, hatnhan2 211, mayphat1 202, thangnhietdo4 207 (vượt nhẹ); **thuchanhtu4 285** (bản 2 ngày 11/11).
- Có một cảnh > 260 từ/phút: apsuat1, apsuat2, boyle, camungdt.
- Dài hơn 50 s (17 clip L12, 51–54 s): apsuat1, antoanpx1, apsuat2, boyle, chuyenthe, camungdt3, camungdt, hatnhan1, dttruong2, hatnhan2, mayphat1, nllk1, mayphat3, thuchanh2, thangnhietdo4, phongxa2, tutruong4, xoaychieu3. (hatnhan3 63 s là cố ý.)
- JSON khung vi phạm K3 (ô chữ dài hơn thời gian đọc) — 19 clip, đều L12: antoanpx1, apsuat2, boyle, camungdt, camungdt3, chuyenthe, dttruong2, hatnhan1, mayphat1, mayphat3, nllk1, phongxa2, pttrangthai2, thangnhietdo1, thangnhietdo4, thuchanh2, tutruong4, udcamung2, xoaychieu3. Nặng nhất: xoaychieu3 (41 từ / 4,4 s), pttrangthai2 (67 từ / 8,5 s), dttruong2 (43 từ / 6,1 s).
- **thuchanhtu4**: JSON khung `tong_giay` 48,1 s lệch engine 49,9 s → điểm dừng sai nếu tải bản 2 mà không xuất lại khung.
- K5 (có số % trong ô, cần đối chiếu kho): conang1, congsuat1, dongluong1, hatnhan2, thuchanhdl3.
- Kho: `tn-l12-boylecharles-01.json` còn mâu thuẫn 5 % (dòng 25, 66) và 8 % (dòng 59, 174); `tn-l12-tutruong-04.json` ghi nam châm trụ đứng, clip vẽ nằm ngang.

## 2. Soát mắt 8 clip mẫu (chưa từng qua cổng mp4)

Kết quả: 1 đạt, 7 sửa nhẹ; 1 lỗi nặng; 7/8 clip có gợi ý chốt nêu sẵn cách làm.

### mayphat1 (L12) — SỬA NHẸ, có 1 lỗi NẶNG
- 2–22 s · NẶNG · mạch hở: dây 1 chỉ tới tần số kế, dây 2 chỉ tới bóng đèn (`mayphat1.py:55–56`), không thiết bị nào nối đủ hai đầu cuộn dây → mỗi thiết bị nối cả hai dây, song song với cuộn dây.
- 50,2–53,7 s · VỪA · gợi ý chốt "đổi ra vòng/s" (dòng 255) nêu đúng bước bẫy → "chú ý đơn vị của n" hoặc bỏ.
- 41,3–44,6 s · NHẸ · nửa dưới hộp bẫy trống tới 43,8 s.
- 12–16 s · NHẸ · "n = ··· vòng/s" đọc như số hỏng → "n đang tăng…".
- 15,9–20,3 s · NHẸ · hàng bảng 2–5 cách nhau ≈ 1 s, đọc không kịp.

### boyle (L12) — SỬA NHẸ
- 50,2–54,1 s · VỪA · gợi ý chốt "p·V ≈ 800 · thang đo 300 kPa" (dòng 251) nêu cách làm → chỉ giữ "p·V ≈ 800" hoặc bỏ.
- 42,1–48,1 s · NHẸ · áp kế cảnh bẫy: "300" dính "kPa", chữ 32 px (dòng 239); "8,0 → 4,0 ml" 34 px (dòng 228) → ≥ 36.
- 31,8–34,4 s · NHẸ · nửa dưới khung trống, hai hộp lệch nhau.
- 42,1 s · NHẸ · mốc "215" hiện trước lời giải thích.

### moment3 (L10) — SỬA NHẸ
- 27,2–29,4 s · VỪA · nhãn "Mỗi lực F = 1,0 N" (dòng 138) chạm đầu mũi tên F.
- 46,1–48,8 s · VỪA · gợi ý chốt "Đổi cm ra m trước khi tính" (dòng 215) nêu bước làm → "d tính bằng mét" hoặc bỏ.
- 26,1 s · NHẸ · hàng 3 của bảng (d = 0,15) hiện trước khi hình nhích hai giá vào.
- 31,5 s; 38,3–42 s · NHẸ · thẻ bẫy trống nửa dưới; cảnh Giới hạn tĩnh 4,6 s.
- 43,9 s · NHẸ (nghi) · câu THỬ NGHĨ không nói hai lực ngược chiều.

### nemngang2 (L10) — ĐẠT
- NHẸ · vài chữ đúng ngưỡng 11 px (36 px trong mã) → 40 nếu còn chỗ; nửa dưới trống 2 s ở 30,8 s.
- NHẸ (nghi) · đáp số THỬ NGHĨ 0,525 nội suy được ≈ 0,52 từ hai hàng bảng → kiểm khoảng cách các lựa chọn A–D ở khung.

### tudien2 (L11) — SỬA NHẸ
- 46,1–49,6 s · VỪA · gợi ý "Q = C · U" nêu cách làm → gợi ý kiểm lại ("12 V vẫn dưới 16 V ghi trên vỏ").
- 33,1–40,7 s · NHẸ (nghi) · bẫy 470 μF vs 481 μF chỉ chênh 2 % → kiểm lựa chọn A–D cách xa nhau.
- 13,2 s; 17,4 s · NHẸ · dấu "+" điện tích sát nhãn cực "+".
- 17,4–22,3 s · NHẸ · số vôn kế mỗi lần tua chỉ hiện 0,7 s.
- 26,7–31 s · NHẸ · nhãn "4000" tắt nhưng vạch còn; "số liệu mô phỏng" 36 px; hộp THỬ NGHĨ trống nửa dưới 2,5 s.

### sddpin2 (L11) — SỬA NHẸ
- 43,4–49,7 s · VỪA · câu chốt có/không lộ "không" qua chữ "chỉ"; gợi ý "Vôn kế đọc tới 0,01 V" nêu lý do → hỏi mở ("Chọn hai lần đo nào để tính r đáng tin nhất, vì sao?"), bỏ 0,01 V.
- 12–17 s · NHẸ · mũi tên I cách thẻ đồng hồ 6 px.
- 27,3–32,3 s · NHẸ · nhãn "phần hụt I·r" chỉ ở một cột; cảnh Rút ra dày.
- 34,4–39 s · NHẸ · nửa dưới trống; 24,2 s "ℰ" chưa chú thích.

### motadddh1 (L11) — SỬA NHẸ
- 44,7–48,2 s · VỪA · gợi ý "Biên độ mới 6 cm, T vẫn là 2 s" nêu cách làm (clip chưa hề hiện T) → "Nhìn lại bảng: sau 1,0 s vật ở đâu?".
- NHẸ · hộp THỬ NGHĨ, hộp BẪY trống 1/3–40 %; khung "Chưa nói được" có lúc trống 1 s.

### l9ohm1 (L9) — SỬA NHẸ
- 44,6–49,7 s · VỪA · gợi ý "Đừng chỉ nhìn ampe kế" loại sẵn một lựa chọn; banner "R = U : I" hiện cùng câu hỏi → gợi ý trung tính, banner hiện sau thời gian nghĩ.
- 4,9–9,4 s · NHẸ · hộp DỰ ĐOÁN hẹp hơn thẻ dụng cụ phía sau, mép thẻ thò ra.
- NHẸ · cảnh Kết quả, Bẫy trống 35–40 % khung dưới; hình dây C trong hộp chốt nhỏ.

## 3. Clip chưa từng soát mắt (75 clip còn lại)

Đã soát mắt mp4 (không cần làm lại): ddh1, ddh3, vantocdddh2, tatdan1–3, bttdaodong2, btnangluong2, conangdddh2,
trondeu2, huongtam2–4, lamquen2, saiso1, dotocdo1–2, dtdctg2, dog1, roitudo3, hatnhan3, thuchanhtu4 + 8 clip mục 2.

- L12 (20): antoanpx1, apsuat1, apsuat2, camungdt, camungdt3, chuyenthe, dttruong2, hatnhan1, hatnhan2, mayphat3, nllk1, phongxa2, pttrangthai2, thangnhietdo1, thangnhietdo4, thuchanh2, thuchanhtu3, tutruong4, udcamung2, xoaychieu3 (+ boyle, mayphat1 đã có ở mục 2).
- L10 (30): trongluc2, trongluc3, giaibtdlh1, giaibtdlh2, klr1, klr2, tonghopluc2, congsuat1, dongnang1, conang1, hieusuat1, dongluong1, dongluong2, thuchanhdl3, tdvt1, tdvt3, ddqd1, dotocdo3, dtdctg1, giatoc1, giatoc2, ctbdd1, roitudo2, dog2, dog3, trondeu3, biendang3, saiso2, antoan1, antoan2.
- L11 (18): coulomb2, dientruong11, dtdeu2, thenang1, dienthe1, dienthe2, cddd2, ohm3, nangluong2, nangluong3, nguondien1, nguondien2, motadddh2, vantocdddh1, bttdaodong1, bttdaodong3, conangdddh1, btnangluong1.
- L9 (7): l9tieucu3, l9congsuat1, l9congsuat3, l9conang1, l9dongthe1, l9dongthe2, l9congco1.

## 4. Soát mắt lô L12 (19 clip, 12/11/2026)

Cách soát như mục 2 (khung-375.py + kiem-code đóng vai HS lớp 12, mỗi agent 2 clip). thuchanhtu3 không soát: phiên khác đang làm bản 2 (nhánh `claude/magnetic-field-simulation-video-76aa88`).
Kết quả: 19 sửa nhẹ, 0 soạn lại; 2 lỗi NẶNG (dttruong2 mạch hở, thangnhietdo4 thẻ chốt lộ đáp án — cả hai phiên chính đã xác nhận trong mã). Cả 19 clip còn K10 (nút A–D trong hộp Dự đoán); 17/19 có gợi ý chốt nêu cách làm; 18/19 có chữ thông tin chính 32–34 px mã (< 11 px). Mọi số trên màn đã tính lại, khớp kho; đáp án Dự đoán khớp khung ở cả 19.

### antoanpx1 (L12) — SỬA NHẸ
- 3,1–8,9 s · VỪA · K10: hộp Dự đoán vẽ 4 thẻ A–D kèm thanh đếm, trông như bấm được (`antoanpx1.py:75,84–90`) → bỏ 4 thẻ, giữ câu hỏi + thanh đếm.
- 53–54 s · VỪA · gợi ý chốt "Nhớ lại cột N·d²" nêu sẵn cách giải (dòng 266) → gợi ý trung tính ("Xem lại hình các ô vuông").
- cả clip · VỪA · chữ 34 px mã (≈ 10,4 px) ở nhãn chính: "xung/phút (nhịp đo)" (72), trục N, d (145–146), số thước (43), nhãn cột (183), "Cách tâm nguồn", "Máy đếm" (65, 69); "chì" 32 px (56) → ≥ 36.
- 3,1–8,9 s · NHẸ · đề nêu "Ở 1 m: 360 xung/phút" nhưng bảng ở 1 m ghi nhịp đo 390 → thêm "(đã trừ phông)".
- 43–52 s · NHẸ · cảnh bẫy nửa dưới trống (251–259).
- cả clip · NHẸ · 54,6 s (> 50 s), 199 từ/phút.
- Số đã tính lại khớp kho (71×9 ≈ 640, 1454/166 ≈ 8,8, N·d² 356–374, phông 30); đáp án B khớp khung.

### apsuat1 (L12) — SỬA NHẸ
- 9,1–11,3 s · VỪA · K10: 4 viên A–D trông như bấm được (`apsuat1.py:81–102`) → bỏ, giữ câu hỏi + thanh đếm.
- 48–52,5 s · VỪA · gợi ý chốt "Số cú đập mỗi giây phụ thuộc vào gì?" dắt sẵn cách làm (234) → gợi ý trung tính.
- 33–37 s · VỪA · công thức "n = N·v/(2L)" không giải nghĩa N, v, L (195) → thêm một dòng chú thích.
- cả clip · VỪA · chữ 32 px mã (≈ 9,8 px): "Số tính từ mô hình" (191), nhãn bảng đếm (72–74), tiêu đề cột (171), trục "t · chiếu chậm" (129); "một cú đập" 34 px (137) → ≥ 36.
- 46–52,5 s · NHẸ · cảnh chốt 34 từ / 6,5 s; cả clip 52,6 s.
- 17–27 s · NHẸ (nghi) · vạch lực cao gấp 3 ở 3 Hz có thể kéo HS về nhiễu "gấp chín" → chú thích "mỗi vạch cao ∝ v".
- Số tính lại khớp kho (125/375/250/750/1500); đáp án B khớp khung.

### apsuat2 (L12) — SỬA NHẸ
- 3,3–8,7 s · VỪA · K10: 4 nút "A. 96 kPa … D. 864 kPa" trông như bấm được (`apsuat2.py:85–89`) → bỏ, giữ câu hỏi + thanh đếm.
- 46,6–52,6 s · VỪA · gợi ý chốt "Đổi hai nhiệt độ sang kelvin rồi so" (257) nêu cách làm; cảnh bẫy ngay trước đã ghi "Đúng: T = t + 273" (245) → "p tỉ lệ thuận với đại lượng nào?".
- 9,3–20,6 s · VỪA · chữ 34 px mã (≈ 10,4 px): nhãn Áp kế/Nhiệt kế/kPa/°C (64–73), số trục (145–147, 223–225), hàng "T (K)", "p/T" (165–166); "0,25 lít" 30 px (51) → ≥ 36.
- 20,6 s · NHẸ · nét đứt nối về O ngoại suy ngoài khoảng đo 283–363 K (kho: "không nói gì ngoài khoảng đo") → ghi "ngoại suy".
- 18–27 s · NHẸ · nửa dưới trống lúc 20,6 s; cảnh cuối 300 từ/phút; cả clip 52,6 s.
- Số tính lại khớp kho (p/T 0,3388–0,3394; 96·363/283 = 123,2 → B); nhiễu C, D sai rõ.

### camungdt (L12) — SỬA NHẸ
- 5–8,7 s · VỪA · K10: 3 nút A–C trông như bấm được (`camungdt.py:182–185`) và chữ HOA "YÊN" gợi đáp án (180) → bỏ nút, viết thường.
- 10,9 s · VỪA · số thoáng qua "i = +3,0 mA" (ramp số, 213) trong khi kho/bảng là +3,9 → chỉ hiện số khi kim đứng ở đỉnh.
- 45–51,8 s · VỪA · gợi ý chốt "Cực S: từ trường ngược cực N" (335) nêu sẵn lập luận → "Nhớ lại điện kế khi rút nam châm ra".
- 25–33 s · VỪA · nhãn "+3,9" bị đường cam gạch ngang (275–283) → đường dừng ở 0,4 m/s hoặc dời nhãn.
- 10,9–33 s · VỪA · chữ 32 px mã (≈ 9,8 px): chip bước (225–227), tiêu đề cột (233), trục + nhãn điểm (265–284), "ĐÁP ÁN B" (254); dòng bằng chứng "0,1 → 1,0 · 0,4 → 3,9 mA" 34 px (299) → ≥ 36, dòng 299 lên 38–40.
- 23,9–33 s · NHẸ · điểm +2,1 (0,2 m/s) có trên đồ thị nhưng chưa làm trong cảnh Tiến hành → ghi "tính theo tỉ lệ".
- 47,4 s · NHẸ (nghi) · câu chốt hỏi "bao nhiêu" với cực S, kho không có số → hỏi "phía nào".
- 23,9 s · NHẸ · thẻ "Từ thông BIẾN THIÊN…" rỗng nửa dưới (304); cảnh cuối 291 từ/phút, cả clip 51,8 s.
- Số khớp kho (1,0 / 2,1 / 3,9 / −2,0); đường sức ra N vào S đúng; đáp án B khớp khung.

### dttruong2 (L12) — SỬA NHẸ, có 1 lỗi NẶNG
- 2,0–50,6 s · NẶNG · mạch hở: dây chỉ đi máy phát → tụ → đồng hồ (`dttruong2.py:20–21`, vẽ ở 58), không có dây từ đồng hồ về máy phát → thêm dây hồi, vẽ rõ hai cực máy phát và đồng hồ.
- 3,3–9,2 s · VỪA · K10: 4 thẻ "A. Luôn bằng 0 … D." trông như nút (89–102) → bỏ, giữ câu hỏi.
- 44,6–50,6 s · VỪA · thẻ chốt "I tỉ lệ thuận f" (263) + gợi ý "I/f có đổi không?" (265) cho sẵn cách giải câu "f = 1 600 Hz: đồng hồ chỉ?" → thẻ "Dòng điện dịch", gợi ý trung tính.
- 44,6–50,6 s · NHẸ (nghi) · đáp số câu chốt (≈ 116–120 mA) là ngoại suy, kho không có.
- 19,3–21,2 s · NHẸ · chế độ một chiều vẫn vẽ E giữa hai bản tụ khi đồng hồ chỉ 0 → chú thích "tụ đã nạp xong".
- cả clip · NHẸ · 50,6 s, 204 từ/phút.
- Số khớp kho (58,0/3,6 ≈ 16,1; I/f 0,072–0,074; "thấp hơn 2–5 %" đúng 1,9–4,5 %); đáp án C khớp khung; cỡ chữ nhỏ nhất 36 px mã.

### hatnhan1 (L12) — SỬA NHẸ
- 5,8–10,8 s · VỪA · K10: 4 hàng viên thuốc A–D (`hatnhan1.py:150–154`) → bỏ, giữ câu hỏi.
- 48,5–51,6 s · VỪA · gợi ý chốt "Phần bề rộng bị chắn?" (302) nêu cách làm → gợi ý trung tính hoặc bỏ.
- 0–44 s · VỪA · chữ 34 px mã (≈ 10,4 px): thang "20 cm" (115–116), "bi 10 mm" (142), nhãn "Đi thẳng / Lệch mạnh / Tỉ lệ lệch" (252) → ≥ 36.
- 38–43 s · NHẸ · thẻ "Chưa nói được" trống đáy; "LỰC ĐIỆN ĐẨY" 56 px hiện đột ngột (294).
- cả clip · NHẸ · 51,7 s, 209 từ/phút.
- Số khớp kho (57 + 3 = 60, 3/60 = 0,05; bán kính chạm 6 mm; câu chốt dùng đúng hàng 40 cm); phản xạ 3 tia đúng; đáp án C khớp khung.

### camungdt3 (L12) — SỬA NHẸ
- 4,9–9,1 s · VỪA · K10: 4 thẻ viền A–D kèm đồ thị nhỏ trông như bấm được (`camungdt3.py:127, 140–150`) → bỏ chữ A–D và viền nút, để 4 đồ thị nhỏ không nhãn.
- 12,4–15,6 s · VỪA (nghi) · số dừng ở 30° (Φ = 0,00866 Wb) chỉ hiện ≈ 0,6 s, ở 60° ≈ 0,8 s (157–160, 198–203) → mỗi lần dừng ≥ 1,5 s hoặc giữ ô đọc khi quay.
- 46,9–50,3 s · VỪA · gợi ý chốt "Nhớ lại dạng đồ thị Φ theo α" chỉ cách làm (270–272) → "Xem lại bảng số liệu".
- cả clip · VỪA · số trục Φ(α) và nhãn "Φ (Wb)", "α (°)" 34 px mã (106–116); "dải cam…" 32 px (72); "khung (nhìn cạnh)", "điện kế" 34 px (88, 178) → ≥ 36.
- 90° · NHẸ · chú thích "dải cam: xuyên qua khung" vẫn hiện khi không đường nào xuyên (71) → ẩn khi |cos α| < 0,05.
- 26–29 s · NHẸ · vùng trống dưới đồ thị; thẻ "Càng nghiêng…" cao 180 chỉ một dòng; cả clip 50,3 s.
- Số khớp kho (Φ = 0,01 cos α; 0,005 → 60°); đáp án C khớp khung; đường sức N → S đúng.

### chuyenthe (L12) — SỬA NHẸ
- 5,2–9,1 s · VỪA · clip vẽ 4 thẻ A–D (D: đường tiệm cận) nhưng khung chỉ có 3 lựa chọn A–C; thẻ viền như nút (K10) (`chuyenthe.py:137–164`) → bỏ thẻ lựa chọn khỏi mp4.
- 46,3–50,6 s · VỪA · gợi ý chốt "λ = 334 · L = 2 260 kJ/kg" nêu sẵn đại lượng cần so, "334" thiếu đơn vị (364) → "Bếp cấp nhiệt như nhau mỗi phút. Nhiệt dùng vào việc gì?".
- 38,2–44 s · VỪA · số đọc 0,2/0,3 và "0 °C" 32–34 px mã, trục phóng to thiếu "t (phút)" (311–326); số trục đồ thị chính 32–34 px (107, 117) → ≥ 36, thêm nhãn trục.
- 30–36 s · NHẸ · thanh "Động năng" cao khác nhau giữa tan (0,45) và sôi (0,8) cùng nhãn "không tăng" → ghi "Động năng TB: không đổi".
- 14–25 s · NHẸ · số phút tua nhanh; 205 từ/phút, cảnh cuối 249; cả clip 50,6 s.
- 3–5 s; 26,6–28 s · NHẸ · nửa dưới trống trước khi hộp hiện.
- Số khớp kho (0,2/0,3; 17,8; 100,3; L/λ = 6,77 ≈ "gần 7 lần"); đáp án C khớp khung.

### hatnhan2 (L12) — SỬA NHẸ
- 3,3–12,8 s · VỪA · K10: 4 thẻ tím A–D viền bo như nút (`hatnhan2.py:76–79`) → bỏ, giữ đề + thanh đếm.
- 46,9–53,4 s · VỪA · gợi ý chốt "Diện tích gấp đôi: m thay đổi?" (239) nêu bước giải → "Bề dày d phụ thuộc những đại lượng nào?".
- 3,3–47 s · VỪA · số mũ vẽ bằng 0,72 × cỡ (`rich2`, 22–24): "2,8×10⁻¹⁰ m" (74, 102) số mũ ≈ 8,8 px; "10⁻¹⁵" (184–186) ≈ 9,8–10,6 px; tiêu đề đồ thị (206) ≈ 7,9 px → hệ số ≥ 0,9 cho số mũ âm.
- 3,3 s · NHẸ · "Nguyên tử nhôm: 2,8×10⁻¹⁰ m" không nói là đường kính (cảnh sau ghi r ≈ 1,4×10⁻¹⁰ m) → "Đường kính nguyên tử nhôm".
- 18–44 s · NHẸ · "A = 27/63/197" (211), "cân điện tử" (50) 34 px mã.
- cả clip · NHẸ · 53,5 s, 211 từ/phút; hộp "Thử nghĩ" trống quá nửa.
- khung `rut_ra` · NHẸ (nghi) · "nhiều hơn lá vàng của Rutherford" không có trong kho.
- Số khớp kho (d 10,0/10,4/10,1 µm; R 3,6/4,8/7,0 ×10⁻¹⁵ m; 7,0/3,6 ≈ 1,94); đáp án C khớp khung.

### mayphat3 (L12) — SỬA NHẸ
- 3,8–10 s · VỪA · K10: lưới 2×2 nút "A. 6 V … D. 48 V" (`mayphat3.py:101–105`) → bỏ, giữ đề + thanh đếm.
- 49,5–53 s · VỪA · gợi ý chốt "100 vòng cho ra mấy vôn?" (273) dẫn thẳng tới hàng 100 vòng → "Số đo so với số tính theo công thức: cao hay thấp?".
- 49,5–53 s · VỪA (nghi) · câu chốt "Muốn thứ cấp ra 6 V: hơn hay kém 100 vòng?" (268) mơ hồ: lí tưởng đúng 100 vòng, chỉ "hơn" nếu tính hao phí → thêm "theo số đo của bảng".
- 25–30 s · NHẸ · cột "U₁/U₂ đo" trống ≈ 5 s (199); hộp "Cùng lõi…" trống 2/3.
- cả clip · NHẸ · "Số liệu minh hoạ" 34 px mã (143, 162); 53,2 s, 179 từ/phút.
- Số khớp kho (5,9/11,6/23,5/35,1 V trong ±0,1 V của 12·N₂/200·0,975); mạch kín, vôn kế song song thứ cấp; đáp án C khớp khung.

### pttrangthai2 (L12) — SỬA NHẸ
- 5,1–8,4 s · VỪA · K10: 4 ô A–D viền tím như nút (`pttrangthai2.py:82, 92–99`) → bỏ, giữ câu hỏi + dữ kiện.
- 45,7–48,4 s · VỪA · gợi ý chốt "Đổi sang kelvin trước." (248) nêu bước giải; ô chốt "p/T không đổi (kelvin)" (237) đã nêu quy tắc → "Thể tích bình có đổi không?".
- 17–35 s · NHẸ · số trục 34 px mã (174, 177).
- Số khớp kho (p/T 0,365–0,367; p/t 4,36→1,36, ÷0 ở 0 °C); đáp án C khớp khung; câu chốt 60 °C → ≈ 122 kPa không lộ.

### thangnhietdo1 (L12) — SỬA NHẸ
- 2,0–8,9 s · VỪA · K10: 4 ô A–D như nút (`thangnhietdo1.py:84, 101–108`) → bỏ, giữ câu hỏi.
- 42,9–48,4 s · VỪA · gợi ý chốt "Nhớ ca 100 g + 200 g." (338) gần như nêu cách loại trừ, lại mơ hồ ("ca" = cốc) → "So sánh với ca vừa xem".
- 22,5–29,8 s · VỪA · nhãn "giữa: 40,0" 34 px mã, xám nhạt, mà là thông tin chính của so sánh (257) → 38 px, màu INK; số thang 34 px (163, 235, 281) → 36.
- 22,5 s · NHẸ · "39,1" hiện trước nhãn "giữa: 40,0", không ghi "đo".
- 11,0 s · NHẸ · "100 g · 60 °C" (193) gần chạm "Số liệu minh hoạ" (29).
- 13,5–14,7 s · NHẸ · cốc nghiêng vẽ thành hình thoi trắng, không thấy nước (192).
- 31,9–40,8 s · NHẸ · "Nước nhiều kéo về phía nó" (308) ẩn dụ lỏng → "Nước nhiều đổi nhiệt độ ít hơn".
- Số khớp kho (32,9 / 33,3 / 39,1 / 40,0; bẫy (60 + 20)/2 = 40); đáp án B khớp khung.

### nllk1 (L12) — SỬA NHẸ
- 9,9 s · VỪA · K10: 4 viên A–D như nút (`nllk1.py:126–129`) → bỏ, giữ câu hỏi + thanh đếm.
- 43,8–51,2 s · VỪA · gợi ý chốt "Lực điện hút hay đẩy?" (302) loại trừ sẵn → "Nhìn lại chiếc đai trong thí nghiệm".
- 21,9 s · VỪA · chữ < 36 px mã: trục "d (mm)", "t", "0" 32 px (173–174); số 18, 5 34 px (177); "P nhỏ, không vẽ" 32 px (95–97); nhãn bước "Thả / Ép rồi thả / Siết đai" 32 px (162–164); cột "d (mm)" 34 px (235) → ≥ 36.
- cả clip · NHẸ · 51,3 s; cảnh bẫy 222 từ/phút; vùng trống 2–6 s và cảnh chốt.
- Số khớp kho (18, 18, 5 mm); cực N–N, chiều lực đẩy/đai/P đúng; đáp án B khớp khung.

### phongxa2 (L12) — SỬA NHẸ
- 4,5–8,4 s · VỪA · K10: 3 viên A–C viền tím như nút (`phongxa2.py:73–76`) → bỏ, giữ câu hỏi + thanh đếm.
- 8,9–55 s · VỪA · trục "H (xung/phút)", "t (phút)" và số trục 34 px mã (131–137) → ≥ 36.
- 50,4–54,8 s · VỪA · câu chốt "Bớt một nửa lượng nguồn thì T còn 5 phút không?" (231) mơ hồ ("còn 5" đọc như giảm xuống 5) → "…thì T có đổi không?".
- 14–19 s · NHẸ · hàng số hiện cách nhau 0,6 s (84).
- cả clip · NHẸ · 54,9 s; cảnh hook 218, cảnh chốt 212 từ/phút; thẻ đáp án trống 1/3 khung 5 s.
- Số khớp kho (trừ phông 23; tỉ số 2,04 / 1,95 / 2,10 / 1,87 / 2,17; chưa trừ phông 1,60); đáp án B khớp khung; gợi ý chốt không nêu cách làm.

### thangnhietdo4 (L12) — SỬA NHẸ, có 1 lỗi NẶNG
- 44,7–52,6 s · NẶNG · lộ đáp án câu chốt: thẻ "Mặt bóng cho số thấp giả" nằm ngay trên câu hỏi "Sao máy hồng ngoại chỉ 41,0 °C?" (`thangnhietdo4.py:276–277`) → tiêu đề chốt trung tính ("Ba nhiệt kế, ba cách đo").
- 44,7–52,6 s · VỪA · gợi ý "So ε giấy bạc với 0,95" (278) nêu cả bước làm lẫn lời giải → "Máy hồng ngoại đo bằng cách nào?".
- 0–9,6 s · VỪA · K10: 3 hàng A–C viền bo như nút (152–155) → bỏ.
- 32,9–44 s · VỪA · giá trị trên đồ thị điểm 32 px mã (225), số trục, "°C" (213–214) → ≥ 36.
- 36,5–40,5 s · NHẸ (nghi) · "Lùi xa: vết đo tràn ra" khác kho (chùm tia hứng thêm bức xạ nền) → "vết đo rộng hơn, hứng cả nền".
- cả clip · NHẸ · nhãn "5 cm" = 56 px làm cốc ≈ 27 cm; 52,6 s, 207 từ/phút; khung ghi "nhiệt kế điện trở", clip ghi "điện tử".
- Số khớp kho (49,8 / 50,2 / 48,4 / 47,1 / 41,0 / 38,5; ε 0,95; |49,8 − 50,2| = 0,4 < 0,5); đáp án B khớp khung.

### thuchanh2 (L12) — SỬA NHẸ
- 47,3–53,3 s · VỪA · gợi ý chốt "λ = P·τ/m; λ giữ nguyên" nêu sẵn công thức (`thuchanh2.py:349–352`) → "Đoạn ngang này ứng với giai đoạn nào?".
- 47,3–53,3 s · VỪA · câu chốt "Đoạn ngang dài bao lâu?" mơ hồ — có hai đoạn ngang 0 °C và 100 °C (344–345) → "đoạn ngang ở 0 °C (đá tan)".
- 0–9,5 s · VỪA · K10: 4 hàng A–D viền bo (133, 150) → bỏ.
- 22,3–30 s · VỪA · "Sôi gấp ≈ 5,4 lần" không nói so với gì (250); thanh Tan ngay trên dễ đọc thành so với tan (6,77) → "…lần Nóng lên".
- 40–46 s · VỪA · mũi tên xanh chỉ vào nước không nhãn (321); "cân cả vào m" (323) lệch → thêm nhãn "nước".
- 20,2 s · NHẸ · "Sôi 2 260 s" hiện < 0,5 s (140–142).
- cả clip · NHẸ · "oát kế" (80), "TUA NHANH" (180) 32 px; nửa dưới cảnh tính λ, L trống; 53,3 s.
- Số khớp kho (33 400 / 41 900 / 226 000 J; λ, c, L; sôi chiếm 75 %); đáp án C khớp khung.

### tutruong4 (L12) — SỬA NHẸ
- cả clip · VỪA (nghi mức lệch) · kho `tn-l12-tutruong-04.json` (`cac_buoc.lam`) ghi nam châm trụ ĐỨNG, clip vẽ nằm ngang theo thước (`tutruong4.py:19–21`); mô hình √(B_lt² + 30²) chỉ đúng khi trục nam châm vuông góc từ trường Trái Đất → sửa kho thành "nằm ngang, trục theo thước, hướng Đông–Tây" + ghi giả thiết vuông góc (chờ thầy chốt, chưa sửa).
- 6,1–8,1 s · VỪA · K10: 4 viên A–D viền tím (57–62) → bỏ.
- 45,0–53,8 s · VỪA · gợi ý chốt "Nhớ lại: gấp đôi ra 1/8" (215) nêu sẵn quy luật 1/d³ → "B giảm theo khoảng cách thế nào?".
- cả clip · VỪA · số trục + thước (51, 140), "S" "N", chú giải "số đọc / mô hình" (223) 34 px mã; số ô phóng to 32 px → ≥ 36.
- 21–54 s · NHẸ · vùng trống dưới đồ thị, ô hồng cảnh bẫy, cảnh chốt.
- 0–10 s · NHẸ · nam châm vẽ 0,57 × 1,4 cm, kho ghi đĩa ∅ 5 mm dày 2 mm (19).
- cả clip · NHẸ · 53,9 s.
- Số khớp kho (8000/d³ → 1000 / 125 / 37,0 / 15,6 / 8,0 µT; tổng hợp 1000 / 129 / 48 / 34 / 31 µT).

### udcamung2 (L12) — SỬA NHẸ
- 5,7–9,3 s · VỪA · K10: 4 viên A–D viền (`udcamung2.py:187–190`) → bỏ.
- 41,5–48,3 s · VỪA · gợi ý chốt "e₂ = −M·Δi₁/Δt / Giữ K đóng: kim chỉ ở đâu?" (301) đưa sẵn công thức + cách làm → "Nhớ lại: lúc nào kim điện kế lệch?".
- cả clip · VỪA · "1,5 V" (93), "0 / 0,5 A" (124), số + tên trục i₁, e₂, t (149–157), tiêu đề cột (253) 32 px mã → ≥ 36.
- 24,6–29,2 s · NHẸ · nhãn "bật", "ngắt" bị viền dải xanh cắt, "e₂ (V)" sát mép (146, 159).
- 41,5–48,3 s · NHẸ · thẻ "Thử nghĩ" trống giữa.
- 2–9,4 s · NHẸ (nghi) · chiều đường sức (77) chưa đối chiếu được với chiều cuốn dây.
- Số khớp kho (2·10⁻³ × 25 = 0,05 V; 0,5/0,02 = 25 A/s); hai mạch kín; đáp án C khớp khung.

### xoaychieu3 (L12) — SỬA NHẸ
- 3,4–9,6 s · VỪA · K10: 4 thẻ "A. Không sáng … D. Sáng hơn" viền tím như nút (`xoaychieu3.py:131–135`) → bỏ, giữ câu hỏi + thanh đếm.
- 50,8–52,5 s · VỪA · gợi ý chốt "Dùng U hay U₀?" (255) nêu sẵn bước loại trừ → "Xem lại cảnh Cái bẫy".
- 17–41 s · VỪA · số trục 17, 12, −17 và nhãn "một chiều" 34 px mã (94, 152, 156) → ≥ 36.
- 17–20 s · NHẸ · "V~" trên vôn kế 32 px (52).
- 20,9 s · NHẸ · phụ đề "Công suất p luôn dương" lệch nhãn hình "p luôn ≥ 0" (275) → "p không bao giờ âm".
- 22,5–31 s · NHẸ · đường "đỉnh gấp 2" không ghi 24 W; vùng trống dưới đồ thị (188).
- cả clip · NHẸ · 52,5 s.
- Số khớp kho (12 W; đỉnh 12√2 ≈ 17 V; p đỉnh 24 W; câu chốt 24²/12 = 48 W); mạch kín, vôn kế song song; đáp án C khớp khung.

