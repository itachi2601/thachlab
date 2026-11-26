# Clip: tn-l12-dttruong-01 - Nam cham qua ong day: tu truong bien thien sinh dien truong xoay (ban 2, 26/11/2026: khung mau xoaychieu2)
# So lieu nguyen tu content/thi-nghiem/tn-l12-dttruong-01.json:
#   so_lieu_mau: v = 0,25 ; 0,50 ; 1,00 m/s -> e = 75,5 ; 149,0 ; 298,0 mV ; nam yen giua ong -> 0,0 mV
#   mo_hinh: e = N.A.B0.v/L = 1000 . 4e-4 . 0,15 . v / 0,2 = 0,3.v (V)  (kiem bang assert)
# Du doan (hien_tuong_hay_sai[1]): "nam cham nam yen giua ong, noi B manh nhat, thi kim lech manh nhat" -> dap an 0,0 mV.
# Bay (hien_tuong_hay_sai[2]): "dien truong trong day do dien tich cua nam cham" -> sai: cung nam cham, yen 0 mV, chay 298 mV.
# Chua noi duoc (khong_chung_minh[1] + quan_sat[3] khong hien trong clip): hinh duong suc dien truong xoay; e luc ra khoi ong.
# Cau chot THU NGHI (ghi_chu kho): nam cham yen, keo ong len 0,40 m/s -> e lon nhat = 0,3.0,40 = 0,12 V = 120 mV.
# Vat li co che: nhin tu tren, N o duoi roi vao ong -> B trong ong huong XUONG va dang tang -> E xoay NGUOC chieu kim dong ho.
from engine import *

DGREEN = (21, 128, 61); DARK_OR = (181, 71, 8)
assert abs(1000 * 4e-4 * 0.15 / 0.2 - 0.3) < 1e-12
assert abs(0.3 * 0.40 * 1000 - 120) < 1e-9
NOTE = (70, 75, 95)
COP = (184, 115, 51)
ROWS = [(0.10, "0,10", 30.0, "30,0"), (0.25, "0,25", 75.5, "75,5"), (0.50, "0,50", 149.0, "149,0"),
        (0.75, "0,75", 224.0, "224,0"), (1.00, "1,00", 298.0, "298,0")]

# Faraday: lay phap tuyen n = +z (ve phia nguoi nhin tu tren). B = -z, do lon tang -> Phi = B.n.A giam (am hon)
# -> lien hoan E.dl theo chieu duong (nguoc kim dong ho nhin tu +z) = -dPhi/dt > 0 -> E nguoc chieu kim dong ho.
_dPhi = (-1.0) * (+1.0)            # dB_z/dt * n_z : B_z = -|B|, |B| tang -> dB_z/dt < 0
assert -_dPhi > 0                  # lien hoan duong -> CCW nhin tu tren

# ---------------- bo cuc ong day dung ----------------
CX = 300                           # truc ong
CT, CB = 560, 890                  # dau tren / duoi cuon day (20 cm)
CRX, CRY, NT = 92, 16, 12
ML, MW = 170, 64                   # nam cham: dai, rong
YMID = (CT + CB) / 2

def _trace(ang, ml, inset=10):
    """Duong suc ngoai nam cham (toa do cuc bo: x doc truc, N o x = 0 phia +, S o x = -ml). Ra o N, vao o S."""
    nx, sx = -inset, -ml + inset
    x, y = nx + 6 * math.cos(ang), -6 * math.sin(ang); pts = [(x, y)]
    for _ in range(4000):
        ex = ey = 0.0
        for px, q in ((nx, 1), (sx, -1)):
            dx, dy = x - px, y; r3 = (dx * dx + dy * dy) ** 1.5; ex += q * dx / r3; ey += q * dy / r3
        n = math.hypot(ex, ey); x += 3 * ex / n; y += 3 * ey / n; pts.append((x, y))
        if math.hypot(x - sx, y) < 8: break
    return pts
_RAW = [_trace(math.radians(a), ML) for a in (60, 82, 104)]
_SQ = 150 / max(-y for _, y in _RAW[0])
FIELD = [[(x, y * _SQ) for x, y in ln] for ln in _RAW]

def dashed_poly(d, pts, color, w=4, seg=10, gap=8):
    acc, on, cur = 0.0, True, [pts[0]]
    for p, q in zip(pts, pts[1:]):
        acc += math.dist(p, q); cur.append(q)
        if acc >= (seg if on else gap):
            if on and len(cur) > 1: d.line(cur, fill=color, width=w)
            on, acc, cur = not on, 0.0, [q]
    if on and len(cur) > 1: d.line(cur, fill=color, width=w)

