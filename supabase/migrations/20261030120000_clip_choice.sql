-- Lựa chọn Dự đoán ở khung video thí nghiệm (components/lessons/KhungPortals.tsx → logClipChoice).
-- Đi chung đường gom lô DT-01: client đẩy sự kiện kind 'clip_choice' vào log_learning_events(p_events),
-- KHÔNG thêm round-trip khi tải trang.
--
-- Payload: {"kind":"clip_choice","lessonId":12,"tnId":"camungdt-01","choice":0..3|null,"correct":true|false|null,"at":"..."}
--   choice null = HS bấm "Chưa muốn đoán, xem luôn" (bỏ qua).
--
-- Thiết kế:
--   * Bảng riêng lesson_clip_choices, 1 dòng / (HS, tn_id) — chỉ giữ lần ĐẦU (unique + on conflict do nothing):
--     Dự đoán chỉ có nghĩa trước khi xem clip; xem lại/đoán lại sau đó là đã biết kết quả. Gửi lặp vô hại.
--     tn_id là mã khung (data.id trong JSON khung), coi như duy nhất toàn site; lesson_id lưu theo lần đầu.
--   * Kiểm: tnId ~ '^[a-z0-9-]{1,60}$'; lessonId số nguyên và bài phải tồn tại (kiểm trước insert để một
--     sự kiện sai KHÔNG làm cả lô rơi vào nhánh foreign_key_violation → return 0); choice là số JSON 0..3
--     hoặc null; correct là boolean JSON hoặc null; choice null thì ép correct = null. Sai là bỏ sự kiện đó.
--   * Tài khoản staff (is_staff: admin/GV/TA) xem thử bài thì KHÔNG ghi, như read_depth.
--   * Giữ DB không phình: purge_lesson_clip_choices() xoá dòng > 12 tháng, pg_cron 3:45 VN ngày 1 hằng tháng
--     (hàm riêng, không sửa purge_learning_events). Sau khi xoá, lần chọn kế tiếp của HS được ghi lại như lần đầu.
--   * log_learning_events: create or replace từ bản mới nhất 20261018150000_read_depth_quiz.sql (không migration
--     nào sau đó thay hàm này — đã kiểm main + các nhánh claude/* 30/10/2026); nhánh read_depth và open/leave/submit
--     giữ nguyên từng dòng; chỉ thêm khai báo biến + nhánh 'clip_choice' trước nhánh read_depth.
--   * teacher_clip_choice_stats(p_class_id): số đếm theo tn_id cho HS đang active trong lớp, KHÔNG trả tên/id HS.
--
-- Ai đọc / ghi được gì:
--   | Vai                                   | lesson_clip_choices (đọc)               | Ghi                                             |
--   |---------------------------------------|-----------------------------------------|-------------------------------------------------|
--   | anon                                  | không                                   | không                                           |
--   | Học sinh                              | dòng của mình                           | chỉ qua log_learning_events, ép student_id = auth.uid(), lần đầu / tn_id |
--   | Giảng viên (class_instructors)        | HS các lớp mình dạy (teaches_student)   | không (is_staff → sự kiện bị bỏ)                |
--   | Trợ giảng đang hoạt động              | mọi HS (teaches_student, như learning_events) | không                                     |
--   | Admin                                 | tất cả                                  | không (trừ purge chạy bằng cron/postgres)       |
--   | teacher_clip_choice_stats(lớp)        | manages_class / assists_class / admin; chỉ số đếm, không tên HS | —                       |
--
-- Phụ thuộc: chạy SAU 20261018150000_read_depth_quiz (đã chạy). Chạy giờ nào cũng được (chỉ tạo bảng/hàm,
-- thay thân log_learning_events trong một giao dịch, không xoá dữ liệu). Rollback ở cuối file.

begin;

-- ---------- 1. Bảng ----------
create table if not exists public.lesson_clip_choices (
  student_id  uuid not null references public.profiles(id) on delete cascade,
  tn_id       text not null check (tn_id ~ '^[a-z0-9-]{1,60}$'),
  lesson_id   bigint not null references public.lessons(id) on delete cascade,
  choice      smallint check (choice is null or choice between 0 and 3),
  correct     boolean,
  occurred_at timestamptz not null default now(),
  primary key (student_id, tn_id),
  check (choice is not null or correct is null)
);
create index if not exists lesson_clip_choices_tn_idx on public.lesson_clip_choices (tn_id);
create index if not exists lesson_clip_choices_time_idx on public.lesson_clip_choices (occurred_at);

alter table public.lesson_clip_choices enable row level security;
revoke all on public.lesson_clip_choices from anon, authenticated;
grant select on public.lesson_clip_choices to authenticated;

drop policy if exists "hs xem du doan clip cua minh" on public.lesson_clip_choices;
create policy "hs xem du doan clip cua minh" on public.lesson_clip_choices
  as permissive for select to authenticated
  using (student_id = (select auth.uid()));

drop policy if exists "giao vien xem du doan clip cua lop" on public.lesson_clip_choices;
create policy "giao vien xem du doan clip cua lop" on public.lesson_clip_choices
  as permissive for select to authenticated
  using (public.teaches_student(student_id) or public.is_admin());

-- ---------- 2. log_learning_events: thêm nhánh clip_choice ----------
-- p_events (cũ, giữ nguyên): {"lessonId":12,"itemId":34,"kind":"open|leave|submit","durationS":45,"at":"..."}
--                            {"kind":"read_depth","itemId":34,"h3Max":3,"h3Total":5,"quizDone":1,"quizTotal":2,"at":"..."}
-- p_events (mới):            {"kind":"clip_choice","lessonId":12,"tnId":"camungdt-01","choice":2,"correct":false,"at":"..."}
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
  v_tn text;
  v_choice smallint;
  v_correct boolean;
begin
  if v_uid is null then
    raise exception 'Chưa đăng nhập' using errcode = '42501';
  end if;
  if p_events is null or jsonb_typeof(p_events) <> 'array' then
    return 0;
  end if;
  for v_e in select * from jsonb_array_elements(p_events) limit 50 loop
    v_kind := v_e ->> 'kind';

    if v_kind = 'clip_choice' then
      if v_staff is null then
        v_staff := public.is_staff();
      end if;
      continue when v_staff;
      v_tn := v_e ->> 'tnId';
      continue when v_tn is null or v_tn !~ '^[a-z0-9-]{1,60}$';
      continue when coalesce(v_e ->> 'lessonId', '') !~ '^[0-9]{1,18}$';
      v_lesson := (v_e ->> 'lessonId')::bigint;
      continue when not exists (select 1 from public.lessons l where l.id = v_lesson);
      -- choice: số JSON 0..3 hoặc null/thiếu (bỏ qua). Chuỗi "2", 1.5, 4 → bỏ sự kiện.
      if v_e -> 'choice' is null or jsonb_typeof(v_e -> 'choice') = 'null' then
        v_choice := null;
      elsif jsonb_typeof(v_e -> 'choice') = 'number' and (v_e ->> 'choice') in ('0', '1', '2', '3') then
        v_choice := (v_e ->> 'choice')::smallint;
      else
        continue;
      end if;
      -- correct: boolean JSON hoặc null; bỏ qua (choice null) thì luôn null.
      if v_choice is null or v_e -> 'correct' is null or jsonb_typeof(v_e -> 'correct') = 'null' then
        v_correct := null;
      elsif jsonb_typeof(v_e -> 'correct') = 'boolean' then
        v_correct := (v_e -> 'correct')::boolean;
      else
        continue;
      end if;
      begin
        v_at := (v_e ->> 'at')::timestamptz;
      exception when others then
        v_at := null;
      end;
      if v_at is null or v_at > now() + interval '5 minutes' or v_at < now() - interval '1 day' then
        v_at := now();
      end if;
      insert into public.lesson_clip_choices (student_id, tn_id, lesson_id, choice, correct, occurred_at)
      values (v_uid, v_tn, v_lesson, v_choice, v_correct, v_at)
      on conflict (student_id, tn_id) do nothing;
      v_n := v_n + 1;
      continue;
    end if;

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

-- ---------- 3. Xoá dữ liệu > 12 tháng ----------
create or replace function public.purge_lesson_clip_choices(p_before timestamptz default (now() - interval '12 months'))
returns bigint
language plpgsql security definer set search_path = public
as $$
declare
  v_n bigint;
begin
  delete from public.lesson_clip_choices where occurred_at < p_before;
  get diagnostics v_n = row_count;
  return v_n;
end;
$$;
revoke all on function public.purge_lesson_clip_choices(timestamptz) from public, anon, authenticated;

-- ---------- 4. RPC cho GV/TA: số đếm theo khung (tn_id), không tên HS ----------
-- Chỉ tính HS đang active trong lớp. Thứ tự lựa chọn 0..3 = A..D như client hiển thị.
create or replace function public.teacher_clip_choice_stats(p_class_id bigint)
returns table (
  tn_id          text,
  lesson_id      bigint,   -- bài của lần ghi gần nhất (tn_id coi như duy nhất toàn site)
  class_students int,      -- số HS active trong lớp (mẫu số)
  n              int,      -- số HS đã tới điểm dừng (chọn + bỏ qua)
  n_chon         int,
  n_bo_qua       int,
  n_a            int,
  n_b            int,
  n_c            int,
  n_d            int,
  n_dung         int,
  last_at        timestamptz
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
  ), src as (
    select c.tn_id, c.lesson_id, c.choice, c.correct, c.occurred_at
    from public.lesson_clip_choices c
    join st on st.user_id = c.student_id
  )
  select s.tn_id,
         (array_agg(s.lesson_id order by s.occurred_at desc))[1],
         (select count(*)::int from st),
         count(*)::int,
         count(s.choice)::int,
         count(*) filter (where s.choice is null)::int,
         count(*) filter (where s.choice = 0)::int,
         count(*) filter (where s.choice = 1)::int,
         count(*) filter (where s.choice = 2)::int,
         count(*) filter (where s.choice = 3)::int,
         count(*) filter (where s.correct)::int,
         max(s.occurred_at)
  from src s
  group by s.tn_id
  order by s.tn_id;
end;
$$;
revoke all on function public.teacher_clip_choice_stats(bigint) from public, anon;
grant execute on function public.teacher_clip_choice_stats(bigint) to authenticated;

commit;

-- ---------- 5. Lịch pg_cron (ngoài giao dịch, như 20261017230000) ----------
do $$
begin
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'lesson-clip-choices-purge';
    perform cron.schedule('lesson-clip-choices-purge', '45 20 1 * *', 'select public.purge_lesson_clip_choices();');
    raise notice 'Đã đặt lịch pg_cron lesson-clip-choices-purge (3:45 VN ngày 1 hằng tháng)';
  else
    raise notice 'pg_cron chưa bật: chạy tay select public.purge_lesson_clip_choices(); mỗi học kì';
  end if;
end $$;

-- ---------- KIỂM THỬ (chạy trong giao dịch rồi rollback; thay <...> bằng id thật) ----------
-- begin;
--   -- Học sinh: kỳ vọng trả 2 (1 open + 1 clip_choice hợp lệ); 4 sự kiện sai bị bỏ êm, không làm rơi cả lô
--   set local role authenticated;
--   select set_config('request.jwt.claims', '{"sub":"<uuid_hs>","role":"authenticated"}', true);
--   select public.log_learning_events('[
--     {"kind":"open","lessonId":<lesson>,"itemId":<item_lt>},
--     {"kind":"clip_choice","lessonId":<lesson>,"tnId":"thu-nghiem-01","choice":2,"correct":false},
--     {"kind":"clip_choice","lessonId":<lesson>,"tnId":"Thu Nghiem","choice":1,"correct":true},
--     {"kind":"clip_choice","lessonId":<lesson>,"tnId":"thu-nghiem-02","choice":4,"correct":true},
--     {"kind":"clip_choice","lessonId":<lesson>,"tnId":"thu-nghiem-03","choice":"1","correct":true},
--     {"kind":"clip_choice","lessonId":999999999999,"tnId":"thu-nghiem-04","choice":1,"correct":true}
--   ]'::jsonb);
--   -- Lần sau cùng tn_id: trả 1 nhưng KHÔNG ghi đè (giữ lần đầu choice=2)
--   select public.log_learning_events('[{"kind":"clip_choice","lessonId":<lesson>,"tnId":"thu-nghiem-01","choice":0,"correct":true}]');
--   -- Bỏ qua kèm correct=true: correct bị ép null
--   select public.log_learning_events('[{"kind":"clip_choice","lessonId":<lesson>,"tnId":"thu-nghiem-05","choice":null,"correct":true}]');
--   select tn_id, choice, correct from public.lesson_clip_choices;          -- kỳ vọng (thu-nghiem-01,2,false), (thu-nghiem-05,null,null), chỉ của HS này
--   select * from public.teacher_clip_choice_stats(<class>);                -- kỳ vọng lỗi 42501
--   insert into public.lesson_clip_choices (student_id, tn_id, lesson_id) values ('<uuid_hs>', 'x', <lesson>); -- kỳ vọng permission denied
--   -- Trợ giảng (ta_assistants.active): đọc được, ghi bị bỏ (is_staff)
--   select set_config('request.jwt.claims', '{"sub":"<uuid_tro_giang>","role":"authenticated"}', true);
--   select count(*) from public.lesson_clip_choices;                         -- kỳ vọng >= 2
--   select * from public.teacher_clip_choice_stats(<class_cua_hs>);          -- kỳ vọng thu-nghiem-01: n=1,n_chon=1,n_c=1,n_dung=0; không có cột tên/id HS
--   select public.log_learning_events('[{"kind":"clip_choice","lessonId":<lesson>,"tnId":"thu-nghiem-09","choice":1,"correct":true}]'); -- kỳ vọng 0
--   -- Giảng viên lớp khác (không manages/assists): kỳ vọng lỗi 42501
--   select set_config('request.jwt.claims', '{"sub":"<uuid_gv_lop_khac>","role":"authenticated"}', true);
--   select * from public.teacher_clip_choice_stats(<class_cua_hs>);
--   -- Admin: đọc tất cả, RPC chạy cho mọi lớp
--   select set_config('request.jwt.claims', '{"sub":"<uuid_admin>","role":"authenticated"}', true);
--   select count(*) from public.lesson_clip_choices;
--   select * from public.teacher_clip_choice_stats(<class_cua_hs>);
--   -- anon: không đọc được, không gọi được RPC
--   reset role; set local role anon;
--   select count(*) from public.lesson_clip_choices;                         -- kỳ vọng permission denied
-- rollback;

-- ---------- ROLLBACK ----------
-- do $$ begin
--   if exists (select 1 from pg_extension where extname = 'pg_cron') then
--     perform cron.unschedule(jobid) from cron.job where jobname = 'lesson-clip-choices-purge';
--   end if;
-- end $$;
-- drop function if exists public.teacher_clip_choice_stats(bigint);
-- drop function if exists public.purge_lesson_clip_choices(timestamptz);
-- -- log_learning_events: chạy lại khối create or replace function (mục 3) ở
-- --   supabase/migrations/20261018150000_read_depth_quiz.sql (nhánh clip_choice mất; client gửi clip_choice bị bỏ êm)
-- drop table if exists public.lesson_clip_choices;
