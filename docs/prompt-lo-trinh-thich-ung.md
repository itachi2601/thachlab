# Prompt Claude Code — Lộ trình thích ứng: "Bước tiếp theo" + "Khám phá sức mạnh"

> Chạy tại thư mục gốc repo ThachLab, một phiên cloud. Đọc `AGENTS.md`, `docs/STATE.md`,
> `docs/mastery-rules.md`, `docs/PHU-DAO.md`, `docs/KHOA-HOC.md` (mục "Vào lớp trễ") trước.
> Sandbox KHÔNG nối được Supabase (proxy chặn) — migration chỉ viết file, kiểm bằng đọc lại SQL,
> `npx tsc --noEmit`, `npm run build`, `npm run lint` và test thuần cho hàm xếp ưu tiên.

---

## Vấn đề cần giải

Học sinh vào lớp lúc khác nhau, kiến thức chênh nhau, nhưng trang chủ HS (`components/dashboard/
ThptStudentHome.tsx`, hàm `nextLesson` dòng ~251) gợi ý cùng một thứ cho mọi em: bài đầu tiên chưa
hoàn thành theo thứ tự chương. Em giỏi bị ép học lại, em yếu bị đẩy vào bài lớp đang học dù hổng bài
trước, em mới không có dữ liệu nên hệ không biết gì về em.

Mục tiêu: **mỗi lần vào, mỗi em thấy 1 việc chính + 2 lựa chọn phụ đúng với trình độ mình, mỗi việc
≤10 phút, xác suất thành công ~75–85%**, và em mới có "Khám phá sức mạnh" 10 phút để hệ biết em ở đâu.

Hạ tầng đã có, chỉ cần định tuyến (KHÔNG thêm huy hiệu/lớp động lực mới — ROADMAP cấm tới 25/10):
- Nhãn mastery theo YCCĐ: RPC `get_lesson_mastery(p_lesson)` (auth.uid(), ≥4 lượt mới có nhãn),
  `get_chapter_mastery`. Quy tắc ở `docs/mastery-rules.md`.
- Mức câu `difficulty` (`de`/`trung-binh`/`kho`) ở `exams.questions[]`, `question_bank`,
  `practice_question_results.difficulty`. Thang tăng dần `features/lessons/practice-ladder.ts`.
- Luyện theo YCCĐ: `components/mastery/TopicPracticeModal.tsx` (bốc câu từ đề của bài, lọc theo
  `topic`), lưu bằng `savePracticeSession` (`services/lessons.ts`) → `practice_sessions` +
  `practice_question_results`.
- Kênh phụ đạo: `tutoring_needs` (status open/assigned/tutored), `tutoring_exit_attempts` + thời gian
  chờ `EXIT_COOLDOWN_HOURS`, `nextExitAttemptAt` (`services/tutoring.ts`); `TutoringExitQuiz`.
- Bù bài: `thpt_registrations.catchup_topic_ids` (phần tử đầu = bài kế tiếp), `thpt_courses.
  current_topic_id` (mốc lớp đang dạy), RPC `thpt_taught_topics(p_course)`.
- Danh hiệu chuyên môn 3 mức + tiến độ: `rank_my_titles()` → `RankTitle.progress`.
- Học sinh chỉ đọc `question_bank` qua policy exit-quiz → mọi câu luyện/khám phá **bốc từ đề đã
  publish của bài** như `TopicPracticeModal`, không đọc thẳng `question_bank`.

## Luật chung
- Không đổi giao diện các mục đã có, chỉ **thêm** thẻ. Không đổi công thức mastery, RP, danh hiệu.
- Migration: chỉ viết file `supabase/migrations/<timestamp>_*.sql` + rollback `perf/rollback/*.down.sql`,
  cập nhật `FILES` trong `scripts/run-migrations.sh` và mục "ĐANG CHỜ" của `docs/STATE.md`. KHÔNG chạy.
- Trang chủ HS: tối đa **1 RPC mới**, gọi song song với các fetch đang có (Promise.all), không thêm
  query rời. Trang `/lop-hoc/bai` **không thêm round-trip nào**.
- Component mới có JS đáng kể → `next/dynamic({ ssr:false })` + `LazyErrorBoundary`
  (`components/ui/LazyErrorBoundary.tsx`). KaTeX giữ đồng bộ ở trang HS.
