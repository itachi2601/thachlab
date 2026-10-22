begin;
alter table public.exams disable trigger trg_exams_sync_bank;
update public.exams e set questions = (
  select jsonb_agg(case when b.ex is not null and (q.value->>'explanation') is distinct from b.ex then jsonb_set(q.value, '{explanation}', to_jsonb(b.ex)) else q.value end order by q.ordinality)
  from jsonb_array_elements(e.questions) with ordinality q(value, ordinality)
  left join lateral (select question->>'explanation' ex from public.question_bank
     where not archived and coalesce(question->>'explanation','') <> '' and content_hash = case when jsonb_typeof(q.value)='object' then public.question_content_hash(q.value) end limit 1) b on true)
where e.id in (354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393) and jsonb_typeof(e.questions)='array';
alter table public.exams enable trigger trg_exams_sync_bank;
commit;