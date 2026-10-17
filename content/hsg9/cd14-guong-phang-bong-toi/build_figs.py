"""Sinh 5 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd14-guong-phang-bong-toi/build_figs.py
Quy ước hình: tia sáng nét liền, mũi tên V giữa tia; đường kéo dài và ảnh ảo nét đứt; mặt sau gương gạch chéo;
vùng tối tô đậm, vùng nửa tối tô nhạt. Hình không ghi số liệu của quiz."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron

PHUT = 16
TOI = "rgba(51,65,85,.85)"
NUATOI = "rgba(148,163,184,.35)"
T_B, T_O, T_R, T_G = "#0369a1", "#c2410c", "#b91c1c", "#047857"   # màu CHỮ (đậm, đọc rõ trên nền sáng)


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def poly(pts, fill):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" stroke="none"/>'


def ray(p, q, c=ORG, w=2.2, at=0.5):
    """Tia sáng thật: nét liền p→q, đầu V ở giữa tia (hoặc tại tỉ lệ `at`)."""
    mx, my = p[0] + (q[0] - p[0]) * at, p[1] + (q[1] - p[1]) * at
    return line(*p, *q, c, w) + chevron(mx + (q[0] - p[0]) * 0.04, my + (q[1] - p[1]) * 0.04, q[0] - p[0], q[1] - p[1], c, w, 11)


def ext(p, q, c=ORG, w=1.6):
    """Đường kéo dài (không có ánh sáng thật): nét đứt."""
    return line(*p, *q, c, w, "6 5", .9)


def mirror(p, q, side, w=3.2, n=None, L=10):
    """Gương thẳng p→q, gạch chéo ở mặt sau. side=+1/−1 chọn phía pháp tuyến (x,y)->(−dy,dx)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    Lm = math.hypot(dx, dy)
    ux, uy = dx / Lm, dy / Lm
    nx, ny = -uy * side, ux * side
    s = line(*p, *q, "currentColor", w)
    k = n or max(4, int(Lm // 14))
    for j in range(k + 1):
        t = j / k
        x, y = p[0] + dx * t, p[1] + dy * t
        s += line(x, y, x + nx * L - ux * 6, y + ny * L - uy * 6, "currentColor", 1.3, "", .75)
    return s


def dot(p, c="currentColor", r=3.6, hollow=False):
    if hollow:
        return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r+0.6:.1f}" fill="none" stroke="{c}" stroke-width="1.8" stroke-dasharray="3 2"/>'
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{c}"/>'


def rich(x, y, parts, c="currentColor", size=15, anchor="start", weight="700"):
    """Chữ có chỉ số: parts = [("S", 0), ("1", 1)] — 1 là chỉ số dưới (cỡ 12, hạ 4)."""
    s, low = "", False
    for t, is_sub in parts:
        if is_sub and not low:
            s += f'<tspan font-size="12" dy="4">{t}</tspan>'
            low = True
        elif not is_sub and low:
            s += f'<tspan dy="-4">{t}</tspan>'
            low = False
        else:
            fs = ' font-size="12"' if is_sub else ""
            s += f'<tspan{fs}>{t}</tspan>'
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'


def arc(c, r, a0, a1, col="currentColor", w=1.6):
    """Cung tròn tâm c, bán kính r, từ góc a0 tới a1 (độ, hệ SVG: 0° sang phải, 90° xuống dưới)."""
    x0, y0 = c[0] + r * math.cos(math.radians(a0)), c[1] + r * math.sin(math.radians(a0))
    x1, y1 = c[0] + r * math.cos(math.radians(a1)), c[1] + r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    return f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}" fill="none" stroke="{col}" stroke-width="{w}"/>'


def polar(c, r, a):
    return (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))


def at_x(p, q, x):
    return p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0])


