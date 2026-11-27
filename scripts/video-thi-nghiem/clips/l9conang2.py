# Clip: tn-l9-conang-02 - Con lac vuong dinh: vat len lai toi dau? (KHTN 9, lo 6, 18/11/2026)
# Dung lai theo cong moi 27/11/2026 (Viec 4 L9 nhom C): chu >= 56, canh <= 180 tu/phut, khoi chu cach >= 2,5 s, K10,
#   Bay hai cung canh nhau (o ✓ >= 3 s), Chua noi = luc can lam hut bao nhieu (chua do).
#   Chot (ca MOI, tu suy trong dai tham_so): h = 0,20 m, dinh d = 0,70 m (r = 0,30 m > h nen day cang), ben dinh o do cao
#   0,05 m: Wd = 10m(0,20 - 0,05) -> 0,15 : 0,20 = 75 % co nang (moc the nang o cho thap nhat, bo qua luc can).
#   (Kho ghi_chu de xuat 0,25 m -> 60 %, nhung 0,25 m ngoai dai tham_so h 0,05-0,20 -> dung 0,20 m.)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-conang-02.json:
#   tham_so: day dai 1 m (gia_thiet) ; h = 0,15 m ; d (dinh duoi diem treo) = 0,5 m ; h_len = h (bo qua luc can)
#   so_lieu_mau: h tha 0,15 m -> h len 0,15 m ; ghi_chu: thuc te thap hon 1-2 mm.
# Chuyen dong: tich phan phi'' = -(g/R) sin(phi), R = 1 m ben trai, 0,5 m ben phai (vuong dinh), omega doi theo v lien tuc.
# Canh: Du doan (chi cau hoi + hinh, K10) -> Tien hanh (lan 1 khong dinh, lan 2 co dinh, so "len duoc" hien dung luc vat
#   o dinh cung) -> DAP AN · len toi dung vach ngang -> Rut ra (chay lai + thanh the nang/dong nang, tong khong doi)
#   -> Chua noi duoc + bay "cung ngan hon -> len thap hon" ✗ -> Chot + THU NGHI (h = 0,20 m, dinh 0,70 m -> 0,20 m).
# Lua chon Du doan (o khung web): A. Thap hon vach ngang · B. Dung ngang vach (dung) · C. Cao hon vach ngang
#   · D. Khong len duoc vi day vuong dinh.
from engine import *

G, LM, HM, DM = 9.8, 1.0, 0.15, 0.5          # g, dai day (m), do cao tha (m), dinh duoi diem treo (m)
RM = LM - DM                                   # ban kinh phan day duoi dinh
S = 700                                        # px moi m
PX, PY = 540, 330                              # diem treo
NXY = (PX, PY + DM * S)                        # dinh
YB = PY + LM * S                               # vi tri thap nhat
YA = YB - HM * S                               # vach ngang (ngang tam A)
PHI0 = -math.acos(1 - HM / LM)
WOOD = (236, 214, 178); WOOD_D = (160, 120, 70); BOB = (37, 99, 235)
def fm(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def sim(nail, T=6.0, dt=1 / 1200):
    """Tra ve danh sach (t, phi, omega) tu luc tha o A."""
    out = []; phi, om, t = PHI0, 0.0, 0.0
    while t <= T:
        out.append((t, phi, om))
        R = RM if (nail and phi > 0) else LM
        a = -(G / R) * math.sin(phi)
        om2 = om + a * dt; phi2 = phi + om2 * dt
        if nail and phi <= 0 < phi2: om2 *= LM / RM          # vuong dinh: v lien tuc
        if nail and phi > 0 >= phi2: om2 *= RM / LM          # roi dinh
        phi, om, t = phi2, om2, t + dt
    return out
SIM = {False: sim(False), True: sim(True)}
def period(nail):
    s = SIM[nail]
    for i in range(1, len(s)):
        if s[i - 1][2] < 0 <= s[i][2] and s[i][1] < 0: return s[i][0]    # quay lai A
def apex_r(nail):
    s = SIM[nail]
    for i in range(1, len(s)):
        if s[i - 1][2] > 0 >= s[i][2] and s[i][1] > 0: return s[i][0]    # dinh cung ben phai
TP = {k: period(k) for k in (False, True)}; TAPEX = {k: apex_r(k) for k in (False, True)}

def bob_at(nail, tau):
    """Vi tri vat (px) va diem gay day sau tau giay ke tu luc tha; tau < 0: dang giu o A."""
    if tau <= 0: phi = PHI0
    else:
        s = SIM[nail]; i = min(int(tau * 1200), len(s) - 1); phi = s[i][1]
    if nail and phi > 0:
        return (NXY[0] + RM * S * math.sin(phi), NXY[1] + RM * S * math.cos(phi)), NXY
    return (PX + LM * S * math.sin(phi), PY + LM * S * math.cos(phi)), None
def height_m(p): return (YB - p[1]) / S

def dashed(d, p1, p2, color, w=4, dash=18, gap=12):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (dash + gap)) + 1
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def arc_pts(c, R, a0, a1, n=60):
    return [(c[0] + R * math.sin(lerp(a0, a1, k / n)), c[1] + R * math.cos(lerp(a0, a1, k / n))) for k in range(n + 1)]

