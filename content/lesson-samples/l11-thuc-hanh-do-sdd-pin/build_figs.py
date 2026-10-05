#!/usr/bin/env python3
"""Sinh 4 hình SVG cho bài 26 (lesson 45) Thực hành đo suất điện động và điện trở trong của pin
và thay <!--FIGn--> trong theory.src.html -> theory.html. Chạy lại được (idempotent).
Điểm đồ thị tính từ số đo + hàm lưới tuyến tính; assert toạ độ, bề rộng nhãn, chiều mạch ở cuối mỗi hình."""
import pathlib, re
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
YEL = "#fbbf24"
VB_W = 440


# ---------- tiện ích vẽ
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, marker=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    o = f' stroke-opacity="{op}"' if op != 1 else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
            f'stroke-width="{w}"{d}{o}{m}/>')


def poly(pts, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' stroke-opacity="{op}"' if op != 1 else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" '
            f'stroke-linecap="round"{d}{o} points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')


def dot(x, y, r=4, c="currentColor", stroke=""):
    s = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"{s}/>'


def ring(x, y, r, c, label, size=13):
    """Đồng hồ / động cơ: vòng tròn viền màu c, chữ ở tâm."""
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c}" stroke-width="2.2"/>'
            f'<text x="{x}" y="{y + size * 0.36:.1f}" fill="currentColor" font-size="{size}" font-weight="700" '
            f'text-anchor="middle">{label}</text>')


def sub(s):  # R_0 -> R<tspan baseline-shift="sub">0</tspan>
    return re.sub(r"_(\w)", r'<tspan baseline-shift="sub" font-size="11">\1</tspan>', s)


class Fig:
    """Gom thân SVG + hộp bao nhãn/chấm để kiểm toạ độ: nhãn trong khung, không chồng nhau."""

    def __init__(self, name, vb_h):
        self.name, self.h, self.body = name, vb_h, defs(name)
        self.boxes, self.dots = [], []

    def add(self, s):
        self.body += s

    def T(self, x, y, s, c="currentColor", size=13, anchor="start", weight="600"):
        assert "$" not in s, "không dùng $…$ trong <text>"
        plain = re.sub(r"<[^>]+>", "", s)
        plain = re.sub(r"_(\w)", r"\1", plain)  # chỉ số dưới hẹp hơn nhưng cứ tính đủ ký tự
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
        """Nhãn không bị nét thẳng (trừ lưới mờ) cắt xuyên: lấy mẫu dọc từng đoạn, hộp nhãn thu 1 px."""
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


def zig_v(x, y1, y2, c, n=5, a=6):
    """Điện trở răng cưa dọc: n nhịp, biên độ a."""
    pts, step = [(x, y1)], (y2 - y1) / (2 * n)
    for i in range(1, 2 * n):
        pts.append((x + (a if i % 2 else -a), y1 + i * step))
    pts.append((x, y2))
    return poly(pts, c, 2)


def zig_h(y, x1, x2, c, n=5, a=6):
    pts, step = [(x1, y)], (x2 - x1) / (2 * n)
    for i in range(1, 2 * n):
        pts.append((x1 + i * step, y + (a if i % 2 else -a)))
    pts.append((x2, y))
    return poly(pts, c, 2)


# =====================================================================
# Hình 1: cùng một viên pin, hai số đo (hở mạch / có tải)
# =====================================================================
f1 = Fig("f1", 190)
f1.add('<defs><marker id="f1-i" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
       f'<path d="M0,0 L10,5 L0,10 z" fill="{ORG}"/></marker></defs>')
BAT_W, BAT_H, BAT_Y = 70, 26, 80
TY = BAT_Y + BAT_H / 2          # 93: cao độ hai cực
VR = 16
PANEL = {}


