# Clip: tn-l12-boylecharles-02 - Cot khi trong ong thuy tinh, ap suat khong doi (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-boylecharles-02.json -> so_lieu_mau:
#   t (°C) 0 / 25 / 50 / 75 ; T (K) 273 / 298 / 323 / 348 ; L (cm) 10,0 / 10,9 / 11,9 / 12,9 ; L/T 0,0366 / 0,0366 / 0,0368
#   (L/T o 75 °C = 0,0371 KHONG hien: bang so do trong bai de o nay "em tu tinh").
#   -273 °C (= 0 K) lay tu goi_y_mo_phong.diem_nhan; doi 2 phut lay tu cac_buoc.lam.
# Canh: Du doan (25 -> 50 °C) -> Tien hanh (4 coc, bang t/T/L) + dap an -> Do thi L-T qua O + bang L/T
#       -> Co che + chua noi duoc -> Bay (L ti le voi t °C) -> Chot + THU NGHI.
#
# Khung cau hoi (4 lua chon cho VideoThiNghiemKhung, KHONG ve trong mp4 - K10):
#   Cau: "Nuoc 25 °C -> 50 °C, ap suat khong doi. Cot khi 10,9 cm se dai khoang bao nhieu?"
#   A. khoang 10,9 cm (nghi p khong doi thi V khong doi)
#   B. khoang 21,8 cm (gap doi theo °C)
#   C. khoang 11,9 cm   <- DAP AN (so lieu mau o 50 °C)
#   D. khoang 5,5 cm  (nham ti le nghich nhu Boyle)
# THU NGHI (cau chot): ngam ong vao nuoc 100 °C (so moi, chua hien tren man; thang do nhiet ke khong ghi so 100)
#   -> L = 10,0 x 373/273 ≈ 13,7 cm (kho: so_lieu_mau.ghi_chu "o 100 °C mo hinh cho 13,7 cm").
#   Duong thang tren do thi chi ve toi 348 K (khong cham 373 K).
#   Cau chot: "Theo dinh luat Charles, ngam ong vao nuoc 100 °C: cot khi dai bao nhieu?" (100 °C ngoai khoang do).
#   dai chot: "Cung ong, cung giot dau"; goi_y: "Nhiet ke ghi °C" (khong neu cong thuc).
from engine import *
import random

ROWS = [(0, 273, 10.0, 0.0366), (25, 298, 10.9, 0.0366), (50, 323, 11.9, 0.0368), (75, 348, 12.9, 0.0371)]
L0, T0 = 10.0, 273
def fmt(v, n=1): return f"{v:.{n}f}".replace(".", ",")
def dashed(d, p1, p2, color, w=3, dash=16, gap=12):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

R = random.Random(21)
MOL = [(R.random(), R.random(), R.choice((-1, 1)) * R.uniform(0.25, 0.45), R.choice((-1, 1)) * R.uniform(0.25, 0.45)) for _ in range(14)]

# ---------------- coc nuoc + ong + thuoc ----------------
BK0, BK1, BKT, BKB, WLV = 110, 590, 430, 1050, 470        # coc: trai, phai, mieng, day; muc nuoc
TX, TW, YB, PX = 380, 22, 1000, 40                         # ong: tam x, nua be rong trong, day kin (y), px/cm
def yL(L): return YB - L * PX
COLD, HOT = (186, 222, 255), (255, 196, 170)

