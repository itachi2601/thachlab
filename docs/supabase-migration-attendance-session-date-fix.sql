-- Sửa dữ liệu cũ: session_date từng bị tính qua UTC (start.toISOString().slice(0,10))
-- nên buổi mở trước 7h sáng giờ VN bị lùi 1 ngày. Tính lại từ starts_at theo giờ VN.
-- Chạy MỘT LẦN, an toàn để chạy lại nhiều lần (idempotent).

update public.attendance_sessions
set session_date = (starts_at at time zone 'Asia/Ho_Chi_Minh')::date
where session_date <> (starts_at at time zone 'Asia/Ho_Chi_Minh')::date;
