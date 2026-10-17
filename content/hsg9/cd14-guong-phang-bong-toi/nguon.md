# CĐ14. Gương phẳng, bóng tối và nửa tối (bài 158, khoá Vật lí HSG & chuyên KHTN 9) — dàn ý chung

Nguồn: docx 14 (đã trích ở `nguon.txt` cùng thư mục) — CHỈ dùng phần quang (B1 mục 1–5, B2 mục 1–5, C dạng 1–5, G1–G3, nhóm lỗi 1–4)
làm khung; ví dụ D/E/G trong docx KHÔNG chép, số liệu dưới đây là số mới tự đặt, đã tính bằng `tinh.py` (chạy
`python3 content/hsg9/cd14-guong-phang-bong-toi/tinh.py`, mọi kết quả kiểm bằng phản xạ véc-tơ). Viết lại bằng lời mình.
Phạm vi: kiến thức KHTN 7 (Ánh sáng) dạy lại cho lớp 9; phần (mở rộng ngoài YCCĐ) của docx là trọng tâm HSG — ghi nhãn "mở rộng" ở lý thuyết.

**Ranh giới với CĐ17 (bài 178, Thiên văn):** múi giờ, pha Mặt Trăng, nhật thực/nguyệt thực VỀ MẶT THIÊN VĂN, Hệ Mặt Trời thuộc CĐ17.
CĐ14 làm hình học bóng (nguồn điểm, nguồn rộng, bóng trên tường/sàn, bóng người dưới đèn đường di chuyển, bóng nắng); chỉ một câu
liên hệ "vùng tối của Mặt Trăng chạm Trái Đất → nhật thực; chóp tối không chạm → nhật thực hình khuyên (xem CĐ17)", KHÔNG làm dạng.
**Ranh giới với CĐ06/07:** khúc xạ, thấu kính không đụng tới. Tuần dùng: buổi 13 (gửi 26/12): thứ Hai đọc lý thuyết + quiz (40 phút),
thứ Ba bài tập mẫu (60 phút) (`tuan.json`).

## Quy ước số liệu & ký hiệu (mọi file dùng chung)
- Ánh sáng truyền thẳng trong không khí. Góc tới $i$, góc phản xạ $i'$ đo với **pháp tuyến**; góc giữa tia và **mặt gương** ký hiệu $\beta$ ($i = 90^\circ - \beta$).
- Gương: $G$, $G_1$, $G_2$; điểm sáng $S$, ảnh $S'$; điểm tới $I$ (lần 2: $J$ hoặc $I_2$); pháp tuyến $IN$; tia phản xạ $IR$.
- Góc giữa hai gương $\alpha$ (giao tuyến/đỉnh $O$); góc quay của gương $\delta$ (tia phản xạ quay $2\delta$); góc lệch tổng $D$.
- Bóng: nguồn điểm $S$ hoặc nguồn rộng đường kính $D_n$ (đĩa) / chiều dài (đèn tuýp); vật chắn đường kính $d$; $a$ = khoảng cách nguồn → vật,
  $L$ = khoảng cách nguồn → màn (mọi khoảng cách đo **từ nguồn**); đường kính vùng tối $d_{t}$, mép ngoài vùng nửa tối $d_{n}$.
  (Không dùng chữ $D$ cho cả nguồn lẫn góc lệch trong cùng một bài.)
- Đèn đường cao $H$, người cao $h$, người cách chân đèn $x$, bóng dài $\ell$; tốc độ người $v$.
- Gương toàn thân: chiều cao người $h$, độ cao mắt $h_m$; mép dưới $Q$, mép trên $P$.
- Hình: tia sáng nét liền, mũi tên giữa tia; đường kéo dài và ảnh ảo nét đứt; mặt sau gương gạch chéo; vùng tối tô đậm, vùng nửa tối tô nhạt.
- Làm tròn: góc tới 0,1°; độ dài 2–3 chữ số có nghĩa.

## Lý thuyết (theory.src.html) — 7 mục, ~15 phút
I. Mở bài: phòng thử đồ chỉ treo gương cao chừng nửa người mà ai cũng thấy đủ từ đầu tới chân; tối đi dưới đèn đường bóng mình "chạy" trước mặt.
   **Câu dự đoán:** (1) lùi xa gương có thấy được nhiều thân mình hơn không? (2) đi xa cột đèn với tốc độ không đổi thì đỉnh bóng chạy nhanh hơn, chậm hơn hay bằng mình?
