# Đặc tả hình — Bài 23. Điện trở. Định luật Ohm (lesson 42)

Bốn hình, đánh số theo thứ tự xuất hiện trong `theory.src.html` (mốc `<!--FIG1-->` … `<!--FIG4-->`).
Quy ước chung (theo `references/hinh-svg.md`): `viewBox` rộng ≤ 440; chữ `currentColor`, cỡ ≥ 11 px; marker mũi tên
mỗi hình một tiền tố (`f1-`, `f2-`…); **không** dùng `$…$` trong `<text>` (KaTeX sẽ phá chữ) — chỉ số dưới viết bằng
`<tspan dy="4" font-size="9">…</tspan><tspan dy="-4">`; chèn dạng `<figure class="fig" data-tl="1">…<figcaption>…</figcaption></figure>`.
Màu: xanh dương `#38bdf8` = điện trở/đường thẳng (vật "chuẩn"); cam `#fb923c` = đèn sợi đốt/nóng; đỏ `#f87171` = electron/dòng;
xanh lá `#34d399` = điểm đo. Nền trong suốt, nét thân vật `currentColor` để tối/sáng đều đọc.

Hai hình đồ thị (FIG2, FIG4) dùng **cùng một hệ trục và cùng phép chiếu** để học sinh so sánh được bằng mắt:

```
viewBox 0 0 420 300
gốc O tại (50, 250)
x = 50 + 55·U        (U tính bằng V; U = 6 → x = 380)
y = 250 − 350·I      (I tính bằng A; I = 0,6 → y = 40)
trục U: 0..6 V, vạch mỗi 1 V (x = 50, 105, 160, 215, 270, 325, 380), nhãn "0" … "6"
trục I: 0..0,6 A, vạch mỗi 0,1 A (y = 250, 215, 180, 145, 110, 75, 40), nhãn "0" "0,1" … "0,6"
```
Agent code **phải assert** bằng toạ độ: mọi điểm dữ liệu nằm đúng phép chiếu trên (sai lệch < 1 px), hai trục chia
tuyến tính (khoảng cách vạch bằng nhau), điểm nằm trên đường (với đường thẳng: `|y − (250 − 350·x_U/R)| < 1`).

---

## FIG1 — Sơ đồ mạch đo đường đặc trưng vôn – ampe

- **Vị trí:** mục II.2, ngay sau dòng 🔑, trước hộp thí nghiệm `tn-l11-dien-tro-ohm-01`.
- **Mục đích:** học sinh nhìn ra ampe kế **nối tiếp** với linh kiện, vôn kế **song song** với linh kiện, nguồn điều chỉnh được.
- **data-exp:** `tn-l11-dien-tro-ohm-01` (đặt trên `<figure>`).
- **viewBox gợi ý:** `0 0 420 210`.
- **Đối tượng (vẽ bằng ký hiệu mạch điện chuẩn, nét `currentColor` 2 px):**
  1. Mạch chữ nhật lớn: góc trên-trái (40, 40), góc dưới-phải (380, 170).
  2. **Nguồn điều chỉnh** trên cạnh trái, giữa (x = 40, y ≈ 105): ký hiệu pin (vạch dài + vạch ngắn, vạch dài ở trên = cực +) có mũi tên chéo xuyên qua (ký hiệu "điều chỉnh được"). Nhãn bên trái ký hiệu, chữ 11 px: "Nguồn" (dòng 1), "0–6 V" (dòng 2); dấu "+" nhỏ phía trên vạch dài, "−" phía dưới vạch ngắn.
  3. **Khoá K** trên cạnh trên, cách góc trái ~70 px (x ≈ 110): hai chấm + đoạn nghiêng mở nhẹ; nhãn "K" phía trên.
  4. **Ampe kế** trên cạnh trên, giữa (x ≈ 210, y = 40): vòng tròn bán kính 16, chữ "A" ở tâm, cỡ 14 px, màu `currentColor`. Nhãn nhỏ phía trên vòng tròn: "nối tiếp" (11 px).
  5. **Linh kiện R** trên cạnh phải, giữa (x = 380, y ≈ 105): hình chữ nhật đứng 16 × 44 (ký hiệu điện trở IEC), màu viền `#38bdf8`. Nhãn bên phải: "R = 10 Ω" (dòng 1), "(hoặc đèn)" (dòng 2), 11 px — nếu chạm mép phải thì để nhãn bên trong mạch, bên trái linh kiện.
  6. **Vôn kế** mắc song song với R: hai dây rẽ từ hai đầu R (y ≈ 75 và y ≈ 135) vào trong mạch tới vòng tròn tâm (310, 105) bán kính 16, chữ "V" ở tâm 14 px. Nhãn nhỏ phía trên vòng tròn: "song song" (11 px).
  7. **Mũi tên chiều dòng I**: trên cạnh dưới, giữa (x ≈ 210, y = 170), mũi tên đỏ `#f87171` dài 40 px chỉ **từ phải sang trái** (dòng đi ra từ cực + ở trên cạnh trái, theo chiều kim đồng hồ: lên → sang phải qua K, A → xuống qua R → sang trái ở cạnh dưới → về cực −). Nhãn "I" đỏ, 13 px, phía trên mũi tên.
