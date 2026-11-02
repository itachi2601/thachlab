"""Bài tập mẫu bài 48 — Bài 3. Đơn vị và sai số trong vật lí (Lớp 10). 3 dạng, dễ → khó.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-48.py  → ghi scripts/data/bai-tap-mau/48.json (review.checked=false)
Chủ đề ngân hàng: 'Sai số tuyệt đối, sai số tỉ đối' + 'Ghi kết quả đo và chữ số có nghĩa'."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "48.json")
VB = "0 0 420 200"
NOTE = "Hình minh hoạ, không theo tỉ lệ."
TOPIC = "Sai số tuyệt đối, sai số tỉ đối"
MUTE = "#94a3b8"

# ───────────── Dạng 1: cân viên bi, 4 lần đo trực tiếp ─────────────
M1 = [5.38, 5.42, 5.38, 5.42]; DC1 = 0.01
mean1 = sum(M1) / 4
di = [abs(mean1 - x) for x in M1]
dmean = sum(di) / 4
dA1 = dmean + DC1
assert abs(mean1 - 5.40) < 1e-9 and all(abs(a - b) < 1e-9 for a, b in zip(di, [0.02] * 4))
assert abs(dmean - 0.02) < 1e-9 and abs(dA1 - 0.03) < 1e-9 and max(di) < dA1
d1pct = dA1 / mean1 * 100
assert abs(d1pct - 0.5556) < 0.001                       # 0,56 %

# ───────────── Dạng 2: tốc độ v = s/t (đo gián tiếp, nhân chia) ─────────────
S2, DS2, T2, DT2 = 2.50, 0.01, 4.2, 0.1
ds_pct, dt_pct = DS2 / S2 * 100, DT2 / T2 * 100
dv_pct = ds_pct + dt_pct
v2 = S2 / T2; dv2 = v2 * dv_pct / 100
assert abs(ds_pct - 0.4) < 1e-9 and abs(dt_pct - 2.381) < 0.001 and abs(dv_pct - 2.781) < 0.001
assert abs(v2 - 0.5952) < 0.0001 and abs(dv2 - 0.01655) < 0.00005
assert round(dv2, 3) == 0.017 and round(v2, 3) == 0.595   # (0,595 ± 0,017) m/s

# ───────────── Dạng 3: gia tốc a = 2s/t² (số mũ), 5 lần đo t ─────────────
S3, DS3 = 1.20, 0.01
T3 = [1.54, 1.48, 1.48, 1.51, 1.49]; DC3 = 0.01
t3 = sum(T3) / 5
d3 = [abs(t3 - x) for x in T3]
dt3 = sum(d3) / 5 + DC3
assert abs(t3 - 1.50) < 1e-9 and abs(sum(d3) / 5 - 0.02) < 1e-9 and abs(dt3 - 0.03) < 1e-9 and max(d3) > dt3
dtp = dt3 / t3 * 100; dsp = DS3 / S3 * 100
assert abs(dtp - 2.0) < 1e-9 and abs(dsp - 0.8333) < 0.001
a3 = 2 * S3 / t3 ** 2; da_pct = dsp + 2 * dtp; da3 = a3 * da_pct / 100
assert abs(a3 - 1.0667) < 0.0001 and abs(da_pct - 4.8333) < 0.001 and abs(da3 - 0.05156) < 0.0002
assert round(da3, 2) == 0.05 and round(a3, 2) == 1.07     # a = (1,07 ± 0,05) m/s²
assert 2 * dtp > dsp                                      # sai số thời gian đóng góp nhiều hơn

# ───────────── hình ─────────────
def strip(k):
    X = lambda v: 60 + (v - 5.36) / 0.08 * 300
    b = seg(50, 110, 380, 110, "currentColor", 2) + chevron(380, 110, 1, 0, "currentColor", 2)
    for v in (5.36, 5.38, 5.40, 5.42, 5.44):
        b += seg(X(v), 104, X(v), 116, "currentColor", 1.6) + lbl(X(v), 134, f"{v:.2f}".replace(".", ","), "currentColor", 12, "middle", "600")
    b += lbl(380, 160, "số chỉ cân (g)", "currentColor", 12, "end", "400")
    if k == 0:
        for i, v in enumerate(M1):
            b += dot(X(v), 110, 5, ORG)
        b += ball([(X(v), 110) for v in (5.38, 5.42, 5.40, 5.40)], 0, 0.8)
        return fig("d1-0", VB, "Bốn số chỉ của cân điện tử trên trục số, từ 5,38 g đến 5,42 g", b,
                   "Mô phỏng: chấm xanh đi qua bốn số chỉ lần lượt. " + NOTE)
    b += lbl(210, 66, "bốn lần đo tản quanh một giá trị", MUTE, 12, "middle", "400")
    for v in M1:
        b += dot(X(v), 110, 5, ORG)
    return fig("d1-2", VB, "Bốn số chỉ của cân điện tử trên trục số", b, "Dữ kiện: bốn số chỉ trong đề. " + NOTE)

def ray(k):
    b = seg(40, 130, 380, 130, "currentColor", 2) + seg(50, 124, 50, 136, "currentColor", 2) + seg(370, 124, 370, 136, "currentColor", 2)
    car = ('<rect x="30" y="108" width="40" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="2"/>'
           '<circle cx="40" cy="127" r="4.5" fill="currentColor"/><circle cx="60" cy="127" r="4.5" fill="currentColor"/>')
    b += dim("", "o", 50, 80, 370, 80, "s = 2,50 m", 210, 70, "middle")
    if k == 0:
        b += f'<g>{car}<animateTransform attributeName="transform" type="translate" values="0 0;320 0" dur="2.6s" begin="indefinite" fill="freeze"/></g>'
        b += lbl(210, 168, "t = 4,2 s (đồng hồ bấm tay)", ORG, 13, "middle", "700")
        return fig("d2-0", VB, "Xe lăn chạy hết đường ray dài 2,50 m", b, "Mô phỏng: xe chạy đều qua đường ray 2,50 m. " + NOTE)
    b += car + lbl(210, 168, "v = ? (tính từ s và t)", RED, 14, "middle", "700")
    return fig("d2-2", VB, "Xe lăn và đường ray cần đo tốc độ", b, "Dữ kiện: s và t đo trực tiếp. " + NOTE)

def slope(k):
    x0, y0, x1, y1 = 60, 150, 360, 70
    b = seg(x0, y0, x1, y1, "currentColor", 2.5) + seg(x0, y0, x1, y0, MUTE, 1.5, "5 4")
    b += dim("", "o", x0 - 8, y0 - 14, x1 - 8, y1 - 14, "s = 1,20 m", 190, 92, "middle")
    if k == 0:
        pts = []
        for i in range(26):
            f = (i / 25) ** 2                           # x = ½ a t²: tỉ lệ t²
            pts.append((x1 + (x0 - x1) * f, y1 + (y0 - y1) * f - 8))
        b += ball(pts, 0, 0.06)
        b += lbl(300, 170, "t ≈ 1,50 s", ORG, 13, "middle", "700")
        return fig("d3-0", VB, "Vật trượt từ nghỉ xuống mặt phẳng nghiêng dài 1,20 m, chuyển động nhanh dần", b,
                   "Mô phỏng: vật chuyển động nhanh dần đều từ nghỉ, quãng đường tỉ lệ với t². " + NOTE)
    b += lbl(300, 170, "a = ? (từ s và t)", RED, 14, "middle", "700")
    return fig("d3-2", VB, "Mặt phẳng nghiêng dài 1,20 m, đo thời gian trượt", b, "Dữ kiện: s đo một lần, t đo năm lần. " + NOTE)

BUILD = [strip, ray, slope]

# ───────────── đề ─────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Đo trực tiếp nhiều lần: trung bình, sai số tuyệt đối, tỉ đối, ghi kết quả", topic=TOPIC,
      problem_html=(r"<p>Một viên bi thép được cân bốn lần bằng cân điện tử có độ chia nhỏ nhất $0{,}01\ \text{g}$ (sai số dụng cụ lấy bằng một độ chia nhỏ nhất), "
                    r"số chỉ lần lượt: $5{,}38\ \text{g}$; $5{,}42\ \text{g}$; $5{,}38\ \text{g}$; $5{,}42\ \text{g}$.</p>"
                    r"<p>a) Tính giá trị trung bình $\overline{m}$. b) Tính sai số tuyệt đối $\Delta m$ của phép đo. "
                    r"c) Tính sai số tỉ đối $\delta m$. d) Ghi kết quả đo.</p>")),
 dict(label="Dạng 2 · Trung bình · Đo gián tiếp (nhân, chia): cộng sai số tỉ đối rồi ghi kết quả", topic=TOPIC,
      problem_html=(r"<p>Một xe lăn chạy hết đường ray, quãng đường đo bằng thước cuộn được $s = (2{,}50 \pm 0{,}01)\ \text{m}$; thời gian đo bằng đồng hồ bấm tay được "
                    r"$t = (4{,}2 \pm 0{,}1)\ \text{s}$. Tốc độ trung bình của xe được tính bằng $v = \dfrac{s}{t}$.</p>"
                    r"<p>a) Tính $\delta s$ và $\delta t$. b) Tính sai số tỉ đối $\delta v$. c) Tính $\overline{v}$ và sai số tuyệt đối $\Delta v$, rồi ghi kết quả "
                    r"$v = \overline{v} \pm \Delta v$ với đúng chữ số có nghĩa.</p>")),
 dict(label="Dạng 3 · Khó · Gián tiếp có số mũ: gộp phép đo nhiều lần với phép đo một lần, tìm nguồn sai số lớn nhất", topic=TOPIC,
      problem_html=(r"<p>Một vật trượt không vận tốc đầu trên mặt phẳng nghiêng dài $s = (1{,}20 \pm 0{,}01)\ \text{m}$. Thời gian trượt $t$ đo năm lần bằng đồng hồ số "
                    r"(độ chia nhỏ nhất $0{,}01\ \text{s}$, sai số dụng cụ lấy bằng một độ chia): $1{,}54\ \text{s}$; $1{,}48\ \text{s}$; $1{,}48\ \text{s}$; $1{,}51\ \text{s}$; $1{,}49\ \text{s}$. "
                    r"Gia tốc tính theo $a = \dfrac{2s}{t^{2}}$.</p>"
                    r"<p>a) Tính $\overline{t}$ và $\Delta t$ của phép đo thời gian. b) Tính $\delta s$, $\delta t$ rồi $\delta a$. "
                    r"c) Tính $\overline{a}$, $\Delta a$ và ghi kết quả $a = \overline{a} \pm \Delta a$ đúng chữ số có nghĩa. "
                    r"d) Đại lượng nào đóng góp nhiều nhất vào $\delta a$?</p>")),
]

# ───────────── bảng phân tích đề ─────────────
ANALYSIS = [
 [("\"cân bốn lần ... $5{,}38$; $5{,}42$; $5{,}38$; $5{,}42$\"", "Bốn số đo cùng đơn vị g", r"Giá trị trung bình của $n$ lần đo tính thế nào?"),
  ("\"độ chia nhỏ nhất $0{,}01\\ \\text{g}$ (sai số dụng cụ ... một độ chia)\"", "$\\Delta m_{\\text{dc}} = 0{,}01\\ \\text{g}$",
   r"⚠ Sai số tuyệt đối gồm hai phần: phần nào từ dao động giữa các lần đo, phần nào từ dụng cụ?"),
  ("\"sai số tuyệt đối $\\Delta m$\"", "Cần tìm $\\Delta m$", r"Độ lệch từng lần $|\overline{m} - m_i|$ rồi lấy trung bình, cộng sai số dụng cụ."),
  ("\"sai số tỉ đối $\\delta m$ ... ghi kết quả\"", "$\\delta = \\dfrac{\\Delta m}{\\overline{m}}$", r"Cần ghi cả sai số tỉ đối và khoảng $\overline{m} \pm \Delta m$ với đúng chữ số có nghĩa.")],
 [("\"$s = (2{,}50 \\pm 0{,}01)\\ \\text{m}$\"", "$\\Delta s = 0{,}01\\ \\text{m}$", r"Sai số tỉ đối của $s$ tính thế nào?"),
  ("\"$t = (4{,}2 \\pm 0{,}1)\\ \\text{s}$\"", "$\\Delta t = 0{,}1\\ \\text{s}$", r"Sai số tỉ đối của $t$ tính thế nào?"),
  ("\"$v = \\dfrac{s}{t}$\"", "Một thương", r"⚠ Phép chia thì cộng sai số tuyệt đối hay sai số tỉ đối?"),
  ("\"ghi kết quả ... đúng chữ số có nghĩa\"", "Cần $\\overline{v}$ và $\\Delta v$", r"$\Delta v$ giữ mấy chữ số có nghĩa? $\overline{v}$ lấy đến chữ số thập phân nào?")],
 [("\"$s = (1{,}20 \\pm 0{,}01)\\ \\text{m}$\"", "$\\Delta s = 0{,}01\\ \\text{m}$", r"Đo một lần: sai số tuyệt đối là bao nhiêu và $\delta s$ tính thế nào?"),
  ("\"đo năm lần ... đồng hồ số\"", "Năm số đo $t$", r"⚠ Đo nhiều lần: $\Delta t$ gồm trung bình các độ lệch cộng sai số dụng cụ."),
  ("\"$a = \\dfrac{2s}{t^{2}}$\"", "Có tỉ số và số mũ 2", r"$t$ có số mũ 2 thì $\delta t$ vào $\delta a$ với hệ số bao nhiêu? Số $2$ có sai số không?"),
  ("\"đại lượng nào đóng góp nhiều nhất\"", "So hai thành phần của $\\delta a$", r"So $\delta s$ với phần đóng góp của $t$ trong tổng.")],
]

# ───────────── lời giải ─────────────
R1 = [r"<strong>Trung bình:</strong> $\overline{A} = \dfrac{A_1 + \dots + A_n}{n}$; <strong>độ lệch từng lần:</strong> $\Delta A_i = |\overline{A} - A_i|$.",
      r"<strong>Sai số tuyệt đối:</strong> $\Delta A = \overline{\Delta A} + \Delta A_{\text{dc}}$.",
      r"<strong>Sai số tỉ đối:</strong> $\delta A = \dfrac{\Delta A}{\overline{A}} \cdot 100\,\%$.",
      r"⚠ <strong>Điều kiện:</strong> $\Delta A$ viết 1–2 chữ số có nghĩa; $\overline{A}$ viết cùng bậc thập phân với $\Delta A$."]
R2 = [r"<strong>Tỉ đối của từng đại lượng:</strong> $\delta X = \dfrac{\Delta X}{\overline{X}} \cdot 100\,\%$.",
      r"<strong>Nhân, chia:</strong> $\delta A = \delta X + \delta Y + \delta Z$ (chia cũng cộng).",
      r"<strong>Sai số tuyệt đối:</strong> $\Delta A = \overline{A} \cdot \dfrac{\delta A}{100\,\%}$.",
      r"⚠ <strong>Điều kiện:</strong> $\Delta A$ giữ 2 chữ số có nghĩa nếu chữ số đầu là $1$ hoặc $2$, còn lại giữ $1$."]
R3 = [r"<strong>Đo nhiều lần:</strong> $\Delta t = \overline{\Delta t} + \Delta t_{\text{dc}}$.",
      r"<strong>Số mũ:</strong> $A = X^{n}\dfrac{Y^{m}}{Z^{k}}$ thì $\delta A = n\,\delta X + m\,\delta Y + k\,\delta Z$.",
      r"<strong>Hệ số $2$:</strong> hằng số chính xác nên không đóng góp vào sai số.",
      r"⚠ <strong>Điều kiện:</strong> chỉ cộng các $\delta$ khi các phép đo độc lập; giữ chữ số có nghĩa theo $\Delta a$."]

SOLS = [
 sol(R1, [
  ("Giá trị trung bình", [P(r"Cộng bốn số chỉ rồi chia cho $4$:"), M(r"\overline{m} = \dfrac{5{,}38 + 5{,}42 + 5{,}38 + 5{,}42}{4} = \dfrac{21{,}60}{4}"), A(r"5{,}40\ \text{g}")]),
  ("Sai số tuyệt đối", [P(r"Độ lệch mỗi lần đều bằng $0{,}02\ \text{g}$. Trung bình các độ lệch:"), M(r"\overline{\Delta m} = \dfrac{4 \cdot 0{,}02}{4} = 0{,}02\ \text{g}"),
                       P(r"Cộng sai số dụng cụ:"), M(r"\Delta m = 0{,}02 + 0{,}01"), A(r"0{,}03\ \text{g}")]),
  ("Sai số tỉ đối", [M(r"\delta m = \dfrac{0{,}03}{5{,}40} \cdot 100\,\% \approx 0{,}56\,\%"), A(r"0{,}56\,\%")]),
  ("Ghi kết quả", [P(r"$\Delta m = 0{,}03\ \text{g}$ (1 chữ số có nghĩa), dừng ở chữ số thập phân thứ hai nên $\overline{m}$ cũng lấy hai chữ số thập phân:"),
                   A(r"m = (5{,}40 \pm 0{,}03)\ \text{g}")])],
  [r"a) $5{,}40\ \text{g}$", r"b) $0{,}03\ \text{g}$", r"c) $\approx 0{,}56\,\%$", r"d) $m = (5{,}40 \pm 0{,}03)\ \text{g}$"],
  r"Nhận dạng: đề cho <strong>nhiều lần đo cùng một đại lượng</strong> → trung bình, độ lệch từng lần, cộng sai số dụng cụ, rồi $\delta$ và cách ghi."),
 sol(R2, [
  ("Sai số tỉ đối của s và t", [P(r"Áp dụng $\delta X = \dfrac{\Delta X}{\overline{X}}$:"), M(r"\delta s = \dfrac{0{,}01}{2{,}50} \cdot 100\,\% = 0{,}4\,\%"), M(r"\delta t = \dfrac{0{,}1}{4{,}2} \cdot 100\,\% \approx 2{,}38\,\%"),
                               A(r"\delta s = 0{,}4\,\%;\ \delta t \approx 2{,}38\,\%")]),
  ("Sai số tỉ đối của v", [P(r"$v = \dfrac{s}{t}$ là phép chia, cộng sai số tỉ đối:"), M(r"\delta v = \delta s + \delta t = 0{,}4 + 2{,}38"), A(r"\delta v \approx 2{,}78\,\%")]),
  ("Giá trị và sai số tuyệt đối", [M(r"\overline{v} = \dfrac{2{,}50}{4{,}2} \approx 0{,}595\ \text{m/s}"), M(r"\Delta v = \overline{v} \cdot \dfrac{\delta v}{100\,\%} = 0{,}595 \cdot 0{,}0278 \approx 0{,}0166\ \text{m/s}"),
                                  A(r"\Delta v \approx 0{,}017\ \text{m/s}")]),
  ("Ghi kết quả", [P(r"Chữ số đầu của $\Delta v$ là $1$, nên giữ hai chữ số có nghĩa: $0{,}017$. $\overline{v}$ lấy đến chữ số thập phân thứ ba:"), A(r"v = (0{,}595 \pm 0{,}017)\ \text{m/s}")])],
  [r"a) $\delta s = 0{,}4\,\%$; $\delta t \approx 2{,}38\,\%$", r"b) $\delta v \approx 2{,}78\,\%$", r"c) $v = (0{,}595 \pm 0{,}017)\ \text{m/s}$"],
  r"Nhận dạng: đề cho <strong>kết quả dạng $X \pm \Delta X$ và công thức nhân chia</strong> → đổi sang $\delta$, cộng lại, đổi ngược về $\Delta$."),
 sol(R3, [
  ("Trung bình và sai số của t", [P(r"Giá trị trung bình:"), M(r"\overline{t} = \dfrac{1{,}54 + 1{,}48 + 1{,}48 + 1{,}51 + 1{,}49}{5} = \dfrac{7{,}50}{5} = 1{,}50\ \text{s}"),
                                 P(r"Độ lệch từng lần: $0{,}04;\ 0{,}02;\ 0{,}02;\ 0{,}01;\ 0{,}01\ \text{s}$. Trung bình độ lệch: $\dfrac{0{,}10}{5} = 0{,}02\ \text{s}$."),
                                 M(r"\Delta t = 0{,}02 + 0{,}01"), A(r"0{,}03\ \text{s}")]),
  ("Sai số tỉ đối của s, t", [M(r"\delta s = \dfrac{0{,}01}{1{,}20} \cdot 100\,\% \approx 0{,}83\,\%"), M(r"\delta t = \dfrac{0{,}03}{1{,}50} \cdot 100\,\% = 2{,}0\,\%"), A(r"\delta s \approx 0{,}83\,\%;\ \delta t = 2{,}0\,\%")]),
  ("Sai số tỉ đối của a", [P(r"$t$ có số mũ $2$; hệ số $2$ là hằng số chính xác:"), M(r"\delta a = \delta s + 2\,\delta t = 0{,}83 + 2 \cdot 2{,}0"), A(r"\delta a \approx 4{,}8\,\%")]),
  ("Giá trị và sai số tuyệt đối của a", [M(r"\overline{a} = \dfrac{2 \cdot 1{,}20}{1{,}50^{2}} \approx 1{,}07\ \text{m/s}^2"), M(r"\Delta a = 1{,}067 \cdot 0{,}048 \approx 0{,}051\ \text{m/s}^2"),
                                       P(r"Chữ số đầu của $\Delta a$ là $5$: giữ một chữ số có nghĩa, $0{,}05$; $\overline{a}$ lấy hai chữ số thập phân:"), A(r"a = (1{,}07 \pm 0{,}05)\ \text{m/s}^2")]),
  ("Nguồn sai số lớn nhất", [P(r"Phần đóng góp của $t$ là $2\,\delta t = 4{,}0\,\%$; của $s$ chỉ $0{,}83\,\%$."), A(r"T:Thời gian $t$ đóng góp nhiều nhất: muốn giảm sai số cần cải thiện phép đo thời gian.")])],
  [r"a) $\overline{t} = 1{,}50\ \text{s}$; $\Delta t = 0{,}03\ \text{s}$", r"b) $\delta s \approx 0{,}83\,\%$; $\delta t = 2{,}0\,\%$; $\delta a \approx 4{,}8\,\%$", r"c) $a = (1{,}07 \pm 0{,}05)\ \text{m/s}^2$", r"d) Thời gian $t$"],
  r"Nhận dạng: đề <strong>trộn phép đo nhiều lần, đo một lần, có số mũ</strong> → tính $\Delta$ từng đại lượng, đổi sang $\delta$, nhân số mũ rồi cộng."),
]

# ───────────── tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>nhiều lần đo cùng một đại lượng</b> → <b>trung bình, độ lệch, cộng sai số dụng cụ</b>, rồi tỉ đối",
      cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Giá trị trung bình", "Giá trị trung bình của bốn số chỉ là bao nhiêu gam?", dap_so=5.40, don_vi="g", sai_so=0.005,
       loi=r"Lấy số chỉ giữa danh sách, hoặc chia tổng cho 5 thay vì cho số lần đo."),
  buoc("Sai số tuyệt đối", "Sai số tuyệt đối $\\Delta m$ của phép đo là bao nhiêu gam?", dap_so=0.03, don_vi="g", sai_so=0.005,
       loi=r"Quên cộng sai số dụng cụ, hoặc nhầm khi lấy trung bình các độ lệch.",
       ke=[(r"Lấy trung bình các độ lệch rồi cộng sai số dụng cụ", True),
           (r"Chỉ lấy độ lệch của một lần đo", r"Phải lấy trung bình các độ lệch của mọi lần, rồi cộng sai số dụng cụ."),
           (r"Chỉ lấy sai số dụng cụ", r"Bốn lần đo không trùng nhau nên còn phần sai số do sự tản của các lần đo.")]),
  buoc("Sai số tỉ đối", "Sai số tỉ đối $\\delta m$ gần bằng bao nhiêu phần trăm?", dap_so=0.56, don_vi="%", sai_so=0.02,
       loi=r"Chia $\Delta m$ cho $0{,}01$ hoặc quên nhân $100\,\%$."),
  buoc("Ghi kết quả", "Cách ghi nào đúng?", loi=r"Giữ nhiều chữ số thập phân hơn sai số cho phép, hoặc ghi thiếu sai số.",
       lua_chon=[(r"$m = (5{,}40 \pm 0{,}03)\ \text{g}$", True), (r"$m = (5{,}4 \pm 0{,}03)\ \text{g}$", r"Giá trị trung bình phải có cùng số chữ số thập phân với sai số: hai chữ số thập phân."),
                 (r"$m = (5{,}400 \pm 0{,}03)\ \text{g}$", r"Ba chữ số thập phân nhiều hơn sai số cho phép; sai số dừng ở hai chữ số thập phân.")])]),
 dict(nhan_dang=r"Thấy <b>kết quả dạng X ± ΔX và công thức nhân chia</b> → đổi sang <b>sai số tỉ đối</b>, cộng, rồi đổi ngược",
      cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Sai số tỉ đối của thời gian", "Sai số tỉ đối $\\delta t$ của thời gian là bao nhiêu phần trăm?", dap_so=2.38, don_vi="%", sai_so=0.03,
       loi=r"Lấy $0{,}1\ \text{s}$ làm sai số tỉ đối, hoặc chia cho quãng đường."),
  buoc("Sai số tỉ đối của tốc độ", "Với $v = s/t$ thì $\\delta v$ là bao nhiêu phần trăm?", dap_so=2.78, don_vi="%", sai_so=0.05,
       loi=r"Trừ hai sai số tỉ đối vì thấy phép chia, hoặc cộng sai số tuyệt đối.",
       lua_chon=[(r"$\delta v = \delta s + \delta t$", True), (r"$\delta v = \delta s - \delta t$", r"Phép chia cũng cộng sai số tỉ đối, không trừ."),
                 (r"$\delta v = \Delta s + \Delta t$", r"Cộng các sai số tỉ đối, không cộng sai số tuyệt đối khác đơn vị.")],
       ke=[(r"Cộng sai số tỉ đối của $s$ và của $t$", True),
           (r"Trừ sai số tỉ đối của $t$ khỏi của $s$", r"Chia hay nhân đều cộng sai số tỉ đối; trừ làm đánh giá thiếu sai số."),
           (r"Cộng $0{,}01$ và $0{,}1$ rồi chia cho $\overline{v}$", r"$\Delta s$ và $\Delta t$ khác đơn vị nên không cộng trực tiếp được.")]),
  buoc("Sai số tuyệt đối của tốc độ", "Sai số tuyệt đối $\\Delta v$ gần bằng bao nhiêu m/s?", dap_so=0.017, don_vi="m/s", sai_so=0.001,
       loi=r"Dùng $\delta v$ đang tính bằng phần trăm mà chưa đổi ra số thập phân, hoặc quên nhân với $\overline{v}$."),
  buoc("Ghi kết quả", "Kết quả $v$ ghi đúng chữ số có nghĩa là gì?", loi=r"Làm tròn $\Delta v$ và $\overline{v}$ theo cùng một cách cho gọn.",
       lua_chon=[(r"$v = (0{,}595 \pm 0{,}017)\ \text{m/s}$", True), (r"$v = (0{,}60 \pm 0{,}02)\ \text{m/s}$", r"Chữ số đầu của $\Delta v$ là 1 nên giữ hai chữ số có nghĩa: $0{,}017$."),
                 (r"$v = (0{,}5952 \pm 0{,}017)\ \text{m/s}$", r"$\overline{v}$ phải dừng ở cùng chữ số thập phân với $\Delta v$.")],
       ke=[(r"Làm tròn $\Delta v$ trước, rồi làm tròn $\overline{v}$ cùng chữ số thập phân", True),
           (r"Làm tròn $\overline{v}$ tới một chữ số có nghĩa", r"Số chữ số của $\overline{v}$ do $\Delta v$ quyết định, không do tuỳ ý."),
           (r"Giữ nguyên mọi chữ số máy tính cho", r"Máy tính cho nhiều chữ số hơn dụng cụ đo đã cho phép.")])]),
 dict(nhan_dang=r"Thấy <b>phép đo trộn nhiều lần, một lần, có số mũ</b> → tính <b>Δ</b>, đổi sang <b>δ</b>, nhân số mũ, cộng",
      cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Sai số tuyệt đối của thời gian", "Sai số tuyệt đối $\\Delta t$ của phép đo thời gian là bao nhiêu giây?", dap_so=0.03, don_vi="s", sai_so=0.005,
       loi=r"Quên cộng sai số dụng cụ, hoặc lấy độ lệch lớn nhất làm sai số."),
  buoc("Sai số tỉ đối của t", "Sai số tỉ đối $\\delta t$ của thời gian là bao nhiêu phần trăm?", dap_so=2.0, don_vi="%", sai_so=0.05,
       loi=r"Chia $\Delta t$ cho $\overline{t}$ nhưng quên nhân $100\,\%$, hoặc chia cho quãng đường.",
       lua_chon=[(r"$\delta t = \dfrac{\Delta t}{\overline{t}} \cdot 100\,\%$", True), (r"$\delta t = \dfrac{\Delta t}{s} \cdot 100\,\%$", r"Sai số tỉ đối chia cho chính giá trị trung bình của đại lượng đó, không chia cho đại lượng khác."),
                 (r"$\delta t = \Delta t \cdot \overline{t}$", r"Sai số tỉ đối là một thương, không phải một tích.")],
       ke=[(r"Chia $\Delta t$ cho $\overline{t}$ rồi nhân $100\,\%$", True),
           (r"Lấy $\Delta t$ chia cho quãng đường rồi nhân $100\,\%$", r"Hai đại lượng khác nhau, khác đơn vị: phải chia cho giá trị trung bình của chính đại lượng đó."),
           (r"Lấy $\Delta t$ nhân $100\,\%$", r"Thiếu phép chia cho giá trị đo: không có ý nghĩa mức độ chính xác.")]),
  buoc("Sai số tỉ đối của a", "Sai số tỉ đối $\\delta a$ của gia tốc là bao nhiêu phần trăm?", dap_so=4.8, don_vi="%", sai_so=0.1,
       loi=r"Quên số mũ 2 của $t$, hoặc cộng thêm sai số cho hệ số $2$ trong công thức.",
       lua_chon=[(r"$\delta a = \delta s + 2\,\delta t$", True), (r"$\delta a = \delta s + \delta t$", r"$t$ có số mũ $2$ nên $\delta t$ được nhân với $2$."),
                 (r"$\delta a = 2\,\delta s + 2\,\delta t$", r"Hệ số $2$ trong tử là hằng số chính xác, không đóng góp sai số.")],
       ke=[(r"Cộng $\delta s$ với hai lần $\delta t$", True),
           (r"Cộng $\delta s$ và $\delta t$ một lần", r"Đại lượng có số mũ $n$ thì sai số tỉ đối nhân với $n$."),
           (r"Nhân $\delta s$ với $\delta t$", r"Sai số tỉ đối của tích hoặc thương là tổng, không phải tích.")]),
  buoc("Ghi kết quả", "Kết quả $a$ ghi đúng chữ số có nghĩa là gì?", loi=r"Giữ hai chữ số có nghĩa cho $\Delta a$ vì làm tròn máy tính ra 0,051.",
       lua_chon=[(r"$a = (1{,}07 \pm 0{,}05)\ \text{m/s}^2$", True), (r"$a = (1{,}07 \pm 0{,}051)\ \text{m/s}^2$", r"Chữ số đầu của $\Delta a$ là 5 nên chỉ giữ một chữ số có nghĩa."),
                 (r"$a = (1{,}1 \pm 0{,}05)\ \text{m/s}^2$", r"$\overline{a}$ phải có cùng số chữ số thập phân với $\Delta a$ (hai chữ số).")],
       ke=[(r"Làm tròn $\Delta a$ trước, rồi làm tròn $\overline{a}$ cùng chữ số thập phân", True),
           (r"Làm tròn $\overline{a}$ tới một chữ số có nghĩa", r"Số chữ số của $\overline{a}$ do $\Delta a$ quyết định, không do tuỳ ý."),
           (r"Giữ nguyên mọi chữ số máy tính cho", r"Máy tính cho nhiều chữ số hơn dụng cụ đo đã cho phép.")]),
  buoc("Nguồn sai số lớn nhất", "Đại lượng nào đóng góp nhiều nhất vào sai số tỉ đối của $a$?", loi=r"Chọn đại lượng có giá trị đo lớn hơn.",
       lua_chon=[(r"Thời gian $t$", True), (r"Quãng đường $s$", r"Phần của $s$ là $0{,}83\,\%$, nhỏ hơn phần $4{,}0\,\%$ của $t$."),
                 (r"Hai đại lượng đóng góp như nhau", r"Hai phần $0{,}83\,\%$ và $4{,}0\,\%$ khác nhau nhiều.")],
       ke=[(r"So $\delta s$ với $2\,\delta t$", True),
           (r"So $\Delta s$ với $\Delta t$", r"Hai sai số tuyệt đối khác đơn vị, không so được."),
           (r"So $s$ với $t$", r"Giá trị đo của hai đại lượng không nói lên mức đóng góp vào sai số.")])]),
]

write(J, 48, "Bài 3. Đơn vị và sai số trong vật lí", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)

_t = open(J).read().replace('\\\\\\"', '\\"')
open(J, "w").write(_t)
