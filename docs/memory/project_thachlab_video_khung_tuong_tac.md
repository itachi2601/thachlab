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

- 29/10 khuya (thầy báo tràn dọc): gốc lỗi = ở 1024–1279 cột tương tác chỉ ~322 px nên ô câu hỏi cao ~540 px, cả 6 ô cùng mở nội dung, trong bài video không dính → xem video thì mất câu hỏi. Sửa (f4e5efbac, đã deploy): chỉ ô hiện tại mở nội dung (ô khác 1 dòng, bấm = tua tới), video dính `lg:top-24` dưới thanh tab, rộng lg 280 / xl 340 theo chiều cao màn, điện thoại video ≤ 50svh; ≥1280 `.tl-box--khung.tl-khung-on` lan sang lề phải (`--wide-bleed`). Chưa chụp trên trang bài thật đã đăng nhập (sticky có thể bị tổ tiên overflow chặn — kiểm `getComputedStyle` + cuộn).
- 29/10 khuya: ĐÃ ĐĂNG khung vào cả 17 bài L12 có clip tự dựng (14 bài mới = 20 hộp, ghi thẳng DB bằng `scripts/video-thi-nghiem/gan-khung-db.py`, sao lưu `scripts/logs/ly-thuyet-bai<id>-khung-backup-*.json`); repo cũng đã gắn (034aca3e8) nhưng repo bài 12 thiếu hộp thuchanhtu-04, bài 9/12/15/126… repo lệch DB → đăng lại từ repo phải so kỹ. Kiểm web thật: 1280×800 khung cao 723 px (vừa một màn), 375 px video 228×406. Chỉ tdhphantu-04 (bài 6) chưa có JSON khung.

## 30/10/2026 — bỏ hộp chữ trùng khung + stepper dọc (đã đăng DB bài 2, đã deploy 8ed63d7c1)
- Bài Sự chuyển thể (lesson 2): hộp chữ `.tl-box--exp` tn-l12-chuyenthe-01 trùng 6 ô khung và lộ đáp án Dự đoán → bỏ, bù chi tiết thi cử (số liệu, nhiệt kế, sai số có chiều, áp suất) vào ô khung. Tiết kiệm ~1,1 màn hình 375px. Sách in (`book/build.py` đọc `.tl-box--exp`) sẽ thiếu khối này — chưa sửa pipeline sách.
- Khung: xem hết clip một lần thì mở cả 6 ô (localStorage `khung-xong:<id>`); màn rộng là stepper dọc (ray nối, ✓ ô đã qua, mốc m:ss thay "Xem lại", ô khoá "mở ở m:ss"); thẻ điện thoại ghi i/6 · m:ss. `.tl-khung-host li` bị globals.css ép `padding-left:0` → lề trái của li phải đặt inline.
- Sau khi đăng DB, trình duyệt có service worker cũ (`thachlab-runtime-v6`) vẫn hiện bản cũ tới khi SW cập nhật — kiểm trên trang thật phải xoá cache SW trước khi kết luận "DB chưa ghi".
- Còn lại: các bài L12 khác vẫn có cả hộp chữ lẫn khung cùng id (19 hộp) → rà và bỏ hộp chữ tương tự khi thầy duyệt.
- 30/10 (tiếp): đã bỏ 20 hộp chữ trùng khung ở 15 bài L12 còn lại (3 agent Sonnet song song + kiem-code soát: 4 chỗ phải sửa — lộ đáp án bài "em tự tính" ở apsuatdongnang-02/camungdt-01, câu alpha xuyên lá nhôm ở hatnhan-02, câu "quay nhanh" nói trước clip ở camungdt-03). Hộp phongxa-02 chứa figure Geiger → chèn lại sau khung; camungdt-01 tách bảng số đo ra `<details>`. Đã đăng DB cả 15 bài (log `/tmp/dang-15-bai.log`, sao lưu `scripts/logs/ly-thuyet-bai*-backup-*.json`). Không cần deploy (chỉ nội dung). 37 ô vượt hạn K3 (chữ/giây) — chấp nhận vì khung mở hết 6 ô sau lần xem đầu; sách in `book/build.py` giờ thiếu 21 khối thí nghiệm ở L12 → cần cho sách đọc JSON khung (việc riêng).