- **Kiểm chiều vật lí:** cực + của nguồn nối vào cạnh trên (qua K, A) → dòng quy ước qua R từ trên xuống → trên cạnh dưới dòng chạy sang trái về cực −. Mũi tên I ở cạnh dưới phải chỉ sang trái.
- **figcaption:** `Hình 1. Mạch đo đường đặc trưng vôn – ampe: ampe kế nối tiếp với linh kiện, vôn kế song song với linh kiện; nguồn điều chỉnh được từ 0 đến 6 V.`
- **aria-label (trên `<svg>`):** `Sơ đồ mạch điện gồm nguồn điều chỉnh, khoá K, ampe kế nối tiếp với điện trở R, vôn kế mắc song song hai đầu R, mũi tên I chỉ chiều dòng điện.`

---

## FIG2 — Đường đặc trưng vôn – ampe của điện trở (đường thẳng qua gốc)

- **Vị trí:** mục II.2, ngay sau bảng số liệu điện trở 10 Ω (mốc `<!--FIG2-->`), trước danh sách bullet "Đường đặc trưng vôn – ampe".
- **Mục đích:** 5 điểm đo nằm đúng trên một đường thẳng qua gốc; đường 20 Ω thoải hơn để thấy "dốc hơn là R nhỏ hơn".
- **data-exp:** `tn-l11-dien-tro-ohm-01`.
- **viewBox:** `0 0 420 300`, hệ trục chung ở đầu file.
- **Đối tượng:**
  1. Hai trục `currentColor` 1,5 px có đầu mũi tên: trục U từ (50, 250) → (400, 250); trục I từ (50, 250) → (50, 25). Nhãn "U (V)" ở (395, 275) `text-anchor="end"`; nhãn "I (A)" ở (58, 22) `text-anchor="start"`; "O" ở (40, 265).
  2. Vạch chia + nhãn như hệ trục chung (chữ 11 px; nhãn trục U đặt y = 268; nhãn trục I đặt x = 44, `text-anchor="end"`, căn giữa theo vạch).
  3. **Đường R = 10 Ω** màu `#38bdf8`, 2,5 px, từ O (50, 250) tới U = 5,6 V → (358, 54) (dừng trước mép trên). Phương trình: I = U/10. Nhãn "R = 10 Ω" màu `#38bdf8` 12 px đặt ở (300, 95), phía trên-trái đường (không đè đường).
  4. **5 điểm đo** `#34d399`, bán kính 4, viền `currentColor` 1 px, tại (U, I) = (1; 0,10), (2; 0,20), (3; 0,30), (4; 0,40), (5; 0,50) → toạ độ (105, 215), (160, 180), (215, 145), (270, 110), (325, 75). Assert mỗi điểm nằm trên đường (sai < 1 px).
  5. **Đường R = 20 Ω** màu `#38bdf8` nhưng **nét đứt** `stroke-dasharray="6 4"`, 2 px, từ O tới U = 6 V → (380, 145). Phương trình I = U/20. Nhãn "R = 20 Ω" 12 px ở (330, 170), phía dưới-phải đường.
  6. Chú thích nhỏ góc trên-phải (260, 45), 11 px, `currentColor`: "dốc hơn → R nhỏ hơn".
- **Kiểm bằng toạ độ:** điểm thứ k có x = 50 + 55k, y = 250 − 35k; đường 20 Ω tại x = 380 phải có y = 145.
- **figcaption:** `Hình 2. Đường đặc trưng vôn – ampe của điện trở: đường thẳng qua gốc toạ độ. Năm điểm đo của điện trở 10 Ω nằm đúng trên đường I = U/10; đường đứt là điện trở 20 Ω, thoải hơn vì R lớn hơn.`
- **aria-label:** `Đồ thị I theo U: đường thẳng qua gốc của điện trở 10 Ω với năm điểm đo, và đường đứt thoải hơn của điện trở 20 Ω.`

---

## FIG3 — Electron va chạm ion nút mạng: kim loại lạnh và kim loại nóng