def panel(f, bx, mx, loaded):
    """Vẽ một khung: pin tại (bx, BAT_Y), vôn kế tâm (mx, TY). Trả toạ độ cực + nút nối để assert."""
    plus, minus = (bx + BAT_W + 6, TY), (bx, TY)
    f.add(f'<rect x="{bx}" y="{BAT_Y}" width="{BAT_W}" height="{BAT_H}" rx="3" fill="rgba(148,163,184,.22)" stroke="currentColor" stroke-width="2"/>')
    f.add(f'<rect x="{bx + BAT_W}" y="{TY - 6}" width="6" height="12" fill="currentColor"/>')
    f.T(bx + 12, TY + 5, "−", BLUE, 15, "middle", "700")
    f.T(bx + BAT_W - 14, TY + 5, "+", RED, 15, "middle", "700")
    # dây vôn kế: cực + tới mép trái vôn kế; cực − vòng lên trên rồi xuống đỉnh vôn kế
    if loaded:
        node_p = (plus[0] + 7, TY)
        node_m = (bx - 8, TY)
    else:
        node_p, node_m = plus, minus
    f.add(poly([plus, (mx - VR, TY)]))
    f.add(poly([minus, node_m, (node_m[0], 60), (mx, 60), (mx, TY - VR)]))
    f.add(ring(mx, TY, VR, BLUE, "V"))
    return plus, minus, node_p, node_m


# khung trái: hở mạch
f1.T(110, 30, "Chưa lắp vào xe", "currentColor", 13, "middle")
pl, mi, _, _ = panel(f1, 40, 165, loaded=False)
f1.add(f'<rect x="137" y="118" width="56" height="20" rx="3" fill="rgba(56,189,248,.14)" stroke="{BLUE}" stroke-width="1.5"/>')
f1.T(165, 133, "1,50 V", BLUE, 13, "middle", "700")
f1.T(110, 165, "I = 0", "currentColor", 13, "middle", "400")
# khung phải: có tải
f1.T(330, 30, "Động cơ đang quay", "currentColor", 13, "middle")
pr, mr, node_p, node_m = panel(f1, 260, 385, loaded=True)
MX, MY, MR = 315, 150, 13
f1.add(dot(node_p[0], node_p[1], 3) + dot(node_m[0], node_m[1], 3))
f1.add(poly([node_p, (node_p[0], MY), (MX + MR, MY)]))
f1.add(poly([node_m, (node_m[0], MY), (MX - MR, MY)]))
f1.add(ring(MX, MY, MR, "currentColor", "M", 13))
f1.add(line(node_p[0], 106, node_p[0], 132, ORG, 2.2, marker="f1-i"))
f1.T(node_p[0] - 17, 124, "I ≈ 0,5 A", ORG, 12, "end", "600")
f1.add(f'<rect x="357" y="118" width="56" height="20" rx="3" fill="rgba(248,113,113,.14)" stroke="{RED}" stroke-width="1.5"/>')
f1.T(385, 133, "1,06 V", RED, 13, "middle", "700")
# assert: vôn kế song song hai cực pin (đầu dây trùng cực), dòng cam chỉ ở khung phải, số đúng
assert pl == (116, TY) and mi == (40, TY) and pr == (336, TY) and mr == (260, TY)
assert node_p[0] > pr[0] and node_m[0] < mr[0]                 # nhánh động cơ rẽ ra từ chính hai cực
assert f1.body.count('marker-end="url(#f1-i)"') == 1 and "f1-i" in f1.body
assert "1,50 V" in f1.body and "1,06 V" in f1.body
fig1 = fig(f1, "Hai khung: pin với vôn kế hở mạch đọc 1,50 V; pin nối động cơ đang quay, vôn kế đọc 1,06 V.",
           "Hình 1. Một viên pin: hở mạch 1,50 V, động cơ quay còn 1,06 V.",
           exp="tn-l11-do-sdd-pin-03")

# =====================================================================
# Hình 2: sơ đồ mạch đo ℰ và r
# =====================================================================
f2 = Fig("f2", 230)
f2.add(f'<defs><marker id="f2-i" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ORG}"/></marker>'
       '<marker id="f2-c" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>')
