---
name: soan-bai-tap-mau
description: Soạn mục BÀI TẬP MẪU của một bài học thachlab — 2–4 dạng bài cho mỗi bài, mỗi dạng có đề, 3 gợi ý mở dần (kiến thức + điều kiện áp dụng → dữ kiện/hướng giải → công thức), lời giải đầy đủ theo phong cách thầy Thạch (AI-TUTOR 9.1/9.3/9.5), gắn YCCĐ để web tự tìm 3 bài tương tự trong ngân hàng câu hỏi sau khi học sinh đọc xong. Dùng khi thầy nói "soạn bài tập mẫu cho bài X", "làm các dạng bài tập của bài…", "thêm bài tập mẫu có gợi ý", "bài tập mẫu theo phong cách của tôi". Khác soan-bai-ly-thuyet-tuong-tac (bài lý thuyết, có sẵn "bài toán mẫu" nằm TRONG lý thuyết) và dang-bai-hoc-thachlab (đăng .tex). Soạn + kiểm chạy được trên cloud; ĐĂNG lên DB phải chạy trên Mac.
---

# Soạn Bài tập mẫu có cấu trúc (thầy chốt 6/10/2026)

Mục **Bài tập mẫu** (`lesson_items.kind='bai_tap_mau'`, cột `questions`) thay nội dung cũ bằng các **dạng bài** có cấu trúc. Web (`components/lessons/WorkedQuestionsGrid.tsx`) hiện mỗi dạng: **đề → tự thử trên giấy → gợi ý 1/3, 2/3, 3/3 mở dần → "Xem lời giải đầy đủ" → nút "Làm bài tương tự"** (`SimilarBankPractice.tsx`, bốc 3 câu cùng YCCĐ/Dạng từ `question_bank` qua RPC `get_similar_bank_questions`, chấm ngay, "Làm 3 câu khác"). Dạng cũ chỉ có `body_html` vẫn hiển thị bình thường.

Đầu ra: `scripts/data/bai-tap-mau/<lesson_id>.json`. Đăng: `scripts/publish-bai-tap-mau.mts` (Mac, chỉ ghi cột `questions` của đúng mục, tự sao lưu). Skill **không cần DB/key**.

## Phong cách thầy Thạch — đọc `docs/AI-TUTOR.md` mục 9 trước khi viết (nguồn chuẩn, đừng chép lại ở đây)

Áp vào từng dạng:
1. **Gợi ý 1 = kiến thức + ĐIỀU KIỆN áp dụng** (9.1). Thứ tự: khái niệm → định luật → công thức → điều kiện dùng được. Câu mở đầu là câu hỏi về điều kiện ("Có lực nào không phải lực thế không? Vậy đại lượng nào bảo toàn?"), **không đưa công thức**. Validator cảnh báo nếu gợi ý 1 không có chữ "điều kiện".
2. **Gợi ý 2 = đọc đề lấy dữ kiện + chọn hướng** (nêu đại lượng cho/hỏi, hệ quy chiếu, đơn vị). **Gợi ý 3 = công thức/phép biến đổi** — chỉ lúc này mới chạm công thức.
3. **Lời giải**: bắt đầu bằng khung "Kiến thức cần gọi lại" (khái niệm → định luật → công thức → điều kiện), rồi giải từng bước đánh số, **kiểm đơn vị/hợp lí của kết quả**, kết bằng 1 dòng "Dạng này nhận ra khi… → làm…" (nhận dạng). Số liệu 3–4 chữ số có nghĩa, ghi đơn vị (9.4 tình huống 1).
4. **Câu khái niệm** thì nói thẳng ngắn gọn rồi khái quát (9.5); **không** hỏi ngược trong lời giải.
5. **Retrieval** (9.3): web đã đặt chữ "gấp lại, tự trình bày từ đầu" trước nút bài tương tự; trong lời giải, dòng cuối nhắc "3 ngày sau che lời giải, giải lại".
6. **Nền trước, kỹ năng sau** (9.2): các dạng trong một bài xếp **từ cơ bản → kết hợp**, dạng sau dùng lại cách làm dạng trước. Dạng khó nhất là dạng 3–4.
7. **KHÔNG dùng vai "thầy/cô"** trong nội dung (feedback 2/10/2026, validator chặn). Giọng trung tính, câu ngắn, đánh số khi nhiều ý, không mở bằng lời khen.

## Quy trình

1. **Chọn bài** (`lesson_id`). Đọc `public/data/lessons/<id>.json` mục `ly_thuyet` (để dạng bài **khớp đúng kiến thức bài đã dạy**, cùng ký hiệu), và mục `bai_tap_mau` hiện có (không để mất ví dụ hay đang có — đưa lại thành 1 dạng nếu tốt). Nếu thiếu `public/data`: `npm ci && node scripts/build-content.mjs`.
2. **Chốt 2–4 dạng** (mặc định thử **1 bài trước**, thầy duyệt rồi mới nhân ra cả chương). Mỗi dạng = một kiểu bài học sinh sẽ gặp lặp lại trong đề (không phải 4 bài số khác nhau của cùng một cách làm). Với mỗi dạng chọn **`topic` = tên YCCĐ con** sát dạng nhất trong `scripts/data/question-topics.json` (đúng `lesson_id` của bài; sao chép nguyên văn). Vì bài tương tự lấy theo YCCĐ, YCCĐ quá rộng → bài lạc dạng; chỉ có chủ đề cha → ghi rõ cho thầy.
   - Soát nhanh ngân hàng trước khi chốt: `topic` đó có bao nhiêu câu `bai_tap` chưa lưu trữ (`select count(*) from question_bank where topic_id=… and form='bai_tap' and not archived`, chạy trên Mac). < 6 câu → báo thầy, vì nút bài tương tự sẽ nhanh hết.
