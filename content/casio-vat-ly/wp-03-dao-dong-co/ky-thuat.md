# Chuyên đề 1 · Dao động cơ: ba trang kỹ thuật (WP-03)

> Công cụ máy xem `../wp-01-so-tay-fx580vnx/so-tay.md`. Trang này chỉ ghi **công thức và cách nghĩ theo từng dạng**, cùng thao tác máy ứng với dạng đó. Thể lệ tạm: làm tròn 4 chữ số có nghĩa, đơn vị gốc trong ngoặc.

---

## Trang 1 · Phương trình dao động, pha, và tìm thời điểm

**Công thức**
- $x = A\cos(\omega t + \varphi)$; $v = -A\omega\sin(\omega t + \varphi)$; $a = -\omega^2 x$.
- $\omega = \dfrac{2\pi}{T} = 2\pi f$; $v_{max} = \omega A$; $a_{max} = \omega^2 A$.
- Hệ thức độc lập: $A^2 = x^2 + \dfrac{v^2}{\omega^2}$.
- Phương trình $\sin$ đổi sang $\cos$: $\sin\theta = \cos\left(\theta - \dfrac{\pi}{2}\right)$.

**Dạng A · Tính $x, v, a$ tại thời điểm $t$**
1. Máy để **Rad** (vì $\omega t$ tính bằng rad).
2. Lưu $\omega t + \varphi$ vào biến (ví dụ B) rồi dùng lại: `4π×0.25 + π÷6` → `STO B`.
3. Tính `5cos(B)`, `−5×4π×sin(B)`, `−(4π)²×5cos(B)`.
*Bẫy:* quên đổi đơn vị $x$ (cm) trước khi dùng $a$ theo m/s².

**Dạng B · Thời điểm vật qua một li độ**
1. Viết $x(t) = x_0$, đặt $\theta = \omega t + \varphi$.
2. `SOLVE` với giá trị đầu **gần nghiệm mong muốn**.
3. Phân biệt chiều chuyển động bằng dấu $v$: tại nghiệm tìm được, tính $-A\omega\sin\theta$.
*Bẫy:* SOLVE chỉ trả một nghiệm. Muốn nghiệm thứ hai, đổi giá trị đầu sang vùng khác, hoặc cộng $T$.

**Dạng C · Quãng đường trong khoảng thời gian $\Delta t$**
1. $\Delta t = nT + \delta$ (hoặc $n\dfrac{T}{2} + \delta$): mỗi chu kì đi $4A$, mỗi nửa chu kì đi $2A$.
2. Phần dư $\delta$: tính pha đầu và pha cuối, cộng đoạn từng khúc ($A \to 0$, $0 \to -A$…), nhớ khi qua biên phải đổi chiều.
*Bẫy:* dùng $v\cdot t$ cho dao động điều hoà (vận tốc thay đổi).

---

## Trang 2 · Con lắc lò xo, con lắc đơn, và năng lượng

**Con lắc lò xo**
- $\omega = \sqrt{\dfrac{k}{m}}$; $T = 2\pi\sqrt{\dfrac{m}{k}}$.
- Năng lượng: $W = \dfrac12 kA^2 = \dfrac12 m\omega^2A^2$; $W_t = \dfrac12 kx^2$; $W_đ = W - W_t$.
- Đổi nhanh: $W_đ = nW_t$ khi $x = \pm\dfrac{A}{\sqrt{n+1}}$.
- Treo thẳng đứng: $\Delta\ell_0 = \dfrac{mg}{k}$ ($= \dfrac{gT^2}{4\pi^2}$).
  - $F_{max} = k(\Delta\ell_0 + A)$.
  - $F_{min} = k(\Delta\ell_0 - A)$ nếu $A < \Delta\ell_0$; $F_{min} = 0$ nếu $A \geq \Delta\ell_0$ (lò xo có lúc không biến dạng).