II. Truyền thẳng, vùng tối – vùng nửa tối: nguồn điểm chỉ cho vùng tối; nguồn rộng cho vùng tối + vùng nửa tối (nửa tối = nhận sáng từ **một phần** nguồn).
   Cách vẽ tia "cùng mép" (giới hạn vùng tối) và "chéo mép" (mép ngoài nửa tối); tỉ số đồng dạng đỉnh tại nguồn $d' = d\,L/a$; diện tích tăng $(L/a)^2$.
   Vật nhỏ hơn nguồn: vùng tối thu hẹp, mất khi $L = a\,D_n/(D_n-d)$ (+1 câu liên hệ nhật thực → CĐ17). Bóng nắng: tia song song, $H/\ell_H = h/\ell_h$.
   Bóng người dưới đèn: $\ell = h\,x/(H-h)$ (mở rộng).
III. Định luật phản xạ: hai ý; hệ quả: góc giữa tia tới và tia phản xạ $= 2i$; tia bị lệch $180^\circ - 2i$; muốn đặt gương: pháp tuyến là phân giác của góc $SIR$.
   Phản xạ gương và phản xạ khuếch tán (định luật vẫn đúng ở từng điểm). Mở rộng: tia tới cố định, gương quay $\delta$ ⇒ tia phản xạ quay $2\delta$ cùng chiều.
IV. Ảnh qua gương phẳng: ảo, bằng vật, đối xứng qua gương; mọi tia phản xạ có đường kéo dài qua $S'$ (dùng để vẽ nhanh tia phản xạ).
   Mở rộng: vật/gương dịch chuyển — vật lại gần $x$ thì khoảng vật–ảnh giảm $2x$; gương tịnh tiến $x$ (vuông góc mặt gương) thì ảnh dời $2x$;
   vật chuyển động xiên góc $\beta$ với mặt gương: ảnh có cùng tốc độ, thành phần dọc gương giữ nguyên, thành phần vuông góc đổi chiều.
V. Vùng nhìn thấy (mở rộng): dựng ảnh $O'$ của mắt, nối $O'$ với hai mép gương → vùng nhìn thấy; $S$ thấy được khi đoạn $S'O$ (hoặc $O'S$) cắt gương trong mép.
   Gương toàn thân: chiều cao tối thiểu $h/2$, mép dưới $h_m/2$, mép trên $(h_m+h)/2$, không phụ thuộc khoảng cách (chứng minh đường trung bình).
   Tia đi qua điểm cho trước: nối $S'$ với $R$ cắt gương tại $I$; đó cũng là **đường ngắn nhất** $S \to$ gương $\to R$ (bất đẳng thức tam giác).
VI. Hai gương (mở rộng): song song → vô số ảnh; hợp góc $\alpha$: nếu $360^\circ/\alpha = m$ nguyên chẵn → $m-1$ ảnh; $m$ lẻ → $m-1$ ảnh khi vật trên phân giác,
   $m$ ảnh khi lệch; ảnh nằm trên đường tròn tâm $O$ bán kính $OS$. Tia phản xạ lần lượt trên hai gương: góc giữa tia và mặt gương tăng thêm $\alpha$ mỗi lần
   ($i_1 + i_2 = \alpha$ khi $i_1 \lt \alpha$); góc lệch tổng sau 2 lần $D = 360^\circ - 2\alpha$ (với $\alpha \le 90^\circ$: tia ló hợp tia tới $2\alpha$);
   $\alpha = 90^\circ$ → tia ló song song ngược chiều (phản quang xe đạp).
VII. Trả bài và mang về (6 câu tự trả lời): định nghĩa nửa tối; vì sao đo từ nguồn; vì sao tia quay $2\delta$; vì sao gương $h/2$ không phụ thuộc khoảng cách;
   đếm ảnh $\alpha = 72^\circ$; cách vẽ tia qua điểm cho trước.

