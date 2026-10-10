"""Bài 69 — "Bài 24. Công suất" (Vật lí 10, chương 4). 5 dạng; chưa có ví dụ cũ nên KHÔNG có tự luận.
Mẫu: build-hinh-58.py. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-69.py  → ghi scripts/data/bai-tap-mau/69.json
Dạng theo quét: scripts/logs/batch-ra-soat/ket-qua/69.quet-dang.json (5 dạng, cấp 1,1,2,3,4). Hình: hinh_69.py.
Lệch có chủ ý so với bản quét: dạng 4 chọn tình huống nâng vật (thời gian ngắn nhất), dạng 5 gộp "chạy đều: lực kéo = lực cản" với xe lên dốc."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_69 import BUILD

J = os.path.join(HERE, "69.json")
T28, T134, T135 = "Công suất", "Tính công suất trung bình và công suất tức thời", "Công suất của động cơ, máy kéo"

# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
# D1: bơm 2,0 kW × 3,0 h
Pk, t = 2.0, 3.0
A_kwh = Pk * t; ok("D1 kWh", A_kwh, 6.0, 1e-9)
A_J = (Pk * 1000) * (t * 3600); ok("D1 J", A_J, 2.16e7, 1); ok("D1 J qua kWh", A_kwh * 3.6e6, A_J, 1)
CV = 2000 / 736; ok("D1 CV", CV, 2.72, 0.005)
t2 = A_kwh / 0.50; ok("D1 t'", t2, 12, 1e-9); ok("D1 kiểm", 0.50 * t2, A_kwh, 1e-9)
assert len({round(x, 3) for x in (A_kwh, A_kwh * 3600, A_kwh * 1000)}) == 3           # các cách sai cho kết quả khác
assert abs(2.0 * 736 - 2000 / 736) > 1000 and abs(2.0 / 736 - CV) > 2 and abs(0.50 / A_kwh - t2) > 10 and abs(t - t2) > 5
# D2
F1, d1, s1 = 120.0, 15.0, 20.0
A1 = F1 * d1; ok("D2 A1", A1, 1800, 1e-9); P1 = A1 / s1; ok("D2 P1", P1, 90, 1e-9)
m, h, s2 = 24.0, 1.5, 3.0; F2 = m * 10; ok("D2 F2", F2, 240, 1e-9)
A2 = F2 * h; ok("D2 A2", A2, 360, 1e-9); P2 = A2 / s2; ok("D2 P2", P2, 120, 1e-9)
ok("D2 kiểm1", F1 * (d1 / s1), P1, 1e-9); ok("D2 kiểm2", F2 * (h / s2), P2, 1e-9)
assert len({A1, P1, F2, A2, P2, F1 * h, F2 * d1, A2 / s1, m * h}) == 9
# D3
v = 36 / 3.6; ok("D3 v", v, 10, 1e-9); Pa = 150 * v; ok("D3 P", Pa, 1500, 1e-9)
Ab = Pa * 5.0 * 60; ok("D3 A", Ab / 1000, 450, 1e-9); ok("D3 kiểm A=Fs", 150 * (v * 300) / 1000, 450, 1e-9)
v3 = 54 / 3.6; ok("D3 v'", v3, 15, 1e-9); Pc = 120 * v3; ok("D3 P'", Pc / 1000, 1.8, 1e-9)
assert len({Pa, 150 * 36, 150 / v, Pa * 5, Pc, 120 * 36, Pa * 5.0 / 1000}) == 7 and abs(Pc - Pa) > 100
# D4
m, g, Pd = 750.0, 10.0, 22500.0; F = m * g; ok("D4 F", F, 7500, 1e-9)
vmax = Pd / F; ok("D4 v", vmax, 3.0, 1e-9); tmin = 30 / vmax; ok("D4 t", tmin, 10, 1e-9)
ok("D4 kiểm", m * g * 30, 225000, 1e-9); ok("D4 kiểm Pt", Pd * tmin, 225000, 1e-9)
assert abs(Pd / 30 - tmin) > 100 and abs(30 / 22.5 - tmin) > 5 and abs(F / Pd - vmax) > 2 and abs(30 / 3.0 - tmin) < 1e-9
# D5
m, Pm, Fc = 4500.0, 36000.0, 1800.0; v1 = Pm / Fc; ok("D5 v1", v1, 20, 1e-9)
sinA = 6 / 100; Fd = m * 10 * sinA; ok("D5 Fd", Fd, 2700, 1e-9); F2 = Fc + Fd; ok("D5 F2", F2, 4500, 1e-9)
v2 = Pm / F2; ok("D5 v2", v2, 8.0, 1e-9); ok("D5 km/h", v2 * 3.6, 28.8, 1e-9); t5 = 500 / v2; ok("D5 t", t5, 62.5, 1e-9)
ok("D5 kiểm Fv", F2 * v2, Pm, 1e-9); ok("D5 tỉ số", F2 / Fc, 2.5, 1e-9); ok("D5 v1/2,5", v1 / 2.5, v2, 1e-9)
assert len({round(x, 3) for x in (F2, Fc, Fd, m * 10, Pm / Fc, Pm / (m * 10), v2, 500 / v1)}) == 8      # các cách sai khác đáp án
assert abs(Pm / (Fc + m * 10) - v2) > 0.5 and abs(Pm / Fc - v2) > 5 and abs(Fc - F2) > 1000


# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Công suất, công và đổi đơn vị (kWh, mã lực)", topic=T28,
      problem_html=r"""<p>Một máy bơm nước có công suất $2{,}0\ \text{kW}$, hoạt động liên tục $3{,}0$ giờ.</p>