- **Vị trí:** mục II.4, ngay sau dòng 🔑 (mốc `<!--FIG3-->`), trước danh sách bullet.
- **Mục đích:** một hình = một ý: electron tự do trôi qua mạng ion dương, bị va chạm; nóng hơn → ion rung mạnh hơn → va nhiều hơn.
- **data-exp:** không có (không gắn thí nghiệm).
- **viewBox:** `0 0 440 230`, chia hai ô bằng nhau: ô trái x ∈ [10, 210], ô phải x ∈ [230, 430]; mỗi ô là khung chữ nhật bo góc, viền `currentColor` 1 px, mờ 0,5.
- **Đối tượng trong MỖI ô:**
  1. Tiêu đề ô ở (x_giữa_ô, 28), `text-anchor="middle"`, 12 px đậm: ô trái "Kim loại lạnh" ; ô phải "Kim loại nóng" (màu cam `#fb923c`).
  2. **Mạng ion dương 3 hàng × 4 cột**: vòng tròn bán kính 9, viền `currentColor`, nền trong suốt, dấu "+" ở tâm (10 px). Tâm tại x = x0 + 50·j (j = 0..3, x0 = 35 cho ô trái, 255 cho ô phải), y = 70 + 45·i (i = 0..2) → y = 70, 115, 160.
  3. **Ô phải (nóng)**: mỗi ion vẽ thêm hai cung "rung" (hai nét cong ngắn hai bên ion, màu `#fb923c`, 1,5 px) hoặc vẽ ion thành **hai vòng tròn mờ lệch nhau** ±4 px theo ngang (nét mờ 0,5) để diễn tả dao động mạnh. Ô trái: ion chỉ có một cung rung rất nhỏ hoặc không có.
  4. **Electron**: chấm đỏ `#f87171` bán kính 4 có dấu "−" trắng, xuất phát ở mép trái ô (x = x0 − 15, **y = 92,5** — hành lang giữa hàng ion 1 (y = 70) và hàng 2 (y = 115), không đè ion) đi sang phải.
     - Ô trái: đường đi `polyline` đỏ 1,5 px **gần thẳng**, zigzag nhẹ (lệch ±6 px) qua 3 điểm gấp khúc; kết thúc ở mép phải ô (x = x0 + 170, y ≈ 115) bằng đầu mũi tên (marker `f3-r`).
     - Ô phải: đường đi zigzag **mạnh** (lệch ±18 px) với 6 điểm gấp khúc, mỗi điểm gấp khúc đặt **sát mép một ion** (cách tâm ion ≈ 12 px) để diễn tả va chạm; kết thúc ở mép phải ô, cũng có mũi tên.
  5. **Mũi tên chiều trôi** dưới mỗi ô, y = 200: mũi tên đỏ dài 60 px chỉ sang phải, nhãn "electron trôi" 11 px đỏ bên phải mũi tên (ô trái) — ô phải chỉ vẽ mũi tên, nhãn "va nhiều, trôi chậm" 11 px cam.
  6. Chú thích chung một dòng ở đáy (220, 222), `text-anchor="middle"`, 11 px, `currentColor`: "ion dương ở nút mạng (+) · electron tự do (−)".
- **Kiểm:** hai ô có cùng số ion, cùng toạ độ tương đối; tổng độ lệch ngang của zigzag ô phải lớn hơn ô trái ít nhất 2 lần; mọi nhãn không đè lên ion (kiểm bằng khoảng cách tâm ion ↔ hộp chữ ≥ 6 px).
- **figcaption:** `Hình 3. Trái: kim loại lạnh, ion rung ít, electron đi gần thẳng. Phải: kim loại nóng, ion rung mạnh, electron va chạm nhiều, trôi chậm hơn.`
- **aria-label:** `Hai ô so sánh: trong kim loại lạnh electron đi gần thẳng qua mạng ion dương; trong kim loại nóng ion rung mạnh, electron va chạm liên tục, đường đi zigzag.`

---

## FIG4 — Đường đặc trưng vôn – ampe của đèn sợi đốt (đường cong)

