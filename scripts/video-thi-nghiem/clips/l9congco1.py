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
# Cau hoi chot: keo deu 0,60 m (chua tung hien, nam giua 0,50 va 1,00 m) -> A = 1,5 . 0,60 = 0,90 J (chua hien).
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
        for k, s in ((0, "0"), (10, "0,50 m"), (20, "1,00 m")):
            text(d, (x1 - k * PX_M / 20, y_top + 130), s, 40, INK)
        arrow(d, (520, y_top + 80), (330, y_top + 80), BLUE, w=6, head=20)
        text(d, (310, y_top + 80), "dịch chuyển", 40, BLUE, anchor="rm")

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
    se = luc_ke(d, Q, ROPE, ROPE + 20, ROPE + 20 + BODY, FMAX, f_read, nho=0.1, so=(0, 1, 2, 3, 4, 5), hw=40, ben=-1)
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
    text(d, (230, 795), "Lực kế chỉ", 40, INK, bold=False)
    text(d, (230, 870), val, 60, INK)
    d.line([(420, 770), (420, 910)], fill=LIGHT, width=3)
    yb = 860
    d.line([(450, yb), (1010, yb)], fill=NAVY, width=3)
    for k in range(-4, 5):
        f = F_THAT + k * 0.05; x = ZX0 + (f - F_THAT) * ZPX
        if 455 <= x <= 1005: d.line([(x, yb), (x, yb - (30 if k % 2 == 0 else 14))], fill=NAVY, width=3 if k % 2 == 0 else 2)
    for v in (1.3, 1.4, 1.5, 1.6, 1.7):
        text(d, (ZX0 + (v - F_THAT) * ZPX, yb + 38), vn(v), 40, INK)
    if f_needle is not None and 1.25 < f_needle < 1.75:
        x = ZX0 + (f_needle - F_THAT) * ZPX
        d.line([(x, yb - 56), (x, yb + 6)], fill=RED, width=6)
        d.polygon([(x, yb + 4), (x - 10, yb - 16), (x + 10, yb - 16)], fill=RED)

XS = (110, 330, 600, 870)
def table(d, n, y=950, show_a=None, hl=()):
    """n = so hang da ghi; show_a(j) -> alpha cot A (None = an ca cot)."""
    card(d, (40, y, 1040, y + 540), fill=WHITE, outline=LIGHT, w=3)
    for x, t1, t2, c in ((XS[1], "lực kéo", "F (N)", INK), (XS[2], "quãng đường", "s (m)", INK)):
        text(d, (x, y + 48), t1, 40, MUTED, bold=False); text(d, (x, y + 100), t2, 44, c)
    if show_a is not None:
        k = show_a(-1)
        text(d, (XS[3], y + 48), "công", 40, MUTED, bold=False, alpha=k); text(d, (XS[3], y + 100), "A (J)", 44, ORANGE, alpha=k)
    d.line([(70, y + 140), (1010, y + 140)], fill=LIGHT, width=3)
    for j, (f, s, a) in enumerate(ROWS):
        yy = y + 195 + j * 92
        if j in hl: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=20, fill=(255, 237, 213))
        text(d, (XS[0], yy), f"lần {j + 1}", 40, MUTED, bold=False)
        if j < n:
            text(d, (XS[1], yy), vn(f), 48, NAVY); text(d, (XS[2], yy), vn(s, 2), 48, BLUE)
        else:
            for x in XS[1:3]: text(d, (x, yy), "·", 44, GRAY)
        if show_a is not None:
            k = show_a(j)
            if k > 0: text(d, (XS[3], yy), vn(a, 2), 48, ORANGE, alpha=k)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, X_START, None); band(d, "? N", None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 450), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 240, "Kéo đều 1,00 m\nthay vì 0,50 m.\nCông A thay đổi thế nào?", 52, INK,
          maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 400, 940, y0 + 412], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 400, 140 + 800 * (1 - p), y0 + 412], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T_S = (0.4, 2.1, 3.8, 5.5)     # bat dau moi lan keo
RISE, V_PX = 0.3, 150 / 1.1    # kim len 0,3 s roi go chay deu (0,50 m trong 1,1 s)
T_ROW = 0.2                    # hang bang hien sau khi go dung
OM = 2 * math.pi * 2.0         # kim rung 2 lan/giay

def pull(k):
    ts = T_S[k]; dur = ROWS[k][1] * PX_M / V_PX
    return ts, ts + RISE, ts + RISE + dur, ts + RISE + 0.6 * dur      # bat dau, go bat dau chay, go dung, luc doc

