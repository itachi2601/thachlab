-- ============================================================
-- BTVN ôn tập tự động sau khi chữa đề trên lớp (trình chiếu chữa bài)
-- Nguồn: docs/supabase-migration-class-review-homework.sql — xem file đó để biết lý do thiết kế.
-- Idempotent — chạy lại được.
-- ============================================================

create table if not exists public.class_review_homework (
  id bigint generated always as identity primary key,
  class_id bigint not null references public.classes (id) on delete cascade,
  source_exam_id bigint references public.exams (id) on delete set null,
  exam_id bigint not null references public.exams (id) on delete cascade,
  title text not null check (length(trim(title)) > 0),
  wrong_count int not null default 0,
  bank_count int not null default 0,
  created_by uuid not null references public.profiles (id) on delete cascade,
  created_at timestamptz not null default now()
);
create index if not exists class_review_homework_class_idx
  on public.class_review_homework (class_id, created_at desc);
create unique index if not exists class_review_homework_exam_idx
  on public.class_review_homework (exam_id);

alter table public.class_review_homework enable row level security;

drop policy if exists "staff create review homework" on public.class_review_homework;
create policy "staff create review homework" on public.class_review_homework
  for insert to authenticated
  with check (
    created_by = auth.uid()
    and (public.manages_class(class_id) or public.assists_class(class_id) or public.is_admin())
  );

drop policy if exists "staff read review homework" on public.class_review_homework;
create policy "staff read review homework" on public.class_review_homework
  for select to authenticated
  using (public.manages_class(class_id) or public.assists_class(class_id) or public.is_admin());

drop policy if exists "staff delete review homework" on public.class_review_homework;
create policy "staff delete review homework" on public.class_review_homework
  for delete to authenticated
  using (public.manages_class(class_id) or public.assists_class(class_id) or public.is_admin());

drop policy if exists "students read class review homework" on public.class_review_homework;
create policy "students read class review homework" on public.class_review_homework
  for select to authenticated
  using (exists (
    select 1 from public.user_classes uc
    where uc.user_id = auth.uid() and uc.class_id = class_review_homework.class_id and uc.status = 'active'
  ));
