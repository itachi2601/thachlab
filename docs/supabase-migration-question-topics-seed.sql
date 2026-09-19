-- ============================================================
-- Danh mục chủ đề câu hỏi (question_topics) — Vật lí THPT + KHTN 9
-- ============================================================
-- Nguồn: Chương trình GDPT môn Vật lí 2018 (mạch nội dung / "Nội dung" từng lớp),
-- ánh xạ sang đúng cây Chương → Bài đang có trên thachlab để nút "Ôn lại" nhảy
-- thẳng vào bài cần học lại.
--
-- Chạy SAU docs/supabase-migration-exam-analytics.sql (đã tạo bảng question_topics).
-- Chạy lại nhiều lần được: khớp theo (subject_code, grade, name), chỉ cập nhật
-- chapter_id / lesson_id / sort_order, KHÔNG đụng nhãn đã gắn trên câu hỏi.
--
-- Tên chương là duy nhất trong bảng chapters nên khớp theo tiêu đề là an toàn;
-- khối lấy từ chapter_classes (KHTN 9 → '9', các lớp còn lại → '10' | '11' | '12').
-- Bài nào đổi tên sau này thì lesson_id về null — chạy lại file này sau khi sửa tên.
-- ============================================================

create temporary table tmp_topics (
  grade text, ch_title text, lesson_title text, name text, sort_order int
) on commit drop;

