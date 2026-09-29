-- Thay ô tự khai "Đã dò lại bài cũ" (recalled) trong điểm phụ đạo (25đ, ta_monthly_policy)
-- bằng bằng chứng khách quan: học sinh đã tự kiểm tra đạt (tutoring_exit_attempts.passed)
-- ngay trong ngày ghi buổi, cho đúng em/chủ đề đã tick "đã dạy" trong buổi đó
-- (tutoring_session_topics). "prepared" và "asked_each" vẫn tự khai — đó là việc của
-- trợ giảng, không có cách nào đo khách quan.
--
-- Chạy SAU: docs/supabase-migration-ta-policy-oct2026.sql, docs/supabase-migration-tutoring-needs.sql
-- (tutoring_session_topics), docs/supabase-migration-tutoring-exit-quiz.sql (tutoring_exit_attempts).
-- Idempotent — chạy lại được. Không ảnh hưởng tháng đã chốt (ta_monthly_policy trả thẳng
-- snapshot cho tháng closed_at is not null, không đụng tới hàm này).
--
-- Chưa có buổi phụ đạo nào thật sự tính theo công thức 01/10/2026 tại thời điểm viết
-- (hôm nay 25/9/2026) nên đổi công thức lúc này không làm sai lệch lương đã tính.
begin;

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
   and exists(select 1 from public.tutoring_session_topics tst
              join public.tutoring_exit_attempts ea on ea.student_id = tst.student_id and ea.topic_id = tst.topic_id
              where tst.session_id = approved.id and ea.passed and ea.created_at::date = approved.work_date)
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
commit;
