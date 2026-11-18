# Clip: tn-l10-thuchanhdl-02 - Hai xe day nhau bang lo xo: tong dong luong sau ~ 0 (lo 9, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-thuchanhdl-02.json:
#   tham_so: s = 0,0500 m (tam can quang) ; dong ho 0,001 s ; can 0,001 kg ; chieu duong sang phai.
#   so_lieu_mau (lan, m1, m2, t1', t2', p1', p2', p', dp'): 1 0,205 0,198 0,205 0,195 -0,0500 +0,0507 +0,0007 0,0010 ;
#   2 0,405 0,198 0,404 0,200 -0,0502 +0,0495 -0,0007 0,0007 ; 3 0,205 0,398 0,205 0,402 -0,0500 +0,0494 -0,0006 0,0007.
#   (v lam tron 0,001 m/s roi nhan m, theo gia_thiet kho.) Kiem: _kiem_so().
# Hai vat tuong tac: xe 1 CAM (di sang trai, qua cong 1), xe 2 XANH (sang phai, cong 2); nhan "p1' xe 1" / "p2' xe 2"
#   ngay tren hinh, cung mau xe. Day cung chinh la hien tuong tn-l10-newton3-05 nhung clip chi lam thuchanhdl-02.
# Du doan (K10: chi cau hoi + hinh; lan 2: xe 1 0,405 kg, xe 2 0,198 kg): cat day, tong dong luong hai xe sau do?
#   A. Khoang 0,10 kg.m/s (cong hai do lon) ; B. Gan bang 0 (DUNG) ; C. Lech ve phia xe nhe, vi xe nhe chay nhanh hon.
# KHONG tra loi san cau trong bai: Cau 2 (m1 = 0,300, m2 = 0,150, t2' = 0,150 -> t1') -> clip khong noi "t' ti le m",
#   khong chia t1'/t2'; Cau 3 (chieu duong sang TRAI) -> clip khong doi chieu duong.
# Bay = hien_tuong_hay_sai[0] (cong do lon, quen dau).
# Cau chot (ca tu suy, ghi trong ghi_chu kho): m1 = 0,300 kg (trong 0,19-0,6), t1' = 0,200 s -> v1 = 0,250 m/s,
#   p1' = -0,0750 kg.m/s ; p2' ~ +0,0750 kg.m/s (p0 = 0,075 trong 0,02-0,1). Chua hien tren man.
# Chuyen dong thoi gian that: v = s/t' dung -> dong ho cong dem toi dung t' luc tam can quang ra khoi cong.
from engine import *

ROWS = [(1, 0.205, 0.198, 0.205, 0.195, -0.0500, 0.0507, 0.0007, 0.0010),
        (2, 0.405, 0.198, 0.404, 0.200, -0.0502, 0.0495, -0.0007, 0.0007),
        (3, 0.205, 0.398, 0.205, 0.402, -0.0500, 0.0494, -0.0006, 0.0007)]
SW = 0.0500
def vn(x, n=3): return f"{x:.{n}f}".replace(".", ",")
def sg(x, n=4): return ("−" if x < 0 else "+") + vn(abs(x), n)

def _kiem_so():
    bad = []
    for n, m1, m2, t1, t2, p1, p2, p, dp in ROWS:
        v1 = round(SW / t1, 3); v2 = round(SW / t2, 3)
        if abs(round(-m1 * v1, 4) - p1) > 1e-9: bad.append(("p1", n))
        if abs(round(m2 * v2, 4) - p2) > 1e-9: bad.append(("p2", n))
        if abs(round(p1 + p2, 4) - p) > 1e-9: bad.append(("p'", n))
        e = abs(p1) * (0.001 / m1 + 0.001 / t1) + abs(p2) * (0.001 / m2 + 0.001 / t2)
        if abs(round(e, 4) - dp) > 1e-9: bad.append(("dp'", n, round(e, 5)))
        if abs(p) > dp + 1e-12: bad.append(("|p'| > dp'", n))
    if abs(round(0.300 * SW / 0.200, 4) - 0.0750) > 1e-9: bad.append("chot")
    return bad

