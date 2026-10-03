-- Xoá 2 phiên "Ôn tổng hợp" thử nghiệm 3/10/2026 (practice_sessions 202 và 203, lesson_id null).
-- Chạy: supabase db query --linked -f scripts/xoa-phien-on-tong-hop-test.sql
-- An toàn: chỉ xoá nếu cả 2 phiên đúng là phiên tổng hợp (lesson_id null, 20 + 30 câu) của cùng 1 học sinh;
-- sai một điều kiện thì dừng, không xoá gì. Không đụng exam_results / rank_* (phiên luyện không cộng RP).
-- Mastery/danh hiệu tính từ practice_question_results nên tự trở lại như trước khi thử.
-- Không có rollback (xoá dữ liệu thử); xem trước bằng khối SELECT ở dưới.

-- Xem trước (chạy riêng được):
-- select s.id, s.student_id, s.lesson_id, s.question_count, s.correct_count, s.created_at,
--   (select count(*) from practice_question_results r where r.session_id = s.id) as results
-- from practice_sessions s where s.id in (202, 203) order by s.id;

begin;

do $$
declare n int; students int;
begin
  select count(*), count(distinct student_id) into n, students
  from practice_sessions
  where id in (202, 203) and lesson_id is null and question_count in (20, 30);
  if n <> 2 or students <> 1 then
    raise exception 'Không khớp phiên thử (khớp %, học sinh %) — dừng, chưa xoá gì', n, students;
  end if;
end $$;

delete from practice_question_results where session_id in (202, 203);
delete from practice_sessions where id in (202, 203);

-- Kiểm: phải ra 0 và 0
select (select count(*) from practice_sessions where id in (202, 203)) as phien_con_lai,
       (select count(*) from practice_question_results where session_id in (202, 203)) as ket_qua_con_lai;

commit;
