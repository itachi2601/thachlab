-- ============================================================================
-- feat(rank): "Tiến bộ so với chính em" — giai đoạn 1b, việc 1 (29/9/2026)
--
-- Luật (tham chiếu ban đầu, chỉnh qua mùa sau bằng rank_seasons.config, không cần sửa code):
--   Tuần Thứ Hai → Chủ Nhật (giờ VN). Tỉ lệ đúng của tuần = tổng điểm đạt / tổng điểm tối đa của
--   mọi câu (đề + luyện tập, trừ tự luận) làm trong tuần. Mốc so sánh = tỉ lệ đúng của 2 tuần liền
--   trước (gộp).
--   Được thưởng khi: tuần này >= progress_min_questions câu VÀ mốc >= progress_min_questions câu VÀ
--     tăng >= min(progress_min_gain_pct, 100 - mốc) điểm phần trăm.
--     (Em đã ở mốc cao gần 100% chỉ cần giữ/nhích lên; mốc 100% cần giữ 100%.)
--   Thưởng RP (một lần/tuần, chỉ tăng chứ không giảm, cùng cơ chế rank_award):
--     progress_rp (15) khi đạt ngưỡng, +progress_step_rp (5) mỗi progress_step_pct (5) điểm % tăng
--     thêm, tối đa progress_rp_max (25).
--   Em chưa đủ dữ liệu (mới vào, nghỉ lâu) không bị trừ gì, chỉ chưa có thưởng tuần đó.
--
-- Cấu hình mùa (rank_seasons.config, mọi khoá đều tuỳ chọn, thiếu thì dùng mặc định trong ngoặc):
--   progress_min_gain_pct (5) · progress_rp (15) · progress_rp_max (25) · progress_step_pct (5)
--   progress_step_rp (5) · progress_min_questions (15)
--
-- Hai thay đổi hệ thống hiện có:
--   1. rank_rp_awards_source_kind_check thêm 'progress_week'.
--   2. trg_rank_question_results (chạy 1 lần/lượt nộp đề, SAU khi kết quả từng câu đã ghi) gọi thêm
--      rank_eval_progress_week. Luyện tập: thêm trigger mới trên practice_question_results.
--   Mọi lỗi trong phần tiến bộ chỉ ghi cảnh báo, không bao giờ làm hỏng việc nộp bài.
--
-- KHÔNG đụng: rank_on_result, mục tiêu tuần, chuỗi ngày, danh hiệu, huy hiệu (thành tích
-- "Tiến bộ tuần" để đợt sau). Không tự xoá/ghi dữ liệu học sinh lúc chạy migration.
--
-- Cách chạy: bash scripts/run-migrations.sh    (chạy giờ nào cũng được, chỉ tạo hàm/trigger/chỉ mục)
-- Lưu ý: tiến bộ chỉ được tính khi có lượt làm bài MỚI (trigger), không cộng bù tuần đã qua và
-- rank_recompute_season không tính phần này.
-- Rollback:  supabase db query --linked -f perf/rollback/20260929110000_rank_progress_week.down.sql
-- ============================================================================

-- ---------- 1. Cho phép nguồn RP 'progress_week' (giữ nguyên các giá trị đang có) ----------
alter table public.rank_rp_awards drop constraint if exists rank_rp_awards_source_kind_check;
alter table public.rank_rp_awards add constraint rank_rp_awards_source_kind_check
  check (source_kind in ('practice', 'fix', 'weekly_goal', 'daily_streak', 'manual', 'homework_check', 'progress_week'));

-- ---------- 2. Chỉ mục cho phép tính theo tuần (không tạo nếu đã có cột đầu tương đương) ----------
create index if not exists exam_question_results_student_time_idx
  on public.exam_question_results (student_id, created_at);
create index if not exists practice_question_results_student_time_idx
  on public.practice_question_results (student_id, created_at);

