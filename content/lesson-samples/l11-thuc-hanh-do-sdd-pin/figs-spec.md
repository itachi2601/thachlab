# Đặc tả hình — Bài 26 (lesson 45) Thực hành đo $\mathcal{E}$, r của pin

Bốn hình, đánh số theo thứ tự xuất hiện trong `theory.src.html` (mốc `<!--FIG1-->` … `<!--FIG4-->`). Quy ước chung
(theo `references/hinh-svg.md`): `<figure class="fig" data-tl="1">` + `<figcaption>`; viewBox rộng **≤ 440** để vừa 375 px;
nét thân mạch/chữ dùng `currentColor`; marker mũi tên mỗi hình một tiền tố (`f1-`, `f2-`…); **KHÔNG** viết `$…$` trong `<text>`
(KaTeX phá SVG) — chỉ số dưới viết bằng ký tự Unicode (U₁, R₀, Rₓ) hoặc `<tspan dy="4" font-size="9">`; chữ nhãn/số trục 13 (chỉ số dưới 11) vì viewBox 440 thu về ~0,8 ở 375 px;
nhãn sát mép dùng `text-anchor="start"`. Màu có nghĩa: đỏ `#f87171` = pin cũ / số đo tụt; xanh dương `#38bdf8` = pin mới /
vôn kế; xanh lá `#34d399` = đường thẳng khớp; cam `#fb923c` = ampe kế / dòng điện.

Trong mọi nhãn chữ KHÔNG dùng `$`. Ký hiệu suất điện động trong nhãn SVG ghi là "ℰ" (U+2130) hoặc chữ "E" — bài dùng ℰ.

---

## Hình 1 — Cùng một viên pin, hai số đo (mở bài)

- **Vị trí:** sau hai đoạn mở bài, trước hộp "Dự đoán". Mốc `<!--FIG1-->`.
- **Mục đích:** cho thấy vôn kế hở mạch đọc 1,50 V, còn khi động cơ quay thì chỉ còn 1,06 V. Hình = một ý: "có dòng thì U tụt".
- **`data-exp="tn-l11-do-sdd-pin-03"`** đặt trên `<figure>`.
- **viewBox:** `0 0 440 190`. Hai khung cạnh nhau, mỗi khung rộng ~200, cách nhau 20, lề 10.
- **Khung trái (x 10–210): "Hở mạch".**
  - Pin AA vẽ nằm ngang: hình chữ nhật 70×26 tại (40, 80), đầu cực dương là núm nhỏ 6×12 ở mép phải; nhãn "+" sát núm, "−" đầu trái (font 12).
  - Vôn kế: vòng tròn r = 16 tại (150, 93), chữ "V" ở tâm (font 13, `currentColor`), viền xanh dương `#38bdf8`.
  - Hai dây từ hai cực pin lên vôn kế (polyline, `currentColor`, stroke 1.5). Không có tải nào khác.
  - Hộp số hiện (màn hình đồng hồ): hình chữ nhật 56×20 tại (122, 118), chữ **"1,50 V"** (font 13, đậm, xanh dương) ở tâm.
  - Nhãn tiêu đề khung: "Chưa lắp vào xe" tại (110, 30), `text-anchor="middle"`, font 12.
  - Chú thích dưới: "I = 0" tại (110, 165), middle, font 11.
- **Khung phải (x 230–430): "Có tải".**
  - Cùng viên pin (hình chữ nhật 70×26 tại (260, 80)), cùng vôn kế (vòng r = 16 tại (370, 93)) mắc song song pin như khung trái.
  - Thêm **động cơ**: vòng tròn r = 13 tại (315, 150) chữ "M" ở tâm, nối tiếp với pin thành mạch kín (dây từ cực + đi xuống qua M về cực −). Mũi tên dòng điện cam `#fb923c` (marker `f1-i`) trên dây phía trên, chiều từ cực + ra ngoài, nhãn "I ≈ 0,5 A" cạnh mũi tên (font 11, cam).
  - Hộp số: chữ **"1,06 V"** (font 13, đậm, đỏ `#f87171`) trong hộp 56×20 tại (342, 118).
  - Nhãn tiêu đề khung: "Động cơ đang quay" tại (330, 30), middle, font 12.
