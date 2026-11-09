# Rà soát dạng bài tập mẫu — còn xót bài/dạng nào (9/11/2026)

Chỉ đọc, không ghi DB. Nguồn: truy vấn thẳng DB 9/11/2026 (`lessons`, `chapter_classes`, `lesson_items` kind=`bai_tap_mau`, `question_topics`, `question_bank` chưa lưu trữ, `question_dang`) bằng `scripts/logs/ra-soat-dang-btm-20261109.mts` (gitignore; kết quả thô `scripts/logs/ra-soat-dang-btm-20261109.json`), so với `scripts/data/bai-tap-mau/<id>.json`.

## Trả lời thẳng

- **Chuẩn "một dạng – một hình": KHÔNG còn xót trong phạm vi 97 bài đã lên kế hoạch.** 97/97 bài có JSON ở repo đều đã lên DB, số dạng DB = repo, số hình `cong_cu.de` DB = repo, không còn `<figure` trong `problem_html`/`analysis_html`. Ghi chú cũ "Đ9 (KHTN 9 + HSG 9) chưa đăng" đã lỗi thời: 129–131, 150–167, 178 đều đã ở DB, khớp repo.
- **Dạng thiếu hình cố ý:** 46 (1/3 dạng có hình), 47 (2/3), 48 (1/3) — đúng ghi chú "46–48 có dạng cố ý không có hình".
- **Thật sự còn xót (chưa ai lên kế hoạch, không có trong 492 dạng của KE-HOACH-MODEL.md):** KHTN 9 **bài 85 Lăng kính (48 câu ngân hàng), 86 Thấu kính (54 câu), 88 Kính lúp. Bài tập thấu kính (0 câu), 92 Cảm ứng điện từ (23 câu)** — có lý thuyết hoặc câu ngân hàng nhưng chưa có mục bài tập mẫu. 93, 94, 95, 128 cũng chưa có, nhưng là bài gần như không có bài tập tính toán (0–3 câu ngân hàng; 92–95 và 128 còn chưa có mục nào, kể cả lý thuyết).
- **Còn BTM bản CŨ trên DB** (có `<figure`, không `cong_cu`, không JSON repo) ở 5 bài thầy đã chốt BỎ: 5, 59, 61, 64, 75. Học sinh vẫn thấy bản cũ này. Cần thầy quyết: để nguyên, gỡ, hay chuyển sang chuẩn mới.
- **Ngân hàng không chỉ ra chủ đề nào bị thiếu dạng:** không bài nào có số chủ đề ≥20 câu bài tập nhiều hơn số dạng. (Bảng `question_dang` mới gán 3–25% số câu bài tập ở nhiều bài, ví dụ 2, 5, 7, 8, 10, 11, 13, 14, 43, 50, 54, 60 — đó là việc gán dạng cho ôn tập (`on-tap-dang-bai-tap`), không phải thiếu dạng.)

## Trạng thái các bài trong danh sách "thầy chốt BỎ" (trạng thái THẬT trên DB)

| id | Bài | Thực tế 9/11 |
|---|---|---|
| 38 | L11 Thế năng điện | đã làm, 4 dạng, một-hình, DB = repo (không còn là "bỏ") |
| 46, 47, 48 | L10 Ch.1 | đã làm, 3 dạng mỗi bài, DB = repo, một số dạng cố ý không hình |
| 45 | L11 Thực hành suất điện động | đã làm, 3 dạng, đủ hình, DB = repo |
| 34 | L11 Bài 15 Thực hành đo tốc độ truyền âm | đã làm, DB = repo (không còn là "bỏ") |
| 59, 61, 64 | L10 ĐL1, ĐL3 Newton, Lực cản–lực nâng | **BTM cũ 3 dạng còn trên DB** (`<figure`), không JSON repo, 0 câu ngân hàng |
| 5, 75 | L12 thực hành nhiệt dung; L10 thực hành động lượng | **BTM cũ 4 dạng còn trên DB** (`<figure`), không JSON repo. Bài 5 có 1.124 câu ngân hàng (811 bài tập) — nhiều nhất trong nhóm |
| 12, 29, 51, 56, 65, 67 | thực hành / bài 20 ví dụ động lực học | không có mục BTM (đúng quyết định bỏ) |

