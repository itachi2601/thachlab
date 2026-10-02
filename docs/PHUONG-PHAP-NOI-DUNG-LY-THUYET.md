# Phương pháp tạo nội dung lý thuyết — độ dài, nhịp đọc, cách kiểm

**Đọc file này khi**: soạn/sửa một bài lý thuyết cho học sinh, quyết định cắt hay giữ một mục, hoặc
khi thấy một bài "đọc mệt" mà không rõ vì sao.

Liên quan: `docs/QUY-TAC-THIET-KE.md` (quy tắc UI theo nghiên cứu — file này chỉ nói về **nội dung/độ
dài**, mã quy tắc `N*`, `C*`, `L*` dẫn từ đó), skill `.claude/skills/soan-bai-ly-thuyet-tuong-tac/`
(14 nét phong cách + quy trình soạn), và công cụ đo
`.claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py`.

Chốt ngày 2/10/2026 sau khi đo 5 bài lý thuyết đang có. Số liệu trong file là **số đo thật**, không
phải ước lượng.

---

## 1. Bài dài ảnh hưởng gì — cơ chế, không phải "mất tập trung" chung chung

Nói rõ một chỗ hay bị nói sai trước: **không có bằng chứng "attention span của giới trẻ giảm còn 8
giây"** — đó là con số không có nguồn, đã bị bác ([BBC, *Busting the attention span myth*](https://www.stage.bbc.co.uk/news/health-38896790)).
Học sinh vẫn ngồi được 90 phút xem bóng. Vấn đề không phải sức chịu đựng, mà là **ngưỡng bỏ cuộc khi
chưa thấy phần thưởng** và **chi phí quay lại bài sau mỗi lần bị ngắt**.

| Cơ chế | Biểu hiện trong bài đọc dài | Mã |
|---|---|---|
| Phần thưởng bị trì hoãn | Đọc 700 từ mới tới chỗ được làm gì đó → bỏ giữa chừng; tiến độ khởi đầu 0% làm nản | L2, N5 |
| Mắt chỉ quét 20–28% chữ | Mục dài ở giữa bị bỏ qua, kể cả phần "cái bẫy" — phần có giá trị nhất | G3, B8 |
| Không truy xuất thì không nhớ | Đọc liền một mạch thấy "hiểu rồi" nhưng không qua tự trả lời → trôi sau vài ngày (ảo giác đã hiểu) | L1 |
| Dài = nhiều cửa sổ bị ngắt | 25 phút đọc trên điện thoại có Zalo/TikTok chạy nền = 5–10 lần ngắt, mỗi lần trả giá khởi động lại | G2, B4 |
| Chi tiết dẫn dụ | Văn xuôi dài quanh một ý làm giảm nhớ và vận dụng so với bản cô đọng (Harp & Mayer 1998) | N1, N7 |

### Về "thời đại video ngắn"

