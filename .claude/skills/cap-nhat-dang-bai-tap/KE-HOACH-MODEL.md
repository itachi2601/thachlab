# Phân loại 492 dạng bài tập mẫu → giải cùng hình

Ràng buộc: mỗi bài chọn tối đa 2 dạng "giải cùng hình" (ưu tiên dạng mẫu đầu của họ, rồi dạng khó nhất có hình mang lập luận); dạng còn lại chỉ tóm đề (Sonnet), kể cả khi vẽ được.

Ký hiệu: D = Dạng, B = Bài (id 167). Ưu tiên P1 = L12/L11, P2 = L10, P3 = KHTN9/HSG9, P4 = bài chỉ tóm đề.

## A. Họ hình

| Họ hình | Mô tả component | Dạng mẫu đầu (Opus) | Số dạng dùng lại (Sonnet) | Bài/chương phủ |
|---|---|---|---|---|
| `do_thi` (`DoThi.tsx`, Đ2 ✓) | Đồ thị trên lưới (đoạn thẳng + đường cong hàm, tô diện tích, tam giác độ dốc, điểm đánh dấu): x–t, v–t, T–t chuyển thể, T–Q, p–V/V–T/p–T, U–I, Φ–t, N(t), x–t dao động, W–x, W–t, A–f cộng hưởng, P(R) | 2 · D4 | 30 | 2, 3, 7, 8, 13, 18, 20, 21, 22, 23, 24, 25, 26, 42, 52, 53, 54, 89, 150, 153, 159, 160, 162, 166 · H9 Cơ; H9 Nhiệt; H9 Âm; H9 Điện; K9 Ch.3; L10 Ch.2; L11 Ch.1; L11 Ch.4; L12 Ch.1; L12 Ch.2; L12 Ch.3; L12 Ch.4 |
| `tu_truong` (`TuTruong.tsx`, Đ2 ✓) | Nền B (mũi/chấm/chéo), nam châm, dây thẳng + đường sức tròn, la bàn, vectơ F (bàn tay trái), khung dây + pháp tuyến n, từ thông, Lenz | 11 · D4 | 6 | 10, 11, 13, 14, 126 · L12 Ch.3 |
| `vong_tron` (`VongTronPha.tsx`, Đ1 ✓) | Đường tròn: điểm quay + góc quét + chiếu lên trục x; vectơ v tiếp tuyến, a hướng tâm — vòng tròn pha (dao động, i/u xoay chiều, E–B) và chuyển động tròn đều | 23 · D4 | 9 | 14, 20, 21, 22, 23, 76, 77, 127 · L10 Ch.6; L11 Ch.1; L12 Ch.3 |
| `thanh_nang_luong` (`ThanhNangLuong.tsx`, Đ2 ✓) | Cảnh (độ cao, dốc, con lắc, lò xo) + cột Wđ/Wt/Q; hộp hệ với mũi tên Q, A vào/ra (dấu ĐL1 NĐLH); chuỗi khâu hiệu suất | 26 · D2 | 14 | 4, 24, 26, 70, 71, 72, 129, 130, 163, 166, 167 · H9 Cơ; H9 Điện; K9 Ch.1; L10 Ch.4; L11 Ch.1; L12 Ch.1 |
| `song_day` (`SongDay.tsx`, Đ1 ✓) | Dây/ống: u–x sóng chạy (chiều truyền, chiều chuyển động phần tử, Δφ hai điểm), sóng dọc nén–dãn, sóng dừng bụng–nút, ống một đầu kín | 27 · D4 | 6 | 27, 28, 32, 34 · L11 Ch.2 |
| `giao_thoa_2_nguon` | Hai nguồn trên mặt nước, vân cực đại/cực tiểu (đã có) | 33 · D3 (đã có) | 1 | 31, 33 · L11 Ch.2 |
| `van_giao_thoa` (`VanGiaoThoa.tsx`, Đ1 ✓) | Màn khe Young: thước vân sáng/tối, khoảng vân, trùng vân hai bức xạ | 31 · D4 | 1 | 31, 33 · L11 Ch.2 |
| `dien_truong_deu` (`DienTruongDeu.tsx`, Đ3 ✓) | Hai bản song song: đường sức, điểm M/N, hình chiếu d, điện thế, quỹ đạo hạt bay vào, tụ phẳng đổi d | 37 · D3 | 6 | 37, 38, 39, 40 · L11 Ch.3 |
| `mach_dien` (`MachDien.tsx`, Đ3 ✓) | Sơ đồ mạch: nguồn (E,r), R nối tiếp/song song/cầu, biến trở, khoá, ampe/vôn kế, đèn, tụ ghép, đường dây truyền tải | 43 · D3 | 16 | 40, 43, 44, 90, 91, 125, 152, 157, 159, 165 · H9 Điện; K9 Ch.3; L11 Ch.3; L11 Ch.4; L12 Ch.3 |
| `truc_chuyen_dong` | Trục toạ độ 1D: vị trí theo thời điểm, đi–quay lại, hai vật gặp/đuổi, vật có chiều dài (tàu, cầu), xuôi–ngược dòng, tiếng vang; va chạm/súng giật trước–sau (mũi tên v, p) | 50 · D3 | 5 | 50, 54, 73, 74, 150 · H9 Âm; L10 Ch.2; L10 Ch.5 |
| `so_do_vecto` (`SoDoVecto.tsx`, ✓ 3/11) | Vectơ đồng quy + phân tích/hình bình hành trên nền: mặt ngang, mặt nghiêng, dây treo, ròng rọc/palăng, lò xo + thước; cũng dùng cho cộng vận tốc, độ dịch chuyển 2D, Δv, động lượng theo góc, lực Coulomb/E tổng hợp | 63 · D4 | 26 | 35, 36, 49, 50, 53, 58, 60, 62, 63, 68, 69, 70, 73, 78, 155, 161, 162 · H9 Cơ; L10 Ch.2; L10 Ch.3; L10 Ch.4; L10 Ch.5; L10 Ch.7; L11 Ch.3 |
| `quy_dao_nem` | Mặt phẳng đứng: rơi tự do (chấm theo từng giây), ném ngang/xiên/đứng, tách vx–vy, vectơ v chạm đất | 57 · D4 | 3 | 55, 57 · L10 Ch.2 |
| `thanh_moment` (`SoDoVecto.tsx` cảnh `thanh`, ✓ 3/11) | Thanh cứng + điểm tựa/bản lề/giá đỡ, lực, cánh tay đòn, ngẫu lực, đòn bẩy, ròng rọc cố định | 66 · D4 | 3 | 66, 154, 155 · H9 Cơ; L10 Ch.3 |
| `cot_chat_long` | Bình/ống chất lỏng: áp suất theo độ sâu, bình thông nhau nhiều chất lỏng, pittông, vật nổi/chìm (Archimedes), mực nước dâng, cột thuỷ ngân giam khí | 79 · D4 | 4 | 7, 79, 154, 167 · H9 Cơ; L10 Ch.7; L12 Ch.2 |
| `tia_sang` (`TiaSang.tsx`, Đ5 ✓) | Dò tia: mặt phân cách (khúc xạ, phản xạ, toàn phần, góc tới hạn), bản mặt, lăng kính, sợi quang, gương phẳng, nguồn rộng + vật chắn (bóng tối/nửa tối, nhật–nguyệt thực), tia song song (Eratosthenes) | 83 · D4 | 9 | 83, 84, 151, 158, 178 · H9 Quang; H9 Âm; K9 Ch.2 |
| `thau_kinh` (`ThauKinh.tsx`, Đ5 ✓) | Trục chính + thấu kính hội tụ/phân kì, F/F′, 3 tia đặc biệt, ảnh thật/ảo, hệ 2 thấu kính, kính lúp | 156 · D1 | 1 | 156 · H9 Quang |

