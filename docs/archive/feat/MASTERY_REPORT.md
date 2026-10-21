# Báo cáo — nhánh `feat/mastery` (Agent C)

25/9/2026. Đọc trước: `feat/SURVEY.md` mục 1 + mục 5 (Agent C), `docs/mastery-rules.md`.

## Tóm tắt

Xây lớp "mức độ thành thạo" (mastery) theo YCCĐ trên nền dữ liệu đã có sẵn
(`exam_question_results` + `practice_question_results`), không tạo bảng mới. 2 RPC Postgres +
lớp service TypeScript + 3 component React + gắn vào 2 trang phía học sinh. Migration **chưa
chạy lên production** — đã kiểm thử logic bằng giao dịch tạo-hàm-rồi-ROLLBACK trên dữ liệu thật
(chi tiết mục "Kết quả thử nghiệm").

## File đã sửa / tạo

Mới:
- `docs/mastery-rules.md` — quy tắc tính mastery, ngưỡng nhãn, công thức, lý do dùng earned/max,
  ghi chú lệch màu so với đặc tả gốc, điểm mở rộng difficulty để dành cho sau.
- `supabase/migrations/20260925160000_mastery.sql` — 2 RPC `get_lesson_mastery`,
  `get_chapter_mastery` (xem chữ ký bên dưới). **CHƯA CHẠY**.
- `services/mastery.ts` — `fetchLessonMastery`, `fetchChapterMastery`, types
  `MasteryLevel/TopicMastery/LessonMastery`, hằng nhãn/icon/tone, `needsPractice`.
- `components/mastery/MasteryBadge.tsx` — icon ✅🟡🔴⚪ nhỏ cạnh tên bài.
- `components/mastery/LessonMasteryCard.tsx` — thẻ mastery từng YCCĐ + nhãn cả bài, nút "Làm mới",
  nút "Luyện 10 câu phần này".
- `components/mastery/TopicPracticeModal.tsx` — phiên luyện nhanh theo đúng 1 YCCĐ (tái dùng
  plumbing luyện tập hiện có, xem mục "Quyết định thiết kế: nút Luyện 10 câu").

Sửa (chỉ trong vùng được giao):
- `app/lop-hoc/bai/page.tsx` — thêm `lessonExamIds` (từ `items` đã tải sẵn, không query mới) +
  render `<LessonMasteryCard>` ngay trước `{pager}` cuối trang.
- `app/lop-hoc/page.tsx` — thêm state `chapterMastery` (cache theo `chapterId`), hàm
  `ensureChapterMastery` gọi `get_chapter_mastery` **chỉ cho chương đang mở** (mặc định trang chỉ
  mở sẵn 1 chương → đúng 1 RPC lúc tải trang; mở thêm chương mới gọi thêm, có cache chống gọi
  lặp), và render `<MasteryBadge>` cạnh tên bài trong danh sách.

**Không đụng** `ExamReviewPager.tsx`, `ExamRunner.tsx`, `PracticeSession.tsx`,
`components/admin/**`, trang Đăng đề/Sửa đề — đúng phạm vi được giao (xem "Quyết định thiết kế"
bên dưới về lý do không sửa 3 file exam đầu).

## RPC mới

### `public.get_lesson_mastery(p_lesson bigint) returns table(topic_id bigint, topic_name text, sort_order integer, answered_count integer, level text, pct integer, is_summary boolean)`
`security invoker`. Trả 1 dòng/YCCĐ của bài (`is_summary=false`) + 1 dòng tổng kết cả bài
(`is_summary=true`, các cột topic là null). Dùng `(select auth.uid())` — chỉ trả mastery của chính
người gọi, không nhận `p_student` (giữ đúng phạm vi "nhãn cho học sinh đang đăng nhập", không mở
rộng cho giáo viên xem hộ — để dành giai đoạn Learning Journey sau, ghi rõ trong comment SQL).

### `public.get_chapter_mastery(p_chapter bigint) returns table(lesson_id bigint, lesson_title text, sort_order integer, level text)`
`security invoker`. 1 dòng/bài trong chương, gọi lại `get_lesson_mastery` qua `lateral join` (một
nguồn logic duy nhất, theo đúng cách `ta_monthly_scores` bọc `ta_monthly_score` trong
`supabase/migrations/20260925130000_perf_rpc_gv.sql`).

Cả hai **không nới RLS** — chạy dưới quyền người gọi, dựa hoàn toàn vào policy đã có sẵn trên
`exam_question_results`/`practice_question_results` (`student_id = auth.uid() OR
teaches_student(...)`).

## Quyết định thiết kế: nút "Luyện 10 câu phần này"

