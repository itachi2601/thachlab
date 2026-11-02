# 07 — Sơ đồ khí nén (Pneumatics Build, WS26_250603 rev 13)

Nguồn: `WS2026_TP01_Pneumatics Build` — bản vẽ Festo FluidDRAW, 6 tờ: 1 Mục lục + lịch sử sửa đổi, 2 Air Prep (xử lý khí), 3 Main Circuit (mạch điều khiển), 4 Actuators (cơ cấu chấp hành), 5 Parts List (danh sách linh kiện), 6 Tubing List (danh sách ống). Vẽ: ACK (Jim Ackert, Festo), 2026-09-08, rev 13. Tiêu đề: "2026 WS Industrial Mechanic 01 — WorldSkills Shanghai 2026".

> **Dùng để huấn luyện**
> - **Điểm liên quan:** E1 đi ống **10.4**, F1 vận hành **7.5** (chuỗi đúng 2.0, khoá liên động 2.0), G1 sửa lỗi FluidSIM **2.5** = **20.4 điểm** phụ thuộc vào việc thuộc sơ đồ này.
> - **Điểm dễ lấy:** 74 ống đều có tên WQG1–WQG74 với điểm đầu, điểm cuối, số cổng và đường kính — lắp theo bảng ống như theo "công thức", đánh dấu từng ống đã lắp; dùng đúng Ø4 cho tín hiệu, Ø6 cho nguồn và xi lanh.
> - **Bẫy mất điểm:** cổng **12 và 14** trên van VUWG-L10-B52 đổi chỗ → xi lanh chạy ngược chuỗi (−2 điểm/lượt thử thêm); cảm biến SMPO-8E gắn sai đầu xi lanh; tiết lưu GRLA lắp ngược chiều (chỉnh xả); quên nút bịt (B-M5-B, B-M7, B-1/8) → xì khí; ống bẹp dưới dây rút; **không khoá khí** (van đóng/mở trên MS4) trước khi tháo ống = vi phạm an toàn −0.5.

## 1. Chuỗi hoạt động (Circuit Sequence) — giải thích bằng lời

**Circuit Sequence: (MM1+, MM2+ & MM3+, MM4+) (MM1−, MM2− & MM3−, MM4−)**

Bốn xi lanh (tờ 4, "Actuators"):

| Mã | Tên trên sơ đồ | Xi lanh Festo | Vai trò |
|---|---|---|---|
| -MMB1 (MM1) | Clamping Cylinder | AEN-32-10-A-P-A (Ø32, hành trình 10, cần piston lùi vào) | **Kẹp phôi** lên khối cối 401; cần có khớp tự lựa FK-M12×1,25 |
| -MMB2 (MM2) | Bending Cylinder 1 | ADN-32-30-A-P-A (Ø32, hành trình 30) | **Uốn cánh trái**: kéo con trượt gót 302 dọc má uốn |
| -MMB3 (MM3) | Bending Cylinder 2 | ADN-32-30-A-P-A | **Uốn cánh phải** (đồng thời với MM2) |
| -MMB4 (MM4) | Punch Cylinder | ADN-S-50-20-A-P-A (Ø50, hành trình 20) | **Đột lỗ** Ø6.5 qua tấm mang chày 403 |

[Ghi chú dịch: tờ 4 rev 13 ghi mã xi lanh là **-MMB1…-MMB4** (ba chữ, EN IEC 81346-2:2019), còn dòng Circuit Sequence trên tờ 1, đề A2 và thang điểm F1 viết tắt **MM1…MM4**. Cùng một xi lanh. Bản dịch dùng MM1…MM4 khi nói về chuỗi, -MMB khi tra bảng linh kiện.]

Diễn giải một chu trình (dấu + = đi ra/duỗi, − = đi về/co):

1. **Điều kiện khởi động:** khí đã cấp qua bộ xử lý -AZA1 (8.0 bar); **cửa chắn đóng** → công tắc cửa -QMA1 (VMEF-RT-M32, "Gate Switch") được nhấn, cho khí qua; **có phôi** → chốt báo phôi 103 nhấn van con lăn -QMA2 (R-3-M5, "Part Present"); công tắc chọn -SGA1 (N-22-SW, "Reset Switch") ở vị trí chạy.
2. **Nhấn hai nút cùng lúc** -SGC1 và -SGC2 (T-22-GE trên van SV-3-M5 -QMA3, -QMA4) → khối hai tay -QMA6 (ZSB-1/8-B) chỉ cho tín hiệu ra khi hai nút nhấn gần đồng thời (an toàn hai tay).
3. **Bước 1 — MM1+:** tín hiệu khởi động đặt van -QMA7 (VUWG-L10-M52, 5/2 lò xo) và qua -QMA9 → van 5/3 -QMA20 (VUWG-L10-P53C-M7) cấp khí cho **MM1 đi ra, kẹp phôi**. Tốc độ do tiết lưu -RNB1 (GR-M5X2-B).
4. **Bước 2 — MM2+ & MM3+:** cảm biến cuối hành trình MM1 (-QMA8, SMPO-8E) báo kẹp xong → qua van -QMA12 → van -QMA21 cấp khí cho **MM2 và MM3 cùng đi ra, uốn hai cánh** (ống chia bằng chữ Y -XMA20, -XMA21; tiết lưu -RNB2…-RNB5).
5. **Bước 3 — MM4+:** cảm biến cuối hành trình MM2 và MM3 (-QMA10, -QMA14) qua phần tử **AND** -KHB3/-KHB4/-KHB5 (ZK-PK-3) → van -QMA15/-QMA16 → van -QMA22 cấp khí cho **MM4 đi ra, đột lỗ** (tiết lưu -RNB6, -RNB7).
6. **Bước 4 — MM1−:** cảm biến cuối hành trình MM4 (-QMA18) đổi trạng thái → **MM1 đi về, nhả kẹp**.
7. **Bước 5 — MM2− & MM3−:** cảm biến đầu hành trình MM1 (-QMA11) → **MM2, MM3 đi về**.
8. **Bước 6 — MM4−:** cảm biến đầu hành trình MM2, MM3 (-QMA13, -QMA17) qua AND → **MM4 đi về**. Máy sẵn sàng chu trình mới; chuỗi đúng = F1 2.0 điểm.
9. **Khoá liên động (interlock):** mở cửa chắn (QMA1 nhả) hoặc rút phôi (QMA2 nhả) thì nguồn khí điều khiển cắt → máy dừng/không khởi động — F1 2.0 điểm. Phần tử **OR** -KHB1, -KHB2 (OS-PK-3) gom tín hiệu reset/điều kiện.