# ═════════ Hình 1: nguồn rộng, vật chắn lớn hơn nguồn → vùng tối + nửa tối ═════════
XS, XV, XM = 40, 150, 290                 # nguồn, vật chắn, màn (khoảng cách đo từ nguồn)
S1, S2 = (XS, 130), (XS, 170)             # hai mép nguồn (trên, dưới)
V1, V2 = (XV, 110), (XV, 190)             # hai mép vật chắn
yt1, yt2 = at_x(S1, V1, XM), at_x(S2, V2, XM)      # tia cùng mép → vùng tối
yn1, yn2 = at_x(S2, V1, XM), at_x(S1, V2, XM)      # tia chéo mép → mép ngoài nửa tối
# kiểm bằng công thức của bài: d_t = D + (d − D)L/a, d_n = (d + D)L/a − D
Dn, dv, a_, L_ = 40, 80, XV - XS, XM - XS
assert abs((yt2 - yt1) - (Dn + (dv - Dn) * L_ / a_)) < 1e-9
assert abs((yn2 - yn1) - ((dv + Dn) * L_ / a_ - Dn)) < 1e-9
assert 20 < yn1 < yt1 < yt2 < yn2 < 290
b = ""
b += poly([V1, (XM, yn1), (XM, yt1)], NUATOI) + poly([V2, (XM, yn2), (XM, yt2)], NUATOI)
b += poly([V1, (XM, yt1), (XM, yt2), V2], TOI)
b += line(XM, 20, XM, 282, "currentColor", 3)                                   # màn
b += line(XM, yt1, XM, yt2, "currentColor", 7, "", .55)                         # vệt tối trên màn
b += f'<rect x="{XS-5}" y="{S1[1]}" width="10" height="{S2[1]-S1[1]}" rx="3" fill="{ORG}" opacity=".9"/>'   # đèn
b += line(*V1, *V2, "currentColor", 5)                                          # vật chắn
for p, q, col in ((S1, (XM, yt1), BLUE), (S2, (XM, yt2), BLUE), (S2, (XM, yn1), ORG), (S1, (XM, yn2), ORG)):
    b += ray(p, q, col, 1.8, 0.3)
b += text(XS, 196, "nguồn", T_O, 15, "middle", "700")
b += text(144, 216, "vật chắn", "currentColor", 15, "end", "700")
b += text(XM, 14, "màn", "currentColor", 15, "middle", "700")
b += text(XM + 8, (yn1 + yt1) / 2 + 5, "nửa tối", "currentColor", 15, "start", "700")
b += text(XM + 8, (yt1 + yt2) / 2 + 5, "vùng tối", "currentColor", 15, "start", "700")
b += text(XM + 8, (yt2 + yn2) / 2 + 5, "nửa tối", "currentColor", 15, "start", "700")
for y, x2, lab in ((292, XV, "a"), (310, XM, "L")):
    b += line(XS, y, x2, y, "currentColor", 1.4) + chevron(x2, y, 1, 0, "currentColor", 1.4, 8) + chevron(XS, y, -1, 0, "currentColor", 1.4, 8)
    b += line(x2, y - 6, x2, y + 6, "currentColor", 1.2) + line(XS, y - 6, XS, y + 6, "currentColor", 1.2)
    b += text((XS + x2) / 2, y - 4, lab, "currentColor", 15, "middle", "700")
fig1 = wrap("0 0 400 320", "Nguồn sáng rộng, vật chắn lớn hơn nguồn và màn. Hai tia cùng mép giới hạn vùng tối, hai tia chéo mép giới hạn mép ngoài vùng nửa tối",
            b, "Hình 1. Nguồn rộng, vật chắn lớn hơn nguồn.<br>Tia cùng mép (xanh) giới hạn vùng tối.<br>Tia chéo mép (cam) giới hạn mép ngoài vùng nửa tối.<br>a, L đều đo từ nguồn.")

