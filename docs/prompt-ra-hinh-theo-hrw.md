# Prompt: rà hình SVG bài lý thuyết lớp 12 theo Halliday–Resnick–Walker bản 12 (HRW)

Viết 26/10/2026 để giao cho một phiên/agent riêng (Sonnet, context mới). Phiên chính không đọc PDF, không đọc ảnh.
Chạy trên Mac (cần `pdftoppm`, `pdftotext`, PyMuPDF đã có; ĐĂNG DB cần `.env.local`).

---

## Nhiệm vụ

Đối chiếu từng hình SVG tự vẽ trong 22 bài lý thuyết lớp 12 (`content/lesson-samples/l12-*/`, ~90 hình) với hình
tương ứng trong sách *Fundamentals of Physics, 12th ed.* (HRW), hai file PDF ở
`/Users/MAC/Documents/THPT/số hoá THPT/Fundamentals of Physics 12th/` (Volume 1: chương 1–20, Volume 2: chương 21–44).
Mục tiêu: tìm chỗ hình của ta **sai hoặc kém rõ** so với sách (chiều vectơ, tỉ lệ vật lý, góc nhìn, thiếu nhãn, nhãn đặt xa
phần tử, thiếu phần tử quan trọng, sai quy ước), rồi sửa trong **nguồn vẽ** của bài. Không "làm đẹp" cho giống sách.

**Hai giai đoạn, dừng giữa chừng chờ thầy duyệt:**
1. **Rà** cả 22 bài → bảng phát hiện ở `docs/ra-soat/hinh-hrw-l12.md`. Không sửa gì ở giai đoạn này. Commit bảng, báo thầy.
2. **Sửa** các dòng thầy duyệt → build lại → xem thử 375 px → đăng bằng `cap-nhat-ly-thuyet.sh` → commit từng bài.

## Bản quyền — bắt buộc (`docs/AGENTS-CHUYEN-DE.md` mục "Bản quyền", thầy chốt 12/10/2026)

- HRW là sách giữ bản quyền (Wiley), **không có giấy phép mở**. Không cắt, không đồ lại, không chèn ảnh trang sách vào bài,
  vào repo, vào `bundle.json`. Ảnh trang sách chỉ nằm trong thư mục tạm, xoá sau khi rà.
- Chỉ lấy **ý tưởng bố cục và tính đúng đắn vật lý**: góc nhìn, phần tử nào cần có, nhãn nào cần, chiều vectơ. Vẽ lại bằng
  `svg_lib.py` theo bối cảnh của bài (vật, số liệu, chữ Việt). Hình sửa xong phải khác hình sách về bố cục cụ thể.
- Ghi vào `nguon.md` trong thư mục bài: `Hình n — bố cục tham khảo HRW 12e, Fig. X-Y (ch. X), vẽ lại bằng svg_lib`.

## Ánh xạ bài ↔ chương HRW (đọc mục lục ở trang đầu mỗi PDF để chốt số trang)

| Bài | Chương HRW |
|---|---|
| l12-thang-nhiet-do, l12-noi-nang-dl1, l12-su-chuyen-the, l12-thuc-hanh-nhiet | 18 Temperature, Heat, and the First Law of Thermodynamics |
| l12-thuyet-dong-hoc-phan-tu, l12-ap-suat-dong-nang, l12-boyle-charles, l12-phuong-trinh-trang-thai | 19 The Kinetic Theory of Gases (+ 18 cho pV) |
| l12-khai-niem-tu-truong, l12-luc-tu-cam-ung-tu, l12-thuc-hanh-cam-ung-tu | 28 Magnetic Fields, 29 Magnetic Fields Due to Currents |
| l12-cam-ung-dien-tu, l12-ung-dung-cam-ung-dien-tu, l12-ung-dung-cam-ung.cu | 30 Induction and Inductance |
| l12-dong-dien-xoay-chieu, l12-may-phat-dien-bien-ap | 31 Electromagnetic Oscillations and Alternating Current (máy phát: 30) |
| l12-dien-tu-truong-song-dien-tu | 33 Electromagnetic Waves |
| l12-hat-nhan-mo-hinh-nguyen-tu, l12-nang-luong-lien-ket, l12-phong-xa, l12-an-toan-phong-xa | 42 Nuclear Physics |
| l12-phan-hach-nhiet-hach | 43 Energy from the Nucleus |

Lưu ý khác biệt quy ước: HRW dùng SI nhưng ký hiệu khác SGK Việt Nam (ví dụ `ℰ` cho suất điện động, `Φ_B`, `i` cho dòng tức
thời). Khác ký hiệu **không** phải lỗi. Chỉ ghi nhận khác biệt về **vật lý và cách truyền đạt**.

## Cách làm từng bài (lặp 22 lần, mỗi bài một mẻ, không gom)

