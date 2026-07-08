# Hướng dẫn nhúng AZOTA vào ThachLab

## 📋 Tổng quan

AZOTA Integration cho phép bạn nhúng bài tập/đề kiểm tra trực tiếp từ **azota.vn** vào ThachLab mà không cần copy dữ liệu.

## 🚀 Các chỗ có thể nhúng AZOTA

### 1. **Nội dung bài học**
   - Quản trị → Bài học → Chọn chương → Soạn mục
   - Loại mục: "Lý thuyết", "Video", v.v.
   - Tab **🔗 AZOTA** → Dán iframe code

### 2. **Câu hỏi trong đề kiểm tra**
   - Quản trị → Đề kiểm tra → Tạo/sửa đề
   - Cho mỗi câu hỏi: Tab **🔗 AZOTA**
   - Dán iframe code của câu hỏi AZOTA

## 📝 Cách lấy iframe từ AZOTA

### Bước 1: Vào AZOTA
Truy cập [azota.vn](https://azota.vn)

### Bước 2: Tìm bài tập hoặc tạo bài tập
- Tìm kiếm bài tập có sẵn
- Hoặc tạo bài tập mới

### Bước 3: Lấy iframe code

**Cách A: Nếu AZOTA có nút "Chia sẻ" hoặc "Embed"**
- Click nút đó
- Tìm option "Nhúng iframe" hoặc "HTML code"
- Copy code iframe

**Cách B: Từ URL của bài tập**
Nếu URL là: `https://azota.vn/de-thi/ezkjlr`

Tạo iframe như sau:
```html
<iframe
  width="100%"
  height="900"
  src="https://azota.vn/de-thi/ezkjlr"
  title="Tên bài tập"
  frameborder="0"
  allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture"
  allowfullscreen>
</iframe>
```

### Bước 4: Dán vào ThachLab

**Trong form soạn bài học hoặc câu hỏi:**

1. Chọn tab **🔗 AZOTA**
2. Dán iframe code vào textarea
3. Xem preview (nếu cần)
4. Click **✓ Nhúng AZOTA**

## ✅ Ví dụ

### Ví dụ 1: Nhúng bài tập vào nội dung bài học

```html
<iframe
  width="100%"
  height="900"
  src="https://azota.vn/de-thi/abc123"
  title="Bài tập về lực"
  frameborder="0"
  allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture"
  allowfullscreen>
</iframe>
```

**Kết quả:** Bài tập AZOTA được nhúng trong bài học, học sinh có thể làm trực tiếp.

### Ví dụ 2: Nhúng câu hỏi AZOTA vào đề kiểm tra

Tương tự, khi thêm câu hỏi vào đề:
- Chọn loại "Trắc nghiệm", "Đúng/Sai", v.v.
- Tab **🔗 AZOTA** → Dán iframe

## 🎨 Styling tự động

Khi nhúng AZOTA, ThachLab tự động:
- ✅ Resize responsive (chiều rộng 100%, chiều cao 900px)
- ✅ Add border và styling
- ✅ Cho phép fullscreen
- ✅ Enable các tính năng (clipboard, gyroscope, v.v.)

HTML được tạo tự động:
```html
<div class="azota-embed w-full bg-white rounded-lg overflow-hidden" data-src="...">
  <iframe width="100%" height="900" src="..." ...></iframe>
</div>
```

## ❓ FAQ

**Q: Khi nhúng AZOTA, dữ liệu có được copy vào ThachLab không?**
A: Không, chỉ lưu iframe (link). Khi học sinh xem, sẽ fetch từ azota.vn trực tiếp.

**Q: Nếu AZOTA down, học sinh có thể làm bài không?**
A: Không, vì dữ liệu ở AZOTA. Nên backup bài tập nếu sợ downtime.

**Q: Có thể nhúng YouTube, Google Forms, v.v. không?**
A: Hiện tại component chỉ validate azota.vn. Có thể mở rộng sau nếu cần.

**Q: Làm sao để edit bài tập AZOTA đã nhúng?**
A: 
1. Sửa bài tập gốc trên azota.vn
2. Hoặc replace iframe code bằng code mới

**Q: Iframe không load trong preview?**
A: 
- Kiểm tra link azota.vn có đúng không
- Thử mở link trực tiếp trong browser
- Có thể AZOTA không cho phép embed từ localhost (dev), nhưng hoạt động trên prod

## 🔧 Kỹ thuật

### Validation
- ✓ URL phải từ azota.vn
- ✓ Iframe phải có src attribute
- ✓ Tự động trim whitespace

### Lưu trữ
- HTML iframe được lưu vào `body_html` (nội dung bài học)
- Hoặc `question` field (câu hỏi đề thi)
- LaTeX gốc không được lưu (chỉ HTML)

### Render
- Khi hiển thị, iframe tự động embed và load từ azota.vn
- Responsive design tự động
- Không cần plugin thêm

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra iframe code có đúng syntax không
2. Thử mở link azota.vn trực tiếp
3. Đảm bảo URL từ azota.vn chứ không phải site khác
