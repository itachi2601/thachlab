# Chuyên đề 4 · Dao động và sóng điện từ, sóng ánh sáng: ba trang kỹ thuật (WP-06)

> Công cụ máy: `../wp-01-so-tay-fx580vnx/so-tay.md`. Mỗi công thức ghi kèm điều kiện áp dụng. Khi cần $c$, đề cho $c = 3.10^8$ m/s; thể lệ tạm: làm tròn 4 chữ số có nghĩa.

---

## Trang 1 · Mạch dao động LC và sóng điện từ

**Mạch LC lí tưởng** (không điện trở, không bức xạ)
- $\omega = \dfrac{1}{\sqrt{LC}}$; $T = 2\pi\sqrt{LC}$; $f = \dfrac{1}{2\pi\sqrt{LC}}$.
- $q = Q_0\cos(\omega t + \varphi)$; $i = q' = -\omega Q_0\sin(\omega t + \varphi)$ nên $I_0 = \omega Q_0$; $U_0 = \dfrac{Q_0}{C}$.
- Hệ thức: $I_0 = \omega Q_0 = U_0\sqrt{\dfrac{C}{L}}$.
- Năng lượng: $W = \dfrac{Q_0^2}{2C} = \dfrac12 CU_0^2 = \dfrac12 LI_0^2$ **không đổi**. Năng lượng điện và từ biến thiên với chu kì $\dfrac{T}{2}$.
- Thời gian ngắn nhất (tính trong mạch lí tưởng, từ lúc $q = Q_0$):
  - $q$ giảm từ $Q_0$ xuống $\dfrac{Q_0}{2}$: $\dfrac{T}{6}$.
  - $q$ giảm từ $Q_0$ xuống $0$: $\dfrac{T}{4}$.
  - $W_đ$ bằng $W_t$ lần đầu: $\dfrac{T}{8}$.

**Ghép tụ** (cùng cuộn cảm $L$): từ $\dfrac{1}{f^2} = 4\pi^2LC$:
- Hai tụ **song song**: $C = C_1 + C_2$ nên $\dfrac{1}{f^2} = \dfrac{1}{f_1^2} + \dfrac{1}{f_2^2}$.
- Hai tụ **nối tiếp**: $\dfrac{1}{C} = \dfrac{1}{C_1} + \dfrac{1}{C_2}$ nên $f^2 = f_1^2 + f_2^2$.
(Đừng nhầm hai trường hợp: tụ song song làm $f$ **giảm**, nối tiếp làm $f$ **tăng**.)

**Sóng điện từ**
- $\lambda = \dfrac{c}{f} = cT$ (trong chân không/không khí).
- Mạch chọn sóng thu cộng hưởng khi $f_{mạch} = f_{sóng}$: $\lambda = 2\pi c\sqrt{LC}$.
- Tụ xoay có điện dung tăng **bậc nhất** theo góc xoay $\theta$ từ $0°$ đến $180°$: $C(\theta) = C_{min} + \dfrac{\theta}{180°}(C_{max} - C_{min})$.
  - Khi đó $C$ tăng đều nhưng $\lambda \propto \sqrt{C}$ **không** tăng đều theo $\theta$.

**Thao tác máy**
- Lưu $\omega$ vào `D` (không dùng `A` nếu đang lưu biên độ).
- Khi viết $10^{-12}$ dùng `×10^−12`, tránh nhầm với `E`.

**Bẫy**
- Đổi mH, μF, pF về H, F trước khi thế.
- $T = 2\pi\sqrt{LC}$ là chu kì dao động điện; chu kì biến thiên của năng lượng là $\dfrac{T}{2}$.

---

## Trang 2 · Giao thoa ánh sáng (Y-âng)

**Công thức**
- Khoảng vân: $i = \dfrac{\lambda D}{a}$.
- Vân sáng: $x_k = ki$ ($k$ nguyên, $k = 0$ là vân trung tâm).
- Vân tối: $x = \left(k + \dfrac12\right)i$ ($k$ nguyên). **Vân tối thứ $n$ tính từ trung tâm ứng $k = n - 1$**, tức $x = \left(n - \dfrac12\right)i$ (vân tối thứ 3 ở $2{,}5i$).
- Khoảng cách giữa vân sáng bậc $m$ và vân tối thứ $n$: cùng phía $|mi - (n - \tfrac12)i|$; khác phía $(m + n - \tfrac12)i$.

