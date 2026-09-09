-- ============================================================
-- Migration: Phân tích kết quả kiểm tra + Cảnh báo phụ đạo
-- Thiết kế: scratchpad/design/phan-tich-canh-bao.html
-- Chạy SAU: supabase-schema.sql, supabase-migration-classes.sql,
--           supabase-migration-class-instructors.sql,
--           supabase-migration-thpt-instructor-access.sql,
--           supabase-migration-lessons-periodic-exam.sql
-- Idempotent — chạy lại được.
-- ============================================================

-- ---------- Helper: người dùng hiện tại có được xem học sinh này không ----------
-- true nếu là admin, hoặc là giảng viên được phân công một lớp mà học sinh đang học.
create or replace function public.teaches_student(p_student uuid)
returns boolean
language sql security definer stable set search_path = public
as $$
  select public.is_admin() or exists (
    select 1
    from public.user_classes uc
    join public.class_instructors ci on ci.class_id = uc.class_id
    where uc.user_id = p_student and ci.instructor_id = auth.uid()
  );
$$;

-- true nếu là admin hoặc giảng viên THPT được phân công lớp này.
create or replace function public.manages_class(p_class bigint)
returns boolean
language sql security definer stable set search_path = public
as $$
  select public.is_admin() or exists (
    select 1 from public.class_instructors ci
    where ci.class_id = p_class and ci.instructor_id = auth.uid()
  );
$$;


-- ============================================================
-- 1. Danh mục chủ đề câu hỏi (chuẩn hoá — không gõ tự do)
-- ============================================================
create table if not exists public.question_topics (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  subject_code text not null default 'vat-ly',
  grade text not null,                       -- '10' | '11' | '12' | '9'
  chapter_id bigint references public.chapters (id) on delete set null,
  lesson_id bigint references public.lessons (id) on delete set null,  -- nút "Ôn lại" nhảy vào đây
  name text not null,
  sort_order int not null default 0,
  unique (subject_code, grade, name)
);
create index if not exists question_topics_grade_idx
  on public.question_topics (subject_code, grade, sort_order);

alter table public.question_topics enable row level security;
drop policy if exists "anyone reads question topics" on public.question_topics;
create policy "anyone reads question topics" on public.question_topics
  for select using (true);
-- Cả admin lẫn giảng viên THPT được thêm/sửa chủ đề.
drop policy if exists "staff manage question topics" on public.question_topics;
create policy "staff manage question topics" on public.question_topics
  for all to authenticated
  using (public.is_admin() or exists (
    select 1 from public.profiles p
    where p.id = auth.uid() and p.role = 'instructor' and p.admin_area = 'thpt'
  ))
  with check (public.is_admin() or exists (
    select 1 from public.profiles p
    where p.id = auth.uid() and p.role = 'instructor' and p.admin_area = 'thpt'
  ));

-- Nhãn trên từng câu hỏi nằm trong exams.questions[i] (jsonb) — KHÔNG cần cột:
--   "topic_id": <question_topics.id>,  "form": "ly_thuyet" | "bai_tap"
-- Skill up-de-kiem-tra gắn khi nhập đề; ExamEditor cho sửa tay.


-- ============================================================
-- 2. Kết quả từng câu — chốt tại thời điểm nộp bài (ảnh chụp)
-- ============================================================
create table if not exists public.exam_question_results (
  exam_result_id bigint not null references public.exam_results (id) on delete cascade,
  question_index int not null,
  student_id uuid not null references public.profiles (id) on delete cascade,
  exam_id bigint not null references public.exams (id) on delete cascade,
  topic_id bigint references public.question_topics (id) on delete set null,
  topic_name text not null default '',
  form text not null default '',              -- 'ly_thuyet' | 'bai_tap' | ''
  qtype text not null,
  earned numeric(4,2) not null default 0,
  max numeric(4,2) not null default 0,
  is_correct boolean not null default false,
  estimated boolean not null default false,   -- true = suy ngược từ detail cũ khi backfill
  created_at timestamptz not null default now(),
  primary key (exam_result_id, question_index)
);
create index if not exists eqr_topic_idx on public.exam_question_results (topic_id);
create index if not exists eqr_student_exam_idx on public.exam_question_results (student_id, exam_id);
create index if not exists eqr_exam_correct_idx on public.exam_question_results (exam_id, is_correct);

alter table public.exam_question_results enable row level security;

drop policy if exists "student reads own question results" on public.exam_question_results;
create policy "student reads own question results" on public.exam_question_results
  for select to authenticated
  using (student_id = auth.uid() or public.teaches_student(student_id));

drop policy if exists "student inserts own question results" on public.exam_question_results;
create policy "student inserts own question results" on public.exam_question_results
  for insert to authenticated
  with check (student_id = auth.uid());

drop policy if exists "admin manages question results" on public.exam_question_results;
create policy "admin manages question results" on public.exam_question_results
  for all to authenticated using (public.is_admin()) with check (public.is_admin());


