# Bàn giao lập trình — Thi thăng hạng thích ứng + Luyện từng câu (3/10/2026)

Người viết: phiên Fable 5.1 (phân tích). Người làm: phiên Sonnet. Thầy Thạch đã duyệt hướng đi ở
hội thoại 3/10/2026; bản này là spec kỹ thuật, không cần hỏi lại phần "làm gì", chỉ hỏi khi gặp mâu
thuẫn với code thật.

Đọc trước khi code: `AGENTS.md` (quy tắc migration, không tự chạy lên production), `docs/STATE.md`,
`docs/DATABASE.md` (bảng `rank_*`, `question_bank`, `practice_*`), `docs/DATABASE-RPC.md` (chữ ký RPC),
`docs/QUY-TAC-THIET-KE.md` (mọi UI học sinh). Nguồn SQL gốc của hệ rank:
`docs/supabase-migration-rank-system.sql` (đã chạy) + các file `supabase/migrations/2026092*_rank_*.sql`.

---

## 0. Vì sao làm (tóm tắt số liệu 3/10, season 4, ngày 12/35)

| Chỉ số | Giá trị |
|---|---|
| HS trong mùa / Tân Binh / Chiến Binh / Tinh Anh / Tinh Nhuệ / Đại Sư | 177 / 120 / 22 / 31 / 1 / 3 |
| Đã qua cửa Tinh Anh (chỉ cần 1 Thức Tỉnh = câu Dễ) | 126 (71%) |
| Config season 4: RP/đề (điểm tốt nhất) · RP mục tiêu tuần (2 bài ≥7) · RP sửa sai | 60 · 90 · 30 |
| Làm lại cùng đề: điểm lượt đầu → điểm tốt nhất (56 cặp) | 4,64 → 8,48 |
| Cao Thủ / Thách Đấu | không ai lên được vì `challenge_exam_id` null |

Kết luận đã chốt: **RP đo nỗ lực (giữ dễ), lên bậc phải qua bài thi thăng hạng thích ứng đo năng
lực.** Luyện tập thêm chế độ phản hồi từng câu để học; đề kiểm tra (ExamRunner) giữ nguyên nộp cả bài.

---

## 1. Phạm vi — 3 việc, làm theo thứ tự

| # | Việc | Loại | Ước lượng |
|---|---|---|---|
| A | Thi thăng hạng thích ứng (gate exam sinh từ `question_bank`) | 1 migration + 1 RPC start/answer/finish + 1 modal HS + 1 ô cấu hình admin | lớn |
| B | Luyện từng câu (Duolingo) trong `PracticeSession` | client + 1 trường mới trong `question.json` (ghi chú phương án nhiễu, backfill sau) | vừa |
| C | Cân bằng RP mùa 2 | sửa `rank_on_result` tính lượt ĐẦU; còn lại là config | nhỏ |

Không làm trong đợt này: IRT/mô hình năng lực thật, "tim" trừ mạng, lớp 10 (kho câu = 0), thay
ExamRunner của đề kiểm tra.

---

## 2. Việc A — Thi thăng hạng thích ứng

### 2.1 Hành vi
- Khi `rp >= next_tier.min_rp` nhưng bậc kế tiếp cần cửa (`rank_tier_needs_gate`), HS thấy nút
  **"Thi thăng hạng"** ở `RankCard`/`RankPage` (chỗ hiện đang ghi "cần đề thử thách").
- Bài gồm `gate_quiz_count` câu (mặc định 12), bốc từ `question_bank` theo **các topic của mọi danh
  hiệu chuyên môn thuộc khối lớp của HS** (`rank_title_topics` ⨝ `rank_titles.kind='specialist'`,
  lọc `question_bank.grade` theo lớp HS; nếu cột grade không khớp định dạng thì lọc theo
  `question_topics` của khối). Loại `qtype='essay'`, loại câu HS đã gặp: `content_hash` có trong
  `exam_question_results`/`practice_question_results` của HS (join qua `exams.questions`/
  `question_bank.content_hash` — xem cách `rank_fix_quiz_start` dùng `question_content_hash`).
