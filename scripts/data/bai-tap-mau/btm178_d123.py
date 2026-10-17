"""Bài tập mẫu CĐ17 "Thiên văn: Mặt Trăng, Hệ Mặt Trời và Ngân Hà" (lesson 178) — Dạng 1–3 (phần đọc buổi 13: pha Mặt Trăng,
nhật thực, nguyệt thực). Module được build-hinh-178.py import.
Dàn ý + số liệu đã tính: content/hsg9/cd17-thien-van/nguon.md (mục "Bài tập mẫu", D1–D3) + tinh.py — dùng nguyên số.
Quy ước: 1 AU = 1,5·10^8 km; D_S = 1,39·10^6 km; D_E = 12 740 km (R_E = 6370 km); D_M = 3470 km; d_M 363 000 / 384 000 / 405 000 km;
Tuần Trăng S = 29,5 ngày (đề dễ). Góc trông α ≈ D/ℓ (rad), đổi độ nhân 180/π.
YCCĐ "bài tương tự": "Pha Mặt Trăng, nhật thực và nguyệt thực".
Mọi đáp số tính lại bằng Python trong kiem_so(); mọi lựa chọn sai có số được assert cho kết quả nằm ngoài sai số."""
import math
from dung import *   # sol, buoc, M/P/A, fig, seg, lbl, poly, arrow, chevron, RED/BLUE/ORG/GRN

GREY = "#94a3b8"
YEL = "#facc15"
DARK = "#475569"
TOPIC = "Pha Mặt Trăng, nhật thực và nguyệt thực"

# ── số liệu chung ──
AU, D_S, D_M, D_E = 1.5e8, 1.39e6, 3470, 12740
R_E = D_E / 2
D_GAN, D_TB, D_XA = 363_000, 384_000, 405_000
S = 29.5
DEG = 180 / math.pi
# D1
NGAY_HH = 3 + S / 4                     # 10,375 → 10/3
NGAY_KT = 3 + S / 2                     # 17,75 → 17–18/3
NGAY_RAM = 3 + S - 31                   # 1,5 → 1–2/4
LECH = 360 / 365.25 * S                 # Mặt Trời dời so với giao tuyến sau 1 Tuần Trăng (độ)
VD = 5 * math.sin(math.radians(LECH))   # trăng tròn lệch khỏi mặt phẳng quỹ đạo TĐ (độ)
# D2
A_S = D_S / AU * DEG                    # 0,531°
L_GAN, L_XA = D_GAN - R_E, D_XA - R_E   # 356 630; 398 630 km
A_GAN, A_XA = D_M / L_GAN * DEG, D_M / L_XA * DEG
TI_LE = (A_XA / A_S) ** 2               # 0,882
L_MAX = D_M * AU / D_S                  # 374 460 km
XU = 0.02 * AU / D_S                    # m
# D3
def non(d):
    a = AU - d
    L = a * D_M / (D_S - D_M)
    x = d - R_E
    return a, L, x
A3G, L3G, X3G = non(D_GAN)
TOI_GAN = D_M * (L3G - X3G) / L3G       # 165 km
NUA_GAN = D_M + X3G * (D_S + D_M) / A3G  # 6791 km
A3X, L3X, X3X = non(D_XA)
KHUYEN = D_M * (X3X - L3X) / L3X        # 225 km
L_E = AU * D_E / (D_S - D_E)            # 1,39·10^6 km
TOI_E = D_E * (L_E - D_TB) / L_E        # 9214 km


