# Clip: tn-l10-dongluong-02 - Bi lan tu mang nghieng va vao khuc go (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dongluong-02.json:
#   so_lieu_mau m (kg) / h (m) / v (m/s) / p (kg.m/s): 0,05/0,1/1,18/0,059 ; 0,05/0,2/1,67/0,084 ;
#   0,1/0,1/1,18/0,118 ; 0,1/0,2/1,67/0,167.  tham_so: m 0,02-0,2 kg, h 0,05-0,3 m.
#   Quang go di: kho chi dinh tinh (khong co so) -> ve tang theo p, KHONG ghi so, khong thuoc do.
# Canh: Du doan (50 g tha 20 cm hay 100 g tha 10 cm, K10: chi cau hoi + hinh) -> Tien hanh (4 lan tha, bang so
#       lieu dien dung luc bi toi chan mang) -> Rut ra (p = m.v) -> Chua noi duoc gi -> Bay (nang gap doi lan nhanh
#       gap doi?) -> Chot + cau hoi tu nho lai (200 g tha 5 cm vs 50 g tha 30 cm: bien tham_so, chua hien tren man).
# Khac dongluong1 (xe + dem lo xo): truc chinh la mang nghieng + bi + khuc go, so sanh theo m va h.
from engine import *

ROWS = [("0,05", "0,1", "1,18", "0,059"), ("0,05", "0,2", "1,67", "0,084"),
        ("0,1", "0,1", "1,18", "0,118"), ("0,1", "0,2", "1,67", "0,167")]          # so_lieu_mau
RUNS = [(50, 10, 0.059), (50, 20, 0.084), (100, 10, 0.118), (100, 20, 0.167)]       # (g, cm, p)
DRED = (185, 28, 28)
WOOD = (222, 184, 135); WOOD_D = (150, 105, 60)
RAMP = (226, 232, 240); RAMP_D = (100, 116, 139)
STEEL = (148, 163, 184); STEEL_D = (71, 85, 105)

# ---------- hinh hoc mang (toa do cuc bo, chan mang o (0,0), y huong xuong) ----------
TOPX, TOPY = -480, -340
SL = math.hypot(TOPX, TOPY); UX, UY = -TOPX / SL, -TOPY / SL      # huong xuong doc (0,816; 0,578)
NX, NY = UY, -UX                                                  # phap tuyen huong len (0,578; -0,816)
PXCM = 15                                                         # 1 cm do cao = 15 px
XB, BW, BH = 60, 130, 110                                          # mep trai khuc go, rong, cao
ACC = 1038.0                                                      # gia toc doc mang (px/s2): tha 20 cm mat ~1 s
DMAX = 280                                                        # quang go di khi p = 0,167 (lon nhat)
SLIDE = 0.9
def rad(g): return 22 if g == 50 else 28                          # bi thep: r ti le can bac 3 cua m
def dist(p): return DMAX * p / 0.167

def surf(hcm):  # diem tren mat mang o do cao hcm
    hp = hcm * PXCM; return (TOPX * hp / -TOPY, -hp)

def ball_path(hcm, r, tau):
    """Tra ve (x, y, da_va_cham, thoi_diem_va_cham) cua tam bi, tau giay sau khi tha."""
    sx, sy = surf(hcm); x0, y0 = sx + r * NX, sy + r * NY
    L = (-r - y0) / UY                                            # quang doc mang toi khi tam o y = -r
    t1 = math.sqrt(2 * L / ACC); v1 = ACC * t1
    x1 = x0 + L * UX; Lh = (XB - r) - x1; t2 = Lh / v1; ti = t1 + t2
    if tau <= 0: return x0, y0, False, ti
    if tau < t1:
        s = 0.5 * ACC * tau * tau; return x0 + s * UX, y0 + s * UY, False, ti
    if tau < ti: return x1 + v1 * (tau - t1), -r, False, ti
    return XB - r, -r, True, ti

def slide(tau_after, D):  # quang go da di, giam dan deu toi D
    u = clamp(tau_after / SLIDE); return D * (1 - (1 - u) ** 2)

def P(O, s, x, y): return (O[0] + x * s, O[1] + y * s)

