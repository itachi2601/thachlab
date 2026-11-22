-- CHI DOC (22/11/2026): so luot lam, ket qua, tham chieu bai hoc cua de 693/701/1227/1352
select e.id, e.title, e.published, jsonb_array_length(e.questions) so_cau,
  (select count(*) from exam_attempts a where a.exam_id = e.id) luot_lam,
  (select count(*) from exam_results r where r.exam_id = e.id) ket_qua,
  (select count(*) from lesson_items li where e.id = any(li.exam_ids)) bai_tham_chieu
from exams e where e.id in (693, 701, 1227, 1352) order by e.id;
