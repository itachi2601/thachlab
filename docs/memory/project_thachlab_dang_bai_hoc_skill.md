---
name: project-thachlab-dang-bai-hoc-skill
description: Skill dang-bai-hoc-thachlab từng có 2 bản lệch quy trình (Library vs ~/.codex), đã hợp nhất 21/9/2026 thêm bước gắn nhãn Chủ đề:/Dạng:
metadata:
  type: project
---

Skill `dang-bai-hoc-thachlab` (đăng bài học .tex → LMS) từng bị **2 bản lệch hẳn quy trình**, không giống
kiểu [[project_thachlab_azota_skill]]/`ngan-hang-cau-hoi` (2 bản đó vẫn giống hệt nhau). Bản Library
(`.../skills-plugin/.../skills/dang-bai-hoc-thachlab/`) mô tả đăng qua `/quan-tri/nhap-bai` bằng gói JSON
dán tay, có tạo đề. Bản `~/.codex/skills/dang-bai-hoc-thachlab/` mô tả đăng qua `/quan-tri/bai-hoc/` (HTML
tĩnh từng mục), cố ý **không** tạo `exams`. Cả hai bản đều **không có bước gắn nhãn Chủ đề:/Dạng:** —
đây là lý do các bài đăng qua skill này (khác với `azota`/`up-de-kiem-tra`/`ngan-hang-cau-hoi`) thiếu nhãn
YCCĐ dù code (`services/exam-latex-parser.ts` dòng 78-83) đã hỗ trợ sẵn 2 dòng tag này trong cú pháp `.tex`.

**Đã hợp nhất 21/9/2026** (theo yêu cầu người dùng "hợp nhất lại thành 1 bản duy nhất"): xác minh lại
source code thực tế trang `/quan-tri/nhap-bai` (`components/admin/LessonImporter.tsx`, sau commit
`5ee6a43c`) — luồng chính hiện nay là dán `.tex` trực tiếp (auto-parse `parseLessonTex`/`parseExamLatex`),
phần Đề dùng chung `ExamSection` với `/quan-tri/dang-de` (có nhãn + audit "Nhãn chủ đề trước khi đăng"
mục 4). Gói JSON `thachlab.lesson-bundle/v1` vẫn còn nhưng chỉ là lối "Nâng cao" dự phòng (ảnh scan/SVG
phức tạp). Đã viết lại `SKILL.md` + `references/tex-structure.md` (thêm mục nhãn Chủ đề:/Dạng:) +
`references/bundle-schema.md` (thêm field `topic`/`form` optional) + đồng bộ y hệt cả 2 vị trí (Library
và `~/.codex`) — từ nay chỉ còn 1 quy trình duy nhất.

**Why:** người dùng chọn hợp nhất thay vì giữ 2 luồng riêng, để tránh mất bước gắn nhãn ở bất kỳ đường
nào và để 2 bản không lệch tiếp theo thời gian.

**How to apply:** khi sửa skill này về sau, sửa **1 lần** rồi copy y hệt sang cả 2 đường dẫn (như quy tắc
cũ của `azota`/`ngan-hang-cau-hoi` trong [[project_thachlab_azota_skill]]) — đừng để lệch lại. Nếu
`/quan-tri/nhap-bai` được viết lại lần nữa (đổi luồng chính), phải đọc lại source code thật trước khi tin
nội dung SKILL.md cũ, vì tài liệu skill đã từng lỗi thời so với code 1 lần.

Việc backfill nhãn cho các câu hỏi **cũ đã đăng** (trước khi có bước này) chưa làm — người dùng chọn "chưa
backfill, chỉ lo sửa skill trước" trong phiên 21/9/2026. Không có sẵn cơ chế gắn nhãn hàng loạt: Edge
Function `classify-questions` (`supabase/functions/classify-questions/index.ts`) đòi JWT người dùng, giới
hạn 60 câu/lần, chỉ xử lý 1 đề đang mở trên UI. Muốn backfill toàn bộ `exams` phải viết script Node mới
(service-role, mẫu kết nối như `scripts/restore-posts.mjs`, tái dùng `auditQuestionTags`/
`canonicalizeQuestionTopics` từ `features/exams/types.ts`).

