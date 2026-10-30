#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài tắt dần / cưỡng bức / cộng hưởng và thay <!--FIGn--> trong theory.src.html."""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math
from svg_lib import *

# Đầu mũi tên V 30° (thầy chốt 7/10/2026), không marker tam giác. Bản sao chevron của svg_lib skill.
def chevron(x, y, dx, dy, c="currentColor", w=2, L=12, ang=30):
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    t = math.radians(ang)
    pts = []
    for sg in (1, -1):
        c_, s_ = math.cos(t), math.sin(sg * t)
        bx, by = ux * c_ - uy * s_, ux * s_ + uy * c_
        pts.append((x - L * bx, y - L * by))
    (ax, ay), (bx, by) = pts
    return (f'<path d="M{ax:.1f},{ay:.1f} L{x:.1f},{y:.1f} L{bx:.1f},{by:.1f}" fill="none" stroke="{c}" '
            f'stroke-width="{w}" stroke-linejoin="miter" stroke-miterlimit="10"/>')

def defs(prefix):
    return ""

def arrow(p, c, x1, y1, x2, y2, w=3, dash=""):
    col = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}[c]
    ww = min(w, 2.8)
    L = max(6, min(3.4 * ww + 3, 0.5 * math.hypot(x2 - x1, y2 - y1)))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{ww}"{d}/>'
            + chevron(x2, y2, x2 - x1, y2 - y1, col, ww, L))

def poly(pts, c, w=2.2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"{d} points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
            f'stroke-width="{w}"{d} opacity="{op}"/>')

