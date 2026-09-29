# Khảo sát Phase 0 — 3 tính năng song song (Vật lý THPT thachlab)

Ngày khảo sát: 25/9/2026. Chỉ đọc (schema thật qua `supabase db query --linked`, đọc code), không sửa code, không chạy migration.

## 1. Schema các bảng liên quan

Đọc trực tiếp từ `information_schema.columns` (không đoán).

### `question_topics` (cây 2 tầng)
`id, created_at, subject_code, grade, chapter_id, lesson_id, name, sort_order, parent_id`
- `parent_id is null` → tầng "Bài" (gắn `lesson_id`); `parent_id is not null` → tầng con "YCCĐ/Dạng".
- `chapter_id` trỏ `chapters(id, title, sort_order, subject_code)`. `grade` là text ('9'/'10'/'11'/'12').

### `question_bank`
`id, created_at, updated_at, subject_code, grade, topic_id, topic_name, form, qtype, difficulty, question (jsonb), content_hash, source_exam_id, source_index, archived, note, figure_not_needed`
- **Xác nhận: KHÔNG có cột `difficulty_source`** (gv/ai) — đúng như bối cảnh đã biết.
- `difficulty` là text: `''|'de'|'trung-binh'|'kho'`.
- Cột `question` (jsonb) là bản sao/nguồn của câu hỏi — cùng cấu trúc với 1 phần tử trong `exams.questions`.

### `exams`
`id, created_at, title, duration_minutes, published, questions (jsonb), question_count, topic, difficulty (mức cả đề), type_counts, subject_code, cnc_key, pass_score`

### Cấu trúc từng phần tử `exams.questions[]` (khảo sát thật bằng SQL, không đoán)
Lấy tần suất key trên toàn bộ 7154 câu hỏi hiện có trong `exams`:

| key | số câu có key | Ghi chú |
|---|---:|---|
| `type` | 7154 | `multiple_choice` / đúng-sai / trả lời ngắn |
| `explanation` | 7154 | lời giải |
| `question` | 7154 | đề bài (HTML) |
| `form` | 6935 | `ly_thuyet`\|`bai_tap` — nhãn "Dạng" |
| `topic` | 6935 | tên YCCĐ (text, khớp `question_topics.name`) — nhãn "Chủ đề" |
| `answer` | 6140 | đáp án đúng |
| `options` | 4982 | phương án (trắc nghiệm) |
| **`difficulty`** | **3740** | **ĐÃ TỒN TẠI SẴN** — `de`\|`trung-binh`\|`kho` |
| `statements` | 1014 | câu đúng/sai nhiều ý |

**Phát hiện quan trọng:** field `difficulty` mức từng câu **đã có sẵn trong `exams.questions` jsonb** (52% số câu đã gắn), **KHÔNG phải là field cần tạo mới**. Ví dụ 1 câu thật:
```json
{
  "form": "bai_tap", "type": "multiple_choice",
  "topic": "Mol, số Avogadro và lượng chất khí",
  "difficulty": "de",
  "question": "...", "options": [...], "answer": 2, "explanation": "..."
}
```
Phân bố giá trị `difficulty` trên toàn bộ câu trong `exams.questions` (7154 câu, mọi đề):

| difficulty | số câu |
|---|---:|
| null (key không tồn tại) | 3415 |
| `de` | 1908 |
| `trung-binh` | 1350 |
| `kho` | 414 |
| `""` (rỗng, key có nhưng chưa chọn) | 68 |

### `exam_question_results` / `practice_question_results`
Cả hai đều có: `..., topic_id (bigint), topic_name (text), form (text), qtype (text), earned, max, is_correct, created_at, ...` (riêng `exam_question_results` có thêm `manual_earned/manual_max/graded_by/graded_at` cho chấm tay; `practice_question_results` có `session_id, source_index`). **Không có cột `difficulty`** ở 2 bảng này — đây là dữ liệu làm bài (per-attempt), không phải nhãn câu hỏi.

### `lesson_items`
`id, created_at, lesson_id, kind, title, subtitle, body_html, video_url, pdf_url, sort_order, exam_ids (bigint[]), questions (jsonb), due_at, quiz_min_correct, practice_pass_score, required`

### `lesson_progress`
`user_id, item_id, done_at, course_id` — không có bảng chấm điểm riêng, chỉ đánh dấu hoàn thành mục.

