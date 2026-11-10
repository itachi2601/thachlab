-- ============================================================================
-- feat(rank): đóng mùa #5 "Alpha test" + mở 4 mùa mới theo khối, 02/11/2026 → 17/01/2027 (thầy duyệt 5/11/2026)
--
--   "Mùa 2 · Lôi Đình Cảm Ứng"  → lớp 12 (class 18)      nguồn RP chép từ mùa 4 (phần thuộc lớp 12)
--   "Mùa 2 · Thợ Săn Sóng"      → lớp 11 (class 17)      nguồn RP chép từ mùa 4 (phần thuộc lớp 11)
--   "Mùa 2 · Kỷ Nguyên Newton"  → lớp 10 (class 16)      nguồn RP chép từ mùa 5
--   "Mùa 1 · Bẻ Cong Ánh Sáng"  → KHTN 9 (15) + HSG 9 (19)  chưa có mùa cũ
-- 11 tuần (T2 02/11 → CN 17/01), status 'active'. Không chép rank_gate_passes (quy tắc 3); danh hiệu giữ nguyên.
--
-- ---------------------------------------------------------------------------
-- NGƯỠNG BẬC — lập luận (số liệu thật dump 5/11, 4 quy tắc "Mùa sau" ở docs/memory/project_thachlab_rank_gate_adaptive.md)
-- ---------------------------------------------------------------------------
--   Mùa 4 (L11+L12, 5 tuần): p50 155, p90 374, max 591. Mùa 5 (L10, 5 tuần): p50 135, p90 301, max 948.
--   Mùa mới 11 tuần: 11/5 = 2,2; trừ ~10% (nhịp giảm giữa mùa dài, thưởng tuần 30 → 25) → hệ số ~2,0.
--   Dự báo cuối mùa: L11/L12 p50 ~310, p90 ~750, max ~1.200; L10 p50 ~270, p90 ~600.
--
--   Lượt nộp XẤU NHẤT (quy tắc 4) với config dưới đây:
--     bài vừa sàn 6,0 điểm trên nguồn 20 RP ................ 12   (rank_score_to_rp(6, 20))
--     + thưởng tuần (bài này là bài thứ 2 đạt >= 6) ......... 25   (weekly_goal_rp, kẹp thêm weekly_goal_rp_max 25)
--     + chuỗi ngày ......................................... 5    (thực tế cần >= 7 điểm nên bài 6,0 KHÔNG nhận; cộng dự phòng)
--     + tiến bộ tuần (trần) ................................ 15   (progress_rp_max; cần đúng >= 60%)
--     = 57 RP  <  60 = phân bậc hẹp nhất (180 / 3)  → một bài sát sàn KHÔNG vượt quá một phân bậc.
--   Ca cực đoan hơn (bài 10 điểm 20 + 25 + 5 + 15 + mục tiêu cả lớp 10) = 75 < 120 = 2 phân bậc → không lượt nộp nào
--   nhảy qua trọn một phân bậc. Bài < 5 (thực tế < 6) không bao giờ xong tuần (quy tắc 2: score_floor 6, abs_floor 6,
--   count_min 2). Mỗi khoản thưởng một cục (25, 15, 10, 5) < 60 (quy tắc 1). Sửa sai fix_max_rp 30 và lý thuyết
--   (15 + 5 thưởng, trần ngày 45) là lượt nộp riêng, cũng < 60.
--   => Phân bậc phải >= 58 → bậc >= 174 → làm tròn 180 (phân bậc 60). Bậc đều 180:
--        Đồng 0 · Bạc 180 · Vàng 360 · Bạch Kim 540 · Kim Cương 720 · Tinh Anh 900 · Cao Thủ 1080
--   So "mùa 4 × 2" (108/256/428/600/750/898): đáy cao hơn (bắt buộc bởi quy tắc 1+4), đỉnh khớp — Tinh Anh 900 ≈ p90–p95
--   dự báo (mùa 4: Tinh Anh = p90), Cao Thủ = 1,2 × Tinh Anh như mùa 4. Vàng trở lên vẫn cần danh hiệu + thi cửa.
--   RP lý thuyết cả mùa bị kẹp 25% × 1080 = 270 (theory_season_cap_pct).
--
-- CONFIG = config mùa 4 (gốc) || chỉnh:
--   practice_max_rp 60 → 20   (mặc định max_rp khi thầy bật bài mới trong RankAdmin; 60 sẽ phá quy tắc 1)
--   weekly_goal_rp 30 → 25, thêm weekly_goal_rp_max 25, weekly_goal_count 2, weekly_goal_count_min 2 (mặc định hàm là 1!),
--   weekly_goal_score_floor 6, weekly_goal_abs_floor 6, weekly_goal_min_score 7 (giữ), daily_streak_rp 5,
--   progress_rp 10 / progress_rp_max 15 (mặc định 15/25), progress_min_acc_pct 60, class_goal_rp 10, rp_first_attempt_only 0 (giữ).
--   Key thật được đọc (rank_cfg): weekly_goal_count = số bài khi CHƯA có mục tiêu riêng; weekly_goal_count_min = sàn số
--   bài của mục tiêu riêng (rank_weekly_goal_of) — phải đặt cả hai.
--
-- NGUỒN RP (rank_sources):
--   a) chép mùa 4 → mùa 12/11 theo lớp suy ra (exam_classes ∪ lesson_items.exam_ids→lessons→chapter_classes; practice_item
--      → lesson_items→lessons→chapter_classes). Nguồn mùa 4 không suy ra được lớp 11/12 → đưa vào CẢ HAI mùa (an toàn: em
--      chỉ nhận RP ở mùa của lớp mình, cùng max_rp như mùa 4). Chép mùa 5 → mùa 10 nguyên trạng.
--   b) bật thêm (không đè dòng đã chép) theo đúng luật đợt 11/10, 17/10: đề trong mục BTVN/Kiểm tra của chương thuộc lớp;
--      đề định kỳ class_assessments; đề "Kiểm tra nhanh/Kiểm tra hiểu bài/Luyện tập" lẻ gắn lớp (exam_classes) không nằm
--      trong mục Luyện tập; đề HS của mùa đã nộp từ 02/11. Max: 10 RP nếu tiêu đề bắt đầu "Kiểm tra nhanh" / "Kiểm tra hiểu
--      bài" / "Luyện tập", còn lại 20. Mục Luyện tập (practice_item) của chương thuộc lớp + mục HS đã nộp từ 02/11: 20 RP.
--   Lớp 19 (HSG 9) không có chapter_classes riêng: chương môn 'hsg-vat-ly' tính là của lớp 19.
--
-- CUỐI FILE: rank_recompute_season cho 4 mùa (bài nộp 02/11 → nay được cộng; chỉ quét từ 02/11 nên nhẹ). Cần staff →
-- giả lập JWT admin trong giao dịch (như 20261011160000). Lưu ý: RP lý thuyết 02–05/11 KHÔNG được tính bù (recompute chỉ
-- phát lại exam_results/practice_sessions). Chuông "+N RP · Đạt mục tiêu tuần" sẽ gửi cho em đạt tuần 02/11.
--
-- Idempotent: mùa tìm theo name; tiers/sources on conflict do nothing; chỉ đóng mùa 5 khi còn 'active'.
-- Cách chạy: bash scripts/run-migrations.sh --only N — NGOÀI giờ HS làm bài (đổi bảng xếp hạng + recompute ~350 HS).
-- Rollback: perf/rollback/20261105200000_rank_mo_mua_2.down.sql
-- ============================================================================

