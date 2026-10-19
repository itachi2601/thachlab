# Chuyên đề 3 · Điện xoay chiều RLC: ba trang kỹ thuật (WP-05)

> Công cụ máy: `../wp-01-so-tay-fx580vnx/so-tay.md`. Mỗi công thức ghi kèm điều kiện áp dụng. **Quy ước:** $U, I$ là giá trị hiệu dụng, $U_0, I_0$ là biên độ; số phức nhập cùng loại (hiệu dụng với hiệu dụng, biên độ với biên độ). Thể lệ tạm: làm tròn 4 chữ số có nghĩa.

---

## Trang 1 · Mạch RLC nối tiếp và số phức

**Công thức**
- $Z_L = \omega L$; $Z_C = \dfrac{1}{\omega C}$; $Z = \sqrt{R^2 + (Z_L - Z_C)^2}$; $I = \dfrac{U}{Z}$.
- $\tan\varphi = \dfrac{Z_L - Z_C}{R}$, $\varphi = \varphi_u - \varphi_i$.
  - $Z_L > Z_C$: $\varphi > 0$, $u$ **sớm** pha hơn $i$ (mạch cảm kháng).
  - $Z_L < Z_C$: $\varphi < 0$, $u$ **trễ** pha hơn $i$ (mạch dung kháng).
- $\cos\varphi = \dfrac{R}{Z}$; $P = UI\cos\varphi = I^2R$.
- Điện áp hai đầu từng phần tử: $U_R = IR$, $U_L = IZ_L$, $U_C = IZ_C$; $U^2 = U_R^2 + (U_L - U_C)^2$. $U_L$ hoặc $U_C$ **có thể lớn hơn** $U$.
- $u_R$ cùng pha với $i$; $u_L$ sớm pha $\dfrac{\pi}{2}$ so với $i$; $u_C$ trễ pha $\dfrac{\pi}{2}$ so với $i$.

**Số phức (Complex)**
- $Z = R + (Z_L - Z_C)\,\mathrm{i}$; $I = \dfrac{U}{Z}$ (cả hai nhập dạng cực $a\angle\varphi$).
- Cuộn dây có điện trở $r$: $Z_d = r + Z_L\mathrm{i}$.
- Hộp đen $X$ nối tiếp với phần tử đã biết: $Z_X = \dfrac{U}{I} - Z_{biết}$ (số phức), rồi đọc phần thực → $R$, phần ảo dương → $L$, phần ảo âm → $C$.

**Bẫy**
- Dạng phức chỉ cho đúng khi $U$ và $I$ cùng loại (cùng hiệu dụng hoặc cùng biên độ); tỉ số $\dfrac{U_0}{I_0} = \dfrac{U}{I}$ nên $Z$ giống nhau.
- Phần thực của $Z_X$ có thể ra âm do sai dữ liệu: kiểm lại dấu của pha.
- Góc $\varphi$ máy cho theo Độ hay Rad tuỳ SETUP.

---

## Trang 2 · Cực trị

**Cộng hưởng** (thay $\omega$, hoặc $L$, hoặc $C$ cho đến khi $Z_L = Z_C$)
- $\omega^2LC = 1$; $Z = R$; $I_{max} = \dfrac{U}{R}$; $P_{max} = \dfrac{U^2}{R}$; $\cos\varphi = 1$; $u$ cùng pha $i$.

**$R$ thay đổi** ($U, L, C, \omega$ cố định)
- Điện trở $R$ thuần, không cuộn dây điện trở: $P_{max}$ khi $R = |Z_L - Z_C|$; $P_{max} = \dfrac{U^2}{2|Z_L - Z_C|}$.
- Có cuộn dây điện trở $r$ nối tiếp với biến trở $R$, $d = |Z_L - Z_C|$:
  - **Công suất toàn mạch** cực đại khi $R + r = d$, **nếu $r < d$**; nếu $r \geq d$ thì $P$ giảm khi $R$ tăng nên cực đại tại $R = 0$.
  - **Công suất trên $R$** cực đại khi $R = \sqrt{r^2 + d^2}$, và $P_{R\,max} = \dfrac{U^2}{2(R + r)}$.
