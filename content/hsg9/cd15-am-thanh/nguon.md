# CĐ15. Âm thanh (bài 150, khoá Vật lí HSG & chuyên KHTN 9) — dàn ý chung

Không có docx nguồn (chuyên đề mới, thêm theo đề cương "THI HSG 9 KHTN 26-27", slide 4:
"Âm thanh: Sóng âm. Độ to và độ cao. Phản xạ âm"). Phần âm thanh thuộc KHTN 7 (Chương trình GDPT 2018);
chuyên đề này ôn lại chuẩn lớp 7 rồi nâng lên mức HSG 9 / tuyển sinh 10 chuyên. Đề HSG 9 thật 2024–2025 ra âm
ít và nhẹ (đo độ sâu bằng siêu âm, đọc đồ thị dao động âm thoa → biên độ, tần số).

## Quy ước số liệu (mọi file dùng chung)
- Tốc độ âm: không khí $340\ \text{m/s}$ (khi đề không cho), nước $1500\ \text{m/s}$, thép $\approx 6000\ \text{m/s}$ (bài nào dùng thì đề cho số).
- Ánh sáng truyền "tức thời" so với âm ($3\cdot10^8$ m/s) — nêu rõ điều kiện này khi dùng.
- Tai người nghe được $20\ \text{Hz}$ – $20\,000\ \text{Hz}$; hạ âm dưới 20 Hz, siêu âm trên 20 000 Hz.
- Tiếng vang: nghe được khi âm phản xạ tới tai chậm hơn âm trực tiếp **ít nhất $\tfrac{1}{15}$ s** (chuẩn SGK lớp 7)
  ⇒ khoảng cách tới vật phản xạ $d \ge \dfrac{340}{2\cdot15}\approx 11{,}3\ \text{m}$.
- Mức cường độ âm (dB): chỉ nêu định tính (ngưỡng đau ≈ 130 dB, giới hạn tiếng ồn), KHÔNG có bài tính log.

## Lý thuyết (theory.src.html) — 6–7 mục, ~15 phút
I. Mở bài: thấy chớp rồi mới nghe sấm (câu dự đoán: chớp cách bao xa nếu sau 3 s mới nghe sấm).
II. Nguồn âm và sóng âm: vật dao động phát âm; âm truyền qua rắn, lỏng, khí, không truyền trong chân không;
   $v_{rắn} > v_{lỏng} > v_{khí}$; $s = v\,t$. Mở rộng HSG: sóng âm trong khí là sóng dọc; $\lambda = v/f = vT$; khi âm đi
   sang môi trường khác, tần số giữ nguyên, tốc độ và bước sóng đổi.
III. Độ cao và độ to: tần số $f = N/t$ (N dao động trong t giây), chu kì $T = 1/f$; tần số lớn → âm cao (bổng);
   biên độ lớn → âm to; đọc đồ thị dao động (trục thời gian → T, f; trục li độ → biên độ); hạ âm, siêu âm (dơi, cá heo,
   siêu âm y khoa). Bẫy: "âm to" ≠ "âm cao"; chu kì đọc trên đồ thị phải đếm trọn dao động.
IV. Phản xạ âm, tiếng vang: vật cứng nhẵn phản xạ tốt, vật mềm xốp hấp thụ tốt; điều kiện nghe tiếng vang;
   đo độ sâu/khoảng cách bằng tiếng vang (sonar): $d = v\,t/2$. Bẫy: quên chia 2.
V. Mở rộng HSG: (1) âm truyền trong hai môi trường cùng chiều dài (ống thép – không khí) nghe hai tiếng cách nhau
   $\Delta t$ ⇒ $L = \dfrac{\Delta t}{1/v_1 - 1/v_2}$; (2) nguồn âm chuyển động về phía vách rồi nghe tiếng vang
   (tổng quãng đường xe + âm $= 2d$); (3) chống ô nhiễm tiếng ồn (giảm tại nguồn, ngăn đường truyền, hấp thụ).
VI. Trả bài và mang về (6 câu tự trả lời).

## Bài tập mẫu (scripts/data/bai-tap-mau/150.json) — 6 dạng, cấp không giảm
D1 (cấp 1) Tốc độ – quãng đường truyền âm: chớp và sấm, nghe tiếng nổ xa, so sánh thời gian truyền trong hai môi trường.
D2 (cấp 1–2) Tần số, độ cao, độ to: đếm dao động → f, T; đọc đồ thị dao động hai âm thoa; xếp hạ âm/nghe được/siêu âm.
D3 (cấp 2) Tiếng vang và đo khoảng cách: siêu âm đo độ sâu biển, khoảng cách tối thiểu để nghe tiếng vang.
D4 (cấp 3) Hai tiếng qua hai môi trường: gõ đầu ống thép / đường ray, đầu kia nghe hai tiếng cách $\Delta t$ → tìm L hoặc v.
D5 (cấp 3–4) Nguồn chuyển động + tiếng vang: ô tô chạy thẳng về vách núi bóp còi, sau t nghe tiếng vang → khoảng cách lúc bóp còi / lúc nghe.
D6 (cấp 4) Bước sóng và đổi môi trường (Mở rộng HSG): $\lambda = v/f$; âm từ không khí vào nước giữ f, tìm $\lambda$ mới; kết hợp với tiếng vang.

## Tự luận (tu_luan) — 8 bài dễ → khó, mỗi bài có Hướng dẫn giải trong <details>.

## YCCĐ cho "Làm bài tương tự"
KHTN 9 chưa có YCCĐ âm. Dùng topic của L11 sóng (bài 27, 28): "Bước sóng, chu kì, tần số, tốc độ truyền sóng",
"Phân biệt sóng ngang và sóng dọc". Dạng nào không khớp topic nào thì để topic gần nhất và ghi chú.
