---
name: project_thachlab_tutoring_exit_quiz
description: "Thoát phụ đạo bằng tự kiểm tra (cách 2 bên cạnh đăng ký buổi học) — đã commit + push 25/9/2026 (gộp vào quy chế trợ giảng, xem [[project_thachlab_ta_policy]]), chưa test UI thật"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0ec98e35-2fd3-4f4d-b29b-7813ba145d23
  modified: 2026-09-26T02:32:44.289Z
---

Thêm cách thứ 2 để học sinh tự gỡ một chủ đề khỏi danh sách "cần phụ đạo"
([[project_thachlab_phu_dao]]) mà không cần chờ trợ giảng: tự ôn rồi làm bài ~20 câu bốc
ngẫu nhiên từ ngân hàng câu hỏi đúng chủ đề đang hổng, đạt ≥ 80% thì DB tự chuyển
`tutoring_needs.status = 'cleared'`. Tối đa 3 lượt/chủ đề (tổng, không theo ngày); nếu ngân
hàng không đủ 20 câu vẫn cho làm với số câu ít hơn.

Đã code xong (23/9/2026):
- `docs/supabase-migration-tutoring-exit-quiz.sql` — bảng `tutoring_exit_attempts` +
  trigger chặn quá 3 lượt/tính pct-passed + trigger tự đóng mục khi đạt + RLS mới trên
  `question_bank` cho học sinh đọc câu đúng chủ đề mình đang cần phụ đạo (trước đó chỉ
  giáo viên đọc được bảng này).
- `services/tutoring.ts` — thêm `fetchMyExitAttempts`, `logExitAttempt`.
- `components/results/TutoringExitQuiz.tsx` — modal làm bài (tái dùng `QuestionCard`,
  `gradeExam`, `pickRandom` có sẵn, không đụng `ExamRunner` vì nó gắn chặt bảng `exams`).
- `components/dashboard/ThptStudentHome.tsx` — thêm đoạn giải thích 2 cách + nút "Tự kiểm
  tra (còn N lượt)" ở mục "Chủ đề cần phụ đạo".

**Why:** chấm điểm vẫn ở client như mọi đề khác trong app (đúng mức tin cậy hiện có của
`ExamRunner`/`PracticeSession` — không có RPC chấm server-side nào trong toàn bộ codebase);
phần không thể để client tự khai (đếm lượt, tính pct/passed, đóng mục) đẩy xuống trigger DB.

**Còn treo (cập nhật 24/9/2026):** migration đã chạy trên Supabase. Vẫn CHƯA test UI thật
trên trình duyệt (không có tài khoản học sinh test trong phiên code), và CHƯA commit/deploy
— khi được hỏi "deploy tất cả các thay đổi", thầy chọn tách feature này ra (giữ lại WIP,
chỉ deploy phần khác) đúng theo [[feedback_thachlab_deploy_scope]]. File liên quan vẫn nằm
trong working tree: components/results/TutoringExitQuiz.tsx, components/dashboard/ThptStudentHome.tsx,
services/tutoring.ts, docs/supabase-migration-tutoring-exit-quiz.sql — đợi thầy test rồi mới commit riêng.

**Cập nhật 2026-09-25 (phiên khác, không phải phiên viết memory này — xem [[project_thachlab_concurrent_sessions]]):**
đã commit + push (`b85d82a7 feat(tro-giang): kiểm soát đầu ra phụ đạo bằng bài tự kiểm tra thay vì tick tay`),
GỘP LUÔN vào công thức lương trợ giảng: điểm 25đ "phụ đạo" trong `ta_monthly_policy`
([[project_thachlab_ta_policy]]) từ 01/10/2026 giờ đòi có bằng chứng khách quan là
`tutoring_exit_attempts` đạt ≥80% cùng ngày ghi buổi, không chỉ tick tay
prepared/recalled/asked_each như trước (buổi trước 01/10/2026 vẫn giữ cách tick tay cũ).
`PhudaoPlanner` hiện trạng thái tự kiểm tra realtime theo từng chủ đề. `scripts/tests/ta-policy.mjs`
đã có ca kiểm thử công thức mới, 13/13 pass. **Vẫn CHƯA test UI thật** qua tài khoản học sinh/trợ giảng thật.
