"""Sinh 4 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Vectơ lực vẽ TỈ LỆ độ lớn bằng svg_lib.vec_luc (một hệ số k px/N cho mỗi hình), đầu mũi tên chữ V 30°.
Chạy: python3 content/hsg9/cd10-luc/build_figs.py"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron, vec_luc

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def sub(main, s, c="currentColor", x=0, y=0, size=16, anchor="start"):
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">{main}'
            f'<tspan baseline-shift="sub" font-size="{size-3}">{s}</tspan></text>')

def arc(cx, cy, r, a0, a1, c="currentColor", w=1.8):
    """Cung tròn tâm (cx,cy), bán kính r, từ góc a0 đến a1 (độ, ngược chiều kim đồng hồ trên màn hình = y lên)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
    return f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 0 0 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>'

# ---------- Hình 1: tổng hợp 50 N và 30 N hợp 60° bằng quy tắc hình bình hành (k = 2,4 px/N) ----------
F1, F2, ALPHA, K1 = 50, 30, 60, 2.4
R = math.sqrt(F1**2 + F2**2 + 2 * F1 * F2 * math.cos(math.radians(ALPHA)))
assert abs(R - 70) < 1e-9
ox, oy = 90, 180
a = math.radians(ALPHA)
s1, t1 = vec_luc("r", ox, oy, 1, 0, F1, K1)
s2, t2 = vec_luc("b", ox, oy, math.cos(a), -math.sin(a), F2, K1)
phi = math.degrees(math.atan2(F2 * math.sin(a), F1 + F2 * math.cos(a)))
sR, tR = vec_luc("g", ox, oy, math.cos(math.radians(phi)), -math.sin(math.radians(phi)), R, K1)
assert abs(tR[0] - (t1[0] + t2[0] - ox)) < 0.1 and abs(tR[1] - (t1[1] + t2[1] - oy)) < 0.1   # R = F1 + F2 (cùng gốc)
b = line(t1[0], t1[1], tR[0], tR[1], "currentColor", 1.6, "5 4", .7) + line(t2[0], t2[1], tR[0], tR[1], "currentColor", 1.6, "5 4", .7)
b += s1 + s2 + sR
b += f'<circle cx="{ox}" cy="{oy}" r="4" fill="currentColor"/>'
b += arc(ox, oy, 36, 0, ALPHA) + text(ox + 42, oy - 14, "α", "currentColor", 17, "start", "700")
b += sub("F", "1", RED, t1[0] - 8, t1[1] + 22, 17, "middle")
b += sub("F", "2", BLUE, t2[0] - 14, t2[1] - 4, 17, "end")
b += text(tR[0] + 8, tR[1] + 6, "R", GRN, 18, "start", "700")
b += text(250, 40, "Cùng gốc O,", "currentColor", 15, "start", "400")
b += text(250, 60, "đường chéo là hợp lực R", "currentColor", 15, "start", "400")
fig1 = wrap("0 0 440 218", "Quy tắc hình bình hành: lực 50 N và 30 N hợp góc 60 độ có hợp lực 70 N",
            b, "Hình 1. Hai lực F₁ = 50 N, F₂ = 30 N hợp góc α = 60° (1 N ứng 2,4 px). Đường chéo hình bình hành dài 168 px, tức R = 70 N.")

# ---------- Hình 2: vật 100 N treo bằng hai dây vuông góc (k = 0,9 px/N) ----------
K2, P2 = 0.9, 100
T2 = P2 / (2 * math.cos(math.radians(45)))
ox, oy = 220, 150
sP, tP = vec_luc("r", ox, oy, 0, 1, P2, K2)
sT1, tT1 = vec_luc("b", ox, oy, -1, -1, T2, K2)
sT2, tT2 = vec_luc("b", ox, oy, 1, -1, T2, K2)
tS = (ox, oy - K2 * P2)                       # tổng hai lực căng = -P (đối với P)
assert abs((oy - tT1[1]) * 2 - K2 * P2) < 0.2   # 2·T·cos45° = P (thành phần đứng của hai dây)
ceil = 45
b = line(100, ceil, 340, ceil, "currentColor", 3)
for x in range(104, 340, 16):
    b += line(x, ceil, x - 9, ceil - 10, "currentColor", 1.4, "", .6)
