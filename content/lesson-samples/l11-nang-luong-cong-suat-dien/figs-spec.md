# Đặc tả 4 hình — Bài 25. Năng lượng điện và công suất điện (lesson 44)

Mốc trong `theory.src.html`: `<!--FIG1-->` … `<!--FIG4-->`, đánh số theo thứ tự xuất hiện. Mỗi hình bọc
`<figure class="fig" data-tl="1">…<figcaption>Hình n. …</figcaption></figure>`. Quy ước chung (theo
`references/hinh-svg.md`): viewBox rộng ≤ 440; chữ ≥ 11 px; nét thân vật và chữ `currentColor`; marker mũi
tên mỗi hình một tiền tố (`f1-`, `f2-`…); chỉ số dưới bằng `<tspan dy="4" font-size="9">` rồi `<tspan dy="-4">`;
**không** đặt `$…$` trong `<text>`. Màu: đỏ `#f87171` = năng lượng/công suất nguồn phát; xanh dương
`#38bdf8` = phần có ích (mạch ngoài); cam `#fb923c` = hao phí/nhiệt; xanh lá `#34d399` = kết quả/đồ thị.
**Figcaption ≤ 12 từ mỗi hình** (bài đang 2.248 từ hiện ngay, trần 2.300 — caption dài sẽ vượt).

---

## FIG1 — Công tơ điện đếm năng lượng của mọi thiết bị (mục I, sau đoạn "Câu hỏi để nghĩ")

**Mục đích:** cho thấy công tơ đứng giữa nguồn và các thiết bị, hiển thị **kWh** (năng lượng), còn mỗi thiết
bị mang nhãn **W/kW** (công suất) — đặt nền cho câu dự đoán ngay bên dưới.

**viewBox:** `0 0 440 230`.

**Đối tượng và vị trí (tọa độ tương đối):**
1. Trái (x ≈ 12–70, y ≈ 90–140): ổ cắm/đường dây vào, nhãn `Lưới điện` (text-anchor start, x = 12, y = 84).
2. Giữa-trái (x ≈ 90–210, y ≈ 70–160): **công tơ điện** — hộp chữ nhật bo góc, bên trong một "màn hình"
   chữ nhật nhỏ (x ≈ 105–195, y ≈ 95–120) ghi `0312,4 kWh` (font-family monospace, 13 px, text-anchor middle
   tại x = 150). Dưới màn hình nhãn `Công tơ điện` (11 px, middle, x = 150, y = 150).
3. Dây từ lưới vào công tơ: đoạn thẳng y = 115 từ x = 70 đến x = 90. Dây từ công tơ ra: từ x = 210, y = 115
   rẽ ba nhánh (đường gấp khúc) tới ba thiết bị ở cột phải.
4. Cột phải (x ≈ 260–430), ba thiết bị xếp dọc, mỗi cái có hình đơn giản + nhãn hai dòng (tên + nhãn công suất):
   - y ≈ 40: **bóng đèn** (vòng tròn r = 14 + đuôi nhỏ), nhãn `Đèn` / `100 W` (text-anchor start, x = 300).
   - y ≈ 115: **trục chính CNC** (hình chữ nhật đứng 24×36 + mũi khoan tam giác phía dưới), nhãn
     `Trục chính CNC` / `2,2 kW` (x = 300).
   - y ≈ 190: **ấm siêu tốc** (hình thang + quai), nhãn `Ấm đun` / `1800 W` (x = 300).
5. Mũi tên nhỏ màu đỏ `#f87171` dọc dây vào công tơ (chiều từ lưới → công tơ) và trên mỗi nhánh ra (chiều
   công tơ → thiết bị): chiều dòng năng lượng **đi từ lưới qua công tơ tới thiết bị**, không ngược lại.
6. Ghi chú góc trên trái (x = 12, y = 20, 11 px): `kWh = năng lượng đã dùng`; góc dưới phải, dưới ấm
   (x = 300, y = 222): `W, kW = công suất`.

**Ràng buộc kiểm:** nhãn thiết bị không chồng dây (các nhánh ra kết thúc ở x ≈ 258, nhãn bắt đầu x = 300);
chữ `0312,4 kWh` nằm gọn trong màn hình; mọi text-anchor middle cách mép ≥ 40 px.

