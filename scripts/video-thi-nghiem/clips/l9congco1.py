# Clip: tn-l9-congco-01 - Keo deu khoi go bang luc ke, tinh cong A = F.s (KHTN 9, 05/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-congco-01.json:
#   so_lieu_mau (F N, s m, A J): 1,5 0,5 0,75 ; 1,6 0,5 0,80 ; 1,4 0,5 0,70 ; 1,5 1,0 1,5 (ghi_chu: so lieu minh hoa).
#   tham_so: F_that = 1,5 N (luc can), s 0,1..1,0 m buoc 0,1 ; dung_cu: luc ke GHD 5 N, DCNN 0,1 N.
#   quan_sat[0]: kim rung nhe quanh vach 1,5 N -> ve kim dao dong +-0,1 N (mo_hinh: "kim rung mot vach"), lan doc = so bang.
#   bay = hien_tuong_hay_sai[1] (keo xien len: chi mot phan luc cung huong dich chuyen) + mo_hinh.gia_thiet[1].
#   chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet (keo deu, luc theo phuong ngang).
# Cau hoi ngay sau hop trong bai (Cau 1: lam gi cho A dang tin hon -> keo deu, do nhieu lan lay trung binh) KHONG duoc
#   giai/goi y trong clip: khong noi "trung binh", "do nhieu lan", khong noi giat manh (lua chon A), luc ke do chia 1 N (C).
# Du doan (K10: chi cau hoi + hinh): keo deu nhu cu, di 1,00 m thay vi 0,50 m -> cong gap doi (0,75 -> 1,50 J).
# Dung lai theo cong moi 27/11/2026 (Viec 4 L9 nhom C): chu >= 56, canh <= 180 tu/phut, khoi chu cach >= 2,5 s.
# Cau hoi chot (ca MOI, nguoc chieu, khong phai phep nhan tran): keo deu, cong do duoc 1,2 J -> di bao xa?
#   Keo deu nen F van ~1,5 N (HS phai tu nho tu clip, cau hoi khong cho F) -> s = 1,2 : 1,5 = 0,80 m (trong dai tham_so s).
# Chua noi duoc: mat ban khac thi luc keo bao nhieu (chua do) - khong noi "trung binh/do nhieu lan" (Cau 1).
# Bo cuc (khac trongluc3/tonghopluc2 cua L10): ban ngang nhin ngang, keo sang TRAI (so tren luc ke tang sang phai),
#   thuoc do tu vach xuat phat; o phong to vach chia 0,1 N; bang F-s-A. Tu kiem: python3 clips/l9congco1.py --kiem
import math
from engine import *

ROWS = [(1.5, 0.5, 0.75), (1.6, 0.5, 0.80), (1.4, 0.5, 0.70), (1.5, 1.0, 1.5)]   # so_lieu_mau
F_THAT, FMAX = 1.5, 5.0
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); SKIN = (240, 196, 160); RULER = (253, 230, 138)
DGREEN = (21, 110, 55); DRED = (185, 28, 28)

# ---------------- dan thi nghiem (nhin ngang) ----------------
X_START, PX_M = 890, 300          # mep trai khoi go luc xuat phat; 1 m = 300 px (keo sang trai)
BW, BH, TOP, HOOK_Y = 120, 100, 560, 510
ROPE, BODY = 30, 400

def table_ruler(d, y_top=TOP, labels=True):
    d.rectangle([60, y_top, 1020, y_top + 34], fill=WOOD); d.line([(60, y_top), (1020, y_top)], fill=WOOD_D, width=4)
    # thuoc dat doc duong di, do tu vach xuat phat (mep trai khoi go luc dau)
    x1, x0 = X_START, X_START - PX_M
    d.rounded_rectangle([x0 - 30, y_top + 48, x1 + 30, y_top + 92], radius=8, fill=RULER, outline=WOOD_D, width=2)
    for k in range(21):
        x = x1 - k * PX_M / 20; L = 26 if k % 10 == 0 else (18 if k % 5 == 0 else 10)
        d.line([(x, y_top + 48), (x, y_top + 48 + L)], fill=NAVY, width=3 if L == 26 else 2)
    if labels:
        for k, s in ((0, "0"), (20, "1,00 m")):
            text(d, (x1 - k * PX_M / 20, y_top + 130), s, 56, INK)

