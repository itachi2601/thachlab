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

## Ruột tập theo bài (`scripts/ruot-tap/`) — chuẩn chất lượng từ bài 14 VL12 (thầy chốt 25/10/2026)
Khác sách A4 cả chương: ruột tập là 12 trang 165×240 mm cho MỘT bài, đóng **lò xo**, dùng hai buổi theo nhịp L12. Bài sau
chép `bai14.mjs` + `bai14-btm.mjs` thành `baiNN.mjs`, giữ nguyên các quy ước sau (không hạ chuẩn):
- **Lề đóng lò xo**: gáy 20 mm, mép ngoài 10 mm, đổi bên theo trang chẵn/lẻ (`--pl/--pr` + `.page:nth-of-type(even)`);
  ô ly, chân trang, nhãn Tập đều bám `--pl/--pr`. Không còn ràng buộc "số trang chia hết cho 4".
- **Font Source Sans 3** (OFL, `scripts/ruot-tap/fonts/`, thầy chốt 25/10 để tiết kiệm trang: hẹp hơn Noto Sans ~10%, x-height cao)
  với **cỡ chữ 4 mức** (C3): `--fs-h1` 4,4 · `--fs-h3` 3,7 · `--fs-body` 3,3 (≈9,4 pt) · `--fs-sm` 2,95 mm (≈8,4 pt, sàn — C1);
  không đặt mm lẻ trong component; chỉ nạp 2 độ đậm (400/700). Thân chữ line-height 1,45; dòng kẻ viết tay giữ 5 mm.
- **Mỗi ý của câu hỏi một dòng** (a), b), c)… và A. B. C. D.), không nối bằng “ · ” để tiết kiệm chỗ — thầy chốt 25/10.
- **Không xoay ảnh** để vừa cột; ảnh dọc thì thu cột (≈30 mm) và đặt cạnh khối cao tương đương.
- **Không giải thích quy trình trên giấy** (thầy chốt 25/10: thầy tự điều phối): không ô nhịp buổi, không phụ đề "điền khi nghe
  giảng"/"làm cùng thầy", không hint trong ngoặc sau tiêu đề mục; chỉ giữ nhãn cho biết ghi gì. Không Ngày/Tên đầu trang (tờ đóng
  thành sách).
- **QR chỉ ở trang cuối, chỉ để xem lại bài** (thầy chốt 25/10 tối): không in tên web ở đầu/chân trang, không QR giữa tập, không
  câu giới thiệu/quảng cáo kiểu "mượn tập của bạn". Trang ghi chú cuối có một ô mảnh viền xám (`gioiThieu`): 2 QR nhỏ 22 mm
  (bài học này · trang chủ) + 1–2 dòng chữ phụ "Xem lại bài này trên thachlab.id.vn: quét mã…".
- **Hình minh hoạ bắt buộc** (thầy 25/10: trang không hình là thiếu): mỗi trang học/bài tập có ≥1 hình SVG tự vẽ trong
  `hinh.mjs`, mỗi hình trả lời một câu hỏi (H1), đặt CẠNH khối chữ bằng `.fig-side` (grid `1fr 40–46mm`) để không tốn
  chiều cao; hình ở ô giải dạng khó là gợi ý nhìn trước khi tính (để trống tỉ số/kết quả cho HS điền). Chữ trong SVG
  ≥ 20 đơn vị viewBox (≈3 mm khi in rộng 46 mm) — kiểm bằng `node scripts/ruot-tap/xem-hinh.mjs` trước khi dựng.
  Ảnh sách tham khảo: ruột tập lưu hành nội bộ nên thầy chốt 25/10 **được lấy hình từ Halliday "Fundamentals of Physics 12th"**
  (`/Users/MAC/Documents/THPT/số hoá THPT/Fundamentals of Physics 12th/`, 2 PDF) mà không xét giấy phép: `pdftotext` tìm
  "Figure NN.N.N" → số trang, `pdftoppm -r 200 -f N -l N` → cắt bằng PIL bỏ chữ Anh thừa, xoay nếu cần để hình nằm ngang,
  lưu `scripts/ruot-tap/anh/*.png` ≤150 KB, chèn bằng `hinh.anh(file, chú thích Việt dịch nhãn)`. Hình cao (dọc) tốn chỗ gấp
  đôi hình ngang — chọn hình ngang hoặc xoay; cột ảnh ≤ 24 mm chỉ còn đọc được nhờ chú thích.
  **Ảnh cắt từ sách và PDF chứa chúng chỉ giữ trên Mac, không đẩy lên GitHub** (`scripts/ruot-tap/anh/` và `out/*.pdf` đã
  gitignore từ 25/10) — có bản sao ở ngoài repo vì mất là phải cắt lại.
