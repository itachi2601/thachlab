# 00 — Tổng quan đề thi (Test Project overview) — WorldSkills Shanghai 2026, Skill 01 Industrial Mechanics

Nguồn: `WSC2026_TP01_skill_sets_pre_en` (bản pre-release, 24.06.2026, v1.1), phần Criteria của thang điểm (Marking Scheme), và trang "Instructions to the Competitor" của các đề thật Module A1, A2, B, C, D (30.07.26, v1.0).

> **Dùng để huấn luyện**
> - **Điểm tối đa toàn bài: 100.** Gia công (C) 26.0 + Lắp ráp cơ khí (D) 22.1 = **48.1 điểm**, gần nửa bài. Tập tiện–phay và lắp ráp trước, kỹ hơn mọi phần khác.
> - **Điểm dễ lấy:** mọi điểm "ký xác nhận" (Expert sign off) trong Module A — chỉ cần gọi chuyên gia đúng lúc; áp suất 8.0 bar (0.5 điểm, F1); nộp chi tiết đúng giờ; tự ghi báo cáo đủ 5 mục ở A9 (1.5 điểm).
> - **Bẫy mất điểm (áp dụng mọi module):**
>   1. Vi phạm an toàn: **−0.5 điểm mỗi lần**, lần thứ 3 **bị dừng thi**, chấm trên phần đã làm.
>   2. Bỏ sót một điểm ký xác nhận (sign off point) → **mất toàn bộ điểm của mục đó**.
>   3. Không nộp chi tiết **ngay khi hết giờ** (Module B, C, D) → **0 điểm** mục đó.
>   4. Module D: chạy thử chức năng được **1 lượt miễn phí**, mỗi lượt thêm **−2 điểm**, tối đa **3 lượt**; sửa lỗi khi vận hành cũng vậy.
>   5. Module D: **không được bắt đầu lắp khí nén** trước khi chuyên gia chấm xong phần cơ khí.

## 1. Thời gian và 4 module (Modules Overview)

Tổng thời gian thi (Total Competition Time): **20 giờ**.

| Module (đề thật) | Module (pre-release) | Giờ | Nội dung EN | Nội dung VI |
|---|---|---|---|---|
| **A1** + **A2** | Module 1 | 4 h | Predictive Maintenance (3.5 h) and Pneumatics Troubleshooting (0.5 h) | Bảo trì dự đoán (3.5 h) và sửa lỗi khí nén (0.5 h, trên FluidSIM) |
| **B1** + **B2** | Module 2 | 4 h | Fabrication, Welding (3 h) and Precision Layout (1 h) | Chế tạo, hàn (3 h) và lấy dấu chính xác (1 h) |
| **C1** + **C2** | Module 3 | 5 h | Machining (Turning 2.5 h – Milling 2.5 h) | Gia công: tiện (2.5 h) và phay (2.5 h) |
| **D** | Module 4 | 7 h | Mechanical and Pneumatic Systems Assembly | Lắp ráp hệ cơ khí và khí nén, vận hành |

Ghi chú chung của đề (General notes):
- Sản phẩm Module 2 và 3 được **dùng tiếp trong Module 4** (Modules 2 and 3 are incorporated into Module 4 build and assembly). Làm hỏng chi tiết ở B/C thì D cũng khó chạy.
- Bản vẽ chi tiết và bản vẽ lắp cấp theo **cả hai phép chiếu góc thứ nhất và góc thứ ba** (first-angle and third-angle projections) — nội dung giống nhau, chọn bản quen dùng.
- Toàn bộ ghi kích thước **hệ mét** (metric).
- Máy tiện và máy phay đứng có **bộ hiển thị toạ độ số** (Digital Readout, DRO).
- Phải thể hiện **quy trình làm việc an toàn và thực hành tốt** (safe working procedures and best practices) **mọi lúc**.

## 2. Trọng số điểm thật (Marking Scheme — Criteria)

| Tiêu chí (Criterion) | Tên EN | Tên VI | Điểm | Số mục chấm | Thuộc module |
|---|---|---|---|---|---|
| A | Predictive Maintenance | Bảo trì dự đoán | **17.5** | 47 | A1 |
| B | Fabrication, Welding and Precision Layout | Chế tạo, hàn và lấy dấu chính xác | **14.0** | 54 | B1 (B2 lấy dấu chấm ở D1) |
| C | Machining – Turning – Milling | Gia công tiện – phay | **26.0** | 44 | C1 (405), C2 (404), C3 (401) |
| D | Mechanical Assembly | Lắp ráp cơ khí | **22.1** | 28 | D1 (Detail 301), D2 (lắp ráp) |
| E | Pneumatic Assembly | Lắp ráp khí nén (đi ống) | **10.4** | 12 | D |
| F | Final Project Functionality | Vận hành cuối cùng | **7.5** | 6 | D |
| G | Pneumatic Troubleshooting | Sửa lỗi khí nén (FluidSIM) | **2.5** | 7 | A2 |
| H, I | — | (không dùng) | 0 | 0 | — |
| **Tổng** | | | **100.0** | 198 | |

