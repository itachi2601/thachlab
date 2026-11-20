# Clip: tn-l10-baotoandl-02 - Hai xe cung khoi luong, dem lo xo la: va cham gan dan hoi (lo 9, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-baotoandl-02.json:
#   tham_so: m = 0,20 kg moi xe ; v1 0,1-1,0 m/s
#   so_lieu_mau (v1, v1', v2'): 0,3 0 0,3 ; 0,5 0 0,5 ; 0,8 0 0,8 (mo hinh dan hoi li tuong; xe that mat vai %)
# Cung dan voi baotoandl1 (ray dem khi, hai cong quang) nhung trong tam: XE 1 DUNG HAN, XE 2 NHAN GAN TRON.
# Du doan (K10), v1 = 0,50 m/s, xe 2 dung yen: ngay sau va cham hai xe chay the nao?
#   A. Xe 1 dung, xe 2 di 0,50 m/s (DUNG) ; B. Hai xe cung di 0,25 m/s ; C. Xe 1 bat nguoc 0,50 m/s, xe 2 di 0,50 m/s.
# Bay = hien_tuong_hay_sai[0] (nham voi va cham mem: cung di nua toc do; 0,25 m/s them vao ghi_chu kho).
# Khong viet cong thuc v1', v2' (hop "Mo rong" ngay sau hop trong bai).
# Cau chot (ca tu suy, ghi trong ghi_chu kho): xe 2 dang chay 0,20 m/s cung chieu, xe 1 toi 0,60 m/s
#   -> v1' = 0,20 m/s ; v2' = 0,60 m/s (cong thuc mo_hinh kho, m1 = m2). Chua hien tren man.
from engine import *

ROWS = [(0.3, 0.0, 0.3), (0.5, 0.0, 0.5), (0.8, 0.0, 0.8)]   # v1, v1', v2'
MX = 0.20
C1, C1D = ORANGE, (154, 52, 18)                 # xe 1
C2, C2D = BLUE, (30, 64, 175)                   # xe 2
RAIL = (148, 163, 184); RAIL_D = (100, 116, 139); LCD = (134, 239, 172)
NOTE = (60, 64, 84); DGREEN = (21, 110, 55); LEAF = (71, 85, 105)
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def _kiem_so():
    bad = []
    def el(m1, m2, v1, v2): return ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2), ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
    for v1, a, b in ROWS:
        p, q = el(MX, MX, v1, 0.0)
        if abs(p - a) > 1e-9 or abs(q - b) > 1e-9: bad.append(v1)
    if [round(x, 2) for x in el(MX, MX, 0.60, 0.20)] != [0.20, 0.60]: bad.append("chot")
    if round(MX * 0.50 / (2 * MX), 2) != 0.25: bad.append("bay")
    return bad

