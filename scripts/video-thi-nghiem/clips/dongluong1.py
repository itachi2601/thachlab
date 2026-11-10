# Clip: tn-l10-dongluong-01 - Xe tren ray dem khi bat vao dem lo xo gan cam bien luc (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dongluong-01.json:
#   tham_so: m = 0,250 kg (co dinh), e (0..1) ; so_lieu_mau: v1 / v2 / cam bien = 0,40 / -0,32 / 0,176 ...
#   ghi_chu: m(v2 - v1) = 0,180 ; 0,2725 ; 0,3575 ; 0,4525 kg.m/s.
#   Cau chot dung tham_so trong mien cho phep (v1 = 0,50 m/s, e = 0: xe dinh vao dem) -> 0,125, chua tung hien.
# Truc chinh: xe + dem lo xo + DAU cua van toc (chieu duong ro, v2 doi dau). Khac dongluong2 (bi + mang nghieng + khuc go).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (xe chay, cong quang, do thi F-t) -> Dap an + bang 4 lan
#       -> Rut ra (vecto p1, p2, dp; luc dem cung huong dp; chua noi duoc) -> Bay (quen doi dau) -> Chot + cau hoi.
from engine import *

M_XE = 0.25
ROWS = [(0.40, -0.32, 0.180, 0.176), (0.60, -0.49, 0.2725, 0.268),
        (0.80, -0.63, 0.3575, 0.352), (1.00, -0.81, 0.4525, 0.445)]      # v1, v2, |m(v2-v1)| (ghi_chu), cam bien
CART = (59, 130, 246); RAIL = (196, 200, 212); RAIL_D = (150, 155, 170)
XFREE, XBLK = 905, 985          # dau tu do cua lo xo / mat cam bien
CW = 170                        # be rong xe
GX = 520                        # cong quang

def vn(x, nd=None):
    s = (f"{x:.{nd}f}" if nd is not None else f"{x:g}").replace(".", ",")
    return s.replace("-", "−")

