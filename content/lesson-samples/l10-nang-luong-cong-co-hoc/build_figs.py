"""Sinh 4 hình SVG cho bài 'Năng lượng. Công cơ học' (lesson 68) và thay mốc <!--FIGn--> trong
theory.src.html -> theory.html. Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Tự kiểm bằng toạ độ: nhãn không chồng nhau, không vượt viewBox, không bị nét vẽ cắt xuyên; góc giữa F và d
tính lại từ toạ độ mũi tên và so dấu cos với nhãn A > 0 / = 0 / < 0; góc dây kéo hình 4 đúng 30°."""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap, chevron  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2)
BAD = []
CUR = {"fig": 0}
VB = {}


def defs(p):
    """Không còn marker tam giác: mũi tên vẽ đầu V 30° bằng chevron (thầy chốt 7/10/2026)."""
    return ""


def seg(x1, y1, x2, y2):
    SEGS.append((CUR["fig"], x1, y1, x2, y2))


def arrow(p, c, x1, y1, x2, y2, w=3, dash=""):
    seg(x1, y1, x2, y2)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    ww = min(w, 2.8)
    L = max(5, min(3.4 * ww + 2, 0.6 * math.hypot(x2 - x1, y2 - y1)))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{ww}"{d}/>'
            + chevron(x2, y2, x2 - x1, y2 - y1, COL[c], ww, L))


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, track=True):
    if track:
        seg(x1, y1, x2, y2)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="14">{s}</tspan>'


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


# ---------------- Hình 1: ảnh OpenStax College Physics 2e, Hình 7.2 (a, c, e) (đợt 1 + đợt 2, 28/10/2026) ----------------
fig1 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l10-nang-luong-cong-co-hoc/hinh-cong-luc-goc.webp" '
        'alt="Ba tình huống: (a) người đẩy máy cắt cỏ bằng lực F chếch góc θ so với độ dịch chuyển d, (c) người xách cặp đi ngang, F vuông góc d, (e) cặp được máy phát điện hạ xuống, lực F hướng lên còn d hướng xuống" '
        'loading="lazy" width="875" height="910">'
        '<figcaption>Hình 1. Ba tình huống về công:<br>'
        '(a) đẩy xe cắt cỏ, như Lan đẩy Hà: <em>F</em>·<em>d</em>·cosθ.<br>'
        '(c) xách cặp đi ngang: θ = 90°, không sinh công.<br>'
        '(e) hạ cặp xuống: <em>F</em> ngược <em>d</em>, công âm.<br>'
        'Nhãn: <em>F</em>: lực.<br>'
        '<em>d</em>: độ dịch chuyển.<br>'
        'θ: góc giữa <em>F</em> và <em>d</em> (trong bài là α).<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 7.2 (a, c, e) — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>'
        '</figcaption></figure>')

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
    if a > 90:   # góc tù: nhãn trên đầu mũi tên, khỏi chạm vạch ngăn cột
        b += text(fx + 8, fy - 10, "F", RED, 16, "middle", "700", True)
    else:
        b += text(fx + (8 if a < 90 else 9), fy + (4 if a != 90 else 10), "F", RED, 16, "start", "700", True)
    b += text(ox + DL - 4, OY + 22, "d", GRN, 16, "middle", "700", True)
    b += text(x0 + 73, 26, title, "currentColor", 14, "middle")
    b += text(x0 + 73, 160, sign, "currentColor", 15, "middle")
    b += text(x0 + 73, 182, name, RED if sgn > 0 else (BLUE if sgn < 0 else "currentColor"), 14, "middle", "600")
for xs in (146, 294):
    b += line(xs, 14, xs, 190, "currentColor", 1, "3 5", .4, track=False)
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Ba trường hợp góc alpha giữa lực F và độ dịch chuyển d: góc nhọn công dương, góc vuông công bằng 0, góc tù công âm", b,
            "Hình 2. Cùng độ dịch chuyển $\\vec d$ (xanh lá), đổi hướng lực $\\vec F$ (đỏ): dấu của $\\cos\\alpha$ quyết định dấu của công.")

# ---------------- Hình 3: thí nghiệm mặt phẳng nghiêng ----------------
CUR["fig"] = 3
VB[3] = (440, 186)
PXM = 360 / 0.80
S3, H3 = 0.80, 0.20
th = math.asin(H3 / S3)
Ax, Ay = 20, 152                      # chân dốc
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
b += text(front[0] + 0.5 * FLEN * u[0] + 14 * nrm[0], front[1] + 0.5 * FLEN * u[1] + 14 * nrm[1], "F", RED, 16, "middle", "700", True)
b += text(ex_ + 50, ey_ - 18, "lực kế", BLUE, 14, "start", "600")   # bên phải thân lực kế, không chạm thân
b += text(Tx + 8, (Ay + Ty) / 2 + 5, "h", "currentColor", 16, "start", "700", True)
b += text(Tx + 8, (Ay + Ty) / 2 + 24, "0,20 m", "currentColor", 14, "start", "600")
# đường kích thước s song song mặt dốc, cách mặt dốc DN px về phía ngoài, vạch hai đầu
DN = 46
d0 = (Ax + DN * nrm[0], Ay + DN * nrm[1])
d1 = (Tx + DN * nrm[0], Ty + DN * nrm[1])
expect(abs(math.dist(d0, d1) - S3 * PXM) < 1e-6, "Hình 3: đoạn đo s phải dài đúng mặt dốc")
b += line(*d0, *d1, "currentColor", 1.3)
for q in (d0, d1):
    b += line(q[0] - 6 * nrm[0], q[1] - 6 * nrm[1], q[0] + 6 * nrm[0], q[1] + 6 * nrm[1], "currentColor", 1.5)
