# Báo cáo sơ bộ ngân hàng câu hỏi theo bài — 24/10/2026

Đo trực tiếp trên DB production (chỉ đọc). Ngân hàng đang bật: **24.512 câu** (L12 10.185 · L11 4.790 · L10 8.350 · L9 467 · chưa gắn lớp 909; đã lưu trữ ~4.800).

## 1. Kết luận chính: ngân hàng CHƯA nối vào phần Luyện tập của bài

- Phần "Luyện tập" của mỗi bài chỉ lấy câu từ **các đề gắn vào mục `luyen_tap` của bài** (`lesson_items.exam_ids` → `fetchExamsForPractice`, `app/lop-hoc/bai/page.tsx`, `services/lessons.ts`). Mỗi bài thường chỉ có **1 đề**, 5–210 câu.
- `question_bank` là bản **sao tổng hợp từ đề** (`sync_exam_to_bank`), chiều ngược lại không có: câu nạp vào ngân hàng (thi thử, VnTeach, Word…) không tự chảy vào Luyện tập. Chỗ duy nhất trang bài đọc ngân hàng là "Bài tương đương" (`get_similar_bank_questions`) dưới bài tập mẫu.
- Ví dụ **L12 Bài 1. Sự chuyển thể**: Luyện tập = 1 đề 32 câu (28 câu thuộc chủ đề "Nóng chảy…", 1 câu Celsius/Kelvin và 1 câu nhiệt nóng chảy riêng thuộc Bài 2–4). Ngân hàng có **568 câu** dưới 3 chủ đề của bài (Dễ 471 · TB 77 · Khó 19); chỉ 16 câu trong số đó nằm trong đề luyện tập, ~93 câu không rõ nguồn đề, còn lại đến từ ~60 đề thi thử.
- Toàn bộ 4 khối: ngân hàng theo chủ đề của bài ≈ 22.800 câu, đề luyện tập tổng ≈ 4.450 câu → **~88% (≈20.000 câu) ngân hàng nằm ngoài tầm học sinh khi luyện theo bài** (chỉ thấy khi vào thi thử/đề gắn tay).
- Khoảng trống phụ: **29 bài** "Bài tập về…/Thực hành/Mở đầu" không có chủ đề ngân hàng nào (bank = 0) dù có 5–112 câu luyện tập; **1.231 câu** chưa gắn chủ đề (909 chưa cả lớp); 28 mục "Kiểm tra…" không có luyện tập (đúng thiết kế).

## 2. Bảng tổng hợp theo khối

| Khối | Số bài | Câu luyện tập (đề gắn bài) | Ngân hàng theo chủ đề của bài | Chưa vào luyện tập | Bài chưa có chủ đề NH | Bài luyện tập <30 câu |
|---|--:|--:|--:|--:|--:|--:|
| Lớp 12 | 21 | 1448 | 9365 | 8671 | 4 | 3 |
| Lớp 11 | 26 | 1657 | 4681 | 3567 | 7 | 3 |
| Lớp 10 | 34 | 1108 | 8431 | 7627 | 11 | 18 |
| Lớp 9 | 17 | 239 | 281 | 181 | 7 | 12 |

## Lớp 12