def tube(d, t, L, tf, x=TX, yb=YB, px=PX, top_cm=15.0, w=TW, mol=True):
    top = yb - top_cm * px; yc = yb - L * px
    d.rounded_rectangle([x - w - 7, top, x + w + 7, yb + 7], radius=w + 7, fill=(250, 252, 255))
    d.rounded_rectangle([x - w, yc, x + w, yb], radius=w, fill=mix((222, 236, 255), (255, 226, 214), tf))
    if mol:
        sp = 1 + 1.6 * tf
        for (ux, uy, vx, vy) in MOL[:9]:
            mx = x - w + 8 + refl(ux + vx * t * sp, 0, 1) * (2 * w - 16)
            my = yc + 10 + refl(uy + vy * t * sp, 0, 1) * (yb - yc - 20)
            dot(d, mx, my, 5, mix(ORANGE, RED, tf))
    d.rectangle([x - w, yc - 26, x + w, yc], fill=(250, 196, 40))           # giot dau
    d.line([(x - w - 7, top), (x - w - 7, yb - w)], fill=NAVY, width=5)
    d.line([(x + w + 7, top), (x + w + 7, yb - w)], fill=NAVY, width=5)
    d.arc([x - w - 7, yb - 2 * w - 7, x + w + 7, yb + 7], 0, 180, fill=NAVY, width=5)

def thermo(d, tf, x=200):
    tb, tt = 990, 560
    d.rounded_rectangle([x - 14, tt, x + 14, tb], radius=14, fill=WHITE, outline=NAVY, width=4)
    dot(d, x, tb + 14, 26, RED, NAVY)
    lvl = lerp(tb - 70, tb - 330, tf)
    d.rectangle([x - 7, lvl, x + 7, tb], fill=RED)
    for k in range(5): d.line([(x + 14, tb - 70 - k * 86.7), (x + 30, tb - 70 - k * 86.7)], fill=NAVY, width=3)

def rig(d, t, tf, L, ice=0.0, steam=0.0, panel=None, wait=0.0):
    d.rounded_rectangle([BK0, BKT, BK1, BKB], radius=24, fill=(248, 250, 252))
    d.rectangle([BK0 + 6, WLV, BK1 - 6, BKB - 6], fill=mix(COLD, HOT, tf))
    for j in range(3):                                     # vien da
        if ice > 0.02:
            x = 170 + j * 70 + (j == 2) * 300; y = WLV + 20 + (j % 2) * 26
            d.rounded_rectangle([x, y, x + 54, y + 46], radius=8, fill=A(WHITE, ice), outline=A((150, 190, 230), ice), width=3)
    if steam > 0.02:                                       # hoi nuoc
        for j in range(3):
            x = 200 + j * 150; ph = (t * 0.6 + j * 0.33) % 1
            pts = [(x + 14 * math.sin(6 * s + j), WLV - 20 - ph * 120 - s * 60) for s in [i / 8 for i in range(9)]]
            d.line(pts, fill=A((170, 175, 190), steam * (1 - ph)), width=5)
    thermo(d, tf)
    tube(d, t, L, tf)
    for c in range(0, 15):                                 # thuoc chia cm gan ong
        y = yL(c); Lm = 22 if c % 2 == 0 else 12
        d.line([(TX + TW + 14, y), (TX + TW + 14 + Lm, y)], fill=NAVY, width=3)
        if c % 4 == 0: text(d, (TX + TW + 46, y), str(c), 44, MUTED, bold=False, anchor="lm")
    d.rounded_rectangle([BK0, BKT, BK1, BKB], radius=24, outline=NAVY, width=6)
    text(d, (TX + 44, BKT - 36), "đầu hở", 44, MUTED, bold=False, anchor="lm")
    card(d, (630, 330, 1030, 760), fill=WHITE, outline=LIGHT, r=28, w=4)
    if panel is None:
        text(d, (830, 545), "đợi 2 phút…", 48, MUTED, alpha=max(wait, 0.0))
        return
    tc, Tk, Lc = panel
    text(d, (830, 410), f"t = {tc} °C", 52, RED)
    text(d, (830, 500), f"T = {Tk} K", 52, MUTED)
    text(d, (830, 590), f"L = {fmt(Lc)} cm", 52, BLUE)
    text(d, (830, 690), "p không đổi", 44, INK, bold=False)