# ═════════ Hình 2: định luật phản xạ ═════════
I = (200, 210)
IA = 48                                   # góc tới vẽ minh hoạ (độ)
S = polar(I, 150, -90 - IA)               # tia tới đến từ trên trái
R = polar(I, 150, -90 + IA)
N = (200, 52)
b = mirror((50, 210), (350, 210), 1)      # gạch chéo phía dưới (mặt sau)
b += ext(I, N, "currentColor", 1.6)
b += ray(S, I, ORG, 2.4) + ray(I, R, ORG, 2.4)
b += arc(I, 44, -90 - IA, -90, RED, 1.8) + arc(I, 44, -90, -90 + IA, RED, 1.8)
b += arc(I, 70, 180, 180 + (90 - IA), GRN, 1.8)
pi_ = polar(I, 60, -90 - IA / 2)
pr_ = polar(I, 60, -90 + IA / 2)
pb_ = polar(I, 86, 180 + (90 - IA) / 2)
b += text(pi_[0], pi_[1] + 5, "i", T_R, 16, "middle", "700")
b += rich(pr_[0] - 2, pr_[1] + 5, [("i'", 0)], T_R, 16, "middle")
b += text(pb_[0] - 2, pb_[1] + 6, "β", T_G, 16, "middle", "700")
b += text(S[0] - 6, S[1] - 4, "S", "currentColor", 16, "end", "700")
b += text(R[0] + 6, R[1] - 4, "R", "currentColor", 16, "start", "700")
b += text(N[0] + 8, N[1] + 12, "N", "currentColor", 16, "start", "700")
b += text(I[0], I[1] + 34, "I", "currentColor", 16, "middle", "700")
b += text(342, 200, "gương", "currentColor", 15, "end", "700")
b += text(208, 120, "pháp tuyến", "currentColor", 15, "start", "600")
fig2 = wrap("0 40 400 220", "Tia tới SI phản xạ trên gương phẳng thành tia IR; pháp tuyến IN; góc tới i bằng góc phản xạ i phẩy; góc beta giữa tia tới và mặt gương",
            b, "Hình 2. Góc tới i và góc phản xạ i' đo với pháp tuyến IN.<br>β là góc giữa tia và mặt gương: i = 90° − β.")

# ═════════ Hình 3: ảnh qua gương phẳng, tia phản xạ kéo dài qua S' ═════════
XG = 200
S = (110, 160)
Sp = (2 * XG - S[0], S[1])
I1, I2 = (XG, 100), (XG, 222)
b = mirror((XG, 34), (XG, 286), -1)       # gạch chéo bên phải (sau gương)
b += line(*S, *Sp, "currentColor", 1.2, "3 4", .6)
for Ik in (I1, I2):
    dx, dy = Ik[0] - Sp[0], Ik[1] - Sp[1]
    t = 0.95
    Rk = (Ik[0] + dx * t, Ik[1] + dy * t)
    b += ray(S, Ik, ORG, 2.2) + ray(Ik, Rk, ORG, 2.2) + ext(Ik, Sp, ORG)
    # kiểm định luật phản xạ: góc với pháp tuyến (phương ngang) hai bên bằng nhau
    a_in = math.degrees(math.atan2(abs(Ik[1] - S[1]), Ik[0] - S[0]))
    a_out = math.degrees(math.atan2(abs(Rk[1] - Ik[1]), Ik[0] - Rk[0]))
    assert abs(a_in - a_out) < 1e-9
b += dot(S, "currentColor") + dot(Sp, "currentColor", 3.6, True)
b += text(S[0] - 8, S[1] + 5, "S", "currentColor", 16, "end", "700")
b += text(Sp[0] + 10, Sp[1] + 5, "S'", "currentColor", 16, "start", "700")
b += text(I1[0] + 10, I1[1] - 6, "I", "currentColor", 16, "start", "700")
b += text(I2[0] + 10, I2[1] + 18, "J", "currentColor", 16, "start", "700")
b += text((S[0] + XG) / 2, S[1] - 8, "d", "currentColor", 15, "middle", "700")
b += text((Sp[0] + XG) / 2, S[1] - 8, "d", "currentColor", 15, "middle", "700")
b += text(XG + 14, 28, "gương", "currentColor", 15, "start", "700")
fig3 = wrap("0 10 400 290", "Điểm sáng S trước gương phẳng, ảnh ảo S phẩy đối xứng sau gương; hai tia phản xạ tại I và J có đường kéo dài nét đứt đi qua S phẩy",
            b, "Hình 3. Ảnh S' đối xứng với S qua gương.<br>Đường kéo dài của mọi tia phản xạ (nét đứt) đi qua S'.")

