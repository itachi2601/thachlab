"""Sinh 4 hình SVG cho bài 'Đồ thị độ dịch chuyển – thời gian' (lesson 52), thay mốc <!--FIGn--> trong theory.src.html -> theory.html.
Mọi điểm/đường vẽ qua hàm đổi toạ độ (t, d) -> pixel nên nằm đúng trên đồ thị; có lớp kiểm:
hộp nhãn không chồng nhau, không vượt viewBox, không bị đường/điểm cắt xuyên; độ dốc tính lại khớp số trong bài;
bảng số liệu thí nghiệm trong theory.src.html khớp mô hình.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import math, pathlib, re, subprocess, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
ERR = []


def fmt(v):
    return f"{v:g}".replace(".", ",")


class Canvas:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.markers, self.segs = "", [], set(), []

    def add(self, s):
        self.body += s

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, obstacle=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" stroke-linecap="round"/>'
        if obstacle:
            self.segs.append((x1, y1, x2, y2))

    def dot(self, x, y, r=4, c="currentColor"):
        self.body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
        self.segs.append((x - r, y, x + r, y))
        self.segs.append((x, y - r, x, y + r))

    def arr(self, c, x1, y1, x2, y2, w=2, head=10):
        """Mũi tên có ĐỈNH đúng tại (x2,y2); marker cỡ cố định (userSpaceOnUse)."""
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * head, y2 - uy * head
        self.markers.add((c, head))
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{COL[c]}" stroke-width="{w}" '
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
                    f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{COL[c]}"/></marker>')
        return out + "</defs>"

    def check(self):
        errs = []
        for i, a in enumerate(self.labels):
            if a[5] < 13:
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 13")
            if a[1] < 2 or a[3] > self.w - 2 or a[2] < 0 or a[4] > self.h:
                errs.append(f"{self.name}: nhãn '{a[0]}' vượt viewBox {[round(v) for v in a[1:5]]}")
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' chồng '{b[0]}'")
            x0, y0, x1, y1 = a[1] - 1, a[2] - 1, a[3] + 1, a[4] + 1
            for (sx1, sy1, sx2, sy2) in self.segs:
                for k in range(61):
                    px, py = sx1 + (sx2 - sx1) * k / 60, sy1 + (sy2 - sy1) * k / 60
                    if x0 < px < x1 and y0 < py < y1:
                        errs.append(f"{self.name}: nhãn '{a[0]}' bị nét ({sx1:.0f},{sy1:.0f})-({sx2:.0f},{sy2:.0f}) cắt")
                        break
        return errs

    def svg(self, label, cap, exp=None):
        s = wrap(f"0 0 {self.w} {self.h}", label, self.defs() + self.body, cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s


class Graph(Canvas):
    """Hệ trục t (ngang) – d (đứng). P(t, d) -> pixel."""

    def __init__(self, name, w, h, ox, oy, sx, sy):
        super().__init__(name, w, h)
        self.ox, self.oy, self.sx, self.sy = ox, oy, sx, sy

    def P(self, t, d):
        return self.ox + t * self.sx, self.oy - d * self.sy

    def axes(self, tmax, dmax, tticks=(), dticks=(), tlab="t (s)", dlab="d (m)", dmin=0):
        xe, _ = self.P(tmax, 0)
        _, ye = self.P(0, dmax)
        _, yb = self.P(0, dmin)
        self.arr("k", self.ox, self.oy, xe, self.oy, 1.8)
        self.arr("k", self.ox, yb, self.ox, ye, 1.8)
        for t in tticks:
            x, _ = self.P(t, 0)
            self.line(x, self.oy, x, self.oy + 5, w=1.5)
            self.text(x, self.oy + 21, fmt(t), size=14, anchor="middle", weight="500")
        for d in dticks:
            _, y = self.P(0, d)
            self.line(self.ox - 5, y, self.ox, y, w=1.5)
            self.text(self.ox - 8, y + 5, fmt(d), size=14, anchor="end", weight="500")
        self.text(self.w - 8, self.oy + 20, tlab, size=14, anchor="end", weight="600")
        self.text(self.ox + 10, ye + 8, dlab, size=14, weight="600")

    def poly(self, pts, c, w=3):
        px = [self.P(*p) for p in pts]
        self.add(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in px)}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>')
        for a, b in zip(px, px[1:]):
            self.segs.append((*a, *b))
        return px


def slope(p, q):
    return (q[1] - p[1]) / (q[0] - p[0])


# ---------------- Hình 1: đồ thị chuyến đi xe đạp — toạ độ x theo t, KHÔNG ghi số (không lộ đáp án)
g = Graph("f1", 400, 250, 50, 210, 30, 22)
g.axes(10.8, 7.9, tlab="t", dlab="x")
F1 = [(0, 0), (3, 6), (6, 6), (9.5, 0)]
px = g.poly(F1, BLUE, 3.2)
g.text(40, 228, "O", size=14, anchor="end", italic=True)
for k, (a, b, lab) in enumerate(((px[0], px[1], "①"), (px[1], px[2], "②"), (px[2], px[3], "③"))):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    vx, vy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(vx, vy)
    nx, ny = vy / L, -vx / L            # pháp tuyến
    if ny > 0:                          # luôn đặt nhãn phía trên đường
        nx, ny = -nx, -ny
    g.text(mx + 20 * nx, my + 20 * ny + 5, lab, size=16, anchor="middle")
# kiểm: đoạn ② nằm ngang, ① đi lên, ③ đi xuống
if not (slope(F1[0], F1[1]) > 0 and slope(F1[1], F1[2]) == 0 and slope(F1[2], F1[3]) < 0):
    ERR.append("f1: dạng ba đoạn sai")
fig1 = g.svg("Đồ thị toạ độ x của bạn đi xe đạp theo thời gian t gồm ba đoạn thẳng: đoạn 1 đi lên, đoạn 2 nằm ngang, đoạn 3 đi xuống về trục t",
             "Hình 1. Ứng dụng bản đồ trên điện thoại: toạ độ <em>x</em> của bạn đi xe đạp theo thời gian <em>t</em> trong một buổi sáng (gốc toạ độ ở nhà bạn).")
ERR += g.check()

# ---------------- Hình 2: thí nghiệm bọt khí — điểm đo + đường thẳng kẻ qua + tam giác độ dốc
V_BOT = 5.0                                   # cm/s, mô hình d = v·t
DATA = [(0, 0), (2.1, 10), (3.9, 20), (6.1, 30), (7.9, 40), (10.0, 50)]
g = Graph("f2", 400, 290, 60, 245, 28, 4)
g.axes(11.4, 56, tticks=(2, 4, 6, 8, 10), dticks=(10, 20, 30, 40, 50), dlab="d (cm)")
g.poly([(0, 0), (10.6, V_BOT * 10.6)], BLUE, 2.4)
for t, d in DATA:
    x, y = g.P(t, d)
    g.dot(x, y, 4.5, ORG)
    if abs(t - d / V_BOT) > 0.1 + 1e-9:
        ERR.append(f"f2: điểm ({t},{d}) lệch mô hình quá 0,1 s")
a, b, c3 = g.P(2.5, 12.5), g.P(8.5, 12.5), g.P(8.5, 42.5)         # đỉnh tam giác tránh các chấm đo
for p in ((2.5, 12.5), (8.5, 42.5)):
    if abs(p[1] - V_BOT * p[0]) > 1e-9:
        ERR.append("f2: đỉnh tam giác độ dốc không nằm trên đường")
g.line(*a, *b, "currentColor", 1.6, "5 4", .8)
g.line(*b, *c3, "currentColor", 1.6, "5 4", .8)
g.text((a[0] + b[0]) / 2, a[1] + 20, "Δt = 6 s", size=14, anchor="middle", weight="600")
g.text(b[0] + 8, (b[1] + c3[1]) / 2 + 5, "Δd = 30 cm", size=14, weight="600")
if abs(30 / 6 - V_BOT) > 1e-9:
    ERR.append("f2: độ dốc tam giác khác 5 cm/s")
fig2 = g.svg("Năm điểm đo thời gian bọt khí đi qua các vạch 10 đến 50 cm nằm gần một đường thẳng qua gốc; tam giác độ dốc Delta t bằng 6 giây, Delta d bằng 30 cm",
             "Hình 2. Số liệu minh hoạ của thí nghiệm bọt khí (chấm cam) và đường thẳng kẻ gần mọi điểm. Độ dốc: 30 cm : 6 s = 5 cm/s.",
             exp="tn-l10-dt-dctg-01")
ERR += g.check()

# kiểm bảng số liệu trong theory.src.html khớp DATA và d/t làm tròn 2 chữ số
src = (HERE / "theory.src.html").read_text(encoding="utf8")
for t, d in DATA[1:]:
    row = f"<tr><td>{d}</td><td>{t:.1f}".replace(".", ",") + f"</td><td>{d / t:.2f}".replace(".", ",") + "</td></tr>"
    if row not in src:
        ERR.append(f"bảng TN1 thiếu/sai hàng: {row}")
dev = [abs(d / t - V_BOT) for t, d in DATA[1:]]
if dev.index(max(dev)) != 0:
    ERR.append("bảng TN1: hàng lệch nhiều nhất không phải hàng đầu (lời nhận xét sẽ sai)")

# ---------------- Hình 3: bốn xe, bốn dạng đường
LINES = [("①", RED, (0, 0), (4, 16)),       # v = 4 m/s
         ("②", ORG, (0, 4), (4, 8)),        # v = 1 m/s
         ("③", BLUE, (0, 10), (4, 10)),     # v = 0
         ("④", GRN, (0, 14), (4, 2))]       # v = -3 m/s
g = Graph("f3", 400, 300, 56, 255, 68, 13)
g.axes(4.65, 17.6, tticks=(1, 2, 3, 4), dticks=(4, 8, 12, 16))
# giao điểm ① – ④ (dùng cho Câu 5): 4t = 14 - 3t
ti = 14 / 7
di = 4 * ti
if abs(di - (14 - 3 * ti)) > 1e-9 or (ti, di) != (2, 8):
    ERR.append("f3: giao điểm ①④ không phải (2 s; 8 m)")
xi, yi = g.P(ti, di)
g.line(xi, yi, xi, g.oy, "currentColor", 1.3, "4 4", .6, obstacle=False)
g.line(g.ox, yi, xi, yi, "currentColor", 1.3, "4 4", .6, obstacle=False)
# dóng riêng cho đường ④: hai đầu (0 s; 14 m) và (4 s; 2 m) — dùng cho Câu 2
for dv in (14, 2):
    _, y = g.P(0, dv)
    g.line(g.ox - 5, y, g.ox, y, GRN, 2)
    g.text(g.ox - 8, y + 5, fmt(dv), GRN, 14, anchor="end", weight="700")
x4, y4 = g.P(4, 2)
g.line(g.ox, y4, x4, y4, GRN, 1.3, "4 4", .7, obstacle=False)
for lab, col, p, q in LINES:
    g.poly([p, q], col, 3)
    x, y = g.P(*q)
    g.text(x + 8, y + 6, lab, col, 16)
g.dot(xi, yi, 4.5)
for q in ((0, 14), (4, 2)):
    g.dot(*g.P(*q), 3.5, GRN)
if [slope(p, q) for _, _, p, q in LINES] != [4, 1, 0, -3]:
    ERR.append("f3: độ dốc bốn đường sai")
fig3 = g.svg("Bốn đường độ dịch chuyển theo thời gian: đường 1 dốc nhiều đi lên, đường 2 dốc ít đi lên, đường 3 nằm ngang, đường 4 đi xuống; đường 1 và 4 cắt nhau",
             "Hình 3. Bốn xe trên cùng một đường thẳng: ① đi lên dốc nhiều, ② đi lên dốc ít, ③ nằm ngang, ④ đi xuống (hai đầu ghi số 14 và 2 trên trục). Chấm tròn: chỗ đường ① cắt đường ④.")
ERR += g.check()

# ---------------- Hình 4: bài toán mẫu — xe đồ chơi O(0;0) A(4;8) B(6;8) C(10;0)
PTS = {"O": (0, 0), "A": (4, 8), "B": (6, 8), "C": (10, 0)}
g = Graph("f4", 400, 280, 56, 235, 28, 21)
g.axes(11.5, 9.6, tticks=(2, 4, 6, 8, 10), dticks=(2, 4, 6, 8))
for nm in ("A", "B"):
    x, y = g.P(*PTS[nm])
    g.line(x, y, x, g.oy, "currentColor", 1.3, "4 4", .6, obstacle=False)
xA, yA = g.P(*PTS["A"])
g.line(g.ox, yA, xA, yA, "currentColor", 1.3, "4 4", .6, obstacle=False)
px4 = g.poly([PTS[k] for k in "OABC"], BLUE, 3.2)
for (x, y) in px4[1:3]:
    g.dot(x, y, 4)
g.text(46, 252, "O", size=15, anchor="end", italic=True)
g.text(xA - 6, yA - 10, "A", size=15, anchor="end", italic=True)
xB, yB = g.P(*PTS["B"])
g.text(xB + 6, yB - 10, "B", size=15, italic=True)
xC, yC = g.P(*PTS["C"])
g.text(xC + 8, yC - 9, "C", size=15, italic=True)
v = [slope(PTS[a], PTS[b]) for a, b in ("OA", "AB", "BC")]
if v != [2, 0, -2]:
    ERR.append(f"f4: vận tốc các đoạn {v} khác 2; 0; -2 m/s")
s_tot = sum(abs(PTS[b][1] - PTS[a][1]) for a, b in ("OA", "AB", "BC"))
if s_tot != 16 or PTS["C"][1] != 0 or s_tot / 10 != 1.6:
    ERR.append("f4: s, d, tốc độ trung bình không khớp lời giải")
if 8 + (-2) * (8 - 6) != 4:
    ERR.append("f4: vị trí lúc 8 s")
fig4 = g.svg("Đồ thị độ dịch chuyển – thời gian của xe đồ chơi: từ O lên A tại 4 giây 8 mét, nằm ngang tới B tại 6 giây, rồi đi xuống về C tại 10 giây 0 mét",
             "Hình 4. Đồ thị độ dịch chuyển – thời gian của xe đồ chơi (chiều dương từ vạch mốc ra cọc cờ).",
             exp="tn-l10-dt-dctg-03")
ERR += g.check()

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

h = src
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
# số phút: điền từ lint_do_dai (đo trên chính bản đã chèn hình)
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