**"Bài tập mẫu tự chấm" — code có sẵn nhưng UI thiếu, đã vá 21/9/2026 (commit `6044b006`).** Kiểm tra
thực tế trên app thấy: dù `SampleQuestionsGrid`/`QuestionCard` (ghi đáp án → Kiểm tra → tô đúng/sai →
mới hiện lời giải) đã có trong code từ commit `7bb1fa06` (xem [[project_thachlab_lesson_sections]]), CẢ
`/quan-tri/nhap-bai` (`LessonImporter.tsx`) LẪN `/quan-tri/dang-de` (`AzotaExamComposer.tsx`) chưa bao giờ
có ô tick "Bài tập mẫu" để gắn `exam_ids` vào đó — mọi mục Bài tập mẫu trong Supabase thực tế đều
`exam_ids: []`, nên học sinh chỉ thấy dạng cũ (`WorkedQuestionsGrid`, mở ra là thấy lời giải ngay, không
tự chấm). Đã thêm ô tick thứ ba "Bài tập mẫu (tự chấm)" ở cả 2 trang, sửa `LessonImporter` để không đè
mất `questions` (dạng bài prose) khi chỉ gắn thêm đề tự chấm, và sửa `AzotaExamComposer` (trước đó luôn
ghi `questions: []` khi update — sẽ xoá mất dạng bài nếu gắn kind `bai_tap_mau` mà không sửa). Đã cập
nhật `SKILL.md` + `references/tex-structure.md` (mục "Ví dụ tự chấm trong Bài tập mẫu") ở cả 2 vị trí
skill, giải thích khi nào dùng văn xuôi (`VÍ DỤ`/`DẠNG n`, đọc-không-chấm) vs khi nào soạn theo mẫu Azota
(`Câu n.`/`Đáp án:`/`Lời giải:`) để gắn được vào Bài tập mẫu tự chấm — và vì `parseLessonTex` gộp cả file
thành 1 khối đề duy nhất, nếu bài cần cả ngân hàng Luyện tập/Kiểm tra riêng thì phải đăng 2 lượt.

**Why:** người dùng hỏi "cập nhật skill để câu ví dụ định dạng đúng có luồng tự chấm" — kiểm tra thì phát
hiện gốc vấn đề không phải ở skill mà ở UI admin thiếu tuỳ chọn, nên phải sửa code trước rồi mới sửa skill.
**How to apply:** đã build + typecheck + xác nhận UI (checkbox hiện đúng, tick được) qua Browser pane
local. Chỉ commit đúng 2 file `AzotaExamComposer.tsx`/`LessonImporter.tsx` bằng `git commit <path>`
(không qua `git add` — xem [[project_thachlab_concurrent_sessions]] về race của index dùng chung).

**Cập nhật 2026-09-21 tối:** thầy xác nhận đã test đăng thật + deploy (commit `6044b006` nằm trong
build `deploy` branch 22:30:32). Coi như xong.

**Cập nhật 2026-09-22 — đổi luồng mặc định sang script cục bộ để tiết kiệm token.** Theo yêu cầu người
dùng, "Quy trình chính" giờ là: dựng gói JSON `thachlab.lesson-bundle/v1` rồi chạy
`npx tsx scripts/upload-lesson.mts bundle.json --lesson <id> ...` (sửa luôn lệnh cũ ghi sai
`node scripts/upload-lesson.mjs` — file thật là `.mts`, chạy qua `npx tsx`) — không cần mở/lái trình
duyệt. Trang `/quan-tri/nhap-bai` (dán `.tex` trực tiếp hoặc dán gói) lùi thành "Đường thay thế": dùng khi
cần xem preview trực tiếp, cần nút "AI gắn nhãn" ngay lúc soạn, hoặc cần tick "Bài tập mẫu (tự chấm)" —
`upload-lesson.mts` **chưa hỗ trợ** gắn `exam_ids` vào `bai_tap_mau` (chỉ gắn được `luyen_tap`/`kiem_tra`),
đây là giới hạn thật của script, không phải thiếu sót tài liệu. Đường script không có audit nhãn tự động
như trang — phải tự soát `topic`/`form` trong gói trước khi chạy, vá thiếu sau bằng nút "AI gắn nhãn" ở
`/quan-tri/ngan-hang-cau-hoi` (đã có từ trước, xem đoạn dưới).

**An toàn quan trọng thêm vào lần này:** `upload-lesson.mts` hỏi `SUPABASE_SERVICE_ROLE_KEY` (nhập ẩn) —
đã ghi rõ trong SKILL.md là **không bao giờ tự nhập/tự cầm key này** (cùng nhóm với mật khẩu admin/database
đã cấm từ trước), phải chạy lệnh qua tab Terminal của người dùng để chính họ gõ. Đây là quy tắc an toàn hệ
thống (cấm nhập API key/token dù được yêu cầu), không phải tuỳ chọn.

**Why:** người dùng nói "cập nhật kỹ năng đăng bài tiết kiệm hơn nữa: dùng nhánh script cục bộ ... thay vì
qua browser" — driving trang admin qua Browser pane (nhiều bước screenshot/click) tốn token hơn hẳn một
lệnh script, khớp [[feedback_token_discipline]].

**How to apply:** đã sửa cả 2 vị trí skill (Library + `~/.codex`, đồng bộ y hệt — `diff` xác nhận). Lần tới
gặp file `~/.codex/skills/dang-bai-hoc-thachlab/SKILL.md` bị lệch nội dung so với snapshot cũ trong memory
này (như lần 22/9: phiên khác đã thêm mục "vá nhãn"/thư mục lưu gói JSON cố định TRƯỚC khi mình sửa) —
đọc lại file thật ngay trước khi ghi đè, đừng tin nội dung nhớ từ đầu phiên (khớp
[[project_thachlab_concurrent_sessions]] dù đây không phải git).
