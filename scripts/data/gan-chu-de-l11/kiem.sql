-- Kiểm (CHỈ ĐỌC) 5 đề L11 638/639/658/693/701 so với ánh xạ chủ đề của migration 20261006130000 (không chạy migration đó nữa).
-- 22/11/2026: 126/129 OK; lệch: 658 câu 18 (chủ đề), 701 câu 16, 28 (hash đề ≠ bank). Chạy từ checkout chính: supabase db query --linked -f <file> -o json
-- Chỉ đọc: mọi câu trong 5 đề — chủ đề trong đề vs dòng bank theo hash vs chủ đề đích của ánh xạ (theo dòng gốc cùng đề + vị trí)
with m(qid, tid) as (values (683622,177),(683623,179),(683624,179),(683625,183),(683626,183),(683627,182),(683628,182),(683629,184),(683630,184),(683631,182),(683632,185),(683633,185),(683634,185),(683635,177),(683636,185),(683637,177),(683638,179),(683639,182),(683640,183),(683641,184),(683642,186),(683643,177),(683644,177),(683645,177),(683646,177),(683647,177),(683648,179),(683649,179),(683650,179),(683651,179),(683652,179),(683653,181),(683654,178),(683655,182),(683656,184),(683657,183),(683658,183),(683659,183),(683660,183),(683661,183),(683662,184),(683663,183),(684034,163),(684035,154),(684036,163),(684037,160),(684038,154),(684039,162),(684040,155),(684041,160),(684042,156),(684043,154),(684044,158),(684045,163),(684046,157),(684047,154),(684048,154),(684049,154),(684050,160),(684051,158),(684052,154),(684053,163),(684054,156),(684055,161),(684056,158),(684057,154),(684058,154),(684059,157),(684908,154),(684909,157),(684910,154),(684911,164),(684912,null),(684913,155),(684914,166),(684915,null),(684916,null),(684917,170),(684918,166),(684919,154),(684920,154),(684921,null),(684922,null),(684923,154),(684924,160),(684925,null),(684926,162),(684927,154),(684928,154),(684929,154),(684930,155),(684931,166),(684932,175),(684933,null),(684934,173),(684935,171),(684936,175),(684937,157),(684938,174),(684939,154),(684940,154),(685082,177),(685083,184),(685084,191),(685085,185),(685086,193),(685087,191),(685088,193),(685089,null),(685090,177),(685091,179),(685092,null),(685093,187),(685094,187),(685095,192),(685096,184),(685097,177),(685098,192),(685099,190),(685100,177),(685101,191),(685102,190),(685103,191),(685104,183),(685105,185),(685106,190),(685107,null),(685108,null),(685109,191)),
dich as (select b0.source_exam_id as de, b0.source_index as idx, m.qid, m.tid, t.name as ten_dich
         from m join public.question_bank b0 on b0.id = m.qid left join public.question_topics t on t.id = m.tid),
cau as (select e.id as de, (x.o-1)::int as idx, x.v->>'topic' as topic_de, public.question_content_hash(x.v) as h,
               left(regexp_replace(x.v->>'question', '<[^>]*>|\s+', ' ', 'g'), 60) as de_bai
        from public.exams e cross join lateral jsonb_array_elements(e.questions) with ordinality x(v,o)
        where e.id in (638,639,658,693,701))
select c.de, c.idx+1 as cau, d.qid as goc, d.ten_dich, c.topic_de, b.id as bank_hash, b.topic_id, tb.name as ten_theo_id, b.topic_name as bank_ten, b.grade, b.archived,
       case when b.id is null then 'KHONG_BANK'
            when d.qid is null then 'KHONG_ANH_XA'
            when coalesce(c.topic_de,'') is distinct from coalesce(d.ten_dich,'') then 'DE_LECH'
            when coalesce(b.topic_name,'') is distinct from coalesce(d.ten_dich,'') then 'BANK_TEN_LECH'
            when b.topic_id is distinct from d.tid then 'BANK_ID_LECH' else 'OK' end as tt,
       c.de_bai
from cau c left join dich d on d.de = c.de and d.idx = c.idx
left join public.question_bank b on b.content_hash = c.h
left join public.question_topics tb on tb.id = b.topic_id
order by (case when b.id is null or d.qid is null or coalesce(c.topic_de,'') is distinct from coalesce(d.ten_dich,'') or coalesce(b.topic_name,'') is distinct from coalesce(d.ten_dich,'') or b.topic_id is distinct from d.tid then 0 else 1 end), c.de, c.idx;