[Ghi chú dịch: thứ tự cảm biến–van trong các bước 3–8 suy ra từ bảng ống WQG và vị trí phần tử; muốn luyện chi tiết hãy mở sơ đồ PDF tờ 3–4 và dò theo từng WQG trong mục 4.]

## 2. Mã tham chiếu (Reference designation, EN IEC 81346-2:2019)

Mỗi phần tử có mã bắt đầu bằng dấu "-" + 3 chữ (lớp đối tượng) + số thứ tự; phần tử con nối tiếp bằng "-": ví dụ `-QMA5-XMA1` = đầu nối số 1 của van số 5; `-AZA2-XMA1-RND1` = nút bịt 1 trên đầu nối 1 của thanh gom 2.

| Mã | Lớp đối tượng (EN) | Nghĩa VI | Ví dụ trong sơ đồ |
|---|---|---|---|
| -MMB | Pneumatic linear actuator (cylinder) | **Xi lanh** khí nén (MM trong chuỗi) | -MMB1 kẹp, -MMB2/-MMB3 uốn, -MMB4 đột |
| -QMA | Valve, directional / control | **Van** phân phối, van hành trình, nút nhấn van, cảm biến khí | -QMA1 công tắc cửa, -QMA2 báo phôi, -QMA3/-QMA4 nút hai tay, -QMA5 van chọn SV-5, -QMA6 khối hai tay, -QMA7/-QMA9/-QMA12/-QMA15/-QMA16 van 5/2, -QMA8/-QMA10/-QMA11/-QMA13/-QMA14/-QMA17/-QMA18/-QMA19 cảm biến SMPO-8E, -QMA20…-QMA22 van 5/3 cấp xi lanh |
| -KHB | Logic element (pneumatic) | **Phần tử logic** AND / OR | -KHB1, -KHB2 OR (OS-PK-3); -KHB3…-KHB5 AND (ZK-PK-3) |
| -KHA | Pressure control / regulating element | Phần tử điều áp (trong bộ xử lý khí) | -AZA1-KHA1 |
| -XMA | Connector, fitting | **Đầu nối** ống (thẳng, L, T, Y) | -XMA2, -XMA3 chữ T Ø6; -XMA4…-XMA19 chữ T/Y Ø4; -XMA20, -XMA21 chữ Y Ø6 |
| -GQA | Pneumatic supply (compressor / air source) | **Nguồn khí** nén | -GQA1 |
| -AZA | Assembly / unit (air preparation, manifold) | **Cụm**: bộ xử lý khí, thanh gom | -AZA1 bộ xử lý MS4; -AZA2 thanh gom VABM |
| -SGC | Manual control, pushbutton | **Nút nhấn** (tay) | -SGC1, -SGC2 (T-22-GE) hai tay |
| -SGA | Manual control, selector switch | **Công tắc chọn** | -SGA1 (N-22-SW) Reset |
| -RNB | Flow restrictor (flow control) | **Tiết lưu** một chiều | -RNB1 (GR-M5X2-B), -RNB2…-RNB7 (GRLA-1/8-QS-6-D) |
| -RND | Blanking (closing) element | **Nút bịt** cổng | -QMA7-RND1, -AZA2-XMA1-RND1 |
| -RMB | Blanking plug (M7) | Nút bịt (trên van P53C) | -QMA20-RMB1 |
| -RQC | Silencer | **Bộ giảm thanh** | -QMA1-RQC1, -QMA5-RQC2 |
| -UQA | Mounting (sensor kit) | Bộ gá cảm biến | -QMA8-UQA1 (SMB-8E) |
| -UPA / -UPB | Mounting accessory (flange / foot, coupler) | Mặt bích xoay / đế chạc, khớp nối cần | -MMB2-UPA1 (SNCS-32), -MMB2-UPB1 (LBG-32), -MMB1-UPB1 (FK-M12X1,25) |
| WQG1…WQG74 | Pneumatic tubing (line) | **Ống** khí số 1…74 | xem mục 4 |
| P1…P9 | Page connector | Mối nối liên trang (tín hiệu sang tờ khác), ví dụ `P4 /4.D3` = tiếp ở tờ 4 ô D3 | |
| /2.E4 | Location | Vị trí trên bản vẽ: tờ 2, hàng E, cột 4 | |
| 1, 2, 3, 4, 5 / 12, 14 / P(1), A(2), R(3) | Port numbers (ISO 11727) | Số cổng van: 1 = cấp khí, 2, 4 = ra làm việc, 3, 5 = xả, 12/14 = cổng điều khiển (đẩy sang nối 1→2 / 1→4); P/A/R là ký hiệu cũ trên SV-3-M5 | |

