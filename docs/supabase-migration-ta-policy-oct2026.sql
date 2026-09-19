-- Quy chế Phần A từ 01/10/2026. Chạy SAU các migration trợ giảng hiện có.
-- Không sửa ta_monthly_score/ta_converted_hours cũ: lịch sử trước 10/2026 giữ nguyên.
begin;
create or replace function public.ta_policy_today() returns date language sql stable set search_path=public as $$ select (now() at time zone 'Asia/Ho_Chi_Minh')::date $$;
revoke all on function public.ta_policy_today() from public,anon,authenticated;
alter table public.ta_sessions add column if not exists policy jsonb not null default '{}'::jsonb;
create table if not exists public.ta_month_reviews (
 assistant_id uuid not null references public.ta_assistants(id),
 month date not null check (month >= date '2026-10-01' and extract(day from month)=1),
 scores jsonb not null default '{}'::jsonb,
 hourly_rate integer check(hourly_rate > 0),
 note text not null default '',
 closed_at timestamptz,
 snapshot jsonb,
 updated_by uuid references auth.users(id),
 updated_at timestamptz not null default now(),
 primary key(assistant_id,month)
);
create table if not exists public.ta_policy_audit (
 id bigint generated always as identity primary key,
 assistant_id uuid not null,
 month date not null,
 actor_id uuid,
 action text not null,
 before_value jsonb,
 after_value jsonb,
 created_at timestamptz not null default now()
);
alter table public.ta_month_reviews enable row level security;
alter table public.ta_policy_audit enable row level security;
drop policy if exists ta_review_read on public.ta_month_reviews;
create policy ta_review_read on public.ta_month_reviews for select to authenticated
 using (public.is_admin() or assistant_id=public.ta_current_assistant_id());
drop policy if exists ta_audit_read on public.ta_policy_audit;
create policy ta_audit_read on public.ta_policy_audit for select to authenticated
 using (public.is_admin() or assistant_id=public.ta_current_assistant_id());
grant select on public.ta_month_reviews, public.ta_policy_audit to authenticated;
revoke insert,update,delete on public.ta_month_reviews,public.ta_policy_audit from authenticated,anon;

