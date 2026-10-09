-- Khoá "Vật lí HSG & Luyện chuyên" trong KHTN 9 (thầy chốt 10/10/2026).
-- Thêm DỮ LIỆU (không đổi schema): 1 môn mới `hsg-vat-ly` + 6 chương + 17 bài (14 chuyên đề từ
-- tài liệu docx + 3 chuyên đề còn thiếu so với đề cương THI HSG 9 KHTN 26-27: Lực, Âm thanh,
-- Truyền nhiệt & nở vì nhiệt). Chương gắn lớp KHTN 9 (class_id = 15) qua chapter_classes.
-- Mọi bài tạo với published = false (HS chưa thấy); riêng CĐ01, CĐ02 có sẵn mục ly_thuyet +
-- bai_tap_mau rỗng để các script cap-nhat-ly-thuyet.sh / publish-bai-tap-mau.mts ghi vào.
-- Idempotent: chạy lại không tạo trùng (so khớp theo tiêu đề).
-- Rollback: cuối file.

begin;

insert into public.academic_subjects (code, label, icon, sort_order, active)
values ('hsg-vat-ly', 'Vật lí HSG & chuyên', '🏆', 4, true)
on conflict (code) do nothing;

-- ── Chương ──────────────────────────────────────────────────────────────
create temporary table _hsg_ch (title text, so int) on commit drop;
insert into _hsg_ch values
  ('Nền tảng: công cụ toán học và thực hành', 101),
  ('Cơ học và năng lượng cơ học', 102),
  ('Nhiệt học và âm thanh', 103),
  ('Điện học', 104),
  ('Quang học và Trái Đất – bầu trời', 105),
  ('Điện từ và năng lượng với cuộc sống', 106);

insert into public.chapters (title, sort_order, subject_code)
select c.title, c.so, 'hsg-vat-ly'
from _hsg_ch c
where not exists (
  select 1 from public.chapters x where x.subject_code = 'hsg-vat-ly' and x.title = c.title
);

insert into public.chapter_classes (chapter_id, class_id)
select x.id, 15
from public.chapters x
where x.subject_code = 'hsg-vat-ly'
  and not exists (
    select 1 from public.chapter_classes cc where cc.chapter_id = x.id and cc.class_id = 15
  );

-- ── Bài (mỗi chuyên đề = một bài) ───────────────────────────────────────
create temporary table _hsg_ls (chuong text, so int, title text, mo_ta text) on commit drop;
insert into _hsg_ls values
  ('Nền tảng: công cụ toán học và thực hành', 1, 'Chuyên đề 00. Kỹ năng nền: công cụ toán học, đọc đồ thị, sai số và thực hành',
     'Biến đổi đại số, tỉ lệ, đọc đồ thị, ước lượng, sai số và cách trình bày bài thi HSG.'),
  ('Cơ học và năng lượng cơ học', 1, 'Chuyên đề 01. Công và công suất',
     'Công cơ học, công suất, máy cơ đơn giản, palăng, mặt phẳng nghiêng; mở rộng lực xiên góc và công suất tức thời.'),
  ('Cơ học và năng lượng cơ học', 2, 'Chuyên đề 02. Động năng, thế năng, cơ năng và định luật bảo toàn cơ năng',
     'Động năng, thế năng, cơ năng, bảo toàn và biến thiên cơ năng khi có ma sát.'),
  ('Cơ học và năng lượng cơ học', 3, 'Chuyên đề 10. Lực: tổng hợp lực, cân bằng, ma sát, đòn bẩy',
     'Chuyên đề mới, đang soạn: lực và cân bằng lực, ma sát, mô men và đòn bẩy.'),
  ('Cơ học và năng lượng cơ học', 4, 'Chuyên đề 11. Cơ học chất lưu: áp suất chất lỏng, bình thông nhau và lực đẩy Archimedes',
     'Khối lượng riêng, áp suất chất lỏng, bình thông nhau, lực đẩy Archimedes.'),
  ('Cơ học và năng lượng cơ học', 5, 'Chuyên đề 13. Chuyển động cơ học và đồ thị chuyển động',
     'Tốc độ, tốc độ trung bình, chuyển động tương đối, đồ thị quãng đường – thời gian.'),
  ('Nhiệt học và âm thanh', 1, 'Chuyên đề 12. Nhiệt học nâng cao: phương trình cân bằng nhiệt và chuyển thể',
     'Cân bằng nhiệt nhiều vật, chuyển thể, đồ thị nhiệt độ – thời gian, hao phí nhiệt.'),
  ('Nhiệt học và âm thanh', 2, 'Chuyên đề 16. Truyền năng lượng nhiệt và sự nở vì nhiệt',
     'Chuyên đề mới, đang soạn: dẫn nhiệt, đối lưu, bức xạ nhiệt, nở vì nhiệt.'),
  ('Nhiệt học và âm thanh', 3, 'Chuyên đề 15. Âm thanh: sóng âm, độ to – độ cao, phản xạ âm',
     'Chuyên đề mới, đang soạn: sóng âm, tần số, độ to và độ cao, tiếng vang.'),
  ('Điện học', 1, 'Chuyên đề 03. Điện trở và định luật Ohm',
     'Điện trở, định luật Ohm, điện trở suất, biến trở.'),
  ('Điện học', 2, 'Chuyên đề 04. Đoạn mạch nối tiếp, song song và mạch hỗn hợp',
     'Mạch nối tiếp, song song, hỗn hợp, mạch cầu và biến đổi mạch.'),
  ('Điện học', 3, 'Chuyên đề 05. Năng lượng của dòng điện, công suất điện và định luật Joule–Lenz',
     'Công, công suất điện, nhiệt lượng toả ra trên điện trở, hiệu suất.'),
  ('Quang học và Trái Đất – bầu trời', 1, 'Chuyên đề 06. Khúc xạ ánh sáng, phản xạ toàn phần, lăng kính và tán sắc',
     'Khúc xạ, phản xạ toàn phần, lăng kính, tán sắc ánh sáng.'),
  ('Quang học và Trái Đất – bầu trời', 2, 'Chuyên đề 07. Thấu kính mỏng và kính lúp',
     'Dựng ảnh, công thức thấu kính, kính lúp, hệ thấu kính.'),
  ('Quang học và Trái Đất – bầu trời', 3, 'Chuyên đề 14. Gương phẳng và Trái Đất – bầu trời',
     'Gương phẳng, bóng, múi giờ, pha Mặt Trăng, nhật thực – nguyệt thực, Hệ Mặt Trời, Ngân Hà.'),
  ('Điện từ và năng lượng với cuộc sống', 1, 'Chuyên đề 08. Cảm ứng điện từ và dòng điện xoay chiều',
     'Cảm ứng điện từ, máy phát điện xoay chiều, máy biến áp, truyền tải điện.'),
  ('Điện từ và năng lượng với cuộc sống', 2, 'Chuyên đề 09. Năng lượng với cuộc sống: vòng năng lượng Trái Đất, nhiên liệu và năng lượng tái tạo',
     'Vòng năng lượng, nhiên liệu hoá thạch, năng lượng tái tạo, hiệu suất, chi phí và CO2.');

