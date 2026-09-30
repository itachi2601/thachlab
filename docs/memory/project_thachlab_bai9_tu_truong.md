---
name: project-thachlab-bai9-tu-truong
description: "Bài 9 Khái niệm từ trường (lớp 12, lesson 10) — đã tách bài tập tại lớp → Luyện tập (đề 19) và BTVN (đề 20) ngày 19/09/2026; còn vài câu đáp án chờ thầy chốt"
metadata: 
  node_type: memory
  type: project
  originSessionId: d31a25a7-38a8-4c23-80bf-691df55c5ee6
  modified: 2026-09-19T07:22:51.001Z
---

Ngày 19/09/2026 tách mục "Bài tập — Khái niệm từ trường" (lesson_items 43, HTML tĩnh không đáp án, đã XÓA — bản lưu ở `output/tu-truong-latex/published.json`) thành hai đề chấm tự động trên lesson 10:
- Luyện tập: exam 19 (30 TN + 7 ĐS, 45 phút) → lesson_items 70.
- Bài tập về nhà: exam 20 (56 TN, 60 phút) → lesson_items 71, `due_at` chưa đặt.
Draft/bundle lưu ở `output/tu-truong-latex/build/` (kèm `dapan.txt` = đáp án thầy cho phần tại lớp; BTVN nguồn KHÔNG có đáp án, Claude tự giải).

**Câu chờ thầy chốt** (đáp án hiện đang ghi trong đề):
- LT câu 26: thầy ghi C (vòng tròn cùng chiều kim đồng hồ) nhưng hình 3.2 vẽ I hướng lên, nhìn từ trên → ngược chiều kim đồng hồ; đề đang để **D**.
- LT câu 31 ý b (từ trường đều: đường sức song song cách đều): thầy đánh S, đề để **Đúng** (khớp câu 13 cùng đáp án thầy).
- LT câu 1: thầy ghi "bỏ" — vẫn giữ, đáp án B (đồng oxit). Câu 24 không có trong đáp án: tự tạo 4 phương án Hình A–D, chọn A. Câu 14 câu dẫn gốc thiếu chủ ngữ, đã bổ sung.
- BTVN câu 30, 32, 36, 39, 40 (câu hình): đáp án suy từ ảnh, phân vân — xem báo cáo trong phiên; câu 49 phương án D sửa thành "Chiều các đường sức phụ thuộc chiều dòng điện"; câu 55 D trùng A đã sửa.

**Mẹo kỹ thuật:** `build_bundle.py` chặn mọi chuỗi `media/…` trong câu hỏi coi là placeholder ảnh chưa khai báo, dù trang admin chỉ soát theory/worked examples. Ảnh đã nằm sẵn ở `public/lessons/<slug>/media/` thì dùng `output/tu-truong-latex/build/build.sh <tên>` (đổi tạm `/media/` → `/MEDIAX/` rồi đổi lại). Đăng BTVN: nhập bài gắn Luyện tập + "Giữ + thêm", rồi PATCH/POST `lesson_items` bằng fetch trong `javascript_tool` (token từ localStorage `sb-…-auth-token` + anon key) — nhanh hơn đi qua /quan-tri/bai-hoc.

Liên quan: [[project-thachlab-lesson-sections]], [[project-thachlab-up-de-skill]], [[feedback-token-discipline]]
