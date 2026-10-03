-- ============================================================================
-- Phụ đạo — bài kiểm tra cuối buổi: học sinh tự làm trên tài khoản của mình trong cửa sổ
-- thời gian do trợ giảng mở (không đưa máy), điểm phụ đạo 25đ tính theo TỈ LỆ NHÓM đạt.
--
--  1. tutoring_exit_windows: trợ giảng mở cửa sổ 20 phút cho 1–4 em, theo các chủ đề đã dạy.
--  2. tutoring_exit_attempts.window_id: lượt làm trong cửa sổ. Trong cửa sổ: 10 câu, đạt từ 70%,
--     mỗi em/chủ đề 1 lượt/cửa sổ, KHÔNG áp thời gian chờ 24 giờ. Ngoài cửa sổ (tự kiểm tra
--     thoát phụ đạo như cũ): 80%, chờ 24 giờ, KHÔNG được tính vào điểm trợ giảng.
--  3. ta_monthly_policy: điểm phụ đạo mỗi buổi = 25đ nếu >= 60% cặp (em, chủ đề đã dạy) đạt
--     trong cửa sổ của chính trợ giảng đó ngay ngày ghi buổi; 12,5đ nếu 40–59%; 0đ nếu < 40%.
--     (các điều kiện khác — nắm bài trước, hỏi từng em, phiếu đủ — giữ nguyên.)
--
-- Chạy trong giờ nào cũng được (chỉ thêm bảng/cột, thay hàm). Không ảnh hưởng tháng đã chốt.
-- Rollback: perf/rollback/20261003150000_phu_dao_kiem_tra_cuoi_buoi.down.sql
-- ============================================================================
begin;

-- ---------- 1. Cửa sổ kiểm tra cuối buổi ----------
create table if not exists public.tutoring_exit_windows (
  id uuid primary key default gen_random_uuid(),
  assistant_id uuid not null references public.ta_assistants (id) on delete cascade,
  class_id bigint,
  student_ids uuid[] not null,
  topic_ids bigint[] not null,
  opened_at timestamptz not null default now(),
  closes_at timestamptz not null default now() + interval '20 minutes',
  created_at timestamptz not null default now(),
  check (cardinality(student_ids) between 1 and 4),
  check (cardinality(topic_ids) >= 1)
);
create index if not exists tutoring_exit_windows_assistant_idx
  on public.tutoring_exit_windows (assistant_id, opened_at desc);

-- Giờ mở/đóng do máy chủ đặt, client không tự khai.
create or replace function public.tutoring_exit_window_defaults()
returns trigger language plpgsql as $$
begin
  new.opened_at := now();
  new.closes_at := now() + interval '20 minutes';
  return new;
end; $$;
drop trigger if exists trg_tutoring_exit_window_defaults on public.tutoring_exit_windows;
create trigger trg_tutoring_exit_window_defaults before insert on public.tutoring_exit_windows
  for each row execute function public.tutoring_exit_window_defaults();

alter table public.tutoring_exit_windows enable row level security;

drop policy if exists "ta opens own exit window" on public.tutoring_exit_windows;
create policy "ta opens own exit window" on public.tutoring_exit_windows
  for insert to authenticated
  with check (assistant_id = public.ta_current_assistant_id());

drop policy if exists "read exit windows" on public.tutoring_exit_windows;
create policy "read exit windows" on public.tutoring_exit_windows
  for select to authenticated
  using (
    public.is_admin()
    or assistant_id = public.ta_current_assistant_id()
    or auth.uid() = any (student_ids)
  );

-- ---------- 2. Lượt làm trong cửa sổ ----------
alter table public.tutoring_exit_attempts
  add column if not exists window_id uuid references public.tutoring_exit_windows (id) on delete set null;
create unique index if not exists tutoring_exit_attempts_window_need_uniq
  on public.tutoring_exit_attempts (window_id, tutoring_need_id) where window_id is not null;

-- Trợ giảng đọc được lượt của các em trong cửa sổ mình mở (RLS cũ chỉ cho em + người dạy em).
drop policy if exists "ta reads own window attempts" on public.tutoring_exit_attempts;
create policy "ta reads own window attempts" on public.tutoring_exit_attempts
  for select to authenticated
  using (
    window_id is not null
    and exists (
      select 1 from public.tutoring_exit_windows w
      where w.id = tutoring_exit_attempts.window_id
        and (w.assistant_id = public.ta_current_assistant_id() or public.is_admin())
    )
  );

