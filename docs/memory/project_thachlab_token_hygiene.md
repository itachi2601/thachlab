---
name: project_thachlab_token_hygiene
description: "Đợt giảm token 28/9/2026: .claudeignore, docs/DATABASE.md tự sinh (99 bảng), STATE-archive, dọn 20 worktree 9 GB; còn treo: consolidate-memory, tắt MCP thừa, 2 skill đề xuất"
metadata:
  node_type: memory
  type: project
  originSessionId: 50c3a84d-5a36-4441-9256-c5e110888e68
  modified: 2026-09-28T16:49:39.397Z
---

Đợt "giảm token cho Claude Code" 28/9/2026, commit 68e24cb5 + b2ef4624 đã push main.

**Đã làm**
- `.claudeignore` (mới): node_modules/.next/out/dist, ảnh học liệu `public/**`, dump `output/ tmp/
  scratchpad/ scripts/data/`, và **`.claude/worktrees/`** — trước có 21 worktree = 9,1 GB bản sao
  repo, grep toàn repo ra kết quả ×21. Đây là nguồn phình context lớn nhất.
- `docs/DATABASE.md` trước đó **rỗng 0 byte**; giờ sinh bằng `node scripts/gen-database-doc.mjs`
  (chỉ đọc pg_class/pg_proc qua `supabase db query --linked`) → 99 bảng gom 7 nhóm + file riêng
  `docs/DATABASE-RPC.md` 216 hàm. Chạy lại sau mỗi đợt migration (đã ghi vào AGENTS.md).
- `docs/STATE.md` 208→110 dòng; log migration đã chạy → `docs/STATE-archive.md`.
- AGENTS.md có bảng "đọc khi cần" trỏ đúng file docs/ theo chủ đề.
- Worktree: gỡ 19/21, chỉ giữ `deploy-tree` (detached, dùng cho deploy.sh thin push). File sửa dở
  của 10 worktree đã commit snapshot "wip: snapshot…" vào **nhánh của chính nó** (không mất gì):
  feat/difficulty, perf/round4-katex-framer-split, claude/angry-curie-528414, claude/kind-mcnulty-346304,
  wip/perf-thpt, perf2/integration, claude/practical-bassi-68ca90, claude/quizzical-gauss-065911,
  claude/student-management-by-course-1890b4, claude/update-checklist-cnc-afc30c (cái này 24 file
  CNC lệch xa main — nếu thầy hỏi "code CNC checklist live monitor đâu" thì ở nhánh này).
- 3 commit chưa merge tìm thấy khi dọn: audit SQL (đã cherry-pick), Cache-Control deploy.sh (main đã
  có, bỏ), fix parser "Đáp án nào sau đây…" (main đã vá khác cách → gộp tay, thêm test 5 ca).

**Còn treo (thầy chưa quyết)**
- `/consolidate-memory` — 82 file memory/616 KB, MEMORY.md 80 dòng, nhiều mục đã xong.
- Tắt MCP không dùng cho web (iOS Simulator, computer-use, Google Drive, Claude Docs) trong app.
- 2 skill đề xuất: kiểm hồi quy đăng nhập 3 vai (từ [[project_thachlab_auth_regression_test]]) và
  kiểm tốc độ trước khi đăng (checklist trong AGENTS.md).
- (Parser fix b2ef4624 ĐÃ deploy 28/9 — build sạch trong worktree `deploy-tree` (`git checkout --detach
  main` rồi `bash scripts/deploy.sh` từ đó) để không dính WIP phiên khác. Dùng lại cách này khi
  working tree bẩn.)

**How to apply:** khi cần schema → đọc `docs/DATABASE.md`, đừng `select *`. Khi thấy
`.claude/worktrees/` lại phình → gỡ theo cách trên (snapshot vào nhánh rồi `git worktree remove`).
Liên quan [[feedback_token_discipline]], [[project_thachlab_concurrent_sessions]].