## 3. Danh sách linh kiện (Parts List, tờ 5) — mã Festo giữ nguyên

Cột: Pos. (số vị trí trên BOM), Part number (mã đặt hàng Festo), Quantity, Order code (mã kiểu), Item name, mô tả VI, Identification (mã tham chiếu các phần tử dùng mã này), Location (tờ.ô). Nhà cung cấp: Festo cho mọi dòng.

| Pos. | Mã Festo | SL | Mã kiểu (Order code) | Tên EN | Mô tả VI | Mã tham chiếu (Identification) | Vị trí sơ đồ |
|---|---|---|---|---|---|---|---|
| 20 | 531666 | 1 | KS3-1/4-A | Quick coupling plug | Đầu cắm khớp nối nhanh (phía ống cấp khí) | -AZA1-QMA1-XMA1 | /2.E4 |
| 30 | 8098373 | 1 | MS4-EM1FR-1/4-D6-C-P-M-AG-BAR-WPE-B | Service unit | Bộ xử lý khí: van đóng/mở + lọc 5 µm + điều áp có đồng hồ bar (đặt 8.0 bar) | -AZA1 | /2.E5 |
| 40 | 186118 | 1 | QSL-G1/4-6 | Push-in L-fitting | Đầu nối cắm nhanh chữ L (cút góc) | -AZA1-KHA1-XMA1 | /2.E5 |
| 50 | 2316 | 1 | U-1/4 | Silencer | Bộ giảm thanh (ống xả) | -AZA1-QMA1-RQC1 | /2.E5 |
| 60 | 8049239 | 1 | VMEF-RT-M32-M-G18 | Roller lever valve | Van cần con lăn 3/2 (van hành trình) | -QMA1 | /2.E6 |
| 70 | 186107 | 3 | QS-G1/8-6-I | Push-in fitting | Đầu nối cắm nhanh thẳng | -QMA1-XMA1, -QMA1-XMA2, -AZA2-XMA1-XMA1 | /2.E6, /2.E6, /4.C4 |
| 80 | 153134 | 2 | QST-6-4 | Push-in T-connector | Đầu nối cắm nhanh chữ T | -XMA2, -XMA3 | /2.E6, /2.E7 |
| 90 | 1206622 | 4 | AMTE-M-H-G18 | Silencer | Bộ giảm thanh (ống xả) | -AZA2-XMA5-RQC1, -QMA1-RQC1, -QMA6-RQC1, -AZA2-XMA5-RQC2 | /4.C8, /2.E6, /3.B4, /4.C8 |
| 190 | 153333 | 18 | QSML-M5-4 | Push-in L-fitting | Đầu nối cắm nhanh chữ L (cút góc) | -QMA5-XMA1, -QMA5-XMA3, -QMA15-XMA3, -QMA12-XMA3, -QMA15-XMA2, -QMA16-XMA1, -QMA5-XMA2, -QMA7-XMA1, -QMA20-XMA3, -QMA20-XMA1, -QMA16-XMA3, -QMA21-XMA1, -QMA21-XMA4, -QMA9-XMA3, -QMA22-XMA1, -QMA9-XMA1, -QMA22-XMA4, -QMA12-XMA1 | /3.B8, /3.B8, /3.E5, /3.D5, /3.E4, /3.E4, /3.B8, /3.B7, /4.D5, /4.D4, /3.E5, /4.D5, /4.D6, /3.C5, /4.D6, /3.C5, /4.D7, /3.D5 |
| 310 | 566559 | 1 | VABM-L1-10S-G18-3 | Manifold rail | Thanh gom (manifold) cho van VUWG | -AZA2 | /4.C4 |
| 480 | 197383 | 1 | PUN-H-4X0,75-BL | Plastic tubing | Ống nhựa Ø4 × 0.75, màu xanh (BL) — cuộn | — | /2.F8 |
| 490 | 197390 | 1 | PUN-H-4X0,75-SW | Plastic tubing | Ống nhựa Ø4 × 0.75, màu đen (SW) — cuộn | — | /2.E8 |
| 500 | 558278 | 1 | PUN-H-4X0,75-SI | Plastic tubing | Ống nhựa Ø4 × 0.75, màu bạc (SI) — cuộn | — | /2.E8 |
| 510 | 197384 | 1 | PUN-H-6X1-BL | Plastic tubing | Ống nhựa Ø6 × 1, màu xanh (BL) — cuộn | — | /2.E8 |
| 520 | 197391 | 1 | PUN-H-6X1-SW | Plastic tubing | Ống nhựa Ø6 × 1, màu đen (SW) — cuộn | — | /2.E8 |
| 530 | 558279 | 1 | PUN-H-6X1-SI | Plastic tubing | Ống nhựa Ø6 × 1, màu bạc (SI) — cuộn | — | /2.E8 |
| 540 | 531629 | 1 | KD3-CK-4 | Quick coupling socket | Ổ cắm khớp nối nhanh (phía máy) | -XMA1 | /2.E4 |
| 550 | 9301 | 1 | N-22-SW | Selector switch | Công tắc chọn chế độ (xoay) – Reset | -SGA1 | /3.B8 |
| 560 | 3629 | 1 | R-3-M5 | Roller lever valve | Van cần con lăn 3/2 (van hành trình) | -QMA2 | /3.A3 |
| 570 | 11914 | 1 | SV-5-M5-B | Front panel valve | Van gắn mặt máy 3/2 (SV-3) hoặc 5/2 (SV-5), tác động nút nhấn | -QMA5 | /3.B8 |
| 580 | 574254 | 1 | VUWG-L10-M52-M-M5 | Pneumatic valve | Van phân phối khí nén (VUWG-L10: 5/2 tác động khí hai phía B52, hoặc một phía lò xo M52; P53C = 5/3 vị trí giữa đóng) | -QMA7 | /3.B7 |
| 590 | 576656 | 1 | ZSB-1/8-B | Control block for two-hand start | Khối điều khiển khởi động hai tay (ZSB) | -QMA6 | /3.B4 |
| 600 | 174308 | 2 | B-M5-B | Blanking plug | Nút bịt cổng | -QMA7-RND1, -QMA9-RND1 | /3.B7, /3.C5 |
| 610 | 6817 | 2 | SV-3-M5 | Front panel valve | Van gắn mặt máy 3/2 (SV-3) hoặc 5/2 (SV-5), tác động nút nhấn | -QMA3, -QMA4 | /3.B3, /3.B5 |
| 620 | 186095 | 3 | QS-G1/8-4 | Push-in fitting | Đầu nối cắm nhanh thẳng | -QMA6-XMA3, -QMA6-XMA2, -QMA6-XMA1 | /3.B4, /3.C4, /3.B3 |
| 630 | 1206621 | 14 | AMTE-M-H-M5 | Silencer | Bộ giảm thanh (ống xả) | -QMA7-RQC2, -QMA12-RQC2, -QMA9-RQC1, -QMA4-RQC1, -QMA5-RQC2, -QMA3-RQC1, -QMA15-RQC1, -QMA15-RQC2, -QMA5-RQC1, -QMA16-RQC1, -QMA16-RQC2, -QMA12-RQC1, -QMA7-RQC1, -QMA9-RQC2 | /3.B7, /3.D5, /3.C5, /3.B5, /3.B8, /3.B3, /3.E5, /3.E5, /3.B8, /3.E4, /3.E5, /3.D5, /3.B7, /3.C5 |
| 640 | 130831 | 14 | QSMLV-M5-4-I | Push-in L-fitting | Đầu nối cắm nhanh chữ L (cút góc) | -QMA12-XMA5, -QMA7-XMA2, -QMA4-XMA1, -QMA4-XMA2, -QMA12-XMA4, -QMA16-XMA2, -QMA15-XMA5, -QMA15-XMA4, -QMA3-XMA1, -QMA7-XMA3, -QMA3-XMA2, -QMA15-XMA1, -QMA12-XMA2, -QMA9-XMA4 | /3.D5, /3.B7, /3.B5, /3.B5, /3.D5, /3.E4, /3.E5, /3.E5, /3.B3, /3.B7, /3.B3, /3.E5, /3.D5, /3.C5 |
| 650 | 178230 | 8 | SMB-8E | Mounting kit | Bộ gá cảm biến lên xi lanh | -QMA11-UQA1, -QMA13-UQA1, -QMA10-UQA1, -QMA8-UQA1, -QMA14-UQA1, -QMA17-UQA1, -QMA18-UQA1, -QMA19-UQA1 | /3.D4, /3.D3, /3.D4, /3.C7, /3.D4, /3.G4, /3.G4, /3.G6 |
| 660 | 153128 | 12 | QST-4 | Push-in T-connector | Đầu nối cắm nhanh chữ T | -XMA10, -XMA18, -XMA11, -XMA19, -XMA16, -XMA7, -XMA9, -XMA13, -XMA6, -XMA4, -XMA17, -XMA14 | /3.C5, /3.D8, /3.F6, /3.F8, /3.D7, /3.F5, /3.F5, /3.F3, /3.C4, /3.A3, /3.E7, /3.A7 |
| 670 | 178563 | 8 | SMPO-8E | Proximity sensor | Cảm biến tiệm cận khí nén (báo vị trí piston, SMPO-8E) | -QMA18, -QMA19, -QMA14, -QMA10, -QMA13, -QMA17, -QMA11, -QMA8 | /3.G4, /3.G6, /3.D4, /3.D4, /3.D3, /3.G4, /3.D4, /3.C7 |
| 680 | 153315 | 5 | QSM-M5-4-I | Push-in fitting | Đầu nối cắm nhanh thẳng | -QMA2-XMA2, -QMA2-XMA1, -QMA16-XMA4, -QMA16-XMA5, -QMA9-XMA2 | /3.A3, /3.A3, /3.E4, /3.E5, /3.C5 |
| 690 | 573809 | 4 | VUWG-L10-B52-M5 | Pneumatic valve | Van phân phối khí nén (VUWG-L10: 5/2 tác động khí hai phía B52, hoặc một phía lò xo M52; P53C = 5/3 vị trí giữa đóng) | -QMA15, -QMA16, -QMA9, -QMA12 | /3.E5, /3.E4, /3.C5, /3.D5 |
| 700 | 9290 | 2 | T-22-GE | Pushbutton actuator | Nút nhấn (đầu tác động cho SV-3-M5), màu vàng GE | -SGC2, -SGC1 | /3.B4, /3.B3 |
| 710 | 6685 | 3 | ZK-PK-3 | AND gate | Phần tử AND (van hai áp) | -KHB3, -KHB5, -KHB4 | /3.G3, /3.G7, /3.G5 |
| 720 | 153344 | 15 | QSML-4 | Push-in L-connector | Đầu nối cắm nhanh chữ L (ống–ống) | -KHB2-XMA1, -KHB1-XMA2, -KHB2-XMA2, -KHB2-XMA3, -KHB3-XMA1, -KHB3-XMA3, -KHB4-XMA1, -KHB1-XMA1, -KHB4-XMA2, -KHB4-XMA3, -KHB5-XMA1, -KHB5-XMA3, -KHB5-XMA2, -KHB3-XMA2, -KHB1-XMA3 | /3.E4, /3.D4, /3.E4, /3.E4, /3.G3, /3.G3, /3.G5, /3.D4, /3.G5, /3.G5, /3.G7, /3.G7, /3.G8, /3.G3, /3.E4 |
| 730 | 153148 | 2 | QSY-4 | Push-in Y-connector | Đầu nối cắm nhanh chữ Y | -XMA12, -XMA8 | /3.F6, /3.F4 |
| 740 | 6684 | 2 | OS-PK-3 | OR gate | Phần tử OR (van con thoi) | -KHB2, -KHB1 | /3.E4, /3.D4 |
| 750 | 174309 | 1 | B-M7 | Blanking plug | Nút bịt cổng | -QMA20-RMB1 | /4.D5 |
| 760 | 3568 | 3 | B-1/8 | Blanking plug | Nút bịt cổng | -AZA2-XMA5-RND1, -AZA2-XMA1-RND1, -AZA2-XMA1-RND2 | /4.C8, /4.C4, /4.C4 |
| 770 | 566673 | 3 | VABD-L1-10X-S-M7 | Seal | Tấm đệm/kín cho manifold | -AZA2-XMA4-RNB1, -AZA2-XMA3-RNB1, -AZA2-XMA2-RNB1 | /4.C7, /4.C6, /4.C4 |
| 780 | 573826 | 3 | VUWG-L10-P53C-M7 | Pneumatic valve | Van phân phối khí nén (VUWG-L10: 5/2 tác động khí hai phía B52, hoặc một phía lò xo M52; P53C = 5/3 vị trí giữa đóng) | -QMA22, -QMA21, -QMA20 | /4.D7, /4.D6, /4.D4 |
| 790 | 153321 | 5 | QSM-M7-6-I | Push-in fitting | Đầu nối cắm nhanh thẳng | -QMA20-XMA2, -QMA21-XMA2, -QMA21-XMA3, -QMA22-XMA3, -QMA22-XMA2 | /4.D4, /4.D5, /4.D6, /4.D7, /4.D7 |
| 800 | 8092076 | 1 | ADN-S-50-20-A-P-A | Compact cylinder | Xi lanh compact tác động kép | -MMB4 | /4.F7 |
| 810 | 536418 | 1 | AEN-32-10-A-P-A | Compact cylinder | Xi lanh compact tác động kép | -MMB1 | /4.F4 |
| 820 | 6141 | 1 | FK-M12X1,25 | Self-aligning rod coupler | Khớp nối tự lựa cần piston | -MMB1-UPB1 | /4.F8 |
| 830 | 152611 | 1 | GR-M5X2-B | One-way flow control valve | Van tiết lưu một chiều (chỉnh tốc độ xi lanh) | -RNB1 | /4.F4 |
| 840 | 186117 | 1 | QSL-G1/8-6 | Push-in L-fitting | Đầu nối cắm nhanh chữ L (cút góc) | -MMB1-XMA1 | /4.F4 |
| 850 | 536273 | 2 | ADN-32-30-A-P-A | Compact cylinder | Xi lanh compact tác động kép | -MMB3, -MMB2 | /4.F6, /4.F5 |
| 860 | 31761 | 2 | LBG-32 | Clevis foot | Đế chạc (chân chạc chữ U) cho xi lanh | -MMB2-UPB1, -MMB3-UPB1 | /4.F5, /4.F6 |
| 870 | 174397 | 2 | SNCS-32 | Swivel flange | Mặt bích xoay (lắp xi lanh lắc được) | -MMB3-UPA1, -MMB2-UPA1 | /4.F6, /4.F5 |
| 880 | 193144 | 6 | GRLA-1/8-QS-6-D | One-way flow control valve | Van tiết lưu một chiều (chỉnh tốc độ xi lanh) | -RNB2, -RNB3, -RNB6, -RNB7, -RNB4, -RNB5 | /4.F5, /4.F5, /4.F7, /4.F7, /4.F6, /4.F6 |
| 890 | 153317 | 2 | QSM-M5-6-I | Push-in fitting | Đầu nối cắm nhanh thẳng | -RNB1-XMA2, -RNB1-XMA1 | /4.F4, /4.E4 |
| 900 | 153149 | 2 | QSY-6 | Push-in Y-connector | Đầu nối cắm nhanh chữ Y | -XMA21, -XMA20 | /4.E6, /4.E5 |
Tổng: 46 dòng BOM + 6 cuộn ống. Những thứ **thí sinh phải tự lắp lên tấm 500 và xi lanh**: van VUWG (690, 780) lên thanh gom VABM (310) với đệm (770); nút bịt (600, 750, 760); giảm thanh (90, 630); đầu nối (70, 80, 190, 620, 640, 660, 680, 720, 730, 790, 890, 900); cảm biến SMPO-8E (670) với gá SMB-8E (650); tiết lưu (830, 880); khớp FK (820), đế chạc LBG-32 (860), bích SNCS-32 (870).

