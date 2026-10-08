"""Sinh 4 hình SVG cho bài 'Tổng hợp và phân tích lực. Cân bằng lực' và thay mốc <!--FIGn--> trong theory.src.html -> theory.html."""
import math
from svg_lib import *

_COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}
def arrow(p, c, x1, y1, x2, y2, w=3, dash=""):
    """Vectơ lực theo quy ước đầu V nhọn (hai vạch lệch 30°), không dùng marker: thân mảnh + đầu chevron."""
    col = _COL[c]
    w = min(w, 2.8)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    n = math.hypot(x2 - x1, y2 - y1) or 1
    L = min(12, n * 0.45)
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"{d}/>'
            + chevron(x2, y2, x2 - x1, y2 - y1, col, w, L))

def P(x, y): return f"{x:.1f},{y:.1f}"
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def dot(x, y, r=4, c="currentColor"): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
def vec(p, c, x, y, ang, L, w=3, dash=""):
    """Mũi tên từ (x,y), góc ang (độ, ngược chiều kim đồng hồ, trục y hướng lên), dài L; trả (chuỗi, đầu mút)."""
    a = math.radians(ang); x2, y2 = x + L * math.cos(a), y - L * math.sin(a)
    return arrow(p, c, x, y, round(x2, 1), round(y2, 1), w, dash), (x2, y2)
def sub(base, s): return f'{base}<tspan dy="4" font-size="11">{s}</tspan>'
def arc(x, y, r, a1, a2, c="currentColor", w=1.5):
    p1 = (x + r * math.cos(math.radians(a1)), y - r * math.sin(math.radians(a1)))
    p2 = (x + r * math.cos(math.radians(a2)), y - r * math.sin(math.radians(a2)))
    sweep = 0 if a2 > a1 else 1
    return f'<path d="M{P(*p1)} A{r},{r} 0 0 {sweep} {P(*p2)}" fill="none" stroke="{c}" stroke-width="{w}"/>'

# ---- Hình 1: quy tắc hình bình hành
ox, oy = 90, 190
a1, a2 = 15, 85              # hướng F1, F2 (alpha = 70 độ)
L1, L2 = 190, 120
x1, y1 = ox + L1 * math.cos(math.radians(a1)), oy - L1 * math.sin(math.radians(a1))
x2, y2 = ox + L2 * math.cos(math.radians(a2)), oy - L2 * math.sin(math.radians(a2))
xf, yf = x1 + x2 - ox, y1 + y2 - oy
b = defs("f1")
b += line(x1, y1, xf, yf, "currentColor", 1.5, "5 4", .6) + line(x2, y2, xf, yf, "currentColor", 1.5, "5 4", .6)
b += arrow("f1", "r", ox, oy, round(x1, 1), round(y1, 1), 3.2) + arrow("f1", "b", ox, oy, round(x2, 1), round(y2, 1), 3.2)
b += arrow("f1", "g", ox, oy, round(xf, 1), round(yf, 1), 3.6)
b += arc(ox, oy, 46, a1, a2, "currentColor") + text(ox + 26, oy - 44, "α", "currentColor", 14, "start", "700")
fa = math.degrees(math.atan2(oy - yf, xf - ox))
b += arc(ox, oy, 78, a1, fa, GRN) + text(ox + 82, oy - 40, "θ", GRN, 14, "start", "700")
b += text(x1 - 34, y1 + 30, sub("F", "1"), RED, 15, "end", "700")
b += text(x2 - 10, y2 + 4, sub("F", "2"), BLUE, 15, "end", "700")
b += text(xf + 10, yf + 8, "F", GRN, 16, "start", "700")
b += dot(ox, oy, 4)
b += text(ox - 6, oy + 18, "O", "currentColor", 14, "end", "600")
fig1 = wrap("0 0 440 220", "Quy tắc hình bình hành: hai lực F1, F2 hợp nhau góc alpha, đường chéo là hợp lực F",
            b, "Hình 1. Quy tắc hình bình hành: đường chéo xuất phát từ O (xanh lá) là hợp lực <em>F</em>; α là góc giữa hai lực.")

