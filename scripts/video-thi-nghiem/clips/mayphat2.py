# Clip: tn-l12-mayphatdien-02 - Ba cuon day lech 120 do quanh MOT nam cham quay
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-mayphatdien-02.json:
#   tham_so: U0 = 6 V moi pha, lech_pha 120 do, f_quay mac dinh 1 vong/s (p = 1 -> f = 1 Hz, T = 1 s).
#   so_lieu_mau (6 hang): t = 0 ; 0,083 ; 0,167 ; 0,25 ; 0,333 ; 0,417 s va u1, u2, u3 ; tong ba cot = 0 (ghi_chu cua kho).
#   mo_hinh: u1 = U0.cos(2.pi.f.t), u2 = U0.cos(2.pi.f.t - 2.pi/3), u3 = U0.cos(2.pi.f.t + 2.pi/3).
# Ban 2 (26/11/2026, viec 4 lo 32, cong --do-chu moi):
#   Du doan (K10 khong ve nut; khung web hoi A-D): quay 1 vong/s, den 1 vua sang nhat -> bao lau sau den 2 sang nhat?
#     A. 0 s (cung luc)  B. 0,25 s (lech 90 do)  C. 1/3 s (dung, u2 dat dinh tai t = 1/3 s)  D. 0,5 s (lech 180 do)
#     -> danh hien_tuong_hay_sai #2 (90/180 do). Cau 3 trong bai hoi "dac diem ba suat dien dong" (dinh tinh): khong trung so.
#   Bay: "ba pha = ba tan so?" (hien_tuong_hay_sai #1): hinh ba song khac tan so canh ba song do duoc cung chu ki.
#   Chot (khung web hoi A-D, dap so KHONG hien): dao chieu quay nam cham -> sau den 1 la den 3 (thu tu 1 -> 3 -> 2).
#     Ca suy tu mo hinh: e_k ~ -sin(phi - theta_k) khi phi giam; khong co hang do dao chieu trong kho.
# Vat li: tu thong qua cuon k ~ cos(phi - theta_k) -> e_k ~ sin(phi - theta_k), phi = theta_1 + 90 + 360.f.t
#   -> u1 = 6.cos(2.pi.t), u2 = 6.cos(2.pi.t - 120), u3 = 6.cos(2.pi.t + 120) dung mo_hinh. LED sang khi u_k > U0/2.
# Toa do mp4 = 65 + 0,88.x; chu than canh ve >= 56 px (ra >= 49 px).
from engine import *

U0 = 6.0
ROWS = [("0", "6,0", "−3,0", "−3,0"), ("0,083", "5,2", "0,0", "−5,2"), ("0,167", "3,0", "3,0", "−6,0"),
        ("0,25", "0,0", "5,2", "−5,2"), ("0,333", "−3,0", "6,0", "−3,0"), ("0,417", "−5,2", "5,2", "0,0")]
assert all(abs(sum(float(v.replace(",", ".").replace("−", "-")) for v in r[1:])) < 1e-9 for r in ROWS)
PH = (ORANGE, TEAL, PURPLE)                    # mau pha 1, 2, 3
COP, COP_D = (196, 120, 52), (130, 72, 28)
TH = (-90.0, 30.0, 150.0)                      # goc dat cuon 1, 2, 3 tren man (do, chieu kim dong ho, -90 = dinh)
DARK_OR = (181, 71, 8)

def u_k(k, ts): return U0 * math.cos(2 * math.pi * ts - 2 * math.pi * k / 3)          # ts: thoi gian mo phong (s), f = 1 Hz
def phi_deg(ts): return TH[0] + 90 + 360 * ts                                          # huong cuc N
assert abs(math.sin(math.radians(phi_deg(0.2) - TH[1])) * U0 - u_k(1, 0.2)) < 1e-9     # e_k ~ sin(phi - theta_k)
assert abs(u_k(1, 1 / 3) - U0) < 1e-9                                                  # den 2 dat dinh sau 1/3 s

