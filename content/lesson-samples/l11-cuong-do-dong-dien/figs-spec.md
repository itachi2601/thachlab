# Đặc tả hình — Bài 22. Cường độ dòng điện (lesson_id 41)

Dành cho agent code viết `build_figs.py` (dùng `svg_lib.py`, chèn vào mốc `<!--FIGn-->` trong `theory.src.html` → `theory.html`).

Quy ước chung (xem `references/hinh-svg.md`):
- Mỗi hình bọc `<figure class="fig" data-tl="1"><svg viewBox="…" role="img" aria-label="…">…</svg><figcaption>Hình n. …</figcaption></figure>`.
- Marker mũi tên mỗi hình một tiền tố (`f1-`, `f2-`, `f3-`, `f4-`), không trùng id giữa các hình.
- Màu: đỏ `#f87171` = dòng điện quy ước I; xanh dương `#38bdf8` = electron / số đọc đồng hồ; xanh lá `#34d399` = vận tốc trôi v / chấm dữ liệu; cam `#fb923c` = hạt tải dương; thân vật, trục, chữ dùng `currentColor`.
- **Không dùng `$…$` trong `<text>`.** Chỉ số dưới viết bằng `<tspan dy="4" font-size="9">0</tspan>` rồi `<tspan dy="-4">` trả về. Trong đặc tả này "I₀", "v·Δt" là chữ thường mô tả nhãn, agent tự tách tspan.
- Chữ ≥ 11 px; nhãn sát mép dùng `text-anchor="start"` với x ≥ 12, không `middle` sát biên.
- Hình đánh số đúng thứ tự xuất hiện: FIG1 (mục II.1) → FIG2 (II.2) → FIG3 (II.3) → FIG4 (II.4). Bẫy 2 nhắc lại "hình 3" bằng chữ, không có hình mới.
- Sau khi dựng: chụp 375 px, xem mắt; dùng toạ độ để assert như ghi ở từng hình.

---

## FIG1 — Mạch kín có ampe kế nối tiếp; chiều dòng điện và chiều electron