- **Thích ứng bậc thang** (server quyết định câu kế tiếp, client không được chọn):
  bắt đầu `trung-binh`; đúng → lên 1 mức (tối đa `kho`), sai → xuống 1 mức (tối thiểu `de`).
  Hết pool ở một mức thì lấy mức kề.
- **Điều kiện qua** (lưu trong `rank_tiers` cột mới, có mặc định):

| Bậc (code) | `gate_pass_pct` | `gate_min_hard_correct` | `gate_min_level_held` |
|---|---|---|---|
| chien_binh | không thi | | |
| tinh_anh | 70 | 0 | de |
| tinh_nhue | 70 | 0 | trung-binh |
| dai_su | 75 | 2 | trung-binh |
| cao_thu | 80 | 3 | trung-binh |
| thach_dau | 80 | 4 | kho |

  `gate_min_level_held` = mức mà HS phải kết thúc bài ở đó hoặc cao hơn (mức của câu cuối cùng).
  Điều kiện danh hiệu hiện có (`required_title_count/level`) **giữ nguyên, cộng thêm** điều kiện thi.
- **Trượt**: không trừ RP, không mất gì. Chờ `gate_cooldown_hours` (mặc định 48) mới thi lại. Nhãn
  HS: "Đủ RP rồi, còn bài thi thăng hạng" + đồng hồ chờ. Không giới hạn tổng số lượt.
- **Đỗ**: insert `rank_gate_passes` (evidence = `{attempt_id, pct, hard_correct, level_end}`) rồi
  `rank_refresh_student` → lên bậc ngay, hiện màn chúc mừng (dùng animation sẵn có của lên bậc nếu
  có, không thêm thư viện).
- Nếu `rank_tiers.challenge_exam_id` **không null** thì giữ cơ chế cũ (đề tĩnh) cho bậc đó — admin
  được chọn 1 trong 2; config mùa `gate_mode` ∈ {`adaptive`, `static`}, mặc định `adaptive`.
- Thi thăng hạng **không cộng RP**, **không** ghi `practice_question_results` (tránh làm lệch
  mastery/danh hiệu), nhưng ghi từng câu vào bảng riêng để GV xem.

### 2.2 Dữ liệu (1 migration, tên `supabase/migrations/20261003100000_rank_gate_adaptive.sql`, kèm
`perf/rollback/20261003100000_rank_gate_adaptive.down.sql`)
```
alter table rank_tiers add column gate_pass_pct int, gate_min_hard_correct int default 0,
  gate_min_level_held text;            -- null → dùng mặc định bảng trên theo code
create table rank_gate_attempts (
  id bigserial pk, season_id, student_id, tier_code text, status text ('open'|'done'),
  question_ids bigint[] default '{}', answers jsonb default '[]',   -- [{qid, level, correct}]
  level_cur text, correct int, total int, hard_correct int, pct int, passed bool,
  created_at, submitted_at, unique open per (season,student,tier) bằng partial index
);
RLS: HS đọc dòng của mình; ghi chỉ qua RPC security definer. Staff đọc hết (rank_is_staff).
```
RPC (security definer, `grant execute to authenticated`):
- `rank_gate_start(p_tier_code text) → jsonb {attempt_id, total, question}`: kiểm `rp >= min_rp`,
  cooldown, lượt đang mở thì trả tiếp câu hiện tại; bốc câu đầu mức TB. Trả câu dạng
  `question_bank.question` (cùng shape `ExamQuestion`) **bỏ `answer`/`explanation`** (client không
  được thấy đáp án khi thi).
- `rank_gate_answer(p_attempt_id bigint, p_response jsonb) → jsonb {correct, next_question|null,
  done, index}`: chấm phía DB (viết `rank_grade_question(question jsonb, response jsonb) → boolean`
  cho 3 dạng: `options` → so `answer`; `statements` → đúng–sai phải khớp hết; `answer` text → so
  chuẩn hoá số/chuỗi như `gradeExam` ở `features/exams/types.ts`; essay đã loại). Cập nhật
  `answers`, `level_cur`, bốc câu kế theo bậc thang, loại các `question_ids` đã dùng.
