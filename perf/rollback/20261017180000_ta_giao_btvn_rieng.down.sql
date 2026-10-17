-- Hoàn tác 20261017180000_ta_giao_btvn_rieng.sql. Mất danh sách BTVN riêng đã giao (bài nộp thật trong exam_results giữ nguyên).
-- Thông báo đã gửi giữ nguyên (xoá tay nếu cần: delete from notifications where kind = 'ta_homework_new').
drop function if exists public.ta_homework_overview(bigint, int);
drop function if exists public.my_pending_homework();
drop function if exists public.ta_homework_assign(bigint, uuid[], bigint, timestamptz, text);
drop table if exists public.ta_homework_assignments;
