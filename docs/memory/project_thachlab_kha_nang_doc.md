---
name: project_thachlab_kha_nang_doc
description: "Đợt rà khả năng đọc/tương phản WCAG 02/10/2026 — P0 (phiên khác) + P1/P2 (phiên này) đã vào main; chuẩn ở docs/UI.md, kiểm bằng npm run check:a11y"
metadata:
  node_type: memory
  type: project
  originSessionId: 63f37369-bb37-41b6-b78c-8e8808867ae8
  modified: 2026-10-02T16:32:13.342Z
---

**Bối cảnh (02/10/2026):** thầy đưa một bản nhận xét WCAG về giao diện (nút `#3b82f6` 3,68:1, `text-slate-500`
3,98:1, chữ 7–11px, eyebrow IN HOA, gradient text, không có `prefers-contrast`, `docs/UI.md` rỗng). Tôi đối chiếu:
đúng về bản chất; sai 1 điểm kỹ thuật (Tailwind **v4** → `slate-500` = `#62748e`, và theme sáng đã override
`.text-slate-500` nên lỗi chỉ ở theme tối), phóng đại 2 chỗ (eyebrow chỉ thuộc module CNC; violet 4,76 trên nền
trang vẫn đạt AA ở theme tối, trượt ở theme sáng vì selector `text-violet-` không khớp token `text-violet`).

**Đã làm, đều vào `main`:**
- P0 (phiên khác, commit `4ad013dd0`): token `--color-primary` #2563eb, `--color-slate-500` #7c8ba1, chữ xanh tách
  theo theme (`[class*="text-primary"]` tối #60a5fa / sáng #1d4ed8).
- P1+P2 (phiên này, commit `2ada3eadd`): sàn chữ 12px (193 `text-[≤11px]` + 63 rule CSS), eyebrow CNC 13px/.08em,
  `/phu-huynh` mặc định theme sáng khi chưa lưu lựa chọn (script inline `app/layout.tsx`), chữ gradient → màu đặc
  (`--accent-brand-text`/`--accent-warm-text`), `components/ui/ReadingZone.tsx` (A−/A+ đặt font-size `<html>`,
  Dịu mắt = theme sáng + `html.is-dim`) gắn ở `/phu-huynh` và `/kiem-tra/lam`, `@media (prefers-contrast: more)`
  + `forced-colors`, `docs/UI.md` chuẩn + `scripts/check-a11y.mjs` (`npm run check:a11y`).

**Chưa kiểm được / còn treo:**
- ReadingZone chỉ xem được khi đăng nhập (không có tài khoản thử, 3 tài khoản test 26/9 đã xoá) → mới kiểm CSS
  bằng cách chèn markup tay ở trang khách + tsc/eslint; cần thầy đăng nhập xem thật ở `/phu-huynh` và một đề.
- Chưa xem từng chỗ trong 193 nhãn vừa phóng 10/11→12px có tràn ô không (admin, rank, trợ giảng). Trang chủ, bài học
  và `/phu-huynh` khách ở 375px không thấy vỡ.
- Thầy chọn KHÔNG làm chung P0 trong phiên này (phiên khác làm). Việc còn theo nhận xét: `text-violet` token ở
  theme sáng (42 chỗ, 4,23:1) chưa sửa.

**How to apply:** trang/khối mới → đọc `docs/UI.md`, chạy `npm run check:a11y` trước khi báo xong; không viết
`text-[<12px]`, không gradient text, màu nhấn phải có 2 giá trị theo theme. Trang đọc lâu → bọc `<ReadingZone>`.
Liên quan: [[feedback_mobile_first_ui]], [[project_thachlab_lesson_ui_redesign]].
