---
name: hoc-phong-cach
description: Ghi lại phong cách học và dạy của thầy Thạch (cách gọi kiến thức trước khi giải, nguyên tắc nền tảng, retrieval practice, cách thầy hỏi lại học sinh khi chữa bài) vào docs/AI-TUTOR.md mục 9 + memory, thành quy tắc dùng được cho prompt và eval của AI Tutor (GĐ 4). Dùng khi thầy kể một triết lý học, một trải nghiệm học (trượt băng, học toán…), một nghiên cứu giáo dục thầy tâm đắc, hoặc một tình huống chữa bài cụ thể; khi thầy nói "ghi phong cách này", "học phong cách của tôi", "lưu cách dạy này cho AI tutor", "tôi chữa bài thế này…". KHÔNG dùng để xây tutor hay sửa prompt — chỉ ghi và chuẩn hoá nguồn phong cách.
---

# Học phong cách của thầy — ghi vào nguồn, không "học bằng trò chuyện"

Model không nhớ gì qua phiên. Phong cách của thầy chỉ tới được AI Tutor khi nằm trong **file mà prompt và eval đọc
được**: `docs/AI-TUTOR.md` mục 9 (trong git, mọi phiên thấy). Memory `user_thach_phong_cach_hoc_va_day` (chỉ trên Mac,
gitignore) là bản nháp/chỉ mục, không phải nguồn chính. Skill này làm đúng một việc: biến lời thầy kể thành mục có cấu trúc
trong hai nơi đó.

## Bước 1 — Phân loại điều thầy vừa nói

| Thầy kể về | Ghi thành | Vào mục |
|---|---|---|
| Cách thầy tiếp cận một bài / một dạng (thứ tự nghĩ, chỗ thầy nhấn) | **Quy tắc tư duy** | 9.1 hoặc mục 9.x mới |
| Trải nghiệm học của chính thầy (trượt băng, học ngoại ngữ…) | **Nguyên tắc học** + bài học rút ra | 9.2 hoặc mục mới |
| Nghiên cứu / thí nghiệm giáo dục thầy dẫn | **Cơ chế** (tên tác giả, năm, tạp chí, con số) — kiểm lại nguồn trước khi ghi, sửa chỗ thầy nhớ lệch và nói rõ với thầy | 9.3 hoặc mục mới |
| Một tình huống chữa bài cụ thể: HS hỏi/sai gì, thầy hỏi lại gì | **Ví dụ hội thoại mẫu** | 9.4 |
| Điều thầy KHÔNG muốn tutor làm ("đừng cho đáp án", "đừng khen suông") | **Cấm** | mục "Điều tutor không làm" (tạo nếu chưa có) |

Một lời kể có thể rơi vào nhiều ô. Ví dụ hội thoại là thứ quý nhất — luôn hỏi thêm nếu thầy mới kể nguyên tắc mà chưa có
tình huống: *"Thầy nhớ một lần HS sai kiểu này, thầy hỏi lại câu gì?"*

## Bước 2 — Viết mục theo khuôn cố định

Mỗi quy tắc gồm đúng 3 phần, ngắn:

```
### 9.N <tên quy tắc 5–10 chữ>

<Thầy nói gì — giữ ý và hình ảnh của thầy, kể cả ví dụ đời thường. 2–5 dòng.>

Áp vào tutor: <câu hỏi/hành vi cụ thể tutor phải làm, kèm 1 ví dụ câu hỏi thật và 1 ví dụ câu KHÔNG được hỏi.
Nếu chạm UI/luồng học (hẹn ôn, thẻ công thức…) ghi một dòng, không thiết kế ở đây.>
```

Ví dụ hội thoại mẫu (9.4) ghi dạng:

```
**Tình huống k.** <Bài gì, HS sai/hỏi gì — tóm 1–2 dòng, có thể dẫn exam/câu nếu thầy nêu.>
- HS: "…"
- Thầy: "…"   ← câu hỏi lại của thầy, giữ nguyên lời
- (HS trả lời) → Thầy: "…"
*Vì sao thầy hỏi vậy:* <1 dòng, nếu thầy giải thích>
```

## Bước 3 — Ghi vào hai nơi

1. `docs/AI-TUTOR.md` mục 9: **chỉ nối thêm**, không viết lại mục có sẵn. Mục trùng ý thì bổ sung vào mục đó một gạch
   đầu dòng có ngày, không tạo mục mới. Cập nhật dòng "(ghi từ …, bổ sung dần)" nếu cần.
2. Memory `~/.claude/projects/-Users-MAC-Projects-thachlab/memory/user_thach_phong_cach_hoc_va_day.md`: thêm một dòng
   `- YYYY-MM-DD · <ý chính> → <áp dụng>` trỏ về mục 9.N. Không chép dài — nguồn chính là AI-TUTOR.md.

Mỗi mục ghi **ngày thầy nói** (ngày hôm nay). Không gán cho thầy điều thầy không nói: phần "Áp vào tutor" là suy diễn của
agent, phải viết tách khỏi phần lời thầy.

## Bước 4 — Báo lại thầy, ngắn

3 dòng: ghi mục nào (9.N tên gì), có sửa chỗ nào thầy nhớ lệch (nguồn nghiên cứu, con số), và **một câu hỏi tiếp** để lấy
thêm ví dụ hội thoại hoặc trường hợp ngoại lệ. Không hỏi quá một câu. Không commit (thầy làm trên Mac; đụng `docs/AI-TUTOR.md`
là file riêng, commit bằng `git commit -- docs/AI-TUTOR.md`).

## Kết nối với phần còn lại

- `docs/AI-TUTOR.md` mục 7 (eval): khi mục 9 có ví dụ hội thoại mẫu, nhắc thầy thêm tiêu chí chấm thứ 4 "đúng phong cách
  thầy" và dùng ví dụ làm few-shot trong `scripts/eval-ai-tutor.mts`.
- `soan-bai-ly-thuyet-tuong-tac` / `soan-quiz-ly-thuyet`: quy tắc 9.x áp cho cả bài lý thuyết (mục "Trả bài", luyện biến thể).
  Thấy quy tắc mới ảnh hưởng cách soạn bài thì ghi một dòng vào Nhật ký rút kinh nghiệm của skill đó.
- `docs/QUY-TAC-THIET-KE.md`: ý tưởng UI nảy ra từ phong cách (hẹn ôn, thẻ công thức) chỉ ghi một dòng ở "Áp vào tutor",
  làm thật thì theo quy tắc thiết kế.

## Nhật ký rút kinh nghiệm

- 2026-10-06 · Thầy dẫn Karpicke & Roediger 2008 là "đọc tài liệu 4 lần" nhưng thí nghiệm gốc dùng cặp từ Swahili; bản văn bản
  là Karpicke & Blunt 2011 → nghiên cứu thầy dẫn luôn kiểm lại nguồn trước khi ghi, ghi đúng và nói rõ với thầy chỗ lệch.
- 2026-10-06 · Thầy hỏi "trò chuyện nhiều để AI học phong cách đúng không?" → trả lời thẳng là không; chỉ file mới tồn tại.
  Vì vậy skill này tồn tại: mỗi lần thầy kể là một lần ghi, không để trôi trong hội thoại.
