---
name: project-thachlab-l10-ly-thuyet-ch5-7
description: 9 bài lý thuyết tương tác lớp 10 còn thiếu (Ch5 động lượng, Ch6 tròn đều, Ch7 biến dạng/áp suất, B20, B22) soạn + kiểm chéo + ghi DB + deploy 2026-10-06
metadata:
  type: project
---

Thầy yêu cầu 6/10/2026 "soạn lý thuyết tương tác cho phần còn lại của lớp" → chọn lớp 10. 9 bài, thư mục `content/lesson-samples/l10-*`:
B28 `dong-luong` (lesson 73), B29 `bao-toan-dong-luong` (74), B30 `thuc-hanh-dong-luong` (75), B31 `chuyen-dong-tron-deu` (76),
B32 `luc-huong-tam` (77), B33 `bien-dang-vat-ran` (78), B34 `khoi-luong-rieng-ap-suat` (79), B20 `giai-bai-toan-dong-luc-hoc` (65),
B22 `thuc-hanh-tong-hop-luc` (67). Commit d840ea842 (lô 1), b603f8ea3 (lô 2), 6d7da8f4a (nhật ký skill); kho thí nghiệm 211→244.
Đã `cap-nhat-ly-thuyet.sh` 7/9 bài + deploy 6/10. **B20 (65) và B22 (67) KHÔNG lên DB hôm đó** (lesson_items rỗng, script đòi đúng 1 dòng) — phát hiện 9/10/2026 qua `public/data/lessons/65|67.json` items=[]; 9/10 đã kiểm chéo lại (bài 67 sửa 3 chỗ lộ đáp án, commit 4f56f73e9), đăng bằng `upload-lesson.mts` (tạo mục Lý thuyết + đề Luyện tập 904/905) + deploy. Lớp 10 giờ đủ 34/34 bài lý thuyết tương tác.

**Treo:** chưa xem ảnh `sec-*` B30 và fig B28 sau sửa chữ SVG; B20 nhãn F_ms hình 3–4 hơi chạm mép thùng; B20/B22 chưa đối chiếu SGK
(bài cũ 65/67 không có nội dung); chưa còn bài lý thuyết tương tác nào thiếu ở lớp 10. Lớp 11 còn: B4, B7, B9, B10, B11, B15; lớp 12: KHÔNG còn bài nào (kiểm DB 9/10/2026: 20/20 bài lý thuyết tương tác, file = DB).
Bài học đã ghi ở cuối skill `soan-bai-ly-thuyet-tuong-tac` (chữ SVG ≥17, bảng không đứng trước quiz, `</div>` khung quiz).