## B. Theo bài


### Lớp 12 · Ch.1 Vật lí nhiệt

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 2 | Bài 1. Sự chuyển thể | ✓ D4 (do_thi) 3/11 | ✓ D5 (do_thi) 3/11 | ✓ D1, D2, D3 3/11 | Opus | P1 |
| 3 | Bài 2. Thang nhiệt độ | — | D6 (do_thi) | D1, D2, D3, D4, D5 | Sonnet | P1 |
| 4 | Bài 3. Nội năng. Định luật 1 của nhiệt động lực học | — | D4 (thanh_nang_luong), D5 (thanh_nang_luong) | D1, D2, D3 | Sonnet | P1 |

### Lớp 12 · Ch.2 Khí lí tưởng

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 6 | Bài 5. Thuyết động học phân tử chất khí | — | — | D1, D2, D3, D4, D5 | Sonnet | P4 |
| 7 | Bài 6. Định luật Boyle. Định luật Charles | — | D4 (do_thi), D5 (cot_chat_long) | D1, D2, D3 | Sonnet | P1 |
| 8 | Bài 7. Phương trình trạng thái của khí lí tưởng | — | D3 (do_thi) | D1, D2, D4, D5 | Sonnet | P1 |
| 9 | Bài 8. Áp suất - động năng của phân tử khí | — | — | D1, D2, D3, D4, D5 | Sonnet | P4 |

### Lớp 12 · Ch.3 Từ trường

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 10 | Bài 9. Khái niệm từ trường | — | D3 (tu_truong), D4 (tu_truong) | D1, D2 | Sonnet | P1 |
| 11 | Bài 10. Lực từ. Cảm ứng từ | ✓ D4 (tu_truong) 3/11 | ✓ D5 (tu_truong) 3/11 | ✓ D1, D2, D3 3/11 | Opus | P1 |
| 13 | Bài 12. Hiện tượng cảm ứng điện từ | — | D4 (tu_truong), D5 (do_thi) | D1, D2, D3 | Sonnet | P1 |
| 14 | Bài 13. Đại cương về dòng điện xoay chiều | — | D4 (tu_truong), D5 (vong_tron) | D1, D2, D3 | Sonnet | P1 |
| 125 | Bài 14. Máy phát điện xoay chiều. Máy biến áp | — | D4 (mach_dien), D5 (mach_dien) | D1, D2, D3 | Sonnet | P1 |
| 126 | Bài 15. Một số ứng dụng của cảm ứng điện từ | — | D1 (tu_truong) | D2, D3, D4 | Sonnet | P1 |
| 127 | Bài 16. Điện từ trường. Mô hình sóng điện từ | — | D6 (vong_tron) | D1, D2, D3, D4, D5 | Sonnet | P1 |

