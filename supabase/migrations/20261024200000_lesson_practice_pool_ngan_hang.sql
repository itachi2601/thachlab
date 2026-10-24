-- ============================================================================
-- Chặng 0 — nối ngân hàng câu hỏi vào phần Luyện tập của bài (24/10/2026)
-- Báo cáo: docs/BAO-CAO-NGAN-HANG-THEO-BAI-2026-10-24.md. Hiện Luyện tập chỉ lấy câu từ các đề gắn mục `luyen_tap`
-- (mỗi bài ~1 đề); ~88% ngân hàng gắn chủ đề của bài nằm ngoài tầm HS.
--
-- Hàm mới (RPC cho authenticated), CHỈ THÊM — không đụng hàm/bảng cũ ngoài 1 cột nullable:
--   lesson_practice_pool(p_lesson_id, p_per_level)  → jsonb  kho câu ngân hàng của bài, ĐÃ LƯỢC đáp án, bốc ngẫu nhiên
--                                                     tối đa p_per_level câu mỗi mức (de / trung-binh / kho / chưa nhãn)
--   check_bank_practice_answer(p_bank_id, p_response) → jsonb  chấm 1 câu ngân hàng, trả đáp án + lời giải (cùng dạng
--                                                     check_practice_answer, thêm bank_id thay exam_id/question_index)
--   practice_question_results.bank_id (nullable)     → vết câu ngân hàng đã làm (exam_id để null ⇒ trigger sổ tay câu
--                                                     sai bỏ qua, đúng ý: câu ngân hàng chưa có chỗ trong student_mistakes)
-- Hàm nội bộ (không cấp cho authenticated): bank_practice_lesson_ok.
--
-- Quy tắc lọc kho (cùng tinh thần P0 #1, 24/10/2026):
--   * Chỉ mở nếu HS mở được ít nhất một đề luyện tập của bài (exam_open_to_student) hoặc là staff — bài lớp riêng
--     (avcn…) không lộ ngân hàng cho người ngoài lớp.
--   * Bài thuộc chương giới hạn lớp (chapter_classes) chỉ mở cho HS thuộc lớp đó.
--   * Bỏ câu archived, câu có lint_flags, dạng essay, câu có nguồn là đề đánh giá (exam_is_assessment) — tránh moi
--     đáp án đề kiểm tra/BTVN qua cửa sau; bỏ câu đã nằm trong đề luyện tập của chính bài (không trùng pool cũ).
--   * Đáp án/lời giải chỉ ra sau khi trả lời qua check_bank_practice_answer; response null bị từ chối.
-- Chưa lọc được: câu "_can_xac_nhan" (127 câu chờ thầy duyệt) vì DB không có cờ — danh sách ở
--   scripts/data/bank-answer-fixes.json; nên gắn lint_flags cho chúng trước khi client bật kho (xem docs báo cáo, chặng 3).
--
-- Nặng không: chỉ tạo hàm + 1 cột nullable → chạy giờ nào cũng được. Hàm đọc question_bank theo topic_id (đã có
-- chỉ mục topic) mỗi lần mở phiên luyện, ~300–1.100 dòng/bài; client nên gọi 1 lần/phiên.
-- Rollback: khối ROLLBACK cuối file.
-- Sau khi chạy: kiểm thử tay trong SQL editor bằng role HS:
--   select jsonb_array_length(public.lesson_practice_pool(2) -> 'items');   -- ≤ (số mức difficulty khác nhau) * p_per_level
--   (câu ngân hàng có hình: đối chiếu 1 câu — exam_q_public là danh sách trắng, khoá hình lạ sẽ bị cắt)
-- ============================================================================

begin;

alter table public.practice_question_results add column if not exists bank_id bigint;
comment on column public.practice_question_results.bank_id is
  'Câu ngân hàng (question_bank.id) khi câu luyện tập lấy từ lesson_practice_pool; null với câu lấy từ đề.';

-- ---------- Cổng vào: HS/staff có được luyện bài này không ----------
create or replace function public.bank_practice_lesson_ok(p_lesson_id bigint, p_uid uuid)
returns boolean
language sql stable security definer set search_path = public
as $$
  select p_uid is not null
    and exists (select 1 from public.lessons l where l.id = p_lesson_id and (l.published or public.is_staff()))
    and (public.is_staff()
         or (-- chương giới hạn theo lớp (chapter_classes) thì HS phải thuộc một lớp đó; không giới hạn thì mở
             (not exists (select 1 from public.lessons l join public.chapter_classes cc on cc.chapter_id = l.chapter_id
                          where l.id = p_lesson_id)
              or exists (select 1 from public.lessons l
                         join public.chapter_classes cc on cc.chapter_id = l.chapter_id
                         join public.user_classes uc on uc.class_id = cc.class_id
                         where l.id = p_lesson_id and uc.user_id = p_uid and uc.status = 'active'))
             and exists (select 1
                    from public.lesson_items li
                    join public.exams e on e.id = any (li.exam_ids)
                    where li.lesson_id = p_lesson_id and li.kind = 'luyen_tap'
                      and e.published and public.exam_open_to_student(e.id, p_uid))))
$$;
revoke all on function public.bank_practice_lesson_ok(bigint, uuid) from public, anon, authenticated;

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
    select s.id from src s where public.exam_is_assessment(s.id)
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
     or (b.source_exam_id is not null and public.exam_is_assessment(b.source_exam_id)) then
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

-- ============================================================================
-- ROLLBACK (chưa có client nào gọi thì an toàn bỏ ngay):
--   begin;
--   drop function if exists public.check_bank_practice_answer(bigint, jsonb);
--   drop function if exists public.lesson_practice_pool(bigint, int);
--   drop function if exists public.bank_practice_lesson_ok(bigint, uuid);
--   alter table public.practice_question_results drop column if exists bank_id;
--   commit;
-- ============================================================================
