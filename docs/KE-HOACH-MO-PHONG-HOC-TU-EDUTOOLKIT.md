# Kế hoạch: dụng cụ đo tương tác · thư viện mô phỏng công khai · thí nghiệm ảo theo bộ thiết bị SGK

Lập 21/11/2026 sau khi xem edutoolkit.net (bộ công cụ lớp học + 100 mô phỏng Vật lí của tác giả khác).
Thầy chốt làm ba gói A, B, C dưới đây; **không làm** đồng hồ + gọi tên trong trình chiếu và chấm phiếu bằng camera.
File này để giao phiên khác thực hiện. Mỗi gói làm trên một nhánh `claude/<tên>` riêng, xong gói nào chốt gói đó.

## 0. Điều học được và ranh giới

- Edutoolkit mạnh ở chỗ mô phỏng **dựng đúng bộ thiết bị thực hành SGK** (đệm khí, cổng quang, đồng hồ hiện số, lấy số liệu, vẽ đồ thị) và có nhóm **đo lường & sai số** (thước kẹp, panme, đồng hồ đa năng). Trang đó yếu ở chỗ mô phỏng đứng một mình: không dự đoán trước, không câu hỏi sau, không lưu tiến độ, chữ nhỏ trên nền tối.
- thachlab làm phần họ thiếu: mô phỏng **nằm trong bài**, có Dự đoán (`PredictGate`), có chấm, đúng khung T1–T12.
- **Bản quyền**: trang đó không ghi giấy phép → không nhúng, không chép mã, không chép hình. Chỉ học ý tưởng, tự dựng. Không đặt link tới trang đó trong bài học sinh.

## 1. Thứ đã có trong repo (đừng dựng lại)

| Thứ | Ở đâu |
|---|---|
| Mô phỏng tự dựng (khí lí tưởng, hạt trong điện trường, cân dòng điện, ném xiên, lò xo, giao thoa…) | `components/physics/*Simulation.tsx`, nạp lười qua `SimulationsLazy.tsx` |
| Cổng dự đoán trước khi chạy mô phỏng | `components/physics/PredictGate.tsx` |
| Chỗ gắn mô phỏng vào bài lý thuyết | `components/lessons/MoPhongPortals.tsx`; trang thử `app/dev/mo-phong-tu-keo/` |
| Màu sân khấu mô phỏng | `components/physics/stage-theme.ts` |
| Hình tương tác của bài tập mẫu | `components/lessons/cong-cu/*` |
| Một trang mô phỏng công khai mẫu | `app/(public)/mo-phong/giao-thoa-am/page.tsx` (chưa có trang chỉ mục `/mo-phong`) |
| Kho 323 thí nghiệm đọc máy được (`tham_so`, `mo_hinh`, `so_lieu_mau`, `sai_so_thuong_gap`, `goi_y_mo_phong`, `video`) | `content/thi-nghiem/tn-*.json`, `index.json` (sinh tự động, không sửa tay), `README.md` |
| Quy tắc | `docs/QUY-TAC-THIET-KE.md`, `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md`, `docs/MAU-NEN-SANG.md`, skill `phet` |

Việc đầu tiên của phiên nhận: đọc `MoPhongPortals.tsx` và một mô phỏng đang chạy (`CurrentBalanceSimulation.tsx`, lesson 12 lớp 12) để theo đúng cách gắn, cách nạp lười, cách dùng `PredictGate`.

## 2. Tư vấn theo nghiên cứu (áp cho cả ba gói)

- **Hợp**: L1 (truy xuất ngay, phản hồi tức thì có giải thích), N6 (ví dụ mẫu trước, tự làm sau), T7–T8 (sai số có chiều, bảng số liệu thật), H3 (nhãn ngay trên hình).
- **Dễ phạm**: N2 (bảng điều khiển mô phỏng hay vượt 4 nút), B4 (không chuyển động khi chưa bấm), C1/H4 (chữ trong hình ≥ 13px ở 360px, điều trang kia làm kém), M1/M7 (nền sáng, không sân khấu tối), D2/D6 (đích chạm 44pt, `inputmode="decimal"`), L3 (không hiện điểm/rank trong lúc làm).
- **Điều chỉnh**: mỗi mô phỏng một nhiệm vụ đo cụ thể thay vì "nghịch tự do"; kéo du xích bằng ngón tay phải có nút ± bước nhỏ đi kèm vì kéo chính xác 0,02 mm trên điện thoại là không thể.
- **Cách đo**: tỉ lệ học sinh hoàn thành nhiệm vụ đo / số em mở mô phỏng, và tỉ lệ đúng các câu sai số–dụng cụ đo trong ngân hàng trước và sau 4 tuần.

## 3. Gói A — Dụng cụ đo tương tác (làm trước)

**Mục tiêu**: học sinh tự đọc được thước kẹp, panme, đồng hồ đo điện đa năng, đồng hồ đo thời gian hiện số; được chấm ngay.

