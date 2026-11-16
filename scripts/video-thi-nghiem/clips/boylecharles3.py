# Clip: tn-l12-boylecharles-03 - Ong chu J mot dau kin, rot them chat long (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-boylecharles-03.json:
#   h = 0 (p0 = 760 mmHg, L = 21,8 cm: cac_buoc.lam + mo_hinh), so_lieu_mau: h 55/85/110/165 mmHg,
#   p 815/845/870/925 mmHg, L 20,3/19,6/19,0/17,9 cm, p.L 1,65/1,66/1,65/1,66 (10^4 mmHg.cm); h = 0 -> 1,66 (mo_hinh).
#   Doi 1 phut moi lan: cac_buoc.lam. Khoang 760-925 mmHg: khong_chung_minh.
# Khac boyle.py (xilanh + ap ke kPa, 8 -> 3 ml): o day ong chu J, cot chat long vua la pittong vua la ap ke, don vi mmHg.
# Canh: Du doan (h = 110 -> p?) -> Tien hanh (rot 4 lan, bang h/L, roi cot p = p0 + h + dap an)
#       -> Do thi p-L (nhanh hypebol) + cot p.L -> Rut ra + chua noi duoc -> Bay (them chat long = them khi?) -> Chot.
#
# Khung cau hoi (4 lua chon cho VideoThiNghiemKhung, KHONG ve trong mp4 - K10):
#   Cau: "Muc hai nhanh chenh 110 mmHg (nhanh ho cao hon), khi quyen 760 mmHg.
#         Khi bi nhot co ap suat bao nhieu?"
#   A. 650 mmHg (tru h - nham chieu, hien_tuong_hay_sai 1)
#   B. 760 mmHg (bo qua cot chat long)
#   C. 870 mmHg   <- DAP AN (p = p0 + h, so lieu mau)
#   D. 110 mmHg (chi lay h)
# THU NGHI (cau chot): "Muc hai nhanh chenh 150 mmHg: cot khi dai bao nhieu?" (trong khoang do, chua hien tren man)
#   -> p = 910 mmHg, L = 760 x 21,8 / 910 ≈ 18,2 cm. dai chot "Cung ong, cung luong khi"; goi_y "Van mot luong khi nhot kin".
#   Duong cong: lien trong khoang do 17,9-21,8 cm, net dut ngoai khoang (16,8-22,1); qua diem (18,2; 910) - phien chinh da chon h = 150.
from engine import *
import random

HS = [0, 55, 85, 110, 165]
PS = [760, 815, 845, 870, 925]
LS = [21.8, 20.3, 19.6, 19.0, 17.9]
PL = [1.66, 1.65, 1.66, 1.65, 1.66]
def fmt(v, n=1): return f"{v:.{n}f}".replace(".", ",")
def dashed(d, p1, p2, color, w=3, dash=14, gap=10):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

R = random.Random(33)
MOL = [(R.random(), R.random(), R.choice((-1, 1)) * R.uniform(0.25, 0.45), R.choice((-1, 1)) * R.uniform(0.25, 0.45)) for _ in range(12)]
HG = (172, 178, 194); GLASS = (250, 252, 255); GAS = (214, 232, 255)

# ---------------- ong chu J ----------------
XC, YCT, SC = 330, 430, 1.0          # nhanh kin (tam x), dinh nhanh kin (y), ti le
def geo(xc=XC, yct=YCT, s=SC):
    S = 24 * s; w = 20 * s; xo = xc + 200 * s; yb = yct + 600 * s; ytop = yct - 80 * s
    return S, w, xo, yb, ytop