| Bài | Luyện tập (câu) | Ngân hàng theo chủ đề | Dễ | TB | Khó | Trong đề luyện tập | Ngân hàng chưa dùng cho luyện tập |
|---|--:|--:|--:|--:|--:|--:|--:|
| Bài 1. Sự chuyển thể | 32 | 568 | 471 | 77 | 19 | 16 | 552 |
| Bài 2. Thang nhiệt độ | 47 | 537 | 358 | 131 | 47 | 0 | 537 |
| Bài 3. Nội năng. Định luật 1 của nhiệt động lực học | 75 | 577 | 359 | 179 | 39 | 0 | 577 |
| Bài 4. Thực hành đo nhiệt dung riêng, nhiệt nóng chảy r | 44 | 1073 | 464 | 403 | 206 | 0 | 1073 |
| Bài 5. Thuyết động học phân tử chất khí | 66 | 330 | 257 | 66 | 7 | 60 | 270 |
| Bài 6. Định luật Boyle. Định luật Charles | 97 | 976 | 437 | 367 | 172 | 78 | 898 |
| Bài 7. Phương trình trạng thái của khí lí tưởng | 104 | 647 | 220 | 270 | 157 | 81 | 566 |
| Bài 8. Áp suất - động năng của phân tử khí ⚠ luyện tập mỏng | 11 | 307 | 194 | 94 | 19 | 10 | 297 |
| Bài 9. Khái niệm từ trường | 37 | 345 | 249 | 80 | 16 | 24 | 321 |
| Bài 10. Lực từ. Cảm ứng từ | 66 | 628 | 282 | 240 | 106 | 52 | 576 |
| Bài 11. Thực hành đo độ lớn cảm ứng từ ⚠ chưa có chủ đề NH | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 12. Hiện tượng cảm ứng điện từ | 210 | 925 | 427 | 367 | 131 | 130 | 795 |
| Bài 13. Đại cương về dòng điện xoay chiều | 146 | 812 | 508 | 237 | 67 | 74 | 738 |
| Bài 14. Máy phát điện xoay chiều. Máy biến áp ⚠ chưa có chủ đề NH | 112 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 15. Một số ứng dụng của cảm ứng điện từ ⚠ chưa có chủ đề NH | 72 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 16. Điện từ trường. Mô hình sóng điện từ ⚠ chưa có chủ đề NH | 75 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 14. Hạt nhân và mô hình nguyên tử | 76 | 355 | 267 | 77 | 11 | 68 | 287 |
| Bài 15. Năng lượng liên kết hạt nhân | 59 | 248 | 144 | 95 | 9 | 45 | 203 |
| Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng  | 46 | 395 | 152 | 120 | 123 | 1 | 394 |
| Bài 17. Hiện tượng phóng xạ | 47 | 530 | 202 | 186 | 142 | 36 | 494 |
| Bài 18. An toàn phóng xạ ⚠ luyện tập mỏng | 21 | 112 | 95 | 13 | 4 | 19 | 93 |
| **Tổng** | **1448** | **9365** | **5086** | **3002** | **1275** | **694** | **8671** |

## Lớp 11

| Bài | Luyện tập (câu) | Ngân hàng theo chủ đề | Dễ | TB | Khó | Trong đề luyện tập | Ngân hàng chưa dùng cho luyện tập |
|---|--:|--:|--:|--:|--:|--:|--:|
| Bài 1. Dao động điều hoà ⚠ chưa có chủ đề NH | 89 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 2. Mô tả dao động điều hoà | 35 | 760 | 481 | 205 | 72 | 29 | 731 |
| Bài 3. Vận tốc, gia tốc trong dao động điều hoà | 103 | 313 | 177 | 112 | 24 | 59 | 254 |
| Bài 4. Bài tập về dao động điều hoà ⚠ chưa có chủ đề NH | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 5. Động năng. Thế năng. Sự chuyển hoá giữa động năn | 108 | 363 | 134 | 161 | 68 | 77 | 286 |
| Bài 6. Dao động tắt dần. Dao động cưỡng bức. Hiện tượng | 63 | 320 | 205 | 94 | 21 | 54 | 266 |
| Bài 7. Bài tập về sự chuyển hoá năng lượng trong dao độ ⚠ chưa có chủ đề NH | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 8. Mô tả sóng | 39 | 358 | 187 | 118 | 53 | 35 | 323 |
| Bài 9. Sóng ngang, sóng dọc, sự truyền năng lượng của s | 100 | 104 | 94 | 10 | 0 | 12 | 92 |
| Bài 10. Thực hành: Đo tần số của sóng âm ⚠ chưa có chủ đề NH | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 11. Sóng điện từ | 92 | 215 | 165 | 47 | 3 | 82 | 133 |
| Bài 12. Giao thoa sóng | 119 | 314 | 154 | 111 | 49 | 110 | 204 |
| Bài 13. Sóng dừng | 64 | 195 | 90 | 71 | 34 | 55 | 140 |
| Bài 14. Bài tập về sóng ⚠ chưa có chủ đề NH | 67 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 15. Thực hành: Đo tốc độ truyền âm | 30 | 77 | 40 | 31 | 6 | 28 | 49 |
| Bài 16. Lực tương tác giữa hai điện tích | 77 | 227 | 126 | 80 | 21 | 75 | 152 |
| Bài 17. Khái niệm điện trường | 88 | 227 | 143 | 63 | 21 | 86 | 141 |
| Bài 18. Điện trường đều | 50 | 140 | 58 | 53 | 29 | 37 | 103 |
| Bài 19. Thế năng điện ⚠ chưa có chủ đề NH | 51 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 20. Điện thế | 73 | 315 | 215 | 84 | 16 | 63 | 252 |
| Bài 21. Tụ điện | 86 | 209 | 131 | 73 | 5 | 70 | 139 |
| Bài 22. Cường độ dòng điện | 51 | 113 | 80 | 27 | 6 | 50 | 63 |
| Bài 23. Điện trở. Định luật Ohm | 72 | 129 | 89 | 35 | 5 | 68 | 61 |
| Bài 24. Nguồn điện | 67 | 193 | 106 | 66 | 21 | 65 | 128 |
| Bài 25. Năng lượng điện và công suất điện | 85 | 109 | 74 | 31 | 4 | 59 | 50 |
| Bài 26. Thực hành: Đo suất điện động và điện trở trong  ⚠ chưa có chủ đề NH | 33 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Tổng** | **1657** | **4681** | **2749** | **1472** | **458** | **1114** | **3567** |

