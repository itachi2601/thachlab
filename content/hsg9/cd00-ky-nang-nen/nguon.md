# Chuyên đề 00. Kỹ năng nền: công cụ toán học, đọc đồ thị, sai số và thực hành

## A. Yêu cầu cần đạt và phạm vi

Chuyên đề này không dạy thêm một định luật vật lí mới. Nó trang bị bộ công cụ để học sinh giải được bài HSG Vật lí 9 ở cả năm chương: năng lượng cơ học, ánh sáng, điện, điện từ và năng lượng với cuộc sống. Kinh nghiệm chấm thi cho thấy phần lớn điểm bị mất không nằm ở chỗ "không biết định luật", mà nằm ở chỗ biến đổi đại số sai, đọc đồ thị lệch, quên đổi đơn vị, ghi kết quả đo sai quy cách và trình bày thiếu bước.

Sau khi học xong chuyên đề, học sinh cần đạt:

1. Biến đổi thành thạo các biểu thức đại số ở mức lớp 9: rút một đại lượng, lập tỉ số giữa hai trạng thái, chứng minh một hệ thức vật lí bằng lập luận từ công thức gốc.
2. Nhận ra và vận dụng quan hệ tỉ lệ thuận, tỉ lệ nghịch, tỉ lệ với bình phương, tỉ lệ nghịch với tổng hai đại lượng.
3. Đọc, vẽ, nội suy và ngoại suy đồ thị; nêu được ý nghĩa hệ số góc và ý nghĩa diện tích dưới đồ thị ở mức lớp 9.
4. Ước lượng nhanh một đại lượng, kiểm tra đơn vị (thứ nguyên) của công thức và phán đoán tính hợp lí của kết quả.
5. Hiểu sai số là gì, tính giá trị trung bình, tính sai số tuyệt đối và sai số tương đối, ghi kết quả đo đúng quy cách, biết xử lí một bảng số liệu thực hành.
6. Trình bày một bài thi HSG đúng cấu trúc: tóm tắt, đặt ký hiệu, lập luận từng bước, kết luận có đơn vị.

Phạm vi áp dụng và mức độ:

| Kỹ năng | Chương 1 Năng lượng cơ học | Chương 2 Ánh sáng | Chương 3 Điện | Chương 4 Điện từ | Chương 5 Năng lượng |
|---|---|---|---|---|---|
| Tỉ lệ thuận – tỉ lệ nghịch | A, P, v, h | n = c/v, f, d, d' | R = U/I, mạch nt và // | số vòng dây, hiệu điện thế (*) | công suất, hiệu suất |
| Đọc và vẽ đồ thị | s–t, v–t | quan hệ d–d' | U–I, P–t | U–t xoay chiều | P–t |
| Ước lượng và đơn vị | J, W, kWh | cm, m, đi-ốp | Ω, A, V, W | V, Hz | J, kWh, tấn dầu |
| Sai số và thực hành | đo thời gian, quãng đường | đo tiêu cự thấu kính | đo U, I, R | đo U, I | đọc công tơ điện |
| Trình bày bài thi | mọi dạng | mọi dạng | mọi dạng | mọi dạng | mọi dạng |

> **Ghi chú phạm vi (đối chiếu Yêu cầu cần đạt môn KHTN – Chương trình GDPT 2018, phần lớp 9):** một số nội dung được dùng trong tài liệu này nhưng **không có trong Yêu cầu cần đạt lớp 9** — chỉ nên dạy cho đội tuyển và phải nói rõ khi dạy:
>
> - (*) Tỉ số máy biến áp về số vòng dây và hiệu điện thế (không có trong mục lục cả ba bộ sách giáo khoa hiện hành, nhưng đề thi học sinh giỏi và đề thi vào lớp 10 chuyên vẫn ra).
> - Định luật Jun – Len-xơ Q = I²·R·t (bảng công thức ở mục B3 và Bài E7). Chương trình chỉ yêu cầu tính năng lượng của dòng điện và công suất điện.
> - Công thức thấu kính 1/f = 1/d + 1/d' (Yêu cầu cần đạt chỉ yêu cầu vẽ sơ đồ tỉ lệ để giải bài tập đơn giản về thấu kính hội tụ).
> - Số bội giác của kính lúp G = 25/f (Yêu cầu cần đạt chỉ yêu cầu mô tả cấu tạo và sử dụng kính lúp).
> - Ba quy tắc lan truyền sai số định lượng ở mục B2 (gần với Vật lí 10 hơn là lớp 9).
>
> **Về sai số dụng cụ, có hai trường hợp khác nhau:** dụng cụ chỉ có vạch chia thì lấy nửa độ chia nhỏ nhất (cách dùng trong tài liệu này); dụng cụ có ghi cấp chính xác thì lấy cấp chính xác nhân với giá trị lớn nhất của thang đo (cách trình bày trong chuyên đề 03). Không dùng lẫn hai cách cho cùng một dụng cụ.

## B. Lý thuyết trọng tâm

### B1. Kiến thức chuẩn theo SGK

**1. Tỉ lệ thuận và tỉ lệ nghịch.** Hai đại lượng y và x tỉ lệ thuận khi thương của chúng không đổi; viết y = k·x với k là hằng số. Hai đại lượng tỉ lệ nghịch khi tích của chúng không đổi; viết y = k/x. Cách dùng thực dụng nhất khi giải bài là lập tỉ số giữa hai trạng thái, vì hằng số k tự triệt tiêu.

Với hai trạng thái 1 và 2 của cùng một hệ, nếu y tỉ lệ thuận với x thì:

y₂/y₁ = x₂/x₁

Nếu y tỉ lệ nghịch với x thì:

y₂/y₁ = x₁/x₂

**2. Giá trị trung bình cộng.** Khi đo nhiều lần một đại lượng, giá trị đại diện là trung bình cộng của các lần đo. Với n lần đo giá trị A₁, A₂, ..., Aₙ:

A_tb = (A₁ + A₂ + ... + Aₙ)/n

**3. Đơn vị và đổi đơn vị.** Mỗi đại lượng vật lí có đơn vị hợp pháp. Trong hệ SI: mét (m), giây (s), kilôgam (kg), ampe (A), vôn (V), ôm (Ω), oát (W), jun (J), hec (Hz). Khi thay số vào công thức, phải đổi tất cả về một hệ đơn vị thống nhất, thường là hệ SI.

**4. Bảng số liệu và đồ thị.** Khi khảo sát quan hệ giữa hai đại lượng, SGK trình bày bảng số liệu kèm sai số của dụng cụ đo, sau đó vẽ đồ thị để thấy xu hướng. Một đồ thị đúng phải có trục hoành, trục tung ghi rõ tên đại lượng và đơn vị, có vạch chia đều theo tỉ lệ, có các điểm đo và đường biểu diễn.

**5. Định luật Ôm.** Cường độ dòng điện qua một đoạn mạch tỉ lệ thuận với hiệu điện thế hai đầu đoạn mạch và tỉ lệ nghịch với điện trở của đoạn mạch:

I = U/R

Đây là ví dụ chuẩn mực nhất của quan hệ tỉ lệ, đồng thời là mẫu để luyện đọc đồ thị U–I.

### B2. Mở rộng – nâng cao cho HSG

**1. Bốn kiểu quan hệ thường gặp.** Học sinh giỏi phải phân biệt được, vì chỉ cần nhận sai kiểu quan hệ là mất cả bài.

- Tỉ lệ thuận: y = k·x. Ví dụ A = P·t khi P không đổi, I = U/R khi R không đổi, s = v·t khi v không đổi.
- Tỉ lệ nghịch: y = k/x. Ví dụ I = U/R khi U không đổi, t = A/P khi A không đổi.
- Tỉ lệ với bình phương: y = k·x². Ví dụ P = I²R khi I thay đổi, Q = I²Rt, A_động = m·v²/2.
- Tỉ lệ nghịch với tổng: y = k/(a + x). Ví dụ I = U/(R₀ + R) khi biến trở R thay đổi. Đây không phải tỉ lệ nghịch đơn thuần với R, nên không được viết I₂/I₁ = R₁/R₂.

**2. Kỹ thuật rút tỉ số.** Muốn so sánh hai trạng thái mà không cần biết hằng số, hãy chia hai phương trình cho nhau. Ví dụ trong đoạn mạch nối tiếp, cùng dòng điện I chạy qua hai điện trở:

U₁ = I·R₁

U₂ = I·R₂

Chia vế theo vế:

U₁/U₂ = R₁/R₂

Cách làm này ngắn hơn nhiều so với việc tính số cụ thể từng bước.

**3. Nội suy và ngoại suy.** Nội suy là tìm giá trị nằm giữa hai điểm đo đã có; ngoại suy là tìm giá trị nằm ngoài khoảng đo. Với đồ thị gần đúng là đường thẳng, dùng nội suy tuyến tính: giữa hai điểm (x₁; y₁) và (x₂; y₂), tại x nằm giữa ta có:

y = y₁ + (y₂ − y₁)·(x − x₁)/(x₂ − x₁)

Quy tắc an toàn: chỉ ngoại suy trong khoảng ngắn và phải nói rõ đó là dự đoán, không phải số liệu đo.

**4. Ý nghĩa hệ số góc.** Trên đồ thị đường thẳng y = a·x + b, hệ số góc a cho biết khi x tăng 1 đơn vị thì y tăng a đơn vị. Đơn vị của a là đơn vị của y chia cho đơn vị của x. Cụ thể ở lớp 9:

- Đồ thị s–t (quãng đường theo thời gian) của chuyển động đều: hệ số góc là vận tốc, đơn vị m/s.
- Đồ thị U–I (hiệu điện thế theo cường độ dòng điện) của một dây dẫn: hệ số góc là điện trở, đơn vị V/A = Ω.
- Đồ thị I–U: hệ số góc là 1/R, đơn vị A/V.

**5. Ý nghĩa diện tích dưới đồ thị.** Diện tích phần giới hạn bởi đường biểu diễn và trục hoành bằng tích của hai đại lượng ở hai trục, nên mang ý nghĩa một đại lượng thứ ba:

- Đồ thị v–t: diện tích bằng quãng đường đi được, đơn vị (m/s)·s = m.
- Đồ thị P–t: diện tích bằng công (điện năng) tiêu thụ, đơn vị W·s = J.

Với đồ thị dạng bậc thang (chia thành các giai đoạn có giá trị không đổi), chỉ cần tính diện tích từng hình chữ nhật rồi cộng lại.

**6. Phân tích đơn vị (thứ nguyên).** Một công thức vật lí chỉ đúng khi hai vế cùng đơn vị. Kỹ thuật: thay đơn vị của từng đại lượng rồi rút gọn như rút gọn phân số đại số. Ví dụ kiểm tra v = √(2gh):

