-- Độ sâu đọc lý thuyết + quiz đã bấm (trang /lop-hoc/bai, mục lesson_items.kind = 'ly_thuyet').
-- Đi chung đường gom lô DT-01: client đẩy sự kiện kind 'read_depth' vào log_learning_events(p_events),
-- KHÔNG thêm round-trip khi tải trang.
--
-- Thiết kế:
--   * Bảng mới lesson_read_depth, 1 dòng / (học sinh, mục, ngày VN). Lý do không gộp vào learning_events:
--     learning_events là nhật ký nối tiếp (mỗi lần gửi 1 dòng, giữ 12 tháng); read_depth gửi lại mỗi lần
--     ẩn tab/rời mục nên nếu nối tiếp sẽ sinh nhiều dòng trùng ý. Upsert lấy MAX theo ngày thì gửi lặp
--     vô hại (idempotent), không cần client sinh mã lượt mở, và trần dòng = HS × mục lý thuyết × 90 ngày.
--   * Nếu tổng h3/tổng quiz đổi trong ngày (bài vừa sửa) thì lấy bộ số mới, không trộn max của hai bản bài.
--   * Mục phải tồn tại và là 'ly_thuyet'; lesson_id lấy từ mục (bỏ lessonId client gửi). Tài khoản staff
--     (admin/giảng viên/trợ giảng, is_staff()) xem thử bài thì KHÔNG ghi, để số liệu chỉ là HS.
--   * Kiểm số: số nguyên 0..200, h3Max <= h3Total, quizDone <= quizTotal; sai là bỏ sự kiện đó
--     (không clamp, vì số vượt là lỗi client). Cả h3Total và quizTotal = 0 thì bỏ (không có gì để đo).
--   * Giữ DB không phình: dữ liệu thô > 90 ngày gộp vào lesson_read_depth_rollups — 1 dòng / (HS, mục)
--     cả đời (giữ mức sâu nhất, tỉ lệ quiz cao nhất, số ngày có đọc). Trần = HS × mục lý thuyết, không lớn
--     theo thời gian, và vẫn lọc được theo lớp hiện tại. pg_cron 4:00 VN thứ Hai hằng tuần.
--   * learning_events ĐÃ có purge 12 tháng (20261017230000) — migration này không đụng.
--   * log_learning_events: create or replace, phần open/leave/submit giữ nguyên từng dòng; chỉ thêm nhánh
--     'read_depth' trước bước kiểm kind. Kết quả trả về = số sự kiện đã nhận (cả read_depth).
--
-- Ai đọc / ghi được gì:
--   | Vai                                   | lesson_read_depth / _rollups          | Ghi                        |
--   |---------------------------------------|---------------------------------------|----------------------------|
--   | anon                                  | không                                 | không                      |
--   | Học sinh                              | dòng của mình                          | chỉ qua log_learning_events, ép student_id = auth.uid() |
--   | Giảng viên (class_instructors)        | HS các lớp mình dạy (teaches_student)  | không                      |
--   | Trợ giảng đang hoạt động              | mọi HS (teaches_student, như learning_events) | không               |
--   | Admin                                 | tất cả                                 | không (trừ hàm rollup chạy bằng cron/postgres) |
--   | teacher_lesson_read_depth(lớp, bài)   | manages_class / assists_class / admin  | —                          |
--
-- Phụ thuộc: chạy SAU 20261017230000_learning_events (đã chạy 17/10). Chạy giờ nào cũng được
-- (chỉ tạo bảng/hàm, thay thân hàm log_learning_events trong một giao dịch, không xoá dữ liệu).
-- Rollback ở cuối file.

begin;

