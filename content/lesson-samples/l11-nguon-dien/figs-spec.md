# Đặc tả hình — Bài 24. Nguồn điện (lesson_id 43)

Cho agent code viết `build_figs.py` (dùng `svg_lib.py` như bài `l11-dien-truong-deu`). Bốn mốc `<!--FIG1-->` … `<!--FIG4-->` trong `theory.src.html`, đánh số theo thứ tự xuất hiện. Mỗi hình chèn dưới dạng:

```html
<figure class="fig" data-tl="1" [data-exp="…"]><svg viewBox="…" role="img" aria-label="…">…</svg><figcaption>Hình n. …</figcaption></figure>
```

Quy ước chung (theo `references/hinh-svg.md`):
- viewBox rộng **≤ 440** (vừa 375 px). Chữ ≥ 11 px. Nét thân vật và chữ dùng `currentColor`.
- Màu: **đỏ `#f87171`** = dòng điện I / lực lạ (đại lượng "tác động"); **xanh dương `#38bdf8`** = electron / lực điện / đối tượng thứ hai; **xanh lá `#34d399`** = kết quả đo (điểm dữ liệu, đường khớp); **cam `#fb923c`** = nhãn phụ.
- Marker mũi tên: tiền tố riêng mỗi hình (`f1-`, `f2-`, `f3-`, `f4-`).
- **Không dùng `$…$` trong `<text>`.** Chỉ số dưới viết bằng `<tspan dy="4" font-size="9">…</tspan><tspan dy="-4">`. Chữ ℰ (suất điện động) viết bằng ký tự Unicode `ℰ` (U+2130) hoặc chữ "E" nghiêng — dùng `ℰ` nếu font hiện được, kiểm bằng ảnh; nếu mất chữ thì thay bằng "E".
- Nhãn `text-anchor="start"` với x ≥ 12 ở sát mép trái; nhãn sát mép phải phải kết thúc ≤ 428.
- Figcaption **≤ 7 từ, dùng đúng chuỗi ghi dưới** (bài đã 2.29x từ hiện ngay; 4 figcaption cộng ~26 từ → ~2.31x, dưới trần cứng 2.500 của lint; không thêm chữ nào khác vào hình ngoài nhãn đã liệt kê).
- Agent code **assert bằng toạ độ** (xem từng hình) trước khi chụp.

---

## Hình 1 — Hai quả cầu nối dây: dòng chỉ chạy một lát

- **Mốc:** `<!--FIG1-->` (mục II.1, ngay sau 4 gạch đầu dòng về quả cầu A, B).
- **Mục đích:** minh hoạ ý "dòng điện chỉ chạy khi còn chênh lệch điện thế; hai quả cầu trung hoà thì dòng ngừng" → vì sao cần nguồn.
- **viewBox:** `0 0 440 180`. Hai khung nhỏ trái/phải, mỗi khung rộng ~205.
- **Khung trái (x 10–215): "Lúc mới nối"**
  - Quả cầu A: `circle` tâm (60, 80), r = 22, nét `currentColor`, fill nhạt (opacity 0.15). Chữ "A" ở tâm (font 13, bold). Nhãn "+q" phía trên tâm, y = 48, `text-anchor="middle"`, màu đỏ.
  - Quả cầu B: tâm (165, 80), r = 22. Chữ "B" ở tâm. Nhãn "−q" phía trên, y = 48, màu xanh dương.
  - Dây dẫn: `line` từ (82, 80) đến (143, 80), nét 2.
  - Mũi tên **electron** (xanh dương): phía TRÊN dây, từ (135, 64) đến (92, 64) — **chiều B → A** (electron chạy từ quả cầu âm sang quả cầu dương). Nhãn "electron" đặt trên mũi tên, y = 58, x = 113, `middle`, font 11, xanh dương.
  - Mũi tên **dòng điện I** (đỏ): phía DƯỚI dây, từ (92, 96) đến (135, 96) — **chiều A → B** (ngược với electron). Nhãn "I" dưới mũi tên, y = 112, x = 113, `middle`, đỏ, font 12 nghiêng.
  - Dòng chú thích dưới khung: "V<tspan sub>A</tspan> > V<tspan sub>B</tspan>: có dòng" tại (112, 150), `middle`, font 12. (Dùng ký tự ">" thật trong text, không có `$`.)
