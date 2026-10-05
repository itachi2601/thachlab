"""Sinh 4 hình SVG cho bài 'Năng lượng. Công cơ học' (lesson 68) và thay mốc <!--FIGn--> trong
theory.src.html -> theory.html. Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Tự kiểm bằng toạ độ: nhãn không chồng nhau, không vượt viewBox, không bị nét vẽ cắt xuyên; góc giữa F và d
tính lại từ toạ độ mũi tên và so dấu cos với nhãn A > 0 / = 0 / < 0; góc dây kéo hình 4 đúng 30°."""
import math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2)
BAD = []
CUR = {"fig": 0}
VB = {}


def defs(p):
    out = "<defs>"
    for n, c in COL.items():
        out += (f'<marker id="{p}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="11" markerHeight="11" '
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
    plain = re.sub(r"<[^>]+>", "", s).replace("&lt;", "<").replace("&gt;", ">")
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.2 * size, plain))
    it = ' font-style="italic" font-family="serif"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{it}>{s}</text>')


def person(x, ground, arm_to=None, track=True):
    """Người que đi giày trượt. Trả (svg, toạ độ vai)."""
    hy, ty, sh = ground - 100, ground - 62, ground - 78
    g = f'<circle cx="{x}" cy="{hy}" r="12" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    g += line(x, hy + 12, x, ty, w=2.5, track=track)
    g += line(x, ty, x - 12, ground - 6, w=2.5, track=track)
    g += line(x, ty, x + 12, ground - 6, w=2.5, track=track)
    g += line(x - 22, ground - 2, x + 22, ground - 2, BLUE, 3, track=track)
    if track:
        seg(x - 12, hy - 12, x + 12, hy + 12); seg(x - 12, hy + 12, x + 12, hy - 12)
    if arm_to is not None:
        g += line(x, sh, arm_to[0], arm_to[1], w=2.5, track=track)
    return g, (x, sh)


def expect(cond, msg):
    if not cond:
        BAD.append(msg)


def angle_between(ux, uy, vx, vy):
    c = (ux * vx + uy * vy) / (math.hypot(ux, uy) * math.hypot(vx, vy))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


# ---------------- Hình 1: hai cảnh ở sân băng (mở bài, không ghi kết luận) ----------------
CUR["fig"] = 1
VB[1] = (440, 230)
G1 = 200
b = defs("f1")
b += line(10, G1, 430, G1, "currentColor", 2, track=False)
b += line(212, 20, 212, G1 - 4, "currentColor", 1.2, "4 5", .45, track=False)
# Trái: Minh ôm ba lô đứng yên
pm, shm = person(70, G1, arm_to=(104, 120))
b += pm
b += f'<rect x="100" y="106" width="34" height="40" rx="6" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2"/>'
seg(100, 106, 134, 106); seg(100, 146, 134, 146); seg(100, 106, 100, 146); seg(134, 106, 134, 146)
b += arrow("f1", "r", 117, 106, 117, 56, 3)          # lực tay lên ba lô, đặt tại ba lô, hướng lên
b += text(126, 66, sub("F", "tay"), RED, 15, "start", "700", True)
b += text(20, 30, "Minh giữ ba lô", "currentColor", 14, "start")
b += text(20, 222, "đứng yên 5 phút", "currentColor", 13, "start", "600")
# Phải: Lan đẩy lưng Hà, Hà lướt sang phải
XH = 330
contact = (XH - 4, G1 - 78)
pl, _ = person(262, G1, arm_to=contact)
ph, _ = person(XH, G1)
b += pl + ph
b += f'<circle cx="{contact[0]}" cy="{contact[1]}" r="3.5" fill="{RED}"/>'
b += arrow("f1", "r", contact[0], contact[1], contact[0] + 52, contact[1], 3)   # lực đẩy đặt tại lưng Hà, chiều sang phải
b += text(contact[0] + 58, contact[1] + 5, "F", RED, 16, "start", "700", True)
b += text(228, 30, "Lan đẩy lưng Hà", "currentColor", 14, "start")
b += arrow("f1", "g", XH - 20, 214, XH + 80, 214, 2.6, "6 4")
b += text(XH - 24, 220, "Hà lướt 3 m", GRN, 13, "end", "600")
b += text(244, 150, "Lan", "currentColor", 13, "end", "600")
b += text(XH + 18, 162, "Hà", "currentColor", 13, "start", "600")
expect(contact[0] + 52 > contact[0], "Hình 1: lực đẩy của Lan phải hướng sang phải (chiều Hà lướt)")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Bên trái Minh đứng yên ôm ba lô, lực tay hướng lên; bên phải Lan đẩy lưng Hà, Hà lướt sang phải 3 m", b,
            "Hình 1. Trái: Minh giữ ba lô đứng yên, lực tay hướng lên. Phải: Lan đẩy lưng Hà, Hà lướt đi $3$ m.")

