---
name: project_thachlab_title_showcase
description: "Danh hiệu đeo dưới tên HS + khung sưu tập huy hiệu cạnh rank — code xong, commit 7d4cb122 đã push origin/main + deploy 28/9/2026; migration 20260928130000 ĐÃ chạy 28/9 10:42; 13 ảnh BST/thành tích chưa vẽ (spec đã ghi)"
metadata:
  type: project
---

28/9/2026 thầy yêu cầu: tên HS có dòng danh hiệu đang đeo bên dưới, cạnh rank có khung nhỏ hiện mọi huy hiệu đã sưu tập.
Nghiên cứu: `docs/rank-title-showcase-design.md` + mockup https://claude.ai/artifact/WdsCPm7LFMSGEwvnnxCEtG (v2, ảnh thật).

**Đã làm (commit 7d4cb122 trên origin/main, build từ deploy-tree, 28/9/2026):**
- `components/rank/WornTitle.tsx` (logo + tên + mức, màu theo mức) gắn ở khung chào ThptStudentHome, RankCard, RankPage,
  chip ClassRankGroups, top tuần ClassRankBoard. `TitleShowcase.tsx` cạnh RankCard trên trang chủ HS (grid 2 cột desktop).
  `TitleBadge.tsx` (next/image; chưa có ảnh → lục giác vàng ★).
- Ảnh: DÙNG bộ của PR #15 (commit 39c71b76, phiên khác): `public/images/rank/titles/cm-*.webp` 512px +
  `features/rank/badge-assets.ts`. Em bổ sung `SINGLE_SLUG` (13 bst-/tt-), `SINGLE_AVAILABLE` (trống), `titleBadgeDisplaySrc`,
  `levelTextColor`; vá `cm-dien-truong-thuc-tinh.webp` bị 0 byte. KHÔNG tạo bộ ảnh thứ hai.
- Migration `20260928130000_rank_title_code_in_class_rpcs.sql` (+ rollback perf/rollback/): rank_class_groups trả title.code,
  rank_class_board trả top_week[].title. Client chấp nhận cả dạng cũ → CHƯA chạy cũng không lỗi, chỉ thiếu logo ở chip lớp/top tuần.
- Spec vẽ 13 danh hiệu bộ sưu tập (khung kép vàng + nguyệt quế + vương miện) và thành tích (huy chương tròn đinh tán) đã ghi
  vào design system Cowork (project/README.md v12). Thêm ảnh: ép 512px vào public/images/rank/titles/ + thêm mã vào SINGLE_AVAILABLE.

**Why:** thầy muốn động lực sưu tập; "đeo danh hiệu" vốn đã có (profiles.display_title_code), chỉ thiếu logo + chỗ hiện.

**How to apply (chốt 2026-09-28, cuối phiên):**
- Migration `20260928130000` ĐÃ chạy 2026-09-28 10:42 (log `scripts/logs/20260928-104205-*`). Cùng lúc thầy chạy
  `20260928100000_rank_specialist_difficulty` của phiên khác + `docs/supabase-recompute-rank-titles-20260928.sql`
  (63 danh hiệu mới cho 50 HS). Code specialist_difficulty ĐÃ gộp + commit 6edbeaf2 + push + deploy 2026-09-28
  (phiên sau, theo yêu cầu thầy) → web thật đã hiện lại tiến độ danh hiệu chuyên môn theo Dễ/TB/Khó. Chưa test UI thật.
- CÒN TREO của tính năng này: (1) CHƯA test UI bằng tài khoản HS thật (browser pane không còn phiên đăng nhập; mới có
  SSR render + tsc/eslint + xác nhận chunk trên web) — cần xem /tai-khoan khung chào, khung sưu tập, chip lớp, top tuần,
  mobile 375; (2) popover xem khung của bạn cùng lớp + ghim tối đa 6 huy hiệu (bước 4b/5 trong doc) chưa làm, chờ nhu cầu;
  (3) 13 PNG bộ sưu tập/thành tích chờ thầy vẽ trên Cowork, xong thì ép 512px vào `public/images/rank/titles/` và thêm mã
  vào `SINGLE_AVAILABLE` (features/rank/badge-assets.ts).
- Quyết định đã chốt: chỉ hiện danh hiệu ĐÃ MỞ trong khung nhỏ (không vẽ ô khoá); thứ tự đang đeo → mức cao → mới nhận;
  mức ghi bằng chữ + màu chữ (ảnh 3 mức chỉ khác khung, cỡ nhỏ không phân biệt được); chip 14–20px bắt buộc kèm tên vì
  nhiều danh hiệu trùng tông màu; KHÔNG thay RankBadge SVG bằng PNG rank.
- Git: local main đã merge origin/main (ef609edd) + có thêm af656f0a của phiên khác; commit của em 7d4cb122 build từ
  `.claude/worktrees/deploy-tree` (đang detach ở 7d4cb122). WIP specialist_difficulty đã commit 6edbeaf2.
Xem [[project_thachlab_specialist_badge_design]], [[thachlab-rank-system]], [[feedback-thachlab-deploy-scope]].
