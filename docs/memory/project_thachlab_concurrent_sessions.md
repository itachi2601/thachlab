---
name: project_thachlab_concurrent_sessions
description: "Repo thachlab luôn có thể có phiên Claude khác sửa cùng lúc — quy tắc git/build/deploy an toàn (commit bằng pathspec, build sạch trong worktree, không tin báo cáo chưa tự verify)"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-09-28T17:04:05.351Z
  originSessionId: 50c3a84d-5a36-4441-9256-c5e110888e68
---

`/Users/MAC/Projects/thachlab` là thư mục dùng chung: thường xuyên có 2–3 phiên Claude khác sửa
cùng lúc, `git status` đổi giữa các bước, index (`git add`) dùng chung, untracked file có thể bị
phiên khác dọn. Mọi quy tắc dưới đây đều rút từ sự cố thật (18–28/9/2026).

## Commit
- **Luôn `git commit -m "..." -- <path...>` một lệnh**, không tách `git add` + `git commit`: index
  dùng chung có thể đã chứa WIP của phiên khác (đã 3 lần commit nhầm 14, 310, 351 file thay vì 1–2).
  File MỚI thì `git add <file mới>` rồi `git commit -- <mọi path>` ngay sát nhau. Sau commit soát
  `git show --stat HEAD`; nhầm thì `git reset --soft HEAD~1` (không mất gì) rồi làm lại.
- Trước khi add một file đang có WIP phiên khác (vd ThptStudentHome.tsx 26/9): `git diff HEAD -- <file>
  | grep '^+import'` để thấy hunk lạ; không stage hunk đó.
- Trước stash/rebase/reset: `git status` + `git log -1` ngay sát thao tác; file vừa đổi trong ~10 phút
  (`find . -mmin -10`, `stat -f "%Sm"`) → hỏi thầy. **Không `git stash` trần** khi có worktree/agent
  song song — nếu bắt buộc: `stash push -m <tên riêng>` chỉ đúng file cần, rồi `stash apply <hash>`
  (không `pop` trần), tự đối chiếu ngay.

## Build / deploy sạch
- `scripts/deploy.sh` build thẳng từ working tree → chạy trên cây bẩn = đẩy WIP phiên khác lên
  production. Cách đúng: worktree `.claude/worktrees/deploy-tree` (đã có node_modules + .env.local):
  `git -C <wt> checkout --detach main` rồi `bash scripts/deploy.sh` từ trong worktree đó. Tạo mới thì
  worktree phải nằm TRONG thư mục dự án và `cp -al node_modules` (hardlink; symlink hay /tmp làm
  Turbopack báo "points out of the filesystem root"). Xem lại `git log -1` sau build — phiên khác có
  thể vừa commit thêm.
- Lỗi build "next/font/google queries have exactly one entry" ở deploy-tree = cache `.next` hỏng →
  `rm -rf .next out` rồi chạy lại.
- Không chạy được `next dev` thứ hai trong cùng thư mục dù khác cổng (khoá theo thư mục) → dev server
  riêng phải ở worktree riêng, hoặc `npm run build` + `npx serve out/`. Dev server dùng chung mà treo
  giữa lúc nhiều phiên đang commit → đừng khởi động lại hộ, chuyển sang test trên web thật.

## Trùng việc & dữ liệu bay hơi
- Việc ghi ở `docs/STATE.md` mục "đang chờ/đề xuất" ai cũng đọc thấy và tự nhận: 27/9 có 3 phiên
  làm ĐÚNG một việc trong 3 worktree. Trước khi tin agent nền "xong", chạy `git worktree list` xem
  có worktree khác cùng chủ đề không.
- Untracked scratch trong `scripts/data/` từng biến mất giữa phiên (phiên khác `git clean`?). Trạng
  thái quan trọng ("file nào đã xử lý") phải nằm ở nguồn không thể mất: Supabase, hoặc di chuyển file
  nguồn đã xử lý ra thư mục ngoài repo. Thấy file rỗng/thiếu → kiểm tra nguồn khác trước khi kết luận.
- `.git/HEAD.lock` cũ hàng giờ + `ps aux | grep git` không có tiến trình git thật = an toàn để xoá;
  đừng suy từ "đang có nhiều phiên" mà giữ lock.

## Không tin báo cáo chưa tự verify
Phiên/agent khác báo "đã test, không còn crash" nhưng tự tái hiện (worktree cô lập đúng commit, tự
build, xoá đúng chunk, mở tab mới) thì thấy khác báo cáo ít nhất một phần — cả 2 lần trong đợt perf 4.
Việc liên quan production/dữ liệu học sinh: **luôn tái hiện bằng tay**, không suy luận từ code hay
lời kể.

**Why:** 26/9 thầy chọn "cứ deploy luôn" trên cây bẩn một lần (có hỏi trước) và may không sao —
đó là ngoại lệ có chủ đích, không phải quy trình.
**How to apply:** áp dụng cho MỌI thao tác git/build/deploy trong repo này, kể cả khi vội.
Liên quan [[feedback_thachlab_deploy_scope]], [[project_thachlab_token_hygiene]].
