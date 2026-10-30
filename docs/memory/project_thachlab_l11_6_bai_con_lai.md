---
name: project_thachlab_l11_6_bai_con_lai
description: Đợt 9/10/2026 soạn + đăng 6 bài lý thuyết tương tác L11 còn lại (B4, B7, B9, B10, B11, B15 — id 23/26/28/29/30/34); phân công agent, kết quả kiểm chéo, việc còn treo (video, thầy đối chiếu SGK)
metadata:
  type: project
---

Thầy yêu cầu 9/10/2026: "phân công agent tối ưu token, dùng skill soạn lý thuyết tương tác cho các bài còn lại của lớp 11". Liên quan [[project_thachlab_l10_ly_thuyet_ch5_7]], [[project_thachlab_bai_ly_thuyet_tuong_tac]].

**Phân công đã chạy (2 lô 3+3, ~14 lượt agent, ~3,7 M token agent):** bản giao việc dùng chung viết ra scratchpad (agent đọc file thay vì prompt dài); Opus soạn 4 bài (B4, B7, B9, B11), Sonnet soạn 2 bài thực hành (B10, B15); mỗi bài 1 `kiem-code` Sonnet kiểm chéo; sửa bằng SendMessage cho chính agent soạn; phiên chính chỉ chạy lint + thi_nghiem.py + commit + đăng.

| id | Bài | Thư mục `content/lesson-samples/` | Kiểm chéo |
|---|---|---|---|
| 23 | B4 Bài tập dao động | `l11-bai-tap-dao-dong` | 0 chặn; đăng bằng `upload-lesson.mts` (bài rỗng) → đề 906 |
| 26 | B7 Bài tập năng lượng | `l11-bai-tap-nang-luong-dao-dong` | 0 chặn (sửa A > Δl tĩnh) → đề 907 |
| 28 | B9 Sóng ngang/dọc | `l11-song-ngang-song-doc` | 0 chặn; `cap-nhat-ly-thuyet` item 77 |
| 29 | B10 TH đo tần số âm | `l11-thuc-hanh-do-tan-so-am` | 0 chặn (sai số cộng Δ dụng cụ theo SGK) → đề 908 |
| 30 | B11 Sóng điện từ | `l11-song-dien-tu` | 1 chặn (chú thích B "vào trang" ngược hình) đã sửa; item 155 |
| 34 | B15 TH đo tốc độ âm | `l11-thuc-hanh-do-toc-do-am` | 0 chặn (e = 0,6r, ống 16 mm); item 168 |

Commit `e37d29cc7` (main, đã push), kho thí nghiệm 266 → 283. Sao lưu DB: `scripts/logs/ly-thuyet-bai{28,30,34}-backup-*.json`. Deploy 9/10/2026 từ `deploy-tree` (bản build 6/6 có tl-quiz).

**Còn treo:**
- Video (bước 4c) chưa làm cho cả 6 bài; ứng viên chương 2 ở `content/thi-nghiem/video-de-xuat-l11-chuong2.md`.
- Thầy đối chiếu SGK: B9 cách nói "sóng mặt nước là sóng ngang" + năng lượng ∝ f²; B11 mốc tử ngoại 380 nm / tia X 10 pm–10 nm; B10 cách ghi Δf = Δf̄ + Δf_dc và số chữ số có nghĩa; B15 phần đặc trưng âm (mức nhận biết) và độ to chỉ gắn với L; B7 ký hiệu W_đ/W_t (bài 5 dùng E_đ/E_t).
- Lớp 11 KHÔNG còn bài lý thuyết tương tác nào thiếu (26 bài). Lớp 10, 12 cũng đủ.

**Cập nhật 12/10/2026:** video đã chèn + ĐĂNG (`--chi-video`) cho B9/B10/B11/B15 (id 28/29/30/34): 9 clip, bảng duyệt `content/thi-nghiem/video-de-xuat-l11-chuong2-con-lai.md`, commit `4003e5229`. Còn không có clip: `tn-l11-dotansoam-02/03`, `tn-l11-dotocdoam-03`, `tn-l11-songngangdoc-03` (dùng clip quay chậm, không phải bấm giờ), và clip mở bài của 4 bài. Tìm clip bằng `scripts/tim-clip-youtube.py`.

**Rà soát hình 30/10/2026 (Ch.1 L11 Dao động, Bài 2–7):** 14/19 hình vẽ lại (nhánh `claude/ra-soat-bai-hoc-chuong-1-34b0a1`, đã vào main). **ĐÃ ĐĂNG DB 30/10/2026 22:08–22:09** bằng `cap-nhat-ly-thuyet.sh` (lịch tự chạy), tiêu đề đã đối chiếu: Bài 2 = id 21, Bài 3 = 22, Bài 4 = 23, Bài 5 = 24, Bài 6 = 25, Bài 7 = 26; sao lưu `scripts/logs/ly-thuyet-bai{21..26}-backup-*.json`; không cần deploy (không đổi CSS). Còn: Bài 1 (`l11-dao-dong-dieu-hoa`) chưa rà/đăng; thầy chốt dòng 581 Bài 6 "4 hình = cả bài".
