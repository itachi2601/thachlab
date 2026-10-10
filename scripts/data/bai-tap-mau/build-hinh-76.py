"""Bài 76 — "Bài 31. Động học của chuyển động tròn đều" (Vật lí 10, chương 6). 5 dạng + tự luận (ví dụ cũ chưa biên tập).
Mẫu: build-hinh-58.py. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-76.py  → ghi scripts/data/bai-tap-mau/76.json
Dạng theo quét: scripts/logs/batch-ra-soat/ket-qua/76.quet-dang.json. Hình: hinh_76.py (vị trí tính thật từ ω·t, không vẽ vectơ, không ghi đáp số).
Ví dụ cũ (old/76.json, 14 mục): cả 12 mục dùng được (idx 0-10 và 13) vào tự luận xếp dễ→khó, giữ nguyên lời giải gốc (chỉ sửa "1.2" thành 1·2, bỏ alt ảnh);
dạng mới viết lại với số liệu khác từ ý của VD4/VD5 (đổi vòng/phút), VD6 (chu kì), VD7–VD9 (v = ωr nhiều điểm), VD10 (cùng chu kì, khác bán kính).
BỎ: VD12 (idx 11, trái bóng buộc dây): dữ kiện không nhất quán với con lắc nón thật (T ≈ 0,75 s chứ không phải 1 s) và phụ thuộc hình;
VD13 (idx 12, Trái Đất–Mặt Trời): số làm tròn sớm lệch nhau (467,2 m/s ở ý b, 404,6 m/s ở ý c so với 465,4 và 403,1 m/s khi tính từ ω chưa làm tròn),
lại có 2 ảnh trong đề/lời giải không kiểm được.
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_76 import BUILD

J = os.path.join(HERE, "76.json")
OLD = json.load(open(os.path.join(HERE, "old/76.json")))["questions"]
T34, T146, T147 = "Động học của chuyển động tròn đều", "Tốc độ góc, chu kì, tần số", "Liên hệ tốc độ dài và tốc độ góc"

# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
PI = math.pi
# D1
r1, v1, t1 = 0.50, 0.40, 5.0
s1 = v1 * t1; th1 = s1 / r1
ok("D1 s", s1, 2.0, 1e-9); ok("D1 θ", th1, 4.0, 1e-9); ok("D1 θ độ", math.degrees(th1), 229.2, 0.05)
assert PI < th1 < 2 * PI                                                             # hơn nửa vòng, chưa hết vòng
ok("D1 chu vi", 2 * PI * r1, 3.14, 0.005); assert s1 < 2 * PI * r1
assert abs(v1 * t1 - th1) > 1 and abs(s1 * r1 - th1) > 1.5                           # θ = v t (quên chia r), θ = s·r đều ra số khác 4,0
# D2
n2, dt2 = 5, 120.0
T2 = dt2 / n2; f2 = 1 / T2; w2 = 2 * PI / T2; th2 = w2 * 10
ok("D2 T", T2, 24, 1e-9); ok("D2 f", f2, 0.0417, 5e-5); ok("D2 ω", w2, 0.262, 5e-4); ok("D2 ω=π/12", w2, PI / 12, 1e-12)
ok("D2 θ rad", th2, 2.62, 5e-3); ok("D2 θ độ", math.degrees(th2), 150.0, 1e-9)
ok("D2 kiểm ωT", w2 * T2, 2 * PI, 1e-9); ok("D2 kiểm vòng", 10 / T2 * 360, 150, 1e-9)
assert abs(n2 / dt2 - T2) > 20 and abs(2 * PI * f2 * 10 * (180 / PI) - 150) < 1e-9     # chia ngược n/Δt cho f, không phải T
assert abs(2 * PI * f2 * 10 * (180 / PI) - 150) < 1e-9
# D3
n3 = 7200
f3 = n3 / 60; T3 = 1 / f3; w3 = 2 * PI * f3; th3 = w3 * 1e-3
ok("D3 f", f3, 120, 1e-9); ok("D3 T ms", T3 * 1e3, 8.33, 5e-3); ok("D3 ω", w3, 754, 0.5); ok("D3 ω=240π", w3, 240 * PI, 1e-9)
ok("D3 θ rad", th3, 0.754, 5e-4); ok("D3 θ độ", math.degrees(th3), 43.2, 0.05); ok("D3 kiểm", f3 * 1e-3 * 360, 43.2, 1e-9)
assert abs(w3 * 1.0 - th3) > 100 and abs(360 * f3 - math.degrees(th3)) > 1000 and abs(w3 * T3 * 180 / PI - math.degrees(th3)) > 100     # các lựa chọn sai
assert abs(2 * PI * n3 - w3) > 1 and abs(f3 - w3) > 100 and abs(2 * PI * 60 / n3 - w3) > 100                     # quên chia 60 / quên 2π / lật ngược
# D4
n4, dia4, rN = 45, 0.30, 0.050
f4 = n4 / 60; w4 = 2 * PI * f4; rM = dia4 / 2; vM = w4 * rM; vN = w4 * rN
ok("D4 f", f4, 0.75, 1e-12); ok("D4 ω", w4, 4.71, 5e-3); ok("D4 ω=1,5π", w4, 1.5 * PI, 1e-12)
ok("D4 vM", vM, 0.707, 5e-4); ok("D4 vN", vN, 0.236, 5e-4); ok("D4 tỉ số", vM / vN, 3.0, 1e-12); ok("D4 tỉ số hiển thị", 0.707 / 0.236, 3.00, 0.01)
assert abs(w4 * dia4 - vM) > 0.3 and abs(vM - vN) > 0.4 and abs(w4 * rN * 100 - vN) > 1       # r = đường kính; giữ v_M; để r tính cm
assert abs(2 * PI * n4 * rM - vM) > 10                                                      # quên chia 60
# D5
n5, r5, n5b = 480, 0.40, 320
f5 = n5 / 60; w5 = 2 * PI * f5; v5 = w5 * r5; w5b = 2 * PI * n5b / 60; r5b = v5 / w5b
ok("D5 f", f5, 8.0, 1e-12); ok("D5 ω", w5, 50.3, 0.05); ok("D5 ω=16π", w5, 16 * PI, 1e-12); ok("D5 v", v5, 20.1, 0.05)
ok("D5 km/h", v5 * 3.6, 72, 0.5)
ok("D5 f₂", n5b / 60, 5.33, 0.005); ok("D5 ω₂", w5b, 33.5, 0.05); ok("D5 r₂", r5b, 0.60, 1e-9); ok("D5 r₂ cách tắt", r5 * n5 / n5b, 0.60, 1e-9)
ok("D5 r₂ từ số làm tròn", 20.1 / 33.5, 0.60, 0.005)
ok("D5 kiểm ω₁r₁", 50.3 * 0.40, 20.1, 0.05); ok("D5 kiểm ω₂r₂", 33.5 * 0.60, 20.1, 0.05)
assert abs(2 * PI * n5 - w5) > 100 and abs(2 * PI * n5b - w5b) > 100 and abs(n5b - w5b) > 100 and abs(v5 * w5b - r5b) > 100 and abs(w5b / v5 - r5b) > 1 and abs(r5 - r5b) > 0.1
assert abs(w5 * r5 - 2 * f5 * r5) > 10 and abs(w5 / r5 - v5) > 10
# Tự luận cũ
ok("VD3 f", 3600 / 60, 60, 0); ok("VD3 ω", 2 * PI * 60, 120 * PI, 1e-9)
ok("VD4 ω", 2 * PI * 125 / 60, 13.1, 0.05)
ok("VD5 T", 60 / 3000, 0.02, 1e-12)
ok("VD6 ω", 2 * PI / 86400, 7.27e-5, 5e-8); ok("VD6 v", 2 * PI / 86400 * 6.4e6, 465.4, 0.1)
ok("VD7 tỉ số", (1 / 60) * (4 / 5), 1 / 75, 1e-12); ok("VD8 tỉ số", 12 * 4 / 3, 16, 1e-12); ok("VD9", 15 / 3, 5, 0)
ok("VD2 b", 3.5 * 30, 105, 0); ok("VD2 rad", 105 * PI / 180, 7 * PI / 12, 1e-12)
ok("VD13 a", 27.32 / 365.25 * 2 * 3.14 * 1.5e11, 70.46e9, 0.01e9); ok("VD13 b", 365.25 / 27.32, 13.4, 0.05)

# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Nhận biết chuyển động tròn đều, vận tốc và độ dịch chuyển góc", topic=T34,
      problem_html=r"""<p>Một xe đồ chơi chạy ngược chiều kim đồng hồ trên đường ray hình tròn tâm $O$, bán kính $r=0{,}50\ \text{m}$. Đồng hồ tốc độ của xe luôn chỉ $0{,}40\ \text{m/s}$. Xét lúc xe đi qua điểm $A$ xa nhất về bên phải tâm $O$ (nhìn từ trên xuống).</p>
