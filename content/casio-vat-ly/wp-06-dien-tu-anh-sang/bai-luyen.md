# 12 bài luyện · Điện từ và ánh sáng (WP-06)

Mức: ⭐ cơ bản · ⭐⭐ đúng cấp thi · ⭐⭐⭐ phân loại. Làm tròn tạm **4 chữ số có nghĩa**; khi cần, $c = 3.10^8$ m/s. Đáp số sinh từ `tinh.py`. Quy trình bấm máy theo `../wp-01-so-tay-fx580vnx/so-tay.md` (đã đối chiếu sách hướng dẫn chính hãng fx-580VN X; thầy đã thử máy thật 19/10/2026).

---

## Q1 ⭐ Mạch dao động LC
**Đề.** Mạch LC có $L = 2$ mH, $C = 0{,}5\ \mu$F, điện tích cực đại $Q_0 = 2\ \mu$C. Tính $\omega$, $T$, $f$, $I_0$, $U_0$ và năng lượng dao động.
**Đáp số.** $\omega = 3{,}162.10^4$ rad/s; $T = 1{,}987.10^{-4}$ s; $f = 5033$ Hz; $I_0 = 0{,}06325$ A; $U_0 = 4{,}000$ V; $W = 4{,}000.10^{-6}$ J.
**Bấm máy**
- `1÷√(2×10^−3×0.5×10^−6)`, `STO D`.
- `2π÷D`; `D÷(2π)`; `D×2×10^−6`; `2×10^−6÷(0.5×10^−6)`; `(2×10^−6)²÷(2×0.5×10^−6)`.
**Bẫy.** mH → $10^{-3}$ H, μF → $10^{-6}$ F.

## Q2 ⭐ Sóng điện từ và mạch chọn sóng
**Đề.** (a) Đài phát sóng $90$ MHz: tính bước sóng. (b) Cuộn cảm $L = 1\ \mu$H cần tụ điện dung bao nhiêu để thu sóng đó?
**Đáp số.** (a) $\lambda = 3{,}333$ m. (b) $C = 3{,}127$ pF.
**Bấm máy**
- `3×10^8÷(90×10^6)`.
- $C = \dfrac{1}{4\pi^2f^2L}$: `1÷((2π×90×10^6)²×10^−6)×10^12`.
**Bẫy.** Cộng hưởng khi $f_{mạch} = f_{sóng}$; hoặc dùng $C = \dfrac{1}{L}\left(\dfrac{\lambda}{2\pi c}\right)^2$. Hai cách cho cùng kết quả.

## Q3 ⭐ Khoảng vân, vân sáng và vân tối
**Đề.** Y-âng: $\lambda = 0{,}6\ \mu$m, $a = 1$ mm, $D = 2$ m. Tính khoảng vân, vị trí vân sáng bậc 3 và vân tối thứ 3 (tính từ vân trung tâm, một phía).
**Đáp số.** $i = 1{,}200$ mm; vân sáng bậc 3: $3{,}600$ mm; vân tối thứ 3: $3{,}000$ mm ($= 2{,}5i$).
**Bấm máy**
- `0.6×10^−6×2÷(10^−3)×10^3` → $1{,}2$ mm, `STO D`.
- `3×D`; `2.5×D`.
**Bẫy.** Vân tối thứ 3 ở $2{,}5i$ (không phải $3{,}5i$ và không phải $3i$).

## Q4 ⭐ Khúc xạ và góc giới hạn
**Đề.** Tia sáng từ không khí tới mặt thuỷ tinh $n = 1{,}5$ với góc tới $40°$. Tính góc khúc xạ. Tính góc giới hạn phản xạ toàn phần khi ánh sáng đi từ thuỷ tinh ra không khí.
**Đáp số.** $r = 25{,}37°$; $i_{gh} = 41{,}81°$.
**Bấm máy**
- Độ. `sin⁻¹(sin(40)÷1.5)`; `sin⁻¹(1÷1.5)`.
**Bẫy.** Sang môi trường chiết quang kém hơn mới có phản xạ toàn phần.

