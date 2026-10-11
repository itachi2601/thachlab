-- ============================================================================
-- Dọn các mục phụ đạo chỉ mở vì câu Khó (thầy duyệt 11/10/2026, đi cùng 20261011220000_phu_dao_bo_cau_kho)
-- Chỉ đóng mục status='open' (chưa ai nhận) mà: tính cả câu Khó thì đạt ngưỡng mở (>=3 câu, sai >=50%),
-- bỏ câu Khó thì không còn đạt. Mục assigned/tutored giữ nguyên. Đóng = 'cleared' + ghi chú; nếu em hổng thật
-- ở bài sau thì refresh_tutoring_needs tự mở lại như cũ. Cùng cửa sổ "2 bài gần nhất" như hàm chính.
-- Sao lưu trạng thái cũ vào tutoring_needs_backup_20261011 (RLS bật, không cấp quyền) để hoàn tác.
-- Cách chạy: bash scripts/run-migrations.sh — lúc nào cũng được (ghi một lần, không có trigger).
-- Rollback: perf/rollback/20261011230000_phu_dao_don_muc_chi_vi_cau_kho.down.sql
-- ============================================================================

create table if not exists public.tutoring_needs_backup_20261011 (
  id bigint primary key, status text, cleared_at timestamptz, note text
);
alter table public.tutoring_needs_backup_20261011 enable row level security;
revoke all on public.tutoring_needs_backup_20261011 from anon, authenticated;

create temp table _don_muc on commit drop as
with ranked as (
  select er.student_id, er.exam_id,
         row_number() over (partition by er.student_id order by max(er.created_at) desc) rn
  from public.exam_results er group by er.student_id, er.exam_id
), last_try as (
  select distinct on (er.student_id, er.exam_id) er.id
  from public.exam_results er
  join ranked r on r.student_id = er.student_id and r.exam_id = er.exam_id and r.rn <= 2
  order by er.student_id, er.exam_id, er.created_at desc
), agg as (
  select q.student_id, coalesce(t.parent_id, q.topic_id) as topic_id, coalesce(nullif(q.form, ''), '') as form,
         count(*) as total1, count(*) filter (where not q.is_correct) as wrong1,
         count(*) filter (where coalesce(q.difficulty, '') <> 'kho') as total2,
         count(*) filter (where coalesce(q.difficulty, '') <> 'kho' and not q.is_correct) as wrong2
  from public.exam_question_results q
  join last_try lt on lt.id = q.exam_result_id
  join public.question_topics t on t.id = q.topic_id
  where q.topic_id is not null
  group by 1, 2, 3
)
select n.id
from public.tutoring_needs n
join agg a on a.student_id = n.student_id and a.topic_id = n.topic_id and a.form = n.form
where n.status = 'open'
  and a.total1 >= 3 and a.wrong1 * 100.0 / a.total1 >= 50
  and (a.total2 < 3 or a.wrong2 * 100.0 / a.total2 < 50);

insert into public.tutoring_needs_backup_20261011 (id, status, cleared_at, note)
select n.id, n.status, n.cleared_at, n.note
from public.tutoring_needs n join _don_muc d on d.id = n.id
on conflict (id) do nothing;

update public.tutoring_needs n
set status = 'cleared', cleared_at = now(), last_seen_at = now(),
    note = 'không tính câu khó, chưa cần phụ đạo'
from _don_muc d
where n.id = d.id and n.status = 'open';
