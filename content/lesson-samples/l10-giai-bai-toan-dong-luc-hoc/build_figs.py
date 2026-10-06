"""Sinh 5 hình SVG cho bài 20 'Một số ví dụ về cách giải các bài toán thuộc phần động lực học' (lesson 65),
thay mốc <!--FIGn--> và bảng __BANG_TN2__ trong theory.src.html -> theory.html.
Chạy (sau build_thi_nghiem.py): python3 build_figs.py
Độ dài mũi tên lực tính từ độ lớn lực (một thang px/N cho mỗi hình), hướng tính từ góc nghiêng; script kiểm:
nhãn không chồng nhau, không vượt viewBox, không bị nét đã đăng ký cắt xuyên; các lực đúng chiều vật lí."""
import json, math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2, tên)
CHECKS = []
CUR = {"fig": 0}
VB = {}
G = 10


def defs(p):
    out = "<defs>"
    for n, c in COL.items():
        out += (f'<marker id="{p}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="12" markerHeight="12" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"


def arrow(p, c, x1, y1, x2, y2, w=3, name="", dash=""):
    if name:
        SEGS.append((CUR["fig"], x1, y1, x2, y2, name))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
            f'marker-end="url(#{p}-{c})"/>')


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, name=""):
    if name:
        SEGS.append((CUR["fig"], x1, y1, x2, y2, name))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def it(s):
    return f'<tspan font-style="italic" font-family="serif">{s}</tspan>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="13">{s}</tspan>'


def text(x, y, s, c="currentColor", size=17, anchor="start", weight="700"):
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.25 * size, plain))
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{s}</text>')


def same_dir(fig, name, x1, y1, x2, y2, ux, uy, tol_deg=1.0):
    """Kiểm mũi tên (x1,y1)->(x2,y2) cùng hướng vectơ (ux,uy)."""
    ax, ay = x2 - x1, y2 - y1
    c = (ax * ux + ay * uy) / (math.hypot(ax, ay) * math.hypot(ux, uy))
    ang = math.degrees(math.acos(max(-1, min(1, c))))
    if ang > tol_deg:
        CHECKS.append(f"Hình {fig}: '{name}' lệch {ang:.1f}° so với hướng vật lí")


def length_ok(fig, name, x1, y1, x2, y2, want, tol=0.6):
    L = math.hypot(x2 - x1, y2 - y1)
    if abs(L - want) > tol:
        CHECKS.append(f"Hình {fig}: '{name}' dài {L:.1f}px, cần {want:.1f}px")


def force(p, c, C, u, L, name, fig):
    """Mũi tên lực gốc ở trọng tâm C, hướng u (đơn vị), dài L px; tự kiểm hướng và độ dài."""
    x2, y2 = C[0] + L * u[0], C[1] + L * u[1]
    same_dir(fig, name, C[0], C[1], x2, y2, *u)
    length_ok(fig, name, C[0], C[1], x2, y2, L)
    return arrow(p, c, C[0], C[1], x2, y2, 3.2, name=name), (x2, y2)


def kid(cx, cy, rb, rh):
    """Người ngồi trên cầu trượt (nhìn ngang): thân tròn + đầu."""
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rb}" fill="rgba(56,189,248,.35)" stroke="currentColor" stroke-width="2"/>'
            f'<circle cx="{cx:.1f}" cy="{cy - rb - rh:.1f}" r="{rh}" fill="rgba(251,146,60,.35)" stroke="currentColor" stroke-width="2"/>')