## Q5 ⭐⭐ Thời gian ngắn nhất trong mạch LC
**Đề.** Mạch LC có $L = 0{,}4$ mH, $C = 0{,}9\ \mu$F. Tại $t = 0$ tụ tích điện cực đại. Tính chu kì, thời gian ngắn nhất để điện tích giảm còn một nửa, và thời gian ngắn nhất để năng lượng điện bằng năng lượng từ.
**Đáp số.** $T = 1{,}192.10^{-4}$ s; $t_1 = \dfrac{T}{6} = 1{,}987.10^{-5}$ s; $t_2 = \dfrac{T}{8} = 1{,}490.10^{-5}$ s.
**Bấm máy**
- `2π√(0.4×10^−3×0.9×10^−6)`, `STO D`; `D÷6`; `D÷8`.
- Kiểm bằng SOLVE (Rad): `cos(2π÷D×x) = 0.5` (x là phím `x`), giá trị đầu `10^−5`.
**Bẫy.** $W_đ = W_t$ khi $|q| = \dfrac{Q_0}{\sqrt2}$ (không phải $\dfrac{Q_0}{2}$): góc quay $\dfrac{\pi}{4}$, tức $\dfrac{T}{8}$.

## Q6 ⭐⭐ Tụ xoay trong mạch chọn sóng
**Đề.** Mạch chọn sóng có $L = 2\ \mu$H, tụ xoay $C$ tăng bậc nhất theo góc xoay từ $10$ pF ($0°$) đến $250$ pF ($180°$). (a) Dải bước sóng thu được. (b) Góc xoay để thu sóng $25$ m.
**Đáp số.** (a) $\lambda_{min} = 8{,}430$ m; $\lambda_{max} = 42{,}15$ m. (b) $C = 87{,}95$ pF; $\theta = 58{,}46°$.
**Bấm máy**
- $\lambda = 2\pi c\sqrt{LC}$: `2π×3×10^8×√(2×10^−6×10×10^−12)`; rồi với `250×10^−12`.
- $C = \dfrac{1}{L}\left(\dfrac{\lambda}{2\pi c}\right)^2$: `(25÷(2π×3×10^8))²÷(2×10^−6)×10^12` $= 87{,}95$ pF.
- `180×(87.95−10)÷(250−10)`.
**Bẫy.** $\theta$ bậc nhất theo $C$, không theo $\lambda$ (dùng tỉ lệ $\lambda$ cho $\theta$ là sai).

## Q7 ⭐⭐ Đếm vân trong trường giao thoa
**Đề.** Y-âng: $\lambda = 0{,}5\ \mu$m, $a = 0{,}8$ mm, $D = 1{,}6$ m. Trường giao thoa rộng $21{,}5$ mm, đối xứng qua vân trung tâm. Đếm số vân sáng và vân tối.
**Đáp số.** $i = 1{,}000$ mm; $21$ vân sáng; $22$ vân tối.
**Bấm máy**
- `0.5×10^−6×1.6÷(0.8×10^−3)×10^3` $= 1$ mm.
- $\dfrac{L}{2i} = 10{,}75$: vân sáng $2\times10 + 1 = 21$.
- Vân tối: $\left(k+\tfrac12\right)\cdot 1 \leq 10{,}75$ nên $k = 0,\dots,10$: 11 mỗi bên, tổng $22$.
**Bẫy.** Phần thập phân $0{,}75 > 0{,}5$ nên số vân tối (22) lớn hơn số vân sáng (21).

## Q8 ⭐⭐ Hai bức xạ, vân trùng
**Đề.** Y-âng: $a = 1{,}2$ mm, $D = 1{,}8$ m, $\lambda_1 = 0{,}48\ \mu$m, $\lambda_2 = 0{,}64\ \mu$m. Tìm vị trí vân sáng trùng gần vân trung tâm nhất và số vân sáng trùng trong trường rộng $30$ mm (đối xứng, kể cả vân trung tâm).
**Đáp số.** $i_1 = 0{,}7200$ mm; $i_2 = 0{,}9600$ mm; $\dfrac{k_1}{k_2} = \dfrac{4}{3}$; $x = 2{,}880$ mm; $11$ vân trùng.
**Bấm máy**
- `0.64÷0.48` $= \dfrac43$ (dạng phân số tối giản $\dfrac43$).
- `4×0.72` $= 2{,}88$ mm; kiểm `3×0.96`.
- Số vân trùng: $2\lfloor\dfrac{15}{2{,}88}\rfloor + 1 = 2\times5 + 1 = 11$.
**Bẫy.** Phải rút gọn phân số: nếu lấy $k_1 : k_2 = 0{,}64 : 0{,}48$ không rút gọn sẽ cho vị trí sai.

## Q9 ⭐⭐ Dịch màn, tìm bước sóng
**Đề.** Y-âng: $a = 1{,}5$ mm. Khi dịch màn ra xa thêm $0{,}75$ m thì khoảng vân tăng từ $0{,}9$ mm lên $1{,}2$ mm. Tìm $\lambda$ và khoảng cách ban đầu từ hai khe tới màn.
**Đáp số.** $\lambda = 0{,}6000\ \mu$m; $D = 2{,}250$ m.
**Bấm máy**
- `1.5×10^−3×0.3×10^−3÷0.75×10^6` $= 0{,}6\ \mu$m.
- `0.9×10^−3×1.5×10^−3÷(0.6×10^−6)`.
**Bẫy.** $\Delta i = \dfrac{\lambda\Delta D}{a}$; dùng $i_{sau}$ thay $\Delta i$ là sai.

