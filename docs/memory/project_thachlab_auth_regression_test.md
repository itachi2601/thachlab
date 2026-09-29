---
name: project_thachlab_auth_regression_test
description: "Kiểm hồi quy đăng nhập 3 vai (HS/GV/admin) sau đợt tối ưu AuthProvider 26/9/2026 — PASS hết, quy trình test an toàn cho lần sau"
metadata:
  node_type: memory
  type: project
  originSessionId: b58df4c0-6421-486c-bbed-06f9484d52e0
  modified: 2026-09-26T11:14:32.605Z
---

Sau 2 đợt tối ưu tốc độ (perf 25/9 + perf2, cả hai đều động vào AuthProvider) mà chưa ai kiểm bằng tài khoản đăng nhập thật. Thầy yêu cầu gọi 3 agent song song đăng nhập 3 vai — học sinh làm 1 đề, giáo viên xem gradebook + phụ đạo, admin vào đăng đề — cộng thêm trang Rank và 1 trang CNC.

**Kết quả (26/9/2026): PASS toàn bộ, không phát hiện lỗi do AuthProvider mới.**
- HS: đăng nhập → `/tai-khoan` → làm đề `id=96` (Bài 2. Thang nhiệt độ, lớp 12) → nộp, chấm điểm, trang kết quả đúng → trang Rank `/lop-hoc/xep-hang` ghi nhận đúng +RP.
- GV: đăng nhập → `/dashboard-thpt` → tab Bảng điểm (208 lượt làm lớp 12, dữ liệu thật) → tab Phụ đạo (46 HS cần phụ đạo) → Phân tích/Cảnh báo đều render đúng.
- Admin: đăng nhập → `/quan-tri/dang-de` (dropdown Lớp→Chương tự nạp đúng dữ liệu, không bấm nút Đăng để tránh ghi dữ liệu thật) → trang CNC `/quan-tri/cnc-bai-hoc` render đúng 7 bài CNC thật.
- Phát hiện phụ (không phải bug): khi phiên bị lẫn tài khoản khác, app fail-safe đúng (hiện "cần đăng nhập"/"không đủ quyền", không crash, không lộ dữ liệu).

**Cách làm an toàn (áp dụng lại được cho lần kiểm hồi quy sau):**
1. KHÔNG được gõ mật khẩu thật vào site production (an toàn: chỉ localhost). Tạo 3 tài khoản test throwaway bằng script kiểu `scripts/create-accounts-hien.mjs` (service role key), gán role/track/admin_area qua `profiles`, gán lớp thật qua `user_classes` (HS) và `class_instructors` (GV) — dùng lớp có sẵn nhiều dữ liệu thật (lớp 12 = class_id 18, 93+ HS active) để gradebook/phụ đạo có gì mà xem. Xoá tài khoản + `exam_attempts`/`user_classes`/`class_instructors` liên quan ngay sau khi xong (không để rác trong DB thật).
2. KHÔNG chạy dev server ở thư mục chính nếu đã có server khác đang chạy (kiểm bằng cách gọi `preview_start` — nếu báo "Another next dev server is already running" nghĩa là phiên khác đang dùng, đừng kill). Thay vào đó tạo git worktree riêng (`git worktree add .claude/worktrees/<tên> HEAD`), copy `.env.local`, và **dùng `cp -al node_modules` (hardlink) thay vì symlink** — xem [[project_thachlab_perf_optimization]] mục Turbopack root. Chạy `npm run dev -- -p <port khác>` trong worktree đó bằng Bash nền, rồi dùng `navigate` thẳng tới `http://localhost:<port>` (không cần sửa `.claude/launch.json` dùng chung — sửa file đó có thể đụng phiên khác).
3. **Đừng chạy nhiều agent song song đăng nhập các vai khác nhau trên CÙNG một origin/port** — Supabase lưu session trong `localStorage` theo origin, dùng chung giữa mọi tab, nên agent này đăng nhập sẽ đá văng phiên của agent kia dù mỗi agent dùng `tabId` riêng. Hậu quả từng thấy: mất tiến độ làm bài giữa chừng (không phải bug ExamRunner, chỉ là bị đăng xuất/đăng nhập lại). Cách xử lý: chạy 3 agent song song vẫn tạm chấp nhận được để lấy tín hiệu nhanh (app fail-safe đúng, không crash), NHƯNG phải test lại từng vai một lần nữa RIÊNG LẺ (1 agent/1 phiên, không ai khác đăng nhập cùng lúc) trước khi kết luận chắc chắn không có lỗi thật — đã làm vậy với vai HS (`localStorage.clear()` rồi đăng nhập lại 1 mình, làm/nộp đề sạch, không còn hiện tượng mất phiên).

**Phát hiện phụ đã tách việc riêng (task_781e8105):** nút đáp án A/B/C/D trong ExamRunner có vẻ re-render rất thường xuyên trong lúc làm bài (nghi đồng hồ đếm ngược cập nhật state ở cấp cha mỗi giây) — không phải bug chức năng, nhưng đáng xem lại hiệu năng.

**Why:** đợt tối ưu 2 (perf2) sửa AuthProvider mà chưa ai test bằng tài khoản thật — nếu có bug thì mọi học sinh/GV đều dính ngay khi vào lớp học lại (5/10). Cần quy trình test lặp lại được, an toàn (không đụng dữ liệu thật, không đụng phiên khác).
**How to apply:** khi cần kiểm hồi quy đăng nhập/quyền lần sau (đổi AuthProvider, đổi RLS, đổi role logic): làm lại đúng quy trình 3 bước trên; đọc thêm [[project_thachlab_concurrent_sessions]] (kiểm tra git trước khi động vào working tree chung) và [[project_thachlab_perf_optimization]] (kỹ thuật worktree + các lỗ hổng RLS liên quan).