- **Mốc:** `<!--FIG1-->` (mục II.1, ngay sau dòng "Mẹo nhớ", trước hộp thí nghiệm 01).
- **Mục đích:** một hình nói ba ý: ampe kế mắc nối tiếp; chiều dòng điện quy ước từ cực + qua mạch ngoài về cực −; electron chạy ngược chiều.
- **viewBox:** `0 0 420 230`.
- **`data-exp="tn-l11-cuong-do-dong-dien-01"`** đặt trên `<figure>`.
- **Đối tượng (toạ độ gợi ý):**
  - Mạch hình chữ nhật, nét `currentColor` 2 px: cạnh trên y = 50, cạnh dưới y = 180, cạnh trái x = 60, cạnh phải x = 360.
  - **Pin** nằm giữa cạnh trái (x = 60, y từ 100 đến 130), vẽ hai vạch ngang: vạch dài (30 px, nét 3) ở **trên** = cực dương, vạch ngắn (16 px, nét 1.5) ở **dưới** = cực âm; dây nối vào từ y = 50 xuống vạch dài và từ vạch ngắn xuống y = 180. Nhãn "+" đặt bên trái vạch dài (x = 40, y = 104), "−" bên trái vạch ngắn (x = 40, y = 134). Nhãn "Pin" ở x = 12, y = 120 (text-anchor start).
  - **Ampe kế** nằm trên cạnh trên, tâm (210, 50), bán kính 20, vòng tròn nét `#38bdf8` 2 px, chữ "A" `#38bdf8` 16 px bold ở giữa; dây cạnh trên ngắt từ x = 190 đến 230 để vòng tròn thay chỗ (nối tiếp). Nhãn nhỏ "nối tiếp" 11 px đặt trên vòng, x = 210, y = 22, text-anchor middle (xa mép, an toàn).
  - **Bóng đèn** nằm giữa cạnh phải: tâm (360, 115), bán kính 18, vòng tròn `currentColor`, bên trong dấu "×" (hai đường chéo); dây cạnh phải ngắt từ y = 97 đến 133. Nhãn "Đèn" ở x = 385, y = 119 (start).
  - **Mũi tên đỏ dòng điện I** (marker `f1-r`, nét 2.5 `#f87171`), đặt **trên dây**, 4 mũi theo **chiều kim đồng hồ** đúng vật lí (cực + ở trên bên trái):
    1. cạnh trên: từ (100, 50) → (170, 50) (hướng **sang phải**, tức đi từ cực + về phía ampe kế);
    2. cạnh phải: từ (360, 60) → (360, 90) (hướng **xuống**, vào đèn);
    3. cạnh dưới: từ (320, 180) → (250, 180) (hướng **sang trái**);
    4. cạnh trái dưới pin: từ (60, 170) → (60, 145) (hướng **lên**, về cực −).
    Nhãn "I" đỏ 14 px bold cạnh mũi 1: x = 135, y = 42, middle.
  - **Mũi tên xanh electron** (marker `f1-b`, nét 2 `#38bdf8`, nét đứt `4 3`), vẽ **song song bên trong mạch, cách dây 14 px**, **ngược chiều** mũi đỏ:
    1. song song cạnh trên, y = 64: từ (170, 64) → (100, 64) (sang **trái**);
    2. song song cạnh dưới, y = 166: từ (250, 166) → (320, 166) (sang **phải**).
    Nhãn "electron" `#38bdf8` 11 px tại x = 135, y = 78, middle; vẽ 2 chấm tròn nhỏ r = 4 fill `#38bdf8` ở gốc mỗi mũi xanh, chữ "−" trắng 8 px bên trong.
  - Nhãn chú thích góc dưới trái 11 px `currentColor`: "đỏ: chiều dòng điện · xanh: chiều electron" tại x = 12, y = 215 (start).
- **Kiểm bằng toạ độ:** mũi đỏ cạnh trên có x2 > x1; mũi đỏ cạnh phải có y2 > y1; mũi đỏ cạnh dưới có x2 < x1; mũi xanh cạnh trên có x2 < x1; mũi xanh cạnh dưới có x2 > x1. Vạch dài của pin nằm **trên** vạch ngắn (y_dài < y_ngắn). Không chữ nào có x < 12 hoặc x + độ dài chữ > 420.
- **figcaption:** `Hình 1. Ampe kế mắc nối tiếp; dòng điện từ cực + qua mạch ngoài về cực −, electron ngược lại.`
- **aria-label:** `Mạch kín gồm pin, ampe kế nối tiếp và bóng đèn; mũi tên đỏ chỉ chiều dòng điện từ cực dương qua mạch ngoài về cực âm, mũi tên xanh chỉ electron đi ngược chiều.`

---

## FIG2 — Đồ thị điện lượng theo thời gian ở dòng không đổi 1,50 A

- **Mốc:** `<!--FIG2-->` (mục II.2, sau dòng "Kiểm hàng đầu… Khớp.", trước `<details>` "Sai số đến từ đâu?").
- **Mục đích:** 5 chấm số liệu của bảng II.2 nằm trên một đường thẳng qua gốc; độ dốc = I.
- **viewBox:** `0 0 420 260`.
- **`data-exp="tn-l11-cuong-do-dong-dien-02"`** trên `<figure>`.
- **Hệ trục:** gốc O tại (60, 220). Trục t ngang tới (400, 220), trục q dọc tới (60, 20); đầu mũi tên `currentColor` (marker `f2-k`).
  - Thang ngang: 1 phút = 6 px → t = 10, 20, 30, 40, 50 phút tại x = 120, 180, 240, 300, 360. Vạch chia + nhãn "10", "20", "30", "40", "50" ở y = 238, middle. Nhãn trục "Δt (phút)" tại x = 400, y = 250, text-anchor **end**.
  - Thang dọc: 1 C = 0,04 px → q = 900, 1800, 2700, 3600, 4500 C tại y = 184, 148, 112, 76, 40. Vạch chia + nhãn "900", "1800", "2700", "3600", "4500" ở x = 54, text-anchor end, 11 px. Nhãn trục "Δq (C)" tại x = 14, y = 16 (start).
  - Nhãn "0" tại (54, 238) end.