-- ---------- 1. Bảng thô ----------
create table if not exists public.lesson_read_depth (
  student_id  uuid not null references public.profiles(id) on delete cascade,
  item_id     bigint not null references public.lesson_items(id) on delete cascade,
  read_date   date not null,
  lesson_id   bigint references public.lessons(id) on delete set null,
  h3_max      smallint not null check (h3_max between 0 and 200),
  h3_total    smallint not null check (h3_total between 0 and 200),
  quiz_done   smallint not null check (quiz_done between 0 and 200),
  quiz_total  smallint not null check (quiz_total between 0 and 200),
  sends       integer not null default 1,
  first_at    timestamptz not null default now(),
  last_at     timestamptz not null default now(),
  primary key (student_id, item_id, read_date),
  check (h3_max <= h3_total),
  check (quiz_done <= quiz_total)
);
create index if not exists lesson_read_depth_item_idx on public.lesson_read_depth (item_id, read_date desc);
create index if not exists lesson_read_depth_date_idx on public.lesson_read_depth (read_date);

alter table public.lesson_read_depth enable row level security;
revoke all on public.lesson_read_depth from anon, authenticated;
grant select on public.lesson_read_depth to authenticated;

drop policy if exists "hs xem do sau doc cua minh" on public.lesson_read_depth;
create policy "hs xem do sau doc cua minh" on public.lesson_read_depth
  as permissive for select to authenticated
  using (student_id = (select auth.uid()));

drop policy if exists "giao vien xem do sau doc cua lop" on public.lesson_read_depth;
create policy "giao vien xem do sau doc cua lop" on public.lesson_read_depth
  as permissive for select to authenticated
  using (public.teaches_student(student_id) or public.is_admin());

-- ---------- 2. Bảng gộp (HS × mục, cả đời) ----------
create table if not exists public.lesson_read_depth_rollups (
  student_id  uuid not null references public.profiles(id) on delete cascade,
  item_id     bigint not null references public.lesson_items(id) on delete cascade,
  lesson_id   bigint references public.lessons(id) on delete set null,
  days_read   integer not null default 0,
  h3_max      smallint not null default 0,   -- của ngày có tỉ lệ h3_max/h3_total cao nhất
  h3_total    smallint not null default 0,
  quiz_done   smallint not null default 0,   -- của ngày có tỉ lệ quiz cao nhất
  quiz_total  smallint not null default 0,
  first_at    timestamptz,
  last_at     timestamptz,
  updated_at  timestamptz not null default now(),
  primary key (student_id, item_id)
);
create index if not exists lesson_read_depth_rollups_item_idx on public.lesson_read_depth_rollups (item_id);

alter table public.lesson_read_depth_rollups enable row level security;
revoke all on public.lesson_read_depth_rollups from anon, authenticated;
grant select on public.lesson_read_depth_rollups to authenticated;

drop policy if exists "hs xem gop do sau doc cua minh" on public.lesson_read_depth_rollups;
create policy "hs xem gop do sau doc cua minh" on public.lesson_read_depth_rollups
  as permissive for select to authenticated
  using (student_id = (select auth.uid()));

drop policy if exists "giao vien xem gop do sau doc cua lop" on public.lesson_read_depth_rollups;
create policy "giao vien xem gop do sau doc cua lop" on public.lesson_read_depth_rollups
  as permissive for select to authenticated
  using (public.teaches_student(student_id) or public.is_admin());

-- ---------- 3. log_learning_events: thêm nhánh read_depth ----------
-- p_events (cũ, giữ nguyên): {"lessonId":12,"itemId":34,"kind":"open|leave|submit","durationS":45,"at":"..."}
-- p_events (mới):            {"kind":"read_depth","itemId":34,"h3Max":3,"h3Total":5,"quizDone":1,"quizTotal":2,"at":"..."}
create or replace function public.log_learning_events(p_events jsonb)
returns integer
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_n integer := 0;
  v_e jsonb;
  v_kind text;
  v_dur integer;
  v_at timestamptz;
  v_staff boolean;
  v_item bigint;
  v_lesson bigint;
  v_h3m integer; v_h3t integer; v_qd integer; v_qt integer;
