# CĐ17. Thiên văn: Mặt Trăng, Hệ Mặt Trời và Ngân Hà (bài 178, khoá Vật lí HSG & chuyên KHTN 9) — dàn ý chung

Nguồn: KHÔNG có docx riêng. Khung lấy từ phần "Trái Đất – bầu trời" trong `../cd14-guong-phang-bong-toi/nguon.txt`
(mục B.6–B.9, Dạng 7, Bài 11, Bài 4 tổng hợp) + đề cương THI HSG 9 KHTN 26-27, phần chung "Trái Đất và bầu trời"
(CHỈ phần Vật lí – thiên văn, không soạn Hoá–Sinh). Viết lại bằng lời mình; mọi số liệu tự đặt, tính ở `tinh.py`.
Phạm vi: YCCĐ KHTN 6 (Mặt Trời mọc–lặn, ngày–đêm, pha Mặt Trăng, Hệ Mặt Trời, Ngân Hà) là nền; phần định lượng
(bóng Mặt Trăng, góc trông, góc cao Mặt Trời, Eratosthenes, tháng giao hội, năm ánh sáng) là mở rộng HSG/chuyên — đề luôn cho số liệu.

**Ranh giới với CĐ14 (bài 158, Gương phẳng, bóng tối và nửa tối):** CĐ14 đã dạy bóng tối/nửa tối với nguồn rộng và vật chắn
(tia "mép – mép", tam giác đồng dạng, $d_{tối} = D + (d-D)\frac{L}{a}$, vùng tối biến mất khi $L = \frac{aD}{D-d}$, bài bìa tròn
nhỏ → "nhật thực hình khuyên"). CĐ17 DÙNG LẠI kết quả đó, chỉ thay số thiên văn — không dựng lại chứng minh, chỉ nhắc 3 dòng + link bài 158.
Không dùng định luật Kepler III (ngoài phạm vi; đề cho chu kì thì lập tỉ số).
Tuần dùng (`tuan.json`): buổi 13 (gửi 26/12) thứ Sáu đọc phần nhật thực, nguyệt thực, pha Mặt Trăng ⇒ mục II–III và dạng D1–D3
ĐỨNG ĐẦU bài; buổi 16 (gửi 16/01) thứ Sáu đọc "phần còn lại" (mục IV–VII, dạng D4–D6).

## Quy ước số liệu & ký hiệu (mọi file dùng chung — lý thuyết, bài tập mẫu, luyện tập dùng y như vậy)
- Tốc độ ánh sáng $c = 3\cdot10^5$ km/s. Đơn vị thiên văn 1 AU $= 1{,}5\cdot10^8$ km (khoảng cách trung bình Trái Đất – Mặt Trời).
- 1 năm $= 365{,}25$ ngày; 1 năm ánh sáng (ly) $\approx 9{,}46\cdot10^{12}$ km $\approx 63\,000$ AU.
- Đường kính: Mặt Trời $D_S = 1{,}39\cdot10^6$ km; Trái Đất $D_E = 12\,740$ km ($R_E = 6370$ km); Mặt Trăng $D_M = 3470$ km.
- Trái Đất – Mặt Trăng (tâm–tâm): trung bình $d_M = 384\,000$ km; gần nhất $363\,000$ km; xa nhất $405\,000$ km.
- Tháng thiên văn (so với sao) $T = 27{,}32$ ngày (đề dễ: 27,3); tháng giao hội = Tuần Trăng $S = 29{,}53$ ngày (đề dễ: 29,5 — giữ như CĐ14).
- Trục Trái Đất nghiêng $23{,}5°$; xích vĩ Mặt Trời $\delta$: xuân phân/thu phân $0°$, hạ chí (~21/6) $+23{,}5°$, đông chí (~22/12) $-23{,}5°$.
- Vĩ độ: Hà Nội $21{,}0°$B, Huế $16{,}5°$B, TP.HCM $10{,}8°$B.
- Ngân Hà: đường kính ~100 000 ly, đĩa dày ~1000 ly, 100–400 tỉ sao; Mặt Trời cách tâm ~26 000 ly, một vòng ~230 triệu năm.
- Sao gần nhất (Proxima Centauri) 4,24 ly. Khoảng cách hành tinh tới Mặt Trời: Hoả 1,52; Mộc 5,2; Thổ 9,5; Hải Vương 30 AU.
- Ký hiệu: góc trông $\alpha$ (rad, $\alpha \approx D/d$ khi nhỏ; đổi ra độ nhân $180/\pi$); góc cao Mặt Trời buổi trưa $h$; vĩ độ $\varphi$;
  chiều dài nón bóng tối $L$; khoảng cách Mặt Trời – Mặt Trăng $a$. Kết quả làm tròn 2–3 chữ số có nghĩa.
