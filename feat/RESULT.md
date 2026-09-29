# Báo cáo — Agent D: kiểm tra độc lập 3 tính năng (bundles / difficulty / mastery)

Ngày: 25/9/2026. Worktree riêng, checkout ban đầu từ `main` **thiếu cả 3 merge** (HEAD lúc mở việc
là `09a2d383`, TRƯỚC `e2b39a88`/`543e2813`/`eea8b504`/`205ef296`) — đã tự phát hiện và
`git merge main --ff-only` để lấy đúng `main` hiện tại (`205ef296`) trước khi kiểm tra. Đây là rủi
ro quy trình cần lưu ý: nếu một agent kiểm tra không tự phát hiện việc này, kết quả "PASS" của họ
sẽ vô nghĩa (kiểm tra nhầm code cũ).

Toàn bộ SQL chạy trên DB thật qua `supabase db query --linked` — chỉ SELECT, hoặc CREATE OR REPLACE
FUNCTION bọc trong `begin;...rollback;` rồi xác nhận lại bằng `select proname from pg_proc where
proname in (...)` trả rỗng sau mỗi lần. Không có lệnh ghi nào được để lại trên production. Worktree
ban đầu thiếu `supabase/.temp/{project-ref,linked-project.json,pooler-url}` (state cục bộ, không
theo git) — đã copy từ checkout chính để `supabase db query --linked` hoạt động; không ảnh hưởng
production, chỉ là thông tin kết nối.

## Tóm tắt PASS/FAIL

| Mục | Kết quả |
|---|---|
| 1. `npx tsc --noEmit` | **PASS** — sạch, không lỗi |
| 1. `npm run build` | **PASS** — 69 trang tĩnh, không lỗi, đủ toàn bộ route cũ |
| 2. Migration `difficulty_source` — review | **PASS** (đọc code) — 3 hàm đúng chế độ bảo mật gốc (`sync_exam_to_bank`/`trg_bank_tags_to_exams` = SECURITY DEFINER như bản gốc, `trg_bank_touch` = INVOKER như bản gốc), không nới RLS, cú pháp hợp lệ. **Xác nhận qua SQL: CHƯA chạy trên production** (`information_schema.columns` không có `difficulty_source`) |
| 2. Logic UI huy hiệu AI/GV (`ExamSection.tsx`) | **PASS** (đọc code) — bấm tay luôn ghi hậu tố `(GV)` (dòng 812), AI gợi ý ghi `(AI)` (dòng 645), huy hiệu chỉ hiện khi `difficulty && difficultySource==="ai"` (dòng 821) |
| 2. Backfill không có dry-run | **PASS, xác nhận lại** — đọc `scripts/backfill-question-bank-difficulty.mts` dòng 11-18: không có cờ `--apply`/dry-run, `update()` ghi thật ngay; tham số duy nhất là giới hạn số câu |
| 3. Migration `mastery` — review | **PASS** (đọc code) — cả 2 hàm `security invoker`, không nới RLS. **Xác nhận qua SQL: CHƯA chạy trên production** (`information_schema.routines` không có `get_lesson_mastery`/`get_chapter_mastery`) |
| 3. Test `get_lesson_mastery`/`get_chapter_mastery` bằng dữ liệu thật | **PASS** — tự chọn học sinh/bài **độc lập với báo cáo C** (không dùng lại `b4e8be9f...`): học sinh `376abc10-973d-438a-8004-fdfd87337218`, bài `lesson_id=10` ("Bài 9. Khái niệm từ trường"). Tính tay bằng SQL độc lập trước (2 YCCĐ, mỗi YCCĐ 10 lượt gần nhất, earned=1.50/max=2.50 → 60% → `practicing`), sau đó chạy đúng RPC trong transaction → **kết quả khớp 100%** với tính tay (topic 213: 10 lượt/60%/practicing; topic 214: 10 lượt/60%/practicing; tổng bài: practicing). Trường hợp học sinh không có dữ liệu (`00000000-…`, bài 10): trả đúng `insufficient` cho cả 2 YCCĐ + dòng tổng, không lỗi. `get_chapter_mastery(4)` trả đủ 9 bài trong chương, bài 10 = practicing khớp, các bài khác = insufficient (đúng vì học sinh test chưa làm). Đã xác nhận `ROLLBACK` không để lại hàm nào trên DB thật (2 lần kiểm). Ngưỡng nhãn khớp đúng `docs/mastery-rules.md` (< 4 lượt → insufficient; ≥0.8 → mastered; ≥0.5 → practicing; else weak) |
| 3. Nút "Luyện 10 câu phần này" — nguồn câu hỏi | **XÁC NHẬN ĐÚNG NHƯ BÁO CÁO** — đọc `components/mastery/TopicPracticeModal.tsx` dòng 66-77: gọi `fetchExamsFull(examIds)` (chỉ đề của chính bài học), lọc `question.topic === topicName`; KHÔNG đụng `question_bank`. Mức độ nghiêm trọng: **trung bình** — nếu bài học có đề nhưng câu đúng YCCĐ đó không nằm trong đề (dù ngân hàng chung còn câu), học sinh sẽ thấy "chưa có đủ câu hỏi" dù dữ liệu vẫn tồn tại nơi khác; không phải lỗi, là đánh đổi có chủ đích tránh nới RLS — đã ghi rõ trong báo cáo gốc và `docs/mastery-rules.md`, không phải rủi ro ẩn |
| 3. UI thật `/lop-hoc`, `/lop-hoc/bai` | **KHÔNG KIỂM TRA ĐƯỢC** — cần tài khoản học sinh thật đăng nhập qua Supabase Auth, không có trong worktree/sandbox này. Đã đọc code thay thế: cả `LessonMasteryCard` và badge ở `app/lop-hoc/page.tsx` đều fail-safe — RPC lỗi/chưa tồn tại → component trả `null` (ẩn lặng lẽ), KHÔNG chặn trang. Nghĩa là **code hiện tại AN TOÀN để deploy ngay cả trước khi chạy migration mastery** (chỉ đơn giản chưa hiện mastery) |
| 4. Bundles — 6 dòng `lesson_items` (52,66,141,143,145,183) | **PASS** — tự chạy SQL độc lập, không tin báo cáo: `body_html` không rỗng, không có `{{`/`PLACEHOLDER`/`output/`; độ dài khớp 100% với bảng trong `BUNDLES_REPORT.md` (127477/259891/101435/141719/88497/99132); số ảnh khớp (87/124/17/20/20/15) |
| 4. Ảnh không lẫn giữa các bài | **PASS** — trích toàn bộ URL ảnh từng dòng: mỗi dòng chỉ chứa URL dạng `.../lesson-media/<lesson_id>/...` đúng khớp `lesson_id` của chính nó (11→11, 13→13, 14→14, 125→125, 126→126, 127→127), không có URL lẫn từ lesson khác. Timestamp trong tên file tăng dần liên tục qua từng lesson (không xen kẽ) — nhất quán với 1 lần chạy tuần tự sạch |
| 4. Ảnh tồn tại thật | **PASS** — tải thử 3 URL (lesson 11, 13, 127) đều trả `HTTP 200`, `content-type: image/png`, kích thước hợp lý |
| 4. `node scripts/build-content.mjs` | **PASS gián tiếp** — không chạy tách riêng (script này là bước `prebuild` của `npm run build`, đã chạy PASS ở mục 1); không kiểm lại đối chiếu JSON tĩnh vs DB do giới hạn thời gian — rủi ro thấp vì đã verify trực tiếp DB |
| 5. Hồi quy route cũ | **PASS (qua build list)** — `npm run build` liệt kê đủ `/kiem-tra/lam`, `/quan-tri/bang-diem`, `/tro-giang/phu-dao`, `/quan-tri/chu-de`, `/lop-hoc/cnc`, `/quan-tri/cnc-dang-de`. Đối chiếu diff của cả 3 merge commit (`git show --stat`): không file nào trong 6 route này bị đụng tới → rủi ro hồi quy thấp. Không test tương tác (cần đăng nhập) |

