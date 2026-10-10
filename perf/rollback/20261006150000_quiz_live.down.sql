-- Hoàn tác Đố vui lớp học. Phòng chơi chỉ là tạm; bộ câu (quiz_sets) sẽ mất — câu đã đưa vào ngân hàng vẫn còn.
begin
drop function if exists public.quiz_set_to_bank(bigint, text, text, text);
drop function if exists public.quiz_bank_search(text, bigint, text, text, int, boolean);
drop function if exists public.quiz_host_end(bigint);
drop function if exists public.quiz_host_kick(bigint, bigint);
drop function if exists public.quiz_host_advance(bigint);
drop function if exists public.quiz_host_state(bigint);
drop function if exists public.quiz_host_create(bigint, int);
drop function if exists public.quiz_host_room(bigint);
drop function if exists public.quiz_answer(bigint, uuid, int);
drop function if exists public.quiz_state(bigint, uuid);
drop function if exists public.quiz_join(text, text);
drop function if exists public.quiz_leaderboard(bigint, int);
drop function if exists public.quiz_secs_left(public.quiz_rooms);
drop function if exists public.quiz_eff_phase(public.quiz_rooms);
drop table if exists public.quiz_answers, public.quiz_players, public.quiz_rooms, public.quiz_sets;
commit