## 4. Danh sách ống (Tubing List, tờ 6) — 74 ống

Cách đọc: ống WQGn đi **từ** phần tử A (cổng x, tờ.ô) **đến** phần tử B (cổng y, tờ.ô), đường kính Ø4 (tín hiệu điều khiển) hoặc Ø6 (nguồn khí và cấp xi lanh). "—" = đầu nối T/Y không ghi số cổng. Thí sinh đánh dấu ✓ vào cột đầu khi đã lắp.

| Pos. | Ống | Từ (trang/ô) | Từ phần tử | Cổng | Đến (trang/ô) | Đến phần tử | Cổng | Ø ống |
|---|---|---|---|---|---|---|---|---|
| 1 | WQG1 | /2.D4 | -GQA1 | — | /2.E4 | -XMA1 | 1 | Ø6mm |
| 2 | WQG2 | /2.E5 | -AZA1-KHA1-XMA1 | 2 | /2.E6 | -XMA2 | — | Ø6mm |
| 3 | WQG3 | /2.E7 | -XMA3 | — | /3.A3 | -XMA4 | — | Ø4mm |
| 4 | WQG4 | /2.E6 | -XMA2 | — | /2.E6 | -QMA1-XMA1 | 1 | Ø6mm |
| 5 | WQG5 | /2.E6 | -QMA1-XMA2 | 2 | /2.E7 | -XMA3 | — | Ø6mm |
| 6 | WQG6 | /2.E6 | -XMA2 | — | /3.B5 | -QMA4-XMA1 | P(1) | Ø4mm |
| 7 | WQG7 | /2.E7 | -XMA3 | — | /4.C4 | -AZA2-XMA1-XMA1 | 1 | Ø6mm |
| 8 | WQG8 | /3.A3 | -XMA4 | — | /3.A7 | -XMA14 | — | Ø4mm |
| 9 | WQG9 | /3.A3 | -XMA4 | — | /3.A3 | -QMA2-XMA1 | 1 | Ø4mm |
| 10 | WQG10 | /3.A7 | -XMA14 | — | /3.B8 | -QMA5-XMA1 | 1 | Ø4mm |
| 11 | WQG11 | /3.A3 | -QMA2-XMA2 | 2 | /3.B3 | -QMA3-XMA1 | P(1) | Ø4mm |
| 12 | WQG12 | /3.A7 | -XMA14 | — | /3.B7 | -QMA7-XMA2 | 1 | Ø4mm |
| 13 | WQG13 | /3.B3 | -QMA3-XMA2 | A(2) | /3.B3 | -QMA6-XMA1 | 1 | Ø4mm |
| 14 | WQG14 | /3.B5 | -QMA4-XMA2 | A(2) | /3.B4 | -QMA6-XMA3 | 1 | Ø4mm |
| 15 | WQG15 | /3.C4 | -QMA6-XMA2 | 2 | /3.C4 | -XMA6 | — | Ø4mm |
| 16 | WQG16 | /3.C4 | -XMA6 | — | /3.C5 | -XMA10 | — | Ø4mm |
| 17 | WQG17 | /3.C5 | -XMA10 | — | /3.B7 | -QMA7-XMA1 | 14 | Ø4mm |
| 18 | WQG18 | /3.B7 | -QMA7-XMA3 | 2 | /3.C7 | -QMA8-XMA2 | 1 | Ø4mm |
| 19 | WQG19 | /3.C4 | -XMA6 | — | /3.C5 | -QMA9-XMA1 | 14 | Ø4mm |
| 20 | WQG20 | /3.C5 | -XMA10 | — | /3.C5 | -QMA9-XMA2 | 1 | Ø4mm |
| 21 | WQG21 | /3.C7 | -XMA5 | — | /3.C5 | -QMA9-XMA3 | 12 | Ø4mm |
| 22 | WQG22 | /3.C7 | -QMA8-XMA1 | 2 | /3.C7 | -XMA5 | — | Ø4mm |
| 23 | WQG23 | /3.B8 | -QMA5-XMA2 | 4 | /3.D8 | -XMA18 | — | Ø4mm |
| 24 | WQG24 | /3.C5 | -QMA9-XMA4 | 4 | /3.D5 | -QMA12-XMA2 | 1 | Ø4mm |
| 25 | WQG25 | /3.C7 | -XMA5 | — | /3.D7 | -XMA16 | — | Ø4mm |
| 26 | WQG26 | /3.D4 | -QMA10-XMA1 | 2 | /3.D4 | -QMA14-XMA2 | 1 | Ø4mm |
| 27 | WQG27 | /3.D4 | -QMA11-XMA1 | 2 | /3.D5 | -QMA12-XMA1 | 14 | Ø4mm |
| 28 | WQG28 | /3.D7 | -XMA16 | — | /3.D5 | -QMA12-XMA3 | 12 | Ø4mm |
| 29 | WQG29 | /3.B8 | -QMA5-XMA3 | 2 | /3.F8 | -XMA19 | — | Ø4mm |
| 30 | WQG30 | /3.D4 | -QMA14-XMA1 | 2 | /3.D4 | -KHB1-XMA1 | 1 | Ø4mm |
| 31 | WQG31 | /3.D5 | -QMA12-XMA4 | 4 | /3.E5 | -QMA15-XMA1 | 1 | Ø4mm |
| 32 | WQG32 | /3.D7 | -XMA16 | — | /3.E7 | -XMA17 | — | Ø4mm |
| 33 | WQG33 | /3.D3 | -QMA13-XMA1 | 2 | /3.E4 | -KHB2-XMA1 | 1 | Ø4mm |
| 34 | WQG34 | /3.F5 | -XMA9 | — | /3.D4 | -QMA10-XMA2 | 1 | Ø4mm |
| 35 | WQG35 | /3.D8 | -XMA18 | — | /3.E4 | -KHB2-XMA2 | 1 | Ø4mm |
| 36 | WQG36 | /3.E4 | -KHB1-XMA3 | 2 | /3.E4 | -QMA15-XMA2 | 14 | Ø4mm |
| 37 | WQG37 | /3.D8 | -XMA18 | — | /3.D4 | -KHB1-XMA2 | 1 | Ø4mm |
| 38 | WQG38 | /3.E7 | -XMA17 | — | /3.E5 | -QMA15-XMA3 | 12 | Ø4mm |
| 39 | WQG39 | /3.F3 | -XMA13 | — | /3.D4 | -QMA11-XMA2 | 1 | Ø4mm |
| 40 | WQG40 | /3.F5 | -XMA7 | — | /3.D3 | -QMA13-XMA2 | 1 | Ø4mm |
| 41 | WQG41 | /3.E7 | -XMA17 | — | /3.E5 | -QMA16-XMA3 | 12 | Ø4mm |
| 42 | WQG42 | /3.D5 | -QMA12-XMA5 | 2 | /3.F3 | -XMA13 | — | Ø4mm |
| 43 | WQG43 | /3.E4 | -KHB2-XMA3 | 2 | /3.E4 | -QMA16-XMA1 | 14 | Ø4mm |
| 44 | WQG44 | /3.E5 | -QMA15-XMA4 | 4 | /3.E4 | -QMA16-XMA2 | 1 | Ø4mm |
| 45 | WQG45 | /3.E5 | -QMA15-XMA5 | 2 | /3.F5 | -XMA9 | — | Ø4mm |
| 46 | WQG46 | /3.E4 | -QMA16-XMA4 | 4 | /3.F4 | -XMA8 | — | Ø4mm |
| 47 | WQG47 | /3.E5 | -QMA16-XMA5 | 2 | /3.F5 | -XMA7 | — | Ø4mm |
| 48 | WQG48 | /3.F8 | -XMA19 | — | /3.F6 | -XMA11 | — | Ø4mm |
| 49 | WQG49 | /3.F3 | -XMA13 | — | /3.G3 | -KHB3-XMA1 | 1 | Ø4mm |
| 50 | WQG50 | /3.F6 | -XMA11 | — | /3.G3 | -KHB3-XMA2 | 1 | Ø4mm |
| 51 | WQG51 | /3.F4 | -XMA8 | — | /3.G4 | -QMA17-XMA2 | 1 | Ø4mm |
| 52 | WQG52 | /3.F4 | -XMA8 | — | /3.F6 | -XMA12 | — | Ø4mm |
| 53 | WQG53 | /3.F5 | -XMA7 | — | /3.G7 | -KHB5-XMA1 | 1 | Ø4mm |
| 54 | WQG54 | /3.F5 | -XMA9 | — | /3.G5 | -KHB4-XMA1 | 1 | Ø4mm |
| 55 | WQG55 | /3.F6 | -XMA11 | — | /3.G5 | -KHB4-XMA3 | 1 | Ø4mm |
| 56 | WQG56 | /3.F8 | -XMA19 | — | /3.G8 | -KHB5-XMA2 | 1 | Ø4mm |
| 57 | WQG57 | /3.F6 | -XMA12 | — | /3.G6 | -QMA19-XMA2 | 1 | Ø4mm |
| 58 | WQG58 | /3.G4 | -QMA17-XMA1 | 2 | /3.G4 | -QMA18-XMA2 | 1 | Ø4mm |
| 59 | WQG59 | /3.G3 | -KHB3-XMA3 | 2 | /4.D4 | -QMA20-XMA1 | 14 | Ø4mm |
| 60 | WQG60 | /3.G4 | -QMA18-XMA1 | 2 | /4.D5 | -QMA20-XMA3 | 12 | Ø4mm |
| 61 | WQG61 | /3.G5 | -KHB4-XMA2 | 2 | /4.D5 | -QMA21-XMA1 | 14 | Ø4mm |
| 62 | WQG62 | /3.G6 | -QMA19-XMA1 | 2 | /4.D6 | -QMA21-XMA4 | 12 | Ø4mm |
| 63 | WQG63 | /3.G7 | -KHB5-XMA3 | 2 | /4.D6 | -QMA22-XMA1 | 14 | Ø4mm |
| 64 | WQG64 | /3.F6 | -XMA12 | — | /4.D7 | -QMA22-XMA4 | 12 | Ø4mm |
| 65 | WQG65 | /4.D4 | -QMA20-XMA2 | 4 | /4.E4 | -RNB1-XMA1 | 1 | Ø6mm |
| 66 | WQG66 | /4.D5 | -QMA21-XMA2 | 4 | /4.E5 | -XMA20 | — | Ø6mm |
| 67 | WQG67 | /4.D6 | -QMA21-XMA3 | 2 | /4.E6 | -XMA21 | — | Ø6mm |
| 68 | WQG68 | /4.D7 | -QMA22-XMA2 | 4 | /4.F7 | -RNB6 | 1 | Ø6mm |
| 69 | WQG69 | /4.D7 | -QMA22-XMA3 | 2 | /4.F7 | -RNB7 | 1 | Ø6mm |
| 70 | WQG70 | /4.E5 | -XMA20 | — | /4.F5 | -RNB2 | 1 | Ø6mm |
| 71 | WQG71 | /4.E5 | -XMA20 | — | /4.F6 | -RNB4 | 1 | Ø6mm |
| 72 | WQG72 | /4.E6 | -XMA21 | — | /4.F5 | -RNB3 | 1 | Ø6mm |
| 73 | WQG73 | /4.E6 | -XMA21 | — | /4.F6 | -RNB5 | 1 | Ø6mm |
| 74 | WQG74 | /4.F4 | -RNB1-XMA2 | 2 | /4.F4 | -MMB1-XMA1 | — | Ø6mm |
Quy tắc đi ống để lấy đủ E1 (10.4 điểm): cắt vuông, cắm hết chiều sâu đầu nối, bó ống Ø4 tín hiệu thành bó dọc tấm 500, ống động đến xi lanh uốn bó cùng ống cố định, dây rút cách đều (≈100 mm) **không siết bẹp**, bán kính uốn tối thiểu ≈ 20 mm cho Ø4 và ≈ 30 mm cho Ø6, chừa chiều dài cho MM2/MM3 lắc trên bích xoay, không để ống chạm con trượt gót 302 và tấm mang chày 403.