- **Đường thẳng mô hình** `#f87171` nét 2: từ O (60, 220) đến (372, 32) — chính là q = 90·t (C, t phút) kéo tới t = 52 phút: x = 60 + 6·52 = 372, y = 220 − 0,04·90·52 = 32,8 ≈ 32. (Agent tự tính lại từ công thức, không gõ tay.)
- **5 chấm dữ liệu** `#34d399` r = 5, fill, viền `currentColor` 1 px, tại (120, 184), (180, 148), (240, 112), (300, 76), (360, 40).
- **Nhãn độ dốc** `#f87171` 11 px: "độ dốc = I = 1,50 A" tại x = 200, y = 60, text-anchor start (nằm phía trên-trái đường thẳng, không chạm chấm). Kiểm: không chồng chấm (300, 76).
- **Kiểm bằng toạ độ (assert trong build_figs.py):** với mỗi chấm, `abs(y − (220 − 0.04·90·t)) < 0.5` và `x == 60 + 6·t`; khoảng cách x giữa các chấm bằng nhau (60 px) và khoảng cách y bằng nhau (36 px) — trục chia tuyến tính; điểm đầu đường thẳng trùng O.
- **figcaption:** `Hình 2. Dòng không đổi 1,50 A: điện lượng tỉ lệ với thời gian, độ dốc là I.`
- **aria-label:** `Đồ thị điện lượng theo thời gian: năm chấm số liệu nằm trên đường thẳng qua gốc, độ dốc bằng cường độ dòng điện 1,50 ampe.`

---

## FIG3 — Dòng điện không đổi và dòng điện một chiều (hai đồ thị I–t)

- **Mốc:** `<!--FIG3-->` (mục II.3, ngay sau danh sách gạch đầu dòng "Dòng điện không đổi / một chiều", cuối mục).
- **Mục đích:** hai đồ thị cạnh nhau: trái "không đổi" là đường nằm ngang; phải "một chiều" là các bướu nửa sin nằm trọn phía trên trục t (chiều không đổi, cường độ nhấp nhô).
- **viewBox:** `0 0 420 170`. Hai ô, mỗi ô rộng 190: ô trái x ∈ [15, 205], ô phải x ∈ [215, 405].
- **Ô trái (Không đổi):**
  - Gốc O₁ tại (40, 130). Trục t ngang tới (200, 130), trục I dọc tới (40, 30), đầu mũi tên (marker `f3-k`). Nhãn "t" tại (196, 148) end, "I" tại (28, 34) end, "0" tại (34, 146) end.
  - Vạch ngang I₀: đường `#f87171` nét 2.5 từ (40, 70) đến (195, 70) — y **không đổi**. Nhãn "I₀" `#f87171` 12 px tại x = 34, y = 74, text-anchor end (chỉ số "0" bằng tspan).
  - Tiêu đề ô: "Không đổi" 12 px bold `currentColor` tại x = 110, y = 20, middle.