Đơn vị của g·h là (m/s²)·m = m²/s²

Lấy căn bậc hai được m/s, đúng bằng đơn vị của vận tốc.

Phân tích đơn vị không chứng minh được công thức đúng hoàn toàn, nhưng loại được rất nhiều công thức sai và là công cụ kiểm tra cực nhanh trong phòng thi.

**7. Sai số.** Sai số tuyệt đối của một phép đo là độ lệch giữa giá trị đo và giá trị thực, nhưng vì không biết giá trị thực nên trong thực hành ta lấy giá trị trung bình làm chuẩn.

Sai số ngẫu nhiên trung bình:

ΔA_ng = (|A₁ − A_tb| + |A₂ − A_tb| + ... + |Aₙ − A_tb|)/n

Sai số dụng cụ thường lấy bằng nửa độ chia nhỏ nhất (ĐCNN) của dụng cụ.

Sai số tuyệt đối của phép đo:

ΔA = ΔA_ng + ΔA_dc

Sai số tương đối:

δA = ΔA/A_tb

Kết quả đo được ghi dưới dạng A = A_tb ± ΔA, kèm đơn vị. Sai số tương đối thường ghi theo phần trăm.

Ba quy tắc lan truyền sai số cần nhớ ở mức lớp 9:

- Phép cộng và phép trừ: Δ(A ± B) = ΔA + ΔB (sai số tuyệt đối cộng lại).
- Phép nhân và phép chia: δ(A·B) = δA + δB và δ(A/B) = δA + δB (sai số tương đối cộng lại).
- Nhân với một hằng số đúng: sai số tương đối không đổi; ví dụ f = d/2 thì δf = δd, suy ra Δf = f·δd.

**8. Chữ số có nghĩa và cách làm tròn.** Sai số quyết định số chữ số được giữ lại của kết quả. Quy tắc thực hành: sai số tuyệt đối làm tròn đến một chữ số có nghĩa (hai chữ số nếu chữ số đầu là 1), còn giá trị trung bình làm tròn đến cùng hàng thập phân với sai số. Số 0,30 A có hai chữ số có nghĩa, số 0,3 A chỉ có một; không được viết 0,3 khi dụng cụ đọc được đến 0,01 A.

**9. Loại bỏ số liệu bất thường.** Một lần đo lệch hẳn khỏi các lần còn lại (do đọc nhầm, chạm tay vào dụng cụ, mất ổn định) phải được loại bỏ trước khi tính trung bình, và phải ghi rõ lí do loại. Không được vừa giữ giá trị bất thường vừa tự ý bỏ qua nó khi nhận xét.

**10. Kỹ năng trình bày bài thi HSG.** Một bài giải được điểm tối đa cần:

- Tóm tắt đề bằng ký hiệu có ghi đơn vị, kể cả đại lượng cần tìm.
- Vẽ hình (nếu có) và đặt ký hiệu trên hình khớp với tóm tắt.
- Viết công thức gốc trước, thay số sau, mỗi bước một dòng.
- Giữ ký hiệu chữ đến bước cuối rồi mới thay số khi bài toán cho nhiều trạng thái.
- Kiểm tra đơn vị và tính hợp lí của kết quả trước khi kết luận.
- Kết luận thành câu, có đơn vị, có so sánh hoặc nhận xét nếu đề hỏi.

### B3. Công thức và hằng số cần nhớ (bảng)

**Bảng 1. Đổi đơn vị thường dùng**

| Đại lượng | Đổi đơn vị |
|---|---|
| Vận tốc | 1 m/s = 3,6 km/h; 1 km/h = 1/3,6 m/s ≈ 0,278 m/s |
| Thời gian | 1 phút = 60 s; 1 giờ = 3600 s; 1 ngày = 86400 s |
| Năng lượng | 1 kJ = 1000 J; 1 MJ = 10⁶ J; 1 kWh = 3,6·10⁶ J; 1 cal ≈ 4,2 J |
| Công suất | 1 kW = 1000 W; 1 MW = 10⁶ W; 1 HP ≈ 746 W |
| Khối lượng | 1 tấn = 1000 kg; 1 g = 10⁻³ kg; 1 lạng = 100 g |
| Thể tích | 1 lít = 1 dm³ = 10⁻³ m³; 1 ml = 1 cm³ = 10⁻⁶ m³ |
| Diện tích | 1 cm² = 10⁻⁴ m²; 1 mm² = 10⁻⁶ m² |
| Khối lượng riêng | 1 g/cm³ = 1000 kg/m³ |
| Dòng điện | 1 mA = 10⁻³ A; 1 A = 1000 mA |
| Hiệu điện thế | 1 mV = 10⁻³ V; 1 kV = 1000 V |
| Điện trở | 1 kΩ = 1000 Ω; 1 MΩ = 10⁶ Ω |
| Chiều dài | 1 cm = 10⁻² m; 1 mm = 10⁻³ m; 1 km = 1000 m |
| Góc | 1° = 60' (phút góc) |

**Bảng 2. Công thức Vật lí 9 dùng nhiều**

| Nhóm | Công thức |
|---|---|
| Chuyển động | v = s/t; s = v·t; t = s/v; v_tb = s_tổng/t_tổng |
| Công – công suất | A = F·s (khi F cùng phương với s); P = A/t |
| Cơ năng | W_đ = m·v²/2; W_t = 10·m·h; W = W_đ + W_t |
| Định luật Ôm | I = U/R; U = I·R; R = U/I |
| Mạch nối tiếp | I = I₁ = I₂; U = U₁ + U₂; R_tđ = R₁ + R₂ |
| Mạch song song | U = U₁ = U₂; I = I₁ + I₂; 1/R_tđ = 1/R₁ + 1/R₂ |
| Hai điện trở song song | R_tđ = R₁·R₂/(R₁ + R₂) |
| Điện trở dây dẫn | R = ρ·l/S; S = π·d²/4 |
| Công – công suất điện | A = U·I·t = I²·R·t = U²·t/R; P = U·I = I²·R = U²/R |
| Định luật Jun – Len-xơ (bổ sung ngoài YCCĐ lớp 9) | Q = I²·R·t |
| Nhiệt lượng | Q = m·c·Δt; Q = m·λ (nóng chảy); Q = m·L (hoá hơi); Q = q·m (nhiên liệu) |
| Hiệu suất | H = A_ích/A_toàn phần · 100% |
| Khúc xạ | n = c/v; n₁·sin i = n₂·sin r (khi i nhỏ: n₁·i ≈ n₂·r) |
| Phản xạ toàn phần | chỉ xảy ra khi ánh sáng đi từ môi trường chiết quang hơn sang kém hơn và i ≥ i_gh |
| Thấu kính hội tụ (bổ sung ngoài YCCĐ lớp 9) | 1/f = 1/d + 1/d'; ảnh thật: d' = d·f/(d − f) |
| Số bội giác kính lúp (bổ sung ngoài YCCĐ lớp 9) | G = 25/f (f tính bằng cm) |

**Bảng 3. Hằng số và số liệu cần nhớ**

| Đại lượng | Giá trị thường dùng |
|---|---|
| Gia tốc trọng trường | g = 10 m/s² (bài toán cho phép lấy tròn); chính xác hơn 9,8 m/s² |
| Nhiệt dung riêng của nước | c = 4200 J/(kg·K) |
| Nhiệt dung riêng của nước đá | c = 2100 J/(kg·K) |
| Nhiệt dung riêng của nhôm | c = 880 J/(kg·K) |
| Nhiệt dung riêng của đồng | c = 380 J/(kg·K) |
| Nhiệt dung riêng của thép | c = 460 J/(kg·K) |
| Nhiệt dung riêng của không khí | c ≈ 1000 J/(kg·K) |
| Nhiệt nóng chảy của nước đá | λ = 3,4·10⁵ J/kg |
| Nhiệt hoá hơi của nước | L = 2,3·10⁶ J/kg |
| Năng suất toả nhiệt của xăng | q = 4,6·10⁷ J/kg |
| Năng suất toả nhiệt của dầu hoả | q = 4,4·10⁷ J/kg |
| Năng suất toả nhiệt của than đá | q = 2,7·10⁷ J/kg |
| Năng suất toả nhiệt của củi khô | q = 1,0·10⁷ J/kg |
| Khối lượng riêng của nước | D = 1000 kg/m³ |
| Khối lượng riêng của nhôm | D = 2700 kg/m³ |
| Khối lượng riêng của đồng | D = 8900 kg/m³ |
| Khối lượng riêng của thép | D = 7800 kg/m³ |
| Khối lượng riêng của thuỷ ngân | D = 13600 kg/m³ |
| Khối lượng riêng của không khí | D ≈ 1,29 kg/m³ |
| Tốc độ ánh sáng trong chân không | c = 3·10⁸ m/s |
| Chiết suất của nước | n = 4/3 ≈ 1,33 |
| Chiết suất của thuỷ tinh thường | n ≈ 1,5 |
| Chiết suất của kim cương | n = 2,42 |
| Tốc độ truyền âm trong không khí | v ≈ 340 m/s |
| Nhiệt độ nước đá đang tan | 0 °C |
| Nhiệt độ nước sôi ở áp suất thường | 100 °C |
| Điện áp lưới điện sinh hoạt Việt Nam | 220 V, tần số 50 Hz |

## C. Các dạng bài và phương pháp giải

### Dạng 1. Biến đổi đại số, tỉ lệ thuận – tỉ lệ nghịch, rút tỉ số và chứng minh hệ thức

**Nhận dạng.** Đề cho hai trạng thái của cùng một hệ (hoặc hỏi "khi ... tăng gấp đôi thì ... thay đổi thế nào"), hoặc yêu cầu chứng minh một hệ thức như U₁/U₂ = R₁/R₂, P₁/P₂ = R₁/R₂, Q₁/Q₂ = R₁/R₂. Trong đề cũng thường có câu "tính tỉ số" hoặc "lập luận để suy ra".

**Phương pháp.**

1. Viết công thức gốc liên hệ các đại lượng.
2. Viết công thức cho trạng thái 1 và trạng thái 2, giữ nguyên ký hiệu chữ.
3. Chia hai phương trình vế theo vế để triệt tiêu các đại lượng không đổi.
4. Rút ra tỉ số cần tìm; nếu cần thì thay số ở bước cuối.
5. Kiểm tra lại bằng cách thay một bộ số đơn giản.

**Ví dụ mẫu.** Một dây dẫn có điện trở R không đổi. Khi đặt hiệu điện thế U₁ = 6 V thì dòng điện là I₁ = 0,30 A. Hỏi khi đặt hiệu điện thế U₂ = 9 V thì dòng điện là bao nhiêu?

**Lời giải**

