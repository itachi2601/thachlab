# CĐ16. Truyền nhiệt và sự nở vì nhiệt (bài 164, khoá Vật lí HSG & chuyên KHTN 9) — dàn ý chung

Không có docx nguồn (chuyên đề mới, thêm theo đề cương "THI HSG 9 KHTN 26-27", mạch Năng lượng nhiệt).
Nền: KHTN 8 (sự truyền nhiệt: dẫn nhiệt, đối lưu, bức xạ; sự nở vì nhiệt). Chuyên đề ôn chuẩn lớp 8 rồi nâng lên
mức HSG 9 / tuyển sinh 10 chuyên. Lời văn tự viết, không chép SGK.

**Ranh giới với CĐ12 (bài 153, Nhiệt học & cân bằng nhiệt):** CĐ12 lo $Q = mc\Delta t$, cân bằng nhiệt, chuyển thể,
đồ thị T–t, rót qua lại, hiệu suất đun bằng nhiên liệu. CĐ16 lo **cách và tốc độ truyền nhiệt** (hao phí ra môi trường
theo thời gian / theo hiệu nhiệt độ) và **sự nở vì nhiệt**. CĐ16 được dùng $Q = mc\Delta t$ như công cụ, không dạy lại.
Tuần dùng: buổi 7 (21/11), HS đọc lý thuyết thứ Tư, làm bài tập mẫu thứ Năm (`tuan.json`); thứ Sáu đọc trước "đo nhiệt dung riêng".

## Quy ước số liệu (mọi file dùng chung)
- Nước $c = 4200\ \text{J/(kg·K)}$, $D = 1000\ \text{kg/m}^3$; 1 lít nước = 1 kg. Nhôm $c = 880$. Sôi ở $100\ ^\circ\text{C}$.
- Độ chênh nhiệt độ: $1\ ^\circ\text{C} = 1\ \text{K}$ (ghi rõ một lần ở lý thuyết).
- Hệ số nở dài (đề luôn cho số): thép $12\cdot10^{-6}\ \text{K}^{-1}$, đồng $17\cdot10^{-6}$, nhôm $24\cdot10^{-6}$.
  Chất rắn nở khối $\beta \approx 3\alpha$. Dầu hoả/xăng $\beta \approx 1\cdot10^{-3}\ \text{K}^{-1}$.
- Công thức nở: $l = l_0(1 + \alpha\Delta t)$, $V = V_0(1 + \beta\Delta t)$, $D = \dfrac{D_0}{1 + \beta\Delta t}$ (khối lượng không đổi).
- Hao phí ra môi trường: (a) "công suất hao phí không đổi" ⇒ $Q_{hp} = P_{hp}\,t$; (b) "công suất hao phí tỉ lệ với hiệu nhiệt độ vật – môi trường" ⇒ $P_{hp} = k(t - t_0)$. Đề phải nói rõ dùng giả thiết nào.
- Dẫn nhiệt qua vách: định tính $P \propto \dfrac{S\,\Delta t}{d}$ (không dạy hệ số dẫn nhiệt, chỉ dùng tỉ lệ).

## Lý thuyết (theory.src.html) — 6 mục, ~15 phút
I. Mở bài: thìa kim loại trong cốc trà nóng nóng lên tới cán; đường ray có khe hở. Câu dự đoán: sờ tay vào thanh sắt và
   miếng gỗ cùng để trong phòng, cái nào thấy lạnh hơn, vì sao (cùng nhiệt độ — sắt dẫn nhiệt tốt).
II. Ba cách truyền nhiệt: nhiệt tự truyền từ vật nóng hơn sang vật lạnh hơn. **Dẫn nhiệt** (chủ yếu ở rắn; kim loại dẫn tốt;
   lỏng, khí dẫn kém; chân không không dẫn). **Đối lưu** (lỏng, khí: phần nóng nở ra, nhẹ hơn, đi lên). **Bức xạ nhiệt**
   (truyền cả trong chân không; mặt sẫm màu, xù xì hấp thụ và bức xạ mạnh; mặt sáng bóng phản xạ). Ứng dụng: phích (chân
   không chặn dẫn nhiệt và đối lưu, mặt tráng bạc chặn bức xạ, nút chặn đối lưu ra ngoài); áo nhiều lớp (không khí kẹp giữa).