# ---------------- Hình 1: hai làn cầu trượt (mở bài, chỉ cảnh — không lực, không số) ----------------
CUR["fig"] = 1
VB[1] = (420, 230)
b = defs("f1")
GROUND = 212
b += line(8, GROUND, 412, GROUND, "currentColor", 2)
for i, (rb, rh, lab, lx) in enumerate(((9, 6, "em", None), (13, 8, "bạn nặng gấp đôi", None))):
    x0 = 18 + i * 200
    T = (x0 + 24, 70)
    E = (x0 + 190, 200)
    L = math.hypot(E[0] - T[0], E[1] - T[1])
    u = ((E[0] - T[0]) / L, (E[1] - T[1]) / L)
    n = (u[1], -u[0])                               # pháp tuyến hướng lên khỏi mặt trượt
    assert n[1] < 0
    b += line(x0 + 10, T[1] - 6, x0 + 10, GROUND, "currentColor", 2)       # thang
    b += line(T[0], T[1] - 6, T[0], GROUND, "currentColor", 2)
    for k in range(4):
        yk = T[1] + 22 + 32 * k
        b += line(x0 + 10, yk, T[0], yk, "currentColor", 1.6)
    b += line(*T, *E, "currentColor", 4) + line(E[0], E[1], E[0] + 14, E[1], "currentColor", 4)   # mặt trượt
    S = (T[0] + 0.14 * L * u[0], T[1] + 0.14 * L * u[1])
    cx, cy = S[0] + (rb + 2) * n[0], S[1] + (rb + 2) * n[1]
    b += kid(cx, cy, rb, rh)
    top = cy - rb - 2 * rh
    b += text(cx, top - 8, lab, BLUE if i == 0 else ORG, 17, "middle", "700")
    slope_deg = math.degrees(math.atan2(E[1] - T[1], E[0] - T[0]))
assert abs(slope_deg - math.degrees(math.atan2(130, 166))) < 1e-9   # hai làn cùng độ dốc
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Hai làn cầu trượt giống hệt nhau, cùng độ dốc; bên trái là em, bên phải là bạn nặng gấp đôi, cả hai ngồi ở đỉnh sắp buông tay",
            b, "Hình 1. Hai làn trượt giống hệt nhau. Cùng buông tay: ai tới chân trước?")
fig1 = fig1.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-giaibt-dlh-01"', 1)

# ---------------- Hình 2: gia tốc là cầu nối ----------------
CUR["fig"] = 2
VB[2] = (420, 270)
b = defs("f2")
BOX = [(12, 132, "các lực", it("ΣF")), (170, 250, "cầu nối", it("a")), (288, 408, "chuyển động", it("v, s, t"))]
for x0, x1, cap, inner in BOX:
    b += (f'<rect x="{x0}" y="36" width="{x1 - x0}" height="46" rx="8" fill="rgba(148,163,184,.15)" '
          f'stroke="currentColor" stroke-width="2"/>')
    b += text((x0 + x1) / 2, 24, cap, size=17, anchor="middle", weight="600")
    b += text((x0 + x1) / 2, 66, inner, GRN if cap == "cầu nối" else "currentColor", 22, "middle")
for (xa, xb), c in (((132, 170), "g"), ((250, 288), "g")):
    b += arrow("f2", c, xa + 2, 112, xb - 2, 112, 3)
for (xa, xb), c in (((288, 250), "r"), ((170, 132), "r")):
    b += arrow("f2", c, xa - 2, 178, xb + 2, 178, 3)
b += text(12, 142, "Thuận: biết lực → tìm chuyển động", GRN, 17, "start", "700")
b += text(12, 208, "Ngược: biết chuyển động → tìm lực", RED, 17, "start", "700")
b += text(12, 240, "Lực ↔ a: định luật II, ΣF = ma", size=17, weight="600")
b += text(12, 262, "a ↔ chuyển động: công thức v, s, t", size=17, weight="600")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Sơ đồ ba ô: các lực, gia tốc a, chuyển động. Bài toán thuận đi từ lực qua a tới chuyển động; bài toán ngược đi chiều ngược lại",
            b, "Hình 2. Gia tốc <em>a</em> nằm giữa: định luật II nối lực với <em>a</em>, công thức chuyển động nối <em>a</em> với <em>v</em>, <em>s</em>, <em>t</em>.")

# ---------------- Hình 3: thùng kéo xiên trên sàn (sơ đồ lực) ----------------
CUR["fig"] = 3
VB[3] = (420, 280)
m3, F3, al3, mu3 = 20, 100, 30, 0.2          # đúng số Câu 1: F_ms = 0,2·150 = 30 N
N3 = m3 * G - F3 * math.sin(math.radians(al3))
f3 = mu3 * N3
assert F3 * math.cos(math.radians(al3)) > f3   # thùng tăng tốc theo chiều kéo
K3 = 0.65                                     # px/N
C3 = (190, 125)
b = defs("f3")
b += line(20, C3[1] + 22, 400, C3[1] + 22, "currentColor", 2.4)
for k in range(10):
    xh = 30 + 38 * k
    b += line(xh, C3[1] + 22, xh - 10, C3[1] + 32, "currentColor", 1.2, op=.5)