begin;

do $$
declare
  v_admin uuid;
  s4 public.rank_seasons%rowtype;
  s5 public.rank_seasons%rowtype;
  v_cfg jsonb;
  r record;
  v_id bigint;
  v_closed int := 0;
  v_n int;
  v_ids bigint[] := '{}';
begin
  -- 0. Quyền staff cho các hàm rank_* (auth.uid() = admin trong giao dịch này).
  select id into v_admin from public.profiles where role = 'admin' order by created_at limit 1;
  if v_admin is null then raise exception 'Không tìm thấy admin'; end if;
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);

  select * into s4 from public.rank_seasons where id = 4;
  if s4.id is null or s4.status <> 'closed' then raise exception 'Mùa 4 chưa đóng — dừng'; end if;
  if (select count(*) from public.rank_tiers where season_id = 4) <> 7 then raise exception 'Mùa 4 không đủ 7 bậc — dừng'; end if;

  -- 1. Đóng mùa 5 bằng chính rank_close_season (chụp rank_season_results đầy đủ như mùa 4).
  select * into s5 from public.rank_seasons where id = 5;
  if s5.id is null or s5.name <> 'Alpha test' then raise exception 'Mùa 5 không phải "Alpha test" — dừng'; end if;
  if s5.status = 'active' then
    v_closed := public.rank_close_season(5);
  end if;

  v_cfg := coalesce(s4.config, '{}'::jsonb) || jsonb_build_object(
    'practice_max_rp', 20,
    'weekly_goal_rp', 25, 'weekly_goal_rp_max', 25,
    'weekly_goal_count', 2, 'weekly_goal_count_min', 2,
    'weekly_goal_min_score', 7, 'weekly_goal_score_floor', 6, 'weekly_goal_abs_floor', 6,
    'daily_streak_rp', 5,
    'progress_rp', 10, 'progress_rp_max', 15, 'progress_min_acc_pct', 60,
    'class_goal_rp', 10,
    'rp_first_attempt_only', 0);

  -- Bản đồ chương → lớp (chương HSG Vật lí 'hsg-vat-ly' tính thêm cho lớp 19).
  create temp table _m2_chap on commit drop as
    select cc.chapter_id, cc.class_id from public.chapter_classes cc
    union
    select ch.id, 19::bigint from public.chapters ch where ch.subject_code = 'hsg-vat-ly';

  -- Bản đồ nguồn → lớp.
  create temp table _m2_src_cls on commit drop as
    select 'exam'::text as kind, ec.exam_id as id, ec.class_id from public.exam_classes ec
    union
    select 'exam', x.exam_id, m.class_id
      from public.lesson_items li
      cross join lateral unnest(li.exam_ids) as x(exam_id)
      join public.lessons l on l.id = li.lesson_id
      join _m2_chap m on m.chapter_id = l.chapter_id
    union
    select 'practice_item', li.id, m.class_id
      from public.lesson_items li
      join public.lessons l on l.id = li.lesson_id
      join _m2_chap m on m.chapter_id = l.chapter_id
     where li.kind = 'luyen_tap';

  for r in
    select * from (values
      (1, 'Mùa 2 · Lôi Đình Cảm Ứng', array[18]::bigint[], 4::bigint),
      (2, 'Mùa 2 · Thợ Săn Sóng',     array[17]::bigint[], 4::bigint),
      (3, 'Mùa 2 · Kỷ Nguyên Newton', array[16]::bigint[], 5::bigint),
      (4, 'Mùa 1 · Bẻ Cong Ánh Sáng', array[15, 19]::bigint[], null::bigint)
    ) v(ord, name, class_ids, src_season)
    order by ord
  loop
    -- 2. Mùa (idempotent theo tên).
    select id into v_id from public.rank_seasons where name = r.name;
    if v_id is null then
      insert into public.rank_seasons (name, starts_on, ends_on, class_ids, status, config, created_by)
      values (r.name, date '2026-11-02', date '2027-01-17', r.class_ids, 'active', v_cfg, v_admin)
      returning id into v_id;
    end if;
    v_ids := v_ids || v_id;

    -- 3. Bậc: tên/code/điều kiện/cửa như mùa 4, chỉ đổi min_rp.
    insert into public.rank_tiers (season_id, code, sort, name, min_rp, has_divisions,
      required_title_count, required_title_level, challenge_exam_id, challenge_pass_score,
      gate_pass_pct, gate_min_hard_correct, gate_min_level_held)
    select v_id, t.code, t.sort, t.name, m.min_rp, t.has_divisions,
           t.required_title_count, t.required_title_level, t.challenge_exam_id, t.challenge_pass_score,
           t.gate_pass_pct, t.gate_min_hard_correct, t.gate_min_level_held
      from public.rank_tiers t
      join (values ('tan_binh', 0), ('chien_binh', 180), ('tinh_anh', 360), ('tinh_nhue', 540),
                   ('dai_su', 720), ('cao_thu', 900), ('thach_dau', 1080)) m(code, min_rp) on m.code = t.code
     where t.season_id = 4
     order by t.sort
    on conflict (season_id, code) do nothing;

    -- 4a. Chép nguồn từ mùa cũ.
    if r.src_season = 4 then
      insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
      select v_id, rs.source_kind, rs.source_id, rs.max_rp, rs.enabled
        from public.rank_sources rs
       where rs.season_id = 4
         and (exists (select 1 from _m2_src_cls c
                       where c.kind = rs.source_kind and c.id = rs.source_id and c.class_id = any (r.class_ids))
              or not exists (select 1 from _m2_src_cls c
                       where c.kind = rs.source_kind and c.id = rs.source_id and c.class_id in (17, 18)))
      on conflict (season_id, source_kind, source_id) do nothing;
    elsif r.src_season = 5 then
      insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
      select v_id, rs.source_kind, rs.source_id, rs.max_rp, rs.enabled
        from public.rank_sources rs where rs.season_id = 5
      on conflict (season_id, source_kind, source_id) do nothing;
    end if;

    -- 4b. Đề còn thiếu.
    insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
    select v_id, 'exam', e.id,
           case when e.title ilike 'Kiểm tra nhanh%' or e.title ilike 'Kiểm tra hiểu bài%' or e.title ilike 'Luyện tập%'
                then 10 else 20 end,
           true
      from public.exams e
     where e.id in (
             -- đề trong mục BTVN / Kiểm tra của chương thuộc lớp
             select x.exam_id from public.lesson_items li
               cross join lateral unnest(li.exam_ids) as x(exam_id)
               join public.lessons l on l.id = li.lesson_id
               join _m2_chap m on m.chapter_id = l.chapter_id and m.class_id = any (r.class_ids)
              where li.kind in ('bai_tap_ve_nha', 'kiem_tra')
             union
             -- đề định kỳ của lớp
             select ca.exam_id from public.class_assessments ca
              where ca.class_id = any (r.class_ids) and ca.exam_id is not null
             union
             -- Kiểm tra nhanh / hiểu bài / Luyện tập lẻ gắn lớp, không nằm trong mục Luyện tập (đã tính qua practice_item)
             select e2.id from public.exams e2
              where e2.published
                and (e2.title ilike 'Kiểm tra nhanh%' or e2.title ilike 'Kiểm tra hiểu bài%' or e2.title ilike 'Luyện tập%')
                and exists (select 1 from public.exam_classes ec where ec.exam_id = e2.id and ec.class_id = any (r.class_ids))
                and not exists (select 1 from public.lesson_items li where li.kind = 'luyen_tap' and e2.id = any (li.exam_ids))
             union
             -- đề HS của mùa đã nộp từ ngày mở mùa
             select er.exam_id from public.exam_results er
              where er.created_at >= (date '2026-11-02')::timestamp at time zone 'Asia/Ho_Chi_Minh'
                and er.student_id in (select uc.user_id from public.user_classes uc
                                       where uc.status = 'active' and uc.class_id = any (r.class_ids)))
    on conflict (season_id, source_kind, source_id) do nothing;

    -- 4c. Mục Luyện tập còn thiếu.
    insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
    select v_id, 'practice_item', li.id, 20, true
      from public.lesson_items li
     where li.kind = 'luyen_tap'
       and li.id in (
             select c.id from _m2_src_cls c
              where c.kind = 'practice_item' and c.class_id = any (r.class_ids)
             union
             select ps.item_id from public.practice_sessions ps
              where ps.created_at >= (date '2026-11-02')::timestamp at time zone 'Asia/Ho_Chi_Minh'
                and ps.student_id in (select uc.user_id from public.user_classes uc
                                       where uc.status = 'active' and uc.class_id = any (r.class_ids)))
    on conflict (season_id, source_kind, source_id) do nothing;
  end loop;

  -- 5. Tính lại RP (bài nộp từ 02/11). Tách ra lệnh riêng nếu giao dịch quá lâu — xem cuối file.
  foreach v_id in array v_ids loop
    v_n := public.rank_recompute_season(v_id);
    raise notice 'Mùa %: tính lại % học sinh', v_id, v_n;
  end loop;
  raise notice 'Đóng mùa 5: % kết quả; mùa mới: %', v_closed, v_ids;
