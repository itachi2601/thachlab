# Clip: tn-l10-nemngang-02 - Ban bi ngang o ba do cao: do tam xa, suy ra van toc nem (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-nemngang-02.json:
#   tham_so: v0 = 1,5 m/s (giu nguyen khi doi h), g = 9,8 m/s2, h trong mien 0,2..1,5 m (buoc 0,05).
#   so_lieu_mau: h = 0,45 / 0,80 / 0,80 / 1,25 m -> t = 0,303 / 0,404 / 0,404 / 0,505 s,
#                L do = 0,451 / 0,611 / 0,606 / 0,757 m, v0 = L/t = 1,49 / 1,51 / 1,50 / 1,50 m/s.
#   Cau chot dung tham_so trong mien (h = 0,60 m, v0 = 1,50 m/s): t = 0,350 s, L = 0,525 m -- chua tung hien.
# Trong tam (hop data-exp trong bai): ca bon lan deu cho v0 ~ 1,50 m/s; do cao chi doi thoi gian roi va tam xa.
# Truc chinh: quy dao vẽ DUNG TI LE (480 px/m ca hai phuong, truc co dinh), vet giay than + bang h-t-L
#   (khac dog2: do thi s-t^2; khac roitudo2: nhieu anh roi thang dung).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (4 lan ban, chieu cham 3 lan, chip nhac cau hoi)
#       -> Dap an (cot v0 = L/t) -> Rut ra (do thi L-t qua goc; chua noi duoc) -> Bay (L ti le h) -> Chot.
# Mau: h = PURPLE, t = TEAL, L = ORANGE, v0 = BLUE; bi = xam thep; quy dao = xam.
from engine import *

G = 9.8
V0 = 1.50
ROWS = [(0.45, 0.303, 0.451, 1.49), (0.80, 0.404, 0.611, 1.51),
        (0.80, 0.404, 0.606, 1.50), (1.25, 0.505, 0.757, 1.50)]                 # so_lieu_mau
STEEL = (110, 120, 140); GHOST = (190, 196, 210); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
PAPER = (60, 64, 80)

def vn(x, nd=2):
    return f"{x:.{nd}f}".replace(".", ",")

# ---------------- khung dung ti le (dung chung) ----------------
PXM = 480.0                    # px / m, ca hai phuong (quy dao dung ti le)
YF = 980                       # mat ban
X0 = 300                       # dau nong sung (x = 0 cua tam xa)
POLE = 215                     # cot gia do
def P(x, y): return (X0 + x * PXM, YF - y * PXM)

def setup(d, h, alpha=1.0, marks=True):
    """Ban + gia + sung o do cao h (m), thuoc cuon tren ban, giay than."""
    c = lambda col: A(col, alpha)
    d.rectangle([60, YF, 1020, YF + 34], fill=c(WOOD), outline=c(WOOD_D), width=3)            # mat ban
    # giay than (0,30 .. 0,85 m)
    x1, x2 = P(0.30, 0)[0], P(0.85, 0)[0]
    d.rectangle([x1, YF - 7, x2, YF], fill=c(PAPER))
    # thuoc cuon: vach moi 0,1 m, ghi so moi 0,2 m (36 px)
    d.rectangle([X0, YF + 34, P(0.85, 0)[0], YF + 58], fill=c((253, 224, 71)), outline=c(WOOD_D), width=2)
    for k in range(0, 9):
        xx = P(k / 10, 0)[0]
        L = 24 if k % 2 == 0 else 14
        d.line([(xx, YF + 34), (xx, YF + 34 + L)], fill=c(NAVY), width=3)
        if k % 2 == 0: text(d, (xx, YF + 92), vn(k / 10, 1) if k else "0", 36, INK, alpha=alpha)
    text(d, (P(0.85, 0)[0] + 18, YF + 92), "m", 36, INK, anchor="lm", alpha=alpha)
    # gia do
    top = YF - 1.32 * PXM
    d.rectangle([POLE - 9, top, POLE + 9, YF], fill=c((120, 128, 145)))
    d.rectangle([POLE - 60, YF - 16, POLE + 60, YF], fill=c((90, 98, 115)))
    if marks:                                                                   # vach do cao tren cot
        for hh in (0.45, 0.80, 1.25):
            yy = P(0, hh)[1]
            d.line([(POLE - 30, yy), (POLE - 9, yy)], fill=c(PURPLE), width=4)
            text(d, (POLE - 40, yy), vn(hh), 36, PURPLE, anchor="rm", alpha=alpha)
    # sung: than + nong nam ngang, dau nong o X0
    yy = P(0, h)[1]
    d.rounded_rectangle([POLE - 20, yy - 20, X0 - 34, yy + 20], radius=8, fill=c(NAVY))
    d.rectangle([X0 - 36, yy - 9, X0, yy + 9], fill=c((60, 70, 100)))
    d.rectangle([POLE - 16, yy + 18, POLE + 16, yy + 30], fill=c((70, 78, 95)))           # kep

