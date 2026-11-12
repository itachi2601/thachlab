-- ============================================================================
-- Quiz trắc nghiệm CNC chấm ở server — BƯỚC 1/2: thêm hàm cnc_quiz_submit.
-- Trước đây máy học sinh tự chấm rồi gửi "điểm/tổng" lên record_cnc_learning_result → gửi thẳng 20/20 là đạt.
-- Hàm mới nhận BÀI LÀM (chỉ số câu → phương án), tự tra ngân hàng đúng với (bài, bài kiểm), chấm và ghi
-- cnc_learning_records. Ngưỡng đạt giữ như giao diện: kiểm tra cuối bài + bài tập 1, 2: 80%; vận hành máy, cài đặt dao: 100%.
-- Chạy TRƯỚC khi deploy client. Lúc nào cũng được: chỉ thêm 2 hàm.
-- Bước 2 (20261112100000): record_cnc_learning_result thôi nhận điểm/đạt của các bài này — chạy sau deploy, khi tab cũ đã tải lại.
-- Ngoài phạm vi: bài tự luận/điền khuyết/viết chương trình/checklist (đáp án nằm trong mã client) vẫn chấm ở máy.
--
-- Rollback: perf/rollback/20261112090000_cnc_quiz_cham_server_buoc_1.down.sql
-- ============================================================================
begin;

-- (bài, bài kiểm) → ngân hàng (exams.cnc_key) + tỉ lệ đạt. Khớp CNC_FINAL_TEST_BANK, ProgrammingTestSuite, OperationTestSuite.
create or replace function public.cnc_quiz_bank_of(p_lesson_id text, p_assessment_id text)
returns table (cnc_key text, pass_ratio numeric)
language sql immutable set search_path = public
as $$
  select m.cnc_key, m.pass_ratio
  from (values
    ('lesson-1',      'final',             'lesson-1',        0.8),
    ('lesson-2',      'final',             'test-2',          0.8),
    ('lesson-3',      'final',             'test-3',          0.8),
    ('lesson-4-turn', 'final',             'test-4-turn',     0.8),
    ('lesson-4-mill', 'final',             'test-4-mill',     0.8),
    ('lesson-5',      'final',             'test-5',          0.8),
    ('lesson-6',      'final',             'test-6',          0.8),
    ('lesson-2',      'exercise-1',        'lesson-2',        0.8),
    ('lesson-3',      'exercise-1',        'lesson-3',        0.8),
    ('lesson-2',      'exercise-2',        'turn-translate',  0.8),
    ('lesson-3',      'exercise-2',        'mill-translate',  0.8),
    ('lesson-4-turn', 'machine-operation', 'operation-turn',  1.0),
    ('lesson-4-mill', 'machine-operation', 'operation-mill',  1.0),
    ('lesson-4-turn', 'tool-setup',        'tool-setup-turn', 1.0),
    ('lesson-4-mill', 'tool-setup',        'tool-setup-mill', 1.0)
  ) as m(lesson_id, assessment_id, cnc_key, pass_ratio)
  where m.lesson_id = p_lesson_id and m.assessment_id = p_assessment_id;
$$;
revoke all on function public.cnc_quiz_bank_of(text, text) from public, anon, authenticated;

-- p_answers: {"<thứ tự câu trắc nghiệm trong ngân hàng, từ 0>": <chỉ số phương án, từ 0>}.
create or replace function public.cnc_quiz_submit(p_course_id bigint, p_lesson_id text, p_assessment_id text, p_answers jsonb)
returns table (score integer, total integer, passed boolean)
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_key text;
  v_ratio numeric;
  v_questions jsonb;
  v_score integer;
  v_total integer;
  v_pass boolean;
begin
  if v_uid is null then raise exception 'Bạn cần đăng nhập.' using errcode = '42501'; end if;
  if not exists (
    select 1 from public.course_enrollments ce
    where ce.course_id = p_course_id and ce.student_id = v_uid and ce.status = 'active'
  ) then raise exception 'Bạn chưa được duyệt vào khóa học này.' using errcode = '42501'; end if;

  select b.cnc_key, b.pass_ratio into v_key, v_ratio from public.cnc_quiz_bank_of(p_lesson_id, p_assessment_id) b;
  if v_key is null then
    raise exception 'Bài kiểm tra này không chấm trắc nghiệm ở máy chủ.' using errcode = '22023';
  end if;
  if jsonb_typeof(p_answers) is distinct from 'object' or octet_length(p_answers::text) > 20000 then
    raise exception 'Bài làm không hợp lệ.' using errcode = '22023';
  end if;

  select e.questions into v_questions from public.exams e
  where e.cnc_key = v_key and e.published and jsonb_typeof(e.questions) = 'array';
  if v_questions is null then
    raise exception 'Chưa có ngân hàng câu hỏi cho bài này.' using errcode = '22023';
  end if;

  -- Cùng thứ tự với client: chỉ lấy câu multiple_choice, đánh số lại từ 0.
  select count(*)::int,
         count(*) filter (where p_answers ->> (mc.idx - 1)::text = mc.q ->> 'answer')::int
    into v_total, v_score
  from (
    select q, row_number() over (order by ord) as idx
    from jsonb_array_elements(v_questions) with ordinality as t(q, ord)
    where q ->> 'type' = 'multiple_choice'
  ) mc;
  if v_total = 0 then
    raise exception 'Chưa có ngân hàng câu hỏi cho bài này.' using errcode = '22023';
  end if;
  v_pass := v_score >= ceil(v_total * v_ratio);

  insert into public.cnc_learning_records (
    course_id, student_id, lesson_id, assessment_id, completed, latest_score, best_score,
    total_questions, attempt_count, last_activity_at
  ) values (
    p_course_id, v_uid, p_lesson_id, p_assessment_id, v_pass, v_score, v_score, v_total, 1, now()
  )
  on conflict (course_id, student_id, lesson_id, assessment_id) do update set
    completed = cnc_learning_records.completed or excluded.completed,
    latest_score = excluded.latest_score,
    best_score = greatest(coalesce(cnc_learning_records.best_score, 0), excluded.best_score),
    total_questions = excluded.total_questions,
    attempt_count = cnc_learning_records.attempt_count + 1,
    last_activity_at = now();

  return query select v_score, v_total, v_pass;
end;
$$;
revoke all on function public.cnc_quiz_submit(bigint, text, text, jsonb) from public, anon;
grant execute on function public.cnc_quiz_submit(bigint, text, text, jsonb) to authenticated;

commit;
