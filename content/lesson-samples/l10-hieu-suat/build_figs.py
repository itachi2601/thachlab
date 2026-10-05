"""Sinh 4 hình SVG cho bài 'Bài 27. Hiệu suất' (lesson 72) và thay mốc <!--FIGn--> trong
theory.src.html -> theory.html. Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Tự kiểm bằng toạ độ: nhãn không chồng nhau, không vượt viewBox, không bị nét vẽ cắt xuyên; cánh tay đòn tính lại
bằng khoảng cách vuông góc từ trục tới đường tác dụng; chiều quay suy từ dấu moment (r × F)."""
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
SEGV = []


def poly_h(c, x1, x2, yc, th, label_fig=True):
    th = max(th, 2.2)
    """Mũi tên khối nằm ngang: thân dày th, đầu tam giác."""
    hl, hw = 18, th / 2 + 6
    pts = [(x1, yc - th / 2), (x2 - hl, yc - th / 2), (x2 - hl, yc - hw), (x2, yc), (x2 - hl, yc + hw), (x2 - hl, yc + th / 2), (x1, yc + th / 2)]
    seg(x1, yc - hw, x2, yc - hw); seg(x1, yc + hw, x2, yc + hw)
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{COL[c]}" opacity=".85"/>'


def poly_v(c, xc, y1, y2, th):
    th = max(th, 2.2)
    hl, hw = 18, th / 2 + 6
    pts = [(xc - th / 2, y1), (xc - th / 2, y2 - hl), (xc - hw, y2 - hl), (xc, y2), (xc + hw, y2 - hl), (xc + th / 2, y2 - hl), (xc + th / 2, y1)]
    seg(xc - hw, y1, xc - hw, y2); seg(xc + hw, y1, xc + hw, y2)
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{COL[c]}" opacity=".85"/>'


# ---------------- Hình 1: hai bóng đèn (mở bài) ----------------
CUR["fig"] = 1
VB[1] = (440, 190)
b = ""
for cx, lab in ((100, "Sợi đốt · 60 W"), (340, "LED · 9 W")):
    cy, r = 70, 36
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2.4"/>'
    b += f'<rect x="{cx-14}" y="{cy+r-4}" width="28" height="24" rx="3" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2.2"/>'
    b += line(cx - 14, cy + r + 8, cx + 14, cy + r + 8, "currentColor", 1.6, track=False)
    b += line(cx - 10, cy + r + 24, cx + 10, cy + r + 24, "currentColor", 3, track=False)
    for ang in (-180, -150, -120, -90, -60, -30, 0):
        x0, y0 = cx + 46 * math.cos(math.radians(ang)), cy + 46 * math.sin(math.radians(ang))
        x1, y1 = cx + 58 * math.cos(math.radians(ang)), cy + 58 * math.sin(math.radians(ang))
        b += line(x0, y0, x1, y1, ORG, 2.4)
    b += text(cx, 168, lab, "currentColor", 14, "middle")
b += text(220, 76, "cùng độ sáng", "currentColor", 14, "middle", "600")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Hai bóng đèn cùng độ sáng: bóng sợi đốt ghi 60 W và bóng LED ghi 9 W", b,
            "Hình 1. Hai bóng đèn sáng ngang nhau nhưng công suất ghi trên bóng khác nhau.")

# ---------------- Hình 2: sơ đồ năng lượng (minh hoạ 100 J = 80 J + 20 J) ----------------
CUR["fig"] = 2
VB[2] = (440, 225)
WT, WC, WH = 100, 80, 20
expect(WT == WC + WH, "Hình 2: W_tp = W_ci + W_hp")
K = 0.2                                  # px bề dày mỗi J
b = ""
b += f'<rect x="150" y="62" width="140" height="80" rx="8" fill="rgba(148,163,184,.2)" stroke="currentColor" stroke-width="2.4"/>'
seg(150, 62, 290, 62); seg(150, 142, 290, 142); seg(150, 62, 150, 142); seg(290, 62, 290, 142)
b += text(220, 108, "Máy", "currentColor", 16, "middle")
b += poly_h("o", 14, 148, 102, WT * K)
b += poly_h("g", 292, 426, 102, WC * K)
b += poly_v("r", 220, 144, 200, WH * K)
b += text(14, 76, sub("W", "tp") + " = 100 J", ORG, 14, "start")
b += text(296, 78, sub("W", "ci") + " = 80 J", GRN, 14, "start")
b += text(236, 172, sub("W", "hp") + " = 20 J", RED, 14, "start")
b += text(236, 192, "nhiệt · âm · rung", RED, 13, "start", "600")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Sơ đồ năng lượng qua một máy: 100 J đi vào, 80 J có ích đi ra, 20 J hao phí", b,
            "Hình 2. Bề dày mũi tên tỉ lệ với năng lượng (số liệu minh hoạ): vào $100$ J, ra có ích $80$ J, hao phí $20$ J.".replace("$100$ J", "100 J").replace("$80$ J", "80 J").replace("$20$ J", "20 J"))

