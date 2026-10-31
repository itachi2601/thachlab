---
name: project_thachlab_token_hygiene
description: "Đo 31/10: phí cố định 87k/request, 56% token ở request >200k → compact 300k + hook nhắc; đợt 28/9: .claudeignore, docs/DATABASE.md tự sinh (99 bảng), STATE-archive, dọn 20 worktree 9 GB; còn treo: consolidate-memory, tắt MCP thừa, 2 skill đề xuất"
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

**Đợt 31/10/2026 (nhánh claude/token-usage-review-1b413a)** — đo 14 ngày, 920 phiên, 58k request, 11,4 tỷ cache-read phiên chính + 1,7 tỷ subagent.
- Phí cố định request đầu: trung vị 87k (28/9 là ~60k). Nguồn trong repo: AGENTS.md 23,6→~21 KB, mô tả skill 19,6→10,5 KB, MEMORY.md 11,3→10,2 KB. Phần còn lại là system prompt + MCP (Gmail, Drive, Sheets, Docs, computer-use, iOS Simulator, visualize) + skill claude.ai — chỉ tắt được trong app.
- 56% token nằm ở request context >200k; 7 phiên lớn nhất (424–706 request, đỉnh 600–970k) ≈ 1,6 tỷ. → `CLAUDE_CODE_AUTO_COMPACT_WINDOW=300000` trong `.claude/settings.json` + hook UserPromptSubmit `.claude/hooks/nhac-context.sh` nhắc /clear khi >180k.
- Danh sách skill bị cắt vì ngân sách: 6 skill dự án (phet, bao-cao-hoc-tap-tuan, soan-bai-tap-tu-luan-hsg, dang-tin-tuc-vat-ly, kiem-tra-tro-giang-tuan, xem-ghi-chu-lop) hiện không mô tả → rút 21 mô tả về ≤~450 ký tự.
- Còn treo: SKILL.md `soan-bai-ly-thuyet-tuong-tac` 117 KB (~40k token mỗi lần gọi, 16 lần/14 ngày) nên tách phần tham chiếu ra file riêng; 3.256 ảnh/14 ngày, 14 phiên >30 ảnh.