def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animate attributeName="{attr}" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def anim_tr(vals, dur):
    return (f'<animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")


def sunrays(x0, x1, ys):
    b = ""
    for y in ys:
        b += seg(x0, y, x1, y, YEL, 2) + chevron(x1, y, 1, 0, YEL, 2, 9)
    return b


def moon(r, lit_left=True):
    """Mặt Trăng tại gốc toạ độ: nửa tối + nửa sáng quay về phía Mặt Trời (bên trái)."""
    half = f"M0,{-r} A{r},{r} 0 0,0 0,{r} Z" if lit_left else f"M0,{-r} A{r},{r} 0 0,1 0,{r} Z"
    return (f'<circle cx="0" cy="0" r="{r}" fill="{DARK}" stroke="currentColor" stroke-width="1.2"/>'
            f'<path d="{half}" fill="{YEL}" stroke="none"/>')


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 1 · pha Mặt Trăng ─────────────
def d1(kk):
    b = ""
    if kk == 0:
        DUR = 10.0
        EX, EY, R = 250, 150, 104
        b += lbl(16, 24, "ánh sáng Mặt Trời", ORG, 14, "start", "700")
        b += sunrays(16, 70, (60, 110, 160, 210, 260))
        b += f'<circle cx="{EX}" cy="{EY}" r="{R}" fill="none" stroke="{GREY}" stroke-width="1.4" stroke-dasharray="5 4"/>'
        for k in range(8):
            t = math.radians(45 * k)
            b += f'<circle cx="{EX + R * math.cos(t):.1f}" cy="{EY - R * math.sin(t):.1f}" r="2.6" fill="{GREY}"/>'
        # Trái Đất: nửa trái (hướng Mặt Trời) sáng
        b += f'<circle cx="{EX}" cy="{EY}" r="17" fill="{BLUE}" fill-opacity="0.35" stroke="currentColor" stroke-width="1.4"/>'
        b += f'<path d="M{EX},{EY - 17} A17,17 0 0,1 {EX},{EY + 17} Z" fill="{DARK}" fill-opacity="0.75" stroke="none"/>'
        b += lbl(EX, EY + 36, "Trái Đất", "currentColor", 14, "middle", "700")
        # chiều quay quanh Trái Đất (ngược chiều kim đồng hồ khi nhìn từ phía Bắc)
        t = math.radians(135)
        b += chevron(EX + R * math.cos(t), EY - R * math.sin(t), -math.sin(t), -math.cos(t), GREY, 2, 11)
        b += lbl(EX + R + 14, EY + 5, "rằm 3/3", RED, 14, "start", "700")
        b += lbl(EX, EY - R - 12, "?", GRN, 16, "middle", "700")
        b += lbl(EX - R - 10, EY + 5, "?", GRN, 16, "end", "700")
        # Mặt Trăng chạy một vòng, nửa sáng luôn quay về Mặt Trời
        N = 36
        pts = [(EX + R * math.cos(2 * math.pi * i / N), EY - R * math.sin(2 * math.pi * i / N)) for i in range(N + 1)]
        vals = ";".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        b += f'<g transform="translate({pts[0][0]:.1f},{pts[0][1]:.1f})">{moon(11)}{anim_tr(vals, DUR)}</g>'
        b += lbl(16, 292, "Nhìn từ phía Bắc, không theo tỉ lệ", GREY, 14, "start", "400")
        return fig("c17-1-0", "0 0 420 300",
                   "Mặt Trăng đi một vòng quanh Trái Đất bắt đầu từ vị trí rằm ngày 3 tháng 3, nửa được chiếu sáng luôn quay về phía Mặt Trời ở bên trái",
                   b, "Mô phỏng chạy nhanh: Mặt Trăng đi trọn một vòng ứng với một Tuần Trăng, bắt đầu từ rằm 3/3. "
                      "Nửa sáng luôn quay về phía Mặt Trời. Các vị trí dấu ? là ngày cần tìm.")
    # hình dữ kiện: một phần tư vòng + quỹ đạo nghiêng 5°
    EX, EY, R = 100, 120, 70
    b += f'<circle cx="{EX}" cy="{EY}" r="{R}" fill="none" stroke="{GREY}" stroke-width="1.4" stroke-dasharray="5 4"/>'
    b += f'<circle cx="{EX}" cy="{EY}" r="12" fill="{BLUE}" fill-opacity="0.35" stroke="currentColor" stroke-width="1.4"/>'
    b += sunrays(4, 22, (80, 120, 160))
    b += lbl(4, 24, "ánh sáng Mặt Trời", ORG, 14, "start", "700")
    b += f'<circle cx="{EX + R}" cy="{EY}" r="8" fill="{YEL}" stroke="currentColor" stroke-width="1.2"/>'
    b += lbl(EX + R + 12, EY + 5, "rằm", RED, 14, "start", "700")
    b += f'<circle cx="{EX}" cy="{EY - R}" r="6" fill="{GREY}"/>'
    b += seg(EX, EY, EX + R, EY, GREY, 1.2, "3 3") + seg(EX, EY, EX, EY - R, GREY, 1.2, "3 3")
    b += f'<path d="M{EX + 30},{EY} A30,30 0 0,0 {EX},{EY - 30}" fill="none" stroke="{ORG}" stroke-width="2"/>'
    b += lbl(EX + 26, EY - 26, "90°", ORG, 14, "start", "700")
    b += lbl(EX, 222, "1/4 vòng ↔ S/4", ORG, 14, "middle", "700")
    # quỹ đạo nghiêng (phóng đại)
    X0, X1, YC = 220, 410, 120
    b += seg(X0, YC, X1, YC, BLUE, 2) + lbl(X0, YC - 30, "mặt phẳng quỹ đạo", BLUE, 14, "start", "400") + lbl(X0, YC - 12, "Trái Đất", BLUE, 14, "start", "400")
    th = math.radians(14)
    xm = (X0 + X1) / 2
    b += seg(xm - 90 * math.cos(th), YC + 90 * math.sin(th), xm + 90 * math.cos(th), YC - 90 * math.sin(th), GRN, 2)
    b += lbl(X1, YC - 54, "quỹ đạo Mặt Trăng", GRN, 14, "end", "700")
    b += f'<circle cx="{xm}" cy="{YC}" r="4.5" fill="{RED}"/>' + lbl(xm + 6, YC + 32, "giao tuyến", RED, 14, "start", "700")
    b += f'<path d="M{xm + 50},{YC} A50,50 0 0,0 {xm + 50 * math.cos(th):.1f},{YC - 50 * math.sin(th):.1f}" fill="none" stroke="{ORG}" stroke-width="1.8"/>'
    b += lbl(xm + 56, YC - 4, "5°", ORG, 14, "start", "700")
    b += lbl(X0, 222, "góc 5° vẽ phóng đại", GREY, 14, "start", "400")
    return fig("c17-1-2", "0 0 420 236",
               "Bên trái: từ rằm đi một phần tư vòng quỹ đạo ứng với một phần tư Tuần Trăng. Bên phải: quỹ đạo Mặt Trăng nghiêng 5 độ so với mặt phẳng quỹ đạo Trái Đất, cắt nhau ở giao tuyến",
               b, "Dữ kiện: mỗi phần tư vòng ứng với S/4. Quỹ đạo Mặt Trăng chỉ cắt mặt phẳng quỹ đạo Trái Đất ở giao tuyến.")


# ───────────── Dạng 2 · góc trông ─────────────
def eye(x, y):
    return (f'<path d="M{x - 14},{y} Q{x},{y - 12} {x + 14},{y} Q{x},{y + 12} {x - 14},{y} Z" fill="none" stroke="currentColor" stroke-width="1.8"/>'
            f'<circle cx="{x + 3}" cy="{y}" r="4.5" fill="currentColor"/>')


def d2(kk):
    b = ""
    if kk == 0:
        DUR = 5.0
        EX, EY = 34, 110
        SX, SR = 356, 52                      # Mặt Trời (vẽ phóng đại, không theo tỉ lệ)
        b += f'<circle cx="{SX}" cy="{EY}" r="{SR}" fill="{YEL}" fill-opacity="0.85" stroke="{ORG}" stroke-width="1.6"/>'
        b += lbl(SX, EY + SR + 20, "Mặt Trời", ORG, 14, "middle", "700")
        b += eye(EX, EY)
        b += seg(EX + 6, EY, SX, EY - SR, ORG, 1.4, "5 4") + seg(EX + 6, EY, SX, EY + SR, ORG, 1.4, "5 4")
        # dấu ngắt khoảng cách (không theo tỉ lệ)
        for dx in (0, 8):
            b += seg(270 + dx, EY + 64, 278 + dx, EY + 50, "currentColor", 1.6)
        b += lbl(274, EY + 84, "không theo tỉ lệ", GREY, 14, "middle", "400")
        # đồng xu tiến ra xa mắt tới khi vừa che kín đĩa Mặt Trời
        HC = 20                               # nửa chiều cao đồng xu (px)
        xf = EX + 6 + HC * (SX - EX - 6) / SR
        b += (f'<rect x="64" y="{EY - HC}" width="7" height="{2 * HC}" rx="3" fill="{GREY}" stroke="currentColor" stroke-width="1.4">'
              f'{anim("x", f"64;{xf - 3.5:.1f}", DUR)}</rect>')
        b += lbl(66, EY - HC - 10, "đồng xu 2 cm", "currentColor", 14, "start", "700")
        b += (f'<g opacity="0">{anim("opacity", "0;0;1", DUR, "0;0.97;1")}'
              f'{dim("", "g", EX + 6, EY + 40, xf, EY + 40, "", 0, 0)}'
              f'<text x="{(EX + xf) / 2:.1f}" y="{EY + 60}" fill="{GRN}" font-size="15" font-weight="700" text-anchor="middle">ℓ = ?</text></g>')
        b += lbl(16, 24, "Chỉ nhìn qua kính lọc chuyên dụng", RED, 14, "start", "700")
        return fig("c17-2-0", "0 0 420 220",
                   "Đồng xu dịch dần ra xa mắt cho tới khi vừa che kín đĩa Mặt Trời, khoảng cách từ mắt tới đồng xu chưa biết",
                   b, "Mô phỏng: đồng xu dời ra xa tới khi vừa lấp kín hai tia nhìn tới mép đĩa Mặt Trời. Khoảng cách và góc vẽ phóng đại, không đo trên hình được.")
    # hình dữ kiện: góc trông + người quan sát ngay dưới Mặt Trăng
    CX, CY, RR = 120, 262, 92
    b += f'<circle cx="{CX}" cy="{CY}" r="{RR}" fill="{BLUE}" fill-opacity="0.18" stroke="{BLUE}" stroke-width="1.8"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="3.5" fill="currentColor"/>'
    ox, oy = CX, CY - RR
    mx, my, mr = CX, 34, 13
    b += f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="{DARK}" stroke="currentColor" stroke-width="1.4"/>'
    b += lbl(mx, my - 18, "Mặt Trăng, đường kính D", "currentColor", 14, "middle", "700")
    b += f'<circle cx="{ox}" cy="{oy}" r="4" fill="{RED}"/>' + lbl(ox + 8, oy - 6, "mắt", RED, 14, "start", "700")
    b += seg(ox, oy, mx - mr, my, ORG, 1.4) + seg(ox, oy, mx + mr, my, ORG, 1.4)
    b += lbl(ox + 8, oy - 30, "α", ORG, 16, "start", "700")
    # khoảng cách tâm–tâm (trái) và từ mặt đất (phải)
    b += dim("", "b", CX - 40, my, CX - 40, CY, "", 0, 0) + lbl(CX - 48, 150, "d", BLUE, 15, "end", "700")
    b += dim("", "g", CX + 40, my, CX + 40, oy, "", 0, 0) + lbl(CX + 48, 110, "ℓ = d − R", GRN, 15, "start", "700")
    b += lbl(CX + 6, 226, "R", "currentColor", 14, "start", "700") + seg(CX, CY, CX, oy, GREY, 1.2, "3 3")
    b += lbl(250, 200, "α ≈ D / ℓ (rad)", "currentColor", 14, "start", "700")
    b += lbl(250, 222, "độ = rad × 180/π", "currentColor", 14, "start", "400")
    return fig("c17-2-2", "0 0 420 300",
               "Người quan sát đứng trên mặt đất ngay dưới Mặt Trăng; khoảng cách tới Mặt Trăng bằng khoảng cách tâm trừ bán kính Trái Đất; góc trông alpha bằng đường kính chia khoảng cách",
               b, "Dữ kiện: khoảng cách từ mắt tới Mặt Trăng tính từ mặt đất, không từ tâm Trái Đất. Hình không theo tỉ lệ.")


# ───────────── Dạng 3 · nón bóng ─────────────
def d3(kk):
    b = ""
    if kk == 0:
        DUR = 6.0
        b += f'<defs><linearGradient id="c17g3" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{DARK}" stop-opacity="0.85"/>'
        b += f'<stop offset="1" stop-color="{DARK}" stop-opacity="0"/></linearGradient></defs>'
        b += f'<circle cx="-70" cy="120" r="112" fill="{YEL}" fill-opacity="0.85" stroke="{ORG}" stroke-width="1.6"/>'
        b += lbl(8, 228, "Mặt Trời", ORG, 14, "start", "700")
        for dx in (0, 8):
            b += seg(82 + dx, 214, 90 + dx, 200, "currentColor", 1.6)
        b += lbl(90, 190, "rất xa", GREY, 14, "middle", "400")
        # Trái Đất (mép trái ở x = 330)
        b += f'<circle cx="510" cy="120" r="180" fill="{BLUE}" fill-opacity="0.22" stroke="{BLUE}" stroke-width="1.8"/>'
        b += lbl(412, 30, "Trái Đất", BLUE, 14, "end", "700")
        # Mặt Trăng + bóng chuyển động theo phương vuông góc trục (Mặt Trăng đi trên quỹ đạo)
        MX, MR = 176, 13
        g = ""
        g += f'<path d="M{MX},{-MR} L340,{-56} L340,{56} L{MX},{MR} Z" fill="{GREY}" fill-opacity="0.28" stroke="none"/>'
        g += f'<path d="M{MX},{-MR} L292,-3 L292,3 L{MX},{MR} Z" fill="url(#c17g3)" stroke="none"/>'
        g += f'<circle cx="{MX}" cy="0" r="{MR}" fill="{DARK}" stroke="currentColor" stroke-width="1.4"/>'
        g += f'<path d="M{MX},{-MR} A{MR},{MR} 0 0,0 {MX},{MR} Z" fill="{YEL}" stroke="none"/>'
        g += f'<text x="306" y="5" fill="{GRN}" font-size="17" font-weight="700" text-anchor="middle">?</text>'
        ys = [70, 120, 170]
        g = f'<g transform="translate(0,{ys[0]})">{g}{anim_tr(";".join(f"0,{y}" for y in ys), DUR)}</g>'
        b += g
        b += lbl(176, 26, "Mặt Trăng", "currentColor", 14, "middle", "700")
        b += lbl(250, 228, "nửa tối", GREY, 14, "middle", "700")
        b += lbl(16, 24, "Ngày không trăng", "currentColor", 14, "start", "700")
        return fig("c17-3-0", "0 0 420 240",
                   "Mặt Trăng đi ngang qua đường nối Mặt Trời và Trái Đất, kéo theo nón bóng tối và vùng nửa tối; chóp nón bóng tối có chạm mặt đất hay không là điều cần tìm",
                   b, "Mô phỏng: Mặt Trăng đi trên quỹ đạo, bóng của nó quét qua Trái Đất. Bóng tối vẽ mờ dần ở gần mặt đất: chóp nón ở trước hay sau mặt đất phải tính. Không theo tỉ lệ.")
    # hình dữ kiện: tam giác đồng dạng tổng quát
    YC = 120
    SX, SH, MX, MH = 40, 80, 180, 30
    apex = MX + MH * (MX - SX) / (SH - MH)
    b += seg(SX, YC - SH, SX, YC + SH, ORG, 3) + f'<text x="{SX - 6}" y="{YC - SH - 8}" fill="{ORG}" font-size="14" font-weight="700">nguồn D<tspan dy="4" font-size="12">0</tspan></text>'
    b += seg(MX, YC - MH, MX, YC + MH, "currentColor", 3) + lbl(MX, YC - MH - 16, "vật chắn D", "currentColor", 14, "middle", "700")
    b += f'<path d="M{MX},{YC - MH} L{apex:.1f},{YC} L{MX},{YC + MH} Z" fill="{DARK}" fill-opacity="0.35" stroke="none"/>'
    b += seg(SX, YC - SH, apex, YC, "currentColor", 1.4) + seg(SX, YC + SH, apex, YC, "currentColor", 1.4)
    # tia nửa tối (chéo)
    k = (MH + SH) / (MX - SX)
    xe = 400
    b += seg(SX, YC - SH, xe, YC + MH + k * (xe - MX), GREY, 1.3, "5 4") + seg(SX, YC + SH, xe, YC - MH - k * (xe - MX), GREY, 1.3, "5 4")
    b += seg(SX, YC, 410, YC, GREY, 1, "2 3")
    b += dim("", "o", SX, 214, MX, 214, "", 0, 0) + lbl((SX + MX) / 2, 232, "a", ORG, 15, "middle", "700")
    b += dim("", "b", MX, 192, apex, 192, "", 0, 0) + lbl(apex + 8, 197, "L", BLUE, 15, "start", "700")
    xo = 236
    b += seg(xo, 22, xo, 214, GRN, 1.6, "6 4") + lbl(xo + 6, 34, "nơi quan sát", GRN, 14, "start", "700")
    b += dim("", "g", MX, 204, xo, 204, "", 0, 0)
    b += lbl(xo + 8, 222, "x", GRN, 15, "start", "700")
    b += lbl(330, 110, "nửa tối", GREY, 14, "middle", "700")
    return fig("c17-3-2", "0 0 420 240",
               "Sơ đồ tam giác đồng dạng: nguồn sáng đường kính D0, vật chắn đường kính D cách nguồn khoảng a, nón bóng tối dài L, nơi quan sát cách vật chắn khoảng x, các tia chéo giới hạn vùng nửa tối",
               b, "Sơ đồ chung cho cả nhật thực (vật chắn là Mặt Trăng) và nguyệt thực (vật chắn là Trái Đất). Không theo tỉ lệ.")


BUILD = [d1, d2, d3]

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Pha Mặt Trăng và lịch thực: từ ngày rằm suy ra các pha, ngày có thể có nhật thực",
      topic=TOPIC,
      problem_html=r"""<p>Ngày 3/3 là ngày trăng tròn (rằm) và đêm đó có nguyệt thực toàn phần. Lấy một Tuần Trăng (tháng giao hội) $S=29{,}5$ ngày; tháng 3 có $31$ ngày. Coi Mặt Trăng chuyển động đều quanh Trái Đất.</p><ol type="a"><li>Tìm ngày có trăng hạ huyền gần nhất sau đó, ngày không trăng kế tiếp và ngày trăng tròn kế tiếp. Nếu trong khoảng này có nhật thực thì nhật thực chỉ có thể rơi vào ngày nào? Vì sao?</li><li>Trăng thượng huyền mọc vào khoảng mấy giờ? Lúc $18$ h, người ở Việt Nam thấy nó ở đâu trên bầu trời, phần sáng quay về phía nào?</li><li>Vì sao đêm trăng tròn kế tiếp thường không có nguyệt thực nữa?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Góc trông: Mặt Trăng che kín Mặt Trời hay chỉ tạo nhật thực hình khuyên",
      topic=TOPIC,
      problem_html=r"""<p>Đường kính Mặt Trời $D_S=1{,}39\cdot10^6\ \text{km}$, khoảng cách Trái Đất – Mặt Trời $1\ \text{AU}=1{,}5\cdot10^8\ \text{km}$; đường kính Mặt Trăng $D_M=3470\ \text{km}$; bán kính Trái Đất $R_E=6370\ \text{km}$. Khoảng cách tâm Trái Đất – tâm Mặt Trăng lúc gần nhất là $363\,000\ \text{km}$, lúc xa nhất là $405\,000\ \text{km}$. Coi góc trông nhỏ: $\alpha\approx\dfrac{D}{\ell}$ (rad), với $D$ là đường kính vật, $\ell$ là khoảng cách từ mắt tới vật.</p><ol type="a"><li>Nhìn Mặt Trời qua kính lọc chuyên dụng (không bao giờ nhìn bằng mắt thường hay kính râm), một bạn giơ đồng xu đường kính $2\ \text{cm}$ trước mắt. Phải đặt đồng xu cách mắt bao xa để nó vừa che kín đĩa Mặt Trời?</li><li>Tính góc trông Mặt Trời theo độ.</li><li>Người quan sát đứng ở điểm mặt đất ngay dưới Mặt Trăng. Tính góc trông Mặt Trăng lúc gần nhất và lúc xa nhất. Nếu khi đó xảy ra nhật thực trung tâm (tâm ba thiên thể thẳng hàng) thì mỗi trường hợp là nhật thực toàn phần hay hình khuyên?</li><li>Khi Mặt Trăng ở xa nhất, đĩa Mặt Trời bị che tối đa bao nhiêu phần trăm diện tích?</li><li>Khoảng cách từ người quan sát tới Mặt Trăng không được vượt quá bao nhiêu thì Mặt Trăng còn che kín được Mặt Trời?</li></ol>"""),
 dict(label="Dạng 3 · Nâng cao · Nón bóng Mặt Trăng và Trái Đất: vùng tối, vùng nửa tối, nhật thực hình khuyên, nguyệt thực",
      topic=TOPIC,
      problem_html=r"""<p>Một quả cầu chắn sáng đường kính $D$ đặt cách một nguồn sáng hình cầu đường kính $D_0\gt D$ một khoảng $a$ (tính giữa hai tâm) thì phía sau nó có một nón bóng tối thu nhỏ dần, bao quanh là vùng nửa tối (bài Gương phẳng, bóng tối và nửa tối). Áp dụng cho nhật thực và nguyệt thực với số liệu: $D_S=1{,}39\cdot10^6\ \text{km}$; $D_M=3470\ \text{km}$; $D_E=12\,740\ \text{km}$ ($R_E=6370\ \text{km}$); khoảng cách Mặt Trời – Trái Đất $1\ \text{AU}=1{,}5\cdot10^8\ \text{km}$. Khoảng cách tâm Trái Đất – tâm Mặt Trăng: gần nhất $363\,000\ \text{km}$, trung bình $384\,000\ \text{km}$, xa nhất $405\,000\ \text{km}$. Chỉ xét nhật thực, nguyệt thực trung tâm (tâm ba thiên thể thẳng hàng); coi chỗ mặt đất hứng bóng là mặt phẳng vuông góc với trục nón.</p><ol type="a"><li>Ngày nhật thực, Mặt Trăng ở gần nhất. Tính chiều dài $L$ của nón bóng tối Mặt Trăng.</li><li>Chóp nón bóng tối có tới được mặt đất không? Tính đường kính vùng tối và vùng nửa tối trên mặt đất, tại điểm gần Mặt Trăng nhất.</li><li>Ngày nhật thực khác, Mặt Trăng ở xa nhất. Người ở điểm ngay dưới Mặt Trăng thấy nhật thực loại gì? Tính đường kính vùng mặt đất thấy được loại nhật thực đó.</li><li>Ngày nguyệt thực, Mặt Trăng ở khoảng cách trung bình. Tính chiều dài nón bóng tối của Trái Đất và đường kính vùng tối tại quỹ đạo Mặt Trăng. Vùng tối đó gấp bao nhiêu lần đường kính Mặt Trăng?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1 (mo_het)
 [(r'"Ngày 3/3 là ngày trăng tròn (rằm) và đêm đó có nguyệt thực toàn phần"', r"Mốc: rằm 3/3",
   r"Trăng tròn: Mặt Trời – Trái Đất – Mặt Trăng thẳng hàng, Trái Đất ở giữa<br>Có nguyệt thực: đang trong mùa thực"),
  (r'"Tuần Trăng … $S=29{,}5$ ngày; tháng 3 có $31$ ngày"', r"$S=29{,}5$ ngày",
   r"Một Tuần Trăng thì trở lại pha cũ<br>Sang tháng 4 phải trừ số ngày tháng 3"),
  (r'"Coi Mặt Trăng chuyển động đều"', r"Góc tỉ lệ với thời gian",
   r"⚠ chỉ khi coi đều mới chia thời gian theo góc; thực tế các pha lệch được khoảng $\pm1$ ngày"),
  (r'"ngày … hạ huyền …, ngày không trăng …, ngày trăng tròn kế tiếp"', r"Cần ba ngày",
   r"Rằm → hạ huyền → không trăng → thượng huyền → rằm<br>Mỗi pha chính cách nhau $\dfrac{S}{4}$"),
  (r'"nhật thực chỉ có thể rơi vào ngày nào?"', r"Điều kiện nhật thực",
   r"Nhật thực: Mặt Trăng nằm giữa Mặt Trời và Trái Đất"),
  (r'"Trăng thượng huyền mọc vào khoảng mấy giờ? … Lúc $18$ h"', r"Thượng huyền",
   r"Thượng huyền: góc Mặt Trăng – Trái Đất – Mặt Trời là $90°$<br>Trái Đất tự quay $15°$ mỗi giờ"),
  (r'"thường không có nguyệt thực nữa"', r"Một Tuần Trăng sau",
   r"Quỹ đạo Mặt Trăng nghiêng $5°$; chỉ thẳng hàng khi trăng tròn ở gần giao tuyến")],
 # Dạng 2 (giau_buoc_cuoi: bước cuối có hỏi = khoảng cách lớn nhất)
 [(r'"$D_S=1{,}39\cdot10^6\ \text{km}$ … $1\ \text{AU}=1{,}5\cdot10^8\ \text{km}$; … $D_M=3470\ \text{km}$; … $R_E=6370\ \text{km}$"',
   r"$D_S$; AU; $D_M$; $R_E$", r"Đổi mọi khoảng cách về cùng đơn vị trước khi chia"),
  (r'"Coi góc trông nhỏ: $\alpha\approx\dfrac{D}{\ell}$ (rad)"', r"",
   r"⚠ chỉ dùng khi $D$ rất nhỏ so với $\ell$<br>⚠ kết quả ra rad; đổi sang độ nhân $\dfrac{180}{\pi}$"),
  (r'"đồng xu đường kính $2\ \text{cm}$ … vừa che kín đĩa Mặt Trời"', r"$D_x=2\ \text{cm}$; cần $\ell_x$",
   r"Vừa che kín khi hai góc trông bằng nhau"),
  (r'"kính lọc chuyên dụng (không bao giờ nhìn bằng mắt thường hay kính râm)"', r"",
   r"⚠ an toàn: nhìn thẳng Mặt Trời làm hỏng võng mạc, kính râm không đủ lọc"),
  (r'"Tính góc trông Mặt Trời theo độ"', r"Cần $\alpha_S$", r"$\alpha_S\approx\dfrac{D_S}{1\ \text{AU}}$ rồi đổi ra độ"),
  (r'"đứng ở điểm mặt đất ngay dưới Mặt Trăng"', r"Người đứng gần Mặt Trăng hơn tâm Trái Đất",
   r"Khoảng cách từ mắt: $\ell=d-R_E$"),
  (r'"lúc gần nhất là $363\,000\ \text{km}$, lúc xa nhất là $405\,000\ \text{km}$"', r"$d_{\text{gần}}$; $d_{\text{xa}}$",
   r"Đường kính không đổi, khoảng cách đổi thì góc trông đổi"),
  (r'"toàn phần hay hình khuyên?"', r"So hai góc trông",
   r"Toàn phần khi đĩa Mặt Trăng trông lớn hơn đĩa Mặt Trời; nhỏ hơn thì còn viền sáng"),
  (r'"che tối đa bao nhiêu phần trăm diện tích?"', r"Cần tỉ lệ diện tích",
   r"Diện tích hình tròn tỉ lệ với bình phương đường kính"),
  (r'"không được vượt quá bao nhiêu thì … còn che kín được"', r"Cần $\ell_{\max}$",
   r"Ở khoảng cách giới hạn, hai góc trông quan hệ thế nào?")],
 # Dạng 3 (giau_tu_buoc_2: chỉ bước 1 mở)
 [(r'"quả cầu chắn sáng đường kính $D$ … nguồn sáng hình cầu đường kính $D_0$ … khoảng $a$"', r"$D_0$; $D$; $a$",
   r"Hai tia nối mép nguồn với mép vật chắn gặp nhau ở chóp nón<br>Tam giác đồng dạng: $\dfrac{D}{L}=\dfrac{D_0}{a+L}$"),
  (r'"Chỉ xét nhật thực, nguyệt thực trung tâm …; coi chỗ mặt đất hứng bóng là mặt phẳng vuông góc với trục nón"', r"",
   r"⚠ chỉ khi tâm ba thiên thể thẳng hàng và mặt hứng bóng vuông góc trục mới tính được đường kính vùng tối bằng tam giác đồng dạng"),
  (r'"Ngày nhật thực, Mặt Trăng ở gần nhất"', r"$d=363\,000\ \text{km}$",
   r"Nguồn: Mặt Trời; vật chắn: Mặt Trăng nằm giữa<br>Khoảng cách nguồn – vật chắn: $a=1\ \text{AU}-d$"),
  (r'"Chóp nón bóng tối có tới được mặt đất không?"', r"Cần so sánh",
   r"Từ Mặt Trăng tới mặt đất (chỗ gần nhất) là bao xa? So với $L$ thế nào?"),
  (r'"đường kính vùng tối và vùng nửa tối trên mặt đất"', r"Cần hai đường kính",
   r"Đi thêm một đoạn sau vật chắn, nón bóng tối hẹp lại bao nhiêu?<br>Hai tia chéo của vùng nửa tối loe ra thế nào?"),
  (r'"Mặt Trăng ở xa nhất … thấy nhật thực loại gì?"', r"$d=405\,000\ \text{km}$",
   r"$L$ và khoảng cách tới mặt đất thay đổi thế nào? Chóp nón nằm ở đâu?"),
  (r'"đường kính vùng mặt đất thấy được loại nhật thực đó"', r"Cần một đường kính",
   r"Sau chóp nón, các tia mép tiếp tục đi thế nào?"),
  (r'"Ngày nguyệt thực, Mặt Trăng ở khoảng cách trung bình"', r"$d=384\,000\ \text{km}$",
   r"Vật chắn bây giờ là thiên thể nào? Nó cách nguồn bao xa?"),
  (r'"gấp bao nhiêu lần đường kính Mặt Trăng?"', r"Cần tỉ số", r"So vùng tối với $D_M$")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> Mặt Trăng không tự phát sáng; nửa quay về Mặt Trời luôn sáng, phần ta thấy tuỳ góc Mặt Trời – Trái Đất – Mặt Trăng.",
      r"<strong>Chu kì:</strong> sau một Tuần Trăng $S$ pha lặp lại; các pha chính cách nhau $\dfrac{S}{4}$.",
      r"<strong>Điều kiện thực:</strong> nhật thực chỉ vào ngày không trăng, nguyệt thực chỉ vào đêm rằm.",
      r"<strong>Vì sao hiếm:</strong> quỹ đạo Mặt Trăng nghiêng $5°$, chỉ thẳng hàng khi gần giao tuyến (mùa thực)."]
R2 = [r"<strong>Khái niệm:</strong> góc trông là góc giữa hai tia nhìn tới hai mép vật.",
      r"<strong>Công thức:</strong> $\alpha\approx\dfrac{D}{\ell}$ (rad); đổi ra độ nhân $\dfrac{180}{\pi}$.",
      r"<strong>Điều kiện toàn phần:</strong> $\alpha_M\ge\alpha_S$; $\alpha_M\lt\alpha_S$ thì nhật thực hình khuyên.",
      r"<strong>Lưu ý:</strong> người đứng trên mặt đất nên $\ell=d-R_E$; diện tích đĩa tỉ lệ bình phương góc trông."]
R3 = [r"<strong>Nón bóng tối:</strong> $\dfrac{D}{L}=\dfrac{D_0}{a+L}\Rightarrow L=\dfrac{aD}{D_0-D}$.",
      r"<strong>Vùng tối cách vật chắn $x$:</strong> $D\,\dfrac{L-x}{L}$ khi $x\lt L$; sau chóp ($x\gt L$) vùng hình khuyên rộng $D\,\dfrac{x-L}{L}$.",
      r"<strong>Vùng nửa tối:</strong> $D+x\,\dfrac{D_0+D}{a}$.",
      r"<strong>Áp dụng:</strong> nhật thực: $D_0=D_S$, $D=D_M$, $a=1\ \text{AU}-d$, $x=d-R_E$; nguyệt thực: $D=D_E$, $a=1\ \text{AU}$, $x=d$."]

SOLS = [
 sol(R1, [
  ("Ngày hạ huyền", [P(r"Từ rằm tới hạ huyền là một phần tư vòng:"),
     M(r"\dfrac{S}{4}=\dfrac{29{,}5}{4}\approx7{,}4\ \text{ngày}"), M(r"3+7{,}4=10{,}4"), A(r"T:Hạ huyền khoảng ngày 10/3")]),
  ("Ngày không trăng", [P(r"Không trăng ở phía đối diện rằm, cách nửa vòng:"),
     M(r"\dfrac{S}{2}=14{,}75\ \text{ngày}"), M(r"3+14{,}75=17{,}75"), A(r"T:Không trăng khoảng ngày 17–18/3"),
     P(r"Nhật thực cần Mặt Trăng nằm giữa Mặt Trời và Trái Đất, tức ngày không trăng, nên chỉ có thể rơi vào khoảng 17–18/3."),
     P(r"Ngày đó chỉ cách rằm có nguyệt thực nửa tháng, vẫn trong mùa thực, nên có khả năng xảy ra nhật thực (thường chỉ thấy ở một dải hẹp trên Trái Đất).")]),
  ("Ngày rằm kế tiếp", [P(r"Sau một Tuần Trăng thì trở lại rằm:"), M(r"3+29{,}5=32{,}5"),
     P(r"Tháng 3 có $31$ ngày:"), M(r"32{,}5-31=1{,}5"), A(r"T:Rằm kế tiếp khoảng ngày 1–2/4")]),
  ("Trăng thượng huyền", [P(r"Thượng huyền: Mặt Trăng lệch $90°$ về phía Đông so với Mặt Trời. Trái Đất quay $15°$ mỗi giờ:"),
     M(r"\dfrac{90°}{15°/\text{h}}=6\ \text{h}"),
     P(r"Mặt Trăng mọc sau Mặt Trời khoảng $6$ h, tức khoảng $12$ h trưa."),
     P(r"Lúc $18$ h Mặt Trời lặn ở phía Tây; Mặt Trăng đã mọc được $6$ h nên lên cao nhất, gần kinh tuyến (ở Việt Nam thường lệch về phía Nam)."),
     A(r"T:Mọc khoảng 12 h; lúc 18 h ở cao nhất, phần sáng quay về phía Tây (phía Mặt Trời)")]),
  ("Vì sao rằm tháng 4 thường không có nguyệt thực", [P(r"Quỹ đạo Mặt Trăng nghiêng $5°$ so với mặt phẳng quỹ đạo Trái Đất. Rằm 3/3 có nguyệt thực vì lúc đó trăng tròn ở gần giao tuyến."),
     P(r"Sau một Tuần Trăng, Trái Đất đã đi thêm trên quỹ đạo, hướng Mặt Trời quay đi so với giao tuyến:"),
     M(r"\dfrac{360°}{365{,}25}\cdot29{,}5\approx29°"),
     P(r"Trăng tròn lần sau không còn ở giao tuyến nên đi phía trên hoặc phía dưới bóng Trái Đất: không có nguyệt thực. Mùa thực kế tiếp đến sau khoảng $6$ tháng.")]),
  ("Kiểm tra", [P(r"Thứ tự pha: rằm 3/3 → hạ huyền 10/3 → không trăng 17–18/3 → thượng huyền khoảng 25/3 → rằm 1–2/4; mỗi khoảng khoảng $7{,}4$ ngày ✓."),
     P(r"Ước lượng (giả sử rằm 3/3 nằm đúng giao tuyến): rằm 1–2/4 lệch khỏi mặt phẳng quỹ đạo Trái Đất khoảng $5°\cdot\sin29°\approx2{,}4°$; cả vùng nửa tối của bóng Trái Đất chỉ trải khoảng $1{,}2°$ quanh trục bóng, cộng bán kính góc Mặt Trăng $0{,}26°$ vẫn nhỏ hơn $2{,}4°$ ✓.")])],
  [r"a) Hạ huyền khoảng 10/3; không trăng khoảng 17–18/3; rằm kế tiếp khoảng 1–2/4", r"a) Nhật thực (nếu có) chỉ có thể vào khoảng 17–18/3, ngày không trăng",
   r"b) Mọc khoảng 12 h; lúc 18 h ở cao nhất trên bầu trời, phần sáng quay về phía Tây",
   r"c) Quỹ đạo Mặt Trăng nghiêng 5°; một tháng sau trăng tròn không còn gần giao tuyến nên đi lệch khỏi bóng Trái Đất"],
  r"Nhận dạng: thấy <strong>cho một ngày rằm hoặc ngày không trăng, hỏi ngày pha khác</strong> → cộng bội của $S/4$; nhật thực chỉ ngày không trăng, nguyệt thực chỉ đêm rằm."),
 sol(R2, [
  ("Khoảng cách đồng xu", [P(r"Vừa che kín khi góc trông đồng xu bằng góc trông Mặt Trời:"),
     M(r"\dfrac{D_x}{\ell_x}=\dfrac{D_S}{1\ \text{AU}}\Rightarrow\ell_x=D_x\,\dfrac{1\ \text{AU}}{D_S}"),
     M(r"\ell_x=0{,}02\ \text{m}\cdot\dfrac{1{,}5\cdot10^8}{1{,}39\cdot10^6}"), A(r"\ell_x\approx2{,}16\ \text{m}")]),
  ("Góc trông Mặt Trời", [M(r"\alpha_S\approx\dfrac{1{,}39\cdot10^6}{1{,}5\cdot10^8}\approx9{,}27\cdot10^{-3}\ \text{rad}"),
     M(r"\alpha_S\approx9{,}27\cdot10^{-3}\cdot\dfrac{180}{\pi}"), A(r"\alpha_S\approx0{,}531°")]),
  ("Góc trông Mặt Trăng lúc gần nhất", [P(r"Người đứng trên mặt đất ngay dưới Mặt Trăng:"),
     M(r"\ell=363\,000-6370=356\,630\ \text{km}"), M(r"\alpha_M=\dfrac{3470}{356\,630}\cdot\dfrac{180}{\pi}"), A(r"\alpha_M\approx0{,}557°")]),
  ("Góc trông Mặt Trăng lúc xa nhất", [M(r"\ell=405\,000-6370=398\,630\ \text{km}"), M(r"\alpha'_M=\dfrac{3470}{398\,630}\cdot\dfrac{180}{\pi}"),
     A(r"\alpha'_M\approx0{,}499°")]),
  ("Toàn phần hay hình khuyên", [P(r"Lúc gần nhất $0{,}557°\gt0{,}531°$: đĩa Mặt Trăng trông lớn hơn, che kín Mặt Trời: <strong>nhật thực toàn phần</strong>."),
     P(r"Lúc xa nhất $0{,}499°\lt0{,}531°$: đĩa Mặt Trăng trông nhỏ hơn, còn một viền sáng: <strong>nhật thực hình khuyên</strong>.")]),
  ("Phần trăm diện tích bị che", [P(r"Diện tích đĩa tỉ lệ bình phương đường kính, tức bình phương góc trông:"),
     M(r"\dfrac{S_{\text{che}}}{S_{\text{đĩa}}}=\left(\dfrac{\alpha'_M}{\alpha_S}\right)^2=\left(\dfrac{0{,}499}{0{,}531}\right)^2"), A(r"\approx0{,}88=88\ \%")]),
  ("Khoảng cách lớn nhất để còn che kín", [P(r"Ở khoảng cách giới hạn, hai góc trông bằng nhau:"),
     M(r"\dfrac{D_M}{\ell_{\max}}=\dfrac{D_S}{1\ \text{AU}}\Rightarrow\ell_{\max}=D_M\,\dfrac{1\ \text{AU}}{D_S}"),
     M(r"\ell_{\max}=3470\cdot\dfrac{1{,}5\cdot10^8}{1{,}39\cdot10^6}"), A(r"\ell_{\max}\approx374\,000\ \text{km}")]),
  ("Kiểm tra", [P(r"$356\,630\ \text{km}\lt374\,000\ \text{km}\lt398\,630\ \text{km}$: khớp kết luận toàn phần lúc gần, hình khuyên lúc xa ✓."),
     P(r"Đồng xu và Mặt Trăng cùng che vừa Mặt Trời khi khoảng cách gấp khoảng $108$ lần đường kính: $\dfrac{2{,}16\ \text{m}}{0{,}02\ \text{m}}\approx\dfrac{374\,000}{3470}\approx108$ ✓."),
     P(r"Mặt Trời to gấp khoảng $400$ lần Mặt Trăng nhưng cũng xa gấp khoảng $400$ lần, nên hai đĩa trông gần bằng nhau.")])],
  [r"a) $\ell_x\approx2{,}16\ \text{m}$", r"b) $\alpha_S\approx0{,}531°$",
   r"c) Gần nhất $\alpha_M\approx0{,}557°$: toàn phần", r"c) Xa nhất $\alpha'_M\approx0{,}499°$: hình khuyên",
   r"d) Khoảng $88\ \%$", r"e) $\ell_{\max}\approx374\,000\ \text{km}$"],
  r"Nhận dạng: thấy <strong>toàn phần hay hình khuyên, che vừa kín</strong> → so góc trông $\alpha\approx D/\ell$, khoảng cách tính từ chỗ người đứng."),
 sol(R3, [
  ("Chiều dài nón bóng tối Mặt Trăng", [P(r"Ngày nhật thực Mặt Trăng nằm giữa:"),
     M(r"a=1{,}5\cdot10^8-363\,000=1{,}49637\cdot10^8\ \text{km}"),
     M(r"L=\dfrac{a\,D_M}{D_S-D_M}=\dfrac{1{,}49637\cdot10^8\cdot3470}{1{,}39\cdot10^6-3470}"), A(r"L\approx374\,000\ \text{km}")]),
  ("Vùng tối lúc gần nhất", [P(r"Từ Mặt Trăng tới mặt đất (chỗ gần nhất):"), M(r"x=363\,000-6370=356\,630\ \text{km}"),
     P(r"$x\lt L$: chóp nón xuyên qua mặt đất, người trong vùng tối thấy <strong>nhật thực toàn phần</strong>."),
     M(r"D_{\text{tối}}=D_M\,\dfrac{L-x}{L}=3470\cdot\dfrac{374\,489-356\,630}{374\,489}"), A(r"D_{\text{tối}}\approx165\ \text{km}")]),
  ("Vùng nửa tối lúc gần nhất", [M(r"D_{\text{nửa}}=D_M+x\,\dfrac{D_S+D_M}{a}=3470+356\,630\cdot\dfrac{1{,}39347\cdot10^6}{1{,}49637\cdot10^8}"),
     A(r"D_{\text{nửa}}\approx6790\ \text{km}"),
     P(r"Trong vùng này người ta thấy nhật thực một phần.")]),
  ("Loại nhật thực lúc xa nhất", [M(r"a'=1{,}5\cdot10^8-405\,000=1{,}49595\cdot10^8\ \text{km}"),
     M(r"L'=\dfrac{a'D_M}{D_S-D_M}\approx374\,384\ \text{km}"), M(r"x'=405\,000-6370=398\,630\ \text{km}"),
     P(r"$x'\gt L'$: chóp nón dừng trước mặt đất; người ngay dưới Mặt Trăng thấy đĩa Mặt Trời còn viền sáng: <strong>nhật thực hình khuyên</strong>.")]),
  ("Vùng thấy nhật thực hình khuyên", [P(r"Sau chóp, hai tia mép đi tiếp và loe ra với cùng độ dốc:"),
     M(r"D_{\text{khuyên}}=D_M\,\dfrac{x'-L'}{L'}=3470\cdot\dfrac{398\,630-374\,384}{374\,384}"), A(r"D_{\text{khuyên}}\approx225\ \text{km}")]),
  ("Nón bóng tối Trái Đất", [P(r"Ngày nguyệt thực vật chắn là Trái Đất, cách Mặt Trời $1\ \text{AU}$:"),
     M(r"L_E=\dfrac{1\ \text{AU}\cdot D_E}{D_S-D_E}=\dfrac{1{,}5\cdot10^8\cdot12\,740}{1{,}39\cdot10^6-12\,740}"), A(r"L_E\approx1{,}39\cdot10^6\ \text{km}")]),
  ("Vùng tối tại quỹ đạo Mặt Trăng", [M(r"D'_{\text{tối}}=D_E\,\dfrac{L_E-d}{L_E}=12\,740\cdot\dfrac{1\,387\,538-384\,000}{1\,387\,538}"),
     A(r"D'_{\text{tối}}\approx9210\ \text{km}"), M(r"\dfrac{D'_{\text{tối}}}{D_M}=\dfrac{9214}{3470}\approx2{,}66")]),
  ("Kiểm tra", [P(r"$L\approx374\,000\ \text{km}$ khớp khoảng cách giới hạn che kín tìm bằng góc trông ở Dạng 2 (cũng $\approx374\,000\ \text{km}$, làm tròn nghìn km): hai cách cho cùng kết quả ✓."),
     P(r"Vùng tối nhật thực chỉ khoảng $165\ \text{km}$: một nơi rất hiếm khi thấy nhật thực toàn phần ✓."),
     P(r"Bóng Trái Đất tại quỹ đạo rộng gấp $2{,}66$ lần Mặt Trăng: Mặt Trăng nằm gọn trong bóng, mọi nơi đang là đêm đều thấy nguyệt thực ✓.")])],
  [r"a) $L\approx374\,000\ \text{km}$", r"b) Có, toàn phần; vùng tối $\approx165\ \text{km}$; vùng nửa tối $\approx6790\ \text{km}$",
   r"c) Nhật thực hình khuyên; vùng rộng $\approx225\ \text{km}$", r"d) $L_E\approx1{,}39\cdot10^6\ \text{km}$; vùng tối $\approx9210\ \text{km}\approx2{,}66\,D_M$"],
  r"Nhận dạng: thấy <strong>bóng của Mặt Trăng, bóng Trái Đất, vùng tối rộng bao nhiêu</strong> → tam giác đồng dạng: $L=\dfrac{aD}{D_0-D}$, so $x$ với $L$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>cho ngày rằm, hỏi ngày các pha khác, ngày có thể có thực</b> → cộng bội của $S/4$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Ngày hạ huyền", "Trăng hạ huyền gần nhất rơi vào ngày nào của tháng 3 (ghi số ngày)?", 10.4, None, 0.6,
       loi=r"Cộng nửa Tuần Trăng: từ rằm tới hạ huyền chỉ mới một phần tư vòng."),
  buoc("Ngày không trăng", "Ngày không trăng kế tiếp rơi vào ngày nào của tháng 3 (ghi số ngày)?", 17.75, None, 0.8,
       loi=r"Cộng cả một Tuần Trăng; sau một Tuần Trăng thì trở lại rằm, không phải không trăng.",
       ke=[(r"Cộng thêm $\dfrac{S}{2}$ vào ngày rằm", True),
           (r"Cộng thêm $\dfrac{S}{4}$ vào ngày rằm", r"Một phần tư Tuần Trăng mới tới hạ huyền; không trăng ở phía đối diện rằm, cách nửa vòng."),
           (r"Cộng thêm $S$ vào ngày rằm", r"Sau một Tuần Trăng Mặt Trăng trở lại đúng pha cũ, tức lại là rằm.")]),
  buoc("Ngày rằm kế tiếp", "Trăng tròn kế tiếp rơi vào ngày nào của tháng 4 (ghi số ngày)?", 1.5, None, 0.6,
       loi=r"Cộng $S$ rồi trừ $30$ ngày; tháng 3 có $31$ ngày.",
       ke=[(r"Cộng $S$ vào ngày 3/3 rồi trừ $31$ ngày của tháng 3", True),
           (r"Cộng $S$ rồi trừ $30$ ngày", r"Tháng 3 có $31$ ngày; trừ $30$ thì lệch sang một ngày sau."),
           (r"Cộng $2S$ vào ngày 3/3", r"Chỉ cần một Tuần Trăng là trở lại rằm; $2S$ là rằm của tháng sau nữa.")]),
  buoc("Trăng thượng huyền", "Câu nào mô tả đúng trăng thượng huyền?",
       lua_chon=[(r"Mọc khoảng $12$ h; lúc $18$ h ở cao nhất trên bầu trời, phần sáng quay về phía Tây", True),
                 (r"Mọc khoảng $18$ h; lúc $18$ h vừa nhô lên ở phía Đông", r"Đó là trăng tròn: đối diện Mặt Trời nên mọc lúc Mặt Trời lặn."),
                 (r"Mọc khoảng $12$ h; lúc $18$ h ở cao nhất, phần sáng quay về phía Đông", r"Phần sáng luôn quay về phía Mặt Trời; lúc $18$ h Mặt Trời đang lặn ở phía Tây.")],
       loi=r"Nhầm thượng huyền với hạ huyền: hạ huyền mọc khoảng nửa đêm và sáng nửa phía Đông.",
       ke=[(r"Dùng góc $90°$ giữa Mặt Trăng và Mặt Trời, Trái Đất quay $15°$ mỗi giờ", True),
           (r"Dùng giờ mọc của trăng tròn cho mọi pha", r"Mỗi ngày trăng mọc trễ khoảng $49$ phút, mỗi pha có giờ mọc riêng tuỳ góc với Mặt Trời."),
           (r"Cho rằng phần sáng quay về phía Mặt Trăng mọc", r"Phần sáng do Mặt Trời chiếu nên quay về phía Mặt Trời, không phụ thuộc phía mọc.")]),
  buoc("Vì sao rằm tháng 4 thường không có nguyệt thực", "Nguyên nhân chính là gì?",
       lua_chon=[(r"Quỹ đạo Mặt Trăng nghiêng khoảng $5°$; một tháng sau trăng tròn không còn ở gần giao tuyến nên đi lệch khỏi bóng Trái Đất", True),
                 (r"Trái Đất tự quay nên bóng Trái Đất quay sang chỗ khác", r"Tự quay không đổi hướng bóng; bóng Trái Đất luôn nằm phía đối diện Mặt Trời."),
                 (r"Quỹ đạo Mặt Trăng là elip nên tháng sau Mặt Trăng ở quá xa, không chạm bóng", r"Khoảng cách Mặt Trăng chỉ đổi khoảng $10\ \%$, chưa đủ ra khỏi bóng; nguyên nhân là Mặt Trăng lệch lên hoặc xuống.")],
       loi=r"Cho rằng đêm rằm nào cũng có nguyệt thực, quên quỹ đạo Mặt Trăng nghiêng.",
       ke=[(r"Xét vị trí trăng tròn so với mặt phẳng quỹ đạo Trái Đất", True),
           (r"Xét khoảng cách Trái Đất – Mặt Trời trong năm", r"Khoảng cách đó chỉ đổi vài phần trăm và không quyết định ba thiên thể có thẳng hàng hay không."),
           (r"Xét tốc độ tự quay của Trái Đất", r"Tự quay chỉ quyết định nơi nào đang là đêm, không làm Mặt Trăng vào hay ra khỏi bóng.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>toàn phần hay hình khuyên, che vừa kín</b> → so góc trông $D/\ell$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Khoảng cách đồng xu", "Đồng xu phải cách mắt bao nhiêu mét?", 2.16, "m", 0.05,
       loi=r"Để đường kính đồng xu theo cm, khoảng cách Mặt Trời theo km rồi không đổi đơn vị, kết quả sai hàng trăm lần."),
  buoc("Góc trông Mặt Trời", "Góc trông Mặt Trời bằng bao nhiêu độ?", 0.531, "°", 0.003,
       loi=r"Quên đổi rad sang độ, ghi luôn tỉ số $D_S/\text{AU}$ là số độ.",
       ke=[(r"Tính $\dfrac{D_S}{1\ \text{AU}}$ rồi nhân $\dfrac{180}{\pi}$", True),
           (r"Tính $\dfrac{D_S}{1\ \text{AU}}$ và coi đó là số độ", r"Tỉ số đường kính trên khoảng cách cho góc theo rad, phải đổi sang độ."),
           (r"Tính $\dfrac{D_S/2}{1\ \text{AU}}$ rồi đổi ra độ", r"Đó là góc nhìn một bán kính; góc trông tính giữa hai mép, ứng với cả đường kính.")]),
  buoc("Góc trông Mặt Trăng lúc gần nhất", "Góc trông Mặt Trăng lúc gần nhất bằng bao nhiêu độ?", 0.557, "°", 0.003,
       loi=r"Lấy khoảng cách tâm – tâm $363\,000\ \text{km}$, quên người đứng trên mặt đất gần Mặt Trăng hơn một bán kính Trái Đất.",
       ke=[(r"Lấy $\ell=363\,000-6370\ \text{km}$ rồi tính $\dfrac{D_M}{\ell}$", True),
           (r"Lấy $\ell=363\,000\ \text{km}$", r"Đó là khoảng cách từ tâm Trái Đất; người quan sát đứng trên mặt đất, ngay dưới Mặt Trăng."),
           (r"Lấy $\ell=363\,000-12\,740\ \text{km}$", r"Từ tâm ra mặt đất chỉ là một bán kính, không phải cả đường kính Trái Đất.")]),
  buoc("Góc trông Mặt Trăng lúc xa nhất", "Góc trông Mặt Trăng lúc xa nhất bằng bao nhiêu độ?", 0.499, "°", 0.003,
       loi=r"Cộng thêm $R_E$ vào khoảng cách vì nghĩ người đứng xa hơn tâm Trái Đất.",
       ke=[(r"Làm như bước trước với $\ell=405\,000-6370\ \text{km}$", True),
           (r"Giữ nguyên góc trông của lúc gần nhất vì đường kính Mặt Trăng không đổi", r"Góc trông phụ thuộc cả khoảng cách; ở xa hơn thì trông nhỏ hơn."),
           (r"Lấy $\ell=405\,000+6370\ \text{km}$", r"Người đứng giữa tâm Trái Đất và Mặt Trăng nên khoảng cách giảm đi $R_E$, không tăng.")]),
  buoc("Toàn phần hay hình khuyên", "Kết luận nào đúng?",
       lua_chon=[(r"Lúc gần nhất: toàn phần; lúc xa nhất: hình khuyên", True),
                 (r"Cả hai lần đều toàn phần vì Mặt Trăng nằm chắn giữa", r"Chắn giữa chưa đủ: đĩa Mặt Trăng phải trông lớn hơn đĩa Mặt Trời mới che kín."),
                 (r"Lúc gần nhất: hình khuyên; lúc xa nhất: toàn phần", r"Ngược chiều: ở gần thì góc trông lớn hơn, dễ che kín hơn.")],
       loi=r"So đường kính thật $D_M$ với $D_S$ rồi kết luận Mặt Trăng không bao giờ che kín được.",
       ke=[(r"So góc trông Mặt Trăng với góc trông Mặt Trời trong từng trường hợp", True),
           (r"So đường kính thật của Mặt Trăng với Mặt Trời", r"Đường kính thật chênh khoảng $400$ lần; phải so góc trông vì nó đã kể cả khoảng cách."),
           (r"So khoảng cách tới Mặt Trăng với khoảng cách tới Mặt Trời", r"Thiếu đường kính; vật gần hơn chưa chắc trông lớn hơn.")]),
  buoc("Phần trăm diện tích bị che", "Đĩa Mặt Trời bị che tối đa bao nhiêu phần trăm diện tích?", 88, "%", 1,
       loi=r"Lấy tỉ số góc trông mà không bình phương; diện tích tỉ lệ bình phương đường kính.",
       ke=[(r"Tính $\left(\dfrac{\alpha'_M}{\alpha_S}\right)^2$", True),
           (r"Tính $\dfrac{\alpha'_M}{\alpha_S}$", r"Đó là tỉ số đường kính; diện tích hình tròn tỉ lệ bình phương đường kính."),
           (r"Tính $1-\dfrac{\alpha'_M}{\alpha_S}$", r"Đó là phần đường kính còn hở, không phải phần diện tích bị che.")]),
  buoc("Khoảng cách lớn nhất để còn che kín", "Khoảng cách đó bằng bao nhiêu nghìn km?", 374.0, "nghìn km", 0.6,
       loi=r"Đảo tỉ số thành $D_S\cdot\text{AU}/D_M$, ra khoảng cách lớn hơn cả $1\ \text{AU}$, vô lí.",
       ke=[(r"Cho góc trông Mặt Trăng bằng góc trông Mặt Trời rồi giải ra $\ell$", True),
           (r"Tính $\ell=D_S\,\dfrac{1\ \text{AU}}{D_M}$", r"Đảo ngược tỉ số; kết quả lớn hơn cả khoảng cách tới Mặt Trời là vô lí."),
           (r"Lấy trung bình hai khoảng cách $356\,630$ và $398\,630\ \text{km}$", r"Giới hạn do điều kiện hai góc trông bằng nhau quyết định, không phải trung bình cộng.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>bóng Mặt Trăng, bóng Trái Đất, vùng tối rộng bao nhiêu</b> → tam giác đồng dạng, so $x$ với $L$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Chiều dài nón bóng tối Mặt Trăng", "L bằng bao nhiêu nghìn km?", 374.0, "nghìn km", 0.6,
       loi=r"Lấy $a=1\ \text{AU}+d$ như thể Mặt Trăng ở xa Mặt Trời hơn Trái Đất; ngày nhật thực Mặt Trăng nằm giữa."),
  buoc("Vùng tối lúc gần nhất", "Đường kính vùng tối trên mặt đất bằng bao nhiêu km?", 165, "km", 4,
       loi=r"Lấy khoảng cách tới tâm Trái Đất ($363\,000\ \text{km}$) thay vì tới mặt đất; vì $L-x$ nhỏ nên sai này làm kết quả lệch rất nhiều.",
       ke=[(r"Tính $x=d-R_E$, so với $L$, rồi lấy $D_M\,\dfrac{L-x}{L}$", True),
           (r"Lấy $x=d$ rồi tính $D_M\,\dfrac{L-x}{L}$", r"Bóng rơi lên mặt đất, gần Mặt Trăng hơn tâm Trái Đất một bán kính."),
           (r"Tính $D_M\,\dfrac{x}{L}$", r"Đó là phần đường kính nón đã thu hẹp đi sau đoạn $x$, không phải phần còn lại.")]),
  buoc("Vùng nửa tối lúc gần nhất", "Đường kính vùng nửa tối bằng bao nhiêu km?", 6791, "km", 60,
       loi=r"Coi vùng nửa tối rộng đúng bằng Mặt Trăng như khi chiếu bằng chùm sáng song song.",
       ke=[(r"Tính $D_M+x\,\dfrac{D_S+D_M}{a}$", True),
           (r"Lấy đúng bằng $D_M$", r"Tia từ mép trên Mặt Trời qua mép dưới Mặt Trăng đi chéo, nên vùng nửa tối loe rộng ra."),
           (r"Tính $x\,\dfrac{D_S}{a}$", r"Thiếu chính đường kính Mặt Trăng ở gốc nón; công thức đúng còn phải cộng $D_M$ và dùng $D_S+D_M$.")]),
  buoc("Loại nhật thực lúc xa nhất", "Người ngay dưới Mặt Trăng thấy gì?",
       lua_chon=[(r"Nhật thực hình khuyên: chóp nón bóng tối dừng trước mặt đất", True),
                 (r"Nhật thực toàn phần vì ba thiên thể vẫn thẳng hàng", r"Thẳng hàng chưa đủ; phải xét chóp nón bóng tối có tới mặt đất không."),
                 (r"Không thấy nhật thực vì ở ngoài nón bóng tối", r"Ngay dưới Mặt Trăng, phần giữa đĩa Mặt Trời vẫn bị che, chỉ còn viền sáng quanh.")],
       loi=r"Dùng lại khoảng cách tới mặt đất của câu b; khoảng cách Mặt Trăng đã đổi.",
       ke=[(r"Tính lại $L$ với $a=1\ \text{AU}-405\,000$ và $x=405\,000-6370$ rồi so", True),
           (r"Dùng lại khoảng cách $x$ của câu b", r"Mặt Trăng đã ra xa thêm $42\,000\ \text{km}$, khoảng cách tới mặt đất phải tính lại."),
           (r"So $D_M$ với $D_S$", r"So đường kính thật không đủ; chóp nón phụ thuộc cả khoảng cách.")]),
  buoc("Vùng thấy nhật thực hình khuyên", "Đường kính vùng đó bằng bao nhiêu km?", 225, "km", 4,
       loi=r"Vẫn dùng $D_M\,\dfrac{L-x}{L}$ nên ra số âm.",
       ke=[(r"Tính $D_M\,\dfrac{x-L}{L}$", True),
           (r"Tính $D_M\,\dfrac{L-x}{L}$", r"Lúc này $x\gt L$ nên biểu thức âm; sau chóp, các tia mép loe ra và độ rộng là $D_M\,\dfrac{x-L}{L}$."),
           (r"Tính $D_M+x\,\dfrac{D_S+D_M}{a}$", r"Đó là vùng nửa tối, nơi chỉ thấy nhật thực một phần, rộng hàng nghìn km.")]),
  buoc("Nón bóng tối Trái Đất", "Nón bóng tối Trái Đất dài bao nhiêu triệu km?", 1.39, "triệu km", 0.01,
       loi=r"Dùng đường kính Mặt Trăng thay cho đường kính Trái Đất; ngày nguyệt thực vật chắn là Trái Đất.",
       ke=[(r"Tính $\dfrac{1\ \text{AU}\cdot D_E}{D_S-D_E}$", True),
           (r"Tính $\dfrac{1\ \text{AU}\cdot D_M}{D_S-D_M}$", r"Ngày nguyệt thực vật chắn sáng là Trái Đất, không phải Mặt Trăng."),
           (r"Tính $\dfrac{1\ \text{AU}\cdot D_E}{D_S+D_E}$", r"Dấu cộng ứng với điểm giao của các tia nửa tối; chóp nón bóng tối dùng $D_S-D_E$.")]),
  buoc("Vùng tối tại quỹ đạo Mặt Trăng", "Đường kính vùng tối tại quỹ đạo Mặt Trăng bằng bao nhiêu km?", 9214, "km", 60,
       loi=r"Coi bóng Trái Đất rộng bằng Trái Đất; nón bóng tối hẹp dần nên tại quỹ đạo Mặt Trăng nhỏ hơn $D_E$.",
       ke=[(r"Tính $D_E\,\dfrac{L_E-d}{L_E}$ với $d=384\,000\ \text{km}$", True),
           (r"Lấy đúng bằng $D_E$", r"Nón bóng tối thu nhỏ dần về chóp, nên càng xa Trái Đất càng hẹp."),
           (r"Tính $D_E\,\dfrac{d}{L_E}$", r"Đó là phần đường kính đã thu hẹp đi, không phải phần còn lại.")]),
  buoc("Kiểm tra")]),
]


def kiem_so():
    deg = DEG
    # D1
    assert abs(NGAY_HH - 10.375) < 1e-9 and abs(NGAY_KT - 17.75) < 1e-9 and abs(NGAY_RAM - 1.5) < 1e-9
    assert abs(LECH - 29.08) < 0.01 and abs(VD - 2.43) < 0.01
    u_rad = (16331 / 2) / D_TB * deg + (D_M / 2) / D_TB * deg       # bán kính góc nửa tối + bán kính góc Mặt Trăng
    assert abs(u_rad - 1.48) < 0.01 and VD > u_rad
    assert abs((3 + S / 2) - 10.4) > 0.6 and abs((3 + S) - 17.75) > 0.8              # lỗi D1 bước 1, 2
    assert abs((3 + S / 4) - 17.75) > 0.8
    assert abs((3 + S - 30) - 1.5) > 0.6 and abs((3 + 2 * S - 31) - 1.5) > 0.6       # lỗi D1 bước 3
    # D2
    assert abs(XU - 2.158) < 1e-3 and abs(XU * 100 - 2.16) > 0.05                     # quên đổi cm→m
    assert abs(A_S - 0.5309) < 1e-4 and round(A_S, 3) == 0.531
    assert abs(D_S / AU - 0.531) > 0.003 and abs(A_S / 2 - 0.531) > 0.003
    assert round(A_GAN, 3) == 0.557 and round(A_XA, 3) == 0.499
    assert abs(D_M / D_GAN * deg - 0.557) > 0.003 and abs(D_M / (D_GAN - D_E) * deg - 0.557) > 0.003
    assert abs(A_GAN - 0.499) > 0.003 and abs(D_M / (D_XA + R_E) * deg - 0.499) > 0.003
    assert A_GAN > A_S > A_XA
    assert round(TI_LE * 100) == 88 and abs(A_XA / A_S * 100 - 88) > 1 and abs((1 - A_XA / A_S) * 100 - 88) > 1
    assert abs(L_MAX - 374460) < 1 and round(L_MAX, -3) == 374_000
    assert abs(D_S * AU / D_M / 1000 - 374.0) > 0.6 and abs((L_GAN + L_XA) / 2000 - 374.0) > 0.6 and abs(L_MAX / 1000 - 374.0) < 0.6
    assert L_GAN < L_MAX < L_XA
    assert abs(L_MAX / D_M - XU / 0.02) < 0.01 and round(XU / 0.02) == 108
    # D3
    assert abs(L3G - 374489) < 1 and abs(L3G / 1000 - 374.0) < 0.6
    assert abs((AU + D_GAN) * D_M / (D_S - D_M) / 1000 - 374.0) > 0.6
    assert X3G == 356630 and X3G < L3G and abs(TOI_GAN - 165.5) < 0.1 and abs(TOI_GAN - 165) < 4
    assert abs(D_M * (L3G - D_GAN) / L3G - 165) > 4 and abs(D_M * X3G / L3G - 165) > 4
    assert abs(NUA_GAN - 6791) < 1 and abs(D_M - 6791) > 60 and abs(D_S * X3G / A3G - 6791) > 60
    assert abs(L3X - 374384) < 1 and X3X == 398630 and X3X > L3X and abs(KHUYEN - 224.7) < 0.1 and abs(KHUYEN - 225) < 4
    assert D_M * (L3X - X3X) / L3X < 0 and abs(D_M + X3X * (D_S + D_M) / A3X - 225) > 4
    # dùng lại L lúc gần cho lúc xa vẫn trong sai số (không phạt cách gần đúng này)
    assert abs(D_M * (X3X - L3G) / L3G - 225) < 4
    assert abs(L_E - 1387538) < 1 and abs(L_E / 1e6 - 1.39) < 0.01
    assert abs(AU * D_M / (D_S - D_M) / 1e6 - 1.39) > 0.01 and abs(AU * D_E / (D_S + D_E) / 1e6 - 1.39) > 0.01
    assert abs(TOI_E - 9214) < 1 and abs(TOI_E / D_M - 2.66) < 0.005
    assert abs(D_E - 9214) > 60 and abs(D_E * D_TB / L_E - 9214) > 60
    assert abs(L3G - L_MAX) < 100                                                    # hai cách gần trùng nhau
    print("kiểm số liệu D1–D3 (bài 178): đạt")
