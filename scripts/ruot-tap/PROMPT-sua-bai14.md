# Prompt: sửa ruột tập Vật lí 12 – Bài 14 theo góp ý học sinh (giao Sonnet)

Sửa file `scripts/ruot-tap/bai14.mjs` (script dựng PDF ruột tập 165×240 mm, ô ly 5 mm, chạy
`node scripts/ruot-tap/bai14.mjs`, ra `scripts/ruot-tap/out/ruot-tap-vl12-bai14.pdf`; cần `book/node_modules`,
worktree không có thì script tự dùng `~/Projects/thachlab/book`). Bài web tương ứng:
`content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/theory.src.html` (các thẻ `data-tap` là mã ô trong tập;
`components/lessons/LessonPresenter.tsx` hiện nhãn "✍ Tập: trang · ô" từ mã đó khi trình chiếu).
Đọc `docs/QUY-TAC-THIET-KE.md` mục N1, L4 trước. Không đụng file khác ngoài hai file nêu ở bước 1 và 7.

## Phải làm (theo thứ tự ưu tiên)

1. **Đổi thứ tự trang 3 và 4** cho đúng thứ tự web III Bẫy → IV Trả bài → V Bài toán mẫu: trang 3 = Bẫy + Trả bài,
   trang 4 = Bài toán mẫu. Cập nhật số trang ở `foot()` và các thẻ `tag()`. Sau đó đổi `data-tap` trong
   `theory.src.html`: `III` → `3.1`, `IV` → `3.2`, `V` → `4`; build lại `theory.html`/`bundle.json` bằng
   `python3 content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/build_bundle.py` (xem file đó trước khi chạy).
   Không ghi DB.
2. **Thêm bảng "Kết quả tự kiểm tra"** (đặt ở trang 2, thay/ghép với mục "Ghi chú thêm của em"): cột
   `Câu | Em chọn | Chắc? (☐) | Đúng? (☐)`, 7 hàng cho câu 1–7 trên web, mỗi hàng cao 1 ô ly (5 mm). Câu 1 đã có
   ô riêng ở II.1 thì vẫn giữ.
3. **Mở rộng chỗ viết**: Trả bài câu 3 và câu 4 → 3 dòng mỗi câu (câu 1, 2, 5 giữ 2 dòng); Bài mẫu a) và b) → 3
   dòng mỗi câu; bảng Thomson/Rutherford/Bohr → ô cao ≥ 25 mm (5 ô ly) để vẽ được hình; "Ghi chú thêm" nếu còn giữ
   thì ≥ 4 dòng. Chỗ trống dưới mã QR dùng cho mục 4 và 5 dưới đây.
4. **Thêm ô "Mang về" 8 dòng** (tiêu đề "Mang về · chép tóm tắt cuối bài") ở trang có mã QR, 8 dòng kẻ chấm.
5. **Thêm chỗ "Điền bước còn thiếu"** sau câu d) của bài mẫu: hai dòng gắn nhãn "Bước 2: m(Cu) = 63,54 / N_A = …" và
   "Bước 3: đổi sang u = …", mỗi nhãn 2 dòng viết.
6. **Nhãn ô to và thống nhất**: thẻ `tag()` cỡ chữ ≥ 3,2 mm, nền navy chữ trắng, nằm trong khung chứ không đè mép;
   nội dung dạng `Web II.1`, `Web III`, `Web V` (tên mục trên web) thay cho "ô 1"/"trang 3". Mã `data-tap` vẫn giữ
   dạng số như bước 1.
7. **Bỏ đáp án lộ**: dòng `A (trên) = số ___ (prôtôn + nơtron)` → `A (trên) = số ___ = ___ + ___`.
8. **Ô điền số**: dòng `1 u ≈ ___ kg ≈ ___ MeV/c²` và `1 MeV = ___ J` tách thành 2 dòng, mỗi `.fill` ≥ 22 mm; chỗ điền
   trong 5 cụm từ khoá ≥ 18 mm.
9. **Ô tick** `.ck` 4,8 mm; **mã QR** 25 mm, viền trắng 2 mm quanh (quiet zone), vẫn trỏ `LINK` hiện có.

## Ràng buộc

- Giữ đúng 4 trang, mỗi trang không tràn (`overflow:hidden` đang che lỗi tràn, phải kiểm bằng mắt).
- Mã ô trên giấy ↔ `data-tap` trên web phải khớp từng mục sau khi đổi; liệt kê bảng đối chiếu trong báo cáo.
- Không đổi nội dung vật lí, không thêm câu hỏi mới ngoài bảng kết quả ở mục 2.

## Kiểm tra trước khi báo xong

1. `node scripts/ruot-tap/bai14.mjs` chạy không lỗi; `pdftoppm -r 110 -png` 4 trang ra `scripts/ruot-tap/out/xem-thu/`
   rồi xem từng ảnh: không chữ chồng, không tràn trang, chỗ viết đúng số dòng ở trên.
2. `npx tsx scripts/ruot-tap/giai-ma-qr.mts scripts/ruot-tap/out/ruot-tap-vl12-bai14.pdf` (hoặc cách giải mã QR sẵn
   trong file đó) ra đúng `LINK`.
3. Mở trình chiếu bài 14 (`/lop-hoc/bai/?id=15`, nút Trình chiếu) xem nhãn ✍ khớp số trang mới.
4. Commit đúng hai đường dẫn: `git commit -- scripts/ruot-tap/bai14.mjs content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/`
   với mô tả ghi mã quy tắc (N1, L4). Báo: số dòng viết từng mục trước/sau, bảng đối chiếu mã ô, ảnh xem thử.
