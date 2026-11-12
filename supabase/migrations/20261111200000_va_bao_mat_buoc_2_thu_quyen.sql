-- ============================================================================
-- Vá bảo mật sau rà soát 11/11/2026 — BƯỚC 2/2: thu quyền. Đây cũng là P0 #1 chặng 3 (thu quyền exams.questions).
-- CHỈ chạy SAU KHI đã chạy bước 1 (20261111190000) VÀ đã deploy client gọi notify_user_staff / get_cnc_quiz_banks /
-- cnc_milling_quiz_save. Chạy sau 22h: bản client cũ còn mở trong trình duyệt sẽ lỗi ở quiz CNC, nhắc làm bài, quiz phay
-- cho tới khi tải lại trang. Không quét/ghi dữ liệu → nhẹ.
--
--  1. exams.questions (có answer + explanation): thu quyền đọc trực tiếp của anon/authenticated. Từ đây:
--       HS đọc đề qua get_exam_for_taking (đã lược đáp án) / get_exam_review (sau khi nộp);
--       admin/GV/TA đọc đủ đáp án qua view exams_staff; quiz CNC qua get_cnc_quiz_banks.
--     Các cột còn lại của exams vẫn đọc như cũ (RLS không đổi). Ghi (insert/update/delete) không đổi.
--  2. notify_user: chỉ còn hàm/trigger nội bộ gọi; client dùng notify_user_staff.
--  3. cnc_milling_quiz_attempts: bỏ 2 policy cho anon INSERT/UPDATE mọi dòng; ghi qua cnc_milling_quiz_save.
--  4. rank_gate_pool_ids (quyền người gọi, đọc exams.questions, nhận p_student bất kỳ): chỉ rank_gate_start (definer)
--     gọi → thu quyền gọi trực tiếp của anon/authenticated.
--
-- Rollback: perf/rollback/20261111200000_va_bao_mat_buoc_2_thu_quyen.down.sql
-- ============================================================================
begin;

-- ---------- 1. exams: đọc theo cột, trừ questions ----------
revoke select on public.exams from anon, authenticated;
grant select (id, created_at, title, duration_minutes, published, question_count, topic, difficulty, type_counts,
              subject_code, cnc_key, pass_score)
  on public.exams to anon, authenticated;

-- ---------- 2. notify_user: nội bộ ----------
revoke all on function public.notify_user(uuid, text, text, text, text) from public, anon, authenticated;

-- ---------- 3. Quiz phay: thôi ghi thẳng vào bảng ----------
drop policy if exists "classroom creates live milling attempts" on public.cnc_milling_quiz_attempts;
drop policy if exists "classroom updates live milling attempts" on public.cnc_milling_quiz_attempts;

-- ---------- 4. rank_gate_pool_ids: nội bộ ----------
revoke all on function public.rank_gate_pool_ids(bigint, uuid, text) from public, anon, authenticated;

commit;
