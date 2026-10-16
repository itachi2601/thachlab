"""Sinh 4 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd16-truyen-nhiet-no-vi-nhiet/build_figs.py"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron, arrow

PHUT = 14
GREY = "rgba(148,163,184,.3)"


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def path(pts, c="currentColor", w=2.4, dash=""):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"{ds}/>'


def rect(x, y, w, h, fill=GREY, c="currentColor", sw=2, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def wavy(x1, y1, x2, y2, c, amp=4, n=3, w=2.2):
    """Mũi tên lượn sóng (tia nhiệt) từ (x1,y1) tới (x2,y2)."""
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    pts = []
    for i in range(61):
        s = i / 60 * (L - 6)
        o = amp * math.sin(2 * math.pi * n * s / (L - 6))
        pts.append((x1 + ux * s + nx * o, y1 + uy * s + ny * o))
    pts.append((x2, y2))
    return path(pts, c, w) + chevron(x2, y2, ux, uy, c, w, 9)


def flame(cx, y, h=20, w=14):
    return (f'<path d="M{cx-w/2:.1f},{y} Q{cx-w/2:.1f},{y-h*0.6:.1f} {cx:.1f},{y-h:.1f} '
            f'Q{cx+w/2:.1f},{y-h*0.6:.1f} {cx+w/2:.1f},{y} Z" fill="rgba(251,146,60,.35)" stroke="{ORG}" stroke-width="2"/>')


# ═════════ Hình 1: ba cách truyền nhiệt quanh nồi nước + cấu tạo phích ═════════
b = ""
# --- nồi nước trên bếp
PX0, PX1, PY0, PY1 = 30, 170, 120, 200          # thân nồi
WTOP = 136                                      # mặt nước
b += f'<rect x="{PX0+2}" y="{WTOP}" width="{PX1-PX0-4}" height="{PY1-WTOP-2}" fill="rgba(56,189,248,.18)"/>'
b += path([(PX0, PY0), (PX0, PY1), (PX1, PY1), (PX1, PY0)], "currentColor", 2.6)
b += line(PX0 + 2, WTOP, PX1 - 2, WTOP, BLUE, 1.6)
# cán kim loại + mũi tên dẫn nhiệt dọc cán
b += line(PX1, 128, 216, 128, "currentColor", 5)
b += arrow("", "r", 176, 116, 214, 116, 2.4)
b += text(195, 104, "dẫn nhiệt", RED, 15, "middle", "700")
# dòng đối lưu: giữa đi lên (nóng), hai bên đi xuống (nguội)
b += arrow("", "r", 100, 192, 100, 146, 2.4)
b += path([(100, 146), (100, 142)], RED, 2.4)
b += arrow("", "b", 48, 146, 48, 190, 2.2)
b += arrow("", "b", 152, 146, 152, 190, 2.2)
b += path([(92, 144), (56, 144)], RED, 1.8, "4 3") + path([(108, 144), (144, 144)], RED, 1.8, "4 3")
b += chevron(56, 144, -1, 0, RED, 1.8, 8) + chevron(144, 144, 1, 0, RED, 1.8, 8)
b += text(100, 112, "đối lưu", BLUE, 15, "middle", "700")
# bếp + lửa
b += rect(36, 222, 128, 10, GREY, "currentColor", 2, 2)
for cx in (62, 86, 110, 134):
    b += flame(cx, 220, 16, 12)
# tia bức xạ từ lửa ra ngoài
b += wavy(40, 214, 8, 248, ORG, 3.5, 2)
b += wavy(160, 214, 200, 246, ORG, 3.5, 2)
b += text(10, 272, "bức xạ", ORG, 15, "start", "700")
b += text(204, 270, "bức xạ", ORG, 15, "end", "700")
# --- phích (mặt cắt), chỉ ghi tên bộ phận
CX0, CX1, CY0, CY1 = 252, 332, 68, 276          # vỏ ngoài
b += rect(CX0, CY0 + 18, CX1 - CX0, CY1 - CY0 - 18, "none", "currentColor", 2.2, 8)
OG = (263, 321, 98, 266)                        # lớp thuỷ tinh ngoài (x0, x1, y0, y1)
IG = (273, 311, 108, 256)                       # lớp thuỷ tinh trong
b += f'<rect x="{OG[0]}" y="{OG[2]}" width="{OG[1]-OG[0]}" height="{OG[3]-OG[2]}" rx="14" fill="rgba(148,163,184,.10)" stroke="#94a3b8" stroke-width="3"/>'
b += f'<rect x="{IG[0]}" y="{IG[2]}" width="{IG[1]-IG[0]}" height="{IG[3]-IG[2]}" rx="10" fill="rgba(56,189,248,.18)" stroke="#94a3b8" stroke-width="3"/>'
b += rect(IG[0] + 3, 108, IG[1] - IG[0] - 6, 18, "rgba(251,146,60,.30)", ORG, 1.8, 3)   # nút đậy miệng ruột
b += rect(CX0 + 10, CY0, CX1 - CX0 - 20, 18, GREY, "currentColor", 2, 4)              # nắp
LX = 346
for yl, x_from, s in ((77, CX1 - 10, "nắp"), (117, IG[1] - 3, "nút"), (160, (IG[1] + OG[1]) / 2, "chân không"),
                      (206, OG[1] + 1, "tráng bạc"), (262, CX1, "vỏ")):
    b += line(x_from, yl, LX - 4, yl, "currentColor", 1.2, "", .7)
    b += text(LX, yl + 5, s, "currentColor", 15, "start", "700")
b += text(CX0 + 40, 296, "phích", "currentColor", 15, "middle", "700")
b += text(100, 296, "nồi nước trên bếp", "currentColor", 15, "middle", "700")
fig1 = wrap("0 58 440 248", "Bên trái: nồi nước trên bếp, nhiệt dẫn dọc cán, đối lưu trong nước, bức xạ từ ngọn lửa ra xung quanh. Bên phải: mặt cắt phích gồm nắp, nút, hai lớp thuỷ tinh tráng bạc kẹp chân không, vỏ",
            b, "Hình 1. Bên trái: ba cách nhiệt đi ra từ bếp và nồi nước.<br>Bên phải: mặt cắt phích, chỉ ghi tên bộ phận.")

# ═════════ Hình 2: khe hở giữa hai thanh ray, mùa đông và mùa hè ═════════
b = ""
for y0, gap, lab in ((58, 22, "mùa đông: ray co lại, khe rộng"), (148, 8, "mùa hè: ray nở ra, khe hẹp")):
    xm = 220
    b += text(16, y0 - 22, lab, "currentColor", 15, "start", "700")
    for x in range(30, 420, 34):                                   # tà vẹt
        b += rect(x, y0 + 14, 22, 8, GREY, "currentColor", 1.2, 1)
    b += rect(16, y0, xm - gap / 2 - 16, 14, "rgba(148,163,184,.45)", "currentColor", 2, 1)
    b += rect(xm + gap / 2, y0, 424 - xm - gap / 2, 14, "rgba(148,163,184,.45)", "currentColor", 2, 1)
    col = BLUE if gap > 10 else RED
    b += line(xm - gap / 2, y0 - 10, xm + gap / 2, y0 - 10, col, 1.6)
    b += line(xm - gap / 2, y0 - 15, xm - gap / 2, y0 - 5, col, 1.6) + line(xm + gap / 2, y0 - 15, xm + gap / 2, y0 - 5, col, 1.6)
    b += text(xm + 20, y0 - 4, "khe", col, 15, "start", "700")
fig2 = wrap("0 18 440 168", "Hai thanh ray đặt nối tiếp trên tà vẹt: mùa đông khe giữa hai thanh rộng, mùa hè ray nở ra nên khe hẹp lại",
            b, "Hình 2. Chừa khe để ray có chỗ dãn.<br>Không có khe, ray nóng lên sẽ đẩy nhau và cong vênh.")

# ═════════ Hình 3: băng kép đồng – thép ở nhiệt độ phòng (chưa nung) ═════════
b = ""
b += rect(18, 44, 34, 82, GREY, "currentColor", 2, 2)
for y in range(50, 124, 12):
    b += line(20, y + 10, 50, y, "currentColor", 1.1, "", .5)
b += text(35, 146, "ngàm", "currentColor", 15, "middle", "700")
b += rect(52, 72, 330, 11, "rgba(251,146,60,.45)", ORG, 1.8)
b += rect(52, 83, 330, 11, "rgba(148,163,184,.55)", "currentColor", 1.8)
b += text(216, 62, "lá đồng: α lớn hơn", ORG, 15, "middle", "700")
b += text(216, 116, "lá thép: α nhỏ hơn", "currentColor", 15, "middle", "700")
for cx in (190, 216, 242):
    b += flame(cx, 158, 18, 13)
b += text(262, 154, "nung nóng", ORG, 15, "start", "700")
fig3 = wrap("0 38 440 128", "Băng kép gồm lá đồng ở trên và lá thép ở dưới tán chặt vào nhau, một đầu kẹp vào ngàm, ở nhiệt độ phòng băng thẳng; bên dưới có ngọn lửa",
            b, "Hình 3. Băng kép ở nhiệt độ phòng: thẳng.<br>Lá đồng ở trên, lá thép ở dưới.")

# ═════════ Hình 4: khối lượng riêng của nước từ 0 đến 10 °C ═════════
DATA = [999.84, 999.90, 999.94, 999.96, 999.97, 999.96, 999.94, 999.90, 999.85, 999.78, 999.70]   # kg/m3, t = 0..10 °C
GX0, GX1, GY0, GY1 = 72, 418, 240, 50          # trục: x 0..10 °C, y 999,65..1000,00
DMIN, DMAX = 999.65, 1000.00
fx = lambda t: GX0 + (GX1 - GX0) * t / 10
fy = lambda d: GY0 - (GY0 - GY1) * (d - DMIN) / (DMAX - DMIN)
b = ""
for t in range(11):
    b += line(fx(t), GY1, fx(t), GY0, "currentColor", 1, "", .22)
for k in range(1, 4):
    d = 999.7 + 0.1 * k - 0.1
    b += line(GX0, fy(d), GX1, fy(d), "currentColor", 1, "", .22)
b += line(GX0, fy(1000.0), GX1, fy(1000.0), "currentColor", 1, "", .22)
b += line(GX0, GY0, GX1 + 8, GY0, "currentColor", 1.6) + line(GX0, GY0, GX0, GY1 - 8, "currentColor", 1.6)
# Catmull-Rom qua các điểm số liệu
P = [(fx(t), fy(d)) for t, d in enumerate(DATA)]
curve = []
for i in range(len(P) - 1):
    p0, p1, p2, p3 = P[max(i - 1, 0)], P[i], P[i + 1], P[min(i + 2, len(P) - 1)]
    for j in range(12):
        s = j / 12
        curve.append(tuple(0.5 * (2 * p1[k] + (-p0[k] + p2[k]) * s + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * s * s
                                  + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * s ** 3) for k in (0, 1)))
curve.append(P[-1])
b += path(curve, BLUE, 2.8)
for x, y in P:
    b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{BLUE}"/>'
assert min(P, key=lambda p: p[1]) == P[4]                     # đỉnh đúng ở 4 °C
b += line(fx(4), fy(DATA[4]) + 6, fx(4), GY0, ORG, 1.6, "5 4")
for t in (0, 2, 4, 6, 8, 10):
    b += text(fx(t), GY0 + 20, str(t), "currentColor", 15, "middle", "600")
for d, s in ((999.7, "999,7"), (999.8, "999,8"), (999.9, "999,9"), (1000.0, "1000,0")):
    b += text(GX0 - 6, fy(d) + 5, s, "currentColor", 14, "end", "600")
b += text(GX1, GY0 + 40, "t (°C)", "currentColor", 15, "end", "700")
b += text(GX0 + 6, GY1 - 10, "D (kg/m³)", "currentColor", 15, "start", "700")
fig4 = wrap("0 28 440 262", "Đồ thị khối lượng riêng của nước theo nhiệt độ từ 0 đến 10 độ C: tăng từ 999,84 lên 999,97 kilôgam trên mét khối ở 4 độ C rồi giảm còn 999,70 ở 10 độ C",
            b, "Hình 4. Khối lượng riêng của nước từ 0 °C đến 10 °C.<br>Trục dọc đã phóng to: cả đồ thị chỉ chênh nhau 0,3 kg/m³.")

# ═════════ ghi theory.html ═════════
src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in ((1, fig1), (2, fig2), (3, fig3), (4, fig4)):
    assert f"<!--FIG{n}-->" in src, n
    src = src.replace(f"<!--FIG{n}-->", f)
src = src.replace("__PHUT__", str(PHUT))
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
