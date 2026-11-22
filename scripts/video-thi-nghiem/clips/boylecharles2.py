# Clip: tn-l12-boylecharles-02 - Cot khi trong ong thuy tinh, ap suat khong doi (dinh luat Charles)
# Ban 2 (21/11/2026, viec 4 lo 20 KE-HOACH-CAI-TIEN-CLIP): dung lai theo cong --do-chu moi (chu than canh >= 56 px,
#   bo chu xam nhat cho dieu quan trong, moi nhip >= 2,5 s, dem nguoc 5 cham, khong ve nut A-D - K10, bo dong
#   "Chon dap an o khung cau hoi"). Quan niem sai can danh: lay ti so theo °C (87/27, 50/25) thay vi kenvin ->
#   canh Bay dat ngay sau dap an, HINH tu giai thich: ba cot t (°C) | L (cm) | T (K) cung ve tu goc 0 cua thang minh;
#   cot °C gap ba (25 -> 75), cot L do that va cot T (K) chi nhich -> "SAI" / "KHOP".
# Ban 1 (14/11/2026): Du doan -> Tien hanh -> Do thi -> Co che -> Bay (L ti le t °C) -> Chot.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-boylecharles-02.json -> so_lieu_mau:
#   t (°C) 0 / 25 / 50 / 75 ; T (K) 273 / 298 / 323 / 348 ; L (cm) 10,0 / 10,9 / 11,9 / 12,9.
#   Doi 2 phut: cac_buoc.lam. Gioi han 273-348 K: khong_chung_minh.
# Du doan (khung web hoi A-D, clip khong ve nut): nuoc 25 °C -> 50 °C, p khong doi, cot khi 10,9 cm dai bao nhieu?
#   A. 10,9 cm  B. 21,8 cm (gap doi theo °C)  C. 11,9 cm <- DAP AN (so_lieu_mau o 50 °C)  D. 5,5 cm (ti le nghich).
# THU NGHI (cau chot, so moi chua hien tren man): biet 0 °C: L = 10,0 cm; nuoc soi 100 °C: L = ?
#   -> 100 °C = 373 K; L = 10,0 x 373/273 ≈ 13,7 cm (kho: so_lieu_mau.ghi_chu "Ca tu suy cho cau chot clip ... ≈ 13,7 cm").
#   Lay ti so °C (100/0) khong tinh duoc -> buoc phai doi ra K. 373 va 13,7 KHONG xuat hien tren man;
#   duong thang tren do thi chi ve toi 348 K, nhiet ke khong ghi so.
from engine import *
import random

ROWS = [(0, 273, 10.0), (25, 298, 10.9), (50, 323, 11.9), (75, 348, 12.9)]
L0, T0 = 10.0, 273
def fmt(v, n=1): return f"{v:.{n}f}".replace(".", ",")
def dashed(d, p1, p2, color, w=3, dash=16, gap=12):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)
def pill(d, cx, cy, s, size, bg, k):
    pw = tw(d, s, F(size)) + 56
    card(d, (cx - pw / 2, cy - size * 0.72, cx + pw / 2, cy + size * 0.72), fill=A(bg, k), r=int(size * 0.72))
    text(d, (cx, cy), s, size, WHITE, alpha=k)

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

def clock(d, cx, cy, r, ph, k):
    """Dong ho doi 2 phut: kim quay (hinh, khong chu)."""
    if k <= 0: return
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(WHITE, k), outline=A(NAVY, k), width=6)
    a = -math.pi / 2 + 2 * math.pi * ph
    d.line([(cx, cy), (cx + 0.8 * r * math.cos(a), cy + 0.8 * r * math.sin(a))], fill=A(ORANGE, k), width=8)
    dot(d, cx, cy, 8, A(NAVY, k))

