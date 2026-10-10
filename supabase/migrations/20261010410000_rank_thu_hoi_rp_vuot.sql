-- ============================================================================
-- data(rank): thu hồi RP thưởng tuần/tiến bộ đã cộng vượt luật mới (10/10/2026)
--
-- Chạy SAU 20261010400000_rank_chan_thuong_qua_cao.sql (luật mới: sàn 6 điểm, trần 40 RP, tiến bộ cần đúng >= 60%).
-- Với mỗi dòng rank_rp_awards còn dương:
--   * weekly_goal  : đánh giá lại tuần đó với ngưỡng điểm >= 6; không còn đạt mục tiêu → 0; còn đạt → giảm xuống tối đa 30
--                    (mùa 4 từng cộng 90). Dòng <= 30 mà vẫn đạt thì giữ nguyên.
--   * progress_week: tỉ lệ đúng của tuần đó < progress_min_acc_pct (60) → 0.
-- KHÔNG đụng practice / fix / daily_streak / class_goal / theory / manual.
-- Mỗi thay đổi: lưu dòng cũ vào rank_rp_awards_backup_20261010 (kèm new_awarded, ghi chú), ghi một dòng ÂM vào
-- rank_rp_ledger (em xem được lý do trong lịch sử RP), rồi rank_refresh_student để RP tổng + bậc tính lại.
-- Bậc có thể tụt; danh hiệu / thành tích đã cấp và cửa thăng hạng đã qua KHÔNG bị thu hồi.
-- Chạy lại lần hai không đổi gì thêm (dòng đã điều chỉnh không còn vượt luật).
-- Xem trước (không ghi): bash scripts/xem-truoc-thu-hoi-rp.sh   — giờ nào cũng được.
-- Rollback: ở cuối file.
-- ============================================================================

create table if not exists public.rank_rp_awards_backup_20261010 (
  season_id bigint, student_id uuid, source_kind text, source_ref text,
  awarded int, best_value numeric(6, 2), updated_at timestamptz,
  new_awarded int, note text, backed_up_at timestamptz default now()
);
alter table public.rank_rp_awards_backup_20261010 enable row level security;
revoke all on public.rank_rp_awards_backup_20261010 from anon, authenticated;

do $$
declare
  r record; c record; w record;
  v_new int; v_note text;
  v_week date; v_from timestamptz; v_to timestamptz; v_min numeric; v_cnt int;
  v_min_acc numeric;
  v_cap int;
  v_n int := 0; v_sum int := 0;
begin
  for r in
    select * from public.rank_rp_awards
    where source_kind in ('weekly_goal', 'progress_week') and awarded > 0
    order by season_id, student_id, source_ref
  loop
    v_new := r.awarded; v_note := null;
    begin
      v_week := r.source_ref::date;
    exception when others then continue;
    end;

    if r.source_kind = 'weekly_goal' then
      v_cap := 30; -- mức thưởng mục tiêu tuần chuẩn (mùa 4 từng đặt 90)
      select g.target, g.min_score into w from public.rank_weekly_goal_of(r.season_id, r.student_id, v_week) g;
      v_min := greatest(w.min_score, public.rank_cfg(r.season_id, 'weekly_goal_abs_floor', 6));
      v_from := (v_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
      v_to := ((v_week + 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
      select count(*) into v_cnt from (
        select er.exam_id as id
        from public.exam_results er
        join public.rank_sources rs on rs.season_id = r.season_id and rs.enabled and rs.source_kind = 'exam' and rs.source_id = er.exam_id
        where er.student_id = r.student_id and er.created_at >= v_from and er.created_at < v_to
        group by er.exam_id having max(er.score) >= v_min
        union all
        select ps.item_id
        from public.practice_sessions ps
        join public.rank_sources rs on rs.season_id = r.season_id and rs.enabled and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id
        where ps.student_id = r.student_id and ps.created_at >= v_from and ps.created_at < v_to
        group by ps.item_id having max(ps.score) >= v_min
      ) x;
      if v_cnt < w.target then
        v_new := 0; v_note := 'Mục tiêu tuần: chưa có đủ ' || w.target || ' bài đạt từ ' || v_min || ' điểm';
      elsif r.awarded > v_cap then
        v_new := v_cap; v_note := 'Mục tiêu tuần: đưa về mức thưởng ' || v_cap || ' RP';
      end if;
    else
      v_min_acc := public.rank_cfg(r.season_id, 'progress_min_acc_pct', 60);
      select * into c from public.rank_progress_calc(r.student_id, v_week);
      if c.acc_now is null or c.acc_now < v_min_acc then
        v_new := 0; v_note := 'Tiến bộ tuần: tỉ lệ đúng tuần đó ' || coalesce(replace(c.acc_now::text, '.', ','), '?') || '% chưa tới ' || v_min_acc || '%';
      end if;
    end if;

    if v_new < r.awarded then
      insert into public.rank_rp_awards_backup_20261010 (season_id, student_id, source_kind, source_ref, awarded, best_value, updated_at, new_awarded, note)
      values (r.season_id, r.student_id, r.source_kind, r.source_ref, r.awarded, r.best_value, r.updated_at, v_new, v_note);
      update public.rank_rp_awards set awarded = v_new, updated_at = now()
        where season_id = r.season_id and student_id = r.student_id and source_kind = r.source_kind and source_ref = r.source_ref;
      insert into public.rank_rp_ledger (season_id, student_id, source_kind, source_ref, amount, reason)
      values (r.season_id, r.student_id, r.source_kind, r.source_ref, v_new - r.awarded,
              'Điều chỉnh thưởng theo luật mới (10/10/2026): ' || v_note);
      perform public.rank_refresh_student(r.season_id, r.student_id);
      v_n := v_n + 1; v_sum := v_sum + (r.awarded - v_new);
    end if;
  end loop;
  raise notice 'Điều chỉnh % dòng, thu hồi tổng % RP', v_n, v_sum;
end $$;

-- Tóm tắt: theo nguồn và kiểu điều chỉnh
select source_kind, case when new_awarded = 0 then 'về 0' else 'giảm bớt' end as kieu,
       count(*) as so_dong, count(distinct student_id) as so_em, sum(awarded - new_awarded) as rp_thu_hoi
from public.rank_rp_awards_backup_20261010 group by 1, 2 order by 1, 2;

-- Rollback (khôi phục từ bảng sao lưu; ghi dòng DƯƠNG vào ledger):
--   update public.rank_rp_awards a set awarded = b.awarded, updated_at = now()
--     from public.rank_rp_awards_backup_20261010 b
--     where a.season_id = b.season_id and a.student_id = b.student_id and a.source_kind = b.source_kind and a.source_ref = b.source_ref;
--   insert into public.rank_rp_ledger (season_id, student_id, source_kind, source_ref, amount, reason)
--     select season_id, student_id, source_kind, source_ref, awarded - new_awarded, 'Hoàn tác điều chỉnh 10/10/2026' from public.rank_rp_awards_backup_20261010;
--   select public.rank_refresh_student(season_id, student_id) from (select distinct season_id, student_id from public.rank_rp_awards_backup_20261010) x;