def rig(d, O, s, marks=(10, 20), floor_r=540, alpha=1.0, block_dx=None, lbl=36, loff=70):
    c = lambda col: A(col, alpha)
    tri = [P(O, s, TOPX, TOPY), P(O, s, 0, 0), P(O, s, TOPX, 0)]
    d.polygon(tri, fill=c(RAMP)); d.line(tri + [tri[0]], fill=c(RAMP_D), width=max(3, int(5 * s)))
    d.line([P(O, s, TOPX - 20, 0), P(O, s, floor_r, 0)], fill=c(NAVY), width=max(4, int(6 * s)))
    for hcm in marks:                                             # vach do cao tren mat mang
        sx, sy = surf(hcm)
        d.line([P(O, s, sx, sy), P(O, s, sx - 26 * NX, sy - 26 * NY)], fill=c(NAVY), width=4)
        lx, ly = P(O, s, sx + loff / s * NX - 20, sy + loff / s * NY)
        text(d, (lx, ly), f"{hcm} cm", lbl, NAVY, alpha=alpha)
    if block_dx is not None:
        x0 = XB + block_dx
        d.rectangle([P(O, s, x0, -BH), P(O, s, x0 + BW, 0)], fill=c(WOOD), outline=c(WOOD_D), width=max(3, int(4 * s)))
        for k in (1, 2):
            yy = -BH * k / 3
            d.line([P(O, s, x0 + 10, yy), P(O, s, x0 + BW - 10, yy)], fill=c(WOOD_D), width=2)

def ball(d, O, s, x, y, r, alpha=1.0):
    cx, cy = P(O, s, x, y); R = r * s
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A(STEEL, alpha), outline=A(NAVY, alpha), width=4)
    d.ellipse([cx - R * 0.55, cy - R * 0.6, cx - R * 0.1, cy - R * 0.15], fill=A(WHITE, alpha * 0.8))

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; s = 0.62
    for i, (g, hcm, O) in enumerate(((50, 20, (500, 520)), (100, 10, (500, 820)))):
        k = appear(t, 0.2 + 0.4 * i)
        if k <= 0: continue
        rig(d, O, s, marks=(hcm,), floor_r=520, alpha=k, block_dx=0, loff=112)
        r = rad(g) * 1.5; sx, sy = surf(hcm)                     # phong to bi o hinh nho cho de thay
        ball(d, O, s, sx + r * NX, sy + r * NY, r, alpha=k)
        text(d, (O[0] + 260, O[1] - 175), f"Bi {g} g", 42, INK, alpha=k)
        text(d, (O[0] + 260, O[1] - 120), f"thả từ {hcm} cm", 40, INK, alpha=k)
    text(d, (W / 2, 905), "Khúc gỗ nặng hơn bi nhiều", 40, MUTED, alpha=appear(t, 1.0))
    k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 960 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 175, "Lần thả nào đẩy khúc gỗ", 46, INK, alpha=k)
    ctext(d, y0 + 240, "đi xa hơn?", 46, INK, alpha=k)
    card(d, (W / 2 - 80, y0 + 300, W / 2 + 80, y0 + 450), fill=A((245, 243, 255), k), outline=A(PURPLE, k), r=26, w=4)
    text(d, (W / 2, y0 + 375), "?", 90, PURPLE, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 500, 880, y0 + 516], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 500, 200 + 680 * (1 - q), y0 + 516], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh (4 lan tha) ----------------
OD = (560, 800)
R0, RGAP = 0.8, 2.1
BADGE = 9.2
XS = (130, 300, 480, 670, 880)