**Sản phẩm** (thư mục mới `components/physics/do-luong/`):

| Component | Nội dung | Gắn vào bài |
|---|---|---|
| `ThuocKep.tsx` | Du xích 0,1 / 0,05 / 0,02 mm; kéo hàm + nút ±; vạch trùng được tô khi xem đáp án | L10 bài 3 (lesson 48); lớp CNC/cơ khí của thầy |
| `Panme.tsx` | Độ chia 0,01 mm; xoay ống + nút ± | như trên |
| `DongHoDaNang.tsx` | Chọn thang V/A/Ω, cắm que đúng cổng; chọn sai thang thì báo lỗi kiểu thật (quá thang, cháy cầu chì) | L10 bài 2 (lesson 47); L11 thực hành đo suất điện động (lesson 45) |
| `DongHoHienSo.tsx` | Đồng hồ đo thời gian + cổng quang, MODE A, B, A↔B; **dùng lại ở gói C** | L10 bài 6 (lesson 51) |

**Hai chế độ cho mỗi dụng cụ**: *Xem cách đọc* (một ví dụ mẫu có chú thích từng bước, N6) rồi *Luyện đọc* (số ngẫu nhiên, học sinh nhập đáp số, chấm ngay kèm câu chỉ chỗ sai theo L4; xong khi đúng 5 lần liên tiếp).

**Ràng buộc**
- Không thêm round-trip Supabase: tiến độ luyện đọc lưu `localStorage`. Chưa ghi vào mastery ở đợt này.
- Nạp bằng `next/dynamic({ssr:false})` + `LazyErrorBoundary`, thêm vào `SimulationsLazy.tsx` (chỉ thêm dòng).
- SVG `currentColor`, nền sáng, không thư viện 3D, mỗi component ≤ ~25 KB mã.
- Sai số ghi kết quả theo đúng cách SGK lớp 10 đang dùng ở bài 3; đối chiếu `content/lesson-samples/` của lesson 48 trước khi viết phần chấm.

**Bước làm**
1. Đọc cách gắn mô phỏng (mục 1), dựng `ThuocKep` trước ở một trang `/dev/do-luong`.
2. Chụp 375 và 360 sáng + tối, tự chạy checklist mục 8 của `QUY-TAC-THIET-KE.md`; thầy duyệt một dụng cụ rồi mới làm ba cái còn lại.
3. Gắn vào bài: sửa `theory.src.html` của lesson 48, 47, 51, 45, đăng bằng `bash scripts/cap-nhat-ly-thuyet.sh <file> <lesson_id>` (Mac, ngoài giờ học sinh).
4. Agent `kiem-code` soát số học phần chấm (làm tròn, dấu phẩy thập phân, sai số dụng cụ).

**Xong khi**: bốn dụng cụ chạy ở 375px không cuộn ngang, đích chạm ≥ 44pt, chấm đúng 20/20 ca thử tay gồm ca biên (vạch 0 trùng, vạch cuối trùng), đã gắn vào 4 bài và deploy.

## 4. Gói B — Trang thư viện `/mo-phong` công khai

**Mục tiêu**: một trang không cần đăng nhập gom mọi thí nghiệm và mô phỏng thachlab đã có, tìm được theo lớp và chủ đề; phục vụ tuyển sinh và để học sinh tìm lại nhanh.

**Nguồn dữ liệu (không gọi Supabase khi tải trang)**: script mới `scripts/gen-thu-vien-mo-phong.mts` sinh `lib/data/thu-vien-mo-phong.json` từ
- `content/thi-nghiem/index.json` (chỉ mục có `co_video: true`, lấy thông tin clip ở trường `video` của từng file),
- danh sách mô phỏng tự dựng (khai tay một mảng nhỏ: tên, lớp, chủ đề, slug),
- các PhET đã nhúng (quét `content/lesson-samples/**/theory.src.html`; ghi nguồn CC BY 4.0 theo skill `phet`).

**Trang**
- `app/(public)/mo-phong/page.tsx`: tĩnh, lọc Lớp (9/10/11/12) + Chủ đề, ô tìm không dấu, thẻ có số đếm. Mỗi vùng ≤ 4 lựa chọn nhìn thấy (N2), chủ đề dài thì thu gọn.
- Mỗi thẻ: tên, một dòng "Nhìn vào:" (V2), nhãn loại (Mô phỏng / Clip / PhET). Clip theo V5: ảnh bìa + nút phát, không nạp player trước khi bấm.
- Mô phỏng tự dựng mở ở `/mo-phong/<slug>` theo mẫu `giao-thoa-am` (đợt đầu 4–6 cái mạnh nhất + bốn dụng cụ đo của gói A).
- Thẻ dẫn vào bài học cần đăng nhập: giữ `?next=` đủ cả query (quy tắc link sâu trong `AGENTS.md`).
- Cuối trang một lời mời đăng ký duy nhất (B2). Phụ huynh cũng đọc trang này nên soát thêm cỡ chữ theo `QUY-TAC-THIET-KE-PHU-HUYNH.md`.
- Thêm vào `app/sitemap.ts` và menu công khai (chỉ thêm dòng).