Đặc tả gốc gợi ý "bốc câu cùng topic_id bằng phiên luyện tập hiện có" và dẫn tới
`services/tutoring.ts`. Sau khi khảo sát kỹ (không đoán):

- `services/tutoring.ts` **không có** cơ chế bốc câu theo topic — chỉ quản lý `tutoring_needs`
  (mục cần phụ đạo) và `tutoring_slots` (lịch phụ đạo), không tạo phiên luyện tập.
- Cơ chế "bốc N câu cùng chủ đề" có thật DUY NHẤT ở `rank_fix_quiz_start`
  (`docs/supabase-migration-rank-system.sql`, gọi qua `services/rank.ts:startFixQuiz` +
  `components/rank/FixQuizModal.tsx`) — nhưng nó: (a) cần một `exam_result_id` có thật (không có ở
  ngữ cảnh "cuối bài học" hay "sau khi nộp phiên luyện tập" — `PracticeSession` không ghi
  `exam_results`); (b) cần mùa rank đang mở + đề đó được cấu hình là nguồn RP; (c) bốc theo topic
  **tầng Bài** (`coalesce(t.parent_id, t.id) = p_topic_id`), không lọc đúng YCCĐ con — nếu truyền
  thẳng id YCCĐ vào sẽ luôn trả 0 câu vì cây chỉ 2 tầng. Không dùng được cho yêu cầu "luyện đúng
  YCCĐ này" mà không có exam_result.
- `question_bank` (nguồn câu hỏi theo `topic_id`) có RLS chỉ mở cho học sinh qua **đúng 1 policy
  hẹp** gắn với `tutoring_needs` đang mở (`docs/supabase-migration-tutoring-needs` /
  `supabase/migrations/20260925140000_perf_rls.sql` dòng ~669). Viết RPC mới `security definer` để
  vòng qua RLS này sẽ vi phạm luật "không nới RLS" của nhánh này.

→ Quyết định: `TopicPracticeModal` bốc câu từ **chính các đề đã gắn vào bài học đang xem**
(`examIds` học sinh đã có quyền đọc sẵn qua đường `fetchExamsFull` mà `PracticeSession.tsx` đang
dùng — không cần RLS/RPC mới), lọc theo `question.topic === topicName` (đúng cách
`exams.questions[].topic` được gắn khi đăng đề, cùng quy ước `buildQuestionResults` đang dùng để
tra `topic_id`), rồi tái dùng **plumbing thật của luồng luyện tập hiện có**: `fetchExamsFull`,
`gradeExam`/`emptyResponses`/`isAnswered`/`pickRandom`, `QuestionCard`, và quan trọng nhất —
`savePracticeSession` (ghi đúng `practice_sessions`/`practice_question_results`, nên lượt luyện
này TỰ ĐỘNG tính vào 10 lượt gần nhất của lần tính mastery kế tiếp — vòng khép kín, không cần đồng
bộ tay).

**Hạn chế đã biết**: nếu YCCĐ đó có câu nhưng chưa từng xuất hiện trong ĐỀ của bài học này (chỉ có
trong `question_bank` chung), nút sẽ báo "chưa có đủ câu hỏi" dù ngân hàng có thể vẫn còn câu ở nơi
khác. Đây là đánh đổi có chủ đích để không nới RLS/không viết RPC bốc-câu mới — nêu rõ để thầy
quyết có chấp nhận không, hoặc cân nhắc mở policy `question_bank` rộng hơn ở một nhánh riêng sau.

## Câu hỏi chưa gắn YCCĐ (mục 4 đặc tả)

Theo `feat/SURVEY.md` mục 3b/3d: chương Động học lớp 10 (`chapter_id=11`) đã gắn `topic_id` cho
100% câu thuộc chương (272/272, xác nhận lại bằng SQL lúc kiểm thử — mục dưới). Không cần viết
`scripts/tag-yccd-dong-hoc-10`. Không phát hiện chương nào khác cần ưu tiên xử lý ngay trong phạm
vi công việc này (493 câu `topic_id is null` trên toàn hệ là orphan không quy được về 1
chương/khối cụ thể — SURVEY.md đã ghi rõ không có cách xác định). Không viết
`scripts/tag-yccd-dry-run.mts` (tuỳ chọn, không bắt buộc, và không có mục tiêu rõ ràng để nhắm
tới sau khi xác nhận Động học 10 đã đạt).

## Kết quả thử nghiệm

Vì luật "migration KHÔNG chạy lên production", đã kiểm thử bằng cách chạy đúng nội dung 2 hàm
trong một giao dịch `BEGIN; create or replace function ...; <test>; ROLLBACK;` qua
`supabase db query --linked -f <file>` (đọc/ghi tạm thời, tự huỷ, không để lại gì — đã xác minh
bằng `select proname from pg_proc where proname in (...)` sau đó trả về rỗng). Mô phỏng
`auth.uid()` bằng `set local role authenticated; set local request.jwt.claim.sub = '<uuid>';`.

