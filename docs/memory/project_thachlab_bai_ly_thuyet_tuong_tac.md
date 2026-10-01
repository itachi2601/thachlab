---
name: project-thachlab-bai-ly-thuyet-tuong-tac
description: Skill soan-bai-ly-thuyet-tuong-tac + bài mẫu Định luật III Newton (lớp 10) — soạn 1/10/2026, thầy CHƯA xem được trên web
metadata:
  type: project
---

1/10/2026: làm bài mẫu `content/lesson-samples/l10-dinh-luat-3-newton/` (mở bằng sân băng, 4 quiz radio tự chấm, 3 `<details>`, 3 hình SVG tự vẽ) + CSS `.tl-*` cuối `app/globals.css` + skill `.claude/skills/soan-bai-ly-thuyet-tuong-tac/` (SKILL.md, linh kiện HTML, quy ước hình SVG, `lint_theory.py`, `preview.mjs`, `svg_lib.py`).

**Chưa làm / chờ:** chưa đăng DB, chưa deploy CSS, thầy chưa xem được bài → các mục "Cần kiểm tra khi thầy xem được" cuối SKILL.md còn trống; thầy sẽ phản hồi rồi bổ sung. Skill chưa sync sang Library plugin + `~/.codex` (chạy `bash scripts/sync-skill.sh` trên Mac).

**Why:** HTML lưu DB cấm script/style/on* nên tương tác chỉ bằng details + radio:checked; hình sách Halliday có bản quyền nên vẽ lại SVG.
**How to apply:** soạn bài lý thuyết mới → đọc SKILL.md trước; sau khi thầy xem được bài mẫu, cập nhật mục kiểm tra + bài học rút ra.

**Cập nhật 1/10 (sau khi thầy nêu cách dạy):** mục đích = bài đọc để thầy chiếu giảng trực tiếp VÀ học sinh tự học lại (không phải video). 3 thói quen bắt buộc: (1) mỗi kiến thức có ví dụ/thí nghiệm (`.tl-box--exp`: Làm–Quan sát–Rút ra), (2) "Trả bài" lý thuyết/công thức trước khi giải bài tập, (3) mỗi bài toán mẫu: bảng *Câu trong đề / Dữ liệu / Kiến thức liên quan* (`.tl-table--data`) rồi mới lời giải. Đã sửa bài mẫu (6 mục, 4 hình, 8 details), SKILL.md, linh kiện, lint cảnh báo thiếu 3 thứ đó. Bài mẫu đích đăng: lesson_id 61 (Lớp 10, chương 12) — thầy chọn xoá bài cũ đăng thay, chưa thấy lên web (cần upload-lesson + deploy từ nhánh có CSS).
