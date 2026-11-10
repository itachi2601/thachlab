-- Đề làm bằng MÃ, không cần tài khoản: mỗi lượt vào (quét QR / nhập mã) em nhập họ tên + MSSV + lớp, server XÁO câu và
-- XÁO phương án riêng cho lượt đó, chấm ở server (dùng lại exam_grade_responses), điểm vào bảng điểm riêng theo lớp
-- (cột gradebook, vd 'CĐCK 24A').
--  - guest_exam_links     : đề nào mở bằng mã nào, ghi vào bảng điểm nào, đang mở/đóng.
--  - guest_exam_sessions  : mỗi lượt = một dòng (thông tin em nhập, hoán vị đã xáo, bài làm, điểm).
--  - guest_exam_info(code) / guest_exam_start(...) / guest_exam_submit(...) : anon gọi được, KHÔNG lộ đáp án.
-- Bảng mới: bật RLS, chỉ staff (is_staff) đọc/ghi; anon không đụng trực tiếp vào bảng.
-- Chạy lúc nào cũng được (bảng + hàm mới, không đụng dữ liệu cũ).

begin;

create table if not exists public.guest_exam_links (
  id bigint generated always as identity primary key,
  code text not null unique check (code = upper(code) and code ~ '^[A-Z0-9]{4,12}$'),
  exam_id bigint not null references public.exams(id) on delete cascade,
  gradebook text not null check (length(btrim(gradebook)) between 2 and 60),
  is_open boolean not null default true,
  note text,
  created_by uuid references public.profiles(id),
  created_at timestamptz not null default now()
);
create index if not exists guest_exam_links_exam_idx on public.guest_exam_links (exam_id);

create table if not exists public.guest_exam_sessions (
  id uuid primary key default gen_random_uuid(),
  link_id bigint not null references public.guest_exam_links(id) on delete cascade,
  exam_id bigint not null references public.exams(id) on delete cascade,
  gradebook text not null,
  full_name text not null,
  student_code text not null,
  class_name text not null,
  perm jsonb not null,                 -- [{src, opt:[...], st:[...]}] theo thứ tự HIỂN THỊ
  responses jsonb,                     -- bài làm theo thứ tự hiển thị
  score numeric(4,2),
  correct_count int,
  question_count int,
  started_at timestamptz not null default now(),
  submitted_at timestamptz,
  duration_seconds int
);
create index if not exists guest_exam_sessions_gradebook_idx on public.guest_exam_sessions (gradebook, student_code);
create index if not exists guest_exam_sessions_link_idx on public.guest_exam_sessions (link_id);

alter table public.guest_exam_links enable row level security;
alter table public.guest_exam_sessions enable row level security;
revoke all on public.guest_exam_links, public.guest_exam_sessions from anon, authenticated;
grant select, insert, update, delete on public.guest_exam_links to authenticated;
grant select, delete on public.guest_exam_sessions to authenticated;

drop policy if exists guest_exam_links_staff on public.guest_exam_links;
create policy guest_exam_links_staff on public.guest_exam_links
  for all to authenticated using (public.is_staff()) with check (public.is_staff());
drop policy if exists guest_exam_sessions_staff_read on public.guest_exam_sessions;
create policy guest_exam_sessions_staff_read on public.guest_exam_sessions
  for select to authenticated using (public.is_staff());
drop policy if exists guest_exam_sessions_staff_delete on public.guest_exam_sessions;
create policy guest_exam_sessions_staff_delete on public.guest_exam_sessions
  for delete to authenticated using (public.is_staff());

-- ---------- Thông tin hiển thị ở màn nhập (trước khi nhập tên) ----------
create or replace function public.guest_exam_info(p_code text)
returns jsonb
language sql stable security definer set search_path = public
as $$
  select jsonb_build_object('title', e.title, 'duration_minutes', e.duration_minutes,
                            'question_count', jsonb_array_length(e.questions), 'gradebook', l.gradebook)
  from public.guest_exam_links l join public.exams e on e.id = l.exam_id
  where l.code = upper(btrim(coalesce(p_code, ''))) and l.is_open
$$;

