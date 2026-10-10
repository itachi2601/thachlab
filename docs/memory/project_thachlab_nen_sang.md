---
name: project_thachlab_nen_sang
description: "Nền SÁNG (trắng) là mặc định toàn site từ 11/10/2026: bảng màu light-first trong globals.css, khác biệt theo lứa tuổi (HS 14–18 / PH 45–60 / GV-quản trị), dọn ~112 file màu nền tối hard-code, trang xem thử /dev/giao-dien, công cụ đo bố cục scripts/do-bo-cuc.mjs"
metadata:
  node_type: memory
  type: project
  modified: 2026-10-10T06:20:00.000Z
---

**Thầy chốt 11/10/2026:** "thiết kế giao diện trắng của trang thachlab phù hợp với thị giác lứa tuổi
từng trang, hiện tại màu sắc khá không đẹp" → chọn: nền sáng làm mặc định **toàn site**, nền tối giữ
làm **tuỳ chọn**, và làm tới mức "bảng màu mới + sửa hết chỗ màu chỏi trên các trang chính".

## Vì sao cũ không đẹp (nguyên nhân thật)
Mặc định là nền tối "deep space"; chế độ sáng chỉ là ~300 dòng `!important` vá lên class tối. Khi bật
sáng: (1) hàng trăm chỗ JSX hard-code `bg-[#0B1020]`, `bg-white/5`, `border-white/10`, gradient
`from-[#172c46]`, quầng sáng `shadow-[0_0_24px…]` → **mảng tối lẫn trong trang sáng**; (2) nhiều sắc
độ bão hoà cùng màn hình (cyan + violet + amber + emerald) → vi phạm M3; (3) gradient/quầng sáng ở
vùng đọc (M6). Nền tối không sai về kỹ thuật — sai ở chỗ nó là mặc định cho trang đọc dài (M1).

## Đã làm
- **`app/globals.css`**: đảo tầng token — khối `@theme` = NỀN SÁNG (mặc định, `--color-bg:#f5f7fa`);
  `html[data-theme="dark"]` = nền tối (giữ bảng "deep space" cũ). Token mới: `surface-2`,
  `line-strong` (`#8b93a1` = 3,2:1 — WCAG 1.4.11 cho viền ô nhập; xám nhạt `#cfd6e0` chỉ 1,5:1 nên
  không dùng được), `ok/warn/danger`, `primary-soft`. Bỏ gradient + quầng sáng ở hero/competency-path.
- **Theo nhóm người xem** (cùng hệ màu, chỉ khác số đo — đổi màu theo trang là phá M3/N4):
  `.parent-page` (PH 45–60): nền ấm `#f7f7f4`, chữ phụ `#3d4653` **8,9:1 (AAA, P2)**, nhấn navy
  `#1e40af`, viền ô nhập `#767f8d`, trạng thái `#065f46/#78350f/#991b1b` (đều ≥7:1);
  `.teacher-dashboard`/`.admin-shell`: nền trung tính `#f4f5f7`, cỡ chữ gốc 14px (mật độ cao).
  **Bẫy đã dính:** token của `.parent-page` đặt trên phần tử con sẽ đè token của `html.is-dim` →
  phải bọc trong `html:not(.is-dim)` kẻo vô hiệu hoá chế độ "Dịu mắt" của người lão thị.
- **Mặc định theme**: `app/layout.tsx` (`data-theme="light"`, bỏ `prefers-color-scheme`,
  `statusBarStyle:"default"`, `themeColor:#f5f7fa`), `components/ui/ReadingZone.tsx`,
  `components/layout/ThemeToggle.tsx` (snapshot SSR = light + tự cập nhật `meta theme-color`),
  `app/manifest.ts`. Chỉ đổi sang tối khi người dùng **đã tự chọn** (`thachlab-theme` trong localStorage).
- **Dọn ~112 file component** theo bảng quy đổi (`text-white`→`text-ink` nhưng GIỮ `text-white` trên
  nền màu đặc; `bg-white/5`→`bg-surface-2`; `border-white/10`→`border-line`; viền ô nhập →
  `border-line-strong`; bỏ gradient/glow/neon). 5 phiên con chia theo nhóm trang.
