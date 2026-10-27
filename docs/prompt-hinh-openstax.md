# Prompt: thay/bổ sung hình bài lý thuyết lớp 12 bằng hình OpenStax College Physics 2e

Viết 27/10/2026, thay cho kế hoạch HRW (`docs/prompt-ra-hinh-theo-hrw.md`; bảng rà và 19 bài đã sửa SVG nằm ở nhánh
`claude/kind-satoshi-913de4`, đã vào `main`, **chưa đăng DB**). Giao cho một phiên Sonnet, context mới, chạy trên Mac.

## Giấy phép — đọc kỹ trước khi làm (kiểm 27/10/2026 tại trang Preface)

- *College Physics 2e* (Urone & Hinrichs, OpenStax, 2022) và cả bộ *University Physics* đều là **CC BY‑NC‑SA 4.0**, không phải
  CC BY. Ba điều kiện: ghi nguồn; **phi thương mại**; bản phái sinh (hình đã dịch nhãn, vẽ lại theo) phải giữ cùng giấy phép.
- Dùng trên thachlab chỉ khi thầy Thạch đã chấp nhận điều kiện phi thương mại (trang web không bán nội dung này). Nếu thầy chưa
  chốt, dừng ở giai đoạn 1 (chọn hình), không chèn.
- OpenStax yêu cầu dòng ghi nguồn trên **mỗi trang** dùng nội dung: dạng tiếng Việt
  `Hình: OpenStax, College Physics 2e, Hình 22.3 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e` đặt ngay trong
  `<figcaption>` của từng hình (mỗi ý một dòng theo quy tắc chú thích). Hình nào trong sách có `(credit: …)` thì giữ nguyên
  dòng credit đó, vì đó là ảnh bên thứ ba.
- Thêm một đoạn ở `/dieu-khoan` (app/dieu-khoan) nói rõ: một số hình trích từ OpenStax theo CC BY‑NC‑SA 4.0, bản dịch nhãn của
  thachlab cũng theo giấy phép đó. Việc này chỉ làm một lần, ở giai đoạn 2.

## Mục tiêu

Hình trong bài lý thuyết lớp 12 đúng vật lý và rõ như sách in: thay hoặc bổ sung bằng hình OpenStax ở những chỗ hình SVG tự vẽ
còn yếu (theo bảng `docs/ra-soat/hinh-hrw-l12.md`, cột mức A/B/C và Trạng thái), giữ SVG ở chỗ SVG đã đủ tốt hoặc cần chữ Việt
trong hình. Không thêm hình chỉ để trang trí (quy tắc G1/G2, M trong `docs/QUY-TAC-THIET-KE.md`).

## Quy tắc chọn hình (quyết định cho từng hình, ghi lý do vào bảng)

| Loại hình OpenStax | Cách dùng |
|---|---|
| Ảnh chụp thật, hình không có chữ hoặc chỉ có ký hiệu (B, v, F, N, S) | **Chèn trực tiếp** (webp) |
| Sơ đồ có nhãn tiếng Anh ngắn (≤ 5 từ) | Chèn trực tiếp, giải nghĩa nhãn trong figcaption, mỗi nhãn một dòng |
| Sơ đồ nhiều chữ tiếng Anh, bảng, đồ thị có trục chữ | **Vẽ lại SVG** theo bố cục đó bằng `svg_lib.py`, nhãn tiếng Việt, ghi "vẽ lại theo OpenStax Hình x.y" |
| Hình ở đơn vị/bối cảnh Mỹ (feet, dặm, °F) không tránh được | Vẽ lại SVG, đổi sang SI |
| Hình có `(credit: …)` của bên thứ ba mà giấy phép riêng không rõ | Không dùng |

Mỗi bài giữ tổng số hình ≤ 6 và hạn mức độ dài trong `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`; thay hình, không chồng thêm.

## Ánh xạ bài ↔ chương College Physics 2e (agent mở mục lục để chốt số mục)

| Bài | Chương / mục OpenStax |
|---|---|
| l12-thang-nhiet-do, l12-noi-nang-dl1, l12-su-chuyen-the, l12-thuc-hanh-nhiet | 13.1–13.2, 14.1–14.3, 15.1 |
| l12-thuyet-dong-hoc-phan-tu, l12-ap-suat-dong-nang, l12-boyle-charles, l12-phuong-trinh-trang-thai | 13.3–13.4 |
| l12-khai-niem-tu-truong, l12-luc-tu-cam-ung-tu, l12-thuc-hanh-cam-ung-tu | 22.1–22.7 |
| l12-cam-ung-dien-tu, l12-ung-dung-cam-ung-dien-tu | 23.1–23.4 |
| l12-dong-dien-xoay-chieu, l12-may-phat-dien-bien-ap | 20.5, 23.5–23.6 |
| l12-dien-tu-truong-song-dien-tu | 24.1–24.3 |
| l12-hat-nhan-mo-hinh-nguyen-tu, l12-nang-luong-lien-ket | 30.2, 31.3, 31.6 |
| l12-phong-xa, l12-an-toan-phong-xa | 31.1–31.5, 32.1–32.2 |
| l12-phan-hach-nhiet-hach | 32.5–32.6 |

