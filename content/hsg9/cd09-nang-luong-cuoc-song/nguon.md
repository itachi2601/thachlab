# CĐ09. Năng lượng với cuộc sống: vòng năng lượng Trái Đất, nhiên liệu và năng lượng tái tạo (bài 163, khoá Vật lí HSG & chuyên KHTN 9) — dàn ý chung

Nguồn: docx `09` (đã trích ở `nguon.txt` cùng thư mục — mục A, B, C, H/I dùng làm khung; ví dụ C/D/E/G trong docx KHÔNG chép,
số liệu dưới đây là số mới tự đặt, tính bằng `tinh.py` cùng thư mục: `python3 tinh.py`). Viết lại bằng lời mình.
Bám SGK KHTN 9 Chương V (Bài 16 Vòng năng lượng trên Trái Đất. Năng lượng hoá thạch; Bài 17 Một số dạng năng lượng tái tạo)
+ mở rộng định lượng cho HSG. **Chỉ phần Vật lí**: không viết phương trình hoá học đốt cháy (docx có CH₄ + 2O₂…, bỏ), không soạn
chu trình carbon kiểu Sinh học, không mưa acid ở mức hoá học (chỉ nêu tên tác hại một dòng).

**Ranh giới:**
- Nhiệt lượng nhiên liệu đun nước + hiệu suất bếp (Dạng 7 docx, bài D3/D6/E6/E10/E11) đã ở **CĐ12 (bài 153, D4)** — CĐ09 KHÔNG làm
  dạng "đun m kg nước từ t₁ lên t₂ bằng bếp…". Nhiên liệu ở CĐ09 chỉ dùng để **phát điện / chạy máy** ($Q = qm$ rồi nhân chuỗi $H$).
- Hao phí truyền tải điện năng ($P_{hp} = P^2R/U^2$), máy biến áp thuộc **CĐ08 (bài 152)** — mọi đề CĐ09 ghi "bỏ qua hao phí trên đường dây".
- Tiền điện = $A$(kWh) × đơn giá, đọc công tơ thuộc **CĐ05 (bài 165)** — CĐ09 chỉ dùng tiền để so sánh phương án, đơn giá cho sẵn
  một con số; KHÔNG dạy biểu giá bậc thang (docx Bảng 5, D2, G2 — số liệu thật đang thay đổi, xem "Sai sót docx").
- Công, công suất cơ học $A = Fs$, $P = A/t$ ở **CĐ01**; thế năng $mgh$ ở **CĐ02** — CĐ09 dùng lại, không dạy lại.
- Phản ứng hạt nhân chỉ ở mức định tính (phân hạch/nhiệt hạch là gì, chuỗi năng lượng nhà máy điện hạt nhân); số "1 g U-235 toả
  $8{,}2\cdot10^{10}$ J" luôn cho sẵn trong đề, không tính từ độ hụt khối.

Tuần dùng: buổi 16 — thứ Tư "Đọc lý thuyết CĐ09 Năng lượng; làm quiz (40 phút)"; BTVN "Hoàn thành quiz CĐ15, CĐ09" (`tuan.json`).
Vì vậy phần **Luyện tập là trọng tâm** (quiz 40 phút), bài tập mẫu để tự đọc.

## Quy ước số liệu & ký hiệu (mọi file dùng chung)
- $g = 10$ m/s²; khối lượng riêng nước $D = 1000$ kg/m³, trọng lượng riêng $d = 10D = 10\,000$ N/m³ (ký hiệu KHTN 9: $D$, $d$ — KHÔNG dùng $\rho$).
  Không khí $D_{kk} = 1{,}2$ kg/m³. 1 kWh $= 3{,}6\cdot10^6$ J. 1 ngày $= 86\,400$ s.
- Hiệu suất $H = \dfrac{A_{ích}}{A_{tp}}$ (hoặc $\dfrac{P_{ích}}{P_{tp}}$); chuỗi nhiều cấp $H = H_1H_2H_3\dots$; $A_{hp} = A_{tp} - A_{ích} = (1-H)A_{tp}$.
- **Lưu lượng nước ký hiệu $L$ (m³/s)** — KHÔNG dùng $Q$ (docx dùng $Q$, trùng nhiệt lượng). Độ cao cột nước $h$ (m).
  Công suất dòng nước $P_n = d\,L\,h = 10D\,L\,h$; công suất điện $P_đ = H P_n$.