### Lớp 12 · Ch.4 Vật lí hạt nhân

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 15 | Bài 14. Hạt nhân và mô hình nguyên tử | — | — | D1, D2, D3, D4, D5 | Sonnet | P4 |
| 16 | Bài 15. Năng lượng liên kết hạt nhân | — | — | D1, D2, D3, D4, D5, D6 | Sonnet | P4 |
| 17 | Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng | — | — | D1, D2, D3, D4, D5 | Sonnet | P4 |
| 18 | Bài 17. Hiện tượng phóng xạ | — | D3 (do_thi), D5 (do_thi) | D1, D2, D4 | Sonnet | P1 |
| 19 | Bài 18. An toàn phóng xạ | — | — | D1, D2, D3, D4, D5, D6 | Sonnet | P4 |

### Lớp 11 · Ch.1 Dao động

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 20 | Bài 1. Dao động điều hoà | — | D3 (do_thi), D5 (vong_tron) | D1, D2, D4 | Sonnet | P1 |
| 21 | Bài 2. Mô tả dao động điều hoà | — | D4 (do_thi), D5 (vong_tron) | D1, D2, D3 | Sonnet | P1 |
| 22 | Bài 3. Vận tốc, gia tốc trong dao động điều hoà | — | D3 (do_thi), D4 (vong_tron) | D1, D2, D5 | Sonnet | P1 |
| 23 | Bài 4. Bài tập về dao động điều hoà | ✓ D4 (vong_tron) 3/11 | D3 (do_thi) — chờ Đ2 | ✓ D1, D2, D3, D5 3/11 | Opus | P1 |
| 24 | Bài 5. Động năng. Thế năng. Sự chuyển hoá giữa động năng và | — | D2 (thanh_nang_luong), D5 (do_thi) | D1, D3, D4 | Sonnet | P1 |
| 25 | Bài 6. Dao động tắt dần. Dao động cưỡng bức. Hiện tượng cộng | — | D2 (do_thi), D3 (do_thi) | D1, D4, D5 | Sonnet | P1 |
| 26 | Bài 7. Bài tập về sự chuyển hoá năng lượng trong dao động đi | ✓ D2 (thanh_nang_luong) 3/11 | ✓ D5 (do_thi) 3/11 | ✓ D1, D3, D4 3/11 | Opus | P1 |

### Lớp 11 · Ch.2 Sóng

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 27 | Bài 8. Mô tả sóng | ✓ D4 (song_day) 3/11 | ✓ D5 (song_day) 3/11 | ✓ D1, D2, D3 3/11 | Opus | P1 |
| 28 | Bài 9. Sóng ngang, sóng dọc, sự truyền năng lượng của sóng c | — | D3 (song_day) | D1, D2, D4, D5, D6 | Sonnet | P1 |
| 30 | Bài 11. Sóng điện từ | — | — | D1, D2, D3, D4 | Sonnet | P4 |
| 31 | Bài 12. Giao thoa sóng | ✓ D4 (van_giao_thoa) 3/11 | ✓ D3 (giao_thoa_2_nguon `kieu: dem_day`) 3/11 | ✓ D1, D2, D5 3/11 | Opus | P1 |
| 32 | Bài 13. Sóng dừng | — | D5 (song_day), D6 (song_day) | D1, D2, D3, D4 | Sonnet | P1 |
| 33 | Bài 14. Bài tập về sóng | — | D3 (giao_thoa_2_nguon, đã làm), D4 (van_giao_thoa) | D1, D2, D5, D6 | Sonnet | P1 |
| 34 | Bài 15. Thực hành: Đo tốc độ truyền âm | — | D2 (song_day), D3 (song_day) | D1, D4 | Sonnet | P1 |

### Lớp 11 · Ch.3 Điện trường

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 35 | Bài 16. Lực tương tác giữa hai điện tích | — | D4 (so_do_vecto), D5 (so_do_vecto) | D1, D2, D3 | Sonnet | P1 |
| 36 | Bài 17. Khái niệm điện trường | — | D4 (so_do_vecto), D5 (so_do_vecto) | D1, D2, D3 | Sonnet | P1 |
| 37 | Bài 18. Điện trường đều | ✓ D3 (dien_truong_deu) 3/11 | ✓ D5 (dien_truong_deu) 3/11 | ✓ D1, D2, D4 3/11 | Opus | P1 |
| 38 | Bài 19. Thế năng điện | — | D3 (dien_truong_deu), D4 (dien_truong_deu) | D1, D2 | Sonnet | P1 |
| 39 | Bài 20. Điện thế | — | D4 (dien_truong_deu), D5 (dien_truong_deu) | D1, D2, D3 | Sonnet | P1 |
| 40 | Bài 21. Tụ điện | — | D4 (mach_dien), D5 (dien_truong_deu) | D1, D2, D3 | Sonnet | P1 |

