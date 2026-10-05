"""Sinh 4 hình SVG cho bài 'Cơ năng và định luật bảo toàn cơ năng' (lesson 71) và thay mốc <!--FIGn--> trong
theory.src.html -> theory.html. Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Tự kiểm bằng toạ độ: nhãn không chồng nhau, không vượt viewBox, không bị nét vẽ cắt xuyên; điểm nằm đúng trên
lòng chảo z = H(x/X)^2; cột năng lượng có tổng không đổi; trục độ cao chia tuyến tính."""
import math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2)
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


def arrow(p, c, x1, y1, x2, y2, w=2.6):
    seg(x1, y1, x2, y2)
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{w}" '
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


def expect(cond, msg):
    if not cond:
        BAD.append(msg)


class Bowl:
    """Lòng chảo parabol: độ cao z (m) = Zr*(dx/X)^2, đáy tại (cx, base)."""

    def __init__(self, cx, base, X, Zr, pxm):
        self.cx, self.base, self.X, self.Zr, self.pxm = cx, base, X, Zr, pxm

    def y(self, z):
        return self.base - z * self.pxm

    def pt(self, z, side):
        dx = self.X * math.sqrt(z / self.Zr)
        return (self.cx + side * dx, self.y(z))

    def z_at(self, x):
        return self.Zr * ((x - self.cx) / self.X) ** 2

    def path(self, n=60):
        pts = []
        for i in range(n + 1):
            x = self.cx - self.X + 2 * self.X * i / n
            pts.append((x, self.y(self.z_at(x))))
        for a, b in zip(pts, pts[1:]):
            seg(*a, *b)
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="3"/>'


VB = {}

# ---------------- Hình 1: lòng chảo mở bài (không lộ đáp án: không vẽ đường ngang độ cao) ----------------
CUR["fig"] = 1
VB[1] = (440, 225)
bw = Bowl(220, 190, 165, 3.0, 43.0)
b = defs("f1")
b += bw.path()
rimL, rimR = bw.pt(3.0, -1), bw.pt(3.0, 1)
b += line(14, rimL[1], rimL[0], rimL[1], "currentColor", 3) + line(rimR[0], rimR[1], 426, rimR[1], "currentColor", 3)
b += f'<circle cx="{rimL[0]-12:.1f}" cy="{rimL[1]-9:.1f}" r="8" fill="{GRN}"/>'
b += text(rimL[0] - 12, rimL[1] - 26, "Lan", GRN, 14, "middle")
# mũi tên chiều chuyển động dọc thành trái, đặt phía trong lòng chảo
p0, p1 = bw.pt(2.4, -1), bw.pt(1.2, -1)
b += arrow("f1", "g", p0[0] + 16, p0[1] - 4, p1[0] + 16, p1[1] - 6, 2.6)
expect(p1[1] > p0[1], "Hình 1: mũi tên phải hướng xuống")
b += text(220, 212, "đáy", "currentColor", 14, "middle", "600")
q = bw.pt(2.0, 1)
b += text(q[0] - 30, q[1] - 6, "?", RED, 26, "middle")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Lòng chảo trượt ván: Lan đứng ở mép trái, chuẩn bị thả mình xuống; thành bên phải có dấu hỏi", b,
            "Hình 1. Lan thả mình từ mép trái lòng chảo, không đạp, không nhún. Lượt đầu, Lan lên thành bên kia tới đâu?")