def chev(d, x, y, ang, color, L=16, w=4):
    for s in (1, -1):
        a = ang + math.pi - s * math.radians(30)
        d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=color, width=w)

# ---------------- nam cham thang chuan (port PIL tu bar_magnet / svg_lib.py), xoay goc ang ----------------
UM_EDGE = (51, 65, 85)
UM_N = ((220, 38, 38), (248, 113, 113), (185, 28, 28))
UM_S = ((37, 99, 235), (96, 165, 250), (30, 64, 175))

def bar_magnet_pil(d, cx, cy, L, H, ang=0.0, dep=(10, -7), fs=56, sw=4):
    r = math.radians(ang); ca, sa = math.cos(r), math.sin(r); dx, dy = dep
    P = lambda u, v: (cx + u * ca - v * sa, cy + u * sa + v * ca)
    h, l = H / 2, L / 2
    edges = [((0, -h), (l, -h), UM_N, (0, -1)), ((-l, -h), (0, -h), UM_S, (0, -1)),
             ((0, h), (l, h), UM_N, (0, 1)), ((-l, h), (0, h), UM_S, (0, 1)),
             ((l, -h), (l, h), UM_N, (1, 0)), ((-l, -h), (-l, h), UM_S, (-1, 0))]
    for a, b, pal, (nu, nv) in edges:
        nx, ny = nu * ca - nv * sa, nu * sa + nv * ca
        if nx * dx + ny * dy <= 0: continue
        pa, pb = P(*a), P(*b)
        col = pal[1] if -ny > 0.5 else pal[2]
        d.polygon([pa, pb, (pb[0] + dx, pb[1] + dy), (pa[0] + dx, pa[1] + dy)], fill=col, outline=UM_EDGE, width=sw)
    d.polygon([P(0, -h), P(l, -h), P(l, h), P(0, h)], fill=UM_N[0], outline=UM_EDGE, width=sw)
    d.polygon([P(-l, -h), P(0, -h), P(0, h), P(-l, h)], fill=UM_S[0], outline=UM_EDGE, width=sw)
    text(d, P(l / 2, 0), "N", fs, WHITE); text(d, P(-l / 2, 0), "S", fs, WHITE)

# ---------------- duong suc cua nam cham thang ----------------
ML, MHH = 230, 66
def _trace(ang):
    a = ML / 2 - 14; nx, sx = a, -a
    x, y = nx + 6 * math.cos(ang), -6 * math.sin(ang); pts = [(x, y)]
    for _ in range(3000):
        ex = ey = 0.0
        for px, q in ((nx, 1), (sx, -1)):
            ddx, ddy = x - px, y; r3 = (ddx * ddx + ddy * ddy) ** 1.5; ex += q * ddx / r3; ey += q * ddy / r3
        n = math.hypot(ex, ey); x += 3 * ex / n; y += 3 * ey / n; pts.append((x, y))
        if math.hypot(x - sx, y) < 8: break
    return pts
FIELD = [_trace(math.radians(a)) for a in (96, 135)]

def field(d, cx, cy, ang, a=1.0):
    r = math.radians(ang); ca, sa = math.cos(r), math.sin(r); c = A(PURPLE, 0.75 * a)
    for ln in FIELD:
        for sg in (1, -1):
            pts = [(cx + u * ca - sg * v * sa, cy + u * sa + sg * v * ca) for u, v in ln]
            d.line(pts, fill=c, width=5, joint="curve")
            k = max(range(len(ln)), key=lambda n: abs(ln[n][1]))
            (x0, y0), (x1, y1) = pts[max(0, k - 3)], pts[min(len(pts) - 1, k + 3)]
            chev(d, pts[k][0], pts[k][1], math.atan2(y1 - y0, x1 - x0), A(PURPLE, 0.8 * a))