def jtube(d, t, L, h, xc=XC, yct=YCT, s=SC, mol=True, pour=0.0):
    S, w, xo, yb, ytop = geo(xc, yct, s)
    yc = yct + L * S; yo = yc - h / 10 * S
    cx, Rm = (xc + xo) / 2, (xo - xc) / 2
    o = 6 * s
    d.rectangle([xc - w - o, yct - o, xc + w + o, yb], fill=NAVY)
    d.rectangle([xo - w - o, ytop, xo + w + o, yb], fill=NAVY)
    d.arc([cx - Rm - w - o, yb - Rm - w - o, cx + Rm + w + o, yb + Rm + w + o], 0, 180, fill=NAVY, width=int(2 * (w + o)))
    d.rectangle([xc - w, yct, xc + w, yb], fill=GLASS)
    d.rectangle([xo - w, ytop - 10, xo + w, yb], fill=GLASS)
    d.arc([cx - Rm - w, yb - Rm - w, cx + Rm + w, yb + Rm + w], 0, 180, fill=HG, width=int(2 * w))
    d.rectangle([xc - w, yct, xc + w, yc], fill=GAS)
    d.rectangle([xc - w, yc, xc + w, yb + 1], fill=HG)
    d.rectangle([xo - w, yo, xo + w, yb + 1], fill=HG)
    for x, y in ((xc, yc), (xo, yo)): d.line([(x - w, y), (x + w, y)], fill=(120, 126, 145), width=max(2, int(4 * s)))
    if mol:
        for (ux, uy, vx, vy) in MOL:
            mx = xc - w + 6 * s + refl(ux + vx * t, 0, 1) * (2 * w - 12 * s)
            my = yct + 8 * s + refl(uy + vy * t, 0, 1) * (yc - yct - 16 * s)
            dot(d, mx, my, 5 * s, ORANGE)
    if pour > 0:                                         # ong nho giot tren mieng nhanh ho
        d.rounded_rectangle([xo - 14, ytop - 110, xo + 14, ytop - 30], radius=10, fill=WHITE, outline=NAVY, width=4)
        d.ellipse([xo - 30, ytop - 150, xo + 30, ytop - 100], fill=(70, 78, 100))
        ph = (t * 2.2) % 1
        dot(d, xo, lerp(ytop - 30, yo - 10, ph), 9, HG)
    return yc, yo, xo

def figure(d, t, L, h, show_h=True, show_L=True, pour=0.0, h_lbl=None):
    yc, yo, xo = jtube(d, t, L, h, pour=pour)
    S, w, _, yb, ytop = geo()
    for c in range(0, 23):                              # thuoc do cot khi, 0 o dinh nhanh kin
        y = YCT + c * S; Lm = 22 if c % 5 == 0 else 11
        d.line([(XC + w + 10, y), (XC + w + 10 + Lm, y)], fill=NAVY, width=3)
        if c % 5 == 0: text(d, (XC + w + 44, y), str(c), 44, MUTED, bold=False, anchor="lm")
    text(d, (XC + w + 44, YCT - 50), "cm", 44, MUTED, bold=False, anchor="lm")
    if show_L:
        text(d, (XC - w - 30, (YCT + yc) / 2 - 36), "cột khí", 44, MUTED, bold=False, anchor="rm")
        text(d, (XC - w - 30, (YCT + yc) / 2 + 30), f"L = {fmt(L)} cm", 48, BLUE, anchor="rm")
    # khi quyen tac dung o mieng nhanh ho
    if pour <= 0: arrow(d, (xo, ytop - 90), (xo, ytop - 12), GRAY, w=6, head=20)
    text(d, (xo + 70, ytop - 92), "khí quyển", 44, MUTED, bold=False, anchor="lm")
    text(d, (xo + 70, ytop - 36), "p0 = 760 mmHg", 48, INK, anchor="lm")
    if show_h and h > 0.5:
        bx = xo + w + 60
        dashed(d, (XC + w, yc), (bx + 20, yc), NAVY, w=3); d.line([(xo + w, yo), (bx + 20, yo)], fill=NAVY, width=3)
        if yc - yo > 50:
            arrow(d, (bx, (yo + yc) / 2), (bx, yo + 3), RED, w=5, head=16); arrow(d, (bx, (yo + yc) / 2), (bx, yc - 3), RED, w=5, head=16)
        lbl = h_lbl if h_lbl is not None else f"h = {h:.0f} mmHg"
        text(d, (bx + 40, (yo + yc) / 2 - 30), lbl, 48, RED, anchor="lm")
        text(d, (bx + 40, (yo + yc) / 2 + 32), "độ chênh mức", 44, MUTED, bold=False, anchor="lm")

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    figure(d, t, LS[3], HS[3])
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1200, 1020, 1590), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1260), "Dự đoán", 50, PURPLE, alpha=k)
    ctext(d, 1365, "Chênh 110 mmHg: khí bị nhốt\ncó áp suất bao nhiêu?", 46, INK, maxw=900, alpha=k)
    text(d, (W / 2, 1480), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=k)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1540, 940, 1556], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1540, 140 + 800 * (1 - q), 1556], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
