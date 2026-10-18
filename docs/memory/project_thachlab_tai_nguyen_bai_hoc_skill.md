---
name: project-thachlab-tai-nguyen-bai-hoc-skill
description: Skill tai-nguyen-bai-hoc (kế hoạch hình/PhET/video cho bài học) đã chép vào repo 7/10/2026; bản gốc ở Library plugin
metadata:
  type: project
---

Skill `tai-nguyen-bai-hoc` lập kế hoạch tài nguyên trực quan cho bài từ file .tex: bảng chọn công cụ (PhET iframe ưu tiên, widget HTML, TikZ/SVG cho hình có số liệu, ảnh Gemini chỉ cho hình đời sống, video YouTube kèm mốc thời gian), xuất `prompts.md` cho Gemini, kiểm ảnh, chèn rồi chuyển sang `dang-bai-hoc-thachlab`.

Nguồn gốc: Library plugin (`~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/.../skills/tai-nguyen-bai-hoc/`), chỉ có `SKILL.md`. Ghi nhận 7/10/2026: chép nguyên bản vào `.claude/skills/tai-nguyen-bai-hoc/` (repo là nguồn chính).

**Why:** trước đó skill chỉ nằm ngoài repo, phiên cloud và Codex không thấy.
**How to apply:** sửa skill thì sửa bản trong repo rồi chạy `scripts/cai-skill.sh`; bản Library có thể lệch, diff trước ([[feedback_skill_two_copies]]). Đăng bài theo [[project_thachlab_dang_bai_hoc_skill]]. Với bài lý thuyết tương tác thì dùng [[project_thachlab_bai_ly_thuyet_tuong_tac]] (hình SVG tự vẽ), skill này chủ yếu cho bài .tex kiểu cũ.

**18/10/2026 · Đợt 1 L12 ch1–2 (id 2–9):** 8 sim PhET nhúng vào 6 bài (2, 4, 6×2, 7, 8, 9) đã ghi DB + deploy; kế hoạch `content/tai-nguyen/vl12-ch1-2/kehoach.md`. Bài 3 và 5 bỏ PhET (sim không minh hoạ được). Video: `prompts-video.md` chờ thầy dán Gemini (WebSearch không có YouTube). Bẫy deploy: lỗi font "exactly one entry" = cache `.next` hỏng → `rm -rf .next`; typecheck `scripts/*.mts` đã loại khỏi tsconfig; sau deploy HS cũ vẫn thấy bài cũ vì service worker cache (`thachlab-runtime-v4`) tới khi tải lại lần 2. Đợt sau: L12 ch3–4 (id 10–19) rồi L11/L10 theo `docs/memory` + kehoach.
