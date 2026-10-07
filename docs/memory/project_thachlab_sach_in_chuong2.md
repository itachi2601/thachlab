---
name: project_thachlab_sach_in_chuong2
description: "Sách in A4 đen–trắng từ nội dung web (Chương 2 lớp 10) — pipeline book/, bối cảnh DÙNG TRÊN LỚP đã chốt, v6 123 trang (ô lời giải, ⏱ 1′, vạch tiết, bảng đáp án thuần), bài học kỹ thuật"
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

**Bản v5 (7/10/2026, thầy yêu cầu tiết kiệm giấy):** 138 trang (v4: 189). Bỏ khung "chỗ em chưa hiểu", bỏ trang đệm/trang chẵn (lề đối xứng nên không cần), phần đầu sách còn 4 trang, hình SVG co theo tỉ lệ chữ (13 đơn vị = 8,4pt, `bw.gray_svg`), bảng "Phân tích đề" ô trống KHÔNG kẻ dòng, folio đúng số trang PDF (đặt `counter-reset` từng `.pagedjs_page` trong `book.js` theo `data-start`). **Đáp án & gợi ý chuyển lên web**: trang mới `app/(public)/sach/dap-an/page.tsx` (`/sach/dap-an/?bai=<lesson id>`, công khai, đã chặn robots), dữ liệu tĩnh `public/sach-data/dap-an-<id>.json` do `python3 build.py web` (hoặc `make.py`) sinh — gồm ô điền công thức, đáp án trắc nghiệm + phân tích, tự hỏi/trả bài, lời giải bài tập mẫu; số thứ tự trùng số in trong sách. Cuối mỗi bài có 2 mã QR (luyện tập/giải đề + đáp án). ĐÃ commit (`b936e560a`, `b57a76754` loại `book/` khỏi tsconfig) và deploy 2026-10-07 từ `.claude/worktrees/deploy-tree`; `/sach/dap-an/?bai=49` và `/sach-data/dap-an-49.json` trả 200. Dữ liệu đáp án để ở `public/sach-data/` (KHÔNG để `public/data/` — bị gitignore nên không lên bản deploy).

**Bài học kỹ thuật:**
- Đổi `①`, `✓`, `<`, chỉ số dưới unicode bằng regex làm vỡ KaTeX và SVG → tách token (svg / `$…$` / văn bản), xử lý riêng; trong math dùng `\textcircled`, `\checkmark`, `\lt`.
- Nguồn bài tập có `<` thô trong `$…$` (vd `$s_{2}<s_{1}$`) bị parser HTML nuốt → đổi `\lt` trước khi parse.
- Paged.js sập (`item doesn't belong to list`) với selector `a:first-of-type+p::first-letter` → gắn class thay vì dùng combinator `+`.
- SVG làm ảnh nền CSS không dùng được phông trang → chỉ vẽ hình học trong đó; chữ làm bằng HTML.
- Khối lồng nhau (bảng/thí nghiệm trong `details` trong khung) cần một lượt `final_pass` cuối, nếu không mất kiểu in.
- Màu→nét thống nhất cả cuốn: đỏ=nét đậm, cam=nét đứt, xanh lá=chấm gạch, xanh dương=xám; chữ nhắc màu viết lại bằng bảng luật trong `bw.py` (không đụng "đèn đỏ/đèn xanh"). Kiểm bằng cách grep chữ trong PDF.
- Kiểm tự động sau render: `.katex-error`, phần tử tràn khung, `$` sót trong text PDF.

**BỐI CẢNH DÙNG ĐÃ CHỐT (7/10/2026, sau v5):** sách dùng TRÊN LỚP OFFLINE — thầy giảng lý thuyết, chỉ HS điền ô công thức, hướng dẫn giải bài tập mẫu trên bảng, mô phỏng thầy chiếu. Phần Ở NHÀ (luyện tập, giải đề, đáp án phân tích) mới dùng web. Mọi quyết định thiết kế xét theo bối cảnh này, KHÔNG xét theo tự học.

**Phản biện v5 theo nghiên cứu (guided notes Konrad 2009, generation effect, split-attention, negative testing effect) — 4 điểm, đã sửa ở v6:**
1. Bài tập mẫu 37 Dạng không thể giảng hết (≈4 Dạng/bài) → v6: chỉ Dạng CHUNG NHẤT có ô lời giải; còn lại thành "Luyện thêm" chỉ đề. ✔
2. Ô trống chỉ có tác dụng khi HS thử TRƯỚC khi thầy công bố → v6: trang Cách dùng thêm nhịp "thầy đọc đề → em tự điền 1 phút → thầy chữa → sửa bút khác màu"; biểu tượng ⏱ 1′ cố định ở góc mọi khung có ô điền. ✔
3. Hộp Trên lớp/Ở nhà giống hệt nhau ở 9 bài, vô dụng → v6: thay bằng vạch lề "▌hết tiết n" theo `book/src/tiet.json`. ✔
4. 56 CÂU + 10 DỰ ĐOÁN không có đáp án trong sách; câu thầy không kịp chữa sẽ không bao giờ được chữa nếu HS không quét QR (negative testing effect) → v6: bảng đáp án THUẦN 2 trang cuối sách. ✔