def ball(d, x, y, r=10, col=STEEL):
    dot(d, x, y, r, col, outline=NAVY)

def path_pts(h, L, tt, n=40):
    v = L / tt
    return [P(v * tt * i / n, h - G / 2 * (tt * i / n) ** 2) for i in range(n + 1)]

def chip(d):
    """Chip nho nhac cau hoi du doan (vien tim, chu tim nhat -- khong phai so do)."""
    f = F(36, False); w = tw(d, "Câu hỏi:", f) + 16 + rich_w(d, "v_{0} = L/t ở ba độ cao thế nào?", 40) + 50
    card(d, (W / 2 - w / 2, 266, W / 2 + w / 2, 330), fill=(245, 243, 255), outline=PURPLE, r=32, w=3)
    x = W / 2 - w / 2 + 25
    dtext(d, (x, 297), "Câu hỏi:", F(36, False), PURPLE, 1.0, "lm"); x += tw(d, "Câu hỏi:", f) + 16
    rx(d, x, 295, "v_{0} = L/t ở ba độ cao thế nào?", 40, PURPLE, anchor="l")

def _segs(s, size):
    """Chi so duoi >= 36 px (quy tac lo: chu trong ham ve, ke ca chi so, >= 36 px)."""
    out = []
    for p in [p for p in TOK.split(s) if p]:
        if p.startswith("_{"): out.append((p[2:-1], max(36, int(size * 0.75)), size * 0.26))
        else: out.append((p, size, 0))
    return out

def rich_w(d, s, size):
    return sum(tw(d, q, F(sz)) for q, sz, _ in _segs(s, size))

def rx(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    x = cx - rich_w(d, s, size) / 2 if anchor == "m" else cx
    for q, sz, dy in _segs(s, size):
        dtext(d, (x, cy + dy), q, F(sz), color, alpha, "lm"); x += tw(d, q, F(sz))

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1130), fill=WHITE, outline=LIGHT, w=3)
    setup(d, 0.80)
    y = P(0, 0.80)[1]
    arrow(d, (X0 + 10, y), (X0 + 150, y), BLUE, w=7, head=20)                  # van toc nem, nam ngang
    rx(d, X0 + 80, y + 46, "v_{0}", 46, BLUE)
    text(d, (POLE - 40, 330), "h (m)", 38, PURPLE, anchor="rm")
    lp = P(0.62, 0)                                                            # nhan giay than co duong dan
    d.line([(lp[0], YF - 10), (lp[0] + 60, YF - 150)], fill=INK, width=3)
    text(d, (lp[0] + 70, YF - 175), "giấy than", 40, INK, anchor="lm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1150 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 450), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 84), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 53), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    text(d, (W / 2, y0 + 140), "Nòng nằm ngang, đặt ở ba độ cao.", 44, INK, alpha=a)
    rx(d, W / 2, y0 + 215, "Vận tốc ném v_{0} = L/t đo được", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 285), "sẽ thế nào?", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 355), "L: tầm xa · t: thời gian rơi", 40, INK, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.5
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 410, 940, y0 + 424], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 410, 140 + 800 * (1 - p), y0 + 424], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (4 lan ban, chieu cham 3 lan) ----------------
SLOW = 3.0
MOVE, HOLD, RUN0 = 0.55, 0.65, 0.5
def schedule():
    out = []; s = RUN0
    for i, (h, tt, L, v) in enumerate(ROWS):
        mv = MOVE if (i == 0 or ROWS[i - 1][0] != h) else 0.25
        out.append((s, mv)); s += mv + tt * SLOW + HOLD
    return out
