# Clip: tn-l9-conang-02 - Con lac vuong dinh: vat len lai toi dau? (KHTN 9, lo 6, 18/11/2026)
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

def board(d, nail_a=1.0, line=True, label=True):
    card(d, (70, 280, 1010, 1080), fill=WOOD, outline=WOOD_D, r=20, w=5)
    d.rectangle([PX - 70, PY - 22, PX + 70, PY], fill=NAVY)                 # gia treo
    dot(d, PX, PY, 9, WHITE, outline=NAVY)
    if line:
        dashed(d, (95, YA), (985, YA), RED, w=5)
    if nail_a > 0:
        dot(d, NXY[0], NXY[1], 11, A(NAVY, nail_a))
        text(d, (NXY[0] + 30, NXY[1]), "đinh", 40, NAVY, anchor="lm", alpha=nail_a)

def vach_label(d):
    """Nhan ve SAU day/vat: nen go che day phia sau chu."""
    w = tw(d, "vạch ngang", F(40))
    d.rounded_rectangle([380 - w / 2 - 10, YA - 58, 380 + w / 2 + 10, YA - 12], radius=10, fill=WOOD)
    text(d, (380, YA - 34), "vạch ngang", 40, RED)

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

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    board(d)
    p, k = bob_at(True, -1); pendulum(d, p, k)
    text(d, (p[0] + 4, p[1] - 58), "A", 44, NAVY)
    dashed(d, (PX, PY), (PX, YB + 30), A(GRAY, 0.9), w=3, dash=10, gap=10)
    vach_label(d)
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1110, 1020, 1520), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1165), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1270, "Thả từ A, dây vướng đinh.\nBên kia lên cao tới đâu?", 44, INK, alpha=k)
    text(d, (W / 2, 1390), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=appear(t, sc["M"][1] + 0.2))
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1462, 940, 1476], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1462, 140 + 800 * (1 - q), 1476], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
R1, NAIL_IN, R2 = 0.6, 3.3, 4.1              # tha lan 1, dong dinh, tha lan 2 (giay trong canh)
def do_state(t):
    """(lan, nail, tau, so 'len duoc' dang hien hay None)."""
    if t < NAIL_IN:
        tau = min(t - R1, TP[False]); up = fm(HM) if tau >= TAPEX[False] else None
        return 1, False, tau, up
    tau = t - R2
    if tau >= 2 * TP[True]: tau = 2 * TP[True]                       # bat lai o A sau hai lan dao dong
    up = fm(HM) if tau >= TAPEX[True] else None
    return 2, True, tau, up

def readout(d, run, up, nail):
    card(d, (60, 1110, 1020, 1330), fill=WHITE, outline=LIGHT, r=26, w=4)
    text(d, (W / 2, 1160), f"Lần {run}: " + ("dây vướng đinh" if nail else "chưa có đinh"), 42, NAVY)
    text(d, (300, 1260), "thả từ " + fm(HM) + " m", 42, ORANGE)
    text(d, (770, 1260), "lên được " + (up + " m" if up else "?"), 42, BLUE)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    run, nail, tau, up = do_state(t)
    na = appear(t, NAIL_IN, 0.5)
    board(d, nail_a=na)
    trace(d, nail, tau, ORANGE if nail else GRAY)
    p, k = bob_at(nail, tau); pendulum(d, p, k)
    if up and tau >= TAPEX[nail]:
        bx = PX + LM * S * math.sin(-PHI0) if not nail else NXY[0] + RM * S * math.sin(math.acos(1 - HM / RM))
        d.ellipse([bx - 40, YA - 40, bx + 40, YA + 40], outline=GREEN, width=6)
    vach_label(d)
    readout(d, run, up, nail)

