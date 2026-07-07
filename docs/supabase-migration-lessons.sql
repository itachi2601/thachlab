-- ============================================================
-- Migration v3: Chương → Bài học → Mục (lý thuyết/video/đề…)
-- Chạy SAU supabase-migration-classes.sql (idempotent, chạy lại được)
-- ============================================================

-- ---------- Chương (gán lớp qua M2M, không gán = toàn trường) ----------
create table if not exists public.chapters (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  title text not null,
  sort_order int not null default 0
);

create table if not exists public.chapter_classes (
  chapter_id bigint not null references public.chapters (id) on delete cascade,
  class_id bigint not null references public.classes (id) on delete cascade,
  primary key (chapter_id, class_id)
);

-- ---------- Bài học trong chương ----------
create table if not exists public.lessons (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  chapter_id bigint not null references public.chapters (id) on delete cascade,
  title text not null,
  sort_order int not null default 0,
  published boolean not null default true
);

-- ---------- Mục trong bài học (6 loại, theo thứ tự cố định §1–§6) ----------
create table if not exists public.lesson_items (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  lesson_id bigint not null references public.lessons (id) on delete cascade,
  kind text not null check (kind in
    ('ly_thuyet', 'video', 'bai_tap_mau', 'luyen_tap_sach', 'luyen_tap_de', 'kiem_tra')),
  title text not null,
  subtitle text not null default '',
  body_html text not null default '',   -- lý thuyết / bài tập mẫu (HTML + $LaTeX$)
  video_url text not null default '',   -- link YouTube
  pdf_url text not null default '',     -- link PDF (Supabase storage hoặc ngoài)
  exam_id bigint references public.exams (id) on delete set null, -- luyen_tap_de / kiem_tra
  sort_order int not null default 0
);

create index if not exists lesson_items_lesson_idx on public.lesson_items (lesson_id, sort_order);
create index if not exists lessons_chapter_idx on public.lessons (chapter_id, sort_order);

-- ---------- Tiến độ học (đã xem/đã làm từng mục) ----------
create table if not exists public.lesson_progress (
  user_id uuid not null references public.profiles (id) on delete cascade,
  item_id bigint not null references public.lesson_items (id) on delete cascade,
  done_at timestamptz not null default now(),
  primary key (user_id, item_id)
);

-- ---------- RLS ----------
alter table public.chapters enable row level security;
alter table public.chapter_classes enable row level security;
alter table public.lessons enable row level security;
alter table public.lesson_items enable row level security;
alter table public.lesson_progress enable row level security;

drop policy if exists "anyone reads chapters" on public.chapters;
create policy "anyone reads chapters" on public.chapters for select using (true);
drop policy if exists "admin manages chapters" on public.chapters;
create policy "admin manages chapters" on public.chapters
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "anyone reads chapter classes" on public.chapter_classes;
create policy "anyone reads chapter classes" on public.chapter_classes for select using (true);
drop policy if exists "admin manages chapter classes" on public.chapter_classes;
create policy "admin manages chapter classes" on public.chapter_classes
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "anyone reads published lessons" on public.lessons;
create policy "anyone reads published lessons" on public.lessons
  for select using (published or public.is_admin());
drop policy if exists "admin manages lessons" on public.lessons;
create policy "admin manages lessons" on public.lessons
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "anyone reads lesson items" on public.lesson_items;
create policy "anyone reads lesson items" on public.lesson_items for select using (true);
drop policy if exists "admin manages lesson items" on public.lesson_items;
create policy "admin manages lesson items" on public.lesson_items
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "student manages own progress" on public.lesson_progress;
create policy "student manages own progress" on public.lesson_progress
  for all to authenticated
  using (user_id = auth.uid() or public.is_admin())
  with check (user_id = auth.uid());

-- ---------- Số câu theo dạng (TN/ĐS/TLN) — cột generated như question_count ----------
create or replace function public.count_question_types(qs jsonb)
returns jsonb
language sql immutable
as $$
  select coalesce(jsonb_object_agg(t, n), '{}'::jsonb)
  from (
    select q ->> 'type' as t, count(*) as n
    from jsonb_array_elements(qs) as q
    group by 1
  ) s;
$$;

alter table public.exams add column if not exists type_counts jsonb
  generated always as (public.count_question_types(questions)) stored;