# ---------------- Hình 3: ván nghiêng (lần đo 35°) ----------------
CUR["fig"] = 3
VB[3] = (440, 250)
SC = 7.5                                  # px/cm
ALPHA3, H3 = 35, 20.0
S3 = 34.9
expect(abs(S3 * math.sin(math.radians(ALPHA3)) - H3) < 0.1, "Hình 3: s·sinα ≈ h")
Ax, Ay = 40, 218
Bx, By = Ax + S3 * math.cos(math.radians(ALPHA3)) * SC, Ay
Cx, Cy = Bx, Ay - H3 * SC
u = (math.cos(math.radians(ALPHA3)), -math.sin(math.radians(ALPHA3)))
n = (-math.sin(math.radians(ALPHA3)), -math.cos(math.radians(ALPHA3)))   # pháp tuyến hướng lên-trái, ra khỏi ván
expect(abs(Cy - (Ay - (Cx - Ax) * math.tan(math.radians(ALPHA3)))) < 1.0, "Hình 3: đỉnh ván đúng góc α")
b = defs("f3")
b += f'<polygon points="{Ax},{Ay} {Bx:.1f},{By} {Cx:.1f},{Cy:.1f}" fill="rgba(148,163,184,.14)" stroke="currentColor" stroke-width="2.4"/>'
seg(Ax, Ay, Bx, By); seg(Bx, By, Cx, Cy); seg(Ax, Ay, Cx, Cy)
t0 = 0.5
C0 = (Ax + t0 * (Cx - Ax), Ay + t0 * (Cy - Ay))
W_, H_ = 44, 24
ctr = (C0[0] + n[0] * H_ / 2, C0[1] + n[1] * H_ / 2)
corners = [(C0[0] - u[0] * W_ / 2, C0[1] - u[1] * W_ / 2), (C0[0] + u[0] * W_ / 2, C0[1] + u[1] * W_ / 2)]
corners += [(corners[1][0] + n[0] * H_, corners[1][1] + n[1] * H_), (corners[0][0] + n[0] * H_, corners[0][1] + n[1] * H_)]
b += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in corners)}" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2.2"/>'
PXN = 16                                  # px/N
F3, MG3, MU3 = 3.13, 4.0, 0.25
f3 = MU3 * MG3 * math.cos(math.radians(ALPHA3))
expect(abs(F3 - (MG3 * math.sin(math.radians(ALPHA3)) + f3)) < 0.05, "Hình 3: F ≈ mg sinα + f")
b += arrow("f3", "r", ctr[0], ctr[1], ctr[0] + u[0] * F3 * PXN, ctr[1] + u[1] * F3 * PXN, 3.2)
b += arrow("f3", "b", C0[0] + u[0] * 14, C0[1] + u[1] * 14, C0[0] + u[0] * 14 - u[0] * f3 * PXN, C0[1] + u[1] * 14 - u[1] * f3 * PXN, 3.2)
b += arrow("f3", "o", ctr[0], ctr[1], ctr[0], ctr[1] + MG3 * PXN, 3.2)
b += text(ctr[0] + u[0] * F3 * PXN + 8, ctr[1] + u[1] * F3 * PXN - 4, "F", RED, 16, "start", "700", True)
b += text(ctr[0] + 8, ctr[1] + MG3 * PXN + 6, "mg", ORG, 15, "start", "700", True)
b += text(C0[0] + 12, C0[1] + 18, "ma sát", BLUE, 13, "start", "600")
# kích thước h
xh = Bx + 24
b += line(xh, Ay, xh, Cy, GRN, 2) + line(xh - 6, Ay, xh + 6, Ay, GRN, 2) + line(xh - 6, Cy, xh + 6, Cy, GRN, 2)
b += text(xh + 10, (Ay + Cy) / 2 + 5, "h = 20 cm", GRN, 14, "start")
OFF = 28
Ap, Cp = (Ax + OFF * n[0], Ay + OFF * n[1]), (Cx + OFF * n[0], Cy + OFF * n[1])
b += line(*Ap, *Cp, "currentColor", 1.6)
for P_ in (Ap, Cp):
    b += line(P_[0] - 6 * n[0], P_[1] - 6 * n[1], P_[0] + 6 * n[0], P_[1] + 6 * n[1], "currentColor", 1.6)
