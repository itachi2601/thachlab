# CĐ06. Khúc xạ ánh sáng, phản xạ toàn phần, lăng kính và tán sắc (bài 151, khoá Vật lí HSG & chuyên KHTN 9) — dàn ý chung

Nguồn: docx `06` (đã trích ở `nguon.txt` cùng thư mục — mục A, B, C, I dùng làm khung; ví dụ D/E/G/H trong docx KHÔNG chép,
số liệu dưới đây là số mới tự đặt). Viết lại bằng lời mình. Mọi số đã tính bằng `tinh.py` (chạy `python3 tinh.py`, kết quả chép nguyên dưới đây).
Phạm vi (docx A3): CT 2018 lớp 9 có định tính khúc xạ, $n = c/v$, định luật dạng sin trường hợp đơn giản, điều kiện phản xạ toàn phần,
đường truyền qua lăng kính, tán sắc và màu sắc vật. Mở rộng HSG/chuyên: $n_1\sin i = n_2\sin r$ định lượng, ảnh qua mặt phân cách,
vùng sáng tròn, bản mặt song song, góc lệch qua lăng kính (chỉ bằng hình học), sợi quang định lượng. Đề luôn cho sẵn bảng sin hoặc số.

**Ranh giới với CĐ07 (bài 156, Thấu kính & kính lúp):** mọi thứ về thấu kính, tiêu cự, dựng ảnh qua thấu kính, kính lúp, mắt thuộc CĐ07 — CĐ06 KHÔNG làm.
**Ranh giới với CĐ14 (bài 158):** định luật phản xạ, gương phẳng, bóng tối/nửa tối thuộc CĐ14; CĐ06 chỉ nhắc "luôn có một phần phản xạ".
Tuần dùng: buổi 13 (gửi 26/12): Thứ Tư đọc lý thuyết CĐ06 (40 phút), Thứ Năm bài tập mẫu CĐ06 (60 phút); Thứ Sáu tuần sau ôn tổng hợp Quang (`tuan.json`).

## Quy ước số liệu & ký hiệu (mọi file dùng chung)
- Chiết suất: không khí $n = 1$; nước $n = \frac43$; thuỷ tinh thường $1{,}5$; kim cương $2{,}42$. $c = 3\cdot10^8$ m/s.
- Tán sắc (thuỷ tinh): $n_đ = 1{,}50$ (đỏ), $n_t = 1{,}54$ (tím) — dùng y như vậy ở lý thuyết, BTM, luyện tập.
- **Mọi góc đo so với PHÁP TUYẾN**: góc tới $i$, góc khúc xạ $r$, góc giới hạn $i_{gh}$ (viết `i_{gh}`), góc chiết quang lăng kính $A$, góc lệch $D$.
  Lăng kính: mặt vào $AB$, mặt ra $AC$; ở mặt thứ hai góc tới $i_2$, góc ló $r_2$.
- Định luật: $n_1\sin i = n_2\sin r$ (môi trường 1 chứa tia tới). $n = \dfrac cv$. $\sin i_{gh} = \dfrac{n_2}{n_1}$ (chỉ khi $n_1 \gt n_2$).
- Độ sâu biểu kiến (nhìn gần vuông góc): $h' = \dfrac hn$; nhiều lớp $h' = \sum \dfrac{h_k}{n_k}$; vật trong không khí nhìn từ nước $H' = nH$.
- Bản mặt song song dày $e$: độ dời ngang $d = \dfrac{e\sin(i-r)}{\cos r}$; nhìn vuông góc, ảnh dịch lại gần mắt $\Delta = e\left(1-\dfrac1n\right)$.
- Góc làm tròn 0,1°; sin 4 chữ số; độ dài 2–3 chữ số có nghĩa. Bảng tra: $\sin 30° = 0{,}5$; $\sin 45° \approx 0{,}7071$; $\sin 60° \approx 0{,}8660$; $\sin 36° \approx 0{,}5878$.
- Hình: tia sáng nét liền mũi tên giữa tia; pháp tuyến và đường kéo dài nét đứt; ảnh ảo đánh dấu $S'$.

