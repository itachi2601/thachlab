-- 20261108120000_cnc_prep_responses.sql
-- CNC lớp đảo ngược: quiz "chuẩn bị tối trước" theo buổi (JiTT) + câu "chỗ em chưa rõ".
-- Câu hỏi nằm ở exams.cnc_key = 'prep-<buổi>' (đăng qua /quan-tri/cnc-dang-de như các ngân hàng CNC khác).
-- Bảng này lưu MỖI LƯỢT nộp (làm lại được) để giảng viên xem trước giờ học: câu nào lớp sai nhiều,
-- ai chưa làm, các câu hỏi chưa rõ. Không tính điểm (chỉ chẩn đoán) nên chấm ở máy khách là đủ.
-- Thiết kế: docs/CNC-FLIPPED-THIET-KE-LAI-2026-11-08.md mục 5 việc 1.
--
-- Ai đọc / ghi được gì:
--   | Vai                                 | SELECT              | INSERT                                          | UPDATE/DELETE |
--   |-------------------------------------|---------------------|-------------------------------------------------|---------------|
--   | anon                                | không               | không                                           | không         |
--   | sinh viên                           | dòng của mình       | dòng của mình, khi đang ghi danh active khoá đó | không         |
--   | giảng viên được phân công khoá      | mọi dòng khoá đó    | (như sinh viên)                                 | không         |
--   | admin                               | mọi dòng            | (như sinh viên)                                 | không         |
--
-- Bảng mới, rỗng, không quét dữ liệu cũ → chạy giờ nào cũng được.
-- Chạy: bash scripts/run-migrations.sh (KHÔNG supabase db push).
-- Rollback: perf/rollback/20261108120000_cnc_prep_responses.down.sql

create table if not exists public.cnc_prep_responses (
  id          bigint generated always as identity primary key,
  course_id   bigint not null references public.course_offerings(id) on delete cascade,
  student_id  uuid not null default auth.uid() references public.profiles(id) on delete cascade,
  session_no  smallint not null check (session_no between 1 and 30),
  -- Mảng theo thứ tự câu trong ngân hàng prep-<buổi>: chỉ số phương án đã chọn (0 = A) hoặc null.
  answers     jsonb not null check (jsonb_typeof(answers) = 'array' and jsonb_array_length(answers) between 1 and 20),
  score       smallint not null,
  total       smallint not null check (total between 1 and 20),
  chua_ro     text check (chua_ro is null or char_length(chua_ro) <= 500),
  created_at  timestamptz not null default now(),
  constraint cnc_prep_responses_score_chk check (score between 0 and total)
);

comment on table public.cnc_prep_responses is
  'CNC lớp đảo ngược: mỗi lượt nộp quiz chuẩn bị tối trước (exams.cnc_key prep-N). SV ghi/đọc của mình; GV phân công khoá + admin đọc cả khoá.';

create index if not exists cnc_prep_responses_course_session_idx
  on public.cnc_prep_responses (course_id, session_no, created_at);

alter table public.cnc_prep_responses enable row level security;

revoke all on table public.cnc_prep_responses from anon, authenticated;
grant insert, select on table public.cnc_prep_responses to authenticated;

drop policy if exists "cnc_prep_responses insert own enrolled" on public.cnc_prep_responses;
create policy "cnc_prep_responses insert own enrolled" on public.cnc_prep_responses
  for insert to authenticated
  with check (
    student_id = (select auth.uid())
    and exists (
      select 1 from public.course_enrollments e
      where e.course_id = cnc_prep_responses.course_id
        and e.student_id = (select auth.uid())
        and e.status = 'active'
    )
  );

drop policy if exists "cnc_prep_responses select own or course staff" on public.cnc_prep_responses;
create policy "cnc_prep_responses select own or course staff" on public.cnc_prep_responses
  for select to authenticated
  using (
    student_id = (select auth.uid())
    or public.is_admin()
    or exists (
      select 1 from public.course_instructors ci
      where ci.course_id = cnc_prep_responses.course_id
        and ci.instructor_id = (select auth.uid())
    )
  );

-- Kiểm thử sau khi chạy (trong giao dịch, rollback cuối):
-- begin;
--   set local role authenticated;
--   -- SV đã ghi danh active khoá <course>: insert OK, select thấy dòng của mình.
--   select set_config('request.jwt.claims', json_build_object('sub','<uuid_sv>','role','authenticated')::text, true);
--   insert into public.cnc_prep_responses (course_id, session_no, answers, score, total, chua_ro)
--     values (<course>, 2, '[0,1,null,2,3]', 3, 5, 'thử');                -- OK
--   select count(*) from public.cnc_prep_responses;                        -- >= 1 (chỉ của mình)
--   insert into public.cnc_prep_responses (course_id, student_id, session_no, answers, score, total)
--     values (<course>, '<uuid_khac>', 2, '[0]', 0, 1);                    -- lỗi RLS
--   update public.cnc_prep_responses set score = 5;                        -- permission denied
--   -- GV được phân công khoá: thấy mọi dòng khoá đó.
--   select set_config('request.jwt.claims', json_build_object('sub','<uuid_gv>','role','authenticated')::text, true);
--   select count(*) from public.cnc_prep_responses where course_id = <course>;  -- >= 1
-- rollback;
--
-- ROLLBACK: drop table if exists public.cnc_prep_responses;
