-- ============================================================================
-- GĐ 1b #6 — Mục tiêu chung của lớp (30/9/2026)
--
-- "Cả lớp đạt N huy hiệu trong tuần" (Thứ Hai–Chủ Nhật, giờ VN). Huy hiệu = mỗi lượt nhận danh hiệu/mức
-- danh hiệu mới (rank_title_awards) của bất kỳ học sinh nào trong lớp trong tuần. Đạt -> MỖI học sinh
-- đang học trong lớp được cộng class_goal_rp RP (một lần/lớp/tuần). Cấu trúc hợp tác: em giỏi có lý do
-- giúp em yếu — mọi huy hiệu của bất kỳ ai đều tính vào mục tiêu chung.
-- Cấu hình mùa (rank_seasons.config, mọi khoá tuỳ chọn):
--   class_goal_badges (0 = tự tính) · class_goal_min (3) · class_goal_ratio (0.25, N = max(min, ceil(sĩ số x ratio)))
--   class_goal_rp (10; 0 = tắt phần thưởng, vẫn hiện tiến độ)
--
-- Thay đổi: 1) rank_rp_awards_source_kind_check thêm 'class_goal' (giữ nguyên các giá trị đang có)
--   2) hàm mới rank_class_goal_of (chỉ đọc) và rank_eval_class_goal (cộng RP)
--   3) trigger sau khi thêm dòng vào rank_title_awards gọi rank_eval_class_goal (mọi lỗi chỉ cảnh báo, không chặn cấp danh hiệu)
--   4) rank_class_board định nghĩa lại = bản 20260930110000 + khoá 'class_goal' (KHÔNG thêm truy vấn ở trang chủ HS)
-- Phải chạy SAU 20260930110000_rank_board_by_tier.sql. Chạy giờ nào cũng được.
-- Rollback: perf/rollback/20260930140000_rank_class_goal.down.sql
-- ============================================================================

alter table public.rank_rp_awards drop constraint if exists rank_rp_awards_source_kind_check;
alter table public.rank_rp_awards add constraint rank_rp_awards_source_kind_check
  check (source_kind in ('practice', 'fix', 'weekly_goal', 'daily_streak', 'manual', 'homework_check', 'progress_week', 'class_goal'));

create index if not exists rank_title_awards_time_idx on public.rank_title_awards (awarded_at);