Chi tiết từng tiêu chí con (Sub Criterion):

| Sub | Tên EN | Tên VI | Điểm |
|---|---|---|---|
| A1 | Data Collection | Thu thập dữ liệu (ban đầu) | 1.6 |
| A2 | Flatness Check | Kiểm tra độ phẳng | 1.2 |
| A3 | Level Check | Kiểm tra cân bằng (thuỷ) | 1.3 |
| A4 | Shaft Alignment (Pre-Alignment) | Cân chỉnh trục — kiểm tra trước cân chỉnh | 2.75 |
| A5 | Precision Alignment | Cân chỉnh chính xác (laser) | 2.95 |
| A6 | Thermal Growth Measurement | Đo giãn nở nhiệt | 2.8 |
| A7 | Balancing | Cân bằng động | 1.7 |
| A8 | Data Collection | Thu thập dữ liệu (cuối) | 0.8 |
| A9 | Reporting | Báo cáo | 1.5 |
| A10 | Belt Alignment | Căn đai | 0.9 |
| B1 | Fabrication and Welding | Chế tạo và hàn (khung 200) | 14.0 |
| C1 | Detail 405 | Chi tiết 405 (tiện: trục ren M24) | 9.1 |
| C2 | Detail 404 | Chi tiết 404 (tiện: đầu giữ chày, nhôm) | 3.5 |
| C3 | Detail 401 | Chi tiết 401 (phay: khối cối) | 13.4 |
| D1 | Detail 301 | Chi tiết 301 (tấm lưng: lấy dấu, khoan, ta-rô, siết) | 7.65 |
| D2 | Mechanical Assembly | Lắp ráp cơ khí | 14.45 |
| E1 | Pneumatic Assembly | Lắp ráp khí nén | 10.4 |
| F1 | Final Project Functionality | Vận hành cuối cùng | 7.5 |
| G1 | Pneumatic Troubleshooting | Sửa lỗi khí nén | 2.5 |

Hai kiểu mục chấm (Aspect):
- **M — Measurement (chấm đo):** đạt/không đạt theo số đo hoặc có/không; đa số mục. Nhiều mục kiểu "nhập số lượng đúng" (Enter the number…), điểm chia đều theo số lượng.
- **J — Judgement (chấm đánh giá):** chỉ có ở B1 (chất lượng mối hàn), 15 mục × 0.2 điểm, thang 0–3: 0 = phải làm lại, 1 = chuẩn công nghiệp (trung bình), 2 = tốt, 3 = xuất sắc.

## 3. Luật trừ điểm và điểm ký xác nhận (chung cho mọi đề thật)

Nguyên văn (có ở đầu đề A1, B, C, D; đề A2 chỉ có đoạn "REMEMBER"):

> READ THE ENTIRE DOCUMENT BEFORE PROCEDING. ALL PROPER SAFETY PROCEDURES MUST BE DEMONSTRATED AS YOU WOULD ON THE JOB SITE. YOU ARE BEING OBSERVED AT ALL TIMES. IF YOU HAVE TO BE ADVISED OF SAFETY INFRACTIONS DURING THIS MODULE, 0.5 MARKS WILL BE DEDUCTED FOR EACH INFRACTION. Experts will not intervene unless there is a safety concern. On the 3rd infraction, the Competitor will be stopped, evaluation will be based on the work already completed. REMEMBER: Experts MUST sign off at designated module points in the documentation. If a sign off point is missed all marks for that section of the project will be deducted from the overall project total.

Dịch:
> ĐỌC HẾT TÀI LIỆU TRƯỚC KHI BẮT ĐẦU. PHẢI THỂ HIỆN MỌI QUY TRÌNH AN TOÀN ĐÚNG NHƯ KHI LÀM VIỆC THẬT TẠI HIỆN TRƯỜNG. BẠN BỊ QUAN SÁT MỌI LÚC. NẾU BỊ NHẮC VI PHẠM AN TOÀN TRONG MODULE NÀY, **TRỪ 0.5 ĐIỂM MỖI LẦN VI PHẠM.** Chuyên gia sẽ không can thiệp trừ khi có vấn đề an toàn. **Đến lần vi phạm thứ 3, thí sinh bị dừng thi**, chấm điểm trên phần việc đã hoàn thành. NHỚ: Chuyên gia **PHẢI ký xác nhận** tại các điểm quy định trong tài liệu. **Bỏ sót một điểm ký xác nhận thì toàn bộ điểm của phần đó bị trừ khỏi tổng điểm.**