-- ============================================================
-- 3. Bài kiểm tra định kỳ của lớp — xác định "liên tiếp"
-- ============================================================
create table if not exists public.class_assessments (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  class_id bigint not null references public.classes (id) on delete cascade,
  exam_id bigint not null references public.exams (id) on delete cascade,
  lesson_id bigint references public.lessons (id) on delete set null,
  kind text not null default 'thuong_xuyen'
    check (kind in ('giua_ki', 'cuoi_ki', 'thuong_xuyen', 'chuong')),
  term text not null default '',              -- 'HK1' | 'HK2' | '2025-2026'
  sequence int,                                -- thứ tự trong (class, term); null = xếp theo published_at
  weight numeric(4,2) not null default 1,
  published_at timestamptz not null default now(),
  unique (class_id, exam_id)
);
create index if not exists class_assessments_class_idx
  on public.class_assessments (class_id, term, sequence, published_at);

alter table public.class_assessments enable row level security;
drop policy if exists "anyone reads class assessments" on public.class_assessments;
create policy "anyone reads class assessments" on public.class_assessments
  for select to authenticated using (true);
drop policy if exists "staff manage class assessments" on public.class_assessments;
create policy "staff manage class assessments" on public.class_assessments
  for all to authenticated
  using (public.manages_class(class_id)) with check (public.manages_class(class_id));


-- ============================================================
-- 4. Cảnh báo phụ đạo
-- ============================================================
create table if not exists public.student_alerts (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.profiles (id) on delete cascade,
  class_id bigint references public.classes (id) on delete set null,
  kind text not null check (kind in ('low_score_streak', 'missed_assessment')),
  severity text not null default 'warning' check (severity in ('warning', 'urgent')),
  reason text not null default '',
  assessment_ids bigint[] not null default '{}',
  status text not null default 'open'
    check (status in ('open', 'contacted', 'tutoring', 'resolved', 'dismissed')),
  assigned_to uuid references public.profiles (id) on delete set null,
  handled_by uuid references public.profiles (id) on delete set null,
  handled_note text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (student_id, kind)
);
create index if not exists student_alerts_open_idx
  on public.student_alerts (class_id, status, updated_at desc);

alter table public.student_alerts enable row level security;

-- Học sinh chỉ thấy cảnh báo của mình KHI trợ giảng đã xử lý (status <> 'open').
drop policy if exists "student reads own visible alerts" on public.student_alerts;
create policy "student reads own visible alerts" on public.student_alerts
  for select to authenticated
  using (
    (student_id = auth.uid() and status <> 'open')
    or public.teaches_student(student_id)
  );

-- Admin + giảng viên phụ trách lớp: sửa trạng thái, gán trợ giảng, ghi chú.
drop policy if exists "staff update alerts" on public.student_alerts;
create policy "staff update alerts" on public.student_alerts
  for update to authenticated
  using (public.teaches_student(student_id)) with check (public.teaches_student(student_id));
drop policy if exists "admin manages alerts" on public.student_alerts;
create policy "admin manages alerts" on public.student_alerts
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
-- Việc TẠO cảnh báo do trigger (security definer) làm — không có policy insert cho người dùng thường.

create or replace function public.touch_student_alert()
returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end; $$;
drop trigger if exists trg_touch_student_alert on public.student_alerts;
create trigger trg_touch_student_alert before update on public.student_alerts
  for each row execute function public.touch_student_alert();