def tf_of(tc): return tc / 75

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    r = ROWS[1]; rig(d, t, tf_of(r[0]), r[2], panel=(r[0], r[1], r[2]))
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1110, 1020, 1590), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1175), "Dự đoán", 50, PURPLE, alpha=k)
    ctext(d, 1300, "Nước 25 °C → 50 °C, p không đổi.\nCột khí 10,9 cm sẽ dài khoảng bao nhiêu?", 48, INK, maxw=900, alpha=k)
    text(d, (W / 2, 1440), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=k)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1520, 940, 1536], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1520, 140 + 800 * (1 - q), 1536], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
STEP = [0.2, 2.2, 4.3, 7.0]       # moc bat dau doi coc lan i
TR, SETTLE = 1.0, 0.5            # chuyen coc + doi on dinh
def row_at(i): return STEP[i] + TR + SETTLE
def do_state(t):
    """(tf, L, ice, steam, panel|None, wait)"""
    i = max([j for j in range(4) if t >= STEP[j]], default=0)
    prev = ROWS[i - 1] if i > 0 else ROWS[0]; cur = ROWS[i]
    k = ease((t - STEP[i]) / TR)
    tf = lerp(tf_of(prev[0]), tf_of(cur[0]), k); L = lerp(prev[2], cur[2], k)
    ice = 1 - k if i == 1 else (1.0 if i == 0 else 0.0)
    steam = clamp((tf - 0.5) / 0.5)
    if t >= row_at(i): return tf, L, ice, steam, (cur[0], cur[1], cur[2]), 0
    return tf, L, ice, steam, None, appear(t, STEP[i] + 0.2, 0.3)

XS = [250, 520, 790]
def s_do(img, d, t, sc):
    IMG_REF[0] = img
    tf, L, ice, steam, panel, wait = do_state(t)
    rig(d, t, tf, L, ice, steam, panel, wait)
    n = sum(1 for i in range(4) if t >= row_at(i))
    ka = appear(t, sc["M"][2], 0.45)
    yb = 1580 if ka > 0 else 1225 + max(n - 1, 0) * 70 + 55
    card(d, (80, 1100, 1000, yb), fill=WHITE, outline=NAVY, w=4)
    for x, c in zip(XS, ["t (°C)", "T (K)", "L (cm)"]): text(d, (x, 1150), c, 46, MUTED)
    d.line([(110, 1188), (970, 1188)], fill=LIGHT, width=4)
    for i, (tc, Tk, Lc, _) in enumerate(ROWS):
        a = appear(t, row_at(i), 0.35); y = 1225 + i * 70
        if a <= 0: continue
        if i == 2 and ka > 0: d.rounded_rectangle([100, y - 32, 980, y + 32], radius=16, fill=A((220, 252, 231), ka))
        for x, s, col in zip(XS, [str(tc), str(Tk), fmt(Lc)], [RED, MUTED, BLUE]): text(d, (x, y), s, 48, col, alpha=a)
    if ka > 0:
        lb = "ĐÁP ÁN · khoảng 11,9 cm"
        pw = tw(d, lb, F(46)) + 60
        card(d, (W / 2 - pw / 2, 1482, W / 2 + pw / 2, 1556), fill=A(GREEN, ka), r=37)
        text(d, (W / 2, 1519), lb, 46, WHITE, alpha=ka)