C1, C1D = ORANGE, (154, 52, 18)                 # xe 1
C2, C2D = BLUE, (30, 64, 175)                   # xe 2
RAIL = (148, 163, 184); RAIL_D = (100, 116, 139); LCD = (134, 239, 172)
DRED = (185, 28, 28); NOTE = (60, 64, 84); DGREEN = (21, 110, 55)

TOK2 = re.compile(r"(_\{[^}]*\})")
def rs(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chu co chi so duoi; chi so >= 40 px (brief lo 9)."""
    sub = max(40, int(size * 0.72)); segs = []
    for p in [p for p in TOK2.split(s) if p]:
        segs.append((p[2:-1], sub, size * 0.30) if p.startswith("_{") else (p, size, 0))
    tot = sum(tw(d, x, F(z)) for x, z, _ in segs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for s_, z, dy in segs:
        dtext(d, (x, cy + dy), s_, F(z), color, alpha, "lm"); x += tw(d, s_, F(z))
    return tot

# ---------------- bang dem khi + hai xe ----------------
XC, PXM = 540, 600                    # tam bang (px), px / m
G1, G2 = -0.30, 0.30                  # vi tri hai cong (m)
CLM, X10, X20, XSTOP = 0.12, -0.08, 0.08, 0.62   # xe dung o chot, mep xe trong [204, 876] px
def sx(x): return XC + x * PXM

def track(d, yb):
    d.rectangle([60, yb + 2, 1020, yb + 26], fill=RAIL, outline=NAVY)
    for i in range(1, 40): dot(d, 60 + i * 24, yb + 14, 3, RAIL_D)
    for x in (-XSTOP - CLM / 2 - 0.02, XSTOP + CLM / 2 + 0.02):
        d.rectangle([sx(x) - 8, yb - 34, sx(x) + 8, yb + 2], fill=NAVY)
    d.rectangle([90, yb + 26, 120, yb + 70], fill=RAIL_D); d.rectangle([960, yb + 26, 990, yb + 70], fill=RAIL_D)

def gate_back(d, yb, g):
    x = sx(g); d.line([(x - 28, yb + 26), (x - 28, yb - 140)], fill=NAVY, width=7); d.line([(x + 28, yb + 26), (x + 28, yb - 140)], fill=NAVY, width=7)
def gate_front(d, yb, g):
    x = sx(g); d.line([(x - 32, yb - 140), (x + 32, yb - 140)], fill=NAVY, width=9)
    dot(d, x - 28, yb - 80, 7, RED); dot(d, x + 28, yb - 80, 7, RED)

def cart(d, yb, x, col, cold, label, k=1.0):
    c = lambda cc: A(cc, k); w = CLM * PXM / 2; X = sx(x)
    hw = SW * PXM / 2                                                             # tam can quang 5,00 cm = 30 px
    d.rectangle([X - hw, yb - 100, X + hw, yb - 44], fill=c(NAVY))
    d.rounded_rectangle([X - w, yb - 46, X + w, yb - 2], radius=10, fill=c(col), outline=c(cold), width=3)
    text(d, (X, yb - 24), label, 40, WHITE, alpha=k)

def spring(d, yb, xl, xr, k=1.0):
    """Lo xo gan ben phai xe 1, tu xl toi xr (px)."""
    n = 7; y = yb - 24; pts = [(xl, y)]
    for i in range(1, 2 * n):
        pts.append((lerp(xl, xr, i / (2 * n)), y + (11 if i % 2 else -11)))
    pts.append((xr, y)); d.line(pts, fill=A(NAVY, k), width=3)

def lcd(d, x, y, lab, val, col):
    text(d, (x, y - 70), lab, 40, col)
    card(d, (x - 110, y - 40, x + 110, y + 40), fill=NAVY, r=14)
    text(d, (x, y), val, 44, LCD)

def pos(x0, v, u):
    """Vi tri tam xe sau khi cat day u giay (v co dau), dung o chot cuoi bang."""
    x = x0 + v * max(0.0, u)
    return max(-XSTOP, min(XSTOP, x))

def gate_read(x0, v, u, g, tp):
    """So dong ho cong g: dem thoi gian tam can quang che tia; ra khoi tia thi dung o t'."""
    if u <= 0: return 0.0, False
    u_in = (g - x0 + (SW / 2 if v < 0 else -SW / 2)) / v      # mep truoc tam can quang cham tia
    if u < u_in: return 0.0, False
    e = u - u_in
    return (tp, True) if e >= tp else (e, False)

def momentum_arrows(d, yb, x1, x2, k, short=False):
    if k <= 0: return
    L = 140
    X1 = max(sx(x1), 250); X2 = min(sx(x2), 830)              # neo mui ten + nhan trong khung (nhan rong ~180 px)
    arrow(d, (X1, yb + 80), (X1 - L, yb + 80), A(C1, k), w=7, head=20)
    arrow(d, (X2, yb + 80), (X2 + L, yb + 80), A(C2, k), w=7, head=20)
    rs(d, X1 - L / 2, yb + 130, "p_{1}′ xe 1", 42, C1D, alpha=k)
    rs(d, X2 + L / 2, yb + 130, "p_{2}′ xe 2", 42, C2D, alpha=k)

def positive_axis(d, y):
    arrow(d, (XC - 90, y), (XC + 90, y), NAVY, w=5, head=18)
    text(d, (XC + 110, y), "chiều dương", 40, NAVY, anchor="lm")

def rig(d, row, u, show_lcd=True, mk=1.0, tied=True):
    """Hinh trong the y 265-945. row = hang so_lieu_mau ; u = giay tu luc cat day (None: chua cat)."""
    n, m1, m2, t1, t2 = row[:5]
    card(d, (40, 265, 1040, 945), fill=WHITE, outline=LIGHT, w=3)
    yb = 680
    text(d, (70, 305), f"xe 1: {vn(m1)} kg", 42, C1D, anchor="lm", alpha=mk)
    text(d, (1010, 305), f"xe 2: {vn(m2)} kg", 42, C2D, anchor="rm", alpha=mk)
    v1, v2 = -SW / t1, SW / t2
    uu = -1 if u is None else u
    r1, d1 = gate_read(X10, v1, uu, G1, t1); r2, d2 = gate_read(X20, v2, uu, G2, t2)
    if show_lcd:
        lcd(d, sx(G1), 440, "cổng 1", vn(r1), C1D); lcd(d, sx(G2), 440, "cổng 2", vn(r2), C2D)
    track(d, yb); gate_back(d, yb, G1); gate_back(d, yb, G2)
    x1, x2 = pos(X10, v1, uu), pos(X20, v2, uu)
    w = CLM * PXM / 2
    if tied:
        spring(d, yb, sx(X10) + w, sx(X20) - w)
        d.line([(sx(X10), yb - 50), (sx(X20), yb - 50)], fill=INK, width=3)
    else:
        spring(d, yb, sx(x1) + w, sx(x1) + w + 42)
    cart(d, yb, x1, C1, C1D, "1"); cart(d, yb, x2, C2, C2D, "2")
    gate_front(d, yb, G1); gate_front(d, yb, G2)
    return yb, x1, x2, (r1, d1), (r2, d2)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    yb, *_ = rig(d, ROWS[1], None)
    positive_axis(d, yb + 200)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 975 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 165), "Hai xe đứng yên. Cắt dây.", 46, INK, alpha=a)
    ctext(d, y0 + 300, "Tổng động lượng hai xe sau đó?", 52, INK, maxw=860, alpha=a)
    text(d, (W / 2, y0 + 440), "Chọn đáp án ở khung câu hỏi", 38, NOTE, bold=False, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 505, 940, y0 + 519], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 505, 140 + 800 * (1 - p), y0 + 519], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (3 lan) ----------------
