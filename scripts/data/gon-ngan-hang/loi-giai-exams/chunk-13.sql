begin;
alter table public.exams disable trigger trg_exams_sync_bank;
update public.exams e set questions = (
  select jsonb_agg(case when b.ex is not null and (q.value->>'explanation') is distinct from b.ex then jsonb_set(q.value, '{explanation}', to_jsonb(b.ex)) else q.value end order by q.ordinality)
  from jsonb_array_elements(e.questions) with ordinality q(value, ordinality)
  left join lateral (select question->>'explanation' ex from public.question_bank
     where not archived and coalesce(question->>'explanation','') <> '' and content_hash = case when jsonb_typeof(q.value)='object' then public.question_content_hash(q.value) end limit 1) b on true)
where e.id in (554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593) and jsonb_typeof(e.questions)='array';
alter table public.exams enable trigger trg_exams_sync_bank;
commit;