Bẫy (từ nhóm lỗi 1–4 của docx, viết lại): lấy góc với mặt gương làm góc tới; tia vuông góc gương ghi $i = 90^\circ$; ảnh vẽ nét liền/phía trước gương;
khoảng vật–ảnh là $d$ thay vì $2d$, dịch $x$ thì đổi $x$ thay vì $2x$; mép dưới gương $= h/2$ thay vì $h_m/2$; "lùi xa thấy nhiều hơn";
quên điều kiện "$360^\circ/\alpha$ nguyên", đếm cả vật; gương quay $\delta$ thì tia quay $\delta$; dùng $i_1 + i_2 = \alpha$ khi $i_1 \gt \alpha$;
trong bài bóng lấy khoảng vật–màn thay vì nguồn–màn; diện tích bóng nhân $L/a$ thay vì $(L/a)^2$; nguồn rộng chỉ vẽ tia từ tâm;
"đỉnh bóng chạy bằng tốc độ người".

## Bài tập mẫu (scripts/data/bai-tap-mau/158.json) — 7 dạng, cấp không giảm. SỐ LIỆU ĐÃ TÍNH, dùng nguyên.
D1 (cấp 1) **Định luật phản xạ, đặt gương, gương quay.** (a) Tia nắng chếch xuống hợp phương ngang 50°, muốn hắt thẳng đứng xuống đáy giếng:
   góc $SIR = 140^\circ$, $i = 70^\circ$, gương hợp phương ngang $70^\circ$. (b) Cùng tia nắng, hắt thẳng đứng lên trần: $SIR = 40^\circ$, $i = 20^\circ$, gương hợp ngang $20^\circ$.
   (c) Bút laser, tia phản xạ đập vuông góc vào tường cách điểm tới 4,0 m; quay gương 3° quanh trục qua điểm tới: tia quay 6°, vệt sáng dịch $4\tan6^\circ \approx 0{,}42$ m = 42 cm
   (bẫy: quên 2δ → 21 cm). (d) Muốn vệt dịch 70 cm: tia quay ≈ 9,93°, gương quay ≈ 4,96° (≈ 5°). topic: "Định luật phản xạ ánh sáng".
D2 (cấp 2) **Bóng người dưới đèn đường (nguồn điểm).** Đèn cao $H = 4{,}5$ m, người $h = 1{,}5$ m đi ra xa chân đèn $v = 1{,}2$ m/s.
   (a) Cách chân đèn 2 m → bóng 1,00 m; cách 5 m → bóng 2,50 m ($\ell = x/2$). (b) Đỉnh bóng chạy $v H/(H-h) = 1{,}80$ m/s; bóng dài thêm 0,60 m mỗi giây.
   (c) Tường thẳng đứng cách chân đèn 9 m: bóng bắt đầu leo lên tường khi người cách đèn 6,00 m; khi người cách đèn 7,5 m, bóng trên tường cao 0,90 m (trên sàn 1,50 m).
   (d) Đèn thứ hai giống hệt cách đèn thứ nhất 12 m, người đứng giữa cách đèn 1 là 4 m: hai bóng ngược chiều dài 2,00 m và 4,00 m. topic: "Bóng tối, bóng nửa tối".
D3 (cấp 2) **Nguồn rộng: vùng tối, vùng nửa tối.** Đèn đĩa $D_n = 20$ cm, đĩa chắn $d = 30$ cm đồng trục cách đèn $a = 60$ cm, màn cách đèn $L = 180$ cm.
   (a) Nếu là nguồn điểm: bóng 90 cm. (b) Nguồn rộng: vùng tối $d_t = 50$ cm, mép ngoài nửa tối $d_n = 130$ cm, vành nửa tối rộng 40 cm.
   (c) Thay đĩa chắn $d = 12$ cm (nhỏ hơn đèn): vùng tối mất khi $L = 150$ cm; tại $L = 120$ cm vùng tối 4,0 cm, nửa tối 44 cm; tại $L = 180$ cm không còn vùng tối
   (tính ra −4 cm: đĩa giữa 4 cm vẫn thấy vành sáng của đèn), mép ngoài nửa tối 76 cm. (d) Đĩa 30 cm: muốn vùng tối 60 cm phải đặt màn cách đèn 240 cm (khi đó nửa tối 180 cm).
   Chỉ 1 câu liên hệ nhật thực hình khuyên → CĐ17. topic: "Bóng tối, bóng nửa tối".
