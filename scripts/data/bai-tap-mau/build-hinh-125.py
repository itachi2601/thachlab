"""Bài tập mẫu Bài 14 "Máy phát điện xoay chiều. Máy biến áp" (Vật lí 12), lesson_id 125. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/125.quet-dang.json). Hình: hinh_125.py. Ví dụ cũ (old/125.json, 2 dạng cũ / 13 ví dụ):
khung 500 vòng 2000 vòng/phút → biên tập thành Dạng 2; 11 ví dụ vào tu_luan (C4, C5, C6 tự giải lại vì lời giải gốc hỏng/sai);
bỏ: Câu 7 (cuộn sơ cấp quấn ngược, ngoài lý thuyết bài và lời giải gốc sai: đáp số đúng 9,4 V chứ không phải 6,5 V),
ảnh <img> lạc đầu Bài 3 tự luận (không kiểm được nội dung).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-125.py   (idempotent, ghi 125.json với review.checked=false)"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_125 import *

J = os.path.join(HERE, "125.json")
T236 = "Nguyên tắc tạo ra dòng điện xoay chiều"
T238 = "Máy biến áp"

# ═════════════ KHỐI TỰ GIẢI (độc lập với lời giải; sai số thì dừng) ═════════════
# Dạng 1
n1 = 750 / 60; f1 = n1 * 4; w1 = TAU * f1; p1b = 50 / (300 / 60)
assert abs(n1 - 12.5) < 1e-9 and abs(f1 - 50) < 1e-9 and abs(w1 - 314.159) < 1e-2 and abs(p1b - 10) < 1e-9
# Dạng 2
N2_, S2_, B2_ = 400, 50e-4, 0.030
w2 = TAU * 1200 / 60; E02 = N2_ * B2_ * S2_ * w2; Eh2 = E02 / math.sqrt(2); E02n = N2_ * B2_ * S2_ * TAU * 1800 / 60
assert abs(w2 - 125.664) < 1e-2 and abs(E02 - 7.5398) < 1e-3 and abs(Eh2 - 5.3315) < 1e-3 and abs(E02n - 11.3097) < 1e-3
assert abs(E02n / E02 - 1.5) < 1e-9
# Dạng 3
U2_3 = 220 * 60 / 1100; I1_3 = 2.5 * 60 / 1100; P1_3 = 220 * I1_3; P2_3 = U2_3 * 2.5
assert abs(U2_3 - 12) < 1e-9 and abs(I1_3 - 0.136364) < 1e-5 and abs(P1_3 - 30) < 1e-9 and abs(P2_3 - 30) < 1e-9 and 60 < 1100
# Dạng 4
I4 = 1.2e6 / 20e3; dP4 = 5 * I4 ** 2; H4 = 1 - dP4 / 1.2e6; I4b = 1.2e6 / 60e3; dP4b = 5 * I4b ** 2
assert abs(I4 - 60) < 1e-9 and abs(dP4 - 18000) < 1e-6 and abs(H4 - 0.985) < 1e-9 and abs(dP4b - 2000) < 1e-6 and abs(dP4 / dP4b - 9) < 1e-9
# Dạng 5
U2_5 = 2e3 * 5000 / 1000; I5 = 400e3 / U2_5; dP5 = 10 * I5 ** 2; Imax5 = math.sqrt(0.01 * 400e3 / 10); Umin5 = 400e3 / Imax5; N2min5 = 1000 * Umin5 / 2e3
assert U2_5 == 10000 and abs(I5 - 40) < 1e-9 and abs(dP5 - 16000) < 1e-6 and abs(Imax5 - 20) < 1e-9 and abs(Umin5 - 20000) < 1e-6 and abs(N2min5 - 10000) < 1e-6
assert abs((1 - dP5 / 400e3) - 0.96) < 1e-9 and abs(2e3 * (400e3 / 2e3) - 400e3) < 1e-6 and abs((400e3 / 2e3) / I5 - 5) < 1e-9
# kiểm các lựa chọn sai thật sự sai (không trùng đáp số)
assert abs(12.5 / 4 - 50) > 1 and abs(12.5 - 50) > 1                       # D1: f = n/p, f = n
assert abs(50 / 300 - 10) > 1 and abs(300 / 50 - 10) > 1                   # D1: p = f/n(vòng/phút), p = n/f
assert abs(220 * 1100 / 60 - 12) > 1 and abs(2.5 * 1100 / 60 - 0.1364) > 1  # D3: tỉ số ngược
assert abs(1.2e6 / 20 - 60) > 1 and abs(5 * 60 - 18000) > 1               # D4: quên đổi đơn vị; ΔP = RI

DANG = [
 dict(label="Dạng 1 · Dễ · Tần số dòng điện của máy phát: f = np", topic=T236,
      problem_html=r"""<p>Rô-to của một máy phát điện xoay chiều một pha là nam châm có $4$ cặp cực, quay đều với tốc độ $750$ vòng/phút.</p><ol type="a"><li>Tính tần số $f$ của dòng điện do máy phát ra.</li><li>Tính tần số góc $\omega$ của suất điện động ở câu a.</li><li>Một máy phát khác có rô-to quay $300$ vòng/phút. Muốn dòng điện phát ra có tần số $50\ \text{Hz}$ thì rô-to của máy này phải có bao nhiêu cặp cực?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Suất điện động cực đại và hiệu dụng của khung quay", topic=T236,
      problem_html=r"""<p>Một khung dây phẳng gồm $N=400$ vòng, diện tích mỗi vòng $S=50\ \text{cm}^2$, quay đều với tốc độ $1200$ vòng/phút quanh một trục vuông góc với đường sức của từ trường đều có cảm ứng từ $B=0{,}030\ \text{T}$.</p><ol type="a"><li>Tính tần số góc $\omega$ của khung.</li><li>Tính suất điện động cực đại $E_0$ trong khung.</li><li>Tính suất điện động hiệu dụng $E$.</li><li>Giữ nguyên $N$, $S$, $B$ và tăng tốc độ quay lên $1800$ vòng/phút. Khi đó $E_0$ bằng bao nhiêu?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Máy biến áp lí tưởng: điện áp, cường độ và công suất hai cuộn", topic=T238,
      problem_html=r"""<p>Một máy biến áp lí tưởng có cuộn sơ cấp $N_1=1100$ vòng, cuộn thứ cấp $N_2=60$ vòng. Mắc cuộn sơ cấp vào mạng điện xoay chiều có điện áp hiệu dụng $U_1=220\ \text{V}$. Cuộn thứ cấp nối với một bóng đèn, cường độ hiệu dụng ở cuộn thứ cấp là $I_2=2{,}5\ \text{A}$.</p><ol type="a"><li>Máy này là máy tăng áp hay hạ áp? Tính điện áp hiệu dụng $U_2$ ở hai đầu cuộn thứ cấp.</li><li>Tính cường độ hiệu dụng $I_1$ ở cuộn sơ cấp.</li><li>Tính công suất mà mạch sơ cấp lấy từ mạng điện.</li></ol>"""),
 dict(label="Dạng 4 · Khá · Hao phí và hiệu suất khi truyền tải điện năng", topic=T238,
      problem_html=r"""<p>Một nhà máy truyền công suất $P=1{,}2\ \text{MW}$ đến nơi tiêu thụ bằng đường dây có điện trở tổng cộng $R=5\ \Omega$. Điện áp hiệu dụng ở nơi phát là $U=20\ \text{kV}$, coi $\cos\varphi=1$.</p><ol type="a"><li>Tính cường độ hiệu dụng $I$ trên đường dây.</li><li>Tính công suất hao phí $\Delta P$ trên đường dây và hiệu suất truyền tải $H$.</li><li>Giữ nguyên $P$ và $R$, tăng điện áp nơi phát lên $60\ \text{kV}$. Công suất hao phí lúc này là bao nhiêu?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Máy tăng áp trước đường dây: hao phí và điện áp tối thiểu", topic=T238,
      problem_html=r"""<p>Một máy phát điện có công suất $P=400\ \text{kW}$, điện áp hiệu dụng ở hai cực $U_1=2\ \text{kV}$. Điện được đưa qua máy biến áp lí tưởng có $N_1=1000$ vòng, $N_2=5000$ vòng rồi truyền đi trên đường dây có điện trở tổng cộng $R=10\ \Omega$ (coi $\cos\varphi=1$; điện áp ở đầu đường dây là điện áp thứ cấp của máy biến áp).</p><ol type="a"><li>Tính điện áp hiệu dụng ở đầu đường dây.</li><li>Tính cường độ hiệu dụng trên đường dây và công suất hao phí trên đó.</li><li>Muốn hiệu suất truyền tải đạt ít nhất $99\%$ với cùng $P$, $R$, $U_1$ và $N_1$ thì điện áp ở đầu đường dây tối thiểu là bao nhiêu kV, và $N_2$ tối thiểu là bao nhiêu vòng?</li></ol>"""),
]
BUILD = [d1, d2, d3, d4, d5]

