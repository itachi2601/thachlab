# 02 — Module A2: Sửa lỗi khí nén trên FluidSIM (Pneumatic Troubleshooting)

Nguồn: `WSC2026_TP01_MA2_actual_en` (30.07.26, v1.0, 2 trang). Người ra đề: Jim Ackert, FESTO (ITPD). Người thẩm định: Craig Brazil (ITPV). Chấm theo Tiêu chí **G** (G1), **2.5 điểm**, 7 mục. Thời gian: 0.5 giờ (nằm trong 4 giờ của Module A).

> **Dùng để huấn luyện**
> - **Điểm tối đa: 2.5** — 3 lỗi xác định (3 × 0.3) + 3 lỗi sửa (3 × 0.3) + tổng thời gian (0.7, xếp hạng theo tốc độ).
> - **Điểm dễ lấy:** 1.8 điểm cho việc tìm và sửa đủ 3 lỗi, không cần nhanh. Mạch là **đúng mạch của Module D** (chuỗi MM1+, MM2+ & MM3+, MM4+ …), nên ai đã thuộc sơ đồ file 07 thì nhìn ra lỗi rất nhanh.
> - **Bẫy mất điểm:** không gọi chuyên gia **ký và ghi giờ** sau khi *xác định* xong, rồi lại sau khi *sửa* xong (2 lần ký) → mất điểm G1; sửa lỗi mà không mô phỏng chạy lại đủ chuỗi → chuyên gia không công nhận "restored to full operational condition".

## 1. Giới thiệu (Introduction)

**EN:** Competitors will complete a timed pneumatic troubleshooting speed challenge by diagnozing and correcting faults within a FluidSim schematic. Competitors who successfully restore the pneumatic system to full operational condition will be ranked from the fastest aggregate troubleshooting time to the slowest. Bonus marks will be awarded based on this final ranking.

**VI:** Thí sinh thực hiện một **thử thách tốc độ sửa lỗi khí nén có tính giờ**: chẩn đoán và sửa các lỗi trong một **sơ đồ FluidSIM** (phần mềm mô phỏng Festo, không phải mạch vật lý). Những thí sinh **khôi phục được hệ khí nén về trạng thái vận hành hoàn toàn** sẽ được xếp hạng theo **tổng thời gian sửa lỗi** (aggregate troubleshooting time) từ nhanh nhất đến chậm nhất. **Điểm thưởng** (bonus marks) được trao theo thứ hạng cuối cùng này. [Ứng với mục "Total aggregate time" 0.7 điểm trong thang điểm G1.]

## 2. Hướng dẫn thí sinh (Instructions to the Competitor)

**EN:** READ THE ENTIRE DOCUMENT BEFORE PROCEDING. REMEMBER: Experts MUST sign off at designated module points in the documentation. If a sign off point is missed all marks for that section of the project will be deducted from the overall project total.

**VI:** ĐỌC HẾT TÀI LIỆU TRƯỚC KHI BẮT ĐẦU. NHỚ: Chuyên gia PHẢI ký xác nhận tại các điểm quy định. Bỏ sót một điểm ký thì toàn bộ điểm phần đó bị trừ khỏi tổng.

[Ghi chú dịch: đề A2 **không** có đoạn trừ 0.5 điểm an toàn vì làm trên máy tính; luật an toàn chung vẫn áp dụng cho cả ngày thi.]

## 3. Chuỗi hoạt động và nhiệm vụ (Circuit Sequence)

**Circuit Sequence: (MM1+, MM2+ & MM3+, MM4+) (MM1−, MM2− & MM3−, MM4−)**

Đọc: xi lanh **MM1 đi ra** (kẹp phôi) → **MM2 và MM3 cùng đi ra** (hai xi lanh uốn) → **MM4 đi ra** (đột) → **MM1 đi về** → **MM2 và MM3 cùng đi về** → **MM4 đi về**. Giải thích chi tiết từng phần tử ở `07-so-do-khi-nen.md`.

| EN | VI |
|---|---|
| Identify and rectify the three faults on the supplied FluidSim schematic. | Xác định và sửa **ba lỗi** trên sơ đồ FluidSIM được cấp. |
| Fault's 1, 2, and 3 identified: YES / NO — Time: _________ | Đã xác định lỗi 1, 2, 3: CÓ / KHÔNG — Thời gian: ______ |
| Experts sign off: _____________ | Chuyên gia ký xác nhận: ______ |
| Fault's 1, 2, and 3 rectified: YES / NO — Time: _________ | Đã sửa lỗi 1, 2, 3: CÓ / KHÔNG — Thời gian: ______ |
| Experts sign off: _____________ | Chuyên gia ký xác nhận: ______ |

Quy trình nên tập:
1. Mở sơ đồ, **chạy mô phỏng** ngay để xem chuỗi dừng ở bước nào.
2. So với sơ đồ chuẩn (file 07): kiểm tra nguồn khí – van hai tay – van phân phối 5/2 – cổng 14/12 – cảm biến đầu/cuối hành trình (QMA8…QMA19) – phần tử AND/OR (KHB1…KHB5) – tiết lưu.
3. Lỗi điển hình trên FluidSIM: ống nối nhầm cổng (2↔4, 12↔14), van đổi loại (thường đóng ↔ thường mở), thiếu dây tín hiệu, cảm biến gắn sai xi lanh, tiết lưu ngược chiều, nguồn khí không nối.
4. Ghi lại **3 lỗi đã xác định**, gọi chuyên gia **ký + ghi giờ**. Rồi sửa, chạy lại đủ một chu trình, gọi chuyên gia **ký + ghi giờ** lần 2.

## 4. Thang điểm Tiêu chí G

| Mục chấm (EN) | VI | Điểm |
|---|---|---|
| Fault 1 / 2 / 3 Identified | Đã xác định lỗi 1 / 2 / 3 | 3 × 0.3 |
| Fault 1 / 2 / 3 Rectified | Đã sửa lỗi 1 / 2 / 3 | 3 × 0.3 |
| Total aggregate time | Tổng thời gian (xếp hạng tốc độ) | 0.7 |
| **Tổng** | | **2.5** |

## Ghi chú bản gốc

- "diagnozing" (đúng: diagnosing), "PROCEDING" — lỗi chính tả, bỏ qua.
- "Fault's 1, 2, and 3" — dấu nháy sai (`loi-ban-goc.md` #9), bỏ qua.
- Đề viết "FluidSim", phần mềm chính thức viết "FluidSIM" — giữ tên hãng.
- Tiêu đề trang 1 là "Module A2", trang 2 ghi file `WSC2026_TP01_MA2_actual_en` — nhất quán.
