select ex.id as exam_id, (q.ordinality-1)::int as idx, public.question_content_hash(q.value) as h
from public.exams ex, jsonb_array_elements(ex.questions) with ordinality q(value, ordinality)
where jsonb_typeof(ex.questions)='array' and jsonb_typeof(q.value)='object' and coalesce(q.value->>'question','')<>''