def chevron(d, x, y, ang, color, s=16, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def field(d, ny, alpha=1.0, cx=CX):
    """Nam cham dung, cuc N o duoi (dau N tai y = ny), S o tren (y = ny - ML).
    Diem cuc bo (x, w), x <= 0 la phia S -> man hinh (cx + w, ny + x): S nam TREN N, duong suc vong tu N len S.
    (Ban 14/11 dung ny - x -> cuc S ao nam duoi N, duong suc bo quanh dau duoi: sai hinh dang, sua 18/11.)"""
    if alpha <= 0: return
    c = A(PURPLE, 0.5 * alpha)
    for ln in FIELD:
        for sg in (1, -1):
            pts = [(cx + sg * w, ny + x) for x, w in ln]
            dashed_poly(d, pts, c)
            k = max(range(len(pts)), key=lambda n: abs(pts[n][0] - cx))   # diem xa truc nhat: mui ten N -> S (di len)
            (x0, y0), (x1, y1) = pts[max(0, k - 3)], pts[min(len(pts) - 1, k + 3)]
            chevron(d, pts[k][0], pts[k][1], math.atan2(y1 - y0, x1 - x0), c)
    d.line([(cx, ny + 6), (cx, ny + 110)], fill=c, width=4); chevron(d, cx, ny + 110, math.pi / 2, c)   # ra khoi N (xuong)
    ys = ny - ML
    d.line([(cx, ys - 80), (cx, ys - 6)], fill=c, width=4); chevron(d, cx, ys - 30, math.pi / 2, c)     # vao S (xuong)

def magnet(d, ny, cx=CX, s=1.0):
    """Nam cham dung: S (xanh) tren, N (do) duoi; ny = toa do dau N."""
    ml, mw = ML * s, MW * s; y0, ym = ny - ml, ny - ml / 2
    d.rounded_rectangle([cx - mw / 2, y0, cx + mw / 2, ym], radius=10, fill=BLUE)
    d.rounded_rectangle([cx - mw / 2, ym, cx + mw / 2, ny], radius=10, fill=RED)
    d.rectangle([cx - mw / 2, ym - 10, cx + mw / 2, ym + 10], fill=RED)
    d.rectangle([cx - mw / 2, ym - 10, cx + mw / 2, ym], fill=BLUE)
    if s < 1: return                                   # nam cham thu nho: chi giu hai mau (chu vo, bi vong day cat)
    for yy, ch in ((y0 + ml / 4, "S"), (ny - ml / 4, "N")):
        if not (CT - 40 < yy < CB + 40): text(d, (cx, yy), ch, 56, WHITE)   # trong cuon day: bo chu (vong truoc cat chu)

def turns(ct=CT, cb=CB): return [ct + j * (cb - ct) / (NT - 1) for j in range(NT)]
def coil_back(d, cx=CX, ct=CT, cb=CB, rx=CRX):
    for y in turns(ct, cb): d.arc([cx - rx, y - CRY, cx + rx, y + CRY], 180, 360, fill=mix(COP, BG, 0.45), width=6)
def coil_front(d, cx=CX, ct=CT, cb=CB, rx=CRX):
    for y in turns(ct, cb): d.arc([cx - rx, y - CRY, cx + rx, y + CRY], 0, 180, fill=COP, width=8)

ROWS = [(0.25, "0,25", 75.5, "75,5"), (0.50, "0,50", 149.0, "149,0"), (1.00, "1,00", 298.0, "298,0")]
for v, _, e, _ in ROWS: assert abs(e - 300 * v) / (300 * v) < 0.01

def tube(d):
    for x in (CX - 46, CX + 46): d.line([(x, 330), (x, 1000)], fill=A(GRAY, 0.55), width=3)

def wires(d):
    d.line([(CX + CRX, CT), (440, CT), (440, 500), (600, 500)], fill=NAVY, width=5)
    d.line([(CX + CRX, CB), (500, CB), (500, 720), (600, 720)], fill=NAVY, width=5)

def meter(d, val, vtxt=""):
    card(d, (580, 400, 1030, 790), fill=WHITE, outline=NAVY, r=26, w=5)
    text(d, (805, 455), "e lớn nhất", 56, NOTE)
    d.rounded_rectangle([610, 505, 1000, 635], radius=14, fill=NAVY)
    text(d, (805, 570), f"{val} mV", 64, (134, 239, 172))
    if vtxt: text(d, (805, 715), vtxt, 56, TEAL)

def rig(d, ny, val, vtxt="", hold=False, dims=True):
    field(d, ny)
    tube(d); coil_back(d)
    if hold: d.line([(CX, 300), (CX, ny - ML)], fill=NAVY, width=6)
    magnet(d, ny)
    coil_front(d); wires(d)
    meter(d, val, vtxt)
    text(d, (805, 860), "1000 vòng", 56, NOTE)
    if dims: text(d, (805, 930), "dài 20 cm", 56, NOTE)

# ---------------- do thi e theo v ----------------
def graph(d, box, gy0, pxe, npt, rest=False, line=0.0, hl=0.0, rest_lab=0.0):
    gx0, pxv = 190, 760
    gp = lambda v, e: (gx0 + v * pxv, gy0 - e * pxe)
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    top = gy0 - 320 * pxe
    d.line([(gx0, gy0), (gx0 + 1.1 * pxv, gy0)], fill=NAVY, width=4)
    d.line([(gx0, gy0), (gx0, top)], fill=NAVY, width=4)
    chevron(d, gx0 + 1.1 * pxv, gy0, 0, NAVY, 18, 4); chevron(d, gx0, top, -math.pi / 2, NAVY, 18, 4)
    for v, s in ((0.5, "0,5"), (1.0, "1,0")):
        x, _ = gp(v, 0); d.line([(x, gy0 - 8), (x, gy0 + 8)], fill=NAVY, width=3)
        text(d, (x, gy0 + 42), s, 56, NOTE, bold=False)
    for e in (100, 200, 300):
        _, y = gp(0, e); d.line([(gx0 - 8, y), (gx0 + 8, y)], fill=NAVY, width=3)
        text(d, (gx0 - 18, y), str(e), 56, NOTE, bold=False, anchor="rm")
    text(d, (gx0 + 26, top + 10), "e (mV)", 56, INK, anchor="lm")
    text(d, (1020, gy0 - 44), "v (m/s)", 56, INK, anchor="rm")
    if line > 0:
        x1, y1 = gp(1.04 * line, 300 * 1.04 * line)
        d.line([gp(0, 0), (x1, y1)], fill=A(ORANGE, 0.5), width=5)
    if hl > 0:
        for v, e, s in ((0.25, 75.5, "75,5"), (0.5, 149.0, "149,0")):
            x, y = gp(v, e)
            for k in range(0, int(x - gx0), 22): d.line([(gx0 + k, y), (gx0 + k + 11, y)], fill=A(ORANGE, hl), width=3)
            if v < 0.3: text(d, (x - 24, y - 34), s, 56, ORANGE, anchor="rm", alpha=hl)
            else: text(d, (x + 24, y + 30), s, 56, ORANGE, anchor="lm", alpha=hl)
    for r in ROWS[:npt]:
        x, y = gp(r[0], r[2]); dot(d, x, y, 14, ORANGE)
    if rest:
        dot(d, gx0, gy0, 17, GREEN)
        if rest_lab > 0: text(d, (gx0 + 30, gy0 - 50), "nằm yên: 0", 56, GREEN, anchor="lm", alpha=rest_lab)

# ---------------- canh 1: Du doan ----------------
NY_TOP = 520
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, NY_TOP + 10 * math.sin(2.4 * t), "0,0", dims=False)
    M = sc["M"]; a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    gy = YMID + ML / 2                                     # nam cham "ma" net dut: vi tri giua ong cua cau hoi
    for x0_, y0_, x1_, y1_ in ((CX - MW / 2, gy - ML, CX + MW / 2, gy - ML), (CX - MW / 2, gy, CX + MW / 2, gy),
                               (CX - MW / 2, gy - ML, CX - MW / 2, gy), (CX + MW / 2, gy - ML, CX + MW / 2, gy)):
        dashed_poly(d, [(x0_, y0_), (x1_, y1_)], A(PURPLE, 0.8 * a), w=4, seg=12, gap=8)
    y0 = 1060 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 180), "Nam châm yên giữa ống", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 260), "(B mạnh nhất):", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 340), "đồng hồ chỉ?", 60, PURPLE, alpha=a)
    tc, te = M[1] + 0.3, sc["T"] - 0.1
    p = clamp((t - tc) / (te - tc))
    d.rounded_rectangle([110, y0 + 395, 970, y0 + 495], radius=24, fill=A(LIGHT, a))
    if p < 1: d.rounded_rectangle([110, y0 + 395, 110 + 860 * (1 - p), y0 + 495], radius=24, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
DUR = {0.25: 2.0, 0.50: 1.0, 1.00: 0.5}           # thoi gian qua khung ti le nghich v
NY0, NY1 = 380, 1100
NY_IN = CT + 10
GAP = 0.3
YMID = (CT + CB) / 2
def drops(sc):
    s = sc["M"][0] + 0.6; out = []
    for r in ROWS:
        out.append((s, s + DUR[r[0]], r)); s += DUR[r[0]] + GAP
    return out
def t_rest(sc): return sc["M"][1] + 0.3

def state_do(t, sc):
    ds = drops(sc); ny, val, vt, npt, rest = NY0, "0,0", "", 0, False
    for j, (a, b, r) in enumerate(ds):
        if t < a: break
        u = clamp((t - a) / (b - a)); ny = lerp(NY0, NY1, u); vt = f"v = {r[1]} m/s"
        if ny >= NY_IN: val, npt = r[3], j + 1
        else: val, npt = "0,0", j
        if t >= b: ny, val, npt = NY1 + 999, r[3], j + 1
    if t >= t_rest(sc):
        ny, val, vt, rest = YMID + ML / 2, "0,0", "v = 0", True
    return ny, val, vt, npt, rest

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    ny, val, vt, npt, rest = state_do(t, sc)
    rig(d, ny, val, vt, hold=rest)
    graph(d, (40, 1030, 1040, 1588), 1460, 1.15, npt, rest=rest)
    text(d, (1010, 1075), "minh hoạ", 56, NOTE, bold=False, anchor="rm")

# ---------------- canh 3: Dap an + co che ----------------
def ring_view(d, k, cx=250, cy=1290):
    for r, n in ((95, 3), (205, 4)):
        c = A(TEAL, k)
        pts = [(cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))) for a in range(0, 361, 3)]
        dashed_poly(d, pts, c, w=5, seg=16, gap=10)
        for j in range(n):
            th = math.radians(90 + j * 360 / n)
            x, y = cx + r * math.cos(th), cy - r * math.sin(th)
            arrow(d, (x + 22 * math.sin(th), y + 22 * math.cos(th)), (x - 22 * math.sin(th), y - 22 * math.cos(th)), c, w=5, head=18)
    d.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], outline=A(COP, k), width=12)
    for x, y in ((cx - 45, cy - 45), (cx + 45, cy - 45), (cx - 45, cy + 45), (cx + 45, cy + 45)):
        d.ellipse([x - 16, y - 16, x + 16, y + 16], outline=A(PURPLE, k), width=4)
        d.line([(x - 10, y - 10), (x + 10, y + 10)], fill=A(PURPLE, k), width=4); d.line([(x - 10, y + 10), (x + 10, y - 10)], fill=A(PURPLE, k), width=4)

