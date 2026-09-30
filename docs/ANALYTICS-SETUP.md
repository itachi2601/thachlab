# Phân tích điểm số & chủ đề hay sai — hiện trạng (cập nhật 29/09/2026)

Bản cũ của file này (viết khi mới tạo bảng `exam_question_results`) mô tả quy trình **nhập tay** từng
câu sai và trường `topic` dạng text. Cả hai đã lỗi thời. Dưới đây là cách hệ thống đang chạy thật;
cột bảng lấy từ `docs/DATABASE.md` (sinh tự động), không tự dò schema.

## Dữ liệu được ghi tự động

- **Khi HS nộp bài** (`components/exams/ExamRunner.tsx`, khoảng dòng 180–229): chấm từng câu bằng
  `gradeQuestion()` (`features/exams/types.ts`) rồi ghi một dòng `exam_results` và **mỗi câu một
  dòng** `exam_question_results`. Không còn bước nhập tay.
- Cột chính của `exam_question_results`: `exam_result_id`, `question_index`, `student_id`, `exam_id`,
  `topic_id → question_topics` (YCCĐ 2 tầng Bài → yêu cầu cần đạt), `topic_name`, `form`
  (lý thuyết / bài tập), `qtype`, `earned`, `max`, `is_correct`, `difficulty` (Dễ/TB/Khó),
  `manual_earned` / `manual_max` / `graded_by` / `graded_at` (tự luận chấm tay qua RPC
  `grade_essay_answer`).
- Phiên luyện tập tự bốc câu ghi vào `practice_sessions` + `practice_question_results` (cùng cấu
  trúc earned/max/topic_id/difficulty).
- Nhãn `topic_id`/`form`/`difficulty` của câu đến từ lúc **đăng đề** (dòng `Chủ đề:`/`Dạng:` ở
  `/quan-tri/dang-de`, nút "AI gắn nhãn") — xem `docs/DANG-DE-TU-WORD.md`. Câu không có nhãn thì
  không vào thống kê theo YCCĐ.
- Bài làm cũ trước khi có cơ chế tự ghi: dựng lại bằng `node scripts/backfill-exam-analytics.mjs`.
- Kết quả quá 12 tháng được gộp vào `question_result_rollups` (pg_cron, xem
  `docs/STATE-archive.md`), thống kê vẫn đọc được.

## Nơi hiển thị

| Ai | Trang / component | Nguồn |
|---|---|---|
| Học sinh | `/lop-hoc/ket-qua` (`StudentResultsDashboard`): xu hướng điểm, chủ đề sai nhiều, nút "Ôn lại bài"; thẻ mastery trong bài học ("Luyện 10 câu phần này") | RPC `get_lesson_mastery`, `get_chapter_mastery` — quy tắc ở `docs/mastery-rules.md` |
| Giáo viên | `/dashboard-thpt` tab **Phân tích** (`TeacherThptAnalysis.tsx`): phổ điểm, câu sai nhiều nhất, chủ đề yếu của lớp; tab **Cảnh báo phụ đạo**, **Phụ đạo**; trình chiếu chữa bài `/dashboard-thpt/chua-bai` | RPC `get_class_exam_question_stats`, `get_class_topic_matrix`, `student_outcome_gaps`; `services/analytics.ts` |
| Phụ huynh | `/phu-huynh` (cùng `StudentResultsDashboard`, viewer `parent`) | như HS, chỉ đọc — `docs/PHU-HUYNH.md` |
| Trợ giảng | `/tro-giang/phu-dao` | `tutoring_needs` (trigger tự mở/đóng, `docs/PHU-DAO.md`) |

Ngưỡng màu: đỏ khi sai > 50 %, vàng 30–50 %; mastery: ≥ 80 % Nắm vững, 50–80 % Cần luyện thêm,
< 50 % Chưa đạt (chi tiết và TODO trọng số độ khó ở `docs/mastery-rules.md`).

## Chưa có (tính đến 29/09/2026)

- Xuất báo cáo phân tích ra Word/PDF/Excel cho tổ chuyên môn (THPT chỉ có CSV bảng điểm thô).
- Nhập kết quả làm trên Azota về LMS — toàn bộ tích hợp Azota hiện chỉ là chiều đề → LMS hoặc nhúng
  iframe (`docs/AZOTA-INTEGRATION.md`).
- Hai việc trên nằm trong đề xuất skill `phan-tich-ket-qua` ở `docs/DE-XUAT-SKILL-2026-09-29.md`.
