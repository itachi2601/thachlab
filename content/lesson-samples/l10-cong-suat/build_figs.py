"""Sinh 4 hình SVG cho bài 'Bài 24. Công suất' (lesson 69) và thay mốc <!--FIGn--> trong
theory.src.html -> theory.html. Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Tự kiểm bằng toạ độ: nhãn không chồng nhau, không vượt viewBox, không bị nét vẽ cắt xuyên; chấm bảng nằm trên đường
F = P/v; số liệu hình khớp bài (A = mgh, P = A/t, F·v)."""
import math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2) nét vẽ để kiểm nhãn bị cắt
BAD = []
CUR = {"fig": 0}


def defs(p):
    out = "<defs>"
    for n, c in COL.items():
        out += (f'<marker id="{p}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="12" markerHeight="12" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"


def seg(x1, y1, x2, y2):
    SEGS.append((CUR["fig"], x1, y1, x2, y2))


def arrow(p, c, x1, y1, x2, y2, w=3, dash=""):
    seg(x1, y1, x2, y2)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
            f'marker-end="url(#{p}-{c})"/>')


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, track=True):
    if track:
        seg(x1, y1, x2, y2)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="12">{s}</tspan>'


def text(x, y, s, c="currentColor", size=14, anchor="start", weight="700", italic=False):
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.2 * size, plain))
    it = ' font-style="italic" font-family="serif"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{it}>{s}</text>')