- **Khung phải (x 225–430): "Một lát sau"**
  - Hai quả cầu cùng kích cỡ: A tâm (275, 80), B tâm (380, 80); chữ "A", "B" ở tâm; nhãn trên mỗi quả "0" (y = 48, `middle`, `currentColor`) biểu thị trung hoà.
  - Dây dẫn (297, 80)–(358, 80), **không có mũi tên nào**.
  - Chú thích dưới khung: "V<tspan sub>A</tspan> = V<tspan sub>B</tspan>: dòng ngừng" tại (327, 150), `middle`, font 12.
- Đường phân cách dọc mờ (dashed, opacity 0.3) tại x = 220 từ y = 30 đến 165. Tiêu đề nhỏ mỗi khung ở y = 24: "Lúc mới nối" (x = 112) và "Một lát sau" (x = 327), font 11, cam.
- **Assert:** mũi tên electron có x_đầu > x_cuối (hướng về A bên trái); mũi tên I có x_đầu < x_cuối (hướng về B bên phải); khung phải không có `marker-end`.
- **aria-label:** "Hai quả cầu A dương và B âm nối dây: lúc đầu electron chạy từ B sang A, dòng điện từ A sang B; sau một lát hai quả cầu trung hoà, dòng ngừng."
- **figcaption:** "Hình 1. Dòng chỉ chạy một lát"

---

## Hình 2 — Bên trong nguồn: lực lạ đẩy điện tích ngược điện trường

- **Mốc:** `<!--FIG2-->` (mục II.2, sau 4 gạch đầu dòng về lực lạ, trước hộp định nghĩa suất điện động).
- **Mục đích:** hình quan trọng nhất bài — thấy (1) dòng ở mạch ngoài đi từ (+) về (−), (2) trong nguồn dòng đi từ (−) lên (+), (3) lực lạ hướng lên (ngược điện trường), lực điện hướng xuống, lực lạ dài hơn.
- **viewBox:** `0 0 440 240`.
- **Nguồn điện:** `rect` x = 140, y = 50, w = 150, h = 140, rx = 8, nét `currentColor` 2, fill opacity 0.06.
  - Bản cực dương: `rect` x = 160, y = 58, w = 110, h = 8, fill đỏ opacity 0.6. Nhãn "cực (+)" tại (158, 80) `start`, font 12, đỏ.
  - Bản cực âm: `rect` x = 160, y = 174, w = 110, h = 8, fill xanh dương opacity 0.6. Nhãn "cực (−)" tại (158, 168) `start`, font 12, xanh dương.
  - Điện tích dương bên trong: `circle` tâm (200, 125), r = 10, fill cam opacity 0.5, chữ "+" ở tâm (font 13 bold).
  - **Lực lạ** (đỏ, mũi tên dài): từ (200, 113) lên (200, 72) — chiều **từ (−) lên (+)**, dài 41. Nhãn "lực lạ" tại (208, 95) `start`, font 12, đỏ.
  - **Lực điện** (xanh dương, mũi tên ngắn): từ (200, 137) xuống (200, 162) — chiều **từ (+) xuống (−)**, dài 25 (ngắn hơn lực lạ vì A_lạ > A_điện). Nhãn "lực điện" tại (208, 155) `start`, font 12, xanh dương.
  - Điện trường trong nguồn: mũi tên mảnh, `currentColor` opacity 0.5, dashed, từ (260, 70) xuống (260, 170) — **chiều từ bản (+) sang bản (−)**. Nhãn "điện trường" xoay dọc hoặc đặt tại (266, 125) `start`, font 10, opacity 0.7. (Nếu chật, bỏ nhãn chữ và chỉ giữ chữ "E" nghiêng tại (266, 125) — không phải ℰ.)
