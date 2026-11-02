-- Học phần CTTC "WorldSkills — Industrial Mechanics" (2/11/2026): bộ dịch song ngữ đề thi Shanghai 2026 Skill 01
-- (content/worldskills-im/dich/) dùng huấn luyện đội tuyển. Môn 'worldskills-im', lớp vào tự do, 5 chương theo
-- 4 giai đoạn huấn luyện + chương cho giáo viên, 16 bài. Chỉ chèn dữ liệu, idempotent, không đổi schema/policy.
-- Nội dung lý thuyết (lesson_items kind=ly_thuyet) ghi bằng: bash scripts/dang-worldskills-im.sh
begin;

insert into public.academic_subjects (code, label, icon, sort_order, active)
values ('worldskills-im', 'WorldSkills — Industrial Mechanics', '🛠️', 7, true)
on conflict (code) do nothing;

insert into public.classes (name, slug, color, icon, sort_order, active, requires_approval)
select 'WorldSkills — Industrial Mechanics', 'worldskills-im', '#C2410C', '🛠️', 8, true, false
where not exists (select 1 from public.classes where slug = 'worldskills-im');

create temporary table _ws_ch (so int, title text) on commit drop;
insert into _ws_ch values
  (1, 'Nền tảng — đọc trước khi vào xưởng'),
  (2, 'Kỹ năng đơn lẻ — hàn, tiện phay, khí nén'),
  (3, 'Tích hợp — lắp ráp, bảo trì, sửa lỗi'),
  (4, 'Thi thử 20 giờ và chấm điểm'),
  (5, 'Dành cho giáo viên huấn luyện');

insert into public.chapters (title, sort_order, subject_code)
select c.title, c.so, 'worldskills-im'
from _ws_ch c
where not exists (select 1 from public.chapters x where x.subject_code = 'worldskills-im' and x.sort_order = c.so);

insert into public.chapter_classes (chapter_id, class_id)
select x.id, c.id
from public.chapters x, public.classes c
where x.subject_code = 'worldskills-im' and c.slug = 'worldskills-im'
on conflict do nothing;

create temporary table _ws_ls (ch int, so int, title text) on commit drop;
insert into _ws_ls values
  (1, 1, 'Tổng quan đề thi: 4 module, 20 giờ, trọng số điểm'),
  (1, 2, 'Chú giải bản vẽ, BOM và vật liệu'),
  (1, 3, 'Trang bị bảo hộ và luật riêng của nghề'),
  (1, 4, 'Thuật ngữ Anh – Việt'),
  (2, 1, 'Module B: Hàn và lấy dấu'),
  (2, 2, 'Module C: Tiện và phay'),
  (2, 3, 'Sơ đồ khí nén và lắp ráp khí nén (E)'),
  (3, 1, 'Module D: Lắp ráp cơ khí và vận hành cuối (F)'),
  (3, 2, 'Module A1: Bảo trì dự đoán'),
  (3, 3, 'Module A2: Sửa lỗi mạch khí nén trên FluidSIM (G)'),
  (4, 1, 'Thang điểm đầy đủ A–G (198 mục, 100 điểm)'),
  (4, 2, 'Cách chấm, trừ điểm và thẩm định đề'),
  (5, 1, 'Mô tả nghề và chuẩn WSOS'),
  (5, 2, 'Yêu cầu thiết kế đề thi'),
  (5, 3, 'Máy phay M5 và danh mục file gốc'),
  (5, 4, 'Ghi chú lỗi trong bản gốc');

insert into public.lessons (chapter_id, title, sort_order, published)
select x.id, l.title, l.so, true
from _ws_ls l
join public.chapters x on x.subject_code = 'worldskills-im' and x.sort_order = l.ch
where not exists (select 1 from public.lessons y where y.chapter_id = x.id and y.sort_order = l.so);

commit;

-- Kiểm: 16 dòng.
select x.sort_order as ch, y.sort_order as so, y.id, y.title
from public.lessons y join public.chapters x on x.id = y.chapter_id
where x.subject_code = 'worldskills-im' order by 1, 2;

-- ROLLBACK (chạy tay khi cần):
-- begin;
-- delete from public.lesson_items where lesson_id in (select y.id from public.lessons y join public.chapters x on x.id = y.chapter_id where x.subject_code = 'worldskills-im');
-- delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'worldskills-im');
-- delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'worldskills-im');
-- delete from public.chapters where subject_code = 'worldskills-im';
-- delete from public.user_classes where class_id in (select id from public.classes where slug = 'worldskills-im');
-- delete from public.classes where slug = 'worldskills-im';
-- delete from public.academic_subjects where code = 'worldskills-im';
-- commit;
