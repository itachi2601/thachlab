-- ============================================================
-- Migration: loại tài khoản không phải học sinh khỏi hệ thống Rank/RP
--
-- Vấn đề: mọi UI hiển thị rank (Bậc trong lớp, Bảng tuần, Xếp hạng mùa cho
-- admin) đều lọc `profiles.role = 'student'` nên GV/admin không LỘ RA màn
-- hình — nhưng trigger cộng RP (trg_rank_exam_result / trg_rank_practice_session
-- / trg_rank_question_results) không hề kiểm tra role: nếu GV/admin tự làm
-- một bài luyện tập/đề để test tính năng, tài khoản đó vẫn bị ghi vào
-- rank_student_seasons (và sẽ có RP thật nếu bài đó tính RP). Đây là gốc của
-- việc "lọt vào bảng xếp hạng chung" mà thầy Thạch (role=admin) gặp phải.
--
-- Sửa: thêm rank_is_student() và chặn ngay từ điểm vào (rank_on_result,
-- rank_ensure_member, trg_rank_question_results) — tài khoản không phải
-- role='student' không bao giờ được tạo dòng rank_student_seasons / cộng RP /
-- cấp danh hiệu nữa. Dọn luôn dữ liệu rác đã lỡ tạo trước đó.
--
-- Idempotent — chạy lại được (create or replace function; delete có điều kiện).
-- Rollback: perf/rollback/20260926110000_rank_exclude_staff.down.sql
-- ============================================================

create or replace function public.rank_is_student(p_student uuid)
returns boolean
language sql security definer stable set search_path = public
as $$
  select exists (select 1 from public.profiles where id = p_student and role = 'student');
$$;

-- Không tạo dòng thành viên mùa cho tài khoản không phải học sinh.
create or replace function public.rank_ensure_member(p_season bigint, p_student uuid)
returns void
language sql security definer set search_path = public
as $$
  insert into public.rank_student_seasons (season_id, student_id)
  select p_season, p_student
  where public.rank_is_student(p_student)
  on conflict (season_id, student_id) do nothing;
$$;

-- Chặn sớm nhất có thể: bỏ qua toàn bộ xử lý RP nếu không phải học sinh.
create or replace function public.rank_on_result(
  p_student uuid, p_kind text, p_source_id bigint, p_score numeric, p_at timestamptz, p_result_ref bigint
)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_season bigint;
  v_src public.rank_sources%rowtype;
  v_title text;
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

-- Xét danh hiệu theo câu hỏi cũng phải bỏ qua tài khoản không phải học sinh.
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
        perform public.rank_eval_achievements(v_season, r.student_id, now());
        perform public.rank_refresh_student(v_season, r.student_id);
      end if;
    exception when others then
      raise warning 'rank: bỏ qua lỗi khi xét danh hiệu cho %: %', r.student_id, sqlerrm;
    end;
  end loop;
  return null;
end; $$;

-- ---------- Dọn dữ liệu rác đã lỡ tạo cho tài khoản không phải học sinh ----------
delete from public.rank_student_seasons rss
  using public.profiles p
  where p.id = rss.student_id and p.role <> 'student';

delete from public.rank_rp_awards a
  using public.profiles p
  where p.id = a.student_id and p.role <> 'student';

delete from public.rank_rp_ledger l
  using public.profiles p
  where p.id = l.student_id and p.role <> 'student';

delete from public.rank_title_awards ta
  using public.profiles p
  where p.id = ta.student_id and p.role <> 'student';

delete from public.rank_gate_passes gp
  using public.profiles p
  where p.id = gp.student_id and p.role <> 'student';

delete from public.rank_fix_attempts fa
  using public.profiles p
  where p.id = fa.student_id and p.role <> 'student';

delete from public.rank_season_results sr
  using public.profiles p
  where p.id = sr.student_id and p.role <> 'student';

update public.profiles
  set display_title_code = null, display_title_level = null
  where role <> 'student' and display_title_code is not null;