def block(d, xl, y_top=TOP):
    d.rounded_rectangle([xl, y_top - BH, xl + BW, y_top], radius=8, fill=WOOD, outline=WOOD_D, width=4)
    for i in range(3):
        yy = y_top - BH + 24 + i * 26
        d.line([(xl + 16, yy), (xl + BW - 16, yy + 6)], fill=WOOD_D, width=2)
    dot(d, xl, HOOK_Y + (y_top - TOP), 8, NAVY)

def meter_h(d, xl, f_read, y_top=TOP):
    """Luc ke nam ngang (mau trongluc2, GHD 5 N, vach 0,1 N), moc vao mep trai khoi go, tay keo sang trai."""
    yh = HOOK_Y + (y_top - TOP)
    Q = lambda s, h=0.0: (xl - s, yh + h)
    d.line([Q(0), Q(ROPE - 13)], fill=NAVY, width=5)
    se = luc_ke(d, Q, ROPE, ROPE + 20, ROPE + 20 + BODY, FMAX, f_read, nho=0.1, so=(0, 1, 2, 3, 4, 5), hw=40, ben=-1, co=56)
    d.line([Q(se - 16), Q(se + 12)], fill=NAVY, width=8)
    hx, hy = Q(se + 40)
    dot(d, hx, hy, 28, SKIN, outline=(190, 140, 105))

def rig(d, xl, f_read):
    card(d, (40, 260, 1040, 730), fill=WHITE, outline=LIGHT, w=3)
    table_ruler(d); block(d, xl); meter_h(d, xl, f_read)

ZX0, ZPX = 730, 1300               # o phong to: x = ZX0 + (f - 1,5) * ZPX
def band(d, val, f_needle):
    """Hop so chi (trai) + o phong to vach chia 1,3..1,7 N (phai). f_needle None: an kim."""
    card(d, (40, 750, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    text(d, (230, 800), "Lực kế chỉ", 56, NAVY)
    text(d, (230, 880), val, 64, INK)
    d.line([(420, 770), (420, 910)], fill=LIGHT, width=3)
    yb = 860
    d.line([(450, yb), (1010, yb)], fill=NAVY, width=3)
    yb = 840
    for k in range(-4, 5):
        f = F_THAT + k * 0.05; x = ZX0 + (f - F_THAT) * ZPX
        if 455 <= x <= 1005: d.line([(x, yb), (x, yb - (30 if k % 2 == 0 else 14))], fill=NAVY, width=3 if k % 2 == 0 else 2)
    for v in (1.4, 1.5, 1.6):                     # GĐ2: chi 3 nhan, khong chen nhau
        text(d, (ZX0 + (v - F_THAT) * ZPX, yb + 40), vn(v), 56, INK)
    if f_needle is not None and 1.25 < f_needle < 1.75:
        x = ZX0 + (f_needle - F_THAT) * ZPX
        d.line([(x, yb - 56), (x, yb + 6)], fill=RED, width=6)
        d.polygon([(x, yb + 4), (x - 10, yb - 16), (x + 10, yb - 16)], fill=RED)

XS = (130, 380, 630, 880)
def table(d, n, y=950, show_a=None, hl=(), h=540):
    """n = so hang da ghi; show_a(j) -> alpha cot A (None = an ca cot)."""
    card(d, (40, y, 1040, y + h), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[1], y + 60), "F (N)", 56, NAVY); text(d, (XS[2], y + 60), "s (m)", 56, BLUE)
    if show_a is not None: text(d, (XS[3], y + 60), "A (J)", 56, ORANGE, alpha=show_a(-1))
    d.line([(70, y + 110), (1010, y + 110)], fill=LIGHT, width=3)
    for j, (f, s, a) in enumerate(ROWS):
        yy = y + 170 + j * (h - 160) / 4
        if j in hl: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=20, fill=(255, 237, 213))
        text(d, (XS[0], yy), f"lần {j + 1}", 56, NAVY)
        if j < n:
            text(d, (XS[1], yy), vn(f), 56, NAVY); text(d, (XS[2], yy), vn(s, 2), 56, BLUE)
        if show_a is not None:
            k = show_a(j)
            if k > 0: text(d, (XS[3], yy), vn(a, 2), 56, ORANGE, alpha=k)

