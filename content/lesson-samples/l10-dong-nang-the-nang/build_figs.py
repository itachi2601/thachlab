"""Sinh 4 hình SVG cho bài 'Động năng, thế năng' (lesson 70) và thay mốc <!--FIGn--> trong
theory.src.html -> theory.html. Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Tự kiểm bằng toạ độ: nhãn không chồng nhau, không vượt viewBox, không bị nét vẽ cắt xuyên; điểm A, B, D nằm
đúng trên ray tàu lượn; mũi tên vận tốc vẽ tỉ lệ; dấu z khớp vị trí so với mốc."""
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


VB = {}
G = 10.0

# ---------------- Hình 1: xe đạp phanh, hai tốc độ (mở bài) ----------------
CUR["fig"] = 1
VB[1] = (440, 235)
PX_M = 35                         # 35 px cho 1 m quãng lết
PX_V = 4                          # 4 px cho 1 km/h


def bike(x, gy):
    """Xe đạp que: bánh sau tâm (x+14, gy-14), bánh trước (x+64, gy-14). Không ghi vào SEGS (nhãn đặt xa xe)."""
    r1, r2 = (x + 14, gy - 14), (x + 64, gy - 14)
    crank, seat, head = (x + 36, gy - 14), (x + 30, gy - 40), (x + 58, gy - 42)
    o = (f'<circle cx="{r1[0]}" cy="{r1[1]}" r="14" fill="none" stroke="currentColor" stroke-width="2.2"/>'
         f'<circle cx="{r2[0]}" cy="{r2[1]}" r="14" fill="none" stroke="currentColor" stroke-width="2.2"/>')
    for a, c in ((r1, crank), (crank, seat), (r1, seat), (seat, head), (crank, head), (head, r2)):
        o += line(*a, *c, "currentColor", 2.2, track=False)
    o += line(seat[0] - 7, seat[1] - 2, seat[0] + 7, seat[1] - 2, "currentColor", 3, track=False)
    o += line(head[0], head[1], head[0] - 4, head[1] - 8, "currentColor", 2.2, track=False)
    o += line(head[0] - 4, head[1] - 8, head[0] + 6, head[1] - 8, "currentColor", 2.2, track=False)
    return o


b = defs("f1")
X_BRAKE = 100
for gy, vkmh, tag, known in ((92, 10, "Hôm qua", True), (205, 20, "Hôm sau", False)):
    b += line(8, gy, 432, gy, "currentColor", 2, op=.6)
    b += bike(12, gy)
    xa = 84
    b += arrow("f1", "g", xa, gy - 30, xa + vkmh * PX_V, gy - 30, 3)
    b += text(xa + 2, gy - 42, f"{vkmh} km/h", GRN, 14, "start")
    b += text(12, gy - 66, tag, "currentColor", 14, "start")
    b += line(X_BRAKE, gy - 8, X_BRAKE, gy + 8, RED, 2)                      # vạch bóp phanh
    if known:
        L = 2 * PX_M
        b += line(X_BRAKE, gy - 1.5, X_BRAKE + L, gy - 1.5, RED, 5, op=.75)  # vệt lết
        b += line(X_BRAKE + L, gy - 22, X_BRAKE + L, gy + 4, "currentColor", 2)
        b += text(X_BRAKE + L + 6, gy - 10, "dừng", "currentColor", 13, "start", "600")
        b += text(X_BRAKE + L / 2, gy + 22, "lết 2 m", RED, 14, "middle")
        expect(abs(L / PX_M - 2) < 1e-9, "Hình 1: vệt lết hôm qua phải đúng 2 m theo tỉ lệ")
    else:
        # nét đứt mờ dần tới mép hình: KHÔNG theo tỉ lệ, không lộ đáp án 8 m
        xs_ = [X_BRAKE + k * 41 for k in range(9)]
        for k, (u0, u1) in enumerate(zip(xs_, xs_[1:])):
            b += line(u0, gy - 1.5, min(u1, 428), gy - 1.5, RED, 5, "4 7", round(.6 - .07 * k, 2))
        b += text(X_BRAKE + 150, gy + 22, "lết ? m (không theo tỉ lệ)", RED, 14, "middle")
    b += text(X_BRAKE - 4, gy + 22, "bóp phanh", RED, 13, "end", "600")
expect(20 * PX_V == 2 * 10 * PX_V, "Hình 1: mũi tên vận tốc phải tỉ lệ 1 : 2")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Hai lần phanh xe đạp: hôm qua 10 km/h lết 2 m; hôm sau 20 km/h, lết bao xa chưa biết", b,
            "Hình 1. Cùng xe, cùng lực phanh (minh hoạ). Mũi tên vận tốc vẽ tỉ lệ: hôm sau dài gấp đôi. Vạch lết hôm sau chưa biết dài bao nhiêu, vẽ không theo tỉ lệ.")

