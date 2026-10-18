# 12 bài luyện · Sóng cơ (WP-04)

Mức: ⭐ cơ bản · ⭐⭐ đúng cấp thi · ⭐⭐⭐ phân loại. Làm tròn tạm **4 chữ số có nghĩa**. Đáp số sinh từ `tinh.py`. Quy trình bấm máy theo `../wp-01-so-tay-fx580vnx/so-tay.md`, **chưa thử trên máy thật**.

---

## W1 ⭐ Phương trình sóng và độ lệch pha
**Đề.** Nguồn $u_0 = 3\cos(20\pi t)$ (cm, s), tốc độ truyền sóng $2$ m/s. Tính bước sóng; độ lệch pha giữa điểm $M$ cách nguồn $25$ cm và nguồn; li độ của $M$ tại $t = 0{,}04$ s.
**Đáp số.** $\lambda = 20{,}00$ cm; $\Delta\varphi = 7{,}854$ rad $\left(= \dfrac{5\pi}{2}\right)$, tức vuông pha; $u_M = 1{,}763$ cm.
**Bấm máy**
- `λ`: `200÷10` $= 20$ cm, `STO D`.
- Δφ: `2π×25÷D` $= 7{,}854$, `STO B`.
- SETUP **Rad**, rồi `3cos(20π×0.04 − B)` $= 1{,}763$.
**Bẫy.** $f = \dfrac{\omega}{2\pi} = 10$ Hz; $\lambda = \dfrac{200}{10}$ cm, không phải $\dfrac{2}{10}$ cm.

## W2 ⭐ Mức cường độ âm
**Đề.** Nguồn âm điểm công suất $0{,}5$ W. Tính cường độ âm và mức cường độ âm tại điểm cách nguồn $10$ m. Nếu khoảng cách tăng gấp đôi, mức cường độ âm giảm bao nhiêu dB?
**Đáp số.** $I = 3{,}979.10^{-4}$ W/m²; $L = 86{,}00$ dB; giảm $6{,}021$ dB (còn $79{,}98$ dB).
**Bấm máy**
- `0.5÷(4π×10²)`, `STO D`.
- `10×log(D÷10^−12)`.
- Giảm: `20×log(2)`.
**Bẫy.** Dùng `log` (thập phân), không dùng `ln`.

## W3 ⭐ Sóng dừng hai đầu cố định
**Đề.** Dây dài $0{,}9$ m hai đầu cố định, tần số $50$ Hz, quan sát được $3$ bụng. Tính bước sóng, tốc độ truyền sóng và tần số nhỏ nhất để có sóng dừng trên dây đó.
**Đáp số.** $\lambda = 0{,}6000$ m; $v = 30{,}00$ m/s; $f_1 = 16{,}67$ Hz.
**Bấm máy**
- `2×0.9÷3` → `STO D`; `D×50`; rồi `30÷(2×0.9)`.
**Bẫy.** $n$ là số **bụng**, không phải số nút.

## W4 ⭐ Tốc độ dao động và tốc độ truyền sóng
**Đề.** Sóng biên độ $2$ mm, tần số $25$ Hz, tốc độ truyền $0{,}5$ m/s. Tính bước sóng, tốc độ dao động cực đại của phần tử môi trường và tỉ số $v_{max}/v$.
**Đáp số.** $\lambda = 2{,}000$ cm; $v_{max} = 0{,}3142$ m/s; $\dfrac{v_{max}}{v} = 0{,}6283$.
**Bấm máy**
- `0.5÷25`; `2π×25×0.002`; `Ans÷0.5`.
**Bẫy.** Đổi $A$ về m trước khi nhân.

