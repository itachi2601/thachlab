# Rà soát hình trong Bài tập mẫu — L12 Ch.3 Từ trường (5/11/2026)

Phạm vi: 7 bài (lesson 10, 11, 13, 14, 125, 126, 127), 35 dạng, dữ liệu `scripts/data/bai-tap-mau/<id>.json`.
Đã xem bằng mắt ở 375px (`/dev/btm`) bài 10 · Dạng 3; các dạng khác rà từ JSON (chú thích, `aria-label`, `cong_cu`).

## 1. Hiện trạng: một dạng có tới BA hình, vẽ bằng ba "ngôn ngữ"

| Chỗ hiện | Nguồn | Vẽ bằng | Lúc soạn |
|---|---|---|---|
| ① Mô phỏng dưới đề | `problem_html` (SVG + SMIL, nút ▶) | `hinh.py` trong `build-hinh-<id>.py` | 10/2026 (`soan-bai-tap-mau`) |
| ② Hình dữ kiện trong "Phân tích đề" | `analysis_html` | `hinh.py` | 10/2026 |
| ③ Hình giải cùng bước (dính trên, thêm lớp) | `cong_cu` | component React (`TuTruong.tsx`, `DoThi.tsx`…) | 11/2026 (`cap-nhat-dang-bai-tap`) |

Ví dụ đã chụp — **bài 10 · Dạng 3 (la bàn dưới dây)**:
- ① la bàn tròn nhìn từ trên, dây cam dọc, kim đỏ lệch 37°, $B_đ$ xanh ở góc;
- ② ba vectơ thành hình chữ nhật ($B_đ$ xanh, $B_{dây}$ cam, $B$ đỏ), không có la bàn;
- ③ trục đen nét đứt, "Bđ (bắc)" màu đen chữ thường, mũi tên I cam nhỏ, chữ Tây/Đông — không la bàn, không cùng màu với ① ②.

Học sinh phải tự ghép ba hình khác hướng nhìn, khác màu, khác nhãn → tách chú ý (N8) và lặp thông tin (N4).

## 2. Nguyên nhân
1. Ba hình ra đời ở hai đợt, hai công cụ, không có toạ độ/màu/nhãn chung.
2. Quy tắc chống lộ đáp án (nhật ký `soan-bai-tap-mau`: "chưa vẽ lực", "trục không ghi số", "số liệu hình khác đề", "không đúng tỉ lệ") khiến mô phỏng bị rút hết thông tin → còn lại chuyển động diễn lại dữ kiện đề đã cho.
3. Mô phỏng soạn trước lời giải từng bước, không ai hỏi "bước nào dùng hình này" (H1).
4. 23/35 dạng KHÔNG có `cong_cu` → lúc giải từng bước không có hình, phải cuộn lên ① hoặc ② (N8).

## 3. Đánh giá từng dạng

Cột "Mô phỏng ①": **Có ích** = cho thấy điều HS cần hình dung để làm một bước mà hình tĩnh khó cho; **Trang trí** = chỉ diễn lại dữ kiện đề đã ghi bằng chữ, hoặc bị cắt hết thông tin.

| Dạng | Mô phỏng ① | Bước dùng được / lý do | Có ③ |
|---|---|---|---|
| 10·D1 từ phổ thanh nam châm | Có ích | câu c (mạt sắt ≠ đường sức), so sánh A–B | — |
| 10·D2 từ phổ dây thẳng | Có ích | vòng đồng tâm, thưa dần → so sánh B và C | — |
| 10·D3 la bàn, 1 dây | Trang trí | kim dừng ở 37° đề đã cho; ③ khác hẳn ① | ✓ |
| 10·D4 la bàn, 2 dây | Trang trí | như D3 | ✓ |
| 11·D1 bàn tay trái | Trang trí | điện tích chạy theo chiều I đề đã nói, "chưa vẽ lực" | — |
| 11·D2 bài ngược bàn tay trái | Nửa vời | dây "bị đẩy nhẹ" = chiều F đề đã cho; giữ hình tĩnh là đủ | — |
| 11·D3 F = BIl sinα | Có ích | dây quay α 0→90° thấy F phụ thuộc góc | — |
| 11·D4 tìm B từ F đo được | Trang trí | điểm chạy tới (2,5 A; 15 mN) đề đã cho | — |
| 11·D5 dây cân bằng | Trang trí | kim ampe kế quay, thang không số | ✓ |
| 11·D6 khung dây, mômen | Có ích | khung quay đổi góc pháp tuyến | ✓ |
| 13·D1 từ thông, góc pháp tuyến | Có ích | quay tới vị trí đề → chỗ khó nhất là góc α | — |
| 13·D2 Lenz | Có ích | B tăng (⊗ dày dần) → từ thông tăng | — |
| 13·D3 suất điện động khi B đổi | Trang trí | B giảm 0,50→0,20 T đề đã cho | — |
| 13·D4 cuộn N vòng quay | Có ích | như 13·D1 | ✓ |
| 13·D5 đồ thị Φ–t | Trang trí | điểm chạy trên đồ thị đã đủ đọc | ✓ |
| 14·D1 đọc biểu thức u | Trang trí | điểm chạy, trục không số | — |
| 14·D2 công suất trên R | Trang trí | điểm chạy + điện trở sáng | — |
| 14·D3 viết biểu thức i | Trang trí | điểm chạy, trục không số | — |
| 14·D4 khung quay: Φ và e | Có ích | khung quay ↔ Φ(t) | ✓ |
| 14·D5 thời gian đèn sáng | Có ích | đèn sáng khi \|u\| vượt ngưỡng | ✓ |
| 125·D1 f = np | Có ích | rô-to nhiều cặp cực quét qua cuộn | — |
| 125·D2 E₀ của khung quay | Có ích | khung quay ↔ e(t) (trùng ý 14·D4) | — |
| 125·D3 máy biến áp lí tưởng | Trang trí | lõi đậm nhạt, không dùng ở bước nào | — |
| 125·D4 hao phí truyền tải | Trang trí | hạt dao động, dây sáng | ✓ |
| 125·D5 máy tăng áp | Trang trí | như D4 | ✓ |
| 126·D1 ghi ta điện | Có ích | dây dao động → từ thông biến thiên | ✓ |
| 126·D2 sạc không dây | Trang trí | mũi tên đổi chiều | — |
| 126·D3 dòng Foucault | Có ích | so 4 tình huống có/không đổi từ thông | — |
| 126·D4 bếp từ | Trang trí | mũi tên đổi chiều, bài chủ yếu tính nhiệt | — |
| 127·D1 điện trường xoáy | Có ích | nam châm chạy/dừng ↔ kim lệch/về 0 | — |
| 127·D2 λ, T, f | Trang trí | sóng FM chạy | — |
| 127·D3 E, B cùng pha | Có ích | hai điểm cùng lên cùng xuống | — |
| 127·D4 đổi môi trường | **Gây hiểu sai** | chú thích tự nhận "tỉ lệ hai bước sóng không đúng với đề" | — |
| 127·D5 xung tới Mặt Trăng | Trang trí | xung đi–về | — |
| 127·D6 thời điểm E = 0 / cực đại | Có ích | M dao động (nên chuyển sang vòng tròn pha của ③) | ✓ |

