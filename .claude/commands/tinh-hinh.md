---
description: Đầu phiên - đọc memory và working tree để nắm việc đang dở
allowed-tools: Bash(git status:*), Bash(git log:*), Bash(git diff:*), Read, Glob, Grep
---

Nắm tình hình trước khi làm. Chỉ đọc, chưa sửa gì cả.

1. `git status --short`, `git log --oneline -10`, `git diff --stat`
2. Đọc các file `project_*.md` trong `~/.claude/projects/-Users-MAC-Projects-thachlab/memory/` mà `MEMORY.md` cho thấy có liên quan tới đám file đang sửa dở — chỉ đọc file liên quan, đừng đọc hết.
3. Nếu working tree có file lạ không memory nào nhắc tới, mở xem đủ để đoán ý đồ.

Rồi tóm tắt cho tôi, tối đa 10 dòng:
- Đang làm dở mảng nào, tới đâu
- Việc gì đang treo chờ tôi (chạy migration, gửi key, test, deploy)
- Bước tiếp theo hợp lý là gì

Đừng bắt tay làm gì cho tới khi tôi nói.
