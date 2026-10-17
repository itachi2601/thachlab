"""Bài tập mẫu CĐ17 "Thiên văn: Mặt Trăng, Hệ Mặt Trời và Ngân Hà" (lesson 178) — Dạng 4–6 (phần đọc buổi 16).
Module được build-hinh-178.py import. Dàn ý + số liệu: content/hsg9/cd17-thien-van/nguon.md mục "Bài tập mẫu" (tinh.py).
Dạng sau dùng lại cách làm dạng trước:
  D4 tháng giao hội (hiệu tốc độ góc, như hai kim đồng hồ đuổi nhau) + ngày sao + thời gian nguyệt thực toàn phần
     (dùng vùng tối của bóng Trái Đất đã tính ở D3, tốc độ tương đối theo tháng giao hội)
  D5 góc cao Mặt Trời buổi trưa h = 90° − |φ − δ|, bóng cọc, rồi phép đo Eratosthenes (góc so le trong, tỉ lệ cung)
  D6 tổng hợp Hệ Mặt Trời – Ngân Hà: t = s/c, v = 2πr/T, đổi AU – ly – km, mô hình tỉ lệ.
Topic: YCCĐ CĐ17 trong question-topics.json.
Xuất DANG, BUILD, ANALYSIS, SOLS, STEPS (3 phần tử mỗi list) và kiem_so()."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *  # noqa: F401,F403  (fig, seg, lbl, dot, poly, chevron, arrow, sol, M, P, A, buoc …)

T4, T5, T6 = "Pha Mặt Trăng, nhật thực và nguyệt thực", "Chuyển động nhìn thấy của Mặt Trời, ngày đêm và mùa", "Hệ Mặt Trời và Ngân Hà"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
SUN = "#facc15"
PI = math.pi

# ═════════════ SỐ LIỆU (mọi đáp số tính ở đây, kiem_so() kiểm lại) ═════════════
# D4
T_TV, NAM = 27.32, 365.25                    # ngày
W_M = 360 / T_TV                             # 13,177 °/ngày
W_E = 360 / NAM                              # 0,9856 °/ngày
W_D = W_M - W_E                              # 12,19 °/ngày
S4 = 360 / W_D                               # 29,53 ngày
GOC_E4 = W_E * T_TV                          # 26,9°
DT4 = GOC_E4 / W_D                           # 2,21 ngày
NGAY_SAO = 24 * 360 / (360 + W_E)            # 23,934 h
HUT4 = (24 - NGAY_SAO) * 60                  # 3,93 phút
U4, DM4, DMM4 = 9200, 3470, 384_000          # km: vùng tối bóng TĐ tại quỹ đạo Mặt Trăng; đường kính Mặt Trăng; Trái Đất – Mặt Trăng
V4 = 2 * PI * DMM4 / (S4 * 86400)            # 0,946 km/s
TTP4 = (U4 - DM4) / V4 / 60                  # 101 phút
# D5
PHI_HN, PHI_HCM, DEL = 21.0, 10.8, 23.5
hcao = lambda phi, d: 90 - abs(phi - d)
H_XP_HN = hcao(PHI_HN, 0)                    # 69,0°
H_HC_HN = hcao(PHI_HN, DEL)                  # 87,5°
H_DC_HN = hcao(PHI_HN, -DEL)                 # 45,5°
B_DC_HN = 1 / math.tan(math.radians(H_DC_HN))   # 0,983 m
H_HC_HCM = hcao(PHI_HCM, DEL)                # 77,3°
B_HC_HCM = 1 / math.tan(math.radians(H_HC_HCM))  # 0,225 m
BONG_B, S_AB = 0.0875, 556                   # m ; km
TH5 = math.degrees(math.atan(BONG_B))        # 5,00°
C5 = S_AB * 360 / TH5                        # ≈ 40 030 km
BK5 = C5 / (2 * PI)                           # ≈ 6370 km
# D6
C_AS, AU, LY = 3e5, 1.5e8, 9.46e12           # km/s ; km ; km
NAM_S = NAM * 86400
T_E6 = AU / C_AS                             # 500 s
T_N6 = 30 * AU / C_AS / 3600                 # 4,17 h
T_MA_MIN, T_MA_MAX = 0.52 * AU / C_AS / 60, 2.52 * AU / C_AS / 60   # 4,3 ; 21,0 phút
V_E6 = 2 * PI * AU / NAM_S                   # 29,9 km/s
PROX_KM = 4.24 * LY                          # 4,01·10^13 km
PROX_AU = PROX_KM / AU                       # ≈ 267 000 AU
T_TAU = PROX_KM / 17 / NAM_S                 # ≈ 74 800 năm
V_GAL = 2 * PI * 26_000 * LY / (230e6 * NAM_S)   # 213 km/s
VONG = 4.6e9 / 230e6                         # 20 vòng
MOON_CM = DMM4 * 1e5 / 1e10                  # 3,84 cm


def rich(s, size=14):
    """Nhãn SVG có chỉ số dưới 'D_{M}' và số mũ '10^{12}' → tspan dy."""
    ms = list(re.finditer(r"([_^])\{([^}]+)\}", s))
    if not ms:
        return s
    out = s[:ms[0].start()]
    for k, m in enumerate(ms):
        dy = 4 if m.group(1) == "_" else -6
        out += f'<tspan dy="{dy}" font-size="{max(12, size - 2)}">{m.group(2)}</tspan>'
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        out += f'<tspan dy="{-dy}">{s[m.end():nxt]}</tspan>' if s[m.end():nxt] else f'<tspan dy="{-dy}"></tspan>'
    return out

def txt(x, y, s, c="currentColor", size=14, anchor="start", weight="700", extra=""):
    size = max(size, 14)                                   # quy ước: nhãn ≥ 14, chỉ số ≥ 12
    t = lbl(x, y, rich(s, size), c, size, anchor, weight)
    return t.replace("<text ", f"<text {extra} ", 1) if extra else t

def show_at(t, dur):
    k = max(0.001, min(0.999, t / dur))
    return (f'<animate attributeName="opacity" values="0;1" keyTimes="0;{k:.4f}" calcMode="discrete" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')

def show_between(k0, k1, dur):
    return (f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{k0:.4f};{k1:.4f}" calcMode="discrete" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def timed(t, s, x, y, c="currentColor", size=14, anchor="start", weight="700", k1=None, dur=None):
    a = show_between(t, k1, dur) if k1 is not None else show_at(t * dur, dur)
    return txt(x, y, s, c, size, anchor, weight, 'opacity="0"').replace("</text>", a + "</text>", 1)

def anim(attr, vals, dur):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.1f}" for v in vals)}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')

def circ(x, y, r, c="currentColor", fill="none", op=1, sw=2, dash="", extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" fill-opacity="{op}" stroke="{c}" '
            f'stroke-width="{sw}"{d}{extra}/>')

def arc_m(cx, cy, r, a0, a1, c=RED, w=1.8):
    """Cung tròn, góc kiểu toán (độ, ngược kim đồng hồ, Oy lên), a0 < a1, |a1 − a0| < 180."""
    return arc(cx, cy, r, a0, a1, c, w)

def pt(cx, cy, r, a):
    return cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))

def sun(x, y, r):
    b = circ(x, y, r, ORG, SUN, .9, 2)
    for k in range(8):
        a = 45 * k
        x1, y1 = pt(x, y, r + 4, a)
        x2, y2 = pt(x, y, r + 10, a)
        b += seg(x1, y1, x2, y2, ORG, 2)
    return b


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 4 · tháng thiên văn và tháng giao hội ─────────────
SX4, SY4, RO4, RM4 = 22, 130, 290, 46          # Mặt Trời, bán kính quỹ đạo TĐ (px), quỹ đạo Mặt Trăng (px, không tỉ lệ)
A04 = -14.5                                     # góc Trái Đất lúc đầu (độ)

def d4(kk):
    b = ""
    if kk == 0:
        TT, n = 10.0, 120
        days = [S4 * i / n for i in range(n + 1)]
        aE = [A04 + W_E * t for t in days]
        E = [pt(SX4, SY4, RO4, a) for a in aE]
        Mo = [pt(ex, ey, RM4, A04 + 180 + W_M * t) for (ex, ey), t in zip(E, days)]
        b += txt(16, 22, "Nhìn từ phía Bắc: Trái Đất quanh Mặt Trời,", "currentColor", 14)
        b += txt(16, 40, "Mặt Trăng quanh Trái Đất", "currentColor", 14)
        b += sun(SX4, SY4, 16)
        orb = [pt(SX4, SY4, RO4, a) for a in [A04 - 4 + .5 * k for k in range(70)]]
        b += poly(orb, GREY, 1.6, "5 5")
        # hướng tới một ngôi sao xa: cố định, vẽ ở vị trí đầu
        e0, m0 = E[0], Mo[0]
        ux, uy = m0[0] - e0[0], m0[1] - e0[1]
        nn = math.hypot(ux, uy); ux, uy = ux / nn, uy / nn
        b += seg(e0[0], e0[1], e0[0] + 120 * ux, e0[1] + 120 * uy, GREY, 1.4, "3 4")
        b += txt(e0[0] + 124 * ux - 4, e0[1] + 124 * uy + 18, "hướng sao xa", GREY, 14, "end", "600")
        k_t = T_TV / S4
        it = round(k_t * n)
        eT = E[it]
        b += (f'<line x1="{eT[0]:.1f}" y1="{eT[1]:.1f}" x2="{eT[0] + 120 * ux:.1f}" y2="{eT[1] + 120 * uy:.1f}" stroke="{GREY}" '
              f'stroke-width="1.4" stroke-dasharray="3 4" opacity="0">{show_at(k_t * TT, TT)}</line>')
        b += (f'<circle cx="{E[0][0]:.1f}" cy="{E[0][1]:.1f}" r="{RM4}" fill="none" stroke="{GREY}" stroke-width="1.2" stroke-dasharray="2 4">'
              f'{anim("cx", [p[0] for p in E], TT)}{anim("cy", [p[1] for p in E], TT)}</circle>')
        b += (f'<circle cx="{E[0][0]:.1f}" cy="{E[0][1]:.1f}" r="10" fill="{BLUE}" stroke="currentColor" stroke-width="1.5">'
              f'{anim("cx", [p[0] for p in E], TT)}{anim("cy", [p[1] for p in E], TT)}</circle>')
        b += (f'<circle cx="{Mo[0][0]:.1f}" cy="{Mo[0][1]:.1f}" r="6" fill="{GREY}" stroke="currentColor" stroke-width="1.5">'
              f'{anim("cx", [p[0] for p in Mo], TT)}{anim("cy", [p[1] for p in Mo], TT)}</circle>')
        b += timed(0, "ngày 0: trăng non", 16, 246, BLUE, 14, "start", "700", .12, TT)
        b += timed(k_t, "ngày 27,32: Mặt Trăng về lại hướng sao,", 16, 228, ORG, 14, "start", "700", None, TT)
        b += timed(k_t, "nhưng chưa tới trăng non", 16, 246, ORG, 14, "start", "700", None, TT)
        b += timed(.995, "trăng non kế tiếp: ngày ?", 16, 264, RED, 14, "start", "700", None, TT)
        return fig("c17-4-0", "0 0 420 274", "Trái Đất đi một cung trên quỹ đạo quanh Mặt Trời, Mặt Trăng quay quanh Trái Đất từ trăng non tới trăng non kế tiếp",
                   b, "Mô phỏng: nhìn từ phía Bắc, không theo tỉ lệ khoảng cách; chạy nhanh hơn thật rất nhiều lần, không ghi tỉ lệ thời gian.")
    # hình dữ kiện: hai vị trí Trái Đất + dải vùng tối
    b += txt(16, 20, "a), b) Hai lần Mặt Trăng ở cùng hướng sao", "currentColor", 14)
    sx, sy, R = 22, 118, 270
    a1, a2 = -13.0, 14.0
    e1, e2 = pt(sx, sy, R, a1), pt(sx, sy, R, a2)
    b += sun(sx, sy, 14)
    b += seg(sx, sy, *e1, GREY, 1.4, "5 4") + seg(sx, sy, *e2, GREY, 1.4, "5 4")
    b += arc_m(sx, sy, 70, a1, a2, ORG, 2) + txt(sx + 76, sy + 5, "?", ORG, 14)
    b += circ(*e1, 9, "currentColor", BLUE, 1, 1.5) + circ(*e2, 9, "currentColor", BLUE, 1, 1.5)
    u = math.degrees(math.atan2(-(sy - e1[1]), sx - e1[0]))          # hướng E1 → Mặt Trời (góc toán)
    m1, m2 = pt(*e1, 44, u), pt(*e2, 44, u)
    b += seg(*e1, *m1, "currentColor", 1.6) + seg(*e2, *m2, "currentColor", 1.6)
    b += circ(*m1, 6, "currentColor", GREY, 1, 1.4) + circ(*m2, 6, "currentColor", GREY, 1, 1.4)
    u2 = math.degrees(math.atan2(-(sy - e2[1]), sx - e2[0])) % 360
    b += arc_m(*e2, 30, u, u2, RED, 2)
    ax, ay = pt(*e2, 40, (u + u2) / 2)
    b += txt(ax - 4, ay + 6, "?", RED, 14, "end")
    b += txt(e1[0] + 14, e1[1] + 6, "trăng non", BLUE, 14) + txt(e1[0] + 14, e1[1] + 24, "(ngày 0)", "currentColor", 14, "start", "600")
    b += txt(e2[0] + 14, e2[1] + 2, "sau T =", "currentColor", 14, "start", "600") + txt(e2[0] + 14, e2[1] + 20, "27,32 ngày", "currentColor", 14, "start", "600")
    # d) vùng tối của bóng Trái Đất
    y0, k = 236, 0.025
    w_u, r_m = U4 * k, DM4 * k / 2
    x0 = 210 - w_u / 2
    b += txt(16, 200, "d) Mặt Trăng đi xuyên tâm vùng tối", "currentColor", 14)
    b += f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w_u:.1f}" height="{2 * r_m + 12:.1f}" fill="{GREY}" fill-opacity=".35" stroke="{GREY}" stroke-width="1.6"/>'
    cy = y0 + r_m + 6
    b += circ(x0 + r_m, cy, r_m, "currentColor", "none", 1, 1.6, "5 4") + circ(x0 + w_u - r_m, cy, r_m, "currentColor", "none", 1, 1.6, "5 4")
    b += arrow("", "r", round(x0 + r_m, 1), round(cy, 1), round(x0 + w_u - r_m, 1), round(cy, 1), 2.2)
    b += txt(210, cy - 8, "v = ?", RED, 14, "middle")
    yb = y0 + 2 * r_m + 30
    b += dim("", "b", round(x0, 1), yb, round(x0 + w_u, 1), yb, "", 0, 0)
    b += txt(210, yb + 20, "vùng tối: 9200 km", BLUE, 14, "middle")
    b += txt(x0 - 6, cy + 5, "D_{M}", "currentColor", 14, "end", "600")
    b += txt(x0 + w_u + 6, cy - 14, "bắt đầu", "currentColor", 14, "start", "600") + txt(x0 + w_u + 6, cy + 4, "và hết", "currentColor", 14, "start", "600")
    b += txt(x0 + w_u + 6, cy + 22, "toàn phần", "currentColor", 14, "start", "600")
    return fig("c17-4-2", f"0 0 420 {yb + 30:.0f}", "Trên: hai vị trí Trái Đất cách nhau một tháng thiên văn, Mặt Trăng cùng chỉ một hướng sao; dưới: Mặt Trăng đi qua dải vùng tối của bóng Trái Đất",
               b, "Dữ kiện: góc hai dấu ? cần tìm (vẽ minh hoạ). Dải vùng tối và Mặt Trăng vẽ cùng tỉ lệ; hai vòng nét đứt là lúc bắt đầu và lúc hết toàn phần.")


# ───────────── Dạng 5 · góc cao Mặt Trời và Eratosthenes ─────────────
def d5(kk):
    b = ""
    if kk == 0:
        TT = 7.0
        ox, oy, r = 140, 150, 100
        b += txt(16, 22, "Trưa xuân phân: tia nắng song song tới A và B", "currentColor", 14)
        b += f'<path d="M{ox},{oy - r} A{r},{r} 0 0 1 {ox},{oy + r}" fill="{BLUE}" fill-opacity=".12" stroke="currentColor" stroke-width="2.2"/>'
        aB = 22.0                                    # góc vẽ phóng to (thật 5°)
        A_, B_ = pt(ox, oy, r, 0), pt(ox, oy, r, aB)
        tA, tB = pt(ox, oy, r + 26, 0), pt(ox, oy, r + 26, aB)
        b += seg(*A_, *tA, "currentColor", 3) + seg(*B_, *tB, "currentColor", 3)
        b += dot(*A_, 3.5) + dot(*B_, 3.5)
        b += txt(A_[0] + 4, A_[1] + 22, "A (xích đạo)", "currentColor", 14, "start", "600")
        b += txt(B_[0] - 6, B_[1] - 30, "B", "currentColor", 14, "end")
        # tia nắng tới từ bên phải (ngang), đầu tia chạy vào
        ys = [tB[1], oy - 52, oy - 20, oy, oy + 30, oy + 60]
        for k, yy in enumerate(ys):
            dx = math.sqrt(max(0, r * r - (yy - oy) ** 2))
            xe = ox + dx
            if abs(yy - tB[1]) < .1:
                xe = tB[0]
            if abs(yy - oy) < .1:
                xe = tA[0]
            x_start = 410
            b += (f'<line x1="{x_start}" y1="{yy:.1f}" x2="{x_start}" y2="{yy:.1f}" stroke="{ORG}" stroke-width="2">'
                  f'{anim("x2", [x_start, xe, xe], TT * .4)}</line>')
            if k in (0, 3):
                b += f'<g opacity="0">{chevron((x_start + xe) / 2 - 10, yy, -1, 0, ORG, 2, 10)}{show_at(.4 * TT * .9, TT)}</g>'
        # tia qua đỉnh cọc B chạm đất → bóng
        yb = tB[1]
        xg = ox + math.sqrt(r * r - (yb - oy) ** 2)
        b += (f'<line x1="{tB[0]:.1f}" y1="{yb:.1f}" x2="{xg:.1f}" y2="{yb:.1f}" stroke="{ORG}" stroke-width="2" opacity="0">'
              f'{show_at(.45 * TT, TT)}</line>')
        b += (f'<path d="M{B_[0]:.1f},{B_[1]:.1f} A{r},{r} 0 0 1 {xg:.1f},{yb:.1f}" fill="none" stroke="currentColor" stroke-width="5" '
              f'opacity="0">{show_at(.5 * TT, TT)}</path>')
        b += timed(.5, "bóng", B_[0] - 8, B_[1] - 10, RED, 14, "end", "700", None, TT)
        b += timed(.5, "A: không có bóng", 250, 196, BLUE, 14, "start", "700", None, TT)
        # bán kính tới tâm + góc ở tâm
        b += f'<g opacity="0">{seg(ox, oy, *tA, GREY, 1.4, "5 4")}{seg(ox, oy, *tB, GREY, 1.4, "5 4")}{arc_m(ox, oy, 34, 0, aB, RED, 2)}{show_at(.7 * TT, TT)}</g>'
        b += timed(.7, "θ = ?", ox + 40, oy - 2, RED, 14, "start", "700", None, TT)
        b += dot(ox, oy, 3) + txt(ox - 8, oy + 5, "O", "currentColor", 14, "end")
        b += txt(410, 248, "tia nắng từ Mặt Trời", ORG, 14, "end", "600")
        return fig("c17-5-0", "0 0 420 258", "Tia nắng song song tới hai điểm A và B trên cùng kinh tuyến; cọc ở A không có bóng, cọc ở B có bóng ngắn",
                   b, "Mô phỏng: góc giữa A và B vẽ phóng to nhiều lần để dễ nhìn; không theo tỉ lệ.")
    # hình dữ kiện: mặt cắt kinh tuyến, góc cao buổi trưa
    ox, oy, r = 150, 140, 92
    phi, dl = 38.0, 14.0                              # góc minh hoạ, KHÔNG phải số của đề
    b += txt(16, 20, "Mặt cắt Trái Đất theo kinh tuyến, lúc giữa trưa", "currentColor", 14)
    b += circ(ox, oy, r, "currentColor", BLUE, .1, 2.2)
    b += seg(ox - r - 10, oy, ox + r + 40, oy, "currentColor", 1.4, "6 4") + txt(ox - r + 6, oy + 20, "xích đạo", "currentColor", 14, "start", "600")
    Pp = pt(ox, oy, r, phi)
    b += seg(ox, oy, *Pp, "currentColor", 1.6)
    b += arc_m(ox, oy, 26, 0, phi, BLUE, 2) + txt(ox + 30, oy - 8, "φ", BLUE, 14)
    # đường chân trời tại P (tiếp tuyến) + thiên đỉnh
    tx, ty = math.sin(math.radians(phi)), math.cos(math.radians(phi))  # hướng xuống-phải trên màn hình (phía Nam)
    b += seg(Pp[0] - 55 * tx, Pp[1] - 55 * ty, Pp[0] + 70 * tx, Pp[1] + 70 * ty, GRN, 2)
    z = pt(*Pp, 52, phi)
    b += seg(*Pp, *z, "currentColor", 1.4, "4 4") + txt(z[0] + 6, z[1] - 2, "thiên đỉnh", "currentColor", 14, "start", "600")
    b += txt(Pp[0] - 55 * tx - 4, Pp[1] - 55 * ty + 4, "chân trời", GRN, 14, "end", "600")
    # tia nắng tới P: đi từ hướng (cos δ, sin δ)
    src = pt(*Pp, 150, dl)
    b += seg(*src, *Pp, ORG, 2.2) + chevron((src[0] + Pp[0]) / 2, (src[1] + Pp[1]) / 2, Pp[0] - src[0], Pp[1] - src[1], ORG, 2.2, 10)
    b += arc_m(*Pp, 30, phi - 90, dl, RED, 2)
    hx, hy = pt(*Pp, 40, (phi - 90 + dl) / 2)
    b += txt(hx + 2, hy + 6, "h = ?", RED, 14)
    # δ: tia song song qua tâm
    q = pt(ox, oy, r + 52, dl)
    b += seg(ox, oy, *q, ORG, 1.4, "5 4") + arc_m(ox, oy, 62, 0, dl, ORG, 2) + txt(ox + 66, oy - 4, "δ", ORG, 14)
    b += dot(ox, oy, 3) + txt(ox - 6, oy + 18, "O", "currentColor", 14, "end") + dot(*Pp, 3.5) + txt(Pp[0] - 8, Pp[1] + 4, "P", "currentColor", 14, "end")
    # bóng cọc
    x1, y1 = 300, 252
    b += txt(300, 198, "cọc và bóng:", "currentColor", 14, "start", "600")
    b += seg(x1, y1, x1, y1 - 40, "currentColor", 3) + seg(x1 - 6, y1, 410, y1, GRN, 2)
    b += seg(x1, y1 - 40, x1 + 80, y1, ORG, 2) + seg(x1, y1, x1 + 80, y1, "currentColor", 4)
    b += arc_m(x1 + 80, y1, 18, 153.4, 180, RED, 2) + txt(x1 + 52, y1 - 6, "h", RED, 14, "end")
    b += txt(x1 - 6, y1 - 16, "1 m", "currentColor", 14, "end", "600") + txt(x1 + 40, y1 + 18, "bóng = ?", RED, 14, "middle")
    return fig("c17-5-2", "0 0 420 272", "Mặt cắt kinh tuyến: điểm P ở vĩ độ φ, tia nắng tới lệch δ so với mặt phẳng xích đạo, góc cao h giữa tia nắng và đường chân trời; bên cạnh là cọc và bóng",
               b, "Dữ kiện: các góc vẽ minh hoạ, không phải số của đề. Tia nắng coi là song song.")


# ───────────── Dạng 6 · Hệ Mặt Trời và Ngân Hà ─────────────
PLAN = [("Trái Đất", 1.0), ("Sao Hoả", 1.52), ("Sao Mộc", 5.2), ("Sao Thổ", 9.5), ("Sao Hải Vương", 30.0)]

def d6(kk):
    b = ""
    if kk == 0:
        TT = 8.0
        x0, kx, y0 = 24, (388 - 24) / 30, 160          # trục chính: 1 AU = 12,1 px (đúng tỉ lệ khoảng cách)
        xi, ki, yi = 24, 120, 92                       # khung phóng to: 1 AU = 120 px
        Rmax = 30.4                                     # AU, mặt sóng đi tới đây ở cuối mô phỏng
        b += txt(16, 22, "Ánh sáng rời Mặt Trời, lan ra các hành tinh", "currentColor", 14)
        b += (f'<defs><clipPath id="c17-6-cl"><rect x="0" y="122" width="420" height="78"/></clipPath>'
              f'<clipPath id="c17-6-ci"><rect x="16" y="50" width="250" height="62"/></clipPath></defs>')
        # khung phóng to vùng trong (Trái Đất, Sao Hoả)
        b += f'<rect x="16" y="50" width="250" height="62" rx="6" fill="none" stroke="{GREY}" stroke-width="1.4" stroke-dasharray="4 4"/>'
        b += txt(262, 66, "phóng to ×10", GREY, 14, "end", "600")
        b += seg(xi, yi, 258, yi, GREY, 1.2, "3 4") + sun(xi, yi, 8)
        b += (f'<circle cx="{xi}" cy="{yi}" r="1" fill="none" stroke="{ORG}" stroke-width="2.4" clip-path="url(#c17-6-ci)">'
              f'{anim("r", [1, Rmax * ki], TT)}</circle>')
        for ten, a_ in PLAN[:2]:
            x = xi + ki * a_
            b += f'<circle cx="{x:.1f}" cy="{yi}" r="5" fill="{BLUE}" stroke="currentColor" stroke-width="1.4"/>'
            b += f'<circle cx="{x:.1f}" cy="{yi}" r="10" fill="none" stroke="{ORG}" stroke-width="2" opacity="0">{show_at(a_ / Rmax * TT, TT)}</circle>'
            b += txt(x, yi - 14, ten, "currentColor", 14, "middle", "600")
        b += txt(xi + ki, yi + 26, "1 AU", "currentColor", 14, "middle", "600")
        # trục chính tới Sao Hải Vương
        b += seg(x0, y0, 400, y0, GREY, 1.2, "3 4") + circ(x0, y0, 5, ORG, SUN, .9, 1.6)
        b += seg(x0 - 6, y0 - 8, x0 - 6, y0 + 8, GREY, 1.2) + seg(x0 + kx * 1.6 + 4, y0 - 8, x0 + kx * 1.6 + 4, y0 + 8, GREY, 1.2)
        b += seg(18, 112, x0 - 6, y0 - 8, GREY, 1, "3 3") + seg(266, 112, x0 + kx * 1.6 + 4, y0 - 8, GREY, 1, "3 3")
        b += (f'<circle cx="{x0}" cy="{y0}" r="1" fill="none" stroke="{ORG}" stroke-width="2.4" clip-path="url(#c17-6-cl)">'
              f'{anim("r", [1, Rmax * kx], TT)}</circle>')
        for ten, a_ in PLAN[2:]:
            x = x0 + kx * a_
            b += f'<circle cx="{x:.1f}" cy="{y0}" r="5" fill="{BLUE}" stroke="currentColor" stroke-width="1.4"/>'
            b += f'<circle cx="{x:.1f}" cy="{y0}" r="10" fill="none" stroke="{ORG}" stroke-width="2" opacity="0">{show_at(a_ / Rmax * TT, TT)}</circle>'
            if a_ < 20:
                b += txt(x, y0 + 26, ten, "currentColor", 14, "middle", "600")
        xN = x0 + kx * 30
        b += txt(xN - 10, y0 - 12, "Sao Hải Vương, 30 AU", "currentColor", 14, "end", "600")
        b += timed(.999, "tới Sao Hải Vương: t = ?", xN - 10, y0 + 30, RED, 14, "end", "700", None, TT)
        return fig("c17-6-0", "0 0 420 204", "Mặt sóng ánh sáng lan ra từ Mặt Trời, lần lượt tới Trái Đất, Sao Hoả (khung phóng to), Sao Mộc, Sao Thổ, Sao Hải Vương",
                   b, "Mô phỏng: khoảng cách đúng tỉ lệ AU (khung trên phóng to 10 lần), ánh sáng đi đều; chạy chậm hơn thật nhiều lần, không ghi tỉ lệ thời gian. Cỡ hành tinh không theo tỉ lệ.")
    # hình dữ kiện: Ngân Hà nhìn nghiêng + thang đơn vị
    cx, cy, rx, ry = 210, 104, 186, 48
    b += txt(16, 20, "Ngân Hà nhìn nghiêng (đường kính ~100 000 ly)", "currentColor", 14)
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{GREY}" fill-opacity=".18" stroke="{GREY}" stroke-width="1.6"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="16" fill="{SUN}" fill-opacity=".35" stroke="{ORG}" stroke-width="1.4"/>'
    rs = 26_000 / 50_000 * rx
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rs:.1f}" ry="{rs * ry / rx:.1f}" fill="none" stroke="{GRN}" stroke-width="1.8" stroke-dasharray="6 4"/>'
    sxp, syp = cx + rs, cy
    b += circ(sxp, syp, 5, "currentColor", SUN, 1, 1.4)
    b += chevron(sxp, syp - 12, 0, -1, GRN, 2, 10)
    b += seg(cx, cy, sxp, syp, "currentColor", 1.4) + dot(cx, cy, 3)
    b += txt(cx + rs / 2, cy + 42, "r = 26 000 ly", "currentColor", 14, "middle", "600")
    b += txt(sxp + 8, syp - 14, "Mặt Trời", "currentColor", 14, "start", "600")
    b += txt(sxp + 8, syp + 4, "v = ?", RED, 14, "start", "700")
    b += txt(cx, cy + ry + 22, "một vòng: T = 230 triệu năm", GRN, 14, "middle", "600")
    yb = 196
    b += txt(16, yb, "1 AU = 1,5·10^{8} km", "currentColor", 14, "start", "600")
    b += txt(16, yb + 22, "1 ly = 9,46·10^{12} km", "currentColor", 14, "start", "600")
    b += txt(16, yb + 44, "c = 3·10^{5} km/s", "currentColor", 14, "start", "600")
    b += txt(230, yb, "Proxima: 4,24 ly", "currentColor", 14, "start", "600")
    b += txt(230, yb + 22, "tàu 17 km/s: t = ?", RED, 14, "start", "700")
    b += txt(230, yb + 44, "mô hình 1 : 10^{10}", "currentColor", 14, "start", "600")
    return fig("c17-6-2", "0 0 420 252", "Ngân Hà nhìn nghiêng: Mặt Trời ở cách tâm 26 000 năm ánh sáng, quay một vòng mất 230 triệu năm; bên dưới là các đơn vị và dữ kiện",
               b, "Dữ kiện: Ngân Hà và quỹ đạo Mặt Trời vẽ minh hoạ. " + NOTE)


BUILD = [d4, d5, d6]

# ═════════════ ĐỀ ═════════════
DANG = [
dict(label="Dạng 4 · Nâng cao · Tháng giao hội, ngày sao và thời gian nguyệt thực toàn phần",
     topic=T4,
     problem_html=r"""<p>Tháng thiên văn (thời gian Mặt Trăng quay một vòng quanh Trái Đất so với các ngôi sao) là $T=27{,}32$ ngày; một năm có $365{,}25$ ngày. Coi các quỹ đạo là đường tròn, nằm trong cùng một mặt phẳng; Mặt Trăng quay quanh Trái Đất, Trái Đất quay quanh Mặt Trời và tự quay quanh trục đều cùng một chiều.</p><ol type="a"><li>Tính tốc độ góc của Mặt Trăng quanh Trái Đất và của Trái Đất quanh Mặt Trời (theo độ/ngày). Từ đó tính tháng giao hội $S$ (thời gian giữa hai lần trăng non liên tiếp).</li><li>Bắt đầu từ một lần trăng non. Sau đúng một tháng thiên văn, Mặt Trăng còn phải đi thêm bao nhiêu ngày nữa mới tới lần trăng non kế tiếp?</li><li>Ngày Mặt Trời (thời gian giữa hai lần liên tiếp Mặt Trời lên cao nhất) dài $24$ h. Ngày sao (thời gian Trái Đất tự quay đúng một vòng so với các ngôi sao) ngắn hơn ngày Mặt Trời bao nhiêu phút?</li><li>Trong một lần nguyệt thực, Mặt Trăng đi xuyên qua đúng giữa vùng tối của bóng Trái Đất. Tại quỹ đạo Mặt Trăng, vùng tối rộng $9200$ km; Mặt Trăng có đường kính $3470$ km và cách Trái Đất $384\,000$ km. Bóng Trái Đất luôn nằm trên đường thẳng nối Mặt Trời với Trái Đất. Coi Mặt Trăng chuyển động thẳng đều trong lúc đi qua bóng. Tính tốc độ của Mặt Trăng so với bóng Trái Đất và thời gian nguyệt thực toàn phần dài nhất.</li></ol>"""),
dict(label="Dạng 5 · Nâng cao · Góc cao Mặt Trời buổi trưa và phép đo của Eratosthenes",
     topic=T5,
     problem_html=r"""<p>Trục Trái Đất nghiêng $23{,}5°$. Lúc giữa trưa, tia nắng chiếu vuông góc với mặt đất tại nơi có vĩ độ bằng xích vĩ $\delta$ của Mặt Trời: ngày xuân phân $\delta=0°$, ngày hạ chí $\delta=+23{,}5°$ (phía Bắc), ngày đông chí $\delta=-23{,}5°$ (phía Nam). Hà Nội ở vĩ độ $21{,}0°$ Bắc, TP.HCM ở vĩ độ $10{,}8°$ Bắc. Các cọc đều cắm thẳng đứng trên mặt đất nằm ngang.</p><ol type="a"><li>Tính góc cao của Mặt Trời lúc giữa trưa ở Hà Nội ngày xuân phân và ngày hạ chí. Trưa hạ chí, bóng cọc ở Hà Nội ngả về phía Bắc hay phía Nam?</li><li>Tính chiều dài bóng của một cọc cao $1$ m lúc giữa trưa ở Hà Nội ngày đông chí, và ở TP.HCM ngày hạ chí.</li><li>Trưa ngày xuân phân, tại điểm A trên xích đạo, cọc không có bóng. Cùng lúc đó, tại điểm B cùng kinh tuyến với A và cách A $556$ km về phía Bắc, cọc cao $1$ m có bóng dài $0{,}0875$ m. Coi tia nắng tới Trái Đất là song song. Tính góc lệch giữa tia nắng và cọc ở B, rồi tính chu vi và bán kính Trái Đất.</li></ol>"""),
dict(label="Dạng 6 · Vận dụng cao · Hệ Mặt Trời và Ngân Hà: khoảng cách, thời gian, tốc độ",
     topic=T6,
     problem_html=r"""<p>Cho tốc độ ánh sáng $c=3\cdot10^5$ km/s; $1$ AU $=1{,}5\cdot10^8$ km (khoảng cách Trái Đất – Mặt Trời); một năm có $365{,}25$ ngày; $1$ năm ánh sáng (ly) $=9{,}46\cdot10^{12}$ km. Coi các quỹ đạo là đường tròn.</p><ol type="a"><li>Ánh sáng Mặt Trời tới Trái Đất mất bao lâu? Tới Sao Hải Vương (cách Mặt Trời $30$ AU) mất bao nhiêu giờ?</li><li>Khoảng cách Trái Đất – Sao Hoả thay đổi từ $0{,}52$ AU đến $2{,}52$ AU. Sóng vô tuyến (truyền với tốc độ ánh sáng) đi từ Trái Đất tới một xe tự hành trên Sao Hoả mất ít nhất và nhiều nhất bao nhiêu phút? Vì sao người ta không lái xe đó trực tiếp như lái xe đồ chơi điều khiển từ xa?</li><li>Tính tốc độ của Trái Đất trên quỹ đạo quanh Mặt Trời (km/s).</li><li>Ngôi sao gần nhất (Proxima Centauri) cách ta $4{,}24$ ly. Đổi khoảng cách này ra AU. Một tàu vũ trụ bay đều với tốc độ $17$ km/s thì mất bao nhiêu năm để tới đó?</li><li>Mặt Trời cách tâm Ngân Hà khoảng $26\,000$ ly và quay một vòng quanh tâm mất khoảng $230$ triệu năm. Tính tốc độ của Mặt Trời quanh tâm Ngân Hà (km/s). Trong $4{,}6$ tỉ năm tuổi của mình, Mặt Trời đã đi được khoảng bao nhiêu vòng?</li><li>Thu nhỏ Hệ Mặt Trời theo tỉ lệ $1:10^{10}$ thì Mặt Trời thành quả bóng đường kính $14$ cm. Mặt Trăng cách Trái Đất $384\,000$ km. Trong mô hình đó, Mặt Trăng cách Trái Đất bao nhiêu xentimét?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 1 nguyên văn đề ; cột 2 dữ liệu ; cột 3 kiến thức nền + câu hỏi gợi) ═════════════
