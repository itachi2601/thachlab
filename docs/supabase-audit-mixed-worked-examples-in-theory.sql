-- ============================================================
-- Khảo sát (CHỈ ĐỌC): tìm lesson_items(kind='ly_thuyet') còn sót nội dung
-- "Dạng N: Bài tập ... Câu N. ... Hướng dẫn giải ..." lẽ ra phải nằm trong
-- lesson_items(kind='bai_tap_mau') cùng lesson_id (mảng questions jsonb
-- {label, body_html}[] — xem components/lessons/WorkedQuestionsGrid.tsx).
--
-- Bối cảnh: phát hiện lỗi này ở lesson_id=84 (Bài 6. Phản xạ toàn phần,
-- đã sửa tay 25/9/2026). Nghi là lỗi từ đợt nhập bài gốc trước khi có cấu
-- trúc "6 mục bài học". Script này chỉ liệt kê, KHÔNG sửa dữ liệu.
--
-- Chạy: supabase db query --linked -f docs/supabase-audit-mixed-worked-examples-in-theory.sql
-- (xem quy ước trong memory reference_supabase_db_query_cli — không cần mật khẩu DB)
--
-- Dấu hiệu xác nhận mạnh nhất: số "Dạng N" tìm thấy trong body_html của mục lý thuyết
-- KHÔNG có mặt trong nhãn "label" (dạng "Dạng N: ...") của bất kỳ question nào trong
-- mảng questions của mục bai_tap_mau cùng bài — tức là Dạng đó chưa được tách ra.
-- Chỉ dựa vào "questions rỗng toàn bộ" là KHÔNG đủ: quan sát thực tế cho thấy nhiều bài
-- đã tách đúng một phần (vd. Dạng 2, Dạng 3) nhưng bỏ sót đúng Dạng 1 còn kẹt lại trong
-- lý thuyết, nên questions vẫn có phần tử (không rỗng) dù vẫn đang lỗi.
with theory as (
  select
    li.id as theory_item_id,
    li.lesson_id,
    l.title as lesson_title,
    li.body_html,
    (select count(*) from regexp_matches(li.body_html, 'Câu\s*\d+\s*\.', 'gi')) as cau_count,
    (select array_agg(distinct (m[1])::int order by (m[1])::int)
       from regexp_matches(li.body_html, 'Dạng\s*(\d+)\s*[:.]', 'gi') as m) as dang_nums_in_theory
  from lesson_items li
  join lessons l on l.id = li.lesson_id
  where li.kind = 'ly_thuyet'
    and li.body_html ~* 'Câu\s*\d+\s*\.'
),
worked as (
  select
    bm.lesson_id,
    bm.id as worked_item_id,
    coalesce(length(bm.body_html), 0) as worked_body_len,
    coalesce(jsonb_array_length(bm.questions), 0) as worked_questions_count,
    (
      select array_agg(distinct (regexp_match(q->>'label', 'Dạng\s*(\d+)', 'i'))[1]::int
                        order by (regexp_match(q->>'label', 'Dạng\s*(\d+)', 'i'))[1]::int)
      from jsonb_array_elements(coalesce(bm.questions, '[]'::jsonb)) as q
      where (q->>'label') ~* 'Dạng\s*\d+'
    ) as dang_nums_in_worked
  from lesson_items bm
  where bm.kind = 'bai_tap_mau'
)
select
  t.theory_item_id,
  t.lesson_id,
  t.lesson_title,
  length(t.body_html) as theory_len,
  t.cau_count,
  t.dang_nums_in_theory,
  w.worked_item_id,
  w.worked_body_len,
  w.worked_questions_count,
  w.dang_nums_in_worked,
  -- Dạng có trong lý thuyết nhưng chưa có trong questions của bai_tap_mau => nghi vấn mạnh
  (
    select array_agg(d order by d)
    from unnest(coalesce(t.dang_nums_in_theory, '{}')) as d
    where d <> all (coalesce(w.dang_nums_in_worked, '{}'))
  ) as dang_missing_from_worked
from theory t
left join worked w on w.lesson_id = t.lesson_id
order by t.lesson_id;
