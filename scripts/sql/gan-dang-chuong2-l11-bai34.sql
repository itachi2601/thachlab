-- Gán dạng bài tập cho câu ngân hàng (sinh bởi skill on-tap-dang-bai-tap). Rollback: delete from public.question_dang where source = 'claude-2026-11-05-chuong2-l11-bai34';
begin;
insert into public.question_dang (question_id, lesson_id, dang_label, unsure, source)
select v.qid, v.lid, v.label, v.unsure, 'claude-2026-11-05-chuong2-l11-bai34'
from (values
  (7265, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', false),
  (1233091, 34, 'Dạng 2 · Trung bình · Ống một đầu kín: dự đoán các vị trí cộng hưởng', true),
  (7258, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', false),
  (7269, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', true),
  (7254, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', false),
  (7267, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', false),
  (7268, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', false),
  (1247587, 34, 'Dạng 3 · Trung bình · Từ hai lần cộng hưởng tính bước sóng, tốc độ và đoạn e', true),
  (7264, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', false),
  (1232564, 34, 'Dạng 3 · Trung bình · Từ hai lần cộng hưởng tính bước sóng, tốc độ và đoạn e', true),
  (7260, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', true),
  (7247, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', false),
  (7259, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', false),
  (7257, 34, 'Dạng 4 · Khó · Xử lý bảng số liệu: sai số và so với giá trị tham khảo', false),
  (7263, 34, 'Dạng 3 · Trung bình · Từ hai lần cộng hưởng tính bước sóng, tốc độ và đoạn e', true)
) as v(qid, lid, label, unsure)
join public.question_bank qb on qb.id = v.qid
on conflict (question_id, lesson_id) do update set dang_label = excluded.dang_label, unsure = excluded.unsure, source = 'claude-2026-11-05-chuong2-l11-bai34';
commit;
