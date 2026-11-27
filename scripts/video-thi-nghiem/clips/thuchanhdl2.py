# Clip: tn-l10-thuchanhdl-02 - Hai xe day nhau bang lo xo: tong dong luong sau ~ 0 (lo 9, 18/11/2026; dung lai
# 27/11/2026 theo cong moi L10b: chu >= 55 px khi ve, nhip >= 2,5 s, K10 khong nut A-D, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-thuchanhdl-02.json (_kiem_so() doi chieu):
#   tham_so: s = 0,0500 m ; so_lieu_mau (lan, m1, m2, t1', t2', p1', p2', p', dp'):
#   1 0,205 0,198 0,205 0,195 -0,0500 +0,0507 +0,0007 0,0010 ; 2 0,405 0,198 0,404 0,200 -0,0502 +0,0495 -0,0007 0,0007 ;
#   3 0,205 0,398 0,205 0,402 -0,0500 +0,0494 -0,0006 0,0007.
# Du doan (K10, lan 2: xe 1 0,405 kg, xe 2 0,198 kg): cat day, tong dong luong hai xe sau do?
#   Khung: A. Khoang 0,10 (cong do lon) ; B. Gan bang 0 (DUNG) ; C. Am, xe nang "thang" ; D. Duong, xe nhe chay nhanh hon.
# KHONG tra loi san cau trong bai: Cau 2 (t' ti le m) -> clip khong chia t1'/t2' ; Cau 3 (chieu duong sang TRAI) ->
#   clip giu chieu duong sang phai. Ket qua chi hien tong p' + dp' (hop bai de HS tu tinh p1', p2').
# Bay = hien_tuong_hay_sai[0] (cong do lon, quen dau) o LAN 1 (cap so khac Du doan): 0,0500 + 0,0507 -> -0,0500 + 0,0507.
#   Chua noi duoc: hai xe dang chay roi moi day nhau (tong truoc khac 0) chua thu.
# Cau chot (ca tu suy, ghi trong ghi_chu kho): m1 = 0,300 kg, t1' = 0,200 s -> v1 = 0,250 m/s, p1' = -0,0750 ;
#   hoi p2' (khong cho m2: buoc "tong truoc = 0" chua chieu bang so) -> +0,0750 kg.m/s. Khong hien tren man.
from engine import *

ROWS = [(1, 0.205, 0.198, 0.205, 0.195, -0.0500, 0.0507, 0.0007, 0.0010),
        (2, 0.405, 0.198, 0.404, 0.200, -0.0502, 0.0495, -0.0007, 0.0007),
        (3, 0.205, 0.398, 0.205, 0.402, -0.0500, 0.0494, -0.0006, 0.0007)]
SW = 0.0500
CHOT = (0, 0.300, None, 0.200)                 # m1, t1' ; dap so p2' = +0,0750
def vn(x, n=3): return f"{x:.{n}f}".replace(".", ",")
def sg(x, n=4): return ("−" if x < 0 else "+") + vn(abs(x), n)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-thuchanhdl-02.json")))
    for r, h in zip(ROWS, k["so_lieu_mau"]["hang"]): assert all(abs(a - b) < 1e-9 for a, b in zip(r, h)), ("lech kho", r)
    for n, m1, m2, t1, t2, p1, p2, p, dp in ROWS:
        assert abs(round(-m1 * round(SW / t1, 3), 4) - p1) < 1e-9 and abs(round(p1 + p2, 4) - p) < 1e-9 and abs(p) <= dp
    g = k["so_lieu_mau"]["ghi_chu"]
    for s in ("m1 = 0,300 kg", "t1' = 0,200 s", "p2' ≈ +0,0750"): assert s in g, ("ghi_chu thieu", s)
    assert abs(round(CHOT[1] * SW / CHOT[3], 4) - 0.0750) < 1e-9
_kiem_so()

C1, C1D = ORANGE, (154, 52, 18)                 # xe 1
C2, C2D = BLUE, (30, 64, 175)                   # xe 2
RAIL = (148, 163, 184); RAIL_D = (100, 116, 139); LCD = (134, 239, 172)
DRED = (185, 28, 28); NOTE = (60, 64, 84); DGREEN = (21, 110, 55); EMPTY = (148, 140, 128)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o (cao 70 px), tat lan luot tu phai sang trai."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- bang dem khi + hai xe (goc o giua bang) ----------------
XC, PXM = 540, 600                    # mp4 x = 65 + 0,88 x
G1, G2 = -0.25, 0.25
CLM, X10, X20, XSTOP = 0.12, -0.10, 0.10, 0.62
YB = 790
def sx(x): return XC + x * PXM

