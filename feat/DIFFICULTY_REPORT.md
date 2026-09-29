# Báo cáo — Agent A: mức độ Dễ/Trung bình/Khó, cột `difficulty_source`

Nhánh: `feat/difficulty` (tạo từ `main`, tại commit `3ced896e`).

## Commit

1. `76b3b9ed` — `feat(ngân hàng): migration difficulty_source ('gv'|'ai')`
   — chỉ thêm file `supabase/migrations/20260925150000_difficulty_source.sql`.
2. `9b5a8916` — `feat(đăng đề): phân biệt mức độ do GV gắn tay hay AI gợi ý`
   — `features/exams/types.ts`, `services/exam-latex-parser.ts`,
   `components/admin/ExamSection.tsx`, `scripts/backfill-question-bank-difficulty.mts`.

Không đụng file nào khác — working tree sạch sau 2 commit này (`git status --short` rỗng).

## Việc 1 — cột `difficulty_source` (bắt buộc) — ĐÃ LÀM XONG (code), CHỜ CHẠY MIGRATION

### File migration mới (chưa chạy lên production)
`supabase/migrations/20260925150000_difficulty_source.sql` — idempotent, bọc trong
`begin;/commit;`. Nội dung:
- `alter table question_bank add column if not exists difficulty_source text check (difficulty_source is null or difficulty_source in ('gv','ai'))`.
- `create or replace function sync_exam_to_bank(...)` — vá y nguyên bản trong
  `docs/supabase-migration-question-bank-difficulty.sql` (KHÔNG sửa file đó), thêm đọc
  `r.q->>'difficultySource'`, ghi cột `difficulty_source` lúc insert, và rule
  on-conflict: chỉ ghi đè nguồn khi đề mới có cả `difficulty` khác rỗng lẫn
  `difficultySource` hợp lệ — đăng lại đề không đổi mức độ thì giữ nguyên nguồn cũ trong
  ngân hàng.
- `create or replace function trg_bank_tags_to_exams()` — trigger đổi từ
  `after update of topic_name, form, difficulty` thành thêm `difficulty_source`; patch
  jsonb ghi thêm key `difficultySource` (bao gồm cả khi null) vào mọi câu trùng
  `content_hash` trong `exams.questions`.
- `create or replace function trg_bank_touch()` — vá để `jsonb_build_object` ghi thêm
  `difficultySource` vào chính `question` jsonb của dòng ngân hàng khi sửa trực tiếp.
- **Giữ nguyên chế độ bảo mật từng hàm y như bản gốc**: `sync_exam_to_bank` và
  `trg_bank_tags_to_exams` vẫn `security definer` (đã vậy từ trước, không phải tôi thêm);
  `trg_bank_touch` vẫn KHÔNG có `security definer` (chạy quyền người gọi). Không nới RLS,
  không đổi quyền `execute` nào ngoài revoke đã có sẵn.

### Lệnh orchestrator/thầy cần tự chạy
```
supabase db query --linked -f supabase/migrations/20260925150000_difficulty_source.sql
```
(hoặc dán nội dung file vào Dashboard → SQL Editor → Run). Tôi KHÔNG tự chạy vì không có
service-role key / kết nối DB thật trong phiên này, và vì đây là thay đổi schema production
theo đúng luật "Migration KHÔNG chạy lên production".

### Field `difficultySource` trong jsonb `exams.questions[]`
Không phải cột DB — chỉ là 1 key jsonb, đã cho parser/trigger đọc-ghi (xem Việc 1 code bên
dưới). Câu chưa từng qua UI mới (đề cũ) sẽ không có key này — coi là "không rõ nguồn", không
suy diễn thành `gv` hay `ai`.

### Code (đã build + tsc sạch)
- `features/exams/types.ts`: thêm `export type DifficultySource = "gv" | "ai"` và field
  `difficultySource?: DifficultySource` trong `QuestionTags` (interface nội bộ, áp dụng cho
  cả 4 loại câu hỏi qua `ExamQuestion`).
