---
name: project-thachlab-phong-cach-de-bo-gd
description: Phong cách ra đề TN THPT 2025/2026 của Bộ (cấu trúc, kiểu nhiễu, giới hạn chương trình) dùng để soạn lại quiz lý thuyết cuối bài; Chương 3 lớp 12 đang soạn lại bằng batch API
metadata:
  type: project
---

Thầy gửi 2 đề Bộ (2025, 2026 mã 0211) ngày 21/10/2026 để làm chuẩn: quiz lý thuyết cuối bài **không được hỏi ngoài chương trình** (ví dụ cũ: "cực từ Trái Đất lệch trục quay bao nhiêu độ" trong bài 9 L12).

**Why:** câu ngoài chương trình không bao giờ ra thi, làm HS học lan man và mất niềm tin vào bộ câu; nghiên cứu nội dung đề Bộ đã đúc ở `.claude/skills/soan-quiz-ly-thuyet/references/phong-cach-de-bo-gd.md` (cấu trúc 18 TN / 4 Đ–S / 6 TLN, nhiễu là hiểu lầm kinh điển, 6 quy tắc loại câu ngoài chương trình). File này được nối vào prompt sinh VÀ kiểm chéo của `scripts/batch-quiz-ly-thuyet.mts`.

**How to apply:** mọi lần soạn/sửa quiz lý thuyết, đề tự soạn, câu ngân hàng cho L12 thì đọc file phong cách trước. Chương 3 L12 = chapter 4 trong DB, lesson 10, 11, 12, 13, 14, 125, 126, 127 (bài 9–16).

**Tiến độ 21/10:** đã gửi batch sinh `msgbatch_017iJ7GXDhXTyWSkeSLY7cwr` (Sonnet), chuỗi lệnh nhận → kiểm chéo (Opus) → ghi `scripts/data/theory-quiz/<id>.json` chạy ở tab terminal; bản cũ còn trong git. Chưa đăng DB: cần `publish-theory-quiz.mts --replace` + deploy sau khi thầy xem lại (T6). Các chương 1, 2, 4 L12 chưa soạn lại theo chuẩn mới.

Liên quan: [[project_thachlab_cai_tien_chuong1_l12]], [[project_thachlab_giai_lai_ngan_hang]].
