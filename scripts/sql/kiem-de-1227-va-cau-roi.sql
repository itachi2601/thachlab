-- CHI DOC (22/11/2026): de quiz cu 1227 + 11 cau chu de rong de 693/701 + so luot lam.
select 'de1227' k, e.id, e.title, e.published, (select count(*) from exam_attempts a where a.exam_id = e.id) luot_lam,
       (select count(*) from lesson_items li where e.id = any(li.exam_ids)) lesson_items_tham_chieu
from exams e where e.id in (1227, 1352);
select 'de' k, e.id, (select count(*) from exam_attempts a where a.exam_id = e.id) luot_lam
from exams e where e.id in (693, 701);
select 'cau' k, e.id de, (x.o)::int cau, x.v->>'topic' chu_de, left(regexp_replace(x.v->>'question','<[^>]*>|\s+',' ','g'),90) noi_dung
from exams e cross join lateral jsonb_array_elements(e.questions) with ordinality x(v,o)
where (e.id = 693 and x.o in (5,8,9,14,15,18,26)) or (e.id = 701 and x.o in (8,11,26,27));
