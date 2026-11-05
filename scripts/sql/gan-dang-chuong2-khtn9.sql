-- Gán dạng bài tập cho câu ngân hàng (sinh bởi skill on-tap-dang-bai-tap). Rollback: delete from public.question_dang where source = 'claude-2026-11-05-chuong2-khtn9';
begin;
insert into public.question_dang (question_id, lesson_id, dang_label, unsure, source)
select v.qid, v.lid, v.label, v.unsure, 'claude-2026-11-05-chuong2-khtn9'
from (values
  (377781, 83, 'Dạng 1 · Chiết suất và tốc độ ánh sáng trong môi trường', false),
  (377834, 83, 'Dạng 1 · Chiết suất và tốc độ ánh sáng trong môi trường', false),
  (377622, 83, 'Dạng 1 · Chiết suất và tốc độ ánh sáng trong môi trường', true),
  (378523, 83, 'Dạng 4 · Tia phản xạ và tia khúc xạ: tìm chiết suất và tốc độ ánh sáng', false),
  (377675, 83, 'Dạng 1 · Chiết suất và tốc độ ánh sáng trong môi trường', false),
  (378470, 83, 'Dạng 3 · Tia sáng đi từ thuỷ tinh ra không khí: góc khúc xạ và góc lệch', false),
  (1514912, 83, 'Dạng 1 · Chiết suất và tốc độ ánh sáng trong môi trường', false),
  (456360, 83, 'Dạng 4 · Tia phản xạ và tia khúc xạ: tìm chiết suất và tốc độ ánh sáng', false),
  (377993, 83, 'Dạng 4 · Tia phản xạ và tia khúc xạ: tìm chiết suất và tốc độ ánh sáng', true),
  (377728, 83, 'Dạng 4 · Tia phản xạ và tia khúc xạ: tìm chiết suất và tốc độ ánh sáng', false),
  (378152, 83, 'Dạng 3 · Tia sáng đi từ thuỷ tinh ra không khí: góc khúc xạ và góc lệch', true),
  (377940, 83, 'Dạng 1 · Chiết suất và tốc độ ánh sáng trong môi trường', false),
  (434087, 84, 'Dạng 1 · Tính góc tới hạn khi ra không khí và ra nước', false),
  (434192, 84, 'Dạng 1 · Tính góc tới hạn khi ra không khí và ra nước', false),
  (434122, 84, 'Dạng 1 · Tính góc tới hạn khi ra không khí và ra nước', false)
) as v(qid, lid, label, unsure)
join public.question_bank qb on qb.id = v.qid
on conflict (question_id, lesson_id) do update set dang_label = excluded.dang_label, unsure = excluded.unsure, source = 'claude-2026-11-05-chuong2-khtn9';
commit;
