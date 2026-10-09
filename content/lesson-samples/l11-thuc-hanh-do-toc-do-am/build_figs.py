#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài 15 (lesson 34) Thực hành đo tốc độ truyền âm và thay <!--FIGn--> trong
theory.src.html -> theory.html. Chạy lại được (idempotent). Kiểm toạ độ: nhãn trong khung, không chồng,
không bị nét cắt xuyên; nút/bụng đúng vị trí theo phương trình; trục đồ thị chia tuyến tính; đỉnh đúng l1, l2."""
import math
import pathlib
import re
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
VB_W = 420
YEL = "#fbbf24"
WATER = BLUE


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' stroke-opacity="{op}"' if op != 1 else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}{o}/>'


def poly(pts, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' stroke-opacity="{op}"' if op != 1 else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{d}{o} points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')


def rect(x, y, w, h, c="currentColor", sw=2.2, fill="none", fop=1, rx=0):
    f = f' fill-opacity="{fop}"' if fill != "none" else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{f} stroke="{c}" stroke-width="{sw}"/>'


def fill_rect(x, y, w, h, c, op=.35):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" fill-opacity="{op}" stroke="none"/>'


def dot(x, y, r=4, c="currentColor", hollow=False):
    if hollow:
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{c}" stroke-width="2"/>'
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'


def sub(s):
    return re.sub(r"_(\w)", r'<tspan baseline-shift="sub" font-size="13">\1</tspan>', s)


class Fig:
    def __init__(self, name, vb_h):
        self.name, self.h, self.body = name, vb_h, ""
        self.boxes = []

    def add(self, s):
        self.body += s

    def T(self, x, y, s, c="currentColor", size=17, anchor="start", weight="600"):
        assert "$" not in s, "không dùng $…$ trong <text>"
        assert size >= 17, "chữ SVG phải >= 17"
        plain = re.sub(r"<[^>]+>", "", s)
        plain = re.sub(r"_(\w)", r"\1", plain)
        w = (0.6 if int(weight) >= 600 else 0.55) * size * len(plain)
        x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anchor]
        self.boxes.append((x0, y - size * 0.8, x0 + w, y + size * 0.2, plain))
        self.body += text(x, y, sub(s), c, size, anchor, weight)

    def check(self):
        for (a, b, c, d, t) in self.boxes:
            assert a >= 2 and c <= VB_W - 2 and b >= 0 and d <= self.h, f"{self.name}: nhãn '{t}' vượt khung ({a:.0f},{b:.0f},{c:.0f},{d:.0f})"
        for i, p in enumerate(self.boxes):
            for q in self.boxes[i + 1:]:
                assert p[2] <= q[0] or q[2] <= p[0] or p[3] <= q[1] or q[3] <= p[1], f"{self.name}: nhãn '{p[4]}' chồng '{q[4]}'"

    def check_segments(self):
        segs = []
        for m in re.finditer(r"<line ([^>]*)/>", self.body):
            a = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(1)))
            if float(a.get("stroke-opacity", 1)) <= 0.2:
                continue
            segs.append((float(a["x1"]), float(a["y1"]), float(a["x2"]), float(a["y2"])))
        for m in re.finditer(r"<polyline ([^>]*)/>", self.body):
            pts = [tuple(map(float, q.split(","))) for q in re.search(r'points="([^"]*)"', m.group(1)).group(1).split()]
            segs += [(a[0], a[1], b[0], b[1]) for a, b in zip(pts, pts[1:])]
        for (a, b, c, d, t) in self.boxes:
            for (x1, y1, x2, y2) in segs:
                n = max(2, int(max(abs(x2 - x1), abs(y2 - y1)) * 2))
                for k in range(n + 1):
                    x, y = x1 + (x2 - x1) * k / n, y1 + (y2 - y1) * k / n
                    assert not (a + 1 < x < c - 1 and b + 1 < y < d - 1), f"{self.name}: nhãn '{t}' bị nét ({x1:.0f},{y1:.0f})-({x2:.0f},{y2:.0f}) cắt xuyên"

    def close(self):
        self.check()
        self.check_segments()
        return f"0 0 {VB_W} {self.h}", self.body


def fig(f, label, cap, exp=None):
    vb, body = f.close()
    s = wrap(vb, label, body, cap)
    if exp:
        s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
    return s


def dim_v(x, y1, y2, c="currentColor"):
    """Mũi tên hai đầu thẳng đứng (chữ V 30°) từ y1 xuống y2."""
    return line(x, y1, x, y2, c, 1.8) + chevron(x, y1, 0, -1, c, 1.8, 11) + chevron(x, y2, 0, 1, c, 1.8, 11)


# =====================================================================
# Hình 1: ba chai, lượng nước khác nhau, thổi ngang miệng (chỉ vẽ cảnh)
# =====================================================================
f1 = Fig("f1", 208)
SURF = {"A": 112, "B": 134, "C": 154}
BOT = 172
for name, bx in (("A", 70), ("B", 210), ("C", 350)):
    ys = SURF[name]
    f1.add(fill_rect(bx - 27, ys, 54, BOT - ys - 1, WATER, .4))
    f1.add(line(bx - 27, ys, bx + 27, ys, WATER, 2))
    f1.add(f'<path d="M{bx-11},40 L{bx-11},78 L{bx-28},98 L{bx-28},{BOT-6} Q{bx-28},{BOT} {bx-22},{BOT} L{bx+22},{BOT} '
           f'Q{bx+28},{BOT} {bx+28},{BOT-6} L{bx+28},98 L{bx+11},78 L{bx+11},40" fill="none" stroke="currentColor" stroke-width="2.4" '
           f'stroke-linejoin="round"/>')
    f1.add(line(bx - 46, 28, bx + 12, 28, ORG, 2.4) + chevron(bx + 12, 28, 1, 0, ORG, 2.4, 11))
    f1.T(bx, 200, name, "currentColor", 22, "middle", "700")
assert SURF["A"] < SURF["B"] < SURF["C"] < BOT                     # A nhiều nước nhất, C ít nhất
air = [SURF[k] - 40 for k in "ABC"]
assert air[0] < air[1] < air[2]                                      # cột khí A ngắn nhất
fig1 = fig(f1, "Ba chai giống nhau: chai A nhiều nước nhất, chai B vừa, chai C ít nhất; mũi tên cam là hơi thổi ngang miệng từng chai.",
           "Hình 1. Ba chai giống nhau, lượng nước khác nhau.<br>Mũi tên cam: thổi ngang miệng chai.",
           exp="tn-l11-dotocdoam-02")

# =====================================================================
# Hình 2: ống cộng hưởng, hai lần cộng hưởng đầu tiên
# =====================================================================
f2 = Fig("f2", 372)
Y0, QUART, E = 60, 90, 10                    # miệng ống, λ/4, e (vẽ phóng to)
HW, AMP = 20, 16                             # nửa bề rộng ống, biên độ vẽ
L1PX, L2PX = QUART - E, 3 * QUART - E        # l1 = λ/4 - e ; l2 = 3λ/4 - e
assert (L2PX - L1PX) == 2 * QUART            # l2 - l1 = λ/2
BOTT = 354


def tube(cx, ywater, env):
    s = fill_rect(cx - HW + 1, ywater, 2 * HW - 2, BOTT - ywater, WATER, .4)
    s += line(cx - HW, ywater, cx + HW, ywater, WATER, 2.2)
    s += line(cx - HW, Y0, cx - HW, BOTT, "currentColor", 2.6) + line(cx + HW, Y0, cx + HW, BOTT, "currentColor", 2.6)
    s += line(cx - HW, BOTT, cx + HW, BOTT, "currentColor", 2.6)
    ys = [Y0 - E + i * 1.0 for i in range(0, int(ywater - (Y0 - E)) + 1)]
    for sgn in (-1, 1):
        solid = [(cx + sgn * env(y), y) for y in ys if y >= Y0]
        dashed = [(cx + sgn * env(y), y) for y in ys if y <= Y0]
        s += poly(solid, ORG, 2.4) + poly(dashed, ORG, 2.4, "3 3")
    s += line(cx - HW, Y0 - E, cx + HW, Y0 - E, ORG, 1.6, "3 3")
    return s


# ống 1: bụng ở y = Y0 - E, nút ở mặt nước y = Y0 + L1PX
C1, C2 = 100, 300
W1 = Y0 + L1PX
env1 = lambda y: AMP * abs(math.cos(math.pi / 2 * (y - (Y0 - E)) / QUART))
W2 = Y0 + L2PX
env2 = lambda y: AMP * abs(math.sin(math.pi * (W2 - y) / (2 * QUART)))
assert env1(Y0 - E) > AMP - 1e-9 and env1(W1) < 1e-6                  # bụng trên, nút ở mặt nước
assert env2(W2) < 1e-6 and env2(W2 - 2 * QUART) < 1e-6 and env2(W2 - QUART) > AMP - 1e-9 and env2(Y0 - E) > AMP - 1e-9
f2.add(tube(C1, W1, env1) + tube(C2, W2, env2))
# nút (chấm đặc) và bụng (vòng rỗng)
for cx, nodes, anti in ((C1, [W1], [Y0 - E]), (C2, [W2, W2 - 2 * QUART], [Y0 - E, W2 - QUART])):
    for y in nodes:
        f2.add(dot(cx, y, 4.5))
        f2.T(cx + HW + 10, y + 6, "nút")
    for y in anti:
        f2.add(dot(cx, y, 4.5, "currentColor", True))
        f2.T(cx + HW + 10, y + 6, "bụng")
# kích thước l1, l2
f2.add(dim_v(58, Y0, W1) + line(58, Y0, C1 - HW, Y0, "currentColor", 1.2, "", .5) + line(58, W1, C1 - HW, W1, "currentColor", 1.2, "", .5))
f2.T(50, (Y0 + W1) / 2 + 6, "l_1", "currentColor", 18, "end", "700")
f2.add(dim_v(250, Y0, W2) + line(250, Y0, C2 - HW, Y0, "currentColor", 1.2, "", .5) + line(250, W2, C2 - HW, W2, "currentColor", 1.2, "", .5))
f2.T(242, (Y0 + W2) / 2 + 6, "l_2", "currentColor", 18, "end", "700")
fig2 = fig(f2, "Hai ống cộng hưởng: ống trái có cột khí l1 bằng một phần tư bước sóng trừ e, với bụng ở miệng ống và nút ở mặt nước; ống phải có cột khí l2 bằng ba phần tư bước sóng trừ e, thêm một nút và một bụng ở giữa.",
           "Hình 2. Sóng dừng trong cột khí ở hai lần cộng hưởng đầu tiên.<br>Đường cam: biên độ dao động của không khí.<br>Nét đứt trên miệng ống: bụng nằm cao hơn miệng một đoạn <em>e</em> (vẽ phóng to).")

# =====================================================================
# Hình 3: bộ dụng cụ, bình thông nhau
# =====================================================================
f3 = Fig("f3", 352)
TOP, TB, CX, TH = 140, 290, 250, 16
WS = 226                                    # mặt nước (ống và bình cùng độ cao)
f3.add(rect(14, 40, 120, 64, "currentColor", 2.2, "none", 1, 4))
f3.T(74, 66, "Máy phát", "currentColor", 17, "middle", "600")
f3.T(74, 90, "tần số", "currentColor", 17, "middle", "600")
f3.add(poly([(134, 72), (180, 72), (180, 108), (230, 108)], "currentColor", 2))
f3.add(rect(230, 96, 40, 24, "currentColor", 2.2))
f3.add(f'<polygon points="230,120 270,120 284,134 216,134" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>')
f3.T(292, 114, "loa")
f3.add(fill_rect(CX - TH + 1, WS, 2 * TH - 2, TB - WS, WATER, .4) + line(CX - TH, WS, CX + TH, WS, WATER, 2.2))
f3.add(line(CX - TH, TOP, CX - TH, TB, "currentColor", 2.6) + line(CX + TH, TOP, CX + TH, TB, "currentColor", 2.6))
f3.T(226, 170, "ống trong suốt", "currentColor", 17, "end", "600")
# thước: số 0 ở miệng ống
RX = 272
f3.add(rect(RX, TOP, 12, TB - TOP, "currentColor", 1.8))
for i in range(0, TB - TOP + 1, 10):
    L = 8 if i % 50 == 0 else 5
    f3.add(line(RX, TOP + i, RX + L, TOP + i, "currentColor", 1.2))
f3.T(294, 164, "thước mm")
f3.T(294, 186, "số 0 ở miệng")
# bình nước
f3.add(rect(36, 204, 70, 108, "currentColor", 2.4) + fill_rect(38, WS, 66, 312 - WS - 1, WATER, .4) + line(38, WS, 104, WS, WATER, 2.2))
f3.add(line(106, WS, CX - TH, WS, "currentColor", 1.6, "6 4", .7))
f3.T(170, 216, "cùng mực", "currentColor", 17, "middle", "600")
f3.add(f'<path d="M{CX},{TB} C{CX},335 71,335 71,312" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>')
f3.T(160, 306, "ống mềm", "currentColor", 17, "middle", "600")
f3.add(dim_v(71, 152, 198))
f3.T(71, 140, "nâng, hạ", "currentColor", 17, "middle", "600")
f3.T(71, 346, "bình nước", "currentColor", 17, "middle", "600")
assert WS > TOP and WS < TB and 204 < WS < 312
fig3 = fig(f3, "Sơ đồ bộ dụng cụ: máy phát tần số nối loa đặt sát miệng ống thuỷ tinh có thước; đáy ống nối ống mềm với bình nước; mặt nước ở ống và ở bình cùng độ cao.",
           "Hình 3. Bộ ống cộng hưởng.<br>Mặt nước ở ống và ở bình luôn cùng độ cao.<br>Nâng hay hạ bình để đổi mực nước trong ống.")

# =====================================================================
# Hình 4: độ to theo chiều dài cột khí, hai đỉnh
# =====================================================================
f4 = Fig("f4", 274)
X0, SC, YB = 40, 5.0, 220                    # l = 0 -> x = 40 ; 5 px/cm ; trục ngang y = 220
xs = lambda l: X0 + SC * l
L1, L2 = 16.72, 50.88
assert abs(xs(70) - 390) < 1e-9 and abs(xs(L2) - xs(L1) - SC * (L2 - L1)) < 1e-9          # trục tuyến tính
A = lambda l: .06 + 1.0 / (1 + ((l - L1) / 2.2) ** 2) + .85 / (1 + ((l - L2) / 2.2) ** 2)
H = 105
pts = [(xs(l / 2), YB - H * A(l / 2)) for l in range(0, 141)]
top = min(range(len(pts)), key=lambda i: pts[i][1] if xs(L1) - 20 < pts[i][0] < xs(L1) + 20 else 1e9)
assert abs(pts[top][0] - xs(L1)) <= SC * .26                                                # đỉnh 1 đúng l1
seg2 = [p for p in pts if xs(L2) - 20 < p[0] < xs(L2) + 20]
assert abs(min(seg2, key=lambda p: p[1])[0] - xs(L2)) <= SC * .26                           # đỉnh 2 đúng l2
f4.add(line(X0, YB, 400, YB, "currentColor", 2) + chevron(400, YB, 1, 0, "currentColor", 2, 11))
f4.add(line(X0, YB, X0, 40, "currentColor", 2) + chevron(X0, 40, 0, -1, "currentColor", 2, 11))
for l in range(0, 71, 10):
    f4.add(line(xs(l), YB, xs(l), YB + 6, "currentColor", 1.6))
    f4.T(xs(l), 246, str(l), "currentColor", 17, "middle", "600")
f4.T(46, 36, "độ to", "currentColor", 17, "start", "600")
f4.T(215, 268, "chiều dài cột khí l (cm)", "currentColor", 17, "middle", "600")
f4.add(poly(pts, BLUE, 2.6))
for l in (L1, L2):
    f4.add(line(xs(l), 62, xs(l), YB, "currentColor", 1.5, "5 4", .7))
f4.add(line(xs(L1), 62, xs(L2), 62, "currentColor", 1.8) + chevron(xs(L1), 62, -1, 0, "currentColor", 1.8, 11) + chevron(xs(L2), 62, 1, 0, "currentColor", 1.8, 11))
f4.T((xs(L1) + xs(L2)) / 2, 52, "λ/2 ≈ 34,2 cm", "currentColor", 17, "middle", "700")
f4.T(xs(L1) + 9, 96, "l_1", "currentColor", 18, "start", "700")
f4.T(xs(L2) + 9, 112, "l_2", "currentColor", 18, "start", "700")
fig4 = fig(f4, "Đồ thị độ to nghe được theo chiều dài cột khí từ 0 đến 70 cm: hai đỉnh nhọn ở l1 khoảng 16,7 cm và l2 khoảng 50,9 cm, khoảng cách giữa hai đỉnh bằng nửa bước sóng.",
           "Hình 4. Độ to nghe được theo chiều dài cột khí (số minh hoạ).<br>Hai đỉnh là hai lần cộng hưởng.")

# ---------- ghi theory.html
src = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, n
    src = src.replace(f"<!--FIG{n}-->", f)
assert "<!--FIG" not in src
(HERE / "theory.html").write_text(src, encoding="utf8")
print("ok", len(src), "· 4 hình")
