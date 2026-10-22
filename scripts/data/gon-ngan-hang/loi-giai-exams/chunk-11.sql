begin;
alter table public.exams disable trigger trg_exams_sync_bank;
update public.exams e set questions = (
  select jsonb_agg(case when b.ex is not null and (q.value->>'explanation') is distinct from b.ex then jsonb_set(q.value, '{explanation}', to_jsonb(b.ex)) else q.value end order by q.ordinality)
  from jsonb_array_elements(e.questions) with ordinality q(value, ordinality)
  left join lateral (select question->>'explanation' ex from public.question_bank
     where not archived and coalesce(question->>'explanation','') <> '' and content_hash = case when jsonb_typeof(q.value)='object' then public.question_content_hash(q.value) end limit 1) b on true)
where e.id in (474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513) and jsonb_typeof(e.questions)='array';
alter table public.exams enable trigger trg_exams_sync_bank;
commit;