create or replace function public.ta_policy_session_guard() returns trigger
language plpgsql security definer set search_path=public as $$
declare m date; old_m date; n integer; mins numeric; p jsonb; k text;
begin
 m:=date_trunc('month',new.work_date)::date;
 if TG_OP='UPDATE' then
  old_m:=date_trunc('month',old.work_date)::date;
  if old.work_date>=date '2026-10-01' and new.work_date<date '2026-10-01' then raise exception 'Không chuyển công quy chế mới về tháng lịch sử'; end if;
  if old.assistant_id<>new.assistant_id then raise exception 'Không chuyển chủ sở hữu buổi làm việc'; end if;
 end if;
 -- Cùng khóa với thao tác chốt; khóa tháng theo thứ tự để tránh deadlock khi chuyển ngày.
 perform pg_advisory_xact_lock(hashtextextended(new.assistant_id::text||least(m,coalesce(old_m,m))::text,0));
 if old_m is not null and old_m<>m then
  perform pg_advisory_xact_lock(hashtextextended(new.assistant_id::text||greatest(m,old_m)::text,0));
 end if;
 if not public.is_admin() and exists(select 1 from public.ta_month_reviews r
   where r.assistant_id=new.assistant_id and r.month in (m,old_m) and r.closed_at is not null) then
  raise exception 'Tháng này đã chốt. Liên hệ thầy để điều chỉnh';
 end if;
 if new.work_date>=date '2026-10-01' then
  if new.session_type='hanhchinh' then raise exception 'Từ 01/10/2026 không ghi công hành chính'; end if;
  if new.work_date>public.ta_policy_today() then raise exception 'Chỉ ghi buổi đã diễn ra'; end if;
  if jsonb_typeof(new.policy)<>'object' then raise exception 'Phiếu không hợp lệ'; end if;
  p:=new.policy;
  if new.session_type in ('lop','phudao') and nullif(trim(new.class_label),'') is null then raise exception 'Cần ghi lớp'; end if;
  if new.session_type='lop' then
   foreach k in array array['arrived_early','homework_checked','walked_tables','reported_students'] loop
    if jsonb_typeof(p->k) is distinct from 'boolean' then raise exception 'Phiếu cần mục %',k; end if;
   end loop;
   if coalesce(new.student_touches,-1)<0 then raise exception 'Cần số lượt tiếp xúc không âm'; end if;
   if coalesce(p->>'attendance','') not in ('on_time','late','excused_absence','unexcused_absence') then raise exception 'Cần ghi chuyên cần'; end if;
   if coalesce(p->>'teaching_minutes','') !~ '^[0-9]+$' then raise exception 'Phút chữa bài phải là số nguyên không âm'; end if;
   mins:=(p->>'teaching_minutes')::numeric;
   if mins>extract(epoch from (new.end_time-new.start_time))/60 then raise exception 'Phút chữa bài vượt thời lượng buổi'; end if;
   if p->>'attendance' in ('excused_absence','unexcused_absence') and (mins>0 or new.student_touches>0) then raise exception 'Buổi vắng không ghi chữa bài hay lượt tiếp xúc'; end if;
   if mins>0 and nullif(trim(p->>'teaching_note'),'') is null then raise exception 'Ghi nội dung chữa bài thay thầy'; end if;
   if coalesce(p->>'homework_missing','') !~ '^[0-9]+$' then raise exception 'Số em chưa làm bài phải không âm'; end if;
  elsif new.session_type='phudao' then
   foreach k in array array['prepared','recalled','asked_each'] loop
    if jsonb_typeof(p->k) is distinct from 'boolean' then raise exception 'Phiếu cần mục %',k; end if;
   end loop;
   n:=cardinality(new.phudao_students);
   if n<1 or n>4 then raise exception 'Phụ đạo từ 1 đến 4 em mỗi buổi'; end if;
   if n<>(select count(distinct lower(trim(x))) from unnest(new.phudao_students) x where trim(x)<>'') then raise exception 'Tên em phụ đạo không được trống hoặc trùng'; end if;
   if jsonb_typeof(p->'followups') is distinct from 'array' or jsonb_array_length(p->'followups')<>n then raise exception 'Cần phiếu theo dõi cho từng em'; end if;
   for n in 1..cardinality(new.phudao_students) loop
    if jsonb_typeof(p->'followups'->(n-1)) is distinct from 'object'
      or p->'followups'->(n-1)->>'student' is distinct from new.phudao_students[n]
      or jsonb_typeof(p->'followups'->(n-1)->'lesson') is distinct from 'string'
      or jsonb_typeof(p->'followups'->(n-1)->'difficulty') is distinct from 'string'
      then raise exception 'Phiếu từng em không khớp danh sách phụ đạo'; end if;
   end loop;
  elsif new.session_type='chambai' and coalesce(new.papers_graded,0)<=0 then raise exception 'Số bài chấm phải lớn hơn 0';
  end if;
 end if;
 if public.is_admin() then
  -- Sửa công đã chốt sẽ mở lại tháng. Bản chốt cũ được giữ trong nhật ký.
  insert into public.ta_policy_audit(assistant_id,month,actor_id,action,before_value)
   select r.assistant_id,r.month,auth.uid(),'reopen_after_session_edit',r.snapshot
   from public.ta_month_reviews r where r.assistant_id=new.assistant_id and r.month in(m,old_m) and r.closed_at is not null;
  update public.ta_month_reviews r set closed_at=null,snapshot=null,updated_at=now(),updated_by=auth.uid()
   where r.assistant_id=new.assistant_id and r.month in(m,old_m) and r.closed_at is not null;
 end if;
 if m>=date '2026-10-01' or old_m>=date '2026-10-01' then
  insert into public.ta_policy_audit(assistant_id,month,actor_id,action,before_value,after_value)
   values(new.assistant_id,m,auth.uid(),lower(TG_OP)||'_session',case when TG_OP='UPDATE' then to_jsonb(old) else null end,to_jsonb(new));
 end if;
 return new;
