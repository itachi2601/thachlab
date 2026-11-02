# 01 — Module A1: Bảo trì dự đoán (Predictive Maintenance)

Nguồn: `WSC2026_TP01_MA1_actual_en` (30.07.26, v1.0, 12 trang). Người ra đề (ITPD): Nathalie Drouin, STCD. Người thẩm định (ITPV): Alex Le Comte, STCD. Chấm theo Tiêu chí **A** (A1–A10), **17.5 điểm**, 47 mục chấm. Thời gian: 3.5 giờ (phần còn lại 0.5 giờ là Module A2).

> **Dùng để huấn luyện**
> - **Điểm tối đa: 17.5** — A1 1.6 · A2 1.2 · A3 1.3 · A4 2.75 · A5 2.95 · A6 2.8 · A7 1.7 · A8 0.8 · A9 1.5 · A10 0.9.
> - **Điểm dễ lấy (≈ 3.7 điểm chỉ cần gọi ký + ghi đủ):** 10 mục có "Expert Sign Off" (xác nhận tốc độ 0.4, số đo ban đầu 0.4, soft foot trước 0.25 và sau 0.25, báo cáo cân chỉnh 0.3, báo cáo giãn nở nhiệt 0.4, cân bằng cuối 0.3, báo cáo cuối 0.4, căn đai đã sửa 0.2, kiểm tra trước căn đai 0.2) và báo cáo A9 (1.5: tình trạng trước/sau, hình học, 7 mục cân chỉnh, cân bằng). Bài tính giãn nở nhiệt (0.5) là toán lớp 10.
> - **Bẫy mất điểm:** không gọi chuyên gia ký ở từng Task → mất cả mục; quên **cân chỉnh cho máy 3600 rpm** (dung sai chặt hơn 1800 rpm); quên **bù giãn nở nhiệt** vào cân chỉnh (0.4) rồi quên **đo lại khi OL2R đến** (0.5); siết bu-lông xong **không rút bu-lông đẩy (jack bolt) về** (0.15); vi phạm an toàn −0.5/lần.

## 1. Giới thiệu (Introduction)

**EN:** You have been sent to the Oriental Pearl TV Tower, in Shanghai, to inspect one of their main ventilation fans.

**VI:** Bạn được cử đến Tháp truyền hình Minh Châu Phương Đông (Oriental Pearl TV Tower), Thượng Hải, để kiểm tra một trong các quạt thông gió chính.

- **EN:** The fan and motor assembly is exhibiting abnormally high vibration levels, and the motor's axially secured bearing is operating at an elevated temperature. Preliminary information suggests an issue with the motor base and foundation. No corrections will be made at this point, only verification. Verify the condition and identify the corrective actions required. You will safely collect all the required data.
  **VI:** Cụm quạt–động cơ đang rung bất thường ở mức cao, và ổ lăn chặn dọc trục (axially secured bearing) của động cơ đang chạy ở nhiệt độ cao. Thông tin ban đầu cho thấy vấn đề nằm ở **đế động cơ và nền móng** (motor base and foundation). Ở bước này **chưa sửa gì, chỉ kiểm tra** (verification). Hãy kiểm tra tình trạng và xác định các biện pháp khắc phục cần thiết. Thu thập mọi dữ liệu cần thiết một cách an toàn.
- **EN:** Your OL2R bracket is delayed.
  **VI:** Giá đo OL2R (off-line to running, đo giãn nở nhiệt từ nguội sang chạy) của bạn **đến muộn**. [Ý: phải cân chỉnh trước bằng **giá trị tính toán** giãn nở nhiệt, khi OL2R đến mới đo thật và đối chiếu.]
- **EN:** The tools provided will enable you to perform all required alignment, balancing, and vibration checks on the motor and fan assembly. Upon receiving your OL2R, you must verify that the compensation applied for thermal growth was accurate.
  **VI:** Dụng cụ được cấp đủ để thực hiện mọi việc cân chỉnh đồng trục (alignment), cân bằng động (balancing) và kiểm tra rung (vibration checks) trên cụm động cơ–quạt. **Khi nhận được OL2R, bạn phải kiểm chứng rằng lượng bù giãn nở nhiệt (thermal growth compensation) đã áp dụng là chính xác.**