Ý nghĩa khi luyện tập:
- "Vi phạm an toàn" gồm: không đeo kính/giày/găng đúng lúc, tay gần dao đang quay, không khoá khí trước khi sửa ống, đứng sai vị trí khi máy chạy, để phoi/dầu trên sàn, dùng khí nén thổi người… Hãy tập phản xạ an toàn như một thói quen, vì chuyên gia **không nhắc trước**, chỉ ghi trừ điểm.
- Ở mỗi phiếu nhiệm vụ đều có dòng `Expert sign off: ____` hoặc `Expert Initials: ____`. **Thí sinh phải chủ động gọi chuyên gia đến ký**. Không ký = mất điểm cả phần.

## 4. Điểm ký xác nhận và thứ tự nộp bài (theo đề thật)

| Module | Việc | Nộp / ký khi nào | Hậu quả nếu bỏ |
|---|---|---|---|
| A1 | Mỗi Task 1–9 | `Expert sign off` sau mỗi task (có cả "Calculation" ở Task 3) | Mất điểm mục đó |
| A1 | Các mục thang điểm có "Expert Sign Off": xác nhận tốc độ, số đo tình trạng ban đầu, soft foot trước/sau, báo cáo kết quả cân chỉnh, báo cáo số đo cuối, cân bằng cuối, báo cáo cuối, căn đai đã sửa | Gọi ký ngay khi làm xong bước đó | 0 điểm mục đó |
| A2 | Xác định 3 lỗi → ký + ghi giờ; sửa 3 lỗi → ký + ghi giờ | Hai lần ký | Mất điểm G1, mất xếp hạng thưởng |
| B1 | Cụm hàn 201–207 | **Ngay khi hết 3 giờ** trình chuyên gia; `Expert Initials` | **0 điểm** |
| B2 | Detail 301 (lấy dấu) | **Ngay khi hoàn thành** (trong 1 giờ); `Expert Initials` | **0 điểm** |
| C1 | Detail 404 + 405 (tiện) | **Ngay khi xong hoặc hết 2.5 giờ**; `Expert Initials` | **0 điểm** |
| C2 | Detail 401 (phay) | **Ngay khi xong hoặc hết 2.5 giờ**; `Expert Initials` | **0 điểm** |
| D-1 | Detail 301 khoan/ta-rô hoàn thiện | Nộp ngay khi xong; `Expert Initials` | 0 điểm mục |
| D-2 | Lắp ráp cơ khí xong | Báo chuyên gia; **chưa được lắp khí nén** cho đến khi chấm xong; `Expert Initials` | 0 điểm mục |
| D-3 | Lắp khí nén xong, đặt 8.0 bar, chạy thử chuỗi | Báo chuyên gia; 1 lượt thử miễn phí, −2/lượt thêm, tối đa 3; `Expert Initials` | 0 điểm mục |
| D-4 | Nghiệm thu: ra 1 sản phẩm, rồi thêm 2 | Báo chuyên gia ngay khi xong; sửa lỗi 1 lượt miễn phí, −2/lượt thêm, tối đa 3; `Expert Initials` | 0 điểm mục |

Thứ tự thi dự kiến (theo logic "B, C làm ra chi tiết cho D"): A1/A2 → B → C → D, hoặc B → C → A → D tuỳ ban tổ chức xếp lịch. Trong Module D, thí sinh **được làm theo thứ tự tuỳ chọn** (You may perform the work in any order you prefer), nhưng ba mốc ký D-2 → D-3 → D-4 phải theo đúng trình tự.

## 5. Nội dung pre-release từng module (skill sets) — dịch kèm ghi chú thay thế

### Module 1 — Predictive Maintenance (Bảo trì dự đoán)
Thực hiện các hoạt động bảo trì dự đoán bằng dụng cụ chẩn đoán và thiết bị giám sát được cấp:
- Kiểm tra thiết bị tìm dấu hiệu mòn và/hoặc hư hỏng (Inspect equipment for signs of wear and/or malfunction)
- Dùng dụng cụ chẩn đoán đo bất thường trong thông số vận hành
- Ghi và diễn giải dữ liệu (Record and interpret data)
- Áp dụng biện pháp khắc phục khi cần

