-- Hồ sơ thành tựu theo mùa — bản chụp đầy đủ khi đóng mùa (15/10/2026, spec docs/THANH-TUU-MUA-VA-AVATAR.md).
--
-- rank_close_season đã ghi rank_season_results (rp, bậc, số danh hiệu) và mọi bảng rank đều khoá theo season_id,
-- nên mở mùa 2 KHÔNG mất mùa 1. File này chỉ bổ sung những gì bản chụp cũ thiếu để dựng "dấu mùa", "dòng hành trình"
-- và các kiểu ghi nhận ngoài RP (bền bỉ, tiến bộ, làm chủ YCCĐ):
--   - tên + thứ tự bậc lúc đóng (bảng bậc có thể đổi ở mùa sau), lớp lúc đóng (năm sau em đổi lớp)
--   - danh hiệu nhận TRONG mùa (titles_count cũ đếm mọi mùa)
--   - số tuần đạt mục tiêu, RP theo từng tuần (để tính "tiến bộ nhất" sau này mà không cần ledger)
--   - YCCĐ đang "Nắm vững" tại thời điểm đóng (luật docs/mastery-rules.md: 10 lượt gần nhất, ≥4 lượt, ≥80%)
-- Thêm hàm rank_snapshot_season (idempotent). Mùa đang mở KHÔNG được chụp thường (rank_seasons_of sẽ hiện số cũ thay
-- RP live, achievement Huyền Thoại đếm nhầm mùa chưa xong) — chỉ rank_close_season gọi với p_force. Xem thử trước khi
-- đóng: begin; select rank_snapshot_season(4, true); select ... from rank_season_results ...; rollback;
-- Chỉ thêm cột + thay hàm; chạy lúc nào cũng được.

alter table public.rank_season_results
  add column if not exists tier_sort int,
  add column if not exists tier_name text,
  add column if not exists class_names text,
  add column if not exists season_titles jsonb not null default '[]'::jsonb,
  add column if not exists weeks_goal_met int not null default 0,
  add column if not exists weekly_rp jsonb not null default '{}'::jsonb,
  add column if not exists mastered_topic_ids bigint[] not null default '{}',
  add column if not exists mastered_count int not null default 0,
  add column if not exists snapshot_at timestamptz;

comment on column public.rank_season_results.season_titles is
  'Danh hiệu nhận trong mùa: [{code, level, awarded_at}]';
comment on column public.rank_season_results.weekly_rp is
  'RP theo tuần (khoá = ngày Thứ Hai, rank_week_start): {"2026-09-21": 45, ...}';
comment on column public.rank_season_results.mastered_topic_ids is
  'YCCĐ (question_topics.parent_id not null) đang Nắm vững lúc chụp — luật docs/mastery-rules.md';

-- Chụp kết quả mùa cho mọi thành viên. Mốc tính YCCĐ = now, hoặc hết ngày ends_on nếu đã qua.
create or replace function public.rank_snapshot_season(p_season bigint, p_force boolean default false)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  s public.rank_seasons%rowtype;
  v_at timestamptz;
  v_n int;
