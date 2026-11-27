# Clip: tn-l10-thuchanhthl-01 - Ba luc ke keo nut O: so F ve (hinh binh hanh) voi luc do duoc (ban 2 cong moi, 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-thuchanhthl-01.json (_kiem_so() doi chieu so_lieu_mau):
#   lan 1: F1 1,6 ; F2 2,1 ; alpha 80 ; F3 2,9 N (cheo 5,7 cm -> F ve 2,85 N, delta 0,05) | lan 2: 2,0 ; 2,0 ; 60 ; 3,5 N
#   lan 3: 1,4 ; 1,6 ; 110 ; F3 doc 2,1 N gom so 0 lech 0,3 N -> 1,8 N ; F ve 1,75 N ; delta 0,35 -> 0,05.
#   ti le xich 1 cm ung 0,5 N ; Delta = 0,3 N ; luc ke 5 N. Huong day: tinh tu mo hinh (nut O can bang, F3 thang dung).
# Du doan (K10, khong nut; v2 theo kiem-code 27/11) = hien_tuong_hay_sai[3]: F (tong hop F1, F2) huong the nao so voi
#   luc keo cua luc ke 3? (dap an: nguoc chieu). Bang trong bai khong co huong; ban 1 hoi do lon -> bang __BANG_A1__ lo.
# Bay = hien_tuong_hay_sai[2]: lan 3 delta = 0,35 N > Delta -> "quy tac sai"; thao vat, luc ke 3 chi 0,3 N.
# Chot (v2): F1 = 0,9 N, F2 = 1,2 N, hai day vuong goc -> 1,5 N (3-4-5; khong so nao trung bang; cong thang 2,1 N la
#   dap an nhieu). Ca nay chua co trong ghi_chu kho (phien chinh sua). So 1,5 khong hien o canh end.
from engine import *

DRED = (185, 28, 28); NOTE = (60, 64, 84); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
BRASS = (196, 150, 70); BRASS_D = (140, 100, 40); PAPER = (250, 250, 245)
LAN = [(1.6, 2.1, 80, 2.9), (2.0, 2.0, 60, 3.5), (1.4, 1.6, 110, 2.1)]       # so_lieu_mau (F1, F2, alpha, F3 doc)
CHEO, FVE = (5.7, 6.9, 3.5), (2.85, 3.45, 1.75)
XICH, DELTA, SO0 = 0.5, 0.3, 0.3
_GK = "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf"; _gc = {}
def FG(size):
    size = int(size)
    if size not in _gc: _gc[size] = ImageFont.truetype(_GK, size)
    return _gc[size]
def atext(d, xy, s, size, color=INK, alpha=1.0):
    runs = [(p, FG(size * 1.12) if p == "α" else F(size)) for p in re.split(r"(α)", s) if p]
    x = xy[0] - sum(tw(d, p, f) for p, f in runs) / 2
    for p, f in runs: dtext(d, (x, xy[1]), p, f, color, alpha, "lm"); x += tw(d, p, f)
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def fmodel(f1, f2, a): return math.sqrt(f1 * f1 + f2 * f2 + 2 * f1 * f2 * math.cos(math.radians(a)))
def betas(f1, f2, a):
    b1 = math.degrees(math.atan2(f2 * math.sin(math.radians(a)), f1 + f2 * math.cos(math.radians(a))))
    return b1, a - b1

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-thuchanhthl-01.json")))
    for (f1, f2, a, f3), c, fv, h in zip(LAN, CHEO, FVE, k["so_lieu_mau"]["hang"]):
        assert (f1, f2, a, f3, c, fv, h[9]) == (h[1], h[2], h[3], h[4], h[6], h[7], DELTA), h
        assert abs(round(fmodel(f1, f2, a) / XICH, 1) - c) < 1e-9 and abs(c * XICH - fv) < 1e-9
    assert k["so_lieu_mau"]["hang"][2][5] == SO0
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}; assert ts["xich"]["gia_tri"] == XICH
    assert "Lực kế 5 N, độ chia 0,1 N" in [x["ten"] for x in k["dung_cu"]]
    assert LAN[0][3] < LAN[0][0] + LAN[0][1]                                        # du doan: nho hon tong
    assert abs(abs(1.75 - 2.1) - 0.35) < 1e-9 and abs((2.1 - SO0) - 1.8) < 1e-9 and abs(abs(1.75 - 1.8) - 0.05) < 1e-9
    assert abs(fmodel(0.9, 1.2, 90) - 1.5) < 1e-9                                   # ca chot
    for f1, f2, a, _ in LAN:                                                         # day can bang: thanh phan ngang triet tieu
        b1, b2 = betas(f1, f2, a); assert abs(f1 * math.sin(math.radians(b1)) - f2 * math.sin(math.radians(b2))) < 1e-9