## Việc cần làm tiếp (ưu tiên)

1. **Bài 5 (L12 nhiệt dung riêng…)** — kiến nghị **LÀM** (chờ thầy): BTM cũ còn hiện cho HS, chủ đề có 811 câu bài tập (Q = mcΔt, nhiệt nóng chảy/hoá hơi) — dạng tính nhiệt lượng rất hay thi. Có thể soạn lại 4 dạng theo chuẩn một-hình (`do_thi`/`cot` nhiệt).
2. **KHTN 9 bài 86 Thấu kính, 85 Lăng kính, 88 Kính lúp. Bài tập thấu kính** — kiến nghị **LÀM** (chờ thầy chốt có dạy KHTN 9 Ch.2 không): đã có lý thuyết, ngân hàng 48–54 câu; dùng lại họ `thau_kinh`, `tia_sang` (`canh: "tu_do"` đã có lăng kính từ Đ9c). 88 tên bài là "bài tập thấu kính" nên đáng có BTM nhất.
3. **KHTN 9 bài 92 Cảm ứng điện từ** — **chờ thầy**: chưa có cả lý thuyết; 23 câu ngân hàng. Làm khi soạn lý thuyết.
4. **59, 61, 64, 75 (BTM cũ còn trên DB)** — **chờ thầy**: (a) giữ bản cũ, (b) chuyển sang một-hình (59/61/64 là bài lý thuyết Newton, ngân hàng 0 câu vì câu gắn chủ đề cha ở bài 60), hoặc (c) gỡ mục. Không tự gỡ.
5. **Nhỏ:** `tom_de` thiếu ở 45, 46, 47, 48 (mọi dạng) và 13 (1/5 dạng) — repo cũng thiếu, nên là cố ý hoặc sót của đợt cũ; không chắc. UI vẫn chạy (dạng không `tom_de` thì không hiện dòng Tìm).
6. **Nhỏ:** mục `bai_tap_mau` RỖNG (0 dạng, đã xuất bản) ở 3 bài kiểm tra: 96 (KT giữa kì 1 L12), 98 (KT chương L11 Ch.1), 101 (KT chương L11 Ch.2). Không chắc HS có thấy một mục trống hay không — nên mở trang kiểm, nếu hiện thì gỡ.
7. 93, 94, 95, 128 (KHTN 9) — kiến nghị **BỎ** (bài định tính/mở đầu, 0–3 câu ngân hàng, chưa có lý thuyết).

## Dải id không có JSON — là gì

| id | Là gì | Cần BTM theo dạng? |
|---|---|---|
| 1, 80–82, 112, 124, 133–149 | không tồn tại trong `lessons` (đã xoá hoặc không dùng) | không |
| 85–88, 92–95, 128 | KHTN 9 (xem trên) | 85, 86, 88 nên có; 92 khi có lý thuyết; còn lại không |
| 96–111, 113–123 | bài Kiểm tra chương / giữa kì / cuối kì (lesson_kind kiểm tra) | không (96, 98, 101 có mục BTM rỗng) |
| 132 | "Đề thi thử các trường, sở GD&ĐT 2026" (L12, kind bai_hoc nhưng chỉ có đề) | không |
| 168–177, 184 | Anh văn chuyên ngành Cơ khí — mục BTM là đề mẫu kiểu khác (không `problem_html`) | không theo chuẩn dạng |
| 179–183 | Giải Vật lí bằng Casio — mục BTM kiểu khác | không theo chuẩn dạng |
| 185–200 | WorldSkills Industrial Mechanics (chỉ lý thuyết) | không |

Ghi chú: các chuyên đề HSG 9 (150–167, 178) trong `chapter_classes` gắn với lớp **KHTN 9** (id 15), không thấy gắn lớp "Học sinh giỏi & Chuyên Vật lý 9" (id 19) — không chắc đó là cố ý (khoá HSG có thể đi qua bảng khoá học khác). Bài 167 "Bài tập tuần này" có 12 dạng (bộ tự luận tuần), không phải bài lý thuyết.

## Bảng đầy đủ theo lớp → chương → bài

