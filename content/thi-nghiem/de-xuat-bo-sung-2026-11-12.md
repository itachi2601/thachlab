# Đề xuất thí nghiệm / mô phỏng cần bổ sung — 12/11/2026

Căn cứ: kho `content/thi-nghiem/` (306 thí nghiệm, 96 bài), 105 clip tự dựng, PhET đã nhúng trong 21 bài L12,
6 mô phỏng tự viết ở `components/physics/`, và phân tích hai đề Bộ 2025 (mã 0203), 2026 (mã 0211) đã có trong repo
(`docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md` mục 1, `.claude/skills/soan-quiz-ly-thuyet/references/phong-cach-de-bo-gd.md`).
Chưa đọc lại file đề gốc, chưa phân tích đề tham khảo/minh hoạ. Đề thi chỉ ra nội dung lớp 12 nên ưu tiên L12.

## Hiện trạng

- Mọi bài L10–L12 đều có 2–9 thí nghiệm trong kho; không bài nào trống.
- Đề Bộ: 5/8 câu Đúng–Sai của hai năm là câu thí nghiệm, hỏi theo khung giả thuyết → bố trí → bước → "coi rằng/bỏ qua"
  → hiện tượng → kết luận → cơ chế → chiều sai số → điều thí nghiệm KHÔNG chứng minh.
- Clip bẫy mới có cho Chương 3 L12 (`bay-ch3-01..05`); Chương 1, 2, 4 chưa có.
- Mô phỏng học sinh tự kéo: L12 chỉ có PhET ở 12/21 bài; 9 bài không có gì để tự thử (Lực từ, Thực hành đo B,
  Máy phát–biến áp, Ứng dụng cảm ứng, Điện từ trường, Năng lượng liên kết, Phân hạch, An toàn phóng xạ, Thực hành nhiệt;
  Thang nhiệt độ cũng không).

## A. Thí nghiệm đúng bối cảnh đề Bộ nhưng chưa có clip hoặc chưa có trong kho (làm trước)

| # | Thí nghiệm | Kho | Clip | Bẫy đề đánh vào |
|---|---|---|---|---|
| A1 | Phễu nước đá + dây điện trở, hai giai đoạn (đề 2025 II.1) | có `tn-l12-thuchanh-03` | chưa | quên trừ nước tan do môi trường (m₂ − m₁); nguồn nhiệt từng giai đoạn; λ lệch về phía nào; đánh giá phương án |
| A2 | Đo nhiệt dung riêng của nước, giả thuyết "c phụ thuộc m" (đề 2026 II.4) | có `tn-l12-thuchanh-01` | chưa | "toàn bộ nhiệt toả ra làm nóng nước"; chiều mất mát theo Δt; kết quả bác bỏ giả thuyết |
| A3 | Xilanh cách nhiệt (một ngăn nén khí; hai ngăn có vách) | CHƯA có | chưa | "cách nhiệt" bị hiểu là "nội năng không đổi"; dấu của A và Q trong ΔU = A + Q |
| A4 | Hạt mang điện trong từ trường đều: quỹ đạo tròn | CHƯA có (lý thuyết vừa bổ sung, commit edc27281d) | chưa | lực từ không sinh công, tốc độ không đổi; T không phụ thuộc v; hạt đứng yên hoặc bay dọc B không chịu lực |
| A5 | Thanh trượt trên hai ray trong từ trường, e = Bℓv | CHƯA có | chưa | chiều dòng cảm ứng; lực từ CẢN chuyển động; công suất kéo bằng công suất toả nhiệt |
| A6 | Hai dây song song mang dòng điện | CHƯA có | chưa | cùng chiều thì HÚT (ngược với trực giác "cùng dấu đẩy nhau") |
| A7 | Mô hình sóng điện từ: E, B, phương truyền | kho chỉ có phần "biến thiên sinh ra" | chưa | E và B dao động CÙNG pha, vuông góc nhau và vuông góc phương truyền; truyền được trong chân không |

