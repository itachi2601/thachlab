# 12 bài luyện · Điện xoay chiều (WP-05)

Mức: ⭐ cơ bản · ⭐⭐ đúng cấp thi · ⭐⭐⭐ phân loại. Làm tròn tạm **4 chữ số có nghĩa**. Đáp số sinh từ `tinh.py`. Quy trình bấm máy theo `../wp-01-so-tay-fx580vnx/so-tay.md`, **chưa thử trên máy thật**. Biến nhớ: dùng `D` cho $\omega$, tránh trùng ký hiệu đại lượng.

---

## E1 ⭐ Mạch RLC nối tiếp
**Đề.** Đặt $u = 200\sqrt2\cos(100\pi t)$ (V) vào mạch nối tiếp $R = 60\ \Omega$, $L = \dfrac{0{,}4}{\pi}$ H, $C = \dfrac{250}{3\pi}\ \mu$F. Tính $Z_L$, $Z_C$, $Z$, $I$, $\cos\varphi$, $P$, $U_R$, $U_L$, $U_C$ và độ lệch pha của $u$ so với $i$.
**Đáp số.** $Z_L = 40{,}00\ \Omega$; $Z_C = 120{,}0\ \Omega$; $Z = 100{,}0\ \Omega$; $I = 2{,}000$ A; $\cos\varphi = 0{,}6000$; $P = 240{,}0$ W; $U_R = 120{,}0$ V; $U_L = 80{,}00$ V; $U_C = 240{,}0$ V; $\varphi = -53{,}13°$ ($u$ trễ pha hơn $i$).
**Bấm máy**
- `100π×0.4÷π` → $40$; `1÷(100π×250×10^−6÷(3π))` → $120$.
- `√(60²+(40−120)²)` → $100$; `200÷100` → $2$.
- `60÷100`; `2²×60`; Độ: `tan⁻¹((40−120)÷60)`.
**Bẫy.** $U_C = 240\ \text{V} > U = 200\ \text{V}$ là bình thường, không phải sai.

## E2 ⭐ Cộng hưởng
**Đề.** Mạch RLC nối tiếp $R = 25\ \Omega$, $L = 0{,}5$ H, $C = 20\ \mu$F, $U = 100$ V, tần số thay đổi. Tìm tần số cộng hưởng, $I$, $P$ và $U_C$ tại cộng hưởng.
**Đáp số.** $f_0 = 50{,}33$ Hz; $I = 4{,}000$ A; $P = 400{,}0$ W; $U_C = 632{,}5$ V.
**Bấm máy**
- `1÷(2π√(0.5×20×10^−6))` → `STO F`.
- `100÷25`; `100²÷25`.
- $U_C = I\cdot Z_C$: `4×1÷(2π×F×20×10^−6)`.
**Bẫy.** $U_C \gg U$ ở cộng hưởng khi $R$ nhỏ: nguy hiểm trong thực tế.

## E3 ⭐ Hao phí truyền tải
**Đề.** Nhà máy truyền đi công suất $100$ kW ở điện áp $10$ kV, $\cos\varphi = 0{,}9$, điện trở tổng dây $10\ \Omega$. Tính công suất hao phí và hiệu suất truyền tải. Nếu tăng điện áp lên gấp đôi (các đại lượng khác không đổi) thì sao?
**Đáp số.** $\Delta P = 1235$ W; $H = 98{,}77\%$; sau khi tăng: $\Delta P = 308{,}6$ W; $H = 99{,}69\%$.
**Bấm máy**
- `(100000²×10)÷(10000²×0.9²)`; `1−Ans÷100000`.
- Gấp đôi $U$: `Ans÷4` ở bước hao phí.
**Bẫy.** Đổi kW, kV về W, V trước khi tính; có $\cos^2\varphi$ ở mẫu.

## E4 ⭐ Máy biến áp
**Đề.** Máy biến áp có $N_1 = 1100$ vòng, $N_2 = 60$ vòng, $U_1 = 220$ V, tải $4\ \Omega$ ở thứ cấp, hiệu suất $90\%$ (coi $\cos\varphi_1 = 1$). Tính $U_2$, $I_2$, công suất thứ cấp, công suất sơ cấp và $I_1$.
**Đáp số.** $U_2 = 12{,}00$ V; $I_2 = 3{,}000$ A; $P_2 = 36{,}00$ W; $P_1 = 40{,}00$ W; $I_1 = 0{,}1818$ A.
**Bấm máy**
- `220×60÷1100`; `Ans÷4`; `12×3`; `36÷0.9`; `40÷220`.
**Bẫy.** Với hiệu suất < 100%, $I_1 \neq I_2\dfrac{N_2}{N_1}$ (kết quả đó là $0{,}1636$ A, sai).