- Pin Mặt Trời: cường độ bức xạ tới $I$ (W/m²), diện tích $S$ (m²), $P_{đỉnh} = H_{pin} I S$; **số giờ nắng đỉnh $t_đ$** (h/ngày, số giờ quy đổi về
  $I = 1000$ W/m²) — sản lượng ngày $A = P_{đỉnh}\,t_đ\,H_{bt}$ với $H_{bt}$ hiệu suất biến tần (nếu đề cho). Mặt đất trời nắng $I \approx 1000$ W/m²;
  rìa khí quyển (hằng số Mặt Trời) $I_0 = 1360$ W/m².
- Gió: $P_{gió} = \tfrac12 D_{kk} S v^3$ (đề CHO SẴN công thức), $S = \pi d_q^2/4$ ($d_q$ đường kính vòng quét); tuabin $P \propto v^3$ khi $v_{kđ} \le v \lt v_{đm}$;
  $P = P_{đm}$ khi $v_{đm} \le v \le v_{ngắt}$; $P = 0$ khi $v \lt v_{kđ}$ hoặc $v \gt v_{ngắt}$. Mặc định $v_{kđ} = 3$ m/s, $v_{ngắt} = 25$ m/s. Giới hạn Betz $16/27 \approx 59{,}3\,\%$.
- Năng suất toả nhiệt $q$ (đề cho): than đá $2{,}7\cdot10^7$, xăng $4{,}6\cdot10^7$, dầu diesel $4{,}4\cdot10^7$ J/kg. Xăng $D = 0{,}70$ kg/L, diesel $0{,}84$ kg/L.
- Phát thải: **hệ số cho sẵn**, ký hiệu $k$ (kg CO₂ trên 1 kg nhiên liệu): than đá $2{,}5$; xăng $3{,}2$; diesel $3{,}2$. Điện lưới $k_e$ (kg CO₂/kWh), mặc định $0{,}65$.
  $m_{CO_2} = k\,m_{nl}$ hoặc $k_e A$. Chỉ tính tỉ lệ khối lượng, không viết phương trình hoá học.
- Hạt nhân: "1 g U-235 phân hạch hết toả khoảng $8{,}2\cdot10^{10}$ J" (đề cho) ≈ năng lượng đốt $3000$ kg than đá.
- Mặc định mọi đề ghi rõ: "bỏ qua hao phí trên đường dây tải điện".

## Lý thuyết (theory.src.html) — 7 mục, ~15–18 phút
I. **Mở bài.** Bóng đèn trong phòng đang sáng — đi ngược dòng năng lượng của nó về tận gốc. Câu dự đoán (chọn trước khi học):
   (1) Nhà máy nhiệt điện đốt than toả 100 J thì tới bóng đèn còn khoảng bao nhiêu J điện: 90 J / 60 J / 35 J? (đáp: ~35 J);
   (2) Trong bốn dạng gió, than đá, thuỷ điện, **thuỷ triều**, dạng nào KHÔNG có gốc từ bức xạ Mặt Trời? (đáp: thuỷ triều).
II. **Bảo toàn và chuyển hoá năng lượng — hiệu suất chuỗi.** Năng lượng không tự sinh ra/mất đi, chỉ chuyển dạng; phần "hao phí" không biến mất mà
   thành nhiệt toả ra môi trường. $H = A_{ích}/A_{tp} \lt 1$. Máy nhiều cấp: $H = H_1H_2H_3$ (sơ đồ dòng năng lượng dạng mũi tên tách nhánh).
   Ví dụ nhanh: lò hơi 90 %, tuabin 42 %, máy phát 96 % ⇒ $H \approx 36\,\%$; hao phí lớn nhất ở khâu nhiệt → cơ (tuabin), không phải máy phát.
   Bẫy: tính $A_{tp} = A_{ích}\cdot H$ (sai, phải chia); cộng hoặc lấy trung bình các hiệu suất thay vì nhân; nghĩ "hao phí = năng lượng mất đi".
