# 20 bài luyện thao tác fx-580VN X (WP-01)

Mục đích: **luyện phím và thói quen**, chưa phải mức đề thi. Mọi đáp số sinh từ `tinh.py` (chạy lại để kiểm). Quy tắc làm tròn dùng tạm: **4 chữ số có nghĩa** (chờ thể lệ, WP-02).
Mức: ⭐ cơ bản · ⭐⭐ đúng cấp thi. Quy trình bấm máy theo `so-tay.md`, đã đối chiếu sách hướng dẫn chính hãng fx-580VN X và thầy đã thử máy thật (19/10/2026).

---

## A. SOLVE

### S1 ⭐⭐ Thời điểm vật qua li độ 2 cm
**Đề.** Vật dao động $x = 4\cos\left(5\pi t - \dfrac{\pi}{3}\right)$ (cm, s). Tìm thời điểm đầu tiên $t > 0$ vật có $x = 2$ cm.
**Đáp số.** $t = 0{,}1333$ s (đúng $\dfrac{2}{15}$ s).
**Bấm máy**
- SETUP: đơn vị góc **Rad**.
- Gõ `4cos(5πx − π÷3) = 2` (x là phím `x`).
- `SHIFT CALC` (SOLVE), giá trị đầu x = `0.1`, bấm `=`, rồi bấm `=` thêm một lần để giải.
- Lưu ý: $t = 0$ cũng thoả $x(0)=2$ nhưng đề cần $t>0$. Giá trị đầu gần 0 có thể làm máy trả về $t = 0$ hoặc nghiệm âm: khi đó đổi giá trị đầu sang `0.1`.
**Lời giải.** $\cos\left(5\pi t - \frac{\pi}{3}\right) = \frac12$ nên $5\pi t - \frac{\pi}{3} = \pm\frac{\pi}{3} + 2k\pi$. Nghiệm dương nhỏ nhất: $5\pi t = \frac{2\pi}{3}$, $t = \frac{2}{15}$ s.
**Bẫy.** Để máy ở Độ thì ra số vô nghĩa. Giá trị đầu khác nhau cho nghiệm khác nhau.

### S2 ⭐ Nhiệt độ cân bằng
**Đề.** Thả cục nhôm 0,3 kg ở 100 °C ($c = 880$ J/kg.K) vào 0,5 kg nước ở 20 °C ($c = 4180$ J/kg.K). Bỏ qua mất mát nhiệt. Tìm nhiệt độ cân bằng.
**Đáp số.** $t = 28{,}97$ °C.
**Bấm máy**
- Gõ `0.3×880×(100−x) = 0.5×4180×(x−20)`.
- `SHIFT CALC`, giá trị đầu x = `50`, bấm `=`, rồi `=` thêm một lần.
**Lời giải.** $m_1c_1(t_1 - t) = m_2c_2(t - t_2)$ nên $t = \dfrac{m_1c_1t_1 + m_2c_2t_2}{m_1c_1 + m_2c_2}$.
**Bẫy.** Nghiệm phải nằm giữa 20 và 100; ngoài khoảng đó là gõ sai dấu.

### S3 ⭐⭐ Thời gian phóng xạ
**Đề.** Co-60 có chu kì bán rã $T = 5{,}27$ năm. Sau bao lâu thì còn lại 30% số hạt ban đầu?
**Đáp số.** $t = 9{,}154$ năm.
**Bấm máy**
- Gõ `2^(−x÷5.27) = 0.3`.
- `SHIFT CALC`, giá trị đầu x = `5`, bấm `=`, rồi `=` thêm một lần.
**Lời giải.** $\dfrac{N}{N_0} = 2^{-t/T}$ nên $t = T\log_2\dfrac{1}{0{,}3}$.
**Bẫy.** Gõ `2^−x÷5.27` thiếu ngoặc thì máy hiểu $(2^{-x})/5{,}27$.

---

## B. CALC

