---
name: project-thachlab-va-bao-mat-2026-11
description: "Rà soát + vá bảo mật thachlab 11–12/11/2026 (exams.questions, notify_user, quiz CNC chấm server, ruleset GitHub) — đã xong gì, còn lỗ nào, cách đẩy main sau khi có ruleset"
metadata:
  node_type: memory
  type: project
  originSessionId: d337e9ac-21d7-47d3-974d-53e372187226
  modified: 2026-11-12T05:04:57.266Z
---

**Mục tiêu**: thầy nhờ rà bảo mật ngày 2026-11-11 vì học sinh nói "phá được website qua GitHub". Rà GitHub, khoá bí mật, RLS/RPC Supabase, Edge Function, site thật; vá các lỗ DB.

**Đã xong (đều đã chạy trên DB, đã vào main, client đã deploy)** — nhánh `claude/thachlab-security-audit-8b86fd`, commit cuối `44ab88e01`:
- `20261111190000` (11/11 ~18:45): `notify_user_staff`, `get_cnc_quiz_banks`, `cnc_milling_quiz_save`, `exam_has_essay`; xoá `rank_fix_quiz_submit(bigint,int)`.
- `20261111200000` (2026-11-12 06:40): thu quyền đọc `exams.questions` của anon/authenticated (đọc theo 12 cột còn lại), `notify_user` + `rank_gate_pool_ids` thành nội bộ, bỏ policy anon ghi `cnc_milling_quiz_attempts`. Staff đọc đáp án qua view `exams_staff`.
- `20261112070000` (08:15): `record_cnc_learning_result` kiểm đầu vào, thôi mở cho anon.
- `20261112090000` + `20261112100000` (08:45, 08:52): `cnc_quiz_submit` chấm 15 quiz trắc nghiệm CNC ở server (bảng ánh xạ trong `cnc_quiz_bank_of`: final ×7 và exercise-1/2 đạt 80%; machine-operation/tool-setup đạt 100%); hàm cũ từ chối điểm/"đạt" của 15 bài này.
- Client deploy 2026-11-12 ~08:50 = commit `874bef7f6` + 6 file (`TeacherThptAlerts.tsx`, `lib/tro-giang/queries.ts`, `services/cnc-exam-bank.ts`, `services/cnc-milling-quiz-attempts.ts`, `CncCourseWorkspace.tsx`, `services/cnc-learning-records.ts`). Deploy hẹp: worktree tạm ở commit đang chạy + `git checkout <commit> -- <file>` + `bash scripts/deploy.sh`.
- Rollback từng file ở `perf/rollback/<cùng tên>.down.sql`; log ở `scripts/logs/`.

**Còn chờ**:
- Chưa có lượt nộp nào của sinh viên thật qua `cnc_quiz_submit` (admin không ghi điểm). Sau buổi CNC tới: xem `cnc_learning_records` có dòng mới của 15 bài không; không có = lỗi. Tab SV mở trước 08:50 ngày 12/11 phải tải lại.
- Chưa bấm thử nút nhắc làm bài (`notify_user_staff`) và giao diện bằng tài khoản HS/TA.
- Chưa vá (cần đổi client, thầy quyết): bài CNC chấm ở máy (dịch lệnh trả lời ngắn, điền khuyết, viết chương trình, checklist — đáp án nằm trong mã client), `practice_sessions.score` (HS tự insert điểm, có trigger rank), `question_bank` lộ đáp án qua policy exit-quiz/diagnostic, mật khẩu mặc định = mã số HS, CSP report-only, nâng gói npm (next critical).
- GitHub (chỉ thầy làm được): repo vẫn công khai; `nhmkct1`, `zKdKaidO` vẫn quyền ghi.

**Quyết định/điều không tự suy ra từ code**:
- Ruleset GitHub `bao-ve-main-deploy` (tạo 2026-11-12 06:46) chỉ cho admin cập nhật `main`/`deploy` → workflow `gop-claude-vao-main.yml` bị GH013, KHÔNG tự gộp nữa. Phiên Mac: `git merge origin/main` rồi `git push origin HEAD:main` (fast-forward, quyền admin của thầy). Phiên cloud không vào main được — chờ thầy quyết (đổi ruleset hoặc bỏ workflow).
- Đáp án vẫn gửi về máy trong `get_cnc_quiz_banks`: cố ý, vì quiz CNC cho xem đáp án sau khi nộp và làm lại không giới hạn; server chấm chỉ chặn việc gửi thẳng điểm.
- 7 dòng `tool-setup` có best=20 > total=19 là do ngân hàng từng rút còn 19 câu, không phải gian lận.
- Script đăng nhập tài khoản thường mà đọc `exams.questions` phải đổi sang `exams_staff`.
- Chạy SQL từ worktree: `supabase db query --linked -f <file>` trong tab terminal, đứng ở `/Users/MAC/Projects/thachlab` (worktree không có `supabase/.temp`). Kiểm bằng khối `do $t$` đổi vai rồi `raise exception 'KETQUA…'` để tự rollback.

Liên quan: [[project_thachlab_hosting]], [[project_thachlab_cnc_flipped]], [[project_thachlab_concurrent_sessions]].
