---
name: project_thachlab_specialist_badge_design
description: "Bộ huy hiệu PNG cho 32 danh hiệu chuyên môn (kind specialist) — ĐỦ 96/96 từ 28/9/2026, bản đầy đủ ở ~/Downloads/thachlab-huy-hieu-96/; 13 danh hiệu bộ sưu tập/thành tích chưa có ảnh"
metadata:
  node_type: memory
  type: project
  originSessionId: 687a8f62-4ed0-4aeb-bcb5-3b02e90927b5
  modified: 2026-09-27T17:56:26.074Z
---

Có Artifact "Design System" tên **ThachLab Huy Hiệu** (https://claude.ai/artifact/NeuGnhubmbeFQi1ZxZZRTR) chứa quy tắc vẽ
huy hiệu PNG phong cách MOBA/RPG (kim loại + năng lượng vũ trụ, khung lục giác, 1024×1024 nền trong suốt) cho:
- 7 huy hiệu rank (đã xong, xem [[project_thachlab_rank_badge_medal]]).
- 32 danh hiệu chuyên môn (kind `specialist` trong `features/rank/types.ts`, 5 nhóm: Cơ học, Dao động & Sóng, Điện & Từ,
  Nhiệt học, Vật lý hiện đại) × 3 cấp Thức Tỉnh/Làm Chủ/Huyền Thoại = 96 PNG khi xong. Mới có 6 danh hiệu × 3 cấp = 18 PNG
  (Newton, Động Lượng, Giao Thoa, Điện Trường, Từ Trường, Hạt Nhân). 28/9/2026 đã bổ sung spec (slug `cm-<ten>` + mô tả
  biểu tượng) cho 26 danh hiệu còn lại vào `project/README.md` của design system, sẵn sàng vẽ tiếp.

**Why:** 18 PNG đầu được vẽ trên **Cowork** (nơi có công cụ sinh ảnh) — Claude Code không có công cụ sinh ảnh nên không tự
vẽ PNG được, chỉ viết được spec/thiết kế văn bản.

**How to apply:** Khi thầy nhờ "vẽ tiếp huy hiệu chuyên môn" / "làm nốt 26 danh hiệu còn lại" trong phiên Claude Code, nói
rõ giới hạn này và hướng thầy mở lại design system trên Cowork để sinh ảnh theo đúng spec đã ghi (đừng tự bịa PNG hay đổi
hướng sang SVG code nếu không được yêu cầu — SVG khác hẳn phong cách PNG kim loại/MOBA đã chốt). Nếu thầy muốn dùng ngay
trong code trước khi có đủ PNG, TitleCollection.tsx (`components/rank/TitleCollection.tsx`) hiện dùng icon chung
Sparkles/Lock — đó là chỗ sẽ gắn 96 PNG này vào khi đủ.

**28/9/2026 (sau) — ĐỦ BỘ 96 PNG:** thầy vẽ nốt 26 danh hiệu trên Cowork (tải về từ asset store của design system,
ánh xạ tên↔blob nằm trong `project/design-system.json` → `assetGroups.ChuyenMon.files`; đọc asset bằng Artifact read
`path=<asset id>` từng cái, `paths` KHÔNG nhận asset id). Đã soát: 96/96 1024×1024 RGBA nền trong suốt, phong cách khớp.
Trọn bộ 96 + 7 rank lưu ở `~/Downloads/thachlab-huy-hieu-96/` (thư mục mới, không đụng _2). Mockup
https://claude.ai/artifact/WdsCPm7LFMSGEwvnnxCEtG v2 đã dùng ảnh thật. Còn thiếu ảnh: 13 danh hiệu bộ sưu tập/thành tích.
Bảng slug → `rank_titles.code` CHƯA có (anon key không đọc được rank_titles) — lấy lúc code bước 1 ở [[project_thachlab_title_showcase]].

**2026-09-28 (cuối phiên):** spec 13 danh hiệu còn thiếu ĐÃ ghi vào `project/README.md` của design system (v12):
6 bộ sưu tập `bst-<slug>` (khung lục giác kép vàng + nguyệt quế + vương miện, lõi màu theo nhóm; `bst-vu-tru` khung bạch kim
hào quang 5 màu) và 7 thành tích `tt-<slug>` (huy chương TRÒN viền đinh tán xanh thép `#9fb4d8`, ruy-băng chữ V, mỗi cái
một biểu tượng/màu nhấn). Slug ↔ `rank_titles.code` nằm ở `SINGLE_SLUG` trong `features/rank/badge-assets.ts` (repo).
Ảnh chuyên môn trên web dùng bộ của PR #15 (`public/images/rank/titles`, 512px), KHÔNG phải bộ 96px em từng ép — đã xoá.
Cách tải asset từ design system trong Claude Code: Artifact read `path=<asset id>` từng cái (`paths` không nhận id),
ánh xạ tên↔id ở `project/design-system.json` → `assetGroups.<Group>.files`.