<ol type="a"><li>Tính công máy bơm sinh ra, theo kWh và theo jun.</li>
<li>Công suất của máy bơm bằng bao nhiêu mã lực Pháp? Lấy $1\ \text{CV}=736\ \text{W}$.</li>
<li>Một máy bơm khác có công suất $0{,}50\ \text{kW}$ phải hoạt động bao lâu để sinh cùng công đó?</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Công suất trung bình khi kéo vật trượt và khi nâng vật", topic=T134,
      problem_html=r"""<p>Một người làm hai việc liên tiếp.</p>
<ol type="a"><li>Kéo đều một thùng hàng trượt trên sàn ngang bằng lực kéo $120\ \text{N}$ cùng hướng chuyển động. Thùng đi được $15\ \text{m}$ trong $20\ \text{s}$. Tính công của lực kéo và công suất trung bình khi kéo.</li>
<li>Nâng đều thùng hàng $24\ \text{kg}$ từ sàn lên giá cao $1{,}5\ \text{m}$ trong $3{,}0\ \text{s}$. Lấy $g=10\ \text{m/s}^2$. Tính công suất trung bình của lực nâng.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Công suất tức thời P = F·v, đổi km/h ra m/s", topic=T134,
      problem_html=r"""<p>Một xe máy điện chạy trên đường thẳng nằm ngang. Lực kéo của động cơ luôn cùng hướng chuyển động.</p>
<ol type="a"><li>Xe chạy đều với tốc độ $36\ \text{km/h}$, lực kéo $150\ \text{N}$. Tính công suất tức thời của động cơ.</li>
<li>Xe giữ chạy đều như vậy trong $5{,}0$ phút. Tính công động cơ sinh ra.</li>
<li>Sau đó xe tăng tốc. Lúc tốc độ đạt $54\ \text{km/h}$ thì lực kéo là $120\ \text{N}$. Tính công suất tức thời lúc đó.</li></ol>"""),
 dict(label="Dạng 4 · Khó · Công suất động cơ nâng vật: lực nâng, vận tốc lớn nhất, thời gian ngắn nhất", topic=T135,
      problem_html=r"""<p>Một cần cẩu tháp có động cơ công suất $22{,}5\ \text{kW}$ nâng đều một kiện vật liệu khối lượng $750\ \text{kg}$ từ mặt đất lên tầng cao $30\ \text{m}$. Coi toàn bộ công suất của động cơ dùng để nâng kiện vật liệu. Lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Tính lực nâng của cáp.</li>
