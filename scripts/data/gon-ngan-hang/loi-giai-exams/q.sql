with b as materialized (select content_hash h, question->>'explanation' ex from public.question_bank where not archived and coalesce(question->>'explanation','') <> ''),
 el as (select ex.id exam_id, (q.ordinality-1)::int idx, q.value v, public.question_content_hash(q.value) h
        from public.exams ex, jsonb_array_elements(ex.questions) with ordinality q(value, ordinality)
        where jsonb_typeof(ex.questions)='array' and jsonb_typeof(q.value)='object' and coalesce(q.value->>'question','')<>'')
 select el.exam_id, el.idx, b.ex as moi, el.v->>'explanation' as cu from el join b on b.h = el.h where (el.v->>'explanation') is distinct from b.ex