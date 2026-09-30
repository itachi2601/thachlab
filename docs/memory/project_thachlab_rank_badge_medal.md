---
name: thachlab-rank-badge-medal
description: "Huy hiệu bậc rank đã đổi sang huy chương quân đội (SVG) + đổi tên 7 bậc Tinh Quang→Chí Tôn 26/9/2026; mã bậc tan_binh… giữ nguyên; thiết kế gốc 'Astral Monarch' trong Design artifact"
metadata:
  type: project
---

Huy hiệu bậc rank (`components/rank/RankBadge.tsx`) đổi từ khiên đơn sắc sang **huy chương quân đội** SVG, commit `1a5468b9` (26/9/2026), đã push main + deploy qua worktree sạch `.claude/worktrees/deploy-tree`.

**Tên bậc mới (commit 219d1240, 26/9/2026, đã sửa DB rank_tiers + rank_seed_tiers):** tan_binh=Tinh Quang · chien_binh=Tiên Phong · tinh_anh=Nhật Hoa · tinh_nhue=Vương Lễ · dai_su=Vương Triều · cao_thu=Thiên Thể · thach_dau=Chí Tôn. MÃ BẬC KHÔNG ĐỔI — hàm SQL, test, memberships vẫn dùng mã cũ; danh hiệu "Chiến Binh Bất Diệt" là danh hiệu thành tích, không phải bậc, giữ nguyên tên.

**Tên bậc hai dòng (commit 759568af + fix ô mobile, 26/9/2026):** `components/rank/TierName.tsx` — tiếng Anh lớn (Cinzel, `--font-cinzel`) trên, tiếng Việt nhỏ (Playfair Display, `--font-playfair`) dưới; `TIER_META[code].en` = Starlight/Vanguard/Corona/Regalia/Dynasty/Celestial/Sovereign. `tierLabel()` một dòng giờ trả "Starlight III · Tinh Quang". Cỡ `sm` đưa phân bậc xuống dòng Việt; ô thống kê trang chủ HS xếp dọc trên mobile vì tên Anh Cinzel không cắt được.

**Quy ước đã chốt với thầy:**
- Thân huy chương + màu ruy-băng nhận diện BẬC: Tân Binh đĩa tròn sao (xanh đêm) · Chiến Binh khiên chữ V (xanh rêu) · Tinh Anh mặt trời 16 tia (cam) · Tinh Nhuệ thập tự pattée + nguyệt quế (đỏ thẫm) · Đại Sư sao 8 cánh treo vương miện (xanh hoàng gia) · Cao Thủ sao 16 cánh vàng-bạch kim (tím) · Thách Đấu đại huân chương gươm chéo + kim cương (đen-vàng-đỏ).
- Kim loại nhận diện PHÂN BẬC: III đồng · II bạc · I vàng; Cao Thủ/Thách Đấu (không phân bậc) và khi không truyền division → vàng.
- `TIER_META` màu bậc đổi theo màu ruy-băng (ảnh hưởng viền/nền RankCard, RankPage, ClassRankGroups).
- Badge dưới 40px bỏ filter bóng/pattern vải để nhẹ (danh sách lớp dùng size 14–32).

**Why:** thầy thấy huy hiệu cũ đơn điệu; đã thử 3 hướng (kim loại-đá quý, hologram sci-fi, huy chương quân đội) trong Design artifact "Astral Monarch — Rank System Design" (https://claude.ai/artifact/SAasE3rpgsZrKZj3euEwoY) và chọn huy chương quân đội ("quá đẹp luôn").

**How to apply:** muốn sửa hình huy chương thì sửa artboard trong artifact trước cho thầy duyệt rồi port sang RankBadge.tsx (cùng toạ độ viewBox 240×280, crop 28..212). Font tiếng Việt: Cinzel/Orbitron/Rajdhani KHÔNG có dấu Việt — dùng Playfair Display / Be Vietnam Pro / Chakra Petch / Exo 2. Thầy không thích ký hiệu viết tắt (SL, VG…) trên huy hiệu.

**26/9/2026 — Lộ trình các bậc (commit dd624860, đã push + deploy qua deploy-tree):** mục mới trên /lop-hoc/xep-hang ngay dưới thẻ bậc hiện tại — `components/rank/TierLadder.tsx`: dải 7 huy hiệu (✓ đã đạt / chấm = hiện tại / khoá), chạm để xem dải RP, 3 phân bậc III/II/I với ngưỡng (cùng công thức SQL rank_tier_info, chia đều /3), điều kiện RP + danh hiệu + thử thách. Dữ liệu từ `fetchTierLadder(seasonId)` (rank_tiers + tên đề, policy anyone-reads). Không có mùa → vẫn hiện 7 huy hiệu, chỉ thiếu số. Đã test mobile 375 + desktop bằng tài khoản admin (0 RP); chưa test với HS có RP thật.

**26/9/2026 — đầu trang HS gọn lại (commit f6139e30, đã deploy):** `components/rank/RankAvatarFrame.tsx` bọc AvatarUploader — vành kim loại theo phân bậc + vành màu bậc + huy chương nhỏ góc; khung chào chỉ còn tên + Lớp + thanh Năng lượng + ô Điểm TB; bỏ 3 ô Tiến độ/Điểm TB/Xếp hạng (trùng RankCard), RankCard không truyền name. ⚠ Commit f0069025 trước đó lỡ kéo WIP `@/services/homework` của phiên khác (file untracked) → f6139e30 gỡ lại; working tree ThptStudentHome vẫn giữ WIP đó cho phiên kia. Luôn `git diff HEAD -- file` soát import lạ trước khi commit file này.