b += (f'<rect x="{C3[0] - 30}" y="{C3[1] - 22}" width="60" height="44" rx="3" fill="rgba(251,146,60,.18)" '
      f'stroke="currentColor" stroke-width="2"/>')
ua = (math.cos(math.radians(al3)), -math.sin(math.radians(al3)))
b += line(C3[0], C3[1], C3[0] + 92, C3[1], "currentColor", 1.3, "5 5", .6)          # mốc ngang của góc α
sP, tP = force("f3", "r", C3, (0, 1), K3 * m3 * G, "P", 3)
sN, tN = force("f3", "b", C3, (0, -1), K3 * N3, "N", 3)
sF, tF = force("f3", "o", C3, ua, K3 * F3, "F", 3)
sf, tf = force("f3", "r", C3, (-1, 0), K3 * f3, "Fms", 3)
b += sP + sN + sF + sf
A_R = 44
pts = [(C3[0] + A_R * math.cos(math.radians(t)), C3[1] - A_R * math.sin(math.radians(t))) for t in range(0, al3 + 1, 3)]
b += '<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '" fill="none" stroke="currentColor" stroke-width="1.6"/>'
b += text(C3[0] + 52 * math.cos(math.radians(14)) + 2, C3[1] - 52 * math.sin(math.radians(14)) + 6, it("α"), size=19)
b += f'<circle cx="{C3[0]}" cy="{C3[1]}" r="3.5" fill="currentColor"/>'
b += text(tP[0] + 9, tP[1] - 4, it("P"), RED, 19)
b += text(tN[0] + 9, tN[1] + 12, it("N"), BLUE, 19)
b += text(tF[0] + 6, tF[1] - 8, it("F"), ORG, 19)
b += text(tf[0] - 8, tf[1] - 12, sub(it("F"), "ms"), RED, 19, "end")
# trục toạ độ
OX = (42, 252)
b += arrow("f3", "k", *OX, OX[0] + 58, OX[1], 2, name="Ox") + arrow("f3", "k", *OX, OX[0], OX[1] - 58, 2, name="Oy")
b += text(OX[0] + 62, OX[1] + 6, it("x"), size=18) + text(OX[0] + 8, OX[1] - 52, it("y"), size=18)
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Thùng trên sàn kéo bằng dây xiên lên góc alpha: trọng lực P hướng xuống, phản lực N hướng lên ngắn hơn P, lực kéo F xiên lên, ma sát hướng ngược chiều kéo; trục x theo chiều kéo, y hướng lên",
            b, "Hình 3. Kéo xiên lên góc α: bốn lực vẽ chung gốc ở trọng tâm. Phản lực <em>N</em> (xanh) ngắn hơn trọng lực <em>P</em> vì dây nhấc bớt thùng.")
fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-giaibt-dlh-03"', 1)

# ---------------- Hình 4: vật trượt xuống mặt phẳng nghiêng ----------------
CUR["fig"] = 4
VB[4] = (420, 290)
al4, mu4 = 30, 0.2                             # khớp Câu 2 (μ = 0,2); vật trượt xuống: tanα > μ
assert math.tan(math.radians(al4)) > mu4
ra = math.radians(al4)
BASE_Y, XL, XR = 260, 20, 400
TOP = (XL, BASE_Y - (XR - XL) * math.tan(ra))
u4 = (math.cos(ra), math.sin(ra))              # xuống dốc (SVG: y hướng xuống)
n4 = (math.sin(ra), -math.cos(ra))             # pháp tuyến hướng ra khỏi mặt nghiêng
K4, m4 = 11, 1.0                               # px/N với m = 1 kg -> P = 10 N = 110 px
P4 = m4 * G
N4 = P4 * math.cos(ra)
f4 = mu4 * N4
b = defs("f4")
b += (f'<path d="M{XL},{BASE_Y} L{XR},{BASE_Y} L{TOP[0]},{TOP[1]:.1f} z" fill="rgba(148,163,184,.15)" '
      f'stroke="currentColor" stroke-width="2.2"/>')