L, R_, TOPY, BOTY = 70, 380, 50, 180
PLUS_Y, MINUS_Y = 108, 122
M_PT, N_PT = (70, 85), (70, 145)
AX, AY, AR = 230, 50, 14
VX, VY, VRR = 150, 115, 14
# khung mạch (ngắt ở K, A, R0, Rx, pin)
f2.add(poly([(L, PLUS_Y), (L, TOPY), (120, TOPY)]))                      # từ cực + lên đỉnh, tới khoá K
f2.add(poly([(160, TOPY), (AX - AR, TOPY)]))
f2.add(poly([(AX + AR, TOPY), (R_, TOPY), (R_, 80)]))
f2.add(poly([(R_, 120), (R_, BOTY), (280, BOTY)]))
f2.add(poly([(200, BOTY), (L, BOTY), (L, MINUS_Y)]))
# pin: vạch dài (+) trên, vạch ngắn dày (−) dưới
f2.add(line(L - 12, PLUS_Y, L + 12, PLUS_Y, "currentColor", 2.5))
f2.add(line(L - 6, MINUS_Y, L + 6, MINUS_Y, "currentColor", 5))
f2.T(14, 118, "ℰ, r", "currentColor", 14, "start", "700")
f2.add(dot(*M_PT, 3) + dot(*N_PT, 3))
f2.T(50, 82, "M", "currentColor", 13, "start", "700")
f2.T(50, 152, "N", "currentColor", 13, "start", "700")
f2.T(90, PLUS_Y + 4, "+", RED, 13, "middle", "700")
f2.T(90, MINUS_Y + 7, "−", BLUE, 13, "middle", "700")
# khoá K (ĐÓNG: thanh gạt nối hai chấm, dòng điện đang chạy)
f2.add(dot(120, TOPY, 3.5) + dot(160, TOPY, 3.5) + line(120, TOPY, 160, TOPY, "currentColor", 2.4))
f2.T(140, 34, "K", "currentColor", 13, "middle", "700")
# ampe kế nối tiếp
f2.add(ring(AX, AY, AR, ORG, "A"))
# mũi tên dòng điện (chiều +x: từ cực + ra ngoài qua K, A, R0 về cực −)
f2.add(line(290, TOPY, 330, TOPY, ORG, 2.4, marker="f2-i"))
f2.T(310, 40, "I", ORG, 13, "middle", "700")
# điện trở bảo vệ R0
f2.add(zig_v(R_, 80, 120, BLUE))
f2.T(R_ - 12, 104, "R_0 = 2 Ω", BLUE, 13, "end", "700")
# biến trở Rx
f2.add(zig_h(BOTY, 200, 280, BLUE))
f2.add(line(205, 200, 275, 162, "currentColor", 1.8, marker="f2-c"))
f2.T(240, 220, "R_x (0–100 Ω)", BLUE, 13, "middle", "700")
# vôn kế song song hai cực pin M, N
f2.add(poly([M_PT, (VX, M_PT[1]), (VX, VY - VRR)]))
f2.add(poly([(VX, VY + VRR), (VX, N_PT[1]), N_PT]))
f2.add(ring(VX, VY, VRR, GRN, "V"))
f2.T(170, 120, "U", GRN, 13, "start", "700")
# assert hình học
assert (M_PT[0], M_PT[1]) == (L, 85) and N_PT == (L, 145)
assert M_PT[1] < PLUS_Y and N_PT[1] > MINUS_Y                    # M trên cực +, N dưới cực −: vôn kế mắc hai cực pin
assert AY == TOPY and BOTY - TOPY > 0                            # ampe kế nằm trên nhánh chính, nối tiếp
assert f2.body.count('marker-end="url(#f2-i)"') == 1 and 290 < 330  # mũi tên I chiều +x
assert f'x1="120.0" y1="{TOPY:.1f}" x2="160.0" y2="{TOPY:.1f}"' in f2.body   # K đóng: thanh gạt nằm ngang nối hai chấm (không còn gạch chéo)
assert PLUS_Y < MINUS_Y and (L - 12) < (L - 6)                   # vạch dài ở trên (cực +)
fig2 = fig(f2, "Sơ đồ mạch kín: pin, khoá K, ampe kế, điện trở bảo vệ R0 và biến trở Rx nối tiếp; vôn kế mắc song song hai cực pin.",
           "Hình 2. Sơ đồ mạch đo: vôn kế song song hai cực pin M, N.")

