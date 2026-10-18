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

**2026-10-18/19 — Push THÔNG BÁO (kiểu Duolingo), đã deploy**
- Mọi dòng mới ở `notifications` được đẩy ra màn hình khoá + rung. Migration `20261018150000_push_thong_bao.sql` (cột `pushed_at`, hàm `claim_notification_pushes`: ≤3 push/ngày/em, chỉ 6–22h VN, tin >30 phút bỏ, mỗi lượt 1 tin mới nhất/em) và `20261018160000_push_nhac_lui_dan.sql` (nhắc luyện hằng ngày lùi dần: ngày 0–3 mỗi ngày, rồi 5/7/14, quá 14 thôi) ĐÃ chạy. Edge Function `send-notification-push` + `send-daily-push` (luân phiên 3 mẫu tin, đổi giọng khi lâu chưa học, `message.ts`) ĐÃ deploy. Web (sw.js v5 rung + postMessage, `NotificationBell` popup + vibrate, `PushOptInPrompt` sau 25 giây, "Để sau" nhớ 14 ngày) đã push nhánh deploy 2026-10-18.
- Cron: `send-notification-push` `* 23,0-14 * * *` UTC (= 6h–21h59 VN), tạo bằng cách sao `command` của job `send-daily-push` (secret nằm sẵn trong đó, không cần nhập); `don-cron-log` 20h30 UTC dọn `cron.job_run_details` >3 ngày. Gọi thử trả 200 `{"due":0}`. Doc: cuối `docs/PUSH-NHAC-HANG-NGAY.md`.
- Quyết định: giọng nhẹ, KHÔNG dọa mất chuỗi (SDT, nghiên cứu HS 14–18); chưa dùng bandit (Duolingo KDD20) vì chưa đủ dữ liệu; thông báo sự kiện không luân phiên mẫu (nội dung thật từ trigger).
- CÒN CHỜ: chưa thử push thật. Đăng ký iPhone của thầy đang nằm ở tài khoản `thachngo20212022@gmail.com` (không phải HS Test 1) → nhắn "gửi thông báo thử" SAU 6h VN (ngoài khung tin bị đóng dấu không gửi) thì tạo 1 dòng `notifications` cho tài khoản đó rồi kiểm điện thoại rung/popup. 4 HS thật đã có đăng ký từ trước (push_subscriptions id 14–17) nên cũng sẽ nhận push thông báo từ 6h sáng 19/10 — thầy được báo, chưa quyết tạm tắt cron.
- Chưa làm: nút "Nhắc cả lớp" cho thầy/trợ giảng; chưa kiểm cron `engagement-alerts-sweep` (6h sáng) có tạo thông báo cho HS không; chỉ HS có đăng ký push (giáo viên/phụ huynh chưa); `navigator.vibrate` không chạy trên iOS.
- Bài học: không gọi `claim_push_reminders_due(...) limit 0` để "thử" — hàm ghi `last_sent_at` (dừng kịp bằng Ctrl-C trước khi chạy); SQL phải chạy bằng `supabase db query --linked`, đừng dán vào zsh; `read -s` chỉ chạy trong tab Terminal, không trong khung chat; `profiles` không có cột email (join `auth.users`).
