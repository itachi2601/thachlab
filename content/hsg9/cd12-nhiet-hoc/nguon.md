# CĐ12. Nhiệt học nâng cao: cân bằng nhiệt và chuyển thể (bài 153, khoá Vật lí HSG & chuyên KHTN 9) — dàn ý chung

Nguồn: docx `12_nhiet-hoc-va-can-bang-nhiet.docx` (đã trích ở `nguon.txt` cùng thư mục — mục A, B, C, H/I dùng làm khung;
ví dụ D/E/G trong docx KHÔNG chép, số liệu dưới đây là số mới tự đặt). Viết lại bằng lời mình.
Lưu ý phạm vi (docx ghi): $c$, $\lambda$, $L$ và các công thức $Q$ không nằm trong YCCĐ lớp 8 CT 2018 — là kiến thức bổ sung
cho HSG; đề luôn cho sẵn hằng số.

**Ranh giới với CĐ16 (bài 164, Truyền nhiệt & nở vì nhiệt):** hao phí ra môi trường "công suất không đổi / tỉ lệ hiệu nhiệt độ",
ba cách truyền nhiệt, sự nở thuộc CĐ16 — CĐ12 KHÔNG làm các dạng đó. CĐ12 chỉ dùng hiệu suất $H = Q_{ích}/Q_{tp}$.
Tuần dùng: buổi 7 (21/11): thứ Hai đọc lý thuyết + quiz, thứ Ba bài tập mẫu "cân bằng nhiệt, chuyển thể" (`tuan.json`).

## Quy ước số liệu (mọi file dùng chung)
- Nước $c_n = 4200$, nước đá $c_đ = 2100$, nhôm $880$, đồng $380$, sắt/thép $460$, chì $130$ (J/(kg·K)).
- $\lambda_{đá} = 3{,}4\cdot10^5$ J/kg; $L_{nước} = 2{,}3\cdot10^6$ J/kg; chì: nóng chảy 327 °C, $\lambda_{chì} = 2{,}5\cdot10^4$ J/kg.
- Năng suất toả nhiệt: dầu hoả/gas $q = 4{,}4\cdot10^7$ J/kg (đề cho số). $g = 10$ m/s². 1 lít nước = 1 kg. 1 °C = 1 K cho hiệu nhiệt độ.
- Mặc định "bỏ qua trao đổi nhiệt với môi trường" phải GHI trong đề; bình chứa có tính hay không cũng phải ghi.

## Lý thuyết (theory.src.html) — 6 mục, ~15 phút
I. Mở bài: pha nước tắm cho em bé từ nước sôi và nước lạnh — bao nhiêu mỗi loại. Câu dự đoán: trộn 1 kg nước 80 °C với 1 kg
   nước 20 °C được bao nhiêu độ; nếu thay 1 kg nước 80 °C bằng 1 kg sắt 80 °C thì cao hơn hay thấp hơn 50 °C.
II. Nhiệt lượng $Q = mc\Delta t$; ý nghĩa nhiệt dung riêng (nước lớn ⇒ nóng lâu, nguội lâu, điều hoà khí hậu); nhiệt dung của vật $C = mc$.
III. Phương trình cân bằng nhiệt: nguyên lí truyền nhiệt (nóng → lạnh, tới khi bằng nhau, $Q_{toả} = Q_{thu}$ nếu bỏ qua hao phí);
   công thức nhanh hệ nhiều vật $t_{cb} = \dfrac{\sum m_i c_i t_i}{\sum m_i c_i}$ (khi không có chuyển thể); nhớ kể bình chứa.
IV. Chuyển thể: nóng chảy/đông đặc $Q = \lambda m$, hoá hơi/ngưng tụ $Q = Lm$; trong lúc chuyển thể nhiệt độ không đổi dù vẫn nhận/toả nhiệt;
   **biện luận trạng thái cuối** (so $Q_{toả,max}$ về 0 °C với $Q$ đưa đá lên 0 °C và $Q$ làm tan hết) — bốn khả năng; đọc đồ thị T–t
   (đoạn dốc: một thể, $P\,\Delta\tau = mc\Delta t$; đoạn ngang: chuyển thể, $P\,\Delta\tau = \lambda m$).
V. Mở rộng HSG: hiệu suất đun ($Q_{tp} = q\,m_{nl}$ hoặc $P\tau$); rót qua lại hai bình; chuyển hoá cơ năng ⇒ nhiệt năng (ma sát, va chạm: $Q = H\cdot W$).
VI. Trả bài và mang về (6 câu tự trả lời).

Bẫy (từ mục I docx, viết lại): nhầm nhiệt độ với nhiệt lượng; quên đổi g → kg; quên bình chứa; giả sử ngay $t_{cb} > 0$ °C rồi giải ra
âm; "nhiệt độ không đổi nghĩa là không nhận nhiệt" (sai); nghĩ $t_{cb}$ là trung bình cộng khi $mc$ khác nhau.

## Bài tập mẫu (scripts/data/bai-tap-mau/153.json) — 6 dạng, cấp không giảm. SỐ LIỆU ĐÃ TÍNH, dùng nguyên.
D1 (cấp 1) **Cân bằng nhiệt có kể bình.** Nhiệt lượng kế nhôm 150 g chứa 400 g nước 20 °C; thả miếng đồng 500 g ở 120 °C; bỏ qua môi trường.
   ⇒ $t_{cb} \approx 29{,}5$ °C. Nếu quên bình ⇒ tính ra $\approx 30{,}2$ °C (lệch ≈ 0,7 °C). topic: "Nhiệt độ và cân bằng nhiệt".