Mp = ((Ap[0] + Cp[0]) / 2, (Ap[1] + Cp[1]) / 2)
b += text(Mp[0] - 12, Mp[1] - 6, "s = 34,9 cm", "currentColor", 14, "end")
b += f'<path d="M{Ax+46:.1f},{Ay:.1f} A46,46 0 0 0 {Ax+46*u[0]:.1f},{Ay+46*u[1]:.1f}" fill="none" stroke="currentColor" stroke-width="1.6"/>'
b += text(Ax + 52, Ay - 6, "α", "currentColor", 16, "start", "700", True)
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Xe gỗ được kéo đều lên ván nghiêng góc 35 độ; lực kéo F song song ván, ma sát hướng xuống dọc ván, trọng lượng mg hướng thẳng xuống, độ cao h = 20 cm", b,
            "Hình 3. Lần đo <em>α</em> = 35°: lực kéo <em>F</em> (đỏ) dọc ván, ma sát (xanh) ngược chiều chuyển động, trọng lượng <em>mg</em> (cam) thẳng đứng. Mũi tên vẽ tỉ lệ độ lớn lực.")
fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-hieu-suat-02"', 1)

# ---------------- Hình 4: xe máy — hai khâu nối tiếp ----------------
CUR["fig"] = 4
VB[4] = (440, 215)
H1, H2 = 0.30, 0.90
E0, E1, E2 = 100, 100 * H1, 100 * H1 * H2
expect(abs(E1 - 30) < 1e-9 and abs(E2 - 27) < 1e-9, "Hình 4: 100 → 30 → 27")
b = defs("f4")
K4 = 0.1
b += poly_h("o", 6, 60, 80, E0 * K4)
b += poly_h("g", 160, 222, 80, E1 * K4)
b += poly_h("g", 322, 434, 80, E2 * K4)
for x0, x1, l1, l2 in ((60, 160, "Động cơ", sub("H", "1") + " = 30%"), (222, 322, "Truyền động", sub("H", "2") + " = 90%")):
    b += f'<rect x="{x0}" y="50" width="{x1-x0}" height="60" rx="8" fill="rgba(148,163,184,.2)" stroke="currentColor" stroke-width="2.2"/>'
    seg(x0, 50, x1, 50); seg(x0, 110, x1, 110); seg(x0, 50, x0, 110); seg(x1, 50, x1, 110)
    b += text((x0 + x1) / 2, 76, l1, "currentColor", 14, "middle")
    b += text((x0 + x1) / 2, 98, l2, "currentColor", 14, "middle")
b += poly_v("r", 110, 112, 152, (E0 - E1) * K4)
b += poly_v("r", 272, 112, 152, (E1 - E2) * K4)
b += text(6, 62, "100 kJ", ORG, 14, "start")
b += text(191, 62, "30 kJ", GRN, 14, "middle")
b += text(378, 62, "27 kJ", GRN, 14, "middle")
b += text(126, 140, "70 kJ hao phí", RED, 14, "start")
b += text(288, 140, "3 kJ hao phí", RED, 14, "start")
b += text(220, 192, "H = 0,30 · 0,90 = 27%", GRN, 15, "middle")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Xe máy: động cơ hiệu suất 30%, bộ truyền động hiệu suất 90%; từ 100 kJ năng lượng xăng chỉ còn 27 kJ tới bánh xe", b,
            "Hình 4. Hai khâu nối tiếp (số liệu minh hoạ): 100 kJ → 30 kJ → 27 kJ. Bề dày mũi tên tỉ lệ năng lượng (mũi tên 3 kJ vẽ dày tối thiểu cho dễ thấy). Mỗi khâu lấy đi thêm một phần hao phí.")
fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-hieu-suat-03"', 1)

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
