-- ============================================================================
-- perf(db-index): index bổ sung cho các truy vấn nóng — Pha 1 tối ưu tốc độ 9/2026
-- ============================================================================
-- Nguồn: perf/DB_REPORT.md (bảng "cột bị lọc / sắp xếp" đối chiếu pg_indexes
-- thật trên project, đọc 25/9/2026, PostgreSQL 17.6).
--
-- Cách chạy:
--   * Dashboard → SQL Editor → dán cả file, Run. Mọi lệnh đều idempotent
--     (`if not exists`), chạy lại không lỗi.
--   * SQL Editor chạy trong MỘT transaction nên KHÔNG dùng `concurrently`.
--     Mọi bảng ở đây đều nhỏ (lớn nhất question_bank ≈ 10.8k dòng / 27 MB),
--     mỗi lệnh khoá bảng vài chục ms → chạy cả file một lần là được.
--   * Nếu sau này bảng lớn (> vài trăm nghìn dòng) thì chạy TỪNG lệnh, hoặc
--     dùng psql/`supabase db query` và thêm `concurrently` (ngoài transaction).
--   * KHÔNG dùng `supabase db push` cho file này khi thư mục migrations chưa
--     được đồng bộ với DB (99 file docs/supabase-migration-*.sql chạy tay).
-- ============================================================================

-- ---------------------------------------------------------------------------
-- 1. question_bank — bảng lớn nhất (≈ 10.8k dòng, 27 MB, 293k idx_scan)
-- ---------------------------------------------------------------------------
-- dùng bởi services/question-bank.ts:85-103 (fetchBankQuestions: lọc grade +
--   archived, order topic_id nulls last → source_exam_id → source_index, limit 500)
-- dùng bởi services/question-bank.ts:143-147 (fetchBankUnknownGradeCount: grade='' và archived=false)
-- dùng bởi view question_bank_topic_counts (services/question-bank.ts:126-129, group by grade/topic_id/archived)
-- Index sẵn có question_bank_grade_idx (subject_code, grade, archived) KHÔNG dùng
-- được vì code không lọc subject_code (PG 17 chưa có skip scan). Thứ tự cột
-- khớp cả WHERE lẫn ORDER BY → planner đi Index Scan, bỏ bước Sort, dừng sớm ở LIMIT.
create index if not exists idx_question_bank_grade_archived_browse
  on public.question_bank (grade, archived, topic_id, source_exam_id, source_index);

-- ---------------------------------------------------------------------------
-- 2. exam_attempts — khôi phục bài làm dở, gọi mỗi lần mở đề
-- ---------------------------------------------------------------------------
-- dùng bởi services/progress.ts:307-315 (findOpenExamAttempt: student_id = ? and
--   exam_id = ? and submitted_at is null order by started_at desc limit 1)
-- dùng bởi services/progress.ts:93-99 (fetchRawProgressBatch: in student_id, in exam_id, submitted_at is null)
-- Index sẵn có exam_attempts_student_idx (student_id, started_at) phải lọc thêm
-- exam_id + submitted_at trên heap. Partial index chỉ giữ bài đang dở → rất nhỏ.
create index if not exists idx_exam_attempts_student_exam_open
  on public.exam_attempts (student_id, exam_id, started_at desc)
  where submitted_at is null;

-- ---------------------------------------------------------------------------
-- 3. exam_results — cặp (học sinh, đề) bị hỏi ở cả client lẫn trigger/RPC
-- ---------------------------------------------------------------------------
-- dùng bởi services/progress.ts:85-89 (fetchRawProgressBatch: in student_id, in exam_id)
-- dùng bởi services/analytics.ts:252-256 và :758 (eq exam_id, in student_id)
-- dùng bởi RPC rank_best_pct (docs/supabase-migration-rank-system.sql: where student_id = ? and exam_id = ? and created_at trong khoảng)
-- dùng bởi evaluate_student_alerts / sweep_missed_assessments (docs/supabase-migration-exam-analytics.sql:241,266,358 — chạy trong trigger sau mỗi lần nộp bài)
-- dùng bởi refresh_tutoring_needs (docs/supabase-migration-tutoring-needs.sql:218-228, trigger sau mỗi lần nộp bài)
-- Index sẵn có exam_results_student_idx (student_id, created_at) vẫn giữ để liệt kê
-- lịch sử theo thời gian; index này phục vụ lookup theo (student_id, exam_id).
create index if not exists idx_exam_results_student_exam_created
  on public.exam_results (student_id, exam_id, created_at desc);