insert into tmp_topics (grade, ch_title, lesson_title, name, sort_order) values
  ('9', 'Chương 1: Năng lượng cơ học', 'Bài 2. Động năng. Thế năng', 'Động năng. Thế năng', 10),
  ('9', 'Chương 1: Năng lượng cơ học', 'Bài 3. Cơ năng', 'Cơ năng', 20),
  ('9', 'Chương 1: Năng lượng cơ học', 'Bài 4. Công và công suất', 'Công và công suất', 30),
  ('9', 'Chương 2: Ánh sáng', 'Bài 5. Khúc xạ ánh sáng', 'Khúc xạ ánh sáng', 40),
  ('9', 'Chương 2: Ánh sáng', 'Bài 6. Phản xạ toàn phần', 'Phản xạ toàn phần', 50),
  ('9', 'Chương 2: Ánh sáng', 'Bài 7. Lăng kính', 'Lăng kính', 60),
  ('9', 'Chương 2: Ánh sáng', 'Bài 8. Thấu kính', 'Thấu kính', 70),
  ('9', 'Chương 3: Điện', 'Bài 11. Điện trở. Định luật Ohm', 'Điện trở. Định luật Ohm', 80),
  ('9', 'Chương 3: Điện', 'Bài 12. Đoạn mạch nối tiếp, song song', 'Đoạn mạch nối tiếp, song song', 90),
  ('9', 'Chương 3: Điện', 'Bài 13. Năng lượng của dòng điện và công suất điện', 'Năng lượng và công suất điện', 100),
  ('9', 'Chương 4: Điện từ', 'Bài 14. Cảm ứng điện từ. Nguyên tắc tạo ra dòng điện xoay chiều', 'Cảm ứng điện từ. Dòng điện xoay chiều', 110),
  ('9', 'Chương 4: Điện từ', 'Bài 15. Tác dụng của dòng điện xoay chiều', 'Tác dụng của dòng điện xoay chiều', 120),
  ('9', 'Chương 5: Năng lượng với cuộc sống', 'Bài 16. Vòng năng lượng trên Trái Đất. Năng lượng hóa thạch', 'Năng lượng hoá thạch', 130),
  ('9', 'Chương 5: Năng lượng với cuộc sống', 'Bài 17. Một số dạng năng lượng tái tạo', 'Năng lượng tái tạo', 140),
  ('10', 'Chương 1: Mở đầu', 'Bài 2. Các quy tắc an toàn trong phòng thực hành Vật lí', 'Phương pháp nghiên cứu và an toàn thí nghiệm', 10),
  ('10', 'Chương 1: Mở đầu', 'Bài 3. Thực hành tính sai số trong phép đo. Ghi kết quả đo', 'Sai số trong phép đo', 20),
  ('10', 'Chương 2: Động học', 'Bài 5. Tốc độ và vận tốc', 'Độ dịch chuyển, quãng đường, tốc độ, vận tốc', 30),
  ('10', 'Chương 2: Động học', 'Bài 7. Đồ thị độ dịch chuyển - thời gian', 'Đồ thị độ dịch chuyển – thời gian', 40),
  ('10', 'Chương 2: Động học', 'Bài 9. Chuyển động thẳng biến đổi đều', 'Chuyển động thẳng biến đổi đều. Gia tốc', 50),
  ('10', 'Chương 2: Động học', 'Bài 10. Sự rơi tự do', 'Sự rơi tự do', 60),
  ('10', 'Chương 2: Động học', 'Bài 12. Chuyển động ném', 'Chuyển động ném', 70),
  ('10', 'Chương 3: Động lực học', 'Bài 13. Tổng hợp và phân tích lực. Cân bằng lực', 'Tổng hợp và phân tích lực. Cân bằng lực', 80),
  ('10', 'Chương 3: Động lực học', 'Bài 15. Định luật 2 Newton', 'Ba định luật Newton', 90),
  ('10', 'Chương 3: Động lực học', 'Bài 17. Trọng lực và lực căng', 'Trọng lực và lực căng', 100),
  ('10', 'Chương 3: Động lực học', 'Bài 18. Lực ma sát', 'Lực ma sát, lực cản và lực nâng', 110),
  ('10', 'Chương 3: Động lực học', 'Bài 21. Moment lực. Cân bằng của vật rắn', 'Moment lực. Cân bằng của vật rắn', 120),
  ('10', 'Chương 4: Năng lượng, công, công suất', 'Bài 23. Năng lượng. Công cơ học', 'Năng lượng. Công cơ học', 130),
  ('10', 'Chương 4: Năng lượng, công, công suất', 'Bài 24. Công suất', 'Công suất', 140),
  ('10', 'Chương 4: Năng lượng, công, công suất', 'Bài 25. Động năng, thế năng', 'Động năng, thế năng', 150),
  ('10', 'Chương 4: Năng lượng, công, công suất', 'Bài 26. Cơ năng và định luật bảo toàn cơ năng', 'Cơ năng và định luật bảo toàn cơ năng', 160),
  ('10', 'Chương 4: Năng lượng, công, công suất', 'Bài 27. Hiệu suất', 'Hiệu suất', 170),
  ('10', 'Chương 5: Động lượng', 'Bài 28. Động lượng', 'Động lượng', 180),
  ('10', 'Chương 5: Động lượng', 'Bài 29. Định luật bảo toàn động lượng', 'Bảo toàn động lượng và va chạm', 190),
  ('10', 'Chương 6: Chuyển động tròn', 'Bài 31. Động học của chuyển động tròn đều', 'Động học của chuyển động tròn đều', 200),
  ('10', 'Chương 6: Chuyển động tròn', 'Bài 32. Lực hướng tâm và gia tốc hướng tâm', 'Lực hướng tâm và gia tốc hướng tâm', 210),
  ('10', 'Chương 7: Biến dạng của vật rắn. Áp suất chất lỏng', 'Bài 33. Biến dạng của vật rắn', 'Biến dạng của vật rắn. Định luật Hooke', 220),
  ('10', 'Chương 7: Biến dạng của vật rắn. Áp suất chất lỏng', 'Bài 34. Khối lượng riêng. Áp suất chất lỏng', 'Khối lượng riêng. Áp suất chất lỏng', 230),
  ('11', 'Chương 1: Dao động', 'Bài 2. Mô tả dao động điều hoà', 'Dao động điều hoà', 10),
  ('11', 'Chương 1: Dao động', 'Bài 3. Vận tốc, gia tốc trong dao động điều hoà', 'Vận tốc, gia tốc trong dao động điều hoà', 20),
  ('11', 'Chương 1: Dao động', 'Bài 5. Động năng. Thế năng. Sự chuyển hoá giữa động năng và thế năng trong dao động điều hoà', 'Năng lượng trong dao động điều hoà', 30),
  ('11', 'Chương 1: Dao động', 'Bài 6. Dao động tắt dần. Dao động cưỡng bức. Hiện tượng cộng hưởng', 'Dao động tắt dần. Dao động cưỡng bức. Cộng hưởng', 40),
  ('11', 'Chương 2: Sóng', 'Bài 8. Mô tả sóng', 'Mô tả sóng', 50),
  ('11', 'Chương 2: Sóng', 'Bài 9. Sóng ngang, sóng dọc, sự truyền năng lượng của sóng cơ', 'Sóng ngang, sóng dọc. Truyền năng lượng của sóng cơ', 60),
  ('11', 'Chương 2: Sóng', 'Bài 11. Sóng điện từ', 'Sóng điện từ', 70),
  ('11', 'Chương 2: Sóng', 'Bài 12. Giao thoa sóng', 'Giao thoa sóng', 80),
  ('11', 'Chương 2: Sóng', 'Bài 13. Sóng dừng', 'Sóng dừng', 90),
  ('11', 'Chương 2: Sóng', 'Bài 15. Thực hành: Đo tốc độ truyền âm', 'Sóng âm và đo tốc độ truyền âm', 100),
  ('11', 'Chương 3: Điện trường', 'Bài 16. Lực tương tác giữa hai điện tích', 'Lực tương tác giữa hai điện tích', 110),
  ('11', 'Chương 3: Điện trường', 'Bài 17. Khái niệm điện trường', 'Khái niệm điện trường. Cường độ điện trường', 120),
  ('11', 'Chương 3: Điện trường', 'Bài 18. Điện trường đều', 'Điện trường đều', 130),
  ('11', 'Chương 3: Điện trường', 'Bài 20. Điện thế', 'Thế năng điện. Điện thế', 140),
  ('11', 'Chương 3: Điện trường', 'Bài 21. Tụ điện', 'Tụ điện và điện dung', 150),
  ('11', 'Chương 4: Dòng điện. Mạch điện', 'Bài 22. Cường độ dòng điện', 'Cường độ dòng điện', 160),
  ('11', 'Chương 4: Dòng điện. Mạch điện', 'Bài 23. Điện trở. Định luật Ohm', 'Điện trở. Định luật Ohm', 170),
  ('11', 'Chương 4: Dòng điện. Mạch điện', 'Bài 24. Nguồn điện', 'Nguồn điện. Suất điện động', 180),
  ('11', 'Chương 4: Dòng điện. Mạch điện', 'Bài 25. Năng lượng điện và công suất điện', 'Năng lượng điện. Công suất điện', 190),
  ('12', 'Chương 1: Vật lí nhiệt', 'Bài 1. Sự chuyển thể', 'Sự chuyển thể', 10),
  ('12', 'Chương 1: Vật lí nhiệt', 'Bài 2. Thang nhiệt độ', 'Thang nhiệt độ. Nhiệt kế', 20),
  ('12', 'Chương 1: Vật lí nhiệt', 'Bài 3. Nội năng. Định luật 1 của nhiệt động lực học', 'Nội năng. Định luật 1 của nhiệt động lực học', 30),
  ('12', 'Chương 1: Vật lí nhiệt', 'Bài 4. Thực hành đo nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng', 'Nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng', 40),
  ('12', 'Chương 2: Khí lí tưởng', 'Bài 5. Thuyết động học phân tử chất khí', 'Thuyết động học phân tử chất khí', 50),
  ('12', 'Chương 2: Khí lí tưởng', 'Bài 6. Định luật Boyle. Định luật Charles', 'Định luật Boyle. Định luật Charles', 60),
  ('12', 'Chương 2: Khí lí tưởng', 'Bài 7. Phương trình trạng thái của khí lí tưởng', 'Phương trình trạng thái khí lí tưởng', 70),
  ('12', 'Chương 2: Khí lí tưởng', 'Bài 8. Áp suất - động năng của phân tử khí', 'Áp suất và động năng phân tử khí', 80),
  ('12', 'Chương 3: Từ trường', 'Bài 9. Khái niệm từ trường', 'Khái niệm từ trường', 90),
  ('12', 'Chương 3: Từ trường', 'Bài 10. Lực từ. Cảm ứng từ', 'Lực từ. Cảm ứng từ', 100),
  ('12', 'Chương 3: Từ trường', 'Bài 12. Hiện tượng cảm ứng điện từ', 'Từ thông. Hiện tượng cảm ứng điện từ', 110),
  ('12', 'Chương 3: Từ trường', 'Bài 13. Đại cương về dòng điện xoay chiều', 'Đại cương về dòng điện xoay chiều', 120),
  ('12', 'Chương 4: Vật lí hạt nhân', 'Bài 14. Hạt nhân và mô hình nguyên tử', 'Cấu trúc hạt nhân', 130),
  ('12', 'Chương 4: Vật lí hạt nhân', 'Bài 15. Năng lượng liên kết hạt nhân', 'Độ hụt khối. Năng lượng liên kết hạt nhân', 140),
  ('12', 'Chương 4: Vật lí hạt nhân', 'Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng', 'Phản ứng phân hạch, phản ứng nhiệt hạch', 150),
  ('12', 'Chương 4: Vật lí hạt nhân', 'Bài 17. Hiện tượng phóng xạ', 'Hiện tượng phóng xạ. Chu kì bán rã', 160),
  ('12', 'Chương 4: Vật lí hạt nhân', 'Bài 18. An toàn phóng xạ', 'An toàn phóng xạ', 170)