STEP = [0.8, 2.4, 4.0, 5.6]       # moc bat dau rot lan i (h: 0 -> 55 -> 85 -> 110 -> 165)
TR, SETTLE = 0.8, 0.4
def row_at(i): return 0.0 if i == 0 else STEP[i - 1] + TR + SETTLE
def do_state(t):
    """(L, h, pour, i_on_dinh|None) - so tren hinh = hang bang moi nhat khi on dinh."""
    i = sum(1 for s_ in STEP if t >= s_)
    if i == 0: return LS[0], HS[0], 0.0, 0
    k = ease((t - STEP[i - 1]) / TR)
    L = lerp(LS[i - 1], LS[i], k); h = lerp(HS[i - 1], HS[i], k)
    pour = 1.0 if t < STEP[i - 1] + TR else 0.0
    return L, h, pour, (i if t >= row_at(i) else None)

XS = [230, 540, 850]
def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    L, h, pour, ion = do_state(t)
    if ion is None:
        figure(d, t, L, h, show_L=False, pour=pour, h_lbl="h = …")
        text(d, (XC - 50, 640), "đợi 1 phút…", 44, MUTED, bold=False, anchor="rm")
    else:
        figure(d, t, LS[ion], HS[ion], pour=pour)
    n = sum(1 for i in range(5) if t >= row_at(i))
    kp = appear(t, M[2] + 0.2, 0.4); ka = appear(t, M[2] + 1.2, 0.45)
    yb = 1585 if ka > 0 else 1246 + max(n - 1, 0) * 52 + 46
    card(d, (60, 1165, 1020, yb), fill=WHITE, outline=NAVY, w=4)
    text(d, (XS[0], 1195), "h (mmHg)", 44, MUTED); text(d, (XS[1], 1195), "L (cm)", 44, MUTED)
    text(d, (XS[2], 1195), "p (mmHg)", 44, MUTED, alpha=1 - kp)
    if kp > 0: text(d, (XS[2], 1195), "p = p0 + h", 46, GREEN, alpha=kp)
    d.line([(90, 1222), (990, 1222)], fill=LIGHT, width=4)
    for i in range(5):
        a = appear(t, row_at(i), 0.3); y = 1246 + i * 52
        if a <= 0: continue
        if i == 3 and ka > 0: d.rounded_rectangle([80, y - 25, 1000, y + 25], radius=14, fill=A((220, 252, 231), ka))
        text(d, (XS[0], y), str(HS[i]), 46, RED, alpha=a); text(d, (XS[1], y), fmt(LS[i]), 46, BLUE, alpha=a)
        kpi = appear(t, M[2] + 0.4 + i * 0.15, 0.3)
        if kpi > 0: text(d, (XS[2], y), str(PS[i]), 46, INK, alpha=kpi)
    if ka > 0:
        lb = "ĐÁP ÁN · 870 mmHg"; pw = tw(d, lb, F(46)) + 60
        card(d, (W / 2 - pw / 2, 1502, W / 2 + pw / 2, 1572), fill=A(GREEN, ka), r=35)
        text(d, (W / 2, 1537), lb, 46, WHITE, alpha=ka)

# ---------------- canh 3: do thi p-L ----------------
GX0, GX1, GYB, GYT = 210, 970, 900, 340
LMIN, LMAX, PMIN, PMAX = 16, 23, 700, 1000
def GX(L): return GX0 + (L - LMIN) / (LMAX - LMIN) * (GX1 - GX0)
def GY(p): return GYB - (p - PMIN) / (PMAX - PMIN) * (GYB - GYT)
def s_graph(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 250, 1040, 1030), fill=WHITE, outline=LIGHT, w=3)
    for p_ in (800, 900): d.line([(GX0, GY(p_)), (GX1, GY(p_))], fill=(240, 236, 228), width=2)
    d.line([(GX0, GYB), (GX1 + 20, GYB)], fill=NAVY, width=5); d.line([(GX0, GYB), (GX0, GYT - 30)], fill=NAVY, width=5)
    for dy in (0, 16):                                   # dau ngat truc (truc khong bat dau tu 0)
        d.line([(GX0 - 16, GYB - 40 - dy), (GX0 + 16, GYB - 28 - dy)], fill=NAVY, width=4)
        d.line([(GX0 + 34 + dy, GYB + 16), (GX0 + 46 + dy, GYB - 16)], fill=NAVY, width=4)
    text(d, (GX1 + 20, GYB - 52), "L (cm)", 46, MUTED, anchor="rm")
    text(d, (GX0 + 20, GYT - 30), "p (mmHg)", 46, MUTED, anchor="lm")
    for L_ in (18, 20, 22):
        d.line([(GX(L_), GYB), (GX(L_), GYB + 12)], fill=NAVY, width=3); text(d, (GX(L_), GYB + 46), str(L_), 44, MUTED, bold=False)
    for p_ in (800, 900):
        d.line([(GX0 - 12, GY(p_)), (GX0, GY(p_))], fill=NAVY, width=3); text(d, (GX0 - 20, GY(p_)), str(p_), 44, MUTED, bold=False, anchor="rm")
    k = ease((t - M[0] - 1.4) / 1.0)                    # nhanh hypebol chi trong khoang do (17,9 - 21,8 cm)
    if k > 0:
        cur = lambda L_: (GX(L_), GY(PS[0] * LS[0] / L_))      # p = 760 x 21,8 / L (duong cong, khong noi diem)
        Ls = [22.1 - (22.1 - 16.8) * j / 106 for j in range(107)]; nn = max(2, int(len(Ls) * k))
        for j in range(nn - 1):
            La, Lb = Ls[j], Ls[j + 1]
            if 17.9 <= Lb and La <= 21.8: d.line([cur(La), cur(Lb)], fill=A(BLUE, 0.85), width=4)   # trong khoang do: lien
            elif j % 4 < 2: d.line([cur(La), cur(Lb)], fill=A(BLUE, 0.6), width=3)                  # ngoai khoang: net dut
        text(d, (GX(20.6), GY(900)), "nhánh hypebol", 44, BLUE, alpha=appear(t, M[0] + 2.2))
    for i in range(5):
        a = appear(t, M[0] + 0.2 + i * 0.22, 0.35)
        if a > 0: dot(d, GX(LS[i]), GY(PS[i]), 15 * back(a), ORANGE, WHITE)