- **Học sinh có dữ liệu**: `student_id = b4e8be9f-4e7c-4dfc-af7c-21da5e43975b`, 74 lượt trên 13 YCCĐ
  thuộc chương Động học lớp 10. `get_lesson_mastery(50)` ("Bài 5. Tốc độ và vận tốc") trả đúng 3
  dòng YCCĐ (topic 107 "Phân biệt quãng đường và độ dịch chuyển": 10 lượt, 100%, mastered; topic
  108 "Tốc độ trung bình và vận tốc trung bình": 4 lượt, 43%, weak; topic 109 "Tổng hợp vận tốc,
  tính tương đối của chuyển động": 9 lượt, 22%, weak) + 1 dòng tổng kết `is_summary=true,
  level='weak'` (đúng: thấp nhất trong {mastered, weak, weak} = weak). `get_chapter_mastery(11)`
  trả đủ 10 bài của chương với nhãn hợp lý (`weak` cho bài 5/9 học sinh này yếu, `insufficient` cho
  các bài học sinh chưa đụng tới).
- **Tài khoản/kịch bản chưa có dữ liệu**: `get_lesson_mastery(1)` (bài lớp khác, học sinh này chưa
  từng làm) trả đúng 1 dòng duy nhất (`is_summary=true, level='insufficient'`, không lỗi, không
  trả dòng YCCĐ nào) — đúng hành vi mong đợi khi thiếu dữ liệu hoặc bài không có topic nào khớp.

## `npm run build` / `npx tsc --noEmit`

- `npx tsc --noEmit`: sạch, không lỗi.
- `npm run build`: build thành công (Next.js 16.2.10, Turbopack), 68 trang tĩnh generate xong,
  không lỗi TypeScript trong bước build.
- `npx eslint` trên các file đã sửa: sạch. 3 lỗi `react-hooks/set-state-in-effect` còn lại ở
  `app/lop-hoc/page.tsx` (dòng 103, 189, 222) đã xác minh là lỗi **có sẵn từ trước** (không nằm
  trong diff của nhánh này — `git diff main -- app/lop-hoc/page.tsx` xác nhận các dòng đó không
  đổi), không phải do thay đổi lần này.

## Rủi ro / việc còn lại

- Migration `20260925160000_mastery.sql` chưa chạy — cần thầy xác nhận rồi chạy bằng
  `supabase db query --linked -f supabase/migrations/20260925160000_mastery.sql` (idempotent,
  `create or replace function`). Nếu nhánh `feat/difficulty` cũng đặt file ở đúng mốc
  `20260925160000`, đổi tên 1 trong 2 khi merge (không phụ thuộc bảng/cột của nhau).
- Chưa test UI thật trên trình duyệt (không có phiên trình duyệt sẵn có phù hợp với worktree +
  Supabase auth thật trong phạm vi công việc này) — mới kiểm thử: build/tsc sạch, RPC đúng trên dữ
  liệu thật qua SQL trực tiếp. Đề nghị thầy tự xem `/lop-hoc` (icon cạnh tên bài) và cuối một trang
  `/lop-hoc/bai` (thẻ mastery) sau khi chạy migration.
- Nút "Luyện 10 câu phần này" có hạn chế đã nêu ở trên (chỉ bốc từ đề của chính bài học đang xem,
  không quét toàn ngân hàng câu hỏi theo YCCĐ) — đánh đổi có chủ đích để tuân thủ "không nới RLS".
- `docs/mastery-rules.md` mục 5 đã ghi rõ TODO trọng số Dễ/TB/Khó, để dành tới khi `feat/difficulty`
  merge và quyết định có thêm cột `difficulty` vào `exam_question_results`/`practice_question_results`
  hay không.
- Màu sắc: đặc tả gốc yêu cầu `#0B3D91`/`#F4B400` — hai màu này không tồn tại trong design system
  thật (`app/globals.css`: `--color-primary:#3b82f6`, `--color-accent:#facc15`). Đã đổi sang dùng
  đúng `components/ui/Badge.tsx` (tone success/warning/error/neutral) đang dùng thống nhất toàn
  trang thay vì hex không có thật — ghi rõ lý do trong `docs/mastery-rules.md` mục 2.

## Nhánh & commit

Nhánh: `feat/mastery` (tạo từ `main` @ `3ced896e`).
Commit: xem `git log feat/mastery` — 1 commit duy nhất gồm toàn bộ thay đổi trên, message tiếng
Việt, `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