**figcaption:** `Hình 1. Công tơ đếm kWh; mỗi thiết bị ghi công suất W.`
**aria-label:** `Sơ đồ lưới điện qua công tơ điện hiển thị 0312,4 kWh tới ba thiết bị: đèn 100 W, trục chính CNC 2,2 kW, ấm đun 1800 W`.
**data-exp:** `tn-l11-nang-luong-dien-01` (đặt trên `<figure>`).

---

## FIG2 — Dòng năng lượng của nguồn: EI = UI + I²r (mục II.3, sau danh sách bullet)

**Mục đích:** nhìn thấy công suất nguồn phát ra **chia làm hai phần**: mạch ngoài nhận UI, nguồn tự nóng I²r.
Đây là hình cho "bẫy 2" (công suất nguồn ≠ công suất mạch ngoài).

**viewBox:** `0 0 440 210`.

**Đối tượng:**
1. Trái (x ≈ 15–135, y ≈ 60–150): **khối nguồn** — hộp bo góc, viền `currentColor`, bên trong ký hiệu pin
   (hai vạch dài/ngắn) và nhãn `Nguồn` (13 px, middle, x = 75, y = 85), dòng dưới `ℰ, r` viết bằng chữ
   thường: dùng ký tự `ℰ` (U+2130) trong `<text>` hoặc chữ in nghiêng `E` kèm `r` — nhãn `ℰ, r` (11 px, middle,
   x = 75, y = 105).
2. Phải (x ≈ 300–425, y ≈ 60–150): **khối mạch ngoài** — hộp bo góc, bên trong ký hiệu điện trở zíc-zắc
   ngang, nhãn `Mạch ngoài` (13 px, middle, x = 362, y = 85) và `R` (11 px, middle, x = 362, y = 140).
3. **Mũi tên to màu đỏ `#f87171`** từ mép phải khối nguồn (x = 135, y = 105) đi ngang sang phải tới x = 215;
   nhãn phía trên (y = 92, middle, x = 175): `P nguồn = ℰI` (12 px, màu đỏ).
4. Tại x = 215 mũi tên **rẽ làm hai**:
   - nhánh **xanh dương `#38bdf8`**, to hơn (stroke-width ≈ 6), tiếp tục ngang tới mép trái khối mạch ngoài
     (x = 300, y = 105), đầu mũi tên chạm hộp; nhãn phía dưới (x = 257, y = 125, middle, 12 px, xanh dương):
     `Có ích: UI`.
   - nhánh **cam `#fb923c`**, mảnh hơn (stroke-width ≈ 3), từ (215, 105) cong lên trên về phía **khối nguồn**
     (ví dụ path cong kết thúc tại (110, 60) — đầu mũi tên chạm mép trên khối nguồn, vì nhiệt toả **trong
     nguồn**); nhãn cạnh nhánh (x = 150, y = 40, start, 12 px, cam): `Hao phí: I²r` — viết `I` rồi
     `<tspan dy="-5" font-size="9">2</tspan><tspan dy="5">r</tspan>` (chỉ số trên).
   - Vài vạch sóng nhiệt nhỏ (3 đường lượn) màu cam cạnh mép trên khối nguồn, gần (90–120, 50–58).
5. Dòng chữ tổng kết ở đáy (x = 220, y = 190, middle, 12 px, `currentColor`): `ℰI = UI + I²r` (chỉ số trên
   bằng tspan như trên).
6. Bề rộng (stroke-width) ba mũi tên **tỉ lệ công suất của bài toán mẫu**: đỏ 24 W ≈ 9 px, xanh 20 W ≈ 7,5 px,
   cam 4 W ≈ 1,5 px → làm tròn 9 / 7 / 2 px (xanh + cam ≈ đỏ). Marker mũi tên đặt tiền tố `f2-r`, `f2-b`, `f2-o`.

**Ràng buộc kiểm:** nhánh xanh và cam đều **xuất phát từ cùng điểm (215, 105)**; đầu mũi cam nằm trên khối
nguồn (x trong [15,135], y = 60); đầu mũi xanh chạm x = 300; không nhãn nào chồng mũi tên (`Có ích: UI` nằm
dưới trục y = 105 ít nhất 15 px).

**figcaption:** `Hình 2. Nguồn phát ℰI: mạch ngoài nhận UI, nguồn nóng I²r.` (trong figcaption HTML được dùng
`$\mathcal{E}I$`, `$I^2r$` — figcaption không phải `<text>` SVG).
**aria-label:** `Sơ đồ dòng năng lượng: công suất nguồn EI tách thành phần có ích UI tới mạch ngoài và phần hao phí I bình phương r toả nhiệt trong nguồn`.

