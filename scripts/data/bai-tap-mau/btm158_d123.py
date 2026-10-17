"""Bài tập mẫu CĐ14 "Gương phẳng, bóng tối và nửa tối" (lesson 158) — Dạng 1–3. Module được build-hinh-158.py import.
Dàn ý + số liệu đã tính: content/hsg9/cd14-guong-phang-bong-toi/nguon.md (mục "Bài tập mẫu", D1–D3 dùng nguyên số; tinh.py).
Quy ước: góc tới/góc phản xạ đo với PHÁP TUYẾN; khoảng cách trong bài bóng đo TỪ NGUỒN; hình không theo tỉ lệ để không đo ra đáp số.
Mọi đáp số tính lại bằng Python trong kiem_so(); mọi lựa chọn sai của chon_buoc_ke được assert cho số khác đáp án đúng."""
import math
from fractions import Fraction as Fr
from dung import *   # sol, buoc, M/P/A, fig, seg, lbl, poly, arrow, chevron, RED/BLUE/ORG/GRN

GREY = "#94a3b8"
SUN = "#f59e0b"
UMB, PEN = "#475569", "#64748b"   # vùng tối tô đặc, nửa tối gạch chéo (phân biệt được cả nền sáng lẫn nền tối)
TOPIC_PX = "Định luật phản xạ ánh sáng"
# Chữ/nhãn trong hình phải đọc được trên NỀN SÁNG (mặc định site): nét tia giữ màu svg_lib, chữ dùng tông đậm.
TXT = {BLUE: "#0369a1", ORG: "#c2410c", SUN: "#b45309", GRN: "#15803d", RED: "#b91c1c", GREY: "#475569"}
_lbl0 = lbl


def lbl(x, y, s, c="currentColor", *a, **k):
    return _lbl0(x, y, s, TXT.get(c, c), *a, **k)


TOPIC_BONG = "Bóng tối, bóng nửa tối"

# số liệu D1
BETA_NANG = 50                      # tia nắng hợp phương ngang (chếch xuống)
SIR_A = BETA_NANG + 90              # hắt xuống giếng
I_A = SIR_A / 2
SIR_B = 90 - BETA_NANG              # hắt lên trần
I_B = SIR_B / 2
L_TUONG, DELTA = 4.0, 3.0
X_C = L_TUONG * math.tan(math.radians(2 * DELTA))          # m
PHI_D = math.degrees(math.atan(0.70 / L_TUONG))
DELTA_D = PHI_D / 2
# số liệu D2
H2, h2, v2 = Fr(9, 2), Fr(3, 2), Fr(6, 5)
def bong(x, H=H2, h=h2):
    return h * x / (H - h)
V_DINH = v2 * H2 / (H2 - h2)
V_DAI = v2 * h2 / (H2 - h2)
X_TUONG = 9
X_CHAM = X_TUONG * (H2 - h2) / H2
X_N = Fr(15, 2)
Y_TUONG = H2 - (H2 - h2) * X_TUONG / X_N
KC2, X_P = 12, 4
# số liệu D3 (cm)
DN, D3D, A3, L3 = 20, 30, 60, 180
def d_toi(Dn, d, a, L):
    return Dn + Fr(d - Dn) * L / a
def d_ngoai(Dn, d, a, L):
    return Fr(d + Dn) * L / a - Dn
D_DIEM = Fr(D3D * L3, A3)
DT3, DNG3 = d_toi(DN, D3D, A3, L3), d_ngoai(DN, D3D, A3, L3)
D_NHO = 12
L_MAT = Fr(A3 * DN, DN - D_NHO)
DT_120, DNG_120 = d_toi(DN, D_NHO, A3, 120), d_ngoai(DN, D_NHO, A3, 120)
DT_180, DNG_180 = d_toi(DN, D_NHO, A3, 180), d_ngoai(DN, D_NHO, A3, 180)
L_60 = Fr(60 - DN) * A3 / (D3D - DN)


def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animate attributeName="{attr}" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def ray(x1, y1, x2, y2, c=SUN, w=2.4, f=0.5):
    """Tia sáng: nét liền, đầu V ở giữa tia (hướng truyền 1 → 2)."""
    mx, my = x1 + f * (x2 - x1), y1 + f * (y2 - y1)
    return seg(x1, y1, x2, y2, c, w) + chevron(mx, my, x2 - x1, y2 - y1, c, w, 10)


def mirror(x1, y1, x2, y2, back=1, n=7):
    """Gương: nét đậm + gạch chéo ở mặt sau (back = ±1 chọn phía)."""
    b = seg(x1, y1, x2, y2, "currentColor", 3.2)
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy * back, ux * back
    for k in range(n):
        t = (k + 0.5) / n
        px, py = x1 + dx * t, y1 + dy * t
        b += seg(px, py, px + 9 * nx - 6 * ux, py + 9 * ny - 6 * uy, "currentColor", 1.3)
    return b