<ol type="a"><li>Chuyển động của xe có phải là chuyển động tròn đều không? Vận tốc của xe có đổi không?</li>
<li>Tại $A$, vectơ vận tốc có phương, chiều thế nào?</li>
<li>Sau $5{,}0\ \text{s}$ kể từ lúc qua $A$, xe đi được cung dài bao nhiêu và độ dịch chuyển góc là bao nhiêu radian?</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Tìm chu kì, tần số, tốc độ góc từ số vòng đếm được", topic=T146,
      problem_html=r"""<p>Một vòng đu quay trong công viên quay đều, quay hết $5$ vòng trong $2{,}0$ phút. Lúc bắt đầu tính thời gian, một cabin đang ở vị trí thấp nhất.</p>
<ol type="a"><li>Tính chu kì và tần số quay của vòng đu quay.</li>
<li>Tính tốc độ góc của vòng đu quay.</li>
<li>Sau $10\ \text{s}$ kể từ lúc đó, bán kính nối cabin ấy với trục quay đã quét một góc bao nhiêu độ?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Đổi vòng/phút sang rad/s và tìm góc quay trong thời gian ngắn", topic=T146,
      problem_html=r"""<p>Đĩa của một ổ cứng máy tính quay đều với tốc độ $7200$ vòng/phút. Lúc bắt đầu tính thời gian, một điểm đánh dấu gần mép đĩa nằm ở đỉnh đĩa (nhìn từ trên xuống).</p>
<ol type="a"><li>Tính tần số quay và chu kì quay (chu kì tính ra mili giây).</li>
<li>Tính tốc độ góc của đĩa theo rad/s.</li>
<li>Trong khoảng thời gian $1{,}0\ \text{ms}$, đĩa quay được một góc bao nhiêu độ?</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Các điểm cùng quay, khác bán kính: tốc độ v = ωr", topic=T147,
      problem_html=r"""<p>Một đĩa than có đường kính $30\ \text{cm}$ quay đều $45$ vòng/phút quanh trục qua tâm. Điểm $M$ nằm ở mép đĩa, điểm $N$ cách tâm $5{,}0\ \text{cm}$.</p>
<ol type="a"><li>Tính tốc độ góc của đĩa.</li>
<li>Tính tốc độ của điểm $M$.</li>
<li>Tính tốc độ của điểm $N$.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Cánh quạt: từ vòng/phút tìm tốc độ đầu cánh, bài ngược tìm chiều dài cánh mới", topic=T147,
      problem_html=r"""<p>Cánh quạt của một máy làm mát công nghiệp dài $0{,}40\ \text{m}$ (tính từ trục quay đến đầu cánh), quay đều $480$ vòng/phút.</p>
