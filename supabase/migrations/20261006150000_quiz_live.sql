-- Đố vui lớp học (kiểu Quizizz/Kahoot) — thầy/trợ giảng chiếu câu hỏi, học sinh vào bằng mã PIN trên điện thoại,
-- không cần đăng nhập. Câu lấy từ ngân hàng (question_bank) hoặc tự gõ; câu tự gõ đưa ngược vào ngân hàng được.
--
-- Thiết kế:
--  * Chỉ trắc nghiệm (multiple_choice) — chơi nhanh trên điện thoại. Khoá RLS: học sinh/ẩn danh KHÔNG đọc trực tiếp
--    bảng nào; mọi thứ đi qua RPC security definer (không bao giờ trả đáp án trước khi hết giờ).
--  * Trạng thái phòng: lobby → question → reveal → … → finished. Hết giờ (hoặc tất cả đã trả lời) coi như reveal
--    ngay trong hàm đọc, người điều khiển bấm "Tiếp" để sang câu sau.
--  * Điểm: đúng = 500–1000 tuỳ nhanh/chậm (đo bằng đồng hồ máy chủ), sai = 0. Bảng xếp hạng tính từ quiz_answers.
--  * Mỗi phòng chụp bản sao câu hỏi (questions) lúc mở, sửa bộ câu sau đó không làm lệch phòng đang chơi.
--
-- Chạy bất kỳ lúc nào: chỉ thêm bảng và hàm mới, không đụng dữ liệu cũ.
-- Rollback ở cuối file và perf/rollback/20261006150000_quiz_live.down.sql.
begin;

-- ---------- Bảng ----------
create table if not exists public.quiz_sets (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  owner_id uuid references public.profiles (id) on delete set null default auth.uid(),
  title text not null check (length(btrim(title)) between 1 and 120),
  grade text not null default '',
  questions jsonb not null default '[]'::jsonb check (jsonb_typeof(questions) = 'array'),
  banked_at timestamptz
);

create table if not exists public.quiz_rooms (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  pin text not null,
  set_id bigint references public.quiz_sets (id) on delete set null,
  host_id uuid references public.profiles (id) on delete set null default auth.uid(),
  title text not null,
  questions jsonb not null,
  time_limit_sec int not null default 20 check (time_limit_sec between 5 and 120),
  status text not null default 'lobby' check (status in ('lobby', 'question', 'reveal', 'finished')),
  current_index int not null default -1,
  question_started_at timestamptz
);
create unique index if not exists quiz_rooms_pin_live on public.quiz_rooms (pin) where status <> 'finished';

create table if not exists public.quiz_players (
  id bigint generated always as identity primary key,
  room_id bigint not null references public.quiz_rooms (id) on delete cascade,
  nickname text not null check (length(nickname) between 1 and 20),
  token uuid not null default gen_random_uuid(),
  joined_at timestamptz not null default now()
);
create unique index if not exists quiz_players_nick on public.quiz_players (room_id, lower(nickname));
create index if not exists quiz_players_room on public.quiz_players (room_id);

create table if not exists public.quiz_answers (
  room_id bigint not null references public.quiz_rooms (id) on delete cascade,
  player_id bigint not null references public.quiz_players (id) on delete cascade,
  q_index int not null,
  choice int not null,
  correct boolean not null,
  points int not null default 0,
  answered_at timestamptz not null default now(),
  primary key (player_id, q_index)
);
create index if not exists quiz_answers_room_q on public.quiz_answers (room_id, q_index);

alter table public.quiz_sets enable row level security;
alter table public.quiz_rooms enable row level security;
alter table public.quiz_players enable row level security;
alter table public.quiz_answers enable row level security;

-- Nhân sự (admin/giảng viên/trợ giảng) quản bộ câu; phòng/người chơi/đáp án chỉ đọc qua RPC (không policy cho anon).
drop policy if exists "staff manage quiz sets" on public.quiz_sets;
create policy "staff manage quiz sets" on public.quiz_sets
  for all to authenticated using (public.is_staff()) with check (public.is_staff());