Cột "Hình `de` · `<figure` · tom_de · buoc" đếm số dạng trên DB. Tổng dạng trên DB (L10–12 + KHTN 9/HSG 9): 522, trong đó 17 dạng thuộc 5 bài BTM cũ (5, 59, 61, 64, 75) → 505 dạng chuẩn mới ở 97 bài.

### Lớp 12 · Chương 1: Vật lí nhiệt

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 2 | Bài 1. Sự chuyển thể | 5 / 5 | 5 · 0 · 5 · 5 | 732/179 | ✓ đủ một-dạng-một-hình, DB = repo |
| 3 | Bài 2. Thang nhiệt độ | 6 / 6 | 6 · 0 · 6 · 6 | 622/345 | ✓ đủ một-dạng-một-hình, DB = repo |
| 4 | Bài 3. Nội năng. Định luật 1 của nhiệt động lực học | 5 / 5 | 5 · 0 · 5 · 5 | 650/289 | ✓ đủ một-dạng-một-hình, DB = repo |
| 5 | Bài 4. Thực hành đo nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá | 4 / — | 0 · 4 · 0 · 4 | 1124/811 | **BTM bản cũ** (`<figure`, chưa một-hình, không có JSON repo) · thầy chốt BỎ (đợt F) |
| 96 | Kiểm tra giữa học kì 1 | 0 / — | — | 0/0 | kiểm tra — không cần BTM (có mục BTM rỗng 0 dạng) |
| 97 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 12 · Chương 2: Khí lí tưởng

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 6 | Bài 5. Thuyết động học phân tử chất khí | 5 / 5 | 5 · 0 · 5 · 5 | 382/103 | ✓ đủ một-dạng-một-hình, DB = repo |
| 7 | Bài 6. Định luật Boyle. Định luật Charles | 5 / 5 | 5 · 0 · 5 · 5 | 1026/563 | ✓ đủ một-dạng-một-hình, DB = repo |
| 8 | Bài 7. Phương trình trạng thái của khí lí tưởng | 5 / 5 | 5 · 0 · 5 · 5 | 693/513 | ✓ đủ một-dạng-một-hình, DB = repo |
| 9 | Bài 8. Áp suất - động năng của phân tử khí | 5 / 5 | 5 · 0 · 5 · 5 | 347/161 | ✓ đủ một-dạng-một-hình, DB = repo |
| 100 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |
| 121 | Kiểm tra cuối học kì 1 | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 12 · Chương 3: Từ trường

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 10 | Bài 9. Khái niệm từ trường | 4 / 4 | 4 · 0 · 4 · 4 | 392/81 | ✓ đủ một-dạng-một-hình, DB = repo |
| 11 | Bài 10. Lực từ. Cảm ứng từ | 6 / 6 | 6 · 0 · 6 · 6 | 672/402 | ✓ đủ một-dạng-một-hình, DB = repo |
| 12 | Bài 11. Thực hành đo độ lớn cảm ứng từ | — / — | — | 0/0 | chưa có mục BTM · thầy chốt BỎ (đợt F) |
| 13 | Bài 12. Hiện tượng cảm ứng điện từ | 5 / 5 | 5 · 0 · 4 · 5 | 979/503 | ✓ đủ một-dạng-một-hình, DB = repo |
| 14 | Bài 13. Đại cương về dòng điện xoay chiều | 5 / 5 | 5 · 0 · 5 · 5 | 880/413 | ✓ đủ một-dạng-một-hình, DB = repo |
| 125 | Bài 14. Máy phát điện xoay chiều. Máy biến áp | 5 / 5 | 5 · 0 · 5 · 5 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 122 | Kiểm tra giữa học kì 2 | — / — | — | 0/0 | kiểm tra — không cần BTM |
| 126 | Bài 15. Một số ứng dụng của cảm ứng điện từ | 4 / 4 | 4 · 0 · 4 · 4 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 127 | Bài 16. Điện từ trường. Mô hình sóng điện từ | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 103 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 12 · Chương 4: Vật lí hạt nhân

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 15 | Bài 14. Hạt nhân và mô hình nguyên tử | 5 / 5 | 5 · 0 · 5 · 5 | 443/197 | ✓ đủ một-dạng-một-hình, DB = repo |
| 16 | Bài 15. Năng lượng liên kết hạt nhân | 6 / 6 | 6 · 0 · 6 · 6 | 294/140 | ✓ đủ một-dạng-một-hình, DB = repo |
| 17 | Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng | 5 / 5 | 5 · 0 · 5 · 5 | 475/315 | ✓ đủ một-dạng-một-hình, DB = repo |
| 18 | Bài 17. Hiện tượng phóng xạ | 5 / 5 | 5 · 0 · 5 · 5 | 644/443 | ✓ đủ một-dạng-một-hình, DB = repo |
| 19 | Bài 18. An toàn phóng xạ | 6 / 6 | 6 · 0 · 6 · 6 | 143/12 | ✓ đủ một-dạng-một-hình, DB = repo |
| 106 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |
| 123 | Kiểm tra cuối học kì 2 | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 12 · Đề thi thử các trường, sở GD&ĐT 2026

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 132 | Đề thi thử các trường, sở GD&ĐT 2026 | — / — | — | 354/153 | chưa có mục BTM |