# ---------------- Hình 2: cột năng lượng quả táo rơi ----------------
CUR["fig"] = 2
VB[2] = (440, 262)
BASE2, PXJ = 200, 13.0          # 13 px cho 1 J
m, g = 0.2, 10
cols = [(90, 5.0, "trên cành", "z = 5 m"), (220, 2.5, "giữa đường", "z = 2,5 m"), (350, 0.0, "chạm đất", "z = 0")]
W_TOT = m * g * 5.0
b = defs("f2")
b += line(30, BASE2, 410, BASE2, "currentColor", 2)
ytop = BASE2 - W_TOT * PXJ
b += line(40, ytop, 400, ytop, "currentColor", 1.5, "6 5", .8)
b += text(40, ytop - 10, "W = 10 J ở cả ba vị trí", "currentColor", 14, "start")
for x, z, lab, zlab in cols:
    wt = m * g * z
    wd = W_TOT - wt
    expect(abs(wt + wd - W_TOT) < 1e-9, "Hình 2: tổng không đổi")
    hb, hg = wt * PXJ, wd * PXJ
    if hb:
        b += f'<rect x="{x-28}" y="{BASE2-hb:.1f}" width="56" height="{hb:.1f}" fill="rgba(56,189,248,.35)" stroke="{BLUE}" stroke-width="2"/>'
        b += text(x, BASE2 - hb / 2 + 5, f"{wt:g} J".replace(".", ","), "currentColor", 14, "middle")
    if hg:
        b += f'<rect x="{x-28}" y="{BASE2-hb-hg:.1f}" width="56" height="{hg:.1f}" fill="rgba(52,211,153,.35)" stroke="{GRN}" stroke-width="2"/>'
        b += text(x, BASE2 - hb - hg / 2 + 5, f"{wd:g} J".replace(".", ","), "currentColor", 14, "middle")
    b += text(x, BASE2 + 22, lab, "currentColor", 14, "middle", "600")
    b += text(x, BASE2 + 42, zlab, "currentColor", 14, "middle", "600")
b += f'<rect x="40" y="12" width="14" height="14" fill="rgba(56,189,248,.35)" stroke="{BLUE}" stroke-width="2"/>'
b += text(60, 24, "thế năng " + sub("W", "t"), BLUE, 14, "start")
b += f'<rect x="230" y="12" width="14" height="14" fill="rgba(52,211,153,.35)" stroke="{GRN}" stroke-width="2"/>'
b += text(250, 24, "động năng " + sub("W", "d"), GRN, 14, "start")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Ba cột năng lượng của quả táo 0,2 kg rơi từ 5 m: trên cành toàn thế năng 10 J, giữa đường 5 J và 5 J, chạm đất toàn động năng 10 J",
            b,
            "Hình 2. Quả táo 0,2 kg rơi từ cành cao 5 m, bỏ qua cản. Phần xanh dương (thế năng) đổi dần thành phần xanh lá (động năng); chiều cao cả cột không đổi.")

# ---------------- Hình 3: có ma sát — đỉnh thấp dần ----------------
CUR["fig"] = 3
VB[3] = (440, 232)
bw3 = Bowl(220, 185, 165, 3.0, 43.0)
b = defs("f3")
b += bw3.path()
r3L, r3R = bw3.pt(3.0, -1), bw3.pt(3.0, 1)
b += line(14, r3L[1], r3L[0], r3L[1], "currentColor", 3) + line(r3R[0], r3R[1], 426, r3R[1], "currentColor", 3)
b += line(r3L[0], r3L[1], r3R[0], r3R[1], ORG, 1.5, "6 5", .9)
b += text(220, r3L[1] - 10, "độ cao xuất phát", ORG, 14, "middle", "600")
peaks = [(3.0, -1, "xuất phát"), (2.6, 1, "đỉnh lượt 1"), (2.2, -1, "đỉnh lượt 2")]
prev = None
for z, side, lab in peaks:
    x, y = bw3.pt(z, side)
    expect(abs(bw3.z_at(x) - z) < 1e-9, f"Hình 3: điểm {lab} không nằm trên lòng chảo")
    if prev is not None:
        expect(z < prev, "Hình 3: đỉnh sau phải thấp hơn")
    prev = z
    b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{GRN}"/>'
pL1 = bw3.pt(2.6, 1)
b += text(pL1[0] - 12, pL1[1] + 4, "đỉnh lượt 1", GRN, 14, "end")
pL2 = bw3.pt(2.2, -1)
b += text(pL2[0] + 12, pL2[1] + 4, "đỉnh lượt 2", GRN, 14, "start")
b += text(220, 212, "mỗi lượt mất một ít cơ năng → nhiệt", ORG, 14, "middle", "600")
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Lòng chảo có ma sát: đỉnh lượt 1 bên phải và đỉnh lượt 2 bên trái thấp dần dưới đường ngang độ cao xuất phát",
            b,
            "Hình 3. Có ma sát và lực cản: đỉnh sau thấp hơn đỉnh trước (độ cao minh hoạ 3,0; 2,6; 2,2 m). Phần cơ năng mất thành nhiệt.")

