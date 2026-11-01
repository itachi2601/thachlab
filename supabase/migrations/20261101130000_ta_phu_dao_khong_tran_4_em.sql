-- Trợ giảng được điền tên phụ đạo hơn 4 em/buổi; hệ số lương vẫn dừng ở mức 3+ em (×1,3 từ 11/2026, ×1,2 tháng 10).
-- Chỉ đổi trigger ta_policy_session_guard: bỏ chặn n>4 (vẫn cần ≥1 em, tên không trống/trùng, phiếu từng em khớp).
-- ta_monthly_policy đã tính "<=2 em → hệ số thấp, còn lại → hệ số cao" nên không phải sửa.
-- Chạy lúc nào cũng được (chỉ thay 1 hàm). Rollback: chạy lại hàm trong docs/supabase-migration-ta-policy-oct2026.sql (dòng 40–).
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
   if n<1 then raise exception 'Buổi phụ đạo phải có ít nhất 1 em'; end if;
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
