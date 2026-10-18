# 12 bài luyện · Dao động cơ (WP-03)

Mức: ⭐ cơ bản · ⭐⭐ đúng cấp thi · ⭐⭐⭐ phân loại. Làm tròn tạm **4 chữ số có nghĩa**. Đáp số sinh từ `tinh.py`. Quy trình bấm máy theo `../wp-01-so-tay-fx580vnx/so-tay.md`, **chưa thử trên máy thật**.

---

## D1 ⭐ Con lắc lò xo: đại lượng cơ bản
**Đề.** Con lắc lò xo $k = 50$ N/m, $m = 200$ g, biên độ $A = 6$ cm. Tính $\omega$, $T$, $f$, $v_{max}$, $a_{max}$ và cơ năng.
**Đáp số.** $\omega = 15{,}81$ rad/s; $T = 0{,}3974$ s; $f = 2{,}516$ Hz; $v_{max} = 0{,}9487$ m/s; $a_{max} = 15{,}00$ m/s²; $W = 0{,}09000$ J.
**Bấm máy**
- Gõ `√(50÷0.2)`, `STO W`.
- `2π÷W` cho $T$; `W÷(2π)` cho $f$.
- `W×0.06` cho $v_{max}$; `W²×0.06` cho $a_{max}$; `0.5×50×0.06²` cho $W$.
**Bẫy.** Đổi $m$ về kg và $A$ về m trước khi thế.

## D2 ⭐ Con lắc đơn góc nhỏ
**Đề.** Con lắc đơn $\ell = 0{,}75$ m, $g = 9{,}81$ m/s², biên độ góc $8°$. Tính chu kì (công thức góc nhỏ) và tốc độ cực đại (công thức chính xác và gần đúng).
**Đáp số.** $T = 1{,}737$ s (góc nhỏ); $v_{max} = 0{,}3784$ m/s (chính xác), $0{,}3787$ m/s (gần đúng $\sqrt{g\ell}\,\alpha_0$).
**Bấm máy**
- SETUP **Độ**: `√(2×9.81×0.75×(1−cos(8)))`.
- Gần đúng: đổi sang **Rad**, gõ `√(9.81×0.75)×(8π÷180)`.
**Bẫy.** Ở Rad mà gõ `cos(8)` là cos của 8 rad, sai hoàn toàn.

## D3 ⭐ Li độ, vận tốc, gia tốc tại một thời điểm
**Đề.** $x = 5\cos\left(4\pi t + \dfrac{\pi}{6}\right)$ (cm, s). Tính $x$, $v$, $a$ tại $t = 0{,}25$ s.
**Đáp số.** $x = -4{,}330$ cm; $v = 31{,}42$ cm/s; $a = 683{,}8$ cm/s².
**Bấm máy**
- Rad. Gõ `4π×0.25 + π÷6`, `STO B`.
- `5cos(B)`; `−5×4π×sin(B)`; `−(4π)²×5cos(B)`.
**Bẫy.** Vật ở li độ âm và $v>0$: đang đi về phía dương.

## D4 ⭐ Tổng hợp hai dao động
**Đề.** $x_1 = 8\cos\left(2\pi t + \dfrac{\pi}{6}\right)$, $x_2 = 8\cos\left(2\pi t + \dfrac{\pi}{2}\right)$ (cm). Tìm biên độ và pha ban đầu của dao động tổng hợp.
**Đáp số.** $A = 13{,}86$ cm; $\varphi = 1{,}047$ rad $= \dfrac{\pi}{3}$.
**Bấm máy**
- Số phức, **Độ**: `8∠30 + 8∠90`, `=`, dạng r∠θ: $13{,}86\angle 60$.
**Lời giải.** Hai biên độ bằng nhau nên pha tổng hợp là trung bình cộng: $\dfrac{30° + 90°}{2} = 60°$, $A = 2\cdot 8\cos 30°$.