## Lý thuyết (theory.src.html) — 7 mục, ~40 phút
I. Mở bài: đồng xu "hiện ra" khi rót nước vào chậu (lùi tới khi vừa mất dấu đồng xu rồi rót nước). Câu dự đoán:
   (1) laser chiếu từ không khí vào nước với góc tới 50° — tia trong nước gần hay xa pháp tuyến hơn? (đáp: gần, $r \approx 35{,}1°$);
   (2) người đâm cá nhìn thấy cá ở điểm X — phải phóng lao cao hơn hay thấp hơn X? (thấp hơn — sâu hơn chỗ nhìn thấy).
II. Khúc xạ và chiết suất: hiện tượng, tên các yếu tố (điểm tới, pháp tuyến, mặt phẳng tới, $i$, $r$); $n = c/v$, bảng
   nước $v = 2{,}25\cdot10^8$, thuỷ tinh $2{,}00\cdot10^8$, kim cương $\approx 1{,}24\cdot10^8$ m/s; định luật $n_1\sin i = n_2\sin r$
   (tia khúc xạ ở bên kia pháp tuyến; vào môi trường chiết quang hơn ⇒ lệch gần pháp tuyến; $i = 0$ ⇒ truyền thẳng); tính thuận nghịch;
   luôn có một phần phản xạ đồng thời.
III. Ảnh qua mặt phân cách và bản mặt song song: chứng minh $h' = h\tan i/\tan r \approx h/n$ bằng hai tam giác vuông chung cạnh ngang
   (điều kiện nhìn gần vuông góc); $H' = nH$; nhiều lớp; quy tắc "ảnh dịch về phía môi trường chiết quang kém"; cọc cắm xiên trông gãy.
   Bản mặt song song: tia ló song song tia tới, chỉ dời ngang $d$; nhìn vuông góc qua bản kính dày $e$ thì vật trông gần hơn $e(1-1/n)$.
   Ví dụ số (khác BTM): kính 6 cm, $n = 1{,}5$ nhìn vuông góc ⇒ gần hơn 2 cm.
IV. Phản xạ toàn phần: tăng dần $i$ khi đi từ nước ra không khí — $r$ chạm 90° trước; $\sin i_{gh} = n_2/n_1$; hai điều kiện (cả hai cùng lúc);
   bảng $i_{gh}$: nước→kk 48,6°; thuỷ tinh→kk 41,8°; kim cương→kk 24,4°; thuỷ tinh→nước 62,7°; nước→thuỷ tinh: không có.
   Ứng dụng: vùng sáng tròn trên mặt nước $R = h\tan i_{gh}$ (nguồn điểm ở đáy); sợi quang (lõi chiết suất lớn hơn vỏ); kim cương lấp lánh; ảo ảnh đường nóng (định tính).
V. Lăng kính: tiết diện tam giác, góc chiết quang $A$, tia ló lệch về phía đáy. Trường hợp chính của HSG 9: tia tới vuông góc mặt $AB$
   ⇒ truyền thẳng, góc tới ở mặt $AC$ là $i_2 = A$ (chứng minh bằng góc có cạnh tương ứng vuông góc); nếu $A \ge i_{gh}$ thì phản xạ toàn phần ở $AC$;
   nếu ló thì $\sin r_2 = n\sin A$ và góc lệch $D = r_2 - A$. Lăng kính phản xạ toàn phần (tam giác vuông cân, $n \ge \sqrt2$): quay tia 90° hoặc 180° (ống nhòm, kính tiềm vọng).
   Mở rộng chuyên (một khung "Đọc thêm"): tia tới xiên, $D = i_1 + r_2 - A$ suy từ tổng góc trong tam giác — KHÔNG ra bài tính bằng công thức này (xem điểm cần thầy quyết).