A3–A7 cần thêm file `tn-l12-*.json` (kèm `gia_thuyet`, `du_doan_neu_dung`, `khong_chung_minh` theo T11) trước khi dựng clip.

## B. Clip bẫy theo chương (theo mẫu `bay-ch3-01`, tình huống lấy từ câu học sinh sai nhiều nhất 30 ngày)

- **Chương 1 Vật lí nhiệt (4 clip):** nước đang sôi vẫn 100 °C dù vẫn nhận nhiệt · "vật chứa nhiệt lượng" (nhiệt lượng là phần
  truyền, không phải thứ vật có) · Δt (°C) = ΔT (K) nhưng T ≠ t · dấu A, Q khi khí bị nén / tự dãn.
- **Chương 2 Khí lí tưởng (4 clip):** cùng một quá trình trên ba hệ trục p–V, p–T, V–T (đường kéo dài qua gốc chỉ khi dùng kelvin) ·
  động năng trung bình chỉ phụ thuộc T, không phụ thuộc loại khí · lốp xe xả bớt khí: lượng khí đổi thì không dùng p₁V₁/T₁ = p₂V₂/T₂ ·
  nén nhanh không còn đẳng nhiệt.
- **Chương 4 Hạt nhân (4 clip):** năng lượng liên kết ≠ năng lượng liên kết riêng (bền vững so bằng cái nào) · sau 2T còn 1/4,
  không phải hết · phóng xạ không đổi theo nhiệt độ, áp suất, bình chì · thí nghiệm Rutherford KHÔNG chứng minh quỹ đạo dừng;
  hạt alpha lệch do hạt nhân chứ không do êlectron.

## C. Mô phỏng tự kéo (học sinh đổi tham số, đoán trước rồi xem) — ít nhưng đúng chỗ bẫy

| # | Mô phỏng | Gắn bài | Vì sao |
|---|---|---|---|
| C1 | Ba đồ thị khí lí tưởng nối nhau: kéo điểm trạng thái trên p–V, hai hệ trục kia chạy theo | L12 bài 6, 7 | bẫy đọc đồ thị là dạng đề hỏi đều; PhET gas-properties không vẽ đồ thị |
| C2 | Hạt điện tích trong từ trường đều: đổi v, B, q, góc; hiện bán kính, chu kì, tốc độ | L12 bài 10 | cho A4; PhET không có bản HTML5 |
| C3 | Thanh trượt trên ray: đổi v, B, R; hiện e, I, lực cản, công suất | L12 bài cảm ứng điện từ | cho A5 |
| C4 | Phân rã: N(t) với hạt ngẫu nhiên + nút "trừ phông" | L12 bài 17, 18 | bẫy 2T, bẫy quên trừ phông (T7) |
| C5 | Cân dòng điện: đổi I, chiều I, góc; số cân tăng hay giảm | L12 bài 10, 11 | đề 2025 II.2; đã có clip `thuchanhtu3/4` nhưng chưa tự kéo được |

## Thứ tự và cách đo

1. A1, A2 (kho đã có, chỉ dựng clip) → A4, A5, A6 (thêm kho + clip) → A3, A7.
2. B: Chương 4 và Chương 1 trước (hai chương có câu thí nghiệm trong cả hai đề).
3. C1 rồi C2; C3–C5 sau khi có số liệu.
- Quy tắc áp dụng: T2 (không lộ kết quả trước hộp Dự đoán), T5, T7, T9, T12 (chạy mô hình sai trước), V7; clip theo cổng A–B + cổng mp4 375 px.
- Đo: tỉ lệ đúng của câu bẫy tương ứng trong Kiểm tra nhanh / Trả bài trước và sau 30 ngày (cách đã dùng cho `bay-ch3`).
- L10, L11: không đề xuất thêm thí nghiệm; việc còn lại là soát mắt clip đã dựng (`ra-soat-clip-2026-11-11.md` mục 3).