def track(d, yb, k=1.0):
    d.rectangle([60, yb + 2, 1020, yb + 26], fill=A(RAIL, k), outline=A(NAVY, k))
    for i in range(1, 40): dot(d, 60 + i * 24, yb + 14, 3, A(RAIL_D, k))
    for x in (-XSTOP - CLM / 2 - 0.02, XSTOP + CLM / 2 + 0.02):
        d.rectangle([sx(x) - 8, yb - 40, sx(x) + 8, yb + 2], fill=A(NAVY, k))
    d.rectangle([90, yb + 26, 120, yb + 60], fill=A(RAIL_D, k)); d.rectangle([960, yb + 26, 990, yb + 60], fill=A(RAIL_D, k))

def gate_back(d, yb, g):
    x = sx(g)
    for dx in (-30, 30): d.line([(x + dx, yb + 26), (x + dx, yb - 175)], fill=NAVY, width=7)
def gate_front(d, yb, g):
    x = sx(g); d.line([(x - 34, yb - 175), (x + 34, yb - 175)], fill=NAVY, width=9)
    dot(d, x - 30, yb - 110, 8, RED); dot(d, x + 30, yb - 110, 8, RED)

def cart(d, yb, x, col, cold, label, n_gt=0, k=1.0):
    c = lambda cc: A(cc, k); w = CLM * PXM / 2; X = sx(x); hw = SW * PXM / 2
    d.rectangle([X - hw, yb - 132, X + hw, yb - 76], fill=c(NAVY))
    for j in range(n_gt):
        dx = (-1) ** j * 0; lv = j
        d.rectangle([X - hw - 26, yb - 104 - 26 * lv, X - hw - 4, yb - 80 - 26 * lv], fill=c(GRAY), outline=c(NAVY), width=2)
        d.rectangle([X + hw + 4, yb - 104 - 26 * lv, X + hw + 26, yb - 80 - 26 * lv], fill=c(GRAY), outline=c(NAVY), width=2)
    d.rounded_rectangle([X - w, yb - 76, X + w, yb - 2], radius=12, fill=c(col), outline=c(cold), width=3)
    text(d, (X, yb - 39), label, 56, WHITE, alpha=k)

def spring(d, yb, xl, xr, k=1.0):
    n = 6; y = yb - 39; pts = [(xl, y)]
    for i in range(1, 2 * n):
        pts.append((lerp(xl, xr, i / (2 * n)), y + (13 if i % 2 else -13)))
    pts.append((xr, y)); d.line(pts, fill=A(NAVY, k), width=4)

def lcd(d, x, y, lab, val, col, hi=False):
    text(d, (x, y - 80), lab, 56, col)
    card(d, (x - 135, y - 44, x + 135, y + 44), fill=NAVY, r=14)
    text(d, (x, y), val, 56, YELLOW if hi else LCD)

def pos(x0, v, u):
    return max(-XSTOP, min(XSTOP, x0 + v * max(0.0, u)))

def gate_done(x0, v, u, g, tp):
    """Dong ho dung (hien t') khi tam can quang da ra khoi tia."""
    if u <= 0: return False
    u_in = (g - x0 + (SW / 2 if v < 0 else -SW / 2)) / v
    return u - u_in >= tp - 1e-9

def axis(d, y, k=1.0):
    arrow(d, (XC - 230, y), (XC - 70, y), A(NAVY, k), w=6, head=20)
    text(d, (XC - 40, y), "chiều dương", 56, NAVY, anchor="lm", alpha=k)