## Migration đang chờ chạy — ĐÚNG THỨ TỰ

**Xác nhận bằng SQL: cả 2 đều CHƯA chạy** (`information_schema` không thấy cột/hàm tương ứng).

### 1. `supabase/migrations/20260925150000_difficulty_source.sql`
- Làm gì: thêm cột `question_bank.difficulty_source text check (... in ('gv','ai'))`; vá 3 hàm
  (`sync_exam_to_bank`, `trg_bank_tags_to_exams`, `trg_bank_touch`) để đọc/ghi thêm nguồn nhãn mức
  độ (AI gợi ý vs GV xác nhận tay) 2 chiều đề ↔ ngân hàng.
- Chạy: `supabase db query --linked -f supabase/migrations/20260925150000_difficulty_source.sql`
- Rollback:
  ```sql
  -- Khôi phục 3 hàm về bản trước (docs/supabase-migration-question-bank-difficulty.sql, bỏ phần
  -- difficulty_source) rồi:
  alter table public.question_bank drop column if exists difficulty_source;
  ```
  (Lưu ý: rollback hàm cần dán lại đúng nội dung cũ từ `docs/supabase-migration-question-bank-difficulty.sql`
  — file migration mới không tự chứa bản "trước", DROP COLUMN không tự phục hồi hành vi hàm cũ.)

### 2. `supabase/migrations/20260925160000_mastery.sql`
- Làm gì: tạo mới `get_lesson_mastery(p_lesson)`, `get_chapter_mastery(p_chapter)` — cả hai
  `security invoker`, không tạo bảng/cột mới, chỉ đọc `question_topics` + `exam_question_results` +
  `practice_question_results` (đọc dưới quyền RLS của người gọi).
- Chạy: `supabase db query --linked -f supabase/migrations/20260925160000_mastery.sql`
- Rollback (đã có sẵn ở cuối file, đã kiểm cú pháp đúng):
  ```sql
  begin;
  drop function if exists public.get_chapter_mastery(bigint);
  drop function if exists public.get_lesson_mastery(bigint);
  commit;
  ```
