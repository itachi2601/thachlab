"""Sinh 6 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Kèm khối KIỂM SỐ: mọi số trong quiz/ví dụ/thử thách của bài lý thuyết được tính và assert ở đây.
Chạy: python3 content/hsg9/cd06-khuc-xa-phan-xa-toan-phan/build_figs.py"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron

PHUT = 19
GRAY = "rgba(148,163,184,.22)"
WATER = "rgba(56,189,248,.16)"
GLASS = "rgba(148,163,184,.20)"
VIO = "#a78bfa"
LIGHT = ORG          # tia sáng
S = lambda a: math.sin(math.radians(a))
T = lambda a: math.tan(math.radians(a))
ASIN = lambda x: math.degrees(math.asin(x))
ATAN = lambda x: math.degrees(math.atan(x))


def close(a, b, tol):
    assert abs(a - b) <= tol, (a, b)


# ═════════ KIỂM SỐ (số xuất hiện trong theory.src.html) ═════════
NN = 4 / 3
close(ASIN(S(50) / NN), 35.1, 0.05)                                   # Mở bài: r ≈ 35,1°
close(ASIN(S(45) / 1.5), 28.1, 0.05)                                  # q1: thuỷ tinh i = 45°
# Thí nghiệm bán trụ (số minh hoạ, r đo tròn độ): i = 20/40/70 -> r = 13/25/39
for i, r, k in ((20, 13, 1.52), (40, 25, 1.52), (70, 39, 1.49)):
    close(ASIN(S(i) / 1.5), r, 0.4)
    close(S(i) / S(r), k, 0.006)
close((1.52 + 1.52 + 1.49) / 3, 1.51, 0.005)
for n, v in ((NN, 2.25), (1.5, 2.00), (2.42, 1.24)):                 # bảng vận tốc (1e8 m/s)
    close(3 / n, v, 0.005)
close(1.5 * NN, 2.0, 1e-9); close(1.5 / NN, 1.125, 1e-9)            # q2: chim cao 1,5 m
close(7.5 * (1 - 1 / 1.5), 2.5, 1e-9)                                 # ví dụ bản kính 7,5 cm
for n1, n2, g in ((NN, 1, 48.6), (1.5, 1, 41.8), (2.42, 1, 24.4), (1.5, NN, 62.7)):
    close(ASIN(n2 / n1), g, 0.05)                                     # bảng i_gh
close(ASIN(1.5 * S(55) / NN), 67.2, 0.05)                             # q3 đúng
close(ASIN(NN * S(55) / 1.5), 46.7, 0.05)                             # q3 nhiễu (ngược tỉ số)
TG = math.tan(math.asin(3 / 4))
close(TG, 1.134, 0.0005)
close(0.75 * TG, 0.85, 0.005); close(math.pi * (0.75 * TG) ** 2, 2.27, 0.005)   # bài toán mẫu h = 0,75 m
close(0.75 * T(41.8), 0.67, 0.005)                                    # nhiễu: dùng i_gh của thuỷ tinh
close(0.75 * S(48.6), 0.56, 0.005)                                    # nhiễu: dùng sin thay tan
close(1.0 * TG, 1.13, 0.005)                                          # điền bước h = 1,0 m
close(1.5 * S(35), 0.8604, 0.0001); close(ASIN(1.5 * S(35)), 59.4, 0.05)   # q4: A = 35°
close(ASIN(1.5 * S(35)) - 35, 24.4, 0.05)
close(ASIN(S(45) / math.sqrt(2)), 30, 1e-6); assert 180 - 45 - 30 == 105   # thử thách 1
close(60 / NN + 15 / 1.5, 55, 1e-9)                                   # thử thách 2
A3 = math.degrees(math.acos(0.75))                                    # thử thách 3: D = A
close(A3, 41.4, 0.05); close(ASIN(1.5 * S(A3)), 2 * A3, 1e-6); assert A3 < ASIN(1 / 1.5)
close(math.sqrt(2), 1.414, 0.0005)


# ═════════ helper vẽ ═════════
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def ray(p, q, c=LIGHT, w=2.6, op=1, at=0.55):
    """Tia sáng nét liền p -> q, đầu V ở giữa tia."""
    (x1, y1), (x2, y2) = p, q
    mx, my = x1 + (x2 - x1) * at, y1 + (y2 - y1) * at
    return line(x1, y1, x2, y2, c, w, "", op) + chevron(mx, my, x2 - x1, y2 - y1, c, w, 11).replace("/>", f' opacity="{op}"/>')


def dash(p, q, c="currentColor", w=1.5, op=.75):
    return line(p[0], p[1], q[0], q[1], c, w, "5 4", op)


def go(p, ang, L):
    """Điểm cách p một đoạn L theo hướng ang (độ, 0 = sang phải, 90 = xuống dưới — toạ độ màn hình)."""
    return (p[0] + L * math.cos(math.radians(ang)), p[1] + L * math.sin(math.radians(ang)))


def arc(p, a0, a1, R=34, c="currentColor", w=1.6):
    n = 24
    pts = [go(p, a0 + (a1 - a0) * k / n, R) for k in range(n + 1)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"/>'


def lab(p, s, c="currentColor", size=15, anchor="middle", weight="700"):
    return text(round(p[0], 1), round(p[1], 1), s, c, size, anchor, weight)


def sub(x, y, a, b, c="currentColor", size=15, anchor="middle", tail=""):
    """Chữ a có chỉ số dưới b (cỡ 12, hạ 4)."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">{a}'
            f'<tspan font-size="12" dy="4">{b}</tspan><tspan dy="-4">{tail}</tspan></text>')