# ---------------- canh 4: rut ra + chua noi duoc ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    yc, yo, xo = jtube(d, t, LS[4], HS[4], xc=260, yct=420, s=0.9)
    S, w, _, yb, ytop = geo(260, 420, 0.9)
    k0 = appear(t, 0.3); ya = yo + 70
    arrow(d, (xo + 120, ya), (xo + w + 10, ya), A(ORANGE, k0), w=5, head=16)
    text(d, (xo + 140, ya - 30), "đè lên khí", 44, ORANGE, bold=False, anchor="lm", alpha=k0)
    text(d, (xo + 140, ya + 30), "như pittông", 48, ORANGE, anchor="lm", alpha=k0)
    k1 = appear(t, 0.9); bx = xo + w + 30
    d.line([(260 + w, yc), (bx + 16, yc)], fill=A(RED, k1), width=3); d.line([(xo + w, yo), (bx + 16, yo)], fill=A(RED, k1), width=3)
    d.line([(bx, yo), (bx, yc)], fill=A(RED, k1), width=5)
    my = (yo + yc) / 2 + 90
    text(d, (xo + 140, my - 30), "độ chênh h", 44, RED, bold=False, anchor="lm", alpha=k1)
    text(d, (xo + 140, my + 30), "như áp kế", 48, RED, anchor="lm", alpha=k1)
    kf = appear(t, M[0] + 1.6); k2 = appear(t, M[1] - 0.1)
    if kf > 0 and k2 < 1:
        a = kf * (1 - k2)
        card(d, (80, 1190, 1000, 1500), fill=A(WHITE, a), outline=A(GREEN, a), w=6)
        rich(d, W / 2, 1295, "p_{1}V_{1} = p_{2}V_{2}", 84, GREEN, alpha=a)
        text(d, (W / 2, 1420), "T không đổi", 48, INK, bold=False, alpha=a)
    if k2 > 0:
        card(d, (80, 1190, 1000, 1560), fill=A(WHITE, k2), outline=A(BLUE, k2), w=6)
        text(d, (W / 2, 1255), "Chưa nói được gì?", 48, BLUE, alpha=k2)
        text(d, (W / 2, 1355), "Chỉ đo từ 760 đến 925 mmHg.", 46, INK, alpha=k2)
        text(d, (W / 2, 1455), "Nhiệt độ đổi thì chưa biết.", 46, INK, bold=False, alpha=k2)