- **Kiểm (assert trong build_figs.py):** cả hai vôn kế đều mắc song song hai cực pin (đầu dây vôn kế trùng toạ độ hai cực); dòng cam chỉ có ở khung phải; chữ "1,50 V" và "1,06 V" đúng số của bài.
- **figcaption:** `Hình 1. Cùng một viên pin: hở mạch vôn kế đọc 1,50 V, khi động cơ quay chỉ còn 1,06 V.`
- **aria-label:** `Hai khung: pin với vôn kế hở mạch đọc 1,50 V; pin nối động cơ đang quay, vôn kế đọc 1,06 V.`

---

## Hình 2 — Sơ đồ mạch đo ℰ và r

- **Vị trí:** mục II.2, sau danh sách dụng cụ, trước đoạn "Vôn kế mắc song song…". Mốc `<!--FIG2-->`.
- **Mục đích:** sơ đồ chuẩn để học sinh lắp theo: pin – K – ampe kế – R₀ – biến trở Rₓ nối tiếp; vôn kế song song hai cực pin (M, N). Thay cho hình 1 của bản cũ (phải giữ: điểm M, N; R đã biết; Rx; A; V; K; ℰ, r).
- **viewBox:** `0 0 440 230`.
- **Mạch chữ nhật** nét `currentColor` stroke 2: đỉnh trái-trên (70, 50), phải-trên (380, 50), phải-dưới (380, 180), trái-dưới (70, 180).
- **Cạnh trái (x = 70), pin:** ký hiệu pin tại giữa cạnh: vạch dài (cực +) ngang 24 px tại y = 108, vạch ngắn dày (cực −) ngang 12 px tại y = 122; cực + ở **trên**. Nhãn "ℰ, r" tại (20, 118) font 13, `text-anchor="start"`. Hai điểm nút **M** (70, 85) và **N** (70, 145) vẽ chấm r = 3, nhãn "M" tại (52, 82), "N" tại (52, 152) font 12.
- **Cạnh trên (y = 50):** 
  - **Khoá K** tại x 120–160 (đóng, đang đọc số): chấm (120, 50), chấm (160, 50), thanh gạt ngang nối hai chấm (120, 50)→(160, 50), nhãn "K" tại (140, 34) middle font 13.
  - **Ampe kế A**: vòng tròn r = 14 tại (230, 50), chữ "A" ở tâm font 13, viền cam `#fb923c`. Dây cạnh trên ngắt hai bên vòng tròn (không vẽ xuyên qua).
  - Mũi tên dòng điện cam (marker `f2-i`) trên đoạn (290, 50)→(330, 50) chiều **từ trái sang phải** (từ cực + ra ngoài qua K, A rồi về cực −). Nhãn "I" tại (310, 40) font 12 cam.
- **Cạnh phải (x = 380):** điện trở bảo vệ **R₀**: răng cưa (polyline zigzag, xanh dương `#38bdf8`, stroke 2) dọc từ (380, 80) tới (380, 120); nhãn "R₀ = 2 Ω" tại (392, 104) font 12, `text-anchor="start"`.
- **Cạnh dưới (y = 180):** biến trở **Rₓ**: răng cưa ngang từ (200, 180) tới (280, 180), xanh dương; mũi tên chéo xuyên qua (ký hiệu biến trở) từ (205, 200) tới (275, 162) có đầu mũi (marker `f2-b`, `currentColor`); nhãn "Rₓ (0–100 Ω)" tại (240, 215) middle font 12.
- **Vôn kế V:** nhánh song song pin, nằm **bên trong** khung: từ M (70, 85) sang phải tới (150, 85), xuống (150, 145), về N (70, 145); vòng tròn r = 14 tại (150, 115) chữ "V" font 13, viền xanh lá `#34d399`; dây ngắt hai bên vòng tròn. Nhãn "U" tại (170, 119) font 12 start.
- **Kiểm (assert):** hai đầu nhánh vôn kế trùng toạ độ M và N; vòng A nằm trên cạnh trên (nối tiếp); mũi tên I chiều +x trên cạnh trên; không nhãn nào có x < 12 hay x > 428; không có `$`.
- **figcaption:** `Hình 2. Sơ đồ mạch đo: pin (ℰ, r) – khoá K – ampe kế A – R₀ – biến trở Rₓ nối tiếp; vôn kế V mắc song song hai cực pin M, N.`
- **aria-label:** `Sơ đồ mạch kín: pin, khoá K, ampe kế, điện trở bảo vệ R0 và biến trở Rx nối tiếp; vôn kế mắc song song hai cực pin.`

