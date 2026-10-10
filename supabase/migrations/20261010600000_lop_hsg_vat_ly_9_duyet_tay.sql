-- Lớp "Học sinh giỏi & Chuyên Vật lý 9" ở chỗ chọn lớp khi đăng ký: phải được thầy duyệt tay.
-- Thêm cột classes.requires_approval; chính sách RLS chỉ cho học sinh gửi 'pending' vào lớp loại này
-- (các lớp khác giữ nguyên: tự vào 'active' như alpha test 7/10). Chỉ giáo viên/quản trị mới đặt 'active'.
begin;

alter table public.classes add column if not exists requires_approval boolean not null default false;

insert into public.classes (name, slug, color, icon, sort_order, active, requires_approval)
select 'Học sinh giỏi & Chuyên Vật lý 9', 'hsg-vat-ly-9', '#F59E0B', '🏆', 5, true, true
where not exists (select 1 from public.classes where slug = 'hsg-vat-ly-9');
update public.classes set requires_approval = true where slug = 'hsg-vat-ly-9';

drop policy if exists "students request own class" on public.user_classes;
create policy "students request own class" on public.user_classes
  as permissive for insert to authenticated
  with check (
    user_id = (select auth.uid())
    and status = case when coalesce((select c.requires_approval from public.classes c where c.id = class_id), false)
                      then 'pending' else 'active' end
  );

drop policy if exists "students resubmit rejected class request" on public.user_classes;
create policy "students resubmit rejected class request" on public.user_classes
  as permissive for update to authenticated
  using (user_id = (select auth.uid()) and status in ('rejected', 'pending'))
  with check (
    user_id = (select auth.uid())
    and status = case when coalesce((select c.requires_approval from public.classes c where c.id = class_id), false)
                      then 'pending' else 'active' end
  );

commit;

-- ROLLBACK:
-- begin;
-- drop policy "students request own class" on public.user_classes;
-- create policy "students request own class" on public.user_classes as permissive for insert to authenticated
--   with check (user_id = (select auth.uid()) and status in ('pending', 'active'));
-- drop policy "students resubmit rejected class request" on public.user_classes;
-- create policy "students resubmit rejected class request" on public.user_classes as permissive for update to authenticated
--   using (user_id = (select auth.uid()) and status in ('rejected', 'pending')) with check (user_id = (select auth.uid()) and status = 'active');
-- delete from public.user_classes where class_id in (select id from public.classes where slug = 'hsg-vat-ly-9');
-- delete from public.classes where slug = 'hsg-vat-ly-9';
-- alter table public.classes drop column requires_approval;
-- commit;