## D5 ⭐⭐ Thời điểm đầu tiên (SOLVE)
**Đề.** Vật dao động điều hoà biên độ 10 cm, chu kì 0,6 s. Tại $t = 0$, vật ở li độ 5 cm và đang đi theo chiều âm. Tìm thời điểm đầu tiên vật có li độ $-5\sqrt3$ cm.
**Đáp số.** $t = 0{,}1500$ s ($= \dfrac{T}{4}$).
**Bấm máy**
- Pha ban đầu $\varphi = \dfrac{\pi}{3}$ (vì $x>0$, $v<0$). Rad.
- Gõ `10cos(2π÷0.6×X + π÷3) = −5√3`, `SHIFT CALC`, giá trị đầu `0.1`.
**Lời giải.** Từ pha $60°$ đến pha $150°$ là $90°$ nên $t = T/4 = 0{,}15$ s.
**Bẫy.** $\varphi = -\dfrac{\pi}{3}$ thì vật đang đi chiều dương: sai chiều thì sai đáp số.

## D6 ⭐⭐ Quãng đường trong khoảng thời gian dài
**Đề.** $x = 6\cos\left(4\pi t - \dfrac{\pi}{3}\right)$ (cm, s). Tính quãng đường vật đi được từ $t = 0$ đến $t = 1{,}375$ s.
**Đáp số.** $s = 63{,}80$ cm.
**Bấm máy**
- $T = 0{,}5$ s, $\Delta t = 2T + 0{,}75T$.
- $2T$: `2×4×6` $= 48$ cm.
- Phần $0{,}75T$ ứng với pha $-60° \to 210°$:
  - từ pha $-60°$ đến $0°$: `6−3`$= 3$ cm.
  - từ $0°$ đến $180°$: `2×6`$= 12$ cm.
  - từ $180°$ đến $210°$: `6−6cos(30°)`$= 0{,}8038$ cm.
- Cộng: `48+3+12+0.8038`.
**Bẫy.** $0{,}75T$ không phải lúc nào cũng $3A$; phụ thuộc vị trí đầu.

## D7 ⭐⭐ Lực đàn hồi con lắc treo thẳng đứng
**Đề.** Lò xo treo thẳng đứng, $k = 100$ N/m, $m = 0{,}25$ kg, $g = 9{,}8$ m/s². Tính $\Delta\ell_0$, $T$, lực đàn hồi cực đại và cực tiểu khi biên độ (a) 2 cm, (b) 5 cm.
**Đáp số.** $\Delta\ell_0 = 2{,}450$ cm; $T = 0{,}3142$ s.
(a) $F_{max} = 4{,}450$ N; $F_{min} = 0{,}4500$ N.
(b) $F_{max} = 7{,}450$ N; $F_{min} = 0$.
**Bấm máy**
- `0.25×9.8÷100` cho $\Delta\ell_0$, `STO A`.
- `100(A+0.02)`, `100(A−0.02)`; rồi `100(A+0.05)`.
**Bẫy.** Ở (b) $A > \Delta\ell_0$ nên $F_{min} = 0$, không phải $k(\Delta\ell_0 - A) < 0$.