ANALYSIS = [
 # Dạng 4
 [(r'"Tháng thiên văn (thời gian Mặt Trăng quay một vòng quanh Trái Đất so với các ngôi sao) là $T=27{,}32$ ngày; một năm có $365{,}25$ ngày"', r"$T=27{,}32$ ngày ; $1$ năm $=365{,}25$ ngày", r"Tốc độ góc đều : $\omega=\dfrac{360°}{\text{chu kì}}$"),
  (r'"Mặt Trăng quay quanh Trái Đất, Trái Đất quay quanh Mặt Trời và tự quay quanh trục đều cùng một chiều"', r"cùng chiều quay", r"⚠ hai chuyển động cùng chiều : hướng Mặt Trời (nhìn từ Trái Đất) cũng quay. Mặt Trăng phải đuổi theo hướng đó với tốc độ góc nào ?"),
  (r'"tính tháng giao hội $S$ (thời gian giữa hai lần trăng non liên tiếp)"', r"$S=?$", r"Trăng non : Mặt Trăng ở giữa Mặt Trời và Trái Đất. Giữa hai lần, Mặt Trăng hơn hướng Mặt Trời đúng một vòng"),
  (r'"Sau đúng một tháng thiên văn, Mặt Trăng còn phải đi thêm bao nhiêu ngày nữa"', r"$\Delta t=?$", r"Lúc đó Mặt Trăng về lại hướng sao cũ ; hướng Mặt Trời đã lệch đi một góc bằng góc nào ?"),
  (r'"Ngày sao (thời gian Trái Đất tự quay đúng một vòng so với các ngôi sao) ngắn hơn ngày Mặt Trời bao nhiêu phút?"', r"ngày Mặt Trời $=24$ h ; chênh lệch $=?$", r"Cùng ý tưởng câu a : trong một ngày Mặt Trời, Trái Đất tự quay bao nhiêu độ so với sao ?"),
  (r'"Tại quỹ đạo Mặt Trăng, vùng tối rộng $9200$ km; Mặt Trăng có đường kính $3470$ km và cách Trái Đất $384\,000$ km"', r"vùng tối $9200$ km ; $D_M=3470$ km ; $d=384\,000$ km", r"Quãng đường trên quỹ đạo tròn : chu vi $2\pi d$"),
  (r'"Bóng Trái Đất luôn nằm trên đường thẳng nối Mặt Trời với Trái Đất"', r"bóng quay theo hướng Mặt Trời", r"⚠ so với bóng, Mặt Trăng quay một vòng hết thời gian nào : $T$ hay $S$ ?"),
  (r'"thời gian nguyệt thực toàn phần dài nhất"', r"$t_{tp}=?$", r"Toàn phần bắt đầu khi Mặt Trăng vừa nằm gọn trong vùng tối, kết thúc khi bắt đầu ló ra : tâm Mặt Trăng đi được bao xa ?")],
 # Dạng 5
 [(r'"Lúc giữa trưa, tia nắng chiếu vuông góc với mặt đất tại nơi có vĩ độ bằng xích vĩ $\delta$ của Mặt Trời"', r"xuân phân $0°$ ; hạ chí $+23{,}5°$ ; đông chí $-23{,}5°$", r"Góc cao buổi trưa : $h=90°-|\varphi-\delta|$"),
  (r'"Hà Nội ở vĩ độ $21{,}0°$ Bắc, TP.HCM ở vĩ độ $10{,}8°$ Bắc"', r"$\varphi_{HN}=21{,}0°$ ; $\varphi_{HCM}=10{,}8°$", r"⚠ $\delta$ và $\varphi$ mang dấu (Bắc dương, Nam âm) ; lấy hiệu rồi trị tuyệt đối"),
  (r'"Trưa hạ chí, bóng cọc ở Hà Nội ngả về phía Bắc hay phía Nam?"', r"hướng bóng $=?$", r"Mặt Trời ở phía nào của thiên đỉnh ? So sánh $\delta$ với $\varphi$"),
  (r'"Tính chiều dài bóng của một cọc cao $1$ m lúc giữa trưa"', r"cọc $1$ m ; bóng $=?$", r"Tam giác vuông cọc – bóng – tia nắng : $\tan h=\dfrac{\text{cọc}}{\text{bóng}}$"),
  (r'"tại điểm B cùng kinh tuyến với A và cách A $556$ km về phía Bắc, cọc cao $1$ m có bóng dài $0{,}0875$ m"', r"cung $AB=556$ km ; cọc $1$ m, bóng $0{,}0875$ m", r"Góc lệch $\theta$ giữa tia nắng và cọc : $\tan\theta=\dfrac{\text{bóng}}{\text{cọc}}$"),
  (r'"Coi tia nắng tới Trái Đất là song song"', r"tia ở A và tia ở B song song", r"⚠ cọc ở A, ở B đều hướng về tâm Trái Đất. Góc ở tâm giữa OA và OB liên hệ với $\theta$ thế nào ?"),
  (r'"rồi tính chu vi và bán kính Trái Đất"', r"$C=?$ ; $R=?$", r"Độ dài cung tỉ lệ với góc ở tâm : $\dfrac{s}{C}=\dfrac{\theta}{360°}$ ; $C=2\pi R$")],
 # Dạng 6
 [(r'"Cho tốc độ ánh sáng $c=3\cdot10^5$ km/s; $1$ AU $=1{,}5\cdot10^8$ km"', r"$c=3\cdot10^5$ km/s ; $1$ AU $=1{,}5\cdot10^8$ km", r"Chuyển động đều : $t=\dfrac{s}{v}$ ; đổi khoảng cách ra km trước"),
  (r'"Tới Sao Hải Vương (cách Mặt Trời $30$ AU) mất bao nhiêu giờ?"', r"$s=30$ AU ; $t=?$ (h)", r"$1$ h $=3600$ s"),
  (r'"Sóng vô tuyến (truyền với tốc độ ánh sáng) đi từ Trái Đất tới một xe tự hành trên Sao Hoả"', r"$0{,}52$ AU … $2{,}52$ AU", r"⚠ đề hỏi một chiều Trái Đất → xe ; khi điều khiển cần cả lệnh đi lẫn hình ảnh về"),
  (r'"Tính tốc độ của Trái Đất trên quỹ đạo quanh Mặt Trời (km/s)"', r"$r=1$ AU ; $T=1$ năm", r"Quỹ đạo tròn : $v=\dfrac{2\pi r}{T}$, $T$ đổi ra giây"),
  (r'"Ngôi sao gần nhất (Proxima Centauri) cách ta $4{,}24$ ly"', r"$s=4{,}24$ ly", r"⚠ năm ánh sáng là đơn vị đo đại lượng nào ? $1$ ly $=9{,}46\cdot10^{12}$ km"),
  (r'"Một tàu vũ trụ bay đều với tốc độ $17$ km/s thì mất bao nhiêu năm để tới đó?"', r"$v=17$ km/s ; $t=?$ (năm)", r"$t=\dfrac{s}{v}$ rồi đổi giây ra năm"),
  (r'"Mặt Trời cách tâm Ngân Hà khoảng $26\,000$ ly và quay một vòng quanh tâm mất khoảng $230$ triệu năm"', r"$r=26\,000$ ly ; $T=2{,}3\cdot10^8$ năm", r"$v=\dfrac{2\pi r}{T}$ với $r$ theo km, $T$ theo giây ; số vòng $=\dfrac{\text{tuổi}}{T}$"),
  (r'"Thu nhỏ Hệ Mặt Trời theo tỉ lệ $1:10^{10}$"', r"tỉ lệ $1:10^{10}$ ; $d=384\,000$ km", r"Độ dài trong mô hình $=\dfrac{\text{độ dài thật}}{10^{10}}$ ; $1$ km $=10^5$ cm")],
]

