---
name: soan-quiz-ly-thuyet
description: >-
  Tự soạn bộ câu hỏi "Kiểm tra nhanh" (định nghĩa, định luật, công thức, đơn vị) cho từng bài học
  thachlab từ CHÍNH nội dung lý thuyết đã có trong public/data — không cần file đề đầu vào. Dùng
  khi nói "soạn quiz lý thuyết cho bài X", "soạn bộ câu công thức lớp 12", "tạo kiểm tra nhanh
  cho cả chương", "làm quiz lý thuyết cả lớp 12". KHÁC up-de-kiem-tra (skill đó nhận MỘT file đề
  Word/PDF có sẵn rồi đăng) — skill này tự sinh câu, kiểm chéo, ghi file JSON; đăng lên DB bằng
  script riêng chạy trên Mac.
---

# Soạn quiz lý thuyết + công thức cho từng bài

**Chạy được trên cloud** (không cần DB, không gọi API ngoài — chính Claude Code sinh câu).
**Đăng lên DB phải chạy trên Mac** (`scripts/publish-theory-quiz.mts`, cần service role).

## Chuẩn bị
- `public/data/` bị gitignore; nếu chưa có: `node scripts/build-content.mjs` (chỉ đọc bằng anon key).
- Tên YCCĐ (tuỳ chọn): `scripts/data/question-topics.json` (do `scripts/export-question-topics.mts` chạy trên Mac xuất).
  **Chưa có file → `topic` = đúng `lesson.title`** (nhãn tầng Bài, hệ mastery vẫn nhận). Có file → chọn tên
  chủ đề con của bài (`lesson_id` khớp, kể cả con qua `parent_id`) sát nhất với ý của câu; không có tên nào hợp thì dùng `lesson.title`.

## Quy trình
1. **Chọn bài.** Nhận một/nhiều `lesson_id`, hoặc "cả lớp 12": trong `public/data/catalog.json` lấy `lessons` mà
   `chapters[chapter_id].classIds` chứa 18. Bỏ bài `lesson_kind` ≠ `bai_hoc`, bỏ bài không có mục `ly_thuyet`,
   bỏ bài đã có `scripts/data/theory-quiz/<id>.json` (trừ khi được bảo làm lại).
2. **Đọc bài.** Từ `public/data/lessons/<id>.json` lấy mục `kind === "ly_thuyet"`: `summary_html` + `body_html`.
   Chạy `npx tsx .claude/skills/soan-quiz-ly-thuyet/scripts/list-sections.mts <id>` → bảng đoạn.
   **Chỉ số ở cột "đoạn" là giá trị duy nhất được dùng cho `theorySection`** (0-based, do đúng hàm `wrapTheorySections`
   sinh) — không tự đếm bằng cách khác. Mục không có đoạn nào → bỏ `theorySection`.
3. **Bước A — Phiếu kiến thức** (trong đầu hoặc file tạm ở scratchpad): khái niệm/định luật + phát biểu chuẩn; công
   thức LaTeX + tên từng ký hiệu + đơn vị + điều kiện áp dụng; mỗi mục ghi thuộc đoạn số mấy.
4. **Bước B — Sinh 12 câu**, theo `references/prompt-sinh-cau.md` (tỉ lệ: 5 TN · 3 ĐS · 4 TLN; ≥ 8 câu Dễ, không Khó).
5. **Bước C — Kiểm chéo**: giao MỘT subagent khác (Agent) theo `references/prompt-kiem-cheo.md`, đưa nguyên văn
   `body_html` + bảng đoạn + 12 câu. Câu "sai"/"nghi ngờ" hoặc `theorySection` sai → sửa nếu chỉ lệch đoạn, ngược lại
   loại và ghi `review.removed[{question, reason}]`. Còn < 10 câu → sinh bù rồi kiểm lại (tối đa 2 vòng).
6. **Ghi file** `scripts/data/theory-quiz/<lesson_id>.json` (schema dưới), rồi
   `npx tsx .claude/skills/soan-quiz-ly-thuyet/scripts/validate-quiz.mts scripts/data/theory-quiz/<id>.json` —
   chỉ giữ file khi qua. `quiz_min_correct` = làm tròn lên 75% số câu còn lại.
7. **Kết thúc**: in bảng *bài · số câu · số câu bị loại*, rồi nhắc lệnh đăng (thầy chạy trên Mac):
   `npx tsx scripts/publish-theory-quiz.mts --lesson <id> [--dry-run]`, sau đó `bash scripts/deploy.sh`.

## Schema file
```json
{ "lesson_id": 10, "lesson_title": "Bài 9. …", "item_id": 42, "generated_at": "2026-09-30",
  "generated_by": "claude-code", "quiz_min_correct": 9,
  "review": { "checked": true, "removed": [ { "question": "…", "reason": "…" } ] },
  "questions": [ … ] }
```
Câu hỏi đúng `features/exams/types.ts` (`multiple_choice` / `true_false` / `short_answer`) + `topic`, `form: "ly_thuyet"`,
`difficulty` ∈ `Dễ | Trung bình | Khó` (script đăng đổi sang mã DB `de|trung-binh|kho`), `difficultySource: "ai"`,
`theorySection`, và `kind` ∈ `dinh_nghia | dinh_luat | cong_thuc | don_vi | tinh_nhanh | hien_tuong` (chỉ để soát;
script đăng bỏ trước khi ghi DB). `short_answer.answer` ≤ 4 ký tự, chỉ `0-9 , -`. Công thức viết `$…$`.

## Ví dụ (rút gọn)
- ✓ TN công thức: "Hệ thức giữa $T$ (K) và $t$ (°C)?" — nhiễu: `T = t − 273` (sai dấu), `T = t + 373` (nhầm hằng số), `t = T + 273` (đảo chiều) → lỗi HS hay mắc.
- ✗ Nhiễu bịa: `T = t² / 273` (vô nghĩa, loại ngay khi đọc); câu phải dùng kiến thức bài khác; đáp án TLN "0,3333" (> 4 ký tự).
- ✓ ĐS: 4 ý xoay quanh một định luật, có ý sai tinh vi ("áp suất tỉ lệ thuận với thể tích").
- ✓ TLN: số tròn, 1 bước: "Đổi $27\,^\circ\mathrm C$ sang K" → `300`.