create or replace function public.tutoring_exit_attempt_guard()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  v_need public.tutoring_needs%rowtype;
  v_win public.tutoring_exit_windows%rowtype;
  v_last timestamptz;
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

  new.topic_id := v_need.topic_id;
  new.form := v_need.form;
  new.pct := round(new.correct * 100.0 / new.total)::int;
  new.passed := new.pct >= 80;
  return new;
end; $$;

-- ---------- 3. Tỉ lệ nhóm đạt của một buổi phụ đạo ----------
-- Cặp (em, chủ đề đã dạy trong buổi) tính là đạt nếu có lượt passed trong cửa sổ do CHÍNH
-- trợ giảng mở, mở đúng ngày ghi buổi (giờ Việt Nam). Chỉ tính chủ đề nằm trong danh sách hổng của em
-- (có dòng tutoring_needs). Trả null nếu buổi chưa ghi chủ đề nào như vậy.
create or replace function public.ta_tutoring_pass_ratio(p_session uuid)
returns numeric language sql stable security definer set search_path = public as $$
  select case when count(*) = 0 then null
    else count(*) filter (where ok)::numeric / count(*) end
  from (
    select exists (
      select 1
      from public.tutoring_exit_attempts ea
      join public.tutoring_exit_windows w on w.id = ea.window_id
      where ea.student_id = tst.student_id
        and ea.topic_id = tst.topic_id
        and ea.passed
        and w.assistant_id = s.assistant_id
        and (w.opened_at at time zone 'Asia/Ho_Chi_Minh')::date = s.work_date
    ) as ok
    from public.ta_sessions s
    join public.tutoring_session_topics tst on tst.session_id = s.id
    where s.id = p_session
      -- chủ đề dạy thêm ngoài danh sách hổng của em không có bài để làm -> không đưa vào mẫu số
      and exists (select 1 from public.tutoring_needs n
                  where n.student_id = tst.student_id and n.topic_id = tst.topic_id)
  ) t;
$$;
revoke all on function public.ta_tutoring_pass_ratio(uuid) from public, anon;
grant execute on function public.ta_tutoring_pass_ratio(uuid) to authenticated;

-- ---------- 4. Điểm phụ đạo theo tỉ lệ nhóm ----------
create or replace function public.ta_monthly_policy(p_assistant_id uuid,p_month date) returns jsonb
language plpgsql stable security definer set search_path=public as $$
declare
 m date:=date_trunc('month',p_month)::date;
 r public.ta_month_reviews%rowtype;
 a public.ta_assistants%rowtype;
 x record; result jsonb; missing text[]:='{}';
 ts numeric; ps numeric; hs numeric; ats numeric; obs numeric; total numeric; rate numeric; factor numeric;
