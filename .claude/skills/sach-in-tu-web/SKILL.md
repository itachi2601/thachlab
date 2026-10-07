---
name: sach-in-tu-web
description: Dựng SÁCH IN A4 đen–trắng (PDF) từ nội dung đã đăng trên thachlab (bài lý thuyết tương tác + bài tập mẫu) bằng pipeline `book/` (HTML → Paged.js → Chrome → PDF, KaTeX + SVG + QR), kèm bảng đáp án thuần cuối sách và dữ liệu đáp án cho trang web /sach/dap-an. Dùng khi thầy nói "in sách chương X", "làm bản in cho lớp", "dựng lại sách sau khi sửa bài", "đổi Dạng được giảng trên lớp", "chia tiết trong sách", "thêm chương vào sách in". Sách dùng TRÊN LỚP có thầy (không phải tự học) — hỏi bối cảnh dùng trước khi bỏ/thêm lời giải, đáp án. Chạy được trên Mac (cần Chrome + node_modules trong book/); không ghi DB.
---

# Sách in từ web — pipeline `book/`

## Bối cảnh dùng (thầy chốt 7/10/2026) — đọc trước khi quyết định bất cứ gì
Sách dùng **TRÊN LỚP OFFLINE, có thầy**: thầy giảng lý thuyết, chỉ học sinh điền ô công thức, hướng dẫn
giải bài tập mẫu trên bảng; mô phỏng thầy chiếu trên web. Phần **Ở NHÀ** (luyện tập, giải đề, đáp án có
phân tích) mới dùng web qua mã QR cuối bài. Mọi quyết định thiết kế xét theo bối cảnh này:
- Có chỗ GHI ở đúng nơi thầy chữa (ô lời giải Dạng chung, bảng phân tích đề, số liệu thí nghiệm, ô công thức).
- Không in lời giải đầy đủ / tự luyện (đã ở web), nhưng **phải có đáp án thuần** trong sách cho câu thầy không kịp chữa.
- Không nền đen chữ trắng, không cột ghi chú cả trang, cỡ chữ 5 mức (7,6 / 8,4 / 9,6 / 11,6 / 13,6 pt).

## Chạy
```bash
cd book && python3 make.py            # cả chương, ~30–60 s → out/vat-li-10-chuong-2-dong-hoc.pdf + public/sach-data/dap-an-<id>.json
cd book && python3 make.py 49 50      # thử vài bài
cd book && python3 build.py lesson 49 5 && node render.mjs src/lesson-49.html out/_t.pdf   # một bài, xem nhanh
```
Lệnh > 30 s chạy trong tab terminal (`run_in_terminal`) để thầy theo dõi; `build.py`/`render.mjs` một bài thì `Bash` được.

## Cấu hình thầy chỉnh (JSON trong `book/src/`, không sửa tay HTML)
- `dang-chung.json` `{lesson_id: [chỉ số Dạng]}` — Dạng CHUNG NHẤT được giảng trên lớp (có ô "Lời giải — ghi cùng thầy cô").
  Mặc định `[1, 2]`; các Dạng còn lại + thử thách phân tầng tự thành mục "Luyện thêm — bài tương tự" (chỉ đề).
- `tiet.json` `{lesson_id: [anchor]}` — vạch lề "hết tiết n". Anchor: `muc:II` (hết mục II lý thuyết), `dang:2`, `bai-tap-mau`.
  Mặc định tiết 1 hết mục II, tiết 2 hết Bài tập mẫu (bài thực hành: hết mục V).
- Mục lục (`front.toc_full`) sinh tự động, một trang riêng, đủ phần đầu + mục con từng bài + phần cuối; số trang mục con
  đọc từ PDF con đã dựng bằng `make.page_of`. Phần đầu sách cố định `FRONT_PAGES` trang — `make.py` tự dừng nếu lệch.
- Thêm chương: sửa `CHAPTER` trong `build.py` + tên ga/tổng kết/tự đánh giá trong `front.py` (đang viết riêng cho chương 2 lớp 10).

## Kiểm sau mỗi lần dựng (bắt buộc, trước khi đưa thầy xem)
1. `render.mjs` tự in `CHẨN ĐOÁN` nếu có `.katex-error`, phần tử tràn khung, trang còn `$` — phải trống.
2. PyMuPDF: đếm trang; trang < 60 từ phải ≈ 0; thống kê cỡ chữ (chỉ 5 mức + lẻ của KaTeX); không Dạng nào in 2 lần
   (Paged.js có thể nhân đôi nội dung mà không báo lỗi — xem nhật ký).
3. Rasterize 3–4 trang mẫu ở 60 dpi để tự xem, 100 dpi để gửi thầy (`pdftoppm -f N -l N -r 100 -png`).
4. Có sửa `export_web` → so số thứ tự trong `public/sach-data/*.json` với số in trong sách (cùng dict, không được lệch).
5. Đối chiếu MỤC LỤC với trang thật: mỗi số trang trong mục lục (phần đầu, Lý thuyết/Bài tập mẫu/Luyện thêm từng bài,
   Tổng kết, Tự đánh giá, Bảng đáp án) phải trỏ tới trang có đúng tiêu đề đó (so chuỗi đã bỏ khoảng trắng). Số 0 hoặc
   trống = tìm không ra, không được giao.

