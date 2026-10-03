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