begin
  if not public.rank_is_staff() then raise exception 'Không có quyền chụp kết quả mùa'; end if;
  select * into s from public.rank_seasons where id = p_season;
  if not found then raise exception 'Không có mùa %', p_season; end if;
  if s.status = 'active' and not p_force then
    raise exception 'Mùa % đang mở — chỉ chụp khi đóng mùa (hoặc p_force trong transaction rồi rollback)', p_season;
  end if;
  v_at := least(now(), ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh');

  insert into public.rank_season_results as r (
    season_id, student_id, rp, tier_code, division, titles_count,
    tier_sort, tier_name, class_names, season_titles, weeks_goal_met, weekly_rp,
    mastered_topic_ids, mastered_count, snapshot_at)
  select m.season_id, m.student_id, m.rp, m.tier_code, m.division,
         (select count(distinct a.title_code)::int from public.rank_title_awards a where a.student_id = m.student_id),
         m.tier_sort,
         (select t.name from public.rank_tiers t where t.season_id = m.season_id and t.code = m.tier_code),
         (select string_agg(c.name, ', ' order by c.name)
            from public.user_classes uc join public.classes c on c.id = uc.class_id
           where uc.user_id = m.student_id and uc.status = 'active'
             and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids))),
         coalesce((select jsonb_agg(jsonb_build_object('code', a.title_code, 'level', a.level, 'awarded_at', a.awarded_at)
                                    order by a.awarded_at)
                     from public.rank_title_awards a
                    where a.student_id = m.student_id and a.season_id = m.season_id), '[]'::jsonb),
         (select count(*)::int from public.rank_rp_awards w
           where w.season_id = m.season_id and w.student_id = m.student_id
             and w.source_kind = 'weekly_goal' and w.awarded > 0),
         coalesce((select jsonb_object_agg(wk, rp)
                     from (select public.rank_week_start(l.created_at)::text as wk, sum(l.amount)::int as rp
                             from public.rank_rp_ledger l
                            where l.season_id = m.season_id and l.student_id = m.student_id
                            group by 1) x), '{}'::jsonb),
         mt.ids, coalesce(cardinality(mt.ids), 0),
         now()
  from public.rank_student_seasons m
  left join lateral (
    select coalesce(array_agg(topic_id order by topic_id), '{}') as ids
    from (
      select a.topic_id
      from (
        select u.topic_id, u.earned, u.max,
               row_number() over (partition by u.topic_id order by u.created_at desc) as rn
        from (
          select topic_id, earned, max, created_at from public.exam_question_results
           where student_id = m.student_id and topic_id is not null and created_at < v_at
          union all
          select topic_id, earned, max, created_at from public.practice_question_results
           where student_id = m.student_id and topic_id is not null and created_at < v_at
        ) u
      ) a
      join public.question_topics qt on qt.id = a.topic_id and qt.parent_id is not null
      where a.rn <= 10
      group by a.topic_id
      having count(*) >= 4 and sum(a.max) > 0 and sum(a.earned) / sum(a.max) >= 0.8
    ) ok
  ) mt on true
  where m.season_id = p_season
  on conflict (season_id, student_id) do update
    set rp = excluded.rp, tier_code = excluded.tier_code, division = excluded.division,
        titles_count = excluded.titles_count, tier_sort = excluded.tier_sort, tier_name = excluded.tier_name,
        class_names = excluded.class_names, season_titles = excluded.season_titles,
        weeks_goal_met = excluded.weeks_goal_met, weekly_rp = excluded.weekly_rp,
        mastered_topic_ids = excluded.mastered_topic_ids, mastered_count = excluded.mastered_count,
        snapshot_at = excluded.snapshot_at;
  get diagnostics v_n = row_count;
  return v_n;
end; $$;
grant execute on function public.rank_snapshot_season(bigint, boolean) to authenticated;

-- Đóng mùa = chụp đầy đủ + đổi trạng thái + xét thành tích như cũ.
create or replace function public.rank_close_season(p_season bigint)
returns int
language plpgsql security definer set search_path = public
as $$
declare v_n int; r record;
begin
  if not public.rank_is_staff() then raise exception 'Không có quyền đóng mùa'; end if;
  v_n := public.rank_snapshot_season(p_season, true);
  update public.rank_season_results set closed_at = now() where season_id = p_season;
  update public.rank_seasons set status = 'closed', closed_at = now() where id = p_season;
  for r in select student_id from public.rank_season_results where season_id = p_season and tier_code = 'thach_dau' loop
    perform public.rank_eval_achievements(p_season, r.student_id, now());
  end loop;
  return v_n;
end; $$;
grant execute on function public.rank_close_season(bigint) to authenticated;

-- ============================================================
-- ROLLBACK (chạy tay nếu cần): trả rank_close_season về bản gốc, bỏ hàm + cột mới.
-- ============================================================
-- create or replace function public.rank_close_season(p_season bigint)
-- returns int language plpgsql security definer set search_path = public as $$
-- declare v_n int; r record;
-- begin
--   if not public.rank_is_staff() then raise exception 'Không có quyền đóng mùa'; end if;
--   insert into public.rank_season_results (season_id, student_id, rp, tier_code, division, titles_count)
--   select m.season_id, m.student_id, m.rp, m.tier_code, m.division,
--          (select count(distinct a.title_code) from public.rank_title_awards a where a.student_id = m.student_id)
--   from public.rank_student_seasons m where m.season_id = p_season
--   on conflict (season_id, student_id) do update
--     set rp = excluded.rp, tier_code = excluded.tier_code, division = excluded.division,
--         titles_count = excluded.titles_count, closed_at = now();
--   get diagnostics v_n = row_count;
--   update public.rank_seasons set status = 'closed', closed_at = now() where id = p_season;
--   for r in select student_id from public.rank_season_results where season_id = p_season and tier_code = 'thach_dau' loop
--     perform public.rank_eval_achievements(p_season, r.student_id, now());
--   end loop;
--   return v_n;
-- end; $$;
-- drop function if exists public.rank_snapshot_season(bigint, boolean);
-- alter table public.rank_season_results
--   drop column if exists tier_sort, drop column if exists tier_name, drop column if exists class_names,
--   drop column if exists season_titles, drop column if exists weeks_goal_met, drop column if exists weekly_rp,
--   drop column if exists mastered_topic_ids, drop column if exists mastered_count, drop column if exists snapshot_at;