### C1 ⭐ Chu kì con lắc đơn
**Đề.** Con lắc đơn dài $l$ tại nơi $g = 9{,}8$ m/s². Tính chu kì với $l = 0{,}8$; $1{,}0$; $1{,}2$ m.
**Đáp số.** $T = 1{,}795$ s; $2{,}007$ s; $2{,}199$ s.
**Bấm máy**
- Gõ `2π√(A÷9.8)` (A là biến, `ALPHA` + phím A).
- `CALC`, nhập A = `0.8`, `=`.
- `CALC` lại, nhập A = `1`, rồi A = `1.2`.
**Bẫy.** Căn phải bao cả `A÷9.8`.

### C2 ⭐⭐ Công suất mạch RLC theo R
**Đề.** Mạch RLC nối tiếp, $U = 200$ V, $Z_L - Z_C = 40\ \Omega$. Tính $P = \dfrac{U^2R}{R^2 + (Z_L - Z_C)^2}$ khi $R = 20; 40; 60; 80\ \Omega$.
**Đáp số.** $P = 400$ W; $500$ W; $461{,}5$ W; $400$ W. Công suất lớn nhất tại $R = |Z_L - Z_C| = 40\ \Omega$.
**Bấm máy**
- Gõ `200²×A÷(A²+40²)`.
- `CALC`, lần lượt A = `20`, `40`, `60`, `80`.
**Bẫy.** Phải có ngoặc quanh mẫu số.

---

## C. TABLE

### T1 ⭐⭐ Cộng hưởng điện
**Đề.** Mạch RLC nối tiếp: $R = 50\ \Omega$, $L = 0{,}1$ H, $C = 25\ \mu$F, $U = 100$ V. Lập bảng $I(f)$ với $f$ từ 80 đến 120 Hz, bước 5 Hz, rồi thu hẹp bước 0,5 Hz. Tìm $f$ làm $I$ lớn nhất.
**Đáp số.** Bước 5 Hz: lớn nhất tại 100 Hz ($I = 1{,}9997$ A). Bước 0,5 Hz: tại 100,5 Hz. Kiểm bằng công thức: $f_0 = \dfrac{1}{2\pi\sqrt{LC}} = 100{,}66$ Hz.
**Bấm máy**
- `MENU` → Table (SETUP → Table → f(x) trước để máy không hỏi g(x)). Nhập `f(x) = 100÷√(50²+(2πx×0.1 − 1÷(2πx×25×10^−6))²)` (x là phím `x`).
- Start = `80`, End = `120`, Step = `5`.
- Chạy lại với Start = `98`, End = `103`, Step = `0.5`.
**Bẫy.** Bảng chỉ cho giá trị theo bước; đáp số cuối tính bằng công thức. Đơn vị góc: không ảnh hưởng ở bài này nhưng nên để Rad.

### T2 ⭐ Đếm cực đại giao thoa
**Đề.** Hai nguồn cùng pha cách nhau $AB = 10{,}5$ cm, bước sóng $\lambda = 2$ cm. Có bao nhiêu điểm dao động cực đại trên đoạn $AB$?
**Đáp số.** 11 điểm ($k = -5, \dots, 5$).
**Bấm máy**
- Table: `f(x) = 2x` (hiệu đường đi $k\lambda$), Start = `-6`, End = `6`, Step = `1`.
- Đếm các hàng có $|f(x)| < 10{,}5$: 11 hàng.
**Lời giải.** Cực đại cùng pha: $d_2 - d_1 = k\lambda$, $|k\lambda| < AB$ nên $|k| < 5{,}25$.
**Bẫy.** Không tính hai đầu A, B (nguồn). Điều kiện là bất đẳng thức chặt.

### T3 ⭐⭐ Vân trùng của hai bức xạ
**Đề.** Giao thoa Y-âng: $a = 1$ mm, $D = 2$ m, hai bức xạ $\lambda_1 = 0{,}45\ \mu$m và $\lambda_2 = 0{,}60\ \mu$m. Tìm vị trí vân sáng trùng đầu tiên (khác vân trung tâm).
**Đáp số.** $x = 3{,}6$ mm.
**Bấm máy**
- Table: `f(x) = 0.45x÷0.6`, Start = `1`, End = `20`, Step = `1`.
- Tìm hàng đầu tiên mà $f(x)$ là số nguyên: x = 4 cho 3.
**Lời giải.** $k_1/k_2 = \lambda_2/\lambda_1 = 4/3$, $x = k_1\dfrac{\lambda_1D}{a} = 4 \times 0{,}9 = 3{,}6$ mm.
**Bẫy.** Bảng làm tròn hiển thị; số nguyên giả (như 2,9999) vẫn chấp nhận được, nhưng kiểm bằng tỉ số tối giản.