# ---------------- canh 3: do thi L-T ----------------
GX0, GX1, GYB, GYT = 200, 980, 900, 330
def GX(T): return GX0 + T / 400 * (GX1 - GX0)
def GY(L): return GYB - L / 14 * (GYB - GYT)
def s_graph(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 250, 1040, 1020), fill=WHITE, outline=LIGHT, w=3)
    for L_ in (5, 10): d.line([(GX0, GY(L_)), (GX1, GY(L_))], fill=(240, 236, 228), width=2)
    d.line([(GX0, GYB), (GX1 + 20, GYB)], fill=NAVY, width=5); d.line([(GX0, GYB), (GX0, GYT - 30)], fill=NAVY, width=5)
    text(d, (GX1 + 20, GYB - 40), "T (K)", 46, MUTED, anchor="rm")
    text(d, (GX0 + 20, GYT - 30), "L (cm)", 46, MUTED, anchor="lm")
    for L_ in (5, 10): text(d, (GX0 - 18, GY(L_)), str(L_), 44, MUTED, bold=False, anchor="rm")
    text(d, (GX0 - 18, GYB + 30), "O", 46, INK, anchor="rm")
    for T_ in (273, 348):
        d.line([(GX(T_), GYB), (GX(T_), GYB + 12)], fill=NAVY, width=3)
        text(d, (GX(T_), GYB + 44), str(T_), 44, MUTED, bold=False)
    k = ease((t - M[0] - 1.0) / 0.8)                      # doan do duoc 273 -> 348 K (khong ve qua 348)
    if k > 0:
        p1, p2 = (GX(273), GY(L0)), (GX(lerp(273, 348, k)), GY(L0 * lerp(273, 348, k) / T0))
        d.line([p1, p2], fill=A(BLUE, 0.7), width=7)
    ke = ease((t - M[1] - 0.3) / 1.0)                     # keo dai ve goc O
    if ke > 0:
        Tk = lerp(273, 0, ke); dashed(d, (GX(273), GY(L0)), (GX(Tk), GY(L0 * Tk / T0)), BLUE, w=5)
        text(d, (GX(70), GY(4.6)), "kéo dài", 44, BLUE, alpha=appear(t, M[1] + 1.0))
    for i, r in enumerate(ROWS):
        a = appear(t, M[0] + 0.2 + i * 0.25, 0.4)
        if a > 0: dot(d, GX(r[1]), GY(r[2]), 15 * back(a), ORANGE, WHITE)
    a1 = appear(t, M[2] - 0.2)
    if a1 <= 0: return
    card(d, (60, 1060, 1020, 1520), fill=A(WHITE, a1), outline=A(GREEN, a1), w=4)
    xs = [230, 520, 810]
    for x, c in zip(xs, ["T (K)", "L (cm)", "L/T (cm/K)"]): text(d, (x, 1110), c, 44, MUTED, alpha=a1)
    d.line([(90, 1145), (990, 1145)], fill=A(LIGHT, a1), width=4)
    for i, (tc, Tk, Lc, q) in enumerate(ROWS):
        a = appear(t, M[2] + 0.1 + i * 0.35, 0.35); y = 1190 + i * 74
        if a <= 0: continue
        qs = fmt(q, 4) if i < 3 else "?"
        for x, s, col in zip(xs, [str(Tk), fmt(Lc), qs], [MUTED, BLUE, GREEN]): text(d, (x, y), s, 48, col, alpha=a)