# chu co chi so duoi: chi so >= 36 px (brief: chu phu >= 36 px truoc khi thu x0,88)
def rt(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    segs = []
    for p in [p for p in re.split(r"(_\{[^}]*\})", s) if p]:
        if p.startswith("_{"): segs.append((p[2:-1], max(36, int(size * 0.66)), size * 0.26))
        else: segs.append((p, size, 0))
    tot = sum(tw(d, t, F(sz)) for t, sz, _ in segs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for t, sz, dy in segs:
        dtext(d, (x, cy + dy), t, F(sz), color, alpha, "lm"); x += tw(d, t, F(sz))
    return tot

# ---------------- hinh: ray, xe, dem lo xo, cong quang ----------------
def ray(d, yr, comp=0.0, label=False, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rectangle([50, yr, XBLK, yr + 26], fill=c(RAIL), outline=c(RAIL_D), width=3)
    for x in range(80, XBLK - 20, 46): d.ellipse([x - 4, yr + 9, x + 4, yr + 17], fill=c(RAIL_D))
    d.rectangle([XBLK, yr - 120, 1040, yr + 40], fill=c(NAVY))                 # cam bien luc gan tuong
    d.rectangle([XBLK - 14, yr - 70, XBLK, yr - 20], fill=c(GRAY))            # dau do
    x0 = XFREE - comp; n = 12; pts = []
    for i in range(n + 1):
        x = lerp(x0, XBLK - 14, i / n); pts.append((x, yr - 45 + (0 if i in (0, n) else (18 if i % 2 else -18))))
    d.line(pts, fill=c(INK), width=5)
    d.rectangle([x0 - 8, yr - 72, x0, yr - 18], fill=c(INK))                   # dia tiep xuc
    if label: text(d, (1035, yr - 160), "cảm biến lực", 40, INK, anchor="rm", alpha=alpha)

def xe(d, xr, yr, dirn=0, alpha=1.0):
    """Xe: canh phai o xr. dirn = +1/-1 ve mui ten trang tren than xe (chieu chuyen dong)."""
    c = lambda col: A(col, alpha); xl = xr - CW
    d.rounded_rectangle([xl, yr - 84, xr, yr - 2], radius=12, fill=c(CART), outline=c(NAVY), width=4)
    xm = xl + CW / 2
    d.rectangle([xm - 6, yr - 150, xm + 6, yr - 84], fill=c(INK))                 # tam chan sang
    if dirn:
        a, b = (xm - 50 * dirn, yr - 43), (xm + 50 * dirn, yr - 43)
        arrow(d, a, b, c(WHITE), w=7, head=18)

def cong(d, yr, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rectangle([GX - 11, yr - 225, GX + 11, yr - 100], fill=c((71, 85, 105)))
    d.rectangle([GX - 22, yr - 140, GX + 22, yr - 104], fill=c((71, 85, 105)))
    dot(d, GX, yr - 122, 7, c(RED))

def truc_duong(d, x0, y, alpha=1.0):
    arrow(d, (x0, y), (x0 + 200, y), A(INK, alpha), w=6, head=20)
    text(d, (x0 + 230, y), "chiều dương (+)", 40, INK, anchor="lm", alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 585), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 300), "Lúc tới", 40, MUTED, anchor="lm")
    ray(d, 500); xe(d, 640, 500)
    arrow(d, (555, 318), (755, 318), BLUE, w=8, head=24)                       # 0,40 m/s -> 200 px
    text(d, (775, 318), "0,40 m/s", 44, BLUE, anchor="lm")
    truc_duong(d, 80, 556)
    card(d, (40, 605, 1040, 925), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 640), "Lúc bật lại", 40, MUTED, anchor="lm")
    ray(d, 840); xe(d, 760, 840)
    arrow(d, (675, 658), (515, 658), GREEN, w=8, head=24)                      # 0,32 m/s -> 160 px
    text(d, (495, 658), "0,32 m/s", 44, GREEN, anchor="rm")
    text(d, (80, 893), "xe m = 0,250 kg", 44, NAVY, anchor="lm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 200, "Độ biến thiên động lượng", 50, INK, maxw=880, alpha=a)
    ctext(d, y0 + 280, "của xe có độ lớn bao nhiêu?", 50, INK, maxw=880, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 484], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 484], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
X_START, V_IN = 260, 360.0                 # px/s luc toi; luc ve 0,8 lan (0,32 / 0,40)
TA = (XFREE - X_START) / V_IN              # thoi gian chay toi dem
TC = 1.5                                   # thoi gian tiep xuc tren man (chieu cham)
V_OUT = V_IN * 0.32 / 0.40
X_END = 200
CMAX = 70
def ts_do(sc): return sc["M"][1] - TA      # dem bat dau nen dung luc phu de 2 len

def motion(t, sc):
    """-> (canh phai xe, do nen lo xo, chieu chuyen dong, pha 0..3)."""
    u = t - ts_do(sc)
    if u <= 0: return X_START, 0.0, 0, 0
    if u < TA: return X_START + V_IN * u, 0.0, 1, 1
    u -= TA
    if u < TC:
        c = CMAX * math.sin(math.pi * u / TC); return XFREE - c, c, (1 if u < TC / 2 else -1), 2
    u -= TC
    return max(X_END, XFREE - V_OUT * u), 0.0, (-1 if XFREE - V_OUT * u > X_END else 0), 3

def doc_cong(t, sc):
    """Cong quang chi hien so sau khi tam chan sang di qua het chum sang (dong pha voi xe)."""
    xr, _, _, ph = motion(t, sc); xm = xr - CW / 2
    v1 = ph >= 2 or (ph == 1 and xm > GX + 10)
    v2 = ph == 3 and xm < GX - 10
    return v1, v2

G_X0, G_X1, G_Y0, G_YT = 150, 980, 1240, 330      # goc do thi, dinh xung = 330 px
G_PAD = 0.5
def gx(u): return G_X0 + (u + G_PAD) / (TC + 2 * G_PAD) * (G_X1 - G_X0)
def gF(u): return G_YT * math.sin(math.pi * u / TC) if 0 <= u <= TC else 0.0

def s_do(img, d, t, sc):
    M = sc["M"]; yr = 660
    card(d, (40, 265, 1040, 765), fill=WHITE, outline=LIGHT, w=3)
    xr, comp, dirn, ph = motion(t, sc)
    ray(d, yr, comp, label=True); xe(d, xr, yr, dirn); cong(d, yr)
    truc_duong(d, 80, 728)
    v1, v2 = doc_cong(t, sc)
    card(d, (330, 290, 760, 440), fill=NAVY, r=20)
    rt(d, 360, 330, "v_{1} = 0,40 m/s" if v1 else "v_{1} = …", 44, YELLOW if v1 else GRAY, anchor="l")
    rt(d, 360, 398, "v_{2} = −0,32 m/s" if v2 else "v_{2} = …", 44, YELLOW if v2 else GRAY, anchor="l")
    text(d, (GX - 28, 470), "cổng quang", 40, INK, anchor="rm")
    # do thi F - t
    card(d, (40, 790, 1040, 1330), fill=WHITE, outline=LIGHT, w=3)
    arrow(d, (G_X0, G_Y0), (G_X1 + 30, G_Y0), INK, w=4, head=16)
    arrow(d, (G_X0, G_Y0), (G_X0, G_Y0 - G_YT - 60), INK, w=4, head=16)
    text(d, (G_X0 + 24, G_Y0 - G_YT - 50), "F (độ lớn)", 44, INK, anchor="lm")
    text(d, (G_X1 + 30, G_Y0 + 40), "t", 44, INK)
    uc = t - ts_do(sc) - TA                         # thoi gian tinh tu luc cham dem
    if uc > -G_PAD:
        ue = min(uc, TC + G_PAD)
        if uc >= TC:
            poly = [(gx(0), G_Y0)] + [(gx(TC * i / 60), G_Y0 - gF(TC * i / 60)) for i in range(61)] + [(gx(TC), G_Y0)]
            d.polygon(poly, fill=A((253, 186, 116), appear(uc, TC, 0.5)))
        n = 120; pts = []
        for i in range(n + 1):
            u = -G_PAD + (ue + G_PAD) * i / n; pts.append((gx(u), G_Y0 - gF(u)))
        d.line(pts, fill=RED, width=6)
        dot(d, pts[-1][0], pts[-1][1], 9, RED)
        if uc >= TC:
            k = appear(uc, TC + 0.2, 0.5)
            text(d, (gx(TC / 2), G_Y0 - 95), "0,176 N·s", 44, INK, alpha=k)
            text(d, (W / 2, 1400), "diện tích = xung lượng", 40, INK, alpha=k)
    if 0 < t - ts_do(sc) < TA + TC + 0.4:
        text(d, (W / 2, 1490), "quay chậm", 42, INK)

# ---------------- canh 3: Dap an + bang 4 lan ----------------
COLS = (165, 400, 650, 890)
DP3 = ("0,180", "0,273", "0,358", "0,453")     # ghi_chu 0,180 / 0,2725 / 0,3575 / 0,4525 lam tron len 3 chu so
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · khoảng 0,18 kg·m/s"
    pw = tw(d, lb, F(38)) + 56
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 314), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 282), lb, 38, WHITE, alpha=ka)
    card(d, (40, 345, 1040, 625), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5)
    rt(d, W / 2, 415, "Δp = 0,250 · (−0,32 − 0,40)", 50, INK, alpha=ka)
    k2 = appear(t, 0.9, 0.5)
    text(d, (W / 2, 492), "= −0,180 kg·m/s", 52, GREEN, alpha=k2)
    text(d, (W / 2, 570), "cảm biến: 0,176 N·s", 42, INK, alpha=k2)
    k3 = appear(t, M[0] + 1.4, 0.5)
    if k3 <= 0: return
    y = 660
    card(d, (40, y, 1040, y + 700), fill=A(WHITE, k3), outline=A(LIGHT, k3), w=3)
    for x, s in zip(COLS, ("v_{1}", "v_{2}", "|Δp|", "cảm biến")): rt(d, x, y + 55, s, 44, INK, alpha=k3)
    for x, s in zip(COLS, ("m/s", "m/s", "kg·m/s", "N·s")): text(d, (x, y + 112), s, 38, INK, bold=False, alpha=k3)
    d.line([(70, y + 150), (1010, y + 150)], fill=A(LIGHT, k3), width=3)
    kh = appear(t, M[1] - 0.1, 0.4)
    if kh > 0:
        d.rounded_rectangle([530, y + 12, 1022, y + 690], radius=24, outline=A(ORANGE, kh), width=6)
        text(d, (W / 2, y + 760), "1 N·s = 1 kg·m/s", 42, ORANGE, alpha=kh)
    for j, (v1, v2, dp, J) in enumerate(ROWS):
        k = appear(t, M[0] + 1.6 + 0.35 * j, 0.4); yy = y + 230 + j * 125
        text(d, (COLS[0], yy), vn(v1, 2), 48, INK, alpha=k)
        text(d, (COLS[1], yy), vn(v2, 2), 48, RED, alpha=k)
        text(d, (COLS[2], yy), DP3[j], 48, NAVY, alpha=k)
        text(d, (COLS[3], yy), vn(J, 3), 48, NAVY, alpha=k)