def dim(x, y1, y2, c="currentColor"):
    """Mũi tên kích thước thẳng đứng hai đầu."""
    return line(x, y1, x, y2, c, 1.4) + chevron(x, y1, 0, -1, c, 1.4, 8) + chevron(x, y2, 0, 1, c, 1.4, 8)


# ═════════ Hình 1: khúc xạ ở mặt không khí – nước ═════════
I = (200, 150)
b = f'<rect x="20" y="150" width="360" height="140" fill="{WATER}"/>' + line(20, 150, 380, 150, BLUE, 2)
b += dash((200, 26), (200, 284))
Sx = go(I, -90 - 50, 128)                 # nguồn: phía trên bên trái, i = 50°
Rr = go(I, 90 - 35.07, 128)               # tia khúc xạ: r ≈ 35,1°
Rf = go(I, -90 + 50, 120)                 # tia phản xạ (yếu)
b += ray(Sx, I) + ray(I, Rr) + ray(I, Rf, LIGHT, 2, .45)
b += arc(I, -90, -140, 40) + lab(go(I, -112, 54), "i")
b += arc(I, 90, 90 - 35.07, 44) + lab(go(I, 72, 60), "r")
b += f'<circle cx="200" cy="150" r="3.4" fill="currentColor"/>' + lab((188, 170), "I")
b += lab((Sx[0] - 8, Sx[1] - 6), "S")
b += text(208, 38, "pháp tuyến", "currentColor", 15, "start", "600")
b += text(Rf[0] - 4, Rf[1] - 10, "tia phản xạ (yếu)", "currentColor", 14, "middle", "600")
b += text(Rr[0] + 8, Rr[1] + 2, "tia khúc xạ", LIGHT, 15, "start", "700")
b += sub(28, 140, "không khí, n", "1", "currentColor", 15, "start")
b += sub(28, 280, "nước, n", "2", BLUE, 15, "start")
fig1 = wrap("0 14 400 284", "Tia sáng từ không khí tới mặt nước tại điểm I: góc tới i và góc khúc xạ r đo so với pháp tuyến, có thêm tia phản xạ yếu",
            b, "Hình 1. Khúc xạ ở mặt không khí – nước.<br>Góc i và r đo so với pháp tuyến, không đo so với mặt nước.<br>Luôn có thêm một phần ánh sáng phản xạ.")