tm = 0.22 * S3 * PXM
b += text(d0[0] + tm * u[0] + 22 * nrm[0], d0[1] + tm * u[1] + 22 * nrm[1], "s = 0,80 m", "currentColor", 14, "middle", "700")
b += text(130, Ay + 24, "xe lăn P = 2,0 N, kéo đều", "currentColor", 14, "start", "600")
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
def limb(pts, w=3.2, c="currentColor"):
    out = ""
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        seg(xa, ya, xb, yb)
        out += (f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{c}" stroke-width="{w}" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
    return out


def head(x, y, r):
    seg(x - r, y - r, x + r, y + r); seg(x - r, y + r, x + r, y - r)
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="currentColor" fill-opacity=".12" '
            f'stroke="currentColor" stroke-width="2.4"/>')


# em nhỏ ngồi trên ván: lưng thẳng, chân duỗi về trước, tay đặt lên gối
b += head(165, G4 - 60, 9)
b += limb([(165, G4 - 50), (161, G4 - 17)], 3.6)                          # thân
b += limb([(161, G4 - 17), (177, G4 - 33), (191, G4 - 17)], 3.2)           # chân: ngồi bó gối
b += limb([(164, G4 - 42), (176, G4 - 33)], 2.6)                           # tay ôm gối
# dây kéo 30°
A30 = math.radians(30)
rope0 = (260, G4 - 10)
RL = 116
rope1 = (rope0[0] + RL * math.cos(A30), rope0[1] - RL * math.sin(A30))
expect(abs(math.degrees(math.atan2(rope0[1] - rope1[1], rope1[0] - rope0[0])) - 30) < 1e-6, "Hình 4: dây phải chếch 30°")
b += line(*rope0, *rope1, "currentColor", 1.4, track=False)
# Lan ngả người ra sau, hai tay kéo dây, chân trước đạp lưỡi trượt
b += limb([(384, G4 - 2), (392, G4 - 28), (402, G4 - 52)], 3.6)            # chân trước
b += limb([(402, G4 - 52), (412, G4 - 28), (418, G4 - 2)], 3.6)            # chân sau
b += limb([(402, G4 - 52), (410, G4 - 92)], 4.2)                           # thân ngả sau
b += limb([(408, G4 - 84), (386, G4 - 76), rope1], 3.0)                    # tay nắm dây
b += head(414, G4 - 105, 11)
b += limb([(372, G4 - 2), (396, G4 - 2)], 3, BLUE) + limb([(406, G4 - 2), (430, G4 - 2)], 3, BLUE)
FL4 = 62
fe = (rope0[0] + FL4 * math.cos(A30), rope0[1] - FL4 * math.sin(A30))
b += arrow("f4", "r", *rope0, *fe, 3)
b += f'<path d="M{rope0[0]+30},{rope0[1]} A30,30 0 0 0 {rope0[0]+30*math.cos(A30):.1f},{rope0[1]-30*math.sin(A30):.1f}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
b += line(rope0[0], rope0[1], rope0[0] + 44, rope0[1], "currentColor", 1.2, "3 3", .7, track=False)
b += text(rope0[0] + 36, rope0[1] - 4, "30°", "currentColor", 14, "start", "600")
b += text(fe[0] - 6, fe[1] - 10, "F", RED, 16, "end", "700", True)
# N (lên), P (xuống) tại giữa ván; ma sát ngược chiều chuyển động
XC = 205                         # tâm ván (x = 150..260)
YC = G4 - 8                      # tâm ván
LN, LP = 280 * 0.2, 300 * 0.2    # 0,2 px/N: N = 280 N ngắn hơn P = 300 N
b += arrow("f4", "b", XC, YC, XC, YC - LN, 3)
b += text(XC + 8, YC - LN + 12, "N", BLUE, 16, "start", "700", True)
b += arrow("f4", "o", XC, YC, XC, YC + LP, 3)
b += text(XC + 8, YC + LP - 4, "P", ORG, 16, "start", "700", True)
b += f'<circle cx="{XC}" cy="{YC}" r="3" fill="currentColor"/>'
b += arrow("f4", "k", 150, YC, 104, YC, 3)        # ma sát ở mặt tiếp xúc, ngược hướng chuyển động
b += text(118, YC - 14, sub("F", "ms"), "currentColor", 16, "middle", "700", True)
# độ dịch chuyển
b += arrow("f4", "g", 262, 210, 372, 210, 2.6, "6 4")
b += text(318, 232, "s = 15 m", GRN, 14, "middle", "600")
b += text(394, 62, "Lan", "currentColor", 14, "end", "600")
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
out.write_text(margin_figs(src.replace("__PHUT__", "?")), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
m = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout) or re.search(r'"minutes"\s*:\s*([\d.]+)', r.stdout)
phut = round(float(m.group(1))) if m else None
if phut is None:
    print("KHÔNG đọc được số phút từ lint_do_dai:", r.stdout[:300])
    phut = "?"
out.write_text(margin_figs(src.replace("__PHUT__", str(phut))), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut)
sys.exit(1 if BAD else 0)
