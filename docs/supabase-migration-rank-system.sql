-- ============================================================
-- Hệ thống rank (RP theo mùa) + bộ sưu tập danh hiệu Vật lý
-- ============================================================
-- Chạy SAU:
--   docs/supabase-migration-exam-analytics.sql        (question_topics, exam_question_results, teaches_student)
--   docs/supabase-migration-topic-outcomes.sql        (question_topics.parent_id — chủ đề 2 tầng)
--   docs/supabase-migration-question-bank.sql         (question_bank, question_content_hash)
--   docs/supabase-migration-lesson-sections-v4.sql    (practice_sessions, lesson_items.bai_tap_ve_nha)
--   docs/supabase-migration-phu-huynh.sql             (is_parent_of)
--   docs/supabase-migration-tutoring-exit-quiz.sql    (tutoring_needs.cleared)
-- Idempotent — chạy lại được. Chỉ CỘNG THÊM: không sửa/xoá bảng điểm, kết quả, lịch sử cũ.
--
-- Ý tưởng
--   * Điểm kiểm tra (exam_results / practice_sessions) giữ nguyên nghĩa — chỉ đọc.
--   * RP là tiến trình TRONG MÙA: mỗi nguồn (bài, tuần, sửa sai) chỉ được cộng PHẦN CHÊNH LỆCH
--     so với mức đã nhận (rank_rp_awards là khoá chống cộng trùng, khoá dòng khi ghi).
--   * Danh hiệu chuyên môn tính trên TOÀN BỘ lịch sử exam_question_results, giữ qua các mùa.
--   * App là static export (không có server) — mọi thứ ở đây chạy trong Postgres
--     (trigger + RPC security definer), client không tự ghi RP/danh hiệu được.
--   * Trigger bọc exception: lỗi logic rank KHÔNG được làm hỏng việc nộp bài của học sinh.
-- ============================================================


-- ============================================================
-- 0. Tiện ích
-- ============================================================

-- Admin hoặc giảng viên THPT — cùng phép với policy "staff manage question topics".
create or replace function public.rank_is_staff()
returns boolean
language sql security definer stable set search_path = public
as $$
  select public.is_admin() or exists (
    select 1 from public.profiles p
    where p.id = auth.uid() and p.role = 'instructor' and p.admin_area = 'thpt'
  );
$$;

-- Ngày/tuần theo giờ Việt Nam (DB chạy UTC).
create or replace function public.rank_vn_date(p_at timestamptz default now())
returns date language sql immutable
as $$ select (p_at at time zone 'Asia/Ho_Chi_Minh')::date; $$;

create or replace function public.rank_week_start(p_at timestamptz default now())
returns date language sql immutable
as $$ select date_trunc('week', (p_at at time zone 'Asia/Ho_Chi_Minh'))::date; $$;

create or replace function public.rank_level_rank(p_level text)
returns int language sql immutable
as $$
  select case p_level when 'thuc_tinh' then 1 when 'lam_chu' then 2 when 'huyen_thoai' then 3 when 'don' then 3 else 0 end;
$$;


-- ============================================================
-- 1. Bảng
-- ============================================================

-- ---------- Mùa ----------
create table if not exists public.rank_seasons (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  created_by uuid references public.profiles (id) on delete set null,
  name text not null,
  starts_on date not null,
  ends_on date not null,
  class_ids bigint[] not null default '{}',            -- rỗng = mọi lớp THPT (có user_classes active)
  status text not null default 'draft' check (status in ('draft', 'active', 'closed')),
  -- practice_max_rp 20 · fix_max_rp 10 · weekly_goal_rp 30 · weekly_goal_count 3 ·
  -- weekly_goal_min_score 7 · fix_pass_pct 80 · fix_min_pool 5 · fix_quiz_count 10
  config jsonb not null default '{}'::jsonb,
  boss_exam_id bigint references public.exams (id) on delete set null,   -- "Trùm Cuối"
  boss_pass_score numeric(4, 2),
  closed_at timestamptz,
  check (ends_on >= starts_on)
);
create index if not exists rank_seasons_active_idx on public.rank_seasons (status, starts_on, ends_on);

create or replace function public.rank_cfg(p_season bigint, p_key text, p_default numeric)
returns numeric
language sql stable set search_path = public
as $$
  select coalesce((s.config ->> p_key)::numeric, p_default)
  from public.rank_seasons s where s.id = p_season;
$$;

-- ---------- Bậc (copy mặc định vào từng mùa, giáo viên sửa min_rp/điều kiện) ----------
create table if not exists public.rank_tiers (
  season_id bigint not null references public.rank_seasons (id) on delete cascade,
  code text not null check (code in ('tan_binh', 'chien_binh', 'tinh_anh', 'tinh_nhue', 'dai_su', 'cao_thu', 'thach_dau')),
  sort int not null,
  name text not null,
  min_rp int not null check (min_rp >= 0),
  has_divisions boolean not null default true,
  required_title_count int not null default 0,
  required_title_level text check (required_title_level in ('thuc_tinh', 'lam_chu', 'huyen_thoai')),
  challenge_exam_id bigint references public.exams (id) on delete set null,
  challenge_pass_score numeric(4, 2),
  primary key (season_id, code)
);

-- Ngưỡng phải tăng dần theo bậc — không cho hở/chồng.
create or replace function public.rank_tiers_guard()
returns trigger language plpgsql set search_path = public
as $$
begin
  if exists (
    select 1 from public.rank_tiers t
    where t.season_id = new.season_id and t.code <> new.code
      and ((t.sort < new.sort and t.min_rp >= new.min_rp) or (t.sort > new.sort and t.min_rp <= new.min_rp))
  ) then
    raise exception 'Ngưỡng RP của bậc "%" phải lớn hơn bậc dưới và nhỏ hơn bậc trên', new.name;
  end if;
  if new.required_title_count > 0 and new.required_title_level is null then
    new.required_title_level := 'thuc_tinh';
  end if;
  return new;
end; $$;
drop trigger if exists trg_rank_tiers_guard on public.rank_tiers;
create trigger trg_rank_tiers_guard before insert or update on public.rank_tiers
  for each row execute function public.rank_tiers_guard();

create or replace function public.rank_seed_tiers(p_season bigint)
returns void
language sql security definer set search_path = public
as $$
  insert into public.rank_tiers (season_id, code, sort, name, min_rp, has_divisions, required_title_count, required_title_level)
  values
    (p_season, 'tan_binh',   1, 'Tinh Quang',   0,    true,  0, null),
    (p_season, 'chien_binh', 2, 'Tiên Phong', 200,  true,  0, null),
    (p_season, 'tinh_anh',   3, 'Nhật Hoa',   500,  true,  1, 'thuc_tinh'),
    (p_season, 'tinh_nhue',  4, 'Vương Lễ',  900,  true,  2, 'thuc_tinh'),
    (p_season, 'dai_su',     5, 'Vương Triều',     1400, true,  1, 'lam_chu'),
    (p_season, 'cao_thu',    6, 'Thiên Thể',    2000, false, 2, 'lam_chu'),
    (p_season, 'thach_dau',  7, 'Chí Tôn',  2600, false, 3, 'lam_chu')
  on conflict (season_id, code) do nothing;
$$;

-- Một mùa chỉ active khi không đè lên mùa active khác của cùng lớp.
create or replace function public.rank_seasons_guard()
returns trigger language plpgsql set search_path = public
as $$
begin
  if new.status = 'active' and exists (
    select 1 from public.rank_seasons s
    where s.id <> new.id and s.status = 'active'
      and s.starts_on <= new.ends_on and s.ends_on >= new.starts_on
      and (cardinality(s.class_ids) = 0 or cardinality(new.class_ids) = 0 or s.class_ids && new.class_ids)
  ) then
    raise exception 'Đã có mùa khác đang mở cho lớp này trong cùng khoảng thời gian';
  end if;
  if new.status = 'closed' and new.closed_at is null then
    new.closed_at := now();
  end if;
  return new;
end; $$;
drop trigger if exists trg_rank_seasons_guard on public.rank_seasons;
create trigger trg_rank_seasons_guard before insert or update on public.rank_seasons
  for each row execute function public.rank_seasons_guard();

-- ---------- Bài được tính RP ----------
create table if not exists public.rank_sources (
  season_id bigint not null references public.rank_seasons (id) on delete cascade,
  source_kind text not null check (source_kind in ('practice_item', 'exam')),
  source_id bigint not null,          -- lesson_items.id (luyen_tap) | exams.id (BTVN / kiểm tra)
  max_rp int not null default 20 check (max_rp between 0 and 200),
  enabled boolean not null default true,
  primary key (season_id, source_kind, source_id)
);