# ---------------- Hình 4: bài toán mẫu ----------------
CUR["fig"] = 4
VB[4] = (440, 240)
bw4 = Bowl(220, 205, 165, 3.2, 45.0)
b = defs("f4")
b += bw4.path()
A4, M4, B4, O4 = bw4.pt(3.2, -1), bw4.pt(1.4, -1), bw4.pt(2.8, 1), (bw4.cx, bw4.base)
R4 = bw4.pt(3.2, 1)
b += line(14, A4[1], A4[0], A4[1], "currentColor", 3) + line(R4[0], R4[1], 426, R4[1], "currentColor", 3)
for (x, y), z in ((A4, 3.2), (M4, 1.4), (B4, 2.8)):
    expect(abs((bw4.base - y) / bw4.pxm - z) < 1e-9, f"Hình 4: độ cao {z}")
    expect(abs(bw4.z_at(x) - z) < 1e-9, f"Hình 4: điểm z={z} không nằm trên lòng chảo")
for (x, y) in (A4, M4, B4, O4):
    b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{GRN}"/>'
# kích thước độ cao: nét đứt thẳng đứng xuống mức đáy
b += line(A4[0], A4[1] + 6, A4[0], bw4.base, BLUE, 1.5, "5 4", .9)
b += line(M4[0], M4[1] + 6, M4[0], bw4.base, BLUE, 1.5, "5 4", .9)
b += line(B4[0], B4[1] + 6, B4[0], bw4.base, BLUE, 1.5, "5 4", .9)
b += line(14, bw4.base, 426, bw4.base, "currentColor", 1.2, "2 4", .6)
b += text(A4[0] - 6, 150, "3,2 m", BLUE, 14, "end")
b += text(M4[0] - 6, 192, "1,4 m", BLUE, 14, "end")
b += text(B4[0] + 6, 160, "2,8 m", BLUE, 14, "start")
b += text(A4[0] - 4, A4[1] - 10, "A", "currentColor", 15, "middle", "700", True)
b += text(M4[0] + 12, M4[1] - 4, "M", "currentColor", 15, "start", "700", True)
b += text(O4[0], O4[1] + 24, "O (mốc)", "currentColor", 14, "middle", "700")
b += text(B4[0] - 12, B4[1] + 6, "B", "currentColor", 15, "end", "700", True)
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Lòng chảo của bài toán mẫu: mép A cao 3,2 m, điểm M cao 1,4 m cùng phía, điểm B cao 2,8 m ở thành bên kia, đáy O là mốc thế năng",
            b,
            "Hình 4. Bài toán mẫu: <em>A</em>, <em>M</em>, <em>B</em> cao 3,2; 1,4; 2,8 m so với đáy <em>O</em> (mốc thế năng). Độ cao vẽ đúng tỉ lệ.")
fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-co-nang-bao-toan-03"', 1)


# ---------------- Kiểm toạ độ nhãn ----------------
def seg_hits_box(x1, y1, x2, y2, bx0, by0, bx1, by1):
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
    for g_, a0, b0, a1, b1, t in LABELS[i + 1:]:
        if g_ == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            BAD.append(f"Hình {f}: nhãn '{s}' chồng '{t}'")
    for g_, sx1, sy1, sx2, sy2 in SEGS:
        if g_ == f and seg_hits_box(sx1, sy1, sx2, sy2, x0 + 1, y0 + 1, x1 - 1, y1 - 1):
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
m_ = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout) or re.search(r'"minutes"\s*:\s*([\d.]+)', r.stdout)
phut = round(float(m_.group(1))) if m_ else None
if phut is None:
    print("KHÔNG đọc được số phút từ lint_do_dai:", r.stdout[:300])
    phut = "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut)
sys.exit(1 if BAD else 0)