def arc_deg(cx, cy, r, a0, a1, c="currentColor", w=1.6):
    """Cung tròn, góc toán học (độ, ngược chiều kim đồng hồ, trục y hướng lên)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
    large = 1 if abs(a1 - a0) > 180 else 0
    return f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 {large} 0 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>'


def hdim(x1, x2, y, s, c="currentColor", up=True):
    """Kích thước nằm ngang có vạch hai đầu, chữ ở giữa."""
    b = seg(x1, y, x2, y, c, 1.3) + seg(x1, y - 5, x1, y + 5, c, 1.3) + seg(x2, y - 5, x2, y + 5, c, 1.3)
    return b + lbl((x1 + x2) / 2, y - 6 if up else y + 18, s, c, 14, "middle", "700")


# ═════════════ HÌNH ═════════════
def rot(v, deg):
    """Quay véc-tơ theo phép rotate() của SVG (trục y hướng xuống)."""
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def refl(v, m):
    n = math.hypot(*m)
    m = (m[0] / n, m[1] / n)
    d = v[0] * m[0] + v[1] * m[1]
    return (2 * d * m[0] - v[0], 2 * d * m[1] - v[1])


# ───────────── Dạng 1 · phản xạ, đặt gương, gương quay ─────────────
def d1(kk):
    b = ""
    if kk == 0:
        DUR, TH = 3.0, -6.0                       # góc quay vẽ phóng to (không theo tỉ lệ)
        IX, IY, WX = 110, 170, 390
        b += f'<rect x="{IX - 16}" y="12" width="32" height="24" rx="4" fill="none" stroke="{RED}" stroke-width="2"/>'
        b += lbl(IX + 24, 30, "laser (cố định)", RED, 14, "start", "700")
        b += ray(IX, 36, IX, IY, RED, 2.4)
        # tường
        b += seg(WX, 40, WX, 230, "currentColor", 2.6)
        for k in range(10):
            yy = 46 + 19 * k
            b += seg(WX, yy, WX + 8, yy - 8, "currentColor", 1.2)
        b += lbl(WX - 6, 226, "tường", "currentColor", 14, "end", "700")
        # gương + gạch, quay quanh I
        m0 = (math.sqrt(0.5), math.sqrt(0.5))
        hl = 46
        g = mirror(IX - hl * m0[0], IY - hl * m0[1], IX + hl * m0[0], IY + hl * m0[1], back=1)
        b += (f'<g>{g}<animateTransform attributeName="transform" type="rotate" values="0 {IX} {IY};{TH} {IX} {IY}" '
              f'dur="{DUR:.2f}s" begin="indefinite" fill="freeze"/></g>')
        ts = [k / 10 for k in range(11)]
        ys = []
        for s in ts:
            r = refl((0, 1), rot(m0, TH * s))
            ys.append(IY + (WX - IX) * r[1] / r[0])
        kt = ";".join(f"{s:.2f}" for s in ts)
        yv = ";".join(f"{y:.1f}" for y in ys)
        b += (f'<line x1="{IX}" y1="{IY}" x2="{WX}" y2="{IY}" stroke="{RED}" stroke-width="2.4">{anim("y2", yv, DUR, kt)}</line>')
        b += f'<circle cx="{WX}" cy="{IY}" r="4" fill="{GREY}" stroke="none"/>'
        b += (f'<circle cx="{WX}" cy="{IY}" r="6" fill="{RED}" stroke="none">{anim("cy", yv, DUR, kt)}</circle>')
        b += seg(WX - 12, IY, WX - 12, IY - 12, "currentColor", 1.2) + seg(WX - 12, IY - 12, WX, IY - 12, "currentColor", 1.2)
        b += lbl(118, 162, "I", "currentColor", 15, "start", "700")
        b += lbl(250, 190, "4,0 m", "currentColor", 14, "middle", "700")
        b += lbl(150, 226, "gương quay 3° quanh I", "currentColor", 14, "start", "400")
        yf = ys[-1]
        b += (f'<g opacity="0">{anim("opacity", "0;0;1", DUR, "0;0.95;1")}'
              f'{seg(WX - 26, yf, WX - 26, IY, GRN, 1.6)}{seg(WX - 31, yf, WX - 21, yf, GRN, 1.6)}{seg(WX - 31, IY, WX - 21, IY, GRN, 1.6)}'
              f'{lbl(WX - 32, (yf + IY) / 2 + 5, "dịch ?", GRN, 15, "end", "700")}</g>')
        return fig("c14-1-0", "0 0 420 240",
                   "Tia laser cố định chiếu xuống gương tại I, tia phản xạ đập vuông góc vào tường; gương quay quanh I, vệt sáng trên tường dịch lên một đoạn chưa biết",
                   b, "Mô phỏng câu c: tia laser giữ cố định, gương quay quanh trục qua I, tia phản xạ quét lên, vệt sáng dịch trên tường. "
                      "Góc quay vẽ phóng to, hình không theo tỉ lệ.")
    # hình dữ kiện câu a, b: hướng tia tới đã biết, gương chưa vẽ
    IX, IY = 210, 122
    b += seg(70, IY, 380, IY, GREY, 1.2, "4 3") + lbl(380, IY + 20, "phương ngang", GREY, 14, "end", "400")
    ux, uy = math.cos(math.radians(BETA_NANG)), math.sin(math.radians(BETA_NANG))
    sx, sy = IX - 130 * ux, IY - 130 * uy
    b += ray(sx, sy, IX, IY, SUN, 2.6)
    b += lbl(sx - 4, sy + 4, "S", SUN, 15, "end", "700") + lbl(sx + 10, sy - 2, "tia nắng", SUN, 14, "start", "700")
    b += arc_deg(IX, IY, 36, 180 - BETA_NANG, 180)
    b += lbl(IX - 60, IY - 12, "50°", "currentColor", 14, "end", "700")
    b += seg(IX, IY, IX, 210, GRN, 2, "6 4") + chevron(IX, 210, 0, 1, GRN, 2, 10)
    b += lbl(IX + 8, 204, "(a) xuống đáy giếng", GRN, 14, "start", "700")
    b += seg(IX, IY, IX, 30, BLUE, 2, "6 4") + chevron(IX, 30, 0, -1, BLUE, 2, 10)
    b += lbl(IX + 8, 40, "(b) lên trần", BLUE, 14, "start", "700")
    b += f'<circle cx="{IX}" cy="{IY}" r="4" fill="currentColor"/>' + lbl(IX - 8, IY + 22, "I", "currentColor", 15, "end", "700")
    b += lbl(IX + 10, IY - 10, "gương đặt thế nào?", RED, 14, "start", "700")
    return fig("c14-1-2", "0 0 420 222",
               "Tia nắng S tới điểm I hợp phương ngang 50 độ; hai hướng tia phản xạ cần có là thẳng đứng xuống và thẳng đứng lên; gương chưa vẽ",
               b, "Dữ kiện câu a, b: hướng tia tới đã biết, hai hướng tia phản xạ cần có (nét đứt); hướng gương phải tìm.")


# ───────────── Dạng 2 · bóng người dưới đèn đường ─────────────
GY2 = 214


def nguoi(x, hp, c="currentColor"):
    """Người đứng tại chân x, cao hp px."""
    top = GY2 - hp
    r = hp * 0.11
    return (f'<circle cx="{x}" cy="{top + r:.1f}" r="{r:.1f}" fill="none" stroke="{c}" stroke-width="2"/>'
            + seg(x, top + 2 * r, x, GY2 - hp * 0.42, c, 2.4)
            + seg(x, GY2 - hp * 0.42, x - hp * 0.12, GY2, c, 2.2) + seg(x, GY2 - hp * 0.42, x + hp * 0.12, GY2, c, 2.2)
            + seg(x - hp * 0.16, top + hp * 0.36, x + hp * 0.16, top + hp * 0.36, c, 2.2))


def d2(kk):
    b = ""
    if kk == 0:
        DUR = 2.5                                  # đúng thời gian thật: 3 m với 1,2 m/s
        PX, HP, hp, SX = 70, 150, 60, 28           # cột tại x=70; tỉ lệ cao không theo tỉ lệ thật
        x_a, x_b = PX + 2 * SX, PX + 5 * SX
        tip = lambda x: PX + (x - PX) * HP / (HP - hp)
        b += seg(16, GY2, 410, GY2, "currentColor", 2)
        b += seg(PX, GY2, PX, GY2 - HP, "currentColor", 3)
        b += f'<circle cx="{PX}" cy="{GY2 - HP}" r="7" fill="{SUN}" stroke="none"/>'
        b += lbl(PX - 8, GY2 - HP - 6, "đèn", SUN, 14, "end", "700")
        b += lbl(PX - 8, GY2 - 78, "H", "currentColor", 15, "end", "700")
        b += (f'<line x1="{PX}" y1="{GY2 - HP}" x2="{tip(x_a):.1f}" y2="{GY2}" stroke="{SUN}" stroke-width="1.8">'
              f'{anim("x2", f"{tip(x_a):.1f};{tip(x_b):.1f}", DUR)}</line>')
        b += (f'<line x1="{x_a}" y1="{GY2}" x2="{tip(x_a):.1f}" y2="{GY2}" stroke="currentColor" stroke-width="6" opacity="0.55">'
              f'{anim("x1", f"{x_a};{x_b}", DUR)}{anim("x2", f"{tip(x_a):.1f};{tip(x_b):.1f}", DUR)}</line>')
        b += (f'<g>{nguoi(0, hp)}<animateTransform attributeName="transform" type="translate" values="{x_a} 0;{x_b} 0" '
              f'dur="{DUR:.2f}s" begin="indefinite" fill="freeze"/></g>').replace(f'<g>{nguoi(0, hp)}', f'<g transform="translate({x_a} 0)">{nguoi(0, hp)}')
        b += lbl(230, 40, "người đi ra xa cột", "currentColor", 14, "start", "400")
        b += arrow("", "g", 232, 54, 300, 54, 2.4) + lbl(306, 59, "1,2 m/s", GRN, 14, "start", "700")
        b += lbl(250, 236, "bóng", "currentColor", 14, "middle", "400")
        b += (f'<g opacity="0">{anim("opacity", "0;0;1", DUR, "0;0.95;1")}'
              f'{lbl(250, 92, "đỉnh bóng chạy nhanh bao nhiêu?", RED, 14, "middle", "700")}</g>')
        return fig("c14-2-0", "0 0 420 244",
                   "Đèn trên đỉnh cột, người đi ra xa cột, tia sáng sát đỉnh đầu chạm đất ở đỉnh bóng; bóng dài dần khi người đi xa",
                   b, "Mô phỏng chạy đúng thời gian thật: người đi từ chỗ cách cột 2 m tới chỗ cách cột 5 m trong 2,5 s. "
                      "Hình không theo tỉ lệ, không đo trên hình.")
    # hình dữ kiện: hai tam giác đồng dạng, tường câu c
    GY = 196
    PX, HP, hp, XN = 40, 156, 66, 170
    T = PX + (XN - PX) * HP / (HP - hp)
    WX = 350
    b += seg(16, GY, 410, GY, "currentColor", 2)
    b += seg(PX, GY, PX, GY - HP, "currentColor", 3) + f'<circle cx="{PX}" cy="{GY - HP}" r="6" fill="{SUN}" stroke="none"/>'
    b += lbl(PX + 10, GY - HP - 4, "S (đèn)", SUN, 14, "start", "700")
    b += lbl(PX - 6, GY - HP / 2, "H", "currentColor", 15, "end", "700")
    b += seg(XN, GY, XN, GY - hp, BLUE, 3) + lbl(XN - 6, GY - hp / 2 + 4, "h", BLUE, 15, "end", "700")
    b += ray(PX, GY - HP, T, GY, SUN, 2.2, 0.3)
    b += seg(XN, GY, T, GY, "currentColor", 6, "", 0.5)
    b += f'<circle cx="{T:.1f}" cy="{GY}" r="4" fill="{RED}"/>' + lbl(T + 6, GY - 8, "T", RED, 15, "start", "700")
    b += seg(WX, GY, WX, 60, GREY, 2, "6 4") + lbl(WX + 4, 54, "tường (câu c)", GREY, 14, "middle", "400")
    b += hdim(PX, XN, GY + 16, "x", "currentColor", False)
    b += hdim(XN, T, GY + 16, "ℓ = ?", RED, False)
    return fig("c14-2-2", "0 0 420 240",
               "Đèn S trên cột cao H, người cao h cách chân cột x, tia sáng từ S sát đỉnh đầu chạm đất tại đỉnh bóng T; bóng dài l chưa biết; tường ở xa hơn",
               b, "Dữ kiện (hình không theo tỉ lệ): cột và người cùng thẳng đứng; T là đỉnh bóng; tường dùng cho câu c.")


# ───────────── Dạng 3 · nguồn rộng: vùng tối, nửa tối ─────────────
def d3(kk):
    b = ""
    Y0 = 132
    if kk == 0:
        DUR = 4.0
        KX, KY, X0 = 2.2, 1.6, 30                 # hai tỉ lệ khác nhau: không đo được trên hình
        xa = X0 + KX * A3
        rn, rd = KY * DN / 2, KY * D3D / 2
        L_A, L_B = 90, 130                        # vị trí màn trong mô phỏng (không phải số trong đề)
        def ys(L):
            xs = X0 + KX * L
            t = (xs - X0) / (xa - X0)
            yt = -rn + (-rd + rn) * t             # tia cùng mép trên (đi từ mép trên đèn)
            yn = rn + (-rd - rn) * t              # tia chéo mép (từ mép dưới đèn qua mép trên đĩa)
            return xs, yt, yn
        xs0, yt0, yn0 = ys(L_A)
        xs1, yt1, yn1 = ys(L_B)
        def pts(xs, yt, yn):
            umb = f"{xa:.1f},{Y0 - rd:.1f} {xs:.1f},{Y0 + yt:.1f} {xs:.1f},{Y0 - yt:.1f} {xa:.1f},{Y0 + rd:.1f}"
            pt = f"{xa:.1f},{Y0 - rd:.1f} {xs:.1f},{Y0 + yn:.1f} {xs:.1f},{Y0 + yt:.1f}"
            pb = f"{xa:.1f},{Y0 + rd:.1f} {xs:.1f},{Y0 - yn:.1f} {xs:.1f},{Y0 - yt:.1f}"
            return umb, pt, pb
        a0, a1 = pts(xs0, yt0, yn0), pts(xs1, yt1, yn1)
        b += ('<defs><pattern id="c14-nt" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
              f'<line x1="0" y1="0" x2="0" y2="7" stroke="{PEN}" stroke-width="2.2"/></pattern></defs>')
        for k, (col, op) in enumerate(((UMB, 0.9), ("url(#c14-nt)", 1), ("url(#c14-nt)", 1))):
            b += (f'<polygon points="{a0[k]}" fill="{col}" opacity="{op}" stroke="none">'
                  f'{anim("points", a0[k] + ";" + a1[k], DUR)}</polygon>')
        # bốn tia giới hạn, kéo tới màn
        for (sy, ey0, ey1, c) in ((-rn, yt0, yt1, BLUE), (rn, -yt0, -yt1, BLUE), (rn, yn0, yn1, ORG), (-rn, -yn0, -yn1, ORG)):
            b += (f'<line x1="{X0}" y1="{Y0 + sy:.1f}" x2="{xs0:.1f}" y2="{Y0 + ey0:.1f}" stroke="{c}" stroke-width="1.8">'
                  f'{anim("x2", f"{xs0:.1f};{xs1:.1f}", DUR)}{anim("y2", f"{Y0 + ey0:.1f};{Y0 + ey1:.1f}", DUR)}</line>')
            ty = sy + (ey0 - sy) * (0.5 * (xa - X0) / (xs0 - X0))
            b += chevron(X0 + 0.5 * (xa - X0), Y0 + ty, xs0 - X0, ey0 - sy, c, 1.8, 9)
        b += seg(X0, Y0 - rn, X0, Y0 + rn, SUN, 6)
        b += seg(xa, Y0 - rd, xa, Y0 + rd, "currentColor", 5)
        b += (f'<line x1="{xs0:.1f}" y1="34" x2="{xs0:.1f}" y2="230" stroke="currentColor" stroke-width="2.6">'
              f'{anim("x1", f"{xs0:.1f};{xs1:.1f}", DUR)}{anim("x2", f"{xs0:.1f};{xs1:.1f}", DUR)}</line>')
        b += lbl(X0 - 4, Y0 + rn + 20, "đèn", SUN, 14, "start", "700")
        b += lbl(xa, Y0 + rd + 20, "đĩa chắn", "currentColor", 14, "middle", "700")
        b += lbl(230, 24, "màn dịch ra xa →", "currentColor", 14, "start", "400")
        b += f'<rect x="20" y="240" width="16" height="12" fill="{UMB}" opacity="0.9"/>' + lbl(42, 251, "vùng tối", "currentColor", 14, "start", "400")
        b += f'<rect x="150" y="240" width="16" height="12" fill="url(#c14-nt)" stroke="{PEN}" stroke-width="1"/>' + lbl(172, 251, "vùng nửa tối", "currentColor", 14, "start", "400")
        b += seg(20, 270, 40, 270, BLUE, 2) + lbl(46, 275, "tia cùng mép", BLUE, 14, "start", "400")
        b += seg(150, 270, 170, 270, ORG, 2) + lbl(176, 275, "tia chéo mép", ORG, 14, "start", "400")
        return fig("c14-3-0", "0 0 420 284",
                   "Đèn dạng đĩa, đĩa chắn lớn hơn đèn đặt đồng trục, màn dịch ra xa; vùng tối ở giữa và vùng nửa tối bao quanh lớn dần",
                   b, "Mô phỏng: màn dịch dần ra xa đèn, vùng tối và vành nửa tối trên màn cùng lớn lên. "
                      "Vị trí cuối của màn không phải vị trí trong đề; hai chiều vẽ khác tỉ lệ, không đo trên hình.")
    # hình dữ kiện: cách vẽ tia cùng mép / chéo mép (số đo không theo đề)
    X0, XA, XS = 40, 170, 360
    rn, rd = 20, 34
    def at(y1, y2, x):
        return y1 + (y2 - y1) * (x - X0) / (XA - X0)
    yt = at(-rn, -rd, XS)
    yn = at(rn, -rd, XS)
    b += seg(X0, Y0, XS, Y0, GREY, 1.1, "4 3")
    b += ray(X0, Y0 - rn, XS, Y0 + yt, BLUE, 2, 0.25) + ray(X0, Y0 + rn, XS, Y0 - yt, BLUE, 2, 0.25)
    b += ray(X0, Y0 + rn, XS, Y0 + yn, ORG, 2, 0.25) + ray(X0, Y0 - rn, XS, Y0 - yn, ORG, 2, 0.25)
    b += seg(X0, Y0 - rn, X0, Y0 + rn, SUN, 6) + seg(XA, Y0 - rd, XA, Y0 + rd, "currentColor", 5)
    b += seg(XS, 12, XS, 252, "currentColor", 2.6)
    b += lbl(X0 - 6, Y0 - rn - 2, "A", SUN, 15, "end", "700") + lbl(X0 - 6, Y0 + rn + 12, "B", SUN, 15, "end", "700")
    b += lbl(XA + 6, Y0 - rd - 6, "M", "currentColor", 15, "start", "700") + lbl(XA + 6, Y0 + rd + 16, "N", "currentColor", 15, "start", "700")
    b += f'<text x="{X0 - 8}" y="{Y0 + 3}" fill="{TXT[SUN]}" font-size="14" font-weight="700" text-anchor="end">D<tspan dy="4" font-size="12">n</tspan></text>'
    b += lbl(XA - 8, Y0 + 5, "d", "currentColor", 15, "end", "700")
    b += f'<text x="{XS + 6}" y="{Y0 + yt + 26:.1f}" fill="{TXT[BLUE]}" font-size="14" font-weight="700">d<tspan dy="4" font-size="12">t</tspan><tspan dy="-4"> = ?</tspan></text>'
    b += f'<text x="{XS + 6}" y="{Y0 + yn + 10:.1f}" fill="{TXT[ORG]}" font-size="14" font-weight="700">d<tspan dy="4" font-size="12">n</tspan><tspan dy="-4"> = ?</tspan></text>'
    b += lbl(232, 116, "AM: tia cùng mép", BLUE, 14, "start", "700")
    b += lbl(240, 30, "BM: tia chéo mép", ORG, 14, "end", "700")
    b += hdim(X0, XA, 262, "a", "currentColor", True)
    b += hdim(X0, XS, 280, "L", "currentColor", True)
    return fig("c14-3-2", "0 0 420 290",
               "Đèn AB, đĩa chắn MN, màn; tia cùng mép AM giới hạn vùng tối, tia chéo mép BM giới hạn mép ngoài vùng nửa tối; a đo từ đèn tới đĩa, L từ đèn tới màn",
               b, "Cách vẽ (hình không theo số của đề): tia cùng mép AM cho mép vùng tối, tia chéo mép BM cho mép ngoài vùng nửa tối. "
                  "Khoảng cách a, L đều đo từ đèn.")


BUILD = [d1, d2, d3]

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Định luật phản xạ: đặt gương để hắt tia theo hướng cho trước, gương quay",
      topic=TOPIC_PX,
      problem_html=r"""<p>Ánh nắng chiếu xiên xuống mặt đất: tia nắng đi từ trái sang phải và hợp với phương nằm ngang góc $50^\circ$. Dùng một gương phẳng nhỏ đặt tại điểm $I$ trên đường đi của tia nắng.</p><ol type="a"><li>Muốn tia phản xạ đi thẳng đứng xuống đáy một cái giếng thì góc tới bằng bao nhiêu và phải đặt gương hợp với phương nằm ngang góc bao nhiêu?</li><li>Vẫn tia nắng đó, muốn tia phản xạ hắt thẳng đứng lên trần nhà thì gương phải hợp với phương nằm ngang góc bao nhiêu?</li><li>Trong phòng tối, chiếu một tia laser cố định vào một gương phẳng nhỏ sao cho tia phản xạ đập vuông góc vào bức tường cách điểm tới $4{,}0\ \text{m}$, tạo một vệt sáng. Quay gương một góc $3^\circ$ quanh trục đi qua điểm tới (trục vuông góc với mặt phẳng tới). Vệt sáng trên tường dịch đi bao nhiêu xentimét?</li><li>Muốn vệt sáng dịch $70\ \text{cm}$ so với vị trí ban đầu thì phải quay gương một góc bao nhiêu?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Bóng người dưới đèn đường: chiều dài bóng, tốc độ đỉnh bóng, bóng leo tường, hai đèn",
      topic=TOPIC_BONG,
      problem_html=r"""<p>Một ngọn đèn đường, coi là một điểm sáng, đặt trên đỉnh một cột thẳng đứng cao $H=4{,}5\ \text{m}$. Một người cao $h=1{,}5\ \text{m}$ đi thẳng ra xa chân cột trên mặt đường nằm ngang với tốc độ không đổi $v=1{,}2\ \text{m/s}$.</p><ol type="a"><li>Tính chiều dài bóng của người trên mặt đường khi người cách chân cột $2\ \text{m}$ và khi cách $5\ \text{m}$.</li><li>Đỉnh bóng (bóng của đỉnh đầu) chuyển động với tốc độ bao nhiêu? Mỗi giây bóng dài thêm bao nhiêu?</li><li>Cách chân cột $9\ \text{m}$ có một bức tường thẳng đứng, người đi về phía tường. Người cách chân cột bao nhiêu thì bóng bắt đầu leo lên tường? Khi người cách chân cột $7{,}5\ \text{m}$, phần bóng trên tường cao bao nhiêu?</li><li>Bỏ bức tường đi. Trên đường có thêm một ngọn đèn thứ hai giống hệt, chân cột cách chân cột thứ nhất $12\ \text{m}$. Người đứng yên trên đoạn nối hai chân cột, cách chân cột thứ nhất $4\ \text{m}$. Mỗi đèn tạo ra một bóng của người: tính chiều dài của hai bóng và cho biết mỗi bóng hướng về phía nào.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Nguồn sáng rộng: vùng tối, vùng nửa tối trên màn; đĩa chắn nhỏ hơn nguồn",
      topic=TOPIC_BONG,
      problem_html=r"""<p>Một bóng đèn dạng đĩa tròn phát sáng đều có đường kính $D_n=20\ \text{cm}$. Một đĩa chắn sáng tròn đường kính $d=30\ \text{cm}$ đặt song song với đèn, cách đèn $a=60\ \text{cm}$. Màn chắn đặt song song với đèn, cách đèn $L=180\ \text{cm}$. Tâm đèn và tâm đĩa cùng nằm trên một đường thẳng vuông góc với màn.</p><ol type="a"><li>Nếu đèn chỉ là một điểm sáng đặt tại tâm đèn thì bóng của đĩa trên màn có đường kính bao nhiêu?</li><li>Với đèn thật (đường kính $20\ \text{cm}$), tính đường kính vùng tối và đường kính mép ngoài vùng nửa tối trên màn. Vành nửa tối rộng bao nhiêu?</li><li>Thay đĩa chắn bằng một đĩa đường kính $12\ \text{cm}$ (nhỏ hơn đèn), vẫn cách đèn $60\ \text{cm}$. Màn đặt cách đèn bao xa thì vùng tối vừa biến mất? Khi màn cách đèn $120\ \text{cm}$, vùng tối có đường kính bao nhiêu? Khi màn cách đèn $180\ \text{cm}$, trên màn còn vùng tối không?</li><li>Trở lại đĩa chắn $30\ \text{cm}$. Phải đặt màn cách đèn bao xa để vùng tối có đường kính $60\ \text{cm}$?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1
 [(r'"tia nắng đi từ trái sang phải và hợp với phương nằm ngang góc $50^\circ$"', r"Hướng tia tới; tia $IS$ ngược về phía Mặt Trời hợp phương ngang $50^\circ$",
   r"Ánh sáng truyền thẳng<br>Vẽ tia $IS$ đi ra từ $I$ về phía nguồn"),
  (r'"tia phản xạ đi thẳng đứng xuống đáy một cái giếng"', r"Hướng tia $IR$ đã biết", r"Góc $SIR$ giữa hai tia chung gốc $I$"),
  (r'"Dùng một gương phẳng nhỏ đặt tại điểm $I$"', r"Chưa biết hướng gương",
   r"⚠ góc tới, góc phản xạ đo với pháp tuyến, không đo với mặt gương<br>Định luật phản xạ: $i'=i$, pháp tuyến $IN$ là phân giác góc $SIR$"),
  (r'"góc tới bằng bao nhiêu … hợp với phương nằm ngang góc bao nhiêu?"', r"Cần $i$ và góc gương – phương ngang",
   r"$i=\dfrac{\widehat{SIR}}{2}$; gương vuông góc $IN$"),
  (r'"hắt thẳng đứng lên trần nhà"', r"$IR$ hướng thẳng lên", r"Góc $SIR$ mới, tính lại từ đầu"),
  (r'"tia phản xạ đập vuông góc vào bức tường cách điểm tới $4{,}0\ \text{m}$"', r"$\ell=4{,}0\ \text{m}$",
   r"Tia lúc đầu vuông góc tường: tam giác vuông có cạnh kề $\ell$"),
  (r'"Quay gương một góc $3^\circ$ quanh trục đi qua điểm tới"', r"$\delta=3^\circ$",
   r"⚠ tia tới giữ cố định; gương quay $\delta$ thì tia phản xạ quay $2\delta$ cùng chiều"),
  (r'"Vệt sáng trên tường dịch đi bao nhiêu"', r"Cần $x$", r"$x=\ell\tan(2\delta)$"),
  (r'"Muốn vệt sáng dịch $70\ \text{cm}$"', r"$x'=0{,}70\ \text{m}$", r"Bài ngược: tìm góc quay của tia phản xạ trước, rồi suy ra góc quay của gương")],
 # Dạng 2
 [(r'"ngọn đèn đường, coi là một điểm sáng … cột thẳng đứng cao $H=4{,}5\ \text{m}$"', r"$H=4{,}5\ \text{m}$",
   r"⚠ nguồn điểm: bóng chỉ có vùng tối, mép bóng do tia từ đèn sát đỉnh đầu quyết định<br>Ánh sáng truyền thẳng"),
  (r'"người cao $h=1{,}5\ \text{m}$"', r"$h=1{,}5\ \text{m}$", r"Người và cột cùng thẳng đứng: hai tam giác đồng dạng có chung đỉnh là đỉnh bóng"),
  (r'"đi thẳng ra xa chân cột … $v=1{,}2\ \text{m/s}$"', r"$v=1{,}2\ \text{m/s}$", r"Khoảng cách người – chân cột $x$ tăng $v$ mỗi giây"),
  (r'"chiều dài bóng … khi người cách chân cột $2\ \text{m}$ và khi cách $5\ \text{m}$"', r"$x_1=2\ \text{m}$; $x_2=5\ \text{m}$; cần $\ell$",
   r"$\dfrac{\ell}{x+\ell}=\dfrac{h}{H}$"),
  (r'"Đỉnh bóng … chuyển động với tốc độ bao nhiêu?"', r"Cần $v_{\text{đ}}$", r"Viết vị trí đỉnh bóng $x+\ell$ theo $x$"),
  (r'"bức tường thẳng đứng cách chân cột $9\ \text{m}$"', r"Tường ở $9\ \text{m}$", r"Bóng bắt đầu lên tường khi điểm nào của bóng chạm chân tường?"),
  (r'"Khi người cách chân cột $7{,}5\ \text{m}$, phần bóng trên tường cao bao nhiêu?"', r"$x=7{,}5\ \text{m}$; cần độ cao trên tường",
   r"Tia từ đèn sát đỉnh đầu cắt tường ở đâu? Tam giác đồng dạng có đỉnh tại đèn"),
  (r'"ngọn đèn thứ hai giống hệt … cách chân cột thứ nhất $12\ \text{m}$ … cách chân cột thứ nhất $4\ \text{m}$"', r"Hai đèn, người ở giữa",
   r"Mỗi đèn cho một bóng riêng: với đèn thứ hai, người cách chân cột bao xa? Bóng hướng về phía nào?")],
 # Dạng 3
 [(r'"bóng đèn dạng đĩa tròn … đường kính $D_n=20\ \text{cm}$"', r"$D_n=20\ \text{cm}$",
   r"⚠ nguồn rộng: có vùng tối (không nhận ánh sáng nào của đèn) và vùng nửa tối (nhận ánh sáng từ một phần của đèn)"),
  (r'"đĩa chắn sáng … $d=30\ \text{cm}$ … cách đèn $a=60\ \text{cm}$ … cùng nằm trên một đường thẳng vuông góc với màn"', r"$d=30\ \text{cm}$; $a=60\ \text{cm}$",
   r"Hình đối xứng qua trục: chỉ cần tính nửa trên rồi nhân đôi"),
  (r'"Màn chắn … cách đèn $L=180\ \text{cm}$"', r"$L=180\ \text{cm}$", r"⚠ mọi khoảng cách đo từ đèn; tỉ số đồng dạng dùng $\dfrac{L}{a}$"),
  (r'"Nếu đèn chỉ là một điểm sáng"', r"Cần $d'$", r"$d'=d\,\dfrac{L}{a}$"),
  (r'"đường kính vùng tối và đường kính mép ngoài vùng nửa tối"', r"Cần $d_t$; $d_n$",
   r"Tia cùng mép (mép trên đèn – mép trên đĩa) cho mép vùng tối<br>Tia chéo mép (mép dưới đèn – mép trên đĩa) cho mép ngoài nửa tối"),
  (r'"đĩa đường kính $12\ \text{cm}$ (nhỏ hơn đèn)"', r"$d_2=12\ \text{cm}$", r"Tia cùng mép giờ đi chụm về trục: vùng tối co lại khi lùi màn"),
  (r'"Khi màn cách đèn $180\ \text{cm}$, trên màn còn vùng tối không?"', r"$L=180\ \text{cm}$", r"So với khoảng cách lúc vùng tối vừa biến mất"),
  (r'"để vùng tối có đường kính $60\ \text{cm}$"', r"Cần $L'$", r"Đường kính vùng tối thay đổi theo $L$ thế nào? Có tỉ lệ thuận với $L$ không?")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> góc tới $i$ là góc giữa tia tới và pháp tuyến tại điểm tới; góc giữa tia và mặt gương bằng $90^\circ-i$.",
      r"<strong>Định luật:</strong> tia phản xạ nằm trong mặt phẳng tới; góc phản xạ bằng góc tới, $i'=i$.",
      r"<strong>Hệ quả:</strong> góc giữa tia tới và tia phản xạ $\widehat{SIR}=2i$; pháp tuyến là phân giác của góc đó; gương vuông góc pháp tuyến.",
      r"<strong>Gương quay:</strong> tia tới cố định, gương quay $\delta$ thì tia phản xạ quay $2\delta$ cùng chiều."]