- **Lưới an toàn cuối `globals.css`**: quét nốt idiom cũ còn trong JSX (attribute selector không
  phân biệt hoa/thường `[class*="bg-[#05070b]" i]`, `[class~="bg-white/10"]` để không đụng
  `hover:bg-white/20`). Không phải nguồn màu — xoá dần khi component đã sạch.
- **Trang xem thử `/dev/giao-dien`** (`?theme=dark`, `?aud=parent|teacher`): bảng token + bộ dựng
  (nút/thẻ/ô nhập/tab/bảng/trạng thái). Duyệt màu ở đây thay vì soi từng trang.
- **Công cụ**: `scripts/check-a11y.mjs` (bổ sung cặp đo nền sáng + PH AAA), `scripts/kiem-doi-mau.mts`
  (bỏ mọi chuỗi rồi so HEAD → chứng minh "chỉ đổi class"), `scripts/do-bo-cuc.mjs` (chụp + đo bố cục
  bằng device emulation), ảnh kiểm chứng ở `docs/anh/giao-dien-nen-sang/`.
- **Tài liệu**: `docs/MAU-NEN-SANG.md` (nguồn chính: token + số đo + bảng quy đổi + việc còn treo +
  nhật ký rút kinh nghiệm), `docs/UI.md` §1–2/§5 (bảng token mới + cách chụp 375px), thêm **M7** vào
  `docs/QUY-TAC-THIET-KE.md`.

## Kiểm chứng
`npm run check:a11y` ĐẠT (0 cặp màu lỗi; 0 chỗ chữ <12px — đã nâng 4 chỗ có sẵn); `npx tsc --noEmit`
sạch; `npx next build` xanh; ảnh 375/1440 hai theme không tràn (`scrollWidth = viewport`).

## Trạng thái deploy
`deploy` = `9077fbd47` (build 13:11 10/10 từ `main` @ `b37f7c7dc`), hosting cron kéo trong ~10 phút.
Deploy chạy từ **worktree sạch** `.claude/worktrees/deploy-nen-sang` tại HEAD (không đụng WIP
untracked của phiên khác: `components/quiz-live/`, `app/tro-giang/do-vui/`, `app/(public)/choi/` —
đã kiểm bản deploy không có các path này). Migration `20261010400000/410000/420000` + `hsg_cham_nhanh`
do phiên khác chạy lúc 13:08 (log `scripts/logs/20261010-130800-*`).

## Còn treo
Canvas mô phỏng vẫn vẽ nền tối trong theme sáng (màu trong JS, như canvas); màu bậc rank trong
`features/rank/types.ts`; màn ăn mừng + toast "Lên hạng!" cố ý giữ nền tối (L3); M4 thiếu ở
`QuestionCard` chế độ xem lại câu Đúng/Sai (chỉ hiện bằng màu); còn `StudentAttendancePanel`,
`StudentFinalGradeCard`, `PwaInstallCard`, `StudentCodeField`, `QuickPractice` dùng idiom nền tối
(lưới an toàn đang che); `text-slate-600/700` chưa có token.

## Bài học (chi tiết + ngày ở `docs/MAU-NEN-SANG.md` §8 và `AGENTS.md`)
- `chrome --headless --window-size=375,812` **không** cho viewport 375px (vẫn dàn ~500px rồi cắt ảnh)
  → suýt sửa một lỗi "tràn ngang" không tồn tại. Dùng `scripts/do-bo-cuc.mjs`.
- Hai phiên cùng một cây làm việc: `git commit -a` nuốt thay đổi chưa commit của phiên kia, và có thể
  nuốt **một phần** file (`globals.css` của đợt này từng bị commit nửa vời vào commit của phiên khác)
  → commit theo đường dẫn cụ thể, chia mẻ nhỏ, `git log -S '<chuỗi>' -- <file>` khi thấy lạ.
- Kiểm chứng "chỉ đổi màu" bằng máy (`scripts/kiem-doi-mau.mts`): nhớ bỏ cả chuỗi trong `${…}` của
  template literal, nếu không báo động giả hàng loạt.

Liên quan: [[project_thachlab_kha_nang_doc]], [[project_thachlab_lesson_ui_redesign]],
[[project_thachlab_phu_huynh_ui]], [[feedback-deploy-autonomy]], [[feedback-thachlab-deploy-scope]].
