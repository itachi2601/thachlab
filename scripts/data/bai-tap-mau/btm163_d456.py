"""Bài tập mẫu CĐ09 "Năng lượng với cuộc sống" (lesson 163) — Dạng 4–5 (phần khó).
Module được build-hinh-163.py import. Dàn ý: content/hsg9/cd09-nang-luong-cuoc-song/nguon.md mục "Bài tập mẫu" (số liệu dùng nguyên,
tính lại ở tinh.py cùng thư mục). Dạng sau dùng lại cách làm dạng trước:
  D4 điện gió: H = P_ích/P_tp (D1) + lập phương tốc độ gió + vùng làm việc; điện năng ngày so với nhà máy than D1 (7920 MWh)
  D5 xe xăng và xe điện: chuỗi hiệu suất nhân nhau (D1), Q = qm, m_CO2 = k·m, tiền = lượng dùng × đơn giá (D3).
Xuất DANG, BUILD, ANALYSIS, SOLS, STEPS (2 phần tử mỗi list) và kiem_so()."""
import math, os, re, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *  # noqa: F401,F403  (fig, seg, lbl, dot, chevron, arrow, sol, M, P, A, buoc …)

T_TT = "Các dạng năng lượng tái tạo và nguồn gốc"
T_HT = "Ưu nhược điểm của nhiên liệu hoá thạch"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"

# ═════════════ SỐ LIỆU (mọi đáp số tính ở đây, kiem_so() kiểm lại) ═════════════
KWH = 3_600_000
# D4 — điện gió
DQ4, DKK, VDM, PDM, VKD, VNG = 80, F(6, 5), 12, F(2), 3, 25          # m ; kg/m³ ; m/s ; MW ; m/s ; m/s
S4 = math.pi * DQ4 ** 2 / 4                                         # ≈ 5027 m²
PG4 = 0.5 * float(DKK) * S4 * VDM ** 3 / 1e6                        # ≈ 5,21 MW
H4 = float(PDM) / PG4                                               # ≈ 38,4 %
BANG4 = [(4, 2), (8, 6), (6, 9), (4, 12), (2, 15)]                  # (giờ, v m/s)
def P4(v):
    if v < VKD or v > VNG:
        return F(0)
    if v >= VDM:
        return PDM
    return PDM * F(v, VDM) ** 3
A4 = sum(h * P4(v) for h, v in BANG4)                               # 19,0625 MWh
HSCS4 = A4 / (PDM * 24)                                             # ≈ 39,7 %
A_D1 = 330 * 24                                                     # 7920 MWh — nhà máy than D1
N4 = math.ceil(A_D1 / A4)                                           # 416
# D5 — xe máy xăng và xe máy điện
F5, S5 = 70, 40_000
AICH5 = F5 * S5                                                     # 2,8·10⁶ J
HX, QX, DX, KX, GX = F(15, 100), 46_000_000, F(7, 10), F(16, 5), 24_000
QTP5 = AICH5 / HX                                                   # ≈ 1,867·10⁷ J
MX5 = QTP5 / QX                                                     # ≈ 0,406 kg
VX5 = MX5 / DX                                                      # ≈ 0,580 L
TX5 = VX5 * GX                                                      # ≈ 13 913 đ
CX5 = KX * MX5                                                      # ≈ 1,30 kg CO₂
HDC, HS, GD, KE = F(4, 5), F(9, 10), 3000, F(13, 20)
HE5 = HDC * HS                                                      # 72 %
AE5 = AICH5 / HE5 / KWH                                             # ≈ 1,080 kWh
TE5 = AE5 * GD                                                      # ≈ 3241 đ
CE5 = KE * AE5                                                      # ≈ 0,702 kg CO₂
TK5 = (TX5 - TE5) * 365                                             # ≈ 3,90 triệu đồng/năm
HNM, QT, KT = F(363, 1000), 27_000_000, F(5, 2)
HC5 = HNM * HE5                                                     # ≈ 26,1 %
MT5 = AICH5 / HC5 / QT                                              # ≈ 0,397 kg than
CT5 = KT * MT5                                                      # ≈ 0,992 kg CO₂
KE_TD = KT / (HNM * QT / KWH)                                       # ≈ 0,92 kg CO₂/kWh


def rich(s, size=14):
    """Nhãn SVG có chỉ số dưới: 'v_{kđ}' → tspan dy (chỉ số Unicode hiện như dấu phẩy ở một số máy)."""
    ms = list(re.finditer(r"_\{([^}]+)\}", s))
    if not ms:
        return s
    out = s[:ms[0].start()]
    for k, m in enumerate(ms):
        out += f'<tspan dy="4" font-size="{max(12, size - 2)}">{m.group(1)}</tspan>'
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        out += f'<tspan dy="-4">{s[m.end():nxt]}</tspan>' if s[m.end():nxt] else '<tspan dy="-4"></tspan>'
    return out

def txt(x, y, s, c="currentColor", size=14, anchor="start", weight="700", extra=""):
    size = max(size, 14)
    t = lbl(x, y, rich(s, size), c, size, anchor, weight)
    return t.replace("<text ", f"<text {extra} ", 1) if extra else t

def show_at(t, dur):
    k = max(0.001, min(0.999, t / dur))
    return (f'<animate attributeName="opacity" values="0;1" keyTimes="0;{k:.4f}" calcMode="discrete" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')

