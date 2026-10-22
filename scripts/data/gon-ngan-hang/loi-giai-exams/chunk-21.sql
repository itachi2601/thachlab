begin;
alter table public.exams disable trigger trg_exams_sync_bank;
update public.exams e set questions = (
  select jsonb_agg(case when b.ex is not null and (q.value->>'explanation') is distinct from b.ex then jsonb_set(q.value, '{explanation}', to_jsonb(b.ex)) else q.value end order by q.ordinality)
  from jsonb_array_elements(e.questions) with ordinality q(value, ordinality)
  left join lateral (select question->>'explanation' ex from public.question_bank
     where not archived and coalesce(question->>'explanation','') <> '' and content_hash = case when jsonb_typeof(q.value)='object' then public.question_content_hash(q.value) end limit 1) b on true)
where e.id in (874,875,876,877,878,879,880,881,882,883,884,885,886,887,888,889,890,891,892,893,894,895,896,897,898,899,900,901,903,904,905,906,907,908,909,910,911,912,913,914) and jsonb_typeof(e.questions)='array';
alter table public.exams enable trigger trg_exams_sync_bank;
commit;