- `rank_gate_finish(p_attempt_id) → jsonb {passed, pct, hard_correct, level_end, tier}`: tự gọi khi
  `index = total`; tính đỗ/trượt; đỗ → `rank_gate_passes` + `rank_refresh_student`.
- Sửa `rank_eval_gates`: khi `challenge_exam_id is null` và `gate_mode='adaptive'` → `v_chal_ok`
  = tồn tại `rank_gate_attempts.passed` của bậc đó trong mùa. Bỏ dòng cứng
  `t.code not in ('cao_thu','thach_dau')`.
- Sửa `rank_status_of.next.gate`: thêm `adaptive bool, attempts int, last_passed bool,
  cooldown_until timestamptz, can_start bool` (client cũ bỏ qua khoá lạ — giữ khoá cũ nguyên).
- Thêm `rank_gate_attempts_of(p_student)` cho tab GV (danh sách lượt, từng câu đúng/sai).

Mặc định config: `gate_quiz_count 12`, `gate_cooldown_hours 48`, `gate_mode adaptive`, đọc qua
`rank_cfg(season, key, default)`.

### 2.3 Client
- `features/rank/types.ts`: `GateStatus`, `GateAttempt`, `GateQuestion`.
- `services/rank.ts`: `startGateQuiz`, `answerGateQuiz`, `finishGateQuiz`, `fetchGateAttemptsOf`.
- `components/rank/GateQuizModal.tsx` — **chép khung từ `components/rank/FixQuizModal.tsx`**
  (phase loading/intro/running/result, dùng `QuestionCard`, toast). Khác: mỗi câu gọi
  `answerGateQuiz` rồi mới hiện câu sau; KHÔNG hiện đúng/sai từng câu trong lúc thi (đây là bài đo,
  khác việc B); kết quả cuối hiện % + đỗ/trượt + nếu trượt thì "thi lại sau 48 giờ" + gợi ý 2 chủ đề
  sai nhiều nhất (từ `answers` ⨝ topic). Tách bằng `next/dynamic({ssr:false})` + `LazyErrorBoundary`.
- Gắn nút ở `components/rank/RankCard.tsx` và `RankPage` (tìm chỗ render `gate.challenge_required`).
- `components/admin/RankAdmin.tsx` tab Bậc: thêm 3 ô `gate_pass_pct / gate_min_hard_correct /
  gate_min_level_held` cạnh ô đề thử thách, ghi chú "để trống = mặc định"; `updateTier` đã nhận
  patch tuỳ ý. Tab Tổng quan HS: bảng lượt thi thăng hạng (đọc `rank_gate_attempts_of`).
- UI học sinh theo `docs/QUY-TAC-THIET-KE.md`: 1 câu/màn, đích chạm ≥44px, không đếm ngược gây
  căng (không giới hạn thời gian ở bài thăng hạng), kiểm 375px. Ghi mã quy tắc vào commit.

### 2.4 Kiểm thử
- SQL: file `docs/supabase-test-rank-gate.sql` dạng `begin; ... raise exception '...'; rollback;`
  giả lập JWT HS (xem `docs/memory/reference_supabase_db_query_cli.md`) chạy đủ: start → 12 answer →
  finish đỗ; trường hợp trượt + cooldown; gọi start lần 2 trả lại lượt đang mở; hết pool.
  **Không chạy migration lên production** — chỉ viết file, cập nhật `FILES` trong
  `scripts/run-migrations.sh`, in lệnh cho thầy theo AGENTS.md.
- Client: `npm run build` (hoặc `npx tsc --noEmit` + eslint) sạch; mock RPC để chụp 375px
  intro/running/result.

---

## 3. Việc B — Luyện từng câu (chế độ Duolingo) trong Luyện tập