VI. Tán sắc và màu sắc: ánh sáng trắng là hỗn hợp; chiết suất phụ thuộc màu ($n_đ \lt n_t$) ⇒ tím lệch nhiều nhất, thứ tự đỏ→tím từ đỉnh xuống đáy;
   cầu vồng (khúc xạ – phản xạ – khúc xạ trong giọt nước, định tính); màu của vật = màu ánh sáng nó hắt lại nhiều (vật trắng hắt mọi màu, vật đen hấp thụ hết,
   lá xanh dưới đèn đỏ trông đen); tấm lọc màu cho qua màu của nó, hấp thụ màu khác (lọc đỏ chồng lọc lục ⇒ tối); trộn ánh sáng màu trên màn trắng:
   đỏ + lục ⇒ vàng, đỏ + lam ⇒ đỏ tím (magenta), lục + lam ⇒ lam lục (cyan), đỏ + lục + lam ⇒ trắng (khác pha màu sơn).
VII. Trả bài và mang về (6 câu tự trả lời).

Bẫy (từ mục I docx, viết lại + bổ sung): đo góc so với mặt phân cách; viết ngược tỉ số chiết suất (kiểm: vào nước mà ra $r \gt i$ là sai);
nghĩ phản xạ toàn phần xảy ra khi đi vào nước; thiếu một trong hai điều kiện; nhầm $\sin i_{gh} = n_1/n_2$ (ra số $\gt 1$); "$r = 90°$ là mất tia khúc xạ"
(chưa — tia đi là là); chiết suất lớn ⇒ ánh sáng nhanh (ngược); dùng $h/n$ khi nhìn xiên (xiên thì còn nông hơn nữa); nhân thay vì chia;
tia đỏ lệch nhiều nhất (ngược); tưởng bản mặt song song làm tia đổi hướng; trộn ánh sáng đỏ + lục ra nâu như pha sơn (thực ra vàng);
lăng kính vuông cân: lấy góc 90° làm $i_2$ (phải lấy góc giữa mặt vào và mặt tia gặp, 45°).

## Bài tập mẫu (scripts/data/bai-tap-mau/151.json) — 7 dạng, cấp không giảm. SỐ LIỆU ĐÃ TÍNH, dùng nguyên.
D1 (cấp 1) **Định luật khúc xạ, chiết suất và vận tốc.** Laser từ không khí vào một chất lỏng: $i = 60°$, đo được $r = 36°$ (cho $\sin36° \approx 0{,}5878$).
   (a) $n = \frac{0{,}8660}{0{,}5878} \approx 1{,}47$; $v \approx 2{,}04\cdot10^8$ m/s. (b) Chiếu ngược từ chất lỏng ra không khí với $i = 30°$: $\sin r \approx 0{,}737$ ⇒ $r \approx 47{,}4°$ (lệch xa pháp tuyến).
   (c) Với $i = 60°$, góc giữa tia phản xạ và tia khúc xạ $= 180° - 60° - 36° = 84°$. (d, mở rộng) Góc tới để tia phản xạ ⊥ tia khúc xạ: $r = 90° - i$ ⇒ $\tan i = n$ ⇒ $i \approx 55{,}8°$, $r \approx 34{,}2°$.
   topic: "Chiết suất và định luật khúc xạ ánh sáng".
D2 (cấp 2) **Độ sâu biểu kiến nhiều lớp.** Bể: lớp dầu $n = 1{,}4$ dày 14 cm nổi trên lớp nước dày 80 cm; nhìn gần vuông góc.
   (a) Đáy trông sâu $\frac{14}{1{,}4} + \frac{80}{4/3} = 10 + 60 = 70$ cm (nâng 24 cm). (b) Cá ở 40 cm dưới mặt phân cách dầu–nước: trông cách mặt dầu $10 + 30 = 40$ cm.
   (c) Cá nhìn lên đèn treo 150 cm trên mặt dầu: đèn trông cách cá $\frac43\left(\frac{40}{4/3} + \frac{14}{1{,}4} + 150\right) \approx 253{,}3$ cm (thật 204 cm), tức cao ≈ 199,3 cm trên mặt dầu.
   topic: "Mô tả hiện tượng khúc xạ, vẽ đường truyền tia sáng".