def pill(d, s, y, a, color, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, X_START, None); band(d, "? N", None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 165), "Kéo đều 1,00 m", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "thay vì 0,50 m.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 335), "Công A đổi thế nào?", 58, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 420, 970, y0 + 510], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 420, 110 + max(90, 860 * (1 - p)), y0 + 510], radius=45, fill=A((76, 29, 149), a))

# ---------------- canh 2: Tien hanh ----------------
T_S = (0.4, 2.1, 3.8, 5.5)
RISE, V_PX = 0.3, 150 / 1.1
T_ROW = 0.2
OM = 2 * math.pi * 2.0

def pull(k):
    ts = T_S[k]; dur = ROWS[k][1] * PX_M / V_PX
    return ts, ts + RISE, ts + RISE + dur, ts + RISE + 0.6 * dur

def phase(k):
    fk = ROWS[k][0]; return math.asin(clamp((fk - F_THAT) / 0.1, -1, 1))

HOLD = 0.8
def do_state(t):
    k = sum(1 for ts in T_S if t >= ts - 1e-9) - 1
    n = sum(1 for j in range(4) if t >= pull(j)[2] + T_ROW - 1e-9)
    if k < 0: return -1, X_START, 0.0, None, n
    ts, tm, te, tr = pull(k)
    if t < tm:   x = X_START; f = F_THAT * ease((t - ts) / RISE)
    elif t < te:                                  # GĐ2: kim dung yen dung so ghi bang HOLD s ke tu luc doc
        x = X_START - (t - tm) * V_PX
        f = ROWS[k][0] if tr <= t < tr + HOLD else F_THAT + 0.1 * math.sin(OM * (t - tr - (HOLD if t >= tr + HOLD else 0)) + phase(k))
    else:        x = X_START - ROWS[k][1] * PX_M; f = F_THAT * (1 - ease((t - te) / 0.3))
    read = ROWS[k][0] if t >= tr - 1e-9 else (ROWS[k - 1][0] if k > 0 else None)
    return k, x, f, read, n

def s_do(img, d, t, sc):
    k, x, f, read, n = do_state(t)
    rig(d, x, max(0.0, f)); band(d, (vn(read) + " N") if read is not None else "…", f if f > 1.2 else None)
    table(d, n, hl=((n - 1,) if n > 0 else ()), h=600)