# ---- Hình 2: phân tích lực khi kéo vali / xe
gx = 70                       # mặt đất
b = defs("f2")
b += line(20, 190, 420, 190, "currentColor", 2, "", .7)
b += f'<rect x="{gx+10}" y="146" width="96" height="44" rx="4" fill="rgba(148,163,184,.2)" stroke="currentColor" stroke-width="2.4"/>'
b += f'<circle cx="{gx+30}" cy="192" r="6" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="{gx+88}" cy="192" r="6" fill="none" stroke="currentColor" stroke-width="2"/>'
hx, hy = gx + 106, 160        # điểm đặt lực (tay kéo)
alpha = 40
s, (ex, ey) = vec("f2", "r", hx, hy, alpha, 140, 3.4)
b += s
b += line(ex, hy, ex, ey, "currentColor", 1.5, "5 4", .6) + line(hx, ey, ex, ey, "currentColor", 1.5, "5 4", .6)
b += arrow("f2", "g", hx, hy, round(ex, 1), hy, 3)
b += arrow("f2", "o", hx, hy, hx, round(ey, 1), 3)
b += arc(hx, hy, 52, 0, alpha, "currentColor") + text(hx + 56, hy - 8, "α", "currentColor", 14, "start", "700")
b += text((hx + ex) / 2 - 12, (hy + ey) / 2 - 8, "F", RED, 16, "end", "700")
b += text(hx + 8, hy + 22, sub("F", "x") + " = F cos α", GRN, 14, "start", "700")
b += text(hx - 8, (hy + ey) / 2 + 4, sub("F", "y") + " = F sin α", ORG, 14, "end", "700")
fig2 = wrap("0 0 440 220", "Phân tích lực kéo F của tay thành thành phần nằm ngang Fx và thẳng đứng Fy",
            b, "Hình 2. Lực kéo nghiêng <em>F</em> phân tích thành <em>F<sub>x</sub></em> (làm xe chạy) và <em>F<sub>y</sub></em> (nhấc bớt xe lên); α là góc với phương ngang.")

# ---- Hình 3: mặt phẳng nghiêng
al = 30
bx, by = 40, 200               # chân dốc
Ls = 340
tx, ty = bx + Ls * math.cos(math.radians(al)), by - Ls * math.sin(math.radians(al))
b = defs("f3")
b += f'<polygon points="{P(bx,by)} {P(tx,ty)} {P(tx,by)}" fill="rgba(148,163,184,.12)" stroke="currentColor" stroke-width="2.4"/>'
# khối đặt trên dốc ở khoảng giữa
u = (math.cos(math.radians(al)), -math.sin(math.radians(al)))      # vector đơn vị dọc dốc (hướng lên)
nvec = (math.sin(math.radians(al)), math.cos(math.radians(al)))    # pháp tuyến ra ngoài (lên-trái? -> lên-phải)
nvec = (-math.sin(math.radians(al)), -math.cos(math.radians(al)))  # lên trên-trái (y hướng xuống màn hình = âm)
cx0, cy0 = bx + 205 * u[0], by + 205 * u[1]
hw, hh = 34, 24
pts = [(cx0 - hw*u[0], cy0 - hw*u[1]), (cx0 + hw*u[0], cy0 + hw*u[1]),
       (cx0 + hw*u[0] + hh*nvec[0], cy0 + hw*u[1] + hh*nvec[1]), (cx0 - hw*u[0] + hh*nvec[0], cy0 - hw*u[1] + hh*nvec[1])]