Vì điện trở không đổi, cường độ dòng điện tỉ lệ thuận với hiệu điện thế:

I = U/R

Lập tỉ số cho hai trạng thái:

I₂/I₁ = U₂/U₁

Suy ra:

I₂ = I₁·U₂/U₁

Thay số:

I₂ = 0,30 × 9/6 = 0,30 × 1,5

I₂ = 0,45 A

Kiểm tra hợp lí: hiệu điện thế tăng 1,5 lần thì dòng điện cũng tăng 1,5 lần; điện trở suy ra từ hai trạng thái đều bằng R = 6/0,30 = 20 Ω và R = 9/0,45 = 20 Ω, khớp nhau.

**Đáp số:** I₂ = 0,45 A.

**Lưu ý.**

- Chỉ được lập tỉ số trực tiếp khi đại lượng ở mẫu thực sự không đổi. Với mạch có biến trở, I không tỉ lệ nghịch với R của biến trở mà tỉ lệ nghịch với tổng R₀ + R.
- Khi tỉ lệ với bình phương, phải bình phương cả tỉ số. Ví dụ P = I²R nên P₂/P₁ = (I₂/I₁)².
- Với đoạn mạch song song, công thức đúng là I₁/I₂ = R₂/R₁ (nghịch đảo), đừng viết nhầm thành R₁/R₂.
- Không được thay số vào công thức gốc ngay từ đầu rồi mới rút tỉ số, vì sẽ làm mất dấu vết lập luận và dễ sai số.

### Dạng 2. Đọc, vẽ và nội suy đồ thị

**Nhận dạng.** Đề cho bảng số liệu kèm yêu cầu vẽ đồ thị, hoặc cho mô tả đồ thị và yêu cầu xác định một đại lượng (điện trở, vận tốc), tìm giá trị tại một điểm không có trong bảng (nội suy), hoặc nhận xét hai dây dẫn nào có điện trở lớn hơn.

**Phương pháp.**

1. Xác định rõ trục hoành, trục tung biểu diễn đại lượng nào và đơn vị nào.
2. Chọn tỉ lệ xích sao cho đồ thị chiếm phần lớn khổ giấy, chia vạch đều.
3. Đánh dấu các điểm đo bằng dấu chấm rõ ràng, ghi bên cạnh bảng giá trị nếu cần.
4. Nối các điểm bằng một đường liền mạch phù hợp xu hướng; nếu các điểm gần thẳng hàng thì vẽ một đường thẳng đi sát các điểm, không nhất thiết đi qua tất cả.
5. Nhận xét dạng đồ thị: đường thẳng qua gốc toạ độ là tỉ lệ thuận; đường thẳng không qua gốc có dạng y = a·x + b; đường cong là quan hệ phi tuyến.
6. Nội suy bằng công thức nội suy tuyến tính hoặc bằng cách đọc trực tiếp trên đồ thị, rồi ghi rõ đó là giá trị nội suy.

**Ví dụ mẫu.** Bảng số liệu khảo sát một dây dẫn:

| U (V) | 0 | 1,5 | 3,0 | 4,5 | 6,0 |
|---|---|---|---|---|---|
| I (A) | 0 | 0,10 | 0,20 | 0,30 | 0,40 |

a) Vẽ đồ thị U theo I và cho biết dây dẫn có tuân theo định luật Ôm không.

b) Xác định điện trở của dây dẫn từ đồ thị.

c) Nội suy cường độ dòng điện khi U = 3,75 V.

d) Ngoại suy hiệu điện thế khi I = 0,55 A.

**Lời giải**

a) Trục hoành là I (A), trục tung là U (V). Năm điểm đo là (0; 0), (0,10; 1,5), (0,20; 3,0), (0,30; 4,5), (0,40; 6,0). Các điểm này nằm trên một đường thẳng đi qua gốc toạ độ, nên U tỉ lệ thuận với I: dây dẫn tuân theo định luật Ôm.

b) Lấy hai điểm bất kì trên đường thẳng:

R = U/I = 1,5/0,10 = 15 Ω

Kiểm tra với điểm khác:

R = 4,5/0,30 = 15 Ω

Kết quả trùng nhau, vậy R = 15 Ω. Trên đồ thị U–I, hệ số góc của đường thẳng chính là điện trở.

c) Vì U tỉ lệ thuận với I nên:

I = U/R = 3,75/15 = 0,25 A

d) Ngoại suy trong khoảng ngắn:

U = I·R = 0,55 × 15 = 8,25 V

**Đáp số:** a) Đồ thị là đường thẳng qua gốc, dây dẫn tuân theo định luật Ôm. b) R = 15 Ω. c) I = 0,25 A. d) U = 8,25 V (giá trị dự đoán, cần kiểm tra bằng thực nghiệm).

**Lưu ý.**

- Không được nối các điểm đo bằng đường gấp khúc zíc zắc; hãy vẽ một đường trơn hoặc đường thẳng phù hợp xu hướng.
- Ghi đơn vị trên cả hai trục, nếu thiếu sẽ bị trừ điểm dù hình vẽ đẹp.
- Trên đồ thị I–U thì hệ số góc là 1/R, còn trên đồ thị U–I thì hệ số góc là R. Đọc sai trục là sai toàn bộ kết luận.
- Ngoại suy xa vùng số liệu rất dễ sai và không có giá trị thực nghiệm; chỉ nên ngoại suy khi đường biểu diễn đã rõ dạng.

### Dạng 3. Ý nghĩa hệ số góc và diện tích dưới đồ thị

**Nhận dạng.** Đề yêu cầu tính quãng đường từ đồ thị vận tốc, tính điện năng từ đồ thị công suất, hoặc yêu cầu nêu ý nghĩa của hệ số góc và diện tích trên một đồ thị cho trước.

**Phương pháp.**

1. Xác định hai đại lượng trên hai trục và đơn vị của chúng.
2. Nếu đề hỏi về tốc độ biến thiên (một đại lượng chia cho đại lượng kia), đó là hệ số góc; đơn vị là thương hai đơn vị.
3. Nếu đề hỏi về tích hai đại lượng, đó là diện tích dưới đồ thị; đơn vị là tích hai đơn vị.
4. Với đồ thị bậc thang, chia thành các hình chữ nhật, tính diện tích từng hình rồi cộng.
5. Với đồ thị tam giác hoặc hình thang, dùng công thức diện tích tam giác và hình thang ở mức toán lớp 8.

**Ví dụ mẫu.** Một bếp điện hoạt động theo hai giai đoạn: trong 5 phút đầu công suất là 800 W, trong 10 phút tiếp theo công suất là 1200 W. Vẽ dạng đồ thị P–t và tính điện năng tiêu thụ trong 15 phút đó.

**Lời giải**

Đồ thị P–t gồm hai hình chữ nhật: hình thứ nhất cao 800 W rộng 300 s, hình thứ hai cao 1200 W rộng 600 s. Diện tích dưới đồ thị chính là điện năng tiêu thụ.

Đổi thời gian:

t₁ = 5 phút = 300 s

t₂ = 10 phút = 600 s

Điện năng giai đoạn 1:

A₁ = P₁·t₁ = 800 × 300 = 240 000 J

Điện năng giai đoạn 2:

A₂ = P₂·t₂ = 1200 × 600 = 720 000 J

Tổng điện năng:

A = A₁ + A₂ = 240 000 + 720 000

A = 960 000 J

Đổi sang kWh:

A = 960 000/3 600 000 = 0,267 kWh ≈ 0,27 kWh

**Đáp số:** A = 960 000 J ≈ 0,27 kWh.

**Lưu ý.**

- Phải đổi phút ra giây trước khi nhân với công suất tính bằng oát, nếu không kết quả sẽ sai 60 lần.
- Diện tích dưới đồ thị v–t là quãng đường, diện tích dưới đồ thị P–t là công. Diện tích dưới đồ thị U–I không có ý nghĩa vật lí đơn giản ở lớp 9, đừng gán bừa.
- Với đồ thị v–t có đoạn nằm dưới trục hoành (vật đi ngược chiều), diện tích âm biểu diễn độ dịch chuyển ngược chiều; quãng đường vẫn là tổng các giá trị tuyệt đối. Ở lớp 9 hầu như chỉ gặp trường hợp vận tốc không đổi dấu.

### Dạng 4. Ước lượng, kiểm tra đơn vị và kiểm tra tính hợp lí của kết quả

**Nhận dạng.** Đề yêu cầu "kiểm tra lại kết quả", "nhận xét kết quả có hợp lí không", hoặc bài thực hành yêu cầu chọn dụng cụ đo phù hợp. Dạng này cũng xuất hiện như bước cuối của mọi bài giải.

**Phương pháp.**

1. Viết công thức, thay đơn vị của từng đại lượng rồi rút gọn để kiểm tra hai vế.
2. Ước lượng bậc độ lớn trước khi tính chính xác: con số phải nằm trong khoảng quen thuộc của đời sống.
3. So sánh kết quả với một mốc đã biết (ví dụ điện trở bóng đèn 220 V – 60 W cỡ vài trăm ôm, dòng điện qua bóng đèn cỡ vài phần mười ampe).
4. Nếu kết quả vô lí (dòng điện hàng nghìn ampe qua đèn pin, hiệu suất lớn hơn 100%), phải tìm lỗi trước khi kết luận.

**Ví dụ mẫu.** Kiểm tra các phát biểu sau:

a) Công thức v = √(2gh) có đúng đơn vị không?

b) Một học sinh tính nhiệt lượng cần đun 2 kg nước từ 20 °C lên 100 °C là 672 000 J. Đúng hay sai?

c) Một bóng đèn ghi 220 V – 60 W. Tính điện trở và dòng điện định mức, nhận xét kết quả.

**Lời giải**

a) Xét đơn vị của biểu thức dưới căn:

g·h có đơn vị là (m/s²)·m = m²/s²

Căn bậc hai của m²/s² là m/s, đúng bằng đơn vị của vận tốc. Vậy công thức hợp lí về đơn vị.

b) Nhiệt lượng cần thiết:

Q = m·c·Δt

Với Δt = 100 − 20 = 80 °C, độ tăng nhiệt độ cũng bằng 80 K.

Q = 2 × 4200 × 80

Q = 672 000 J

Vậy kết quả của học sinh là đúng.

c) Điện trở của đèn ở chế độ làm việc bình thường:

R = U²/P = 220²/60

R = 48 400/60 ≈ 807 Ω

Cường độ dòng điện định mức:

I = P/U = 60/220 ≈ 0,27 A

Nhận xét: dòng điện cỡ vài phần mười ampe và điện trở cỡ vài trăm ôm là hoàn toàn hợp lí với một bóng đèn dây tóc gia dụng. Nếu tính ra dòng điện vài chục ampe thì chắc chắn đã lẫn đơn vị.