- **Trang sửa bài không có lưới đáp án**: đề làm trên web nên chỉ dòng "Câu sai P.I/P.II/P.III" + 5 ô Thầy chữa.
  Ghi chú tự do đúng 2 trang/bài; không ô "câu hỏi cho trợ giảng".
- Cân trang bằng dòng `trang N: dư X mm` script in ra (mục tiêu 0–15 mm, âm = tràn); đo từng khối bằng
  `getBoundingClientRect` trên `.pdf.html` khi không rõ khối nào phình, rồi mới nhìn ảnh.

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
- 2026-10-25 · Ruột tập bài 14: xếp bố cục theo bài web thay vì theo nhịp buổi của thầy (10′ ôn → 20′ KT → 30′ sửa → bài mới) và đoán "BTVN = phần web mang về" → thiếu ô đề BTVN, trang sửa bài ghi "trong 24 giờ". **Giấy dùng trên lớp phải hỏi nhịp buổi + BTVN là gì trước khi xếp trang**; quy ước đã ghi `docs/memory/project_thachlab_ruot_tap_bai14.md`.
- 2026-10-25 · Bảng sửa bài nhiều cột tick (chắc/đoán, 5 loại lỗi, dạng, ô Tập) là thiết kế cho người phân tích sau, HS trung bình không kịp điền khi thầy chữa → giấy điền TRONG giờ: lưới đáp án em–đúng để dò nhanh + ô chép rộng + ≤4 tick; tự hỏi "em có kịp điền không" trước khi thêm cột. Đề xuất bảng phân tích đề in sẵn cũng bị thầy bỏ (phân tích trong ô giải khi học) → chỗ trống rộng hơn khuôn in sẵn.
- 2026-10-25 · Số + đơn vị bị tách dòng ("14 / g") → đưa đơn vị vào KaTeX (`14\ \mathrm{g}`) hoặc bọc `.nw{white-space:nowrap}`; ô đáp số có thể là phân số thì cao ≥ 9 mm. Nhãn yêu cầu ghi gọn ("Phân tích và giải"), không ghi cách làm trong ngoặc.
- 2026-10-25 · Cân trang bằng chỉ số "dư … mm" script in ra, chỉ nhìn ảnh một lần cuối và cắt dải đầu trang bằng `pdftoppm -x -y -W -H`; đọc `.pdf.html` trung gian thay vì ảnh PDF khi cần nội dung. Trước khi sửa script ở worktree khác: `diff` với bản mình (bản kia mới hơn một commit font chưa vào main → cherry-pick).
- 2026-10-25 · Hình SVG vẽ với chữ 10–11 đơn vị viewBox (như hình trên web) in ra chỉ 1,5 mm, không đọc được; `figure` còn
  mang margin mặc định 40px của trình duyệt làm cột hình bị bóp → chữ trong SVG ≥ 20 đơn vị, `.fig{margin:0}`, và chụp
  từng hình ở cỡ in bằng `xem-hinh.mjs` trước khi ghép vào trang. Hình đặt cạnh khối chữ (`.fig-side`) thay vì xếp dưới:
  5 hình thêm vào mà tổng số trang không đổi.
- 2026-10-25 · Lưới đáp án em–đúng trên trang sửa bài là chép lại thứ web đã hiện → với đề làm trên web, chỉ ghi số câu
  sai; hỏi "đề làm ở đâu" trước khi vẽ bảng điền.