# ---------------- stato: vong nhua + ba cuon day ----------------
RCX, RCY, RR = 390, 590, 205
def coil(d, k, cx0=RCX, cy0=RCY, rr=RR, sc=1.0):
    th = math.radians(TH[k]); ux, uy = math.cos(th), math.sin(th); tx, ty = -uy, ux
    cx, cy = cx0 + rr * ux, cy0 + rr * uy
    Q = lambda s, h: (cx + sc * (s * tx + h * ux), cy + sc * (s * ty + h * uy))
    d.polygon([Q(-62, -30), Q(62, -30), Q(62, 30), Q(-62, 30)], fill=COP, outline=NAVY, width=4)
    for s in range(-50, 56, 13):
        d.line([Q(s, -30), Q(s + 6, 30)], fill=COP_D, width=3)
    bx, by = cx0 + (rr + 82 * sc) * ux, cy0 + (rr + 82 * sc) * uy
    dot(d, bx, by, 36, PH[k], outline=WHITE)
    text(d, (bx, by), str(k + 1), 56, WHITE)

def ring(d, cx, cy, rr):
    d.ellipse([cx - rr - 14, cy - rr - 14, cx + rr + 14, cy + rr + 14], outline=(203, 213, 225), width=28)
    d.ellipse([cx - rr - 14, cy - rr - 14, cx + rr + 14, cy + rr + 14], outline=NAVY, width=3)
    d.ellipse([cx - rr + 14, cy - rr + 14, cx + rr - 14, cy + rr - 14], outline=NAVY, width=3)

def stator(d, show120=False):
    ring(d, RCX, RCY, RR)
    if show120:
        r = RR + 36
        d.arc([RCX - r, RCY - r, RCX + r, RCY + r], TH[0] + 16, TH[1] - 16, fill=NAVY, width=5)
        a = math.radians(-30); text(d, (RCX + (RR + 104) * math.cos(a), RCY + (RR + 104) * math.sin(a)), "120°", 56, NAVY)

def leds(d, lit):
    for k in range(3):
        y = 400 + k * 175
        b = lit[k]
        if b > 0:
            for j in range(6, 0, -1): dot(d, 910, y, 42 + j * 11, A((250, 204, 21), 0.09 * b))
        dot(d, 910, y, 46, mix((235, 235, 235), (255, 236, 140), b), outline=NAVY)
        dot(d, 795, y, 36, PH[k], outline=WHITE); text(d, (795, y), str(k + 1), 56, WHITE)

def led_lit(ts): return [clamp((u_k(k, ts) / U0 - 0.5) / 0.5) for k in range(3)]

def spin(d, cx, cy, r, cw=True, a0=0.0, a=1.0, w=9, L=28):
    """Mui ten cung chi chieu quay; a0 (do) xoay ca mui ten de hinh khong dung yen."""
    if cw:
        s0, s1 = -130 + a0, -60 + a0; ae = math.radians(s1); dirn = ae + math.pi / 2
    else:
        s0, s1 = -120 - a0, -50 - a0; ae = math.radians(s0); dirn = ae - math.pi / 2
    d.arc([cx - r, cy - r, cx + r, cy + r], s0, s1, fill=A(ORANGE, a), width=w)
    chev(d, cx + r * math.cos(ae), cy + r * math.sin(ae), dirn, A(ORANGE, a), L=L, w=w)

def rig(d, ts, lit, show120=False, spin_arrow=False):
    card(d, (40, 250, 1040, 890), fill=WHITE, outline=LIGHT, w=3)
    ang = phi_deg(ts)
    field(d, RCX, RCY, ang)
    stator(d, show120)
    for k in range(3): coil(d, k)
    bar_magnet_pil(d, RCX, RCY, ML, MHH, ang)
    dot(d, RCX, RCY, 9, NAVY)
    if spin_arrow: spin(d, RCX, RCY, 150)
    leds(d, lit)