R0, RUN, CUT = 0.6, 2.9, 0.5

def do_state(t):
    """-> (lan i, u tu luc cat (None chua cat), do mo xe)."""
    if t < R0: return 0, None, 1.0
    i = min(2, int((t - R0) // RUN)); w = t - R0 - i * RUN
    k = appear(w, 0.0, 0.2) if i > 0 else 1.0
    if i < 2: k *= 1.0 - appear(w, RUN - 0.25, 0.2)
    return i, (w - CUT if w >= CUT else None), k

XS = (110, 300, 500, 720, 920)
def table(d, cells, hl=None, y=975):
    """cells[j] = (co m, co t1', co t2')."""
    card(d, (40, y, 1040, y + 470), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y + 58), "Lần", 42, INK)
    rs(d, XS[1], y + 52, "m_{1} (kg)", 44, C1D); rs(d, XS[2], y + 52, "m_{2} (kg)", 44, C2D)
    rs(d, XS[3], y + 52, "t_{1}′ (s)", 44, C1D); rs(d, XS[4], y + 52, "t_{2}′ (s)", 44, C2D)
    d.line([(70, y + 110), (1010, y + 110)], fill=LIGHT, width=3)
    for j, (cm, c1, c2) in enumerate(cells):
        n, m1, m2, t1, t2 = ROWS[j][:5]; yy = y + 175 + j * 95
        if j == hl: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=20, fill=(255, 247, 237))
        text(d, (XS[0], yy), str(n), 46, MUTED if not cm else INK)
        if cm: text(d, (XS[1], yy), vn(m1), 46, C1D); text(d, (XS[2], yy), vn(m2), 46, C2D)
        if c1: text(d, (XS[3], yy), vn(t1), 46, C1D)
        if c2: text(d, (XS[4], yy), vn(t2), 46, C2D)