-- ---------- 3. Tính tỉ lệ đúng tuần này và mốc 2 tuần trước ----------
create or replace function public.rank_progress_calc(p_student uuid, p_week date)
returns table(q_now int, acc_now numeric, q_base int, acc_base numeric, gain numeric)
language plpgsql stable security definer set search_path = public
as $$
declare
  v_from timestamptz := (p_week::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_to timestamptz := ((p_week + 7)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_base_from timestamptz := ((p_week - 14)::timestamp) at time zone 'Asia/Ho_Chi_Minh';
  v_qn int; v_en numeric; v_mn numeric;
  v_qb int; v_eb numeric; v_mb numeric;
begin
  select coalesce(sum(n), 0), coalesce(sum(e), 0), coalesce(sum(m), 0) into v_qn, v_en, v_mn from (
    select count(*) as n, sum(coalesce(earned, 0)) as e, sum(max) as m
    from public.exam_question_results
    where student_id = p_student and created_at >= v_from and created_at < v_to
      and max > 0 and qtype is distinct from 'essay'
    union all
    select count(*), sum(coalesce(earned, 0)), sum(max)
    from public.practice_question_results
    where student_id = p_student and created_at >= v_from and created_at < v_to
      and max > 0 and qtype is distinct from 'essay'
  ) x;
  select coalesce(sum(n), 0), coalesce(sum(e), 0), coalesce(sum(m), 0) into v_qb, v_eb, v_mb from (
    select count(*) as n, sum(coalesce(earned, 0)) as e, sum(max) as m
    from public.exam_question_results
    where student_id = p_student and created_at >= v_base_from and created_at < v_from
      and max > 0 and qtype is distinct from 'essay'
    union all
    select count(*), sum(coalesce(earned, 0)), sum(max)
    from public.practice_question_results
    where student_id = p_student and created_at >= v_base_from and created_at < v_from
      and max > 0 and qtype is distinct from 'essay'
  ) x;
  q_now := v_qn; q_base := v_qb;
  acc_now := case when v_mn > 0 then round(100 * v_en / v_mn, 1) end;
  acc_base := case when v_mb > 0 then round(100 * v_eb / v_mb, 1) end;
  gain := case when acc_now is not null and acc_base is not null then round(acc_now - acc_base, 1) end;
  return next;
end; $$;
revoke all on function public.rank_progress_calc(uuid, date) from public, anon, authenticated;

-- ---------- 4. Xét và cộng RP tiến bộ tuần ----------
create or replace function public.rank_eval_progress_week(p_season bigint, p_student uuid, p_at timestamptz)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  v_week date := public.rank_week_start(p_at);
  s public.rank_seasons%rowtype;
  v_min_gain numeric := public.rank_cfg(p_season, 'progress_min_gain_pct', 5);
  v_rp_base int := public.rank_cfg(p_season, 'progress_rp', 15)::int;
  v_rp_max int := public.rank_cfg(p_season, 'progress_rp_max', 25)::int;
  v_step_pct numeric := greatest(public.rank_cfg(p_season, 'progress_step_pct', 5), 0.1);
  v_step_rp int := public.rank_cfg(p_season, 'progress_step_rp', 5)::int;
  v_min_q int := public.rank_cfg(p_season, 'progress_min_questions', 15)::int;
  c record;
  v_need numeric;
  v_rp int;
begin
  if not public.rank_is_student(p_student) then return 0; end if;
  select * into s from public.rank_seasons where id = p_season;
  if s.id is null or s.status <> 'active' then return 0; end if;
  if public.rank_vn_date(p_at) < s.starts_on or public.rank_vn_date(p_at) > s.ends_on then return 0; end if;

  select * into c from public.rank_progress_calc(p_student, v_week);
  if c.q_now < v_min_q or c.q_base < v_min_q or c.gain is null then return 0; end if;

  v_need := least(v_min_gain, 100 - c.acc_base);
  if c.gain < v_need then return 0; end if;

  v_rp := least(v_rp_max, v_rp_base + (floor(greatest(c.gain - v_min_gain, 0) / v_step_pct)::int) * v_step_rp);
  return public.rank_award(p_season, p_student, 'progress_week', v_week::text, v_rp,
    'Tiến bộ tuần ' || to_char(v_week, 'DD/MM') || ': tỉ lệ đúng '
      || replace(c.acc_now::text, '.', ',') || '% (mốc 2 tuần trước '
      || replace(c.acc_base::text, '.', ',') || '%, +' || replace(c.gain::text, '.', ',') || ' điểm %)', null);
end; $$;
revoke all on function public.rank_eval_progress_week(bigint, uuid, timestamptz) from public, anon, authenticated;

-- ---------- 5. Gọi sau khi kết quả từng câu ĐỀ đã ghi (thêm đúng 1 dòng vào hàm hiện có) ----------
create or replace function public.trg_rank_question_results()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  r record;
  v_season bigint;
begin
  for r in select distinct student_id from inserted loop
    if not public.rank_is_student(r.student_id) then continue; end if;
    begin
      v_season := public.rank_season_for_at(r.student_id, now());
      perform public.rank_eval_titles(r.student_id, v_season);
      if v_season is not null then
        perform public.rank_eval_gates(v_season, r.student_id);
        perform public.rank_eval_progress_week(v_season, r.student_id, now());
        perform public.rank_eval_achievements(v_season, r.student_id, now());
        perform public.rank_refresh_student(v_season, r.student_id);
      end if;
    exception when others then
      raise warning 'rank: bỏ qua lỗi khi xét danh hiệu cho %: %', r.student_id, sqlerrm;
    end;
  end loop;
  return null;
end; $$;

-- ---------- 6. Luyện tập: trigger mới, một lần mỗi câu lệnh chèn, bọc lỗi ----------
create or replace function public.trg_rank_progress_practice()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  r record;
  v_season bigint;
begin
  for r in select distinct student_id from inserted loop
    if not public.rank_is_student(r.student_id) then continue; end if;
    begin
      v_season := public.rank_season_for_at(r.student_id, now());
      if v_season is not null then
        perform public.rank_eval_progress_week(v_season, r.student_id, now());
        perform public.rank_refresh_student(v_season, r.student_id);
      end if;
    exception when others then
      raise warning 'rank: bỏ qua lỗi khi xét tiến bộ tuần cho %: %', r.student_id, sqlerrm;
    end;
  end loop;
  return null;
end; $$;
drop trigger if exists trg_rank_progress_practice on public.practice_question_results;
create trigger trg_rank_progress_practice after insert on public.practice_question_results
  referencing new table as inserted
  for each statement execute function public.trg_rank_progress_practice();

-- Kiểm nhanh sau khi chạy (chỉ đọc), thay <uuid học sinh> và tuần (Thứ Hai):
--   select * from public.rank_progress_calc('<uuid học sinh>', date_trunc('week', now() at time zone 'Asia/Ho_Chi_Minh')::date);

-- ============================================================================
-- ROLLBACK: perf/rollback/20260929110000_rank_progress_week.down.sql
-- ============================================================================
