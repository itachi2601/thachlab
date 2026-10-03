-- ============================================================
-- Kiểm chứng "RP chỉ tính lượt đầu" (rank_on_result) — chạy SAU migration 20261003110000_rank_rp_first_attempt.sql:
--   supabase db query --linked -f docs/supabase-test-rank-rp-first.sql
-- Một giao dịch, ROLLBACK ở cuối. Lệch chỗ nào -> raise exception 'C…: …'; chạy xong không lỗi = đạt.
-- ============================================================
begin;

do $$
declare
  v_student uuid;
  v_class bigint;
  v_season bigint;
  v_exam1 bigint;
  v_exam2 bigint;
  v_rp int;
  v_rows int;
begin
  select uc.user_id, uc.class_id into v_student, v_class
  from public.user_classes uc
  join public.profiles p on p.id = uc.user_id and p.role = 'student'
  where uc.status = 'active' order by uc.user_id limit 1;
  select id into v_exam1 from public.exams where published order by id desc limit 1;
  select id into v_exam2 from public.exams where published and id <> v_exam1 order by id desc limit 1;
  if v_student is null or v_exam1 is null or v_exam2 is null then raise exception 'C0: thiếu học sinh/đề để thử'; end if;

  update public.rank_seasons set status = 'closed' where status = 'active';
  insert into public.rank_seasons (name, starts_on, ends_on, class_ids, status, config)
  values ('TEST rp-first', current_date - 1, current_date + 30, array[v_class], 'active', '{}'::jsonb)
  returning id into v_season;
  perform public.rank_seed_tiers(v_season);
  insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
  values (v_season, 'exam', v_exam1, 60, true), (v_season, 'exam', v_exam2, 60, true);

  -- lượt 1 điểm 5 -> 30 RP; lượt 2 điểm 10 -> KHÔNG thêm (mặc định chỉ lượt đầu)
  perform public.rank_on_result(v_student, 'exam', v_exam1, 5, now(), null);
  select coalesce(sum(awarded), 0) into v_rp from public.rank_rp_awards where season_id = v_season and student_id = v_student;
  if v_rp <> 30 then raise exception 'C1: lượt đầu điểm 5 phải 30 RP, được %', v_rp; end if;
  perform public.rank_on_result(v_student, 'exam', v_exam1, 10, now(), null);
  select coalesce(sum(awarded), 0) into v_rp from public.rank_rp_awards where season_id = v_season and student_id = v_student;
  if v_rp <> 30 then raise exception 'C2: làm lại điểm cao hơn không được cộng thêm, được %', v_rp; end if;
  if (select rp from public.rank_student_seasons where season_id = v_season and student_id = v_student) <> 30 then
    raise exception 'C2b: rank_student_seasons.rp phải là 30';
  end if;
  select count(*) into v_rows from public.rank_rp_ledger where season_id = v_season and student_id = v_student and source_kind = 'practice';
  if v_rows <> 1 then raise exception 'C2c: ledger phải có đúng 1 dòng, được %', v_rows; end if;

  -- lượt đầu 0 điểm: dòng awarded = 0 vẫn "chiếm chỗ" -> lượt sau điểm cao không được cộng
  perform public.rank_on_result(v_student, 'exam', v_exam2, 0, now(), null);
  perform public.rank_on_result(v_student, 'exam', v_exam2, 10, now(), null);
  select coalesce(sum(awarded), 0) into v_rp from public.rank_rp_awards where season_id = v_season and student_id = v_student and source_ref = 'exam:' || v_exam2;
  if v_rp <> 0 then raise exception 'C3: lượt đầu 0 điểm, lượt sau 10 điểm vẫn phải 0 RP, được %', v_rp; end if;

  -- tắt cờ -> như cũ (điểm tốt nhất): nâng exam1 từ 30 lên 60
  update public.rank_seasons set config = config || '{"rp_first_attempt_only":0}'::jsonb where id = v_season;
  perform public.rank_on_result(v_student, 'exam', v_exam1, 10, now(), null);
  select coalesce(sum(awarded), 0) into v_rp from public.rank_rp_awards where season_id = v_season and student_id = v_student and source_ref = 'exam:' || v_exam1;
  if v_rp <> 60 then raise exception 'C4: cờ = 0 phải tính điểm tốt nhất (60 RP), được %', v_rp; end if;

  -- bật lại, gọi lại nhiều lần (giống rank_recompute) -> không cộng đôi
  update public.rank_seasons set config = config || '{"rp_first_attempt_only":1}'::jsonb where id = v_season;
  perform public.rank_on_result(v_student, 'exam', v_exam1, 10, now(), null);
  perform public.rank_on_result(v_student, 'exam', v_exam1, 10, now(), null);
  select coalesce(sum(awarded), 0) into v_rp from public.rank_rp_awards where season_id = v_season and student_id = v_student and source_ref = 'exam:' || v_exam1;
  if v_rp <> 60 then raise exception 'C5: gọi lại không được cộng thêm, được %', v_rp; end if;
end $$;

rollback;