end $$;

commit;

-- Kiểm tra (CLI chỉ in câu cuối):
select s.id, s.name, s.status, s.class_ids, s.starts_on, s.ends_on,
       (select count(*) from public.rank_tiers t where t.season_id = s.id) as n_tiers,
       (select string_agg(t.min_rp::text, '/' order by t.sort) from public.rank_tiers t where t.season_id = s.id) as min_rp,
       (select count(*) from public.rank_sources rs where rs.season_id = s.id and rs.source_kind = 'exam') as src_exam,
       (select count(*) from public.rank_sources rs where rs.season_id = s.id and rs.source_kind = 'practice_item') as src_item,
       (select count(*) from public.rank_student_seasons m where m.season_id = s.id) as members,
       (select count(*) from public.rank_student_seasons m where m.season_id = s.id and m.rp > 0) as members_rp,
       (select max(m.rp) from public.rank_student_seasons m where m.season_id = s.id) as max_rp,
       (select count(*) from public.rank_season_results x where x.season_id = s.id) as results,
       (select count(*) from public.rank_season_results x where x.season_id = s.id and x.snapshot_at is not null) as results_snap,
       s.config ->> 'weekly_goal_rp' as wg_rp, s.config ->> 'weekly_goal_count_min' as wg_cmin
from public.rank_seasons s
where s.id in (4, 5)
   or s.name in ('Mùa 2 · Lôi Đình Cảm Ứng', 'Mùa 2 · Thợ Săn Sóng', 'Mùa 2 · Kỷ Nguyên Newton', 'Mùa 1 · Bẻ Cong Ánh Sáng')
order by s.id;

-- Nếu recompute làm giao dịch quá lâu (Management API timeout): xoá khối "5." ở trên, chạy migration, rồi chạy riêng
-- từng mùa (mỗi lệnh một giao dịch):
--   begin; select set_config('request.jwt.claims', json_build_object('sub', (select id from public.profiles where role = 'admin'
--     order by created_at limit 1), 'role', 'authenticated')::text, true);
--   select public.rank_recompute_season(id) from public.rank_seasons where name = 'Mùa 2 · Lôi Đình Cảm Ứng'; commit;