drop policy if exists "staff read quiz rooms" on public.quiz_rooms;
create policy "staff read quiz rooms" on public.quiz_rooms
  for select to authenticated using (public.is_staff());

-- ---------- Hàm nội bộ ----------
-- Pha hiệu lực: hết giờ hoặc mọi người chơi đã trả lời → coi như đã sang reveal.
create or replace function public.quiz_eff_phase(r public.quiz_rooms)
returns text language sql stable security definer set search_path = public
as $$
  select case
    when r.status = 'question' and (
      now() >= r.question_started_at + make_interval(secs => r.time_limit_sec)
      or (
        exists (select 1 from public.quiz_players p where p.room_id = r.id)
        and not exists (
          select 1 from public.quiz_players p
          where p.room_id = r.id
            and not exists (select 1 from public.quiz_answers a
                            where a.player_id = p.id and a.q_index = r.current_index)
        )
      )
    ) then 'reveal'
    else r.status
  end;
$$;

create or replace function public.quiz_secs_left(r public.quiz_rooms)
returns numeric language sql stable
as $$
  select case when r.status = 'question' and r.question_started_at is not null
    then greatest(0, round((r.time_limit_sec - extract(epoch from (now() - r.question_started_at)))::numeric, 1))
    else 0 end;
$$;

-- Bảng xếp hạng: [{id, nickname, score}] giảm dần.
create or replace function public.quiz_leaderboard(p_room bigint, p_limit int default 10)
returns jsonb language sql stable security definer set search_path = public
as $$
  select coalesce(jsonb_agg(t order by (t->>'score')::int desc, t->>'nickname'), '[]'::jsonb) from (
    select jsonb_build_object('id', p.id, 'nickname', p.nickname, 'score', coalesce(sum(a.points), 0)::int) as t
    from public.quiz_players p
    left join public.quiz_answers a on a.player_id = p.id
    where p.room_id = p_room
    group by p.id, p.nickname
    order by coalesce(sum(a.points), 0) desc, p.nickname
    limit greatest(p_limit, 1)
  ) x;
$$;
revoke execute on function public.quiz_eff_phase(public.quiz_rooms) from public, anon, authenticated;
revoke execute on function public.quiz_secs_left(public.quiz_rooms) from public, anon, authenticated;
revoke execute on function public.quiz_leaderboard(bigint, int) from public, anon, authenticated;

-- ---------- Học sinh (ẩn danh) ----------
create or replace function public.quiz_join(p_pin text, p_nickname text)
returns jsonb language plpgsql security definer set search_path = public
as $$
declare
  r public.quiz_rooms;
  v_nick text := regexp_replace(btrim(coalesce(p_nickname, '')), '\s+', ' ', 'g');
  p public.quiz_players;
begin
  if length(v_nick) < 1 or length(v_nick) > 20 then
    raise exception 'nickname_invalid';
  end if;
  select * into r from public.quiz_rooms where pin = btrim(coalesce(p_pin, '')) and status <> 'finished';
  if not found then
    raise exception 'room_not_found';
  end if;
  begin
    insert into public.quiz_players (room_id, nickname) values (r.id, v_nick) returning * into p;
  exception when unique_violation then
    raise exception 'nickname_taken';
  end;
  return jsonb_build_object('room_id', r.id, 'player_id', p.id, 'token', p.token, 'title', r.title, 'nickname', p.nickname);
end; $$;

create or replace function public.quiz_state(p_room bigint, p_token uuid)
returns jsonb language plpgsql stable security definer set search_path = public
as $$
declare
  r public.quiz_rooms;
  p public.quiz_players;
  v_phase text;
  v_q jsonb;
  v_ans public.quiz_answers;
  v_score int := 0;
  v_rank int := 0;
  v_n int := 0;
  v_out jsonb;
