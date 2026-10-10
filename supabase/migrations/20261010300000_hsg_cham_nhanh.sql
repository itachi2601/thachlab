-- Bảng chấm nhanh bài kiểm tra HSG KHTN 9 (nhập đáp án, chấm tự động; câu tự luận nhờ AI chấm).
-- Chỉ giáo viên/trợ giảng (is_staff) đọc/ghi. Tên học sinh KHÔNG được gửi cho AI (xem Edge Function hsg-ai-grade).
begin;

create table if not exists public.hsg_grade_tests (
  id bigint generated always as identity primary key,
  title text not null,
  kind text not null default 'custom' check (kind in ('pretest','custom')),
  config jsonb not null,           -- {questions:[{n,type:'mcq'|'num'|'essay',key,pts,topic,unit?,tol?}]}
  created_by uuid references public.profiles(id),
  created_at timestamptz not null default now(),
  archived boolean not null default false
);

create table if not exists public.hsg_grade_sheets (
  id bigint generated always as identity primary key,
  test_id bigint not null references public.hsg_grade_tests(id) on delete cascade,
  student_name text not null,
  class_name text not null default '',
  answers jsonb not null default '{}',   -- {"1":"C","21":"1,2","25":"bài làm tự luận…"}
  scores jsonb not null default '{}',    -- {"1":{"got":0.4,"by":"key"},"25":{"got":1.5,"by":"ai","comment":"…"}}
  total numeric not null default 0,
  graded_by uuid references public.profiles(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (test_id, student_name, class_name)
);
create index if not exists hsg_grade_sheets_test_idx on public.hsg_grade_sheets(test_id);

alter table public.hsg_grade_tests enable row level security;
alter table public.hsg_grade_sheets enable row level security;
revoke all on public.hsg_grade_tests, public.hsg_grade_sheets from anon, authenticated;
grant select, insert, update, delete on public.hsg_grade_tests, public.hsg_grade_sheets to authenticated;

create policy hsg_grade_tests_staff on public.hsg_grade_tests for all to authenticated
  using (public.is_staff()) with check (public.is_staff());
create policy hsg_grade_sheets_staff on public.hsg_grade_sheets for all to authenticated
  using (public.is_staff()) with check (public.is_staff());

-- Bài khảo sát đầu vào Cơ học THCS (24 câu, 10 điểm) — khoá lấy từ sinh-pretest-khtn-thcs.py
insert into public.hsg_grade_tests (title, kind, config)
select 'Pre-test Cơ học THCS (KHTN 9 – HSG)', 'pretest', '{"questions": [{"n": 1, "type": "mcq", "key": "C", "pts": 0.4, "topic": "Tốc độ"}, {"n": 2, "type": "mcq", "key": "B", "pts": 0.4, "topic": "Tốc độ"}, {"n": 3, "type": "mcq", "key": "A", "pts": 0.4, "topic": "Tốc độ"}, {"n": 4, "type": "mcq", "key": "D", "pts": 0.4, "topic": "Tốc độ"}, {"n": 5, "type": "mcq", "key": "A", "pts": 0.4, "topic": "KLR – áp suất – Archimedes"}, {"n": 6, "type": "mcq", "key": "D", "pts": 0.4, "topic": "KLR – áp suất – Archimedes"}, {"n": 7, "type": "mcq", "key": "B", "pts": 0.4, "topic": "KLR – áp suất – Archimedes"}, {"n": 8, "type": "mcq", "key": "C", "pts": 0.4, "topic": "KLR – áp suất – Archimedes"}, {"n": 9, "type": "mcq", "key": "C", "pts": 0.4, "topic": "KLR – áp suất – Archimedes"}, {"n": 10, "type": "mcq", "key": "A", "pts": 0.4, "topic": "KLR – áp suất – Archimedes"}, {"n": 11, "type": "mcq", "key": "B", "pts": 0.4, "topic": "Lực"}, {"n": 12, "type": "mcq", "key": "D", "pts": 0.4, "topic": "Lực"}, {"n": 13, "type": "mcq", "key": "A", "pts": 0.4, "topic": "Lực"}, {"n": 14, "type": "mcq", "key": "B", "pts": 0.4, "topic": "Lực"}, {"n": 15, "type": "mcq", "key": "C", "pts": 0.4, "topic": "Lực"}, {"n": 16, "type": "mcq", "key": "D", "pts": 0.4, "topic": "Năng lượng cơ học"}, {"n": 17, "type": "mcq", "key": "A", "pts": 0.4, "topic": "Năng lượng cơ học"}, {"n": 18, "type": "mcq", "key": "B", "pts": 0.4, "topic": "Năng lượng cơ học"}, {"n": 19, "type": "mcq", "key": "C", "pts": 0.4, "topic": "Năng lượng cơ học"}, {"n": 20, "type": "mcq", "key": "D", "pts": 0.4, "topic": "Năng lượng cơ học"}, {"n": 21, "type": "num", "key": 1.2, "unit": "h", "tol": 0.01, "pts": 0.5, "topic": "Tốc độ"}, {"n": 22, "type": "num", "key": 600, "unit": "kg/m³", "tol": 0.01, "pts": 0.5, "topic": "KLR – áp suất – Archimedes"}, {"n": 23, "type": "num", "key": 400, "unit": "N", "tol": 0.01, "pts": 0.5, "topic": "Lực"}, {"n": 24, "type": "num", "key": 66.7, "unit": "%", "tol": 0.01, "pts": 0.5, "topic": "Năng lượng cơ học"}]}'::jsonb
where not exists (select 1 from public.hsg_grade_tests where kind='pretest');

commit;

-- ROLLBACK:
-- drop table if exists public.hsg_grade_sheets; drop table if exists public.hsg_grade_tests;
