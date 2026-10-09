"""Bài tập mẫu bài 11 (lesson 30) — Sóng điện từ. 4 dạng, dễ → khó (quét dạng: scripts/logs/batch-ra-soat/ket-qua/30.quet-dang.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-30.py  → ghi scripts/data/bai-tap-mau/30.json (không có old/30.json nên không có tu_luan).
Hình tính thật: sóng = hình sin dịch đúng một bước sóng sau một chu kì (cùng tốc độ c); ra-đa = xung đi về đều với tốc độ không đổi."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "30.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
MUTE = "#94a3b8"
C = 3e8

# ───────────── hàm chung ─────────────
def sine(x0, x1, y0, A, lam, xc, step):
    """Sóng sin y = y0 − A·cos(2π(x − xc)/λ): đỉnh tại x = xc + kλ."""
    n = int((x1 - x0) / step) + 1
    return [(x0 + i * step, y0 - A * math.cos(2 * math.pi * (x0 + i * step - xc) / lam)) for i in range(n)]

def moving(pts, dx, dur, col, w=2.4):
    """Hình sin dịch sang phải dx px trong dur giây (chạy một lần khi bấm)."""
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{dx} 0" dur="{dur}s" begin="indefinite" fill="freeze"/>'
            + poly(pts, col, w) + '</g>')

def radar(x, y):
    return (f'<path d="M{x},{y - 16} Q{x + 18},{y} {x},{y + 16}" fill="none" stroke="currentColor" stroke-width="2.6"/>'
            + seg(x - 2, y, x - 16, y, "currentColor", 2.6) + seg(x - 16, y - 8, x - 16, y + 8, "currentColor", 2.6))

def drone(x, y):
    """Drone nhìn từ bên: thân + hai cánh quạt, tâm tại (x, y)."""
    return (f'<rect x="{x - 12}" y="{y - 4}" width="24" height="9" rx="3" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            + seg(x - 22, y - 9, x - 4, y - 9, "currentColor", 2.4) + seg(x + 4, y - 9, x + 22, y - 9, "currentColor", 2.4)
            + seg(x - 13, y - 9, x - 13, y - 4, "currentColor", 2) + seg(x + 13, y - 9, x + 13, y - 4, "currentColor", 2))

# ───────────── Dạng 1: λ = c/f (bộ đàm 150 MHz, trạm 4G 15 cm) ─────────────
def d1(k):
    p = f"d1{k}"
    if k == 2:
        b = ""
        rows = [("Đề cho f", "tìm λ = c / f", BLUE), ("Đề cho λ", "tìm f = c / λ", BLUE), ("MHz → Hz", "nhân 10⁶", ORG), ("GHz → Hz", "nhân 10⁹", ORG), ("cm → m", "nhân 10⁻²", ORG)]
        for i, (a, c_, col) in enumerate(rows):
            b += lbl(40, 34 + i * 28, a, col, 14, "start", "700") + lbl(170, 34 + i * 28, "▸  " + c_, "currentColor", 14, "start", "400")
        return fig("d1-2", "0 0 420 170", "Hai cách dùng công thức bước sóng và các đổi đơn vị cần làm trước", b, "Dữ kiện: đổi về Hz, m rồi mới thế vào công thức. " + NOTE)
    lt, lb = 180, 13.5
    top = sine(-140, 400, 84, 24, lt, 70, 2)
    bot = sine(-140, 400, 172, 9, lb, 70, 1.35)
    b = defs(p) + '<clipPath id="c30a"><rect x="40" y="52" width="360" height="170"/></clipPath>'
    b += '<g clip-path="url(#c30a)">' + moving(top, lt, 4, RED) + moving(bot, lt, 4, RED, 2.2) + '</g>'
    b += lbl(40, 18, "Bộ đàm: f = 150 MHz", "currentColor", 13, "start", "700")
    b += dim(p, "b", 70, 42, 70 + lt, 42, "", 0, 0) + lbl(70 + lt / 2 - 22, 36, "λ = ?", BLUE, 13, "start", "700")
    b += lbl(40, 134, "Trạm 4G: λ = 15 cm", "currentColor", 13, "start", "700") + lbl(250, 134, "f = ?", ORG, 13, "start", "700")
    b += arrow(p, "g", 40, 212, 130, 212, 2.4) + lbl(138, 217, "cùng tốc độ c", GRN, 13, "start", "700")
    return fig("d1-0", "0 0 420 230", "Hai sóng điện từ cùng lan truyền sang phải với tốc độ c; sóng bộ đàm có bước sóng dài, sóng 4G có bước sóng ngắn", b,
               "Mô phỏng: sau một chu kì của sóng bộ đàm, cả hai sóng cùng dịch một đoạn bằng c·T (chạy chậm hàng tỉ lần). Hình minh hoạ, không đúng tỉ lệ.")

# ───────────── Dạng 2: thang sóng điện từ ─────────────
X0, PD = 30, 24      # x của λ = 10³ m; px mỗi bậc 10
def xs(lg): return X0 + PD * (3 - lg)
BANDS = [(3, 0, "#38bdf8"), (0, -3, "#818cf8"), (-3, math.log10(760e-9), "#fb923c"), (math.log10(760e-9), math.log10(380e-9), "#4ade80"),
         (math.log10(380e-9), -8, "#a78bfa"), (-8, -11, "#f87171"), (-11, -12, "#fbbf24")]
NAMES = [("vô tuyến", 0, "a"), ("vi sóng", 1, "b"), ("hồng ngoại", 2, "a"), ("nhìn thấy", 3, "b"), ("tử ngoại", 4, "a"), ("tia X", 5, "b"), ("tia γ", 6, "b")]

def scale(with_pointer):
    b = ""
    for (a, c_, col) in BANDS:
        b += f'<rect x="{xs(a):.1f}" y="100" width="{xs(c_) - xs(a):.1f}" height="26" fill="{col}" fill-opacity="0.35" stroke="currentColor" stroke-width="1.4"/>'
    for nm, i, side in NAMES:
        a, c_, _ = BANDS[i]; cx = (xs(a) + xs(c_)) / 2
        b += lbl(cx, 92 if side == "a" else 146, nm, "currentColor", 12, "middle", "700")
    if True:   # vạch chia theo luỹ thừa 10
        for lg, name in ((3, "1 km"), (0, "1 m"), (-3, "1 mm"), (-6, "1 μm"), (-9, "1 nm"), (-12, "1 pm")):
            x = xs(lg); b += seg(x, 126, x, 134, "currentColor", 1.4) + lbl(x, 172, name, MUTE, 12, "middle", "400")
    return b

def d2(k):
    p = f"d2{k}"
    b = defs(p) + scale(False)
    if k == 0:
        b += arrow(p, "b", 60, 58, 360, 58, 2.4) + lbl(60, 48, "bước sóng λ giảm dần, tần số f tăng dần", BLUE, 13, "start", "700")
        ptr = seg(X0, 70, X0, 130, ORG, 3) + f'<polygon points="{X0 - 6},64 {X0 + 6},64 {X0},74" fill="{ORG}"/>'
        b += f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{360} 0" dur="6s" begin="indefinite" fill="freeze"/>{ptr}</g>'
        return fig("d2-0", "0 0 420 190", "Thang sóng điện từ chia theo luỹ thừa của 10 từ bước sóng 1 km đến 1 pm, có kim quét từ sóng dài sang sóng ngắn", b,
                   "Mô phỏng: kim quét qua thang từ bước sóng dài đến ngắn (chạy 6 s). Trục chia theo luỹ thừa 10; vùng nhìn thấy là dải rất hẹp.")
    if k == 2:
        b += lbl(30, 28, "λ₁ = ?  (đổi ra nm)", ORG, 13, "start", "700") + lbl(30, 48, "λ₂ = ?  (đổi ra μm)", ORG, 13, "start", "700")
        b += lbl(240, 28, "1 nm = 10⁻⁹ m", "currentColor", 13, "start", "400") + lbl(240, 48, "1 μm = 10⁻⁶ m", "currentColor", 13, "start", "400")
        return fig("d2-2", "0 0 420 190", "Cần tính hai bước sóng, đổi sang nm và μm rồi so với các mốc của thang sóng điện từ", b, "Dữ kiện: so λ với mốc phải cùng đơn vị. " + NOTE)
    b += lbl(30, 28, "① λ = c / f", ORG, 14, "start", "700") + lbl(30, 50, "② đổi cùng đơn vị với mốc", ORG, 14, "start", "700") + lbl(30, 72, "③ nằm giữa hai mốc nào?", ORG, 14, "start", "700")
    return fig("d2-3", "0 0 420 190", "Ba bước: tính bước sóng, đổi đơn vị, so với mốc của thang", b, "Dữ kiện: ba bước theo thứ tự. " + NOTE)

# ───────────── Dạng 3: chọn nhận định đúng (vệ tinh → mặt đất) ─────────────
def d3(k):
    p = f"d3{k}"
    if k == 2:
        b = ""
        rows = [("a", "môi trường truyền: sóng cơ hay sóng điện từ?"), ("b", "hướng của E, B và phương truyền"), ("c", "f, v, λ: đại lượng nào đổi khi đổi môi trường?"), ("d", "tốc độ trong chân không phụ thuộc vào gì?")]
        for i, (a, t) in enumerate(rows):
            b += lbl(26, 36 + i * 30, a, ORG, 15, "start", "700") + lbl(48, 36 + i * 30, "▸  " + t, "currentColor", 13, "start", "400")
        return fig("d3-2", "0 0 420 150", "Mỗi nhận định ứng với một khái niệm cần nhớ lại", b, "Dữ kiện: mỗi nhận định kiểm tra một ý riêng. " + NOTE)
    sx, sy, v, D = 210, 52, 45.0, 4.0
    b = defs(p) + '<clipPath id="c30b"><rect x="12" y="62" width="396" height="170"/></clipPath><g clip-path="url(#c30b)">'
    for i in range(6):
        t0 = 0.5 * i; R = v * (D - t0)
        kt, vals = ("0;1", f"0;{R:.0f}") if i == 0 else (f"0;{t0 / D:.3f};1", f"0;0;{R:.0f}")
        b += f'<circle cx="{sx}" cy="{sy}" r="0" fill="none" stroke="{GRN}" stroke-width="2.2"><animate attributeName="r" values="{vals}" keyTimes="{kt}" dur="{D}s" begin="indefinite" fill="freeze"/></circle>'
    b += '</g>'
    b += f'<rect x="{sx - 10}" y="{sy - 12}" width="20" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    b += f'<rect x="{sx - 40}" y="{sy - 5}" width="26" height="9" fill="none" stroke="currentColor" stroke-width="2"/><rect x="{sx + 14}" y="{sy - 5}" width="26" height="9" fill="none" stroke="currentColor" stroke-width="2"/>'
    b += f'<path d="M{sx - 20},206 Q{sx},232 {sx + 20},206 Z" fill="none" stroke="currentColor" stroke-width="2.4"/>' + seg(sx, 219, sx, 230, "currentColor", 2.4)
    b += lbl(sx + 50, sy - 2, "ăng ten phát (vệ tinh)", "currentColor", 13, "start", "700") + lbl(sx + 30, 224, "chảo thu", "currentColor", 13, "start", "700")
    return fig("d3-0", "0 0 420 240", "Vệ tinh phát sóng điện từ, các mặt sóng lan ra xa dần về phía chảo thu trên mặt đất", b,
               "Mô phỏng: các mặt sóng từ ăng ten lan ra với tốc độ không đổi (chạy 4 s). " + NOTE)

# ───────────── Dạng 4: ra-đa, drone ─────────────
RX, XD1, XD2 = 52, 250, 282
def d4(k):
    p = f"d4{k}"; y = 128
    b = defs(p)
    if k == 2:
        b += radar(RX, y) + drone(XD1, y)
        b += arrow(p, "o", RX + 24, y - 12, XD1 - 30, y - 12, 2.4) + lbl((RX + XD1) / 2 - 8, y - 20, "đi", ORG, 13, "start", "700")
        b += arrow(p, "b", XD1 - 30, y + 12, RX + 24, y + 12, 2.4) + lbl((RX + XD1) / 2 - 8, y + 30, "về", BLUE, 13, "start", "700")
        b += dim(p, "g", RX, y + 54, XD1, y + 54, "d = ?", (RX + XD1) / 2 - 20, y + 72)
        b += lbl(30, 28, "s = c · t là quãng đường cả đi lẫn về", "currentColor", 13, "start", "700") + lbl(30, 50, "hai lần đo cách nhau Δt → tốc độ", "currentColor", 13, "start", "700")
        return fig("d4-2", "0 0 420 220", "Xung sóng đi từ ra-đa tới drone rồi phản xạ về; khoảng cách d khác quãng đường đi và về", b, "Dữ kiện: phân biệt quãng đường sóng đi với khoảng cách tới vật. " + NOTE)
    if k == 1:
        return ""
    # k = 0: mô phỏng hai lần đo; tốc độ xung không đổi 200 px/s, drone dịch ra xa trong khoảng 30 s giữa hai lần đo
    v = 200.0; dt = 0.05
    tA, tB = (XD1 - RX) / v, (XD2 - RX) / v          # thời gian đi tới drone ở lần 1, lần 2
    t1e = 2 * tA; gap = 1.2; t2s = t1e + gap; t2e = t2s + 2 * tB
    n = int(round(t2e / dt)) + 1
    ts = [i * dt for i in range(n)]
    def pulse(t):
        if t <= tA: return RX + v * t, 1
        if t <= t1e: return XD1 - v * (t - tA), 1
        if t < t2s: return RX, 0
        u = t - t2s
        if u <= tB: return RX + v * u, 1
        return XD2 - v * (u - tB), 1
    def dpos(t):
        if t <= t1e: return 0.0
        if t >= t2s: return XD2 - XD1
        return (XD2 - XD1) * (t - t1e) / gap
    px = [pulse(t)[0] for t in ts]; po = [pulse(t)[1] for t in ts]; dx = [dpos(t) for t in ts]
    dur = ts[-1]
    A = lambda attr, vals: f'<animate attributeName="{attr}" values="{";".join(f"{x:.1f}" if attr != "opacity" else str(x) for x in vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'
    b += radar(RX, y)
    b += f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"{x:.1f} 0" for x in dx)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>{drone(XD1, y)}</g>'
    b += f'<circle cx="{px[0]:.1f}" cy="{y}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">{A("cx", px)}{A("opacity", po)}</circle>'
    b += dim(p, "g", RX, y + 44, XD1, y + 44, "d₁ = ?", (RX + XD1) / 2 - 20, y + 62) + dim(p, "g", RX, y + 74, XD2, y + 74, "d₂ = ?", (RX + XD2) / 2 - 20, y + 92)
    b += lbl(30, 26, "Lần 1: t₁ = 160 μs", "currentColor", 13, "start", "700") + lbl(30, 46, "Lần 2 (sau 30 s): t₂ = 164 μs", "currentColor", 13, "start", "700") + lbl(250, 26, "v = ?", ORG, 13, "start", "700")
    b += lbl(RX - 10, y - 26, "ra-đa", "currentColor", 12, "middle", "400")
    return fig("d4-0", "0 0 420 240", "Ra-đa phát xung tới drone, thu xung phản xạ; 30 giây sau drone đã ra xa hơn và ra-đa đo lần hai", b,
               "Mô phỏng: xung đi tới drone rồi về, lặp lại sau khi drone bay ra xa (chạy chậm; khoảng dịch của drone vẽ phóng đại).")

BUILD = [d1, d2, d3, d4]

DANG = [
 dict(label="Dạng 1 · Dễ · Tính bước sóng hoặc tần số (λ = c/f)",
      topic="Đặc điểm và thang sóng điện từ",
      problem_html=("<p>Bộ đàm của đội cứu hộ phát sóng điện từ có tần số $150\\ \\text{MHz}$. Một trạm 4G phát sóng điện từ có bước sóng $15\\ \\text{cm}$. "
                    "Coi hai sóng truyền trong không khí như trong chân không, lấy $c=3\\cdot10^{8}\\ \\text{m/s}$.</p>"
                    "<p>a) Tính bước sóng của sóng bộ đàm.</p><p>b) Tính tần số của sóng trạm 4G.</p>"
                    "<p>c) Sóng nào có bước sóng dài hơn và dài gấp mấy lần?</p>")),
 dict(label="Dạng 2 · Trung bình · Xác định vùng của bức xạ trên thang sóng điện từ",
      topic="Đặc điểm và thang sóng điện từ",
      problem_html=("<p>Một nguồn phát ra hai bức xạ điện từ trong chân không, có tần số $f_1=6{,}0\\cdot10^{14}\\ \\text{Hz}$ và $f_2=3{,}0\\cdot10^{12}\\ \\text{Hz}$. "
                    "Lấy $c=3\\cdot10^{8}\\ \\text{m/s}$. Mắt người nhìn thấy ánh sáng có bước sóng từ $380\\ \\text{nm}$ đến $760\\ \\text{nm}$.</p>"
                    "<p>a) Tính bước sóng của mỗi bức xạ.</p><p>b) Mỗi bức xạ thuộc vùng nào của thang sóng điện từ?</p>")),
 dict(label="Dạng 3 · Trung bình · Chọn nhận định đúng về sóng điện từ",
      topic="Đặc điểm và thang sóng điện từ",
      problem_html=("<p>Một sóng điện từ truyền thẳng đứng từ vệ tinh xuống mặt đất. Cho biết mỗi nhận định sau đúng hay sai.</p>"
                    "<p>a) Sóng này cần có không khí làm môi trường truyền.</p>"
                    "<p>b) Tại mỗi điểm, vectơ cường độ điện trường $\\vec E$ và vectơ cảm ứng từ $\\vec B$ vuông góc với nhau và cùng vuông góc với phương truyền.</p>"
                    "<p>c) Khi sóng đi từ không khí vào thuỷ tinh, tần số của sóng giảm còn tốc độ truyền không đổi.</p>"
                    "<p>d) Trong chân không, ánh sáng đỏ và ánh sáng tím truyền với cùng một tốc độ.</p>")),
 dict(label="Dạng 4 · Khó · Thời gian truyền tín hiệu và đo khoảng cách bằng ra-đa",
      topic="Ứng dụng sóng điện từ trong truyền thông",
      problem_html=("<p>Một ra-đa phát xung sóng điện từ về phía một chiếc drone đang bay thẳng ra xa nó. Xung phản xạ thu lại sau $t_1=160\\ \\mu\\text{s}$ kể từ lúc phát. "
                    "Sau $30\\ \\text{s}$, ra-đa đo lần hai và thu xung phản xạ sau $t_2=164\\ \\mu\\text{s}$. Coi sóng truyền trong không khí với tốc độ $c=3\\cdot10^{8}\\ \\text{m/s}$.</p>"
                    "<p>a) Tính khoảng cách từ ra-đa tới drone ở mỗi lần đo.</p><p>b) Tính tốc độ trung bình của drone.</p>")),
]

ANALYSIS = [
 [("\"sóng điện từ có tần số $150\\ \\text{MHz}$\"", "$f=150$ MHz", "Cho $f$ thì tìm $\\lambda=\\dfrac{c}{f}$; đổi MHz ra Hz"),
  ("\"trạm 4G … bước sóng $15\\ \\text{cm}$\"", "$\\lambda=15$ cm", "Cho $\\lambda$ thì tìm $f=\\dfrac{c}{\\lambda}$; đổi cm ra m"),
  ("\"như trong chân không, $c=3\\cdot10^{8}\\ \\text{m/s}$\"", "$c=3\\cdot10^{8}$ m/s", "⚠ $\\lambda=\\dfrac{c}{f}$ dùng với $c$ trong chân không; $f$ (Hz), $\\lambda$ (m)"),
  ("\"sóng nào có bước sóng dài hơn, gấp mấy lần\"", "So hai bước sóng", "Chia hai bước sóng cùng đơn vị")],
 [("\"$f_1=6{,}0\\cdot10^{14}\\ \\text{Hz}$ và $f_2=3{,}0\\cdot10^{12}\\ \\text{Hz}$\"", "$f_1$, $f_2$ (Hz)", "Cho $f$ thì tìm $\\lambda=\\dfrac{c}{f}$"),
  ("\"trong chân không, $c=3\\cdot10^{8}\\ \\text{m/s}$\"", "$c$", "⚠ $\\lambda=\\dfrac{c}{f}$ là bước sóng trong chân không; các mốc của thang cũng tính trong chân không"),
  ("\"tính bước sóng của mỗi bức xạ\"", "Cần $\\lambda_1$, $\\lambda_2$", "Giữ đơn vị mét rồi đổi: $1\\ \\text{nm}=10^{-9}$ m; $1\\ \\mu\\text{m}=10^{-6}$ m"),
  ("\"nhìn thấy … từ $380\\ \\text{nm}$ đến $760\\ \\text{nm}$\"", "Dải $380$–$760$ nm", "Một mốc của thang sóng điện từ"),
  ("\"thuộc vùng nào của thang\"", "Cần vùng", "So $\\lambda$ với mốc các vùng (cùng đơn vị): vô tuyến, vi sóng, hồng ngoại, nhìn thấy, tử ngoại, tia X, tia gamma")],
 [("\"cần có không khí làm môi trường truyền\"", "Nhận định a", "⚠ Mỗi tính chất chỉ đúng trong phạm vi của nó: chân không hay môi trường vật chất, sóng cơ hay sóng điện từ"),
  ("\"$\\vec E$ và $\\vec B$ … phương truyền\"", "Nhận định b", "Hướng của $\\vec E$, $\\vec B$ so với nhau và so với phương truyền"),
  ("\"từ không khí vào thuỷ tinh\"", "Nhận định c", "Đại lượng do nguồn quyết định ($f$, $T$) và đại lượng do môi trường quyết định ($v$, $\\lambda=\\dfrac{v}{f}$)"),
  ("\"ánh sáng đỏ và ánh sáng tím … trong chân không\"", "Nhận định d", "Tốc độ sóng điện từ trong chân không và quan hệ $c=\\lambda f$")],
 [("\"ra-đa phát xung … thu lại sau $t_1=160\\ \\mu\\text{s}$\"", "$t_1=160\\ \\mu$s", "Thời gian đi - về của sóng; đổi $\\mu$s ra s"),
  ("\"tốc độ $c=3\\cdot10^{8}\\ \\text{m/s}$\"", "$c$", "⚠ Sóng truyền thẳng đều với tốc độ $c$: $s=ct$ là quãng đường sóng đi được"),
  ("\"sau $30\\ \\text{s}$ … $t_2=164\\ \\mu\\text{s}$\"", "$\\Delta t=30$ s; $t_2$", "Mỗi lần đo cho một khoảng cách; tốc độ lấy từ hiệu hai khoảng cách"),
  ("\"khoảng cách từ ra-đa tới drone ở mỗi lần đo\"", "Cần $d_1$, $d_2$", "Từ $s=ct$ và quan hệ giữa $s$ với $d$"),
  ("\"tốc độ trung bình của drone\"", "Cần $v$", "$v=\\dfrac{\\Delta d}{\\Delta t}$")],
]

R1 = ["<strong>Khái niệm:</strong> bước sóng $\\lambda$ là quãng đường sóng đi được trong một chu kì.",
      "<strong>Định luật:</strong> trong chân không mọi sóng điện từ cùng tốc độ $c=3\\cdot10^{8}$ m/s.",
      "$\\lambda=\\dfrac{c}{f}=cT$ · $f=\\dfrac{c}{\\lambda}$",
      "Đổi: $1\\ \\text{MHz}=10^{6}$ Hz · $1\\ \\text{GHz}=10^{9}$ Hz · $1\\ \\text{cm}=10^{-2}$ m",
      "⚠ <strong>Điều kiện:</strong> $c$ là tốc độ trong chân không (không khí coi như chân không); đổi mọi đại lượng về Hz, m, m/s."]
R2 = ["<strong>Khái niệm:</strong> thang sóng điện từ xếp các vùng theo bước sóng giảm dần (tần số tăng dần).",
      "<strong>Định luật:</strong> mọi vùng cùng bản chất, khác $\\lambda$; trong chân không $\\lambda=\\dfrac{c}{f}$.",
      "Thứ tự: vô tuyến → vi sóng → hồng ngoại → nhìn thấy → tử ngoại → tia X → tia gamma.",
      "Mốc: nhìn thấy $380$–$760$ nm · hồng ngoại $760\\ \\text{nm}$–$1\\ \\text{mm}$ · vi sóng $1\\ \\text{mm}$–$1\\ \\text{m}$",
      "⚠ <strong>Điều kiện:</strong> so $\\lambda$ với mốc phải cùng đơn vị; $1\\ \\text{nm}=10^{-9}$ m, $1\\ \\mu\\text{m}=10^{-6}$ m."]
R3 = ["<strong>Khái niệm:</strong> sóng điện từ là điện từ trường biến thiên lan truyền, không cần phần tử môi trường.",
      "<strong>Định luật:</strong> $\\vec E\\perp\\vec B\\perp$ phương truyền, cùng pha: sóng ngang.",
      "Chân không: mọi sóng điện từ cùng tốc độ $c$, $c=\\lambda f$.",
      "Đổi môi trường: $f$, $T$ giữ nguyên; $v$ và $\\lambda=\\dfrac{v}{f}$ đổi.",
      "⚠ <strong>Điều kiện:</strong> xét đúng phạm vi của từng tính chất (chân không hay môi trường vật chất)."]
R4 = ["<strong>Khái niệm:</strong> ra-đa đo khoảng cách bằng thời gian sóng đi tới vật rồi phản xạ về.",
      "<strong>Định luật:</strong> sóng điện từ truyền thẳng đều với tốc độ $c$.",
      "Quãng đường đi - về: $s=ct$ · tốc độ trung bình: $v=\\dfrac{\\Delta d}{\\Delta t}$",
      "Đổi: $1\\ \\mu\\text{s}=10^{-6}$ s",
      "⚠ <strong>Điều kiện:</strong> sóng đi thẳng tới vật rồi phản xạ về đúng đường cũ."]

SOLS = [
 sol(R1, [
  ("Bước sóng của sóng bộ đàm", [P("Đổi tần số ra Hz: $f=150\\ \\text{MHz}=1{,}5\\cdot10^{8}\\ \\text{Hz}$."), M(r"\lambda=\dfrac{c}{f}=\dfrac{3\cdot10^{8}}{1{,}5\cdot10^{8}}"), A(r"\lambda=2\ \text{m}")]),
  ("Tần số của sóng trạm 4G", [P("Đổi bước sóng ra mét: $\\lambda=15\\ \\text{cm}=0{,}15\\ \\text{m}$."), M(r"f=\dfrac{c}{\lambda}=\dfrac{3\cdot10^{8}}{0{,}15}=2\cdot10^{9}\ \text{Hz}"), A(r"f=2\ \text{GHz}")]),
  ("So hai bước sóng", [P("Hai bước sóng cùng đơn vị mét, chia số lớn cho số nhỏ:"), M(r"\dfrac{2}{0{,}15}\approx13{,}3"), A("T:Sóng bộ đàm có bước sóng dài hơn, gấp khoảng $13{,}3$ lần.")]),
  ("Kiểm tra", [P("Tích $\\lambda f$ của cả hai sóng bằng $3\\cdot10^{8}$ m/s ✓."), P("Bước sóng dài hơn ứng với tần số nhỏ hơn: $150\\ \\text{MHz}\\lt2\\ \\text{GHz}$ ✓.")])],
  ["a) $\\lambda=2\\ \\text{m}$", "b) $f=2\\ \\text{GHz}$", "c) Sóng bộ đàm dài hơn, gấp khoảng $13{,}3$ lần"],
  "Nhận dạng: đề cho <strong>tần số</strong> hoặc <strong>bước sóng</strong> của sóng điện từ → $\\lambda=\\dfrac{c}{f}$, đổi về Hz và m trước."),
 sol(R2, [
  ("Bước sóng của bức xạ thứ nhất", [M(r"\lambda_1=\dfrac{c}{f_1}=\dfrac{3\cdot10^{8}}{6\cdot10^{14}}=5\cdot10^{-7}\ \text{m}"), A(r"\lambda_1=500\ \text{nm}")]),
  ("Bước sóng của bức xạ thứ hai", [M(r"\lambda_2=\dfrac{c}{f_2}=\dfrac{3\cdot10^{8}}{3\cdot10^{12}}=10^{-4}\ \text{m}"), A(r"\lambda_2=100\ \mu\text{m}=0{,}1\ \text{mm}")]),
  ("Xếp vào thang sóng điện từ", [P("$500\\ \\text{nm}$ nằm trong khoảng $380$–$760$ nm: <strong>ánh sáng nhìn thấy</strong>."), P("$0{,}1\\ \\text{mm}$ nằm trong khoảng $760\\ \\text{nm}$–$1\\ \\text{mm}$: <strong>hồng ngoại</strong>."), A("T:Mắt chỉ nhìn thấy bức xạ thứ nhất.")]),
  ("Kiểm tra", [P("$f_1\\gt f_2$ nên $\\lambda_1\\lt\\lambda_2$ ✓."), P("Hồng ngoại có bước sóng dài hơn ánh sáng nhìn thấy ✓.")])],
  ["a) $\\lambda_1=500\\ \\text{nm}$ · $\\lambda_2=100\\ \\mu\\text{m}$", "b) Bức xạ 1: ánh sáng nhìn thấy · bức xạ 2: hồng ngoại"],
  "Nhận dạng: đề cho <strong>tần số</strong> rồi hỏi <strong>vùng</strong> của bức xạ → tính $\\lambda=\\dfrac{c}{f}$, đổi đơn vị rồi so với mốc của thang."),
 sol(R3, [
  ("Nhận định a", [P("Sóng điện từ không cần phần tử môi trường: ánh sáng Mặt Trời tới Trái Đất qua chân không."), A("T:Nhận định a) <strong>sai</strong>.")]),
  ("Nhận định b", [P("Tại mỗi điểm $\\vec E\\perp\\vec B$, cả hai vuông góc phương truyền: sóng điện từ là sóng ngang."), A("T:Nhận định b) <strong>đúng</strong>.")]),
  ("Nhận định c", [P("Tần số do nguồn quyết định nên giữ nguyên khi đổi môi trường; tốc độ và bước sóng đổi."), M(r"\lambda=\dfrac{v}{f}"), A("T:Nhận định c) <strong>sai</strong>: tần số không đổi, tốc độ giảm.")]),
  ("Nhận định d", [P("Trong chân không mọi sóng điện từ có cùng tốc độ $c$, kể cả ánh sáng đỏ và tím."), M(r"c=\lambda f"), P("$f$ tăng thì $\\lambda$ giảm đúng tỉ lệ, tích vẫn bằng $c$."), A("T:Nhận định d) <strong>đúng</strong>.")])],
  ["a) Sai", "b) Đúng", "c) Sai", "d) Đúng"],
  "Nhận dạng: đề cho <strong>nhiều nhận định</strong> về sóng điện từ → xét từng ý theo môi trường truyền, hướng $\\vec E$, $\\vec B$, đại lượng đổi hay không khi đổi môi trường."),
 sol(R4, [
  ("Quãng đường sóng đi - về, lần 1", [P("Đổi: $t_1=160\\ \\mu\\text{s}=1{,}6\\cdot10^{-4}\\ \\text{s}$."), M(r"s_1=ct_1=3\cdot10^{8}\cdot1{,}6\cdot10^{-4}"), A(r"s_1=4{,}8\cdot10^{4}\ \text{m}=48\ \text{km}")]),
  ("Khoảng cách lần 1", [P("Sóng đi tới drone rồi quay về nên quãng đường gồm hai lần khoảng cách:"), M(r"d_1=\dfrac{s_1}{2}=\dfrac{48}{2}"), A(r"d_1=24\ \text{km}")]),
  ("Khoảng cách lần 2", [P("Làm tương tự với $t_2=164\\ \\mu\\text{s}=1{,}64\\cdot10^{-4}\\ \\text{s}$:"), M(r"d_2=\dfrac{ct_2}{2}=\dfrac{3\cdot10^{8}\cdot1{,}64\cdot10^{-4}}{2}"), A(r"d_2=2{,}46\cdot10^{4}\ \text{m}=24{,}6\ \text{km}")]),
  ("Tốc độ trung bình của drone", [M(r"\Delta d=d_2-d_1=24{,}6-24=0{,}6\ \text{km}=600\ \text{m}"), P("Thời gian giữa hai lần đo là $\\Delta t=30$ s:"), M(r"v=\dfrac{\Delta d}{\Delta t}=\dfrac{600}{30}"), A(r"v=20\ \text{m/s}")]),
  ("Kiểm tra", [P("$20\\ \\text{m/s}=72\\ \\text{km/h}$: hợp lí với một chiếc drone ✓."), P("$t_2\\gt t_1$ nên $d_2\\gt d_1$: drone bay ra xa ✓.")])],
  ["a) $d_1=24\\ \\text{km}$ · $d_2=24{,}6\\ \\text{km}$", "b) $v=20\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>thời gian từ lúc phát đến lúc thu</strong> sóng phản xạ → $d=\\dfrac{ct}{2}$; hai lần đo → $v=\\dfrac{\\Delta d}{\\Delta t}$."),
]

STEPS = [
 dict(nhan_dang="Thấy <b>tần số</b> hoặc <b>bước sóng</b> của sóng điện từ → dùng $\\lambda=\\dfrac{c}{f}$, đổi về Hz và m trước.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Bước sóng của sóng bộ đàm", "Bước sóng của sóng bộ đàm bằng bao nhiêu mét?", 2, "m", 0.05,
       loi="Quên đổi MHz ra Hz (thế $150$ thay vì $1{,}5\\cdot10^{8}$) hoặc lật ngược thành $\\dfrac{f}{c}$."),
  buoc("Tần số của sóng trạm 4G", "Tần số của sóng trạm 4G bằng bao nhiêu GHz?", 2, "GHz", 0.05,
       loi="Chia $c$ cho $15$ (quên đổi cm ra m) ra $2\\cdot10^{7}$ Hz; hoặc nhân $c\\cdot\\lambda$ thay vì chia.",
       ke=[("Dùng $f=\\dfrac{c}{\\lambda}$ với $\\lambda$ đổi ra mét", True),
           ("$f=c\\cdot\\lambda$", "Đơn vị không hợp: $c\\lambda$ có đơn vị m²/s, không phải Hz; công thức đúng là $f=\\dfrac{c}{\\lambda}$."),
           ("$f=\\dfrac{c}{\\lambda}$ với $\\lambda=15$ (giữ nguyên cm)", "Phải đổi cm ra m ($0{,}15$ m) vì $c$ tính bằng m/s.")]),
  buoc("So hai bước sóng", "Bước sóng của bộ đàm gấp mấy lần bước sóng của trạm 4G?", 13.3, None, 0.2,
       loi="Chia $2$ cho $15$ khi chưa cùng đơn vị, hoặc chia ngược lại.",
       ke=[("Đổi cùng đơn vị rồi chia bước sóng lớn cho bước sóng nhỏ", True),
           ("Lấy hiệu hai bước sóng", "Hỏi \"gấp mấy lần\" là phép chia, không phải phép trừ."),
           ("Chia ngay $2\\ \\text{m}$ cho $15\\ \\text{cm}$", "Chưa cùng đơn vị nên tỉ số sai; phải đổi cả hai về mét hoặc cả hai về cm.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Đề cho <b>tần số</b> rồi hỏi <b>vùng</b> của bức xạ → tính $\\lambda=\\dfrac{c}{f}$, đổi đơn vị rồi so với mốc của thang.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Bước sóng của bức xạ thứ nhất", "Bước sóng $\\lambda_1$ bằng bao nhiêu nm?", 500, "nm", 5,
       loi="Đọc $5\\cdot10^{-7}$ m thành $5$ nm hoặc $500\\ \\mu\\text{m}$ vì nhầm $10^{-9}$ với $10^{-6}$."),
  buoc("Bước sóng của bức xạ thứ hai", "Bước sóng $\\lambda_2$ bằng bao nhiêu μm?", 100, "μm", 2,
       loi="Đổi $10^{-4}$ m ra μm sai luỹ thừa (ra $0{,}1\\ \\mu\\text{m}$ hoặc $10^{-4}\\ \\mu\\text{m}$).",
       ke=[("Dùng $\\lambda_2=\\dfrac{c}{f_2}$ rồi đổi mét sang μm", True),
           ("$\\lambda_2=\\lambda_1\\dfrac{f_2}{f_1}$", "Ngược tỉ lệ: $\\lambda$ tỉ lệ nghịch với $f$, nên phải là $\\lambda_1\\dfrac{f_1}{f_2}$."),
           ("$\\lambda_2=\\dfrac{f_2}{c}$", "Lật ngược công thức; đơn vị hai vế không khớp.")]),
  buoc("Xếp vào thang sóng điện từ", "Mỗi bức xạ thuộc vùng nào của thang sóng điện từ?",
       loi="Quên đổi đơn vị trước khi so mốc, ví dụ so số của μm với mốc ghi bằng nm.",
       lua_chon=[("Bức xạ 1 là ánh sáng nhìn thấy; bức xạ 2 là hồng ngoại", True),
                 ("Bức xạ 1 là tử ngoại; bức xạ 2 là vi sóng", "$\\lambda_1$ nằm trong khoảng $380$–$760$ nm của ánh sáng nhìn thấy (tử ngoại ngắn hơn $380$ nm); $\\lambda_2\\lt1$ mm nên là hồng ngoại, vi sóng dài hơn $1$ mm."),
                 ("Bức xạ 1 là hồng ngoại; bức xạ 2 là sóng vô tuyến", "Hồng ngoại dài hơn $760$ nm mà $\\lambda_1$ nằm trong dải nhìn thấy; sóng vô tuyến dài hơn $1$ m còn $\\lambda_2$ chỉ cỡ $0{,}1$ mm.")],
       ke=[("So $\\lambda$ (cùng đơn vị) với các mốc của thang", True),
           ("So $f$ với $c$", "$c$ là tốc độ, không phải mốc phân vùng; vùng được phân theo $\\lambda$ (hay tần số tương ứng)."),
           ("Chọn vùng theo tên nghe quen (tử ngoại, tia X)", "Không có phép tính thì không phân biệt được; phải có $\\lambda$ để so với mốc.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>nhiều nhận định</b> về sóng điện từ → xét từng ý: môi trường truyền, hướng $\\vec E$, $\\vec B$, đại lượng đổi hay không.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhận định a", "Nhận định a) đúng hay sai?",
       loi="Gán tính chất của sóng âm cho sóng điện từ.",
       lua_chon=[("Sai: sóng điện từ truyền được cả khi không có môi trường vật chất", True),
                 ("Đúng: sóng nào cũng phải có phần tử môi trường để dao động", "Đó là sóng cơ. Sóng điện từ là điện từ trường biến thiên lan truyền nên đi được qua chân không."),
                 ("Sai: sóng điện từ chỉ truyền được trong chất rắn", "Sóng điện từ truyền được trong rắn, lỏng, khí và cả chân không.")]),
  buoc("Nhận định b", "Nhận định b) đúng hay sai?",
       loi="Cho rằng $\\vec E$ và $\\vec B$ cùng phương vì \"cùng pha\".",
       lua_chon=[("Đúng: $\\vec E$, $\\vec B$ và phương truyền đôi một vuông góc", True),
                 ("Sai: $\\vec E$ và $\\vec B$ cùng phương nhưng ngược chiều", "Hai vectơ vuông góc với nhau; \"cùng pha\" nói về thời điểm đạt cực đại, không nói về phương."),
                 ("Sai: $\\vec B$ nằm dọc theo phương truyền", "Nếu có thành phần dọc thì thành sóng dọc; sóng điện từ là sóng ngang.")],
       ke=[("Xét hướng của $\\vec E$, $\\vec B$ so với nhau và so với phương truyền", True),
           ("Tính $\\lambda=\\dfrac{c}{f}$ để kiểm tra", "Nhận định này nói về hướng của các vectơ, không cần tính bước sóng."),
           ("Xét xem sóng có cần môi trường không", "Đó là nội dung nhận định a; nhận định b nói về hướng của $\\vec E$, $\\vec B$.")]),
  buoc("Nhận định c", "Nhận định c) đúng hay sai?",
       loi="Cho rằng tần số đổi theo môi trường, hoặc tốc độ không đổi khi sóng đổi môi trường.",
       lua_chon=[("Sai: tần số giữ nguyên, còn tốc độ và bước sóng giảm", True),
                 ("Đúng: sóng vào thuỷ tinh thì tần số giảm", "Tần số do nguồn quyết định nên không đổi khi sóng đổi môi trường."),
                 ("Sai: tần số tăng, tốc độ không đổi", "Tần số không đổi; tốc độ trong thuỷ tinh nhỏ hơn trong không khí.")],
       ke=[("Phân biệt đại lượng do nguồn quyết định ($f$) và do môi trường quyết định ($v$, $\\lambda$)", True),
           ("Dùng $c=3\\cdot10^{8}$ m/s cho cả hai môi trường", "$c$ là tốc độ trong chân không; trong thuỷ tinh sóng chậm hơn."),
           ("Xét xem $\\vec E$ có vuông góc $\\vec B$ không", "Đó là nội dung nhận định b, không liên quan đến việc đổi môi trường.")]),
  buoc("Nhận định d", "Nhận định d) đúng hay sai?",
       loi="Cho rằng tần số lớn thì truyền nhanh hơn trong chân không.",
       lua_chon=[("Đúng: mọi sóng điện từ có cùng tốc độ $c$ trong chân không", True),
                 ("Sai: ánh sáng tím có $f$ lớn hơn nên nhanh hơn", "$c=\\lambda f$ không đổi: $f$ lớn thì $\\lambda$ nhỏ đúng tỉ lệ, tốc độ vẫn là $c$."),
                 ("Sai: ánh sáng đỏ có $\\lambda$ dài hơn nên nhanh hơn", "Bước sóng dài đi với tần số nhỏ; tích $\\lambda f$ vẫn bằng $c$.")],
       ke=[("Dùng $c=\\lambda f$: tích $\\lambda f$ là hằng số trong chân không", True),
           ("So tần số: tần số lớn hơn thì nhanh hơn", "Tốc độ trong chân không không phụ thuộc tần số."),
           ("So khả năng đâm xuyên của hai ánh sáng", "Đâm xuyên là tương tác với vật chất, không quyết định tốc độ truyền trong chân không.")])]),
 dict(nhan_dang="Thấy <b>thời gian từ lúc phát đến lúc thu</b> sóng phản xạ → khoảng cách $d=\\dfrac{ct}{2}$; hai lần đo → $v=\\dfrac{\\Delta d}{\\Delta t}$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Quãng đường sóng đi - về, lần 1", "Quãng đường sóng đi và về trong lần đo thứ nhất bằng bao nhiêu km?", 48, "km", 0.5,
       loi="Quên đổi μs ra s (thế $160$ thay cho $1{,}6\\cdot10^{-4}$) hoặc đổi sai luỹ thừa $10^{-6}$."),
  buoc("Khoảng cách lần 1", "Khoảng cách từ ra-đa tới drone lúc đo lần 1 bằng bao nhiêu km?", 24, "km", 0.3,
       loi="Lấy luôn quãng đường đi - về làm khoảng cách, quên rằng sóng đã đi tới vật rồi quay về.",
       ke=[("Chia đôi quãng đường vì sóng đi tới vật rồi quay về", True),
           ("Lấy $d=ct$ vì sóng truyền với tốc độ $c$", "$ct$ là quãng đường đi - về; khoảng cách tới vật chỉ bằng một nửa."),
           ("Nhân đôi quãng đường vì có hai chiều", "Quãng đường đi - về đã gồm cả hai chiều; khoảng cách chỉ là một chiều nên phải chia đôi.")]),
  buoc("Khoảng cách lần 2", "Khoảng cách lúc đo lần 2 bằng bao nhiêu km?", 24.6, "km", 0.05,
       loi="Dùng lại $t_1$, hoặc cộng thêm $\\Delta t$ vào $t_2$.",
       ke=[("Làm như lần 1 với $t_2$: $d_2=\\dfrac{ct_2}{2}$", True),
           ("Cộng $30\\ \\text{s}$ vào $t_2$ rồi tính", "$30\\ \\text{s}$ là khoảng giữa hai lần đo, không phải thời gian sóng đi - về."),
           ("$d_2=d_1+ct_2$", "Mỗi lần đo cho khoảng cách tính từ ra-đa, không cộng dồn với lần trước.")]),
  buoc("Tốc độ trung bình của drone", "Tốc độ trung bình của drone bằng bao nhiêu m/s?", 20, "m/s", 0.3,
       loi="Lấy $\\Delta d$ theo km chia cho giây (ra $0{,}02$), hoặc chia cho $t_2-t_1$ thay vì $30$ s.",
       ke=[("$v=\\dfrac{d_2-d_1}{\\Delta t}$ với $\\Delta t=30$ s, $\\Delta d$ đổi ra mét", True),
           ("$v=\\dfrac{d_2-d_1}{t_2-t_1}$", "$t_2-t_1$ chỉ là hiệu thời gian sóng đi - về; thời gian drone bay là $30$ s giữa hai lần đo."),
           ("$v=\\dfrac{d_2}{t_2}$", "Đó là $\\dfrac{c}{2}$, tốc độ liên quan đến sóng, không phải tốc độ của drone.")]),
  buoc("Kiểm tra")]),
]

write(J, 30, "Bài 11. Sóng điện từ", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