## W5 ⭐⭐ Đếm cực đại và cực tiểu, nguồn cùng pha
**Đề.** Hai nguồn $A, B$ cùng pha, $AB = 19$ cm, $f = 25$ Hz, tốc độ sóng $0{,}8$ m/s. Có bao nhiêu điểm cực đại và cực tiểu trên đoạn $AB$?
**Đáp số.** $\lambda = 3{,}200$ cm; $11$ cực đại; $12$ cực tiểu.
**Bấm máy**
- `80÷25` $= 3{,}2$ cm, `STO D`; `19÷D` $= 5{,}9375$.
- Cực đại: $|k| < 5{,}9375$ nên $k = -5 \dots 5$.
- Cực tiểu: $|k + 0{,}5| < 5{,}9375$ nên $k = -6 \dots 5$.
**Bẫy.** Cực tiểu nhiều hơn cực đại một khi phần thập phân của $AB/\lambda$ lớn hơn 0,5.

## W6 ⭐⭐ Hai nguồn ngược pha
**Đề.** Như W5 nhưng hai nguồn **ngược pha** và $AB = 17{,}5$ cm. Đếm cực đại và cực tiểu trên $AB$.
**Đáp số.** $10$ cực đại; $11$ cực tiểu.
**Bấm máy**
- `17.5÷3.2` $= 5{,}469$.
- Cực đại: $|k + 0{,}5| < 5{,}469$ nên $k = -5 \dots 4$.
- Cực tiểu: $|k| < 5{,}469$ nên $k = -5 \dots 5$.
**Bẫy.** Quên đổi vai trò cực đại ↔ cực tiểu khi đổi pha nguồn.

## W7 ⭐⭐ Cực trị trên cạnh hình vuông
**Đề.** Hai nguồn $A, B$ cùng pha, $ABCD$ là hình vuông cạnh $10$ cm, $\lambda = 1{,}2$ cm. Đếm số điểm cực đại và cực tiểu trên cạnh $CD$ (không kể $C, D$).
**Đáp số.** $|d_2 - d_1|$ biến thiên từ $0$ đến $10\sqrt2 - 10 = 4{,}142$ cm: $7$ cực đại; $6$ cực tiểu.
**Bấm máy**
- `10√2 − 10` $= 4{,}142$.
- Cực đại: $|k| \cdot 1{,}2 < 4{,}142$ nên $|k| \leq 3$: 7 điểm.
- Cực tiểu: $|k + 0{,}5| \cdot 1{,}2 < 4{,}142$ nên $k + 0{,}5 \in \{\pm 0{,}5; \pm1{,}5; \pm 2{,}5\}$: 6 điểm.
- Hoặc TABLE: cực đại `f(X) = 1.2X`; cực tiểu `f(X) = 1.2(X+0.5)`; Start `-4`, End `3`, Step `1`; đếm hàng có $|f| < 4{,}142$.
**Bẫy.** Ở mỗi giá trị $d_2 - d_1$ khác $0$, có **một** điểm trên $CD$ ($CD$ nằm một nửa mặt phẳng; hiệu đường đi đơn điệu theo vị trí). Riêng $k=0$ là điểm giữa $CD$, cũng chỉ một điểm.

## W8 ⭐⭐ Một đầu cố định, một đầu tự do
**Đề.** Dây dài $0{,}75$ m, một đầu cố định, một đầu tự do, tốc độ truyền sóng $60$ m/s. Tìm tần số nhỏ nhất; và các tần số trong khoảng $150$–$250$ Hz kèm số bụng tương ứng.
**Đáp số.** $f_1 = 20{,}00$ Hz; có $180$ Hz ($5$ bụng) và $220$ Hz ($6$ bụng).
**Bấm máy**
- `60÷(4×0.75)` $= 20$.
- Bảng: `f(X) = (2X+1)×20`, Start `0`, End `12`, Step `1`: đọc các hàng $150 \leq f \leq 250$.
- Số bụng $= n + 1$: $180 \to n = 4$; $220 \to n = 5$.
**Bẫy.** Bội chẵn (40, 80…) không có sóng dừng vì đầu tự do phải là bụng.