### 3.1 Hành vi
- Ở `components/lessons/PracticeSession.tsx` thêm công tắc chế độ **"Từng câu"** (mặc định bật cho
  `luyen_tap`; "Cả bài" giữ như cũ, có đồng hồ). Lưu lựa chọn localStorage như `practice-ladder.ts`.
- Mỗi câu: chọn → bấm **Kiểm tra** → hiện ngay đúng/sai, đáp án đúng, `explanation` (98% câu đã có),
  và **lý do phương án em chọn sai** nếu câu có `distractorNotes[<key>]` (trường mới, xem 3.3; chưa
  có thì chỉ hiện lời giải). Sai → thêm nút **"Làm câu tương tự"**: bốc 1 câu cùng `topic` cùng
  `difficulty` từ bank của mục đó chưa dùng trong phiên, chèn ngay sau.
- Câu sai **xếp lại cuối phiên** (làm lại 1 lần, không tính điểm lần 2). Chuỗi đúng trong phiên hiện
  nhỏ ở góc (không có "tim", không trừ mạng — nhóm 25% dưới nhạy với mất mát).
- Kết thúc phiên: vẫn gọi `savePracticeSession` với `picks` + đúng/sai **lần đầu** của mỗi câu →
  `practice_question_results` để mastery/danh hiệu/thang độ khó chạy như cũ. Thêm `mode: 'step'`
  vào payload nếu bảng có cột; không có thì bỏ qua (không thêm migration cho việc B).
- Giãn cách (mục còn treo GĐ 1b): lưu danh sách `{questionHash, dueAt}` câu sai ở localStorage theo
  HS; phiên sau ưu tiên bốc câu đã tới hạn (2 ngày → 1 tuần → 1 tháng). Chỉ client, không round-trip.
- RP: phiên "Từng câu" vẫn đi qua `practice_sessions` nên trigger rank cộng như phiên thường; để
  không phá cân bằng, việc C hạ `practice_max_rp`. Không viết cơ chế RP riêng cho B.

### 3.2 Client
- Tách view mới `components/lessons/PracticeStepView.tsx` (lazy + boundary) dùng lại `QuestionCard`;
  `PracticeRunningView` giữ nguyên cho chế độ cả bài. Chấm bằng `gradeExam`/hàm chấm 1 câu trong
  `features/exams/types.ts` (tách `gradeQuestion` nếu chưa có).
- Thời lượng mục tiêu 10 câu ≈ 8 phút (trung vị hiện 50 giây/câu).
- Theo `docs/QUY-TAC-THIET-KE.md`: phản hồi sai dùng màu + biểu tượng + chữ (không chỉ màu), khối
  giải thích ≤ 60–75 ký tự/dòng, nút Tiếp ở đáy màn trong tầm ngón cái.

### 3.3 Ghi chú phương án nhiễu (`distractorNotes`) — chuẩn bị, không chặn việc B
- Shape trong `question_bank.question`: `"distractorNotes": {"A": "…", "C": "…"}` (khoá = nhãn
  phương án sai; với `statements` dùng chỉ số câu). Thêm vào type `ExamQuestion` (optional).
- Script `scripts/backfill-distractor-notes.mts` theo mẫu `scripts/backfill-question-bank-difficulty.mts`:
  gọi Claude API (`claude-sonnet-5-5`), mỗi câu MCQ sinh 1 câu ≤ 25 từ cho MỖI phương án sai
  nêu đúng lỗi tư duy (nhầm công thức, quên đổi đơn vị, đổi dấu…), **không nhắc "thầy"**, giọng theo
  `docs/memory/feedback_giong-van-bai-ly-thuyet.md`. Tham số = số câu; ghi thật ngay, ưu tiên
  `grade in ('12','11')` và topic của 8 danh hiệu có ≥20 câu TB (chua_te_song, bac_thay_mach_dien,
  vu_cong_lech_pha, bac_thay_nhip_dao_dong, nguoi_truyen_nang_luong, phap_su_dien_truong,
  ke_danh_thuc_dong_dien, ke_tich_tru_loi_dinh). Chạy trên Mac (cần service role). Thử 20 câu trước.

