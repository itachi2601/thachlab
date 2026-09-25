# Quy tắc tính "mức độ thành thạo" (mastery) theo YCCĐ

Nhánh `feat/mastery`, 25/9/2026. Đọc `feat/SURVEY.md` mục 1 + mục 5 (Agent C) trước khi sửa file
này — đã khảo sát schema thật, không đoán.

## 1. Dữ liệu đầu vào

Gộp hai bảng kết quả làm bài (per-attempt, KHÔNG phải nhãn câu hỏi):
- `public.exam_question_results` (làm đề: kiểm tra, luyện tập gắn đề)
- `public.practice_question_results` (phiên luyện tập tự bốc câu)

Cả hai đều có sẵn `student_id, topic_id (bigint), topic_name, form, qtype, earned, max, is_correct,
created_at` — không cần thêm cột nào.

Với mỗi học sinh × mỗi `topic_id` (tầng YCCĐ): lấy **tối đa 10 dòng gần nhất theo
`created_at desc`**, gộp cả hai bảng trước khi cắt (không phải 10 dòng/bảng).

## 2. Ngưỡng nhãn

Tính trên tối đa 10 lượt gần nhất:

| Điều kiện | Nhãn | Icon | Màu (Badge tone / Tailwind) |
|---|---|---|---|
| Số lượt < 4 | **Chưa đủ dữ liệu** | ⚪ | `neutral` — `bg-slate-500/20 text-slate-400` |
| tỉ lệ đúng ≥ 80% | **Nắm vững** | ✅ | `success` — `bg-emerald-500/15 text-emerald-300` |
| 50% ≤ tỉ lệ < 80% | **Cần luyện thêm** | 🟡 | `warning` — `bg-amber-500/15 text-amber-300` |
| tỉ lệ < 50% | **Chưa đạt** | 🔴 | `error` — `bg-red-500/15 text-red-300` |

Khi "Chưa đủ dữ liệu", kèm gợi ý "Làm thêm N câu" với `N = 4 - số lượt đã có` (tối thiểu 1).

**Ghi chú màu:** đặc tả gốc yêu cầu primary `#0B3D91`/accent `#F4B400`, nhưng hai màu này **không
tồn tại** trong design system thật của repo (`app/globals.css` dùng Tailwind v4 `@theme`:
`--color-primary: #3b82f6`, `--color-accent: #facc15`). Đã đổi sang dùng đúng token/class có sẵn
(`components/ui/Badge.tsx` — 6 tone `success/error/warning/info/violet/neutral`, đã dùng thống nhất
ở `QuestionCard.tsx`) thay vì hex tưởng tượng, để nhãn mastery nhất quán với toàn bộ giao diện.

## 3. Tỉ lệ đúng — công thức thống nhất mọi loại câu

`tỉ lệ = sum(earned) / sum(max)` trên các lượt lấy được (không phải đếm `is_correct` nhị phân).

Lý do dùng `earned/max` thay vì đếm `is_correct`:
- Trắc nghiệm & trả lời ngắn: `earned/max` ∈ {0, 1} — **giống hệt** đếm theo `is_correct`, không
  đổi kết quả.
- Đúng–sai 4 ý (`type: "true_false"`): `gradeQuestion()` (`features/exams/types.ts`) chấm luỹ tiến
  theo số ý đúng — `max` luôn là 1 nhưng `earned` ∈ {0, 0.1, 0.25, 0.5, 1} tương ứng 0/1/2/3/4 ý
  đúng (xem bảng `TF_SCALE`). Đây **đã là** một dạng "tính theo từng ý" được chấm sẵn lúc nộp bài
  và lưu thẳng vào cột `earned`/`max` — không cần đọc lại `statements` thô. Dùng `earned/max` cho
  câu này tự động phản ánh đúng/sai từng ý mà không cần nhánh riêng theo `qtype`.

→ Một công thức `sum(earned)/sum(max)` áp dụng đồng nhất cho mọi `qtype`, không cần switch-case.

## 4. Cấp Bài (lesson-level) và câu chưa gắn YCCĐ