# ═════════════ LỜI GIẢI ═════════════
R4 = [r"<strong>Tốc độ góc:</strong> quay đều một vòng hết chu kì $T$ thì $\omega=\dfrac{360°}{T}$.",
      r"<strong>Đuổi nhau cùng chiều</strong> (như hai kim đồng hồ): góc lệch tăng với tốc độ $\omega_1-\omega_2$ ; hơn nhau một vòng sau $\dfrac{360°}{\omega_1-\omega_2}$.",
      r"<strong>Trăng non:</strong> Mặt Trăng nằm trên hướng Trái Đất → Mặt Trời ; bóng Trái Đất nằm trên đường Mặt Trời – Trái Đất.",
      r"<strong>Chuyển động đều:</strong> $v=\dfrac{2\pi d}{\text{chu kì}}$ ; $t=\dfrac{s}{v}$.",
      r"<strong>Điều kiện:</strong> quỹ đạo tròn, đồng phẳng, cùng chiều quay ; $1$ ngày $=86\,400$ s."]
R5 = [r"<strong>Góc cao Mặt Trời</strong> $h$: góc giữa tia nắng và mặt đất nằm ngang.",
      r"<strong>Buổi trưa:</strong> $h=90°-|\varphi-\delta|$ ; $\delta\lt\varphi$ thì Mặt Trời ở phía Nam thiên đỉnh, bóng ngả về Bắc ; $\delta\gt\varphi$ thì ngược lại.",
      r"<strong>Bóng cọc:</strong> $\tan h=\dfrac{\text{cọc}}{\text{bóng}}$.",
      r"<strong>Eratosthenes:</strong> tia song song cắt hai bán kính, góc ở tâm $=\theta$ (so le trong) ; $\dfrac{s}{C}=\dfrac{\theta}{360°}$, $C=2\pi R$.",
      r"<strong>Điều kiện:</strong> tia nắng song song ; A, B cùng kinh tuyến ; cọc thẳng đứng."]