## Q10 ⭐⭐ Tán sắc qua lăng kính
**Đề.** Lăng kính góc chiết quang $A = 6°$, chiết suất $n_{đỏ} = 1{,}642$, $n_{tím} = 1{,}685$. Chùm sáng trắng hẹp tới gần pháp tuyến mặt bên (dùng công thức góc nhỏ $D = (n-1)A$ cho góc lệch). Tính góc lệch tia đỏ, tia tím và bề rộng quang phổ trên màn vuông góc đặt cách lăng kính $2$ m.
**Đáp số.** $D_đ = 3{,}852°$; $D_t = 4{,}110°$; chênh $0{,}2580°$; bề rộng $9{,}050$ mm (gần đúng góc nhỏ: $9{,}006$ mm).
**Bấm máy**
- `(1.642−1)×6`; `(1.685−1)×6`.
- Độ: `2×(tan(4.11) − tan(3.852))×1000` $= 9{,}050$ mm.
**Bẫy.** Công thức $D = (n-1)A$ chỉ dùng khi $A$ nhỏ và tia tới gần pháp tuyến; kết quả hai cách tính khác nhau cỡ $0{,}5\%$, đề cho cách nào dùng cách đó.

## Q11 ⭐⭐⭐ Ghép tụ
**Đề.** Cuộn cảm $L = 1$ mH nối với tụ $C_1$ thì tần số dao động $12$ kHz, nối với tụ $C_2$ thì $16$ kHz. Tìm $C_1$, $C_2$, và tần số khi dùng $L$ với (a) hai tụ nối tiếp, (b) hai tụ song song.
**Đáp số.** $C_1 = 0{,}1759\ \mu$F; $C_2 = 0{,}09895\ \mu$F; (a) $f = 20{,}00$ kHz; (b) $f = 9{,}600$ kHz.
**Bấm máy**
- `1÷((2π×12000)²×10^−3)×10^6`; tương tự với `16000`.
- (a) `√(12²+16²)`; (b) `12×16÷√(12²+16²)`.
- Kiểm bằng điện dung: nối tiếp $C = \dfrac{C_1C_2}{C_1+C_2}$ rồi $f = \dfrac{1}{2\pi\sqrt{LC}}$.
**Bẫy.** Nối tiếp thì $f$ tăng ($20 > 16$), song song thì $f$ giảm ($9{,}6 < 12$). Nhầm hai trường hợp là lỗi phổ biến.

## Q12 ⭐⭐⭐ Ánh sáng trắng, đếm bức xạ
**Đề.** Y-âng: $a = 1$ mm, $D = 2$ m, ánh sáng trắng $0{,}38\ \mu\text{m} \leq \lambda \leq 0{,}76\ \mu$m. Tại điểm $M$ cách vân trung tâm $7{,}0$ mm, có bao nhiêu bức xạ cho vân sáng, bao nhiêu bức xạ cho vân tối? Nêu bước sóng.
**Đáp số.** 5 bức xạ vân sáng: $0{,}7000$; $0{,}5833$; $0{,}5000$; $0{,}4375$; $0{,}3889\ \mu$m (ứng $k = 5, \dots, 9$).
4 bức xạ vân tối: $0{,}6364$; $0{,}5385$; $0{,}4667$; $0{,}4118\ \mu$m (ứng $k = 5, \dots, 8$).
**Bấm máy**
- Vân sáng: TABLE `f(x) = 3.5÷x` (đơn vị μm, vì $ax/D = 3{,}5\ \mu$m), Start `4`, End `10`, Step `1`; lọc $0{,}38 \leq f \leq 0{,}76$: $x=5\dots9$.
- Vân tối: `f(x) = 3.5÷(x+0.5)`, Start `4`, End `10`: lọc: $x=5\dots8$.
**Bẫy.** $ax/D = 10^{-3}\cdot 7\cdot10^{-3}/2 = 3{,}5\cdot 10^{-6}$ m $= 3{,}5\ \mu$m. Kiểm $k=4$ cho vân sáng ($0{,}875\ \mu$m) và vân tối ($0{,}7778\ \mu$m) đều ngoài vùng nhìn thấy; $k=10$ vân sáng ($0{,}35\ \mu$m) và $k=9$ vân tối ($0{,}3684\ \mu$m) cũng ngoài.