# =====================================================================
# Đồ thị (hình 3, 4): lưới tuyến tính x = X0 + kx·I, y = Y0 − ky·(U − 1,0)
# =====================================================================
X0, Y0, XEND, UMIN, UMAX = 60, 250, 410, 1.0, 1.7
KY = (250 - 30) / (UMAX - UMIN)          # 314.2857 px/V

OLD = dict(I=[0.014, 0.066, 0.117, 0.191, 0.311, 0.534], U=[1.48, 1.44, 1.40, 1.35, 1.25, 1.06], a=1.496, b=-0.806)
NEW = dict(I=[0.015, 0.073, 0.129, 0.217, 0.372, 0.701], U=[1.58, 1.56, 1.55, 1.53, 1.49, 1.40], a=1.583, b=-0.259)


def vc(u):                                # vi tri pixel theo U
    return Y0 - KY * (u - UMIN)


def axes(f, imax, ticks):
    kx = (XEND - X0) / imax
    xs = lambda i: X0 + kx * i
    # lưới + vạch chia
    for i in ticks:
        x = xs(i)
        f.add(line(x, 30, x, 250, "currentColor", 1, op=.15))
        f.add(line(x, 250, x, 255, "currentColor", 1.2))
        f.T(x, 268, f"{i:g}".replace(".", ","), "currentColor", 13, "middle", "400")
    for k in range(8):
        u = 1.0 + k * 0.1
        y = vc(u)
        f.add(line(60, y, 410, y, "currentColor", 1, op=.15))
        f.add(line(55, y, 60, y, "currentColor", 1.2))
        f.T(52, y + 5, f"{u:.1f}".replace(".", ","), "currentColor", 13, "end", "400")
    f.add(line(60, 250, 420, 250, "currentColor", 1.8, marker=f"{f.name}-c"))
    f.add(line(60, 250, 60, 18, "currentColor", 1.8, marker=f"{f.name}-c"))
    f.T(12, 15, "U (V)", "currentColor", 13, "start", "700")
    f.T(392, 285, "I (A)", "currentColor", 13, "start", "700")
    return xs


def head(name):
    return (f'<defs><marker id="{name}-c" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>')


def check_data(xs, ds, table):
    """Điểm đo phải khớp bảng của spec (<0,1 px) và cách đường khớp ≤ 6 px theo y."""
    out = []
    for (I, U), (tx, ty) in zip(zip(ds["I"], ds["U"]), table):
        x, y = xs(I), vc(U)
        assert abs(x - tx) < 0.1 and abs(y - ty) < 0.1, (I, U, x, y, tx, ty)
        assert abs(y - vc(ds["a"] + ds["b"] * I)) <= 6, (I, U)
        out.append((x, y))
    return out


def check_linear(xs, imax, ticks):
    ds = [xs(i) for i in ticks]
    steps = [round(b - a, 6) for a, b in zip(ds, ds[1:])]
    assert max(steps) - min(steps) < 1e-6, steps                  # chia tuyến tính
    assert abs(xs(imax) - XEND) < 1e-9
    uy = [vc(1.0 + k * 0.1) for k in range(8)]
    st = [round(a - b, 6) for a, b in zip(uy, uy[1:])]
    assert max(st) - min(st) < 1e-6 and abs(uy[0] - 250) < 1e-9 and abs(uy[-1] - 30) < 1e-9