b += f'<polygon points="{" ".join(P(*p) for p in pts)}" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2.4"/>'
gx0, gy0 = cx0 + 12 * nvec[0], cy0 + 12 * nvec[1]       # trọng tâm
b += dot(gx0, gy0, 3.5)
Lp = 96
_px_t = (gx0 - Lp * math.sin(math.radians(al)) * math.cos(math.radians(al)), gy0 + Lp * math.sin(math.radians(al)) * math.sin(math.radians(al)))
_py_t = (gx0 + Lp * math.cos(math.radians(al)) * math.sin(math.radians(al)), gy0 + Lp * math.cos(math.radians(al)) * math.cos(math.radians(al)))
b += line(_px_t[0], _px_t[1], gx0, gy0 + Lp, "currentColor", 1.5, "5 4", .6) + line(_py_t[0], _py_t[1], gx0, gy0 + Lp, "currentColor", 1.5, "5 4", .6)
b += arrow("f3", "r", round(gx0, 1), round(gy0, 1), round(gx0, 1), round(gy0 + Lp, 1), 3.4)               # P thẳng đứng xuống
px, pyy = Lp * math.sin(math.radians(al)), Lp * math.cos(math.radians(al))
b += arrow("f3", "g", round(gx0, 1), round(gy0, 1), round(gx0 - px * math.cos(math.radians(al)), 1), round(gy0 + px * math.sin(math.radians(al)), 1), 3)   # Px dọc dốc xuống
b += arrow("f3", "o", round(gx0, 1), round(gy0, 1), round(gx0 + pyy * math.sin(math.radians(al)), 1), round(gy0 + pyy * math.cos(math.radians(al)), 1), 3)   # Py vuông góc, vào dốc
b += text(gx0 + 10, gy0 + Lp + 4, "P", RED, 16, "start", "700")
b += text(gx0 - px * math.cos(math.radians(al)) - 4, gy0 + px * math.sin(math.radians(al)) - 18, sub("P", "x") + " = P sin α", GRN, 14, "end", "700")
b += text(gx0 + pyy * math.sin(math.radians(al)) + 10, gy0 + pyy * math.cos(math.radians(al)) - 4, sub("P", "y"), ORG, 14, "start", "700") + text(gx0 + pyy * math.sin(math.radians(al)) + 10, gy0 + pyy * math.cos(math.radians(al)) + 12, "= P cos α", ORG, 14, "start", "700")
b += arc(bx, by, 70, 0, al, "currentColor") + text(bx + 78, by - 8, "α", "currentColor", 14, "start", "700")
fig3 = wrap("0 0 440 232", "Vật trên mặt phẳng nghiêng góc alpha: trọng lực P phân tích thành Px dọc dốc và Py vuông góc dốc",
            b, "Hình 3. Trên dốc nghiêng góc α, trọng lực <em>P</em> phân tích thành <em>P<sub>x</sub></em> = <em>P</em> sin α (dọc dốc) và <em>P<sub>y</sub></em> = <em>P</em> cos α (ép vào dốc).")

# ---- Hình 4: đèn treo bằng hai dây
half = 30
ox, oy = 220, 160              # chỗ buộc dây
L = 100
b = defs("f4")
b += line(60, 22, 380, 22, "currentColor", 3, "", 1)
for k in range(10):
    b += line(64 + k * 34, 22, 56 + k * 34, 12, "currentColor", 1.6, "", .5)
ax, ay = ox - L * math.sin(math.radians(half)) * 1.6, 22
bx2 = ox + L * math.sin(math.radians(half)) * 1.6
b += line(ax, 22, ox, oy, "currentColor", 1.8, "", .6) + line(bx2, 22, ox, oy, "currentColor", 1.8, "", .6)
# vectơ lực tại O
dx, dy = ox - ax, oy - 22
nrm = math.hypot(dx, dy)
Tl = 62
b += arrow("f4", "r", ox, oy, round(ox - dx / nrm * Tl, 1), round(oy - dy / nrm * Tl, 1), 3.2)
b += arrow("f4", "b", ox, oy, round(ox + dx / nrm * Tl, 1), round(oy - dy / nrm * Tl, 1), 3.2)
b += arrow("f4", "o", ox, oy, ox, oy + 74, 3.4)
Fy = 2 * (dy / nrm) * Tl
b += arrow("f4", "g", ox, oy, ox, round(oy - Fy, 1), 3.2, "6 4")
b += line(ox - dx / nrm * Tl, oy - dy / nrm * Tl, ox, oy - Fy, "currentColor", 1.4, "5 4", .55)
b += line(ox + dx / nrm * Tl, oy - dy / nrm * Tl, ox, oy - Fy, "currentColor", 1.4, "5 4", .55)
b += dot(ox, oy, 4.5)
b += f'<path d="M{ox-20},{oy+98} L{ox+20},{oy+98} L{ox+14},{oy+132} L{ox-14},{oy+132} Z" fill="rgba(251,146,60,.2)" stroke="currentColor" stroke-width="2.2"/>' + line(ox, oy + 74, ox, oy + 98, "currentColor", 1.6)
b += text(ox - dx / nrm * Tl - 14, oy - dy / nrm * Tl + 18, sub("T", "1"), RED, 15, "end", "700")
b += text(ox + dx / nrm * Tl + 14, oy - dy / nrm * Tl + 18, sub("T", "2"), BLUE, 15, "start", "700")
b += text(ox + 10, oy + 66, "P", ORG, 16, "start", "700")
b += text(ox, oy - Fy - 12, sub("F", "12") + " = P", GRN, 14, "middle", "700")
b += arc(ox, oy, 44, 90 - half, 90 + half, "currentColor") + text(ox, oy - 28, "α", "currentColor", 14, "middle", "700")
fig4 = wrap("0 0 440 304", "Đèn treo bằng hai dây: hai lực căng T1, T2 có hợp lực F12 cân bằng với trọng lực P",
            b, "Hình 4. Đèn đứng yên: hợp lực <em>F</em><sub>12</sub> của hai lực căng <em>T</em><sub>1</sub>, <em>T</em><sub>2</sub> cân bằng với trọng lực <em>P</em>; α là góc giữa hai dây.")

fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-tonghopluc-03"', 1)

def _chips(name, cls, angles, checked):
    row = f'<div class="tl-sim__row"><b>{name}</b>'
    for a in angles:
        cid = f"tl58-{cls}{a}"
        on = " checked" if a == checked else ""
        row += f'<input type="radio" name="tl58-{cls}" class="{cls}-a{a}" id="{cid}"{on}>'
        row += f'<label for="{cid}" class="tl-sim__chip">{a}°</label>'
    return row + "</div>\n"

def sim_keo():
    """Nhìn từ trên xuống: F1, F2 vẽ từ xe; hai nét đứt khép thành hình bình hành; đường chéo là hợp lực F."""
    parts = []
    ox, oy, sc = 210, 206, 0.8
    for alpha, F in ((0, 200), (60, 173), (90, 141), (120, 100), (180, 0)):
        h = math.radians(alpha / 2)
        nud = 7 if alpha == 0 else 0
        t1 = (ox - 100 * sc * math.sin(h) - nud, oy - 100 * sc * math.cos(h))
        t2 = (ox + 100 * sc * math.sin(h) + nud, oy - 100 * sc * math.cos(h))
        tf = (ox, oy - F * sc)
        b = defs(f"k{alpha}")
        b += '<rect x="14" y="10" width="392" height="236" rx="12" fill="rgba(56,189,248,.08)" stroke="currentColor" stroke-width="1.4"/>'
        if 0 < alpha < 180:
            b += line(t1[0], t1[1], tf[0], tf[1], "currentColor", 1.6, "5 4", .6)
            b += line(t2[0], t2[1], tf[0], tf[1], "currentColor", 1.6, "5 4", .6)
        b += f'<rect x="{ox-28}" y="{oy}" width="56" height="30" rx="6" fill="rgba(251,146,60,.22)" stroke="currentColor" stroke-width="2.4"/>'
        b += f'<circle cx="{ox-16}" cy="{oy+34}" r="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="{ox+16}" cy="{oy+34}" r="5" fill="none" stroke="currentColor" stroke-width="2"/>'
        b += arrow(f"k{alpha}", "r", ox - nud, oy, round(t1[0], 1), round(t1[1], 1), 3.2)
        b += arrow(f"k{alpha}", "b", ox + nud, oy, round(t2[0], 1), round(t2[1], 1), 3.2)
        if F > 0:
            b += arrow(f"k{alpha}", "g", ox, oy, round(tf[0], 1), round(tf[1], 1), 4)
            b += text(tf[0] + 14, tf[1] + 8, "F", GRN, 18, "start", "700")
        else:
            b += dot(ox, oy, 5, GRN)
        b += text(t1[0] - 12, t1[1] - 4, sub("F", "1"), RED, 18, "end", "700")
        b += text(t2[0] + 12, t2[1] - 4, sub("F", "2"), BLUE, 18, "start", "700")
        if alpha > 0:
            half = alpha / 2
            b += arc(ox, oy, 28, 90 - half, 90 + half, "currentColor", 1.8)
            b += text(ox + 5, oy - 34, "α", "currentColor", 16, "start", "700")
        b += text(30, 36, f"α = {alpha}°", "currentColor", 17, "start", "700")
        b += text(210, 268, f"F₁ = F₂ = 100 N  →  hợp lực F = {F} N", GRN, 17, "middle", "700")
        parts.append(
            f'<svg class="k-a{alpha}" viewBox="0 0 420 280" role="img" '
            f'aria-label="Hai lực kéo 100 niutơn hợp góc {alpha} độ; đường chéo hình bình hành là hợp lực {F} niutơn">{b}</svg>'
        )
    h = '<div class="tl-box tl-sim tl-sim--keo">\n'
    h += '<p class="tl-label">🎛️ Mô phỏng: hai dây kéo xe (nhìn từ trên xuống)</p>\n'
    h += _chips("Góc giữa hai dây", "k", (0, 60, 90, 120, 180), 0)
    h += "\n".join(parts) + "\n"
    h += '<p><strong>Quy tắc hình bình hành:</strong> lấy <span class="lg-F">F₁</span>, <span class="lg-B">F₂</span> làm hai cạnh; <strong class="lg-N">đường chéo</strong> từ xe là hợp lực <em>F</em>.</p>\n</div>\n'
    return h

