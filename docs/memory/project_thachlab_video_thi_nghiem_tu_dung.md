---
name: project_thachlab_video_thi_nghiem_tu_dung
description: "Video thí nghiệm tự dựng (9:16, không lời, phụ đề + nhạc tổng hợp) cho thí nghiệm không có clip YouTube; Lô 0 = 3 clip mẫu L12 làm 27/10/2026"
metadata:
  node_type: memory
  type: project
---

Thầy chốt 27/10/2026: thí nghiệm không tìm được clip YouTube thì tự dựng video kiểu "tóm tắt Bài 1 Ch.2 L12" nhưng **không giọng đọc**, chỉ phụ đề + nhạc nền (giọng chỉ dành cho video ôn tập).

- Bộ dựng: `scripts/video-thi-nghiem/` (`engine.py`, `render.py <tên clip> [--preview]`, kịch bản mỗi thí nghiệm ở `clips/*.py`). mp4 ra `scripts/video-thi-nghiem/ra/` (gitignore). Nhạc tổng hợp bằng numpy, không dính bản quyền.
- Lô 0 xong và thầy DUYỆT (27/10, bản Opus làm lại): `boyle` 48 s, `chuyenthe` 49 s, `camungdt` 42 s; 1,9–2,6 MB/clip. Skill: `.claude/skills/dung-video-thi-nghiem`. Mỗi clip: hook có hộp Dự đoán → tiến hành vẽ động theo `so_lieu_mau` → rút ra (cơ chế, giới hạn, bẫy).
- Còn mở: chỗ đặt mp4 (YouTube không công khai hay file tĩnh trong web) chưa chốt; chưa chèn vào bài. Engine đã sửa lỗi chữ không mờ dần (Pillow 11, `IMG_REF`/`dtext`).

- 27/10 tối: `chuyenthe` bản 3 theo góp ý học sinh ảo — lộ đáp án C + phóng to −6→0 °C, trục t cố định, hình tan/sôi riêng, câu hỏi chốt 4 vs 27 phút; bỏ nhạc, chỉ tiếng báo ở mốc (`cues` → `engine.sfx`). Thầy DUYỆT cả 3 clip bản 3 (27/10): chuyenthe, boyle, camungdt (đã vẽ lại đường sức ra N vào S). mp4 ở `ra/*-v3.mp4`; còn chờ chốt nơi đặt mp4. Lỗi nhỏ còn lại: JSON boyle tự mâu thuẫn sai số 5% (rut_ra) vs 8% (quan_sat).

**Why:** 271/306 thí nghiệm chưa có video; clip thật không có cho nhiều thí nghiệm.
**How to apply:** lô tiếp theo = viết thêm `clips/<tên>.py` (copy mẫu gần nhất), render trong tab terminal (~2 phút/clip, chạy song song được). Liên quan: [[project_thachlab_thi_nghiem_khung_de_thi]].

- 28/10: lọc YouTube 195 thí nghiệm → A 23 / B 88 / C 84 (`content/thi-nghiem/danh-sach-tu-dung.md`); thầy duyệt hết A → 20 clip nhập kho + chèn vào file bài (3 trùng clip đã có), **chưa đăng DB**. Thử 3 clip C bằng Opus: `phongxa2`, `udcamung2`, `thangnhietdo4` (47–50 s, 1,8–2,1 MB) — chi phí đo được 1,7–2,3 USD/clip → 84 clip C ≈ 170–200 USD. Chờ thầy xem 3 clip rồi chốt chạy hàng loạt; nhóm B (88) chờ thầy duyệt.
- 28/10 chiều: lô 1 = 10 clip L12 nhóm C (antoanpx1, apsuat1/2, camungdt3, dttruong2, hatnhan1/2, mayphat1/3, nllk1) render xong, commit `clips/*.py`; 24,0 USD (TB 2,4 USD/clip, kể cả cổng B kiem-code). Còn 7 clip L12 nhóm C cho lô sau. Tồn: JSON `tn-l12-hatnhan-02` tên/mục tiêu nói "suy ra bán kính hạt nhân" nhưng R lấy từ công thức, và cân 0,001 g vs ±0,01 g lệch nhau → cần sửa JSON.
- 28/10 tối: lô 2 = 7 clip L12 nhóm C còn lại (pttrangthai2, thangnhietdo1, thuchanh2, thuchanhtu3/4, tutruong4, xoaychieu3) render + commit; 18,3 USD (TB 2,6). **Nhóm C L12 xong cả 20** (3 thử + 10 lô 1 + 7 lô 2). Đã sửa JSON hatnhan-02 (tên/mục tiêu, cân 0,01 g) và pttrangthai-02 (p/t giảm dần). Tồn: JSON tutruong-04 ghi nam châm trụ đứng, clip vẽ nằm ngang (sơ đồ). mp4 chưa chèn bài, chưa đăng.
- 28/10 chiều: **ĐÃ LÊN WEB**. 23 clip L12 (20 nhóm C + 3 bản 3 đã duyệt) ở bucket `lesson-clips/clip/<tn>-20261028.mp4|.webp`; chèn 16 bài L12 + đăng DB cùng 22 bài nhóm A còn treo = 32 bài (log `scripts/logs/dang-ly-thuyet-hang-loat-20261028-16*.log`); kiểm web bài 18: video phát được, 1080×1920. Không cần deploy. Tồn: udcamung-02 chưa chèn (bài 126 bản đăng không có hộp này); udcamung-04 (nhóm A) cũng chỉ vào `.cu`.
- 28/10 tối: bài 126 thêm hộp thí nghiệm hai cuộn + clip udcamung-02 (kiem-code ĐẠT), đã đăng + kiểm web. 23 clip đổi nhãn "Xem thí nghiệm dựng lại: …" + dòng Nhìn vào, đăng lại 17 bài. Nhóm C L12 xong trọn trên web. Còn: udcamung-04 (YouTube nhóm A) chỉ ở thư mục `.cu`.
- 28/10 tối: hộp clip tự dựng đổi sang khung dọc 9:16 + tên TN làm tiêu đề (CSS `tl-video--doc` trong globals.css), đăng lại 17 bài (16 L12 + 126) và deploy.
- 28/10 khuya: 23 clip dựng lại (V12: vùng an toàn khi dừng + ≤200 từ/phút, phụ đề ≤8 từ một dòng), tải `<tn>-20261028-2`, đổi URL tại chỗ trên DB 17 bài. CSS khung dọc `tl-video--doc` CHƯA lên production (nhánh deploy 22:44 không có) → thầy chạy `bash scripts/deploy.sh`.
