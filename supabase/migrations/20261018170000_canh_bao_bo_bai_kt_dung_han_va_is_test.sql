-- Cảnh báo "Bỏ bài KT" chỉ sinh khi đề đã QUÁ HẠN nộp, hoặc đề không có hạn mà >=50% HS thật của lớp đã nộp.
-- Trước đây: cứ published_at cách đây >= p_days (3-7 ngày) là tính "bỏ bài", kể cả đề Cuối kỳ chưa tới hạn,
-- và tính cả admin/giáo viên/tài khoản thử đã nằm trong user_classes.
-- Thêm: class_assessments.due_at (hạn nộp, null = không hạn); profiles.is_test (tài khoản thử, thay cho lọc theo tên).
-- Không đổi chữ ký hàm, UI cũ vẫn gọi được.

alter table public.class_assessments add column if not exists due_at timestamptz;
alter table public.profiles add column if not exists is_test boolean not null default false;

-- Gắn cờ tài khoản thử đang có (chạy một lần): email hs.test% hoặc tên có từ "test"/"anonymus".
-- Ca nhầm thì: update public.profiles set is_test = false where id = '...';
update public.profiles p set is_test = true
where p.is_test = false
  and (
    exists (select 1 from auth.users u where u.id = p.id and u.email like 'hs.test%@thachlab.local')
    or p.full_name ~* '\m(test|anonymus)\M'
  );

create or replace function public.sweep_missed_assessments(p_class bigint, p_days int default 7)
returns int
language plpgsql security definer set search_path = public
as $$
declare v_count int := 0; r record;
begin
  if not public.manages_class(p_class) then
    raise exception 'không có quyền với lớp này';
  end if;

  drop table if exists _miss;
  create temp table _miss on commit drop as
  with stu as (
    select uc.user_id as student_id
    from public.user_classes uc
    join public.profiles p on p.id = uc.user_id
    where uc.class_id = p_class and uc.status = 'active'
      and p.role = 'student' and not p.is_test
  ),
  n_stu as (select count(*)::numeric as n from stu),
  asm as (
    select ca.*,
      (select count(distinct er.student_id) from public.exam_results er
        join stu s on s.student_id = er.student_id where er.exam_id = ca.exam_id)::numeric as n_done
    from public.class_assessments ca
    where ca.class_id = p_class
  ),
  due as (
    select a.* from asm a, n_stu
    where (a.due_at is not null and a.due_at < now())
       or (a.due_at is null and n_stu.n > 0 and a.n_done / n_stu.n >= 0.5)
  )
  select s.student_id,
         array_agg(d.id) as ids,
         string_agg(
           (case d.kind when 'giua_ki' then 'Giữa kỳ' when 'cuoi_ki' then 'Cuối kỳ'
                        when 'chuong' then 'KT chương' else 'KT thường xuyên' end)
           || coalesce(' ' || nullif(d.term, ''), ''), ' · ') as labels
  from stu s
  join due d on true
  where not exists (
    select 1 from public.exam_results er where er.student_id = s.student_id and er.exam_id = d.exam_id
  )
  group by s.student_id;

  for r in select * from _miss loop
    insert into public.student_alerts
      (student_id, class_id, kind, severity, reason, assessment_ids, status)
    values (
      r.student_id, p_class, 'missed_assessment',
      case when array_length(r.ids, 1) >= 2 then 'urgent' else 'warning' end,
      'Chưa làm ' || array_length(r.ids, 1) || ' bài kiểm tra: ' || r.labels,
      r.ids, 'open'
    )
    on conflict (student_id, kind) do update set
      severity = excluded.severity,
      reason = excluded.reason,
      assessment_ids = excluded.assessment_ids,
      -- chỉ mở lại cảnh báo đã đóng/bỏ qua khi tập bài thiếu thay đổi (trước đây mỗi lần rà đều mở lại)
      status = case when student_alerts.status in ('resolved', 'dismissed')
                         and student_alerts.assessment_ids is distinct from excluded.assessment_ids
                    then 'open' else student_alerts.status end,
      updated_at = now();
    v_count := v_count + 1;
  end loop;

  -- tự đóng cảnh báo mở không còn đúng luật (chưa tới hạn, đã nộp, hoặc không còn là HS thật)
  update public.student_alerts sa
    set status = 'resolved', updated_at = now(),
        handled_note = case when sa.handled_note = '' or sa.handled_note is null
                            then 'tự đóng: chưa tới hạn / đã nộp' else sa.handled_note end
  where sa.kind = 'missed_assessment' and sa.class_id = p_class and sa.status = 'open'
    and not exists (select 1 from _miss m where m.student_id = sa.student_id);

  return v_count;
end;
$$;

grant execute on function public.sweep_missed_assessments(bigint, int) to authenticated;

-- ROLLBACK:
--   1. Chạy lại thân hàm sweep_missed_assessments trong docs/supabase-migration-exam-analytics.sql (dòng ~335-382).
--   2. alter table public.profiles drop column if exists is_test;
--      alter table public.class_assessments drop column if exists due_at;