# ═════════ Hình 2: độ sâu biểu kiến ═════════
YS, YB = 100, 270
h = YB - YS - 10                              # S nằm trên đáy
Sp = (190, YS + h)
iw = 20.0                                     # góc trong nước (vẽ phóng to cho rõ)
ra = ASIN(NN * S(iw))
Ip = (Sp[0] + h * T(iw), YS)
hp = (Ip[0] - Sp[0]) / T(ra)
Sv = (Sp[0], YS + hp)
b = f'<rect x="20" y="{YS}" width="360" height="{YB - YS}" fill="{WATER}"/>' + line(20, YS, 380, YS, BLUE, 2)
b += line(20, YB, 380, YB, "currentColor", 2)
b += ray(Sp, (Sp[0], YS)) + ray((Sp[0], YS), (Sp[0], 26), LIGHT, 2.6, 1, .5)
b += ray(Sp, Ip) + ray(Ip, go(Ip, -90 + ra, 76))
b += dash(Ip, Sv, LIGHT, 1.8, .9) + dash((Ip[0], 36), (Ip[0], 182))
E = go(Ip, -90 + ra, 76)
b += f'<ellipse cx="{E[0] + 10:.1f}" cy="{E[1] - 8:.1f}" rx="13" ry="7" fill="none" stroke="currentColor" stroke-width="1.8"/>'
b += f'<circle cx="{E[0] + 10:.1f}" cy="{E[1] - 8:.1f}" r="3" fill="currentColor"/>' + text(E[0] + 28, E[1] - 3, "mắt", "currentColor", 15, "start", "700")
b += f'<circle cx="{Sp[0]}" cy="{Sp[1]:.1f}" r="5" fill="{ORG}"/>' + lab((Sp[0] + 16, Sp[1] - 6), "S", ORG, 15, "start")
b += f'<circle cx="{Sv[0]}" cy="{Sv[1]:.1f}" r="4" fill="none" stroke="{ORG}" stroke-width="2"/>' + text(Sv[0] - 10, Sv[1] + 5, "S'", ORG, 15, "end", "700")
b += f'<circle cx="{Sp[0]}" cy="{YS}" r="3" fill="currentColor"/>' + lab((Sp[0] - 12, YS - 8), "H", "currentColor", 15, "end")
b += lab((Ip[0] + 6, YS - 10), "I", "currentColor", 15, "start")
b += dim(70, YS, Sp[1]) + lab((60, (YS + Sp[1]) / 2 + 5), "h", "currentColor", 15, "end")
b += dim(118, YS, Sv[1]) + lab((128, (YS + Sv[1]) / 2 + 5), "h'", "currentColor", 15, "start")
b += dash((70, Sp[1]), (Sp[0], Sp[1]), "currentColor", 1, .5) + dash((118, Sv[1]), (Sv[0], Sv[1]), "currentColor", 1, .5)
b += text(372, YB - 10, "đáy", "currentColor", 15, "end", "600") + text(372, YS + 22, "nước", BLUE, 15, "end", "700")
fig2 = wrap("0 4 400 278", "Vật S ở đáy nước, tia từ S ló ra mặt nước tại I lệch xa pháp tuyến tới mắt; đường kéo dài nét đứt gặp đường thẳng đứng qua S tại ảnh S' nông hơn",
            b, "Hình 2. Mắt nhìn thấy S tại ảnh S', nông hơn vật thật.<br>Góc vẽ phóng to cho dễ nhìn.<br>Tia ló kéo dài ngược (nét đứt) đi qua S'.")