# ---------------- Hình 2: thế năng theo mốc ----------------
CUR["fig"] = 2
VB[2] = (440, 250)
AX2, Y0 = 60, 135                # trục Oz, mốc ở y = 135
b = defs("f2")
b += arrow("f2", "k", AX2, 238, AX2, 14, 2)
b += text(AX2 + 10, 26, "z", "currentColor", 16, "start", "700", True)
b += line(30, Y0, 432, Y0, "currentColor", 1.6, "7 5", .8)
b += text(AX2 - 8, Y0 + 18, "O", "currentColor", 15, "end", "700", True)
b += text(AX2 + 10, Y0 + 20, "mốc thế năng", "currentColor", 13, "start", "600")
XB2 = 200
balls = ((60, BLUE, ("z &gt; 0", "W", "t", " &gt; 0")), (Y0, "currentColor", ("z = 0", "W", "t", " = 0")),
         (210, RED, ("z &lt; 0", "W", "t", " &lt; 0")))
for y, c, (zs, w, sb, rest) in balls:
    b += f'<circle cx="{XB2}" cy="{y}" r="11" fill="rgba(251,146,60,.35)" stroke="{ORG}" stroke-width="2.2"/>'
    b += text(XB2 + 24, y + (-8 if y == Y0 else 5), f"{zs}: " + sub(w, sb) + rest, c, 15, "start")
    expect((y < Y0) == ("&gt;" in zs) and (y > Y0) == ("&lt;" in zs), f"Hình 2: dấu z sai ở y={y}")
# kích thước z cho vật phía trên mốc
XD = 160
b += line(XD, Y0, XD, 60, GRN, 2) + line(XD - 6, 60, XD + 6, 60, GRN, 2) + line(XD - 6, Y0, XD + 6, Y0, GRN, 2)
b += text(XD - 8, 103, "z", GRN, 16, "end", "700", True)
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Trục z hướng lên, gốc tại mốc thế năng; vật phía trên mốc có thế năng dương, tại mốc bằng 0, phía dưới mốc âm", b,
            "Hình 2. Trục <em>z</em> hướng lên, gốc tại mốc. Trên mốc <em>W</em><sub>t</sub> &gt; 0, tại mốc bằng 0, dưới mốc <em>W</em><sub>t</sub> &lt; 0.")

# ---------------- Hình 3: công trọng lực không phụ thuộc đường đi ----------------
CUR["fig"] = 3
VB[3] = (440, 260)
M3, N3 = (110, 50), (330, 196)
K3 = (M3[0], N3[1])
AX3 = 40
b = defs("f3")
b += arrow("f3", "k", AX3, 236, AX3, 14, 2)
b += text(AX3 + 8, 24, "z", "currentColor", 15, "start", "700", True)
for y, lab in ((M3[1], "M"), (N3[1], "N")):
    b += line(AX3 - 5, y, AX3 + 5, y, "currentColor", 2)
    b += line(AX3, y, M3[0], y, "currentColor", 1.2, "4 4", .6, track=False)
    b += text(AX3 - 8, y + 5, sub("z", lab), "currentColor", 14, "end", "700", True)
# đường 1: thẳng M -> N
b += arrow("f3", "b", *M3, *N3, 2.6)
# đường 2: M -> K -> N
b += line(*M3, *K3, ORG, 2.6)
b += arrow("f3", "o", *K3, N3[0] - 2, N3[1], 2.6)
# đường 3: cong (cubic Bezier), ghi từng đoạn vào SEGS
C1, C2 = (270, -10), (420, 110)


def bez(t):
    s = 1 - t
    return (s**3 * M3[0] + 3 * s * s * t * C1[0] + 3 * s * t * t * C2[0] + t**3 * N3[0],
            s**3 * M3[1] + 3 * s * s * t * C1[1] + 3 * s * t * t * C2[1] + t**3 * N3[1])


pts = [bez(i / 40) for i in range(41)]
for p, q in zip(pts, pts[1:]):
    seg(*p, *q)
expect(all(4 < x < 436 and 4 < y < 256 for x, y in pts), "Hình 3: đường cong vượt viewBox")
b += (f'<path d="M{M3[0]},{M3[1]} C{C1[0]},{C1[1]} {C2[0]},{C2[1]} {N3[0]},{N3[1]}" fill="none" stroke="{GRN}" '
      f'stroke-width="2.6" marker-end="url(#f3-g)"/>')
for p, lab in ((M3, "M"), (N3, "N"), (K3, "K")):
    b += f'<circle cx="{p[0]}" cy="{p[1]}" r="4.5" fill="currentColor"/>'