begin
 if not public.is_admin() and p_assistant_id is distinct from public.ta_current_assistant_id() then raise exception 'Không có quyền xem trợ giảng này'; end if;
 if m<date '2026-10-01' then raise exception 'Dùng bảng lịch sử cho tháng trước 10/2026'; end if;
 select * into a from public.ta_assistants where id=p_assistant_id;
 if not found then raise exception 'Không tìm thấy trợ giảng'; end if;
 select * into r from public.ta_month_reviews where assistant_id=p_assistant_id and month=m;
 if r.closed_at is not null and r.snapshot is not null then return r.snapshot||jsonb_build_object('closed_at',r.closed_at); end if;
 select coalesce(r.hourly_rate,a.retained_rate,(select base_rate from public.ta_rates where tier=a.tier and effective_from<=m order by effective_from desc limit 1)) into rate;
 with s as(select * from public.ta_sessions where assistant_id=p_assistant_id and work_date>=m and work_date<m+interval '1 month'),
 approved as(select * from s where status='approved')
 select
  count(*) filter(where session_type='lop') as class_count,
  count(*) filter(where session_type='phudao') as tutoring_count,
  (select count(*) from s where status='submitted') as pending_count,
  coalesce(avg(least(1,greatest(0,student_touches)/12.0)) filter(where session_type='lop' and policy->>'attendance' not in ('excused_absence','unexcused_absence')),0)*30 as touch_points,
  avg(case when coalesce((policy->>'prepared')::boolean,false) and coalesce((policy->>'asked_each')::boolean,false)
   and not exists(select 1 from jsonb_array_elements(coalesce(policy->'followups','[]')) f where nullif(trim(f->>'lesson'),'') is null or nullif(trim(f->>'difficulty'),'') is null)
   then case when coalesce(public.ta_tutoring_pass_ratio(approved.id),0) >= 0.6 then 25.0
             when coalesce(public.ta_tutoring_pass_ratio(approved.id),0) >= 0.4 then 12.5
             else 0 end
   else 0 end) filter(where session_type='phudao') as tutoring_points,
  coalesce(avg(case when coalesce((policy->>'homework_checked')::boolean,false) then 20.0 else 0 end) filter(where session_type='lop' and policy->>'attendance' not in ('excused_absence','unexcused_absence')),0) as homework_points,
  coalesce(avg(case when policy->>'attendance'='on_time' then 15.0 else 0 end) filter(where session_type='lop' and policy->>'attendance'<>'excused_absence'),0) as attendance_points,
  coalesce(sum(hours-coalesce((policy->>'teaching_minutes')::numeric,0)/60) filter(where session_type='lop' and policy->>'attendance' not in ('excused_absence','unexcused_absence')),0) as class_hours,
  coalesce(sum(coalesce((policy->>'teaching_minutes')::numeric,0)/60) filter(where session_type='lop' and policy->>'attendance' not in ('excused_absence','unexcused_absence')),0) as teaching_hours,
  coalesce(sum(hours*case when cardinality(phudao_students)<=2 then 1.2 else 1.4 end) filter(where session_type='phudao'),0) as tutoring_weighted_hours,
  coalesce(sum(hours) filter(where session_type='phudao'),0) as tutoring_hours,
  coalesce(sum(papers_graded) filter(where session_type='chambai'),0) as papers
 into x from approved;
 ts:=coalesce((r.scores->>'touches')::numeric,x.touch_points);
 ps:=coalesce((r.scores->>'phudao')::numeric,x.tutoring_points);
 hs:=coalesce((r.scores->>'homework')::numeric,x.homework_points);
 ats:=coalesce((r.scores->>'attendance')::numeric,x.attendance_points);
 obs:=(r.scores->>'observation')::numeric;
 if ps is null then missing:=array_append(missing,'Thầy nhập điểm phụ đạo (tháng không có buổi phụ đạo)'); end if;
 if obs is null then missing:=array_append(missing,'Thầy nhập điểm quan sát'); end if;
 if rate is null or rate<=0 then missing:=array_append(missing,'Thầy nhập đơn giá giờ'); end if;
 if x.pending_count>0 then missing:=array_append(missing,'Còn buổi chờ duyệt'); end if;
 total:=round(ts,2)+round(ps,2)+round(hs,2)+round(ats,2)+obs;
 factor:=case when m=date '2026-10-01' then 1.0 when total is null then null when total>=70 then 1.0 else 0.9 end;
 result:=jsonb_build_object('assistant_id',p_assistant_id,'month',m,'closed_at',null,'note',coalesce(r.note,''),'overrides',coalesce(r.scores,'{}'),
  'class_count',x.class_count,'tutoring_count',x.tutoring_count,'pending_count',x.pending_count,
  'touches',round(ts,2),'phudao',round(ps,2),'homework',round(hs,2),'attendance',round(ats,2),'observation',obs,'total_score',round(total,2),
  'hourly_rate',rate,'class_factor',factor,'class_hours',x.class_hours,'teaching_hours',x.teaching_hours,'tutoring_hours',x.tutoring_hours,
  'tutoring_weighted_hours',x.tutoring_weighted_hours,'papers',x.papers,
  'class_pay',round(x.class_hours*rate*factor),'teaching_pay',round(x.teaching_hours*rate*1.6),'tutoring_pay',round(x.tutoring_weighted_hours*rate),
  'grading_pay',x.papers*1500,'total_pay',round(x.class_hours*rate*factor)+round(x.teaching_hours*rate*1.6)+round(x.tutoring_weighted_hours*rate)+x.papers*1500,
  'missing',to_jsonb(missing),'trial',m=date '2026-10-01');
 return result;
end; $$;
revoke all on function public.ta_monthly_policy(uuid,date) from public,anon;
grant execute on function public.ta_monthly_policy(uuid,date) to authenticated;

commit;

-- ROLLBACK: xem perf/rollback/20261003150000_phu_dao_kiem_tra_cuoi_buoi.down.sql