- Công thức góc cao buổi trưa: $h = 90° - |\varphi - \delta|$ (bóng ngả về Bắc khi $\delta \lt \varphi$, về Nam khi $\delta \gt \varphi$).

## Lý thuyết (theory.src.html) — 7 mục, ~20 phút (mục I–III đọc buổi 13; IV–VII buổi 16)
I. Mở bài: đêm 7 rạng 8/9/2025 cả nước thấy "trăng máu" (nguyệt thực toàn phần), nhưng nhật thực toàn phần thì nhiều người cả đời
   chưa thấy. Câu dự đoán: (1) nguyệt thực xảy ra vào đêm trăng gì? (2) Đĩa Mặt Trời to gấp ~400 lần đĩa Mặt Trăng; nhìn từ Trái Đất,
   cái nào trông to hơn? (3) Nếu tháng nào cũng có trăng non, sao không tháng nào cũng có nhật thực?
II. Pha Mặt Trăng: Mặt Trăng phản xạ ánh sáng Mặt Trời, luôn có nửa được chiếu sáng; phần ta thấy tuỳ góc Mặt Trời – Trái Đất – Mặt Trăng.
   8 pha (không trăng → lưỡi liềm đầu tháng → thượng huyền → trăng khuyết (gần tròn) → tròn → … → hạ huyền → không trăng).
   Giờ mọc theo pha: không trăng mọc cùng Mặt Trời (~6 h), thượng huyền ~12 h (đầu hôm cao trên trời phía Nam, sáng nửa phía Tây),
   tròn ~18 h, hạ huyền ~0 h; mỗi ngày trăng mọc trễ ~49 phút (= 24 h / 29,5).
   Tháng thiên văn 27,32 ngày vs tháng giao hội 29,53 ngày: trong một vòng của Mặt Trăng, Trái Đất đã đi thêm ~27° quanh Mặt Trời,
   Mặt Trăng phải đi thêm ~2,2 ngày mới về lại pha cũ; $\frac1S = \frac1T - \frac1{365{,}25}$ (hiệu tốc độ góc — giống bài hai kim đồng hồ đuổi nhau).