def cells_at(t):
    i, u, k = do_state(t); out = []
    for j in range(3):
        if t < R0 or j > i: out.append((False, False, False)); continue
        if j < i: out.append((True, True, True)); continue
        n, m1, m2, t1, t2 = ROWS[j][:5]
        uu = -1 if u is None else u
        _, d1 = gate_read(X10, -SW / t1, uu, G1, t1); _, d2 = gate_read(X20, SW / t2, uu, G2, t2)
        out.append((True, d1, d2))
    return out

def s_do(img, d, t, sc):
    i, u, k = do_state(t)
    IMG_REF[0] = img
    yb, x1, x2, g1, g2 = rig(d, ROWS[i], u, mk=k, tied=u is None)
    if u is not None and u < 0.25:                             # vet cat day
        text(d, (XC, yb - 120), "cắt", 44, INK, alpha=1 - u / 0.25)   # SFNS khong co glyph keo
    momentum_arrows(d, yb, x1, x2, (appear(u, 0.5, 0.3) if u is not None else 0) * k)
    positive_axis(d, yb + 210)
    table(d, cells_at(t), hl=i if t >= R0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: o bang = so dong ho da dung ; so dong ho luc dung = t' cua hang ; xe khong qua chot cuoi."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, u, k = do_state(t); n, m1, m2, t1, t2 = ROWS[i][:5]; uu = -1 if u is None else u
        r1, d1 = gate_read(X10, -SW / t1, uu, G1, t1); r2, d2 = gate_read(X20, SW / t2, uu, G2, t2)
        c = cells_at(t)[i] if t >= R0 else (False, False, False)
        if t >= R0 and (c[1] != d1 or c[2] != d2): bad.append(("bang/dong ho", round(t, 2)))
        if d1 and r1 != t1 or d2 and r2 != t2: bad.append(("so dong ho", round(t, 2)))
        t += 0.05
    for j in range(3):                                         # ca hai dong ho dung truoc khi het luot
        n, m1, m2, t1, t2 = ROWS[j][:5]
        for x0, v, g, tp in ((X10, -SW / t1, G1, t1), (X20, SW / t2, G2, t2)):
            _, done = gate_read(x0, v, RUN - CUT - 0.3, g, tp)
            if not done: bad.append(("chua qua cong", j + 1))
    if R0 + 3 * RUN > sc["T"] + 0.01: bad.append("lan cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def ptable(d, y, rows_k, alpha=1.0):
    card(d, (40, y, 1040, y + 450), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    # Hop trong bai giao HS tu tinh p1', p2' co dau roi cong -> chi hien tong p' va sai so dp'.
    xs = (170, 540, 870)
    text(d, (xs[0], y + 55), "Lần", 42, INK, alpha=alpha)
    text(d, (xs[1], y + 55), "p′ (tổng)", 46, DGREEN, alpha=alpha); text(d, (xs[2], y + 55), "Δp′", 46, INK, alpha=alpha)
    text(d, (W / 2, y + 112), "đơn vị: kg·m/s", 40, NOTE, bold=False, alpha=alpha)
    d.line([(70, y + 150), (1010, y + 150)], fill=A(LIGHT, alpha), width=3)
    for j, r in enumerate(ROWS):
        k = rows_k[j] * alpha
        if k <= 0: continue
        yy = y + 210 + j * 85
        text(d, (xs[0], yy), str(r[0]), 44, INK, alpha=k)
        text(d, (xs[1], yy), sg(r[7]), 44, DGREEN, alpha=k); text(d, (xs[2], yy), vn(r[8], 4), 44, INK, alpha=k)

def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.1, 0.4)
    lab = "ĐÁP ÁN · Gần bằng 0"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 338), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 304), lab, 42, WHITE, alpha=ka)
    # hinh nho: sau khi cat day, hai mui ten nguoc chieu
    card(d, (40, 365, 1040, 690), fill=WHITE, outline=LIGHT, w=3)
    yb = 500; track(d, yb)
    x1, x2 = -0.45, 0.45
    spring(d, yb, sx(x1) + CLM * PXM / 2, sx(x1) + CLM * PXM / 2 + 42)
    cart(d, yb, x1, C1, C1D, "1"); cart(d, yb, x2, C2, C2D, "2")
    momentum_arrows(d, yb - 10, x1, x2, 1.0)
    text(d, (XC, 400), "chiều dương", 40, NAVY)
    arrow(d, (XC - 70, 450), (XC + 70, 450), NAVY, w=5, head=18)
    ptable(d, 720, [appear(t, M[0] + 0.2 + 0.5 * j, 0.4) for j in range(3)])
    kr = appear(t, M[1] - 0.2, 0.45)
    if kr > 0:
        y0 = 1200 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 320), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pw = tw(d, "RÚT RA", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(GREEN, kr), r=32)
        text(d, (W / 2, y0 + 56), "RÚT RA", 40, WHITE, alpha=kr)
        text(d, (W / 2, y0 + 160), "|p′| ≤ Δp′ (sai số) ở cả ba lần", 50, INK, alpha=kr)
        text(d, (W / 2, y0 + 250), "tổng sau ≈ tổng trước = 0", 46, DGREEN, alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    kf = appear(t, 2.6, 0.4)          # hinh chieu chuyen dong hien cung the xanh, sau khi cau sai bi gach
    if kf > 0:
        card(d, (40, 1130, 1040, 1500), fill=A(WHITE, kf), outline=A(LIGHT, kf), w=3)
        yb = 1290; track(d, yb)
        x1, x2 = -0.30, 0.30
        cart(d, yb, x1, C1, C1D, "1", k=kf); cart(d, yb, x2, C2, C2D, "2", k=kf)
        arrow(d, (sx(x1), yb + 70), (sx(x1) - 140, yb + 70), A(C1, kf), w=7, head=20)
        arrow(d, (sx(x2), yb + 70), (sx(x2) + 140, yb + 70), A(C2, kf), w=7, head=20)
        text(d, (sx(x1) - 70, 1420), "sang trái", 40, C1D, alpha=kf); text(d, (sx(x2) + 70, 1420), "sang phải", 40, C2D, alpha=kf)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3); y = 300
    if a1 > 0:
        card(d, (40, y, 1040, y + 790), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        text(d, (W / 2, y + 160), "Lần 2", 42, NOTE, bold=False, alpha=a1)
        q = "“p′ = 0,0502 + 0,0495”"
        ks = clamp((t - 1.4) / 0.4); f = F(52); lw = tw(d, q, f); yy = y + 260
        text(d, (W / 2, yy), q, 52, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 370), "quên dấu  ✗", 46, DRED, alpha=appear(t, 1.8, 0.4) * a1)
        kg = appear(t, 2.6, 0.4) * a1
        card(d, (90, y + 450, 990, y + 740), fill=A((236, 253, 243), kg), r=24)
        text(d, (W / 2, y + 530), "Xe 1 ngược chiều dương:", 44, DGREEN, alpha=kg)
        text(d, (W / 2, y + 640), "p′ = −0,0502 + 0,0495 = −0,0007  ✓", 44, DGREEN, alpha=kg)
    if k3 > 0:
        card(d, (40, y, 1040, y + 790), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 90), "Chưa nói được", 50, NAVY, alpha=k3)
        for j, s in enumerate(("• Lò xo đẩy mỗi xe", "  mạnh bao nhiêu?", "• Va chạm mềm thì", "  còn bảo toàn không?")):
            kk = k3 * appear(t, M[1] + 0.3 + 0.6 * (j // 2), 0.4)
            text(d, (110, y + 240 + 100 * j + 70 * (j // 2)), s, 48, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot -> THU NGHI ca m1 = 0,300 kg, t1' = 0,200 s (so moi) ; goi y la du kien, tre 2,6 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, "Đứng yên rồi đẩy nhau: p′ ≈ 0 trong sai số", 50, GREEN, maxw=840, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 2.6, 0.5)
    card(d, (40, 600, 1040, 1080 + 330 * kh), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)   # co theo noi dung
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ka = appear(t, M[0] + 0.4, 0.5)
    ctext(d, 790, "Xe 1 nặng 0,300 kg qua cổng 1\nhết 0,200 s (tấm chắn 5,00 cm).", 46, INK, maxw=920, alpha=ka)
    text(d, (W / 2, 925), "Chiều dương sang phải, bỏ qua sai số.", 46, INK, alpha=ka)
    rs(d, W / 2, 1005, "p_{1}′, p_{2}′ = ?", 46, INK, alpha=ka)
    if kh > 0:
        card(d, (110, 1090, 970, 1370), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1155), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1270), "5,00 cm = 0,0500 m", 46, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for i in range(3):
        out.append((do["t0"] + R0 + i * RUN + CUT, "tap"))                     # cat day
    return out + [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-thuchanhdl-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Thực hành động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Lò xo nén giữa hai xe", draw=s_hook, tail=0.6, caps=[
   ("Dây buộc giữ lò xo nén.", 3.2),
   ("Dừng video, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cắt dây: hai xe bật ra.", 4.4),
   ("Đo ba lần.", 5.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Xe 1 đi ngược chiều dương.", 4.2),
   ("So độ lớn p′ với sai số.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Cộng thẳng hai số.", 4.4),
   ("Hai câu còn bỏ ngỏ.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự tính.", 6.8)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("số:", _kiem_so() or "khớp kho"); print("đồng bộ:", _kiem_dong_bo() or "không lệch")
