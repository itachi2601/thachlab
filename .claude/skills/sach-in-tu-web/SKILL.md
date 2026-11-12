---
name: sach-in-tu-web
description: Dựng SÁCH IN A4 đen–trắng (PDF) từ bài lý thuyết + bài tập mẫu đã đăng bằng pipeline book/ (Paged.js → Chrome), kèm bảng đáp án và dữ liệu /sach/dap-an. Dùng khi thầy nói "in sách chương X", "làm bản in cho lớp", "dựng lại sách", "chia tiết trong sách". Sách dùng trên lớp có thầy — hỏi bối cảnh trước khi bỏ/thêm lời giải. Chạy trên Mac.
---

# Sách in từ web — pipeline `book/`

## Bối cảnh dùng (thầy chốt 7/10/2026) — đọc trước khi quyết định bất cứ gì
Sách dùng **TRÊN LỚP OFFLINE, có thầy**: thầy giảng lý thuyết, chỉ học sinh điền ô công thức, hướng dẫn
giải bài tập mẫu trên bảng; mô phỏng thầy chiếu trên web. Phần **Ở NHÀ** (luyện tập, giải đề, đáp án có
phân tích) mới dùng web qua mã QR cuối bài. Mọi quyết định thiết kế xét theo bối cảnh này:
- Có chỗ GHI ở đúng nơi thầy chữa (ô lời giải Dạng chung, bảng phân tích đề, số liệu thí nghiệm, ô công thức).
- Không in lời giải đầy đủ / tự luyện (đã ở web), nhưng **phải có đáp án thuần** trong sách cho câu thầy không kịp chữa.
- Không nền đen chữ trắng, không cột ghi chú cả trang, cỡ chữ 5 mức (7,6 / 8,4 / 9,6 / 11,6 / 13,6 pt).

## Chạy — luôn soát lệch với web trước, rồi mới dựng
Mỗi cuốn một **hồ sơ** `book/sach/<mã>.json`; nội dung lấy từ **web thật (DB, chỉ đọc)** về `book/cache/`, không đọc file nháp trong repo.
Dùng `/usr/bin/python3` (có bs4, PyMuPDF, PIL; `python3` của Homebrew thiếu). Worktree mới chưa có `book/node_modules` →
`ln -sfn /Users/MAC/Projects/thachlab/book/node_modules book/node_modules`.
```bash
cd book && /usr/bin/python3 sach.py list                      # các cuốn + bản đang có
cd book && /usr/bin/python3 sach.py lech l10-ch2-dong-hoc     # tải web → so với sổ khoá (cần mạng: tab terminal)
cd book && /usr/bin/python3 make.py l10-ch2-dong-hoc          # cả cuốn ~1–2 phút → out/<tep>.pdf + sổ khoá + public/sach-data
cd book && /usr/bin/python3 make.py l10-ch2-dong-hoc 49 50    # thử vài bài → out/<tep>-thu.pdf (không ghi sổ khoá)
```
- `sach.py lech` báo từng bài: **khớp** (không làm gì) · **chữ** (nội dung đổi, số ô điền/câu/Dạng giữ nguyên → dựng lại, sách đã
  phát vẫn dùng được) · **đánh số** (bộ đếm đổi → dựng lại sẽ tăng số bản, sách đã phát lệch số với đáp án mới) · **mới**.
  Khớp hết thì DỪNG, không dựng lại. Dòng "repo có bản bài tập mẫu KHÁC bản đã đăng" = có nháp chưa đăng; sách vẫn theo web.
- **Sổ khoá** `book/sach/<mã>.lock.json` (commit vào git) do `make.py` ghi sau khi dựng trọn cuốn: số bản, ngày, dấu vân tay
  lý thuyết + bài tập mẫu từng bài, bộ đếm, trang bắt đầu. Không sửa tay.
- Cuốn mới: `npx tsx book/lay-noi-dung.mts --moi <mã> <lớp> <lesson_id bất kỳ trong chương>` → hồ sơ nháp + cache; thầy sửa chữ.
- Lệnh > 30 s hoặc cần mạng chạy trong tab terminal (`run_in_terminal`); `build.py lesson`/`render.mjs` một bài thì `Bash` được
  (`BOOK_SACH=<mã>` chọn cuốn cho `build.py`).

## Hồ sơ sách thầy chỉnh (`book/sach/<mã>.json`, không sửa tay HTML/Python)
- Bắt buộc: `lop`, `chuong`, `ten`, `lessons` (id bài theo thứ tự). `tep` = tên file PDF. `bia` = chữ trên bìa.
- `dang_chung` `{lesson_id: [chỉ số Dạng]}` — Dạng CHUNG NHẤT được giảng trên lớp (có ô "Lời giải — ghi cùng thầy cô").
  Mặc định `[1, 2]`; các Dạng còn lại + thử thách phân tầng tự thành mục "Luyện thêm — bài tương tự" (chỉ đề).