-- ---------- Bắt đầu một lượt: xáo câu (trong từng phần) + xáo phương án / ý a) b) c) d) ----------
create or replace function public.guest_exam_start(p_code text, p_full_name text, p_student_code text, p_class_name text)
returns jsonb
language plpgsql volatile security definer set search_path = public
as $$
declare
  v_name text := regexp_replace(btrim(coalesce(p_full_name, '')), '\s+', ' ', 'g');
  v_mssv text := upper(regexp_replace(btrim(coalesce(p_student_code, '')), '\s+', '', 'g'));
  v_class text := upper(regexp_replace(btrim(coalesce(p_class_name, '')), '\s+', ' ', 'g'));
  l public.guest_exam_links%rowtype;
  e public.exams%rowtype;
  v_perm jsonb;
  v_pub jsonb;
  v_id uuid;
begin
  if length(v_name) < 2 or length(v_name) > 80 then raise exception 'Họ tên chưa hợp lệ' using errcode = '22023'; end if;
  if length(v_mssv) < 3 or length(v_mssv) > 20 or v_mssv !~ '^[A-Z0-9._-]+$' then
    raise exception 'Mã số sinh viên chưa hợp lệ' using errcode = '22023';
  end if;
  if length(v_class) < 2 or length(v_class) > 30 then raise exception 'Lớp chưa hợp lệ' using errcode = '22023'; end if;

  select * into l from public.guest_exam_links where code = upper(btrim(coalesce(p_code, ''))) and is_open;
  if not found then raise exception 'Mã đề không đúng hoặc đã đóng' using errcode = 'P0002'; end if;
  select * into e from public.exams where id = l.exam_id;
  if not found or jsonb_typeof(e.questions) <> 'array' or jsonb_array_length(e.questions) = 0 then
    raise exception 'Đề chưa có câu hỏi' using errcode = 'P0002';
  end if;

  -- Hoán vị: giữ thứ tự các PHẦN (trắc nghiệm → đúng/sai → trả lời ngắn → dịch → tự luận), xáo câu trong từng phần.
  select jsonb_agg(jsonb_build_object(
           'src', o.src,
           'opt', case when o.v ->> 'type' = 'multiple_choice' and jsonb_typeof(o.v -> 'options') = 'array' then (
                    select jsonb_agg(k - 1 order by random()) from generate_series(1, jsonb_array_length(o.v -> 'options')) k) end,
           'st',  case when o.v ->> 'type' = 'true_false' and jsonb_typeof(o.v -> 'statements') = 'array' then (
                    select jsonb_agg(k - 1 order by random()) from generate_series(1, jsonb_array_length(o.v -> 'statements')) k) end
         ) order by o.part, random())
    into v_perm
  from (
    select (t.i - 1)::int as src, t.v,
           case t.v ->> 'type' when 'multiple_choice' then 1 when 'true_false' then 2 when 'short_answer' then 3
                               when 'translation' then 4 else 5 end as part
    from jsonb_array_elements(e.questions) with ordinality as t (v, i)
  ) o;

  select jsonb_agg(
           case p.pq ->> 'type'
             when 'multiple_choice' then jsonb_set(p.pq, '{options}', coalesce((
               select jsonb_agg(p.q -> 'options' -> (x.o)::int order by x.n)
               from jsonb_array_elements_text(p.perm -> 'opt') with ordinality as x (o, n)), '[]'::jsonb))
             when 'true_false' then jsonb_set(p.pq, '{statements}', coalesce((
               select jsonb_agg(p.pq -> 'statements' -> (x.o)::int order by x.n)
               from jsonb_array_elements_text(p.perm -> 'st') with ordinality as x (o, n)), '[]'::jsonb))
             else p.pq end
           order by p.pos)
    into v_pub
  from (
    select pe.pos, pe.perm, e.questions -> (pe.perm ->> 'src')::int as q,
           public.exam_q_public(e.questions -> (pe.perm ->> 'src')::int) as pq
    from jsonb_array_elements(v_perm) with ordinality as pe (perm, pos)
  ) p;

  insert into public.guest_exam_sessions (link_id, exam_id, gradebook, full_name, student_code, class_name, perm)
  values (l.id, e.id, l.gradebook, v_name, v_mssv, v_class, v_perm)
  returning id into v_id;

  return jsonb_build_object('session_id', v_id, 'title', e.title, 'duration_minutes', e.duration_minutes,
                            'gradebook', l.gradebook, 'questions', v_pub);
