---
name: reference_scheduled_task_model
description: Model của lịch tự động (scheduled task) trong app Claude Desktop chỉ chọn được ở form Edit của app, không có trường model trong SKILL.md hay tool update_scheduled_task
metadata:
  type: reference
---

Lịch tự động (`~/.claude/scheduled-tasks/<id>/SKILL.md`) chỉ có frontmatter `name`, `description`; model và permission mode chọn ở form **Edit** của task trong app Claude Desktop (picker cạnh ô Instructions). Tool `update_scheduled_task` không đổi được model. Nguồn: https://code.claude.com/docs/en/desktop-scheduled-tasks.md

**Cách áp dụng:** thầy muốn lịch chạy model rẻ (Haiku) → nhắc thầy mở Edit task và chọn model; Claude không tự đổi được. Việc nặng trong task có thể giao subagent `model: haiku` để giảm chi phí dù phiên chính vẫn model mặc định.
- 17/10/2026: thầy muốn `hsg9-gui-btvn-thu-7` (xem trước BTVN HSG 9 thứ Bảy) chạy Haiku.
