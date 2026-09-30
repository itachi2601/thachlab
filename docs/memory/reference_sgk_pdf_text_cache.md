---
name: reference-sgk-pdf-text-cache
description: "File SGK PDF của thầy chỉ là ảnh scan (không có lớp text) — mỗi lần đọc xong một bài, chép lại thành .md cạnh file PDF để phiên sau không phải đọc lại ảnh"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 318917b3-f9ac-44db-85fc-d9039816c797
  modified: 2026-09-23T07:38:00.403Z
---

Các file SGK trong `/Users/MAC/Documents/THPT/` (Lớp 10/11/12, Cánh diều/Kết nối tri
thức) là **PDF scan thuần ảnh** — đã kiểm bằng PyMuPDF (`page.get_text()` trả về rỗng ở
mọi trang, mỗi trang chỉ có 1 ảnh raster). `pdftotext`/`pdfplumber` vô dụng với các file
này; cách duy nhất đọc được là công cụ Read với `pages="a-b"` (tốn token ảnh, đắt).

**Quy ước cache:** mỗi khi đã đọc xong nội dung một Bài từ ảnh PDF (để soạn lý thuyết,
đối chiếu, v.v.), chép lại thành 1 file `.md` trong thư mục
`<tên-file-pdf-không-đuôi>-text/` nằm CẠNH file PDF gốc (không phải trong repo thachlab —
để dùng chung được cho mọi phiên làm việc với sách đó, không riêng gì thachlab). Tên file
`baiNN-slug-khong-dau.md`. Nội dung: chép lại nguyên văn từng mục theo cấu trúc SGK
(mở bài, mục La Mã/số, câu hỏi hộp bên, "Em đã học"/"Em có thể"), mô tả bằng lời phần
hình vẽ (không vẽ lại), giữ công thức dạng LaTeX `$...$`, ghi rõ số trang sách + số trang
PDF vật lý ở đầu file.

Ví dụ đã có: `SGK_va_sach_tham_khao/sách gk/SGK-Vat-Li-11-KNTT-text/bai01-dao-dong-dieu-hoa.md`
(Lớp 11, Bài 1 — Dao động điều hoà, chép 23/9/2026).

**Why:** thầy hỏi thẳng "làm sao lưu nội dung đã đọc trong sách" vì phiên đọc ảnh PDF dài
tốn nhiều token, muốn tránh đọc lại ảnh ở phiên sau cho cùng một bài.

**How to apply:**
- Trước khi gọi Read với `pages=` trên một SGK PDF: tìm thử `<tên-pdf>-text/baiNN-*.md`
  cạnh file PDF trước — có rồi thì đọc file .md đó (rẻ), không cần mở lại ảnh.
- Sau khi đọc ảnh một Bài mới xong (vì chưa có cache): trước khi dùng nội dung, viết
  transcript ra file .md theo quy ước trên — không chỉ dùng xong rồi bỏ.
- Vì mỗi trang PDF ứng với 1 ảnh, số trang PDF thường lệch số trang in trong sách (có bìa
  + lời nói đầu + mục lục ở đầu) — luôn ghi rõ cả hai số trang trong file .md để đối
  chiếu lại nếu cần xem ảnh gốc (ví dụ hình vẽ chi tiết).
- Việc này áp dụng cho MỌI sách SGK dạng scan thầy dùng (không riêng Lớp 11 Vật lí), làm
  dần theo yêu cầu thực tế, không cần transcribe trước cả cuốn.

Liên quan: [[feedback_token_discipline]] (ảnh không nên nằm lại trong context chính).
