# Tự đăng đề từ file Word — không cần trợ lý

Trang **Quản trị → Nhập bài học** (`/quan-tri/nhap-bai`) đọc thẳng file `.docx` ngay trong trình
duyệt: tách câu, lấy đáp án, đổi công thức sang LaTeX, gom ảnh. Không có gì gửi đi đâu cả —
file chỉ nằm trong máy thầy cho tới lúc bấm **Đăng bài học**.

## Làm một lần trong Word

1. **Công thức MathType → Office Math.** Mở file → tab **MathType** → **Convert Equations** →
   mục *Convert equations to* chọn **Microsoft Office Math** → OK → lưu lại.
   Công thức gõ bằng Word (`Alt` + `=`) thì bỏ qua bước này.
   *Vì sao cần:* MathType lưu công thức dạng OLE + ảnh WMF, trình duyệt không đọc được. Chỗ nào
   còn sót, trang sẽ hiện mốc `⟦CT⟧` và báo số lượng để thầy biết mà quay lại chuyển.
2. **Đánh dấu đáp án đúng** bằng dấu `*` ngay trước phương án — kiểu Azota:

   ```
   Câu 1. Tốc độ trung bình được tính bằng
   A. v = s.t     *B. v = s/t     C. v = t/s     D. v = s + t
   Lời giải: Tốc độ trung bình bằng quãng đường chia thời gian.
   ```

   Không có dấu `*` thì viết dòng `Đáp án: B`. Câu đúng–sai: đánh `*` ở các ý Đúng
   (`*a) …`, `*c) …`). Câu trả lời ngắn: `Đáp án: 2,5`.
3. **Số câu phải là chữ gõ tay** (`Câu 1.`, `Câu 2.`), không dùng đánh số tự động của Word —
   số tự động không nằm trong nội dung file nên trang không thấy.
4. **Hình vẽ để dạng PNG/JPG.** Ảnh WMF/EMF web không hiện được (chuột phải ảnh →
   *Save as Picture* → PNG → chèn lại).

Có sẵn "PHẦN I / PHẦN II / PHẦN III" thì trang tự hiểu loại câu (trắc nghiệm · đúng–sai ·
trả lời ngắn). Không có phần nào thì coi cả đề là trắc nghiệm A–D.

## Trên web

1. Vào `/quan-tri/nhap-bai`, mục **1** chọn Lớp → Môn → Chương → Bài.
2. Mục **2**, tab **Từ file Word (.docx)**, kéo file vào. Trang báo đọc được bao nhiêu câu trên
   tổng số mốc "Câu n.", bao nhiêu công thức, bao nhiêu ảnh; phần ghi chú màu vàng nói rõ chỗ nào
   còn thiếu.
3. Mục **3** bấm **Sửa từng câu**: câu nào thiếu đáp án / thiếu phương án / thiếu lời giải sẽ có
   viền vàng. Sửa tại chỗ, gõ công thức trong `$…$`, bấm hình con mắt để xem đúng như học sinh
   thấy. Có thể đổi loại câu, thêm/xóa/đảo thứ tự câu, điền **chủ đề** cho từng câu (dùng cho
   thống kê chỗ hổng và nút "Ôn lại").
4. Mục **4** tick **Kiểm tra** (có tính giờ, vào bảng điểm) hoặc **Luyện tập** (học sinh tự làm,
   xem đáp án ngay). Bài đã có đề cũ thì chọn **Thay** / **Giữ + thêm**.
5. Bấm **Đăng bài học**, rồi mở link bài học hiện ra để kiểm tra lại.

Gói đề nhập từ Word không đụng tới mục **Lý thuyết** và **Các dạng bài tập** của bài — nội dung
cũ ở đó được giữ nguyên.

## Khi nào vẫn cần trợ lý

- Đề chỉ có bản **PDF** hoặc ảnh chụp/scan.
- Không chuyển được MathType sang Office Math.
- Cần **vẽ lại hình** (đồ thị, sơ đồ mạch) thành hình véc-tơ, hoặc cần viết lời giải cho nhiều
  câu còn trống.

## Kiểm thử

Bộ đọc file Word có kiểm thử chạy trong Chromium thật (vì dùng `DOMParser` và
`DecompressionStream` của trình duyệt):

```bash
npm i --no-save playwright
node scripts/tests/docx-import.mjs
```

Chạy trên máy đã có sẵn Chromium của Playwright thì đặt `CHROMIUM_PATH` trỏ tới file chrome.