-- ============================================================
-- 5. Đánh giá cảnh báo cho 1 học sinh — chạy sau mỗi lần nộp bài
--    (a) đóng cảnh báo "bỏ bài" nếu đã nộp đủ
--    (b) tính chuỗi điểm thấp < 6,5 liên tiếp (>= 2 bài)
-- ============================================================
create or replace function public.evaluate_student_alerts(p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_threshold numeric := 6.5;
  v_min_streak int := 2;
  v_class bigint;
  v_streak int := 0;
  v_reason text := '';
  v_ids bigint[] := '{}';
  r record;
begin
  -- (a) đã nộp hết các bài từng bị ghi thiếu -> đóng cảnh báo missed_assessment
  update public.student_alerts sa
    set status = 'resolved',
        handled_note = case when sa.handled_note = '' then 'tự đóng: đã làm bài' else sa.handled_note end
  where sa.student_id = p_student and sa.kind = 'missed_assessment'
    and sa.status in ('open', 'contacted', 'tutoring')
    and not exists (
      select 1 from public.class_assessments ca
      where ca.id = any (sa.assessment_ids)
        and not exists (
          select 1 from public.exam_results er
          where er.student_id = p_student and er.exam_id = ca.exam_id
        )
    );

  -- (b) chuỗi điểm thấp — lớp có bài kiểm tra định kỳ gần nhất của học sinh
  select ca.class_id into v_class
  from public.class_assessments ca
  join public.user_classes uc on uc.class_id = ca.class_id
  where uc.user_id = p_student
  order by ca.published_at desc
  limit 1;

  if v_class is null then
    return; -- chưa thuộc lớp nào có bài kiểm tra định kỳ
  end if;

  -- Duyệt bài kiểm tra định kỳ của lớp, MỚI NHẤT trước; chỉ tính bài đã làm
  -- (điểm cao nhất); đếm chuỗi < threshold liên tiếp tính từ bài mới nhất.
  for r in
    select ca.id,
           coalesce(nullif(ca.term, '') || ' · ', '') ||
           (case ca.kind
              when 'giua_ki' then 'Giữa kỳ' when 'cuoi_ki' then 'Cuối kỳ'
              when 'chuong' then 'KT chương' else 'KT thường xuyên' end) as label,
           (select max(er.score)
              from public.exam_results er
              where er.student_id = p_student and er.exam_id = ca.exam_id) as best
    from public.class_assessments ca
    where ca.class_id = v_class
    order by coalesce(ca.sequence, 0) desc, ca.published_at desc
  loop
    if r.best is null then
      continue; -- bài chưa làm -> bỏ qua (không tính 0, không cắt chuỗi)
    end if;
    if r.best < v_threshold then
      v_streak := v_streak + 1;
      v_ids := v_ids || r.id;
      v_reason := v_reason || (case when v_reason = '' then '' else ' · ' end)
        || r.label || ' (' || to_char(r.best, 'FM990D0') || ')';
    else
      exit; -- gặp bài đạt -> hết chuỗi
    end if;
  end loop;

  if v_streak >= v_min_streak then
    insert into public.student_alerts
      (student_id, class_id, kind, severity, reason, assessment_ids, status)
    values (
      p_student, v_class, 'low_score_streak',
      case when v_streak >= 3 then 'urgent' else 'warning' end,
      v_streak || ' bài liên tiếp < ' || to_char(v_threshold, 'FM990D0') || ': ' || v_reason,
      v_ids, 'open'
    )
    on conflict (student_id, kind) do update set
      severity = excluded.severity,
      reason = excluded.reason,
      assessment_ids = excluded.assessment_ids,
      class_id = excluded.class_id,
      -- cảnh báo đã đóng mà chuỗi thấp quay lại -> mở lại như vấn đề mới
      status = case when student_alerts.status in ('resolved', 'dismissed')
                    then 'open' else student_alerts.status end,
      handled_note = case when student_alerts.status in ('resolved', 'dismissed')
                    then '' else student_alerts.handled_note end;
  else
    -- không còn chuỗi -> tự đóng cảnh báo đang mở/đang xử lý
    update public.student_alerts
      set status = 'resolved',
          handled_note = case when handled_note = '' then 'tự đóng: điểm phục hồi' else handled_note end
      where student_id = p_student and kind = 'low_score_streak'
        and status in ('open', 'contacted', 'tutoring');
  end if;
end;
$$;

create or replace function public.trg_exam_result_alert()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  perform public.evaluate_student_alerts(new.student_id);
  return new;
end;
$$;

drop trigger if exists trg_exam_result_alert on public.exam_results;
create trigger trg_exam_result_alert
  after insert on public.exam_results
  for each row execute function public.trg_exam_result_alert();


-- ============================================================
-- 6. Rà "bỏ bài kiểm tra" — gọi từ dashboard (không có cron)
--    Với mỗi bài kiểm tra định kỳ đã phát hành quá p_days ngày mà học sinh
--    trong lớp chưa nộp -> cảnh báo missed_assessment.
-- ============================================================
create or replace function public.sweep_missed_assessments(p_class bigint, p_days int default 7)
returns int
language plpgsql security definer set search_path = public
as $$
declare v_count int := 0; r record;
begin
  if not public.manages_class(p_class) then
    raise exception 'không có quyền với lớp này';
  end if;

  for r in
    select uc.user_id as student_id,
           array_agg(ca.id) as ids,
           string_agg(
             (case ca.kind when 'giua_ki' then 'Giữa kỳ' when 'cuoi_ki' then 'Cuối kỳ'
                           when 'chuong' then 'KT chương' else 'KT thường xuyên' end)
             || coalesce(' ' || nullif(ca.term, ''), ''), ' · ') as labels
    from public.class_assessments ca
    join public.user_classes uc on uc.class_id = ca.class_id
    where ca.class_id = p_class
      and ca.published_at < now() - make_interval(days => p_days)
      and not exists (
        select 1 from public.exam_results er
        where er.student_id = uc.user_id and er.exam_id = ca.exam_id
      )
    group by uc.user_id
  loop
    insert into public.student_alerts
      (student_id, class_id, kind, severity, reason, assessment_ids, status)
    values (
      r.student_id, p_class, 'missed_assessment',
      case when array_length(r.ids, 1) >= 2 then 'urgent' else 'warning' end,
      'Chưa làm ' || array_length(r.ids, 1) || ' bài kiểm tra: ' || r.labels,
      r.ids, 'open'
    )
    on conflict (student_id, kind) do update set
      severity = excluded.severity,
      reason = excluded.reason,
      assessment_ids = excluded.assessment_ids,
      status = case when student_alerts.status in ('resolved', 'dismissed')
                    then 'open' else student_alerts.status end;
    v_count := v_count + 1;
  end loop;
  return v_count;
end;
$$;

grant execute on function public.sweep_missed_assessments(bigint, int) to authenticated;
grant execute on function public.evaluate_student_alerts(uuid) to authenticated;