### `tutoring_needs`
`id, student_id, class_id, topic_id, form, wrong, total, pct, source, status, assigned_to, note, first_seen_at, last_seen_at, tutored_at, cleared_at, updated_at` — đã có cấu trúc theo `topic_id`+`form`, dùng để cảnh báo phụ đạo hiện tại.

## 2. Trang Đăng đề, Edge Function `classify-questions`, pipeline nạp bài học

### `app/quan-tri/(thpt)/dang-de/page.tsx`
Chỉ render `<AzotaExamComposer />`. Logic thật nằm ở `components/admin/ExamSection.tsx` (dùng chung cho cả Đăng đề và Sửa đề — `app/quan-tri/(thpt)/sua-de`) và `components/admin/ExamDraftEditor.tsx`.

**Phát hiện quan trọng — hạ tầng mức độ Dễ/TB/Khó theo từng câu ĐÃ ĐƯỢC XÂY GẦN NHƯ ĐẦY ĐỦ, không phải làm từ đầu:**
- `features/exams/types.ts`: đã có `type Difficulty = "" | "de" | "trung-binh" | "kho"`, `DIFFICULTY_LABELS`, field `difficulty?: Difficulty` trong `ExamQuestion`, và hàm audit đề đã có `missingDifficulty: number[]` (số câu chưa gắn mức độ — "không chặn Đăng, chỉ nhắc").
- `components/admin/ExamSection.tsx` (bảng "Phân loại câu"): đã có UI gắn mức độ tay cho từng câu (click chọn Dễ/TB/Khó, dòng ~800-810), nút gắn hàng loạt cho các câu còn thiếu (`untaggedDifficulty`, dòng ~759), và gọi AI gợi ý qua `classifyQuestionTags` rồi tự ghi `difficulty` (dòng ~640-644).
- `services/ai-classify.ts` → gọi Edge Function `classify-questions`.

### `supabase/functions/classify-questions/index.ts`
Input: `{ topics: string[], items: [{index, text}] }` (giới hạn 60 câu/lượt). Dùng Claude Haiku 4.5, prompt yêu cầu AI trả về **cả 3 nhãn cùng lúc**: `topic` (khớp nguyên văn 1 mục trong danh mục YCCĐ gửi kèm), `form` (`ly_thuyet`/`bai_tap`), **và `difficulty`** (`de`/`trung-binh`/`kho`, có tiêu chí rõ: 1 bước tính / 2-3 bước / nhiều bước-đồ thị-dễ nhầm). Kết quả ghi thẳng vào văn bản đề khi thầy bấm, không qua duyệt riêng.

### Đồng bộ 2 chiều đề ↔ ngân hàng câu hỏi (đã deploy)
`docs/supabase-migration-question-bank-difficulty.sql` (đã chạy, theo ghi chú trong chính file: "cột `question_bank.difficulty` đã có sẵn từ bản gốc") vá 2 hàm:
- `sync_exam_to_bank(exam_id)`: khi đăng đề → đọc `q->>'difficulty'` của từng câu, ghi vào `question_bank.difficulty` (on conflict theo `content_hash`, ưu tiên giá trị mới nếu khác rỗng).
- `trg_bank_tags_to_exams()` (trigger `after update of topic_name, form, difficulty`): khi sửa nhãn/mức độ trực tiếp trên dòng `question_bank` (ở trang `/quan-tri/ngan-hang-cau-hoi`) → tự `jsonb_set` ngược lại **mọi đề** đang chứa đúng câu đó (khớp `question_content_hash`).
- `trg_bank_touch` (trigger `before update`): khi sửa `topic_name` trên `question_bank`, tự dò lại `topic_id` theo tên, và ghi `topic/form/difficulty` ngược vào cột `question` (jsonb) của chính dòng đó.

→ Kết luận: **cơ chế lưu + đồng bộ 2 chiều mức độ từng câu đã hoàn thiện và đã deploy**. Phần còn thiếu thực sự chỉ là: (a) cột `difficulty_source` (gv/ai) để phân biệt nguồn — chưa có ở đâu cả 2 nơi; (b) tồn đọng dữ liệu chưa gắn (xem mục 3); (c) chưa thấy nơi nào trong UI học sinh/giáo viên **lọc hoặc hiển thị** theo mức độ (ExamRunner, ExamReviewPager, phân tích lớp) — chỉ mới có ở khâu biên soạn đề.