D4 (cấp 2) **Ảnh khi vật/gương dịch chuyển.** (a) Người cách gương 3,0 m → cách ảnh 6,0 m; đi tới gương 1,2 m/s: ảnh lại gần người 2,4 m/s; sau 1,5 s người–ảnh 2,4 m.
   (b) Người đứng yên, gương lùi ra xa 0,4 m/s (vuông góc mặt gương): ảnh đi xa 0,8 m/s so với đất; sau 2 s người–ảnh 7,6 m.
   (c) Người đi 1,2 m/s theo phương hợp mặt gương 60°: ảnh cũng 1,2 m/s (so với đất), hai vận tốc hợp nhau 120°; người–ảnh lại gần nhau $2v\sin60^\circ \approx 2{,}08$ m/s.
   (d) Người đứng yên cách gương 3,0 m, gương quay 15° quanh trục thẳng đứng qua chân đường vuông góc $H$: ảnh quay 30° quanh $H$ trên đường tròn bán kính 3 m, dời ≈ 1,55 m.
   topic: "Ảnh của vật tạo bởi gương phẳng".
D5 (cấp 3) **Vùng nhìn thấy, gương thấy toàn thân.** (a) Người cao 1,70 m, mắt cách đỉnh đầu 12 cm ($h_m = 1{,}58$ m): gương tối thiểu 0,85 m, mép dưới 0,79 m,
   mép trên 1,64 m; chứng minh không phụ thuộc khoảng cách (bẫy: mép dưới 0,85 m lệch 6 cm). (b) Gương có sẵn cao 0,60 m treo mép dưới 0,95 m (mép trên 1,55 m):
   thấy từ độ cao 0,32 m đến 1,52 m (không thấy chân, không thấy đỉnh đầu). (c) Gương rộng 40 cm treo tường, mắt trên trục cách gương 30 cm, tường đối diện cách gương 2,0 m
   (sau lưng): thấy dải tường rộng ≈ 3,07 m; lùi mắt ra 60 cm → còn ≈ 1,73 m (lại gần thấy nhiều hơn). (d) Mắt lệch: cách gương 0,5 m, lệch khỏi tâm gương 0,5 m sang phải:
   dải thấy được trên tường từ $x = -3{,}0$ m đến $x = -1{,}0$ m (điểm $x = -1{,}5$ m thấy, $x = -3{,}4$ m không thấy). topic: "Ảnh của vật tạo bởi gương phẳng".
D6 (cấp 3) **Tia qua điểm cho trước, đường ngắn nhất.** (a) $A$ cách gương 30 cm, $B$ cùng phía cách gương 50 cm, hai chân đường vuông góc cách nhau 60 cm:
   nối $A'B$ → $I$ cách chân của $A$ 22,5 cm, $i \approx 36{,}9^\circ$, đường $A \to I \to B$ = 100 cm (so sánh: $I$ ở trung điểm → 100,74 cm; lệch 10 cm → 101,29 cm).
   (b) Cùng hình học, phiên bản đời sống: lều cách sông 30 m, nhà cách sông 50 m, chân cách 60 m, đi 1,25 m/s ra sông lấy nước rồi về nhà: ngắn nhất 100 m, 80 s.
   (c) Hai gương vuông góc ($G_1 = Ox$, $G_2 = Oy$), $A(40;20)$, $B(10;50)$ cm, tia từ $A$ phản xạ trên $G_1$ rồi $G_2$ tới $B$: dựng ảnh kép $A_{12}(-40;-20)$,
   $I$ tại $x \approx 25{,}7$ cm trên $G_1$, $J$ tại $y = 36{,}0$ cm trên $G_2$, đường dài ≈ 86,0 cm; tia ló $JB$ song song ngược chiều tia tới $AI$. topic: "Ảnh của vật tạo bởi gương phẳng".
D7 (cấp 4) **Hai gương hợp góc: số ảnh, phản xạ nhiều lần, góc lệch.** (a) Số ảnh: $\alpha = 72^\circ$ → 4 ảnh (vật trên phân giác) / 5 ảnh (lệch);
   $\alpha = 60^\circ$ → 5; $\alpha = 45^\circ$ → 7; $\alpha = 100^\circ$ (không nguyên) → 4 ảnh (dựng lần lượt). (b) $\alpha = 72^\circ$, $i_1 = 25^\circ$: $i_2 = 47^\circ$,
   góc lệch tổng $D = 216^\circ$, tia ló hợp tia tới $144^\circ = 2\alpha$. (c) Tia tới $G_1$ với $i_1 = 70^\circ$; tìm $\alpha$ để ở lần phản xạ thứ 3 tia tới vuông góc gương
   rồi quay ngược đường cũ: góc với mặt gương $20^\circ \to 20^\circ+\alpha \to 20^\circ + 2\alpha = 90^\circ$ ⇒ $\alpha = 35^\circ$; góc tới lần lượt 70°, 35°, 0°, 35°, 70°; tổng 5 lần phản xạ
   (điều kiện tia vào được từ miệng góc: $90^\circ - i_1 = 20^\circ \lt \alpha$). (d) Hai gương song song cách 20 cm, $S$ cách $G_1$ 6 cm: hai ảnh gần nhất cách nhau 40 cm
   (= 2 lần khoảng cách gương); chuỗi ảnh (gốc tại $G_1$): −6; 46; −46; 86 … và 34; −34; 74; −74 … cm. topic: "Ảnh của vật tạo bởi gương phẳng".

