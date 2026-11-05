# Đo "bài tương tự" có đúng dạng không — 05/11/2026 (chặng 4)

Chỉ đọc, không sửa DB. Đo trên prod sau khi đã nạp `question_dang` 5.039 dòng (1.313 unsure) và deploy RPC
`get_similar_dang_questions`. Truy vấn và dữ liệu thô nằm ở scratchpad phiên (`phu.sql`, `mau.sql`, `mau.json`,
`ket-qua-a/b.json`), không commit.

## Kết luận

- **Đúng dạng: 82/88 câu = 93,2%** (mục tiêu ≥95% — **chưa đạt**). 0 câu sai hẳn, 6 câu lệch dạng.
- 18/20 dạng mẫu đúng 100%. Lỗi dồn vào **một dạng**: L11 Bài Điện trường (lesson 38) Dạng 4 — cả 4 câu chắc đều lệch.
  Bỏ dạng đó, tỉ lệ còn lại là 82/84 = 97,6%.
- Đánh dấu unsure 4 câu lesson 38 (+ 2 câu ranh giới) thì RPC chỉ còn trả câu đã chấm đúng ở mẫu này.
- 95 câu mới soạn cho dạng lý thuyết (`claude-2026-11-05-soan-dang-thieu`): 15/15 câu rơi vào mẫu đều đúng dạng.
- **Độ phủ: 497 dạng, 134 dạng 0 câu, 84 dạng 1–2 câu, 279 dạng ≥3 câu.** Cả 26 dạng lý thuyết trong
  `docs/dang-thieu-cau.md` đã lên ≥3 câu; 218 dạng <3 câu còn lại đều là dạng tính toán (đổi số được).
- UI prod: bấm "Làm bài tương tự" ở Bài 16 (lesson 17) Dạng 2 trên 375px → hiện câu "tìm hạt X" đúng dạng,
  không có nhãn "chưa phân dạng". Ảnh: `side-session-notes/.../cau-tuong-tu-375/do-chang4-bai17-dang2.jpg`.

## 1. Độ phủ theo chương

Đếm theo nhãn `Dạng N` trong `lesson_items.questions` (kind `bai_tap_mau`) và câu `question_dang` có
`unsure=false`, **lọc giống RPC** (không archived, không essay, không `lint_flags`) — tức số câu học sinh thật sự
nhận được. Chênh với "câu chắc" thô chỉ 3 câu (bị lint_flags/essay). Không có dòng `question_dang` nào mồ côi
(tổng câu chắc 3.726 = 5.039 − 1.313, khớp hết vào dạng có trong Bài tập mẫu).

| Chương | Tổng dạng | 0 câu | 1–2 câu | ≥3 câu | Câu dùng được |
|---|---|---|---|---|---|
| L10 Chương 1: Mở đầu | 9 | 2 | 0 | 7 | 78 |
| L10 Chương 2: Động học | 37 | 4 | 5 | 28 | 334 |
| L10 Chương 3: Động lực học | 36 | 12 | 6 | 18 | 272 |
| L10 Chương 4: Năng lượng, công, công suất | 25 | 3 | 1 | 21 | 242 |
| L10 Chương 5: Động lượng | 14 | 5 | 0 | 9 | 95 |
| L10 Chương 6: Chuyển động tròn | 10 | 1 | 1 | 8 | 111 |
| L10 Chương 7: Biến dạng của vật rắn. Áp suất chất lỏng | 10 | 2 | 2 | 6 | 52 |
| L11 Chương 1: Dao động | 35 | 8 | 6 | 21 | 256 |
| L11 Chương 2: Sóng | 36 | 9 | 2 | 25 | 338 |
| L11 Chương 3: Điện trường | 29 | 5 | 5 | 19 | 255 |
| L11 Chương 4: Dòng điện. Mạch điện | 22 | 6 | 9 | 7 | 61 |
| L12 Chương 1: Vật lí nhiệt | 20 | 3 | 3 | 14 | 165 |
| L12 Chương 2: Khí lí tưởng | 20 | 2 | 2 | 16 | 202 |
| L12 Chương 3: Từ trường | 34 | 4 | 6 | 24 | 284 |
| L12 Chương 4: Vật lí hạt nhân | 27 | 7 | 1 | 19 | 285 |
| KHTN9 Chương 2: Ánh sáng | 9 | 5 | 1 | 3 | 12 |
| KHTN9 Chương 3: Điện | 12 | 6 | 6 | 0 | 7 |
| HSG9 Nền tảng: công cụ toán học và thực hành | 6 | 2 | 2 | 2 | 100 |
| HSG9 Cơ học và năng lượng cơ học | 32 | 10 | 3 | 19 | 417 |
| HSG9 Nhiệt học và âm thanh | 18 | 7 | 6 | 5 | 47 |
| HSG9 Điện học | 18 | 14 | 2 | 2 | 9 |
| HSG9 Quang học và Trái Đất – bầu trời | 27 | 14 | 10 | 3 | 38 |
| HSG9 Điện từ và năng lượng với cuộc sống | 11 | 3 | 5 | 3 | 63 |
| **Tổng** | **497** | **134** | **84** | **279** | **3723** |