III. **Vòng năng lượng trên Trái Đất.** Mặt Trời (năng lượng sinh ra từ nhiệt hạch trong lõi) → bức xạ tới Trái Đất; ~30 % bị phản xạ về vũ trụ, phần
   còn lại hấp thụ → (a) làm nóng không đều → gió → sóng biển; (b) bốc hơi → mây → mưa trên cao → thế năng nước sông (thuỷ điện); (c) quang hợp →
   sinh khối → bị chôn vùi hàng trăm triệu năm → than, dầu, khí (năng lượng Mặt Trời "tích trữ"). Trái Đất bức xạ nhiệt (hồng ngoại) trở lại vũ trụ — cân bằng.
   Số để "cảm" độ lớn: công suất tới $P = I_0\pi R^2 \approx 1{,}75\cdot10^{17}$ W, gấp ~9000 lần công suất loài người dùng (~$2\cdot10^{13}$ W).
   Ba ngoại lệ không từ bức xạ Mặt Trời: **địa nhiệt** (nhiệt lòng đất), **hạt nhân** (urani có sẵn trong vỏ Trái Đất), **thuỷ triều** (lực hấp dẫn của
   Mặt Trăng và Mặt Trời + Trái Đất tự quay).
   Bẫy: dùng diện tích mặt cầu $4\pi R^2$ thay cho hình chiếu $\pi R^2$; gộp thuỷ triều với sóng biển; trả lời "nguồn gốc từ Mặt Trời" mà không viết chuỗi.
IV. **Nhiên liệu hoá thạch và ấm lên toàn cầu.** Than, dầu, khí: không tái tạo (hình thành triệu năm, khai thác hàng ngày). $Q = qm$; mật độ năng lượng cao,
   ổn định, dễ chở — ưu điểm thật (đừng chỉ kể nhược). Đốt thải CO₂ theo hệ số $k$ cho sẵn: $m_{CO_2} = k\,m$. Hiệu ứng nhà kính: ánh sáng Mặt Trời
   (bước sóng ngắn) đi qua khí quyển, bức xạ hồng ngoại Trái Đất phát ra bị CO₂, hơi nước, CH₄ giữ lại một phần. Hiệu ứng tự nhiên là cần thiết
   (không có nó Trái Đất trung bình khoảng −18 °C); con người đốt nhiên liệu làm **tăng cường** hiệu ứng ⇒ ấm lên toàn cầu (băng tan, nước biển dâng,
   thời tiết cực đoan) — chỉ định tính. Giá nhiên liệu phụ thuộc chi phí khai thác, vận chuyển, thuế phí, cung–cầu (một dòng).
   Bẫy: nhầm hiệu ứng nhà kính với thủng tầng ozone; "CO₂ chặn ánh sáng Mặt Trời"; nhầm $q$ (J/kg) với $c$ (J/(kg·K)).
V. **Năng lượng tái tạo — bốn nguồn có công thức.** Tái tạo = được bổ sung liên tục trong tự nhiên.
   (a) Thuỷ điện $P_đ = H\,d\,L\,h$ ($H$ 80–90 %); suy từ trọng lượng nước chảy qua mỗi giây $\times h$. (b) Pin Mặt Trời $P_{đỉnh} = H I S$ (15–22 %), sản lượng
   theo **giờ nắng đỉnh**, số tấm làm tròn LÊN. (c) Gió $P \propto v^3$ (gió ×2 ⇒ công suất ×8), $P_{gió} = \tfrac12 D S v^3$, Betz 59,3 %, vùng làm việc
   khởi động–định mức–ngắt. (d) Sinh khối, sóng biển, địa nhiệt: định tính. Nhược điểm chung: không ổn định ⇒ cần lưu trữ (acquy, **thuỷ điện tích năng**:
   đêm bơm nước lên, ngày xả phát điện), đầu tư lớn, chiếm diện tích.
   Bẫy: $P \propto v^2$ (nhầm động năng); dùng $v^3$ cả khi gió vượt tốc độ định mức; lấy 12 h trời sáng thay giờ nắng đỉnh; quên $D$ khi tính khối lượng nước.