def board(d, nail_a=1.0, line=True, label=True, col=RED):
    card(d, (70, 280, 1010, 1080), fill=WOOD, outline=WOOD_D, r=20, w=5)
    d.rectangle([PX - 70, PY - 22, PX + 70, PY], fill=NAVY)                 # gia treo
    dot(d, PX, PY, 9, WHITE, outline=NAVY)
    if line:
        dashed(d, (95, YA), (985, YA), col, w=5 if col == RED else 4)
    if nail_a > 0:
        dot(d, NXY[0], NXY[1], 11, A(NAVY, nail_a))
        text(d, (NXY[0] + 30, NXY[1]), "đinh", 56, NAVY, anchor="lm", alpha=nail_a)

def vach_label(d, col=RED):
    """Nhan ve SAU day/vat: nen go che day phia sau chu. (Du doan/Tien hanh: xam, chi do tu canh dap an.)"""
    w = tw(d, "vạch ngang", F(56))
    d.rounded_rectangle([380 - w / 2 - 10, YA + 12, 380 + w / 2 + 10, YA + 74], radius=10, fill=WOOD)
    text(d, (380, YA + 42), "vạch ngang", 56, col)

def pendulum(d, p, kink, alpha=1.0):
    pts = [(PX, PY)] + ([kink] if kink else []) + [p]
    d.line(pts, fill=A(NAVY, alpha), width=4, joint="curve")
    dot(d, p[0], p[1], 28, A(BOB, alpha), outline=A(NAVY, alpha))

def h_arrow(d, x, label, col, alpha=1.0, side="l"):
    arrow(d, (x, YB), (x, YA + 4), A(col, alpha), w=6, head=20)
    arrow(d, (x, YA), (x, YB - 4), A(col, alpha), w=6, head=20)
    if side == "l": text(d, (x - 18, (YA + YB) / 2), label, 40, col, anchor="rm", alpha=alpha)
    else: text(d, (x + 18, (YA + YB) / 2), label, 40, col, anchor="lm", alpha=alpha)

def trace(d, nail, tau, color):
    if tau <= 0: return
    s = SIM[nail]; n = min(int(tau * 1200), len(s) - 1); pts = []
    for i in range(0, n + 1, 12):
        p, _ = bob_at(nail, s[i][0] + 1e-6); pts.append(p)
    if len(pts) > 1: d.line(pts, fill=A(color, 0.55), width=6, joint="curve")

DRED = (185, 28, 28); DGREEN = (21, 110, 55)
def pill(d, s, y, a, color, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    board(d, col=GRAY)
    p, k = bob_at(True, -1); pendulum(d, p, k)
    text(d, (p[0] + 4, p[1] - 66), "A", 58, NAVY)
    dashed(d, (PX, PY), (PX, YB + 30), A(GRAY, 0.9), w=3, dash=10, gap=10)
    vach_label(d, GRAY)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1110 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 460), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 160), "Dây vướng đinh.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 240), "Bên kia, vật lên tới đâu?", 58, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p_ = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 320, 970, y0 + 410], radius=45, fill=A((237, 233, 254), a))
        if p_ < 1: d.rounded_rectangle([110, y0 + 320, 110 + max(90, 860 * (1 - p_)), y0 + 410], radius=45, fill=A((76, 29, 149), a))

