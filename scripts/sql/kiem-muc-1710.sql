-- Chỉ đọc: kiểm mục phụ đạo 1710 (nghi bị chuyển 'tutored' sau khi đã đạt bài tự kiểm tra thoát)
select id, status, first_seen_at, tutored_at, cleared_at, updated_at, left(note, 120) as note
from tutoring_needs where id in (1710, 1718, 1880);

select id, tutoring_need_id, pct, passed, created_at
from tutoring_exit_attempts where tutoring_need_id in (1710, 1718, 1880) order by created_at;

select id, session_id, need_id, created_at
from tutoring_session_topics where need_id in (1710, 1718, 1880) order by created_at;