# ═════════ Hình 3: bản mặt song song ═════════
Y1, Y2 = 110, 196
i3 = 50.0
r3 = ASIN(S(i3) / 1.5)
I3 = (140, Y1)
J3 = (I3[0] + (Y2 - Y1) * T(r3), Y2)
P0 = (I3[0] - 120 * S(i3), I3[1] - 120 * math.cos(math.radians(i3)))
Q3 = (J3[0] + 100 * S(i3), J3[1] + 100 * math.cos(math.radians(i3)))
Xt = (I3[0] + 180 * S(i3), I3[1] + 180 * math.cos(math.radians(i3)))   # kéo dài tia tới (không có kính)
b = f'<rect x="20" y="{Y1}" width="360" height="{Y2 - Y1}" fill="{GLASS}" stroke="currentColor" stroke-width="2"/>'
b += dash((I3[0], 30), (I3[0], 176)) + dash((J3[0], 128), (J3[0], 278))
b += ray(P0, I3) + ray(I3, J3) + ray(J3, Q3)
b += dash(I3, Xt, LIGHT, 1.8, .8)
# độ dời ngang d: đoạn vuông góc giữa đường kéo dài tia tới và tia ló
ux, uy = S(i3), math.cos(math.radians(i3))
t = (J3[0] - I3[0]) * ux + (J3[1] - I3[1]) * uy
F = (I3[0] + t * ux, I3[1] + t * uy)               # chân vuông góc từ J xuống đường kéo dài
off = 60
Fa, Ja = (F[0] + off * ux, F[1] + off * uy), (J3[0] + off * ux, J3[1] + off * uy)
b += line(Fa[0], Fa[1], Ja[0], Ja[1], "currentColor", 1.4)
b += chevron(Fa[0], Fa[1], Fa[0] - Ja[0], Fa[1] - Ja[1], "currentColor", 1.4, 8) + chevron(Ja[0], Ja[1], Ja[0] - Fa[0], Ja[1] - Fa[1], "currentColor", 1.4, 8)
b += lab(((Fa[0] + Ja[0]) / 2 + 22, (Fa[1] + Ja[1]) / 2 + 10), "d")
b += arc(I3, -90, -90 - i3, 36) + lab(go(I3, -115, 50), "i")
b += arc(I3, 90, 90 - r3, 46) + lab(go(I3, 76, 62), "r")
b += lab((I3[0] + 14, Y1 - 8), "I") + lab((J3[0] - 12, Y2 + 20), "J")
b += dim(360, Y1, Y2) + lab((350, (Y1 + Y2) / 2 + 5), "e", "currentColor", 15, "end")
b += text(30, Y2 - 12, "kính, n", "currentColor", 15, "start", "700")
b += text(Q3[0] + 6, Q3[1] + 4, "tia ló", LIGHT, 15, "start", "700")
fig3 = wrap("0 18 400 276", "Tia sáng qua tấm kính hai mặt song song dày e: tia ló song song với tia tới, chỉ dời ngang một đoạn d so với đường kéo dài của tia tới",
            b, "Hình 3. Bản mặt song song.<br>Tia ló song song tia tới.<br>Nét đứt cam: đường tia sẽ đi nếu không có kính.<br>d: độ dời ngang.")

