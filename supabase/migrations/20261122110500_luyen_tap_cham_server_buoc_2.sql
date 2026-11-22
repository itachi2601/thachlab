-- ============================================================================
-- Vá bảo mật — practice_sessions.score do máy HS gửi — BƯỚC 2/2: thu quyền INSERT trực tiếp (22/11/2026)
-- CHỈ chạy khi: bước 1 (20261122100000) đã chạy, client mới (services/lessons.ts gửi qua practice_session_submit)
-- đã deploy ≥1 ngày (tab cũ đã tải lại, hàng đợi offline kiểu cũ đã kịp gửi). Ngoài giờ HS làm bài (sau 22h/trước 6h).
-- Sau file này phiên kiểu cũ còn nằm trong hàng đợi offline của máy nào đó sẽ bị từ chối (client bỏ qua, không lặp).
--
-- Làm gì: bỏ policy "student inserts own practice sessions" + "student inserts own practice question results".
-- Giữ: policy đọc của HS/GV/TA (teaches_student), phụ huynh, "admin manages …" (nếu có trên prod).
--
-- Ai đọc/ghi được gì SAU file này:
-- | Vai             | practice_sessions / practice_question_results                   |
-- |-----------------|-----------------------------------------------------------------|
-- | HS              | đọc của mình; ghi CHỈ qua practice_session_submit (server chấm) |
-- | Trợ giảng / GV  | đọc HS mình dạy; ghi phiên của chính mình qua RPC               |
-- | Admin           | như cũ (policy "admin manages …")                               |
-- | Phụ huynh       | đọc của con                                                     |
-- | anon            | không                                                           |
--
-- Kiểm thử sau khi chạy (tự rollback):
--   do $t$ begin
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid HS>','role','authenticated')::text, true);
--     set local role authenticated;
--     insert into public.practice_sessions (student_id, question_count, correct_count, score)
--       values ('<uuid HS>', 10, 10, 10);   -- mong đợi: new row violates row-level security policy
--   end $t$;
--   HS gọi practice_session_submit (khối kiểm thử ở bước 1) → vẫn ghi được.
--   GV: select count(*) from public.practice_sessions where student_id = '<HS lớp mình>' → như trước khi chạy.
--
-- Rollback: perf/rollback/20261122110500_luyen_tap_cham_server_buoc_2.down.sql (dựng lại 2 policy y nguyên).
-- ============================================================================
begin;

drop policy if exists "student inserts own practice sessions" on public.practice_sessions;
drop policy if exists "student inserts own practice question results" on public.practice_question_results;

commit;