def run_state(i, t):
    """Trang thai lan tha i luc t (giay trong canh): (bi x, y, r, go_dx, da_toi_chan, da_dung)."""
    g, hcm, p = RUNS[i]; r = rad(g); tau = t - (R0 + RGAP * i)
    x, y, hit, ti = ball_path(hcm, r, tau)
    gd = slide(tau - ti, dist(p)) if hit else 0.0
    if hit: x += 0.25 * gd
    return x, y, r, gd, hit, tau >= ti + SLIDE

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; s = 1.0
    cur = max(0, min(3, int((t - R0) // RGAP))) if t >= R0 else 0
    x, y, r, gd, hit, done = run_state(cur, t)
    rig(d, OD, s, floor_r=500, block_dx=gd)
    ka = appear(t, BADGE, 0.4)
    for i in range(4):                                            # vach noi go dung cua cac lan da xong
        if not run_state(i, t)[5]: continue
        X = OD[0] + XB + dist(RUNS[i][2])
        col = ORANGE if (ka > 0.5 and i in (1, 2)) else INK
        d.line([(X, OD[1] + 6), (X, OD[1] + 34)], fill=col, width=5)
        text(d, (X, OD[1] + 64), str(i + 1), 36, col)
    ball(d, OD, s, x, y, r)
    # bang so lieu: m, h hien luc tha; v, p hien dung luc bi toi khuc go
    card(d, (60, 905, 1020, 1250), fill=WHITE, outline=NAVY, w=4)
    for xx, hd in zip(XS, ("Lần", "m (kg)", "h (m)", "v (m/s)", "p (kg·m/s)")): text(d, (xx, 950), hd, 36, INK)
    d.line([(90, 982), (990, 982)], fill=LIGHT, width=4)
    for i, row in enumerate(ROWS):
        tau = t - (R0 + RGAP * i)
        if tau < 0: continue
        yy = 1022 + i * 60
        hit_i = run_state(i, t)[4]
        if ka > 0 and i in (1, 2):
            d.rounded_rectangle([80, yy - 28, 1000, yy + 28], radius=14, fill=A((255, 237, 213), ka))
        elif i == cur and not run_state(i, t)[5]:
            d.rounded_rectangle([80, yy - 28, 1000, yy + 28], radius=14, fill=(239, 246, 255))
        text(d, (XS[0], yy), str(i + 1), 40, MUTED)
        text(d, (XS[1], yy), row[0], 40, NAVY); text(d, (XS[2], yy), row[1], 40, NAVY)
        if hit_i:
            text(d, (XS[3], yy), row[2], 40, BLUE); text(d, (XS[4], yy), row[3], 40, BLUE)
    if ka > 0:
        s_ = "ĐÁP ÁN · Bi 100 g thả 10 cm"; pw = tw(d, s_, F(44)) + 70
        card(d, (W / 2 - pw / 2, 1290, W / 2 + pw / 2, 1390), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=26, w=4)
        text(d, (W / 2, 1340), s_, 44, GREEN, alpha=ka)
        text(d, (W / 2, 1455), "Lần 3 xa hơn lần 2", 46, (154, 52, 18), alpha=appear(t, BADGE + 0.3))

# ---------------- canh 3: rut ra ----------------
def s_rutra(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 270, 1020, 440), fill=A((239, 246, 255), a), r=30)
    text(d, (W / 2, 325), "p = m · v", 64, BLUE, alpha=a)
    text(d, (W / 2, 400), "khả năng truyền chuyển động", 40, INK, alpha=a)
    k1 = appear(t, M[0] - 0.05, 0.4)
    if k1 > 0:
        card(d, (60, 470, 1020, 880), fill=A(WHITE, k1), outline=A(NAVY, k1), w=4)
        text(d, (W / 2, 520), "Cùng h = 10 cm", 42, MUTED, alpha=k1)
        for cx, g in ((330, 50), (750, 100)):
            R = rad(g) * 1.6
            d.ellipse([cx - R, 640 - R, cx + R, 640 + R], fill=A(STEEL, k1), outline=A(NAVY, k1), width=4)
            text(d, (cx, 725), f"{g} g", 42, INK, alpha=k1)
        arrow(d, (440, 640), (630, 640), A(NAVY, k1), w=6)
        text(d, (W / 2, 820), "p: 0,059 → 0,118", 52, BLUE, alpha=k1)
    k2 = appear(t, M[1] - 0.05, 0.4)
    if k2 > 0:
        card(d, (60, 910, 1020, 1330), fill=A(WHITE, k2), outline=A(NAVY, k2), w=4)
        text(d, (W / 2, 960), "Cùng m = 50 g", 42, MUTED, alpha=k2)
        text(d, (W / 2, 1050), "h: 10 cm → 20 cm", 50, NAVY, alpha=k2)
        text(d, (W / 2, 1150), "v: 1,18 → 1,67 m/s", 52, BLUE, alpha=k2)
        text(d, (W / 2, 1250), "v chỉ tăng ≈ 1,41 lần", 46, NAVY, alpha=k2)
    k3 = appear(t, M[1] + 1.4, 0.4)
    if k3 > 0:
        card(d, (60, 1370, 1020, 1510), fill=A((255, 247, 237), k3), outline=A(ORANGE, k3), r=26, w=4)
        text(d, (W / 2, 1440), "Lần 2, 3: cùng động năng, khác p", 44, (154, 52, 18), alpha=k3)

# ---------------- canh 4: chua noi duoc gi ----------------
def s_gioihan(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.05, 0.35); y1 = 290
    card(d, (60, y1, 1020, y1 + 1150), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, y1 + 85), "Chưa nói được gì?", 54, NAVY, alpha=k)
    card(d, (110, y1 + 170, 970, y1 + 600), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 330, "Quãng gỗ đi tỉ lệ", 50, BLUE, alpha=k)
    ctext(d, y1 + 440, "thế nào với p?", 50, BLUE, alpha=k)
    ctext(d, y1 + 1050, "Coi gỗ nặng hơn bi nhiều", 44, INK, alpha=k)
    O = (W / 2 - 300, y1 + 820); s = 1.0                            # khuc go + mui ten quang di co dau hoi
    d.line([(O[0] - 60, O[1]), (O[0] + 620, O[1])], fill=A(NAVY, k), width=6)
    d.rectangle([O[0], O[1] - BH, O[0] + BW, O[1]], fill=A(WOOD, k), outline=A(WOOD_D, k), width=4)
    gx = O[0] + 420
    d.rectangle([gx, O[1] - BH, gx + BW, O[1]], outline=A(GRAY, k), width=4)
    arrow(d, (O[0] + BW + 10, O[1] - 40), (gx - 12, O[1] - 40), A(NAVY, k), w=5)
    text(d, ((O[0] + BW + gx) / 2, O[1] - 110), "?", 80, PURPLE, alpha=k)

# ---------------- canh 5: bay ----------------
BT0 = 1.3
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 270, 1020, 650), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 364), fill=A(DRED, a), r=32)
    text(d, (W / 2, 332), "Bẫy", 40, WHITE, alpha=a)
    q = "Nặng gấp đôi → nhanh gấp đôi"; f = F(52); lw = tw(d, q, f); yy = 500
    text(d, (W / 2, yy), q, 52, DRED, alpha=a)
    ks = clamp((t - 0.9) / 0.4)
    if ks > 0: d.line([(W / 2 - lw / 2 - 10, yy + 2), (W / 2 - lw / 2 - 10 + (lw + 20) * ks, yy + 2)], fill=DRED, width=7)
    card(d, (60, 690, 1020, 1600), fill=WHITE, outline=GREEN, w=5)
    s = 0.6
    for g, O in ((50, (480, 1060)), (100, (480, 1460))):
        r = rad(g); rig(d, O, s, marks=(10,), floor_r=860)
        sx, sy = surf(10); x0, y0 = sx + r * NX, sy + r * NY
        L = (-r - y0) / UY; t1 = math.sqrt(2 * L / ACC); v1 = ACC * t1
        tau = t - BT0
        if tau <= 0: x, y = x0, y0
        elif tau < t1: sd = 0.5 * ACC * tau * tau; x, y = x0 + sd * UX, y0 + sd * UY
        else: x, y = min(x0 + L * UX + v1 * (tau - t1), 520), -r
        ball(d, O, s, x, y, r)
        text(d, (O[0] + 300, O[1] - 190), f"Bi {g} g", 42, INK)
        if tau >= t1:
            text(d, (O[0] + 300, O[1] - 120), "v = 1,18 m/s", 42, GREEN, alpha=appear(t, BT0 + t1, 0.3))

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def hint(d, t, k):
        ctext(d, 900, "Bi 200 g thả 5 cm, bi 50 g\nthả 30 cm: p bi nào lớn hơn?", 52, INK,
              maxw=880, alpha=appear(t, sc["M"][0] + 0.4, 0.5))
        kh = appear(t, sc["M"][0] + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 1230, 970, 1530), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=3)
        ctext(d, 1300, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1420, "Đừng chỉ so độ cao", 48, (154, 52, 18), maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Gỗ đi xa hơn khi p lớn hơn", "", body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + BADGE, "ding"), (b["t0"] + 0.9, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-dongluong-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Động lượng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bi lăn va khúc gỗ", draw=s_hook, tail=0.5, caps=[
   ("Cùng khúc gỗ, hai cách thả.", 3.4),
   ("Dừng video, tự đoán.", 5.2)]),
 dict(key="do", title="Thả bốn lần", draw=s_do, tail=0.5, caps=[
   ("Mỗi lần thả, gỗ đặt lại chỗ cũ.", 6.4),
   ("So vạch dừng lần 2, lần 3.", 4.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Nặng gấp đôi: p gấp đôi.", 3.0),
   ("Cao gấp đôi: v chưa gấp đôi.", 3.8)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Giới hạn của thí nghiệm.", 4.8)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Hai bi tới chân máng cùng lúc.", 3.2),
   ("Cùng độ cao, cùng v, dù nặng nhẹ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 6.2)]),
])