---

## D. Số phức

### X1 ⭐ Tổng hợp hai dao động
**Đề.** $x_1 = 3\cos\left(10t + \dfrac{\pi}{3}\right)$ và $x_2 = 4\cos\left(10t - \dfrac{\pi}{6}\right)$ (cm). Tìm biên độ và pha ban đầu của dao động tổng hợp.
**Đáp số.** $A = 5$ cm; $\varphi = 0{,}1199$ rad ($6{,}870°$).
**Bấm máy**
- `MENU` → Số phức, SETUP: **Độ**.
- Gõ `3∠60 + 4∠−30` (∠ là `SHIFT ENG`; dấu trừ của góc gõ bằng phím `(−)`), bấm `=`.
- `OPTN ▼ 1` (▶r∠θ) ở cuối biểu thức để đọc $5\angle 6{,}870$.
- Muốn rad: đổi SETUP sang Rad rồi bấm lại `=` (hoặc đổi độ sang rad bằng $\varphi\times\pi/180$).
**Lời giải.** Hai dao động vuông pha ($60° - (-30°) = 90°$) nên $A = \sqrt{3^2 + 4^2} = 5$, $\varphi = 60° - \arctan\frac43 = 6{,}87°$.
**Bẫy.** Đề cho rad mà nhập độ (hoặc ngược lại).

### X2 ⭐⭐ Dòng điện qua mạch RLC
**Đề.** Mạch nối tiếp có $R = 30\ \Omega$, $Z_L = 80\ \Omega$, $Z_C = 40\ \Omega$, $u = 100\sqrt2\cos(100\pi t)$ (V). Viết biểu thức $i$.
**Đáp số.** $i = 2\sqrt2\cos(100\pi t - 0{,}9273)$ A, tức $I = 2$ A hiệu dụng, trễ pha hơn $u$ góc $0{,}9273$ rad ($53{,}13°$).
**Bấm máy**
- Chế độ Số phức, SETUP: **Rad**.
- Gõ `(100√2∠0) ÷ (30+40i)` (*i* là phím `ENG`), `=`, dạng r∠θ (`OPTN ▼ 1`): $2\sqrt2\angle -0{,}9273$.
**Bẫy.** Dùng biên độ ($100\sqrt2$) thì ra biên độ $2\sqrt2$; dùng 100 thì ra hiệu dụng 2. Trộn hai loại là sai.

### X3 ⭐⭐ Hộp đen
**Đề.** Hộp đen chứa $R$ nối tiếp $L$. Đặt $u = 200\cos\left(100\pi t + \dfrac{\pi}{6}\right)$ (V) thì $i = 2\cos\left(100\pi t - \dfrac{\pi}{6}\right)$ (A). Tìm $R$ và $L$.
**Đáp số.** $R = 50\ \Omega$; $Z_L = 86{,}60\ \Omega$; $L = 0{,}2757$ H.
**Bấm máy**
- Số phức, SETUP: Rad.
- Gõ `(200∠(π÷6)) ÷ (2∠(−π÷6))`, `=`, dạng a+bi (`OPTN ▼ 2`): $50 + 86{,}60i$.
- $L = Z_L/\omega$: gõ `86.60254 ÷ (100π)` hoặc lấy phần ảo của `Ans` bằng `OPTN 4` (ImP).
**Bẫy.** Phần ảo dương cho cuộn cảm, phần ảo âm cho tụ điện.