[Ghi chú dịch: đề thật A1 nêu rõ kịch bản quạt thông gió tháp Oriental Pearl, thiết bị AT-400 Ultimate, WBT-400, Machine Defender, Run-Out Probe, Stroboscope, OL2R, PAT; quạt 10 kg, 3600 rpm — xem file 01. Phần 0.5 giờ "Pneumatics Troubleshooting" thành Module A2 trên **phần mềm FluidSIM**, không phải mạch vật lý — xem file 02.]

### Module 2 — Fabrication, Welding and Precision Layout (Chế tạo, hàn và lấy dấu chính xác)
- Vật liệu: thép hộp vuông hoặc chữ nhật thép cacbon thấp (mild steel square or rectangular tubing), thành dày 2 mm – 4 mm. [Ghi chú dịch: đề thật dùng hộp vuông 50 × 50 × 2 (SHS), xem file 06.]
- Dây hàn: Merit Pro6 Premium MIG Wire, 1.0 mm
- Khí bảo vệ: 80% Argon / 20% CO₂
- Tiêu chuẩn hàn: ISO 2553:2019, Hệ A (System A)

Lấy dấu chính xác và dụng cụ cầm tay (Precision Layout and Hand Tools): thước ê-ke tổ hợp (combination squares), thước cuộn (measuring tape), thước lá 300 mm (steel rule), tay quay ta-rô (tap handle), mũi vạch (scribing tools), đột tâm (centre punches), thiết bị khoan, giũa (files), búa đầu tròn (ball-peen hammers), máy khoan điện cầm tay (portable electric drills).

Yêu cầu dung sai (pre-release): ±1.0 mm với chiều dài ≤ 150 mm; ±1.5 mm với 150–300 mm; ±2 mm với > 300 mm.
[Ghi chú dịch: thang điểm thật B1 dùng ±2 mm cho kích thước bao 500/400/675, ±1 mm cho vị trí 130 mm, ±2° cho góc vuông, ±2 mm hiệu đường chéo; D1 dùng ±0.5 mm cho vị trí lỗ trên Detail 301. Lấy số của thang điểm thật làm chuẩn luyện tập.]

Nhiệm vụ (Tasks): lấy dấu và vạch dấu chính xác các chi tiết; khoan, giũa và chuẩn bị chi tiết đúng kích thước; chế tạo và hàn ra chi tiết chính xác cho Module 4.

### Module 3 — Machining (Gia công)
**Phần 1: Tiện (Turning – Centre Lathe – 4 Jaw Independent Chuck, máy tiện vạn năng, mâm cặp 4 chấu độc lập).** Các nguyên công: tiện mặt đầu, tiện trụ, tiện côn, tiện vai (facing, parallel turning, taper turning, shoulder turning); tiện rãnh thoát dao, vát mép, tiện lỗ (undercutting, chamfering, boring); tiện ren ngoài (external thread cutting); khoan và ta-rô; làm ra chi tiết chính xác cho Module 4. Vật liệu: thép cacbon thấp cán nguội 1020 (Cold Rolled Mild Steel 1020); nhôm 6160 T6 [Ghi chú dịch: đúng là 6061-T6, link kèm theo trong bản gốc cũng dẫn tới 6061]. Yêu cầu dung sai (pre-release): kích thước ±0.025 mm.

**Phần 2: Phay (Milling – Vertical Milling Machine, máy phay đứng).** Các nguyên công: rãnh then, rãnh, hốc (keyways, slots, pockets); khoan, ta-rô, doa (drilling, tapping, reaming); khoét bậc, khoét côn (counterboring, countersinking); làm ra chi tiết chính xác cho Module 4. Vật liệu: thép 1020; nhôm 6160 T6 [Ghi chú dịch: 6061-T6]; đồng thau C36000 (Brass C36000); Acetyl (Delrin) [Ghi chú dịch: đúng là Acetal/POM]. Yêu cầu dung sai (pre-release): kích thước ±0.025 mm, vị trí ±0.01 mm.

[Ghi chú dịch — **đã bị thang điểm thật thay thế**: thực tế chấm theo lắp ghép ISO ghi trên bản vẽ: Ø85 f8 (84.910–84.964), Ø58 (57.97–58.00), Ø20 H8 (20.000–20.033), Ø12 H8 (12.000–12.027), ren M24×3 6g (đường kính trung bình 21.803–22.003), rãnh 25.1–25.2 và 25.15–25.35; các kích thước còn lại ±0.15 hoặc ±0.3 (dung sai chung ISO 2768-1 fK); **chỉ** khoảng tâm lỗ 75 là ±0.01 và tâm lỗ 20 là ±0.02. Xem file 04 và CSV 08. Dung sai ±0.025 "cho mọi kích thước" của pre-release không còn hiệu lực.]

