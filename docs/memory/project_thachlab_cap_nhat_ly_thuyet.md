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