III. Nhật thực, nguyệt thực (trọng tâm buổi 13):
   - Điều kiện: nhật thực — thứ tự Mặt Trời – Mặt Trăng – Trái Đất, chỉ vào ngày không trăng, thấy ban ngày, dải hẹp; nguyệt thực — Mặt Trời –
     Trái Đất – Mặt Trăng, chỉ đêm trăng tròn, cả nửa Trái Đất đang đêm thấy được.
   - Vì sao không tháng nào cũng có: quỹ đạo Mặt Trăng nghiêng ~5° so với mặt phẳng quỹ đạo Trái Đất; chỉ khi trăng non/tròn rơi gần giao
     tuyến hai mặt phẳng (hai "mùa thực" mỗi năm, cách nhau ~6 tháng) mới thẳng hàng; mỗi năm 4–7 lần thực tổng cộng.
   - Hình học bóng (dùng lại CĐ14, chỉ thay số): góc trông Mặt Trời $\approx 0{,}53°$, Mặt Trăng $0{,}49°$–$0{,}55°$ (tuỳ gần/xa) — trùng hợp gần bằng
     nhau ⇒ nón bóng tối Mặt Trăng dài $L \approx 374\,000$ km, xấp xỉ khoảng cách tới mặt đất. Mặt Trăng ở gần: chóp nón chạm đất → toàn phần
     (vùng tối rộng ~160 km); ở xa: chóp nón không chạm → hình khuyên; nơi trong nửa tối (rộng ~7000 km) → một phần.
   - Nguyệt thực: nón bóng tối Trái Đất dài ~1,39 triệu km (≈ 3,6 lần $d_M$); tại quỹ đạo Mặt Trăng vùng tối rộng ~9200 km ≈ 2,7 $D_M$
     ⇒ Mặt Trăng nằm gọn trong bóng, toàn phần kéo dài tới ~1,7 h. Màu đỏ: ánh sáng đỏ khúc xạ qua khí quyển Trái Đất lọt vào vùng tối (nối CĐ06).
   - An toàn: không nhìn Mặt Trời bằng mắt thường/kính râm; dùng kính lọc chuẩn hoặc chiếu ảnh qua lỗ nhỏ (buồng tối — CĐ14).
IV. Chuyển động nhìn thấy của Mặt Trời, ngày–đêm: Trái Đất tự quay Tây → Đông, 24 h/vòng (15°/h) ⇒ Mặt Trời "đi" Đông → Tây;
   nửa được chiếu sáng là ngày. Giờ địa phương theo kinh độ (chênh $\Delta\lambda/15$ giờ, phía Đông sớm hơn) và múi giờ (VN +7) — nhắc ngắn.
   Mở rộng: ngày sao 23 h 56 min vs ngày Mặt Trời 24 h (cùng ý tưởng tháng thiên văn/giao hội). Tốc độ tự quay ở xích đạo ~463 m/s.
V. Mùa và góc cao Mặt Trời: trục nghiêng 23,5° giữ hướng cố định khi quay quanh Mặt Trời ⇒ góc chiếu và độ dài ngày đổi theo năm
   (mùa KHÔNG do gần/xa Mặt Trời: Trái Đất gần Mặt Trời nhất đầu tháng 1). $h = 90° - |\varphi - \delta|$; vùng giữa hai chí tuyến
   có hai ngày Mặt Trời đứng bóng; vòng cực 66,5° có ngày/đêm 24 h. Độ dài ngày hạ chí: Hà Nội ~13,3 h, TP.HCM ~12,6 h (chỉ định tính,
   không bắt tính). Eratosthenes: cùng trưa, cùng kinh tuyến, hai nơi lệch góc tia nắng $\theta$ cách nhau cung $s$ ⇒ chu vi $= s\cdot\frac{360°}{\theta}$.
VI. Hệ Mặt Trời: Mặt Trời (sao, tự phát sáng) + 8 hành tinh (4 đất đá gần, 4 khí/băng khổng lồ xa) + hành tinh lùn, tiểu hành tinh, sao chổi, vệ tinh;
   càng xa chu kì càng dài. Đơn vị AU; ánh sáng Mặt Trời tới Trái Đất ~8,3 phút, tới Hải Vương ~4,2 h. Tốc độ quỹ đạo Trái Đất ~30 km/s.
   Mô hình tỉ lệ 1 : $10^{10}$: Mặt Trời quả bóng 14 cm, Trái Đất hạt 1,3 mm cách 15 m, Hải Vương cách 450 m, sao gần nhất cách ~4000 km.
VII. Ngân Hà và Trả bài: Ngân Hà là thiên hà xoắn ốc có thanh chắn, đĩa ~100 000 ly, Mặt Trời ở một nhánh xoắn cách tâm ~26 000 ly (không ở tâm);
   dải sáng mờ trên trời đêm là đĩa nhìn từ bên trong. Mặt Trời quay quanh tâm ~213 km/s, ~230 triệu năm/vòng. Năm ánh sáng là đơn vị
   KHOẢNG CÁCH. Trả bài 6 câu tự trả lời.

