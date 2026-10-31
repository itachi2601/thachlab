# Clip: tn-l11-conangdddh-01 - Do k bang cach treo qua nang, roi tinh Et, Ed, W tai cac vach li do (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-conangdddh-01.json:
#   tham_so: m = 0,200 kg ; g = 9,8 m/s^2 ; A = 0,080 m. cac_buoc.lam: delta_l = 0,049 m -> k = 40 N/m.
#   so_lieu_mau (x m, Et, Ed, W J): 0 0 0,128 0,128 ; 0,04 0,032 0,096 0,128 ; A/sqrt2 (5,66 cm) 0,064 0,064 0,128 ;
#     A sqrt3/2 (6,93 cm) 0,096 0,032 0,128 ; 0,08 0,128 0 0,128.
#   hien_tuong_hay_sai[3]: moc the nang o cho lo xo chua dan -> tai VTCB ra 0,04802 J thay vi 0 -> canh bay.
#   Du doan: vat o x = 4,0 cm (A/2): Ed so voi Et? Dap an: Ed = 3 Et (hien_tuong_hay_sai[1]: tuong bang nhau).
#   Cau chot: li do nao Et = 3 Ed? -> x = A sqrt3/2 ~ 6,93 cm. Hang 6,93 cm KHONG hien o bang (chi 4 hang), so 6,93
#   khong xuat hien tren man; nguoc phan xa tuyen tinh (3/4 A = 6 cm).
# Dan canh rieng (khac motadddh1/motadddh2/vantocdddh1): Tien hanh 1 = GIA TREO lo xo dung + thuoc dung do delta_l;
#   Tien hanh 2 = ray nho + COT NANG LUONG chong (Et cam duoi, Ed xanh tren, dinh = W) + bang 4 hang; dung hinh
#   tai tung vach (vat dang chay, khong phai giu yen -> Ed khac 0 dung vat li).
# Chuyen dong: x = A cos(omega tau), omega = sqrt(k/m) = sqrt(200) rad/s, T = 0,444 s; quay cham x24 (ghi tren man);
#   tau = thoi gian chay (bo qua luc dung hinh) / 24. Vach 5,66 cm o pha pi/4, 4,0 cm o pi/3, 0 o pi/2.
from engine import *

K_, A_M, W_J = 40.0, 0.08, 0.128
OMEGA = math.sqrt(200.0)
SLOW = 24
TV = SLOW * 2 * math.pi / OMEGA                          # chu ki tren video (s)
ROWS = [("8,0", 8.0, "0,128", "0"), ("5,66", 80 * math.cos(math.pi / 4) / 10, "0,064", "0,064"),
        ("4,0", 4.0, "0,032", "0,096"), ("0", 0.0, "0", "0,128")]   # x (cm) nhan, x so, Et, Ed (so_lieu_mau)
DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55)
CET = (234, 88, 12); CED = (37, 99, 235)                 # mau Et (cam) / Ed (xanh)
BLOCK = (250, 204, 120); WOOD = (196, 160, 112)
def et_of(x_cm): return 0.5 * K_ * (x_cm / 100) ** 2

