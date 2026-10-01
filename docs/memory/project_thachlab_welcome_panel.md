---
name: project_thachlab_welcome_panel
description: Bảng chào mừng theo vai + gợi ý theo số liệu (HS THPT, GV THPT) — đã merge + deploy 2026-09-30
type: project
---
# Bảng chào mừng theo vai (2026-09-30)

**Mục tiêu:** khi HS/GV/admin/trợ giảng/phụ huynh đăng nhập ThachLab, thấy lời chào + việc nên làm đầu tiên theo đúng vai.

**Đã xong — ĐÃ MERGE + DEPLOY (2026-09-30):**
- PR https://github.com/itachi2601/thachlab/pull/17 merge vào main tại `f865285` (kiểu merge). Nhánh làm việc `claude/inspiring-mendel-6k34x0`.
- Build từ main OK (70 trang, 116 bài/257 mục; chỉ khóa anon trong bundle), `scripts/deploy.sh` force-push nhánh `deploy` 43879bd→553c80f. Hosting cron kéo trong ≤10 phút. Có cảnh báo git "push negotiation failed" nhưng push vẫn thành công (gửi full).
- Chi tiết code:
- Commit `e5ef009` — `components/account/WelcomePanel.tsx` (mới, 11 tình huống: student_new, thpt_pick_class/pending/active, cttc_join/pending/active, instructor, admin, tro_giang, parent) + gắn vào `Account()` ở `app/tai-khoan/page.tsx` (body chuyển thành IIFE `body`, biến `variant` tính từ track + enrollment + classRequest).
- Commit `9ea403e` — `components/dashboard/ThptStudentHome.tsx`: gợi ý ngày thêm "Còn X RP là lên {bậc}" khi X≤50; `components/dashboard/TeacherThptOverview.tsx`: khối "Nên làm trước" (cảnh báo khẩn/phụ đạo, HS chưa làm bài, chưa có buổi điểm danh).
- tsc + eslint sạch (sau `npm ci`). CHƯA chạy app / chưa xem trên trình duyệt / chưa test bằng tài khoản thật.

**Quyết định thiết kế (không suy ra được từ code):**
- Không thêm truy vấn Supabase mới, không migration — theo quy tắc perf trong AGENTS.md; chỉ dùng dữ liệu component đã tải.
- Đóng bảng lưu localStorage key `thachlab_welcome_off_<userId>_<variant>` → đổi tình huống thì bảng hiện lại.
- Render lần đầu coi như đã đóng (useSyncExternalStore, server snapshot=true) để không chớp.
- Route đã kiểm tồn tại: /lop-hoc, /lop-hoc/xep-hang, /lop-hoc/ket-qua, /khoa-hoc, /dashboard-thpt, /quan-tri, /quan-tri/dang-de, /phu-huynh, /tro-giang, /thong-bao, /bao-loi-cua-toi. `/kiem-tra` KHÔNG có page (chỉ /kiem-tra/lam).
- Trợ giảng (role tro_giang) đang đi qua luồng học sinh trong Account(); bảng tro_giang hiện phía trên.

**Còn chờ / chưa làm:**
- Kiểm bằng mắt trên web thật từng vai sau deploy (chưa ai xem): HS THPT, CTTC, GV, admin ("Xem như học sinh"), phụ huynh, trợ giảng.
- Gợi ý theo số liệu thật cho phụ huynh (tóm tắt tuần của con), admin (lời mời GV chưa nhận, báo lỗi mới, nghi trùng), CTTC — cần RPC gộp = migration mới (phải viết file + thêm vào `scripts/run-migrations.sh` + ghi ĐANG CHỜ trong `docs/STATE.md`, không tự chạy).
- Số bài tự luận chưa chấm cho GV: chưa tìm thấy nguồn dữ liệu sẵn.
- `docs/STATE.md` ĐÃ ghi đợt này (PR #18, main `cff75f3`, 2026-09-30) — phiên Mac đọc được qua `git pull`.
- File memory này chỉ nằm trong container đám mây; đã gửi bản sao cho thầy chép vào `~/.claude/projects/-Users-MAC-Projects-thachlab/memory/` trên Mac (chưa biết thầy đã chép chưa).
