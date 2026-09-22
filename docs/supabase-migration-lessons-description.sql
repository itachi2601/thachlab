-- Mô tả ngắn (yêu cầu cần đạt) cho từng bài học, hiện dưới tên bài trên trang lớp học.
alter table lessons add column if not exists description text not null default '';