SCHED = schedule()

def shot_state(t):
    """-> (lan j, do cao sung hien tai, tau that trong luc bay (None neu chua ban), so hang da xong)."""
    j = 0
    for i, (s, mv) in enumerate(SCHED):
        if t >= s: j = i
    s, mv = SCHED[j]
    h, tt, L, v = ROWS[j]
    hp = ROWS[j - 1][0] if j > 0 else 0.80
    if t < s: return 0, 0.80, None, 0
    hc = lerp(hp, h, ease((t - s) / mv)) if t < s + mv else h
    if t < s + mv: return j, hc, None, j
    tau = min((t - s - mv) / SLOW, tt)
    return j, h, tau, j + (1 if (t - s - mv) / SLOW >= tt else 0)

def s_do(img, d, t, sc):
    chip(d)
    j, hc, tau, done = shot_state(t)
    card(d, (40, 340, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    setup(d, hc)
    for i in range(done):                                                    # quy dao + vet cac lan truoc
        h, tt, L, v = ROWS[i]
        if i == j: continue
        d.line(path_pts(h, L, tt), fill=GHOST, width=3)
        lx = P(L, 0)[0]; d.line([(lx, YF - 18), (lx, YF + 2)], fill=ORANGE, width=5)
    h, tt, L, v = ROWS[j]
    if tau is None:
        ball(d, X0 + 4, P(0, hc)[1])
    else:
        vx = L / tt
        n = int(tau / 0.05)
        for k in range(1, n + 1):                                            # vet bong moi 0,05 s
            tk = k * 0.05
            gx, gy = P(vx * tk, h - G / 2 * tk * tk); dot(d, gx, gy, 7, GHOST)
        bx, by = P(vx * tau, h - G / 2 * tau * tau); by -= 10 * min(1.0, tau / tt)
        if tau >= tt - 1e-9:
            d.line(path_pts(h, L, tt), fill=GHOST, width=3)
            lx = P(L, 0)[0]; d.line([(lx, YF - 18), (lx, YF + 2)], fill=ORANGE, width=5)
        ball(d, bx, by)
    # so doc ben phai (dong pha voi lan ban)
    text(d, (1000, 400), "chiếu chậm 3 lần", 38, INK, bold=False, anchor="rm")
    if t >= SCHED[0][0]:
        text(d, (1000, 470), "h = " + vn(ROWS[j][0]) + " m", 46, PURPLE, anchor="rm")
    if done > j:
        text(d, (1000, 540), "L = " + vn(L, 3) + " m", 46, ORANGE, anchor="rm")
    # bang h - t - L
    y = 1120
    card(d, (40, y, 1040, y + 470), fill=WHITE, outline=LIGHT, w=3)
    XS = (220, 540, 860)
    text(d, (XS[0], y + 50), "h (m)", 42, PURPLE)
    text(d, (XS[1], y + 50), "t = √(2h/g) (s)", 42, TEAL)
    text(d, (XS[2], y + 50), "L đo (m)", 42, ORANGE)
    d.line([(70, y + 90), (1010, y + 90)], fill=LIGHT, width=3)
    for i, (h, tt, L, v) in enumerate(ROWS):
        yy = y + 140 + i * 82
        if i == j and done <= i:
            d.rounded_rectangle([60, yy - 36, 1020, yy + 36], radius=16, fill=(255, 247, 237))
        if i < done:
            text(d, (XS[0], yy), vn(h), 46, INK)
            text(d, (XS[1], yy), vn(tt, 3), 46, INK)
            text(d, (XS[2], yy), vn(L, 3), 46, INK)

# ---------------- canh 3: Dap an (cot v0 = L/t) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · gần như bằng nhau"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 330), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 296), lb, 40, WHITE, alpha=ka)
    y = 360
    card(d, (40, y, 1040, y + 520), fill=WHITE, outline=LIGHT, w=3)
    XS = (180, 410, 640, 880)
    text(d, (XS[0], y + 55), "h (m)", 42, PURPLE)
    text(d, (XS[1], y + 55), "t (s)", 42, TEAL)
    text(d, (XS[2], y + 55), "L đo (m)", 42, ORANGE)
    rx(d, XS[3], y + 55, "v_{0} = L/t", 42, BLUE)
    text(d, (XS[3], y + 108), "(m/s)", 36, BLUE, bold=False)
    d.line([(70, y + 140), (1010, y + 140)], fill=LIGHT, width=3)
    for i, (h, tt, L, v) in enumerate(ROWS):
        yy = y + 190 + i * 82
        text(d, (XS[0], yy), vn(h), 46, INK)
        text(d, (XS[1], yy), vn(tt, 3), 46, INK)
        text(d, (XS[2], yy), vn(L, 3), 46, INK)
        k = appear(t, M[0] + 1.8 + 0.35 * i, 0.35)
        if k > 0:
            d.rounded_rectangle([XS[3] - 95, yy - 34, XS[3] + 95, yy + 34], radius=14, fill=A((219, 234, 254), k))
            text(d, (XS[3], yy), vn(v), 48, BLUE, alpha=k)
    # phep tinh mau, du don vi
    k1 = appear(t, M[0] + 1.8, 0.5)
    card(d, (40, 910, 1040, 1100), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    text(d, (W / 2, 965), "Lần 1:", 40, INK, bold=False, alpha=k1)
    text(d, (W / 2, 1040), "0,451 m : 0,303 s ≈ 1,49 m/s", 46, BLUE, alpha=k1)
    k2 = appear(t, M[0] + 4.0, 0.5)
    card(d, (40, 1130, 1040, 1420), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
    text(d, (W / 2, 1215), "h đổi, L đổi", 48, GREEN, alpha=k2)
    rx(d, W / 2, 1320, "v_{0} chỉ lệch tới 0,02 m/s", 48, GREEN, alpha=k2)

# ---------------- canh 4: Rut ra (do thi L theo t) ----------------
GX0, GY0 = 230, 860            # goc do thi
GPX_T, GPX_L = 1200.0, 650.0   # px / s ; px / m
def GP(tt, L): return (GX0 + tt * GPX_T, GY0 - L * GPX_L)

def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1010), fill=WHITE, outline=LIGHT, w=3)
    text(d, (GX0 + 22, 300), "L (m)", 40, ORANGE, anchor="lm")
    d.line([GP(0, 0), GP(0.66, 0)], fill=INK, width=4); d.line([GP(0, 0), GP(0, 0.84)], fill=INK, width=4)
    for k in range(1, 4):                                                   # truc t: 0,2 0,4 0,6
        x, y = GP(k * 0.2, 0); d.line([(x, y - 12), (x, y + 12)], fill=INK, width=3)
        text(d, (x, y + 45), vn(k * 0.2, 1), 38, INK)
    text(d, (GP(0, 0)[0] - 20, GP(0, 0)[1] + 40), "0", 38, INK)
    text(d, (GP(0.66, 0)[0], GY0 - 40), "t (s)", 40, TEAL, anchor="rm")
    for k in range(1, 5):                                                   # truc L: 0,2 .. 0,8
        x, y = GP(0, k * 0.2); d.line([(x - 12, y), (x + 12, y)], fill=INK, width=3)
        text(d, (x - 24, y), vn(k * 0.2, 1), 38, INK, anchor="rm")
    kl = appear(t, M[0] + 0.6, 0.8)                                          # duong L = v0 t qua goc
    if kl > 0:
        te = 0.55 * kl
        d.line([GP(0, 0), GP(te, V0 * te)], fill=BLUE, width=5)
    for i, (h, tt, L, v) in enumerate(ROWS):
        k = appear(t, 0.3 + 0.2 * i, 0.35)
        if k <= 0: continue
        x, y = GP(tt, L); dot(d, x, y, 13, A(ORANGE, k), outline=NAVY)
    k8 = appear(t, 0.9, 0.35)                                                # hai lan h = 0,80 m gan trung nhau
    if k8 > 0:
        px, py = GP(0.404, 0.611)
        d.line([(640, 418), (px - 12, py - 10)], fill=A(INK, k8), width=3)
        text(d, (630, 400), "2 lần", 40, INK, anchor="rm", alpha=k8)
    kt = appear(t, M[0] + 1.4, 0.5)
    rx(d, 800, 640, "L = v_{0}·t", 46, BLUE, alpha=kt)
    rx(d, 800, 710, "v_{0} ≈ 1,50 m/s", 44, BLUE, alpha=kt)
    # chua noi duoc
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y0 = 1060 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 520), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 65), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        card(d, (80, y0 + 125, 1000, y0 + 470), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, y0 + 225), "Nòng chếch lên thì sao?", 48, RED, alpha=kk)
        text(d, (W / 2, y0 + 360), "mới thử nòng nằm ngang", 46, NAVY, alpha=kk)