**Bản v6 (7/10/2026): 123 trang (v5: 138).** Làm trong `build.py`/`front.py`/`bw.py`/`make.py`/`book.css`, không sửa tay HTML:
- `book/src/dang-chung.json` {lesson_id: [chỉ số Dạng]} — Dạng chung nhất được giảng (MẶC ĐỊNH [1, 2] vì chưa có số liệu đề kiểm tra, chờ thầy chỉnh). 7 bài có bài tập mẫu (49, 50, 52, 53, 54, 55, 57; bài thực hành 51/56 không có) → 14 ô "LỜI GIẢI — GHI CÙNG THẦY CÔ" (cao 84 mm ≈ 1/3 trang, nét đứt, không kẻ dòng, `.solbox`). Mục tiêu đề bài 18 = 2×9 không đạt được vì 2 bài thực hành không có Dạng.
- "LUYỆN THÊM — BÀI TƯƠNG TỰ" (`render_luyen_them`): 23 Dạng còn lại + 24 thử thách phân tầng (dời từ mục VI lý thuyết xuống, giữ ★); chỉ đề, bỏ bảng phân tích, bỏ mô phỏng (giữ hình thu nhỏ nếu đề nhắc "đồ thị/hình" vì không có hình thì không làm được), không ô lời giải. Dòng "tương tự Dạng n" = Dạng chung có cùng `topic` (YCCĐ); không trùng topic thì ghi "dạng riêng · lời giải trên web" (không bịa). Giữ số Dạng gốc để khớp web và bảng đáp án.
- ⏱ 1′ (`build.timer()`, icon clock của `bw.ICONS`, class `.t1`): GHI NHỚ có ô điền, Phân tích đề, ô Lời giải (cả gnote "Bài toán mẫu" trong lý thuyết), Số liệu thí nghiệm. `bw.to_print` bỏ qua `<svg class="ic"` để không ép cỡ icon.
- Vạch chia tiết `book/src/tiet.json` {lesson_id: [anchor]}; anchor `muc:<La Mã>` (hết mục đó), `dang:<k>`, `bai-tap-mau`. MẶC ĐỊNH tiết 1 hết mục II, tiết 2 hết Bài tập mẫu (bài thực hành: hết mục V) — chờ thầy chỉnh. Bỏ hộp `.use-row`.
- Trang 2 Cách dùng: bước 2 = nhịp tự điền trước; bước 3 = ở nhà mở đáp án; legend thêm "Ô lời giải" và "Vạch chia tiết".
- Bảng đáp án thuần (`front.answer_table`, trang 122–123 = đúng 2 trang): công thức ô điền (số nhỏ + KaTeX), CÂU/DỰ ĐOÁN chỉ chữ cái, Luyện thêm đáp số theo Dạng (D3…), Thử thách đáp số theo số câu. Sinh từ cùng dict mà `export_web` ghi ra `public/sach-data/dap-an-<id>.json` (thêm field `answer`, `inClass`, `similarTo`, `num`, `name`) nên không lệch số. Trả bài/Tự hỏi/Điền bước vẫn chỉ trên web (đáp án tự luận, không "thuần").
- 9 trang gần trống chỉ có 2 QR: nguyên nhân thật là `.websec` (và `.ltsec`) nằm NGOÀI section có `page:lesson` → Paged.js coi là trang tên khác, bắt buộc sang trang mới và mất cả đầu trang/folio. Sửa: `.ltsec,.websec{page:lesson}` + QR gọn 17 mm. Kết quả 0 trang <60 từ.
- Folio phần cuối (tổng kết, tự đánh giá, đáp án) giờ nối tiếp số trang bài (trước là 1, 2…).
- Kiểm tự động sau render: KaTeX lỗi 0, tràn khung 0, `$` sót 0, trang <60 từ 0, cỡ chữ vẫn 5 mức (9,6/8,4/7,6/11,6/13,6; lẻ chỉ KaTeX + nhãn 7pt bảng đáp án), không Dạng nào in 2 lần.

**Còn treo (2026-10-07, sau v6):** chưa in thử giấy thật (cỡ 9,6pt thân / 8,4pt trong hình; ô lời giải 84 mm đủ cho một bài không?); thầy chốt `book/src/dang-chung.json` (Dạng chung nhất mỗi bài, đang mặc định 1–2) và `book/src/tiet.json` (vị trí chia tiết, đang mặc định); `public/sach-data/*.json` bản v6 (thêm field answer/inClass/similarTo) CHƯA commit/deploy — bản đang chạy trên web là v5, số thứ tự giống nhau nên QR vẫn đúng đáp án, chỉ thiếu nhãn "Luyện thêm"; trang `/sach/dap-an` chưa hiện "Dạng chung / Luyện thêm"; đổi nội dung bài trên web thì chạy lại `cd book && python3 make.py` rồi commit + deploy json; câu trắc nghiệm ngân hàng chưa đưa vào sách; nhân sang chương khác cần sửa `CHAPTER` trong `book/build.py` + tên ga trong `book/front.py`. Skill: `.claude/skills/sach-in-tu-web/SKILL.md` (nguồn duy nhất).