# ═════════ Hình 4: gương thấy toàn thân ═════════
FLOOR, TOP, EYE = 290, 70, 88               # sàn, đỉnh đầu, mắt (px)
XP, XG, XA = 120, 220, 320                  # người, gương, ảnh (XA − XG = XG − XP)
assert XA - XG == XG - XP
M = (XP, EYE)                               # mắt (trên trục thân, trong đầu)
Mi = (2 * XG - M[0], EYE)
head_top, foot = (XP, TOP), (XP, FLOOR)
ih, ifo = (XA, TOP), (XA, FLOOR)
P = (XG, at_x(M, ih, XG))
Q = (XG, at_x(M, ifo, XG))
# kiểm: P ở giữa mắt và đỉnh đầu, Q ở nửa độ cao mắt, PQ = h/2
assert abs(P[1] - (EYE + TOP) / 2) < 1e-6 and abs((FLOOR - Q[1]) - (FLOOR - EYE) / 2) < 1e-6
assert abs((Q[1] - P[1]) - (FLOOR - TOP) / 2) < 1e-6


def stick(x, dash="", op=1):
    s = f'<circle cx="{x}" cy="{TOP+16}" r="16" fill="none" stroke="currentColor" stroke-width="2.4"{" stroke-dasharray=" + chr(34) + dash + chr(34) if dash else ""} opacity="{op}"/>'
    for (x1, y1, x2, y2) in ((x, TOP + 32, x, 210), (x, 210, x - 16, FLOOR), (x, 210, x + 16, FLOOR), (x, 130, x - 22, 180), (x, 130, x + 22, 180)):
        s += line(x1, y1, x2, y2, "currentColor", 2.4, dash, op)
    return s


b = line(30, FLOOR, 380, FLOOR, "currentColor", 1.6)
b += mirror((XG, P[1]), (XG, Q[1]), -1, 3.6)
b += line(XG, 40, XG, P[1], "currentColor", 1, "2 4", .5) + line(XG, Q[1], XG, FLOOR, "currentColor", 1, "2 4", .5)
b += stick(XP) + stick(XA, "5 4", .7)
b += dot(M, BLUE, 3.4)
b += ray(head_top, P, ORG, 2) + ray(P, M, ORG, 2) + ext(P, ih, ORG)
b += ray(foot, Q, ORG, 2) + ray(Q, M, ORG, 2) + ext(Q, ifo, ORG)
b += text(XG + 8, P[1] + 20, "P", "currentColor", 16, "start", "700")
b += text(XG + 8, Q[1] - 8, "Q", "currentColor", 16, "start", "700")
b += text(M[0] + 4, EYE - 28, "mắt", T_B, 15, "start", "700")
b += text(XA, 54, "ảnh", "currentColor", 15, "middle", "700")
b += line(44, TOP, 44, FLOOR, "currentColor", 1.4) + chevron(44, TOP, 0, -1, "currentColor", 1.4, 8) + chevron(44, FLOOR, 0, 1, "currentColor", 1.4, 8)
b += text(38, (TOP + FLOOR) / 2 + 5, "h", "currentColor", 16, "end", "700")
b += line(66, EYE, 66, FLOOR, BLUE, 1.4) + chevron(66, EYE, 0, -1, BLUE, 1.4, 8) + chevron(66, FLOOR, 0, 1, BLUE, 1.4, 8)
b += rich(72, FLOOR - 14, [("h", 0), ("m", 1)], T_B, 16)
fig4 = wrap("0 30 400 280", "Người đứng trước gương thẳng đứng PQ và ảnh của người sau gương; tia từ đỉnh đầu phản xạ tại P, tia từ chân phản xạ tại Q, cả hai vào mắt; đường kéo dài nét đứt tới ảnh",
            b, "Hình 4. Tia từ đỉnh đầu phản xạ ở mép P, tia từ chân phản xạ ở mép Q, rồi vào mắt.<br>Đường kéo dài (nét đứt) đi tới ảnh.<br>h: chiều cao người; h<sub>m</sub>: độ cao mắt.")