**Đáp số:** a) Đơn vị đúng. b) Q = 672 000 J, học sinh đúng. c) R ≈ 807 Ω; I ≈ 0,27 A, hợp lí.

**Lưu ý.**

- Kiểm tra đơn vị không phát hiện được sai hệ số (ví dụ viết A = F·s/2 thay vì A = F·s vẫn đúng đơn vị), nên phải dùng kèm với kiểm tra bản chất.
- Khi nhân hoặc chia hỗn hợp đơn vị, hãy viết đơn vị ra như viết ký hiệu đại số, tuyệt đối không bỏ qua.
- Một số đơn vị phi SI như kWh, cal, mã lực vẫn dùng trong thực tế; khi tính theo công thức SI phải đổi về J và W.

### Dạng 5. Sai số, giá trị trung bình, ghi kết quả đo và xử lí bảng số liệu thực hành

**Nhận dạng.** Đề cho một bảng số liệu đo nhiều lần hoặc đo ở nhiều mức giá trị, yêu cầu tính giá trị trung bình, tính sai số, ghi kết quả đo, hoặc xử lí số liệu để suy ra một đại lượng (điện trở, tiêu cự, nhiệt dung riêng) rồi nhận xét.

**Phương pháp.**

1. Kiểm tra dụng cụ: đọc ĐCNN để biết sai số dụng cụ bằng nửa ĐCNN.
2. Tính giá trị trung bình cộng của các lần đo.
3. Tính độ lệch tuyệt đối của từng lần so với trung bình, rồi lấy trung bình cộng các độ lệch đó.
4. Cộng sai số ngẫu nhiên với sai số dụng cụ để được sai số tuyệt đối.
5. Làm tròn sai số và giá trị trung bình về cùng một hàng thập phân.
6. Tính sai số tương đối theo phần trăm.
7. Ghi kết quả dạng A = A_tb ± ΔA kèm đơn vị.
8. Với bảng số liệu nhiều mức giá trị, tính đại lượng cần tìm ở từng hàng rồi lấy trung bình, đồng thời so sánh các hàng để phát hiện hàng bất thường.

**Ví dụ mẫu.** Dùng vôn kế có ĐCNN 0,1 V đo hiệu điện thế hai đầu một điện trở, thu được bảng sau.

| Lần đo | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| U (V) | 5,8 | 5,9 | 5,8 | 5,9 | 6,1 |

Tính giá trị trung bình, sai số tuyệt đối, sai số tương đối và ghi kết quả đo.

**Lời giải**

Giá trị trung bình:

U_tb = (5,8 + 5,9 + 5,8 + 5,9 + 6,1)/5

U_tb = 29,5/5 = 5,90 V

Độ lệch của từng lần đo so với giá trị trung bình:

|5,8 − 5,90| = 0,10 V

|5,9 − 5,90| = 0,00 V

|5,8 − 5,90| = 0,10 V

|5,9 − 5,90| = 0,00 V

|6,1 − 5,90| = 0,20 V

Sai số ngẫu nhiên trung bình:

ΔU_ng = (0,10 + 0,00 + 0,10 + 0,00 + 0,20)/5

ΔU_ng = 0,40/5 = 0,08 V

Sai số dụng cụ bằng nửa ĐCNN:

ΔU_dc = 0,1/2 = 0,05 V

Sai số tuyệt đối của phép đo:

ΔU = 0,08 + 0,05 = 0,13 V

Làm tròn theo ĐCNN 0,1 V, lấy ΔU = 0,1 V.

Sai số tương đối:

δU = 0,1/5,90 ≈ 0,017 = 1,7%

Kết quả đo:

U = 5,90 V ± 0,1 V, tức là U = 5,9 V ± 0,1 V (sai số tương đối khoảng 1,7%).

**Lưu ý.**

- Phải lấy giá trị tuyệt đối của độ lệch; nếu cộng đại số thì các độ lệch dương và âm sẽ triệt tiêu và cho kết quả sai.
- Sai số tuyệt đối được làm tròn tới **một chữ số có nghĩa**, và giá trị trung bình được làm tròn tới cùng hàng với sai số. Nếu muốn thận trọng (không đánh giá phép đo tốt hơn thực tế) thì làm tròn **lên**; nếu theo thói quen trình bày ở trường thì làm tròn tới chữ số có nghĩa gần nhất. Trong cả hai cách, phải giữ nhất quán giữa sai số và giá trị trung bình.
- Không ghi kết quả với quá nhiều chữ số: U = 5,9 V ± 0,1 V là hợp lí, còn U = 5,900 V ± 0,1 V là sai quy cách.
- Nếu một lần đo lệch hẳn (ví dụ 6,8 V trong khi bốn lần kia đều 5,8 đến 5,9 V), phải loại bỏ và ghi rõ lí do trước khi tính trung bình.

**Ví dụ mẫu 2.** Xử lí bảng số liệu đo điện trở bằng cách thay đổi hiệu điện thế.

| Lần đo | U (V) | I (A) |
|---|---|---|
| 1 | 2,0 | 0,13 |
| 2 | 4,0 | 0,26 |
| 3 | 6,0 | 0,40 |
| 4 | 8,0 | 0,53 |
| 5 | 10,0 | 0,67 |

Tính điện trở trong mỗi lần đo và giá trị trung bình.

**Lời giải**

Áp dụng R = U/I cho từng hàng:

R₁ = 2,0/0,13 ≈ 15,38 Ω

R₂ = 4,0/0,26 ≈ 15,38 Ω

R₃ = 6,0/0,40 = 15,00 Ω

R₄ = 8,0/0,53 ≈ 15,09 Ω

R₅ = 10,0/0,67 ≈ 14,93 Ω

Giá trị trung bình:

R_tb = (15,38 + 15,38 + 15,00 + 15,09 + 14,93)/5

R_tb = 75,78/5 ≈ 15,16 Ω

Làm tròn theo độ chính xác của số liệu: R ≈ 15,2 Ω.

Nhận xét: năm giá trị điện trở sai khác nhau không quá 0,5 Ω, chứng tỏ điện trở gần như không đổi; dây dẫn tuân theo định luật Ôm. Nếu một hàng cho giá trị lệch hẳn (ví dụ 30 Ω) thì phải kiểm tra lại phép đọc cường độ dòng điện ở hàng đó.

**Đáp số:** R ≈ 15,2 Ω.

**Lưu ý.**

- Có thể xác định R bằng hệ số góc của đồ thị U–I, cách này thường chính xác hơn lấy trung bình các tỉ số vì san đều sai số của cả 5 điểm.
- Giữ đủ chữ số trung gian khi chia, chỉ làm tròn ở kết quả cuối; làm tròn sớm sẽ làm lệch kết quả trung bình.
- Ghi đơn vị cho từng giá trị trong bảng kết quả, không chỉ ghi ở tiêu đề.

### Dạng 6. Trình bày bài thi HSG: tóm tắt, đặt ký hiệu, lập luận từng bước, kết luận có đơn vị

**Nhận dạng.** Mọi bài tự luận. Dạng này không có đề riêng, nhưng là dạng quyết định điểm số nhiều nhất vì cùng một lời giải, người trình bày tốt có thể hơn 1 đến 2 điểm.

**Phương pháp.** Dùng khung bốn bước cố định sau.

1. Bước 1 — Tóm tắt. Ghi các đại lượng đã cho bằng ký hiệu, kèm đơn vị đã đổi về SI. Ghi đại lượng cần tìm. Nếu đề có nhiều trạng thái, đánh số 1 và 2 cho từng trạng thái.
2. Bước 2 — Đặt ký hiệu và vẽ hình. Với bài mạch điện, vẽ sơ đồ và ghi tên các điện trở, chiều dòng điện. Với bài quang học, vẽ trục chính, thấu kính, vật, ảnh và ghi khoảng cách d, d', f.
3. Bước 3 — Lập luận. Viết công thức gốc, biến đổi từng bước một dòng. Với bài có nhiều trạng thái, giữ ký hiệu chữ đến bước cuối rồi mới thay số.
4. Bước 4 — Kết luận. Trả lời đúng câu hỏi, có đơn vị, có nhận xét hoặc kiểm tra hợp lí nếu đề yêu cầu.

**Ví dụ mẫu.** Một ấm điện ghi 220 V – 1000 W được dùng ở hiệu điện thế 220 V để đun 1,5 lít nước từ 25 °C đến 100 °C. Hiệu suất của ấm là 90%. Nhiệt dung riêng của nước là 4200 J/(kg·K). Tính thời gian đun.

**Tóm tắt**

U = 220 V

P = 1000 W

V = 1,5 lít, suy ra m = 1,5 kg (vì khối lượng riêng của nước là 1000 kg/m³)

t₁ = 25 °C; t₂ = 100 °C; Δt = 75 K

H = 90% = 0,9

c = 4200 J/(kg·K)

Tìm t = ?

**Lời giải**

Vì ấm dùng đúng hiệu điện thế định mức 220 V nên công suất tiêu thụ đúng bằng 1000 W.

Nhiệt lượng có ích để đun nước:

Q_ích = m·c·Δt

Thay số:

Q_ích = 1,5 × 4200 × 75

Q_ích = 472 500 J

Điện năng ấm tiêu thụ (năng lượng toàn phần):

H = Q_ích/A

Suy ra:

A = Q_ích/H

A = 472 500/0,9 = 525 000 J

Mặt khác:

A = P·t

Suy ra:

t = A/P

t = 525 000/1000 = 525 s

Đổi ra phút:

t = 525/60 = 8,75 phút = 8 phút 45 giây

**Kiểm tra hợp lí:** đun sôi 1,5 lít nước trong khoảng 9 phút bằng ấm 1000 W là hoàn toàn phù hợp với thực tế.

**Đáp số:** t = 525 s = 8 phút 45 giây.

**Lưu ý.**

- Đơn vị của khối lượng phải là kg, của nhiệt độ là K hoặc °C (độ chênh lệch như nhau), của thời gian là s.
- Đừng quên đổi thể tích nước ra khối lượng; đây là lỗi mất điểm phổ biến nhất ở dạng bài nhiệt.
- Khi viết hiệu suất, phải viết dưới dạng số thập phân hoặc phần trăm nhưng thống nhất trong suốt bài.
- Mỗi bước biến đổi một dòng, có dấu suy ra rõ ràng; không nhảy bước từ công thức gốc tới đáp số.
- Kết luận phải là một câu trả lời trọn vẹn, không chỉ là một con số trơ trọi.

## D. Bài tập ví dụ có lời giải (độ khó tăng dần)

### Bài D1. Mạch nối tiếp – rút tỉ số