1. Liệt kê hình của ta: `grep -o '<figure class="fig"[^>]*><svg[^>]*aria-label="[^"]*"' theory.html` và `figcaption`.
   Nguồn vẽ là `build_figs.py` (chèn vào mốc `<!--FIG:n-->` của `theory.src.html` → `theory.html`); vài bài vẽ SVG
   thẳng trong `theory.src.html` — xác định trước bằng `grep -c '<svg' theory.src.html`.
2. Chụp hình của ta ở 375 px: `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/chup_anh.py` (đọc đầu file để
   biết tham số) → ảnh vào `xem-thu/`.
3. Tìm hình sách khớp: `pdftotext -f A -l B <pdf> - | grep -n "Fig\. 30-"` quanh phạm vi trang của chương (mục lục cho số
   trang đầu chương; chương HRW dài ~30–40 trang). Chọn 1–3 hình sách cùng hiện tượng cho mỗi hình của ta.
   Render trang sách: `pdftoppm -r 110 -f N -l N -png <pdf> /tmp/hrw/p` (thư mục tạm, xoá sau).
4. **Đọc ảnh trong subagent**, không ở phiên chính: giao agent `general-purpose` (model sonnet) đọc ảnh trang sách + ảnh
   hình của ta, trả về **chỉ văn bản** theo mẫu dưới. Mỗi agent tối đa một bài (≤6 hình).
5. Ghi vào bảng `docs/ra-soat/hinh-hrw-l12.md`:

```
| Bài | Hình (aria-label) | HRW Fig. | Phát hiện | Mức | Cách sửa đề xuất |
```
   - Mức: **A** sai vật lý (chiều lực/từ trường/dòng, tỉ lệ dẫn tới hiểu sai) · **B** thiếu phần tử hoặc nhãn làm HS khó
     đọc · **C** khác sách nhưng của ta chấp nhận được (ghi 1 dòng, không sửa).
   - Mỗi phát hiện một dòng, viết cụ thể ("mũi tên B ở hình 2 hướng xuống, phải hướng vào trang theo quy tắc bàn tay phải
     với dòng chiều này"), không viết "nên đẹp hơn".
   - Hình không có hình sách tương ứng: ghi "không có đối chiếu", bỏ qua.

## Giai đoạn 2 — sửa (chỉ các dòng mức A, B được thầy duyệt)

- Sửa trong `build_figs.py` (hoặc `theory.src.html` nếu SVG nằm thẳng ở đó), chạy `python3 build_figs.py` rồi
  `python3 build_bundle.py` trong thư mục bài. Đọc `.claude/skills/soan-bai-ly-thuyet-tuong-tac/references/hinh-svg.md` và
  `docs/QUY-TAC-THIET-KE.md` mục H, V trước khi vẽ.
- Quy tắc hình (`docs/AGENTS-CHUYEN-DE.md`): đường sức từ nét đứt, đầu mũi tên chevron 30° (`field_line`/`chevron` trong
  `svg_lib.py`); chú thích mỗi ý một dòng; nét/chữ `currentColor`; chữ ≥ 14 đơn vị viewBox; ≤ 15 KB/hình; không base64.
- Chụp lại 375 px, đọc ảnh trong subagent để xác nhận, rồi đăng: `bash scripts/cap-nhat-ly-thuyet.sh <thư mục bài>/theory.html <lesson_id>`
  (lesson_id tra bằng `npx tsx scripts/liet-ke-bai.mts`; chạy trong tab terminal, đọc kết quả, không chạy nền).
- Commit theo đường dẫn, mỗi bài một commit:
  `git commit -- content/lesson-samples/<bài>/ docs/ra-soat/hinh-hrw-l12.md` — không `git add .`, không `commit -a`.
- Lỗi gặp trong lúc làm ghi vào `ra-soat.md` của thư mục bài (quy ước chặng commit + ra-soat.md).

## Tiết kiệm token

- Phiên chính chỉ điều phối và ghi bảng; mọi ảnh (trang sách, ảnh chụp 375 px) đọc trong subagent.
- `pdftotext` theo khoảng trang hẹp, không đổ cả PDF ra. Không đọc `theory.html` cả file — grep đúng thẻ `<figure>`.
- Không báo tiến độ giữa chừng; xong giai đoạn 1 báo một lần kèm số dòng A/B/C từng bài.
- Nếu một bài không có hình sách khớp sau 2 lần tìm, ghi "không có đối chiếu" và đi tiếp.

## Kết quả cần nộp

- Giai đoạn 1: `docs/ra-soat/hinh-hrw-l12.md` (bảng đủ 22 bài) + tóm tắt: số hình mức A, B, C; 5 lỗi đáng sửa nhất.
- Giai đoạn 2: danh sách bài đã sửa và đã đăng, commit tương ứng, `nguon.md` từng bài đã có dòng tham khảo HRW.
- Cuối phiên: mục "Rút kinh nghiệm" (3–6 dòng) ghi vào `.claude/skills/soan-bai-ly-thuyet-tuong-tac/SKILL.md` mục
  Nhật ký nếu bài học gắn với cách vẽ hình; ghi dòng ĐANG CHỜ vào `docs/STATE.md` nếu còn bài chưa đăng.