d = 150
S4 = (TOP[0] + d * u4[0], TOP[1] + d * u4[1])
C4 = (S4[0] + 18 * n4[0], S4[1] + 18 * n4[1])
b += (f'<rect x="{C4[0] - 24:.1f}" y="{C4[1] - 18:.1f}" width="48" height="36" rx="3" fill="rgba(251,146,60,.18)" '
      f'stroke="currentColor" stroke-width="2" transform="rotate({al4} {C4[0]:.1f} {C4[1]:.1f})"/>')
sP, tP = force("f4", "r", C4, (0, 1), K4 * P4, "P", 4)
sN, tN = force("f4", "b", C4, n4, K4 * N4, "N", 4)
sf, tf = force("f4", "r", C4, (-u4[0], -u4[1]), K4 * f4, "Fms", 4)
# hai thành phần của P (nét đứt)
tPs = (C4[0] + K4 * P4 * math.sin(ra) * u4[0], C4[1] + K4 * P4 * math.sin(ra) * u4[1])
tPc = (C4[0] - K4 * P4 * math.cos(ra) * n4[0], C4[1] - K4 * P4 * math.cos(ra) * n4[1])
# kiểm: hai thành phần cộng lại đúng bằng P
assert abs(tPs[0] + tPc[0] - C4[0] - tP[0]) < 1e-6 and abs(tPs[1] + tPc[1] - C4[1] - tP[1]) < 1e-6
b += arrow("f4", "r", *C4, *tPs, 2.2, name="Psin", dash="6 4") + arrow("f4", "r", *C4, *tPc, 2.2, name="Pcos", dash="6 4")
b += line(*tPs, *tP, "currentColor", 1.2, "3 4", .55, name="net dut 1") + line(*tPc, *tP, "currentColor", 1.2, "3 4", .55, name="net dut 2")
SEGS.append((4, XL, BASE_Y, XR, BASE_Y, "day doc")); SEGS.append((4, XL, TOP[1], XR, BASE_Y, "mat nghieng"))
assert tP[1] < BASE_Y - 22   # nhãn P nằm trên đáy
b += sP + sN + sf
b += f'<circle cx="{C4[0]:.1f}" cy="{C4[1]:.1f}" r="3.5" fill="currentColor"/>'
b += text(tP[0] + 8, tP[1] + 16, it("P"), RED, 19)
b += text(tN[0] + 8, tN[1] + 14, it("N"), BLUE, 19)
b += text(tf[0] - 2, tf[1] - 14, sub(it("F"), "ms"), RED, 19, "end")
b += text(tPs[0] + 8, tPs[1] + 8, it("P") + " sin" + it("α"), RED, 17)
b += text(tPc[0] - 8, tPc[1] + 6, it("P") + " cos" + it("α"), RED, 17, "end")
# góc α ở chân phải, giữa đáy và mặt nghiêng
AR = 52
arc_pts = [(XR - AR * math.cos(math.radians(t)), BASE_Y - AR * math.sin(math.radians(t))) for t in range(0, al4 + 1, 3)]
b += '<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in arc_pts) + '" fill="none" stroke="currentColor" stroke-width="1.6"/>'
b += text(XR - 74, BASE_Y - 8, it("α"), size=19)
# trục toạ độ (góc trên phải, ngoài mặt nghiêng)
OX4 = (330, 64)
xa = (OX4[0] + 52 * u4[0], OX4[1] + 52 * u4[1])
ya = (OX4[0] + 52 * n4[0], OX4[1] + 52 * n4[1])
b += arrow("f4", "k", *OX4, *xa, 2, name="Ox") + arrow("f4", "k", *OX4, *ya, 2, name="Oy")
b += text(xa[0] + 4, xa[1] + 16, it("x"), size=18) + text(ya[0] + 8, ya[1] + 6, it("y"), size=18)
# kiểm: chân góc α nằm đúng giao của đáy và mặt nghiêng
assert abs((BASE_Y - TOP[1]) / (XR - XL) - math.tan(ra)) < 1e-9
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Hộp trên mặt phẳng nghiêng góc alpha: trọng lực P thẳng đứng xuống, tách thành P sin alpha dọc dốc và P cos alpha vuông góc mặt nghiêng; phản lực N vuông góc mặt nghiêng bằng P cos alpha; ma sát hướng lên dốc; trục x dọc dốc hướng xuống",
            b, "Hình 4. Trục <em>x</em> dọc dốc: chỉ trọng lực phải tách. <em>N</em> cân bằng với <em>P</em> cos<em>α</em> nên ngắn hơn <em>P</em>; ma sát ngược chiều trượt.")
fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-giaibt-dlh-01"', 1)

# ---------------- Hình 5: hai vật nối dây qua ròng rọc ----------------
CUR["fig"] = 5
VB[5] = (420, 290)
m1, m2, mu = 2, 1, 0.2                          # đúng số của bài toán mẫu
a5 = (m2 * G - mu * m1 * G) / (m1 + m2)
T5 = m2 * (G - a5)
f5 = mu * m1 * G
assert abs(a5 - 2) < 1e-9 and abs(T5 - 8) < 1e-9 and abs(T5 - f5 - m1 * a5) < 1e-9
K5 = 5                                          # px/N
TABLE_Y, TABLE_R = 150, 318
C1 = (150, 128)                                 # tâm khối m1 (cao 44 -> đáy chạm mặt bàn)
PUL = (332, 142, 14)                            # tâm, bán kính ròng rọc: đỉnh ròng rọc ngang tâm m1
assert abs(PUL[1] - PUL[2] - C1[1]) < 1e-9     # dây nằm ngang
XS = PUL[0] + PUL[2]                            # dây thả đứng bên phải ròng rọc
C2 = (XS, 222)
b = defs("f5")
b += line(10, TABLE_Y, TABLE_R, TABLE_Y, "currentColor", 3) + line(TABLE_R - 10, TABLE_Y, TABLE_R - 10, 284, "currentColor", 2.4, name="chan ban")
b += line(TABLE_R - 6, TABLE_Y, PUL[0], PUL[1], "currentColor", 2)
b += f'<circle cx="{PUL[0]}" cy="{PUL[1]}" r="{PUL[2]}" fill="none" stroke="currentColor" stroke-width="2"/>'
b += line(C1[0] + 22, C1[1], PUL[0], C1[1], "currentColor", 1.6, name="day ngang")
b += line(XS, PUL[1], XS, C2[1] - 18, "currentColor", 1.6, name="day dung")
b += (f'<rect x="{C1[0] - 22}" y="{C1[1] - 22}" width="44" height="44" rx="3" fill="rgba(251,146,60,.18)" '
      f'stroke="currentColor" stroke-width="2"/>')
b += (f'<rect x="{C2[0] - 18}" y="{C2[1] - 18}" width="36" height="36" rx="3" fill="rgba(56,189,248,.18)" '
      f'stroke="currentColor" stroke-width="2"/>')
s1, tN1 = force("f5", "b", C1, (0, -1), K5 * m1 * G, "N1", 5)
s2, tP1 = force("f5", "r", C1, (0, 1), K5 * m1 * G, "P1", 5)
s3, tT1 = force("f5", "o", C1, (1, 0), K5 * T5, "T1", 5)
s4, tf5 = force("f5", "r", C1, (-1, 0), K5 * f5, "Fms", 5)
s5, tT2 = force("f5", "o", C2, (0, -1), K5 * T5, "T2", 5)
s6, tP2 = force("f5", "r", C2, (0, 1), K5 * m2 * G, "P2", 5)
b += s1 + s2 + s3 + s4 + s5 + s6
for C in (C1, C2):
    b += f'<circle cx="{C[0]}" cy="{C[1]}" r="3.5" fill="currentColor"/>'
