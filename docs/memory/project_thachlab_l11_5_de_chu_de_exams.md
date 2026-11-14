---
name: project_thachlab_l11_5_de_chu_de_exams
description: Vá tên chủ đề lớp 10 còn sót trong exams.questions của 5 đề L11 (701: 17 câu, 638: 1 câu) sau khi bank đã sạch — chạy SAU 22H
metadata:
  type: project
---
**Trạng thái 14/11/2026:** `fix_grade` + `gan_lai_chu_de` đã áp (chạy ~09:00 trong giao dịch tắt `trg_exams_sync_bank`, giữ khoá `exams` ~3 phút). Bank sạch (0 câu grade 11 chủ đề lớp 10). CÒN: `exams.questions` đề 701 (17/28 câu) + 638 (1/21) mang tên chủ đề lớp 10 (khoá JSON là `topic`, không phải topic_id); chủ đề rỗng: bank đề 701 21 câu, đề 693 7 câu.
**Why:** trigger `trg_bank_tags_to_exams` chỉ lan tới đề theo content_hash; bank dedup nên nhiều câu của 701 có `source_exam_id` là đề khác → khớp theo (source_exam_id, source_index) sai (trùng nhiều dòng).
**How to apply:** (1) kiểm xem 17 câu của 701 có thuộc danh sách 129 id trong `supabase/migrations/20261006130000_gan_lai_chu_de_5_de_l11.sql` không (so content_hash, không so source_index); nếu ngoài danh sách thì có thể KHÔNG phải lỗi. (2) Nếu cần vá: mẫu `lib/sua-dinh-dang.ts` + `scripts/sua-dinh-dang-hang-loat.mts`, sau 22h, dry-run → sao lưu `exams` 5 đề → giao dịch tắt `trg_exams_sync_bank`, `statement_timeout` 300s, chạy `supabase db query --linked -f` từ thư mục chính (worktree chưa link). Client có thể báo 524 dù server đã commit → kiểm lại bằng truy vấn.
Liên quan [[project_thachlab_ngan_hang_cau_hoi_skill]].