begin
  select * into r from public.quiz_rooms where id = p_room;
  if not found then
    return jsonb_build_object('phase', 'gone');
  end if;
  select * into p from public.quiz_players where room_id = p_room and token = p_token;
  if not found then
    return jsonb_build_object('phase', 'kicked');
  end if;
  v_phase := public.quiz_eff_phase(r);
  select coalesce(sum(points), 0)::int into v_score from public.quiz_answers where player_id = p.id;
  select count(*) into v_n from public.quiz_players where room_id = p_room;
  select 1 + count(*) into v_rank from (
    select pl.id, coalesce(sum(a.points), 0) as s
    from public.quiz_players pl left join public.quiz_answers a on a.player_id = pl.id
    where pl.room_id = p_room group by pl.id
  ) x where x.s > v_score;

  v_out := jsonb_build_object(
    'phase', v_phase, 'title', r.title, 'index', r.current_index,
    'total', jsonb_array_length(r.questions), 'time_limit', r.time_limit_sec,
    'seconds_left', public.quiz_secs_left(r), 'players', v_n,
    'nickname', p.nickname, 'score', v_score, 'rank', v_rank);

  if v_phase in ('question', 'reveal') and r.current_index >= 0 then
    v_q := r.questions -> r.current_index;
    select * into v_ans from public.quiz_answers where player_id = p.id and q_index = r.current_index;
    v_out := v_out || jsonb_build_object(
      'question', v_q ->> 'question', 'options', v_q -> 'options',
      'my_choice', case when v_ans.player_id is null then null else v_ans.choice end,
      'my_points', coalesce(v_ans.points, 0));
    if v_phase = 'reveal' then
      v_out := v_out || jsonb_build_object(
        'answer', (v_q ->> 'answer')::int, 'explanation', coalesce(v_q ->> 'explanation', ''),
        'my_correct', coalesce(v_ans.correct, false));
    end if;
  end if;
  if v_phase in ('reveal', 'finished') then
    v_out := v_out || jsonb_build_object('top', public.quiz_leaderboard(p_room, 5));
  end if;
  return v_out;
end; $$;

create or replace function public.quiz_answer(p_room bigint, p_token uuid, p_choice int)
returns jsonb language plpgsql security definer set search_path = public
as $$
declare
  r public.quiz_rooms;
  p public.quiz_players;
  v_q jsonb;
  v_elapsed numeric;
  v_ok boolean;
  v_pts int;
begin
  select * into r from public.quiz_rooms where id = p_room;
  if not found then raise exception 'room_not_found'; end if;
  select * into p from public.quiz_players where room_id = p_room and token = p_token;
  if not found then raise exception 'kicked'; end if;
  if r.status <> 'question' then raise exception 'not_open'; end if;
  v_elapsed := extract(epoch from (now() - r.question_started_at));
  if v_elapsed > r.time_limit_sec + 1.5 then raise exception 'time_up'; end if;
  v_q := r.questions -> r.current_index;
  if p_choice is null or p_choice < 0 or p_choice >= jsonb_array_length(v_q -> 'options') then
    raise exception 'bad_choice';
  end if;
  v_ok := p_choice = (v_q ->> 'answer')::int;
  v_pts := case when v_ok
    then round(1000 - 500 * least(1, greatest(0, v_elapsed / r.time_limit_sec)))::int else 0 end;
  insert into public.quiz_answers (room_id, player_id, q_index, choice, correct, points)
  values (p_room, p.id, r.current_index, p_choice, v_ok, v_pts)
  on conflict (player_id, q_index) do nothing;
  return jsonb_build_object('ok', true);
end; $$;

-- ---------- Người điều khiển (thầy / trợ giảng) ----------
create or replace function public.quiz_host_room(p_room bigint)
returns public.quiz_rooms language plpgsql stable security definer set search_path = public
as $$
declare r public.quiz_rooms;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  select * into r from public.quiz_rooms where id = p_room;
  if not found then raise exception 'room_not_found'; end if;
  if r.host_id is distinct from auth.uid() and not public.is_admin() then raise exception 'forbidden'; end if;
  return r;