---

## 4. Việc C — Cân bằng RP

- Sửa `rank_on_result` (bản mới nhất là `20260929100000_rank_restore_daily_streak.sql`): RP của một
  đề = **lượt đầu** trong mùa, không phải điểm tốt nhất. Cách làm: trước khi `rank_award`, kiểm đã có
  dòng `rank_rp_awards (season, student, 'practice', kind:id)` chưa → có rồi thì bỏ qua cộng RP (vẫn
  chạy weekly/daily/gates/achievements). Ghi vào cùng migration của việc A (hoặc file riêng
  `20261003110000_rank_rp_first_attempt.sql`, ưu tiên file riêng để rollback độc lập). Cờ config
  `rp_first_attempt_only` (mặc định 1) để tắt được không cần code.
- Config mùa 2 (chỉ UI admin / SQL update, không code): `practice_max_rp 30`, `weekly_goal_rp 40`,
  giữ `fix_max_rp 30`. Ghi đề xuất này vào `docs/STATE.md` mục ĐANG CHỜ, thầy quyết lúc mở mùa 2.
- Việc làm tay ngay (thầy, qua `/quan-tri/xep-hang`): gắn một đề thi thử khó làm `challenge_exam_id`
  cho `cao_thu`/`thach_dau` season 4 để 3 em ở Đại Sư có đích trong 3 tuần còn lại. Sau khi A chạy
  thì bỏ gán để chuyển sang thích ứng.

---

## 5. Quy tắc làm việc (bắt buộc)
- Working tree đang đầy WIP của phiên khác: chỉ `git add`/`git commit -- <đúng file của mình>`.
  Không format/dọn file ngoài phạm vi. File dùng chung (`docs/STATE.md`, `scripts/run-migrations.sh`,
  `docs/memory/MEMORY.md`): chỉ thêm dòng.
- Không chạy migration, không `supabase db push`, không lệnh ghi lên production. Đọc để kiểm
  (`supabase db query --linked -f file.sql` với `begin … rollback`) thì được.
- Mỗi chunk JS mới ở trang HS: `next/dynamic({ssr:false})` + `LazyErrorBoundary`. Không thêm
  round-trip Supabase mới cho `/lop-hoc/bai` ngoài các RPC nêu ở đây (thi thăng hạng nằm ở trang
  rank/tài khoản, không ở trang bài).
- Commit tách theo việc: A (migration + client), B (client), C (migration). Ghi mã quy tắc thiết kế
  vào mô tả commit.
- Kết thúc: cập nhật `FILES` trong `scripts/run-migrations.sh`, mục ĐANG CHỜ trong `docs/STATE.md`,
  memory `docs/memory/project_thachlab_rank_gate_adaptive.md` (tạo mới), in khối lệnh
  `bash scripts/run-migrations.sh` + 3 dòng theo AGENTS.md. Không deploy khi migration chưa chạy
  (client đọc khoá mới trong `rank_status_of` sẽ trống → nút ẩn, không crash; ghi rõ điều này).

## 6. Tiêu chí chấp nhận
- [ ] Test SQL `docs/supabase-test-rank-gate.sql` chạy sạch trong `begin/rollback` trên production.
- [ ] HS đủ RP + thiếu cửa thấy nút Thi thăng hạng; thi 12 câu, đáp án không lộ trong payload mạng.
- [ ] Trượt → cooldown 48h hiện đúng; đỗ → bậc đổi ngay không cần tải lại.
- [ ] Admin chỉnh được ngưỡng từng bậc; để trống dùng mặc định.
- [ ] Luyện tập có công tắc Từng câu/Cả bài; sai hiện lời giải + ghi chú nhiễu nếu có + Làm câu tương tự;
      kết quả vẫn ghi `practice_question_results` đúng lần đầu.
- [ ] `rank_on_result` chỉ cộng RP lượt đầu khi `rp_first_attempt_only=1`; recompute không cộng đôi.
- [ ] Build sạch; chụp 375px cho modal thi và màn luyện từng câu.