- **EN:** The weight of your fan blade is 10 kg.
  **VI:** Khối lượng cánh quạt là **10 kg** (dùng cho cân bằng động).
- **EN:** The alignment must be done for a 3600-rpm piece of equipment.
  **VI:** Cân chỉnh phải theo chuẩn cho thiết bị **3600 rpm**. [Dung sai cân chỉnh phụ thuộc tốc độ; chọn đúng tốc độ trong máy laser — mục "Confirming Speed" 0.4 điểm.]
- **EN:** You must produce a complete digital report on all inspections, corrections and final alignment results.
  **VI:** Phải lập **báo cáo số hoàn chỉnh** (digital report) về mọi kiểm tra, sửa chữa và kết quả cân chỉnh cuối cùng.
- **EN:** There is also belt driven equipment that will need to be inspected and repaired.
  **VI:** Còn có thiết bị **truyền động đai** (belt driven) cần kiểm tra và sửa (căn đai/puli — A10).

## 2. Hướng dẫn thí sinh (Instructions to the Competitor)

Đoạn luật chung (an toàn −0.5/lần, lần 3 dừng thi, bỏ sót ký xác nhận mất cả phần): xem `00-tong-quan-de-thi.md` mục 3.

**EN:** Diagnostic and corrective actions will be performed with the following equipment:
**VI:** Chẩn đoán và khắc phục được thực hiện bằng các thiết bị sau (tên hãng giữ nguyên):

| Thiết bị (EN) | Là gì / dùng cho việc gì (VI) |
|---|---|
| AT-400 Ultimate | Máy cân chỉnh đồng trục bằng laser (laser shaft alignment), đo lệch góc/lệch tâm, soft foot, có chức năng đo giãn nở nhiệt với OL2R |
| Wireless Balancer WBT-400 | Bộ cân bằng động không dây, một mặt phẳng (single-plane balancing) — tính khối lượng thử/hiệu chỉnh |
| Machine Defender | Máy phân tích rung động cầm tay (vibration analyser) — đo tình trạng trước/sau |
| Run-Out Probe | Đầu đo độ đảo (run-out) trục và khớp nối, hướng kính và dọc trục |
| Stroboscope | Đèn hoạt nghiệm — xem pha/đánh dấu góc khi cân bằng, đo tốc độ |
| OL2R | Giá đo giãn nở nhiệt off-line to running (lắp lên máy, đo thay đổi vị trí khi máy nóng) |
| PAT | Dụng cụ căn đai/puli bằng laser (pulley alignment tool) |

## 3. Phiếu nhiệm vụ (Task sheets) — 9 phiếu giống nhau

Mỗi phiếu Task # 1 … Task # 9 có cùng mẫu (trang 3–11 của đề). Thí sinh **tự điền mô tả việc đã làm**, số đo trước/sau, rồi gọi chuyên gia ký.

```
Task # __ : Description ____________________________
(Mô tả nhiệm vụ)

                                   Value Before      Value After
                                   (Giá trị trước)   (Giá trị sau)
                                                     If applicable (nếu có)

Expert sign off: ___________________________________
(Chuyên gia ký xác nhận)
```

Riêng **Task # 3** có thêm dòng `Calculation:` (Tính toán) — chỗ ghi **bài tính giãn nở nhiệt** (xem mục 4).

Gợi ý 9 nhiệm vụ ứng với thang điểm A1–A10 (đề không ghi sẵn, thí sinh tự đặt; đây là cách xếp hợp lý theo thứ tự thang điểm):

