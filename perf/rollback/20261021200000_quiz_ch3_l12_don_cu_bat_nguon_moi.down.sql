-- Hoàn tác 20261021200000: bỏ ẩn câu cũ, gỡ nguồn RP đề mới, xoá thông báo quiz_updated đã gửi hôm đó.
update public.question_bank q set archived = b.archived, note = b.note
  from public.quiz_ch3_l12_bank_backup_20261021 b where q.id = b.id;
delete from public.rank_sources rs using public.quiz_ch3_l12_sources_backup_20261021 b
 where rs.season_id = b.season_id and rs.source_kind = b.source_kind and rs.source_id = b.source_id;
delete from public.notifications where kind = 'quiz_updated' and title = 'Kiểm tra nhanh Chương 3 đã được cập nhật' and created_at::date = date '2026-10-21';
