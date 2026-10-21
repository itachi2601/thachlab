# Khảo sát Pha 0 — Mobile PWA (05/10/2026)

## Đã có sẵn (brief giả định chưa có)
- Thanh đáy HS: `components/layout/MobileTabBar.tsx` (Trang chủ · Lớp học · Luyện tập · Tài khoản), hiện < 1024px,
  tự ẩn ở /quan-tri, /kiem-tra/lam, /lop-hoc/bai, /tro-giang/ghi, /phu-huynh. Brief muốn < 768px, 4 tab Học·Luyện·Lộ trình·Tôi.
- `viewport-fit: cover` đã có (`app/layout.tsx`). Navbar còn menu ☰ trên mobile.
- Streak đóng băng 1 ngày/tuần + mốc reset 3h sáng ĐÃ có: migration `20260930130000_rank_streak_freeze.sql`
  (kiểm xem đã chạy prod chưa ở docs/STATE.md). M4 mục 4 gần như trùng.
- Công thức là KaTeX (không phải MathJax). `output: "export"` + `trailingSlash` đúng như brief.

## Chưa có
- Không có manifest, service worker, icon PWA, `idb`, `web-push`, `analytics_events` (kiểm lại DATABASE.md), `push_subscriptions`.
- `docs/rank-rules.md` không tồn tại; `scripts/worktree.sh` không tồn tại.

## Lệch hợp đồng "Luyện tập 26/09"
- `app/luyen-tap/page.tsx` KHÔNG đọc tham số `lop/chuong/bai/yccd/muc/so/uu_tien` (không có searchParams/useSearchParams).
- Không thấy RPC `get_practice_questions` trong services/ hay migrations; `get_weak_skills` chỉ thấy trong services/mastery.ts (cần xác minh).
  `practice_question_results` và `WeakestSkillsCard` tồn tại. Có thể hợp đồng nằm trên nhánh khác (feat/mastery, chore/gop-luyen-tap), chưa vào main.
- `PracticeSession` hiện ở `components/lessons/PracticeSession.tsx` (554 dòng) + PracticeStepView/RunningView/DoneView, không phải `components/practice/*`.

## Rủi ro
- Working tree main đang có ~100 file WIP của phiên khác (gồm Navbar, MobileTabBar, PracticeSession, globals.css — đúng vùng M1/M2). Worktree mới từ HEAD sẽ không thấy các thay đổi này → xung đột khi merge.