**Đề bài.** Một đoạn mạch gồm hai điện trở R₁ và R₂ mắc nối tiếp, đặt vào hiệu điện thế U = 12 V thì cường độ dòng điện trong mạch là 0,4 A. Biết R₁ = 10 Ω.

a) Tính điện trở tương đương và R₂.

b) Tính hiệu điện thế hai đầu mỗi điện trở và kiểm tra tỉ số U₁/U₂ có bằng R₁/R₂ không.

**Tóm tắt**

U = 12 V; I = 0,4 A; R₁ = 10 Ω

Tìm R_tđ, R₂, U₁, U₂

**Lời giải**

a) Điện trở tương đương của đoạn mạch nối tiếp:

R_tđ = U/I = 12/0,4 = 30 Ω

Vì mắc nối tiếp:

R_tđ = R₁ + R₂

Suy ra:

R₂ = R_tđ − R₁ = 30 − 10 = 20 Ω

b) Trong mạch nối tiếp, dòng điện qua hai điện trở bằng nhau và bằng I = 0,4 A.

U₁ = I·R₁ = 0,4 × 10 = 4 V

U₂ = I·R₂ = 0,4 × 20 = 8 V

Kiểm tra tổng:

U₁ + U₂ = 4 + 8 = 12 V, đúng bằng U đã cho.

Kiểm tra tỉ số:

U₁/U₂ = 4/8 = 1/2

R₁/R₂ = 10/20 = 1/2

Hai tỉ số bằng nhau, phù hợp với hệ thức U₁/U₂ = R₁/R₂ trong đoạn mạch nối tiếp.

**Đáp số:** R_tđ = 30 Ω; R₂ = 20 Ω; U₁ = 4 V; U₂ = 8 V.

### Bài D2. Đọc đồ thị của hai dây dẫn

**Đề bài.** Khảo sát hai dây dẫn, thu được bảng số liệu:

| U (V) | 1,5 | 3,0 | 4,5 | 6,0 |
|---|---|---|---|---|
| I₁ (A) | 0,075 | 0,15 | 0,225 | 0,30 |
| I₂ (A) | 0,05 | 0,10 | 0,15 | 0,20 |

a) Tính điện trở của mỗi dây dẫn.

b) Vẽ đồ thị U–I của hai dây trên cùng một hệ trục và cho biết đường của dây nào dốc hơn.

c) Nội suy cường độ dòng điện qua mỗi dây khi U = 2,4 V.

**Tóm tắt**

Bảng số liệu U, I₁, I₂

Tìm R₁, R₂, so sánh độ dốc, nội suy I tại U = 2,4 V

**Lời giải**

a) Với dây dẫn thứ nhất, lấy điểm U = 6,0 V; I₁ = 0,30 A:

R₁ = U/I₁ = 6,0/0,30 = 20 Ω

Kiểm tra với điểm U = 1,5 V; I₁ = 0,075 A:

R₁ = 1,5/0,075 = 20 Ω, khớp nhau.

Với dây dẫn thứ hai, lấy điểm U = 6,0 V; I₂ = 0,20 A:

R₂ = 6,0/0,20 = 30 Ω

b) Trên hệ trục có trục hoành là I (A), trục tung là U (V), mỗi dây cho một đường thẳng đi qua gốc toạ độ. Với cùng một giá trị U, dây thứ hai có I nhỏ hơn nên điểm của nó nằm lệch về phía trái; đường của dây thứ hai dốc hơn. Kết luận: đường dốc hơn ứng với điện trở lớn hơn, phù hợp với việc hệ số góc của đồ thị U–I bằng R.

c) Vì cả hai dây đều có U tỉ lệ thuận với I:

I₁ = U/R₁ = 2,4/20 = 0,12 A

I₂ = U/R₂ = 2,4/30 = 0,08 A

**Đáp số:** R₁ = 20 Ω; R₂ = 30 Ω; đường của dây thứ hai dốc hơn; tại U = 2,4 V thì I₁ = 0,12 A và I₂ = 0,08 A.

### Bài D3. Điện năng từ đồ thị công suất

**Đề bài.** Một bếp điện hoạt động theo hai giai đoạn: 5 phút đầu công suất 800 W, 10 phút sau công suất 1200 W. Biết 80% điện năng tiêu thụ chuyển thành nhiệt làm nóng nước, nước nhận nhiệt từ 25 °C đến 100 °C, nhiệt dung riêng của nước là 4200 J/(kg·K).

a) Tính điện năng tiêu thụ, ra J và kWh.

b) Tính khối lượng nước đun được.

c) Nếu giá điện là 2000 đồng một kWh, tính tiền điện cho 15 phút hoạt động trên.

**Tóm tắt**

P₁ = 800 W; t₁ = 300 s

P₂ = 1200 W; t₂ = 600 s

H = 80% = 0,8; Δt = 75 K; c = 4200 J/(kg·K)

Tìm A, m, số tiền

**Lời giải**

a) Điện năng là diện tích dưới đồ thị P–t:

A₁ = P₁·t₁ = 800 × 300 = 240 000 J

A₂ = P₂·t₂ = 1200 × 600 = 720 000 J

A = A₁ + A₂ = 960 000 J

Đổi sang kWh:

A = 960 000/3 600 000 ≈ 0,267 kWh

b) Nhiệt lượng có ích nước nhận được:

Q = H·A = 0,8 × 960 000 = 768 000 J

Mặt khác:

Q = m·c·Δt

Suy ra:

m = Q/(c·Δt)

m = 768 000/(4200 × 75)

m = 768 000/315 000 ≈ 2,44 kg

Ứng với khoảng 2,44 lít nước.

c) Tiền điện:

Số tiền = 0,267 × 2000 = 534 đồng

**Đáp số:** A = 960 000 J ≈ 0,27 kWh; m ≈ 2,44 kg; tiền điện khoảng 534 đồng.

### Bài D4. Kiểm tra đơn vị và ước lượng

**Đề bài.** Hãy kiểm tra và nhận xét:

a) Công thức A = P·t có đúng đơn vị không?

b) Một người đi bộ quãng đường 1,8 km trong 30 phút. Vận tốc tính được là bao nhiêu m/s, có hợp lí không?

c) Một học sinh viết công thức tính quãng đường của vật rơi tự do là s = 5·t² với g = 10 m/s². Kiểm tra đơn vị.

d) Một bếp điện 220 V – 1500 W. Tính dòng điện qua bếp và nhận xét.

**Lời giải**

a) Đơn vị của P là W = J/s, đơn vị của t là s. Tích:

W·s = (J/s)·s = J

Vế phải có đơn vị jun, đúng bằng đơn vị của công A. Công thức hợp lí về đơn vị.

b) Đổi đơn vị:

s = 1,8 km = 1800 m

t = 30 phút = 1800 s

v = s/t = 1800/1800 = 1 m/s

Vận tốc 1 m/s tương ứng 3,6 km/h, đúng với tốc độ đi bộ thông thường của người. Kết quả hợp lí.

c) Trong công thức s = 5·t², hệ số 5 có đơn vị là m/s² (vì g/2 = 10/2 = 5 m/s²). Khi đó:

(m/s²)·s² = m

Vế phải có đơn vị mét, đúng bằng đơn vị của quãng đường. Lưu ý rằng phải hiểu hệ số 5 mang đơn vị m/s², nếu coi 5 là số thuần thì công thức sai đơn vị.

d) Cường độ dòng điện định mức:

I = P/U = 1500/220 ≈ 6,82 A

Nhận xét: dòng điện gần 7 A là hợp lí với bếp điện công suất lớn, và dây dẫn cấp điện cho bếp phải chịu được dòng này. Nếu tính ra 0,68 A thì đã sai một bậc thập phân.

**Đáp số:** a) Đúng đơn vị. b) v = 1 m/s, hợp lí. c) Đúng đơn vị khi hiểu hệ số 5 có đơn vị m/s². d) I ≈ 6,8 A, hợp lí.

### Bài D5. Sai số và ghi kết quả đo

**Đề bài.** Dùng một thước có ĐCNN 0,1 cm đo chiều dài của một vật, thu được các giá trị: 15,4 cm; 15,5 cm; 15,4 cm; 15,6 cm; 15,5 cm. Hãy tính giá trị trung bình, sai số tuyệt đối, sai số tương đối và ghi kết quả đo.

**Lời giải**

Giá trị trung bình:

L_tb = (15,4 + 15,5 + 15,4 + 15,6 + 15,5)/5

L_tb = 77,4/5 = 15,48 cm

Độ lệch của từng lần đo:

|15,4 − 15,48| = 0,08 cm

|15,5 − 15,48| = 0,02 cm

|15,4 − 15,48| = 0,08 cm

|15,6 − 15,48| = 0,12 cm

|15,5 − 15,48| = 0,02 cm

Sai số ngẫu nhiên trung bình:

ΔL_ng = (0,08 + 0,02 + 0,08 + 0,12 + 0,02)/5

ΔL_ng = 0,32/5 = 0,064 cm

Sai số dụng cụ bằng nửa ĐCNN:

ΔL_dc = 0,05 cm

Sai số tuyệt đối:

ΔL = 0,064 + 0,05 = 0,114 cm ≈ 0,1 cm

Làm tròn giá trị trung bình về cùng hàng với sai số:

L_tb ≈ 15,5 cm

Sai số tương đối:

δL = 0,1/15,5 ≈ 0,0065 = 0,65%

Kết quả đo:

L = 15,5 cm ± 0,1 cm, sai số tương đối khoảng 0,65%.

**Đáp số:** L_tb = 15,48 cm; ΔL ≈ 0,1 cm; δL ≈ 0,65%; L = 15,5 cm ± 0,1 cm.

### Bài D6. Trình bày hoàn chỉnh một bài toán tổng hợp

**Đề bài.** Một bếp điện ghi 220 V – 1500 W được dùng ở hiệu điện thế 220 V để đun 2 lít nước từ 30 °C. Hiệu suất của bếp là 85%, nhiệt dung riêng của nước là 4200 J/(kg·K).

a) Tính thời gian cần thiết để nước sôi.

b) Tính điện năng tiêu thụ trong thời gian đó, ra J và kWh.

c) Nếu mỗi ngày đun một lần như trên, tính điện năng tiêu thụ trong 30 ngày và số tiền phải trả với giá 2000 đồng một kWh.

**Tóm tắt**

U = 220 V; P = 1500 W

m = 2 kg; t₁ = 30 °C; t₂ = 100 °C; Δt = 70 K

H = 85% = 0,85; c = 4200 J/(kg·K)

Tìm t, A, A_30ngày, số tiền

**Lời giải**

a) Nhiệt lượng có ích để đun sôi nước:

Q_ích = m·c·Δt = 2 × 4200 × 70

Q_ích = 588 000 J

Nhiệt lượng toàn phần bếp phải cung cấp:

H = Q_ích/Q_toàn phần

