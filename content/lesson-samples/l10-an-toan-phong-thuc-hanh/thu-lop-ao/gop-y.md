# Góp ý lớp ảo · L10 Bài 2 An toàn phòng thực hành (6 điểm dừng, 3 vai)
HS (haiku) đã đọc: CHỈ `sach-trong.md`, `de-hs-1..6.md` (chỉ-đề, không đáp án). Không đọc `dung-*.md`, `nhat-ky-thay.md`.

| # | file · vị trí | sửa gì | ưu tiên | bằng chứng |
|---|---|---|---|---|
| 1 | Tập ô 13·4 "Đo thử" | bỏ số vôn kế in sẵn (3,1; 6,2; 9,3; 12,4), để ô ghi theo clip | cao | hs-2 khó hiểu 4 |
| 2 | Tập ô 14·1 cột Ý nghĩa | bỏ chữ "cẩn thận/không được làm/phải làm" (lộ tên nhóm) | cao | hs-3 khó hiểu 2 |
| 3 | Tập ô 15·1 dòng nhiệt kế | để trống, ghi từ clip (không lộ B "gần tụt nhanh") | vừa | hs-4 khó hiểu 2 |
| 4 | màn 5a vs 5b–5d | dời màn ba bẫy xuống sau Câu 6 (Câu 4–6 chép nguyên chữ bẫy) | cao | hs-5 khó hiểu 1 |
| 5 | màn 5a, 6a | "quá áp" lạ → "vôn vượt định mức" ở 5a | thấp | hs-5 khó hiểu 2 |
| 6 | màn 6day | thêm "đánh ô 13·1 mục tiêu" | vừa | hs-6 khó hiểu (mục tiêu) |
| 7 | ghi chú điểm dừng 3 | ô 14·2 Câu 1 một dòng, còn lại về nhà (4 phút gấp) | vừa | hs-3 thời gian |
| 8 | ghi chú điểm dừng 2 | nói rõ Tập không in sẵn số; Câu 1 màn = Câu 2 ô 14·2 | thấp | hs-2 khó hiểu 1 |
| 9 | màn 4a từ khoá | HS chép từ khoá, giữ (gợi nhớ) | thấp | hs-4 khó hiểu 1 |
| 10 | màn 6s | một phút thiếu, không có ô Tập | thấp | hs-6 thời gian; ghi nhận, không sửa (Tập kín trang) |
| 11 | màn 1/mở đầu | "Phích vừa khít ổ" chưa gặp ở tr.13 | thấp | hs-1; ghi nhận |

## Đã xử lý
- 1, 2, 3: sửa `scripts/ruot-tap/l10-bai2.mjs`, in lại PDF: vẫn 12 trang (trang 1 dư 1 mm, trang 2 dư 17 mm).
- 4, 5: dời màn 5a sau 5d trong tren-lop.src.html, ghi chú dạy cập nhật.
- 6, 7, 8: thêm dòng ở màn Quay lại và ghi chú điểm dừng 2, 3.
- 9, 10, 11: ghi nhận, không sửa.
- Kiểm máy `scripts/tren-lop/kiem.mjs`: ĐẠT, 24 màn, không tràn, katex-error 0, 375px không cuộn ngang, chữ hình nhỏ nhất 0,85 (m6s).
- Lưu ý: de-hs-4 do thầy viết sai "chữ cái đầu bị che" và HS tưởng 2b chỉ có 2 dừng; không phải lỗi bản chiếu.