def rig(d, row, u, yc=930, show_m=True, freeze=None, q2=False, ax=True):
    """Hinh trong the y 265-yc. u = giay tu luc cat day (None: chua cat). freeze = (x1, x2) dat xe co dinh."""
    n, m1, m2, t1, t2 = row[:5]
    card(d, (40, 265, 1040, yc), fill=WHITE, outline=LIGHT, w=3)
    text(d, (70, 320), f"xe 1: {vn(m1)} kg" if show_m else "xe 1", 56, C1D, anchor="lm")
    text(d, (1010, 320), (f"xe 2: {vn(m2)} kg" if m2 else "xe 2") if show_m else "xe 2", 56, C2D, anchor="rm")
    v1, v2 = -SW / t1, (SW / t2 if t2 else 0.25)
    uu = -1 if u is None else u
    if freeze: x1, x2 = freeze; d1, d2 = True, False
    else:
        x1, x2 = pos(X10, v1, uu), pos(X20, v2, uu)
        d1 = gate_done(X10, v1, uu, G1, t1); d2 = gate_done(X20, v2, uu, G2, t2)
    lcd(d, sx(G1) - 10, 495, "cổng 1", f"{vn(t1)} s" if d1 else "– – –", C1D)
    lcd(d, sx(G2) + 10, 495, "cổng 2", "?" if q2 else (f"{vn(t2)} s" if d2 else "– – –"), C2D, hi=d2)
    track(d, YB); gate_back(d, YB, G1); gate_back(d, YB, G2)
    w = CLM * PXM / 2
    if u is None and not freeze:
        spring(d, YB, sx(X10) + w, sx(X20) - w)
        d.line([(sx(X10), YB - 70), (sx(X20), YB - 70)], fill=INK, width=4)
    else: spring(d, YB, sx(x1) + w, sx(x1) + w + 40)
    cart(d, YB, x1, C1, C1D, "1", int(round((m1 - 0.205) / 0.1)) if m1 < 0.5 else 0)
    cart(d, YB, x2, C2, C2D, "2", int(round((m2 - 0.198) / 0.1)) if m2 else 0)
    gate_front(d, YB, G1); gate_front(d, YB, G2)
    if ax: axis(d, YB + 100)
    return x1, x2, d1, d2

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, ROWS[1], None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 965 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Cắt dây. Tổng động lượng", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "hai xe sau đó?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 410, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (3 lan) ----------------
R0, RUN, CUT = 0.5, 2.3, 0.4