# ---------------- do thi ba suat dien dong ----------------
GX0, GX1 = 180, 980
def graph(d, y0, y1, kx, cursor=None, ticks=False, peaks=0.0, a=1.0):
    yc, s = (y0 + y1) / 2, ((y1 - y0) / 2 - 20) / U0
    X = lambda ts: GX0 + (GX1 - GX0) * ts
    for v in (6, -6):
        d.line([(GX0, yc - s * v), (GX1, yc - s * v)], fill=A((236, 232, 222), a), width=2)
        text(d, (GX0 - 14, yc - s * v), "6" if v > 0 else "−6", 56, INK, anchor="rm", alpha=a)
    d.line([(GX0, yc), (GX1 + 22, yc)], fill=A(NAVY, a), width=4)
    d.line([(GX0, y1), (GX0, y0)], fill=A(NAVY, a), width=4)
    text(d, (GX0 - 14, yc), "0", 56, INK, anchor="rm", alpha=a)
    if ticks:
        for j, lab in ((1, "T/3"), (2, "2T/3"), (3, "T")):
            x = X(j / 3); d.line([(x, yc - 12), (x, yc + 12)], fill=A(NAVY, a), width=4)
            text(d, (x - (20 if j == 3 else 0), yc + 48), lab, 56, INK, alpha=a)
    else:
        d.line([(X(1), y1 - 6), (X(1), y1 + 6)], fill=A(NAVY, a), width=4)
        text(d, (X(1), y1 + 40), "1 s", 56, INK, alpha=a)
    m = int(240 * clamp(kx))
    for k in range(3):
        if m > 1:
            pts = [(X(j / 240), yc - s * u_k(k, j / 240)) for j in range(m + 1)]
            d.line(pts, fill=A(PH[k], a), width=7, joint="curve")
        if peaks > 0:
            x = X(k / 3); dot(d, x, yc - s * U0, 15, A(PH[k], peaks * a), outline=A(WHITE, peaks * a))
            yy = y0 + 8
            while yy < yc:
                d.line([(x, yy), (x, min(yy + 12, yc))], fill=A(PH[k], peaks * a), width=4); yy += 22
    if cursor is not None:
        d.line([(X(cursor), y0), (X(cursor), y1)], fill=A(NAVY, 0.6 * a), width=4)
    return X, yc, s

# ---------------- canh 1: mo bai + du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    rig(d, 0.0, led_lit(0.0), spin_arrow=True)        # khong ghi 120 do o hook (cong B: 120/360 lo 1/3 s)        # t = 0: den 1 sang nhat (u1 = 6 V)
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 930 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 180), "Quay 1 vòng/s.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Đèn 1 vừa sáng nhất.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 350), "Bao lâu sau tới đèn 2?", 60, INK, alpha=a)
    tc, te = M[1] + 0.3, sc["T"] - 0.1                  # thanh dem lien, cao 120 px
    p = clamp((t - tc) / (te - tc))
    d.rounded_rectangle([110, y0 + 415, 970, y0 + 535], radius=24, fill=A(LIGHT, a))
    if p < 1: d.rounded_rectangle([110, y0 + 415, 110 + 860 * (1 - p), y0 + 535], radius=24, fill=A(PURPLE, a))

# ---------------- canh 2: tien hanh ----------------
SLOW = 0.4                                     # chieu cham: 1 s that -> 2,5 s tren man
def ts_do(t): return max(0.0, (t - 0.6) * SLOW)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    ts = ts_do(t)
    rig(d, ts, led_lit(ts) if t > 0.6 else [0, 0, 0])
    card(d, (40, 920, 1040, 1480), fill=WHITE, outline=LIGHT, w=3)
    text(d, (70, 975), "Dao động kí", 56, INK, anchor="lm")
    for k, x in enumerate((640, 790, 940)): text(d, (x, 975), f"e{k + 1}", 60, PH[k])
    graph(d, 1060, 1400, ts, cursor=(ts % 1.0) if ts > 0 else None)