# ═════════ Hình 5: hai gương vuông góc, ảnh trên đường tròn ═════════
O = (190, 175)
RR = 112
TH = 32                                    # góc của S so với G1 (độ, ngược chiều kim đồng hồ)
Sx = (O[0] + RR * math.cos(math.radians(TH)), O[1] - RR * math.sin(math.radians(TH)))
S1_ = (Sx[0], 2 * O[1] - Sx[1])            # qua G1 (nằm ngang)
S2_ = (2 * O[0] - Sx[0], Sx[1])            # qua G2 (thẳng đứng)
S3_ = (2 * O[0] - Sx[0], 2 * O[1] - Sx[1])  # ảnh kép (trùng nhau)
for p in (S1_, S2_, S3_):
    assert abs(math.dist(O, p) - RR) < 1e-9
b = f'<circle cx="{O[0]}" cy="{O[1]}" r="{RR}" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 5" opacity=".55"/>'
b += mirror(O, (372, O[1]), 1)            # G1: gạch chéo phía dưới
b += mirror(O, (O[0], 28), -1)            # G2: gạch chéo bên trái
b += line(*Sx, *S1_, "currentColor", 1.2, "3 4", .6) + line(*Sx, *S2_, "currentColor", 1.2, "3 4", .6)
b += line(*S1_, *S3_, "currentColor", 1.2, "3 4", .6) + line(*S2_, *S3_, "currentColor", 1.2, "3 4", .6)
b += dot(Sx, ORG, 4.2)
for p in (S1_, S2_, S3_):
    b += dot(p, "currentColor", 3.6, True)
b += text(Sx[0] + 10, Sx[1] - 6, "S", T_O, 16, "start", "700")
b += rich(S1_[0] + 10, S1_[1] + 6, [("S", 0), ("1", 1)], "currentColor", 16)
b += rich(S2_[0] - 10, S2_[1] - 6, [("S", 0), ("2", 1)], "currentColor", 16, "end")
b += rich(S3_[0] - 10, S3_[1] + 6, [("S", 0), ("3", 1)], "currentColor", 16, "end")
b += text(O[0] - 8, O[1] + 20, "O", "currentColor", 16, "end", "700")
b += rich(368, O[1] - 10, [("G", 0), ("1", 1)], "currentColor", 16, "end")
b += rich(O[0] + 10, 42, [("G", 0), ("2", 1)], "currentColor", 16)
fig5 = wrap("0 20 400 278", "Hai gương G1 và G2 vuông góc tại O; vật S và ba ảnh S1, S2, S3 cùng nằm trên đường tròn tâm O bán kính OS",
            b, "Hình 5. Hai gương vuông góc: ảnh nằm trên đường tròn tâm O, bán kính OS.<br>S<sub>3</sub> vừa là ảnh của S<sub>1</sub> qua G<sub>2</sub>, vừa là ảnh của S<sub>2</sub> qua G<sub>1</sub>.")

# ═════════ ghi theory.html ═════════
src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4, fig5), 1):
    assert src.count(f"<!--FIG{n}-->") == 1, n
    src = src.replace(f"<!--FIG{n}-->", f)
src = src.replace("__PHUT__", str(PHUT))
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