### Lớp 11 · Ch.4 Dòng điện, mạch điện

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 41 | Bài 22. Cường độ dòng điện | — | — | D1, D2, D3, D4, D5 | Sonnet | P4 |
| 42 | Bài 23. Điện trở. Định luật Ohm | — | D2 (do_thi), D3 (do_thi) | D1, D4, D5 | Sonnet | P1 |
| 43 | Bài 24. Nguồn điện | ✓ D3 (mach_dien) 3/11 | ✓ D4 (mach_dien) 3/11 | ✓ D1, D2 3/11 | Opus | P1 |
| 44 | Bài 25. Năng lượng điện và công suất điện | — | D4 (mach_dien), D5 (mach_dien) | D1, D2, D3 | Sonnet | P1 |

### Lớp 10 · Ch.2 Động học

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 49 | Bài 4. Độ dịch chuyển và quãng đường đi được | — | D3 (so_do_vecto), D5 (so_do_vecto) | D1, D2, D4 | Sonnet | P2 |
| 50 | Bài 5. Tốc độ và vận tốc | ✓ D3 (truc_chuyen_dong) 3/11 | ✓ D6 (so_do_vecto, cảnh `song`) 3/11 | ✓ D1, D2, D4, D5 3/11* | Opus | P2 |
| 52 | Bài 7. Đồ thị độ dịch chuyển - thời gian | — | D3 (do_thi), D4 (do_thi) | D1, D2 | Sonnet | P2 |
| 53 | Bài 8. Chuyển động biến đổi. Gia tốc | — | D4 (do_thi), D5 (so_do_vecto) | D1, D2, D3 | Sonnet | P2 |
| 54 | Bài 9. Chuyển động thẳng biến đổi đều | — | D5 (do_thi), D6 (truc_chuyen_dong) | D1, D2, D3, D4 | Sonnet | P2 |
| 55 | Bài 10. Sự rơi tự do | — | D4 (quy_dao_nem), D5 (quy_dao_nem) | D1, D2, D3 | Sonnet | P2 |
| 57 | Chuyển động ném | ✓ D4 (quy_dao_nem) 3/11 | ✓ D6 (quy_dao_nem) 3/11 | ✓ D1, D2, D3, D5 3/11* | Opus | P2 |

### Lớp 10 · Ch.3 Động lực học

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 58 | Bài 13. Tổng hợp và phân tích lực. Cân bằng lực | — | ✓ D5 (so_do_vecto), D6 (so_do_vecto) 3/11 | ✓ D1, D2, D3, D4 3/11* | Sonnet | P2 |
| 60 | Bài 15. Định luật 2 Newton | — | ✓ D2 (so_do_vecto), D4 (so_do_vecto) 3/11 | ✓ D1, D3, D5, D6 3/11* | Sonnet | P2 |
| 62 | Bài 17. Trọng lực và lực căng | — | ✓ D4 (so_do_vecto), D5 (so_do_vecto) 3/11 | ✓ D1, D2, D3 3/11* | Sonnet | P2 |
| 63 | Bài 18. Lực ma sát | ✓ D4 (so_do_vecto) 3/11 | ✓ D5 (so_do_vecto) 3/11 | ✓ D1, D2, D3 3/11* | Opus | P2 |
| 66 | Bài 21. Moment lực. Cân bằng của vật rắn | ✓ D4 (thanh_moment) 3/11 | ✓ D5 (thanh_moment) 3/11 | ✓ D1, D2, D3 3/11* | Opus | P2 |

\* Tóm đề đã ghi vào JSON nhưng dạng không có `cong_cu` đi qua `StepwiseSolution`, chưa hiện `tom_de` (3/11) — cần sửa UI trước khi đăng mới có tác dụng.

### Lớp 10 · Ch.4 Năng lượng, công, công suất

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 68 | Bài 23. Năng lượng. Công cơ học | — | D4 (so_do_vecto), D5 (so_do_vecto) | D1, D2, D3 | Sonnet | P2 |
| 69 | Bài 24. Công suất | — | D5 (so_do_vecto) | D1, D2, D3, D4 | Sonnet | P2 |
| 70 | Bài 25. Động năng, thế năng | — | D4 (thanh_nang_luong), D5 (so_do_vecto) | D1, D2, D3 | Sonnet | P2 |
| 71 | Bài 26. Cơ năng và định luật bảo toàn cơ năng | — | D4 (thanh_nang_luong), D5 (thanh_nang_luong) | D1, D2, D3 | Sonnet | P2 |
| 72 | Bài 27. Hiệu suất | — | D5 (thanh_nang_luong) | D1, D2, D3, D4 | Sonnet | P2 |

### Lớp 10 · Ch.5 Động lượng

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 73 | Bài 28. Động lượng | — | D3 (so_do_vecto), D5 (truc_chuyen_dong) | D1, D2, D4 | Sonnet | P2 |
| 74 | Bài 29. Định luật bảo toàn động lượng | — | D4 (truc_chuyen_dong), D5 (truc_chuyen_dong) | D1, D2, D3 | Sonnet | P2 |

### Lớp 10 · Ch.6 Chuyển động tròn

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 76 | Bài 31. Động học của chuyển động tròn đều | — | D4 (vong_tron), D5 (vong_tron) | D1, D2, D3 | Sonnet | P2 |
| 77 | Bài 32. Lực hướng tâm và gia tốc hướng tâm | — | D4 (vong_tron), D5 (vong_tron) | D1, D2, D3 | Sonnet | P2 |