## E5 ⭐⭐ Biểu thức dòng điện bằng số phức
**Đề.** Đặt $u = 120\sqrt2\cos(100\pi t)$ (V) vào mạch nối tiếp $R = 40\ \Omega$, $Z_L = 130\ \Omega$, $Z_C = 60\ \Omega$. Viết biểu thức $i$, $u_L$ và $u_C$.
**Đáp số.** $Z = 80{,}62\ \Omega$; $I_0 = 2{,}105$ A ($I = 1{,}488$ A).
$i = 2{,}105\cos(100\pi t - 1{,}052)$ A.
$u_L = 273{,}6\cos(100\pi t + 0{,}5191)$ V.
$u_C = 126{,}3\cos(100\pi t - 2{,}622)$ V.
**Bấm máy**
- Số phức, **Rad**. Gõ `(120√2∠0) ÷ (40+70i)`, `=`, dạng r∠θ: $2{,}105\angle -1{,}052$.
- $u_L$: biên độ $2{,}105\times130$; pha $-1{,}052 + \dfrac{\pi}{2}$.
- $u_C$: biên độ $2{,}105\times60$; pha $-1{,}052 - \dfrac{\pi}{2}$.
**Bẫy.** Dùng biên độ của $u$ thì ra biên độ của $i$ (không phải hiệu dụng). $u_L$ sớm pha $\dfrac{\pi}{2}$ so với $i$, không so với $u$.

## E6 ⭐⭐ Cuộn dây có điện trở, biến trở $R$
**Đề.** Cuộn dây $r = 10\ \Omega$, $Z_L = 70\ \Omega$ nối tiếp biến trở $R$ và tụ $Z_C = 30\ \Omega$; $U = 120$ V. (a) Tìm $R$ để công suất toàn mạch cực đại và giá trị đó. (b) Tìm $R$ để công suất trên $R$ cực đại và giá trị đó.
**Đáp số.** (a) $R = 30{,}00\ \Omega$; $P_{max} = 180{,}0$ W. (b) $R = 41{,}23\ \Omega$; $P_{R\,max} = 140{,}5$ W.
**Bấm máy**
- $d = 70 - 30 = 40$. (a): `40−10`; `120²÷(2×40)`.
- (b): `√(10²+40²)` → `STO D`; `120²÷(2×(D+10))`.
- Kiểm bằng TABLE: `f(X) = 120²×X÷((X+10)²+40²)`, Start `30`, End `50`, Step `1`: lớn nhất quanh $X = 41$.
**Bẫy.** (a) ĐK $r < d$ thoả ($10 < 40$). Nếu $r \geq 40$ thì $R=0$. Hai ý (a), (b) cho hai kết quả $R$ khác nhau, đừng lẫn.

## E7 ⭐⭐ $C$ thay đổi, $U_C$ cực đại
**Đề.** Mạch $R = 30\ \Omega$, $Z_L = 40\ \Omega$, $U = 100$ V, $\omega = 100\pi$ rad/s, $C$ thay đổi. Tìm $Z_C$, $C$ và $U_{C\,max}$.
**Đáp số.** $Z_C = 62{,}50\ \Omega$; $C = 50{,}93\ \mu$F; $U_{C\,max} = 166{,}7$ V.
**Bấm máy**
- `(30²+40²)÷40` → $62{,}5$, `STO D`.
- `1÷(100π×D)×10^6` → $50{,}93\ \mu$F.
- `100×√(30²+40²)÷30`.
- Kiểm: TABLE `f(X) = 100X÷√(30²+(40−X)²)`, Start `50`, End `75`, Step `2.5`.
**Bẫy.** Đây không phải cộng hưởng ($Z_C = 40$ sẽ cho $U_C = 133{,}3$ V, nhỏ hơn).

## E8 ⭐⭐ $L$ thay đổi, $U_L$ cực đại
**Đề.** Mạch $R = 40\ \Omega$, $Z_C = 30\ \Omega$, $U = 100$ V, $\omega = 100\pi$ rad/s, $L$ thay đổi. Tìm $Z_L$, $L$ và $U_{L\,max}$.
**Đáp số.** $Z_L = 83{,}33\ \Omega$; $L = 0{,}2653$ H; $U_{L\,max} = 125{,}0$ V.
**Bấm máy**
- `(40²+30²)÷30` → `STO D`; `D÷(100π)`; `100×√(40²+30²)÷40`.
**Bẫy.** Nhập $Z_L$ vào $L$ cần chia cho $\omega$.

