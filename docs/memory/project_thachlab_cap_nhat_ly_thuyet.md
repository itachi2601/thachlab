---
name: project-thachlab-cap-nhat-ly-thuyet
description: Quy tắc đẩy riêng phần lý thuyết bài học lên DB (script cap-nhat-ly-thuyet.sh), bài Giao thoa sóng L11 đã soạn chờ đăng
metadata:
  type: project
---

Thầy yêu cầu 2/10/2026: cập nhật bài lý thuyết tương tác phải **chỉ đẩy phần lý thuyết**, không đụng đề/bài tập mẫu/tiêu đề. Bộ script: `scripts/cap-nhat-ly-thuyet.sh` (bọc `update-ly-thuyet-from-bundle.mts`, nhận theory.html hoặc bundle.json, mặc định chỉ ghi `body_html`, tự sao lưu) + `khoi-phuc-ly-thuyet.mts`. Quy tắc đã ghi vào `AGENTS.md` và skill soan-bai-ly-thuyet-tuong-tac.

Bài Giao thoa sóng Vật lí 11 (lesson 31) soạn xong tại `content/lesson-samples/l11-giao-thoa-song/` (commit e4f76f15), **chưa đăng**: chờ thầy chạy `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l11-giao-thoa-song/theory.html 31`.

**Why:** tránh ghi đè Luyện tập/đề đã có học sinh làm.
**How to apply:** mọi lần đăng lại lý thuyết dùng script này; `\lt` thay `<` trong công thức.

## 4/10/2026 — quy tắc thành ràng buộc trong script (thầy: "chỉ đăng đúng vào phần lý thuyết của bài, không làm ảnh hưởng đến phần còn lại")

`update-ly-thuyet-from-bundle.mts` nay tự thực thi quy tắc, không dựa vào việc người chạy nhớ:
1. Lọc đúng MỘT mục `kind='ly_thuyet'` của bài; 0 hoặc >1 mục → dừng (không tự tạo mục).
2. `--dry-run` in rõ **phạm vi**: "CHỈ mục #108 (ly_thuyet). 2 mục khác của bài giữ nguyên — #109 bai_tap_mau, #110 luyen_tap."
3. UPDATE ràng buộc cả `id` lẫn `kind='ly_thuyet'`, `.select("id")` và đòi đúng 1 dòng bị ảnh hưởng.
4. Chụp toàn bộ `lesson_items` của bài TRƯỚC/SAU rồi đối chiếu: ngoài `body_html` (và `title`/`subtitle` khi
   `--with-title`) của mục Lý thuyết, mọi cột/mục khác phải y nguyên; lệch → in danh sách chỗ lệch + lệnh hoàn tác,
   `exit 1`. Logic đối chiếu đã kiểm bằng 8 ca (chỉ body_html đổi / mục Luyện tập đổi / mất exam_ids / đổi title
   ngoài phạm vi / có `--with-title` / thêm mục / mất mục / không đổi gì) — tất cả đúng.
5. Quy tắc ghi ở `AGENTS.md` mục "Cập nhật bài lý thuyết đã đăng" + bước 7 của skill soan-bai-ly-thuyet-tuong-tac,
   kèm câu "sửa script thì giữ nguyên phần kiểm này".

Bài 13 Tổng hợp và phân tích lực (lớp 10, lesson 58) đã đăng theo đúng quy tắc này 4/10/2026 (item 108, sao lưu
`scripts/logs/ly-thuyet-bai58-backup-1791083195069.json`), đã deploy; mục #109 và #110 giữ nguyên.