### Lớp 11 · Chương 1: Dao động

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 20 | Bài 1. Dao động điều hoà | 5 / 5 | 5 · 0 · 5 · 5 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 21 | Bài 2. Mô tả dao động điều hoà | 5 / 5 | 5 · 0 · 5 · 5 | 786/384 | ✓ đủ một-dạng-một-hình, DB = repo |
| 22 | Bài 3. Vận tốc, gia tốc trong dao động điều hoà | 5 / 5 | 5 · 0 · 5 · 5 | 338/155 | ✓ đủ một-dạng-một-hình, DB = repo |
| 23 | Bài 4. Bài tập về dao động điều hoà | 5 / 5 | 5 · 0 · 5 · 5 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 24 | Bài 5. Động năng. Thế năng. Sự chuyển hoá giữa động năng và thế năng t | 5 / 5 | 5 · 0 · 5 · 5 | 388/206 | ✓ đủ một-dạng-một-hình, DB = repo |
| 25 | Bài 6. Dao động tắt dần. Dao động cưỡng bức. Hiện tượng cộng hưởng | 5 / 5 | 5 · 0 · 5 · 5 | 348/85 | ✓ đủ một-dạng-một-hình, DB = repo |
| 26 | Bài 7. Bài tập về sự chuyển hoá năng lượng trong dao động điều hoà | 5 / 5 | 5 · 0 · 5 · 5 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 98 | Kiểm tra chương | 0 / — | — | 0/0 | kiểm tra — không cần BTM (có mục BTM rỗng 0 dạng) |
| 117 | Kiểm tra giữa học kì 1 | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 11 · Chương 2: Sóng

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 27 | Bài 8. Mô tả sóng | 5 / 5 | 5 · 0 · 5 · 5 | 386/230 | ✓ đủ một-dạng-một-hình, DB = repo |
| 28 | Bài 9. Sóng ngang, sóng dọc, sự truyền năng lượng của sóng cơ | 6 / 6 | 6 · 0 · 6 · 6 | 134/6 | ✓ đủ một-dạng-một-hình, DB = repo |
| 29 | Bài 10. Thực hành: Đo tần số của sóng âm | — / — | — | 0/0 | chưa có mục BTM · thầy chốt BỎ (đợt F) |
| 30 | Bài 11. Sóng điện từ | 4 / 4 | 4 · 0 · 4 · 4 | 245/41 | ✓ đủ một-dạng-một-hình, DB = repo |
| 31 | Bài 12. Giao thoa sóng | 5 / 5 | 5 · 0 · 5 · 5 | 338/185 | ✓ đủ một-dạng-một-hình, DB = repo |
| 32 | Bài 13. Sóng dừng | 6 / 6 | 6 · 0 · 6 · 6 | 220/97 | ✓ đủ một-dạng-một-hình, DB = repo |
| 33 | Bài 14. Bài tập về sóng | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 34 | Bài 15. Thực hành: Đo tốc độ truyền âm | 4 / 4 | 4 · 0 · 4 · 4 | 102/31 | ✓ đủ một-dạng-một-hình, DB = repo · (đợt F từng chốt BỎ — nay đã làm) |
| 101 | Kiểm tra chương | 0 / — | — | 0/0 | kiểm tra — không cần BTM (có mục BTM rỗng 0 dạng) |
| 118 | Kiểm tra cuối học kì 1 | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 11 · Chương 3: Điện trường

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 35 | Bài 16. Lực tương tác giữa hai điện tích | 5 / 5 | 5 · 0 · 5 · 5 | 253/113 | ✓ đủ một-dạng-một-hình, DB = repo |
| 36 | Bài 17. Khái niệm điện trường | 5 / 5 | 5 · 0 · 5 · 5 | 255/91 | ✓ đủ một-dạng-một-hình, DB = repo |
| 37 | Bài 18. Điện trường đều | 5 / 5 | 5 · 0 · 5 · 5 | 167/62 | ✓ đủ một-dạng-một-hình, DB = repo |
| 38 | Bài 19. Thế năng điện | 4 / 4 | 4 · 0 · 4 · 4 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo · (đợt E từng chốt BỎ — nay đã làm) |
| 39 | Bài 20. Điện thế | 5 / 5 | 5 · 0 · 5 · 5 | 347/157 | ✓ đủ một-dạng-một-hình, DB = repo |
| 40 | Bài 21. Tụ điện | 5 / 5 | 5 · 0 · 5 · 5 | 235/107 | ✓ đủ một-dạng-một-hình, DB = repo |
| 104 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |
| 119 | Kiểm tra giữa học kì 2 | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 11 · Chương 4: Dòng điện. Mạch điện

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 41 | Bài 22. Cường độ dòng điện | 5 / 5 | 5 · 0 · 5 · 5 | 142/47 | ✓ đủ một-dạng-một-hình, DB = repo |
| 42 | Bài 23. Điện trở. Định luật Ohm | 5 / 5 | 5 · 0 · 5 · 5 | 149/57 | ✓ đủ một-dạng-một-hình, DB = repo |
| 43 | Bài 24. Nguồn điện | 4 / 4 | 4 · 0 · 4 · 4 | 219/86 | ✓ đủ một-dạng-một-hình, DB = repo |
| 44 | Bài 25. Năng lượng điện và công suất điện | 5 / 5 | 5 · 0 · 5 · 5 | 134/46 | ✓ đủ một-dạng-một-hình, DB = repo |
| 45 | Bài 26. Thực hành: Đo suất điện động và điện trở trong của pin điện ho | 3 / 3 | 3 · 0 · 0 · 3 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo · (đợt F từng chốt BỎ — nay đã làm) |
| 107 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |
| 120 | Kiểm tra cuối học kì 2 | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 10 · Chương 1: Mở đầu

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 46 | Bài 1. Làm quen với Vật lí | 3 / 3 | 2 · 0 · 0 · 3 | 0/0 | ✓ DB = repo; 1 dạng cố ý không hình · (đợt E từng chốt BỎ — nay đã làm) |
| 47 | Bài 2. Các quy tắc an toàn trong phòng thực hành Vật lí | 3 / 3 | 1 · 0 · 0 · 3 | 707/23 | ✓ DB = repo; 2 dạng cố ý không hình · (đợt F từng chốt BỎ — nay đã làm) |
| 48 | Bài 3. Thực hành tính sai số trong phép đo. Ghi kết quả đo | 3 / 3 | 2 · 0 · 0 · 3 | 366/123 | ✓ DB = repo; 1 dạng cố ý không hình · (đợt F từng chốt BỎ — nay đã làm) |
| 99 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 10 · Chương 2: Động học

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 49 | Bài 4. Độ dịch chuyển và quãng đường đi được | 5 / 5 | 5 · 0 · 5 · 5 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 50 | Bài 5. Tốc độ và vận tốc | 6 / 6 | 6 · 0 · 6 · 6 | 1127/543 | ✓ đủ một-dạng-một-hình, DB = repo |
| 51 | Bài 6. Thực hành: Đo tốc độ của vật chuyển động | — / — | — | 0/0 | chưa có mục BTM · thầy chốt BỎ (đợt F) |
| 52 | Bài 7. Đồ thị độ dịch chuyển - thời gian | 4 / 4 | 4 · 0 · 4 · 4 | 286/151 | ✓ đủ một-dạng-một-hình, DB = repo |
| 53 | Bài 8. Chuyển động biến đổi. Gia tốc | 5 / 5 | 5 · 0 · 5 · 5 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 54 | Bài 9. Chuyển động thẳng biến đổi đều | 6 / 6 | 6 · 0 · 6 · 6 | 1080/576 | ✓ đủ một-dạng-một-hình, DB = repo |
| 55 | Bài 10. Sự rơi tự do | 5 / 5 | 5 · 0 · 5 · 5 | 463/281 | ✓ đủ một-dạng-một-hình, DB = repo |
| 56 | Bài 11. Thực hành: Đo gia tốc rơi tự do | — / — | — | 0/0 | chưa có mục BTM · thầy chốt BỎ (đợt F) |
| 57 | Bài 12. Chuyển động ném | 6 / 6 | 6 · 0 · 6 · 6 | 397/224 | ✓ đủ một-dạng-một-hình, DB = repo |
| 102 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |
| 113 | Kiểm tra giữa học kì 1 | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 10 · Chương 3: Động lực học

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 58 | Bài 13. Tổng hợp và phân tích lực. Cân bằng lực | 6 / 6 | 6 · 0 · 6 · 6 | 323/133 | ✓ đủ một-dạng-một-hình, DB = repo |
| 59 | Bài 14. Định luật 1 Newton | 3 / — | 0 · 3 · 0 · 3 | 0/0 | **BTM bản cũ** (`<figure`, chưa một-hình, không có JSON repo) · thầy chốt BỎ (đợt E) |
| 60 | Bài 15. Định luật 2 Newton | 6 / 6 | 6 · 0 · 6 · 6 | 838/384 | ✓ đủ một-dạng-một-hình, DB = repo |
| 61 | Bài 16. Định luật 3 Newton | 3 / — | 0 · 3 · 0 · 3 | 0/0 | **BTM bản cũ** (`<figure`, chưa một-hình, không có JSON repo) · thầy chốt BỎ (đợt E) |
| 62 | Bài 17. Trọng lực và lực căng | 5 / 5 | 5 · 0 · 5 · 5 | 247/104 | ✓ đủ một-dạng-một-hình, DB = repo |
| 63 | Bài 18. Lực ma sát | 5 / 5 | 5 · 0 · 5 · 5 | 418/202 | ✓ đủ một-dạng-một-hình, DB = repo |
| 64 | Bài 19. Lực cản và lực nâng | 3 / — | 0 · 3 · 0 · 3 | 0/0 | **BTM bản cũ** (`<figure`, chưa một-hình, không có JSON repo) · thầy chốt BỎ (đợt E) |
| 65 | Bài 20. Một số ví dụ về cách giải các bài toán thuộc phần động lực học | — / — | — | 0/0 | chưa có mục BTM · thầy chốt BỎ (đợt F) |
| 66 | Bài 21. Moment lực. Cân bằng của vật rắn | 5 / 5 | 5 · 0 · 5 · 5 | 267/112 | ✓ đủ một-dạng-một-hình, DB = repo |
| 67 | Bài 22. Thực hành: Tổng hợp lực | — / — | — | 0/0 | chưa có mục BTM · thầy chốt BỎ (đợt F) |
| 105 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 10 · Chương 4: Năng lượng, công, công suất

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 68 | Bài 23. Năng lượng. Công cơ học | 5 / 5 | 5 · 0 · 5 · 5 | 376/171 | ✓ đủ một-dạng-một-hình, DB = repo |
| 69 | Bài 24. Công suất | 5 / 5 | 5 · 0 · 5 · 5 | 240/95 | ✓ đủ một-dạng-một-hình, DB = repo |
| 70 | Bài 25. Động năng, thế năng | 5 / 5 | 5 · 0 · 5 · 5 | 324/148 | ✓ đủ một-dạng-một-hình, DB = repo |
| 71 | Bài 26. Cơ năng và định luật bảo toàn cơ năng | 5 / 5 | 5 · 0 · 5 · 5 | 209/89 | ✓ đủ một-dạng-một-hình, DB = repo |
| 72 | Bài 27. Hiệu suất | 5 / 5 | 5 · 0 · 5 · 5 | 169/64 | ✓ đủ một-dạng-một-hình, DB = repo |
| 108 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |
| 114 | Kiểm tra cuối học kì 1 | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 10 · Chương 5: Động lượng

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 73 | Bài 28. Động lượng | 5 / 5 | 5 · 0 · 5 · 5 | 228/132 | ✓ đủ một-dạng-một-hình, DB = repo |
| 74 | Bài 29. Định luật bảo toàn động lượng | 5 / 5 | 5 · 0 · 5 · 5 | 188/101 | ✓ đủ một-dạng-một-hình, DB = repo |
| 75 | Bài 30. Thực hành: Xác định động lượng của vật trước và sau va chạm | 4 / — | 0 · 4 · 0 · 4 | 0/0 | **BTM bản cũ** (`<figure`, chưa một-hình, không có JSON repo) · thầy chốt BỎ (đợt F) |
| 109 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |
| 115 | Kiểm tra giữa học kì 2 | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 10 · Chương 6: Chuyển động tròn

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 76 | Bài 31. Động học của chuyển động tròn đều | 5 / 5 | 5 · 0 · 5 · 5 | 249/129 | ✓ đủ một-dạng-một-hình, DB = repo |
| 77 | Bài 32. Lực hướng tâm và gia tốc hướng tâm | 5 / 5 | 5 · 0 · 5 · 5 | 180/81 | ✓ đủ một-dạng-một-hình, DB = repo |
| 110 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp 10 · Chương 7: Biến dạng của vật rắn. Áp suất chất lỏng

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 78 | Bài 33. Biến dạng của vật rắn | 5 / 5 | 5 · 0 · 5 · 5 | 173/55 | ✓ đủ một-dạng-một-hình, DB = repo |
| 79 | Bài 34. Khối lượng riêng. Áp suất chất lỏng | 5 / 5 | 5 · 0 · 5 · 5 | 198/66 | ✓ đủ một-dạng-một-hình, DB = repo |
| 111 | Kiểm tra chương | — / — | — | 0/0 | kiểm tra — không cần BTM |
| 116 | Kiểm tra cuối học kì 2 | — / — | — | 0/0 | kiểm tra — không cần BTM |

