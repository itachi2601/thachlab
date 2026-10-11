-- Hoàn tác: trả các mục đã đóng về trạng thái trước khi dọn
update public.tutoring_needs n
set status = b.status, cleared_at = b.cleared_at, note = b.note
from public.tutoring_needs_backup_20261011 b
where n.id = b.id and n.note = 'không tính câu khó, chưa cần phụ đạo';
