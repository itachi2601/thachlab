-- Đợt 3 rà soát bảo mật 17/10/2026 (docs/RA-SOAT-MA-NGUON-2026-10-17.md mục A2, A3, A4, A6).
-- 1) Bảng rate_hits + hàm rl_allow / rl_client_ip: giới hạn tần suất dùng chung (theo IP hoặc khoá tuỳ ý).
-- 2) resolve_login_email: chặn dò username -> email hàng loạt (giữ nguyên kết quả cho người dùng bình thường).
-- 3) quiz_join: trần số người/phòng và số lượt vào/IP (anon gọi được, trước đây không giới hạn).
-- 4) Vá search_path cho mọi hàm SECURITY DEFINER ở schema public còn thiếu.
-- Trần đặt CAO vì cả lớp thường dùng chung một IP wifi trường. Chạy lúc nào cũng được (không khoá bảng lớn).
-- Hậu kiểm: select count(*) from pg_proc p join pg_namespace n on n.oid=p.pronamespace
--   where n.nspname='public' and p.prosecdef and (p.proconfig is null or not exists
--   (select 1 from unnest(p.proconfig) c where c like 'search_path=%'));   -- phải = 0

-- ───────── 1. Bảng + hàm giới hạn tần suất ─────────
create table if not exists public.rate_hits (
  id bigint generated always as identity primary key,
  key text not null,
  hit_at timestamptz not null default now()
);
create index if not exists rate_hits_key_time on public.rate_hits (key, hit_at desc);
alter table public.rate_hits enable row level security;
revoke all on public.rate_hits from anon, authenticated;

-- IP người gọi, đọc từ header PostgREST. Ưu tiên cf-connecting-ip (do proxy Supabase/Cloudflare đặt,
-- khó giả), rồi x-real-ip, cuối cùng phần tử đầu của x-forwarded-for. Không đọc được thì 'unknown'
-- (mọi người chung một xô — vẫn an toàn, chỉ chặt hơn).
create or replace function public.rl_client_ip()
returns text language plpgsql stable set search_path = public
as $$
declare h json;
begin
  begin
    h := current_setting('request.headers', true)::json;
  exception when others then
    return 'unknown';
  end;
  if h is null then return 'unknown'; end if;
  return coalesce(
    nullif(btrim(h->>'cf-connecting-ip'), ''),
    nullif(btrim(h->>'x-real-ip'), ''),
    nullif(btrim(split_part(coalesce(h->>'x-forwarded-for', ''), ',', 1)), ''),
    'unknown');
end; $$;

-- true = được phép (đã ghi 1 lượt); false = vượt trần trong cửa sổ p_window.
create or replace function public.rl_allow(p_key text, p_max int, p_window interval)
returns boolean language plpgsql volatile security definer set search_path = public
as $$
declare n int;
begin
  select count(*) into n from public.rate_hits where key = p_key and hit_at > now() - p_window;
  if n >= p_max then
    return false;
  end if;
  insert into public.rate_hits (key) values (p_key);
  -- dọn dần, ~2% lượt gọi xoá bản ghi cũ hơn 1 ngày (không cần pg_cron)
  if random() < 0.02 then
    delete from public.rate_hits where hit_at < now() - interval '1 day';
  end if;
  return true;
end; $$;

revoke all on function public.rl_client_ip() from public;
revoke all on function public.rl_allow(text, int, interval) from public;
-- Edge Function (reset-password) gọi bằng service_role; hàm definer khác gọi nội bộ nên không cần cấp thêm.
grant execute on function public.rl_allow(text, int, interval) to service_role;
grant execute on function public.rl_client_ip() to service_role;