# ---------------- Hình 2: ba trường hợp góc α ----------------
CUR["fig"] = 2
VB[2] = (440, 200)
b = defs("f2")
DL, FL, OY = 75, 66, 112
cases = [(0, 40, "α nhọn", "A &gt; 0", "phát động", 1),
         (148, 90, "α = 90°", "A = 0", "không sinh công", 0),
         (296, 140, "α tù", "A &lt; 0", "công cản", -1)]
for x0, a, title, sign, name, sgn in cases:
    ox = x0 + 58
    b += f'<circle cx="{ox}" cy="{OY}" r="4" fill="currentColor"/>'
    b += arrow("f2", "g", ox, OY, ox + DL, OY, 3)
    fx, fy = ox + FL * math.cos(math.radians(a)), OY - FL * math.sin(math.radians(a))
    b += arrow("f2", "r", ox, OY, fx, fy, 3)
    ang = angle_between(fx - ox, fy - OY, DL, 0)
    expect(abs(ang - a) < 1e-6, f"Hình 2: góc vẽ {ang:.1f} ≠ {a}")
    c = math.cos(math.radians(ang))
    real = 0 if abs(c) < 1e-9 else (1 if c > 0 else -1)
    expect(real == sgn, f"Hình 2: dấu công ở góc {a}° sai")
    if a == 90:
        k = 11
        b += f'<path d="M{ox+k},{OY} L{ox+k},{OY-k} L{ox},{OY-k}" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        b += text(ox + 16, OY - 18, "α", "currentColor", 15, "start", "700", True)
    else:
        r = 24
        ex, ey = ox + r * math.cos(math.radians(a)), OY - r * math.sin(math.radians(a))
        large = 1 if a > 180 else 0
        b += f'<path d="M{ox+r},{OY} A{r},{r} 0 {large} 0 {ex:.1f},{ey:.1f}" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        hx, hy = ox + 36 * math.cos(math.radians(a / 2)), OY - 36 * math.sin(math.radians(a / 2))
        b += text(hx - 4, hy + 5, "α", "currentColor", 15, "start", "700", True)
    b += text(fx + (8 if a < 90 else (-8 if a > 90 else 9)), fy + (4 if a != 90 else 10), "F", RED, 16,
              "start" if a <= 90 else "end", "700", True)
    b += text(ox + DL - 4, OY + 22, "d", GRN, 16, "middle", "700", True)
    b += text(x0 + 73, 26, title, "currentColor", 14, "middle")
    b += text(x0 + 73, 160, sign, "currentColor", 15, "middle")
    b += text(x0 + 73, 182, name, RED if sgn > 0 else (BLUE if sgn < 0 else "currentColor"), 13, "middle", "600")
for xs in (146, 294):
    b += line(xs, 14, xs, 190, "currentColor", 1, "3 5", .4, track=False)
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Ba trường hợp góc alpha giữa lực F và độ dịch chuyển d: góc nhọn công dương, góc vuông công bằng 0, góc tù công âm", b,
            "Hình 2. Cùng độ dịch chuyển $\\vec d$ (xanh lá), đổi hướng lực $\\vec F$ (đỏ): dấu của $\\cos\\alpha$ quyết định dấu của công.")