-- ---------------------------------------------------------------------------
-- 4. question_topics — tra id chủ đề theo tên khi nộp bài / lưu luyện tập
-- ---------------------------------------------------------------------------
-- dùng bởi components/exams/ExamRunner.tsx:196-199 (.in("name", names) — mỗi lần nộp bài kiểm tra)
-- dùng bởi services/lessons.ts:362-365 (savePracticeSession: .in("name", names))
-- dùng bởi docs/supabase-migration-rank-system.sql:1750 (not exists ... qt.grade = ? and qt.name = ?)
-- Unique key sẵn có (subject_code, grade, name) không dùng được khi chỉ lọc name.
create index if not exists idx_question_topics_name
  on public.question_topics (name);

-- ---------------------------------------------------------------------------
-- 5. lesson_items — tiến độ theo bài: chỉ cần id + exam_ids, không cần nội dung
-- ---------------------------------------------------------------------------
-- dùng bởi services/lessons.ts:208-211 (fetchItemIdsByLessons: select id, lesson_id in lesson_id)
-- dùng bởi services/lessons.ts:233-234 (fetchLessonProgressSummaries: select id, lesson_id, exam_ids in lesson_id — trang /lop-hoc và trang chủ HS)
-- Bảng chỉ 262 dòng nhưng ~3 KB/dòng (HTML lý thuyết). Covering index cho phép
-- Index Only Scan, không chạm heap → không đọc nội dung HTML chỉ để đếm mục.
create index if not exists idx_lesson_items_lesson_cover
  on public.lesson_items (lesson_id) include (id, exam_ids);

-- ---------------------------------------------------------------------------
-- 6. exam_question_results — câu tự luận chờ chấm (bảng 7.2k dòng, tăng nhanh nhất)
-- ---------------------------------------------------------------------------
-- dùng bởi services/progress.ts:443-450 (fetchPendingEssays: qtype = 'essay' and
--   graded_at is null and student_id in (...) — dashboard giáo viên mỗi lần mở lớp)
-- Các truy vấn khác trên bảng này (student_id, exam_id, exam_result_id, topic_id)
-- đã có index từ migration exam-analytics — xem DB_REPORT.md. Partial index này
-- chỉ chứa câu tự luận chưa chấm nên gần như rỗng, gần như không tốn chi phí ghi.
create index if not exists idx_eqr_pending_essay
  on public.exam_question_results (student_id)
  where qtype = 'essay' and graded_at is null;

-- ---------------------------------------------------------------------------
-- 7. attendance_records — lịch sử máy nào ai đứng (trang tình trạng máy CNC)
-- ---------------------------------------------------------------------------
-- dùng bởi services/course-attendance.ts:27-31 (fetchMachineUsageHistory: eq machine_code, limit 30)
-- Không có index nào bắt đầu bằng machine_code; partial bỏ dòng chưa chọn máy.
create index if not exists idx_attendance_records_machine_code
  on public.attendance_records (machine_code)
  where machine_code is not null;

-- ============================================================================
-- Kiểm tra sau khi chạy (chỉ đọc):
--   select indexname, indexdef from pg_indexes
--   where schemaname = 'public' and indexname like 'idx\_%' escape '\' order by 1;
-- Theo dõi index có được dùng không (sau vài ngày):
--   select relname, indexrelname, idx_scan from pg_stat_user_indexes
--   where indexrelname like 'idx\_%' escape '\' order by idx_scan;
-- ============================================================================

-- ============================================================================
-- ROLLBACK (chạy tay nếu cần gỡ — thứ tự không quan trọng, đều idempotent)
-- ============================================================================
-- drop index if exists public.idx_question_bank_grade_archived_browse;
-- drop index if exists public.idx_exam_attempts_student_exam_open;
-- drop index if exists public.idx_exam_results_student_exam_created;
-- drop index if exists public.idx_question_topics_name;
-- drop index if exists public.idx_lesson_items_lesson_cover;
-- drop index if exists public.idx_eqr_pending_essay;
-- drop index if exists public.idx_attendance_records_machine_code;