- `tiet` `{lesson_id: [anchor]}` — vạch lề "hết tiết n". Anchor: `muc:II` (hết mục II lý thuyết), `dang:2`, `bai-tap-mau`.
  Mặc định tiết 1 hết mục II, tiết 2 hết Bài tập mẫu (bài không có bài tập mẫu: hết mục V).
- `ban_do_chuong.ga` (tên ga ngắn, thiếu thì lấy tên bài), `ban_do_chuong.nhom`, `tu_danh_gia` (thiếu thì bỏ trang Tự đánh giá).
- Mục lục (`front.toc_full`) sinh tự động, một trang riêng, đủ phần đầu + mục con từng bài + phần cuối; số trang mục con
  đọc từ PDF con đã dựng bằng `make.page_of`. Phần đầu sách cố định `FRONT_PAGES` trang — `make.py` tự dừng nếu lệch.
- `anh_that` `{lesson_id: [{sau, tep, chu, nguon}]}` — ảnh THỰC TẾ chèn ngay sau phần tử đầu tiên có chữ chứa `sau`
  (nên neo vào tiêu đề h3/h4). File ở `book/assets/anh-that/` (xám, rộng ≤1200px, ≤150 KB); in ảnh trái 72 mm, chú thích phải.
  Ưu tiên ảnh thật trên web; thiếu thì cắt từ Halliday *Fundamentals of Physics 12th* (`/Users/MAC/Documents/THPT/số hoá THPT/…`,
  lưu hành nội bộ, thầy chốt 11/11/2026 bỏ qua bản quyền) hoặc Wikimedia Commons (`book/tim_anh_wikimedia.py`, ghi
  tác giả + giấy phép trong `nguon`). Đặt ảnh ngay dưới đoạn đầu mục "Mở bài" (neo = vài chữ đầu đoạn) — ảnh là móc vào bài. Neo không khớp → `build.py` in `! ảnh thực tế … không thấy chỗ neo`.
- **Hình mô phỏng** (`figure[data-exp|data-bt]`) KHÔNG in thành hình (thầy chốt 11/11/2026: in ra chỉ là khung tĩnh to,
  vô ích) → `sim_line` thu thành 1 dòng `▶ Hình N · mô phỏng trên web · chú thích`, giữ số hình. Trừ chú thích có
  đồ thị/điểm đo/số liệu/tỉ lệ xích (`KEEP_SIM_RE`) và đề bài đọc đồ thị/"như hình" (`GRAPH_RE`).
- Còn chờ làm (thiết kế `docs/THIET-KE-SKILL-SACH-DONG-BO.md` chặng C–E): số bản trong QR, web → "Sách tr. X", bản Word.

## Kiểm sau mỗi lần dựng (bắt buộc, trước khi đưa thầy xem)
0. `make.py` in `! CẢNH BÁO` (trang < 60 từ, bài thiếu hộp "Mang về") → xử lý hết hoặc ghi rõ khi giao.
1. `render.mjs` tự in `CHẨN ĐOÁN` nếu có `.katex-error`, phần tử tràn khung, trang còn `$` — phải trống.
2. PyMuPDF: đếm trang; trang < 60 từ phải ≈ 0; thống kê cỡ chữ (chỉ 5 mức + lẻ của KaTeX); không Dạng nào in 2 lần
   (Paged.js có thể nhân đôi nội dung mà không báo lỗi — xem nhật ký).
2b. `/usr/bin/python3 book/do_trong.py out/<tep>.pdf 50` — trang có khoảng trống cuối ≥50 mm. Trống do hết bài là bình
   thường; trống vì hình/khung to không vừa trang thì thu hình hoặc bỏ hình mô phỏng, báo tổng cm trống trước/sau.
3. Rasterize 3–4 trang mẫu ở 60 dpi để tự xem, 100 dpi để gửi thầy (`pdftoppm -f N -l N -r 100 -png`).
4. Có sửa `export_web` → so số thứ tự trong `public/sach-data/*.json` với số in trong sách (cùng dict, không được lệch).
5. Đối chiếu MỤC LỤC với trang thật: mỗi số trang trong mục lục (phần đầu, Lý thuyết/Bài tập mẫu/Luyện thêm từng bài,
   Tổng kết, Tự đánh giá, Bảng đáp án) phải trỏ tới trang có đúng tiêu đề đó (so chuỗi đã bỏ khoảng trắng). Số 0 hoặc
   trống = tìm không ra, không được giao.
6. Lấp đáy trang: đếm trang có "GHI CHÉP" (ô ca-rô `book.js`) + `do_trong.py`; trống ≥80 mm mà không có ô Ghi chép là lỗi.
7. **Học sinh thử trước khi in (bắt buộc, thầy duyệt 12/11/2026)** — 3 agent `kiem-code` chia bài, mỗi agent một thư mục
   ảnh riêng (`<scratchpad>/hs-thu-<n>/`, không chung tên file), đóng vai HS 15–16 tuổi: tự làm câu, ô điền, bài mẫu,
   Luyện thêm rồi đối chiếu bảng đáp án + `public/sach-data/dap-an-<id>.json`. Báo theo 5 nhóm: hình thiếu mà đề trỏ
   tới · đáp án lộ trước khi HS thử (Nhận xét, lời giải Thử thách, công thức cạnh ô điền, gợi ý trên câu hỏi) · ô viết
   không vừa · khung/tiêu đề bị cắt · chữ chỉ-web ("Bấm…", mã H2/H3, "Cam/Xanh"). Lần đầu đọc ảnh mọi trang; **lần sau
   chỉ đọc ảnh trang đã đổi** (so text từng trang với bản trước), phần còn lại dùng chữ trích — lần đầu tốn ~425k token.
