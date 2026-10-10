---
name: project_thachlab_anh_xau_ngan_hang
description: "Vẽ lại ảnh xấu (đồ thị, mạch điện) trong ngân hàng câu hỏi — Gemini Spark đọc ảnh trả thông số qua thư mục, code vẽ SVG bằng figure-spec; thí điểm 20 câu đã xuất 10/10/2026, chờ thầy chạy Gemini"
metadata:
  node_type: memory
  type: project
  originSessionId: 5b77bacd-1fdf-4390-a91f-e394b3c235ab
  modified: 2026-10-10T13:57:13.942Z
---

**Quyết định thầy chốt 10/10/2026:** phạm vi toàn ngân hàng trừ `archived`; Gemini chỉ ĐỌC ảnh và trả THÔNG SỐ
(không vẽ, không trả SVG), code vẽ SVG bằng `services/figure-spec.ts` để kiểm được bằng đề bài. Gemini Spark trên
Mac đọc được thư mục → trao đổi qua `scripts/data/gemini-hinh/` (PROMPT.md + schema.json + `cau/<id>/`), không API.
Mô phỏng bài học: làm tương tác có nút phát như video (từ `content/thi-nghiem/`), không làm video; Gemini chỉ là
người đọc thứ hai theo checklist, kiểm số liệu bằng máy.

**Kiểm kê 10/10/2026** (`scripts/data/kiem-ke-anh-ngan-hang/summary.md`): 3 958 câu có ảnh / 5 261 ảnh; đồ thị +
mạch điện 922 câu, trong đó 736 câu ảnh rộng <500px (p50 = 282px), chỉ 38 câu ok. Ảnh <40px là glyph công thức
MathType, không phải hình (đã loại trong script).

**Quy trình:** `kiem-ke-anh-ngan-hang.mts` (≈40 phút, mạng Supabase chậm) → `xuat-hinh-cho-gemini.mts --n 20
--loai do_thi` → thầy cho Gemini Spark đọc thư mục, ghi `out/<id>.json` → `nhan-hinh-tu-gemini.mts` dựng
`so-sanh.html` (ảnh cũ | SVG mới, nút Dùng/Vẽ lại/Bỏ) → thầy duyệt → bước GHI DB **chưa viết** (dự kiến qua
RPC `bank_set_question_figure` có sẵn, hoặc cột `ai_figure` để duyệt trên trang ngân hàng).

**Còn chờ:** thầy chạy Gemini Spark cho 20 câu thí điểm; mở rộng schema (parabol, bậc thang, vectơ) và DSL mạch
điện sau khi xem kết quả; ví dụ "mô phỏng không phù hợp" của thầy để làm checklist.
Liên quan: [[project_thachlab_missing_figures]] (80 hình AI cũ chưa duyệt), [[project_thachlab_bai_ly_thuyet_tuong_tac]].