## Lớp 10

| Bài | Luyện tập (câu) | Ngân hàng theo chủ đề | Dễ | TB | Khó | Trong đề luyện tập | Ngân hàng chưa dùng cho luyện tập |
|---|--:|--:|--:|--:|--:|--:|--:|
| Bài 1. Làm quen với Vật lí ⚠ chưa có chủ đề NH | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 2. Các quy tắc an toàn trong phòng thực hành Vật lí ⚠ luyện tập mỏng | 8 | 668 | 641 | 26 | 1 | 7 | 661 |
| Bài 3. Thực hành tính sai số trong phép đo. Ghi kết quả ⚠ luyện tập mỏng | 9 | 342 | 232 | 95 | 15 | 9 | 333 |
| Bài 4. Độ dịch chuyển và quãng đường đi được ⚠ chưa có chủ đề NH | 20 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 5. Tốc độ và vận tốc | 40 | 1100 | 737 | 327 | 36 | 35 | 1065 |
| Bài 6. Thực hành: Đo tốc độ của vật chuyển động ⚠ chưa có chủ đề NH | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 7. Đồ thị độ dịch chuyển - thời gian ⚠ luyện tập mỏng | 27 | 262 | 92 | 125 | 45 | 24 | 238 |
| Bài 8. Chuyển động biến đổi. Gia tốc ⚠ chưa có chủ đề NH | 38 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 9. Chuyển động thẳng biến đổi đều | 42 | 1054 | 705 | 278 | 71 | 41 | 1013 |
| Bài 10. Sự rơi tự do | 50 | 440 | 285 | 127 | 28 | 0 | 440 |
| Bài 11. Thực hành: Đo gia tốc rơi tự do ⚠ chưa có chủ đề NH | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 12. Chuyển động ném | 31 | 371 | 190 | 148 | 33 | 23 | 348 |
| Bài 13. Tổng hợp và phân tích lực. Cân bằng lực ⚠ luyện tập mỏng | 20 | 292 | 218 | 64 | 10 | 18 | 274 |
| Bài 14. Định luật 1 Newton ⚠ chưa có chủ đề NH | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 15. Định luật 2 Newton ⚠ luyện tập mỏng | 25 | 811 | 545 | 242 | 24 | 21 | 790 |
| Bài 16. Định luật 3 Newton ⚠ chưa có chủ đề NH | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 17. Trọng lực và lực căng ⚠ luyện tập mỏng | 6 | 225 | 189 | 32 | 4 | 6 | 219 |
| Bài 18. Lực ma sát ⚠ luyện tập mỏng | 20 | 392 | 266 | 99 | 27 | 19 | 373 |
| Bài 19. Lực cản và lực nâng ⚠ chưa có chủ đề NH | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 20. Một số ví dụ về cách giải các bài toán thuộc ph ⚠ chưa có chủ đề NH | 7 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 21. Moment lực. Cân bằng của vật rắn ⚠ luyện tập mỏng | 15 | 242 | 181 | 53 | 8 | 14 | 228 |
| Bài 22. Thực hành: Tổng hợp lực ⚠ chưa có chủ đề NH | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 23. Năng lượng. Công cơ học | 64 | 340 | 234 | 89 | 17 | 61 | 279 |
| Bài 24. Công suất | 44 | 214 | 160 | 44 | 10 | 43 | 171 |
| Bài 25. Động năng, thế năng | 83 | 298 | 212 | 80 | 6 | 75 | 223 |
| Bài 26. Cơ năng và định luật bảo toàn cơ năng | 37 | 185 | 105 | 74 | 6 | 34 | 151 |
| Bài 27. Hiệu suất ⚠ luyện tập mỏng | 20 | 144 | 90 | 49 | 5 | 20 | 124 |
| Bài 28. Động lượng | 72 | 204 | 122 | 70 | 12 | 63 | 141 |
| Bài 29. Định luật bảo toàn động lượng | 57 | 162 | 104 | 34 | 24 | 24 | 138 |
| Bài 30. Thực hành: Xác định động lượng của vật trước và ⚠ chưa có chủ đề NH | 35 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 31. Động học của chuyển động tròn đều | 84 | 219 | 148 | 67 | 4 | 79 | 140 |
| Bài 32. Lực hướng tâm và gia tốc hướng tâm | 73 | 151 | 92 | 39 | 20 | 64 | 87 |
| Bài 33. Biến dạng của vật rắn | 62 | 143 | 109 | 29 | 5 | 56 | 87 |
| Bài 34. Khối lượng riêng. Áp suất chất lỏng | 75 | 172 | 122 | 42 | 8 | 68 | 104 |
| **Tổng** | **1108** | **8431** | **5779** | **2233** | **419** | **804** | **7627** |