- `services/exam-latex-parser.ts`: đọc/ghi hậu tố `(AI)`/`(GV)` gắn ngay sau giá trị dòng
  "Mức độ: …" trong văn bản đề (vd `Mức độ: dễ (AI)`) — vì trang Đăng đề dùng **văn bản làm
  nguồn sự thật** (state `text`, re-parse mỗi lần debounce qua `docxTextToBundle` →
  `parseExamLatex`), không phải object rời, nên không thể thêm 1 dòng nhãn "Nguồn:" riêng mà
  không phá cấu trúc `TagField` hiện có (`topic`/`form`/`difficulty`) — chọn cách nhúng hậu tố
  vào cùng dòng "Mức độ:" là ít xâm lấn nhất, tương thích ngược 100% với đề cũ (dòng "Mức độ:
  dễ" không có hậu tố vẫn parse ra `difficulty="de"`, `difficultySource=undefined`).
- `components/admin/ExamSection.tsx`:
  - `runAutoTag` (nút "AI gắn nhãn") ghi `difficulty` kèm hậu tố `(AI)`.
  - Bấm tay từng câu (nút Dễ/TB/Khó trong bảng "Phân loại câu") và nút gắn hàng loạt cho câu
    còn thiếu đều ghi kèm hậu tố `(GV)` — kể cả khi giáo viên bấm lại đúng mức AI đã gợi ý,
    hành động bấm tay luôn được coi là xác nhận, chuyển ngay `difficultySource` thành `gv`.
  - Huy hiệu nhỏ "AI" (class `admin-badge admin-badge--accent` — tái dùng token màu accent có
    sẵn của hệ thống `admin-*`, không tự bịa mã màu `#0B3D91`/`#F4B400` vì 2 mã đó không tồn
    tại ở đâu trong codebase hiện tại) hiện cạnh 3 nút mức độ khi
    `q.difficulty && q.difficultySource === "ai"`, biến mất ngay khi giáo viên bấm tay.

## Việc 2 — Backfill dữ liệu cũ (bắt buộc) — CODE XONG, **CHƯA CHẠY** (an toàn trước)

### Phát hiện quan trọng lệch với mô tả trong đề bài
`scripts/backfill-question-bank-difficulty.mts` **KHÔNG có chế độ dry-run / cờ `--apply`**
như mô tả trong bối cảnh giao việc — đọc kỹ code xác nhận: mỗi lần chạy, script gọi thẳng
Anthropic API rồi `update()` ngay vào `question_bank` cho từng câu, không có bước xem trước.
Tham số duy nhất là `[số câu tối đa]` (giới hạn số dòng xử lý trong 1 lần chạy, không phải
dry-run — vẫn ghi thật). Tôi **không viết lại** script (đúng yêu cầu), chỉ sửa dòng ghi
`update()` để thêm `difficulty_source: "ai"`, và ghi rõ ghi chú "không có dry-run" ngay đầu
file để orchestrator/thầy biết trước khi chạy.

### Đã KHÔNG tự chạy script
Lý do: (1) cần `SUPABASE_SERVICE_ROLE_KEY` + `ANTHROPIC_API_KEY` — không có sẵn trong phiên
này và không nên tự hỏi/nhập theo luật an toàn; (2) script ghi thẳng vào DB thật ngay lần
chạy đầu, không có cách nào "xem trước rồi mới apply" như mô tả — chạy thử dù chỉ vài câu vẫn
là ghi thật lên production. Ưu tiên AN TOÀN theo đúng chỉ dẫn.

### Lệnh orchestrator/thầy cần tự chạy (sau khi đã chạy migration ở Việc 1)
```
# Khuyến nghị: thử trước với số nhỏ, tự xem lại vài dòng trong
# /quan-tri/ngan-hang-cau-hoi trước khi chạy hết
npx tsx scripts/backfill-question-bank-difficulty.mts 20

# Chạy hết phần còn thiếu (không giới hạn) — xử lý dần 3534 câu difficulty=''
npx tsx scripts/backfill-question-bank-difficulty.mts
```
Script tự chạy lại an toàn (chỉ xử lý câu còn `difficulty=''`), có thể dừng giữa chừng
(Ctrl+C) và chạy tiếp sau.

### Xác nhận cơ chế lan ngược đề ↔ ngân hàng
Đã đọc kỹ `trg_bank_tags_to_exams` (trigger `after update of ... difficulty, difficulty_source`)
trong migration mới — khi script `update` cột `difficulty`/`difficulty_source` trên
`question_bank`, trigger tự bắn và `jsonb_set` ngược vào MỌI câu trong `exams.questions`
khớp đúng `content_hash`. Đây là đọc code + suy luận logic SQL, **chưa test thật trên DB**
(không có quyền chạy) — orchestrator/thầy nên kiểm 1-2 câu cụ thể trước/sau khi chạy backfill
thật (query `question_bank` theo id + `exams` chứa câu đó qua `content_hash`) để xác nhận
đúng như thiết kế.

### 3415 câu "mồ côi" trong `exams.questions` (chưa có key `difficulty`, không khớp
`content_hash` nào trong `question_bank`)
Không xử lý (đúng phạm vi "không bắt buộc"). Số liệu lấy nguyên từ `feat/SURVEY.md` (khảo sát
25/9/2026, không tự đếm lại). Đề xuất cách xử lý nếu thầy muốn làm tiếp:
1. Chạy `sync_exam_to_bank(exam_id)` cho từng đề cũ (RPC có sẵn, `security definer`,
   `revoke execute from public/anon/authenticated` — cần chạy qua service-role hoặc thêm 1
   lượt gọi từ trang admin có quyền) để nạp các câu này vào `question_bank` trước (nếu
   `content_hash` chưa tồn tại thì sẽ tạo dòng mới, không phải update).