# ---------------- canh 2: tien hanh ----------------
R1, NAIL_IN, R2 = 0.6, 3.6, 4.3
def do_state(t):
    if t < NAIL_IN:
        tau = min(t - R1, TP[False]); up = fm(HM) if tau >= TAPEX[False] else None
        return 1, False, tau, up
    tau = t - R2
    if tau >= 2 * TP[True]: tau = 2 * TP[True]
    up = fm(HM) if tau >= TAPEX[True] else None
    return 2, True, tau, up

def readout(d, up):
    card(d, (60, 1120, 1020, 1330), fill=WHITE, outline=LIGHT, r=26, w=4)
    text(d, (300, 1180), "thả từ", 56, ORANGE); text(d, (300, 1270), fm(HM) + " m", 60, ORANGE)
    text(d, (770, 1180), "lên được", 56, BLUE); text(d, (770, 1270), (up + " m") if up else "?", 60, BLUE)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    run, nail, tau, up = do_state(t)
    na = appear(t, NAIL_IN, 0.5)
    board(d, nail_a=na, col=GRAY)
    trace(d, nail, tau, ORANGE if nail else GRAY)
    p, k = bob_at(nail, tau); pendulum(d, p, k)
    if up and tau >= TAPEX[nail]:
        bx = PX + LM * S * math.sin(-PHI0) if not nail else NXY[0] + RM * S * math.sin(math.acos(1 - HM / RM))
        d.ellipse([bx - 40, YA - 40, bx + 40, YA + 40], outline=GREEN, width=6)
    vach_label(d, GRAY)
    readout(d, up)

