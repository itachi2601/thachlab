-- ============================================================================
-- Báo live "bao nhiêu bạn đang học, đang học chủ đề nào" cho học sinh (thầy chốt 11/10/2026): toàn trường, ẩn danh.
-- RPC live_study_summary(): gộp student_learning_presence (last_seen trong 2 phút) → tổng số + top 3 bài có >= 3 em.
-- Ngưỡng ẩn 3: dưới 3 em thì tổng trả few=true (hiện "vài bạn"), không trả bài nào — không lộ được danh tính.
-- Không đụng bảng nào; học sinh vẫn không đọc được bảng presence thô, chỉ gọi RPC này (security definer).
-- Cách chạy: bash scripts/run-migrations.sh — chạy lúc nào cũng được (chỉ thêm hàm mới).
-- Rollback: perf/rollback/20261011210000_live_study_summary.down.sql
-- ============================================================================

create or replace function public.live_study_summary()
returns jsonb
language sql stable security definer set search_path = public
as $$
  with active as (
    select p.lesson_id
    from public.student_learning_presence p
    where p.last_seen_at >= now() - interval '2 minutes'
  ), tot as (
    select count(*)::int as n from active
  ), top as (
    select a.lesson_id, l.title, count(*)::int as n
    from active a
    join public.lessons l on l.id = a.lesson_id
    where l.published
    group by a.lesson_id, l.title
    having count(*) >= 3
    order by count(*) desc, l.title
    limit 3
  )
  select jsonb_build_object(
    'total', case when tot.n >= 3 then tot.n else 0 end,
    'few', tot.n between 1 and 2,
    'topics', coalesce((select jsonb_agg(jsonb_build_object('lesson_id', t.lesson_id, 'title', t.title, 'n', t.n) order by t.n desc, t.title) from top t), '[]'::jsonb)
  )
  from tot;
$$;

revoke all on function public.live_study_summary() from public, anon;
grant execute on function public.live_study_summary() to authenticated;

-- ROLLBACK: drop function if exists public.live_study_summary();
