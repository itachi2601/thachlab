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

**Why:** 271/306 thí nghiệm chưa có video; clip thật không có cho nhiều thí nghiệm.
**How to apply:** lô tiếp theo = viết thêm `clips/<tên>.py` (copy mẫu gần nhất), render trong tab terminal (~2 phút/clip, chạy song song được). Liên quan: [[project_thachlab_thi_nghiem_khung_de_thi]].