<ol type="a"><li>Tính tốc độ của đầu cánh.</li>
<li>Người ta thay cánh khác và cho quạt quay chậm lại còn $320$ vòng/phút, nhưng muốn đầu cánh vẫn giữ tốc độ như trước. Hỏi cánh mới phải dài bao nhiêu?</li></ol>"""),
]
FORMS = ["ly_thuyet", "bai_tap", "bai_tap", "bai_tap", "bai_tap"]

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“xe đồ chơi chạy ngược chiều kim đồng hồ trên đường ray hình tròn tâm $O$, bán kính $r=0{,}50$ m”", r"Quỹ đạo tròn; $r=0{,}50\ \text{m}$", r"Chuyển động tròn: quỹ đạo là đường tròn"),
  (r"“đồng hồ tốc độ của xe luôn chỉ $0{,}40$ m/s”", r"$v=0{,}40\ \text{m/s}$, không đổi", r"⚠ Chuyển động tròn đều cần đủ hai điều: quỹ đạo tròn và tốc độ không đổi"),
  (r"“a) có phải chuyển động tròn đều không? Vận tốc có đổi không?”", r"Cần kết luận về loại chuyển động và về vận tốc", r"Tốc độ chỉ là độ lớn; vận tốc là vectơ có phương, chiều"),
  (r"“b) tại $A$ … vectơ vận tốc có phương, chiều thế nào”", r"$A$ xa nhất về bên phải tâm; xe quay ngược chiều kim đồng hồ", r"Quan hệ giữa phương của vận tốc và quỹ đạo, bán kính"),
  (r"“c) sau $5{,}0$ s”", r"$t=5{,}0\ \text{s}$", r"Cung đi được khi tốc độ không đổi: $s=vt$"),
  (r"“cung dài bao nhiêu … độ dịch chuyển góc bao nhiêu radian”", r"Cần $s$ (m), $\theta$ (rad)", r"Đại lượng cần tìm: $\theta=\dfrac{s}{r}$")],
 [(r"“vòng đu quay quay đều”", r"$\omega$, $T$ không đổi", r"⚠ Chuyển động tròn đều: dùng được $\theta=\omega t$"),
  (r"“quay hết $5$ vòng trong $2{,}0$ phút”", r"$n=5$ vòng; $\Delta t=2{,}0\ \text{phút}$", r"⚠ Đổi thời gian ra giây trước khi tính"),
  (r"“a) chu kì và tần số”", r"Cần $T$ (s), $f$ (Hz)", r"Đại lượng cần tìm: $T=\dfrac{\Delta t}{n}$, $f=\dfrac{1}{T}$"),
  (r"“b) tốc độ góc”", r"Cần $\omega$ (rad/s)", r"Đại lượng cần tìm: $\omega=\dfrac{2\pi}{T}=2\pi f$"),
  (r"“c) sau $10$ s … quét một góc bao nhiêu độ”", r"$t=10\ \text{s}$; cần $\theta$ (độ)", r"Góc quét liên hệ với $\omega$ và thời gian; đổi rad sang độ")],
 [(r"“quay đều với tốc độ $7200$ vòng/phút”", r"$n=7200$ vòng/phút", r"⚠ Vòng/phút chưa phải đơn vị của $\omega$: đổi trước khi tính"),
  (r"“a) tần số quay và chu kì quay (ra mili giây)”", r"Cần $f$ (Hz), $T$ (ms)", r"Đại lượng cần tìm: $f=\dfrac{n}{60}$, $T=\dfrac{1}{f}$"),
  (r"“b) tốc độ góc theo rad/s”", r"Cần $\omega$ (rad/s)", r"Đại lượng cần tìm: $\omega=2\pi f$"),
  (r"“c) trong khoảng thời gian $1{,}0$ ms”", r"$t=1{,}0\ \text{ms}$", r"⚠ Thời gian đổi ra giây khi nhân với $\omega$ (rad/s)"),
  (r"“đĩa quay được một góc bao nhiêu độ”", r"Cần $\theta$ (độ)", r"Góc quét $\theta=\omega t$; đổi rad sang độ")],
 [(r"“đĩa than có đường kính $30$ cm”", r"$d=30\ \text{cm}$", r"⚠ Bán kính là nửa đường kính; đổi ra mét"),
  (r"“quay đều $45$ vòng/phút quanh trục qua tâm”", r"$n=45$ vòng/phút", r"Đổi sang $f$ rồi $\omega$"),
  (r"“a) tốc độ góc của đĩa”", r"Cần $\omega$ (rad/s)", r"Đại lượng cần tìm: $\omega=2\pi f$"),
  (r"“điểm $M$ nằm ở mép đĩa” — “b) tốc độ của $M$”", r"$M$ cách tâm một bán kính đĩa; cần $v_M$ (m/s)", r"Công thức liên hệ $v$, $\omega$, $r$: $v=\omega r$"),
  (r"“điểm $N$ cách tâm $5{,}0$ cm” — “c) tốc độ của $N$”", r"$r_N=5{,}0\ \text{cm}$; cần $v_N$ (m/s)", r"⚠ $M$ và $N$ cùng nằm trên một đĩa quay: so $\omega$ của hai điểm trước khi chọn công thức")],
 [(r"“cánh quạt … dài $0{,}40$ m (tính từ trục quay đến đầu cánh)”", r"$r_1=0{,}40\ \text{m}$", r"Bán kính quỹ đạo của đầu cánh"),
  (r"“quay đều $480$ vòng/phút”", r"$n=480$ vòng/phút", r"⚠ Đổi vòng/phút trước khi dùng $\omega$"),
  (r"“a) tốc độ của đầu cánh”", r"Cần $v_1$ (m/s)", r"Đại lượng cần tìm: $v=\omega r$"),
  (r"“quay chậm lại còn $320$ vòng/phút”", r"$n_2=320$ vòng/phút", r"⚠ Đổi vòng/phút trước khi dùng $\omega$"),
  (r"“đầu cánh vẫn giữ tốc độ như trước”", r"$v_2=v_1$", r"⚠ Giữ $v$ thì $r$ phải chọn lại theo $\omega$ mới"),
  (r"“b) cánh mới phải dài bao nhiêu”", r"Cần $r_2$ (m)", r"Bán kính quỹ đạo của đầu cánh mới; $v=\omega r$ viết cho cánh mới")],
]

# ═════════════ Lời giải từng bước ═════════════
R_D1 = [r"<strong>Khái niệm:</strong> chuyển động tròn đều có quỹ đạo tròn và tốc độ không đổi.",
        r"Vận tốc là vectơ: phương tiếp tuyến với quỹ đạo, chiều theo chiều chuyển động, độ lớn bằng tốc độ $v$.",
        r"Cung đi được: $s=vt$. Độ dịch chuyển góc: $\theta=\dfrac{s}{r}$ (rad).",
        r"⚠ <strong>Điều kiện:</strong> $s=vt$ chỉ dùng khi tốc độ $v$ không đổi."]
R_D2 = [r"<strong>Khái niệm:</strong> chu kì $T$ là thời gian đi hết một vòng; $n$ vòng trong $\Delta t$ thì $T=\dfrac{\Delta t}{n}$.",
        r"Tần số $f=\dfrac{1}{T}$ (Hz).",
        r"Tốc độ góc $\omega=\dfrac{2\pi}{T}=2\pi f$ (rad/s); góc quét $\theta=\omega t$.",
        r"⚠ <strong>Điều kiện:</strong> thời gian đổi ra giây; $\omega$ không đổi nên dùng được $\theta=\omega t$."]
R_D3 = [r"Vòng/phút → vòng/giây: chia $60$, được tần số $f$.",
        r"$\omega=2\pi f$; $T=\dfrac{1}{f}$.",
        r"Góc quét $\theta=\omega t$ (rad); đổi sang độ: nhân $\dfrac{180^\circ}{\pi}$.",
        r"⚠ <strong>Điều kiện:</strong> $t$ đổi ra giây ($1\ \text{ms}=10^{-3}\ \text{s}$) trước khi nhân với $\omega$."]
R_D4 = [r"Mọi điểm của một vật quay đều có cùng $\omega$, $T$, $f$.",
        r"$\omega=2\pi f$ (vòng/phút: chia $60$ rồi nhân $2\pi$).",
        r"Tốc độ của điểm cách trục $r$: $v=\omega r$.",
        r"⚠ <strong>Điều kiện:</strong> $r$ là khoảng cách từ điểm đó đến trục (bán kính, nửa đường kính), đổi ra mét."]
R_D5 = [r"Vòng/phút → $f$: chia $60$; $\omega=2\pi f$.",
        r"Đầu cánh cách trục một đoạn bằng chiều dài cánh: $v=\omega r$.",
        r"Đổi ngược: $r=\dfrac{v}{\omega}$; vòng/phút → $\omega=2\pi\cdot\dfrac{n}{60}$.",
        r"⚠ <strong>Điều kiện:</strong> thay cánh và đổi tốc độ quay thì $r$ được chọn lại để giữ $v$; các điểm của cùng một cánh vẫn cùng $\omega$."]

SOLS = [
 sol(R_D1, [
  (r"Loại chuyển động", [P(r"Quỹ đạo là đường tròn bán kính $0{,}50\ \text{m}$."), P(r"Đồng hồ tốc độ luôn chỉ cùng một số, nên tốc độ không đổi."), A(r"T:Đây là chuyển động tròn đều.")]),
  (r"Vận tốc có đổi không", [P(r"Tốc độ chỉ là độ lớn của vận tốc."), P(r"Vận tốc là vectơ: hướng đổi cũng là vận tốc đổi."), A(r"T:Tốc độ không đổi nhưng vận tốc đổi hướng liên tục.")]),
  (r"Vận tốc tại $A$", [P(r"Bán kính $OA$ nằm ngang; vận tốc vuông góc với bán kính nên nằm trên tiếp tuyến, thẳng đứng."), P(r"Xe đi ngược chiều kim đồng hồ qua điểm bên phải nên đi lên."), A(r"T:$\vec v$ thẳng đứng, hướng lên, độ lớn $0{,}40\ \text{m/s}$.")]),
  (r"Cung đi được sau $5{,}0\ \text{s}$", [P(r"Tốc độ không đổi nên:"), M(r"s=vt=0{,}40\cdot5{,}0"), A(r"s=2{,}0\ \text{m}")]),
  (r"Độ dịch chuyển góc", [M(r"\theta=\dfrac{s}{r}=\dfrac{2{,}0}{0{,}50}"), A(r"\theta=4{,}0\ \text{rad}")]),
  (r"Kiểm tra", [P(r"$4{,}0\ \text{rad}\approx229^\circ$: lớn hơn nửa vòng ($\pi\approx3{,}14\ \text{rad}$), nhỏ hơn một vòng ($2\pi\approx6{,}28\ \text{rad}$)."), P(r"Chu vi đường ray $2\pi r\approx3{,}14\ \text{m}$; xe đi $2{,}0\ \text{m}$ nên chưa hết vòng ✓.")])],
  [r"a) chuyển động tròn đều; vận tốc đổi hướng liên tục", r"b) $\vec v$ thẳng đứng, hướng lên", r"c) $s=2{,}0\ \text{m}$ · $\theta=4{,}0\ \text{rad}$"],
  r"Nhận dạng: đề cho <strong>quỹ đạo tròn</strong> và <strong>tốc độ không đổi</strong> → chuyển động tròn đều; vận tốc luôn tiếp tuyến, $\theta=\dfrac{s}{r}$."),
 sol(R_D2, [
  (r"Chu kì", [P(r"Đổi thời gian ra giây: $\Delta t=2{,}0\ \text{phút}=120\ \text{s}$."), M(r"T=\dfrac{\Delta t}{n}=\dfrac{120}{5}"), A(r"T=24\ \text{s}")]),
  (r"Tần số", [M(r"f=\dfrac{1}{T}=\dfrac{1}{24}"), A(r"f\approx0{,}0417\ \text{Hz}")]),
  (r"Tốc độ góc", [M(r"\omega=\dfrac{2\pi}{T}=\dfrac{2\pi}{24}"), A(r"\omega=\dfrac{\pi}{12}\approx0{,}262\ \text{rad/s}")]),
  (r"Góc quét sau $10\ \text{s}$", [M(r"\theta=\omega t=\dfrac{\pi}{12}\cdot10"), M(r"\theta=\dfrac{5\pi}{6}\ \text{rad}\approx2{,}62\ \text{rad}"), P(r"Đổi sang độ:"), M(r"\theta=\dfrac{5\pi}{6}\cdot\dfrac{180^\circ}{\pi}"), A(r"\theta=150^\circ")]),
  (r"Kiểm tra", [M(r"\omega T=\dfrac{\pi}{12}\cdot24=2\pi\ \text{rad}"), P(r"Đúng bằng một vòng ✓."), P(r"$\dfrac{10}{24}\approx0{,}417$ vòng; $0{,}417\cdot360^\circ=150^\circ$ ✓.")])],
  [r"a) $T=24\ \text{s}$ · $f\approx0{,}0417\ \text{Hz}$", r"b) $\omega\approx0{,}262\ \text{rad/s}$", r"c) $\theta=150^\circ$"],
  r"Nhận dạng: đề cho <strong>số vòng và thời gian đếm được</strong> → $T=\dfrac{\Delta t}{n}$, rồi $f$, $\omega$ và góc quét $\theta=\omega t$."),
 sol(R_D3, [
  (r"Tần số", [M(r"f=\dfrac{n}{60}=\dfrac{7200}{60}"), A(r"f=120\ \text{Hz}")]),
  (r"Chu kì", [M(r"T=\dfrac{1}{f}=\dfrac{1}{120}\ \text{s}\approx0{,}00833\ \text{s}"), A(r"T\approx8{,}33\ \text{ms}")]),
  (r"Tốc độ góc", [M(r"\omega=2\pi f=2\pi\cdot120=240\pi"), A(r"\omega\approx754\ \text{rad/s}")]),
  (r"Góc quét trong $1{,}0\ \text{ms}$", [P(r"Đổi thời gian: $t=1{,}0\ \text{ms}=10^{-3}\ \text{s}$."), M(r"\theta=\omega t=240\pi\cdot10^{-3}\approx0{,}754\ \text{rad}"), P(r"Đổi sang độ:"), M(r"\theta=0{,}754\cdot\dfrac{180^\circ}{\pi}"), A(r"\theta\approx43{,}2^\circ")]),
  (r"Kiểm tra", [P(r"Trong $1{,}0\ \text{ms}$ đĩa quay $f\cdot t=120\cdot10^{-3}=0{,}12$ vòng."), M(r"0{,}12\cdot360^\circ=43{,}2^\circ"), P(r"Khớp với kết quả trên ✓.")])],
  [r"a) $f=120\ \text{Hz}$ · $T\approx8{,}33\ \text{ms}$", r"b) $\omega\approx754\ \text{rad/s}$", r"c) $\theta\approx43{,}2^\circ$"],
  r"Nhận dạng: đề cho <strong>vòng/phút</strong> → chia $60$ ra $f$, nhân $2\pi$ ra $\omega$; thời gian ngắn thì đổi ra giây."),
 sol(R_D4, [
  (r"Tốc độ góc của đĩa", [M(r"f=\dfrac{n}{60}=\dfrac{45}{60}=0{,}75\ \text{Hz}"), M(r"\omega=2\pi f=2\pi\cdot0{,}75=1{,}5\pi"), A(r"\omega\approx4{,}71\ \text{rad/s}")]),
  (r"Tốc độ của điểm $M$", [P(r"$M$ ở mép nên bán kính bằng nửa đường kính: $r_M=\dfrac{30}{2}=15\ \text{cm}=0{,}15\ \text{m}$."), M(r"v_M=\omega r_M=1{,}5\pi\cdot0{,}15"), A(r"v_M\approx0{,}707\ \text{m/s}")]),
  (r"Tốc độ của điểm $N$", [P(r"Cùng một đĩa nên $N$ có cùng $\omega$; chỉ bán kính khác: $r_N=5{,}0\ \text{cm}=0{,}050\ \text{m}$."), M(r"v_N=\omega r_N=1{,}5\pi\cdot0{,}050"), A(r"v_N\approx0{,}236\ \text{m/s}")]),
  (r"Kiểm tra", [M(r"\dfrac{v_M}{v_N}=\dfrac{r_M}{r_N}=\dfrac{15}{5{,}0}=3"), P(r"Từ hai kết quả: $\dfrac{0{,}707}{0{,}236}\approx3{,}00$ ✓."), P(r"Hai điểm cùng $\omega$ nên tốc độ tỉ lệ với bán kính.")])],
  [r"a) $\omega\approx4{,}71\ \text{rad/s}$", r"b) $v_M\approx0{,}707\ \text{m/s}$", r"c) $v_N\approx0{,}236\ \text{m/s}$"],
  r"Nhận dạng: đề cho <strong>nhiều điểm trên cùng một vật quay</strong> → cùng $\omega$, tính $v=\omega r$ với $r$ riêng từng điểm."),
 sol(R_D5, [
  (r"Tần số", [M(r"f=\dfrac{n}{60}=\dfrac{480}{60}"), A(r"f=8{,}0\ \text{Hz}")]),
  (r"Tốc độ góc", [M(r"\omega=2\pi f=2\pi\cdot8{,}0=16\pi"), A(r"\omega\approx50{,}3\ \text{rad/s}")]),
  (r"Tốc độ đầu cánh", [P(r"Đầu cánh cách trục $r_1=0{,}40\ \text{m}$:"), M(r"v=\omega r_1=16\pi\cdot0{,}40"), A(r"v\approx20{,}1\ \text{m/s}"), P(r"Khoảng $72\ \text{km/h}$.")]),
  (r"Tốc độ góc mới", [P(r"Quạt quay $n_2=320$ vòng/phút:"), M(r"f_2=\dfrac{n_2}{60}=\dfrac{320}{60}\approx5{,}33\ \text{Hz}"), M(r"\omega_2=2\pi f_2=2\pi\cdot5{,}33"), A(r"\omega_2\approx33{,}5\ \text{rad/s}")]),
  (r"Chiều dài cánh mới", [P(r"Giữ $v=20{,}1\ \text{m/s}$ ở đầu cánh mới:"), M(r"r_2=\dfrac{v}{\omega_2}=\dfrac{20{,}1}{33{,}5}"), A(r"r_2\approx0{,}60\ \text{m}")]),
  (r"Kiểm tra", [M(r"\omega_1r_1=50{,}3\cdot0{,}40\approx20{,}1\ \text{m/s}"), M(r"\omega_2r_2=33{,}5\cdot0{,}60\approx20{,}1\ \text{m/s}"), P(r"Cách tắt: $r_2=r_1\cdot\dfrac{n_1}{n_2}=0{,}40\cdot\dfrac{480}{320}=0{,}60\ \text{m}$ ✓.")])],
  [r"a) $v\approx20{,}1\ \text{m/s}$", r"b) $r_2\approx0{,}60\ \text{m}$"],
  r"Nhận dạng: <strong>đổi tốc độ quay, giữ tốc độ đầu cánh</strong> → $v=\omega r$ cố định, đổi vòng/phút ra $\omega$ rồi tìm $r$."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>quỹ đạo tròn</b> và <b>tốc độ không đổi</b> → nghĩ tới <b>chuyển động tròn đều</b> và <b>$\theta=\dfrac{s}{r}$</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Loại chuyển động", r"Chuyển động của xe thuộc loại nào?",
       loi=r"Cho rằng vận tốc đổi hướng thì tốc độ cũng đổi, nên không gọi là đều.",
       lua_chon=[(r"Tròn đều: quỹ đạo tròn, tốc độ không đổi", True),
                 (r"Không đều: vận tốc đổi hướng nên tốc độ cũng đổi", r"Tốc độ chỉ là độ lớn của vận tốc; hướng đổi không làm tốc độ đổi. Đồng hồ vẫn chỉ cùng một số."),
                 (r"Chưa kết luận được, vì chưa biết chu kì", r"Tròn đều chỉ đòi hai điều: quỹ đạo tròn và tốc độ không đổi; không cần biết chu kì.")]),
  buoc(r"Vận tốc có đổi không", r"Vận tốc (vectơ) của xe có đổi không?",
       loi=r"Coi vận tốc và tốc độ là một: tốc độ không đổi nên vận tốc không đổi.",
       lua_chon=[(r"Có đổi, vì hướng của vận tốc thay đổi liên tục", True),
                 (r"Không đổi, vì tốc độ không đổi", r"Vận tốc là vectơ; chỉ cần hướng đổi là vận tốc đã đổi."),
                 (r"Không đổi, vì xe chạy trên đường ray có hình dạng cố định", r"Hình dạng đường ray cố định, nhưng phương tiếp tuyến của nó đổi từ điểm này sang điểm khác.")]),
  buoc(r"Vận tốc tại $A$", r"Tại $A$, vectơ vận tốc hướng thế nào?",
       loi=r"Vẽ vận tốc theo phương bán kính, hoặc vẽ đúng phương nhưng ngược chiều chuyển động.",
       lua_chon=[(r"Thẳng đứng, hướng lên", True),
                 (r"Nằm ngang, hướng vào tâm $O$", r"Phương hướng vào tâm là phương bán kính; vận tốc vuông góc với bán kính."),
                 (r"Thẳng đứng, hướng xuống", r"Đúng phương tiếp tuyến nhưng ngược với chiều chuyển động của xe (ngược chiều kim đồng hồ).")]),
  buoc(r"Cung đi được sau $5{,}0\ \text{s}$", r"Cung $s$ xe đi được sau $5{,}0\ \text{s}$ dài bao nhiêu mét?", 2.0, "m", 0.05,
       loi=r"Lấy tốc độ chia cho thời gian, hoặc nhân với $r$ thay cho thời gian."),
  buoc(r"Độ dịch chuyển góc", r"Độ dịch chuyển góc $\theta$ bằng bao nhiêu radian?", 4.0, "rad", 0.05,
       loi=r"Nhân cung với bán kính thay vì chia, hoặc lấy luôn độ dài cung làm góc."),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>số vòng đếm được trong một khoảng thời gian</b> → nghĩ tới <b>$T=\dfrac{\Delta t}{n}$</b>, rồi $f$, $\omega$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Chu kì", r"Chu kì $T$ bằng bao nhiêu giây?", 24, "s", 0.1,
       loi=r"Quên đổi phút ra giây, hoặc chia số vòng cho thời gian (ra tần số chứ không phải chu kì)."),
  buoc(r"Tần số", r"Tần số $f$ bằng bao nhiêu hertz?", 0.0417, "Hz", 0.001,
       loi=r"Dùng $f=T$ hoặc lấy số vòng chia cho số phút rồi coi là hertz."),
  buoc(r"Tốc độ góc", r"Tốc độ góc $\omega$ bằng bao nhiêu rad/s?", 0.262, "rad/s", 0.003,
       loi=r"Quên nhân với $2\pi$ (ra chính $f$), hoặc chia $2\pi$ cho tần số thay vì cho chu kì."),
  buoc(r"Góc quét sau $10\ \text{s}$", r"Sau $10\ \text{s}$ bán kính nối cabin quét góc bao nhiêu độ?", 150, "°", 1,
       loi=r"Quên đổi radian sang độ, hoặc nhân $\omega$ với chu kì thay cho thời gian $10\ \text{s}$."),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vòng/phút</b> → nghĩ tới <b>chia $60$ ra $f$, nhân $2\pi$ ra $\omega$</b>; thời gian ngắn thì đổi ra giây.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Tần số", r"Tần số $f$ bằng bao nhiêu hertz?", 120, "Hz", 1,
       loi=r"Quên chia $60$ (coi $7200$ là số vòng mỗi giây), hoặc nhân với $60$ thay vì chia."),
  buoc(r"Chu kì", r"Chu kì $T$ bằng bao nhiêu mili giây?", 8.33, "ms", 0.05,
       loi=r"Đổi giây sang mili giây sai hệ số, hoặc lấy $T=f$."),
  buoc(r"Tốc độ góc", r"Tốc độ góc $\omega$ bằng bao nhiêu rad/s?", 754, "rad/s", 2,
       loi=r"Dừng ở bước đổi sang vòng/giây (được $f$ chứ chưa phải $\omega$), hoặc quên chia $60$.",
       ke=[(r"Từ $f$ đã có, nhân với $2\pi$", True),
           (r"Lấy luôn $f$ làm $\omega$", r"$f$ tính theo vòng/giây còn $\omega$ tính theo rad/s; mỗi vòng là $2\pi\ \text{rad}$."),
           (r"Nhân $7200$ với $2\pi$ rồi dừng", r"$7200$ là vòng mỗi phút; $\omega$ cần vòng mỗi giây, nên còn phải chia $60$.")]),
  buoc(r"Góc quét trong $1{,}0\ \text{ms}$", r"Trong $1{,}0\ \text{ms}$ đĩa quay được góc bao nhiêu độ?", 43.2, "°", 0.3,
       loi=r"Quên đổi mili giây ra giây, hoặc quên đổi radian sang độ.",
       ke=[(r"Nhân $\omega$ với $t$ đã đổi ra giây, rồi đổi sang độ", True),
           (r"Nhân $\omega$ với $1{,}0$ (giữ nguyên số của mili giây)", r"$\omega$ tính theo rad/s nên thời gian phải ở đơn vị giây; để nguyên số mili giây thì kết quả sai hệ số một nghìn."),
           (r"Lấy $360^\circ$ nhân với tần số $f$", r"Tích đó cho góc quay trong $1\ \text{s}$ chứ không phải trong $1{,}0\ \text{ms}$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>nhiều điểm trên cùng một vật quay</b> → nghĩ tới <b>cùng $\omega$</b>, $v=\omega r$ với $r$ riêng từng điểm.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Tốc độ góc của đĩa", r"Tốc độ góc $\omega$ của đĩa bằng bao nhiêu rad/s?", 4.71, "rad/s", 0.03,
       loi=r"Dùng $\omega=2\pi n$ với $n$ tính bằng vòng/phút (quên chia $60$)."),
  buoc(r"Tốc độ của điểm $M$", r"Tốc độ $v_M$ của điểm $M$ ở mép bằng bao nhiêu m/s?", 0.707, "m/s", 0.005,
       loi=r"Lấy bán kính bằng cả đường kính, hoặc để $r$ tính bằng cm rồi ghi kết quả là m/s."),
  buoc(r"Tốc độ của điểm $N$", r"Tốc độ $v_N$ của điểm $N$ bằng bao nhiêu m/s?", 0.236, "m/s", 0.003,
       loi=r"Cho mỗi điểm một $\omega$ riêng theo khoảng cách tới tâm, hoặc lấy lại tốc độ của $M$.",
       ke=[(r"Giữ nguyên $\omega$ của đĩa, thay $r$ bằng khoảng cách từ $N$ đến tâm", True),
           (r"Dùng $\omega$ riêng cho $N$ vì $N$ nằm gần tâm", r"Mọi điểm của đĩa quét cùng một góc trong cùng thời gian nên có chung $\omega$; chỉ $v$ phụ thuộc $r$."),
           (r"Giữ nguyên $v_M$ vì cùng một đĩa", r"Cùng $\omega$ nhưng khác bán kính quỹ đạo thì $v=\omega r$ khác nhau.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>đổi tốc độ quay, giữ tốc độ đầu cánh</b> → nghĩ tới <b>$v=\omega r$</b> với $r$ đổi theo $\omega$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc(r"Tần số", r"Tần số $f$ của quạt bằng bao nhiêu hertz?", 8.0, "Hz", 0.05,
       loi=r"Quên chia $60$, hoặc nhân với $60$ thay vì chia."),
  buoc(r"Tốc độ góc", r"Tốc độ góc $\omega$ bằng bao nhiêu rad/s?", 50.3, "rad/s", 0.3,
       loi=r"Nhân $2\pi$ với số vòng/phút thay vì tần số.",
       ke=[(r"Nhân $2\pi$ với tần số tính bằng Hz", True),
           (r"Nhân $2\pi$ với số vòng/phút", r"Số vòng/phút chưa phải vòng/giây; $\omega$ theo rad/s phải dùng $f$ (vòng/giây)."),
           (r"Lấy $2\pi$ chia cho tần số", r"Phải chia $2\pi$ cho chu kì; chia cho tần số thì ra đơn vị không phải rad/s.")]),
  buoc(r"Tốc độ đầu cánh", r"Tốc độ $v$ của đầu cánh bằng bao nhiêu m/s?", 20.1, "m/s", 0.2,
       loi=r"Dùng $v=\omega/r$, hoặc lấy tần số thay cho tốc độ góc.",
       ke=[(r"Dùng $v=\omega r$ với $r$ là chiều dài cánh", True),
           (r"Dùng $v=\omega/r$", r"Chia $\omega$ cho $r$ cho đơn vị $1/(\text{m}\cdot\text{s})$, không phải m/s."),
           (r"Lấy $v=f\cdot r$", r"Thiếu hệ số $2\pi$: một vòng dài $2\pi r$, nên $v=2\pi fr=\omega r$.")]),
  buoc(r"Tốc độ góc mới", r"Quạt quay $320$ vòng/phút thì $\omega_2$ bằng bao nhiêu rad/s?", 33.5, "rad/s", 0.3,
       loi=r"Lấy luôn số vòng/phút làm $\omega$, hoặc nhân $2\pi$ với số vòng/phút mà quên chia $60$.",
       ke=[(r"Chia $60$ ra $f_2$ rồi nhân $2\pi$", True),
           (r"Lấy $\omega_2$ bằng số vòng/phút", r"Vòng/phút là đơn vị của $n$; $\omega$ tính theo rad/s, mỗi vòng là $2\pi\ \text{rad}$ và mỗi phút có $60$ giây."),
           (r"Nhân $2\pi$ với số vòng/phút", r"Chưa chia $60$ thì chưa ra vòng/giây nên kết quả sai hệ số $60$.")]),
  buoc(r"Chiều dài cánh mới", r"Cánh mới dài $r_2$ bằng bao nhiêu mét?", 0.6, "m", 0.01,
       loi=r"Nhân $v$ với $\omega_2$ thay vì chia, hoặc giữ nguyên chiều dài cánh cũ.",
       ke=[(r"Giữ $v$ của đầu cánh, lấy $v$ chia cho $\omega_2$", True),
           (r"Lấy $v$ nhân với $\omega_2$", r"Tích $v\omega$ có đơn vị $\text{m/s}^2$, không phải mét."),
           (r"Lấy $\omega_2$ chia cho $v$", r"Thương $\omega/v$ có đơn vị $1/\text{m}$, đó là $1/r$ chứ không phải $r$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ Tự luận: ví dụ cũ chưa biên tập (idx 0-based trong old/76.json), xếp dễ → khó ═════════════
# idx0 VD1: s = θr · idx1 VD2: kim giờ · idx2 VD3: bảng độ ↔ rad · idx3 VD4: 3600 vòng/phút · idx4 VD5: 125 vòng/phút
# idx5 VD6: chu kì quạt · idx6 VD7: xích đạo · idx7 VD8: tỉ số kim phút/giây · idx8 VD9: tỉ số kim giờ/phút · idx9 VD10: A, B cùng chu kì
# idx10 VD11: hai vật gặp nhau · idx13 VD14: Trái Đất–Mặt Trăng
ORDER = [2, 0, 1, 5, 3, 4, 6, 9, 7, 8, 13, 10]
MUC = {2: "Dễ", 0: "Dễ", 1: "Dễ", 5: "Dễ", 3: "Dễ", 4: "Trung bình", 6: "Trung bình", 9: "Trung bình", 7: "Trung bình", 8: "Trung bình", 13: "Khó", 10: "Khó"}
def _sub(i, a, c):
    assert a in OLD[i]["body_html"], (i, a)
    OLD[i]["body_html"] = OLD[i]["body_html"].replace(a, c)
_sub(0, r"s = \theta r = 1.2 = 2$ m.", r"s = \theta r = 1\cdot 2 = 2$ m.")
for _i in ORDER:
    _h = OLD[_i]["body_html"]
    _h = re.sub(r'alt="[^"]*"', 'alt=""', _h)
    _h = _h.replace("=&gt;", r"\Rightarrow ").replace("=>", r"\Rightarrow ")
    OLD[_i]["body_html"] = _h
TU_LUAN = tu_luan_tu(OLD, ORDER, MUC)

write(J, 76, "Bài 31. Động học của chuyển động tròn đều", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-11"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
