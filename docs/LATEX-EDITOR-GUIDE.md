# Hướng dẫn sử dụng LaTeX Editor

## 📋 Tổng quan

LaTeX Editor giúp admin dễ dàng soạn thảo nội dung bài học với:
- **LaTeX Mode**: Viết định dạng LaTeX, tự động convert sang HTML
- **HTML Mode**: Viết HTML trực tiếp (nếu cần)
- **Live Preview**: Xem trước kết quả trước khi lưu
- **Math Rendering**: Hỗ trợ công thức toán (KaTeX)

## 🚀 Cách sử dụng

### 1. Chế độ LaTeX (Khuyên dùng)

Khi soạn bài học trong tab "Bài học" → "Quản trị" → chọn hoặc thêm mục:

1. Chọn tab **📐 LaTeX**
2. Viết nội dung theo cú pháp LaTeX
3. Bật **Preview** để xem trước
4. Click **✓ Convert → HTML** để chuyển đổi
5. Bài được lưu dưới dạng HTML (có thể render math)

### 2. Chế độ HTML

Nếu cần chỉnh sửa HTML trực tiếp:

1. Chọn tab **♯ HTML**
2. Sửa HTML theo ý
3. Click **Save** để lưu

## 📝 Cú pháp LaTeX hỗ trợ

### Tiêu đề

```latex
\section{Chương 1: Lực và Chuyển động}
Nội dung chương...

\subsection{1.1. Định luật Newton}
Giải thích chi tiết...

\subsubsection{1.1.1. Định luật I}
Nội dung nhỏ hơn...

\paragraph{Ví dụ minh họa}
Cụ thể hóa...
```

**Output HTML:**
```html
<h1 class="text-2xl font-bold mt-4 mb-2">Chương 1: Lực và Chuyển động</h1>
<p class="text-base leading-relaxed my-2">Nội dung chương...</p>

<h2 class="text-xl font-bold mt-3 mb-1.5">1.1. Định luật Newton</h2>
<p class="text-base leading-relaxed my-2">Giải thích chi tiết...</p>

<h3 class="text-lg font-semibold mt-2 mb-1">1.1.1. Định luật I</h3>
<p class="text-base leading-relaxed my-2">Nội dung nhỏ hơn...</p>

<h4 class="font-semibold mt-2 mb-1">Ví dụ minh họa</h4>
<p class="text-base leading-relaxed my-2">Cụ thể hóa...</p>
```

### Định dạng văn bản

```latex
\textbf{In đậm}
\textit{In nghiêng}
\emph{Nhấn mạnh}
\texttt{Mã code}
```

**Output:**
- **In đậm**
- *In nghiêng*
- *Nhấn mạnh*
- `Mã code`

### Danh sách

#### Liệt kê không sắp xếp
```latex
\begin{itemize}
\item Lực là vector có hướng
\item Lực gây ra gia tốc
\item Đơn vị lực là Newton (N)
\end{itemize}
```

**Output:**
- Lực là vector có hướng
- Lực gây ra gia tốc
- Đơn vị lực là Newton (N)

#### Danh sách có thứ tự
```latex
\begin{enumerate}
\item Đầu tiên, xác định lực
\item Tiếp theo, tính gia tốc
\item Cuối cùng, kiểm tra kết quả
\end{enumerate}
```

**Output:**
1. Đầu tiên, xác định lực
2. Tiếp theo, tính gia tốc
3. Cuối cùng, kiểm tra kết quả

### Công thức toán

#### Công thức trong dòng (Inline Math)

Sử dụng `$...$` hoặc `\(...\)`:

```latex
Định luật II Newton: $F = ma$, trong đó m là khối lượng.
```

**Output:**
Định luật II Newton: $F = ma$, trong đó m là khối lượng.

#### Công thức tách dòng (Display Math)

Sử dụng `$$...$$` hoặc `\[...\]`:

```latex
Công thức tính công:
$$W = F \cdot s \cdot \cos\theta$$

Hoặc:
\[E_k = \frac{1}{2}mv^2\]
```

**Output:**
Công thức tính công:
$$W = F \cdot s \cdot \cos\theta$$