- **Ô phải (Một chiều, sau chỉnh lưu):**
  - Gốc O₂ tại (240, 130). Trục t tới (400, 130), trục I tới (240, 30). Nhãn "t" tại (396, 148) end, "I" tại (228, 34) end, "0" tại (234, 146) end.
  - Đường `#f87171` nét 2.5: các **bướu nửa sin** liên tiếp, biên độ 60 px (đỉnh y = 70, cùng mức I₀ của ô trái), mỗi bướu rộng 40 px, bắt đầu từ x = 240: bướu k chạy từ x = 240 + 40k đến 280 + 40k, k = 0..3 (kết thúc x = 400). Sinh bằng polyline: y = 130 − 60·|sin(π·(x − 240)/40)| lấy mẫu mỗi 2 px. Đường chấm ngang mảnh `currentColor` opacity 0.4 dash `3 3` ở y = 70 từ (240, 70) đến (400, 70) để thấy đỉnh bằng I₀; nhãn "I₀" tại x = 234, y = 74 end.
  - Tiêu đề ô: "Một chiều" 12 px bold tại x = 320, y = 20, middle.
- **Chú thích chung** 11 px `currentColor` tại x = 12, y = 164 (start): "cả hai: chiều không đổi · chỉ bên trái cường độ cũng không đổi".
- **Kiểm bằng toạ độ:** ô trái: mọi điểm của đường có y = 70; ô phải: mọi mẫu của polyline có `70 ≤ y ≤ 130` (không bao giờ xuống dưới trục t, tức không đổi chiều), min y = 70 tại x = 260, 300, 340, 380 (đỉnh bướu), y = 130 tại x = 240, 280, 320, 360, 400.
- **figcaption:** `Hình 3. Trái: dòng không đổi. Phải: dòng một chiều sau chỉnh lưu, chỉ chiều không đổi.`
- **aria-label:** `Hai đồ thị cường độ dòng điện theo thời gian: bên trái đường nằm ngang là dòng không đổi, bên phải các bướu nửa sin nằm trên trục thời gian là dòng một chiều có cường độ thay đổi.`

---

## FIG4 — Hình trụ dài v·Δt trước tiết diện S: đếm hạt để ra I = Snve

- **Mốc:** `<!--FIG4-->` (mục II.4, sau đoạn văn "Dây tiết diện S… phía trước S.", trước danh sách "Số hạt trong trụ").
- **Mục đích:** thấy "hạt nào đi qua S trong Δt": đúng các hạt nằm trong hình trụ dài v·Δt ở phía **đi tới** S.
- **viewBox:** `0 0 420 200`.
- **`data-exp="tn-l11-cuong-do-dong-dien-03"`** trên `<figure>`.
- **Đối tượng:**
  - **Dây dẫn** hình trụ nằm ngang: hai đường `currentColor` nét 2 ở y = 60 và y = 140, từ x = 30 đến x = 390; đầu phải vẽ ellipse đặc (cx = 390, cy = 100, rx = 10, ry = 40) fill `currentColor` opacity 0.08, viền nét 2; đầu trái vẽ nửa ellipse hở (cung) cùng kích thước.
  - **Tiết diện S**: ellipse nét đứt `#f87171` nét 2, dash `5 3`, cx = 270, cy = 100, rx = 10, ry = 40, fill `#f87171` opacity 0.15. Nhãn "S" `#f87171` 14 px bold tại x = 270, y = 30, middle, kèm đường dẫn mảnh từ (270, 34) xuống (270, 58).
  - **Hình trụ "sắp đi qua S"**: vùng tô `#34d399` opacity 0.12 từ x = 150 đến x = 270 (chiều dài v·Δt = 120 px), y từ 60 đến 140; ellipse đầu trái nét đứt mảnh `#34d399` tại cx = 150, cùng rx, ry. Hạt **ở bên trái S** (phía đi tới) vì hạt chuyển động **sang phải**.
  - **Mũi tên hai đầu** `currentColor` (marker `f4-k` hai đầu) ở y = 160, từ (150, 160) đến (270, 160); nhãn "v·Δt" 12 px tại x = 210, y = 178, middle (dùng ký tự Δ thường, không KaTeX).
  - **Hạt tải dương**: 6 chấm `#fb923c` r = 7 với chữ "+" trắng 10 px bold ở giữa, rải trong hình trụ (tránh chồng nhãn): (170, 80), (200, 118), (225, 85), (245, 125), (190, 100), (255, 100). Thêm 2 chấm **ngoài** trụ bên trái (x = 90, y = 90 và x = 115, y = 125) và 1 chấm bên phải S (x = 330, y = 95) để thấy hạt ngoài trụ không được đếm.
  - **Mũi tên v** `#34d399` nét 2 (marker `f4-g`) từ mép phải mỗi chấm trong trụ sang **phải** dài 16 px (ví dụ chấm (170, 80): từ (178, 80) → (194, 80)); nhãn "v" `#34d399` 12 px italic tại x = 200, y = 72 (gần mũi của chấm (170, 80)), start. Hạt ngoài trụ cũng có mũi tên v (cùng chiều) nhưng không tô nền.
  - **Mũi tên I** `#f87171` nét 3 (marker `f4-r`) dưới dây: từ (300, 188) → (380, 188), nhãn "I" đỏ 14 px bold tại x = 340, y = 182, middle. Cùng chiều với v (hạt dương).
  - Nhãn "n hạt trong mỗi m³" 11 px `currentColor` tại x = 32, y = 50, start.
  - Nhãn "N = n·S·v·Δt hạt" `#34d399` 11 px tại x = 150, y = 50... **không** — tránh chồng với "n hạt trong mỗi m³"; đặt tại x = 395, y = 178, text-anchor **end** (góc dưới phải, dưới ellipse đầu dây, không chạm mũi tên I ở y = 188: mũi I nằm x ≤ 380, nhãn kết thúc ở x = 395 cùng hàng y = 178 — nếu chồng, dời mũi I xuống y = 194).