## Lớp 9

| Bài | Luyện tập (câu) | Ngân hàng theo chủ đề | Dễ | TB | Khó | Trong đề luyện tập | Ngân hàng chưa dùng cho luyện tập |
|---|--:|--:|--:|--:|--:|--:|--:|
| Bài 1. Giới thiệu một số dụng cụ và hóa chất. Thuyết tr ⚠ chưa có chủ đề NH | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 2. Động năng. Thế năng ⚠ chưa có chủ đề NH | 39 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 3. Cơ năng ⚠ chưa có chủ đề NH | 36 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 4. Công và công suất ⚠ chưa có chủ đề NH | 57 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 5. Khúc xạ ánh sáng | 52 | 72 | 47 | 21 | 4 | 49 | 23 |
| Bài 6. Phản xạ toàn phần | 34 | 53 | 34 | 13 | 6 | 30 | 23 |
| Bài 7. Lăng kính ⚠ chưa có đề luyện tập | 0 | 22 | 14 | 7 | 1 | 0 | 22 |
| Bài 8. Thấu kính ⚠ chưa có đề luyện tập | 0 | 28 | 15 | 12 | 1 | 0 | 28 |
| Bài 9. Thực hành đo tiêu cự của thấu kính hội tụ ⚠ chưa có chủ đề NH | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 10. Kính lúp. Bài tập thấu kính ⚠ chưa có chủ đề NH | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 11. Điện trở. Định luật Ohm ⚠ luyện tập mỏng | 7 | 29 | 16 | 12 | 1 | 7 | 22 |
| Bài 12. Đoạn mạch nối tiếp, song song ⚠ luyện tập mỏng | 7 | 27 | 16 | 9 | 2 | 7 | 20 |
| Bài 13. Năng lượng của dòng điện và công suất điện ⚠ luyện tập mỏng | 7 | 27 | 15 | 10 | 2 | 7 | 20 |
| Bài 14. Cảm ứng điện từ. Nguyên tắc tạo ra dòng điện xo ⚠ chưa có đề luyện tập | 0 | 18 | 11 | 7 | 0 | 0 | 18 |
| Bài 15. Tác dụng của dòng điện xoay chiều ⚠ chưa có chủ đề NH | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Bài 16. Vòng năng lượng trên Trái Đất. Năng lượng hóa t ⚠ chưa có đề luyện tập | 0 | 2 | 1 | 1 | 0 | 0 | 2 |
| Bài 17. Một số dạng năng lượng tái tạo ⚠ chưa có đề luyện tập | 0 | 3 | 0 | 3 | 0 | 0 | 3 |
| **Tổng** | **239** | **281** | **169** | **95** | **17** | **100** | **181** |


## 3. Chất lượng (số đo hiện có)

| Chỉ số | Giá trị |
|---|---|
| Có lời giải | ~99,7% (24.4k/24.5k) |
| Phân bố mức độ | Dễ 57% · TB 31% · Khó 12% (L10: Khó 5%; L12: Khó 13%) |
| Cảnh báo lint đang tồn | 1 câu |
| Không rõ nguồn đề | L10 1.008 · L12 347 · chưa lớp 48 |
| Dạng | Phần I (trắc nghiệm) 17,4k · Đúng/Sai 3,2k · Trả lời ngắn 4,1k |
| Chờ thầy duyệt (STATE) | 127 câu đáp án cần xác nhận; 556+100 câu sai DB; viet-lai13/14/15/lech (~850 câu) |

Chưa đo (cần mẫu): độ đúng chủ đề — mỗi bài chỉ có 3–4 chủ đề rộng nên "thuộc chủ đề" chưa chắc "liên quan tới bài" (chủ đề "Nóng chảy, đông đặc, hoá hơi, ngưng tụ" 347 câu gánh cả Bài 2–4).