def phase(k):
    fk = ROWS[k][0]; return math.asin(clamp((fk - F_THAT) / 0.1, -1, 1))

def do_state(t):
    """-> (k lan keo dang/vua xong (-1 chua), x mep trai go, so chi kim, so da doc tren hop (None), so hang da ghi)."""
    k = sum(1 for ts in T_S if t >= ts - 1e-9) - 1
    n = sum(1 for j in range(4) if t >= pull(j)[2] + T_ROW - 1e-9)
    if k < 0: return -1, X_START, 0.0, None, n
    ts, tm, te, tr = pull(k)
    if t < tm:   x = X_START; f = F_THAT * ease((t - ts) / RISE)
    elif t < te: x = X_START - (t - tm) * V_PX; f = F_THAT + 0.1 * math.sin(OM * (t - tr) + phase(k))
    else:        x = X_START - ROWS[k][1] * PX_M; f = F_THAT * (1 - ease((t - te) / 0.3))
    read = ROWS[k][0] if t >= tr - 1e-9 else (ROWS[k - 1][0] if k > 0 else None)
    return k, x, f, read, n

def s_do(img, d, t, sc):
    k, x, f, read, n = do_state(t)
    rig(d, x, max(0.0, f)); band(d, (vn(read) + " N") if read is not None else "…", f if f > 1.2 else None)
    table(d, n, hl=((n - 1,) if n > 0 else ()))

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
    return [r for r in ROWS if abs(r[0] * r[1] - r[2]) > 1e-6] + ([] if abs(F_THAT * 0.6 - 0.9) < 1e-9 else ["chot"])

# ---------------- canh 3: Ket qua ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · công gấp đôi"
    pw = tw(d, lab, F(42)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 344), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 308), lab, 42, WHITE, alpha=ka)
    sa = lambda j: appear(t, 0.4, 0.4) if j < 0 else appear(t, 0.8 + 0.45 * j, 0.35)
    k2 = appear(t, M[1] - 0.1, 0.45)
    table(d, 4, y=380, show_a=sa, hl=((0, 3) if k2 > 0 else ()))
    k1 = appear(t, M[0] + 0.2, 0.45)
    if k1 > 0:
        y0 = 950 + (1 - k1) * 30
        card(d, (40, y0, 1040, y0 + 260), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, y0 + 80), "A = F·s", 64, GREEN, alpha=k1)
        text(d, (W / 2, y0 + 180), "A: công (jun, J)", 42, DGREEN, alpha=k1)
    if k2 > 0:
        y0 = 1240 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 250), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), w=4)
        text(d, (W / 2, y0 + 75), "lần 1:  0,50 m  →  0,75 J", 46, (154, 52, 18), alpha=k2)
        text(d, (W / 2, y0 + 175), "lần 4:  1,00 m  →  1,50 J", 46, (154, 52, 18), alpha=k2)

# ---------------- canh 4: Rut ra (cot A theo s + co che) ----------------
GX0, GBASE, GTOP = 130, 760, 360
def gy(a): return GBASE - a / 1.6 * (GBASE - GTOP)
BXS = (300, 480, 660, 870)
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GTOP - 30), (GX0, GBASE)], fill=NAVY, width=4)
    d.line([(GX0, GBASE), (1000, GBASE)], fill=NAVY, width=4)
    text(d, (GX0 + 20, 310), "công A (J)", 42, ORANGE, anchor="lm")
    for j, (f, s, a) in enumerate(ROWS):
        g = ease((t - 0.3 - 0.3 * j) / 0.6)
        h = (GBASE - gy(a)) * g
        if h > 2: d.rectangle([BXS[j] - 55, GBASE - h, BXS[j] + 55, GBASE], fill=ORANGE)
        if g > 0.95: text(d, (BXS[j], gy(a) - 32), vn(a, 2), 42, ORANGE)
        text(d, (BXS[j], GBASE + 40), vn(s, 2) + " m", 40, BLUE)
        text(d, (BXS[j], GBASE + 100), vn(f) + " N", 40, NAVY)
    k1 = appear(t, M[0] + 0.3, 0.45)
    card(d, (40, 1000, 1040, 1160), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
    text(d, (W / 2, 1080), "Kéo đều: số chỉ lực kế gần như không đổi", 44, DGREEN, alpha=k1)
    k2 = appear(t, M[1] + 0.2, 0.45)
    card(d, (40, 1200, 1040, 1350), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), w=4)
    text(d, (W / 2, 1275), "Quãng đường gấp đôi → công gấp đôi", 44, (154, 52, 18), alpha=k2)

