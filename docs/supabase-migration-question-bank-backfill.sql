-- ============================================================
-- NGÂN HÀNG CÂU HỎI — bước 8: nạp lại toàn bộ đề đang có
-- ============================================================
-- Chạy SAU docs/supabase-migration-question-bank.sql (bảng + trigger đã tạo xong).
-- Idempotent: chạy lại chỉ upsert theo content_hash, không tạo dòng trùng.
-- Tách riêng để không giữ khoá độc quyền bảng exams (từ CREATE TRIGGER) trong lúc
-- đọc toàn bộ đề → tránh deadlock với app đang chạy.

select count(*) as exams_synced, sum(public.sync_exam_to_bank(id)) as questions_synced
from public.exams;
