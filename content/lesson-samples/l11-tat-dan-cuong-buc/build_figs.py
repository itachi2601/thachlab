#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài tắt dần / cưỡng bức / cộng hưởng và thay <!--FIGn--> trong theory.src.html."""
import math
from svg_lib import *

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

# ---- Hình 1: xích đu, nhún cùng chiều chỉ một phần nhịp
# Gần đáy, đang đi sang phải. Mũi xanh = chiều đu, mũi đỏ = lực nhún, song song.
b = defs("f1")
b += line(70, 26, 200, 26, "currentColor", 4)
b += line(128, 26, 128, 34, "currentColor", 2.5)
pivot_x, pivot_y, L, ang = 128.0, 34.0, 158.0, math.radians(8)
sx = pivot_x + L * math.sin(ang)
sy = pivot_y + L * math.cos(ang)
# cung quỹ đạo mờ, chỉ phía trong, không đè mũi tên
arc = []
for deg in range(-42, -4, 3):
    a = math.radians(deg)
    arc.append((pivot_x + L * math.sin(a), pivot_y + L * math.cos(a)))
b += poly(arc, "currentColor", 1.3, "4 4")
b += line(pivot_x, pivot_y, sx - 14, sy, "currentColor", 2.2)
b += (f'<rect x="{sx - 16:.1f}" y="{sy - 5:.1f}" width="34" height="9" rx="2" '
      f'fill="{ORG}" stroke="currentColor" stroke-width="1.4"/>')
hx, hy = sx + 2, sy - 42
b += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="11" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += line(hx, hy + 11, sx + 2, sy - 5, "currentColor", 2.2)
# mũi cùng chiều, nằm bên phải người, không cắt dây
b += arrow("f1", "g", 196, 132, 360, 132, 3.2)
b += text(204, 116, "chiều đang đi", GRN, 13, "start", "700")
b += arrow("f1", "r", 196, 158, 318, 158, 3.2)
b += text(204, 180, "nhún cùng chiều", RED, 13, "start", "700")
b += text(196, 208, "chỉ một phần nhịp", "currentColor", 13, "start", "600")
b += text(196, 228, "không đẩy suốt vòng", "currentColor", 13, "start", "600")
fig1 = fig("0 0 440 252",
           "Xích đu gần đáy đang sang phải: lực nhún cùng chiều chuyển động, chỉ một phần nhịp",
           b,
           "Hình 1. Xích đu: nhún cùng chiều, chỉ một phần nhịp.",
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
    out = text(X0, y_title, title, col, 13, "start", "700")
    out += line(X0, y_top, X0, y_bot, "currentColor", 1.3, "", 0.55)
    out += line(X0, mid, X1, mid, "currentColor", 1.2, "", 0.45)
    out += text(X1 + 6, mid + 4, "t", "currentColor", 12, "start", "600")
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
b += text(14, 18, "x", "currentColor", 13, "start", "700")
b += panel("Không khí — tắt chậm", 0.40, BLUE, 36, 44, 132)
b += panel("Nước — tắt nhanh hơn", 1.15, ORG, 164, 172, 260)
b += panel("Dầu nhớt — gần như hết sau một nhịp", 2.8, RED, 292, 300, 388)
b += text(52, 414, "Đường đứt là biên độ. Càng nhớt, đường càng áp vào trục.", "currentColor", 12, "start", "500")
fig2 = fig("0 0 440 430",
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

# ---- Hình 4: sơ đồ cầu Tacoma, tự vẽ, không phải ảnh
b = defs("f4")
# gió
for yy in (78, 118, 158):
    b += arrow("f4", "b", 16, yy, 62, yy, 2.4)
b += text(16, 64, "gió đều", BLUE, 13, "start", "700")
# trụ
b += f'<rect x="78" y="36" width="16" height="150" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += f'<rect x="332" y="36" width="16" height="150" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += line(70, 186, 364, 186, "currentColor", 1.4, "", 0.4)
# hai tư thế mặt cầu (xoắn), không giao chữ
b += line(102, 128, 324, 92, RED, 3.2)
b += line(102, 100, 324, 148, ORG, 2.4, "7 4")
b += text(188, 80, "tư thế 1", RED, 12, "start", "700")
b += text(188, 176, "tư thế 2", ORG, 12, "start", "700")
# dây treo ngắn, né chữ
b += line(94, 36, 140, 112, "currentColor", 1.2, "", 0.7)
b += line(340, 36, 300, 104, "currentColor", 1.2, "", 0.7)
b += text(168, 214, "mặt cầu xoắn · 1940", "currentColor", 14, "start", "700")
b += text(168, 234, "sơ đồ tự vẽ, không phải ảnh", "currentColor", 12, "start", "500")
fig4 = fig("0 0 440 250",
           "Sơ đồ tự vẽ cầu Tacoma Narrows năm 1940: gió đều, mặt cầu xoắn giữa hai tư thế",
           b,
           "Hình 4. Sơ đồ tự vẽ cầu Tacoma, 1940: gió làm mặt cầu xoắn. Không phải ảnh.")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    assert f.count("$") == 0, n  # không nhét công thức vào SVG
    h = h.replace(f"<!--FIG{n}-->", f)
assert "<!--FIG" not in h
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h))