end; $$;
revoke execute on function public.quiz_host_room(bigint) from public, anon;

create or replace function public.quiz_host_create(p_set bigint, p_time_limit int default 20)
returns jsonb language plpgsql security definer set search_path = public
as $$
declare
  s public.quiz_sets;
  v_pin text;
  v_id bigint;
  v_tries int := 0;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  select * into s from public.quiz_sets where id = p_set;
  if not found then raise exception 'set_not_found'; end if;
  if jsonb_array_length(s.questions) = 0 then raise exception 'set_empty'; end if;
  -- Dọn phòng bị bỏ quên (>12 giờ chưa kết thúc) để mã PIN không cạn.
  update public.quiz_rooms set status = 'finished' where status <> 'finished' and created_at < now() - interval '12 hours';
  loop
    v_pin := lpad((floor(random() * 1000000))::int::text, 6, '0');
    begin
      insert into public.quiz_rooms (pin, set_id, title, questions, time_limit_sec)
      values (v_pin, s.id, s.title, s.questions, greatest(5, least(120, coalesce(p_time_limit, 20))))
      returning id into v_id;
      exit;
    exception when unique_violation then
      v_tries := v_tries + 1;
      if v_tries > 20 then raise exception 'pin_busy'; end if;
    end;
  end loop;
  return jsonb_build_object('room_id', v_id, 'pin', v_pin);
end; $$;

create or replace function public.quiz_host_state(p_room bigint)
returns jsonb language plpgsql stable security definer set search_path = public
as $$
declare
  r public.quiz_rooms;
  v_phase text;
  v_q jsonb;
  v_out jsonb;
  v_players jsonb;
  v_counts jsonb;
begin
  r := public.quiz_host_room(p_room);
  v_phase := public.quiz_eff_phase(r);
  select coalesce(jsonb_agg(jsonb_build_object(
      'id', p.id, 'nickname', p.nickname,
      'answered', exists (select 1 from public.quiz_answers a where a.player_id = p.id and a.q_index = r.current_index))
    order by p.joined_at), '[]'::jsonb)
  into v_players from public.quiz_players p where p.room_id = p_room;

  v_out := jsonb_build_object(
    'pin', r.pin, 'phase', v_phase, 'title', r.title, 'index', r.current_index,
    'total', jsonb_array_length(r.questions), 'time_limit', r.time_limit_sec,
    'seconds_left', public.quiz_secs_left(r), 'players', v_players);

  if v_phase in ('question', 'reveal') and r.current_index >= 0 then
    v_q := r.questions -> r.current_index;
    select coalesce(jsonb_agg(coalesce(c.n, 0) order by o.i), '[]'::jsonb) into v_counts
    from generate_series(0, jsonb_array_length(v_q -> 'options') - 1) as o(i)
    left join (select choice, count(*) as n from public.quiz_answers
               where room_id = p_room and q_index = r.current_index group by choice) c on c.choice = o.i;
    v_out := v_out || jsonb_build_object('question', v_q ->> 'question', 'options', v_q -> 'options', 'counts', v_counts);
    if v_phase = 'reveal' then
      v_out := v_out || jsonb_build_object('answer', (v_q ->> 'answer')::int, 'explanation', coalesce(v_q ->> 'explanation', ''));
    end if;
  end if;
  if v_phase in ('reveal', 'finished') then
    v_out := v_out || jsonb_build_object('top', public.quiz_leaderboard(p_room, 10));
  end if;
  return v_out;
end; $$;

-- "Tiếp": lobby → câu 1 · đang hỏi → chốt đáp án · đang xem đáp án → câu sau (hết thì kết thúc).
create or replace function public.quiz_host_advance(p_room bigint)
returns void language plpgsql security definer set search_path = public
as $$
declare
  r public.quiz_rooms;
  v_phase text;