- `npx tsc --noEmit`, `npm run build`, `npm run lint` phải sạch trước mỗi commit.
- Commit nhỏ, tiếng Việt: `feat(lo-trinh): ...`. Mỗi việc dưới đây = 1 commit riêng, làm tuần tự.
- Không push, không tạo PR. Cuối cùng in báo cáo + khối lệnh migration cho Thạch (theo AGENTS.md).

---

## Việc 1 — Thẻ "Bước tiếp theo" (rule-based, chạy được ngay với dữ liệu đang có)

### 1a. RPC gộp `get_next_step_snapshot(p_class bigint)` → jsonb (1 migration)
`security invoker`, đọc theo `(select auth.uid())`, chỉ gom dữ liệu — **không xếp ưu tiên trong SQL**.
Trả:
```
{
  "focus_lesson_ids": [..],      -- bài lớp đang dạy + 2 bài liền trước (xem cách chọn dưới)
  "mastery": [ {lesson_id, topic_id, topic_name, form, answered_count, pct, level,
                placement_count} ],   -- từng YCCĐ của focus lessons, tái dùng logic get_lesson_mastery
                                      -- (bọc bằng lateral join, KHÔNG copy công thức; thêm cột
                                      -- placement_count = số lượt từ phiên kind='placement', xem Việc 2)
  "needs": [ {id, topic_id, topic_name, lesson_id, form, status, pct, next_attempt_at} ],
                                      -- tutoring_needs status in (open,assigned,tutored) của em,
                                      -- next_attempt_at tính từ tutoring_exit_attempts + cooldown
  "catchup_next_topic_id": <bigint|null>,   -- thpt_registrations.catchup_topic_ids[1] nếu status='catchup'
  "current_topic_id": <bigint|null>,        -- thpt_courses.current_topic_id của khoá em đã ghi danh
  "has_any_result": <bool>,                 -- em đã có dòng nào trong exam/practice_question_results chưa
  "placement_done_at": <ts|null>            -- phiên kind='placement' gần nhất (null trước Việc 2)
}
```
Chọn `focus_lesson_ids`: nếu có `current_topic_id` → bài của topic đó + 2 bài trước cùng khối theo
`sort_order` chương/bài; nếu không → bài có `exam_question_results` gần nhất của em; vẫn không có →
3 bài đầu chương đầu của khối. Nếu `get_lesson_mastery` chưa nhận `p_student` thì giữ nguyên bản
auth.uid() và bọc lại, đúng ghi chú trong `20260925160000_mastery.sql`.

### 1b. Hàm xếp ưu tiên thuần TS `features/learning/next-steps.ts`
`rankNextSteps(snapshot, ctx): NextStep[]` (tối đa 3, phần tử đầu là việc chính). `ctx` gồm
`classLessons`, `chapters`, `progress` (đã có trong ThptStudentHome), `titles` (RankTitle[]),
`today` (Date). Một `NextStep` = `{ kind, title, why, minutes, reward, href, topicId?, lessonId?,
chapterId?, difficulty? }`.

Thứ tự ưu tiên (dừng khi đủ 3, không lặp cùng topic):
1. `unlock` — need đang mở và `next_attempt_at <= now`: "Mở khoá <topic>" → đọc đoạn lý thuyết của
   bài + 10 câu **Dễ** đúng YCCĐ. **Tối đa 1 bước `unlock`/ngày** (nhớ bằng localStorage
   `thachlab:next-step:unlock-day:<studentId>`), để em yếu không thấy toàn việc sửa lỗi.
2. `near_mastery` — YCCĐ level `practicing` có `pct` cao nhất (< 80): "Còn N câu đúng nữa là Nắm vững"
   (N = số câu đúng cần thêm để 10 lượt gần nhất đạt 80%, tối thiểu 1) → 10 câu mức
   `trung-binh` (pct ≥ 65) hoặc `de` (pct < 65).
3. `fill_data` — YCCĐ của bài `current_topic_id` (hoặc bài focus mới nhất) đang `insufficient`:
   "Mở nhãn <topic>: làm 4 câu" → mức `de`.
4. `catchup` — `catchup_next_topic_id` có: "Bù bài <tên>" → link bài đó (đã có CatchupCard, ở đây
   chỉ trỏ tới). Bỏ qua nếu topic này đã thành bước 1–3.