def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    s = "ĐÁP ÁN: 0,0 mV"; pw = tw(d, s, F(56)) + 70                    # hien ngay tu 0 s
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 340), fill=GREEN, r=39)
    text(d, (W / 2, 301), s, 56, WHITE)
    graph(d, (40, 370, 1040, 1000), 880, 1.3, 3, rest=True, line=clamp((t - M[1] + 0.1) / 0.8),
          hl=appear(t, M[1] - 0.1, 0.4), rest_lab=1.0)
    k = appear(t, M[2] - 0.1, 0.5)
    card(d, (40, 1030, 1040, 1588), fill=A(WHITE, k), outline=A(TEAL, k), w=5)
    if k <= 0: return
    ring_view(d, k)
    text(d, (500, 1100), "từ trên xuống:", 56, NOTE, anchor="lm", alpha=k)
    text(d, (500, 1180), "B xuống, tăng", 56, PURPLE, anchor="lm", alpha=k)
    k2 = k
    text(d, (500, 1300), "mũi tên: chiều E", 56, TEAL, anchor="lm", alpha=k2)
    text(d, (500, 1380), "E khép kín", 56, TEAL, anchor="lm", alpha=k2)
    text(d, (500, 1490), "electron: ngược E", 56, NOTE, anchor="lm", alpha=k2)