# ---------------- canh 5: Bay (keo xien) roi Chua noi duoc ----------------
TILT = math.radians(20)
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 730), fill=WHITE, outline=LIGHT, w=3)
    table_ruler(d, labels=False)
    xl = 840; block(d, xl)
    ux, uy = -math.cos(TILT), -math.sin(TILT); nx, ny = -uy, ux
    Q = lambda s, h=0.0: (xl + ux * s + nx * h, HOOK_Y + uy * s + ny * h)
    d.line([Q(0), Q(ROPE - 13)], fill=NAVY, width=5)
    se = luc_ke(d, Q, ROPE, ROPE + 20, ROPE + 20 + BODY, FMAX, None, nho=0.1, so=(0, 1, 2, 3, 4, 5), hw=40, ben=-1)
    d.line([Q(se - 16), Q(se + 12)], fill=NAVY, width=8)
    hx, hy = Q(se + 40); dot(d, hx, hy, 28, SKIN, outline=(190, 140, 105))
    # huong luc keo (doc luc ke) va huong go di (ngang)
    arrow(d, Q(60, 100), Q(280, 100), ORANGE, w=7, head=24)
    arrow(d, (xl + BW, 690), (xl - 120, 690), BLUE, w=7, head=24)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 770
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        q = "“Kéo xiên: lực kế nhân s”"
        ks = clamp((t - M[0] - 2.2) / 0.4)
        f = F(48); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2 - 20, yy), q, 48, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            xa = W / 2 - 20 - lw / 2 - 6
            d.line([(xa, yy + 2), (xa + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 - 20 + lw / 2 + 40, yy), "✗", 48, DRED, alpha=a1 * ks)
        kk = a1 * appear(t, M[0] + 2.4, 0.4)
        card(d, (70, y0 + 290, 1010, y0 + 520), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 360), "✓ Tính A = F·s khi lực", 46, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 445), "cùng hướng dịch chuyển", 46, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 770 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 360), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        text(d, (90, y0 + 180), "• Số liệu minh hoạ,", 46, INK, anchor="lm", alpha=kk)
        text(d, (128, y0 + 270), "chưa phải số đo thật", 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        # hinh nho: khoi go keo deu 0,60 m (luc ke che "?")
        y = 1150; x1 = 840; x0 = x1 - 0.6 * 600
        d.line([(110, y), (970, y)], fill=A(WOOD_D, k), width=6)
        d.rounded_rectangle([x1, y - 80, x1 + 96, y], radius=8, fill=A(WOOD, k), outline=A(WOOD_D, k), width=4)
        d.rounded_rectangle([x0 - 10, y - 80, x0 + 86, y], radius=8, outline=A(WOOD_D, k), width=3)
        arrow(d, (x1, y + 40), (x0, y + 40), A(BLUE, k), w=5, head=18); arrow(d, (x0, y + 40), (x1, y + 40), A(BLUE, k), w=5, head=18)
        text(d, ((x0 + x1) / 2, y + 90), "0,60 m", 44, BLUE, alpha=k)
        text(d, (x0 - 130, y - 40), "A = ? J", 44, ORANGE, alpha=k)
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1355, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1450, "Lực kéo đều có đổi không?", 44, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Kéo đều: công tăng\ntheo quãng đường",
             "Cùng khối gỗ, kéo đều 0,60 m.\nCông bao nhiêu jun?", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"), (do["t0"] + T_S[0], "tap")]
    out += [(do["t0"] + ts, "tick") for ts in T_S[1:]]
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 0.2, "tap"), (b["t0"] + 0.2, "buzz"),
            (b["t0"] + b["M"][0] + 2.4, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-congco-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Công cơ học · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kéo khối gỗ bằng lực kế", draw=s_hook, tail=0.8, caps=[
   ("Kéo đều khối gỗ trên bàn.", 3.0),
   ("Dừng video, chọn câu trả lời.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Đọc lực kế khi gỗ chạy đều.", 3.8),
   ("Kim rung nhẹ quanh 1,5 N.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Nhân F với s mỗi lần.", 3.0),
   ("So lần đầu với lần cuối.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Xem số lực kế dưới mỗi cột.", 3.8),
   ("So cột 0,50 m với 1,00 m.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Kéo xiên lên thì sao?", 5.3),
   ("Chưa nói được gì?", 3.3)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 5.6)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch A = F·s:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