-- ---------- Khoá chống cộng trùng: mức đã nhận cho từng nguồn ----------
create table if not exists public.rank_rp_awards (
  season_id bigint not null references public.rank_seasons (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  source_kind text not null check (source_kind in ('practice', 'fix', 'weekly_goal', 'manual')),
  source_ref text not null,           -- 'exam:12' | 'practice_item:7' | 'exam_result:99' | '2026-09-21' | 'manual'
  awarded int not null default 0,
  best_value numeric(6, 2),
  updated_at timestamptz not null default now(),
  primary key (season_id, student_id, source_kind, source_ref)
);
create index if not exists rank_rp_awards_student_idx on public.rank_rp_awards (season_id, student_id);

-- ---------- Lịch sử mọi thay đổi RP ----------
create table if not exists public.rank_rp_ledger (
  id bigint generated always as identity primary key,
  season_id bigint not null references public.rank_seasons (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  source_kind text not null,
  source_ref text not null default '',
  amount int not null,
  reason text not null default '',
  ref_result_id bigint,
  actor uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now()
);
create index if not exists rank_rp_ledger_student_idx on public.rank_rp_ledger (season_id, student_id, created_at desc);
create index if not exists rank_rp_ledger_season_time_idx on public.rank_rp_ledger (season_id, created_at desc);

-- ---------- Trạng thái học sinh trong mùa ----------
create table if not exists public.rank_student_seasons (
  season_id bigint not null references public.rank_seasons (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  rp int not null default 0,
  tier_code text not null default 'tan_binh',
  tier_sort int not null default 1,
  division int,
  tier_reached_at timestamptz,
  joined_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (season_id, student_id)
);

-- ---------- Điều kiện lên hạng đã vượt ----------
create table if not exists public.rank_gate_passes (
  season_id bigint not null references public.rank_seasons (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  tier_code text not null,
  passed_at timestamptz not null default now(),
  evidence jsonb not null default '{}'::jsonb,
  primary key (season_id, student_id, tier_code)
);

-- ---------- Danh mục danh hiệu ----------
create table if not exists public.rank_titles (
  code text primary key,
  group_code text not null check (group_code in ('co_hoc', 'dao_dong_song', 'dien_tu', 'nhiet_hoc', 'hien_dai', 'bo_suu_tap', 'thanh_tich')),
  kind text not null check (kind in ('specialist', 'collection', 'achievement')),
  name text not null,
  description text not null default '',
  sort int not null default 0,
  min_questions int not null default 12,       -- Thức Tỉnh: số câu tối thiểu (Làm Chủ: gấp đôi)
  awaken_accuracy int not null default 60,     -- % đúng cho Thức Tỉnh
  master_accuracy int not null default 80,     -- % đúng cho Làm Chủ
  legend_challenge_exam_id bigint references public.exams (id) on delete set null,
  legend_accuracy int not null default 90,     -- % điểm đề thử thách cho Huyền Thoại
  requires jsonb not null default '{}'::jsonb, -- collection: {"titles":[...], "level":"lam_chu"} | {"collections":true}
  enabled boolean not null default true
);

create table if not exists public.rank_title_topics (
  title_code text not null references public.rank_titles (code) on delete cascade,
  topic_id bigint not null references public.question_topics (id) on delete cascade,
  primary key (title_code, topic_id)
);
create index if not exists rank_title_topics_topic_idx on public.rank_title_topics (topic_id);

-- ---------- Danh hiệu đã cấp (mỗi mức một dòng — giữ lịch sử) ----------
create table if not exists public.rank_title_awards (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.profiles (id) on delete cascade,
  title_code text not null references public.rank_titles (code) on delete cascade,
  level text not null check (level in ('thuc_tinh', 'lam_chu', 'huyen_thoai', 'don')),
  season_id bigint references public.rank_seasons (id) on delete set null,
  evidence jsonb not null default '{}'::jsonb,
  awarded_at timestamptz not null default now(),
  unique (student_id, title_code, level)
);
create index if not exists rank_title_awards_student_idx on public.rank_title_awards (student_id, awarded_at desc);

-- ---------- Bài sửa sai ----------
create table if not exists public.rank_fix_attempts (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.profiles (id) on delete cascade,
  season_id bigint not null references public.rank_seasons (id) on delete cascade,
  exam_result_id bigint not null references public.exam_results (id) on delete cascade,
  exam_id bigint not null references public.exams (id) on delete cascade,
  topic_id bigint not null references public.question_topics (id) on delete cascade,  -- tầng bài
  question_ids bigint[] not null default '{}',
  total int not null check (total > 0),
  correct int not null default 0 check (correct >= 0),
  pct int not null default 0,
  passed boolean not null default false,
  status text not null default 'open' check (status in ('open', 'done')),
  created_at timestamptz not null default now(),
  submitted_at timestamptz
);
create index if not exists rank_fix_attempts_result_idx on public.rank_fix_attempts (exam_result_id, topic_id);

-- ---------- Lưu trữ khi đóng mùa ----------
create table if not exists public.rank_season_results (
  season_id bigint not null references public.rank_seasons (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  rp int not null,
  tier_code text not null,
  division int,
  titles_count int not null default 0,
  closed_at timestamptz not null default now(),
  primary key (season_id, student_id)
);

-- ---------- Danh hiệu đang đeo ----------
alter table public.profiles add column if not exists display_title_code text references public.rank_titles (code) on delete set null;
alter table public.profiles add column if not exists display_title_level text;

-- Chỉ đeo danh hiệu mình có — chặn ở trigger nên không phụ thuộc policy update của profiles.
create or replace function public.rank_display_title_guard()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if new.display_title_code is distinct from old.display_title_code
     or new.display_title_level is distinct from old.display_title_level then
    if new.display_title_code is null then
      new.display_title_level := null;
    elsif not public.is_admin() and not exists (
      select 1 from public.rank_title_awards a
      where a.student_id = new.id and a.title_code = new.display_title_code and a.level = new.display_title_level
    ) then
      raise exception 'Em chưa sở hữu danh hiệu này';
    end if;
  end if;
  return new;
end; $$;
drop trigger if exists trg_rank_display_title_guard on public.profiles;
create trigger trg_rank_display_title_guard before update on public.profiles
  for each row execute function public.rank_display_title_guard();


-- ============================================================
-- 2. RLS
-- ============================================================
alter table public.rank_seasons enable row level security;
alter table public.rank_tiers enable row level security;
alter table public.rank_sources enable row level security;
alter table public.rank_titles enable row level security;
alter table public.rank_title_topics enable row level security;
alter table public.rank_rp_awards enable row level security;
alter table public.rank_rp_ledger enable row level security;
alter table public.rank_student_seasons enable row level security;
alter table public.rank_gate_passes enable row level security;
alter table public.rank_title_awards enable row level security;
alter table public.rank_fix_attempts enable row level security;
alter table public.rank_season_results enable row level security;

-- Cấu hình: ai đăng nhập cũng đọc được; admin/GV THPT sửa.
do $$
declare t text;
begin
  foreach t in array array['rank_seasons', 'rank_tiers', 'rank_sources', 'rank_titles', 'rank_title_topics'] loop
    execute format('drop policy if exists "anyone reads %1$s" on public.%1$I', t);
    execute format('create policy "anyone reads %1$s" on public.%1$I for select to authenticated using (true)', t);
    execute format('drop policy if exists "staff manage %1$s" on public.%1$s', t);
    execute format('create policy "staff manage %1$s" on public.%1$I for all to authenticated using (public.rank_is_staff()) with check (public.rank_is_staff())', t);
  end loop;
end $$;

-- Dữ liệu học sinh: chính em / giáo viên của em / phụ huynh đọc; KHÔNG có policy ghi cho
-- người dùng thường — mọi ghi đi qua trigger/RPC security definer.
do $$
declare t text;
begin
  foreach t in array array['rank_rp_awards', 'rank_rp_ledger', 'rank_student_seasons', 'rank_gate_passes', 'rank_title_awards', 'rank_fix_attempts', 'rank_season_results'] loop
    execute format('drop policy if exists "read own %1$s" on public.%1$I', t);
    execute format('create policy "read own %1$s" on public.%1$I for select to authenticated using (student_id = auth.uid() or public.teaches_student(student_id) or public.is_parent_of(student_id))', t);
    execute format('drop policy if exists "admin manages %1$s" on public.%1$I', t);
    execute format('create policy "admin manages %1$s" on public.%1$I for all to authenticated using (public.is_admin()) with check (public.is_admin())', t);
  end loop;
end $$;


-- ============================================================
-- 3. Mùa & bậc — tra cứu
-- ============================================================

-- Mùa đang mở cho học sinh tại thời điểm p_at (theo lớp em đang active).
create or replace function public.rank_season_for_at(p_student uuid, p_at timestamptz default now())
returns bigint
language sql stable set search_path = public
as $$
  select s.id
  from public.rank_seasons s
  where s.status = 'active'
    and public.rank_vn_date(p_at) between s.starts_on and s.ends_on
    and exists (
      select 1 from public.user_classes uc
      where uc.user_id = p_student and uc.status = 'active'
        and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids))
    )
  order by s.starts_on desc
  limit 1;
$$;

-- Bậc theo RP thuần (chưa xét điều kiện).
create or replace function public.rank_tier_code_by_rp(p_season bigint, p_rp int)
returns text
language sql stable set search_path = public
as $$
  select t.code from public.rank_tiers t
  where t.season_id = p_season and t.min_rp <= p_rp
  order by t.sort desc limit 1;
$$;

-- Thông tin bậc + phân bậc III/II/I cho một bậc cụ thể tại mức RP (kẹp RP trong dải bậc).
-- Phân bậc = chia 3 đoạn [min_rp, next_min-1]: III thấp nhất, I cao nhất — không hở, không chồng.
create or replace function public.rank_tier_info(p_season bigint, p_code text, p_rp int)
returns table(code text, name text, sort int, tier_min int, next_min int, division int, div_min int, div_max int)
language plpgsql stable set search_path = public
as $$
declare
  v record;
  v_rp int;
  v_w int;
begin
  select t.code, t.name, t.sort, t.min_rp, t.has_divisions,
         (select min(n.min_rp) from public.rank_tiers n where n.season_id = p_season and n.sort > t.sort) as next_min
  into v
  from public.rank_tiers t where t.season_id = p_season and t.code = p_code;
  if not found then return; end if;

  code := v.code; name := v.name; sort := v.sort; tier_min := v.min_rp; next_min := v.next_min;
  if not v.has_divisions or v.next_min is null then
    division := null; div_min := v.min_rp; div_max := v.next_min - 1;
    return next; return;
  end if;
  v_rp := least(greatest(p_rp, v.min_rp), v.next_min - 1);
  v_w := (v.next_min - v.min_rp) / 3;
  if v_rp >= v.min_rp + 2 * v_w then
    division := 1; div_min := v.min_rp + 2 * v_w; div_max := v.next_min - 1;
  elsif v_rp >= v.min_rp + v_w then
    division := 2; div_min := v.min_rp + v_w; div_max := v.min_rp + 2 * v_w - 1;
  else
    division := 3; div_min := v.min_rp; div_max := v.min_rp + v_w - 1;
  end if;
  return next;
end; $$;

create or replace function public.rank_tier_needs_gate(t public.rank_tiers)
returns boolean language sql immutable
as $$
  select t.required_title_count > 0 or t.challenge_exam_id is not null or t.code in ('cao_thu', 'thach_dau');
$$;


-- ============================================================
-- 4. Lõi cộng RP (chỉ cộng phần chênh lệch, khoá dòng)
-- ============================================================
create or replace function public.rank_score_to_rp(p_score numeric, p_max int)
returns int language sql immutable
as $$ select greatest(0, least(p_max, round(coalesce(p_score, 0) / 10 * p_max)))::int; $$;

create or replace function public.rank_ensure_member(p_season bigint, p_student uuid)
returns void
language sql security definer set search_path = public
as $$
  insert into public.rank_student_seasons (season_id, student_id)
  values (p_season, p_student)
  on conflict (season_id, student_id) do nothing;
$$;

-- Trả về số RP thực cộng (0 nếu không vượt mức đã nhận). Hai giao dịch đồng thời cùng nguồn
-- xếp hàng ở "for update" nên giao dịch sau thấy mức mới -> delta 0, không cộng trùng.
create or replace function public.rank_award(
  p_season bigint, p_student uuid, p_kind text, p_ref text,
  p_value int, p_reason text, p_result_ref bigint default null
)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_old int;
  v_delta int;
begin
  insert into public.rank_rp_awards (season_id, student_id, source_kind, source_ref, awarded)
  values (p_season, p_student, p_kind, p_ref, 0)
  on conflict (season_id, student_id, source_kind, source_ref) do nothing;

  select awarded into v_old from public.rank_rp_awards
  where season_id = p_season and student_id = p_student and source_kind = p_kind and source_ref = p_ref
  for update;

  v_delta := p_value - v_old;
  if v_delta <= 0 then
    return 0;
  end if;

  update public.rank_rp_awards
    set awarded = p_value, best_value = greatest(coalesce(best_value, 0), p_value), updated_at = now()
  where season_id = p_season and student_id = p_student and source_kind = p_kind and source_ref = p_ref;

  insert into public.rank_rp_ledger (season_id, student_id, source_kind, source_ref, amount, reason, ref_result_id)
  values (p_season, p_student, p_kind, p_ref, v_delta, p_reason, p_result_ref);

  return v_delta;
end; $$;

-- Tính lại RP tổng + bậc/phân bậc. Bậc = bậc cao nhất có min_rp <= RP mà MỌI bậc có điều kiện
-- từ đó trở xuống đều đã vượt (rank_gate_passes). Đủ RP nhưng kẹt điều kiện -> đứng ở phân bậc I
-- của bậc hiện tại (UI nói rõ còn thiếu gì).
create or replace function public.rank_refresh_student(p_season bigint, p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_rp int;
  v_tier public.rank_tiers%rowtype;
  v_code text := 'tan_binh';
  v_sort int := 1;
  v_info record;
  v_old_sort int;
begin
  perform public.rank_ensure_member(p_season, p_student);

  select coalesce(sum(awarded), 0) into v_rp
  from public.rank_rp_awards where season_id = p_season and student_id = p_student;
  v_rp := greatest(v_rp, 0);

  for v_tier in
    select * from public.rank_tiers where season_id = p_season and min_rp <= v_rp order by sort
  loop
    if public.rank_tier_needs_gate(v_tier) and not exists (
      select 1 from public.rank_gate_passes g
      where g.season_id = p_season and g.student_id = p_student and g.tier_code = v_tier.code
    ) then
      exit;
    end if;
    v_code := v_tier.code;
    v_sort := v_tier.sort;
  end loop;

  select * into v_info from public.rank_tier_info(p_season, v_code, v_rp);
  select tier_sort into v_old_sort from public.rank_student_seasons where season_id = p_season and student_id = p_student;

  update public.rank_student_seasons
    set rp = v_rp,
        tier_code = v_code,
        tier_sort = v_sort,
        division = v_info.division,
        tier_reached_at = case when v_sort > coalesce(v_old_sort, 0) then now() else tier_reached_at end,
        updated_at = now()
  where season_id = p_season and student_id = p_student;
end; $$;


-- ============================================================
-- 5. Mục tiêu tuần
-- ============================================================
-- Tuần Thứ Hai → Chủ Nhật (giờ VN). Đạt khi có >= N bài tính RP (khác nhau) mà kết quả tốt
-- nhất trong tuần >= điểm tối thiểu. Cộng một lần/tuần (source_ref = ngày đầu tuần).
create or replace function public.rank_eval_weekly_goal(p_season bigint, p_student uuid, p_at timestamptz)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_week date := public.rank_week_start(p_at);
  v_from timestamptz := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to timestamptz := ((v_week + 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_need int := public.rank_cfg(p_season, 'weekly_goal_count', 3)::int;
  v_min numeric := public.rank_cfg(p_season, 'weekly_goal_min_score', 7);
  v_rp int := public.rank_cfg(p_season, 'weekly_goal_rp', 30)::int;
  v_count int;
  s public.rank_seasons%rowtype;
begin
  select * into s from public.rank_seasons where id = p_season;
  if v_week < s.starts_on or v_week > s.ends_on then
    return 0;
  end if;

  select count(*) into v_count from (
    select 'exam' as k, er.exam_id as id
    from public.exam_results er
    join public.rank_sources rs on rs.season_id = p_season and rs.enabled and rs.source_kind = 'exam' and rs.source_id = er.exam_id
    where er.student_id = p_student and er.created_at >= v_from and er.created_at < v_to
    group by er.exam_id having max(er.score) >= v_min
    union
    select 'practice_item', ps.item_id
    from public.practice_sessions ps
    join public.rank_sources rs on rs.season_id = p_season and rs.enabled and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id
    where ps.student_id = p_student and ps.created_at >= v_from and ps.created_at < v_to
    group by ps.item_id having max(ps.score) >= v_min
  ) x;

  if v_count >= v_need then
    return public.rank_award(p_season, p_student, 'weekly_goal', v_week::text, v_rp,
      'Mục tiêu tuần ' || to_char(v_week, 'DD/MM') || ': ' || v_count || ' bài đạt từ ' || replace(v_min::text, '.', ','), null);
  end if;
  return 0;
end; $$;


-- ============================================================
-- 6. Danh hiệu chuyên môn & bộ sưu tập (toàn bộ lịch sử, không theo mùa)
-- ============================================================
-- Thống kê của một học sinh trên một danh hiệu: số câu, số đúng, số chủ đề đã "chạm" (>= 3 câu).
create or replace function public.rank_title_stats(p_student uuid, p_title text)
returns table(n int, correct int, covered int, total_topics int, acc int)
language sql stable set search_path = public
as $$
  with topics as (
    select tt.topic_id from public.rank_title_topics tt where tt.title_code = p_title
  ),
  rows_ as (
    select coalesce(t.parent_id, t.id) as lesson_topic, eqr.is_correct
    from public.exam_question_results eqr
    join public.question_topics t on t.id = eqr.topic_id
    where eqr.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
  ),
  per_topic as (
    select lesson_topic, count(*) as c from rows_ group by lesson_topic
  )
  select
    (select count(*) from rows_)::int,
    (select count(*) filter (where is_correct) from rows_)::int,
    (select count(*) from per_topic where c >= 3)::int,
    (select count(*) from topics)::int,
    case when (select count(*) from rows_) > 0
      then round((select count(*) filter (where is_correct) from rows_) * 100.0 / (select count(*) from rows_))::int
      else 0 end;
$$;

-- % điểm tốt nhất của học sinh trên một đề (0..100), null nếu chưa làm.
create or replace function public.rank_best_pct(p_student uuid, p_exam bigint, p_from timestamptz default null, p_to timestamptz default null)
returns int
language sql stable set search_path = public
as $$
  select round(max(er.score) * 10)::int
  from public.exam_results er
  where er.student_id = p_student and er.exam_id = p_exam
    and (p_from is null or er.created_at >= p_from)
    and (p_to is null or er.created_at < p_to);
$$;

create or replace function public.rank_grant_title(p_student uuid, p_title text, p_level text, p_season bigint, p_evidence jsonb)
returns boolean
language plpgsql security definer set search_path = public
as $$
begin
  insert into public.rank_title_awards (student_id, title_code, level, season_id, evidence)
  values (p_student, p_title, p_level, p_season, coalesce(p_evidence, '{}'::jsonb))
  on conflict (student_id, title_code, level) do nothing;
  return found;
end; $$;

-- Danh hiệu "active": có ít nhất một chủ đề ánh xạ (đúng chương trình thực tế).
create or replace function public.rank_title_is_active(p_title text)
returns boolean
language sql stable set search_path = public
as $$
  select exists (select 1 from public.rank_title_topics tt where tt.title_code = p_title);
$$;

create or replace function public.rank_eval_titles(p_student uuid, p_season bigint default null)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  t public.rank_titles%rowtype;
  st record;
  v_legend int;
  v_have_master boolean;
  v_level text;
  v_req_titles text[];
  v_req_level text;
  v_ok boolean;
begin
  -- (a) chuyên môn: Thức Tỉnh → Làm Chủ → Huyền Thoại
  for t in select * from public.rank_titles where kind = 'specialist' and enabled and public.rank_title_is_active(code) loop
    select * into st from public.rank_title_stats(p_student, t.code);
    if st.n >= t.min_questions and st.covered * 2 >= st.total_topics and st.acc >= t.awaken_accuracy then
      perform public.rank_grant_title(p_student, t.code, 'thuc_tinh', p_season, jsonb_build_object('n', st.n, 'acc', st.acc, 'covered', st.covered, 'total', st.total_topics));
    end if;
    if st.n >= t.min_questions * 2 and st.covered = st.total_topics and st.acc >= t.master_accuracy then
      perform public.rank_grant_title(p_student, t.code, 'lam_chu', p_season, jsonb_build_object('n', st.n, 'acc', st.acc, 'covered', st.covered, 'total', st.total_topics));
      if t.legend_challenge_exam_id is not null then
        v_legend := public.rank_best_pct(p_student, t.legend_challenge_exam_id);
        if v_legend >= t.legend_accuracy then
          perform public.rank_grant_title(p_student, t.code, 'huyen_thoai', p_season, jsonb_build_object('exam_id', t.legend_challenge_exam_id, 'pct', v_legend));
        end if;
      end if;
    end if;
  end loop;

  -- (b) bộ sưu tập: mọi danh hiệu thành phần ĐANG ACTIVE đạt từ mức yêu cầu
  for t in select * from public.rank_titles where kind = 'collection' and enabled and (requires ? 'titles') loop
    select array_agg(x) into v_req_titles from jsonb_array_elements_text(t.requires -> 'titles') x;
    v_req_level := coalesce(t.requires ->> 'level', 'lam_chu');
    if not exists (select 1 from unnest(v_req_titles) c where public.rank_title_is_active(c)) then
      continue;
    end if;
    select bool_and(exists (
      select 1 from public.rank_title_awards a
      where a.student_id = p_student and a.title_code = c and public.rank_level_rank(a.level) >= public.rank_level_rank(v_req_level)
    )) into v_ok
    from unnest(v_req_titles) c where public.rank_title_is_active(c);
    if coalesce(v_ok, false) then
      perform public.rank_grant_title(p_student, t.code, 'don', p_season, jsonb_build_object('level', v_req_level));
    end if;
  end loop;

  -- (c) "Kẻ Giải Mã Vũ Trụ": mọi bộ sưu tập đang khả dụng
  for t in select * from public.rank_titles where kind = 'collection' and enabled and coalesce((requires ->> 'collections')::boolean, false) loop
    select bool_and(exists (
      select 1 from public.rank_title_awards a where a.student_id = p_student and a.title_code = c.code
    )) into v_ok
    from public.rank_titles c
    where c.kind = 'collection' and c.enabled and (c.requires ? 'titles')
      and exists (select 1 from jsonb_array_elements_text(c.requires -> 'titles') x where public.rank_title_is_active(x));
    if coalesce(v_ok, false) then
      perform public.rank_grant_title(p_student, t.code, 'don', p_season, '{}'::jsonb);
    end if;
  end loop;
end; $$;


-- ============================================================
-- 7. Điều kiện lên hạng
-- ============================================================
create or replace function public.rank_titles_at_level(p_student uuid, p_level text)
returns int
language sql stable set search_path = public
as $$
  select count(distinct a.title_code)::int
  from public.rank_title_awards a
  join public.rank_titles t on t.code = a.title_code and t.kind = 'specialist' and t.enabled
  where a.student_id = p_student and public.rank_level_rank(a.level) >= public.rank_level_rank(p_level);
$$;

create or replace function public.rank_eval_gates(p_season bigint, p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  t public.rank_tiers%rowtype;
  s public.rank_seasons%rowtype;
  v_titles int;
  v_pct int;
  v_titles_ok boolean;
  v_chal_ok boolean;
begin
  select * into s from public.rank_seasons where id = p_season;
  for t in select * from public.rank_tiers where season_id = p_season order by sort loop
    if not public.rank_tier_needs_gate(t) then continue; end if;
    if exists (select 1 from public.rank_gate_passes g where g.season_id = p_season and g.student_id = p_student and g.tier_code = t.code) then
      continue;
    end if;

    v_titles := public.rank_titles_at_level(p_student, coalesce(t.required_title_level, 'thuc_tinh'));
    v_titles_ok := v_titles >= t.required_title_count;

    if t.challenge_exam_id is null then
      -- Thiên Thể / Chí Tôn bắt buộc có thử thách; chưa gán -> chưa thể vượt.
      v_chal_ok := t.code not in ('cao_thu', 'thach_dau');
      v_pct := null;
    else
      v_pct := public.rank_best_pct(p_student, t.challenge_exam_id,
        (s.starts_on::timestamp) at time zone 'Asia/Ho_Chi_Minh',
        ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh');
      v_chal_ok := v_pct is not null and v_pct >= round(coalesce(t.challenge_pass_score, 8) * 10);
    end if;

    if v_titles_ok and v_chal_ok then
      insert into public.rank_gate_passes (season_id, student_id, tier_code, evidence)
      values (p_season, p_student, t.code, jsonb_build_object('titles', v_titles, 'challenge_pct', v_pct))
      on conflict do nothing;
    end if;
  end loop;
end; $$;


-- ============================================================
-- 8. Danh hiệu thành tích
-- ============================================================
create or replace function public.rank_eval_achievements(p_season bigint, p_student uuid, p_at timestamptz)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  s public.rank_seasons%rowtype;
  v_week date := public.rank_week_start(p_at);
  v_this int;
  v_prev numeric;
  v_prev_weeks int;
  v_streak int;
  v_n int;
  v_pct int;
  r record;
  v_from timestamptz;
  v_to timestamptz;
begin
  select * into s from public.rank_seasons where id = p_season;
  v_from := (s.starts_on::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to := ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh';

  -- Bứt Phá Thần Tốc: RP tuần này >= 60 và >= 2× trung bình 3 tuần liền trước (đủ 3 tuần trong mùa, TB >= 10).
  if v_week - 21 >= s.starts_on then
    select coalesce(sum(amount), 0) into v_this from public.rank_rp_ledger
      where season_id = p_season and student_id = p_student and source_kind <> 'manual'
        and public.rank_week_start(created_at) = v_week;
    select coalesce(sum(amount), 0) / 3.0 into v_prev from public.rank_rp_ledger
      where season_id = p_season and student_id = p_student and source_kind <> 'manual'
        and public.rank_week_start(created_at) between v_week - 21 and v_week - 7;
    if v_this >= 60 and v_prev >= 10 and v_this >= 2 * v_prev then
      perform public.rank_grant_title(p_student, 'but_pha_than_toc', 'don', p_season, jsonb_build_object('week', v_week, 'rp', v_this, 'prev_avg', round(v_prev)));
    end if;
  end if;

  -- Chiến Binh Bất Diệt: đạt mục tiêu 4 tuần liên tiếp.
  v_streak := 0;
  for r in
    select source_ref::date as w from public.rank_rp_awards
    where season_id = p_season and student_id = p_student and source_kind = 'weekly_goal' and awarded > 0
    order by 1 desc
  loop
    if v_streak = 0 or r.w = v_week - 7 * v_streak then
      v_week := case when v_streak = 0 then r.w else v_week end;
      v_streak := v_streak + 1;
    else
      exit;
    end if;
  end loop;
  if v_streak >= 4 then
    perform public.rank_grant_title(p_student, 'chien_binh_bat_diet', 'don', p_season, jsonb_build_object('weeks', v_streak));
  end if;

  -- Bách Phát Bách Trúng: >= 3 đề thử thách (bậc / Huyền Thoại / trùm) đạt 100% trong mùa.
  select count(*) into v_n from (
    select e.exam_id from (
      select challenge_exam_id as exam_id from public.rank_tiers where season_id = p_season and challenge_exam_id is not null
      union select legend_challenge_exam_id from public.rank_titles where legend_challenge_exam_id is not null
      union select s.boss_exam_id where s.boss_exam_id is not null
    ) e
    where public.rank_best_pct(p_student, e.exam_id, v_from, v_to) >= 100
  ) x;
  if v_n >= 3 then
    perform public.rank_grant_title(p_student, 'bach_phat_bach_trung', 'don', p_season, jsonb_build_object('exams', v_n));
  end if;

  -- Lật Kèo Ngoạn Mục: một chủ đề tầng bài từng <50% (8 câu đầu) rồi >=80% (8 câu gần nhất, tổng >=16);
  -- hoặc đã tự thoát phụ đạo bằng bài kiểm tra.
  if exists (
    select 1 from public.tutoring_needs n
    where n.student_id = p_student and n.status = 'cleared' and n.note like 'Tự kiểm tra%'
  ) or exists (
    with rows_ as (
      select coalesce(t.parent_id, t.id) as lt, eqr.is_correct,
             row_number() over (partition by coalesce(t.parent_id, t.id) order by eqr.created_at, eqr.question_index) as rn,
             count(*) over (partition by coalesce(t.parent_id, t.id)) as cnt
      from public.exam_question_results eqr
      join public.question_topics t on t.id = eqr.topic_id
      where eqr.student_id = p_student
    )
    select lt from rows_ where cnt >= 16 group by lt
    having avg(case when rn <= 8 then (is_correct)::int end) < 0.5
       and avg(case when rn > cnt - 8 then (is_correct)::int end) >= 0.8
  ) then
    perform public.rank_grant_title(p_student, 'lat_keo_ngoan_muc', 'don', p_season, '{}'::jsonb);
  end if;

  -- Phá Đảo Chuyên Đề: một chương mà mọi chủ đề tầng bài đều >= 5 câu, >= 85% đúng, và có cả lý thuyết lẫn bài tập.
  for r in
    with lt as (
      select t.id as topic_id, t.chapter_id from public.question_topics t where t.parent_id is null and t.chapter_id is not null
    ),
    per as (
      select lt.chapter_id, lt.topic_id,
             count(eqr.*) as n,
             count(*) filter (where eqr.is_correct) as c,
             count(distinct eqr.form) filter (where eqr.form in ('ly_thuyet', 'bai_tap')) as forms
      from lt
      left join public.question_topics ch on coalesce(ch.parent_id, ch.id) = lt.topic_id
      left join public.exam_question_results eqr on eqr.topic_id = ch.id and eqr.student_id = p_student
      group by lt.chapter_id, lt.topic_id
    )
    select chapter_id from per
    group by chapter_id
    having bool_and(n >= 5 and c * 100 >= n * 85) and max(forms) = 2
    limit 1
  loop
    perform public.rank_grant_title(p_student, 'pha_dao_chuyen_de', 'don', p_season, jsonb_build_object('chapter_id', r.chapter_id));
  end loop;

  -- Trùm Cuối: vượt đề khó nhất mùa.
  if s.boss_exam_id is not null then
    v_pct := public.rank_best_pct(p_student, s.boss_exam_id, v_from, v_to);
    if v_pct is not null and v_pct >= round(coalesce(s.boss_pass_score, 8) * 10) then
      perform public.rank_grant_title(p_student, 'trum_cuoi', 'don', p_season, jsonb_build_object('exam_id', s.boss_exam_id, 'pct', v_pct));
    end if;
  end if;

  -- Huyền Thoại Đấu Trường: Chí Tôn ở >= 2 mùa đã đóng.
  select count(*) into v_n from public.rank_season_results where student_id = p_student and tier_code = 'thach_dau';
  if v_n >= 2 then
    perform public.rank_grant_title(p_student, 'huyen_thoai_dau_truong', 'don', p_season, jsonb_build_object('seasons', v_n));
  end if;
end; $$;


-- ============================================================
-- 9. Xử lý một lần nộp bài (gọi từ trigger và khi tính lại)
-- ============================================================
create or replace function public.rank_on_result(
  p_student uuid, p_kind text, p_source_id bigint, p_score numeric, p_at timestamptz, p_result_ref bigint
)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_season bigint := public.rank_season_for_at(p_student, p_at);
  v_src public.rank_sources%rowtype;
  v_title text;
begin
  if v_season is null then return; end if;

  select * into v_src from public.rank_sources
  where season_id = v_season and source_kind = p_kind and source_id = p_source_id and enabled;

  perform public.rank_ensure_member(v_season, p_student);

  if v_src.season_id is not null then
    if p_kind = 'exam' then
      select title into v_title from public.exams where id = p_source_id;
    else
      select li.title into v_title from public.lesson_items li where li.id = p_source_id;
    end if;
    perform public.rank_award(v_season, p_student, 'practice', p_kind || ':' || p_source_id,
      public.rank_score_to_rp(p_score, v_src.max_rp),
      'Bài luyện tập: ' || coalesce(v_title, '#' || p_source_id) || ' (' || replace(to_char(p_score, 'FM990.0'), '.', ',') || ' điểm)',
      p_result_ref);
    perform public.rank_eval_weekly_goal(v_season, p_student, p_at);
  end if;

  perform public.rank_eval_gates(v_season, p_student);
  perform public.rank_eval_achievements(v_season, p_student, p_at);
  perform public.rank_refresh_student(v_season, p_student);
end; $$;

create or replace function public.trg_rank_exam_result()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  begin
    perform public.rank_on_result(new.student_id, 'exam', new.exam_id, new.score, new.created_at, new.id);
  exception when others then
    raise warning 'rank: bỏ qua lỗi khi cộng RP cho exam_results %: %', new.id, sqlerrm;
  end;
  return new;
end; $$;
drop trigger if exists trg_rank_exam_result on public.exam_results;
create trigger trg_rank_exam_result after insert on public.exam_results
  for each row execute function public.trg_rank_exam_result();

create or replace function public.trg_rank_practice_session()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if new.item_id is null then return new; end if;
  begin
    perform public.rank_on_result(new.student_id, 'practice_item', new.item_id, new.score, new.created_at, new.id);
  exception when others then
    raise warning 'rank: bỏ qua lỗi khi cộng RP cho practice_sessions %: %', new.id, sqlerrm;
  end;
  return new;
end; $$;
drop trigger if exists trg_rank_practice_session on public.practice_sessions;
create trigger trg_rank_practice_session after insert on public.practice_sessions
  for each row execute function public.trg_rank_practice_session();

-- Kết quả từng câu được ghi SAU exam_results (client chèn riêng) -> xét danh hiệu ở đây,
-- một lần cho mỗi học sinh trong câu lệnh chèn.
create or replace function public.trg_rank_question_results()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  r record;
  v_season bigint;
begin
  for r in select distinct student_id from inserted loop
    begin
      v_season := public.rank_season_for_at(r.student_id, now());
      perform public.rank_eval_titles(r.student_id, v_season);
      if v_season is not null then
        perform public.rank_eval_gates(v_season, r.student_id);
        perform public.rank_eval_achievements(v_season, r.student_id, now());
        perform public.rank_refresh_student(v_season, r.student_id);
      end if;
    exception when others then
      raise warning 'rank: bỏ qua lỗi khi xét danh hiệu cho %: %', r.student_id, sqlerrm;
    end;
  end loop;
  return null;
end; $$;
drop trigger if exists trg_rank_question_results on public.exam_question_results;
create trigger trg_rank_question_results after insert on public.exam_question_results
  referencing new table as inserted
  for each statement execute function public.trg_rank_question_results();


-- ============================================================
-- 10. Sửa sai để nhận RP
-- ============================================================
-- Bài ngắn bốc từ ngân hàng cùng chủ đề tầng bài, LOẠI câu đã có trong đề gốc (so content_hash).
-- Chỉ áp dụng cho bài chạy qua ExamRunner (có exam_question_results). Tối đa 3 lượt/(bài, chủ đề).
create or replace function public.rank_fix_quiz_start(p_exam_result_id bigint, p_topic_id bigint)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_student uuid := auth.uid();
  v_res public.exam_results%rowtype;
  v_exam public.exams%rowtype;
  v_season bigint;
  v_min_pool int;
  v_count int;
  v_done int;
  v_ids bigint[];
  v_questions jsonb;
  v_attempt bigint;
  v_topic_name text;
begin
  select * into v_res from public.exam_results where id = p_exam_result_id and student_id = v_student;
  if not found then raise exception 'Không tìm thấy bài làm của em'; end if;

  v_season := public.rank_season_for_at(v_student, now());
  if v_season is null then raise exception 'Hiện chưa có mùa xếp hạng nào đang mở cho lớp em'; end if;
  if not exists (select 1 from public.rank_sources where season_id = v_season and source_kind = 'exam' and source_id = v_res.exam_id and enabled) then
    raise exception 'Bài này không được tính RP trong mùa hiện tại';
  end if;

  if not exists (
    select 1 from public.exam_question_results eqr
    join public.question_topics t on t.id = eqr.topic_id
    where eqr.exam_result_id = p_exam_result_id and not eqr.is_correct and coalesce(t.parent_id, t.id) = p_topic_id
  ) then
    raise exception 'Em không sai câu nào ở chủ đề này trong bài đó';
  end if;

  select count(*) into v_done from public.rank_fix_attempts
  where exam_result_id = p_exam_result_id and topic_id = p_topic_id and status = 'done';
  if v_done >= 3 then raise exception 'Em đã dùng hết 3 lượt sửa sai cho chủ đề này'; end if;

  select * into v_exam from public.exams where id = v_res.exam_id;
  v_min_pool := public.rank_cfg(v_season, 'fix_min_pool', 5)::int;
  v_count := public.rank_cfg(v_season, 'fix_quiz_count', 10)::int;

  -- Lượt đang mở (chưa nộp) -> trả lại chính nó, không bốc bộ mới.
  select id, question_ids into v_attempt, v_ids from public.rank_fix_attempts
  where exam_result_id = p_exam_result_id and topic_id = p_topic_id and status = 'open'
  order by created_at desc limit 1;

  if v_attempt is null then
    with seen as (
      select public.question_content_hash(q) as h from jsonb_array_elements(v_exam.questions) q
    ),
    pool as (
      select qb.id
      from public.question_bank qb
      join public.question_topics t on t.id = qb.topic_id
      where coalesce(t.parent_id, t.id) = p_topic_id
        and not qb.archived and qb.qtype <> 'essay'
        and qb.content_hash not in (select h from seen)
    )
    select array_agg(id) into v_ids from (select id from pool order by random() limit v_count) p;

    if coalesce(cardinality(v_ids), 0) < v_min_pool then
      raise exception 'Ngân hàng chưa đủ câu tương đương cho chủ đề này (cần ít nhất % câu khác đề gốc)', v_min_pool;
    end if;

    insert into public.rank_fix_attempts (student_id, season_id, exam_result_id, exam_id, topic_id, question_ids, total)
    values (v_student, v_season, p_exam_result_id, v_res.exam_id, p_topic_id, v_ids, cardinality(v_ids))
    returning id into v_attempt;
  end if;

  select jsonb_agg(qb.question order by array_position(v_ids, qb.id)) into v_questions
  from public.question_bank qb where qb.id = any (v_ids);
  select name into v_topic_name from public.question_topics where id = p_topic_id;

  return jsonb_build_object(
    'attempt_id', v_attempt,
    'topic_name', v_topic_name,
    'total', cardinality(v_ids),
    'attempts_left', 3 - v_done,
    'pass_pct', public.rank_cfg(v_season, 'fix_pass_pct', 80)::int,
    'questions', coalesce(v_questions, '[]'::jsonb)
  );
end; $$;
grant execute on function public.rank_fix_quiz_start(bigint, bigint) to authenticated;

create or replace function public.rank_fix_quiz_submit(p_attempt_id bigint, p_correct int)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_student uuid := auth.uid();
  a public.rank_fix_attempts%rowtype;
  v_pass int;
  v_wrong int;
  v_fixed int;
  v_max int;
  v_delta int;
  v_title text;
begin
  select * into a from public.rank_fix_attempts where id = p_attempt_id and student_id = v_student for update;
  if not found then raise exception 'Không tìm thấy lượt sửa sai'; end if;
  if a.status <> 'open' then raise exception 'Lượt này đã nộp rồi'; end if;
  if p_correct < 0 or p_correct > a.total then raise exception 'Số câu đúng không hợp lệ'; end if;

  v_pass := public.rank_cfg(a.season_id, 'fix_pass_pct', 80)::int;
  update public.rank_fix_attempts
    set correct = p_correct,
        pct = round(p_correct * 100.0 / a.total)::int,
        passed = round(p_correct * 100.0 / a.total)::int >= v_pass,
        status = 'done', submitted_at = now()
  where id = p_attempt_id
  returning * into a;

  -- số chủ đề (tầng bài) em sai trong bài gốc / số chủ đề đã sửa xong
  select count(distinct coalesce(t.parent_id, t.id)) into v_wrong
  from public.exam_question_results eqr join public.question_topics t on t.id = eqr.topic_id
  where eqr.exam_result_id = a.exam_result_id and not eqr.is_correct;
  select count(distinct topic_id) into v_fixed from public.rank_fix_attempts
  where exam_result_id = a.exam_result_id and passed;

  v_max := public.rank_cfg(a.season_id, 'fix_max_rp', 10)::int;
  select title into v_title from public.exams where id = a.exam_id;
  v_delta := public.rank_award(a.season_id, v_student, 'fix', 'exam_result:' || a.exam_result_id,
    case when v_wrong = 0 then 0 else round(v_max * v_fixed::numeric / v_wrong)::int end,
    'Sửa sai: ' || coalesce(v_title, '') || ' (' || v_fixed || '/' || v_wrong || ' chủ đề)', a.exam_result_id);
  perform public.rank_refresh_student(a.season_id, v_student);

  return jsonb_build_object('pct', a.pct, 'passed', a.passed, 'rp_delta', v_delta,
    'fixed_topics', v_fixed, 'wrong_topics', v_wrong);
end; $$;
grant execute on function public.rank_fix_quiz_submit(bigint, int) to authenticated;


-- ============================================================
-- 11. RPC học sinh / phụ huynh / giáo viên xem
-- ============================================================
create or replace function public.rank_can_view(p_student uuid)
returns boolean
language plpgsql security definer stable set search_path = public
as $$
begin
  return p_student = auth.uid() or public.teaches_student(p_student) or public.is_parent_of(p_student);
end; $$;

-- Trạng thái rank của một học sinh: bậc, RP, phân bậc, điều kiện tiếp theo, danh hiệu đeo, mục tiêu tuần.
create or replace function public.rank_status_of(p_student uuid)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_season bigint;
  s public.rank_seasons%rowtype;
  m public.rank_student_seasons%rowtype;
  info record;
  nxt public.rank_tiers%rowtype;
  v_next jsonb := null;
  v_gate jsonb := null;
  v_titles int;
  v_pct int;
  v_chal_title text;
  v_passed boolean;
  v_week date := public.rank_week_start(now());
  v_week_done int;
  v_display jsonb := null;
  p public.profiles%rowtype;
  v_rp int := 0;
  v_code text := 'tan_binh';
begin
  if not public.rank_can_view(p_student) then return null; end if;
  select * into p from public.profiles where id = p_student;
  if p.display_title_code is not null then
    select jsonb_build_object('code', t.code, 'name', t.name, 'level', p.display_title_level, 'group', t.group_code)
    into v_display from public.rank_titles t where t.code = p.display_title_code;
  end if;

  v_season := public.rank_season_for_at(p_student, now());
  if v_season is null then
    return jsonb_build_object('season', null, 'display_title', v_display,
      'titles_count', (select count(distinct title_code) from public.rank_title_awards where student_id = p_student));
  end if;
  select * into s from public.rank_seasons where id = v_season;
  select * into m from public.rank_student_seasons where season_id = v_season and student_id = p_student;
  if found then v_rp := m.rp; v_code := m.tier_code; end if;
  select * into info from public.rank_tier_info(v_season, v_code, v_rp);

  -- bậc kế tiếp + điều kiện còn thiếu
  select * into nxt from public.rank_tiers where season_id = v_season and sort = info.sort + 1;
  if found then
    v_passed := exists (select 1 from public.rank_gate_passes g where g.season_id = v_season and g.student_id = p_student and g.tier_code = nxt.code);
    if public.rank_tier_needs_gate(nxt) then
      v_titles := public.rank_titles_at_level(p_student, coalesce(nxt.required_title_level, 'thuc_tinh'));
      if nxt.challenge_exam_id is not null then
        select title into v_chal_title from public.exams where id = nxt.challenge_exam_id;
        v_pct := public.rank_best_pct(p_student, nxt.challenge_exam_id,
          (s.starts_on::timestamp) at time zone 'Asia/Ho_Chi_Minh',
          ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh');
      end if;
      v_gate := jsonb_build_object(
        'passed', v_passed,
        'required_title_count', nxt.required_title_count,
        'required_title_level', nxt.required_title_level,
        'titles_have', v_titles,
        'challenge_required', nxt.challenge_exam_id is not null or nxt.code in ('cao_thu', 'thach_dau'),
        'challenge_exam_id', nxt.challenge_exam_id,
        'challenge_title', v_chal_title,
        'challenge_pass_pct', round(coalesce(nxt.challenge_pass_score, 8) * 10),
        'challenge_best_pct', v_pct
      );
    end if;
    v_next := jsonb_build_object('code', nxt.code, 'name', nxt.name, 'min_rp', nxt.min_rp,
      'rp_needed', greatest(0, nxt.min_rp - v_rp), 'gate', v_gate);
  end if;

  select count(*) into v_week_done from (
    select er.exam_id from public.exam_results er
    join public.rank_sources rs on rs.season_id = v_season and rs.enabled and rs.source_kind = 'exam' and rs.source_id = er.exam_id
    where er.student_id = p_student and public.rank_week_start(er.created_at) = v_week
    group by er.exam_id having max(er.score) >= public.rank_cfg(v_season, 'weekly_goal_min_score', 7)
    union all
    select ps.item_id from public.practice_sessions ps
    join public.rank_sources rs on rs.season_id = v_season and rs.enabled and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id
    where ps.student_id = p_student and public.rank_week_start(ps.created_at) = v_week
    group by ps.item_id having max(ps.score) >= public.rank_cfg(v_season, 'weekly_goal_min_score', 7)
  ) x;

  return jsonb_build_object(
    'season', jsonb_build_object('id', s.id, 'name', s.name, 'starts_on', s.starts_on, 'ends_on', s.ends_on, 'status', s.status),
    'rp', v_rp,
    'tier', jsonb_build_object('code', info.code, 'name', info.name, 'sort', info.sort, 'tier_min', info.tier_min,
      'next_min', info.next_min, 'division', info.division, 'div_min', info.div_min, 'div_max', info.div_max),
    'next', v_next,
    'tier_reached_at', m.tier_reached_at,
    'joined_at', m.joined_at,
    'display_title', v_display,
    'titles_count', (select count(distinct title_code) from public.rank_title_awards where student_id = p_student),
    'weekly', jsonb_build_object('week_start', v_week, 'done', v_week_done,
      'target', public.rank_cfg(v_season, 'weekly_goal_count', 3)::int,
      'min_score', public.rank_cfg(v_season, 'weekly_goal_min_score', 7),
      'rp', public.rank_cfg(v_season, 'weekly_goal_rp', 30)::int,
      'achieved', exists (select 1 from public.rank_rp_awards a where a.season_id = v_season and a.student_id = p_student and a.source_kind = 'weekly_goal' and a.source_ref = v_week::text and a.awarded > 0))
  );
end; $$;
grant execute on function public.rank_status_of(uuid) to authenticated;

create or replace function public.rank_my_status()
returns jsonb language sql security definer stable set search_path = public
as $$ select public.rank_status_of(auth.uid()); $$;
grant execute on function public.rank_my_status() to authenticated;

-- Bộ sưu tập: mọi danh hiệu + mức đã có + tiến độ. "visible" = có chủ đề thuộc chương lớp em thấy.
create or replace function public.rank_titles_of(p_student uuid)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_out jsonb := '[]'::jsonb;
  t public.rank_titles%rowtype;
  st record;
  v_levels jsonb;
  v_have text;
  v_visible boolean;
  v_legend_best int;
  v_progress jsonb;
  v_req int;
  v_met int;
begin
  if not public.rank_can_view(p_student) then return null; end if;

  for t in select * from public.rank_titles where enabled order by
    case group_code when 'co_hoc' then 1 when 'dao_dong_song' then 2 when 'dien_tu' then 3 when 'nhiet_hoc' then 4 when 'hien_dai' then 5 when 'bo_suu_tap' then 6 else 7 end, sort
  loop
    select coalesce(jsonb_object_agg(a.level, a.awarded_at), '{}'::jsonb) into v_levels
    from public.rank_title_awards a where a.student_id = p_student and a.title_code = t.code;
    select a.level into v_have from public.rank_title_awards a
    where a.student_id = p_student and a.title_code = t.code
    order by public.rank_level_rank(a.level) desc limit 1;

    v_progress := null;
    if t.kind = 'specialist' then
      v_visible := exists (
        select 1 from public.rank_title_topics tt
        join public.question_topics qt on qt.id = tt.topic_id
        left join public.chapter_classes cc on cc.chapter_id = qt.chapter_id
        where tt.title_code = t.code
          and (cc.class_id is null or cc.class_id in (
            select class_id from public.user_classes where user_id = p_student and status = 'active'))
      );
      select * into st from public.rank_title_stats(p_student, t.code);
      v_legend_best := case when t.legend_challenge_exam_id is null then null else public.rank_best_pct(p_student, t.legend_challenge_exam_id) end;
      v_progress := jsonb_build_object('n', st.n, 'correct', st.correct, 'acc', st.acc, 'covered', st.covered,
        'total_topics', st.total_topics, 'min_questions', t.min_questions,
        'awaken_accuracy', t.awaken_accuracy, 'master_accuracy', t.master_accuracy,
        'legend_exam_id', t.legend_challenge_exam_id, 'legend_accuracy', t.legend_accuracy, 'legend_best', v_legend_best,
        'topics', (select coalesce(jsonb_agg(jsonb_build_object('id', qt.id, 'name', qt.name, 'lesson_id', qt.lesson_id) order by qt.grade, qt.sort_order), '[]'::jsonb)
                   from public.rank_title_topics tt join public.question_topics qt on qt.id = tt.topic_id where tt.title_code = t.code));
    elsif t.kind = 'collection' and (t.requires ? 'titles') then
      select count(*) filter (where public.rank_title_is_active(x)),
             count(*) filter (where public.rank_title_is_active(x) and exists (
               select 1 from public.rank_title_awards a where a.student_id = p_student and a.title_code = x
                 and public.rank_level_rank(a.level) >= public.rank_level_rank(coalesce(t.requires ->> 'level', 'lam_chu'))))
      into v_req, v_met
      from jsonb_array_elements_text(t.requires -> 'titles') x;
      v_visible := v_req > 0;
      v_progress := jsonb_build_object('required', v_req, 'met', v_met, 'level', coalesce(t.requires ->> 'level', 'lam_chu'),
        'titles', t.requires -> 'titles');
    else
      v_visible := true;
    end if;

    v_out := v_out || jsonb_build_object(
      'code', t.code, 'group', t.group_code, 'kind', t.kind, 'name', t.name, 'description', t.description,
      'visible', v_visible, 'active', case when t.kind = 'specialist' then public.rank_title_is_active(t.code) else v_visible end,
      'level', v_have, 'levels', v_levels, 'progress', v_progress
    );
  end loop;
  return v_out;
end; $$;
grant execute on function public.rank_titles_of(uuid) to authenticated;

create or replace function public.rank_my_titles()
returns jsonb language sql security definer stable set search_path = public
as $$ select public.rank_titles_of(auth.uid()); $$;
grant execute on function public.rank_my_titles() to authenticated;

create or replace function public.rank_ledger_of(p_student uuid, p_season bigint default null, p_limit int default 50)
returns table(id bigint, season_id bigint, source_kind text, source_ref text, amount int, reason text, ref_result_id bigint, actor_name text, created_at timestamptz)
language plpgsql security definer stable set search_path = public
as $$
begin
  if not public.rank_can_view(p_student) then return; end if;
  return query
  select l.id, l.season_id, l.source_kind, l.source_ref, l.amount, l.reason, l.ref_result_id, p.full_name, l.created_at
  from public.rank_rp_ledger l
  left join public.profiles p on p.id = l.actor
  where l.student_id = p_student and (p_season is null or l.season_id = p_season)
  order by l.created_at desc
  limit greatest(1, least(p_limit, 500));
end; $$;
grant execute on function public.rank_ledger_of(uuid, bigint, int) to authenticated;

-- Thành tích theo mùa: mùa đã đóng (lưu trữ) + mùa đang tham gia.
create or replace function public.rank_seasons_of(p_student uuid)
returns table(season_id bigint, name text, starts_on date, ends_on date, status text, rp int, tier_code text, division int, titles_count int)
language plpgsql security definer stable set search_path = public
as $$
begin
  if not public.rank_can_view(p_student) then return; end if;
  return query
  select s.id, s.name, s.starts_on, s.ends_on, s.status,
         coalesce(r.rp, m.rp, 0), coalesce(r.tier_code, m.tier_code, 'tan_binh'), coalesce(r.division, m.division),
         coalesce(r.titles_count, 0)
  from public.rank_seasons s
  left join public.rank_season_results r on r.season_id = s.id and r.student_id = p_student
  left join public.rank_student_seasons m on m.season_id = s.id and m.student_id = p_student
  where r.student_id is not null or m.student_id is not null
  order by s.starts_on desc;
end; $$;
grant execute on function public.rank_seasons_of(uuid) to authenticated;

create or replace function public.rank_set_display_title(p_code text, p_level text)
returns void
language plpgsql security definer set search_path = public
as $$
begin
  if p_code is null then
    update public.profiles set display_title_code = null, display_title_level = null where id = auth.uid();
    return;
  end if;
  if not exists (select 1 from public.rank_title_awards a where a.student_id = auth.uid() and a.title_code = p_code and a.level = p_level) then
    raise exception 'Em chưa sở hữu danh hiệu này';
  end if;
  update public.profiles set display_title_code = p_code, display_title_level = p_level where id = auth.uid();
end; $$;
grant execute on function public.rank_set_display_title(text, text) to authenticated;

-- Trang lớp: các nhóm bậc (tên xếp ABC, KHÔNG RP, KHÔNG thứ tự) + ghi nhận tuần này.
create or replace function public.rank_class_groups(p_class_id bigint)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_season bigint;
  s public.rank_seasons%rowtype;
  v_week date := public.rank_week_start(now());
  v_from timestamptz := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_tiers jsonb;
  v_weekly jsonb;
  v_unranked jsonb;
begin
  if not (public.manages_class(p_class_id) or exists (
    select 1 from public.user_classes where user_id = auth.uid() and class_id = p_class_id and status = 'active'
  )) then
    return null;
  end if;

  select rs.id into v_season from public.rank_seasons rs
  where rs.status = 'active' and public.rank_vn_date(now()) between rs.starts_on and rs.ends_on
    and (cardinality(rs.class_ids) = 0 or p_class_id = any (rs.class_ids))
  order by rs.starts_on desc limit 1;
  if v_season is null then return jsonb_build_object('season', null); end if;
  select * into s from public.rank_seasons where id = v_season;

  with members as (
    select uc.user_id, p.full_name, p.display_title_code, p.display_title_level, m.tier_code, m.tier_sort, m.division
    from public.user_classes uc
    join public.profiles p on p.id = uc.user_id
    left join public.rank_student_seasons m on m.season_id = v_season and m.student_id = uc.user_id
    where uc.class_id = p_class_id and uc.status = 'active' and p.role = 'student'
  )
  select
    (select jsonb_agg(jsonb_build_object('code', t.code, 'name', t.name, 'sort', t.sort,
        'members', (select coalesce(jsonb_agg(jsonb_build_object('name', mm.full_name, 'division', mm.division,
                        'title', (select jsonb_build_object('name', rt.name, 'level', mm.display_title_level) from public.rank_titles rt where rt.code = mm.display_title_code))
                        order by mm.full_name), '[]'::jsonb)
                    from members mm where mm.tier_code = t.code)) order by t.sort desc)
     from public.rank_tiers t where t.season_id = v_season),
    (select coalesce(jsonb_agg(jsonb_build_object('name', mm.full_name) order by mm.full_name), '[]'::jsonb) from members mm where mm.tier_code is null)
  into v_tiers, v_unranked;

  with members as (
    select uc.user_id, p.full_name from public.user_classes uc join public.profiles p on p.id = uc.user_id
    where uc.class_id = p_class_id and uc.status = 'active' and p.role = 'student'
  ),
  ev as (
    select mm.full_name, 'weekly_goal' as kind, 'đạt mục tiêu tuần' as label, l.created_at as happened_at
    from public.rank_rp_ledger l join members mm on mm.user_id = l.student_id
    where l.season_id = v_season and l.source_kind = 'weekly_goal' and l.created_at >= v_from
    union all
    select mm.full_name, 'tier_up', 'lên bậc ' || t.name, m.tier_reached_at
    from public.rank_student_seasons m join members mm on mm.user_id = m.student_id
    join public.rank_tiers t on t.season_id = m.season_id and t.code = m.tier_code
    where m.season_id = v_season and m.tier_reached_at >= v_from and m.tier_sort > 1
    union all
    select mm.full_name, 'title', 'nhận danh hiệu ' || rt.name || case a.level when 'thuc_tinh' then ' · Thức Tỉnh' when 'lam_chu' then ' · Làm Chủ' when 'huyen_thoai' then ' · Huyền Thoại' else '' end, a.awarded_at
    from public.rank_title_awards a join members mm on mm.user_id = a.student_id
    join public.rank_titles rt on rt.code = a.title_code
    where a.awarded_at >= v_from
  )
  select coalesce(jsonb_agg(jsonb_build_object('name', e.full_name, 'kind', e.kind, 'label', e.label, 'at', e.happened_at) order by e.happened_at desc), '[]'::jsonb)
  into v_weekly from (select * from ev order by happened_at desc limit 40) e;

  return jsonb_build_object(
    'season', jsonb_build_object('id', s.id, 'name', s.name, 'starts_on', s.starts_on, 'ends_on', s.ends_on),
    'tiers', coalesce(v_tiers, '[]'::jsonb),
    'unranked', v_unranked,
    'weekly', v_weekly,
    'week_start', v_week
  );
end; $$;
grant execute on function public.rank_class_groups(bigint) to authenticated;


-- ============================================================
-- 12. RPC giáo viên
-- ============================================================
create or replace function public.rank_create_season(
  p_name text, p_starts date, p_ends date, p_class_ids bigint[] default '{}', p_activate boolean default false
)
returns bigint
language plpgsql security definer set search_path = public
as $$
declare v_id bigint;
begin
  if not public.rank_is_staff() then raise exception 'Không có quyền tạo mùa'; end if;
  insert into public.rank_seasons (name, starts_on, ends_on, class_ids, status, created_by)
  values (p_name, p_starts, p_ends, coalesce(p_class_ids, '{}'), case when p_activate then 'active' else 'draft' end, auth.uid())
  returning id into v_id;
  perform public.rank_seed_tiers(v_id);
  return v_id;
end; $$;
grant execute on function public.rank_create_season(text, date, date, bigint[], boolean) to authenticated;

-- Điều chỉnh tay (có lý do, có người làm) — đi qua ledger như mọi thay đổi khác.
create or replace function public.rank_adjust_rp(p_season bigint, p_student uuid, p_delta int, p_reason text)
returns void
language plpgsql security definer set search_path = public
as $$
begin
  if not public.rank_is_staff() or not public.teaches_student(p_student) then
    raise exception 'Không có quyền điều chỉnh RP của học sinh này';
  end if;
  if coalesce(btrim(p_reason), '') = '' then raise exception 'Cần ghi lý do điều chỉnh'; end if;
  if p_delta = 0 then return; end if;
  perform public.rank_ensure_member(p_season, p_student);
  insert into public.rank_rp_awards (season_id, student_id, source_kind, source_ref, awarded)
  values (p_season, p_student, 'manual', 'manual', p_delta)
  on conflict (season_id, student_id, source_kind, source_ref) do update
    set awarded = public.rank_rp_awards.awarded + excluded.awarded, updated_at = now();
  insert into public.rank_rp_ledger (season_id, student_id, source_kind, source_ref, amount, reason, actor)
  values (p_season, p_student, 'manual', 'manual', p_delta, btrim(p_reason), auth.uid());
  perform public.rank_eval_gates(p_season, p_student);
  perform public.rank_refresh_student(p_season, p_student);
end; $$;
grant execute on function public.rank_adjust_rp(bigint, uuid, int, text) to authenticated;

-- Đóng mùa: lưu bậc/RP cuối, không xoá gì. Mùa mới bắt đầu từ 0 RP, danh hiệu giữ nguyên.
create or replace function public.rank_close_season(p_season bigint)
returns int
language plpgsql security definer set search_path = public
as $$
declare v_n int; r record;
begin
  if not public.rank_is_staff() then raise exception 'Không có quyền đóng mùa'; end if;
  insert into public.rank_season_results (season_id, student_id, rp, tier_code, division, titles_count)
  select m.season_id, m.student_id, m.rp, m.tier_code, m.division,
         (select count(distinct a.title_code) from public.rank_title_awards a where a.student_id = m.student_id)
  from public.rank_student_seasons m where m.season_id = p_season
  on conflict (season_id, student_id) do update
    set rp = excluded.rp, tier_code = excluded.tier_code, division = excluded.division,
        titles_count = excluded.titles_count, closed_at = now();
  get diagnostics v_n = row_count;
  update public.rank_seasons set status = 'closed', closed_at = now() where id = p_season;
  for r in select student_id from public.rank_season_results where season_id = p_season and tier_code = 'thach_dau' loop
    perform public.rank_eval_achievements(p_season, r.student_id, now());
  end loop;
  return v_n;
end; $$;
grant execute on function public.rank_close_season(bigint) to authenticated;

-- Tính lại cho một học sinh: quét mọi bài trong khung mùa theo đúng luật live (delta -> idempotent).
-- Dùng cho học sinh vào lớp muộn hoặc mùa mở sau khi đã có bài. KHÔNG tự chạy.
create or replace function public.rank_recompute_student(p_season bigint, p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  s public.rank_seasons%rowtype;
  v_from timestamptz; v_to timestamptz;
  r record;
begin
  if not public.rank_is_staff() then raise exception 'Không có quyền'; end if;
  select * into s from public.rank_seasons where id = p_season;
  if s.status <> 'active' then raise exception 'Chỉ tính lại được mùa đang mở'; end if;
  v_from := (s.starts_on::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to := ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh';

  perform public.rank_ensure_member(p_season, p_student);
  for r in
    select 'exam' as k, er.exam_id as sid, er.score, er.created_at, er.id
    from public.exam_results er
    join public.rank_sources rs on rs.season_id = p_season and rs.enabled and rs.source_kind = 'exam' and rs.source_id = er.exam_id
    where er.student_id = p_student and er.created_at >= v_from and er.created_at < v_to
    union all
    select 'practice_item', ps.item_id, ps.score, ps.created_at, ps.id
    from public.practice_sessions ps
    join public.rank_sources rs on rs.season_id = p_season and rs.enabled and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id
    where ps.student_id = p_student and ps.created_at >= v_from and ps.created_at < v_to
    order by 4
  loop
    perform public.rank_on_result(p_student, r.k, r.sid, r.score, r.created_at, r.id);
  end loop;
  perform public.rank_eval_titles(p_student, p_season);
  perform public.rank_eval_gates(p_season, p_student);
  perform public.rank_eval_achievements(p_season, p_student, now());
  perform public.rank_refresh_student(p_season, p_student);
end; $$;
grant execute on function public.rank_recompute_student(bigint, uuid) to authenticated;

create or replace function public.rank_recompute_season(p_season bigint)
returns int
language plpgsql security definer set search_path = public
as $$
declare r record; v_n int := 0; s public.rank_seasons%rowtype;
begin
  if not public.rank_is_staff() then raise exception 'Không có quyền'; end if;
  select * into s from public.rank_seasons where id = p_season;
  for r in
    select distinct uc.user_id from public.user_classes uc
    join public.profiles p on p.id = uc.user_id and p.role = 'student'
    where uc.status = 'active' and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids))
  loop
    perform public.rank_recompute_student(p_season, r.user_id);
    v_n := v_n + 1;
  end loop;
  return v_n;
end; $$;
grant execute on function public.rank_recompute_season(bigint) to authenticated;

-- Bảng học sinh cho trang giáo viên.
create or replace function public.rank_season_overview(p_season bigint)
returns table(student_id uuid, full_name text, class_names text, rp int, tier_code text, tier_sort int, division int,
              titles_count int, last_award_at timestamptz, pending_gate text)
language plpgsql security definer stable set search_path = public
as $$
declare s public.rank_seasons%rowtype;
begin
  if not public.rank_is_staff() then return; end if;
  select * into s from public.rank_seasons where id = p_season;
  return query
  with members as (
    select distinct uc.user_id from public.user_classes uc
    join public.profiles p on p.id = uc.user_id and p.role = 'student'
    where uc.status = 'active' and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids))
  )
  select mm.user_id, p.full_name,
         (select string_agg(c.name, ', ' order by c.name) from public.user_classes uc join public.classes c on c.id = uc.class_id where uc.user_id = mm.user_id and uc.status = 'active'),
         coalesce(m.rp, 0), coalesce(m.tier_code, 'tan_binh'), coalesce(m.tier_sort, 1), m.division,
         (select count(distinct a.title_code)::int from public.rank_title_awards a where a.student_id = mm.user_id),
         (select max(l.created_at) from public.rank_rp_ledger l where l.season_id = p_season and l.student_id = mm.user_id),
         (select t.name from public.rank_tiers t
            where t.season_id = p_season and t.min_rp <= coalesce(m.rp, 0) and t.sort > coalesce(m.tier_sort, 1)
            order by t.sort limit 1)
  from members mm
  join public.profiles p on p.id = mm.user_id
  left join public.rank_student_seasons m on m.season_id = p_season and m.student_id = mm.user_id
  order by coalesce(m.tier_sort, 1) desc, coalesce(m.rp, 0) desc, p.full_name;
end; $$;
grant execute on function public.rank_season_overview(bigint) to authenticated;


-- ============================================================
-- 13. Seed danh hiệu (chạy lại: cập nhật tên/mô tả, giữ ngưỡng đã chỉnh)
-- ============================================================
insert into public.rank_titles (code, group_code, kind, name, description, sort) values
  ('ke_san_quy_dao',          'co_hoc', 'specialist', 'Kẻ Săn Quỹ Đạo',          'Chuyển động và đồ thị', 10),
  ('bac_thay_gia_toc',        'co_hoc', 'specialist', 'Bậc Thầy Gia Tốc',        'Chuyển động biến đổi', 20),
  ('chien_than_newton',       'co_hoc', 'specialist', 'Chiến Thần Newton',       'Lực và các định luật Newton', 30),
  ('ke_pha_the_can_bang',     'co_hoc', 'specialist', 'Kẻ Phá Thế Cân Bằng',     'Moment lực, cân bằng vật rắn', 40),
  ('chua_te_dong_luong',      'co_hoc', 'specialist', 'Chúa Tể Động Lượng',      'Xung lượng, va chạm, bảo toàn động lượng', 50),
  ('nguoi_giu_nang_luong',    'co_hoc', 'specialist', 'Người Giữ Năng Lượng',    'Công, công suất, bảo toàn cơ năng', 60),
  ('vu_cong_quy_dao',         'co_hoc', 'specialist', 'Vũ Công Quỹ Đạo',         'Chuyển động tròn', 70),
  ('bac_thay_nhip_dao_dong',  'dao_dong_song', 'specialist', 'Bậc Thầy Nhịp Dao Động',  'Dao động điều hoà', 10),
  ('ke_dieu_khien_cong_huong','dao_dong_song', 'specialist', 'Kẻ Điều Khiển Cộng Hưởng','Dao động cưỡng bức, cộng hưởng', 20),
  ('chua_te_song',            'dao_dong_song', 'specialist', 'Chúa Tể Của Những Loại Sóng', 'Sự truyền sóng', 30),
  ('phap_su_giao_thoa',       'dao_dong_song', 'specialist', 'Pháp Sư Giao Thoa',       'Giao thoa sóng', 40),
  ('nguoi_giu_nut_song',      'dao_dong_song', 'specialist', 'Người Giữ Nút Sóng',      'Sóng dừng', 50),
  ('tho_san_tan_so',          'dao_dong_song', 'specialist', 'Thợ Săn Tần Số',          'Sóng âm', 60),
  ('phap_su_dien_truong',     'dien_tu', 'specialist', 'Pháp Sư Điện Trường',     'Lực điện, cường độ điện trường', 10),
  ('ke_tich_tru_loi_dinh',    'dien_tu', 'specialist', 'Kẻ Tích Trữ Lôi Đình',    'Tụ điện, năng lượng điện trường', 20),
  ('bac_thay_mach_dien',      'dien_tu', 'specialist', 'Bậc Thầy Mạch Điện',      'Dòng điện, điện trở, mạch điện', 30),
  ('chua_te_tu_truong',       'dien_tu', 'specialist', 'Chúa Tể Từ Trường',       'Từ trường và lực từ', 40),
  ('ke_danh_thuc_dong_dien',  'dien_tu', 'specialist', 'Kẻ Đánh Thức Dòng Điện',  'Cảm ứng điện từ', 50),
  ('vu_cong_lech_pha',        'dien_tu', 'specialist', 'Vũ Công Lệch Pha',        'Dòng điện xoay chiều', 60),
  ('nguoi_truyen_nang_luong', 'dien_tu', 'specialist', 'Người Truyền Năng Lượng', 'Máy biến áp, truyền tải điện', 70),
  ('hoa_phap_su',             'nhiet_hoc', 'specialist', 'Hỏa Pháp Sư',             'Nhiệt lượng, nhiệt dung riêng', 10),
  ('bac_thay_chuyen_the',     'nhiet_hoc', 'specialist', 'Bậc Thầy Chuyển Thể',     'Nóng chảy, hoá hơi', 20),
  ('ke_thuan_hoa_phan_tu',    'nhiet_hoc', 'specialist', 'Kẻ Thuần Hóa Phân Tử',    'Mô hình động học phân tử', 30),
  ('chua_te_ap_suat',         'nhiet_hoc', 'specialist', 'Chúa Tể Áp Suất',         'Các định luật chất khí', 40),
  ('nguoi_giu_can_bang_nhiet','nhiet_hoc', 'specialist', 'Người Giữ Cân Bằng Nhiệt','Trao đổi nhiệt', 50),
  ('bac_thay_noi_nang',       'nhiet_hoc', 'specialist', 'Bậc Thầy Nội Năng',       'Nguyên lí I nhiệt động lực học', 60),
  ('ke_be_cong_anh_sang',     'hien_dai', 'specialist', 'Kẻ Bẻ Cong Ánh Sáng',     'Khúc xạ ánh sáng', 10),
  ('phap_su_thau_kinh',       'hien_dai', 'specialist', 'Pháp Sư Thấu Kính',       'Tạo ảnh qua thấu kính', 20),
  ('tho_san_photon',          'hien_dai', 'specialist', 'Thợ Săn Photon',          'Lượng tử ánh sáng, quang điện', 30),
  ('nguoi_giai_ma_nguyen_tu', 'hien_dai', 'specialist', 'Người Giải Mã Nguyên Tử', 'Cấu trúc, mức năng lượng nguyên tử', 40),
  ('ke_giai_ma_phong_xa',     'hien_dai', 'specialist', 'Kẻ Giải Mã Phóng Xạ',     'Phóng xạ, chu kì bán rã', 50),
  ('nguoi_giu_loi_hat_nhan',  'hien_dai', 'specialist', 'Người Giữ Lõi Hạt Nhân',  'Liên kết, năng lượng hạt nhân', 60),
  ('but_pha_than_toc',        'thanh_tich', 'achievement', 'Bứt Phá Thần Tốc',        'RP tuần này từ 60 và gấp đôi trung bình 3 tuần trước', 10),
  ('chien_binh_bat_diet',     'thanh_tich', 'achievement', 'Chiến Binh Bất Diệt',     'Đạt mục tiêu tuần 4 tuần liên tiếp', 20),
  ('bach_phat_bach_trung',    'thanh_tich', 'achievement', 'Bách Phát Bách Trúng',    'Đúng 100% ở ít nhất 3 đề thử thách trong mùa', 30),
  ('lat_keo_ngoan_muc',       'thanh_tich', 'achievement', 'Lật Kèo Ngoạn Mục',       'Một chủ đề từng dưới 50% nay đạt từ 80%, hoặc tự thoát phụ đạo bằng bài kiểm tra', 40),
  ('pha_dao_chuyen_de',       'thanh_tich', 'achievement', 'Phá Đảo Chuyên Đề',       'Mọi chủ đề của một chương đạt từ 85%, cả lý thuyết lẫn bài tập', 50),
  ('trum_cuoi',               'thanh_tich', 'achievement', 'Trùm Cuối',               'Vượt đề khó nhất mùa', 60),
  ('huyen_thoai_dau_truong',  'thanh_tich', 'achievement', 'Huyền Thoại Đấu Trường',  'Đạt Chí Tôn ở hai mùa trở lên', 70)
on conflict (code) do update set group_code = excluded.group_code, kind = excluded.kind, name = excluded.name,
  description = excluded.description, sort = excluded.sort;

insert into public.rank_titles (code, group_code, kind, name, description, sort, requires) values
  ('hau_due_newton',           'bo_suu_tap', 'collection', 'Hậu Duệ Newton',           'Hoàn thành bộ Cơ học', 10,
    '{"level":"lam_chu","titles":["ke_san_quy_dao","bac_thay_gia_toc","chien_than_newton","ke_pha_the_can_bang","chua_te_dong_luong","nguoi_giu_nang_luong","vu_cong_quy_dao"]}'),
  ('nhac_truong_vu_tru',       'bo_suu_tap', 'collection', 'Nhạc Trưởng Vũ Trụ',       'Hoàn thành bộ Dao động và Sóng', 20,
    '{"level":"lam_chu","titles":["bac_thay_nhip_dao_dong","ke_dieu_khien_cong_huong","chua_te_song","phap_su_giao_thoa","nguoi_giu_nut_song","tho_san_tan_so"]}'),
  ('loi_than_maxwell',         'bo_suu_tap', 'collection', 'Lôi Thần Maxwell',         'Hoàn thành bộ Điện và Từ', 30,
    '{"level":"lam_chu","titles":["phap_su_dien_truong","ke_tich_tru_loi_dinh","bac_thay_mach_dien","chua_te_tu_truong","ke_danh_thuc_dong_dien","vu_cong_lech_pha","nguoi_truyen_nang_luong"]}'),
  ('nguoi_giu_lua_vinh_hang',  'bo_suu_tap', 'collection', 'Người Giữ Lửa Vĩnh Hằng',  'Hoàn thành bộ Nhiệt học', 40,
    '{"level":"lam_chu","titles":["hoa_phap_su","bac_thay_chuyen_the","ke_thuan_hoa_phan_tu","chua_te_ap_suat","nguoi_giu_can_bang_nhiet","bac_thay_noi_nang"]}'),
  ('lu_khach_luong_tu',        'bo_suu_tap', 'collection', 'Lữ Khách Lượng Tử',        'Hoàn thành bộ Vật lý hiện đại', 50,
    '{"level":"lam_chu","titles":["ke_be_cong_anh_sang","phap_su_thau_kinh","tho_san_photon","nguoi_giai_ma_nguyen_tu","ke_giai_ma_phong_xa","nguoi_giu_loi_hat_nhan"]}'),
  ('ke_giai_ma_vu_tru',        'bo_suu_tap', 'collection', 'Kẻ Giải Mã Vũ Trụ',        'Hoàn thành mọi bộ chuyên môn được giao', 60,
    '{"collections":true}')
on conflict (code) do update set group_code = excluded.group_code, kind = excluded.kind, name = excluded.name,
  description = excluded.description, sort = excluded.sort, requires = excluded.requires;

-- Ánh xạ danh hiệu → chủ đề tầng bài (khớp theo (grade, name) của question_topics — xem
-- supabase-migration-question-topics-seed.sql). Chủ đề không có trong DB thì bỏ qua; danh hiệu
-- không ánh xạ được chủ đề nào (Photon, Nguyên tử, Máy biến áp, Cân bằng nhiệt) sẽ KHÔNG active
-- cho tới khi giáo viên gắn chủ đề ở /quan-tri/xep-hang.
create temporary table tmp_rank_title_topics (title_code text, grade text, topic_name text) on commit drop;
insert into tmp_rank_title_topics values
  ('ke_san_quy_dao', '10', 'Độ dịch chuyển, quãng đường, tốc độ, vận tốc'),
  ('ke_san_quy_dao', '10', 'Đồ thị độ dịch chuyển – thời gian'),
  ('bac_thay_gia_toc', '10', 'Chuyển động thẳng biến đổi đều. Gia tốc'),
  ('bac_thay_gia_toc', '10', 'Sự rơi tự do'),
  ('bac_thay_gia_toc', '10', 'Chuyển động ném'),
  ('chien_than_newton', '10', 'Tổng hợp và phân tích lực. Cân bằng lực'),
  ('chien_than_newton', '10', 'Ba định luật Newton'),
  ('chien_than_newton', '10', 'Trọng lực và lực căng'),
  ('chien_than_newton', '10', 'Lực ma sát, lực cản và lực nâng'),
  ('ke_pha_the_can_bang', '10', 'Moment lực. Cân bằng của vật rắn'),
  ('chua_te_dong_luong', '10', 'Động lượng'),
  ('chua_te_dong_luong', '10', 'Bảo toàn động lượng và va chạm'),
  ('nguoi_giu_nang_luong', '10', 'Năng lượng. Công cơ học'),
  ('nguoi_giu_nang_luong', '10', 'Công suất'),
  ('nguoi_giu_nang_luong', '10', 'Động năng, thế năng'),
  ('nguoi_giu_nang_luong', '10', 'Cơ năng và định luật bảo toàn cơ năng'),
  ('nguoi_giu_nang_luong', '10', 'Hiệu suất'),
  ('nguoi_giu_nang_luong', '9', 'Động năng. Thế năng'),
  ('nguoi_giu_nang_luong', '9', 'Cơ năng'),
  ('nguoi_giu_nang_luong', '9', 'Công và công suất'),
  ('vu_cong_quy_dao', '10', 'Động học của chuyển động tròn đều'),
  ('vu_cong_quy_dao', '10', 'Lực hướng tâm và gia tốc hướng tâm'),
  ('bac_thay_nhip_dao_dong', '11', 'Dao động điều hoà'),
  ('bac_thay_nhip_dao_dong', '11', 'Vận tốc, gia tốc trong dao động điều hoà'),
  ('bac_thay_nhip_dao_dong', '11', 'Năng lượng trong dao động điều hoà'),
  ('ke_dieu_khien_cong_huong', '11', 'Dao động tắt dần. Dao động cưỡng bức. Cộng hưởng'),
  ('chua_te_song', '11', 'Mô tả sóng'),
  ('chua_te_song', '11', 'Sóng ngang, sóng dọc. Truyền năng lượng của sóng cơ'),
  ('chua_te_song', '11', 'Sóng điện từ'),
  ('phap_su_giao_thoa', '11', 'Giao thoa sóng'),
  ('nguoi_giu_nut_song', '11', 'Sóng dừng'),
  ('tho_san_tan_so', '11', 'Sóng âm và đo tốc độ truyền âm'),
  ('phap_su_dien_truong', '11', 'Lực tương tác giữa hai điện tích'),
  ('phap_su_dien_truong', '11', 'Khái niệm điện trường. Cường độ điện trường'),
  ('phap_su_dien_truong', '11', 'Điện trường đều'),
  ('ke_tich_tru_loi_dinh', '11', 'Thế năng điện. Điện thế'),
  ('ke_tich_tru_loi_dinh', '11', 'Tụ điện và điện dung'),
  ('bac_thay_mach_dien', '11', 'Cường độ dòng điện'),
  ('bac_thay_mach_dien', '11', 'Điện trở. Định luật Ohm'),
  ('bac_thay_mach_dien', '11', 'Nguồn điện. Suất điện động'),
  ('bac_thay_mach_dien', '11', 'Năng lượng điện. Công suất điện'),
  ('bac_thay_mach_dien', '9', 'Điện trở. Định luật Ohm'),
  ('bac_thay_mach_dien', '9', 'Đoạn mạch nối tiếp, song song'),
  ('bac_thay_mach_dien', '9', 'Năng lượng và công suất điện'),
  ('chua_te_tu_truong', '12', 'Khái niệm từ trường'),
  ('chua_te_tu_truong', '12', 'Lực từ. Cảm ứng từ'),
  ('ke_danh_thuc_dong_dien', '12', 'Từ thông. Hiện tượng cảm ứng điện từ'),
  ('ke_danh_thuc_dong_dien', '9', 'Cảm ứng điện từ. Dòng điện xoay chiều'),
  ('vu_cong_lech_pha', '12', 'Đại cương về dòng điện xoay chiều'),
  ('vu_cong_lech_pha', '9', 'Tác dụng của dòng điện xoay chiều'),
  ('hoa_phap_su', '12', 'Nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng'),
  ('hoa_phap_su', '12', 'Thang nhiệt độ. Nhiệt kế'),
  ('bac_thay_chuyen_the', '12', 'Sự chuyển thể'),
  ('ke_thuan_hoa_phan_tu', '12', 'Thuyết động học phân tử chất khí'),
  ('chua_te_ap_suat', '12', 'Định luật Boyle. Định luật Charles'),
  ('chua_te_ap_suat', '12', 'Phương trình trạng thái khí lí tưởng'),
  ('chua_te_ap_suat', '12', 'Áp suất và động năng phân tử khí'),
  ('bac_thay_noi_nang', '12', 'Nội năng. Định luật 1 của nhiệt động lực học'),
  ('ke_be_cong_anh_sang', '9', 'Khúc xạ ánh sáng'),
  ('ke_be_cong_anh_sang', '9', 'Phản xạ toàn phần'),
  ('ke_be_cong_anh_sang', '9', 'Lăng kính'),
  ('phap_su_thau_kinh', '9', 'Thấu kính'),
  ('ke_giai_ma_phong_xa', '12', 'Hiện tượng phóng xạ. Chu kì bán rã'),
  ('ke_giai_ma_phong_xa', '12', 'An toàn phóng xạ'),
  ('nguoi_giu_loi_hat_nhan', '12', 'Cấu trúc hạt nhân'),
  ('nguoi_giu_loi_hat_nhan', '12', 'Độ hụt khối. Năng lượng liên kết hạt nhân'),
  ('nguoi_giu_loi_hat_nhan', '12', 'Phản ứng phân hạch, phản ứng nhiệt hạch');

insert into public.rank_title_topics (title_code, topic_id)
select t.title_code, qt.id
from tmp_rank_title_topics t
join public.question_topics qt on qt.grade = t.grade and qt.name = t.topic_name and qt.parent_id is null
on conflict do nothing;

do $$
declare r record;
begin
  for r in
    select t.title_code, t.grade, t.topic_name from tmp_rank_title_topics t
    where not exists (select 1 from public.question_topics qt where qt.grade = t.grade and qt.name = t.topic_name)
  loop
    raise notice 'rank: chưa có chủ đề "% (lớp %)" cho danh hiệu % — gắn tay ở trang quản trị', r.topic_name, r.grade, r.title_code;
  end loop;
end $$;