III. Tốc độ truyền nhiệt (Mở rộng HSG): qua vách $P \propto S\Delta t/d$; hao phí ra môi trường hai giả thiết (a), (b) ở trên.
   Hệ quả: dùng hai lần đun để khử ẩn (hao phí không đổi); nhiệt độ ổn định khi công suất cấp = công suất hao phí
   $P = k(t_{ođ} - t_0)$ — vật không nóng mãi.
IV. Sự nở vì nhiệt: rắn, lỏng, khí đều nở khi nóng, co khi lạnh; khí nở nhiều nhất, lỏng nhiều hơn rắn; công thức nở dài,
   nở khối, khối lượng riêng giảm khi nóng; vật bị cản nở sinh lực rất lớn (khe hở ray, ống dẫn uốn khúc, đầu cầu đặt con lăn);
   băng kép: khi nóng cong về phía kim loại nở ít (kim loại nở nhiều ở mặt lồi); nước bất thường: từ 0 °C đến 4 °C co lại,
   khối lượng riêng lớn nhất ở 4 °C ⇒ hồ đóng băng từ mặt, đáy hồ ~4 °C.
V. Mở rộng HSG: thước đo bị nở → số đọc sai; chất lỏng trong bình cùng nở ⇒ thể tích tràn $= V_0(\beta_l - \beta_b)\Delta t$;
   hai thanh có hiệu chiều dài không đổi ở mọi nhiệt độ ⇔ $l_1\alpha_1 = l_2\alpha_2$.
VI. Trả bài và mang về (6 câu tự trả lời).

Bẫy (H): "lạnh truyền sang" (sai — chỉ có nhiệt truyền từ nóng sang lạnh); sờ thấy lạnh ≠ nhiệt độ thấp hơn;
quên nhân $l_0$ ban đầu / dùng $l$ sau thay $l_0$; băng kép cong sai phía; đổi $^\circ$C sang K cho hiệu nhiệt độ (không cần);
áp hao phí "không đổi" khi đề cho "tỉ lệ hiệu nhiệt độ"; nghĩ rằng tăng thời gian đun thì vật nóng mãi.

## Bài tập mẫu (scripts/data/bai-tap-mau/164.json) — 6 dạng, cấp không giảm. SỐ LIỆU ĐÃ TÍNH, dùng nguyên.
D1 (cấp 1) **Dẫn nhiệt qua vách — tỉ lệ.** Hộp xốp đựng đá, thành dày 2 cm, chênh nhiệt độ trong–ngoài 30 °C: đá tan hết sau 6 h.
   Hộp cùng vật liệu, cùng diện tích, thành dày 3 cm, chênh 25 °C ⇒ $t = 6\cdot\frac{3}{2}\cdot\frac{30}{25} = 10{,}8$ h.
   Điều kiện phụ ghi trong đề: đá nhận nhiệt chỉ qua thành hộp; trong hộp giữ 0 °C khi đá đang tan; cùng lượng đá.
   topic: "Nhiệt độ và cân bằng nhiệt".
D2 (cấp 2) **Hao phí không đổi — đun hai lần khử ẩn.** Ấm điện, nước từ 20 °C đến sôi: 1 lít mất 10 min, 2 lít mất 18 min
   (cùng ấm, cùng bếp, hao phí công suất không đổi, ấm có nhiệt dung $C$ chưa biết).
   ⇒ $P - P_{hp} = \frac{4200\cdot80}{480\ \text{s}} = 700$ W; $C = 1050$ J/K; 3 lít mất $\frac{(3\cdot4200+1050)\cdot80}{700} = 1560$ s = 26 min;
   nếu ấm ghi 875 W ⇒ $P_{hp} = 175$ W, hiệu suất lần 1 (chỉ tính nước) $= \frac{336000}{875\cdot600} = 64\%$.
   topic: "Tính nhiệt lượng theo nhiệt dung riêng".
D3 (cấp 3) **Hao phí tỉ lệ hiệu nhiệt độ — nhiệt độ ổn định.** Máy sưởi 1200 W, ngoài trời 10 °C, phòng ổn định 22 °C
   ⇒ $k = 100$ W/°C. Ngoài trời 4 °C, muốn giữ 22 °C cần $1800$ W. Vẫn dùng 1200 W khi ngoài 4 °C ⇒ phòng ổn định ở 16 °C.
   topic: "Nhiệt độ và cân bằng nhiệt".