- `question_topics` là cây 2 tầng: `parent_id is null` = tầng Bài (có `lesson_id`), `parent_id is
  not null` = tầng con YCCĐ. Theo trigger `question_topic_tree_guard()`
  (`docs/supabase-migration-topic-outcomes.sql`), mọi YCCĐ con **tự động kế thừa `lesson_id` của
  cha** khi tạo/sửa — nên lọc `question_topics.lesson_id = p_lesson` là lấy đủ cả topic tầng Bài
  lẫn mọi YCCĐ con của bài đó trong một câu, không cần join thêm.
- Câu hỏi gắn thẳng vào **topic tầng Bài** (không có YCCĐ con, ví dụ phần "521 câu tầng Bài" theo
  SURVEY.md mục 3a) → góp vào tính "nhãn của cả bài" nhưng **không** hiện thành một dòng YCCĐ riêng
  (vì nó không phải YCCĐ).
- Nhãn của cả bài = nhãn **thấp nhất** trong các "nhóm" (mỗi YCCĐ con + nhóm câu tầng Bài, nếu có)
  đã đủ dữ liệu, theo thứ tự **Chưa đạt (0) < Cần luyện thêm (1) < Nắm vững (2)**.
  "Chưa đủ dữ liệu" không tham gia so sánh, **trừ khi TẤT CẢ nhóm đều thiếu dữ liệu** → khi đó cả
  bài cũng là "Chưa đủ dữ liệu".
- Câu có `topic_id is null` (493 câu theo SURVEY.md mục 3a) không tính vào bất kỳ nhãn nào — không
  thể quy về một bài/chương cụ thể, bỏ qua hoàn toàn trong `get_lesson_mastery`/`get_chapter_mastery`.

## 5. Điểm mở rộng CHƯA làm — trọng số theo mức độ khó

**Chưa** cộng trọng số Dễ/Trung bình/Khó vào công thức mastery. Lý do: nhánh `feat/difficulty`
(Agent A theo `feat/SURVEY.md` mục 5) đang song song xây hạ tầng `difficulty` — field này **đã tồn
tại** ở `exams.questions[].difficulty` và `question_bank.difficulty` (không phải cột mới), nhưng
`exam_question_results`/`practice_question_results` (bảng nguồn của mastery) **chưa có cột
`difficulty`** ở thời điểm khảo sát 25/9/2026. Khi nhánh `feat/difficulty` merge xong và quyết định
có/không thêm cột `difficulty` vào 2 bảng kết quả (hoặc join ngược qua `topic_id + question_index`
→ `question_bank`), có thể nâng cấp `get_lesson_mastery`/`get_chapter_mastery` để:
- Câu Khó trả lời đúng đóng góp trọng số cao hơn câu Dễ khi tính tỉ lệ "nắm vững".
- Hoặc: chỉ coi "Nắm vững" khi tỉ lệ đúng ở câu mức Khó/Trung bình cũng đạt ngưỡng (không chỉ dựa
  vào câu Dễ).

Việc này để lại như một TODO rõ ràng trong comment SQL của 2 hàm RPC, không chặn nhánh này.

## 6. RPC

- `public.get_lesson_mastery(p_lesson bigint)` — `security invoker`, trả 1 dòng/YCCĐ của bài
  (`topic_id, topic_name, sort_order, answered_count, level, pct, is_summary=false`) **cộng thêm 1
  dòng tổng kết cả bài** (`topic_id=null, is_summary=true, level=<nhãn cả bài>`).
- `public.get_chapter_mastery(p_chapter bigint)` — `security invoker`, trả 1 dòng/bài trong chương
  (`lesson_id, lesson_title, sort_order, level`), gọi lại `get_lesson_mastery` qua `lateral join`
  (giống cách `ta_monthly_scores` bọc `ta_monthly_score` trong
  `supabase/migrations/20260925130000_perf_rpc_gv.sql`) — một nguồn logic duy nhất, không copy công
  thức 2 lần.

Cả hai đều đọc theo `(select auth.uid())` (không nới quyền — học sinh chỉ thấy mastery của chính
mình, đúng RLS hiện có trên `exam_question_results`/`practice_question_results`:
`student_id = auth.uid() OR teaches_student(student_id)`).