_kiem_so()

OX, OY = 540, 640
def ux(beta, side):   # don vi theo day: side -1 = trai, +1 = phai ; beta tinh tu phuong thang dung huong len
    r = math.radians(beta); return (side * math.sin(r), -math.cos(r))

def meter_on(d, beta, side, f, alpha=1.0, o=(OX, OY)):
    u = ux(beta, side); nv = (u[1], -u[0])
    Q = lambda s, h: (o[0] + u[0] * s + nv[0] * h, o[1] + u[1] * s + nv[1] * h)
    d.line([o, Q(60, 0)], fill=A(NAVY, alpha), width=4)
    se = luc_ke(d, Q, 70, 90, 420, 5.0, f, nho=0.2, so=(0, 1, 2, 3, 4), hw=40, ben=1 if side < 0 else -1, alpha=alpha, co=55)
    p = Q(se + 10, 0); dot(d, p[0], p[1], 15, A((90, 95, 110), alpha), A(WHITE, alpha))       # chot tren gia

def meter3(d, f, weight=True, alpha=1.0, y_ring=None, x=OX):
    """Luc ke 3 thang dung duoi nut O: vong treo o tren (noi day len O), moc o duoi treo vat."""
    yr = y_ring or OY + 50; yb = yr + 416
    Q = lambda s, h: (x + h, yb - s)
    if y_ring is None: d.line([(x, OY), (x, OY + 50)], fill=A(NAVY, alpha), width=4)
    luc_ke(d, Q, 0, 20, 400, 5.0, f, nho=0.2, so=(0, 1, 2, 3, 4), hw=40, ben=1, alpha=alpha, co=55)
    if weight:
        d.line([(x, yb + 12), (x, yb + 30)], fill=A(NAVY, alpha), width=4)
        d.rounded_rectangle([x - 55, yb + 30, x + 55, yb + 120], radius=12, fill=A(BRASS, alpha), outline=A(BRASS_D, alpha), width=3)

def board(d):
    card(d, (50, 262, 1030, 1236), fill=PAPER, outline=LIGHT, r=18, w=3)

def chip(d, box, s, col, a=1.0):
    card(d, box, fill=A(WHITE, a), outline=A(col, a), r=24, w=4)
    text(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), s, 55, col, alpha=a)

def rig(d, b1, b2, f1, f2, f3, al, show, hide3=False):
    board(d)
    meter_on(d, b1, -1, f1); meter_on(d, b2, 1, f2); meter3(d, None if hide3 else f3)
    dot(d, OX, OY, 14, NAVY, WHITE)
    text(d, (OX - 60, OY + 20), "O", 55, NAVY)
    r = 90; a0 = -90 - b1; a1 = -90 + b2                                            # cung goc alpha giua hai day
    d.arc([OX - r, OY - r, OX + r, OY + r], a0, a1, fill=ORANGE, width=5)
    goc(d, "α = ···" if not show else f"α = {al:g}°")
    v = lambda x: "···" if not show else vn(x) + " N"
    chip(d, (60, 760, 400, 850), "F1 = " + v(f1), BLUE)
    chip(d, (680, 760, 1020, 850), "F2 = " + v(f2), BLUE)
    chip(d, (650, 980, 1020, 1070), "F3 = " + ("?" if hide3 else v(f3)), RED)

def goc(d, s, a=1.0):
    card(d, (42, 870, 492, 1060), fill=A(WHITE, a), outline=A(ORANGE, a), r=24, w=4)
    text(d, (267, 920), "góc giữa hai dây", 55, DORANGE, alpha=a)
    atext(d, (267, 1005), s, 55, DORANGE, alpha=a)