begin
  if v_uid is null then
    raise exception 'Chưa đăng nhập' using errcode = '42501';
  end if;
  if p_events is null or jsonb_typeof(p_events) <> 'array' then
    return 0;
  end if;
  for v_e in select * from jsonb_array_elements(p_events) limit 50 loop
    v_kind := v_e ->> 'kind';

    if v_kind = 'read_depth' then
      if v_staff is null then
        v_staff := public.is_staff();
      end if;
      continue when v_staff;
      continue when not (
        coalesce(v_e ->> 'itemId', '')   ~ '^[0-9]{1,18}$'
        and coalesce(v_e ->> 'h3Max', '')    ~ '^[0-9]{1,3}$'
        and coalesce(v_e ->> 'h3Total', '')  ~ '^[0-9]{1,3}$'
        and coalesce(v_e ->> 'quizDone', '') ~ '^[0-9]{1,3}$'
        and coalesce(v_e ->> 'quizTotal', '') ~ '^[0-9]{1,3}$'
      );
      v_h3m := (v_e ->> 'h3Max')::integer;
      v_h3t := (v_e ->> 'h3Total')::integer;
      v_qd  := (v_e ->> 'quizDone')::integer;
      v_qt  := (v_e ->> 'quizTotal')::integer;
      continue when v_h3t > 200 or v_qt > 200 or v_h3m > v_h3t or v_qd > v_qt or (v_h3t = 0 and v_qt = 0);
      v_item := (v_e ->> 'itemId')::bigint;
      select li.lesson_id into v_lesson
        from public.lesson_items li where li.id = v_item and li.kind = 'ly_thuyet';
      continue when not found;
      begin
        v_at := (v_e ->> 'at')::timestamptz;
      exception when others then
        v_at := null;
      end;
      if v_at is null or v_at > now() + interval '5 minutes' or v_at < now() - interval '1 day' then
        v_at := now();
      end if;
      insert into public.lesson_read_depth as d
        (student_id, item_id, read_date, lesson_id, h3_max, h3_total, quiz_done, quiz_total, first_at, last_at)
      values (v_uid, v_item, (v_at at time zone 'Asia/Ho_Chi_Minh')::date, v_lesson,
              v_h3m, v_h3t, v_qd, v_qt, v_at, v_at)
      on conflict (student_id, item_id, read_date) do update set
        h3_max     = case when d.h3_total = excluded.h3_total then greatest(d.h3_max, excluded.h3_max) else excluded.h3_max end,
        h3_total   = excluded.h3_total,
        quiz_done  = case when d.quiz_total = excluded.quiz_total then greatest(d.quiz_done, excluded.quiz_done) else excluded.quiz_done end,
        quiz_total = excluded.quiz_total,
        lesson_id  = excluded.lesson_id,
        sends      = d.sends + 1,
        first_at   = least(d.first_at, excluded.first_at),
        last_at    = greatest(d.last_at, excluded.last_at);
      v_n := v_n + 1;
      continue;
    end if;

    continue when v_kind is null or v_kind not in ('open', 'leave', 'submit');
    v_dur := case when (v_e ->> 'durationS') ~ '^[0-9]{1,5}$' then least((v_e ->> 'durationS')::integer, 3600) end;
    begin
      v_at := (v_e ->> 'at')::timestamptz;
    exception when others then
      v_at := null;
    end;
    if v_at is null or v_at > now() + interval '5 minutes' or v_at < now() - interval '1 day' then
      v_at := now();
    end if;
    insert into public.learning_events (student_id, lesson_id, item_id, kind, duration_s, occurred_at)
    values (
      v_uid,
      case when (v_e ->> 'lessonId') ~ '^[0-9]{1,18}$' then (v_e ->> 'lessonId')::bigint end,
      case when (v_e ->> 'itemId') ~ '^[0-9]{1,18}$' then (v_e ->> 'itemId')::bigint end,
      v_kind, v_dur, v_at
    );
    v_n := v_n + 1;
  end loop;
  return v_n;
exception when foreign_key_violation then
  -- lesson_id/item_id không tồn tại: bỏ cả lô, không làm hỏng trang đang học
  return 0;
end;
$$;
revoke all on function public.log_learning_events(jsonb) from public, anon;
grant execute on function public.log_learning_events(jsonb) to authenticated;

-- ---------- 4. Gộp thô > 90 ngày ----------
-- select public.rollup_lesson_read_depth(current_date - 90, true);   -- chỉ đếm thử
create or replace function public.rollup_lesson_read_depth(
  p_before date default ((now() at time zone 'Asia/Ho_Chi_Minh')::date - 90),
  p_dry boolean default false
)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_rows bigint;
  v_pairs bigint;