# ---------- Hình 3: pin cũ
f3 = Fig("f3", 290)
f3.add(head("f3"))
xs3 = axes(f3, 0.6, [0, .1, .2, .3, .4, .5, .6])
check_linear(xs3, 0.6, [0, .1, .2, .3, .4, .5, .6])
assert abs(xs3(.3) - (xs3(.2) + xs3(.4)) / 2) < 1e-9
T3 = [(68.2, 99.1), (98.5, 111.7), (128.2, 124.3), (171.4, 140.0), (241.4, 171.4), (371.5, 231.1)]
pts3 = check_data(xs3, OLD, T3)
# đường khớp I: 0 -> 0,6
p0, p1 = (xs3(0), vc(OLD["a"])), (xs3(0.6), vc(OLD["a"] + OLD["b"] * 0.6))
assert abs(p0[1] - 94.1) < .05 and abs(p1[1] - 246.1) < .05, (p0, p1)
f3.add(line(*p0, *p1, GRN, 2))
# tam giác hệ số góc A, B
A3, B3 = (xs3(0), vc(1.50)), (xs3(0.5), vc(1.09))
for P, I_ in ((A3, 0), (B3, 0.5)):
    assert abs(P[1] - vc(OLD["a"] + OLD["b"] * I_)) < 1.5      # A (1,50 V) làm tròn từ 1,496 → lệch 1,2 px
assert abs(A3[1] - 92.9) < .05 and abs(B3[0] - 351.7) < .05 and abs(B3[1] - 221.7) < .05
f3.add(line(*A3, B3[0], A3[1], "currentColor", 1.4, "5 4", .6))
f3.add(line(B3[0], A3[1], *B3, "currentColor", 1.4, "5 4", .6))
for (x, y) in pts3:
    f3.add(dot(x, y, 4, RED)); f3.D(x, y, 4)
f3.add(dot(*p0, 4, GRN)); f3.D(*p0, 4)
f3.add(dot(*A3, 4, YEL, "currentColor")); f3.D(*A3, 4)
f3.add(dot(*B3, 4, YEL, "currentColor")); f3.D(*B3, 4)
f3.T(68, 70, "ℰ ≈ 1,50 V", GRN, 13, "start", "700")
f3.T(68, 86, "A", "currentColor", 13, "start", "700")
f3.T(344, 207, "B", "currentColor", 13, "end", "700")
f3.T((A3[0] + B3[0]) / 2, 87, "ΔI = 0,500 A", "currentColor", 13, "middle", "400")
f3.T(B3[0] + 6, 157, "ΔU = 0,41 V", "currentColor", 13, "start", "400")
f3.T(200, 44, "r = ΔU/ΔI = 0,82 Ω", "currentColor", 13, "start", "700")
assert abs(A3[1] - B3[1]) == abs(vc(1.50) - vc(1.09)) and abs((1.50 - 1.09) - 0.41) < 1e-9
fig3 = fig(f3, "Đồ thị U theo I với sáu điểm đo nằm gần một đường thẳng dốc xuống, cắt trục U tại 1,50 V; hai điểm A và B trên đường tạo tam giác hệ số góc.",
           "Hình 3. Đồ thị pin cũ: đường khớp cắt trục U tại ℰ ≈ 1,50 V; A, B cho r = 0,82 Ω.")