R2 = [r"<strong>Khái niệm:</strong> ánh sáng truyền thẳng; bóng là vùng không nhận được ánh sáng từ nguồn.",
      r"<strong>Nguồn điểm:</strong> mép bóng do tia từ đèn đi sát đỉnh đầu quyết định.",
      r"<strong>Công thức:</strong> tam giác đồng dạng $\dfrac{\ell}{x+\ell}=\dfrac{h}{H}$, suy ra $\ell=\dfrac{h\,x}{H-h}$.",
      r"<strong>Điều kiện:</strong> cột và người cùng thẳng đứng, mặt đường nằm ngang."]
R3 = [r"<strong>Khái niệm:</strong> vùng tối không nhận ánh sáng nào của nguồn; vùng nửa tối chỉ nhận ánh sáng từ một phần của nguồn.",
      r"<strong>Cách vẽ:</strong> tia cùng mép (mép trên đèn – mép trên đĩa) cho mép vùng tối; tia chéo mép (mép dưới đèn – mép trên đĩa) cho mép ngoài nửa tối.",
      r"<strong>Công thức:</strong> $d_t=D_n+(d-D_n)\dfrac{L}{a}$; $d_n=(d+D_n)\dfrac{L}{a}-D_n$; nguồn điểm $d'=d\,\dfrac{L}{a}$.",
      r"<strong>Điều kiện:</strong> nguồn, đĩa, màn song song và đồng trục; $a$, $L$ đo từ nguồn."]