begin
  select count(*), count(distinct (student_id, item_id)) into v_rows, v_pairs
    from public.lesson_read_depth where read_date < p_before;
  if p_dry or v_rows = 0 then
    return jsonb_build_object('dry', p_dry, 'before', p_before, 'rows', v_rows, 'pairs', v_pairs);
  end if;

  with old as (
    delete from public.lesson_read_depth where read_date < p_before returning *
  ), cnt as (
    select o.student_id, o.item_id, count(*)::int as days_read, min(o.first_at) as first_at, max(o.last_at) as last_at
    from old o group by o.student_id, o.item_id
  ), bh as (
    select distinct on (o.student_id, o.item_id) o.student_id, o.item_id, o.lesson_id, o.h3_max, o.h3_total
    from old o
    order by o.student_id, o.item_id,
             case when o.h3_total > 0 then o.h3_max::numeric / o.h3_total else -1 end desc, o.read_date desc
  ), bq as (
    select distinct on (o.student_id, o.item_id) o.student_id, o.item_id, o.quiz_done, o.quiz_total
    from old o
    order by o.student_id, o.item_id,
             case when o.quiz_total > 0 then o.quiz_done::numeric / o.quiz_total else -1 end desc, o.read_date desc
  )
  insert into public.lesson_read_depth_rollups as r
    (student_id, item_id, lesson_id, days_read, h3_max, h3_total, quiz_done, quiz_total, first_at, last_at)
  select c.student_id, c.item_id, bh.lesson_id, c.days_read, bh.h3_max, bh.h3_total, bq.quiz_done, bq.quiz_total,
         c.first_at, c.last_at
  from cnt c
  join bh on bh.student_id = c.student_id and bh.item_id = c.item_id
  join bq on bq.student_id = c.student_id and bq.item_id = c.item_id
  on conflict (student_id, item_id) do update set
    days_read = r.days_read + excluded.days_read,
    h3_max   = case when coalesce(excluded.h3_max::numeric / nullif(excluded.h3_total, 0), -1)
                       >= coalesce(r.h3_max::numeric / nullif(r.h3_total, 0), -1)
                    then excluded.h3_max else r.h3_max end,
    h3_total = case when coalesce(excluded.h3_max::numeric / nullif(excluded.h3_total, 0), -1)
                       >= coalesce(r.h3_max::numeric / nullif(r.h3_total, 0), -1)
                    then excluded.h3_total else r.h3_total end,
    quiz_done  = case when coalesce(excluded.quiz_done::numeric / nullif(excluded.quiz_total, 0), -1)
                         >= coalesce(r.quiz_done::numeric / nullif(r.quiz_total, 0), -1)
                      then excluded.quiz_done else r.quiz_done end,
    quiz_total = case when coalesce(excluded.quiz_done::numeric / nullif(excluded.quiz_total, 0), -1)
                         >= coalesce(r.quiz_done::numeric / nullif(r.quiz_total, 0), -1)
                      then excluded.quiz_total else r.quiz_total end,
    lesson_id = coalesce(excluded.lesson_id, r.lesson_id),
    first_at  = least(r.first_at, excluded.first_at),
    last_at   = greatest(r.last_at, excluded.last_at),
    updated_at = now();

  return jsonb_build_object('dry', false, 'before', p_before, 'rows', v_rows, 'pairs', v_pairs);
end;
$$;
revoke all on function public.rollup_lesson_read_depth(date, boolean) from public, anon, authenticated;