Bẫy: "năm ánh sáng là đơn vị thời gian"; mùa do Trái Đất gần/xa Mặt Trời; pha Mặt Trăng do bóng Trái Đất che (nhầm với nguyệt thực);
nhật thực xảy ra ngày trăng tròn; tháng nào cũng có thực; quên trừ $R_E$ khi tính khoảng cách Mặt Trăng → mặt đất; dùng góc trông ở độ
mà quên đổi rad (hoặc ngược lại); góc cao trưa lấy $\varphi + \delta$ thay vì $|\varphi - \delta|$, quên đổi hướng bóng khi $\delta \gt \varphi$;
tưởng Mặt Trời ở tâm Ngân Hà; Mặt Trăng "không tự quay" (thật ra tự quay một vòng đúng bằng một vòng quanh Trái Đất nên luôn quay một mặt về ta).

## Bài tập mẫu (scripts/data/bai-tap-mau/178.json) — 6 dạng, cấp không giảm. SỐ LIỆU ĐÃ TÍNH (tinh.py), dùng nguyên.
D1 (cấp 1) **Pha Mặt Trăng và lịch thực.** Ngày 3/3 là trăng tròn (rằm), có nguyệt thực; lấy $S = 29{,}5$ ngày.
   (a) Hạ huyền sau $S/4 \approx 7{,}4$ ngày → ~10/3; không trăng sau $14{,}75$ ngày → ~17–18/3 (nhật thực, nếu có, chỉ có thể vào đây);
   trăng tròn kế ~1–2/4. (b) Thượng huyền mọc lúc nào, thấy ở đâu lúc 18 h: mọc ~12 h, lúc 18 h ở cao phía Nam, sáng nửa phía Tây.
   (c) Vì sao 1–2/4 thường KHÔNG có nguyệt thực nữa (5°, mùa thực cách ~6 tháng). Hình SVG quỹ đạo 8 vị trí, không tô sẵn đáp án.
D2 (cấp 2) **Góc trông: toàn phần hay hình khuyên.** Góc trông Mặt Trời $\alpha_S = D_S/\text{AU} \approx 0{,}531°$.
   Mặt Trăng nhìn từ điểm mặt đất ngay dưới nó (khoảng cách $d - R_E$): gần nhất $0{,}557°$ (> ⇒ toàn phần), trung bình $0{,}526°$,
   xa nhất $0{,}499°$ (< ⇒ hình khuyên, che tối đa $(0{,}499/0{,}531)^2 \approx 88$ % diện tích đĩa). Khoảng cách tối đa để che vừa:
   $D_M\cdot\text{AU}/D_S \approx 374\,000$ km. Mở đầu bằng thí nghiệm đồng xu 2 cm che vừa Mặt Trời khi cách mắt ≈ 2,2 m.
D3 (cấp 3) **Nón bóng Mặt Trăng và Trái Đất** (dùng công thức CĐ14, $a = \text{AU} - d$). (a) Nón bóng tối Mặt Trăng $L = \frac{aD_M}{D_S - D_M} \approx 374\,500$ km.
   (b) Mặt Trăng ở gần nhất (363 000 km): khoảng tới mặt đất $356\,630$ km < L ⇒ toàn phần, vùng tối $D_M\frac{L-x}{L} \approx 165$ km,
   vùng nửa tối $\approx 6800$ km. (c) Mặt Trăng xa nhất (405 000 km): $398\,630 \gt L$ ⇒ hình khuyên (vùng hình khuyên ≈ 225 km).
   (d) Nguyệt thực: nón bóng tối Trái Đất $\approx 1{,}39\cdot10^6$ km; tại $d_M$ vùng tối rộng $\approx 9200$ km ≈ 2,66 $D_M$ (nửa tối ≈ 16 300 km).