D3 (cấp 2) **Phản xạ toàn phần: vùng sáng tròn, đĩa chắn.** Bóng đèn nhỏ ở đáy bể nước sâu 0,9 m.
   (a) $i_{gh} \approx 48{,}6°$, $\tan i_{gh} = 3/\sqrt7 \approx 1{,}134$ ⇒ vùng sáng bán kính $R \approx 1{,}02$ m (diện tích ≈ 3,27 m²); đĩa chắn nổi, tâm ngay trên đèn, bán kính tối thiểu ≈ 1,02 m.
   (b) Thay nước bằng chất lỏng $n = 1{,}6$ cùng độ sâu: $i_{gh} \approx 38{,}7°$, $\tan \approx 0{,}801$ ⇒ $R \approx 0{,}72$ m (thu hẹp).
   (c) Có sẵn đĩa bán kính 0,5 m nổi trên nước: đèn đặt dưới tâm đĩa sâu tối đa $h = 0{,}5/1{,}134 \approx 0{,}44$ m thì không tia nào ló ra.
   topic: "Điều kiện xảy ra phản xạ toàn phần".
D4 (cấp 2–3) **Bản mặt song song.** Tấm kính dày 6 cm, $n = 1{,}5$, tia tới $i = 60°$.
   (a) $\sin r \approx 0{,}5774$ ⇒ $r \approx 35{,}3°$; tia ló song song tia tới; đường đi trong kính ≈ 7,35 cm. (b) Độ dời ngang $d = \frac{6\sin(24{,}7°)}{\cos 35{,}3°} \approx 3{,}07$ cm.
   (c) Bảng $i$–$d$: 30° → 1,16 cm; 45° → 1,97 cm; 60° → 3,07 cm; 75° → 4,49 cm (i càng lớn dời càng nhiều; $i = 0$ không dời).
   (d) Nhìn vuông góc qua tấm kính xuống trang sách: chữ trông gần hơn $6(1 - 1/1{,}5) = 2$ cm. topic: "Chiết suất và định luật khúc xạ ánh sáng".
D5 (cấp 3) **Lăng kính: góc lệch và tán sắc.** Lăng kính thuỷ tinh $A = 30°$, chùm sáng trắng hẹp tới vuông góc mặt $AB$; $n_đ = 1{,}50$, $n_t = 1{,}54$.
   (a) Ở $AC$: $i_2 = 30°$; đỏ $\sin r_2 = 0{,}75$ ⇒ $r_2 \approx 48{,}6°$, $D_đ \approx 18{,}6°$; tím $\sin r_2 = 0{,}77$ ⇒ $r_2 \approx 50{,}4°$, $D_t \approx 20{,}4°$; góc mở đỏ–tím ≈ 1,76°.
   (b) Màn đặt vuông góc phương tia tới, cách lăng kính 1,2 m: vệt màu rộng $1{,}2(\tan D_t - \tan D_đ) \approx 4{,}2$ cm (tan 0,3364 và 0,3710); tím gần đáy.
   (c) Đặt tấm lọc đỏ trước màn ⇒ chỉ còn vệt đỏ; chồng thêm lọc lục ⇒ màn tối. Màn là tờ giấy xanh lục thay giấy trắng ⇒ chỉ vùng lục sáng rõ, vùng đỏ gần như đen.
   (d) Đổi sang $A = 41°$: $i_{gh,đ} \approx 41{,}8° \gt 41°$ ⇒ đỏ ló ($r_2 \approx 79{,}8°$); $i_{gh,t} \approx 40{,}5° \lt 41°$ (tức $1{,}54\sin41° \approx 1{,}010 \gt 1$) ⇒ tím phản xạ toàn phần.
   topic: "Tán sắc ánh sáng qua lăng kính" (a, b: "Đường truyền tia sáng qua lăng kính").
