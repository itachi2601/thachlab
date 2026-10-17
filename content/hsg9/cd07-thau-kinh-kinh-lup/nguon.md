# CĐ07. Thấu kính mỏng và kính lúp (bài 156, khoá Vật lí HSG & chuyên KHTN 9) — dàn ý chung

Nguồn: docx `07` (đã trích ở `nguon.txt` cùng thư mục — mục A, B, C (phương pháp), I (lỗi thường gặp) dùng làm khung;
ví dụ mẫu mục C, bài D/E/G và câu H trong docx KHÔNG chép, số liệu dưới đây là số mới tự đặt). Viết lại bằng lời mình.
Mọi số tính trong `tinh.py` cùng thư mục (`python3 tinh.py`, có assert) — sửa số thì sửa ở đó rồi chép lại.

**Phạm vi (docx ghi, phải nói rõ với HS):** YCCĐ KHTN 9 chỉ gồm: khái niệm quang tâm, trục chính, tiêu điểm, tiêu cự; vẽ ảnh;
thí nghiệm ảnh thật hứng được / ảnh ảo không; vẽ sơ đồ tỉ lệ cho bài tập đơn giản về TK hội tụ; cấu tạo và dùng kính lúp;
đo tiêu cự TK hội tụ. **Ngoài YCCĐ, bổ sung cho HSG:** công thức $\frac1f=\frac1d+\frac1{d'}$, $G=\frac{25}{f}$, hệ hai thấu kính,
mắt (chỉ định tính + điểm cực cận/cực viễn để hiểu kính lúp). Không dùng: công thức Newton, công thức độ tụ hệ ghép cách nhau,
đạo hàm. Mọi bài giải được bằng tam giác đồng dạng + đại số (phương trình bậc hai, điều kiện $\Delta \ge 0$).

**Ranh giới:** khúc xạ, phản xạ toàn phần, lăng kính, tán sắc thuộc CĐ06 (bài 151) — CĐ07 chỉ nhắc một câu "thấu kính làm lệch tia
nhờ khúc xạ ở hai mặt" rồi dùng ngay quy tắc ba tia. Gương phẳng thuộc CĐ14. "12 câu tự luyện CĐ07" (buổi 15 thứ Hai) KHÔNG làm ở đây.
**Tuần dùng** (`tuan.json`): buổi 14 (gửi 02/01/2027): thứ Hai đọc lý thuyết + quiz; thứ Ba BTM dựng ảnh (giấy ô ly, thước, bút chì);
thứ Tư BTM công thức + quy ước dấu; thứ Năm vẽ 2 bài trên giấy ô ly. Buổi 15 (gửi 09/01): thứ Ba dịch chuyển vật–ảnh, hệ hai TK;
thứ Tư đọc cách đo tiêu cự (Kiểm tra 3 Quang có câu thí nghiệm đo tiêu cự).

## Quy ước số liệu & ký hiệu (mọi file dùng chung, viết y như vậy)
- Vật sáng $AB$ vuông góc trục chính $\Delta$, $A$ trên trục; ảnh $A'B'$. Quang tâm $O$; tiêu điểm vật $F$, tiêu điểm ảnh $F'$, $OF=OF'=|f|$.
  Điểm tới của tia song song: $I$ (trên thấu kính, $OI = AB$). Tia qua $F$ gặp thấu kính tại $K$ ($OK = A'B'$).
- $d = OA > 0$ (vật thật). $d'$: **$d'>0$ ảnh thật** (khác phía vật), **$d'<0$ ảnh ảo** (cùng phía vật), $|d'|$ là khoảng cách ảnh–TK.
  **$f>0$ TK hội tụ, $f<0$ TK phân kì.** Công thức duy nhất: $\dfrac1f=\dfrac1d+\dfrac1{d'}$ ⇒ $d'=\dfrac{df}{d-f}$.
- Độ cao: $h = AB$, $h' = A'B' > 0$ (độ dài hình học). Tỉ số $|k| = \dfrac{h'}{h} = \dfrac{|d'|}{d}$. Chiều: $d'>0$ ngược chiều, $d'<0$ cùng chiều.
  Không dùng số phóng đại có dấu ở bài HS; hệ hai TK đếm số lần đảo chiều (mỗi ảnh thật đảo một lần).
- Khoảng cách vật–ảnh: ảnh thật $L = d + d'$; ảnh ảo $L = \big|\,d - |d'|\,\big|$.
- Hệ hai TK cách nhau $a$: $d_2 = a - d_1'$ (đúng cả khi $d_1' < 0$: $d_2 = a + |d_1'|$); chỉ xét $d_2 > 0$ (vật thật cho TK2), trừ trường hợp ghép sát.
  Ghép sát: $\dfrac1f=\dfrac1{f_1}+\dfrac1{f_2}$.
- Bessel: vật–màn $L$ cố định, hai vị trí TK cách nhau $\ell$: $f = \dfrac{L^2-\ell^2}{4L}$, điều kiện $L \ge 4f$. Kính lúp $G = \dfrac{25}{f}$ ($f$ tính bằng cm,
  mắt tốt, ngắm chừng ở vô cực). Điểm cực cận $C_c$, cực viễn $C_v$; mắt tốt $OC_c = 25$ cm, $C_v$ ở vô cực. Kính đặt sát mắt.
- Đơn vị cm cho mọi khoảng cách; kết quả lẻ làm tròn 2 chữ số thập phân hoặc để phân số.
- Hình: tia sáng nét liền có mũi tên giữa tia; đường kéo dài và ảnh ảo nét đứt; TK hội tụ vẽ đoạn thẳng có hai mũi tên hướng ra,
  phân kì hai đầu chữ V hướng vào. Hình bài tập không vẽ sẵn ảnh/kết quả.
- Đối chiếu SBT KNTT: sách viết $\frac1f = \frac1d - \frac1{d'}$ cho ảnh ảo với $d'$ là độ dài dương — cùng một phương trình, khác quy ước. Nhắc HS đọc quy ước của đề.

## Lý thuyết (theory.src.html) — 7 mục, ~18 phút
I. **Mở bài**: giọt nước đọng trên lá phóng to gân lá; kính lúp hứng nắng đốt giấy. Hai câu dự đoán:
   (1) Che nửa trên một thấu kính hội tụ đang cho ảnh rõ trên màn — ảnh mất nửa trên, mất nửa dưới, hay vẫn đủ nhưng tối hơn? (đáp: vẫn đủ, tối hơn —
   mỗi điểm ảnh do cả chùm tia qua mọi phần thấu kính tạo nên);
   (2) Cầm kính lúp sát dòng chữ rồi kéo xa dần — chữ to lên mãi, hay tới lúc nào đó lộn ngược? (đáp: to dần, mờ đi qua $d=f$, rồi lộn ngược khi $d>f$).
II. **Thấu kính, ba tia đặc biệt, dựng ảnh**: nhận dạng HT/PK theo hình dạng (rìa mỏng/rìa dày) và theo chùm tia; trục chính, $O$, $F$, $F'$, $f$;
   HT: $F'$ khác phía vật; PK: $F'$ cùng phía vật. Ba tia (song song → qua $F'$; qua $F$ → song song; qua $O$ → thẳng), bản PK dùng đường kéo dài.
   Quy trình 4 bước dựng ảnh trên **giấy ô ly** (trục → TK → $F$, $F'$ đúng số ô → vật → 2 tia từ $B$ → $B'$ → hạ $A'$), dùng tia thứ ba để kiểm.
   Điểm sáng $S$ trên trục chính: tia bất kì $SI$ + trục phụ qua $O$ song song $SI$ cắt tiêu diện ảnh tại $F_1'$ ⇒ tia ló qua $F_1'$.
   Bảng vị trí vật → ảnh (HT: $d>2f$, $d=2f$, $f<d<2f$, $d=f$, $d<f$; PK: luôn ảo, cùng chiều, nhỏ hơn, trong khoảng $OF'$).
   Thí nghiệm Làm–Quan sát–Rút ra: hứng ảnh ngọn đèn trên màn (ảnh thật) / không hứng được ảnh qua kính lúp (ảnh ảo).
III. **Công thức thấu kính + quy ước dấu + chứng minh** (trọng tâm HSG, HS phải tự chứng minh được ba trường hợp):
   (a) HT ảnh thật: $\triangle OAB \sim \triangle OA'B'$ ⇒ $\frac{h'}{h}=\frac{d'}{d}$; $\triangle F'OI \sim \triangle F'A'B'$ ⇒ $\frac{h'}{h}=\frac{d'-f}{f}$ ⇒ $fd' = dd' - df$ ⇒ chia $dd'f$ ⇒ $\frac1f=\frac1d+\frac1{d'}$.
   (b) HT ảnh ảo (đặt $d'=-|d'|$): $\frac{h'}{h}=\frac{|d'|}{d}=\frac{|d'|+f}{f}$ ⇒ $\frac1f=\frac1d-\frac1{|d'|}$ — cùng công thức khi thay $d'<0$.
   (c) PK (đặt $f=-|f|$): $\frac{h'}{h}=\frac{|d'|}{d}=\frac{|f|-|d'|}{|f|}$ ⇒ $-\frac1{|f|}=\frac1d-\frac1{|d'|}$ — cùng công thức.
   Ví dụ kiểm quy ước (tinh.py): HT $f=12$, $d=20$ ⇒ $d'=30$, ảnh thật, ngược chiều, $h'=1{,}5h$; HT $f=12$, $d=8$ ⇒ $d'=-24$, ảnh ảo, cùng chiều, $h'=3h$;
   PK $f=-12$, $d=12$ ⇒ $d'=-6$, ảnh ảo, $h'=0{,}5h$. Mẹo kiểm nhanh: ảnh ảo của HT thì $|d'|>d$; ảnh của PK thì $|d'|<|f|$ và $|d'|<d$.
IV. **Dịch chuyển vật–ảnh, khoảng cách vật–ảnh nhỏ nhất, hai vị trí**:
   $d' = f + \dfrac{f^2}{d-f}$ (biến đổi đại số) ⇒ HT, $d>f$: $d$ giảm thì $d'$ tăng — **vật và ảnh thật luôn dịch cùng chiều** (cùng chiều truyền ánh sáng), ảnh lớn dần.
   Bảng $f=12$: $d = 60, 36, 24, 18, 16, 14, 13$ ⇒ $d' = 15, 18, 24, 36, 48, 84, 156$; $|k| = 0{,}25;\ 0{,}5;\ 1;\ 2;\ 3;\ 6;\ 12$; $L = 75, 54, 48, 54, 64, 98, 169$.
   $L = d+d'$ ⇒ $d^2 - Ld + Lf = 0$ có nghiệm ⇔ $\Delta = L^2 - 4Lf \ge 0$ ⇔ **$L \ge 4f$**, dấu bằng khi $d=d'=2f$ (ảnh bằng vật).
   $L>4f$: hai nghiệm $d_1 + d_2 = L$, $d_1d_2 = Lf$ ⇒ $\ell^2 = L^2-4Lf$ ⇒ $f=\frac{L^2-\ell^2}{4L}$; hai vị trí đối xứng ($d_1 = d_2'$), $h_1'h_2' = h^2$.
   Ảnh ảo HT ($d<f$): vật lại gần TK thì ảnh ảo lại gần TK và nhỏ dần. PK: vật ra xa thì ảnh ảo ra xa TK, tiến dần về $F'$.
V. **Hệ hai thấu kính đồng trục**: sơ đồ $AB \xrightarrow{TK_1} A_1'B_1' \xrightarrow{TK_2} A_2'B_2'$; ảnh qua TK1 là vật của TK2, $d_2 = a - d_1'$;
   $h_2' = h\cdot\frac{|d_1'|}{d_1}\cdot\frac{|d_2'|}{d_2}$; chiều: đếm số ảnh thật (mỗi lần đảo chiều). Ghép sát: $\frac1f=\frac1{f_1}+\frac1{f_2}$
   (hai HT ⇒ hội tụ mạnh hơn; HT + PK cùng $|f|$ ⇒ như tấm kính phẳng). Không dùng công thức độ tụ cho hệ cách nhau.
VI. **Kính lúp và đo tiêu cự (thực hành)**: kính lúp = TK hội tụ $f$ ngắn, vật đặt trong $OF$; mắt (định tính): thể thuỷ tinh ~ TK hội tụ, màng lưới ~ màn,
   điều tiết, $C_c$, $C_v$; ngắm chừng ở $C_c$ (ảnh ảo tại $C_c$, $d'=-OC_c$) và ở vô cực ($d=f$); $G=\frac{25}{f}$ (kính ghi 5× ⇒ $f=5$ cm), phân biệt $G$ với $|k|$.
   Ba cách đo $f$: (1) vật rất xa ⇒ ảnh ở $F'$; (2) **2f–2f**: dịch TK và màn tới khi ảnh bằng vật, hoặc tìm $L$ nhỏ nhất ⇒ $f=L/4$;
   (3) **Bessel**: vật–màn cố định $L>4f$, đo $\ell$ ⇒ $f=\frac{L^2-\ell^2}{4L}$. Sai số: đo 3 lần, $f = \bar f \pm \Delta f$; với Bessel, đổi $L$ thêm 1 cm
   làm $f$ đổi ≈ 0,34 cm còn đổi $\ell$ thêm 1 cm làm $f$ đổi ≈ 0,30 cm (số D5, tinh.py) ⇒ đo $L$ cẩn thận hơn (lập luận bằng số, không đạo hàm).
VII. **Trả bài và mang về** (6 câu tự trả lời): $f$ của PK âm hay dương; $d'<0$ nghĩa là gì; $d=2f$ thì ảnh ở đâu, cao bao nhiêu; vì sao $L\ge 4f$;
   ảnh qua TK1 đóng vai gì với TK2; kính ghi 2,5× có tiêu cự bao nhiêu.

**Bẫy** (từ mục I docx + bổ sung, viết lại): (1) giải ra $\frac1{d'}<0$ vẫn kết luận ảnh thật; (2) quên $f<0$ với PK; (3) cố hứng ảnh ảo trên màn;
(4) tính khoảng cách vật–ảnh ảo bằng $d+|d'|$; (5) nhầm $G$ với tỉ số $\frac{h'}{h}$; (6) dùng công thức Bessel khi $L<4f$; (7) dùng tia qua $O$ cho điểm sáng
trên trục chính; (8) làm tròn giữa chừng; (9) che nửa thấu kính tưởng mất nửa ảnh; (10) bài "ảnh cao gấp $n$ lần" chỉ xét ảnh thật, bỏ sót ảnh ảo;
(11) hệ hai TK lấy $d_2 = a$ hoặc quên ảnh trung gian ảo ($d_2 = a + |d_1'|$); (12) vẽ $F'$ của PK ở khác phía vật.

## Bài tập mẫu (scripts/data/bai-tap-mau/156.json) — 7 dạng, cấp không giảm. SỐ LIỆU ĐÃ TÍNH (tinh.py), dùng nguyên.
D1 (cấp 1) **Dựng ảnh trên giấy ô ly (thuận và ngược).** Quy ước 1 ô = 2 cm.
   (a) TK HT $f=8$ cm (4 ô), vật cao 2 cm (1 ô), $d=12$ cm (6 ô): dựng bằng 2 tia, kiểm bằng tia thứ ba ⇒ đọc trên lưới $d'=24$ cm (12 ô), $h'=4$ cm (2 ô), ảnh thật, ngược chiều.
   (b) Bài ngược: cho trục chính, $B$ tại $(-24;\,3)$, $B'$ tại $(-8;\,1)$ (cm, gốc chưa biết là $O$), $B'$ cùng phía, cùng chiều, nhỏ hơn ⇒ TK phân kì;
   $O$ = giao $BB'$ với trục (tại $x=0$); tia từ $B$ song song trục tới $I(0;3)$, đường kéo dài tia ló qua $B'$ cắt trục tại $F'$ ($x=-12$) ⇒ $f=-12$ cm.
   Hình: lưới ô ly SVG, chỉ có trục + điểm đề cho. topic: "Dựng ảnh của vật qua thấu kính".
D2 (cấp 2) **Công thức + quy ước dấu + chứng minh lại bằng tam giác đồng dạng.**
   (a) HT $f=20$, vật cao 1 cm, $d=15$ ⇒ $d'=-60$ cm, ảnh ảo, cùng chiều, $h'=4$ cm, cách vật 45 cm. Yêu cầu: dựng ảnh rồi chỉ hai cặp tam giác đồng dạng để ra lại $d'$.
   (b) PK $f=-30$, vật cao 1,5 cm, $d=15$ ⇒ $d'=-10$ cm, $h'=1$ cm, ảnh cách vật 5 cm. topic: "Công thức thấu kính và số phóng đại".
D3 (cấp 2–3) **Bài toán ngược nhiều trường hợp** (bẫy bỏ sót ảnh ảo). TK HT $f=12$ cm.
   (a) Ảnh cao gấp 3 vật: ảnh thật $d=16$, $d'=48$ (cách vật 64 cm); ảnh ảo $d=8$, $d'=-24$ (cách vật 16 cm).
   (b) Tìm mọi vị trí vật để ảnh cách vật 50 cm: ảnh thật $d^2-50d+600=0$ ⇒ $d=20$ ($d'=30$) hoặc $d=30$ ($d'=20$);
   ảnh ảo $d^2+50d-600=0$ ⇒ $d=10$ ($d'=-60$). **Ba vị trí.** topic: "Công thức thấu kính và số phóng đại".
D4 (cấp 3) **Dịch chuyển vật–ảnh, khoảng cách nhỏ nhất 4f.** TK HT $f=15$ cố định, vật cao 2 cm.
   (a) $d=45$ ⇒ $d'=22{,}5$, $L=67{,}5$, $|k|=0{,}5$; dịch vật lại gần 15 cm ($d=30$) ⇒ $d'=30$, $L=60$, $|k|=1$: ảnh dịch ra xa TK 7,5 cm (cùng chiều với vật).
   (b) Dịch tiếp 10 cm ($d=20$) ⇒ $d'=60$, $L=80$, $|k|=3$: ảnh dịch 30 cm; $L$ giảm rồi tăng ⇒ chứng minh $L_{min}=4f=60$ bằng $\Delta\ge0$.
   (c) Bài ngược: TK HT chưa biết $f$; vật dịch lại gần 5 cm thì ảnh thật dịch 10 cm và cao gấp đôi ảnh cũ ⇒ dùng $|k| = \frac{f}{d-f}$:
   $d_1 - f = 10$, $d_2'-d_1' = \frac{f^2}{10} = 10$ ⇒ $f=10$ cm, $d_1=20$, $d_1'=20$, $d_2=15$, $d_2'=30$. topic: "Công thức thấu kính và số phóng đại".
D5 (cấp 3) **Đo tiêu cự: Bessel và 2f–2f.** Vật–màn cố định $L=125$ cm; hai vị trí TK cách nhau $\ell=75$ cm.
   (a) $f=\frac{125^2-75^2}{500}=20$ cm; vị trí 1: $d=25$, $d'=100$, ảnh 8 cm; vị trí 2: $d=100$, $d'=25$, ảnh 0,5 cm (vật 2 cm);
   $h_1'h_2'=4=h^2$ ⇒ đo được chiều cao vật từ hai ảnh: $h=2$ cm.
   (b) Đưa màn lại gần tới $L=70$ cm: $70<4f=80$ ⇒ không còn vị trí nào cho ảnh rõ. $L$ nhỏ nhất còn ảnh rõ: 80 cm.
   (c) Thực hành 2f–2f: ba lần đo $L_{min}$ = 79,5; 80,6; 80,2 cm ⇒ $\bar L=80{,}10$, $\overline{\Delta L}=0{,}40$ ⇒ $f=20{,}0\pm0{,}1$ cm.
   (d) Vì sao đo $L$ phải cẩn thận hơn đo $\ell$: $L$ thêm 1 cm ⇒ $f=20{,}34$ (đổi +0,34); $\ell$ thêm 1 cm ⇒ $f=19{,}70$ (đổi −0,30).
   topic: "Đặc điểm thấu kính hội tụ, phân kì và tiêu cự".
D6 (cấp 3) **Kính lúp, ngắm chừng, khoảng đặt vật.** Kính ghi 5× ⇒ $f=5$ cm; kính sát mắt.
   (a) Mắt tốt ($OC_c=25$, $C_v$ vô cực): ngắm chừng ở $C_c$ ⇒ $d=\frac{25}{6}\approx4{,}17$ cm, $|k|=6$; ở vô cực ⇒ $d=5$ cm, $G=5$.
   Vật phải đặt trong $4{,}17\le d\le5$ cm (xê dịch ≈ 0,83 cm). Vật 0,4 mm ngắm ở $C_c$ ⇒ ảnh 2,4 mm.
   (b) Người cận $OC_c=12$, $OC_v=50$ cm dùng kính đó: $d$ từ $\frac{60}{17}\approx3{,}53$ đến $\frac{50}{11}\approx4{,}55$ cm (xê dịch ≈ 1,02 cm); ở $C_c$: $|k|=3{,}4$.
   topic: "Công thức thấu kính và số phóng đại" (KHÔNG có YCCĐ kính lúp — xem mục cuối).
D7 (cấp 4) **Hệ hai thấu kính đồng trục.** TK1 HT $f_1=20$, vật cao 2 cm, $d_1=30$ ⇒ $d_1'=60$, ảnh trung gian thật, ngược chiều, cao 4 cm.
   (a) TK2 PK $f_2=-20$ cách TK1 $a=80$: $d_2=20$ ⇒ $d_2'=-10$ — ảnh cuối ảo, giữa hai TK, cách TK2 10 cm (cách TK1 70 cm), cao 2 cm, ngược chiều vật.
   (b) Đẩy TK2 sát TK1: $\frac1f = \frac1{20}-\frac1{20}=0$ ⇒ hệ như tấm kính phẳng, ảnh trùng vật (ảo, cùng chiều, bằng vật). Kiểm (đọc thêm, vật ảo): $d_2=-60$ ⇒ $d_2'=-30$.
   (c) Thay TK2 bằng HT $f_2=20$; tìm $a$ để ảnh cuối thật, cao gấp đôi vật: $\frac{20}{d_2-20}=1$ ⇒ $d_2=40$, $a=100$ cm, $d_2'=40$, ảnh cuối cùng chiều vật (2 lần đảo).
   topic: "Công thức thấu kính và số phóng đại".

## Tự luận (tu_luan) — 8 bài dễ → khó, mỗi bài có Hướng dẫn giải trong <details>. Số liệu đã tính (tinh.py), KHÁC BTM và KHÁC docx.
TL1. HT $f=6$, vật 1 cm, $d=9$: dựng trên giấy ô ly (1 ô = 1 cm) + tính ⇒ $d'=18$, $h'=2$ cm, ảnh thật, ngược chiều, cách vật 27 cm.
TL2. PK $f=-10$, vật 5 cm, $d=40$ ⇒ $d'=-8$, $h'=1$ cm, cách vật 32 cm.
TL3. Kính lúp $f=4$ cm: $G=6{,}25$; mắt tốt, kính sát mắt: đặt vật trong $\frac{100}{29}\approx3{,}45\le d\le4$ cm; vật 0,5 mm ngắm ở $C_c$ ⇒ ảnh ≈ 3,63 mm.
TL4. Chứng minh (chữ, không số): vật thật qua PK luôn cho ảnh ảo, cùng chiều, nhỏ hơn vật, trong khoảng $OF'$: $|d'|=\frac{d|f|}{d+|f|}\lt|f|$, $\lt d$; $|k|=\frac{|f|}{d+|f|}\lt1$.
TL5. Điểm sáng $S$ trên trục chính HT $f=10$, $SO=25$: dựng ảnh bằng tia bất kì + trục phụ, rồi tính $d'=\frac{50}{3}\approx16{,}67$ cm (ảnh thật).
TL6. HT $f=18$, cần ảnh thật trên màn cách vật $L=81$ cm: $d^2-81d+1458=0$, $\Delta=729$ ⇒ $d=27$ hoặc $54$; giải thích vì sao với $L\lt72$ không làm được.
TL7. Bessel ngược: vật–màn 72 cm, hai vị trí TK cho hai ảnh rõ cao 9 cm và 1 cm ⇒ $h=3$ cm, $d=18$, $d'=54$, $f=13{,}5$ cm, $\ell=36$ (kiểm bằng công thức Bessel).
TL8. Hệ HT–HT: $f_1=10$, $f_2=15$, $a=40$, vật 1 cm, $d_1=15$ ⇒ $d_1'=30$, $d_2=10\lt f_2$ ⇒ $d_2'=-30$: ảnh cuối ảo, cách TK2 30 cm về phía TK1
   (tức cách TK1 10 cm, nằm giữa vật và TK1), ngược chiều vật, cao 6 cm.

## Luyện tập (8 câu, tự chấm, nhãn như đề thật): 4 Phần I (A–D), 2 Phần II (a)–d) Đúng/Sai), 2 Phần III (đáp số).
I.1 Che nửa trên TK hội tụ đang cho ảnh rõ trên màn ⇒ ảnh: A. mất nửa trên; B. mất nửa dưới; **C. vẫn đủ, tối hơn**; D. biến mất. (topic 87)
I.2 HT $f=15$, $d=10$ ⇒ ảnh: **A. ảo, cùng chiều, cách TK 30 cm**; B. thật, ngược chiều, cách TK 30 cm; C. ảo, cùng chiều, cách TK 6 cm; D. thật, ngược chiều, cách TK 6 cm. (88)
I.3 Vật và màn cách nhau 72 cm; tiêu cự LỚN NHẤT của TK hội tụ còn cho ảnh rõ trên màn: A. 12 cm; **B. 18 cm**; C. 24 cm; D. 36 cm. (88)
I.4 Kính lúp ghi 2,5×, mắt tốt ngắm chừng ở vô cực ⇒ đặt vật cách kính: A. 2,5 cm; B. 5 cm; **C. 10 cm**; D. 25 cm. (86)
II.1 PK $f=-20$, vật 5 cm, $d=30$ ($d'=-12$, $h'=2$; $d=60$ ⇒ $d'=-15$): a) ảnh ảo, cùng chiều (**Đ**); b) ảnh cách TK 12 cm (**Đ**);
   c) ảnh cao 2,5 cm (**S**, 2 cm); d) dịch vật ra xa TK thì ảnh dịch lại gần TK (**S**, ra xa, tiến về $F'$). (88)
II.2 Vật–màn $L=100$ cm, HT $f=21$ cm ($\ell=40$; $d=30$ hoặc $70$; $4f=84$): a) có hai vị trí TK cho ảnh rõ (**Đ**); b) hai vị trí cách nhau 40 cm (**Đ**);
   c) ở vị trí gần vật, ảnh nhỏ hơn vật (**S**, lớn hơn ≈ 2,33 lần); d) đưa màn lại gần còn $L=80$ cm vẫn có ảnh rõ (**S**, $80\lt84$). (86)
III.1 HT $f=20$, $d=25$: khoảng cách vật–ảnh (cm)? Đáp số **125** ($d'=100$). (88)
III.2 Hai TK hội tụ $f_1=30$, $f_2=20$ ghép sát, vật cách hệ 18 cm: ảnh cách hệ bao nhiêu cm? Đáp số **36** ($f=12$). (88)

## YCCĐ cho "Làm bài tương tự"
KHTN 9 bài 86 "Thấu kính" (question-topics, lesson_id 86): **"Đặc điểm thấu kính hội tụ, phân kì và tiêu cự" (86)**, **"Dựng ảnh của vật qua thấu kính" (87)**,
**"Công thức thấu kính và số phóng đại" (88)**. Không có YCCĐ riêng cho kính lúp và đo tiêu cự — D5 gán 86, D6 gán 88 (tạm, xem điểm cần thầy quyết).
Lưu ý: ngân hàng câu của 88 có thể dùng quy ước SBT ($\frac1f=\frac1d-\frac1{d'}$ cho ảnh ảo) — bài tương tự hiện ra có thể khác quy ước.

## Sai sót docx (đã sửa trong dàn ý này, không chép lỗi)
1. Dạng 7 ví dụ mẫu phần b: "thấu kính thứ nhất **vẫn** là $f_1 = 15$ cm" nhưng phần a là $f_1 = 30$ cm — chữ "vẫn" sai. Bộ số phần b
   ($f_1=15$, $f_2=20$, $a=60$, $d_1=30$) còn lặp y hệt ở E11 và G4a (ba lần một bài).
2. B2.7 (sai số Bessel) dùng đạo hàm riêng $\partial f/\partial\ell$, trái với chính mục A2 ("không dùng đạo hàm"). Thay bằng so sánh số: đổi $L$ hoặc $\ell$ thêm 1 cm (D5d).
3. B1.9 nói $G = 25/f$ ứng với "ngắm chừng ở vô cực", Dạng 8 lại nói "ngắm chừng ở điểm cực viễn" — chỉ trùng nhau với mắt tốt. Thống nhất: mắt tốt, ngắm chừng ở vô cực.
4. B1.1 "nhận dạng nhanh: thấy chữ cùng chiều, lớn hơn ⇒ hội tụ" thiếu điều kiện: phải đặt kính **sát** dòng chữ (trong khoảng tiêu cự); để xa thì HT cho ảnh lộn ngược.
5. B2.6 và Dạng 7 viết $d_2 = a - d_1'$ "khi ảnh trung gian là ảnh thật" — công thức đúng cả với ảnh trung gian ảo ($d_1'<0$ ⇒ $d_2 = a+|d_1'|$); hạn chế không cần thiết (TL8 không cần, nhưng HSG hay gặp).
6. Tỉ số chiều cao hệ hai TK viết bằng giá trị tuyệt đối nên không cho chiều; docx bù bằng "đếm số lần đảo chiều" — giữ cách đó, ghi rõ ở quy ước.
(Đã kiểm bằng tinh.py: đáp án E1–E12, G1–G4, H3–H9 và các ví dụ mục C của docx đúng số; H1, H2, H6, H7, H10 là câu định tính, đúng.)

## Điểm cần thầy quyết
- Kính lúp và đo tiêu cự chưa có YCCĐ riêng trong question_topics (chỉ 86/87/88). Có thêm topic con (ví dụ "Kính lúp và số bội giác", "Đo tiêu cự thấu kính hội tụ") không — cần migration.
- D6b (người cận dùng kính lúp) và D7b (vật ảo khi ghép sát) hơi vượt khung lớp 9; giữ làm ý ⭐⭐⭐ hay bỏ.