# ---------------- canh 4: Rut ra (vecto + luc dem + chua noi duoc) ----------------
PX = 4000                       # px / (kg.m/s): p1 = 0,10 -> 400 px, p2 = 0,08 -> 320 px, dp = 0,18 -> 720 px
OX = 560
def dash(d, p, q, col, w=4, n=10):
    for i in range(n):
        a0, a1 = i / n, (i + 0.5) / n
        d.line([(lerp(p[0], q[0], a0), lerp(p[1], q[1], a0)), (lerp(p[0], q[0], a1), lerp(p[1], q[1], a1))], fill=col, width=w)

def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    truc_duong(d, 80, 320)
    x1, x2 = OX + 0.10 * PX, OX - 0.08 * PX
    d.line([(OX, 380), (OX, 560)], fill=GRAY, width=3)
    arrow(d, (OX, 420), (x1, 420), BLUE, w=8, head=24); rt(d, (OX + x1) / 2, 380, "p_{1}", 48, BLUE)
    arrow(d, (OX, 520), (x2, 520), GREEN, w=8, head=24); rt(d, (OX + x2) / 2, 480, "p_{2}", 48, GREEN)
    kd = appear(t, 0.6, 0.6)
    if kd > 0:
        dash(d, (x1, 432), (x1, 640), A(MUTED, kd)); dash(d, (x2, 532), (x2, 640), A(MUTED, kd))
        xe_ = lerp(x1, x2, ease(clamp((t - 0.6) / 0.9)))
        arrow(d, (x1, 650), (xe_, 650), A(ORANGE, kd), w=10, head=28)
        rt(d, (x1 + x2) / 2, 705, "Δp = p_{2} − p_{1}", 42, ORANGE, alpha=appear(t, 1.4, 0.4))
    k1 = appear(t, M[0] + 0.6, 0.5)
    card(d, (40, 830, 1040, 1110), fill=A((255, 247, 237), k1), outline=A(ORANGE, k1), w=5)
    arrow(d, (330, 905), (130, 905), A(RED, k1), w=8, head=24)
    text(d, (360, 905), "lực đệm lên xe", 42, RED, anchor="lm", alpha=k1)
    text(d, (W / 2, 990), "F·Δt = Δp", 54, GREEN, alpha=k1)
    text(d, (W / 2, 1060), "ngược chiều dương", 40, INK, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y0 = 1140 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 450), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 65), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        card(d, (80, y0 + 130, 1000, y0 + 410), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, y0 + 210), "ray có ma sát?", 46, RED, alpha=kk)
        text(d, (W / 2, y0 + 320), "xe khối lượng khác?", 46, RED, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    card(d, (40, 265, 1040, 700), fill=WHITE, outline=LIGHT, w=3)
    ray(d, 640); xe(d, 640, 640)
    arrow(d, (470, 345), (630, 345), BLUE, w=8, head=24); rt(d, 650, 345, "v_{1} = 0,40 m/s", 44, BLUE, anchor="l")
    arrow(d, (630, 432), (502, 432), GREEN, w=8, head=24); rt(d, 482, 432, "v_{2} = −0,32 m/s", 44, GREEN, anchor="r")
    a1 = appear(t, 0.2, 0.45); y0 = 740
    card(d, (40, y0, 1040, y0 + 820), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    q = "Δp = 0,250 · (0,40 − 0,32) = 0,02"
    ks = clamp((t - 1.0) / 0.4); f = F(46); lw = tw(d, q, f); yy = y0 + 200
    text(d, (W / 2, yy), q, 46, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
    kk = a1 * appear(t, 1.5, 0.5)
    card(d, (90, y0 + 330, 990, y0 + 740), fill=A((236, 253, 243), kk), r=24)
    rt(d, W / 2, y0 + 420, "v_{2} = −0,32 m/s", 46, GREEN, alpha=kk)
    rt(d, W / 2, y0 + 530, "Δp = 0,250 · (−0,32 − 0,40)", 46, GREEN, alpha=kk)
    text(d, (W / 2, y0 + 640), "|Δp| = 0,18 kg·m/s", 50, GREEN, alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        if k > 0.02:                                   # hinh: xe dinh vao dem
            yr = 1220
            d.rectangle([140, yr, XBLK - 40, yr + 22], fill=A(RAIL, k), outline=A(RAIL_D, k), width=3)
            d.rectangle([XBLK - 40, yr - 110, XBLK + 10, yr + 34], fill=A(NAVY, k))
            n = 10; pts = [(lerp(XBLK - 140, XBLK - 40, i / n), yr - 45 + (0 if i in (0, n) else (16 if i % 2 else -16))) for i in range(n + 1)]
            d.line(pts, fill=A(INK, k), width=5)
            d.rounded_rectangle([XBLK - 140 - CW, yr - 84, XBLK - 140, yr - 2], radius=12, fill=A(CART, k), outline=A(NAVY, k), width=4)
            text(d, (330, yr - 45), "0,50 m/s", 44, BLUE, alpha=k)
            arrow(d, (230, yr - 100), (430, yr - 100), A(BLUE, k), w=7, head=20)
        kh = appear(t, M[0] + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 1290, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1350), "Gợi ý", 40, INK, alpha=kh)
        rt(d, W / 2, 1450, "v_{2} bằng bao nhiêu?", 46, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Nếu xe bật ngược lại thì\nvận tốc về mang dấu trừ",
             "Cùng xe, tới 0,50 m/s\nrồi dừng hẳn tại đệm. |Δp| = ?", None, body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + ts_do(do) + TA, "tap"), (do["t0"] + ts_do(do) + TA + TC, "tap"),
            (da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][0] + 0.6, "tap"),
            (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-dongluong-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe bật vào đệm lò xo", draw=s_hook, tail=0.8, caps=[
   ("Xe bật ngược lại khỏi đệm.", 3.0),
   ("Dừng video, chọn câu trả lời.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.9, caps=[
   ("Đo vận tốc tới và về.", 4.2),
   ("Đệm nén: cảm biến ghi lực.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Vận tốc lúc về mang dấu trừ.", 3.0),
   ("Bốn lần đo, hai cột gần bằng nhau.", 3.0)]),
 dict(key="rutra", title="Vì sao?", draw=s_rutra, tail=0.6, caps=[
   ("Đệm đẩy xe về phía âm.", 3.0),
   ("Chưa kiểm hai điều.", 4.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.5, caps=[
   ("Lấy hiệu hai tốc độ là sai.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.4, caps=[
   ("Dừng video, tự trả lời.", 5.4)]),
])
