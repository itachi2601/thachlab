-- "Gửi trợ giảng xem trước": thầy gửi một đề (kể cả đề đang ẩn với học sinh) cho trợ giảng làm thử
-- từng câu, có đáp án ngay sau mỗi câu, rồi sang trang Chữa bài /tro-giang/chua-bai của đề đó.
--  1) Bảng exam_ta_previews: đề nào đã gửi cho TA, theo lớp nào (lớp quyết định trang Chữa bài lấy
--     học sinh nào để thống kê). Không đổi gì ở exams.published → học sinh không thấy đề.
--  2) Policy SELECT trên exams: TA đọc được đề ĐÃ GỬI mình, dù đề còn ẩn.
begin;

create table if not exists public.exam_ta_previews (
  exam_id  bigint      not null references public.exams(id) on delete cascade,
  class_id bigint      not null references public.classes(id) on delete cascade,
  sent_by  uuid        references auth.users(id) on delete set null default auth.uid(),
  sent_at  timestamptz not null default now(),
  primary key (exam_id, class_id)
);

alter table public.exam_ta_previews enable row level security;
revoke all on public.exam_ta_previews from anon, authenticated;
grant select, insert, delete on public.exam_ta_previews to authenticated;

-- Thầy (admin/instructor) gửi và thu hồi; trợ giảng đang hoạt động chỉ đọc danh sách.
drop policy if exists "staff manage ta previews" on public.exam_ta_previews;
create policy "staff manage ta previews" on public.exam_ta_previews
  as permissive for all to authenticated
  using (exists (select 1 from public.profiles p where p.id = (select auth.uid()) and p.role in ('admin', 'instructor')))
  with check (exists (select 1 from public.profiles p where p.id = (select auth.uid()) and p.role in ('admin', 'instructor')));

drop policy if exists "ta read ta previews" on public.exam_ta_previews;
create policy "ta read ta previews" on public.exam_ta_previews
  as permissive for select to authenticated
  using (public.assists_class(class_id));

-- TA đọc được đề đã gửi (policy permissive cộng với policy cũ; policy restrictive
-- "students only see own-class exams" đã cho staff — gồm tro_giang — đi qua).
drop policy if exists "ta read previewed exams" on public.exams;
create policy "ta read previewed exams" on public.exams
  as permissive for select to authenticated
  using (
    exists (
      select 1 from public.exam_ta_previews t
      where t.exam_id = exams.id and public.assists_class(t.class_id)
    )
  );

commit;

-- ROLLBACK:
-- drop policy if exists "ta read previewed exams" on public.exams;
-- drop table if exists public.exam_ta_previews;