b += text(M3[0] - 10, M3[1] - 10, "M", "currentColor", 16, "end", "700", True)
b += text(N3[0] + 4, N3[1] + 22, "N", "currentColor", 16, "start", "700", True)
b += text(K3[0] - 6, K3[1] + 22, "K", "currentColor", 16, "end", "700", True)
mid1 = ((M3[0] + N3[0]) / 2, (M3[1] + N3[1]) / 2)
b += text(mid1[0] - 14, mid1[1] + 18, "1", BLUE, 15, "end")
b += text(K3[0] + 10, (M3[1] + K3[1]) / 2, "2", ORG, 15, "start")
p3 = bez(0.5)
b += text(p3[0] + 10, p3[1] - 6, "3", GRN, 15, "start")
b += text(220, 250, "A = mg(" + sub("z", "M") + " − " + sub("z", "N") + ") cho cả 3 đường", "currentColor", 14, "middle")
expect(N3[1] > M3[1], "Hình 3: N phải thấp hơn M (đi xuống, công dương)")
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Ba đường đi từ M xuống N: đường thẳng, đường gấp khúc qua K, đường cong; công của trọng lực như nhau", b,
            "Hình 3. Ba đường từ <em>M</em> xuống <em>N</em>: thẳng (1), gấp khúc qua <em>K</em> (2), cong (3). Công của trọng lực chỉ phụ thuộc độ cao đầu và cuối.")

# ---------------- Hình 4: bài toán mẫu — tàu lượn ----------------
CUR["fig"] = 4
VB[4] = (440, 250)
GY4, PZ = 210, 8                  # mặt đất y = 210, 8 px/m
KN = [(14, 14), (80, 18), (230, 3), (360, 13), (430, 8)]   # (x px, z m); A, B, D là các điểm cực trị


def zy(z):
    return GY4 - PZ * z


def track_z(x):
    for (x0, z0), (x1, z1) in zip(KN, KN[1:]):
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return z0 + (z1 - z0) * (1 - math.cos(math.pi * t)) / 2
    raise ValueError(x)


xs = [KN[0][0] + i for i in range(KN[-1][0] - KN[0][0] + 1)]
tp = [(x, zy(track_z(x))) for x in xs]
for p, q in zip(tp, tp[1:]):
    seg(*p, *q)
A4, B4, D4 = [(KN[i][0], zy(KN[i][1])) for i in (1, 2, 3)]
for P, z in ((A4, 18), (B4, 3), (D4, 13)):
    expect(abs(zy(track_z(P[0])) - P[1]) < 1e-9 and abs((GY4 - P[1]) / PZ - z) < 1e-9, f"Hình 4: điểm z={z} không nằm trên ray")
b = defs("f4")
b += line(8, GY4, 432, GY4, "currentColor", 2)
b += '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in tp) + '" fill="none" stroke="currentColor" stroke-width="3"/>'
for P, lab, dx in ((A4, "18 m", 6), (B4, "3 m", 6), (D4, "13 m", 6)):
    b += line(P[0], P[1] + 6, P[0], GY4, "currentColor", 1.2, "4 4", .7, track=False)
    ly = GY4 - 6 if lab == "3 m" else (P[1] + GY4) / 2 + 5
    b += text(P[0] + dx, ly, lab, "currentColor", 13, "start", "600")
# toa tàu tại A
b += f'<rect x="{A4[0]-15}" y="{A4[1]-17}" width="30" height="14" rx="3" fill="rgba(251,146,60,.35)" stroke="{ORG}" stroke-width="2"/>'
b += arrow("f4", "g", A4[0] + 18, A4[1] - 10, A4[0] + 68, A4[1] - 10, 3)
b += text(A4[0] + 20, A4[1] - 24, sub("v", "A") + " = 10 m/s", GRN, 14, "start")
for P in (A4, B4, D4):
    b += f'<circle cx="{P[0]}" cy="{P[1]}" r="4" fill="currentColor"/>'
b += text(A4[0] - 22, A4[1] - 8, "A", "currentColor", 16, "end", "700", True)
b += text(B4[0] - 10, 204, "B", "currentColor", 16, "end", "700", True)
b += text(D4[0], D4[1] - 12, "D", "currentColor", 16, "middle", "700", True)
b += text(12, 236, "mặt đất (mốc thế năng)", "currentColor", 13, "start", "600")
expect(abs(track_z(A4[0] + 1) - 18) < 0.01, "Hình 4: tại A ray nằm ngang nên vận tốc vẽ ngang")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Đường ray tàu lượn: điểm A cao 18 m, toa có vận tốc 10 m/s; điểm B cao 3 m; đỉnh D cao 13 m; mốc thế năng ở mặt đất", b,
            "Hình 4. Ray tàu lượn của bài toán mẫu. Độ cao tính từ mặt đất; độ cao vẽ đúng tỉ lệ, khoảng cách ngang thì không.")
fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-dong-nang-the-nang-03"', 1)

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
phut = int(float(m.group(1)) + 0.5) if m else None
if phut is None:
    print("KHÔNG đọc được số phút từ lint_do_dai:", r.stdout[:300])
    phut = "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut)
sys.exit(1 if BAD else 0)
