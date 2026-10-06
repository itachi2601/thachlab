# Bàn giao: "Ôn tổng hợp" nhiều bài đã học — giai đoạn 1 (không migration)

Ngày 3/10/2026. Soạn bởi phiên Fable để phiên khác (Sonnet) code tiếp. Đọc file này là đủ ngữ cảnh;
không cần đọc lại hội thoại. Trước khi code: đọc `AGENTS.md`, `docs/QUY-TAC-THIET-KE.md` (mục 8 checklist),
và chỉ các file liệt kê ở mục 3.

## 1. Mục tiêu giai đoạn 1

Học sinh vào `/luyen-tap`, chọn **nhiều bài đã học** (không chỉ 1 bài như hiện nay), bấm một nút,
hệ thống bốc N câu trộn đều từ các bài đó, làm ngay trong modal luyện tập sẵn có, kết quả lưu như
phiên luyện tập bình thường và hiện **bảng kết quả theo từng bài**.

Không làm ở giai đoạn này: RPC đọc `question_bank`, chế độ "ôn chỗ yếu" theo mastery, "ôn lại câu
sai", "thi thử chương" có đồng hồ. Không thêm migration.

## 2. Hiện trạng đã khảo sát (tin được, đã đọc code)

- `app/luyen-tap/page.tsx` (304 dòng, client component): chọn Lớp → Chương → Bài → YCCĐ → Mức.
  Pool câu lấy bằng `fetchExamsFull(examIds)` với `examIds` = gộp `itemRefs[].exam_ids` của **một**
  bài. Mở `TopicPracticeModal` để luyện.
- `components/mastery/TopicPracticeModal.tsx` (232 dòng): props
  `{ lessonId: number; examIds: number[]; topicName: string; difficulty?: Difficulty; onClose; onFinished? }`.
  Tải câu bằng `fetchExamsFull`, lọc `topicName`/`difficulty`, bỏ `type === "essay"`, bốc
  `pickRandom(pool, COUNT)` (COUNT = 10), chấm bằng `gradeExam`, lưu bằng `savePracticeSession`.
- `services/lessons.ts`: `fetchExamsFull(examIds: number[]): Promise<Map<number, Exam>>` (dòng ~244);
  `PracticePick { question, examId, sourceIndex }`; `PracticeSessionInput.lessonId: number | null`
  (đã cho phép null → phiên tổng hợp ghi `lessonId: null`, không cần đổi schema).
- `features/exams/types.ts`: `pickRandom<T>(items, n)`, `gradeExam`, `DIFFICULTY_LABELS`,
  kiểu `Difficulty = "" | "de" | "trung-binh" | "kho"`.
- Mastery theo YCCĐ (`docs/mastery-rules.md`) tính từ `practice_question_results.topic_id` → phiên
  tổng hợp **tự nuôi mastery, danh hiệu, cảnh báo phụ đạo** mà không sửa gì thêm.
- "Bài đã học" suy từ `lesson_progress` (user_id, item_id, done_at); xem cách query ở
  `services/progress.ts` dòng ~133 và ~428. Chưa có hàm "danh sách lesson_id em đã học" — cần viết
  một hàm nhỏ trong `services/progress.ts` (1 query `lesson_progress` của chính em, map item_id →
  lesson_id qua `lessons`/`itemRefs` đã có sẵn trên client).
- RLS: học sinh **không** select được `question_bank` trực tiếp. Giai đoạn 1 chỉ dùng `exams` qua
  `fetchExamsFull` như hiện nay.

## 3. Việc cần làm (theo thứ tự)

1. **`services/progress.ts`**: thêm `fetchLearnedLessonIds(studentId): Promise<Set<number>>` —
   lesson nào có ≥1 item trong `lesson_progress` của em. Không thêm round-trip cho trang khác.