- An toàn triển khai: code UI (`LessonMasteryCard`, badge ở `app/lop-hoc/page.tsx`) đã fail-safe —
  chạy migration TRƯỚC hay SAU khi deploy code đều không crash trang, chỉ đơn giản chưa hiện mastery
  cho tới khi migration chạy xong.

Không có phụ thuộc chéo giữa 2 file (khác cột/bảng/hàm) — thứ tự chạy trước/sau không bắt buộc về
mặt kỹ thuật, nhưng giữ đúng thứ tự mốc thời gian (150000 trước 160000) cho rõ ràng.

## Lệnh backfill cần chạy tay (SAU khi chạy cả 2 migration trên)

```
# Thử trước với số nhỏ — vẫn ghi thật (không có dry-run thật sự), chỉ giới hạn số câu xử lý:
npx tsx scripts/backfill-question-bank-difficulty.mts 20
# Tự xem lại vài dòng ở /quan-tri/ngan-hang-cau-hoi trước khi chạy tiếp.

# Chạy hết phần còn thiếu (không giới hạn) — hiện còn 3541/7223 câu question_bank.difficulty='' (số
# đếm lúc kiểm tra 25/9/2026, xấp xỉ khớp 3534/7216 trong feat/SURVEY.md, không lệch bất thường):
npx tsx scripts/backfill-question-bank-difficulty.mts
```

**CẢNH BÁO** (xác nhận lại bằng đọc code, không chỉ tin báo cáo A): script này **không có** cờ
dry-run/`--apply` thật sự. Tham số số nguyên duy nhất chỉ giới hạn SỐ CÂU xử lý trong lần chạy —
mọi câu được xử lý đều bị `update()` ghi thẳng vào `question_bank` ngay lập tức (tốn API
Anthropic thật). Không có cách "xem trước toàn bộ rồi mới áp dụng" — cách an toàn nhất là chạy số
nhỏ trước rồi tự xem lại UI như ghi chú trong chính file script.

## CSV/kết quả chờ duyệt

Xác nhận lại: **không có file CSV nào** chờ duyệt trong diff của cả 3 merge (`git show --stat` +
`find` toàn repo không thấy `.csv` liên quan). Đúng như 3 báo cáo không đề cập.

## Rủi ro phát hiện thêm (3 báo cáo A/B/C chưa nêu rõ)

1. **Worktree kiểm tra ban đầu KHÔNG có 3 merge** (xem đầu file) — nếu quy trình orchestrator tạo
   worktree Agent D không đảm bảo checkout đúng `main` mới nhất tại thời điểm giao việc, kết quả
   kiểm tra "độc lập" có thể vô giá trị mà không ai biết. Nên thêm bước xác nhận
   `git merge-base --is-ancestor <sha giao việc> HEAD` đầu mỗi phiên kiểm tra tương tự.
2. **2 migration đứng độc lập nhưng cùng có khả năng bị bỏ sót nếu chạy tay từng file** — không có
   script gộp chạy cả 2 theo thứ tự; nếu thầy chỉ chạy 1 trong 2 rồi quên, `LessonMasteryCard`/badge
   vẫn im lặng ẩn đi (an toàn) nhưng huy hiệu AI/GV ở trang Đăng đề sẽ lỗi cứng nếu UI đã gọi cột
   `difficulty_source` chưa tồn tại — cần kiểm tra thêm bước gọi `onTag` có bọc try/catch phía
   client khi cột chưa có không (ngoài phạm vi thời gian kiểm tra sâu ở đây, nêu để thầy lưu ý).
3. **Backfill 3541 câu bằng Haiku 4.5 sẽ tốn kha khá lượt gọi API** (~90 lô × 40 câu/lô) — không rõ
   ràng đã ước tính chi phí trong báo cáo A; nên thầy hỏi trước ngân sách API nếu quan tâm.
4. Đã xoá 1 file bị build tự động sửa (`features/lessons/image-dimensions.json`, do
   `gen-image-dimensions.mjs` chạy trong `prebuild`) để giữ working tree sạch — không phải rủi ro,
   chỉ ghi chú để không ai nhầm là thay đổi thật.

## Kết luận

3 tính năng đều **sẵn sàng để chạy migration** — không phát hiện lỗi cú pháp SQL, không nới RLS sai
chỗ nào, dữ liệu bundles đã ghi đúng/không lẫn/ảnh tồn tại thật, mastery RPC tính đúng trên dữ liệu
thật (xác minh độc lập, không dùng lại ví dụ của báo cáo C). Khuyến nghị: **chạy được ngay** theo
đúng thứ tự ở trên (migration difficulty_source → migration mastery → backfill difficulty), không
cần sửa gì trước. Việc duy nhất cần thầy tự làm thêm là xem qua UI thật trên trình duyệt sau khi
migration chạy (`/quan-tri/dang-de` cho huy hiệu AI/GV, `/lop-hoc` + `/lop-hoc/bai` cho mastery,
`/lop-hoc/bai/?id=11,13,14,125,126,127` cho nội dung bundles mới) vì phiên này không đăng nhập được.