_TI = {}
def TI(size):                                            # Times Bold Italic cho ky hieu l (SF khong co glyph)
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Cong thuc: 'ℓ' ve bang Times Bold Italic; _{..} chi so duoi, ^{..} so mu (>= 36 px)."""
    fs = []
    for p in [p for p in re.split(r"(ℓ|_\{[^}]*\}|\^\{[^}]*\})", s) if p]:
        if p == "ℓ": fs.append((p, TI(size * 1.1), 0))
        elif p.startswith("_{"): fs.append((p[2:-1], F(max(40, size * 0.62)), size * 0.26))
        elif p.startswith("^{"): fs.append((p[2:-1], F(max(40, size * 0.62)), -size * 0.34))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def coil(d, x, ya, yb, amp=26, n=12, col=NAVY, w=5, alpha=1.0):
    """Lo xo dung tu ya xuong yb."""
    e = 16; pts = [(x, ya), (x, ya + e)]; L = (yb - e) - (ya + e)
    for i in range(1, 2 * n): pts.append((x + (amp if i % 2 else -amp), ya + e + L * i / (2 * n)))
    pts += [(x, yb - e), (x, yb)]
    d.line(pts, fill=A(col, alpha), width=w, joint="curve")

def hcoil(d, xa, xb, y, amp=22, n=12, col=NAVY, w=5):
    e = 14; pts = [(xa, y), (xa + e, y)]; L = (xb - e) - (xa + e)
    for i in range(1, 2 * n): pts.append((xa + e + L * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(xb - e, y), (xb, y)]
    d.line(pts, fill=col, width=w, joint="curve")

def dashed(d, p0, p1, col, w=4, on=16, off=12):
    L = math.dist(p0, p1); n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p0[0], p1[0], a), lerp(p0[1], p1[1], a)), (lerp(p0[0], p1[0], b), lerp(p0[1], p1[1], b))], fill=col, width=w)

# ---------------- gia treo (do k) ----------------
def stand(d, sx, top, base, arm1, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rectangle([sx - 120, base, sx + 300, base + 30], fill=c(GRAY), outline=c(NAVY), width=3)
    d.rectangle([sx - 10, top - 10, sx + 10, base], fill=c(GRAY), outline=c(NAVY), width=3)
    d.rectangle([sx - 10, top - 14, arm1, top + 10], fill=c(GRAY), outline=c(NAVY), width=3)

def hang(d, cx, top, yend, alpha=1.0, label=True, mass=1.0):
    """Lo xo treo tu top, dau duoi o yend; qua nang 200 g treo duoi (mass = do hien qua nang)."""
    coil(d, cx, top + 10, yend, alpha=alpha)
    d.line([(cx, yend), (cx, yend + 22)], fill=A(NAVY, alpha), width=5)
    if mass <= 0: return
    alpha = alpha * mass
    d.rounded_rectangle([cx - 70, yend + 22, cx + 70, yend + 130], radius=14, fill=A(BLOCK, alpha), outline=A(NAVY, alpha), width=4)
    if label: text(d, (cx, yend + 76), "200 g", 40, INK, alpha=alpha)

# khung do k (canh Tien hanh 1)
SX, TOP, BASE = 170, 330, 1100
HX = 470                                         # truc lo xo
Y0 = 680                                         # dau duoi lo xo luc chua treo (vach 0 cua thuoc)
PXC = 50                                         # px / cm
YE = Y0 + 4.9 * PXC                              # dau duoi khi treo 200 g (dan 4,9 cm)
RX = 600                                         # thuoc dung

def ruler_v(d, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rectangle([RX, Y0 - 20, RX + 44, Y0 + 6 * PXC + 20], fill=c((250, 240, 200)), outline=c(NAVY), width=2)
    for k in range(0, 61):
        y = Y0 + k * PXC / 10
        L = 24 if k % 10 == 0 else (15 if k % 5 == 0 else 8)
        d.line([(RX, y), (RX + L, y)], fill=c(NAVY), width=3 if L == 24 else 2)
    for k in range(0, 7):
        text(d, (RX + 62, Y0 + k * PXC), str(k), 40, INK, bold=False, anchor="lm", alpha=alpha)
    text(d, (RX + 22, Y0 - 56), "cm", 40, INK, bold=False, alpha=alpha)

# ---------------- canh: Du doan (K10: chi cau hoi + hinh) ----------------
XO, PX, RY = 420, 70, 420                        # ray nho: O, px/cm, tam vat
def X(x_cm): return XO + x_cm * PX
def rail(d, x_cm, vfrac=0.0, olab=True, marks=True):
    """Ray go: tuong trai, lo xo ngang, vat 200 g, thuoc cm duoi ray, vach O; vfrac > 0 -> mui ten v sang trai."""
    d.rectangle([60, 330, 84, 480], fill=GRAY, outline=NAVY, width=3)
    d.rectangle([60, 470, 1050, 490], fill=WOOD, outline=NAVY, width=2)
    dashed(d, (XO, 330), (XO, 468), MUTED, w=4, on=12, off=10)
    if olab: text(d, (XO, 300), "O", 40, MUTED)
    xc = X(x_cm)
    hcoil(d, 84, xc - 50, RY)
    d.rounded_rectangle([xc - 50, RY - 46, xc + 50, RY + 46], radius=12, fill=BLOCK, outline=NAVY, width=4)
    d.rectangle([X(0) - 20, 505, X(8) + 20, 545], fill=(250, 240, 200), outline=NAVY, width=2)
    for k in range(0, 81, 5):
        L = 22 if k % 10 == 0 else 12
        d.line([(X(k / 10), 505), (X(k / 10), 505 + L)], fill=NAVY, width=3 if L == 22 else 2)
    for k in range(0, 9, 2): text(d, (X(k), 580), str(k), 40, INK, bold=False)
    text(d, (X(0) - 46, 580), "cm", 40, INK, bold=False, anchor="rm")
    if marks:                                    # vach da danh dau (dau cam tren mat ray)
        for _, xv, _, _ in ROWS:
            d.polygon([(X(xv), 492), (X(xv) - 10, 504), (X(xv) + 10, 504)], fill=ORANGE)
    if vfrac > 0.01:
        L = 170 * vfrac
        arrow(d, (xc, RY - 78), (xc - L, RY - 78), DGREEN, w=6, head=20)
        text(d, (xc - L - 14, RY - 78), "v (vận tốc)" if xc - L > 330 else "v", 40, DGREEN, anchor="rm")

def s_hook(img, d, t, sc):
    M = sc["M"]
    rail(d, 4.0, marks=False)
    k = appear(t, 0.6, 0.5)
    if k > 0:                                    # x = 4,0 cm (O -> vat) va A = 8,0 cm (O -> bien)
        y = 640
        d.line([(XO, y), (X(4), y)], fill=A(ORANGE, k), width=5)
        for xx in (XO, X(4)): d.line([(xx, y - 14), (xx, y + 14)], fill=A(ORANGE, k), width=5)
        text(d, ((XO + X(4)) / 2, y + 44), "x = 4,0 cm", 42, ORANGE, alpha=k)
        y = 740
        d.line([(XO, y), (X(8), y)], fill=A(NAVY, k), width=5)
        for xx in (XO, X(8)): d.line([(xx, y - 14), (xx, y + 14)], fill=A(NAVY, k), width=5)
        text(d, ((XO + X(8)) / 2, y + 44), "biên độ A = 8,0 cm", 42, NAVY, alpha=k)
    kc = appear(t, 1.2, 0.5)
    if kc > 0:                                   # hai cot nang luong chua biet
        for bx, lab, col in ((300, "E_{t}", CET), (640, "E_{d}", CED)):
            d.rounded_rectangle([bx, 860, bx + 140, 960], radius=10, fill=A((245, 243, 255), kc), outline=A(col, kc), width=4)
            text(d, (bx + 70, 910), "?", 56, PURPLE, alpha=kc)
            eq(d, bx + 200, 910, lab, 48, col, alpha=kc, anchor="l")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 480), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 245, "Vật qua x = 4,0 cm, nửa biên độ.\nĐộng năng và thế năng\nso với nhau thế nào?", 48, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 420, 940, y0 + 432], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 420, 140 + 800 * (1 - p), y0 + 432], radius=6, fill=A(PURPLE, a))

# ---------------- canh: Tien hanh 1 - do k ----------------
H0, H1 = 0.5, 1.6                               # lo xo dan dan tu 0 toi 4,9 cm
def yend_at(t): return Y0 + 4.9 * PXC * ease((t - H0) / (H1 - H0))

def s_dok(img, d, t, sc):
    M = sc["M"]
    stand(d, SX, TOP, BASE, HX + 40)
    ruler_v(d)
    ye = yend_at(t)
    hang(d, HX, TOP, ye, mass=appear(t, H0 - 0.3, 0.3))     # chua treo: chi co moc; treo roi ha nhe tay
    if H0 - 0.3 <= t < H1 + 0.1:
        card(d, (690, 1030, 990, 1090), fill=NAVY, r=30); text(d, (840, 1060), "hạ nhẹ tay", 40, WHITE)
    dashed(d, (HX + 40, Y0), (RX - 4, Y0), MUTED, w=3)                  # muc chua treo
    d.line([(HX + 40, ye), (RX - 4, ye)], fill=ORANGE, width=4)          # muc dau lo xo hien tai
    kb = appear(t, H1 + 0.2, 0.4)                                        # chi hien khi lo xo da dung yen
    if kb > 0:
        bx = RX + 120
        d.line([(bx, Y0), (bx, YE)], fill=A(ORANGE, kb), width=5)
        for yy in (Y0, YE): d.line([(bx - 14, yy), (bx + 14, yy)], fill=A(ORANGE, kb), width=5)
        eq(d, bx + 26, (Y0 + YE) / 2, "Δℓ = 4,9 cm", 44, ORANGE, alpha=kb, anchor="l")
    km = appear(t, 0.5, 0.4)
    card(d, (60, 1170, 1020, 1470), fill=A(WHITE, km), outline=A(NAVY, km), r=24, w=4)
    eq(d, W / 2, 1235, "m = 0,200 kg   g = 9,8 m/s^{2}", 44, INK, alpha=km)
    kk = appear(t, M[1] + 0.1, 0.5)
    if kk > 0:
        eq(d, W / 2, 1325, "k = mg / Δℓ", 50, DBLUE, alpha=kk)
        eq(d, W / 2, 1410, "= 0,200 · 9,8 / 0,049 = 40 N/m", 46, DBLUE, alpha=kk)

# ---------------- canh: Tien hanh 2 - cot nang luong + bang ----------------
P0, P1, REL, FZ = 0.4, 1.3, 1.7, 0.8            # keo ra bien; tha; moi lan dung hinh 0,8 s
MA, MB, MC = TV / 8, TV / 6, TV / 4             # thoi gian chay (video) toi 5,66 / 4,0 / 0 cm
TA = REL + MA; TB = TA + FZ + (MB - MA); TC = TB + FZ + (MC - MB)
ROW_T = [P1 + 0.15, TA + 0.15, TB + 0.15, TC + 0.15]   # luc hien tung hang (vat da dung hinh dung vach)

def run_time(t):
    """Thoi gian chay tinh tren video (bo qua luc dung hinh)."""
    if t < REL: return 0.0
    if t < TA: return t - REL
    if t < TA + FZ: return MA
    if t < TB: return MA + (t - TA - FZ)
    if t < TB + FZ: return MB
    if t < TC: return MB + (t - TB - FZ)
    return MC

def vach_state(t):
    """-> (x cm, |v|/vmax, da tha, dang dung hinh). Mot nguon cho vat, cot nang luong, bang."""
    if t < REL:
        x = 8.0 * ease((t - P0) / (P1 - P0)); return x, 0.0, False, False
    m = run_time(t); ph = 2 * math.pi * m / TV
    frozen = (TA <= t < TA + FZ) or (TB <= t < TB + FZ) or t >= TC
    return 8.0 * math.cos(ph), math.sin(ph), True, frozen

CB0, CB1, CBX0, CBX1 = 1100, 690, 90, 240      # cot nang luong: day, dinh (= 0,128 J), x
def column(d, et, ed, x0=CBX0, x1=CBX1, yb=CB0, yt=CB1, wline=True, alpha=1.0):
    h = yb - yt
    d.rectangle([x0, yt, x1, yb], fill=A((248, 246, 240), alpha), outline=A(NAVY, alpha), width=3)
    ht = h * et / W_J; hd = h * ed / W_J
    if ht > 2: d.rectangle([x0 + 3, yb - ht, x1 - 3, yb - 2], fill=A(CET, alpha))
    if hd > 1: d.rectangle([x0 + 3, yb - ht - hd, x1 - 3, yb - ht], fill=A(CED, alpha))
    if wline:
        d.line([(x0 - 20, yt), (x1 + 20, yt)], fill=A(INK, alpha), width=4)

TX = [400, 580, 760, 940]; TY = [780, 860, 940, 1020]
def s_vach(img, d, t, sc):
    M = sc["M"]
    x, vf, rel, frozen = vach_state(t)
    rail(d, x, vfrac=vf if rel else 0.0)
    if t >= REL:                                  # nhan quay cham / dung hinh
        lab, col = ("dừng hình", PURPLE) if frozen else (f"quay chậm ×{SLOW}", ORANGE)
        pw = tw(d, lab, F(40)) + 48
        card(d, (1040 - pw, 616, 1040, 674), fill=col, r=29); text(d, (1040 - pw / 2, 645), lab, 40, WHITE)
    else:
        lab = "kéo tới A = 8,0 cm"
        pw = tw(d, lab, F(40)) + 48
        card(d, (1040 - pw, 616, 1040, 674), fill=NAVY, r=29); text(d, (1040 - pw / 2, 645), lab, 40, WHITE)
    et = et_of(x); ed = (W_J - et) if rel else 0.0
    column(d, et, ed, wline=t >= P1)
    if t >= P1: eq(d, CBX0 - 20, CB1 - 40, "W = 0,128 J", 40, INK, anchor="l")
    eq(d, CBX0 + 10, 1150, "E_{t}", 44, CET, anchor="l"); eq(d, CBX0 + 90, 1150, "E_{d}", 44, CED, anchor="l")
    # bang
    nr = sum(1 for rt in ROW_T if t >= rt)
    card(d, (300, 700, 1040, max(790, TY[max(nr, 1) - 1] + 45)), fill=WHITE, outline=NAVY, r=20, w=3)
    for cx, hd in zip(TX, ("x (cm)", "E_{t} (J)", "E_{d} (J)", "W (J)")): eq(d, cx, 735, hd, 40, INK)
    d.line([(310, 760), (1030, 760)], fill=NAVY, width=3)
    for i, (xl, xv, e1, e2) in enumerate(ROWS):
        if t < ROW_T[i]: continue
        ka = appear(t, ROW_T[i], 0.3)
        cur = frozen and abs(x - xv) < 0.02 or (i == 0 and P1 <= t < REL)
        if cur: d.rounded_rectangle([308, TY[i] - 34, 1032, TY[i] + 34], radius=12, fill=A((255, 237, 213), ka))
        for cx, v, col in zip(TX, (xl, e1, e2, "0,128"), (INK, CET, CED, INK)):
            text(d, (cx, TY[i]), v, 42, col, alpha=ka)
    card(d, (60, 1220, 1020, 1400), fill=(240, 244, 255), r=22)
    text(d, (W / 2, 1268), "k = 40 N/m · A = 8,0 cm", 42, INK)
    eq(d, W / 2, 1350, "E_{t} = ½kx^{2}     E_{d} = ½k(A^{2} − x^{2})", 42, INK)

# ---------------- canh: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · động năng gấp 3 thế năng"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 280, W / 2 + pw / 2, 344), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 312), lab, 42, WHITE, alpha=ka)
    x0, x1, yb, yt = 150, 360, 1060, 420          # cot lon tai x = 4,0 cm, chia 4 phan bang nhau
    column(d, et_of(4.0), W_J - et_of(4.0), x0, x1, yb, yt, wline=True)
    q = (yb - yt) / 4
    for j in (1, 2, 3):
        dashed(d, (x0 + 4, yb - j * q), (x1 - 4, yb - j * q), WHITE, w=4)
    text(d, ((x0 + x1) / 2, 380), "x = 4,0 cm", 40, INK)
    eq(d, 400, yb - q / 2, "E_{t} = 0,032 J", 46, CET, anchor="l")
    eq(d, 400, yt + 1.5 * q - 30, "E_{d} = 0,096 J", 46, CED, anchor="l")
    kr = appear(t, M[0] + 0.5, 0.4)
    if kr > 0: eq(d, 400, yt + 1.5 * q + 40, "= 3 × 0,032 J", 46, CED, alpha=kr, anchor="l")
    k2 = appear(t, M[0] + 1.2, 0.4)
    if k2 > 0:
        card(d, (60, 1120, 1020, 1240), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), r=20, w=3)
        eq(d, W / 2, 1180, "x: 8,0 → 4,0 cm thì E_{t}: 0,128 → 0,032 J", 40, ORANGE, alpha=k2)
    kn = appear(t, M[1] + 0.1, 0.4)
    if kn > 0:
        card(d, (60, 1290, 1020, 1430), fill=A((236, 253, 243), kn), outline=A(GREEN, kn), r=20, w=3)
        eq(d, W / 2, 1360, "W = E_{t} + E_{d} = 0,128 J", 50, DGREEN, alpha=kn)

# ---------------- canh: Bay roi Chua noi duoc ----------------
BT, BL0, BPX = 330, 260, 45                      # treo dung thu nho: dinh, dai chua dan, px/cm
BY0 = BT + BL0; BYE = BY0 + 4.9 * BPX
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k2)
    kf = appear(t, M[0] + 0.8, 0.4)               # cong thuc sai hien sau nhan
    kc = appear(t, M[0] + 2.8, 0.5)               # dau dung tre >= 2 s sau cong thuc
    stand(d, 170, BT, BYE + 160, 520)
    hang(d, 480, BT, BYE)
    dashed(d, (400, BY0), (720, BY0), mix(MUTED, DRED, a1), w=5)          # moc sai: cho chua dan
    text(d, (740, BY0), "chưa dãn", 40, DRED if a1 > 0.5 else MUTED, anchor="lm")
    d.line([(400, BYE), (720, BYE)], fill=mix(MUTED, GREEN, kc), width=5)   # VTCB (dung)
    text(d, (740, BYE), "VTCB", 40, DGREEN if kc > 0.5 else MUTED, anchor="lm")
    d.line([(700, BY0), (700, BYE)], fill=ORANGE, width=5)
    for yy in (BY0, BYE): d.line([(686, yy), (714, yy)], fill=ORANGE, width=5)
    eq(d, 740, (BY0 + BYE) / 2, "Δℓ = 4,9 cm", 40, ORANGE, anchor="l")
    if a1 > 0:
        y0 = 1000
        card(d, (40, y0, 1040, y0 + 440), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        text(d, (W / 2, y0 + 150), "Nếu treo thẳng đứng, mốc ở chỗ chưa dãn", 42, DRED, alpha=a1)
        yy = y0 + 250; s = "VTCB: E_{t} = ½k·Δℓ^{2} = 0,04802 J"
        lw = eq(d, W / 2, yy, s, 42, DRED, alpha=a1 * kf)
        if kc > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * kc, yy + 2)], fill=A((140, 15, 15), a1), width=6)
            eq(d, W / 2, y0 + 360, "✓ Mốc ở VTCB thì E_{t} = 0", 46, DGREEN, alpha=a1 * kc)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• E_{d} chỉ tính, chưa đo v", "• Ma sát: chưa xét")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            eq(d, 90, y0 + 190 + j * 120, l1, 46, INK, alpha=kk, anchor="l")

# ---------------- canh: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: li do nao Et = 3 Ed (dap so 6,93 cm khong hien); goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 500), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    eq(d, W / 2, 340, "Bỏ ma sát: W không đổi,", 50, GREEN, alpha=k0)
    eq(d, W / 2, 420, "E_{t} và E_{d} chỉ đổi chỗ.", 50, GREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 560, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 590, W / 2 + pw / 2, 654), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 622), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.9, 0.5)
    ctext(d, 760, "Vật ở li độ nào thì\nthế năng gấp 3 động năng?", 48, INK, maxw=920, alpha=kq)
    if kq > 0:                                    # cot: 3 phan Et, 1 phan Ed (dieu kien, khong phai dap so)
        x0, x1, yb, yt = 220, 360, 1180, 900
        q = (yb - yt) / 4
        d.rectangle([x0, yt, x1, yb], fill=A(CED, kq), outline=A(NAVY, kq), width=3)
        d.rectangle([x0 + 3, yb - 3 * q, x1 - 3, yb - 2], fill=A(CET, kq))
        for j in (1, 2): dashed(d, (x0 + 4, yb - j * q), (x1 - 4, yb - j * q), WHITE, w=4)
        eq(d, 390, yb - 1.5 * q, "E_{t}", 46, CET, alpha=kq, anchor="l")
        eq(d, 390, yt + q / 2, "E_{d}", 46, CED, alpha=kq, anchor="l")
        text(d, (760, 1040), "x = ? cm", 56, PURPLE, alpha=kq)
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    if kh > 0:
        card(d, (110, 1230, 970, 1390), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1272), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1340), "Tổng vẫn là 0,128 J", 44, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, dk, v, da, b, e = sc["hook"], sc["dok"], sc["vach"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (dk["t0"] + 0.1, "ding"), (dk["t0"] + H1, "tap"),
            (v["t0"] + REL, "tap")] + [(v["t0"] + tt, "tick") for tt in (TA, TB, TC)] + [
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]

CLIP = dict(id="tn-l11-conangdddh-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Cơ năng dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Con lắc lò xo nằm ngang", draw=s_hook, tail=0.8, caps=[
   ("Vật ở nửa biên độ.", 2.6),
   ("Tự đoán trước khi xem tiếp.", 5.6)]),
 dict(key="dok", title="Đo độ cứng", draw=s_dok, tail=0.6, caps=[
   ("Treo quả 200 g, đo độ dãn.", 3.4),
   ("Tính ra độ cứng k.", 2.6)]),
 dict(key="vach", title="Năng lượng ở từng vạch", draw=s_vach, caps=[
   ("Cùng lò xo, nằm ngang, thả từ biên.", 4.3),
   ("Thế năng giảm, động năng tăng bù.", 3.8)], tail=0.4),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Thế năng chỉ một phần tư.", 3.4),
   ("Mọi vạch: tổng vẫn như nhau.", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: mốc ở chỗ lò xo chưa dãn.", 4.6),
   ("Bảng chỉ minh hoạ, chưa phải đo.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 5.4)]),
])