### X4 ⭐⭐ Tìm dao động thành phần
**Đề.** Dao động tổng hợp $x = 6\cos\left(\omega t + \dfrac{\pi}{3}\right)$, một thành phần $x_1 = 4\cos\left(\omega t + \dfrac{\pi}{6}\right)$ (cm). Tìm thành phần còn lại.
**Đáp số.** $A_2 = 3{,}230$ cm; $\varphi_2 = 1{,}715$ rad ($98{,}26°$).
**Bấm máy**
- Số phức, SETUP: Rad.
- Gõ `6∠(π÷3) − 4∠(π÷6)`, `=`, rồi `OPTN ▼ 1` (▶r∠θ).
**Bẫy.** Argument nằm góc phần tư thứ hai ($\cos<0$, $\sin>0$); máy tự cho 98,26° đúng, đừng tự cộng $\pi$.

---

## E. Vectơ

### V1 ⭐⭐ Lực Lorentz
**Đề.** Hạt $q = 1{,}6.10^{-19}$ C có vận tốc $\vec v = (2.10^5; 3.10^5; 0)$ m/s trong từ trường $\vec B = (0; 0; 0{,}5)$ T. Tính $\vec F = q\,\vec v \times \vec B$ và độ lớn.
**Đáp số.** $\vec F = (2{,}4.10^{-14};\ -1{,}6.10^{-14};\ 0)$ N; $F = 2{,}884.10^{-14}$ N.
**Bấm máy**
- `MENU` → Vector: VctA = (`2×10^5`, `3×10^5`, `0`); VctB = (`0`, `0`, `0.5`).
- `AC`, gõ `1.6×10^−19 × (VctA × VctB)` (VctA = `OPTN 3`, VctB = `OPTN 4`), `=`.
- Độ lớn: `Abs(VctAns)` (`SHIFT (`, rồi VctAns = `OPTN ▼ 1`, rồi `)`).
**Bẫy.** Đổi thứ tự thành $\vec B \times \vec v$ thì ra vectơ đối.

### V2 ⭐ Công và góc
**Đề.** Lực $\vec F = (4; -3; 2)$ N tác dụng làm vật dời $\vec d = (2; 1; 5)$ m. Tính công và góc giữa $\vec F$ và $\vec d$.
**Đáp số.** $A = 15$ J; $\alpha = 59{,}43°$.
**Bấm máy**
- VctA = (4, −3, 2); VctB = (2, 1, 5).
- `VctA • VctB` (Dot Product = `OPTN ▼ 2`) = `15`.
- Góc, cách 1: SETUP Độ, gõ `cos⁻¹(15 ÷ (Abs(VctA)×Abs(VctB)))`.
- Góc, cách 2: `Angle(VctA,VctB)` (`OPTN ▼ 3`; dấu phẩy là `SHIFT )`).
**Bẫy.** Không để Rad khi đề hỏi góc bằng độ.

---

## F. Thống kê

### St1 ⭐ Trung bình và sai số
**Đề.** Đo gia tốc rơi tự do 5 lần: 9,78; 9,83; 9,80; 9,86; 9,81 (m/s²). Tính giá trị trung bình và độ lệch chuẩn.
**Đáp số.** $\bar g = 9{,}816$; $\sigma_x = 0{,}02728$ (chia $n$); $s_x = 0{,}03050$ (chia $n-1$).
**Bấm máy**
- `MENU` → Statistics → **1-Variable**; nhập 5 giá trị vào cột x.
- `AC`, `OPTN` → 1-Variable Calc để đọc $\bar x$, $\sigma x$, $sx$ (hoặc `OPTN ▼ 2` để chèn từng giá trị).
**Bẫy.** Đề yêu cầu loại nào thì ghi loại đó; chưa có thể lệ thì ghi rõ trong bài.

### St2 ⭐⭐ Hồi quy T² theo l
**Đề.** Con lắc đơn có $l$ (m): 0,30; 0,50; 0,70; 0,90; 1,10 và $T^2$ (s²): 1,22; 2,01; 2,78; 3,60; 4,37. Dùng $T^2 = \dfrac{4\pi^2}{g}l$ để tìm $g$.
**Đáp số.** $b = 3{,}945$; $a = 0{,}0345$; $r = 0{,}99996$; $g = \dfrac{4\pi^2}{b} = 10{,}01$ m/s².
**Bấm máy**
- Statistics → **y=a+bx**; x = $l$, y = $T^2$.
- `AC`, `OPTN` → Regression Calc để đọc a, b, r.
- Gõ `4π² ÷ b`, với b chèn bằng `OPTN ▼ 4` → b.
**Bẫy.** Đọc nhầm a (tung độ gốc) thay b (hệ số góc). Gõ `ALPHA B` sẽ lấy biến nhớ B, không phải hệ số b.