- **Kiểm bằng toạ độ:** mọi chấm "trong trụ" có `150 + 7 ≤ cx ≤ 270 − 7` và `60 + 7 ≤ cy ≤ 140 − 7`; chấm ngoài trụ có cx < 143 hoặc cx > 277; mọi mũi tên v có x2 > x1 (sang phải); mũi tên I có x2 > x1; mũi tên v·Δt có x1 = 150, x2 = 270 (đúng bằng chiều dài vùng tô). Hai nhãn 11 px cùng hàng không được cách nhau < 8 px theo x.
- **figcaption:** `Hình 4. Hạt trong hình trụ dài v·Δt trước tiết diện S đi qua S trong Δt: N = nSvΔt.`
- **aria-label:** `Đoạn dây dẫn hình trụ, tiết diện S vẽ nét đứt; các hạt tải điện dương nằm trong đoạn dài v nhân delta t phía trước S đang trôi sang phải sẽ đi qua S; mũi tên I cùng chiều với v.`

---

## Ghi chú cho agent code

- Số từ hiện ngay của `theory.src.html` đang ≈ 2.215 (đo `lint_do_dai.py`); 4 figcaption trên cộng thêm ≈ 75 từ → bản `theory.html` cuối ≈ 2.29x từ (đã mô phỏng bằng cách chèn figcaption giả, 0 lỗi cứng). Giữ figcaption **đúng như đặc tả**, đừng viết dài hơn, kẻo vượt 2.300.
- Khung 🎯 ghi "Khoảng 16 phút" — sau khi dựng `theory.html` chạy lại `lint_do_dai.py`, nếu lệch khỏi 16 thì sửa số trong khung.
- `build_bundle.py`: đọc `exam.json` cùng thư mục (đừng chép tay 5 câu vào script), `target.lesson_title = "Bài 22. Cường độ dòng điện"`, `theory_subtitle = "Cường độ dòng điện, chiều dòng điện, dòng điện không đổi và liên hệ I = Snve với hạt tải điện"`.
- Mục II.3 hiện chưa có nhịp nào (lint cảnh báo) — FIG3 chèn vào đó sẽ hết cảnh báo; đừng chuyển FIG3 sang chỗ khác.
