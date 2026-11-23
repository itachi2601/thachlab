-- Rollback 20261122090000_bank_hs_khong_doc_dap_an_buoc_1: bỏ 3 hàm + bảng entry_diagnostic_checks + trigger.
-- Chỉ chạy khi bước 2 (20261122110000) CHƯA chạy hoặc đã rollback — client mới gọi các hàm này.
begin;
drop trigger if exists trg_entry_diagnostic_checks_clear on public.entry_diagnostics;
drop function if exists public.trg_entry_diagnostic_checks_clear();
drop function if exists public.diagnostic_check_answer(bigint, jsonb);
drop table if exists public.entry_diagnostic_checks;
drop function if exists public.tutoring_exit_quiz_submit(bigint, bigint[], jsonb, uuid);
drop function if exists public.bank_questions_for_student(bigint[], text, bigint[], int);
commit;
