-- ============================================================================
-- Phụ đạo — bắt buộc XEM LẠI LÝ THUYẾT TƯƠNG TÁC trước khi làm bài tự kiểm tra thoát phụ đạo.
--
--  1. tutoring_theory_reviews: mỗi mục cần phụ đạo có đúng 1 dòng "lượt xem lại" hiện tại — thời gian
--     xem thật (máy chủ tự kẹp theo đồng hồ), số mốc đã cuộn tới, số câu tự kiểm tra trong bài đã trả lời.
--  2. rpc tutoring_review_start / tutoring_review_ping: mở lượt (tự tìm mục lý thuyết của bài) và ghi tiến độ.
--     Hoàn thành khi: đủ thời gian xem (40% thời gian đọc ước tính, 45–480 giây) + cuộn hết mọi mốc +
--     trả lời >= 80% câu tự kiểm tra nằm trong bài.
--  3. tutoring_exit_attempt_guard: lượt TỰ KIỂM TRA (ngoài cửa sổ cuối buổi) chỉ được ghi khi đã có lượt
--     xem lại hoàn thành SAU lượt làm trước đó — mỗi lần thử lại đều phải xem lại. Bài không có mục lý
--     thuyết thì không chặn. Lượt trong cửa sổ cuối buổi (trợ giảng mở) KHÔNG đòi xem lại.
--
-- Chạy lúc nào cũng được (chỉ thêm bảng/hàm, thay guard). Chưa chạy thì client tự bỏ qua bước xem lại
-- (RPC không tồn tại) và guard cũ vẫn như cũ.
-- Rollback: perf/rollback/20261004130000_phu_dao_xem_lai_ly_thuyet.down.sql
-- ============================================================================
begin;