;

-- Chương không tìm thấy thì dừng lại, đừng chèn nửa vời.
do $$
declare v_missing text;
begin
  select string_agg(distinct t.ch_title, ', ') into v_missing
  from tmp_topics t
  where not exists (select 1 from public.chapters c where c.title = t.ch_title);
  if v_missing is not null then
    raise exception 'Không tìm thấy chương: %', v_missing;
  end if;
end $$;

insert into public.question_topics (subject_code, grade, chapter_id, lesson_id, name, sort_order)
select 'vat-ly', t.grade, c.id, l.id, t.name, t.sort_order
from tmp_topics t
join public.chapters c on c.title = t.ch_title
left join public.lessons l on l.chapter_id = c.id and l.title = t.lesson_title
on conflict (subject_code, grade, name) do update
  set chapter_id = excluded.chapter_id,
      lesson_id  = coalesce(excluded.lesson_id, public.question_topics.lesson_id),
      sort_order = excluded.sort_order;

-- Báo lại chủ đề nào chưa trỏ được vào bài (sai tên bài) để sửa rồi chạy lại.
do $$
declare r record;
begin
  for r in
    select t.grade, t.name, t.lesson_title
    from tmp_topics t
    join public.chapters c on c.title = t.ch_title
    left join public.lessons l on l.chapter_id = c.id and l.title = t.lesson_title
    where l.id is null
  loop
    raise notice 'Chủ đề "% (lớp %)" chưa gắn được bài: không có bài tên "%"', r.name, r.grade, r.lesson_title;
  end loop;
end $$;