# ---------------- canh 3: dap an ----------------
PHB = math.acos(1 - HM / RM)                  # goc dinh cung ben phai (quanh dinh)
def s_ans(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    board(d, label=False)
    a0 = appear(t, 0.2, 0.6)
    pa = (PX + LM * S * math.sin(PHI0), PY + LM * S * math.cos(PHI0))
    pb = (NXY[0] + RM * S * math.sin(PHB), NXY[1] + RM * S * math.cos(PHB))
    d.line(arc_pts((PX, PY), LM * S, PHI0, 0), fill=A(GRAY, a0), width=7)                   # cung lon (trai)
    d.line(arc_pts(NXY, RM * S, 0, PHB), fill=A(ORANGE, a0), width=7)                         # cung nho (phai)
    a1 = appear(t, M[0] + 0.6, 0.5)
    pts = arc_pts((PX, PY), LM * S, 0, -PHI0)
    for i in range(0, len(pts) - 1, 4): d.line(pts[i:i + 3], fill=A(GRAY, 0.7 * a1), width=5)  # cung lon neu khong co dinh
    text(d, (860, 790), "cung nhỏ hơn", 40, ORANGE, alpha=a1)
    dot(d, pa[0], pa[1], 28, A(BOB, 0.45), outline=A(NAVY, 0.45))
    pendulum(d, pb, NXY)
    h_arrow(d, 120, "", ORANGE, alpha=a0); text(d, (150, YA - 60), fm(HM) + " m", 40, ORANGE, alpha=a0, anchor="lm")
    a2 = appear(t, M[1] - 0.1, 0.4)
    if a2 > 0:
        h_arrow(d, 960, "", BLUE, alpha=a2); text(d, (930, YA - 60), fm(HM) + " m", 40, BLUE, alpha=a2, anchor="rm")
        card(d, (110, 1140, 970, 1250), fill=A(GREEN, a2), r=50)
        text(d, (W / 2, 1195), "ĐÁP ÁN · lên tới đúng vạch ngang", 44, WHITE, alpha=a2)

# ---------------- canh 4: rut ra (chay lai + thanh nang luong) ----------------
RR, SLOW_R = 0.5, 4.0
TBOT = next(s[0] for a_, s in zip(SIM[True], SIM[True][1:]) if a_[1] < 0 <= s[1])   # luc vat qua diem thap nhat
def rut_tau(t, sc):
    """Pha 1 (phu de 1): A -> diem thap nhat; pha 2 (phu de 2): diem thap nhat -> dinh ben dinh. Chieu cham x4."""
    m1 = sc["M"][1]
    if t < m1: return min(max(t - RR, 0) / SLOW_R, TBOT) if t >= RR else -1
    return min(TBOT + (t - m1 - 0.1) / SLOW_R, TAPEX[True]) if t > m1 + 0.1 else TBOT
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    tau = rut_tau(t, sc)
    board(d)
    p, k = bob_at(True, tau); pendulum(d, p, k); vach_label(d)
    wt = clamp(height_m(p) / HM); wd = 1 - wt
    card(d, (60, 1110, 1020, 1560), fill=WHITE, outline=LIGHT, w=4)
    text(d, (W / 2, 1165), "cơ năng = thế năng + động năng", 42, INK)
    x0, x1, yb0, yb1 = 110, 970, 1240, 1320
    L = x1 - x0
    if wt * L > 2: d.rectangle([x0, yb0, x0 + wt * L, yb1], fill=ORANGE)
    if wd * L > 2: d.rectangle([x0 + wt * L, yb0, x1, yb1], fill=BLUE)
    d.rectangle([x0, yb0, x1, yb1], outline=NAVY, width=4)
    d.rectangle([150, 1360, 190, 1400], fill=ORANGE); text(d, (205, 1380), "thế năng", 40, INK, anchor="lm")
    d.rectangle([520, 1360, 560, 1400], fill=BLUE); text(d, (575, 1380), "động năng", 40, INK, anchor="lm")
    text(d, (W / 2, 1445), "Thế năng tỉ lệ với độ cao", 40, INK, alpha=appear(t, sc["M"][0] + 1.0))
    text(d, (W / 2, 1510), "Tổng không đổi", 42, GREEN, alpha=appear(t, sc["M"][1] + 0.3))
    text(d, (990, 1048), "chiếu chậm", 40, MUTED, bold=False, anchor="rm")

# ---------------- canh 5: chua noi duoc + bay ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.1)
    card(d, (60, 270, 1020, 470), fill=WHITE, outline=BLUE, w=6)
    text(d, (W / 2, 325), "Chưa nói được:", 46, BLUE, alpha=a)
    text(d, (W / 2, 405), "Thực tế: thấp hơn vạch 1–2 mm.", 42, INK, alpha=a)
    b = appear(t, M[1] - 0.05, 0.3)
    if b <= 0: return
    x = appear(t, M[1] + 2.3, 0.3)
    hh = 1180 if x > 0 else 760
    card(d, (60, 590, 1020, hh), fill=A(WHITE, b), outline=A(RED, b), w=6)
    text(d, (W / 2, 650), "Bẫy:", 44, RED, alpha=b)
    q = "“Cung ngắn hơn thì lên thấp hơn”"; qw = tw(d, q, F(44))
    text(d, (W / 2, 715), q, 44, INK, alpha=b)
    if x <= 0: return
    d.line([(W / 2 - qw / 2 - 6, 717), (W / 2 + qw / 2 + 6, 717)], fill=A(RED, x), width=6)
    text(d, (W / 2 + qw / 2 + 30, 715), "✗", 48, RED, anchor="lm", alpha=x)
    # hinh nho: hai cung, hai dau cung cung mot vach
    cx, cy, sc_ = W / 2, 760, 0.42
    def P(xp, yp): return (cx + (xp - PX) * sc_, cy + (yp - PY) * sc_)
    pa = P(PX + LM * S * math.sin(PHI0), PY + LM * S * math.cos(PHI0))
    pb = P(NXY[0] + RM * S * math.sin(PHB), NXY[1] + RM * S * math.cos(PHB))
    yl = P(0, YA)[1]
    dashed(d, (cx - 260, yl), (cx + 260, yl), A(RED, x), w=4, dash=12, gap=8)
    d.line([P(*q_) for q_ in arc_pts((PX, PY), LM * S, PHI0, 0)], fill=A(GRAY, x), width=5)
    d.line([P(*q_) for q_ in arc_pts(NXY, RM * S, 0, PHB)], fill=A(ORANGE, x), width=5)
    dot(d, pa[0], pa[1], 14, A(BOB, x)); dot(d, pb[0], pb[1], 14, A(BOB, x))
    text(d, (W / 2, 1130), "✓ Hai đầu cung ngang nhau", 42, GREEN, alpha=x)

# ---------------- canh 6: chot + cau hoi (the chot hien SAU thoi gian nghi) ----------------
T_CHOT = 4.0
def s_end(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 620, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(38)) + 52
        card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 682), "THỬ NGHĨ", 38, WHITE, alpha=k1)
        ctext(d, 790, "Ở 0,10 m bên kia, động năng\nbằng bao nhiêu % cơ năng?", 44, INK, maxw=940,
              alpha=appear(t, M[0] + 0.4, 0.5))
        # hinh nho: day 1 m, dinh 0,70 m duoi diem treo; A cao 0,25 m (trai), vat cao 0,10 m ben dinh (phai)
        ka = appear(t, M[0] + 0.6, 0.5) * k1
        s2 = 0.6; cx, cy = 540, 880
        L2, d2, r2 = LM * S * s2, 0.70 * S * s2, 0.30 * S * s2
        pa_ = -math.acos(1 - 0.25 / LM); pb_ = math.acos(1 - 0.10 / 0.30)
        a = (cx + L2 * math.sin(pa_), cy + L2 * math.cos(pa_)); yb = cy + L2
        nx, ny = cx, cy + d2
        b = (nx + r2 * math.sin(pb_), ny + r2 * math.cos(pb_))
        d.rectangle([cx - 40, cy - 12, cx + 40, cy], fill=A(NAVY, ka))
        dashed(d, (cx, cy), a, A(GRAY, ka), w=3, dash=10, gap=8)
        d.line([(cx, cy), (nx, ny), b], fill=A(NAVY, ka), width=4)
        dot(d, nx, ny, 9, A(NAVY, ka)); text(d, (nx - 22, ny - 4), "đinh", 40, NAVY, anchor="rm", alpha=ka)
        dot(d, a[0], a[1], 16, A(BOB, 0.45 * ka), outline=A(NAVY, 0.45 * ka))
        text(d, (a[0], a[1] - 46), "A", 40, NAVY, alpha=ka)
        dot(d, b[0], b[1], 18, A(BOB, ka), outline=A(NAVY, ka))
        dashed(d, (a[0] - 100, yb), (b[0] + 150, yb), A(GRAY, ka), w=3, dash=10, gap=8)
        arrow(d, (a[0] - 60, yb), (a[0] - 60, a[1] + 4), A(ORANGE, ka), w=5, head=16)
        text(d, (a[0] - 76, (a[1] + yb) / 2), "0,25 m", 40, ORANGE, anchor="rm", alpha=ka)
        arrow(d, (b[0] + 70, yb), (b[0] + 70, b[1] + 4), A(BLUE, ka), w=5, head=14)
        text(d, (b[0] + 90, (b[1] + yb) / 2 - 10), "0,10 m", 40, BLUE, anchor="lm", alpha=ka)
        kh = appear(t, M[0] + 2.6, 0.5)
        if kh > 0:
            card(d, (110, 1370, 970, 1540), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
            text(d, (W / 2, 1415), "Gợi ý", 40, ORANGE, alpha=kh)
            ctext(d, 1485, "Mốc thế năng ở chỗ thấp nhất", 42, INK, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 410, "Bỏ qua lực cản: cơ năng không đổi", 50, GREEN, maxw=860, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.5, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + R1 + TAPEX[False], "tap"), (do["t0"] + R2 + TAPEX[True], "tap"),
            (an["t0"] + an["M"][1] - 0.1, "ding"), (tr["t0"] + tr["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l9-conang-02", header="KHTN 9 · THÍ NGHIỆM", cues=_cues,
    footer="Cơ năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Con lắc và cái đinh", draw=s_hook, tail=0.6, caps=[
   ("Kẻ vạch ngang ngang tầm A.", 2.6),
   ("Nghĩ kĩ rồi mới xem tiếp.", 5.6)]),
 dict(key="do", title="Thả nhẹ từ A", draw=s_do, tail=0.6, caps=[
   ("Lần 1: chưa đóng đinh.", 3.4),
   ("Lần 2: dây vướng đinh.", 4.0)]),
 dict(key="ans", title="So hai bên vạch ngang", draw=s_ans, tail=0.6, caps=[
   ("Bên phải: cung nhỏ hơn.", 2.8),
   ("Độ cao vẫn như lúc thả.", 3.4)]),
 dict(key="rut", title="Vì sao lên đúng vạch?", draw=s_rut, tail=0.5, caps=[
   ("Đi xuống: thế năng thành động năng.", 3.0),
   ("Đi lên: đổi ngược lại.", 3.2)]),
 dict(key="trap", title="Giới hạn và cái bẫy", draw=s_trap, tail=0.5, caps=[
   ("Giới hạn của thí nghiệm.", 3.2),
   ("Đúng không? Nhìn vạch ngang.", 4.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Tự trả lời trước khi xem.", 6.2)]),
])
