-- ============================================================================
-- RP chỉ tính LƯỢT ĐẦU của mỗi bài trong mùa — việc C của docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md
--
-- Số liệu 3/10 (mùa 4): làm lại cùng đề, điểm lượt đầu 4,64 -> điểm tốt nhất 8,48; RP mỗi đề theo điểm TỐT NHẤT
-- nên làm lại nhiều lần "bơm" RP. Từ nay rank_on_result chỉ cộng RP cho lượt đầu của một bài (đề/mục luyện tập) trong
-- mùa: đã có dòng rank_rp_awards (season, student, 'practice', 'exam|practice_item:<id>') thì bỏ qua rank_award
-- (mục tiêu tuần, chuỗi ngày, cửa lên hạng, thành tích, rank_refresh_student vẫn chạy như cũ).
--
-- Config mùa: rp_first_attempt_only (mặc định 1 = chỉ lượt đầu; 0 = như cũ, điểm tốt nhất) — đổi được ở
-- /quan-tri/xep-hang, không cần sửa code.
-- RP đã cộng trước đây GIỮ NGUYÊN (không tính lại, không trừ). rank_recompute_* quét kết quả theo thứ tự thời gian
-- nên cũng chỉ nhận lượt đầu, không cộng đôi.
-- Định nghĩa lại: rank_on_result (bản live = 20260929100000_rank_restore_daily_streak.sql, chỉ thêm khối v_seen).
-- Cách chạy: bash scripts/run-migrations.sh — nên NGOÀI giờ học sinh làm bài (create or replace hàm chạy sau mỗi lần nộp bài).
-- Rollback: perf/rollback/20261003110000_rank_rp_first_attempt.down.sql
-- ============================================================================

CREATE OR REPLACE FUNCTION public.rank_on_result(p_student uuid, p_kind text, p_source_id bigint, p_score numeric, p_at timestamp with time zone, p_result_ref bigint)
 RETURNS void
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $$
declare
  v_season bigint;
  v_src public.rank_sources%rowtype;
  v_title text;
  v_ref text;
  v_seen boolean := false;
begin
  if not public.rank_is_student(p_student) then return; end if;

  v_season := public.rank_season_for_at(p_student, p_at);
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
    v_ref := p_kind || ':' || p_source_id;
    -- RP của một bài = LƯỢT ĐẦU trong mùa (không phải điểm tốt nhất): đã có dòng nhận RP cho bài này thì bỏ qua
    -- phần cộng RP (mục tiêu tuần / chuỗi ngày / cửa / thành tích bên dưới vẫn chạy). Tắt bằng config mùa
    -- rp_first_attempt_only = 0. Khoá tư vấn để hai lượt nộp đồng thời không cùng thấy "chưa có dòng".
    if public.rank_cfg(v_season, 'rp_first_attempt_only', 1) >= 1 then
      perform pg_advisory_xact_lock(hashtextextended('rank_first:' || v_season || ':' || p_student || ':' || v_ref, 0));
      v_seen := exists (
        select 1 from public.rank_rp_awards a
        where a.season_id = v_season and a.student_id = p_student and a.source_kind = 'practice' and a.source_ref = v_ref);
    end if;
    if not v_seen then
      perform public.rank_award(v_season, p_student, 'practice', v_ref,
        public.rank_score_to_rp(p_score, v_src.max_rp),
        'Bài luyện tập: ' || coalesce(v_title, '#' || p_source_id) || ' (' || replace(to_char(p_score, 'FM990.0'), '.', ',') || ' điểm)',
        p_result_ref);
    end if;
    perform public.rank_eval_weekly_goal(v_season, p_student, p_at);
    perform public.rank_eval_daily_streak(v_season, p_student, p_at);
  end if;

  perform public.rank_eval_gates(v_season, p_student);
  perform public.rank_eval_achievements(v_season, p_student, p_at);
  perform public.rank_refresh_student(v_season, p_student);
end; $$;