**Không làm**: không đăng lại clip chưa qua rà soát (xem `content/thi-nghiem/ra-soat-clip-2026-11-11.md`, 2 clip YouTube nghi sai đang chờ thầy thì loại khỏi thư viện).

**Xong khi**: trang tải không gọi DB, tìm "con lac" ra đúng thẻ có dấu, 375px + 1280px sáng/tối đã chụp, link mọi thẻ đã bấm thử (script kiểm link), đã deploy.

Gói B độc lập với A và C, chạy song song được. Chỉ chung một điểm: bốn dụng cụ đo vào thư viện sau khi gói A xong.

## 5. Gói C — Thí nghiệm ảo theo bộ thiết bị SGK (làm 2 bài mẫu rồi dừng chờ duyệt)

**Mục tiêu**: bài "Thực hành" có mô phỏng đúng bộ dụng cụ trong sách, học sinh tự lấy số liệu, lập bảng, tính kết quả và sai số như phiếu thực hành, theo kiểu đề TN THPT hỏi.

**Hai bài mẫu**
1. **L10 bài 11 — Đo gia tốc rơi tự do** (lesson 56): nam châm điện, cổng quang, thước, đồng hồ hiện số (`DongHoHienSo` của gói A).
2. **L10 bài 30 — Động lượng trước và sau va chạm** (lesson 75): đệm khí, hai xe, hai cổng quang.

**Thiết kế mỗi mô phỏng**
- Thông số, khoảng giá trị, phương trình, sai số đo lấy từ file `tn-*.json` tương ứng trong `content/thi-nghiem/` (kho này viết sẵn cho việc này); thiếu trường nào thì bổ sung vào JSON rồi chạy lại `thi_nghiem.py` sinh `index.json`.
- Mỗi lần đo có nhiễu theo `sai_so_do` để các lần đo khác nhau thật (T8), và ít nhất một nguồn sai số hệ thống bật/tắt được để thấy **chiều** lệch (T7).
- Trình tự: Dự đoán (`PredictGate`, T2) → lắp/chỉnh ≤ 4 điều khiển (N2) → đo 5 lần, số tự vào bảng → học sinh tự tính giá trị trung bình và sai số, nhập kết quả, được chấm → một câu hỏi kiểu đề (T9) → ô "Chưa nói được gì" (T5).
- Không chuyển động trước khi bấm (B4); bảng số liệu xếp dọc ở điện thoại (H2); bài đã có mô phỏng thì bỏ clip trùng nội dung (V6, V11).

**Bước làm**
1. Dựng bài 11 ở trang `/dev`, `kiem-code` tính lại số liệu và soát theo checklist mục 3 của `QUY-TAC-THI-NGHIEM-TRONG-BAI.md`.
2. Thầy duyệt trên điện thoại → gắn vào bài, đăng bằng `cap-nhat-ly-thuyet.sh`.
3. Làm bài 30, dùng lại khung bảng số liệu + phần chấm của bài 11 (tách thành `components/physics/thuc-hanh/BangSoLieu.tsx`).
4. **Dừng, báo thầy** kèm số liệu dùng thử. Chỉ mở rộng sang các bài thực hành còn lại (L10: 6, 22; L11: đo tần số âm, tốc độ truyền âm, suất điện động pin; L12: nhiệt dung riêng, cảm ứng từ; L9: tiêu cự thấu kính) khi thầy đồng ý.

**Xong khi**: hai bài mẫu đã đăng, mỗi bài chạy trọn trình tự ở 375px trong ≤ 8 phút, kết quả học sinh nhập được chấm đúng trong khoảng sai số cho phép.

## 6. Thứ tự và phân công

| Thứ tự | Gói | Phụ thuộc | Ghi DB | Mô hình |
|---|---|---|---|---|
| 1 | A — dụng cụ đo | không | không (chỉ cập nhật `ly_thuyet` 4 bài) | phiên chính; `kiem-code` soát |
| song song | B — thư viện `/mo-phong` | 4 dụng cụ của A vào sau | không | phiên chính |
| 2 | C — thí nghiệm ảo | `DongHoHienSo` của A | không (cập nhật `ly_thuyet` 2 bài) | phiên chính; `kiem-code` tính lại số |

- Không gói nào cần migration. Nếu sau này muốn ghi kết quả luyện đọc vào mastery thì đó là việc riêng, giao `kien-truc-du-lieu`.
- File chung sẽ đụng: `components/physics/SimulationsLazy.tsx`, `components/lessons/MoPhongPortals.tsx`, `app/sitemap.ts`, `docs/STATE.md` (chỉ thêm dòng). A và C cùng đụng hai file đầu nên làm nối tiếp, không song song.
- Mọi thay đổi UI: ghi mã quy tắc vào commit, chụp 375px trước khi báo xong, đăng bài ngoài giờ học sinh.
