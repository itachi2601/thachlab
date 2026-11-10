# Thiết kế: nâng cấp skill `sach-in-tu-web` thành sách đồng bộ với website

Ngày 10/11/2026 · bản thiết kế, CHƯA cài đặt. Thầy đã chốt: nâng cấp skill cũ (không tạo skill mới) ·
đồng bộ = **nội dung luôn khớp web** + **liên kết hai chiều** · xuất **PDF A4 đen–trắng** + **Word**.

## 1. Hiện trạng và ba chỗ hở

| Chỗ hở | Chi tiết đã kiểm trong code |
|---|---|
| Viết cứng một chương | `CHAPTER` trong `book/build.py:24` (lớp 11 Sóng phải bật bằng biến môi trường `BOOK_CHAPTER`); tên chương, "Chín ga", tổng kết viết thẳng trong `book/front.py`; tên file PDF cố định. |
| Nguồn nội dung không phải web thật | `load_lesson` đọc `public/data/lessons/<id>.json` — thư mục bị gitignore, `build-content.mjs` chỉ xuất **bài xem thử** (checkout chính hiện có 3 file). Bài tập mẫu đọc `scripts/data/bai-tap-mau/<id>.json` trong repo, có thể khác bản đã đăng DB. |
| Không biết sách lệch web lúc nào | Không lưu dấu vết "sách này dựng từ bản nội dung nào". Sửa bài bằng `cap-nhat-ly-thuyet.sh` xong thì sách cũ lệch mà không ai báo. QR đáp án không mang số bản → sách đã phát cho lớp trỏ vào đáp án của bản mới, **lệch số ô/số câu**. |

## 2. Kiến trúc sau nâng cấp

```
DB (web thật) ──lay-noi-dung──▶ book/cache/<lid>.json ──build.py──▶ HTML sách ──┬─ render.mjs ─▶ PDF A4
                    │                                                           └─ word.py ───▶ .docx
                    ▼                                                  │
        book/sach/<mã>.lock.json  ◀── ghi sau khi dựng ────────────────┘
        (dấu vân tay nội dung, số trang, số bản)
                    │
                    ├─▶ public/sach-data/dap-an-<lid>-b<bản>.json   (QR trong sách → web)
                    └─▶ public/sach-data/trang-<mã>.json            (web → "Sách tr. X")
```

### 2.1 Hồ sơ sách `book/sach/<mã>.json` — thay mọi chỗ viết cứng
Mỗi cuốn một file, ví dụ `l10-ch2-dong-hoc.json`:
```json
{
  "ma": "l10-ch2-dong-hoc", "lop": 10, "chuong": 2,
  "ten": "Động học", "phu_de": "Mô tả chuyển động — chưa cần hỏi vì sao vật chuyển động",
  "lessons": [49, 50, 51, 52, 53, 54, 55, 56, 57],
  "dang_chung": { "49": [1, 2] },
  "tiet": { "49": ["muc:II", "bai-tap-mau"] },
  "ban_do_chuong": { "tieu_de": "Chín ga trên tuyến “Động học”", "ga": ["…"] },
  "tong_ket": ["…"]
}
```
- `dang_chung`, `tiet` chuyển từ `book/src/*.json` vào đây (một nơi cho thầy chỉnh).
- `ban_do_chuong`, `tong_ket` thiếu thì `front.py` **bỏ trang đó**, không bịa; `FRONT_PAGES` tính theo số trang thật có.
- Lệnh: `python3 make.py <mã>` · `python3 make.py <mã> 49 50` · `python3 make.py --list`.
- Thêm cuốn mới: `python3 sach.py moi <lớp> <chương>` sinh hồ sơ nháp từ danh sách bài của chương (đọc cache), thầy chỉ sửa chữ.

### 2.2 Lấy nội dung từ web thật: `book/lay-noi-dung.mts <mã>`
- Chỉ ĐỌC, đúng một truy vấn cho cả chương: `lessons` + `lesson_items` (`ly_thuyet`, bài tập mẫu) theo danh sách `lessons`.
- Ghi `book/cache/<lid>.json` (gitignore) kèm `updated_at` và dấu vân tay `sha256` riêng cho lý thuyết / bài tập mẫu
  (chuẩn hoá khoảng trắng trước khi băm để đổi format không tính là lệch).
