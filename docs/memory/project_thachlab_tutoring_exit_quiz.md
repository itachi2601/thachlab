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

**Cập nhật 2026-10-03 — bài kiểm tra cuối buổi (đổi cách đo buổi phụ đạo):** thầy chốt đo chất lượng buổi bằng
TỈ LỆ NHÓM ĐẠT, không còn "một em đạt 80% là đủ 25đ". Trợ giảng tick chủ đề đã dạy rồi bấm "Mở bài kiểm tra cuối buổi"
(`PhudaoPlanner`) → bảng `tutoring_exit_windows` (20 phút, giờ do máy chủ đặt); em tự đăng nhập tài khoản mình làm
(banner trên trang chủ HS, 10 câu cơ cấu 4 dễ/4 TB/2 khó ưu tiên câu chưa gặp, đạt ≥70%, 1 lượt/cửa sổ/chủ đề, không áp
cooldown 24h). Điểm phụ đạo 25đ/buổi: ≥60% cặp (em, chủ đề đã dạy có trong danh sách hổng) đạt trong cửa sổ do chính
trợ giảng mở đúng ngày ghi buổi → 25; 40–59% → 12,5; <40% → 0. Tự ôn ở nhà (80%, 24h) giữ nguyên nhưng KHÔNG tính điểm
trợ giảng. Chú thích "đưa lại điện thoại cho em" đã bỏ khỏi PhudaoPlanner và `/tro-giang/quy-che`.
Migration `20261003150000_phu_dao_kiem_tra_cuoi_buoi.sql` ĐANG CHỜ chạy; test `scripts/tests/ta-policy.mjs` 15/15 pass
(pglite); CHƯA test UI thật, chưa commit/deploy. Treo: chưa gắn tên 'buổi' vào cửa sổ (liên kết qua ngày + trợ giảng),
em không có thiết bị thì mượn máy lớp (đã ghi trong chú thích).

**Cập nhật 2026-10-04 — bắt buộc xem lại lý thuyết trước bài thoát:** tự kiểm tra giờ gồm bước 1 `TheoryReviewStep` (đọc hết mốc +
≥80% câu tự kiểm tra trong bài + đủ thời gian xem, máy chủ ghi `tutoring_theory_reviews`, guard chặn nộp nếu chưa xem sau lượt trước)
rồi bước 2 bài ~20 câu: ≤8 câu dễ từ bộ Kiểm tra nhanh của bài + còn lại ngân hàng (dễ→khó). Cửa sổ cuối buổi không đổi.
Migration `20261004130000_phu_dao_xem_lai_ly_thuyet.sql` ĐANG CHỜ (SQL test pglite qua); CHƯA test UI HS thật, chưa commit/deploy.
Lớp 12 chưa đăng bộ Kiểm tra nhanh nên phần câu dễ từ quiz lý thuyết rỗng tới khi đăng. Treo: nếu lý thuyết có nhiều bài trong một
chủ đề thì chỉ lấy mục `ly_thuyet` đầu tiên theo `sort_order`.