Suy ra:

Q_toàn phần = Q_ích/H = 588 000/0,85

Q_toàn phần ≈ 691 765 J

Vì bếp dùng đúng hiệu điện thế định mức nên P = 1500 W. Điện năng bếp tiêu thụ bằng nhiệt lượng toàn phần:

A = Q_toàn phần ≈ 691 765 J

Thời gian:

t = A/P = 691 765/1500

t ≈ 461 s ≈ 7 phút 41 giây

b) Điện năng tiêu thụ đã tính ở trên:

A ≈ 691 765 J

Đổi sang kWh:

A = 691 765/3 600 000 ≈ 0,192 kWh

c) Điện năng trong 30 ngày:

A₃₀ = 0,1922 × 30 ≈ 5,766 kWh

Làm tròn: A₃₀ ≈ 5,77 kWh

Số tiền:

Số tiền = 5,766 × 2000 ≈ 11 532 đồng, làm tròn khoảng 11 530 đồng

Kiểm tra hợp lí: mỗi tháng khoảng 5,8 kWh cho việc đun nước sôi hai lít mỗi ngày là hợp lí, tiền điện hơn mười nghìn đồng một tháng.

**Đáp số:** a) t ≈ 461 s ≈ 7 phút 41 giây. b) A ≈ 691 765 J ≈ 0,19 kWh. c) A₃₀ ≈ 5,77 kWh; khoảng 11 530 đồng.

## E. Bài tập tự luyện (12 bài)

**Bài E1.** Một dây dẫn có điện trở không đổi. Khi đặt hiệu điện thế 6 V thì cường độ dòng điện là 0,25 A.

a) Tính điện trở của dây.

b) Tính cường độ dòng điện khi hiệu điện thế là 9 V.

c) Nêu rõ đại lượng nào tỉ lệ thuận với đại lượng nào trong câu b.

**Bài E2.** Hai điện trở R₁ = 15 Ω và R₂ = 30 Ω được mắc song song vào hiệu điện thế 9 V.

a) Tính cường độ dòng điện qua mỗi điện trở và dòng điện trong mạch chính.

b) Chứng tỏ rằng I₁/I₂ = R₂/R₁.

**Bài E3.** Chứng minh rằng trong một đoạn mạch nối tiếp, tỉ số công suất toả nhiệt trên hai điện trở bằng tỉ số hai điện trở: P₁/P₂ = R₁/R₂. Sau đó áp dụng cho R₁ = 6 Ω và R₂ = 18 Ω, biết dòng điện trong mạch là 0,5 A, hãy tính P₁ và P₂ rồi kiểm tra lại tỉ số.

**Bài E4.** Cho bảng số liệu của một dây dẫn:

| U (V) | 2 | 4 | 6 | 8 |
|---|---|---|---|---|
| I (A) | 0,16 | 0,32 | 0,48 | 0,64 |

a) Vẽ đồ thị U–I.

b) Tính điện trở của dây dẫn.

c) Nội suy cường độ dòng điện khi U = 5 V.

d) Ngoại suy hiệu điện thế khi I = 0,8 A.

**Bài E5.** Một chiếc quạt điện có công suất 55 W, mỗi ngày chạy 6 giờ.

a) Tính điện năng quạt tiêu thụ trong 30 ngày, ra kWh.

b) Tính số tiền điện phải trả cho quạt trong 30 ngày, biết giá 1800 đồng một kWh.

**Bài E6.** Một vật chuyển động đều. Đồ thị quãng đường – thời gian của vật là một đường thẳng đi qua gốc toạ độ và đi qua điểm có toạ độ (5 s; 20 m).

a) Tính vận tốc của vật.

b) Tính quãng đường vật đi được sau 12 s.

c) Nêu ý nghĩa hệ số góc của đồ thị này.

**Bài E7.** Kiểm tra đơn vị của hai công thức sau:

a) Q = I²·R·t.

b) R = ρ·l/S, từ đó suy ra đơn vị của điện trở suất ρ.

**Bài E8.** Một gia đình thay bóng đèn sợi đốt 60 W bằng bóng đèn LED 9 W có cùng độ sáng, mỗi ngày dùng 5 giờ.

a) Tính điện năng tiết kiệm được trong 30 ngày, ra kWh.

b) Với giá 2000 đồng một kWh, mỗi tháng tiết kiệm được bao nhiêu tiền?

**Bài E9.** Dùng thước có ĐCNN 0,1 cm đo chiều dài một vật, thu được: 25,0 cm; 25,2 cm; 24,9 cm; 25,1 cm; 25,3 cm. Tính giá trị trung bình, sai số tuyệt đối, sai số tương đối và ghi kết quả đo.

**Bài E10.** Cho bảng số liệu đo điện trở:

| Lần đo | U (V) | I (A) |
|---|---|---|
| 1 | 3,0 | 0,20 |
| 2 | 6,0 | 0,40 |
| 3 | 9,0 | 0,60 |
| 4 | 12,0 | 0,81 |

Tính điện trở ở mỗi lần đo và giá trị trung bình. Hàng nào có dấu hiệu bất thường, hãy nhận xét.

**Bài E11.** Đổi các đơn vị sau:

a) 36 km/h ra m/s.

b) 1,2 kWh ra J.

c) 2500 Ω ra kΩ.

d) 0,45 A ra mA.

e) 2,5·10⁶ J ra kWh.

**Bài E12.** Một bàn là ghi 220 V – 1000 W được dùng ở hiệu điện thế 220 V trong 20 phút.

a) Tính điện năng tiêu thụ ra J và kWh.

b) Tính nhiệt lượng bàn là toả ra, biết hiệu suất là 100%.

c) Trình bày bài giải theo đúng bốn bước: tóm tắt, đặt ký hiệu, lập luận, kết luận có đơn vị.

## F. Đáp án và hướng dẫn ngắn cho mục E

**E1.** a) R = U/I = 6/0,25 = 24 Ω. b) I' = 9/24 = 0,375 A. c) Vì R không đổi nên I tỉ lệ thuận với U; hiệu điện thế tăng 1,5 lần thì dòng điện cũng tăng 1,5 lần (0,25 × 1,5 = 0,375 A).

**E2.** a) Vì mắc song song nên U₁ = U₂ = 9 V. I₁ = 9/15 = 0,6 A; I₂ = 9/30 = 0,3 A; I = 0,6 + 0,3 = 0,9 A. b) I₁/I₂ = 0,6/0,3 = 2 và R₂/R₁ = 30/15 = 2; hai tỉ số bằng nhau. Lập luận chung: U = I₁R₁ = I₂R₂ nên I₁/I₂ = R₂/R₁.

**E3.** Trong mạch nối tiếp, hai điện trở có cùng dòng điện I. P₁ = I²R₁ và P₂ = I²R₂. Chia vế theo vế được P₁/P₂ = R₁/R₂. Áp dụng: P₁ = 0,5² × 6 = 1,5 W; P₂ = 0,5² × 18 = 4,5 W. Tỉ số P₁/P₂ = 1,5/4,5 = 1/3 và R₁/R₂ = 6/18 = 1/3, khớp nhau.

**E4.** a) Năm điểm (0; 0), (0,16; 2), (0,32; 4), (0,48; 6), (0,64; 8) thẳng hàng qua gốc. b) R = 2/0,16 = 12,5 Ω. c) I = 5/12,5 = 0,4 A. d) U = 0,8 × 12,5 = 10 V.

**E5.** a) A = 55 × 6 × 30 = 9900 Wh = 9,9 kWh. b) Số tiền = 9,9 × 1800 = 17 820 đồng.

**E6.** a) v = 20/5 = 4 m/s. b) s = 4 × 12 = 48 m. c) Hệ số góc của đồ thị s–t bằng vận tốc của vật, đơn vị m/s.

**E7.** a) Đơn vị: A²·Ω·s. Vì Ω = V/A nên A²·(V/A)·s = A·V·s = J, đúng bằng đơn vị của Q. b) Từ R = ρ·l/S suy ra ρ = R·S/l, đơn vị là Ω·m²/m = Ω·m. Vậy điện trở suất có đơn vị ôm mét.

**E8.** a) Công suất tiết kiệm: 60 − 9 = 51 W. Điện năng tiết kiệm: 51 × 5 × 30 = 7650 Wh = 7,65 kWh. b) Số tiền tiết kiệm: 7,65 × 2000 = 15 300 đồng.

**E9.** L_tb = (25,0 + 25,2 + 24,9 + 25,1 + 25,3)/5 = 125,5/5 = 25,10 cm. Độ lệch: 0,10; 0,10; 0,20; 0,00; 0,20 cm, tổng 0,60 cm, trung bình 0,12 cm. Sai số dụng cụ 0,05 cm. ΔL = 0,12 + 0,05 = 0,17 cm ≈ 0,2 cm. δL = 0,2/25,1 ≈ 0,8%. Kết quả: L = 25,1 cm ± 0,2 cm.

**E10.** R₁ = 3,0/0,20 = 15 Ω; R₂ = 6,0/0,40 = 15 Ω; R₃ = 9,0/0,60 = 15 Ω; R₄ = 12,0/0,81 ≈ 14,8 Ω. Trung bình ≈ (15 + 15 + 15 + 14,8)/4 ≈ 14,95 Ω, làm tròn 15 Ω. Hàng 4 lệch không đáng kể (khoảng 0,2 Ω, tương đương sai số đọc 0,01 A), có thể giữ lại; nếu lệch trên 1 Ω thì phải kiểm tra lại phép đọc và có thể loại bỏ.

**E11.** a) 36/3,6 = 10 m/s. b) 1,2 × 3,6·10⁶ = 4,32·10⁶ J. c) 2500/1000 = 2,5 kΩ. d) 0,45 × 1000 = 450 mA. e) 2,5·10⁶/3,6·10⁶ ≈ 0,69 kWh.

**E12.** a) t = 20 phút = 1200 s. A = P·t = 1000 × 1200 = 1 200 000 J = 0,333 kWh. b) Với hiệu suất 100% thì Q = A = 1 200 000 J. c) Bài trình bày phải có: tóm tắt với U, P, t và đơn vị đã đổi; ký hiệu A, Q; lập luận viết công thức gốc rồi thay số từng dòng; kết luận có đơn vị kèm nhận xét rằng nhiệt lượng toả ra bằng điện năng tiêu thụ khi hiệu suất bằng 100%.

## G. Bài tập nâng cao kiểu đề thi HSG (4 bài, có lời giải đầy đủ)

### Bài G1. Biến trở và công suất – kỹ thuật lập bảng, rút tỉ số và chặn trên

**Đề bài.** Một đoạn mạch gồm điện trở R₀ = 3 Ω mắc nối tiếp với một biến trở R. Hai đầu đoạn mạch được mắc vào nguồn có hiệu điện thế không đổi U = 12 V. Bỏ qua điện trở của dây nối và nguồn.