**So với `docs/dang-thieu-cau.md`** (lập trước đợt nạp 05/11, 244 dạng <3 câu):

| Trước → nay | Số dạng |
|---|---|
| ≥3 câu → vẫn ≥3 câu | 250 (không dạng nào giảm số câu) |
| <3 (lý thuyết) → ≥3 câu | 26 — đủ cả 26 dạng lý thuyết nhờ 95 câu mới |
| <3 (tính toán) → vẫn 0 câu | 123 |
| <3 (tính toán) → vẫn 1–2 câu | 77 |
| KHTN9 (21 dạng, file cũ không có cột mức nên không khớp được dòng) | 11 dạng 0 câu, 7 dạng 1–2, 3 dạng ≥3 — y như file cũ |

134 dạng 0 câu theo mức: Khó 37, Trung bình 35, Nâng cao 20, Dễ 14, không ghi mức (KHTN9) 11, Vận dụng cao 7,
khác 10. Các dạng này hiện rơi về câu cùng chủ đề có nhãn "chưa phân dạng". Danh sách ở Phụ lục.

## 2. Mẫu chấm

20 dạng ≥3 câu, chọn ngẫu nhiên (seed 20261105) trải chương: L10 ×5, L11 ×5, L12 ×5, KHTN9 ×3, HSG9 ×2; 4 dạng
có câu mới soạn. Mỗi dạng gọi `get_similar_dang_questions(lesson, dạng, '{}', 5)` với `set role authenticated`
+ JWT giả (bảng tạm tạo trước khi đổi vai). Được 88 câu (một số dạng chỉ có 3–4 câu). Hai agent `kiem-code` chấm
độc lập (mỗi agent 10 dạng, chỉ thấy đề mẫu + câu, không thấy kết luận của phiên chính) theo 3 mức
đúng dạng / lệch dạng / sai hẳn.

| Lesson · Dạng | Chương | Tên dạng | Đúng | Lệch |
|---|---|---|---|---|
| 2 · 2 | L12 Ch.1 | Thể tích và hình dạng chất rắn, lỏng, khí *(câu mới)* | 4 | 0 |
| 8 · 1 | L12 Ch.2 | Đẳng tích: nung nóng bình kín | 4 | 0 |
| 10 · 1 | L12 Ch.3 | Chiều từ trường quanh thanh nam châm *(câu mới)* | 4 | 0 |
| 17 · 2 | L12 Ch.4 | Bảo toàn nuclôn, điện tích, tìm hạt X | 5 | 0 |
| 18 · 3 | L12 Ch.4 | Khối lượng đã phân rã: tìm T | 5 | 0 |
| 24 · 2 | L11 Ch.1 | Wđ = n·Wt: li độ, tốc độ | 5 | 0 |
| 26 · 4 | L11 Ch.1 | Con lắc đơn góc lớn | 3 | 0 |
| 31 · 1 | L11 Ch.2 | Điểm cực đại/cực tiểu giao thoa | 5 | 0 |
| **38 · 4** | **L11 Ch.3** | **Từ nghỉ, chỉ lực điện: công = ΔWđ, bài ngược tìm E** | **0** | **4** |
| 41 · 4 | L11 Ch.4 | Tốc độ trôi electron từ I = Snve | 5 | 0 |
| 48 · 2 | L10 Ch.1 | Sai số phép nhân, chia | 5 | 0 |
| 50 · 1 | L10 Ch.2 | Tốc độ trung bình nhiều đoạn | 5 | 0 |
| 58 · 1 | L10 Ch.3 | Hợp lực hai lực đồng quy | 5 | 0 |
| 70 · 4 | L10 Ch.4 | Công trọng lực, độ biến thiên thế năng | 5 | 0 |
| 78 · 1 | L10 Ch.7 | Nhận biết biến dạng *(câu mới)* | 4 | 0 |
| 83 · 1 | KHTN9 Ánh sáng | Chiết suất và tốc độ ánh sáng | 5 | 0 |
| 83 · 4 | KHTN9 Ánh sáng | Tia phản xạ và tia khúc xạ: tìm n, v | 2 | 1 |
| 84 · 1 | KHTN9 Ánh sáng | Góc tới hạn | 3 | 0 |
| 150 · 2 | HSG9 Nhiệt & âm | Tần số, độ cao, độ to: đồ thị *(câu mới)* | 4 | 0 |
| 153 · 6 | HSG9 Nhiệt & âm | Cơ năng → nhiệt (H·W = Q) | 4 | 1 |

Theo lượt gán (`question_dang.source`): `claude-2026-11-05-chuong3-l11` 0/4 đúng (cả 4 là dạng 38·4); các lượt khác
100% trừ `chuong2-khtn9` 10/11 và `hsg9-nhiet-am` 5/6. Lượt 23–24/10: 17/17 đúng.

## 3. Câu lệch dạng