# ---------------- canh 4: Bay ----------------
def mini(d, cx, ny, val, moving, k):
    ct, cb = 860, 1080
    coil_back(d, cx, ct, cb, 70)
    if not moving: d.line([(cx, 760), (cx, ny - ML * 0.7)], fill=A(NAVY, k), width=5)
    magnet(d, ny, cx, 0.7)
    coil_front(d, cx, ct, cb, 70)
    if moving: arrow(d, (cx + 110, 880), (cx + 110, 1040), A(TEAL, k), w=7, head=22)
    d.rounded_rectangle([cx - 190, 1150, cx + 190, 1260], radius=14, fill=A(NAVY, k))
    text(d, (cx, 1205), f"{val} mV", 60, (134, 239, 172), alpha=k)
    text(d, (cx, 1320), "yên" if not moving else "v = 1,0 m/s", 56, NOTE, alpha=k)

def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    b1, b2, b3 = (m - 0.1 for m in sc["M"])
    k2, k3 = appear(t, b2, 0.4), appear(t, b3, 0.4)
    card(d, (40, 262, 1040, 620), outline=RED, w=5)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 282, W / 2 + pw / 2, 358), fill=RED, r=38)
    text(d, (W / 2, 320), "BẪY", 56, WHITE)
    ks = clamp((t - b3) / 0.4)
    for j, q in enumerate(("“Điện tích của nam châm", "đẩy electron trong dây”")):
        yy = 445 + 85 * j
        text(d, (W / 2, yy), q, 60, mix(INK, GRAY, 0.45 * ks))
        if ks > 0:
            lw = tw(d, q, F(60))
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=6)
    if k3 > 0:
        pw2 = tw(d, "SAI", F(56)) + 50
        card(d, (1020 - pw2, 282, 1020, 358), fill=A((127, 29, 29), k3), r=38)
        text(d, (1020 - pw2 / 2, 320), "SAI", 56, WHITE, alpha=k3)
    card(d, (40, 650, 1040, 1380), fill=A(WHITE, k2), outline=A(LIGHT, k2), w=3)
    if k2 > 0:
        mini(d, 290, 1000 + 60, "0,0", False, k2)
        u = ((t - b2) / 0.7) % 1.0
        mini(d, 790, lerp(800, 1180, u), "298,0", True, k2)
    if k3 > 0:
        card(d, (40, 1410, 1040, 1588), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1499), "Nguồn là B đang đổi", 60, DGREEN, alpha=k3)