# ---------------- Hình 3: thí nghiệm mặt phẳng nghiêng ----------------
CUR["fig"] = 3
VB[3] = (440, 230)
PXM = 360 / 0.80
S3, H3 = 0.80, 0.20
th = math.asin(H3 / S3)
Ax, Ay = 20, 196                      # chân dốc
Tx, Ty = Ax + S3 * PXM * math.cos(th), Ay - S3 * PXM * math.sin(th)
expect(abs((Ay - Ty) / PXM - H3) < 1e-9, "Hình 3: chiều cao h sai tỉ lệ")
b = defs("f3")
b += (f'<path d="M{Ax},{Ay} L{Tx:.1f},{Ay} L{Tx:.1f},{Ty:.1f} Z" fill="rgba(148,163,184,.15)" '
      f'stroke="currentColor" stroke-width="2"/>')
seg(Ax, Ay, Tx, Ty); seg(Ax, Ay, Tx, Ay); seg(Tx, Ay, Tx, Ty)
u = (math.cos(th), -math.sin(th))
nrm = (-math.sin(th), -math.cos(th))   # pháp tuyến hướng lên khỏi mặt dốc
# xe lăn ở 40 % dốc
t0 = 0.40 * S3 * PXM
cx, cy = Ax + t0 * u[0], Ay + t0 * u[1]
deg = -math.degrees(th)
b += (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({deg:.2f})">'
      f'<rect x="-26" y="-26" width="52" height="18" rx="3" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2"/>'
      f'<circle cx="-15" cy="-4" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/>'
      f'<circle cx="15" cy="-4" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/></g>')
front = (cx + 26 * u[0] + 17 * nrm[0], cy + 26 * u[1] + 17 * nrm[1])   # đầu xe, chỗ móc dây
# dây + lực kế song song dốc
t1 = 0.78 * S3 * PXM
ex_, ey_ = Ax + t1 * u[0] + 17 * nrm[0], Ay + t1 * u[1] + 17 * nrm[1]
b += line(front[0], front[1], ex_, ey_, "currentColor", 1.4, track=False)
b += (f'<g transform="translate({ex_:.1f},{ey_:.1f}) rotate({deg:.2f})">'
      f'<rect x="0" y="-7" width="46" height="14" rx="4" fill="rgba(56,189,248,.18)" stroke="currentColor" stroke-width="2"/></g>')
FLEN = 48
b += arrow("f3", "r", front[0], front[1], front[0] + FLEN * u[0], front[1] + FLEN * u[1], 3)
ang = angle_between(FLEN * u[0], FLEN * u[1], u[0], u[1])
expect(abs(ang) < 1e-6, "Hình 3: lực kéo phải song song mặt dốc (α = 0)")
b += text(front[0] + 18, front[1] - 26, "F", RED, 16, "start", "700", True)
b += text(ex_ - 8, ey_ - 18, "lực kế", BLUE, 13, "start", "600")
b += text(Tx + 8, (Ay + Ty) / 2 + 5, "h", "currentColor", 16, "start", "700", True)
b += text(Tx + 8, (Ay + Ty) / 2 + 24, "0,20 m", "currentColor", 13, "start", "600")
mx, my = Ax + 0.16 * S3 * PXM * u[0], Ay + 0.16 * S3 * PXM * u[1]
b += text(mx - 6, my - 14, "s", "currentColor", 16, "end", "700", True)
b += text(130, 220, "xe lăn P = 2,0 N, kéo đều", "currentColor", 13, "start", "600")
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Xe lăn được kéo đều lên mặt nghiêng bằng lực kế, lực kéo song song mặt dốc; độ cao h bằng 0,20 m", b,
            "Hình 3. Kéo đều xe lên độ cao $h$ bằng lực kế song song mặt nghiêng dài $s$ (hình vẽ lần $s = 0{,}80$ m).")
fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-nang-luong-cong-02"', 1)

