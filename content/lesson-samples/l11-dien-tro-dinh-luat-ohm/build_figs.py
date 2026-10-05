#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài 23 Điện trở. Định luật Ohm (lesson 42) và thay <!--FIGn--> trong theory.src.html -> theory.html.
Chạy lại được. Mọi toạ độ đồ thị tính từ phương trình trong figs-spec.md và kiểm bằng assert;
nhãn chữ được kiểm không vượt viewBox, không chồng nhau, không đè nét/chấm (ước bề rộng chữ = 0,55·cỡ·số ký tự)."""
import math
import pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent


class Fig:
    """Gom phần tử SVG kèm dữ liệu hình học để kiểm va chạm nhãn."""

    def __init__(self, prefix, w, h):
        self.p, self.w, self.h = prefix, w, h
        self.parts = [defs(prefix) + self._k_marker()]
        self.texts, self.pts, self.rects = [], [], []

    def _k_marker(self):
        return (f'<marker id="{self.p}-k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker>')

    def raw(self, s):
        self.parts.append(s)

    def _sample(self, pts):
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            n = max(1, int(math.hypot(x2 - x1, y2 - y1)))
            for i in range(n + 1):
                self.pts.append((x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n))

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", marker="", op=1, obst=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{self.p}-{marker})"' if marker else ""
        o = f' opacity="{op}"' if op != 1 else ""
        self.parts.append(f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" stroke-width="{w}"{d}{o}{m}/>')
        if obst:
            self._sample([(x1, y1), (x2, y2)])

    def poly(self, pts, c="currentColor", w=2, dash="", marker="", closed=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{self.p}-{marker})"' if marker else ""
        tag = "polygon" if closed else "polyline"
        self.parts.append(f'<{tag} fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"{d}{m} points="'
                          + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')
        self._sample(pts + ([pts[0]] if closed else []))

    def circle(self, x, y, r, fill="none", stroke="currentColor", sw=2, op=1, obst=True):
        o = f' opacity="{op}"' if op != 1 else ""
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.parts.append(f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="{fill}"{s}{o}/>')
        if obst:
            self.rects.append((x - r, y - r, x + r, y + r))

    def rect(self, x, y, w, h, stroke="currentColor", sw=2, rx=0, op=1, obst=True):
        o = f' opacity="{op}"' if op != 1 else ""
        self.parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" fill="none" stroke="{stroke}" stroke-width="{sw}"{o}/>')
        if obst:
            self._sample([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)])

    def text(self, x, y, s, c="currentColor", size=12, anchor="start", weight="600", inside=False):
        self.parts.append(text(f"{x:g}", f"{y:g}", s, c, size, anchor, weight))
        plain = s.replace("&amp;", "&")
        wd = (0.58 if int(weight) >= 600 else 0.55) * size * len(plain)
        x0 = {"start": x, "middle": x - wd / 2, "end": x - wd}[anchor]
        self.texts.append((x0, y - size * 0.82, x0 + wd, y + size * 0.22, s, inside))

    def check(self, name):
        w, h, m = self.w, self.h, 1.5
        for i, (x0, y0, x1, y1, s, inside) in enumerate(self.texts):
            assert x0 >= 2 and y0 >= 2 and x1 <= w - 2 and y1 <= h - 2, f"{name}: nhãn '{s}' vượt viewBox ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})"
            if inside:
                continue
            for (a0, b0, a1, b1, s2, _) in self.texts[i + 1:]:
                assert x1 + m < a0 or a1 + m < x0 or y1 + m < b0 or b1 + m < y0, f"{name}: nhãn '{s}' chồng '{s2}'"
            for (px, py) in self.pts:
                assert not (x0 - m <= px <= x1 + m and y0 - m <= py <= y1 + m), f"{name}: nhãn '{s}' đè nét tại ({px:.0f},{py:.0f})"
            for (a0, b0, a1, b1) in self.rects:
                assert x1 + m < a0 or a1 + m < x0 or y1 + m < b0 or b1 + m < y0, f"{name}: nhãn '{s}' đè hình ({a0:.0f},{b0:.0f})"

    def html(self, label, cap, exp=None):
        s = wrap(f"0 0 {self.w} {self.h}", label, "".join(self.parts), cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s


def sub_ok(x, lo, hi):
    return lo <= x <= hi


# ======================= HÌNH 1: sơ đồ mạch đo
f = Fig("f1", 440, 210)
XL, XR, YT, YB = 40, 350, 40, 170
AX, VX = 180, 275                      # tâm ampe kế, vôn kế
# nguồn trên cạnh trái: vạch dài (+) ở trên, vạch ngắn (−) ở dưới
f.line(XL, YT, XL, 96)
f.line(28, 96, 52, 96, w=2.5)           # vạch dài = cực +
f.line(33, 108, 47, 108, w=4.5)         # vạch ngắn = cực −
f.line(XL, 108, XL, YB)
f.line(31, 121, 55, 87, w=1.8, marker="k")   # mũi tên chéo: điều chỉnh được
f.text(21, 96, "+", size=13, anchor="middle", weight="700")
f.text(18, 118, "−", size=13, anchor="middle", weight="700")
f.text(62, 100, "Nguồn", size=14, weight="600")
f.text(62, 116, "0–6 V", size=13, weight="400")
# cạnh trên: khoá K (hở), ampe kế
f.line(XL, YT, 92, YT)
f.circle(92, YT, 3, fill="currentColor", stroke="", obst=False); f.circle(118, YT, 3, fill="currentColor", stroke="", obst=False)
f.line(92, YT, 114, 27, w=2)
f.text(104, 20, "K", size=14, anchor="middle", weight="700")
f.line(118, YT, AX - 16, YT)
f.circle(AX, YT, 16, sw=2)
f.text(AX, YT + 5, "A", size=14, anchor="middle", weight="700", inside=True)
f.text(AX, 15, "nối tiếp", size=13, anchor="middle", weight="400")
f.line(AX + 16, YT, XR, YT)
# cạnh phải: điện trở R (hình chữ nhật đứng 16 × 44)
f.line(XR, YT, XR, 83)
f.rect(XR - 8, 83, 16, 44, stroke=BLUE, sw=2.5)
f.line(XR, 127, XR, YB)
f.text(366, 102, "R = 10 Ω", BLUE, 14, "start", "700")
f.text(366, 119, "(hoặc đèn)", "currentColor", 13, "start", "400")
# vôn kế song song với R
f.poly([(XR, 70), (VX, 70), (VX, 105 - 16)], w=2)
f.poly([(XR, 140), (VX, 140), (VX, 105 + 16)], w=2)
f.circle(XR, 70, 3, fill="currentColor", stroke="", obst=False); f.circle(XR, 140, 3, fill="currentColor", stroke="", obst=False)
f.circle(VX, 105, 16, sw=2)
f.text(VX, 110, "V", size=14, anchor="middle", weight="700", inside=True)
f.text(250, 109, "song song", size=13, anchor="end", weight="400")
# cạnh dưới + mũi tên chiều dòng I (phải -> trái)
f.line(XL, YB, XR, YB)
IA = (215, YB, 175, YB)
f.line(*IA, c=RED, w=3, marker="r", obst=False)
f.text(195, 158, "I", RED, 14, "middle", "700")
f.check("fig1")
assert IA[2] < IA[0], "mũi tên I phải chỉ sang trái ở cạnh dưới"
assert (96 < 108) and (52 - 28) > (47 - 33), "vạch dài (+) ở trên, ngắn (−) ở dưới"
fig1 = f.html("Sơ đồ mạch điện gồm nguồn điều chỉnh, khoá K, ampe kế nối tiếp với điện trở R, vôn kế mắc song song hai đầu R, mũi tên I chỉ chiều dòng điện.",
              "Hình 1. Mạch đo: ampe kế nối tiếp, vôn kế song song với linh kiện.",
              exp="tn-l11-dien-tro-ohm-01")


# ======================= Hệ trục chung cho HÌNH 2 và HÌNH 4
OX, OY, KU, KI = 50, 250, 55, 350      # x = 50 + 55·U ; y = 250 − 350·I


def px(u): return OX + KU * u
def py(i): return OY - KI * i


def axes(f):
    f.line(OX, OY, 400, OY, w=1.5, marker="k")
    f.line(OX, OY, OX, 25, w=1.5, marker="k")
    f.text(405, 290, "U (V)", size=14, anchor="end", weight="600")
    f.text(58, 22, "I (A)", size=14, anchor="start", weight="600")
    f.text(38, 268, "O", size=14, anchor="end", weight="600")
    xt = []
    for u in range(0, 7):
        x = px(u); xt.append(x)
        if u:
            f.line(x, OY, x, OY - 5, w=1.2)
        if u:
            f.text(x, 268, str(u), size=13, anchor="middle", weight="400")
    assert all(abs((xt[k + 1] - xt[k]) - 55) < 1e-9 for k in range(6)) and xt[0] == 50 and xt[-1] == 380
    yt = []
    for k in range(0, 7):
        y = py(k / 10); yt.append(y)
        if k:
            f.line(OX, y, OX + 5, y, w=1.2)
            f.text(44, y + 4, ("0," + str(k)), size=13, anchor="end", weight="400")
    assert all(abs((yt[k] - yt[k + 1]) - 35) < 1e-9 for k in range(6)) and yt[0] == 250 and abs(yt[-1] - 40) < 1e-9


def dot_pt(f, x, y):
    f.circle(x, y, 4, fill=GRN, stroke="currentColor", sw=1)


# ======================= HÌNH 2: đường đặc trưng của điện trở
f = Fig("f2", 420, 300)
axes(f)
f.line(px(0), py(0), px(5.6), py(0.56), c=BLUE, w=2.5)
assert abs(px(5.6) - 358) < 1e-9 and abs(py(0.56) - 54) < 1e-9
f.line(px(0), py(0), px(6), py(0.3), c=BLUE, w=2, dash="6 4")
assert (px(6), py(0.3)) == (380, 145)
meas2 = [(k, k / 10) for k in range(1, 6)]
for U, I in meas2:
    x, y = px(U), py(I)
    assert abs(x - (50 + 55 * U)) < 1e-9 and abs(y - (250 - 35 * U)) < 1e-9
    assert abs(y - (250 - 350 * U / 10)) < 1     # nằm trên đường R = 10 Ω
    dot_pt(f, x, y)
assert [(px(U), py(I)) for U, I in meas2] == [(105, 215), (160, 180), (215, 145), (270, 110), (325, 75)]
f.text(285, 80, "R = 10 Ω", BLUE, 14, "end", "700")
f.text(330, 184, "R = 20 Ω", BLUE, 14, "start", "700")
f.text(260, 45, "dốc hơn → R nhỏ hơn", "currentColor", 13, "start", "400")
f.check("fig2")
fig2 = f.html("Đồ thị I theo U: đường thẳng qua gốc của điện trở 10 Ω với năm điểm đo, và đường đứt thoải hơn của điện trở 20 Ω.",
              "Hình 2. Năm điểm đo của điện trở 10 Ω nằm trên đường thẳng I&nbsp;=&nbsp;U/10; đường đứt là 20 Ω.",
              exp="tn-l11-dien-tro-ohm-01")


# ======================= HÌNH 3: electron va chạm ion nút mạng
f = Fig("f3", 440, 230)
RION = 9
YE = 92.5                                    # hành lang giữa hàng 1 (y=70) và hàng 2 (y=115)
ROWS = (70, 115, 160)
cells = {"cold": (10, 35, "Kim loại lạnh", "currentColor"), "hot": (230, 255, "Kim loại nóng", ORG)}
ions_all = {}


def path_ok(pts, ions, clear):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        for (cx, cy) in ions:
            dx, dy = x2 - x1, y2 - y1
            t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)))
            d = math.hypot(x1 + t * dx - cx, y1 + t * dy - cy)
            assert d >= clear, f"đường electron cách ion ({cx},{cy}) chỉ {d:.1f}"


zig_len = {}
for key, (cx0, x0, title, tcol) in cells.items():
    f.rect(cx0, 8, 200, 200, sw=1, rx=8, op=.5, obst=False)
    f.text(cx0 + 100, 28, title, tcol, 14, "middle", "700")
    ions = [(x0 + 50 * j, y) for y in ROWS for j in range(4)]
    ions_all[key] = ions
    shadow = []
    for (ix, iy) in ions:
        if key == "hot":
            for dxs in (-4, 4):
                f.circle(ix + dxs, iy, RION, stroke=ORG, sw=1, op=.55, obst=True)
                shadow.append((ix + dxs, iy))
        f.circle(ix, iy, RION, stroke="currentColor", sw=1.5)
        f.text(ix, iy + 4, "+", size=13, anchor="middle", weight="700", inside=True)
    xs, xe = x0 - 15, x0 + 170
    if key == "cold":
        mid = [(x0 + 25, YE + 6), (x0 + 80, YE - 6), (x0 + 135, YE + 6)]
    else:
        mid = [(251, 82), (260, 103), (301, 82), (310, 103), (351, 82), (360, 103)]
        assert len(mid) == 6
        for (bx, by) in mid:   # mỗi điểm gấp khúc sát mép một ion (cách tâm ≈ 12 px)
            dmin = min(math.hypot(bx - cx, by - cy) for cx, cy in ions)
            assert 11.5 <= dmin <= 14.5, (bx, by, dmin)
    route = [(xs, YE)] + mid + [(xe, YE)]
    path_ok(route, ions + shadow, RION + 1.5)
    zig_len[key] = sum(abs(b[1] - a[1]) for a, b in zip(route, route[1:]))
    f.poly(route, c=RED, w=1.5, marker="r")
    f.circle(xs, YE, 4, fill=RED, stroke="", obst=False)
    f.line(xs - 2.5, YE, xs + 2.5, YE, c="#ffffff", w=1.3, obst=False)
    # mũi tên chiều trôi dưới ô
    f.line(cx0 + 8, 196, cx0 + 48, 196, c=RED, w=2.5, marker="r", obst=False)
    if key == "cold":
        f.text(cx0 + 55, 200, "electron trôi", RED, 13, "start", "600")
    else:
        f.text(cx0 + 55, 200, "va nhiều, trôi chậm", ORG, 13, "start", "600")
assert zig_len["hot"] >= 2 * zig_len["cold"], zig_len       # zigzag ô nóng mạnh gấp > 2 lần ô lạnh
assert len(ions_all["cold"]) == len(ions_all["hot"]) == 12
f.text(220, 222, "ion dương ở nút mạng (+) · electron tự do (−)", "currentColor", 13, "middle", "400")
f.check("fig3")
fig3 = f.html("Hai ô so sánh: trong kim loại lạnh electron đi gần thẳng qua mạng ion dương; trong kim loại nóng ion rung mạnh, electron va chạm liên tục, đường đi zigzag.",
              "Hình 3. Trái: kim loại lạnh, ion rung ít, electron đi gần thẳng. Phải: kim loại nóng, ion rung mạnh, electron va chạm nhiều, trôi chậm hơn.")


# ======================= HÌNH 4: đường đặc trưng của đèn sợi đốt
f = Fig("f4", 420, 300)
axes(f)
curve_I = lambda u: 0.1706 * u ** 0.6
spec_us = [k * 0.25 for k in range(0, 25)]      # 25 mẫu theo spec: 0, 0,25, …, 6,0
assert len(spec_us) == 25 and abs(spec_us[-1] - 6.0) < 1e-9
us = [k * 0.05 for k in range(0, 121)]          # lấy mẫu dày hơn (bước 0,05; chứa đủ 25 mẫu spec) để đoạn gần gốc không bị gãy góc
assert all(any(abs(u - v) < 1e-9 for u in us) for v in spec_us)
curve = [(px(u), py(curve_I(u))) for u in us]
assert curve[0] == (50, 250) and abs(curve[-1][0] - 380) < 1e-9 and abs(curve[-1][1] - 75) < 0.2
f.poly(curve, c=ORG, w=2.5)
f.line(px(0), py(0), px(6), py(0.5), c=BLUE, w=2, dash="6 4")
assert (px(6), py(0.5)) == (380, 75)
meas4 = [(1, .17), (2, .26), (3, .33), (4, .39), (5, .45), (6, .50)]
assert [(px(U), py(I)) for U, I in meas4] == [(105, 190.5), (160, 159), (215, 134.5), (270, 113.5), (325, 92.5), (380, 75)]
for U, I in meas4:
    assert abs(py(I) - py(curve_I(U))) < 2, (U, I)      # điểm đo cách đường cong < 2 px theo y
    dot_pt(f, px(U), py(I))
# các điểm giữa nằm PHÍA TRÊN đường thẳng 12 Ω (y nhỏ hơn); độ dốc giảm dần theo U
for U, I in meas4[:-1]:
    assert py(I) < py(U / 12) - 5, U
assert py(.26) < 250 - 350 * 2 / 12
slopes = [abs((py(meas4[k + 1][1]) - py(meas4[k][1])) / KU) for k in range(5)]
assert all(slopes[k] >= slopes[k + 1] for k in range(4)), slopes   # số đo làm tròn 2 chữ số: cho phép bằng nhau
assert slopes[0] > slopes[4] * 1.5
f.text(268, 190, "R = 12 Ω không đổi", BLUE, 13, "start", "600")
f.text(110, 105, "Đèn sợi đốt", ORG, 14, "start", "700")
f.text(250, 50, "R tăng dần", "currentColor", 13, "start", "400")
f.line(290, 57, 320, 85, w=1, marker="k")
f.check("fig4")
fig4 = f.html("Đồ thị I theo U của đèn sợi đốt: đường cong qua sáu điểm đo, độ dốc giảm dần; đường đứt thẳng ứng với điện trở 12 Ω để so sánh.",
              "Hình 4. Đèn 6 V – 3 W: đường cong; đường đứt là R = 12 Ω không đổi.",
              exp="tn-l11-dien-tro-ohm-02")

# ---------- thay mốc
src = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert src.count(f"<!--FIG{n}-->") == 1, n
    src = src.replace(f"<!--FIG{n}-->", fg)
assert "<!--FIG" not in src
(HERE / "theory.html").write_text(src, encoding="utf8")
print("ok", len(src))