## Tự luận (tu_luan) — 8 bài dễ → khó, mỗi bài có Hướng dẫn giải trong <details>. Số liệu khác bài tập mẫu và khác docx (đã tính ở `tinh.py`).
1. Hắt nắng vào hang: tia nắng chếch xuống 36°, muốn tia phản xạ nằm ngang đi tiếp cùng chiều → $i = 72^\circ$, gương hợp ngang 18°; hắt ngang ngược lại → $i = 18^\circ$, gương 72°.
2. Đo chiều cao cột bằng bóng nắng khi bóng chạm tường: cọc 1,0 m bóng 1,25 m; cột cách tường 6 m, bóng lên tường 1,6 m → cột cao 6,40 m.
3. Tìm độ cao đèn: người 1,6 m đi 4 m từ chân đèn, bóng 2,0 m → đèn 4,80 m; đi 1 m/s thì đỉnh bóng 1,50 m/s.
4. Không biết vị trí: người 1,5 m thấy bóng 1,0 m, lùi xa thêm 2,0 m bóng 1,8 m → đèn cao 5,25 m, lúc đầu cách chân đèn 2,50 m.
5. Đếm và dựng ảnh: $\alpha = 30^\circ$ → 11 ảnh; $\alpha = 40^\circ$ → 8 ảnh (phân giác) / 9 ảnh (lệch); vẽ đường tròn chứa ảnh.
6. Kính tiềm vọng hai gương song song nghiêng 45°, ống cao 0,8 m, vật cách gương trên 20 m (theo phương ngang) → ảnh cuối cách gương dưới 20,8 m, cùng chiều vật.
7. Gương quay đều 2 vòng/phút: tia phản xạ quay 4 vòng/phút; vệt sáng trên tường cách 5 m, lúc ở chân đường vuông góc chạy ≈ 2,09 m/s.
8. Đèn tuýp dài 1,2 m treo ngang cao 2,4 m, thước 0,3 m song song ngay dưới tâm đèn: thước cao 0,8 m → không có vùng tối (nửa tối 1,05 m);
   thước cao 0,2 m → vùng tối ≈ 0,22 m, nửa tối ≈ 0,44 m; còn vùng tối khi thước cao ≤ 0,60 m (bài toán một chiều: dùng chiều dài thay đường kính).

## Luyện tập (8 câu, tự chấm, nhãn như đề thật): 4 Phần I (A–D), 2 Phần II (a)–d) Đúng/Sai), 2 Phần III (đáp số).
P1. Tia tới hợp mặt gương 25° → góc giữa tia tới và tia phản xạ **130°**; nhiễu 50° (2β), 65° (chỉ là $i$), 25° (β). topic: "Định luật phản xạ ánh sáng".
P2. Hai gương hợp 45°, vật đặt bất kì giữa hai gương → **7 ảnh**; nhiễu 8 (đếm cả vật), 6, vô số. topic: "Ảnh của vật tạo bởi gương phẳng".
P3. Tia tới cố định, quay gương 12° → tia phản xạ quay **24°**; nhiễu 12° (quên 2δ), 6°, 48°. topic: "Định luật phản xạ ánh sáng".
P4. Khái niệm: vùng nửa tối là vùng **chỉ nhận ánh sáng từ một phần của nguồn**; nhiễu "ánh sáng yếu do xa nguồn", "không nhận ánh sáng", "chỉ có với nguồn điểm".
   topic: "Bóng tối, bóng nửa tối".
