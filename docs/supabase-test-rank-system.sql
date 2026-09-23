-- ============================================================
-- Kiểm chứng hệ thống rank — chạy trong Supabase SQL editor SAU migration rank-system.
-- Toàn bộ nằm trong một giao dịch và ROLLBACK ở cuối: không để lại dữ liệu.
-- Điền 4 giá trị ở khối "THAM SỐ" rồi chạy cả file. Lệch chỗ nào -> raise exception ngay dòng đó.
-- ============================================================
begin;

do $$
declare
  -- ---------- THAM SỐ (sửa cho đúng dữ liệu của mình) ----------
  v_student uuid := (select uc.user_id from public.user_classes uc join public.profiles p on p.id = uc.user_id
                     where uc.status = 'active' and p.role = 'student' order by uc.user_id limit 1);
  v_class bigint := (select uc.class_id from public.user_classes uc where uc.status = 'active' order by uc.class_id limit 1);
  v_exam bigint := (select e.id from public.exams e where e.published order by e.id desc limit 1);
  v_exam2 bigint := (select e.id from public.exams e where e.published order by e.id desc offset 1 limit 1);
  v_admin uuid := (select p.id from public.profiles p where p.role = 'admin' order by p.id limit 1);
  -- --------------------------------------------------------------
  v_season bigint;
  v_season2 bigint;
  v_rp int;
  v_n int;
  v_status jsonb;
  v_tier text;
  v_div int;
  v_err text;
  v_res1 bigint;