Bỏ qua `l12-ung-dung-cam-ung.cu` (bản cũ đã đổi tên, không đăng).

## Cách lấy hình

- Trang bài: `https://openstax.org/books/college-physics-2e/pages/<mục>` ; đọc bằng `WebFetch` (văn bản) để lấy số hình,
  caption, credit và URL ảnh dạng `https://openstax.org/apps/image-cdn/v1/f=webp/apps/archive/<ngày>/resources/<hash>`.
  Đọc ảnh để chọn thì làm trong subagent, không ở phiên chính.
- Tải: `curl -L -o <tmp>.webp <url>`; nén/thu bằng `sharp` (có sẵn, xem `scripts/optimize-images.mjs`): rộng ≤ 1200 px,
  ≤ 150 KB, webp. Lưu ở `public/assets/openstax/<slug bài>/hinh-<n>.webp`. Không base64, không nhúng URL CDN của OpenStax
  thẳng vào bài (hash đổi theo đợt archive).
- Chèn theo mẫu đã dùng cho AVCN:
  `<figure class="fig"><img src="/assets/openstax/<bài>/hinh-2.webp" alt="<mô tả tiếng Việt>" loading="lazy" width=".." height=".."><figcaption>…</figcaption></figure>`
  — chèn vào `theory.src.html` tại đúng mốc hình thay thế (`<!--FIG:n-->` nếu bài dùng `build_figs.py`: bỏ hình đó trong
  `build_figs.py`, giữ mốc), chạy `build_figs.py` + `build_bundle.py`. Hình ảnh raster là ngoại lệ có chủ đích của quy tắc
  "SVG tự vẽ" trong skill `soan-bai-ly-thuyet-tuong-tac` — ghi vào `nguon.md` của bài.

## Hai giai đoạn

**Giai đoạn 1 — chọn (không sửa bài):** với 21 bài, lập `docs/ra-soat/hinh-openstax-l12.md`:

```
| Bài | Hình hiện có (aria-label) | Hình OpenStax (số, caption ngắn, credit) | Quyết định (chèn trực tiếp / vẽ lại / giữ SVG) | Lý do |
```
Thêm cả hàng "hình mới" nếu bài thiếu hình ở một kiến thức có hộp thí nghiệm mà sách có hình tốt. Commit bảng, push, báo
một lần: số hình chèn trực tiếp / vẽ lại / giữ, và 5 bài đổi nhiều nhất. Dừng chờ thầy duyệt.

**Giai đoạn 2 — làm (sau khi thầy duyệt bảng):** mỗi bài một mẻ: tải + nén ảnh → chèn/vẽ lại → build → `chup_anh.py` 375 px,
đọc ảnh trong subagent (ảnh không tràn, chữ đọc được, không chồng caption) → `kiem-code` soát diff → `nguon.md` →
`git commit -- content/lesson-samples/<bài>/ public/assets/openstax/<bài>/ docs/ra-soat/hinh-openstax-l12.md` → đăng bằng
`bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/<bài>/theory.html <lesson_id>` trong tab terminal, mỗi lệnh một bài,
đọc kết quả; script hỏi [y/N] thì dừng để thầy gõ, không dùng `--yes` trừ khi thầy bảo. Mã bài: su-chuyen-the 2,
thang-nhiet-do 3, noi-nang-dl1 4, thuc-hanh-nhiet 5, thuyet-dong-hoc 6, boyle-charles 7, phuong-trinh-trang-thai 8,
ap-suat-dong-nang 9, khai-niem-tu-truong 10, luc-tu-cam-ung-tu 11, thuc-hanh-cam-ung-tu 12, cam-ung-dien-tu 13,
hat-nhan 15, nang-luong-lien-ket 16, phong-xa 18, an-toan-phong-xa 19, may-phat-dien-bien-ap 125,
ung-dung-cam-ung-dien-tu 126, dien-tu-truong-song-dien-tu 127 (kiểm lại bằng `npx tsx scripts/liet-ke-bai.mts`).
Deploy ảnh mới trong `public/` theo quy trình deploy hiện hành (ảnh không nằm trong DB).

## Tiết kiệm token
- Phiên chính không đọc ảnh; mỗi subagent một bài; `WebFetch` theo trang mục, không tải cả chương.
- Không báo tiến độ giữa chừng. Lỗi ghi vào `ra-soat.md` của bài. Cuối phiên: Rút kinh nghiệm vào
  `.claude/skills/soan-bai-ly-thuyet-tuong-tac/SKILL.md` mục Nhật ký, dòng ĐANG CHỜ vào `docs/STATE.md` nếu còn bài chưa đăng.