8. QR đáp án phải sống TRƯỚC khi in: `curl -s -o /dev/null -w '%{http_code}' https://thachlab.id.vn/sach-data/dap-an-<id>.json`
   = 200 cho mọi bài. Số trang/đáp án đổi theo mỗi lần dựng → kiểm lại sau lần dựng cuối.

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
  câu giới thiệu/quảng cáo kiểu "mượn tập của bạn". Ô cuối trang cuối (`gioiThieu`, mảnh viền xám) có **MỘT mã QR 34 mm = đúng bài học này** + 1 dòng "Xem lại bài N trên
  thachlab.id.vn: quét mã bên…". **Không QR Trang chủ** (thầy chốt 10/11: hai mã cạnh nhau, máy quét dễ trúng nhầm mã cần dùng). Kiểm QR
  bằng `pdftoppm -r 300 -f 12 -l 12` + `npx tsx scripts/ruot-tap/giai-ma-qr.mts`.
- **Hình minh hoạ bắt buộc** (thầy 25/10: trang không hình là thiếu): mỗi trang học/bài tập có ≥1 hình SVG tự vẽ trong
  `hinh.mjs`, mỗi hình trả lời một câu hỏi (H1), đặt CẠNH khối chữ bằng `.fig-side` (grid `1fr 40–46mm`) để không tốn
  chiều cao; hình ở ô giải dạng khó là gợi ý nhìn trước khi tính (để trống tỉ số/kết quả cho HS điền). Chữ trong SVG
  ≥ 20 đơn vị viewBox (≈3 mm khi in rộng 46 mm) — kiểm bằng `node scripts/ruot-tap/xem-hinh.mjs` trước khi dựng.
  Ảnh sách tham khảo: ruột tập lưu hành nội bộ nên thầy chốt 25/10 **được lấy hình từ Halliday "Fundamentals of Physics 12th"**
  (`/Users/MAC/Documents/THPT/số hoá THPT/Fundamentals of Physics 12th/`, 2 PDF) mà không xét giấy phép: `pdftotext` tìm
  "Figure NN.N.N" → số trang, `pdftoppm -r 200 -f N -l N` → cắt bằng PIL bỏ chữ Anh thừa, xoay nếu cần để hình nằm ngang,
  lưu `scripts/ruot-tap/anh/*.png` ≤150 KB, chèn bằng `hinh.anh(file, chú thích Việt dịch nhãn)`. Hình cao (dọc) tốn chỗ gấp
  đôi hình ngang — chọn hình ngang hoặc xoay; cột ảnh ≤ 24 mm chỉ còn đọc được nhờ chú thích.
  **Nguồn + hình đã dùng (cắt bằng `python3 scripts/ruot-tap/cat-anh.py`, bảng `ANH` trong script ghi pdf/trang/bbox, chạy lại là có đủ):**
  PDF = `/Users/MAC/Documents/THPT/số hoá THPT/Fundamentals of Physics 12th/Fundamentals of Physics 12th Volume 2.pdf` (chương 42 Nuclear Physics, 43 Energy from the Nucleus; trang PDF = trang in + 384).
  Bài 14: Fig 42.1.1 (tr.737) `rutherford-bo-thi-nghiem.png`, Fig 42.1.3 (tr.737) `rutherford-alpha-qua-la-vang.png`; bài 15: Fig 42.2.3 (tr.743) `nang-luong-lien-ket-rieng.png`;
  bài 16: Fig 43.2.2 (tr.778) `lo-phan-ung-nuoc-ap-luc.png`, Fig 43.5.1 (tr.784) `chu-trinh-proton-proton.png`; bài 17: Fig 42.3.1 (tr.748) `phong-xa-do-thi-ln-r.png`;
  bài 18 (an toàn phóng xạ): Halliday không có hình phù hợp (chỉ ảnh chụp), dùng SVG tự vẽ. Bản sao ảnh ngoài repo: `/Users/MAC/Documents/THPT/số hoá THPT/ruot-tap-anh/`.
  Hình Halliday chữ nhỏ (≈ 8 pt gốc) → thu còn 52–62 mm thì chữ trong hình không đọc được: chú thích tiếng Việt PHẢI nêu ý chính; muốn đọc được nhãn thì để rộng ≥ 84 mm (chu trình p–p).
  **Ảnh cắt từ sách và PDF chứa chúng chỉ giữ trên Mac, không đẩy lên GitHub** (`scripts/ruot-tap/anh/` và `out/*.pdf` đã
  gitignore từ 25/10) — có bản sao ở ngoài repo vì mất là phải cắt lại.
