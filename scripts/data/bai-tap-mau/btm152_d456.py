"""Bài tập mẫu CĐ08 "Cảm ứng điện từ và dòng điện xoay chiều" (lesson 152) — Dạng 4–6 (truyền tải điện năng, Mở rộng HSG).
Module được build-hinh-152.py import. Dàn ý + số liệu: content/hsg9/cd08-cam-ung-dien-tu/nguon.md (tinh.py), dùng nguyên.
Dạng sau dùng lại cách làm dạng trước:
  D4 hao phí P_hp = RI², I = P/U; tăng U k lần ⇒ hao phí giảm k² lần; so với cách tăng tiết diện (R = ρℓ/S của CĐ04)
  D5 đường dây thật: R = ρ·2ℓ/S, rồi điều kiện % hao phí của D4 ⇒ U tối thiểu ⇒ tỉ số vòng máy tăng áp (máy biến áp của D3)
  D6 cho công suất NƠI TIÊU THỤ: UI = P_tt + RI² (bậc hai), H theo D4, bẫy "giữ P đầu dây không đổi".
Xuất DANG, BUILD, ANALYSIS, SOLS, STEPS (3 phần tử mỗi list) và kiem_so()."""
import math, os, re, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *  # noqa: F401,F403  (fig, seg, lbl, dot, poly, chevron, arrow, sol, M, P, A, buoc …)

T_BA = "Máy biến áp"          # chưa có YCCĐ "truyền tải điện năng" (nguon.md mục "Cần thầy quyết" 2)
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
YEL = "#facc15"

# ═════════════ SỐ LIỆU (mọi đáp số tính ở đây, kiem_so() kiểm lại; khớp content/hsg9/cd08-cam-ung-dien-tu/tinh.py) ═════════════
# D4 — hao phí cơ bản
P4, R4, U4A, U4B = F(600_000), F(24), F(15_000), F(60_000)
I4A = P4 / U4A                                   # 40 A
PH4A = R4 * I4A**2                               # 38 400 W
H4A = 1 - PH4A / P4                              # 0,936
I4B = P4 / U4B                                   # 10 A
PH4B = R4 * I4B**2                               # 2 400 W
H4B = 1 - PH4B / P4                              # 0,996
GIAM4 = PH4A / PH4B                              # 16 lần
U4MIN = math.sqrt(float(P4 * R4 / F(1, 100)))    # ≈ 37 947 V
K4 = U4MIN / float(U4A)                          # ≈ 2,53
R4D = R4 / GIAM4                                 # 1,5 Ω
S4D = R4 / R4D                                   # tiết diện gấp 16 lần
# D5 — đường dây nhôm thật
P5, U50, L5, S5 = F(2_000_000), F(6000), F(20_000), F(70, 10**6)
RHO_AL = F(28, 10**9)
R5 = RHO_AL * 2 * L5 / S5                        # 16 Ω
I5A = P5 / U50                                   # 333,3 A
PH5A = R5 * I5A**2                               # ≈ 1,778 MW
DU5A = I5A * R5                                  # ≈ 5333 V
UTT5A = U50 - DU5A                               # ≈ 667 V
U5MIN = math.sqrt(float(P5 * R5 / F(2, 100)))    # 40 000 V
N51 = 300
N52 = N51 * U5MIN / float(U50)                   # 2000 vòng
I5C = P5 / F(40_000)                             # 50 A
PH5C = R5 * I5C**2                               # 40 000 W
DU5C = I5C * R5                                  # 800 V
UTT5C = F(40_000) - DU5C                         # 39 200 V
K5HA = UTT5C / 400                               # 98
U5D = F(22_000)
R5MAX = F(2, 100) * U5D**2 / P5                  # 4,84 Ω
S5MIN = RHO_AL * 2 * L5 / R5MAX * 10**6          # ≈ 231,4 mm²
# D6 — công suất nơi tiêu thụ cho trước
R6, U6, PTT6 = 10, 10_000, 1_600_000
DISC6 = U6**2 - 4 * R6 * PTT6
I6A, I6B = (U6 - math.sqrt(DISC6)) / (2 * R6), (U6 + math.sqrt(DISC6)) / (2 * R6)   # 200 A, 800 A
P6A = U6 * I6A                                   # 2 MW
H6A = PTT6 / P6A                                 # 0,8
DU6A = I6A * R6                                  # 2000 V
UTT6A = U6 - DU6A                                # 8000 V
H62 = 0.95
P62 = PTT6 / H62                                 # ≈ 1,684 MW
PH62 = P62 - PTT6                                # ≈ 84 210 W
I62 = math.sqrt(PH62 / R6)                       # ≈ 91,8 A
U62 = P62 / I62                                  # ≈ 18 353 V
U62F = math.sqrt(PTT6 * R6 / (H62 * (1 - H62)))  # công thức gộp, phải bằng U62
U6SAI = U6 * math.sqrt((1 - H6A) / (1 - H62))    # 20 000 V (cách làm sai của câu c)
X6 = PTT6 * R6 / U6SAI**2                        # H(1−H) ở 20 kV = 0,04
H6SAI = (1 + math.sqrt(1 - 4 * X6)) / 2          # ≈ 95,8 %


# ═════════════ HÌNH: linh kiện dùng chung ═════════════
def rich(s, size=14):
    """Nhãn SVG có chỉ số dưới: 'P_{hp}' → tspan dy."""
    ms = list(re.finditer(r"_\{([^}]+)\}", s))
    if not ms:
        return s
    out = s[:ms[0].start()]
    for k, m in enumerate(ms):
        out += f'<tspan dy="4" font-size="{max(12, size - 2)}">{m.group(1)}</tspan>'
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        out += f'<tspan dy="-4">{s[m.end():nxt]}</tspan>' if s[m.end():nxt] else '<tspan dy="-4"></tspan>'
    return out

def txt(x, y, s, c="currentColor", size=14, anchor="start", weight="700", extra=""):
    size = max(size, 14)                                   # quy ước cỡ chữ: nhãn ≥ 14
    t = lbl(x, y, rich(s, size), c, size, anchor, weight)
    return t.replace("<text ", f"<text {extra} ", 1) if extra else t

def rect(x, y, w, h, c="currentColor", sw=2, fill="none", op=1, rx=0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" '
            f'stroke="{c}" stroke-width="{sw}"/>')