D4 (cấp 3) **Tháng giao hội từ tháng thiên văn.** $\omega_M = 360/27{,}32 = 13{,}18°$/ngày, $\omega_E = 360/365{,}25 = 0{,}986°$/ngày;
   hiệu $12{,}19°$/ngày ⇒ $S = 29{,}53$ ngày; sau 27,32 ngày Trái Đất đã đi $26{,}9°$, cần thêm $2{,}21$ ngày. Biến thể (cùng phương pháp):
   ngày sao $= 23$ h 56 min 4 s. Kèm (thuộc nhật/nguyệt thực): thời gian toàn phần dài nhất của nguyệt thực — tốc độ Mặt Trăng so với
   bóng Trái Đất $2\pi d_M/S \approx 0{,}946$ km/s ⇒ $(9214 - 3470)/0{,}946 \approx 101$ phút ≈ 1,7 h; từ lúc chạm tới lúc rời hẳn vùng tối ≈ 3,7 h.
   (Lý do dùng $S$ chứ không phải $T$: bóng đi theo Trái Đất.)
D5 (cấp 3) **Góc cao Mặt Trời buổi trưa và Eratosthenes.** (a) Hà Nội: xuân phân $69{,}0°$, hạ chí $87{,}5°$ (bóng về Nam), đông chí $45{,}5°$;
   TP.HCM: $79{,}2°$ / $77{,}3°$ (bóng về Nam) / $55{,}7°$. Bóng cọc 1 m: Hà Nội đông chí 0,98 m; TP.HCM hạ chí 0,23 m về Nam.
   (b) Eratosthenes: trưa xuân phân… (số tự đặt) A không có bóng, ở B cùng kinh tuyến cách 556 km cọc 1 m có bóng 0,0875 m ⇒ $\theta = 5{,}00°$
   ⇒ chu vi ≈ 40 000 km, $R \approx 6370$ km. Hình SVG: hai tia song song, góc ở tâm = góc lệch tia nắng (góc so le trong).
D6 (cấp 4) **Hệ Mặt Trời – Ngân Hà theo tỉ lệ (tổng hợp nhiều bước).** (a) Ánh sáng Mặt Trời → Trái Đất 500 s ≈ 8,3 min; → Hải Vương (30 AU) 4,17 h;
   tín hiệu điều khiển xe tự hành Sao Hoả mất 4,3–21 min một chiều (0,52–2,52 AU) ⇒ vì sao không lái trực tiếp. (b) Tốc độ quỹ đạo Trái Đất
   $2\pi\,\text{AU}/(365{,}25\cdot86\,400) \approx 29{,}9$ km/s (≈ 2,58 triệu km/ngày). (c) Proxima 4,24 ly ≈ $4{,}0\cdot10^{13}$ km ≈ 268 000 AU;
   tàu 17 km/s mất ≈ 75 000 năm. (d) Mặt Trời quanh tâm Ngân Hà: $2\pi\cdot26\,000$ ly / 230 triệu năm ≈ 213 km/s; 4,6 tỉ năm ≈ 20 vòng.
   (e) Mô hình 1 : $10^{10}$ (số ở mục VI). topic: xem mục YCCĐ.