- **Trang sửa bài không có lưới đáp án**: đề làm trên web nên chỉ dòng "Câu sai P.I/P.II/P.III" + 4–5 ô Thầy chữa, mỗi ô có tick lí do
  và dòng "Mẹo nhớ" (ghi mẹo ngắn, không chép lại lời giải). Hai trang sửa bài phải KHÁC nhau: trang kiểm tra chương có thêm ô
  "Kế hoạch ôn chương" + "Lần trước". Không ô "câu hỏi cho trợ giảng".
- **Nhịp buổi thầy áp dụng (10/11/2026)**: 10′ ôn bài trước → 20′ kiểm tra → 30′ sửa bài → bài mới → giao BTVN. Giấy chỉ giữ việc phải
  viết tay (ghi bài, bài mẫu, bài tương tự, sửa bài); trắc nghiệm và bài nhiều câu luyện trên web có đáp án ngay — không chép đề
  trắc nghiệm ra giấy.
- **Bài tương tự trên giấy (bài 14, `bai14-tuongtu.mjs`, thầy chốt 10/11)**: sau Bài tập mẫu có 2 trang, MỖI DẠNG 2 bài cùng dạng
  làm tại chỗ (không dạng nào bị rút — 5 dạng thì 10 bài), đề ngắn, số dòng kẻ ≈ số ý, đáp số tính bằng Python in ở dải cuối trang
  **lật ngược 180°** (`transform:rotate(180deg)`) để HS không liếc thấy trước. Đề bài phải ghi đủ hằng số cần (N_A, e, 1 u) cho
  CẢ hai bài trong dạng. Dòng "Bài tương tự … /2" ở trang Bài tập mẫu phải khớp số bài thật. Để vẫn 12 trang thì bỏ 2 trang ghi chú
  tự do (quy ước "ghi chú đúng 2 trang" cũ không còn áp cho bài 14); thứ tự bài 14 hiện nay: 1–5 học bài mới · 6–7 Bài tập mẫu ·
  8–9 Bài tương tự · 10 sửa bài trên lớp · 11 sửa bài kiểm tra chương · 12 làm lại câu sai + QR. **Bài 15–18 (`khung.mjs`) vẫn
  bố cục cũ, chưa có trang Bài tương tự** — làm thì chép `bai14-tuongtu.mjs`.
- **Ảnh raster phải có trên máy dựng**: `scripts/ruot-tap/anh/` bị gitignore nên worktree mới không có → ảnh vỡ chỉ còn chữ alt,
  script vẫn báo thành công. Chép từ `/Users/MAC/Documents/THPT/số hoá THPT/ruot-tap-anh/` vào `scripts/ruot-tap/anh/` rồi dựng, và
  kiểm `pdfimages -list <pdf>` (trang có hình Halliday phải có ảnh cỡ hàng trăm px, không phải 14×16 px).
- **Chú thích hình không lộ đáp án ô Dự đoán** đứng cạnh (học sinh ảo bắt được ở bài 14): chú thích mô tả cái em thấy, không nêu kết luận.
- **Học sinh ảo dùng thử trước khi in** (10/11): mở phiên riêng đóng vai HS trung bình làm thử cả quyển, tính lại đáp số bằng Python,
  xếp lỗi A (sai/vô nghĩa) · B (khó dùng) · C (gợi ý); sửa A và B rồi mới in. Phiên con chạy Sonnet dù yêu cầu Opus (không nâng được model).
- **Bài 15–18 (lesson 16–19) dùng khung chung** `scripts/ruot-tap/khung.mjs` (CSS, trang 8–12 sinh tự động, bài tập mẫu `btm.dang`, chẩn đoán dư mm) + `hinh-ch4.mjs` (hình): chạy `node scripts/ruot-tap/bai15.mjs` … `bai18.mjs`. Bài 14 giữ bản riêng `bai14.mjs`. Bài mới: chép `bai18.mjs`, đổi `khoiTao({bai, lid})`, nội dung 5 trang đầu + mảng `dang`, thêm hình vào `hinh-ch4.mjs`.
- **Khung chung có bố cục bài 14 cho lớp/chương khác** (VL10 Ch.4, 10/11): `khoiTao({bai, lid, lop: 10, baiDau: 23})` (đánh số trang
  liền mạch từ `baiDau`) + `dung({…, tuongTu: {trang:[[{t,de,k}…],[…]], dap:[…], tieuDe:[…]}})` → tr.8–9 Bài tương tự (đáp số lật
  ngược), 10–11 sửa bài, 12 làm lại + QR; không có `tuongTu` thì bố cục cũ. `btm.dang[i].cot: 2` chia ô đáp số 2 cột khi đáp số dài/kép.
  Mỗi bài một file `l10-baiN.mjs` + hình riêng `hinh-l10-baiN.mjs` (không dùng chung file hình → phiên song song không xung đột);
  dựng cả quyển `bash scripts/ruot-tap/dung-l10-chuong4.sh`. Soạn cả chương: mỗi bài một phiên song song (nhánh riêng, tự gộp main),
  phiên chính chỉ giữ `khung.mjs` + script dựng quyển.
