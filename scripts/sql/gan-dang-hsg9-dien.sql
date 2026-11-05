-- Gán dạng bài tập cho câu ngân hàng (sinh bởi skill on-tap-dang-bai-tap). Rollback: delete from public.question_dang where source = 'claude-2026-11-05-hsg9-dien';
begin;
insert into public.question_dang (question_id, lesson_id, dang_label, unsure, source)
select v.qid, v.lid, v.label, v.unsure, 'claude-2026-11-05-hsg9-dien'
from (values
  (1255077, 157, 'Dạng 1 · Cơ bản · Mạch hỗn hợp R1 nối tiếp (R2 // R3): bốn bước và tính ngược', true),
  (1192366, 157, 'Dạng 1 · Cơ bản · Mạch hỗn hợp R1 nối tiếp (R2 // R3): bốn bước và tính ngược', true),
  (295966, 157, 'Dạng 6 · Nâng cao · Mạch ba tầng, đọc ampe kế nhánh trong, tính ngược tìm điện trở chưa biết', true),
  (296112, 157, 'Dạng 1 · Cơ bản · Mạch hỗn hợp R1 nối tiếp (R2 // R3): bốn bước và tính ngược', true),
  (1192695, 159, 'Dạng 4 · Trung bình · Đọc đồ thị U–I của hai vật dẫn: điện trở, so sánh độ dốc, ghép nối tiếp – song song', true),
  (1192895, 159, 'Dạng 4 · Trung bình · Đọc đồ thị U–I của hai vật dẫn: điện trở, so sánh độ dốc, ghép nối tiếp – song song', false),
  (1195266, 159, 'Dạng 4 · Trung bình · Đọc đồ thị U–I của hai vật dẫn: điện trở, so sánh độ dốc, ghép nối tiếp – song song', false),
  (1194576, 159, 'Dạng 4 · Trung bình · Đọc đồ thị U–I của hai vật dẫn: điện trở, so sánh độ dốc, ghép nối tiếp – song song', false),
  (1196117, 159, 'Dạng 4 · Trung bình · Đọc đồ thị U–I của hai vật dẫn: điện trở, so sánh độ dốc, ghép nối tiếp – song song', true),
  (1194795, 159, 'Dạng 4 · Trung bình · Đọc đồ thị U–I của hai vật dẫn: điện trở, so sánh độ dốc, ghép nối tiếp – song song', true),
  (1537452, 159, 'Dạng 1 · Dễ · Điện trở dây dẫn R = ρl/S: đổi đơn vị, so sánh hai vật liệu, đường kính dây', false),
  (1475206, 159, 'Dạng 2 · Dễ · Cắt dây thành nhiều đoạn bằng nhau rồi ghép nối tiếp hoặc song song', false),
  (1537451, 159, 'Dạng 1 · Dễ · Điện trở dây dẫn R = ρl/S: đổi đơn vị, so sánh hai vật liệu, đường kính dây', false),
  (1475210, 159, 'Dạng 1 · Dễ · Điện trở dây dẫn R = ρl/S: đổi đơn vị, so sánh hai vật liệu, đường kính dây', false),
  (1475234, 165, 'Dạng 2 · Cơ bản · Hiệu suất bếp, ấm: nhiệt lượng có ích, điện năng, thời gian đun, tiền điện', true),
  (1475236, 165, 'Dạng 2 · Cơ bản · Hiệu suất bếp, ấm: nhiệt lượng có ích, điện năng, thời gian đun, tiền điện', false),
  (1475238, 165, 'Dạng 2 · Cơ bản · Hiệu suất bếp, ấm: nhiệt lượng có ích, điện năng, thời gian đun, tiền điện', false)
) as v(qid, lid, label, unsure)
join public.question_bank qb on qb.id = v.qid
on conflict (question_id, lesson_id) do update set dang_label = excluded.dang_label, unsure = excluded.unsure, source = 'claude-2026-11-05-hsg9-dien';
commit;