## 4. Đề xuất tiến trình nâng cấp

**Chặng 0 — nối ngân hàng vào Luyện tập (cần trước, 2–3 ngày, không ghi dữ liệu)**
- RPC gộp `lesson_practice_pool(lesson_id)`: đề gắn bài + câu ngân hàng theo chủ đề của bài (ẩn đáp án; chấm qua `check_practice_answer` mở rộng cho `question_bank`). Không thêm round-trip cho `/lop-hoc/bai`. Giao `kien-truc-du-lieu`; migration chỉ viết file.
- Khoá: loại câu có `lint_flags`, câu `_can_xac_nhan`, câu `archived`, đề đánh giá; ưu tiên đúng `question_dang`/YCCĐ khi có.
- Thang Dễ→TB→Khó (`practice-ladder.ts`) giữ nguyên; mỗi phiên trộn ~60% câu từ đề của bài + 40% từ ngân hàng, không lặp câu đã đúng.

**Chặng 1 — làm sạch độ liên quan (1 tuần, chạy ban đêm)**
- Lấy mẫu 30 câu/bài cho 10 bài thí điểm (L12 Bài 1–4, L11 Bài 1–3, L10 Bài 5–7), để `kiem-code`/subagent chấm "đúng bài / sang bài khác / ngoài chương trình" → ra tỉ lệ nhiễu và quyết định có cần tách chủ đề rộng thành chủ đề theo bài.
- Gán 1.231 câu chưa có chủ đề (script `backfill-question-bank-topics.mts`, dry-run → ghi sau 22h).
- Chủ đề cho 29 bài "Bài tập/Thực hành": ánh xạ về chủ đề của bài lý thuyết cha.

**Chặng 2 — số lượng (mục tiêu ≥150 câu/bài, gồm ≥25 Khó, đủ Phần I/II/III)**
- Còn thiếu để đủ 150/bài: L12 ≈ 640 · L11 ≈ 1.280 · L10 ≈ 1.660 (chủ yếu các bài chưa có chủ đề ở mục 2). Ưu tiên theo tải học: L12 (đang thi), L11 Chương 4 Dòng điện (Bài 22–25 dưới 150), L10 Chương 1, 3.
- Nguồn: nạp VnTeach L12 ch.1–4 và VL10 Ch.I, VII (đang chờ chọn đường); bài tập mẫu → "Bài tương đương"; sinh biến thể từ câu Khó thật (Claude/ngoài Claude theo phân công, lời giải ngoài phải được Claude đối chiếu).
- Tăng Khó: L10 5% → 15%, L11 10% → 18%, L12 13% → 20%; không phá thang Dễ bắt đầu (cảm giác thành thạo giảm bỏ cuộc).

**Chặng 3 — chất lượng bền vững**
- Xử lý hàng chờ duyệt (127 + 656 + ~850 câu) trước khi bật câu mới vào Luyện tập.
- Dedup sau mỗi mẻ nạp; kiểm nhãn như đề thật (E1–E3), hình ≤150 KB, một đáp án đúng.
- Đo (không cần thêm bảng): từ `practice_question_results` lấy tỉ lệ đúng theo câu — câu >95% hoặc <10% đúng sau ≥30 lượt bị gắn cờ xem lại; đếm số câu HS chạm/bài trước-sau chặng 0.

**Lưu ý nghiên cứu**: kho lớn hơn giúp truy hồi cách quãng và tránh học vẹt đáp án (đề 32 câu bị nhớ sau 1–2 lượt); rủi ro là câu thi thử khó/lệch bài làm HS đầu bài nản và tải nhận thức cao ở người mới → nên giữ thang Dễ→Khó và lọc theo chủ đề/YCCĐ trước khi mở rộng số lượng (chưa tra lại tài liệu nghiên cứu trong repo cho báo cáo này).

Cột "Trong đề luyện tập" = 0 ở nhiều bài (vd. L12 Bài 2–4) nghĩa là đề luyện tập của bài chưa được đồng bộ vào ngân hàng dưới chủ đề của bài đó — cần kiểm `sync_exam_to_bank` khi làm chặng 0.

Ghi chú phương pháp: lớp của bài suy từ mã bài (2–19, 125–127 → L12; 20–45 → L11; 46–82 → L10; 83–95, 128–131 → L9); "Luyện tập" = tổng `question_count` đề đã xuất bản gắn mục `luyen_tap`; "Ngân hàng" = câu chưa lưu trữ thuộc chủ đề có `lesson_id` của bài.