def do_state(t):
    if t < R0: return 0, None, 1.0
    i = min(2, int((t - R0) // RUN)); w = t - R0 - i * RUN
    k = appear(w, 0.0, 0.2) if i > 0 else 1.0
    if i < 2: k *= 1.0 - appear(w, RUN - 0.25, 0.2)
    return i, (w - CUT if w >= CUT else None), k

XS = (110, 300, 500, 705, 910)
def table(d, cells, hl=None, y=965):
    card(d, (40, y, 1040, y + 610), fill=WHITE, outline=LIGHT, w=3)
    for x, lab, unit, col in ((XS[0], "Lần", "", INK), (XS[1], "m₁", "kg", C1D), (XS[2], "m₂", "kg", C2D),
                              (XS[3], "t₁′", "s", C1D), (XS[4], "t₂′", "s", C2D)):
        text(d, (x, y + 60), lab, 60, col)
        if unit: text(d, (x, y + 125), unit, 56, col, bold=False)
    d.line([(70, y + 170), (1010, y + 170)], fill=LIGHT, width=3)
    for j, (cm, c1, c2) in enumerate(cells):
        n, m1, m2, t1, t2 = ROWS[j][:5]; yy = y + 235 + j * 95
        if j == hl: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=20, fill=(255, 247, 237))
        if cm:
            text(d, (XS[0], yy), str(n), 60, INK)
            text(d, (XS[1], yy), vn(m1), 60, C1D); text(d, (XS[2], yy), vn(m2), 60, C2D)
        if c1: text(d, (XS[3], yy), vn(t1), 60, C1D)
        if c2: text(d, (XS[4], yy), vn(t2), 60, C2D)
    text(d, (W / 2, y + 555), "tấm cản quang rộng 5,00 cm", 56, NOTE)

def cells_at(t):
    i, u, k = do_state(t); out = []
    for j in range(3):
        if t < R0 or j > i: out.append((False, False, False)); continue
        if j < i: out.append((True, True, True)); continue
        n, m1, m2, t1, t2 = ROWS[j][:5]; uu = -1 if u is None else u
        out.append((True, gate_done(X10, -SW / t1, uu, G1, t1), gate_done(X20, SW / t2, uu, G2, t2)))
    return out

def s_do(img, d, t, sc):
    i, u, k = do_state(t)
    x1, x2, *_ = rig(d, ROWS[i], u, show_m=False, ax=False)
    if u is not None and u < 0.4: text(d, (XC, YB - 215), "cắt", 56, INK, alpha=1 - u / 0.4)
    ka = (appear(u, 0.3, 0.3) if u is not None else 0) * k
    if ka > 0:
        X1, X2 = max(sx(x1), 250), min(sx(x2), 830); y = YB + 95
        arrow(d, (X1, y), (X1 - 130, y), A(C1, ka), w=8, head=22); text(d, (X1 - 175, y), "p₁′", 56, C1D, alpha=ka)
        arrow(d, (X2, y), (X2 + 130, y), A(C2, ka), w=8, head=22); text(d, (X2 + 175, y), "p₂′", 56, C2D, alpha=ka)
    table(d, cells_at(t), hl=i if t >= R0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: o bang = dong ho da dung ; ca hai dong ho dung truoc het luot ; lan 3 xong truoc het canh."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, u, k = do_state(t); n, m1, m2, t1, t2 = ROWS[i][:5]; uu = -1 if u is None else u
        c = cells_at(t)[i] if t >= R0 else (False, False, False)
        if t >= R0 and (c[1], c[2]) != (gate_done(X10, -SW / t1, uu, G1, t1), gate_done(X20, SW / t2, uu, G2, t2)):
            bad.append(("bang/dong ho", round(t, 2)))
        t += 0.05
    for j in range(3):
        n, m1, m2, t1, t2 = ROWS[j][:5]
        for x0, v, g, tp in ((X10, -SW / t1, G1, t1), (X20, SW / t2, G2, t2)):
            if not gate_done(x0, v, RUN - CUT - 0.3, g, tp): bad.append(("chua qua cong", j + 1))
    if R0 + 3 * RUN > sc["T"] - 0.2: bad.append("lan cuoi sat cuoi canh")
    return bad

# ---------------- canh 3: Ket qua ----------------
def s_kq(img, d, t, sc):
    M = sc["M"]; r = ROWS[1]
    card(d, (40, 265, 1040, 660), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 325), "Lần 2", 56, INK, anchor="lm")
    yb = 530; track(d, yb)
    x1, x2 = -0.42, 0.42
    spring(d, yb, sx(x1) + CLM * PXM / 2, sx(x1) + CLM * PXM / 2 + 40)
    cart(d, yb, x1, C1, C1D, "1", 2); cart(d, yb, x2, C2, C2D, "2")
    g = ease((t - 0.4) / 0.6); y = yb + 85
    if g > 0:
        L1, L2 = 3000 * abs(r[5]) * g, 3000 * abs(r[6]) * g             # px / (kg.m/s): hai mui ten gan bang
        arrow(d, (sx(x1) + 60, y), (sx(x1) + 60 - L1, y), C1, w=9, head=24)
        arrow(d, (sx(x2) - 60, y), (sx(x2) - 60 + L2, y), C2, w=9, head=24)
        text(d, (sx(x1) + 60 - L1 - 60, y), "p₁′", 56, C1D); text(d, (sx(x2) - 60 + L2 + 60, y), "p₂′", 56, C2D)
    ka = appear(t, M[1] - 0.1, 0.45)
    if ka > 0:
        y0 = 690
        card(d, (40, y0, 1040, y0 + 520), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
        xs = (170, 540, 870)
        text(d, (xs[0], y0 + 60), "Lần", 60, INK, alpha=ka)
        text(d, (xs[1], y0 + 60), "tổng p′", 60, DGREEN, alpha=ka); text(d, (xs[2], y0 + 60), "sai số Δp′", 60, INK, alpha=ka)
        text(d, (W / 2, y0 + 130), "đơn vị kg·m/s", 56, INK, alpha=ka)
        d.line([(70, y0 + 175), (1010, y0 + 175)], fill=A(LIGHT, ka), width=3)
        for j, rr in enumerate(ROWS):
            yy = y0 + 245 + j * 95
            text(d, (xs[0], yy), str(rr[0]), 60, INK, alpha=ka)
            text(d, (xs[1], yy), sg(rr[7]), 60, DGREEN, alpha=ka); text(d, (xs[2], yy), vn(rr[8], 4), 60, INK, alpha=ka)
    kb = appear(t, M[2] - 0.1, 0.45)
    if kb > 0:
        card(d, (40, 1240, 1040, 1560), fill=A((236, 253, 243), kb), outline=A(GREEN, kb), w=5)
        text(d, (W / 2, 1340), "|tổng p′| ≤ sai số", 64, INK, alpha=kb)
        text(d, (W / 2, 1460), "tổng sau = 0 trong sai số", 60, DGREEN, alpha=kb)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; r = ROWS[0]
    a1 = appear(t, 0.3, 0.45)
    card(d, (40, 265, 1040, 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 335, "BẪY", RED, a1)
    q, q0 = "p′ = 0,0500 + 0,0507", "Lần 1:  "
    ks = clamp((t - M[1]) / 0.4); lw = tw(d, q, F(62)); l0 = tw(d, q0, F(62)); yy = 470
    xl = W / 2 - (lw + l0) / 2
    text(d, (xl, yy), q0, 62, INK, anchor="lm", alpha=a1)
    text(d, (xl + l0, yy), q, 62, mix(INK, DRED, ks), anchor="lm", alpha=a1)
    text(d, (xl + l0 + lw / 2, yy + 75), "p₁′ + p₂′ (kg·m/s)", 56, NOTE, alpha=a1)
    if ks > 0: d.line([(xl + l0 - 6, yy + 2), (xl + l0 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
    kk = appear(t, M[1] + 0.1, 0.45)
    if kk > 0:
        card(d, (40, 640, 1040, 1240), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
        yb = 810; track(d, yb, kk)
        x1, x2 = -0.40, 0.40
        cart(d, yb, x1, C1, C1D, "1", 0, kk); cart(d, yb, x2, C2, C2D, "2", 0, kk)
        y = yb + 80
        arrow(d, (sx(x1) + 70, y), (sx(x1) - 90, y), A(C1, kk), w=8, head=22)
        arrow(d, (sx(x2) - 70, y), (sx(x2) + 90, y), A(C2, kk), w=8, head=22)
        text(d, (sx(x1) - 10, yb + 150), sg(r[5]), 60, C1D, alpha=kk)
        text(d, (W / 2, yb + 150), "kg·m/s", 56, NOTE, bold=False, alpha=kk)
        text(d, (sx(x2) + 10, yb + 150), sg(r[6]), 60, C2D, alpha=kk)
        text(d, (XC, yb - 110), "chiều dương", 56, NAVY, alpha=kk)
        arrow(d, (XC - 80, yb - 40), (XC + 80, yb - 40), A(NAVY, kk), w=6, head=20)
        text(d, (W / 2, 1090), "p₁′ + p₂′ = −0,0500 + 0,0507", 62, DGREEN, alpha=kk)
        text(d, (W / 2, 1180), "= +0,0007 kg·m/s ✓", 62, DGREEN, alpha=kk)
    k5 = appear(t, M[2] + 0.1, 0.45)
    if k5 > 0:
        y0 = 1270 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 290), fill=A(WHITE, k5), outline=A(NAVY, k5), w=6)
        pill(d, W / 2, y0 + 70, "CHƯA NÓI ĐƯỢC", NAVY, k5)
        text(d, (W / 2, y0 + 200), "hai xe đang chạy mới đẩy nhau", 58, INK, alpha=k5)

# ---------------- canh 5: THU NGHI (cau chot o khung web: p2' = +0,0750) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    rig(d, (0, CHOT[1], None, CHOT[3], None), None, freeze=(-0.50, 0.40), q2=True)
    y0 = 965
    card(d, (40, y0, 1040, 1665), fill=WHITE, outline=ORANGE, w=6)
    pill(d, W / 2, y0 + 70, "THỬ NGHĨ", ORANGE)
    k1 = appear(t, 2.6, 0.45)
    text(d, (W / 2, y0 + 195), "Tấm cản quang rộng 5,00 cm.", 60, INK, alpha=k1)
    k2 = appear(t, 5.0, 0.45)
    text(d, (W / 2, y0 + 300), "Động lượng p₂′ của xe 2?", 62, ORANGE, alpha=k2)
    seg_bar(d, y0 + 370, t, 5.2, sc["T"] - 0.2, ORANGE, k2)
    kh = appear(t, 7.5, 0.45)
    if kh > 0:
        card(d, (90, y0 + 475, 990, y0 + 680), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, y0 + 530), "Gợi ý", 56, INK, alpha=kh)
        text(d, (W / 2, y0 + 620), "dấu theo chiều dương", 58, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, b, e = sc["hook"], sc["do"], sc["kq"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for i in range(3): out.append((do["t0"] + R0 + i * RUN + CUT, "tap"))            # cat day
    return out + [(kq["t0"] + 0.4, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 5.0, "open")]

CLIP = dict(id="tn-l10-thuchanhdl-02", header="VẬT LÍ 10 · THỰC HÀNH", footer="Thực hành động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Lò xo nén giữa hai xe", draw=s_hook, tail=0.3, caps=[
   ("Dây buộc giữ lò xo nén.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cắt dây: hai xe bật ra.", 3.4),
   ("Đổi gia trọng, đo ba lần.", 3.6)]),
 dict(key="kq", title="Kết quả", draw=s_kq, tail=0.3, caps=[
   ("Đáp án: gần bằng 0.", 3.0),
   ("Cộng có dấu, so với sai số.", 3.6),
   ("Bảo toàn trong sai số.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.0),
   ("Sai: xe 1 đi ngược chiều dương.", 4.0),
   ("Thí nghiệm này còn thiếu gì?", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Một lần đo mới.", 4.6),
   ("Dừng lại, tự tính.", 4.8)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("đồng bộ:", _kiem_dong_bo() or "không lệch")