-- ---------- 5. RPC cho GV: theo từng mục lý thuyết của bài ----------
-- Mỗi HS (đang active trong lớp) lấy 1 bản ghi "tốt nhất" gộp cả thô lẫn rollup:
-- độ sâu = h3_max của bản ghi có tỉ lệ h3_max/h3_total cao nhất; quiz tương tự, độc lập.
-- depth_hist: {"<h3_max>": số HS}. reached_end: số HS có h3_max = h3_total (> 0).
create or replace function public.teacher_lesson_read_depth(p_class_id bigint, p_lesson_id bigint)
returns table (
  item_id        bigint,
  item_title     text,
  sort_order     int,
  h3_total       int,     -- tổng h3 mới nhất HS báo về (bài có thể đã sửa)
  quiz_total     int,
  class_students int,
  students_read  int,
  reached_end    int,
  avg_depth_ratio numeric, -- trung bình h3_max/h3_total của HS đã đọc (0..1), null nếu mục không có h3
  depth_hist     jsonb,
  students_quiz  int,      -- HS có quiz_total > 0
  avg_quiz_ratio numeric,  -- trung bình quiz_done/quiz_total (0..1)
  last_read_at   timestamptz
)
language plpgsql stable security definer set search_path = public
as $$
#variable_conflict use_column
begin
  if not (public.manages_class(p_class_id) or public.assists_class(p_class_id) or public.is_admin()) then
    raise exception 'Không có quyền xem lớp này.' using errcode = '42501';
  end if;

  return query
  with st as (
    select uc.user_id from public.user_classes uc
    where uc.class_id = p_class_id and uc.status = 'active'
  ), items as (
    select li.id, li.title, li.sort_order from public.lesson_items li
    where li.lesson_id = p_lesson_id and li.kind = 'ly_thuyet'
  ), src as (
    select d.student_id, d.item_id, d.h3_max, d.h3_total, d.quiz_done, d.quiz_total, d.last_at
      from public.lesson_read_depth d
      join st on st.user_id = d.student_id join items on items.id = d.item_id
    union all
    select r.student_id, r.item_id, r.h3_max, r.h3_total, r.quiz_done, r.quiz_total, r.last_at
      from public.lesson_read_depth_rollups r
      join st on st.user_id = r.student_id join items on items.id = r.item_id
  ), best_h3 as (
    select distinct on (s.student_id, s.item_id) s.student_id, s.item_id, s.h3_max, s.h3_total
    from src s
    order by s.student_id, s.item_id,
             case when s.h3_total > 0 then s.h3_max::numeric / s.h3_total else -1 end desc, s.last_at desc
  ), best_qz as (
    select distinct on (s.student_id, s.item_id) s.student_id, s.item_id, s.quiz_done, s.quiz_total
    from src s where s.quiz_total > 0
    order by s.student_id, s.item_id, s.quiz_done::numeric / s.quiz_total desc, s.last_at desc
  ), latest as (
    select distinct on (s.item_id) s.item_id, s.h3_total, s.quiz_total
    from src s order by s.item_id, s.last_at desc
  ), hist as (
    select b.item_id, jsonb_object_agg(b.h3_max::text, b.n) as h
    from (select item_id, h3_max, count(*)::int as n from best_h3 where h3_total > 0 group by 1, 2) b
    group by b.item_id
  )
  select i.id, i.title, i.sort_order,
         l.h3_total::int, l.quiz_total::int,
         (select count(*)::int from st),
         (select count(*)::int from best_h3 b where b.item_id = i.id),
         (select count(*)::int from best_h3 b where b.item_id = i.id and b.h3_total > 0 and b.h3_max = b.h3_total),
         (select round(avg(b.h3_max::numeric / b.h3_total), 3) from best_h3 b where b.item_id = i.id and b.h3_total > 0),
         coalesce(h.h, '{}'::jsonb),
         (select count(*)::int from best_qz q where q.item_id = i.id),
         (select round(avg(q.quiz_done::numeric / q.quiz_total), 3) from best_qz q where q.item_id = i.id),
         (select max(s.last_at) from src s where s.item_id = i.id)
  from items i
  left join latest l on l.item_id = i.id
  left join hist h on h.item_id = i.id
  order by i.sort_order, i.id;
end;
$$;
revoke all on function public.teacher_lesson_read_depth(bigint, bigint) from public, anon;
grant execute on function public.teacher_lesson_read_depth(bigint, bigint) to authenticated;

commit;