a) Lập bảng giá trị công suất tiêu thụ trên biến trở P_R ứng với R = 1 Ω; 2 Ω; 3 Ω; 4 Ω; 6 Ω; 9 Ω.

b) Vẽ dạng đồ thị P_R theo R và nhận xét.

c) Chứng minh rằng công suất trên biến trở đạt giá trị lớn nhất khi R = R₀ và tính giá trị lớn nhất đó.

d) Tìm hai giá trị khác nhau của R cho cùng một giá trị công suất P_R = 9 W.

**Tóm tắt**

R₀ = 3 Ω; U = 12 V

Tìm P_R theo R; P_R max; các giá trị R ứng với P_R = 9 W

**Lời giải**

a) Cường độ dòng điện trong mạch:

I = U/(R₀ + R)

Công suất trên biến trở:

P_R = I²·R = U²·R/(R₀ + R)²

Với U = 12 V và R₀ = 3 Ω:

P_R = 144·R/(R + 3)²

Lần lượt thay số:

R = 1 Ω: I = 12/4 = 3 A; P_R = 3² × 1 = 9 W

R = 2 Ω: I = 12/5 = 2,4 A; P_R = 2,4² × 2 = 11,52 W

R = 3 Ω: I = 12/6 = 2 A; P_R = 2² × 3 = 12 W

R = 4 Ω: I = 12/7 ≈ 1,714 A; P_R ≈ 1,714² × 4 ≈ 11,76 W

R = 6 Ω: I = 12/9 ≈ 1,333 A; P_R ≈ 1,333² × 6 ≈ 10,67 W

R = 9 Ω: I = 12/12 = 1 A; P_R = 1² × 9 = 9 W

Bảng kết quả:

| R (Ω) | 1 | 2 | 3 | 4 | 6 | 9 |
|---|---|---|---|---|---|---|
| I (A) | 3 | 2,4 | 2 | 1,714 | 1,333 | 1 |
| P_R (W) | 9 | 11,52 | 12 | 11,76 | 10,67 | 9 |

b) Đồ thị P_R theo R là một đường cong: tăng từ 9 W tại R = 1 Ω lên cực đại 12 W tại R = 3 Ω, sau đó giảm dần; tại R = 9 Ω công suất trở lại 9 W bằng giá trị ở R = 1 Ω. Nhận xét: P_R không tỉ lệ thuận cũng không tỉ lệ nghịch đơn thuần với R, vì mẫu số chứa (R + R₀)².

c) Từ biểu thức:

P_R = U²·R/(R + R₀)²

Ta có bất đẳng thức đúng với mọi R dương:

(R + R₀)² ≥ 4·R·R₀

Vì (R + R₀)² − 4RR₀ = (R − R₀)² ≥ 0.

Do đó:

P_R = U²·R/(R + R₀)² ≤ U²·R/(4RR₀) = U²/(4R₀)

Dấu bằng xảy ra khi (R − R₀)² = 0, tức R = R₀ = 3 Ω.

Giá trị lớn nhất:

P_max = U²/(4R₀) = 144/(4 × 3) = 144/12 = 12 W

Kết quả khớp với bảng ở câu a.

d) Giải phương trình P_R = 9 W:

144·R/(R + 3)² = 9

Chia hai vế cho 9:

16R/(R + 3)² = 1

Suy ra:

16R = (R + 3)²

16R = R² + 6R + 9

R² − 10R + 9 = 0

Phân tích thành nhân tử:

(R − 1)(R − 9) = 0

Vậy R = 1 Ω hoặc R = 9 Ω, đúng như hai giá trị đã thấy trong bảng. Nhận xét: ứng với mỗi giá trị công suất nhỏ hơn P_max luôn có hai giá trị của biến trở, một nhỏ hơn R₀ và một lớn hơn R₀.

**Đáp số:** a) Bảng như trên. b) Đồ thị dạng đường cong có cực đại. c) P_max = 12 W khi R = R₀ = 3 Ω. d) R = 1 Ω hoặc R = 9 Ω.

### Bài G2. Đồ thị vận tốc – thời gian dạng bậc thang

**Đề bài.** Một vật chuyển động theo ba giai đoạn liên tiếp, được mô tả bằng đồ thị vận tốc theo thời gian:

- Giai đoạn 1: từ t = 0 đến t = 5 s, vật chuyển động đều với vận tốc 4 m/s.
- Giai đoạn 2: từ t = 5 s đến t = 8 s, vật dừng lại (vận tốc bằng 0).
- Giai đoạn 3: từ t = 8 s đến t = 12 s, vật chuyển động đều với vận tốc 6 m/s theo chiều cũ.

a) Tính quãng đường vật đi được trong mỗi giai đoạn và tổng quãng đường.

b) Tính tốc độ trung bình của vật trên toàn bộ hành trình.

c) Vẽ dạng đồ thị quãng đường – thời gian tương ứng và nêu rõ hệ số góc của từng đoạn.

d) Giải thích vì sao tổng diện tích các hình chữ nhật dưới đồ thị v–t bằng quãng đường đi được.

**Tóm tắt**

v₁ = 4 m/s trong t₁ = 5 s

v₂ = 0 trong t₂ = 3 s

v₃ = 6 m/s trong t₃ = 4 s

Tìm s₁, s₂, s₃, s, v_tb

**Lời giải**

a) Quãng đường từng giai đoạn:

s₁ = v₁·t₁ = 4 × 5 = 20 m

s₂ = v₂·t₂ = 0 × 3 = 0 m

s₃ = v₃·t₃ = 6 × 4 = 24 m

Tổng quãng đường:

s = s₁ + s₂ + s₃ = 20 + 0 + 24 = 44 m

b) Tổng thời gian chuyển động:

t = t₁ + t₂ + t₃ = 5 + 3 + 4 = 12 s

Tốc độ trung bình trên toàn hành trình:

v_tb = s/t = 44/12 ≈ 3,67 m/s

Lưu ý: tốc độ trung bình này nhỏ hơn giá trị trung bình cộng của các vận tốc, vì thời gian dừng cũng được tính vào mẫu số.

c) Đồ thị s–t gồm ba đoạn:

- Từ t = 0 đến t = 5 s: đoạn thẳng từ s = 0 lên s = 20 m, hệ số góc bằng 4 m/s.
- Từ t = 5 s đến t = 8 s: đoạn nằm ngang ở mức s = 20 m, hệ số góc bằng 0, vật dừng.
- Từ t = 8 s đến t = 12 s: đoạn thẳng từ s = 20 m lên s = 44 m, hệ số góc bằng 6 m/s.

d) Ở mỗi giai đoạn vận tốc không đổi, nên quãng đường bằng tích vận tốc và thời gian. Trên đồ thị v–t, tích đó đúng bằng diện tích hình chữ nhật có chiều cao là vận tốc và chiều rộng là thời gian. Vì đơn vị của tích (m/s)·s chính là mét, tổng diện tích dưới đồ thị bằng tổng quãng đường.

**Đáp số:** a) s₁ = 20 m; s₂ = 0; s₃ = 24 m; s = 44 m. b) v_tb ≈ 3,67 m/s. c) Ba đoạn với hệ số góc 4 m/s; 0; 6 m/s. d) Vì diện tích hình chữ nhật dưới đồ thị v–t bằng tích v·t, tức quãng đường.

### Bài G3. Xử lí số liệu thực hành đo tiêu cự thấu kính hội tụ

**Đề bài.** Trong bài thực hành đo tiêu cự của thấu kính hội tụ, một học sinh đặt vật và màn ảnh sao cho ảnh hiện rõ nét trên màn và có kích thước bằng vật. Khi đó khoảng cách từ vật đến thấu kính bằng khoảng cách từ ảnh đến thấu kính và bằng hai lần tiêu cự, tức d = d' = 2f, suy ra f = d/2.

Kết quả đo khoảng cách d bằng thước có ĐCNN 0,1 cm:

| Lần đo | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| d (cm) | 20,0 | 20,2 | 19,8 | 20,1 | 20,4 |

a) Tính giá trị trung bình của d.

b) Tính sai số tuyệt đối và sai số tương đối của phép đo d.

c) Tính tiêu cự f và sai số của f. Ghi kết quả đo tiêu cự.

d) Nêu một nguyên nhân gây sai số hệ thống và một nguyên nhân gây sai số ngẫu nhiên trong phép đo này.

**Lời giải**

a) Giá trị trung bình:

d_tb = (20,0 + 20,2 + 19,8 + 20,1 + 20,4)/5

d_tb = 100,5/5 = 20,10 cm

b) Độ lệch của từng lần đo so với trung bình:

|20,0 − 20,10| = 0,10 cm

|20,2 − 20,10| = 0,10 cm

|19,8 − 20,10| = 0,30 cm

|20,1 − 20,10| = 0,00 cm

|20,4 − 20,10| = 0,30 cm

Sai số ngẫu nhiên trung bình:

Δd_ng = (0,10 + 0,10 + 0,30 + 0,00 + 0,30)/5

Δd_ng = 0,80/5 = 0,16 cm

Sai số dụng cụ bằng nửa ĐCNN:

Δd_dc = 0,1/2 = 0,05 cm

Sai số tuyệt đối của d:

Δd = 0,16 + 0,05 = 0,21 cm ≈ 0,2 cm

Sai số tương đối của d:

δd = Δd/d_tb = 0,21/20,10

δd ≈ 0,0104 = 1,04% ≈ 1,0%

c) Tiêu cự:

f = d_tb/2 = 20,10/2 = 10,05 cm

Vì f = d/2 với hệ số 1/2 là số đúng, sai số tương đối của f bằng sai số tương đối của d:

δf = δd ≈ 1,04%

Sai số tuyệt đối của f:

Δf = f·δf = 10,05 × 0,0104 ≈ 0,105 cm ≈ 0,1 cm

Làm tròn giá trị trung bình về cùng hàng với sai số:

f ≈ 10,1 cm

Kết quả đo tiêu cự:

f = 10,1 cm ± 0,1 cm với sai số tương đối khoảng 1%.

Kiểm tra bằng công thức thấu kính: với d = d' = 20,10 cm thì 1/f = 1/20,10 + 1/20,10 = 2/20,10, suy ra f = 10,05 cm, khớp với kết quả trên.

d) Sai số hệ thống: thước bị lệch vạch số 0, hoặc học sinh xác định vị trí ảnh rõ nét bằng mắt nên luôn đánh giá lệch về một phía; giá đỡ thấu kính không vuông góc với băng quang học. Sai số ngẫu nhiên: mỗi lần đọc vị trí vật và màn khác nhau một chút, do mắt ước lượng độ nét không hoàn toàn giống nhau.