# ---------------- canh 4: co che + chua noi duoc ----------------
def s_why(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    for x, r, lab in ((330, ROWS[0], "0 °C"), (750, ROWS[3], "75 °C")):
        tf = tf_of(r[0])
        d.rounded_rectangle([x - 150, 300, x + 150, 1000], radius=24, fill=mix(COLD, HOT, tf))
        tube(d, t, r[2], tf, x=x, yb=930, px=44, top_cm=13.8, w=42, mol=False)
        yc = 930 - r[2] * 44; sp = 0.5 + 2.2 * tf
        for (ux, uy, vx, vy) in MOL:
            mx = x - 34 + refl(ux + vx * t * sp, 0, 1) * 68
            my = yc + 12 + refl(uy + vy * t * sp, 0, 1) * (930 - yc - 30)
            dot(d, mx, my, 8, mix(ORANGE, RED, tf))
            if my - yc < 22: d.line([(x - 30, yc - 2), (x + 30, yc - 2)], fill=YELLOW, width=8)
        text(d, (x, 1045), lab, 48, RED if tf > 0.5 else BLUE)
        text(d, (x, 1110), f"{fmt(r[2])} cm", 44, INK, bold=False)
    k1 = appear(t, M[1] - 0.1); k2 = appear(t, M[2] - 0.1)
    if k1 > 0 and k2 < 1:
        a = k1 * (1 - k2)
        card(d, (80, 1180, 1000, 1500), fill=A(WHITE, a), outline=A(GREEN, a), w=6)
        rich(d, W / 2, 1290, "V_{1}/T_{1} = V_{2}/T_{2}", 84, GREEN, alpha=a)
        text(d, (W / 2, 1420), "p không đổi, T tính bằng kenvin", 44, INK, bold=False, alpha=a)
    if k2 > 0:
        card(d, (80, 1180, 1000, 1540), fill=A(WHITE, k2), outline=A(BLUE, k2), w=6)
        text(d, (W / 2, 1245), "Chưa nói được gì?", 48, BLUE, alpha=k2)
        text(d, (W / 2, 1345), "Chỉ đo từ 273 K đến 348 K.", 46, INK, alpha=k2)
        text(d, (W / 2, 1445), "Đoạn tới 0 K là kéo dài, chưa đo.", 46, INK, bold=False, alpha=k2)

# ---------------- canh 5: bay ----------------
BX0, BX1, BYB, BYT = 160, 980, 1250, 760
def BXt(tc): return BX0 + (tc + 300) / 400 * (BX1 - BX0)
def BY(L): return BYB - L / 14 * (BYB - BYT)
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.1); mk = M[1]
    card(d, (60, 260, 1020, 560), fill=A(WHITE, a), outline=A(RED, a), w=6)
    text(d, (W / 2, 320), "Bẫy trong đề", 46, RED, alpha=a)
    s = "“L tỉ lệ thuận với t (°C)”"; f = F(50); sw = tw(d, s, f)
    text(d, (W / 2, 420), s, 50, INK, alpha=a)
    g = ease((t - mk) / 0.4)
    if g > 0:
        d.line([(W / 2 - sw / 2 - 10, 420), (W / 2 - sw / 2 - 10 + (sw + 20) * g, 420)], fill=RED, width=7)
        text(d, (W / 2 + sw / 2 + 50, 420), "✗", 56, RED, alpha=g)
    # do thi L theo t (°C)
    card(d, (40, 600, 1040, 1380), fill=WHITE, outline=LIGHT, w=3)
    xO = BXt(0)
    d.line([(BX0, BYB), (BX1 + 10, BYB)], fill=NAVY, width=5); d.line([(xO, BYB + 10), (xO, BYT - 30)], fill=NAVY, width=5)
    text(d, (BX1 + 10, BYB - 40), "t (°C)", 46, MUTED, anchor="rm"); text(d, (xO + 20, BYT - 30), "L (cm)", 46, MUTED, anchor="lm")
    text(d, (xO - 16, BYB + 34), "O", 46, INK, anchor="rm")
    d.line([(BXt(75), BYB), (BXt(75), BYB + 12)], fill=NAVY, width=3); text(d, (BXt(75), BYB + 44), "75", 44, MUTED, bold=False)
    for r in ROWS: dot(d, BXt(r[0]), BY(r[2]), 14, ORANGE, WHITE)
    d.line([(BXt(0), BY(10.0)), (BXt(75), BY(12.9))], fill=A(BLUE, 0.7), width=6)
    c1 = appear(t, mk + 0.2, 0.4)                          # hinh "dap" hien SAU khi gach
    if c1 > 0:
        d.ellipse([xO - 30, BY(10) - 30, xO + 30, BY(10) + 30], outline=A(RED, c1), width=6)
        text(d, (xO - 40, BY(10) - 60), "t = 0 °C: L = 10,0 cm", 44, RED, anchor="rm", alpha=c1)
        kk = ease((t - mk - 0.8) / 1.0)
        if kk > 0:
            tz = lerp(0, -273, kk); dashed(d, (BXt(0), BY(10.0)), (BXt(tz), BY(10.0 * (tz + 273) / 273)), BLUE, w=5)
        c2 = appear(t, mk + 1.6)
        d.line([(BXt(-273), BYB), (BXt(-273), BYB + 12)], fill=A(NAVY, c2), width=3)
        text(d, (BXt(-273), BYB + 44), "−273", 44, BLUE, alpha=c2)
    c3 = appear(t, mk + 2.4)
    if c3 > 0:
        card(d, (60, 1420, 1020, 1560), fill=A((220, 252, 231), c3), r=26)
        text(d, (W / 2, 1490), "✓ L tỉ lệ thuận với T (K)", 48, GREEN, alpha=c3)