VI. **Năng lượng hạt nhân (định tính).** Phân hạch: hạt nhân nặng (U-235) hấp thụ nơtron, vỡ thành hai hạt nhẹ hơn + vài nơtron, toả năng lượng lớn; phản ứng
   dây chuyền có điều khiển trong lò. Nhà máy điện hạt nhân: năng lượng hạt nhân → nhiệt (hơi nước) → cơ (tuabin) → điện — nửa sau giống hệt nhiệt điện, $H \approx 33\,\%$.
   Nhiệt hạch: hạt nhân nhẹ (hiđrô) kết hợp thành heli ở nhiệt độ hàng chục triệu độ — nguồn năng lượng của Mặt Trời, chưa dùng phát điện thương mại.
   Ưu: không thải CO₂ khi vận hành, 1 g U-235 ≈ 3 tấn than. Nhược: chất thải phóng xạ lâu dài, nguy cơ sự cố, vốn lớn; **không tái tạo** (urani hữu hạn).
   Bẫy: xếp năng lượng hạt nhân vào tái tạo; nghĩ nhà máy hạt nhân "đốt" urani; nhầm phân hạch (nhà máy) với nhiệt hạch (Mặt Trời).
VII. **Trả bài và mang về** (6 câu tự trả lời): viết chuỗi cho gió/thuỷ điện/than; ba ngoại lệ; $H$ chuỗi; vì sao $v^3$ làm điện gió thất thường;
   giờ nắng đỉnh là gì; hiệu ứng nhà kính tự nhiên khác tăng cường thế nào.

Hình SVG gợi ý: sơ đồ vòng năng lượng (Mặt Trời → các nhánh, ba ngoại lệ ô riêng nét đứt); sơ đồ dòng năng lượng nhà máy nhiệt điện (độ rộng mũi tên
tỉ lệ công suất — KHÔNG ghi số kết quả của D1); đồ thị $P(v)$ của tuabin gió có ba vùng (trục chỉ ghi $v_{kđ}$, $v_{đm}$, $v_{ngắt}$).

## Bài tập mẫu (scripts/data/bai-tap-mau/163.json) — 5 dạng, cấp không giảm. SỐ LIỆU ĐÃ TÍNH (`tinh.py`), dùng nguyên.
D1 (cấp 1) **Chuỗi hiệu suất nhà máy nhiệt điện than.** Lò hơi $H_1 = 90\,\%$, tuabin $H_2 = 42\,\%$, máy phát $H_3 = 96\,\%$; công suất điện 330 MW;
   than $q = 2{,}7\cdot10^7$ J/kg, $k = 2{,}5$.
   (a) $H = 0{,}36288 \approx 36{,}3\,\%$. (b) $P_{nl} \approx 909{,}4$ MW; $P_{hp} \approx 579{,}4$ MW; hao phí từng khâu: lò hơi ≈ 90,9 MW, tuabin ≈ 474,7 MW,
   máy phát ≈ 13,75 MW (tổng khớp 579,4). (c) Than ≈ 33,68 kg/s ≈ 121,3 tấn/giờ ≈ 2910 tấn/ngày; CO₂ ≈ 7275 tấn/ngày.
   (d) Nâng tuabin lên 45 % ⇒ $H = 38{,}88\,\%$, than ≈ 2716 tấn/ngày, tiết kiệm ≈ 194 tấn/ngày (≈ 6,7 %). Điện năng 1 ngày: 7920 MWh (dùng lại ở D2, D4).
   topic: "Tính hiệu suất của máy và động cơ" (140); phụ "Ưu nhược điểm của nhiên liệu hoá thạch" (100).
D2 (cấp 2) **Công suất thuỷ điện từ lưu lượng và độ cao.** Mùa mưa $h = 95$ m, $L = 250$ m³/s; tuabin 92 %, máy phát 96 % ⇒ $H = 0{,}8832$.
   (a) $P_n = 237{,}5$ MW; $P_đ \approx 209{,}8$ MW. (b) Mùa khô $h = 80$ m, $L = 160$ m³/s ⇒ $P_đ \approx 113{,}1$ MW (≈ 54 % mùa mưa — cả $h$ lẫn $L$ cùng giảm).
   (c) Giữ 150 MW khi $h = 80$ m cần $L \approx 212{,}3$ m³/s. (d) Một ngày mùa mưa: $A \approx 5034$ MWh, nước qua tuabin $2{,}16\cdot10^7$ m³;
   nếu nhà máy than ở D1 ($H = 36{,}288\,\%$) làm ra lượng điện đó thì đốt ≈ 1850 tấn than, thải ≈ 4624 tấn CO₂.
   topic: "Các dạng năng lượng tái tạo và nguồn gốc" (101).
