"""Bài tập mẫu CĐ07 "Thấu kính mỏng và kính lúp" (lesson 156) — Dạng 4–7 (phần khó). Module được build-hinh-156.py import.
Dàn ý + số liệu đã tính: content/hsg9/cd07-thau-kinh-kinh-lup/nguon.md mục "Bài tập mẫu" (D4–D7 dùng nguyên số, tinh.py).
Quy ước: d > 0 vật thật; d' > 0 ảnh thật, d' < 0 ảnh ảo; f > 0 hội tụ, f < 0 phân kì; 1/f = 1/d + 1/d'.
Dạng sau dùng lại cách làm dạng trước:
  D4 dịch chuyển vật–ảnh (công thức D2 + phương trình bậc hai của D3, rồi Δ ≥ 0 ⇒ L ≥ 4f)
  D5 đo tiêu cự Bessel / 2f–2f (phương trình d² − Ld + Lf = 0 của D4, hai nghiệm cách nhau ℓ)
  D6 kính lúp (công thức với ảnh ảo d' < 0 của D2: ảnh tại C_c ⇒ d' = −OC_c)
  D7 hệ hai thấu kính (ảnh qua TK1 là vật của TK2; ý b ⭐⭐⭐ vật ảo khi ghép sát).
Quyết định đã chốt: BỎ ý D6b (người cận dùng kính lúp); giữ D7b, đánh dấu ⭐⭐⭐ mở rộng chuyên.
Xuất DANG, BUILD, ANALYSIS, SOLS, STEPS (4 phần tử mỗi list) và kiem_so()."""
import math, os, re, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *  # noqa: F401,F403  (fig, seg, lbl, dot, poly, chevron, arrow, sol, M, P, A, buoc …)

T_DAC = "Đặc điểm thấu kính hội tụ, phân kì và tiêu cự"
T_CT = "Công thức thấu kính và số phóng đại"
NOTE = "Chiều cao vật và ảnh phóng to theo phương đứng cho dễ nhìn."
GREY = "#94a3b8"


def anh(f, d):
    """d' theo 1/f = 1/d + 1/d' (Fraction); None nếu ảnh ở vô cực."""
    f, d = F(f), F(d)
    inv = 1 / f - 1 / d
    return None if inv == 0 else 1 / inv


def kabs(d, dp):
    return abs(F(dp)) / abs(F(d))


# ═════════════ SỐ LIỆU (mọi đáp số tính ở đây, kiem_so() kiểm lại) ═════════════
# D4 — TK HT f = 15 cố định, vật cao 2 cm
F4, H4 = F(15), F(2)
D4_1, D4_2, D4_3 = F(45), F(30), F(20)
D4_1P, D4_2P, D4_3P = anh(F4, D4_1), anh(F4, D4_2), anh(F4, D4_3)          # 22,5 ; 30 ; 60
L4 = [D4_1 + D4_1P, D4_2 + D4_2P, D4_3 + D4_3P]                             # 67,5 ; 60 ; 80
DICH4_1, DICH4_2 = D4_2P - D4_1P, D4_3P - D4_2P                             # 7,5 ; 30
LMIN4 = 4 * F4                                                               # 60
# D4c — TK khác: vật lại gần 5 cm, ảnh dịch 10 cm, cao gấp đôi
X4C = F(10)                     # d1 − f, từ (d1 − f) = 2(d1 − 5 − f)
F4C = F(10)                     # f²/10 = 10
D4C1, D4C2 = F4C + X4C, F4C + X4C - 5                                        # 20 ; 15
D4C1P, D4C2P = anh(F4C, D4C1), anh(F4C, D4C2)                                # 20 ; 30
# D5 — Bessel L = 125, ℓ = 75, vật 2 cm
L5, l5, H5 = F(125), F(75), F(2)
F5 = (L5**2 - l5**2) / (4 * L5)                                              # 20
D5_1, D5_2 = (L5 - l5) / 2, (L5 + l5) / 2                                    # 25 ; 100
H5_1, H5_2 = H5 * (L5 - D5_1) / D5_1, H5 * (L5 - D5_2) / D5_2                # 8 ; 0,5
LMIN5 = 4 * F5                                                               # 80
LS5 = [F("79.5"), F("80.6"), F("80.2")]
LTB5 = sum(LS5) / 3                                                          # 80,1
DL5 = sum(abs(x - LTB5) for x in LS5) / 3                                    # 0,4
FTB5, DF5 = LTB5 / 4, DL5 / 4                                                # 20,025 ; 0,1
F5_L = ((L5 + 1)**2 - l5**2) / (4 * (L5 + 1))                                # ≈ 20,339
F5_l = (L5**2 - (l5 + 1)**2) / (4 * L5)                                      # ≈ 19,698
DFL5, DFl5 = F5_L - F5, F5 - F5_l                                            # ≈ 0,34 ; ≈ 0,30
# D6 — kính lúp 5×, mắt tốt, kính sát mắt
G6, CC6, H6 = F(5), F(25), F(4, 10)                                          # h = 0,4 mm
F6 = 25 / G6                                                                 # 5 cm
D6_CC = 1 / (1 / F6 + 1 / CC6)                                               # 25/6 ≈ 4,17 (d' = −25)
K6_CC = CC6 / D6_CC                                                          # 6
D6_V = F6                                                                    # ngắm chừng vô cực: d = f
XD6_MM = (D6_V - D6_CC) * 10                                                 # 25/3 ≈ 8,33 mm
H6P = K6_CC * H6                                                             # 2,4 mm
# D7 — TK1 HT f1 = 20, vật 2 cm, d1 = 30
F7_1, H7, D7_1 = F(20), F(2), F(30)
D7_1P = anh(F7_1, D7_1)                                                      # 60
H7_1 = H7 * kabs(D7_1, D7_1P)                                                # 4
A7A, F7_2A = F(80), F(-20)
D7_2A = A7A - D7_1P                                                          # 20
D7_2AP = anh(F7_2A, D7_2A)                                                   # −10
H7_2A = H7_1 * kabs(D7_2A, D7_2AP)                                           # 2
INV7B = 1 / F7_1 + 1 / F7_2A                                                 # 0
D7_2B = 0 - D7_1P                                                            # −60 (vật ảo)
D7_2BP = anh(F7_2A, D7_2B)                                                   # −30 (trùng vật)
F7_2C = F(20)
D7_2C = 2 * F7_2C                                                            # 40 (|k2| = 1)
A7C = D7_1P + D7_2C                                                          # 100
D7_2CP = anh(F7_2C, D7_2C)                                                   # 40