begin
  r := public.quiz_host_room(p_room);
  v_phase := public.quiz_eff_phase(r);
  if v_phase = 'finished' then return; end if;
  if v_phase = 'question' then
    update public.quiz_rooms set status = 'reveal' where id = p_room;
  elsif r.current_index + 1 >= jsonb_array_length(r.questions) then
    update public.quiz_rooms set status = 'finished' where id = p_room;
  else
    update public.quiz_rooms
    set status = 'question', current_index = r.current_index + 1, question_started_at = now()
    where id = p_room;
  end if;
end; $$;

create or replace function public.quiz_host_kick(p_room bigint, p_player bigint)
returns void language plpgsql security definer set search_path = public
as $$
begin
  perform public.quiz_host_room(p_room);
  delete from public.quiz_players where id = p_player and room_id = p_room;
end; $$;

create or replace function public.quiz_host_end(p_room bigint)
returns void language plpgsql security definer set search_path = public
as $$
begin
  perform public.quiz_host_room(p_room);
  update public.quiz_rooms set status = 'finished' where id = p_room;
end; $$;

-- ---------- Ngân hàng câu hỏi ↔ bộ câu ----------
-- Trợ giảng không đọc trực tiếp question_bank (RLS chỉ cho admin/giảng viên THPT) nên tìm câu qua hàm này.
-- Chỉ trả trắc nghiệm 4 phương án, chưa lưu trữ, không thiếu hình.
create or replace function public.quiz_bank_search(
  p_grade text default '', p_topic_id bigint default null, p_difficulty text default '',
  p_search text default '', p_limit int default 40, p_random boolean default false)
returns table (id bigint, grade text, topic_id bigint, topic_name text, difficulty text, question jsonb)
language plpgsql stable security definer set search_path = public
as $$
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  return query
  select b.id, b.grade, b.topic_id, b.topic_name, b.difficulty, b.question
  from public.question_bank b
  where b.archived = false and b.qtype = 'multiple_choice'
    and (coalesce(p_grade, '') = '' or b.grade = p_grade)
    and (p_topic_id is null or b.topic_id = p_topic_id
         or b.topic_id in (select t.id from public.question_topics t where t.parent_id = p_topic_id))
    and (coalesce(p_difficulty, '') = '' or b.difficulty = p_difficulty)
    and (coalesce(btrim(p_search), '') = '' or b.question ->> 'question' ilike '%' || btrim(p_search) || '%')
    and jsonb_typeof(b.question -> 'options') = 'array'
    and jsonb_array_length(b.question -> 'options') between 2 and 4
  order by case when p_random then random() end, b.topic_id nulls last, b.id
  limit greatest(1, least(coalesce(p_limit, 40), 200));
end; $$;

-- Đưa các câu TỰ GÕ của bộ vào ngân hàng (câu đã có bank_id thì bỏ qua; trùng nội dung cũng bỏ qua).
create or replace function public.quiz_set_to_bank(
  p_set bigint, p_grade text, p_topic_name text default '', p_form text default '')
