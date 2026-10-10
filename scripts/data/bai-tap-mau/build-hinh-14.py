"""Bài tập mẫu Bài 13 "Đại cương về dòng điện xoay chiều" (Vật lí 12) — lesson_id 14. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/14.quet-dang.json). Hình: hinh_14.py. Ví dụ cũ (old/14.json): i(0) → câu c Dạng 1; Q=I²Rt → Dạng 2;
khung dây 2000 vòng/phút → Dạng 4; còn lại vào tu_luan (bỏ: độ lệch pha, hao phí truyền tải, điện lượng tích phân, đèn huỳnh quang lời giải sai).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-14.py   (idempotent, ghi 14.json với review.checked=false)"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_14 import *

J = os.path.join(HERE, "14.json")
T219 = "Giá trị hiệu dụng của dòng điện xoay chiều"
T220 = "Viết biểu thức u, i theo thời gian"
T236 = "Nguyên tắc tạo ra dòng điện xoay chiều"

DANG = [
 dict(label="Dạng 1 · Dễ · Đọc các đại lượng từ biểu thức của điện áp", topic=T220,
      problem_html=r"""<p>Điện áp tức thời giữa hai đầu một thiết bị là $u=20\sqrt{2}\cos\left(40\pi t+\dfrac{\pi}{3}\right)\ \text{V}$, với $t$ tính bằng giây.</p><ol type="a"><li>Tìm điện áp hiệu dụng $U$ và pha ban đầu $\varphi_u$.</li><li>Tìm tần số góc $\omega$, tần số $f$ và chu kì $T$.</li><li>Tính điện áp tức thời tại $t=0$.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Công suất và nhiệt lượng toả ra trên điện trở", topic=T219,
      problem_html=r"""<p>Dòng điện xoay chiều $i=4\cos\left(100\pi t-\dfrac{\pi}{6}\right)\ \text{A}$ chạy qua điện trở $R=25\ \Omega$ ($t$ tính bằng giây).</p><ol type="a"><li>Tính công suất toả nhiệt trung bình của $R$.</li><li>Tính nhiệt lượng toả ra trong $2$ phút.</li><li>Một dòng điện không đổi muốn toả cùng nhiệt lượng đó trên $R$ trong cùng thời gian thì phải có cường độ bao nhiêu?</li></ol>"""),
 dict(label="Dạng 3 · Khá · Viết biểu thức i từ tần số, cường độ hiệu dụng và giá trị lúc t = 0", topic=T220,
      problem_html=r"""<p>Dòng điện xoay chiều trong một mạch có tần số $50\ \text{Hz}$ và cường độ hiệu dụng $2\ \text{A}$. Tại $t=0$, cường độ tức thời là $-\sqrt{2}\ \text{A}$ và đang tăng.</p><ol type="a"><li>Viết biểu thức của $i$ (dạng hàm cos, $t$ tính bằng giây).</li><li>Tính cường độ tức thời tại $t=\dfrac{1}{200}\ \text{s}$.</li></ol>"""),
 dict(label="Dạng 4 · Khá · Khung dây quay trong từ trường: từ thông và suất điện động", topic=T236,
      problem_html=r"""<p>Một khung dây dẫn $N=200$ vòng, diện tích mỗi vòng $S=100\ \text{cm}^2$, quay đều với tốc độ $1500$ vòng/phút quanh một trục vuông góc với đường sức của từ trường đều $B=0{,}04\ \text{T}$. Lúc $t=0$, pháp tuyến của khung cùng hướng với $\vec{B}$.</p><ol type="a"><li>Tính tần số góc $\omega$ của khung và từ thông cực đại $\Phi_0$.</li><li>Tính suất điện động cực đại $E_0$ và suất điện động hiệu dụng $E$.</li><li>Viết biểu thức suất điện động cảm ứng $e$ trong khung ($e$ tính bằng V, $t$ tính bằng s).</li></ol>"""),
 dict(label="Dạng 5 · Khó · Thời gian đèn sáng và thời điểm đèn tắt", topic=T220,
      problem_html=r"""<p>Một bóng đèn chỉ sáng khi độ lớn điện áp tức thời đặt vào đèn không nhỏ hơn $100\sqrt{3}\ \text{V}$. Đặt vào đèn điện áp $u=200\cos(100\pi t)\ \text{V}$ ($t$ tính bằng giây).</p><ol type="a"><li>Trong một chu kì, đèn sáng tổng cộng bao nhiêu mili-giây?</li><li>Trong $1\ \text{s}$, đèn sáng tổng cộng bao lâu?</li><li>Kể từ $t=0$ (đèn đang sáng), đèn tắt lần đầu vào thời điểm nào (tính bằng mili-giây)?</li></ol>"""),
]
BUILD = [d1, d2, d3, d4, d5]

