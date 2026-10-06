---
name: project-thachlab-question-bank
description: "Ngân hàng câu hỏi xếp theo năng lực cần đạt + mức độ Dễ/TB/Khó + cảnh báo câu trùng (pg_trgm); commit 5e430e55, deploy 24/9/2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: c26b382e-0c25-47b5-b93f-6aa82ebddd00
  modified: 2026-09-26T02:30:40.576Z
---

Ngân hàng câu hỏi (commit 3d8c5efe, 19/9/2026): bảng `question_bank` là bản sao có chỉ mục của từng câu trong `exams.questions`, trigger DB tự nạp khi đề tạo/sửa (kể cả từ skill up-de-kiem-tra, LessonImporter), chống trùng theo `content_hash` (md5 câu bỏ topic/form/explanation), trỏ `question_topics` (bài → yêu cầu cần đạt). Trang `/quan-tri/ngan-hang-cau-hoi` (QuestionBankAdmin) → giỏ câu (sessionStorage) → "Soạn đề" chuyển sang `/quan-tri/dang-de` ở chế độ sửa chi tiết (AzotaExamComposer đọc `takeHandoff()`).

**Trạng thái (24/9/2026):** thêm cột `difficulty` (Dễ/Trung bình/Khó) — gắn tay hoặc AI gợi ý ở trang Đăng đề/ExamSection, đồng bộ hai chiều đề ↔ ngân hàng qua `sync_exam_to_bank()`/`trg_bank_tags_to_exams()` (vá ở supabase-migration-question-bank-difficulty.sql), dòng "Mức độ:"/"Độ khó:" trong văn bản Azota cũng được parser nhận. Thêm cảnh báo câu trùng gần đúng trong cùng chủ đề bằng pg_trgm (supabase-migration-question-bank-similarity.sql) — chỉ cảnh báo, không tự gộp/xoá. Script `scripts/backfill-question-bank-difficulty.mts` gắn mức độ bằng AI cho câu cũ còn thiếu (chưa chạy, thầy tự chạy khi cần). 3 migration đã chạy trên Supabase + đã deploy (commit 5e430e55, deploy branch 649cf1d) 24/9/2026 — chưa ai test UI thật.

**Why:** thầy muốn mọi câu của đề kiểm tra/thi/luyện tập/BTVN gom lại để lấy ra soạn đề mới, sắp theo năng lực đã có trong hệ thống.

**How to apply:** deploy an toàn = `git worktree add --detach <scratch> HEAD` + `cp -Rl node_modules` + copy `.env.local` và `public/lessons`, `npm run build`, rồi làm phần push của scripts/deploy.sh trên `out/` — không đụng working tree đầy WIP ([[feedback-thachlab-deploy-scope]]). Preview localhost cần đăng nhập; không được tự nhập mật khẩu → phải nhờ thầy đăng nhập trong khung trình duyệt. Sửa nhãn trong ngân hàng sẽ ghi ngược vào mọi đề chứa câu đó (trigger `trg_bank_tags_to_exams`). Liên quan: [[project-thachlab-exam-analytics]], [[project-thachlab-dang-de-azota]].

**Cập nhật 2026-09-25:** hàm băm `question_content_hash()` đã loại thêm `difficulty` và gộp trùng 10 780 → 7 215 dòng; thêm cột `figure_not_needed`, `ai_figure`, RPC `bank_set_question_figure`, Edge Function `draw-figure`. Chi tiết ở [[project_thachlab_missing_figures]].

**Cập nhật 2026-09-26 (đợt 3 agent song song, xem [[project_thachlab_mastery_yccd]]):** thêm cột `question_bank.difficulty_source` ('gv'|'ai', migration `supabase/migrations/20260925150000_difficulty_source.sql`) để phân biệt mức độ do AI gợi ý hay giáo viên tự xác nhận — vá lại 3 hàm `sync_exam_to_bank`/`trg_bank_tags_to_exams`/`trg_bank_touch` để đọc/ghi 2 chiều đề↔ngân hàng, và `ExamSection.tsx` (trang Đăng đề/Sửa đề) hiện huy hiệu "AI gợi ý" khi `difficulty_source='ai'`, tự ẩn + đổi thành `'gv'` khi giáo viên bấm sửa tay. Đã chạy migration lên production + chạy hết `scripts/backfill-question-bank-difficulty.mts` (không giới hạn) — 3511/3544 câu rỗng trước đó đã được AI gắn mức độ (nguồn `ai`), còn **33 câu** AI không chắc/bỏ qua, cần gắn tay ở `/quan-tri/ngan-hang-cau-hoi`. Lưu ý quan trọng: script backfill **không có cờ dry-run/--apply thật** — tham số số nguyên duy nhất chỉ giới hạn SỐ CÂU xử lý trong 1 lần chạy, mọi câu được xử lý đều ghi thẳng DB + tốn API Anthropic ngay lập tức, không có bước "xem trước rồi mới áp dụng".

