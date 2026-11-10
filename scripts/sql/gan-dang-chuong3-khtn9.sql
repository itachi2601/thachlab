-- Gán dạng bài tập cho câu ngân hàng (sinh bởi skill on-tap-dang-bai-tap). Rollback: delete from public.question_dang where source = 'claude-2026-11-05-chuong3-khtn9';
begin;
insert into public.question_dang (question_id, lesson_id, dang_label, unsure, source)
select v.qid, v.lid, v.label, v.unsure, 'claude-2026-11-05-chuong3-khtn9'
from (values
  (1475204, 89, 'Dạng 1 · Tính điện trở và cường độ dòng điện bằng định luật Ohm', false),
  (1537452, 89, 'Dạng 3 · Điện trở thay đổi theo chiều dài và tiết diện', false),
  (1475206, 89, 'Dạng 3 · Điện trở thay đổi theo chiều dài và tiết diện', false),
  (1537451, 89, 'Dạng 4 · Tổng hợp: tìm vật liệu dây, rồi gập đôi dây', true),
  (1475210, 89, 'Dạng 4 · Tổng hợp: tìm vật liệu dây, rồi gập đôi dây', true),
  (1475222, 90, 'Dạng 2 · Đoạn mạch song song: điện trở tương đương, dòng từng nhánh, dòng mạch chính', false),
  (1475224, 90, 'Dạng 3 · Mạch hỗn hợp: R₁ nối tiếp (R₂ song song R₃)', false),
  (1475238, 91, 'Dạng 2 · Điện năng tiêu thụ và tiền điện trong một tháng', false),
  (1475233, 91, 'Dạng 1 · Từ số ghi trên thiết bị: tính cường độ dòng điện và điện trở', false)
) as v(qid, lid, label, unsure)
join public.question_bank qb on qb.id = v.qid
on conflict (question_id, lesson_id) do update set dang_label = excluded.dang_label, unsure = excluded.unsure, source = 'claude-2026-11-05-chuong3-khtn9';
commit;