def table(d, n, y=1250, hl=-1):
    card(d, (40, y, 1040, y + 335), fill=WHITE, outline=NAVY, w=4)
    xs = (115, 300, 500, 690, 900)
    for x, h in zip(xs, ("Lần", "F1 (N)", "F2 (N)", "α", "F3 (N)")): atext(d, (x, y + 48), h, 55, INK)
    d.line([(60, y + 90), (1020, y + 90)], fill=LIGHT, width=4)
    for i in range(n):
        f1, f2, a, f3 = LAN[i]; yy = y + 136 + i * 70
        if i == hl: d.rounded_rectangle([55, yy - 33, 1025, yy + 33], radius=14, fill=(255, 237, 213))
        for x, s, col in zip(xs, (str(i + 1), vn(f1), vn(f2), f"{a}°", vn(f3)), (INK, BLUE, BLUE, DORANGE, RED)):
            text(d, (x, yy), s, 55, col)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; f1, f2, a, f3 = LAN[0]; b1, b2 = betas(f1, f2, a)
    rig(d, b1, b2, f1, f2, f3, a, True, hide3=True)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1085 + (1 - k) * 30
    card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    for j, s1 in enumerate(("F1, F2 hợp thành F.", "F hướng thế nào so với", "lực kéo của lực kế 3?")):
        text(d, (W / 2, y0 + 165 + j * 75), s1, 58, PURPLE if j == 2 else INK, alpha=k)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh ----------------
TS = [0.4, 2.8, 5.2]              # lan 1: cho O yen roi doc ; lan 2, 3: doi chot/vat (MOVE), cho O dung yen roi doc so
MOVE, SETTLE = 1.0, 0.5

def do_state(t):
    """-> (b1, b2, f1, f2, f3 kim, so hien?, so hang bang)."""
    k = max([i for i, s in enumerate(TS) if t >= s], default=-1)
    cb0 = betas(*LAN[0][:3])
    if k < 0: return cb0[0], cb0[1], LAN[0][0], LAN[0][1], None, False, 0
    x = t - TS[k]; cur = LAN[k]; cb = betas(*cur[:3])
    if k == 0:
        if x < SETTLE: return cb[0], cb[1], cur[0], cur[1], None, False, 0
        return cb[0], cb[1], cur[0], cur[1], cur[3], True, 1
    prev = LAN[k - 1]; pb = betas(*prev[:3])
    if x < MOVE + SETTLE:
        e = ease(x / MOVE)
        return (lerp(pb[0], cb[0], e), lerp(pb[1], cb[1], e), lerp(prev[0], cur[0], e), lerp(prev[1], cur[1], e),
                lerp(prev[3], cur[3], e), False, k)
    return cb[0], cb[1], cur[0], cur[1], cur[3], True, k + 1

def s_do(img, d, t, sc):
    b1, b2, f1, f2, f3, show, n = do_state(t)
    k = max(0, n - 1) if show else n
    rig(d, b1, b2, f1, f2, f3, LAN[min(k, 2)][2], show or n == 0, hide3=f3 is None)
    if not show and n == 0: chip(d, (650, 980, 1020, 1070), "F3 = ?", RED)
    table(d, n, hl=n - 1 if show else -1)