- **Checklist học sinh ảo cho ruột tập** (rút từ đợt VL10 Ch.4 — HS ảo bắt 40+ điểm dù đáp số đúng hết): (1) ô điền có đúng MỘT
  đáp án, đủ rộng (số ≥12 mm, chữ ≥25 mm, phân số cao ≥9 mm); (2) hình/thước đo/chú thích cạnh ô Dự đoán không lộ đáp án (vạch
  vẽ đúng tỉ lệ, dấu "?" đặt đúng vị trí, cột năng lượng vẽ bằng nhau đều là lộ); (3) mọi hằng số, đơn vị lạ (HP, CV, cal), danh
  sách (lực thế) và thuật ngữ ô hỏi tới đã có trong tập hoặc in sẵn; (4) tham chiếu "Xem lại ở Tập x·y" trỏ đúng ô; (5) số dòng
  kẻ ≥ số ý; (6) số + đơn vị không gãy dòng (`nw()`); (7) chữ trong hình ≥7 pt ở cỡ in; (8) bấm giờ: tr.8–9 (10 bài tương tự)
  cần ≥40′ với HS trung bình. **Thầy chốt 10/11: Bài tương tự là bài về nhà, GIẢI VÀO VỞ** — giấy chỉ in đề + ô đáp số
  (`tuongTu.vo = true`, mỗi bài `o: ['a','b',…]` thay `k`, hoặc `dapSo([...])` trong bố cục tự làm), đáp số in ngược xếp theo nhãn ô.
- **Đo chỗ viết bằng số, không ước bằng mắt**: `node scripts/ruot-tap/do-cho-viet.mjs out/<bài>.pdf.html` in số ý, số ô, dòng-130/ý.
  Giải trên giấy cần ≥ 2 dòng rộng 130 mm mỗi ý (dòng nửa cột 62 mm chỉ tính 0,5); không đạt thì chuyển sang giải vào vở.
- **Quyển = chương, đánh số trang liền mạch** (thầy chốt 26/10): bài 14 = tr.1–12, 15 = 13–24 … 18 = 49–60; chân trang "Bài N · tr. X", nhãn "Tập X·ô" và mọi tham chiếu (tr.10, trang 8, "Xem lại ở Tập") dùng số tuyệt đối (`khung.mjs`: `off`). Dựng cả quyển: `bash scripts/ruot-tap/dung-chuong4.sh` → `out/ruot-tap-vl12-chuong4.pdf` (60 trang, `pdfunite`). Nối tiếp chương liền kề: `BOOK_PAGE_START=61 bash …` (cả bài 14–18 theo; số bắt đầu chẵn thì lề gáy đổi bên; lưu ý data-tap trên web của bài 14 dùng số 1–12 nên chỉ khớp khi START=1).
- Cân trang bằng dòng `trang N: dư X mm` script in ra (mục tiêu 0–15 mm, âm = tràn); đo từng khối bằng
  `getBoundingClientRect` trên `.pdf.html` khi không rõ khối nào phình, rồi mới nhìn ảnh.

## Ruột tập cả chương bằng phiên song song (quy trình VL10 Ch.4 → VL11 Ch.3, 12/11/2026)
Thầy nói "làm ruột sách chương X lớp Y" → phiên chính KHÔNG soạn bài, chỉ dựng khung rồi mở mỗi bài một phiên:
1. **Hồ sơ + cache (phiên chính, tab terminal)**: `npx tsx book/lay-noi-dung.mts --moi l<lớp>-ch<N>-<tên> <lớp> <một lesson_id trong chương>`
   → sửa `book/sach/<mã>.json` bỏ "Kiểm tra chương"/"KT giữa/cuối HK" (không có lý thuyết). Tra id: Ch.2 L11 = 27–33, Ch.3 L11 = 35–40,
   L10 Ch.4 = 68–72; chưa biết thì đoán id gần rồi đọc danh sách lệnh in ra. `book/cache/` bị gitignore → mỗi phiên tự tải lại bằng
   `npx tsx book/lay-noi-dung.mts <mã>` (cần `.env.local`; worktree thiếu thì `ln -s /Users/MAC/Projects/thachlab/.env.local .env.local`).
2. **Script dựng quyển** `scripts/ruot-tap/dung-l<lớp>-chuong<N>.sh` (chép `dung-l11-chuong3.sh`: bỏ qua bài chưa có file, ghép
   bằng `pdfunite`, cảnh báo font hệ thống). Phiên chính là chủ DUY NHẤT của `khung.mjs` + script này; cần đổi khung thì phiên bài
   báo lại, không tự sửa.