## W9 ⭐⭐ Biên độ điểm trên dây sóng dừng
**Đề.** Dây hai đầu cố định có sóng dừng, biên độ bụng $4$ cm, $\lambda = 60$ cm. (a) Biên độ điểm cách nút gần nhất $5$ cm. (b) Khoảng cách nhỏ nhất giữa hai điểm có cùng biên độ $2\sqrt2$ cm.
**Đáp số.** (a) $A = 2{,}000$ cm. (b) $15{,}00$ cm $\left(= \dfrac{\lambda}{4}\right)$.
**Bấm máy**
- Rad: `4×abs(sin(2π×5÷60))`.
- (b): $|\sin\theta| = \dfrac{\sqrt2}{2}$ nên $\theta = \dfrac{\pi}{4}$, $\dfrac{3\pi}{4}$, …; khoảng cách giữa hai vị trí liên tiếp $= \dfrac{\lambda}{4}$.
**Bẫy.** Các điểm biên độ $\dfrac{A_b}{\sqrt2}$ cách nhau đều $\dfrac{\lambda}{4}$, không phải $\dfrac{\lambda}{8}$ ($\lambda/8$ là khoảng cách tới nút).

## W10 ⭐⭐ Điểm cực đại gần nguồn nhất (SOLVE)
**Đề.** Hai nguồn cùng pha $A, B$ cách nhau $20$ cm, $\lambda = 3$ cm. Trên đường thẳng vuông góc với $AB$ tại $A$, tìm điểm cực đại gần $A$ nhất (khác $A$).
**Đáp số.** Cực đại bậc $k_{max} = 6$: $x = 2{,}111$ cm.
**Bấm máy**
- `20÷3` $= 6{,}67$ nên $k_{max} = 6$.
- SOLVE: `√(X²+400) − X = 18`, giá trị đầu `2`. Hoặc `(400−18²)÷(2×18)`.
**Bẫy.** Chọn $k = 1$ cho điểm **xa** $A$ nhất ($x = 65{,}17$ cm), không phải gần nhất.

## W11 ⭐⭐⭐ Thời gian li độ không vượt ngưỡng
**Đề.** Sóng dừng trên dây, biên độ bụng $4$ cm, chu kì $0{,}2$ s. Điểm $M$ có biên độ $2\sqrt3$ cm. Trong một chu kì, tính khoảng thời gian li độ của $M$ có độ lớn không vượt quá $2$ cm.
**Đáp số.** Tỉ lệ $0{,}3918\ T$; $t = 0{,}07837$ s.
**Bấm máy**
- Độ lớn $\left|2\sqrt3\cos\theta\right| \leq 2$ nên $|\cos\theta| \leq \dfrac{1}{\sqrt3}$.
- Độ: `1 − 2×cos⁻¹(1÷√3)÷180` $= 0{,}3918$ (giữ `cos⁻¹` trả độ ở chế độ Độ; tỉ lệ của $T$).
- Nhân $0{,}2$.
**Lời giải.** Trong nửa chu kì $\theta$ chạy $180°$; li độ vượt ngưỡng khi $|\cos\theta| > c$ trong hai cung mỗi cung $\arccos c$; còn lại $180° - 2\arccos c$ thoả.
**Bẫy.** Đổi arccos ra độ rồi chia $180$ (nửa chu kì), không chia $360$.

## W12 ⭐⭐⭐ Mức cường độ âm tại trung điểm
**Đề.** Nguồn âm điểm $O$; $A$ và $B$ thẳng hàng với $O$, cùng phía. Mức cường độ âm tại $A$ là $60$ dB, tại $B$ là $40$ dB. Tính mức cường độ âm tại trung điểm $M$ của $AB$. Nếu đặt thêm một nguồn giống hệt tại $O$ (hai nguồn **không kết hợp**, cường độ cộng lại) thì mức tại $M$ là bao nhiêu?
**Đáp số.** $L_M = 45{,}19$ dB; sau khi thêm nguồn: $48{,}20$ dB.
**Bấm máy**
- $L_A - L_B = 20 = 20\log\dfrac{OB}{OA}$ nên $OB = 10\ OA$.
- $OM = \dfrac{OA + OB}{2} = 5{,}5\ OA$.
- `60 − 20×log(5.5)` $= 45{,}19$; rồi `Ans + 10×log(2)` $= 48{,}20$.
**Bẫy.** $OM$ là trung bình cộng hai **khoảng cách tới nguồn**, không phải trung bình cộng hai mức dB.
