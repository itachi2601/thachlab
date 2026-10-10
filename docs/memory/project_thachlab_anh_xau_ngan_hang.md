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

## Bàn giao 2026-10-10 (phiên Mac, mọi thứ đã vào `main`: 6541ca90a, d578ccf02)
Phiên sau làm tiếp theo thứ tự, **không cần chạy lại kiểm kê** (rows.json đã có ở `scripts/data/kiem-ke-anh-ngan-hang/`, gitignore):
1. Hỏi thầy đã cho Gemini Spark chạy 20 câu thí điểm chưa (`scripts/data/gemini-hinh/out/` còn 0 file lúc bàn giao).
   Nếu rồi: `npx tsx scripts/nhan-hinh-tu-gemini.mts` → mở `so-sanh.html` → thầy duyệt → đọc `bao-cao.md` xem Gemini
   đọc đúng bao nhiêu phần, sai kiểu gì (pha sin, trục, vạch chia) → sửa PROMPT.md trước khi mở rộng.
2. Viết bước GHI DB (chưa có): nhận `quyet-dinh.json` (từ nút "Xuất quyết định" trên so-sanh.html) → câu "dung" gọi
   RPC `bank_set_question_figure(p_bank_id, p_img_html)` với SVG (RPC này tự chèn vào mọi `exams.questions` dùng câu đó,
   xem [[project_thachlab_missing_figures]]); câu "sua" xuất lại cho Gemini kèm ghi chú thầy. Phải sao lưu câu trước khi ghi
   (log `scripts/logs/`), chạy trên Mac qua tab terminal.
3. Mở rộng: 4 phương án ảnh đồ thị ("đồ thị nào đúng", 350 câu có ảnh ở phương án) → xuất mỗi ảnh một spec riêng,
   `xuat-hinh-cho-gemini.mts` hiện xuất `anh-1..n` nhưng schema chỉ nhận MỘT spec/câu → cần đổi `out/<id>.json` thành
   mảng theo ảnh. Thêm loại `parabola`, `step` vào `figure-spec.ts` nếu bao-cao cho thấy nhiều câu "khong_ve_duoc".
4. Mạch điện (72 câu): DSL riêng, chưa thiết kế.
5. Mô phỏng bài học: chưa bắt đầu; chờ thầy đưa ví dụ "mô phỏng không phù hợp" để lập checklist, rồi chọn 3 mẫu
   (chuyển động thẳng, dao động, mạch điện) làm component `next/dynamic` gắn qua `data-exp` (HTML trong DB cấm script).
Lưu ý kỹ thuật: mạng Mac → Supabase chậm (≈1 000 câu/phút, 1 ảnh/3 s) nên script nào tải ảnh phải chạy tab terminal và
giới hạn số ảnh; `question_bank` đọc toàn bộ cột `question` rất nặng, luôn lọc server bằng `question->>...imatch`.

## Kết quả 10–11/10/2026 (phiên Mac, thí điểm xong)
- Gemini đọc thông số (20 câu): 6 câu đã ghi bằng `scripts/ghi-hinh-sau-duyet.mts` (RPC `bank_set_question_figure_svc`, migration 20261011130000). 10 câu "vẽ lại" chưa làm (`gemini-hinh/can-ve-lai.md`: 523830, 674785 cần sửa tay/Gemini; còn lại dùng nền trắng). `figure-spec.ts` có thêm `parabola`, `kind:"multi"` (lưới A–D), nhãn đường luôn ở đầu mút phải.
- **Bài học chính: ảnh gốc đúng nội dung chỉ xấu nền → xử lý ảnh (`lam-trang-nen-anh.mts`/`nen-trang-theo-url.mts`, lib `lib-nen-trang.ts`, ghi đè tại chỗ trên Storage, URL không đổi) rẻ và đúng hơn bắt Gemini đọc lại.** Đã ghi 8 câu (28 ảnh) + 21 ảnh theo ghi chú; ảnh gốc ở `gemini-hinh/cau/` và `nen-trang-url/goc/` (gitignore).
- Ảnh công thức MathType (PNG nhỏ) → chữ LaTeX: `duyet-cong-thuc.html` (agent chep-de đọc contact sheet, thầy duyệt) → `thay-anh-cong-thuc.mts` (RPC `bank_replace_question_imgs`, migration 20261011140000). 91/96 câu đã thay; **#1246425 (trùng #684056) và #1254950 (trùng #1191945) chưa thay** vì sau thay thành câu y hệt — chờ thầy lưu trữ bản trùng. Sao lưu ở `scripts/logs/cong-thuc-sao-luu-*.json`.
- Kiểm kê cũ chỉ đo dung lượng/kích thước nên sót ảnh trống/chỉ còn khung trục; dùng `xem-anh-nghi-hong.mts` (ảnh < 1200 B, thầy ghi chú từng ảnh) thay vì tiêu chí độ lệch chuẩn. Thầy ghi "bỏ câu này" cho 25 câu — chưa lưu trữ (chờ thầy xác nhận).
- Kỹ thuật: tải ảnh nhỏ nhanh bằng `curl -P32`, node fetch rất chậm; chụp contact sheet cho agent phải đủ cao (cửa sổ 800 px cắt hàng cuối); mẫu prompt agent phải điền hết chỗ trống.