## E9 ⭐⭐ $\omega$ thay đổi, $U_C$ cực đại
**Đề.** Mạch nối tiếp $R = 20\ \Omega$, $L = 0{,}1$ H, $C = 20\ \mu$F, $U = 100$ V, tần số thay đổi. Tìm $\omega$ và $f$ để $U_C$ cực đại, và $U_{C\,max}$. So với $U_C$ ở cộng hưởng.
**Đáp số.** Điều kiện $R^2 = 400 < \dfrac{2L}{C} = 10000$ thoả. $\omega = 692{,}8$ rad/s; $f = 110{,}3$ Hz; $U_{C\,max} = 357{,}1$ V (ở cộng hưởng chỉ $353{,}6$ V).
**Bấm máy**
- `√(1÷(0.1×20×10^−6) − 20²÷(2×0.1²))` → $692{,}8$; `÷(2π)`.
- `100×2×0.1÷(20×√(4×0.1×20×10^−6 − 20²×(20×10^−6)²))`.
**Bẫy.** $\omega_{U_C max} \neq \omega_0$ (với $R\neq0$); chỉ gần nhau khi $R$ nhỏ.

## E10 ⭐⭐ Hộp đen nối tiếp với tụ
**Đề.** Hộp $X$ (chứa $R$ nối tiếp $L$) nối tiếp với tụ $Z_C = 100\ \Omega$. Đặt $u = 200\cos(100\pi t)$ (V) thì $i = 2\cos\left(100\pi t + \dfrac{\pi}{4}\right)$ (A). Tìm $R$ và $L$ của hộp $X$.
**Đáp số.** $Z_{tổng} = 70{,}71 - 70{,}71\mathrm{i}\ (\Omega)$; $Z_X = 70{,}71 + 29{,}29\mathrm{i}\ (\Omega)$; $R = 70{,}71\ \Omega$; $L = 0{,}09323$ H.
**Bấm máy**
- Số phức, **Độ**. `(200∠0) ÷ (2∠45)`, `=`: $100\angle -45$.
- Chuyển a+bi: $70{,}71 - 70{,}71\mathrm{i}$. Cộng `+100i`: $70{,}71 + 29{,}29\mathrm{i}$.
- $L$: `29.29÷(100π)` (dùng `Ans` phần ảo cho đủ chữ số).
**Bẫy.** $Z_{tổng} = Z_X + Z_C$ với $Z_C = -100\mathrm{i}$, nên $Z_X = Z_{tổng} + 100\mathrm{i}$.

## E11 ⭐⭐⭐ Hai tần số cho cùng cường độ
**Đề.** Mạch nối tiếp $R = 30\ \Omega$, $L = 0{,}2$ H; $U = 60$ V. Khi $f_1 = 40$ Hz hoặc $f_2 = 90$ Hz thì dòng điện hiệu dụng như nhau. Tìm tần số cộng hưởng, $C$, và (tại $f_1$) $Z$, $I$, $\cos\varphi$, $\varphi$; so sánh với $f_2$.
**Đáp số.** $f_0 = 60{,}00$ Hz; $C = 35{,}18\ \mu$F; $Z = 69{,}63\ \Omega$; $I = 0{,}8617$ A; $\cos\varphi = 0{,}4309$; $\varphi_1 = -64{,}48°$, $\varphi_2 = +64{,}48°$ (cùng $Z$, cùng $I$, pha đối nhau).
**Bấm máy**
- `√(40×90)` → $60$; `1÷((2π×60)²×0.2)×10^6` → `STO C`.
- `CALC` công thức $Z(f) = \sqrt{30^2 + (2\pi f\,0{,}2 - \dfrac{1}{2\pi f\,C})^2}$ với $f = 40$ rồi $f = 90$: hai kết quả bằng nhau.
- `60÷Z`; `30÷Z`.
**Lời giải.** $\omega_1\omega_2 = \dfrac{1}{LC} = \omega_0^2$ nên $f_0 = \sqrt{f_1f_2}$.
**Bẫy.** Hệ thức chỉ cho đúng khi $I$ (hay $Z$) bằng nhau tại hai tần số; không dùng cho hai tần số bất kì.

## E12 ⭐⭐⭐ Số hộ dân được cấp điện
**Đề.** Trạm phát giữ công suất nơi phát và $\cos\varphi$ không đổi. Khi truyền với điện áp $2$ kV thì cấp đủ cho $100$ hộ và hao phí trên dây bằng $20\%$ công suất nơi phát. Nếu tăng điện áp lên $4$ kV thì cấp đủ cho tối đa bao nhiêu hộ (mỗi hộ tiêu thụ như nhau)?
**Đáp số.** Hao phí còn $5\%$; công suất tới tải $0{,}95P$ so với $0{,}8P$ trước; $n = 100\cdot\dfrac{0{,}95}{0{,}8} = 118{,}75$, vậy **118 hộ**.
**Bấm máy**
- `20÷4` → $5\%$ (hao phí tỉ lệ nghịch bình phương $U$: $\dfrac{2^2}{4^2} = \dfrac14$).
- `100×(1−0.05)÷(1−0.2)` → $118{,}75$.
**Bẫy.** Làm tròn **xuống**: với $119$ hộ không đủ điện. Dùng hao phí $= 20\%/2$ (nhầm tỉ lệ nghịch $U$) cho đáp số sai.