# ═════════ Hình 4: phản xạ toàn phần, vùng sáng tròn ═════════
YS4, YB4 = 160, 272
h4 = YB4 - YS4 - 10
S4 = (200, YS4 + h4)
G = ASIN(1 / NN)
b = f'<rect x="10" y="{YS4}" width="380" height="{YB4 - YS4}" fill="{WATER}"/>' + line(10, YS4, 390, YS4, BLUE, 2)
b += line(10, YB4, 390, YB4, "currentColor", 2)
# vùng sáng trên mặt nước
xl, xr = S4[0] - h4 * T(G), S4[0] + h4 * T(G)
b += line(xl, YS4, xr, YS4, "#facc15", 6, "", .85)
# (1) i nhỏ, sang trái: khúc xạ ra ngoài
i1 = 22.0
P1 = (S4[0] - h4 * T(i1), YS4)
b += ray(S4, P1) + ray(P1, go(P1, -90 - ASIN(NN * S(i1)), 96))
b += lab((P1[0] - 30, P1[1] - 70), "(1)")
# (2) i = i_gh, sang trái: tia ló đi là là mặt nước
P2 = (xl, YS4)
b += ray(S4, P2) + ray(P2, (22, YS4 - 3), LIGHT, 2.6, 1, .6)
b += dash((P2[0], YS4 - 70), (P2[0], YB4 - 4))
b += arc(P2, 90, 90 - G, 40) + sub(P2[0] + 8, P2[1] + 58, "i", "gh", "currentColor", 15, "start")
b += lab((P2[0] - 26, YS4 - 12), "(2)")
# (3) i > i_gh, sang phải: phản xạ toàn phần
i3b = 56.0
P3 = (S4[0] + h4 * T(i3b), YS4)
b += ray(S4, P3) + ray(P3, go(P3, 90 - i3b, 52))
b += dash((P3[0], YS4 - 50), (P3[0], YB4 - 4))
b += lab((P3[0] + 10, YS4 - 12), "(3)", "currentColor", 15, "start")
b += f'<circle cx="{S4[0]}" cy="{S4[1]}" r="5" fill="{ORG}"/>' + lab((S4[0], S4[1] + 22), "S", ORG)
# bán kính R
b += line(S4[0], YS4 - 26, xr, YS4 - 26, "currentColor", 1.4) + chevron(xr, YS4 - 26, 1, 0, "currentColor", 1.4, 8)
b += dash((S4[0], YS4 - 32), (S4[0], S4[1]), "currentColor", 1.2, .6)
b += lab(((S4[0] + xr) / 2, YS4 - 34), "R")
b += text(380, YS4 - 52, "vùng sáng", "#ca8a04", 15, "end", "700")
b += text(380, YB4 - 10, "nước", BLUE, 15, "end", "700")
b += dim(34, YS4, S4[1]) + text(42, (YS4 + S4[1]) / 2 + 5, "h", "currentColor", 15, "start", "700")
fig4 = wrap("0 40 400 252", "Nguồn sáng S ở đáy nước: tia 1 góc tới nhỏ ló ra ngoài, tia 2 tới với góc giới hạn ló ra đi là là mặt nước, tia 3 góc tới lớn hơn bị phản xạ toàn phần; trên mặt nước có vùng sáng tròn bán kính R",
            b, "Hình 4. Nguồn S ở đáy nước, độ sâu h.<br>(1) i nhỏ: khúc xạ ra ngoài.<br>(2) i = i<sub>gh</sub>: tia ló đi là là mặt nước.<br>(3) i &gt; i<sub>gh</sub>: phản xạ toàn phần.<br>Chỉ vùng tròn bán kính R có ánh sáng ló ra.")

# ═════════ Hình 5 & 6: lăng kính, tia tới vuông góc mặt AB ═════════
AP = 36.0                                      # góc chiết quang dùng để vẽ (không trùng bài nào)


def prism(Ax=120, Ay=34, Yb=282):
    A_ = (Ax, Ay); B_ = (Ax, Yb); C_ = (Ax + (Yb - Ay) * T(AP), Yb)
    s = f'<path d="M{A_[0]},{A_[1]} L{B_[0]},{B_[1]} L{C_[0]:.1f},{C_[1]} Z" fill="{GLASS}" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'
    s += lab((A_[0] - 10, A_[1] + 4), "A", "currentColor", 15, "end") + lab((B_[0] - 10, B_[1] + 4), "B", "currentColor", 15, "end")
    s += lab((C_[0] + 10, C_[1] + 4), "C", "currentColor", 15, "start")
    return s, A_