- Bài tập mẫu lấy **bản DB**; nếu khác `scripts/data/bai-tap-mau/<lid>.json` trong repo thì in cảnh báo
  "repo có bản chưa đăng" — sách theo web, không theo bản nháp.
- Cần mạng + `.env.local` → chạy trong tab terminal (sandbox `Bash` chặn `*.supabase.co`). Phiên cloud: in lệnh cho thầy.
- Tải nhẹ (vài chục dòng) nên không vướng quy tắc "ghi/quét hàng loạt sau 22h".

### 2.3 Sổ khoá `book/sach/<mã>.lock.json` (commit vào git) — trái tim của "đồng bộ"
Ghi sau mỗi lần dựng thành công:
```json
{ "ban": 7, "ngay": "2026-11-10", "tong_trang": 124,
  "bai": { "49": { "ly_thuyet": "sha…", "btm": "sha…", "trang": [6, 18],
                   "o_dien": 14, "cau": 7, "dang": 5,
                   "neo": { "muc:I": 6, "muc:II": 8, "dang:1": 14, "luyen-them": 16 } } } }
```
Lệnh `python3 sach.py lech <mã>` (chạy `lay-noi-dung` rồi so với sổ khoá) in bảng:

| Bài | Phần | Mức lệch | Hệ quả |
|---|---|---|---|
| 52 | Lý thuyết | **Chữ** — số ô điền/câu/Dạng không đổi | Dựng lại bài đó; sách đã phát vẫn dùng được, QR vẫn đúng |
| 54 | Bài tập mẫu | **Đánh số** — thêm 1 Dạng | Tăng số bản; sách đã phát giữ đáp án bản cũ (mục 2.4) |
| 57 | — | Khớp | Không làm gì |

Ba mức: `khớp` · `chữ` (dấu vân tay đổi, bộ đếm `o_dien/cau/dang` giữ nguyên) · `đánh số` (bộ đếm đổi).
Không lệch thì skill dừng ngay, không dựng lại. Số trang đổi sau khi dựng lại cũng được báo (bài nào dời trang).

### 2.4 Liên kết hai chiều
**Sách → web (đã có, thêm số bản).** QR đáp án thành `/sach/dap-an/?bai=49&b=7`; dữ liệu ghi
`public/sach-data/dap-an-49-b7.json`, giữ file bản cũ. Trang `/sach/dap-an` đọc `b`, thiếu `b` thì lấy bản mới nhất
(tương thích sách v5/v6 đã in). Chỉ tăng `ban` khi có lệch mức **đánh số**; lệch mức **chữ** ghi đè file bản hiện tại.
Không đưa dữ liệu cá nhân nào vào query (chỉ id bài và số bản).

**Web → sách (mới).** `make.py` sinh `public/sach-data/trang-<mã>.json` từ `neo` trong sổ khoá:
`{ "49": { "ban": 7, "muc": {"I": 6, "II": 8}, "dang": {"1": 14}, "dap_an": 123 } }`.
- Giai đoạn 1 (không đụng UI học sinh): chế độ trình chiếu của thầy (`LessonPresenter`, đã có cơ chế `data-tap` cho ruột tập)
  hiện "Sách tr. 8" cạnh tiêu đề mục — thầy đang chiếu web nói ngay được "mở sách trang 8".
- Giai đoạn 2 (UI học sinh, **chờ thầy quyết**): nhãn nhỏ "Sách tr. 8" ở tiêu đề mục trang bài học, chỉ cho lớp có phát sách.
  File tĩnh nạp lười, **không thêm round-trip Supabase** cho `/lop-hoc/bai`. Theo `QUY-TAC-THIET-KE.md` phải soát tải nhận thức
  (thêm một nhãn trên mỗi tiêu đề) và chụp 375px trước khi bật.

### 2.5 Bản Word `book/word.py <mã>`
- Dùng **cùng HTML trung gian** mà PDF dùng (sau `build.py`, trước Paged.js) → `pandoc` (đã có ở `/opt/homebrew/bin/pandoc`)
  với `--from html+tex_math_dollars` để công thức thành **phương trình Word sửa được**, `--reference-doc book/src/mau.docx`
  cho phông/cỡ chữ/lề theo trang mẫu sách của thầy.
