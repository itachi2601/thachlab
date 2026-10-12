-- Lớp avcn vào tự do (không ai có dòng user_classes) nhưng đề luyện tập 914 gắn exam_classes → lớp avcn,
-- nên RLS "students only see own-class exams" chặn học sinh đã đăng nhập: mục Luyện tập của Chapter 8 mất đề
-- và trang quay về Lý thuyết. Gỡ gắn lớp = đề toàn trường (đúng như các đề THPT vào tự do). Idempotent.
begin;
create table if not exists public._bak_exam_classes_avcn_20261013 as select * from public.exam_classes where false;
alter table public._bak_exam_classes_avcn_20261013 enable row level security;
revoke all on public._bak_exam_classes_avcn_20261013 from anon, authenticated;
insert into public._bak_exam_classes_avcn_20261013
  select ec.* from public.exam_classes ec where ec.exam_id = 914 and ec.class_id = (select id from public.classes where slug = 'avcn');
delete from public.exam_classes where exam_id = 914 and class_id = (select id from public.classes where slug = 'avcn');
commit;
-- ROLLBACK: insert into public.exam_classes select * from public._bak_exam_classes_avcn_20261013 on conflict do nothing;
