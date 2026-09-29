---
name: project-thachlab-exam-class-access-fix
description: Vá lỗ hổng phân quyền /kiem-tra/lam — học sinh làm/nộp được đề không thuộc lớp mình; đã deploy + verify xong 2026-09-27
metadata:
  node_type: memory
  type: project
  originSessionId: 3036e6f7-2221-4c39-a498-e54ce46db8ff
  modified: 2026-09-27T13:07:25.657Z
---

Lỗ hổng phát hiện lúc test luồng làm bài ở worktree `perf5-test-exam-flow`
(xem `perf5/RESULT-exam-flow.md`): học sinh đã đăng nhập có thể làm và NỘP
bất kỳ đề `published` nào qua `/kiem-tra/lam?id=<id>` dù không thuộc lớp
mình (đoán/chia sẻ id tăng dần) — vì `RequireAuth` ở trang đó không kiểm tra
lớp, và RLS cũ trên `exams`/`exam_results`/`exam_question_results` chỉ yêu
cầu `published`/`student_id = auth.uid()`, không đối chiếu `exam_classes` ↔
`user_classes`.

**Đã xong hoàn toàn (2026-09-27), không còn gì treo:**
- UI: [app/kiem-tra/lam/page.tsx](../../../../Projects/thachlab/app/kiem-tra/lam/page.tsx)
  chặn sớm + báo "Đề này không thuộc lớp của em" khi đề có gán lớp mà học
  sinh không active trong lớp đó (bỏ qua kiểm tra cho admin/instructor/
  tro_giang, dùng `realProfile.role` chứ không phải `profile` bị ghi đè bởi
  "Xem như học sinh" — preview mode vẫn cố ý mở khoá hết, không đổi).
- DB: `supabase/migrations/20260927150000_exam_class_access.sql` — thêm 2
  hàm `public.is_staff()` + `public.exam_open_to_student(exam_id, user_id)`
  và 3 policy RLS **restrictive** (AND với policy permissive cũ, không đụng
  is_admin()/published/cnc_key hiện có) trên `exams` (select),
  `exam_results` + `exam_question_results` (insert). Rollback:
  `perf/rollback/20260927150000_exam_class_access.down.sql`.
- **ĐÃ CHẠY migration production** qua
  `supabase db query --linked -f <đường dẫn tuyệt đối>` (worktree không có
  `supabase link`, phải chạy từ `/Users/MAC/Projects/thachlab`).
- **ĐÃ MERGE** nhánh `claude/cranky-colden-989171` vào `main` (commit
  `e4498d4c`), đã push origin/main.
- **ĐÃ DEPLOY** qua `bash scripts/deploy.sh` (build 69 route OK, force-push
  nhánh `deploy`), hosting tự kéo bản mới trong ~10 phút qua cron job.
- **ĐÃ VERIFY bằng dữ liệu thật trên production** (chỉ đọc, không ghi) —
  gọi trực tiếp `exam_open_to_student()`: đề có gán lớp + học sinh đúng lớp
  → `true`; đề đó + học sinh khác lớp → `false`; đề toàn trường (không có
  dòng nào trong `exam_classes`) + học sinh bất kỳ → `true`. Đúng như thiết
  kế.

**Quyết định thiết kế quan trọng (đọc code không tự suy ra được):**
- Nguồn thật để xác định đề thuộc lớp nào là bảng `exam_classes` (M2M
  exam↔lớp), KHÔNG phải đường `lesson_items → lessons → chapters →
  chapter_classes` (đó là M2M khác, chỉ gate hiển thị mục trong bài học,
  không phải quyền làm đề — 1 exam_id có thể được nhiều lesson_items ở
  nhiều lớp khác nhau cùng tham chiếu, vd đề ngân hàng câu hỏi dùng chung).
- "Đề không có dòng nào trong exam_classes" = đề toàn trường, CHỦ Ý, đúng
  logic `services/content.ts#visibleTo` đã dùng sẵn để lọc danh sách đề
  hiển thị — không phải lỗ hổng, không được chặn.
- Ngân hàng CNC (`exams.cnc_key is not null`, luôn `published=false`) được
  giữ nguyên hành vi cũ (không qua exam_classes) — không thuộc phạm vi lỗ
  hổng đang vá, tránh vỡ tính năng `/quan-tri/cnc-*`.
- Chưa test UI đầu-cuối bằng tài khoản học sinh thật thấp cấp (không phải
  admin) — không bắt buộc, user đã xác nhận verify bằng DB + hàm SQL là đủ
  (2026-09-27). Nếu sau này nghi ngờ hồi quy, có thể tự đăng ký 1 tài khoản
  throwaway qua `/dang-ky` (không gán lớp) rồi thử `/kiem-tra/lam?id=<id đề
  có gán lớp>` — phải bị chặn.

Liên quan: [[project_thachlab_exam_proctoring]], [[project_thachlab_perf_optimization]]
(worktree perf5-test-exam-flow phát hiện lỗ hổng này trong lúc verify).
