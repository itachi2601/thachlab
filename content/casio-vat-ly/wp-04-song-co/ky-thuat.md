# Chuyên đề 2 · Sóng cơ, giao thoa, sóng dừng, sóng âm: ba trang kỹ thuật (WP-04)

> Công cụ máy: `../wp-01-so-tay-fx580vnx/so-tay.md`. Mỗi công thức ghi kèm **điều kiện áp dụng** (bài học từ kiểm chéo WP-03). Thể lệ tạm: làm tròn 4 chữ số có nghĩa.

---

## Trang 1 · Sóng truyền và độ lệch pha

**Công thức**
- $\lambda = vT = \dfrac{v}{f}$.
- Nguồn $u_0 = A\cos(\omega t + \varphi)$ thì điểm cách nguồn $x$ (sóng truyền từ nguồn, không mất năng lượng): $u(x,t) = A\cos\left(\omega t + \varphi - \dfrac{2\pi x}{\lambda}\right)$.
- Độ lệch pha giữa hai điểm trên phương truyền cách nhau $d$: $\Delta\varphi = \dfrac{2\pi d}{\lambda}$.
  - Cùng pha: $d = k\lambda$. Ngược pha: $d = (k+\tfrac12)\lambda$. Vuông pha: $d = (2k+1)\tfrac{\lambda}{4}$ ($k$ nguyên).
- Tốc độ dao động cực đại của phần tử: $v_{max} = \omega A = 2\pi f A$; so với tốc độ truyền: $\dfrac{v_{max}}{v} = \dfrac{2\pi A}{\lambda}$. **Hai tốc độ này khác nhau, đừng nhầm.**

**Thao tác máy**
- Phương trình sóng: lưu $\lambda$ vào `W`, rồi `CALC` với $x$ và $t$ ở chế độ **Rad**.
- Tìm điểm cùng pha / ngược pha trong khoảng $[d_1, d_2]$: TABLE với $f(X) = \dfrac{X}{\lambda}$ (số bước sóng); các hàng có giá trị nguyên là cùng pha với nguồn, giá trị bán nguyên là ngược pha.

**Bẫy**
- Công thức $u(x,t)$ có dấu trừ khi sóng truyền theo chiều $+x$; truyền ngược thì dấu cộng.
- Đổi $\lambda$ và $x$ cùng đơn vị (cm hay m).

---

## Trang 2 · Giao thoa hai nguồn

Hai nguồn $A, B$ cách nhau $AB$, cùng biên độ, $\lambda$ cho trước. Gọi $d_1, d_2$ là khoảng cách từ điểm $M$ tới $A, B$.

| | Hai nguồn **cùng pha** | Hai nguồn **ngược pha** |
|---|---|---|
| Cực đại | $d_2 - d_1 = k\lambda$ | $d_2 - d_1 = (k+\tfrac12)\lambda$ |
| Cực tiểu | $d_2 - d_1 = (k+\tfrac12)\lambda$ | $d_2 - d_1 = k\lambda$ |

**Đếm số cực trị trên đoạn $AB$**
1. Với mọi điểm trên đoạn $AB$: $|d_2 - d_1| < AB$ (**bất đẳng thức chặt**, vì $A$ và $B$ là nguồn, không tính).
2. Giải bất phương trình theo $k$ nguyên; số nghiệm là số cực trị.
3. Cực trị nào có hiệu đường đi bằng $\pm AB$ (xảy ra khi $\dfrac{AB}{\lambda}$ nguyên với họ $k\lambda$, hoặc bán nguyên với họ $(k+\tfrac12)\lambda$) ứng với chính $A, B$ nên **loại**; bất đẳng thức chặt ở bước 1 đã loại sẵn.