---

## Hình 3 — Đồ thị U–I của pin cũ, đường thẳng khớp, ℰ và hai điểm A, B

- **Vị trí:** mục V, ngay sau hộp "Đề bài", trước câu "Mỗi cụm của đề…". Mốc `<!--FIG3-->`.
- **Mục đích:** minh hoạ lời giải: 6 điểm đo, đường thẳng khớp, giao trục U = ℰ, hai điểm A, B trên đường và tam giác ΔU/ΔI.
- **viewBox:** `0 0 440 290`.
- **Lưới toạ độ (TUYẾN TÍNH — assert bằng toạ độ):** vùng vẽ x từ 60 đến 410 ứng với I = 0 → 0,6 A (583.3 px/A); y từ 250 đến 30 ứng với U = 1,0 → 1,7 V (314.3 px/V). Hàm: `x = 60 + 583.3333·I`, `y = 250 − 314.2857·(U − 1,0)`.
  - Trục I: mũi tên tới (420, 250), nhãn "I (A)" tại (396, 272) font 12. Vạch chia 0; 0,1; …; 0,6 ở x = 60.0, 118.3, 176.7, 235.0, 293.3, 351.7, 410.0; ghi số "0", "0,1" … "0,6" dưới trục (y = 266, font 11, middle).
  - Trục U: mũi tên tới (60, 18), nhãn "U (V)" tại (14, 16) font 12 start. Vạch chia 1,0; 1,1; …; 1,7 ở y = 250.0, 218.6, 187.1, 155.7, 124.3, 92.9, 61.4, 30.0; ghi số bên trái trục (x = 52, `text-anchor="end"`, font 11). Trục U bắt đầu tại U = 1,0 (không từ 0) — ghi rõ "1,0" ở gốc để học sinh không hiểu nhầm.
  - Lưới mờ (stroke-opacity 0.15) qua các vạch.
- **6 điểm đo (chấm đỏ `#f87171`, r = 4):**

| Lần | I (A) | U (V) | (x, y) |
|---|---|---|---|
| 1 | 0.014 | 1.48 | (68.2, 99.1) |
| 2 | 0.066 | 1.44 | (98.5, 111.7) |
| 3 | 0.117 | 1.40 | (128.2, 124.3) |
| 4 | 0.191 | 1.35 | (171.4, 140.0) |
| 5 | 0.311 | 1.25 | (241.4, 171.4) |
| 6 | 0.534 | 1.06 | (371.5, 231.1) |

- **Đường thẳng khớp (xanh lá `#34d399`, stroke 2):** `U = 1.496 − 0.806·I` (bình phương tối thiểu trên 6 điểm). Vẽ từ I = 0 → (60.0, 94.1) tới I = 0,6 → (410.0, 246.1) (U = 1.012 V). Assert: mỗi chấm đỏ cách đường ≤ 6 px theo phương y.
- **Giao trục U:** chấm xanh lá r = 4 tại (60.0, 94.1); nhãn "ℰ ≈ 1,50 V" tại (68, 86) font 12 start, xanh lá.
- **Điểm A và B trên đường (vàng `#fbbf24`, r = 4, viền `currentColor`):** A = (0; 1,50) → (60.0, 92.9); B = (0,500; 1,09) → (351.7, 221.7). Nhãn "A" tại (68.0, 84.9) và "B" tại (359.7, 225.7) font 12.
- **Tam giác hệ số góc (nét đứt `currentColor`, stroke-opacity 0.6):** ngang từ A tới (351.7, 92.9), dọc xuống B. Nhãn "ΔI = 0,500 A" tại (206, 86.9) middle font 11; nhãn "ΔU = 0,41 V" tại (357.7, 157) start font 11. Nếu "ΔU = 0,41 V" chạm mép phải (x + chiều rộng chữ > 430) thì đặt nhãn bên trái cạnh dọc với `text-anchor="end"`.
- **Chú thích (font 11, `currentColor`):** "r = ΔU/ΔI = 0,82 Ω" tại (200, 44), `text-anchor="start"`. Không thêm chú thích nào khác (figcaption đã đủ).
- **Kiểm (assert):** điểm (0,3 A) nằm giữa (0,2) và (0,4) đúng khoảng cách (chia tuyến tính); 6 chấm đỏ theo đúng bảng; A, B nằm **trên** đường (|y − y_đường| < 1 px); giao trục đúng y = 94.1.
- **figcaption:** `Hình 3. Đồ thị U theo I của pin cũ: 6 điểm đo (đỏ), đường thẳng khớp U = 1,496 − 0,806·I (xanh), cắt trục U tại ℰ ≈ 1,50 V; hai điểm A, B trên đường cho r = ΔU/ΔI = 0,41/0,500 = 0,82 Ω.`
- **aria-label:** `Đồ thị U theo I với sáu điểm đo nằm gần một đường thẳng dốc xuống, cắt trục U tại 1,50 V; hai điểm A và B trên đường tạo tam giác hệ số góc.`