def rig(d, t, tf, L, ice=0.0, steam=0.0, panel=None, wait=0.0, wph=0.0):
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
        if c % 4 == 0: text(d, (TX + TW + 46, y), str(c), 56, INK, bold=False, anchor="lm")
    d.rounded_rectangle([BK0, BKT, BK1, BKB], radius=24, outline=NAVY, width=6)
    text(d, (TX + 40, BKT - 44), "đầu hở", 56, INK, bold=False, anchor="lm")
    card(d, (630, 330, 1030, 760), fill=WHITE, outline=NAVY, r=28, w=4)
    text(d, (830, 690), "p không đổi", 56, INK, bold=False)
    if panel is None:
        clock(d, 830, 500, 110, wph, max(wait, 0.0))
        return
    tc, Lc = panel
    text(d, (830, 415), f"t = {tc} °C", 60, RED)
    text(d, (830, 540), f"L = {fmt(Lc)} cm", 60, BLUE)

def tf_of(tc): return tc / 75

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    r = ROWS[1]; rig(d, t, tf_of(r[0]), r[2], panel=(r[0], r[2]))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1080 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 64, "DỰ ĐOÁN", 56, PURPLE, a)
    text(d, (W / 2, y0 + 180), "Nước 25 °C → 50 °C", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "Cột khí dài bao nhiêu?", 62, INK, alpha=a)     # K10: khong ve nut A-D
    tc, tend = M[1] + 0.3, sc["T"] - 0.1                    # dem nguoc 5 cham (>= 5 s)
    n_off = 0 if t < tc else min(5, int((t - tc) / ((tend - tc) / 5)) + 1)
    for j in range(5):
        dot(d, W / 2 + (j - 2) * 140, y0 + 410, 40, A(LIGHT, a) if j >= 5 - n_off else A(PURPLE, a))

# ---------------- canh 2: tien hanh ----------------
STEP = [-2.0, 2.0, 3.9, 6.3]      # moc bat dau doi coc lan i (coc 0 °C da on dinh tu dau canh)
TR, SETTLE = 1.0, 0.5            # chuyen coc + doi on dinh
def row_at(i): return STEP[i] + TR + SETTLE
def do_state(t):
    """(tf, L, ice, steam, panel|None, wait, wph)"""
    i = max([j for j in range(4) if t >= STEP[j]], default=0)
    prev = ROWS[i - 1] if i > 0 else ROWS[0]; cur = ROWS[i]
    k = ease((t - STEP[i]) / TR)
    tf = lerp(tf_of(prev[0]), tf_of(cur[0]), k); L = lerp(prev[2], cur[2], k)
    ice = 1 - k if i == 1 else (1.0 if i == 0 else 0.0)
    steam = clamp((tf - 0.5) / 0.5)
    if t >= row_at(i): return tf, L, ice, steam, (cur[0], cur[2]), 0, 0
    return tf, L, ice, steam, None, appear(t, STEP[i] + 0.1, 0.3), clamp((t - STEP[i]) / (TR + SETTLE))

XS = [230, 540, 850]
def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    tf, L, ice, steam, panel, wait, wph = do_state(t)
    rig(d, t, tf, L, ice, steam, panel, wait, wph)
    ka = appear(t, M[2], 0.45)
    card(d, (60, 1095, 1020, 1600), fill=WHITE, outline=NAVY, w=4)
    for x, c, col in zip(XS, ["t (°C)", "T (K)", "L (cm)"], [RED, GREEN, BLUE]): text(d, (x, 1150), c, 58, col)
    d.line([(90, 1192), (990, 1192)], fill=LIGHT, width=4)
    for i, (tc, Tk, Lc) in enumerate(ROWS):
        a = appear(t, row_at(i), 0.35); y = 1238 + i * 76
        if a <= 0: continue
        if i == 2 and ka > 0: d.rounded_rectangle([80, y - 34, 1000, y + 34], radius=16, fill=A((220, 252, 231), ka))
        for x, s in zip(XS, [str(tc), str(Tk), fmt(Lc)]): text(d, (x, y), s, 58, INK, alpha=a)
    if ka > 0:
        pill(d, W / 2, 1548, "ĐÁP ÁN: 11,9 cm", 56, GREEN, ka)