### Lớp KHTN 9 · Mở đầu

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 128 | Bài 1. Giới thiệu một số dụng cụ và hóa chất. Thuyết trình một vấn đề  | — / — | — | 0/0 | chưa có mục BTM |

### Lớp KHTN 9 · Chương 1: Năng lượng cơ học

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 129 | Bài 2. Động năng. Thế năng | 4 / 4 | 4 · 0 · 4 · 4 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 130 | Bài 3. Cơ năng | 4 / 4 | 4 · 0 · 4 · 4 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 131 | Bài 4. Công và công suất | 4 / 4 | 4 · 0 · 4 · 4 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |

### Lớp KHTN 9 · Chương 2: Ánh sáng

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 83 | Bài 5. Khúc xạ ánh sáng | 5 / 5 | 5 · 0 · 5 · 5 | 98/33 | ✓ đủ một-dạng-một-hình, DB = repo |
| 84 | Bài 6. Phản xạ toàn phần | 4 / 4 | 4 · 0 · 4 · 4 | 79/15 | ✓ đủ một-dạng-một-hình, DB = repo |
| 85 | Bài 7. Lăng kính | — / — | — | 48/1 | chưa có mục BTM |
| 86 | Bài 8. Thấu kính | — / — | — | 54/7 | chưa có mục BTM |
| 87 | Bài 9. Thực hành đo tiêu cự của thấu kính hội tụ | — / — | — | 0/0 | chưa có mục BTM |
| 88 | Bài 10. Kính lúp. Bài tập thấu kính | — / — | — | 0/0 | chưa có mục BTM |

