---
name: project_thachlab_video_khung_tuong_tac
description: "Bản thử video thí nghiệm bán tương tác (khung 6 ô + dừng ở câu Dự đoán), 29/10/2026; trang /dev/video-tuong-tac, chưa gắn vào bài"
metadata:
  node_type: memory
  type: project
---

29/10/2026 thầy đồng ý thử: quanh 3 clip tự dựng đã có (boyle, chuyenthe, camungdt) thêm khung sáu ô (Giả thuyết→Dự đoán→Dụng cụ→Quan sát→Rút ra→Chưa nói được) sáng theo giây, ô sau khoá; video tự dừng một lần ở câu Dự đoán, chọn xong bấm Xem tiếp, không điểm. Mã: `components/lessons/VideoThiNghiemKhung.tsx`, dữ liệu `content/thi-nghiem/video-khung/<id>.json` (mốc giây từ `render.py <clip> --kich-ban`), xem thử `/dev/video-tuong-tac`. kiem-code soát xong, đã sửa 3 lỗi chặn.

**Còn mở:** (1) ĐÃ XONG 29/10: thầy chốt khoá Giả thuyết tới sau Dự đoán — trước đó ô hiện câu trung tính `kiem` ("Cần kiểm tra"), sau Dự đoán mới hiện giả thuyết; (2) chưa gắn vào bài thật (hộp video trong DB là HTML tĩnh, cần cách nhúng component); (3) chưa ghi sự kiện (dừng/chọn/xem lại) vào DB để đo; (4) JSON nguồn `tn-l12-boylecharles-01.json` còn mâu thuẫn sai số 5%/8%.

**Why:** học sinh 14–18 học tốt hơn khi đoán trước; khung cạnh video theo nguyên tắc kề cận (Mayer), clip không lời cần chữ nhưng không nói trùng phụ đề (V8, V12).
**How to apply:** nhân ra clip khác = tạo JSON mốc + chọn; liên quan [[project_thachlab_video_thi_nghiem_tu_dung]].

- 29/10 chiều (học sinh ảo Opus xem, thầy chốt sửa cả 5): Giả thuyết ẩn tới sau khi chọn; chạm video/tua qua đều bị hỏi lại (chỉ có nút "Chưa muốn đoán, xem luôn"); desktop video TRÁI dính + tương tác PHẢI, mobile video dính trên đầu thu theo chiều cao; đổi tên clip Boyle; rút ô Dụng cụ nước đá. Quy tắc K1–K10 ở skill `dung-video-thi-nghiem` (mục "Khung bán tương tác") + V13 trong QUY-TAC-THIET-KE; script `scripts/video-thi-nghiem/xuat-khung.py <clip> [--kiem]`. Còn: 20 clip nhóm C chưa có JSON khung; mp4 đã đăng còn nút A/B/C vẽ trong hình, chữ "YÊN" hoa, số 208→219 thoáng qua (K10, dựng lại khi có đợt sửa clip).

- 29/10 tối: JSON khung đủ 23 clip L12 (3 mẫu + 20 clip nhóm C), `--kiem` OK cả 23, trang xem thử `/dev/video-tuong-tac` có đủ 23; kiem-code soát vật lí 20 file không lỗi chắc chắn, 15 chỗ K4 + 3 chỗ nội dung đã sửa (commit bdd37d9a5). Phiên khác "Thiết kế lại hộp video thí nghiệm" [af7377] đụng hộp video — đối chiếu trước khi gắn vào bài. Còn: gắn vào bài thật (đo sticky với `.lesson-nav` top 76px, xoay ngang, toàn màn hình iOS), ghi sự kiện DB, dựng lại mp4 theo K10.

- 29/10 khuya: ĐÃ GẮN vào 3 bài L12 trong repo (Boyle id 7, Sự chuyển thể id 2, Cảm ứng điện từ id 13): `scripts/gan-khung-video.mts`, `ContentHtml` → `KhungPortals` → `VideoKhungLazy`; bài không dùng video dính; xem thử `/dev/video-tuong-tac/bai?bai=…`. CHƯA đăng DB (lệnh: `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/<slug>/bundle.json <id> --chi-video`) và CHƯA deploy code (ContentHtml, globals.css). Cảnh báo: `chen-video-thi-nghiem.mts --lam-lai` làm mất nội dung bài (xem nhật ký skill).

- 29/10 tối muộn: ĐÃ DEPLOY code (nhánh deploy 323e075) và ĐÃ ĐĂNG 3 bài lên DB (mục lý thuyết id 220/8/66; sao lưu ở `scripts/logs/ly-thuyet-bai{7,2,13}-backup-*.json`). `--chi-video` báo "khác ngoài khối video" dù chỉ thêm thuộc tính khung (so bằng difflib với bản sao lưu: đúng) → dùng `--cho-phep-khac` sau khi tự so. Bài 13: DB đặt 2 hộp video ở vị trí khác bản repo (repo `bundle.json` lệch DB từ trước) → đăng bản DB + thuộc tính khung, repo bài 13 vẫn lệch DB. Còn: chụp kiểm trang bài thật sau đăng nhập, ghi sự kiện DB.
