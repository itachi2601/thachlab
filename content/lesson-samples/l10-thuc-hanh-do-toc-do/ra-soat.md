Chặng hiện tại: đã soạn lại + kiểm chéo xong (10/11/2026). Bước kế tiếp: thầy duyệt → đăng DB (lý thuyết, bài tập mẫu, quiz) → deploy.

# L10 Bài 6. Thực hành đo tốc độ — soạn lại 10/11/2026 (lesson_id 51, item lý thuyết 287)

Bản mới bám bài thực hành SGK: bi thép, máng nghiêng, nam châm điện, hai cổng quang E–F, đồng hồ hiện số (MODE A↔B, MODE A/B).
Bản cũ (xe đồ chơi, bấm tay, tấm chắn) bỏ; `content/thi-nghiem/tn-l10-do-toc-do-03.json` (tấm chắn, có clip) còn trong kho nhưng bài không dùng nữa.

## Lý thuyết (kiem-code soát độc lập: 14 nhóm số, 7 quiz, 5 câu Trả bài, 3 hình + ảnh 375px)
- [x] Câu 6 phương án B (± 0,003) không khớp lí do "lấy hiệu" — đổi thành ± 0,002 (0,3 % × 0,800), sửa cả `build_bundle.py`
- [x] "Thử sức đổi phương án": câu "thời gian chắn dài hơn ở F" sai chiều — sửa thành "ở E dài hơn ở F"
- [x] Thử thách ⭐⭐⭐: thêm điều kiện "chỉ khớp khi bi nhanh dần đều"
- [x] Thuật ngữ "sai số tương đối" → "sai số tỉ đối" cho khớp Bài 3 và tên YCCĐ
- [ ] Bảng Thí nghiệm 2: độ lệch tính so với t̄ đã làm tròn (0,024) — kết quả cuối không đổi, để thầy quyết có đổi số liệu không
- [ ] Hình 2: chấm đỏ tia sáng nằm sát mặt máng, chưa đúng ngang tâm bi như chú thích (hình vẫn đạt) — chỉnh nếu thầy muốn
- [ ] Mục VI "trượt băng tốc độ: tia sáng ở vạch đích" — người soát nghi (có nơi dùng chip); thầy rành môn này, xin thầy xác nhận
- [ ] Tổng 2.457 từ hiện ngay (trần 2.500), mục II.2 gần trần — không thêm chữ nữa

## Bài tập mẫu `scripts/data/bai-tap-mau/51.json` (4 dạng, 19 bước; kiem-code tự giải độc lập, đáp số khớp)
- [x] Dạng 1 bước 3: `loi_hay_gap` đặt nhầm lỗi của bước sau — đã thay
- [x] Dạng 1, 3: đề thiếu điều kiện "tia đi ngang tâm bi" — đã thêm
- [x] Dạng 2 bước 2: câu hỏi lộ hướng giải ("gồm cả sai số dụng cụ") — đã bỏ; bước 3 `loi_hay_gap` không phải lỗi — đã thay
- [x] Dạng 4: bỏ "sai số hệ thống/ngẫu nhiên" (bài lý thuyết không dùng) → "độ lệch luôn về một phía"
- [ ] Chưa có hình/mô phỏng dưới đề (bảng số liệu là hình của dạng); bài 51 chưa có YCCĐ riêng trong `question-topics.json` nên gắn tạm YCCĐ Bài 3 và Bài 5

## Quiz `scripts/data/theory-quiz/51.json` (20 câu: 14 TN + 6 Đ–S)
- [x] Câu 13 có hai đáp án đúng (đổi t sang mili giây cũng ra m/s) — thay phương án nhiễu "đổi t sang phút"
- [x] Câu 2 note B dùng kiến thức ngoài bài — đã sửa; câu 11 nhiễu 2s/t → s/(2t); câu 9 theorySection 2 → 1
- [ ] Câu 6, 7, 10 cùng xoay quanh tia lệch tâm (trùng ý một phần) — giữ, thầy muốn thì thay câu 7
- [ ] `theorySection` tính theo bản lý thuyết MỚI → phải đăng lý thuyết trước rồi mới đăng quiz