ANALYSIS = [
 [("\"$u=20\\sqrt{2}\\cos\\left(40\\pi t+\\dfrac{\\pi}{3}\\right)\\ \\text{V}$\"", "Biểu thức $u$ có số cụ thể", "⚠ So từng số hạng với dạng chuẩn hàm cos có hệ số dương; nếu đề viết hàm sin hay hệ số âm thì phải đổi trước"),
  ("\"$20\\sqrt{2}$\" (hệ số trước $\\cos$)", "Một trong ba loại giá trị của $u$", "Phân biệt giá trị tức thời, cực đại, hiệu dụng"),
  ("\"$40\\pi t$\"", "Số nhân với $t$", "Tần số góc và liên hệ với tần số, chu kì"),
  ("\"$+\\dfrac{\\pi}{3}$\"", "Số cộng với $\\omega t$", "Pha ban đầu"),
  ("\"Tìm điện áp hiệu dụng $U$ và pha ban đầu $\\varphi_u$\"", "Cần $U$, $\\varphi_u$", "Cần hiệu dụng, pha ban đầu"),
  ("\"tần số góc, tần số, chu kì\"", "Cần $\\omega$, $f$, $T$", "Cần ba đại lượng liên hệ với nhau"),
  ("\"điện áp tức thời tại $t=0$\"", "Cần $u(0)$", "Thế $t=0$ vào biểu thức")],
 [("\"$i=4\\cos\\left(100\\pi t-\\dfrac{\\pi}{6}\\right)\\ \\text{A}$\"", "Biểu thức $i$ có số cụ thể", "⚠ Điều kiện: $R$ là điện trở thuần và $i$ biến thiên theo dạng hình sin"),
  ("\"$4\\cos$\" (hệ số trước $\\cos$)", "Một trong ba loại giá trị của $i$", "Phân biệt cực đại và hiệu dụng"),
  ("\"$-\\dfrac{\\pi}{6}$\"", "Pha ban đầu", "Pha ban đầu có ảnh hưởng đến công suất trung bình hay không?"),
  ("\"điện trở $R=25\\ \\Omega$\"", "$R=25\\ \\Omega$", "Điện trở thuần: điện năng chuyển hoàn toàn thành nhiệt"),
  ("\"công suất toả nhiệt trung bình\"", "Cần $P$", "Cần công suất trung bình"),
  ("\"trong $2$ phút\"", "$\\Delta t=2$ phút", "Đơn vị thời gian khi tính nhiệt lượng bằng jun"),
  ("\"nhiệt lượng toả ra\"", "Cần $Q$", "Cần nhiệt lượng"),
  ("\"dòng điện không đổi … toả cùng nhiệt lượng\"", "Cần $I_{dc}$", "Định nghĩa giá trị hiệu dụng")],
 [("\"tần số $50\\ \\text{Hz}$\"", "$f=50\\ \\text{Hz}$", "Liên hệ giữa tần số và tần số góc"),
  ("\"cường độ hiệu dụng $2\\ \\text{A}$\"", "$I=2\\ \\text{A}$", "Liên hệ giữa hiệu dụng và cực đại"),
  ("\"Tại $t=0$, cường độ tức thời là $-\\sqrt{2}\\ \\text{A}$\"", "$i(0)=-\\sqrt{2}\\ \\text{A}$", "Thế $t=0$ vào biểu thức để lập phương trình cho $\\varphi$"),
  ("\"đang tăng\" (điều kiện ngầm)", "$i$ tăng lúc $t=0$", "⚠ Một giá trị của $\\cos\\varphi$ ứng với hai nghiệm $\\varphi$ đối nhau; chiều biến thiên lúc $t=0$ để chọn nghiệm"),
  ("\"Viết biểu thức của $i$\"", "Cần $\\omega$, $I_0$, $\\varphi$", "Cần dạng hàm cos với $I_0\\gt0$"),
  ("\"tại $t=\\dfrac{1}{200}\\ \\text{s}$\"", "Cần $i$ tại thời điểm này", "Thế vào biểu thức vừa viết, góc tính bằng rad")],
 [("\"$N=200$ vòng, diện tích mỗi vòng $S=100\\ \\text{cm}^2$\"", "$N=200$; $S=100\\ \\text{cm}^2$", "Từ thông qua cả khung gồm $N$ vòng; đổi $S$ sang m²"),
  ("\"quay đều với tốc độ $1500$ vòng/phút\"", "$n=1500$ vòng/phút", "Đổi sang vòng/giây; liên hệ giữa $n$ và $\\omega$"),
  ("\"trục vuông góc với đường sức … $B=0{,}04\\ \\text{T}$\"", "$B=0{,}04\\ \\text{T}$; trục quay $\\perp\\vec{B}$", "⚠ Chỉ dùng cho khung quay đều quanh trục vuông góc với $\\vec{B}$"),
  ("\"Lúc $t=0$, pháp tuyến cùng hướng với $\\vec{B}$\"", "Góc giữa $\\vec{n}$ và $\\vec{B}$ bằng $0$ lúc $t=0$", "Pha ban đầu của từ thông"),
  ("\"Tính $\\omega$ và $\\Phi_0$\"", "Cần $\\omega$, $\\Phi_0$", "Cần tần số góc, từ thông cực đại"),
  ("\"Tính $E_0$ và $E$\"", "Cần $E_0$, $E$", "Liên hệ suất điện động với từ thông; hiệu dụng"),
  ("\"Viết biểu thức $e$\"", "Cần $e(t)$", "Pha của $e$ so với pha của $\\Phi$")],
 [("\"chỉ sáng khi độ lớn điện áp tức thời … không nhỏ hơn $100\\sqrt{3}\\ \\text{V}$\"", "$|u|\\ge100\\sqrt{3}\\ \\text{V}$", "⚠ Điều kiện đề cho theo độ lớn $|u|$"),
  ("\"$u=200\\cos(100\\pi t)\\ \\text{V}$\"", "$U_0=200\\ \\text{V}$; $\\omega=100\\pi\\ \\text{rad/s}$; $\\varphi_u=0$", "Đọc biên độ, tần số góc, pha ban đầu"),
  ("\"Trong một chu kì, đèn sáng tổng cộng bao nhiêu ms\"", "Cần tổng thời gian sáng trong $T$", "Cần chu kì, số lần sáng mỗi chu kì, thời gian một lần sáng"),
  ("\"Trong $1\\ \\text{s}$\"", "Cần tổng thời gian sáng trong $1\\ \\text{s}$", "Số chu kì trong $1\\ \\text{s}$"),
  ("\"Kể từ $t=0$ (đèn đang sáng), đèn tắt lần đầu\"", "Cần thời điểm tắt lần đầu", "Pha lúc $|u|$ chạm ngưỡng lần đầu")],
]

