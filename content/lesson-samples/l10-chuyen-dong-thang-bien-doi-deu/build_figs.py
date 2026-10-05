"""Sinh 4 hình SVG cho bài 'Chuyển động thẳng biến đổi đều' (lesson 54), thay mốc <!--FIGn--> trong theory.src.html -> theory.html.
Toạ độ đồ thị TÍNH từ phương trình (v = v0 + at) qua hàm đổi trục; lớp kiểm: hộp nhãn không chồng nhau, không vượt viewBox,
không bị đường đồ thị/mũi tên cắt xuyên; điểm cắt, độ dốc, diện tích đối chiếu lại với số trong bài.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import math, pathlib, re, subprocess, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}


def sub(base, s, size=11):
    return f'{base}<tspan baseline-shift="sub" font-size="{size}">{s}</tspan>'


class Canvas:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.markers, self.segs = "", [], set(), []

    def add(self, s):
        self.body += s

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, obstacle=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
        if obstacle:
            self.segs.append((x1, y1, x2, y2))

    def dot(self, x, y, r=4, c="currentColor"):
        self.body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

    def arr(self, c, x1, y1, x2, y2, w=3, head=11):
        """Mũi tên có ĐỈNH đúng tại (x2,y2); marker cỡ cố định (userSpaceOnUse)."""
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * head, y2 - uy * head
        self.markers.add((c, head))
        col = COL.get(c, "currentColor")
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{col}" stroke-width="{w}" '
                      f'marker-end="url(#{self.name}-{c}{head})"/>')
        self.segs.append((x1, y1, x2, y2))

    def text(self, x, y, s, c="currentColor", size=14, anchor="start", weight="700", italic=False):
        st = ' font-style="italic" font-family="serif"' if italic else ""
        self.body += f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{st}>{s}</text>'
        plain = re.sub(r"<[^>]+>", "", s)
        wdt = 0.58 * size * len(plain)
        x0 = x if anchor == "start" else (x - wdt / 2 if anchor == "middle" else x - wdt)
        self.labels.append((plain, x0, y - 0.78 * size, x0 + wdt, y + 0.22 * size, size))

    def defs(self):
        out = "<defs>"
        for c, hd in sorted(self.markers):
            out += (f'<marker id="{self.name}-{c}{hd}" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="{hd}" markerHeight="{hd}" '
                    f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{COL.get(c, "currentColor")}"/></marker>')
        return out + "</defs>"

    def check(self):
        errs = []
        for i, a in enumerate(self.labels):
            if a[5] < 13:
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 13")
            if a[1] < 2 or a[3] > self.w - 2 or a[2] < 0 or a[4] > self.h:
                errs.append(f"{self.name}: nhãn '{a[0]}' vượt viewBox {tuple(round(v) for v in a[1:5])}")
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' chồng '{b[0]}'")
            for (x1, y1, x2, y2) in self.segs:          # đường cắt xuyên hộp nhãn (lấy mẫu 200 điểm)
                for k in range(201):
                    px, py = x1 + (x2 - x1) * k / 200, y1 + (y2 - y1) * k / 200
                    if a[1] + 1 < px < a[3] - 1 and a[2] + 1 < py < a[4] - 1:
                        errs.append(f"{self.name}: đường ({x1:.0f},{y1:.0f})→({x2:.0f},{y2:.0f}) cắt nhãn '{a[0]}'")
                        break
        return errs

    def svg(self, label, cap, exp=None):
        s = wrap(f"0 0 {self.w} {self.h}", label, self.defs() + self.body, cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s


class Plot:
    """Hệ trục v–t: gốc (ox, oy) màn hình, kx px/s, kv px/(m/s)."""

    def __init__(self, c, ox, oy, kx, kv, tmax, vmax, tticks, vticks):
        self.c, self.ox, self.oy, self.kx, self.kv = c, ox, oy, kx, kv
        X, Y = self.X, self.Y
        c.arr("k", ox, oy, X(tmax) + 22, oy, 1.8, 9)
        c.arr("k", ox, oy, ox, Y(vmax) - 22, 1.8, 9)
        for t in tticks:
            c.line(X(t), oy, X(t), oy + 5, "currentColor", 1.5, obstacle=False)
            c.text(X(t), oy + 20, f"{t:g}", size=13, anchor="middle", weight="600")
        for v in vticks:
            c.line(ox - 5, Y(v), ox, Y(v), "currentColor", 1.5, obstacle=False)
            c.text(ox - 9, Y(v) + 5, f"{v:g}", size=13, anchor="end", weight="600")
        c.text(ox - 8, oy + 20, "O", size=13, anchor="end", weight="600")
        c.text(X(tmax) + 6, oy - 10, "t (s)", size=13, weight="600")
        c.text(ox + 8, Y(vmax) - 12, "v (m/s)", size=13, weight="600")

    def X(self, t):
        return self.ox + self.kx * t

    def Y(self, v):
        return self.oy - self.kv * v


ERR = []

# ---------------- Hình 1: mở bài — hai lần phanh, 36 km/h dừng sau 10 m; 72 km/h: ? (không lộ đáp án)
c = Canvas("f1", 400, 240)
K = 7.0                      # px / m
XB = 112                     # chỗ bắt đầu phanh (đầu xe)


def car(x_front, y_road, col):
    c.add(f'<rect x="{x_front-56}" y="{y_road-26}" width="56" height="18" rx="4" fill="{col}" fill-opacity=".35" stroke="currentColor" stroke-width="2"/>')
    c.add(f'<path d="M{x_front-46},{y_road-26} L{x_front-38},{y_road-38} L{x_front-18},{y_road-38} L{x_front-10},{y_road-26}" fill="none" stroke="currentColor" stroke-width="2"/>')
    for wx in (x_front - 44, x_front - 12):
        c.add(f'<circle cx="{wx}" cy="{y_road-6}" r="6" fill="none" stroke="currentColor" stroke-width="2"/>')


for lane, (yr, kmh, col) in enumerate(((92, "36 km/h", ORG), (192, "72 km/h", BLUE))):
    c.line(14, yr, 390, yr, "currentColor", 2, obstacle=False)                     # mặt đường
    car(XB, yr, col)
    c.text(20, yr - 48, kmh, size=14)
    c.line(XB, yr - 44, XB, yr + 6, RED, 2, "4 3", obstacle=False)                 # vạch bắt đầu phanh
    if lane == 0:
        XS = XB + 10 * K
        c.line(XS, yr - 44, XS, yr + 6, "currentColor", 2.4, obstacle=False)       # vạch dừng
        c.line(XB + 2, yr + 18, XS - 2, yr + 18, "currentColor", 1.5, obstacle=False)
        c.add(f'<path d="M{XB+2},{yr+13} v10 M{XS-2},{yr+13} v10" stroke="currentColor" stroke-width="1.5"/>')
        c.text((XB + XS) / 2, yr + 34, "10 m", size=14, anchor="middle")
        c.text(XS + 8, yr - 30, "dừng", size=13, weight="600")
    else:
        c.line(XB + 2, yr + 18, 384, yr + 18, "currentColor", 1.5, "5 4", obstacle=False)
        c.text(250, yr + 36, "dừng ở đâu?", size=14, anchor="middle")
c.text(XB + 6, 22, "bắt đầu phanh", RED, 13, weight="600")
fig1 = c.svg("Hai lần phanh cùng một xe: ở 36 km/h xe dừng sau 10 m; ở 72 km/h chưa biết xe dừng ở đâu",
             "Hình 1. Cùng xe, cùng đường, cùng cách phanh. Chỉ khác tốc độ lúc bắt đầu phanh.")
ERR += c.check()

# ---------------- Hình 2: đồ thị v–t ba xe. A: v = 1 + t; B: v = 7 − t; C: v = 3
c = Canvas("f2", 440, 300)
p = Plot(c, 50, 252, 50, 25, 6.4, 8, [1, 2, 3, 4, 5, 6], [2, 4, 6, 8])
X, Y = p.X, p.Y
LINES = {"A": (1, 1, GRN), "B": (7, -1, ORG), "C": (3, 0, BLUE)}     # v0, a, màu
for n, (v0, a, col) in LINES.items():
    c.line(X(0), Y(v0), X(6), Y(v0 + a * 6), col, 3.2)
    c.text(X(6) + 8, Y(v0 + a * 6) + 5, n, col, 15)
# tam giác độ dốc trên A, từ t = 4 đến 6
c.line(X(4), Y(5), X(6), Y(5), "currentColor", 1.6, "4 3", obstacle=False)
c.line(X(6), Y(5), X(6), Y(7), "currentColor", 1.6, "4 3", obstacle=False)
c.text(X(5), Y(5) + 17, "Δt = 2 s", size=13, anchor="middle", weight="600")
c.text(X(6) + 8, Y(6) + 5, "Δv = 2 m/s", size=13, weight="600")
# chú giải
for k, (n, s) in enumerate((("A", "nhanh dần đều"), ("B", "chậm dần đều"), ("C", "thẳng đều"))):
    col = LINES[n][2]
    c.text(150, 26 + 18 * k, f"{n}: {s}", col, 13, weight="700")
# kiểm: A, B cắt nhau tại t = 3 s, v = 4 m/s (dùng ở Câu 1 và Câu 5); độ dốc B = −1
tA = (7 - 1) / (1 - (-1))
if abs(tA - 3) > 1e-9 or abs(1 + tA - 4) > 1e-9:
    ERR.append("f2: A, B không cắt nhau tại (3 s; 4 m/s)")
if (Y(1) - Y(7)) / (X(6) - X(0)) * (-p.kx / p.kv) != -1:
    ERR.append("f2: độ dốc B trên hình khác −1 m/s²")
fig2 = c.svg("Đồ thị vận tốc theo thời gian của ba xe: A dốc lên, B dốc xuống, C nằm ngang; tam giác độ dốc trên A",
             r"Hình 2. Đồ thị <em>v</em>–<em>t</em>: A nhanh dần đều ($v_0 = 1\ \text{m/s}$, dốc lên), B chậm dần đều ($v_0 = 7\ \text{m/s}$, dốc xuống), C thẳng đều. Tam giác nét đứt: độ dốc của A là $a = 2/2 = 1\ \text{m/s}^2$.")
ERR += c.check()

# ---------------- Hình 3: diện tích dưới đồ thị v–t = độ dịch chuyển. v0 = 2, a = 1, t = 0..4
c = Canvas("f3", 400, 290)
V0, A3, T3 = 2, 1, 4
V3 = V0 + A3 * T3
p = Plot(c, 50, 248, 64, 28, 4.6, 7, [1, 2, 3, 4], [2, 4, 6])
X, Y = p.X, p.Y
c.add(f'<rect x="{X(0)}" y="{Y(V0)}" width="{X(T3)-X(0)}" height="{Y(0)-Y(V0)}" fill="rgba(56,189,248,.28)"/>')
c.add(f'<polygon points="{X(0)},{Y(V0)} {X(T3)},{Y(V3)} {X(T3)},{Y(V0)}" fill="rgba(52,211,153,.30)"/>')
c.line(X(0), Y(V0), X(T3), Y(V3), "currentColor", 3)
c.line(X(T3), Y(V3), X(T3), Y(0), "currentColor", 1.4, "4 3", obstacle=False)
c.line(X(0), Y(V0), X(T3), Y(V0), "currentColor", 1.2, "3 3", .6, obstacle=False)
c.text((X(0) + X(T3)) / 2, (Y(V0) + Y(0)) / 2 + 6, sub("v", "0", 12) + "t = 8 m", size=15, anchor="middle")
gx, gy = (X(0) + 2 * X(T3)) / 3, (Y(V0) * 2 + Y(V3)) / 3       # trọng tâm tam giác
c.text(gx + 6, gy + 10, "½at² = 8 m", size=15, anchor="middle")
c.text(X(T3) + 8, Y(V3) - 4, "v = 6 m/s", size=13, weight="600")
area = (V0 + V3) / 2 * T3
if area != 16 or V0 * T3 != 8 or 0.5 * A3 * T3 ** 2 != 8:
    ERR.append("f3: diện tích không khớp 8 + 8 = 16 m")
fig3 = c.svg("Hình thang dưới đồ thị v–t chia thành hình chữ nhật v0 t bằng 8 m và tam giác một nửa a t bình phương bằng 8 m",
             r"Hình 3. $v_0 = 2\ \text{m/s}$, $a = 1\ \text{m/s}^2$, $t = 4\ \text{s}$. Diện tích hình thang $= \dfrac{2 + 6}{2}\cdot 4 = 8 + 8 = 16\ \text{m}$: chữ nhật xanh dương là $v_0t$, tam giác xanh lá là $\tfrac12at^2$.")
ERR += c.check()

# ---------------- Hình 4: bài toán mẫu — ô tô v = 2t, xe máy v = 10
c = Canvas("f4", 412, 300)
p = Plot(c, 55, 252, 25, 8, 12, 24, [5, 10], [10, 20])
X, Y = p.X, p.Y
TC, TG = 5, 10                            # cùng vận tốc; gặp nhau
c.add(f'<polygon points="{X(0)},{Y(10)} {X(TC)},{Y(10)} {X(0)},{Y(0)}" fill="rgba(56,189,248,.32)"/>')
c.add(f'<polygon points="{X(TC)},{Y(10)} {X(TG)},{Y(10)} {X(TG)},{Y(20)}" fill="rgba(251,146,60,.32)"/>')
c.line(X(0), Y(0), X(12), Y(24), ORG, 3.2)
c.line(X(0), Y(10), X(12), Y(10), BLUE, 3.2)
c.line(X(TG), Y(20), X(TG), Y(0), "currentColor", 1.4, "4 3", obstacle=False)
c.dot(X(TC), Y(10), 4.5)
c.text(X(0) + 8, Y(10) - 10, "xe máy: v = 10", BLUE, 13)
c.text(X(8.6), Y(17.2) - 14, "ô tô: v = 2t", ORG, 13, anchor="end")
c.text((X(0) * 2 + X(TC)) / 3 + 2, (Y(10) * 2 + Y(0)) / 3 + 5, "25 m", size=14, anchor="middle")
c.text((X(TC) + 2 * X(TG)) / 3 - 2, (Y(10) * 2 + Y(20)) / 3 + 5, "25 m", size=14, anchor="middle")
c.text(X(TG) + 8, Y(10) + 26, "gặp nhau", size=13, weight="600")
c.text(X(TG) + 8, Y(10) + 43, "t = 10 s", size=13, weight="600")
# kiểm: diện tích hai phần bằng nhau = 25 m, tổng mỗi xe 100 m
s1 = 0.5 * TC * 10
s2 = 0.5 * (TG - TC) * (2 * TG - 10)
if s1 != 25 or s2 != 25 or 0.5 * 2 * TG ** 2 != 100 or 10 * TG != 100:
    ERR.append("f4: diện tích không khớp")
fig4 = c.svg("Đồ thị v–t của ô tô (đường dốc lên v = 2t) và xe máy (đường ngang v = 10); hai phần tô màu 25 m bằng nhau, gặp nhau lúc 10 s",
             "Hình 4. Phần tô xanh (0–5&nbsp;s): xe máy bỏ xa ô tô thêm 25&nbsp;m. Phần tô cam (5–10&nbsp;s): ô tô đuổi lại đúng 25&nbsp;m. Hai đường cắt nhau lúc 5&nbsp;s là <strong>cùng vận tốc</strong>; gặp nhau lúc 10&nbsp;s.",
             exp="tn-l10-ctbdd-03")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
phut = round(float(m.group(1).replace(",", "."))) if m else None
if phut is None:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600]); sys.exit(1)
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 4 hình · {phut} phút")