D6 (cấp 3) **Lăng kính phản xạ toàn phần.** Lăng kính thuỷ tinh tam giác vuông cân, tia tới vuông góc mặt huyền (gần một đầu).
   (a) Tia gặp lần lượt hai mặt bên với góc tới 45° > 41,8° ⇒ phản xạ toàn phần hai lần, ló ra qua mặt huyền ngược chiều tia tới (quay 180°, dời ngang) — ống nhòm.
   (b) Điều kiện trong không khí: $n \ge \sqrt2 \approx 1{,}414$. (c) Nhúng lăng kính vào nước: cần $n \ge \frac43\sqrt2 \approx 1{,}886$; thuỷ tinh 1,5 có $i_{gh,thuỷ\,tinh→nước} \approx 62{,}7° \gt 45°$
   ⇒ không còn phản xạ toàn phần; tia ló vào nước ở mặt bên thứ nhất với $\sin r \approx 0{,}796$ ⇒ $r \approx 52{,}7°$ (lệch 7,7° so với phương tới). topic: "Điều kiện xảy ra phản xạ toàn phần".
D7 (cấp 4) **Sợi quang định lượng.** Lõi $n_1 = 1{,}60$, vỏ $n_2 = 1{,}50$, đầu sợi phẳng vuông góc trục, đặt trong không khí; dài 1 km.
   (a) $\sin i_{gh} = 0{,}9375$ ⇒ $i_{gh} \approx 69{,}6°$ ⇒ trong lõi tia hợp với trục tối đa $20{,}4°$ ⇒ góc tới tối đa ở đầu sợi $\sin i_{max} = 1{,}6\sin20{,}36° = \sqrt{n_1^2 - n_2^2} \approx 0{,}557$ ⇒ $i_{max} \approx 33{,}8°$.
   (b) Thời gian truyền 1 km: tia dọc trục $\approx 5{,}333$ µs; tia xiên nhất (đường dài $L/\sin i_{gh}$) $\approx 5{,}689$ µs; chênh ≈ 356 ns (lí do xung bị "nhoè").
   (c) Đầu sợi nhúng trong nước: $\sin i_{max} = 0{,}557/(4/3) \approx 0{,}418$ ⇒ $i_{max} \approx 24{,}7°$. topic: "Tính góc tới hạn, ứng dụng cáp quang".

## Tự luận (tu_luan) — 8 bài dễ → khó, mỗi bài có Hướng dẫn giải trong <details>. Số đã tính (tinh.py, mục "Tự luận").
TL1. Đồng xu ở đáy cốc nước sâu 12 cm, nhìn gần vuông góc ⇒ trông sâu 9,0 cm (nâng 3 cm); giải thích vì sao rót nước thì đồng xu "hiện ra".
TL2. Màu sắc (định tính, không tính): áo trắng / lá xanh lục / chữ đỏ trên giấy trắng dưới đèn đỏ, đèn lục; nhìn qua kính lọc đỏ; trộn đèn đỏ + đèn lục trên tường trắng (vàng); vì sao màn hình chỉ cần ba màu.
TL3. Ánh sáng đi 3 m trong nước mất ≈ 13,3 ns, trong không khí 10,0 ns; trong cùng thời gian đó ánh sáng đi được 4,0 m trong không khí.
TL4. Nhìn xiên: cá sâu 0,6 m, tia từ cá ló ra không khí với $\sin r = 0{,}8$ ($r \approx 53{,}1°$) ⇒ $\sin i = 0{,}6$, $i \approx 36{,}9°$; điểm ló cách chân đường thẳng đứng qua cá 0,45 m;
   ảnh (giao đường kéo dài với đường thẳng đứng qua cá) sâu ≈ 0,338 m — nông hơn giá trị $h/n = 0{,}45$ m khi nhìn vuông góc. Kết luận về người đâm cá.