# ---------------- canh 6: chot ----------------
def mini(d, t, k):                                   # coc nuoc soi + ong (x1,5), ben trai; goi y ben phai
    x0, y0, x1, y1 = 110, 960, 470, 1440
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=A(HOT, k), outline=A(NAVY, k), width=6)
    for j in range(6):
        ph = (t * 0.8 + j * 0.19) % 1
        dot(d, x0 + 45 + j * 55, y1 - 30 - ph * 380, 12, A(WHITE, k * (1 - ph)))
    tx = (x0 + x1) / 2
    d.rounded_rectangle([tx - 24, 900, tx + 24, y1 - 30], radius=24, fill=A((250, 252, 255), k), outline=A(NAVY, k), width=5)
    text(d, (tx, 1200), "?", 72, PURPLE, alpha=k)

def s_end(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    chot_hoi(d, t, sc, "Cùng ống, cùng giọt dầu",
             "Theo định luật Charles, nước 100 °C: cột khí dài bao nhiêu?", None, body=mini)
    kh = appear(t, M[0] + 2.5, 0.5)
    if kh > 0:
        card(d, (510, 1140, 1000, 1400), fill=A((255, 247, 237), kh), r=24)
        text(d, (755, 1210), "Gợi ý", 44, MUTED, bold=False, alpha=kh)
        text(d, (755, 1310), "Nhiệt kế ghi °C", 48, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, g, tr, e = sc["hook"], sc["do"], sc["graph"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][2], "ding"), (g["t0"] + g["M"][1] + 0.3, "tap"),
            (tr["t0"] + tr["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-boylecharles-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Định luật Charles · thachlab.id.vn", scenes=[
 dict(key="hook", title="Cột khí trong ống nghiệm", draw=s_hook, tail=0.4, caps=[
   ("Giọt dầu nhốt khí.", 2.5),
   ("Em đoán thử.", 4.8)]),
 dict(key="do", title="Ngâm ống vào từng cốc nước", draw=s_do, tail=0.4, caps=[
   ("Nước đá rồi nóng dần.", 2.9),
   ("Mỗi cốc đợi 2 phút.", 2.9),
   ("50 °C → 11,9 cm.", 3.4)]),
 dict(key="graph", title="Đồ thị L theo T", draw=s_graph, tail=0.4, caps=[
   ("Bốn điểm thẳng hàng.", 2.5),
   ("Kéo dài: qua gốc O.", 2.5),
   ("L chia T gần không đổi.", 2.5)]),
 dict(key="why", title="Vì sao cột khí dài ra?", draw=s_why, tail=0.4, caps=[
   ("Phân tử chạy nhanh hơn.", 2.9),
   ("Khí dãn, giữ p như cũ.", 2.9),
   ("Giới hạn thí nghiệm.", 3.6)]),
 dict(key="trap", title="Đúng không?", draw=s_trap, tail=0.4, caps=[
   ("Xét phát biểu này.", 2.5),
   ("Ở 0 °C cột khí vẫn dài.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Thử tính.", 5.2)]),
])
