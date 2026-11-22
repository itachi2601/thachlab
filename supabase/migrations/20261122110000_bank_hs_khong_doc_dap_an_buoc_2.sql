-- ============================================================================
-- Vá bảo mật chặng 4 — question_bank lộ đáp án cho HS — BƯỚC 2/2: thu quyền cũ (22/11/2026)
-- CHỈ chạy khi: bước 1 (20261122090000) đã chạy, client mới (TutoringExitQuiz/EntryDiagnosticQuiz gọi
-- bank_questions_for_student / tutoring_exit_quiz_submit / diagnostic_check_answer) đã deploy ≥1 ngày (tab cũ đã tải lại).
-- Chạy ngoài giờ HS làm bài (sau 22h hoặc trước 6h): tab cũ chưa tải lại sẽ thấy "Ngân hàng chưa có câu nào".
--
-- Làm gì: bỏ 2 policy SELECT cho HS trên question_bank + policy HS INSERT thẳng tutoring_exit_attempts.
-- Giữ: policy "staff manage question bank" (admin/GV THPT), "read own exit attempts", "ta reads own window attempts",
--       hàm diagnostic_bank_topic_ids() (bank_questions_for_student/diagnostic_check_answer dùng).
--
-- Ai đọc/ghi được gì SAU file này:
-- | Vai             | question_bank (bảng)          | câu không đáp án (RPC)            | tutoring_exit_attempts            |
-- |-----------------|-------------------------------|-----------------------------------|-----------------------------------|
-- | HS              | KHÔNG đọc được dòng nào       | chủ đề phụ đạo mở + bài chẩn đoán | đọc của mình; ghi CHỈ qua         |
-- |                 |                               |                                   | tutoring_exit_quiz_submit (server |
-- |                 |                               |                                   | chấm)                             |
-- | Trợ giảng       | không                         | ≈ không (không có mục phụ đạo)    | đọc lượt trong cửa sổ mình mở /   |
-- |                 |                               |                                   | HS mình dạy; không ghi            |
-- | GV THPT / admin | đọc/ghi tất cả (như cũ)       | mọi chủ đề                        | đọc HS mình dạy; không ghi thẳng  |
-- | Phụ huynh       | không                         | không                             | như cũ                            |
-- | anon            | không                         | không                             | không                             |
--
-- Kiểm thử sau khi chạy (tự rollback):
--   do $t$ declare n int; begin
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid HS có mục phụ đạo mở>','role','authenticated')::text, true);
--     set local role authenticated;
--     select count(*) into n from public.question_bank;                       -- mong đợi 0
--     raise exception 'KETQUA hs_doc_bang=% rpc=%', n,
--       jsonb_array_length(public.bank_questions_for_student(array[<topic mục phụ đạo>]::bigint[]));  -- rpc > 0
--   end $t$;
--   Cùng khối, HS: insert into public.tutoring_exit_attempts(tutoring_need_id, student_id, total, correct)
--     values (<need của em>, '<uuid HS>', 1, 1);  → mong đợi lỗi "new row violates row-level security policy".
--   Admin: select count(*) from public.question_bank → > 0 (như cũ).
--
-- Rollback: perf/rollback/20261122110000_bank_hs_khong_doc_dap_an_buoc_2.down.sql (dựng lại 3 policy y nguyên).
-- ============================================================================
begin;

drop policy if exists "student reads exit-quiz bank questions" on public.question_bank;
drop policy if exists "student reads entry-diagnostic bank questions" on public.question_bank;
drop policy if exists "student logs own exit attempt" on public.tutoring_exit_attempts;

commit;