2. Sau đó chạy lại `scripts/backfill-question-bank-difficulty.mts` — các câu mới nạp có
   `difficulty=''` sẽ được AI gắn mức độ, rồi tự lan ngược lại đúng đề gốc nhờ trigger.
3. Rủi ro cần lưu ý: một số đề cũ có thể đã bị xoá/ẩn (`published=false`) hoặc không còn gán
   lớp (`exam_classes` rỗng) — `sync_exam_to_bank` vẫn chạy được (grade để rỗng) nhưng nên
   lọc trước danh sách `exam_id` cần chạy thay vì lặp toàn bộ `exams` để tránh tốn thời gian.

## Việc 3 (tuỳ chọn) — hiển thị/lọc difficulty phía học sinh/GV
**Bỏ qua** — đúng như đề bài cho phép ("không bắt buộc"). Lý do ưu tiên thời gian cho 2 việc
bắt buộc + kiểm tra kỹ an toàn dữ liệu (migration + backfill). Ghi chú cho phiên sau nếu làm
tiếp:
- `components/exams/ExamReviewPager.tsx` và `components/dashboard/TeacherThptAnalysis.tsx` đã
  có sẵn trong working tree ở trạng thái "modified" (WIP của phiên khác — feature AI vẽ hình
  câu thiếu hình / phân tích lớp) khi tôi bắt đầu; nhánh `feat/difficulty` được tạo sạch từ
  `main` nên KHÔNG kế thừa các thay đổi đó — nếu làm việc 3, cần merge/rebase cẩn thận để
  không đụng WIP song song (xem `feat/SURVEY.md` mục "Phiên chạy song song").
- Nên đọc `perf/RESULT.md` trước — 2 trang trên có thể đã được tối ưu để không thêm query
  Supabase rời; nếu cần thêm dữ liệu `difficulty`, ưu tiên gộp vào các RPC có sẵn
  (`get_class_exam_question_stats`, `get_class_topic_matrix`...) thay vì query mới.

## Kết quả kiểm tra
```
npx tsc --noEmit     → sạch, không lỗi
npm run build        → "Compiled successfully", TypeScript pass, 68 trang static generate OK
```

## Rủi ro / lưu ý cho orchestrator
1. Migration + backfill đều CHƯA chạy trên DB thật — cần thầy tự chạy theo đúng thứ tự
   (migration trước, backfill sau) bằng lệnh ở Việc 1/2.
2. Backfill không có dry-run thật sự — mỗi lần chạy là ghi thật + tốn phí Anthropic API.
3. Cách nhúng hậu tố `(AI)`/`(GV)` vào dòng "Mức độ: …" trong văn bản đề là quyết định thiết
   kế của tôi (không có trong đặc tả gốc) — nếu sau này có skill/script ngoài UI
   (`up-de-kiem-tra`, `ngan-hang-cau-hoi`, `azota`...) tự sinh dòng "Mức độ: …" trong file Word
   xuất ra mà không theo đúng hậu tố này thì `difficultySource` sẽ là `undefined` (không rõ
   nguồn) — không lỗi, chỉ đơn giản là không hiện huy hiệu "AI", hành vi an toàn.
4. Không đụng `components/admin/QuestionBankAdmin.tsx` (trang `/quan-tri/ngan-hang-cau-hoi`)
   dù cột `difficulty_source` cũng có ý nghĩa ở đó — nằm ngoài danh sách file được giao, và
   file này đang có WIP song song (feature AI vẽ hình) nên không tự sửa. Nếu muốn hiển thị/sửa
   tay `difficulty_source` ở trang ngân hàng, cần một phiên riêng.