---

## Hình 4 — Hai đường U–I: pin mới thoải, pin cũ dốc

- **Vị trí:** mục V, ngay sau hộp `.tl-box--exp` "Lặp lại với pin mới", trước hộp "Điền bước còn thiếu". Mốc `<!--FIG4-->`.
- **Mục đích:** so sánh: hai pin có ℰ gần nhau nhưng r khác nhau → độ dốc khác hẳn. Minh hoạ cho bước điền trống và chuyện xe đồ chơi.
- **`data-exp="tn-l11-do-sdd-pin-02"`** đặt trên `<figure>` (hộp exp phía trên đã có cùng id — được phép trùng).
- **viewBox:** `0 0 440 290`. Cùng kiểu trục như hình 3 nhưng **trục I tới 0,8 A**: x từ 60 đến 410 ứng I = 0 → 0,8 (437.50 px/A); y như hình 3 (U 1,0 → 1,7). Hàm: `x = 60 + 437.5000·I`, `y = 250 − 314.2857·(U − 1,0)`. Vạch chia I: 0; 0,2; 0,4; 0,6; 0,8 ở x = 60.0, 147.5, 235.0, 322.5, 410.0. Vạch U như hình 3.
- **Pin cũ (đỏ `#f87171`):** 6 chấm r = 3,5 và đường `U = 1.496 − 0.806·I` từ I = 0 (60.0, 94.1) tới I = 0,6 (322.5, 246.1).

| Lần | I (A) | U (V) | (x, y) |
|---|---|---|---|
| 1 | 0.014 | 1.48 | (66.1, 99.1) |
| 2 | 0.066 | 1.44 | (88.9, 111.7) |
| 3 | 0.117 | 1.40 | (111.2, 124.3) |
| 4 | 0.191 | 1.35 | (143.6, 140.0) |
| 5 | 0.311 | 1.25 | (196.1, 171.4) |
| 6 | 0.534 | 1.06 | (293.6, 231.1) |

- **Pin mới (xanh dương `#38bdf8`):** 6 chấm r = 3,5 và đường `U = 1.583 − 0.259·I` từ I = 0 (60.0, 66.8) tới I = 0,8 (410.0, 131.9) (U = 1.376 V).

| Lần | I (A) | U (V) | (x, y) |
|---|---|---|---|
| 1 | 0.015 | 1.58 | (66.6, 67.7) |
| 2 | 0.073 | 1.56 | (91.9, 74.0) |
| 3 | 0.129 | 1.55 | (116.4, 77.1) |
| 4 | 0.217 | 1.53 | (154.9, 83.4) |
| 5 | 0.372 | 1.49 | (222.7, 96.0) |
| 6 | 0.701 | 1.40 | (366.7, 124.3) |