# ---------------- canh 3: dap an + tong bang 0 ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    b = 1.0                                       # hien cung do thi (mot khoi chu luc 0 s)
    pw = tw(d, "ĐÁP ÁN: 1/3 s", F(60)) + 70
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 342), fill=A(GREEN, b), r=40)
    text(d, (W / 2, 302), "ĐÁP ÁN: 1/3 s", 60, WHITE, alpha=b)
    card(d, (40, 372, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    text(d, (1010, 410), "T = 1 s", 56, INK, anchor="rm")
    ki = appear(t, M[1] - 0.1, 0.3)
    i = min(5, max(0, int((t - M[1] - 0.2) / 0.62)))
    X, yc, s = graph(d, 450, 800, 1.0, ticks=True, peaks=appear(t, 0.8) * (1 - ki),
                     cursor=float(ROWS[i][0].replace(",", ".")) if ki > 0.5 else None)
    kc = appear(t, M[0] + 2.4)
    text(d, (W / 2, 862), "cùng biên độ, cùng chu kì", 56, INK, alpha=kc)
    if ki <= 0: return
    tt = float(ROWS[i][0].replace(",", "."))
    for k in range(3):
        dot(d, X(tt), yc - s * u_k(k, tt), 14, A(PH[k], ki), outline=A(WHITE, ki))
    card(d, (40, 940, 1040, 1560), fill=A(WHITE, ki), outline=A(NAVY, ki), w=4)
    text(d, (W / 2, 1010), f"t = {ROWS[i][0]} s", 60, NAVY, alpha=ki)
    cols = (165, 375, 585, 845)
    for j, (h, col) in enumerate(zip(("e1", "e2", "e3", "tổng (V)"), PH + (GREEN,))):
        text(d, (cols[j], 1110), h, 60, col, alpha=ki)
    d.line([(70, 1160), (1010, 1160)], fill=A(NAVY, ki), width=3)
    for j in range(3):                                   # dau cua so sau dat o o phan cach: 3,0 + 3,0 − 6,0 = 0
        v = ROWS[i][j + 1]
        text(d, (cols[j], 1240), v.lstrip("−") if j > 0 else v, 64, INK, alpha=ki)
    for j in range(3):
        sg = "=" if j == 2 else ("−" if ROWS[i][j + 2].startswith("−") else "+")
        text(d, ((cols[j] + cols[j + 1]) / 2 + 6, 1240), sg, 64, NAVY, alpha=ki)
    d.rounded_rectangle([cols[3] - 90, 1185, cols[3] + 90, 1295], radius=18, fill=A((220, 252, 231), ki))
    text(d, (cols[3], 1240), "0", 66, GREEN, alpha=ki)
    kz = appear(t, M[1] + 3.2)
    text(d, (W / 2, 1420), "Tổng luôn bằng 0", 64, GREEN, alpha=kz)

# ---------------- canh 4: Bay - ba pha = ba tan so? ----------------
def waves(d, box, freqs, a=1.0, marks=False):
    x0, y0, x1, y1 = box; yc = (y0 + y1) / 2; amp = (y1 - y0) / 2 - 22
    d.line([(x0, yc), (x1, yc)], fill=A(NAVY, a), width=3)
    for k, f in enumerate(freqs):
        pts = [(x0 + (x1 - x0) * j / 200, yc - amp * math.cos(2 * math.pi * f * j / 200 - 2 * math.pi * k / 3)) for j in range(201)]
        d.line(pts, fill=A(PH[k], a), width=6, joint="curve")
    if marks:                                   # vach moi chu ki: ca ba lap lai cung luc
        for j in (0.5, 1.0):
            x = x0 + (x1 - x0) * j; yy = y0
            while yy < y1:
                d.line([(x, yy), (x, min(yy + 14, y1))], fill=A(NAVY, a), width=4); yy += 26

def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    b1, b2, b3 = (m - 0.1 for m in sc["M"])
    k1, k2, k3 = appear(t, b1, 0.4), appear(t, b2, 0.4), appear(t, b3, 0.4)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 260, W / 2 + pw / 2, 336), fill=A(RED, k1), r=38)
    text(d, (W / 2, 298), "BẪY", 56, WHITE, alpha=k1)
    text(d, (W / 2, 420), "Ba pha là ba tần số?", 64, RED, alpha=k1)
    card(d, (40, 490, 1040, 860), fill=A(WHITE, k1), outline=A(RED, k1), w=4)
    if k1 > 0: waves(d, (120, 520, 1000, 830), (1, 1.5, 2), a=k1)          # 3 song khac tan so (sai)
    if k3 > 0:
        d.line([(80, 520), (1000, 830)], fill=A(RED, 0.85 * k3), width=10)
        d.line([(1000, 520), (80, 830)], fill=A(RED, 0.85 * k3), width=10)
    if k2 <= 0: return
    card(d, (40, 900, 1040, 1300), fill=A(WHITE, k2), outline=A(GREEN, k2), w=4)
    text(d, (200, 950), "Đo được", 64, DGREEN_, alpha=k2)
    waves(d, (120, 990, 1000, 1280), (2, 2, 2), a=k2, marks=True)
    if k3 > 0:
        card(d, (40, 1340, 1040, 1500), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1420), "Một nam châm: chung T", 64, DGREEN_, alpha=k3)
