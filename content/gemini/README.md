# Thư mục dùng chung với Gemini (chốt 8/10/2026)

Quy trình và quy tắc: `.claude/skills/cap-nhat-bai-hoc-theo-gemini/SKILL.md`. Mỗi bài có `content/lesson-samples/<bài>/gemini/` gồm 3 ngăn đi một chiều:

| Ngăn | Ai ghi | Nội dung |
|---|---|---|
| `gui/` | Claude (script xuất) | File để thầy sao chép–dán vào Gemini |
| `nhan/` | Thầy (hoặc Claude lưu khi thầy dán JSON vào chat) | JSON Gemini trả về |
| `da-xu-ly/` | Claude | Sổ quyết định từng góp ý, bản đã kiểm, báo cáo ngắn |

`hang-doi.md`: trạng thái từng bài (`chua-gui → da-gui → da-nhan → da-sua → cho-duyet → da-dang`).
