---
name: thachlab-paragon-badge
description: "Huy hiệu độc quyền Vô Song (Paragon) trên Chí Tôn — 26/9/2026 ĐÃ gắn vào UI + chế độ Xem như học sinh mở khoá hết (features/rank/preview.ts); migration rank_paragon ĐÃ chạy, commit aaf7e464 đã push main + deploy 26/9/2026; thầy chưa xác nhận trên web thật"
metadata:
  node_type: memory
  type: project
  originSessionId: a20bf812-ac19-4b9e-a4be-20a057f1a0b1
  modified: 2026-09-26T03:38:16.136Z
---

Thầy yêu cầu (26/9/2026): giả định HS đạt trọn bộ danh hiệu + vượt mọi bậc → thiết kế 1 huy hiệu độc quyền.

**Đã làm:** trang thiết kế "Huy hiệu Vô Song" https://claude.ai/artifact/1uWukFBD9cnqCR1Je1SS9D
(hero, so với 7 huy chương thật, cạnh Chí Tôn, giải phẫu, các cỡ, điều kiện đề xuất, 3 tên).
Component `components/rank/ParagonBadge.tsx` (untracked, chưa import ở đâu, tsc sạch) — cùng viewBox
240×280 crop 28..212 với RankBadge, props `size`, `animate`.

**Thiết kế đã chốt trong bản vẽ:** tên Paragon · Vô Song (phương án khác: Eternal · Vĩnh Hằng, Zenith · Đỉnh Thiên).
Đại huân chương đeo cổ: dây chuyền vàng–bạch kim hai bên ruy-băng · ruy-băng men huyền sọc cực quang
(teal→tím→hồng→vàng, animate 9s) · hoa hồng men huyền + 2 thanh cài bạch kim đính 3 sao vàng · vương miện kín
có vòm + quả cầu + sao · gươm chéo bạc · nguyệt quế vàng · 32 tia (16 dài vàng / 16 ngắn bạch kim) ·
đôi cánh vàng vẽ ĐÈ LÊN tia, luồn dưới men (vẽ dưới tia thì bị che) · 12 kim cương quanh men ·
men huyền obsidian với NGUYÊN TỬ (3 quỹ đạo bạch kim, 3 electron vàng, hạt nhân sáng xoay chậm 24s).
Dưới 40px bỏ halo/bóng/animation như RankBadge.

**Chưa làm (chờ thầy duyệt):** nối vào RankBadge (cờ paragon), TierName, RankAvatarFrame, TierLadder ô thứ 8,
cột `is_paragon` + điều kiện trong rank_tier_info (viết migration file, thầy tự chạy). Điều kiện đề xuất:
đang Chí Tôn + 45/45 danh hiệu mức cao nhất + (duy nhất trong lớp HOẶC giữ tới hết mùa) — thầy chọn.
Lưu ý: 4 danh hiệu chưa gắn chủ đề (Photon, Nguyên tử, Máy biến áp, Cân bằng nhiệt) phải kích hoạt trước,
nếu không không ai đạt 45/45.

**How to apply:** muốn sửa hình → sửa ParagonBadge.tsx, render lại bằng react-dom/server (script phải nằm
trong repo để resolve node_modules), thay vào template rồi republish artifact. Browser pane đăng nhập tài
khoản caothang nên không mở được artifact private của itachi2601 → soát bằng Chrome headless chụp file local.
Xem thêm [[thachlab-rank-badge-medal]], [[thachlab-rank-system]].

**26/9/2026 (phiên 2, bị cắt vì hết hạn mức):** thầy bảo "gắn lên + mở khoá hết năng lực cho trang xem thử".
ĐÃ LÀM (tsc + eslint sạch, SSR render OK, CHƯA commit, CHƯA test trình duyệt thật):
- `features/rank/types.ts`: `RankTierInfo.paragon?`, `PARAGON_META`, `tierMeta(code, paragon)`, `tierLabel(..., paragon)`.
- `features/rank/preview.ts` (mới): `isStudentPreview()` (sessionStorage "thachlab_preview_as_student"==="1", KHÔNG áp cho cttc),
  `unlockStatus/unlockTitles/unlockBoard/unlockSeasons` — services/rank.ts gọi sau RPC → admin "Xem như học sinh"
  thấy Vô Song, 999 RP, 45 danh hiệu Huyền Thoại, chuỗi 30 ngày, đứng đầu bảng tuần. Tài khoản Thạch ở lớp 18, season 4 nên /tai-khoan render ThptStudentHome.
- RankBadge `paragon` → ParagonBadge; TierName, RankCard, RankAvatarFrame (vành cực quang), RankPage, ClassRankBoard, TierLadder (ô thứ 8 tách vạch, panel điều kiện).
- Migration `supabase/migrations/20260926100000_rank_paragon.sql` + rollback `perf/rollback/…down.sql`: hàm `rank_is_paragon`
  (mọi danh hiệu enabled khả dụng: specialist mức huyen_thoai, còn lại có award) + cờ trong rank_status_of / rank_class_board.
  Đã thêm vào FILES của scripts/run-migrations.sh (file 6) + docs/STATE.md.
CÒN LẠI: thầy test trình duyệt (bật Xem như học sinh → /tai-khoan, /lop-hoc/xep-hang, mobile 375), commit đúng phạm vi
(git diff HEAD soát WIP lạ ở ThptStudentHome — KHÔNG đụng file đó), deploy, chạy migration.

**26/9/2026 (phiên 3):** thầy đã chạy migration (rank_status_of trả `paragon:false` OK). Commit `aaf7e464` (chỉ file rank + migration + STATE.md/run-migrations.sh),
push main, build từ deploy-tree tại commit đó, push nhánh deploy (ea38992). Chưa test trình duyệt thật (browser pane không đăng nhập thachlab) —
thầy tự bật "Xem như học sinh" xem /tai-khoan + /lop-hoc/xep-hang. Điều kiện "duy nhất trong lớp" vẫn chưa có trong SQL.
