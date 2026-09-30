---
name: project-thachlab-mastery-yccd
description: Nhãn Nắm vững/Cần luyện thêm/Chưa đạt theo YCCĐ (mastery) ở /lop-hoc; RPC get_lesson_mastery/get_chapter_mastery; deploy 26/9/2026
metadata:
  node_type: memory
  type: project
  originSessionId: 6093eceb-f6fb-4d0d-b57e-05c21ebebc94
  modified: 2026-09-26T02:31:10.603Z
---

Mục tiêu: cho học sinh thấy mình đang mạnh/yếu ở yêu cầu cần đạt (YCCĐ) nào trong 1 bài, không chỉ điểm số chung. Đây là 1 trong 3 việc chạy song song bằng 3 agent + 1 agent kiểm tra độc lập (roadmap tuần 25-26/9/2026, xem [[project_thachlab_question_bank]] cho phần difficulty cùng đợt, và feat/SURVEY.md ở gốc repo cho khảo sát Phase 0 gốc).

**Đã xong (26/9/2026), migration đã chạy lên production:**
- Migration `supabase/migrations/20260925160000_mastery.sql` — 2 hàm `security invoker`: `get_lesson_mastery(p_lesson bigint)` trả nhãn từng YCCĐ trong bài + nhãn cả bài (thấp nhất trong các YCCĐ đủ dữ liệu); `get_chapter_mastery(p_chapter bigint)` trả nhãn từng bài trong 1 chương.
- Quy tắc tính (hằng số, xem `docs/mastery-rules.md`): gộp `exam_question_results`+`practice_question_results`, lấy tối đa 10 lượt gần nhất mỗi YCCĐ (`topic_id`); <4 lượt → "Chưa đủ dữ liệu" (xám); ≥80% đúng → "Nắm vững" ✅; 50–79% → "Cần luyện thêm" 🟡; <50% → "Chưa đạt" 🔴. Câu chỉ gắn tầng Bài (không có YCCĐ con) chỉ tính vào nhãn cấp Bài, không tính YCCĐ nào.
- UI: `components/mastery/{MasteryBadge,LessonMasteryCard,TopicPracticeModal}.tsx`, `services/mastery.ts`; gắn vào `app/lop-hoc/page.tsx` (icon ✅🟡🔴⚪ theo bài trong chương) và `app/lop-hoc/bai/page.tsx` (thẻ nhãn YCCĐ + nút "Luyện 10 câu phần này" sau khi nộp bài).
- Code fail-safe: nếu gọi RPC lỗi/chưa tồn tại thì component tự trả `null` (ẩn lặng lẽ), không crash trang — nên deploy code trước/sau khi chạy migration đều an toàn.
- Đã merge vào `main` (nhánh `feat/mastery`, xem lịch sử `git log --oneline` quanh `eea8b504`) và đã push lên origin.

**Quyết định thiết kế quan trọng không tự suy ra được từ code:**
- "Luyện 10 câu phần này" **KHÔNG** bốc câu từ toàn bộ `question_bank` theo YCCĐ — chỉ lấy câu trong chính các đề (`exam_ids`) của bài học đó, lọc theo `topic === topicName` (xem `TopicPracticeModal.tsx` dòng ~66-77, dùng lại `fetchExamsFull`/`gradeExam`/`savePracticeSession` sẵn có). Lý do: cơ chế bốc câu theo topic thật (`rank_fix_quiz_start`) đòi hỏi `exam_result_id` + mùa rank đang mở, không dùng được ở đây; đọc trực tiếp `question_bank` thì bị RLS chặn (chỉ có policy hẹp cho `tutoring_needs`). Hệ quả: nếu YCCĐ đó có câu trong ngân hàng chung nhưng KHÔNG nằm trong đề của chính bài học, học sinh sẽ thấy "chưa đủ câu hỏi" dù dữ liệu vẫn tồn tại nơi khác — đây là đánh đổi có chủ đích, không phải lỗi.
- **Chưa** trọng số theo mức độ Dễ/TB/Khó khi tính mastery (điểm mở rộng để làm sau khi difficulty đã đủ dữ liệu — xem [[project_thachlab_question_bank]]).
- Chương "Động học" lớp 10 đã gắn YCCĐ 100% từ trước nên KHÔNG cần chạy script AI gán YCCĐ dự phòng (`tag-yccd-dry-run`) — bỏ qua bước này theo đúng khảo sát.

**Còn treo:**
- Chưa test UI thật qua trình duyệt đăng nhập tài khoản học sinh (sandbox không đăng nhập được) — chỉ test RPC bằng SQL thật (transaction + rollback, xác nhận khớp tính tay 100% trên 1 học sinh mẫu + 1 case chưa có dữ liệu, xem `feat/RESULT.md` ở gốc repo lúc merge).
- Cân nhắc thêm trọng số difficulty vào công thức mastery khi difficulty đã đủ dữ liệu (33 câu ngân hàng còn thiếu mức độ, xem [[project_thachlab_question_bank]]).

**How to apply:** khi sửa trang `/lop-hoc` hoặc `/lop-hoc/bai`, đừng thêm query Supabase rời mới — 2 trang này đã qua đợt tối ưu hiệu năng ([[project_thachlab_perf_optimization]]), chỉ gọi đúng 1 RPC mastery là đủ.
