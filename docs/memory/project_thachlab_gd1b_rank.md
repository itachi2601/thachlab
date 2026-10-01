---
name: GĐ 1b rank – gộp main + deploy
description: Trạng thái gộp nhánh modest-darwin-aj4843 (việc 1–5) vào main, lỗi kiểu preview.ts, deploy
type: project
---
Cập nhật 2026-09-30.

Mục tiêu: GĐ 1b rank — tiến bộ so với chính em (#1–2), phụ đạo mở khoá 24 giờ (#3),
luyện tập tăng dần độ khó (#4), bảng tuần lớp chỉ so với bạn cùng bậc (#5).

Đã xong:
- Nhánh claude/modest-darwin-aj4843 (6 commit, #1–5) đã merge vào main: commit cd4b80e6.
  Xung đột docs/STATE.md xử lý bằng `checkout --theirs` (lấy bản của nhánh).
- Migration đã chạy trên production: 20260929100000…130000, 20260930100000 (phụ đạo).
  20260930110000_rank_board_by_tier.sql — thầy báo đã chạy (việc 5).
- Lỗi build: features/rank/preview.ts:116 dùng kiểu `me` cũ (có `pos`). Đã thay bằng
  { rp_week, tier_code:"thach_dau" as const, division:null, tier_size: others.length+1,
    in_top:true, tied:0, above:null, below }. `npx tsc --noEmit` sạch. Build thành công.

Còn chờ / chưa xác nhận:
- Chưa xác nhận commit fix preview.ts đã commit + push origin main chưa (kiểm `git log origin/main -3`).
- Chưa xác nhận `scripts/deploy.sh` đã push nhánh deploy xong (kiểm `git ls-remote origin deploy`).
- Chưa kiểm bằng mắt trang Xếp hạng trên web thật (cửa sổ ẩn danh, tài khoản HS).
- Docs: chuyển 20260930110000 từ "ĐANG CHỜ" (STATE.md) sang STATE-archive.md; đánh dấu
  "ĐÃ CHẠY" trong scripts/run-migrations.sh; chạy `node scripts/gen-database-doc.mjs`.
- Còn stash cục bộ chưa xử lý: "docs-truoc-merge" (STATE.md, STATE-archive.md) và
  "docs-truoc-rebase" (DATABASE.md, DATABASE-RPC.md, ROADMAP.md). DATABASE*.md sinh lại được;
  ROADMAP.md kiểm trước khi bỏ.
- Untracked, KHÔNG xoá/clean: scripts/data/batch-250-3, batch-de-thi-thu-4, batch-de-thi-thu-5.

Bài học: nhánh song song đổi kiểu dùng chung → sau merge phải `npx tsc --noEmit` trước deploy.
