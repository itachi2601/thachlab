-- AVCN: tách thành 10 chương, mỗi chương đúng 1 bài (thầy chốt 20/10/2026).
--
-- Trước: môn 'avcn' có 1 chương "Technical English for Mechanical Engineering" chứa 10 bài
--        "Chapter 1 … Chapter 10" → trang lớp chỉ hiện 1 chương, 10 bài dồn dưới nó.
-- Sau:   10 chương, chương N chứa đúng bài Chapter N. Tiêu đề chương = tên chủ đề của bài
--        (bỏ tiền tố "Chapter N:") để trang tự ghép "Chương N · <tên chủ đề>" mà không lặp số.
--
-- Chỉ dữ liệu (chapters / chapter_classes / lessons), không đổi schema, policy hay hàm. Idempotent:
-- chạy lại không sinh chương trùng, không đổi gì thêm.

begin;

-- 1) Chương gốc (đang chứa cả 10 bài) thành chương 1, tiêu đề = tên chủ đề của bài 1
--    (bỏ tiền tố "Chapter N:"), không giữ tên sách làm tiêu đề chương.
update public.chapters x
set title = (
      select btrim(regexp_replace(y.title, '^[Cc]hapter\s*[0-9]+\s*[:.–\-]\s*', ''))
      from public.lessons y
      where y.chapter_id = x.id
      order by y.sort_order
      limit 1
    ),
    sort_order = 1
where x.subject_code = 'avcn'
  and x.sort_order = 1
  and exists (select 1 from public.lessons y where y.chapter_id = x.id);

-- 2) Sinh chương 2..10 từ chính tên bài (nguồn đúng là lessons.title, không bịa tên mới).
insert into public.chapters (title, sort_order, subject_code)
select distinct on (y.sort_order)
       btrim(regexp_replace(y.title, '^[Cc]hapter\s*[0-9]+\s*[:.–\-]\s*', '')),
       y.sort_order,
       'avcn'
from public.lessons y
join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'avcn'
  and y.sort_order between 2 and 10
  and not exists (
    select 1 from public.chapters c2
    where c2.subject_code = 'avcn' and c2.sort_order = y.sort_order
  )
order by y.sort_order;

-- 3) Cho lớp avcn thấy đủ 10 chương (chapter_classes là thứ trang lớp dùng để lọc).
insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x
join public.classes c on c.slug = 'avcn'
where x.subject_code = 'avcn'
on conflict do nothing;

-- 4) Mỗi bài về đúng chương cùng số thứ tự.
update public.lessons y
set chapter_id = x.id
from public.chapters x
where x.subject_code = 'avcn'
  and y.chapter_id in (select id from public.chapters where subject_code = 'avcn')
  and y.sort_order = x.sort_order;

-- 5) Kiểm: phải ra 10 dòng, so_bai = 1.
select x.sort_order, x.id as chapter_id, x.title, count(y.id) as so_bai
from public.chapters x
left join public.lessons y on y.chapter_id = x.id
where x.subject_code = 'avcn'
group by 1, 2, 3
order by 1;

commit;

-- ROLLBACK (chạy tay khi cần — đưa 10 bài về lại 1 chương):
-- begin;
-- update public.lessons y set chapter_id = x.id
--   from public.chapters x
--  where x.subject_code = 'avcn' and x.sort_order = 1
--    and y.chapter_id in (select id from public.chapters where subject_code = 'avcn');
-- delete from public.chapter_classes
--  where chapter_id in (select id from public.chapters where subject_code = 'avcn' and sort_order > 1);
-- delete from public.chapters where subject_code = 'avcn' and sort_order > 1;
-- update public.chapters set title = 'Technical English for Mechanical Engineering', sort_order = 1
--  where subject_code = 'avcn' and sort_order = 1;
-- commit;