3. **Commit hồ sơ + script + skill, đưa vào `main` TRƯỚC khi mở phiên** (ruleset chặn tự gộp: `git merge origin/main` →
   `git push origin HEAD:main`, kiểm `git log origin/main`). Phiên bài cũng vào main cách này; workflow tự gộp đỏ là bình thường.
4. **Mở mỗi bài một phiên** (`start_session`, worktree riêng, "fresh"), brief mẫu (thay số):
   > Soạn ruột tập VL11 bài 18 (lesson 37, Điện trường đều) theo skill `sach-in-tu-web` mục "Ruột tập theo bài" + checklist học sinh ảo.
   > `git fetch && git merge origin/main`; tải cache `npx tsx book/lay-noi-dung.mts l11-ch3-dien-truong` (tab terminal). Chép
   > `scripts/ruot-tap/l10-bai23.mjs` → `l11-bai18.mjs`, hình riêng `hinh-l11-bai18.mjs`; `khoiTao({bai:18, lid:37, lop:11, baiDau:16,
   > ten, sub:'Vật lí 11 · Chương 3: Điện trường'})`; bố cục bài 14 có `tuongTu` (`vo: true`, giải vào vở). Nội dung lấy từ
   > `book/cache/37.json` (lý thuyết + mọi dạng bài tập mẫu), đáp số tính bằng Python. Chỉ tạo/sửa 2 file của bài mình — KHÔNG đụng
   > `khung.mjs`, script dựng quyển, skill, STATE. Kiểm: 12 trang, dư 0–15 mm, katexErr=0, `pdffonts` sạch, `xem-hinh`, QR giải mã
   > đúng `?id=37`, `do-cho-viet.mjs`. Commit theo đường dẫn, push nhánh, báo trang nào dư bao nhiêu + điểm cần thầy quyết.
   **Brief luôn kèm 4 lỗi lặp (HS ảo L11 Ch.3)**: hằng số (k, e, 1 eV, g…) in sẵn trước khi hỏi · Mục tiêu/chú thích hình cạnh
   Dự đoán không lộ đáp án · ô đủ rộng cho phân số/đáp án dài · số dòng kẻ ≥ số ý ở Dạng 1–3. Bài không có bài tập mẫu (thực hành)
   → tr.6–9 dùng bảng số liệu + xử lí sai số + câu hỏi báo cáo thay Dạng. **Model**: bài có BTM → Opus; bài thực hành,
   bài nhập môn → Sonnet. Kế hoạch các chương còn lại: memory `project_thachlab_ruot_tap_con_lai.md`.
   Ảnh Halliday được dùng (L11 Ch.3 ↔ Vol.2 ch.21 Coulomb, 22 điện trường, 24 điện thế, 25 tụ điện) nhưng chỉ trên Mac, thêm vào
   bảng `ANH` của `cat-anh.py` + chép bản sao ra `ruot-tap-anh/`; không bắt buộc (L10 Ch.4 dùng toàn SVG).
5. **Khi các phiên xong** (phiên chính): merge main, `bash scripts/ruot-tap/dung-l<lớp>-chuong<N>.sh`, rồi MỘT phiên học sinh ảo
   điền thử cả quyển theo checklist (A/B/C) → giao sửa lại cho phiên của từng bài (`SendMessage`) thay vì sửa chéo; dựng lại, gửi PDF
   cho thầy, ghi memory dự án. Workflow tự gộp huỷ lượt chờ khi nhiều nhánh push cùng lúc → `gh run rerun <id>` lượt `cancelled`.

## Nhật ký rút kinh nghiệm (ruột tập)
- 2026-11-10 · Lỗi "chữ đậm lẫn Helvetica": khai báo `@font-face` nhiều tệp con (latin/vietnamese) mà không có `unicode-range` thì tệp sau đè tệp trước, ký tự thiếu rơi về font hệ thống → mỗi tệp con PHẢI kèm `unicode-range` (đã có ở `bai14.mjs`). Kiểm bằng `pdffonts <pdf>`: không được còn Helvetica/Lucida/Hiragino (còn sót ★, φ, chỉ số trên ở bài 14 tr.1/5/6).
- 2026-11-10 · `sed -i 's/…/…/' file` trên macOS hỏng (nuốt chuỗi thay làm hậu tố) → sửa chuỗi bằng Python `replace` có `assert count==1`.
- 2026-11-10 · Nhánh cũ tách từ `main` đã đi xa: `git fetch` + merge `main` TRƯỚC khi sửa ruột tập, nếu không dựng lại bản đã có. Hai QR cạnh nhau thì bỏ QR phụ (chỉ giữ QR bài học).
- 2026-11-10 · VL10 Ch.4 do 5 phiên song song soạn: đáp số đúng 100 % (Python) nhưng HS ảo vẫn thấy ~40 điểm khó dùng — ô quá hẹp, hình lộ đáp án Dự đoán, hằng số/thuật ngữ chưa có trong tập, 7/9 tham chiếu "Xem lại ở Tập" lệch ở một bài → luôn chạy checklist học sinh ảo ở mục trên trước khi in; tham chiếu Tập lấy từ nhãn thật trong `.pdf.html`, không đoán.
- 2026-11-10 · Yêu cầu "≥1 dòng mỗi ý" cho Bài tương tự là quá thấp: dòng nửa cột 62 mm chỉ đủ ghi đáp số, đo ra mỗi ý 0–1 dòng rộng trong khi lời giải cần ~2 → 10 bài/2 trang không thể vừa đề vừa lời giải; tính trước tổng mm cần (số ý × 2 dòng × 5 mm + đề) trước khi định số bài trên giấy.
- 2026-11-12 · VL11 Ch.3 (6 phiên): mỗi phiên tự soát checklist vẫn bỏ sót lỗi lặp cả quyển — hằng số k, e, 1 eV bị hỏi trước khi in, Mục tiêu/chú thích hình cạnh Dự đoán lộ đáp án, ô hẹp cho phân số/đáp án dài, dòng kẻ < số ý ở Dạng 1–3; một HS ảo đọc cả 6 file `.pdf.html` (text, không ảnh, ~90k token) bắt đủ → giao lại từng phiên bằng `SendMessage`, mỗi phiên sửa ~15′. Đưa sẵn 4 lỗi lặp này vào brief phiên bài lần sau.
- 2026-11-10 · 5 nhánh `claude/*` push cùng lúc → workflow tự gộp huỷ lượt chờ (concurrency) → `gh run list --workflow gop-claude-vao-main.yml`, lượt `cancelled` thì `gh run rerun <id>`.