**Đếm vân trong trường giao thoa** (rộng $L$, **đối xứng** qua vân trung tâm)
- Vân sáng: mọi $k$ nguyên có $|ki| \leq \dfrac{L}{2}$: số vân sáng $= 2\left\lfloor \dfrac{L}{2i}\right\rfloor + 1$.
- Vân tối: mọi $k$ nguyên có $\left|(k + \tfrac12)i\right| \leq \dfrac{L}{2}$: đếm các giá trị $k = 0, 1, 2, \dots$ rồi nhân đôi.
- Nếu vân nằm đúng mép trường thì đề thường nói "kể cả"/"không kể".

**Nhiều bức xạ**
- Vân sáng trùng nhau của hai bức xạ: $k_1\lambda_1 = k_2\lambda_2$, $\dfrac{k_1}{k_2} = \dfrac{\lambda_2}{\lambda_1}$. **Rút gọn về phân số tối giản** $\dfrac{p}{q}$: vân trùng đầu tiên (khác trung tâm) ở $x = p\,i_1 = q\,i_2$; các vân trùng cách nhau $p\,i_1$.
- Số vân trùng trong trường $L$: $2\left\lfloor \dfrac{L}{2\,p\,i_1}\right\rfloor + 1$ (kể cả vân trung tâm).
- Ánh sáng trắng ($0{,}38 \leq \lambda \leq 0{,}76\ \mu$m): tại vị trí $x$, các bức xạ cho vân sáng có $\lambda = \dfrac{ax}{kD}$; cho vân tối có $\lambda = \dfrac{ax}{(k + \frac12)D}$. Đếm $k$ nguyên thoả khoảng $\lambda$.

**Thay đổi thiết bị**
- Dịch màn ra xa $\Delta D$: $\Delta i = \dfrac{\lambda\Delta D}{a}$ nên $\lambda = \dfrac{a\,\Delta i}{\Delta D}$.

**Thao tác máy**
- Vân trùng: TABLE với $f(x) = x\dfrac{\lambda_1}{\lambda_2}$ (x là phím `x`); tìm hàng đầu tiên có giá trị nguyên (kiểm bằng phân số tối giản).
- Ánh sáng trắng: TABLE $f(x) = \dfrac{a\,x_M}{xD}$ ($x_M$ là vị trí điểm xét) theo $x = k$ nguyên; lọc hàng nằm trong $[0{,}38; 0{,}76]$.

**Bẫy**
- Đổi $\mu$m, mm về m.
- Phần nguyên ($\lfloor\ \rfloor$) khi đếm, đừng làm tròn thường.

---

## Trang 3 · Khúc xạ, tán sắc, lăng kính

**Khúc xạ**
- $n_1\sin i = n_2\sin r$; $n = \dfrac{c}{v}$.
- Phản xạ toàn phần: ánh sáng đi từ môi trường chiết quang hơn ($n_1$) sang kém hơn ($n_2<n_1$) với góc tới $i \geq i_{gh}$, $\sin i_{gh} = \dfrac{n_2}{n_1}$. Nếu $i < i_{gh}$ thì vẫn có tia khúc xạ.

**Tán sắc**
- Chiết suất phụ thuộc bước sóng: $n_{tím} > n_{đỏ}$ nên tia tím lệch nhiều hơn.
- Lăng kính **góc chiết quang nhỏ**, tia tới gần pháp tuyến: góc lệch $D = (n - 1)A$.
- Bề rộng quang phổ trên màn vuông góc cách lăng kính $d$: $d\left(\tan D_{tím} - \tan D_{đỏ}\right)$; gần đúng góc nhỏ: $d\,(D_{tím} - D_{đỏ})$ (rad). Hai kết quả khác nhau cỡ 0,5%.

**Thao tác máy**
- Góc: đặt SETUP **Độ** cho $\sin^{-1}$, $\tan$ trên độ; đổi sang **Rad** khi cần $(n-1)A$ với $A$ bằng rad.
- Kiểm điều kiện phản xạ toàn phần trước khi tính $r$ (tính $i_{gh}$ trước).

**Bẫy**
- $\sin r > 1$ cho $\sin^{-1}$ lỗi: đó là dấu hiệu phản xạ toàn phần.
- Cộng góc lệch tia đỏ và tím dùng hiệu, không dùng tổng.