def show_between(k0, k1, dur):
    if k0 <= 0:
        return (f'<animate attributeName="opacity" values="1;0" keyTimes="0;{k1:.4f}" calcMode="discrete" '
                f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')
    return (f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{k0:.4f};{k1:.4f}" calcMode="discrete" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def rect(x, y, w, h, c="currentColor", sw=2, fill="none", op=1, rx=0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" '
            f'stroke="{c}" stroke-width="{sw}"/>')

def timed(k0, s, x, y, c="currentColor", size=14, anchor="start", weight="700", k1=None, dur=None):
    """Nhãn hiện từ phân số k0 (tới k1 nếu có) của mô phỏng dài dur. k0 = 0 → hiện sẵn lúc đầu."""
    if k1 is not None:
        a = show_between(k0, k1, dur)
        op = "1" if k0 <= 0 else "0"
    else:
        a, op = show_at(k0 * dur, dur), "0"
    return txt(x, y, s, c, size, anchor, weight, f'opacity="{op}"').replace("</text>", a + "</text>", 1)

def box(x, y, w, h, lines, c="currentColor", fill="none", op=.12):
    b = rect(x, y, w, h, c, 2, fill, op, 6)
    for k, (s, col) in enumerate(lines):
        b += txt(x + w / 2, y + 21 + 19 * k, s, col, 14, "middle", "600")
    return b


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 4 · tuabin gió trong một ngày ─────────────
def d4(kk):
    b = ""
    if kk == 0:
        TT = 12.0                                   # 24 h → 12 s (1 s = 2 h)
        HX0, HY0, RB = 125, 100, 54                 # tâm rôto, độ dài cánh
        # cánh quay: tốc độ góc ∝ v trong vùng 3–12 m/s, không đổi từ 12 m/s, bằng 0 dưới 3 m/s (minh hoạ)
        omega = lambda v: 0 if v < VKD or v > VNG else 36 * min(v, VDM)       # °/s mô phỏng
        ang, kts, t = [0.0], [0.0], 0.0
        for h, v in BANG4:
            dt = h / 2
            ang.append(ang[-1] + omega(v) * dt); t += dt; kts.append(t / TT)
        b += f'<path d="M{HX0 - 7},214 L{HX0 - 3},{HY0 + 6} L{HX0 + 3},{HY0 + 6} L{HX0 + 7},214 Z" fill="{GREY}" fill-opacity=".35" stroke="currentColor" stroke-width="1.8"/>'
        b += seg(16, 214, 180, 214, "currentColor", 2)
        blades = "".join(f'<path d="M0,0 L{RB * math.cos(math.radians(a)):.1f},{RB * math.sin(math.radians(a)):.1f}" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>'
                         for a in (-90, 30, 150))
        b += (f'<g transform="translate({HX0} {HY0})"><g>{blades}'
              f'<animateTransform attributeName="transform" type="rotate" values="{";".join(f"{a:.0f}" for a in ang)}" '
              f'keyTimes="{";".join(f"{k:.4f}" for k in kts)}" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>'
              f'<circle r="7" fill="{GREY}" stroke="currentColor" stroke-width="2"/></g>')
        b += txt(HX0, 236, "d_{q} = 80 m", "currentColor", 14, "middle", "600")
        # mũi tên gió: dài ∝ v (3,5 px mỗi m/s), hiện theo từng khoảng
        KS = [0.0]
        for h, _ in BANG4:
            KS.append(KS[-1] + h / 2 / TT)
        last = len(BANG4) - 1
        for i, (h, v) in enumerate(BANG4):
            anim = show_at(KS[i] * TT, TT) if i == last else show_between(KS[i], KS[i + 1], TT)
            for yy in (70, 100, 130):
                b += f'<g opacity="{1 if i == 0 else 0}">{arrow("", "b", 10, yy, round(10 + 3.5 * v, 1), yy, 2.4)}{anim}</g>'
        # thanh thời gian 24 h
        X0, X1, YB = 200, 372, 172
        px = (X1 - X0) / 24
        t = 0
        cols = [GREY, BLUE, BLUE, GRN, ORG]
        for (h, v), cc in zip(BANG4, cols):
            b += rect(X0 + t * px, YB, h * px, 18, "currentColor", 1.4, cc, .35)
            b += txt(X0 + (t + h / 2) * px, YB + 38, str(v), "currentColor", 14, "middle", "700")
            t += h
        b += txt(X0 - 4, YB + 14, "0 h", "currentColor", 14, "end", "600") + txt(X1 + 4, YB + 14, "24 h", "currentColor", 14, "start", "600")
        b += txt(X0, YB + 60, "v (m/s) từng khoảng", "currentColor", 14, "start", "600")
        b += (f'<path d="M{X0},{YB - 2} l-6,-10 h12 z" fill="{RED}">'
              f'<animateTransform attributeName="transform" type="translate" values="0 0;{X1 - X0} 0" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></path>')
        for i, (h, v) in enumerate(BANG4):
            b += timed(KS[i], f"gió {v} m/s", 200, 70, BLUE, 14, "start", "700", None if i == last else KS[i + 1], TT)
        b += timed(.999, "P từng khoảng = ?", 200, 100, RED, 14, "start", "700", None, TT)
        b += timed(.999, "A cả ngày = ?", 200, 124, RED, 14, "start", "700", None, TT)
        b += txt(16, 22, "Một ngày gió thổi qua tuabin", "currentColor", 14)
        return fig("c09-4-0", "0 0 420 250", "Tuabin gió quay theo gió thay đổi trong 24 giờ; thanh thời gian ghi tốc độ gió từng khoảng",
                   b, "Mô phỏng: 1 s ứng với 2 h thật; tốc độ quay và độ dài mũi tên gió chỉ minh hoạ. Khung cuối không ghi kết quả.")
    # hình dữ kiện: đồ thị v(t) dạng bậc thang + ba ngưỡng
    OX, OY, X1 = 50, 230, 340
    px, py = (X1 - OX) / 24, 7.6
    b += txt(16, 18, "Tốc độ gió trong ngày và ba ngưỡng của tuabin", "currentColor", 14)
    t = 0
    for h, v in BANG4:
        b += rect(OX + t * px, OY - v * py, h * px, v * py, BLUE, 1.6, BLUE, .18)
        b += txt(OX + (t + h / 2) * px, OY - v * py + (18 if v == VDM else -6), str(v), BLUE, 14, "middle", "700")
        t += h
    for v, name in ((VKD, "v_{kđ}"), (VDM, "v_{đm}"), (VNG, "v_{ngắt}")):
        y = OY - v * py
        b += seg(OX, y, X1, y, ORG, 1.6, "6 4") + txt(X1 + 6, y + 5, name, ORG, 14, "start", "700")
        b += txt(OX - 6, y + 5, str(v), ORG, 14, "end", "700")
    b += seg(OX, OY, X1 + 10, OY, "currentColor", 2) + chevron(X1 + 10, OY, 1, 0, "currentColor", 2, 9)
    b += seg(OX, OY, OX, 26, "currentColor", 2) + chevron(OX, 26, 0, -1, "currentColor", 2, 9)
    b += txt(OX + 8, 40, "v (m/s)", "currentColor", 14, "start", "600")
    tt = 0
    for h, _ in [(0, 0)] + BANG4:
        tt += h
        b += txt(OX + tt * px, OY + 20, str(tt), "currentColor", 14, "middle", "600")
    b += txt(X1 + 18, OY + 20, "t (h)", "currentColor", 14, "start", "600")
    return fig("c09-4-2", "0 0 420 256", "Đồ thị bậc thang tốc độ gió theo thời gian trong 24 giờ, kèm ba đường ngưỡng khởi động, định mức và ngắt",
               b, "Dữ kiện: số trên mỗi cột là tốc độ gió (m/s) trong khoảng đó; ba đường nét đứt là ba ngưỡng của tuabin.")


# ───────────── Dạng 5 · xe xăng và xe điện ─────────────
def bike(c):
    return (f'<circle cx="-16" cy="0" r="9" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            f'<circle cx="18" cy="0" r="9" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            f'<path d="M-16,0 L-4,-14 L14,-14 L18,0 M10,-14 L14,-26 L20,-26" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            f'<rect x="-8" y="-22" width="18" height="9" rx="3" fill="{c}" fill-opacity=".7" stroke="currentColor" stroke-width="1.4"/>')

def d5(kk):
    b = ""
    if kk == 0:
        TT = 7.0
        b += txt(16, 22, "Cùng quãng đường 40 km, lực cản 70 N", "currentColor", 14)
        for yy, name, c in ((96, "xe xăng", ORG), (186, "xe điện", BLUE)):
            b += seg(16, yy + 10, 404, yy + 10, "currentColor", 2) + seg(16, yy + 14, 404, yy + 14, GREY, 1, "6 6")
            b += txt(16, yy - 40, name, c, 14, "start", "700")
            extra = ""
            if c == ORG:      # khói thải phía sau xe xăng
                for k in range(3):
                    extra += (f'<circle cx="{-34 - 12 * k}" cy="{-4 - 4 * k}" r="{4 + 2 * k}" fill="{GREY}" fill-opacity=".55" opacity="0">'
                              f'<animate attributeName="opacity" values="0;1;1" keyTimes="0;{.04 + .03 * k:.2f};1" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></circle>')
            else:             # tia sét nhỏ: dùng điện
                extra += f'<path d="M-2,-40 l-6,10 h6 l-4,9" fill="none" stroke="{BLUE}" stroke-width="2"/>'
            b += (f'<g transform="translate(60 {yy})">{extra}{bike(c)}'
                  f'<animateTransform attributeName="transform" type="translate" values="60 {yy};370 {yy}" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += timed(.999, "xăng: ? L ; CO_{2}: ? kg", 404, 134, ORG, 14, "end", "700", None, TT)
        b += timed(.999, "điện: ? kWh ; CO_{2}: ? kg", 404, 224, BLUE, 14, "end", "700", None, TT)
        return fig("c09-5-0", "0 0 420 236", "Xe máy xăng và xe máy điện cùng chạy quãng đường 40 km mỗi ngày",
                   b, "Mô phỏng: không theo thời gian thật, không theo tỉ lệ. Khung cuối không ghi kết quả.")
    # hình dữ kiện: ba chuỗi năng lượng
    b += txt(16, 20, "Năng lượng đi qua những khâu nào tới bánh xe?", "currentColor", 14)
    def link(x1, x2, y, l1, l2):
        return (arrow("", "o", x1, y, x2, y, 2.2) + txt((x1 + x2) / 2, y - 8, l1, "currentColor", 14, "middle", "600")
                + txt((x1 + x2) / 2, y + 20, l2, ORG, 14, "middle", "700"))
    BW, BH = 84, 48
    X = (8, 168, 328)
    # 1 · xe xăng
    y = 34
    b += box(X[0], y, BW, BH, [("xăng", "currentColor"), ("Q = q·m", ORG)], ORG, ORG)
    b += link(X[0] + BW + 4, X[2] - 4, y + BH / 2, "động cơ", "15 %")
    b += box(X[2], y, BW, BH, [("bánh xe", "currentColor"), ("A_{ích}", GRN)], GRN, GRN)
    # 2 · xe điện
    y = 104
    b += box(X[0], y, BW, BH, [("ổ điện", "currentColor"), ("A = ?", RED)], BLUE, BLUE)
    b += link(X[0] + BW + 4, X[1] - 4, y + BH / 2, "sạc", "90 %")
    b += box(X[1], y, BW, BH, [("acquy", "currentColor")], BLUE, BLUE, .06)
    b += link(X[1] + BW + 4, X[2] - 4, y + BH / 2, "động cơ", "80 %")
    b += box(X[2], y, BW, BH, [("bánh xe", "currentColor"), ("A_{ích}", GRN)], GRN, GRN)
    # 3 · điện từ nhà máy than (câu c)
    y = 174
    b += box(X[0], y, BW, BH, [("than", "currentColor"), ("k = 2,5", ORG)], ORG, ORG)
    b += link(X[0] + BW + 4, X[1] - 4, y + BH / 2, "nhà máy", "36,3 %")
    b += box(X[1], y, BW, BH, [("ổ điện", "currentColor")], BLUE, BLUE, .06)
    b += link(X[1] + BW + 4, X[2] - 4, y + BH / 2, "sạc và", "động cơ")
    b += box(X[2], y, BW, BH, [("bánh xe", "currentColor"), ("A_{ích}", GRN)], GRN, GRN)
    return fig("c09-5-2", "0 0 420 232", "Ba chuỗi năng lượng: xăng qua động cơ tới bánh xe; ổ điện qua sạc và động cơ; than qua nhà máy điện rồi tới xe điện",
               b, "Dữ kiện: phần trăm trên mũi tên là hiệu suất của khâu đó; ba chuỗi cùng cần một công có ích ở bánh xe. " + NOTE)


BUILD = [d4, d5]

# ═════════════ ĐỀ ═════════════
DANG = [
dict(label="Dạng 4 · Nâng cao · Điện gió: công suất theo lập phương tốc độ gió và vùng làm việc của tuabin",
     topic=T_TT,
     problem_html=r"""<p>Một tuabin gió có cánh quạt quét thành vòng tròn đường kính $80\ \text{m}$. Tuabin bắt đầu phát điện khi tốc độ gió đạt $3\ \text{m/s}$; đạt công suất định mức $2{,}0\ \text{MW}$ khi gió $12\ \text{m/s}$ và được điều khiển giữ đúng công suất định mức khi gió từ $12\ \text{m/s}$ tới $25\ \text{m/s}$; gió mạnh hơn $25\ \text{m/s}$ thì tuabin dừng để an toàn. Khi gió từ $3\ \text{m/s}$ tới dưới $12\ \text{m/s}$, coi công suất điện tỉ lệ với lập phương tốc độ gió. Khối lượng riêng của không khí là $1{,}2\ \text{kg/m}^3$; công suất của dòng gió đi qua vòng quét là $P_{gió}=\dfrac12D_{kk}Sv^3$ với $S$ là diện tích vòng quét.</p><ol type="a"><li>Tính công suất của dòng gió khi gió $12\ \text{m/s}$ và hiệu suất của tuabin lúc đó. So sánh với giới hạn Betz $59{,}3\,\%$.</li><li>Trong một ngày, gió thổi: $4$ h ở $2\ \text{m/s}$; $8$ h ở $6\ \text{m/s}$; $6$ h ở $9\ \text{m/s}$; $4$ h ở $12\ \text{m/s}$; $2$ h ở $15\ \text{m/s}$. Tính điện năng tuabin phát trong ngày (theo MWh) và hệ số công suất (tỉ số giữa điện năng thực phát và điện năng nếu tuabin chạy định mức suốt $24$ h).</li><li>Một nhà máy nhiệt điện công suất điện $330\ \text{MW}$ chạy liên tục cả ngày. Cần ít nhất bao nhiêu tuabin như trên, với gió như câu b, để phát được lượng điện bằng nhà máy đó trong một ngày? Bỏ qua hao phí trên đường dây tải điện.</li></ol>"""),
dict(label="Dạng 5 · Vận dụng cao · So sánh phương án: xe máy xăng và xe máy điện, tính từ nguồn tới bánh xe",
     topic=T_HT,
     problem_html=r"""<p>Một học sinh mỗi ngày đi xe máy tổng cộng $40\ \text{km}$; lực cản trung bình tác dụng lên xe là $70\ \text{N}$, coi lực kéo bằng lực cản. Bỏ qua hao phí trên đường dây tải điện. So sánh hai phương án:</p><ul><li>Xe xăng: hiệu suất động cơ $15\,\%$; xăng có năng suất toả nhiệt $4{,}6\cdot10^7\ \text{J/kg}$, khối lượng riêng $0{,}70\ \text{kg/L}$, giá $24\,000$ đồng/L; đốt $1\ \text{kg}$ xăng thải ra $3{,}2\ \text{kg}$ khí CO₂.</li><li>Xe điện: hiệu suất động cơ điện $80\,\%$, hiệu suất sạc (từ ổ điện vào acquy) $90\,\%$; giá điện $3\,000$ đồng/kWh; mỗi kWh điện lưới ứng với $0{,}65\ \text{kg}$ khí CO₂ thải ra ở các nhà máy điện.</li></ul><ol type="a"><li>Tính thể tích xăng xe xăng dùng mỗi ngày và khối lượng khí CO₂ thải ra.</li><li>Tính điện năng xe điện lấy từ ổ điện mỗi ngày (theo kWh) và khối lượng khí CO₂ tương ứng. Một năm ($365$ ngày) dùng xe điện thay xe xăng thì tiết kiệm được bao nhiêu tiền?</li><li>Giả sử toàn bộ điện sạc xe lấy từ một nhà máy nhiệt điện than có hiệu suất $36{,}3\,\%$; than có năng suất toả nhiệt $2{,}7\cdot10^7\ \text{J/kg}$, đốt $1\ \text{kg}$ than thải ra $2{,}5\ \text{kg}$ khí CO₂. Tính hiệu suất của cả chuỗi từ than tới bánh xe và khối lượng khí CO₂ thải ra mỗi ngày. Khi đó xe điện còn thải ít CO₂ hơn xe xăng không?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 1 nguyên văn đề ; cột 2 chỉ dữ liệu có trong đề ; cột 3 kiến thức nền + câu hỏi gợi) ═════════════
ANALYSIS = [
 # Dạng 4
 [(r'"cánh quạt quét thành vòng tròn đường kính $80\ \text{m}$"', r"$d_q=80\ \text{m}$", r"Diện tích hình tròn theo đường kính : $S=\dfrac{\pi d_q^2}{4}$"),
  (r'"công suất của dòng gió đi qua vòng quét là $P_{gió}=\dfrac12D_{kk}Sv^3$"', r"$D_{kk}=1{,}2\ \text{kg/m}^3$", r"Công thức đề cho sẵn ; $v$ có số mũ mấy ?"),
  (r'"đạt công suất định mức $2{,}0\ \text{MW}$ khi gió $12\ \text{m/s}$"', r"$P_{đm}=2{,}0\ \text{MW}$ ; $v_{đm}=12\ \text{m/s}$", r"Hiệu suất : $H=\dfrac{P_{ích}}{P_{tp}}$ ; ở đây phần nào là có ích, phần nào là toàn phần ?"),
  (r'"Tuabin bắt đầu phát điện khi tốc độ gió đạt $3\ \text{m/s}$"', r"$v_{kđ}=3\ \text{m/s}$", r"⚠ gió dưới ngưỡng này thì tuabin có phát điện không ?"),
  (r'"được điều khiển giữ đúng công suất định mức khi gió từ $12\ \text{m/s}$ tới $25\ \text{m/s}$"', r"$v_{ngắt}=25\ \text{m/s}$", r"⚠ mỗi tốc độ gió trong bảng nằm ở vùng nào : dưới $v_{kđ}$, giữa $v_{kđ}$ và $v_{đm}$, hay giữa $v_{đm}$ và $v_{ngắt}$ ?"),
  (r'"coi công suất điện tỉ lệ với lập phương tốc độ gió"', r"$P\propto v^3$ khi $3\le v\lt12\ \text{m/s}$", r"Gió nhỏ đi $k$ lần so với $v_{đm}$ thì công suất nhỏ đi mấy lần ?"),
  (r'"Trong một ngày, gió thổi"', r"năm khoảng, tổng $24$ h", r"Mỗi khoảng có công suất riêng : điện năng cả ngày ghép từ các khoảng thế nào ?"),
  (r'"hệ số công suất (tỉ số giữa điện năng thực phát và điện năng nếu tuabin chạy định mức suốt $24$ h)"', r"hệ số $=?$", r"$\dfrac{A}{P_{đm}\cdot24\ \text{h}}$"),
  (r'"Cần ít nhất bao nhiêu tuabin như trên"', r"$P_{nm}=330\ \text{MW}$, chạy $24$ h ; $n=?$", r"So sánh đại lượng nào của nhà máy và của một tuabin : công suất hay điện năng trong ngày ? Số tuabin làm tròn thế nào ?"),
  (r'"Bỏ qua hao phí trên đường dây tải điện"', r"không mất điện năng khi truyền tải", r"⚠ điều kiện để coi điện tuabin phát ra bằng điện tới nơi dùng")],
 # Dạng 5
 [(r'"lực cản trung bình tác dụng lên xe là $70\ \text{N}$, coi lực kéo bằng lực cản"', r"$F=70\ \text{N}$ ; $s=40\ \text{km}$", r"⚠ công có ích ở bánh xe như nhau cho hai xe : $A_{ích}=Fs$, đổi $s$ ra mét"),
  (r'"hiệu suất động cơ $15\,\%$"', r"$H_x=15\,\%$", r"$H=\dfrac{A_{ích}}{Q}$ : biết $A_{ích}$ và $H$, tìm $Q$ bằng phép tính nào ?"),
  (r'"năng suất toả nhiệt $4{,}6\cdot10^7\ \text{J/kg}$, khối lượng riêng $0{,}70\ \text{kg/L}$"', r"$q_x=4{,}6\cdot10^7\ \text{J/kg}$ ; $D_x=0{,}70\ \text{kg/L}$", r"$Q=qm$ ; $D=\dfrac{m}{V}$"),
  (r'"đốt $1\ \text{kg}$ xăng thải ra $3{,}2\ \text{kg}$ khí CO₂"', r"$k_x=3{,}2$", r"⚠ hệ số tính cho mỗi kilôgam hay mỗi lít xăng ?"),
  (r'"hiệu suất động cơ điện $80\,\%$, hiệu suất sạc (từ ổ điện vào acquy) $90\,\%$"', r"$H_{đc}=80\,\%$ ; $H_s=90\,\%$", r"Hai khâu nối tiếp : hiệu suất chung của chuỗi tính thế nào ?"),
  (r'"mỗi kWh điện lưới ứng với $0{,}65\ \text{kg}$ khí CO₂"', r"$k_e=0{,}65\ \text{kg/kWh}$", r"$1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$"),
  (r'"Một năm ($365$ ngày) dùng xe điện thay xe xăng thì tiết kiệm được bao nhiêu tiền?"', r"$24\,000$ đồng/L ; $3\,000$ đồng/kWh", r"Tiền $=$ lượng dùng $\times$ đơn giá ; lượng dùng phải cùng đơn vị với đơn giá (L, kWh)"),
  (r'"nhà máy nhiệt điện than có hiệu suất $36{,}3\,\%$"', r"$H_{nm}=36{,}3\,\%$ ; $q_t=2{,}7\cdot10^7\ \text{J/kg}$ ; $k_t=2{,}5$", r"⚠ đã bỏ qua hao phí đường dây : từ than tới bánh xe năng lượng qua những khâu nào ?"),
  (r'"Khi đó xe điện còn thải ít CO₂ hơn xe xăng không?"', r"so sánh $m_{CO_2}$", r"So sánh hai khối lượng CO₂ cho cùng quãng đường $40\ \text{km}$")],
]

# ═════════════ LỜI GIẢI ═════════════
R4 = [r"<strong>Hiệu suất:</strong> $H=\dfrac{P_{ích}}{P_{tp}}$ ; với tuabin, $P_{tp}$ là công suất dòng gió, $P_{ích}$ là công suất điện.",
      r"<strong>Gió:</strong> $P_{gió}=\dfrac12D_{kk}Sv^3$, $S=\dfrac{\pi d_q^2}{4}$ ; giới hạn Betz $59{,}3\,\%$ là mức tối đa.",
      r"<strong>Vùng làm việc:</strong> $v\lt v_{kđ}$ hoặc $v\gt v_{ngắt}$ : $P=0$ ; $v_{kđ}\le v\lt v_{đm}$ : $P=P_{đm}\left(\dfrac{v}{v_{đm}}\right)^3$ ; $v_{đm}\le v\le v_{ngắt}$ : $P=P_{đm}$.",
      r"<strong>Điện năng:</strong> $A=Pt$ ; $1\ \text{MW}\cdot1\ \text{h}=1\ \text{MWh}$.",
      r"<strong>Điều kiện:</strong> bỏ qua hao phí đường dây ; số tuabin là số nguyên."]
R5 = [r"<strong>Công có ích:</strong> $A_{ích}=Fs$, lực kéo bằng lực cản.",
      r"<strong>Hiệu suất:</strong> $H=\dfrac{A_{ích}}{A_{tp}}$ ; chuỗi nhiều khâu nối tiếp $H=H_1H_2H_3\dots$",
      r"<strong>Nhiên liệu:</strong> $Q=qm$ ; $m=DV$ ; khí thải $m_{CO_2}=k\,m$ hoặc $k_eA$.",
      r"<strong>Đổi đơn vị:</strong> $1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$ ; tiền $=$ lượng dùng $\times$ đơn giá.",
      r"<strong>Điều kiện:</strong> bỏ qua hao phí đường dây ; hai xe cùng quãng đường, cùng lực cản."]

SOLS = [
 sol(R4, [
  ("Công suất dòng gió ở 12 m/s", [P(r"Diện tích vòng quét (đề cho đường kính) :"), M(r"S=\dfrac{\pi d_q^2}{4}=\dfrac{\pi\cdot80^2}{4}\approx5027\ \text{m}^2"),
     M(r"P_{gió}=\dfrac12D_{kk}Sv^3=\dfrac12\cdot1{,}2\cdot5027\cdot12^3"), A(r"P_{gió}\approx5{,}21\cdot10^6\ \text{W}=5{,}21\ \text{MW}")]),
  ("Hiệu suất của tuabin ở 12 m/s", [P(r"Công suất điện lúc này là công suất định mức :"), M(r"H=\dfrac{P_{đm}}{P_{gió}}=\dfrac{2{,}0}{5{,}21}"),
     A(r"H\approx38{,}4\,\%"), A(r"T:$38{,}4\,\%\lt59{,}3\,\%$ : đúng với giới hạn Betz, tuabin thật chỉ đạt khoảng một nửa đến hai phần ba mức đó.")]),
  ("Công suất khi gió 9 m/s", [P(r"$9\ \text{m/s}$ nằm giữa $v_{kđ}$ và $v_{đm}$ : công suất tỉ lệ $v^3$, so với mức định mức :"),
     M(r"P_9=P_{đm}\left(\dfrac{9}{12}\right)^3=2{,}0\cdot0{,}421875"), A(r"P_9\approx0{,}844\ \text{MW}"),
     P(r"Tương tự $6\ \text{m/s}$ : $P_6=2{,}0\cdot\left(\dfrac{6}{12}\right)^3=0{,}25\ \text{MW}$.")]),
  ("Công suất khi gió 2 m/s và 15 m/s", [P(r"$2\ \text{m/s}\lt v_{kđ}=3\ \text{m/s}$ : tuabin chưa phát điện, $P_2=0$."),
     P(r"$12\le15\le25\ \text{m/s}$ : bộ điều khiển giữ công suất định mức, không dùng $v^3$ :"), A(r"P_{15}=P_{đm}=2{,}0\ \text{MW}")]),
  ("Điện năng cả ngày", [P(r"Cộng điện năng từng khoảng $A=\sum P_it_i$ :"), M(r"A=4\cdot0+8\cdot0{,}25+6\cdot0{,}844+4\cdot2{,}0+2\cdot2{,}0"),
     M(r"A=0+2+5{,}0625+8+4"), A(r"A\approx19{,}06\ \text{MWh}")]),
  ("Hệ số công suất", [M(r"\dfrac{A}{P_{đm}\cdot24\ \text{h}}=\dfrac{19{,}06}{2{,}0\cdot24}=\dfrac{19{,}06}{48}"), A(r"\text{hệ số}\approx39{,}7\,\%")]),
  ("Số tuabin", [P(r"Điện năng nhà máy than trong một ngày :"), M(r"A_{nm}=330\cdot24=7920\ \text{MWh}"),
     M(r"n=\dfrac{A_{nm}}{A}=\dfrac{7920}{19{,}06}\approx415{,}5"), A(r"T:Cần ít nhất $416$ tuabin (làm tròn lên : $415$ tuabin phát thiếu).")]),
  ("Kiểm tra", [P(r"Đơn vị : $\text{kg/m}^3\cdot\text{m}^2\cdot(\text{m/s})^3=\text{kg}\cdot\text{m}^2/\text{s}^3=\text{W}$ ✓."),
     P(r"Gió $9\ \text{m/s}$ so với $6\ \text{m/s}$ : $\left(\dfrac96\right)^3\approx3{,}4$ lần công suất, khớp $0{,}844:0{,}25$ ✓."),
     P(r"Hệ số công suất cỡ $25$–$45\,\%$ là mức thường gặp của điện gió ; vì vậy cần rất nhiều tuabin mới thay được một nhà máy than chạy liên tục ✓.")])],
  [r"a) $P_{gió}\approx5{,}21\ \text{MW}$ ; $H\approx38{,}4\,\%\lt59{,}3\,\%$", r"b) $A\approx19{,}06\ \text{MWh}$ ; hệ số công suất $\approx39{,}7\,\%$", r"c) ít nhất $416$ tuabin"],
  r"Nhận dạng: thấy <strong>tuabin gió, tốc độ khởi động, định mức, ngắt</strong> → xếp từng tốc độ gió vào vùng làm việc ; chỉ vùng giữa dùng $P\propto v^3$, rồi $A=\sum P_it_i$."),
 sol(R5, [
  ("Thể tích xăng mỗi ngày", [P(r"Công có ích ở bánh xe (như nhau cho hai xe) :"), M(r"A_{ích}=Fs=70\cdot40\,000=2{,}8\cdot10^6\ \text{J}"),
     M(r"Q=\dfrac{A_{ích}}{H_x}=\dfrac{2{,}8\cdot10^6}{0{,}15}\approx1{,}867\cdot10^7\ \text{J}"),
     M(r"m_x=\dfrac{Q}{q_x}=\dfrac{1{,}867\cdot10^7}{4{,}6\cdot10^7}\approx0{,}406\ \text{kg}"),
     M(r"V=\dfrac{m_x}{D_x}=\dfrac{0{,}406}{0{,}70}"), A(r"V\approx0{,}580\ \text{L}")]),
  ("CO₂ của xe xăng", [P(r"Hệ số tính theo kilôgam xăng :"), M(r"m_{CO_2}=k_xm_x=3{,}2\cdot0{,}406"), A(r"m_{CO_2}\approx1{,}30\ \text{kg}")]),
  ("Điện năng lấy từ ổ điện", [P(r"Chuỗi hai khâu : sạc rồi động cơ, hiệu suất nhân nhau :"), M(r"H_e=H_sH_{đc}=0{,}9\cdot0{,}8=0{,}72"),
     M(r"A=\dfrac{A_{ích}}{H_e}=\dfrac{2{,}8\cdot10^6}{0{,}72}\approx3{,}89\cdot10^6\ \text{J}"),
     M(r"A=\dfrac{3{,}89\cdot10^6}{3{,}6\cdot10^6}\ \text{kWh}"), A(r"A\approx1{,}08\ \text{kWh}")]),
  ("CO₂ ứng với điện của xe điện", [M(r"m_{CO_2}'=k_eA=0{,}65\cdot1{,}080"), A(r"m_{CO_2}'\approx0{,}702\ \text{kg}")]),
  ("Tiền tiết kiệm một năm", [M(r"\text{xăng}:\ 0{,}580\cdot24\,000\approx13\,913\ \text{đồng/ngày}"),
     M(r"\text{điện}:\ 1{,}080\cdot3000\approx3241\ \text{đồng/ngày}"),
     M(r"(13\,913-3241)\cdot365\approx3{,}90\cdot10^6\ \text{đồng}"), A(r"\text{tiết kiệm}\approx3{,}90\ \text{triệu đồng/năm}")]),
  ("Hiệu suất từ than tới bánh xe", [P(r"Bỏ qua đường dây : ba khâu nối tiếp nhà máy → sạc → động cơ :"),
     M(r"H_c=H_{nm}H_sH_{đc}=0{,}363\cdot0{,}72"), A(r"H_c\approx26{,}1\,\%"), P(r"Vẫn cao hơn $15\,\%$ của xe xăng.")]),
  ("CO₂ khi điện lấy từ than", [M(r"m_t=\dfrac{A_{ích}}{H_c\,q_t}=\dfrac{2{,}8\cdot10^6}{0{,}2614\cdot2{,}7\cdot10^7}\approx0{,}397\ \text{kg}"),
     M(r"m_{CO_2}''=k_tm_t=2{,}5\cdot0{,}397"), A(r"m_{CO_2}''\approx0{,}992\ \text{kg}"),
     A(r"T:$0{,}992\ \text{kg}\lt1{,}30\ \text{kg}$ : xe điện vẫn thải ít hơn, nhưng chỉ ít hơn khoảng $1{,}3$ lần thay vì khoảng $1{,}85$ lần ở câu b.")]),
  ("Kiểm tra", [P(r"Đơn vị : $\dfrac{\text{J}}{\text{J/kg}}=\text{kg}$ ; $\dfrac{\text{kg}}{\text{kg/L}}=\text{L}$ ✓."),
     P(r"Điện từ than tương đương $k_e=\dfrac{k_t}{H_{nm}q_t/3{,}6\cdot10^6}=\dfrac{2{,}5}{0{,}363\cdot7{,}5}\approx0{,}92\ \text{kg/kWh}$, lớn hơn $0{,}65$ của lưới (lưới còn thuỷ điện, điện gió, điện Mặt Trời) ✓."),
     P(r"Kết luận : xe điện “sạch” tới đâu phụ thuộc nguồn sinh ra điện ; tiền điện rẻ hơn tiền xăng khoảng $4{,}3$ lần.")])],
  [r"a) $V\approx0{,}580\ \text{L}$ ; $m_{CO_2}\approx1{,}30\ \text{kg}$", r"b) $A\approx1{,}08\ \text{kWh}$ ; $m_{CO_2}\approx0{,}702\ \text{kg}$ ; tiết kiệm khoảng $3{,}90$ triệu đồng/năm",
   r"c) $H_c\approx26{,}1\,\%$ ; $m_{CO_2}\approx0{,}992\ \text{kg}$, vẫn ít hơn xe xăng"],
  r"Nhận dạng: thấy <strong>so sánh hai phương án</strong> cùng một <strong>công có ích</strong> → tính $A_{ích}$ một lần, đi ngược từng chuỗi (chia tích hiệu suất) về nhiên liệu, rồi đổi ra lít, kWh, tiền, CO₂."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>tốc độ khởi động, định mức, ngắt</b> của tuabin → <b>xếp từng tốc độ gió vào vùng</b>, chỉ vùng giữa dùng $v^3$",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Công suất dòng gió ở 12 m/s", "Khi gió 12 m/s, công suất của dòng gió qua vòng quét là bao nhiêu MW?", PG4, "MW", 0.03,
       loi=r"Lấy $80\ \text{m}$ làm bán kính nên diện tích lớn gấp $4$ lần, hoặc quên hệ số $\tfrac12$ trong công thức đề cho."),
  buoc("Hiệu suất của tuabin ở 12 m/s", "Hiệu suất của tuabin khi gió 12 m/s là bao nhiêu phần trăm?", H4 * 100, "%", 0.4,
       loi=r"Chia ngược công suất dòng gió cho công suất điện nên ra hơn $100\,\%$ ; hoặc lấy luôn giới hạn Betz làm hiệu suất.",
       ke=[(r"$H=\dfrac{P_{đm}}{P_{gió}}$", True),
           (r"$H=\dfrac{P_{gió}}{P_{đm}}$", r"Tỉ số này lớn hơn $1$ : điện phát ra không thể nhiều hơn năng lượng gió mang tới."),
           (r"Lấy $H=59{,}3\,\%$ theo giới hạn Betz", r"Betz chỉ là mức tối đa lí thuyết ; hiệu suất thật phải tính từ số liệu của tuabin.")]),
  buoc("Công suất khi gió 9 m/s", "Khi gió 9 m/s, tuabin phát công suất bao nhiêu MW?", float(P4(9)), "MW", 0.006,
       loi=r"Dùng tỉ lệ bình phương như động năng, quên rằng lượng không khí qua vòng quét mỗi giây cũng tăng theo $v$.",
       ke=[(r"$P_9=P_{đm}\left(\dfrac{9}{12}\right)^3$", True),
           (r"$P_9=P_{đm}\left(\dfrac{9}{12}\right)^2$", r"Công suất gió tỉ lệ $v^3$, không phải $v^2$ : động năng mỗi kilôgam $\propto v^2$ nhân lượng khí mỗi giây $\propto v$."),
           (r"$P_9=\dfrac12D_{kk}S\cdot9^3$", r"Đó là công suất của dòng gió, chưa tính hiệu suất ; tuabin chỉ biến một phần thành điện.")]),
  buoc("Công suất khi gió 2 m/s và 15 m/s", "Khi gió 2 m/s và khi gió 15 m/s, tuabin phát công suất lần lượt bao nhiêu?",
       loi=r"Dùng $v^3$ cho cả hai tốc độ : dưới $3\ \text{m/s}$ tuabin chưa phát điện, từ $12\ \text{m/s}$ trở lên bộ điều khiển giữ công suất định mức.",
       lua_chon=[(r"$0$ và $2{,}0\ \text{MW}$", True),
                 (r"$P_{đm}\left(\dfrac{2}{12}\right)^3$ và $P_{đm}\left(\dfrac{15}{12}\right)^3$", r"Công thức $v^3$ chỉ đúng khi gió từ $3\ \text{m/s}$ tới dưới $12\ \text{m/s}$."),
                 (r"$0$ và $0$", r"Tuabin chỉ dừng khi gió mạnh hơn $25\ \text{m/s}$ ; gió $15\ \text{m/s}$ vẫn phát công suất định mức.")],
       ke=[(r"So từng tốc độ gió với $3$, $12$, $25\ \text{m/s}$ để biết nó ở vùng nào", True),
           (r"Dùng $P=P_{đm}\left(\dfrac{v}{12}\right)^3$ cho mọi tốc độ gió", r"Ngoài vùng $3$–$12\ \text{m/s}$ tuabin không làm việc theo $v^3$."),
           (r"Lấy công suất dòng gió $\dfrac12D_{kk}Sv^3$ làm công suất điện", r"Tuabin chỉ biến một phần năng lượng gió thành điện, và còn bị giới hạn ở mức định mức.")]),
  buoc("Điện năng cả ngày", "Điện năng tuabin phát trong ngày là bao nhiêu MWh?", float(A4), "MWh", 0.06,
       loi=r"Lấy tốc độ gió trung bình cả ngày rồi tính công suất một lần ; hoặc coi tuabin chạy định mức suốt $24$ h.",
       ke=[(r"$A=\sum P_it_i$ cho năm khoảng gió", True),
           (r"$A=P_{đm}\cdot24\ \text{h}$", r"Tuabin chỉ chạy định mức khi gió từ $12\ \text{m/s}$ trở lên ; phần lớn thời gian phát ít hơn."),
           (r"Tính gió trung bình cả ngày rồi $A=P(v_{tb})\cdot24\ \text{h}$", r"Công suất theo $v^3$ không tuyến tính : công suất ở gió trung bình khác trung bình các công suất.")]),
  buoc("Hệ số công suất", "Hệ số công suất của tuabin trong ngày đó là bao nhiêu phần trăm?", float(HSCS4) * 100, "%", 0.4,
       loi=r"Chia điện năng cho công suất dòng gió nhân $24$ h, hoặc chỉ chia cho $24$ h (ra công suất trung bình, chưa so với định mức).",
       ke=[(r"$\dfrac{A}{P_{đm}\cdot24\ \text{h}}$", True),
           (r"$\dfrac{A}{P_{gió}\cdot24\ \text{h}}$", r"Hệ số công suất so với chạy định mức, mẫu số là điện năng định mức $P_{đm}\cdot24\ \text{h}$."),
           (r"$\dfrac{A}{24\ \text{h}}$", r"Đó là công suất trung bình (theo MW), chưa chia cho công suất định mức nên chưa là tỉ số.")]),
  buoc("Số tuabin", "Cần ít nhất bao nhiêu tuabin?", N4, "tuabin", 0,
       loi=r"So công suất nhà máy với công suất định mức của một tuabin (coi tuabin chạy định mức cả ngày), hoặc làm tròn xuống nên phát thiếu.",
       ke=[(r"$n=\dfrac{A_{nm}}{A}$ rồi làm tròn lên", True),
           (r"$n=\dfrac{P_{nm}}{P_{đm}}$", r"Tuabin không chạy định mức suốt ngày ; phải so điện năng trong ngày, không so công suất."),
           (r"$n=\dfrac{A_{nm}}{A}$ rồi làm tròn xuống", r"Làm tròn xuống thì tổng điện năng còn thiếu so với nhà máy ; “ít nhất để đủ” phải làm tròn lên.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>so sánh hai phương án</b> cùng quãng đường → <b>tính công có ích một lần</b>, chia tích hiệu suất từng chuỗi",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Thể tích xăng mỗi ngày", "Xe xăng dùng bao nhiêu lít xăng mỗi ngày?", float(VX5), "L", 0.006,
       loi=r"Nhân công có ích với hiệu suất thay vì chia ; hoặc nhân khối lượng với khối lượng riêng thay vì chia khi đổi ra lít."),
  buoc("CO₂ của xe xăng", "Xe xăng thải ra bao nhiêu kilôgam CO₂ mỗi ngày?", float(CX5), "kg", 0.012,
       loi=r"Nhân hệ số với số lít xăng, trong khi đề cho hệ số theo mỗi kilôgam xăng.",
       ke=[(r"$m_{CO_2}=k_x\,m_x$ với $m_x$ theo kg", True),
           (r"$m_{CO_2}=k_x\,V$ với $V$ theo lít", r"Hệ số $3{,}2$ tính cho $1\ \text{kg}$ xăng ; một lít xăng nặng chưa tới $1\ \text{kg}$."),
           (r"$m_{CO_2}=\dfrac{m_x}{k_x}$", r"Mỗi kilôgam xăng thải ra $3{,}2\ \text{kg}$ CO₂ nên phải nhân, không chia.")]),
  buoc("Điện năng lấy từ ổ điện", "Xe điện lấy từ ổ điện bao nhiêu kWh mỗi ngày?", float(AE5), "kWh", 0.012,
       loi=r"Chỉ chia cho hiệu suất động cơ, quên khâu sạc ; hoặc lấy trung bình cộng hai hiệu suất.",
       ke=[(r"$A=\dfrac{A_{ích}}{H_sH_{đc}}$ rồi đổi ra kWh", True),
           (r"$A=\dfrac{A_{ích}}{H_{đc}}$", r"Quên khâu sạc : ổ điện phải cấp nhiều hơn phần đi vào acquy."),
           (r"$A=\dfrac{A_{ích}}{(H_s+H_{đc})/2}$", r"Hai khâu nối tiếp thì hiệu suất nhân nhau, không lấy trung bình.")]),
  buoc("CO₂ ứng với điện của xe điện", "Điện xe điện dùng mỗi ngày ứng với bao nhiêu kilôgam CO₂?", float(CE5), "kg", 0.006,
       loi=r"Nhân hệ số với công có ích ở bánh xe thay vì với điện lấy từ ổ ; hoặc nhân với điện năng tính theo MJ.",
       ke=[(r"$m_{CO_2}'=k_eA$ với $A$ theo kWh", True),
           (r"$m_{CO_2}'=k_eA_{ích}$ với $A_{ích}$ đổi ra kWh", r"Nhà máy phải làm ra cả phần hao phí ở sạc và động cơ ; tính theo điện lấy từ ổ."),
           (r"$m_{CO_2}'=k_eA$ với $A$ theo MJ", r"Hệ số cho theo kWh ; phải đổi điện năng ra kWh trước.")]),
  buoc("Tiền tiết kiệm một năm", "Một năm dùng xe điện tiết kiệm được bao nhiêu triệu đồng?", float(TK5) / 1e6, "triệu đồng", 0.02,
       loi=r"Quên nhân $365$ ngày, hoặc lấy tiền xăng cả năm mà không trừ tiền điện vẫn phải trả.",
       ke=[(r"(tiền xăng $-$ tiền điện mỗi ngày) $\times365$", True),
           (r"tiền xăng $-$ tiền điện mỗi ngày", r"Đó là số tiết kiệm một ngày ; đề hỏi một năm."),
           (r"tiền xăng mỗi ngày $\times365$", r"Dùng xe điện vẫn phải trả tiền điện ; tiết kiệm là phần chênh lệch.")]),
  buoc("Hiệu suất từ than tới bánh xe", "Hiệu suất của cả chuỗi từ than tới bánh xe là bao nhiêu phần trăm?", float(HC5) * 100, "%", 0.2,
       loi=r"Chỉ lấy hiệu suất nhà máy, quên hai khâu sạc và động cơ ; hoặc lấy trung bình các hiệu suất.",
       ke=[(r"$H_c=H_{nm}H_sH_{đc}$", True),
           (r"$H_c=H_{nm}$", r"Điện ra khỏi nhà máy còn qua sạc và động cơ mới thành công ở bánh xe."),
           (r"$H_c=\dfrac{H_{nm}+H_sH_{đc}}{2}$", r"Các khâu nối tiếp nên hiệu suất nhân nhau, không lấy trung bình.")]),
  buoc("CO₂ khi điện lấy từ than", "Khi đó mỗi ngày thải ra bao nhiêu kilôgam CO₂?", float(CT5), "kg", 0.012,
       loi=r"Vẫn dùng hệ số $0{,}65$ của lưới, hoặc tính khối lượng than từ công có ích mà không chia hiệu suất cả chuỗi.",
       ke=[(r"$m_t=\dfrac{A_{ích}}{H_c\,q_t}$ rồi $m_{CO_2}''=k_tm_t$", True),
           (r"$m_{CO_2}''=0{,}65\cdot A$", r"$0{,}65$ là hệ số trung bình của lưới nhiều nguồn ; ở đây toàn bộ điện từ than."),
           (r"$m_t=\dfrac{A_{ích}}{q_t}$ rồi $m_{CO_2}''=k_tm_t$", r"Bỏ qua mọi hao phí : than phải toả nhiều hơn công có ích, chia cho hiệu suất cả chuỗi.")]),
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
    # ── D4: khớp nguon.md / tinh.py ──
    assert round(S4) == 5027 and round(PG4, 2) == 5.21 and round(H4 * 100, 1) == 38.4 and H4 < 16 / 27
    assert [P4(v) for _, v in BANG4] == [0, F(1, 4), F(27, 32), 2, 2]
    assert A4 == F(305, 16) and round(float(A4), 2) == 19.06 and round(float(HSCS4) * 100, 1) == 39.7
    assert A_D1 == 7920 and abs(A_D1 / float(A4) - 415.48) < 0.01 and N4 == 416
    assert round(float(P4(9)), 3) == 0.844 and round(float(P4(9)) * 6, 4) == 5.0625
    # cách sai cho kết quả khác đáp án (ngoài sai số)
    assert abs(0.5 * 1.2 * math.pi * 80 ** 2 * 12 ** 3 / 1e6 - PG4) > 1 and abs(1.2 * S4 * 12 ** 3 / 1e6 - PG4) > 1    # bán kính ; quên ½
    assert PG4 / 2 * 100 > 100 and abs(59.3 - H4 * 100) > 1                                                     # bước 2
    assert abs(2 * 0.75 ** 2 - float(P4(9))) > 0.05 and abs(0.5 * 1.2 * S4 * 9 ** 3 / 1e6 - float(P4(9))) > 0.05  # bước 3
    assert abs(2 * (15 / 12) ** 3 - 2) > 0.5 and 2 * (2 / 12) ** 3 > 0                                          # bước 4
    vtb = F(sum(h * v for h, v in BANG4), 24)
    assert abs(48 - float(A4)) > 1 and abs(float(P4(vtb)) * 24 - float(A4)) > 1                                # bước 5
    assert abs(float(A4) / (PG4 * 24) * 100 - float(HSCS4) * 100) > 1 and abs(float(A4) / 24 - float(HSCS4) * 100) > 1  # bước 6
    assert 330 / 2 != N4 and math.floor(A_D1 / float(A4)) != N4                                                 # bước 7
    # ── D5 ──
    assert AICH5 == 2_800_000 and round(float(QTP5) / 1e7, 3) == 1.867 and round(float(MX5), 3) == 0.406
    assert round(float(VX5), 3) == 0.580 and round(float(TX5)) == 13913 and round(float(CX5), 2) == 1.30
    assert HE5 == F(18, 25) and round(float(AE5), 2) == 1.08 and round(float(AE5), 3) == 1.080
    assert round(float(TE5)) == 3241 and round(float(CE5), 3) == 0.702
    assert round(float(TK5) / 1e6, 2) == 3.90 and round(float(TX5 / TE5), 1) == 4.3 and round(float(CX5 / CE5), 2) == 1.85
    assert round(float(HC5) * 100, 1) == 26.1 and round(float(MT5), 3) == 0.397 and round(float(CT5), 3) == 0.992
    assert CT5 < CX5 and round(float(CX5 / CT5), 1) == 1.3 and round(float(KE_TD), 2) == 0.92
    # cách sai
    assert abs(float(MX5 * DX) - float(VX5)) > 0.006 and abs(float(AICH5 * HX / QX / DX) - float(VX5)) > 0.006   # bước 1
    assert abs(float(KX * VX5 - CX5)) > 0.012 and abs(float(MX5 / KX - CX5)) > 0.012                             # bước 2
    assert abs(float(AICH5 / HDC / KWH - AE5)) > 0.012 and abs(float(AICH5 / ((HS + HDC) / 2) / KWH - AE5)) > 0.012  # bước 3
    assert abs(float(KE * AICH5 / KWH - CE5)) > 0.006 and abs(float(KE * AE5 * KWH / 10 ** 6 - CE5)) > 0.006     # bước 4
    assert abs(float(TX5 - TE5) / 1e6 - float(TK5) / 1e6) > 0.02 and abs(float(TX5) * 365 / 1e6 - float(TK5) / 1e6) > 0.02  # bước 5
    assert abs(float(HNM) - float(HC5)) > 0.002 and abs(float((HNM + HE5) / 2) - float(HC5)) > 0.002            # bước 6
    assert abs(float(KE * AE5) - float(CT5)) > 0.012 and abs(float(KT * AICH5 / QT) - float(CT5)) > 0.012        # bước 7
    # bảng phân tích: cột 1 trích nguyên văn đề ; mỗi dạng có ⚠
    for n, rows in enumerate(_RAW_ANALYSIS):
        for r in rows:
            assert r[0].strip('"') in _RAW_DANG[n]["problem_html"], (n, r[0])
        assert any("⚠" in r[2] for r in rows), n
    # không lộ đáp số trong đề, hình, bảng phân tích, câu hỏi, lựa chọn, lỗi hay gặp
    lo = {0: ["5027", "5 027", "5,21", "38,4", "0,844", "0,84", "0,25", "19,06", "19,1", "39,7", "416", "415", "5,06"],
          1: ["0,58", "0,406", "1,30", "1,29", "1,867", "1,08", "0,702", "3,90", "3,89", "13 9", "13\\,9", "3241", "26,1", "0,397", "0,99", "0,92", "1,85"]}
    for n in range(2):
        figs = re.sub(r"<[^>]+>", " ", BUILD[n](0) + BUILD[n](2))
        blob = DANG[n]["problem_html"] + figs + str(ANALYSIS[n]) + STEPS[n]["nhan_dang"]
        for s in STEPS[n]["buoc"]:
            blob += s.get("tieu_de", "") + s.get("hoi", "") + s.get("loi_hay_gap", "")
            for c in s.get("chon_buoc_ke", []) + s.get("lua_chon", []):
                blob += c["text"] + c.get("vi_sao", "")
        for x in lo[n]:
            assert x not in blob, (n, x)
    for n, s in enumerate(STEPS):
        assert s["cap_do"] in (3, 4) and len(s["buoc"]) == SOLS[n].count('class="bt-step"'), n
    print("btm163_d456: kiểm số liệu đạt")


if __name__ == "__main__":
    kiem_so()
