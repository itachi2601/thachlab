# Khoá "Vật lí HSG & chuyên" (KHTN 9) — khung và bản đồ ánh xạ

Chốt 10/10/2026. Đích: HSG cấp thành phố, tuyển sinh lớp 10 chuyên Lê Hồng Phong, Trần Đại Nghĩa.
Đối chiếu đề cương **THI HSG 9 KHTN 26-27** (mạch "Năng lượng và sự biến đổi" + phần chung Trái Đất – bầu trời).

## Cách đặt trên web
- Không tạo lớp mới (vì `classGrade()` gom theo chữ số "9" nên lớp mới sẽ trộn vào KHTN 9). Khoá là **một môn thứ 4** trong lớp KHTN 9: `academic_subjects.code = 'hsg-vat-ly'`, hiện thành tab "Vật lí HSG & chuyên" cạnh Vật lý / Hóa học / Sinh học ở `/lop-hoc`.
- 6 chương (chapters.subject_code = 'hsg-vat-ly', gắn class_id = 15), mỗi **chuyên đề = một bài** (lessons). Một bài có các mục: `ly_thuyet` (lý thuyết nâng cao), `bai_tap_mau` (dạng bài có từng bước), `luyen_tap` (đề luyện — thầy cung cấp sau), đề thật vào mục riêng khi có.
- Seed dữ liệu: `supabase/migrations/20261010100000_khoa_hsg9_vat_ly_khung.sql` (tất cả bài `published=false`; thầy bật khi duyệt).
- Nguồn nội dung: 14 file docx ở `~/Documents/THPT/Lop09/00_Dung_chung/HSG_KHTN9_Vat_li/01_Chuyen_de/`. Khung mỗi file: A yêu cầu cần đạt · B lý thuyết (chuẩn + mở rộng) · C dạng bài + phương pháp · D ví dụ có lời giải · E tự luyện + đáp án · G nâng cao kiểu đề HSG · H lỗi thường gặp.
- Làm thử trọn vẹn: **CĐ01 + CĐ02**. Nội dung ở `content/hsg9/`.

## Bản đồ chuyên đề → chương → bài đã có → YCCĐ dùng cho "Làm bài tương tự"
Bài tương tự lấy từ `question_bank` theo YCCĐ (`question_topics`). KHTN 9 chưa có YCCĐ; dùng YCCĐ lớp 10–12 trùng chủ đề (id trong ngoặc).

| CĐ | Tên | Chương | Bài KHTN 9 | Bài lớp 10–12 trùng chủ đề | YCCĐ (id) |
|---|---|---|---|---|---|
| 00 | Kỹ năng nền | Nền tảng | — | L10 b3 (48) sai số | — (không có) |
| 01 | Công và công suất | Cơ học | 131 | L10 b23 (68), b24 (69), b27 (72) | 132, 134, 135, 140 |
| 02 | Động năng, thế năng, cơ năng | Cơ học | 129, 130 | L10 b25 (70), b26 (71) | 136–139 |
| 10 | **Lực** (mới) | Cơ học | — | L10 b13 (58), b17 (62), b18 (63), b21 (66) | 119–121, 125–131 |
| 11 | Cơ học chất lưu | Cơ học | — | L10 b34 (79) | 152, 153 |
| 13 | Chuyển động và đồ thị | Cơ học | — | L10 b5 (50), b7 (52) | 107–111 |
| 12 | Nhiệt học nâng cao | Nhiệt – âm | — | L12 b1–b4 (2–5) | 195–203 |
| 16 | **Truyền nhiệt, nở vì nhiệt** (mới) | Nhiệt – âm | — | L12 b3 (4) | 198, 199 |
| 15 | **Âm thanh** (mới) | Nhiệt – âm | — | L11 b8 (27), b9 (28), b10 (29), b15 (34) | 164–167 |
| 03 | Điện trở, định luật Ohm | Điện | 89 | L11 b23 (42) | 189, 190 |
| 04 | Mạch nối tiếp, song song, hỗn hợp | Điện | 90 | L11 b22–b24 (41–43) | 187–192 (gần) |
| 05 | Công suất điện, Joule–Lenz | Điện | 91 | L11 b25 (44) | 193, 194 |
| 06 | Khúc xạ, phản xạ toàn phần, lăng kính | Quang – TĐ | 83, 84, 85 | — | — |
| 07 | Thấu kính, kính lúp | Quang – TĐ | 86, 87, 88 | — | — |
| 14 | Gương phẳng; Trái Đất – bầu trời | Quang – TĐ | — | — | — |
| 08 | Cảm ứng điện từ, dòng xoay chiều | Điện từ – NL | 92, 93 | L12 b12–b15 (13, 14, 125, 126) | 217–220, 235–238 |
| 09 | Năng lượng với cuộc sống | Điện từ – NL | 94, 95 | L12 b16 (17) phân hạch/nhiệt hạch | — |

## Đối chiếu với đề cương "THI HSG 9 KHTN 26-27" (mạch Năng lượng)
Đủ: tốc độ (13), năng lượng cơ học (01, 02), khối lượng riêng – áp suất (11), năng lượng nhiệt (12), ánh sáng (06, 07, 14), điện (03–05), điện từ (08), Hệ Mặt Trời – Mặt Trăng (14), nhiên liệu hoá thạch và ấm lên toàn cầu (09).
Thiếu (đã đặt chỗ trong khung, bài ẩn, "đang soạn"): **CĐ10 Lực** · **CĐ15 Âm thanh** · **CĐ16 Truyền nhiệt và nở vì nhiệt**. Mỏng: Ngân Hà (14), chu trình carbon (09), áp suất khí quyển (11) — thêm đoạn lý thuyết khi soạn lại.

## Quy trình mỗi chuyên đề
1. Lý thuyết nâng cao: từ mục A + B (+ H) của docx, rút gọn theo `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`; ghi bằng `bash scripts/cap-nhat-ly-thuyet.sh content/hsg9/<cd>/theory.html <lesson_id>`.
2. Bài tập mẫu: theo skill `soan-bai-tap-mau` (dạng lấy từ mục C + D của docx, `topic` = YCCĐ ở bảng trên); E + G đưa vào tự luận có lời giải; ghi bằng `publish-bai-tap-mau.mts`.
3. Đề luyện + đề thật: thầy cung cấp sau, gắn vào mục `luyen_tap`.

## lesson_id đã tạo (migration chạy 10/10/2026)
CĐ00=160 · CĐ01=161 · CĐ02=166 · CĐ03=159 · CĐ04=157 · CĐ05=165 · CĐ06=151 · CĐ07=156 · CĐ08=152 · CĐ09=163 · CĐ10=155 · CĐ11=154 · CĐ12=153 · CĐ13=162 · CĐ14=158 · CĐ15=150 · CĐ16=164. Bài tập mẫu: `scripts/data/bai-tap-mau/<lesson_id>.json` (161, 166).