Nghiên cứu EEG của Yan et al. 2024: mức dùng video ngắn cao tương quan với **giảm hoạt động theta ở
vùng điều hành/kiểm soát xung**, trong khi **kết quả làm bài đo được vẫn bình thường**
([bài gốc, *Frontiers in Human Neuroscience*](https://doi.org/10.3389/fnhum.2024.1383913);
[tóm tắt có bàn về thiết kế dạy học](https://scienceandresearch.ue-varna.bg/2026/05/24/short-videos-attention-and-executive-control-what-universities-should-learn-from-new-eeg-research/)).
Diễn giải đúng: học sinh **vẫn đọc được**, nhưng phải *cố nhiều hơn*, và cái mệt chỉ lộ ra ở đúng loại
việc nhàm mà bắt buộc — đọc liền, chịu mơ hồ, tự lập luận. Thêm nữa, đọc hiểu trên màn hình nhìn chung
thấp hơn trên giấy, **khoảng cách lớn nhất ở văn bản dài và khi bị áp lực thời gian** (Delgado et al.
2018, [meta-analysis](https://www.sciencedirect.com/science/article/pii/S1747938X18300101)).

### Điểm cân bằng — đừng "TikTok hoá" bài học

Đề thi vẫn đòi đúng năng lực đọc liền 10–20 phút. Nếu mọi nội dung đều bị cắt đến mức học sinh **không
bao giờ** phải chịu 10 phút liền, trường học đang bỏ luôn bài tập rèn năng lực đó. Mục tiêu đúng:

1. **Ngắn để dẫn vào** — phần đầu bài (mục I, từ khoá) phải trả công ngay.
2. **Chia nhịp để không bỏ cuộc** — không quá ~300 từ liền mà không có việc gì để làm.
3. **Vẫn giữ một đoạn buộc đọc liền có chủ đích** — bài toán mẫu, nơi học sinh phải theo một lập luận
   dài; đây là "máy chạy bộ" của năng lực đọc, không được cắt.

---

## 2. Số đo 5 bài lý thuyết đang có (2/10/2026)

Đo bằng `lint_do_dai.py`. "Từ hiện ngay" = chữ học sinh thật sự nhìn thấy khi mở trang: bỏ nội dung
trong `<details>` (giữ `<summary>`) và bỏ **phản hồi quiz** (`.tl-fb` — CSS ẩn cho tới khi chọn đáp án).
Mục được chia theo cả `<h3>` lẫn `<h4>` (mục con), vì người đọc thấy tiêu đề con ngắt đoạn — mục lục
trong app vẫn chỉ liệt kê `<h3>`. Thời gian tính ở 140 từ/phút — tốc độ đọc chữ Việt trên điện thoại
khi có công thức phải dừng nghĩ (ước lượng, không phải số đo).

> Bản đầu của `lint_do_dai.py` (2/10/2026) tính cả phản hồi quiz vào "từ hiện ngay" (11–13% số từ của
> mỗi bài) và chỉ chia mục theo `<h3>`. Số dưới đây là bản đã sửa; số cũ cao hơn khoảng 12%.

| Bài | Từ hiện ngay | Tổng từ | ~phút | Mục dài nhất | Đoạn liền dài nhất | Kết quả lint |
|---|---|---|---|---|---|---|
| Định luật III Newton (l10) | 1.408 | 2.018 | 10,1 | 350 | 211 | ✓ sạch |
| Dao động điều hoà (l11) | 1.103 | 1.452 | 7,9 | 130 | 143 | ✓ (2 mục con thiếu nhịp) |
| Giao thoa sóng (l11) | 1.537 | 2.023 | 11,0 | 350 | 215 | ✓ sạch |
| Cảm ứng điện từ (l12) | 2.316 | 3.059 | 16,5 | 461 | 253 | ⚠ tổng + 3 mục 371–461 từ |
| **Mô tả sóng (l11)** — trước khi cắt 2/10 | **3.021** | **4.190** | **21,6** | **489** | **478** | ✗ tổng · ✗ đoạn liền 478 · ⚠ 2 mục |
| Mô tả sóng — **sau khi cắt 2/10** | **2.457** | 3.870 | 17,6 | 274 | 194 | ✓ 0 lỗi cứng · ⚠ tổng gần trần |

Đọc bảng này ra ba điều:

1. **Ba bài ngắn thì ổn** (8–11 phút) — hạn mức dưới đây không phải lý thuyết suông, nó đang mô tả
   đúng những bài đã làm tốt. (Chia theo `<h4>` cho thấy "mục II 535 từ" của bài Dao động thực ra là
   5 mục con 61–130 từ — không phải vấn đề.)
2. **Bài được chốt làm chuẩn lại là bài dài nhất.** Mục con "Năm đại lượng đặc trưng" dài 489 từ trong
   *một* `<h4>`, và có một đoạn **478 từ liền không có `<details>`, quiz hay hình nào** (~3,4 phút đọc
   suông). Nếu lấy bài này làm khuôn để nhân rộng thì các bài sau sẽ phình theo.
3. **Cảm ứng điện từ (8 mục lớn, 2.316 từ) là dấu hiệu đã phình** — không bài nào cần quá 6–7 mục.

Điểm quan trọng về mặt kỹ thuật: trong một mục `ly_thuyet`, **toàn bộ các `<h3>` render thẳng một mạch**
(`TheoryBlock` trong `app/lop-hoc/bai/page.tsx` chỉ thu gọn ở cấp *mục bài*, không thu gọn từng `<h3>`).
Nên "bài dài" = học sinh nhận đúng ngần ấy chữ khi mở tab Lý thuyết, không có accordion nào đỡ.

---

## 3. Hạn mức (dùng luôn, không bàn lại)

| Chỉ số | Ngưỡng cảnh báo ⚠ | Ngưỡng lỗi ✗ | Tương đương |
|---|---|---|---|
| Tổng từ hiện ngay cả bài | > 2.000 | > 2.500 | ~14 phút / ~18 phút |
| Một mục (`<h3>`/`<h4>`) | > 350 | > 480 | ~2,5 phút / ~3,4 phút |
| Mục "Bài toán mẫu" | > 500 | > 700 | đây là đoạn **buộc đọc liền** nên nới |
| Đoạn liền không có nhịp nào | > 300 | > 400 | ~2 phút / ~2,9 phút |
| Số quiz | < 4 | > 8 | 4–8 (nét 14 của skill) |
| Số mục `<h3>` | ngoài 6–8 | — | |
| Mỗi mục | không có nhịp nào | — | nhịp = `<details>` · `.tl-quiz` · `<figure>` |

Chạy:

```bash
python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py <theory.html> [...]
# --wpm 160 nếu muốn ước lượng thời gian theo người đọc nhanh; --json để lấy số; --khong-canh-bao chỉ in lỗi cứng
```

Script in bảng từng mục (hiện ngay / tổng / số nhịp / đoạn liền dài nhất) rồi liệt kê lỗi; **exit 1 nếu
có lỗi cứng** nên cắm được vào quy trình soạn bài. Chạy cùng `lint_theory.py` (cấu trúc) và
`check_quizzes.py` (logic tự chấm) ở bước 5 của skill.

Vì sao có hai mức ⚠/✗ thay vì một: các ngưỡng này rút từ số đo 5 bài trên, sao cho **bài đã làm tốt
không bị báo động giả** (3 bài ngắn chỉ ⚠ hoặc sạch) mà **bài phình vẫn bị chặn**. Một ngưỡng cứng
"≤ 300 từ/mục" cho mọi mục sẽ báo lỗi cả 5/5 bài kể cả những bài đọc thoải mái — vô dụng làm cổng kiểm.

---

## 4. Phương pháp soạn nội dung theo nhịp

### 4.1 Kiến trúc 3 tầng cho mỗi mục

| Tầng | Nội dung | Thời gian | Ai đọc |
|---|---|---|---|
| Quét | Dòng 🔑 3–6 từ + bullet ≤ 8 từ | 30 giây | mọi học sinh, kể cả lúc lười |
| Học | Ví dụ / thí nghiệm Làm–Quan sát–Rút ra + quiz tự chấm | 2–3 phút | học sinh học thật |
| Mở rộng | `<details>`: công thức suy ra, ứng dụng, bài khó hơn | tuỳ | học sinh khá |

**Kiến thức bắt buộc không được giấu ở tầng 3** (giữ nguyên quy tắc trong skill). Tầng 1 phải đứng
một mình vẫn có nghĩa: nếu học sinh chỉ đọc dòng 🔑 và bullet, em vẫn nắm được phát biểu.

### 4.2 "Hợp đồng đầu bài"

Đầu bài ghi rõ: mục tiêu (2–4 gạch đầu dòng) + **bao nhiêu câu phải trả lời được ở mục Trả bài** +
**thời gian ước tính** ("khoảng 12 phút · 6 mục · 5 câu tự kiểm tra"). Biết trước còn bao xa là cách rẻ
nhất để giảm bỏ giữa chừng (L2), và cho phép học sinh chọn "học 2 mục rồi mai học tiếp" mà không thấy
tội lỗi — đúng tinh thần segmenting (N5).

### 4.3 Viết chống quét

- **Kết luận trước, giải thích sau**, ở mỗi mục: một câu chốt ngay đầu mục rồi mới dẫn dắt.
- Đoạn văn xuôi tối đa 2–3 câu; quá thì tách thành bullet hoặc đẩy vào `<details>` (nét "Ít chữ").
- Mỗi mục có đúng **một** câu "mang về" nổi bật — nhấn hai thứ là không nhấn gì (N7, B2).
- Cắt theo mục, không cắt theo bài: khi một mục vượt 600 từ, tách thành `II.1`, `II.2`… mỗi mục con có
  🔑 + ví dụ + quiz riêng, thay vì viết mục II khổng lồ (lỗi của bài Mô tả sóng).

### 4.4 Lấy phần hay của video ngắn, không lấy cơ chế gây nghiện

Lấy: hook 2 câu bằng cảnh thật (情境导入), phản hồi đúng/sai **tức thì và gọi tên lỗi**, tiến độ trong
bài, ưu tiên chữ ngắn như phụ đề. Không lấy: streak/huy hiệu trong lúc đọc, chuyển động tự chạy, thông
báo chen giữa bài (L3, B4, B6, L6).

### 4.5 Một nội dung, hai định dạng

Mỗi bài lý thuyết vốn đã là 6 mục ⇒ cắt được thành 6 clip 60–90 giây; clip thí nghiệm lấy thẳng từ
`content/thi-nghiem/` (đã có `data-exp` làm khoá liên kết). Cuối clip trỏ về **đúng mốc** của bài: mỗi
`<h3>` đã có id ổn định `theory-sec-<lesson_item_id>-<chỉ số>` do `wrapTheorySections` sinh ra (dùng cho
mục lục và nút "Ôn ngay"), nên link `#theory-sec-61-2` mở thẳng mục III. Tức là:

- **Video ngắn là cửa vào** — nơi học sinh đang ở.
- **Bài đọc là chỗ học** — nơi có chiều sâu, tra cứu lại được, không phải xem lại từ đầu.
- Chiều ngược lại cũng dùng được: số liệu kênh TikTok cho biết cảnh mở bài nào hút, để chọn 情境导入.

---

## 5. Kiểm chứng bằng dữ liệu trong app, không chỉ tin lý thuyết

- **Đã có sẵn**: `exam_question_results` ghi từng câu theo `topic_id` (YCCĐ) và `get_lesson_mastery` /
  `get_chapter_mastery` tính mastery — nên so được mastery của cùng một YCCĐ **trước và sau** khi thay
  bài (`docs/ANALYTICS-SETUP.md`, `docs/mastery-rules.md`).
- **Đo thêm được rẻ**: độ sâu cuộn theo từng mục (mục nào học sinh rơi nhiều nhất) và tỉ lệ bấm quiz.
  Đây là phép đo trả lời trực tiếp "mục nào đang bị bỏ", tốt hơn mọi tranh luận về độ dài.
- **Thí nghiệm tự nhiên đang có sẵn**: cắt bài Mô tả sóng từ 3.506 xuống ~2.200 từ hiện ngay rồi so tỉ lệ
  hoàn thành + điểm mục Trả bài sau 48 giờ với bản cũ. Nếu mastery không giảm mà tỉ lệ hoàn thành tăng
  thì hạn mức ở mục 3 được xác nhận bằng chính học sinh của mình.

---

## 6. Checklist trước khi đăng một bài lý thuyết

1. `lint_do_dai.py` không có ✗; các ⚠ đã xem và chấp nhận có lý do.
2. `lint_theory.py` + `check_quizzes.py` sạch (cấu trúc, logic tự chấm).
3. Không mục nào quá 600 từ; mục nào quá 400 từ thì đã cân nhắc tách mục con.
4. Không đoạn nào quá 300 từ liền không có việc gì để làm.
5. Hợp đồng đầu bài có mặt (mục tiêu + số câu Trả bài + thời gian ước tính).
6. Có **ít nhất một** đoạn buộc đọc liền có chủ đích (bài toán mẫu) — không cắt hết.
7. Xem ảnh 375px bằng mắt trước khi báo xong (checklist mục 8 của `docs/QUY-TAC-THIET-KE.md`).

---

## 7. Nợ kỹ thuật đang treo

| Việc | Vì sao | Ghi chú |
|---|---|---|
| ~~Cắt lại bài Mô tả sóng (l11)~~ — **đã làm 2/10/2026** | 3.021 từ, mục con 489 từ, đoạn liền 478 từ | còn 2.457 từ (0 lỗi cứng, 1 ⚠ tổng): tách mục con + chuyển 3 khối tra cứu/thí nghiệm vào `<details>`; 3 bảng 3 cột bị bóp chữ ở 375px đã đưa về 2 cột (H2, C4) |
| Tách bớt bài Cảm ứng điện từ (l12) | 2.316 từ (~16,5 phút) + 3 mục 371–461 từ | gộp mục hoặc chuyển phần mở rộng vào `<details>` |
| Thêm nhịp cho 2 mục con bài Dao động điều hoà | "Dao động tuần hoàn" và "Phương trình dao động điều hoà" không có details/quiz/hình | ⚠ nhẹ, thêm 1 quiz hoặc 1 `<details>` mỗi mục |
| Ghi độ sâu cuộn theo mục | chưa có phép đo nào trong app | cần khi muốn kiểm chứng mục 5 |
| Viết bảng số liệu thật cho thí nghiệm đo | nét "数据分析" của skill đòi ≥1 thí nghiệm có bảng 3–5 lần đo + câu hỏi sai số; bài Mô tả sóng chưa có | bổ sung khi soạn lại lần sau |

---

## 8. Nguồn

- Cowan 2001; Sweller 1988; Sweller & Cooper 1985; Kalyuga 2003; Mayer *Multimedia Learning*
  (coherence, signaling, segmenting, redundancy); Harp & Mayer 1998 — nền của `docs/QUY-TAC-THIET-KE.md`.
- Nielsen 2006/2008 (F-pattern, tỉ lệ đọc); Steinberg 2008; Casey–Jones–Hare 2008; Stothart–Mitchum–Yehnert
  2015; Ophir–Nass–Wagner 2009; Roediger & Karpicke 2006; Kivetz–Urminsky–Zheng 2006; Nunes & Drèze 2006;
  Deci–Koestner–Ryan 1999.
- Yan, T., Su, C., Xue, W., Hu, Y., & Zhou, H. (2024). *Mobile phone short video use negatively impacts
  attention functions: An EEG study.* Frontiers in Human Neuroscience 18.
  [doi:10.3389/fnhum.2024.1383913](https://doi.org/10.3389/fnhum.2024.1383913)
- Delgado, P., Vargas, C., Ackerman, R., & Salmerón, L. (2018). *Don't throw away your printed books: A
  meta-analysis on the effects of reading media on reading comprehension.* Educational Research Review.
  [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1747938X18300101)
- BBC — *Busting the attention span myth* (con số "8 giây" không có nguồn).
  [bbc.co.uk](https://www.stage.bbc.co.uk/news/health-38896790)
