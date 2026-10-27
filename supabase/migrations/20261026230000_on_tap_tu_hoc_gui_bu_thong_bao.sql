-- Gửi bù thông báo chuông (trỏ /lop-hoc/on-tap/) cho các buổi "Tự học ở nhà" tạo TRƯỚC migration 20261026210000.
-- Chỉ buổi còn mở (chưa kết thúc, chưa quá hạn). Chạy lại được: bỏ qua em đã có thông báo cùng tiêu đề. Không đụng buổi 'live'.
insert into public.notifications (user_id, kind, title, body, href)
select uc.user_id, 'review_self_new', 'Ôn tập ở nhà: ' || rs.title,
       'Hạn ' || to_char(rs.due_at at time zone 'Asia/Ho_Chi_Minh', 'HH24:MI DD/MM') || ' · bấm để vào làm.',
       '/lop-hoc/on-tap/'
from public.review_sessions rs
join public.user_classes uc on uc.class_id = rs.class_id and uc.status = 'active'
join public.profiles p on p.id = uc.user_id and p.role = 'student'
where rs.mode = 'self' and rs.status <> 'finished' and rs.due_at > now()
  and not exists (
    select 1 from public.notifications n
    where n.user_id = uc.user_id and n.kind = 'review_self_new' and n.title = 'Ôn tập ở nhà: ' || rs.title
  );

-- ROLLBACK: delete from public.notifications where kind = 'review_self_new' and created_at >= '<giờ chạy>';
