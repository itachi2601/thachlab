---
name: project_thachlab_de_xuat_nghien_cuu_hs_14_22
description: "Đề xuất cải tiến từ 5 nhóm nghiên cứu hành vi HS 14–22 (CLT/Mayer, G. Mark, Dahl–Steinberg, SDT, Deterding+Freeman) — 14 việc đã xếp thứ tự, chờ thầy chốt; file docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md"
metadata:
  type: project
---

## Mục tiêu
Đối chiếu nghiên cứu thầy gửi 2026-10-11 với những gì thachlab đã làm (`docs/QUY-TAC-THIET-KE.md`,
`docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`, ROADMAP GĐ 1b, mastery, kho bẫy) → đề xuất cải tiến, không code.

## Đã xong (2026-10-11, nhánh `claude/de-xuat-nghien-cuu-hs-14-22`, đã tự gộp vào main `80be723d`)
- `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md` (3 commit `1f3846a1`, `06344c2a`, `cf1774e6`): mục 1 đọc lại nghiên
  cứu (chỗ tóm tắt nói quá), mục 2 bản đồ đã có/chưa có, mục 3 14 việc A1–E mỗi việc có Vì sao / Lợi ích kỳ vọng
  (giả định) / Đo / Công, mục 4 không nên làm, mục 5 thứ tự 14 việc theo tuần, mục 6 nguồn.
- `docs/STATE.md` thêm 1 dòng ở "CHƯA làm (roadmap)" trỏ tới file.

## Còn chờ
- **Thầy chốt mục 5** (gạch việc không đồng ý). Chưa làm việc nào.
- Thứ tự đề xuất: 1 D2 thử Đố vui `/choi` (kiểm migration `20261006150000_quiz_live` đã chạy chưa) · 2 A1 script đo
  mùa 1 `scripts/do-mua-1.mts` (hạn 25/10) · 3 C2 nhãn "không tính điểm" · 4 A2 cột `sections_opened` vào heartbeat
  `student_learning_presence` · 5 A3 phễu lý thuyết · 6 C1 đổi chuỗi `notify_rp_thuong` · 7 B1 fading theo mastery
  trong `StepwiseSolution` · 8 C3 chọn 1/2 chủ đề ở TodayCard · 9 C5 quyết mùa 2 · 10 B2 luyện đề dài theo phần ·
  11 D1 PhET Dao động L11 (cần thầy duyệt 3 nhiệm vụ + 3 câu/sim) · 12 B3 lint hình · 13 C4 giờ nhắc 20h (gắn M4).

## Quyết định/phát hiện không tự suy từ code
- Con số 47–75 giây của Gloria Mark đo trên nhân viên văn phòng, không phải HS — không thiết kế theo số đó.
- Deterding 2011 chỉ định nghĩa gamification; Hanus & Fox 2015 thấy huy hiệu + bảng xếp hạng làm giảm động lực → mọi
  lớp thưởng mới phải chờ số mùa 1 (A1); nếu phải cắt, cắt bảng tuần cho nhóm dưới trước, giữ tiến bộ tuần.
- `StepwiseSolution` đã có 3 mức `fading` nhưng ghi cứng theo câu (nội dung), chưa thích ứng theo mastery của em.
- Quiz `.tl-quiz` đã có dữ liệu qua `rank_theory_submit`; cái chưa có là đoạn đang đọc về DB (chỉ localStorage).
- Không làm: TikTok hoá bài, Pomodoro trong app, mô phỏng 3D.