### `scripts/backfill-question-bank-difficulty.mts`
Script AI backfill hàng loạt cho `question_bank.difficulty = ''`, cùng model Haiku 4.5, cùng tiêu chí 3 mức, ghi trực tiếp `question_bank.difficulty` (trigger tự đồng bộ ngược đề gốc). Chạy lại an toàn (chỉ xử lý câu còn rỗng). Đây là script CÓ SẴN — Agent A cần biết để không viết lại, hoặc dùng nó cho phần backfill còn thiếu (3534 câu `question_bank` còn rỗng — xem mục 3).

### Pipeline `scripts/upload-lesson.mts` / `upload-lessons-batch.mts`
Đăng "gói bài học" JSON (`schema: thachlab.lesson-bundle/v1`) — đường dự phòng khi không dùng trang `/quan-tri/nhap-bai`. Dùng chung `validateBundle`/`bundleToRows` từ `services/lesson-import.ts` (401 dòng) với trang admin, nên sửa logic ở đó thì cả 2 đường tự theo. Bundle JSON có các key chính: `schema, target, theory_title, theory_html, worked_examples, exam, raster_images`. Script tạo 1 `exams` row từ `bundle.exam`, upsert `lesson_items` cho `ly_thuyet`/`bai_tap_mau`/`luyen_tap` hoặc `kiem_tra` (theo `--target`), gán `exam_classes` nếu có `--class`. `upload-lessons-batch.mts` lặp qua một `manifest.json` nhiều bài, hỏi service-role key một lần duy nhất.

## 3. Kết quả đếm SQL

### 3a. `question_bank.topic_id` theo tầng — TOÀN BỘ

| Tầng | Số câu |
|---|---:|
| Tầng YCCĐ/Dạng (`parent_id is not null`) | 6202 |
| Tầng Bài (`parent_id is null`) | 521 |
| `topic_id` null (chưa gắn) | 493 |
| **Tổng** | **7216** |

### 3b. Riêng chương "Động học" lớp 10 (`chapters.id = 11`, "Chương 2: Động học", `subject_code='vat-ly'`)

| Tầng | Số câu |
|---|---:|
| Tầng YCCĐ/Dạng | 242 |
| Tầng Bài | 30 |
| **Tổng có topic_id thuộc chương này** | **272** |

(Không tính được số "chưa gắn thuộc chương Động học" vì câu `topic_id is null` không có cách nào quy về 1 chương cụ thể — 493 câu null ở mục 3a là orphan toàn cục.)

### 3c. `question_bank.difficulty` — TOÀN BỘ

| difficulty | Số câu | % |
|---|---:|---:|
| `''` (chưa gắn) | 3534 | 49% |
| `de` | 1890 | 26% |
| `trung-binh` | 1378 | 19% |
| `kho` | 414 | 6% |
| **Tổng** | **7216** | 100% |

### 3d. `question_bank.difficulty` — riêng chương Động học lớp 10 (272 câu có topic_id thuộc chương)

| difficulty | Số câu |
|---|---:|
| `de` | 145 |
| `trung-binh` | 102 |
| `kho` | 25 |
| **Tổng** | **272** (0 câu rỗng!) |

→ Chương Động học lớp 10 là ví dụ **đã gắn mức độ 100%** — dùng làm chương mẫu để test Agent A thay vì chọn ngẫu nhiên.

## 4. Bundle bài học đang chờ ở gốc repo

Thư mục `output/` (đã có trong `.gitignore`, là scratch của skill LaTeX `dang-bai-hoc-thachlab`) chứa nhiều bài đang xử lý dở — không phải tất cả đều "sẵn sàng đăng":