b += line(ox - 105, ceil, ox, oy, "currentColor", 1.2, "", .5) + line(ox + 105, ceil, ox, oy, "currentColor", 1.2, "", .5)
b += line(tT1[0], tT1[1], tS[0], tS[1], "currentColor", 1.6, "5 4", .7) + line(tT2[0], tT2[1], tS[0], tS[1], "currentColor", 1.6, "5 4", .7)
b += line(ox, oy, tS[0], tS[1], GRN, 2.4, "5 4")
b += chevron(tS[0], tS[1], 0, -1, GRN, 2.4, 11)
b += sT1 + sT2 + sP + f'<circle cx="{ox}" cy="{oy}" r="4" fill="currentColor"/>'
b += sub("T", "1", BLUE, tT1[0] - 6, tT1[1] + 22, 17, "end") + sub("T", "2", BLUE, tT2[0] + 6, tT2[1] + 22, 17, "start")
b += text(ox + 10, tP[1] - 4, "P", RED, 18, "start", "700")
b += text(300, 108, "T₁ + T₂ = −P", GRN, 16, "start", "700")
fig2 = wrap("0 0 440 262", "Vật nặng 100 N treo bằng hai dây vuông góc: tổng hai lực căng cân bằng với trọng lượng",
            b, "Hình 2. Vật 100 N treo bằng hai dây hợp góc 90° (1 N ứng 0,9 px). Hai lực căng mỗi dây 70,7 N có đường chéo bằng P.")

# ---------- Hình 3: vật 10 kg đứng yên trên dốc 30° (k = 0,9 px/N) ----------
K3, P3, AL = 0.9, 100.0, 30
al = math.radians(AL)
bx0, by0, bx1 = 40, 225, 360
top = (bx1, by0 - (bx1 - bx0) * math.tan(al))
u = (math.cos(al), -math.sin(al))               # dọc dốc, hướng LÊN dốc
n = (-math.sin(al), -math.cos(al))              # pháp tuyến hướng ra ngoài dốc
t = 0.46
px, py = bx0 + (bx1 - bx0) * t, by0 - (bx1 - bx0) * t * math.tan(al)
cx, cy = px + n[0] * 13, py + n[1] * 13
b = line(bx0, by0, bx1, by0, "currentColor", 2.6) + line(bx1, by0, bx1, top[1], "currentColor", 2.6) + line(bx0, by0, top[0], top[1], "currentColor", 2.6)
b += (f'<rect x="{cx-20:.1f}" y="{cy-13:.1f}" width="40" height="26" rx="2" fill="rgba(148,163,184,.3)" stroke="currentColor" '
      f'stroke-width="2" transform="rotate({-AL} {cx:.1f} {cy:.1f})"/>')
Nn, Fms = P3 * math.cos(al), P3 * math.sin(al)
sPp, tPp = vec_luc("r", cx, cy, 0, 1, P3, K3)
sN, tN = vec_luc("b", cx, cy, n[0], n[1], Nn, K3)
sF, tF = vec_luc("o", cx, cy, u[0], u[1], Fms, K3)
sPs, tPs = vec_luc("r", cx, cy, -u[0], -u[1], Fms, K3, w=2, dash="5 4")        # P·sinα (xuống dốc)
sPc, tPc = vec_luc("r", cx, cy, -n[0], -n[1], Nn, K3, w=2, dash="5 4")         # P·cosα (ép vào dốc)
# P = P·sinα + P·cosα (vectơ)
assert abs(tPs[0] + tPc[0] - 2 * cx - (tPp[0] - cx)) < 0.2 and abs(tPs[1] + tPc[1] - 2 * cy - (tPp[1] - cy)) < 0.2
b += sPs + sPc + sN + sF + sPp + f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="currentColor"/>'
b += text(tPp[0] + 8, tPp[1] + 2, "P", RED, 18, "start", "700")
b += text(tN[0] - 6, tN[1] - 4, "N", BLUE, 18, "end", "700")
b += sub("F", "msn", ORG, tF[0] + 6, tF[1] - 14, 17, "start")
b += sub("P sin α", "", RED, tPs[0] - 6, tPs[1] + 18, 15, "end")
b += sub("P cos α", "", RED, tPc[0] + 8, tPc[1] + 8, 15, "start")
b += arc(bx0, by0, 52, 0, AL) + text(bx0 + 58, by0 - 8, "α", "currentColor", 17, "start", "700")
fig3 = wrap("0 0 440 245", "Vật 10 kg đứng yên trên mặt dốc 30 độ: P chia thành P sin α dọc dốc và P cos α ép vào dốc",
            b, "Hình 3. Vật 10 kg (P = 100 N) đứng yên trên dốc 30° (1 N ứng 0,9 px). F<sub>msn</sub> bằng P sin α = 50 N, N bằng P cos α ≈ 86,6 N.")