**Con lắc đơn**
- $T = 2\pi\sqrt{\dfrac{\ell}{g}}$. Góc nhỏ: $v_{max} \approx \sqrt{g\ell}\,\alpha_0$.
- Góc bất kì (chính xác):
  - $v = \sqrt{2g\ell(\cos\alpha - \cos\alpha_0)}$.
  - $\tau = mg(3\cos\alpha - 2\cos\alpha_0)$.
- Thay đổi chu kì: $\dfrac{T'}{T} = \sqrt{\dfrac{\ell'}{\ell}\cdot\dfrac{g}{g'}}$.
  - Nhiệt độ tăng $\Delta t$: $\ell' = \ell(1 + \alpha\Delta t)$.
  - Đồng hồ chạy chậm mỗi ngày: $86400\left(1 - \dfrac{T}{T'}\right)$ giây.

**Thao tác máy**
- `CALC` cho cùng công thức nhiều bộ số.
- Với cos của góc độ (ví dụ $\alpha_0 = 60°$): đổi SETUP sang **Độ**, hoặc nhập `60×π÷180` ở chế độ Rad.
*Bẫy:* $A < \Delta\ell_0$ hay không quyết định $F_{min}$; luôn tính $\Delta\ell_0$ trước.

---

## Trang 3 · Tổng hợp, tắt dần, cực trị bằng TABLE

**Tổng hợp dao động (số phức)**
- $A\angle\varphi = A_1\angle\varphi_1 + A_2\angle\varphi_2$; tìm thành phần: $x_2 = x - x_1$.
- Biên độ: $A^2 = A_1^2 + A_2^2 + 2A_1A_2\cos(\varphi_2 - \varphi_1)$.
- $A$ nhỏ nhất theo $A_2\geq 0$:
  - nếu $\cos(\varphi_2-\varphi_1) < 0$ (lệch pha $>90°$): $A_2 = -A_1\cos(\varphi_2-\varphi_1)$ và $A_{min} = A_1|\sin(\varphi_2-\varphi_1)|$.
  - nếu $\cos(\varphi_2-\varphi_1) \geq 0$: $A_{min} = A_1$ tại $A_2 = 0$ (không có cực tiểu trong).
  Kiểm bằng TABLE: nhập $f(X) = \sqrt{A_1^2 + X^2 + 2A_1X\cos\Delta\varphi}$ rồi thu hẹp bước.

**Tắt dần có ma sát (con lắc lò xo ngang)**
- Giảm biên độ mỗi nửa chu kì: $\Delta A = \dfrac{2\mu mg}{k}$.
- Vị trí cân bằng tạm: $x_0 = \dfrac{\mu mg}{k}$; tốc độ cực đại lần đầu: $v_1 = \omega(A_0 - x_0)$.
- Vật **dừng** ngay sau nửa chu kì thứ $n$, với $n$ nhỏ nhất thoả $A_0 - n\,\Delta A \leq \dfrac{\Delta A}{2}$ (tức $|x| \leq x_0$ nên lực đàn hồi không thắng nổi ma sát nghỉ). Thời gian $t = n\dfrac{T}{2}$.
- Khi $N = \dfrac{A_0}{\Delta A}$ nguyên: $n = N$, vật dừng đúng ở O và quãng đường $S = \dfrac{kA_0^2}{2\mu mg}$.
- Khi $N$ không nguyên: vật dừng ở $x_d = A_0 - n\Delta A$, $S = \dfrac{k(A_0^2 - x_d^2)}{2\mu mg}$.
*Bẫy:* dùng $S = \dfrac{kA_0^2}{2\mu mg}$ khi vật không dừng ở O là sai.

**Dùng TABLE thế nào cho gọn**
1. Bảng bước lớn (khoảng 10 hàng) để thấy vùng cực trị.
2. Thu hẹp quanh cực trị, bước 0,1 hoặc 0,01.
3. Kiểm lại bằng công thức đại số, ghi đáp số theo công thức.
