# 06 — Chú giải bản vẽ (Drawing notes, BOM, part numbers) — không vẽ lại

Nguồn: `WS2026_TP01_1st Assembly and Machining` (bản vẽ lắp 100, 300, 400, 500, chi tiết 301, 401, 404, 405, 1000; 25/08/2026), `WS2026_TP01_1st Angle Machining Aid + Machining Detail Parts` (trích 401, 404, 405 + hướng dẫn gia công), `WS2026_TP01_200 Fab and Welding Series 1st angle` (bản vẽ 200, 201–207), `WSC2026_TP01_1st_angle_pre_en` (bộ pre-release, JANUARY 2026: 101–107, 201–207, 301P, 302–305, 401–410, 500). Người vẽ: Simon Heathcote; SCM: Craig Brazil. Khổ A3.

**Các bản 3rd angle** (`…3rd Assembly and Machining`, `…3rd Angle Machining Aid…`, `…200 Fab and Welding Series 3rd angle`, `WSC2026_TP01_3rd_angle_pre_en`) **trùng nội dung hoàn toàn** với bản 1st angle, chỉ khác phép chiếu (góc thứ ba, kiểu Bắc Mỹ) — không dịch riêng.

> **Dùng để huấn luyện**
> - **Điểm liên quan:** mọi mục của C (26.0), D (22.1) và B1 (14.0) đều chấm theo bản vẽ này — đọc sai bản vẽ là mất điểm ở ba tiêu chí.
> - **Điểm dễ lấy:** thuộc BOM để lắp D2 "complete assembly" (1.75) và "secured" (≈3.5 điểm) không bỏ sót chi tiết; biết ký hiệu ±, H8/f8/6g để tự kiểm tra trước khi nộp.
> - **Bẫy mất điểm:** "DO NOT TIGHTEN NYLOCK NUTS" (tấm chắn phải lật tự do, 8 vị trí); "NO WELD OR TACK ON THIS FACE ON ANY MEMBER"; "DO NOT GRIND WELDS"; "HOLES IN ONE PART ONLY" (chỉ 1 trong 4 chân 201 có lỗ M4); "REAM ON ASSEMBLY WITH PART 401" (lỗ Ø9.5 trên 301 doa khi lắp cùng 401, không doa trước); "MAY NEED TO REAM THE BUSHINGS" (bạc 403 có thể phải doa để trượt êm); ký hiệu "NEAR SIDE ONLY" / "BOTH SIDES" trên 107 và 201.

## 1. Cách đọc khung tên (title block) và ghi chú chung

| Trên bản vẽ (EN) | Nghĩa (VI) |
|---|---|
| Drawing Title: WSC2026_TP01_CA_100_EN | Mã bản vẽ: kỳ thi 2026, đề nghề 01, CA = Competitor/Assembly, số bản vẽ 100, tiếng Anh |
| Scale: 1:5 / 1:2 / 1:1 / 2:1 / NTS / N/A / AS NOTED | Tỷ lệ; NTS = không theo tỷ lệ; AS NOTED = ghi riêng từng hình |
| Sheet Size: A3 — Dwg No: 1 of 3 | Khổ giấy A3 — tờ 1 trong 3 |
| SCM: CRAIG BRAZIL — Drawn by: SIMON HEATHCOTE | Quản lý thi nghề — Người vẽ |
| Date: 25/08/2026 | Ngày (bản thật); bản pre-release ghi JANUARY 2026 |
| PROJECTION (kèm ký hiệu hình nón cụt) | Phép chiếu góc thứ nhất (1st) hoặc góc thứ ba (3rd) |
| PART #: 301 — MTL: STEEL — QNTY: 1 | Mã chi tiết — Vật liệu: thép — Số lượng |
| MTL: ALUM / STEEL / BRASS / ACETAL / LEXAN / BRONZE / M2 | Nhôm / thép / đồng thau / nhựa acetal (POM) / polycarbonate / đồng thanh / thép gió M2 |
| Test Project for the 48th WorldSkills Competition in Shanghai, China 2026 — Copyright © 2026 WorldSkills International | Đề thi Kỳ thi Kỹ năng nghề thế giới lần 48, Thượng Hải 2026 — bản quyền WSI |
| SOLIDWORKS Educational Product. For Instructional Use Only. | Dấu nước của phần mềm vẽ, bỏ qua |
| WSC2026_TPXX_AA_BB_EN_MULTI-SHEET.dwg | Tên file CAD gốc nhiều tờ |

Ghi chú lặp lại trên bản vẽ chi tiết gia công (401, 404, 405):