**Đáp số:** d_tb = 20,10 cm; Δd ≈ 0,2 cm; δd ≈ 1,0%; f = 10,1 cm ± 0,1 cm (δf ≈ 1%).

### Bài G4. Đường đặc trưng vôn – ampe của bóng đèn dây tóc

**Đề bài.** Khảo sát một bóng đèn dây tóc, thu được bảng số liệu:

| U (V) | 2,0 | 3,0 | 4,2 | 5,6 |
|---|---|---|---|---|
| I (A) | 0,40 | 0,50 | 0,60 | 0,70 |

a) Tính điện trở của đèn ứng với mỗi giá trị và nhận xét.

b) Vẽ đồ thị U–I. Đèn có tuân theo định luật Ôm không? Giải thích.

c) Nội suy cường độ dòng điện khi U = 3,5 V và tính điện trở của đèn tại điểm đó.

d) Mắc bóng đèn nối tiếp với điện trở R₀ = 4 Ω rồi nối vào nguồn có hiệu điện thế không đổi 8 V. Dùng số liệu đã cho, xác định cường độ dòng điện trong mạch và hiệu điện thế hai đầu đèn. Tính công suất tiêu thụ của đèn và của R₀.

**Lời giải**

a) Áp dụng R = U/I cho từng hàng:

Hàng 1: R = 2,0/0,40 = 5,0 Ω

Hàng 2: R = 3,0/0,50 = 6,0 Ω

Hàng 3: R = 4,2/0,60 = 7,0 Ω

Hàng 4: R = 5,6/0,70 = 8,0 Ω

Nhận xét: điện trở của đèn tăng dần từ 5,0 Ω lên 8,0 Ω khi hiệu điện thế tăng. Đó là do nhiệt độ dây tóc tăng làm điện trở tăng.

b) Đồ thị U–I có bốn điểm (0,40; 2,0), (0,50; 3,0), (0,60; 4,2), (0,70; 5,6). Các điểm này không nằm trên một đường thẳng đi qua gốc toạ độ, mà độ dốc tăng dần. Vì U không tỉ lệ thuận với I, bóng đèn không tuân theo định luật Ôm trong khoảng khảo sát.

c) Nội suy tuyến tính giữa hai điểm (0,50; 3,0) và (0,60; 4,2):

Hệ số góc của đoạn này:

a = (0,60 − 0,50)/(4,2 − 3,0) = 0,10/1,2 ≈ 0,0833 A/V

Tại U = 3,5 V:

I = 0,50 + 0,0833 × (3,5 − 3,0)

I = 0,50 + 0,0833 × 0,5 ≈ 0,542 A

Điện trở của đèn tại điểm này:

R = 3,5/0,542 ≈ 6,46 Ω

Giá trị này nằm giữa 6,0 Ω và 7,0 Ω, hợp lí.

d) Gọi I là cường độ dòng điện trong mạch và U_đ là hiệu điện thế hai đầu đèn. Vì mắc nối tiếp:

U_đ = 8 − 4·I

Đường đặc trưng của đèn cho quan hệ giữa U_đ và I. Ta đi tìm giao điểm của đường thẳng U_đ = 8 − 4I với đường đặc trưng.

Xét hai điểm số liệu gần giao điểm là (0,60 A; 4,2 V) và (0,70 A; 5,6 V). Trên đoạn này, đường đặc trưng có dạng:

U_đ = 4,2 + (5,6 − 4,2)·(I − 0,60)/(0,70 − 0,60)

U_đ = 4,2 + 14·(I − 0,60)

Cho hai biểu thức bằng nhau:

4,2 + 14·(I − 0,60) = 8 − 4·I

4,2 + 14I − 8,4 = 8 − 4I

14I − 4,2 = 8 − 4I

18I = 12,2

I ≈ 0,678 A

Hiệu điện thế hai đầu đèn:

U_đ = 8 − 4 × 0,678 = 8 − 2,712

U_đ ≈ 5,29 V

Kiểm tra lại bằng đường đặc trưng:

U_đ = 4,2 + 14 × (0,678 − 0,60) = 4,2 + 14 × 0,078

U_đ ≈ 4,2 + 1,09 = 5,29 V, khớp nhau.

Công suất của đèn:

P_đ = U_đ·I = 5,29 × 0,678 ≈ 3,59 W

Công suất của R₀:

P₀ = I²·R₀ = 0,678² × 4

P₀ ≈ 0,460 × 4 ≈ 1,84 W

Kiểm tra tổng công suất:

P_đ + P₀ ≈ 3,59 + 1,84 = 5,43 W

Công suất của nguồn:

P = U·I = 8 × 0,678 ≈ 5,42 W

Hai giá trị xấp xỉ nhau, phù hợp với định luật bảo toàn năng lượng.

**Đáp số:** a) R lần lượt 5,0 Ω; 6,0 Ω; 7,0 Ω; 8,0 Ω, tăng dần theo hiệu điện thế. b) Đèn không tuân theo định luật Ôm vì điện trở thay đổi. c) I ≈ 0,54 A; R ≈ 6,5 Ω. d) I ≈ 0,68 A; U_đ ≈ 5,3 V; P_đ ≈ 3,6 W; P₀ ≈ 1,84 W.

## H. Lỗi thường gặp và ghi chú sư phạm

**Nhóm lỗi về biến đổi đại số và tỉ lệ**

1. Nhầm tỉ lệ thuận với tỉ lệ nghịch khi lập tỉ số. Cách phòng: luôn viết công thức gốc ra giấy trước khi lập tỉ số, không suy diễn bằng cảm giác.
2. Áp dụng tỉ lệ nghịch I₂/I₁ = R₁/R₂ cho mạch có biến trở, trong khi dòng điện tỉ lệ nghịch với tổng R₀ + R. Cách phòng: kiểm tra xem đại lượng ở mẫu có thật sự chỉ là đại lượng đang xét không.
3. Quên bình phương khi đại lượng tỉ lệ với bình phương, ví dụ P = I²R.
4. Bỏ mất căn khi rút từ v = √(2gh).
5. Làm tròn quá sớm ở bước trung gian rồi thay vào bước sau, làm kết quả lệch.
6. Nhân hoặc chia hai vế mà quên điều kiện đại lượng khác không.

**Nhóm lỗi về đồ thị**

7. Không ghi tên và đơn vị trên trục toạ độ.
8. Chia vạch không đều hoặc chọn tỉ lệ xích khiến đồ thị dồn vào một góc.
9. Nối các điểm đo bằng đường gấp khúc thay vì đường thẳng hoặc đường trơn phù hợp xu hướng.
10. Nhầm hệ số góc của đồ thị U–I (bằng R) với hệ số góc của đồ thị I–U (bằng 1/R).
11. Đọc giá trị nội suy bằng mắt trên hình vẽ nhỏ rồi ghi kết quả với nhiều chữ số hơn mức cho phép.
12. Ngoại suy quá xa vùng số liệu rồi coi đó là kết quả đo.

**Nhóm lỗi về đơn vị và hợp lí**

13. Quên đổi phút ra giây, km/h ra m/s, lít ra kg, cm² ra m².
14. Không đổi kWh ra J khi thay vào công thức tính theo đơn vị SI.
15. Viết kết quả không có đơn vị, hoặc ghi đơn vị sai (dùng W cho công, dùng J cho công suất).
16. Chấp nhận kết quả vô lí như hiệu suất lớn hơn 100%, điện trở bằng 0 khi mạch vẫn có dòng điện, dòng điện hàng trăm ampe qua đèn pin.
17. Không kiểm tra tổng các hiệu điện thế trong mạch nối tiếp hoặc tổng các dòng điện trong mạch song song.

**Nhóm lỗi về sai số và thực hành**

18. Cộng đại số các độ lệch thay vì lấy giá trị tuyệt đối, khiến sai số ngẫu nhiên gần bằng 0 một cách vô lí.
19. Bỏ qua sai số dụng cụ, chỉ tính sai số ngẫu nhiên.
20. Ghi kết quả quá nhiều chữ số, ví dụ U = 5,900 V ± 0,1 V.
21. Giữ lại số liệu bất thường do đọc nhầm mà không kiểm tra, hoặc tự ý bỏ mà không ghi lí do.
22. Không đổi đơn vị của số liệu trước khi tính trung bình, ví dụ trộn lẫn cm và m trong cùng một bảng.

**Nhóm lỗi về trình bày**

23. Không có phần tóm tắt, hoặc tóm tắt thiếu đơn vị và thiếu đại lượng cần tìm.
24. Nhảy bước từ công thức gốc tới đáp số, không cho thấy quá trình biến đổi.
25. Dùng cùng một ký hiệu cho hai đại lượng khác nhau (ví dụ dùng R cho cả điện trở và bán kính).
26. Kết luận chỉ ghi một con số trơ trọi, không có đơn vị và không trả lời đúng câu hỏi.
27. Vẽ hình thiếu ký hiệu, ký hiệu trên hình không khớp với tóm tắt.
28. Viết chữ quá ẩu hoặc gạch xoá lem nhem khiến giám khảo không đọc được bước lập luận.

**Ghi chú sư phạm**

- Nên dành hai buổi đầu của khoá bồi dưỡng cho chuyên đề này, trong đó buổi thứ hai là buổi thực hành đo và xử lí số liệu thật, không chỉ làm bài trên giấy.
- Khi chữa bài, hãy yêu cầu học sinh tự chấm chéo theo khung bốn bước ở Dạng 6. Cách này giúp các em nhớ quy cách trình bày nhanh hơn là nghe giảng lại.
- Với mỗi dạng, nên cho một bài "bẫy" nhỏ để học sinh tự phát hiện lỗi: một bài quên đổi kWh ra J, một bài nhầm hệ số góc, một bài trộn lẫn cm và m.
- Khuyến khích học sinh viết nháp phần tóm tắt và công thức gốc trước khi bấm máy tính; đây là thói quen phân biệt học sinh giỏi với học sinh chỉ biết thay số.
- Việc kiểm tra đơn vị nên được luyện như một phản xạ: sau mỗi kết quả, tự hỏi "đơn vị này có đúng không, con số này có hợp lí với đời sống không".
- Cần nhắc học sinh rằng máy tính bỏ túi không sửa được lỗi tư duy; sai một tỉ số thì máy tính vẫn cho ra con số trông rất "đẹp".
- Với học sinh yếu hơn, cho phép dùng bảng đổi đơn vị và bảng hằng số trong lúc luyện tập, nhưng đến giai đoạn thi thì phải nhớ.
- Đánh giá kết quả chuyên đề này không chỉ bằng đáp số đúng, mà bằng tỉ lệ bài có đủ tóm tắt, có đơn vị và có kết luận.