# ---------------- Hình 4: bài toán mẫu — kéo ván trượt ----------------
CUR["fig"] = 4
VB[4] = (440, 240)
G4 = 172
b = defs("f4")
b += line(10, G4, 430, G4, "currentColor", 2, track=False)
b += f'<rect x="150" y="{G4-14}" width="110" height="12" rx="5" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2"/>'
seg(150, G4 - 14, 260, G4 - 14); seg(150, G4 - 2, 260, G4 - 2)
# em nhỏ ngồi trên ván
b += f'<circle cx="176" cy="{G4-56}" r="9" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += line(176, G4 - 47, 176, G4 - 22, w=2.2) + line(176, G4 - 22, 198, G4 - 16, w=2.2)
# dây kéo 30°
A30 = math.radians(30)
rope0 = (260, G4 - 10)
RL = 116
rope1 = (rope0[0] + RL * math.cos(A30), rope0[1] - RL * math.sin(A30))
expect(abs(math.degrees(math.atan2(rope0[1] - rope1[1], rope1[0] - rope0[0])) - 30) < 1e-6, "Hình 4: dây phải chếch 30°")
b += line(*rope0, *rope1, "currentColor", 1.4, track=False)
pl, _ = person(398, G4, arm_to=rope1)
b += pl
FL4 = 62
fe = (rope0[0] + FL4 * math.cos(A30), rope0[1] - FL4 * math.sin(A30))
b += arrow("f4", "r", *rope0, *fe, 3)
b += f'<path d="M{rope0[0]+30},{rope0[1]} A30,30 0 0 0 {rope0[0]+30*math.cos(A30):.1f},{rope0[1]-30*math.sin(A30):.1f}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
b += line(rope0[0], rope0[1], rope0[0] + 44, rope0[1], "currentColor", 1.2, "3 3", .7, track=False)
b += text(rope0[0] + 36, rope0[1] - 4, "30°", "currentColor", 13, "start", "600")
b += text(fe[0] - 6, fe[1] - 10, "F", RED, 16, "end", "700", True)
# N (lên), P (xuống) tại giữa ván; ma sát ngược chiều chuyển động
XC = 218
YC = G4 - 8                      # tâm ván
LN, LP = 280 * 0.2, 300 * 0.2    # 0,2 px/N: N = 280 N ngắn hơn P = 300 N
b += arrow("f4", "b", XC, YC, XC, YC - LN, 3)
b += text(XC + 8, YC - LN + 12, "N", BLUE, 16, "start", "700", True)
b += arrow("f4", "o", XC, YC, XC, YC + LP, 3)
b += text(XC + 8, YC + LP - 4, "P", ORG, 16, "start", "700", True)
b += f'<circle cx="{XC}" cy="{YC}" r="3" fill="currentColor"/>'
b += arrow("f4", "k", 160, G4 - 1, 122, G4 - 1, 3)
b += text(116, G4 - 16, sub("F", "ms"), "currentColor", 15, "end", "700", True)
# độ dịch chuyển
b += arrow("f4", "g", 262, 210, 372, 210, 2.6, "6 4")
b += text(318, 232, "s = 15 m", GRN, 13, "middle", "600")
b += text(398, 52, "Lan", "currentColor", 13, "middle", "600")
expect(YC - LN > 10 and YC + LP < VB[4][1] - 4, "Hình 4: N/P vượt viewBox")
expect(LN < LP and abs(LN / LP - 280 / 300) < 1e-9, "Hình 4: N phải ngắn hơn P theo tỉ lệ 280/300")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Lan kéo ván trượt bằng dây chếch lên 30 độ; các lực lên ván: lực kéo F, trọng lực P, phản lực N, ma sát hướng ngược chiều chuyển động", b,
            "Hình 4. Các lực lên ván: $\\vec F$ chếch lên $30^\\circ$, $\\vec P$, $\\vec N$ và $\\vec F_{ms}$ ngược hướng chuyển động. $\\vec N$ ngắn hơn $\\vec P$ đúng tỉ lệ; $\\vec F$, $\\vec F_{ms}$ không theo tỉ lệ.")
fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-nang-luong-cong-03"', 1)


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
