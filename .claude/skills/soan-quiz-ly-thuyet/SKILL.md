---
name: soan-quiz-ly-thuyet
description: Tự soạn bộ 20 câu "Kiểm tra nhanh" (10 kiến thức + 10 công thức) cho mục lý thuyết của từng bài học từ chính nội dung bài trong public/data — KHÔNG có file đề đầu vào. Dùng khi thầy nói "soạn quiz lý thuyết cho bài X", "soạn bộ câu công thức lớp 12", "tạo kiểm tra nhanh cho cả chương". Khác up-de-kiem-tra (skill đó đăng đề có sẵn từ file Word/LaTeX). Sinh + kiểm chéo + validate chạy được trên cloud (không cần DB); ĐĂNG lên DB phải chạy trên Mac.
---

# Soạn quiz lý thuyết cho từng bài

Đầu ra: `scripts/data/theory-quiz/<lesson_id>.json`. Đăng bằng `scripts/publish-theory-quiz.mts` (Mac). Skill **không gọi API Anthropic, không cần DB/key** — Claude Code tự sinh câu, script chỉ liệt kê đoạn, kiểm và đăng.

Quy ước `difficulty`: dùng **mã** của `features/exams/types.ts` — `"de"` (Dễ), `"trung-binh"` (Trung bình); không dùng "kho". Nhãn tiếng Việt chỉ để nói với thầy.

## Quy trình

1. **Chọn bài.** Một hoặc nhiều `lesson_id`, hoặc "cả lớp 12" → lấy từ `public/data/catalog.json`: bài có `chapters[chapter_id].classIds` chứa `18`. Bỏ bài có `lesson_kind` ≠ `bai_hoc`, bài không có mục `ly_thuyet`, và bài đã có file JSON (trừ khi thầy bảo làm lại).
2. **Đọc bài.** `public/data/lessons/<id>.json` → mục `kind === "ly_thuyet"`: `summary_html` + `body_html`. Rồi chạy
   `npx tsx .claude/skills/soan-quiz-ly-thuyet/scripts/list-sections.mts <id>` — đây là **nguồn duy nhất** của chỉ số `theorySection` (0-based, sinh bởi `wrapTheorySections`). Không tự đếm. Bài không có đoạn nào → bỏ `theorySection`.
3. **Bước A — Phiếu kiến thức** (trong đầu hoặc file tạm ở scratchpad): khái niệm/định luật + phát biểu chuẩn; công thức LaTeX + tên từng ký hiệu + đơn vị + điều kiện áp dụng; mỗi mục ghi thuộc đoạn số mấy.
4. **Bước B — Sinh 20 câu** theo `references/prompt-sinh-cau.md`. Chia 10 câu kiến thức (`kind`: dinh_nghia, dinh_luat, hien_tuong, dieu_kien) + 10 câu công thức (`cong_thuc`, `don_vi`, `tinh_nhanh`, `bien_doi`); dạng: 10 TN, 4 đúng–sai, 6 trả lời ngắn. Bài ít công thức: lấy tối đa công thức có được, phần thiếu bù bằng câu kiến thức; ghi đúng số vào `review.counts`. Thêm `topic`: nếu có `scripts/data/question-topics.json` thì chọn tên YCCĐ của bài (`lesson_id` khớp) sát nội dung câu; chưa có file (hoặc bài không có dòng) → `topic` = đúng `lesson.title`.
5. **Bước C — Kiểm chéo.** Giao **một subagent khác** (prompt: `references/prompt-kiem-cheo.md`) đọc lại nguyên văn `body_html` + các câu, trả đúng / sai / nghi ngờ + lý do + kiểm `theorySection`. Câu "sai"/"nghi ngờ" → loại, ghi `review.removed` `{question, reason}`. Còn < 18 câu → sinh bù rồi kiểm lại (tối đa 2 vòng). Đặt `review.checked: true` chỉ sau bước này.
6. **Validate.** `npx tsx .claude/skills/soan-quiz-ly-thuyet/scripts/validate-quiz.mts scripts/data/theory-quiz/<id>.json` — chỉ giữ file khi qua. `quiz_min_correct` = làm tròn lên 75% số câu.
7. **Báo cáo.** Bảng: bài nào xong · số câu · số câu bị loại (kèm lý do). Nhắc thầy chạy trên Mac:
   ```
   npx tsx scripts/export-question-topics.mts     # 1 lần, để gắn topic theo YCCĐ
   npx tsx scripts/publish-theory-quiz.mts --lesson <id> [--lesson <id>…] [--dry-run] [--replace]
   bash scripts/deploy.sh                          # site tĩnh, không deploy thì web chưa thấy
   ```

## Dạng file (`review`, `kind` chỉ để soát — script đăng bỏ `kind`)

```json
{ "lesson_id": 10, "lesson_title": "…", "item_id": 42, "generated_at": "2026-09-30", "generated_by": "claude-code",
  "quiz_min_correct": 15,
  "review": { "checked": true, "counts": { "kien_thuc": 10, "cong_thuc": 10 }, "removed": [ { "question": "…", "reason": "…" } ] },
  "questions": [ { "type": "multiple_choice", "kind": "dinh_nghia", "topic": "…", "form": "ly_thuyet",
    "difficulty": "de", "difficultySource": "ai", "theorySection": 0,
    "question": "…", "options": ["…","…","…","…"], "answer": 1, "explanation": "…" } ] }
```

Đúng–sai: `statements: [{text, answer:boolean}×4]`; trả lời ngắn: `answer` ≤ 4 ký tự gồm `0-9 , -`. Công thức LaTeX `$…$`.

## Câu tốt / câu xấu

- ✓ "Công thức tính $p$ theo $\rho$ và $\overline{v^2}$?" — nhiễu: `\frac{1}{3}` → `\frac{2}{3}`, thiếu bình phương, đảo tử/mẫu (lỗi học sinh hay mắc).
- ✗ Nhiễu là công thức bịa vô nghĩa (đơn vị không cùng thứ nguyên) → loại.
- ✓ Đúng–sai 4 ý cùng xoay quanh 1 định luật, có ý sai tinh vi (đổi "tỉ lệ thuận" ↔ "tỉ lệ nghịch").
- ✗ Câu cần kiến thức bài khác / số liệu không có trong mục lý thuyết → loại (kể cả khi đúng về vật lí).
