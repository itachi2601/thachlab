-- Hoàn tác 20261105220000_similar_practice_attempts.sql
-- Xoá bảng ghi lượt "Làm bài tương tự" (mất số đo Mẹo nhìn đã ghi; không ảnh hưởng bảng khác).
begin;

drop table if exists public.similar_practice_attempts;

commit;