def sim_doc():
    """Ván nghiêng, lực kế nằm dọc ván. P = 2,0 N. Số trên lực kế là Px = P sin α."""
    rows = ((0, 0.0, 2.0, "0", "2,0"), (15, 0.52, 1.93, "0,52", "1,93"),
            (30, 1.0, 1.73, "1,0", "1,73"), (45, 1.41, 1.41, "1,41", "1,41"),
            (60, 1.73, 1.0, "1,73", "1,0"))
    parts = []
    foot, Lslope = (96, 274), 236
    for alpha, px, py, spx, spy in rows:
        a = math.radians(alpha)
        U = (math.cos(a), -math.sin(a))
        Nout = (-math.sin(a), -math.cos(a))

        def along(t, lift=0):
            return (foot[0] + t * Lslope * U[0] + lift * Nout[0],
                    foot[1] + t * Lslope * U[1] + lift * Nout[1])

        top = along(1)
        b = defs(f"n{alpha}")
        if alpha == 0:
            b += f'<rect x="{foot[0]:.0f}" y="{foot[1]:.0f}" width="{Lslope}" height="12" rx="2" fill="rgba(148,163,184,.16)" stroke="currentColor" stroke-width="2.2"/>'
        else:
            b += f'<polygon points="{P(*foot)} {P(*top)} {P(top[0], foot[1])}" fill="rgba(148,163,184,.14)" stroke="currentColor" stroke-width="2.2"/>'
            b += arc(foot[0], foot[1], 46, 0, alpha, "currentColor")
            b += text(foot[0] + 54, foot[1] - 8, "α", "currentColor", 17, "start", "700")
        c, hw, hh = along(0.42), 26, 18
        corners = []
        for sx, sy in ((-1, 0), (1, 0), (1, 1), (-1, 1)):
            corners.append((c[0] + sx * hw * U[0] + sy * hh * Nout[0],
                            c[1] + sx * hw * U[1] + sy * hh * Nout[1]))
        b += f'<polygon points="{" ".join(P(*q) for q in corners)}" fill="rgba(251,146,60,.22)" stroke="currentColor" stroke-width="2.2"/>'
        t0, slen, thick = 0.58, 78, 26
        hook = along(t0, 1)
        face = (c[0] + hw * U[0] + (hh * 0.55) * Nout[0], c[1] + hw * U[1] + (hh * 0.55) * Nout[1])
        b += line(face[0], face[1], *along(t0, thick / 2), "currentColor", 2)
        b += (f'<g transform="translate({hook[0]:.1f},{hook[1]:.1f}) rotate({-alpha})">'
              f'<rect x="0" y="{-thick}" width="{slen}" height="{thick}" rx="7" '
              f'fill="rgba(52,211,153,.18)" stroke="{GRN}" stroke-width="2.2"/>'
              f'<path d="M12,{-thick / 2:.0f} l6,-6 l6,12 l6,-12 l6,12 l6,-6" fill="none" stroke="{GRN}" stroke-width="1.6"/>'
              f"</g>")
        b += f'<circle cx="{along(t0, thick / 2)[0]:.1f}" cy="{along(t0, thick / 2)[1]:.1f}" r="3.5" fill="none" stroke="{GRN}" stroke-width="2"/>'
        pin = along(t0 + slen / Lslope, thick / 2)
        b += dot(pin[0], pin[1], 4.5, GRN)
        mid = along(t0 + (slen / 2) / Lslope, thick + 58)
        outer = along(t0 + (slen / 2) / Lslope, thick)
        inward = (math.sin(a), math.cos(a))
        tx = 46 / abs(inward[0]) if abs(inward[0]) > 1e-6 else 1e9
        ty = 16 / abs(inward[1]) if abs(inward[1]) > 1e-6 else 1e9
        hit = min(tx, ty)
        edge = (mid[0] + inward[0] * hit, mid[1] + inward[1] * hit)
        b += line(outer[0], outer[1], edge[0], edge[1], GRN, 1.6)
        b += f'<rect x="{mid[0] - 46:.1f}" y="{mid[1] - 16:.1f}" width="92" height="32" rx="8" fill="rgba(52,211,153,.16)" stroke="{GRN}" stroke-width="2"/>'
        b += text(mid[0], mid[1] + 7, f"{spx} N", GRN, 20, "middle", "700")
        g = (c[0] + (hh * 0.45) * Nout[0], c[1] + (hh * 0.45) * Nout[1])
        Lp = 84
        ptip = (g[0], g[1] + Lp)
        pxv = (-U[0] * Lp * math.sin(a), -U[1] * Lp * math.sin(a))
        pyv = (-Nout[0] * Lp * math.cos(a), -Nout[1] * Lp * math.cos(a))
        if alpha > 0:
            b += line(g[0] + pxv[0], g[1] + pxv[1], ptip[0], ptip[1], "currentColor", 2, "5 4", .9)
            b += line(g[0] + pyv[0], g[1] + pyv[1], ptip[0], ptip[1], "currentColor", 2, "5 4", .9)
            b += arrow(f"n{alpha}", "g", round(g[0], 1), round(g[1], 1), round(g[0] + pxv[0], 1), round(g[1] + pxv[1], 1), 3)
            b += arrow(f"n{alpha}", "o", round(g[0], 1), round(g[1], 1), round(g[0] + pyv[0], 1), round(g[1] + pyv[1], 1), 3)
        b += arrow(f"n{alpha}", "r", round(g[0], 1), round(g[1], 1), round(ptip[0], 1), round(ptip[1], 1), 3.2)
        b += dot(g[0], g[1], 3.5)
        b += text(ptip[0] + 10, ptip[1] + 6, "P", RED, 17, "start", "700")
        if alpha > 0:
            b += text(g[0] + pxv[0] - 8, g[1] + pxv[1] + 4, sub("P", "x"), GRN, 17, "end", "700")
            b += text(g[0] + pyv[0] + 8, g[1] + pyv[1] + 16, sub("P", "y"), ORG, 17, "start", "700")
        parts.append(
            f'<svg class="n-a{alpha}" viewBox="0 0 440 324" role="img" '
            f'aria-label="Dốc {alpha} độ, lực kế chỉ {spx} niutơn">{b}</svg>'
        )
    h = '<div class="tl-box tl-box--exp tl-sim tl-sim--doc">\n'
    h += '<p class="tl-label">🎛️ Thí nghiệm: đổi góc, đọc lực kế</p>\n'
    h += _chips("Góc nghiêng", "n", (0, 15, 30, 45, 60), 30)
    h += "\n".join(parts) + "\n</div>\n"
    return h

h = open("theory.src.html", encoding="utf8").read()
assert "<!--SIMKEO-->" in h and "<!--SIMDOC-->" in h
h = h.replace("<!--SIMKEO-->", sim_keo()).replace("<!--SIMDOC-->", sim_doc())
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h))
