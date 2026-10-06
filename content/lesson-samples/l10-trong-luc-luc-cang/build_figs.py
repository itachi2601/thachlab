"""Sinh 4 hình SVG cho bài 'Trọng lực và lực căng' (lesson 62), thay mốc <!--FIGn--> trong theory.src.html -> theory.html.
Có lớp kiểm hình học: hộp nhãn không chồng nhau, không vượt viewBox; mũi tên đúng chiều vật lí; trọng tâm tính từ đa giác.
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
        self.body, self.labels, self.markers, self.arrows = "", [], set(), {}

    def add(self, s):
        self.body += s

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

    def dot(self, x, y, r=4, c="currentColor"):
        self.body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

    def arr(self, tag, c, x1, y1, x2, y2, w=3, head=11, dash=""):
        """Mũi tên có ĐỈNH đúng tại (x2,y2); marker cỡ cố định (userSpaceOnUse)."""
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * head, y2 - uy * head
        self.markers.add((c, head))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
                      f'marker-end="url(#{self.name}-{c}{head})"/>')
        self.arrows[tag] = (x1, y1, x2, y2)

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
            if a[5] < 13 and not a[0].isdigit():
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 13")
            if a[1] < 2 or a[3] > self.w - 2 or a[2] < 0 or a[4] > self.h:
                errs.append(f"{self.name}: nhãn '{a[0]}' vượt viewBox {a[1:5]}")
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' chồng '{b[0]}'")
        return errs

    def svg(self, label, cap, exp=None):
        s = wrap(f"0 0 {self.w} {self.h}", label, self.defs() + self.body, cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s


ERR = []

# ---------------- Hình 1: trọng lực hướng về tâm Trái Đất ở mọi nơi
c = Canvas("f1", 400, 290)
EX, EY, R = 200, 160, 82
c.add(f'<circle cx="{EX}" cy="{EY}" r="{R}" fill="rgba(56,189,248,.12)" stroke="currentColor" stroke-width="2.2"/>')
c.dot(EX, EY, 4)
c.text(EX, EY + 22, "Tâm Trái Đất", size=13, anchor="middle", weight="600")
LP = 46
for k, ang in enumerate((90, 18, 162, 232)):
    a = math.radians(ang)
    ux, uy = math.cos(a), -math.sin(a)                 # hướng từ tâm ra ngoài (y màn hình hướng xuống)
    sx, sy = EX + (R + 14) * ux, EY + (R + 14) * uy     # tâm vật (khối vuông cạnh 20 đặt trên mặt đất)
    rot = -(ang - 90)
    c.add(f'<rect x="{sx-10:.1f}" y="{sy-10:.1f}" width="20" height="20" fill="rgba(251,146,60,.35)" stroke="currentColor" stroke-width="1.8" transform="rotate({rot:.1f} {sx:.1f} {sy:.1f})"/>')
    c.line(sx, sy, EX, EY, "currentColor", 1.2, "4 4", .45)
    tx, ty = sx - LP * ux, sy - LP * uy                  # đỉnh mũi tên: đi VÀO tâm
    c.arr(f"P{k}", "r", sx, sy, tx, ty, 3)
    # kiểm: mũi tên hướng về tâm
    if math.hypot(tx - EX, ty - EY) >= math.hypot(sx - EX, sy - EY):
        ERR.append("f1: mũi tên P không hướng về tâm")
    # nhãn P đặt bên cạnh mũi tên, lệch theo pháp tuyến
    nx, ny = -uy, ux
    mx, my = (sx + tx) / 2, (sy + ty) / 2
    c.text(mx + 16 * nx - 5, my + 16 * ny + 5, "P", RED, 16, "start", italic=True)
c.text(16, 24, "Mọi nơi: P hướng về tâm Trái Đất", size=13, weight="600")
fig1 = c.svg("Trái Đất và bốn vật ở bốn nơi, trọng lực của mỗi vật đều hướng về tâm Trái Đất",
             "Hình 1. Ở bất kì đâu, trọng lực <em>P</em> cũng có phương thẳng đứng tại chỗ đó và hướng về tâm Trái Đất (hình không theo tỉ lệ).")
ERR += c.check()

# ---------------- Hình 2: tìm trọng tâm bằng dây dọi (a, b) + đĩa CD (c)
shape = [(0, 0), (90, -8), (104, 40), (70, 92), (18, 74), (-8, 34)]   # tấm bìa bất kì (toạ độ riêng)


def centroid(p):
    A = cx = cy = 0
    for (x1, y1), (x2, y2) in zip(p, p[1:] + p[:1]):
        k = x1 * y2 - x2 * y1
        A += k; cx += (x1 + x2) * k; cy += (y1 + y2) * k
    A /= 2
    return cx / (6 * A), cy / (6 * A)


Gx, Gy = centroid(shape)
HA = (40, 2)       # lỗ A (gần mép trên)
HB = (88, 52)      # lỗ B (gần mép phải, đủ xa mép để chấm r=3,5 nằm trong bìa)


def hang(hole, px, py, other=None):
    """Xoay tấm bìa quanh lỗ sao cho G nằm ngay dưới lỗ; lỗ đặt tại (px,py). Trả (điểm biến đổi, hàm f)."""
    dx, dy = Gx - hole[0], Gy - hole[1]
    th = math.atan2(dx, dy)            # góc cần xoay để (dx,dy) thành (0,+|d|)
    ct, st = math.cos(th), math.sin(th)

    def f(p):
        x, y = p[0] - hole[0], p[1] - hole[1]
        return px + x * ct - y * st, py + x * st + y * ct
    return f


c = Canvas("f2", 440, 250)
for panel, (hole, hole2, ox) in enumerate(((HA, None, 76), (HB, HA, 226))):
    f = hang(hole, ox, 46)
    pts = [f(p) for p in shape]
    c.add(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="rgba(251,146,60,.22)" stroke="currentColor" stroke-width="2"/>')
    g = f((Gx, Gy)); h = f(hole)
    if abs(g[0] - h[0]) > 0.5 or g[1] <= h[1]:
        ERR.append(f"f2: panel {panel}: G không nằm ngay dưới lỗ treo")
    # đinh + dây dọi thẳng đứng qua lỗ, quả dọi ở dưới
    c.line(h[0] - 14, 30, h[0] + 14, 30, "currentColor", 3)
    c.dot(h[0], h[1], 3.5)
    yb = 205
    c.line(h[0], h[1], h[0], yb, BLUE, 2)
    c.add(f'<path d="M{h[0]-6:.1f},{yb:.1f} L{h[0]+6:.1f},{yb:.1f} L{h[0]:.1f},{yb+14:.1f} Z" fill="{BLUE}"/>')
    c.dot(g[0], g[1], 4.5, RED)
    lab = "A" if hole is HA else "B"
    c.text(h[0] + 9, h[1] + 15, lab, size=14, italic=True)
    if hole2 is not None:                 # đường kẻ lần trước (qua A và G) giữ lại trên bìa, nét đứt
        a2 = f(hole2)
        vx, vy = g[0] - a2[0], g[1] - a2[1]
        Lv = math.hypot(vx, vy)
        e2 = (a2[0] + vx / Lv * (Lv + 30), a2[1] + vy / Lv * (Lv + 30))
        c.line(a2[0], a2[1], e2[0], e2[1], BLUE, 1.6, "5 4", .8)
        c.dot(a2[0], a2[1], 3)
        c.text(a2[0] - 8, a2[1] + 4, "A", size=14, anchor="end", italic=True)
        # kiểm: G nằm trên đường AG (đã kẻ lần trước)
        cross = (g[0] - a2[0]) * (e2[1] - a2[1]) - (g[1] - a2[1]) * (e2[0] - a2[0])
        if abs(cross) > 1:
            ERR.append("f2: G không nằm trên đường kẻ lần 1")
    gx_lab = g[0] + 9 if panel == 0 else g[0] + 10
    c.text(gx_lab, g[1] + 18, "G", RED, 15, italic=True)
    c.text(ox, 240, "(a) treo ở A" if panel == 0 else "(b) treo ở B", size=13, anchor="middle", weight="600")
# (c) đĩa CD: G ở tâm lỗ
vx0, vy0, Ro, Ri = 372, 118, 40, 20
c.line(vx0 - 14, 30, vx0 + 14, 30, "currentColor", 3)
c.line(vx0, 30, vx0, vy0 - Ro, "currentColor", 1.8)
c.add(f'<path d="M{vx0-Ro},{vy0} a{Ro},{Ro} 0 1,0 {2*Ro},0 a{Ro},{Ro} 0 1,0 {-2*Ro},0 Z M{vx0-Ri},{vy0} a{Ri},{Ri} 0 1,1 {2*Ri},0 a{Ri},{Ri} 0 1,1 {-2*Ri},0 Z" '
      f'fill="rgba(148,163,184,.35)" fill-rule="evenodd" stroke="currentColor" stroke-width="2"/>')
c.line(vx0, vy0 - Ro, vx0, 205, BLUE, 1.6, "5 4", .8)
c.dot(vx0, vy0, 4.5, RED)
c.text(vx0 + 7, vy0 + 5, "G", RED, 15, italic=True)
c.text(vx0, 240, "(c) đĩa CD", size=13, anchor="middle", weight="600")
fig2 = c.svg("Tìm trọng tâm tấm bìa: treo ở A rồi ở B, hai đường dây dọi cắt nhau tại G; đĩa CD có trọng tâm ở tâm lỗ",
             "Hình 2. (a), (b): treo bìa ở hai lỗ khác nhau, hai đường dây dọi (xanh) cắt nhau tại trọng tâm <em>G</em>. (c): trọng tâm đĩa CD ở tâm lỗ, ngoài phần vật chất.",
             exp="tn-l10-trong-luc-luc-cang-01")
ERR += c.check()

# ---------------- Hình 3: lực căng ở hai đầu dây treo vật
c = Canvas("f3", 400, 320)
X, YC, YT = 170, 34, 196                # trần ở y=34, đầu dưới dây (chỗ buộc vật) ở y=196
c.line(80, YC, 260, YC, "currentColor", 3)
for k in range(9):
    c.line(86 + k * 20, YC, 78 + k * 20, YC - 10, "currentColor", 1.5, "", .55)
c.line(X, YC, X, YT, "currentColor", 2, "", .55)          # sợi dây
c.add(f'<rect x="{X-30}" y="{YT}" width="60" height="48" rx="4" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2.2"/>')
GYc = YT + 24
L_T = 62
c.arr("T", "b", X, YT, X, YT - L_T, 3.4)                 # dây kéo vật: đặt ở chỗ buộc, hướng LÊN (vào giữa dây)
c.arr("T2", "b", X, YC, X, YC + L_T, 3.4)                # dây kéo trần: đặt ở móc, hướng XUỐNG (vào giữa dây)
c.dot(X, GYc, 4)
c.arr("P", "r", X, GYc, X, GYc + L_T, 3.4)               # trọng lực, vật đứng yên nên P = T (dài bằng nhau)
c.text(X + 12, YT - 26, "T", BLUE, 16, italic=True)
c.text(X + 26, YT - 26, ": dây kéo vật", BLUE, 13, weight="600")
c.text(X + 12, YC + 40, "T′", BLUE, 16, italic=True)
c.text(X + 33, YC + 40, ": dây kéo trần", BLUE, 13, weight="600")
c.text(X + 12, GYc + 50, "P", RED, 16, italic=True)
c.text(X + 26, GYc + 50, ": Trái Đất hút vật", RED, 13, weight="600")
c.text(X - 40, YC + 104, "hai đầu dây:", size=13, anchor="end", weight="600")
c.text(X - 40, YC + 122, "T hướng vào", size=13, anchor="end", weight="600")
c.text(X - 40, YC + 140, "giữa dây", size=13, anchor="end", weight="600")
# kiểm chiều: T (đặt ở đầu dưới) phải hướng lên trên; T' (đặt ở đầu trên) hướng xuống; cả hai đều hướng VÀO giữa dây
mid = (YC + YT) / 2
for tag in ("T", "T2"):
    x1, y1, x2, y2 = c.arrows[tag]
    if abs(y2 - mid) >= abs(y1 - mid):
        ERR.append(f"f3: {tag} không hướng vào giữa dây")
fig3 = c.svg("Vật treo dưới trần bằng dây: lực căng T đặt lên vật hướng lên, lực căng T phẩy đặt lên trần hướng xuống, trọng lực P hướng xuống",
             "Hình 3. Lực căng ở hai đầu dây đều hướng vào giữa dây: <em>T</em> kéo vật lên, <em>T</em>′ kéo móc trần xuống. Vật đứng yên nên <em>T</em> = <em>P</em> (mũi tên dài bằng nhau).")
ERR += c.check()

# ---------------- Hình 4: hệ vật nối dây qua ròng rọc (dùng cho bài toán mẫu: mA = 2 kg, mB = 0,5 kg, T = 4 N, PB = 5 N, a = 2 m/s²)
c = Canvas("f4", 400, 312)
TOP = 132            # mặt bàn
EDGE = 290           # mép bàn
c.add(f'<rect x="20" y="{TOP}" width="{EDGE-20}" height="14" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>')
c.line(40, TOP + 14, 40, 300, "currentColor", 3)
c.line(EDGE - 40, TOP + 14, EDGE - 40, 300, "currentColor", 3)
# khối A
Ax0, Ax1, Ay0 = 96, 176, TOP - 50
c.add(f'<rect x="{Ax0}" y="{Ay0}" width="{Ax1-Ax0}" height="50" rx="3" fill="rgba(251,146,60,.28)" stroke="currentColor" stroke-width="2.2"/>')
c.text((Ax0 + Ax1) / 2, Ay0 + 32, "A", size=16, anchor="middle", italic=True)
# ròng rọc
PX, PY, PR = EDGE + 14, TOP - 18, 14
ys = PY - PR                         # dây ngang tiếp tuyến đỉnh ròng rọc
c.line(EDGE - 6, TOP, PX, PY, "currentColor", 2.4)     # giá đỡ
c.add(f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="none" stroke="currentColor" stroke-width="2.4"/>')
c.dot(PX, PY, 3)
xs = PX + PR                         # dây thẳng đứng tiếp tuyến bên phải
# khối B
By0 = 214
c.add(f'<rect x="{xs-22}" y="{By0}" width="44" height="40" rx="3" fill="rgba(56,189,248,.22)" stroke="currentColor" stroke-width="2.2"/>')
c.text(xs - 12, By0 + 26, "B", size=15, anchor="middle", italic=True)
c.line(Ax1, ys, PX, ys, "currentColor", 1.8, "", .6)
c.line(xs, PY, xs, By0, "currentColor", 1.8, "", .6)
c.add(f'<path d="M{PX},{ys} A{PR},{PR} 0 0 1 {xs},{PY}" fill="none" stroke="currentColor" stroke-width="1.8" opacity=".6"/>')
# lực: tỉ lệ 12 px / N  -> T = 4 N: 48 px; PB = 5 N: 60 px
K = 12
c.arr("TA", "b", Ax1, ys, Ax1 + 4 * K, ys, 3.2)                       # dây kéo A về phía ròng rọc
c.arr("TB", "b", xs, By0, xs, By0 - 4 * K, 3.2)                        # dây kéo B lên
GBy = By0 + 20
c.dot(xs, GBy, 3.5)
c.arr("PB", "r", xs, GBy, xs, GBy + 5 * K, 3.2)                       # trọng lực B, gốc tại trọng tâm B
c.text(Ax1 + 14, ys - 10, "T", BLUE, 16, italic=True)
c.text(xs - 12, By0 - 26, "T", BLUE, 16, anchor="end", italic=True)
c.text(xs + 10, GBy + 50, sub("P", "B", 12), RED, 16, italic=True)
# gia tốc (xanh lá)
c.arr("aA", "g", Ax0 + 10, Ay0 - 16, Ax0 + 58, Ay0 - 16, 2.6)
c.text(Ax0 + 64, Ay0 - 11, "a", GRN, 16, italic=True)
c.arr("aB", "g", xs - 40, By0 + 4, xs - 40, By0 + 48, 2.6)
c.text(xs - 50, By0 + 32, "a", GRN, 16, anchor="end", italic=True)
c.text(30, 24, "Bàn nhẵn · dây nhẹ, không dãn", size=13, weight="600")
# kiểm chiều: TA hướng về ròng rọc (sang phải), TB hướng lên, PB hướng xuống; tỉ lệ PB/T = 5/4
x1, y1, x2, y2 = c.arrows["TA"]; ERR += [] if x2 > x1 and abs(y2 - y1) < .1 else ["f4: TA sai chiều"]
x1, y1, x2, y2 = c.arrows["TB"]; ERR += [] if y2 < y1 else ["f4: TB sai chiều"]
x1, y1, x2, y2 = c.arrows["PB"]; ERR += [] if y2 > y1 and abs((y2 - y1) / (4 * K) - 5 / 4) < 1e-9 else ["f4: PB sai"]
fig4 = c.svg("Khối A trên bàn nhẵn nối qua ròng rọc ở mép bàn với vật B treo; lực căng T kéo A về phía ròng rọc và kéo B lên, trọng lực PB kéo B xuống",
             "Hình 4. Hệ vật nối dây qua ròng rọc: cùng gia tốc <em>a</em>, cùng lực căng <em>T</em>. Vật B đi xuống nhanh dần nên <em>T</em> &lt; <em>P</em><sub>B</sub> (mũi tên đỏ dài hơn).",
             exp="tn-l10-trong-luc-luc-cang-04")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

h = (HERE / "theory.src.html").read_text(encoding="utf8")
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