### Lớp KHTN 9 · Chương 3: Điện

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 89 | Bài 11. Điện trở. Định luật Ohm | 4 / 4 | 4 · 0 · 4 · 4 | 65/5 | ✓ đủ một-dạng-một-hình, DB = repo |
| 90 | Bài 12. Đoạn mạch nối tiếp, song song | 4 / 4 | 4 · 0 · 4 · 4 | 53/4 | ✓ đủ một-dạng-một-hình, DB = repo |
| 91 | Bài 13. Năng lượng của dòng điện và công suất điện | 4 / 4 | 4 · 0 · 4 · 4 | 52/4 | ✓ đủ một-dạng-một-hình, DB = repo |

### Lớp KHTN 9 · Chương 4: Điện từ

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 92 | Bài 14. Cảm ứng điện từ. Nguyên tắc tạo ra dòng điện xoay chiều | — / — | — | 23/7 | chưa có mục BTM |
| 93 | Bài 15. Tác dụng của dòng điện xoay chiều | — / — | — | 0/0 | chưa có mục BTM |

### Lớp KHTN 9 · Chương 5: Năng lượng với cuộc sống

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 94 | Bài 16. Vòng năng lượng trên Trái Đất. Năng lượng hóa thạch | — / — | — | 2/1 | chưa có mục BTM |
| 95 | Bài 17. Một số dạng năng lượng tái tạo | — / — | — | 3/3 | chưa có mục BTM |