TL5. Bóng cọc trên đáy bể: bể sâu 0,8 m đầy nước, cọc 1,2 m cắm thẳng đứng chạm đáy, nắng tới với $i = 60°$ ⇒ $r \approx 40{,}5°$;
   bóng dài $0{,}4\tan60° + 0{,}8\tan40{,}5° \approx 0{,}693 + 0{,}683 \approx 1{,}38$ m (bể cạn sẽ là 2,08 m).
TL6. Bản kính dày 4 cm, $n = 1{,}6$, $i = 45°$: $r \approx 26{,}2°$, độ dời ngang ≈ 1,43 cm; nhìn vuông góc chữ trông gần hơn 1,50 cm.
TL7. Khối lập phương trong suốt: tia vào mặt trên với góc tới bất kì, khúc xạ rồi gặp mặt bên kề. Chứng minh: muốn mọi tia đều phản xạ toàn phần ở mặt bên thì $n \ge \sqrt2 \approx 1{,}414$
   (góc tới mặt bên nhỏ nhất $= 90° - r_{max}$; $n = 1{,}5$: 48,2° > 41,8° thoả; $n = 1{,}3$: 39,7° < 50,3° không thoả).
TL8. Lăng kính tam giác đều $n = 1{,}5$, tia tới vuông góc $AB$: gặp $AC$ với góc tới 60° > 41,8° ⇒ phản xạ toàn phần, rồi tới $BC$ vuông góc (góc tới 0°) và ló thẳng;
   tia ló hợp với phương tia tới 60°. Điều kiện phản xạ toàn phần ở $AC$: $n \ge 1/\sin60° \approx 1{,}155$. (Bài tổng hợp vẽ hình + chứng minh góc.)
Số liệu KHÁC bài tập mẫu và KHÁC ví dụ D/E/G của docx.

## Luyện tập (8 câu, tự chấm, nhãn như đề thật): 4 câu Phần I (A–D), 2 câu Phần II (a)–d) Đúng/Sai), 2 câu Phần III (đáp số). Số từ tinh.py.
I.1 Chất lỏng $n = 1{,}25$: vận tốc ánh sáng — **2,40·10⁸ m/s** (nhiễu: 3,75·10⁸; 1,25·10⁸; 3,00·10⁸).
I.2 Cùng chất lỏng ra không khí: góc giới hạn — **53,1°** (nhiễu: 36,9°; 48,6°; 41,8°).
I.3 Lá cây xanh lục dưới ánh đèn đỏ thuần trông — **gần như đen** (nhiễu: đỏ; vàng; xanh lục).
I.4 Lăng kính $A = 40°$, $n = 1{,}5$, tia vuông góc mặt $AB$: góc lệch — **≈ 34,6°** ($\sin r_2 \approx 0{,}964$, $r_2 \approx 74{,}6°$; nhiễu: 40°; 74,6°; "không ló vì phản xạ toàn phần" — sai vì 40° < 41,8°).
II.1 Phản xạ toàn phần / sợi quang: a) xảy ra khi ánh sáng từ nước vào thuỷ tinh (S); b) kim cương $i_{gh} \approx 24{,}4°$ nên dễ phản xạ toàn phần hơn thuỷ tinh (Đ);
   c) khi $r = 90°$ thì đã hết tia khúc xạ (S); d) lõi sợi quang phải có chiết suất lớn hơn vỏ (Đ).
II.2 Ảnh qua mặt phân cách / bản mặt: a) hồ sâu 2 m nhìn vuông góc trông sâu 1,50 m (Đ); b) bản kính dày 3 cm, $n = 1{,}5$ đặt lên trang sách, nhìn vuông góc chữ trông gần hơn 1,0 cm (Đ);
   c) tia ló khỏi bản mặt song song lệch về phía pháp tuyến so với tia tới (S — song song tia tới); d) nhìn xiên thì đáy hồ trông sâu hơn khi nhìn vuông góc (S — nông hơn).