PII-1. Người cao 1,60 m, mắt cao 1,50 m, đứng cách gương treo tường 2 m: a) ảnh cách người 4 m (Đ); b) gương tối thiểu 0,80 m (Đ);
   c) mép dưới gương phải cách sàn 0,80 m (S — đúng là 0,75 m); d) lùi xa gương thì cần gương cao hơn mới thấy toàn thân (S).
PII-2. Đèn đĩa 10 cm, đĩa chắn 20 cm đồng trục cách đèn 40 cm, màn cách đèn 100 cm: a) nếu nguồn điểm bóng 50 cm (Đ); b) vùng tối 35 cm (Đ);
   c) mép ngoài nửa tối 50 cm (S — đúng 65 cm); d) lùi màn ra xa thì vùng tối nhỏ lại (S — đĩa chắn lớn hơn nguồn nên vùng tối lớn lên).
PIII-1. Đèn đường cao 4,0 m, người 1,6 m đi ra xa 1,2 m/s → tốc độ đỉnh bóng **2,0** m/s (nhiễu 1,2; 0,8). topic: "Bóng tối, bóng nửa tối".
PIII-2. Laser, tia phản xạ vuông góc tường cách 2,5 m; quay gương 4° → vệt dịch **35** cm (35,1; nhiễu 17,5 quên 2δ). topic: "Định luật phản xạ ánh sáng".

## YCCĐ cho "Làm bài tương tự" — CHỜ THẦY QUYẾT
`scripts/data/question-topics.json` (254 YCCĐ L10–12) **không có** YCCĐ nào về phản xạ / gương phẳng / bóng (gần nhất chỉ có khúc xạ 81, phản xạ toàn phần 82–83 —
thuộc CĐ06, không dùng). `docs/HSG9-KHUNG.md` cũng để trống cột YCCĐ của CĐ14. Hai lựa chọn:
(1) để trống `yccd` → bài tập mẫu không hiện "Làm bài tương tự"; (2) thêm 3 YCCĐ mới (KHTN 7, mượn cho HSG) bằng migration:
"Định luật phản xạ ánh sáng", "Ảnh của vật tạo bởi gương phẳng", "Bóng tối, bóng nửa tối" — tên dùng ở các dòng `topic:` trên (ngân hàng hiện chưa có câu gắn nhãn này).

## Sai sót docx (đã sửa trong dàn ý)
1. B2.3 và G1 ghi "dù trường hợp nào, tia ló sau hai lần phản xạ hợp với tia tới góc $2\alpha$": chỉ đúng khi $\alpha \le 90^\circ$. Tổng quát góc lệch $D = 360^\circ - 2\alpha$,
   góc giữa tia ló và tia tới $= 360^\circ - 2\alpha$ khi $\alpha \gt 90^\circ$ (kiểm: $\alpha = 100^\circ$, $i_1 = 30^\circ$ → 160°, không phải 200°).
2. Nhóm lỗi 3: "tia phản xạ từ gương thứ nhất luôn tới được gương thứ hai nếu đi về phía O và gương đủ dài" — sai khi $\alpha \ge 90^\circ + i_1$
   (kiểm: $\alpha = 120^\circ$, $i_1 = 10^\circ$ → chỉ 1 lần phản xạ). Điều kiện đúng: $\alpha \lt 90^\circ + i_1$.
3. G1 (α = 60°, i₁ = 20°): tia tới hợp $G_1$ góc 70° > α nên nếu $G_2$ dài thì chính $G_2$ chắn tia tới — đề phải ghi gương có hạn hoặc nguồn đặt ngoài mép $G_2$.
   Bài tập mẫu D7 chọn số để tránh ($90^\circ - i_1 \lt \alpha$).
4. G3c: tại L = 150 cm docx nói "chỉ có vùng nửa tối"; chính xác hơn: giữa vùng nửa tối có một đĩa nhỏ (đường kính $|D_n + (d-D_n)L/a| = 5$ cm) nơi thấy nguồn thành vành sáng —
   vùng "đối tối" của nhật thực hình khuyên. Lý thuyết nói 1 câu, không đưa thuật ngữ mới.
5. Dạng 4 phương pháp mục 3 (hai gương song song, "ảnh thứ k cách gương theo quy luật cộng dồn") quá mơ hồ: thay bằng quy tắc "hai ảnh đầu cách nhau 2 lần khoảng cách gương;
   mỗi chuỗi ảnh xen kẽ đối xứng qua $G_1$, $G_2$" (D7d).
