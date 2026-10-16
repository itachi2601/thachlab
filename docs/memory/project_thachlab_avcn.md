---
name: project-thachlab-avcn
description: "Lớp Anh văn chuyên ngành Cơ khí (avcn, CTTC, vào tự do) — Chapter 8 mẫu đã đăng 13/10/2026, skill soan-bai-avcn cho 9 chương còn lại"
metadata:
  node_type: memory
  type: project
  originSessionId: 5a69a7bf-72bc-4878-b485-79b78752f6c3
  modified: 2026-10-12T17:32:37.101Z
---

Thầy dạy AVCN Cơ khí ở CĐ Cao Thắng, SV yếu tiếng Anh; mục tiêu nhớ từ + thi cuối kỳ ≥ 5/10. Lớp **miễn phí, vào tự do**
(thầy chốt 13/10/2026). Đề cuối kỳ 5 Part cố định (Part 1–3 = 7 điểm nhận diện từ + đọc lại Article giáo trình) — mọi
quyết định soạn bài bám vào đó (`docs/DE-XUAT-AVCN-CHUONG-8-2026-10-12.md`).

- Hạ tầng: lớp `avcn` id 20, môn `academic_subjects.avcn`, chương "Technical English…", 10 bài id 168–177 (Chapter n = 167+n),
  chỉ 175 (Chapter 8) `published=true`; đề luyện tập 914. Migration `20261013100000` đã chạy 13/10.
- Code: `MANAGED_CLASSES` có avcn (không hiện dải THPT), hub `/lop-hoc/avcn` lấy môn `avcn`; nút 🔊 `button[data-tl-speak]`
  xử lý trong `components/exams/ContentHtml.tsx`; CSS `.avcn-*` cuối `globals.css`.
- Nội dung: `content/lesson-samples/avcn-chapter-8-chipping-machining/data/bai.json` là nguồn; dựng bằng
  `.claude/skills/soan-bai-avcn/scripts/build_avcn.py`. Ảnh Wikimedia Commons CC BY/CC0 ở `public/assets/avcn/chapter-8/`
  + `credits.json` (thầy nói "lớp miễn phí nên lấy ảnh trên mạng" → vẫn chỉ dùng ảnh giấy phép mở, ghi nguồn; cam kết `/dieu-khoan`).
- Giáo trình: `/Users/MAC/Documents/CTTC/1 - Giảng dạy/Anh văn chuyên ngành/2026/technical english-final-2.docx`; đề cũ
  `…/AVCN (tổng hợp)/TACN (đáp án)/`.
- Còn treo: 9 chương (1–7, 9, 10) chưa soạn — dùng skill `soan-bai-avcn` (Claude điền hoặc Gemini điền JSON rồi Claude đối
  chiếu); chưa thử với SV thật; chưa có kiểu câu "điền một từ" trong engine đề (short_answer chỉ nhận số); 12 quiz/bài
  vượt hạn 8 của lint Vật lí (cố ý).
- Chapter 5 (Mechanical Fasteners): 13/10 thầy dán `bai.json` do Gemini điền (chưa lưu vào repo). Kiểm sơ bộ: JSON có thể lỗi
  dấu `"` trần trong chuỗi, nhiều `fb_no` lộ đáp án, vài câu Article >25 từ, Part 1 có "[hình: …]" bằng chữ, chưa có ảnh Commons.
  Chưa đối chiếu giáo trình. Việc tiếp: lưu vào `content/lesson-samples/avcn-chapter-5-…/data/bai.json`, sửa, đối chiếu, dựng — hoặc Claude soạn thẳng.

Liên quan: [[feedback-xuong-dong-tung-truong-hop]], [[project-thachlab-cttc-roster-import]].

- 16/10/2026: Article mỗi câu ≤2 từ đố 3 phương án + chạm xem nghĩa, đã đăng Chapter 8 (bài 175) và deploy. Hộp Flashcard (link 404) đã gỡ theo thầy; muốn thêm lại thì đặt `meta.flashcard` trong bai.json khi trang flashcard có thật.
- 16/10/2026: Chapter 5 Mechanical Fasteners do Claude soạn thẳng (bỏ nháp Gemini), thầy duyệt → đăng bài 172 (đề luyện tập 920), published, deploy; `content/lesson-samples/avcn-chapter-5-mechanical-fasteners/`. Còn 8 chương (1–4, 6, 7, 9, 10).