end;
$$;

-- ---------- Nộp bài: trả bài về thứ tự gốc, chấm bằng đúng hàm chấm của đề thường ----------
create or replace function public.guest_exam_submit(p_session_id uuid, p_responses jsonb)
returns jsonb
language plpgsql volatile security definer set search_path = public
as $$
declare
  s public.guest_exam_sessions%rowtype;
  e public.exams%rowtype;
  v_n int;
  v_orig jsonb := '[]'::jsonb;
  v_g jsonb;
  i int;
  k int;
  v_perm jsonb;
  v_r jsonb;
  v_o jsonb;
  d int;
begin
  select * into s from public.guest_exam_sessions where id = p_session_id for update;
  if not found then raise exception 'Không tìm thấy lượt làm' using errcode = 'P0002'; end if;
  if s.submitted_at is not null then
    return jsonb_build_object('score10', s.score, 'correct_count', s.correct_count, 'question_count', s.question_count,
                              'full_name', s.full_name, 'student_code', s.student_code, 'already', true);
  end if;
  if p_responses is null or jsonb_typeof(p_responses) <> 'array' then
    raise exception 'Bài làm không hợp lệ' using errcode = '22023';
  end if;
  select * into e from public.exams where id = s.exam_id;
  v_n := jsonb_array_length(e.questions);

  -- v_orig[src] = bài làm của câu gốc src, đã đổi chỉ số phương án / ý về thứ tự gốc
  for i in 0 .. v_n - 1 loop v_orig := v_orig || jsonb_build_array('null'::jsonb); end loop;
  for k in 0 .. jsonb_array_length(s.perm) - 1 loop
    v_perm := s.perm -> k;
    v_r := p_responses -> k;                        -- SQL NULL nếu mảng ngắn hơn
    v_o := coalesce(v_r, 'null'::jsonb);
    if jsonb_typeof(v_perm -> 'opt') = 'array' then
      v_o := 'null'::jsonb;
      if jsonb_typeof(v_r) = 'number' then
        d := (v_r #>> '{}')::numeric::int;
        if d >= 0 and d < jsonb_array_length(v_perm -> 'opt') then v_o := v_perm -> 'opt' -> d; end if;
      end if;
    elsif jsonb_typeof(v_perm -> 'st') = 'array' then
      v_o := '[null,null,null,null]'::jsonb;
      if jsonb_typeof(v_r) = 'array' then
        for d in 0 .. least(jsonb_array_length(v_r), jsonb_array_length(v_perm -> 'st')) - 1 loop
          if jsonb_typeof(v_r -> d) = 'boolean' then
            v_o := jsonb_set(v_o, array[((v_perm -> 'st' ->> d)::int)::text], v_r -> d);
          end if;
        end loop;
      end if;
    end if;
    v_orig := jsonb_set(v_orig, array[(v_perm ->> 'src')], v_o);
  end loop;

  v_g := public.exam_grade_responses(e.questions, v_orig);
  update public.guest_exam_sessions set
    responses = p_responses, submitted_at = now(),
    score = (v_g ->> 'score10')::numeric, correct_count = (v_g ->> 'correct_count')::int, question_count = v_n,
    duration_seconds = greatest(0, extract(epoch from (now() - started_at))::int)
  where id = s.id;

  return jsonb_build_object('score10', (v_g ->> 'score10')::numeric, 'correct_count', (v_g ->> 'correct_count')::int,
                            'question_count', v_n, 'full_name', s.full_name, 'student_code', s.student_code);
end;
$$;

revoke all on function public.guest_exam_info(text), public.guest_exam_start(text, text, text, text),
  public.guest_exam_submit(uuid, jsonb) from public;
grant execute on function public.guest_exam_info(text) to anon, authenticated;
grant execute on function public.guest_exam_start(text, text, text, text) to anon, authenticated;
grant execute on function public.guest_exam_submit(uuid, jsonb) to anon, authenticated;

commit;

-- ROLLBACK:
--   drop function if exists public.guest_exam_submit(uuid, jsonb), public.guest_exam_start(text, text, text, text), public.guest_exam_info(text);
--   drop table if exists public.guest_exam_sessions, public.guest_exam_links;  -- mất cả bảng điểm: xuất CSV trước
