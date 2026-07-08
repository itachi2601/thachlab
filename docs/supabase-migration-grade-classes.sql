-- ============================================================
-- Migration: Gom lớp theo khối KHTN 9, 10, 11, 12
-- Chạy SAU supabase-migration-classes.sql và supabase-migration-lessons.sql
-- Idempotent: chạy lại được.
-- ============================================================

insert into public.classes (name, slug, color, icon, sort_order, active) values
  ('KHTN 9', 'khtn-9', '#10B981', '🔬', 1, true),
  ('10', 'lop-10', '#22D3EE', '🎓', 2, true),
  ('11', 'lop-11', '#3B82F6', '🎓', 3, true),
  ('12', 'lop-12', '#8B5CF6', '🎓', 4, true)
on conflict (name) do update set
  slug = excluded.slug,
  color = excluded.color,
  icon = excluded.icon,
  sort_order = excluded.sort_order,
  active = true;

do $$
declare
  v_khtn9 bigint;
  v_10 bigint;
  v_11 bigint;
  v_12 bigint;
begin
  select id into v_khtn9 from public.classes where slug = 'khtn-9';
  select id into v_10 from public.classes where slug = 'lop-10';
  select id into v_11 from public.classes where slug = 'lop-11';
  select id into v_12 from public.classes where slug = 'lop-12';

  insert into public.exam_classes (exam_id, class_id)
  select ec.exam_id,
    case
      when c.name ~ '^10' or c.slug ~ '^10' then v_10
      when c.name ~ '^11' or c.slug ~ '^11' then v_11
      when c.name ~ '^12' or c.slug ~ '^12' then v_12
      when c.name in ('KHTN 9', 'KHTN9') or c.slug in ('khtn-9', 'khtn9') then v_khtn9
    end
  from public.exam_classes ec
  join public.classes c on c.id = ec.class_id
  where c.id not in (v_khtn9, v_10, v_11, v_12)
    and (
      c.name ~ '^(10|11|12)'
      or c.slug ~ '^(10|11|12)'
      or c.name in ('KHTN 9', 'KHTN9')
      or c.slug in ('khtn-9', 'khtn9')
    )
  on conflict do nothing;

  insert into public.post_classes (post_id, class_id)
  select pc.post_id,
    case
      when c.name ~ '^10' or c.slug ~ '^10' then v_10
      when c.name ~ '^11' or c.slug ~ '^11' then v_11
      when c.name ~ '^12' or c.slug ~ '^12' then v_12
      when c.name in ('KHTN 9', 'KHTN9') or c.slug in ('khtn-9', 'khtn9') then v_khtn9
    end
  from public.post_classes pc
  join public.classes c on c.id = pc.class_id
  where c.id not in (v_khtn9, v_10, v_11, v_12)
    and (
      c.name ~ '^(10|11|12)'
      or c.slug ~ '^(10|11|12)'
      or c.name in ('KHTN 9', 'KHTN9')
      or c.slug in ('khtn-9', 'khtn9')
    )
  on conflict do nothing;

  insert into public.user_classes (user_id, class_id)
  select uc.user_id,
    case
      when c.name ~ '^10' or c.slug ~ '^10' then v_10
      when c.name ~ '^11' or c.slug ~ '^11' then v_11
      when c.name ~ '^12' or c.slug ~ '^12' then v_12
      when c.name in ('KHTN 9', 'KHTN9') or c.slug in ('khtn-9', 'khtn9') then v_khtn9
    end
  from public.user_classes uc
  join public.classes c on c.id = uc.class_id
  where c.id not in (v_khtn9, v_10, v_11, v_12)
    and (
      c.name ~ '^(10|11|12)'
      or c.slug ~ '^(10|11|12)'
      or c.name in ('KHTN 9', 'KHTN9')
      or c.slug in ('khtn-9', 'khtn9')
    )
  on conflict do nothing;

  if to_regclass('public.chapter_classes') is not null then
    insert into public.chapter_classes (chapter_id, class_id)
    select cc.chapter_id,
      case
        when c.name ~ '^10' or c.slug ~ '^10' then v_10
        when c.name ~ '^11' or c.slug ~ '^11' then v_11
        when c.name ~ '^12' or c.slug ~ '^12' then v_12
        when c.name in ('KHTN 9', 'KHTN9') or c.slug in ('khtn-9', 'khtn9') then v_khtn9
      end
    from public.chapter_classes cc
    join public.classes c on c.id = cc.class_id
    where c.id not in (v_khtn9, v_10, v_11, v_12)
      and (
        c.name ~ '^(10|11|12)'
        or c.slug ~ '^(10|11|12)'
        or c.name in ('KHTN 9', 'KHTN9')
        or c.slug in ('khtn-9', 'khtn9')
      )
    on conflict do nothing;
  end if;

  update public.profiles set class_name = 'KHTN 9'
  where class_name in ('KHTN 9', 'KHTN9');
  update public.profiles set class_name = '10'
  where class_name ~ '^10' or class_name = 'Lớp 10';
  update public.profiles set class_name = '11'
  where class_name ~ '^11' or class_name = 'Lớp 11';
  update public.profiles set class_name = '12'
  where class_name ~ '^12' or class_name = 'Lớp 12';

  update public.messages set class_name = 'KHTN 9'
  where class_name in ('KHTN 9', 'KHTN9');
  update public.messages set class_name = '10'
  where class_name ~ '^10' or class_name = 'Lớp 10';
  update public.messages set class_name = '11'
  where class_name ~ '^11' or class_name = 'Lớp 11';
  update public.messages set class_name = '12'
  where class_name ~ '^12' or class_name = 'Lớp 12';

  update public.classes
  set active = false
  where id not in (v_khtn9, v_10, v_11, v_12)
    and (
      name ~ '^(10|11|12)'
      or slug ~ '^(10|11|12)'
      or name in ('KHTN 9', 'KHTN9')
      or slug in ('khtn-9', 'khtn9')
    );
end $$;