### Lớp 10 · Ch.7 Biến dạng vật rắn. Áp suất chất lỏng

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 78 | Bài 33. Biến dạng của vật rắn | — | D4 (so_do_vecto), D5 (so_do_vecto) | D1, D2, D3 | Sonnet | P2 |
| 79 | Bài 34. Khối lượng riêng. Áp suất chất lỏng | ✓ D4 (cot_chat_long) 3/11 | ✓ D5 (cot_chat_long) 3/11 | ✓ D1, D2, D3 3/11* | Opus | P2 |

### KHTN 9 · Ch.1 Năng lượng cơ học

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 129 | Bài 2. Động năng. Thế năng | — | D3 (thanh_nang_luong), D4 (thanh_nang_luong) | D1, D2 | Sonnet | P3 |
| 130 | Bài 3. Cơ năng | — | D3 (thanh_nang_luong), D4 (thanh_nang_luong) | D1, D2 | Sonnet | P3 |
| 131 | Bài 4. Công và công suất | — | — | D1, D2, D3, D4 | Sonnet | P4 |

### KHTN 9 · Ch.2 Ánh sáng

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 83 | Bài 5. Khúc xạ ánh sáng | ✓ D4 (tia_sang) 4/11 | ✓ D5 (tia_sang) 4/11 | ✓ D1, D2, D3 4/11* | Opus | P3 |
| 84 | Bài 6. Phản xạ toàn phần | — | D2 (tia_sang), D4 (tia_sang) | D1, D3 | Sonnet | P3 |

### KHTN 9 · Ch.3 Điện

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 89 | Bài 11. Điện trở. Định luật Ohm | — | D2 (do_thi) | D1, D3, D4 | Sonnet | P3 |
| 90 | Bài 12. Đoạn mạch nối tiếp, song song | — | D3 (mach_dien), D4 (mach_dien) | D1, D2 | Sonnet | P3 |
| 91 | Bài 13. Năng lượng của dòng điện và công suất điện | — | D3 (mach_dien) | D1, D2, D4 | Sonnet | P3 |