-- ---------- 6. Lịch pg_cron (ngoài giao dịch, như 20261017230000) ----------
do $$
begin
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'lesson-read-depth-rollup';
    perform cron.schedule('lesson-read-depth-rollup', '0 21 * * 0', 'select public.rollup_lesson_read_depth();');
    raise notice 'Đã đặt lịch pg_cron lesson-read-depth-rollup (4:00 VN thứ Hai hằng tuần)';
  else
    raise notice 'pg_cron chưa bật: chạy tay select public.rollup_lesson_read_depth(); mỗi tháng';
  end if;
end $$;

-- ---------- KIỂM THỬ (chạy trong giao dịch rồi rollback; thay <...> bằng id thật) ----------
-- begin;
--   -- Học sinh: ghi được, chỉ thấy dòng của mình; sự kiện sai bị bỏ (kỳ vọng trả 2: 1 open + 1 read_depth hợp lệ)
--   set local role authenticated;
--   select set_config('request.jwt.claims', '{"sub":"<uuid_hs>","role":"authenticated"}', true);
--   select public.log_learning_events('[
--     {"kind":"open","lessonId":<lesson>,"itemId":<item_lt>},
--     {"kind":"read_depth","itemId":<item_lt>,"h3Max":3,"h3Total":5,"quizDone":1,"quizTotal":2},
--     {"kind":"read_depth","itemId":<item_lt>,"h3Max":6,"h3Total":5,"quizDone":0,"quizTotal":2},
--     {"kind":"read_depth","itemId":<item_luyen_tap>,"h3Max":1,"h3Total":2,"quizDone":0,"quizTotal":0}
--   ]'::jsonb);
--   select public.log_learning_events('[{"kind":"read_depth","itemId":<item_lt>,"h3Max":2,"h3Total":5,"quizDone":2,"quizTotal":2}]');
--   select h3_max, h3_total, quiz_done, sends from public.lesson_read_depth;   -- kỳ vọng 3,5,2,2 và chỉ dòng của HS này
--   select public.teacher_lesson_read_depth(<class>, <lesson>);               -- kỳ vọng lỗi 42501
--   insert into public.lesson_read_depth values ('<uuid_hs>', <item_lt>, current_date, null, 0,0,0,0); -- kỳ vọng permission denied
--   -- Trợ giảng (ta_assistants.active): đọc được, ghi read_depth bị bỏ (is_staff)
--   select set_config('request.jwt.claims', '{"sub":"<uuid_tro_giang>","role":"authenticated"}', true);
--   select count(*) from public.lesson_read_depth;                            -- kỳ vọng >= 1
--   select * from public.teacher_lesson_read_depth(<class>, <lesson>);        -- kỳ vọng có students_read >= 1
--   select public.log_learning_events('[{"kind":"read_depth","itemId":<item_lt>,"h3Max":1,"h3Total":5,"quizDone":0,"quizTotal":2}]'); -- kỳ vọng 0
--   -- Admin: đọc tất cả, RPC chạy cho mọi lớp
--   select set_config('request.jwt.claims', '{"sub":"<uuid_admin>","role":"authenticated"}', true);
--   select count(*) from public.lesson_read_depth_rollups;
--   select * from public.teacher_lesson_read_depth(<class>, <lesson>);
--   -- anon: không đọc được
--   reset role; set local role anon;
--   select count(*) from public.lesson_read_depth;                            -- kỳ vọng permission denied
-- rollback;

-- ---------- ROLLBACK ----------
-- do $$ begin
--   if exists (select 1 from pg_extension where extname = 'pg_cron') then
--     perform cron.unschedule(jobid) from cron.job where jobname = 'lesson-read-depth-rollup';
--   end if;
-- end $$;
-- drop function if exists public.teacher_lesson_read_depth(bigint, bigint);
-- drop function if exists public.rollup_lesson_read_depth(date, boolean);
-- -- log_learning_events: chạy lại khối create or replace function ở supabase/migrations/20261017230000_learning_events.sql
-- --   (nhánh read_depth mất; client gửi read_depth sẽ bị bỏ qua êm, không lỗi)
-- drop table if exists public.lesson_read_depth_rollups;
-- drop table if exists public.lesson_read_depth;