ANALYSIS = [
 [("\"Rô-to … là nam châm có $4$ cặp cực\"", "$p=4$ cặp cực", "⚠ $p$ là số cặp cực, không phải số cực"),
  ("\"quay đều với tốc độ $750$ vòng/phút\"", "$n=750$ vòng/phút", "⚠ Công thức tần số dùng vòng quay mỗi giây; kiểm đơn vị của $n$ trước"),
  ("\"Tính tần số $f$ của dòng điện\"", "Đại lượng cần tìm", "Liên hệ giữa tần số, tốc độ quay và số cặp cực"),
  ("\"tần số góc $\\omega$ của suất điện động\"", "Đại lượng cần tìm", "Liên hệ giữa tần số góc và tần số"),
  ("\"quay $300$ vòng/phút … tần số $50\\ \\text{Hz}$\"", "$n'=300$ vòng/phút; $f'=50\\ \\text{Hz}$", "Cùng đổi đơn vị của $n'$; bài hỏi ngược (tìm số cặp cực)"),
  ("\"phải có bao nhiêu cặp cực\"", "Đại lượng cần tìm", "Số cặp cực, không phải số cực")],
 [("\"khung dây phẳng gồm $N=400$ vòng, diện tích mỗi vòng $S=50\\ \\text{cm}^2$\"", "$N=400$; $S=50\\ \\text{cm}^2$", "Số vòng và diện tích; kiểm đơn vị của $S$"),
  ("\"quay đều … $1200$ vòng/phút\"", "$n=1200$ vòng/phút", "Kiểm đơn vị của $n$; liên hệ giữa $n$ và tần số góc"),
  ("\"trục vuông góc với đường sức … $B=0{,}030\\ \\text{T}$\"", "$B=0{,}030\\ \\text{T}$; trục quay $\\perp\\vec{B}$", "⚠ Dùng cho khung quay đều quanh trục vuông góc với $\\vec{B}$"),
  ("\"Tính tần số góc $\\omega$\"", "Đại lượng cần tìm", "Liên hệ tần số góc với tốc độ quay"),
  ("\"suất điện động cực đại $E_0$\"", "Đại lượng cần tìm", "Liên hệ suất điện động cực đại với $N$, $B$, $S$ và tốc độ góc"),
  ("\"suất điện động hiệu dụng $E$\"", "Đại lượng cần tìm", "Liên hệ giữa giá trị hiệu dụng và cực đại"),
  ("\"tăng tốc độ quay lên $1800$ vòng/phút\"", "$n'=1800$ vòng/phút; $N$, $S$, $B$ giữ nguyên", "Đại lượng nào đổi, đại lượng nào giữ nguyên")],
 [("\"máy biến áp lí tưởng\"", "Không hao phí", "⚠ Chỉ dùng tỉ số điện áp, tỉ số cường độ và bảo toàn công suất khi máy lí tưởng, nguồn xoay chiều"),
  ("\"cuộn sơ cấp $N_1=1100$ vòng, … thứ cấp $N_2=60$ vòng\"", "$N_1=1100$; $N_2=60$", "So sánh số vòng hai cuộn để biết tăng hay hạ áp"),
  ("\"điện áp hiệu dụng $U_1=220\\ \\text{V}$\"", "$U_1=220\\ \\text{V}$ (sơ cấp)", "Điện áp sơ cấp đi với số vòng sơ cấp"),
  ("\"cường độ hiệu dụng ở cuộn thứ cấp là $I_2=2{,}5\\ \\text{A}$\"", "$I_2=2{,}5\\ \\text{A}$ (thứ cấp)", "Điện áp và cường độ của một cuộn đi với số vòng của chính cuộn đó"),
  ("\"tăng áp hay hạ áp … $U_2$\"", "Đại lượng cần tìm", "Liên hệ giữa điện áp và số vòng hai cuộn"),
  ("\"cường độ hiệu dụng $I_1$ ở cuộn sơ cấp\"", "Đại lượng cần tìm", "Liên hệ giữa cường độ hai cuộn"),
  ("\"công suất mà mạch sơ cấp lấy từ mạng điện\"", "Đại lượng cần tìm", "Liên hệ giữa công suất hai cuộn")],
 [("\"Điện áp hiệu dụng ở nơi phát là $U=20\\ \\text{kV}$, coi $\\cos\\varphi=1$\"", "$U=20\\ \\text{kV}$; $\\cos\\varphi=1$", "⚠ $U$ là điện áp nơi phát, không phải độ sụt áp trên dây; chỉ khi $\\cos\\varphi=1$ mới có $P=UI$"),
  ("\"công suất $P=1{,}2\\ \\text{MW}$\"", "$P=1{,}2\\ \\text{MW}$", "Đổi MW, kV sang đơn vị cơ bản trước khi tính"),
  ("\"điện trở tổng cộng $R=5\\ \\Omega$\"", "$R=5\\ \\Omega$", "Dây dẫn có điện trở nên toả nhiệt"),
  ("\"cường độ hiệu dụng $I$ trên đường dây\"", "Đại lượng cần tìm", "Liên hệ giữa công suất, điện áp và cường độ"),
  ("\"công suất hao phí … hiệu suất truyền tải\"", "Đại lượng cần tìm", "Hao phí do toả nhiệt trên dây; định nghĩa hiệu suất truyền tải"),
  ("\"tăng điện áp nơi phát lên $60\\ \\text{kV}$\"", "$U'=60\\ \\text{kV}$; $P$, $R$ giữ nguyên", "Điện áp tăng thì cường độ trên dây thay đổi thế nào?")],
 [("\"công suất $P=400\\ \\text{kW}$, … $U_1=2\\ \\text{kV}$\"", "$P=400\\ \\text{kW}$; $U_1=2\\ \\text{kV}$", "Đổi kW, kV sang đơn vị cơ bản trước khi tính"),
  ("\"máy biến áp lí tưởng có $N_1=1000$ vòng, $N_2=5000$ vòng\"", "$N_1=1000$; $N_2=5000$", "⚠ Máy lí tưởng: công suất hai cuộn bằng nhau; điện áp tỉ lệ với số vòng"),
  ("\"điện trở tổng cộng $R=10\\ \\Omega$ (coi $\\cos\\varphi=1$ …)\"", "$R=10\\ \\Omega$; $\\cos\\varphi=1$", "⚠ Điện áp ở đầu đường dây là điện áp thứ cấp; cường độ trên dây tính từ công suất và điện áp này"),
  ("\"điện áp hiệu dụng ở đầu đường dây\"", "Đại lượng cần tìm", "Liên hệ giữa điện áp và số vòng hai cuộn"),
  ("\"cường độ … trên đường dây và công suất hao phí\"", "Đại lượng cần tìm", "Liên hệ giữa công suất, điện áp, cường độ; hao phí do toả nhiệt"),
  ("\"hiệu suất truyền tải đạt ít nhất $99\\%$\"", "Hiệu suất tối thiểu $99\\%$ (giới hạn cho hao phí)", "Điều kiện về hiệu suất liên hệ thế nào với công suất hao phí?"),
  ("\"điện áp … tối thiểu … $N_2$ tối thiểu\"", "Đại lượng cần tìm", "Liên hệ giữa cường độ, điện áp ở đầu đường dây và số vòng thứ cấp")]
]