def anim(attr, vals, kts, dur, fmt="{:.1f}", mode=""):
    cm = f' calcMode="{mode}"' if mode else ""
    return (f'<animate attributeName="{attr}" values="{";".join(fmt.format(v) for v in vals)}" '
            f'keyTimes="{";".join(f"{k:.4f}" for k in kts)}"{cm} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def timed(k0, s, x, y, c="currentColor", k1=None, dur=8.0, anchor="start", weight="700"):
    """Nhãn hiện trong [k0, k1] (phân số của dur); k1=None → hiện tới cuối. k0=0 → hiện ngay từ đầu."""
    if k1 is None:
        a = anim("opacity", [0, 1], [0, max(.001, k0)], dur, "{:.0f}", "discrete")
    else:
        a = anim("opacity", [0, 1, 0], [0, max(.001, k0), k1], dur, "{:.0f}", "discrete")
    op = "1" if k0 == 0 else "0"
    return txt(x, y, s, c, 14, anchor, weight, f'opacity="{op}"').replace("</text>", a + "</text>", 1)

def plant(x, y, sub_=None):
    """Nhà máy điện: khối nhà + ống khói; nhãn bên dưới."""
    b = rect(x, y + 14, 66, 40, "currentColor", 2.2, GREY, .18, 3)
    b += rect(x + 46, y - 8, 12, 22, "currentColor", 2, GREY, .18)
    b += txt(x + 33, y + 40, "Nhà máy", "currentColor", 14, "middle", "700")
    if sub_:
        b += txt(x + 33, y + 74, sub_, "currentColor", 14, "middle", "600")
    return b

def xfmr(cx, cy, c="currentColor", op=1, label=None, ly=None):
    """Kí hiệu máy biến áp: hai vòng tròn chồng nhau."""
    g = (f'<circle cx="{cx - 7}" cy="{cy}" r="12" fill="none" stroke="{c}" stroke-width="2.2"/>'
         f'<circle cx="{cx + 7}" cy="{cy}" r="12" fill="none" stroke="{c}" stroke-width="2.2"/>')
    if label:
        g += txt(cx, ly if ly is not None else cy - 20, label, c, 14, "middle", "700")
    return g

def house(x, yb, c="currentColor"):
    return (f'<path d="M{x},{yb} L{x},{yb - 24} L{x + 16},{yb - 38} L{x + 32},{yb - 24} L{x + 32},{yb} Z" fill="{GREY}" '
            f'fill-opacity=".18" stroke="{c}" stroke-width="2.2"/>' + rect(x + 11, yb - 14, 10, 14, c, 1.6))

Y1, Y2 = 92, 112                                     # hai dây của đường dây

def wires(x1, x2):
    return seg(x1, Y1, x2, Y1, "currentColor", 2.4) + seg(x1, Y2, x2, Y2, "currentColor", 2.4)

def glow(x1, x2, ops, kts, dur):
    """Dải đỏ phủ lên dây: độ đậm = mức nóng (định tính)."""
    a = anim("opacity", ops, kts, dur, "{:.2f}")
    return "".join(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{RED}" stroke-width="11" stroke-linecap="round" '
                   f'opacity="{ops[0]:.2f}">{a}</line>' for y in (Y1, Y2))

def osc(x1, x2, amps, kts, dur, f=1.5, n=200):
    """Chấm cam trên dây dao động qua lại (dòng xoay chiều); biên độ theo tỉ lệ cường độ dòng điện, nội suy giữa các mốc."""
    vals = []
    for i in range(n + 1):
        t = i / n
        for j in range(len(kts) - 1):
            if kts[j] <= t <= kts[j + 1]:
                u = (t - kts[j]) / (kts[j + 1] - kts[j]) if kts[j + 1] > kts[j] else 0
                A_ = amps[j] + (amps[j + 1] - amps[j]) * u
                break
        vals.append(A_ * math.sin(2 * math.pi * f * t * dur))
    a = (f'<animate attributeName="stroke-dashoffset" values="{";".join(f"{v:.1f}" for v in vals)}" dur="{dur:.2f}s" '
         f'begin="indefinite" fill="freeze"/>')
    return "".join(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{ORG}" stroke-width="5" stroke-dasharray="0.1 16" '
                   f'stroke-linecap="round">{a}</line>' for y in (Y1, Y2))

def lamp(cx, cy, ops=None, kts=None, dur=8.0):
    """Bóng đèn ở khu dân cư; độ sáng (định tính) theo ops."""
    a = anim("opacity", ops, kts, dur, "{:.2f}") if ops else ""
    o0 = f"{ops[0]:.2f}" if ops else "1"
    b = f'<circle cx="{cx}" cy="{cy}" r="17" fill="{YEL}" opacity="{o0}">{a}</circle>'
    b += f'<circle cx="{cx}" cy="{cy}" r="10" fill="none" stroke="currentColor" stroke-width="2"/>'
    b += rect(cx - 5, cy + 10, 10, 8, "currentColor", 1.6)
    return b


# ═════════════ HÌNH TỪNG DẠNG ═════════════
# ───────────── Dạng 4 · tăng U giảm hao phí ─────────────
def d4(kk):
    b = ""
    if kk == 0:
        TT = 9.0
        b += timed(0, "U = 15 kV ở đầu đường dây", 16, 22, ORG, .47, TT)
        b += timed(.53, "U = 60 kV ở đầu đường dây", 16, 22, BLUE, None, TT)
        b += timed(0, "dây nóng nhiều", 150, 146, RED, .47, TT)
        b += timed(.53, "dây nóng ít hơn hẳn", 150, 146, RED, None, TT)
        b += plant(14, 66) + xfmr(110, 102, "currentColor", 1, "tăng áp", 72)
        b += seg(80, 102, 98, 102, "currentColor", 2.4)
        b += glow(128, 352, [.75, .75, .05, .05], [0, .47, .53, 1], TT)
        b += wires(128, 352) + seg(128, Y1, 122, 102, "currentColor", 2) + seg(128, Y2, 122, 102, "currentColor", 2)
        b += osc(128, 352, [12, 12, 3, 3], [0, .47, .53, 1], TT)        # biên độ ∝ I: 40 A → 10 A
        b += seg(352, Y1, 362, Y1, "currentColor", 2.4) + seg(352, Y2, 362, Y2, "currentColor", 2.4)
        b += house(364, 124) + house(388, 124)
        b += txt(240, 176, "P = 600 kW không đổi", "currentColor", 14, "middle", "600")
        b += txt(240, 198, "R = 24 Ω (cả hai dây)", "currentColor", 14, "middle", "600")
        b += txt(240, 222, "P_{hp} = ?", RED, 14, "middle", "700")
        return fig("c08-4-0", "0 0 420 232",
                   "Đường dây từ nhà máy qua máy tăng áp tới khu dân cư: ở 15 kV dây nóng nhiều, nâng lên 60 kV dây nóng ít hơn hẳn",
                   b, "Mô phỏng: chấm cam là electron dao động qua lại trong dây (dòng xoay chiều), biên độ theo tỉ lệ cường độ dòng điện. "
                      "Dải đỏ chỉ mức nóng của dây, không ghi số. " + NOTE)
    # hình dữ kiện
    b += plant(14, 66, "P = 600 kW") + xfmr(110, 102) + txt(86, 64, "U = 15 kV → 60 kV", "currentColor", 14, "start", "700")
    b += seg(80, 102, 98, 102, "currentColor", 2.4)
    b += wires(128, 352) + seg(128, Y1, 122, 102, "currentColor", 2) + seg(128, Y2, 122, 102, "currentColor", 2)
    b += seg(352, Y1, 362, Y1, "currentColor", 2.4) + seg(352, Y2, 362, Y2, "currentColor", 2.4)
    b += house(364, 124) + house(388, 124)
    b += txt(300, 84, "R = 24 Ω (tổng)", "currentColor", 14, "middle", "700")
    b += txt(240, 132, "P_{hp} = RI² = ?", RED, 14, "middle", "700")
    b += txt(16, 178, "c) P_{hp} ≤ 1 % P → U_{min} = ?", RED, 14, "start", "700")
    b += txt(16, 202, "d) giữ 15 kV, dây cùng chất, cùng dài:", "currentColor", 14, "start", "600")
    b += txt(16, 222, "S' = ? · S", RED, 14, "start", "700")
    return fig("c08-4-2", "0 44 420 188",
               "Sơ đồ: nhà máy công suất 600 kilôoát, máy tăng áp từ 15 lên 60 kilôvôn, đường dây điện trở tổng 24 ôm, khu dân cư",
               b, "Dữ kiện: P là công suất ở đầu đường dây, R là điện trở tổng của cả hai dây. " + NOTE)


# ───────────── Dạng 5 · đường dây nhôm 20 km ─────────────
def d5(kk):
    b = ""
    if kk == 0:
        TT = 9.0
        b += timed(0, "Nối thẳng: truyền ở 6 kV", 16, 22, ORG, .47, TT)
        b += timed(.53, "Qua máy tăng áp: U = ?", 16, 22, BLUE, None, TT)
        b += plant(14, 66)
        # máy tăng áp hiện ra ở nửa sau
        b += (f'<g opacity="0">{xfmr(110, 102, BLUE, 1, "tăng áp", 72)}'
              f'{anim("opacity", [0, 1], [0, .53], TT, "{:.0f}", "discrete")}</g>')
        b += seg(80, 102, 98, 102, "currentColor", 2.4)
        b += glow(128, 330, [.85, .85, .07, .07], [0, .47, .53, 1], TT)
        b += wires(128, 330) + seg(128, Y1, 122, 102, "currentColor", 2) + seg(128, Y2, 122, 102, "currentColor", 2)
        b += osc(128, 330, [14, 14, 2.1, 2.1], [0, .47, .53, 1], TT)    # biên độ ∝ I: 333 A → 50 A
        b += seg(330, Y1, 342, Y1, "currentColor", 2.4) + seg(330, Y2, 342, Y2, "currentColor", 2.4)
        b += house(344, 124) + lamp(398, 96, [.12, .12, .95, .95], [0, .47, .53, 1], TT)
        b += dim("o", "o", 128, 140, 330, 140, "", 0, 0)
        b += txt(229, 162, "20 km, dây đôi bằng nhôm", "currentColor", 14, "middle", "600")
        b += timed(0, "đèn ở khu dân cư gần như tắt", 16, 200, RED, .47, TT)
        b += timed(.53, "dây ít nóng, đèn sáng", 16, 200, GRN, None, TT)
        return fig("c08-5-0", "0 0 420 214",
                   "Nhà máy nối thẳng vào đường dây 20 km: dây rất nóng, đèn ở khu dân cư gần như tắt; thêm máy tăng áp thì dây ít nóng, đèn sáng",
                   b, "Mô phỏng: dải đỏ chỉ mức nóng của dây, độ sáng của đèn chỉ mang tính định tính; khung cuối không ghi đáp số. " + NOTE)
    # hình dữ kiện
    b += plant(8, 66, "2 MW, 6 kV")
    b += xfmr(104, 102) + txt(104, 52, "N_{1} = 300", "currentColor", 14, "middle", "700") + txt(104, 72, "N_{2} = ?", RED, 14, "middle", "700")
    b += seg(74, 102, 92, 102, "currentColor", 2.4)
    b += wires(122, 318) + seg(122, Y1, 116, 102, "currentColor", 2) + seg(122, Y2, 116, 102, "currentColor", 2)
    b += seg(318, Y1, 324, 102, "currentColor", 2) + seg(318, Y2, 324, 102, "currentColor", 2)
    b += xfmr(336, 102) + txt(336, 52, "hạ áp", "currentColor", 14, "middle", "700") + txt(336, 72, "N_{3}/N_{4} = ?", RED, 14, "middle", "700")
    b += seg(348, 102, 366, 102, "currentColor", 2.4) + house(368, 124)
    b += txt(384, 146, "400 V", "currentColor", 14, "middle", "700")
    b += txt(220, 84, "2 × 20 km nhôm", "currentColor", 14, "middle", "600")
    b += txt(220, 132, "S = 70 mm² mỗi dây", "currentColor", 14, "middle", "600")
    b += txt(16, 186, "P_{hp} ≤ 2 % P → U_{min} = ?", RED, 14, "start", "700")
    b += txt(16, 210, "chỉ dùng 22 kV → S_{min} = ?", RED, 14, "start", "700")
    return fig("c08-5-2", "0 34 420 188",
               "Sơ đồ: nhà máy 2 megaoát 6 kilôvôn, máy tăng áp 300 vòng sơ cấp, dây đôi nhôm 20 kilômét tiết diện 70 milimét vuông, máy hạ áp về 400 vôn",
               b, "Dữ kiện: dây đôi nên tổng chiều dài dây gấp đôi khoảng cách; các máy biến áp lí tưởng. " + NOTE)


# ───────────── Dạng 6 · giữ công suất nơi tiêu thụ ─────────────
def d6(kk):
    b = ""
    if kk == 0:
        TT = 9.0
        b += timed(0, "U = 10 kV ở đầu đường dây", 16, 22, ORG, .47, TT)
        b += timed(.53, "Tăng U để H = 95 %: U = ?", 16, 22, BLUE, None, TT)
        b += txt(404, 50, "Nơi tiêu thụ luôn nhận 1,6 MW", GRN, 14, "end", "700")
        b += plant(14, 66)
        b += seg(80, 102, 122, 102, "currentColor", 2.4)
        b += glow(128, 330, [.6, .6, .1, .1], [0, .47, .53, 1], TT)
        b += wires(128, 330) + seg(128, Y1, 122, 102, "currentColor", 2) + seg(128, Y2, 122, 102, "currentColor", 2)
        b += osc(128, 330, [12, 12, 5.5, 5.5], [0, .47, .53, 1], TT)    # biên độ ∝ I: 200 A → 91,8 A
        b += seg(330, Y1, 342, Y1, "currentColor", 2.4) + seg(330, Y2, 342, Y2, "currentColor", 2.4)
        b += house(344, 124) + lamp(398, 96)
        b += txt(229, 150, "R = 10 Ω (cả hai dây)", "currentColor", 14, "middle", "600")
        b += txt(229, 176, "I = ?", RED, 14, "middle", "700")
        b += txt(16, 204, "đèn sáng như nhau ở cả hai lúc", "currentColor", 14, "start", "600")
        return fig("c08-6-0", "0 0 420 214",
                   "Đường dây có nơi tiêu thụ luôn nhận 1,6 megaoát: ở 10 kilôvôn dây nóng, tăng hiệu điện thế thì dây ít nóng mà đèn vẫn sáng như cũ",
                   b, "Mô phỏng: chấm cam dao động với biên độ theo tỉ lệ cường độ dòng điện; dải đỏ chỉ mức nóng của dây, không ghi số. " + NOTE)
    # hình dữ kiện
    b += plant(14, 66, "P = UI = ?")
    b += seg(80, 102, 122, 102, "currentColor", 2.4)
    b += wires(128, 330) + seg(128, Y1, 122, 102, "currentColor", 2) + seg(128, Y2, 122, 102, "currentColor", 2)
    b += seg(330, Y1, 352, Y1, "currentColor", 2.4) + seg(330, Y2, 352, Y2, "currentColor", 2.4)
    b += house(354, 124)
    b += txt(122, 70, "U = 10 kV", "currentColor", 14, "middle", "700")
    b += txt(229, 84, "R = 10 Ω", "currentColor", 14, "middle", "700")
    b += txt(229, 132, "I = ?", RED, 14, "middle", "700")
    b += txt(404, 146, "P_{tt} = 1,6 MW", GRN, 14, "end", "700")
    b += txt(16, 182, "P = P_{tt} + P_{hp}", "currentColor", 14, "start", "700")
    b += txt(16, 206, "b) giữ P_{tt}, H = 95 % → U_{2} = ?", RED, 14, "start", "700")
    return fig("c08-6-2", "0 44 420 174",
               "Sơ đồ: hiệu điện thế 10 kilôvôn ở đầu dây, điện trở dây 10 ôm, nơi tiêu thụ nhận 1,6 megaoát; công suất đầu dây chưa biết",
               b, "Dữ kiện: công suất cho trước là của NƠI TIÊU THỤ, không phải ở đầu đường dây. " + NOTE)


BUILD = [d4, d5, d6]

# ═════════════ ĐỀ ═════════════
DANG = [
dict(label="Dạng 4 · Trung bình · Mở rộng HSG: Hao phí khi truyền tải và tác dụng của việc tăng hiệu điện thế",
     topic=T_BA,
     problem_html=r"""<p>Một nhà máy truyền đi công suất $P=600\ \text{kW}$ (đo ở đầu đường dây) trên một đường dây có điện trở tổng cộng (cả hai dây) $R=24\ \Omega$. Công suất truyền đi luôn giữ không đổi; coi công suất của dòng điện xoay chiều bằng $UI$.</p><ol type="a"><li>Hiệu điện thế ở đầu đường dây là $15\ \text{kV}$. Tính cường độ dòng điện trên dây, công suất hao phí và hiệu suất truyền tải.</li><li>Dùng máy tăng áp nâng hiệu điện thế ở đầu đường dây lên $60\ \text{kV}$. Công suất hao phí giảm bao nhiêu lần? Hiệu suất truyền tải khi đó bằng bao nhiêu?</li><li>Phải đặt ở đầu đường dây hiệu điện thế tối thiểu bằng bao nhiêu để công suất hao phí không vượt quá $1\,\%$ công suất truyền đi? Hiệu điện thế này gấp ít nhất mấy lần $15\ \text{kV}$?</li><li>Một phương án khác: vẫn dùng $15\ \text{kV}$, thay đường dây bằng dây cùng chất, cùng chiều dài nhưng to hơn, sao cho công suất hao phí giảm đúng bằng số lần như ở câu b. Tiết diện và khối lượng dây mới gấp mấy lần dây cũ? So sánh hai phương án.</li></ol>"""),
dict(label="Dạng 5 · Nâng cao · Mở rộng HSG: Đường dây thật — điện trở từ ρ, độ giảm thế, chọn máy tăng áp và máy hạ áp",
     topic=T_BA,
     problem_html=r"""<p>Một nhà máy phát điện có công suất $2\ \text{MW}$, hiệu điện thế ở hai cực máy phát là $6\ \text{kV}$. Điện được đưa tới một khu dân cư cách nhà máy $20\ \text{km}$ bằng đường dây đôi bằng nhôm, mỗi dây có tiết diện $70\ \text{mm}^2$. Điện trở suất của nhôm là $2{,}8\cdot10^{-8}\ \Omega\cdot\text{m}$. Các máy biến áp coi là lí tưởng; coi công suất của dòng điện xoay chiều bằng $UI$; toàn bộ công suất của máy phát được đưa lên đường dây.</p><ol type="a"><li>Tính điện trở của đường dây. Nếu nối thẳng máy phát vào đường dây (truyền ở $6\ \text{kV}$), tính công suất hao phí và hiệu điện thế ở khu dân cư. Nhận xét.</li><li>Để công suất hao phí không quá $2\,\%$ công suất truyền đi, người ta đặt máy tăng áp ở nhà máy. Tính hiệu điện thế tối thiểu ở đầu đường dây. Cuộn sơ cấp của máy tăng áp có $300$ vòng; cuộn thứ cấp phải có ít nhất bao nhiêu vòng?</li><li>Dùng đúng hiệu điện thế tối thiểu ở câu b. Tính cường độ dòng điện, công suất hao phí và hiệu điện thế ở cuối đường dây. Ở khu dân cư đặt máy hạ áp đưa hiệu điện thế về $400\ \text{V}$; tìm tỉ số $N_3/N_4$ giữa số vòng cuộn sơ cấp và cuộn thứ cấp của máy hạ áp.</li><li>Nếu chỉ được dùng hiệu điện thế $22\ \text{kV}$ ở đầu đường dây mà vẫn đòi công suất hao phí không quá $2\,\%$, thì tiết diện mỗi dây nhôm phải ít nhất bằng bao nhiêu?</li></ol>"""),
dict(label="Dạng 6 · Vận dụng cao · Mở rộng HSG: Cho công suất nơi tiêu thụ — phương trình bậc hai và bẫy “công suất không đổi”",
     topic=T_BA,
     problem_html=r"""<p>Một đường dây tải điện có điện trở tổng cộng (cả hai dây) $R=10\ \Omega$. Hiệu điện thế ở đầu đường dây là $U=10\ \text{kV}$. Nơi tiêu thụ ở cuối đường dây cần nhận công suất $P_{\text{tt}}=1{,}6\ \text{MW}$. Đường dây được thiết kế để hiệu suất truyền tải lớn hơn $50\,\%$. Coi công suất của dòng điện xoay chiều bằng $UI$.</p><ol type="a"><li>Tính cường độ dòng điện trên dây (giải thích cách chọn nghiệm), công suất ở đầu đường dây, hiệu suất truyền tải và hiệu điện thế ở nơi tiêu thụ.</li><li>Nơi tiêu thụ vẫn nhận đúng $1{,}6\ \text{MW}$ nhưng muốn hiệu suất truyền tải đạt $95\,\%$. Hiệu điện thế ở đầu đường dây phải bằng bao nhiêu?</li><li>Một bạn giải câu b bằng công thức $\dfrac{U_2}{U_1}=\sqrt{\dfrac{1-H_1}{1-H_2}}$. Bạn đó tìm được bao nhiêu? Chỉ ra chỗ sai trong cách làm này.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 1 nguyên văn đề ; cột 2 chỉ dữ liệu có trong đề ; cột 3 kiến thức + câu hỏi gợi) ═════════════
ANALYSIS = [
 # Dạng 4
 [(r'"truyền đi công suất $P=600\ \text{kW}$"', r"$P=600\ \text{kW}$ (ở đầu đường dây)", r"Công suất truyền đi : $P=UI$ ⇒ $I=\dfrac{P}{U}$"),
  (r'"điện trở tổng cộng (cả hai dây) $R=24\ \Omega$"', r"$R=24\ \Omega$", r"⚠ $R$ đã tính cho cả hai dây, không nhân đôi nữa. Hao phí : $P_{\text{hp}}=RI^2$"),
  (r'"Công suất truyền đi luôn giữ không đổi"', r"$P$ không đổi", r"⚠ điều kiện để so sánh : cùng $P$, cùng $R$ thì $P_{\text{hp}}=\dfrac{P^2R}{U^2}$ chỉ còn phụ thuộc $U$"),
  (r'"Hiệu điện thế ở đầu đường dây là $15\ \text{kV}$"', r"$U=15\ \text{kV}=15\,000\ \text{V}$", r"$U$ ở đầu dây, không phải hiệu điện thế giữa hai đầu điện trở dây"),
  (r'"công suất hao phí và hiệu suất truyền tải"', r"$P_{\text{hp}}=?$ ; $H=?$", r"$H=1-\dfrac{P_{\text{hp}}}{P}$"),
  (r'"nâng hiệu điện thế ở đầu đường dây lên $60\ \text{kV}$"', r"$U'=60\ \text{kV}$", r"$U$ tăng mấy lần ? Khi đó $I$ giảm mấy lần ? $P_{\text{hp}}$ tỉ lệ với $I$ hay với $I^2$ ?"),
  (r'"công suất hao phí không vượt quá $1\,\%$ công suất truyền đi"', r"$P_{\text{hp}}\le0{,}01\,P$ ; $U_{\min}=?$", r"$\dfrac{P^2R}{U^2}\le0{,}01\,P$"),
  (r'"thay đường dây bằng dây cùng chất, cùng chiều dài nhưng to hơn"', r"cùng $\rho$, cùng $\ell$ ; $S'=?$", r"$R=\rho\dfrac{\ell}{S}$ ; khối lượng dây $m=D\ell S$")],
 # Dạng 5
 [(r'"Một nhà máy phát điện có công suất $2\ \text{MW}$, hiệu điện thế ở hai cực máy phát là $6\ \text{kV}$"', r"$P=2\cdot10^6\ \text{W}$ ; $U_0=6000\ \text{V}$", r"Qua máy biến áp lí tưởng, công suất không đổi"),
  (r'"cách nhà máy $20\ \text{km}$ bằng đường dây đôi"', r"$\ell=20\ \text{km}=2\cdot10^4\ \text{m}$", r"⚠ dây đôi : tổng chiều dài dây là $2\ell$"),
  (r'"mỗi dây có tiết diện $70\ \text{mm}^2$. Điện trở suất của nhôm là $2{,}8\cdot10^{-8}\ \Omega\cdot\text{m}$"', r"$S=70\cdot10^{-6}\ \text{m}^2$ ; $\rho=2{,}8\cdot10^{-8}\ \Omega\cdot\text{m}$", r"$R=\rho\dfrac{2\ell}{S}$ ; đổi $1\ \text{mm}^2=10^{-6}\ \text{m}^2$"),
  (r'"Các máy biến áp coi là lí tưởng"', r"không hao phí trong máy", r"⚠ dùng được $\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}$ và công suất qua máy giữ nguyên"),
  (r'"nối thẳng máy phát vào đường dây (truyền ở $6\ \text{kV}$)"', r"$U=U_0$", r"$I=\dfrac{P}{U}$ ; $P_{\text{hp}}=RI^2$ ; $U_{\text{tt}}=U-IR$"),
  (r'"công suất hao phí không quá $2\,\%$ công suất truyền đi"', r"$P_{\text{hp}}\le0{,}02\,P$ ; $U_{\min}=?$", r"$\dfrac{PR}{U^2}\le0{,}02$"),
  (r'"Cuộn sơ cấp của máy tăng áp có $300$ vòng"', r"$N_1=300$ ; $N_2=?$", r"$N_2=N_1\dfrac{U}{U_0}$"),
  (r'"đặt máy hạ áp đưa hiệu điện thế về $400\ \text{V}$"', r"$U_4=400\ \text{V}$ ; $\dfrac{N_3}{N_4}=?$", r"⚠ máy hạ áp nhận hiệu điện thế ở CUỐI đường dây, đã bị giảm $\Delta U=IR$"),
  (r'"chỉ được dùng hiệu điện thế $22\ \text{kV}$ ở đầu đường dây"', r"$U=22\ \text{kV}$ ; $S_{\min}=?$", r"Từ điều kiện $2\,\%$ ra $R_{\max}$, rồi $S=\rho\dfrac{2\ell}{R}$")],
 # Dạng 6
 [(r'"điện trở tổng cộng (cả hai dây) $R=10\ \Omega$"', r"$R=10\ \Omega$", r"Hao phí : $P_{\text{hp}}=RI^2$"),
  (r'"Hiệu điện thế ở đầu đường dây là $U=10\ \text{kV}$"', r"$U=10^4\ \text{V}$", r"Công suất ở đầu dây : $P=UI$"),
  (r'"Nơi tiêu thụ ở cuối đường dây cần nhận công suất $P_{\text{tt}}=1{,}6\ \text{MW}$"', r"$P_{\text{tt}}=1{,}6\cdot10^6\ \text{W}$", r"⚠ đây là công suất ở CUỐI dây, không phải $P$ : $P=P_{\text{tt}}+P_{\text{hp}}$"),
  (r'"Đường dây được thiết kế để hiệu suất truyền tải lớn hơn $50\,\%$"', r"$H\gt50\,\%$", r"⚠ giả thiết dùng để chọn nghiệm khi phương trình cho hai giá trị của $I$"),
  (r'"giải thích cách chọn nghiệm"', r"phương trình có hai nghiệm", r"Tính $H$ ứng với từng nghiệm, so với giả thiết $H\gt50\,\%$"),
  (r'"Nơi tiêu thụ vẫn nhận đúng $1{,}6\ \text{MW}$ nhưng muốn hiệu suất truyền tải đạt $95\,\%$"', r"$P_{\text{tt}}$ giữ nguyên ; $H_2=0{,}95$ ; $U_2=?$", r"⚠ giữ $P_{\text{tt}}$ nên $P=\dfrac{P_{\text{tt}}}{H}$ thay đổi theo $H$"),
  (r'"bằng công thức $\dfrac{U_2}{U_1}=\sqrt{\dfrac{1-H_1}{1-H_2}}$"', r"công thức của bạn", r"Công thức này suy từ $1-H=\dfrac{PR}{U^2}$ khi đại lượng nào giữ không đổi ?")],
]

# ═════════════ LỜI GIẢI ═════════════
R4_ = [r"<strong>Hao phí trên dây:</strong> dây nóng lên, $P_{\text{hp}}=RI^2$ (định luật Joule–Lenz).",
       r"<strong>Dòng trên dây:</strong> $I=\dfrac{P}{U}$, với $P$ và $U$ ở đầu đường dây.",
       r"<strong>Gộp lại:</strong> $P_{\text{hp}}=\dfrac{P^2R}{U^2}$ ; hiệu suất $H=1-\dfrac{P_{\text{hp}}}{P}$.",
       r"<strong>Điện trở dây:</strong> $R=\rho\dfrac{\ell}{S}$ ; khối lượng dây $m=D\ell S$.",
       r"<strong>Điều kiện:</strong> $P$ không đổi, cùng đường dây ; bỏ qua hệ số công suất."]
R5_ = [r"<strong>Điện trở đường dây đôi:</strong> $R=\rho\dfrac{2\ell}{S}$, $\ell$ là khoảng cách.",
       r"<strong>Truyền tải:</strong> $I=\dfrac{P}{U}$ ; $P_{\text{hp}}=RI^2$.",
       r"<strong>Độ giảm thế:</strong> $\Delta U=IR$ ; $U_{\text{tt}}=U-\Delta U$.",
       r"<strong>Máy biến áp:</strong> $\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}$.",
       r"<strong>Điều kiện:</strong> máy biến áp lí tưởng ; $1\ \text{mm}^2=10^{-6}\ \text{m}^2$."]
R6_ = [r"<strong>Cân bằng công suất:</strong> $P=UI=P_{\text{tt}}+P_{\text{hp}}$, với $P_{\text{hp}}=RI^2$.",
       r"<strong>Hiệu suất:</strong> $H=\dfrac{P_{\text{tt}}}{P}=1-\dfrac{P_{\text{hp}}}{P}$.",
       r"<strong>Hệ quả:</strong> $1-H=\dfrac{P_{\text{hp}}}{P}=\dfrac{PR}{U^2}$.",
       r"<strong>Phương trình bậc hai</strong> $aI^2+bI+c=0$ : $I=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$.",
       r"<strong>Điều kiện:</strong> đề giữ $P_{\text{tt}}$ không đổi, nên $P$ ở đầu dây thay đổi khi đổi $U$."]

SOLS = [
 sol(R4_, [
  ("Cường độ dòng điện ở 15 kV", [P(r"Dòng trên dây do công suất truyền đi quyết định :"),
     M(r"I=\dfrac{P}{U}=\dfrac{600\,000}{15\,000}"), A(r"I=40\ \text{A}")]),
  ("Công suất hao phí ở 15 kV", [M(r"P_{\text{hp}}=RI^2=24\cdot40^2"), A(r"P_{\text{hp}}=38\,400\ \text{W}=38{,}4\ \text{kW}")]),
  ("Hiệu suất ở 15 kV", [M(r"H=1-\dfrac{P_{\text{hp}}}{P}=1-\dfrac{38{,}4}{600}"), A(r"H=0{,}936=93{,}6\,\%")]),
  ("Hao phí khi nâng lên 60 kV", [P(r"$U$ tăng $\dfrac{60}{15}=4$ lần nên $I$ giảm $4$ lần :"),
     M(r"I'=\dfrac{600\,000}{60\,000}=10\ \text{A}"), M(r"P'_{\text{hp}}=24\cdot10^2=2400\ \text{W}"),
     M(r"\dfrac{P_{\text{hp}}}{P'_{\text{hp}}}=\dfrac{38\,400}{2400}=16=4^2"),
     M(r"H'=1-\dfrac{2{,}4}{600}=0{,}996=99{,}6\,\%"), A(r"\text{hao phí giảm }16\text{ lần}")]),
  ("Hiệu điện thế tối thiểu", [P(r"Điều kiện hao phí không quá $1\,\%$ :"),
     M(r"\dfrac{P^2R}{U^2}\le0{,}01\,P\ \Rightarrow\ U\ge\sqrt{\dfrac{PR}{0{,}01}}"),
     M(r"U_{\min}=\sqrt{\dfrac{600\,000\cdot24}{0{,}01}}=\sqrt{1{,}44\cdot10^9}\approx37\,947\ \text{V}"),
     M(r"\dfrac{U_{\min}}{15\ \text{kV}}\approx2{,}53"), A(r"U_{\min}\approx37{,}9\ \text{kV}")]),
  ("Tiết diện dây nếu giữ 15 kV", [P(r"Giữ $P$ và $U$ thì $I=40\ \text{A}$ không đổi ; muốn $P_{\text{hp}}=RI^2$ giảm $16$ lần thì $R$ giảm $16$ lần :"),
     M(r"R'=\dfrac{24}{16}=1{,}5\ \Omega"),
     P(r"Cùng $\rho$, cùng $\ell$ : $S$ tỉ lệ nghịch với $R$ ; khối lượng $m=D\ell S$ tỉ lệ thuận với $S$ :"),
     M(r"\dfrac{S'}{S}=\dfrac{R}{R'}=16"), A(r"S'=16\,S\ ;\ m'=16\,m")]),
  ("Kiểm tra", [P(r"Đơn vị : $\Omega\cdot\text{A}^2=\text{W}$ ✓."),
     P(r"Tăng $U$ lên $4$ lần thì hao phí giảm $4^2=16$ lần, không phải $4$ lần ✓."),
     P(r"So sánh : tăng $U$ chỉ cần một máy tăng áp ở đầu và một máy hạ áp ở cuối ; tăng tiết diện cần lượng kim loại gấp $16$ lần và cột điện chịu nặng hơn. Vì vậy người ta chọn tăng $U$ ✓.")])],
  [r"a) $I=40\ \text{A}$", r"a) $P_{\text{hp}}=38{,}4\ \text{kW}$", r"a) $H=93{,}6\,\%$",
   r"b) hao phí giảm $16$ lần", r"b) $H'=99{,}6\,\%$",
   r"c) $U_{\min}\approx37{,}9\ \text{kV}$", r"c) gấp ít nhất khoảng $2{,}53$ lần",
   r"d) tiết diện và khối lượng dây gấp $16$ lần ; tăng $U$ có lợi hơn"],
  r"Nhận dạng: thấy <strong>cùng công suất, cùng đường dây, đổi hiệu điện thế</strong> → $P_{\text{hp}}=\dfrac{P^2R}{U^2}$ : tăng $U$ lên $k$ lần thì hao phí giảm $k^2$ lần."),
 sol(R5_, [
  ("Điện trở đường dây", [P(r"Dây đôi nên tổng chiều dài dây là $2\ell=40\ \text{km}$ :"),
     M(r"R=\rho\dfrac{2\ell}{S}=2{,}8\cdot10^{-8}\cdot\dfrac{4\cdot10^4}{70\cdot10^{-6}}"), A(r"R=16\ \Omega")]),
  ("Truyền thẳng ở 6 kV", [M(r"I=\dfrac{P}{U_0}=\dfrac{2\cdot10^6}{6000}\approx333{,}3\ \text{A}"),
     M(r"P_{\text{hp}}=RI^2=16\cdot333{,}3^2\approx1{,}78\cdot10^6\ \text{W}"),
     M(r"\Delta U=IR\approx5333\ \text{V}\ \Rightarrow\ U_{\text{tt}}=6000-5333\approx667\ \text{V}"),
     A(r"P_{\text{hp}}\approx1{,}78\ \text{MW}\ (\approx89\,\%\,P)"),
     P(r"Gần $\tfrac{9}{10}$ công suất biến thành nhiệt trên dây, khu dân cư chỉ còn khoảng $667\ \text{V}$ : không dùng được.")]),
  ("Hiệu điện thế tối thiểu ở đầu đường dây", [M(r"\dfrac{PR}{U^2}\le0{,}02\ \Rightarrow\ U\ge\sqrt{\dfrac{PR}{0{,}02}}"),
     M(r"U_{\min}=\sqrt{\dfrac{2\cdot10^6\cdot16}{0{,}02}}=\sqrt{1{,}6\cdot10^9}"), A(r"U_{\min}=40\,000\ \text{V}=40\ \text{kV}")]),
  ("Số vòng cuộn thứ cấp máy tăng áp", [M(r"\dfrac{N_2}{N_1}=\dfrac{U_{\min}}{U_0}=\dfrac{40\,000}{6000}\approx6{,}67"),
     M(r"N_2=300\cdot\dfrac{40\,000}{6000}"), A(r"N_2\ge2000\ \text{vòng}")]),
  ("Cuối đường dây và máy hạ áp", [M(r"I=\dfrac{2\cdot10^6}{40\,000}=50\ \text{A}"), M(r"P_{\text{hp}}=16\cdot50^2=40\,000\ \text{W}"),
     M(r"\Delta U=IR=50\cdot16=800\ \text{V}"), M(r"U_3=40\,000-800=39\,200\ \text{V}"),
     M(r"\dfrac{N_3}{N_4}=\dfrac{U_3}{U_4}=\dfrac{39\,200}{400}"), A(r"\dfrac{N_3}{N_4}=98")]),
  ("Tiết diện tối thiểu khi chỉ dùng 22 kV", [M(r"\dfrac{PR}{U^2}\le0{,}02\ \Rightarrow\ R\le\dfrac{0{,}02\,U^2}{P}"), M(r"R_{\max}=\dfrac{0{,}02\cdot(22\,000)^2}{2\cdot10^6}=4{,}84\ \Omega"),
     M(r"S\ge\rho\dfrac{2\ell}{R_{\max}}=2{,}8\cdot10^{-8}\cdot\dfrac{4\cdot10^4}{4{,}84}\approx2{,}31\cdot10^{-4}\ \text{m}^2"),
     A(r"S_{\min}\approx231\ \text{mm}^2")]),
  ("Kiểm tra", [P(r"Câu c : $\dfrac{P_{\text{hp}}}{P}=\dfrac{40\ \text{kW}}{2000\ \text{kW}}=2\,\%$, đúng giới hạn ✓."),
     P(r"$\dfrac{\Delta U}{U}=\dfrac{800}{40\,000}=2\,\%$ : với cùng $P$, tỉ lệ sụt thế bằng tỉ lệ hao phí vì $\dfrac{\Delta U}{U}=\dfrac{IR}{U}=\dfrac{PR}{U^2}$ ✓."),
     P(r"$231\ \text{mm}^2$ gấp khoảng $3{,}3$ lần dây $70\ \text{mm}^2$ : dây nặng gấp $3{,}3$ lần, nên dùng $40\ \text{kV}$ có lợi hơn ✓.")])],
  [r"a) $R=16\ \Omega$", r"a) $P_{\text{hp}}\approx1{,}78\ \text{MW}$ ; $U_{\text{tt}}\approx667\ \text{V}$ : không dùng được",
   r"b) $U_{\min}=40\ \text{kV}$", r"b) cuộn thứ cấp ít nhất $2000$ vòng",
   r"c) $I=50\ \text{A}$", r"c) $P_{\text{hp}}=40\ \text{kW}$", r"c) cuối đường dây $39{,}2\ \text{kV}$", r"c) $N_3/N_4=98$",
   r"d) $S_{\min}\approx231\ \text{mm}^2$"],
  r"Nhận dạng: thấy <strong>khoảng cách, tiết diện dây</strong> và <strong>phần trăm hao phí cho phép</strong> → $R=\rho\dfrac{2\ell}{S}$, rồi $U_{\min}=\sqrt{\dfrac{PR}{x}}$, rồi tỉ số vòng ; máy hạ áp nhận $U-IR$."),
 sol(R6_, [
  ("Phương trình cho cường độ dòng điện", [P(r"Công suất ở đầu dây chia thành phần tới nơi tiêu thụ và phần hao phí trên dây :"),
     M(r"UI=P_{\text{tt}}+RI^2"), M(r"10I^2-10\,000\,I+1{,}6\cdot10^6=0"), A(r"I^2-1000\,I+160\,000=0")]),
  ("Giải và chọn nghiệm", [M(r"I=\dfrac{1000\pm\sqrt{1000^2-4\cdot160\,000}}{2}=\dfrac{1000\pm600}{2}"),
     P(r"Hai nghiệm : $200\ \text{A}$ và $800\ \text{A}$. Với $800\ \text{A}$ : $P=8\ \text{MW}$, hao phí $6{,}4\ \text{MW}$, $H=20\,\%\lt50\,\%$ — trái giả thiết của đề, loại. Với $200\ \text{A}$ : $H=80\,\%\gt50\,\%$, nhận."),
     A(r"I=200\ \text{A}")]),
  ("Công suất đầu dây, hiệu suất, hiệu điện thế nơi tiêu thụ", [M(r"P=UI=10\,000\cdot200=2\cdot10^6\ \text{W}"),
     M(r"H=\dfrac{P_{\text{tt}}}{P}=\dfrac{1{,}6}{2}=0{,}8"),
     M(r"\Delta U=IR=2000\ \text{V}\ \Rightarrow\ U_{\text{tt}}=8000\ \text{V}"), A(r"H=80\,\%")]),
  ("Công suất đầu dây khi H = 95 %", [P(r"Nơi tiêu thụ vẫn nhận $1{,}6\ \text{MW}$, nên công suất đầu dây đổi theo $H$ :"),
     M(r"P_2=\dfrac{P_{\text{tt}}}{H_2}=\dfrac{1{,}6\cdot10^6}{0{,}95}"), A(r"P_2\approx1{,}684\ \text{MW}")]),
  ("Hiệu điện thế đầu dây khi H = 95 %", [M(r"P_{\text{hp}2}=P_2-P_{\text{tt}}\approx84\,210\ \text{W}"), M(r"I_2=\sqrt{\dfrac{P_{\text{hp}2}}{R}}\approx91{,}8\ \text{A}"),
     M(r"U_2=\dfrac{P_2}{I_2}=\dfrac{1\,684\,210}{91{,}77}\approx18\,353\ \text{V}"),
     P(r"Cách gộp : từ $1-H=\dfrac{PR}{U^2}$ và $P=\dfrac{P_{\text{tt}}}{H}$ có $U^2=\dfrac{P_{\text{tt}}R}{H(1-H)}$ ; thử với $H_1=0{,}8$ ra đúng $10\ \text{kV}$."),
     A(r"U_2\approx18{,}35\ \text{kV}")]),
  ("Chỗ sai của công thức kia", [M(r"U'=U_1\sqrt{\dfrac{1-0{,}8}{1-0{,}95}}=10\ \text{kV}\cdot\sqrt4=20\ \text{kV}"),
     P(r"Công thức đó suy từ $1-H=\dfrac{PR}{U^2}$ khi <strong>$P$ ở đầu dây giữ nguyên</strong>. Ở đây đề giữ $P_{\text{tt}}$, còn $P$ giảm từ $2\ \text{MW}$ xuống khoảng $1{,}684\ \text{MW}$."),
     P(r"Thử lại ở $20\ \text{kV}$ : $H(1-H)=\dfrac{P_{\text{tt}}R}{U^2}=0{,}04\Rightarrow H\approx95{,}8\,\%$, vượt yêu cầu : dùng máy tăng áp lớn hơn mức cần."),
     A(r"U'=20\ \text{kV}\ (\text{sai})")]),
  ("Kiểm tra", [P(r"$U_2\gt U_1$ thì $I_2\lt I_1$ ✓ ; $P_2\gt P_{\text{tt}}$ ✓."),
     P(r"Câu b và câu c lệch nhau khoảng $1{,}65\ \text{kV}$ chỉ vì giữ đại lượng nào không đổi : đọc kĩ đề giữ $P$ ở đầu dây hay $P_{\text{tt}}$."),
     P(r"Đơn vị : $\sqrt{\text{W}\cdot\Omega}=\sqrt{\text{V}^2}=\text{V}$ ✓.")])],
  [r"a) $I=200\ \text{A}$ (loại nghiệm $800\ \text{A}$ vì khi đó $H=20\,\%\lt50\,\%$)", r"a) $P=2\ \text{MW}$", r"a) $H=80\,\%$", r"a) $U_{\text{tt}}=8\ \text{kV}$",
   r"b) $U_2\approx18{,}35\ \text{kV}$",
   r"c) bạn đó tìm được $20\ \text{kV}$", r"c) sai vì coi công suất ở đầu dây không đổi, trong khi đề giữ công suất nơi tiêu thụ"],
  r"Nhận dạng: thấy <strong>công suất nơi tiêu thụ</strong> cho trước → $UI=P_{\text{tt}}+RI^2$ (bậc hai, lấy nghiệm nhỏ) ; đổi $U$ mà giữ $P_{\text{tt}}$ thì $P=\dfrac{P_{\text{tt}}}{H}$ cũng đổi."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>cùng công suất, tăng hiệu điện thế k lần</b> → <b>hao phí giảm k² lần</b>",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Cường độ dòng điện ở 15 kV", "Cường độ dòng điện trên dây bằng bao nhiêu ampe?", float(I4A), "A", 0.5,
       loi=r"Dùng $I=\dfrac{U}{R}$ : sai vì $U$ là hiệu điện thế ở đầu đường dây, không đặt riêng trên điện trở dây ; dòng do công suất truyền đi quyết định."),
  buoc("Công suất hao phí ở 15 kV", "Công suất hao phí trên dây bằng bao nhiêu kilôoát?", float(PH4A) / 1000, "kW", 0.2,
       loi=r"Tính $\dfrac{U^2}{R}$ với $U$ ở đầu dây : ra lớn hơn cả công suất truyền đi mà không thấy vô lí.",
       ke=[(r"$P_{\text{hp}}=RI^2$", True),
           (r"$P_{\text{hp}}=\dfrac{U^2}{R}$", r"$U$ không đặt riêng trên dây ; cách này cho hao phí lớn hơn cả công suất truyền đi — vô lí."),
           (r"$P_{\text{hp}}=UI$", r"$UI$ là công suất truyền đi $P$, không phải phần biến thành nhiệt trên dây.")]),
  buoc("Hiệu suất ở 15 kV", "Hiệu suất truyền tải bằng bao nhiêu phần trăm?", float(H4A) * 100, "%", 0.1,
       loi=r"Lấy $H=\dfrac{P_{\text{hp}}}{P}$ : đó là tỉ lệ hao phí ; hiệu suất là phần còn lại.",
       ke=[(r"$H=1-\dfrac{P_{\text{hp}}}{P}$", True),
           (r"$H=\dfrac{P_{\text{hp}}}{P}$", r"Đó là phần hao phí, không phải phần tới được nơi tiêu thụ."),
           (r"$H=\dfrac{P-P_{\text{hp}}}{P_{\text{hp}}}$", r"Mẫu số phải là công suất truyền đi $P$.")]),
  buoc("Hao phí khi nâng lên 60 kV", "Ở 60 kV, công suất hao phí giảm bao nhiêu lần so với ở 15 kV?", float(GIAM4), "lần", 0.1,
       loi=r"Thấy $U$ tăng $4$ lần thì nghĩ hao phí giảm $4$ lần : quên $P_{\text{hp}}=RI^2$ tỉ lệ với bình phương cường độ dòng.",
       ke=[(r"$P_{\text{hp}}$ tỉ lệ nghịch với $U^2$ : chia cho $\left(\dfrac{60}{15}\right)^2$", True),
           (r"$P_{\text{hp}}$ tỉ lệ nghịch với $U$ : chia cho $\dfrac{60}{15}$", r"$I$ giảm $k$ lần nhưng $P_{\text{hp}}=RI^2$ nên giảm $k^2$ lần."),
           (r"$P_{\text{hp}}=\dfrac{U^2}{R}$ nên tăng $U$ thì hao phí tăng", r"$U$ không đặt riêng trên dây ; kết luận này trái với lí do người ta dùng điện cao thế.")]),
  buoc("Hiệu điện thế tối thiểu", "Hiệu điện thế tối thiểu ở đầu đường dây bằng bao nhiêu kilôvôn?", U4MIN / 1000, "kV", 0.1,
       loi=r"Quên lấy căn bậc hai, hoặc viết $P_{\text{hp}}\le0{,}01$ (theo oát) thay vì $P_{\text{hp}}\le0{,}01\,P$.",
       ke=[(r"$\dfrac{P^2R}{U^2}\le0{,}01P\Rightarrow U\ge\sqrt{\dfrac{PR}{0{,}01}}$", True),
           (r"$U\ge\dfrac{PR}{0{,}01}$", r"Quên căn : hao phí tỉ lệ nghịch với $U^2$, không phải với $U$."),
           (r"$U\ge\sqrt{\dfrac{P^2R}{0{,}01}}$", r"$1\,\%$ là của $P$ : vế phải phải là $0{,}01\,P$, không phải $0{,}01$.")]),
  buoc("Tiết diện dây nếu giữ 15 kV", "Tiết diện dây mới gấp bao nhiêu lần dây cũ?", float(S4D), "lần", 0.1,
       loi=r"Cho tiết diện chỉ gấp $4$ lần (bằng số lần tăng $U$) : hao phí phải giảm đúng như câu b, mà $I$ không đổi nên $R$ phải giảm cùng số lần đó.",
       ke=[(r"Giữ $I$, nên $R$ giảm cùng số lần với $P_{\text{hp}}$ ; $S$ tỉ lệ nghịch với $R$", True),
           (r"$S$ tỉ lệ thuận với $R$", r"$R=\rho\dfrac{\ell}{S}$ : dây to hơn thì điện trở nhỏ hơn."),
           (r"$S$ gấp bằng số lần tăng $U$ ở câu b", r"Hao phí phải giảm bằng số lần ở câu b, tức $k^2$ lần chứ không phải $k$ lần.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>khoảng cách, tiết diện dây, % hao phí cho phép</b> → <b>R = ρ·2ℓ/S, rồi U tối thiểu, rồi tỉ số vòng</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Điện trở đường dây", "Điện trở của đường dây bằng bao nhiêu ôm?", float(R5), "Ω", 0.1,
       loi=r"Quên dây đôi (chỉ lấy chiều dài bằng khoảng cách) nên ra một nửa ; hoặc không đổi km ra m, $\text{mm}^2$ ra $\text{m}^2$."),
  buoc("Truyền thẳng ở 6 kV", "Truyền thẳng ở 6 kV, công suất hao phí bằng bao nhiêu megaoát?", float(PH5A) / 1e6, "MW", 0.03,
       loi=r"Tính $\dfrac{U^2}{R}$ với $U$ ở đầu dây, ra lớn hơn cả công suất nhà máy mà không thấy vô lí.",
       ke=[(r"$I=\dfrac{P}{U_0}$ rồi $P_{\text{hp}}=RI^2$", True),
           (r"$P_{\text{hp}}=\dfrac{U_0^2}{R}$", r"$U_0$ không đặt riêng trên dây ; cách này cho hao phí lớn hơn cả công suất nhà máy — vô lí."),
           (r"$I=\dfrac{U_0}{R}$ rồi $P_{\text{hp}}=RI^2$", r"$U_0$ là hiệu điện thế ở đầu đường dây, không phải giữa hai đầu điện trở dây ; dòng do $P$ quyết định.")]),
  buoc("Hiệu điện thế tối thiểu ở đầu đường dây", "Hiệu điện thế tối thiểu ở đầu đường dây bằng bao nhiêu kilôvôn?", U5MIN / 1000, "kV", 0.1,
       loi=r"Quên lấy căn bậc hai, hoặc lấy $2\,\%$ theo oát thay vì $2\,\%$ của $P$.",
       ke=[(r"$\dfrac{PR}{U^2}\le0{,}02\Rightarrow U\ge\sqrt{\dfrac{PR}{0{,}02}}$", True),
           (r"$U\ge\dfrac{PR}{0{,}02}$", r"Quên căn : hao phí tỉ lệ nghịch với $U^2$."),
           (r"$U\ge\sqrt{\dfrac{P^2R}{0{,}02}}$", r"$2\,\%$ là của $P$ : phải viết $P_{\text{hp}}\le0{,}02\,P$.")]),
  buoc("Số vòng cuộn thứ cấp máy tăng áp", "Cuộn thứ cấp của máy tăng áp phải có ít nhất bao nhiêu vòng?", N52, "vòng", 1,
       loi=r"Viết ngược $\dfrac{U_1}{U_2}=\dfrac{N_2}{N_1}$ nên ra cuộn thứ cấp ít vòng hơn cuộn sơ cấp — vô lí với máy tăng áp.",
       ke=[(r"$N_2=N_1\dfrac{U}{U_0}$", True),
           (r"$N_2=N_1\dfrac{U_0}{U}$", r"Viết ngược tỉ số : máy tăng áp thì cuộn thứ cấp nhiều vòng hơn cuộn sơ cấp."),
           (r"$\dfrac{N_2}{N_1}=\dfrac{I_2}{I_1}$", r"Với máy biến áp, dòng điện tỉ lệ NGHỊCH với số vòng : $\dfrac{I_1}{I_2}=\dfrac{N_2}{N_1}$.")]),
  buoc("Cuối đường dây và máy hạ áp", "Tỉ số N3/N4 của máy hạ áp bằng bao nhiêu?", float(K5HA), "", 0.5,
       loi=r"Chia hiệu điện thế ở đầu đường dây cho $400\ \text{V}$ : quên độ giảm thế $\Delta U=IR$ trên dây.",
       ke=[(r"Tính $U_3=U-IR$ rồi lấy $\dfrac{U_3}{400\ \text{V}}$", True),
           (r"Lấy hiệu điện thế ở đầu đường dây chia cho $400\ \text{V}$", r"Máy hạ áp đặt ở cuối dây, nhận hiệu điện thế đã giảm $IR$."),
           (r"Lấy $\Delta U=IR$ chia cho $400\ \text{V}$", r"$\Delta U$ là phần hiệu điện thế mất trên dây, không phải hiệu điện thế đặt vào máy hạ áp.")]),
  buoc("Tiết diện tối thiểu khi chỉ dùng 22 kV", "Tiết diện tối thiểu của mỗi dây bằng bao nhiêu milimét vuông?", float(S5MIN), "mm²", 1.5,
       loi=r"Quên dây đôi khi tính $S$ từ $R$, hoặc đổi $\text{m}^2$ ra $\text{mm}^2$ sai (nhân $10^3$ thay vì $10^6$).",
       ke=[(r"$R_{\max}=\dfrac{0{,}02\,U^2}{P}$ rồi $S=\rho\dfrac{2\ell}{R_{\max}}$", True),
           (r"$R_{\max}=\dfrac{0{,}02\,U^2}{P}$ rồi $S=\rho\dfrac{\ell}{R_{\max}}$", r"Quên dây đôi : tổng chiều dài dây là $2\ell$."),
           (r"$R_{\max}=\dfrac{U^2}{0{,}02\,P}$ rồi $S=\rho\dfrac{2\ell}{R_{\max}}$", r"Lật sai bất phương trình : từ $\dfrac{PR}{U^2}\le0{,}02$ ra $R\le\dfrac{0{,}02\,U^2}{P}$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>công suất nơi tiêu thụ</b> cho trước → <b>UI = P_tt + RI²</b>, bậc hai ; đổi U thì P đầu dây đổi",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Phương trình cho cường độ dòng điện", "Phương trình nào đúng cho cường độ dòng điện I trên dây?",
       loi=r"Lấy $I=\dfrac{P_{\text{tt}}}{U}$ : chia công suất ở cuối dây cho hiệu điện thế ở đầu dây, hai đại lượng không cùng một chỗ.",
       lua_chon=[(r"$UI=P_{\text{tt}}+RI^2$", True),
                 (r"$I=\dfrac{P_{\text{tt}}}{U}$", r"$P_{\text{tt}}$ là công suất ở cuối dây, còn $U$ ở đầu dây ; cách này bỏ qua hao phí."),
                 (r"$UI=P_{\text{tt}}-RI^2$", r"Công suất ở đầu dây phải lớn hơn công suất nơi tiêu thụ : hao phí cộng vào, không trừ đi.")]),
  buoc("Giải và chọn nghiệm", "Chọn nghiệm hợp lí: cường độ dòng điện trên dây bằng bao nhiêu ampe?", I6A, "A", 1,
       loi=r"Lấy nghiệm lớn mà không kiểm giả thiết $H\gt50\,\%$, hoặc bỏ hạng $RI^2$ cho dễ giải.",
       ke=[(r"Giải phương trình bậc hai, lấy nghiệm cho $H\gt50\,\%$", True),
           (r"Giải phương trình bậc hai, lấy nghiệm lớn", r"Nghiệm lớn cho hao phí lớn hơn cả công suất nơi tiêu thụ, hiệu suất dưới $50\,\%$ — trái giả thiết của đề."),
           (r"Bỏ $RI^2$ cho gọn rồi lấy $I=\dfrac{P_{\text{tt}}}{U}$", r"Bỏ hao phí là coi dây không có điện trở — trái đề.")]),
  buoc("Công suất đầu dây, hiệu suất, hiệu điện thế nơi tiêu thụ", "Hiệu suất truyền tải bằng bao nhiêu phần trăm?", H6A * 100, "%", 0.5,
       loi=r"Lấy tỉ số hao phí trên công suất nơi tiêu thụ làm hiệu suất.",
       ke=[(r"$H=\dfrac{P_{\text{tt}}}{UI}$", True),
           (r"$H=\dfrac{RI^2}{UI}$", r"Đó là tỉ lệ hao phí, không phải phần tới được nơi tiêu thụ."),
           (r"$H=\dfrac{RI^2}{P_{\text{tt}}}$", r"Đó là hao phí so với phần dùng được, không phải hiệu suất.")]),
  buoc("Công suất đầu dây khi H = 95 %", "Khi hiệu suất là 95 %, công suất ở đầu đường dây bằng bao nhiêu megaoát?", P62 / 1e6, "MW", 0.005,
       loi=r"Giữ nguyên công suất đầu dây của câu a khi đổi $U$ : nhưng đề giữ công suất nơi tiêu thụ.",
       ke=[(r"$P_2=\dfrac{P_{\text{tt}}}{H_2}$", True),
           (r"$P_2$ bằng công suất đầu dây ở câu a", r"Tăng $U$ thì hao phí giảm, nên đầu dây phát ít hơn mà nơi tiêu thụ vẫn nhận đủ."),
           (r"$P_2=H_2\cdot P_{\text{tt}}$", r"Nhân $H$ làm $P_2$ nhỏ hơn $P_{\text{tt}}$ — đầu dây phải lớn hơn nơi tiêu thụ.")]),
  buoc("Hiệu điện thế đầu dây khi H = 95 %", "Hiệu điện thế ở đầu đường dây phải bằng bao nhiêu kilôvôn?", U62 / 1000, "kV", 0.05,
       loi=r"Chia $P_2$ cho cường độ dòng của câu a (dòng đã đổi), hoặc dùng công thức tỉ số căn của câu c.",
       ke=[(r"$P_{\text{hp}2}=P_2-P_{\text{tt}}$, $I_2=\sqrt{\dfrac{P_{\text{hp}2}}{R}}$, rồi $U_2=\dfrac{P_2}{I_2}$", True),
           (r"$U_2=\dfrac{P_2}{I}$ với $I$ của câu a", r"Đổi $U$ thì cường độ dòng cũng đổi ; phải tính lại $I_2$ từ hao phí mới."),
           (r"$U_2=U_1\sqrt{\dfrac{1-H_1}{1-H_2}}$", r"Công thức này giả sử công suất đầu dây không đổi ; ở bài này nó đã thay đổi.")]),
  buoc("Chỗ sai của công thức kia", "Theo công thức của bạn, hiệu điện thế U2 bằng bao nhiêu kilôvôn?", U6SAI / 1000, "kV", 0.05,
       loi=r"Thế nhầm tỉ lệ hao phí vào chỗ hiệu suất, hoặc quên căn bậc hai.",
       ke=[(r"Thế đúng $H_1$, $H_2$ vào công thức bạn dùng", True),
           (r"Thế tỉ lệ hao phí vào chỗ $H_1$, $H_2$", r"Công thức đã có sẵn $1-H$ ; thế nhầm sẽ ra số khác."),
           (r"Bỏ căn : $\dfrac{U_2}{U_1}=\dfrac{1-H_1}{1-H_2}$", r"Công thức bạn dùng có căn bậc hai.")]),
  buoc("Kiểm tra")]),
]


# KaTeX: chỉ số dưới có dấu tiếng Việt → \text{…}
_SUBVN = re.compile(r"_\{([^{}\\]*[^\x00-\x7f][^{}\\]*)\}")
_SUBVN1 = re.compile(r"_([^\x00-\x7f])")
def _tx(x):
    if isinstance(x, str):
        if x.lstrip().startswith("<figure"):
            return x
        x = _SUBVN.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
        return _SUBVN1.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
    if isinstance(x, list):
        return [_tx(v) for v in x]
    if isinstance(x, tuple):
        return tuple(_tx(v) for v in x)
    if isinstance(x, dict):
        return {k: _tx(v) for k, v in x.items()}
    return x
_RAW_DANG, _RAW_ANALYSIS = DANG, ANALYSIS
DANG, ANALYSIS, SOLS, STEPS = _tx(DANG), _tx(ANALYSIS), _tx(SOLS), _tx(STEPS)


def kiem_so():
    def near(a, b, e):
        return abs(float(a) - float(b)) <= e
    def far(a, b, e):
        return abs(float(a) - float(b)) > e
    # D4 (khớp nguon.md / tinh.py)
    assert I4A == 40 and PH4A == 38400 and H4A == F(117, 125) and I4B == 10 and PH4B == 2400 and H4B == F(249, 250)
    assert GIAM4 == 16 and R4D == F(3, 2) and S4D == 16
    assert near(U4MIN, 37947.33, 0.01) and round(U4MIN / 1000, 1) == 37.9 and round(K4, 2) == 2.53
    assert far(U4A / R4, I4A, 0.5)                                                     # b1: I = U/R
    assert U4A**2 / R4 > P4 and far(U4A**2 / R4 / 1000, PH4A / 1000, 0.2) and far(U4A * I4A / 1000, PH4A / 1000, 0.2)   # b2
    assert far(PH4A / P4 * 100, H4A * 100, 0.1) and far((P4 - PH4A) / PH4A * 100, H4A * 100, 0.1)                   # b3
    assert far(U4B / U4A, GIAM4, 0.1)                                                  # b4: giảm k lần
    assert far(P4 * R4 / F(1, 100) / 1000, U4MIN / 1000, 0.1) and far(math.sqrt(float(P4**2 * R4 / F(1, 100))) / 1000, U4MIN / 1000, 0.1)  # b5
    assert far(U4B / U4A, S4D, 0.1) and far(R4D / R4, S4D, 0.1)                        # b6
    # D5
    assert R5 == 16 and near(I5A, 333.33, 0.01) and near(PH5A, 1.7778e6, 100) and near(DU5A, 5333.3, 0.1) and near(UTT5A, 666.7, 0.1)
    assert U5MIN == 40000 and N52 == 2000 and I5C == 50 and PH5C == 40000 and DU5C == 800 and UTT5C == 39200 and K5HA == 98
    assert R5MAX == F(121, 25) and near(S5MIN, 231.4, 0.1) and round(float(S5MIN) / 70, 1) == 3.3
    assert PH5C / P5 == F(2, 100) and DU5C / 40000 == F(2, 100)                         # kiểm tra
    assert U50**2 / R5 > P5 and far((U50 / R5)**2 * R5 / 1e6, PH5A / 1e6, 0.03) and far(U50**2 / R5 / 1e6, PH5A / 1e6, 0.03) and near(1.8, PH5A / 1e6, 0.03)        # b2: hai cách sai
    assert far(P5 * R5 / F(2, 100) / 1000, U5MIN / 1000, 0.1) and far(math.sqrt(float(P5**2 * R5 / F(2, 100))) / 1000, U5MIN / 1000, 0.1)  # b3
    assert far(N51 * U50 / U5MIN, N52, 1) and far(N51 * float(I5C / I5A), N52, 1)      # b4: viết ngược ; dùng tỉ số dòng
    assert far(40000 / 400, K5HA, 0.5) and far(DU5C / 400, K5HA, 0.5)                  # b5
    assert far(S5MIN / 2, S5MIN, 1.5) and far(RHO_AL * 2 * L5 / (U5D**2 / (F(2, 100) * P5)) * 10**6, S5MIN, 1.5)   # b6
    # D6
    assert near(I6A, 200, 1e-9) and near(I6B, 800, 1e-9) and near(P6A, 2e6, 1e-3) and near(H6A, 0.8, 1e-12)
    assert near(UTT6A, 8000, 1e-6) and near(U6 * I6B - R6 * I6B**2, PTT6, 1e-3) and near(U6 * I6A - R6 * I6A**2, PTT6, 1e-3)
    assert near(P62, 1.6842e6, 100) and near(I62, 91.77, 0.01) and near(U62, U62F, 1e-6) and round(U62 / 1000, 2) == 18.35
    assert near(math.sqrt(PTT6 * R6 / (H6A * (1 - H6A))), U6, 1e-6)                    # công thức gộp nghiệm lại câu a
    assert near(U6SAI, 20000, 1e-6) and round(H6SAI * 100, 1) == 95.8
    assert far(PTT6 / U6, I6A, 1) and far(I6B, I6A, 1) and PTT6 / (U6 * I6B) < 0.5 < H6A                                  # b2
    assert far(R6 * I6A**2 / P6A * 100, H6A * 100, 0.5) and far(R6 * I6A**2 / PTT6 * 100, H6A * 100, 0.5)   # b3
    assert far(P6A / 1e6, P62 / 1e6, 0.005) and far(H62 * PTT6 / 1e6, P62 / 1e6, 0.005)                   # b4
    assert far(P62 / I6A / 1000, U62 / 1000, 0.05) and far(U6SAI / 1000, U62 / 1000, 0.05)                 # b5
    assert far(U6 * math.sqrt((1 - .2) / (1 - .05)) / 1000, U6SAI / 1000, 0.05) and far(U6 * (1 - H6A) / (1 - H62) / 1000, U6SAI / 1000, 0.05)  # b6
    # bảng phân tích: cột 1 trích nguyên văn đề
    for n, rows in enumerate(_RAW_ANALYSIS):
        for r in rows:
            assert r[0].strip('"') in _RAW_DANG[n]["problem_html"], (n, r[0])
    # không lộ đáp số trong đề, hình, bảng phân tích, câu hỏi, lựa chọn, lỗi hay gặp
    lo = {0: ["40 A", "38,4", "38{,}4", "38 400", "93,6", "93{,}6", "99,6", "99{,}6", "16", "37,9", "37{,}9", "37 9", "2,53", "2{,}53", "1,5", "1{,}5"],
          1: ["16", "333", "1,78", "1{,}78", "5333", "667", "40 kV", "40\\,000", "40 000", "6,67", "6{,}67", "2000", "50 A", "39", "98", "4,84", "4{,}84", "231", "3,3", "3{,}3"],
          2: ["200", "800", "80", "2 MW", "8 kV", "18,3", "18{,}3", "1,68", "1{,}68", "91,", "91{,}", "20 kV", "95,8", "95{,}8"]}
    for n in range(3):
        figs = re.sub(r"<[^>]+>", " ", BUILD[n](0) + BUILD[n](2))           # chỉ chữ hiện trên hình, bỏ toạ độ
        blob = DANG[n]["problem_html"] + figs + str(ANALYSIS[n]) + STEPS[n]["nhan_dang"]
        for s in STEPS[n]["buoc"]:
            blob += s.get("tieu_de", "") + s.get("hoi", "") + s.get("loi_hay_gap", "")
            for c in s.get("chon_buoc_ke", []) + s.get("lua_chon", []):
                blob += c["text"] + c.get("vi_sao", "")
        for x in lo[n]:
            assert x not in blob, (n, x)
    for n, s in enumerate(STEPS):
        assert s["cap_do"] in (2, 3, 4) and len(s["buoc"]) == SOLS[n].count('class="bt-step"'), n
    assert [s["cap_do"] for s in STEPS] == [2, 3, 4]
    assert "marker-end" not in "".join(BUILD[n](k) for n in range(3) for k in (0, 2))
    print("btm152_d456: kiểm số liệu đạt")


if __name__ == "__main__":
    kiem_so()