3. **Soạn từng dạng** (đề riêng, số liệu mới; không chép câu có trong ngân hàng nguyên văn): `problem_html`, `hints_html` (đúng 3), `solution_html`. LaTeX `$…$`; `<`/`>` trong công thức viết `\lt`/`\gt`. Hình cần thiết: SVG tự vẽ như bài lý thuyết (`soan-bai-ly-thuyet-tuong-tac/references/hinh-svg.md`), ảnh nén ≤ ~1200px (AGENTS.md "Đăng nội dung").
4. **Kiểm chéo bắt buộc**: giao subagent `kiem-code` đọc lại **từng dạng**, tự giải độc lập (không nhìn lời giải) rồi so; trả đúng/sai/nghi ngờ + lý do. Sai số, đơn vị, hoặc gợi ý lộ đáp án → sửa. Chỉ đặt `review.checked: true` sau bước này.
5. **Validate**: `npx tsx .claude/skills/soan-bai-tap-mau/scripts/validate.mts scripts/data/bai-tap-mau/<id>.json`.
6. **Báo cáo** + in lệnh cho thầy trên Mac (xem mục "Đăng"). Viết "Rút kinh nghiệm" theo AGENTS.md vào Nhật ký cuối file này.

## Dạng file

```json
{ "lesson_id": 57, "lesson_title": "Chuyển động ném", "generated_at": "2026-10-06",
  "review": { "checked": true, "notes": "…" },
  "dang_bai": [ {
    "label": "Dạng 1 · Ném ngang: tìm thời gian bay và tầm xa",
    "topic": "<tên YCCĐ con, nguyên văn>", "form": "bai_tap",
    "problem_html": "<p>…</p>",
    "hints_html": ["<p>Điều kiện: … Vậy …?</p>", "<p>Dữ kiện: … Chọn hệ …</p>", "<p>Công thức: $…$</p>"],
    "solution_html": "<div class=\"tl-box\">…Kiến thức cần gọi lại…</div><ol class=\"tl-steps\">…</ol><p>Nhận dạng: …</p>" } ] }
```
`topic_id` và `body_html` (gộp để chỗ cũ đọc được) do script đăng sinh — không tự điền. Dùng linh kiện `.tl-*` có sẵn (`tl-box`, `tl-steps`, `tl-table--data`) cho khớp bài lý thuyết.

## Đăng (Mac)

Điều kiện: migration `20261006180000_similar_bank_questions.sql` đã chạy (không thì nút "Làm bài tương tự" báo "Chưa tải được"; phần còn lại vẫn chạy).
```
cd /Users/MAC/Projects/thachlab && git pull origin main
npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --dry-run
npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --giu-cu   # bỏ --giu-cu = GHI ĐÈ toàn bộ dạng cũ
bash scripts/deploy.sh
```
Chạy lệnh dài trong tab terminal (AGENTS.md). Phiên cloud: chỉ soạn + validate, in lệnh cho thầy.

## Giới hạn đã biết

- **Bài đã có dạng cũ (bài 57 có 19 dạng) → luôn đăng bằng `--giu-cu`** (dạng mới lên đầu, dạng cũ nối sau). Không cờ này là ghi đè hết.

- Bài tương tự lấy theo **YCCĐ (+ `form`)**, ngân hàng không có nhãn "dạng bài con" → độ sát phụ thuộc YCCĐ chọn đúng.
- RPC lộ đáp án cho HS đăng nhập (như PracticeSession); không dùng cho bài tính điểm. Chưa ghi kết quả bài tương tự vào `practice_sessions`/mastery (RPC không trả mã đề nguồn) — làm sau nếu thầy muốn.

## Nhật ký rút kinh nghiệm (bắt buộc cập nhật cuối MỖI phiên dùng skill này — xem `AGENTS.md`)

- 2026-10-06 · Pilot bài 57 (3 dạng) → kiểm chéo bắt đề Dạng 3 mơ hồ ("đứng trên mái nhà" không rõ điểm ném, vật cản không nằm trên đường bay) → đề bài có hình học phải nói rõ **điểm ném, mốc đo khoảng cách, vật cản nằm đâu**; khung "Kiến thức" phải chứa mọi ký hiệu lời giải dùng (L).
- 2026-10-06 · Validator chặn `<`/`>` trong `$…$` ngay lần chạy đầu (tôi viết `$v>v_0$`) → viết `\lt`/`\gt` từ đầu.
- 2026-10-06 · YCCĐ trong bank có 2 con/bài (bài 57) nên Dạng 1 và 3 cùng `topic` → bài tương tự của hai dạng sẽ trùng nguồn; chấp nhận, nhưng ngân hàng không có nhãn "dạng bài con".

- 2026-10-06 · Đăng bài 57 không cờ giữ cũ → ghi đè 19 dạng cũ bằng 3 dạng mới (có sao lưu, đã nối lại) → script đăng phải mặc định cảnh báo số dạng cũ sẽ mất; dùng `--giu-cu` cho bài đã có nội dung.