# ---------------- canh 5: Bay (L ti le voi h?) ----------------
def s_bay(img, d, t, sc):
    base, sc_ = 770, 340.0                                                  # cung ti le px/m, hai khung rieng
    for (x0, x1, nm, col, vals, nd, lab) in ((40, 525, "h", PURPLE, (0.45, 1.25), 2, "độ cao h (m)"),
                                             (555, 1040, "L", ORANGE, (0.451, 0.757), 3, "tầm xa L (m)")):
        card(d, (x0, 265, x1, 860), fill=WHITE, outline=LIGHT, w=3)
        cx = (x0 + x1) / 2
        for k, v in enumerate(vals):
            x = cx - 85 + 170 * k; top = base - v * sc_
            d.rectangle([x - 50, top, x + 50, base], fill=col)
            text(d, (x, top - 34), vn(v, nd), 40, col)
        d.line([(x0 + 40, base), (x1 - 40, base)], fill=INK, width=4)
        text(d, (cx, base + 45), lab, 38, col)
    a1 = appear(t, 0.2, 0.45); y0 = 890
    card(d, (40, y0, 1040, y0 + 700), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 60), "BẪY", 38, WHITE, alpha=a1)
    q = "“L tỉ lệ với h”"
    ks = clamp((t - 1.0) / 0.4); f = F(54); lw = tw(d, q, f); yy = y0 + 200
    text(d, (W / 2, yy), q, 54, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 4), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 4)], fill=A(RED, 0.85 * a1), width=5)
    kk = a1 * appear(t, 1.5, 0.5)
    card(d, (90, y0 + 310, 990, y0 + 640), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, y0 + 410), "h × 2,8 → L chỉ × 1,7", 54, GREEN, alpha=kk)
    text(d, (W / 2, y0 + 530), "L tăng chậm hơn h", 52, GREEN, alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):                       # goi y trung tinh, hien tre ~3,7 s
        kh = appear(t, M[0] + 3.7, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Lấy g = 9,8 m/s²", 44, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Cùng súng: vận tốc ném không đổi,\nđộ cao chỉ đổi t và L",
             "Súng bắn ngang 1,50 m/s,\nđặt ở h = 0,60 m:\ntầm xa L bằng bao nhiêu?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for (s, mv), row in zip(SCHED, ROWS): cs.append((do["t0"] + s + mv + row[1] * SLOW, "tap"))   # bi cham giay
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-nemngang-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động ném · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ba độ cao, một súng", draw=s_hook, tail=0.8, caps=[
   ("Cùng một súng, ba độ cao.", 2.6),
   ("Dừng video, chọn câu trả lời.", 6.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Giấy than đánh dấu chỗ bi chạm.", 4.6),
   ("Đo tầm xa L trên thước cuộn.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Chia L cho t ở từng lần.", 5.6)]),
 dict(key="rutra", title="Vì sao?", draw=s_rutra, tail=0.6, caps=[
   ("Cùng súng, cùng vận tốc ném.", 3.4),
   ("Còn một điều chưa biết.", 3.6)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.5, caps=[
   ("So cột h với cột L.", 4.1)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.2, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])