D4 (cấp 2) **Nở dài — khe hở và độ dãn.** Ray thép 12,5 m lắp ở 15 °C, nóng nhất 55 °C, $\alpha = 12\cdot10^{-6}$ ⇒ khe hở tối thiểu 6 mm.
   Cầu thép 500 m, nhiệt độ năm từ 10 °C đến 50 °C ⇒ chiều dài thay đổi 0,24 m = 24 cm. Thước thép khắc đúng ở 20 °C, đo ở
   45 °C đọc được 2,000 m ⇒ chiều dài thật 2,0006 m (thước dãn ⇒ đọc thiếu).
   topic: "Nhiệt độ và cân bằng nhiệt".
D5 (cấp 3) **Nở khối — khối lượng riêng và thể tích tràn.** Dầu hoả $D_{20} = 800$ kg/m³, $\beta = 1\cdot10^{-3}$:
   mua 1000 L lúc 35 °C được $788{,}2$ kg, thiếu $11{,}8$ kg so với 1000 L đo ở 20 °C (≈ 14,8 L ở 20 °C).
   Can thép ($\beta_b = 36\cdot10^{-6}$) chứa đầy 20 L dầu ở 20 °C, nóng lên 40 °C ⇒ tràn $20\cdot(10^{-3} - 36\cdot10^{-6})\cdot20 \approx 0{,}39$ L.
   topic: "Nhiệt độ và cân bằng nhiệt".
D6 (cấp 4) **Hai vật nở khác nhau.** (a) Thanh đồng và thanh thép có hiệu chiều dài luôn 5 cm ở mọi nhiệt độ ⇒ $l_{Cu}\alpha_{Cu} = l_{Fe}\alpha_{Fe}$
   ⇒ $l_{Cu} = 12$ cm, $l_{Fe} = 17$ cm. (b) Vòng nhôm đường kính trong 4,990 cm và quả cầu thép đường kính 5,000 cm ở 20 °C; nung
   cả hai cùng nhiệt độ $t$ thì cầu vừa lọt: $4{,}990(1+24\cdot10^{-6}\Delta t) = 5{,}000(1+12\cdot10^{-6}\Delta t)$ ⇒ $\Delta t \approx 167$ °C, $t \approx 187$ °C.
   topic: "Nhiệt độ và cân bằng nhiệt".

## Tự luận (tu_luan) — 8 bài dễ → khó, mỗi bài có Hướng dẫn giải trong <details>.
Gợi ý chủ đề: giải thích phích / áo bông / nồi đáy dày (định tính); kim loại sờ lạnh hơn gỗ; băng kép trong bàn là tự ngắt;
hồ đóng băng từ mặt; đun nước có hao phí không đổi tìm thời gian (biến thể D2 khác số); ấm tắt điện nguội dần,
hao phí tỉ lệ hiệu nhiệt độ: tốc độ hạ nhiệt gần 100 °C và gần 40 °C (biến thể D3); đồng hồ quả lắc / thước thép nở; bình
thuỷ tinh đầy thuỷ ngân nóng lên; bài tổng hợp HSG (máy sưởi + hai máy / ấm có hai dây điện trở + hao phí tỉ lệ hiệu nhiệt độ).

## Luyện tập (≥6 câu, tự chấm, nhãn như đề thật): 4 câu Phần I (A–D), 2 câu Phần II (a)–d) Đúng/Sai), 2 câu Phần III (đáp số).
Phủ: ba cách truyền nhiệt, phích, băng kép, nước 4 °C, khe hở ray (tính), hao phí tỉ lệ hiệu nhiệt độ (tính), thể tích tràn.
Số liệu KHÁC bài tập mẫu.

## YCCĐ cho "Làm bài tương tự"
KHTN 9 chưa có YCCĐ nhiệt. Dùng L12 bài 3–5: "Nhiệt độ và cân bằng nhiệt" (198), "Tính nhiệt lượng theo nhiệt dung riêng" (201),
"Nội năng và hai cách làm biến đổi nội năng" (199). Không có YCCĐ nở vì nhiệt ⇒ dạng nở dùng 198 tạm, ghi chú.