### Lớp KHTN 9 · Nền tảng: công cụ toán học và thực hành

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 160 | Chuyên đề 00. Kỹ năng nền: công cụ toán học, đọc đồ thị, sai số và thự | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |

### Lớp KHTN 9 · Cơ học và năng lượng cơ học

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 167 | Bài tập tuần này: 12 bài tự luận Cơ học (Vận dụng → Vận dụng cao) | 12 / 12 | 12 · 0 · 12 · 12 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 161 | Chuyên đề 01. Công và công suất | 7 / 7 | 7 · 0 · 7 · 7 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 166 | Chuyên đề 02. Động năng, thế năng, cơ năng và định luật bảo toàn cơ nă | 7 / 7 | 7 · 0 · 7 · 7 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 155 | Chuyên đề 10. Lực: tổng hợp lực, cân bằng, ma sát, đòn bẩy | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 154 | Chuyên đề 11. Cơ học chất lưu: áp suất chất lỏng, bình thông nhau và l | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 162 | Chuyên đề 13. Chuyển động cơ học và đồ thị chuyển động | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |

### Lớp KHTN 9 · Nhiệt học và âm thanh

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 153 | Chuyên đề 12. Nhiệt học nâng cao: phương trình cân bằng nhiệt và chuyể | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 164 | Chuyên đề 16. Truyền năng lượng nhiệt và sự nở vì nhiệt | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 150 | Chuyên đề 15. Âm thanh: sóng âm, độ to – độ cao, phản xạ âm | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |

### Lớp KHTN 9 · Điện học

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 159 | Chuyên đề 03. Điện trở và định luật Ohm | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 157 | Chuyên đề 04. Đoạn mạch nối tiếp, song song và mạch hỗn hợp | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 165 | Chuyên đề 05. Năng lượng của dòng điện, công suất điện và định luật Jo | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |

### Lớp KHTN 9 · Quang học và Trái Đất – bầu trời

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 151 | Chuyên đề 06. Khúc xạ ánh sáng, phản xạ toàn phần, lăng kính và tán sắ | 7 / 7 | 7 · 0 · 7 · 7 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 156 | Chuyên đề 07. Thấu kính mỏng và kính lúp | 7 / 7 | 7 · 0 · 7 · 7 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 158 | Chuyên đề 14. Gương phẳng, bóng tối và nửa tối | 7 / 7 | 7 · 0 · 7 · 7 | 52/7 | ✓ đủ một-dạng-một-hình, DB = repo |
| 178 | Chuyên đề 17. Thiên văn: Mặt Trăng, Hệ Mặt Trời và Ngân Hà | 6 / 6 | 6 · 0 · 6 · 6 | 49/3 | ✓ đủ một-dạng-một-hình, DB = repo |

### Lớp KHTN 9 · Điện từ và năng lượng với cuộc sống

| id | Bài | Dạng DB / repo | Hình `de` · `<figure` · tom_de · buoc (DB) | Câu ngân hàng (tất cả/bài tập) | Trạng thái |
|---|---|---|---|---|---|
| 152 | Chuyên đề 08. Cảm ứng điện từ và dòng điện xoay chiều | 6 / 6 | 6 · 0 · 6 · 6 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
| 163 | Chuyên đề 09. Năng lượng với cuộc sống: vòng năng lượng Trái Đất, nhiê | 5 / 5 | 5 · 0 · 5 · 5 | 0/0 | ✓ đủ một-dạng-một-hình, DB = repo |