-- Tiến độ mục tiêu chung của lớp trong tuần p_week (chỉ đọc).
create or replace function public.rank_class_goal_of(p_season bigint, p_class bigint, p_week date)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_from timestamptz := (p_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to timestamptz := ((p_week + 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_members int;
  v_done int;
  v_mine int := 0;
  v_fixed int := public.rank_cfg(p_season, 'class_goal_badges', 0)::int;
  v_min int := public.rank_cfg(p_season, 'class_goal_min', 3)::int;
  v_ratio numeric := public.rank_cfg(p_season, 'class_goal_ratio', 0.25);
  v_rp int := public.rank_cfg(p_season, 'class_goal_rp', 10)::int;
  v_target int;
begin
  select count(*) into v_members
  from public.user_classes uc join public.profiles p on p.id = uc.user_id
  where uc.class_id = p_class and uc.status = 'active' and p.role = 'student';

  select count(*), count(*) filter (where a.student_id = auth.uid()) into v_done, v_mine
  from public.rank_title_awards a
  where a.awarded_at >= v_from and a.awarded_at < v_to
    and a.student_id in (
      select uc.user_id from public.user_classes uc join public.profiles p on p.id = uc.user_id
      where uc.class_id = p_class and uc.status = 'active' and p.role = 'student');

  v_target := case when v_fixed > 0 then v_fixed else greatest(v_min, ceil(v_members * v_ratio)::int) end;
  return jsonb_build_object(
    'week_start', p_week, 'target', v_target, 'done', v_done, 'members', v_members,
    'my_contrib', v_mine, 'rp', v_rp,
    'reached', v_done >= v_target
      or exists (select 1 from public.rank_rp_awards r
                 where r.season_id = p_season and r.source_kind = 'class_goal' and r.source_ref = p_class || ':' || p_week and r.awarded > 0));
end; $$;
revoke all on function public.rank_class_goal_of(bigint, bigint, date) from public, anon;
grant execute on function public.rank_class_goal_of(bigint, bigint, date) to authenticated;

-- Cộng RP chung khi lớp đạt mục tiêu; gọi từ trigger khi có huy hiệu mới.
create or replace function public.rank_eval_class_goal(p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_season bigint := public.rank_season_for_at(p_student, now());
  v_week date := public.rank_week_start(now());
  s public.rank_seasons%rowtype;
  v_class bigint;
  g jsonb;
  v_rp int;
  m record;
begin
  if v_season is null then return; end if;
  select * into s from public.rank_seasons where id = v_season;
  if s.status <> 'active' or public.rank_vn_date(now()) not between s.starts_on and s.ends_on then return; end if;
  v_rp := public.rank_cfg(v_season, 'class_goal_rp', 10)::int;
  if v_rp <= 0 then return; end if;

  for v_class in
    select uc.class_id from public.user_classes uc
    where uc.user_id = p_student and uc.status = 'active'
      and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids))
  loop
    g := public.rank_class_goal_of(v_season, v_class, v_week);
    if (g ->> 'done')::int >= (g ->> 'target')::int then
      for m in
        select uc.user_id from public.user_classes uc join public.profiles p on p.id = uc.user_id
        where uc.class_id = v_class and uc.status = 'active' and p.role = 'student'
      loop
        if not public.rank_is_student(m.user_id) then continue; end if;
        if public.rank_award(v_season, m.user_id, 'class_goal', v_class || ':' || v_week, v_rp,
             'Cả lớp đạt mục tiêu huy hiệu tuần ' || to_char(v_week, 'DD/MM') || ' (' || (g ->> 'done') || '/' || (g ->> 'target') || ')', null) > 0 then
          perform public.rank_refresh_student(v_season, m.user_id);
        end if;
      end loop;
    end if;
  end loop;
end; $$;
revoke all on function public.rank_eval_class_goal(uuid) from public, anon, authenticated;

create or replace function public.trg_rank_class_goal()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  begin
    perform public.rank_eval_class_goal(new.student_id);
  exception when others then
    raise warning 'rank: bỏ qua lỗi khi xét mục tiêu chung lớp cho %: %', new.student_id, sqlerrm;
  end;
  return null;
end; $$;
drop trigger if exists trg_rank_class_goal on public.rank_title_awards;
create trigger trg_rank_class_goal after insert on public.rank_title_awards
  for each row execute function public.trg_rank_class_goal();

-- rank_class_board = bản 20260930110000 + class_goal
create or replace function public.rank_class_board(p_class_id bigint)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_me uuid := auth.uid();
  v_season bigint;
  s public.rank_seasons%rowtype;
  v_week date := public.rank_week_start(now());
  v_from timestamptz := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_prev_from timestamptz := ((v_week - 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_top jsonb;
  v_me_json jsonb;
  v_improved jsonb;
  v_weekly jsonb;
  v_goal jsonb;
begin
  if not (public.manages_class(p_class_id) or exists (
    select 1 from public.user_classes where user_id = v_me and class_id = p_class_id and status = 'active'
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
    select uc.user_id, p.full_name, p.avatar_url, p.display_title_code, p.display_title_level, m.tier_code, m.division
    from public.user_classes uc
    join public.profiles p on p.id = uc.user_id
    left join public.rank_student_seasons m on m.season_id = v_season and m.student_id = uc.user_id
    where uc.class_id = p_class_id and uc.status = 'active' and p.role = 'student'
  ),
  wk as (
    select mm.*,
      coalesce((select sum(l.amount) from public.rank_rp_ledger l
                where l.season_id = v_season and l.student_id = mm.user_id and l.created_at >= v_from), 0)::int as rp_week,
      coalesce((select sum(l.amount) from public.rank_rp_ledger l
                where l.season_id = v_season and l.student_id = mm.user_id
                  and l.created_at >= v_prev_from and l.created_at < v_from), 0)::int as rp_prev
    from members mm
  ),
  ranked as (
    select w.*, rank() over (order by w.rp_week desc) as pos,
           coalesce(w.tier_code, '') as tcode
    from wk w
  )
  select
    (select coalesce(jsonb_agg(jsonb_build_object(
        'pos', t.pos, 'name', t.full_name, 'avatar', t.avatar_url, 'rp_week', t.rp_week,
        'tier_code', t.tier_code, 'division', t.division, 'is_me', t.user_id = v_me,
        'paragon', t.tier_code = 'thach_dau' and public.rank_is_paragon(t.user_id),
        'title', (select jsonb_build_object('code', rt.code, 'name', rt.name, 'level', t.display_title_level)
                  from public.rank_titles rt where rt.code = t.display_title_code)
      ) order by t.pos, t.full_name), '[]'::jsonb)
     from (select * from ranked where rp_week > 0 order by pos, full_name limit 3) t),
    (select jsonb_build_object(
        'rp_week', r.rp_week,
        'tier_code', r.tier_code, 'division', r.division,
        'tier_size', (select count(*) from ranked x where x.tcode = r.tcode),
        'in_top', r.pos <= 3 and r.rp_week > 0,
        'tied', (select count(*) from ranked x where x.tcode = r.tcode and x.rp_week = r.rp_week) - 1,
        'above', (select jsonb_build_object('name', x.full_name, 'avatar', x.avatar_url, 'rp_week', x.rp_week)
                  from ranked x where x.tcode = r.tcode and x.rp_week > r.rp_week
                  order by x.rp_week asc, x.full_name limit 1),
        'below', (select jsonb_build_object('name', x.full_name, 'avatar', x.avatar_url, 'rp_week', x.rp_week)
                  from ranked x where x.tcode = r.tcode and x.rp_week < r.rp_week
                  order by x.rp_week desc, x.full_name limit 1)
      ) from ranked r where r.user_id = v_me),
    (select jsonb_build_object('name', t.full_name, 'avatar', t.avatar_url, 'rp_week', t.rp_week, 'delta', t.rp_week - t.rp_prev)
     from ranked t where t.rp_week > 0 and t.rp_week - t.rp_prev > 0 and t.pos > 3
     order by (t.rp_week - t.rp_prev) desc, t.full_name limit 1)
  into v_top, v_me_json, v_improved;

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
  into v_weekly from (select * from ev order by happened_at desc limit 20) e;

  v_goal := public.rank_class_goal_of(v_season, p_class_id, v_week);

  return jsonb_build_object(
    'season', jsonb_build_object('id', s.id, 'name', s.name, 'starts_on', s.starts_on, 'ends_on', s.ends_on),
    'week_start', v_week,
    'top_week', v_top,
    'me', v_me_json,
    'improved', v_improved,
    'weekly', v_weekly,
    'class_goal', v_goal
  );
end; $$;
grant execute on function public.rank_class_board(bigint) to authenticated;
