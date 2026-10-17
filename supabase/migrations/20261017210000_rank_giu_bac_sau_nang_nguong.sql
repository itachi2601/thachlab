-- ============================================================================
-- fix(rank): giữ bậc cho 13 em bị tụt do nâng ngưỡng ×1,07 (migration 20261017200000), 17/10/2026
--
-- Thầy chốt 17/10: các em tụt bậc chỉ vì ngưỡng nâng thì giữ nguyên bậc. Cách làm: bảng rank_tier_floor ghi "sàn bậc"
-- cho từng em trong mùa; rank_refresh_student lấy bậc cao hơn giữa bậc tính theo RP và sàn (phân bậc hiển thị là III khi
-- RP dưới mức bậc). Sàn của mỗi em = bậc em đạt theo ngưỡng CŨ (rank_tiers_backup_20261017) và cổng đã vượt; áp cho các em
-- đã nhận chuông 'rank_tier_adjust'. Các em khác không đổi. Gửi chuông cải chính cho 13 em.
-- Hết mùa thì bảng không còn tác dụng (khoá theo season_id).
-- Cách chạy: bash scripts/run-migrations.sh — ngoài giờ học sinh làm bài (chạy sau 20261017200000).
-- Rollback: perf/rollback/20261017210000_rank_giu_bac_sau_nang_nguong.down.sql
-- ============================================================================

create table if not exists public.rank_tier_floor (
  season_id bigint not null references public.rank_seasons (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  tier_code text not null,
  tier_sort int not null,
  reason text not null default '',
  created_at timestamptz not null default now(),
  primary key (season_id, student_id)
);
alter table public.rank_tier_floor enable row level security;
revoke all on public.rank_tier_floor from anon, authenticated;

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
  v_floor public.rank_tier_floor%rowtype;
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

  -- Sàn bậc (giữ bậc khi đổi ngưỡng): không thấp hơn bậc đã ghi.
  select * into v_floor from public.rank_tier_floor where season_id = p_season and student_id = p_student;
  if found and v_floor.tier_sort > v_sort then
    v_code := v_floor.tier_code;
    v_sort := v_floor.tier_sort;
  end if;

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

do $$
declare
  r record; t public.rank_tiers%rowtype;
  v_code text; v_sort int; v_n int := 0;
begin
  for r in
    select m.season_id, m.student_id, m.rp from public.rank_student_seasons m
    where m.season_id in (4, 5)
      and exists (select 1 from public.notifications n where n.user_id = m.student_id and n.kind = 'rank_tier_adjust')
  loop
    v_code := 'tan_binh'; v_sort := 1;
    for t in
      select rt.* from public.rank_tiers rt
      join public.rank_tiers_backup_20261017 b on b.season_id = rt.season_id and b.code = rt.code
      where rt.season_id = r.season_id and b.min_rp <= r.rp order by rt.sort
    loop
      if public.rank_tier_needs_gate(t) and not exists (
        select 1 from public.rank_gate_passes g
        where g.season_id = r.season_id and g.student_id = r.student_id and g.tier_code = t.code
      ) then exit; end if;
      v_code := t.code; v_sort := t.sort;
    end loop;
    insert into public.rank_tier_floor (season_id, student_id, tier_code, tier_sort, reason)
    values (r.season_id, r.student_id, v_code, v_sort, 'Giữ bậc sau khi nâng ngưỡng ×1,07 (17/10/2026)')
    on conflict (season_id, student_id) do nothing;
    perform public.rank_refresh_student(r.season_id, r.student_id);
    perform public.notify_user(r.student_id, 'rank_tier_keep', 'Em được giữ nguyên bậc',
      'Mức RP lên bậc có tăng, nhưng thầy giữ nguyên bậc cũ cho em đến hết mùa. Tiếp tục làm bài để lên bậc cao hơn.',
      '/lop-hoc/xep-hang');
    v_n := v_n + 1;
  end loop;
  raise notice 'Giữ bậc cho % em', v_n;
end $$;
