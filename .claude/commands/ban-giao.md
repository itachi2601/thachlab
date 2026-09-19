---
description: Chốt phiên - ghi trạng thái việc đang làm vào memory trước khi clear
allowed-tools: Bash(git status:*), Bash(git log:*), Bash(git diff:*), Read, Write, Edit, Glob
---

Chốt lại phiên này để phiên sau nắm được việc. KHÔNG commit, KHÔNG deploy, KHÔNG sửa code.

## 1. Xem thực tế đang ở đâu

- `git status --short` và `git log --oneline -10`
- `git diff --stat` + `git diff --stat --cached` để biết file nào đang sửa dở
- Đối chiếu với những gì ta vừa làm trong phiên này

## 2. Cập nhật memory

Thư mục memory: `~/.claude/projects/-Users-MAC-Projects-thachlab/memory/`

Với mỗi mảng việc đang dở:
- Tìm file `project_*.md` đã có về mảng đó (đọc `MEMORY.md` để biết có gì) — **sửa file đó**, đừng tạo file trùng
- Chưa có thì tạo mới, đặt tên `project_thachlab_<slug>.md`, rồi thêm một dòng vào `MEMORY.md`

Nội dung phải trả lời được, cụ thể, có đường dẫn file:
- Mục tiêu của mảng việc này là gì
- Đã xong tới đâu (file nào, commit nào)
- **Còn chờ gì** — migration chưa chạy, chưa test, chưa deploy, chờ user gửi gì
- Quyết định thiết kế nào đã chốt mà đọc code không tự suy ra được

Ngày tháng ghi tuyệt đối (2026-09-14), đừng ghi "hôm qua", "tuần trước".

## 3. Báo lại

Liệt kê ngắn gọn: đã ghi/sửa file memory nào, việc gì còn treo. Rồi nhắc tôi có thể `/clear`.