5. `syllabus` — bài kế tiếp chưa hoàn thành theo giáo trình (logic `nextLesson` hiện tại) **nhưng bỏ
   qua bài mà mọi YCCĐ đã `mastered`**.
6. `challenge` — khi mọi YCCĐ focus đã `mastered`: danh hiệu chuyên môn gần đạt mức kế tiếp nhất
   (theo `RankTitle.progress`, còn thiếu ít câu Khó nhất): "Thử thách Khó: <tên danh hiệu>" → 10 câu
   `kho` của topic thuộc danh hiệu đó.
7. `preview` — vẫn còn chỗ và em đã `mastered` hết focus: "Học trước" bài đầu tiên sau
   `current_topic_id` chưa có dữ liệu.

Luôn kèm 1 việc "chắc thắng" trong 3 việc (mức thấp hơn 1 bậc so với mức hiện tại của em) nếu 2 việc
đầu đều là `unlock`/`near_mastery`. Không bao giờ gợi ý lại YCCĐ đã `mastered` (trừ `challenge` mức Khó).

`reward` ghi rõ và **chỉ dùng phần thưởng đang có**: "+RP luyện tập", "tiến độ danh hiệu <tên>",
"nhãn Nắm vững", "thoát mở khoá". Không hứa thứ chưa có.

Test: `scripts/tests/next-steps.test.mts` chạy bằng `node --import tsx --test` (không thêm framework),
≥6 ca: em mới (rỗng), em vào trễ có catchup, em yếu có 2 need + cooldown chưa hết, em trung bình
practicing 70%, em giỏi mastered hết → challenge/preview, quy tắc 1 unlock/ngày. Thêm script
`"test:next-steps"` vào `package.json`.

### 1c. Thẻ `components/learning/NextStepsCard.tsx`
Đặt **trên cùng** mục "Việc cần làm hôm nay" trong `ThptStudentHome`. Việc chính to, 2 việc phụ nhỏ
dạng chip; mỗi việc: tiêu đề, lý do 1 dòng (`why`), thời gian, phần thưởng, nút. Skeleton khi đang
tải; nếu RPC lỗi → ẩn thẻ, giữ nguyên `nextLesson` cũ (không crash). Mobile 375px phải gọn.
`dailySuggestion` của `DailyStreakCard` lấy từ việc chính thay vì `nextLesson` khi có.

### 1d. Link tới luyện đúng YCCĐ + mức
`/lop-hoc/bai?id=<lesson>&chapter=<ch>&luyen=<topic_id>&muc=<de|trung-binh|kho>&n=10`:
trang bài đọc query, tự mở `TopicPracticeModal` với topic đó, số câu `n`, bốc bằng `pickForLevel`
từ `practice-ladder.ts` theo `muc` (thiếu câu đúng mức thì bù như hàm đã làm). Chỉ client, không
round-trip mới (examIds đã có sẵn ở trang). Với `unlock`, thêm `&ly-thuyet=1` để mở sẵn mục Lý thuyết
của bài trước khi luyện. Với `challenge`, `n=10&muc=kho`.

---

## Việc 2 — "Khám phá sức mạnh" (đầu vào, 1 lần, ~10 phút)

### 2a. Migration
- `alter table practice_sessions add column kind text not null default 'practice'
  check (kind in ('practice','placement'))`, index nhỏ `(student_id, kind)`.
- `savePracticeSession` nhận `kind?: "practice" | "placement"` (mặc định `practice`), fallback khi cột
  chưa có như đang làm với `client_token`.
- `get_next_step_snapshot`: `placement_count` và `placement_done_at` đọc theo `kind='placement'`.
- KHÔNG sửa `get_lesson_mastery` (vẫn ≥4 lượt). Trong `rankNextSteps`, YCCĐ coi là "đủ dữ liệu tạm"
  khi `answered_count >= 4` **hoặc** `placement_count >= 2`; khi đó dùng `pct` để xếp `near_mastery`
  /`fill_data`. Ghi rõ trong comment: nhãn hiển thị vẫn theo mastery-rules, chỉ định tuyến dùng ngưỡng mềm.
- Phiên `placement` có `lesson_id = null`, `item_id = null` → trigger rank bỏ qua (không RP, không
  điểm). Đây là chủ ý: đầu vào không áp lực.