-- ---------- 1. Bảng lượt xem lại ----------
create table if not exists public.tutoring_theory_reviews (
  tutoring_need_id bigint primary key references public.tutoring_needs (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  item_id bigint not null references public.lesson_items (id) on delete cascade,
  started_at timestamptz not null default now(),
  last_ping_at timestamptz not null default now(),
  active_seconds integer not null default 0,
  required_seconds integer not null default 45,
  sections_total integer not null default 1,
  sections_seen integer not null default 0,
  quiz_total integer not null default 0,
  quiz_answered integer not null default 0,
  completed_at timestamptz
);
alter table public.tutoring_theory_reviews enable row level security;

-- Chỉ đọc: học sinh xem của mình, giáo viên/trợ giảng phụ trách xem được em của mình. Ghi qua RPC.
drop policy if exists "read own theory reviews" on public.tutoring_theory_reviews;
create policy "read own theory reviews" on public.tutoring_theory_reviews
  for select to authenticated
  using (student_id = (select auth.uid()) or public.teaches_student(student_id));

-- ---------- 2. Mục lý thuyết của một chủ đề ----------
create or replace function public.tutoring_theory_item(p_topic bigint)
returns bigint
language sql stable security definer set search_path = public
as $$
  select li.id
  from public.question_topics t
  join public.lesson_items li on li.lesson_id = t.lesson_id
  where t.id = p_topic
    and li.kind = 'ly_thuyet'
    and coalesce(btrim(li.body_html), '') <> ''
  order by li.sort_order, li.id
  limit 1
$$;

-- ---------- 3. Mở / tiếp tục lượt xem lại ----------
create or replace function public.tutoring_review_start(
  p_need bigint, p_sections int, p_quiz_total int, p_est_seconds int
) returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_need public.tutoring_needs%rowtype;
  v_item bigint;
  v_last timestamptz;
  v_rev public.tutoring_theory_reviews%rowtype;
  v_req int := greatest(45, least(480, round(greatest(coalesce(p_est_seconds, 0), 0) * 0.4)::int));
  v_sec int := greatest(1, least(coalesce(p_sections, 1), 60));
  v_quiz int := greatest(0, least(coalesce(p_quiz_total, 0), 60));
begin
  select * into v_need from public.tutoring_needs where id = p_need;
  if v_uid is null or not found or v_need.student_id <> v_uid
     or v_need.status not in ('open', 'assigned', 'tutored') then
    return jsonb_build_object('required', false, 'reason', 'no_need');
  end if;
  v_item := public.tutoring_theory_item(v_need.topic_id);
  if v_item is null then
    return jsonb_build_object('required', false, 'reason', 'no_theory');
  end if;

  select max(created_at) into v_last from public.tutoring_exit_attempts
    where tutoring_need_id = p_need and student_id = v_uid and window_id is null;

  select * into v_rev from public.tutoring_theory_reviews where tutoring_need_id = p_need;
  if found and v_rev.item_id = v_item and (v_last is null or v_rev.started_at > v_last) then
    -- lượt hiện tại chưa bị một lượt làm bài "dùng hết": hoàn thành thì giữ, dở dang thì cho xem tiếp
    if v_rev.completed_at is null then
      update public.tutoring_theory_reviews
        set last_ping_at = now(), required_seconds = v_req, sections_total = v_sec, quiz_total = v_quiz,
            sections_seen = least(sections_seen, v_sec), quiz_answered = least(quiz_answered, v_quiz)
        where tutoring_need_id = p_need
        returning * into v_rev;
    end if;
  else
    insert into public.tutoring_theory_reviews as r
      (tutoring_need_id, student_id, item_id, required_seconds, sections_total, quiz_total)
    values (p_need, v_uid, v_item, v_req, v_sec, v_quiz)
    on conflict (tutoring_need_id) do update
      set item_id = excluded.item_id, started_at = now(), last_ping_at = now(), active_seconds = 0,
          required_seconds = excluded.required_seconds, sections_total = excluded.sections_total,
          sections_seen = 0, quiz_total = excluded.quiz_total, quiz_answered = 0, completed_at = null
    returning * into v_rev;
  end if;

  return jsonb_build_object('required', true, 'item_id', v_rev.item_id,
    'completed', v_rev.completed_at is not null,
    'active_seconds', v_rev.active_seconds, 'required_seconds', v_rev.required_seconds,
    'sections_total', v_rev.sections_total, 'sections_seen', v_rev.sections_seen,
    'quiz_total', v_rev.quiz_total, 'quiz_answered', v_rev.quiz_answered);
end; $$;

-- ---------- 4. Ghi tiến độ (client gọi ~10 giây/lần khi em đang thật sự xem) ----------
create or replace function public.tutoring_review_ping(
  p_need bigint, p_delta int, p_sections_seen int, p_quiz_answered int
) returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_rev public.tutoring_theory_reviews%rowtype;
  v_wall int;
  v_add int;
  v_done boolean;
begin
  select * into v_rev from public.tutoring_theory_reviews
    where tutoring_need_id = p_need and student_id = v_uid for update;
  if not found then return jsonb_build_object('ok', false); end if;
  if v_rev.completed_at is not null then
    return jsonb_build_object('ok', true, 'completed', true);
  end if;

  -- Thời gian cộng thêm không được vượt đồng hồ thật kể từ lần ghi trước (+2 giây dung sai), tối đa 20 giây/lần.
  v_wall := greatest(0, floor(extract(epoch from (now() - v_rev.last_ping_at)))::int);
  v_add := greatest(0, least(coalesce(p_delta, 0), 20, v_wall + 2));

  update public.tutoring_theory_reviews set
    last_ping_at = now(),
    active_seconds = active_seconds + v_add,
    sections_seen = greatest(sections_seen, least(greatest(coalesce(p_sections_seen, 0), 0), sections_total)),
    quiz_answered = greatest(quiz_answered, least(greatest(coalesce(p_quiz_answered, 0), 0), quiz_total))
  where tutoring_need_id = p_need
  returning * into v_rev;

  v_done := v_rev.active_seconds >= v_rev.required_seconds
        and v_rev.sections_seen >= v_rev.sections_total
        and v_rev.quiz_answered >= ceil(v_rev.quiz_total * 0.8);
  if v_done then
    update public.tutoring_theory_reviews set completed_at = now()
      where tutoring_need_id = p_need returning * into v_rev;
  end if;

  return jsonb_build_object('ok', true, 'completed', v_done,
    'active_seconds', v_rev.active_seconds, 'required_seconds', v_rev.required_seconds,
    'sections_total', v_rev.sections_total, 'sections_seen', v_rev.sections_seen,
    'quiz_total', v_rev.quiz_total, 'quiz_answered', v_rev.quiz_answered);
end; $$;

revoke all on function public.tutoring_theory_item(bigint) from public;
revoke all on function public.tutoring_review_start(bigint, int, int, int) from public;
revoke all on function public.tutoring_review_ping(bigint, int, int, int) from public;
grant execute on function public.tutoring_review_start(bigint, int, int, int) to authenticated;
grant execute on function public.tutoring_review_ping(bigint, int, int, int) to authenticated;

-- ---------- 5. Guard: tự kiểm tra thoát phụ đạo đòi đã xem lại lý thuyết ----------
create or replace function public.tutoring_exit_attempt_guard()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  v_need public.tutoring_needs%rowtype;
  v_win public.tutoring_exit_windows%rowtype;
  v_last timestamptz;
  v_last_self timestamptz;
  v_rev public.tutoring_theory_reviews%rowtype;
begin
  select * into v_need from public.tutoring_needs where id = new.tutoring_need_id;
  if not found or v_need.student_id <> new.student_id then
    raise exception 'Không tìm thấy mục cần phụ đạo của em';
  end if;
  if v_need.status not in ('open', 'assigned', 'tutored') then
    raise exception 'Chủ đề này không còn cần phụ đạo';
  end if;

  if new.window_id is not null then
    select * into v_win from public.tutoring_exit_windows where id = new.window_id;
    if not found or not (new.student_id = any (v_win.student_ids))
       or not (v_need.topic_id = any (v_win.topic_ids)) then
      raise exception 'Bài kiểm tra cuối buổi này không dành cho em hoặc chủ đề này';
    end if;
    if now() > v_win.closes_at + interval '30 seconds' then
      raise exception 'Cửa sổ kiểm tra cuối buổi đã đóng';
    end if;
    new.topic_id := v_need.topic_id;
    new.form := v_need.form;
    new.pct := round(new.correct * 100.0 / new.total)::int;
    new.passed := new.pct >= 70;
    return new;
  end if;

  select max(created_at) into v_last from public.tutoring_exit_attempts
    where tutoring_need_id = new.tutoring_need_id and student_id = new.student_id;
  if v_last is not null and v_last > now() - interval '24 hours' then
    raise exception 'Lượt tự kiểm tra tiếp theo của chủ đề này mở sau 24 giờ kể từ lượt trước — em ôn lại lý thuyết rồi quay lại nhé.';
  end if;

  -- Phải xem lại lý thuyết tương tác (đủ thời gian, đủ mốc, đủ câu tự kiểm tra) SAU lượt tự kiểm tra trước.
  if public.tutoring_theory_item(v_need.topic_id) is not null then
    select max(created_at) into v_last_self from public.tutoring_exit_attempts
      where tutoring_need_id = new.tutoring_need_id and student_id = new.student_id and window_id is null;
    select * into v_rev from public.tutoring_theory_reviews
      where tutoring_need_id = new.tutoring_need_id and student_id = new.student_id;
    if not found or v_rev.completed_at is null
       or (v_last_self is not null and v_rev.completed_at <= v_last_self) then
      raise exception 'Em cần xem lại bài lý thuyết của chủ đề này (xem đủ các mốc, trả lời các câu tự kiểm tra trong bài) trước khi làm bài thoát phụ đạo.';
    end if;
  end if;

  new.topic_id := v_need.topic_id;
  new.form := v_need.form;
  new.pct := round(new.correct * 100.0 / new.total)::int;
  new.passed := new.pct >= 80;
  return new;
end; $$;

commit;
