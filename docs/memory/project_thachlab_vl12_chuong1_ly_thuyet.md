---
name: project-thachlab-vl12-chuong1-ly-thuyet
description: Chương 1 Vật lí 12 (Vật lí nhiệt) — soạn nốt bài 3 Nội năng/Định luật 1 và bài 4 Thực hành đo nhiệt thành lý thuyết tương tác (4/10/2026), CHƯA ghi DB
metadata:
  type: project
---

## Mục tiêu
Thầy yêu cầu 4/10/2026: "skill lý thuyết tương tác cho các bài còn lại của chương 1 vật lý 12".
Chương 1 (Vật lí nhiệt, `chapter_id=2`) có 6 mục: bài 1 Sự chuyển thể (lesson 2, item `ly_thuyet` 8),
bài 2 Thang nhiệt độ (lesson 3, item 171), bài 3 Nội năng – Định luật 1 (lesson 4, item 173),
bài 4 Thực hành đo nhiệt (lesson 5, item 175), Kiểm tra giữa kì (96), Kiểm tra chương (97).
Thầy chốt phạm vi: **bài 3 (viết đầy đủ lại) + bài 4**, bỏ 2 tiết kiểm tra.

## Vì sao phải làm lại
- Bài 1 và bài 2 đã có bản tương tác (bài 2 soạn 4/10, commit `a7d5cd53c`).
- **Bài 3 bản trên web chỉ 460 từ và THIẾU HẲN định luật I** (`ΔU = A + Q`) — có 4 mục: khái niệm nội năng,
  hai cách đổi nội năng, nhiệt lượng/nhiệt dung riêng, rồi cắt cụt ở "4. Định luật I" (còn "A > 0: vật nhận
  công; A" là hết). Đây là chỗ trống nặng nhất của chương.
- **Bài 4 bản cũ là văn SGK** (nhiệt dung riêng + 4.1/4.2 + nhiệt nóng chảy riêng), lặp tiêu đề
  "Hình 4.1"/"1. Mục đích thí nghiệm" hai lần, không quiz, không nhịp.

## Đã làm (4/10/2026)
Hai thư mục mới trong `content/lesson-samples/`, mỗi thư mục: `theory.src.html` (nguồn có mốc `<!--FIGn-->`),
`build_figs.py` (4 hình SVG qua `svg_lib.py`), `theory.html`, `build_bundle.py`, `bundle.json`, `xem-thu/`.

- `l12-noi-nang-dl1/` — **Bài 3. Nội năng. Định luật 1 của nhiệt động lực học** (lesson_id **4**),
  tiền tố quiz `tl4-q*`. 6 mục: mở bài "hai thanh chạm lúc 6 giờ sáng" (kim loại 5 °C buốt hơn gỗ cùng 5 °C)
  → nội năng → hai cách đổi nội năng (thí nghiệm bơm xe) → `Q = mcΔt` (bảng số liệu 0,500 kg, 500 W) →
  `ΔU = A + Q` + quy ước dấu + bảng bốn quá trình → ba cái bẫy (nội năng ↔ nhiệt độ · nhiệt lượng không
  chứa trong vật · dấu của A) → Trả bài 6 câu → bài toán mẫu bơm xe đạp (60 J nhận, 15 J toả → ΔU = +45 J)
  + điền bước trống (90 J/30 J) + biến thể xilanh (nhận 200 J, sinh 120 J → +80 J) → thử thách ⭐–⭐⭐⭐
  → "Mang về". 6 quiz · 16 details · 4 hình · 2 thí nghiệm `tn-l12-noinang-01..02`.
- `l12-thuc-hanh-nhiet/` — **Bài 4. Thực hành đo nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi
  riêng** (lesson_id **5**), tiền tố `tl5-q*`. Xoay từ "đọc SGK" sang **kỹ năng thực hành**: dụng cụ và
  cách suy `Q = Pτ` → đọc đồ thị t(τ) (đoạn ngang = chuyển thể) → `c = Pτ/(mΔt)` với bảng 0,200 kg/150 W
  → bảng một lần đun đá liên tục (tan 334 s · nóng 0→100 °C mất 838 s · sôi 2 260 s → ra λ, c, L) →
  3 cái bẫy (nhiệt kế đứng yên ≠ hết truyền nhiệt · hai cách tính c · trộn đơn vị) → Trả bài 6 câu →
  bài toán mẫu nhiệt hoá hơi (0,150 → 0,100 kg, 420 W, 810 s) + điền bước + biến thể → thử thách ⭐–⭐⭐⭐
  (bài ⭐⭐⭐: 0,500 kg đá −10 °C → hơi 100 °C ≈ 50,6 phút, hoá hơi chiếm 74%). 6 quiz · 17 details · 4 hình
  · 2 thí nghiệm `tn-l12-thuchanh-01..02`.

## Số đo (đừng đoán lại)
- Bài 3: 39,8 KB · **2.494 từ hiện ngay** (~18 phút) · 6 mục `<h3>` · từng mục ≤ 467 từ · đoạn liền dài
  nhất 335 từ · tới việc đầu 129 từ.
- Bài 4: 42,7 KB · **2.492 từ hiện ngay** · từng mục ≤ 292 từ · tới việc đầu 143 từ.
- Cả hai đều **0 lỗi cứng**, chỉ còn 1 cảnh báo ⚠ "tổng > 2.000 từ" (trần lỗi là 2.500). Hạn mức + lý do:
  `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`. Muốn xuống dưới 2.000 phải bỏ hẳn một mục — đã cân nhắc và
  giữ, vì bài 3 trước đó 4.215 từ còn bài 4 là văn SGK.
- `lint_theory` OK · `check_quizzes` OK (mỗi quiz đúng 1 `tl-ok`) · `thi_nghiem` OK (41 mục trong
  `content/thi-nghiem/index.json`) · `validate_bundle` `ok:true` cho cả hai bundle.

## Bài học rút ra (tốn thời gian nhất ở lượt này)
1. **Đo độ dài trước khi tin là xong**: bản nháp bài 3 là 3.015 từ (vượt trần 2.500). Phải cắt 4 lượt
   (3.015 → 2.585 → 2.530 → 2.494). Cách cắt hiệu quả nhất: (a) gộp `<h4>` con khi mục vượt 480 từ,
   (b) chuyển bảng/danh sách dài vào `<details>` (chữ trong `<details>` **không** tính vào "từ hiện ngay",
   nhưng **`<summary>` thì có**), (c) đổi câu văn dài thành bullet từ khoá.
2. **`lint_do_dai.py` tính cả `<summary>` của `<details>`** — đừng viết summary dài.
3. **"Đoạn liền" không tính tiêu đề `<h3>`/`<h4>` là nhịp** — một mục có 3 `<details>` mà giữa chúng là
   văn xuôi dài vẫn bị báo. Cách chữa: chèn `<details>`/quiz thật vào giữa đoạn văn, hoặc bọc đoạn văn
   vào `<details>`.
4. **Bẫy vẽ SVG hay gặp lại y như tài liệu skill cảnh báo**: nhãn đè mũi tên (Hình 1 bài 3: "rút nhiệt"
   nằm trên bàn tay), nhãn đè tiêu đề (Hình 2 bài 3: "đẩy xuống" nằm trên dòng "a) Thực hiện công"),
   hộp chữ tràn `viewBox` (Hình 1 bài 4: bảng số liệu bị cắt 2 dòng + câu ghi chú). **Chỉ ảnh chụp mới
   thấy** — `--kiem-tran` chỉ bắt tràn ngang, không bắt chồng nhãn. Sửa bằng cách: chừa một "làn" riêng
   cho mỗi thứ (tiêu đề y ≤ 24, hàng nhãn y ≈ 50–70, hình vẽ y ≥ 90), và chiều cao `viewBox` phải đủ cho
   dòng cuối (kiểm bằng cách đếm y lớn nhất + ~16).
5. **Khi soạn bài thực hành, nội dung phải khác bài lý thuyết cùng chương**: bài 4 không dạy lại
   `Q = mcΔt` mà dạy *đo* nó — dụng cụ, đồ thị có đoạn ngang, hai cách tính c, sai số hệ thống. Nếu viết
   theo SGK thì trùng bài 3 gần hết.
6. **Tách mục khi một `<h3>` phình ra**: bài 4 ban đầu có "4. Tính nhiệt dung riêng" gộp cả thí nghiệm
   bếp điện; đổi thành `<h3>III. Thí nghiệm đo nhiệt lượng bằng bếp điện</h3>` thì vừa nhẹ mục vừa có nhịp.

## Đề xuất bị bỏ (để lượt sau khỏi làm lại từ đầu)
Trong phiên 4/10 có soạn nháp một hướng **khác** cho bài 4 rồi không dùng (bản đã đăng là bản thực hành
thuần, xem mục trên). Hướng bị bỏ: đổi bài 4 thành *"nhiệt lượng và chuyển thể"* — 7 quiz (thêm bài tập
tính `Q = λm`, `Q = Lm`; thêm câu **3 nhiệt kế đựng trong một cốc** để nói rõ một phép đo chỉ ra một giá
trị, muốn so ba chất phải làm ba phép đo cùng điều kiện), Hình 4 = "ba đại lượng, hai cách tính". Bản nháp
bị từ chối ghi đè nên **không còn trên đĩa** — nếu thầy muốn đi hướng đó thì phải soạn lại. Lý do chọn
bản hiện tại: giữ đúng mục tiêu "thực hành" của bài 4, và phần `Q = λm`, `Q = Lm` đã có trong bảng số liệu
một lần đun đá liên tục (mục II.4).

## Kiểm chéo độc lập + 11 lỗi đã sửa (4/10/2026)
Nhờ subagent tự tính lại toàn bộ con số và kiểm từng quiz (không dùng lại kết quả của người soạn). Kết quả:
11 mục sai, trong đó **3 lỗi thật phải sửa** — đây là các bẫy đáng nhớ cho mọi bài sau:

1. **Trùng đáp án (lỗi chết người)** — bài 4 câu 3: hai phương án A và B cùng ghi $3\ 750$ J/(kg·K) nhưng
   A bị gắn `tl-no`. Học sinh chọn A bị chấm sai oan. **Quy tắc: sau khi xáo đáp án phải đọc lại cả bốn
   phương án như một học sinh, không chỉ kiểm "có đúng 1 `tl-ok`"** — `check_quizzes.py` và `lint_theory.py`
   không bắt được lỗi này.
2. **Hướng sai số hệ thống bị viết ngược** — chỗ này mình đã hiểu sai vật lí rồi viết vào cả 4 vị trí
   (bài 3 mục II.5, bài 4 mục II.3 + Trả bài 6 + bundle). Sự thật: `c = Pτ/(m·Δt)`; nhiệt mất ra môi
   trường/đun nóng bình ⇒ `Δt` **nhỏ** hơn thực tế ⇒ **c đo được CAO HƠN** giá trị thật. Muốn `c` **thấp
   hơn** thì nhiệt kế phải **đọc cao hơn** thực tế. (SBT Vật lí 12 KNTT Bài 4 cũng hỏi đúng ý này, đáp án
   "cao hơn thực tế vì hiệu suất bộ thí nghiệm < 100%".) Còn với `λ`, `L` thì tính bằng `Pτ/m`, mất nhiệt
   làm **`λ`, `L` đo được lớn hơn** — hai chiều khác nhau, đừng viết chung một câu.
   **Mẹo kiểm: viết `Pτ = m·c·Δt` rồi tự hỏi nhiệt mất đi thì `Δt` tăng hay giảm, `c` sẽ đổi theo chiều nào.**
3. **Số liệu sai hệ số 2 vì trộn hai khối lượng** — bài 4 bảng "một lần đun đá": cột 0,100 kg nhưng thời
   gian giai đoạn nâng nhiệt lại lấy của 0,200 kg (838 s thay vì 419 s), và giá trị $c$ vẫn ghi 4,19.10³
   (không khớp: $83\ 800/(0{,}100 \times 100) = 8\ 380$). **Quy tắc: mỗi bảng số liệu phải kiểm lại toàn bộ
   dòng theo đúng một khối lượng**; hình vẽ SVG cũng phải vẽ theo đúng bảng đó.

Các lỗi còn lại (đã sửa hết): Hình 3 bài 4 ghi phần trăm sai (1,1 / 17,5 / 22% → **0,7 / 11,0 / 13,8 / 74,5%**,
cộng lại phải bằng 100%); câu "gấp gần 7 lần" (thực ra 2260/419 = **5,4 lần**); kiểm tra chéo trộn số của
thử thách ⭐⭐⭐ vào mục II.4 (2 260/3 013 ≈ 75% mới đúng); mô tả lỗi sai bậc 10 ($Q/m_1 = 2,27.10^6$, đúng
bậc 10⁶ chứ không phải 10⁵); câu hỏi "vì sao II.3 ra *thấp* hơn" (thực tế mục II.3 cũng ra **cao** hơn —
nay cả hai chỗ đều nói "cùng hướng, đúng dấu hiệu sai số hệ thống"); bài 3 **thiếu hẳn heading III** nên
nhảy II → IV (đã đánh số lại, cập nhật "7 mục" → "6 mục"); bài 4 ghi "7 câu tự kiểm tra" nhưng chỉ có 6
quiz; **`$c = 4180$` nằm trong `<text>` của SVG** — `ContentHtml` render KaTeX thành `<span>`/MathML, SVG
**không vẽ** `<span>` trong `<text>` nên chữ sẽ mất; nay đã đổi thành chữ thường "c nước = 4180". Quét cả
`content/lesson-samples/*/theory.html`: chỉ bài 3 dính lỗi này.
Xáo lại vị trí đáp án đúng cho khỏi dồn một chỗ: bài 3 nay là B–C–A–B–D–B, bài 4 là B–A–B–B–C–B.

**Bài học về quy trình**: `lint_theory.py` + `check_quizzes.py` + `validate_bundle.mts` đều **không** kiểm
số học và **không** kiểm hai phương án có trùng nhau. Bắt buộc có một lượt **tự tính lại bằng tay hoặc
nhờ subagent tính độc lập** trước khi báo thầy, và lượt đó phải đọc từng phương án của từng quiz.

## Còn chờ
1. **Thầy xem bản xem thử** rồi duyệt:
   `content/lesson-samples/l12-noi-nang-dl1/xem-thu/xem-thu.html` và
   `content/lesson-samples/l12-thuc-hanh-nhiet/xem-thu/xem-thu.html` (mở bằng Chrome, bấm thử radio + details).
2. **Chưa ghi DB.** Lệnh trên Mac (chỉ ghi cột `body_html` của mục `ly_thuyet`, tự sao lưu):
   ```
   cd /Users/MAC/Projects/thachlab
   bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l12-noi-nang-dl1/theory.html 4
   bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l12-thuc-hanh-nhiet/theory.html 5
   # rồi deploy: git -C .claude/worktrees/deploy-tree checkout --detach origin/main && (cd .claude/worktrees/deploy-tree && bash scripts/deploy.sh)
   ```
   ⚠ **lesson 4 = "Bài 3. Nội năng…"**, **lesson 5 = "Bài 4. Thực hành…"** (`chapter_id=2`, lớp 12) —
   số lesson lệch 1 so với số bài, đọc kỹ dòng script in ra trước khi xác nhận.
3. Đề Luyện tập dùng chính 6 câu tự kiểm tra trong bài; **nếu sau này muốn đăng cả đề** thì dùng
   `upload-lesson.mts`, còn `cap-nhat-ly-thuyet.sh` chỉ chạm mục Lý thuyết (quy tắc thầy chốt 4/10/2026).
4. Kiểm chéo độc lập nội dung 2 bài (subagent) — xem kết quả trong phiên; nếu có phát hiện thì sửa rồi
   chạy lại `lint_theory` + `validate_bundle` (chỉ sửa chữ thì không cần chạy lại toàn bộ).