D2 (cấp 2) **Biện luận chuyển thể.** (a) Thả 300 g đá ở −10 °C vào 1 kg nước 30 °C (bình cách nhiệt, bỏ qua nhiệt dung bình):
   $Q_{toả,max} = 126\,000$ J; đưa đá lên 0 °C cần $6300$ J; làm tan hết cần $102\,000$ J; tổng $108\,300 < 126\,000$ ⇒ tan hết, $t_{cb} = \frac{17\,700}{1{,}3\cdot4200} \approx 3{,}2$ °C.
   (b) Thả tiếp 300 g đá −10 °C: nước 1,3 kg ở ≈3,24 °C toả tối đa $17\,700$ J; đưa đá lên 0 °C $6300$ J; tan được $\frac{11\,400}{3{,}4\cdot10^5} \approx 33{,}5$ g
   ⇒ $t_{cb} = 0$ °C, còn ≈ 266,5 g đá. topic: "Nhiệt nóng chảy riêng và nhiệt hoá hơi riêng".
D3 (cấp 2–3) **Đọc đồ thị T–t.** Đun 0,5 kg một chất rắn bằng nguồn cấp nhiệt có ích đều 200 W: 0–2 min nhiệt độ 20 → 80 °C; 2–7 min giữ 80 °C;
   7–9 min 80 → 120 °C. ⇒ $c_{rắn} = 800$, $\lambda = 1{,}2\cdot10^5$ J/kg, $c_{lỏng} = 1200$ J/(kg·K). Đồ thị vẽ SVG (đề cho mốc trên trục, không ghi sẵn kết quả).
   topic: "Nhiệt nóng chảy riêng và nhiệt hoá hơi riêng".
D4 (cấp 2) **Hiệu suất bếp nhiên liệu.** Đun 2 lít nước 20 °C trong nồi nhôm 0,5 kg tới sôi, bếp gas H = 40 %, $q = 4{,}4\cdot10^7$:
   $Q_{ích} = 707\,200$ J ⇒ $m_{gas} \approx 40{,}2$ g. Đun tiếp cho 10 % lượng nước hoá hơi (giữ H) ⇒ thêm $\approx 26{,}1$ g gas.
   topic: "Tính nhiệt lượng theo nhiệt dung riêng".
D5 (cấp 3) **Rót qua lại hai bình.** Bình 1: 2 kg nước 60 °C; bình 2: 1 kg nước 20 °C (bình cách nhiệt, bỏ qua nhiệt dung bình).
   Rót $m$ từ 1 sang 2, cân bằng, rót $m$ từ 2 về 1; bình 1 cuối 56 °C ⇒ $t_2' = 28$ °C, $m = 0{,}25$ kg. topic: "Nhiệt độ và cân bằng nhiệt".
D6 (cấp 4) **Cơ năng thành nhiệt năng.** (a) Thác cao 100 m, toàn bộ thế năng thành nhiệt làm nóng nước ⇒ nước chân thác nóng hơn ≈ 0,24 °C.
   (b) Đạn chì 27 °C bay 300 m/s cắm vào tường, 60 % động năng làm nóng đạn ⇒ tăng ≈ 208 °C, lên ≈ 235 °C < 327 °C ⇒ chưa chảy.
   (c) Vận tốc tối thiểu để đạn chảy hoàn toàn (vẫn 60 %) ⇒ $v \approx 462$ m/s. topic: "Nội năng và hai cách làm biến đổi nội năng".

## Tự luận (tu_luan) — 8 bài dễ → khó, mỗi bài có Hướng dẫn giải trong <details>.
Gợi ý: pha nước tắm (tìm thể tích hai loại nước); xác định nhiệt dung riêng kim loại bằng nhiệt lượng kế (nối buổi thí nghiệm);
dẫn hơi nước 100 °C vào cốc nước (ngưng tụ); đá tan một phần, tìm khối lượng đá ban đầu; đồ thị đông đặc khi làm lạnh;
rót qua lại nhiều lần (tìm quy luật); ba chất lỏng trộn từng đôi biết nhiệt độ cân bằng → tìm nhiệt độ khi trộn cả ba; bài tổng hợp HSG
(đá + hơi nước + bình nhôm, biện luận). Số liệu KHÁC bài tập mẫu và KHÁC ví dụ trong docx.

## Luyện tập (≥6 câu, tự chấm, nhãn như đề thật): 4 câu Phần I (A–D), 2 câu Phần II (a)–d) Đúng/Sai), 2 câu Phần III (đáp số).
Phủ: đơn vị/ý nghĩa $c$, $t_{cb}$ so với trung bình cộng, nhiệt độ khi sôi/nóng chảy, biện luận đá tan (tính), đồ thị T–t, hiệu suất (tính), rót qua lại.

## YCCĐ cho "Làm bài tương tự"
KHTN 9 chưa có YCCĐ nhiệt. Dùng L12 bài 3–5: "Nhiệt độ và cân bằng nhiệt" (198), "Nội năng và hai cách làm biến đổi nội năng" (199),
"Tính nhiệt lượng theo nhiệt dung riêng" (201), "Nhiệt nóng chảy riêng và nhiệt hoá hơi riêng" (202), "Xử lí số liệu thí nghiệm đo nhiệt" (203).