<li>Tính vận tốc nâng đều lớn nhất.</li>
<li>Tính thời gian ngắn nhất để nâng kiện vật liệu lên $30\ \text{m}$.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Xe lên dốc với công suất tối đa: lực kéo tăng, vận tốc giảm", topic=T135,
      problem_html=r"""<p>Một ô tô tải khối lượng $4{,}5$ tấn có động cơ công suất tối đa $36\ \text{kW}$. Tổng lực cản (ma sát và không khí) là $1800\ \text{N}$, coi không đổi cả trên đường ngang lẫn khi lên dốc. Lấy $g=10\ \text{m/s}^2$.</p>
<ol type="a"><li>Xe chạy đều trên đường ngang với công suất tối đa. Tính vận tốc của xe.</li>
<li>Xe lên dốc có độ dốc $6\,\%$ (đi $100\ \text{m}$ theo mặt dốc thì lên cao $6\ \text{m}$). Tính lực kéo của động cơ khi xe lên dốc đều.</li>
<li>Xe lên dốc đều với công suất tối đa. Tính vận tốc của xe.</li>
<li>Đoạn dốc dài $500\ \text{m}$. Tính thời gian xe đi hết đoạn dốc này.</li></ol>"""),
]
FORMS = ["bai_tap"] * 5

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“máy bơm nước có công suất $2{,}0$ kW”", r"$P=2{,}0\ \text{kW}$", r"Công suất: tốc độ sinh công; đơn vị W, kW, mã lực"),
  (r"“hoạt động liên tục”", r"Công suất không đổi trong cả khoảng thời gian", r"⚠ Công suất không đổi thì mới dùng một công thức cho cả khoảng thời gian"),
  (r"“$3{,}0$ giờ”", r"$t=3{,}0\ \text{h}$", r"Thời gian hoạt động"),
  (r"“a) công … theo kWh và theo jun”", r"Cần $A$ (kWh) và $A$ (J)", r"Công và công suất liên hệ qua thời gian; kWh là đơn vị của công, $1\ \text{kWh}=3{,}6\cdot10^{6}\ \text{J}$"),
  (r"“b) bao nhiêu mã lực Pháp? $1\ \text{CV}=736\ \text{W}$”", r"$1\ \text{CV}=736\ \text{W}$; cần $P$ (CV)", r"⚠ Đổi hai đại lượng về cùng đơn vị (W) trước khi so"),
  (r"“c) máy bơm khác … $0{,}50$ kW … cùng công đó”", r"$P'=0{,}50\ \text{kW}$; $A'=A$", r"Cùng công thì thời gian phụ thuộc công suất"),
  (r"“phải hoạt động bao lâu”", r"Cần $t'$ (h)", r"Đại lượng cần tìm")],
 [(r"“Kéo đều một thùng hàng trượt trên sàn ngang”", r"Lực kéo không đổi", r"⚠ $A=Fd$ dùng khi lực không đổi và cùng hướng chuyển động"),
  (r"“lực kéo $120$ N”", r"$F_1=120\ \text{N}$", r"Lực sinh công"),
  (r"“đi được $15$ m trong $20$ s”", r"$d_1=15\ \text{m}$; $t_1=20\ \text{s}$", r"Công suất trung bình là công trong một đơn vị thời gian"),
  (r"“Tính công của lực kéo và công suất trung bình”", r"Cần $A_1$ (J) và $P_1$ (W)", r"Công của lực; công suất trung bình"),
  (r"“Nâng đều thùng hàng $24$ kg”", r"$m=24\ \text{kg}$", r"⚠ Nâng đều: gia tốc bằng không, hai lực tác dụng lên thùng cân bằng"),
  (r"“lên giá cao $1{,}5$ m trong $3{,}0$ s”", r"$h=1{,}5\ \text{m}$; $t_2=3{,}0\ \text{s}$", r"Quãng đường nâng là độ cao"),
  (r"“Lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"Trọng lượng của vật"),
  (r"“công suất trung bình của lực nâng”", r"Cần $P_2$ (W)", r"Đại lượng cần tìm")],
 [(r"“chạy trên đường thẳng nằm ngang”", r"Chuyển động thẳng", r"Lực cùng phương với độ dịch chuyển"),
  (r"“Lực kéo … luôn cùng hướng chuyển động”", r"$\vec F$ cùng hướng $\vec v$", r"⚠ $P=Fv$ chỉ dùng khi lực cùng hướng chuyển động"),
  (r"“a) chạy đều với tốc độ $36$ km/h, lực kéo $150$ N”", r"$v=36\ \text{km/h}$; $F=150\ \text{N}$", r"⚠ Vận tốc phải ở m/s thì tích $Fv$ mới ra W"),
  (r"“công suất tức thời”", r"Cần $P$ (kW)", r"Công suất tại đúng một lúc: $F$ và $v$ lúc đó"),
  (r"“b) giữ chạy đều … trong $5{,}0$ phút”", r"$t=5{,}0\ \text{phút}$", r"⚠ Chạy đều thì $F$, $v$ không đổi nên $P$ không đổi; $t$ tính bằng giây"),
  (r"“Tính công động cơ sinh ra”", r"Cần $A$ (kJ)", r"Công, công suất và thời gian liên hệ nhau"),
  (r"“c) tăng tốc … $54$ km/h … lực kéo là $120$ N”", r"$v'=54\ \text{km/h}$; $F'=120\ \text{N}$", r"Công suất tức thời dùng $F$ và $v$ tại đúng lúc xét, không dùng giá trị của lúc khác")],
 [(r"“động cơ công suất $22{,}5$ kW”", r"$P=22{,}5\ \text{kW}$", r"Công suất của động cơ"),
  (r"“Coi toàn bộ công suất của động cơ dùng để nâng”", r"Công suất động cơ = công suất nâng vật", r"⚠ Bỏ qua mọi hao phí; vận tốc lớn nhất ứng với công suất này"),
  (r"“nâng đều một kiện vật liệu khối lượng $750$ kg”", r"$m=750\ \text{kg}$", r"⚠ Nâng đều: gia tốc bằng không, hai lực tác dụng lên kiện cân bằng"),
  (r"“lên tầng cao $30$ m”", r"$h=30\ \text{m}$", r"Quãng đường nâng là độ cao"),
  (r"“Lấy $g=10$ m/s²”", r"$g=10\ \text{m/s}^2$", r"Trọng lượng của vật"),
  (r"“a) lực nâng của cáp”", r"Cần $F$ (N)", r"Đại lượng cần tìm"),
  (r"“b) vận tốc nâng đều lớn nhất”", r"Cần $v_{max}$ (m/s)", r"Công suất liên hệ lực và vận tốc"),
  (r"“c) thời gian ngắn nhất”", r"Cần $t_{min}$ (s)", r"Chuyển động đều: quãng đường, vận tốc, thời gian")],
 [(r"“ô tô tải khối lượng $4{,}5$ tấn”", r"$m=4{,}5\cdot10^{3}\ \text{kg}$", r"Trọng lượng $mg$"),
  (r"“công suất tối đa $36$ kW”", r"$P_{max}=36\ \text{kW}$", r"Công suất tối đa có hạn: $P=Fv$"),
  (r"“tổng lực cản $1800$ N, coi không đổi”", r"$F_c=1800\ \text{N}$", r"⚠ Chạy đều: lực kéo cân bằng với tổng lực cản"),
  (r"“a) chạy đều trên đường ngang với công suất tối đa”", r"Cần $v_1$ (m/s)", r"Công suất liên hệ lực kéo và vận tốc"),
  (r"“b) độ dốc $6\,\%$ (đi $100$ m theo mặt dốc thì lên cao $6$ m)”", r"$6\ \text{m}$ cao trên $100\ \text{m}$ theo mặt dốc", r"⚠ Trên dốc, trọng lực có thành phần dọc mặt dốc (phân tích lực)"),
  (r"“lực kéo … khi xe lên dốc đều”", r"Cần $F_2$ (N)", r"Chạy đều: tổng các lực dọc theo chuyển động bằng không"),
  (r"“c) lên dốc đều với công suất tối đa”", r"Cần $v_2$ (m/s)", r"Công suất liên hệ lực kéo và vận tốc"),
  (r"“d) đoạn dốc dài $500$ m”", r"$s=500\ \text{m}$; cần $t$ (s)", r"Chuyển động đều: quãng đường, vận tốc, thời gian")],
]

