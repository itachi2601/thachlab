---
name: project_thachlab_dang_de_tags
description: "Trang Đăng đề (/quan-tri/dang-de) gắn yêu cầu cần đạt + dạng câu ngay khi đăng — commit 15091f38, đã deploy 19/9/2026 (deploy 7af1b43)"
metadata:
  type: project
---

Commit 15091f38 (2026-09-19): đề dán/thả .docx vào /quan-tri/dang-de có thể mang sẵn nhãn
phân loại theo yêu cầu cần đạt (`question_topics`, tầng con của bài) và dạng câu.

- Cú pháp trong văn bản/Word, đặt bất kỳ đâu trong khối câu (thường sau "Lời giải"):
  `Chủ đề: <tên YCCĐ đúng như danh mục>` (cũng nhận `YCCĐ:` / `Yêu cầu cần đạt:` / `Năng lực:`)
  và `Dạng: lý thuyết` | `Dạng: bài tập` (cũng nhận `Loại:`). Parser `extractTags` trong
  `services/exam-latex-parser.ts` — dùng chung cho cả .tex của LessonImporter.
- Bảng "Phân loại câu" bên cột xem trước: select YCCĐ (nhóm theo bài, bài chọn ở mục 3 lên đầu),
  nút LT/BT, gắn hàng loạt câu chưa có nhãn → `setQuestionTag` ghi dòng vào văn bản (văn bản là
  nguồn sự thật, giống bảng đáp án). Khoá khi đang "Sửa chi tiết" — khi đó gắn trong thẻ câu
  (ô Chủ đề có datalist gợi ý).
- Tên chủ đề lạ vẫn lưu nguyên văn (viền vàng); `canonicalizeQuestionTopics` chuẩn hoá hoa/thường
  lúc đăng; trigger ngân hàng câu hỏi khớp theo lower(name) để lấy topic_id.

**Why:** thầy muốn đề up lên có luôn phần phân loại như luồng nhập bài (lý thuyết/bài tập/YCCĐ),
không phải gắn tay sau trong ngân hàng.

**How to apply:** đã tsc + lint + test parser bằng Node; UI chưa bấm thử (cần đăng nhập). Đã deploy 2026-09-19
(nhánh deploy 7af1b43, build a2d09ca4 trong worktree riêng) cùng ngân hàng câu hỏi; thầy đã chạy
2 file migration. Thầy chưa phản hồi về UI thật. Skill up-de-kiem-tra chưa biết cú
pháp này — khi soạn draft từ Word có thể thêm 2 dòng nhãn cho mỗi câu.

**Bổ sung 2026-09-19 (commit sau 15091f38):** parser lấy `Lời giải:` tới hết khối câu (nối `<br>`, bỏ
dòng `Đáp án:` đứng sau) — trước chỉ lấy 1 dòng. Kèm docs/DANG-DE-TU-WORD.md viết lại cho trang Đăng đề.