D3 (cấp 2–3) **Pin Mặt Trời cho một gia đình (số tấm).** Gia đình dùng 375 kWh/tháng (30 ngày) ⇒ 12,5 kWh/ngày. Tấm pin 2,0 m², $H_{pin} = 20\,\%$,
   $I = 1000$ W/m², $t_đ = 4{,}0$ h/ngày, biến tần 95 %.
   (a) $P_{đỉnh}$ mỗi tấm = 400 W; mỗi tấm cho 1,52 kWh/ngày. (b) $n = 8{,}22$ ⇒ **9 tấm** (làm tròn lên), công suất đỉnh hệ 3,6 kW.
   Bẫy: quên biến tần ⇒ 7,81 ⇒ 8 tấm (thiếu); lấy 12 h trời sáng ⇒ 2,74 tấm (vô lí). (c) Mái chỉ đặt được 14 m² ⇒ 7 tấm, 10,64 kWh/ngày, thiếu 1,86 kWh/ngày
   = 55,8 kWh/tháng phải mua lưới. (d) Lắp đủ 9 tấm giá 67,5 triệu đồng, đơn giá điện 2 800 đồng/kWh ⇒ tiết kiệm 1 050 000 đồng/tháng, hoàn vốn ≈ 64,3 tháng ≈ 5,4 năm.
   topic: "Sử dụng năng lượng tiết kiệm, hiệu quả" (102); phụ 101.
D4 (cấp 3) **Điện gió: $v^3$ và vùng làm việc.** Tuabin đường kính vòng quét 80 m, định mức 2,0 MW tại 12 m/s, khởi động 3 m/s, ngắt 25 m/s, $D_{kk} = 1{,}2$ kg/m³
   (đề cho $P_{gió} = \tfrac12 D S v^3$).
   (a) $S \approx 5027$ m², $P_{gió}(12) \approx 5{,}21$ MW ⇒ $H \approx 38{,}4\,\% \lt 59{,}3\,\%$. (b) Gió một ngày: 4 h ở 2 m/s; 8 h ở 6 m/s; 6 h ở 9 m/s; 4 h ở 12 m/s; 2 h ở 15 m/s.
   $P$: 0; 0,25 MW; 0,84375 MW; 2 MW; **2 MW** (vượt định mức, KHÔNG dùng $v^3$ — bẫy cho 3,91 MW). Điện năng: 0 + 2 + 5,0625 + 8 + 4 = **19,06 MWh**;
   hệ số công suất ≈ 39,7 %. (c) Số tuabin để bằng sản lượng ngày của nhà máy D1 (7920 MWh): 415,5 ⇒ **416 tuabin**.
   topic: "Các dạng năng lượng tái tạo và nguồn gốc" (101).
D5 (cấp 4) **So sánh phương án: xe máy xăng và xe máy điện (chuỗi từ nguồn tới bánh xe).** Mỗi ngày đi 40 km, lực cản trung bình 70 N ⇒ $A_{ích} = 2{,}8\cdot10^6$ J.
   Xe xăng: $H = 15\,\%$, $q = 4{,}6\cdot10^7$, $D = 0{,}70$ kg/L, $k = 3{,}2$, giá 24 000 đ/L. Xe điện: động cơ 80 %, sạc 90 % ⇒ $H = 72\,\%$, giá điện 3 000 đ/kWh, $k_e = 0{,}65$.
   (a) Xăng: $Q \approx 1{,}867\cdot10^7$ J, $m \approx 0{,}406$ kg, $V \approx 0{,}58$ L, tiền ≈ 13 900 đ, CO₂ ≈ 1,30 kg. (b) Điện: $A \approx 3{,}89\cdot10^6$ J ≈ 1,08 kWh, tiền ≈ 3 240 đ,
   CO₂ ≈ 0,70 kg. Tiền gấp ≈ 4,3 lần; CO₂ gấp ≈ 1,85 lần. Một năm chênh ≈ 3,9 triệu đồng (5,08 tr so với 1,18 tr).
   (c) Nếu toàn bộ điện do nhà máy than D1 cấp (bỏ qua đường dây): $H_{than→bánh} = 0{,}36288\cdot0{,}72 \approx 26\,\%$ (vẫn hơn 15 % của xe xăng); than ≈ 0,397 kg,
   CO₂ ≈ 0,99 kg — vẫn ít hơn xe xăng nhưng gần hơn; tương đương $k_e \approx 0{,}92$ kg/kWh. Kết luận: xe điện "sạch" bao nhiêu phụ thuộc nguồn điện.
   topic: "Ưu nhược điểm của nhiên liệu hoá thạch" (100); phụ 102.