**Xác nhận 2026-09-29:** thầy xác nhận backfill difficulty ĐÃ XONG (con số "còn ~3541/7223 rỗng" trong docs/STATE.md là số cũ trước khi chạy). Chỉ còn ~33 câu gắn tay. Đừng nhắc lại như việc đang chờ.

**Cập nhật 2026-10-05 (gắn nhãn YCCĐ hàng loạt + đổi AI gắn nhãn sang DeepSeek):** Edge Function
`classify-questions` (nút "AI gắn nhãn" ở trang Đăng đề / ngân hàng câu hỏi) đã chuyển từ Claude
(`claude-haiku-4-5`) sang DeepSeek (`deepseek-flash`, JSON Output, `thinking: disabled`) — secret mới
`DEEPSEEK_API_KEY`, đổi model bằng secret `CLASSIFY_MODEL`; cần `supabase functions deploy classify-questions`.
`draw-figure` **giữ nguyên Claude** theo yêu cầu thầy (chi tiết + bài học ở [[project_thachlab_missing_figures]]).
Thêm script `scripts/backfill-question-bank-topics.mts` gắn `topic_name` + `form` cho câu ngân hàng còn trống nhãn
(theo lô 40 câu, mỗi lô chỉ trong MỘT khối lớp vì danh mục YCCĐ gửi kèm là danh mục của khối đó; nhãn AI trả phải
khớp NGUYÊN VĂN danh mục, không khớp thì bỏ qua chứ không đoán bừa). Trạng thái dữ liệu lúc viết script (đọc thật,
chỉ đọc): 20 687 câu chưa lưu trữ, **12 445 câu trống `topic_name`** (lớp 10 = 6 405, lớp 12 = 5 899, 141 câu
không có khối), tất cả đều là `vat-ly`, đề gốc 499 đề, phần lớn đề không có `exams.topic` nên gợi ý nguồn chỉ có
tên đề. Đã chạy thử `--dry-run 5` (không ghi DB) và đối chiếu tay 3/5 câu: nhãn khớp nội dung. Hai điểm phải nhớ:
(1) Ghi `topic_name` vào `question_bank` là **trigger DB tự lo hết** — `trg_bank_touch` tra `topic_id` theo tên,
điền lại `grade`/`subject_code` theo danh mục, `trg_bank_tags_to_exams` vá `topic`/`form` vào MỌI `exams.questions`
cùng `content_hash`; **đừng viết lại logic đồng bộ trong script**. (2) Ngân hàng **chưa có cột `topic_source`**
như `difficulty_source`, nên không phân biệt được nhãn do AI hay do người gắn — hiện chỉ có file log JSON trong
`scripts/logs/` (gitignore) làm bằng chứng + `--undo <log>` để hoàn tác. Muốn có cột đánh dấu thì phải thêm
migration (chưa làm).

**Kiểm đáp án bằng AI (2026-10-06):** `scripts/audit-question-bank-answers.mts` (chỉ đọc, không ghi DB) — DeepSeek giải MÙ từng câu rồi so với đáp án DB; lượt 1 `deepseek-flash`, lượt 2 `--stage 2` dùng `deepseek-v4-pro` cho câu lệch; báo cáo ở `scripts/logs/audit-bank-*.json/.csv`. Thử 200 câu lớp 12 (mẫu ngẫu nhiên, ~11,3k câu lớp 12, ~25% có ảnh/SVG nên bị bỏ qua): 174 khớp, 9 nghi sai, 13 "thiếu dữ kiện", 2 lỗi API. Soát tay 5/9 câu nghi sai: 2 lỗi thật (#5615 đáp án "3,42" thiếu dấu âm theo đề; #671619 đáp án "0,1" trong khi lời giải ra 1,01), 1 đề bị cắt cụt lẫn phương án (#5286), 2 báo nhầm (#440950 SGK 380 vs thực nghiệm 384; #463366 đề gõ sai đơn vị c). **Bài học:** model đúng/sai lẫn lộn ở đổi đơn vị và câu có lời giải mâu thuẫn đề → câu "nghi sai" phải có người duyệt, không tự sửa; nhóm "thiếu dữ kiện" (6,5%) là lỗi dữ liệu đề (cắt cụt/thiếu ngữ cảnh chung), không phải sai đáp án. Chi phí thật 200 câu ≈ $0.28 (giờ thấp điểm; ~820 token ra/câu — thấp hơn dự trù 1500). Ước tính cả bank (~17,5k câu kiểm được) ≈ $25 — chạy với `--conc 150` (mặc định 30 thì ~11 phút/200 câu).
