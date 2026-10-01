---
name: project_thachlab_exam_analytics
description: "Tính năng Phân tích kết quả kiểm tra + Cảnh báo phụ đạo cho thachlab — thiết kế đã duyệt, đang code"
metadata: 
  node_type: memory
  type: project
  originSessionId: cfc01d6b-802a-4159-820c-b5c17d171da0
  modified: 2026-09-21T15:44:18.544Z
---

2026-09-09: user yêu cầu, mình soạn thiết kế đầy đủ, user duyệt → làm **trọn một đợt** (không chia phase).

**Bản thiết kế (nguồn sự thật cho cả nhóm, share cho trợ giảng):**
https://claude.ai/code/artifact/3b999880-53b1-44c7-8a40-ea92e5a4471e — file gốc
`scratchpad/design/phan-tich-canh-bao.html` trong repo (gitignored). Sửa file đó rồi republish cùng URL.

**Quyết định đã chốt:**
- Cảnh báo `low_score_streak`: điểm < 6,5 ở **2 bài kiểm tra định kỳ liên tiếp** (điểm cao nhất mỗi bài; bài chưa làm → bỏ qua, không tính 0). Bài mới ≥ 6,5 → tự đóng.
- Cảnh báo `missed_assessment` (riêng): học sinh bỏ 1 bài KT định kỳ quá N ngày. Rà khi GV/trợ giảng mở tab (không có cron).
- Gắn nhãn câu: skill `up-de-kiem-tra` tự gắn `topic_id` (danh mục `question_topics`) + `form` ('ly_thuyet'|'bai_tap') lúc nhập đề. **Không** làm nút "AI gợi ý nhãn" trong admin — chỉ chọn/sửa thủ công.
- Cả admin lẫn trợ giảng được tạo chủ đề mới.
- Cảnh báo ẩn với chính học sinh cho tới khi trợ giảng chuyển trạng thái khác `open`.

**Schema mới (1 file `docs/supabase-migration-exam-analytics.sql`):** `question_topics`, `exam_question_results` (ghi lúc nộp trong ExamRunner), `class_assessments` (đề nào là bài KT định kỳ của lớp + thứ tự), `student_alerts` + trigger `evaluate_student_alerts` on insert `exam_results`. Toàn bộ cảnh báo chạy trong Supabase (trigger), không cần server.

**Có sẵn để tận dụng:** `exam_results.detail.responses` (chấm lại từng câu được), `gradeQuestion()`, `messages`, `class_instructors`, `lessons.lesson_kind` ([[project_thachlab_periodic_exam]]), RLS instructor `supabase-migration-thpt-instructor-access.sql`, khung `/dashboard-thpt`, `QuestionCard` review mode, `MistakeReviewPanel`.

**Bỏ đi:** nhánh cũ `claude/student-management-by-course-1890b4` commit `445d7db feat(analytics)` có bản nháp thô (`services/analytics.ts`, `WrongTopicsTable.tsx`, `exam_question_results` trong `supabase-migration-topics.sql`) — lấy ý tưởng, viết lại sạch, KHÔNG cherry-pick.

**Tiến độ 2026-09-10 — code xong hết, chờ user chạy migration + backfill + deploy:**
- Migration `docs/supabase-migration-exam-analytics.sql` (commit db5999d — đã fix lỗi 42703 do bảng cũ `topic text`; user re-run).
- Câu hỏi mang `topic` (TÊN chủ đề, khớp `question_topics.name`) + `form` ('ly_thuyet'|'bai_tap') — KHÔNG dùng topic_id trên câu. `features/exams/types.ts` `buildQuestionResults()`.
- `ExamRunner` ghi `exam_question_results` khi nộp (name→id best-effort) + màn kết quả gắn nhãn chủ đề/loại + "Ôn ngay".
- `services/analytics.ts` — toàn bộ query (group theo `topic_name`).
- `/lop-hoc/ket-qua` (trang HS mới, link ở Navbar) — biểu đồ điểm + chủ đề cần ôn + xem câu sai + "Ôn lại".
- `/dashboard-thpt` tab "Phân tích" (`TeacherThptAnalysis`) + "Cảnh báo phụ đạo" (`TeacherThptAlerts`); Overview tích hợp cảnh báo.
- `/quan-tri/chu-de` (`QuestionTopicsAdmin`) — danh mục chủ đề (gắn chương/bài) + gắn nhãn từng câu cho 1 đề.
- Skill `up-de-kiem-tra` (đã đưa vào git): SKILL.md + build_bundle.py hướng dẫn/validate topic+form.
- `scripts/backfill-exam-analytics.mjs` — dựng exam_question_results từ exam_results cũ (cần SERVICE_ROLE_KEY, chạy sau migration).
- KHÔNG làm auto-message trợ giảng (danh sách cảnh báo + metric Overview là kênh thông báo). GV/trợ giảng đánh dấu bài KT định kỳ ở tab Phân tích (`class_assessments`).

**User cần:** (1) re-run migration, (2) `SUPABASE_SERVICE_ROLE_KEY=… node scripts/backfill-exam-analytics.mjs`, (3) đánh dấu vài đề là bài KT định kỳ (tab Phân tích) để cảnh báo chuỗi hoạt động, (4) deploy.

**2026-09-12 — follow-up "xem lại bài + thứ hạng" (commit 43ac23b), code xong chờ migration+deploy:**
User phản hồi "học sinh không xem được bài đã làm" → thêm vào `/lop-hoc/ket-qua`:
mục "Bài đã làm" (danh sách mọi lượt nộp, bấm vào xem lại nguyên bài bằng `QuestionCard review`,
trước đó chỉ xem được câu sai gộp theo chủ đề) + thẻ "Hạng X/Y trong lớp" (điểm TB các bài
KT định kỳ, `class_assessments`) + hạng riêng từng đề khi mở 1 lượt làm.
Vì RLS `exam_results` chỉ cho đọc bài chính mình, hạng phải tính qua 2 RPC security-definer mới
(`docs/supabase-migration-student-rank.sql`: `get_exam_rank`, `get_periodic_rank`) — chỉ trả về
dòng của người gọi, không lộ điểm bạn khác (user chọn "chỉ hạng của chính mình" khi được hỏi).
**User cần:** chạy migration này trong Supabase SQL Editor, rồi deploy — CHƯA deploy vì lúc code
xong working tree có nhiều WIP dở của phiên khác (`app/tro-giang` …) và nhiều session Claude
đang chạy song song, sợ đụng `scripts/deploy.sh` (xem [[feedback_thachlab_deploy_scope]]).

**Cập nhật 2026-09-21 tối:** thầy xác nhận đã chạy `student-rank.sql` + test + deploy. Toàn bộ
đợt "Phân tích & cảnh báo phụ đạo" (migration gốc + backfill + xem lại bài/thứ hạng) coi như xong.

Liên quan: [[project_thachlab_lms]], [[project_thachlab_up_de_skill]], [[project_thachlab_periodic_exam]], [[feedback_thachlab_deploy_scope]]