## Tự luận (tu_luan) — 6 bài dễ → khó, mỗi bài có Hướng dẫn giải trong <details>. Số liệu KHÁC bài tập mẫu và KHÁC docx.
TL1 (định tính) Viết chuỗi biến đổi cho: điện từ tuabin gió, điện từ thuỷ điện, nhiệt từ đốt củi, điện từ nhà máy than; phân loại 8 nguồn (gió, than, thuỷ triều,
   địa nhiệt, sinh khối, dầu mỏ, urani, sóng biển) theo hai tiêu chí "gốc Mặt Trời?" và "tái tạo?". (Thuỷ triều: không gốc Mặt Trời nhưng tái tạo; urani: không/không.)
TL2 Công suất bức xạ tới Trái Đất: $I_0 = 1360$ W/m², $R = 6400$ km ⇒ $P \approx 1{,}75\cdot10^{17}$ W; so với $2{,}0\cdot10^{13}$ W ⇒ ≈ 8750 lần; năng lượng loài người dùng
   một năm Mặt Trời gửi tới trong ≈ 3604 s ≈ 60 phút. Bẫy $4\pi R^2$ ⇒ $7{,}0\cdot10^{17}$ W. Mở rộng: 30 % phản xạ, trung bình mỗi m² bề mặt hấp thụ $0{,}7\cdot1360/4 = 238$ W/m².
TL3 Trường thay 120 đèn 40 W bằng đèn LED 18 W cùng độ sáng, 8 h/ngày, 22 ngày/tháng ⇒ tiết kiệm 464,64 kWh/tháng; tại nhà máy than $H = 36\,\%$
   ($q = 2{,}7\cdot10^7$, $k = 2{,}5$) ⇒ bớt ≈ 172,1 kg than và ≈ 430 kg CO₂ mỗi tháng; tiền (2 900 đ/kWh) ≈ 1 347 000 đ/tháng; 9 tháng học ≈ 4182 kWh.
TL4 Thuỷ điện tích năng: đêm bơm $3{,}6\cdot10^6$ m³ nước lên cao 300 m, $H_{bơm} = 85\,\%$; ngày xả phát điện $H_{phát} = 88\,\%$. Thế năng $1{,}08\cdot10^{13}$ J = 3000 MWh;
   điện bơm ≈ 3529 MWh; điện phát lại 2640 MWh; $H_{chu trình} = 74{,}8\,\%$. Xả trong 6 h ⇒ công suất 440 MW, lưu lượng ≈ 166,7 m³/s. Câu hỏi mở: vì sao "lỗ" 25 % vẫn đáng làm.
TL5 Hạt nhân và than: nhà máy hạt nhân 1000 MW điện, $H = 33\,\%$, chạy đủ 365 ngày; 1 g U-235 toả $8{,}2\cdot10^{10}$ J (cho sẵn) ⇒ năng lượng nhiên liệu ≈ $9{,}56\cdot10^{16}$ J,
   U-235 ≈ 1165 kg/năm. Nhà máy than $H = 36\,\%$ cùng điện năng ⇒ ≈ 3,24 triệu tấn than, ≈ 8,11 triệu tấn CO₂. Khối lượng nhiên liệu chênh ≈ 2,8 triệu lần.
   Định tính: ưu/nhược hạt nhân, vì sao không tái tạo, phân hạch ≠ nhiệt hạch.