---

## FIG3 — Đồ thị hiệu suất H theo R với r = 1,0 Ω (mục II.4, sau câu "So với công thức … Khớp.")

**Mục đích:** bốn điểm đo của thí nghiệm pin nằm đúng trên đường cong H = R/(R + 1); thấy H tăng dần, tiến
tới 100 % không chạm; điểm R = r cho H = 50 %.

**viewBox:** `0 0 440 260`.

**Trục:** gốc O tại (50, 215). Trục ngang R (Ω) từ x = 50 đến x = 410, **chia tuyến tính**: 0 → 10 Ω ứng với
50 → 410 px, tức **36 px / Ω** (vạch và số tại R = 0, 2, 4, 6, 8, 10 → x = 50, 122, 194, 266, 338, 410).
Trục dọc H (%) từ y = 215 (0 %) đến y = 35 (100 %): **1,8 px / %** (vạch và số tại 0, 25, 50, 75, 100 →
y = 215, 170, 125, 80, 35). Nhãn trục: `R (Ω)` tại (405, 240, end); `H (%)` tại (14, 28, start). Số trục 11 px.

**Đường cong (xanh lá `#34d399`, stroke-width 2.5):** polyline từ R = 0 tới R = 10, bước 0,25 Ω, mỗi điểm
`x = 50 + 36·R`, `y = 215 − 1,8·100·R/(R + 1)`. Ví dụ phải đúng: R = 1 → (86, 125); R = 2 → (122, 95);
R = 4 → (194, 71); R = 9 → (374, 53); R = 10 → (410, 51.4).

**Đường tiệm cận:** nét đứt (`stroke-dasharray 4 4`, `currentColor`, opacity 0.5) ngang y = 35 từ x = 50
tới 410, nhãn `100 %` (11 px) đã có trên trục; thêm nhãn nhỏ `không bao giờ chạm` (10 px, start, x = 250,
y = 30).

**Bốn điểm đo** (chấm đỏ `#f87171` r = 4,5) — **tọa độ phải thoả y = 215 − 180·R/(R + 1)**:
| R (Ω) | H | x | y |
|---|---|---|---|
| 1,0 | 50 % | 86 | 125 |
| 2,0 | 66,7 % | 122 | 95 |
| 4,0 | 80 % | 194 | 71 |
| 9,0 | 90 % | 374 | 53 |
Nhãn cạnh mỗi chấm (10 px, start, lệch +7 px sang phải, −6 px lên trên): `50 %`, `67 %`, `80 %`, `90 %`.
(Nhãn `67 %` đặt **dưới-phải** chấm (+7, +14) để không chồng nhãn `50 %`/đường cong; kiểm bằng mắt.)

**Đánh dấu R = r:** đoạn nét đứt mảnh dọc từ (86, 215) lên (86, 125) và ngang từ (50, 125) tới (86, 125);
nhãn `R = r` (10 px, start, x = 90, y = 212).

**Ràng buộc kiểm (assert bằng script):** với mỗi chấm, `abs(y − (215 − 180·R/(R+1))) < 0.6`; khoảng cách vạch
trục ngang đều 72 px; vạch trục dọc đều 45 px.

**figcaption:** `Hình 3. H = R/(R + r) với r = 1 Ω: bốn điểm đo nằm đúng trên đường cong.` (trong HTML viết
`$H = R/(R + r)$`, `$r = 1\ \Omega$`).
**aria-label:** `Đồ thị hiệu suất nguồn theo điện trở mạch ngoài, r bằng 1 ôm: đường cong tăng dần tiến tới 100 phần trăm, bốn điểm đo tại R bằng 1, 2, 4, 9 ôm cho H bằng 50, 67, 80, 90 phần trăm`.
**data-exp:** `tn-l11-nang-luong-dien-03` (đặt trên `<figure>`).

---

## FIG4 — Sơ đồ mạch bài toán mẫu (mục V, sau hộp Đề bài)

**Mục đích:** học sinh thấy mạch kín một vòng: nguồn (ℰ = 12 V, r = 1,0 Ω) và điện trở R = 5,0 Ω, chiều dòng
điện và chỗ đo U.

**viewBox:** `0 0 440 200`.