- Hình SVG: đã qua `bw.gray_svg` (đen–trắng) → PNG 300 dpi rồi nhúng (Word hiển thị SVG không ổn định giữa các máy).
- Khung GHI NHỚ, ô lời giải, bảng phân tích đề → bảng Word một ô có viền; ô điền công thức → gạch chân trống có số.
- Giới hạn nói thẳng trong skill: Word **không giữ dàn trang** của PDF (số trang, vạch tiết, mục lục theo trang PDF không áp dụng;
  Word tự sinh mục lục theo Heading). Word là bản để thầy chỉnh tay/gửi đồng nghiệp: **sửa trong Word không quay ngược về web**,
  chân trang ghi "dựng từ thachlab.id.vn · bản 7 · 10/11/2026" để biết nó ứng với bản nào.
- Kiểm tự động: mở lại `.docx` đếm phương trình OMML = số công thức trong HTML; không còn `$` trần; đủ số hình.

## 3. Luồng skill sau nâng cấp (nội dung `SKILL.md` mới)

1. **Hỏi bối cảnh** (giữ nguyên quy tắc cũ): trên lớp có thầy hay tự học; cuốn nào (`make.py --list`).
2. **Lấy nội dung + soát lệch**: `sach.py lech <mã>` trong tab terminal → báo bảng lệch. Khớp hết → dừng.
3. **Dựng**: `make.py <mã>` (chỉ dựng lại bài lệch + phần đầu/cuối; số trang dồn tự động).
4. **Kiểm** (5 bước cũ) + 3 bước mới: số in trong sách = số trong `dap-an-<lid>-b<bản>.json`; mọi số trang trong
   `trang-<mã>.json` trỏ đúng tiêu đề trong PDF; giải mã lại từng QR bằng `scripts/kiem-qr.mts`.
5. **Word** (khi thầy cần): `word.py <mã>` + kiểm OMML.
6. **Chốt**: ghi sổ khoá, commit `book/sach/*` + `public/sach-data/*` theo đường dẫn; deploy json khi đã mở thử
   `/sach/dap-an/?bai=<id>&b=<bản>`; gửi thầy ảnh trang mẫu + link PDF/Word.

Gắn vào quy trình đăng bài: cuối `cap-nhat-ly-thuyet.sh` in một dòng nhắc nếu `lesson_id` thuộc một hồ sơ sách
("bài 52 nằm trong sách l10-ch2-dong-hoc — chạy `sach.py lech`"). Chỉ nhắc, không tự dựng.

Phần **ruột tập theo bài** đang chiếm nửa `SKILL.md` → tách sang `.claude/skills/sach-in-tu-web/RUOT-TAP.md`, chỉ đọc khi làm
ruột tập (đỡ token mỗi lần gọi skill). Mô tả skill giữ ≤ 400 ký tự, thêm cụm kích hoạt "sách có lệch web không",
"xuất sách ra Word", "in sách chương X lớp Y".

## 4. Thứ tự cài đặt (mỗi chặng một commit, kiểm được độc lập)

| Chặng | Việc | Kiểm xong khi |
|---|---|---|
| A | Hồ sơ sách, bỏ viết cứng trong `build.py`/`front.py`/`make.py` | Dựng lại L10 Ch.2 ra đúng 124 trang, chữ trích từ PDF trùng bản v6 |
| B | `lay-noi-dung.mts`, cache, sổ khoá, `sach.py lech` | Sửa thử 1 chữ trong cache → báo "chữ"; thêm 1 Dạng → báo "đánh số" |
| C | Số bản trong QR + `dap-an-<lid>-b<n>.json` + `trang-<mã>.json` + nhãn ở chế độ trình chiếu | QR cũ (không `b`) vẫn mở được; nhãn trang khớp PDF |
| D | `word.py` + `mau.docx` | Số phương trình OMML khớp; thầy mở trên Word thật |
| E | Viết lại `SKILL.md`, tách `RUOT-TAP.md`, dòng nhắc trong `cap-nhat-ly-thuyet.sh` | Chạy skill trọn một lượt cho L11 Ch.2 Sóng (cuốn thứ hai) |

Không cần migration: mọi thứ là file tĩnh và đọc DB.

## 5. Việc thầy cần quyết trước chặng C–D
1. Nhãn "Sách tr. X" cho **học sinh** (giai đoạn 2) có làm không, hay chỉ ở chế độ trình chiếu của thầy.
2. Bản Word theo trang mẫu nào (`sach_mau.py` của thầy hay giữ kiểu chữ của PDF hiện tại).
3. Cuốn thứ hai để thử chặng E: L11 Ch.2 Sóng (đã có nhánh thử trong code) hay chương khác.
