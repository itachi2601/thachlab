#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài 10 (lesson 29) Thực hành đo tần số của sóng âm, chèn vào theory.src.html -> theory.html.
Chạy lại được (idempotent). Điểm sóng tính từ phương trình; assert toạ độ, hộp nhãn, đếm chu kì ở cuối mỗi hình."""
import math, pathlib, re
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
VB_W = 440
FS = 17      # cỡ chữ nhãn (viewBox 440 -> ~14 px ở 375 px)
FSUB = 13


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' stroke-opacity="{op}"' if op != 1 else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}{o}/>'


def poly(pts, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' stroke-opacity="{op}"' if op != 1 else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{d}{o} points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')


def dot(x, y, r=4, c="currentColor", stroke=""):
    s = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"{s}/>'


def sub(s):
    return re.sub(r"_(\w)", rf'<tspan baseline-shift="sub" font-size="{FSUB}">\1</tspan>', s)


class Fig:
    def __init__(self, name, vb_h):
        self.name, self.h, self.body = name, vb_h, ""
        self.boxes, self.dots = [], []

    def add(self, s):
        self.body += s

    def T(self, x, y, s, c="currentColor", size=FS, anchor="start", weight="600"):
        assert "$" not in s, "không dùng $…$ trong <text>"
        assert size >= FS
        plain = re.sub(r"<[^>]+>", "", s)
        plain = re.sub(r"_(\w)", r"\1", plain)
        w = (0.6 if int(weight) >= 600 else 0.55) * size * len(plain)
        x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anchor]
        self.boxes.append((x0, y - size * 0.8, x0 + w, y + size * 0.2, plain))
        self.body += text(x, y, sub(s), c, size, anchor, weight)

    def D(self, x, y, r):
        self.dots.append((x, y, r))

    def check(self):
        for (a, b, c, d, t) in self.boxes:
            assert a >= 2 and c <= VB_W - 2 and b >= 0 and d <= self.h, f"{self.name}: nhãn '{t}' vượt khung ({a:.0f},{b:.0f},{c:.0f},{d:.0f})"
        for i, p in enumerate(self.boxes):
            for q in self.boxes[i + 1:]:
                assert p[2] <= q[0] or q[2] <= p[0] or p[3] <= q[1] or q[3] <= p[1], f"{self.name}: nhãn '{p[4]}' chồng '{q[4]}'"
        for (a, b, c, d, t) in self.boxes:
            for (x, y, r) in self.dots:
                assert x + r <= a or x - r >= c or y + r <= b or y - r >= d, f"{self.name}: nhãn '{t}' đè chấm ({x:.0f},{y:.0f})"

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


def arc(cx, cy, r, a0, a1, c="currentColor", w=2, op=1, n=24):
    """Cung tròn từ góc a0 tới a1 (độ, đo từ +x, chiều kim đồng hồ trên màn hình vì y hướng xuống)."""
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return poly(pts, c, w, op=op)


# =====================================================================
# Hình 1: cảnh mở bài — ukulele, điện thoại lên dây (không có con số)
# =====================================================================
f1 = Fig("f1", 256)
# ukulele nằm ngang, đầu đàn về bên phải
f1.add('<ellipse cx="62" cy="150" rx="50" ry="44" fill="rgba(251,146,60,.16)" stroke="currentColor" stroke-width="2.2"/>')
f1.add('<ellipse cx="116" cy="150" rx="34" ry="31" fill="rgba(251,146,60,.16)" stroke="currentColor" stroke-width="2.2"/>')
f1.add('<circle cx="86" cy="150" r="14" fill="rgba(0,0,0,.25)" stroke="currentColor" stroke-width="2"/>')
NECK_Y0, NECK_Y1, NECK_X1 = 141, 159, 238
f1.add(f'<rect x="146" y="{NECK_Y0}" width="{NECK_X1 - 146}" height="{NECK_Y1 - NECK_Y0}" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>')
f1.add(f'<rect x="{NECK_X1}" y="{NECK_Y0 - 5}" width="30" height="{NECK_Y1 - NECK_Y0 + 10}" rx="4" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>')
for k in range(4):                                   # 4 dây A, E, C, G (vẽ đều nhau)
    y = NECK_Y0 + 3 + k * 4
    f1.add(line(72, y, NECK_X1 + 10, y, "currentColor", 1.2, op=.8))
for x in (176, 204):                                  # phím đàn
    f1.add(line(x, NECK_Y0, x, NECK_Y1, "currentColor", 1.2, op=.6))
# sóng âm từ lỗ thoát âm đi lên-phải (cung quanh tâm lỗ thoát âm, phía trên cần đàn)
for r in (64, 80, 96):
    f1.add(arc(86, 150, r, -80, -30, BLUE, 2.2, op=.9))
# điện thoại
PX0, PX1, PY0, PY1 = 308, 412, 36, 226
f1.add(f'<rect x="{PX0}" y="{PY0}" width="{PX1 - PX0}" height="{PY1 - PY0}" rx="14" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2.4"/>')
f1.add(f'<rect x="{PX0 + 8}" y="{PY0 + 16}" width="{PX1 - PX0 - 16}" height="{PY1 - PY0 - 54}" rx="4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-opacity=".6"/>')
CX, CY, CR = 360, 138, 40
f1.add(arc(CX, CY, CR, 180, 360, "currentColor", 2))
for a in (180, 225, 270, 315, 360):
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    L2 = 9 if a == 270 else 6
    f1.add(line(CX + (CR - L2) * ca, CY + (CR - L2) * sa, CX + CR * ca, CY + CR * sa, "currentColor", 2))
NEEDLE_DEG = 270 - 14          # kim lệch nhẹ sang trái
f1.add(line(CX, CY, CX + (CR - 8) * math.cos(math.radians(NEEDLE_DEG)), CY + (CR - 8) * math.sin(math.radians(NEEDLE_DEG)), RED, 2.6))
f1.add(dot(CX, CY, 4, "currentColor"))
f1.T(CX, CY + 36, "A", GRN, 26, "middle", "700")
MICX, MICY = 360, 213
f1.add(dot(MICX, MICY, 4.5, ORG)); f1.D(MICX, MICY, 4.5)
f1.T(MICX, 250, "micro", ORG, FS, "middle", "700")
f1.T(PX0 + (PX1 - PX0) / 2, 24, "Điện thoại", "currentColor", FS, "middle", "700")
f1.T(82, 224, "Ukulele", "currentColor", FS, "start", "700")
assert PX0 > NECK_X1 + 30 + 20 and NECK_Y1 - NECK_Y0 == 18
fig1 = fig(f1, "Cây ukulele nằm ngang, sóng âm toả lên phía trên cần đàn; bên phải là điện thoại hiện bộ lên dây với kim chỉ lệch nhẹ về bên trái, micro ở cạnh dưới điện thoại.",
           "Hình 1. Mai đặt điện thoại cạnh đàn để lên dây.")

# =====================================================================
# Hình 2: sơ đồ nối âm thoa - micro - dao động kí
# =====================================================================
f2 = Fig("f2", 252)
# âm thoa (chữ U) + hộp cộng hưởng
f2.add('<path d="M42,34 L42,92 Q42,106 52,106 Q62,106 62,92 L62,34" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/>')
f2.add(line(52, 106, 52, 138, "currentColor", 3))
f2.add('<rect x="22" y="138" width="60" height="46" fill="rgba(251,146,60,.16)" stroke="currentColor" stroke-width="2.2"/>')
f2.T(12, 214, "Âm thoa", "currentColor", FS, "start", "700")
# sóng âm từ âm thoa tới micro (cung quanh nhánh phải)
for r in (26, 44, 62):
    f2.add(arc(62, 64, r, -34, 34, BLUE, 2.2, op=.9))
f2.T(96, 26, "sóng âm", BLUE, FS, "start", "700")
# micro
MX, MY0, MY1 = 190, 50, 92
f2.add(f'<rect x="{MX - 13}" y="{MY0}" width="26" height="{MY1 - MY0}" rx="13" fill="rgba(56,189,248,.16)" stroke="currentColor" stroke-width="2.2"/>')
f2.add(line(MX, MY1, MX, 128, "currentColor", 2.2))
f2.add(line(MX - 16, 128, MX + 16, 128, "currentColor", 2.6))
f2.T(MX - 20, 118, "Micro", "currentColor", FS, "end", "700")
# dao động kí
SX0, SX1, SY0, SY1 = 262, 428, 14, 228
f2.add(f'<rect x="{SX0}" y="{SY0}" width="{SX1 - SX0}" height="{SY1 - SY0}" rx="8" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2.4"/>')
gx0, gy0, gw, gh = SX0 + 12, SY0 + 12, 142, 78
f2.add(f'<rect x="{gx0}" y="{gy0}" width="{gw}" height="{gh}" fill="rgba(0,0,0,.2)" stroke="currentColor" stroke-width="1.4" stroke-opacity=".7"/>')
for i in range(1, 4):
    f2.add(line(gx0 + gw * i / 4, gy0, gx0 + gw * i / 4, gy0 + gh, "currentColor", 1, op=.15))
for j in range(1, 3):
    f2.add(line(gx0, gy0 + gh * j / 3, gx0 + gw, gy0 + gh * j / 3, "currentColor", 1, op=.15))
wave = [(gx0 + 4 + t, gy0 + gh / 2 - 22 * math.sin(2 * math.pi * t / 34)) for t in range(0, gw - 8, 2)]
f2.add(poly(wave, GRN, 2.2))
f2.T(SX0 + (SX1 - SX0) / 2, SY0 + 12 + gh + 26, "Dao động kí", "currentColor", FS, "middle", "700")
# đầu vào CH1 + dây
JX, JY = SX0, 160
f2.add(f'<circle cx="{JX}" cy="{JY}" r="6" fill="currentColor"/>')
f2.add(poly([(MX, 128), (MX, JY), (JX - 6, JY)], "currentColor", 2.2))
f2.T(JX + 12, JY + 6, "CH1", "currentColor", FS, "start", "700")
# hai núm
for k, name in enumerate(("TIME/DIV", "VOLT/DIV")):
    ky = 188 + k * 28
    f2.add(f'<circle cx="{SX0 + 24}" cy="{ky}" r="10" fill="none" stroke="{ORG if k == 0 else BLUE}" stroke-width="2.4"/>')
    f2.add(line(SX0 + 24, ky, SX0 + 24, ky - 8, ORG if k == 0 else BLUE, 2.4))
    f2.T(SX0 + 42, ky + 6, name, ORG if k == 0 else BLUE, FS, "start", "700")
assert JX == SX0 and JY > gy0 + gh
fig2 = fig(f2, "Âm thoa trên hộp cộng hưởng phát sóng âm tới micro; dây tín hiệu từ micro nối vào đầu vào CH1 của dao động kí, bên cạnh có hai núm TIME/DIV và VOLT/DIV.",
           "Hình 2. Sơ đồ nối: nguồn âm đơn, micro, dao động kí.")

# =====================================================================
# Hình 3: màn dao động kí, 4 chu kì liên tiếp chiếm 9,1 ô (1 ms/ô)
# =====================================================================
CELL = 34
GX0, GY0 = 40, 62
NX, NY = 10, 8
f3 = Fig("f3", 424)
f3.add(f'<rect x="{GX0}" y="{GY0}" width="{NX * CELL}" height="{NY * CELL}" fill="rgba(0,0,0,.2)" stroke="currentColor" stroke-width="2"/>')
for i in range(1, NX):
    f3.add(line(GX0 + i * CELL, GY0, GX0 + i * CELL, GY0 + NY * CELL, "currentColor", 1, op=.18))
for j in range(1, NY):
    f3.add(line(GX0, GY0 + j * CELL, GX0 + NX * CELL, GY0 + j * CELL, "currentColor", 1, op=.18))
YC = GY0 + 4 * CELL
f3.add(line(GX0, YC, GX0 + NX * CELL, YC, "currentColor", 1.4, op=.5))
K_MS, F_HZ, N_CH = 1.0, 440.0, 4
T_CELLS = (1000.0 / F_HZ) / K_MS            # 2,2727 ô / chu kì
XS_CELLS = 0.5                              # điểm bắt đầu cách mép trái 0,5 ô
AMP = 2 * CELL
pts = []
x = GX0 + XS_CELLS * CELL
xe = x + N_CH * T_CELLS * CELL
for i in range(0, int((xe + 24 - x) / 2) + 1):
    px = x + i * 2
    if px > GX0 + NX * CELL - 1:
        break
    pts.append((px, YC - AMP * math.sin(2 * math.pi * (px - x) / (T_CELLS * CELL))))
f3.add(poly(pts, GRN, 2.6))
cross = [x + j * T_CELLS * CELL for j in range(N_CH + 1)]
for cx_ in cross:
    f3.add(dot(cx_, YC, 5, ORG, "currentColor")); f3.D(cx_, YC, 5)
for _n in (0, 5, 10):
    f3.add(line(GX0 + _n * CELL, GY0 - 7, GX0 + _n * CELL, GY0, 'currentColor', 2))
    f3.T(GX0 + _n * CELL, GY0 - 12, str(_n), 'currentColor', FS, 'middle', '600')
BY = GY0 + NY * CELL + 18
f3.add(line(cross[0], BY, cross[-1], BY, BLUE, 2.2))
for cx_ in cross:
    f3.add(line(cx_, BY - 8, cx_, BY + 8, BLUE, 2.2))
for j in range(N_CH):
    f3.T((cross[j] + cross[j + 1]) / 2, BY + 30, str(j + 1), BLUE, FS, "middle", "700")
f3.T(GX0, 24, "TIME/DIV: 1 ms/ô", "currentColor", FS, "start", "700")
f3.T(GX0 + NX * CELL, 24, "CH1", "currentColor", FS, "end", "700")
f3.T(GX0 + NX * CELL / 2, BY + 62, "4 chu kì chiếm khoảng 9,1 ô", BLUE, FS, "middle", "700")
# assert: lưới, chiều dài, dấu qua 0 đi lên
assert abs(T_CELLS - 2.2727) < 1e-3 and abs((cross[-1] - cross[0]) / CELL - 9.0909) < 1e-3
assert cross[-1] < GX0 + NX * CELL - 4 and all(abs(pts[0][1] - YC) < 1e-9 for _ in [0])
j0 = next(i for i, p in enumerate(pts) if p[0] >= cross[1] - 1)
assert pts[1][1] < YC                                       # sau điểm đầu sóng đi LÊN (y giảm)
assert abs(F_HZ - N_CH / (((cross[-1] - cross[0]) / CELL) * K_MS * 1e-3)) < 0.1     # f = N/(L·k) ≈ 440
fig3 = fig(f3, "Màn dao động kí 10 ô ngang, 8 ô dọc: sóng hình sin xanh lục, năm chấm cam ở các điểm qua trục ngang đi lên; dấu ngoặc dưới màn chia thành bốn chu kì, chiếm khoảng chín ô.",
           "Hình 3. Màn dao động kí: đếm chu kì giữa các chấm, không đếm chấm.")

# =====================================================================
# Hình 4: hai âm 440 Hz và 880 Hz trên cùng thang thời gian
# =====================================================================
f4 = Fig("f4", 270)
X0_, X1_, TMAX = 60, 400, 9.0          # ms
PXMS = (X1_ - X0_) / TMAX
def tx(t): return X0_ + PXMS * t
Y1C, Y2C, AM4 = 74, 168, 30
AXY = 212
for yc, fq, col in ((Y1C, 440.0, BLUE), (Y2C, 880.0, RED)):
    f4.add(line(X0_, yc, X1_, yc, "currentColor", 1, op=.3))
    P = []
    t = 0.0
    while t <= TMAX + 1e-9:
        P.append((tx(t), yc - AM4 * math.sin(2 * math.pi * fq * t * 1e-3)))
        t += 0.04
    f4.add(poly(P, col, 2.4))
    # kiểm: số lần qua 0 đi lên trong cửa sổ = f·9 ms
    ups = sum(1 for a, b in zip(P, P[1:]) if (a[1] - yc) > 1e-6 >= (b[1] - yc) - 1e-6 and b[1] < a[1] and (a[1] - yc) * (b[1] - yc) <= 0)
    assert abs(ups - fq * TMAX * 1e-3) <= 1.01, (fq, ups)
f4.T(X0_, 30, "440 Hz", BLUE, FS, "start", "700")
f4.T(X0_, 124, "880 Hz (cao hơn)", RED, FS, "start", "700")
f4.add(line(X0_, AXY, X1_ + 10, AXY, "currentColor", 1.8))
for t in (0, 2, 4, 6, 8):
    f4.add(line(tx(t), AXY, tx(t), AXY + 6, "currentColor", 1.6))
    f4.T(tx(t), AXY + 28, str(t), "currentColor", FS, "middle", "600")
f4.T((X0_ + X1_) / 2, 264, "t (ms)", "currentColor", FS, "middle", "700")
# kiểm tuyến tính trục thời gian và tỉ lệ 1 : 2 số chu kì
steps = [round(tx(b) - tx(a), 6) for a, b in zip((0, 2, 4, 6), (2, 4, 6, 8))]
assert max(steps) - min(steps) < 1e-6
assert abs(880 * TMAX * 1e-3 - 2 * 440 * TMAX * 1e-3) < 1e-9
fig4 = fig(f4, "Hai đồ thị sin cùng biên độ trên một trục thời gian từ 0 đến 9 mili giây: đồ thị xanh 440 Hz gần bốn chu kì, đồ thị đỏ 880 Hz gần tám chu kì.",
           "Hình 4. Cùng thang thời gian: âm 880 Hz có số chu kì gấp đôi âm 440 Hz.",
           exp="tn-l11-dotansoam-03")

# ---------- ghi theory.html
src = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, n
    src = src.replace(f"<!--FIG{n}-->", f)
assert "<!--FIG" not in src
(HERE / "theory.html").write_text(src, encoding="utf8")
print("ok", len(src), "· 4 hình")
