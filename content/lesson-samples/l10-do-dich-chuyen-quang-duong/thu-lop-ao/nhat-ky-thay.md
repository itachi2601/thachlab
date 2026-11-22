# Nhật ký thầy — chạy thử bài 4 Độ dịch chuyển và quãng đường đi được với học sinh ảo

Nguồn đối chiếu: `../tren-lop.src.html` (26 màn), `../tren-lop-ghi-chu.html`, `scripts/ruot-tap/l10-bai4.mjs` (p1–p5). Số chỗ trống trong `sach-trong.md`: [__1__]…[__118__]. Mã ô là số trang tuyệt đối 1–5.

## Soát trước giờ (đọc ba tài liệu, chưa dạy)

- **Màn clip ray uốn, bước 10.2 "Đo bốn hình ray: điền cột $d$":** Tập chỉ để trống MỘT ô (d nửa vòng, [__51__]); ba ô d còn lại in sẵn (30,0 · 49,9 · 0,0). Màn bảo "điền cột d" nghe như bốn ô. Sửa chữ thành "điền ô ? (d nửa vòng)".
- **Hai số cho cùng một đại lượng:** d nửa vòng đo = 20,1 (ô [__51__]) rồi d tính = 20 (ô [__53__], màn 4c). Học sinh dễ viết 20,1 vào cả hai hoặc thắc mắc. Thầy phải nói "đo ≠ tính".
- **Màn 4c lộ đáp án câu hỏi mở:** Tập hỏi sẵn "Vì sao cột $s$ lệch nhiều hơn cột $d$?" ([__58__]) còn màn hỏi "cột $s$ hay $d$ lệch nhiều hơn?". Tập đã chọn sẵn vế trả lời, màn 4c hết ý nghĩa câu hỏi mở.
- **Ô "Rút ra" [__56__] "chỉ ray ___ cho $d\approx s$":** chữ "thẳng" chỉ xuất hiện ở bước cuối clip (27,5 s), màn 4c không có. Nếu bỏ clip (ghi chú dạy cho phép khi thiếu giờ) thì ô này không có nguồn điền.
- **Trùng tên màn "Quay lại sân băng":** màn 1b dặn "Đáp án: cuối tiết (màn 'Quay lại sân băng')", nhưng có HAI màn tên đó: 5b (tr.3 ô 3·2, tính $d=0$, $v_{\mathrm{tb}}=3$ m/s) và 6d (tr.1 ô 1·3). Lớp tìm đáp án ở 5b.
- **Màn 5b làm hỏng "cuối giờ quay lại":** 5b công bố $d=0$ cho một vòng sân băng 21 phút trước 6d; học sinh suy ra phương án C, D sai ngay ở điểm dừng 5, 6d chỉ còn xác nhận. Đổi số liệu 5b (ví dụ vòng khác) hoặc bỏ ý "bất ngờ" ở 6d.
- **Nhãn lộ đáp án biểu quyết (clip):** màn 4b bước 21.0 có `data-dung` ở dòng đáp án; đã kiểm, chữ "Đáp án B" chỉ hiện khi tới 21.0, không lộ trước. Nhưng bước 10.2 (hiện 0,1 s sau câu hỏi dừng ①) cùng khung với A–D nên không được che.
- **Nút Mở bẫy 1 (màn 5c):** `li[data-dung]` được tô chỉ khi bấm "Mở: đáp án" (JS gắn theo `id` bắt đầu bằng `a`/`r`); ổn. Ghi chú cho thầy: đừng đặt `id` mới bắt đầu bằng "a" hoặc "r" trong màn có A–D.
- **Phương án dùng khái niệm chưa dạy:** màn 5c phương án D "đường đèo uốn lượn lên dốc" và mục tiêu 1·1 "toạ độ", "hai hướng vuông góc" (ô [__4__]) dùng khái niệm trước khi dạy; màn 1b phương án D "nửa vòng, 30 m" dùng "nửa vòng" mà chưa vẽ hình (hình sân băng trên màn 1a không có đánh dấu nửa vòng).
- **Thứ tự lật Tập** (ghi chú): tr.1 → 2 → 3 → 4 → 1 (ô 1·3) → 3 (ô 3·4) → 5. Bảng ghi chú ghi "tr.4 → tr.1" ở đầu mục nhưng bỏ bước cuối tr.3 ô 3·4; tổng lật 7 lần trong 45 phút. Ô 4·2 (bài mẫu) dạy TRƯỚC ô 4·1 (trả bài) dù ô 4·1 nằm trước trên trang giấy; thầy phải bảo "xuống ô 4·2 trước".
- **Ô điền mà màn không hề nhắc:** 1·1 (mục tiêu, 4 ô ☐; chỉ nhắc ở màn 6f), ☐ chắc/không chắc ([__6__]), ☐ cuối mỗi câu 4·1 ([__79__] …), ô "Bạn cùng bàn kiểm" ([__91__]–[__93__]), ba ô ☐ đầu mỗi bẫy 3·3 ([__67__] [__70__] [__73__]), ô BTVN 5·1 ([__102__]–[__109__]; chỉ có dòng ở màn 6f, không có màn giao đề), ô "câu sai", "câu đoán mò" ([__77__] [__78__]).
- **Mã ô "dòng 1–5…" trên màn** (2a, 2b, 2c, 2d, 2e, 3a) trong khi Tập không đánh số dòng trong ô; học sinh phải đếm dòng trong ô 1·4 (6 dòng), 2·1 (5 dòng), 2·2 (6 dòng).
- **Số câu trả bài:** Tập ô 4·1 có 6 câu, màn 6c chỉ chiếu câu 5 và 6 (đúng ý ghi chú "câu 1–4 về nhà"); nhưng câu 6 chỉ có 1 dòng kẻ mà đáp án có 3 ý ($v_{\mathrm{tb}}=s/t$, không âm, vòng kín $d=0$, $v_{\mathrm{tb}}\gt 0$) và câu 5 có 4 ý trong 2 dòng.
- **Điểm dừng dồn nhiều ô:** ĐD2: 21 chỗ ([__11__]–[__31__]) trong 6 phút, 5 màn. ĐD3: 19 chỗ ([__32__]–[__50__]) trong 7 phút. ĐD5: 17 chỗ ([__59__]–[__75__]) trong 5 phút, 5 màn. ĐD6: 26–30 phút gồm 6a, 6b, 6c, 6d (4 phút, màn 6c và 6d cùng ghi "phút 29–30") cho 8 + 8 + 3 chỗ trước khi chiếu QR. Ghi chú đã tự nhận ĐD2 và ĐD6; ĐD5 cũng chật.
- **Ô 3·4 và 5·1 tr.3/5:** đề 1225 19 câu nhưng chưa kiểm trên web (ghi chú dạy); ô "Câu sai" [__77__] chỉ 30 mm, không đủ ghi nhiều số câu.
- **Hình đáp án bài mẫu:** Tập tr.4 in sẵn hình đạp xe có mũi tên độ dịch chuyển và góc $\alpha$ ngay cạnh các ô giải, trong khi màn 6b giấu hình tới khi bấm "Mở: $\alpha$ và $v_{\mathrm{tb}}$". Học sinh nhìn được hướng của $\vec d$ trước khi tự tính.

## ĐD1 · Dự đoán sân băng (phút 0–3, ô 1·2)
- (Ghi tiếp ở các lượt sau.)

## ĐD2
- (Ghi tiếp ở các lượt sau.)

## ĐD3
- (Ghi tiếp ở các lượt sau.)

## ĐD4
- (Ghi tiếp ở các lượt sau.)

## ĐD5
- (Ghi tiếp ở các lượt sau.)

## ĐD6
- (Ghi tiếp ở các lượt sau.)