III.1 Hồ sâu 1,8 m, nhìn gần vuông góc: đáy trông cách mặt nước bao nhiêu mét? — **1,35**.
III.2 Đèn nhỏ ở độ sâu 0,6 m trong nước: bán kính vùng sáng trên mặt nước (m, làm tròn 2 chữ số thập phân)? — **0,68**.
Phủ: $n = c/v$, $i_{gh}$, màu vật, lăng kính (tính), điều kiện PXTP + sợi quang, độ sâu biểu kiến + bản mặt, vùng sáng (tính).

## YCCĐ cho "Làm bài tương tự"
Dùng YCCĐ của KHTN 9 Chương 2 (mô tả bài 83–85 trên web, đã có trong `scripts/data/bai-tap-mau/83.json`, `84.json`):
"Mô tả hiện tượng khúc xạ, vẽ đường truyền tia sáng", "Chiết suất và định luật khúc xạ ánh sáng" (bài 83);
"Điều kiện xảy ra phản xạ toàn phần", "Tính góc tới hạn, ứng dụng cáp quang" (bài 84);
"Đường truyền tia sáng qua lăng kính", "Tán sắc ánh sáng qua lăng kính" (bài 85 — chưa có 85.json, cần tra `topic_id` trong DB trước khi gắn).
Màu sắc vật / tấm lọc màu: chưa thấy YCCĐ riêng — tạm gắn "Tán sắc ánh sáng qua lăng kính" (cần thầy chốt).

## Sai sót docx (đã sửa trong dàn ý này)
1. B2.8 Cầu vồng: docx nói ở mặt sau giọt nước "có thể là phản xạ toàn phần" — sai: giọt cầu đối xứng, góc tới ở mặt sau bằng đúng góc khúc xạ $r \lt i_{gh}$,
   nên chỉ có phản xạ một phần (vì thế cầu vồng mờ). Lý thuyết mục VI ghi "phản xạ (một phần)".
2. B2.6 ví dụ lăng kính vuông cân ghi "$A = 90°$" ngay sau công thức $i_2 = A$ rồi kết luận góc tới ở mặt huyền là 45° — mâu thuẫn. Đúng: $A$ trong $i_2 = A$ là góc
   giữa mặt tia đi vào và mặt tia gặp tiếp theo (cạnh góc vuông – mặt huyền: 45°). Lý thuyết mục V ghi rõ, thêm vào Bẫy.
3. Dạng 5 c) đáp số "cá vẫn trông nông hơn" thiếu ý chính: nhìn xiên thì trông **nông hơn nữa** so với nhìn vuông góc (chính docx G2 d đã chứng minh $h'/h \lt 1/n$). Dùng trong TL4.
4. B2.5 gọi phép xấp xỉ góc nhỏ $\tan \approx \sin$ là "giá trị làm tròn" — sai thuật ngữ; ghi là "xấp xỉ góc nhỏ".
5. Thiếu nội dung so với phạm vi docx A3 tự nêu: không có phần **màu sắc vật, tấm lọc màu, trộn ánh sáng màu** và **bản mặt song song** — dàn ý bổ sung mới (mục III, VI; D4, D5c).
6. Ảo ảnh đường nóng: docx tả như một lần phản xạ toàn phần ở "lớp sát mặt đường"; thực chất tia cong dần qua các lớp chiết suất giảm liên tục — lý thuyết chỉ nói định tính "cong dần rồi hướng lên".

## Điểm cần thầy quyết
- Góc lệch lăng kính: docx A3 loại công thức tổng quát $A$, $D$; dàn ý chỉ tính $D = r_2 - A$ cho tia tới vuông góc mặt bên (giải bằng hình học), công thức $D = i_1 + r_2 - A$ để ở khung "Đọc thêm". Có cho ra bài tia xiên không?
- D1 (d) góc Brewster ($\tan i = n$) là mở rộng chuyên — giữ hay bỏ.
- YCCĐ cho phần màu sắc vật (xem trên).