# ═════════════ Lời giải từng bước ═════════════
R1 = [r"<strong>Khái niệm:</strong> công suất là công sinh ra trong một đơn vị thời gian.",
      r"$P=\dfrac{A}{t}$, nên $A=Pt$.",
      r"$1\ \text{W}=1\ \text{J/s}$; $1\ \text{kW}=10^{3}\ \text{W}$; $1\ \text{CV}=736\ \text{W}$.",
      r"kWh là đơn vị của <strong>công</strong>: $1\ \text{kWh}=3{,}6\cdot10^{6}\ \text{J}$.",
      r"⚠ <strong>Điều kiện:</strong> công suất không đổi trong cả khoảng thời gian."]
R2 = [r"<strong>Khái niệm:</strong> công suất trung bình là công chia cho thời gian: $P=\dfrac{A}{t}$.",
      r"$A=Fd$ khi lực không đổi, cùng hướng độ dịch chuyển.",
      r"Nâng đều: lực nâng cân bằng trọng lực, $F=mg$.",
      r"⚠ <strong>Điều kiện:</strong> với $A=Fd$, lực không đổi và cùng hướng chuyển động."]
R3 = [r"<strong>Khái niệm:</strong> công suất tức thời là công suất tại đúng một lúc.",
      r"$P=Fv$ với $F$ và $v$ lấy tại lúc đó.",
      r"Đổi tốc độ: $\text{m/s}=\dfrac{\text{km/h}}{3{,}6}$; $1\ \text{phút}=60\ \text{s}$.",
      r"Chạy đều: $F$, $v$ không đổi nên $P$ không đổi, $A=Pt$.",
      r"⚠ <strong>Điều kiện:</strong> lực cùng hướng chuyển động; $v$ tính bằng m/s."]
R4 = [r"<strong>Khái niệm:</strong> công suất động cơ giới hạn $F$ và $v$ qua $P=Fv$.",
      r"Nâng đều: lực nâng cân bằng trọng lực, $F=mg$.",
      r"Vận tốc: $v=\dfrac{P}{F}$ ($P$ đổi ra W).",
      r"Chuyển động đều: $t=\dfrac{h}{v}$.",
      r"⚠ <strong>Điều kiện:</strong> toàn bộ công suất động cơ dùng để nâng vật."]
R5 = [r"<strong>Khái niệm:</strong> công suất tối đa có hạn, $P=Fv$ nên $F$ lớn thì $v$ nhỏ.",
      r"Chạy đều: tổng các lực dọc theo chuyển động bằng không, lực kéo bằng tổng lực cản.",
      r"Thành phần trọng lực dọc dốc: $F_d=mg\sin\alpha$, $\sin\alpha=\dfrac{\text{độ cao}}{\text{độ dài theo mặt dốc}}$.",
      r"Chuyển động đều: $t=\dfrac{s}{v}$.",
      r"⚠ <strong>Điều kiện:</strong> lực cản (ma sát, không khí) coi không đổi khi lên dốc."]

