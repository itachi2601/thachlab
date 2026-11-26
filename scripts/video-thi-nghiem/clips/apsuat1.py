# Clip: tn-l12-apsuatdongnang-01 - Hat dap vao thanh hop: vo so va cham cong thanh luc deu.
# So lieu lay tu content/thi-nghiem/tn-l12-apsuatdongnang-01.json (_kiem_so() doi chieu so_lieu_mau):
#   so_lieu_mau (so hat, tan so lac Hz, so va cham vao mot thanh moi giay) - SO TINH TU MO HINH, khong phai so do:
#     100,1,125 ; 100,3,375 ; 200,1,250 ; 200,3,750 ; 400,3,1500 ; mo_hinh n_va = N_hat.v_hat/(2.l_hop).
# Ban 1-2 (28/10, 12/11/2026). Ban 3 (26/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32): cong --do-chu
#   (chu ve >= 58 px, <= 180 tu/phut moi canh, nhip >= 2,5 s), <= 50 s, K10 (khong nut A-D, khong "chon dap an").
# Du doan: lac 1 Hz -> 3 Hz, so cu dap vao thanh cam? -> gap ba (hang 3 -> 4 kho). Phuong an nhieu "khong doi, van 200 hat".
# Thu tu: Du doan -> Tien hanh (1 hat -> 200 hat 1 Hz -> 3 Hz, do thi luc len thanh cam, chieu cham)
#   -> Ket qua (3 hang 100/1, 200/1, 200/3: x3 theo lac, x2 theo so hat) -> Vi sao luc deu (1 hat: cu le; nhieu hat: tong gan deu)
#   -> Bay "hat nam yen de len thanh" (hai hop canh nhau: nam yen chi de day / chuyen dong day moi thanh) -> Chot + THU NGHI.
#   Hang 100/3 va 400/3 KHONG chieu (khong can, giu clip <= 50 s).
# Thu nghi (= cau_chot khung web, CA TU SUY theo mo_hinh): van 200 hat, lac 1 Hz, hop dai gap doi theo chieu toi thanh cam
#   -> n = N.v/(2l) giam mot nua: 250 -> 125 cu/giay. Dap so khong hien tren man (hat trong the dung yen, khong chop).
# Hinh hat chuyen dong la minh hoa CHIEU CHAM: so vach tren do thi khong bang 250/750, chi ti le day/thua (1:3) la dung.
from engine import *
import random as _rnd