TOK2 = re.compile(r"(_\{[^}]*\})")
def rs(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chu co chi so duoi; chi so >= 40 px."""
    sub = max(40, int(size * 0.72)); segs = []
    for p in [p for p in TOK2.split(s) if p]:
        segs.append((p[2:-1], sub, size * 0.30) if p.startswith("_{") else (p, size, 0))
    tot = sum(tw(d, x, F(z)) for x, z, _ in segs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for s_, z, dy in segs:
        dtext(d, (x, cy + dy), s_, F(z), color, alpha, "lm"); x += tw(d, s_, F(z))
    return tot

# ---------------- ray dem khi, hai cong quang, hai xe co vong lo xo la ----------------
X0, PXM = 60, 800
G1, G2 = 0.40, 0.86
CL, RING = 0.14, 0.04                 # chieu dai xe ; be day vong lo xo la (m) gan dau xe 1
X1S, X2S, X2STOP = 0.28, 0.66, 1.06   # tam xe 2 dung o chan cuoi ray
XC1 = X2S - CL - RING                 # tam xe 1 luc vong lo xo cham xe 2
TC = 0.08                             # thoi gian tiep xuc (s)
def sx(s): return X0 + s * PXM

def track(d, yb, k=1.0):
    d.rectangle([X0, yb + 2, X0 + 1.2 * PXM, yb + 26], fill=A(RAIL, k), outline=A(NAVY, k))
    for i in range(1, 40): dot(d, X0 + i * 24, yb + 14, 3, A(RAIL_D, k))
    d.rectangle([90, yb + 26, 120, yb + 70], fill=A(RAIL_D, k)); d.rectangle([960, yb + 26, 990, yb + 70], fill=A(RAIL_D, k))
    xs = sx(X2STOP + CL / 2); d.rectangle([xs, yb - 40, xs + 16, yb + 2], fill=A(NAVY, k))      # chan cuoi ray

def gate_back(d, yb, g):
    x = sx(g); d.line([(x - 28, yb + 26), (x - 28, yb - 140)], fill=NAVY, width=7); d.line([(x + 28, yb + 26), (x + 28, yb - 140)], fill=NAVY, width=7)
def gate_front(d, yb, g):
    x = sx(g); d.line([(x - 32, yb - 140), (x + 32, yb - 140)], fill=NAVY, width=9)
    dot(d, x - 28, yb - 80, 7, RED); dot(d, x + 28, yb - 80, 7, RED)

def cart(d, yb, x, col, cold, label, k=1.0, ring=None):
    """x = tam xe (m). ring = be day vong lo xo la (m) o dau phai (None: khong co)."""
    c = lambda cc: A(cc, k); w = CL * PXM / 2; X = sx(x)
    d.rectangle([X - 6, yb - 100, X + 6, yb - 46], fill=c(NAVY))
    d.rounded_rectangle([X - w, yb - 46, X + w, yb - 2], radius=10, fill=c(col), outline=c(cold), width=3)
    text(d, (X, yb - 24), label, 40, WHITE, alpha=k)
    if ring is not None:
        rw = max(4, ring * PXM)
        d.ellipse([X + w - 4, yb - 42, X + w - 4 + rw, yb - 6], outline=c(LEAF), width=5)

def lcd(d, x, y, lab, val, col, hi=False):
    text(d, (x, y - 66), lab, 40, col)
    card(d, (x - 125, y - 40, x + 125, y + 40), fill=NAVY, r=14)
    text(d, (x, y), val, 44, YELLOW if hi else LCD)

def kin(v1, u):
    """u: giay tu luc xe 1 chay. -> (x1, x2, be day vong). Tiep xuc: luc lo xo coi nhu khong doi trong TC."""
    uc = (XC1 - X1S) / v1
    if u < uc: return X1S + v1 * max(0.0, u), X2S, RING
    tau = u - uc
    if tau < TC:
        a = v1 / TC
        x1 = XC1 + v1 * tau - a * tau * tau / 2; x2 = X2S + a * tau * tau / 2
        return x1, x2, RING - (v1 * tau - a * tau * tau)
    x1 = XC1 + v1 * TC / 2
    x2 = min(X2STOP, X2S + v1 * TC / 2 + v1 * (tau - TC))
    return x1, x2, RING

def run_len(v1):
    return 0.15 + (XC1 - X1S) / v1 + TC + (G2 + 0.01 - X2S - v1 * TC / 2) / v1 + 0.6

def rig(d, v1, u, yb=700, k=1.0, hook=False):
    card(d, (40, 265, 1040, 845), fill=WHITE, outline=LIGHT, w=3)
    text(d, (70, 305), f"xe 1: {vn(MX)} kg", 42, C1D, anchor="lm", alpha=k)
    text(d, (1010, 305), f"xe 2: {vn(MX)} kg", 42, C2D, anchor="rm", alpha=k)
    if hook: x1, x2, rg = 0.44, X2S, RING
    else: x1, x2, rg = kin(v1, u)
    d1 = hook or x1 >= G1 + 0.01; d2 = (not hook) and x2 >= G2 + 0.01
    lcd(d, sx(G1), 440, "cổng 1", f"{vn(v1)} m/s" if d1 else "– – –", C1D)
    lcd(d, sx(G2), 440, "cổng 2", "?" if hook else (f"{vn(v1)} m/s" if d2 else "– – –"), C2D, hi=d2)
    track(d, yb); gate_back(d, yb, G1); gate_back(d, yb, G2)
    cart(d, yb, x2, C2, C2D, "2", k)
    cart(d, yb, x1, C1, C1D, "1", k, ring=rg)
    gate_front(d, yb, G1); gate_front(d, yb, G2)
    return x1, x2, d1, d2

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; yb = 700
    rig(d, 0.5, None, yb, hook=True)
    X = sx(0.44)
    arrow(d, (X - 60, yb + 70), (X + 60, yb + 70), C1, w=7, head=20)
    text(d, (sx(X2S), yb + 80), "đứng yên", 40, C2D)
    xr = X + CL * PXM / 2 + 16
    d.line([(xr, yb - 44), (xr - 10, yb - 150)], fill=LEAF, width=3)
    text(d, (xr - 10, yb - 180), "lò xo lá", 40, LEAF)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 875 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 250, "Ngay sau va chạm, mỗi xe chạy thế nào?", 50, INK, maxw=880, alpha=a)
    text(d, (W / 2, y0 + 385), "Chọn đáp án ở khung câu hỏi", 38, NOTE, bold=False, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 440, 940, y0 + 454], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 440, 140 + 800 * (1 - p), y0 + 454], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (3 lan) ----------------
R0, FADE = 0.5, 0.2
STARTS = []
_s = R0
for _r in ROWS: STARTS.append(_s); _s += run_len(_r[0])
DO_END = _s

def do_state(t):
    if t < R0: return 0, None, 1.0
    i = max(j for j in range(3) if t >= STARTS[j]); w = t - STARTS[i]; L = run_len(ROWS[i][0])
    k = appear(w, 0.0, FADE) if i > 0 else 1.0
    if i < 2: k *= 1.0 - appear(w, L - FADE, FADE)
    u = min(w, L) - 0.15
    return i, (u if u >= 0 else None), k

def stopped(v1, u):
    return u is not None and u >= (XC1 - X1S) / v1 + TC

XS = (130, 380, 640, 890)
def table(d, cells, hl=None, y=875):
    card(d, (40, y, 1040, y + 470), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y + 58), "Lần", 42, INK)
    rs(d, XS[1], y + 52, "v_{1} (m/s)", 44, C1D); rs(d, XS[2], y + 52, "v_{1}′ (m/s)", 44, C1D)
    rs(d, XS[3], y + 52, "v_{2}′ (m/s)", 44, C2D)
    d.line([(70, y + 110), (1010, y + 110)], fill=LIGHT, width=3)
    for j, (c0, c1, c2) in enumerate(cells):
        v1, a, b = ROWS[j]; yy = y + 180 + j * 95
        if j == hl: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=20, fill=(255, 247, 237))
        text(d, (XS[0], yy), str(j + 1), 46, INK if c0 else MUTED)
        if c0: text(d, (XS[1], yy), vn(v1), 46, C1D)
        if c1: text(d, (XS[2], yy), "0", 46, C1D)
        if c2: text(d, (XS[3], yy), vn(b), 46, C2D)
    text(d, (1010, y + 440), "số liệu mô hình lí tưởng", 40, NOTE, bold=False, anchor="rm")

def cells_at(t):
    i, u, k = do_state(t); out = []
    for j in range(3):
        if t < R0 or j > i: out.append((False, False, False)); continue
        if j < i: out.append((True, True, True)); continue
        v1 = ROWS[j][0]; x1, x2, _ = kin(v1, -1 if u is None else u)
        out.append((u is not None and x1 >= G1 + 0.01, stopped(v1, u), u is not None and x2 >= G2 + 0.01))
    return out

def s_do(img, d, t, sc):
    i, u, k = do_state(t); v1 = ROWS[i][0]; yb = 700
    x1, x2, d1, d2 = rig(d, v1, -1 if u is None else u, k=k)
    if stopped(v1, u):
        ks = appear(u, (XC1 - X1S) / v1 + TC, 0.3) * k
        rs(d, sx(x1), yb + 80, "v_{1}′ = 0", 42, C1D, alpha=ks)
    table(d, cells_at(t), hl=i if t >= R0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: o bang = cong quang / xe 1 da dung ; xe 2 khong qua chan cuoi ; vong lo xo khong am."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, u, k = do_state(t); v1 = ROWS[i][0]
        if t >= R0:
            x1, x2, rg = kin(v1, -1 if u is None else u)
            c = cells_at(t)[i]
            if c != (u is not None and x1 >= G1 + 0.01, stopped(v1, u), u is not None and x2 >= G2 + 0.01): bad.append(("bang", round(t, 2)))
            if rg < 0.004: bad.append(("lo xo", round(t, 2)))
            if x2 - x1 < CL + rg - 1e-6: bad.append(("xe chong", round(t, 2)))
        t += 0.05
    if DO_END > sc["T"] - 0.2: bad.append(("lan 3 sat cuoi canh", round(DO_END, 2), round(sc["T"], 2)))
    for v1, a, b in ROWS:
        x1, x2, _ = kin(v1, run_len(v1) - 0.15 - 0.6 + 0.01)
        if x2 < G2 + 0.01: bad.append(("cong 2 chua doc", v1))
    return bad

# ---------------- canh 3: Dap an ----------------
def badge(d, y, lab, col, alpha=1.0, size=40):
    pw = tw(d, lab, F(size)) + 56
    card(d, (W / 2 - pw / 2, y - 34, W / 2 + pw / 2, y + 34), fill=A(col, alpha), r=34)
    text(d, (W / 2, y), lab, size, WHITE, alpha=alpha)

def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.15, 0.4)
    badge(d, 300, "ĐÁP ÁN · xe 1 dừng, xe 2 đi tiếp", NAVY, ka)
    card(d, (40, 360, 1040, 1150), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 410), "Lần 2", 42, INK, anchor="lm")
    L = 0.50 * 560                                             # mui ten dong luong: dai theo m.v (cung ti le)
    for j, (lab, at) in enumerate((("trước", 0.3), ("sau", 1.2))):
        yb = 640 + j * 300; kk = appear(t, at, 0.45)
        text(d, (80, yb - 120), lab, 42, MUTED, anchor="lm", alpha=kk)
        track(d, yb, kk)
        if j == 0:
            cart(d, yb, 0.30, C1, C1D, "1", kk, ring=RING); cart(d, yb, X2S, C2, C2D, "2", kk)
            g = ease((t - at - 0.3) / 0.4)
            if g > 0:
                X = sx(0.30); arrow(d, (X - L / 2, yb + 70), (X - L / 2 + L * g, yb + 70), C1, w=8, head=22)
                text(d, (X + L / 2 + 20, yb + 70), "p xe 1", 42, C1D, anchor="lm", alpha=g)
        else:
            x1 = XC1 + 0.5 * TC / 2
            cart(d, yb, x1, C1, C1D, "1", kk, ring=RING); cart(d, yb, 0.92, C2, C2D, "2", kk)
            text(d, (sx(x1), yb + 70), "dừng", 42, C1D, alpha=kk)
            g = ease((t - at - 0.3) / 0.4)
            if g > 0:
                X = sx(0.92); arrow(d, (X - L / 2, yb + 70), (X - L / 2 + L * g, yb + 70), C2, w=8, head=22)
                text(d, (X - L / 2 - 20, yb + 120), "p′ xe 2", 42, C2D, anchor="lm", alpha=g)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 320), "Động năng (lần 2)", 44, INK)
    by, H0 = 770, 300
    cols = (("trước", (1.0, 0.0)), ("sau", (0.0, 1.0)))
    for j, (lab, (e1, e2)) in enumerate(cols):
        cx = 300 + j * 480; g = ease((t - 0.4 - 0.9 * j) / 0.5)
        for dx, e, col, nm in ((-75, e1, C1, "xe 1"), (75, e2, C2, "xe 2")):
            h = H0 * e * g
            if h > 2: d.rectangle([cx + dx - 55, by - h, cx + dx + 55, by], fill=col)
            text(d, (cx + dx, by + 40), nm, 40, C1D if col == C1 else C2D)
        text(d, (cx, by + 95), lab, 42, INK)
    d.line([(120, by), (960, by)], fill=INK, width=4)
    k5 = appear(t, M[1] - 0.1, 0.45)
    if k5 > 0:
        y0 = 940 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 270), fill=A((254, 242, 242), k5), outline=A(RED, k5), w=5)
        text(d, (W / 2, y0 + 62), "Thí nghiệm chưa nói được", 44, NAVY, alpha=k5)
        ctext(d, y0 + 170, "hai xe khác khối lượng", 46, RED, alpha=k5)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.2, 0.45)
    card(d, (40, 265, 1040, 640), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    badge(d, 322, "BẪY", RED, a1, 38)
    ks = clamp((t - M[0] - 1.0) / 0.4); f = F(46)
    for j, q in enumerate(("“Mọi va chạm: hai xe", "đi chung, nửa tốc độ”")):
        yy = 445 + j * 70; lw = tw(d, q, f)
        text(d, (W / 2, yy), q, 46, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * a1), width=5)
    text(d, (W / 2, 580), "✗", 56, RED, alpha=ks)
    kk = appear(t, M[1] - 0.1, 0.45)
    if kk <= 0: return
    card(d, (40, 680, 1040, 1330), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
    for j, (lab, col_lab) in enumerate((("Dính (sáp):", MUTED), ("Lò xo lá:", DGREEN))):
        yb = 900 + j * 300; g = appear(t, M[1] + 0.2 + 1.0 * j, 0.4)
        text(d, (80, yb - 140), lab, 44, col_lab, anchor="lm", alpha=g)
        track(d, yb, g)
        if j == 0:
            cart(d, yb, 0.52, C1, C1D, "1", g); cart(d, yb, 0.66, C2, C2D, "2", g)
            X = sx(0.59); arrow(d, (X - 70, yb + 70), (X + 70, yb + 70), A(PURPLE, g), w=7, head=20)
            text(d, (X + 95, yb + 70), "0,25 m/s", 42, PURPLE, anchor="lm", alpha=g)
        else:
            cart(d, yb, XC1 + 0.5 * TC / 2, C1, C1D, "1", g, ring=RING); cart(d, yb, 0.92, C2, C2D, "2", g)
            text(d, (sx(XC1 + 0.02), yb - 140), "dừng", 42, C1D, alpha=g)
            X = sx(0.92); arrow(d, (X - 140, yb + 70), (X + 30, yb + 70), A(C2, g), w=7, head=20)
            text(d, (X - 160, yb + 70), "0,50 m/s", 42, C2D, anchor="rm", alpha=g)

# ---------------- canh 6: Chot ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        if k < 0.02: return
        yb = 1130
        track(d, yb, k)
        cart(d, yb, 0.30, C1, C1D, "1", k, ring=RING); cart(d, yb, 0.70, C2, C2D, "2", k)
        X1, X2 = sx(0.30), sx(0.70)
        arrow(d, (X1 - 60, yb + 70), (X1 + 108, yb + 70), A(C1, k), w=7, head=20)        # 0,60 m/s ~ 168 px
        text(d, (X1 + 24, yb + 120), "0,60 m/s", 42, C1D, alpha=k)
        arrow(d, (X2 - 28, yb + 70), (X2 + 28, yb + 70), A(C2, k), w=7, head=20)         # 0,20 m/s ~ 56 px
        text(d, (X2, yb + 120), "0,20 m/s", 42, C2D, alpha=k)
        kh = appear(t, M[0] + 2.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1320, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1370), "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1455, "Xe 2 đang chạy", 42, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Đàn hồi: động năng gần giữ nguyên",
             "Va chạm đàn hồi, hai xe cùng 0,20 kg. Tốc độ xe 1 sau đó?", None, body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for j, (v1, a, bb) in enumerate(ROWS):                   # va cham
        out.append((do["t0"] + STARTS[j] + 0.15 + (XC1 - X1S) / v1, "tap"))
    out += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l10-baotoandl-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Bảo toàn động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai xe có đệm lò xo", draw=s_hook, tail=0.6, caps=[
   ("Hai xe bằng khối lượng.", 3.0),
   ("Dừng video, chọn câu trả lời.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Ba lần, xe 1 nhanh hơn.", 3.4),
   ("Nhìn xe 1 sau va chạm.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Xe 1 dừng, xe 2 lao đi.", 3.4),
   ("Động lượng chuyển sang xe 2.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Động năng cũng chuyển sang xe 2.", 3.4),
   ("Còn điều gì chưa thử?", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Nhầm với va chạm mềm.", 3.0),
   ("Cùng tốc độ tới, kết quả khác.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự tính.", 6.0)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("số:", _kiem_so() or "khớp kho"); print("đồng bộ:", _kiem_dong_bo() or "không lệch")