# ---------- Hình 4: thanh AB đồng chất 1,2 m, tựa O (k = 1,2 px/N, 1 m ứng 280 px) ----------
K4, M = 1.2, 280
xA = 50
xO, xG, xB = xA + 0.4 * M, xA + 0.6 * M, xA + 1.2 * M
yb = 150
b = f'<rect x="{xA}" y="{yb-5}" width="{xB-xA}" height="10" rx="2" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
b += f'<path d="M{xO},{yb+5} L{xO-14},{yb+34} L{xO+14},{yb+34} Z" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
sA, tA = vec_luc("r", xA, yb + 5, 0, 1, 50, K4)
sG, tG = vec_luc("r", xG, yb + 5, 0, 1, 20, K4)
sB, tB = vec_luc("o", xB, yb + 5, 0, 1, 20, K4)
sO, tO = vec_luc("b", xO, yb - 5, 0, -1, 90, K4)
b += sA + sG + sB + sO
# ΣF = 0 và ΣM quanh O = 0
assert 50 + 20 + 20 == 90 and abs(50 * 0.4 - (20 * 0.2 + 20 * 0.8)) < 1e-9
b += text(xA, tA[1] + 20, "50 N", RED, 16, "middle", "700")
b += text(xG + 6, tG[1] + 20, "20 N", RED, 16, "start", "700")
b += text(xB, tB[1] + 20, "F = 20 N", ORG, 16, "middle", "700")
b += text(xO + 10, tO[1] + 6, "N = 90 N", BLUE, 16, "start", "700")
b += text(xA, yb - 14, "A", "currentColor", 16, "middle", "700") + text(xB, yb - 14, "B", "currentColor", 16, "middle", "700")
b += text(xG, yb - 14, "G", "currentColor", 16, "middle", "700")
b += text(xO - 20, yb + 32, "O", "currentColor", 16, "end", "700")
y1, y2 = 244, 268
b += line(xA, y1, xO, y1, GRN, 2) + line(xA, y1 - 5, xA, y1 + 5, GRN, 2) + line(xO, y1 - 5, xO, y1 + 5, GRN, 2)
b += text((xA + xO) / 2, y1 - 8, "0,4 m", GRN, 15, "middle", "600")
b += line(xO, y2, xB, y2, GRN, 2) + line(xO, y2 - 5, xO, y2 + 5, GRN, 2) + line(xB, y2 - 5, xB, y2 + 5, GRN, 2)
b += text((xO + xB) / 2, y2 + 17, "0,8 m", GRN, 15, "middle", "600")
b += line(xO, y1, xG, y1, GRN, 2) + line(xG, y1 - 5, xG, y1 + 5, GRN, 2)
b += text((xO + xG) / 2, y1 - 8, "0,2 m", GRN, 15, "middle", "600")
fig4 = wrap("0 0 440 296", "Thanh đồng chất AB tựa tại O: lực 50 N ở A, trọng lượng 20 N ở G, lực F = 20 N ở B và phản lực N = 90 N",
            b, "Hình 4. Thanh nằm ngang cân bằng (1 N ứng 1,2 px). Moment quanh O: 50·0,4 = 20·0,2 + 20·0,8 = 20 N·m. Tổng lực: 50 + 20 + 20 = 90 N.")

src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for k, f in ((1, fig1), (2, fig2), (3, fig3), (4, fig4)):
    assert f"<!--FIG{k}-->" in src, k
    src = src.replace(f"<!--FIG{k}-->", f)
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