def arc_arrow(p, c, cx, cy, r, a0, a1, w=2.6):
    """Cung tròn từ góc a0 tới a1 (độ, hệ SVG: y hướng xuống). a1 > a0 => quay THUẬN chiều kim đồng hồ trên màn hình."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    sweep = 1 if a1 > a0 else 0
    large = 1 if abs(a1 - a0) > 180 else 0
    return (f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}" fill="none" stroke="{COL[c]}" '
            f'stroke-width="{w}" marker-end="url(#{p}-{c})"/>')


def moment_sign(ox, oy, ax, ay, fx, fy):
    """Dấu của r × F trong hệ SVG (y xuống): >0 nghĩa là quay THUẬN kim đồng hồ trên màn hình."""
    return (ax - ox) * fy - (ay - oy) * fx


def dist_point_line(px, py, ax, ay, ux, uy):
    """Khoảng cách từ điểm P tới đường thẳng qua A, hướng (ux, uy)."""
    n = math.hypot(ux, uy)
    return abs((px - ax) * uy - (py - ay) * ux) / n


def expect(cond, msg):
    if not cond:
        BAD.append(msg)


def rect(x, y, w, h, fill="none", stroke="currentColor", sw=2, dash="", rx=3, track=True):
    if track:
        seg(x, y, x + w, y); seg(x, y + h, x + w, y + h); seg(x, y, x, y + h); seg(x + w, y, x + w, y + h)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


VB = {}
G = 10.0

# ---------------- Hình 1: hai thang máy nâng cùng thùng lên cùng độ cao (mở bài, không lộ đáp án) ----------------
CUR["fig"] = 1
VB[1] = (440, 240)
GY, TOPY = 200, 90                 # mặt đất; đáy cabin ở vị trí cuối (nét đứt)
CABW, CABH = 60, 50
b = defs("f1")
for name, cx, dimx, anchor in (("Thang A", 110, 52, "end"), ("Thang B", 330, 388, "start")):
    x0 = cx - CABW / 2
    b += line(cx - 52, GY, cx + 52, GY, "currentColor", 2.4)                       # mặt đất
    b += rect(x0, GY - CABH, CABW, CABH, "rgba(148,163,184,.25)", "currentColor", 2.4)   # cabin ở dưới
    b += rect(x0, TOPY - CABH, CABW, CABH, "none", "currentColor", 1.8, "6 5", track=False)  # vị trí cuối (nét đứt)
    b += text(cx, GY - 18, "500 kg", "currentColor", 13, "middle", "600")
    b += arrow("f1", "g", cx, GY - CABH - 5, cx, TOPY + 6, 3.2)                  # chuyển động lên
    b += line(dimx, TOPY, dimx, GY, "currentColor", 1.5)
    b += line(dimx - 6, TOPY, dimx + 6, TOPY, "currentColor", 1.5) + line(dimx - 6, GY, dimx + 6, GY, "currentColor", 1.5)
    hx = dimx - 6 if anchor == "end" else dimx + 8
    b += text(hx, (TOPY + GY) / 2 + 5, "h", "currentColor", 16, anchor, "700", True)
    b += text(cx, 226, name, "currentColor", 14, "middle")
expect(abs((GY - CABH) - (TOPY + 6)) > 40, "Hình 1: mũi tên chuyển động đủ dài")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Hai thang máy A và B cùng nâng một thùng hàng 500 kg từ mặt đất lên cùng độ cao h; cabin nét liền ở dưới, vị trí cuối vẽ nét đứt", b,
            "Hình 1. Hai thang máy nâng cùng thùng hàng từ mặt đất lên cùng độ cao <em>h</em> (vị trí cuối vẽ nét đứt). Mũi tên xanh lá là chiều chuyển động.")

# ---------------- Hình 2: đồ thị F = P/v (xe máy 6 kW), chấm khớp bảng ----------------
CUR["fig"] = 2
VB[2] = (440, 280)
AX, AY = 64, 232                    # gốc toạ độ
PXV, PXF = 16.0, 0.0625             # px cho 1 m/s ; px cho 1 N  (trục chia tuyến tính)
PMAX = 6000.0
def X(v): return AX + PXV * v
def Y(f): return AY - PXF * f
b = defs("f2")
b += line(AX, AY, 420, AY, "currentColor", 2) + line(AX, AY, AX, 26, "currentColor", 2)
for v in (5, 10, 15, 20):
    b += line(X(v), AY, X(v), AY + 5, "currentColor", 1.5, track=False)
    b += text(X(v), AY + 21, str(v), "currentColor", 13, "middle", "600")
b += text(AX, AY + 21, "0", "currentColor", 13, "middle", "600")
for f in (1000, 2000, 3000):
    b += line(AX - 5, Y(f), AX, Y(f), "currentColor", 1.5, track=False)
    b += line(AX, Y(f), 420, Y(f), "currentColor", 1, "3 5", .3, track=False)
    b += text(AX - 9, Y(f) + 5, f"{f:,}".replace(",", " "), "currentColor", 13, "end", "600")
b += text(418, AY + 40, "v (m/s)", "currentColor", 14, "end", "700", True)
b += text(10, 20, "F (N)", "currentColor", 14, "start", "700", True)
# đường cong
pts = []
v = 1.9
while v <= 22.0 + 1e-9:
    pts.append((X(v), Y(PMAX / v)))
    v += 0.1
for p, q in zip(pts, pts[1:]):
    seg(p[0], p[1], q[0], q[1])
b += '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{RED}" stroke-width="3"/>'
TABLE2 = [(20, 300), (10, 600), (5, 1200), (2, 3000)]
for vv, ff in TABLE2:
    expect(abs(vv * ff - PMAX) < 1e-9, f"Hình 2: ({vv}; {ff}) không thuộc P = 6 kW")
    b += f'<circle cx="{X(vv):.1f}" cy="{Y(ff):.1f}" r="5.5" fill="{BLUE}" stroke="currentColor" stroke-width="1.5"/>'
    # chấm nằm trên đường cong (khoảng cách tới điểm gần nhất của polyline)
    dmin = min(math.hypot(X(vv) - x, Y(ff) - y) for x, y in pts)
    expect(dmin < 1.5, f"Hình 2: chấm ({vv}; {ff}) lệch đường cong {dmin:.1f} px")
b += text(X(2) + 12, Y(3000) - 6, "3 000 N", BLUE, 13, "start", "700")
b += text(X(5) + 12, Y(1200) - 8, "1 200 N", BLUE, 13, "start", "700")
b += text(X(10) + 12, Y(600) - 10, "600 N", BLUE, 13, "start", "700")
b += text(X(20), Y(300) - 12, "300 N", BLUE, 13, "middle", "700")
b += text(200, 76, "lên dốc: v nhỏ, F lớn", "currentColor", 13, "start", "600")
b += text(418, 134, "đường bằng: v lớn, F nhỏ", "currentColor", 13, "end", "600")
b += text(418, 32, "P = F·v = 6 kW", RED, 14, "end", "700")
expect(abs(X(22) - 416) < 1e-9, "Hình 2: trục v")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Đồ thị lực kéo lớn nhất F theo vận tốc v của xe máy công suất 6 kW: đường hypebol F = 6000/v đi qua bốn điểm của bảng", b,
            "Hình 2. Lực kéo lớn nhất theo vận tốc khi công suất giữ $6\\ \\text{kW}$ (minh hoạ): chấm xanh là bốn hàng của bảng, nằm trên đường $F = P/v$.".replace("$6\\ \\text{kW}$", "6 kW"))

# ---------------- Hình 3: bẫy — công suất lớn không có nghĩa công lớn ----------------
CUR["fig"] = 3
VB[3] = (440, 250)
BASE = 190
SCP, SCA = 30.0, 4.0                # px/kW ; px/kJ
P_X, T_X, P_Y, T_Y = 4.0, 5.0, 1.0, 30.0
A_X, A_Y = P_X * T_X, P_Y * T_Y       # kJ
expect(A_X == 20.0 and A_Y == 30.0 and A_Y > A_X and P_X > P_Y, "Hình 3: số liệu")
b = defs("f3")
for (title, cxc, bars, sc, unit) in (("Công suất P", 100, ((40, P_X, RED), (110, P_Y, BLUE)), SCP, "kW"),
                                     ("Công A", 310, ((250, A_X, RED), (320, A_Y, BLUE)), SCA, "kJ")):
    b += text(cxc, 26, title, "currentColor", 14, "middle", "700")
    b += line(cxc - 80, BASE, cxc + 80, BASE, "currentColor", 2)
    for (bx, val, col), nm in zip(bars, ("máy X", "máy Y")):
        h = val * sc
        b += rect(bx, BASE - h, 50, h, col, "currentColor", 1.5, "", 2, track=True).replace('fill="%s"' % col, 'fill="%s" fill-opacity=".55"' % col)
        lab = (f"{val:g}".replace(".", ",")) + " " + unit
        b += text(bx + 25, BASE - h - 8, lab, "currentColor", 14, "middle", "700")
        b += text(bx + 25, BASE + 22, nm, col, 14, "middle", "700")
b += text(220, 240, "X chạy 5 s, Y chạy 30 s (số liệu minh hoạ)", "currentColor", 13, "middle", "600")
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Hai cột công suất: máy X 4 kW cao hơn máy Y 1 kW; hai cột công: máy X 20 kJ thấp hơn máy Y 30 kJ", b,
            "Hình 3. Máy X có công suất lớn hơn nhưng chạy ngắn, nên công nhỏ hơn máy Y chạy lâu (số liệu minh hoạ).")

# ---------------- Hình 4: bài toán mẫu — thang máy nâng đều ----------------
CUR["fig"] = 4
VB[4] = (440, 300)
GY4, TOP4 = 280, 40
CX4 = 140
CW, CH = 80, 56
CY0 = 140                          # đỉnh cabin
PXF4 = 56 / 8000.0                 # 8000 N -> 56 px
m, h_, t_ = 800.0, 15.0, 30.0
Wt = m * G
F_ = Wt
LA = F_ * PXF4
expect(abs(Wt - 8000) < 1e-9 and abs(Wt * h_ - 120000) < 1e-9 and abs(Wt * h_ / t_ - 4000) < 1e-9
       and abs(F_ * (h_ / t_) - 4000) < 1e-9, "Hình 4: số liệu bài mẫu")
b = defs("f4")
b += line(60, GY4, 330, GY4, "currentColor", 2.4)
b += line(60, TOP4, 330, TOP4, "currentColor", 1.6, "7 6", .8)
b += rect(CX4 - CW / 2, CY0, CW, CH, "rgba(148,163,184,.25)", "currentColor", 2.4)
b += text(CX4, CY0 + 20, "800 kg", "currentColor", 13, "middle", "600")
b += arrow("f4", "r", CX4, CY0 - 2, CX4, CY0 - 2 - LA, 3.4)                   # F lên, đầu trên cabin
b += arrow("f4", "o", CX4, CY0 + CH / 2, CX4, CY0 + CH / 2 + LA, 3.4)         # P xuống, từ trọng tâm
expect(abs(LA - 56) < 1e-9, "Hình 4: F và P cùng độ dài (nâng đều)")
b += text(CX4 - 8, CY0 - 2 - LA + 18, "lực kéo F", RED, 14, "end", "700", True)
b += text(CX4 - 8, CY0 + CH / 2 + LA - 2, "trọng lực", ORG, 14, "end", "700", True)
b += arrow("f4", "g", CX4 + 62, CY0 + 34, CX4 + 62, CY0 - 6, 3.2)
b += text(CX4 + 72, CY0 + 18, "v", GRN, 16, "start", "700", True)
dx = 300
b += line(dx, TOP4, dx, GY4, "currentColor", 1.6) + line(dx - 7, TOP4, dx + 7, TOP4, "currentColor", 1.6) + line(dx - 7, GY4, dx + 7, GY4, "currentColor", 1.6)
b += text(dx + 14, 150, "15 m", "currentColor", 14, "start", "700")
b += text(dx + 14, 172, "30 s", "currentColor", 14, "start", "700")
b += text(66, TOP4 - 8, "tầng cuối", "currentColor", 13, "start", "600")
b += text(66, GY4 - 8, "mặt đất", "currentColor", 13, "start", "600")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Thang máy cabin cùng hàng 800 kg đang đi lên đều: lực kéo F hướng lên và trọng lực mg hướng xuống bằng nhau; quãng đường 15 m trong 30 s", b,
            "Hình 4. Nâng đều nên lực kéo <em>F</em> bằng trọng lượng <em>mg</em> (hai mũi tên cùng độ dài). Mũi tên xanh lá là chiều chuyển động; cả hành trình dài 15 m, kéo dài 30 s.")
fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-cong-suat-03"', 1)
fig2 = fig2.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-cong-suat-02"', 1)


# ---------------- Kiểm toạ độ nhãn ----------------
def seg_hits_box(x1, y1, x2, y2, bx0, by0, bx1, by1):
    """Liang–Barsky: đoạn thẳng có đi qua hộp không."""
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - bx0), (dx, bx1 - x1), (-dy, y1 - by0), (dy, by1 - y1)):
        if p == 0:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
            if t0 > t1:
                return False
    return True


for i, (f, x0, y0, x1, y1, s) in enumerate(LABELS):
    W, H = VB[f]
    if x0 < 2 or y0 < 2 or x1 > W - 2 or y1 > H - 2:
        BAD.append(f"Hình {f}: nhãn '{s}' vượt viewBox ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    for g, a0, b0, a1, b1, t in LABELS[i + 1:]:
        if g == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            BAD.append(f"Hình {f}: nhãn '{s}' chồng '{t}'")
    for g, sx1, sy1, sx2, sy2 in SEGS:
        if g == f and seg_hits_box(sx1, sy1, sx2, sy2, x0 + 1, y0 + 1, x1 - 1, y1 - 1):
            BAD.append(f"Hình {f}: nhãn '{s}' bị nét ({sx1:.0f},{sy1:.0f})-({sx2:.0f},{sy2:.0f}) cắt")
print("\n".join(BAD) if BAD else "kiểm toạ độ: ok")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
figs = [fig1, fig2, fig3, fig4]
order = [int(n) for n in re.findall(r"<!--FIG(\d)-->", src)]
assert order == sorted(order) == list(range(1, len(figs) + 1)), order
for n, f in enumerate(figs, 1):
    assert f"Hình {n}." in f, n
    src = src.replace(f"<!--FIG{n}-->", f)

lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
m = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout) or re.search(r'"minutes"\s*:\s*([\d.]+)', r.stdout)
phut = round(float(m.group(1))) if m else None
if phut is None:
    print("KHÔNG đọc được số phút từ lint_do_dai:", r.stdout[:300])
    phut = "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut)
sys.exit(1 if BAD else 0)