# ---------- Hình 4: hai pin cùng hệ trục
f4 = Fig("f4", 290)
f4.add(head("f4"))
ticks4 = [0, .2, .4, .6, .8]
xs4 = axes(f4, 0.8, ticks4)
check_linear(xs4, 0.8, ticks4)
T_OLD = [(66.1, 99.1), (88.9, 111.7), (111.2, 124.3), (143.6, 140.0), (196.1, 171.4), (293.6, 231.1)]
T_NEW = [(66.6, 67.7), (91.9, 74.0), (116.4, 77.1), (154.9, 83.4), (222.7, 96.0), (366.7, 124.3)]
po, pn = check_data(xs4, OLD, T_OLD), check_data(xs4, NEW, T_NEW)
assert max(x for x, _ in pn) <= 410 and abs(pn[-1][0] - 366.7) < .1
o0, o1 = (xs4(0), vc(OLD["a"])), (xs4(0.6), vc(OLD["a"] + OLD["b"] * 0.6))      # pin cũ vẽ tới 0,6 A (0,7 A: U < 1,0 ngoài khung)
n0, n1 = (xs4(0), vc(NEW["a"])), (xs4(0.8), vc(NEW["a"] + NEW["b"] * 0.8))
assert abs(o0[1] - 94.1) < .05 and abs(n0[1] - 66.8) < .05 and abs(o1[0] - 322.5) < .05 and abs(n1[1] - 131.9) < .05
assert abs(NEW["b"]) < abs(OLD["b"])                                   # pin mới thoải hơn
assert vc(OLD["a"] + OLD["b"] * 0.6) < 250                              # đầu mút đường đỏ còn trong khung
# đường dóng 0,5 A: giao điểm TÍNH TỪ PHƯƠNG TRÌNH (spec ghi y = 97,3 cho điểm xanh là nhầm; U = 1,583 − 0,259·0,5 = 1,4535 V ≈ 1,45 V → y ≈ 107,5)
XD = xs4(0.5)
UO, UN = OLD["a"] + OLD["b"] * 0.5, NEW["a"] + NEW["b"] * 0.5
assert f"{UO:.2f}" == "1.09" and f"{UN:.2f}" == "1.45", (UO, UN)
yo, yn = vc(UO), vc(UN)
assert abs(XD - 278.8) < .1 and abs(yo - 220.8) < .1 and abs(yn - 107.5) < .1, (XD, yo, yn)
f4.add(line(o0[0], o0[1], o1[0], o1[1], RED, 2))
f4.add(line(n0[0], n0[1], n1[0], n1[1], BLUE, 2))
f4.add(line(XD, 250, XD, yn, "currentColor", 1.4, "5 4", .5))
for (x, y) in po:
    f4.add(dot(x, y, 3.5, RED)); f4.D(x, y, 3.5)
for (x, y) in pn:
    f4.add(dot(x, y, 3.5, BLUE)); f4.D(x, y, 3.5)
f4.add(dot(XD, yo, 3, RED) + dot(XD, yn, 3, BLUE)); f4.D(XD, yo, 3); f4.D(XD, yn, 3)
f4.T(XD - 7, yo + 17, "1,09 V", RED, 13, "end", "700")
f4.T(XD + 7, yn - 7, "1,45 V", BLUE, 13, "start", "700")
f4.T(XD, 268, "0,5 A", "currentColor", 12, "middle", "700")
f4.T(250, 78, "pin mới · r ≈ 0,26 Ω", BLUE, 13, "start", "700")
f4.T(332, 214, "pin cũ", RED, 13, "start", "700")
f4.T(332, 229, "r ≈ 0,82 Ω", RED, 13, "start", "700")
fig4 = fig(f4, "Hai đường thẳng U theo I trên cùng hệ trục: đường pin mới thoải, đường pin cũ dốc; tại 0,5 A pin mới còn 1,45 V, pin cũ còn 1,09 V.",
           "Hình 4. Pin mới (xanh) thoải hơn pin cũ (đỏ); ở 0,5 A còn 1,45 V so với 1,09 V.",
           exp="tn-l11-do-sdd-pin-02")

# ---------- ghi theory.html
src = (HERE / "theory.src.html").read_text(encoding="utf8")
figs = (fig1, fig2, fig3, fig4)
for n, f in enumerate(figs, 1):
    assert f"<!--FIG{n}-->" in src, n
    src = src.replace(f"<!--FIG{n}-->", f)
assert "<!--FIG" not in src
(HERE / "theory.html").write_text(src, encoding="utf8")
print("ok", len(src), "· 4 hình")