end; $$;
drop trigger if exists ta_policy_session_guard on public.ta_sessions;
create trigger ta_policy_session_guard before insert or update on public.ta_sessions for each row execute function public.ta_policy_session_guard();
revoke all on function public.ta_policy_session_guard() from public,anon,authenticated;

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
  avg(case when coalesce((policy->>'prepared')::boolean,false) and coalesce((policy->>'recalled')::boolean,false) and coalesce((policy->>'asked_each')::boolean,false)
   and not exists(select 1 from jsonb_array_elements(coalesce(policy->'followups','[]')) f where nullif(trim(f->>'lesson'),'') is null or nullif(trim(f->>'difficulty'),'') is null)
   then 25.0 else 0 end) filter(where session_type='phudao') as tutoring_points,
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

create or replace function public.ta_save_month_review(p_assistant_id uuid,p_month date,p_scores jsonb,p_rate integer,p_note text,p_close boolean default false) returns jsonb
language plpgsql security definer set search_path=public as $$
declare m date:=date_trunc('month',p_month)::date; before_row jsonb; score jsonb; k text; v jsonb; maximum numeric;
begin
 if not public.is_admin() then raise exception 'Chỉ thầy được chấm và chốt tháng'; end if;
 if m<date '2026-10-01' then raise exception 'Không sửa lịch sử theo quy chế mới'; end if;
 if jsonb_typeof(p_scores) is distinct from 'object' then raise exception 'Điểm không hợp lệ'; end if;
 for k,v in select * from jsonb_each(p_scores) loop
  maximum:=case k when 'touches' then 30 when 'phudao' then 25 when 'homework' then 20 when 'attendance' then 15 when 'observation' then 10 else null end;
  if maximum is null or (v<>'null'::jsonb and (jsonb_typeof(v)<>'number' or v::numeric<0 or v::numeric>maximum)) then raise exception 'Điểm % không hợp lệ',k; end if;
 end loop;
 if nullif(trim(p_note),'') is null then raise exception 'Ghi lý do chấm/điều chỉnh'; end if;
 perform pg_advisory_xact_lock(hashtextextended(p_assistant_id::text||m::text,0));
 select to_jsonb(r) into before_row from public.ta_month_reviews r where assistant_id=p_assistant_id and month=m;
 insert into public.ta_month_reviews(assistant_id,month,scores,hourly_rate,note,updated_by)
 values(p_assistant_id,m,p_scores,p_rate,p_note,auth.uid())
 on conflict(assistant_id,month) do update set scores=excluded.scores,hourly_rate=excluded.hourly_rate,note=excluded.note,updated_by=auth.uid(),updated_at=now(),closed_at=null,snapshot=null;
 score:=public.ta_monthly_policy(p_assistant_id,m);
 if p_close then
  if m>date_trunc('month',public.ta_policy_today())::date then raise exception 'Không chốt tháng tương lai'; end if;
  if jsonb_array_length(score->'missing')>0 then raise exception 'Chưa thể chốt: %',score->'missing'; end if;
  update public.ta_month_reviews set closed_at=now(),snapshot=score where assistant_id=p_assistant_id and month=m;
 end if;
 insert into public.ta_policy_audit(assistant_id,month,actor_id,action,before_value,after_value)
 values(p_assistant_id,m,auth.uid(),case when p_close then 'close_month' else 'save_review' end,before_row,score);
 return public.ta_monthly_policy(p_assistant_id,m);
end; $$;
revoke all on function public.ta_save_month_review(uuid,date,jsonb,integer,text,boolean) from public,anon;
grant execute on function public.ta_save_month_review(uuid,date,jsonb,integer,text,boolean) to authenticated;
commit;