- Hai giá trị $R_1, R_2$ cho cùng $P$ (mạch **không** có $r$): $R_1R_2 = d^2$; $R_1 + R_2 = \dfrac{U^2}{P}$.
  - Có cuộn dây điện trở $r$ (tính $P$ toàn mạch): $(R_1 + r)(R_2 + r) = d^2$; $R_1 + R_2 + 2r = \dfrac{U^2}{P}$.

**$C$ thay đổi** ($R, L, \omega$ cố định)
- $U_C$ cực đại khi $Z_C = \dfrac{R^2 + Z_L^2}{Z_L}$; $U_{C\,max} = \dfrac{U\sqrt{R^2 + Z_L^2}}{R}$.
**$L$ thay đổi** ($R, C, \omega$ cố định)
- $U_L$ cực đại khi $Z_L = \dfrac{R^2 + Z_C^2}{Z_C}$; $U_{L\,max} = \dfrac{U\sqrt{R^2 + Z_C^2}}{R}$.

**$\omega$ thay đổi** ($R, L, C$ cố định)
- $U_C$ cực đại tại $\omega^2 = \dfrac{1}{LC} - \dfrac{R^2}{2L^2}$ **với điều kiện** $R^2 < \dfrac{2L}{C}$; $U_{C\,max} = \dfrac{2UL}{R\sqrt{4LC - R^2C^2}}$. (Nếu điều kiện không thoả, $U_C$ giảm theo $\omega$.)
- Hai tần số $\omega_1, \omega_2$ cho **cùng** $I$ (hay cùng $Z$, $P$, $\cos\varphi$): $\omega_1\omega_2 = \dfrac{1}{LC} = \omega_0^2$; hai pha đối nhau, $\varphi_1 = -\varphi_2$.

**Dùng TABLE để kiểm**
1. Nhập $f(x)$ (x là phím `x`) là đại lượng cần cực đại (ví dụ $U_C$ theo $Z_C$): bảng bước lớn, rồi thu hẹp.
2. Đáp số cuối ghi theo công thức, bảng chỉ để kiểm.

**Bẫy**
- $U_{C\,max}$ khi thay $C$ khác $U_C$ ở cộng hưởng: ở cộng hưởng $U_C = \dfrac{U}{R}\sqrt{\dfrac{L}{C}}$ chưa phải cực đại.
- Đừng áp công thức $R = |Z_L - Z_C|$ cho mạch có cuộn dây điện trở: phải cộng $r$.

---

## Trang 3 · Truyền tải điện, máy biến áp, máy phát

**Truyền tải điện** ($P$ là công suất nơi phát, $r$ là điện trở tổng của dây, $U$ là điện áp nơi phát, $\cos\varphi$ là hệ số công suất của tải)
- $I = \dfrac{P}{U\cos\varphi}$; $\Delta P = I^2r = \dfrac{P^2r}{U^2\cos^2\varphi}$; hiệu suất $H = 1 - \dfrac{\Delta P}{P}$.
- Khi $P, r, \cos\varphi$ không đổi: $\Delta P \propto \dfrac{1}{U^2}$.
- Bài toán "bao nhiêu hộ dân": công suất tải $= P - \Delta P$; chia cho công suất mỗi hộ; **làm tròn xuống** (không đủ cho hộ cuối).

**Máy biến áp lí tưởng**
- $\dfrac{U_2}{U_1} = \dfrac{N_2}{N_1} = \dfrac{I_1}{I_2}$.
- Có hiệu suất $H$: $P_2 = H\,P_1$. Cường độ phía sơ cấp: $I_1 = \dfrac{P_1}{U_1\cos\varphi_1}$ ($\cos\varphi_1 = 1$ nếu đề không nói).

**Máy phát điện xoay chiều**
- $f = np$ ($n$ vòng/s, $p$ cặp cực); $E_0 = \omega N\Phi_0$, $E = \dfrac{E_0}{\sqrt2}$.

**Bẫy**
- $\cos\varphi$ có bình phương trong $\Delta P$: bỏ quên là sai.
- Công suất nơi phát (đầu đường dây) khác công suất nhận (tải).