Hoặc:
$$E_k = \frac{1}{2}mv^2$$

### Math notation

```latex
- Lũy thừa: $x^2$, $e^{-t}$
- Chỉ số: $x_1$, $a_{n+1}$
- Phân số: $\frac{1}{2}$, $\frac{a+b}{c}$
- Căn: $\sqrt{x}$, $\sqrt[3]{x}$
- Tích phân: $\int_0^1 x \, dx$
- Tổng: $\sum_{i=1}^{n} i$
- Giới hạn: $\lim_{x \to 0} \frac{\sin x}{x}$
- Đạo hàm: $\frac{df}{dx}$, $f'(x)$
```

## 📖 Ví dụ đầy đủ

```latex
\section{Chuyển động của vật dưới tác dụng của lực}

Khi một lực \textbf{không đổi} tác dụng lên một vật, nó sẽ tạo ra gia tốc:
$$a = \frac{F}{m}$$

\subsection{Ví dụ 1: Xe tải}

Một xe tải có khối lượng $m = 1000 \text{ kg}$ được kéo bởi lực $F = 5000 \text{ N}$.
Tính gia tốc của xe.

\textit{Giải:}

Áp dụng định luật II Newton:
$$a = \frac{F}{m} = \frac{5000}{1000} = 5 \text{ m/s}^2$$

\subsection{Các bước giải bài tập}

\begin{enumerate}
\item Xác định các lực tác dụng lên vật
\item Vẽ sơ đồ lực (nếu cần)
\item Áp dụng $F = ma$ theo phương chuyển động
\item Tính toán gia tốc hoặc lực
\end{enumerate}

\paragraph{Lưu ý quan trọng}

Định luật Newton chỉ áp dụng trong \textbf{hệ quy chiếu quán tính}.
```

## 🔧 Cách integrate MathRenderer

Khi hiển thị nội dung bài học, sử dụng component `MathRenderer`:

```tsx
import MathRenderer from "@/components/lessons/MathRenderer";

// Trong component của bạn:
<MathRenderer 
  html={lessonItem.body_html}
  className="prose prose-invert max-w-none"
/>
```

Component này sẽ:
1. Parse HTML
2. Tìm các phần math (`.math-inline`, `.math-display`)
3. Render với KaTeX
4. Hiển thị công thức đẹp

## ✅ Validation

LaTeX Editor tự động kiểm tra:
- ✓ Dấu ngoặc `{}` phải khớp
- ✓ Dấu `$` phải thành cặp
- ✓ `\begin{}...\end{}` phải khớp

Nếu có lỗi, sẽ hiển thị danh sách lỗi. Sửa lỗi trước khi convert.

## 🎨 Styling

HTML output tự động có classes Tailwind:

| Element | Classes |
|---------|---------|
| h1 | `text-2xl font-bold mt-4 mb-2` |
| h2 | `text-xl font-bold mt-3 mb-1.5` |
| h3 | `text-lg font-semibold mt-2 mb-1` |
| h4 | `font-semibold mt-2 mb-1` |
| p | `text-base leading-relaxed my-2` |
| ul | `list-disc list-inside my-2 ml-4` |
| ol | `list-decimal list-inside my-2 ml-4` |
| li | `my-1` |
| strong | `font-bold` |
| em | `italic` |
| code | `bg-slate-200 text-slate-900 px-1 rounded font-mono text-sm` |

## 🐛 Troubleshooting

**Q: Công thức không render?**
A: Kiểm tra:
- Syntax LaTeX đúng không?
- Nội dung được wrap trong `$...$` hay `$$...$$`?
- MathRenderer component được sử dụng?

**Q: Convert không thành công?**
A: Xem lỗi syntax trong error box, sửa rồi thử lại.

**Q: Muốn giữ LaTeX gốc?**
A: LaTeX gốc được lưu (hiện tại lưu cùng HTML, có thể split ra sau).

## 📚 Tài liệu thêm

- **KaTeX Math Docs**: https://katex.org/docs/supported.html
- **LaTeX Commands**: https://www.overleaf.com/learn/latex/Mathematical_expressions
- **HTML Reference**: https://developer.mozilla.org/en-US/docs/Web/HTML