# ---------------- canh 3: bay - ti so theo °C ----------------
PB, PH = 1180, 400                 # day cot, chieu cao cot lon nhat
PCX = [185, 540, 895]              # tam 3 o: t (°C) | L (cm) | T (K)
def bars(d, cx, vals, scale, labs, col, k):
    for j, (v, s) in enumerate(zip(vals, labs)):
        x = cx + (j - 0.5) * 150; h = v * scale
        d.rounded_rectangle([x - 48, PB - h * k, x + 48, PB], radius=10, fill=A(col, k))
        text(d, (x, PB - h - 40), s, 56, INK, alpha=k)
def tubes(d, cx, vals, scale, k):
    for j, v in enumerate(vals):
        x = cx + (j - 0.5) * 170; h = v * scale
        d.rounded_rectangle([x - 34, PB - PH - 30, x + 34, PB + 8], radius=30, fill=A((250, 252, 255), k), outline=A(NAVY, k), width=5)
        d.rectangle([x - 28, PB - h * k, x + 28, PB], fill=A((222, 236, 255), k))
        d.rectangle([x - 28, PB - h * k - 22, x + 28, PB - h * k], fill=A((250, 196, 40), k))
        text(d, (x, PB - PH - 75), fmt(v), 56, INK, alpha=k)   # nhan tren dinh ong
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k1 = appear(t, 0.3, 0.4); k2 = appear(t, M[1] - 0.1, 0.4); k3 = appear(t, M[2] - 0.1, 0.4)
    card(d, (60, 250, 1020, 545), fill=A(WHITE, k1), outline=A(RED, k1), w=6)
    pill(d, W / 2, 305, "BẪY", 56, RED, k1)
    text(d, (W / 2, 405), "75 °C gấp ba 25 °C", 62, INK, alpha=k1)
    text(d, (W / 2, 490), "→ cột khí gấp ba?", 62, INK, alpha=k1)
    for cx, k, lab, col in zip(PCX, (k1, k2, k3), ("t (°C)", "L (cm)", "T (K)"), (RED, BLUE, GREEN)):
        if k <= 0: continue
        card(d, (cx - 165, 575, cx + 165, 1370), fill=A(WHITE, k), outline=A(col, k), w=4, r=24)
        text(d, (cx, 625), lab, 58, col, alpha=k)
        d.line([(cx - 140, PB), (cx + 140, PB)], fill=A(NAVY, k), width=5)
    # nhip 1: cot °C tinh tu 0 °C -> 50 cao gap doi 25
    bars(d, PCX[0], (25, 75), PH / 75, ("25", "75"), (252, 165, 165), k1)
    text(d, (PCX[0], PB + 50), "gốc 0 °C", 56, RED, alpha=k1)
    # nhip 2: cot khi do that chi nhich -> °C SAI
    if k2 > 0:
        tubes(d, PCX[1], (10.9, 12.9), PH / 12.9, k2)
        pill(d, PCX[0], 1305, "SAI", 56, RED, k2)
    # nhip 3: cot T (K) tinh tu 0 K -> nhich giong cot khi -> KHOP
    if k3 > 0:
        bars(d, PCX[2], (298, 348), PH / 348, ("298", "348"), (134, 239, 172), k3)
        text(d, (PCX[2], PB + 50), "gốc 0 K", 56, GREEN, alpha=k3)
        pill(d, PCX[2], 1305, "KHỚP", 56, GREEN, k3)