TL6 (HSG tổng hợp) Hệ lai cho đảo 200 hộ × 5 kWh/ngày = 1000 kWh/ngày. Tuabin gió định mức 100 kW tại 12 m/s; hôm đó 10 h gió 6 m/s, 14 h gió 9 m/s ⇒ 12,5 kW và 42,19 kW,
   715,6 kWh. 40 % điện dùng ban đêm phải qua acquy hiệu suất nạp–xả 85 % ⇒ cần phát $1000/(0{,}6 + 0{,}4\cdot0{,}85) \approx 1063{,}8$ kWh ⇒ pin phải cho ≈ 348,2 kWh.
   Pin 19 %, $I = 1000$, $t_đ = 4{,}5$ h, biến tần 95 % ⇒ 0,812 kWh/(m²·ngày) ⇒ $S \approx 429$ m². Ngày không gió không nắng chạy diesel $H = 35\,\%$, $q = 4{,}4\cdot10^7$,
   0,84 kg/L, $k = 3{,}2$ ⇒ ≈ 233,8 kg ≈ 278 L dầu, ≈ 748 kg CO₂.

## Luyện tập (quiz buổi 16, ≥8 câu, tự chấm, nhãn như đề thật): 4 Phần I (A–D), 2 Phần II (a)–d) Đúng/Sai), 2 Phần III (đáp số).
I.1 Dạng nào KHÔNG có nguồn gốc từ bức xạ Mặt Trời? A. gió  B. sinh khối  **C. thuỷ triều**  D. dầu mỏ. (topic 99)
I.2 Máy ba cấp hiệu suất 90 %, 40 %, 95 %. Hiệu suất cả máy: A. 75 %  B. 40 %  **C. 34,2 %**  D. 95 %. (A = trung bình cộng — bẫy.) (topic 140)
I.3 Gió giảm từ 10 m/s xuống 8 m/s (dưới định mức), công suất tuabin: A. giảm 20 %  B. giảm 36 %  **C. giảm 48,8 %**  D. giảm 51,2 %. (B = bẫy bình phương; D = phần còn lại.) (topic 101)
I.4 Phát biểu đúng về năng lượng hạt nhân: **A. Nhà máy điện hạt nhân dùng phản ứng phân hạch urani, nửa sau (hơi nước → tuabin → máy phát) giống nhà máy nhiệt điện.**
   B. Là năng lượng tái tạo vì urani rất nhiều. C. Nhà máy điện hạt nhân hiện nay dùng phản ứng nhiệt hạch như Mặt Trời. D. Khi vận hành thải nhiều CO₂ như nhà máy than. (topic 227)
II.1 Thuỷ điện $h = 60$ m, $L = 100$ m³/s, $H = 85\,\%$, $d = 10^4$ N/m³. a) $P_n = 60$ MW — **Đúng**. b) $P_đ = 51$ MW — **Đúng**.
   c) $h$ giảm còn 30 m (giữ $L$) thì $P_đ$ giảm 4 lần — **Sai** (2 lần). d) Trong 1 giờ có $3{,}6\cdot10^5$ m³ nước qua tuabin — **Đúng**. (topic 101)
II.2 Đốt hết 1 tấn than đá ($q = 2{,}7\cdot10^7$ J/kg, $k = 2{,}5$) trong nhà máy $H = 35\,\%$. a) Than toả $2{,}7\cdot10^{10}$ J — **Đúng**. b) Điện năng thu được 7500 kWh — **Sai** (2625 kWh;
   7500 là chưa nhân $H$). c) CO₂ trong khí quyển giữ lại một phần bức xạ hồng ngoại Trái Đất phát ra — **Đúng**. d) Không có hiệu ứng nhà kính thì Trái Đất ấm áp và
   thuận lợi cho sự sống hơn — **Sai** (≈ −18 °C). (topic 100)
III.1 Hộ cần 9 kWh/ngày; tấm pin 1,8 m², $H = 20\,\%$, $I = 1000$ W/m², $t_đ = 4{,}5$ h, bỏ qua hao phí khác. Số tấm tối thiểu? **6** (5,56 → làm tròn lên). (topic 102)
III.2 Nhà máy nhiệt điện công suất điện 450 MW, $H = 37{,}5\,\%$, than $q = 2{,}4\cdot10^7$ J/kg. Khối lượng than đốt mỗi giờ (tấn)? **180**. (topic 100/140)

