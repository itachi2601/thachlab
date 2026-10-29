---
name: project_thachlab_video_khung_tuong_tac
description: "Bản thử video thí nghiệm bán tương tác (khung 6 ô + dừng ở câu Dự đoán), 29/10/2026; trang /dev/video-tuong-tac, chưa gắn vào bài"
metadata:
  node_type: memory
  type: project
---

29/10/2026 thầy đồng ý thử: quanh 3 clip tự dựng đã có (boyle, chuyenthe, camungdt) thêm khung sáu ô (Giả thuyết→Dự đoán→Dụng cụ→Quan sát→Rút ra→Chưa nói được) sáng theo giây, ô sau khoá; video tự dừng một lần ở câu Dự đoán, chọn xong bấm Xem tiếp, không điểm. Mã: `components/lessons/VideoThiNghiemKhung.tsx`, dữ liệu `content/thi-nghiem/video-khung/<id>.json` (mốc giây từ `render.py <clip> --kich-ban`), xem thử `/dev/video-tuong-tac`. kiem-code soát xong, đã sửa 3 lỗi chặn.

**Còn mở:** (1) ô Giả thuyết hiện từ giây 0 nên lộ đáp án câu Dự đoán (T2) — thầy quyết: khoá tới sau Dự đoán hay chỉ nêu đại lượng; (2) chưa gắn vào bài thật (hộp video trong DB là HTML tĩnh, cần cách nhúng component); (3) chưa ghi sự kiện (dừng/chọn/xem lại) vào DB để đo; (4) JSON nguồn `tn-l12-boylecharles-01.json` còn mâu thuẫn sai số 5%/8%.

**Why:** học sinh 14–18 học tốt hơn khi đoán trước; khung cạnh video theo nguyên tắc kề cận (Mayer), clip không lời cần chữ nhưng không nói trùng phụ đề (V8, V12).
**How to apply:** nhân ra clip khác = tạo JSON mốc + chọn; liên quan [[project_thachlab_video_thi_nghiem_tu_dung]].