- **Nhãn đường:** "pin mới · r ≈ 0,26 Ω" màu xanh dương tại (250, 86) start font 12 (phía trên đường xanh); "pin cũ · r ≈ 0,82 Ω" màu đỏ tại (250, 200) start font 12 (phía dưới đường đỏ). Assert hai nhãn không chồng lên chấm nào (khoảng cách ≥ 10 px).
- **Đường dóng động cơ 0,5 A** (nét đứt `currentColor`, opacity 0.5): dọc x = 278.8 từ y = 250 lên tới đường xanh (y = 107.5); hai chấm nhỏ r = 3 nơi cắt hai đường, toạ độ tính từ phương trình: đỏ tại (278.8, 220.8) (U = 1,496 − 0,806·0,5 = 1,093 V) nhãn "1,09 V" (`text-anchor="end"`, x = 272, font 11, đỏ), xanh tại (278.8, 107.5) (U = 1,583 − 0,259·0,5 = 1,4535 V) nhãn "1,45 V" (`text-anchor="start"`, x = 285, font 11, xanh). Nhãn "0,5 A" ngay dưới trục tại (278.8, 266), middle, font 10, `currentColor`; giữ các số 0; 0,2; 0,4; 0,6; 0,8 (cách nhau 87,5 px nên "0,5 A" ở giữa 0,4 và 0,6 không chồng).
- **Kiểm (assert):** đường xanh thoải hơn đường đỏ (|hệ số góc| nhỏ hơn); hai đường cắt trục U tại y = 94.1 (đỏ) và 66.8 (xanh); chấm xanh I = 0,701 có x = 366.7 ≤ 410.
- **figcaption:** `Hình 4. Cùng hệ trục: pin mới (xanh) ℰ ≈ 1,58 V, r ≈ 0,26 Ω; pin cũ (đỏ) ℰ ≈ 1,50 V, r ≈ 0,82 Ω. Với dòng 0,5 A của động cơ, pin mới còn 1,45 V, pin cũ chỉ còn 1,09 V.`
- **aria-label:** `Hai đường thẳng U theo I trên cùng hệ trục: đường pin mới thoải, đường pin cũ dốc; tại 0,5 A pin mới còn 1,45 V, pin cũ còn 1,09 V.`

---

## Ghi chú cho build_figs.py / build_bundle.py

- Chèn hình **idempotent** tại các mốc `<!--FIGn-->` (giữ mốc trong `theory.src.html`, sinh `theory.html`).
- `data-exp` trên `<figure>`: hình 1 → `tn-l11-do-sdd-pin-03`, hình 4 → `tn-l11-do-sdd-pin-02`. Hình 2, 3 không cần (hộp exp mục II.3 đã mang `tn-l11-do-sdd-pin-01`).
- Sau khi chèn hình, chạy lại `lint_do_dai.py`: cảnh báo "đoạn liền 351 từ" ở mục V sẽ hết vì hình 3 và 4 là nhịp.
- `build_bundle.py`: `target.lesson_title` = "Bài 26. Thực hành: Đo suất điện động và điện trở trong của pin điện hoá", `class_name` = "Vật lí 11"; `exam` lấy từ `exam.json` cùng thư mục (6 câu); `theory_subtitle` gợi ý: "Thiết kế phương án đo ℰ và r của pin bằng biến trở, vôn kế, ampe kế; xử lý số liệu bằng đồ thị U–I".

---

## Cập nhật 5/10/2026 (sau kiểm chéo cỡ chữ) — ghi đè các số cỡ chữ/toạ độ nhãn ở trên khi lệch

Nguồn thật là `build_figs.py`. viewBox giữ 440 (thu ~0,8 ở 375 px) nên nhãn/số trục ≥ 13, chỉ số dưới 11, "0,5 A" 12 đậm.
- Hình 2: khoá K **đóng** (thanh gạt (120,50)→(160,50) nối hai chấm, "K" tại (140,34) middle); "ℰ, r" (14,118) font 14; M, N (50,·) font 13; "I" (310,40) 13; "R₀ = 2 Ω" end (368,104) 13; "Rₓ (0–100 Ω)" middle (240,220) 13; "U" (170,120) 13.
- Hình 3/4: số trục 13 (trục I y = 268, trục U x = 52); "U (V)" (12,15), "I (A)" (392,285) font 13.
- Hình 3: "ℰ ≈ 1,50 V" (68,70) 13; "A" (68,86); "B" end (344,207); "ΔI = 0,500 A" 13; "ΔU = 0,41 V" 13; "r = ΔU/ΔI = 0,82 Ω" 13.
- Hình 4: "pin mới · r ≈ 0,26 Ω" (250,78) 13; "pin cũ" (332,214) và "r ≈ 0,82 Ω" (332,229) 13; "1,09 V" end (271.8,237.8) 13; "1,45 V" start (285.8,100.5) 13; "0,5 A" (278.8,268) 12 đậm.
- Toạ độ điểm đo/đường khớp/điểm dóng 0,5 A (đỏ (278.8, 220.8), xanh (278.8, 107.5)) giữ nguyên. `Fig.check_segments` kiểm nhãn không bị nét thẳng (trừ lưới mờ) cắt xuyên.