### HSG KHTN 9 · Cơ học

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 160 | Chuyên đề 00. Kỹ năng nền: công cụ toán học, đọc đồ thị, sai | — | D3 (do_thi), D4 (do_thi) | D1, D2, D5, D6 | Sonnet | P3 |
| 162 | Chuyên đề 13. Chuyển động cơ học và đồ thị chuyển động | — | D5 (do_thi), D6 (so_do_vecto) | D1, D2, D3, D4 | Sonnet | P3 |
| 155 | Chuyên đề 10. Lực: tổng hợp lực, cân bằng, ma sát, đòn bẩy | — | D5 (thanh_moment), D6 (so_do_vecto) | D1, D2, D3, D4 | Sonnet | P3 |
| 161 | Chuyên đề 01. Công và công suất | — | D5 (so_do_vecto), D7 (so_do_vecto) | D1, D2, D3, D4, D6 | Sonnet | P3 |
| 166 | Chuyên đề 02. Động năng, thế năng, cơ năng và định luật bảo | — | D6 (do_thi), D7 (thanh_nang_luong) | D1, D2, D3, D4, D5 | Sonnet | P3 |
| 154 | Chuyên đề 11. Cơ học chất lưu: áp suất chất lỏng, bình thông | — | D5 (cot_chat_long), D6 (thanh_moment) | D1, D2, D3, D4 | Sonnet | P3 |
| 167 | Bài tập tuần này: 12 bài tự luận Cơ học (Vận dụng → Vận dụng | — | B9 (cot_chat_long), B11 (thanh_nang_luong) | B1, B2, B3, B4, B5, B6, B7, B8, B10, B12 | Sonnet | P3 |

### HSG KHTN 9 · Nhiệt học

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 153 | Chuyên đề 12. Nhiệt học nâng cao: cân bằng nhiệt và chuyển t | — | D2 (do_thi), D3 (do_thi) | D1, D4, D5, D6 | Sonnet | P3 |
| 164 | Chuyên đề 16. Truyền nhiệt và sự nở vì nhiệt | — | — | D1, D2, D3, D4, D5, D6 | Sonnet | P4 |

### HSG KHTN 9 · Điện học & năng lượng

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 159 | Chuyên đề 03. Điện trở và định luật Ohm | — | D4 (do_thi), D6 (mach_dien) | D1, D2, D3, D5 | Sonnet | P3 |
| 157 | Chuyên đề 04. Đoạn mạch nối tiếp, song song, hỗn hợp | — | D5 (mach_dien), D6 (mach_dien) | D1, D2, D3, D4 | Sonnet | P3 |
| 165 | Chuyên đề 05. Công suất điện, định luật Joule–Lenz | — | D5 (mach_dien), D6 (mach_dien) | D1, D2, D3, D4 | Sonnet | P3 |
| 152 | Chuyên đề 08. Cảm ứng điện từ và dòng điện xoay chiều | — | D5 (mach_dien), D6 (mach_dien) | D1, D2, D3, D4 | Sonnet | P3 |
| 163 | Chuyên đề 09. Năng lượng với cuộc sống: vòng năng lượng Trái | — | D1 (thanh_nang_luong) | D2, D3, D4, D5 | Sonnet | P3 |

### HSG KHTN 9 · Quang học

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 151 | Chuyên đề 06. Khúc xạ ánh sáng, phản xạ toàn phần, lăng kính | — | D6 (tia_sang), D7 (tia_sang) | D1, D2, D3, D4, D5 | Sonnet | P3 |
| 156 | Chuyên đề 07. Thấu kính mỏng và kính lúp | ✓ D1 (thau_kinh) 4/11 | ✓ D7 (thau_kinh) 4/11 | ✓ D2, D3, D4, D5, D6 4/11* | Opus | P3 |
| 158 | Chuyên đề 14. Gương phẳng, bóng tối và nửa tối | — | D6 (tia_sang), D7 (tia_sang) | D1, D2, D3, D4, D5 | Sonnet | P3 |

### HSG KHTN 9 · Âm học & thiên văn

| id | Bài | Dạng Opus | Dạng Sonnet có hình | Dạng chỉ tóm đề | Model phiên | Ưu tiên |
|---|---|---|---|---|---|---|
| 150 | Chuyên đề 15. Âm thanh: sóng âm, độ cao, độ to, phản xạ âm | — | D2 (do_thi), D5 (truc_chuyen_dong) | D1, D3, D4, D6 | Sonnet | P3 |
| 178 | Chuyên đề 17. Thiên văn: Mặt Trăng, Hệ Mặt Trời và Ngân Hà | — | D3 (tia_sang), D5 (tia_sang) | D1, D2, D4, D6 | Sonnet | P3 |

## C. Tổng theo chương

| Lớp · Chương | Bài (id) | Model phiên | Ghi chú |
|---|---|---|---|
| Lớp 12 · Ch.1 Vật lí nhiệt | 2, 3, 4 | Opus (2), còn lại Sonnet | 5 dạng có hình (do_thi, thanh_nang_luong); 11 chỉ tóm đề |
| Lớp 12 · Ch.2 Khí lí tưởng | 6, 7, 8, 9 | Sonnet | 3 dạng có hình (cot_chat_long, do_thi); 17 chỉ tóm đề |
| Lớp 12 · Ch.3 Từ trường | 10, 11, 13, 14, 125, 126, 127 | Opus (11), còn lại Sonnet | 12 dạng có hình (do_thi, mach_dien, tu_truong, vong_tron); 22 chỉ tóm đề |
| Lớp 12 · Ch.4 Vật lí hạt nhân | 15, 16, 17, 18, 19 | Sonnet | 2 dạng có hình (do_thi); 25 chỉ tóm đề |
| Lớp 11 · Ch.1 Dao động | 20, 21, 22, 23, 24, 25, 26 | Opus (23, 26), còn lại Sonnet | 14 dạng có hình (do_thi, thanh_nang_luong, vong_tron); 21 chỉ tóm đề |
| Lớp 11 · Ch.2 Sóng | 27, 28, 30, 31, 32, 33, 34 | Opus (27, 31), còn lại Sonnet | 11 dạng có hình (giao_thoa_2_nguon, song_day, van_giao_thoa); 25 chỉ tóm đề |
| Lớp 11 · Ch.3 Điện trường | 35, 36, 37, 38, 39, 40 | Opus (37), còn lại Sonnet | 12 dạng có hình (dien_truong_deu, mach_dien, so_do_vecto); 17 chỉ tóm đề |
| Lớp 11 · Ch.4 Dòng điện, mạch điện | 41, 42, 43, 44 | Opus (43), còn lại Sonnet | 6 dạng có hình (do_thi, mach_dien); 13 chỉ tóm đề |
| Lớp 10 · Ch.2 Động học | 49, 50, 52, 53, 54, 55, 57 | Opus (50, 57), còn lại Sonnet | 14 dạng có hình (do_thi, quy_dao_nem, so_do_vecto, truc_chuyen_dong); 23 chỉ tóm đề |
| Lớp 10 · Ch.3 Động lực học | 58, 60, 62, 63, 66 | Opus (63, 66), còn lại Sonnet | 10 dạng có hình (so_do_vecto, thanh_moment); 17 chỉ tóm đề |
| Lớp 10 · Ch.4 Năng lượng, công, công suất | 68, 69, 70, 71, 72 | Sonnet | 8 dạng có hình (so_do_vecto, thanh_nang_luong); 17 chỉ tóm đề |
| Lớp 10 · Ch.5 Động lượng | 73, 74 | Sonnet | 4 dạng có hình (so_do_vecto, truc_chuyen_dong); 6 chỉ tóm đề |
| Lớp 10 · Ch.6 Chuyển động tròn | 76, 77 | Sonnet | 4 dạng có hình (vong_tron); 6 chỉ tóm đề |
| Lớp 10 · Ch.7 Biến dạng vật rắn. Áp suất chất lỏng | 78, 79 | Opus (79), còn lại Sonnet | 4 dạng có hình (cot_chat_long, so_do_vecto); 6 chỉ tóm đề |
| KHTN 9 · Ch.1 Năng lượng cơ học | 129, 130, 131 | Sonnet | 4 dạng có hình (thanh_nang_luong); 8 chỉ tóm đề |
| KHTN 9 · Ch.2 Ánh sáng | 83, 84 | Opus (83), còn lại Sonnet | 4 dạng có hình (tia_sang); 5 chỉ tóm đề |
| KHTN 9 · Ch.3 Điện | 89, 90, 91 | Sonnet | 4 dạng có hình (do_thi, mach_dien); 8 chỉ tóm đề |
| HSG KHTN 9 · Cơ học | 160, 162, 155, 161, 166, 154, 167 | Sonnet | 14 dạng có hình (cot_chat_long, do_thi, so_do_vecto, thanh_moment, thanh_nang_luong); 36 chỉ tóm đề |
| HSG KHTN 9 · Nhiệt học | 153, 164 | Sonnet | 2 dạng có hình (do_thi); 10 chỉ tóm đề |
| HSG KHTN 9 · Điện học & năng lượng | 159, 157, 165, 152, 163 | Sonnet | 9 dạng có hình (do_thi, mach_dien, thanh_nang_luong); 20 chỉ tóm đề |
| HSG KHTN 9 · Quang học | 151, 156, 158 | Opus (156), còn lại Sonnet | 6 dạng có hình (thau_kinh, tia_sang); 15 chỉ tóm đề |
| HSG KHTN 9 · Âm học & thiên văn | 150, 178 | Sonnet | 4 dạng có hình (do_thi, tia_sang, truc_chuyen_dong); 8 chỉ tóm đề |

## D. Thứ tự đợt làm (mỗi đợt = 1 phiên)

Trong mỗi đợt: làm dạng có hình Khó/TB trước, dạng chỉ tóm đề Dễ để cuối. Đợt Sonnet đông dạng (Đ7–Đ9) có thể tách 2 phiên theo chương nếu context gần 180k.

| Đợt | Model | Nội dung | Bài (id) | Có hình (Opus+Sonnet) | Chỉ tóm đề | Họ hình mới tạo |
|---|---|---|---|---|---|---|
| Đ1 | Opus | L11 dao động–sóng: tạo 3 họ | 23, 27, 31 | 6 | 9 | vong_tron, song_day, van_giao_thoa |
| Đ2 | Opus | L12 nhiệt + từ trường, L11 năng lượng dao động | 2, 11, 26 | 6 | 9 | do_thi, tu_truong, thanh_nang_luong |
| Đ3 | Opus | L11 điện trường–mạch, L10 lực | 37, 43, 63 | 6 | 8 | dien_truong_deu, mach_dien, so_do_vecto |
| Đ4 | Opus | L10 động học, moment, chất lỏng | 50, 57, 66, 79 | 8 | 14 | truc_chuyen_dong, quy_dao_nem, thanh_moment, cot_chat_long |
| Đ5 | Opus | Quang (chỉ có ở KHTN9/HSG9) | 83, 156 | 4 | 8 | tia_sang, thau_kinh |
| Đ6 | Sonnet | L12 còn lại — dùng lại họ (P1) | 3, 4, 6, 7, 8, 9, 10, 13, 14, 125, 126, 127, 15, 16, 17, 18, 19 | 18 | 69 | — |
| Đ7 | Sonnet | L11 còn lại — dùng lại họ (P1) | 20, 21, 22, 24, 25, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 44 | 31 | 59 | — |
| Đ8 | Sonnet | L10 còn lại (P2) | 49, 52, 53, 54, 55, 58, 60, 62, 68, 69, 70, 71, 72, 73, 74, 76, 77, 78 | 34 | 58 | — |
| Đ9 | Sonnet | KHTN 9 + HSG 9 (P3) | 129, 130, 131, 84, 89, 90, 91, 160, 162, 155, 161, 166, 154, 167, 153, 164, 159, 157, 165, 152, 163, 151, 158, 150, 178 | 43 | 102 | — |

## E. Tổng số

| Loại | Số dạng |
|---|---|
| Opus — mẫu đầu họ hình mới | 15 |
| Sonnet — giải cùng hình, dùng lại họ | 140 |
| Đã làm (33 · D3 giao_thoa_2_nguon) | 1 |
| Chỉ tóm đề (Sonnet) | 336 |
| **Cộng** | 492 |

Ghi chú: id 125–127 chỉ tạo muộn nên số id gần dải KHTN 9; trong DB chúng thuộc chương 4 "Chương 3: Từ trường" lớp 12 (sau bài 10–14), không chồng lấn (đối chiếu `public/data/catalog.json` 4/11). Bài 7 · D5 (cột thuỷ ngân) dùng `cot_chat_long` tạo ở Đ4, nên Đ6 phải chạy sau Đ4.

Đ4 xong 3/11/2026 (nhánh `claude/wave-exercises-interactive-graphics-a3ea00`): 3 họ mới `truc_chuyen_dong`, `quy_dao_nem`, `cot_chat_long` (API ghi ở đầu mỗi file component; `cot_chat_long` có 2 cảnh `ong_u`, `be`) + `SoDoVecto` thêm cảnh `song` (sông có bờ gạch, điểm A/B/C, đường đi theo bước). Đã soát 375px mọi bước bằng driver (không chồng/tràn nhãn); HS ảo đã thử + sửa 3/11; ĐÃ ĐĂNG DB 50, 57, 79 ngày 4/11 (sao lưu `scripts/logs/bai-tap-mau-bai{50,57,79}-179377*.json` trong worktree), deploy + kiểm live 4/11. *Tóm đề viết tay, chưa qua HS ảo.

Đ5 xong 4/11/2026 (cùng nhánh): `tia_sang` (môi trường xếp lớp ngang, tia qua từng lớp theo `goc[]`, phản xạ, pháp tuyến, cung góc đặt tên theo hướng `toi`/`khuc_xa`/`phap_vao`…, `chieu: "len"`) và `thau_kinh` (trục + lưới ô ly, TK hội tụ/phân kì, F/F′, vật/ảnh ảo nét đứt, tia `qua`/`keo`/`mep`, thước ngang/dọc; `phan[]` = một khung cho mỗi câu a/b/c, chọn theo **bước đang làm** `tu_buoc`). API ở chú thích đầu hai file. Soát 375px mọi bước bằng driver + một ảnh nền tối + thẻ lề 1280; HS ảo đã thử 4/11 (8 · 7 · 7,5 · 6 điểm) → đã sửa (khoá lựa chọn sau khi đúng, 156 D7 thêm bước hỏi chiều ảnh), deploy + đăng DB 83, 156 ngày 4/11. **Giới hạn cho đợt Sonnet dùng lại** (84, 151, 158, 178): `tia_sang` chưa có lăng kính, gương phẳng, sợi quang, nguồn rộng/bóng tối, tia song song chéo — phiên đó phải mở rộng component (ghi vào mục F trước khi làm).

## F. Còn chờ thầy chốt (3/11/2026)
- ~~Bài 125–127 xếp lớp nào~~ — đã đối chiếu catalog 4/11: thuộc L12 Ch.3 trong DB, không cần thầy xác nhận.
- Có gộp Young (`van_giao_thoa`) vào `giao_thoa_2_nguon` để bớt một đợt Opus không.
- Một số dạng Trung bình hình rất có ích bị xếp "chỉ tóm đề" vì giới hạn 2 dạng/bài (31·D2 đếm cực đại, 58·D4 phân tích trọng lực trên dốc) — rà bảng B trước khi giao đợt.
- `do_thi` (30 dạng dùng lại) và `so_do_vecto` (26) rộng: làm đợt Opus thì cân nhắc tách 2 component.

- Đ1 (3/11): 23·D3 cần `do_thi` (tạo ở Đ2) nên mới có `tom_de`; thêm `cong_cu` khi Đ2 vào main. Ba họ mới khai từng bước bằng `lop: [[mục…], …]` trong JSON (xem chú thích đầu mỗi component) — phiên Sonnet dùng lại chỉ cần viết JSON.
- Đ2 (3/11): thầy duyệt giữ `do_thi` **một** component (gấp khúc `diem` + hàm lấy mẫu `ham` cos/mũ/nghịch/đa thức) — không tách. 23·D3 giờ thêm được `cong_cu` `do_thi`. API JSON từng họ: chú thích đầu `DoThi.tsx`, `TuTruong.tsx`, `ThanhNangLuong.tsx` và kiểu trong `features/lessons/types.ts`. `thanh_nang_luong` mới thử cảnh `lo_xo_ngang`; `con_lac_don`, `doc`, `hop_he` và mục `nam_cham` của `tu_truong` đã viết nhưng chưa soát bằng mắt — phiên dùng lại đầu tiên soát kỹ.
- ~~**Chờ thầy chốt (Đ2 phát hiện):**~~ ĐÃ VÁ 3/11 (`TomDeKhung` trong `TomDe.tsx`). Dạng chỉ có `tom_de` (không `cong_cu`) hiện **chưa hiện gì** — tóm đề chỉ vẽ trong `GiaiCungHinh`; `StepwiseSolution` chưa đọc `tom_de`. Các ô "✓ chỉ tóm đề" ở bảng B là dữ liệu đã ghi, chờ UI (đề xuất: dòng "Tìm" dính đầu khung bước + thẻ lề ≥1280, dùng lại `TomDeBody`).

- Đ3 (3/11): `dien_truong_deu` (bản +/−, đường sức, lực, quỹ đạo parabol `cat` dừng ở bản + chấm, thước ngang/dọc) và `mach_dien` (nguồn, R, đèn, V/A kế, khoá, mũi tên dòng, ngoặc nhóm, `bang` số điền dần với ô "?") — API ở chú thích đầu hai file + `features/lessons/types.ts`. Chưa soát bằng mắt: `khoa`, `dong_ho` kiểu A — phiên dùng lại đầu tiên (38, 40, 44) soát kỹ. Đã xem thử 375px; HS ảo + sửa 3/11; ĐÃ ĐĂNG DB 37, 43 ngày 4/11 (sao lưu `bai-tap-mau-bai{37,43}-179377*.json`), deploy + kiểm live 4/11.

## Cách cập nhật bảng này
Làm xong một dạng → đổi ô của dạng đó thành `✓` + ngày ở bảng B. Họ hình mới tạo xong → ghi tên component ở bảng A. Không sinh lại toàn bộ bảng.