- **Mạch ngoài (dây dẫn, nét 2, `currentColor`):** từ giữa bản (+): (215, 58) lên (215, 22) → sang phải tới (400, 22) → xuống (400, 218) → sang trái tới (215, 218) → lên (215, 182) nối bản (−). (Đi ra từ bản (+) ở mép trên hộp, vào bản (−) ở mép dưới; đoạn dây xuyên qua vỏ hộp vẽ liền, không sao.)
  - Bóng đèn trên dây phải: `circle` tâm (400, 120), r = 14, nét 2; hai đường chéo bên trong (chữ X). Nhãn "đèn" tại (400, 150) `middle`, font 11 (không đặt bên phải đèn vì sẽ vượt x = 428).
  - **Ba mũi tên I** màu đỏ, nhãn "I" nghiêng 12 px đỏ:
    1. Trên dây trên: từ (300, 22) đến (340, 22) — **sang phải** (ra khỏi cực +). Nhãn "I" tại (320, 15) `middle`.
    2. Trên dây phải, đoạn dưới đèn: từ (400, 160) đến (400, 195) — **xuống**. Nhãn "I" tại (410, 180) `start`.
    3. Trên dây dưới: từ (340, 218) đến (300, 218) — **sang trái** (đi về cực −). Nhãn "I" tại (320, 234) `middle`.
  - Mũi tên dòng **trong nguồn**: đỏ, mảnh hơn (nét 1.5), từ (175, 165) lên (175, 85) — **từ (−) lên (+)**, cùng chiều lực lạ. Nhãn "I" tại (165, 128) `end`, font 12 đỏ.
  - Nhãn "mạch ngoài" tại (300, 50) `middle`, font 11, cam.
- **Assert:** (1) mũi tên lực lạ: y_đầu > y_cuối (hướng lên) và độ dài > độ dài lực điện; (2) lực điện y_đầu < y_cuối (hướng xuống); (3) điện trường y_đầu < y_cuối (từ + xuống −); (4) dòng trong nguồn y_đầu > y_cuối (lên); (5) I dây trên x_đầu < x_cuối, I dây dưới x_đầu > x_cuối, I dây phải y_đầu < y_cuối — tức là một vòng theo chiều kim đồng hồ ra từ (+) về (−); (6) mọi `<text>` có x + ước lượng bề rộng ≤ 428.
- **aria-label:** "Mạch kín gồm nguồn và bóng đèn. Ở mạch ngoài dòng điện đi từ cực dương qua đèn về cực âm. Bên trong nguồn, lực lạ đẩy điện tích dương từ cực âm lên cực dương, ngược chiều điện trường và lực điện; dòng điện trong nguồn đi từ cực âm lên cực dương."
- **figcaption:** "Hình 2. Lực lạ đẩy ngược điện trường"

---

## Hình 3 — Đồ thị U theo I của pin (số liệu thí nghiệm 02)

- **Mốc:** `<!--FIG3-->` (mục II.3, ngay sau bảng số liệu R–I–U, trước câu "Độ dốc đường thẳng = −r.").
- **data-exp:** `tn-l11-nguon-dien-02` (đặt trên `<figure>`).
- **Mục đích:** 5 điểm đo nằm trên đường thẳng U = 1,50 − 1,0·I; đường cắt trục U tại ℰ = 1,50 V và cắt trục I tại dòng đoản mạch 1,5 A; độ dốc = −r.
- **viewBox:** `0 0 440 300`.
- **Hệ trục (chia TUYẾN TÍNH, bắt buộc):**
  - Gốc O tại (60, 250). Trục I nằm ngang tới (420, 250), mũi tên ở đầu; trục U thẳng đứng tới (60, 22), mũi tên ở đầu.
  - Tỉ lệ: **1 A = 218,75 px** (I từ 0 đến 1,6 A chiếm 350 px: x = 60 + 218,75·I); **1 V = 137,5 px** (U từ 0 đến 1,6 V chiếm 220 px: y = 250 − 137,5·U).
  - Vạch chia trục I tại I = 0,5; 1,0; 1,5 → x = 169,4; 278,8; 388,1; nhãn "0,5", "1,0", "1,5" dưới trục (y = 268, `middle`, font 11). Nhãn trục "I (A)" tại (420, 272) `end`, font 12.
  - Vạch chia trục U tại U = 0,5; 1,0; 1,5 → y = 181,25; 112,5; 43,75; nhãn "0,5", "1,0", "1,5" bên trái trục (x = 52, `end`, font 11). Nhãn trục "U (V)" tại (66, 18) `start`, font 12. Nhãn "0" tại (52, 262) `end`.
