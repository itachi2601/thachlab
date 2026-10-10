---
name: project_thachlab_l12_ra_soat_2026_10_06
description: Rà soát + sửa 18 bài lý thuyết tương tác lớp 12 (content/lesson-samples/l12-*) ngày 6/10/2026 — đã vào main, còn treo đối chiếu SGK và chưa đăng DB
metadata:
  type: project
---

**Mục tiêu:** 18 bài lý thuyết tương tác lớp 12 (`content/lesson-samples/l12-*`, gồm nhiệt học, từ trường–cảm ứng, hạt nhân) soạn 1–5/10/2026 được rà bằng 6 agent `kiem-code` rồi sửa bằng 6 agent `general-purpose` (mỗi nhóm 3 bài, thư mục riêng nên không đụng nhau). Liên quan [[project_thachlab_vl12_chuong1_ly_thuyet]], [[project_thachlab_bai_ly_thuyet_tuong_tac]].

**Đã xong (2026-10-06):**
- Sửa lỗi vật lí/hình SVG/đáp án/chuẩn skill cho cả 18 bài; commit `473f2193c`, `67e0d173e`, `5a8514266`; merge vào `main` `b864f6436`, push origin. `index.json` thí nghiệm sinh lại (211 mục) `9c9e92f11`. Nhật ký skill `4796da31b` (merge `11777751f`).
- 18/18 bài qua `check_quizzes` + `lint_theory`, `theory_html` khớp `bundle.json`. Bài `l12-ung-dung-cam-ung`: `main` đã có bản của phiên khác (`7c85cb6a5`), thầy chọn giữ bản của phiên này (10 file xung đột), bản kia còn trong lịch sử git.
- Bài `l12-cam-ung-dien-tu` (soạn trước chuẩn 2–4/10) viết lại gần hết; thêm `theory.src.html` + `build_bundle.py`. Thêm 5 file `content/thi-nghiem/tn-l12-udcamung-01..05.json`.

**CÒN TREO:**
- **Chưa ghi DB** — 18 bài chưa đăng/cập nhật lên web (dùng `scripts/cap-nhat-ly-thuyet-hang-loat.sh`, chạy trên Mac).
- **Thầy đối chiếu SGK** (agent không chắc nguồn): tên Boyle/Charles/Gay-Lussac cho đẳng nhiệt/áp/tích (`l12-phuong-trinh-trang-thai`); câu khí thực "năng lượng chuyển sang quay/dao động" (`l12-thuyet-dong-hoc-phan-tu`); lí do nồi nhôm/đồng không dùng được trên bếp từ; v̄ ≈ 455 m/s ở 0 °C; số liệu vòng khói NH₄Cl (số minh hoạ); β của C-14 có thoát khỏi mẫu không (`l12-phong-xa`).
- `tn-l12-tdhphantu-01/-04` vẫn ghi "≈ 400 m/s", lệch với bài nay ghi "vài trăm m/s".
- Chưa xem toàn trang 375px; hình 3 `l12-thang-nhiet-do` mới sửa theo toạ độ, chưa dựng ảnh. Nhiều bài vẫn "gần trần" 2480–2500 từ (cảnh báo lint, không phải lỗi cứng).
- Còn file chưa commit: thư mục `xem-thu/` của `l12-thuc-hanh-nhiet`, `l12-thuyet-dong-hoc-phan-tu`, `l12-ung-dung-cam-ung` (ảnh xem thử, theo skill không commit); `Navbar.tsx`, `docs/STATE.md`, bài L10/L11 là việc dở của phiên khác. Checkout đang ở nhánh `cursor/hoc-phi-an-0749` (thiếu commit của `main`); muốn khớp: stash → checkout main → pull → stash pop.

**Quyết định/mẹo không suy ra từ code:**
- Merge vào `main` khi working tree đầy WIP: dùng `git worktree add <dir> main` + `git merge`, không `checkout main`.
- `thi_nghiem.py` sinh `index.json` từ `tn-*.json` trên đĩa → chạy trong worktree của `main` (đủ file), không chạy trên nhánh thiếu commit (rơi mục).
- Lỗi lặp mà lint không bắt: số liệu thí nghiệm ngược chiều "Rút ra", nhiễu quiz tính sai, mũi tên SVG đảo chiều, B nằm trong mặt phẳng vòng dây, đáp án dồn A/B, số phút Mục tiêu lệch lint — đã ghi ở `## Nhật ký rút kinh nghiệm` của `.claude/skills/soan-bai-ly-thuyet-tuong-tac/SKILL.md` (chưa sửa thành bước trong quy trình skill).
