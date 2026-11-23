-- 22/11/2026 (thay chot): bo 11 cau chu de rong NGOAI chuong trinh khoi de 693 (cau 5,8,9,14,15,18,26 - dien xoay chieu, thuoc lop 12)
-- va 701 (cau 8,11,26,27 - ban dan, chat khi, dien phan). 693/701/1227 deu 0 luot lam (kiem 22/11). Dong thoi an de cu 1227.
-- Chay tu checkout chinh: supabase db query --linked -f <file>. Hoan tac: bang bk_bo11cau_20261122_exams (chep lai questions/question_count/type_counts), bk_..._bank (archived).
begin;
create table public.bk_bo11cau_20261122_exams as select id, questions, question_count, type_counts, published from public.exams where id in (693, 701, 1227);
create table public.bk_bo11cau_20261122_bank as select id, archived from public.question_bank where source_exam_id in (693, 701);
alter table public.bk_bo11cau_20261122_exams enable row level security;
alter table public.bk_bo11cau_20261122_bank enable row level security;
revoke all on public.bk_bo11cau_20261122_exams, public.bk_bo11cau_20261122_bank from anon, authenticated;

alter table public.exams disable trigger trg_exams_sync_bank;
create temp table bo(de bigint, cau int) on commit drop;
insert into bo values (693,5),(693,8),(693,9),(693,14),(693,15),(693,18),(693,26),(701,8),(701,11),(701,26),(701,27);
-- an dong bank tuong ung (khop hash phan tu bi bo, chi dong goc tu chinh de 693/701)
update public.question_bank b set archived = true, updated_at = now()
from public.exams e cross join lateral jsonb_array_elements(e.questions) with ordinality x(v, o)
join bo on bo.de = e.id and bo.cau = x.o
where b.content_hash = public.question_content_hash(x.v) and b.source_exam_id in (693, 701);
-- bo phan tu khoi mang questions
update public.exams e set questions = coalesce((
    select jsonb_agg(x.v order by x.o) from jsonb_array_elements(e.questions) with ordinality x(v, o)
    where not exists (select 1 from bo where bo.de = e.id and bo.cau = x.o)), '[]'::jsonb)
where e.id in (693, 701);
update public.exams set published = false where id = 1227;
alter table public.exams enable trigger trg_exams_sync_bank;
-- kiem: 693 33->26, 701 28->24
select id, question_count, jsonb_array_length(questions) n, published from public.exams where id in (693, 701, 1227) order by id;
select count(*) bank_da_an from public.question_bank b join public.bk_bo11cau_20261122_bank k using (id) where b.archived and not k.archived;
commit;