- **Đường thẳng U = 1,50 − 1,0·I** (xanh lá, nét 2):
  - Đoạn liền từ I = 0 (x = 60, y = 43,75) đến I = 0,70 (x = 213,1; y = 250 − 137,5·0,80 = 140,0).
  - Đoạn **đứt nét** (dashed 6,4) từ I = 0,70 (213,1; 140,0) đến I = 1,5 (x = 388,1; y = 250) — phần ngoại suy tới đoản mạch.
- **5 điểm dữ liệu** (circle r = 4,5, fill xanh lá, nét `currentColor` 1), toạ độ TÍNH từ bảng (x = 60 + 218,75·I; y = 250 − 137,5·U):
  | I (A) | U (V) | x | y |
  |---|---|---|---|
  | 0,10 | 1,40 | 81,9 | 57,5 |
  | 0,15 | 1,35 | 92,8 | 64,4 |
  | 0,30 | 1,20 | 125,6 | 85,0 |
  | 0,50 | 1,00 | 169,4 | 112,5 |
  | 0,60 | 0,90 | 191,3 | 126,3 |
- **Nhãn:**
  - Tại giao với trục U: chấm nhỏ đỏ tại (60, 43,75) và nhãn "ℰ = 1,50 V" tại (68, 40) `start`, font 12, đỏ (nếu ℰ không hiện, dùng "suất điện động 1,50 V").
  - Tại giao với trục I: chấm nhỏ đỏ tại (388,1; 250) và nhãn "đoản mạch 1,5 A" tại (386, 238) `end`, font 11, đỏ.
  - Tam giác độ dốc (nét mảnh, opacity 0.6): hai đoạn từ điểm (I = 0,10; U = 1,40) = (81,9; 57,5) đi ngang tới x = 191,3 (y = 57,5), rồi xuống tới (191,3; 126,3) — tức là tới điểm (0,60; 0,90). Nhãn "ΔI = 0,50 A" tại (136, 52) `middle`, font 10; nhãn "ΔU = −0,50 V" tại (197, 95) `start`, font 10. Nhãn "độ dốc = −r = −1,0 Ω" tại (230, 200) `start`, font 11, xanh lá.
- **Assert (bắt buộc trong `build_figs.py`):** với mỗi điểm, `abs(U - (1.50 - 1.0*I)) < 1e-9` và toạ độ pixel tính đúng công thức tỉ lệ (sai khác < 0,5 px); khoảng cách pixel giữa các vạch chia 0,5 A bằng nhau (109,4 px) và giữa các vạch 0,5 V bằng nhau (68,75 px); hai đầu đường thẳng đúng (60; 43,75) và (388,1; 250); mọi nhãn kết thúc ≤ 428.
- **aria-label:** "Đồ thị hiệu điện thế hai cực U theo cường độ dòng điện I của pin: năm điểm đo nằm trên đường thẳng dốc xuống, cắt trục U tại 1,50 vôn là suất điện động và cắt trục I tại 1,5 ampe là dòng đoản mạch; độ dốc bằng trừ r bằng trừ 1,0 ôm."
- **figcaption:** "Hình 3. U giảm tuyến tính theo I"

---

## Hình 4 — Sơ đồ mạch kín của bài toán mẫu