# ═════════════ HÌNH: tiện ích ═════════════
def rich(s, size=14):
    """Nhãn SVG có chỉ số dưới: 'TK_{1}' → tspan dy."""
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
    k0 = max(0.001, k0)
    return (f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{k0:.4f};{k1:.4f}" calcMode="discrete" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def timed(t, s, x, y, c="currentColor", size=14, anchor="start", weight="700", k1=None, dur=None):
    a = show_between(t, k1, dur) if k1 is not None else show_at(t * dur, dur)
    return txt(x, y, s, c, size, anchor, weight, 'opacity="0"').replace("</text>", a + "</text>", 1)

def grp(t, body, dur, k1=None):
    """Nhóm hiện từ phân số t (tới k1 nếu có) của mô phỏng dài dur."""
    a = show_between(t, k1, dur) if k1 is not None else show_at(t * dur, dur)
    return f'<g opacity="0">{body}{a}</g>'

def rect(x, y, w, h, c="currentColor", sw=2, fill="none", op=1, rx=0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" '
            f'stroke="{c}" stroke-width="{sw}"/>')

def chev_d(x, y, dx, dy, L=9, ang=30):
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    t = math.radians(ang)
    pts = []
    for s in (1, -1):
        bx = ux * math.cos(t) - uy * math.sin(s * t)
        by = ux * math.sin(s * t) + uy * math.cos(t)
        pts.append((x - L * bx, y - L * by))
    (ax, ay), (bx2, by2) = pts
    return f"M{ax:.1f},{ay:.1f} L{x:.1f},{y:.1f} L{bx2:.1f},{by2:.1f}"

def ray(x1, y1, x2, y2, c=ORG, w=2, dash=""):
    """Tia sáng: nét liền, mũi tên chữ V ở giữa tia (đường kéo dài: dash, không mũi tên)."""
    out = seg(x1, y1, x2, y2, c, w, dash)
    if not dash:
        out += chevron((x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1, c, w, 9)
    return out

def lens_ht(x, y, half, c="currentColor", w=2.4):
    return seg(x, y - half, x, y + half, c, w) + chevron(x, y - half, 0, -1, c, w, 10) + chevron(x, y + half, 0, 1, c, w, 10)

def lens_pk(x, y, half, c="currentColor", w=2.4):
    return seg(x, y - half, x, y + half, c, w) + chevron(x, y - half, 0, 1, c, w, 10) + chevron(x, y + half, 0, -1, c, w, 10)

def thing(x, y, hpx, c="currentColor", w=2.6, dash=""):
    """Vật/ảnh: mũi tên đứng từ trục (y) lên (hpx > 0) hoặc xuống (hpx < 0)."""
    tip = y - hpx
    return seg(x, y, x, tip, c, w, dash) + chevron(x, tip, 0, -hpx, c, w, 8)

def axis(x0, x1, y):
    return seg(x0, y, x1, y, "currentColor", 1.4, "", .7)

def tick(x, y, s, below=True, c="currentColor"):
    return dot(x, y, 3.2, c) + txt(x, y + 20 if below else y - 9, s, c, 14, "middle", "700")

def dim2(x1, x2, y, s, c=ORG, ly=None):
    """Kích thước ngang hai đầu chữ V + nhãn ở giữa."""
    out = seg(x1, y, x2, y, c, 1.6) + chevron(x1, y, -1, 0, c, 1.6, 8) + chevron(x2, y, 1, 0, c, 1.6, 8)
    out += seg(x1, y - 5, x1, y + 5, c, 1.2) + seg(x2, y - 5, x2, y + 5, c, 1.2)
    return out + txt((x1 + x2) / 2, ly if ly is not None else y - 7, s, c, 14, "middle", "700")

def anim_d(vals, kts, dur):
    return (f'<animate attributeName="d" values="{";".join(vals)}" keyTimes="{";".join(f"{k:.4f}" for k in kts)}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def apath(vals, kts, dur, c, w=2.2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{vals[0]}" fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" stroke-linejoin="miter">'
            f'{anim_d(vals, kts, dur)}</path>')

def samples(sched, n=12):
    """sched = [(phân số thời gian, giá trị)]: nội suy tuyến tính, lấy n mẫu mỗi đoạn có đổi giá trị."""
    out = [sched[0]]
    for (k0, v0), (k1, v1) in zip(sched, sched[1:]):
        m = n if v0 != v1 else 1
        for i in range(1, m + 1):
            out.append((k0 + (k1 - k0) * i / m, v0 + (v1 - v0) * i / m))
    return out

def P_(x, y):
    return f"{x:.1f},{y:.1f}"


# ═════════════ Dạng 4 · dịch chuyển vật–ảnh ═════════════
S4, V4, X4, Y4 = 2.6, 8, 140, 112

def d4(kk):
    b = ""
    f = float(F4)
    b += axis(10, 410, Y4) + lens_ht(X4, Y4, 72 if kk == 0 else 62) + tick(X4 - S4 * f, Y4, "F") + tick(X4 + S4 * f, Y4, "F'")
    b += txt(X4 + 7, Y4 + 18, "O", "currentColor", 14, "start", "700")
    if kk == 0:
        TT = 7.0
        sched = [(0, 45.0), (.12, 45.0), (.42, 30.0), (.55, 30.0), (.85, 20.0), (1, 20.0)]
        sm = samples(sched, 10)
        vals = ";".join(f"{-S4 * d:.1f} 0" for _, d in sm)
        kts = ";".join(f"{k:.4f}" for k, _ in sm)
        b += (f'<g transform="translate({-S4 * 45:.1f} 0)">{thing(X4, Y4, 16)}<animateTransform attributeName="transform" '
              f'type="translate" values="{vals}" keyTimes="{kts}" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += txt(16, 22, "Thấu kính hội tụ cố định, vật dịch lại gần", "currentColor", 14)
        b += timed(0, "d = 45 cm", 16, 200, "currentColor", 14, "start", "700", .12, TT)
        b += timed(.12, "vật lại gần 15 cm …", 16, 200, ORG, 14, "start", "700", .42, TT)
        b += timed(.42, "d = 30 cm", 16, 200, "currentColor", 14, "start", "700", .55, TT)
        b += timed(.55, "lại gần thêm 10 cm …", 16, 200, ORG, 14, "start", "700", .85, TT)
        b += timed(.85, "d = 20 cm", 16, 200, "currentColor", 14, "start", "700", None, TT)
        b += txt(404, 60, "ảnh ở đâu?", RED, 14, "end", "700") + txt(404, 78, "dịch theo chiều nào?", RED, 14, "end", "700")
        return fig("c07-4-0", "0 0 420 212", "Vật sáng dịch lại gần thấu kính hội tụ cố định qua ba vị trí cách thấu kính 45 cm, 30 cm và 20 cm",
                   b, "Mô phỏng: chỉ vật di chuyển; ảnh để em tự dựng và tính. " + NOTE)
    # hình dữ kiện
    xs = [X4 - S4 * 45, X4 - S4 * 30, X4 - S4 * 20]
    b += thing(xs[0], Y4, 16)
    b += thing(xs[1], Y4, 16, GREY, 2, "4 3") + thing(xs[2], Y4, 16, GREY, 2, "4 3")
    for k, x in enumerate(xs):
        b += txt(x, Y4 - 24, str(k + 1), "currentColor" if k == 0 else GREY, 14, "middle", "700")
    b += dim2(xs[0], X4, Y4 + 34, "d_{1} = 45 cm", ORG, Y4 + 52)
    b += dim2(xs[0], xs[1], Y4 - 50, "15", BLUE) + dim2(xs[1], xs[2], Y4 - 80, "10", BLUE)
    b += txt(X4 + S4 * 15 + 4, Y4 + 40, "f = 15 cm", "currentColor", 14, "start", "600")
    b += txt(250, Y4 - 40, "ảnh: ở đâu?", RED, 14, "start", "700") + txt(250, Y4 - 22, "cao bao nhiêu?", RED, 14, "start", "700")
    b += txt(16, 196, "AB = 2 cm, thấu kính đứng yên.", "currentColor", 14, "start", "600")
    b += txt(16, 216, "c) thấu kính khác: vật lại gần 5 cm,", "currentColor", 14, "start", "600")
    b += txt(16, 234, "ảnh thật dịch 10 cm, cao gấp đôi: f = ?", RED, 14, "start", "700")
    return fig("c07-4-2", "0 0 420 244", "Ba vị trí của vật trước thấu kính hội tụ tiêu cự 15 cm: cách 45 cm, lại gần 15 cm, rồi lại gần thêm 10 cm",
               b, "Dữ kiện: số trên mũi tên xanh là đoạn vật dịch lại gần (cm). Không vẽ ảnh. " + NOTE)


# ═════════════ Dạng 5 · Bessel ═════════════
S5, V5, XA5, Y5 = 2.8, 7, 30, 118

def d5(kk):
    b = ""
    xs = XA5 + S5 * 125
    b += axis(14, 410, Y5) + thing(XA5, Y5, V5 * 2) + txt(XA5, Y5 + 22, "A", "currentColor", 14, "middle")
    b += rect(xs - 3, Y5 - 78, 6, 156, "currentColor", 1.8, GREY, .35)
    b += txt(xs - 8, Y5 - 84, "màn", "currentColor", 14, "end", "700")
    if kk == 0:
        TT = 7.0
        sm = samples([(0, 8.0), (1, 117.0)], 2)
        vals = ";".join(f"{S5 * p:.1f} 0" for _, p in sm)
        kts = ";".join(f"{k:.4f}" for k, _ in sm)
        b += (f'<g transform="translate({S5 * 8:.1f} 0)">{lens_ht(XA5, Y5, 60)}<animateTransform attributeName="transform" '
              f'type="translate" values="{vals}" keyTimes="{kts}" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += txt(16, 22, "Thấu kính trượt từ gần vật tới gần màn", "currentColor", 14)
        b += txt(16, 42, "có hai chỗ ảnh rõ, cách nhau ℓ = 75 cm: f = ?", RED, 14, "start", "700")
        b += dim2(XA5, xs, Y5 + 92, "L = 125 cm", ORG, Y5 + 112)
        return fig("c07-5-0", "0 0 420 238", "Vật và màn cố định cách nhau 125 cm; thấu kính hội tụ trượt đều từ gần vật tới gần màn",
                   b, "Mô phỏng: chỉ thấu kính di chuyển, không vẽ ảnh và không dừng ở vị trí cho ảnh rõ. " + NOTE)
    # hình dữ kiện (vị trí thấu kính vẽ phỏng, không đúng tỉ lệ)
    x1, x2 = 112, 292
    b += lens_ht(x1, Y5, 56, GREY, 2) + lens_ht(x2, Y5, 56, GREY, 2)
    b += txt(x1, Y5 + 76, "vị trí 1", GREY, 14, "middle", "600") + txt(x2, Y5 + 76, "vị trí 2", GREY, 14, "middle", "600")
    b += dim2(x1, x2, Y5 - 66, "ℓ = 75 cm", BLUE)
    b += dim2(XA5, xs, Y5 + 96, "L = 125 cm", ORG, Y5 + 116)
    b += txt(XA5 + 8, Y5 - 22, "h = 2 cm", "currentColor", 14, "start", "600")
    b += txt(16, 22, "Vật, màn cố định; tìm f = ?", RED, 14, "start", "700")
    return fig("c07-5-2", "0 0 420 240", "Vật và màn cách nhau 125 cm; hai vị trí thấu kính cho ảnh rõ cách nhau 75 cm",
               b, "Dữ kiện: hai vị trí thấu kính vẽ phỏng, không đúng tỉ lệ. Không vẽ ảnh.")


# ═════════════ Dạng 6 · kính lúp ═════════════
S6, X6, Y6, HO6 = 12, 348, 142, 7
D6_END = 7.0          # vật dừng NGOÀI khoảng đáp án 25/6–5 cm

def eye(x, y):
    return (f'<path d="M{x},{y} Q{x + 18},{y - 20} {x + 40},{y - 6} L{x + 40},{y + 6} Q{x + 18},{y + 20} {x},{y} Z" fill="none" '
            f'stroke="currentColor" stroke-width="2"/>' + f'<circle cx="{x + 12}" cy="{y}" r="5" fill="currentColor"/>')

def d6(kk):
    b = ""
    b += axis(10, 410, Y6) + lens_ht(X6, Y6, 64) + eye(X6 + 14, Y6)
    xcc = X6 - S6 * 25
    b += tick(xcc, Y6, "C_{c}") + dim2(xcc, X6, Y6 + 44, "OC_{c} = 25 cm", ORG, Y6 + 62)
    if kk == 0:
        TT = 6.0
        sm = samples([(0, 1.5), (1, D6_END)], 2)
        vals = ";".join(f"{-S6 * d:.1f} 0" for _, d in sm)
        kts = ";".join(f"{k:.4f}" for k, _ in sm)
        b += (f'<g transform="translate({-S6 * 1.5:.1f} 0)">{thing(X6, Y6, HO6 + 3)}<animateTransform attributeName="transform" '
              f'type="translate" values="{vals}" keyTimes="{kts}" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += txt(16, 22, "Kính lúp sát mắt, vật dịch dần ra xa kính", "currentColor", 14)
        b += txt(16, 46, "đặt vật ở khoảng nào thì mắt nhìn rõ?", RED, 14, "start", "700")
        return fig("c07-6-0", "0 0 420 222", "Vật nhỏ dịch đều ra xa kính lúp đặt sát mắt; mắt tốt có điểm cực cận cách mắt 25 cm",
                   b, "Mô phỏng: chỉ vật di chuyển; không vẽ ảnh, không đánh dấu khoảng đặt vật. " + NOTE)
    b += thing(X6 - S6 * 3, Y6, HO6 + 3) + txt(X6 - S6 * 3, Y6 - 18, "vật", "currentColor", 14, "middle", "600")
    b += dim2(X6 - S6 * 3, X6, Y6 + 16, "", BLUE) + txt(X6 - S6 * 1.5, Y6 + 34, "d = ?", RED, 14, "middle", "700")
    b += txt(16, 64, "C_{v} ở vô cực (mắt tốt)", "currentColor", 14, "start", "600")
    b += txt(X6 + 4, Y6 - 74, "kính 5×", "currentColor", 14, "end", "700")
    b += txt(16, 22, "Kính đặt sát mắt; ảnh phải nằm từ C_{c} tới C_{v}", "currentColor", 14)
    return fig("c07-6-2", "0 0 420 222", "Mắt tốt đặt sát kính lúp 5×; điểm cực cận cách mắt 25 cm, điểm cực viễn ở vô cực; vật đặt ở đâu chưa biết",
               b, "Dữ kiện: vị trí vật vẽ phỏng, chưa phải chỗ đặt đúng; không vẽ ảnh, không vẽ tiêu điểm.")


# ═════════════ Dạng 7 · hệ hai thấu kính ═════════════
S7, V7, X7_1, Y7 = 3, 8, 120, 100
X7_2 = X7_1 + S7 * 80

def cx(x):
    return X7_1 + S7 * x

def cy(y):
    return Y7 - V7 * y

def d7(kk):
    b = ""
    b += axis(10, 412, Y7) + lens_ht(X7_1, Y7, 56) + lens_pk(X7_2, Y7, 56)
    b += txt(X7_1, Y7 - 72, "TK_{1}", "currentColor", 14, "middle") + txt(X7_2, Y7 - 72, "TK_{2}", "currentColor", 14, "middle")
    b += thing(cx(-30), Y7, V7 * 2) + txt(cx(-30), Y7 + 22, "A", "currentColor", 14, "middle") + txt(cx(-30) - 8, cy(2) + 2, "B", "currentColor", 14, "end")
    if kk == 0:
        TT = 7.0
        B, I1, O1 = (cx(-30), cy(2)), (cx(0), cy(2)), (cx(0), cy(0))
        b += grp(.05, ray(*B, *I1, ORG, 1.8), TT) + grp(.20, ray(*B, *O1, BLUE, 1.8), TT)
        b += timed(.35, "a) ảnh qua TK_{1} ở đâu? Nó là vật của TK_{2}", 16, 200, "currentColor", 14, "start", "600", .6, TT)
        sm = samples([(0, 0.0), (.6, 0.0), (1, -80.0)], 2)
        vals = ";".join(f"{S7 * x:.1f} 0" for _, x in sm)
        kts = ";".join(f"{k:.4f}" for k, _ in sm)
        lb2 = txt(X7_2, Y7 - 72, "TK_{2}", "currentColor", 14, "middle")
        b = b.replace(lens_pk(X7_2, Y7, 56), "").replace(lb2, "")
        b += (f'<g>{lens_pk(X7_2, Y7, 56)}{txt(X7_2 + 14, Y7 - 72, "TK_{2}", "currentColor", 14, "start")}<animateTransform attributeName="transform" type="translate" values="{vals}" '
              f'keyTimes="{kts}" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += timed(.6, "b) ⭐⭐⭐ đẩy TK_{2} lại sát TK_{1}", 16, 200, BLUE, 14, "start", "700", None, TT)
        return fig("c07-7-0", "0 0 420 214", "Vật trước thấu kính hội tụ, hai tia tới; thấu kính phân kì đặt sau rồi được đẩy lại sát thấu kính hội tụ",
                   b, "Mô phỏng: chỉ vẽ tia tới và vị trí các thấu kính; ảnh trung gian và ảnh cuối để em tự tìm. " + NOTE)
    b += dim2(cx(-30), X7_1, Y7 + 48, "d_{1} = 30 cm", ORG, Y7 + 66)
    b += dim2(X7_1, X7_2, Y7 + 92, "a = 80 cm", BLUE, Y7 + 110)
    b += txt(X7_1 + 8, Y7 + 26, "f_{1} = 20 cm", "currentColor", 14, "start", "600")
    b += txt(X7_2 - 8, Y7 + 26, "phân kì, |f_{2}| = 20 cm", "currentColor", 14, "end", "600")
    b += txt(cx(-30) + 8, cy(2) - 6, "2 cm", "currentColor", 14, "start", "600")
    b += txt(16, 22, "A_{2}'B_{2}' = ?", RED, 14, "start", "700")
    b += txt(16, 228, "b) ⭐⭐⭐ ghép sát: ảnh cuối ở đâu?", "currentColor", 14, "start", "600")
    b += txt(16, 248, "c) TK_{2} hội tụ, tiêu cự 20 cm: a = ?", "currentColor", 14, "start", "600")
    return fig("c07-7-2", "0 0 420 258", "Vật cách thấu kính hội tụ 30 cm; thấu kính phân kì đặt sau, cách thấu kính hội tụ 80 cm",
               b, "Dữ kiện: hai thấu kính đồng trục. Không vẽ ảnh. " + NOTE)


BUILD = [d4, d5, d6, d7]

# ═════════════ ĐỀ ═════════════
DANG = [
dict(label="Dạng 4 · Nâng cao · Dịch chuyển vật–ảnh: ảnh dịch theo chiều nào, khoảng cách vật–ảnh nhỏ nhất 4f",
     topic=T_CT,
     problem_html=r"""<p>Một thấu kính hội tụ có tiêu cự $f=15\ \text{cm}$ được giữ cố định. Vật sáng $AB$ cao $2\ \text{cm}$ đặt vuông góc với trục chính, $A$ nằm trên trục chính và cách thấu kính $45\ \text{cm}$.</p><ol type="a"><li>Xác định vị trí, chiều cao của ảnh và khoảng cách vật–ảnh. Dịch vật lại gần thấu kính $15\ \text{cm}$: ảnh dịch theo chiều nào, một đoạn bao nhiêu?</li><li>Dịch vật lại gần thấu kính thêm $10\ \text{cm}$ nữa. Ảnh dịch thêm bao nhiêu? Nhận xét khoảng cách vật–ảnh qua ba vị trí, rồi chứng minh: khoảng cách giữa vật thật và ảnh thật của thấu kính hội tụ không nhỏ hơn $4f$. Tìm khoảng cách nhỏ nhất đó với thấu kính này.</li><li>Một thấu kính hội tụ khác chưa biết tiêu cự. Vật thật đặt trước thấu kính cho ảnh thật. Dịch vật lại gần thấu kính $5\ \text{cm}$ thì ảnh vẫn là ảnh thật, dịch đi $10\ \text{cm}$ và cao gấp đôi ảnh cũ. Tìm tiêu cự của thấu kính và vị trí ban đầu của vật.</li></ol>"""),
dict(label="Dạng 5 · Nâng cao · Đo tiêu cự thấu kính hội tụ: cách Bessel và cách 2f–2f",
     topic=T_DAC,
     problem_html=r"""<p>Vật sáng $AB$ cao $2\ \text{cm}$ và màn ảnh đặt cố định, cách nhau $125\ \text{cm}$. Dịch một thấu kính hội tụ trong khoảng giữa vật và màn (trục chính vuông góc với màn và đi qua $A$), thấy có hai vị trí của thấu kính cách nhau $75\ \text{cm}$ đều cho ảnh rõ trên màn.</p><ol type="a"><li>Tính tiêu cự của thấu kính. Ở mỗi vị trí, ảnh cao bao nhiêu? Chứng tỏ tích hai chiều cao ảnh bằng bình phương chiều cao vật.</li><li>Đưa màn lại gần vật để khoảng cách vật–màn còn $70\ \text{cm}$. Còn vị trí nào của thấu kính cho ảnh rõ trên màn không? Khoảng cách vật–màn nhỏ nhất còn có ảnh rõ là bao nhiêu?</li><li>Một nhóm đo tiêu cự của chính thấu kính này bằng cách 2f–2f: dịch thấu kính và màn tới khi khoảng cách vật–màn nhỏ nhất mà vẫn có ảnh rõ, đo ba lần được $79{,}5\ \text{cm}$; $80{,}6\ \text{cm}$; $80{,}2\ \text{cm}$. Viết kết quả đo tiêu cự dạng $f=\bar f\pm\Delta f$.</li><li>Ở cách đo của câu a, nếu đo khoảng cách vật–màn lệch thêm $1\ \text{cm}$ (thành $126\ \text{cm}$) thì tiêu cự tính ra đổi bao nhiêu? Nếu đo khoảng cách giữa hai vị trí lệch thêm $1\ \text{cm}$ (thành $76\ \text{cm}$)? Đại lượng nào cần đo cẩn thận hơn?</li></ol>"""),
dict(label="Dạng 6 · Nâng cao · Kính lúp: ngắm chừng ở cực cận, ở vô cực và khoảng đặt vật",
     topic=T_CT,
     problem_html=r"""<p>Một kính lúp có ghi $5\times$ trên vành. Một người mắt tốt (điểm cực cận $C_c$ cách mắt $25\ \text{cm}$, điểm cực viễn $C_v$ ở vô cực) đặt kính sát mắt để quan sát một vật nhỏ đặt vuông góc với trục chính.</p><ol type="a"><li>Tính tiêu cự của kính lúp.</li><li>Muốn ngắm chừng ở điểm cực cận (ảnh ảo hiện ra đúng tại $C_c$), phải đặt vật cách kính bao nhiêu? Khi đó ảnh cao gấp mấy lần vật? So sánh với số bội giác ghi trên kính.</li><li>Muốn ngắm chừng ở vô cực (mắt nhìn không phải điều tiết), phải đặt vật ở đâu?</li><li>Vật phải đặt trong khoảng nào trước kính thì mắt nhìn rõ ảnh? Khoảng xê dịch đó dài bao nhiêu milimét? Trên vật có một vết xước dài $0{,}4\ \text{mm}$; ngắm chừng ở $C_c$ thì ảnh của vết xước dài bao nhiêu?</li></ol>"""),
dict(label="Dạng 7 · Vận dụng cao · Hệ hai thấu kính đồng trục: ảnh qua thấu kính 1 là vật của thấu kính 2",
     topic=T_CT,
     problem_html=r"""<p>Thấu kính hội tụ $TK_1$ có tiêu cự $f_1=20\ \text{cm}$. Vật sáng $AB$ cao $2\ \text{cm}$ đặt vuông góc với trục chính, cách $TK_1$ một khoảng $30\ \text{cm}$. Phía sau $TK_1$ đặt thấu kính $TK_2$ đồng trục.</p><ol type="a"><li>$TK_2$ là thấu kính phân kì có tiêu cự $20\ \text{cm}$, đặt cách $TK_1$ một khoảng $80\ \text{cm}$. Xác định vị trí, tính chất, chiều và chiều cao của ảnh cuối cùng qua hệ.</li><li>⭐⭐⭐ <em>Mở rộng chuyên.</em> Đẩy $TK_2$ lại sát $TK_1$ (ghép sát). Hệ tương đương với dụng cụ quang học nào? Ảnh cuối ở đâu? Kiểm lại bằng cách coi ảnh qua $TK_1$ là vật của $TK_2$.</li><li>Thay $TK_2$ bằng thấu kính hội tụ có tiêu cự $20\ \text{cm}$, đặt sau ảnh trung gian $A_1'B_1'$. Phải đặt $TK_2$ cách $TK_1$ bao nhiêu để ảnh cuối là ảnh thật, cao gấp đôi vật? Ảnh cuối cùng chiều hay ngược chiều vật?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 1 nguyên văn đề ; cột 2 dữ liệu ; cột 3 kiến thức) ═════════════
ANALYSIS = [
 # Dạng 4
 [(r'''"Một thấu kính hội tụ có tiêu cự $f=15\ \text{cm}$ được giữ cố định"''', r"$f=15\ \text{cm}$ ; thấu kính đứng yên", r"Công thức : $\dfrac1f=\dfrac1d+\dfrac1{d'}$ ⇒ $d'=\dfrac{df}{d-f}$"),
  (r'''"Vật sáng $AB$ cao $2\ \text{cm}$"''', r"$h=2\ \text{cm}$", r"Tỉ số chiều cao : $\dfrac{h'}{h}=\dfrac{|d'|}{d}$"),
  (r'''"cách thấu kính $45\ \text{cm}$"''', r"$d_1=45\ \text{cm}$", r"⚠ $d_1\gt f$ nên ảnh thật, $d'\gt0$ ; khoảng cách vật–ảnh thật $L=d+d'$"),
  (r'''"Dịch vật lại gần thấu kính $15\ \text{cm}$"''', r"$d_2=d_1-15$", r"Lại gần thì $d$ giảm ; ảnh dịch một đoạn $|d_2'-d_1'|$"),
  (r'''"Dịch vật lại gần thấu kính thêm $10\ \text{cm}$ nữa"''', r"$d_3=d_2-10$", r"⚠ vẫn còn $d_3\gt f$ không ? Có thì ảnh vẫn thật"),
  (r'''"khoảng cách giữa vật thật và ảnh thật của thấu kính hội tụ không nhỏ hơn $4f$"''', r"$L=d+d'$", r"Thế $d'=L-d$ ⇒ phương trình bậc hai ẩn $d$ ; có nghiệm khi $\Delta\ge0$"),
  (r'''"Dịch vật lại gần thấu kính $5\ \text{cm}$ thì ảnh vẫn là ảnh thật, dịch đi $10\ \text{cm}$ và cao gấp đôi ảnh cũ"''', r"$d_2=d_1-5$ ; $d_2'-d_1'=10$ ; $h_2'=2h_1'$", r"Tam giác đồng dạng : $\dfrac{h'}{h}=\dfrac{f}{d-f}$ và $d'-f=\dfrac{f^2}{d-f}$"),
  (r'''"Tìm tiêu cự của thấu kính và vị trí ban đầu của vật"''', r"$f=?$ ; $d_1=?$", r"Hai ẩn $f$, $d_1$ : cần hai phương trình (chiều cao, độ dịch)")],
 # Dạng 5
 [(r'''"Vật sáng $AB$ cao $2\ \text{cm}$ và màn ảnh đặt cố định, cách nhau $125\ \text{cm}$"''', r"$h=2\ \text{cm}$ ; $L=125\ \text{cm}$", r"Ảnh hứng được trên màn là ảnh thật : $d+d'=L$"),
  (r'''"có hai vị trí của thấu kính cách nhau $75\ \text{cm}$ đều cho ảnh rõ trên màn"''', r"$\ell=75\ \text{cm}$", r"⚠ có hai vị trí chỉ khi $L\gt4f$ ; hai nghiệm của $d^2-Ld+Lf=0$ hơn kém nhau $\ell$"),
  (r'''"Chứng tỏ tích hai chiều cao ảnh bằng bình phương chiều cao vật"''', r"$h_1'h_2'=h^2$ ?", r"Hai vị trí đối xứng : $d_1=d_2'$ và $d_1'=d_2$"),
  (r'''"khoảng cách vật–màn còn $70\ \text{cm}$"''', r"$L'=70\ \text{cm}$", r"⚠ so $L'$ với $4f$ trước khi dùng công thức hai vị trí"),
  (r'''"đo ba lần được $79{,}5\ \text{cm}$; $80{,}6\ \text{cm}$; $80{,}2\ \text{cm}$"''', r"$L_1$ ; $L_2$ ; $L_3$", r"Trung bình $\bar L$, sai số $\overline{\Delta L}=\dfrac{\sum|L_i-\bar L|}{3}$ ; $f=\dfrac{L_{min}}{4}$"),
  (r'''"Đại lượng nào cần đo cẩn thận hơn?"''', r"so sánh $L$ và $\ell$", r"Cho từng đại lượng lệch $1\ \text{cm}$, so độ đổi của $f=\dfrac{L^2-\ell^2}{4L}$")],
 # Dạng 6
 [(r'''"Một kính lúp có ghi $5\times$ trên vành"''', r"$G=5$", r"Kính lúp là thấu kính hội tụ tiêu cự ngắn ; $G=\dfrac{25}{f}$ ($f$ tính bằng cm)"),
  (r'''"Một người mắt tốt (điểm cực cận $C_c$ cách mắt $25\ \text{cm}$, điểm cực viễn $C_v$ ở vô cực)"''', r"$OC_c=25\ \text{cm}$ ; $C_v$ ở vô cực", r"Mắt nhìn rõ khi ảnh nằm trong khoảng từ $C_c$ tới $C_v$"),
  (r'''"đặt kính sát mắt"''', r"kính–mắt $\approx0$", r"⚠ kính sát mắt nên khoảng cách ảnh–mắt bằng $|d'|$"),
  (r'''"ảnh ảo hiện ra đúng tại $C_c$"''', r"$|d'|=OC_c$", r"⚠ ảnh ảo nên $d'\lt0$ khi thế vào $\dfrac1f=\dfrac1d+\dfrac1{d'}$"),
  (r'''"So sánh với số bội giác ghi trên kính"''', r"$G$ và $|k|$", r"$|k|=\dfrac{|d'|}{d}$ ; $G=\dfrac{25}{f}$ ứng với ngắm chừng ở vô cực"),
  (r'''"Muốn ngắm chừng ở vô cực"''', r"ảnh ở vô cực", r"Ảnh ở vô cực khi $\dfrac1{d'}=0$"),
  (r'''"Vật phải đặt trong khoảng nào trước kính thì mắt nhìn rõ ảnh?"''', r"$d_{min}\le d\le d_{max}$", r"Hai đầu khoảng ứng với ảnh tại $C_c$ và ảnh tại $C_v$"),
  (r'''"vết xước dài $0{,}4\ \text{mm}$"''', r"$h=0{,}4\ \text{mm}$", r"$h'=|k|\,h$")],
 # Dạng 7
 [(r'''"Thấu kính hội tụ $TK_1$ có tiêu cự $f_1=20\ \text{cm}$"''', r"$f_1=20\ \text{cm}$", r"Công thức thấu kính dùng cho từng thấu kính"),
  (r'''"Vật sáng $AB$ cao $2\ \text{cm}$ đặt vuông góc với trục chính, cách $TK_1$ một khoảng $30\ \text{cm}$"''', r"$h=2\ \text{cm}$ ; $d_1=30\ \text{cm}$", r"Sơ đồ : $AB\xrightarrow{TK_1}A_1'B_1'\xrightarrow{TK_2}A_2'B_2'$"),
  (r'''"$TK_2$ là thấu kính phân kì có tiêu cự $20\ \text{cm}$"''', r"$f_2=-20\ \text{cm}$", r"⚠ thấu kính phân kì : $f\lt0$"),
  (r'''"đặt cách $TK_1$ một khoảng $80\ \text{cm}$"''', r"$a=80\ \text{cm}$", r"Ảnh qua $TK_1$ là vật của $TK_2$ : $d_2=a-d_1'$"),
  (r'''"Xác định vị trí, tính chất, chiều và chiều cao của ảnh cuối cùng qua hệ"''', r"$d_2'=?$ ; $h_2'=?$", r"$h_2'=h\cdot\dfrac{|d_1'|}{d_1}\cdot\dfrac{|d_2'|}{|d_2|}$ ; chiều : mỗi ảnh thật đảo chiều một lần"),
  (r'''"Đẩy $TK_2$ lại sát $TK_1$ (ghép sát)"''', r"$a=0$", r"Ghép sát : $\dfrac1f=\dfrac1{f_1}+\dfrac1{f_2}$"),
  (r'''"coi ảnh qua $TK_1$ là vật của $TK_2$"''', r"$d_2=a-d_1'$", r"⚠ $d_2\lt0$ : chùm tia gặp $TK_2$ trước khi kịp hội tụ, $A_1'B_1'$ là vật ảo"),
  (r'''"Thay $TK_2$ bằng thấu kính hội tụ có tiêu cự $20\ \text{cm}$, đặt sau ảnh trung gian $A_1'B_1'$"''', r"$f_2=20\ \text{cm}$ ; $d_2\gt0$", r"Tỉ số chiều cao của hệ là tích hai tỉ số"),
  (r'''"ảnh cuối là ảnh thật, cao gấp đôi vật"''', r"$h_2'=2h$ ; $a=?$", r"Ảnh thật bằng vật khi $d=d'=2f$")],
]

# ═════════════ LỜI GIẢI ═════════════
R4 = [r"<strong>Công thức:</strong> $\dfrac1f=\dfrac1d+\dfrac1{d'}$ ; $d'\gt0$ ảnh thật, ngược chiều.",
      r"<strong>Tam giác đồng dạng:</strong> ảnh thật có $\dfrac{h'}{h}=\dfrac{d'}{d}=\dfrac{f}{d-f}$ và $d'=f+\dfrac{f^2}{d-f}$.",
      r"<strong>Khoảng cách vật–ảnh thật:</strong> $L=d+d'$.",
      r"<strong>Điều kiện:</strong> thấu kính hội tụ cho ảnh thật khi vật thật đặt ngoài tiêu cự, $d\gt f$."]
R5 = [r"<strong>Ảnh trên màn là ảnh thật:</strong> $d+d'=L$ ⇒ $d^2-Ld+Lf=0$.",
      r"<strong>Hai nghiệm:</strong> $d_1+d_2=L$, $d_2-d_1=\ell=\sqrt{L^2-4Lf}$ ⇒ $f=\dfrac{L^2-\ell^2}{4L}$.",
      r"<strong>Điều kiện:</strong> có ảnh rõ khi $L\ge4f$ ; có hai vị trí khi $L\gt4f$.",
      r"<strong>Sai số:</strong> $\overline{\Delta L}$ là trung bình các $|L_i-\bar L|$ ; $f=\dfrac{L}{4}$ thì $\Delta f=\dfrac{\overline{\Delta L}}{4}$."]
R6 = [r"<strong>Kính lúp:</strong> thấu kính hội tụ tiêu cự ngắn ; vật trong khoảng $OF$ cho ảnh ảo, cùng chiều, lớn hơn.",
      r"<strong>Số bội giác:</strong> $G=\dfrac{25}{f}$ ($f$ tính bằng cm), mắt tốt ngắm chừng ở vô cực.",
      r"<strong>Mắt:</strong> nhìn rõ khi ảnh nằm từ $C_c$ tới $C_v$ ; kính sát mắt nên khoảng cách ảnh–mắt là $|d'|$.",
      r"<strong>Điều kiện:</strong> ảnh ảo thì $d'\lt0$ ; $|k|=\dfrac{|d'|}{d}$ không phải là $G$."]
R7 = [r"<strong>Sơ đồ:</strong> $AB\xrightarrow{TK_1}A_1'B_1'\xrightarrow{TK_2}A_2'B_2'$ ; ảnh qua $TK_1$ là vật của $TK_2$.",
      r"<strong>Khoảng cách:</strong> $d_2=a-d_1'$ (đúng cả khi $d_1'\lt0$).",
      r"<strong>Chiều cao:</strong> $h_2'=h\cdot\dfrac{|d_1'|}{d_1}\cdot\dfrac{|d_2'|}{|d_2|}$ ; mỗi ảnh thật đảo chiều một lần.",
      r"<strong>Ghép sát:</strong> $\dfrac1f=\dfrac1{f_1}+\dfrac1{f_2}$ ; thấu kính phân kì có $f\lt0$.",
      r"<strong>Chiều tổng quát:</strong> $k=-\dfrac{d'}{d}$ cho từng thấu kính, $k_{hệ}=k_1\cdot k_2$ ; $k_{hệ}\gt0$ cùng chiều vật. Đếm ảnh thật chỉ đúng khi mọi vật đều thật."]

SOLS = [
 sol(R4, [
  ("Ảnh lúc đầu", [P(r"$d_1=45\ \text{cm}\gt f$ nên ảnh thật :"),
     M(r"d_1'=\dfrac{d_1f}{d_1-f}=\dfrac{45\cdot15}{45-15}"), A(r"d_1'=22{,}5\ \text{cm}"),
     M(r"h_1'=h\cdot\dfrac{d_1'}{d_1}=2\cdot\dfrac{22{,}5}{45}=1\ \text{cm}"),
     M(r"L_1=d_1+d_1'=67{,}5\ \text{cm}")]),
  (r"Vật lại gần $15\ \text{cm}$", [P(r"$d_2=45-15=30\ \text{cm}$, vẫn lớn hơn $f$ :"),
     M(r"d_2'=\dfrac{30\cdot15}{30-15}=30\ \text{cm}"), M(r"d_2'-d_1'=30-22{,}5"),
     A(r"\text{ảnh dịch ra xa thấu kính }7{,}5\ \text{cm}"),
     P(r"Ảnh cao $2\ \text{cm}$ (bằng vật) ; $L_2=60\ \text{cm}$. Vật và ảnh dịch cùng chiều truyền ánh sáng.")]),
  (r"Vật lại gần thêm $10\ \text{cm}$", [P(r"$d_3=30-10=20\ \text{cm}\gt f$ :"),
     M(r"d_3'=\dfrac{20\cdot15}{20-15}=60\ \text{cm}"), M(r"d_3'-d_2'=60-30"), A(r"\text{ảnh dịch thêm }30\ \text{cm}"),
     P(r"Ảnh cao $2\cdot\dfrac{60}{20}=6\ \text{cm}$ ; $L_3=80\ \text{cm}$. Vật dịch đều, ảnh dịch ngày càng nhanh.")]),
  ("Khoảng cách vật–ảnh nhỏ nhất", [P(r"Qua ba vị trí : $L=67{,}5\to60\to80\ \text{cm}$, giảm rồi tăng. Thế $d'=L-d$ :"),
     M(r"\dfrac1f=\dfrac1d+\dfrac1{L-d}\ \Rightarrow\ d^2-Ld+Lf=0"),
     M(r"\Delta=L^2-4Lf\ge0\ \Rightarrow\ L\ge4f"),
     A(r"L_{min}=4f=60\ \text{cm}"),
     P(r"Dấu bằng khi $d=d'=2f=30\ \text{cm}$ : ảnh thật bằng vật.")]),
  ("Lập phương trình từ chiều cao ảnh", [P(r"Ảnh thật : $\dfrac{h'}{h}=\dfrac{f}{d-f}$. Ảnh mới cao gấp đôi, $d_2=d_1-5$ :"),
     M(r"\dfrac{h_2'}{h_1'}=\dfrac{d_1-f}{d_2-f}=2"), M(r"d_1-f=2\,(d_1-5-f)"), A(r"d_1-f=10\ \text{cm}")]),
  ("Tiêu cự và vị trí ban đầu", [P(r"Dùng $d'-f=\dfrac{f^2}{d-f}$ cho hai vị trí ($d_2-f=5\ \text{cm}$) ; ảnh dịch $10\ \text{cm}$ :"),
     M(r"d_2'-d_1'=\dfrac{f^2}{5}-\dfrac{f^2}{10}=\dfrac{f^2}{10}=10"),
     A(r"f=10\ \text{cm},\quad d_1=20\ \text{cm}")]),
  ("Kiểm tra", [P(r"Câu c : $d_1=20$ ⇒ $d_1'=20\ \text{cm}$, ảnh bằng vật ; $d_2=15$ ⇒ $d_2'=30\ \text{cm}$, ảnh gấp đôi vật ✓ ; ảnh dịch $30-20=10\ \text{cm}$ ✓."),
     P(r"Câu b : vị trí $d=30\ \text{cm}=2f$ cho đúng $L=60\ \text{cm}=4f$, khớp với giá trị nhỏ nhất ✓."),
     P(r"Mọi ảnh đều dịch ra xa khi vật lại gần : đúng nhận xét $d'=f+\dfrac{f^2}{d-f}$ tăng khi $d$ giảm ✓.")])],
  [r"a) $d_1'=22{,}5\ \text{cm}$ ; $h_1'=1\ \text{cm}$ ; $L_1=67{,}5\ \text{cm}$ ; ảnh dịch ra xa thấu kính $7{,}5\ \text{cm}$",
   r"b) ảnh dịch thêm $30\ \text{cm}$ ; $L$ : $67{,}5\to60\to80\ \text{cm}$ ; $L_{min}=4f=60\ \text{cm}$",
   r"c) $f=10\ \text{cm}$ ; vật lúc đầu cách thấu kính $20\ \text{cm}$"],
  r"Nhận dạng: thấy <strong>dịch vật</strong>, <strong>ảnh dịch đi</strong> hay <strong>khoảng cách vật–ảnh</strong> → tính lại $d'$ ở mỗi vị trí ; hỏi nhỏ nhất thì lập $d^2-Ld+Lf=0$ và đòi $\Delta\ge0$."),
 sol(R5, [
  ("Tiêu cự", [P(r"Hai vị trí là hai nghiệm của $d^2-Ld+Lf=0$, hơn kém nhau $\ell$ :"),
     M(r"f=\dfrac{L^2-\ell^2}{4L}=\dfrac{125^2-75^2}{4\cdot125}=\dfrac{10\,000}{500}"), A(r"f=20\ \text{cm}")]),
  ("Ảnh ở vị trí gần vật", [M(r"d_1=\dfrac{L-\ell}{2}=25\ \text{cm},\quad d_1'=L-d_1=100\ \text{cm}"),
     M(r"h_1'=h\cdot\dfrac{d_1'}{d_1}=2\cdot\dfrac{100}{25}"), A(r"h_1'=8\ \text{cm}")]),
  ("Ảnh ở vị trí xa vật", [P(r"Hai vị trí đối xứng : $d_2=d_1'=100\ \text{cm}$, $d_2'=d_1=25\ \text{cm}$ :"),
     M(r"h_2'=2\cdot\dfrac{25}{100}"), A(r"h_2'=0{,}5\ \text{cm}"),
     M(r"h_1'h_2'=h^2\cdot\dfrac{d_1'}{d_1}\cdot\dfrac{d_2'}{d_2}=h^2\cdot\dfrac{d_1'}{d_1}\cdot\dfrac{d_1}{d_1'}=h^2"),
     P(r"Thật vậy $8\cdot0{,}5=4=2^2$ : đo hai ảnh là suy ra được chiều cao vật mà không cần đặt thước vào vật.")]),
  ("Khoảng cách vật–màn nhỏ nhất", [P(r"Phương trình có nghiệm khi $\Delta=L^2-4Lf\ge0$, tức $L\ge4f$ :"),
     A(r"L_{min}=4f=80\ \text{cm}"),
     P(r"$70\ \text{cm}\lt80\ \text{cm}$ nên không còn vị trí nào cho ảnh rõ trên màn.")]),
  ("Kết quả đo 2f–2f", [M(r"\bar L=\dfrac{79{,}5+80{,}6+80{,}2}{3}=80{,}10\ \text{cm}"),
     M(r"\overline{\Delta L}=\dfrac{0{,}6+0{,}5+0{,}1}{3}=0{,}40\ \text{cm}"),
     M(r"\bar f=\dfrac{\bar L}{4}\approx20{,}0\ \text{cm},\quad\Delta f=\dfrac{\overline{\Delta L}}{4}"),
     A(r"f=20{,}0\pm0{,}1\ \text{cm}")]),
  (r"Khi $L$ lệch thêm $1\ \text{cm}$", [M(r"f'=\dfrac{126^2-75^2}{4\cdot126}=\dfrac{10\,251}{504}\approx20{,}34\ \text{cm}"),
     A(r"f\ \text{tăng khoảng }0{,}34\ \text{cm}")]),
  (r"Khi $\ell$ lệch thêm $1\ \text{cm}$", [M(r"f''=\dfrac{125^2-76^2}{4\cdot125}=\dfrac{9849}{500}\approx19{,}70\ \text{cm}"),
     A(r"f\ \text{giảm khoảng }0{,}30\ \text{cm}"),
     P(r"Cùng lệch $1\ \text{cm}$, sai $L$ làm $f$ lệch nhiều hơn : phải đo khoảng cách vật–màn cẩn thận hơn.")]),
  ("Kiểm tra", [P(r"$4f=80\ \text{cm}\lt125\ \text{cm}$ nên đúng là có hai vị trí ✓ ; $d_1+d_2=25+100=125\ \text{cm}$ ✓."),
     P(r"Thế lại : $\dfrac1{25}+\dfrac1{100}=\dfrac{5}{100}=\dfrac1{20}$ ✓."),
     P(r"Cách 2f–2f cho $20{,}0\pm0{,}1\ \text{cm}$, khớp cách hai vị trí ✓.")])],
  [r"a) $f=20\ \text{cm}$ ; ảnh cao $8\ \text{cm}$ và $0{,}5\ \text{cm}$ ; $h_1'h_2'=4\ \text{cm}^2=h^2$",
   r"b) không có vị trí nào ; $L_{min}=80\ \text{cm}$",
   r"c) $f=20{,}0\pm0{,}1\ \text{cm}$",
   r"d) $f$ đổi khoảng $+0{,}34\ \text{cm}$ khi sai $L$, $-0{,}30\ \text{cm}$ khi sai $\ell$ : đo $L$ cẩn thận hơn"],
  r"Nhận dạng: thấy <strong>vật và màn cố định</strong>, <strong>hai vị trí thấu kính</strong> cho ảnh rõ → $f=\dfrac{L^2-\ell^2}{4L}$, hai vị trí đối xứng ; luôn kiểm $L\ge4f$ trước."),
 sol(R6, [
  ("Tiêu cự", [M(r"G=\dfrac{25}{f}\ \Rightarrow\ f=\dfrac{25}{5}"), A(r"f=5\ \text{cm}")]),
  ("Ngắm chừng ở $C_c$", [P(r"Ảnh ảo hiện tại $C_c$, kính sát mắt nên $d'=-OC_c=-25\ \text{cm}$ :"),
     M(r"\dfrac1d=\dfrac1f-\dfrac1{d'}=\dfrac15+\dfrac1{25}=\dfrac{6}{25}"), A(r"d=\dfrac{25}{6}\approx4{,}17\ \text{cm}")]),
  ("Ảnh cao gấp mấy lần vật", [M(r"|k|=\dfrac{|d'|}{d}=\dfrac{25}{25/6}"), A(r"|k|=6"),
     P(r"Lớn hơn số $G=5$ ghi trên kính : $G$ ứng với ngắm chừng ở vô cực, còn ngắm ở $C_c$ ảnh to hơn một chút.")]),
  ("Ngắm chừng ở vô cực", [P(r"Ảnh ở vô cực khi $\dfrac1{d'}=0$ :"), M(r"\dfrac1d=\dfrac1f"), A(r"T:Đặt vật tại tiêu điểm $F$, cách kính $d=f=5\ \text{cm}$.")]),
  ("Khoảng đặt vật", [P(r"Ảnh phải ở từ $C_c$ (vật ở $\tfrac{25}{6}\ \text{cm}$) tới vô cực (vật ở $5\ \text{cm}$) :"),
     M(r"\dfrac{25}{6}\ \text{cm}\le d\le5\ \text{cm}"),
     M(r"\Delta d=5-\dfrac{25}{6}=\dfrac56\ \text{cm}"), A(r"\Delta d\approx8{,}3\ \text{mm}")]),
  ("Ảnh của vết xước", [P(r"Ngắm chừng ở $C_c$ thì tỉ số chiều cao là $|k|$ vừa tìm :"), M(r"h'=|k|\,h=6\cdot0{,}4"), A(r"h'=2{,}4\ \text{mm}")]),
  ("Kiểm tra", [P(r"Thế lại $d=\tfrac{25}{6}$ : $\dfrac{6}{25}-\dfrac1{25}=\dfrac15$ ✓."),
     P(r"Cả khoảng đặt vật nằm trong $OF$ ($d\le f$) nên ảnh luôn ảo, cùng chiều ✓."),
     P(r"Khoảng xê dịch chưa tới $1\ \text{cm}$ : khi dùng kính lúp chỉ cần nhích kính rất nhẹ là ảnh rõ hay mờ ✓.")])],
  [r"a) $f=5\ \text{cm}$",
   r"b) $d=\dfrac{25}{6}\approx4{,}17\ \text{cm}$ ; ảnh cao gấp $6$ lần vật, lớn hơn $G=5$",
   r"c) vật đặt tại tiêu điểm, cách kính $5\ \text{cm}$",
   r"d) $4{,}17\ \text{cm}\le d\le5\ \text{cm}$ ; xê dịch khoảng $8{,}3\ \text{mm}$ ; ảnh vết xước dài $2{,}4\ \text{mm}$"],
  r"Nhận dạng: thấy <strong>kính lúp</strong>, <strong>ngắm chừng ở $C_c$</strong> → ảnh ảo tại $C_c$, thế $d'=-OC_c$ ; <strong>ngắm chừng ở vô cực</strong> → $d=f$, $G=\dfrac{25}{f}$."),
 sol(R7, [
  ("Ảnh qua $TK_1$", [M(r"d_1'=\dfrac{d_1f_1}{d_1-f_1}=\dfrac{30\cdot20}{30-20}"), A(r"d_1'=60\ \text{cm}"),
     P(r"Ảnh trung gian thật, ngược chiều, cao $h_1'=2\cdot\dfrac{60}{30}=4\ \text{cm}$.")]),
  ("Vật của $TK_2$", [P(r"Ảnh trung gian nằm giữa hai thấu kính, trước $TK_2$ :"), M(r"d_2=a-d_1'=80-60"), A(r"d_2=20\ \text{cm}\ (\text{vật thật})")]),
  ("Ảnh qua $TK_2$", [P(r"Thấu kính phân kì : $f_2=-20\ \text{cm}$."), M(r"d_2'=\dfrac{d_2f_2}{d_2-f_2}=\dfrac{20\cdot(-20)}{20+20}"),
     A(r"d_2'=-10\ \text{cm}"),
     P(r"Ảnh ảo, cách $TK_2$ $10\ \text{cm}$ về phía $TK_1$, tức cách $TK_1$ $70\ \text{cm}$ : nằm giữa hai thấu kính.")]),
  ("Chiều cao và chiều của ảnh cuối", [M(r"h_2'=h\cdot\dfrac{|d_1'|}{d_1}\cdot\dfrac{|d_2'|}{d_2}=2\cdot\dfrac{60}{30}\cdot\dfrac{10}{20}"), A(r"h_2'=2\ \text{cm}"),
     P(r"Chỉ một ảnh thật ($A_1'B_1'$) nên đảo chiều một lần : ảnh cuối ngược chiều vật.")]),
  ("⭐⭐⭐ Ghép sát : vật ảo của $TK_2$", [M(r"\dfrac1f=\dfrac1{20}+\dfrac1{-20}=0"),
     P(r"Hệ có tiêu cự vô cùng lớn : như một tấm kính phẳng, ảnh trùng vật (ảo, cùng chiều, bằng vật)."),
     P(r"Kiểm lại từng thấu kính. Chùm tia ló khỏi $TK_1$ đang hội tụ về $A_1'$ (cách $60\ \text{cm}$) thì gặp ngay $TK_2$ : chưa kịp hội tụ. Điểm hội tụ nằm <em>sau</em> $TK_2$, nên $A_1'B_1'$ là <strong>vật ảo</strong> của $TK_2$, khoảng cách mang dấu âm :"),
     M(r"d_2=a-d_1'=0-60"), A(r"d_2=-60\ \text{cm}\ (\text{vật ảo})")]),
  ("Ảnh qua $TK_2$ khi ghép sát", [P(r"Vẫn một công thức, chỉ thế $d_2$ có dấu :"),
     M(r"\dfrac1{d_2'}=\dfrac1{f_2}-\dfrac1{d_2}=-\dfrac1{20}+\dfrac1{60}=-\dfrac1{30}"), A(r"d_2'=-30\ \text{cm}"),
     P(r"Ảnh ảo cách hệ $30\ \text{cm}$ về phía trước : đúng chỗ vật $AB$."),
     M(r"k_1=-\dfrac{60}{30}=-2,\quad k_2=-\dfrac{d_2'}{d_2}=-\dfrac{-30}{-60}=-\dfrac12"),
     P(r"$k_{hệ}=k_1k_2=1$ : cùng chiều, bằng vật — khớp kết luận tấm kính phẳng. Ảnh qua $TK_2$ là ảnh ảo mà vẫn đảo chiều ($k_2\lt0$) vì vật của nó là vật ảo : khi có vật ảo, quy tắc đếm ảnh thật không dùng được.")]),
  ("Đặt $TK_2$ hội tụ", [P(r"Ảnh trung gian đã cao gấp đôi vật, nên $TK_2$ phải cho ảnh thật bằng vật của nó :"),
     M(r"\dfrac{f_2}{d_2-f_2}=1\ \Rightarrow\ d_2=2f_2=40\ \text{cm}"), M(r"a=d_1'+d_2=60+40"), A(r"a=100\ \text{cm}"),
     P(r"Ảnh cuối thật, cách $TK_2$ $40\ \text{cm}$ ; hai ảnh thật nên đảo chiều hai lần : ảnh cuối cùng chiều vật.")]),
  ("Kiểm tra", [P(r"Câu a : ảnh của thấu kính phân kì có $|d_2'|=10\lt|f_2|=20$ và $\lt d_2$ ✓."),
     P(r"Câu c : tỉ số của hệ $2\cdot\dfrac{40}{40}=2$ ✓ ; $d_2=40\gt f_2$ nên ảnh thật ✓."),
     P(r"Câu b chỉ là mở rộng : đề thi lớp 9 thường cho $d_2\gt0$ ; gặp ghép sát thì dùng $\dfrac1f=\dfrac1{f_1}+\dfrac1{f_2}$ là đủ.")])],
  [r"a) ảnh cuối ảo, cách $TK_2$ $10\ \text{cm}$ (cách $TK_1$ $70\ \text{cm}$), cao $2\ \text{cm}$, ngược chiều vật",
   r"b) hệ như tấm kính phẳng ; ảnh ảo trùng vật, cùng chiều, bằng vật ($d_2=-60\ \text{cm}$, $d_2'=-30\ \text{cm}$)",
   r"c) $a=100\ \text{cm}$ ; ảnh cuối thật, cùng chiều vật"],
  r"Nhận dạng: thấy <strong>hai thấu kính đồng trục</strong> → lập sơ đồ ảnh, ảnh qua thấu kính 1 là vật của thấu kính 2, $d_2=a-d_1'$ ; chiều theo $k_{hệ}=k_1k_2$ với $k=-\dfrac{d'}{d}$ (vật đều thật thì đếm số ảnh thật)."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>dịch vật</b>, <b>ảnh dịch đi</b>, <b>khoảng cách vật–ảnh nhỏ nhất</b> → tính lại $d'$, rồi <b>Δ ≥ 0</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Ảnh lúc đầu", "Lúc đầu ảnh cách thấu kính bao nhiêu cm?", float(D4_1P), "cm", 0.1,
       loi=r"Dùng $d'=\dfrac{df}{d+f}$ (sai dấu ở mẫu) ; hoặc nhớ nhầm $\dfrac1{d'}=\dfrac1f+\dfrac1d$."),
  buoc(r"Vật lại gần $15\ \text{cm}$", "Khi vật lại gần thấu kính 15 cm, ảnh dịch đi bao nhiêu cm?", float(DICH4_1), "cm", 0.1,
       loi=r"Cho rằng ảnh dịch bằng vật, hoặc dịch lại gần thấu kính ; thật ra $d'=f+\dfrac{f^2}{d-f}$ tăng khi $d$ giảm.",
       ke=[(r"Tính $d_2'$ với $d_2=d_1-15$, rồi lấy $d_2'-d_1'$", True),
           (r"Ảnh dịch đúng bằng vật : $15\ \text{cm}$", r"Vật và ảnh thật dịch cùng chiều nhưng không cùng độ dài ; phải tính lại $d_2'$."),
           (r"Tính $d_2'$ với $d_2=d_1+15$", r"Lại gần thấu kính thì $d$ giảm, không tăng.")]),
  buoc(r"Vật lại gần thêm $10\ \text{cm}$", "Lần dịch thứ hai, ảnh dịch thêm bao nhiêu cm?", float(DICH4_2), "cm", 0.2,
       loi=r"Lấy $d_3=d_1-10$ (tính từ vị trí ban đầu), hoặc trả lời độ dịch tính từ vị trí ban đầu.",
       ke=[(r"$d_3=d_2-10$, tính $d_3'$ rồi lấy $d_3'-d_2'$", True),
           (r"$d_3=d_1-10$", r"Vật dịch thêm từ vị trí thứ hai, không phải từ vị trí ban đầu."),
           (r"Lấy $d_3'-d_1'$", r"Đó là độ dịch tính từ vị trí ban đầu ; đề hỏi dịch thêm so với vị trí thứ hai.")]),
  buoc("Khoảng cách vật–ảnh nhỏ nhất", "Khoảng cách vật–ảnh thật nhỏ nhất với thấu kính này là bao nhiêu cm?", float(LMIN4), "cm", 0.2,
       loi=r"Kết luận từ ba vị trí đã tính mà không chứng minh ; hoặc giải $\Delta\ge0$ ra $L\ge2f$ vì quên hệ số 4.",
       ke=[(r"Thế $d'=L-d$, lập $d^2-Ld+Lf=0$, đòi $\Delta\ge0$", True),
           (r"Lấy giá trị nhỏ nhất trong ba vị trí đã tính", r"Ba vị trí chỉ là ba mẫu ; phải chứng minh không vị trí nào cho $L$ nhỏ hơn."),
           (r"Cho $d=f$ để $L$ nhỏ nhất", r"Khi $d=f$ ảnh ở vô cực : $L$ lớn vô cùng, không phải nhỏ nhất.")]),
  buoc("Lập phương trình từ chiều cao ảnh", "Câu c: hiệu d₁ − f bằng bao nhiêu cm?", float(X4C), "cm", 0.1,
       loi=r"Viết $d_2=d_1+5$ (vật lại gần mà cho $d$ tăng) ; hoặc đặt tỉ số bằng $\tfrac12$ vì lẫn ảnh cũ với ảnh mới.",
       ke=[(r"Dùng $\dfrac{h'}{h}=\dfrac{f}{d-f}$ cho hai vị trí, chia vế theo vế", True),
           (r"Dùng $\dfrac{h_2'}{h_1'}=\dfrac{d_2}{d_1}$", r"Tỉ số chiều cao ảnh là $\dfrac{d'}{d}$ của từng vị trí, không phải tỉ số hai khoảng cách vật."),
           (r"Dùng $\dfrac{h_2'}{h_1'}=\dfrac{d_2'}{d_1'}$", r"Quên vật cũng đổi chỗ : $\dfrac{h'}{h}=\dfrac{d'}{d}$ có cả $d$ ở mẫu.")]),
  buoc("Tiêu cự và vị trí ban đầu", "Tiêu cự của thấu kính câu c bằng bao nhiêu cm?", float(F4C), "cm", 0.1,
       loi=r"Lẫn hiệu $d_1-f$ vừa tìm với $d_1$ ; hoặc cộng $\dfrac{f^2}{d_2-f}+\dfrac{f^2}{d_1-f}$ thay vì trừ.",
       ke=[(r"Viết $d'-f=\dfrac{f^2}{d-f}$ cho hai vị trí ; hiệu hai $d'$ bằng độ dịch của ảnh", True),
           (r"Cho hiệu hai $d'$ bằng độ dịch của vật", r"Độ dịch của ảnh khác độ dịch của vật ; phải dùng số đề cho cho ảnh."),
           (r"Cho $d_1'=d_1$ rồi thế vào công thức thấu kính", r"Không có lí do để ảnh và vật cách thấu kính bằng nhau ; điều đó chỉ đúng khi $d=2f$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>vật, màn cố định</b>, <b>hai vị trí thấu kính</b> cho ảnh rõ → <b>f = (L² − ℓ²)/4L</b>, kiểm L ≥ 4f",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tiêu cự", "Tiêu cự của thấu kính bằng bao nhiêu cm?", float(F5), "cm", 0.1,
       loi=r"Dùng $f=\dfrac{L-\ell}{4}$ hoặc quên chia cho $4L$ ; cũng hay lấy $f=\dfrac{\ell}{2}$."),
  buoc("Ảnh ở vị trí gần vật", "Ở vị trí thấu kính gần vật, ảnh cao bao nhiêu cm?", float(H5_1), "cm", 0.05,
       loi=r"Lấy $d_1=\dfrac{\ell}{2}$ hoặc $d_1=\ell$ ; hoặc đảo tỉ số thành $\dfrac{d}{d'}$.",
       ke=[(r"$d_1=\dfrac{L-\ell}{2}$, $d_1'=L-d_1$, rồi $h_1'=h\,\dfrac{d_1'}{d_1}$", True),
           (r"$d_1=\ell$", r"$\ell$ là khoảng cách giữa hai vị trí thấu kính, không phải khoảng cách vật–thấu kính."),
           (r"$h_1'=h\,\dfrac{d_1}{d_1'}$", r"Tỉ số bị đảo : ảnh xa thấu kính hơn vật thì ảnh cao hơn vật, $\dfrac{h'}{h}=\dfrac{d'}{d}$.")]),
  buoc("Ảnh ở vị trí xa vật", "Ở vị trí thấu kính xa vật, ảnh cao bao nhiêu cm?", float(H5_2), "cm", 0.02,
       loi=r"Nghĩ hai ảnh cao bằng nhau vì cùng hứng trên một màn.",
       ke=[(r"Hai vị trí đối xứng : $d_2=d_1'$, $d_2'=d_1$", True),
           (r"Ảnh vẫn cao như ở vị trí 1 vì màn không đổi", r"Màn đứng yên nhưng $d$ và $d'$ đổi chỗ cho nhau nên tỉ số $\dfrac{d'}{d}$ đảo ngược."),
           (r"$d_2=L-\ell$", r"Đó là $2d_1$ ; vị trí thứ hai cách vật $d_1+\ell$.")]),
  buoc("Khoảng cách vật–màn nhỏ nhất", "Khoảng cách vật–màn nhỏ nhất còn có ảnh rõ là bao nhiêu cm?", float(LMIN5), "cm", 0.2,
       loi=r"Thế $L=70\ \text{cm}$ vào công thức hai vị trí, ra $\ell^2\lt0$ mà không nhận ra là vô nghiệm.",
       ke=[(r"Điều kiện có nghiệm $\Delta=L^2-4Lf\ge0$", True),
           (r"Điều kiện $L\ge2f$", r"$\Delta\ge0$ cho $L\ge4f$ ; $2f$ là vị trí vật cho ảnh bằng vật, không phải khoảng cách vật–ảnh."),
           (r"Không có giới hạn, chỉ cần dịch thấu kính đủ xa", r"Phương trình $d^2-Ld+Lf=0$ vô nghiệm khi $L\lt4f$ : không vị trí nào cho ảnh rõ.")]),
  buoc("Kết quả đo 2f–2f", "Sai số Δf của phép đo 2f–2f bằng bao nhiêu cm?", float(DF5), "cm", 0.02,
       loi=r"Quên chia sai số cho 4 ; hoặc giữ quá nhiều chữ số thập phân cho $\bar f$.",
       ke=[(r"Tính $\bar L$, $\overline{\Delta L}$ rồi chia cả hai cho 4", True),
           (r"$\Delta f=\overline{\Delta L}$", r"$f=\dfrac{L}{4}$ nên sai số của $f$ cũng chia 4."),
           (r"Lấy hiệu lần đo lớn nhất và nhỏ nhất làm sai số", r"Sai số tuyệt đối trung bình là trung bình các $|L_i-\bar L|$, không phải khoảng biến thiên.")]),
  buoc(r"Khi $L$ lệch thêm $1\ \text{cm}$", "Nếu đo L lệch thêm 1 cm, f tính ra tăng bao nhiêu cm?", round(float(DFL5), 2), "cm", 0.01,
       loi=r"Làm tròn $f$ mới thành số nguyên rồi kết luận không đổi ; phải giữ 2 chữ số thập phân khi so.",
       ke=[(r"Thế $L=126$ vào $f=\dfrac{L^2-\ell^2}{4L}$, trừ cho $f$ cũ", True),
           (r"Cho $f$ đổi $\dfrac14\ \text{cm}$ như cách 2f–2f", r"Công thức hai vị trí không tỉ lệ thuận với $L$ ; phải thế số lại."),
           (r"Chỉ đổi $L^2$ ở tử, giữ $4L$ cũ ở mẫu", r"$L$ có ở cả tử và mẫu ; đổi $L$ phải đổi cả hai.")]),
  buoc(r"Khi $\ell$ lệch thêm $1\ \text{cm}$", "Nếu đo ℓ lệch thêm 1 cm, f tính ra giảm bao nhiêu cm?", round(float(DFl5), 2), "cm", 0.01,
       loi=r"Kết luận đại lượng nào quan trọng hơn theo cảm tính ; phải so độ đổi của $f$ khi mỗi đại lượng lệch cùng $1\ \text{cm}$.",
       ke=[(r"Thế $\ell=76$, giữ $L=125$, trừ cho $f$ cũ", True),
           (r"Cho $f$ đổi đúng như khi $L$ đổi", r"$\ell$ chỉ có ở tử với dấu trừ : ảnh hưởng khác $L$, phải tính riêng."),
           (r"Thế $\ell=74$", r"Lệch thêm $1\ \text{cm}$ là $76\ \text{cm}$, không phải bớt đi.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>kính lúp</b>, <b>ngắm chừng ở cực cận</b> → ảnh ảo tại $C_c$, <b>d' = −OC_c</b> ; ở vô cực → <b>d = f</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tiêu cự", "Tiêu cự của kính lúp bằng bao nhiêu cm?", float(F6), "cm", 0.05,
       loi=r"Lấy $f=\dfrac{G}{25}$ hoặc nhân $5\cdot25$ ; nhớ $G=\dfrac{25}{f}$ với $f$ tính bằng cm."),
  buoc("Ngắm chừng ở $C_c$", "Ngắm chừng ở Cc thì vật cách kính bao nhiêu cm?", round(float(D6_CC), 2), "cm", 0.02,
       loi=r"Thế $d'=+25$ (quên ảnh ảo) ra $d\gt f$ — vô lí, vì khi đó thấu kính hội tụ cho ảnh thật.",
       ke=[(r"Ảnh ảo tại $C_c$ : thế $d'=-25\ \text{cm}$ vào công thức thấu kính", True),
           (r"Thế $d'=+25\ \text{cm}$", r"Ảnh của kính lúp là ảnh ảo, cùng phía vật, nên $d'\lt0$."),
           (r"Đặt vật tại $C_c$, tức $d=25\ \text{cm}$", r"$C_c$ là chỗ ẢNH phải hiện ra ; vật cách kính $25\ \text{cm}$ thì $d\gt f$, ảnh thật lộn ngược.")]),
  buoc("Ảnh cao gấp mấy lần vật", "Ngắm chừng ở Cc, ảnh cao gấp mấy lần vật?", float(K6_CC), "lần", 0.05,
       loi=r"Lẫn tỉ số chiều cao $|k|$ với số bội giác $G$ ghi trên kính.",
       ke=[(r"$|k|=\dfrac{|d'|}{d}$", True),
           (r"$|k|=G$", r"$G=\dfrac{25}{f}$ ứng với ngắm chừng ở vô cực, không phải tỉ số chiều cao ảnh khi ngắm ở $C_c$."),
           (r"$|k|=\dfrac{d}{|d'|}$", r"Ảnh ảo của kính lúp lớn hơn vật nên tỉ số phải lớn hơn 1 ; công thức bị đảo.")]),
  buoc("Ngắm chừng ở vô cực", "Ngắm chừng ở vô cực thì phải đặt vật ở đâu?",
       loi=r"Đặt vật ở xa vô cùng : vô cực là chỗ ẢNH hiện ra, không phải chỗ đặt vật.",
       lua_chon=[(r"Tại tiêu điểm $F$ của kính ($d=f$)", True),
                 (r"Tại $2F$ ($d=2f$)", r"Vật tại $2F$ cho ảnh thật bằng vật ở phía bên kia kính ; mắt sát kính không nhìn được ảnh đó."),
                 (r"Sát kính ($d$ gần bằng 0)", r"Vật sát kính cho ảnh ảo gần như trùng vật, gần mắt hơn $C_c$ : mắt không nhìn rõ.")],
       ke=[(r"Tìm $d$ để $\dfrac1{d'}=0$", True),
           (r"Thế $d'=-25\ \text{cm}$ lần nữa", r"Đó là ngắm chừng ở $C_c$ ; ở vô cực thì ảnh ở rất xa, không ở $C_c$."),
           (r"Lấy $d$ bằng số $G$", r"$G$ là số bội giác, không có đơn vị, không phải khoảng cách.")]),
  buoc("Khoảng đặt vật", "Khoảng xê dịch của vật dài bao nhiêu mm?", round(float(XD6_MM), 2), "mm", 0.1,
       loi=r"Quên đổi cm sang mm ; hoặc lấy cả khoảng từ sát kính tới $F$.",
       ke=[(r"Hiệu hai vị trí giới hạn : $f-d_{C_c}$, rồi đổi ra mm", True),
           (r"Lấy $f$ làm khoảng xê dịch", r"Vật gần hơn vị trí ngắm $C_c$ thì ảnh vào trong $C_c$, mắt không nhìn rõ ; không đặt được từ sát kính."),
           (r"Lấy $OC_c-f$", r"Đó là hiệu khoảng cách ảnh và tiêu cự, không phải khoảng đặt vật.")]),
  buoc("Ảnh của vết xước", "Ngắm chừng ở Cc, ảnh của vết xước dài bao nhiêu mm?", float(H6P), "mm", 0.05,
       loi=r"Nhân với $G$ thay vì $|k|$ ở $C_c$.",
       ke=[(r"Nhân chiều dài vết xước với $|k|$ khi ngắm ở $C_c$", True),
           (r"Nhân với $G$", r"$G$ chỉ đúng khi ngắm chừng ở vô cực ; ở $C_c$ phải dùng $|k|$."),
           (r"Chia cho $|k|$", r"Ảnh qua kính lúp lớn hơn vật nên phải nhân.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 7 ──
 dict(nhan_dang=r"Thấy <b>hai thấu kính đồng trục</b> → <b>ảnh qua TK₁ là vật của TK₂</b>, $d_2=a-d_1'$, đếm ảnh thật",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Ảnh qua $TK_1$", "Ảnh qua TK₁ cách TK₁ bao nhiêu cm?", float(D7_1P), "cm", 0.2,
       loi=r"Nhớ nhầm $\dfrac1{d'}=\dfrac1f+\dfrac1d$, ra ảnh gần thấu kính hơn tiêu cự — vô lí với ảnh thật."),
  buoc("Vật của $TK_2$", "Khoảng cách d₂ từ ảnh trung gian tới TK₂ bằng bao nhiêu cm?", float(D7_2A), "cm", 0.1,
       loi=r"Lấy $d_2=a$ (bẫy : quên ảnh trung gian), hoặc cộng thay vì trừ $d_1'$.",
       ke=[(r"$d_2=a-d_1'$", True),
           (r"$d_2=a$", r"Vật của $TK_2$ là ảnh $A_1'B_1'$, không phải vật $AB$ ban đầu ; phải trừ $d_1'$."),
           (r"$d_2=a+d_1'$", r"Ảnh thật $A_1'B_1'$ nằm giữa hai thấu kính nên gần $TK_2$ hơn $a$, không xa hơn.")]),
  buoc("Ảnh qua $TK_2$", "Với TK₂ phân kì, d₂' bằng bao nhiêu cm (ghi cả dấu)?", float(D7_2AP), "cm", 0.1,
       loi=r"Quên $f_2\lt0$ : thế $f_2$ dương thì $d_2=f_2$, ảnh ở vô cực — vô lí với thấu kính phân kì.",
       ke=[(r"$d_2'=\dfrac{d_2f_2}{d_2-f_2}$ với $f_2\lt0$", True),
           (r"Thế $f_2$ dương", r"Thấu kính phân kì có $f\lt0$ ; thế $f_2$ dương là coi nó là thấu kính hội tụ."),
           (r"$d_2'=\dfrac{d_2f_2}{d_2+f_2}$", r"Sai dấu ở mẫu : từ $\dfrac1f=\dfrac1d+\dfrac1{d'}$ ra $d'=\dfrac{df}{d-f}$.")]),
  buoc("Chiều cao và chiều của ảnh cuối", "Ảnh cuối cao bao nhiêu cm?", float(H7_2A), "cm", 0.05,
       loi=r"Kết luận ảnh cuối cùng chiều vật vì ảnh của thấu kính phân kì cùng chiều — quên ảnh trung gian đã ngược chiều.",
       ke=[(r"$h_2'=h\cdot\dfrac{|d_1'|}{d_1}\cdot\dfrac{|d_2'|}{d_2}$", True),
           (r"$h_2'=h\cdot\dfrac{|d_2'|}{d_2}$", r"Quên ảnh trung gian đã phóng to ; phải nhân cả tỉ số của $TK_1$."),
           (r"$h_2'=h\cdot\dfrac{|d_1'|}{d_1}$", r"Đó mới là ảnh trung gian ; $TK_2$ còn làm chiều cao đổi tiếp.")]),
  buoc("⭐⭐⭐ Ghép sát : vật ảo của $TK_2$", "Ghép sát: d₂ của TK₂ bằng bao nhiêu cm (ghi cả dấu)?", float(D7_2B), "cm", 0.2,
       loi=r"Coi điểm hội tụ $A_1'$ là vật thật (bỏ dấu trừ) : kết quả không khớp kết luận hệ như tấm kính phẳng.",
       ke=[(r"$d_2=a-d_1'$ với $a=0$ : âm, vật ảo", True),
           (r"$d_2=d_1$", r"Vật của $TK_2$ là ảnh qua $TK_1$, không phải $AB$."),
           (r"$d_2=+d_1'$, vật thật", r"Chùm tia gặp $TK_2$ trước khi hội tụ ; điểm hội tụ nằm SAU $TK_2$ nên là vật ảo, $d_2\lt0$.")]),
  buoc("Ảnh qua $TK_2$ khi ghép sát", "Ghép sát: d₂' bằng bao nhiêu cm (ghi cả dấu)?", float(D7_2BP), "cm", 0.2,
       loi=r"Thế $d_2$ dương ; hoặc đi tìm công thức riêng cho vật ảo thay vì dùng lại một công thức.",
       ke=[(r"Thế $d_2\lt0$ vào $\dfrac1{f_2}=\dfrac1{d_2}+\dfrac1{d_2'}$", True),
           (r"Lấy luôn $A_1'B_1'$ làm ảnh cuối", r"$TK_2$ chặn chùm tia trước khi hội tụ nên $A_1'B_1'$ không còn là ảnh thật."),
           (r"Dùng công thức đổi dấu riêng cho vật ảo", r"Không cần công thức mới : một công thức cho mọi trường hợp, chỉ cần thế $d_2$ có dấu.")]),
  buoc("Đặt $TK_2$ hội tụ", "Phải đặt TK₂ hội tụ cách TK₁ bao nhiêu cm?", float(A7C), "cm", 0.2,
       loi=r"Quên tỉ số của $TK_1$ đã bằng 2 nên cho $TK_2$ phóng to tiếp ; hoặc lấy $a=d_2$.",
       ke=[(r"Ảnh trung gian đã gấp đôi vật ⇒ $TK_2$ cho ảnh thật bằng vật : $d_2=2f_2$", True),
           (r"Cho $TK_2$ cũng phóng to gấp đôi", r"Tỉ số của hệ là tích hai tỉ số ; $TK_1$ đã gấp đôi nên $TK_2$ chỉ được cho ảnh bằng vật."),
           (r"Đặt $TK_2$ cách $TK_1$ đúng $2f_2$", r"$d_2$ đo từ ảnh trung gian tới $TK_2$, không phải từ $TK_1$ : $a=d_1'+d_2$.")]),
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
    near = lambda a, b, e: abs(float(a) - float(b)) <= e
    # D4 (nguon.md)
    assert (D4_1P, D4_2P, D4_3P) == (F(45, 2), 30, 60) and L4 == [F(135, 2), 60, 80]
    assert DICH4_1 == F(15, 2) and DICH4_2 == 30 and LMIN4 == 60 and min(L4) == LMIN4
    assert H4 * kabs(D4_1, D4_1P) == 1 and H4 * kabs(D4_2, D4_2P) == 2 and H4 * kabs(D4_3, D4_3P) == 6
    assert D4_1 * F4 / (D4_1 + F4) != D4_1P                                              # sai dấu ở mẫu
    assert anh(F4, D4_1 + 15) - D4_1P != DICH4_1 and F(15) != DICH4_1                    # bước 2: hai lựa chọn sai
    assert anh(F4, D4_1 - 10) - D4_2P != DICH4_2 and D4_3P - D4_1P != DICH4_2            # bước 3
    # D4c: (d1 − f) = 2(d1 − 5 − f) ⇒ d1 − f = 10 ; f²/10 = 10
    x = F(10); assert x == 2 * (x - 5) and X4C == x
    assert F4C**2 / 5 - F4C**2 / 10 == 10 and (D4C1, D4C2) == (20, 15)
    assert D4C2P - D4C1P == 10 and kabs(D4C2, D4C2P) / kabs(D4C1, D4C1P) == 2 and D4C1P > 0 and D4C2P > 0
    # D5
    assert F5 == 20 and (D5_1, D5_2) == (25, 100) and anh(F5, D5_1) == 100 and anh(F5, D5_2) == 25
    assert H5_1 == 8 and H5_2 == F(1, 2) and H5_1 * H5_2 == H5**2 and LMIN5 == 80 and 70 < LMIN5 < L5
    assert near(LTB5, 80.1, 1e-9) and near(DL5, 0.4, 1e-9) and near(FTB5, 20.025, 1e-9) and near(DF5, 0.1, 1e-9)
    assert near(DFL5, 0.339, 0.001) and near(DFl5, 0.302, 0.001) and DFL5 > DFl5
    assert round(float(DFL5), 2) == 0.34 and round(float(DFl5), 2) == 0.30
    assert (L5 - l5) / 4 != F5 and l5 / 2 != F5                                          # bước 1 sai
    assert H5 * D5_1 / (L5 - D5_1) != H5_1 and H5 * (L5 - l5) / l5 != H5_1               # bước 2 sai
    assert abs(float(F(1, 4)) - float(DFL5)) > 0.01 and abs(float(((L5 + 1)**2 - l5**2) / (4 * L5) - F5) - float(DFL5)) > 0.01   # bước 6 sai
    assert abs(float(F5 - (L5**2 - (l5 - 1)**2) / (4 * L5)) - float(DFl5)) > 0.01 or (L5**2 - (l5 - 1)**2) / (4 * L5) > F5    # bước 7 sai
    assert abs(float(DL5) - float(DF5)) > 0.02 and abs(float(max(LS5) - min(LS5)) / 4 - float(DF5)) > 0.02                 # bước 5 sai
    # D6
    assert F6 == 5 and D6_CC == F(25, 6) and round(float(D6_CC), 2) == 4.17 and K6_CC == 6
    assert D6_V == F6 and XD6_MM == F(25, 3) and round(float(XD6_MM), 1) == 8.3 and H6P == F(12, 5)
    assert anh(F6, D6_CC) == -CC6 and 1 / (1 / F6 - 1 / CC6) > F6                          # d' = +25 cho d > f (vô lí)
    assert G6 != K6_CC and G6 * H6 != H6P and F6 * 10 != XD6_MM and (CC6 - F6) * 10 != XD6_MM
    # D7
    assert D7_1P == 60 and H7_1 == 4 and D7_2A == 20 and D7_2AP == -10 and H7_2A == 2 and A7A + D7_2AP == 70
    assert INV7B == 0 and D7_2B == -60 and D7_2BP == -30 and -D7_2BP == D7_1
    assert kabs(D7_1, D7_1P) * kabs(D7_2B, D7_2BP) == 1
    assert A7C == 100 and D7_2CP == 40 and kabs(D7_1, D7_1P) * kabs(D7_2C, D7_2CP) == 2
    assert anh(F(20), D7_2A) is None                                                      # thế f₂ dương: ảnh ở vô cực
    assert A7A != D7_2A and A7A + D7_1P != D7_2A                                         # bước 2 sai
    assert H7 * kabs(D7_2A, D7_2AP) != H7_2A and H7_1 != H7_2A                           # bước 4 sai
    assert anh(F(20), 30) != 40 and 2 * F7_2C != A7C                                       # bước 7 sai (TK2 gấp đôi: d2=30 ⇒ a=90)
    # cấp/fading/số bước
    for n, s in enumerate(STEPS):
        assert len(s["buoc"]) == SOLS[n].count('class="bt-step"'), n
    assert [s["cap_do"] for s in STEPS] == [3, 3, 3, 4]
    # bảng phân tích: cột 1 trích nguyên văn đề
    for n, rows in enumerate(_RAW_ANALYSIS):
        for r in rows:
            assert r[0].strip('"') in _RAW_DANG[n]["problem_html"], (n, r[0])
    # không lộ đáp số trong đề, hình, bảng, câu hỏi, lựa chọn, lỗi hay gặp
    lo = {0: ["22{,}5", "22,5", "7{,}5", "7,5", "67{,}5", "67,5", "L_{min}=60", "= 60"],
          1: ["f=20", "f = 20", "0{,}5", "0,5", "0{,}34", "0{,}3", "80{,}1", "20{,}0", "= 80", "8 cm"],
          2: ["4{,}17", "4,17", "4{,}2", "8{,}3", "8,3", "2{,}4", "2,4", "f = 5", "f=5", "= 6"],
          3: ["= 60", "-10", "−10", "= 100", "100 cm", "-30", "−30", "-60", "−60", "70 cm"]}
    for n in range(4):
        figs = re.sub(r"<[^>]+>", " ", BUILD[n](0) + BUILD[n](2))
        blob = DANG[n]["problem_html"] + figs + str(ANALYSIS[n]) + STEPS[n]["nhan_dang"]
        for s in STEPS[n]["buoc"]:
            blob += s.get("tieu_de", "") + s.get("hoi", "") + s.get("loi_hay_gap", "")
            for c in s.get("chon_buoc_ke", []) + s.get("lua_chon", []):
                blob += c["text"] + c.get("vi_sao", "")
        for x in lo[n]:
            assert x not in blob, (n, x)
    # mô phỏng dưới đề: không vẽ ảnh (màu đỏ chỉ dùng cho chữ hỏi), không dừng ở vị trí đáp án
    for n in range(4):
        h = BUILD[n](0)
        assert f'stroke="{RED}"' not in h and "A_{1}" not in h and "A'B'" not in h, n
    h6 = BUILD[2](0)
    assert f"{-S6 * float(D6_CC):.1f} 0" not in h6 and "C_{c}:" not in h6
    assert not (D6_CC <= F(D6_END) <= D6_V) and f"{-S6 * D6_END:.1f} 0" in h6       # khung cuối ngoài khoảng đặt vật
    h5 = BUILD[1](0)
    assert all(f"{S5 * float(x):.1f} 0" not in h5 for x in (D5_1, D5_2))
    # SVG: chữ ≥ 14, không marker
    for n in range(4):
        for k in (0, 2):
            h = BUILD[n](k)
            assert "marker-end" not in h
            assert all(int(z) >= 14 for z in re.findall(r'<text[^>]*font-size="(\d+)"', h)), (n, k)
    # không ký tự điều khiển (chuỗi thường "\text" → TAB + "ext")
    import json as _j
    src = open(os.path.abspath(__file__), encoding="utf8").read()
    blob = _j.dumps([DANG, ANALYSIS, SOLS, STEPS] + [BUILD[n](k) for n in range(4) for k in (0, 2)], ensure_ascii=False)
    assert not re.search(r"[\x00-\x08\x0b-\x1f]", blob) and "\\t" not in blob.replace("\\\\", ""), "ký tự điều khiển"
    assert not re.search(r"[\x00-\x08\x0b-\x1f]", src)
    # D7b: k = −d'/d cho từng thấu kính; k₂ = −1/2 (ảnh ảo mà vẫn đảo chiều vì vật ảo), k_hệ = 1
    assert -D7_1P / D7_1 == -2 and -D7_2BP / D7_2B == F(-1, 2) and (-D7_1P / D7_1) * (-D7_2BP / D7_2B) == 1
    print("btm156_d456: kiểm số liệu đạt")


if __name__ == "__main__":
    kiem_so()
