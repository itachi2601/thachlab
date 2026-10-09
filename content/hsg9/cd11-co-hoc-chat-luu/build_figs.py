"""Sinh 4 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd11-co-hoc-chat-luu/build_figs.py
Thứ tự hình theo thứ tự xuất hiện trong bài: 1 bình loe/trụ/thóp, 2 ống Torricelli, 3 ống chữ U, 4 lực liên kết."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron, vec_luc

GREY = "rgba(148,163,184,.40)"
WATER = "rgba(56,189,248,.30)"
OIL = "rgba(251,146,60,.38)"

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def path(d, c="currentColor", w=2.4, dash="", fill="none"):
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{w}"{dd} stroke-linejoin="round"/>'

def poly(pts, fill):
    return '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="{fill}" stroke="none"/>'

def sub(main, s, c="currentColor", x=0, y=0, size=14, anchor="start", rest=""):
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="600" text-anchor="{anchor}">{main}'
            f'<tspan baseline-shift="sub" font-size="{size-3}">{s}</tspan>{rest}</text>')

def dim_v(x, y1, y2, c="currentColor", w=1.6):
    """Mũi tên hai đầu thẳng đứng từ y1 (trên) tới y2 (dưới)."""
    return line(x, y1, x, y2, c, w) + chevron(x, y1, 0, -1, c, w, 8) + chevron(x, y2, 0, 1, c, w, 8)

# ---------- Hình 1: bình trụ / loe / thóp, cùng đáy S, cùng h ----------
top, wl, bot = 30, 60, 150          # miệng, mặt nước, đáy
b = line(20, wl, 420, wl, "currentColor", 1.2, "3 4", .55)
b += dim_v(26, wl, bot) + text(6, 110, "h", BLUE, 15, "start", "700")
# trụ
b += poly([(40, wl), (100, wl), (100, bot), (40, bot)], WATER) + path(f"M40,{top} V{bot} H100 V{top}", "currentColor", 2.6)
# loe miệng (miệng 160..280 ở y=top, đáy 190..250)
xl = lambda y: 160 + (y - top) / (bot - top) * 30
b += poly([(xl(wl), wl), (280 - (xl(wl) - 160), wl), (250, bot), (190, bot)], WATER)
b += path(f"M160,{top} L190,{bot} H250 L280,{top}", "currentColor", 2.6)
# thóp miệng (miệng 360..380 ở y=top, đáy 340..400)
xt = lambda y: 360 - (y - top) / (bot - top) * 20
b += poly([(xt(wl), wl), (380 + (360 - xt(wl)), wl), (400, bot), (340, bot)], WATER)
b += path(f"M360,{top} L340,{bot} H400 L380,{top}", "currentColor", 2.6)
b += text(70, 176, "Bình trụ", "currentColor", 14, "middle", "700")
b += text(220, 176, "Bình loe miệng", "currentColor", 14, "middle", "700")
b += text(370, 176, "Bình thóp miệng", "currentColor", 14, "middle", "700")
b += sub("F = P", "cl", GRN, 70, 198, 14, "middle")
b += sub("F &lt; P", "cl", GRN, 220, 198, 14, "middle")
b += sub("F &gt; P", "cl", GRN, 370, 198, 14, "middle")
b += text(220, 226, "Cả ba có cùng d, h, S nên cùng F = d·h·S", "currentColor", 14, "middle", "600")
fig1 = wrap("0 0 440 236", "Ba bình cùng diện tích đáy và cùng mức nước: áp lực lên đáy bằng nhau",
            b, "Hình 1. Ba bình cùng diện tích đáy S và cùng mức nước h: áp lực lên đáy như nhau, còn trọng lượng nước chứa trong bình thì khác nhau.")
# kiểm: đáy ba bình bằng nhau
assert 100 - 40 == 250 - 190 == 400 - 340

# ---------- Hình 2: ống Torricelli đứng và nghiêng ----------
SURF, K = 250, 2.0            # mặt thuỷ ngân trong chậu (y), px mỗi cm
H76 = 76 * K                  # 152 px
YTOP = SURF - H76             # 98
b = poly([(40, SURF), (290, SURF), (290, 282), (40, 282)], GREY)
b += path("M40,236 V282 H290 V236", "currentColor", 2.6)
b += line(40, SURF, 290, SURF, "currentColor", 1.6)
# ống đứng
b += poly([(110, YTOP), (130, YTOP), (130, 272), (110, 272)], GREY)
b += path("M110,272 V60 H130 V272", "currentColor", 2.6)
b += line(110, YTOP, 130, YTOP, "currentColor", 1.6)
# ống nghiêng 30° so với phương thẳng đứng; mặt thuỷ ngân trong ống nằm ngang
S0 = (190.0, float(SURF)); ang = math.radians(30)
u = (math.sin(ang), -math.cos(ang)); n = (math.cos(ang), math.sin(ang))
def wall(sgn, t):
    return (S0[0] + t * u[0] + sgn * 10 * n[0], S0[1] + t * u[1] + sgn * 10 * n[1])
def t_at_y(sgn, y):
    # (S0y + t*u_y + sgn*10*n_y) = y
    return (y - S0[1] - sgn * 10 * n[1]) / u[1]
tl_, tr_ = t_at_y(-1, YTOP), t_at_y(1, YTOP)
pl, pr = wall(-1, tl_), wall(1, tr_)
assert abs(pl[1] - YTOP) < 1e-6 and abs(pr[1] - YTOP) < 1e-6
bl, br = wall(-1, -20), wall(1, -20)
tl2, tr2 = wall(-1, 220), wall(1, 220)
b += poly([pl, pr, br, bl], GREY)
b += path(f"M{bl[0]:.1f},{bl[1]:.1f} L{tl2[0]:.1f},{tl2[1]:.1f} L{tr2[0]:.1f},{tr2[1]:.1f} L{br[0]:.1f},{br[1]:.1f}", "currentColor", 2.6)
b += line(pl[0], pl[1], pr[0], pr[1], "currentColor", 1.6)
# kích thước 76 cm (chiều cao thẳng đứng)
b += line(134, YTOP, 336, YTOP, "currentColor", 1.2, "3 4", .55) + line(290, SURF, 336, SURF, "currentColor", 1.2, "3 4", .55)
b += dim_v(330, YTOP, SURF, GRN, 1.8)
b += text(338, 178, "76 cm", GRN, 15, "start", "700")
b += text(142, 82, "chân không", "currentColor", 14, "start", "600")
b += text(120, 48, "ống đứng", "currentColor", 14, "middle", "700") + text(300, 48, "ống nghiêng", "currentColor", 14, "middle", "700")
for ax in (56, 252):
    b += line(ax, 212, ax, 244, RED, 2.6) + chevron(ax, 246, 0, 1, RED, 2.6, 10)
    b += sub("p", "0", RED, ax + 8, 232, 15, "start")
b += text(250, 275, "thuỷ ngân", "currentColor", 14, "middle", "600")
fig2 = wrap("0 0 440 292", "Ống Torricelli đứng và nghiêng: cột thuỷ ngân cao 76 cm theo phương thẳng đứng",
            b, "Hình 2. Ống Torricelli: ống đứng và ống nghiêng đều giữ cột thuỷ ngân cao 76 cm theo phương thẳng đứng.")
assert abs((SURF - YTOP) / K - 76) < 1e-9

# ---------- Hình 3: ống chữ U, dầu và nước ----------
PX = 5.0                            # px mỗi cm
hd, hn = 20.0, 16.0
assert abs(800 * hd - 1000 * hn) < 1e-9
YI = 150                            # mặt phẳng chuẩn (mặt phân cách bên trái)
YD, YW = YI - hd * PX, YI - hn * PX # 50, 70
L0, L1, R0, R1, CH_TOP, CH_BOT = 100, 150, 280, 330, 190, 226
b = path(f"M{L0},{YI} H{L1} V{CH_TOP} H{R0} V{YW} H{R1} V198 Q{R1},{CH_BOT} {R1-28},{CH_BOT} H{L0+28} Q{L0},{CH_BOT} {L0},198 Z", "none", 0, fill=WATER)
b += poly([(L0, YD), (L1, YD), (L1, YI), (L0, YI)], OIL)
b += path(f"M{L0},40 V198 Q{L0},{CH_BOT} {L0+28},{CH_BOT} H{R1-28} Q{R1},{CH_BOT} {R1},198 V40", "currentColor", 2.6)
b += path(f"M{L1},40 V{CH_TOP} H{R0} V40", "currentColor", 2.6)
b += line(L0 - 6, YI, R1 + 6, YI, "currentColor", 1.4, "5 4", .8)
b += text((L1 + R0) / 2, YI - 8, "mặt phẳng chuẩn", "currentColor", 14, "middle", "600")
b += f'<circle cx="{(L0+L1)/2}" cy="{YI}" r="4.5" fill="currentColor"/><circle cx="{(R0+R1)/2}" cy="{YI}" r="4.5" fill="currentColor"/>'
b += text((L0 + L1) / 2 - 12, YI + 22, "A", "currentColor", 15, "end", "700") + text((R0 + R1) / 2 + 12, YI + 22, "B", "currentColor", 15, "start", "700")
b += text((L0 + L1) / 2, 104, "dầu", ORG, 15, "middle", "700")
b += text((L1 + R0) / 2, 214, "nước", BLUE, 15, "middle", "700")
# h_d (trái) và h_n (phải)
b += dim_v(86, YD, YI, ORG, 1.8) + sub("h", "d", ORG, 80, 104, 15, "end", " = 20 cm")
b += dim_v(344, YW, YI, BLUE, 1.8) + sub("h", "n", BLUE, 352, 114, 15, "start", " = 16 cm")
# chênh lệch mặt thoáng
b += line(R0, YD, 358, YD, "currentColor", 1.2, "3 4", .6)
b += dim_v(358, YD, YW, "currentColor", 1.6) + text(366, 66, "Δh = 4 cm", "currentColor", 14, "start", "600")
fig3 = wrap("0 0 440 244", "Ống chữ U chứa nước và dầu: cột dầu cao 20 cm cân bằng cột nước cao 16 cm",
            b, "Hình 3. Ống chữ U: cột dầu cao 20 cm (bên trái) cân bằng cột nước cao 16 cm (bên phải) so với mặt phẳng chuẩn.")

# ---------- Hình 4: nổi tự do / dây giữ chìm / treo lực kế ----------
KF = 8.0                            # px mỗi N, chung cho mọi vectơ trong hình
top4, bot4 = 36, 200
panels = [(10, "Nổi tự do"), (160, "Dây giữ dưới đáy"), (310, "Treo lực kế")]
b = ""
for x0, name in panels:
    b += path(f"M{x0},{top4} V{bot4} H{x0+120} V{top4}", "currentColor", 2.4)
def water(x0, lvl):
    return poly([(x0, lvl), (x0 + 120, lvl), (x0 + 120, bot4), (x0, bot4)], WATER)
BLK = 'fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="2.2"'
# (a) khối nhựa 1000 cm³, D = 600: P = 6 N = F_A, chìm 60%
x0 = 10; xc = x0 + 60; wl_a = 100
b += water(x0, wl_a)
b += f'<rect x="{xc-25}" y="76" width="50" height="60" {BLK}/>'
assert abs((136 - wl_a) / 60 - 0.6) < 1e-9
P, FA = 6.0, 6.0
s_, _ = vec_luc("r", xc, 106, 0, 1, P, KF); b += s_
s_, _ = vec_luc("b", xc, 106, 0, -1, FA, KF); b += s_
b += text(xc + 8, 156, "P", RED, 15, "start", "700") + sub("F", "A", BLUE, xc + 8, 64, 15)
b += text(xc, 226, "Nổi tự do", "currentColor", 14, "middle", "700")
b += sub("P = F", "A", "currentColor", xc, 246, 14, "middle")
b += text(xc, 266, "6 N = 6 N", "currentColor", 14, "middle", "600")
# (b) cùng khối nhựa, chìm hẳn, dây buộc đáy: F_A = P + T
x0 = 160; xc = x0 + 60; wl_b = 80
b += water(x0, wl_b)
b += line(xc, 160, xc, bot4, "currentColor", 1.4)
b += f'<rect x="{xc-25}" y="100" width="50" height="60" {BLK}/>'
P, FA, T = 6.0, 10.0, 4.0
assert abs(FA - P - T) < 1e-9
s_, _ = vec_luc("r", xc - 12, 130, 0, 1, P, KF); b += s_
s_, _ = vec_luc("b", xc + 12, 130, 0, -1, FA, KF); b += s_
s_, _ = vec_luc("o", xc, 160, 0, 1, T, KF); b += s_
b += text(xc - 16, 182, "P", RED, 15, "end", "700") + sub("F", "A", BLUE, xc + 18, 56, 15) + text(xc + 8, 194, "T", ORG, 15, "start", "700")
b += text(xc, 226, "Dây giữ dưới đáy", "currentColor", 14, "middle", "700")
b += sub("F", "A", "currentColor", xc, 246, 14, "middle", " = P + T")
b += text(xc, 266, "10 = 6 + 4 (N)", "currentColor", 14, "middle", "600")
# (c) vật 4,5 N treo lực kế: P = F_A + T
x0 = 310; xc = x0 + 60; wl_c = 80
b += water(x0, wl_c)
b += f'<rect x="{xc-22}" y="4" width="44" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="2"/>'
b += text(xc, 20, "lực kế", "currentColor", 13, "middle", "600")
b += line(xc, 26, xc, 105, "currentColor", 1.4)
b += f'<rect x="{xc-25}" y="105" width="50" height="50" {BLK}/>'
P, FA, T = 4.5, 1.5, 3.0
assert abs(P - FA - T) < 1e-9
s_, _ = vec_luc("r", xc, 130, 0, 1, P, KF); b += s_
s_, _ = vec_luc("b", xc + 14, 130, 0, -1, FA, KF); b += s_
s_, _ = vec_luc("o", xc - 14, 130, 0, -1, T, KF); b += s_
b += text(xc + 8, 172, "P", RED, 15, "start", "700") + sub("F", "A", BLUE, xc + 32, 124, 15) + text(xc - 30, 112, "T", ORG, 15, "end", "700")
b += text(xc, 226, "Treo lực kế", "currentColor", 14, "middle", "700")
b += sub("P = F", "A", "currentColor", xc, 246, 14, "middle", " + T")
b += text(xc, 266, "4,5 = 1,5 + 3 (N)", "currentColor", 14, "middle", "600")
fig4 = wrap("0 0 440 276", "Ba trường hợp vật trong chất lỏng: nổi tự do, bị dây giữ chìm, treo lực kế",
            b, "Hình 4. Khối nhựa 1000 cm³ (P = 6 N) nổi và bị dây giữ chìm; vật 4,5 N treo lực kế. Cùng tỉ lệ 8 px cho 1 N.")

src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in ((1, fig1), (2, fig2), (3, fig3), (4, fig4)):
    assert f"<!--FIG{n}-->" in src, n
    src = src.replace(f"<!--FIG{n}-->", f)
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
