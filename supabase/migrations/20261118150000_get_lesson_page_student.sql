-- ============================================================================
-- RPC gộp trang bài học /lop-hoc/bai cho học sinh đã đăng nhập (18/11/2026).
-- Thay 7 round-trip mỗi lượt tải (fetchExamMetas, fetchRawProgressBatch ×5, get_lesson_mastery) bằng 1 lần gọi.
-- Chỉ THÊM một hàm mới, không đổi bảng/policy/dữ liệu → chạy lúc nào cũng được (client cũ không gọi hàm này).
--
-- SECURITY INVOKER: RLS hiện có của exams / lesson_items / lesson_progress / exam_results / exam_result_scores
-- (view security_invoker) / exam_attempts / practice_sessions tự áp như các truy vấn client cũ. Hàm còn lọc thêm
-- user_id/student_id = auth.uid(), nên kể cả admin/TA/phụ huynh (RLS cho đọc dòng người khác) cũng chỉ nhận dòng
-- CỦA CHÍNH MÌNH ở progress/results/open_attempts/practice. Riêng "exams" phụ thuộc RLS theo vai:
--   HS: đề published VÀ (không gán lớp hoặc gán lớp HS đang active, hoặc đề CNC)
--   TA: như HS + đề đã gửi xem trước cho lớp mình trợ giảng (exam_ta_previews), kể cả chưa published
--   admin: mọi đề trong E
-- Cột exams đọc được theo grant cột (20261111200000): id, title, duration_minutes, question_count, type_counts,
-- pass_score, published — đều có grant; KHÔNG đụng exams.questions.
--
-- Chưa đăng nhập: anon không có quyền EXECUTE (permission denied 42501); authenticated mà auth.uid() null
-- (JWT hỏng) → raise 42501 'not_authenticated'. Client chỉ gọi khi đã có phiên.
--
-- E = mọi phần tử của lesson_items.exam_ids (bigint[]) của mọi mục bài p_lesson (KHÔNG lọc published_at/kind —
-- client tự lọc như cũ). Item luyện tập = lesson_items.kind (text) = 'luyen_tap'.
--
-- Index phục vụ (theo migration, DATABASE.md không liệt kê index):
--   lesson_items_lesson_idx (lesson_id, sort_order) · exams PK · lesson_progress PK (user_id, item_id)
--   idx_exam_results_student_exam_created (student_id, exam_id, created_at desc)
--   exam_question_results PK (exam_result_id, question_index) cho view exam_result_scores
--   idx_exam_attempts_student_exam_open (student_id, exam_id, started_at desc) where submitted_at is null
--   practice_sessions_student_idx (student_id, created_at desc) — item_id lọc trên heap; mỗi HS vài chục dòng, đủ.
--
-- Rollback: perf/rollback/20261118150000_get_lesson_page_student.down.sql
-- ============================================================================
begin;

create or replace function public.get_lesson_page_student(p_lesson bigint)
returns jsonb
language plpgsql
stable
security invoker
set search_path = public
as $$
declare
  v_uid uuid := (select auth.uid());
  v_item_ids bigint[];
  v_practice_ids bigint[];
  v_exam_ids bigint[];
  v_exams jsonb;
  v_progress jsonb;
  v_results jsonb;
  v_open jsonb;
  v_practice jsonb;
  v_mastery jsonb;