-- ───────── 2. resolve_login_email có giới hạn ─────────
-- Giữ nguyên chữ ký và kết quả; thêm trần 200 lượt/10 phút/IP (cả lớp đăng nhập cùng lúc vẫn dư).
-- Vượt trần: raise 'rate_limited' (trang đăng nhập bỏ qua lỗi và rơi về <username>@thachlab.local nên
-- người dùng thấy "sai thông tin" — chấp nhận được trong lúc bị dò).
create or replace function public.resolve_login_email(p_login text)
returns text
language plpgsql
volatile
security definer
set search_path = public, auth
as $$
declare v_email text;
begin
  if not public.rl_allow('login:' || public.rl_client_ip(), 200, interval '10 minutes') then
    raise exception 'rate_limited';
  end if;
  select u.email::text into v_email
  from auth.users u
  where lower(u.raw_user_meta_data->>'username') = lower(btrim(p_login))
  order by u.created_at
  limit 1;
  return v_email;
end; $$;

revoke all on function public.resolve_login_email(text) from public;
grant execute on function public.resolve_login_email(text) to anon, authenticated;

-- ───────── 3. quiz_join có trần ─────────
-- Thân hàm giữ nguyên bản 20261006150000_quiz_live.sql, thêm 2 chốt: ≤ 60 lượt vào/10 phút/IP và ≤ 300 người/phòng.
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
  if not public.rl_allow('quiz_join:' || public.rl_client_ip(), 60, interval '10 minutes') then
    raise exception 'rate_limited';
  end if;
  select * into r from public.quiz_rooms where pin = btrim(coalesce(p_pin, '')) and status <> 'finished';
  if not found then
    raise exception 'room_not_found';
  end if;
  if (select count(*) from public.quiz_players where room_id = r.id) >= 300 then
    raise exception 'room_full';
  end if;
  begin
    insert into public.quiz_players (room_id, nickname) values (r.id, v_nick) returning * into p;
  exception when unique_violation then
    raise exception 'nickname_taken';
  end;
  return jsonb_build_object('room_id', r.id, 'player_id', p.id, 'token', p.token, 'title', r.title, 'nickname', p.nickname);
end; $$;

revoke execute on function public.quiz_join(text, text) from public;
grant execute on function public.quiz_join(text, text) to anon, authenticated;

-- ───────── 4. Vá search_path cho hàm SECURITY DEFINER còn thiếu ─────────
-- 'public, extensions, auth, pg_temp': giữ đủ nơi mà thân hàm cũ có thể gọi không kèm schema
-- (pgcrypto ở extensions, bảng auth) nên không làm hàm nào hỏng, mà vẫn chặn chiếm quyền qua schema
-- của người dùng và đặt pg_temp cuối. Bỏ qua hàm thuộc extension.
do $$
declare r record; n int := 0;
begin
  for r in
    select p.oid::regprocedure as sig
    from pg_proc p
    join pg_namespace ns on ns.oid = p.pronamespace
    where ns.nspname = 'public'
      and p.prosecdef
      and (p.proconfig is null or not exists (select 1 from unnest(p.proconfig) c where c like 'search_path=%'))
      and not exists (select 1 from pg_depend d where d.objid = p.oid and d.deptype = 'e')
  loop
    execute format('alter function %s set search_path = public, extensions, auth, pg_temp', r.sig);
    raise notice 'search_path đã vá: %', r.sig;
    n := n + 1;
  end loop;
  raise notice 'Tổng số hàm đã vá: %', n;
end $$;

-- ROLLBACK (chỉ phần 1–3; phần 4 vô hại, không cần hoàn tác):
--   -- quiz_join: chạy lại thân hàm trong 20261006150000_quiz_live.sql (dòng 127–150).
--   -- resolve_login_email bản cũ:
--   create or replace function public.resolve_login_email(p_login text) returns text language sql stable
--     security definer set search_path = public, auth as $f$
--     select u.email::text from auth.users u where lower(u.raw_user_meta_data->>'username') = lower(btrim(p_login))
--     order by u.created_at limit 1; $f$;
--   drop function if exists public.rl_allow(text, int, interval);
--   drop function if exists public.rl_client_ip();
--   drop table if exists public.rate_hits;
