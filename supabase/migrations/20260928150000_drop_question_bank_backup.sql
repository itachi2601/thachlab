-- ============================================================
-- Xoá bảng backup tạm của đợt sửa hash/gộp câu trùng ngân hàng câu hỏi (25/9/2026).
-- Bảng được tạo bởi docs/supabase-migration-question-bank-hash-fix.sql, chỉ để đối chiếu
-- ngay sau khi gộp 10 780 → 7 215 dòng. Việc đối chiếu đã xong; question_bank đã được sửa
-- thêm nhiều lần từ đó nên bản backup này không còn dùng để hoàn tác được nữa.
-- Mục đích: lấy lại ~13 MB (≈12% hạn mức 500 MB gói Free).
-- Chạy giờ nào cũng được, không ảnh hưởng học sinh (bảng không được code nào đọc).
-- ============================================================

drop table if exists public.question_bank_backup_20260925;

-- ---------- ROLLBACK ----------
-- Không hoàn tác được: dữ liệu bảng backup mất hẳn khi drop. Nếu cần một bản chụp mới
-- của question_bank thì tạo lại bằng:
--   create table public.question_bank_backup_<ngày> as select * from public.question_bank;
-- (xem perf/rollback/20260928150000_drop_question_bank_backup.down.sql)