def _kiem_dong_bo():
    """Moi 0,05 s: khi so hien thi kim = so tren chip = hang cuoi bang, goc day dung mo hinh; khi chua on dinh thi an so."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        b1, b2, f1, f2, f3, show, n = do_state(t)
        if show:
            row = LAN[n - 1]; bb = betas(*row[:3])
            if (f1, f2, f3) != (row[0], row[1], row[3]) or abs(b1 - bb[0]) > 1e-9 or abs(b2 - bb[1]) > 1e-9: bad.append(round(t, 2))
        t += 0.05
    if TS[-1] + MOVE + SETTLE + 0.5 > sc["T"]: bad.append("lan cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + hinh binh hanh lan 1 (dung ti le) ----------------
PXCM = 60                          # px moi cm tren giay
def s_dapan(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.1, 0.4)
    card(d, (50, 380, 1030, 1130), fill=A(PAPER, k0), outline=A(LIGHT, k0), r=18, w=3)
    f1, f2, a, f3 = LAN[0]; b1, b2 = betas(f1, f2, a); o = (540, 770)
    u1, u2 = ux(b1, -1), ux(b2, 1)
    g = 0.05 + 0.95 * ease((t - 0.4) / 1.6)
    L1, L2 = f1 / XICH * PXCM, f2 / XICH * PXCM
    p1 = (o[0] + u1[0] * L1, o[1] + u1[1] * L1); p2 = (o[0] + u2[0] * L2, o[1] + u2[1] * L2)
    pf = (p1[0] + p2[0] - o[0], p1[1] + p2[1] - o[1])
    diag_cm = math.dist(o, pf) / PXCM
    assert abs(diag_cm - fmodel(f1, f2, a) / XICH) < 1e-6 and abs(round(diag_cm, 1) - CHEO[0]) < 1e-9
    arrow(d, o, (lerp(o[0], p1[0], g), lerp(o[1], p1[1], g)), A(BLUE, k0), w=7, head=24)
    arrow(d, o, (lerp(o[0], p2[0], g), lerp(o[1], p2[1], g)), A(BLUE, k0), w=7, head=24)
    text(d, (p1[0] - 25, p1[1] + 10), "F1 = 1,6 N", 55, BLUE, anchor="rm", alpha=k0)
    text(d, (p2[0] + 25, p2[1] + 40), "F2 = 2,1 N", 55, BLUE, anchor="lm", alpha=k0)
    text(d, (o[0] - 45, o[1] + 30), "O", 55, NAVY, alpha=k0)
    text(d, (1010, 1090), "1 cm ứng 0,5 N", 55, NOTE, anchor="rm", alpha=k0)
    k2 = appear(t, 2.2, 0.5)
    for q, p in ((p1, pf), (p2, pf)):                                               # canh song song (net dut)
        for j in range(12):
            s0, s1 = j / 12, (j + 0.55) / 12
            d.line([(lerp(q[0], p[0], s0), lerp(q[1], p[1], s0)), (lerp(q[0], p[0], s1), lerp(q[1], p[1], s1))], fill=A(GRAY, k2), width=4)
    if k2 > 0:
        arrow(d, o, pf, A(GREEN, k2), w=9, head=28)
        text(d, (pf[0] - 40, pf[1] + 10), "F vẽ", 55, DGREEN, anchor="rm", alpha=k2)
    k3 = appear(t, M[1], 0.5); kc = appear(t, M[1], 0.5)
    if k3 > 0:                                                                       # F3 do duoc: nguoc chieu, dung ti le
        L3 = f3 / XICH * PXCM; p3 = (o[0], o[1] + L3)
        arrow(d, o, p3, A(RED, k3), w=9, head=28)
        text(d, (o[0] + 40, o[1] + 190), "F3 = 2,9 N", 55, RED, anchor="lm", alpha=k3)
    dot(d, o[0], o[1], 10, NAVY, WHITE)
    card(d, (40, 1150, 1040, 1250), fill=A(WHITE, kc), outline=A(GREEN, kc), r=24, w=4)
    text(d, (W / 2, 1200), "chéo 5,7 cm → F vẽ = 2,85 N", 55, DGREEN, alpha=kc)
    kd = appear(t, M[2], 0.45)
    pill(d, W / 2, 320, "ĐÁP ÁN · Ngược chiều", NAVY, kd, size=55)
    card(d, (40, 1270, 1040, 1460), fill=A(WHITE, kd), outline=A(NAVY, kd), r=24, w=4)
    text(d, (W / 2, 1320), "δ = 0,05 N ≤ Δ = 0,3 N", 55, NAVY, alpha=kd)
    text(d, (W / 2, 1405), "độ lệch nhỏ hơn sai số", 55, DGREEN, alpha=kd)

# ---------------- canh 4: Bay (lan 3) + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    kz = appear(t, M[1], 0.45); k3 = appear(t, M[3] - 0.1, 0.4)
    board(d)
    if kz < 1:
        f1, f2, a, f3 = LAN[2]; b1, b2 = betas(f1, f2, a); a0 = 1 - kz
        meter_on(d, b1, -1, f1, alpha=a0); meter_on(d, b2, 1, f2, alpha=a0); meter3(d, f3, alpha=a0)
        dot(d, OX, OY, 14, A(NAVY, a0), A(WHITE, a0))
        d.arc([OX - 90, OY - 90, OX + 90, OY + 90], -90 - b1, -90 + b2, fill=A(ORANGE, a0), width=5)
        goc(d, "α = 110°", a0)
        chip(d, (60, 760, 400, 850), "F1 = 1,4 N", BLUE, a=a0); chip(d, (680, 760, 1020, 850), "F2 = 1,6 N", BLUE, a=a0)
        chip(d, (650, 980, 1020, 1070), "F3 = 2,1 N", RED, a=a0)
        chip(d, (650, 870, 1020, 960), "F vẽ = 1,75 N", DGREEN, a=a0)
    if kz > 0:                                                                       # luc ke 3 thao ra, treo thang dung, chua moc vat
        meter3(d, SO0, weight=False, alpha=kz, y_ring=420)
        chip(d, (650, 700, 1000, 790), "chỉ 0,3 N", DRED, a=kz)
    y = 1100
    if k3 < 1:
        a1 = 1 - k3
        card(d, (40, y, 1040, y + 485), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", DRED, a1)
        text(d, (W / 2, y + 165), "δ = 0,35 N > Δ", 55, DRED, alpha=a1)
        q = "“Quy tắc hình bình hành sai”"
        ks = clamp((t - M[2]) / 0.4); lw = tw(d, q, F(55)); yy = y + 250
        text(d, (W / 2, yy), q, 55, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        if t >= M[2]:
            text(d, (W / 2, y + 345), "2,1 − 0,3 = 1,8 N", 55, DGREEN, alpha=a1)
            text(d, (W / 2, y + 425), "δ = 0,05 N ≤ Δ", 55, DGREEN, alpha=a1)
    if k3 > 0:
        yk = y + (1 - k3) * 30
        card(d, (40, yk, 1040, yk + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, yk + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, yk + 215), "Sai số vẽ thì sao?", 58, INK, alpha=k3)

# ---------------- canh 5: Thu nghi ----------------
E1, E2 = 0.9, 1.2                  # ca chot: hai day vuong goc
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 290, 1040, 1530), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 350, "THỬ NGHĨ", ORANGE, k)
    o = (540, 720); PN = 190                                                        # px moi N
    b1, b2 = betas(E1, E2, 90); assert abs(b1 + b2 - 90) < 1e-9
    us = []
    for side, f, b, lab in ((-1, E1, b1, "F1 = 0,9 N"), (1, E2, b2, "F2 = 1,2 N")):
        u = ux(b, side); us.append(u); p = (o[0] + u[0] * f * PN, o[1] + u[1] * f * PN)
        arrow(d, o, p, A(BLUE, k), w=8, head=26)
        text(d, (p[0] + side * 20, p[1] - 30), lab, 55, BLUE, anchor="lm" if side > 0 else "rm", alpha=k)
    s_ = 34; q1 = (o[0] + us[0][0] * s_, o[1] + us[0][1] * s_); q2 = (o[0] + us[1][0] * s_, o[1] + us[1][1] * s_)
    qm = (q1[0] + q2[0] - o[0], q1[1] + q2[1] - o[1])
    d.line([q1, qm, q2], fill=A(DORANGE, k), width=4)                               # dau goc vuong
    meter3(d, None, weight=True, alpha=k, y_ring=770)
    d.line([o, (o[0], 770)], fill=A(NAVY, k), width=4)
    dot(d, o[0], o[1], 13, A(NAVY, k), A(WHITE, k))
    text(d, (o[0] - 50, o[1] + 25), "O", 55, NAVY, alpha=k)
    text(d, (290, 1030), "Hai dây", 55, INK, alpha=k); text(d, (290, 1100), "vuông góc.", 55, INK, alpha=k)
    text(d, (W / 2, 1350), "Lực kế 3 chỉ bao nhiêu?", 60, DORANGE, alpha=k)
    seg_bar(d, 1420, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + TS[0] + SETTLE, "tap")]
            + [(do["t0"] + s + MOVE + SETTLE, "tap") for s in TS[1:]]
            + [(da["t0"] + da["M"][2], "ding"), (b["t0"] + b["M"][2], "buzz"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-thuchanhthl-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Thực hành tổng hợp lực · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ba lực kế kéo nút O", draw=s_hook, tail=0.2, caps=[
   ("Lực kế 3 treo vật nặng.", 3.0),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Chờ nút O đứng yên rồi đọc.", 3.6),
   ("Đổi chốt hoặc vật, đọc lại.", 3.6)]),
 dict(key="dapan", title="Vẽ hình bình hành lần 1", draw=s_dapan, tail=0.3, caps=[
   ("Vẽ hình bình hành, 1 cm ứng 0,5 N.", 4.2),
   ("So F vẽ với lực kế 3.", 3.4),
   ("Đáp án: ngược chiều.", 2.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Lần 3: độ lệch quá Δ.", 3.4),
   ("Tháo vật, xem lực kế 3.", 3.4),
   ("Trừ số 0 lệch rồi so lại.", 3.8),
   ("Còn bỏ ngỏ.", 2.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