b += text(tN1[0] + 9, tN1[1] + 14, sub(it("N"), "1"), BLUE, 19)
b += text(tP1[0] + 9, tP1[1] - 2, sub(it("P"), "1"), RED, 19)
b += text(tT1[0] + 2, tT1[1] - 12, it("T"), ORG, 19)
b += text(tf5[0] - 10, tf5[1] + 6, sub(it("F"), "ms"), RED, 19, "end")
b += text(tT2[0] - 10, tT2[1] + 4, it("T"), ORG, 19, "end")
b += text(tP2[0] - 10, tP2[1] - 2, sub(it("P"), "2"), RED, 19, "end")
b += text(C1[0] - 30, C1[1] - 30, sub(it("m"), "1"), size=19, anchor="end")
b += text(C2[0] + 24, C2[1] + 6, sub(it("m"), "2"), size=19)
# chiều dương đi vòng theo dây (xanh lá, nét đứt)
b += arrow("f5", "g", 200, 92, 268, 92, 2.6, name="+ngang", dash="7 5")
b += text(234, 82, "(+)", GRN, 17, "middle")
b += arrow("f5", "g", 404, 176, 404, 238, 2.6, name="+dung", dash="7 5")
b += text(400, 262, "(+)", GRN, 17, "middle")
fig5 = wrap(f"0 0 {VB[5][0]} {VB[5][1]}",
            "Khối m1 trên mặt bàn nằm ngang nối dây qua ròng rọc ở mép bàn với quả nặng m2 treo thẳng đứng. Lên m1: P1 xuống, N1 lên bằng P1, lực căng T sang phải, ma sát sang trái. Lên m2: T hướng lên, P2 hướng xuống dài hơn T. Chiều dương: m1 sang phải, m2 hướng xuống",
            b, "Hình 5. Hai vật nối dây: lực căng <em>T</em> (cam) như nhau ở hai đầu dây. Chiều dương (xanh lá) đi vòng theo dây: <em>m</em><sub>1</sub> sang phải, <em>m</em><sub>2</sub> xuống dưới.")
fig5 = fig5.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-giaibt-dlh-02"', 1)


# ---------------- Kiểm toạ độ nhãn ----------------
def seg_hits_box(x1, y1, x2, y2, bx0, by0, bx1, by1):
    for i in range(41):
        t = i / 40
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        if bx0 + 1 < x < bx1 - 1 and by0 + 1 < y < by1 - 1:
            return True
    return False


bad = list(CHECKS)
for i, (f, x0, y0, x1, y1, s) in enumerate(LABELS):
    W, H = VB[f]
    if x0 < 2 or y0 < 2 or x1 > W - 2 or y1 > H - 2:
        bad.append(f"Hình {f}: nhãn '{s}' vượt viewBox ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    for g, a0, b0, a1, b1, t in LABELS[i + 1:]:
        if g == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            bad.append(f"Hình {f}: nhãn '{s}' chồng '{t}'")
    for g, sx1, sy1, sx2, sy2, nm in SEGS:
        if g == f and seg_hits_box(sx1, sy1, sx2, sy2, x0, y0, x1, y1):
            bad.append(f"Hình {f}: nét '{nm}' cắt nhãn '{s}'")
print("\n".join(bad) if bad else "kiểm toạ độ: ok")
if bad:
    sys.exit(1)

# ---------------- Bảng số liệu TN2 lấy từ file thí nghiệm (một nguồn số) ----------------
tn2 = json.loads((HERE.parents[1] / "thi-nghiem/tn-l10-giaibt-dlh-02.json").read_text(encoding="utf8"))


def vn(x, n=2):
    return f"{x:.{n}f}".replace(".", ",")


rows = "\n".join(f"<tr><td>{r[0]}</td><td>{vn(r[1])}</td><td>{vn(r[2])}</td></tr>" for r in tn2["so_lieu_mau"]["hang"])
assert len(tn2["so_lieu_mau"]["hang"]) == 5

src = (HERE / "theory.src.html").read_text(encoding="utf8")
assert "__BANG_TN2__" in src
src = src.replace("__BANG_TN2__", rows)
figs = (fig1, fig2, fig3, fig4, fig5)
order = [int(n) for n in re.findall(r"<!--FIG(\d)-->", src)]
assert order == list(range(1, len(figs) + 1)), order
for n, f in enumerate(figs, 1):
    assert f"<figcaption>Hình {n}." in f, n
    src = src.replace(f"<!--FIG{n}-->", f)

lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
m = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout)
phut = math.ceil(float(m.group(1))) if m else "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut, "(lint đo", m.group(1) if m else "?", ")")