begin
  if v_student is null or v_class is null or v_exam is null or v_admin is null then
    raise exception 'Thiếu tham số: student=% class=% exam=% admin=%', v_student, v_class, v_exam, v_admin;
  end if;
  -- SQL editor không có JWT -> giả lập admin đang gọi (auth.uid() đọc từ request.jwt.claims).
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);
  -- học sinh phải thuộc lớp này
  if not exists (select 1 from public.user_classes where user_id = v_student and class_id = v_class and status = 'active') then
    select class_id into v_class from public.user_classes where user_id = v_student and status = 'active' limit 1;
  end if;

  -- Dọn mùa active trùng khoảng (chỉ trong giao dịch này — rollback sẽ trả lại).
  update public.rank_seasons set status = 'closed' where status = 'active';

  -- ---------- (c) ranh giới bậc / phân bậc ----------
  insert into public.rank_seasons (name, starts_on, ends_on, class_ids, status)
  values ('TEST mùa 1', current_date - 30, current_date + 30, array[v_class], 'active') returning id into v_season;
  perform public.rank_seed_tiers(v_season);

  select division into v_div from public.rank_tier_info(v_season, 'tan_binh', 0);
  if v_div <> 3 then raise exception 'c1: 0 RP phải là Tân Binh III, được %', v_div; end if;
  select division into v_div from public.rank_tier_info(v_season, 'tan_binh', 199);
  if v_div <> 1 then raise exception 'c2: 199 RP phải là Tân Binh I, được %', v_div; end if;
  if public.rank_tier_code_by_rp(v_season, 199) <> 'tan_binh' then raise exception 'c3: 199 RP vẫn là Tân Binh'; end if;
  if public.rank_tier_code_by_rp(v_season, 200) <> 'chien_binh' then raise exception 'c4: 200 RP phải là Chiến Binh'; end if;
  select division into v_div from public.rank_tier_info(v_season, 'chien_binh', 200);
  if v_div <> 3 then raise exception 'c5: 200 RP phải là Chiến Binh III'; end if;
  -- không hở/chồng: mọi RP 0..2599 rơi vào đúng 1 phân bậc, biên liền nhau
  for v_n in 0..2599 loop
    if not exists (select 1 from public.rank_tier_info(v_season, public.rank_tier_code_by_rp(v_season, v_n), v_n) i
                   where v_n between i.div_min and coalesce(i.div_max, 999999)) then
      raise exception 'c6: RP % không rơi vào phân bậc nào', v_n;
    end if;
  end loop;
  -- ngưỡng sai thứ tự bị chặn
  begin
    update public.rank_tiers set min_rp = 100 where season_id = v_season and code = 'tinh_anh';
    raise exception 'c7: phải chặn ngưỡng Tinh Anh < Chiến Binh';
  exception when others then
    if sqlerrm like 'c7%' then raise; end if;
  end;

  -- ---------- (a) cộng phần chênh lệch ----------
  insert into public.rank_sources (season_id, source_kind, source_id, max_rp) values (v_season, 'exam', v_exam, 20);
  insert into public.exam_results (student_id, exam_id, score, detail) values (v_student, v_exam, 6, '{}') returning id into v_res1;
  select rp into v_rp from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  if v_rp <> 12 then raise exception 'a1: 6 điểm -> 12 RP, được %', v_rp; end if;

  insert into public.exam_results (student_id, exam_id, score, detail) values (v_student, v_exam, 9, '{}');
  select rp into v_rp from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  if v_rp <> 18 then raise exception 'a2: 9 điểm -> tổng 18 RP (cộng thêm 6), được %', v_rp; end if;
  select count(*) into v_n from public.rank_rp_ledger where season_id = v_season and student_id = v_student and source_kind = 'practice';
  if v_n <> 2 then raise exception 'a3: phải có 2 dòng ledger (+12, +6), có %', v_n; end if;
  if (select sum(amount) from public.rank_rp_ledger where season_id = v_season and student_id = v_student and source_kind = 'practice') <> 18 then
    raise exception 'a4: tổng ledger phải = 18';
  end if;

  -- nộp lại 9 (bằng mức cũ) và 7 (thấp hơn) -> không đổi, không thêm ledger
  insert into public.exam_results (student_id, exam_id, score, detail) values (v_student, v_exam, 9, '{}');
  insert into public.exam_results (student_id, exam_id, score, detail) values (v_student, v_exam, 7, '{}');
  select rp into v_rp from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  if v_rp <> 18 then raise exception 'a5: nộp lại không được cộng trùng, RP = %', v_rp; end if;
  select count(*) into v_n from public.rank_rp_ledger where season_id = v_season and student_id = v_student and source_kind = 'practice';
  if v_n <> 2 then raise exception 'a6: ledger vẫn phải 2 dòng, có %', v_n; end if;

  -- bài không nằm trong rank_sources -> không cộng
  if v_exam2 is not null then
    insert into public.exam_results (student_id, exam_id, score, detail) values (v_student, v_exam2, 10, '{}');
    select rp into v_rp from public.rank_student_seasons where season_id = v_season and student_id = v_student;
    if v_rp <> 18 then raise exception 'a7: bài chưa được cho phép không được cộng RP'; end if;
  end if;

  -- ---------- (b) tính lại (recompute) idempotent ----------
  perform public.rank_recompute_student(v_season, v_student);
  select rp into v_rp from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  -- em có thể đã làm thật đề này trong khung mùa với điểm cao hơn -> RP chỉ được tăng, không giảm
  if v_rp < 18 then raise exception 'b1: tính lại không được làm giảm RP, = %', v_rp; end if;

  -- ---------- (c') đủ RP nhưng thiếu điều kiện ----------
  -- Bước (b) đã xét lịch sử THẬT của em -> có thể em đã có danh hiệu Thức Tỉnh; kiểm theo đúng tình huống.
  perform public.rank_adjust_rp(v_season, v_student, 600, 'test: đẩy RP');
  v_n := public.rank_titles_at_level(v_student, 'thuc_tinh');
  select tier_code, division into v_tier, v_div from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  v_status := public.rank_status_of(v_student);
  if v_n = 0 then
    if v_tier <> 'chien_binh' then raise exception 'c8: 618 RP chưa có danh hiệu phải kẹt ở Chiến Binh, được %', v_tier; end if;
    if v_div <> 1 then raise exception 'c9: kẹt điều kiện thì đứng ở phân bậc I, được %', v_div; end if;
    if (v_status -> 'next' ->> 'code') <> 'tinh_anh' then raise exception 'c10: bậc tiếp theo phải là Tinh Anh: %', v_status -> 'next'; end if;
    if (v_status -> 'next' -> 'gate' ->> 'required_title_count')::int <> 1 then raise exception 'c11: phải báo cần 1 danh hiệu'; end if;
    if (v_status -> 'next' -> 'gate' ->> 'passed')::boolean then raise exception 'c12: chưa được vượt điều kiện'; end if;
  else
    raise notice 'c8–c12: em đã có % danh hiệu Thức Tỉnh từ dữ liệu thật -> kiểm ngược lại (phải lên Tinh Anh)', v_n;
    if v_tier <> 'tinh_anh' then raise exception 'c8b: có danh hiệu rồi thì 618 RP phải là Tinh Anh, được %', v_tier; end if;
    if (v_status -> 'next' ->> 'code') <> 'tinh_nhue' then raise exception 'c10b: bậc tiếp theo phải là Tinh Nhuệ: %', v_status -> 'next'; end if;
  end if;

  -- cấp một danh hiệu Thức Tỉnh (giả lập) -> vượt điều kiện Tinh Anh
  perform public.rank_grant_title(v_student, 'ke_san_quy_dao', 'thuc_tinh', v_season, '{"test":true}');
  perform public.rank_eval_gates(v_season, v_student);
  perform public.rank_refresh_student(v_season, v_student);
  select tier_code into v_tier from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  if v_tier <> 'tinh_anh' then raise exception 'c13: có danh hiệu rồi phải lên Tinh Anh, được %', v_tier; end if;

  -- Cao Thủ cần thử thách: đẩy tới 2100 RP, cấp đủ danh hiệu Làm Chủ nhưng chưa gán đề -> kẹt Đại Sư
  perform public.rank_adjust_rp(v_season, v_student, 1500, 'test: đẩy RP');
  perform public.rank_grant_title(v_student, 'ke_san_quy_dao', 'lam_chu', v_season, '{}');
  perform public.rank_grant_title(v_student, 'bac_thay_gia_toc', 'thuc_tinh', v_season, '{}');
  perform public.rank_grant_title(v_student, 'bac_thay_gia_toc', 'lam_chu', v_season, '{}');
  perform public.rank_eval_gates(v_season, v_student);
  perform public.rank_refresh_student(v_season, v_student);
  select tier_code into v_tier from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  if v_tier <> 'dai_su' then raise exception 'c14: chưa có đề thử thách thì kẹt Đại Sư, được %', v_tier; end if;
  -- gán đề thử thách và làm đạt -> Cao Thủ
  update public.rank_tiers set challenge_exam_id = v_exam, challenge_pass_score = 8 where season_id = v_season and code = 'cao_thu';
  perform public.rank_eval_gates(v_season, v_student);   -- điểm tốt nhất trên v_exam là 9 (đã nộp ở trên)
  perform public.rank_refresh_student(v_season, v_student);
  select tier_code into v_tier from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  if v_tier <> 'cao_thu' then raise exception 'c15: vượt thử thách phải lên Cao Thủ, được %', v_tier; end if;

  -- ---------- (e) đeo danh hiệu (giả lập chính em sửa hồ sơ — admin thì được bỏ qua kiểm tra) ----------
  perform set_config('request.jwt.claims', json_build_object('sub', v_student, 'role', 'authenticated')::text, true);
  update public.profiles set display_title_code = 'ke_san_quy_dao', display_title_level = 'lam_chu' where id = v_student;
  begin
    update public.profiles set display_title_code = 'chua_te_song', display_title_level = 'lam_chu' where id = v_student;
    raise exception 'e1: phải chặn đeo danh hiệu chưa có';
  exception when others then
    if sqlerrm like 'e1%' then raise; end if;
  end;
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);

  -- ---------- (d) đóng mùa, mùa mới từ 0 ----------
  v_n := public.rank_close_season(v_season);
  if v_n < 1 then raise exception 'd1: đóng mùa phải lưu ít nhất 1 học sinh'; end if;
  if not exists (select 1 from public.rank_season_results where season_id = v_season and student_id = v_student and tier_code = 'cao_thu') then
    raise exception 'd2: kết quả mùa phải ghi Cao Thủ';
  end if;
  if (select count(*) from public.rank_rp_ledger where season_id = v_season and student_id = v_student) < 4 then
    raise exception 'd3: ledger mùa cũ phải còn nguyên';
  end if;
  if (select count(*) from public.rank_title_awards where student_id = v_student) < 4 then
    raise exception 'd4: danh hiệu phải giữ qua mùa';
  end if;
  insert into public.rank_seasons (name, starts_on, ends_on, class_ids, status)
  values ('TEST mùa 2', current_date - 1, current_date + 40, array[v_class], 'active') returning id into v_season2;
  perform public.rank_seed_tiers(v_season2);
  v_status := public.rank_status_of(v_student);
  if (v_status ->> 'rp')::int <> 0 then raise exception 'd5: mùa mới phải bắt đầu 0 RP, được %', v_status ->> 'rp'; end if;
  if (v_status ->> 'titles_count')::int < 2 then raise exception 'd6: mùa mới vẫn thấy danh hiệu cũ'; end if;

  -- ---------- (f) quyền: học sinh không gọi được RPC giáo viên ----------
  perform set_config('request.jwt.claims', json_build_object('sub', v_student, 'role', 'authenticated')::text, true);
  perform set_config('role', 'authenticated', true);
  begin
    perform public.rank_adjust_rp(v_season2, v_student, 999, 'hack');
    raise exception 'f1: học sinh không được tự cộng RP';
  exception when others then
    if sqlerrm like 'f1%' then raise; end if;
  end;
  begin
    perform public.rank_close_season(v_season2);
    raise exception 'f2: học sinh không được đóng mùa';
  exception when others then
    if sqlerrm like 'f2%' then raise; end if;
  end;
  begin
    insert into public.rank_rp_ledger (season_id, student_id, source_kind, amount) values (v_season2, v_student, 'manual', 999);
    raise exception 'f3: học sinh không được ghi thẳng ledger';
  exception when others then
    if sqlerrm like 'f3%' then raise; end if;
  end;
  -- nhưng đọc được trạng thái của mình và đổi danh hiệu đeo của mình
  if public.rank_my_status() is null then raise exception 'f4: học sinh phải đọc được trạng thái của mình'; end if;
  perform public.rank_set_display_title('ke_san_quy_dao', 'thuc_tinh');
  begin
    perform public.rank_set_display_title('chua_te_song', 'lam_chu');
    raise exception 'f5: không được đeo danh hiệu chưa có';
  exception when others then
    if sqlerrm like 'f5%' then raise; end if;
  end;
  perform set_config('role', 'postgres', true);
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);

  raise notice 'RANK TEST: tất cả kiểm chứng đã qua (a, b, c, d, e, f). Sửa sai (g) cần dữ liệu exam_question_results thật — xem hướng dẫn UI.';
end $$;

rollback;