| Thư mục | Bài/Chương đích (đoán từ tên + `report.json`) | Trạng thái pipeline | Đã có trong DB chưa? |
|---|---|---|---|
| `output/lop10-chuong1-latex/bundles/bai1-lam-quen-voi-vat-li.json`, `bai2-an-toan-phong-thuc-hanh.json`, `bai3-sai-so-phep-do.json` | Lớp 10, Chương 1 "Mở đầu" (Bài 1-3) | **3 bundle JSON hoàn chỉnh** (`schema: thachlab.lesson-bundle/v1`, có `theory_html`, `worked_examples`, `exam`) — có vẻ sẵn sàng chạy `upload-lesson.mts` | **ĐÃ CÓ ĐẦY ĐỦ RỒI** — lesson 46/47/48 (khớp đúng 3 bài) đều đã có `ly_thuyet` (body_html), `bai_tap_mau` (2/2/8 câu), và `luyen_tap` đã gắn đề. → 3 bundle này nhiều khả năng là **bản cũ/trùng lặp đã đăng xong**, KHÔNG phải việc đang chờ. Cần thầy xác nhận trước khi dùng lại (tránh ghi đè nhầm bản mới hơn bằng bản cũ trong bundle). |
| `output/bai10-luc-tu`, `bai12-cam-ung-dien-tu`, `bai12-suat-dien-dong`, `bai12-tu-thong`, `bai13-dien-ap-xoay-chieu`, `bai13-nguyen-tac-dxc`, `bai14-may-bien-ap`, `bai14-may-phat-dien`, `bai14-ung-dung-an-toan`, `bai15-dan-ghi-ta-dien`, `bai15-dong-dien-foucault`, `bai16-dien-tu-truong` | Lớp 12, Chương "Từ trường" (lessons 10-14) + "Điện từ" (lessons 92,93,125-127) — theo "Chủ đề N ... - GV.docx" | `status: "extracted"` — mới trích từ Word, **CHƯA render xong công thức** (`equations_pending` > 0 ở hầu hết), chưa có `bundle.json` cuối, chỉ có `parts/01_ly_thuyet.tex/html` + `README_dang_bai.md` (tự ghi "Chỉ đăng khi `html_report.json` có `ready: true`") | Các lesson đích (11, 13, 14, 125, 126, 127) **đã có `ly_thuyet` (has_body=true) trong DB từ trước**. Vì các thư mục này còn dở dang (mtime 23/9/2026, mới nhất trong repo), có khả năng đây là phiên xử lý **thay lý thuyết bằng file GV mới** (giống việc đã làm với "Chương 4 hạt nhân") nhưng bị dừng giữa chừng — KHÔNG được tự ý tiếp tục/ghi đè, phải hỏi thầy trước. |
| `output/12-tu-thong-latex` | Lớp 12 "Từ thông. Hiện tượng cảm ứng điện từ" | `status: "extracted"`, 612 công thức **chưa hoàn thành** (`equations_pending: 612`) | Dở dang nhất — không nên đụng. |
| `output/11-mo-ta-song-latex`, `output/tu-truong-latex` | Bài 8 Mô tả sóng, Bài 9 Khái niệm từ trường | Có `bundle.json`/`published.json` đầy đủ | Theo memory đã đăng xong (19/9, 21/9/2026) — coi như đã xử lý, chỉ còn ở đây làm cache. |

Không tìm thấy bundle JSON "chờ đăng" nào khác ở gốc repo (`ls` gốc chỉ có `package-lock.json/package.json/tsconfig.json`, không có `.tex/.json/.docx` rời). `scripts/data/` chỉ có file phục vụ script khác (không phải bundle bài học). `content/blog/` là bài viết blog, không liên quan.

## 5. Ghi chú cho 3 agent

**Agent A (mức độ Dễ/Trung bình/Khó):**
- **KHÔNG bắt đầu từ đầu** — field `difficulty` mức từng câu đã tồn tại đầy đủ trong `exams.questions[]` (jsonb), trong `question_bank`, có type `Difficulty` trong `features/exams/types.ts`, có UI gắn tay + AI gợi ý ở `/quan-tri/dang-de` (`ExamSection.tsx`), có 2 trigger đồng bộ 2 chiều đề ↔ ngân hàng (`docs/supabase-migration-question-bank-difficulty.sql`, đã deploy), và có script backfill AI hàng loạt (`scripts/backfill-question-bank-difficulty.mts`).
- Việc thật sự còn thiếu, theo thứ tự khả năng cần làm:
  1. Cột `difficulty_source` ('gv'|'ai') — chưa có ở `question_bank` lẫn trong jsonb câu hỏi — nếu cần phân biệt "AI gợi ý chưa duyệt" vs "GV xác nhận tay" thì phải thêm cột + sửa 3 hàm trigger ở migration trên + UI ExamSection để set nguồn khi bấm tay vs khi nhận gợi ý AI.
  2. Backfill nốt dữ liệu cũ: `question_bank` còn 3534/7216 câu (49%) rỗng difficulty — chạy `scripts/backfill-question-bank-difficulty.mts` có sẵn, không cần viết mới.
  3. Chưa thấy nơi nào ở phía học sinh (ExamRunner, ExamReviewPager) hay phân tích lớp (TeacherThptAnalysis) **đọc/lọc/hiển thị** theo `difficulty` — nếu tính năng của Agent A là "cho học sinh luyện theo mức độ" hoặc "thống kê theo mức độ" thì đây mới là phần thật sự cần code mới, không phải phần lưu trữ.
  4. `exams.questions` vẫn còn 3415/7154 câu (48%) chưa có key `difficulty` — vì đây là đề *gốc* (không phải ngân hàng), sync một chiều "ngân hàng → đề" chỉ chạy khi trigger `trg_bank_tags_to_exams` bắn (tức là khi sửa ở trang ngân hàng) — cần Agent A làm rõ: các câu cũ trong đề nhưng CHƯA từng vào ngân hàng (hoặc vào ngân hàng nhưng ngân hàng cũng rỗng) sẽ không tự có difficulty trừ khi chạy lại `sync_exam_to_bank` hoặc backfill ngân hàng trước rồi đợi trigger lan ngược.

