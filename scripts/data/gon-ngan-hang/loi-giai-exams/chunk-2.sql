begin;
alter table public.exams disable trigger trg_exams_sync_bank;
update public.exams e set questions = (
  select jsonb_agg(case when b.ex is not null and (q.value->>'explanation') is distinct from b.ex then jsonb_set(q.value, '{explanation}', to_jsonb(b.ex)) else q.value end order by q.ordinality)
  from jsonb_array_elements(e.questions) with ordinality q(value, ordinality)
  left join lateral (select question->>'explanation' ex from public.question_bank
     where not archived and coalesce(question->>'explanation','') <> '' and content_hash = case when jsonb_typeof(q.value)='object' then public.question_content_hash(q.value) end limit 1) b on true)
where e.id in (91,96,97,98,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135) and jsonb_typeof(e.questions)='array';
alter table public.exams enable trigger trg_exams_sync_bank;
commit;