# ---------------- canh 3: dap an ----------------
PHB = math.acos(1 - HM / RM)
def s_ans(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    board(d)
    a0 = appear(t, 0.2, 0.6)
    pa = (PX + LM * S * math.sin(PHI0), PY + LM * S * math.cos(PHI0))
    pb = (NXY[0] + RM * S * math.sin(PHB), NXY[1] + RM * S * math.cos(PHB))
    d.line(arc_pts((PX, PY), LM * S, PHI0, 0), fill=A(GRAY, a0), width=7)
    d.line(arc_pts(NXY, RM * S, 0, PHB * clamp((t - 0.4) / 1.2)), fill=A(ORANGE, a0), width=9)
    a1 = appear(t, M[0] + 1.0, 0.5)
    pts = arc_pts((PX, PY), LM * S, 0, -PHI0)
    for i in range(0, len(pts) - 1, 4): d.line(pts[i:i + 3], fill=A(GRAY, 0.7 * a1), width=5)
    dot(d, pa[0], pa[1], 28, A(BOB, 0.45), outline=A(NAVY, 0.45))
    pendulum(d, pb, NXY)
    vach_label(d)
    h_arrow(d, 120, "", ORANGE, alpha=a0)
    a2 = appear(t, M[1] - 0.1, 0.4)
    if a2 > 0:
        h_arrow(d, 960, "", BLUE, alpha=a2)
        pill(d, "ĐÁP ÁN: đúng vạch ngang", 1200, a2, GREEN, 58)

# ---------------- canh 4: rut ra (chay lai + thanh nang luong) ----------------
RR, SLOW_R = 0.5, 4.0
TBOT = next(s[0] for a_, s in zip(SIM[True], SIM[True][1:]) if a_[1] < 0 <= s[1])
def rut_tau(t, sc):
    m1 = sc["M"][1]
    if t < m1: return min(max(t - RR, 0) / SLOW_R, TBOT) if t >= RR else -1
    return min(TBOT + (t - m1 - 0.1) / SLOW_R, TAPEX[True]) if t > m1 + 0.1 else TBOT
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    tau = rut_tau(t, sc)
    board(d)
    vach_label(d); p, k = bob_at(True, tau); pendulum(d, p, k)      # nhan truoc, con lac sau: qua nang khong bi che
    text(d, (980, 1030), "chiếu chậm", 56, NAVY, anchor="rm")
    wt = clamp(height_m(p) / HM); wd = 1 - wt
    card(d, (40, 1110, 1040, 1520), fill=WHITE, outline=LIGHT, w=4)
    x0, x1, yb0, yb1 = 110, 970, 1170, 1260
    L = x1 - x0
    if wt * L > 2: d.rectangle([x0, yb0, x0 + wt * L, yb1], fill=ORANGE)
    if wd * L > 2: d.rectangle([x0 + wt * L, yb0, x1, yb1], fill=BLUE)
    d.rectangle([x0, yb0, x1, yb1], outline=NAVY, width=4)
    d.rectangle([110, 1305, 160, 1355], fill=ORANGE); text(d, (180, 1330), "thế năng", 56, INK, anchor="lm")
    d.rectangle([560, 1305, 610, 1355], fill=BLUE); text(d, (630, 1330), "động năng", 56, INK, anchor="lm")
    text(d, (W / 2, 1440), "tổng không đổi", 58, DGREEN, alpha=appear(t, sc["M"][1] + 0.3))

# ---------------- canh 5: bay + chua noi duoc ----------------
BAY_ST = 2.2
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.2, 0.4)
    k2 = appear(t, M[2] - 0.1, 0.45)
    # hinh tu giai thich: cung lon (trai) va cung nho (phai), hai dau cung tren mot vach do
    card(d, (40, 260, 1040, 720), fill=A(WOOD, a), outline=A(WOOD_D, a), w=4)
    cx, cy, sc_ = W / 2, 300, 0.55
    def P(xp, yp): return (cx + (xp - PX) * sc_, cy + (yp - PY) * sc_)
    pa = P(PX + LM * S * math.sin(PHI0), PY + LM * S * math.cos(PHI0))
    pb = P(NXY[0] + RM * S * math.sin(PHB), NXY[1] + RM * S * math.cos(PHB))
    yl = P(0, YA)[1]
    dashed(d, (70, yl), (1010, yl), A(RED, a), w=5, dash=14, gap=10)
    g = clamp((t - 0.4) / 1.4)
    d.line([P(*q_) for q_ in arc_pts((PX, PY), LM * S, PHI0, 0)], fill=A(GRAY, a), width=7)
    if g > 0: d.line([P(*q_) for q_ in arc_pts(NXY, RM * S, 0, PHB * g)], fill=A(ORANGE, a), width=8)
    dot(d, *P(*NXY), 8, A(NAVY, a)); q0 = P(PX, PY); d.rectangle([q0[0] - 40, q0[1] - 12, q0[0] + 40, q0[1]], fill=A(NAVY, a))
    tau = (t * 0.8) % TP[True]                                       # vat chay qua lai tren hai cung (cham)
    pq, kq = bob_at(True, max(tau, 1e-6)); pq2 = P(*pq)
    d.line([P(PX, PY)] + ([P(*kq)] if kq else []) + [pq2], fill=A(NAVY, a), width=3)
    dot(d, pq2[0], pq2[1], 18, A(BOB, a))
    text(d, (190, yl + 58), "cung lớn", 56, NAVY, alpha=a)
    text(d, (880, yl + 58), "cung nhỏ", 56, ORANGE, alpha=a)
    a1 = a * (1 - k2); y0 = 770
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        for j, q in enumerate(("“Cung nhỏ hơn", "thì lên thấp hơn”")):
            yy = y0 + 170 + j * 80; lw = tw(d, q, F(58))
            text(d, (W / 2, yy), q, 58, INK, alpha=a1)
            ks = clamp((t - BAY_ST) / 0.4)
            if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, M[1] + 0.1, 0.4)
        card(d, (70, y0 + 340, 1010, y0 + 500), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 420), "✓ Hai đầu ngang nhau", 58, DGREEN, alpha=kk)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "lực cản: hụt bao nhiêu", 58, INK, alpha=k2)
        text(d, (W / 2, y0 + 320), "(chưa đo)", 56, NAVY, alpha=k2)

