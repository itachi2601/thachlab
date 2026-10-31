# Clip: tn-l10-dong-nang-the-nang-01 - Khuc go truot sau cong quang (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dong-nang-the-nang-01.json:
#   so_lieu_mau: v = 1,00 / 1,50 / 2,00 / 2,50 m/s -> s = 0,21 / 0,44 / 0,82 / 1,22 m; s/v2 = 0,210 / 0,196 / 0,205 / 0,195
#   tham_so: mu = 0,25, g = 10 -> s = v2/5, s/v2 = 0,20 (mo_hinh); 0,82 : 0,21 ~ 3,9 (nhan xet trong bai).
# Canh: Du doan (K10: chi cau hoi + hinh, ten canh khong lo "v2") -> Tien hanh (4 lan, chieu cham 1,5 lan, dong ho so
#       dong pha voi tam chan sang, hang bang hien khi go dung) -> Dap an (thanh 0,21 vs 0,82 + cot s/v2) -> Vi sao
#       (cong ma sat am, dinh li dong nang) -> Bay (s ti le v: duong thang lech diem do) + Chua noi duoc -> Chot + cau hoi
#       (v = 1,25 m/s chua tung hien, giam mot nua -> phan xa "con mot nua" sai, dung: ~0,31 m).
# Lua chon Du doan (o khung web, khong ve trong mp4): A. Khoang gap 2 · B. Khoang gap 3 · C. Khoang gap 4 (dung)
#   · D. Khoang gap 8.
from engine import *