# ═════════════ LỜI GIẢI ═════════════
SOLS = [
 sol([r"Dạng chuẩn $u=U_0\cos(\omega t+\varphi_u)$ với $U_0\gt0$: so từng số hạng.",
      r"$\omega=2\pi f$ và $T=\dfrac{1}{f}$.",
      r"Hiệu dụng: $U=\dfrac{U_0}{\sqrt{2}}$.",
      r"Điều kiện: biểu thức phải ở dạng hàm cos có hệ số dương (đề cho đúng dạng này)."],
  [("Đối chiếu với dạng chuẩn", [M(r"u=U_0\cos(\omega t+\varphi_u)"), P(r"Đề: $u=20\sqrt{2}\cos\left(40\pi t+\dfrac{\pi}{3}\right)$, nên đọc ra $\omega=40\pi\ \text{rad/s}$ và $\varphi_u=\dfrac{\pi}{3}\ \text{rad}$."), M(r"U_0=20\sqrt{2}"), A(r"U_0\approx28{,}28\ \text{V}")]),
   ("Điện áp hiệu dụng (câu a)", [M(r"U=\dfrac{U_0}{\sqrt{2}}=\dfrac{20\sqrt{2}}{\sqrt{2}}"), A(r"U=20\ \text{V}")]),
   ("Tần số (câu b)", [M(r"\omega=2\pi f\Rightarrow f=\dfrac{\omega}{2\pi}=\dfrac{40\pi}{2\pi}"), A(r"f=20\ \text{Hz}")]),
   ("Chu kì (câu b)", [M(r"T=\dfrac{1}{f}=\dfrac{1}{20}"), A(r"T=0{,}05\ \text{s}")]),
   ("Điện áp tức thời tại $t=0$ (câu c)", [M(r"u(0)=U_0\cos\varphi_u=20\sqrt{2}\cos\dfrac{\pi}{3}"), M(r"u(0)=20\sqrt{2}\cdot\dfrac{1}{2}"), A(r"u(0)=10\sqrt{2}\approx14{,}14\ \text{V}"), P("Máy tính để chế độ radian.")]),
   ("Kiểm tra", [P(r"$u(0)=14{,}14\ \text{V}\lt U_0=28{,}28\ \text{V}$: giá trị tức thời không vượt quá cực đại."), P(r"Pha ban đầu $\dfrac{\pi}{3}$ nằm giữa $0$ và $\dfrac{\pi}{2}$ nên $u(0)$ dương và nhỏ hơn cực đại, khớp với hình."), P(r"$U=20\ \text{V}\lt U_0$: hiệu dụng luôn nhỏ hơn cực đại.")])],
  [r"a) $U=20\ \text{V}$; $\varphi_u=\dfrac{\pi}{3}\ \text{rad}$", r"b) $\omega=40\pi\approx125{,}7\ \text{rad/s}$; $f=20\ \text{Hz}$; $T=0{,}05\ \text{s}$", r"c) $u(0)\approx14{,}14\ \text{V}$"],
  r"Nhận dạng: đề cho <strong>biểu thức $u$ có số cụ thể</strong> → đối chiếu dạng chuẩn $U_0\cos(\omega t+\varphi_u)$, đọc từng số hạng."),

 sol([r"Công suất toả nhiệt trung bình: $P=I^2R$ với $I$ là hiệu dụng.",
      r"Hiệu dụng: $I=\dfrac{I_0}{\sqrt{2}}$.",
      r"Nhiệt lượng: $Q=P\Delta t$, $\Delta t$ tính bằng giây.",
      r"Điều kiện: nhiệt tỉ lệ với $i^2$ nên dùng hiệu dụng; pha ban đầu không ảnh hưởng."],
  [("Đổi sang hiệu dụng", [P(r"Đề: $I_0=4\ \text{A}$; pha $-\dfrac{\pi}{6}$ không ảnh hưởng đến công suất."), M(r"I=\dfrac{I_0}{\sqrt{2}}=\dfrac{4}{\sqrt{2}}"), A(r"I=2\sqrt{2}\approx2{,}83\ \text{A}")]),
   ("Công suất trung bình (câu a)", [M(r"P=I^2R=(2\sqrt{2})^2\cdot25=8\cdot25"), A(r"P=200\ \text{W}")]),
   ("Nhiệt lượng (câu b)", [P(r"$2$ phút $=120\ \text{s}$."), M(r"Q=P\Delta t=200\cdot120"), A(r"Q=24\,000\ \text{J}=24\ \text{kJ}")]),
   ("Dòng không đổi tương đương (câu c)", [P("Theo định nghĩa, dòng không đổi $I_{dc}$ toả cùng nhiệt trên cùng $R$ trong cùng thời gian:"), M(r"I_{dc}^2R\Delta t=I^2R\Delta t\Rightarrow I_{dc}=I"), A(r"I_{dc}=2\sqrt{2}\approx2{,}83\ \text{A}")]),
   ("Kiểm tra", [M(r"P=\dfrac{I_0^2R}{2}=\dfrac{16\cdot25}{2}=200\ \text{W}"), P(r"Nếu dùng nhầm $I_0$ trong $I^2R$ thì ra $400\ \text{W}$, gấp đôi, và dòng không đổi tương đương lớn hơn cả hiệu dụng: vô lí.")])],
  [r"a) $P=200\ \text{W}$", r"b) $Q=24\,000\ \text{J}$", r"c) $I_{dc}\approx2{,}83\ \text{A}$, bằng cường độ hiệu dụng"],
  r"Nhận dạng: đề hỏi <strong>công suất, nhiệt lượng trên điện trở</strong> khi cho biểu thức $i$ → đổi $I_0$ sang hiệu dụng rồi dùng $I^2R$."),

 sol([r"$\omega=2\pi f$; $I_0=I\sqrt{2}$.",
      r"Thế $t=0$: $i(0)=I_0\cos\varphi$.",
      r"Chiều biến thiên lúc $t=0$: $i'(0)=-I_0\omega\sin\varphi$; đang tăng thì $i'(0)\gt0$.",
      r"Điều kiện: $I_0\gt0$ và biểu thức viết dạng hàm cos."],
  [("Tần số góc", [M(r"\omega=2\pi f=2\pi\cdot50"), A(r"\omega=100\pi\ \text{rad/s}\approx314{,}2\ \text{rad/s}")]),
   ("Cường độ cực đại", [M(r"I_0=I\sqrt{2}=2\sqrt{2}"), A(r"I_0\approx2{,}83\ \text{A}")]),
   ("Giải cos φ", [P(r"Thế $t=0$ vào $i=I_0\cos(\omega t+\varphi)$:"), M(r"i(0)=I_0\cos\varphi=-\sqrt{2}"), M(r"\cos\varphi=\dfrac{-\sqrt{2}}{2\sqrt{2}}"), A(r"\cos\varphi=-\dfrac{1}{2}"), P(r"Suy ra $\varphi=\pm\dfrac{2\pi}{3}$.")]),
   ("Chọn dấu của φ", [P(r"Đang tăng: $i'(0)\gt0$."), M(r"i'(0)=-I_0\omega\sin\varphi\gt0\Rightarrow\sin\varphi\lt0"), A(r"\varphi=-\dfrac{2\pi}{3}")]),
   ("Biểu thức và giá trị tại $t=\\dfrac{1}{200}\\ \\text{s}$", [M(r"i=2\sqrt{2}\cos\left(100\pi t-\dfrac{2\pi}{3}\right)\ \text{A}"), M(r"i\left(\dfrac{1}{200}\right)=2\sqrt{2}\cos\left(\dfrac{\pi}{2}-\dfrac{2\pi}{3}\right)=2\sqrt{2}\cos\left(-\dfrac{\pi}{6}\right)"), A(r"i=\sqrt{6}\approx2{,}45\ \text{A}")]),
   ("Kiểm tra", [P(r"$t=0$: $2\sqrt{2}\cos\left(-\dfrac{2\pi}{3}\right)=2\sqrt{2}\cdot\left(-\dfrac{1}{2}\right)=-\sqrt{2}\ \text{A}$, đúng đề."), P(r"Pha đi từ $-\dfrac{2\pi}{3}$ đến $-\dfrac{\pi}{3}$ (trong khoảng $(-\pi;0)$) thì cos tăng nên $i$ đang tăng, đúng đề."), P(r"$2{,}45\ \text{A}\lt I_0=2{,}83\ \text{A}$.")])],
  [r"a) $i=2\sqrt{2}\cos\left(100\pi t-\dfrac{2\pi}{3}\right)\ \text{A}$", r"b) $i\left(\dfrac{1}{200}\ \text{s}\right)=\sqrt{6}\approx2{,}45\ \text{A}$"],
  r"Nhận dạng: đề cho <strong>$f$, hiệu dụng, $i(0)$ và “đang tăng/giảm”</strong> → giải $\cos\varphi$ rồi dùng chiều biến thiên chọn dấu $\varphi$."),

 sol([r"Từ thông: $\Phi=NBS\cos(\omega t+\varphi)$, $\Phi_0=NBS$; $\omega=2\pi n$ ($n$ vòng/s).",
      r"Faraday: $e=-\Phi'$, nên $E_0=\Phi_0\omega$ và $e$ chậm pha $\dfrac{\pi}{2}$ so với $\Phi$.",
      r"Hiệu dụng: $E=\dfrac{E_0}{\sqrt{2}}$.",
      r"Điều kiện: trục quay vuông góc với $\vec{B}$, quay đều; $S$ đổi ra m², $n$ ra vòng/s."],
  [("Tần số góc", [P(r"$n=1500$ vòng/phút $=\dfrac{1500}{60}=25$ vòng/s."), M(r"\omega=2\pi n=2\pi\cdot25"), A(r"\omega=50\pi\ \text{rad/s}\approx157{,}1\ \text{rad/s}")]),
   ("Từ thông cực đại (câu a)", [P(r"$S=100\ \text{cm}^2=100\cdot10^{-4}\ \text{m}^2=0{,}01\ \text{m}^2$."), M(r"\Phi_0=NBS=200\cdot0{,}04\cdot0{,}01"), A(r"\Phi_0=0{,}08\ \text{Wb}")]),
   ("Suất điện động cực đại (câu b)", [M(r"e=-\Phi'\Rightarrow E_0=\Phi_0\omega=0{,}08\cdot50\pi"), A(r"E_0=4\pi\approx12{,}57\ \text{V}")]),
   ("Suất điện động hiệu dụng (câu b)", [M(r"E=\dfrac{E_0}{\sqrt{2}}=\dfrac{4\pi}{\sqrt{2}}"), A(r"E=2\sqrt{2}\pi\approx8{,}89\ \text{V}")]),
   ("Biểu thức của $e$ (câu c)", [P(r"Lúc $t=0$ pháp tuyến cùng hướng $\vec{B}$ nên $\Phi=\Phi_0\cos\omega t$."), M(r"e=-\Phi'=\Phi_0\omega\sin\omega t=E_0\cos\left(\omega t-\dfrac{\pi}{2}\right)"), A(r"e=4\pi\cos\left(50\pi t-\dfrac{\pi}{2}\right)\ \text{V}")]),
   ("Kiểm tra", [P(r"$e(0)=4\pi\cos\left(-\dfrac{\pi}{2}\right)=0$: lúc $t=0$ mặt khung vuông góc $\vec{B}$, $\Phi$ cực đại nên $e=0$."), P(r"$E\approx8{,}89\ \text{V}\lt E_0\approx12{,}57\ \text{V}$, hợp lí."), P(r"Nếu quên đổi $\text{cm}^2$ sang $\text{m}^2$ thì $\Phi_0$ lớn gấp $10^4$ lần, vô lí cho một khung nhỏ.")])],
  [r"a) $\omega=50\pi\approx157{,}1\ \text{rad/s}$; $\Phi_0=0{,}08\ \text{Wb}$", r"b) $E_0=4\pi\approx12{,}57\ \text{V}$; $E\approx8{,}89\ \text{V}$", r"c) $e=4\pi\cos\left(50\pi t-\dfrac{\pi}{2}\right)\ \text{V}$"],
  r"Nhận dạng: đề cho <strong>khung $N$ vòng quay trong $\vec{B}$, vòng/phút, cm²</strong> → đổi đơn vị, $\Phi_0=NBS$, $E_0=\Phi_0\omega$, $e$ chậm pha $\dfrac{\pi}{2}$ so với $\Phi$."),

 sol([r"Đèn sáng khi $|u|\ge u_s$: $|\cos\alpha|\ge\dfrac{u_s}{U_0}$ với $\alpha=\omega t$.",
      r"Đổi pha quét sang thời gian: $\Delta t=\dfrac{\Delta\alpha}{\omega}$; $T=\dfrac{2\pi}{\omega}$.",
      r"Mỗi chu kì có một đỉnh dương và một đỉnh âm; đèn sáng quanh mỗi đỉnh.",
      r"Điều kiện: đề cho theo độ lớn $|u|$."],
  [("Chu kì", [M(r"T=\dfrac{2\pi}{\omega}=\dfrac{2\pi}{100\pi}"), A(r"T=0{,}02\ \text{s}=20\ \text{ms}")]),
   ("Pha quét mỗi lần sáng", [M(r"|\cos\alpha|\ge\dfrac{100\sqrt{3}}{200}=\dfrac{\sqrt{3}}{2}"), P(r"Quanh đỉnh $\alpha=0$: $\cos\alpha\ge\dfrac{\sqrt{3}}{2}$ khi $|\alpha|\le\dfrac{\pi}{6}$."), M(r"\Delta\alpha=2\cdot\dfrac{\pi}{6}"), A(r"\Delta\alpha=\dfrac{\pi}{3}\approx1{,}047\ \text{rad}")]),
   ("Số lần sáng mỗi chu kì", [P(r"Đỉnh dương ($\alpha=0$) và đỉnh âm ($\alpha=\pi$) đều làm $|u|=U_0$ lớn hơn ngưỡng."), A(r"T:Đèn sáng $2$ lần trong mỗi chu kì.")]),
   ("Thời gian sáng mỗi chu kì (câu a)", [M(r"\Delta t_1=\dfrac{\Delta\alpha}{\omega}=\dfrac{\pi/3}{100\pi}=\dfrac{1}{300}\ \text{s}"), M(r"\Delta t=2\Delta t_1=\dfrac{1}{150}\ \text{s}"), A(r"\Delta t\approx6{,}67\ \text{ms}")]),
   ("Thời gian sáng trong $1\\ \\text{s}$ (câu b)", [P(r"Số chu kì trong $1\ \text{s}$ là $f=\dfrac{1}{T}=50$."), M(r"\Delta t_{1\,\text{s}}=50\cdot\dfrac{1}{150}"), A(r"\Delta t_{1\,\text{s}}=\dfrac{1}{3}\ \text{s}\approx0{,}333\ \text{s}")]),
   ("Thời điểm tắt lần đầu (câu c)", [P(r"Lúc $t=0$: $|u|=200\ \text{V}\gt100\sqrt{3}\ \text{V}$ nên đèn đang sáng; đèn tắt khi $|u|$ giảm xuống đúng ngưỡng, tức $\alpha=\dfrac{\pi}{6}$."), M(r"t=\dfrac{\alpha}{\omega}=\dfrac{\pi/6}{100\pi}=\dfrac{1}{600}\ \text{s}"), A(r"t\approx1{,}67\ \text{ms}")]),
   ("Kiểm tra", [P(r"Tỉ lệ thời gian sáng: $\dfrac{6{,}67}{20}=\dfrac{1}{3}$, khớp $\dfrac{4\cdot\pi/6}{2\pi}=\dfrac{1}{3}$."), P(r"Thử lại: $u\left(\dfrac{1}{600}\right)=200\cos\dfrac{\pi}{6}=100\sqrt{3}\ \text{V}$, đúng bằng ngưỡng.")])],
  [r"a) $\Delta t\approx6{,}67\ \text{ms}$ mỗi chu kì", r"b) $\dfrac{1}{3}\ \text{s}\approx0{,}333\ \text{s}$ trong $1\ \text{s}$", r"c) $t=\dfrac{1}{600}\ \text{s}\approx1{,}67\ \text{ms}$"],
  r"Nhận dạng: đề cho <strong>đèn sáng khi $|u|$ vượt ngưỡng</strong> → đổi điều kiện thành khoảng pha quét, rồi chia cho $\omega$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>biểu thức $u$ có số cụ thể</b> → nghĩ tới <b>đối chiếu dạng chuẩn $U_0\cos(\omega t+\varphi_u)$</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Đọc giá trị cực đại", "Điện áp cực đại $U_0$ bằng bao nhiêu volt?", 28.28, "V", 0.1,
       loi=r"Lấy luôn hệ số $20$ làm cực đại (quên $\sqrt{2}$ nằm trong hệ số trước $\cos$)."),
  buoc("Điện áp hiệu dụng", "Điện áp hiệu dụng $U$ bằng bao nhiêu volt?", 20, "V", 0.1,
       loi=r"Nhân thêm $\sqrt{2}$ thay vì chia, hoặc chia cho $2$.",
       ke=[(r"$U=\dfrac{U_0}{\sqrt{2}}$ từ cực đại vừa đọc", True),
           (r"$U=U_0\sqrt{2}$", r"Đó là công thức ra cực đại từ hiệu dụng; hiệu dụng phải nhỏ hơn cực đại."),
           (r"$U=\dfrac{U_0}{2}$", r"Hệ số $\dfrac{1}{2}$ xuất hiện ở trung bình của $u^2$; điện áp hiệu dụng chia cho $\sqrt{2}$.")]),
  buoc("Tần số", "Tần số $f$ bằng bao nhiêu hertz?", 20, "Hz", 0.1,
       loi=r"Lấy $f=\omega$ hoặc $f=40$ (quên chia cho $2\pi$).",
       ke=[(r"$f=\dfrac{\omega}{2\pi}$ với $\omega=40\pi$", True),
           (r"$f=\omega$", r"$\omega$ tính bằng rad/s, $f$ tính bằng Hz; hai đại lượng khác nhau hệ số $2\pi$."),
           (r"$f=\dfrac{2\pi}{\omega}$", r"Đó là công thức của chu kì $T$, không phải của $f$.")]),
  buoc("Chu kì", "Chu kì $T$ bằng bao nhiêu giây?", 0.05, "s", 0.001,
       loi=r"Lấy $T=f$ hoặc $T=\dfrac{1}{\omega}$ (quên $2\pi$).",
       ke=[(r"$T=\dfrac{1}{f}$", True),
           (r"$T=2\pi f$", r"$2\pi f$ là tần số góc $\omega$, không phải chu kì."),
           (r"$T=f$", r"$T$ và $f$ là hai số nghịch đảo của nhau, không bằng nhau.")]),
  buoc("Điện áp tức thời tại $t=0$", "Điện áp tức thời tại $t=0$ bằng bao nhiêu volt?", 14.14, "V", 0.1,
       loi=r"Bỏ quên pha ban đầu nên lấy luôn cực đại; hoặc để máy tính ở chế độ độ khi tính $\cos\dfrac{\pi}{3}$.",
       ke=[(r"Thế $t=0$: $u(0)=U_0\cos\varphi_u$", True),
           (r"$u(0)=U_0$ vì lúc $t=0$ điện áp đạt cực đại", r"Chỉ đạt cực đại khi pha bằng $0$; ở đây $\varphi_u\neq0$."),
           (r"$u(0)=U\cos\varphi_u$ với $U$ hiệu dụng", r"Giá trị tức thời tính từ biên độ $U_0$, không phải giá trị hiệu dụng.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>công suất, nhiệt lượng trên điện trở</b> → nghĩ tới <b>đổi sang hiệu dụng rồi dùng $I^2R$</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi sang hiệu dụng", "Cường độ hiệu dụng $I$ bằng bao nhiêu ampe?", 2.83, "A", 0.01,
       loi=r"Dùng luôn cực đại cho mọi phép tính, hoặc chia cho $2$ thay vì $\sqrt{2}$."),
  buoc("Công suất trung bình", "Công suất toả nhiệt trung bình $P$ bằng bao nhiêu watt?", 200, "W", 1,
       loi=r"Dùng $I_0$ thay $I$ nên công suất gấp đôi; hoặc chia $I_0^2R$ cho $\sqrt{2}$ thay vì cho $2$.",
       ke=[(r"$P=I^2R$ với $I$ hiệu dụng", True),
           (r"$P=I_0^2R$", r"$I_0$ là giá trị đỉnh; công suất trung bình dùng hiệu dụng, bằng một nửa $I_0^2R$."),
           (r"$P=\dfrac{I_0^2R}{\sqrt{2}}$", r"Chia $\sqrt{2}$ chỉ ra cường độ hiệu dụng; trong $I^2$ phải chia cho $2$.")]),
  buoc("Nhiệt lượng", "Nhiệt lượng $Q$ toả ra trong $2$ phút bằng bao nhiêu jun?", 24000, "J", 100,
       loi=r"Thế thời gian bằng phút (nhân với $2$) thay vì giây, nên kết quả nhỏ hơn rất nhiều.",
       ke=[(r"$Q=P\Delta t$ với $\Delta t$ tính bằng giây", True),
           (r"$Q=P\Delta t$ với $\Delta t=2$ (phút)", r"Đơn vị jun đòi thời gian bằng giây; $2$ phút là $120$ s."),
           (r"$Q=\dfrac{P}{\Delta t}$", r"Công suất là năng lượng chia thời gian, nên nhiệt lượng bằng công suất nhân thời gian.")]),
  buoc("Dòng không đổi tương đương", "Dòng không đổi toả cùng nhiệt lượng trên $R$ trong cùng thời gian có cường độ thế nào?",
       loi=r"Chọn cực đại vì nghĩ dòng không đổi phải bằng đỉnh, hoặc chọn $0$ vì trung bình của $i$ bằng $0$.",
       lua_chon=[(r"Bằng cường độ hiệu dụng $I$", True),
                 (r"Bằng cường độ cực đại $I_0$", r"Dòng không đổi $I_0$ luôn ở mức đỉnh nên toả nhiều nhiệt hơn dòng xoay chiều chỉ chạm đỉnh thoáng qua."),
                 (r"Bằng $0$ vì trung bình của $i$ trong một chu kì bằng $0$", r"Nhiệt tỉ lệ $i^2$ nên không triệt tiêu: trung bình của $i$ bằng $0$ nhưng trung bình của $i^2$ thì không.")],
       ke=[(r"Dùng định nghĩa: cùng nhiệt trên cùng $R$ trong cùng thời gian", True),
           (r"Lấy $I_{dc}$ bằng giá trị trung bình của $i$", r"Trung bình của $i$ bằng $0$ trong một chu kì, không cho biết nhiệt toả ra."),
           (r"Lấy $I_{dc}=\dfrac{I_0}{2}$", r"Hệ số $\dfrac{1}{2}$ chỉ nằm ở trung bình của $i^2$; cường độ hiệu dụng chia cho $\sqrt{2}$.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>$f$, hiệu dụng, $i(0)$ và “đang tăng”</b> → nghĩ tới <b>giải $\cos\varphi$, chọn dấu theo chiều biến thiên</b>.",
  cap_do=3, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Tần số góc", "Tần số góc $\\omega$ bằng bao nhiêu rad/s?", 314.16, "rad/s", 0.5,
       loi=r"Lấy $\omega=f$ hoặc $\omega=\dfrac{2\pi}{f}$."),
  buoc("Cường độ cực đại", "Cường độ cực đại $I_0$ bằng bao nhiêu ampe?", 2.83, "A", 0.01,
       loi=r"Lấy $I_0=I=2$ (quên nhân $\sqrt{2}$).",
       ke=[(r"$I_0=I\sqrt{2}$", True),
           (r"$I_0=\dfrac{I}{\sqrt{2}}$", r"Cực đại lớn hơn hiệu dụng; chia cho $\sqrt{2}$ cho số nhỏ hơn."),
           (r"$I_0=2I$", r"Hệ số là $\sqrt{2}$ (do trung bình của $\cos^2$ bằng $\dfrac{1}{2}$), không phải $2$.")]),
  buoc("Giải cos φ", "Từ $i(0)$, $\\cos\\varphi$ bằng bao nhiêu?", -0.5, "", 0.01,
       loi=r"Dùng $I$ hiệu dụng thay $I_0$ trong $i(0)=I\cos\varphi$ nên ra giá trị khác.",
       ke=[(r"Thế $t=0$: $i(0)=I_0\cos\varphi$ rồi giải $\cos\varphi$", True),
           (r"Coi $\varphi=\omega\cdot0=0$", r"$\varphi$ là ẩn cần tìm; $t=0$ chỉ làm mất số hạng $\omega t$."),
           (r"Dùng $i(0)=I\cos\varphi$ với $I$ hiệu dụng", r"Giá trị tức thời tính từ biên độ $I_0$, không phải hiệu dụng.")]),
  buoc("Chọn dấu của φ", "Chọn nghiệm nào của $\\varphi$ cho dòng điện \"đang tăng\" lúc $t=0$?",
       loi=r"Lấy nghiệm dương mà máy tính cho ra từ $\arccos$ mà không xét “đang tăng”.",
       lua_chon=[(r"$\varphi=-\dfrac{2\pi}{3}$, vì đang tăng nên $\sin\varphi\lt0$", True),
                 (r"$\varphi=+\dfrac{2\pi}{3}$", r"Với $\varphi=+\dfrac{2\pi}{3}$ thì $i'(0)=-I_0\omega\sin\varphi\lt0$: dòng đang giảm, ngược với đề."),
                 (r"$\varphi=-\dfrac{\pi}{3}$", r"$\cos\left(-\dfrac{\pi}{3}\right)\gt0$ cho $i(0)\gt0$, không khớp $i(0)=-\sqrt{2}$ là số âm.")],
       ke=[(r"Xét dấu $i'(0)=-I_0\omega\sin\varphi$ để chọn nghiệm", True),
           (r"Luôn chọn nghiệm dương cho gọn", r"Dấu của $\varphi$ do chiều biến thiên quyết định, không chọn theo thói quen."),
           (r"Bỏ qua “đang tăng” vì $i(0)$ đã đủ", r"$i(0)$ chỉ cho $\cos\varphi$, tức hai nghiệm đối nhau; “đang tăng” mới chọn được một nghiệm.")]),
  buoc("Biểu thức và giá trị tại $t=\\dfrac{1}{200}\\ \\text{s}$", "Cường độ tức thời tại $t=\\dfrac{1}{200}\\ \\text{s}$ bằng bao nhiêu ampe?", 2.449, "A", 0.02,
       loi=r"Để máy tính ở chế độ độ khi tính cos của góc tính bằng rad, hoặc thế pha ban đầu sai dấu.",
       ke=[(r"Thế $t$ vào biểu thức vừa viết, góc tính bằng rad", True),
           (r"Thế vào nhưng dùng $I$ hiệu dụng thay $I_0$", r"Giá trị tức thời tính từ biên độ $I_0$."),
           (r"Thế vào với máy tính ở chế độ độ", r"Pha $100\pi t+\varphi$ tính bằng rad; để chế độ độ sẽ coi số rad như số độ nên sai.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>khung $N$ vòng quay trong $\vec{B}$, vòng/phút, cm²</b> → nghĩ tới <b>$\Phi_0=NBS$, $E_0=\Phi_0\omega$</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Tần số góc", "Tần số góc $\\omega$ của khung bằng bao nhiêu rad/s?", 157.08, "rad/s", 0.5,
       loi=r"Lấy $\omega=1500$ (quên đổi vòng/phút sang vòng/s) hoặc quên nhân $2\pi$."),
  buoc("Từ thông cực đại", "Từ thông cực đại $\\Phi_0$ bằng bao nhiêu weber?", 0.08, "Wb", 0.001,
       loi=r"Thế $S=100$ (cm²) không đổi ra m², hoặc quên nhân $N$ vòng.",
       ke=[(r"$\Phi_0=NBS$ với $S$ theo m²", True),
           (r"$\Phi_0=BS$ (chỉ một vòng)", r"Khung có $N$ vòng nên từ thông qua cả khung phải nhân với $N$."),
           (r"$\Phi_0=NBS\omega$", r"Đó là $E_0$; từ thông không chứa thừa số $\omega$.")]),
  buoc("Suất điện động cực đại", "Suất điện động cực đại $E_0$ bằng bao nhiêu volt?", 12.57, "V", 0.05,
       loi=r"Lấy $E_0=\Phi_0$ (quên đạo hàm sinh ra thừa số $\omega$) hoặc chia cho $\omega$.",
       ke=[(r"$E_0=\Phi_0\omega$ vì $e=-\Phi'$", True),
           (r"$E_0=\Phi_0$", r"Đạo hàm của $\cos\omega t$ theo $t$ sinh thêm thừa số $\omega$."),
           (r"$E_0=\dfrac{\Phi_0}{\omega}$", r"Lấy đạo hàm thì nhân với $\omega$, không chia.")]),
  buoc("Suất điện động hiệu dụng", "Suất điện động hiệu dụng $E$ bằng bao nhiêu volt?", 8.89, "V", 0.05,
       loi=r"Chia $E_0$ cho $2$ hoặc nhân với $\sqrt{2}$.",
       ke=[(r"$E=\dfrac{E_0}{\sqrt{2}}$", True),
           (r"$E=E_0\sqrt{2}$", r"Hiệu dụng nhỏ hơn cực đại; nhân $\sqrt{2}$ cho số lớn hơn."),
           (r"$E=\dfrac{E_0}{2}$", r"Hệ số $\dfrac{1}{2}$ ở trung bình của bình phương; hiệu dụng chia cho $\sqrt{2}$.")]),
  buoc("Biểu thức của $e$", "Pha ban đầu của $e$ bằng bao nhiêu rad?", -1.571, "rad", 0.01,
       loi=r"Cho $e$ cùng pha ban đầu với $\Phi$ (bằng $0$), hoặc lấy $e$ nhanh pha $\dfrac{\pi}{2}$ thay vì chậm pha.",
       ke=[(r"$e=-\Phi'=E_0\sin\omega t=E_0\cos\left(\omega t-\dfrac{\pi}{2}\right)$", True),
           (r"$e$ cùng pha với $\Phi$ nên pha ban đầu bằng $0$", r"$e$ tỉ lệ với tốc độ biến thiên của $\Phi$ chứ không với $\Phi$; hai đại lượng vuông pha."),
           (r"$e$ nhanh pha $\dfrac{\pi}{2}$ so với $\Phi$", r"Từ $e=-\Phi'$ ra $e=+E_0\sin\omega t$, tức chậm pha $\dfrac{\pi}{2}$ chứ không nhanh pha.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>đèn sáng khi $|u|$ vượt ngưỡng</b> → nghĩ tới <b>đổi điều kiện thành khoảng pha quét</b>, rồi chia cho $\omega$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Chu kì", "Chu kì $T$ bằng bao nhiêu mili-giây?", 20, "ms", 0.1,
       loi=r"Quên đổi giây sang mili-giây, hoặc lấy $T=\dfrac{1}{\omega}$."),
  buoc("Pha quét mỗi lần sáng", "Mỗi lần đèn sáng, pha $\\omega t$ quét được bao nhiêu rad?", 1.047, "rad", 0.01,
       loi=r"Chỉ xét nửa bên của đỉnh (quên đỉnh nằm giữa), hoặc chỉ xét $u$ dương.",
       ke=[(r"$|\cos\alpha|\ge\dfrac{\sqrt{3}}{2}$: pha quanh mỗi đỉnh trong một khoảng đối xứng", True),
           (r"Chỉ xét $u\ge100\sqrt{3}$", r"Đề nói độ lớn nên điện áp âm cũng làm đèn sáng."),
           (r"$|\cos\alpha|\ge\dfrac{1}{2}$ vì ngưỡng bằng nửa biên độ", r"Ngưỡng là $100\sqrt{3}$ V, tức $\dfrac{\sqrt{3}}{2}$ biên độ, không phải một nửa.")]),
  buoc("Số lần sáng mỗi chu kì", "Mỗi chu kì đèn sáng mấy lần?", 2, "lần", 0,
       loi=r"Đếm một lần (chỉ đỉnh dương) hoặc bốn lần (đếm cả lúc bắt đầu và kết thúc mỗi lần sáng).",
       ke=[(r"Sáng quanh mỗi đỉnh: một đỉnh dương, một đỉnh âm", True),
           (r"Chỉ sáng quanh đỉnh dương", r"$|u|$ cũng lớn ở đỉnh âm nên đèn cũng sáng ở đó."),
           (r"Sáng quanh mỗi điểm $u=0$", r"Tại $u=0$ điện áp nhỏ nhất nên đèn tắt, không sáng.")]),
  buoc("Thời gian sáng mỗi chu kì", "Tổng thời gian đèn sáng trong một chu kì là bao nhiêu mili-giây?", 6.67, "ms", 0.05,
       loi=r"Lấy pha quét nhân với $T$ thay vì chia cho $\omega$, hoặc cho rằng đèn sáng một nửa chu kì.",
       ke=[(r"$\Delta t=\dfrac{2\cdot\text{pha quét một lần}}{\omega}$", True),
           (r"$\Delta t=\text{pha quét}\cdot T$", r"Pha quét tính bằng rad; đổi sang thời gian phải chia cho $\omega$ (hoặc lấy tỉ lệ $\dfrac{\text{pha}}{2\pi}$ nhân $T$)."),
           (r"$\Delta t=\dfrac{T}{2}$ vì đèn sáng nửa thời gian", r"Tỉ lệ thời gian sáng phải tính từ pha quét, không đoán bằng một nửa.")]),
  buoc("Thời gian sáng trong 1 s", "Trong $1\\ \\text{s}$ đèn sáng tổng cộng bao nhiêu giây?", 0.333, "s", 0.005,
       loi=r"Nhân với $\omega$ thay vì số chu kì, hoặc đếm số lần đổi chiều thay cho số chu kì.",
       ke=[(r"Số chu kì trong $1$ s là $f$, nhân với thời gian sáng mỗi chu kì", True),
           (r"Nhân với $\omega=100\pi$", r"Số chu kì trong $1$ s là $f$; $\omega$ là rad/s."),
           (r"Nhân với số lần đổi chiều mỗi giây", r"Đèn sáng theo chu kì, mỗi chu kì có thời gian sáng đã tính; đếm lần đổi chiều sẽ nhân gấp đôi.")]),
  buoc("Thời điểm tắt lần đầu", "Kể từ $t=0$, đèn tắt lần đầu vào thời điểm nào, theo mili-giây?", 1.667, "ms", 0.02,
       loi=r"Cho rằng đèn tắt khi $u=0$, hoặc lấy góc ứng với $\cos\alpha=\dfrac{1}{2}$.",
       ke=[(r"Đèn tắt khi $|u|$ xuống đúng ngưỡng: $\cos\alpha=\dfrac{\sqrt{3}}{2}$, lần đầu ngay khi $|\cos\alpha|$ chạm ngưỡng", True),
           (r"Đèn tắt khi $u=0$, tức $\alpha=\dfrac{\pi}{2}$", r"Đèn đã tắt từ lúc $|u|$ xuống dưới ngưỡng, trước khi $u$ về $0$."),
           (r"Đèn tắt ở $\alpha=\dfrac{\pi}{3}$ vì $\cos\dfrac{\pi}{3}=\dfrac{1}{2}$", r"Ngưỡng ứng với $\cos\dfrac{\pi}{6}=\dfrac{\sqrt{3}}{2}$, không phải $\dfrac{1}{2}$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ TỰ LUẬN: ví dụ cũ chưa biên tập thành dạng ═════════════
_old = json.load(open(os.path.join(HERE, "old", "14.json")))["questions"]
_pp = lambda h: re.findall(r'<p class="text-base leading-relaxed my-2">.*?</p>', h, flags=re.S)
_A, _B = _pp(_old[0]["body_html"]), _pp(_old[1]["body_html"])
_ITEMS = [  # (mức, đề, lời giải gốc) xếp dễ → khó
    ("Dễ", _A[0:4], _A[5:7]),
    ("Trung bình", [_B[20]], _B[22:24]),
    ("Trung bình", [_A[13]], [_A[15]]),
    ("Trung bình", [_B[24]], [_B[26]]),
    ("Trung bình", [_B[10]], [_B[12]]),
    ("Khá", [_B[3]], [_B[5]]),
]
_parts = []
for k, (muc, q, s) in enumerate(_ITEMS, 1):
    h = "".join(q); g = "".join(s)
    h = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", h); g = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", g)
    _parts.append(f'<h4>Bài {k} · {muc}</h4>{h}<details><summary>Hướng dẫn giải</summary>{g}</details>')
TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
               body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(_parts))

# ═════════════ GHI FILE ═════════════
write(J, 14, "Bài 13. Đại cương về dòng điện xoay chiều", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