returns jsonb language plpgsql security definer set search_path = public
as $$
declare
  s public.quiz_sets;
  q jsonb;
  v_topic public.question_topics;
  v_name text := regexp_replace(btrim(coalesce(p_topic_name, '')), '\s+', ' ', 'g');
  v_form text := case when p_form in ('ly_thuyet', 'bai_tap') then p_form else '' end;
  v_grade text := coalesce(p_grade, '');
  v_added int := 0;
  v_skipped int := 0;
  v_rows int;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  select * into s from public.quiz_sets where id = p_set;
  if not found then raise exception 'set_not_found'; end if;
  if v_name <> '' then
    select * into v_topic from public.question_topics t
    where lower(t.name) = lower(v_name) and (v_grade = '' or t.grade = v_grade)
    order by (t.grade = v_grade) desc, t.id limit 1;
    if found then v_name := v_topic.name; v_grade := v_topic.grade; end if;
  end if;
  for q in select value from jsonb_array_elements(s.questions) loop
    if q ? 'bank_id' or coalesce(q ->> 'type', '') <> 'multiple_choice'
       or jsonb_typeof(q -> 'options') <> 'array'
       or coalesce((q ->> 'answer')::int, -1) not between 0 and jsonb_array_length(q -> 'options') - 1 then
      v_skipped := v_skipped + 1;
      continue;
    end if;
    q := q - 'bank_id' - 'typed';
    if v_name <> '' then q := q || jsonb_build_object('topic', v_name); end if;
    if v_form <> '' then q := q || jsonb_build_object('form', v_form); end if;
    insert into public.question_bank (subject_code, grade, topic_id, topic_name, form, qtype, question, content_hash, note)
    values ('vat-ly', v_grade, case when v_name <> '' then v_topic.id end, v_name, v_form, 'multiple_choice',
            q, public.question_content_hash(q), 'Từ đố vui lớp học: ' || s.title)
    on conflict (content_hash) do nothing;
    get diagnostics v_rows = row_count;
    if v_rows > 0 then v_added := v_added + 1; else v_skipped := v_skipped + 1; end if;
  end loop;
  update public.quiz_sets set banked_at = now() where id = p_set;
  return jsonb_build_object('added', v_added, 'skipped', v_skipped);
end; $$;

-- ---------- Quyền gọi ----------
revoke execute on function public.quiz_join(text, text) from public;
revoke execute on function public.quiz_state(bigint, uuid) from public;
revoke execute on function public.quiz_answer(bigint, uuid, int) from public;
grant execute on function public.quiz_join(text, text) to anon, authenticated;
grant execute on function public.quiz_state(bigint, uuid) to anon, authenticated;
grant execute on function public.quiz_answer(bigint, uuid, int) to anon, authenticated;

revoke execute on function public.quiz_host_create(bigint, int) from public, anon;
revoke execute on function public.quiz_host_state(bigint) from public, anon;
revoke execute on function public.quiz_host_advance(bigint) from public, anon;
revoke execute on function public.quiz_host_kick(bigint, bigint) from public, anon;
revoke execute on function public.quiz_host_end(bigint) from public, anon;
revoke execute on function public.quiz_bank_search(text, bigint, text, text, int, boolean) from public, anon;
revoke execute on function public.quiz_set_to_bank(bigint, text, text, text) from public, anon;
grant execute on function public.quiz_host_create(bigint, int) to authenticated;
grant execute on function public.quiz_host_state(bigint) to authenticated;
grant execute on function public.quiz_host_advance(bigint) to authenticated;
grant execute on function public.quiz_host_kick(bigint, bigint) to authenticated;
grant execute on function public.quiz_host_end(bigint) to authenticated;
grant execute on function public.quiz_bank_search(text, bigint, text, text, int, boolean) to authenticated;
grant execute on function public.quiz_set_to_bank(bigint, text, text, text) to authenticated;

commit;

-- ROLLBACK (không còn dữ liệu đáng giữ — phòng chơi chỉ là tạm):
-- drop function if exists public.quiz_set_to_bank(bigint, text, text, text);
-- drop function if exists public.quiz_bank_search(text, bigint, text, text, int, boolean);
-- drop function if exists public.quiz_host_end(bigint);
-- drop function if exists public.quiz_host_kick(bigint, bigint);
-- drop function if exists public.quiz_host_advance(bigint);
-- drop function if exists public.quiz_host_state(bigint);
-- drop function if exists public.quiz_host_create(bigint, int);
-- drop function if exists public.quiz_host_room(bigint);
-- drop function if exists public.quiz_answer(bigint, uuid, int);
-- drop function if exists public.quiz_state(bigint, uuid);
-- drop function if exists public.quiz_join(text, text);
-- drop function if exists public.quiz_leaderboard(bigint, int);
-- drop function if exists public.quiz_secs_left(public.quiz_rooms);
-- drop function if exists public.quiz_eff_phase(public.quiz_rooms);
-- drop table if exists public.quiz_answers, public.quiz_players, public.quiz_rooms, public.quiz_sets;