begin
  if v_uid is null then
    raise exception 'not_authenticated' using errcode = '42501';
  end if;

  select coalesce(array_agg(li.id), '{}'::bigint[]),
         coalesce(array_agg(li.id) filter (where li.kind = 'luyen_tap'), '{}'::bigint[])
    into v_item_ids, v_practice_ids
    from public.lesson_items li
   where li.lesson_id = p_lesson;

  select coalesce(array_agg(distinct x.eid), '{}'::bigint[])
    into v_exam_ids
    from public.lesson_items li
   cross join lateral unnest(li.exam_ids) as x(eid)
   where li.lesson_id = p_lesson
     and x.eid is not null;

  -- 1+2. Đề (mọi đề trong E mà người gọi đọc được theo RLS), kèm cờ published để client tự lọc.
  select coalesce(jsonb_agg(jsonb_build_object(
           'id', e.id,
           'title', e.title,
           'duration_minutes', e.duration_minutes,
           'question_count', e.question_count,
           'type_counts', e.type_counts,
           'pass_score', e.pass_score,
           'published', e.published
         ) order by e.id), '[]'::jsonb)
    into v_exams
    from public.exams e
   where e.id = any(v_exam_ids);

  -- 3. Tiến độ mục bài.
  select coalesce(jsonb_agg(jsonb_build_object('item_id', lp.item_id, 'done_at', lp.done_at)
                            order by lp.item_id), '[]'::jsonb)
    into v_progress
    from public.lesson_progress lp
   where lp.user_id = v_uid
     and lp.item_id = any(v_item_ids);

  -- 4. Kết quả đã nộp + điểm cuối (có tự luận đã chấm). Chỉ trả correctCount, không trả cả detail.
  select coalesce(jsonb_agg(jsonb_build_object(
           'id', r.id,
           'exam_id', r.exam_id,
           'created_at', r.created_at,
           'score', r.score,
           'correct_count', case when jsonb_typeof(r.detail -> 'correctCount') = 'number'
                                 then trunc((r.detail ->> 'correctCount')::numeric)::int end,
           'final_score10', s.final_score10,
           'pending_essay_count', s.pending_essay_count
         ) order by r.created_at, r.id), '[]'::jsonb)
    into v_results
    from public.exam_results r
    left join lateral (
      select ers.final_score10, ers.pending_essay_count
        from public.exam_result_scores ers
       where ers.exam_result_id = r.id
    ) s on true
   where r.student_id = v_uid
     and r.exam_id = any(v_exam_ids);

  -- 5. Đề đang làm dở (chưa nộp).
  select coalesce(jsonb_agg(o.exam_id order by o.exam_id), '[]'::jsonb)
    into v_open
    from (
      select distinct a.exam_id
        from public.exam_attempts a
       where a.student_id = v_uid
         and a.exam_id = any(v_exam_ids)
         and a.submitted_at is null
    ) o;

  -- 6. Lượt luyện tập của các mục luyen_tap.
  select coalesce(jsonb_agg(jsonb_build_object('item_id', ps.item_id, 'score', ps.score, 'created_at', ps.created_at)
                            order by ps.created_at, ps.id), '[]'::jsonb)
    into v_practice
    from public.practice_sessions ps
   where ps.student_id = v_uid
     and ps.item_id = any(v_practice_ids);

  -- 7. Mastery — lỗi thì trả null, không làm hỏng cả trang.
  begin
    select coalesce(jsonb_agg(to_jsonb(m) - 'ord' order by m.ord), '[]'::jsonb)
      into v_mastery
      from public.get_lesson_mastery(p_lesson) with ordinality
           as m(topic_id, topic_name, sort_order, answered_count, level, pct, is_summary, ord);
  exception when others then
    v_mastery := null;
  end;

  return jsonb_build_object(
    'v', 1,
    'exams', v_exams,
    'progress', v_progress,
    'results', v_results,
    'open_attempts', v_open,
    'practice', v_practice,
    'mastery', v_mastery
  );
end;
$$;

revoke all on function public.get_lesson_page_student(bigint) from public, anon;
grant execute on function public.get_lesson_page_student(bigint) to authenticated;

commit;

-- ----------------------------------------------------------------------------
-- KIỂM THỬ (chạy tay trong giao dịch, thay <...>; luôn rollback):
--
-- HS (kỳ vọng: exams chỉ đề published + đúng lớp; progress/results/... chỉ của HS này):
--   begin;
--   set local role authenticated;
--   select set_config('request.jwt.claims', json_build_object('sub','<uuid_hs>','role','authenticated')::text, true);
--   select public.get_lesson_page_student(<lesson_id>);
--   -- đối chiếu với truy vấn cũ cùng vai:
--   select count(*) from public.exam_results r
--    where r.student_id = '<uuid_hs>'
--      and r.exam_id in (select unnest(exam_ids) from public.lesson_items where lesson_id = <lesson_id>);
--   rollback;
--
-- Trợ giảng (kỳ vọng: exams thêm đề đã gửi xem trước dù chưa published; results… chỉ của chính TA, thường []):
--   begin; set local role authenticated;
--   select set_config('request.jwt.claims', json_build_object('sub','<uuid_ta>','role','authenticated')::text, true);
--   select jsonb_array_length(x->'exams'), jsonb_array_length(x->'results')
--     from (select public.get_lesson_page_student(<lesson_id>) x) t;
--   rollback;
--
-- Admin (kỳ vọng: exams = mọi đề trong E kể cả published=false; results… chỉ của admin):
--   begin; set local role authenticated;
--   select set_config('request.jwt.claims', json_build_object('sub','<uuid_admin>','role','authenticated')::text, true);
--   select x->'exams' from (select public.get_lesson_page_student(<lesson_id>) x) t;
--   rollback;
--
-- Khách (kỳ vọng: ERROR 42501 permission denied for function):
--   begin; set local role anon; select public.get_lesson_page_student(<lesson_id>); rollback;
--
-- ROLLBACK (= perf/rollback/20261118150000_get_lesson_page_student.down.sql):
--   drop function if exists public.get_lesson_page_student(bigint);
