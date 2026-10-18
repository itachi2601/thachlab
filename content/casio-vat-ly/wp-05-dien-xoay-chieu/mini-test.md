# Mini-test 30 phút · Điện xoay chiều (WP-05)

4 bài, mức ⭐⭐. Làm tròn tạm 4 chữ số có nghĩa. **Đáp án ở cuối file, cắt rời trước khi phát.**

**M1.** Đặt $u = 100\sqrt2\cos(100\pi t)$ (V) vào mạch nối tiếp $R = 30\ \Omega$, $L = \dfrac{0{,}5}{\pi}$ H, $C = \dfrac{10^{-3}}{\pi}$ F. Tính $Z$, $I$, $\cos\varphi$, $P$ và độ lệch pha của $u$ so với $i$.

**M2.** Mạch nối tiếp $R = 20\ \Omega$, $L = \dfrac{0{,}4}{\pi}$ H, $C$ thay đổi, $U = 120$ V, $f = 50$ Hz. Tìm $C$ để cộng hưởng, rồi $I$ và $P$ khi đó.

**M3.** Truyền công suất $500$ kW ở điện áp $50$ kV, $\cos\varphi = 0{,}8$, điện trở tổng dây $20\ \Omega$. Tính cường độ dòng điện trên dây, công suất hao phí và hiệu suất truyền tải.

**M4.** Mạch nối tiếp $R = 20\ \Omega$, $Z_C = 15\ \Omega$, $U = 80$ V, $\omega = 100\pi$ rad/s; $L$ thay đổi. Tìm $L$ để $U_L$ cực đại và giá trị cực đại.

---

## Đáp án (cắt rời)

**M1.** $Z_L = 50\ \Omega$, $Z_C = 10\ \Omega$; $Z = \sqrt{30^2 + 40^2} = 50{,}00\ \Omega$; $I = 2{,}000$ A; $\cos\varphi = 0{,}6000$; $P = I^2R = 120{,}0$ W; $\varphi = +53{,}13°$ ($u$ sớm pha hơn $i$).
- Gõ: `√(30²+(50−10)²)`; `100÷Ans`; `30÷50`; `2²×30`.

**M2.** $Z_L = 40\ \Omega$ nên cộng hưởng khi $Z_C = 40\ \Omega$: $C = \dfrac{1}{\omega Z_C} = 79{,}58\ \mu$F. $I = \dfrac{U}{R} = 6{,}000$ A; $P = \dfrac{U^2}{R} = 720{,}0$ W.
- Gõ: `1÷(100π×40)×10^6`.

**M3.** $I = \dfrac{P}{U\cos\varphi} = 12{,}50$ A; $\Delta P = I^2r = 3125$ W; $H = 1 - \dfrac{3125}{500000} = 99{,}38\%$.
- Gõ: `500000÷(50000×0.8)`; `12.5²×20`.

**M4.** $Z_L = \dfrac{R^2 + Z_C^2}{Z_C} = \dfrac{625}{15} = 41{,}67\ \Omega$; $L = \dfrac{Z_L}{\omega} = 0{,}1326$ H; $U_{L\,max} = \dfrac{U\sqrt{R^2 + Z_C^2}}{R} = \dfrac{80\cdot25}{20} = 100{,}0$ V.
- Gõ: `(20²+15²)÷15`; `÷(100π)`; `80×√(20²+15²)÷20`.
