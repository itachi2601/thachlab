#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài 24 Nguồn điện (lesson 43), thay <!--FIGn--> trong theory.src.html -> theory.html.
Chạy lại được (idempotent). Kiểm bằng toạ độ: chiều mũi tên, chấm trên đường, trục tuyến tính,
nhãn không chồng nhau / không chồng nét / không vượt viewBox. Toạ độ hình 3 TÍNH từ phương trình U = E − I·r."""
import html
import math
import pathlib
import re
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
# Suất điện động: glyph ℰ (U+2130) vẽ nhỏ như "ε" trên Mac, có thể thiếu trên Android
# -> dùng E nghiêng (serif), nhất quán cả 4 hình. Muốn đổi về ℰ: EMF = "ℰ".
EMF = '<tspan font-style="italic" font-family="Georgia,\'Times New Roman\',serif" font-size="1.1em">E</tspan>'
SLATE = "rgba(148,163,184,.18)"


def it(s):
    """Chữ nghiêng (biến vật lí) trong <text>."""
    return f'<tspan font-style="italic" font-family="Georgia,\'Times New Roman\',serif" font-size="1.1em">{s}</tspan>'


def sub(s):
    return f'<tspan baseline-shift="sub" font-size="11">{s}</tspan>'


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, cap=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    k = f' stroke-linecap="{cap}"' if cap else ""
    return (f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" '
            f'stroke-width="{w}"{d}{k} opacity="{op}"/>')


def poly(pts, c, w=2.4, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{d} opacity="{op}" points="'
            + " ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + '"/>')


def dot(x, y, r=5, c="currentColor", stroke=""):
    s = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="{c}"{s}/>'


def circ(x, y, r, fill="none", c="currentColor", sw=2, op=1):
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}" opacity="{op}"/>'


def rect(x, y, w, h, rx=0, fill="none", c="currentColor", sw=2, op=1):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}" opacity="{op}"/>'


def fig(vb, label, body, cap, exp=None):
    s = wrap(vb, label, body, cap)
    if exp:
        s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
    return s


def mk(prefix, name, color, size):
    """Marker mũi tên cỡ cố định (userSpaceOnUse): đỉnh mũi cách đầu đường đúng `size` px."""
    return (f'<marker id="{prefix}-{name}" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="{size}" markerHeight="{size}" '
            f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')


COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}


class Canvas:
    """Gom thân SVG + hộp nhãn + vật cản + mũi tên để kiểm hình học."""
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.obst, self.arrows = "", [], [], {}
        self.markers = set()

    def add(self, s):
        self.body += s

    def arr(self, tag, c, x1, y1, x2, y2, w=2.5, head=9, dash="", op=1, obstacle_pad=None):
        """Mũi tên mà ĐỈNH nằm đúng (x2, y2); thân dừng lại `head` px trước đỉnh."""
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * head, y2 - uy * head
        self.markers.add((c, head))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += (f'<line x1="{x1:g}" y1="{y1:g}" x2="{ex:.2f}" y2="{ey:.2f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
                      f'opacity="{op}" marker-end="url(#{self.name}-{c}{head})"/>')
        self.arrows[tag] = (x1, y1, x2, y2)
        if obstacle_pad is not None:
            self.obstacle_seg(tag, x1, y1, x2, y2, obstacle_pad)

    def defs(self):
        return "<defs>" + "".join(mk(self.name, f"{c}{h}", COL[c], h) for c, h in sorted(self.markers)) + "</defs>"

    def t(self, x, y, s, c="currentColor", size=13, anchor="start", weight="600", tag=None, op=1):
        vis = html.unescape(re.sub(r"<[^>]+>", "", s))
        wd = 0.55 * size * len(vis)
        x0 = x if anchor == "start" else x - wd / 2 if anchor == "middle" else x - wd
        self.labels.append((tag or vis, x0, y - 0.8 * size, x0 + wd, y + 0.25 * size))
        o = f' opacity="{op}"' if op != 1 else ""
        self.body += text(x, y, s, c, size, anchor, weight).replace("<text ", f"<text{o} ", 1) if o else text(x, y, s, c, size, anchor, weight)

    def obstacle_pts(self, name, pts, pad=1.5):
        self.obst.append((name, [(float(x), float(y)) for x, y in pts], pad))

    def obstacle_seg(self, name, x1, y1, x2, y2, pad=1.5):
        n = max(2, int(math.hypot(x2 - x1, y2 - y1) / 2))
        self.obstacle_pts(name, [(x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n) for i in range(n + 1)], pad)

    def obstacle_circle(self, name, cx, cy, r, pad=1.5):
        self.obstacle_pts(name, [(cx + r * math.cos(2 * math.pi * i / 72), cy + r * math.sin(2 * math.pi * i / 72)) for i in range(72)], pad)

    def obstacle_rect_outline(self, name, x0, y0, x1, y1, pad=1.5):
        for k, (a, b, c_, d) in enumerate(((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0))):
            self.obstacle_seg(f"{name}{k}", a, b, c_, d, pad)

    def check(self, allow=()):
        M = 1
        for nm, x0, y0, x1, y1 in self.labels:
            assert x0 >= M and y0 >= M and x1 <= self.w - M and y1 <= self.h - M, (self.name, "vượt viewBox", nm, x0, y0, x1, y1)
        for i, a in enumerate(self.labels):
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    raise AssertionError((self.name, "hai nhãn chồng nhau", a[0], b[0]))
        for nm, x0, y0, x1, y1 in self.labels:
            for on, g, pad in self.obst:
                if (nm, on) in allow:
                    continue
                for px, py in g:
                    if x0 - pad <= px <= x1 + pad and y0 - pad <= py <= y1 + pad:
                        raise AssertionError((self.name, "nhãn chồng nét", nm, on, round(px), round(py)))

    def svg_body(self):
        return self.defs() + self.body


# =====================================================================================
# Hình 1 — hai quả cầu nối dây: dòng chỉ chạy một lát
# =====================================================================================
c1 = Canvas("f1", 440, 180)
c1.t(112, 24, "Lúc mới nối", ORG, 13, "middle", "600")
c1.t(327, 24, "Một lát sau", ORG, 13, "middle", "600")
c1.add(line(220, 30, 220, 165, "currentColor", 1.2, "4 4", .3))
c1.obstacle_seg("phan-cach", 220, 30, 220, 165, 1)
# --- khung trái
AX, BX, CY, RR = 60, 165, 80, 22
for cx, lab in ((AX, "A"), (BX, "B")):
    c1.add(circ(cx, CY, RR, "rgba(148,163,184,.15)"))
    c1.t(cx, CY + 5, lab, "currentColor", 14, "middle", "700")
    c1.obstacle_circle(f"cau{lab}", cx, CY, RR)
c1.t(AX, 48, f"+{it('q')}", RED, 14, "middle", "700")
c1.t(BX, 48, f"−{it('q')}", BLUE, 14, "middle", "700")
c1.add(line(AX + RR, CY, BX - RR, CY, "currentColor", 2))
c1.obstacle_seg("day-trai", AX + RR, CY, BX - RR, CY, 1.5)
left_start = len(c1.body)
c1.arr("e-trai", "b", 135, 64, 92, 64, 2.5, 9, obstacle_pad=5)       # electron: B -> A (sang trái)
c1.t(113, 55, "electron", BLUE, 13, "middle", "600")
c1.arr("I-trai", "r", 92, 96, 135, 96, 2.5, 9, obstacle_pad=5)      # dòng điện I: A -> B (sang phải)
c1.t(113, 114, it("I"), RED, 14, "middle", "700")
c1.t(112, 150, f"{it('V')}{sub('A')} &gt; {it('V')}{sub('B')}: có dòng", "currentColor", 14, "middle", "600")
# --- khung phải
RA, RB = 275, 380
for cx, lab in ((RA, "A"), (RB, "B")):
    c1.add(circ(cx, CY, RR, "rgba(148,163,184,.15)"))
    c1.t(cx, CY + 5, lab, "currentColor", 14, "middle", "700")
    c1.obstacle_circle(f"cau{lab}-p", cx, CY, RR)
    c1.t(cx, 48, "0", "currentColor", 14, "middle", "700")
right_start = len(c1.body)
c1.add(line(RA + RR, CY, RB - RR, CY, "currentColor", 2))
c1.obstacle_seg("day-phai", RA + RR, CY, RB - RR, CY, 1.5)
c1.t(327, 150, f"{it('V')}{sub('A')} = {it('V')}{sub('B')}: dòng ngừng", "currentColor", 14, "middle", "600")
right_body = c1.body[right_start:]
# assert: electron về A (x_đầu > x_cuối), I về B (x_đầu < x_cuối), khung phải không mũi tên
ex1, _, ex2, _ = c1.arrows["e-trai"]; ix1, _, ix2, _ = c1.arrows["I-trai"]
assert ex1 > ex2 and ex2 > AX + RR and ix1 < ix2 and ix2 < BX - RR
assert ex1 - ex2 == ix2 - ix1 == 43                      # hai mũi tên dài bằng nhau
assert "marker-end" not in right_body
c1.check()
fig1 = fig("0 0 440 180",
           "Hai quả cầu A dương và B âm nối dây: lúc đầu electron chạy từ B sang A, dòng điện từ A sang B; sau một lát hai quả cầu trung hoà, dòng ngừng.",
           c1.svg_body(), "Hình 1. Dòng chỉ chạy một lát")

# =====================================================================================
# Hình 2 — bên trong nguồn: lực lạ đẩy điện tích ngược điện trường
# =====================================================================================
c2 = Canvas("f2", 440, 240)
BX0, BY0, BW, BH = 140, 50, 150, 140
c2.add(rect(BX0, BY0, BW, BH, 8, SLATE, "currentColor", 2, 1))
c2.obstacle_rect_outline("hop", BX0, BY0, BX0 + BW, BY0 + BH, 1)
PX0, PW = 160, 110
c2.add(f'<rect x="{PX0}" y="58" width="{PW}" height="8" fill="{RED}" opacity="0.6"/>')
c2.add(f'<rect x="{PX0}" y="174" width="{PW}" height="8" fill="{BLUE}" opacity="0.6"/>')
c2.t(134, 67, "cực (+)", RED, 14, "end", "700")
c2.t(134, 183, "cực (−)", BLUE, 14, "end", "700")
CHX, CHY = 192, 125
c2.add(circ(CHX, CHY, 10, "rgba(251,146,60,.5)", "none", 0))
c2.t(CHX, CHY + 5, "+", "currentColor", 14, "middle", "700")
c2.obstacle_circle("dien-tich", CHX, CHY, 10, 0)
# lực lạ (đỏ, dài 41) từ (−) lên (+); lực điện (xanh, dài 25) xuống
c2.arr("luc-la", "r", CHX, 113, CHX, 72, 2.5, 9, obstacle_pad=4)
c2.t(200, 95, "lực lạ", RED, 14, "start", "700")
c2.arr("luc-dien", "b", CHX, 137, CHX, 162, 2.5, 9, obstacle_pad=4)
c2.t(200, 155, "lực điện", BLUE, 13, "start", "700")
# điện trường trong nguồn: mảnh, đứt nét, từ bản (+) xuống bản (−)
FX = 266
c2.arr("E-trong", "k", FX, 70, FX, 170, 1.5, 8, dash="4 3", op=.55, obstacle_pad=4)
# nhãn xoay dọc "điện trường" nằm trong lề phải của hộp (x 270..290)
c2.add(f'<text x="281" y="120" fill="currentColor" font-size="13" font-weight="400" text-anchor="middle" opacity="0.75" '
       f'transform="rotate(90 281 120)">điện trường</text>')
c2.labels.append(("điện trường (xoay)", 276, 120 - 0.55 * 13 * 11 / 2, 288, 120 + 0.55 * 13 * 11 / 2))
# dòng điện trong nguồn: (−) lên (+)
c2.arr("I-nguon", "r", 172, 165, 172, 85, 1.5, 8, obstacle_pad=4)
c2.t(165, 129, it("I"), RED, 14, "end", "700")
# mạch ngoài (nét 2): (215,58) lên (215,22) sang phải (400,22) xuống (400,218) sang trái (215,218) lên (215,182); đèn ở (400,120)
WIRE = [(215, 58), (215, 22), (400, 22), (400, 106)], [(400, 134), (400, 218), (215, 218), (215, 182)]
for seg in WIRE:
    c2.add(poly(seg, "currentColor", 2))
    for (xa, ya), (xb, yb) in zip(seg, seg[1:]):
        c2.obstacle_seg("day", xa, ya, xb, yb, 1.5)
LX, LY, LR = 400, 120, 14
c2.add(circ(LX, LY, LR, "rgba(251,191,36,.2)"))
d = LR * math.sqrt(0.5)
c2.add(line(LX - d, LY - d, LX + d, LY + d, "currentColor", 1.5) + line(LX - d, LY + d, LX + d, LY - d, "currentColor", 1.5))
c2.obstacle_circle("den", LX, LY, LR)
c2.t(LX - 20, LY + 4, "đèn", "currentColor", 13, "end", "600")
# ba mũi tên I ngoài: vòng theo chiều kim đồng hồ ra từ (+) về (−)
c2.arr("I-tren", "r", 300, 22, 340, 22, 2.5, 9, obstacle_pad=6)
c2.t(320, 12.4, it("I"), RED, 14, "middle", "700")
c2.arr("I-phai", "r", 400, 160, 400, 195, 2.5, 9, obstacle_pad=6)
c2.t(410, 182, it("I"), RED, 14, "start", "700")
c2.arr("I-duoi", "r", 340, 218, 300, 218, 2.5, 9, obstacle_pad=5)
c2.t(320, 235.5, it("I"), RED, 14, "middle", "700")
c2.t(345, 68, "mạch ngoài", ORG, 13, "middle", "600")
A = c2.arrows
ln = lambda k: math.hypot(A[k][2] - A[k][0], A[k][3] - A[k][1])
assert A["luc-la"][1] > A["luc-la"][3] and ln("luc-la") > ln("luc-dien")        # lạ: hướng lên, dài hơn lực điện
assert A["luc-dien"][1] < A["luc-dien"][3]                                       # điện: hướng xuống
assert A["E-trong"][1] < A["E-trong"][3]                                         # điện trường: (+) xuống (−)
assert A["I-nguon"][1] > A["I-nguon"][3]                                         # I trong nguồn: lên
assert A["I-tren"][0] < A["I-tren"][2] and A["I-duoi"][0] > A["I-duoi"][2] and A["I-phai"][1] < A["I-phai"][3]  # vòng kim đồng hồ
assert ln("luc-la") == 41 and ln("luc-dien") == 25
assert A["luc-la"][3] > 66 and A["luc-dien"][3] < 174                            # mũi tên nằm giữa hai bản
c2.check(allow={("+", "luc-la"), ("+", "luc-dien")})                              # chữ "+" nằm trong điện tích, mũi tên bắt đầu ở mép nó
fig2 = fig("0 0 440 240",
           "Mạch kín gồm nguồn và bóng đèn. Ở mạch ngoài dòng điện đi từ cực dương qua đèn về cực âm. Bên trong nguồn, lực lạ đẩy điện tích dương từ cực âm lên cực dương, ngược chiều điện trường và lực điện; dòng điện trong nguồn đi từ cực âm lên cực dương.",
           c2.svg_body(), "Hình 2. Lực lạ đẩy ngược điện trường")

# =====================================================================================
# Hình 3 — đồ thị U theo I của pin: U = 1,50 − 1,0·I
# =====================================================================================
c3 = Canvas("f3", 440, 300)
EMFV, RIN = 1.50, 1.0                       # V, Ω
OX, OY, KI, KU = 60, 250, 218.75, 137.5     # gốc, px/A, px/V
px = lambda I: OX + KI * I
py = lambda U: OY - KU * U
U_of = lambda I: EMFV - RIN * I
c3.add(poly([(OX, OY), (420, OY)], "currentColor", 2))
c3.add(poly([(OX, OY), (OX, 22)], "currentColor", 2))
c3.arr("truc-I", "k", 405, OY, 420, OY, 2, 9)
c3.arr("truc-U", "k", OX, 37, OX, 22, 2, 9)
xt = [(I, px(I)) for I in (0.5, 1.0, 1.5)]
yt = [(U, py(U)) for U in (0.5, 1.0, 1.5)]
for I, x in xt:
    c3.add(line(x, OY, x, OY + 5, "currentColor", 1.5))
    c3.t(x, 268, f"{I:.1f}".replace(".", ","), "currentColor", 14, "middle", "400")
for U, y in yt:
    c3.add(line(OX - 5, y, OX, y, "currentColor", 1.5))
    c3.t(OX - 8, y + 4, f"{U:.1f}".replace(".", ","), "currentColor", 14, "end", "400")
c3.t(52, 262, "0", "currentColor", 14, "end", "400")
c3.t(420, 288, f"{it('I')} (A)", "currentColor", 14, "end", "700")
c3.t(66, 18, f"{it('U')} (V)", "currentColor", 14, "start", "700")
# tam giác độ dốc (nét mảnh): (0,10; 1,40) -> ngang tới I = 0,60 -> xuống (0,60; 0,90)
P1, P5 = (px(0.10), py(U_of(0.10))), (px(0.60), py(U_of(0.60)))
c3.add(poly([P1, (P5[0], P1[1]), P5], "currentColor", 1.3, "", .6))
c3.obstacle_seg("tam-giac-ngang", P1[0], P1[1], P5[0], P1[1], 1)
c3.obstacle_seg("tam-giac-doc", P5[0], P1[1], P5[0], P5[1], 1)
# đường thẳng: liền tới I = 0,70, đứt nét tới đoản mạch I = 1,5
I_sc = EMFV / RIN
solid_end = 0.70
c3.add(poly([(px(0), py(U_of(0))), (px(solid_end), py(U_of(solid_end)))], GRN, 2.2))
c3.add(poly([(px(solid_end), py(U_of(solid_end))), (px(I_sc), py(U_of(I_sc)))], GRN, 2.2, "6 4"))
c3.obstacle_pts("duong", [(px(i / 100), py(U_of(i / 100))) for i in range(0, 151)], 2.5)
# 5 điểm dữ liệu
DATA = [(0.10, 1.40), (0.15, 1.35), (0.30, 1.20), (0.50, 1.00), (0.60, 0.90)]
SPEC_XY = [(81.9, 57.5), (92.8, 64.4), (125.6, 85.0), (169.4, 112.5), (191.3, 126.3)]
for (I, U), (sx, sy) in zip(DATA, SPEC_XY):
    assert abs(U - U_of(I)) < 1e-9, (I, U)
    assert abs(px(I) - sx) < 0.5 and abs(py(U) - sy) < 0.5, (I, U, px(I), py(U))
    c3.add(dot(round(px(I), 3), round(py(U), 3), 4.5, GRN, "currentColor"))
c3.obstacle_pts("diem", [(px(I), py(U)) for I, U in DATA], 5.5)
# giao trục
c3.add(dot(px(0), py(EMFV), 4, RED))
c3.add(dot(px(I_sc), py(0), 4, RED))
c3.t(68, 37, f"{EMF} = 1,50 V", RED, 14, "start", "700")
c3.t(428, 210, "đoản mạch", RED, 14, "end", "700")
c3.t(428, 227, "1,5 A", RED, 14, "end", "700")
c3.t(136, 52, f"Δ{it('I')} = 0,50 A", "currentColor", 13, "middle", "600")
c3.t(197, 95, f"Δ{it('U')} = −0,50 V", "currentColor", 13, "start", "600")
c3.t(197, 113, f"độ dốc = −{it('r')} = −1,0 Ω", GRN, 14, "start", "700")
c3.obstacle_seg("truc-x", OX, OY, 420, OY, 1)
c3.obstacle_seg("truc-y", OX, OY, OX, 22, 1)
c3.obstacle_pts("cham-do", [(px(0), py(EMFV)), (px(I_sc), py(0))], 5)
# --- assert hình học
assert abs(px(0) - 60) < 1e-9 and abs(py(EMFV) - 43.75) < 1e-9 and abs(px(I_sc) - 388.125) < 1e-9 and abs(py(0) - 250) < 1e-9
assert abs(py(U_of(solid_end)) - 140.0) < 1e-9 and abs(px(solid_end) - 213.125) < 1e-9
assert all(abs((xt[i + 1][1] - xt[i][1]) - 109.375) < 1e-9 for i in range(2)) and abs((xt[0][1] - OX) - 109.375) < 1e-9
assert all(abs((yt[i][1] - yt[i + 1][1]) - 68.75) < 1e-9 for i in range(2)) and abs((OY - yt[0][1]) - 68.75) < 1e-9
assert abs(KI * 1.6 - 350) < 1e-9 and abs(KU * 1.6 - 220) < 1e-9
assert abs(-(P5[1] - P1[1]) / (P5[0] - P1[0]) * KI / KU - (-RIN)) < 1e-9         # độ dốc đo bằng pixel = −r
assert [round(px(I), 1) for I, _ in xt] == [169.4, 278.8, 388.1]
assert [round(py(U), 2) for U, _ in yt] == [181.25, 112.5, 43.75]
c3.check()
fig3 = fig("0 0 440 300",
           "Đồ thị hiệu điện thế hai cực U theo cường độ dòng điện I của pin: năm điểm đo nằm trên đường thẳng dốc xuống, cắt trục U tại 1,50 vôn là suất điện động và cắt trục I tại 1,5 ampe là dòng đoản mạch; độ dốc bằng trừ r bằng trừ 1,0 ôm.",
           c3.svg_body(), "Hình 3. U giảm tuyến tính theo I", exp="tn-l11-nguon-dien-02")

# =====================================================================================
# Hình 4 — sơ đồ mạch kín của bài toán mẫu
# =====================================================================================
c4 = Canvas("f4", 440, 210)
L, R_, T, B = 70, 380, 40, 170
LONG_Y, SHORT_Y = 97, 113
wires = [
    [(L, T), (L, LONG_Y)], [(L, SHORT_Y), (L, B)],                         # cạnh trái, ngắt ở nguồn
    [(L, T), (211, T)], [(239, T), (R_, T), (R_, 85)],                     # cạnh trên, ngắt ở ampe kế
    [(R_, 125), (R_, B), (L, B)],                                          # cạnh phải (dưới R) + cạnh dưới
]
for seg in wires:
    c4.add(poly(seg, "currentColor", 2))
    for (xa, ya), (xb, yb) in zip(seg, seg[1:]):
        c4.obstacle_seg("day", xa, ya, xb, yb, 1.5)
# nguồn: vạch dài mảnh (+) ở trên, vạch ngắn dày (−) ở dưới
c4.add(line(52, LONG_Y, 88, LONG_Y, "currentColor", 2) + line(60, SHORT_Y, 80, SHORT_Y, "currentColor", 4))
c4.obstacle_seg("vach-dai", 52, LONG_Y, 88, LONG_Y, 2)
c4.obstacle_seg("vach-ngan", 60, SHORT_Y, 80, SHORT_Y, 3.5)
c4.t(44, 94, "+", RED, 14, "end", "700")
c4.t(44, 118, "−", BLUE, 14, "end", "700")
# vôn kế song song với nguồn, trong vòng
VX, VY, VR = 160, 105, 14
for seg in ([(L, 85), (VX, 85), (VX, VY - VR)], [(L, 125), (VX, 125), (VX, VY + VR)]):
    c4.add(poly(seg, "currentColor", 1.6))
    for (xa, ya), (xb, yb) in zip(seg, seg[1:]):
        c4.obstacle_seg("day-vonke", xa, ya, xb, yb, 1.5)
c4.add(dot(L, 85, 3) + dot(L, 125, 3))
c4.add(circ(VX, VY, VR, "rgba(148,163,184,.12)"))
c4.t(VX, VY + 5, "V", "currentColor", 14, "middle", "700")
c4.obstacle_circle("vonke", VX, VY, VR)
# ampe kế nối tiếp trên cạnh trên
AX_, AY_ = 225, T
c4.add(circ(AX_, AY_, 14, "rgba(148,163,184,.12)"))
c4.t(AX_, AY_ + 5, "A", "currentColor", 14, "middle", "700")
c4.obstacle_circle("ampe", AX_, AY_, 14)
# điện trở R
c4.add(rect(R_ - 10, 85, 20, 40, 0, "rgba(148,163,184,.12)", "currentColor", 2))
c4.obstacle_rect_outline("R", R_ - 10, 85, R_ + 10, 125, 1)
c4.t(362, 109, f"{it('R')} = 8,0 Ω", "currentColor", 14, "end", "700")
# nguồn: nhãn E, r nằm trong vòng, dưới nhánh vôn kế
c4.t(84, 148, f"{EMF} = 9,0 V", "currentColor", 14, "start", "700")
c4.t(84, 164.5, f"{it('r')} = 1,0 Ω", "currentColor", 14, "start", "700")
# dòng điện I: ra từ (+) -> sang phải ở cạnh trên, sang trái ở cạnh dưới
c4.arr("I-tren", "r", 290, T, 330, T, 2.5, 9, obstacle_pad=6)
c4.t(310, 29, it("I"), RED, 14, "middle", "700")
c4.arr("I-duoi", "r", 250, B, 210, B, 2.5, 9, obstacle_pad=6)
c4.t(230, 189, it("I"), RED, 14, "middle", "700")
A = c4.arrows
assert A["I-tren"][0] < A["I-tren"][2] and A["I-duoi"][0] > A["I-duoi"][2]       # vòng kim đồng hồ, ra từ (+) ở trên
assert LONG_Y < SHORT_Y                                                         # vạch dài (+) nằm trên vạch ngắn (−)
assert 85 < LONG_Y and 125 > SHORT_Y                                            # vôn kế nối vào hai bên nguồn
rl = [l for l in c4.labels if l[0].startswith("R =")][0]
assert rl[3] <= 362 and max(l[3] for l in c4.labels) <= 428
c4.check()
fig4 = fig("0 0 440 210",
           "Sơ đồ mạch kín: nguồn có suất điện động 9,0 vôn và điện trở trong 1,0 ôm trên cạnh trái, vôn kế mắc vào hai cực nguồn, ampe kế nối tiếp trên cạnh trên, điện trở 8,0 ôm trên cạnh phải; dòng điện đi từ cực dương qua ampe kế, qua R, về cực âm.",
           c4.svg_body(), "Hình 4. Mạch kín bài toán mẫu")

# =====================================================================================
src = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert src.count(f"<!--FIG{n}-->") == 1, n
    src = src.replace(f"<!--FIG{n}-->", f)
assert "<!--FIG" not in src
assert "$" not in "".join(re.findall(r"<text.*?</text>", src, flags=re.S))
(HERE / "theory.html").write_text(src, encoding="utf8")
print("ok", len(src))