insert into public.lessons (chapter_id, title, sort_order, published, lesson_kind, description)
select ch.id, l.title, l.so, false, 'bai_hoc', l.mo_ta
from _hsg_ls l
join public.chapters ch on ch.subject_code = 'hsg-vat-ly' and ch.title = l.chuong
where not exists (
  select 1 from public.lessons x where x.chapter_id = ch.id and x.title = l.title
);

-- ── Mục có sẵn cho 2 chuyên đề làm thử (CĐ01, CĐ02) ─────────────────────
insert into public.lesson_items (lesson_id, kind, title, subtitle, body_html, sort_order, required, exam_ids, questions, published_at)
select ls.id, 'ly_thuyet', 'Lý thuyết nâng cao', '', '<p>Đang soạn.</p>', 1, true, '{}', '[]'::jsonb, now()
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where (ls.title like 'Chuyên đề 01.%' or ls.title like 'Chuyên đề 02.%')
  and not exists (select 1 from public.lesson_items i where i.lesson_id = ls.id and i.kind = 'ly_thuyet');

insert into public.lesson_items (lesson_id, kind, title, subtitle, body_html, sort_order, required, exam_ids, questions, published_at)
select ls.id, 'bai_tap_mau', 'Các dạng bài tập', '', '', 2, true, '{}', '[]'::jsonb, now()
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
where (ls.title like 'Chuyên đề 01.%' or ls.title like 'Chuyên đề 02.%')
  and not exists (select 1 from public.lesson_items i where i.lesson_id = ls.id and i.kind = 'bai_tap_mau');

commit;

-- Danh sách id để dùng cho cap-nhat-ly-thuyet.sh / publish-bai-tap-mau.mts:
select ls.id as lesson_id, ls.title, ls.published
from public.lessons ls
join public.chapters ch on ch.id = ls.chapter_id and ch.subject_code = 'hsg-vat-ly'
order by ch.sort_order, ls.sort_order;

-- ROLLBACK (chỉ khi chưa có học sinh làm bài trong khoá):
--   begin;
--   delete from public.lesson_items where lesson_id in (select ls.id from public.lessons ls join public.chapters c on c.id = ls.chapter_id where c.subject_code = 'hsg-vat-ly');
--   delete from public.lessons where chapter_id in (select id from public.chapters where subject_code = 'hsg-vat-ly');
--   delete from public.chapter_classes where chapter_id in (select id from public.chapters where subject_code = 'hsg-vat-ly');
--   delete from public.chapters where subject_code = 'hsg-vat-ly';
--   delete from public.academic_subjects where code = 'hsg-vat-ly';
--   commit;
