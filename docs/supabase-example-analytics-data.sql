-- ============================================================
-- Example Data: Phân tích điểm số với Topic
-- Dùng để test tính năng Score Analytics
--
-- ⚠️ CẢNH BÁO: Chỉ chạy trên môi trường DEV/TEST
-- Thay thế {USER_ID} và {EXAM_ID} bằng giá trị thực
-- ============================================================

-- Bước 1: Cập nhật 1 đề thi với topic cho mỗi câu
-- (Ví dụ: exam_id = 1, 10 câu hỏi)
-- Chạy query này trong Supabase SQL Editor

UPDATE public.exams
SET questions = jsonb_set(
  jsonb_set(
    jsonb_set(
      jsonb_set(
        jsonb_set(
          jsonb_set(
            jsonb_set(
              jsonb_set(
                jsonb_set(
                  jsonb_set(
                    questions,
                    '{0,topic}',
                    '"Lực & chuyển động"'
                  ),
                  '{1,topic}',
                  '"Lực & chuyển động"'
                ),
                '{2,topic}',
                '"Năng lượng"'
              ),
              '{3,topic}',
              '"Năng lượng"'
            ),
            '{4,topic}',
            '"Chuyển động thẳng"'
          ),
          '{5,topic}',
          '"Chuyển động thẳng"'
        ),
        '{6,topic}',
        '"Điện tĩnh học"'
      ),
      '{7,topic}',
      '"Điện tĩnh học"'
    ),
    '{8,topic}',
    '"Từ trường"'
  ),
  '{9,topic}',
  '"Từ trường"'
)
WHERE id = 1; -- Thay 1 bằng exam_id cần update

-- Bước 2: Tạo exam_question_results cho một bài làm
-- Giả sử:
-- - exam_result_id = 1 (kết quả bài làm của học sinh)
-- - Học sinh làm sai: câu 1, 3, 4, 8

INSERT INTO public.exam_question_results (exam_result_id, question_index, topic, is_correct)
VALUES
  (1, 0, 'Lực & chuyển động', true),    -- câu 0: đúng
  (1, 1, 'Lực & chuyển động', false),   -- câu 1: sai
  (1, 2, 'Năng lượng', true),           -- câu 2: đúng
  (1, 3, 'Năng lượng', false),          -- câu 3: sai
  (1, 4, 'Chuyển động thẳng', true),    -- câu 4: đúng
  (1, 5, 'Chuyển động thẳng', true),    -- câu 5: đúng
  (1, 6, 'Điện tĩnh học', true),        -- câu 6: đúng
  (1, 7, 'Điện tĩnh học', false),       -- câu 7: sai
  (1, 8, 'Từ trường', true),            -- câu 8: đúng
  (1, 9, 'Từ trường', false);           -- câu 9: sai

-- Bước 3: Verify dữ liệu
-- Chạy các query này để kiểm tra:

-- Query 1: Xem câu sai theo topic
SELECT
  topic,
  COUNT(*) as total,
  SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as correct,
  SUM(CASE WHEN NOT is_correct THEN 1 ELSE 0 END) as wrong,
  ROUND(100.0 * SUM(CASE WHEN NOT is_correct THEN 1 ELSE 0 END) / COUNT(*)) as percent_wrong
FROM public.exam_question_results
WHERE exam_result_id = 1  -- Thay 1 bằng exam_result_id
GROUP BY topic
ORDER BY wrong DESC;

-- Kết quả mong đợi:
-- | topic                | total | correct | wrong | percent_wrong |
-- | Lực & chuyển động    | 2     | 1       | 1     | 50            |
-- | Năng lượng           | 2     | 1       | 1     | 50            |
-- | Từ trường            | 2     | 1       | 1     | 50            |
-- | Điện tĩnh học        | 2     | 1       | 1     | 50            |
-- | Chuyển động thẳng    | 2     | 2       | 0     | 0             |

-- Query 2: Xem chi tiết câu sai của từng topic
SELECT
  topic,
  question_index,
  is_correct
FROM public.exam_question_results
WHERE exam_result_id = 1 AND NOT is_correct
ORDER BY question_index;

-- Query 3: Xem tất cả kết quả của một bài làm
SELECT * FROM public.exam_question_results WHERE exam_result_id = 1;