SOLS = [
 sol(R1, [
  ("Góc giữa tia tới và tia phản xạ", [P(r"Tia $IS$ (ngược về phía Mặt Trời) ở phía trên phương ngang $50^\circ$; tia $IR$ thẳng đứng xuống, ở phía dưới phương ngang $90^\circ$:"),
     M(r"\widehat{SIR}=50^\circ+90^\circ"), A(r"\widehat{SIR}=140^\circ")]),
  ("Góc tới và cách đặt gương", [P(r"Pháp tuyến $IN$ là phân giác của góc $SIR$:"), M(r"i=i'=\dfrac{140^\circ}{2}=70^\circ"),
     P(r"$IN$ hợp với tia $IR$ (thẳng đứng) góc $70^\circ$. Gương vuông góc với $IN$ nên gương hợp với phương ngang cùng góc đó:"),
     A(r"i=70^\circ;\ \text{gương hợp phương ngang } 70^\circ")]),
  ("Hắt lên trần", [P(r"Giờ $IS$ và $IR$ cùng ở phía trên phương ngang: $IS$ thấp $50^\circ$, $IR$ thẳng đứng $90^\circ$, hai góc trừ nhau:"),
     M(r"\widehat{SIR}=90^\circ-50^\circ=40^\circ"), M(r"i=\dfrac{40^\circ}{2}=20^\circ"),
     P(r"$IN$ hợp với phương thẳng đứng $20^\circ$, nên gương hợp với phương ngang:"), A(r"20^\circ")]),
  ("Vệt sáng dịch khi quay gương", [P(r"Tia tới cố định, gương quay $\delta=3^\circ$ thì tia phản xạ quay:"), M(r"2\delta=6^\circ"),
     P(r"Tia lúc đầu vuông góc với tường, nên vệt sáng dịch:"), M(r"x=\ell\tan(2\delta)=4{,}0\cdot\tan6^\circ"),
     A(r"x\approx0{,}42\ \text{m}=42\ \text{cm}")]),
  ("Góc quay để vệt dịch 70 cm", [P(r"Góc quay của tia phản xạ:"), M(r"\tan\varphi=\dfrac{0{,}70}{4{,}0}=0{,}175\ \Rightarrow\ \varphi\approx9{,}93^\circ"),
     P(r"Gương chỉ quay nửa góc đó:"), A(r"\delta=\dfrac{\varphi}{2}\approx4{,}96^\circ\approx5^\circ")]),
  ("Kiểm tra", [P(r"Câu a: tia phản xạ hợp pháp tuyến $70^\circ$ bằng góc tới ✓; góc giữa tia và mặt gương $90^\circ-70^\circ=20^\circ$ ở cả hai phía ✓."),
     P(r"Câu c: góc nhỏ, $\tan6^\circ\approx0{,}105$, $4\cdot0{,}105\approx0{,}42\ \text{m}$ ✓. Nếu quên $2\delta$ sẽ ra khoảng một nửa, sai."),
     P(r"Câu d: $70\ \text{cm}$ lớn hơn $42\ \text{cm}$ khoảng $1{,}7$ lần nên góc quay lớn hơn $3^\circ$ chút ít ✓.")])],
  [r"a) $i=70^\circ$; gương hợp phương ngang $70^\circ$", r"b) Gương hợp phương ngang $20^\circ$ (khi đó $i=20^\circ$)",
   r"c) Vệt sáng dịch khoảng $42\ \text{cm}$", r"d) Quay gương khoảng $4{,}96^\circ\approx5^\circ$"],
  r"Nhận dạng: thấy <strong>muốn tia phản xạ đi theo hướng cho trước</strong> → tìm góc $SIR$, pháp tuyến là phân giác; thấy <strong>quay gương</strong> → tia quay $2\delta$."),
 sol(R2, [
  ("Chiều dài bóng ở hai vị trí", [P(r"Gọi $T$ là đỉnh bóng. Tam giác tạo bởi người và bóng đồng dạng với tam giác tạo bởi cột và đoạn chân cột – $T$:"),
     M(r"\dfrac{\ell}{x+\ell}=\dfrac{h}{H}\ \Rightarrow\ \ell=\dfrac{h\,x}{H-h}=\dfrac{1{,}5\,x}{3}=\dfrac{x}{2}"),
     M(r"x=2\ \text{m}:\ \ell=1{,}00\ \text{m}"), A(r"x=5\ \text{m}:\ \ell=2{,}50\ \text{m}")]),
  ("Tốc độ đỉnh bóng", [P(r"Vị trí đỉnh bóng tính từ chân cột:"), M(r"x_T=x+\ell=\dfrac{H}{H-h}\,x=1{,}5\,x"),
     P(r"Mỗi giây $x$ tăng $v=1{,}2\ \text{m}$ nên $x_T$ tăng:"), M(r"v_{\text{đ}}=\dfrac{H}{H-h}\,v=1{,}5\cdot1{,}2"), A(r"v_{\text{đ}}=1{,}80\ \text{m/s}"),
     P(r"Bóng dài thêm mỗi giây $v_{\text{đ}}-v=0{,}60\ \text{m}$.")]),
  ("Lúc bóng bắt đầu leo tường", [P(r"Bóng bắt đầu lên tường khi đỉnh bóng chạm chân tường:"), M(r"x_T=1{,}5\,x=9"), A(r"x=6{,}00\ \text{m}")]),
  ("Phần bóng trên tường", [P(r"Tia từ đèn sát đỉnh đầu: đi ngang $7{,}5\ \text{m}$ thì hạ xuống $H-h=3\ \text{m}$. Tới tường nó đi ngang $9\ \text{m}$, hạ xuống:"),
     M(r"\Delta y=3\cdot\dfrac{9}{7{,}5}=3{,}6\ \text{m}"), M(r"y=H-\Delta y=4{,}5-3{,}6"), A(r"y=0{,}90\ \text{m}"),
     P(r"Phần bóng trên sàn là đoạn từ chân người tới chân tường: $9-7{,}5=1{,}5\ \text{m}$.")]),
  ("Hai đèn", [P(r"Mỗi đèn dùng khoảng cách từ người tới chân cột của chính nó."),
     M(r"\text{Đèn 1 } (x=4\ \text{m}):\ \ell_1=\dfrac{4}{2}=2{,}00\ \text{m}"), M(r"\text{Đèn 2 } (x=12-4=8\ \text{m}):\ \ell_2=\dfrac{8}{2}"),
     A(r"\ell_2=4{,}00\ \text{m}"),
     P(r"Mỗi bóng hướng ra xa đèn tạo ra nó: bóng do đèn 1 hướng về phía đèn 2, bóng do đèn 2 hướng về phía đèn 1; hai bóng ngược chiều nhau.")]),
  ("Kiểm tra", [P(r"Câu a: $\ell=x/2$, đi xa gấp $2{,}5$ lần thì bóng dài gấp $2{,}5$ lần ✓."),
     P(r"Câu b: đỉnh bóng nhanh hơn người vì bóng còn dài ra ✓; $v_{\text{đ}}$ không phụ thuộc vị trí của người."),
     P(r"Câu c: tại $x=6\ \text{m}$ công thức độ cao trên tường cho $4{,}5-3\cdot\dfrac96=0$ ✓; $0\lt0{,}9\ \text{m}\lt h$ ✓."),
     P(r"Câu d: đỉnh bóng do đèn 2 ở cách chân cột 1 là $4-4=0$, đúng tại chân cột 1 ✓ (một trường hợp đặc biệt của số liệu).")])],
  [r"a) $\ell=1{,}00\ \text{m}$ (cách $2\ \text{m}$); $\ell=2{,}50\ \text{m}$ (cách $5\ \text{m}$)", r"b) $v_{\text{đ}}=1{,}80\ \text{m/s}$; bóng dài thêm $0{,}60\ \text{m}$ mỗi giây",
   r"c) Bóng lên tường khi người cách cột $6{,}00\ \text{m}$; phần trên tường cao $0{,}90\ \text{m}$", r"d) $\ell_1=2{,}00\ \text{m}$ hướng về đèn 2; $\ell_2=4{,}00\ \text{m}$ hướng về đèn 1"],
  r"Nhận dạng: thấy <strong>người đi dưới đèn đường, bóng dài bao nhiêu, chạy nhanh bao nhiêu</strong> → hai tam giác đồng dạng, đỉnh bóng $x_T=\dfrac{H}{H-h}x$."),
 sol(R3, [
  ("Bóng khi coi đèn là điểm sáng", [P(r"Tia từ tâm đèn qua mép đĩa; tỉ số đồng dạng đỉnh tại nguồn:"), M(r"d'=d\,\dfrac{L}{a}=30\cdot\dfrac{180}{60}"), A(r"d'=90\ \text{cm}")]),
  ("Đường kính vùng tối", [P(r"Tia cùng mép đi từ mép trên đèn (cao $10\ \text{cm}$) qua mép trên đĩa (cao $15\ \text{cm}$): cứ $60\ \text{cm}$ theo trục thì lên $5\ \text{cm}$. Tới màn ($180\ \text{cm}$, gấp $3$ lần):"),
     M(r"\dfrac{d_t}{2}=10+5\cdot3=25\ \text{cm}"), A(r"d_t=D_n+(d-D_n)\dfrac{L}{a}=50\ \text{cm}")]),
  ("Mép ngoài vùng nửa tối", [P(r"Tia chéo mép đi từ mép dưới đèn ($-10\ \text{cm}$) qua mép trên đĩa ($15\ \text{cm}$): cứ $60\ \text{cm}$ lên $25\ \text{cm}$. Tới màn:"),
     M(r"\dfrac{d_n}{2}=-10+25\cdot3=65\ \text{cm}"), A(r"d_n=(d+D_n)\dfrac{L}{a}-D_n=130\ \text{cm}"),
     P(r"Vành nửa tối rộng $\dfrac{130-50}{2}=40\ \text{cm}$.")]),
  ("Đĩa nhỏ hơn đèn: lúc vùng tối biến mất", [P(r"Với $d_2=12\ \text{cm}$, $d_2-D_n=-8\ \text{cm}$ âm: tia cùng mép đi chụm về trục, vùng tối co lại khi lùi màn. Cho $d_t=0$:"),
     M(r"20-8\cdot\dfrac{L_0}{60}=0"), A(r"L_0=\dfrac{a\,D_n}{D_n-d_2}=150\ \text{cm}")]),
  ("Vùng tối khi màn cách 120 cm", [M(r"d_t=20-8\cdot\dfrac{120}{60}=20-16"), A(r"d_t=4{,}0\ \text{cm}"),
     P(r"Mép ngoài nửa tối lúc đó: $d_n=32\cdot2-20=44\ \text{cm}$.")]),
  ("Màn cách 180 cm", [P(r"$180\ \text{cm}\gt L_0=150\ \text{cm}$: hai tia cùng mép đã cắt nhau trên trục trước khi tới màn, nên <strong>không còn vùng tối</strong>; công thức cho số âm $20-8\cdot3=-4$, không phải đường kính."),
     P(r"Giữa màn là vùng nửa tối; ngay chính giữa vẫn thấy được vành ngoài của đèn quanh đĩa. Mép ngoài nửa tối: $d_n=32\cdot3-20=76\ \text{cm}$."),
     P(r"Liên hệ: chóp vùng tối của Mặt Trăng không chạm tới Trái Đất thì có nhật thực hình khuyên (xem chuyên đề Thiên văn).")]),
  ("Đặt màn để vùng tối 60 cm", [P(r"Với đĩa $30\ \text{cm}$:"), M(r"20+10\cdot\dfrac{L'}{60}=60"), A(r"L'=240\ \text{cm}"),
     P(r"Lúc đó mép ngoài nửa tối $d_n=50\cdot4-20=180\ \text{cm}$.")]),
  ("Kiểm tra", [P(r"Câu b: $d_t=50\ \text{cm}\lt d'=90\ \text{cm}\lt d_n=130\ \text{cm}$: bóng nguồn điểm nằm giữa mép vùng tối và mép ngoài nửa tối ✓."),
     P(r"Câu c: tại $L=a=60\ \text{cm}$ công thức cho $d_t=12\ \text{cm}=d_2$, đúng bằng đĩa ✓."),
     P(r"Câu d: $d_t$ không tỉ lệ thuận với $L$ (còn số hạng $D_n$), nên vùng tối $60\ \text{cm}$ không ứng với $L=180\cdot\dfrac{60}{50}$ ✓.")])],
  [r"a) $d'=90\ \text{cm}$", r"b) $d_t=50\ \text{cm}$; $d_n=130\ \text{cm}$; vành nửa tối rộng $40\ \text{cm}$",
   r"c) Vùng tối biến mất khi $L=150\ \text{cm}$; tại $120\ \text{cm}$: $d_t=4{,}0\ \text{cm}$; tại $180\ \text{cm}$: không còn vùng tối",
   r"d) $L'=240\ \text{cm}$"],
  r"Nhận dạng: thấy <strong>nguồn sáng có kích thước, vùng tối, vùng nửa tối</strong> → vẽ tia cùng mép và tia chéo mép, đồng dạng đỉnh tại mép nguồn, mọi khoảng cách đo từ nguồn."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>muốn tia phản xạ đi theo hướng cho trước</b> → tìm góc $SIR$; thấy <b>quay gương</b> → tia phản xạ quay $2\delta$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Góc giữa tia tới và tia phản xạ", "Câu a: góc SIR giữa tia tới và tia phản xạ bằng bao nhiêu độ?", 140, "°", 0.5,
       loi=r"Lấy góc giữa hướng truyền của tia nắng và hướng truyền của tia phản xạ, thay vì góc giữa hai tia $IS$, $IR$ cùng xuất phát từ $I$."),
  buoc("Góc tới và cách đặt gương", "Câu a: gương hợp với phương nằm ngang góc bao nhiêu độ?", 70, "°", 0.5,
       loi=r"Lấy góc giữa tia và mặt gương làm góc tới, hoặc đặt mặt gương theo phân giác của góc $SIR$.",
       ke=[(r"Kẻ pháp tuyến $IN$ là phân giác của góc $SIR$, rồi đặt gương vuông góc với $IN$", True),
           (r"Đặt mặt gương theo phân giác của góc $SIR$", r"Phân giác của góc $SIR$ là pháp tuyến; mặt gương phải vuông góc với nó."),
           (r"Lấy góc tới bằng cả góc $SIR$", r"Góc $SIR$ gồm cả góc tới và góc phản xạ, bằng $2i$.")]),
  buoc("Hắt lên trần", "Câu b: gương hợp với phương nằm ngang góc bao nhiêu độ?", 20, "°", 0.5,
       loi=r"Vẫn cộng góc của tia nắng với $90^\circ$ như câu a; khi tia phản xạ hướng lên, hai tia cùng ở phía trên phương ngang nên phải trừ.",
       ke=[(r"Tính lại góc $SIR$ giữa $IS$ và tia hướng thẳng lên, rồi chia đôi", True),
           (r"Cộng góc của tia nắng với $90^\circ$ như câu a", r"Tia phản xạ giờ hướng lên, cùng phía trên phương ngang với $IS$, nên hai góc trừ nhau chứ không cộng."),
           (r"Giữ nguyên góc gương của câu a, chỉ lật mặt phản xạ lên trên", r"Lật gương thì tia nắng chiếu vào mặt sau; hướng tia phản xạ đổi nên góc $SIR$ phải tính lại.")]),
  buoc("Vệt sáng dịch khi quay gương", "Câu c: vệt sáng dịch đi bao nhiêu xentimét?", 42, "cm", 1,
       loi=r"Cho tia phản xạ quay đúng bằng góc quay của gương; tia tới cố định thì góc giữa tia tới và tia phản xạ đổi gấp đôi.",
       ke=[(r"Tìm góc quay của tia phản xạ là $2\delta$, rồi dùng $x=\ell\tan(2\delta)$", True),
           (r"Dùng $x=\ell\tan\delta$ với $\delta$ là góc quay của gương", r"Gương quay $\delta$ thì góc tới đổi $\delta$, góc giữa tia tới và tia phản xạ đổi $2\delta$."),
           (r"Tính cung $x=\ell\cdot2\delta$ với góc để theo độ", r"Công thức độ dài cung cần góc đo bằng radian; để theo độ thì số sai hàng chục lần.")]),
  buoc("Góc quay để vệt dịch 70 cm", "Câu d: phải quay gương bao nhiêu độ?", 4.96, "°", 0.06,
       loi=r"Tìm được góc quay của tia phản xạ rồi lấy luôn làm góc quay của gương, quên chia đôi.",
       ke=[(r"Tìm góc quay $\varphi$ của tia phản xạ từ $\tan\varphi=\dfrac{x'}{\ell}$, rồi lấy một nửa", True),
           (r"Lấy góc quay của gương bằng $\varphi$ với $\tan\varphi=\dfrac{x'}{\ell}$", r"$\varphi$ là góc quay của tia phản xạ; gương chỉ quay nửa góc đó."),
           (r"Lấy góc quay của gương bằng $2\varphi$", r"Ngược quan hệ: tia phản xạ quay gấp đôi gương, không phải gương quay gấp đôi tia.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>người đi dưới đèn đường, bóng dài bao nhiêu, đỉnh bóng chạy nhanh bao nhiêu</b> → hai tam giác đồng dạng chung đỉnh bóng.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Chiều dài bóng ở hai vị trí", "Khi người cách chân cột 5 m, bóng dài bao nhiêu mét?", 2.5, "m", 0.03,
       loi=r"Viết tỉ số đồng dạng $\dfrac{\ell}{x}=\dfrac{h}{H}$: cạnh ứng với $H$ phải là cả đoạn từ chân cột tới đỉnh bóng $x+\ell$, không phải $x$."),
  buoc("Tốc độ đỉnh bóng", "Đỉnh bóng chuyển động với tốc độ bao nhiêu m/s?", 1.8, "m/s", 0.02,
       loi=r"Cho rằng đỉnh bóng chạy cùng tốc độ với người, hoặc lấy tốc độ dài ra của bóng làm tốc độ đỉnh bóng.",
       ke=[(r"Viết vị trí đỉnh bóng $x+\ell$ theo $x$, rồi xem nó tăng bao nhiêu khi $x$ tăng $v$ trong $1\ \text{s}$", True),
           (r"Lấy tốc độ đỉnh bóng bằng $v$ vì bóng đi theo người", r"Bóng dài ra khi người đi xa đèn, nên đỉnh bóng phải nhanh hơn người."),
           (r"Lấy tốc độ đỉnh bóng bằng tốc độ dài ra của bóng", r"Đó là tốc độ của đỉnh bóng so với người; so với mặt đất phải cộng thêm tốc độ của người.")]),
  buoc("Lúc bóng bắt đầu leo tường", "Người cách chân cột bao nhiêu mét thì bóng bắt đầu leo lên tường?", 6, "m", 0.05,
       loi=r"Cho chiều dài bóng bằng khoảng cách từ cột tới tường; bóng bắt đầu từ chân người nên mốc chạm tường là đỉnh bóng $x+\ell$.",
       ke=[(r"Cho vị trí đỉnh bóng $x+\ell$ bằng khoảng cách từ chân cột tới tường", True),
           (r"Cho chiều dài bóng $\ell$ bằng khoảng cách từ chân cột tới tường", r"Bóng bắt đầu từ chân người, không từ chân cột; mốc chạm tường là đỉnh bóng."),
           (r"Dùng $\ell=\dfrac{h\,x}{H}$ rồi cho $x+\ell$ bằng khoảng cách tới tường", r"Tỉ số đồng dạng sai: cạnh ứng với $h$ là $\ell$, cạnh ứng với $H$ là $x+\ell$, nên $\ell=\dfrac{h\,x}{H-h}$.")]),
  buoc("Phần bóng trên tường", "Khi người cách chân cột 7,5 m, phần bóng trên tường cao bao nhiêu mét?", 0.9, "m", 0.02,
       loi=r"Lấy phần bóng thừa ra sau chân tường (khi coi như không có tường) làm chiều cao bóng trên tường; tường dựng đứng chặn tia nên phải tìm chỗ tia cắt tường.",
       ke=[(r"Tìm chỗ tia từ đèn sát đỉnh đầu cắt tường, bằng tam giác đồng dạng có đỉnh tại đèn", True),
           (r"Lấy phần bóng thừa ra sau chân tường khi coi như không có tường", r"Tường dựng đứng chặn tia; phần trên tường là độ cao chỗ tia cắt tường, không bằng phần bóng thừa trên sàn."),
           (r"Lấy chiều cao bóng trên tường bằng chiều cao người", r"Bóng của đỉnh đầu chỉ cao bằng người khi tia nằm ngang, tức đèn thấp ngang đầu; ở đây tia đi chếch xuống.")]),
  buoc("Hai đèn", "Bóng do đèn thứ hai tạo ra dài bao nhiêu mét?", 4, "m", 0.03,
       loi=r"Dùng khoảng cách tới cột thứ nhất (hoặc cả khoảng cách giữa hai cột) cho đèn thứ hai; mỗi bóng dùng khoảng cách từ người tới chân cột của chính đèn tạo ra nó.",
       ke=[(r"Áp dụng công thức của câu a riêng cho từng đèn, mỗi đèn dùng khoảng cách từ người tới chân cột của nó", True),
           (r"Dùng khoảng cách giữa hai chân cột cho đèn thứ hai", r"Người không đứng ở chân cột 1; khoảng cách tới cột 2 là hiệu hai khoảng cách đã cho."),
           (r"Cho hai bóng dài bằng nhau vì hai đèn giống hệt nhau", r"Người đứng lệch về phía đèn 1 nên khoảng cách tới hai cột khác nhau, hai bóng dài khác nhau.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>bóng đèn có kích thước, vùng tối, vùng nửa tối</b> → vẽ tia cùng mép và tia chéo mép, khoảng cách đo từ nguồn.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Bóng khi coi đèn là điểm sáng", "Câu a: bóng của đĩa có đường kính bao nhiêu xentimét?", 90, "cm", 0.5,
       loi=r"Lấy tỉ số theo khoảng cách từ đĩa tới màn $L-a$ thay vì khoảng cách từ nguồn tới màn $L$."),
  buoc("Đường kính vùng tối", "Câu b: vùng tối có đường kính bao nhiêu xentimét?", 50, "cm", 0.5,
       loi=r"Chỉ vẽ tia từ tâm đèn nên ra bóng của nguồn điểm; với nguồn rộng, mép vùng tối do tia cùng mép quyết định.",
       ke=[(r"Vẽ tia cùng mép: từ mép trên của đèn qua mép trên của đĩa, tìm độ cao nó chạm màn", True),
           (r"Vẽ tia từ mép dưới của đèn qua mép trên của đĩa", r"Tia chéo mép đó giới hạn mép ngoài vùng nửa tối, không phải vùng tối."),
           (r"Lấy bóng nguồn điểm trừ đi đường kính đèn", r"Mép đèn lệch khỏi trục được phóng theo tỉ số khác với mép đĩa, nên không trừ thẳng được; phải tính theo tia cùng mép.")]),
  buoc("Mép ngoài vùng nửa tối", "Câu b: mép ngoài vùng nửa tối có đường kính bao nhiêu xentimét?", 130, "cm", 1,
       loi=r"Vẽ tia chéo mép nhưng lấy điểm xuất phát ở mép trên của đèn (dấu cộng), tức là vẽ lại tia cùng mép.",
       ke=[(r"Vẽ tia chéo mép: từ mép dưới của đèn qua mép trên của đĩa", True),
           (r"Dùng lại tia cùng mép của bước trước", r"Tia cùng mép cho mép vùng tối; ngoài mép nửa tối mới thấy được toàn bộ đèn, đó là tia chéo mép."),
           (r"Cộng đường kính đèn vào bóng nguồn điểm", r"Tia chéo mép đi qua mép đĩa nên độ lệch của mép đèn đổi dấu và bị phóng theo tỉ số đồng dạng, không cộng thẳng được.")]),
  buoc("Đĩa nhỏ hơn đèn: lúc vùng tối biến mất", "Câu c: màn cách đèn bao nhiêu xentimét thì vùng tối vừa biến mất?", 150, "cm", 1,
       loi=r"Nghĩ rằng vùng tối luôn lớn dần khi lùi màn; với đĩa nhỏ hơn đèn, tia cùng mép đi chụm về trục nên vùng tối co lại.",
       ke=[(r"Viết đường kính vùng tối theo $L$ với đĩa $12\ \text{cm}$ rồi cho bằng $0$", True),
           (r"Cho bóng nguồn điểm $d_2\,\dfrac{L}{a}$ bằng đường kính đèn", r"Bóng nguồn điểm chỉ dùng khi coi nguồn là điểm; vùng tối do tia cùng mép quyết định."),
           (r"Cho đường kính mép ngoài nửa tối bằng $0$", r"Mép ngoài nửa tối luôn lớn dần khi lùi màn, không bao giờ bằng $0$ sau đĩa.")]),
  buoc("Vùng tối khi màn cách 120 cm", "Câu c: khi màn cách đèn 120 cm, vùng tối có đường kính bao nhiêu xentimét?", 4, "cm", 0.2,
       loi=r"Dùng công thức vùng tối nhưng viết $D_n-d$ thay cho $d-D_n$, tức cho tia cùng mép đi loe ra.",
       ke=[(r"Thay $L$ vào $d_t=D_n+(d_2-D_n)\dfrac{L}{a}$, chú ý $d_2-D_n$ âm", True),
           (r"Lấy $d_2\,\dfrac{L}{a}$", r"Đó là bóng khi coi nguồn là điểm; nguồn rộng thì vùng tối nhỏ hơn thế."),
           (r"Lấy $D_n+(D_n-d_2)\dfrac{L}{a}$", r"Tia cùng mép đi từ mép đèn ở độ cao $D_n/2$ xuống mép đĩa ở $d_2/2$; đảo dấu là cho tia đi lên.")]),
  buoc("Màn cách 180 cm", "Câu c: khi màn cách đèn 180 cm, trên màn có gì?",
       lua_chon=[(r"Không còn vùng tối; giữa màn là vùng nửa tối, ngay chính giữa vẫn thấy vành ngoài của đèn", True),
                 (r"Vẫn còn một vùng tối nhỏ ở giữa màn", r"Màn ở xa hơn chỗ vùng tối vừa biến mất; các tia cùng mép đã cắt nhau trước màn nên điểm nào cũng thấy được một phần đèn."),
                 (r"Màn sáng đều, không còn bóng", r"Đĩa vẫn che một phần đèn đối với các điểm gần giữa màn, nên vẫn có vùng nửa tối.")],
       loi=r"Thế số được đường kính âm rồi lấy trị tuyệt đối làm đường kính vùng tối.",
       ke=[(r"So khoảng cách màn với khoảng cách lúc vùng tối vừa biến mất", True),
           (r"Thế số rồi lấy trị tuyệt đối của kết quả làm đường kính vùng tối", r"Kết quả âm nghĩa là tia cùng mép đã cắt nhau trước màn, không còn vùng tối."),
           (r"Dùng bóng nguồn điểm: bóng $d_2\,\dfrac{L}{a}$ luôn có nên vẫn có vùng tối", r"Với nguồn rộng, điểm nào còn thấy một phần đèn thì không tối hẳn.")]),
  buoc("Đặt màn để vùng tối 60 cm", "Câu d: phải đặt màn cách đèn bao nhiêu xentimét?", 240, "cm", 1,
       loi=r"Dùng công thức bóng nguồn điểm cho vùng tối, hoặc coi đường kính vùng tối tỉ lệ thuận với khoảng cách tới màn.",
       ke=[(r"Cho $D_n+(d-D_n)\dfrac{L'}{a}$ bằng đường kính vùng tối cần có rồi giải $L'$", True),
           (r"Cho $d\,\dfrac{L'}{a}$ bằng đường kính vùng tối cần có", r"Đó là bóng của nguồn điểm; với nguồn rộng, vùng tối nhỏ hơn bóng đó."),
           (r"Nhân khoảng cách ban đầu với tỉ số hai đường kính vùng tối", r"Đường kính vùng tối không tỉ lệ thuận với $L$ vì còn số hạng $D_n$ không đổi.")]),
  buoc("Kiểm tra")]),
]


def kiem_so():
    F = Fr
    # D1
    assert SIR_A == 140 and I_A == 70 and SIR_B == 40 and I_B == 20
    assert abs(X_C * 100 - 42.04) < 0.05 and round(X_C * 100) == 42
    assert abs(PHI_D - 9.926) < 0.01 and abs(DELTA_D - 4.963) < 0.01
    # kiểm véc-tơ (trục y lên): tia nắng hướng −50°, gương hợp ngang 70° → phản xạ thẳng xuống; gương 20° → thẳng lên
    def u(deg): return (math.cos(math.radians(deg)), math.sin(math.radians(deg)))
    def rf(v, mdeg):
        m = u(mdeg); dd = v[0] * m[0] + v[1] * m[1]
        return (2 * dd * m[0] - v[0], 2 * dd * m[1] - v[1])
    r_a = rf(u(-BETA_NANG), 180 - 70); assert abs(r_a[0]) < 1e-9 and r_a[1] < 0
    r_b = rf(u(-BETA_NANG), 20); assert abs(r_b[0]) < 1e-9 and r_b[1] > 0
    # cách sai D1 khác đáp án
    assert 90 - BETA_NANG != SIR_A                      # góc giữa hai hướng truyền = 40 ≠ 140
    assert SIR_A != I_A and (SIR_A / 2) != 90 - I_A + 0.5
    assert (BETA_NANG + 90) / 2 != 20                  # cộng như câu a ở câu b → 70
    assert abs(L_TUONG * math.tan(math.radians(DELTA)) * 100 - 42) > 5   # quên 2δ → 21 cm
    assert abs(L_TUONG * 2 * DELTA * 100 - 42) > 100                   # cung theo độ
    assert abs(PHI_D - 4.96) > 1 and abs(2 * PHI_D - 4.96) > 1
    # D2
    assert bong(2) == 1 and bong(5) == F(5, 2)
    assert V_DINH == F(9, 5) and V_DAI == F(3, 5)
    assert X_CHAM == 6 and Y_TUONG == F(9, 10) and X_TUONG - X_N == F(3, 2)
    assert bong(X_P) == 2 and bong(KC2 - X_P) == 4 and X_P - bong(KC2 - X_P) == 0
    # kiểm D2 bằng giao điểm đường thẳng: tia (0,H) qua (x,h) chạm đất tại x_T
    for x in (2, 5, F(15, 2)):
        xT = x * H2 / (H2 - h2); assert xT - x == bong(x)
    # cách sai D2 khác đáp án
    assert h2 * 5 / H2 != F(5, 2)                                  # ℓ = h x / H
    assert v2 != V_DINH and V_DAI != V_DINH
    assert X_TUONG * (H2 - h2) / h2 != 6 and X_TUONG / (1 + h2 / H2) != 6   # ℓ = 9 → x = 18; ℓ = hx/H → 6,75
    assert X_N + bong(X_N) - X_TUONG != Y_TUONG and h2 != Y_TUONG          # phần thừa 2,25 m; chiều cao người
    assert bong(KC2) != 4 and bong(X_P) != 4                               # dùng 12 m → 6 m; dùng 4 m → 2 m
    # D3
    assert D_DIEM == 90 and DT3 == 50 and DNG3 == 130 and (DNG3 - DT3) / 2 == 40
    assert L_MAT == 150 and DT_120 == 4 and DNG_120 == 44 and DT_180 == -4 and DNG_180 == 76
    assert L_60 == 240 and d_ngoai(DN, D3D, A3, L_60) == 180 and d_toi(DN, D3D, A3, L_60) == 60
    assert d_toi(DN, D_NHO, A3, A3) == D_NHO and d_toi(DN, D3D, A3, A3) == D3D
    # cách sai D3 khác đáp án
    assert Fr(D3D * (L3 - A3), A3) != 90                                   # dùng L − a → 60
    assert D_DIEM - DN != 50 and D_DIEM + DN != 130 and 2 * DT3 != 130      # 70; 110; 100
    assert Fr(A3 * DN, D_NHO) != 150                                       # d₂L/a = D_n → L = 100
    assert Fr(D_NHO * 120, A3) != 4 and DN + Fr(DN - D_NHO) * 120 / A3 != 4  # 24; 36
    assert Fr(60 * A3, D3D) != 240 and Fr(L3 * 60, 50) != 240               # 120; 216
    print("kiểm số liệu D1–D3 (bài 158): đạt")