# ---------------- canh 4: do thi L-T ----------------
GX0, GX1, GYB, GYT = 210, 980, 930, 360
def GX(T): return GX0 + T / 400 * (GX1 - GX0)
def GY(L): return GYB - L / 14 * (GYB - GYT)
def s_graph(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 250, 1040, 1060), fill=WHITE, outline=LIGHT, w=3)
    for L_ in (5, 10): d.line([(GX0, GY(L_)), (GX1, GY(L_))], fill=(240, 236, 228), width=2)
    d.line([(GX0, GYB), (GX1 + 20, GYB)], fill=NAVY, width=5); d.line([(GX0, GYB), (GX0, GYT - 40)], fill=NAVY, width=5)
    text(d, (GX1 + 20, GYB - 44), "T (K)", 58, GREEN, anchor="rm")
    text(d, (GX0 + 22, GYT - 40), "L (cm)", 58, BLUE, anchor="lm")
    for L_ in (5, 10): text(d, (GX0 - 18, GY(L_)), str(L_), 56, INK, bold=False, anchor="rm")
    text(d, (GX0 - 18, GYB + 36), "0", 58, INK, anchor="rm")
    for T_ in (273, 348):
        d.line([(GX(T_), GYB), (GX(T_), GYB + 12)], fill=NAVY, width=3)
        text(d, (GX(T_), GYB + 50), str(T_), 56, INK, bold=False)
    k = ease((t - M[0] - 1.0) / 0.8)                      # doan do duoc 273 -> 348 K
    if k > 0:
        p1, p2 = (GX(273), GY(L0)), (GX(lerp(273, 348, k)), GY(L0 * lerp(273, 348, k) / T0))
        d.line([p1, p2], fill=A(BLUE, 0.7), width=7)
    ke = ease((t - M[1] - 0.1) / 1.0)                     # keo dai ve goc 0 K
    if ke > 0:
        Tk = lerp(273, 0, ke); dashed(d, (GX(273), GY(L0)), (GX(Tk), GY(L0 * Tk / T0)), BLUE, w=5)
        text(d, (GX(60), GY(7.0)), "kéo dài", 58, BLUE, alpha=appear(t, M[1] + 0.3))
    for i, r in enumerate(ROWS):
        a = appear(t, M[0] + 0.2 + i * 0.25, 0.4)
        if a > 0: dot(d, GX(r[1]), GY(r[2]), 15 * back(a), ORANGE, WHITE)
    a0 = appear(t, M[0] + 0.5)                            # nhip 1: ong deu nen L thay cho V
    if a0 > 0:
        card(d, (60, 1095, 1020, 1215), fill=A(WHITE, a0), outline=A(BLUE, a0), w=4)
        text(d, (W / 2, 1155), "L dài hơn → V lớn hơn", 58, INK, alpha=a0)
    a1 = appear(t, M[2] + 0.4)                            # nhip 3: cach "keo dai" >= 2,5 s
    if a1 <= 0: return
    card(d, (60, 1245, 1020, 1570), fill=A((236, 253, 243), a1), outline=A(GREEN, a1), w=5)
    text(d, (W / 2, 1335), "L/T không đổi", 80, GREEN, alpha=a1)
    text(d, (W / 2, 1475), "p không đổi, T đo bằng K", 58, INK, alpha=a1)

