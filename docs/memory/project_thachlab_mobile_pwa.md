---
name: project-thachlab-mobile-pwa
description: GĐ 2.6 Mobile PWA (M1 vỏ PWA, M2 Luyện nhanh 10 câu, M3 offline, M4 Web Push) — code đã vào main + deploy 2026-10-06, chưa thử thiết bị thật
metadata:
  type: project
---

Biến site `output: "export"` thành PWA cài được, KHÔNG làm app native (mốc "mobile app khi ≥500 HS/tuần" ở GĐ 6 giữ nguyên). Spec đã đối chiếu code: `docs/BAN-GIAO-MOBILE-PWA-2026-10-05.md`; mục GĐ 2.6 trong `docs/ROADMAP.md`.

**Quyết định đã chốt (đề xuất gốc sai, đã sửa)**: không có URL `/luyen-tap?...&so=10`, không có RPC `get_practice_questions`/`get_weak_skills` — RPC thật là `get_my_weakest_topics`; chế độ "Từng câu" (`PracticeStepView`) và streak đóng băng (migration 20260930130000) ĐÃ có từ trước; `MobileTabBar` 4 tab giữ nguyên; service worker viết tay (không serwist), `/data/*` network-first vì `services/static-content.ts` tự đối chiếu Supabase.

**Đã xong (trên main, deploy nhánh `deploy` f585f90 ngày 2026-10-06)**
- M1: `app/manifest.ts`, `public/icons/*` (sinh bằng `scripts/gen-pwa-icons.mjs`), `public/sw.js`, `components/pwa/PwaBoot.tsx` + `PwaInstallBanner.tsx`, `lib/pwa-install.ts` (`markFirstPracticeDone()` gọi ở `PracticeSession` + `TopicPracticeModal`). Commit 2bbc1ea4b, 9cd6c3388, bc6f370ce.
- M2: nút "Luyện nhanh 10 câu" ở `components/mastery/WeakestSkillsCard.tsx` (commit 297e1aa99), mở `TopicPracticeModal` count=10.
- M3: `lib/offline-queue.ts`, `components/pwa/OfflineSync.tsx`, `savePracticeSession` xếp hàng khi lỗi mạng (idempotent qua `practice_sessions.client_token`, có unique index), test `npm run test:offline-queue`. Commit 108cf62c9.
- M4: migration `20261005160000_push_subscriptions.sql` ĐÃ CHẠY 2026-10-06 (cùng `20261005140000_weakest_topics.sql`); secrets VAPID đã đặt; Edge Function `send-daily-push` đã deploy (secret đúng → `due:0`, sai → 401); pg_cron job `send-daily-push` mỗi giờ đang active; `NEXT_PUBLIC_VAPID_PUBLIC_KEY` trong `.env.local` (build deploy-tree cũng đã có). Thẻ bật nhắc: `components/pwa/DailyReminderCard.tsx` ở `/tai-khoan`. Hướng dẫn: `docs/PUSH-NHAC-HANG-NGAY.md`. Bản sao khoá VAPID + PUSH_CRON_SECRET nằm ở scratchpad phiên (có thể mất) — nếu cần gọi function ép gửi, lấy secret mới bằng `supabase secrets set` lại hoặc đặt lại cron.

**Còn chờ**
- KHÔNG ai thử trên thiết bị thật: banner cài app ở 375px, cài Android + iPhone, Lighthouse PWA, nút "Luyện nhanh" với HS có kỹ năng yếu, hàng đợi offline xả lên Supabase thật, push thật (bật nhắc ở `/tai-khoan` → đặt giờ = giờ hiện tại → curl function → chạm tin mở `/lop-hoc/`). ROADMAP đã tick M1–M3, M4 vẫn `[ ]` cho tới khi push thật chạy.
- Màn luyện vẫn hiện "đã lưu" khi kết quả mới chỉ nằm trong hàng đợi offline (chưa sửa `PracticeSession` để hiện "sẽ gửi khi có mạng"; thanh chỉ báo chung có sẵn).
- Rủi ro đã biết: `npm:web-push` chạy được trên Edge (đã thử); gửi lỗi tạm thời = mất nhắc ngày đó; đổi khoá VAPID = mọi đăng ký cũ vô hiệu; vị trí chỉ báo offline (4,75rem trên thanh đáy) chưa xem ở 360/375px.
- Đợt 2 sau ra mắt (chưa làm): chụp ảnh bài → AI Tutor (GĐ 4), thẻ chia sẻ lên hạng, tin tuần cho phụ huynh, mô phỏng nghiêng điện thoại, QR điểm danh lớp Cao Thắng.
- `stash@{0}` "wip-pre-pwa-merge" (2 file PracticeSession/TopicPracticeModal) còn trong stash; working tree hiện không còn sửa dở 2 file đó — xem lại rồi `git stash drop` nếu thừa.

Bài học vận hành: brief để uncommitted thì agent trong worktree không đọc được → commit brief trước khi giao; worktree thiếu `node_modules` thì `cp -Rc` (Turbopack không nhận symlink) hoặc `next build --webpack`; không chạy `npm ci` trong deploy-tree ngay trước `deploy.sh` (build lỗi font); `git merge` nhớ `--no-edit` để khỏi treo vim.