## 5. Lịch sử sửa đổi (Revisions, tờ 1)

Bản vẽ qua 13 lần sửa từ 2025-06-06 đến 2026-09-08 (tất cả do ACK). Thiết kế ban đầu (rev 1, 2025-06-06); rev 2 (2025-06-20) đổi xi lanh uốn thành chuyển động 2 (b) và xi lanh đột thành chuyển động 3 (c), thêm công tắc báo phôi; rev 3–6 chỉnh BOM: đầu nối, khớp tự lựa FK-M10×1,25 → FK-M12×1,25 (2025-10-15), xi lanh uốn DSNU-25-40-PPS-A → ADN-32-30-A-P-A (2026-01-14); rev 7 dọn bản vẽ, thêm bảng revision; rev 8 (2026-02-17) thêm QSML-4 và màu ống, chỉnh bảng ống; rev 9 chỉnh ống và khung tên; rev 10 (2026-03-26) cập nhật mạch và BOM; **rev 11 (2026-06-10) đổi mã tham chiếu từ 2 chữ sang 3 chữ (EN 81346-2:2009 → EN IEC 81346-2:2019)** — vì vậy tài liệu cũ ghi A+, B+ nay là MM1+, MM2+; rev 12 (2026-07-17) cập nhật số cổng trên SV-3-M5; rev 13 (2026-09-08) cập nhật mã tham chiếu. Bản thi dùng **rev 13**.

## Ghi chú bản gốc

- `loi-ban-goc.md` #10: rev 11 đổi mã 2 chữ → 3 chữ; bản dịch dùng MM1…MM4.
- Mới (#19): tờ 4 ghi xi lanh là -MMB1…-MMB4 còn chuỗi/đề/thang điểm viết MM1…MM4 — cùng phần tử, chỉ khác độ dài mã.
- Parts List có hai dòng "Front panel valve" (570 SV-5-M5-B là van 5/2, 610 SV-3-M5 là van 3/2) và "Pneumatic valve" chung cho VUWG-L10-M52 (5/2 lò xo), -B52 (5/2 khí hai phía), -P53C (5/3 giữa đóng) — bản dịch ghi rõ loại trong cột mô tả.
- Khung tên tờ 5 ghi FILE NAME "2_Parts_List" trong khi là tờ 5 of 6, tờ 6 ghi "3_Tubing_List" — tên file nội bộ, bỏ qua.
- Pos. 60 (VMEF-RT-M32-M-G18, công tắc cửa) nằm trong Parts List khí nén nhưng cũng là item 7 của BOM bản vẽ 100 — cùng một linh kiện.