# ---------------- canh 5: co che + chua noi duoc ----------------
def s_why(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    for x, r in ((300, ROWS[0]), (780, ROWS[3])):
        tf = tf_of(r[0])
        d.rounded_rectangle([x - 150, 260, x + 150, 960], radius=24, fill=mix(COLD, HOT, tf))
        tube(d, t, r[2], tf, x=x, yb=900, px=44, top_cm=13.6, w=42, mol=False)
        yc = 900 - r[2] * 44; sp = 0.5 + 2.2 * tf
        for (ux, uy, vx, vy) in MOL:
            mx = x - 34 + refl(ux + vx * t * sp, 0, 1) * 68
            my = yc + 12 + refl(uy + vy * t * sp, 0, 1) * (900 - yc - 30)
            dot(d, mx, my, 8, mix(ORANGE, RED, tf))
            if my - yc < 22: d.line([(x - 30, yc - 2), (x + 30, yc - 2)], fill=YELLOW, width=8)
        text(d, (x, 1015), f"{r[0]} °C", 60, RED if tf > 0.5 else BLUE)
        text(d, (x, 1095), f"{fmt(r[2])} cm", 58, INK)
    k2 = appear(t, M[1] - 0.1)
    if k2 > 0:
        card(d, (60, 1160, 1020, 1570), fill=A(WHITE, k2), outline=A(BLUE, k2), w=6)
        text(d, (W / 2, 1240), "Chưa nói được gì?", 58, BLUE, alpha=k2)
        text(d, (W / 2, 1355), "Chỉ đo 273 K → 348 K", 58, INK, alpha=k2)
        text(d, (W / 2, 1465), "Đoạn tới 0 K: chưa đo", 58, INK, alpha=k2)

# ---------------- canh 6: THU NGHI ----------------
DARK_OR = (181, 71, 8)                         # chu cam tren nen sang >= 4,5:1
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    x0, y0, x1, y1 = 250, 420, 830, 980        # coc nuoc soi + ong co "?"
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=HOT, outline=NAVY, width=6)
    for j in range(8):
        ph = (t * 0.8 + j * 0.17) % 1
        dot(d, x0 + 50 + j * 68, y1 - 30 - ph * 480, 12, A(WHITE, 1 - ph))
    tx, top = 540, 310                         # ong rong + "?" (khong ve cot khi: khong goi do dai)
    d.rounded_rectangle([tx - 33, top, tx + 33, 937], radius=33, fill=(250, 252, 255))
    d.line([(tx - 33, top), (tx - 33, 904)], fill=NAVY, width=5); d.line([(tx + 33, top), (tx + 33, 904)], fill=NAVY, width=5)
    d.arc([tx - 33, 871, tx + 33, 937], 0, 180, fill=NAVY, width=5)
    text(d, (640, 560), "?", 110, DARK_OR, anchor="lm")
    k = appear(t, 0.3, 0.5)
    if k <= 0: return
    card(d, (50, 1030, 1030, 1600), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1100, "THỬ NGHĨ", 56, DARK_OR, k)
    text(d, (W / 2, 1200), "Ở 0 °C: L = 10,0 cm", 62, INK, alpha=k)
    text(d, (W / 2, 1290), "p không đổi", 62, INK, alpha=k)
    text(d, (W / 2, 1380), "Nước sôi 100 °C: L = ?", 62, DARK_OR, alpha=k)
    kh = appear(t, 2.8, 0.5)
    if kh > 0:
        card(d, (150, 1440, 930, 1575), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1507), "Gợi ý: đổi °C ra K", 58, INK, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, tr, g, w, e = (sc[k] for k in ("hook", "do", "trap", "graph", "why", "end"))
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][2], "ding"),
            (tr["t0"] + 0.3, "buzz"), (tr["t0"] + tr["M"][2] - 0.1, "tap"),
            (g["t0"] + g["M"][1] + 0.1, "tap"), (w["t0"] + w["M"][1] - 0.1, "tap"),
            (e["t0"] + 0.3, "open")]

CLIP = dict(id="tn-l12-boylecharles-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Định luật Charles · thachlab.id.vn", scenes=[
 dict(key="hook", title="Cột khí trong ống nghiệm", draw=s_hook, tail=0.3, caps=[
   "Giọt dầu nhốt cột khí.",
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Ngâm ống vào từng cốc nước", draw=s_do, tail=0.3, caps=[
   "Nước nóng dần lên.",
   "Mỗi cốc đợi 2 phút.",
   "Dài thêm chừng 1 cm."]),
 dict(key="trap", title="Lấy tỉ số theo °C?", draw=s_trap, tail=0.3, caps=[
   ("Đúng hay sai?", 3.1),
   "Đo thật: không gấp ba.",
   ("Theo kenvin mới khớp.", 3.0)]),
 dict(key="graph", title="Đồ thị L theo T", draw=s_graph, tail=0.3, caps=[
   "Bốn điểm thẳng hàng.",
   "Kéo dài: qua gốc 0 K.",
   ("Định luật Charles.", 2.8)]),
 dict(key="why", title="Vì sao cột khí dài ra?", draw=s_why, tail=0.3, caps=[
   "Phân tử nhanh, khí dãn.",
   ("Giới hạn phép đo.", 4.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự đoán.", 4.2)]),
])
