# Clip: tn-l10-nemngang-02 - Ban bi ngang o ba do cao: do tam xa, suy ra van toc nem (31/10/2026; dung lai 27/11/2026
# theo cong moi viec 4: --do-chu 0 LOI, chu ve >= 55 px, khong nut A-D (K10), thanh dem lien, Bay hai nhip, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-nemngang-02.json (_kiem_so() doi chieu):
#   tham_so: v0 = 1,5 m/s (giu nguyen khi doi h), g = 9,8 m/s2, h trong mien 0,2..1,5 m (buoc 0,05).
#   so_lieu_mau: h = 0,45 / 0,80 / 0,80 / 1,25 m -> t = 0,303 / 0,404 / 0,404 / 0,505 s,
#                L do = 0,451 / 0,611 / 0,606 / 0,757 m, v0 = L/t = 1,49 / 1,51 / 1,50 / 1,50 m/s.
# Du doan: v0 = L/t o ba do cao the nao? -> gan nhu bang nhau (kho: ket_qua_ky_vong).
# Bay = hien_tuong_hay_sai "L ti le voi h": h x 2,8 (0,45 -> 1,25) ma L chi x 1,7 (0,451 -> 0,757).
#   Nhip 1 cot "tuong" net dut do + dau X; nhip 2 cot do that. Khong lap cap so cua Du doan (Du doan khong co so).
# Chua noi duoc: gia_thiet "non nam ngang" -> non chech len thi sao.
# Chot (THU NGHI = cau_chot khung web): h = 0,60 m (trong mien tham_so, theo mo hinh), v0 = 1,50 m/s, g = 9,8:
#   t = sqrt(2h/g) = 0,350 s -> L = 0,52 m. Hai buoc (t roi L), so 0,60 / 0,52 chua tung hien; khac nemngang1
#   (h = 0,50 m, v0 = 2 m/s) va khac Cau 1 bai (L gap doi -> 4h).
from engine import *

G = 9.8
V0 = 1.50
ROWS = [(0.45, 0.303, 0.451, 1.49), (0.80, 0.404, 0.611, 1.51),
        (0.80, 0.404, 0.606, 1.50), (1.25, 0.505, 0.757, 1.50)]                 # so_lieu_mau
H_CHOT = 0.60

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-nemngang-02.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    assert hang == ROWS, hang
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["v0"]["gia_tri"] == V0 and ts["g"]["gia_tri"] == G
    assert ts["h"]["min"] <= H_CHOT <= ts["h"]["max"]
    for h, tt, L, v in ROWS: assert abs(math.sqrt(2 * h / G) - tt) < 6e-4 and abs(L / tt - v) < 6e-3
_kiem_so()

STEEL = (110, 120, 140); GHOST = (175, 182, 198); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
PAPER = (60, 64, 80); DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8); DPURPLE = (91, 33, 182)

def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")

def bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem lien (tut tung nac 10%), cao 70 px."""
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

# ---------------- khung dung ti le (dung chung) ----------------
PXM = 480.0                    # px / m, ca hai phuong
YF = 960                       # mat ban
X0 = 330                       # dau nong sung (x = 0 cua tam xa)
POLE = 240                     # cot gia do
def P(x, y): return (X0 + x * PXM, YF - y * PXM)

def setup(d, h, paper=True, marks=True, ruler=True):
    d.rectangle([60, YF, 1020, YF + 30], fill=WOOD, outline=WOOD_D, width=3)                 # mat ban
    if paper: d.rectangle([P(0.30, 0)[0], YF - 8, P(0.85, 0)[0], YF], fill=PAPER)            # giay than
    if ruler:                                                                                # thuoc cuon
        d.rectangle([X0, YF + 30, P(0.85, 0)[0], YF + 54], fill=(253, 224, 71), outline=WOOD_D, width=2)
        for k in range(0, 9):
            xx = P(k / 10, 0)[0]; L = 24 if k % 2 == 0 else 14
            d.line([(xx, YF + 30), (xx, YF + 30 + L)], fill=NAVY, width=3)
        for k in (0, 4, 8):
            text(d, (P(k / 10, 0)[0], YF + 90), "0" if k == 0 else vn(k / 10, 1), 58, INK)
        text(d, (P(0.85, 0)[0] + 30, YF + 90), "m", 58, INK, anchor="lm")
    top = YF - 1.36 * PXM
    d.rectangle([POLE - 9, top, POLE + 9, YF], fill=(120, 128, 145))
    d.rectangle([POLE - 60, YF - 16, POLE + 60, YF], fill=(90, 98, 115))
    if marks:
        for hh in (0.45, 0.80, 1.25):
            yy = P(0, hh)[1]
            d.line([(POLE - 30, yy), (POLE - 9, yy)], fill=PURPLE, width=5)
            text(d, (POLE - 40, yy), vn(hh), 56, PURPLE, anchor="rm")
    yy = P(0, h)[1]                                                                          # sung, nong ngang
    d.rounded_rectangle([POLE - 20, yy - 22, X0 - 36, yy + 22], radius=8, fill=NAVY)
    d.rectangle([X0 - 38, yy - 10, X0, yy + 10], fill=(60, 70, 100))

def ball(d, x, y, r=17, col=STEEL): dot(d, x, y, r, col, outline=NAVY)

def path_pts(h, L, tt, n=40):
    v = L / tt
    return [P(v * tt * i / n, h - G / 2 * (tt * i / n) ** 2) for i in range(n + 1)]

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 210, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    k = clamp((t - 0.6) / 2.8)                                                 # sung di qua ba do cao roi ve 0,80 m
    hs = (0.80, 0.45, 1.25, 0.80); i = min(2, int(k * 3)); f = ease(k * 3 - i)
    h = lerp(hs[i], hs[i + 1], f) if k < 1 else 0.80
    setup(d, h, ruler=False)
    y = P(0, h)[1]
    arrow(d, (X0 + 12, y), (X0 + 170, y), BLUE, w=8, head=24)
    text(d, (X0 + 200, y), "v₀: vận tốc ném", 58, BLUE, anchor="lm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1120 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 98), fill=A(PURPLE, a), r=36)
    text(d, (W / 2, y0 + 60), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "v₀ = L/t ở ba độ cao", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "sẽ thế nào?", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 335), "L: tầm xa · t: thời gian rơi", 58, DPURPLE, alpha=a)
    bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh (4 lan ban, chieu cham 4 lan) ----------------
SLOW = 4.0
MOVE, HOLD, RUN0 = 0.5, 0.7, 0.5
def schedule():
    out = []; s = RUN0
    for i, (h, tt, L, v) in enumerate(ROWS):
        mv = MOVE if (i == 0 or ROWS[i - 1][0] != h) else 0.25
        out.append((s, mv)); s += mv + tt * SLOW + HOLD
    return out
SCHED = schedule()

def shot_state(t):
    """-> (lan j, do cao sung, tau that (None neu chua ban), so hang da xong)."""
    j = 0
    for i, (s, mv) in enumerate(SCHED):
        if t >= s: j = i
    s, mv = SCHED[j]; h, tt, L, v = ROWS[j]
    hp = ROWS[j - 1][0] if j > 0 else 0.80
    if t < s: return 0, 0.80, None, 0
    if t < s + mv: return j, lerp(hp, h, ease((t - s) / mv)), None, j
    tau = min((t - s - mv) / SLOW, tt)
    return j, h, tau, j + (1 if (t - s - mv) / SLOW >= tt - 1e-9 else 0)

def table(d, y, n, cur=-1, v0col=0.0):
    card(d, (40, y, 1040, y + 500), fill=WHITE, outline=NAVY, w=4)
    xs = (170, 405, 640, 890) if v0col else (220, 540, 860)
    text(d, (xs[0], y + 56), "h (m)", 62, PURPLE); text(d, (xs[1], y + 56), "t (s)", 62, TEAL)
    text(d, (xs[2], y + 56), "L (m)", 62, DORANGE)
    if v0col: text(d, (xs[3], y + 56), "v₀ = L/t", 62, BLUE)
    d.line([(70, y + 104), (1010, y + 104)], fill=NAVY, width=3)
    for i, (h, tt, L, v) in enumerate(ROWS):
        yy = y + 156 + i * 92
        if i == cur and n <= i: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=16, fill=(255, 237, 213))
        if i < n:
            text(d, (xs[0], yy), vn(h), 62, INK); text(d, (xs[1], yy), vn(tt, 3), 62, INK)
            text(d, (xs[2], yy), vn(L, 3), 62, INK)
            if v0col > 0:
                d.rounded_rectangle([xs[3] - 100, yy - 40, xs[3] + 100, yy + 40], radius=14, fill=A((219, 234, 254), v0col))
                text(d, (xs[3], yy), vn(v), 62, BLUE, alpha=v0col)

def s_do(img, d, t, sc):
    j, hc, tau, done = shot_state(t)
    card(d, (40, 210, 1040, 1080), fill=WHITE, outline=LIGHT, w=3)
    setup(d, hc)
    text(d, (1010, 280), "chiếu chậm 4 lần", 58, INK, anchor="rm")
    lp = P(0.78, 0)                                                          # nhan giay than (ben phai, ngoai quy dao)
    d.line([(lp[0], YF - 10), (lp[0] + 40, YF - 55)], fill=INK, width=3)
    text(d, (lp[0] + 50, YF - 75), "giấy than", 58, INK, anchor="lm")
    for i in range(done):                                                    # vet cac lan truoc
        if i == j: continue
        h, tt, L, v = ROWS[i]
        d.line(path_pts(h, L, tt), fill=GHOST, width=4)
        lx = P(L, 0)[0]; d.line([(lx, YF - 22), (lx, YF + 2)], fill=ORANGE, width=7)
    h, tt, L, v = ROWS[j]
    if tau is None: ball(d, X0 + 4, P(0, hc)[1])
    else:
        vx = L / tt
        for kk in range(1, int(tau / 0.05) + 1):                             # vet bong moi 0,05 s
            tk = kk * 0.05; gx, gy = P(vx * tk, h - G / 2 * tk * tk); dot(d, gx, gy, 9, GHOST)
        bx, by = P(vx * tau, h - G / 2 * tau * tau); by -= 17 * min(1.0, tau / tt)
        if tau >= tt - 1e-9:
            d.line(path_pts(h, L, tt), fill=GHOST, width=4)
            lx = P(L, 0)[0]; d.line([(lx, YF - 22), (lx, YF + 2)], fill=ORANGE, width=7)
        ball(d, bx, by)
    text(d, (W / 2, 1118), "t tính từ h: t = √(2h/g)", 58, TEAL)
    table(d, 1158, done, cur=j)

def _kiem_dong_bo():
    bad = []; t = 0.0
    while t < 12:
        j, hc, tau, done = shot_state(t)
        if tau is not None and done > j and abs(tau - ROWS[j][1]) > 1e-9: bad.append((round(t, 2), "hang hien truoc khi cham"))
        t += 0.05
    if shot_state(11.4)[3] != 4: bad.append("chua du 4 hang truoc cuoi canh")
    lands = [s + mv + r[1] * SLOW for (s, mv), r in zip(SCHED, ROWS)]
    if min(b - a for a, b in zip(lands, lands[1:])) < 2.5: bad.append(("hang moi cach < 2,5 s", lands))
    return bad

# ---------------- canh 3: Dap an (cot v0 = L/t) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    table(d, 230, 4, v0col=appear(t, M[0] + 2.0, 0.5))
    k2 = appear(t, M[1] + 0.2, 0.5)
    if k2 > 0:
        card(d, (60, 850, 1020, 1150), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=6)
        text(d, (W / 2, 935), "v₀ ≈ 1,50 m/s", 66, DGREEN, alpha=k2)
        text(d, (W / 2, 1050), "cả bốn lần, lệch ≤ 0,02 m/s", 58, DGREEN, alpha=k2)
    # hinh nho: ba nhat bam cung mot mui ten v0 (cung sung)
    for i, hh in enumerate((0.45, 0.80, 1.25)):
        x = 200 + i * 300; y = 1480 - hh * 200
        d.rounded_rectangle([x - 80, y - 20, x + 30, y + 20], radius=8, fill=NAVY)
        arrow(d, (x + 34, y), (x + 150, y), BLUE, w=8, head=22)
        text(d, (x - 25, 1540), vn(hh) + " m", 56, PURPLE)
        d.line([(x - 25, y + 22), (x - 25, 1500)], fill=A(PURPLE, 0.6), width=4)

# ---------------- canh 4: Rut ra (do thi L theo t) + chua noi duoc ----------------
GX0, GY0 = 270, 880
GPX_T, GPX_L = 1150.0, 690.0
def GP(tt, L): return (GX0 + tt * GPX_T, GY0 - L * GPX_L)

def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 210, 1040, 1010), fill=WHITE, outline=LIGHT, w=3)
    text(d, (GX0 + 24, 270), "L (m)", 60, DORANGE, anchor="lm")
    d.line([GP(0, 0), GP(0.66, 0)], fill=INK, width=5); d.line([GP(0, 0), GP(0, 0.86)], fill=INK, width=5)
    for k in (2, 4, 6):
        x, y = GP(k / 10, 0); d.line([(x, y - 12), (x, y + 12)], fill=INK, width=4)
        text(d, (x, y + 55), vn(k / 10, 1), 56, INK)
    text(d, (GP(0, 0)[0] - 30, GP(0, 0)[1] + 50), "0", 56, INK)
    text(d, (1010, GY0 - 50), "t (s)", 60, TEAL, anchor="rm")
    for k in (4, 8):
        x, y = GP(0, k / 10); d.line([(x - 12, y), (x + 12, y)], fill=INK, width=4)
        text(d, (x - 26, y), vn(k / 10, 1), 56, INK, anchor="rm")
    kl = appear(t, M[0] + 0.8, 1.0)
    if kl > 0:
        te = 0.57 * kl; d.line([GP(0, 0), GP(te, V0 * te)], fill=BLUE, width=6)
    for i, (h, tt, L, v) in enumerate(ROWS):
        k = appear(t, 0.3 + 0.2 * i, 0.35)
        if k > 0:
            x, y = GP(tt, L); dot(d, x, y, 17, A(ORANGE, k), outline=NAVY)
    kt = appear(t, M[0] + 1.8, 0.5)
    text(d, (820, 640), "L = v₀·t", 62, BLUE, alpha=kt)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 <= 0: return
    y0 = 1040 + (1 - k2) * 30
    card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
    text(d, (W / 2, y0 + 70), "Chưa nói được", 62, NAVY, alpha=k2)
    text(d, (W / 2, y0 + 165), "Nòng chếch lên thì sao?", 62, DRED, alpha=k2)
    ang = math.radians(8 + 14 * ease((t - M[1]) / 2.5))                     # nong xoay dan len
    cx, cy = 360, y0 + 430; L1 = 230
    ex, ey = cx + L1 * math.cos(ang), cy - L1 * math.sin(ang)
    d.line([(cx, cy), (ex, ey)], fill=NAVY, width=34)
    arrow(d, (ex + 20 * math.cos(ang), ey - 20 * math.sin(ang)), (ex + 190 * math.cos(ang), ey - 190 * math.sin(ang)), A(BLUE, k2), w=8, head=24)
    d.line([(cx - 40, cy + 60), (960, cy + 60)], fill=A(WOOD_D, k2), width=6)
    text(d, (ex + 190 * math.cos(ang) + 20, ey - 190 * math.sin(ang) + 64), "v₀", 62, BLUE, anchor="lm", alpha=k2)

# ---------------- canh 5: Bay (L ti le voi h?) ----------------
BASE, SCL = 900, 380.0
def colbar(d, x, v, col, lab, dashed=False, a=1.0):
    top = BASE - v * SCL
    if dashed:
        yy = top
        while yy < BASE:
            d.line([(x - 60, yy), (x - 60, min(yy + 22, BASE))], fill=A(DRED, a), width=6)
            d.line([(x + 60, yy), (x + 60, min(yy + 22, BASE))], fill=A(DRED, a), width=6); yy += 38
        xx = x - 60
        while xx < x + 60: d.line([(xx, top), (min(xx + 22, x + 60), top)], fill=A(DRED, a), width=6); xx += 38
    else: d.rectangle([x - 60, top, x + 60, BASE], fill=A(col, a))
    text(d, (x, top - 45), lab, 58, DRED if dashed else col, alpha=a)

def s_bay(img, d, t, sc):
    M = sc["M"]
    for x0, x1, lab, col in ((40, 525, "độ cao h", PURPLE), (555, 1040, "tầm xa L", DORANGE)):
        card(d, (x0, 210, x1, 1010), fill=WHITE, outline=LIGHT, w=3)
        d.line([(x0 + 30, BASE), (x1 - 30, BASE)], fill=INK, width=4)
        text(d, ((x0 + x1) / 2, BASE + 55), lab, 58, col)
    colbar(d, 180, 0.45, PURPLE, "0,45"); colbar(d, 390, 1.25, PURPLE, "1,25")
    colbar(d, 690, 0.451, DORANGE, "0,451")
    ka = 1.0
    card(d, (60, 1050, 1020, 1200), fill=A((245, 243, 255), ka), outline=A(PURPLE, ka), r=24, w=5)
    text(d, (W / 2, 1125), "h gấp 2,8 lần", 62, DPURPLE, alpha=ka)
    kb = 1 - appear(t, M[1] - 0.1, 0.4)             # nhip 1: cot "tuong" net dut
    if kb > 0:
        colbar(d, 900, 1.25 * 0.451 / 0.45, DRED, "tưởng", dashed=True, a=kb)
        card(d, (60, 1230, 1020, 1380), fill=A((254, 242, 242), kb), outline=A(DRED, kb), r=24, w=5)
        text(d, (W / 2, 1305), "✗ L cũng gấp 2,8 lần", 62, DRED, alpha=kb)
    kc = appear(t, M[1] - 0.1, 0.5)                                          # nhip 2: cot do that
    if kc > 0:
        g = ease((t - M[1] + 0.1) / 0.8)
        colbar(d, 900, lerp(0.451, 0.757, g), DORANGE, "0,757", a=kc)
        card(d, (60, 1230, 1020, 1380), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=24, w=5)
        text(d, (W / 2, 1305), "✓ L tăng chậm hơn h", 62, DGREEN, alpha=kc)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1590), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 238, W / 2 + pw / 2, 314), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 276), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    yt = 1130; yg = yt - H_CHOT * 900                                       # do cao 0,60 m (900 px/m, hinh minh hoa)
    d.rectangle([60, yt, 1020, yt + 26], fill=A(WOOD, k1), outline=A(WOOD_D, k1), width=3)
    d.rectangle([200, yg - 380 + 360, 218, yt], fill=A((120, 128, 145), k1))
    d.rounded_rectangle([180, yg - 24, 330, yg + 24], radius=8, fill=A(NAVY, k1))
    arrow(d, (340, yg), (520, yg), A(BLUE, k1), w=8, head=24)
    text(d, (540, yg), "v₀ = 1,50 m/s", 62, BLUE, anchor="lm", alpha=k1)
    xm = 140
    d.line([(xm, yg), (xm, yt)], fill=A(PURPLE, k1), width=5)
    for yy in (yg, yt): d.line([(xm - 14, yy), (xm + 14, yy)], fill=A(PURPLE, k1), width=5)
    text(d, (xm + 100, (yg + yt) / 2 + 40), "0,60 m", 62, PURPLE, anchor="lm", alpha=k1)
    x = 330
    while x < 800: d.line([(x, yt - 30), (min(x + 24, 800), yt - 30)], fill=A(DORANGE, k1), width=6); x += 40
    text(d, (910, yt - 40), "L = ?", 66, DORANGE, alpha=k1)
    text(d, (W / 2, 390), "g = 9,8 m/s²", 60, INK, alpha=k1)
    text(d, (W / 2, 1270), "Tầm xa L bằng bao nhiêu?", 64, DORANGE, alpha=k1)
    bar(d, 1380, t, 0.8, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for (s, mv), row in zip(SCHED, ROWS): cs.append((do["t0"] + s + mv + row[1] * SLOW, "tap"))   # bi cham giay
    cs += [(da["t0"] + da["M"][0] + 2.0, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1], "tap"),
           (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-nemngang-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động ném · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ba độ cao, một súng", draw=s_hook, tail=0.3, caps=[
   ("Súng bắn ngang, ba độ cao.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Lần 1: súng cao 0,45 m.", 3.0),
   ("Cao 0,80 m: bắn hai lần.", 4.6),
   ("Lần 4: súng cao 1,25 m.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Chia L cho t ở từng lần.", 3.2),
   ("Đáp án: gần như bằng nhau.", 3.4)]),
 dict(key="rutra", title="Vì sao?", draw=s_rutra, tail=0.5, caps=[
   ("Các điểm thẳng hàng qua gốc.", 3.4),
   ("Mới thử nòng nằm ngang.", 3.4)]),
 dict(key="bay", title="Bẫy: L tỉ lệ với h?", draw=s_bay, tail=0.4, caps=[
   ("Dễ tưởng: hai cột tăng như nhau.", 3.6),
   ("Đo thật: L chỉ gấp 1,7.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Cùng súng: độ cao chỉ đổi t và L.", 4.4)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
