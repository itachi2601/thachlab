---
name: project_thachlab_sach_in_chuong2
description: "Sách in A4 đen–trắng từ nội dung web (thử Chương 2 lớp 10, Động học) — pipeline book/, quyết định thiết kế thầy chốt, bài học kỹ thuật"
metadata:
  node_type: memory
  type: project
  originSessionId: 33d5b926-53a7-401c-b210-af5590043ba6
  modified: 2026-10-07T02:12:59.638Z
---

Thầy muốn biến nội dung web thành sách để dạy offline TRÊN LỚP kết hợp website (7/10/2026). Làm thử Chương 2 lớp 10 (bài 49–57 = Bài 4–12), A4 in đen–trắng.

**Pipeline** (thư mục `book/`, chưa commit lúc ghi): `build.py` (HTML web → HTML sách), `bw.py` (màu→nét, emoji→icon, đổi chữ nhắc màu), `front.py` (bìa/mục lục/bản đồ chương), `make.py` (render song song từng bài → đánh số trang → ghép PDF), `render.mjs` (puppeteer-core + Chrome + Paged.js + KaTeX + QR), `src/book.css`. Chạy: `cd book && python3 make.py` (~50 giây), ra `book/out/vat-li-10-chuong-2-dong-hoc.pdf`. Chọn HTML→PDF thay vì LaTeX vì nội dung đã là KaTeX + SVG.

**Thầy chốt thiết kế (feedback 7/10/2026, sau bản v1 321 trang):**
- Bản v1 quá dày (321 trang cho 1 chương) và cột ghi chú chấm dòng cả trang → HS sẽ bỏ trống. Chỉ đặt chỗ ghi ở NHỮNG CHỖ CẦN (dự đoán, số liệu thí nghiệm, trả bài, chỗ chưa hiểu, em giải bài mẫu).
- KHÔNG tô đen rồi để chữ trắng trong các khung (bìa, dải đầu bài, nhãn, tiêu đề…): dùng viền + nền xám nhạt, chữ đen.
- Dùng trên lớp phối hợp web: sách là giấy làm việc; mô phỏng/lời giải đầy đủ chiếu trên web (mã QR); lời giải mẫu dời về cuối bài.

**Bản v2 (7/10/2026, đã làm theo feedback):** 233 trang (v1: 321). Trắng hoàn toàn (nhãn = viền + nền xám nhạt, chữ đen), bỏ cột ghi chú → khung "Ghi chú" nét đứt chỉ ở: vì sao em chọn (Dự đoán), số liệu thí nghiệm, trả bài/tự hỏi, em giải bài mẫu, "chỗ em chưa hiểu" cuối lý thuyết. Lời giải bài tập mẫu dời về cuối bài; tự luyện chọn tối đa 2 bài mỗi mức (còn lại ghi "xem trên web"); mã QR cạnh hình có mô phỏng + ở đầu bài; hộp "Trên lớp / Ở nhà".

**Bản v3 (7/10/2026, thầy yêu cầu thêm):** chữ 10,7pt/dãn 1,72; công thức trọng tâm trong khung GHI NHỚ, công thức hiển thị và biểu thức có '=' ở mục II để TRỐNG (ô điền đánh số, đáp án ở trang cuối bài); bảng 'Phân tích đề' chỉ giữ cột 'Câu trong đề', cột dữ liệu/kiến thức để HS điền; BỎ phần tự luyện và lời giải khỏi sách (luyện tập, giải đề làm trên web, có khung QR cuối bài). Trang 'Đáp án & gợi ý' chỉ còn đáp án câu hỏi trong bài + ô điền. Thầy hỏi 'đáp án là gì, sao không thấy bài tập' → đáp án là của câu trắc nghiệm/tự hỏi chèn trong lý thuyết; luôn giải thích rõ tên trang này. 217 trang (bản v3).

**Bản v4 (7/10/2026):** chữ nhỏ lại, thang cỡ chỉ 5 mức (7,6 / 8,4 / 9,6 / 11,6 / 13,6pt; thân 9,6pt, dãn 1,5) — script chuẩn hoá cỡ trong cuối `book/src/book.css` (bản v3 lưu `book/out/book.css.v3.bak`); ẩn QR lặp dưới từng hình (còn QR đầu bài + khung web cuối bài). **189 trang** (v3: 217). Nên giữ: cỡ chữ không tản mạn, kiểm bằng thống kê cỡ chữ trong PDF (PyMuPDF).

**Bản v5 (7/10/2026, thầy yêu cầu tiết kiệm giấy):** 138 trang (v4: 189). Bỏ khung "chỗ em chưa hiểu", bỏ trang đệm/trang chẵn (lề đối xứng nên không cần), phần đầu sách còn 4 trang, hình SVG co theo tỉ lệ chữ (13 đơn vị = 8,4pt, `bw.gray_svg`), bảng "Phân tích đề" ô trống KHÔNG kẻ dòng, folio đúng số trang PDF (đặt `counter-reset` từng `.pagedjs_page` trong `book.js` theo `data-start`). **Đáp án & gợi ý chuyển lên web**: trang mới `app/(public)/sach/dap-an/page.tsx` (`/sach/dap-an/?bai=<lesson id>`, công khai, đã chặn robots), dữ liệu tĩnh `public/sach-data/dap-an-<id>.json` do `python3 build.py web` (hoặc `make.py`) sinh — gồm ô điền công thức, đáp án trắc nghiệm + phân tích, tự hỏi/trả bài, lời giải bài tập mẫu; số thứ tự trùng số in trong sách. Cuối mỗi bài có 2 mã QR (luyện tập/giải đề + đáp án). **CHƯA commit/deploy** các file web này — mã QR trong sách chỉ chạy sau khi deploy.

**Bài học kỹ thuật:**
- Đổi `①`, `✓`, `<`, chỉ số dưới unicode bằng regex làm vỡ KaTeX và SVG → tách token (svg / `$…$` / văn bản), xử lý riêng; trong math dùng `\textcircled`, `\checkmark`, `\lt`.
- Nguồn bài tập có `<` thô trong `$…$` (vd `$s_{2}<s_{1}$`) bị parser HTML nuốt → đổi `\lt` trước khi parse.
- Paged.js sập (`item doesn't belong to list`) với selector `a:first-of-type+p::first-letter` → gắn class thay vì dùng combinator `+`.
- SVG làm ảnh nền CSS không dùng được phông trang → chỉ vẽ hình học trong đó; chữ làm bằng HTML.
- Khối lồng nhau (bảng/thí nghiệm trong `details` trong khung) cần một lượt `final_pass` cuối, nếu không mất kiểu in.
- Màu→nét thống nhất cả cuốn: đỏ=nét đậm, cam=nét đứt, xanh lá=chấm gạch, xanh dương=xám; chữ nhắc màu viết lại bằng bảng luật trong `bw.py` (không đụng "đèn đỏ/đèn xanh"). Kiểm bằng cách grep chữ trong PDF.
- Kiểm tự động sau render: `.katex-error`, phần tử tràn khung, `$` sót trong text PDF.

**Còn treo:** chưa in thử giấy thật; câu trắc nghiệm ngân hàng chưa đưa vào sách; nhãn a), b) của phần tự luận do đoán; ảnh tự luận 34 MB chưa nén mạnh; 233 trang cho một chương vẫn dày — cân nhắc tách quyển hoặc bỏ tự luyện khỏi sách (để trên web); nhãn 'Nâng cao' của tự luyện chưa có sao.