DGREEN_ = (21, 128, 61)

# ---------------- canh 5: chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Nối sao hay tam giác?", "• Điện áp giữa hai dây pha?")):
        text(d, (100, 600 + j * 260), s, 64, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 800), "?", 260, NAVY, alpha=k * (1 - kb))

# ---------------- canh 6: THU NGHI (cau_chot cua khung; dap an KHONG hien) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.3, 0.5)
    card(d, (40, 260, 1040, 1180), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 285, W / 2 + pw / 2, 365), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 325), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 450), "Đảo chiều quay nam châm.", 62, INK, alpha=k)
    text(d, (W / 2, 540), "Sau đèn 1, đèn nào sáng?", 62, DARK_OR, alpha=k)
    # stato nho, nam cham dung yen huong len cuon 1, mui ten nguoc chieu kim dong ho xoay nhe (khong lo den)
    cx, cy, rr = W / 2, 860, 175
    ring(d, cx, cy, rr)
    for kk in range(3): coil(d, kk, cx, cy, rr, 0.85)
    bar_magnet_pil(d, cx, cy, 200, 58, 0)                 # nam ngang nhu khung dau (den 1 sang nhat)
    spin(d, cx, cy, 112, cw=False, a0=25 * math.sin(1.6 * t), a=k, w=14, L=42)
    kh = appear(t, 3.3, 0.5)
    if kh > 0:
        card(d, (90, 1230, 990, 1380), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1305), "Gợi ý: nhìn chiều quay.", 60, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, g, e = (sc[k] for k in ("hook", "do", "ans", "bay", "gioi", "end"))
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + 0.6, "tap"),
            (an["t0"] + 0.2, "ding"), (an["t0"] + an["M"][1] - 0.1, "tap"),
            (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
            (g["t0"] + 2.4, "tap"), (e["t0"] + 0.3, "open")]

CLIP = dict(id="tn-l12-mayphatdien-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Máy phát điện xoay chiều · thachlab.id.vn", scenes=[
 dict(key="hook", title="Ba cuộn dây, một nam châm", draw=s_hook, tail=0.3, caps=[
   ("Mỗi cuộn nối một đèn.", 3.0),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Quay chậm, nhìn thứ tự đèn.", 3.4),
   ("Mỗi vòng quay là một chu kì.", 4.2)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("Đỉnh sau trễ T/3.", 3.6),
   ("Cộng ba e ở mỗi lúc.", 4.6)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("So với đồ thị đo.", 3.0),
   ("Cùng chu kì, đỉnh lệch nhau.", 3.4)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Chưa trả lời được:", 4.6)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 6.8)]),
])