- **Mốc:** `<!--FIG4-->` (mục V, ngay sau hộp Đề bài, trước câu "Với mỗi cụm, tự hỏi…").
- **Mục đích:** học sinh nhìn thấy nguồn (ℰ, r), R, ampe kế nối tiếp, vôn kế mắc vào hai cực nguồn, và chiều I.
- **viewBox:** `0 0 440 210`.
- **Vòng dây (nét 2, `currentColor`):** hình chữ nhật góc (70, 40) – (380, 40) – (380, 170) – (70, 170) – về (70, 40), **ngắt** ở chỗ đặt nguồn, ampe kế, R.
- **Nguồn** trên cạnh trái, tâm (70, 105): ký hiệu pin — vạch dài mảnh (cực +) ở trên: `line` (52, 97)–(88, 97) nét 2; vạch ngắn dày (cực −) ở dưới: `line` (60, 113)–(80, 113) nét 4. Dây nối từ (70, 40) xuống (70, 97) và từ (70, 113) xuống (70, 170). Nhãn "+" tại (44, 94) `end`, font 12 đỏ; "−" tại (44, 118) `end`, xanh dương. Nhãn nguồn đặt **bên trong vòng, dưới nhánh vôn kế**: "ℰ = 9,0 V" tại (84, 150) `start`, font 12; "r = 1,0 Ω" tại (84, 164) `start`, font 12. (Nếu ℰ không hiện: "E = 9,0 V".)
- **Vôn kế V** mắc vào hai cực nguồn: `circle` tâm (160, 105), r = 14, nét 2, chữ "V" ở tâm (font 13). Dây: từ (70, 85) — là điểm trên dây cạnh trái, phía trên cực (+) — sang phải tới (160, 85) rồi xuống (160, 91); từ (70, 125) sang phải tới (160, 125) rồi lên (160, 119). (Nhánh vôn kế song song với nguồn, nằm bên trong vòng; nhãn ℰ/r ở y = 150/164 nằm dưới dây (70,125)–(160,125), không đè.)
- **Ampe kế A** trên cạnh trên, tâm (225, 40): `circle` r = 14, chữ "A" ở tâm; dây ngắt từ x = 211 đến 239.
- **Điện trở R** trên cạnh phải, tâm (380, 105): `rect` x = 370, y = 85, w = 20, h = 40, nét 2, fill opacity 0.1; dây ngắt từ y = 85 đến 125. Nhãn "R = 8,0 Ω" tại (362, 109) `end`, font 12 (bên trái của R, trong vòng).
- **Mũi tên I** (đỏ, nhãn "I" nghiêng): trên cạnh trên đoạn giữa ampe kế và góc phải: từ (290, 40) đến (330, 40) — **sang phải** (ra từ cực +). Nhãn "I" tại (310, 32) `middle`. Mũi tên thứ hai trên cạnh dưới: từ (250, 170) đến (210, 170) — **sang trái** (về cực −). Nhãn "I" tại (230, 186) `middle`.
- **Assert:** mũi tên I trên có x_đầu < x_cuối, mũi tên I dưới có x_đầu > x_cuối (vòng theo chiều kim đồng hồ, ra từ cực + ở trên); vạch dài (+) nằm phía trên vạch ngắn (−) (y_dài < y_ngắn); vôn kế nối vào hai điểm nằm hai bên nguồn trên cạnh trái (y = 85 < 97 và y = 125 > 113); nhãn R kết thúc ≤ 362; mọi `<text>` ≤ 428.
- **aria-label:** "Sơ đồ mạch kín: nguồn có suất điện động 9,0 vôn và điện trở trong 1,0 ôm trên cạnh trái, vôn kế mắc vào hai cực nguồn, ampe kế nối tiếp trên cạnh trên, điện trở 8,0 ôm trên cạnh phải; dòng điện đi từ cực dương qua ampe kế, qua R, về cực âm."
- **figcaption:** "Hình 4. Mạch kín bài toán mẫu"

---

## Việc của agent code sau khi vẽ

1. `python3 build_figs.py` → sinh `theory.html` từ `theory.src.html` (thay mốc `<!--FIGn-->` bằng `<figure>`; idempotent qua `data-tl="1"`).
2. Chạy lại cả 4 lint trên `theory.html` (lint_theory, lint_do_dai — tổng phải ≤ 2.300 từ kể cả figcaption, check_quizzes, thi_nghiem).
3. `build_bundle.py` lấy `exam` từ `exam.json` (6 câu) và `theory.html`; target `{"class_name": "Vật lí 11", "lesson_title": "Bài 24. Nguồn điện"}`; `theory_subtitle`: "Nguồn điện, suất điện động, điện trở trong và định luật Ohm cho toàn mạch". Validate bằng `validate_bundle.mts`.
4. Xem thử 375 px (`build_preview.py` + `chup_anh.py --kiem-tran` rồi `chup_anh.py`), **xem ảnh bằng mắt** từng hình: nhãn "lực lạ"/"lực điện" (Hình 2) không đè mũi tên; nhãn ℰ hiện đúng (nếu font không có U+2130 thì thay "E"); bảng ghép nguồn 2 cột và bảng Pin mới/Pin cũ không bị bóp chữ.