| id | Lesson · Dạng | source | Lý do (agent) |
|---|---|---|---|
| 1509567 | 38 · 4 | claude-2026-11-05-chuong3-l11 | Chỉ tính công A = qEd; không dùng công = độ tăng động năng, không tìm E/tốc độ |
| 13420 | 38 · 4 | claude-2026-11-05-chuong3-l11 | Như trên (bản trắc nghiệm gần trùng 1509567) |
| 1540405 | 38 · 4 | claude-2026-11-05-chuong3-l11 | Như trên |
| 1192367 | 38 · 4 | claude-2026-11-05-chuong3-l11 | Như trên |
| 377728 | 83 · 4 | claude-2026-11-05-chuong2-khtn9 | Chỉ cho i, r → n = sin i/sin r, v = c/n; không có tia phản xạ (ý chính i' = i). *Ranh giới*: gần dạng 83·1 |
| 674161 | 153 · 6 | claude-2026-11-05-hsg9-nhiet-am | Vật trượt mặt nghiêng có ma sát, ΔU = công ma sát; không có H% hay rơi/va chạm |

Agent còn ghi 2 câu "đúng nhưng lỏng" (để thầy xem, không đề xuất sửa): 291460 (41·4, tính xuôi mật độ dòng thay
vì rút v) và 669045 (18·3, cho sẵn T tìm m còn lại, không phải chiều "đã phân rã → tìm T").

## 4. Mẫu lỗi chung

1. **Dạng mức Khó/Nâng cao nhận câu chỉ trùng một bước phụ.** Cả 6 câu lệch đều cùng kiểu: đề mẫu là chuỗi
   nhiều bước (qEd → ΔWđ → bài ngược; phản xạ + khúc xạ; H·W = Q), câu được gán chỉ dùng một bước đơn giản trong
   chuỗi. Bộ gán (subagent theo `on-tap-dang-bai-tap`) xếp theo "có công thức chung" thay vì "cùng cách giải".
2. **Dạng ít câu dễ bị nhét cho đủ.** 38·4 có đúng 4 câu chắc và cả 4 lệch, gần trùng nhau — dấu hiệu bộ gán
   kéo câu gần nhất vào dạng khó còn trống. Sau khi đánh dấu unsure, 38·4 sẽ về 0 câu (rơi về "chưa phân dạng"),
   như vậy trung thực hơn là đưa câu sai dạng.
3. Dạng Dễ/Trung bình và dạng lý thuyết mới soạn: không thấy lỗi trong mẫu.

Giới hạn: mẫu 20 dạng/88 câu nên khoảng tin cậy rộng (≈ ±5 điểm %); mẫu nghiêng về dạng có nhiều câu.
Nên rà riêng các dạng mức Khó/Nâng cao/Vận dụng cao có 3–6 câu chắc trước khi đo lại.

## 5. Đề xuất SQL (CHƯA chạy — thầy duyệt rồi chạy trong tab terminal)

```sql
-- Đánh dấu unsure các câu lệch dạng (đo 05/11/2026). Không xoá dòng, RPC tự bỏ câu unsure.
begin;
create table if not exists public.question_dang_bak_20261105_do as
  select * from public.question_dang
  where (question_id, lesson_id) in ((1509567,38),(13420,38),(1540405,38),(1192367,38),(377728,83),(674161,153));
alter table public.question_dang_bak_20261105_do enable row level security;
revoke all on public.question_dang_bak_20261105_do from anon, authenticated;
update public.question_dang set unsure = true
where (question_id, lesson_id) in ((1509567,38),(13420,38),(1540405,38),(1192367,38),(377728,83),(674161,153))
  and not unsure;           -- kỳ vọng 6 dòng
commit;
```

Hai câu ranh giới (377728, 674161) có thể bỏ khỏi danh sách nếu thầy coi là đúng dạng.

## 6. Việc tiếp theo đề xuất

1. Chạy SQL mục 5 (6 dòng, chạy giờ nào cũng được).
2. Rà lại gán dạng cho các dạng mức Khó/Nâng cao/Vận dụng cao (≈160 dạng) — ưu tiên lượt `chuong3-l11` —
   chỉ hỏi "câu có đi qua đủ chuỗi bước của đề mẫu không", câu chỉ trùng một bước → unsure.
3. Soạn câu đổi số cho 218 dạng tính toán <3 câu (134 dạng 0 câu), ưu tiên Trung bình/Dễ của L10–L12 vì HS bấm
   nhiều nhất; dạng HSG9 Điện học/Quang (28 dạng 0 câu) để sau.
4. Đo lại bằng đúng quy trình này (đổi seed) sau bước 1–2; mục tiêu ≥95%.

## Phụ lục — 134 dạng còn 0 câu dùng được

| Lớp | Bài (lesson_id) | Dạng |
|---|---|---|
| L12 | Bài 1. Sự chuyển thể (2) | Dạng 5 · Nâng cao · Làm nguội kim loại đúc: dữ kiện ẩn về đông đặc |
| L12 | Bài 3. Nội năng. Định luật 1 của nhiệt động l (4) | Dạng 4 · Khó · Công làm nóng vật rồi nhiệt truyền sang nước: đặt dấu riêng cho t |
| L12 | Bài 3. Nội năng. Định luật 1 của nhiệt động l (4) | Dạng 5 · Nâng cao · Cả chu trình: ΔU = 0 trong tủ lạnh |
| L12 | Bài 6. Định luật Boyle. Định luật Charles (7) | Dạng 4 · Khó · Hai giai đoạn nối tiếp: đẳng nhiệt rồi đẳng áp |
| L12 | Bài 7. Phương trình trạng thái của khí lí tưở (8) | Dạng 3 · Trung bình · Đọc đồ thị p–T của hai đường đẳng tích |
| L12 | Bài 9. Khái niệm từ trường (10) | Dạng 4 · Khó · Hai dây quanh la bàn: chiều từ trường rồi tổng hợp |
| L12 | Bài 15. Một số ứng dụng của cảm ứng điện từ (126) | Dạng 2 · Trung bình · Sạc không dây: điện áp thứ cấp lí tưởng và số đo |
| L12 | Bài 15. Một số ứng dụng của cảm ứng điện từ (126) | Dạng 3 · Khá · Dòng điện Foucault: điều kiện xuất hiện, lực hãm và toả nhiệt |
| L12 | Bài 15. Một số ứng dụng của cảm ứng điện từ (126) | Dạng 4 · Khó · Bếp từ: chọn nồi, nhiệt lượng, hiệu suất và thời gian đun |
| L12 | Bài 15. Năng lượng liên kết hạt nhân (16) | Dạng 4 · Khá · Đề cho khối lượng nguyên tử |
| L12 | Bài 18. An toàn phóng xạ (19) | Dạng 1 · Dễ · Liều hấp thụ và liều tương đương của tia X |
| L12 | Bài 18. An toàn phóng xạ (19) | Dạng 2 · Trung bình · Cùng năng lượng hấp thụ, khác loại tia |
| L12 | Bài 18. An toàn phóng xạ (19) | Dạng 3 · Trung bình · Suất liều theo khoảng cách tới nguồn |
| L12 | Bài 18. An toàn phóng xạ (19) | Dạng 4 · Khá · Liều theo thời gian đứng và thời gian đứng tối đa |
| L12 | Bài 18. An toàn phóng xạ (19) | Dạng 5 · Khá · So sánh các biện pháp giảm liều: thời gian, khoảng cách, che chắn |
| L12 | Bài 18. An toàn phóng xạ (19) | Dạng 6 · Khó · Liều cả năm so với giới hạn nghề nghiệp và khoảng cách tối thiểu |
| L11 | Bài 1. Dao động điều hoà (20) | Dạng 2 · Trung bình · Phương trình có dấu trừ trước côsin: đưa về biên độ dương, |
| L11 | Bài 2. Mô tả dao động điều hoà (21) | Dạng 5 · Khó · Đổi mốc thời gian: pha ban đầu đổi, nhịp dao động giữ nguyên |
| L11 | Bài 3. Vận tốc, gia tốc trong dao động điều h (22) | Dạng 3 · Trung bình · Đọc đồ thị x–t: biên độ, chu kì, pha ban đầu; suy ra v và  |
| L11 | Bài 4. Bài tập về dao động điều hoà (23) | Dạng 5 · Khó · Quãng đường, tốc độ trung bình và vận tốc trung bình trong khoảng |
| L11 | Bài 5. Động năng. Thế năng. Sự chuyển hoá giữ (24) | Dạng 5 · Khó · Đọc đồ thị động năng theo li độ: cơ năng, độ cứng, tốc độ cực đại |
| L11 | Bài 6. Dao động tắt dần. Dao động cưỡng bức.  (25) | Dạng 2 · Trung bình · Cộng hưởng qua bảng quét tần số: tìm $f_0$, tần số dao độn |
| L11 | Bài 6. Dao động tắt dần. Dao động cưỡng bức.  (25) | Dạng 5 · Nâng cao · Chọn đệm chống rung: biên độ lúc chạy ổn định và lúc khởi độ |
| L11 | Bài 7. Bài tập về sự chuyển hoá năng lượng tr (26) | Dạng 5 · Khó · Đồ thị năng lượng theo thời gian: tìm cơ năng, chu kì, độ cứng, b |
| L11 | Bài 8. Mô tả sóng (27) | Dạng 5 · Khó · Đọc hai đồ thị u–x và u–t, viết phương trình dao động |
| L11 | Bài 9. Sóng ngang, sóng dọc, sự truyền năng l (28) | Dạng 2 · Trung bình · Sóng truyền đi cái gì, phần tử môi trường ở lại |
| L11 | Bài 9. Sóng ngang, sóng dọc, sự truyền năng l (28) | Dạng 3 · Trung bình · Sóng dọc: vùng nén, vùng dãn và bước sóng |
| L11 | Bài 9. Sóng ngang, sóng dọc, sự truyền năng l (28) | Dạng 4 · Trung bình · Năng lượng sóng tỉ lệ $A^2$ và $f^2$ |
| L11 | Bài 9. Sóng ngang, sóng dọc, sự truyền năng l (28) | Dạng 6 · Nâng cao · Sóng P và sóng S từ cùng tâm chấn |
| L11 | Bài 14. Bài tập về sóng (33) | Dạng 6 · Khó · Sóng dừng trong ống một đầu kín: hai tần số cộng hưởng liên tiếp |
| L11 | Bài 15. Thực hành: Đo tốc độ truyền âm (34) | Dạng 1 · Dễ · Mức cường độ âm: từ cường độ ra dB, từ dB ra cường độ, và cảm giác |
| L11 | Bài 15. Thực hành: Đo tốc độ truyền âm (34) | Dạng 2 · Trung bình · Ống một đầu kín: dự đoán các vị trí cộng hưởng |
| L11 | Bài 15. Thực hành: Đo tốc độ truyền âm (34) | Dạng 3 · Trung bình · Từ hai lần cộng hưởng tính bước sóng, tốc độ và đoạn e |
| L11 | Bài 18. Điện trường đều (37) | Dạng 1 · Dễ · Hai bản song song: cường độ điện trường, lực điện và chiều của lực |
| L11 | Bài 18. Điện trường đều (37) | Dạng 4 · Khó · Ra khỏi hai bản: vận tốc, góc lệch và vệt trên màn |
| L11 | Bài 18. Điện trường đều (37) | Dạng 5 · Khó · Bài ngược: hiệu điện thế lớn nhất để electron còn ra khỏi hai bản |
| L11 | Bài 21. Tụ điện (40) | Dạng 1 · Dễ · Điện dung C = Q/U và đổi đơn vị |
| L11 | Bài 21. Tụ điện (40) | Dạng 3 · Trung bình · Tụ phẳng: điện dung theo cấu tạo và hiệu điện thế không đá |
| L11 | Bài 23. Điện trở. Định luật Ohm (42) | Dạng 3 · Trung bình · So sánh hai đường đặc trưng, trục I tính bằng mA |
| L11 | Bài 23. Điện trở. Định luật Ohm (42) | Dạng 5 · Khó · Dây nung nicrom của bàn là: điện trở khi nóng, dòng lúc cắm điện, |
| L11 | Bài 24. Nguồn điện (43) | Dạng 3 · Khó · Hai lần đo cùng một nguồn: lập hệ để tìm điện trở trong và suất đ |
| L11 | Bài 24. Nguồn điện (43) | Dạng 4 · Khó · Bộ nguồn hỗn hợp đối xứng: suất điện động, điện trở trong, dòng đ |
| L11 | Bài 25. Năng lượng điện và công suất điện (44) | Dạng 5 · Khó · Đoản mạch và chọn cầu chì |
| L11 | Bài 26. Thực hành: Đo suất điện động và điện  (45) | Dạng 2 · Trung bình · Dự đoán số chỉ ampe kế, vôn kế và vai trò điện trở bảo vệ |
| L10 | Bài 1. Làm quen với Vật lí (46) | Dạng 2 · Trung bình · Phương pháp lí thuyết và thực nghiệm: so dự đoán với số đo |
| L10 | Bài 2. Các quy tắc an toàn trong phòng thực h (47) | Dạng 3 · Khó · Giữ khoảng cách an toàn: đọc số đo, so với sai số và áp dụng quy  |
| L10 | Bài 7. Đồ thị độ dịch chuyển - thời gian (52) | Dạng 3 · Trung bình · Hai đồ thị thẳng: lập phương trình và tìm chỗ hai xe gặp n |
| L10 | Bài 7. Đồ thị độ dịch chuyển - thời gian (52) | Dạng 4 · Khó · Xuất phát lệch giờ: tìm vận tốc từ điều kiện gặp nhau, phương trì |
| L10 | Bài 9. Chuyển động thẳng biến đổi đều (54) | Dạng 5 · Khó · Chuyển động hai giai đoạn: dốc rồi mặt ngang |
| L10 | Bài 12. Chuyển động ném (57) | Dạng 6 · Khó · Ném xiên, bài ngược: biết tầm xa, tìm góc ném (có hai nghiệm) |
| L10 | Bài 14. Định luật 1 Newton (59) | Dạng 1 · Dễ · Tủ trượt đều trên sàn ngang: lực ma sát và phản lực của sàn |
| L10 | Bài 14. Định luật 1 Newton (59) | Dạng 2 · Trung bình · Cần cẩu nâng đều: lực căng của cáp |
| L10 | Bài 14. Định luật 1 Newton (59) | Dạng 3 · Khá · Kéo thùng bằng dây chếch lên: ma sát và phản lực khi trượt đều |
| L10 | Bài 15. Định luật 2 Newton (60) | Dạng 6 · Khó · Tắt máy khi đang chạy đều: thời gian và quãng đường dừng |
| L10 | Bài 16. Định luật 3 Newton (61) | Dạng 1 · Dễ · Đẩy tường trên giày trượt: lực của tường và gia tốc người |
| L10 | Bài 16. Định luật 3 Newton (61) | Dạng 2 · Trung bình · Ngựa kéo xe: lực xe kéo ngựa và gia tốc của xe |
| L10 | Bài 17. Trọng lực và lực căng (62) | Dạng 3 · Trung bình · Vật trên bàn nhẵn nối vật treo qua ròng rọc |
| L10 | Bài 17. Trọng lực và lực căng (62) | Dạng 4 · Khó · Hai vật treo hai bên ròng rọc cố định |
| L10 | Bài 17. Trọng lực và lực căng (62) | Dạng 5 · Khó · Bài ngược: dây chỉ chịu lực căng tối đa |
| L10 | Bài 18. Lực ma sát (63) | Dạng 5 · Khó · Lên dốc rồi có tụt xuống không: ma sát đổi chiều theo chuyển động |
| L10 | Bài 19. Lực cản và lực nâng (64) | Dạng 2 · Trung bình · Vừa bung dù: lực cản lớn hơn trọng lực, tìm gia tốc |
| L10 | Bài 21. Moment lực. Cân bằng của vật rắn (66) | Dạng 5 · Khó · Thanh gắn bản lề giữ bằng dây xiên: lực căng và lực bản lề |
| L10 | Bài 25. Động năng, thế năng (70) | Dạng 5 · Khó · Định lí động năng với nhiều ngoại lực |
| L10 | Bài 27. Hiệu suất (72) | Dạng 1 · Dễ · Năng lượng toàn phần, có ích, hao phí |
| L10 | Bài 27. Hiệu suất (72) | Dạng 5 · Khó · Ghép nhiều khâu nối tiếp và giảm hao phí |
| L10 | Bài 29. Định luật bảo toàn động lượng (74) | Dạng 4 · Trung bình · Bảo toàn động lượng với vận tốc ngược chiều |
| L10 | Bài 30. Thực hành: Xác định động lượng của vậ (75) | Dạng 1 · Dễ · Tính tốc độ và động lượng của xe từ số đo cổng quang |
| L10 | Bài 30. Thực hành: Xác định động lượng của vậ (75) | Dạng 2 · Trung bình · Va chạm mềm: tính p, p′ và độ lệch δ rồi so với ε |
| L10 | Bài 30. Thực hành: Xác định động lượng của vậ (75) | Dạng 3 · Khó · Hai xe đẩy nhau: tổng động lượng sau có dấu và sai số |
| L10 | Bài 30. Thực hành: Xác định động lượng của vậ (75) | Dạng 4 · Khó · Độ lệch cùng một phía: tìm nguyên nhân hệ thống (băng nghiêng) |
| L10 | Bài 32. Lực hướng tâm và gia tốc hướng tâm (77) | Dạng 5 · Khó · Lực hướng tâm so với lực ma sát nghỉ cực đại |
| L10 | Bài 34. Khối lượng riêng. Áp suất chất lỏng (79) | Dạng 3 · Trung bình · Áp suất tuyệt đối và áp suất dư |
| L10 | Bài 34. Khối lượng riêng. Áp suất chất lỏng (79) | Dạng 4 · Khó · Bình thông nhau chứa hai chất lỏng không hoà tan |
| KHTN9 | Bài 5. Khúc xạ ánh sáng (83) | Dạng 2 · Đọc góc trên hình khúc xạ: góc tới, góc khúc xạ, chiều lệch |
| KHTN9 | Bài 5. Khúc xạ ánh sáng (83) | Dạng 5 · Nhiều lớp song song: không khí, nước, thuỷ tinh |
| KHTN9 | Bài 6. Phản xạ toàn phần (84) | Dạng 2 · Xét phản xạ toàn phần khi đề cho góc với mặt thoáng |
| KHTN9 | Bài 6. Phản xạ toàn phần (84) | Dạng 3 · Từ góc tới hạn đo được, tìm chiết suất rồi đổi môi trường |
| KHTN9 | Bài 6. Phản xạ toàn phần (84) | Dạng 4 · Sợi quang: điều kiện của lớp vỏ để tia được dẫn |
| KHTN9 | Bài 11. Điện trở. Định luật Ohm (89) | Dạng 2 · Đọc đồ thị I theo U của hai điện trở |
| KHTN9 | Bài 11. Điện trở. Định luật Ohm (89) | Dạng 4 · Tổng hợp: tìm vật liệu dây, rồi gập đôi dây |
| KHTN9 | Bài 12. Đoạn mạch nối tiếp, song song (90) | Dạng 1 · Đoạn mạch nối tiếp: tính điện trở tương đương, I, U từng điện trở |
| KHTN9 | Bài 12. Đoạn mạch nối tiếp, song song (90) | Dạng 4 · Tìm điện trở cần mắc thêm để đèn sáng bình thường |
| KHTN9 | Bài 13. Năng lượng của dòng điện và công suất (91) | Dạng 3 · So sánh độ sáng hai bóng đèn khi mắc nối tiếp và song song |
| KHTN9 | Bài 13. Năng lượng của dòng điện và công suất (91) | Dạng 4 · Tổng hợp: ấm điện có hiệu suất, thời gian đun và tiền điện |
| HSG9 | Chuyên đề 00. Kỹ năng nền: công cụ toán học,  (160) | Dạng 1 · Dễ · Rút tỉ số: tỉ lệ thuận, tỉ lệ nghịch và tỉ lệ với bình phương |
| HSG9 | Chuyên đề 00. Kỹ năng nền: công cụ toán học,  (160) | Dạng 3 · Trung bình · Đọc đồ thị U–I: điện trở, độ dốc, nội suy và ngoại suy |
| HSG9 | Chuyên đề 11. Cơ học chất lưu: áp suất chất l (154) | Dạng 2 · Trung bình · Bình thông nhau chứa hai chất lỏng không hòa tan (tiết diệ |
| HSG9 | Chuyên đề 11. Cơ học chất lưu: áp suất chất l (154) | Dạng 5 · Khó · Biến thiên mực nước: cục đá chứa dị vật tan hết |
| HSG9 | Chuyên đề 11. Cơ học chất lưu: áp suất chất l (154) | Dạng 6 · Nâng cao · Đòn bẩy kết hợp lực đẩy Archimedes: bài ngược tìm khối lượng |
| HSG9 | Chuyên đề 10. Lực: tổng hợp lực, cân bằng, ma (155) | Dạng 6 · Nâng cao · Lực đàn hồi kết hợp ma sát nghỉ: khoảng độ giãn để vật nằm y |
| HSG9 | Chuyên đề 01. Công và công suất (161) | Dạng 5 · Khó · Palăng có ròng rọc động: lực kéo, công và hiệu suất |
| HSG9 | Chuyên đề 01. Công và công suất (161) | Dạng 6 · Khó · Công suất toàn phần, công suất có ích và hiệu suất của máy bơm |
| HSG9 | Chuyên đề 13. Chuyển động cơ học và đồ thị ch (162) | Dạng 2 · Trung bình · Hai xe chuyển động ngược chiều: thời điểm gặp, vị trí gặp, |
| HSG9 | Chuyên đề 13. Chuyển động cơ học và đồ thị ch (162) | Dạng 3 · Trung bình · Vật có chiều dài: đoàn tàu qua người, qua cầu, gặp và vượt |
| HSG9 | Chuyên đề 02. Động năng, thế năng, cơ năng và (166) | Dạng 6 · Khó · Đồ thị năng lượng theo độ cao |
| HSG9 | Chuyên đề 02. Động năng, thế năng, cơ năng và (166) | Dạng 7 · Nâng cao · Bài toán nhiều giai đoạn: dốc – mặt ngang có ma sát – dốc |
| HSG9 | Chuyên đề 15. Âm thanh: sóng âm, độ to – độ c (150) | Dạng 1 · Dễ · Tốc độ truyền âm: thấy chớp rồi mới nghe sấm, quãng đường và thời  |
| HSG9 | Chuyên đề 15. Âm thanh: sóng âm, độ to – độ c (150) | Dạng 3 · Cơ bản · Tiếng vang: máy dò cá bằng siêu âm, khoảng cách tối thiểu để n |
| HSG9 | Chuyên đề 15. Âm thanh: sóng âm, độ to – độ c (150) | Dạng 5 · Vận dụng cao · Nguồn âm chuyển động và tiếng vang: tìm tốc độ xe từ tiế |
| HSG9 | Chuyên đề 16. Truyền năng lượng nhiệt và sự n (164) | Dạng 1 · Dễ · Dẫn nhiệt qua vách: tỉ số công suất theo độ dày và độ chênh nhiệt  |
| HSG9 | Chuyên đề 16. Truyền năng lượng nhiệt và sự n (164) | Dạng 2 · Trung bình · Hao phí không đổi: đun hai lần để khử nhiệt dung chưa biết |
| HSG9 | Chuyên đề 16. Truyền năng lượng nhiệt và sự n (164) | Dạng 4 · Nâng cao · Nở dài: khe hở đường ray, độ dãn của cầu, thước bị nở |
| HSG9 | Chuyên đề 16. Truyền năng lượng nhiệt và sự n (164) | Dạng 6 · Vận dụng cao · Mở rộng HSG: Hai vật khác chất cùng nở vì nhiệt |
| HSG9 | Chuyên đề 04. Đoạn mạch nối tiếp, song song v (157) | Dạng 1 · Cơ bản · Mạch hỗn hợp R1 nối tiếp (R2 // R3): bốn bước và tính ngược |
| HSG9 | Chuyên đề 04. Đoạn mạch nối tiếp, song song v (157) | Dạng 2 · Trung bình · Ampe kế, vôn kế thực: sai số và điều kiện chọn dụng cụ |
| HSG9 | Chuyên đề 04. Đoạn mạch nối tiếp, song song v (157) | Dạng 3 · Trung bình · Khoá K nối tắt đoạn song song và ẩn số điện trở |
| HSG9 | Chuyên đề 04. Đoạn mạch nối tiếp, song song v (157) | Dạng 4 · Kết hợp · Biến trở trong mạch hỗn hợp: giá trị cần chỉnh và miền số chỉ |
| HSG9 | Chuyên đề 04. Đoạn mạch nối tiếp, song song v (157) | Dạng 5 · Kết hợp · Mạch cầu cân bằng, chập hai điểm cùng điện thế |
| HSG9 | Chuyên đề 04. Đoạn mạch nối tiếp, song song v (157) | Dạng 6 · Nâng cao · Mạch ba tầng, đọc ampe kế nhánh trong, tính ngược tìm điện t |
| HSG9 | Chuyên đề 03. Điện trở và định luật Ohm (159) | Dạng 3 · Trung bình · Kéo dãn dây dẫn, thể tích không đổi: R tỉ lệ với bình phươ |
| HSG9 | Chuyên đề 03. Điện trở và định luật Ohm (159) | Dạng 5 · Trung bình · Biến trở mắc nối tiếp: khoảng dòng điều chỉnh, vị trí con  |
| HSG9 | Chuyên đề 03. Điện trở và định luật Ohm (159) | Dạng 6 · Khó · Ampe kế và vôn kế có điện trở: số chỉ, độ lệch so với giá trị thậ |
| HSG9 | Chuyên đề 05. Năng lượng của dòng điện, công  (165) | Dạng 1 · Dễ · Công suất định mức và công suất thực tế: bếp mắc vào hiệu điện thế |
| HSG9 | Chuyên đề 05. Năng lượng của dòng điện, công  (165) | Dạng 3 · Nâng cao · Tổn hao khi đun nước: hai lần đun, tìm công suất toả ra môi  |
| HSG9 | Chuyên đề 05. Năng lượng của dòng điện, công  (165) | Dạng 4 · Nâng cao · Hai đèn định mức mắc nối tiếp: độ sáng, dòng tối đa, điện tr |
| HSG9 | Chuyên đề 05. Năng lượng của dòng điện, công  (165) | Dạng 5 · Nâng cao · Cực đại công suất trên biến trở: giá trị R, công suất cực đạ |
| HSG9 | Chuyên đề 05. Năng lượng của dòng điện, công  (165) | Dạng 6 · Vận dụng cao · Dòng điện lớn trên dây: hao phí khi truyền tải, chọn apt |
| HSG9 | Chuyên đề 06. Khúc xạ ánh sáng, phản xạ toàn  (151) | Dạng 5 · Nâng cao · Lăng kính: góc lệch, tán sắc và màu sắc |
| HSG9 | Chuyên đề 06. Khúc xạ ánh sáng, phản xạ toàn  (151) | Dạng 6 · Nâng cao · Lăng kính phản xạ toàn phần: đổi môi trường bên ngoài |
| HSG9 | Chuyên đề 06. Khúc xạ ánh sáng, phản xạ toàn  (151) | Dạng 7 · Vận dụng cao · Mở rộng HSG: Sợi quang định lượng |
| HSG9 | Chuyên đề 07. Thấu kính mỏng và kính lúp (156) | Dạng 1 · Dễ · Dựng ảnh trên giấy ô ly: cho vật tìm ảnh, cho vật và ảnh tìm thấu  |
| HSG9 | Chuyên đề 07. Thấu kính mỏng và kính lúp (156) | Dạng 3 · Trung bình · Bài toán ngược nhiều trường hợp: ảnh gấp n lần vật, ảnh cá |
| HSG9 | Chuyên đề 07. Thấu kính mỏng và kính lúp (156) | Dạng 4 · Nâng cao · Dịch chuyển vật–ảnh: ảnh dịch theo chiều nào, khoảng cách vậ |
| HSG9 | Chuyên đề 07. Thấu kính mỏng và kính lúp (156) | Dạng 6 · Nâng cao · Kính lúp: ngắm chừng ở cực cận, ở vô cực và khoảng đặt vật |
| HSG9 | Chuyên đề 07. Thấu kính mỏng và kính lúp (156) | Dạng 7 · Vận dụng cao · Hệ hai thấu kính đồng trục: ảnh qua thấu kính 1 là vật c |
| HSG9 | Chuyên đề 14. Gương phẳng, bóng tối và nửa tố (158) | Dạng 4 · Vận dụng · Ảnh khi vật hoặc gương dịch chuyển |
| HSG9 | Chuyên đề 14. Gương phẳng, bóng tối và nửa tố (158) | Dạng 5 · Nâng cao · Vùng nhìn thấy, gương thấy toàn thân |
| HSG9 | Chuyên đề 14. Gương phẳng, bóng tối và nửa tố (158) | Dạng 6 · Nâng cao · Tia sáng qua điểm cho trước, đường đi ngắn nhất |
| HSG9 | Chuyên đề 17. Thiên văn: Mặt Trăng, Hệ Mặt Tr (178) | Dạng 1 · Dễ · Pha Mặt Trăng và lịch thực: từ ngày rằm suy ra các pha, ngày có th |
| HSG9 | Chuyên đề 17. Thiên văn: Mặt Trăng, Hệ Mặt Tr (178) | Dạng 2 · Trung bình · Góc trông: Mặt Trăng che kín Mặt Trời hay chỉ tạo nhật thự |
| HSG9 | Chuyên đề 17. Thiên văn: Mặt Trăng, Hệ Mặt Tr (178) | Dạng 3 · Nâng cao · Nón bóng Mặt Trăng và Trái Đất: vùng tối, vùng nửa tối, nhật |
| HSG9 | Chuyên đề 08. Cảm ứng điện từ và dòng điện xo (152) | Dạng 5 · Nâng cao · Mở rộng HSG: Đường dây thật — điện trở từ ρ, độ giảm thế, ch |
| HSG9 | Chuyên đề 08. Cảm ứng điện từ và dòng điện xo (152) | Dạng 6 · Vận dụng cao · Mở rộng HSG: Cho công suất nơi tiêu thụ — phương trình b |
| HSG9 | Chuyên đề 09. Năng lượng với cuộc sống: vòng  (163) | Dạng 5 · Vận dụng cao · So sánh phương án: xe máy xăng và xe máy điện, tính từ n |