### Module 4 — Mechanical and Pneumatic Systems Assembly (Lắp ráp hệ cơ khí và khí nén)
Các việc sau có thể làm theo thứ tự bất kỳ:
- Lắp một hệ cơ khí và hệ truyền động khí nén (fluid power system)
- Dùng linh kiện khí nén được cấp, gồm phần tử đầu vào, phần tử xử lý, phần tử điều khiển cuối và cơ cấu chấp hành (input elements, processing elements, final control elements, actuators) cho mạch tầng hoặc mạch tuần tự nhiều xi lanh (multi-cylinder cascade or sequential circuit)
- Thiết kế mạch được lập bằng phần mềm thiết kế chuẩn công nghiệp và ghi nhãn theo chuẩn an toàn và vận hành [Ghi chú dịch: đề thật cấp sẵn sơ đồ khí nén Festo rev 13, thí sinh **lắp theo sơ đồ**, không tự thiết kế — xem file 07]
- Lấy dấu chính xác và lắp các chi tiết gia công sẵn, chi tiết chế tạo và chi tiết do thí sinh làm ra (pre-machined, fabricated, and competitor-produced parts)
- Sản phẩm phải đúng bản vẽ và bản thiết kế được cấp (blueprints and drawings)
- Tiêu chuẩn: ISO 1219-1:2012, ISO 1219-2:2012(E/F), EN81346-2:2019, ISO 4414, NFPA 79.

[Ghi chú dịch: đề thật D chia 4 bước có ký xác nhận (lấy dấu 301 → lắp cơ khí → lắp khí nén + chạy thử → nghiệm thu ra 3 sản phẩm), áp suất làm việc 8.0 bar (800 kPa), điều khiển hai tay — xem file 05.]

## 6. Những điểm pre-release đã bị đề thật thay thế (tóm tắt)

| # | Pre-release nói | Đề thật / thang điểm thật | Xem |
|---|---|---|---|
| 1 | Module 1–4 | Đổi tên thành Module A1, A2, B1/B2, C1/C2, D; tiêu chí chấm A–G | file này, mục 2 |
| 2 | Dung sai gia công ±0.025 mm, vị trí ±0.01 mm | Lắp ghép ISO (f8, H8, 6g) + ±0.15/±0.3; chỉ tâm lỗ 75 ±0.01, tâm 20 ±0.02 | `loi-ban-goc.md` #3, file 04 |
| 3 | Dung sai lấy dấu ±1.0/±1.5/±2 theo chiều dài | B1: ±2 mm kích thước bao, ±1 mm vị trí 130, ±2°; D1: ±0.5 mm vị trí lỗ | file 03, 05 |
| 4 | Thép hộp 2–4 mm | 50 × 50 × 2 SHS, chiều dài cắt sẵn 201–207 | file 06 |
| 5 | "Pneumatics Troubleshooting" 0.5 h | Module A2 sửa 3 lỗi trên **FluidSIM**, tính giờ, xếp hạng thưởng | file 02 |
| 6 | "Circuit design will be created using design software" | Sơ đồ cấp sẵn (Festo, rev 13), thí sinh lắp ống theo sơ đồ | file 07 |
| 7 | Nhôm "6160 T6", "Acetyl" | 6061-T6, Acetal | `loi-ban-goc.md` #1, #2 |
| 8 | Chưa có trọng số điểm | A 17.5 / B 14.0 / C 26.0 / D 22.1 / E 10.4 / F 7.5 / G 2.5 | mục 2 |

## Ghi chú bản gốc

- `loi-ban-goc.md` #1, #2: "Aluminum 6160 T6", "Acetyl (Delrin)" — đã chú thích tại chỗ.
- `loi-ban-goc.md` #3: dung sai pre-release ±0.025/±0.01 đã bị thang điểm thật thay thế — đã chú thích.
- Pre-release viết giờ bằng dấu phẩy thập phân ("3,5 hours", "0,5 hour"); bản dịch viết 3.5 h, 0.5 h theo quy ước dấu chấm.
- Đề thật Module C viết ".5 MARKS" (thiếu số 0) thay cho "0.5 MARKS" — cùng nghĩa.
- Đề thật dùng "PROCEDING" (đúng: PROCEEDING) ở mọi module — lỗi chính tả, bỏ qua.