- **Vị trí:** mục II.5, ngay sau bảng số liệu bóng đèn 6 V – 3 W (mốc `<!--FIG4-->`), trước danh sách bullet "Đường cong, dốc giảm dần khi U tăng…".
- **Mục đích:** 6 điểm đo nằm trên một đường **cong** có độ dốc giảm dần; so với đường thẳng 12 Ω (đi qua O và điểm cuối), các điểm giữa nằm **phía trên** đường thẳng.
- **data-exp:** `tn-l11-dien-tro-ohm-02`.
- **viewBox:** `0 0 420 300`, hệ trục chung (giống hệt FIG2: cùng gốc, cùng vạch, cùng nhãn).
- **Đối tượng:**
  1. Hai trục + vạch chia + nhãn: **copy nguyên** từ FIG2 (đổi tiền tố marker thành `f4-`).
  2. **Đường cong của đèn** màu cam `#fb923c`, 2,5 px, `fill="none"`: `polyline` (hoặc `path` nối thẳng các mẫu) lấy mẫu từ phương trình
     `I = 0,1706 · U^0,6` với U = 0; 0,25; 0,5; …; 6,0 (25 mẫu), chiếu bằng phép chiếu chung. Tại U = 0 là O (50, 250); tại U = 6 là (380, 75). Agent code tính mẫu bằng Python, **không** vẽ tay bằng `Q`/`T`.
  3. **6 điểm đo** `#34d399` bán kính 4, viền `currentColor` 1 px, tại (U, I) = (1; 0,17), (2; 0,26), (3; 0,33), (4; 0,39), (5; 0,45), (6; 0,50) → toạ độ (105, 190,5), (160, 159), (215, 134,5), (270, 113,5), (325, 92,5), (380, 75). Assert: mỗi điểm cách đường cong (giá trị đúng của phương trình, chưa làm tròn) < 2 px theo y.
  4. **Đường thẳng 12 Ω** màu `#38bdf8` nét đứt `6 4`, 2 px, từ O (50, 250) tới (380, 75) — chính là đường qua điểm cuối, phương trình I = U/12. Nhãn "R = 12 Ω không đổi" 11 px màu `#38bdf8` đặt ở (300, 190), phía **dưới-phải** đường đứt (không đè đường cong).
  5. Nhãn "Đèn sợi đốt" 12 px cam ở (150, 120), phía **trên-trái** đường cong.
  6. Một mũi tên chú thích nhỏ `currentColor` 1 px từ chữ "R tăng dần" (11 px, ở (250, 50)) chỉ xuống gần điểm (5; 0,45) — chỉ thêm nếu không chạm nhãn khác; bỏ qua nếu chật.
- **Kiểm bằng toạ độ:** tại x = 160 (U = 2) điểm đo y = 159 phải **nhỏ hơn** (nằm trên) y của đường đứt = 250 − 350·2/12 = 191,7; độ dốc đoạn (1→2 V) phải lớn hơn độ dốc đoạn (5→6 V) (tính từ toạ độ pixel: |Δy/Δx| giảm dần theo U).
- **figcaption:** `Hình 4. Đường đặc trưng vôn – ampe của đèn sợi đốt 6 V – 3 W: đường cong, độ dốc giảm dần vì dây tóc càng nóng điện trở càng lớn. Đường đứt là đường thẳng ứng với R = 12 Ω không đổi; các điểm đo ở U nhỏ nằm phía trên đường đó.`
- **aria-label:** `Đồ thị I theo U của đèn sợi đốt: đường cong qua sáu điểm đo, độ dốc giảm dần; đường đứt thẳng ứng với điện trở 12 Ω để so sánh.`

---

## Ghi chú cho agent code

- Chèn hình bằng script idempotent kiểu `build_figs.py` của `content/lesson-samples/l11-dien-truong-deu/` (thay mốc `<!--FIGn-->` bằng `<figure class="fig" data-tl="1" data-exp="…">` khi có `data-exp`), sinh `theory.html` từ `theory.src.html`; giữ nguyên `theory.src.html`.
- Sau khi vẽ, chạy `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/thi_nghiem.py <theory.html>` lại vì `data-exp` trên `<figure>` cũng được kiểm.
- Đồ thị FIG2/FIG4 là chỗ dễ sai nhất (bài học 23 trong SKILL.md): assert bằng toạ độ trước khi chụp ảnh; rồi vẫn phải xem ảnh 375 px xem nhãn "R = 20 Ω"/"R = 12 Ω không đổi" có đè đường hay chạm mép không.

## Cập nhật sau kiểm chéo v1 (5/10/2026) — việc của agent code, chưa làm trong build_figs.py

- FIG2/FIG4 `axes()`: gốc đang in "O" và nhãn "0" của trục U sát nhau thành "O 0" → **bỏ nhãn "0" trên trục U**, giữ "O" ở (40, 265). Vạch chia trục U chỉ còn 1…6.
- FIG3: electron đi ở **y = 92,5** (đã sửa ở mục 4 bên trên cho khớp code); figcaption đổi theo bản mới ở mục FIG3.
- Cỡ chữ SVG: 11 px quá nhỏ ở 375 px → nhãn phụ (vạch chia, chú thích) **13 px**, nhãn chính (tên trục, "R = 10 Ω", tiêu đề ô) **14 px**; hoặc thu `viewBox` về rộng ~380. Sau khi đổi: chạy lại kiểm chồng nhãn (`Fig.check`), `chup_anh.py --chi-hinh`, xem ảnh.
- Mô hình đường cong FIG4 `I = 0,1706·U^0,6` dốc nhất sát gốc (độ dốc 0,178 ở 0,25 V, 0,05 ở 6 V); file `tn-l11-dien-tro-ohm-02.json` đã ghi rõ mô hình không dùng cho U < 1 V. Đoạn O→1 V trên hình vẫn vẽ bằng mô hình để đường đi qua O, chấp nhận được; không mô tả đoạn này là "gần thẳng" ở bất cứ đâu.