| Task | Việc gợi ý | Tiêu chí con | Ghi "Value Before / After" |
|---|---|---|---|
| 1 | Cài máy đo rung, xác nhận tốc độ, đo tình trạng rung ban đầu (4 điểm đo) | A1 Data Collection | Số đo rung ban đầu (mm/s) từng điểm |
| 2 | Kiểm tra độ phẳng đế (flatness check), ≥ 3 điểm chuẩn | A2 Flatness Check | Sai lệch độ phẳng |
| 3 | Kiểm tra cân bằng thuỷ (level check), 1 điểm chuẩn; **tính giãn nở nhiệt** | A3 Level Check + A6 Calculation | Bọt thuỷ; ΔL tính được |
| 4 | Kiểm tra trước cân chỉnh: độ đảo trục, độ đảo khớp nối, dọc trục khớp, độ rơ ổ, **soft foot** (đo → sửa → đo lại) | A4 Pre-Alignment | Số đo đảo; soft foot trước/sau |
| 5 | Cân chỉnh laser chính xác cho 3600 rpm, có bù giãn nở nhiệt; số căn đệm dưới chân; siết bu-lông, rút jack bolt; báo cáo | A5 Precision Alignment | Lệch góc/lệch tâm đứng–ngang trước/sau (xanh/vàng/đỏ) |
| 6 | Lắp OL2R, đo giãn nở nhiệt thật, đối chiếu với tính toán, đo lại cân chỉnh | A6 Thermal Growth | ΔL tính / ΔL đo |
| 7 | Cân bằng động cánh quạt 10 kg | A7 Balancing | Độ rung/độ mất cân bằng trước/sau |
| 8 | Đo tình trạng rung cuối (4 điểm đo) | A8 Data Collection | Số đo rung cuối |
| 9 | Kiểm tra trước và căn đai/puli bằng PAT; ảnh trước/sau | A10 Belt Alignment | Lệch puli trước/sau |
| — | Báo cáo số tổng hợp | A9 Reporting | — |

## 4. Tính giãn nở nhiệt (Thermal Growth Calculation) — trang 12

| EN | VI |
|---|---|
| Equipment Operating Temperature: 40 degrees Celsius | Nhiệt độ làm việc của thiết bị: **40 °C** |
| Room Temperature: 24 degrees Celsius | Nhiệt độ phòng: **24 °C** |
| Coefficient (α) (×10⁻⁶ /°C): Carbon Steel 11-13 | Hệ số giãn nở dài α (×10⁻⁶ /°C): thép cacbon **11–13** |
| ΔL = α × L0 × ΔT | ΔL = α · L₀ · ΔT |

Cách làm (để luyện):
- ΔT = 40 − 24 = **16 °C**.
- L₀ = chiều cao từ mặt đế (chân máy) đến **tâm trục** của động cơ, **đo tại chỗ thi** bằng mm (đề không cho; thí sinh phải đo).
- Chọn α trong khoảng 11–13 ×10⁻⁶ /°C (thường lấy 12, hoặc ghi rõ giá trị đã chọn và lý do).
- Ví dụ: L₀ = 250 mm, α = 12 ×10⁻⁶ → ΔL = 12 ×10⁻⁶ × 250 × 16 = **0.048 mm** (động cơ nóng sẽ **cao lên** 0.048 mm, nên khi cân chỉnh lạnh phải đặt động cơ **thấp hơn** quạt một lượng tương ứng ở phương đứng).
- Ghi phép tính vào dòng `Calculation:` của Task # 3 và nhập giá trị bù vào máy AT-400 ("Compensated in alignment", 0.4 điểm). Khi OL2R đến, đo giãn nở thật và **ghi so sánh** ("Confirmed and remeasured", 0.5 điểm).

## 5. Thang điểm Tiêu chí A (tóm tắt để luyện; đầy đủ ở `08-thang-diem-song-ngu.csv`)