# ---------------- canh 5: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1000), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Hình E xoáy: chưa đo", "• e lúc ra khỏi ống?")):
        text(d, (100, 520 + j * 240), s, 64, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 650), "?", 180, NAVY, alpha=k * (1 - kb))

# ---------------- canh 6: THU NGHI (cau_chot; dap an KHONG hien) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.3, 0.5)
    card(d, (40, 260, 1040, 1200), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 285, W / 2 + pw / 2, 365), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 325), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 450), "Nam châm đứng yên,", 60, INK, alpha=k)
    text(d, (W / 2, 535), "kéo ống lên 0,40 m/s.", 60, INK, alpha=k)
    text(d, (W / 2, 620), "e lớn nhất = ? mV", 60, DARK_OR, alpha=k)
    cx = 540; off = -40 * ((t * 0.5) % 1.0)
    coil_back(d, cx, 820 + off, 1040 + off, 80)
    d.line([(cx, 700), (cx, 990 - ML * 0.7)], fill=A(NAVY, k), width=5)
    magnet(d, 990, cx, 0.7)
    coil_front(d, cx, 820 + off, 1040 + off, 80)
    arrow(d, (720, 1110), (720, 840), A(TEAL, k), w=8, head=24)
    kh = appear(t, 3.3, 0.5)
    if kh > 0:
        card(d, (90, 1240, 990, 1390), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1315), "Gợi ý: v tương đối", 60, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, g, e = (sc[k] for k in ("hook", "do", "ans", "bay", "gioi", "end"))
    return ([(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + a, "tap") for a, _, _ in drops(do)] + [(do["t0"] + t_rest(do), "tap")]
            + [(an["t0"] + 0.1, "ding"), (an["t0"] + an["M"][2] - 0.1, "tap"),
               (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
               (g["t0"] + 2.4, "tap"), (e["t0"] + 0.3, "open")])

CLIP = dict(id="tn-l12-dttruong-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Điện từ trường · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nam châm và ống dây", draw=s_hook, tail=0.3, caps=[
   ("Ống dây nối đồng hồ số.", 3.0),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cho nam châm qua, v tăng dần.", 4.4),
   ("Rồi giữ yên giữa ống.", 3.6)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("Nằm yên: không có e.", 3.0),
   ("v gấp đôi, e gấp đôi.", 3.0),
   ("B đổi sinh điện trường xoáy.", 3.2)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("Cùng một nam châm.", 3.0),
   ("Chỉ khi chạy mới có e.", 3.0)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Chưa trả lời được:", 4.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 6.6)]),
])