def _kiem_dong_bo():
    """Moi 0,05 s: hop so chi = so cua lan doc gan nhat; kim dung so do o luc doc; hang j chi hien sau khi lan j xong;
    go chi chay trong luc keo; quang di khop s cua hang."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        k, x, f, read, n = do_state(t)
        if k >= 0:
            ts, tm, te, tr = pull(k)
            if t >= te and abs((X_START - x) / PX_M - ROWS[k][1]) > 1e-6: bad.append((round(t, 2), "quang duong", x))
            if n not in (k, k + 1): bad.append((round(t, 2), "hang", k, n))
            if not (1.35 <= f <= 1.65) and tm + 0.05 < t < te: bad.append((round(t, 2), "kim ngoai 1 vach", f))
        elif n or read is not None: bad.append((round(t, 2), "truoc lan 1", n, read))
        t += 0.05
    for k in range(4):
        tr = pull(k)[3]; k2, _, f, _, _ = do_state(tr)
        if abs(f - ROWS[k][0]) > 1e-6: bad.append(("doc", k, f))
    if pull(3)[2] + T_ROW > sc["T"] - 0.3: bad.append("hang 4 hien qua muon")
    return bad

def _kiem_so():
    return [r for r in ROWS if abs(r[0] * r[1] - r[2]) > 1e-6] + ([] if abs(CHOT_A / F_THAT - 0.8) < 1e-9 else ["chot"])


# ---------------- canh 3: Ket qua ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    card(d, (40, 265, 1040, 395), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5)
    text(d, (W / 2, 330), "A = F·s", 66, DGREEN, alpha=ka)
    sa = lambda j: ka if j < 0 else appear(t, 0.8 + 0.45 * j, 0.35)
    k2 = appear(t, M[1] - 0.1, 0.45)
    table(d, 4, y=420, show_a=sa, hl=((0, 3) if k2 > 0 else ()), h=560)
    if k2 > 0:
        y0 = 1010
        card(d, (40, y0, 1040, y0 + 220), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), w=4)
        text(d, (W / 2, y0 + 65), "0,50 m  →  0,75 J", 58, (154, 52, 18), alpha=k2)
        text(d, (W / 2, y0 + 155), "1,00 m  →  1,50 J", 58, (154, 52, 18), alpha=k2)
        pill(d, "ĐÁP ÁN: công gấp đôi", 1320, k2, GREEN, 58)

# ---------------- canh 4: Rut ra (cot A theo s) ----------------
GX0, GBASE, GTOP = 100, 760, 380
def gy(a): return GBASE - a / 1.6 * (GBASE - GTOP)
BXS = (230, 450, 670, 890)
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 980), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GBASE), (1010, GBASE)], fill=NAVY, width=4)
    for j, (f, s, a) in enumerate(ROWS):
        g = ease((t - 0.3 - 0.3 * j) / 0.6)
        h = (GBASE - gy(a)) * g
        if h > 2: d.rectangle([BXS[j] - 60, GBASE - h, BXS[j] + 60, GBASE], fill=ORANGE)
        if g > 0.95: text(d, (BXS[j], gy(a) - 36), vn(a, 2), 56, ORANGE)
        text(d, (BXS[j], GBASE + 50), vn(s, 2), 56, BLUE)
        text(d, (BXS[j], GBASE + 130), vn(f) + " N", 56, NAVY)
    text(d, (GX0, 320), "A (J)", 56, ORANGE, anchor="lm")
    k1 = appear(t, M[0] + 0.3, 0.45)
    card(d, (40, 1010, 1040, 1150), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
    text(d, (W / 2, 1080), "Kéo đều: F gần như không đổi", 56, DGREEN, alpha=k1)
    k2 = appear(t, M[1] + 0.2, 0.45)
    card(d, (40, 1180, 1040, 1320), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), w=4)
    text(d, (W / 2, 1250), "s gấp đôi → A gấp đôi", 58, (154, 52, 18), alpha=k2)

# ---------------- canh 5: Bay (keo xien) roi Chua noi duoc ----------------
TILT = math.radians(20)
BAY_ST = 2.2
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 730), fill=WHITE, outline=LIGHT, w=3)
    table_ruler(d, labels=False)
    xl = 860 - 25 * t; block(d, xl)
    ux, uy = -math.cos(TILT), -math.sin(TILT); nx, ny = -uy, ux
    Q = lambda s, h=0.0: (xl + ux * s + nx * h, HOOK_Y + uy * s + ny * h)
    d.line([Q(0), Q(ROPE - 13)], fill=NAVY, width=5)
    se = luc_ke(d, Q, ROPE, ROPE + 20, ROPE + 20 + BODY, FMAX, 1.8, nho=0.1, so=(), hw=40, ben=-1, co=56)
    d.line([Q(se - 16), Q(se + 12)], fill=NAVY, width=8)
    hx, hy = Q(se + 40); dot(d, hx, hy, 28, SKIN, outline=(190, 140, 105))
    pa, pb = Q(80, 110), Q(330, 110)
    arrow(d, pa, pb, ORANGE, w=8, head=26); text(d, (pb[0] + 10, pb[1] + 50), "lực", 56, ORANGE, anchor="lm")
    arrow(d, (xl + BW, 690), (xl - 160, 690), BLUE, w=8, head=26)
    text(d, (xl - 180, 690), "dịch chuyển", 56, BLUE, anchor="rm")
    k2 = appear(t, M[2] - 0.1, 0.45)
    a1 = (1 - k2); y0 = 770
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        for j, q in enumerate(("“Kéo xiên: A bằng", "số lực kế nhân s”")):
            yy = y0 + 170 + j * 80; lw = tw(d, q, F(58))
            text(d, (W / 2, yy), q, 58, INK, alpha=a1)
            ks = clamp((t - BAY_ST) / 0.4)
            if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, M[1] + 0.1, 0.4)
        card(d, (70, y0 + 330, 1010, y0 + 560), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 400), "✓ A = F·s khi lực", 58, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 485), "cùng hướng dịch chuyển", 58, DGREEN, alpha=kk)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "mặt bàn khác thì lực?", 58, INK, alpha=k2)
        text(d, (W / 2, y0 + 320), "(chưa đo)", 56, NAVY, alpha=k2)

# ---------------- canh 6: Chot ----------------
CHOT_A = 1.2                       # J; keo deu F ~ 1,5 N -> s = 0,80 m (khong hien)
END_Q = 0.2
def s_end(img, d, t, sc):
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 280, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 350, k1, ORANGE)
    text(d, (W / 2, 465), "Cùng khối gỗ, kéo đều.", 58, INK, alpha=k1)
    text(d, (W / 2, 550), "Công đo được " + vn(CHOT_A) + " J.", 58, INK, alpha=k1)
    text(d, (W / 2, 635), "Khối gỗ đi bao xa?", 58, INK, alpha=k1)
    if k1 <= 0: return
    y = 1050; x1 = 860; x0 = 300
    d.line([(80, y), (1000, y)], fill=A(WOOD_D, k1), width=8)
    d.rounded_rectangle([x1, y - 100, x1 + 120, y], radius=8, fill=A(WOOD, k1), outline=A(WOOD_D, k1), width=4)
    d.rounded_rectangle([x0, y - 100, x0 + 120, y], radius=8, outline=A(WOOD_D, k1), width=3)
    arrow(d, (x1, y + 60), (x0, y + 60), A(BLUE, k1), w=6, head=22); arrow(d, (x0, y + 60), (x1, y + 60), A(BLUE, k1), w=6, head=22)
    rr = 60 + 30 * math.sin(2 * math.pi * t / 2.0)
    xc, yc = (x0 + x1) / 2, y + 220
    d.ellipse([xc - rr, yc - rr, xc + rr, yc + rr], fill=A(mix(ORANGE, WHITE, 0.45), k1))
    text(d, (xc, yc), "?", 80, WHITE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + T_S[0], "tap")]
    out += [(do["t0"] + ts, "tick") for ts in T_S[1:]]
    out += [(da["t0"] + da["M"][1] - 0.1, "ding"), (r["t0"] + r["M"][1] + 0.2, "tap"), (b["t0"] + BAY_ST, "buzz"),
            (b["t0"] + b["M"][1] + 0.1, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return sorted(out)

CLIP = dict(id="tn-l9-congco-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Công cơ học · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kéo khối gỗ bằng lực kế", draw=s_hook, tail=0.3, caps=[
   ("Kéo đều khối gỗ.", 2.5),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đọc lực kế khi gỗ chạy đều.", 3.4),
   ("Kim rung nhẹ quanh 1,5 N.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Nhân F với s mỗi lần.", 3.0),
   ("So lần 1 với lần 4.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Xem F dưới mỗi cột.", 2.9),
   ("So cột đầu và cuối.", 2.9)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 4.2),
   ("Xem mũi tên.", 3.4),
   ("Còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 6.2)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch A = F·s:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