YR = 196
b, A5 = prism()
b += arc(A5, 90, 90 - AP, 40) + lab(go(A5, 90 - AP / 2, 56), "A", "currentColor", 14)
I5 = (A5[0], YR)
J5 = (A5[0] + (YR - A5[1]) * T(AP), YR)
r2 = ASIN(1.5 * S(AP))
D5 = r2 - AP
b += ray((20, YR), I5) + ray(I5, J5)
out = go(J5, D5, 120)
b += ray(J5, out)
# pháp tuyến tại J (vuông góc AC), hướng ra ngoài: góc -AP so với phương ngang
b += dash(go(J5, -AP, 70), go(J5, 180 - AP, 60))
b += dash(J5, go(J5, 0, 110), LIGHT, 1.6, .8)                 # kéo dài tia tới
b += arc(J5, 180 - AP, 180, 32) + sub(J5[0] - 44, J5[1] - 8, "i", "2", "currentColor", 15, "middle")
b += arc(J5, -AP, D5, 50) + sub(go(J5, -20, 66)[0] + 4, go(J5, -20, 66)[1] + 2, "r", "2", "currentColor", 15, "start")
b += arc(J5, 0, D5, 92, RED) + lab((go(J5, D5 / 2, 104)[0] + 6, go(J5, D5 / 2, 104)[1] + 6), "D", RED, 15, "start")
b += lab((I5[0] + 12, I5[1] - 10), "I", "currentColor", 15, "start") + lab((J5[0] + 24, J5[1] + 34), "J", "currentColor", 15, "start")
b += text(24, YR - 12, "tia tới ⊥ AB", LIGHT, 15, "start", "700")
NP = go(J5, -AP, 70)
b += text(NP[0] - 4, NP[1] - 8, "pháp tuyến", "currentColor", 14, "middle", "600")
fig5 = wrap("0 20 400 290", "Lăng kính ABC, tia tới vuông góc mặt AB đi thẳng tới mặt AC tại J với góc tới i2 bằng góc chiết quang A, ló ra với góc r2, lệch về phía đáy một góc D so với phương tia tới",
            b, "Hình 5. Tia tới vuông góc mặt AB.<br>Ở AB: đi thẳng, không lệch.<br>Ở AC: góc tới i<sub>2</sub> bằng góc chiết quang A.<br>D: góc lệch, tia ló lệch về phía đáy BC.")

b, A6 = prism()
I6 = (A6[0], YR)
J6 = (A6[0] + (YR - A6[1]) * T(AP), YR)
b += line(20, YR, I6[0], YR, "currentColor", 4.4) + chevron(70, YR, 1, 0, "currentColor", 2.4, 11)
b += line(I6[0], YR, J6[0], YR, "currentColor", 3.4, "", .8)
cols = [(RED, 0.0), (ORG, 0.25), ("#facc15", 0.45), (GRN, 0.6), (BLUE, 0.8), (VIO, 1.0)]
XS = 352
for c, f in cols:                          # góc tách vẽ phóng to
    ang = D5 - 6 + 12 * f
    end = (XS, J6[1] + (XS - J6[0]) * T(ang))
    b += line(J6[0], J6[1], end[0], end[1], c, 2.4)
b += line(XS, 226, XS, 296, "currentColor", 3)
yd = J6[1] + (XS - J6[0]) * T(D5 - 6); yt = J6[1] + (XS - J6[0]) * T(D5 + 6)
b += text(XS + 8, yd + 5, "đỏ", RED, 15, "start", "700") + text(XS + 8, yt + 5, "tím", VIO, 15, "start", "700")
b += text(24, YR - 14, "ánh sáng trắng", "currentColor", 15, "start", "700")
b += text(XS, 216, "màn", "currentColor", 15, "middle", "600")
fig6 = wrap("0 20 400 296", "Chùm ánh sáng trắng tới vuông góc mặt AB của lăng kính, ló ra ở mặt AC tách thành dải màu, tia đỏ lệch ít nhất ở phía trên, tia tím lệch nhiều nhất ở phía dưới, gần đáy",
            b, "Hình 6. Tán sắc qua lăng kính (góc tách vẽ phóng to).<br>Đỏ lệch ít nhất, gần đỉnh A.<br>Tím lệch nhiều nhất, gần đáy BC.")

# ═════════ ghi theory.html ═════════
src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4, fig5, fig6), 1):
    assert f"<!--FIG{n}-->" in src, n
    src = src.replace(f"<!--FIG{n}-->", f)
src = src.replace("__PHUT__", str(PHUT))
assert "<!--FIG" not in src and "__PHUT__" not in src
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