**Đếm trên đoạn không phải $AB$ (ví dụ cạnh $CD$ của hình vuông, hình chữ nhật)**
- Tính $d_2 - d_1$ ở hai đầu mút (đây là giá trị lớn nhất và nhỏ nhất của hiệu đường đi trên đoạn đó, **khi hiệu đường đi đơn điệu theo vị trí**, đúng cho cạnh đối diện của hình vuông/chữ nhật nối hai nguồn).
- Đếm $k$ nguyên để $k\lambda$ (hoặc $(k+\tfrac12)\lambda$) nằm **giữa** hai giá trị đó. Mút của đoạn: nếu rơi đúng vào cực trị thì xét theo đề (đề thường nói "kể cả hai đầu" hoặc "không kể").

**Điểm cực đại gần nguồn nhất trên đường thẳng vuông góc $AB$ tại $A$** (nguồn cùng pha)
- $d_1 = x$, $d_2 = \sqrt{x^2 + AB^2}$, cực đại bậc $k$: $\sqrt{x^2 + AB^2} - x = k\lambda$.
- Giải: $x = \dfrac{AB^2 - (k\lambda)^2}{2k\lambda}$, điều kiện $0 < k\lambda < AB$. Điểm **gần $A$ nhất** ứng với $k$ **lớn nhất** thoả điều kiện; điểm xa nhất ứng với $k = 1$.
- Máy: `SOLVE` với $\sqrt{X^2 + AB^2} - X = k\lambda$, giá trị đầu nhỏ.

**Bẫy**
- Đổi nguồn cùng pha thành ngược pha là đổi hẳn cực đại ↔ cực tiểu.
- $k$ có thể âm; đếm cả hai phía của đường trung trực.

---

## Trang 3 · Sóng dừng và sóng âm

**Sóng dừng trên dây** (điều kiện: sóng tới và phản xạ có cùng tần số, biên độ)
- Hai nút liên tiếp (hoặc hai bụng liên tiếp) cách nhau $\dfrac{\lambda}{2}$; nút – bụng liên tiếp cách $\dfrac{\lambda}{4}$.
- **Hai đầu cố định:** $\ell = n\dfrac{\lambda}{2}$, $n$ = số bụng; $f_n = n\dfrac{v}{2\ell}$.
- **Một đầu cố định, một đầu tự do:** $\ell = (2n+1)\dfrac{\lambda}{4}$ ($n=0,1,2,\dots$); số bụng (kể cả đầu tự do) $= n+1$; $f = (2n+1)\dfrac{v}{4\ell}$, chỉ các hoạ âm bậc **lẻ**.
- Biên độ tại điểm cách một nút đoạn $d$: $A_d = A_b\left|\sin\dfrac{2\pi d}{\lambda}\right|$ ($A_b$ là biên độ bụng).
- Các điểm khác nhau trong cùng một bó sóng dao động **cùng pha**; hai bó liền kề **ngược pha**.

**Sóng âm** (nguồn điểm, không hấp thụ)
- Cường độ âm $I = \dfrac{P}{4\pi r^2}$; $I \propto \dfrac{1}{r^2}$.
- Mức cường độ âm $L = 10\log\dfrac{I}{I_0}$ (dB), $I_0 = 10^{-12}$ W/m².
- Hiệu mức: $L_1 - L_2 = 20\log\dfrac{r_2}{r_1}$ (chỉ khi cùng một nguồn điểm); thêm $n$ nguồn giống hệt cùng vị trí **không kết hợp** (cộng cường độ) thì $L$ tăng $10\log n$; nguồn kết hợp cộng biên độ nên không áp dụng.

**Thao tác máy**
- Mũ và log: `10^(...)` và `log(...)` (log thập phân); đừng dùng `ln`.
- Tìm tần số thoả điều kiện nằm trong khoảng: TABLE với $f(X) = (2X+1)\dfrac{v}{4\ell}$, $X = 0,1,2,\dots$; đọc các hàng nằm trong khoảng.

**Bẫy**
- Đầu tự do là **bụng**, đầu cố định là **nút**.
- $L_1 - L_2 = 20\log(r_2/r_1)$ dùng khoảng cách tới **nguồn**; trung điểm của hai điểm cách nguồn $r_A$, $r_B$ thẳng hàng cùng phía là $\dfrac{r_A + r_B}{2}$.