## Tự luận (tu_luan) — 8 bài dễ → khó, mỗi bài có Hướng dẫn giải trong <details>. Số liệu KHÁC bài tập mẫu (tính thêm trong tinh.py khi soạn).
1. Lịch pha từ một ngày không trăng cho trước + giờ mọc trăng mỗi pha (mọc trễ ~49 min/ngày).
2. Giờ địa phương và múi giờ (chuyến bay qua nhiều múi; nối lại phần CĐ14 chưa dạy — xem "Cần thầy quyết").
3. Bóng cọc buổi trưa ở Huế ba ngày đặc biệt ($73{,}5°$ / $83{,}0°$ về Nam / $50{,}0°$; bóng 1 m: 0,30 / 0,12 / 0,84 m); tìm vĩ độ từ bóng đo được.
4. Eratosthenes lịch sử: $7{,}2°$, 5000 stadia (giả thiết 1 stadion = 157,5 m) ⇒ 787,5 km, chu vi ≈ 39 400 km, $R \approx 6270$ km; bàn sai số.
5. Nhật thực hình khuyên: tỉ lệ diện tích đĩa Mặt Trời bị che theo khoảng cách Mặt Trăng; vì sao ở khoảng cách trung bình vẫn là hình khuyên (vùng ~30 km).
6. Mô hình tỉ lệ Hệ Mặt Trời trên sân trường (chọn tỉ lệ, đặt hành tinh, kết luận "Hệ Mặt Trời gần như trống rỗng").
7. Ngày sao và ngày Mặt Trời; giải thích vì sao một ngôi sao mọc sớm ~4 phút mỗi đêm.
8. (HSG) Phương pháp Aristarchus: biết vùng tối Trái Đất tại quỹ đạo Mặt Trăng rộng ≈ 2,6 lần Mặt Trăng và góc trông Mặt Trăng ≈ Mặt Trời
   ⇒ $D_M \approx D_E/(1 + 2{,}6) \approx 3540$ km (thật 3470); góc trông $0{,}52°$ ⇒ $d \approx 390\,000$ km.

## Luyện tập (≥8 câu, tự chấm, nhãn như đề thật): 4 câu Phần I (A–D), 2 câu Phần II (a)–d) Đúng/Sai), 2 câu Phần III (đáp số).
Phần I: (1) nhật thực chỉ có thể xảy ra vào pha nào; (2) nguyên nhân không tháng nào cũng có thực (5°) — nhiễu: Trái Đất quay quanh trục,
  quỹ đạo elip, Mặt Trăng tự quay; (3) góc cao Mặt Trời trưa đông chí ở Hà Nội ≈ $45{,}5°$ (nhiễu 69°, 44,5°, 66,5°);
  (4) vị trí Hệ Mặt Trời trong Ngân Hà / năm ánh sáng đo đại lượng gì.
Phần II: (5) bốn mệnh đề về nhật thực toàn phần/hình khuyên/nửa tối/khi Mặt Trăng xa nhất; (6) bốn mệnh đề về mùa (trục nghiêng,
  gần–xa Mặt Trời, hạ chí ở TP.HCM bóng về Nam, xích đạo ngày ≈ đêm quanh năm).
Phần III: (7) thời gian ánh sáng Mặt Trời → Trái Đất (phút, 1 chữ số thập phân): **8,3**; (8) tháng thiên văn 27,3 ngày, năm 365 ngày,
  tháng giao hội (ngày, 1 chữ số thập phân): **29,5**.
Câu dự phòng: góc cao trưa hạ chí TP.HCM **77,3°**; chiều dài nón bóng tối Mặt Trăng (nghìn km) **374**.

## YCCĐ cho "Làm bài tương tự"
không có — ngân hàng câu hỏi (`scripts/data/question-topics.json`) không có chủ đề Trái Đất – bầu trời/thiên văn
(chỉ có "Vòng năng lượng trên Trái Đất", không khớp). Để trống topic; nếu thầy muốn thì tạo chủ đề KHTN 6 "Trái Đất và bầu trời" sau.

## Sai sót / lưu ý từ nguồn CĐ14
- Không phát hiện sai số liệu. Đã kiểm lại độ dài ngày hạ chí trong CĐ14 (TP.HCM chênh ~1,3 h, Hà Nội ~2,6 h): khớp tinh.py (1,27 h; 2,56 h).
- CĐ14 lấy Tuần Trăng = 29,5 ngày; CĐ17 giữ 29,5 cho đề dễ, dùng 29,53 khi tính tháng giao hội — ghi rõ trong từng đề.
