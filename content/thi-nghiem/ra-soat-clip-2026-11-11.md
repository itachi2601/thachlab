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
