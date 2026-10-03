---
name: project_thachlab_rank_gate_adaptive
description: "Đánh giá rank 3/10/2026 (dễ ở đỉnh, RP đo nỗ lực không đo năng lực) + spec bàn giao Sonnet: thi thăng hạng thích ứng, luyện từng câu kiểu Duolingo, RP tính lượt đầu — docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md"
metadata:
  type: project
---

3/10/2026 thầy hỏi rank có quá dễ không, muốn: (1) lên bậc phải qua đề kiểm tra thích ứng, (2) chế độ làm
bài kiểu Duolingo (biết ngay đúng/sai, chỉ lỗi sai). Đã đo season 4 ngày 12/35: 177 HS, 120 Tân Binh, 3 Đại Sư
(kẹt vì Cao Thủ/Thách Đấu chưa gắn đề); 71% qua cửa Tinh Anh; config 60 RP/đề điểm tốt nhất + 90 RP/tuần;
làm lại cùng đề 4,64 → 8,48. Kho câu: chỉ 8 danh hiệu lớp 11/12 có ≥20 câu TB, lớp 10 = 0 câu, Khó cả kho 940.

**Why:** RP đo lượng hoạt động; cửa lên bậc chỉ cần Thức Tỉnh (câu Dễ). Giữ RP dễ cho nhóm 25% dưới,
tách trục năng lực sang bài thi thăng hạng.

**How to apply:** spec đầy đủ ở `docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md` (việc A gate thích ứng,
B luyện từng câu + `distractorNotes` backfill, C `rank_on_result` lượt đầu + config mùa 2: practice_max_rp 30,
weekly_goal_rp 40). Chỉ bật A cho lớp 11/12. Việc tay ngay: gắn challenge_exam_id cho cao_thu/thach_dau
season 4. Trạng thái lập trình: xem cuối file này / STATE.md. Liên quan [[thachlab-rank-system]],
[[project_thachlab_title_showcase]].

## Trạng thái lập trình (3/10/2026 — phiên Fable 5.1, Mac, nhánh main, CHƯA push/deploy)
Xong cả 3 việc, 4 migration viết + test trong `begin…rollback` trên prod (sạch), **chưa chạy migration thật** → chưa deploy.
- **A thi thăng hạng thích ứng**: `20261003100000_rank_gate_adaptive.sql` (+ `.down.sql`, test `docs/supabase-test-rank-gate.sql`). RPC `rank_gate_start/answer/finish/attempts_of`; bảng `rank_gate_attempts`; 3 cột `gate_*` ở `rank_tiers` (null = mặc định theo mã bậc); sửa `rank_eval_gates`, `rank_tier_needs_gate` (IMMUTABLE→STABLE), `rank_status_of` (khoá `next.gate.adaptive/attempts/last_passed/cooldown_until/can_start/open_attempt/pass_pct/…`). Config mùa: `gate_adaptive` (1/0; hoặc chuỗi `gate_mode`='static' bằng SQL), `gate_quiz_count` 12, `gate_cooldown_hours` 48. Client: `GateQuizModal` (lazy, mount ở gốc `RankPage`), `GateEntry`, `RankCard`/`TierLadder` đổi chữ, `RankAdmin` (ô ngưỡng ở tab Bậc, lượt thi trong tab Học sinh, lưu config không còn xoá khoá lạ). Chọn lựa khác spec: (1) `level_end` = mức SAU khi chấm câu cuối (mức em giữ được), không phải mức của câu cuối; (2) `gate_min_hard_correct` nullable (không default 0) để "để trống = mặc định"; (3) `rank_gate_answer` có thêm tham số tuỳ chọn `p_question_id` chống bấm trùng; (4) pool chốt lúc bắt đầu (`pool_ids`), loại câu đã gặp ở bài làm/luyện tập + các lượt thi trước; (5) giữ nguyên `rank_gate_passes` sẵn có — HS đã qua cửa bằng danh hiệu KHÔNG phải thi (khối SQL tuỳ chọn cuối migration nếu muốn bắt thi); (6) nút "Thi thăng hạng" ở trang xếp hạng (RankCard chỉ đổi chữ vì cả thẻ là link).
- **C RP lượt đầu**: `20261003110000_rank_rp_first_attempt.sql` (test `docs/supabase-test-rank-rp-first.sql`, fail trước migration/pass sau). Cờ mùa `rp_first_attempt_only` (mặc định 1, có ô ở RankAdmin). RP đã cộng giữ nguyên.
- **B Luyện từng câu**: client `PracticeStepView` (lazy + LazyErrorBoundary), công tắc Từng câu/Cả bài (mặc định Từng câu, nhớ localStorage), "Làm câu tương tự", câu sai quay lại cuối phiên, giãn cách 2 ngày→1 tuần→1 tháng (`features/lessons/practice-step.ts`, chỉ chế độ Từng câu, tối đa 40% phiên). Lưu `savePracticeSession` với đúng/sai LẦN ĐẦU, kể cả câu tương tự; không thêm cột `mode`. `distractorNotes` thêm vào type `ExamQuestion`. **Spec sai một điểm**: Luyện tập đọc `exams.questions` chứ không đọc `question_bank`, và `question_content_hash` là khoá chung đề↔ngân hàng → thêm migration `20261003120000_distractor_notes.sql` (hash bỏ qua `distractorNotes` + hàm `bank_set_distractor_notes` ghi cả hai nơi). Script `scripts/backfill-distractor-notes.mts` (claude-sonnet-5-5, MCQ lớp 11/12 của 8 danh hiệu ưu tiên, có `--dry-run`) — CHƯA chạy.
- Còn treo: thầy chạy migration (thứ tự trong `scripts/run-migrations.sh`) rồi deploy; chưa test với HS thật; 375px chỉ kiểm bằng dữ liệu giả (trình duyệt pane ẩn nên không chụp ảnh, đo DOM: không tràn ngang, đích chạm ≥44px); backfill ghi chú; bật config mùa 2 (`practice_max_rp 30`, `weekly_goal_rp 40`).


**3/10/2026 13:30 — 3 migration ĐÃ CHẠY** trên production (log `scripts/logs/20261003-133029-*`), kiểm: `rank_gate_mode(4)=adaptive`, pool câu lớp 12/11/10 = 4721/1702/779, HS Đại Sư top đã `can_start=true` cho cao_thu. Hàm hash mới = bản prod + bỏ `distractorNotes` (đã đối chiếu). FILES trong run-migrations.sh đã trống. Client đang deploy từ deploy-tree (main b027d772e+). CÒN: test HS thật trên web, backfill `scripts/backfill-distractor-notes.mts 20 --dry-run` rồi thật, cấu hình mùa 2 (practice_max_rp 30, weekly_goal_rp 40), 126 em đã qua cửa Tinh Anh bằng danh hiệu không phải thi lại (khối SQL tuỳ chọn cuối migration A nếu muốn).

**3/10 16:40 — backfill distractorNotes:** lượt 1 ghi 158 câu (bỏ 27% vì lô JSON hỏng); nguyên nhân thật = max_tokens 4096 bị token suy nghĩ ăn hết (xem [[reference_anthropic_api_thinking_max_tokens]]); script sửa `f234f3d60`, lượt vét chạy sạch 0 bỏ qua. Giọng ghi chú: không mở đầu "Em", 10–18 từ, "Phát biểu này đúng: …" cho câu chọn phát biểu sai.