| EN | VI |
|---|---|
| 1. BREAK ALL SHARP EDGES | 1. Vê (phá) mọi cạnh sắc |
| 2. UNLESS OTHERWISE SPECIFIED SURFACE FINISH 1.6 (405: 3.2) ON ALL MACHINED SURFACES | 2. Nếu không ghi khác, độ nhám Ra 1.6 µm (405: Ra 3.2) trên mọi mặt gia công |
| 3. UNLESS OTHERWISE SPECIFIED TOLERANCE CLASS IS m (MEDIUM) ISO2768-1fk | 3. Nếu không ghi khác, dung sai chung theo ISO 2768-1, cấp m (trung bình) [Ghi chú dịch: ký hiệu kèm theo lại là "fk" = cấp f (fine) kích thước, K hình học — mâu thuẫn, `loi-ban-goc.md` #16; thang điểm dùng ±0.15/±0.3] |

## 2. Bản vẽ lắp 100 — Toàn máy (WSC2026_TP01_CA_100_EN, 3 tờ, tỷ lệ 1:5, DETAIL G 1:2, DETAIL H 1:5)

Ghi chú trên bản vẽ:

| EN | VI |
|---|---|
| DO NOT TIGHTEN NYLOCK NUTS, ALLOW FREE MOVEMENT OF SAFETY SHIELD – 8 PLACES | **KHÔNG siết chặt đai ốc Nylock** (item 17), để **tấm chắn an toàn chuyển động tự do** — 8 vị trí |

BOM (ITEM NO. | PART NUMBER | DESCRIPTION EN | VI | QTY):

| Item | Mã | Mô tả EN | Mô tả VI | SL |
|---|---|---|---|---|
| 1 | 200 | WELDMENT | Cụm hàn (khung đỡ máy, thí sinh hàn) | 1 |
| 2 | 300 | BACK PLATE ASSEMBLY | Cụm tấm lưng | 1 |
| 3 | 107 | SAFETY SHIELD | Tấm chắn an toàn (Lexan) | 1 |
| 4 | 105 | HANDLE | Tay cầm (acetal) | 1 |
| 5 | 102 | LONG ARM | Tay đòn dài (nhôm) | 2 |
| 6 | 101 | SHORT ARM | Tay đòn ngắn (nhôm) | 2 |
| 7 | 8049239 VMEF-RT-M32-M-G18 | SAFETY SWITCH | Công tắc an toàn (van cần con lăn Festo, -QMA1 "Gate Switch") | 1 |
| 8 | 104 | SAFETY SWITCH STRIKER | Vấu tác động công tắc an toàn (nhôm) | 1 |
| 9 | 91290A129 | M10 X 120 SHCS | Vít lục giác chìm đầu trụ M10 × 120 (bắt 301 vào 200) | 2 |
| 10 | 91455A140 | M10 STEEL WASHER | Vòng đệm thép M10 | 4 |
| 11 | 90591A171 | M10 NUT | Đai ốc M10 | 4 |
| 12 | 91239A152 | M4 X 20 BUTTON HEAD HEX DRIVE SCREW | Vít đầu tròn lục giác chìm M4 × 20 | 2 |
| 13 | 98269A430 | M4 STEEL WASHER | Vòng đệm thép M4 | 4 |
| 14 | 90593A003 | M4 NUT | Đai ốc M4 | 2 |
| 15 | 90854A152 | M6 X 15 STEEL HHCS | Bu-lông đầu lục giác M6 × 15 | 2 |
| 16 | 91310A333 | M6 X 20 STEEL HHCS | Bu-lông đầu lục giác M6 × 20 | 4 |
| 17 | 94645A205 | M6 NYLON-INSERT LOCKNUT | Đai ốc khoá lõi nylon M6 (Nylock) — **không siết chặt** | 8 |
| 18 | 91280A351 | M6 X 65 HHCS | Bu-lông đầu lục giác M6 × 65 | 4 |
| 19 | 91290A541 | M10 X 75 SHCS | Vít lục giác chìm M10 × 75 | 2 |
| 20 | 91290A176 | M4 X 25 SHCS | Vít lục giác chìm M4 × 25 | 2 |
| 21 | 500 | PNEUMATIC ASSEMBLY | Cụm khí nén (tấm linh kiện) | 1 |

Mã dạng 9xxxxAxxx là mã McMaster-Carr (giữ nguyên). Trên bản vẽ, số trong bong bóng (12 13 14, 21, 7, 1, 8, 3, 20, 4 5, 9 10 11, 15, 16, 6, 10 11 19, 18 17) là số item.

## 3. Bản vẽ lắp 300 — Cụm tấm lưng (WSC2026_TP01_CA_300_EN, 1 tờ, 1:5, DETAIL L 2:5)

| Item | Mã | Mô tả EN | Mô tả VI | SL |
|---|---|---|---|---|
| 1 | 301 | BACK PLATE | Tấm lưng (thí sinh lấy dấu, khoan, ta-rô) | 1 |
| 2 | 103 | PART PRESENT CHECK PIN | Chốt báo có phôi (thép) | 1 |
| 3 | 106 | PART PRESENT VALVE BRACKET | Giá van báo phôi (nhôm) | 1 |
| 4 | 3629 R-3-M5 (0) | ROLLER VALVE | Van con lăn Festo R-3-M5 (-QMA2 "Part Present") | 1 |
| 5 | 304 + 305 | BENDING PUNCH | Chày/má uốn trái + phải (acetal) [Ghi chú dịch: bản vẽ pre-release đánh số má uốn là **303 và 304**, còn 305 là khối định vị hành trình bằng thép; thang điểm D2 gọi 304 trái/305 phải — `loi-ban-goc.md` #18] | 2 |
| 6 | 302 | HEEL SLIDE | Con trượt gót (đồng thau) | 2 |
| 7 | 400 | SUB ASSEMBLY | Cụm con (cụm đột) | 1 |
| 8 | 93475A250 | M6 WASHER | Vòng đệm M6 | 12 |
| 9 | 90592A016 | M6 Nut | Đai ốc M6 | 12 |
| 10 | 91290A534 | M10 X 55 SHCS | Vít lục giác chìm M10 × 55 (bắt 401 vào 301) | 2 |
| 11 | 91290A344 | M6 X 60 SHCS | Vít lục giác chìm M6 × 60 | 4 |
| 12 | 91595A664 | 10 DOWEL 60 LONG | Chốt định vị Ø10 dài 60 (vào lỗ Ø9.5 doa trên 301) | 2 |
| 13 | 91290A148 | M4 X 12 SHCS | Vít lục giác chìm M4 × 12 | 2 |
| 14 | 98269A430 | M4 WASHER | Vòng đệm M4 | 2 |
| 15 | 90593A003 | M4 NUT | Đai ốc M4 | 2 |
| 16 | 91290A172 | M4 X 30 SHCS | Vít lục giác chìm M4 × 30 | 2 |
| 17 | 536273 ADN-32-30-A-P-A – with fittings | SQUARE BODY CYLINDER C/W MOUNTING CLEVIS | Xi lanh thân vuông Festo ADN-32-30 kèm đầu nối, **có đế chạc** (clevis LBG-32 + mặt bích xoay SNCS-32) — xi lanh uốn MM2, MM3 | 2 |
| 18 | 91290A330 | M6 X 25 SHCS | Vít lục giác chìm M6 × 25 | 8 |

## 4. Bản vẽ chi tiết 301 — Tấm lưng (WSC2026_TP01_CA_301_EN, 1:2) — thí sinh làm

| EN | VI |
|---|---|
| Notes: 1. ALL HOLE LOCATIONS ±0.5 | Ghi chú: 1. Mọi vị trí lỗ ±0.5 mm |
| 2. BREAK ALL SHARP EDGES | 2. Vê mọi cạnh sắc |
| 8x Ø7 THRU ALL | 8 lỗ Ø7 xuyên suốt (cụm 1, 2: bắt con trượt gót 302) |
| 4x Ø7 THRU | 4 lỗ Ø7 xuyên (cụm 3, 4: bắt đế chạc xi lanh uốn) |
| 4x Ø11 THRU | 4 lỗ Ø11 xuyên (bắt vào khung 200) |
| Ø11 THRU | 1 lỗ Ø11 xuyên (cụm 6) |
| 2x Ø8.5 THRU | 2 lỗ Ø8.5 xuyên |
| Ø9.5 THROUGH — REAM ON ASSEMBLY WITH PART 401 | Ø9.5 xuyên — **doa khi lắp cùng chi tiết 401** (để đóng chốt Ø10) |
| M10x1.5 – 6H THRU | Ren M10 × 1.5 cấp 6H xuyên (2 lỗ, bắt 401) |
| 42 TYP, 25 TYP, 100 TYP | Bước 42 / 25 / 100, áp dụng mọi vị trí tương tự |
| Kích thước vị trí: 95, 15, 139, 20, 243, 254, 135, 97, 88, 90, 105, 62 | Giữ nguyên, đo từ mép tấm |

Tấm 301 pre-release (301P): 500 × 375 (?) có hai khe cắt (CUT OUTS ARE THROUGH), **mài phẳng Blanchard cả hai mặt** (BLANCHARD GRIND BOTH FACES), Ra 3.2, dày 7 ±1, 2 lỗ Ø3.3 ta-rô M4×0.7, R6 TYP, vị trí ⟂ 0.1 B — **cấp sẵn cho thí sinh**; thí sinh chỉ lấy dấu và khoan/ta-rô 20 lỗ.

## 5. Bản vẽ lắp 400 — Cụm đột (WSC2026_TP01_CA_400_EN, 2 tờ; tờ 1 1:1, tờ 2 1:2)

Ghi chú tờ 1:

| EN | VI |
|---|---|
| PRE-BUILD ASSEMBLY AS SHOWN, BEFORE CONTINUING ENSURE THAT; 1, THE UPPER ASSEMBLY SLIDES EVENLY ON THE GUIDE PINS – MAY NEED TO REAM THE BUSHINGS 2, THE PUNCH ENTERS THE DIE BUTTON EVENLY WITH EQUAL CLEARANCE ALL AROUND | **Lắp thử trước như hình**, trước khi tiếp tục phải bảo đảm: 1. Cụm trên **trượt đều trên chốt dẫn hướng** — **có thể phải doa bạc** (sleeve bearing); 2. **Chày vào cối đều, khe hở đều quanh**. [Hai điều này là mục D2 1.5 + 2.0 điểm] |

BOM 400:

| Item | Mã | Mô tả EN | Mô tả VI | SL |
|---|---|---|---|---|
| 1 | 401 | DIE BLOCK | Khối cối (thép, **thí sinh phay**, C3) | 1 |
| 2 | 402 | CLAMP | Kẹp (thép, pre-release gồm 402-A, 402-B, 402-C) | 1 |
| 3 | ADX20-A20-M2-P6.6 | DIE BUTTON | Cối đột Misumi, lỗ Ø6.6 (= 408) | 1 |
| 4 | VFJT12-100-M6 | GUIDE PINS | Chốt dẫn hướng Misumi Ø12 × 100, ren M6 (= 410) | 2 |
| 5 | 91290A332 | M6 X 30 SHCS | Vít lục giác chìm M6 × 30 | 2 |
| 6 | 536418 AEN-32-10-A-P-A---(0) | SQUARE BODY CYLINDER | Xi lanh thân vuông Festo AEN-32-10 — **xi lanh kẹp MM1** | 1 |
| 7 | 402 | SPACER | Căn đệm (thép) [Ghi chú dịch: trùng mã 402 với item 2 — `loi-ban-goc.md` #17] | 2 |
| 8 | 91290A083 | M4 X 65 SHCS | Vít lục giác chìm M4 × 65 | 4 |
| 9 | 404 | PUNCH HOLDER | Đầu giữ chày (nhôm, **thí sinh tiện**, C2) | 1 |
| 10 | 403 | PUNCH PLATE | Tấm mang chày (nhôm, cấp sẵn) | 1 |
| 11 | 2934T138 | FLANGED SLEEVE BEARING | Bạc trượt có vai, đồng thanh (McMaster-Carr) (= 409) | 2 |
| 12 | 401 | STROKE POSITIONING SCREW | Vít định vị hành trình (= **Detail 405**, thép, **thí sinh tiện**, C1) [Ghi chú dịch: trùng mã 401 với item 1 — #17] | 1 |
| 13 | 90593A015 | M24 NUT | Đai ốc M24 (khoá ren M24×3 của 405) | 2 |
| 14 | 98687A327 | M24 WASHER | Vòng đệm M24 | 2 |
| 15 | 305 | STROKE POSITIONING BLOCK | Khối định vị hành trình (thép, lỗ Ø24.5) | 1 |
| 16 | 6141 FK-M12X1,25---(asm_0_0) | MISALIGNMENT COUPLER | Khớp nối tự lựa cần piston Festo FK-M12×1,25 | 1 |
| 17 | 8092076 ADN-S-50-20-A-P-A---(0_high) | SQUARE BODY CYLINDER | Xi lanh thân vuông Festo ADN-S-50-20 — **xi lanh đột MM4** | 1 |
| 18 | 91290A344 | M6 X 60 SHCS | Vít lục giác chìm M6 × 60 | 4 |
| 19 | SPTWA20-40-P6.5-B5-V8-F12 | PUNCH | Chày đột Misumi Ø20 thân, mũi Ø6.5 (= 407) | 1 |
| 20 | 91290A326 | M6 X 20 SHCS | Vít lục giác chìm M6 × 20 | 3 |

**Chiều cao đóng (shut height):** vặn 405 (ren M24×3) qua khối 305 và khoá bằng 2 đai ốc M24 để mũi chày Ø6.5 xuyên qua phôi 0.5 mm vào cối ADX20 (lỗ 6.6) ở điểm chết dưới của MM4.

## 6. Bản vẽ chi tiết gia công 401, 404, 405 — xem số liệu đầy đủ trong `04-module-C-tien-phay.md`

Ghi chú riêng:

| Bản vẽ | EN | VI |
|---|---|---|
| 401 | SECTION B-B REMOVED | Mặt cắt B-B dạng tách (vẽ rời khỏi hình chiếu) |
| 401 | 2 x REAM Ø10.00 THRU ALL | 2 lỗ Ø10.00 doa xuyên |
| 401 | REAM Ø20 H8 +0.033/0.000, depth 20 +0.10/−0.00 | Lỗ doa Ø20 H8 sâu 20 (+0.10/−0) |
| 401 | REAM Ø12 H8 +0.027/0.000, depth 28.6 | Lỗ doa Ø12 H8 sâu 28.6 |
| 401 | 4x Ø3.3 ↧15, M4x0.7 – 6H ↧8 | 4 lỗ mồi Ø3.3 sâu 15, ren M4×0.7 6H sâu 8 |
| 401 | 2x Ø11 THRU ALL; Ø10.5 | 2 lỗ Ø11 xuyên; 1 lỗ Ø10.5 |
| 401 | ⌖ 0.15 D E; ⟂ 0.05 D; 0.05 C D | Dung sai vị trí 0.15 so với chuẩn D, E; vuông góc 0.05 với D; 0.05 với C và D |
| 404 | SECTION I-I (2:1); Ø20 H8 +0.033/0.000; Ø25.10/25.05; 5.1/5.0; 0.5 X 45°; Ra 1.6; ⟂ 0.02 F | Mặt cắt I-I; lỗ Ø20 H8; trụ Ø25 (25.05–25.10); sâu 5.0–5.1; vát 0.5 × 45°; nhám 1.6; vuông góc 0.02 với F |
| 405 | M24 X 3 – 6g, MAJOR DIAMETER 23.952 / 23.577, PITCH DIAMETER 22.003 / 21.803 | Ren M24 × 3 cấp 6g, đường kính đỉnh 23.577–23.952, **đường kính trung bình 21.803–22.003** (mục chấm 2.0 điểm) |
| 405 | Ø85 f8 −0.036/−0.090; Ø58 0.00/−0.03; Ø20; 93; 12; 15; 120; Ø6.8 ↧20, M8x1.25 – 6H ↧16; 4x Ø5 THRU ALL, M6x1.0 – 6H THRU ALL; 1 X 45°; Ra 1.6 trên Ø85; ◎ 0.03 B; ⟂ 0.1 A | Các kích thước tiện và ren; đồng tâm 0.03 với B; vuông góc 0.1 với A |
| 405 (pre-release, phôi) | NUMBER 4 CENTER BOTH ENDS AS SHOWN; Ø100 × 125 | Khoan tâm số 4 hai đầu; phôi Ø100 dài 125 |

## 7. Bản vẽ lắp 500 — Tấm linh kiện khí nén (WSC2026_TP01_CA_500_EN, N.T.S.)

Bản thật chỉ ghi vị trí các phần tử trên tấm: hàng trên **QMA3, QMA4** (2 nút nhấn hai tay), **KHB1 … KHB5** (phần tử OR/AND), **QMA5, QMA6** (van chọn chế độ, khối hai tay), hàng dưới **QMA7, QMA9, QMA12, QMA15, QMA16** (van 5/2) — ý nghĩa mã ở `07-so-do-khi-nen.md`.

Bản pre-release 500: tấm nhôm 750 × 250 (gốc X–Y góc dưới trái), "USE HOLE CHART FOR POSITION AND SIZE OF UNSPECIFIED HOLES. TAGS REMOVED FOR CLARITY" (dùng **bảng toạ độ lỗ** X LOC / Y LOC / SIZE cho các lỗ không ghi; nhãn bỏ cho dễ nhìn); các lỗ Ø4.2 xuyên + M5×0.8 6H, Ø3.3 + M4×0.7 6H, Ø2.5 + M3×0.5 6H, Ø6.5, Ø23 xuyên; hàng lỗ "50 X 7 PITCHES" (7 bước 50 mm); DETAIL H 1:2. **Cấp sẵn**, thí sinh chỉ gắn van và đi ống.

## 8. Bản vẽ 1000 — Phôi/sản phẩm (WSC2026_TP01_CA_1000_EN, 1:1)

| EN | VI |
|---|---|
| MATERIAL IS 0.5 THICK | Vật liệu dày 0.5 mm (nhôm) |
| 200; 25.0 / 24.5 | Dài 200; rộng 25.0 / 24.5 (phôi) |
| DOWN 70° R 5 (×2) | Uốn xuống 70°, bán kính trong R5, hai bên |
| 110° ±15° TYP | Góc sau uốn 110° ±15°, cả hai bên (mục F1 "piece part within dimensional tolerances", 1.5 điểm) |
| MTL: ALUM, QNTY: 1 | Nhôm; 1 (thí sinh được cấp nhiều phôi để ra 3 sản phẩm) |

## 9. Bản vẽ 200 — Cụm hàn (WSC2026_TP01_CA_200_EN, 2 tờ, 1:5; VIEW ON ARROW A 1:10; DETAIL M 2:5) và 201–207

Ghi chú trên bản vẽ 200:

| EN | VI |
|---|---|
| NO WELD OR TACK ON THIS FACE ON ANY MEMBER | **Không hàn, không hàn đính lên mặt này của bất kỳ thanh nào** (mặt lắp tấm lưng 301) |
| NOTE: DO NOT GRIND WELDS | **Không mài mối hàn** (chuyên gia chấm biên dạng mối hàn nguyên trạng) |
| Z3 TYP (ký hiệu hàn ISO 2553) | Mối hàn góc, cạnh mối hàn Z = 3 mm, mọi vị trí tương tự (chấm 3–4 mm) |
| 3 TYP | Cạnh/khe 3 mm điển hình |
| 13; 15; 117; 105; 57.5 TYP; 0 | Kích thước định vị (giữ nguyên) |
| VIEW ON ARROW A | Hình chiếu theo hướng mũi tên A |

BOM 200:

| Item | Mã | Mô tả EN | Mô tả VI | SL |
|---|---|---|---|---|
| 1 | 201 | 50 X 50 X 2 X 300 SHS | Thép hộp vuông 50 × 50 × 2, dài 300 (chân) | 4 |
| 2 | 204 | 50 X 50 X 2 X 500 SHS | Hộp vuông, dài 500 (thanh dài khung trên) | 2 |
| 3 | 202 | 50 X 50 X 2 X 300 SHS | Hộp vuông, dài 300 (thanh hông) | 2 |
| 4 | 203 | 50 X 50 X 2 X 400 SHS | Hộp vuông, dài 400 (thanh trước/sau) | 2 |
| 5 | 206 | 50 X 50 X 2 X 375 SHS | Hộp vuông, dài 375, vát 25° (chống chéo) | 2 |
| 6 | 205 | 50 X 50 X 2 X 275 SHS | Hộp vuông, dài 275 (thanh ngắn khung trên) | 2 |
| 7 | 207 | 50 X 50 X 2 X 400 L | Thép góc L 50 × 50 × 2, dài 400 (đáy, phẳng đáy với 201) | 2 |

Ghi chú bản vẽ 201–207 (WSC2026_TP01_CA_201-4_EN, 205-7_EN, 1:2):

| Chi tiết | EN | VI |
|---|---|---|
| 201 | 2x Ø3.3 THRU, M4x0.7 NEAR SIDE ONLY; NOTE: HOLES IN ONE PART ONLY; TYPICAL SECTION; 57.5, 17.5, 28, 50 | 2 lỗ Ø3.3 ta-rô M4×0.7 **chỉ mặt gần**; **chỉ khoan ở 1 trong 4 chân**; mặt cắt điển hình (hộp 50, thành 2) |
| 204 | 2x Ø12 THRU ALL; 202.5; 95; 15 | 2 lỗ Ø12 xuyên suốt tại 202.5 và 95, cách mép 15 |
| 205 | Ø12 THRU ALL; Ø6.5 THRU ALL; 25; 50; 225; 105 | Lỗ Ø12 và Ø6.5 xuyên suốt |
| 206 | 25°; 65 | Vát đầu 25° |
| 207 | 5; 50; 50 | Thép góc, cạnh 50 |

## 10. Bảng mã chi tiết — vật liệu, số lượng, ai làm

Theo bộ bản vẽ pre-release mọi tờ đều ghi **"SUPPLIED TO THE COMPETITOR"** (cấp cho thí sinh), nghĩa là **phôi hoặc chi tiết hoàn chỉnh được cấp**; cột "Thí sinh làm gì" lấy từ đề thật B, C, D.

| Mã | Tên EN | Tên VI | Vật liệu | SL | Cấp | Thí sinh làm gì |
|---|---|---|---|---|---|---|
| 101 | SHORT ARM | Tay đòn ngắn (tấm chắn) | ALUM | 2 | hoàn chỉnh | lắp |
| 102 | LONG ARM | Tay đòn dài | ALUM | 2 | hoàn chỉnh | lắp |
| 103 | PART PRESENT CHECK PIN | Chốt báo có phôi | STEEL | 1 | hoàn chỉnh | lắp với van con lăn |
| 104 | SAFETY SWITCH STRIKER | Vấu tác động công tắc an toàn | ALUM | 1 | hoàn chỉnh | lắp |
| 105 | HANDLE | Tay cầm, ren M6 | ACETAL | 1 | hoàn chỉnh | lắp |
| 106 | PART PRESENT VALVE BRACKET | Giá van báo phôi | ALUM | 1 | hoàn chỉnh | lắp |
| 107 | SAFETY SHIELD (500 × 350, R10, 2 × Ø7 BOTH SIDES, 2 × Ø5 NEAR SIDE ONLY) | Tấm chắn an toàn | LEXAN | 1 | hoàn chỉnh | lắp, Nylock không siết |
| 201 | 50 × 50 × 2 × 300 SHS | Chân | STEEL | 4 | thanh cắt sẵn | khoan M4 ở 1 chân, hàn |
| 202 | 50 × 50 × 2 × 300 SHS | Thanh hông | STEEL | 2 | thanh cắt sẵn | hàn |
| 203 | 50 × 50 × 2 × 400 SHS | Thanh trước/sau | STEEL | 2 | thanh cắt sẵn | hàn |
| 204 | 50 × 50 × 2 × 500 SHS | Thanh dài khung trên | STEEL | 2 | thanh cắt sẵn | khoan 2 × Ø12, hàn |
| 205 | 50 × 50 × 2 × 275 SHS | Thanh ngắn khung trên | STEEL | 2 | thanh cắt sẵn | khoan Ø12, Ø6.5, hàn |
| 206 | 50 × 50 × 2 × 375 SHS | Chống chéo | STEEL | 2 | thanh cắt sẵn | cắt vát 25°, hàn |
| 207 | 50 × 50 × 2 × 400 L | Thép góc đáy | STEEL | 2 | thanh cắt sẵn | hàn phẳng đáy |
| 301 | BACK PLATE (301P) | Tấm lưng | STEEL | 1 | tấm mài sẵn | **lấy dấu, khoan, ta-rô 20 lỗ**, doa Ø9.5 khi lắp |
| 302 | HEEL SLIDE | Con trượt gót | BRASS | 2 | hoàn chỉnh | lắp, phải trượt tự do |
| 303 / 304 | BENDING WIPER / PUNCH (BOM 300: 304 + 305) | Má uốn trái/phải, M10×1.25 | ACETAL | 1 + 1 | hoàn chỉnh | lắp |
| 305 | STROKE POSITIONING BLOCK (Ø24.5) | Khối định vị hành trình | STEEL | 1 | hoàn chỉnh | lắp, chỉnh shut height |
| 401 | DIE BLOCK | Khối cối | STEEL | 1 | **phôi** 130 × 55 × 53 | **phay** (C3, 13.4 đ) |
| 402 (A, B, C) | CLAMP / SPACER | Kẹp / căn | STEEL | 1 (+2) | hoàn chỉnh | lắp |
| 403 | PUNCH PLATE (75 ±0.01 tâm lỗ, Ø20 H8, M12×1.25) | Tấm mang chày | ALUM | 1 | hoàn chỉnh | lắp, doa bạc nếu kẹt |
| 404 | PUNCH HOLDER | Đầu giữ chày | ALUM | 1 | **phôi** | **tiện** (C2, 3.5 đ) |
| 405 | STROKE POSITIONING SCREW | Vít định vị hành trình, M24×3 | STEEL | 1 | **phôi** Ø100 × 125 | **tiện** (C1, 9.1 đ) |
| 407 | PUNCH — MISUMI SPTWA20-40-P6.5-B5-V8-F12 | Chày đột | M2 | 1 | mua sẵn | lắp |
| 408 | DIE BUTTON — MISUMI ADX20-A20AM2AP6.6 | Cối đột | M2 | 1 | mua sẵn | lắp |
| 409 | FLANGED SLEEVE BEARING — McMASTER-CARR 2934T138 | Bạc trượt có vai | BRONZE | 2 | mua sẵn | lắp vào 403, doa nếu cần |
| 410 | GUIDE PIN — MISUMI VFJT12-100-M6 | Chốt dẫn hướng | STEEL | 2 | mua sẵn | lắp |
| 500 | PNEUMATIC COMPONENT PLATE (750 × 250) | Tấm linh kiện khí nén | ALUM | 1 | hoàn chỉnh | gắn van, đi ống |
| 1000 | WORKPIECE | Phôi/sản phẩm, dày 0.5 | ALUM | nhiều | phôi | máy đột–uốn ra 3 cái |

## 11. Chữ viết tắt và ký hiệu trên bản vẽ

| Ký hiệu | EN | VI |
|---|---|---|
| NTS / N.T.S. | Not to scale | Không theo tỷ lệ |
| TYP | Typical | Điển hình — áp dụng cho mọi vị trí tương tự |
| THRU / THRU ALL | Through / through all | Xuyên / xuyên suốt |
| NEAR SIDE ONLY | | Chỉ mặt gần (mặt nhìn thấy) |
| BOTH SIDES | | Cả hai mặt |
| ↧ 15 (depth symbol) | Depth | Sâu 15 |
| Ø / R | Diameter / radius | Đường kính / bán kính |
| H8, H8 +0.033/0.000 | Hole tolerance ISO | Lỗ cấp H8, miền +0.033/0 |
| f8 −0.036/−0.090 | Shaft tolerance ISO | Trục cấp f8 |
| 6H / 6g | Thread tolerance | Ren trong 6H / ren ngoài 6g |
| M24 X 3 | Metric thread, pitch 3 | Ren hệ mét Ø24 bước 3 |
| Ra 1.6 / 3.2 | Surface roughness | Độ nhám trung bình số học, µm |
| ⌖ 0.15 D E | Position tolerance | Dung sai vị trí 0.15 so với chuẩn D, E |
| ⟂ 0.05 D | Perpendicularity | Độ vuông góc 0.05 so với chuẩn D |
| ◎ 0.03 B | Concentricity | Độ đồng tâm 0.03 so với chuẩn B |
| A, B, C, D, E, F (trong khung) | Datum | Chuẩn |
| ISO 2768-1 fK / m | General tolerances | Dung sai chung ISO 2768-1 |
| SHCS | Socket head cap screw | Vít lục giác chìm đầu trụ |
| HHCS | Hex head cap screw | Bu-lông đầu lục giác ngoài |
| SHS | Square hollow section | Thép hộp vuông |
| L | Angle | Thép góc chữ L |
| MTL / QNTY / QTY | Material / quantity | Vật liệu / số lượng |
| C/W | Complete with | Kèm theo |
| P.C.D. | Pitch circle diameter | Đường kính vòng tròn chia (lỗ cách đều trên vòng) |
| EQUALY SPACED | Equally spaced | Cách đều |
| REAM | | Doa |
| BLANCHARD GRIND | | Mài phẳng (máy mài Blanchard) |
| CROPED VIEW | Cropped view | Hình chiếu cắt bớt |
| SECTION B-B REMOVED | | Mặt cắt tách rời |
| DETAIL G, SCALE 1:2 | | Hình trích G, tỷ lệ 1:2 |
| VIEW ON ARROW A | | Hình chiếu theo hướng mũi tên A |
| DOWN 70° R 5 | Bend down 70°, inside radius 5 | Uốn xuống 70°, bán kính R5 |
| Dwg No: 1 of 3 | Drawing number | Tờ 1 trong 3 |
| SCM | Skill Competition Manager | Quản lý thi nghề |
| ALUM / ACETAL / LEXAN / M2 | | Nhôm / POM / polycarbonate / thép gió M2 |
| 91290A129 … | McMaster-Carr part number | Mã McMaster-Carr (giữ nguyên) |
| 536273 ADN-32-30-A-P-A | Festo part number + type code | Mã đặt hàng Festo + mã kiểu (giữ nguyên) |

## Ghi chú bản gốc

- `loi-ban-goc.md` #14: ngày "26_08_2026"/"25/08/2026"/"JANUARY 2026" trộn; "Dwg No: XX of XX" chưa điền ở pre-release.
- Mới (#15): chiều dài thanh 201 (350→300), 202 (350→300), 205 (310→275), 206 (450→375) khác nhau giữa pre-release và bản thật — dùng bản thật.
- Mới (#16): ghi chú "TOLERANCE CLASS IS m (MEDIUM)" đi kèm "ISO2768-1fk" trên 401/404/405.
- Mới (#17): BOM 400 trùng mã: item 1 và 12 cùng "401" (die block / stroke positioning screw = Detail 405); item 2 và 7 cùng "402" (clamp / spacer).
- Mới (#18): số hiệu má uốn: pre-release 303 + 304 (acetal), 305 = khối định vị thép; BOM 300 ghi "304 + 305 BENDING PUNCH"; thang điểm D2 ghi 304 trái / 305 phải.
- Bản vẽ 107 ghi "BOTH SIDES" cho 2 × Ø7 và "NEAR SIDE ONLY" cho 2 × Ø5 — bình thường; nhưng 100 BOM dùng 8 Nylock M6 cho tấm chắn trong khi 107 chỉ có 4 lỗ — số Nylock còn lại nằm ở tay đòn 101/102; không phải lỗi, ghi để khỏi thắc mắc.
- "EQUALY SPACED", "CROPED VIEW", "CLARTITY" — lỗi chính tả, bỏ qua.