ROWS = [(100, 1, 125), (200, 1, 250), (200, 3, 750)]          # so_lieu_mau hang 1, 3, 4

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-apsuatdongnang-01.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    for r in ROWS: assert r in hang, r
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["N_hat"]["mac_dinh"] == 200
    # mo hinh n = N.v/(2l), v = 0,5 f, l = 0,2 m -> 200 hat, 1 Hz: 200*0,5/0,4 = 250; hop dai gap doi -> 125
    n = lambda N, f, l: N * 0.5 * f / (2 * l)
    assert abs(n(200, 1, ts["l_hop"]["gia_tri"]) - 250) < 1e-9 and abs(n(200, 1, 2 * ts["l_hop"]["gia_tri"]) - 125) < 1e-9
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
FS = 58                                     # chu nho nhat khi ve (x0,88 = 51 px trong mp4)

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem LIEN cao 70 px, ngan dan tu phai sang trai theo 10 nac (moi nac doi hinh du ro)."""
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

# ---------------- bo cuc hop (khung 1080x1920) ----------------
R = 6                                       # ban kinh hat
LO, HI, TOP, BOT = 130, 700, 352, 888       # mien tam hat; thanh hop cach R
L = HI - LO
WALL = (LO - R, TOP - R, HI + R, BOT + R)
GRAIN = (176, 128, 52)
GX0, GX1, GTOP, GBASE = 110, 1000, 1070, 1500    # do thi luc (canh Tien hanh)
WIN = 3.0                                   # cua so do thi (giay)
H1 = 50                                     # chieu cao vach o |vx| = 250 px/s, lac 1 Hz

_r = _rnd.Random(3)
P = [(280.0, 352 + 200.0, 420.0, 200.0)]    # hat 0 (canh "mot hat")
for _ in range(199):
    u = _r.uniform(150, 330); a = _r.uniform(0, 2 * math.pi)
    P.append((_r.uniform(LO, HI), _r.uniform(TOP, BOT), u * math.cos(a), u * math.sin(a)))
PILE = []                                   # 200 hat nam yen o day
for j in range(200):
    row, col = divmod(j, 41)
    PILE.append((LO + col * L / 40 + _r.uniform(-2, 2), BOT - row * 12.5 + _r.uniform(-1.5, 1.5)))

# thoi gian "hieu dung" S(t): toc do hat x sf(t), sf = 1 -> 3 khi chuyen sang 3 Hz
_cache = {}
def timing(sc):
    k = id(sc)
    if k not in _cache:
        M = sc["M"]; tOn, tA, dr = M[1], M[2], 0.6
        def sf(t): return 1.0 if t < tA else (3.0 if t >= tA + dr else 1 + 2 * (t - tA) / dr)
        def S(t):
            if t < tA: return t
            if t < tA + dr: return t + (t - tA) ** 2 / dr
            return tA + 2 * dr + 3 * (t - tA - dr)
        ts = np.linspace(-WIN - 1, sc["T"] + 1, 6000); Ss = np.array([S(x) for x in ts])
        _cache[k] = dict(tOn=tOn, tA=tA, dr=dr, sf=sf, S=S, Sinv=lambda s: float(np.interp(s, Ss, ts)))
    return _cache[k]

def hits(tm, i, ta, tb):
    """Cac lan hat i dap thanh phai (cam) trong [ta, tb]: (thoi diem, y, chieu cao vach)."""
    x0, y0, vx, vy = P[i]
    if i > 0: ta = max(ta, tm["tOn"])
    if tb <= ta or abs(vx) < 1e-6: return []
    S, Sinv = tm["S"], tm["Sinv"]
    qa = (x0 + vx * S(ta) - LO - L) / (2 * L); qb = (x0 + vx * S(tb) - LO - L) / (2 * L)
    lo_k, hi_k = sorted((qa, qb))
    out = []
    for k in range(math.ceil(lo_k), math.floor(hi_k) + 1):
        tau = Sinv((LO + L + 2 * L * k - x0) / vx)
        if ta <= tau <= tb:
            out.append((tau, refl(y0 + vy * S(tau), TOP, BOT), H1 * abs(vx) / 250 * tm["sf"](tau)))
    return out

def box(d, dx=0.0):
    x0, y0, x1, y1 = WALL
    d.rounded_rectangle([x0 - 6 + dx, y0 - 6, x1 + 6 + dx, y1 + 6], radius=18, fill=(250, 252, 255), outline=NAVY, width=6)
    d.line([(x1 + 6 + dx, y0 + 10), (x1 + 6 + dx, y1 - 10)], fill=ORANGE, width=16)

def pile(d, alpha=1.0):
    for x, y in PILE: dot(d, x, y, R, A(GRAIN, alpha))

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    box(d); pile(d)
    ka = appear(t, 0.5, 0.4)                 # nhan "thanh cam" (ki hieu moi co nhan ngay)
    arrow(d, (850, 620), (735, 620), A(ORANGE, ka), w=7, head=24)
    text(d, (900, 690), "thành cam", FS, DORANGE, alpha=ka)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1000 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 185), "Lắc 1 Hz → 3 Hz:", 64, INK, alpha=k)
    text(d, (W / 2, y0 + 280), "số cú đập vào thành cam?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 380, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh (1 hat -> 200 hat 1 Hz -> 3 Hz, lien mach) ----------------
def chips(d, cur):
    for j, s in enumerate(("1 hạt", "1 Hz", "3 Hz")):
        x0 = 60 + j * 330; bx = (x0, 236, x0 + 300, 314)
        if j == cur: card(d, bx, fill=ORANGE, r=36); text(d, (x0 + 150, 275), s, FS, WHITE)
        elif j < cur: card(d, bx, fill=LIGHT, r=36); text(d, (x0 + 150, 275), s, FS, INK)
        else: card(d, bx, fill=WHITE, outline=GRAY, r=36, w=4); text(d, (x0 + 150, 275), s, FS, INK)

def counter(d, n, f, c, ccol=ORANGE):
    card(d, (748, WALL[1] - 6, 1040, WALL[3] + 6), fill=WHITE, outline=LIGHT, r=26, w=4)
    text(d, (894, 400), "Số hạt", FS, INK); text(d, (894, 468), n, 64, BLUE)
    text(d, (894, 565), "Lắc", FS, INK); text(d, (894, 633), f, 64, BLUE)
    text(d, (894, 730), "cú/giây", FS, INK)
    text(d, (894, 815), c, 72, ccol)

def graph(d, tm, t):
    card(d, (40, 930, 1040, 1570), fill=WHITE, outline=LIGHT, w=4)
    text(d, (80, 985), "Lực lên thành cam", FS, INK, anchor="lm")
    d.line([(GX0, GTOP - 20), (GX0, GBASE)], fill=NAVY, width=5)
    d.line([(GX0, GBASE), (GX1 + 16, GBASE)], fill=NAVY, width=5)
    arrow(d, (GX0, GTOP), (GX0, GTOP - 26), NAVY, w=5, head=18)
    arrow(d, (GX1, GBASE), (GX1 + 22, GBASE), NAVY, w=5, head=18)
    text(d, (GX0 + 26, GTOP - 10), "F", FS, INK, anchor="lm")
    text(d, (GX1 + 10, GBASE + 38), "t", FS, INK, anchor="rm")
    X = lambda tau: GX1 - (t - tau) / WIN * (GX1 - GX0)
    ta = max(-0.01, t - WIN)
    for i in range(len(P)):
        for tau, y, h in hits(tm, i, ta, t):
            x = X(tau); d.line([(x, GBASE - 3), (x, GBASE - 3 - h)], fill=A(ORANGE, 0.9), width=4)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    tm = timing(sc); M = sc["M"]
    S = tm["S"](t); dx = 7 * math.sin(2 * math.pi * S)
    stage = 0 if t < M[1] else (1 if t < M[2] else 2)
    chips(d, stage)
    box(d, dx)
    ka = appear(t, tm["tOn"], 0.4)
    for i, (x0, y0, vx, vy) in enumerate(P):
        al = 1.0 if i == 0 else ka
        if al <= 0.01: continue
        x, y = refl(x0 + vx * S, LO, HI) + dx, refl(y0 + vy * S, TOP, BOT)
        if i == 0 and stage == 0: dot(d, x, y, R + 8, RED, outline=WHITE)
        else: dot(d, x, y, R, A(GRAIN, al))
    for i in range(len(P)):                                 # loe sang o thanh cam khi vua dap
        for tau, y, h in hits(tm, i, t - 0.15, t):
            k = 1 - (t - tau) / 0.15
            d.arc([HI + R + 6 + dx - 24, y - 24, HI + R + 6 + dx + 24, y + 24], 300, 60, fill=A(ORANGE, k), width=6)
    if stage == 0: counter(d, "1", "1 Hz", "—", MUTED)
    elif stage == 1: counter(d, "200", "1 Hz", "250")
    else: counter(d, "200", "3 Hz", "750" if t >= tm["tA"] + tm["dr"] else "…")
    graph(d, tm, t)

# ---------------- canh 3: Ket qua (so tu mo hinh) ----------------
XC = (230, 520, 820)
def s_kq(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 260, 1040, 900), fill=WHITE, outline=LIGHT, w=4)
    for x, s in zip(XC, ("Số hạt", "Lắc (Hz)", "Cú đập/giây")): text(d, (x, 330), s, FS, INK)
    d.line([(90, 380), (990, 380)], fill=LIGHT, width=4)
    yr = lambda j: 470 + j * 150
    k3 = appear(t, 0.9, 0.5); k2 = appear(t, M[1], 0.6)
    if k3 > 0:
        for j in (1, 2): d.rounded_rectangle([140, yr(j) - 48, 960, yr(j) + 48], radius=24, fill=A((255, 237, 213), k3 * (1 - k2)))
    if k2 > 0:
        for j in (0, 1): d.rounded_rectangle([140, yr(j) - 48, 960, yr(j) + 48], radius=24, fill=A((220, 252, 231), k2))
    for j, (n, f, c) in enumerate(ROWS):
        a = appear(t, 0.1 + 0.25 * j, 0.35)
        text(d, (XC[0], yr(j)), str(n), 64, BLUE, alpha=a); text(d, (XC[1], yr(j)), str(f), 64, BLUE, alpha=a)
        text(d, (XC[2], yr(j)), str(c), 64, ORANGE, alpha=a)
    if k3 > 0:                                                # ngoac x3 ben phai: 250 -> 750 (lac 1 -> 3 Hz)
        c = A(ORANGE, k3); y1, y2 = yr(1), yr(2)
        d.line([(968, y1), (992, y1), (992, y2), (968, y2)], fill=c, width=6)
        text(d, (1026, (y1 + y2) / 2), "×3", 60, DORANGE, alpha=k3)
    if k2 > 0:                                                # ngoac x2 ben trai: 125 -> 250 (100 -> 200 hat)
        c = A(GREEN, k2); y0_, y1 = yr(0), yr(1)
        d.line([(132, y0_), (108, y0_), (108, y1), (132, y1)], fill=c, width=6)
        text(d, (74, (y0_ + y1) / 2), "×2", 60, DGREEN, alpha=k2)
    # hinh minh hoa duoi bang: hai hop nho, so hat x2 (ve cham, khong chu)
    kb = appear(t, M[1] + 0.3, 0.5)
    if kb > 0:
        rr = _rnd.Random(8)
        for j, (cx, n) in enumerate(((330, 18), (750, 36))):
            d.rounded_rectangle([cx - 150, 1000, cx + 150, 1260], radius=14, fill=A((250, 252, 255), kb), outline=A(NAVY, kb), width=5)
            d.line([(cx + 150, 1010), (cx + 150, 1250)], fill=A(ORANGE, kb), width=12)
            for _ in range(n): dot(d, cx - 130 + rr.random() * 260, 1020 + rr.random() * 220, 8, A(GRAIN, kb))
        arrow(d, (500, 1130), (580, 1130), A(DGREEN, kb), w=7, head=24)
        text(d, (330, 1320), "100 hạt", FS, INK, alpha=kb); text(d, (750, 1320), "200 hạt", FS, INK, alpha=kb)

# ---------------- canh 4: vi sao luc deu ----------------
_rv = _rnd.Random(21)
T1 = [0.35 + 1.05 * k for k in range(-4, 14)]                       # mot hat: quay lai dap thanh moi ~1 s (cu le)
TN = np.array(sorted(_rv.uniform(-4, 12) for _ in range(4800)))   # nhieu hat: ~300 cu/giay (minh hoa)
def force(ts, tau, HP, HW):
    """Tong luc tai cac thoi diem tau: moi cu dap la xung tam giac (cao HP, nua rong HW)."""
    out = np.zeros_like(tau)
    for i, x in enumerate(tau):
        dd = np.abs(ts[(ts > x - HW) & (ts < x + HW)] - x)
        out[i] = np.sum(HP * (1 - dd / HW))
    return out

def panel(d, y0, y1, lbl, ts, t, col, HP, HW):
    card(d, (40, y0, 1040, y1), fill=WHITE, outline=LIGHT, w=4)
    text(d, (80, y0 + 55), lbl, FS, INK, anchor="lm")
    base = y1 - 60
    d.line([(GX0, base), (GX1, base)], fill=NAVY, width=5)
    tau = np.linspace(t - WIN, t, 320); fx = force(np.asarray(ts), tau, HP, HW)
    arrow(d, (GX0, base), (GX0, y0 + 95), NAVY, w=5, head=18); text(d, (GX0 + 30, y0 + 140), "F", FS, INK, anchor="lm")
    pts = [(GX0 + (GX1 - GX0) * (i / 319), base - fx[i]) for i in range(320)]
    d.line(pts, fill=col, width=5)
    return base

def s_why(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    panel(d, 270, 760, "1 hạt", T1, t, ORANGE, 70, 0.03)            # mot cu: xung hep, roi im
    base = panel(d, 820, 1560, "200 hạt", TN, t, ORANGE, 5, 0.1)     # rat nhieu xung chong nhau: trung binh ~150 px, dao dong ~15%
    ka = appear(t, M[1] + 0.2, 0.5)
    if ka > 0:
        ym = base - len(TN) / 16 * 5 * 0.1                    # muc trung binh = (so cu/giay) x (dien tich mot xung)
        d.line([(GX0, ym), (GX1, ym)], fill=A(DGREEN, ka), width=9)
        text(d, (W / 2, ym - 110), "lực trung bình", 64, DGREEN, alpha=ka)

# ---------------- canh 5: Bay: hat nam yen de len thanh? ----------------
RB = _rnd.Random(5)
MOL = [(RB.random(), RB.random(), RB.choice((-1, 1)) * RB.uniform(160, 260), RB.choice((-1, 1)) * RB.uniform(160, 260)) for _ in range(34)]
BY0, BY1 = 470, 1170
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    # trai: nam yen -> chi de day
    x0, x1 = 70, 500
    card(d, (40, 330, 530, 1560), fill=WHITE, outline=DRED, w=6)
    text(d, ((x0 + x1) / 2, 395), "Nằm yên", 62, DRED)
    d.rounded_rectangle([x0, BY0, x1, BY1], radius=16, fill=(250, 252, 255), outline=NAVY, width=6)
    rp = _rnd.Random(2)
    for j in range(90):
        r_, c_ = divmod(j, 22)
        dot(d, x0 + 22 + c_ * 18.5 + rp.uniform(-2, 2), BY1 - 16 - r_ * 17, 8, GRAIN)
    kl = appear(t, 0.5, 0.4)
    if kl > 0:
        for x in (150, 285, 420): arrow(d, (x, BY1 + 20), (x, BY1 + 120), A(NAVY, kl), w=9, head=28)
    # phai: chuyen dong -> dap moi thanh
    x0, x1 = 580, 1010
    card(d, (550, 330, 1040, 1560), fill=WHITE, outline=DGREEN, w=6)
    text(d, ((x0 + x1) / 2, 395), "Chuyển động", 62, DGREEN)
    d.rounded_rectangle([x0, BY0, x1, BY1], radius=16, fill=(250, 252, 255), outline=NAVY, width=6)
    Lx, Ly = x1 - x0 - 40, BY1 - BY0 - 40
    for (ux, uy, vx, vy) in MOL:
        x = x0 + 20 + refl(ux * Lx + vx * t, 0, Lx); y = BY0 + 20 + refl(uy * Ly + vy * t, 0, Ly)
        dot(d, x, y, 9, GRAIN)
        if x - x0 < 30: d.line([(x0, y - 22), (x0, y + 22)], fill=ORANGE, width=12)
        if x1 - x < 30: d.line([(x1, y - 22), (x1, y + 22)], fill=ORANGE, width=12)
        if y - BY0 < 30: d.line([(x - 22, BY0), (x + 22, BY0)], fill=ORANGE, width=12)
        if BY1 - y < 30: d.line([(x - 22, BY1), (x + 22, BY1)], fill=ORANGE, width=12)
    kr = appear(t, M[1], 0.4)
    if kr > 0:
        c = A(DGREEN, kr); xm, ym = (x0 + x1) / 2, (BY0 + BY1) / 2
        for xx in (xm - 110, xm + 110): arrow(d, (xx, BY1 + 20), (xx, BY1 + 120), c, w=9, head=28)
        for yy in (ym - 160, ym + 160):                       # mui ten ra hai thanh dung (gon trong the)
            arrow(d, (x0 + 60, yy), (x0 + 8, yy), c, w=9, head=26)
            arrow(d, (x1 - 60, yy), (x1 - 8, yy), c, w=9, head=26)
        for xx in (xm - 110, xm + 110): arrow(d, (xx, BY0 + 60), (xx, BY0 + 8), c, w=9, head=26)

# ---------------- canh 6: chot (phu de) + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    rr = _rnd.Random(4)
    for (bx0, bx1, by, lab) in ((240, 540, 380, "L"), (240, 840, 700, "2L")):
        d.rounded_rectangle([bx0, by, bx1, by + 160], radius=14, fill=A((250, 252, 255), k1), outline=A(NAVY, k1), width=5)
        d.line([(bx1, by + 10), (bx1, by + 150)], fill=A(ORANGE, k1), width=14)
        for _ in range(30 if lab == "L" else 30): dot(d, bx0 + 18 + rr.random() * (bx1 - bx0 - 36), by + 18 + rr.random() * 124, 8, A(GRAIN, k1))
        yy = by + 190
        d.line([(bx0, yy), (bx1, yy)], fill=A(NAVY, k1), width=4)
        for xx in (bx0, bx1): d.line([(xx, yy - 16), (xx, yy + 16)], fill=A(NAVY, k1), width=4)
        text(d, ((bx0 + bx1) / 2, yy + 45), lab, 62, NAVY, alpha=k1)
    text(d, (W / 2, 1100), "Vẫn 200 hạt, lắc 1 Hz;", 64, INK, alpha=k1)
    text(d, (W / 2, 1190), "hộp 2L: cú đập/giây?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1320, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, w, tr, e = (sc[k] for k in ("hook", "do", "kq", "why", "trap", "end"))
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + do["M"][1], "tap"), (do["t0"] + do["M"][2], "tap"),
            (kq["t0"] + 0.9, "ding"), (w["t0"] + w["M"][1] + 0.2, "tap"),
            (tr["t0"] + 0.5, "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l12-apsuatdongnang-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Áp suất - động năng phân tử khí · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Lắc hộp gạo, áp tai nghe", draw=s_hook, tail=0.3, caps=[
   ("Hộp 200 hạt gạo, đậy kín.", 3.0),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành (chiếu chậm)", draw=s_do, tail=0.3, caps=[
   ("Một hạt: đập rồi bật ra.", 3.4),
   ("200 hạt, lắc 1 Hz.", 3.2),
   ("Lắc 3 Hz: dày gấp ba.", 3.4)]),
 dict(key="kq", title="Kết quả theo mô hình", draw=s_kq, tail=0.3, caps=[
   ("Đáp án: gấp ba.", 2.8),
   ("Gấp đôi số hạt: gấp đôi cú đập.", 4.0)]),
 dict(key="why", title="Vì sao thành bị đẩy đều?", draw=s_why, tail=0.3, caps=[
   ("Một hạt: từng cú lẻ.", 3.0),
   ("Nhiều hạt: lực gần như đều.", 3.4)]),
 dict(key="trap", title="Bẫy: hạt nằm yên đè thành?", draw=s_trap, tail=0.3, caps=[
   ("Nằm yên: chỉ đè xuống đáy.", 3.4),
   ("Va chạm: đẩy đều mọi thành.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Áp suất = vô số va chạm cộng lại.", 6.6)]),
])