## YCCĐ cho "Làm bài tương tự"
KHTN 9 ĐÃ có YCCĐ cho Chương V (`scripts/data/question-topics.json`): bài 94 — "Năng lượng hoá thạch" (13) › "Vòng năng lượng trên Trái Đất" (99),
"Ưu nhược điểm của nhiên liệu hoá thạch" (100); bài 95 — "Năng lượng tái tạo" (14) › "Các dạng năng lượng tái tạo và nguồn gốc" (101),
"Sử dụng năng lượng tiết kiệm, hiệu quả" (102). Bổ sung cho phần định lượng: L10 b27 "Tính hiệu suất của máy và động cơ" (140),
"Hao phí năng lượng và cách giảm hao phí" (141); phần hạt nhân: L12 b16 (lesson 17) "Nhà máy điện hạt nhân và phản ứng nhiệt hạch" (227).
Khung `docs/HSG9-KHUNG.md` ghi CĐ09 "YCCĐ —" và chỉ trỏ L12 bài 17 — nên cập nhật thành 99–102 (+140, 227) nếu thầy đồng ý.
Chưa kiểm số câu trong `question_bank` gắn 99–102 (không truy vấn DB được ở phiên này): câu L12 (227) mức THPT, có độ hụt khối — nặng so với HS lớp 9.

## Sai sót docx (đã sửa/tránh trong bản này)
1. **Thuỷ triều bị bỏ khỏi danh sách "không từ Mặt Trời"**: docx nhiều chỗ ghi "trừ địa nhiệt và năng lượng hạt nhân", lại xếp "sóng biển và thuỷ triều" chung một mục.
   Thuỷ triều chủ yếu do hấp dẫn Mặt Trăng (và Mặt Trời) cùng chuyển động quay của Trái Đất, không do bức xạ Mặt Trời ⇒ thêm làm ngoại lệ thứ ba; tách khỏi sóng biển.
2. **Dạng 4 câu d**: hộ dùng 300 kWh/tháng nhưng docx nói đang trả "giá bậc 5 (3 350 đ)" — theo chính bảng 6 bậc của docx, kWh thứ 300 thuộc bậc 4 (201–300, 2 998 đ).
3. **Bảng 5 giá điện tự mâu thuẫn**: vừa nêu biểu 6 bậc "từ 10/5/2025" vừa nói QĐ 14/2025 rút còn 5 bậc. Số liệu thật đang đổi ⇒ CĐ09 không dùng biểu bậc thang;
   đơn giá luôn cho sẵn trong đề, một con số.
4. **Ký hiệu trùng**: docx dùng $Q$ cho cả lưu lượng nước và nhiệt lượng, $P$ cho cả trọng lượng và công suất (đoạn chứng minh $P = \rho g Q h$), $\rho$ thay cho $D$ của KHTN 9
   ⇒ ở đây: lưu lượng $L$, trọng lượng riêng $d = 10D$, công suất $P$.
5. Phương trình hoá học đốt cháy (C + O₂, CH₄ + 2O₂) và cơ chế mưa acid thuộc Hoá — bỏ (thầy chốt không soạn Hoá–Sinh).
6. Dạng 7 (đun nước bằng bếp các loại) và Dạng 4/bài D2, G2 (tiền điện bậc thang) trùng CĐ12/CĐ05 — không đưa vào CĐ09.
Đã soát nhanh đáp số docx (C Dạng 1/3/5/6, D1–D6, G1–G2, E2–E12): không thấy lệch số; không dùng lại các số đó.

## Điểm cần thầy quyết
- YCCĐ: dùng 99–102 (KHTN 9, có sẵn) thay cho chỉ L12 bài 17 như khung ghi? (đề xuất: có; giữ 227 cho phần hạt nhân).
- Có giữ một bài biểu giá bậc thang + giá biên (docx A2 có nêu) không? Bản này bỏ vì số liệu thật đang đổi và trùng CĐ05.
