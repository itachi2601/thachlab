# Mini-test 30 phút · Dao động cơ (WP-03)

4 bài, mức ⭐⭐. Làm tròn tạm 4 chữ số có nghĩa. Ghi cách giải ngắn và kết quả. **Đáp án ở cuối file, cắt rời trước khi phát cho học sinh.**

**M1.** Một vật dao động điều hoà có tốc độ cực đại $0{,}2\pi$ m/s và gia tốc cực đại $4\pi^2$ m/s². Tính tần số góc, biên độ và chu kì.

**M2.** Hai con lắc đơn dao động tại cùng một nơi. Trong cùng khoảng thời gian, con lắc thứ nhất thực hiện 30 dao động, con lắc thứ hai thực hiện 36 dao động. Hiệu chiều dài hai con lắc là $0{,}44$ m. Tính chiều dài và chu kì mỗi con lắc, lấy $g = 9{,}8$ m/s².

**M3.** Con lắc lò xo treo thẳng đứng dao động điều hoà với chu kì $0{,}4$ s tại nơi $g = 9{,}8$ m/s². Tỉ số giữa lực đàn hồi cực đại và cực tiểu là $3$. Tính độ biến dạng ở vị trí cân bằng, biên độ và tốc độ cực đại.

**M4.** $x_1 = 4\cos\left(2\pi t + \dfrac{\pi}{6}\right)$ và $x_2 = 3\cos\left(2\pi t - \dfrac{\pi}{3}\right)$ (cm, s). Tìm biên độ, pha ban đầu của dao động tổng hợp và thời điểm đầu tiên $t > 0$ vật có li độ $2{,}5$ cm (chấp nhận sai số $\pm 0{,}0001$ s do làm tròn pha).

---

## Đáp án (cắt rời)

**M1.** $\omega = \dfrac{a_{max}}{v_{max}} = 62{,}83$ rad/s $(= 20\pi)$; $A = \dfrac{v_{max}}{\omega} = 1{,}000$ cm; $T = 0{,}1000$ s.
- Gõ: `4π²÷(0.2π)`, `STO D`; `0.2π÷D×100` (cm); `2π÷D`.

**M2.** $\dfrac{T_1}{T_2} = \dfrac{36}{30} = 1{,}2$ nên $\dfrac{\ell_1}{\ell_2} = 1{,}44$; $\ell_1 - \ell_2 = 0{,}44\ell_2 = 0{,}44$ nên $\ell_2 = 1{,}000$ m, $\ell_1 = 1{,}440$ m.
$T_1 = 2{,}409$ s; $T_2 = 2{,}007$ s.
- Gõ: `2π√(1.44÷9.8)`; `2π√(1÷9.8)`.

**M3.** $\dfrac{\Delta\ell_0 + A}{\Delta\ell_0 - A} = 3$ nên $A = \dfrac{\Delta\ell_0}{2}$ (và $A<\Delta\ell_0$ nên $F_{min}\neq 0$ hợp lệ).
$\Delta\ell_0 = \dfrac{gT^2}{4\pi^2} = 3{,}972$ cm; $A = 1{,}986$ cm; $v_{max} = \dfrac{2\pi}{T}A = 31{,}19$ cm/s.
- Gõ: `9.8×0.4²÷(4π²)`.

**M4.** Hai dao động vuông pha ($30° - (-60°) = 90°$): $A = 5{,}000$ cm; $\varphi = 30° - \arctan\dfrac34 = -0{,}1199$ rad $(-6{,}870°)$.
$x = 5\cos(2\pi t - 0{,}1199) = 2{,}5$: $2\pi t - 0{,}1199 = \pm\dfrac{\pi}{3} + 2k\pi$; nghiệm dương nhỏ nhất $t = 0{,}1857$ s (thế $\varphi$ đã làm tròn $-0{,}1199$ vẫn ra $0{,}1857$).
- Gõ SOLVE: `5cos(2πx − 0.1199) = 2.5` (x là phím `x`), giá trị đầu `0.2`. Kiểm: nghiệm $-\dfrac{\pi}{3}$ cho $t<0$.