def fig(vb, label, body, cap, exp=None):
    s = wrap(vb, label, body, cap)
    if exp:
        s = s.replace('<figure class="fig" data-tl="1">',
                      f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
    return s

# ---- Hình 1: xích đu đang ĐI XUỐNG (bên trái điểm treo, đang sang phải), nhún cùng chiều chỉ một phần nhịp.
# Góc lệch θ < 0 (bên trái) + đi sang phải ⇒ θ tăng về 0 ⇒ đang đi xuống về đáy (khớp mở bài "nhún lúc đu đi xuống").
PX, PY, L1 = 160.0, 30.0, 170.0

def on_arc(deg, r=L1):
    a = math.radians(deg)
    return PX + r * math.sin(a), PY + r * math.cos(a)

TH = -14.0
sx, sy = on_arc(TH)
tx, ty = math.cos(math.radians(TH)), -math.sin(math.radians(TH))  # tiếp tuyến chiều θ tăng
assert tx > 0 and ty > 0, "đang sang phải và đi xuống"
assert sx < PX, "ghế bên trái điểm treo"
b = ""
b += line(100, 24, 220, 24, "currentColor", 4)
b += line(PX, 24, PX, PY, "currentColor", 2.5)
# vị trí lúc trước (mờ): cao hơn, bên trái
gx, gy = on_arc(-36)
b += line(PX, PY, gx, gy - 4, "currentColor", 1.6, "", 0.35)
b += (f'<rect x="{gx - 17:.1f}" y="{gy - 4:.1f}" width="34" height="8" rx="2" fill="none" '
      f'stroke="currentColor" stroke-width="1.4" opacity="0.35"/>')
# đường đi: cung nét đứt bán kính lớn hơn (dưới ghế), đầu V chỉ chiều đang đi
arc = [on_arc(d, 190) for d in range(-34, -17, 2)]
b += poly(arc, "currentColor", 1.5, "4 4")
ex, ey = on_arc(-18, 190)
b += chevron(ex, ey, math.cos(math.radians(-18)), -math.sin(math.radians(-18)), "currentColor", 1.6, 9)
# dây + ghế
b += line(PX, PY, sx, sy - 4, "currentColor", 2.2)
b += (f'<rect x="{sx - 18:.1f}" y="{sy - 4:.1f}" width="36" height="8" rx="2" '
      f'fill="{ORG}" stroke="currentColor" stroke-width="1.4"/>')
# người ngồi, mặt hướng sang phải (chiều đi)
hipx, hipy = sx - 4, sy - 5
shx, shy = sx - 9, sy - 44
kx, ky = sx + 13, sy - 9
fx, fy = sx + 32, sy - 6  # chân duỗi về phía trước, ngang mặt ghế, không chạm dây
def rope_x(y):
    return PX + (sx - PX) * (y - PY) / (sy - 4 - PY)
hand_y = sy - 36
b += line(hipx, hipy, shx, shy, "currentColor", 3.4).replace("/>", ' stroke-linecap="round"/>')
b += f'<circle cx="{shx - 1:.1f}" cy="{shy - 13:.1f}" r="10" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += line(hipx, hipy, kx, ky, "currentColor", 3.4).replace("/>", ' stroke-linecap="round"/>')
b += line(kx, ky, fx, fy, "currentColor", 3.4).replace("/>", ' stroke-linecap="round"/>')
b += line(shx, shy + 4, rope_x(hand_y), hand_y, "currentColor", 2.4)
# hai mũi tên song song, cùng chiều tiếp tuyến
g0 = (sx - 6, sy - 24)  # gốc ở thân người
r0 = (sx + 19, sy + 2)  # gốc lực nhún ở mép ghế (đặt lên xích đu)
b += arrow("f1", "g", g0[0], g0[1], g0[0] + 120 * tx, g0[1] + 120 * ty, 3)
b += arrow("f1", "r", r0[0], r0[1], r0[0] + 90 * tx, r0[1] + 90 * ty, 3)
gy_at = lambda x: g0[1] + (x - g0[0]) * ty / tx
ry_at = lambda x: r0[1] + (x - r0[0]) * ty / tx
assert ky - gy_at(kx) > 8 and fy - gy_at(fx) > 8 and ry_at(fx) - fy > 8, "mũi tên không đè chân"
b += text(g0[0] + 120 * tx + 10, g0[1] + 120 * ty + 5, "chiều đang đi", GRN, 14, "start", "700")
b += text(r0[0] + 90 * tx + 10, r0[1] + 90 * ty + 8, "nhún cùng chiều", RED, 14, "start", "700")
b += text(246, 254, "chỉ một phần nhịp", "currentColor", 14, "start", "600")
b += text(246, 274, "không đẩy suốt vòng", "currentColor", 14, "start", "600")
fig1 = fig("0 0 440 288",
           "Xích đu bên trái điểm treo đang đi xuống sang phải: lực nhún cùng chiều chuyển động, chỉ một phần nhịp",
           b,
           "Hình 1. Xích đu đang đi xuống: nhún cùng chiều, chỉ một phần nhịp.",
           "tn-l11-tatdan-03")

# ---- Hình 2: biên độ giảm, ba môi trường. Cùng A0, T, chỉ đổi beta.
# x = exp(-beta t) cos(2 pi t), T = 1 s. Đỉnh dương tại t = 0, 1, 2 phải giảm thật.
A0_PX = 40.0
T_END = 3.05
X0, X1 = 52.0, 416.0

def xt(t, beta):
    return math.exp(-beta * t) * math.cos(2 * math.pi * t)

def panel(title, beta, col, y_title, y_top, y_bot):
    mid = (y_top + y_bot) / 2
    out = text(X0, y_title, title, col, 14, "start", "700")
    out += text(X0 - 10, y_top + 12, "x", "currentColor", 14, "end", "700")
    out += line(X0, y_top, X0, y_bot, "currentColor", 1.3, "", 0.55)
    out += line(X0, mid, X1, mid, "currentColor", 1.2, "", 0.45)
    out += text(X1 + 6, mid + 5, "t", "currentColor", 14, "start", "700")
    n = 240
    pts, env_hi, env_lo = [], [], []
    for i in range(n + 1):
        t = T_END * i / n
        x = X0 + (X1 - X0) * t / T_END
        env = math.exp(-beta * t)
        pts.append((x, mid - A0_PX * xt(t, beta)))
        env_hi.append((x, mid - A0_PX * env))
        env_lo.append((x, mid + A0_PX * env))
    out += poly(env_hi, col, 1.2, "5 4")
    out += poly(env_lo, col, 1.2, "5 4")
    out += poly(pts, col, 2.2)
    # kiểm: ba đỉnh dương t = 0, 1, 2 giảm dần, và không điểm nào vượt đỉnh đầu
    peaks = [abs(xt(k, beta)) for k in (0, 1, 2)]
    assert peaks[0] > peaks[1] > peaks[2] > 0, (title, peaks)
    assert max(abs(xt(T_END * i / n, beta)) for i in range(n + 1)) <= peaks[0] + 1e-9
    # đỉnh sau phải thấp hơn đỉnh trước trên hình (pixel y lớn hơn = gần trục hơn)
    y_peaks = [mid - A0_PX * xt(k, beta) for k in (0, 1, 2)]
    assert y_peaks[0] < y_peaks[1] < y_peaks[2], (title, y_peaks)
    return out

b = ""
b += panel("Không khí — tắt chậm", 0.40, BLUE, 36, 44, 132)
b += panel("Nước — tắt nhanh hơn", 1.15, ORG, 164, 172, 260)
b += panel("Dầu nhớt — gần như hết sau một nhịp", 2.8, RED, 292, 300, 388)
b += text(52, 414, "Đường đứt: biên độ.", "currentColor", 14, "start", "600")
b += text(52, 434, "Càng nhớt, biên độ càng nhanh áp vào trục.", "currentColor", 14, "start", "600")
fig2 = fig("0 0 440 446",
           "Ba đồ thị li độ theo thời gian: không khí tắt chậm, nước nhanh hơn, dầu nhớt gần như dừng",
           b,
           "Hình 2. Biên độ giảm: không khí chậm, nước nhanh, dầu gần hết sau một nhịp.",
           "tn-l11-tatdan-02")

# ---- Hình 3: cộng hưởng, trục f tuyến tính, đỉnh đúng tại f0
# A = Ar * b / sqrt((f-f0)^2 + b^2)
F0, F_LO, F_HI = 2.0, 0.5, 3.5
PLOT_L, PLOT_R, PLOT_T, PLOT_B = 64.0, 400.0, 46.0, 196.0
A_TOP = 7.0  # cm, đầu thang

def A_of(f, b_par, ar):
    return ar * b_par / math.sqrt((f - F0) ** 2 + b_par ** 2)

def x_of(f):
    return PLOT_L + (f - F_LO) / (F_HI - F_LO) * (PLOT_R - PLOT_L)

def y_of(a):
    return PLOT_B - (a / A_TOP) * (PLOT_B - PLOT_T)

# trục tuyến tính: 1 Hz, 2 Hz, 3 Hz cách đều
assert abs((x_of(2) - x_of(1)) - (x_of(3) - x_of(2))) < 0.05
assert abs((y_of(0) - y_of(3)) - (y_of(3) - y_of(6))) < 0.05

def curve(b_par, ar, col):
    pts = []
    best_f, best_a = None, -1
    for i in range(301):
        f = F_LO + (F_HI - F_LO) * i / 300
        a = A_of(f, b_par, ar)
        pts.append((x_of(f), y_of(a)))
        if a > best_a:
            best_f, best_a = f, a
    assert abs(best_f - F0) < 0.02, (b_par, best_f, best_a)
    # đỉnh hình phải đúng hoành độ f0
    y_min = min(p[1] for p in pts)
    xs_at_peak = [p[0] for p in pts if abs(p[1] - y_min) < 0.4]
    assert abs(sum(xs_at_peak) / len(xs_at_peak) - x_of(F0)) < 1.5
    return poly(pts, col, 2.4), best_a

c_small, a_small = curve(0.5, 6.0, BLUE)
c_large, a_large = curve(1.2, 2.5, ORG)
assert abs(a_small - 6.0) < 1e-9 and abs(a_large - 2.5) < 1e-9
assert a_small > a_large

b = defs("f3")
b += line(PLOT_L, PLOT_T - 4, PLOT_L, PLOT_B, "currentColor", 1.5)
b += line(PLOT_L, PLOT_B, PLOT_R + 8, PLOT_B, "currentColor", 1.5)
b += text(14, 28, "A (cm)", "currentColor", 13, "start", "700")
b += text(428, PLOT_B + 18, "f (Hz)", "currentColor", 12, "end", "700")
for a_tick, lab in ((0, "0"), (3, "3"), (6, "6")):
    yy = y_of(a_tick)
    b += line(PLOT_L - 5, yy, PLOT_L, yy, "currentColor", 1.3)
    b += text(PLOT_L - 8, yy + 4, lab, "currentColor", 12, "end", "600")
for f_tick in (1, 2, 3):
    xx = x_of(f_tick)
    b += line(xx, PLOT_B, xx, PLOT_B + 5, "currentColor", 1.3)
    b += text(xx, PLOT_B + 20, str(f_tick), "currentColor", 12, "middle", "600")
# vạch f0
b += line(x_of(F0), PLOT_T - 2, x_of(F0), PLOT_B, RED, 1.2, "4 3", 0.9)
b += text(x_of(F0) + 8, 30, "f0", RED, 13, "start", "700")
b += c_large
b += c_small
# chú giải ở vùng trống phía trên đỉnh (đỉnh cao nhất y ≈ y_of(6) = 61, chú giải y ≤ 40)
b += line(268, 20, 294, 20, BLUE, 3)
b += text(300, 24, "cản nhỏ", BLUE, 13, "start", "700")
b += line(268, 38, 294, 38, ORG, 3)
b += text(300, 42, "cản lớn", ORG, 13, "start", "700")
fig3 = fig("0 0 440 232",
           "Đồ thị cộng hưởng: hai đường lực cản, đỉnh đúng tại f0, trục tần số chia đều",
           b,
           "Hình 3. Cộng hưởng, trục f đều. Đỉnh đúng tại f0. Cản nhỏ: cao, hẹp. Cản lớn: thấp, rộng.",
           "tn-l11-tatdan-01")

# Hình 3 thay bằng ảnh OpenStax (28/10/2026, ngoại lệ có chủ đích: ảnh raster), giữ mốc FIG3
fig3 = '<figure class="fig" data-tl="1" data-exp="tn-l11-tatdan-01"><img src="/assets/openstax/l11-tat-dan-cuong-buc/hinh-duong-cong-huong.webp" alt="Đồ thị biên độ theo tần số ngoại lực với ba mức cản: đỉnh cao và hẹp khi cản nhỏ, thấp và rộng khi cản lớn, đỉnh đúng tại tần số riêng f0" loading="lazy" width="400" height="291"><figcaption>Hình 3. Cộng hưởng: biên độ theo tần số ngoại lực f.<br>Đỉnh đúng tại f₀. Cản nhỏ: cao, hẹp. Cản lớn: thấp, rộng.<br>Small / Medium / Heavy damping = cản nhỏ / vừa / lớn.<br><small>Hình: OpenStax, College Physics 2e, Hình 16.25 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>'

# ---- Hình 4: sơ đồ tự vẽ cầu Tacoma (không phải ảnh).
# Trên: nhìn ngang — mép trước và mép sau lệch ngược nhau, nút xoắn giữa nhịp (dạng xoắn một nút, 1940).
# Dưới: mặt cắt ngang — gió thổi ngang, mặt cầu xoắn qua lại quanh trục giữa.
b = ""
TL, TR, TTOP, GND, DECK = 106.0, 334.0, 56.0, 176.0, 146.0
TW = 228.0
b += text(14, 22, "Nhìn ngang", "currentColor", 14, "start", "700")
# chú giải hai mép (góc trên phải, trên đỉnh trụ)
b += line(250, 18, 276, 18, RED, 3)
b += text(282, 23, "mép phía trước", RED, 14, "start", "700")
b += line(250, 38, 276, 38, ORG, 2.6, "6 4")
b += text(282, 43, "mép phía sau", ORG, 14, "start", "700")
assert TTOP > 43 + 8
# trụ
for x0 in (TL, TR):
    b += (f'<rect x="{x0 - 6:.1f}" y="{TTOP:.1f}" width="12" height="{GND - TTOP:.1f}" fill="none" '
          f'stroke="currentColor" stroke-width="2"/>')
b += line(20, GND, 420, GND, "currentColor", 1.4, "", 0.45)
# cáp chính: parabol giữa hai đỉnh trụ, nhánh biên xuống neo
cab = [(TL + TW * i / 40, TTOP + 60 * (1 - ((TW * i / 40 - TW / 2) / (TW / 2)) ** 2)) for i in range(41)]
assert abs(cab[0][1] - TTOP) < 1e-6 and abs(cab[20][1] - (TTOP + 60)) < 1e-6
b += poly(cab, "currentColor", 1.8)
b += line(TL, TTOP, 30, DECK - 4, "currentColor", 1.8)
b += line(TR, TTOP, 410, DECK - 4, "currentColor", 1.8)
# mép cầu: nhịp biên phẳng, nhịp giữa lệch ngược nhau theo sin, nút ở giữa nhịp
def edge(sign):
    pts = [(30, DECK)]
    for i in range(61):
        x = TL + TW * i / 60
        pts.append((x, DECK + sign * 14 * math.sin(2 * math.pi * (x - TL) / TW)))
    pts.append((410, DECK))
    return pts
front, back = edge(1), edge(-1)
mid_i = 1 + 30
assert abs(front[mid_i][1] - DECK) < 1e-6 and abs(back[mid_i][1] - DECK) < 1e-6  # nút giữa nhịp
# dây treo: từ cáp xuống mép trước (bỏ đoạn sát trụ)
for i in range(2, 39, 3):
    x, yc = cab[i]
    yd = DECK + 14 * math.sin(2 * math.pi * (x - TL) / TW)
    b += line(x, yc, x, yd, "currentColor", 1, "", 0.55)
b += poly(back, ORG, 2.6, "6 4")
b += poly(front, RED, 3)
# ---- mặt cắt ngang
Y0 = 206
b += line(14, Y0, 426, Y0, "currentColor", 1, "3 4", 0.35)
b += text(14, Y0 + 24, "Mặt cắt ngang", "currentColor", 14, "start", "700")
CX, CY, HL = 262.0, 288.0, 72.0
for yy in (270, 288, 306):
    b += arrow("f4", "b", 40, yy, 132, yy, 2.6)
b += text(40, 256, "gió đều", BLUE, 14, "start", "700")
def deck_seg(deg):
    a = math.radians(deg)
    return (CX - HL * math.cos(a), CY - HL * math.sin(a), CX + HL * math.cos(a), CY + HL * math.sin(a))
x1, y1, x2, y2 = deck_seg(14)
b += line(x1, y1, x2, y2, RED, 6)
x1b, y1b, x2b, y2b = deck_seg(-14)
b += line(x1b, y1b, x2b, y2b, ORG, 4, "7 5")
assert min(x1, x1b) > 132 + 20, "gió không đè mặt cầu"
b += f'<circle cx="{CX:.1f}" cy="{CY:.1f}" r="3.5" fill="currentColor"/>'
# cung hai đầu V: xoắn qua lại quanh trục
R = 44
arcp = [(CX + R * math.cos(math.radians(d)), CY + R * math.sin(math.radians(d))) for d in range(236, 305, 4)]
b += poly(arcp, "currentColor", 1.8)
for d, sg in ((236, -1), (304, 1)):
    a = math.radians(d)
    b += chevron(CX + R * math.cos(a), CY + R * math.sin(a), -sg * math.sin(a), sg * math.cos(a), "currentColor", 1.8, 10)
b += text(x2 + 10, y2 + 6, "tư thế 1", RED, 14, "start", "700")
b += text(x2b + 10, y2b + 6, "tư thế 2", ORG, 14, "start", "700")
assert x2 + 10 + 60 < 440 and y2b + 6 > Y0 + 30
fig4 = fig("0 0 440 336",
           "Sơ đồ tự vẽ cầu Tacoma Narrows năm 1940: nhìn ngang hai mép cầu lệch ngược nhau, mặt cắt ngang xoắn qua lại trong gió đều",
           b,
           "Hình 4. Sơ đồ tự vẽ cầu Tacoma, 1940: gió đều làm mặt cầu xoắn qua lại. Không phải ảnh.")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    assert f.count("$") == 0, n  # không nhét công thức vào SVG
    h = h.replace(f"<!--FIG{n}-->", f)
assert "<!--FIG" not in h
open("theory.html", "w", encoding="utf8").write(margin_figs(h))
print("ok", len(h))
