-- ============================================================================
-- Chặng 0 (mở cả kho) — chỉ giữ lại câu từ đề KIỂM TRA THẬT, không tính đề thi thử gắn mục Kiểm tra (24/10/2026)
-- Sau 20261024210000 kho L12 Bài 1 vẫn chỉ ~118 câu cho em mới: exam_is_assessment coi mọi đề trong mục `kiem_tra` của bài là
-- đề đánh giá, nên ~500/661 câu (đề thi thử công khai) nằm sau cổng 3 lượt/đạt điểm. Thầy chốt 24/10/2026: kho chỉ lọc theo
-- nguồn là đề kiểm tra thật.
--   bank_source_is_assessment(đề) = đề đã giao làm bài thật: class_assessments · class_announcements · ta_homework_assignments ·
--   class_review_homework · mục `bai_tap_ve_nha` của bài. KHÔNG tính mục `kiem_tra` (thi thử trong bài; cả "Kiểm tra chương/
--   giữa kỳ/cuối kỳ" của bài kiểm tra).
-- Đề kiểm tra thật vẫn theo quy tắc P0 #1: câu của nó vào kho khi em đã được xem đáp án (exam_answers_revealed). Staff không bị lọc.
-- Lưu ý đo trước (24/10/2026, 996 đề nguồn): 425 đề thuộc bài "Kiểm tra chương/HK", 321 thuộc mục Kiểm tra của bài thường,
-- chỉ 5 BTVN + 2 class_assessments + 7 ta_homework + 2 review_homework là đề thật. Nếu thầy muốn giữ cổng cho đề "Kiểm tra chương/HK"
-- thì thêm nhánh vào bank_source_is_assessment (join lessons.title ilike 'Kiểm tra%') — chỉ sửa 1 hàm này.
-- Chỉ thay thân hàm + 1 hàm nội bộ mới, không đụng dữ liệu → chạy giờ nào cũng được.
-- Rollback: chạy lại phần hàm của 20261024210000_lesson_practice_pool_noi_loc_de_danh_gia.sql (create or replace bản cũ);
--   drop function if exists public.bank_source_is_assessment(bigint);
-- Sau khi chạy: mô phỏng em mới gọi lesson_practice_pool(2, 100): kỳ vọng ~600+ câu (trước 118); không lộ khoá đáp án;
--   câu nguồn là đề giao thật mà em chưa mở đáp án bị check_bank_practice_answer từ chối.
-- ============================================================================

begin;

create or replace function public.bank_source_is_assessment(p_exam bigint)
returns boolean
language sql stable security definer set search_path = public
as $$
  select exists (select 1 from public.class_assessments ca where ca.exam_id = p_exam)
      or exists (select 1 from public.class_announcements an where an.exam_id = p_exam)
      or exists (select 1 from public.ta_homework_assignments ta where ta.exam_id = p_exam)
      or exists (select 1 from public.class_review_homework rh where rh.exam_id = p_exam)
      or exists (select 1 from public.lesson_items li where li.kind = 'bai_tap_ve_nha' and p_exam = any (li.exam_ids));
$$;
revoke all on function public.bank_source_is_assessment(bigint) from public, anon, authenticated;

-- ---------- Kho câu của bài (lược đáp án) ----------
create or replace function public.lesson_practice_pool(p_lesson_id bigint, p_per_level int default 40)
returns jsonb
language plpgsql volatile security definer set search_path = public
as $$
declare
  v_uid uuid := (select auth.uid());
  v_per int := least(greatest(coalesce(p_per_level, 40), 5), 100);
  v_own bigint[];
  v_items jsonb;
begin
  if v_uid is null then raise exception 'Cần đăng nhập' using errcode = '42501'; end if;
  if not public.bank_practice_lesson_ok(p_lesson_id, v_uid) then
    raise exception 'Không tìm thấy bài này' using errcode = 'P0002';
  end if;

  select coalesce(array_agg(distinct x), '{}') into v_own
  from public.lesson_items li, unnest(li.exam_ids) as x
  where li.lesson_id = p_lesson_id and li.kind = 'luyen_tap';

  with src as (
    select distinct b.source_exam_id as id
    from public.question_bank b
    join public.question_topics t on t.id = b.topic_id
    where t.lesson_id = p_lesson_id and b.source_exam_id is not null
  ), bad_src as (
    -- Đề kiểm tra THẬT mà em CHƯA đủ điều kiện xem đáp án (chưa đủ 3 lượt, chưa đạt điểm) thì câu của đề đó chưa vào kho.
    select s.id from src s
    where not public.is_staff() and public.bank_source_is_assessment(s.id) and not public.exam_answers_revealed(s.id, v_uid)
  ), cand as (
    select b.id, b.topic_id, t.name as topic_name, b.form, b.difficulty, b.question,
           row_number() over (partition by coalesce(b.difficulty, '') order by random()) as rn
    from public.question_bank b
    join public.question_topics t on t.id = b.topic_id
    where t.lesson_id = p_lesson_id
      and not b.archived
      and coalesce(cardinality(b.lint_flags), 0) = 0
      and coalesce(b.qtype, b.question ->> 'type') in ('multiple_choice', 'true_false', 'short_answer')
      and b.question ->> 'type' in ('multiple_choice', 'true_false', 'short_answer')
      and jsonb_typeof(b.question) = 'object'
      and (b.source_exam_id is null
           or (not (b.source_exam_id = any (v_own)) and b.source_exam_id not in (select id from bad_src)))
  )
  select coalesce(jsonb_agg(jsonb_build_object(
           'bank_id', c.id, 'topic_id', c.topic_id, 'topic_name', c.topic_name,
           'form', c.form, 'difficulty', coalesce(c.difficulty, ''),
           'question', jsonb_set(public.exam_q_public(c.question), '{difficulty}', to_jsonb(coalesce(c.difficulty, '')))
         ) order by random()), '[]'::jsonb)
  into v_items
  from cand c where c.rn <= v_per;

  return jsonb_build_object('lesson_id', p_lesson_id, 'per_level', v_per, 'items', v_items);
end;
$$;
revoke all on function public.lesson_practice_pool(bigint, int) from public, anon;
grant execute on function public.lesson_practice_pool(bigint, int) to authenticated;

-- ---------- Chấm 1 câu ngân hàng ----------
create or replace function public.check_bank_practice_answer(p_bank_id bigint, p_response jsonb)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_uid uuid := (select auth.uid());
  b public.question_bank%rowtype;
  v_lesson bigint;
  g record;
begin
  if v_uid is null then raise exception 'Cần đăng nhập' using errcode = '42501'; end if;
  select * into b from public.question_bank where id = p_bank_id;
  if not found then raise exception 'Không tìm thấy câu này' using errcode = 'P0002'; end if;
  select t.lesson_id into v_lesson from public.question_topics t where t.id = b.topic_id;
  if b.archived or v_lesson is null
     or coalesce(cardinality(b.lint_flags), 0) > 0
     or b.question ->> 'type' not in ('multiple_choice', 'true_false', 'short_answer')
     or not public.bank_practice_lesson_ok(v_lesson, v_uid)
     or (b.source_exam_id is not null and not public.is_staff()
         and public.bank_source_is_assessment(b.source_exam_id)
         and not public.exam_answers_revealed(b.source_exam_id, v_uid)) then
    raise exception 'Không tìm thấy câu này' using errcode = 'P0002';
  end if;
  if p_response is null or p_response = 'null'::jsonb then
    raise exception 'Cần chọn đáp án trước khi xem đáp án' using errcode = '22023';
  end if;
  select * into g from public.exam_grade_question(b.question, p_response);
  return jsonb_build_object('bank_id', b.id,
    'earned', g.earned, 'max', g.max_pts, 'is_correct', g.max_pts > 0 and g.earned = g.max_pts,
    'question', b.question);
end;
$$;
revoke all on function public.check_bank_practice_answer(bigint, jsonb) from public, anon;
grant execute on function public.check_bank_practice_answer(bigint, jsonb) to authenticated;

commit;
