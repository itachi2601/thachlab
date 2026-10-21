-- ============================================================================
-- Quiz lý thuyết Chương 3 lớp 12 soạn lại 21/10/2026 (đề mới #1055–#1062 thay #759–762, #768–770, #937)
--  1) Ẩn khỏi ngân hàng câu hỏi (archived=true) các câu của 8 đề cũ — có câu ngoài chương trình. Đề cũ GIỮ NGUYÊN
--     (đã bị gỡ khỏi bài; còn kết quả làm bài của 8 em). Sao lưu: quiz_ch3_l12_bank_backup_20261021.
--  2) Bật 10 RP (như mọi Kiểm tra nhanh) cho 8 đề mới ở mùa đang chạy có lớp 12. RP đã cộng từ đề cũ GIỮ NGUYÊN
--     (khoá source_ref khác nhau, rank_award chỉ cộng delta, không trừ). Làm đúng đề mới được cộng thêm.
--     Sao lưu dòng thêm: quiz_ch3_l12_sources_backup_20261021.
--  3) Thông báo cho các em đã làm đề cũ: làm lại bộ mới (mỗi em một thông báo, kind 'quiz_updated').
-- Rollback: perf/rollback/20261021200000_quiz_ch3_l12_don_cu_bat_nguon_moi.down.sql
-- ============================================================================
create table if not exists public.quiz_ch3_l12_bank_backup_20261021 (
  id bigint, archived boolean, note text, backed_up_at timestamptz default now()
);
create table if not exists public.quiz_ch3_l12_sources_backup_20261021 (
  season_id bigint, source_kind text, source_id bigint, max_rp int, backed_up_at timestamptz default now()
);
alter table public.quiz_ch3_l12_bank_backup_20261021 enable row level security;
alter table public.quiz_ch3_l12_sources_backup_20261021 enable row level security;
revoke all on public.quiz_ch3_l12_bank_backup_20261021 from anon, authenticated;
revoke all on public.quiz_ch3_l12_sources_backup_20261021 from anon, authenticated;

do $$
declare
  v_n int; v_old int[] := array[759,760,761,762,768,769,770,937]; s public.rank_seasons%rowtype;
begin
  select count(*) into v_n from public.exams where id between 1055 and 1062;
  if v_n <> 8 then raise exception 'Cần đủ 8 đề mới #1055–#1062, thấy %', v_n; end if;

  -- 1) archive câu cũ
  insert into public.quiz_ch3_l12_bank_backup_20261021 (id, archived, note)
    select id, archived, note from public.question_bank where source_exam_id = any (v_old) and not archived;
  update public.question_bank
     set archived = true,
         note = coalesce(note || ' · ', '') || 'Quiz Ch.3 L12 soạn lại 21/10/2026 (đề cũ có câu ngoài chương trình)'
   where source_exam_id = any (v_old) and not archived;
  get diagnostics v_n = row_count;
  raise notice 'Ẩn % câu cũ khỏi ngân hàng', v_n;

  -- 2) bật nguồn RP cho đề mới
  for s in select * from public.rank_seasons where status = 'active' and 18 = any (class_ids) loop
    with ins as (
      insert into public.rank_sources (season_id, source_kind, source_id, max_rp, enabled)
      select s.id, 'exam', e.id, 10, true from public.exams e
       where e.id between 1055 and 1062
         and not exists (select 1 from public.rank_sources rs where rs.season_id = s.id and rs.source_kind = 'exam' and rs.source_id = e.id)
      returning source_kind, source_id, max_rp
    )
    insert into public.quiz_ch3_l12_sources_backup_20261021 (season_id, source_kind, source_id, max_rp)
      select s.id, source_kind, source_id, max_rp from ins;
    get diagnostics v_n = row_count;
    raise notice 'Mùa %: bật % đề mới (10 RP)', s.id, v_n;
  end loop;

  -- 3) thông báo cho em đã làm đề cũ
  with map(exam_id, lesson_id) as (values (759,10),(760,11),(937,12),(761,13),(762,14),(768,125),(769,126),(770,127)),
  did as (
    select er.student_id, l.id as lesson_id, l.title, l.chapter_id, l.sort_order
      from public.exam_results er
      join map on map.exam_id = er.exam_id
      join public.lessons l on l.id = map.lesson_id
     group by er.student_id, l.id, l.title, l.chapter_id, l.sort_order
  ), per as (
    select student_id,
           string_agg(title, '; ' order by sort_order) as titles,
           (array_agg(lesson_id order by sort_order))[1] as first_lesson,
           (array_agg(chapter_id order by sort_order))[1] as first_chapter
      from did group by student_id
  )
  select count(*) into v_n from (
    select public.notify_user(
      p.student_id, 'quiz_updated',
      'Kiểm tra nhanh Chương 3 đã được cập nhật',
      'Bộ câu Kiểm tra nhanh của ' || p.titles || ' vừa được soạn lại sát đề thi tốt nghiệp, có giải thích vì sao từng phương án sai. '
        || 'Điểm thăng hạng em đã có được giữ nguyên, không trừ. Em làm lại bộ mới nhé: làm đúng sẽ được cộng thêm điểm thăng hạng.',
      '/lop-hoc/bai?id=' || p.first_lesson || '&chapter=' || p.first_chapter)
    from per p
    where not exists (select 1 from public.notifications n where n.user_id = p.student_id and n.kind = 'quiz_updated'
                      and n.created_at > now() - interval '1 day')
  ) t;
  raise notice 'Gửi % thông báo', v_n;
end $$;