# ---------------- canh 6: chot ----------------
CH_H, CH_D, CH_Y = 0.20, 0.70, 0.05      # tha 0,20 m, dinh 0,70 m duoi diem treo, hoi o do cao 0,05 m ben dinh -> 75 %
END_Q = 0.2
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 280, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 350, k1, ORANGE)
    text(d, (W / 2, 440), "Dây dài " + fm(LM) + " m. Bên đinh,", 58, INK, alpha=k1)
    text(d, (W / 2, 515), "ở độ cao " + fm(CH_Y) + " m:", 58, INK, alpha=k1)
    text(d, (W / 2, 590), "động năng = ? % cơ năng", 58, INK, alpha=k1)
    if k1 <= 0: return
    s2 = 0.62; cx, cy = 660, 660
    L2, d2, r2 = LM * S * s2, CH_D * S * s2, (LM - CH_D) * S * s2
    pa_ = -math.acos(1 - CH_H / LM); pb_ = math.acos(1 - CH_Y / (LM - CH_D))
    a = (cx + L2 * math.sin(pa_), cy + L2 * math.cos(pa_)); yb = cy + L2
    nx, ny = cx, cy + d2
    b = (nx + r2 * math.sin(pb_), ny + r2 * math.cos(pb_))
    d.rectangle([cx - 50, cy - 14, cx + 50, cy], fill=A(NAVY, k1))
    dashed(d, (cx, cy), a, A(GRAY, k1), w=3, dash=10, gap=8)
    d.line([(cx, cy), (nx, ny), b], fill=A(NAVY, k1), width=5)
    dot(d, nx, ny, 10, A(NAVY, k1)); text(d, (nx - 24, ny), "đinh", 56, NAVY, anchor="rm", alpha=k1)
    arrow(d, (cx + 40, cy + 8), (cx + 40, ny - 8), A(NAVY, k1), w=4, head=14); arrow(d, (cx + 40, ny - 8), (cx + 40, cy + 8), A(NAVY, k1), w=4, head=14)
    text(d, (cx + 64, (cy + ny) / 2), fm(CH_D) + " m", 56, NAVY, anchor="lm", alpha=k1)
    dot(d, a[0], a[1], 20, A(BOB, 0.45 * k1), outline=A(NAVY, 0.45 * k1))
    text(d, (a[0], a[1] - 56), "A", 56, NAVY, alpha=k1)
    dot(d, b[0], b[1], 22, A(BOB, k1), outline=A(NAVY, k1))
    dashed(d, (110, yb), (990, yb), A(GRAY, k1), w=3, dash=10, gap=8)
    arrow(d, (a[0] - 60, yb), (a[0] - 60, a[1] + 4), A(ORANGE, k1), w=6, head=18)
    text(d, (a[0] - 80, (a[1] + yb) / 2), fm(CH_H) + " m", 56, ORANGE, anchor="rm", alpha=k1)
    arrow(d, (b[0] + 60, yb), (b[0] + 60, b[1] + 4), A(BLUE, k1), w=6, head=14)
    text(d, (b[0] + 80, b[1] - 60), fm(CH_Y) + " m", 56, BLUE, anchor="lm", alpha=k1)
    rr = 60 + 30 * math.sin(2 * math.pi * t / 2.0)
    xc, yc = W / 2, 1400
    d.ellipse([xc - rr, yc - rr, xc + rr, yc + rr], fill=A(mix(ORANGE, WHITE, 0.45), k1))
    text(d, (xc, yc), "?", 80, WHITE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return sorted([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + R1 + TAPEX[False], "tap"), (do["t0"] + R2 + TAPEX[True], "tap"),
            (an["t0"] + an["M"][1] - 0.1, "ding"), (tr["t0"] + BAY_ST, "buzz"), (tr["t0"] + tr["M"][1] + 0.1, "tap"),
            (e["t0"] + END_Q + 0.1, "open")])

CLIP = dict(id="tn-l9-conang-02", header="KHTN 9 · THÍ NGHIỆM", cues=_cues,
    footer="Cơ năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Con lắc và cái đinh", draw=s_hook, tail=0.3, caps=[
   ("Vạch ngang tầm A.", 2.5),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Thả nhẹ từ A", draw=s_do, tail=0.3, caps=[
   ("Lần 1: chưa đóng đinh.", 3.4),
   ("Lần 2: dây vướng đinh.", 3.6)]),
 dict(key="ans", title="So hai bên vạch ngang", draw=s_ans, tail=0.7, caps=[
   ("Bên phải: cung nhỏ hơn.", 2.9),
   ("Độ cao vẫn như lúc thả.", 3.4)]),
 dict(key="rut", title="Vì sao lên đúng vạch?", draw=s_rut, tail=0.4, caps=[
   ("Xuống: thế năng thành động năng.", 3.0),
   ("Lên: đổi ngược lại.", 2.9)]),
 dict(key="trap", title="Bẫy và giới hạn", draw=s_trap, tail=0.3, caps=[
   ("Đúng không?", 4.6),
   ("Nhìn vạch đỏ.", 3.6),
   ("Còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 6.2)]),
])