2. **`components/mastery/TopicPracticeModal.tsx`**: mở rộng để dùng cho nhiều bài, giữ tương thích
   với 2 chỗ đang gọi (trang bài học và `/luyen-tap`):
   - thêm prop tuỳ chọn `count?: number` (mặc định 10) và `lessonIds?: number[]` (khi có → bốc đều:
     chia `count` cho số bài, mỗi bài ≥1 câu nếu còn, phần dư dồn sang bài còn câu; cần biết câu
     thuộc bài nào → truyền `examIdsByLesson: Record<number, number[]>` thay cho `examIds` phẳng,
     hoặc thêm prop mới và giữ `examIds` cũ);
   - khử trùng câu giữa các đề (chuẩn hoá chuỗi đề bài: bỏ HTML, khoảng trắng, lowercase);
   - khi `lessonIds` có → gọi `savePracticeSession({ lessonId: null, ... })`;
   - màn kết quả: nếu nhiều bài → bảng mỗi bài một dòng (đúng/tổng, nhãn theo ngưỡng mastery
     ≥80 % xanh, 50–80 % vàng, <50 % đỏ — dùng `components/ui/Badge.tsx` tone success/warning/error)
     và nút "Luyện riêng bài này" (gọi `onPickLesson?.(lessonId)` để trang cha mở lại modal 1 bài).
3. **`app/luyen-tap/page.tsx`**: thêm tab/khối "Ôn tổng hợp" bên cạnh luồng 1 bài hiện có:
   - chip theo chương, các bài **đã học tick sẵn** (từ bước 1), bài chưa có `exam_ids` làm mờ + chữ
     "chưa có câu"; lối tắt "Cả chương" / "3 bài gần nhất" / "Bỏ chọn hết";
   - chọn số câu 10 / 20 / 30; nút chính một dòng dạng "Làm 20 câu từ 5 bài";
   - mở modal với `lessonIds` + `examIdsByLesson`. Modal vẫn lazy qua `next/dynamic` +
     `LazyErrorBoundary` như hiện tại (không thêm chunk mới).
4. **Kiểm**: `npm run lint`, `npx tsc --noEmit`, `npm run check:a11y` nếu có; chạy dev, chụp 375px
   trang `/luyen-tap` tab mới và màn kết quả nhiều bài; thử 1 bài có 0 câu, 1 bài có 2 câu + 1 bài
   30 câu (phải dồn câu), bấm nộp 2 lần nhanh (không lưu trùng — `clientToken` lo).

## 4. Ràng buộc bắt buộc

- UI học sinh theo `docs/QUY-TAC-THIET-KE.md`: nêu mã quy tắc trong commit; đích chạm ≥44px, chữ
  phụ ≥13px, chụp 375px trước khi báo xong.
- Tốc độ: không thêm round-trip Supabase cho `/`, `/lop-hoc/bai`, `/kiem-tra/lam`; không tách chunk
  mới thiếu `LazyErrorBoundary`; không lazy KaTeX ở trang học sinh.
- Chỉ sửa đúng 3 file ở mục 3 (+ file test nếu có). Working tree đang nhiều WIP của việc khác:
  commit bằng `git commit -- <path>` từng file của mình, không `git add -A`.
- Không migration, không gọi `supabase db query` ghi, không deploy nếu Thạch chưa bảo.
- Không cộng RP cho phiên ôn tổng hợp (giữ nguyên hành vi `savePracticeSession`, không chạm bảng rank).

## 5. Tiêu chí xong

- Em chọn 3 bài, bấm làm 20 câu → đúng 20 câu (hoặc ít hơn kèm thông báo "chỉ có X câu"), không câu trùng.
- Sau nộp: `practice_sessions` có dòng `lesson_id null`, `practice_question_results` đủ 20 dòng có `topic_id`.
- Màn kết quả theo bài hiện đúng số đúng/tổng mỗi bài; "Luyện riêng bài này" mở modal 1 bài.
- Luồng cũ (luyện 1 bài từ trang bài học và từ `/luyen-tap`) không đổi hành vi.
- Lint/type sạch; có ảnh 375px đính kèm báo cáo.

## 6. Giai đoạn 2 (ghi để biết, KHÔNG làm bây giờ)

RPC `build_review_quiz(p_lesson_ids, p_count, p_mode)` SECURITY DEFINER đọc `question_bank` + kết
quả cũ của em (mẫu: `rank_fix_quiz_start`); chế độ "ôn chỗ yếu" trọng số theo nhãn mastery
(Chưa đạt ×3, Cần luyện ×2, Chưa đủ dữ liệu ×2, Nắm vững ×1); "ôn lại câu sai" 7–21 ngày;
"thi thử chương" bằng `ExamRunner`; cột `practice_sessions.lesson_ids bigint[]`; gợi ý ở
"Việc cần làm" trang chủ HS khi ≥3 bài đã học và 7 ngày chưa ôn.