Tổng: **16 có ích · 17 trang trí · 1 nửa vời · 1 gây hiểu sai**; 12/35 dạng có ③, 23 dạng giải từng bước không có hình.

## 4. Đề xuất: "Một dạng — một hình"
1. **Hình gốc duy nhất = `cong_cu`.** Dưới đề hiện lớp nền của chính hình ③ (tĩnh, có số liệu đề) thay cho ①; "Phân tích đề" chỉ còn bảng (bỏ ②). Khi bấm "Giải từng bước", cùng hình đó dính trên và thêm lớp theo bước — HS nhìn một hình từ đầu tới cuối (N8, N4).
2. **Chuyển động chỉ giữ ở 16 dạng "có ích"**, và chạy TRÊN hình gốc (thêm khoá `dong` vào `cong_cu`: quay một nhóm tới góc, điểm chạy trên đồ thị, mũi tên đổi chiều), gắn vào đúng bước dùng nó, bấm mới chạy, ≤ 2 lượt (H1, V10, B4).
3. **Bỏ 17 mô phỏng trang trí + 11·D2 chuyển động**; 127·D4 vẽ lại đúng tỉ lệ hoặc bỏ.
4. **Bổ sung `cong_cu` cho 23 dạng thiếu** bằng họ có sẵn (`tu_truong`, `do_thi`, `vong_tron`, `mach_dien`).
5. **Một quy ước màu cho cả chương** (giữ quy ước đang có ở ①②): B xanh dương, I cam, F đỏ, pháp tuyến/hình học đen; nhãn dùng chỉ số thật ($B_đ$, không "Bđ").
6. **Kiểm**: mỗi hình/lớp phải trả lời "dùng ở bước số mấy"; HS ảo 375px bấm hết bước; so ảnh trước/sau.

Đo hiệu quả: tỉ lệ dạng mở tới bước cuối, số lần cuộn ngược lên đề trong lúc giải (nếu có log), phản hồi Báo lỗi.

Thứ tự làm: (a) code — `cong_cu` hiện dưới đề + khoá `dong` (một phiên); (b) chương Từ trường 35 dạng (soạn hình cho 23 dạng, gỡ ①②, gắn `dong` 16 dạng); (c) thầy duyệt ở `/dev/btm` → đăng → nhân ra các chương khác theo cùng bảng đánh giá.

## 5. Trạng thái (5/11/2026, cuối phiên)
Đã làm đủ 6 điểm trên nhánh `claude/sync-simulation-images-b9910d`: code (`cong_cu.de`, `cong_cu.dong`, mục mới của `tu_truong`/`do_thi`, trang soát `/dev/btm-hinh`) + 35/35 dạng có một hình, `#kiem` SACH cả 7 bài, đã xem 375px. **CHƯA đăng DB, chưa deploy** — chờ thầy duyệt ở `/dev/btm/?f=btm-<id>` (chạy `npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --xem-thu` trước), rồi publish 7 bài `--giu-cu --yes` + deploy.
Chờ thầy quyết: 13·D2 thanh "độ lớn B" (ký hiệu tự đặt) giữ hay bỏ `dong`; 126·D3 tấm Foucault nhìn cạnh nên dòng xoáy/rãnh chỉ có trong chữ; 14·D5 điểm chạy hết một chu kì rồi nhảy về t = 0.
Còn thiếu mục hình: `mach_dien` nguồn xoay chiều/cuộn dây/lõi thép, `tu_truong` hình chữ nhật tô màu + vòng dòng xoáy (đang vẽ gần đúng bằng `duong`/`elip`).
