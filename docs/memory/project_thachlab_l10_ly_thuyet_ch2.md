---
name: project_thachlab_l10_ly_thuyet_ch2
description: Rà soát lý thuyết + vẽ lại hình Chương 2 Động học L10 (Bài 4–12) ngày 30/10/2026 — đã commit, chờ thầy duyệt ảnh rồi đăng
metadata:
  type: project
---

30/10/2026 rà 9 bài Ch.2 L10 bằng skill ra-soat-bai-hoc (nhánh `claude/chuong-2-lop-10-57be28`, commit da0db972e…352ee4134). Chỉ ở repo, **CHƯA đăng DB**.

- Thư mục: `content/lesson-samples/l10-{do-dich-chuyen-quang-duong, toc-do-van-toc, thuc-hanh-do-toc-do, do-thi-dich-chuyen-thoi-gian, chuyen-dong-bien-doi-gia-toc, chuyen-dong-thang-bien-doi-deu, su-roi-tu-do, thuc-hanh-do-g, chuyen-dong-nem}`.
- Cả 9 bài: đầu mũi tên marker → chevron (import svg_lib skill), chữ ≥14. Hình vẽ lại đáng kể: B6 H3 cổng quang, B8 H3, B9 H1 (xe máy), B10 H2, B11 H1, B12 H1/H2/H4 (v không tiếp tuyến). Nội dung sửa: "Mang về: N hình" B4, B12; B10 câu dẫn Hình 1; kho TN `tn-l10-do-toc-do-01.json` thước chia 2 mm.
- **lesson_id SUY** (L10 Bài n = 45 + n, theo Ch.4 B23=68): B4=49 … B12=57 (Chuyển động ném). Dry-run phải in đúng tiêu đề, lệch thì dừng.
- **Chờ thầy chốt**: B7 `$\vec v_\mathrm{tb} = d/t$` (vectơ vế trái, vô hướng vế phải); B11 dòng 14 bấm tay "quanh 0,5 s" so với rơi thật 0,32 s (lệch +0,18 s hơi cao); dòng 🔑/Mang về nối ý bằng "·" (kiểu cố ý, không sửa).
- Vòng 2 chỉnh nhẹ (caption, B9 H1, B10 H2, B11 H1) chưa kiem-code soát lại; B12 và B6 H3 đã soát vòng 2.

**10/11/2026 — Bài 6 (lesson 51, item 287) SOẠN LẠI TỪ ĐẦU** theo bài thực hành SGK (bi thép, máng nghiêng, hai cổng quang, đồng hồ hiện số MODE A↔B / B), thay bản 30/10. Nhánh `claude/bai-thuc-hanh-do-toc-do-47c8b7`. Có đủ: lý thuyết (`theory.html`, 3 hình mới), bài tập mẫu 4 dạng (`scripts/data/bai-tap-mau/51.json`, dựng bằng `build-51.py`), quiz 20 câu (`scripts/data/theory-quiz/51.json`); đã kiem-code soát, danh sách ở `ra-soat.md` của bài. **ĐÃ ghi DB 10/11 08:25** (thầy duyệt): lý thuyết item 287; bài 51 chưa có mục `bai_tap_mau` nên tạo mục id 456 (`tao-muc-bai-tap-mau.mts --lesson 51 --mau 224`) rồi ghi 4 dạng; quiz exam 1352 gắn vào item 287, đề cũ 1227 giữ nguyên chờ thầy dọn; sao lưu `scripts/logs/ly-thuyet-bai51-backup-1794273860495.json`. **Đã deploy 10/11 ~08:50** từ worktree sạch tạm (đã xoá), kiểm trên web: lý thuyết mới, tab Bài mẫu 4 dạng, khối Kiểm tra nhanh. Worktree `deploy-tree` còn thay đổi `globals.css` cũ 28/10 chưa commit (đã có trong main) — worktree deploy mới phải `cp -cR` node_modules từ checkout chính + symlink `.env.local`, thiếu thì Turbopack báo không tìm thấy next/package.json. Thứ tự đã dùng: lý thuyết (`cap-nhat-ly-thuyet.sh … 51`) → bài tập mẫu → quiz (`--replace`, vì theorySection theo bản mới) → deploy. TN-03 (tấm chắn + clip) còn trong kho nhưng bài không dùng. Bài 51 chưa có YCCĐ riêng (bài tập mẫu gắn tạm YCCĐ Bài 3/Bài 5).