## D8 ⭐⭐ Đồng hồ quả lắc chạy chậm
**Đề.** Đồng hồ quả lắc chạy đúng ở $t_1$. Thanh treo có hệ số nở dài $\alpha = 1{,}2.10^{-5}\ \text{K}^{-1}$; nhiệt độ tăng thêm $30$ °C. Tính tỉ số $T'/T$ và số giây đồng hồ chạy chậm mỗi ngày.
**Đáp số.** $\dfrac{T'}{T} = 1{,}00018$; chậm $15{,}55$ s mỗi ngày.
**Bấm máy**
- `√(1+1.2×10^−5×30)`, `STO A`.
- `86400×(1−1÷A)`.
**Bẫy.** Chỉ dùng $\dfrac{86400\,\alpha\Delta t}{2}$ nếu đề cho phép gần đúng; ở đây dùng công thức chính xác.

## D9 ⭐⭐ Động năng, thế năng
**Đề.** Con lắc lò xo $m = 0{,}1$ kg, $k = 40$ N/m, $A = 5$ cm. Tại $x = 3$ cm tính thế năng, động năng, tốc độ. Tìm li độ để động năng gấp 3 lần thế năng.
**Đáp số.** $W = 0{,}05000$ J; $W_t = 0{,}01800$ J; $W_đ = 0{,}03200$ J; $v = 0{,}8000$ m/s; $x = \pm 2{,}500$ cm.
**Bấm máy**
- `0.5×40×0.05²` → `STO A`; `0.5×40×0.03²`; `A−Ans`; `√(2×Ans÷0.1)`.
- Li độ: `0.05÷√(3+1)`.
**Bẫy.** Đổi cm sang m. Đáp số $x = \pm$ hai giá trị.

## D10 ⭐⭐ Con lắc đơn góc lớn
**Đề.** Con lắc đơn $\ell = 1$ m, $m = 0{,}1$ kg, $g = 9{,}8$ m/s², biên độ góc $60°$. Tại vị trí $\alpha = 30°$ tính tốc độ và lực căng dây.
**Đáp số.** $v = 2{,}678$ m/s; $\tau = 1{,}566$ N.
**Bấm máy**
- SETUP **Độ**. `√(2×9.8×1×(cos(30)−cos(60)))`.
- `0.1×9.8×(3cos(30)−2cos(60))`.
**Bẫy.** Dùng công thức góc nhỏ ($\alpha$ rad) ở góc $60°$ sai nhiều.

## D11 ⭐⭐⭐ Tắt dần có ma sát
**Đề.** Con lắc lò xo ngang, $k = 100$ N/m, $m = 0{,}2$ kg, hệ số ma sát $\mu = 0{,}05$, $g = 10$ m/s². Kéo vật đến $A_0 = 10$ cm rồi thả nhẹ. Tính (a) độ giảm biên độ mỗi nửa chu kì, (b) tốc độ cực đại lần đầu, (c) tổng quãng đường, (d) thời gian đến khi dừng.
**Đáp số.** (a) $\Delta A = 2{,}000$ mm. (b) $v_1 = 2{,}214$ m/s. (c) $S = 5{,}000$ m. (d) $N = 50$ nửa chu kì, $t = 7{,}025$ s.
**Bấm máy**
- `2×0.05×0.2×10÷100` → $0{,}002$.
- $\omega$: `√(100÷0.2)` `STO W`; $v_1$: `W×(0.1−0.001)` (với $x_0 = 0{,}001$ m).
- `100×0.1²÷(2×0.05×0.2×10)`.
- $N = 0{,}1 \div 0{,}002 = 50$; `50×π÷A`.
**Bẫy.** $N$ nguyên nên vật dừng đúng ở O. Nếu $N$ có phần thập phân thì phải xét thêm.

## D12 ⭐⭐⭐ Biên độ tổng hợp nhỏ nhất (TABLE)
**Đề.** $x_1 = 6\cos\left(\omega t + \dfrac{\pi}{3}\right)$ cm và $x_2 = A_2\cos\left(\omega t - \dfrac{\pi}{2}\right)$ cm, $A_2$ thay đổi được. Tìm $A_2$ để biên độ tổng hợp nhỏ nhất, giá trị nhỏ nhất đó, và pha ban đầu khi đó.
**Đáp số.** $A_2 = 5{,}196$ cm; $A_{min} = 3{,}000$ cm; $\varphi = 0$.
**Bấm máy**
- Bảng: `f(X) = √(36+X²+12X×cos(150))` (SETUP Độ), Start `0`, End `10`, Step `1`: nhỏ nhất quanh $X=5$ hoặc 6.
- Thu hẹp: Start `4.5`, End `6`, Step `0.1`: nhỏ nhất tại $5{,}2$.
- Kiểm công thức: `−6cos(150)`$= 5{,}196$; `6sin(150)`$= 3$.
- Pha: Số phức, `6∠60 + 5.196∠−90`, `=`: $3\angle 0$.
**Lời giải.** $\Delta\varphi = 150°$; cực tiểu khi $x_2$ triệt tiêu thành phần ảo của $x_1$.
**Bẫy.** Bảng cho nghiệm gần đúng (5,2); đáp số cuối là công thức (5,196).
