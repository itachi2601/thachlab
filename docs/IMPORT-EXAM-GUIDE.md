# Hướng dẫn Import Đề Kiểm Tra

## 📋 Tổng quan

Import Đề cho phép bạn tạo đề kiểm tra bằng 2 cách:

1. **📐 LaTeX Format** - Viết structured LaTeX, auto-parse từng câu hỏi
2. **🔗 AZOTA Embed** - Nhúng toàn bộ đề từ azota.vn

## 🚀 Cách sử dụng

### 1. LaTeX Format (Parse từng câu)

**Vào: Quản trị → Import Đề → Tab 📐 LaTeX**

#### Định dạng:

```latex
\section{Đề kiểm tra Vật lý 10}

\question{Loại: multiple_choice}
Câu hỏi thứ nhất?
A) Đáp án A
B) Đáp án B
C) Đáp án C
D) Đáp án D
\answer{A}
\explanation{Giải thích tại sao A đúng}

\question{Loại: true_false}
Câu hỏi thứ hai
a) Ý 1 - ĐÚNG/SAI
b) Ý 2 - ĐÚNG/SAI
c) Ý 3 - ĐÚNG/SAI
d) Ý 4 - ĐÚNG/SAI
\answer{a, c}
\explanation{Ý a và c đúng vì...}

\question{Loại: short_answer}
Tính kết quả?
\answer{5 m/s²}
\explanation{Công thức: a = F/m = 10/2 = 5}
```

#### Loại câu hỏi:

| Loại | Cú pháp | Mô tả |
|------|---------|-------|
| Trắc nghiệm | `multiple_choice` / `trắc nghiệm` / `A/B/C/D` | 4 option A/B/C/D |
| Đúng/Sai | `true_false` / `đúng/sai` / `4 ý` | 4 ý a/b/c/d, chọn đúng |
| Trả lời ngắn | `short_answer` (mặc định) | Nhập văn bản |

#### Cấu trúc chi tiết:

**Bắt đầu đề:**
```latex
\section{Tên đề kiểm tra}
```

**Bắt đầu câu hỏi:**
```latex
\question{Loại: [loại câu hỏi]}
[Nội dung câu hỏi + options]
\answer{[đáp án]}
\explanation{[giải thích]}
```

**Câu trắc nghiệm (A/B/C/D):**
```
A) Option A
B) Option B
C) Option C
D) Option D
\answer{B}
```

**Câu đúng/sai (a/b/c/d):**
```
a) Statement 1
b) Statement 2
c) Statement 3
d) Statement 4
\answer{b, d}
```

**Câu trả lời ngắn:**
```
Câu hỏi?
\answer{câu trả lời}
```

#### Bước thực hiện:

1. Dán LaTeX format vào textarea
2. Click **✓ Parse LaTeX**
3. Xem preview (số câu, cảnh báo)
4. Click **Xem trước & chỉnh sửa** → ExamEditor
5. Edit, chọn lớp, publish

### 2. AZOTA Embed (Toàn bộ đề)

**Vào: Quản trị → Import Đề → Tab 🔗 AZOTA**

#### Định dạng:

Paste iframe code từ AZOTA:

```html
<iframe width="100%" height="900" src="https://azota.vn/de-thi/ezkjlr" title="[26-27] 12 KTTX tuần 1" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe>
```

#### Bước thực hiện:

1. Vào azota.vn → Tìm bài tập/đề
2. Click "Chia sẻ" → Copy iframe code
3. Paste vào textarea
4. Click **✓ Nhúng AZOTA**
5. Xem preview iframe
6. Click **Xem trước & chỉnh sửa** → ExamEditor
7. Chỉnh sửa tiêu đề, chọn lớp, publish

#### Khi publish AZOTA:

- Toàn bộ đề nhúng từ AZOTA
- Học sinh làm trực tiếp trên AZOTA
- Không có câu hỏi riêng trong ThachLab

## 📝 Ví dụ đầy đủ

### Ví dụ 1: Mix câu hỏi

```latex
\section{Kiểm tra giữa kỳ Vật lý 10 - Chuyên động}

\question{Loại: multiple_choice}
Một vật rơi tự do từ độ cao 20m. Tính vận tốc khi chạm đất? (g=10 m/s²)
A) 10 m/s
B) 20 m/s
C) 30 m/s
D) 40 m/s
\answer{B}
\explanation{Công thức: v² = 2gh → v = √(2×10×20) = 20 m/s}

\question{Loại: true_false}
Xác định đúng (Đ) / sai (S):
a) Gia tốc của vật rơi tự do là 10 m/s²
b) Quãng đường rơi tỉ lệ với thời gian
c) Vận tốc tăng đều theo thời gian
d) Vật nặng rơi nhanh hơn vật nhẹ
\answer{a, c}
\explanation{a-Đ (g=10), b-S (tỉ lệ với t²), c-Đ (v=gt), d-S (môi trường không khí)}

\question{Loại: short_answer}
Một vật được ném ngang từ độ cao 5m với vận tốc 10 m/s. Tính thời gian rơi?
\answer{1 s}
\explanation{h = ½gt² → 5 = ½×10×t² → t = 1s}
```

### Ví dụ 2: AZOTA embed

```
<iframe width="100%" height="900" src="https://azota.vn/de-thi/xyz123" title="Kiểm tra tuần 1" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe>
```

## ⚠️ Cảnh báo & Lỗi

### LaTeX Parse

| Lỗi | Giải pháp |
|-----|-----------|
| "Không tìm thấy câu hỏi" | Kiểm tra format `\question{Loại: ...}` |
| "Trắc nghiệm phải có 4 option" | Thêm A/B/C/D đủ 4 ý |
| "Đáp án phải là A/B/C/D" | Sửa `\answer{A}` (viết hoa) |
| "Đúng/Sai phải có 4 ý" | Thêm a/b/c/d đủ 4 ý |
| "Thiếu \\answer{...}" | Thêm `\answer{...}` cho mỗi câu |

### AZOTA Embed

| Lỗi | Giải pháp |
|-----|-----------|
| "URL phải từ azota.vn" | Copy đúng iframe từ azota.vn |
| "Không tìm thấy src" | Kiểm tra iframe code có đầy đủ không |
| "Iframe không load" | Thử mở link azota.vn trực tiếp |

## 🎯 Khi nào dùng cách nào?

**Dùng LaTeX khi:**
- ✓ Muốn quản lý câu hỏi trong ThachLab
- ✓ Cần edit từng câu sau
- ✓ Câu hỏi phức tạp với công thức

**Dùng AZOTA khi:**
- ✓ Đề được tạo trên AZOTA rồi
- ✓ Muốn học sinh làm trực tiếp trên AZOTA
- ✓ Không cần lưu chi tiết câu hỏi

## 💡 Tips

1. **LaTeX Validation**: Parser tự động kiểm tra syntax, xem cảnh báo trước khi save
2. **Preview**: Xem trước câu hỏi trước khi chỉnh sửa
3. **Edit**: Sau khi import, vẫn có thể edit từng câu trong ExamEditor
4. **Export**: (Tương lai) Có thể export đề thành LaTeX

## 📚 Tài liệu thêm

- `docs/AZOTA-INTEGRATION.md` - Chi tiết nhúng AZOTA
- `docs/LATEX-EDITOR-GUIDE.md` - LaTeX syntax