### St3 ⭐⭐ Hồi quy mũ cho phóng xạ
**Đề.** Số đếm $N$ theo thời gian $t$ (giờ): (0; 1000), (2; 640), (4; 410), (6; 262), (8; 168). Giả sử $N = ae^{bt}$, tìm chu kì bán rã.
**Đáp số.** $b = -0{,}2230$ h⁻¹; $a \approx 999{,}9$; $r = -1{,}000$; $T = \dfrac{\ln 2}{-b} = 3{,}108$ giờ.
**Bấm máy**
- Statistics → **y=a·e^(bx)** (hồi quy mũ); nhập $t$ vào x, $N$ vào y.
- `AC`, `OPTN` → Regression Calc để đọc b.
- Gõ `ln(2) ÷ (−b)`, với b chèn bằng `OPTN ▼ 4` → b (không gõ `ALPHA B`).
**Bẫy.** Hồi quy mũ cần mọi $N>0$. $T$ dương nên dùng $-b$.

---

## G. Hằng số và đổi đơn vị

### K1 ⭐ Năng lượng photon
**Đề.** Tính năng lượng photon ánh sáng $\lambda = 500$ nm theo J và eV. Cho $h = 6{,}626.10^{-34}$ J.s, $c = 3.10^8$ m/s, $1\ \text{eV} = 1{,}602.10^{-19}$ J.
**Đáp số (đề cho số, dùng số đề cho).** $\varepsilon = \dfrac{hc}{\lambda} = 3{,}976.10^{-19}$ J $= 2{,}482$ eV.
**Ghi chú.** Dùng hằng số chính xác ($h = 6{,}62607015.10^{-34}$; $c = 299792458$) cho $3{,}973.10^{-19}$ J $= 2{,}480$ eV. Hai kết quả khác ở chữ số thứ 4: **dùng giá trị đề cho**.
**Bấm máy**
- Gõ `6.626×10^−34 × 3×10^8 ÷ (500×10^−9)`, `=`.
- Chia cho `1.602×10^−19`.
**Bẫy.** $500$ nm $= 500\times10^{-9}$ m, không phải $10^{-6}$.

### K2 ⭐⭐ Năng lượng liên kết He-4
**Đề.** $m_p = 1{,}0073$ u; $m_n = 1{,}0087$ u; $m_{He} = 4{,}0015$ u; $1\ \text{u} = 931{,}5$ MeV/c². Tính độ hụt khối, năng lượng liên kết và năng lượng liên kết riêng của hạt nhân He-4.
**Đáp số.** $\Delta m = 0{,}0305$ u; $W_{lk} = 28{,}41$ MeV; $W_{lkr} = 7{,}103$ MeV/nuclon.
**Bấm máy**
- Gõ `2×1.0073 + 2×1.0087 − 4.0015`, `=`, rồi `×931.5`, `=`, rồi `÷4`.
**Bẫy.** He-4 có 2 proton và 2 nơtron. Chia cho số khối 4.

### K3 ⭐ Thể tích khí lí tưởng
**Đề.** 2 mol khí lí tưởng ở 300 K, áp suất $1{,}013.10^5$ Pa. Cho $R = 8{,}314$ J/(mol.K). Tính thể tích theo lít.
**Đáp số.** $V = \dfrac{nRT}{p} = 0{,}04924$ m³ $= 49{,}24$ lít.
**Bấm máy**
- Gõ `2×8.314×300 ÷ (1.013×10^5)`, `=`; nhân `1000` để ra lít.
**Bẫy.** $1\ \text{m}^3 = 1000$ lít (không phải 100).