### 2b. Phạm vi và cách bốc câu
- YCCĐ của `focus_lesson_ids` (bài lớp đang dạy + 2 bài trước; em vào sớm chỉ gặp chương đầu).
- Câu bốc từ đề publish của các bài đó (đường của `TopicPracticeModal`), lọc theo YCCĐ, ưu tiên câu
  có `difficulty`. YCCĐ nào < 4 câu khả dụng thì bỏ khỏi khám phá (không hỏi 1 câu rồi kết luận).
- Thích ứng theo từng YCCĐ: 1 câu `trung-binh`; đúng → 1 câu `kho` rồi dừng; sai → 2 câu `de`.
  Tối đa 4 câu/YCCĐ, **tối đa 24 câu/phiên**; nếu nhiều YCCĐ hơn thì ưu tiên bài gần mốc hiện tại.
- Được dừng giữa chừng: lưu phần đã làm (vẫn `kind='placement'`), lần sau chỉ hỏi YCCĐ còn thiếu.

### 2c. Giao diện `components/learning/PlacementSession.tsx` (dynamic + LazyErrorBoundary)
- Thẻ mời ở đầu trang chủ HS khi `has_any_result = false` hoặc (`placement_done_at` null và tổng lượt
  < 10): "Khám phá sức mạnh · 10 phút · không tính điểm". Có nút "Để sau" (localStorage, nhắc lại sau
  3 ngày).
- Trong phiên: thanh tiến độ theo YCCĐ, **không hiện đúng/sai từng câu**, không đồng hồ. Sau mỗi YCCĐ
  hiện "Đã mở khoá <tên>" (dù kết quả thế nào).
- Kết thúc: "Đã mở khoá N/M chủ đề", **không có điểm, không có nhãn đỏ**; hiện ngay
  `NextStepsCard` tính lại từ snapshot mới. Từ "Chưa đạt" tuyệt đối không xuất hiện ở màn này.
- Tái dùng `QuestionCard`/luồng trả lời của `TopicPracticeModal`; không viết bộ render câu hỏi mới.

---

## Việc 3 — Hai đầu không bị bỏ rơi (hoàn thiện Việc 1, không code mới lớn)
- Em giỏi: kiểm bằng test rằng khi mọi YCCĐ focus `mastered`, 3 bước là `challenge` + `preview` +
  1 `syllabus`, không có `fill_data`/`near_mastery` lặp bài cũ.
- Em yếu: kiểm rằng ngày có `unlock` thì 2 bước còn lại có ít nhất 1 việc mức `de` ở YCCĐ em đang
  `practicing` hoặc `mastered` (việc chắc thắng).
- `CatchupCard` và `NextStepsCard` không hiển thị trùng một topic ở hai chỗ với cùng lời kêu gọi:
  nếu topic đã là bước 1–3 thì CatchupCard chỉ hiện dòng "đang là bước tiếp theo".

---

## Kiểm tra trước khi báo xong
1. `npx tsc --noEmit`, `npm run build`, `npm run lint`, `npm run test:next-steps` sạch.
2. Đọc lại SQL migration bằng mắt: `security invoker`, `auth.uid()`, không nới RLS, có
   `revoke all ... from public; grant execute ... to authenticated`, có rollback tương ứng.
3. So dung lượng JS ban đầu `/dashboard` và `/lop-hoc/bai` trước/sau (`perf/chunks-report.mjs`
   nếu còn); `/lop-hoc/bai` không tăng quá 5 KB gzip (chỉ thêm đọc query + mở modal đã có).
4. Không thêm round-trip ở `/lop-hoc/bai`; `/dashboard` thêm đúng 1 RPC.

## Báo cáo cuối (in ra, không tạo file mới ngoài docs đã nêu)
- File đã sửa/thêm; số ca test; số đo JS trước/sau.
- Khối lệnh `bash scripts/run-migrations.sh` + 3 dòng theo AGENTS.md (file làm gì, chạy lúc nào,
  rollback).
- Việc chưa làm và lý do. Nhắc Thạch: backfill mức độ câu còn ~3541 câu trống
  (`npx tsx scripts/backfill-question-bank-difficulty.mts`) — thiếu mức thì thang Dễ/TB/Khó của
  Bước tiếp theo bốc câu chưa nhãn bù vào, hiệu quả giảm.
- Cập nhật `docs/STATE.md` (ĐANG CHỜ + mục "Lộ trình thích ứng") và đánh dấu ROADMAP GĐ 2 mục
  "Bước tiếp theo" là `[~]`.
