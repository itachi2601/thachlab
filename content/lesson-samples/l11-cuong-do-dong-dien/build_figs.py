#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài Cường độ dòng điện (lesson 41) và thay <!--FIGn--> trong theory.src.html -> theory.html.
Chạy lại được. Toạ độ/đồ thị tính từ phương trình và kiểm bằng assert; nhãn kiểm không chồng, không vượt viewBox."""
import math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
CC = "currentColor"


class Fig:
    """Gom phần tử + ghi lại khung chữ (ước lượng 0,55·cỡ chữ·số ký tự) để kiểm chồng/tràn."""
    def __init__(self, prefix, w, h):
        self.p, self.w, self.h, self.boxes = prefix, w, h, []
        self.parts = [defs(prefix) + self._k()]

    def _k(self):
        return (f'<defs><marker id="{self.p}-k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>')

    def add(self, s):
        self.parts.append(s)

    def line(self, x1, y1, x2, y2, c=CC, w=2, dash="", op=1, marker="", start=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op != 1 else ""
        m = f' marker-end="url(#{self.p}-{marker})"' if marker else ""
        m += f' marker-start="url(#{self.p}-{start})"' if start else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}{o}{m}/>')

    def text(self, x, y, segs, c=CC, size=11, anchor="start", weight="600", italic=False, reg=True, serif=False):
        size = max(size, 13)
        """segs: chuỗi hoặc danh sách [chuỗi | ("sub", chuỗi)]."""
        if isinstance(segs, str):
            segs = [segs]
        inner, width = "", 0.0
        for sg in segs:
            if isinstance(sg, tuple):
                inner += f'<tspan baseline-shift="sub" font-size="11">{sg[1]}</tspan>'
                width += 0.55 * 11 * len(sg[1])
            else:
                inner += sg
                width += 0.55 * size * len(sg)
        it = ' font-style="italic"' if italic else ""
        if serif:
            it += ' font-family="Georgia, \'Times New Roman\', serif" font-style="italic"'
            if italic: it = it.replace(' font-style="italic"','',1)
        self.add(f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{it}>{inner}</text>')
        x0 = x if anchor == "start" else x - width if anchor == "end" else x - width / 2
        if reg:
            self.boxes.append((x0, y - size * 0.8, x0 + width, y + size * 0.2, "".join(s if isinstance(s, str) else s[1] for s in segs)))

    def dot(self, x, y, r, fill, stroke="", sw=1):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{st}/>')

    def check(self):
        for x0, y0, x1, y1, s in self.boxes:
            assert x0 >= 8 and x1 <= self.w - 4 and y0 >= 0 and y1 <= self.h, (self.p, "nhãn vượt viewBox", s, x0, x1, y0, y1)
        for i, a in enumerate(self.boxes):
            for b in self.boxes[i + 1:]:
                assert not (a[0] < b[2] + 1 and b[0] < a[2] + 1 and a[1] < b[3] and b[1] < a[3]), (self.p, "nhãn chồng", a[4], b[4])

    def html(self, label, cap, exp=None):
        self.check()
        s = wrap(f"0 0 {self.w} {self.h}", label, "".join(self.parts), cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s


def poly(f, pts, c, w=2.5, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{op}"' if op != 1 else ""
    f.add(f'<polyline fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"{d}{o} points="'
          + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')


# ============================================================ Hình 1: mạch kín, chiều I và chiều electron
f = Fig("f1", 420, 230)
TOP, BOT, LX, RX = 50, 180, 60, 360
PIN_L, PIN_S = 108, 122            # vạch dài (cực +) nằm trên vạch ngắn (cực −)
AX, AR = 210, 20                   # ampe kế
BX, BY, BR = 360, 115, 18          # bóng đèn
# dây (nét 2), ngắt chỗ ampe kế, đèn, pin
for seg in ((LX, TOP, AX - AR, TOP), (AX + AR, TOP, RX, TOP), (RX, TOP, RX, BY - BR), (RX, BY + BR, RX, BOT),
            (RX, BOT, LX, BOT), (LX, BOT, LX, PIN_S), (LX, PIN_L, LX, TOP)):
    f.line(*seg, CC, 2)
# pin
f.line(LX - 15, PIN_L, LX + 15, PIN_L, CC, 3)
f.line(LX - 8, PIN_S, LX + 8, PIN_S, CC, 1.5)
f.text(82, PIN_L + 5, "+", CC, 14, "start", "700")
f.text(82, PIN_S + 5, "−", CC, 14, "start", "700")
f.text(12, 120, "Pin", CC, 12, "start", "700")
# ampe kế
f.add(f'<circle cx="{AX}" cy="{TOP}" r="{AR}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
f.text(AX, TOP + 6, "A", BLUE, 16, "middle", "700")
f.text(AX, 22, "nối tiếp", CC, 11, "middle", "600")
# bóng đèn
f.add(f'<circle cx="{BX}" cy="{BY}" r="{BR}" fill="none" stroke="currentColor" stroke-width="2"/>')
k = BR * math.sqrt(0.5)
f.line(BX - k, BY - k, BX + k, BY + k, CC, 2)
f.line(BX - k, BY + k, BX + k, BY - k, CC, 2)
f.text(385, 119, "Đèn", CC, 12, "start", "700")
# mũi tên đỏ: dòng điện quy ước, chiều kim đồng hồ
RED_ARR = {"top": (100, TOP, 170, TOP), "right": (RX, 60, RX, 90), "bottom": (320, BOT, 250, BOT), "left": (LX, 170, LX, 145)}
for a in RED_ARR.values():
    f.line(*a, RED, 2.5, marker="r")
f.text(135, 42, "I", RED, 15, "middle", "700", serif=True)
# mũi tên xanh: electron, ngược chiều
BLU_ARR = {"top": (170, 64, 100, 64), "bottom": (250, 166, 320, 166)}
for a in BLU_ARR.values():
    f.line(*a, BLUE, 2, dash="4 3", marker="b")
for a in BLU_ARR.values():
    f.dot(a[0], a[1], 6, BLUE)
    f.text(a[0], a[1] + 4, "−", "#fff", 11, "middle", "700", reg=False)
f.text(135, 82, "electron", BLUE, 11, "middle", "600")
f.text(12, 215, "đỏ: chiều dòng điện · xanh: chiều electron", CC, 11, "start", "600")
# kiểm hướng
r, b_ = RED_ARR, BLU_ARR
assert r["top"][2] > r["top"][0] and r["right"][3] > r["right"][1] and r["bottom"][2] < r["bottom"][0] and r["left"][3] < r["left"][1]
assert b_["top"][2] < b_["top"][0] and b_["bottom"][2] > b_["bottom"][0]          # electron ngược chiều đỏ
assert PIN_L < PIN_S                                                                  # cực + ở trên
assert r["top"][1] == TOP and r["right"][0] == RX and r["bottom"][1] == BOT and r["left"][0] == LX   # mũi đỏ nằm trên dây
fig1 = f.html("Mạch kín gồm pin, ampe kế nối tiếp và bóng đèn; mũi tên đỏ chỉ chiều dòng điện từ cực dương qua mạch ngoài về cực âm, mũi tên xanh chỉ electron đi ngược chiều.",
              "Hình 1. Ampe kế mắc nối tiếp; dòng điện từ cực + qua mạch ngoài về cực −, electron ngược lại.",
              "tn-l11-cuong-do-dong-dien-01")

# ============================================================ Hình 2: Δq–Δt, I = 1,50 A
f = Fig("f2", 420, 260)
OX, OY = 60, 220
PX_T, PX_Q = 6.0, 0.04                       # px/phút, px/C
I_AMP = 1.50
SLOPE = I_AMP * 60                           # C/phút = 90
f.line(OX, OY, 400, OY, CC, 2, marker="k")
f.line(OX, OY, OX, 20, CC, 2, marker="k")
f.text(54, 238, "0", CC, 11, "end")
f.text(400, 255, "Δt (phút)", CC, 11, "end")
f.text(14, 16, "Δq (C)", CC, 11, "start")
ts = [10, 20, 30, 40, 50]
qs = [SLOPE * t for t in ts]                 # 900 … 4500
px = [OX + PX_T * t for t in ts]
py = [OY - PX_Q * q for q in qs]
for t, x in zip(ts, px):
    f.line(x, OY, x, OY + 5, CC, 1.5)
    f.text(x, 238, str(t), CC, 11, "middle")
for q, y in zip(qs, py):
    f.line(OX - 5, y, OX, y, CC, 1.5)
    f.text(54 - 4, y + 4, str(int(q)), CC, 11, "end")
T_END = 52
f.line(OX, OY, OX + PX_T * T_END, OY - PX_Q * SLOPE * T_END, RED, 2)
f.text(200, 60, "độ dốc = I = 1,50 A", RED, 11, "start", "600")
for x, y in zip(px, py):
    f.dot(x, y, 5, GRN, CC, 1)
# kiểm
assert [round(v) for v in qs] == [900, 1800, 2700, 3600, 4500]
assert [round(x, 6) for x in px] == [120, 180, 240, 300, 360] and [round(y, 6) for y in py] == [184, 148, 112, 76, 40]
for t, x, y in zip(ts, px, py):
    assert x == OX + 6 * t and abs(y - (220 - 0.04 * 90 * t)) < 0.5
assert len({round(b - a, 6) for a, b in zip(px, px[1:])}) == 1 and len({round(b - a, 6) for a, b in zip(py, py[1:])}) == 1   # chia tuyến tính
assert abs((py[0] - py[1]) / (px[1] - px[0]) - 0.6) < 1e-9                                                              # độ dốc trên hình = 3,6/6
fig2 = f.html("Đồ thị điện lượng theo thời gian: năm chấm số liệu nằm trên đường thẳng qua gốc, độ dốc bằng cường độ dòng điện 1,50 ampe.",
              "Hình 2. Dòng không đổi 1,50 A: điện lượng tỉ lệ với thời gian, độ dốc là I.",
              "tn-l11-cuong-do-dong-dien-02")

# ============================================================ Hình 3: hai đồ thị I–t
f = Fig("f3", 420, 192)
Y0, Y_TOP, IY = 130, 70, 70
for ox, tt, title, tx in ((40, "Không đổi", None, 110), (240, "Một chiều", None, 320)):
    f.line(ox, Y0, ox + 160, Y0, CC, 2, marker="k")
    f.line(ox, Y0, ox, 30, CC, 2, marker="k")
    f.text(ox + 156, 148, "t", CC, 12, "end")
    f.text(ox - 12, 34, "I", CC, 14, "end", serif=True)
    f.text(ox - 6, 146, "0", CC, 11, "end")
    f.text(tx, 20, tt, CC, 12, "middle", "700")
    f.text(ox - 6, IY + 4, ["I", ("sub", "0")], RED, 14, "end", "700", serif=True)
left = [(40, IY), (195, IY)]
poly(f, left, RED, 2.5)
f.line(240, IY, 400, IY, CC, 1, "3 3", .4)
bump = [(240 + s, Y0 - 60 * abs(math.sin(math.pi * s / 40))) for s in range(0, 161, 2)]
poly(f, bump, RED, 2.5)
f.text(12, 168, "cả hai: chiều không đổi", CC, 13, "start", "600")
f.text(12, 186, "chỉ bên trái cường độ cũng không đổi", CC, 13, "start", "600")
# kiểm
assert all(y == IY for _, y in left)
assert all(IY - 1e-9 <= y <= Y0 + 1e-9 for _, y in bump)                    # không bao giờ xuống dưới trục t
for xs in (260, 300, 340, 380):
    assert abs(dict(bump)[xs] - IY) < 1e-9
for xs in (240, 280, 320, 360, 400):
    assert abs(dict(bump)[xs] - Y0) < 1e-6
assert bump[0][0] == 240 and bump[-1][0] == 400
fig3 = f.html("Hai đồ thị cường độ dòng điện theo thời gian: bên trái đường nằm ngang là dòng không đổi, bên phải các bướu nửa sin nằm trên trục thời gian là dòng một chiều có cường độ thay đổi.",
              "Hình 3. Trái: dòng không đổi. Phải: dòng một chiều sau chỉnh lưu, chỉ chiều không đổi.")

# ============================================================ Hình 4: hình trụ v·Δt trước tiết diện S
f = Fig("f4", 420, 200)
PT, PB, XL, XR, YC = 60, 140, 30, 390, 100
XS, X0 = 270, 150                                           # tiết diện S; đầu trái hình trụ v·Δt
RYE = (PB - PT) / 2
f.line(XL, PT, XR, PT, CC, 2)
f.line(XL, PB, XR, PB, CC, 2)
f.add(f'<ellipse cx="{XR}" cy="{YC}" rx="10" ry="{RYE:.0f}" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="2"/>')
f.add(f'<path d="M{XL},{PT} A10,{RYE:.0f} 0 0 0 {XL},{PB}" fill="none" stroke="currentColor" stroke-width="2"/>')
f.add(f'<rect x="{X0}" y="{PT}" width="{XS - X0}" height="{PB - PT}" fill="{GRN}" fill-opacity="0.12"/>')
f.add(f'<ellipse cx="{X0}" cy="{YC}" rx="10" ry="{RYE:.0f}" fill="none" stroke="{GRN}" stroke-width="1.2" stroke-dasharray="4 3"/>')
f.add(f'<ellipse cx="{XS}" cy="{YC}" rx="10" ry="{RYE:.0f}" fill="{RED}" fill-opacity="0.15" stroke="{RED}" stroke-width="2" stroke-dasharray="5 3"/>')
f.line(XS, 34, XS, PT - 2, RED, 1.2)
f.text(XS, 30, "S", RED, 15, "middle", "700", serif=True)
f.text(32, 50, "n hạt trong mỗi m³", CC, 11, "start", "600")
IN = [(170, 80), (200, 118), (225, 85), (245, 125), (190, 100), (255, 100)]
OUT = [(90, 90), (115, 125), (330, 95)]
V_ARR = []
for cx, cy in IN + OUT:
    V_ARR.append((cx + 8, cy, cx + 24, cy))
    f.line(*V_ARR[-1], GRN, 2, marker="g")
for cx, cy in IN + OUT:
    f.dot(cx, cy, 7, ORG)
    f.text(cx, cy + 3.5, "+", "#fff", 11, "middle", "700", reg=False)
f.text(200, 70, "v", GRN, 12, "start", "700", italic=True)
f.line(X0, 160, XS, 160, CC, 1.5, marker="k", start="k")
f.text((X0 + XS) / 2, 178, "v·Δt", CC, 12, "middle", "700")
f.text(32, 178, "N = n·S·v·Δt hạt", GRN, 11, "start", "600")
I_ARR = (300, 190, 380, 190)
f.line(*I_ARR, RED, 3, marker="r")
f.text(340, 184, "I", RED, 15, "middle", "700", serif=True)
# kiểm
for cx, cy in IN:
    assert X0 + 7 <= cx <= XS - 7 and PT + 7 <= cy <= PB - 7, (cx, cy)
for cx, cy in OUT:
    assert cx < X0 - 7 or cx > XS + 7, (cx, cy)
assert all(a[2] > a[0] for a in V_ARR) and I_ARR[2] > I_ARR[0]
assert XS - X0 == 120                                                          # vùng tô dài v·Δt = 120 px
assert min(c for c, _ in IN) - 7 >= X0 and X0 < XS                              # hạt trong trụ nằm BÊN TRÁI S (phía đi tới)
for i, (a, b) in enumerate(IN + OUT):
    for c, d in (IN + OUT)[i + 1:]:
        assert math.hypot(a - c, b - d) >= 16, ((a, b), (c, d))                 # hạt không chồng nhau
fig4 = f.html("Đoạn dây dẫn hình trụ, tiết diện S vẽ nét đứt; các hạt tải điện dương nằm trong đoạn dài v nhân delta t phía trước S đang trôi sang phải sẽ đi qua S; mũi tên I cùng chiều với v.",
              "Hình 4. Hạt trong hình trụ dài v·Δt trước tiết diện S đi qua S trong Δt: N = nSvΔt.",
              "tn-l11-cuong-do-dong-dien-03")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert src.count(f"<!--FIG{n}-->") == 1, n
    src = src.replace(f"<!--FIG{n}-->", fg)
assert "<!--FIG" not in src
(HERE / "theory.html").write_text(src, encoding="utf8")
print("ok", len(src))