# ═════════════ LỜI GIẢI ═════════════
SOLS = [
 sol([r"Rô-to có $p$ cặp cực, quay $n$ vòng mỗi giây thì tần số dòng điện $f=np$.",
      r"Tần số góc: $\omega=2\pi f$.",
      r"Điều kiện: $n$ tính bằng vòng/giây (đổi từ vòng/phút bằng cách chia cho $60$); $p$ là số cặp cực, không phải số cực."],
  [("Đổi tốc độ quay sang vòng/giây", [P(r"Đề: $n=750$ vòng/phút."), M(r"n=\dfrac{750}{60}"), A(r"n=12{,}5\ \text{vòng/s}")]),
   ("Tần số (câu a)", [M(r"f=np=12{,}5\cdot4"), A(r"f=50\ \text{Hz}")]),
   ("Tần số góc (câu b)", [M(r"\omega=2\pi f=2\pi\cdot50"), A(r"\omega=100\pi\approx314{,}2\ \text{rad/s}")]),
   ("Số cặp cực của máy thứ hai (câu c)", [P(r"$n'=\dfrac{300}{60}=5$ vòng/s; $f'=50\ \text{Hz}$."), M(r"f'=n'p'\Rightarrow p'=\dfrac{f'}{n'}=\dfrac{50}{5}"), A(r"p'=10\ \text{cặp cực}")]),
   ("Kiểm tra", [P(r"Máy thứ nhất: $12{,}5\cdot4=50\ \text{Hz}$, đúng tần số lưới điện."), P(r"Máy thứ hai: $5\cdot10=50\ \text{Hz}$, khớp đề."), P(r"Nếu quên chia $60$ thì ra $750\cdot4=3000\ \text{Hz}$: lớn gấp $60$ lần tần số lưới, vô lí.")])],
  [r"a) $f=50\ \text{Hz}$", r"b) $\omega=100\pi\approx314{,}2\ \text{rad/s}$", r"c) $p'=10$ cặp cực (tức $20$ cực)"],
  r"Nhận dạng: đề cho <strong>số cặp cực và tốc độ quay bằng vòng/phút</strong> → đổi sang vòng/giây rồi dùng $f=np$."),

 sol([r"Từ thông cực đại qua khung: $\Phi_0=NBS$.",
      r"Suất điện động cảm ứng $e=-\Phi'$ nên $E_0=NBS\omega$, với $\omega=2\pi n$ ($n$ vòng/giây).",
      r"Giá trị hiệu dụng: $E=\dfrac{E_0}{\sqrt{2}}$.",
      r"Điều kiện: trục quay vuông góc với $\vec{B}$, quay đều; đổi $S$ sang m², $n$ sang vòng/giây."],
  [("Tần số góc (câu a)", [P(r"$n=\dfrac{1200}{60}=20$ vòng/s."), M(r"\omega=2\pi n=2\pi\cdot20"), A(r"\omega=40\pi\approx125{,}7\ \text{rad/s}")]),
   ("Suất điện động cực đại (câu b)", [P(r"$S=50\ \text{cm}^2=50\cdot10^{-4}\ \text{m}^2=0{,}005\ \text{m}^2$."), M(r"E_0=NBS\omega=400\cdot0{,}030\cdot0{,}005\cdot40\pi"), M(r"E_0=0{,}06\cdot40\pi=2{,}4\pi"), A(r"E_0\approx7{,}54\ \text{V}")]),
   ("Suất điện động hiệu dụng (câu c)", [M(r"E=\dfrac{E_0}{\sqrt{2}}=\dfrac{2{,}4\pi}{\sqrt{2}}"), A(r"E\approx5{,}33\ \text{V}")]),
   ("Tăng tốc độ quay (câu d)", [P(r"$n'=\dfrac{1800}{60}=30$ vòng/s nên $\omega'=60\pi\ \text{rad/s}$; $N$, $S$, $B$ không đổi."), M(r"E_0'=NBS\omega'=0{,}06\cdot60\pi=3{,}6\pi"), A(r"E_0'\approx11{,}31\ \text{V}")]),
   ("Kiểm tra", [P(r"$E\approx5{,}33\ \text{V}\lt E_0\approx7{,}54\ \text{V}$: hiệu dụng nhỏ hơn cực đại."), P(r"$E_0$ tỉ lệ với tốc độ quay: $\dfrac{1800}{1200}=1{,}5$ lần, và $1{,}5\cdot7{,}54\approx11{,}31\ \text{V}$, khớp."), P(r"Nếu quên đổi $\text{cm}^2$ sang $\text{m}^2$ thì $E_0$ lớn gấp $10^4$ lần, vô lí cho khung nhỏ.")])],
  [r"a) $\omega=40\pi\approx125{,}7\ \text{rad/s}$", r"b) $E_0\approx7{,}54\ \text{V}$", r"c) $E\approx5{,}33\ \text{V}$", r"d) $E_0'\approx11{,}31\ \text{V}$"],
  r"Nhận dạng: đề cho <strong>khung $N$ vòng quay trong $\vec{B}$, vòng/phút, cm²</strong> → đổi đơn vị rồi dùng $E_0=NBS\omega$."),

 sol([r"Máy biến áp lí tưởng: $\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}=\dfrac{I_2}{I_1}$.",
      r"$N_2\lt N_1$: hạ áp; $N_2\gt N_1$: tăng áp.",
      r"Không sinh thêm điện năng: $P_1=P_2$, tức $U_1I_1=U_2I_2$.",
      r"Điều kiện: máy lí tưởng (không hao phí), nguồn xoay chiều, $U$ và $I$ là giá trị hiệu dụng."],
  [("Loại máy (câu a)", [P(r"Đề: $N_2=60$ vòng, $N_1=1100$ vòng nên $N_2\lt N_1$."), A(r"T:Cuộn thứ cấp ít vòng hơn: máy hạ áp.")]),
   ("Điện áp thứ cấp (câu a)", [M(r"\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}\Rightarrow U_2=U_1\dfrac{N_2}{N_1}=220\cdot\dfrac{60}{1100}"), A(r"U_2=12\ \text{V}")]),
   ("Cường độ sơ cấp (câu b)", [M(r"\dfrac{I_2}{I_1}=\dfrac{N_1}{N_2}\Rightarrow I_1=I_2\dfrac{N_2}{N_1}=2{,}5\cdot\dfrac{60}{1100}"), A(r"I_1\approx0{,}136\ \text{A}")]),
   ("Công suất sơ cấp (câu c)", [M(r"P_1=U_1I_1=220\cdot0{,}1364"), A(r"P_1=30\ \text{W}")]),
   ("Kiểm tra", [M(r"P_2=U_2I_2=12\cdot2{,}5=30\ \text{W}=P_1"), P(r"Máy hạ áp nên $I_1\lt I_2$ ($0{,}136\ \text{A}\lt2{,}5\ \text{A}$): điện áp giảm bao nhiêu lần thì cường độ tăng bấy nhiêu lần."), P(r"Công suất sơ cấp bằng thứ cấp: máy biến áp không sinh thêm điện năng.")])],
  [r"a) Máy hạ áp; $U_2=12\ \text{V}$", r"b) $I_1\approx0{,}136\ \text{A}$", r"c) $P_1=30\ \text{W}$ (bằng công suất đèn)"],
  r"Nhận dạng: đề cho <strong>số vòng hai cuộn, máy lí tưởng</strong> → tỉ số điện áp bằng tỉ số vòng, tỉ số cường độ ngược lại, công suất không đổi."),

 sol([r"Khi $\cos\varphi=1$: $I=\dfrac{P}{U}$ ($U$ là điện áp nơi phát).",
      r"Hao phí toả nhiệt trên dây: $\Delta P=RI^2=\dfrac{RP^2}{U^2}$.",
      r"Hiệu suất truyền tải: $H=1-\dfrac{\Delta P}{P}$.",
      r"Tăng $U$ lên $k$ lần thì $\Delta P$ giảm $k^2$ lần. Điều kiện: đổi MW, kV sang W, V."],
  [("Cường độ trên dây (câu a)", [P(r"$P=1{,}2\ \text{MW}=1{,}2\cdot10^6\ \text{W}$; $U=20\ \text{kV}=2\cdot10^4\ \text{V}$."), M(r"I=\dfrac{P}{U}=\dfrac{1{,}2\cdot10^6}{2\cdot10^4}"), A(r"I=60\ \text{A}")]),
   ("Công suất hao phí (câu b)", [M(r"\Delta P=RI^2=5\cdot60^2=5\cdot3600"), A(r"\Delta P=18\,000\ \text{W}=18\ \text{kW}")]),
   ("Hiệu suất truyền tải (câu b)", [M(r"H=1-\dfrac{\Delta P}{P}=1-\dfrac{18}{1200}"), A(r"H=0{,}985=98{,}5\%")]),
   ("Tăng điện áp nơi phát (câu c)", [P(r"$U'=60\ \text{kV}=3U$ nên $k=3$ và hao phí giảm $k^2=9$ lần."), M(r"\Delta P'=\dfrac{\Delta P}{9}=\dfrac{18}{9}"), A(r"\Delta P'=2\ \text{kW}")]),
   ("Kiểm tra", [P(r"Tính trực tiếp: $I'=\dfrac{1{,}2\cdot10^6}{6\cdot10^4}=20\ \text{A}$, $\Delta P'=5\cdot20^2=2000\ \text{W}$, khớp."), P(r"Hao phí $18\ \text{kW}$ chỉ bằng $1{,}5\%$ của $1200\ \text{kW}$: hợp lí cho đường dây cao thế."), P(r"Thế $P$ theo MW và $U$ theo kV vào $I=\dfrac{P}{U}$ thì sai đơn vị: ra $I=0{,}06$ chứ không phải $60\ \text{A}$.")])],
  [r"a) $I=60\ \text{A}$", r"b) $\Delta P=18\ \text{kW}$; $H=98{,}5\%$", r"c) $\Delta P'=2\ \text{kW}$"],
  r"Nhận dạng: đề cho <strong>công suất, điện áp nơi phát, điện trở đường dây</strong> → $I=\dfrac{P}{U}$ rồi $\Delta P=RI^2$."),

 sol([r"Máy biến áp lí tưởng: $\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}$ và $P_1=P_2$ (công suất truyền đi không đổi).",
      r"Đường dây: $I=\dfrac{P}{U_2}$ (cosφ = 1), $\Delta P=RI^2$.",
      r"Hiệu suất $H=1-\dfrac{\Delta P}{P}$; $H\ge99\%$ nghĩa là $\Delta P\le0{,}01P$.",
      r"Điều kiện: $U_2$ là điện áp ở đầu đường dây; đổi kW, kV sang W, V."],
  [("Điện áp ở đầu đường dây (câu a)", [M(r"U_2=U_1\dfrac{N_2}{N_1}=2\cdot\dfrac{5000}{1000}"), A(r"U_2=10\ \text{kV}")]),
   ("Cường độ trên dây (câu b)", [P(r"$P=4\cdot10^5\ \text{W}$; $U_2=10^4\ \text{V}$."), M(r"I=\dfrac{P}{U_2}=\dfrac{4\cdot10^5}{10^4}"), A(r"I=40\ \text{A}")]),
   ("Hao phí trên dây (câu b)", [M(r"\Delta P=RI^2=10\cdot40^2"), A(r"\Delta P=16\,000\ \text{W}=16\ \text{kW}")]),
   ("Cường độ tối đa cho phép (câu c)", [P(r"$H\ge99\%$ nghĩa là $\Delta P\le0{,}01P=4000\ \text{W}$."), M(r"RI^2\le4000\Rightarrow I^2\le\dfrac{4000}{10}=400"), A(r"I_{\max}=20\ \text{A}")]),
   ("Điện áp tối thiểu (câu c)", [P(r"Công suất truyền không đổi nên $U_2=\dfrac{P}{I}$; $I$ càng nhỏ thì $U_2$ càng lớn."), M(r"U_{2,\min}=\dfrac{P}{I_{\max}}=\dfrac{4\cdot10^5}{20}"), A(r"U_{2,\min}=20\,000\ \text{V}=20\ \text{kV}")]),
   ("Số vòng thứ cấp tối thiểu (câu c)", [M(r"\dfrac{N_2}{N_1}=\dfrac{U_2}{U_1}\Rightarrow N_{2,\min}=1000\cdot\dfrac{20}{2}"), A(r"N_{2,\min}=10\,000\ \text{vòng}")]),
   ("Kiểm tra", [P(r"Sơ cấp: $I_1=\dfrac{P}{U_1}=200\ \text{A}$; $\dfrac{I_1}{I_2}=\dfrac{200}{40}=5=\dfrac{N_2}{N_1}$, khớp."), P(r"Với $U_2=10\ \text{kV}$: $H=1-\dfrac{16}{400}=96\%\lt99\%$, nên phải tăng điện áp."), P(r"Với $U_2=20\ \text{kV}$: $\Delta P=10\cdot20^2=4000\ \text{W}$, đúng bằng $1\%$ của $P$.")])],
  [r"a) $U_2=10\ \text{kV}$", r"b) $I=40\ \text{A}$; $\Delta P=16\ \text{kW}$ ($H=96\%$)", r"c) $U_2\ge20\ \text{kV}$; $N_2\ge10\,000$ vòng"],
  r"Nhận dạng: đề cho <strong>máy tăng áp rồi đường dây, hỏi điều kiện hiệu suất</strong> → đổi $H$ thành giới hạn của $\Delta P$, rồi $I$, rồi $U$, rồi $N_2$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>số cặp cực, tốc độ quay bằng vòng/phút</b> → nghĩ tới <b>đổi sang vòng/giây, rồi $f=np$</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đổi tốc độ quay sang vòng/giây", "Tốc độ quay $n$ bằng bao nhiêu vòng/giây?", 12.5, "vòng/s", 0.05,
       loi=r"Giữ nguyên số vòng/phút của đề, hoặc nhân với $60$ thay vì chia."),
  buoc("Tần số", "Tần số $f$ của dòng điện bằng bao nhiêu hertz?", 50, "Hz", 0.5,
       loi=r"Quên nhân với số cặp cực, hoặc dùng số cực thay cho số cặp cực.",
       ke=[(r"$f=np$ với $n$ tính bằng vòng/giây", True),
           (r"$f=\dfrac{n}{p}$", r"Mỗi cặp cực làm tần số tăng thêm một chu kì mỗi vòng, nên phải nhân với $p$, không chia."),
           (r"$f=n$ vì một vòng quay là một chu kì", r"Chỉ đúng khi rô-to có một cặp cực; ở đây mỗi vòng quay cho nhiều chu kì.")]),
  buoc("Tần số góc", "Tần số góc $\\omega$ bằng bao nhiêu rad/s?", 314.16, "rad/s", 0.5,
       loi=r"Lấy $\omega=f$ (quên $2\pi$) hoặc $\omega=\dfrac{f}{2\pi}$.",
       ke=[(r"$\omega=2\pi f$ với $f$ vừa tìm", True),
           (r"$\omega=f$", r"$\omega$ tính bằng rad/s, $f$ bằng Hz; hai đại lượng hơn kém nhau hệ số $2\pi$."),
           (r"$\omega=\dfrac{2\pi}{f}$", r"Sai thứ nguyên: $\omega=2\pi f$, không lấy $2\pi$ chia cho $f$.")]),
  buoc("Số cặp cực của máy thứ hai", "Rô-to của máy thứ hai phải có bao nhiêu cặp cực?", 10, "cặp cực", 0.1,
       loi=r"Dùng $n'=300$ vòng/phút mà không đổi sang vòng/giây, hoặc trả lời số cực thay vì số cặp cực.",
       ke=[(r"$p'=\dfrac{f'}{n'}$ với $n'$ đã đổi sang vòng/giây", True),
           (r"$p'=\dfrac{f'}{n'}$ với $n'=300$ vòng/phút", r"Công thức $f=np$ chỉ đúng khi $n$ tính bằng vòng/giây; để vòng/phút sẽ ra số quá nhỏ."),
           (r"$p'=\dfrac{n'}{f'}$", r"Đảo tỉ số: từ $f=np$ suy ra $p=\dfrac{f}{n}$.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>khung $N$ vòng quay trong $\vec{B}$, vòng/phút, cm²</b> → nghĩ tới <b>$E_0=NBS\omega$</b>, đổi đơn vị trước.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tần số góc", "Tần số góc $\\omega$ của khung bằng bao nhiêu rad/s?", 125.66, "rad/s", 0.5,
       loi=r"Lấy $\omega=1200$ (quên đổi vòng/phút sang vòng/giây) hoặc quên nhân $2\pi$."),
  buoc("Suất điện động cực đại", "Suất điện động cực đại $E_0$ bằng bao nhiêu volt?", 7.54, "V", 0.05,
       loi=r"Thế $S=50$ (cm²) không đổi ra m², hoặc quên nhân số vòng $N$, hoặc quên $\omega$.",
       ke=[(r"$E_0=NBS\omega$ với $S$ theo m²", True),
           (r"$E_0=BS\omega$ (chỉ một vòng)", r"Khung có $N$ vòng nên từ thông và suất điện động phải nhân với $N$."),
           (r"$E_0=NBS$", r"Đó là từ thông cực đại $\Phi_0$; đạo hàm theo thời gian sinh thêm thừa số $\omega$.")]),
  buoc("Suất điện động hiệu dụng", "Suất điện động hiệu dụng $E$ bằng bao nhiêu volt?", 5.33, "V", 0.03,
       loi=r"Chia $E_0$ cho $2$ hoặc nhân với $\sqrt{2}$.",
       ke=[(r"$E=\dfrac{E_0}{\sqrt{2}}$", True),
           (r"$E=E_0\sqrt{2}$", r"Hiệu dụng nhỏ hơn cực đại; nhân $\sqrt{2}$ cho số lớn hơn."),
           (r"$E=\dfrac{E_0}{2}$", r"Hệ số $\dfrac{1}{2}$ chỉ nằm ở trung bình của bình phương; hiệu dụng chia cho $\sqrt{2}$.")]),
  buoc("Tăng tốc độ quay", "Sau khi tăng tốc độ quay, $E_0'$ bằng bao nhiêu volt?", 11.31, "V", 0.06,
       loi=r"Vẫn dùng $\omega$ cũ, hoặc đổi cả $N$, $B$, $S$ thay vì chỉ đổi $\omega$.",
       ke=[(r"Chỉ đổi $\omega$, giữ nguyên $N$, $B$, $S$ rồi tính lại $E_0$", True),
           (r"$E_0$ tỉ lệ với $\omega^2$", r"$E_0=NBS\omega$ chỉ chứa $\omega$ bậc nhất; bình phương không xuất hiện."),
           (r"$E_0$ không đổi vì $N$, $B$, $S$ không đổi", r"$E_0$ còn phụ thuộc tốc độ góc $\omega$, mà $\omega$ đã thay đổi.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>số vòng hai cuộn, máy lí tưởng</b> → nghĩ tới <b>$U$ tỉ lệ $N$, $I$ tỉ lệ ngược</b>, $P_1=P_2$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Loại máy", "Máy biến áp này thuộc loại nào?",
       loi=r"Kết luận theo điện áp mà chưa so sánh số vòng, hoặc nghĩ cuộn ít vòng hơn thì điện áp lớn hơn.",
       lua_chon=[(r"Hạ áp, vì cuộn thứ cấp có ít vòng hơn cuộn sơ cấp", True),
                 (r"Tăng áp, vì cuộn thứ cấp có ít vòng hơn", r"Cuộn nhiều vòng hơn thì điện áp lớn hơn; thứ cấp ít vòng hơn nên điện áp ra nhỏ hơn."),
                 (r"Không đổi điện áp, vì máy lí tưởng", r"Máy lí tưởng chỉ có nghĩa là không hao phí; điện áp vẫn thay đổi theo tỉ số vòng.")]),
  buoc("Điện áp thứ cấp", "Điện áp hiệu dụng $U_2$ bằng bao nhiêu volt?", 12, "V", 0.1,
       loi=r"Viết ngược tỉ số số vòng khi thế vào công thức.",
       ke=[(r"$\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}$ với $N_1$ đi cùng $U_1$", True),
           (r"$U_2=U_1$ vì máy lí tưởng", r"Máy lí tưởng chỉ có nghĩa là không hao phí; điện áp vẫn đổi theo số vòng của hai cuộn."),
           (r"$U_2=U_1\dfrac{N_1}{N_2}$", r"Viết ngược: $N_1$ đi với $U_1$ (sơ cấp), $N_2$ đi với $U_2$ (thứ cấp).")]),
  buoc("Cường độ sơ cấp", "Cường độ hiệu dụng $I_1$ bằng bao nhiêu ampe?", 0.1364, "A", 0.002,
       loi=r"Lẫn thứ tự của hai cuộn khi viết tỉ số cường độ.",
       ke=[(r"Dùng tỉ số cường độ của hai cuộn: $\dfrac{I_2}{I_1}=\dfrac{N_1}{N_2}$", True),
           (r"$\dfrac{I_1}{I_2}=\dfrac{N_1}{N_2}$", r"Sai thứ tự: $I_2$ đi với $N_1$ và $I_1$ đi với $N_2$."),
           (r"$I_1=I_2$ vì dòng điện không bị mất", r"Dòng điện không giữ nguyên: điện áp đổi thì cường độ đổi ngược lại để công suất không đổi.")]),
  buoc("Công suất sơ cấp", "Công suất mạch sơ cấp lấy từ mạng điện bằng bao nhiêu watt?", 30, "W", 0.3,
       loi=r"Lẫn điện áp của cuộn này với cường độ của cuộn kia.",
       ke=[(r"Tính từ điện áp và cường độ của chính cuộn sơ cấp", True),
           (r"$P_1=U_1I_2$", r"Mỗi cuộn dùng điện áp và cường độ của chính nó; $U_1$ phải đi với $I_1$."),
           (r"$P_1=\dfrac{P_2}{N_2/N_1}$ vì điện áp thay đổi", r"Tỉ số vòng chỉ liên hệ $U$ với $U$ và $I$ với $I$ của hai cuộn, không phải công suất.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>công suất, điện áp nơi phát, điện trở dây</b> → nghĩ tới <b>$I=P/U$ rồi $\Delta P=RI^2$</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Cường độ trên dây", "Cường độ hiệu dụng $I$ trên đường dây bằng bao nhiêu ampe?", 60, "A", 0.5,
       loi=r"Thế $P$ theo MW và $U$ theo kV mà không đổi về W, V nên sai cỡ độ lớn."),
  buoc("Công suất hao phí", "Công suất hao phí $\\Delta P$ bằng bao nhiêu kilô-oát?", 18, "kW", 0.1,
       loi=r"Dùng sai công thức của hao phí, hoặc quên đổi W sang kW.",
       ke=[(r"$\Delta P=RI^2$ với $I$ vừa tìm", True),
           (r"$\Delta P=RI$", r"Nhiệt toả ra tỉ lệ với bình phương cường độ, không phải bậc nhất."),
           (r"$\Delta P=UI$ với $U=20\ \text{kV}$", r"$UI$ là toàn bộ công suất truyền đi; $U$ ở đây không phải hiệu điện thế rơi trên dây.")]),
  buoc("Hiệu suất truyền tải", "Hiệu suất truyền tải $H$ bằng bao nhiêu phần trăm?", 98.5, "%", 0.1,
       loi=r"Lấy $H=\dfrac{\Delta P}{P}$ nên ra tỉ lệ hao phí thay vì tỉ lệ còn lại.",
       ke=[(r"$H=1-\dfrac{\Delta P}{P}$, cùng đơn vị công suất", True),
           (r"$H=\dfrac{\Delta P}{P}$", r"Đó là tỉ lệ bị hao phí; hiệu suất là phần còn lại."),
           (r"$H=1-\dfrac{\Delta P}{P}$ với $\Delta P$ theo kW và $P$ theo MW", r"Hai công suất phải cùng đơn vị mới chia được.")]),
  buoc("Tăng điện áp nơi phát", "Công suất hao phí lúc này bằng bao nhiêu kilô-oát?", 2, "kW", 0.02,
       loi=r"Suy hao phí mới từ hệ số tăng của điện áp theo tỉ lệ đoán, không tính lại cường độ.",
       ke=[(r"Tính lại cường độ ứng với điện áp mới rồi tính hao phí", True),
           (r"Hao phí giảm đúng bằng hệ số tăng của điện áp", r"Hao phí phụ thuộc cường độ, không trực tiếp phụ thuộc điện áp; phải tính lại cường độ trước."),
           (r"Hao phí không đổi vì $P$ và $R$ không đổi", r"Hao phí là $RI^2$ mà $I=\dfrac{P}{U}$ thay đổi khi $U$ thay đổi.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>máy tăng áp rồi đường dây, hỏi điều kiện hiệu suất</b> → nghĩ tới <b>đổi $H$ thành giới hạn của $\Delta P$</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Điện áp ở đầu đường dây", "Điện áp hiệu dụng ở đầu đường dây bằng bao nhiêu kilô-vôn?", 10, "kV", 0.1,
       loi=r"Viết ngược tỉ số số vòng."),
  buoc("Cường độ trên dây", "Cường độ hiệu dụng trên đường dây bằng bao nhiêu ampe?", 40, "A", 0.5,
       loi=r"Dùng $U_1$ (điện áp máy phát) thay cho điện áp ở đầu đường dây, hoặc quên đổi kW, kV.",
       ke=[(r"$I=\dfrac{P}{U_2}$ với $U_2$ là điện áp đầu đường dây", True),
           (r"$I=\dfrac{P}{U_1}$", r"Dòng trên đường dây chịu điện áp thứ cấp của máy biến áp, không phải điện áp ở hai cực máy phát."),
           (r"$I=\dfrac{U_2}{R}$", r"Đó là cường độ nếu toàn bộ $U_2$ rơi trên điện trở dây; điện áp truyền tải không rơi hết trên dây.")]),
  buoc("Hao phí trên dây", "Công suất hao phí trên dây bằng bao nhiêu kilô-oát?", 16, "kW", 0.1,
       loi=r"Dùng $\Delta P=RI$ hoặc nhân nhầm với $U_1$.",
       ke=[(r"$\Delta P=RI^2$ với $I$ của đường dây", True),
           (r"$\Delta P=RI_1^2$ với $I_1$ là dòng sơ cấp", r"Nhiệt toả ra trên dây do dòng của đường dây (thứ cấp), không phải dòng ở cuộn sơ cấp."),
           (r"$\Delta P=\dfrac{U_2^2}{R}$", r"Đó là công thức khi toàn bộ điện áp $U_2$ rơi trên điện trở, không phải trường hợp truyền tải.")]),
  buoc("Cường độ tối đa cho phép", "Cường độ lớn nhất trên dây để hiệu suất không dưới $99\\%$ là bao nhiêu ampe?", 20, "A", 0.2,
       loi=r"Hiểu $99\%$ là hao phí và lấy $\Delta P=0{,}99P$, hoặc quên căn bậc hai khi giải $I^2$.",
       ke=[(r"Đổi điều kiện hiệu suất thành giới hạn hao phí, rồi từ giới hạn đó tìm cường độ", True),
           (r"Cho $\Delta P=0{,}99P$", r"Con số $99\%$ là hiệu suất, không phải tỉ lệ hao phí."),
           (r"Giải $I\le\dfrac{\Delta P_{\max}}{R}$", r"Hao phí không tỉ lệ bậc nhất với cường độ.")]),
  buoc("Điện áp tối thiểu", "Điện áp tối thiểu ở đầu đường dây là bao nhiêu kilô-vôn?", 20, "kV", 0.2,
       loi=r"Cho rằng điện áp càng nhỏ thì hao phí càng nhỏ, hoặc quên đổi đơn vị sang W, V.",
       ke=[(r"$U_2=\dfrac{P}{I_{\max}}$ với $P$ là công suất truyền đi", True),
           (r"$U_2=\dfrac{\Delta P_{\max}}{I_{\max}}$", r"$\Delta P$ chỉ là phần hao phí; điện áp truyền tải tính từ công suất truyền đi $P$."),
           (r"$U_2=I\cdot R$", r"$IR$ chỉ là độ sụt áp trên dây, không phải điện áp truyền tải.")]),
  buoc("Số vòng thứ cấp tối thiểu", "Số vòng $N_2$ tối thiểu của cuộn thứ cấp là bao nhiêu vòng?", 10000, "vòng", 100,
       loi=r"Viết ngược tỉ số, hoặc dùng $N_2$ ban đầu thay vì tính lại theo điện áp mới.",
       ke=[(r"$\dfrac{N_2}{N_1}=\dfrac{U_2}{U_1}$ với $U_2$ là giá trị tối thiểu vừa tìm", True),
           (r"$\dfrac{N_2}{N_1}=\dfrac{U_1}{U_2}$", r"Viết ngược: cuộn thứ cấp nhiều vòng hơn thì điện áp lớn hơn."),
           (r"Giữ $N_2=5000$ vì máy đã có sẵn", r"Số vòng thứ cấp phải tính lại theo điện áp tối thiểu vừa tìm, không dùng giá trị cũ.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ TỰ LUẬN: ví dụ cũ chưa biên tập thành dạng ═════════════
_old = json.load(open(os.path.join(HERE, "old", "125.json")))["questions"]
_pp = lambda h: re.findall(r'<p class="text-base leading-relaxed my-2">.*?</p>', h, flags=re.S)
_A, _B = _pp(_old[0]["body_html"]), _pp(_old[1]["body_html"])
assert "điện trở 6,0," in _A[7]; _A[7] = _A[7].replace("điện trở 6,0,", r"điện trở $6{,}0\ \Omega$,")
_noimg = lambda h: re.sub(r"<img[^>]*>", "", h)
_nocau = lambda h: re.sub(r'<strong class="font-bold">Câu \d+\.</strong>\s*', "", h)
_P = lambda s: f'<p class="text-base leading-relaxed my-2">{s}</p>'
_ITEMS = [  # (mức, đề, lời giải) xếp dễ → khó
    ("Dễ", [_nocau(_B[1])], [_B[3]]),
    ("Dễ", [_A[19]], [_A[21]]),
    ("Trung bình", _A[22:25], _A[26:28]),
    ("Trung bình", [_A[28]], [_A[30]]),
    ("Trung bình", _A[3:8], _A[9:13]),
    ("Trung bình", [_noimg(_A[13])] + _A[14:16], [_A[17], _A[18]]),
    ("Trung bình", [_nocau(_B[4])], [_B[6]]),
    ("Trung bình", [_nocau(_B[7])], [_B[9]]),
    ("Khá", [_nocau(_B[10])], [_P(r"Gọi $k$ là điện áp trên mỗi vòng thứ cấp: máy lí tưởng, $U_1$ không đổi nên $U_2=kN_2$."),
                              _P(r"Ban đầu $kN_2=100$. Bớt $n$ vòng: $k(N_2-n)=U$. Thêm $n$ vòng: $k(N_2+n)=2U$."),
                              _P(r"Chia hai vế: $N_2+n=2(N_2-n)\Rightarrow N_2=3n$."),
                              _P(r"Thêm $3n$ vòng: $U'=k(N_2+3n)=k\cdot6n=2kN_2=200\ \text{V}$.")]),
    ("Khá", [_nocau(_B[13])], [_P(r"Gọi $N_1$ là số vòng sơ cấp, máy lí tưởng nên $\dfrac{U_2}{U_1}=\dfrac{N_2}{N_1}$."),
                              _P(r"Lúc đầu $N_2=0{,}43N_1$. Sau khi quấn thêm $24$ vòng: $N_2+24=0{,}45N_1$."),
                              _P(r"Trừ hai phương trình: $24=0{,}02N_1\Rightarrow N_1=1200$ vòng."),
                              _P(r"Dự định $N_2=\dfrac{N_1}{2}=600$ vòng; hiện có $0{,}45\cdot1200=540$ vòng. Cần quấn thêm $600-540=60$ vòng.")]),
    ("Khó", [_nocau(_B[16])], [_P(r"Lúc mới sản xuất $N_1=2N_2$. Nối tắt $x$ vòng thì thứ cấp còn $N_2-x$ vòng: $\dfrac{N_1}{N_2-x}=2{,}5\Rightarrow N_2-x=0{,}4N_1=0{,}8N_2$, nên $x=0{,}2N_2$."),
                             _P(r"Quấn thêm $135$ vòng: $\dfrac{N_1}{N_2-x+135}=1{,}6\Rightarrow N_2-x+135=0{,}625N_1=1{,}25N_2$."),
                             _P(r"Thế $N_2-x=0{,}8N_2$: $0{,}8N_2+135=1{,}25N_2\Rightarrow N_2=300$ vòng."),
                             _P(r"Số vòng bị nối tắt: $x=0{,}2\cdot300=60$ vòng.")]),
]
# tự kiểm các đáp số tự luận
assert abs(1000 * 484 / 220 - 2200) < 1e-9
assert abs(TAU * 50 * 800 * 2.4e-3 / math.sqrt(2) - 426.5) < 0.1 and abs(500 * 0.02 * 50e-4 * TAU * 2000 / 60 - 10.47) < 0.01
assert abs(80 * math.pi * 0.0625 * 0.5 - 7.854) < 1e-3 and abs(300 * 2 * math.sqrt(2) * 1e-3 / math.sqrt(2) - 0.6) < 1e-9
assert abs(TAU * 50 * 8 * 0.5 * 0.09 - 113.1) < 0.1
_Nn = 300; _x = 0.2 * _Nn; assert _x == 60 and 2 * _Nn / (_Nn - _x) == 2.5 and abs(2 * _Nn / (_Nn - _x + 135) - 1.6) < 1e-9
_N1 = 1200; assert abs(0.43 * _N1 - 516) < 1e-9 and abs(516 + 24 - 0.45 * _N1) < 1e-9 and _N1 / 2 - 0.45 * _N1 == 60
_n = 100 / 3 / 1.0; _N2c = 3 * _n; _k = 100 / _N2c; assert abs(_k * (_N2c - _n) * 2 - _k * (_N2c + _n)) < 1e-9 and abs(_k * (_N2c + 3 * _n) - 200) < 1e-9
_parts = []
for k, (muc, q, s) in enumerate(_ITEMS, 1):
    h = "".join(q); g = "".join(s)
    h = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", h); g = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", g)
    _parts.append(f'<h4>Bài {k} · {muc}</h4>{h}<details><summary>Hướng dẫn giải</summary>{g}</details>')
TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
               body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(_parts))

# ═════════════ GHI FILE ═════════════
write(J, 125, "Bài 14. Máy phát điện xoay chiều. Máy biến áp", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