R6 = [r"<strong>Chuyển động đều:</strong> $t=\dfrac{s}{v}$ ; ánh sáng và sóng vô tuyến đi với $c=3\cdot10^5$ km/s.",
      r"<strong>Quỹ đạo tròn:</strong> $v=\dfrac{2\pi r}{T}$.",
      r"<strong>Đơn vị khoảng cách:</strong> $1$ AU $=1{,}5\cdot10^8$ km ; $1$ ly $=9{,}46\cdot10^{12}$ km (quãng đường ánh sáng đi trong một năm).",
      r"<strong>Đổi thời gian:</strong> $1$ năm $=365{,}25\cdot86\,400\approx3{,}156\cdot10^7$ s.",
      r"<strong>Mô hình tỉ lệ $1:k$:</strong> mọi độ dài chia cho $k$."]

SOLS = [
 sol(R4, [
  ("Tốc độ góc của Mặt Trăng", [M(r"\omega_M=\dfrac{360°}{T}=\dfrac{360°}{27{,}32\ \text{ngày}}"), A(r"\omega_M\approx13{,}18°/\text{ngày}")]),
  ("Tốc độ Mặt Trăng đuổi theo hướng Mặt Trời", [P(r"Trái Đất quay quanh Mặt Trời cùng chiều, nên hướng Mặt Trời (nhìn từ Trái Đất) cũng quay :"),
     M(r"\omega_E=\dfrac{360°}{365{,}25\ \text{ngày}}\approx0{,}986°/\text{ngày}"), M(r"\omega_M-\omega_E\approx13{,}177-0{,}986"), A(r"\omega_M-\omega_E\approx12{,}19°/\text{ngày}")]),
  ("Tháng giao hội", [P(r"Giữa hai lần trăng non, Mặt Trăng hơn hướng Mặt Trời đúng một vòng :"),
     M(r"S=\dfrac{360°}{\omega_M-\omega_E}=\dfrac{360°}{12{,}19°/\text{ngày}}"), A(r"S\approx29{,}53\ \text{ngày}")]),
  ("Thời gian Mặt Trăng đi thêm", [P(r"Sau $T$, Mặt Trăng về lại hướng sao cũ. Trong thời gian đó hướng Mặt Trời đã lệch đi đúng góc Trái Đất đi trên quỹ đạo :"),
     M(r"\alpha=\omega_E\,T=0{,}986\cdot27{,}32\approx26{,}9°"),
     P(r"Trong lúc Mặt Trăng đuổi, hướng Mặt Trời vẫn tiếp tục quay, nên dùng tốc độ đuổi :"),
     M(r"\Delta t=\dfrac{\alpha}{\omega_M-\omega_E}=\dfrac{26{,}9°}{12{,}19°/\text{ngày}}"), A(r"\Delta t\approx2{,}21\ \text{ngày}")]),
  ("Ngày sao", [P(r"Trong một ngày Mặt Trời, Trái Đất đi thêm $0{,}986°$ trên quỹ đạo nên phải tự quay $360°+0{,}986°$ thì Mặt Trời mới lên cao nhất lần nữa :"),
     M(r"\omega_{tq}=\dfrac{360{,}986°}{24\ \text{h}}"), M(r"T_{sao}=\dfrac{360°}{\omega_{tq}}=24\cdot\dfrac{360}{360{,}986}\approx23{,}934\ \text{h}"),
     M(r"24\ \text{h}-T_{sao}\approx0{,}0655\ \text{h}"), A(r"\text{ngắn hơn}\approx3{,}93\ \text{phút}\ (\approx3\ \text{min}\ 56\ \text{s})")]),
  ("Tốc độ Mặt Trăng so với bóng", [P(r"Bóng quay theo hướng Mặt Trời, nên so với bóng Mặt Trăng đi một vòng hết $S$, không phải $T$ :"),
     M(r"v=\dfrac{2\pi d}{S}=\dfrac{2\pi\cdot384\,000\ \text{km}}{29{,}53\cdot86\,400\ \text{s}}"), A(r"v\approx0{,}946\ \text{km/s}")]),
  ("Thời gian toàn phần dài nhất", [P(r"Toàn phần từ lúc mép sau vừa vào hẳn vùng tối tới lúc mép trước bắt đầu ra : tâm Mặt Trăng đi được"),
     M(r"s=9200-3470=5730\ \text{km}"), M(r"t_{tp}=\dfrac{s}{v}=\dfrac{5730}{0{,}946}\approx6060\ \text{s}"), A(r"t_{tp}\approx101\ \text{phút}\approx1{,}7\ \text{h}")]),
  ("Kiểm tra", [P(r"$T+\Delta t=27{,}32+2{,}21=29{,}53$ ngày, khớp câu a ✓."),
     P(r"$S\gt T$ : Mặt Trăng phải đuổi theo hướng Mặt Trời đang quay cùng chiều ✓ ; tương tự ngày sao ngắn hơn ngày Mặt Trời ✓."),
     P(r"Từ lúc bắt đầu chạm tới lúc rời hẳn vùng tối : $\dfrac{9200+3470}{0{,}946}\approx13\,400$ s $\approx3{,}7$ h, dài hơn toàn phần, hợp lí ✓.")])],
  [r"a) $\omega_M\approx13{,}18°$/ngày ; $\omega_E\approx0{,}986°$/ngày ; $S\approx29{,}53$ ngày",
   r"b) đi thêm khoảng $2{,}21$ ngày",
   r"c) ngày sao ngắn hơn khoảng $3{,}93$ phút (ngày sao $\approx23$ h $56$ min)",
   r"d) $v\approx0{,}946$ km/s ; toàn phần dài nhất khoảng $101$ phút $\approx1{,}7$ h"],
  r"Nhận dạng: thấy <strong>hai chuyển động quay cùng chiều</strong> và hỏi <strong>chu kì lặp lại vị trí tương đối</strong> → tốc độ góc đuổi $\omega_1-\omega_2$, chu kì $360°/(\omega_1-\omega_2)$."),
 sol(R5, [
  ("Góc cao ở Hà Nội ngày xuân phân", [M(r"h=90°-|\varphi-\delta|=90°-|21{,}0°-0°|"), A(r"h=69{,}0°")]),
  ("Góc cao ở Hà Nội ngày hạ chí", [M(r"h=90°-|21{,}0°-23{,}5°|=90°-2{,}5°"), A(r"h=87{,}5°")]),
  ("Hướng bóng ở Hà Nội trưa hạ chí", [P(r"$\delta=23{,}5°\gt\varphi=21{,}0°$ : tia nắng vuông góc với mặt đất ở một nơi xa hơn về phía Bắc, nên Mặt Trời lệch $2{,}5°$ về phía Bắc so với thiên đỉnh."),
     A(r"T:Bóng ngả về phía Nam (rất ngắn).")]),
  ("Bóng cọc ở Hà Nội ngày đông chí", [M(r"h=90°-|21{,}0°-(-23{,}5°)|=90°-44{,}5°=45{,}5°"), M(r"\text{bóng}=\dfrac{1\ \text{m}}{\tan45{,}5°}"), A(r"\text{bóng}\approx0{,}98\ \text{m}\ (\text{về phía Bắc})")]),
  ("Bóng cọc ở TP.HCM ngày hạ chí", [M(r"h=90°-|10{,}8°-23{,}5°|=90°-12{,}7°=77{,}3°"), M(r"\text{bóng}=\dfrac{1\ \text{m}}{\tan77{,}3°}"),
     A(r"\text{bóng}\approx0{,}23\ \text{m}\ (\text{về phía Nam vì}\ \delta\gt\varphi)")]),
  ("Góc lệch giữa tia nắng và cọc ở B", [M(r"\tan\theta=\dfrac{\text{bóng}}{\text{cọc}}=\dfrac{0{,}0875}{1}"), A(r"\theta\approx5{,}00°")]),
  ("Chu vi và bán kính Trái Đất", [P(r"Ở A tia nắng trùng phương cọc (hướng về tâm O). Tia ở B song song với tia ở A, nên góc ở tâm $\widehat{AOB}=\theta$ (so le trong) :"),
     M(r"C=s\cdot\dfrac{360°}{\theta}=556\cdot\dfrac{360°}{5{,}00°}"), A(r"C\approx40\,000\ \text{km}"),
     M(r"R=\dfrac{C}{2\pi}"), A(r"R\approx6370\ \text{km}")]),
  ("Kiểm tra", [P(r"Hà Nội : góc cao trưa lớn nhất vào hạ chí, nhỏ nhất vào đông chí ✓ ; $45{,}5°\lt69{,}0°\lt87{,}5°$ ✓."),
     P(r"Góc cao gần $45°$ thì bóng gần bằng cọc ✓ ; góc cao gần $90°$ thì bóng rất ngắn ✓."),
     P(r"B cách xích đạo $5°$ vĩ độ, khớp với góc lệch tia nắng ở B ngày xuân phân ($\delta=0$) ✓ ; $R$ khớp giá trị $6370$ km quen dùng ✓.")])],
  [r"a) Hà Nội : xuân phân $h=69{,}0°$ ; hạ chí $h=87{,}5°$, bóng ngả về phía Nam",
   r"b) Hà Nội đông chí : bóng $\approx0{,}98$ m (về Bắc) ; TP.HCM hạ chí : bóng $\approx0{,}23$ m (về Nam)",
   r"c) $\theta\approx5{,}00°$ ; $C\approx40\,000$ km ; $R\approx6370$ km"],
  r"Nhận dạng: thấy <strong>vĩ độ, xuân phân / hạ chí / đông chí</strong> → $h=90°-|\varphi-\delta|$, so $\delta$ với $\varphi$ để biết hướng bóng ; thấy <strong>hai cọc cùng kinh tuyến</strong> → góc ở tâm $=\theta$, $C=s\cdot360°/\theta$."),
 sol(R6, [
  ("Ánh sáng tới Sao Hải Vương", [M(r"t_E=\dfrac{1{,}5\cdot10^8\ \text{km}}{3\cdot10^5\ \text{km/s}}=500\ \text{s}\approx8{,}3\ \text{phút}"),
     M(r"t_N=\dfrac{30\cdot1{,}5\cdot10^8}{3\cdot10^5}=15\,000\ \text{s}"), A(r"t_N\approx4{,}17\ \text{h}")]),
  ("Tín hiệu tới Sao Hoả", [M(r"t_{min}=\dfrac{0{,}52\cdot1{,}5\cdot10^8}{3\cdot10^5}=260\ \text{s}\approx4{,}3\ \text{phút}"),
     M(r"t_{max}=\dfrac{2{,}52\cdot1{,}5\cdot10^8}{3\cdot10^5}=1260\ \text{s}"), A(r"t_{max}=21{,}0\ \text{phút}"),
     P(r"Lệnh đi mất $4$–$21$ phút, hình ảnh từ xe về lại mất chừng đó nữa : khi người lái thấy vật cản thì xe đã đi qua từ lâu. Vì vậy xe phải tự lái, người ở Trái Đất chỉ gửi lộ trình.")]),
  ("Tốc độ quỹ đạo Trái Đất", [M(r"T=365{,}25\cdot86\,400\approx3{,}156\cdot10^7\ \text{s}"), M(r"v=\dfrac{2\pi\cdot1{,}5\cdot10^8\ \text{km}}{3{,}156\cdot10^7\ \text{s}}"), A(r"v\approx29{,}9\ \text{km/s}")]),
  ("Khoảng cách tới Proxima theo AU", [M(r"s=4{,}24\cdot9{,}46\cdot10^{12}\approx4{,}01\cdot10^{13}\ \text{km}"), M(r"\dfrac{4{,}01\cdot10^{13}}{1{,}5\cdot10^8}"), A(r"s\approx2{,}67\cdot10^5\ \text{AU}")]),
  ("Thời gian bay tới Proxima", [M(r"t=\dfrac{4{,}01\cdot10^{13}\ \text{km}}{17\ \text{km/s}}\approx2{,}36\cdot10^{12}\ \text{s}"), M(r"t=\dfrac{2{,}36\cdot10^{12}}{3{,}156\cdot10^7}\ \text{năm}"), A(r"t\approx7{,}5\cdot10^4\ \text{năm}\ (\text{khoảng}\ 75\,000\ \text{năm})")]),
  ("Tốc độ Mặt Trời quanh tâm Ngân Hà", [M(r"r=26\,000\cdot9{,}46\cdot10^{12}\approx2{,}46\cdot10^{17}\ \text{km}"), M(r"T=2{,}3\cdot10^8\cdot3{,}156\cdot10^7\approx7{,}26\cdot10^{15}\ \text{s}"),
     M(r"v=\dfrac{2\pi r}{T}"), A(r"v\approx213\ \text{km/s}"),
     M(r"\text{số vòng}=\dfrac{4{,}6\cdot10^9\ \text{năm}}{2{,}3\cdot10^8\ \text{năm}}"), A(r"\text{khoảng}\ 20\ \text{vòng}")]),
  ("Mặt Trăng trong mô hình", [M(r"384\,000\ \text{km}=3{,}84\cdot10^{10}\ \text{cm}"), M(r"\dfrac{3{,}84\cdot10^{10}\ \text{cm}}{10^{10}}"), A(r"3{,}84\ \text{cm}")]),
  ("Kiểm tra", [P(r"Mô hình : Mặt Trời $1{,}39\cdot10^6$ km $\to13{,}9$ cm, khớp quả bóng $14$ cm đề cho ✓."),
     P(r"Ánh sáng đi $4{,}24$ năm thì tàu chậm hơn ánh sáng $\dfrac{3\cdot10^5}{17}\approx1{,}8\cdot10^4$ lần đi mất $4{,}24\cdot1{,}8\cdot10^4\approx7{,}5\cdot10^4$ năm ✓ (cách tính thứ hai)."),
     P(r"Mặt Trời quanh tâm Ngân Hà nhanh gấp khoảng $7$ lần Trái Đất quanh Mặt Trời, nhưng một vòng vẫn mất hàng trăm triệu năm vì quỹ đạo quá lớn ✓.")])],
  [r"a) tới Trái Đất $500$ s $\approx8{,}3$ phút ; tới Sao Hải Vương $\approx4{,}17$ h",
   r"b) ít nhất $\approx4{,}3$ phút, nhiều nhất $21{,}0$ phút ; trễ quá lớn nên xe phải tự lái",
   r"c) $v\approx29{,}9$ km/s",
   r"d) $\approx2{,}67\cdot10^5$ AU ; khoảng $75\,000$ năm",
   r"e) $v\approx213$ km/s ; khoảng $20$ vòng",
   r"f) Mặt Trăng cách Trái Đất $3{,}84$ cm"],
  r"Nhận dạng: thấy <strong>AU, năm ánh sáng, triệu năm</strong> → đổi hết ra km và giây, rồi dùng $t=s/v$ hoặc $v=2\pi r/T$ ; năm ánh sáng là khoảng cách."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>trăng non lặp lại</b>, <b>cùng chiều quay</b> → nghĩ tới <b>tốc độ góc đuổi ω₁ − ω₂</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 5}, buoc=[
  buoc("Tốc độ góc của Mặt Trăng", "Mặt Trăng quay quanh Trái Đất (so với các sao) bao nhiêu độ mỗi ngày?", round(W_M, 3), "°/ngày", 0.02,
       loi=r"Chia $360°$ cho $29{,}5$ ngày (tháng âm lịch) — đó là tốc độ so với hướng Mặt Trời, không phải so với sao."),
  buoc("Tốc độ Mặt Trăng đuổi theo hướng Mặt Trời", "Mỗi ngày, góc giữa hướng Mặt Trăng và hướng Mặt Trời (nhìn từ Trái Đất) tăng thêm bao nhiêu độ?", round(W_D, 3), "°/ngày", 0.02,
       loi=r"Cộng hai tốc độ góc: Trái Đất quay cùng chiều nên hướng Mặt Trời chạy theo cùng chiều với Mặt Trăng, khoảng cách góc tăng chậm hơn chứ không nhanh hơn.",
       ke=[(r"Lấy $\omega_M-\omega_E$ với $\omega_E=\dfrac{360°}{365{,}25\ \text{ngày}}$", True),
           (r"Lấy $\omega_M+\omega_E$", r"Hai chuyển động cùng chiều: hướng Mặt Trời quay cùng chiều với Mặt Trăng nên phải trừ, như kim phút đuổi kim giờ."),
           (r"Lấy luôn $\omega_M$", r"Bỏ qua chuyển động của Trái Đất quanh Mặt Trời; hướng Mặt Trời không đứng yên so với các sao.")]),
  buoc("Tháng giao hội", "Tháng giao hội S dài bao nhiêu ngày?", round(S4, 3), "ngày", 0.02,
       loi=r"Lấy $\dfrac1S=\dfrac1T+\dfrac1{365{,}25}$ (cộng) nên ra $S$ ngắn hơn $T$ — vô lí, vì Mặt Trăng phải đi thêm mới đuổi kịp hướng Mặt Trời.",
       ke=[(r"$S=\dfrac{360°}{\omega_M-\omega_E}$", True),
           (r"$S=\dfrac{360°}{\omega_M}$", r"Đó chính là tháng thiên văn $T$; trăng non lặp lại khi Mặt Trăng hơn hướng Mặt Trời một vòng."),
           (r"$S=\dfrac{360°}{\omega_M+\omega_E}$", r"Cộng tốc độ góc cho $S$ ngắn hơn $T$; Mặt Trăng phải đuổi theo hướng Mặt Trời nên $S$ dài hơn $T$.")]),
  buoc("Thời gian Mặt Trăng đi thêm", "Sau một tháng thiên văn, Mặt Trăng còn phải đi thêm bao nhiêu ngày?", round(DT4, 3), "ngày", 0.03,
       loi=r"Chia góc Trái Đất đã đi cho $\omega_M$: quên rằng trong lúc Mặt Trăng đi thêm thì hướng Mặt Trời vẫn tiếp tục quay.",
       ke=[(r"Góc Trái Đất đã đi $\omega_E T$, chia cho tốc độ đuổi $\omega_M-\omega_E$", True),
           (r"Góc Trái Đất đã đi $\omega_E T$, chia cho $\omega_M$", r"Trong lúc Mặt Trăng đi thêm, hướng Mặt Trời vẫn quay tiếp; phải dùng tốc độ đuổi."),
           (r"Góc Trái Đất đã đi $\omega_E T$, chia cho $\omega_E$", r"Như vậy chỉ tính lại được chính thời gian $T$ Trái Đất đi góc ấy, không phải thời gian Mặt Trăng đuổi.")]),
  buoc("Ngày sao", "Ngày sao ngắn hơn ngày Mặt Trời bao nhiêu phút?", round(HUT4, 3), "phút", 0.05,
       loi=r"Dùng tháng giao hội của Mặt Trăng để tính, hoặc coi $15°$/h là tốc độ tự quay so với sao.",
       ke=[(r"Trong một ngày Mặt Trời, Trái Đất tự quay $360°+\omega_E\cdot1\ \text{ngày}$; từ đó tính thời gian quay đúng $360°$", True),
           (r"Lấy $24$ h chia cho $29{,}53$ ngày như trăng mọc trễ", r"Ngày Mặt Trời liên quan tới chuyển động của Trái Đất quanh Mặt Trời, không liên quan tới Mặt Trăng."),
           (r"Trái Đất quay $15°$/h nên một vòng so với sao đúng $24$ h", r"$15°$/h là tốc độ so với hướng Mặt Trời; so với sao Trái Đất quay nhanh hơn một chút vì hướng Mặt Trời dịch theo quỹ đạo.")]),
  buoc("Tốc độ Mặt Trăng so với bóng", "Mặt Trăng chuyển động so với bóng Trái Đất với tốc độ bao nhiêu km/s?", round(V4, 4), "km/s", 0.005,
       loi=r"Lấy chu kì $T=27{,}32$ ngày: bóng quay theo hướng Mặt Trời nên Mặt Trăng trở lại bóng sau tháng giao hội, không phải tháng thiên văn.",
       ke=[(r"$v=\dfrac{2\pi d}{S}$, $S$ đổi ra giây", True),
           (r"$v=\dfrac{2\pi d}{T}$, $T$ đổi ra giây", r"Đó là tốc độ so với các sao; bóng Trái Đất quay theo hướng Mặt Trời nên phải dùng $S$."),
           (r"$v=\dfrac{2\pi d}{S}$, đổi $S$ ra giây bằng $S\cdot3600$", r"Một ngày có $24\cdot3600=86\,400$ s; nhân $3600$ là đổi theo giờ.")]),
  buoc("Thời gian toàn phần dài nhất", "Nguyệt thực toàn phần kéo dài nhiều nhất bao nhiêu phút?", round(TTP4, 2), "phút", 1.5,
       loi=r"Chia cả bề rộng vùng tối cho $v$, hoặc cộng thêm đường kính Mặt Trăng — đó là các mốc của pha một phần, không phải toàn phần.",
       ke=[(r"$t=\dfrac{\text{vùng tối}-D_M}{v}$", True),
           (r"$t=\dfrac{\text{vùng tối}+D_M}{v}$", r"Đó là từ lúc Mặt Trăng bắt đầu chạm vùng tối tới lúc rời hẳn, gồm cả hai pha che một phần."),
           (r"$t=\dfrac{\text{vùng tối}}{v}$", r"Toàn phần chỉ bắt đầu khi cả đĩa Mặt Trăng đã vào trong vùng tối; tâm đi ít hơn bề rộng vùng tối đúng một đường kính.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>vĩ độ</b> và <b>hạ chí / đông chí</b> → nghĩ tới <b>h = 90° − |φ − δ|</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Góc cao ở Hà Nội ngày xuân phân", "Trưa xuân phân, Mặt Trời ở Hà Nội có góc cao bao nhiêu độ?", round(H_XP_HN, 2), "°", 0.1,
       loi=r"Lấy góc cao bằng vĩ độ: vĩ độ là góc lệch của tia nắng so với phương thẳng đứng (thiên đỉnh) ngày xuân phân, góc cao là phần còn lại tới $90°$."),
  buoc("Góc cao ở Hà Nội ngày hạ chí", "Trưa hạ chí, Mặt Trời ở Hà Nội có góc cao bao nhiêu độ?", round(H_HC_HN, 2), "°", 0.1,
       loi=r"Cộng $\varphi$ với $\delta$: hạ chí Mặt Trời và Hà Nội cùng ở phía Bắc xích đạo, Mặt Trời gần thiên đỉnh hơn chứ không xa hơn.",
       ke=[(r"$h=90°-|\varphi-\delta|$ với $\delta=+23{,}5°$", True),
           (r"$h=90°-(\varphi+\delta)$", r"$\delta$ hạ chí cùng phía Bắc với Hà Nội; khoảng cách góc tới thiên đỉnh là hiệu $|\varphi-\delta|$, không phải tổng."),
           (r"$h=90°-\varphi+\delta$", r"Góc cao không vượt quá $90°$; khi $\delta\gt\varphi$ Mặt Trời đã qua phía Bắc thiên đỉnh nên phải lấy trị tuyệt đối.")]),
  buoc("Hướng bóng ở Hà Nội trưa hạ chí", "Trưa hạ chí, bóng cọc ở Hà Nội ngả về phía nào?",
       loi=r"Nghĩ ở bán cầu Bắc bóng trưa luôn ngả về phía Bắc: điều đó chỉ đúng khi Mặt Trời ở phía Nam thiên đỉnh.",
       lua_chon=[("Phía Nam", True),
                 ("Phía Bắc", r"Bóng ngả về phía Bắc khi Mặt Trời ở phía Nam thiên đỉnh ($\delta\lt\varphi$); trưa hạ chí ở Hà Nội thì $\delta\gt\varphi$."),
                 ("Không có bóng", r"Cọc không có bóng chỉ khi $\delta=\varphi$ đúng bằng nhau.")],
       ke=[(r"So sánh $\delta$ với $\varphi$ để biết Mặt Trời ở phía nào của thiên đỉnh", True),
           (r"Ở bán cầu Bắc, bóng trưa luôn ngả về phía Bắc", r"Chỉ đúng khi $\delta\lt\varphi$; vùng giữa hai chí tuyến có lúc Mặt Trời ở phía Bắc thiên đỉnh."),
           (r"Xem góc cao lớn hay nhỏ hơn $45°$", r"Độ lớn góc cao không cho biết Mặt Trời lệch về phía Bắc hay phía Nam thiên đỉnh.")]),
  buoc("Bóng cọc ở Hà Nội ngày đông chí", "Trưa đông chí ở Hà Nội, bóng cọc 1 m dài bao nhiêu mét?", round(B_DC_HN, 3), "m", 0.01,
       loi=r"Lấy $\delta=+23{,}5°$ cho đông chí (đông chí Mặt Trời ở phía Nam, $\delta$ âm), hoặc tính bóng $=1\ \text{m}\cdot\tan h$.",
       ke=[(r"$h=90°-|\varphi-\delta|$ với $\delta=-23{,}5°$, rồi bóng $=\dfrac{1\ \text{m}}{\tan h}$", True),
           (r"$h$ như trên, rồi bóng $=1\ \text{m}\cdot\tan h$", r"$\tan h=\dfrac{\text{cọc}}{\text{bóng}}$ nên bóng $=\dfrac{\text{cọc}}{\tan h}$."),
           (r"$h=90°-|\varphi-\delta|$ với $\delta=+23{,}5°$", r"Đông chí Mặt Trời chiếu vuông góc ở chí tuyến Nam nên $\delta$ mang dấu âm.")]),
  buoc("Bóng cọc ở TP.HCM ngày hạ chí", "Trưa hạ chí ở TP.HCM, bóng cọc 1 m dài bao nhiêu mét?", round(B_HC_HCM, 3), "m", 0.01,
       loi=r"Cộng $\varphi$ với $\delta$ như khi tính sai ở Hà Nội, hoặc dùng $\sin h$ thay cho $\tan h$.",
       ke=[(r"$h=90°-|10{,}8°-23{,}5°|$, rồi bóng $=\dfrac{1\ \text{m}}{\tan h}$", True),
           (r"$h=90°-(10{,}8°+23{,}5°)$, rồi bóng $=\dfrac{1\ \text{m}}{\tan h}$", r"Hạ chí Mặt Trời và TP.HCM cùng phía Bắc; phải lấy hiệu $|\varphi-\delta|$."),
           (r"$h=90°-|10{,}8°-23{,}5°|$, rồi bóng $=\dfrac{1\ \text{m}}{\sin h}$", r"Bóng là cạnh góc vuông kề góc $h$; $\dfrac{\text{cọc}}{\sin h}$ là độ dài tia nắng từ đỉnh cọc tới đất.")]),
  buoc("Góc lệch giữa tia nắng và cọc ở B", "Góc lệch θ giữa tia nắng và cọc ở B bằng bao nhiêu độ?", round(TH5, 3), "°", 0.05,
       loi=r"Lấy $\tan\theta=\dfrac{\text{cọc}}{\text{bóng}}$: đó là góc cao của Mặt Trời ở B, không phải góc giữa tia nắng và cọc.",
       ke=[(r"$\tan\theta=\dfrac{\text{bóng}}{\text{cọc}}$", True),
           (r"$\tan\theta=\dfrac{\text{cọc}}{\text{bóng}}$", r"Đó là góc giữa tia nắng và mặt đất (góc cao); góc giữa tia và cọc đối diện cạnh bóng."),
           (r"Lấy luôn $\theta$ bằng số $0{,}0875$, coi là độ", r"$0{,}0875$ là tỉ số bóng/cọc, tức $\tan\theta$, chưa phải số đo góc.")]),
  buoc("Chu vi Trái Đất", "Chu vi Trái Đất tính được khoảng bao nhiêu kilômét?", round(C5), "km", 150,
       loi=r"Nghĩ góc ở tâm gấp đôi $\theta$, hoặc viết ngược tỉ lệ $C=s\cdot\dfrac{\theta}{360°}$.",
       ke=[(r"Góc ở tâm $=\theta$ (so le trong); $C=s\cdot\dfrac{360°}{\theta}$", True),
           (r"$C=s\cdot\dfrac{\theta}{360°}$", r"Ngược tỉ lệ: cung $s$ ứng với góc $\theta$ nhỏ nên cả vòng $360°$ phải dài hơn $s$ rất nhiều lần."),
           (r"Góc ở tâm $=2\theta$; $C=s\cdot\dfrac{360°}{2\theta}$", r"Tia nắng ở A và B song song, cọc A và cọc B là hai bán kính; góc ở tâm bằng $\theta$ (so le trong), không gấp đôi.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>AU, năm ánh sáng, triệu năm</b> → <b>đổi ra km, giây</b> rồi dùng <b>t = s/v, v = 2πr/T</b>",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Ánh sáng tới Sao Hải Vương", "Ánh sáng Mặt Trời tới Sao Hải Vương mất bao nhiêu giờ?", round(T_N6, 3), "h", 0.03,
       loi=r"Quên đổi AU ra km nên chia $30$ cho $3\cdot10^5$; hoặc đổi giây ra giờ bằng cách chia $60$."),
  buoc("Tín hiệu tới Sao Hoả", "Khi Sao Hoả ở xa nhất, sóng vô tuyến từ Trái Đất tới xe mất bao nhiêu phút?", round(T_MA_MAX, 2), "phút", 0.2,
       loi=r"Cộng thêm $1$ AU khoảng cách Trái Đất – Mặt Trời: $2{,}52$ AU đã là khoảng cách Trái Đất – Sao Hoả.",
       ke=[(r"$t=\dfrac{2{,}52\cdot1{,}5\cdot10^8\ \text{km}}{3\cdot10^5\ \text{km/s}}$ rồi đổi ra phút", True),
           (r"$t=\dfrac{(2{,}52+1)\cdot1{,}5\cdot10^8\ \text{km}}{3\cdot10^5\ \text{km/s}}$", r"$2{,}52$ AU là khoảng cách giữa hai hành tinh, không cần cộng khoảng cách Trái Đất – Mặt Trời."),
           (r"Tính như trên rồi nhân $2$ cho đi và về", r"Đề hỏi một chiều từ Trái Đất tới xe; đi và về là để giải thích vì sao không lái trực tiếp.")]),
  buoc("Tốc độ quỹ đạo Trái Đất", "Trái Đất chuyển động quanh Mặt Trời với tốc độ bao nhiêu km/s?", round(V_E6, 2), "km/s", 0.2,
       loi=r"Chia $1$ AU cho một năm (quên chu vi $2\pi r$), hoặc đổi một năm ra giây bằng $365{,}25\cdot3600$.",
       ke=[(r"$v=\dfrac{2\pi\cdot1\ \text{AU}}{365{,}25\cdot86\,400\ \text{s}}$", True),
           (r"$v=\dfrac{1\ \text{AU}}{365{,}25\cdot86\,400\ \text{s}}$", r"Một năm Trái Đất đi hết cả vòng quỹ đạo, quãng đường là chu vi $2\pi r$, không phải bán kính."),
           (r"$v=\dfrac{2\pi\cdot1\ \text{AU}}{365{,}25\cdot3600\ \text{s}}$", r"Một ngày có $86\,400$ s; $365{,}25\cdot3600$ chỉ là số giây trong $365{,}25$ giờ.")]),
  buoc("Khoảng cách tới Proxima theo AU", "Khoảng cách tới Proxima Centauri bằng bao nhiêu AU?", round(PROX_AU), "AU", 2500,
       loi=r"Coi năm ánh sáng là đơn vị thời gian ($4{,}24$ năm) rồi nhân với số ngày: năm ánh sáng là quãng đường ánh sáng đi trong một năm.",
       ke=[(r"$s=4{,}24\cdot9{,}46\cdot10^{12}$ km, rồi chia cho $1{,}5\cdot10^8$ km", True),
           (r"$s=4{,}24\cdot9{,}46\cdot10^{12}$ km, rồi nhân với $1{,}5\cdot10^8$", r"Đổi km ra AU phải chia cho số km của $1$ AU; nhân làm số lớn vô lí."),
           (r"$4{,}24$ ly $=4{,}24\cdot365{,}25$ ngày, rồi đổi ra AU", r"Năm ánh sáng là đơn vị khoảng cách, không phải thời gian.")]),
  buoc("Thời gian bay tới Proxima", "Tàu bay đều 17 km/s mất khoảng bao nhiêu năm để tới Proxima?", round(T_TAU), "năm", 1500,
       loi=r"Trả lời $4{,}24$ năm (thời gian của ánh sáng), hoặc đổi giây ra năm mà quên nhân $365{,}25$.",
       ke=[(r"$t=\dfrac{s\ (\text{km})}{17\ \text{km/s}}$, rồi chia cho số giây của một năm", True),
           (r"$t=4{,}24$ năm vì khoảng cách là $4{,}24$ ly", r"Đó là thời gian của ánh sáng; tàu chậm hơn ánh sáng hàng vạn lần."),
           (r"$t=\dfrac{s}{17}$ rồi chia cho $86\,400$", r"Chia $86\,400$ chỉ đổi giây ra ngày; còn phải chia tiếp cho $365{,}25$ để ra năm.")]),
  buoc("Tốc độ Mặt Trời quanh tâm Ngân Hà", "Mặt Trời quay quanh tâm Ngân Hà với tốc độ bao nhiêu km/s?", round(V_GAL, 1), "km/s", 3,
       loi=r"Lấy $r/T$ (quên $2\pi$), hoặc tính $2\pi r/T$ theo ly/năm rồi đọc luôn là km/s.",
       ke=[(r"$v=\dfrac{2\pi r}{T}$ với $r$ đổi ra km, $T$ đổi ra giây", True),
           (r"$v=\dfrac{r}{T}$ với $r$ theo km, $T$ theo giây", r"Một vòng quanh tâm là chu vi $2\pi r$, không phải bán kính."),
           (r"$v=\dfrac{2\pi r}{T}$ với $r$ theo ly, $T$ theo năm, đọc kết quả là km/s", r"Đơn vị ly/năm khác km/s; $1$ ly/năm chính bằng tốc độ ánh sáng.")]),
  buoc("Mặt Trăng trong mô hình", "Trong mô hình 1: 10¹⁰, Mặt Trăng cách Trái Đất bao nhiêu xentimét?", round(MOON_CM, 3), "cm", 0.05,
       loi=r"Chia $384\,000$ cho $10^{10}$ mà quên đổi km ra cm, nên ra một số cực nhỏ.",
       ke=[(r"Đổi $384\,000$ km ra cm, rồi chia cho $10^{10}$", True),
           (r"Lấy $384\,000$ chia $10^{10}$, coi kết quả là cm", r"Kết quả của phép chia vẫn theo km; phải đổi $1$ km $=10^5$ cm."),
           (r"So với quả bóng: lấy $384\,000$ nhân $14$ cm", r"Tỉ lệ $1:10^{10}$ áp cho mọi độ dài; không nhân với đường kính quả bóng.")]),
  buoc("Kiểm tra")]),
]


# KaTeX: chỉ số dưới có dấu tiếng Việt → \text{…}
_SUBVN = re.compile(r"_\{([^{}\\]*[^\x00-\x7f][^{}\\]*)\}")
_SUBVN1 = re.compile(r"_([^\x00-\x7f])")
def _tx(x):
    if isinstance(x, str):
        if x.lstrip().startswith("<figure"):
            return x
        x = _SUBVN.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
        return _SUBVN1.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
    if isinstance(x, list):
        return [_tx(v) for v in x]
    if isinstance(x, tuple):
        return tuple(_tx(v) for v in x)
    if isinstance(x, dict):
        return {k: _tx(v) for k, v in x.items()}
    return x
_RAW_DANG, _RAW_ANALYSIS = DANG, ANALYSIS
DANG, ANALYSIS, SOLS, STEPS = _tx(DANG), _tx(ANALYSIS), _tx(SOLS), _tx(STEPS)


def kiem_so():
    close = lambda a, b, e: abs(a - b) <= e
    # D4 — khớp nguon.md / tinh.py
    assert close(W_M, 13.18, .005) and close(W_E, 0.9856, .0005) and close(W_D, 12.19, .005)
    assert close(S4, 29.53, .005) and close(GOC_E4, 26.9, .05) and close(DT4, 2.21, .005)
    assert close(T_TV + DT4, S4, 1e-9)
    assert close(NGAY_SAO, 23.9345, .0005) and close(HUT4, 3.93, .005)      # 23 h 56 min 4 s
    assert close(V4, 0.946, .0005) and round(TTP4) == 101 and close(TTP4 / 60, 1.7, .05)
    assert close((U4 + DM4) / V4 / 3600, 3.7, .05)
    # cách sai cho kết quả ngoài sai số
    assert abs(360 / 29.5 - W_M) > .02                                         # bước 1: chia 29,5
    assert abs((W_M + W_E) - W_D) > .02 and abs(W_M - W_D) > .02               # bước 2
    assert abs(360 / W_M - S4) > .02 and abs(360 / (W_M + W_E) - S4) > .02     # bước 3
    assert abs(GOC_E4 / W_M - DT4) > .03 and abs(GOC_E4 / W_E - DT4) > .03     # bước 4
    assert abs(24 * 60 / S4 - HUT4) > .05                                       # bước 5: dùng Mặt Trăng (≈ 49 phút)
    v_T = 2 * PI * DMM4 / (T_TV * 86400); v_h = 2 * PI * DMM4 / (S4 * 3600)
    assert abs(v_T - V4) > .005 and abs(v_h - V4) > .005                        # bước 6
    assert abs(U4 / V4 / 60 - TTP4) > 1.5 and abs((U4 + DM4) / V4 / 60 - TTP4) > 1.5 and abs((U4 - DM4) / v_T / 60 - TTP4) > 1.5
    # D5
    assert H_XP_HN == 69.0 and H_HC_HN == 87.5 and H_DC_HN == 45.5 and round(H_HC_HCM, 1) == 77.3
    assert round(B_DC_HN, 2) == 0.98 and round(B_HC_HCM, 2) == 0.23 and DEL > PHI_HN and DEL > PHI_HCM
    assert close(TH5, 5.00, .005) and close(C5, 40000, 100) and close(BK5, 6370, 10)
    tan = lambda d: math.tan(math.radians(d))
    assert abs(PHI_HN - H_XP_HN) > .1                                           # bước 1: h = φ
    assert abs(90 - (PHI_HN + DEL) - H_HC_HN) > .1 and abs(90 - PHI_HN + DEL - H_HC_HN) > .1    # bước 2
    assert abs(tan(H_DC_HN) - B_DC_HN) > .01 and abs(1 / tan(H_HC_HN) - B_DC_HN) > .01           # bước 4
    assert abs(1 / tan(90 - (PHI_HCM + DEL)) - B_HC_HCM) > .01 and abs(1 / math.sin(math.radians(H_HC_HCM)) - B_HC_HCM) > .01  # bước 5
    assert abs(math.degrees(math.atan(1 / BONG_B)) - TH5) > .05 and abs(BONG_B - TH5) > .05    # bước 6
    assert abs(S_AB * TH5 / 360 - C5) > 150 and abs(S_AB * 360 / (2 * TH5) - C5) > 150          # bước 7
    # D6
    assert T_E6 == 500 and close(T_N6, 4.17, .005) and close(T_MA_MIN, 4.3, .05) and close(T_MA_MAX, 21.0, .05)
    assert close(V_E6, 29.9, .05) and close(PROX_KM, 4.01e13, .01e13) and close(PROX_AU, 267_000, 1000)
    assert close(T_TAU, 75_000, 500) and round(V_GAL) == 213 and round(VONG) == 20 and close(MOON_CM, 3.84, 1e-9)
    assert close(1.39e6 * 1e5 / 1e10, 13.9, .05)                               # quả bóng 14 cm khớp tỉ lệ
    assert abs(30 / C_AS / 3600 - T_N6) > .03 and abs(30 * AU / C_AS / 60 - T_N6) > .03          # bước 1
    assert abs(3.52 * AU / C_AS / 60 - T_MA_MAX) > .2 and abs(2 * T_MA_MAX - T_MA_MAX) > .2      # bước 2
    assert abs(AU / NAM_S - V_E6) > .2 and abs(2 * PI * AU / (NAM * 3600) - V_E6) > .2          # bước 3
    assert abs(4.24 * 365.25 - PROX_AU) > 2500 and abs(PROX_KM * AU - PROX_AU) > 2500            # bước 4
    assert abs(4.24 - T_TAU) > 1500 and abs(PROX_KM / 17 / 86400 - T_TAU) > 1500                 # bước 5
    assert abs(26_000 * LY / (230e6 * NAM_S) - V_GAL) > 3 and abs(2 * PI * 26_000 / 230e6 - V_GAL) > 3   # bước 6
    assert abs(DMM4 / 1e10 - MOON_CM) > .05 and abs(DMM4 * 14 - MOON_CM) > .05                    # bước 7
    # bảng phân tích: cột 1 trích nguyên văn đề
    for n, rows in enumerate(_RAW_ANALYSIS):
        for r in rows:
            assert r[0].strip('"') in _RAW_DANG[n]["problem_html"], (n, r[0])
        assert any("⚠" in r[2] for r in rows), n
    # không lộ đáp số trong đề, hình, bảng phân tích, nhận dạng, câu hỏi, lựa chọn, lỗi hay gặp
    lo = {0: ["13,18", "13,177", "12,19", "29,53", "26,9", "2,21", "3,93", "56 min", "0,946", "101", "1,7 h", "5730"],
          1: ["69", "87,5", "45,5", "0,98", "0,983", "0,22", "0,23", "77,3", "5,00", "40 000", "40\\,000", "6370", "6 370"],
          2: ["500 s", "8,3", "4,17", "15 000", "21,0", "1260", "4,3", "29,9", "267", "2,67", "74 8", "75 000", "7,5", "213", "20 vòng", "3,84"]}
    for n in range(3):
        figs = re.sub(r"<[^>]+>", " ", BUILD[n](0) + BUILD[n](2))           # chỉ chữ hiện trên hình
        blob = DANG[n]["problem_html"] + figs + str(ANALYSIS[n]) + STEPS[n]["nhan_dang"]
        for s in STEPS[n]["buoc"]:
            blob += s.get("tieu_de", "") + s.get("hoi", "") + s.get("loi_hay_gap", "")
            for c in s.get("chon_buoc_ke", []) + s.get("lua_chon", []):
                blob += c["text"] + c.get("vi_sao", "")
        for x in lo[n]:
            assert x not in blob, (n, x)
    for n, s in enumerate(STEPS):
        assert s["cap_do"] in (3, 4) and len(s["buoc"]) == SOLS[n].count('class="bt-step"'), n
    # JSON sạch: không ký tự điều khiển (\t lọt từ "\text" trong chuỗi thường)
    for x in (DANG, ANALYSIS, SOLS, STEPS):
        assert not re.search(r"[\x00-\x08\x0b-\x1f]", str(x).replace("\\n", "")), "ký tự điều khiển"
    for n in range(3):
        for blk in re.findall(r"\$[^$]*\$", DANG[n]["problem_html"] + SOLS[n] + str(ANALYSIS[n])):
            assert "<" not in blk and ">" not in blk, blk
    print("btm178_d456: kiểm số liệu đạt")


if __name__ == "__main__":
    kiem_so()