## Cuối phiên
- Ghi memory `docs/memory/project_thachlab_sach_in_chuong2.md` (bản vN làm gì, số trang, còn treo).
- Commit `book/` (code + `sach/*.json` gồm cả sổ khoá `.lock.json`; HTML/PDF/cache sinh ra đã gitignore). `public/sach-data` + `app/(public)/sach/dap-an`
  chỉ commit/deploy khi đã kiểm trang web thật; chưa thì ghi "ĐANG CHỜ" trong `docs/STATE.md`.
- Vào main: ruleset `bao-ve-main-deploy` (12/11) chặn workflow tự gộp → phiên Mac `git merge origin/main` rồi
  `git push origin HEAD:main` (dòng "Cannot update this protected ref" vẫn hiện dù đẩy được — kiểm `git log origin/main`).
- Chỉ đưa đáp án sách lên web, không deploy cả main (main hay có code phiên khác chưa thử): worktree tạm từ
  `origin/deploy`, chép đúng `public/sach-data/{dap-an-<id>*.json,trang-<mã>.json,trang-bai.json}` vào `sach-data/`,
  commit, `git push origin HEAD:deploy` (fast-forward), hosting kéo trong ≤10 phút → bước 8. Cần thầy cho phép mỗi lần.
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
- 2026-10-25 · Ruột tập bài 15–18: tách KaTeX giữa chừng để chen ô trống (`m('…{')+fill+m('}')`) làm KaTeX báo lỗi → viết lại công thức bằng chỉ số riêng (`A_Y=` ô trống); hình trong SVG có `viewBox` rộng (>320) thì cột hình phải ≥ 52–56 mm mới giữ chữ ≈ 2,9 mm; hình chỉ hiện trong ô giải khi `gi > 0` (dạng `gi: 0` + `fig` thì mất hình, đã gặp ở Dạng 5 bài 18) → với dạng có hình luôn đặt `gi ≥ 1`; trang 7 tràn thì hạ `gi` các dạng không có hình trước, rồi mới rút hình.
- 2026-11-10 · Pipeline đọc `public/data/lessons` (chỉ có bài xem thử, gitignore) + bài tập mẫu trong repo nên sách không theo web thật và không dựng lại được ở máy/worktree khác → nguồn duy nhất là `book/cache` tải từ DB (`sach.py lech`), kèm sổ khoá để biết sách lệch web ở mức chữ hay mức đánh số.
- 2026-11-10 · Ba bài treo 10 phút rồi "render lỗi" không rõ lý do: bài trên web có thêm `<img loading="lazy" src="/assets/…">`; mở bằng file:// ảnh không tải, `img.decode()` của ảnh lazy không bao giờ xong nên Paged.js không chạy → `build.local_imgs` đổi mọi ảnh thành file cục bộ đen–trắng và bỏ `loading/width/height`. Bài treo thì so thẻ/lớp CSS với bài dựng được (đếm bằng regex) trước khi đoán Paged.js.
- 2026-11-10 · Web đổi lớp CSS (`tl-box--rule` thêm `tl-keep`) làm regex khớp nguyên chuỗi `class="…"` trượt → trang Tổng kết chương rỗng mà không báo lỗi; ảnh nguồn mở cao 880px chiếm trọn trang và để lại trang trống trước nó → regex lớp dùng `[^"]*`, ảnh giới hạn `max-height:62mm`, và `make.py` tự in CẢNH BÁO trang < 60 từ / bài thiếu hộp "Mang về". Sách dựng từ web sống thì mỗi kiểm tra bằng mắt cũ phải thành kiểm tự động.
- 2026-11-10 · `make.render` nuốt stdout của `render.mjs` nên dòng `CHẨN ĐOÁN` (KaTeX lỗi, tràn khung) không hiện khi dựng cả cuốn → muốn xem thì dựng lẻ `build.py lesson <id>` + `node render.mjs`; còn chờ sửa cho in ra.
- 2026-11-10 · Chương mới (L10 Ch.3) dùng thành phần web chưa có ở Ch.2: hộp video kiểu clip dựng lại (`<video>` + `.tl-video-ten`), iframe PhET trong `details`, mô phỏng CSS `.tl-sim` (5 SVG cho 5 nút radio → in cả 5 hình, tràn 2 trang gần trống), thuật ngữ `.tl-term` (in dính "Chất điểmVật nhỏ…") → mỗi cuốn mới: đếm `<video|<iframe|tl-sim|tl-term|<input` trong `book/cache/*.json` TRƯỚC khi dựng, thứ nào `build.py` chưa có luật thì thêm luật in (đã thêm `sim_one_frame`, regex video/iframe/term).
- 2026-11-10 · `--moi` lấy cả bài "Kiểm tra chương" (không có lý thuyết) vào `lessons` → `lay-noi-dung.mts` báo lỗi; bỏ id đó khỏi hồ sơ.
- 2026-11-11 · Thầy thấy nhiều trang trống lớn + hình mô phỏng in ra to mà vô ích (trên web chạy được, trên giấy chỉ là khung tĩnh) → 30 hình mô phỏng Ch.3 thu thành một dòng chú thích (`sim_line`), giữ đồ thị/số liệu; đo trống bằng `do_trong.py` (155→147 tr., 479→428 cm trống). Mặc định sách in: hình chỉ in khi tự nó mang thông tin (sơ đồ lực, đồ thị, ảnh thật).
- 2026-11-11 · Sách nên có ảnh THỰC TẾ (hiện tượng đời sống) thay hình mô phỏng; web không có thì cắt Halliday (nội bộ, không xét bản quyền) → khai báo `anh_that` trong hồ sơ sách. File Halliday trong Documents là iCloud `dataless`: sandbox/`cp` báo "Operation timed out", `brctl download` không kéo về được → kiểm `ls -lO` TRƯỚC, dataless thì nhờ thầy bấm Tải về trong Finder ngay đầu việc, đừng chờ vòng lặp.
- 2026-11-11 · Tăng cỡ chữ thân 9,6→10,5pt: `book.css` có 4 dòng `html{font-size…}` đè nhau (v2, v4…) và giãn dòng thật nằm ở khối v4 → grep mọi chỗ đè trước khi sửa; chữ to hơn đẩy khung QR "Ở nhà" sang trang riêng ở 3 bài (cảnh báo < 60 từ).
- 2026-11-11 · Ảnh thực tế từ Wikimedia: tìm cả chương bằng 1 script + 1 tờ ghép 4 ứng viên/bài (xem 1 ảnh thay vì 40), API trả 429 khi gọi dồn → nghỉ 1,5 s/lần + thử lại. Truy vấn tiếng Anh theo hiện tượng (crash test dummy, bobsleigh start push, claw hammer…); chủ đề trừu tượng (khung ảnh treo hai dây) không có ảnh hợp → bỏ, đừng nhét ảnh lạc đề. Neo dưới đoạn đầu "Mở bài" thì ảnh thành móc vào bài và không phá bố cục mục II.
- 2026-11-11 · Hình SVG web in theo bề ngang trang → chữ trong hình to gấp 2 chữ thân, hình chiếm nửa trang → `build.fit_figs` tính bề rộng theo cỡ chữ trong SVG (≈9pt, nhỏ nhất ≥7,6pt); hình ≤100 mm nổi phải (`.fig.fl`, `svg.svfl`), khối có khung `display:flow-root` để đứng cạnh hình; khung Thí nghiệm `clear:both` (đứng cạnh hình thì chật). Ảnh thực tế nổi trái, chèn TRƯỚC đoạn mở bài để chữ chảy cạnh ảnh.
- 2026-11-11 · Thay class bằng `str.replace('fig', 'fig fl')` biến `<figure` thành `<fig flure` → luôn thay cả chuỗi `class="…"`.
- 2026-11-11 · Trang trống đáy: `book.js` sau Paged.js đo đáy nội dung (Range của chữ + khung có viền/nền + ảnh; bỏ phần tử `pagedjs_*` vì khung bao cao 100%) và lấp ≥28 mm bằng ô "Ghi chép" ca-rô nét đứt mờ 3,5 mm; ô `.dl` cũng ca-rô. Tile SVG data-URI: nét tính theo đơn vị tile (40 đơn vị → 3,5 mm thì stroke 2), không thì in ra gần như vô hình. `do_trong.py` vẫn tính vùng ca-rô là trống — đếm trang có "GHI CHÉP" để biết đã lấp.
