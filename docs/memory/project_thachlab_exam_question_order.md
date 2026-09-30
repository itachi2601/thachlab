---
name: project_thachlab_exam_question_order
description: "Bảng câu hỏi học sinh làm bài chia mục TN/ĐS/TLN theo cấu trúc đề thi 2025; câu lấy từ ngân hàng câu hỏi tự sắp lại theo thứ tự này — đã commit + push 26/9/2026, chưa test UI thật"
metadata:
  node_type: memory
  type: project
  originSessionId: 9804f597-ada3-4bde-a864-6479c9c5e06d
  modified: 2026-09-26T02:32:12.146Z
---

Thầy yêu cầu: "bảng câu hỏi" khi học sinh làm bài phải chia rõ theo đúng cấu trúc đề thi
2025 — TN 4 đáp án → Đúng–Sai (ĐS) → Trả lời ngắn (TLN) → (Tự luận) — thay vì một lưới số
câu phẳng; và khi thầy chọn câu từ [[project-thachlab-question-bank]] để soạn đề, câu phải
tự sắp lại theo đúng thứ tự đó bất kể bấm chọn lộn xộn.

Đã code xong (25/9/2026), 4 file:
- [features/exams/types.ts](features/exams/types.ts) — thêm `QUESTION_TYPE_ORDER` (thứ tự
  cố định multiple_choice → true_false → short_answer → essay) và hàm
  `groupQuestionIndexesByType(questions)` dùng chung: gom index câu (0-based) theo loại,
  KHÔNG đổi số thứ tự câu gốc (giữ `index+1` khớp với `QuestionCard`/chấm điểm).
- [components/exams/ExamRunner.tsx](components/exams/ExamRunner.tsx) — "Bảng câu hỏi" lúc
  làm bài (nút "Bảng câu hỏi" ở thanh sticky) đổi từ lưới phẳng sang từng khối có tiêu đề
  "Trắc nghiệm nhiều phương án · N câu" / "Đúng – Sai · N câu" / "Trả lời ngắn · N câu".
- [components/exams/ExamReviewPager.tsx](components/exams/ExamReviewPager.tsx) — áp cùng
  kiểu chia mục cho bảng câu hỏi lúc xem lại bài làm sau khi nộp.
- [components/admin/QuestionBankAdmin.tsx](components/admin/QuestionBankAdmin.tsx) — hàm
  `composeExam()` (nút "Soạn đề từ N câu") sort mảng câu lấy từ giỏ bằng
  `QUESTION_TYPE_ORDER.indexOf(qtype)` trước khi `writeHandoff()` sang trang Đăng đề.

**Why:** cả hai chỗ chỉ nhóm/sắp theo LOẠI câu (type), không đổi số thứ tự toàn cục 1..N —
tránh phải sửa dây chuyền `QuestionCard`/`gradeExam`/lưu `exam_attempts` vốn đang đánh số
theo index toàn cục. Parser văn bản Azota (PHẦN I/II/III) đã tự nhiên sinh câu đúng thứ tự
này rồi nên không cần sort lại ở parser; chỉ cần sort ở đúng chỗ lấy câu KHÔNG theo thứ tự
đề gốc — tức là giỏ ngân hàng câu hỏi.

**Cập nhật 2026-09-26:** đã commit (`6562d89a feat(kiem-tra): chia bảng câu xem lại theo loại TN/ĐS/TLN + nút ẩn/hiện`) và đã push lên `origin/main` (phiên khác chạy song song tự commit/push, không phải phiên viết memory này — xem [[project_thachlab_concurrent_sessions]]).

**Còn treo (2026-09-26):**
- `npx tsc --noEmit` và `npx eslint` trên 4 file trên đều sạch lúc viết code (lỗi eslint còn lại trong
  `QuestionBankAdmin.tsx` ở dòng 184/204 là lỗi có sẵn từ trước, không liên quan).
- **CHƯA test UI thật** — cần mở `/kiem-tra/lam` với một đề có đủ cả 3 loại câu (TN + ĐS +
  TLN) bằng tài khoản học sinh thật để xem bảng câu hỏi chia mục đúng, và thử luồng
  Ngân hàng câu hỏi → chọn câu lộn xộn → "Soạn đề từ N câu" → kiểm tra thứ tự câu ở trang
  Đăng đề có đúng TN→ĐS→TLN không.
- Working tree lúc làm việc này đang có nhiều WIP KHÔNG liên quan (nghi là phiên khác chạy
  song song — xem [[project_thachlab_concurrent_sessions]]): `services/exam-latex-parser.ts`,
  `services/docx-reader.ts`, `services/lesson-import.ts`, `services/question-figures.ts` (file
  mới, chưa track), `components/dashboard/TeacherThptAnalysis.tsx` — có vẻ là một tính năng
  "cảnh báo câu thiếu hình/đồ thị" đang dở, KHÔNG đụng tới trong phiên này, không có memory
  ghi nhận sẵn. Khi deploy nhớ chỉ `git add` đúng 4 file của mảng này theo
  [[feedback_thachlab_deploy_scope]].