**Agent B (nghi vấn: nạp bundle bài học còn lại):**
- Xem mục 4 — chỉ có 12 bài Lớp 12 (Từ trường + Điện từ) đang dở pipeline LaTeX, KHÔNG có bundle JSON hoàn chỉnh nào thật sự "sẵn sàng đăng mà chưa đăng" (3 bundle Chương 1 lớp 10 tưởng chờ nhưng thực ra bài đích đã có nội dung rồi). Việc đầu tiên trước khi code là **hỏi thầy** các thư mục `output/bai10-luc-tu` … `bai16-dien-tu-truong` có phải đang làm dở để thay lý thuyết mới không, tránh Agent B tự "hoàn thiện nốt" rồi ghi đè nhầm nội dung đã ổn định.

**Agent C (nghi vấn: mastery theo topic/YCCĐ):**
- `exam_question_results` và `practice_question_results` đã có sẵn `topic_id, topic_name, form` (không có `difficulty`) — đúng như bối cảnh đã biết, hạ tầng ghi nhận kết quả theo YCCĐ đã có, chỉ chưa có lớp tính "mức độ thành thạo" (mastery) tổng hợp. `tutoring_needs` đã có cấu trúc theo `topic_id + form + wrong/total/pct` — có thể là điểm khởi đầu tốt hơn là tạo bảng mastery mới từ đầu.

**Quy ước bắt buộc tuân theo (từ `perf/RESULT.md`, đợt tối ưu 25/9/2026):**
- Không thêm `select('*')`; luôn liệt kê cột cần dùng (client hiện đã tuân thủ nghiêm, đừng phá quy ước khi thêm code mới).
- Không thêm truy vấn Supabase nối tiếp mới ở các trang đã tối ưu (`/lop-hoc`, `/lop-hoc/bai`, `ThptStudentHome`) — nếu Agent A/B/C cần thêm dữ liệu ở các trang này, cân nhắc gộp vào RPC hiện có (`get_class_exam_best`, `get_class_exam_question_stats`, `get_class_topic_matrix`, `get_student_learning_history`, `ta_monthly_scores` — file `supabase/migrations/20260925130000_perf_rpc_gv.sql`) thay vì query rời.
- Lớp tĩnh `services/static-content.ts` (`/data/lessons/*.json`, `/data/catalog.json`) chỉ dùng cho 4 nơi hiển thị công khai (`app/lop-hoc/page.tsx`, `app/lop-hoc/bai/page.tsx`, `ThptStudentHome.tsx`, `InlineLessonAccordion.tsx`) và **không chứa đáp án/lời giải** — sửa lý thuyết/bài học không tự lên web, phải chạy `scripts/deploy.sh` (rebuild) mới thấy; nhớ điều này nếu Agent B đổi nội dung bài học.
- RLS: có 2 policy tautology đã biết ở `attendance_sessions`/`equipment_breakdown_reports` (lỗ hổng đọc chéo, chưa vá) — không liên quan trực tiếp 3 agent này nhưng nếu đụng tới các bảng đó thì cẩn trọng.
- Working tree hiện có rất nhiều WIP dở dang không liên quan (question-bank-figure-ai, tutoring-exit-quiz, bulk đề thi thử, backfill lessons description...) — 3 agent tuyệt đối không `git add -A`, chỉ commit đúng file của tính năng mình làm.