| Sub | Mục chấm (VI) | Cách tính | Điểm |
|---|---|---|---|
| A1 | Cài đặt máy trong dụng cụ đo (Machine set-up in measuring tool) | có/không | 0.4 |
| A1 | Xác nhận tốc độ (Confirming speed) | Expert Sign Off | 0.4 |
| A1 | Quy trình đo đúng, 4 điểm đo | nhập số điểm đúng /4 | 0.4 |
| A1 | Số đo tình trạng ban đầu (Initial condition reading) | Expert Sign Off | 0.4 |
| A2 | Cài đặt máy; quy trình đo (3 bước); điểm chuẩn (tối đa 3) | nhập số đúng | 0.4 + 0.4 + 0.4 |
| A3 | Cài đặt máy 0.4; quy trình đo (4 bước) 0.25; **bọt thuỷ cân** 0.25; điểm chuẩn (chỉ cần 1) 0.4 | | 1.3 |
| A4 | Độ đảo trục cố định & di động; độ đảo khớp nối; dọc trục khớp nối; khe hở ổ (độ rơ dọc trục) | đủ 2 trục = full, 1 trục = nửa, 0 = 0 | 4 × 0.5 |
| A4 | Soft foot trước cân chỉnh (ký); sửa soft foot; kiểm lại soft foot (ký) | | 3 × 0.25 |
| A5 | Quy trình lắp thiết bị cân chỉnh đúng | | 0.2 |
| A5 | Lệch góc đứng / góc ngang / tâm đứng / tâm ngang | **Đỏ = 0, Vàng = nửa, Xanh = full** (màn hình AT-400) | 4 × 0.5 |
| A5 | Số căn đệm (shim) dưới chân | | 0.3 |
| A5 | Bu-lông đã siết và **bu-lông đẩy đã rút về** | | 0.15 |
| A5 | Báo cáo kết quả cuối | Expert Sign Off | 0.3 |
| A6 | Tính toán 0.5; đã bù vào cân chỉnh 0.4; lắp OL2R đúng 0.5; quy trình đo 0.5; đo lại và xác nhận 0.5; báo cáo số đo cuối (ký) 0.4 | | 2.8 |
| A7 | Lắp phần cứng cân bằng đúng 0.4; cài máy 0.5; quy trình cân bằng 0.5; kết quả cuối trong dung sai (ký) 0.3 | kết quả: **≤ 6.3 → full; 6.4–16 → nửa (0.15); > 16.1 → 0** | 1.7 |
| A8 | Quy trình đo đúng, 4 điểm 0.4; báo cáo số đo cuối (ký) 0.4 | | 0.8 |
| A9 | Báo cáo: tình trạng trước (rung) 0.2; tình trạng cuối (rung) 0.2; hình học đầy đủ 0.2; **cân chỉnh đầy đủ, 7 mục** 0.7; cân bằng 0.2 | | 1.5 |
| A10 | Quy trình đo đúng 0.2; đã sửa (ký) 0.2; kiểm tra trước: dọc trục, độ đảo, trục, độ rơ (ký) 0.2; báo cáo có ảnh trước/sau, tối đa 3 0.3 | | 0.9 |

[Ghi chú dịch: mục A7 "6.3 < =0.3 full marks, 6.4-16=0.15 half marks, 16.1>=0 marks" — đơn vị không ghi trong thang điểm; hiểu là kết quả rung/mất cân bằng còn lại hiển thị trên WBT-400 (thường mm/s hoặc g·mm), ngưỡng ≤ 6.3 đạt trọn 0.3 điểm.]

## Ghi chú bản gốc

- Đề thật A1 có tiêu đề file trong trang là `WSC2026_TP01_MA_actual_en` (không có số 1) — cùng tài liệu.
- "PROCEDING" (đúng: PROCEEDING) — lỗi chính tả, bỏ qua.
- Thang điểm A nhiều lỗi chính tả ("measurent", "Alignement", "Sin Off", "Tigntened", "rmaximum", "loseness") — `loi-ban-goc.md` #8, dịch theo nghĩa.
- A1 và A8 cùng tên "Data Collection": A1 là số đo **ban đầu**, A8 là số đo **cuối** — bản dịch ghi thêm cho rõ.
- Mục A7 "Final Balancing Readings": ngưỡng 6.3 / 6.4–16 / 16.1 không ghi đơn vị — xem ghi chú dịch mục 5.