**Đối tượng:**
1. Vòng mạch chữ nhật: góc (70, 40) – (370, 160), nét `currentColor` 2 px.
2. **Nguồn** nằm trên cạnh trái (x = 70), giữa cạnh (y ≈ 100): ký hiệu pin — vạch dài (cực +, dài 28 px) ở
   **trên**, vạch ngắn (cực −, dài 14 px) ở **dưới**, cách nhau 8 px; cạnh trái ngắt ở đoạn đó. Nhãn `+` nhỏ
   trên vạch dài (x = 56, y = 92), `−` dưới vạch ngắn (x = 56, y = 118). Nhãn bên trái ngoài vòng (x = 12,
   start): `ℰ = 12 V` (y = 86, 12 px) và `r = 1,0 Ω` (y = 104, 12 px). Nếu 12 px không đủ chỗ, hạ còn 11 px.
3. **Điện trở R** trên cạnh phải (x = 370), giữa cạnh: hình chữ nhật đứng 16×50 (y = 75–125), cạnh phải ngắt
   ở đoạn đó; nhãn bên phải ngoài vòng (x = 385, start): `R = 5,0 Ω` (y = 104, 12 px). Phải chắc nhãn kết
   thúc trước x = 440 (ước ~55 px rộng → kết thúc x ≈ 440: **lùi x = 382** hoặc 11 px nếu cần, kiểm bằng mắt).
4. **Chiều dòng điện I** (mũi tên đỏ `#f87171`, marker `f4-r`): trên cạnh trên, từ (180, 40) tới (260, 40),
   **chiều từ trái sang phải** — tức đi **ra từ cực + (vạch dài, phía trên của nguồn)**, chạy qua R rồi trở
   về cực −. Nhãn `I = 2,0 A` (12 px, middle, x = 220, y = 30).
   Trên cạnh dưới, mũi tên đỏ thứ hai từ (260, 160) tới (180, 160) (chiều **phải sang trái**, hoàn tất vòng).
5. **Vôn kế U** đo hai đầu R: vòng tròn r = 13 tại (415, 100) có chữ `V` ở tâm, hai dây mảnh từ (370, 75) và
   (370, 125) nối tới vòng tròn — nhưng vị trí này chạm nhãn R. **Thay bằng**: mũi tên hai đầu mảnh (xanh
   dương `#38bdf8`) đặt **bên trong** vòng, song song cạnh phải, từ (345, 75) tới (345, 125), nhãn `U = 10 V`
   (11 px, end, x = 338, y = 104). Bỏ vôn kế.
6. Nhãn bên trong vòng, góc trên trái (x = 90, y = 70, start, 11 px, opacity 0.75): `mạch kín: I = ℰ/(R + r)`.

**Ràng buộc kiểm:** mũi tên I trên cạnh trên chỉ **sang phải** và trên cạnh dưới chỉ **sang trái** (dòng
điện ra từ cực + ở phía trên nguồn); vạch dài của pin ở trên vạch ngắn; nhãn `R = 5,0 Ω` không vượt
x = 440; nhãn `U = 10 V` không chồng mũi tên U.

**figcaption:** `Hình 4. Mạch kín: nguồn ℰ = 12 V, r = 1,0 Ω nuôi R = 5,0 Ω.` (HTML: `$\mathcal{E} = 12$ V`,
`$r = 1{,}0\ \Omega$`, `$R = 5{,}0\ \Omega$`).
**aria-label:** `Sơ đồ mạch kín một vòng gồm nguồn 12 vôn điện trở trong 1 ôm và điện trở ngoài 5 ôm, dòng điện 2 ampe đi ra từ cực dương, hiệu điện thế hai đầu R là 10 vôn`.

---

## Ghi chú cho agent code
- Sau khi chèn hình, chạy lại `lint_do_dai.py`: tổng phải ≤ 2.300 từ hiện ngay (hiện 2.248 chưa kể figcaption);
  nếu vượt, rút ngắn figcaption trước, không cắt nội dung.
- Số phút trong khung 🎯 Mục tiêu hiện ghi **16 phút**; nếu lint ra ≠ 16 (làm tròn) thì sửa lại số đó.
- Mục II.3 hiện không có "nhịp" (lint cảnh báo) — FIG2 sẽ lấp chỗ đó.
- Ký tự `ℰ` (U+2130) dùng được trong `<text>` SVG; nếu font không có, thay bằng `E` in nghiêng (`font-style="italic"`) nhất quán cả 4 hình và ghi vào báo cáo.