## Cuối phiên
- Ghi memory `docs/memory/project_thachlab_sach_in_chuong2.md` (bản vN làm gì, số trang, còn treo).
- Commit `book/` (code + `src/*.json`; HTML/PDF sinh ra đã gitignore). `public/sach-data` + `app/(public)/sach/dap-an`
  chỉ commit/deploy khi đã kiểm trang web thật; chưa thì ghi "ĐANG CHỜ" trong `docs/STATE.md`.
- Rút kinh nghiệm vào mục dưới.

## Nhật ký rút kinh nghiệm
- 2026-10-07 · Đổi `①`, `✓`, `<`, chỉ số dưới unicode bằng regex trên cả chuỗi làm vỡ KaTeX và SVG → tách token (svg / `$…$` / văn bản) rồi xử lý riêng (`bw.to_print`); trong math dùng `\boxed`, `\checkmark`, `\lt`/`\gt`.
- 2026-10-07 · Paged.js sập (`item doesn't belong to list`) với selector có combinator `+` (`a:first-of-type+p::first-letter`) → gắn class rồi chọn theo class; tránh `+` trong `book.css`.
- 2026-10-07 · SVG làm ảnh nền CSS không dùng được phông của trang → chỉ vẽ hình học trong SVG nền; chữ làm bằng HTML.
- 2026-10-07 · Khối lồng nhau (bảng/thí nghiệm trong `details` trong khung) bị bỏ sót kiểu in → luôn chạy `final_pass` lặp tới khi hết `.tl-box`/`details`.
- 2026-10-07 · Màu web → nét in phải là một bảng luật duy nhất (đỏ=đậm, cam=đứt, xanh lá=chấm gạch, xanh dương=xám) áp cho cả SVG lẫn chữ nhắc màu (`bw.TEXT_RULES`, chừa "đèn đỏ/đèn xanh"); kiểm bằng grep chữ trong PDF.
- 2026-10-07 · **Thiết kế sách phải hỏi BỐI CẢNH DÙNG (trên lớp có thầy / tự học) trước khi quyết định bỏ lời giải hay bỏ đáp án** — v3 bỏ lời giải khỏi sách là đúng cho trên lớp nhưng quên chừa chỗ ghi; v5 bỏ đáp án lên web thì câu thầy không kịp chữa không bao giờ được chữa (negative testing effect) → v6 thêm ô lời giải Dạng chung + bảng đáp án thuần.
- 2026-10-07 · Trang gần trống chỉ có 2 mã QR không phải do QR to: khối nằm NGOÀI section có `page:lesson` bị Paged.js coi là trang tên khác → bắt buộc sang trang mới, mất cả đầu trang/folio. Mọi khối cuối bài phải có `page:lesson`.
- 2026-10-07 · Phần tử cao 0 có `break-after:avoid` (vạch chia tiết) ở biên trang làm Paged.js dàn lại: **nội dung in 2 lần + 1 trang trống, không báo lỗi** → không dùng `break-after:avoid` trên vạch/marker; thêm bước kiểm "Dạng nào in 2 lần" sau render.
- 2026-10-07 · Icon SVG chèn bằng Python trước `bw.to_print` bị `gray_svg` ép `style="width:…mm"` và chèn pattern → `to_print` bỏ qua `<svg class="ic"`.
- 2026-10-07 · Thầy báo "thiếu mục lục" dù mục lục có: 9 dòng tên bài nép dưới "Cách đọc hình" nửa trang, không có phần đầu/cuối, không có mục con → mục lục phải là **một trang riêng, đủ ba phần** (phần đầu, từng bài kèm Lý thuyết · Bài tập mẫu · Luyện thêm, phần cuối). Thứ người dùng không nhìn thấy ngay coi như không có.
- 2026-10-07 · Số trang mục con/phần cuối lấy bằng cách tìm chữ trong PDF con: chữ có `letter-spacing` (nhãn `.pg-k`, `.sb-k`) bị PyMuPDF trích thành "T Ổ N G  K Ế T" → tìm không ra, mục lục in số 0 → **so chuỗi đã bỏ hết khoảng trắng** (`re.sub(r'\s+','',…)` cả hai vế); kiểm tự động phải báo lỗi khi mục lục có số 0.
- 2026-10-07 · Trang nào cần số trang của trang khác (mục lục ↔ phần cuối) thì dựng theo thứ tự: bài → phần cuối → phần đầu; `make.py` giữ `FRONT_PAGES` cố định và tự kiểm số trang phần đầu sau render, lệch thì dừng chứ không ghép PDF sai số.
- 2026-10-07 · Mỗi lần thêm/bớt trang ở phần đầu phải xem lại ảnh trang mẫu gửi thầy: gửi đủ trang Cách dùng, mục lục, một trang Dạng, một trang vạch tiết, trang đáp án — thầy chỉ nhìn ảnh, không mở PDF.