# ---------------- canh 5: bay ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]; mk = M[1]
    a = appear(t, 0.1)
    card(d, (60, 260, 1020, 520), fill=A(WHITE, a), outline=A(RED, a), w=6)
    text(d, (W / 2, 315), "Bẫy trong đề", 46, RED, alpha=a)
    s = "“Rót thêm chất lỏng, p·V tăng”"; sw = tw(d, s, F(48))
    text(d, (W / 2 - 20, 410), s, 48, INK, alpha=a)
    g = ease((t - mk) / 0.4)
    if g > 0:
        x0 = W / 2 - 20 - sw / 2 - 10
        d.line([(x0, 410), (x0 + (sw + 20) * g, 410)], fill=RED, width=7)
        text(d, (W / 2 - 20 + sw / 2 + 44, 410), "✗", 56, RED, alpha=g)
    # bang da do (p, L hien san); cot p.L chi hien SAU khi gach
    card(d, (60, 560, 1020, 1080), fill=A(WHITE, a), outline=A(LIGHT, a), w=4)
    xs = [220, 470, 790]
    for x, c in zip(xs, ["p (mmHg)", "L (cm)", "p·L (10⁴ mmHg·cm)"]): text(d, (x, 610), c, 44, MUTED, alpha=a)
    d.line([(90, 645), (990, 645)], fill=A(LIGHT, a), width=4)
    for i in range(5):
        y = 695 + i * 74
        text(d, (xs[0], y), str(PS[i]), 48, INK, alpha=a); text(d, (xs[1], y), fmt(LS[i]), 48, BLUE, alpha=a)
        c = appear(t, mk + 0.2 + i * 0.3, 0.3)
        if c > 0: text(d, (xs[2], y), "≈ " + fmt(PL[i], 2), 48, GREEN, alpha=c)
    c3 = appear(t, M[2] + 0.4)
    if c3 > 0:
        card(d, (60, 1130, 1020, 1270), fill=A((220, 252, 231), c3), r=26)
        text(d, (W / 2, 1200), "✓ p tăng, L giảm, p·V giữ nguyên", 48, GREEN, alpha=c3)

# ---------------- canh 6: chot ----------------
def mini(d, t, k):                                   # ong chu J phong to (x1,7) ben trai, co vach h
    if k < 0.5: return
    xc, yct, sc_ = 180, 960, 0.6
    yc, yo, xo = jtube(d, t, 18.2, 150, xc=xc, yct=yct, s=sc_, mol=False)
    S, w, _, yb, ytop = geo(xc, yct, sc_)
    text(d, (xc - w - 14, (yct + yc) / 2), "?", 72, PURPLE, anchor="rm")
    bx = xo + w + 26
    d.line([(xc + w, yc), (bx + 14, yc)], fill=RED, width=3); d.line([(xo + w, yo), (bx + 14, yo)], fill=RED, width=3)
    d.line([(bx, yo), (bx, yc)], fill=RED, width=5)
    text(d, (bx + 24, (yo + yc) / 2), "h", 52, RED, anchor="lm")

def s_end(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    chot_hoi(d, t, sc, "Cùng ống, cùng lượng khí",
             "Mức hai nhánh chênh 150 mmHg: cột khí dài bao nhiêu?", None, body=mini)
    kh = appear(t, M[0] + 2.5, 0.5)
    if kh > 0:
        card(d, (430, 1140, 1000, 1400), fill=A((255, 247, 237), kh), r=24)
        text(d, (715, 1210), "Gợi ý", 44, MUTED, bold=False, alpha=kh)
        text(d, (715, 1285), "Vẫn một lượng khí", 46, ORANGE, alpha=kh)
        text(d, (715, 1345), "nhốt kín", 46, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, g, tr, e = sc["hook"], sc["do"], sc["graph"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][2] + 1.2, "ding"), (tr["t0"] + tr["M"][1], "buzz"),
            (tr["t0"] + tr["M"][2] + 0.4, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-boylecharles-03", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Định luật Boyle · thachlab.id.vn", scenes=[
 dict(key="hook", title="Ống chữ J một đầu kín", draw=s_hook, tail=0.4, caps=[
   ("Khí nhốt trong nhánh kín.", 2.9),
   ("Em đoán thử.", 5.3)]),
 dict(key="do", title="Rót thêm chất lỏng", draw=s_do, tail=0.4, caps=[
   ("Rót thêm, đợi 1 phút mỗi lần.", 3.8),
   ("Cột khí ngắn dần.", 3.0),
   ("Chất lỏng đè thêm lên khí.", 3.8)]),
 dict(key="graph", title="Đồ thị p theo L", draw=s_graph, tail=0.4, caps=[
   ("p tăng thì L giảm.", 3.6)]),
 dict(key="trap", title="Cái bẫy rót thêm", draw=s_trap, tail=0.4, caps=[
   ("Đúng không?", 2.5),
   ("Nhân p với L.", 3.2),
   ("Khí nhốt kín, không thêm phân tử.", 3.8)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.4, caps=[
   ("Cột chất lỏng làm hai việc.", 4.0),
   ("Giới hạn thí nghiệm.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Thử tính.", 5.2)]),
])
