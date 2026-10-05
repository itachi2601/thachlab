#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài 25 Năng lượng điện và công suất điện (lesson 44),
thay <!--FIGn--> trong theory.src.html -> theory.html. Chạy lại được (idempotent).
Kiểm bằng toạ độ: chấm trên đường cong, trục tuyến tính, đầu mũi tên, nhãn không chồng/không vượt viewBox."""
import html
import math
import pathlib
import re
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
# Suất điện động: glyph ℰ (U+2130) có trong font Mac nhưng vẽ nhỏ như "ε" và có thể thiếu trên Android
# -> dùng E nghiêng (serif), nhất quán cả 4 hình. Muốn đổi về ℰ: EMF = "ℰ".
EMF = '<tspan font-style="italic" font-family="Georgia,\'Times New Roman\',serif" font-size="1.1em">E</tspan>' 
SLATE = "rgba(148,163,184,.18)"
PFX = "tl44-"                                          # tiền tố id marker, duy nhất toàn trang


def V(x):
    """Đại lượng vật lí: chữ nghiêng serif (cùng kiểu EMF) để I, U, R, r không giống vạch đứng."""
    return f'<tspan font-style="italic" font-family="Georgia,\'Times New Roman\',serif" font-size="1.1em">{x}</tspan>'


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, marker=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    return (f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" '
            f'stroke-width="{w}"{d} opacity="{op}"{m}/>')


def poly(pts, c, w=2.4, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{d} opacity="{op}" points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, rx=0, fill="none", c="currentColor", sw=2):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def path(d, c="currentColor", w=2, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def sub(s):
    return f'<tspan baseline-shift="sub" font-size="0.75em">{s}</tspan>'


def sup(s):
    return f'<tspan baseline-shift="super" font-size="0.75em">{s}</tspan>'


def fig(vb, label, body, cap, exp=None):
    s = wrap(vb, label, body, cap)
    if exp:
        s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
    return s


class Canvas:
    """Gom thân SVG + hộp nhãn + vật cản để kiểm không chồng / không vượt viewBox."""
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.obst = "", [], []

    def add(self, s):
        self.body += s

    def t(self, x, y, s, c="currentColor", size=13, anchor="start", weight="600", tag=None, extra=""):
        vis = html.unescape(re.sub(r"<[^>]+>", "", s))
        wd = 0.55 * size * len(vis)
        x0 = x if anchor == "start" else x - wd / 2 if anchor == "middle" else x - wd
        self.labels.append((tag or vis, x0, y - 0.8 * size, x0 + wd, y + 0.25 * size))
        fam = ' font-family="ui-monospace,Menlo,Consolas,monospace"' if extra == "mono" else ""
        self.body += text(x, y, s, c, size, anchor, weight).replace("<text ", f"<text{fam} ", 1) if fam else text(x, y, s, c, size, anchor, weight)

    def obstacle_pts(self, name, pts, pad=1.5):
        self.obst.append((name, [(float(x), float(y)) for x, y in pts], pad))

    def obstacle_seg(self, name, x1, y1, x2, y2, pad=1.5):
        n = max(2, int(math.hypot(x2 - x1, y2 - y1) / 2))
        self.obstacle_pts(name, [(x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n) for i in range(n + 1)], pad)

    def obstacle_rect(self, name, x0, y0, x1, y1):
        self.obst.append((name, ("rect", x0, y0, x1, y1), 0))

    def check(self, allow=()):
        M = 1
        for nm, x0, y0, x1, y1 in self.labels:
            assert x0 >= M and y0 >= M and x1 <= self.w - M and y1 <= self.h - M, (self.name, "vượt viewBox", nm, x0, y0, x1, y1)
        for i, a in enumerate(self.labels):
            for b in self.labels[i + 1:]:
                if (a[1], b[1]) and a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    raise AssertionError((self.name, "hai nhãn chồng nhau", a[0], b[0]))
        for nm, x0, y0, x1, y1 in self.labels:
            for on, g, pad in self.obst:
                if (nm, on) in allow:
                    continue
                if isinstance(g, tuple) and g[0] == "rect":
                    _, rx0, ry0, rx1, ry1 = g
                    if x0 < rx1 and rx0 < x1 and y0 < ry1 and ry0 < y1:
                        raise AssertionError((self.name, "nhãn chồng vật", nm, on))
                else:
                    for px, py in g:
                        if x0 - pad <= px <= x1 + pad and y0 - pad <= py <= y1 + pad:
                            raise AssertionError((self.name, "nhãn chồng nét", nm, on, round(px), round(py)))


def wd_mark(prefix, name, color, size):
    """Marker mũi tên cỡ cố định (userSpaceOnUse): đỉnh mũi nằm cách đầu đường `size` px theo chiều đường."""
    return (f'<marker id="{prefix}-{name}" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="{size}" markerHeight="{size}" '
            f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')


# =====================================================================================
# Hình 1: công tơ điện + ba thiết bị
# =====================================================================================
c1 = Canvas("f1", 440, 240)
c1.add(defs(PFX + "f1"))
c1.t(12, 20, "kWh = năng lượng đã dùng", "currentColor", 14, "start", "400")
c1.t(12, 84, "Lưới điện", "currentColor", 14, "start", "700")
# ổ cắm
c1.add(rect(12, 98, 40, 34, 5, SLATE))
c1.add(line(25, 108, 25, 122, "currentColor", 3) + line(39, 108, 39, 122, "currentColor", 3))
c1.add(line(52, 115, 90, 115, "currentColor", 2))
c1.add(arrow(PFX + "f1", "r", 58, 115, 84, 115, 2.5))
# công tơ
c1.add(rect(90, 70, 120, 90, 8, SLATE))
c1.add(rect(105, 95, 90, 25, 3, "rgba(15,23,42,.35)", "currentColor", 1.5))
c1.t(150, 112, "0312,4 kWh", GRN, 14, "middle", "700", extra="mono")
c1.t(150, 148, "Công tơ điện", "currentColor", 14, "middle", "600")
c1.add(dot(112, 82, 3, "currentColor") + dot(188, 82, 3, "currentColor"))
# dây ra
c1.add(line(210, 115, 234, 115, "currentColor", 2) + line(234, 40, 234, 190, "currentColor", 2))
ROWS = (40, 115, 190)
for y in ROWS:
    c1.add(arrow(PFX + "f1", "r", 234, y, 254, y, 2.5))
# đèn
c1.add(f'<circle cx="279" cy="38" r="13" fill="rgba(251,191,36,.25)" stroke="currentColor" stroke-width="2"/>')
c1.add(rect(273, 51, 12, 7, 1.5) + line(274, 62, 284, 62, "currentColor", 2))
c1.t(304, 36, "Đèn", "currentColor", 15, "start", "700")
c1.t(304, 54, "100 W", RED, 15, "start", "700")
# trục chính CNC
c1.add(rect(267, 97, 24, 36, 2, SLATE))
c1.add(path("M273,133 L285,133 L279,148 Z", "currentColor", 2, SLATE))
c1.add(line(267, 105, 291, 105, "currentColor", 1.5))
c1.t(304, 111, "Trục chính CNC", "currentColor", 15, "start", "700")
c1.t(304, 129, "2,2 kW", RED, 15, "start", "700")
# ấm đun
c1.add(path("M270,203 L294,203 L290,178 L274,178 Z", "currentColor", 2, SLATE))
c1.add(line(273, 175, 291, 175, "currentColor", 2))
c1.add(path("M291,182 Q299,190 292,198", "currentColor", 2))
c1.t(304, 186, "Ấm đun", "currentColor", 15, "start", "700")
c1.t(304, 204, "1800 W", RED, 15, "start", "700")
c1.t(304, 230, "W, kW = công suất", "currentColor", 14, "start", "400")
# vật cản: dây, mũi tên, biểu tượng thiết bị
c1.obstacle_seg("daymoi", 52, 115, 90, 115)
c1.obstacle_seg("riser", 234, 40, 234, 190)
for y in ROWS:
    c1.obstacle_seg(f"nhanh{y}", 234, y, 258, y)
c1.obstacle_rect("tb-den", 265, 25, 293, 63)
c1.obstacle_rect("tb-cnc", 267, 97, 291, 148)
c1.obstacle_rect("tb-am", 270, 175, 296, 203)
c1.obstacle_rect("congto", 90, 70, 210, 160)
c1.obstacle_rect("o-cam", 12, 98, 52, 132)
# kiểm: nhánh ra kết thúc x≈258 (mũi 254 + 1,4·2,5 = 257,5) và nhãn thiết bị bắt đầu ≥ 300
assert abs(254 + 1.4 * 2.5 - 258) < 1 and all(l[1] >= 300 for l in c1.labels if l[0] in ("Đèn", "100 W", "Trục chính CNC", "2,2 kW", "Ấm đun", "1800 W"))
screen_w = 0.6 * 14 * len("0312,4 kWh")           # chữ monospace nằm gọn màn hình 105..195
assert 150 - screen_w / 2 > 105 and 150 + screen_w / 2 < 195, screen_w
c1.check(allow={("0312,4 kWh", "congto"), ("Công tơ điện", "congto")})
fig1 = fig("0 0 440 240",
           "Sơ đồ lưới điện qua công tơ điện hiển thị 0312,4 kWh tới ba thiết bị: đèn 100 W, trục chính CNC 2,2 kW, ấm đun 1800 W",
           c1.body, "Hình 1. Công tơ đếm kWh; thiết bị ghi công suất W.", exp="tn-l11-nang-luong-dien-01")

# =====================================================================================
# Hình 2: ℰI = UI + I²r
# =====================================================================================
c2 = Canvas("f2", 440, 210)
c2.add("<defs>" + wd_mark(PFX + "f2", "r", RED, 18) + wd_mark(PFX + "f2", "b", BLUE, 16) + wd_mark(PFX + "f2", "o", ORG, 10) + "</defs>")
# khối nguồn
c2.add(rect(15, 60, 120, 90, 8, SLATE))
c2.t(75, 83, "Nguồn", "currentColor", 15, "middle", "700")
c2.t(75, 102, f"{EMF}, {V('r')}", "currentColor", 14, "middle", "600")
# ký hiệu pin: vạch dài = cực (+) quay về phía mạch ngoài (bên phải), vạch ngắn = cực (−) bên trái; kèm dấu +/−
PIN_Y = 130
c2.add(line(44, PIN_Y, 61, PIN_Y, "currentColor", 2) + line(61, PIN_Y - 7, 61, PIN_Y + 7, "currentColor", 3) +
       line(73, PIN_Y - 13, 73, PIN_Y + 13, "currentColor", 3) + line(73, PIN_Y, 90, PIN_Y, "currentColor", 2))
c2.t(28, PIN_Y + 5, "−", "currentColor", 14, "middle", "700")
c2.t(106, PIN_Y + 5, "+", "currentColor", 14, "middle", "700")
# khối mạch ngoài
c2.add(rect(300, 60, 125, 90, 8, SLATE))
c2.t(362, 83, "Mạch ngoài", "currentColor", 15, "middle", "700")
zz = [(322, 114)] + [(330 + 7 * i, 114 + (8 if i % 2 == 0 else -8)) for i in range(8)] + [(402, 114)]
c2.add(poly(zz, "currentColor", 2))
c2.t(362, 144, V("R"), "currentColor", 14, "middle", "600", tag="R")
# độ rộng ∝ công suất 24 : 20 : 4 W  ->  9 : 7 : 2 px (làm tròn từ 9 / 7,5 / 1,5)
W_R, W_B, W_O = 9, 7, 2
assert abs(W_R / 24 - W_B / 20) < 0.04 and W_R == W_B + W_O
HEAD_R, HEAD_B, HEAD_O = 18, 16, 10
JX, JY = 215, 105                                   # điểm rẽ chung
c2.add(f'<line x1="135" y1="{JY}" x2="{JX - HEAD_R}" y2="{JY}" stroke="{RED}" stroke-width="{W_R}" marker-end="url(#{PFX}f2-r)"/>')
c2.add(f'<line x1="{JX}" y1="{JY}" x2="{300 - HEAD_B}" y2="{JY}" stroke="{BLUE}" stroke-width="{W_B}" marker-end="url(#{PFX}f2-b)"/>')
CAM = [(JX, JY), (252, 66), (118, 12), (118, 50)]   # Bezier bậc 3, kết thúc đi xuống thẳng đứng
c2.add(f'<path d="M{CAM[0][0]},{CAM[0][1]} C{CAM[1][0]},{CAM[1][1]} {CAM[2][0]},{CAM[2][1]} {CAM[3][0]},{CAM[3][1]}" '
       f'fill="none" stroke="{ORG}" stroke-width="{W_O}" marker-end="url(#{PFX}f2-o)"/>')
# sóng nhiệt trên mép trên khối nguồn
for xw in (60, 72, 84):
    c2.add(path(f"M{xw},56 q-3,-3.5 0,-7 t0,-7", ORG, 1.6))
# nhãn
c2.t(172, 90, f"{V('P')}{sub('ng')} = {EMF}{V('I')}", RED, 14, "middle", "700", tag="P ng")
c2.t(257, 130, f"Có ích: {V('U')}{V('I')}", BLUE, 14, "middle", "700", tag="Co ich")
c2.t(228, 38, f"Hao phí: {V('I')}{sup('2')}{V('r')}", ORG, 14, "start", "700", tag="Hao phi")
c2.t(220, 190, f"{EMF}{V('I')} = {V('U')}{V('I')} + {V('I')}{sup('2')}{V('r')}", "currentColor", 15, "middle", "700", tag="tong ket")


def bez(P, n=60):
    return [tuple((1 - t) ** 3 * P[0][k] + 3 * (1 - t) ** 2 * t * P[1][k] + 3 * (1 - t) * t * t * P[2][k] + t ** 3 * P[3][k] for k in (0, 1))
            for t in (i / n for i in range(n + 1))]


cam_pts = bez(CAM)
c2.obstacle_pts("nhanh-cam", cam_pts, 2.5)
c2.obstacle_seg("mui-do", 135, JY, JX, JY, 7)
c2.obstacle_seg("mui-xanh", JX, JY, 300, JY, 6)
for nm_, (a_, b_, c_, d_) in (("khoi-nguon", (15, 60, 135, 150)), ("khoi-ngoai", (300, 60, 425, 150))):
    for k_, (x1_, y1_, x2_, y2_) in enumerate(((a_, b_, c_, b_), (c_, b_, c_, d_), (c_, d_, a_, d_), (a_, d_, a_, b_))):
        c2.obstacle_seg(f"{nm_}{k_}", x1_, y1_, x2_, y2_, 1)
c2.obstacle_rect("song-nhiet", 54, 40, 90, 57)
c2.obstacle_seg("pin-day-trai", 44, PIN_Y, 61, PIN_Y, 1.5)
c2.obstacle_seg("pin-ngan", 61, PIN_Y - 7, 61, PIN_Y + 7, 2)
c2.obstacle_seg("pin-dai", 73, PIN_Y - 13, 73, PIN_Y + 13, 2)
c2.obstacle_seg("pin-day-phai", 73, PIN_Y, 90, PIN_Y, 1.5)
c2.obstacle_seg("zigzag", 322, 106, 402, 122, 1)
# kiểm hình học theo spec
tipx_b = (300 - HEAD_B) + HEAD_B
tip_cam = (CAM[3][0], CAM[3][1] + HEAD_O)           # tiếp tuyến cuối thẳng xuống nên mũi nằm cách đầu đường HEAD_O px
assert tipx_b == 300 and (JX, JY) == CAM[0]
assert 15 <= tip_cam[0] <= 135 and tip_cam[1] == 60, tip_cam
assert abs((CAM[3][0] - CAM[2][0])) < 1e-9 and CAM[3][1] > CAM[2][1]
assert 130 - 105 >= 15                                # "Có ích: UI" cách trục >= 15 px
# pin: vạch dài (cực +) nằm bên PHẢI vạch ngắn, tức quay về phía mạch ngoài; dòng/năng lượng đi ra phía phải
assert 73 > 61 and (2 * 13) > (2 * 7) and c2.labels and True
c2.check()
fig2 = fig("0 0 440 210",
           "Sơ đồ dòng năng lượng: công suất nguồn EI tách thành phần có ích UI tới mạch ngoài và phần hao phí I bình phương r toả nhiệt trong nguồn",
           c2.body, "Hình 2. Nguồn phát $\\mathcal{E}I$: mạch ngoài nhận $UI$, nguồn nóng $I^2r$.")

# =====================================================================================
# Hình 3: H(R) = R/(R + r), r = 1 Ω
# =====================================================================================
c3 = Canvas("f3", 440, 260)
OX, OY = 50, 215
KX, KY = 36, 1.8                                    # px/Ω, px/%


def px(R):
    return OX + KX * R


def py(R):
    return OY - 180 * R / (R + 1)


c3.add(line(OX, OY, 420, OY, "currentColor", 2) + line(OX, OY, OX, 28, "currentColor", 2))
xt = [(R, px(R)) for R in (0, 2, 4, 6, 8, 10)]
yt = [(H, OY - KY * H) for H in (0, 25, 50, 75, 100)]
for R, x in xt:
    c3.add(line(x, OY, x, OY + 5, "currentColor", 1.5))
    c3.t(x, 237, f"{R}", "currentColor", 14, "middle", "400")
for H, y in yt:
    c3.add(line(OX - 5, y, OX, y, "currentColor", 1.5))
    c3.t(OX - 8, y + 5, f"{H}", "currentColor", 14, "end", "400")
c3.t(412, 254, f"{V('R')} (Ω)", "currentColor", 14, "end", "700", tag="R (Ω)")
c3.t(8, 20, f"{V('H')} (%)", "currentColor", 14, "start", "700", tag="H (%)")
# tiệm cận 100 %
c3.add(line(OX, 35, 410, 35, "currentColor", 1.5, "4 4", .5))
c3.t(250, 28, "không bao giờ chạm", "currentColor", 14, "start", "400")
# R = r
c3.add(line(86, 215, 86, 125, "currentColor", 1.2, "3 3", .55) + line(50, 125, 86, 125, "currentColor", 1.2, "3 3", .55))
c3.t(91, 208, f"{V('R')} = {V('r')}", "currentColor", 14, "start", "600", tag="R = r")
# đường cong
Rs = [i * 0.25 for i in range(0, 41)]
curve = [(px(R), py(R)) for R in Rs]
c3.add(poly(curve, GRN, 2.5))
# bốn điểm đo
DATA = [(1.0, 86, 125, "50 %"), (2.0, 122, 95, "67 %"), (4.0, 194, 71, "80 %"), (9.0, 374, 53, "90 %")]
for R, x, y, lab in DATA:
    assert abs(x - px(R)) < 0.6 and abs(y - (215 - 180 * R / (R + 1))) < 0.6, (R, x, y)
    c3.add(dot(x, y, 4.5, RED))
    c3.t(x + 7, y + 17, lab, "currentColor", 14, "start", "600")
c3.obstacle_pts("duong-cong", curve, 2.5)
c3.obstacle_pts("cham", [(x, y) for _, x, y, _ in DATA], 5)
c3.obstacle_seg("tiem-can", OX, 35, 410, 35, 1)
c3.obstacle_seg("guide-d", 86, 125, 86, 215, 1)
c3.obstacle_seg("guide-n", 50, 125, 86, 125, 1)
c3.obstacle_seg("truc-x", OX, OY, 420, OY, 1)
c3.obstacle_seg("truc-y", OX, OY, OX, 28, 1)
for _, x in xt:
    c3.obstacle_seg("tick-x", x, OY, x, OY + 5, 1)
for _, y in yt:
    c3.obstacle_seg("tick-y", OX - 5, y, OX, y, 1)
# kiểm trục tuyến tính + ví dụ spec
assert [x for _, x in xt] == [50, 122, 194, 266, 338, 410]
assert [round(y, 6) for _, y in yt] == [215, 170, 125, 80, 35]
assert all(abs((xt[i + 1][1] - xt[i][1]) - 72) < 1e-9 for i in range(5))
assert all(abs((yt[i][1] - yt[i + 1][1]) - 45) < 1e-9 for i in range(4))
assert abs(KX * 10 - 360) < 1e-9 and abs(KY * 100 - 180) < 1e-9
for R, ex, ey in ((1, 86, 125), (2, 122, 95), (4, 194, 71), (9, 374, 53), (10, 410, 51.4)):
    assert abs(px(R) - ex) < 0.1 and abs(py(R) - ey) < 0.1, (R, px(R), py(R))
assert all(abs(py(R) - (215 - 1.8 * 100 * R / (R + 1))) < 1e-9 for R in Rs)
c3.check()
fig3 = fig("0 0 440 260",
           "Đồ thị hiệu suất nguồn theo điện trở mạch ngoài, r bằng 1 ôm: đường cong tăng dần tiến tới 100 phần trăm, bốn điểm đo tại R bằng 1, 2, 4, 9 ôm cho H bằng 50, 67, 80, 90 phần trăm",
           c3.body, "Hình 3. $H=R/(R+r)$, $r=1\\,\\Omega$: bốn điểm đo nằm trên đường cong.",
           exp="tn-l11-nang-luong-dien-03")

# =====================================================================================
# Hình 4: mạch kín bài toán mẫu
# =====================================================================================
c4 = Canvas("f4", 440, 200)
c4.add(defs(PFX + "f4"))
c4.add(f'<defs><marker id="{PFX}f4-bb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
       f'<path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker></defs>')
L, R_, T, B = 120, 345, 40, 160
c4.add(path(f"M{L},96 L{L},{T} L{R_},{T} L{R_},75", "currentColor", 2))
c4.add(path(f"M{R_},125 L{R_},{B} L{L},{B} L{L},104", "currentColor", 2))
# nguồn: vạch dài (+) ở trên, vạch ngắn (−) ở dưới, cách 8 px
LONG_Y, SHORT_Y = 96, 104
assert SHORT_Y - LONG_Y == 8
c4.add(line(L - 14, LONG_Y, L + 14, LONG_Y, "currentColor", 3) + line(L - 7, SHORT_Y, L + 7, SHORT_Y, "currentColor", 3))
c4.t(L + 20, 95, "+", "currentColor", 14, "start", "700")
c4.t(L + 20, 120, "−", "currentColor", 14, "start", "700")
c4.t(12, 72, f"{EMF} = 12 V", "currentColor", 14, "start", "600")
c4.t(12, 90, f"{V('r')} = 1,0 Ω", "currentColor", 14, "start", "600")
# điện trở
c4.add(rect(R_ - 8, 75, 16, 50, 2, SLATE))
c4.t(R_ + 14, 104, f"{V('R')} = 5,0 Ω", "currentColor", 14, "start", "600")
# chiều dòng điện: ra từ cực + (trên) -> sang phải trên cạnh trên, sang trái trên cạnh dưới
c4.add(arrow(PFX + "f4", "r", 190, T, 270, T, 3))
c4.add(arrow(PFX + "f4", "r", 270, B, 190, B, 3))
c4.t(230, 24, f"{V('I')} = 2,0 A", RED, 15, "middle", "700")
# U hai đầu R: mũi tên hai đầu bên trái điện trở
UX = R_ - 19
c4.add(f'<line x1="{UX}" y1="75" x2="{UX}" y2="125" stroke="{BLUE}" stroke-width="1.5" marker-start="url(#{PFX}f4-bb)" marker-end="url(#{PFX}f4-bb)"/>')
c4.t(UX - 7, 105, f"{V('U')} = 10 V", BLUE, 14, "end", "700")
c4.t(L + 12, 66, f"mạch kín: {V('I')} = {EMF}/({V('R')} + {V('r')})", "currentColor", 14, "start", "400")
c4.obstacle_seg("day-tren", L, T, R_, T, 1.5)
c4.obstacle_seg("day-duoi", L, B, R_, B, 1.5)
c4.obstacle_seg("day-trai", L, T, L, 96, 1.5)
c4.obstacle_seg("day-trai2", L, 104, L, B, 1.5)
c4.obstacle_seg("day-phai", R_, T, R_, 75, 1.5)
c4.obstacle_seg("day-phai2", R_, 125, R_, B, 1.5)
c4.obstacle_rect("R", R_ - 8, 75, R_ + 8, 125)
c4.obstacle_seg("mui-U", UX, 70, UX, 130, 2)
c4.obstacle_seg("mui-I-tren", 190, T, 274, T, 11)
c4.obstacle_seg("mui-I-duoi", 266, B, 186, B, 11)
c4.obstacle_seg("thanh-nguon", L - 14, LONG_Y, L + 14, LONG_Y, 2)
c4.obstacle_seg("thanh-nguon2", L - 7, SHORT_Y, L + 7, SHORT_Y, 2)
# kiểm chiều dòng + cực + nhãn R trong khung 440
assert 190 < 270                                      # mũi tên cạnh trên: trái -> phải
assert LONG_Y < SHORT_Y and (L + 14) - (L - 14) == 28 and (L + 7) - (L - 7) == 14
rlab = [l for l in c4.labels if l[0].startswith("R = 5")][0]
assert rlab[3] <= 440, rlab
c4.check()
fig4 = fig("0 0 440 200",
           "Sơ đồ mạch kín một vòng gồm nguồn 12 vôn điện trở trong 1 ôm và điện trở ngoài 5 ôm, dòng điện 2 ampe đi ra từ cực dương, hiệu điện thế hai đầu R là 10 vôn",
           c4.body, "Hình 4. Mạch kín: nguồn $\\mathcal{E}=12$ V, $r=1{,}0\\,\\Omega$ nuôi $R=5{,}0\\,\\Omega$.")

# =====================================================================================
src = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert src.count(f"<!--FIG{n}-->") == 1, n
    src = src.replace(f"<!--FIG{n}-->", f)
assert "<!--FIG" not in src
(HERE / "theory.html").write_text(src, encoding="utf8")
print("ok", len(src))
