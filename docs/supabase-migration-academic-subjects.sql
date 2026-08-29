-- Thêm tầng môn học cho nội dung phổ thông.
-- Idempotent; chạy sau supabase-migration-lessons.sql.

create table if not exists public.academic_subjects (
  code text primary key,
  label text not null,
  icon text not null default '',
  sort_order int not null default 0,
  active boolean not null default true
);

insert into public.academic_subjects (code, label, icon, sort_order) values
  ('vat-ly', 'Vật lý', '⚡', 1),
  ('hoa-hoc', 'Hóa học', '🧪', 2),
  ('sinh-hoc', 'Sinh học', '🧬', 3)
on conflict (code) do update set
  label = excluded.label,
  icon = excluded.icon,
  sort_order = excluded.sort_order;

alter table public.chapters add column if not exists subject_code text;
alter table public.exams add column if not exists subject_code text;
alter table public.posts add column if not exists subject_code text;

update public.chapters set subject_code = 'vat-ly' where subject_code is null;
update public.exams set subject_code = 'vat-ly' where subject_code is null;
update public.posts set subject_code = 'vat-ly' where subject_code is null;

alter table public.chapters alter column subject_code set default 'vat-ly';
alter table public.chapters alter column subject_code set not null;
alter table public.exams alter column subject_code set default 'vat-ly';
alter table public.exams alter column subject_code set not null;
alter table public.posts alter column subject_code set default 'vat-ly';
alter table public.posts alter column subject_code set not null;

do $$ begin
  alter table public.chapters add constraint chapters_subject_code_fkey
    foreign key (subject_code) references public.academic_subjects(code);
exception when duplicate_object then null; end $$;
do $$ begin
  alter table public.exams add constraint exams_subject_code_fkey
    foreign key (subject_code) references public.academic_subjects(code);
exception when duplicate_object then null; end $$;
do $$ begin
  alter table public.posts add constraint posts_subject_code_fkey
    foreign key (subject_code) references public.academic_subjects(code);
exception when duplicate_object then null; end $$;

alter table public.academic_subjects enable row level security;
drop policy if exists "anyone reads academic subjects" on public.academic_subjects;
create policy "anyone reads academic subjects" on public.academic_subjects
  for select using (active or public.is_admin());
drop policy if exists "admin manages academic subjects" on public.academic_subjects;
create policy "admin manages academic subjects" on public.academic_subjects
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

create index if not exists chapters_subject_code_idx on public.chapters(subject_code);
create index if not exists exams_subject_code_idx on public.exams(subject_code);
create index if not exists posts_subject_code_idx on public.posts(subject_code);