SOLS = [
 sol(R1, [
  (r"Công theo kWh", [P(r"Công suất không đổi nên $A=Pt$; kW nhân giờ ra kWh:"), M(r"A=Pt=2{,}0\cdot3{,}0"), A(r"A=6{,}0\ \text{kWh}")]),
  (r"Đổi sang jun", [P(r"$1\ \text{kWh}=3{,}6\cdot10^{6}\ \text{J}$:"), M(r"A=6{,}0\cdot3{,}6\cdot10^{6}"), A(r"A=2{,}16\cdot10^{7}\ \text{J}"),
                     P(r"Kiểm bằng đơn vị SI: $2000\ \text{W}\cdot10800\ \text{s}=2{,}16\cdot10^{7}\ \text{J}$ ✓.")]),
  (r"Đổi sang mã lực", [P(r"Đổi $2{,}0\ \text{kW}=2000\ \text{W}$ rồi chia cho $736\ \text{W/CV}$:"), M(r"P=\dfrac{2000}{736}"), A(r"P\approx2{,}72\ \text{CV}")]),
  (r"Máy bơm thứ hai", [P(r"Cùng công $A=6{,}0\ \text{kWh}$, công suất $P'=0{,}50\ \text{kW}$:"), M(r"t'=\dfrac{A}{P'}=\dfrac{6{,}0\ \text{kWh}}{0{,}50\ \text{kW}}"), A(r"t'=12\ \text{h}")]),
  (r"Kiểm tra", [M(r"P't'=0{,}50\cdot12=6{,}0\ \text{kWh}=A"), P(r"Khớp công đã tính ở ý a ✓.")])],
  [r"a) $A=6{,}0\ \text{kWh}=2{,}16\cdot10^{7}\ \text{J}$", r"b) $P\approx2{,}72\ \text{CV}$", r"c) $t'=12\ \text{h}$"],
  r"Nhận dạng: đề cho <strong>công suất và thời gian hoạt động</strong> → $A=Pt$; kWh là đơn vị công, đổi đơn vị trước khi so."),
 sol(R2, [
  (r"Công của lực kéo", [M(r"A_1=F_1d_1=120\cdot15"), A(r"A_1=1800\ \text{J}")]),
  (r"Công suất khi kéo", [M(r"P_1=\dfrac{A_1}{t_1}=\dfrac{1800}{20}"), A(r"P_1=90\ \text{W}")]),
  (r"Lực nâng", [P(r"Nâng đều nên $a=0$, lực nâng cân bằng trọng lực:"), M(r"F_2=mg=24\cdot10"), A(r"F_2=240\ \text{N}")]),
  (r"Công của lực nâng", [P(r"Thùng đi lên đúng bằng độ cao của giá:"), M(r"A_2=F_2h=240\cdot1{,}5"), A(r"A_2=360\ \text{J}")]),
  (r"Công suất khi nâng", [M(r"P_2=\dfrac{A_2}{t_2}=\dfrac{360}{3{,}0}"), A(r"P_2=120\ \text{W}")]),
  (r"Kiểm tra", [P(r"Dùng $P=Fv$ với vận tốc trung bình:"), M(r"P_1=F_1\cdot\dfrac{d_1}{t_1}=120\cdot0{,}75=90\ \text{W}"), M(r"P_2=F_2\cdot\dfrac{h}{t_2}=240\cdot0{,}50=120\ \text{W}"), P(r"Hai cách cho cùng kết quả ✓.")])],
  [r"a) $A_1=1800\ \text{J}$ · $P_1=90\ \text{W}$", r"b) $P_2=120\ \text{W}$"],
  r"Nhận dạng: đề cho <strong>lực, quãng đường và thời gian</strong> → $A=Fd$ rồi $P=A/t$; nâng đều thì lực nâng là $mg$."),
 sol(R3, [
  (r"Đổi tốc độ", [M(r"v=\dfrac{36}{3{,}6}"), A(r"v=10\ \text{m/s}")]),
  (r"Công suất tức thời khi chạy đều", [P(r"$F$ cùng hướng $v$:"), M(r"P=Fv=150\cdot10"), A(r"P=1500\ \text{W}=1{,}5\ \text{kW}")]),
  (r"Công trong 5,0 phút", [P(r"Chạy đều nên $P$ không đổi; đổi $t=5{,}0\ \text{phút}=300\ \text{s}$:"), M(r"A=Pt=1500\cdot300"), A(r"A=4{,}5\cdot10^{5}\ \text{J}=450\ \text{kJ}")]),
  (r"Công suất lúc tăng tốc", [P(r"Đổi tốc độ và dùng $F'$, $v'$ tại đúng lúc đó:"), M(r"v'=\dfrac{54}{3{,}6}=15\ \text{m/s}"), M(r"P'=F'v'=120\cdot15"), A(r"P'=1800\ \text{W}=1{,}8\ \text{kW}")]),
  (r"Kiểm tra", [P(r"Cách khác cho công: quãng đường $s=vt=10\cdot300=3000\ \text{m}$."), M(r"A=Fs=150\cdot3000=4{,}5\cdot10^{5}\ \text{J}"), P(r"Khớp ý b ✓.")])],
  [r"a) $P=1{,}5\ \text{kW}$", r"b) $A=450\ \text{kJ}$", r"c) $P'=1{,}8\ \text{kW}$"],
  r"Nhận dạng: đề cho <strong>lực kéo cùng hướng chuyển động và tốc độ km/h</strong> → đổi ra m/s rồi dùng $P=Fv$."),
 sol(R4, [
  (r"Lực nâng", [P(r"Nâng đều nên lực nâng cân bằng trọng lực:"), M(r"F=mg=750\cdot10"), A(r"F=7500\ \text{N}")]),
  (r"Vận tốc nâng lớn nhất", [P(r"Đổi $P=22{,}5\ \text{kW}=22500\ \text{W}$:"), M(r"v_{max}=\dfrac{P}{F}=\dfrac{22500}{7500}"), A(r"v_{max}=3{,}0\ \text{m/s}")]),
  (r"Thời gian ngắn nhất", [P(r"Nâng đều với vận tốc lớn nhất:"), M(r"t_{min}=\dfrac{h}{v_{max}}=\dfrac{30}{3{,}0}"), A(r"t_{min}=10\ \text{s}")]),
  (r"Kiểm tra", [P(r"Công cần để nâng kiện lên $30\ \text{m}$:"), M(r"A=mgh=750\cdot10\cdot30=225000\ \text{J}"), M(r"Pt_{min}=22500\cdot10=225000\ \text{J}"), P(r"Hai công bằng nhau ✓.")])],
  [r"a) $F=7500\ \text{N}$", r"b) $v_{max}=3{,}0\ \text{m/s}$", r"c) $t_{min}=10\ \text{s}$"],
  r"Nhận dạng: đề cho <strong>công suất động cơ</strong> và hỏi <strong>vận tốc lớn nhất hoặc thời gian ngắn nhất</strong> → $F=mg$, $v=P/F$, $t=h/v$."),
 sol(R5, [
  (r"Vận tốc trên đường ngang", [P(r"Chạy đều nên lực kéo bằng lực cản; đổi $P_{max}=36\ \text{kW}=36000\ \text{W}$:"), M(r"F_1=F_c=1800\ \text{N}"), M(r"v_1=\dfrac{P_{max}}{F_1}=\dfrac{36000}{1800}"), A(r"v_1=20\ \text{m/s}")]),
  (r"Lực kéo khi lên dốc đều", [P(r"Độ dốc: $\sin\alpha=\dfrac{6}{100}=0{,}06$; trọng lượng $mg=4500\cdot10=45000\ \text{N}$."), M(r"F_d=mg\sin\alpha=45000\cdot0{,}06=2700\ \text{N}"),
                              P(r"Lên dốc đều: lực kéo bằng lực cản cộng thành phần trọng lực dọc dốc:"), M(r"F_2=F_c+F_d=1800+2700"), A(r"F_2=4500\ \text{N}")]),
  (r"Vận tốc khi lên dốc", [P(r"Vẫn dùng công suất tối đa:"), M(r"v_2=\dfrac{P_{max}}{F_2}=\dfrac{36000}{4500}"), A(r"v_2=8{,}0\ \text{m/s}"), P(r"Đổi: $8{,}0\cdot3{,}6=28{,}8\ \text{km/h}$.")]),
  (r"Thời gian đi hết dốc", [P(r"Lên dốc đều với $v_2$:"), M(r"t=\dfrac{s}{v_2}=\dfrac{500}{8{,}0}"), A(r"t=62{,}5\ \text{s}")]),
  (r"Kiểm tra", [M(r"F_1v_1=1800\cdot20=36000\ \text{W},\quad F_2v_2=4500\cdot8{,}0=36000\ \text{W}"), P(r"Cả hai bằng $P_{max}$ ✓."), P(r"Lực kéo tăng $\dfrac{4500}{1800}=2{,}5$ lần nên vận tốc là $\dfrac{20}{2{,}5}=8{,}0\ \text{m/s}$ ✓.")])],
  [r"a) $v_1=20\ \text{m/s}$ ($72\ \text{km/h}$)", r"b) $F_2=4500\ \text{N}$", r"c) $v_2=8{,}0\ \text{m/s}$ ($28{,}8\ \text{km/h}$)", r"d) $t=62{,}5\ \text{s}$"],
  r"Nhận dạng: <strong>lên dốc đều với công suất tối đa</strong> → lực kéo = lực cản + thành phần trọng lực dọc dốc, rồi $v=P/F$."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>công suất và thời gian hoạt động</b> → nghĩ tới <b>A = P·t</b>, rồi đổi đơn vị.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Công theo kWh", r"Công do máy bơm sinh ra trong 3,0 giờ bằng bao nhiêu kWh?", 6.0, "kWh", 0.1,
       loi=r"Ghi kết quả bằng đơn vị công suất (kW) thay vì đơn vị công, hoặc đổi giờ sang giây rồi vẫn gọi là kWh."),
  buoc(r"Đổi sang jun", r"Công đó bằng bao nhiêu jun? (nhập hệ số a của kết quả a·10⁷)", 2.16, "×10⁷ J", 0.02,
       loi=r"Dùng $1\ \text{kWh}=3600\ \text{J}$ (nhầm với số giây trong một giờ) hoặc chỉ nhân với $1000$.",
       ke=[(r"Nhân công theo kWh với $3{,}6\cdot10^{6}\ \text{J/kWh}$", True),
           (r"Nhân với $3600$", r"$3600$ chỉ là số giây trong một giờ; $1\ \text{kWh}$ còn có hệ số $1000$ từ kW sang W."),
           (r"Nhân với $1000$", r"$1000$ chỉ đổi kW sang W; còn phải đổi giờ sang giây.")]),
  buoc(r"Đổi sang mã lực", r"Công suất 2,0 kW bằng bao nhiêu mã lực Pháp (CV)? Lấy 1 CV = 736 W.", 2.72, "CV", 0.02,
       loi=r"Nhân thay vì chia cho $736$, hoặc quên đổi $2{,}0\ \text{kW}$ ra W trước khi chia.",
       ke=[(r"Đổi $2{,}0\ \text{kW}$ ra W rồi chia cho $736\ \text{W/CV}$", True),
           (r"Nhân $2{,}0\ \text{kW}$ với $736$", r"Phép nhân với $736$ là đổi theo chiều ngược lại, từ CV sang W."),
           (r"Chia $2{,}0$ cho $736$ mà không đổi kW ra W", r"$736$ tính bằng W còn $2{,}0$ tính bằng kW; hai số phải cùng đơn vị mới chia được.")]),
  buoc(r"Máy bơm thứ hai", r"Máy 0,50 kW phải hoạt động bao lâu để sinh cùng công đó?", 12, "giờ", 0.2,
       loi=r"Lấy công suất chia cho công (đảo ngược), hoặc giữ nguyên thời gian cũ vì “cùng công”.",
       ke=[(r"$t'=A/P'$ với công theo kWh và công suất theo kW", True),
           (r"$t'=P'/A$", r"Từ $P=A/t$ suy ra $t=A/P$; công suất chia cho công không ra thời gian."),
           (r"Giữ $t'=3{,}0\ \text{h}$ vì cùng công", r"Cùng công nhưng công suất khác nhau thì thời gian sinh ra công đó khác nhau.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực, quãng đường và thời gian</b> → nghĩ tới <b>A = F·d</b> rồi <b>P = A/t</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Công của lực kéo", r"Công của lực kéo 120 N trên quãng đường 15 m bằng bao nhiêu?", 1800, "J", 10,
       loi=r"Chia quãng đường cho lực, hoặc nhân thêm cả thời gian $20\ \text{s}$."),
  buoc(r"Công suất khi kéo", r"Công suất trung bình khi kéo bằng bao nhiêu?", 90, "W", 1,
       loi=r"Nhân công với thời gian thay vì chia.",
       ke=[(r"Chia công cho thời gian $20\ \text{s}$", True),
           (r"Nhân công với $20\ \text{s}$", r"Nhân công với thời gian cho đại lượng khác; công suất là công trên mỗi giây nên phải chia."),
           (r"Chia công cho $15\ \text{m}$", r"Chia công cho quãng đường ra lực, không phải công suất.")]),
  buoc(r"Lực nâng", r"Thùng 24 kg được nâng đều. Lực nâng bằng bao nhiêu? (g = 10 m/s²)", 240, "N", 2,
       loi=r"Lấy lực nâng bằng khối lượng hoặc quên $g$; khối lượng đo bằng kg, lực đo bằng N.",
       ke=[(r"Nâng đều nên lực nâng cân bằng trọng lực, $F=mg$", True),
           (r"$F=m$, vì nâng thì lực nâng bằng khối lượng", r"Khối lượng (kg) và lực (N) khác nhau; trọng lực của vật là $mg$."),
           (r"$F=mgh$", r"$mgh$ là công (J), không phải lực.")]),
  buoc(r"Công của lực nâng", r"Công của lực nâng khi thùng lên cao 1,5 m bằng bao nhiêu?", 360, "J", 2,
       loi=r"Dùng quãng đường $15\ \text{m}$ của cảnh 1 hoặc lực kéo $120\ \text{N}$.",
       ke=[(r"Nhân lực nâng với độ cao nâng $1{,}5\ \text{m}$", True),
           (r"Nhân lực kéo $120\ \text{N}$ với $1{,}5\ \text{m}$", r"$120\ \text{N}$ là lực kéo ngang ở cảnh 1; ở cảnh 2 lực tác dụng lên thùng là lực nâng."),
           (r"Nhân lực nâng với $15\ \text{m}$", r"$15\ \text{m}$ là quãng đường ở cảnh 1; ở cảnh 2 thùng chỉ đi lên $1{,}5\ \text{m}$.")]),
  buoc(r"Công suất khi nâng", r"Công suất trung bình của lực nâng bằng bao nhiêu?", 120, "W", 1,
       loi=r"Chia công cho $20\ \text{s}$ của cảnh 1 thay vì thời gian nâng.",
       ke=[(r"Chia công của lực nâng cho thời gian nâng $3{,}0\ \text{s}$", True),
           (r"Chia công của lực nâng cho $20\ \text{s}$", r"$20\ \text{s}$ là thời gian kéo ở cảnh 1; công của lực nâng sinh ra trong $3{,}0\ \text{s}$."),
           (r"Nhân công với thời gian nâng", r"Công suất là công chia thời gian, không phải nhân.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực kéo cùng hướng chuyển động</b> và <b>tốc độ km/h</b> → nghĩ tới <b>P = F·v</b>, v đổi ra m/s.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(r"Đổi tốc độ", r"Tốc độ 36 km/h bằng bao nhiêu m/s?", 10, "m/s", 0.1,
       loi=r"Nhân với $3{,}6$ thay vì chia, hoặc đưa thẳng $36$ vào công thức."),
  buoc(r"Công suất tức thời khi chạy đều", r"Công suất tức thời của động cơ khi chạy đều bằng bao nhiêu kW?", 1.5, "kW", 0.02,
       loi=r"Nhân $150$ với $36$ mà chưa đổi km/h ra m/s, kết quả sai đơn vị.",
       ke=[(r"Nhân lực kéo với vận tốc đã đổi ra m/s", True),
           (r"Nhân lực kéo với $36\ \text{km/h}$", r"N nhân km/h không ra W; công suất tính bằng W khi $v$ tính bằng m/s."),
           (r"Chia lực kéo cho vận tốc", r"$F/v$ không phải công suất; công suất tức thời là $Fv$.")]),
  buoc(r"Công trong 5,0 phút", r"Công do động cơ sinh ra trong 5,0 phút chạy đều bằng bao nhiêu kJ?", 450, "kJ", 3,
       loi=r"Dùng $5{,}0$ thay cho $300\ \text{s}$ (quên đổi phút ra giây), hoặc quên đổi J ra kJ.",
       ke=[(r"$A=Pt$ với $t=300\ \text{s}$, vì chạy đều thì $P$ không đổi", True),
           (r"$A=Pt$ với $t=5{,}0$ (phút)", r"$P$ tính bằng W ($\text{J/s}$) nên $t$ phải tính bằng giây."),
           (r"$A=Fv$", r"$Fv$ là công suất, đơn vị W; muốn có công phải nhân thêm thời gian.")]),
  buoc(r"Công suất lúc tăng tốc", r"Khi tốc độ đạt 54 km/h với lực kéo 120 N, công suất tức thời bằng bao nhiêu kW?", 1.8, "kW", 0.02,
       loi=r"Dùng lại vận tốc $36\ \text{km/h}$ của ý a, hoặc cho rằng công suất vẫn như cũ.",
       ke=[(r"Dùng $F'$ và $v'$ tại đúng lúc đó, sau khi đổi $v'$ ra m/s", True),
           (r"Giữ công suất của ý a vì vẫn là một xe", r"Công suất tức thời đổi theo $F$ và $v$ tại từng lúc; xe tăng tốc thì $F$ và $v$ đã khác."),
           (r"Dùng $F'$ với $v=36\ \text{km/h}$ cũ", r"Vận tốc phải lấy tại đúng lúc xét, tức $v'$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>công suất động cơ</b> và <b>nâng đều</b> → nghĩ tới <b>F = mg</b>, <b>v = P/F</b>, <b>t = h/v</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Lực nâng", r"Nâng đều, lực nâng của cáp bằng bao nhiêu?", 7500, "N", 50,
       loi=r"Quên nhân với $g$: khối lượng tính bằng kg, lực tính bằng N."),
  buoc(r"Vận tốc nâng lớn nhất", r"Vận tốc nâng đều lớn nhất bằng bao nhiêu?", 3.0, "m/s", 0.05,
       loi=r"Để công suất ở đơn vị kW khi chia cho lực ở đơn vị N.",
       ke=[(r"$v=P/F$ với $P$ đổi ra W", True),
           (r"$v=F/P$", r"Đảo ngược; từ $P=Fv$ suy ra $v=P/F$."),
           (r"$v=h/t$", r"Chưa biết $t$, đó là điều phải tìm ở ý sau; vận tốc lớn nhất phải rút từ công suất.")]),
  buoc(r"Thời gian ngắn nhất", r"Thời gian ngắn nhất để nâng kiện lên 30 m bằng bao nhiêu?", 10, "s", 0.2,
       loi=r"Dùng vận tốc không phải vận tốc lớn nhất, hoặc chia công suất cho độ cao.",
       ke=[(r"$t=h/v$ với $v$ là vận tốc lớn nhất", True),
           (r"$t=P/h$", r"Công suất chia cho độ cao không ra thời gian; quãng đường chia vận tốc mới ra thời gian."),
           (r"$t=h/v$ với $v$ tuỳ ý", r"Thời gian ngắn nhất chỉ ứng với vận tốc lớn nhất.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lên dốc đều</b> → nghĩ tới <b>F = lực cản + trọng lực dọc dốc</b>, rồi <b>v = P/F</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Vận tốc trên đường ngang", r"Chạy đều trên đường ngang với công suất tối đa, vận tốc bằng bao nhiêu?", 20, "m/s", 0.2,
       loi=r"Quên đổi kW ra W, hoặc dùng khối lượng xe để tính lực kéo."),
  buoc(r"Lực kéo khi lên dốc đều", r"Lên dốc đều, lực kéo của động cơ bằng bao nhiêu?", 4500, "N", 30,
       loi=r"Chỉ tính lực cản trên đường ngang mà bỏ thành phần trọng lực dọc dốc, hoặc cộng cả trọng lượng của xe.",
       ke=[(r"Cộng lực cản với thành phần trọng lực dọc dốc", True),
           (r"Chỉ lấy lực cản trên đường ngang", r"Lên dốc, trọng lực có thành phần dọc mặt dốc kéo xe xuống; lực kéo phải thắng thêm phần đó."),
           (r"Cộng lực cản với cả trọng lượng $mg$", r"Chỉ thành phần của trọng lực dọc mặt dốc ($mg\sin\alpha$) cản xe; phần vuông góc mặt dốc đã được mặt đường cân bằng.")]),
  buoc(r"Vận tốc khi lên dốc", r"Lên dốc đều với công suất tối đa, vận tốc bằng bao nhiêu?", 8.0, "m/s", 0.1,
       loi=r"Dùng lực cản trên đường ngang để tính vận tốc, hoặc quên đổi kW ra W.",
       ke=[(r"$v=P/F$ với $F$ là lực kéo khi lên dốc", True),
           (r"$v=P/F_c$ với $F_c$ là lực cản trên đường ngang", r"Lực kéo khi lên dốc khác lực cản trên đường ngang; phải dùng lực kéo ở bước trước."),
           (r"Giữ nguyên vận tốc trên đường ngang vì công suất vẫn là tối đa", r"Công suất không đổi nhưng lực kéo đổi thì vận tốc đổi theo, $v=P/F$.")]),
  buoc(r"Thời gian đi hết dốc", r"Đi hết đoạn dốc dài 500 m mất bao nhiêu giây?", 62.5, "s", 0.5,
       loi=r"Dùng vận tốc trên đường ngang, hoặc đảo ngược tỉ số quãng đường và vận tốc.",
       ke=[(r"$t=s/v$ với $v$ của đoạn lên dốc", True),
           (r"$t=s/v$ với $v$ trên đường ngang", r"Trên dốc xe chạy với vận tốc khác; phải dùng vận tốc lên dốc."),
           (r"$t=v/s$", r"Đảo ngược; thời gian bằng quãng đường chia vận tốc.")]),
  buoc("Kiểm tra")]),
]

write(J, 69, "Bài 24. Công suất", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