WOOD = (176, 124, 74); WOOD_D = (128, 86, 46); STEEL = (90, 98, 120); DRED = (185, 28, 28)
ROWS = [(1.00, 0.21, 0.210), (1.50, 0.44, 0.196), (2.00, 0.82, 0.205), (2.50, 1.22, 0.195)]   # so_lieu_mau
SLOW = 1.5                         # chieu cham 1,5 lan
XG, Y0, PXM = 200, 640, 560        # cong quang (x), mat ban (y), px moi met tren thuoc
APPROACH_PX = 110                  # tam chan sang di 110 px truoc khi toi cong
HOLD = 0.40                        # giay dung hinh sau moi lan (man)
_TI = {}
def TI(size):                      # Times Bold Italic cho mu
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chuoi co ky tu mu: phan 'μ' ve bang Times Bold Italic, con lai SF Bold."""
    parts = [p for p in re.split(r"(μ|_\{[^}]*\})", s) if p]
    fs = []
    for p in parts:
        if p == "μ": fs.append((p, TI(size * 1.08), 0))
        elif p.startswith("_{"): fs.append((p[2:-1], F(max(36, size * 0.62)), size * 0.26))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs); x = cx - tot / 2 if anchor == "m" else cx
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)

# ---------------- dong thoi gian chay thu (thoi gian man, tinh tu run0) ----------------
def runs():
    out = []; t = 0.0
    for i, (v, s, _) in enumerate(ROWS):
        ta = APPROACH_PX / (v * PXM) * SLOW           # di toi cong voi toc do v (dong deu)
        ts = 2 * s / v * SLOW                          # truot cham dan deu tu v toi 0 tren quang s
        out.append(dict(i=i, v=v, s=s, a0=t, g=t + ta, e=t + ta + ts, h=t + ta + ts + HOLD)); t += ta + ts + HOLD
    return out
RUNS = runs(); RUN_END = RUNS[-1]["h"]

def state(tr):
    """tr = giay man ke tu run0. Tra ve (lan, x tam chan sang theo met tu cong (am = truoc cong), da qua cong, da dung)."""
    if tr < 0: return 0, -APPROACH_PX / PXM, False, False
    for r in RUNS:
        if tr < r["h"] or r is RUNS[-1]:
            if tr < r["g"]:
                k = (tr - r["a0"]) / (r["g"] - r["a0"]); return r["i"], -APPROACH_PX / PXM * (1 - k), False, False
            if tr < r["e"]:
                k = (tr - r["g"]) / (r["e"] - r["g"]); return r["i"], r["s"] * (1 - (1 - k) ** 2), True, False
            return r["i"], r["s"], True, True

def rig(d, xm, shown_v=None, q=False, done_s=None, a=1.0):
    """Ban + cong quang + khuc go + thuoc. xm: vi tri tam chan sang (m tu cong)."""
    c = lambda col: A(col, a)
    d.rectangle([40, Y0, 1040, Y0 + 34], fill=c(WOOD), outline=c(WOOD_D), width=3)
    # thuoc 0..1,4 m duoi mat ban
    ry = Y0 + 34
    d.rectangle([XG, ry, XG + 1.4 * PXM, ry + 46], fill=c((253, 246, 200)), outline=c((170, 150, 60)), width=2)
    for k in range(29):
        x = XG + k * 0.05 * PXM; L = 30 if k % 4 == 0 else (18 if k % 2 == 0 else 10)
        d.line([(x, ry), (x, ry + L)], fill=c(NAVY), width=3 if L == 30 else 2)
    for k in range(8):
        text(d, (XG + k * 0.2 * PXM, ry + 84), vn(k * 0.2, 1) if k else "0", 40, INK, alpha=a)
    text(d, (XG - 70, ry + 84), "m", 40, INK, alpha=a)
    # khuc go: tam chan sang o giua khuc go
    bx = XG + xm * PXM; bw, bh = 96, 70
    d.rectangle([bx - bw / 2, Y0 - bh, bx + bw / 2, Y0], fill=c(WOOD), outline=c(WOOD_D), width=4)
    d.rectangle([bx - 6, Y0 - bh - 64, bx + 6, Y0 - bh], fill=c(NAVY))           # tam chan sang
    # cong quang: chu U nguoc, tia sang ngang qua tam chan
    gy0, gy1 = Y0 - 190, Y0
    d.rectangle([XG - 46, gy0, XG - 32, gy1], fill=c(RED)); d.rectangle([XG + 32, gy0, XG + 46, gy1], fill=c(RED))
    d.rectangle([XG - 46, gy0 - 16, XG + 46, gy0], fill=c(RED))
    by = Y0 - bh - 34
    for xx in range(int(XG - 30), int(XG + 30), 14):
        d.line([(xx, by), (xx + 7, by)], fill=c(ORANGE), width=4)
    # dong ho so (noi cong quang)
    d.line([(XG, gy0 - 16), (XG, gy0 - 40)], fill=c(STEEL), width=4)
    bxx = (XG - 150, gy0 - 130, XG + 300, gy0 - 40)
    card(d, bxx, fill=c(NAVY), r=18)
    if q: txt, col = "v = ?", YELLOW
    elif shown_v is None: txt, col = "v = –,–– m/s", GRAY
    else: txt, col = f"v = {vn(shown_v)} m/s", YELLOW
    text(d, ((bxx[0] + bxx[2]) / 2, (bxx[1] + bxx[3]) / 2), txt, 46, col, alpha=a)
    text(d, (bxx[2] + 16, (bxx[1] + bxx[3]) / 2), "cổng quang", 40, MUTED, anchor="lm", alpha=a)
    if done_s is not None:                                                   # mui ten do s tu cong toi tam chan
        ya = Y0 + 165
        x1 = bx
        if x1 - XG > 40:
            d.line([(XG, ya), (x1, ya)], fill=c(GREEN), width=4)
            for xe, sg in ((XG, 1), (x1, -1)):
                d.line([(xe, ya), (xe + sg * 16, ya - 10)], fill=c(GREEN), width=4)
                d.line([(xe, ya), (xe + sg * 16, ya + 10)], fill=c(GREEN), width=4)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 940), fill=WHITE, outline=LIGHT, w=3)
    rig(d, -APPROACH_PX / PXM, q=True)
    text(d, (W / 2, 880), "Cùng khúc gỗ, cùng mặt bàn", 42, INK)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 980 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 180, "Tốc độ qua cổng tăng từ 1,00 lên 2,00 m/s.", 46, NAVY, maxw=880, alpha=a)
    ctext(d, y0 + 340, "Quãng trượt s dài gấp mấy lần?", 50, INK, maxw=880, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 510, 940, y0 + 524], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 510, 140 + 800 * (1 - p), y0 + 524], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
RUN0 = 0.7
def table(d, nrow, hi=-1, y=960):
    card(d, (40, y, 1040, y + 600), fill=WHITE, outline=NAVY, w=4)
    xs = (210, 540, 860)
    for x, s in zip(xs, ("Lần", "v (m/s)", "s (m)")): text(d, (x, y + 55), s, 42, INK)
    d.line([(80, y + 100), (1000, y + 100)], fill=LIGHT, width=4)
    for i in range(4):
        yy = y + 160 + i * 105
        if i == hi: d.rounded_rectangle([70, yy - 44, 1010, yy + 44], radius=18, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(i + 1), 44, INK)
        if i < nrow:
            text(d, (xs[1], yy), vn(ROWS[i][0]), 46, BLUE); text(d, (xs[2], yy), vn(ROWS[i][1]), 46, GREEN)

def do_state(t):
    tr = t - RUN0
    i, xm, passed, stopped = state(tr)
    return i, xm, passed, stopped

def s_do(img, d, t, sc):
    i, xm, passed, stopped = do_state(t)
    card(d, (40, 265, 1040, 920), fill=WHITE, outline=LIGHT, w=3)
    rig(d, xm, shown_v=ROWS[i][0] if passed else None, done_s=ROWS[i][1] if stopped else None)
    if stopped:
        text(d, (W / 2, 870), f"s = {vn(ROWS[i][1])} m", 46, GREEN)
    nrow = i + (1 if stopped else 0)
    table(d, nrow, hi=i if stopped else -1)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lab = "ĐÁP ÁN · gần gấp bốn"
    pw = tw(d, lab, F(40)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 330), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 296), lab, 40, WHITE, alpha=ka)
    card(d, (40, 360, 1040, 860), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    S = 900                                           # px/m cho thanh so sanh
    x0 = 300
    text(d, (80, 450), "1,00 m/s", 40, BLUE, anchor="lm", alpha=ka)
    d.rectangle([x0, 425, x0 + 0.21 * S, 475], fill=A(GREEN, ka))
    text(d, (x0 + 0.21 * S + 16, 450), "0,21 m", 40, GREEN, anchor="lm", alpha=ka)
    kb = appear(t, 0.3, 0.4)
    text(d, (80, 570), "2,00 m/s", 40, BLUE, anchor="lm", alpha=kb)
    d.rectangle([x0, 545, x0 + 0.82 * S * kb, 595], fill=A(GREEN, kb))
    text(d, (x0 + 0.82 * S - 10, 635), "0,82 m", 40, GREEN, anchor="rm", alpha=kb)
    kc = appear(t, 0.7, 0.4)                          # bon doan 0,21 m dat duoi thanh 2,00 m/s
    for j in range(4):
        xa = x0 + j * 0.21 * S
        d.rectangle([xa + 2, 680, xa + 0.21 * S - 2, 712], outline=A(ORANGE, kc), width=4)
    text(d, (W / 2, 790), "0,82 : 0,21 ≈ 3,9", 46, ORANGE, alpha=appear(t, 1.0, 0.4))
    # bang s/v2 (hien truoc phu de 2)
    y = 890
    kt = appear(t, M[1] - 0.1, 0.4)
    if kt <= 0: return
    card(d, (40, y, 1040, y + 700), fill=A(WHITE, kt), outline=A(NAVY, kt), w=4)
    xs = (230, 520, 820)
    for x, s in zip(xs, ("v (m/s)", "s (m)", "s/v² (s²/m)")): text(d, (x, y + 55), s, 40, INK, alpha=kt)
    d.line([(80, y + 100), (1000, y + 100)], fill=A(LIGHT, kt), width=4)
    for j, (v, s, r) in enumerate(ROWS):
        k = appear(t, M[1] - 0.1 + 0.2 * j, 0.35); yy = y + 160 + j * 100
        text(d, (xs[0], yy), vn(v), 44, BLUE, alpha=k); text(d, (xs[1], yy), vn(s), 44, GREEN, alpha=k)
        text(d, (xs[2], yy), vn(r, 3), 46, ORANGE, alpha=k)
    kk = appear(t, M[1] + 0.9, 0.4)
    d.rounded_rectangle([640, y + 570, 1000, y + 660], radius=22, fill=A((255, 237, 213), kk))
    text(d, (820, y + 615), "≈ 0,20", 48, ORANGE, alpha=kk)

# ---------------- canh 4: Vi sao ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([60, 600, 1020, 634], fill=WOOD, outline=WOOD_D, width=3)
    bx = 520
    d.rectangle([bx - 70, 500, bx + 70, 600], fill=WOOD, outline=WOOD_D, width=4)
    arrow(d, (bx + 80, 450), (bx + 300, 450), BLUE, w=7)                        # van toc sang phai
    text(d, (bx + 330, 450), "v", 46, BLUE, anchor="lm")
    k1 = appear(t, M[0] - 0.1, 0.4)
    if k1 > 0:                                                                 # ma sat nguoc chieu chuyen dong, o mat tiep xuc
        arrow(d, (bx - 10, 600), (bx - 230, 600), A(RED, k1), w=8)
        rich(d, bx - 300, 545, "F_{ms}", 46, RED, alpha=k1)
        text(d, (W / 2, 700), "ngược chiều chuyển động", 40, RED, alpha=k1)
    card(d, (40, 780, 1040, 1595), fill=WHITE, outline=NAVY, w=5)
    eq(d, W / 2, 840, "F_{ms} = μmg  →  A_{ms} = −μmg·s", 46, INK, alpha=appear(t, M[0] + 0.5, 0.45))
    k2 = appear(t, M[1] - 0.2, 0.45)
    text(d, (W / 2, 920), "Định lí động năng", 42, MUTED, alpha=k2)
    eq(d, W / 2, 990, "W_{đ sau} − W_{đ đầu} = A_{ms}", 48, INK, alpha=k2)
    k2b = appear(t, M[1] + 0.8, 0.45)
    eq(d, W / 2, 1075, "0 − ½mv² = −μmg·s", 52, INK, alpha=k2b)
    k3 = appear(t, M[1] + 1.8, 0.45)
    if k3 > 0:
        arrow(d, (W / 2, 1120), (W / 2, 1170), A(MUTED, k3), w=6, head=16)
        text(d, (W / 2 + 30, 1145), "m triệt tiêu", 42, ORANGE, anchor="lm", alpha=k3)
        card(d, (190, 1185, 890, 1305), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        eq(d, W / 2, 1245, "s = v² / (2μg)", 58, GREEN, alpha=k3)
    k4 = appear(t, M[1] + 2.6, 0.45)
    eq(d, W / 2, 1390, "μ = 0,25 ;  g = 10 m/s²", 44, INK, alpha=k4)
    text(d, (W / 2, 1490), "s/v² = 1/(2·0,25·10) = 0,20", 44, ORANGE, alpha=k4)

# ---------------- canh 5: Bay + chua noi duoc ----------------
GX0, GY0, GX1, GY1 = 220, 1460, 960, 720          # do thi s theo v: v 0..2,5 ; s 0..1,4
def gx(v): return GX0 + v / 2.5 * (GX1 - GX0)
def gy(s): return GY0 - s / 1.4 * (GY0 - GY1)

def graph(d, a, kd):
    c = lambda col: A(col, a)
    d.line([(GX0, GY0), (GX1 + 20, GY0)], fill=c(INK), width=4); d.line([(GX0, GY0), (GX0, GY1 - 20)], fill=c(INK), width=4)
    for v in (0.5, 1.0, 1.5, 2.0, 2.5):
        d.line([(gx(v), GY0), (gx(v), GY0 + 12)], fill=c(INK), width=3)
        text(d, (gx(v), GY0 + 44), vn(v, 1), 40, INK, alpha=a)
    for s in (0.4, 0.8, 1.2):
        d.line([(GX0 - 12, gy(s)), (GX0, gy(s))], fill=c(INK), width=3)
        text(d, (GX0 - 20, gy(s)), vn(s, 1), 40, INK, anchor="rm", alpha=a)
    text(d, (GX0 - 20, GY0 + 44), "0", 40, INK, anchor="rm", alpha=a)
    text(d, (1010, GY0 + 92), "v (m/s)", 40, INK, anchor="rm", alpha=a)
    text(d, (GX0 - 20, GY1 - 10), "s (m)", 40, INK, anchor="rm", alpha=a)
    # duong s ti le v (bay): qua goc va diem lan 1, net dut do
    pts = [(gx(v), gy(0.21 * v)) for v in np.linspace(0, 2.5, 26)]
    for j in range(0, len(pts) - 1, 2):
        d.line([pts[j], pts[j + 1]], fill=A(RED, a * kd), width=6)
    # duong cong s = v2/5
    kc = appear_k = kd
    cur = [(gx(v), gy(v * v / 5)) for v in np.linspace(0, 2.5, 60)]
    d.line(cur, fill=A(GREEN, a * kc), width=6, joint="curve")
    for v, s, _ in ROWS:
        dot(d, gx(v), gy(s), 16, A(BLUE, a))
    # chu giai
    d.line([(250, 640), (310, 640)], fill=A(GREEN, a * kc), width=6)
    text(d, (325, 640), "s tỉ lệ v²", 42, GREEN, anchor="lm", alpha=a * kc)
    for xx in (600, 630):
        d.line([(xx, 640), (xx + 18, 640)], fill=A(RED, a * kd), width=6)
    text(d, (665, 640), "s tỉ lệ v", 42, RED, anchor="lm", alpha=a * kd)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[2] - 0.1, 0.45)
    a = appear(t, 0.1, 0.4) * (1 - k3)
    if a > 0:
        card(d, (40, 265, 1040, 1600), fill=A(WHITE, a), outline=A(DRED, a), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 352), fill=A(DRED, a), r=31)
        text(d, (W / 2, 321), "BẪY", 38, WHITE, alpha=a)
        q = "“v gấp đôi thì s gấp đôi”"
        yy = 440; lw = tw(d, q, F(52))
        text(d, (W / 2, yy), q, 52, INK, alpha=a)
        ks = clamp((t - 1.0) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a), width=6)
        ctext(d, 545, "Nhầm với chuyển động đều (s tỉ lệ v)", 42, DRED, maxw=900, alpha=a * appear(t, 1.4, 0.4))
        graph(d, a, appear(t, M[1] - 0.2, 0.5))
    if k3 > 0:
        y1 = 720 + (1 - k3) * 30
        card(d, (40, y1, 1040, y1 + 420), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 70), "Chưa nói được gì?", 48, NAVY, alpha=k3)
        items = ("• m triệt tiêu, nhưng chưa đo kiểm", "• Chỉ một mặt bàn, một μ")
        for j, s in enumerate(items):
            kk = k3 * appear(t, M[2] + 0.3 + 0.5 * j, 0.4)
            eq(d, 100, y1 + 195 + j * 120, s, 46, INK, alpha=kk, anchor="l")

# ---------------- canh 6: Chot + cau hoi ----------------
def s_end(img, d, t, sc):                   # nhu chot_hoi cua engine, hop cam thu vua noi dung
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, "Quãng trượt tỉ lệ với v²", 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1290), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 830, "Qua cổng 1,25 m/s, khúc gỗ trượt khoảng bao xa?", 46, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.5, 0.5)                                        # goi y tre 2,5 s
    if kh <= 0: return
    card(d, (110, 990, 970, 1240), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1050, "Gợi ý", 40, INK, alpha=kh)
    ctext(d, 1145, "Không phải 0,61 m", 46, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = (sc[k] for k in ("hook", "do", "dapan", "rutra", "bay", "end"))
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + RUN0 + R["g"], "tap") for R in RUNS]                  # tam chan sang cat tia sang
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 1.8, "tap"),
            (b["t0"] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l10-dong-nang-the-nang-01", header="VẬT LÍ 10 · THÍ NGHIỆM",
            footer="Động năng, thế năng · thachlab.id.vn", cues=_cues, scenes=[
 dict(key="hook", title="Khúc gỗ qua cổng quang", draw=s_hook, tail=0.7, caps=[
   ("Đẩy gỗ, buông trước cổng.", 2.5),
   ("Dừng video, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=max(0.5, RUN0 + RUN_END + 0.3 - 0.4 - cap_dur("Bốn lần, bốn tốc độ.") - cap_dur("Đo s từ cổng tới chỗ dừng.")), caps=[
   ("Bốn lần, bốn tốc độ.", 2.5),
   ("Đo s từ cổng tới chỗ dừng.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So lần 1,00 và 2,00 m/s.", 3.3),
   ("Cột s/v² gần như không đổi.", 3.4)]),
 dict(key="rutra", title="Vì sao như vậy?", draw=s_rutra, tail=0.6, caps=[
   ("Ma sát sinh công âm.", 2.8),
   ("Động năng về 0 thì dừng.", 3.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy hay gặp.", 2.5),
   ("Điểm đo nằm trên đường cong.", 3.0),
   ("Giới hạn của thí nghiệm.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự tính.", 5.2)]),
])
