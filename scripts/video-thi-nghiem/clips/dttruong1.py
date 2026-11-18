# Clip: tn-l12-dttruong-01 - Nam cham qua ong day: tu truong bien thien sinh dien truong xoay (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-dttruong-01.json:
#   so_lieu_mau: v = 0,10 ; 0,25 ; 0,50 ; 0,75 ; 1,00 m/s -> e = 30,0 ; 75,5 ; 149,0 ; 224,0 ; 298,0 mV ; nam yen -> 0,0
#   dung_cu/tham_so: ong day 1000 vong, dai 20 cm ; dong ho giu so lon nhat (sai_so_thuong_gap: "luu gia tri lon nhat").
# Bo cuc KHAC udcamung1 (cung nam cham - cuon day): ong day DUNG, nam cham roi tu tren, dong ho so; truc chinh la
#   do thi e theo v (5 diem + diem nam yen); udcamung1 dung cuon nam ngang + tai nghe/loa + do thi e(t).
# Du doan (khung ben canh, K10 khong ve nut A-D trong mp4):
#   "Nam cham qua ong voi v = 0,25 m/s roi 0,50 m/s. Suat dien dong lon nhat e thay doi the nao?"
#   A. Gan nhu khong doi   B. Tang gan gap doi (DUNG: 75,5 -> 149,0 mV)   C. Tang gan gap bon   D. Giam con mot nua
#   (nhieu: A = "tu thong doi bao nhieu cung vay"; C = nham theo v binh phuong / dong nang; D = "qua nhanh, it thoi gian")
# Bay (hien_tuong_hay_sai[2], doi 14/11 de khong trung phuong an B cau Tu kiem tra sau hop): "dien truong trong day do
#   dien tich cua nam cham gay ra" -> sai: nam cham dung yen e = 0,0 mV -> nguon la B dang doi.
# Chua noi duoc (khong_chung_minh[1], viet lai tranh trung phuong an D): dien truong quanh ong trong ra sao -> dong ho chi cho mot so e.
#   (khong_chung_minh[0] noi ve KIM dien ke; clip dung dong ho so nen khong dung y nay.)
# Cau chot: "B doi cang nhanh, e cang lon" (tranh trung phuong an C).
# Ca chot cho ghi_chu kho: "Ong di len 0,40 m/s qua nam cham dung yen -> e lon nhat khoang 120 mV".
# Cau chot THU NGHI (ca moi, so moi 0,40 m/s chua hien tren man; khong hien "300 mV moi 1 m/s" de khong la mot phep nhan):
#   "Giu nam cham yen, keo ong day len qua no voi 0,40 m/s. e lon nhat khoang bao nhieu?"
#   -> chuyen dong tuong doi nhu nhau -> doc giua 75,5 va 149,0 tren do thi: khoang 120 mV (mo hinh e = 0,3.v V).
#   goi_y: trung tinh "Xem lai do thi".
# Vat li co che (kiem bang assert duoi): nhin tu tren xuong, N o duoi roi vao ong -> B trong ong huong XUONG (ra xa
#   nguoi nhin) va dang tang -> dien truong xoay chay NGUOC chieu kim dong ho (nhin tu tren).
from engine import *

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
CT, CB = 470, 800                  # dau tren / duoi cuon day (20 cm)
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
    d.line([(cx, ys - 110), (cx, ys - 6)], fill=c, width=4); chevron(d, cx, ys - 40, math.pi / 2, c)     # vao S (xuong)

def magnet(d, ny, cx=CX, s=1.0):
    """Nam cham dung: S (xanh) tren, N (do) duoi; ny = toa do dau N."""
    ml, mw = ML * s, MW * s; y0, ym = ny - ml, ny - ml / 2
    d.rounded_rectangle([cx - mw / 2, y0, cx + mw / 2, ym], radius=10, fill=BLUE)
    d.rounded_rectangle([cx - mw / 2, ym, cx + mw / 2, ny], radius=10, fill=RED)
    d.rectangle([cx - mw / 2, ym - 10, cx + mw / 2, ym + 10], fill=RED)
    d.rectangle([cx - mw / 2, ym - 10, cx + mw / 2, ym], fill=BLUE)
    if s < 1: return                                   # nam cham thu nho: chi giu hai mau (chu vo, bi vong day cat)
    for yy, ch in ((y0 + ml / 4, "S"), (ny - ml / 4, "N")):
        if not (CT - 40 < yy < CB + 40): text(d, (cx, yy), ch, 44, WHITE)   # trong cuon day: bo chu (vong truoc cat chu)

def turns(ct=CT, cb=CB): return [ct + j * (cb - ct) / (NT - 1) for j in range(NT)]
def coil_back(d, cx=CX, ct=CT, cb=CB, rx=CRX):
    for y in turns(ct, cb): d.arc([cx - rx, y - CRY, cx + rx, y + CRY], 180, 360, fill=mix(COP, BG, 0.45), width=6)
def coil_front(d, cx=CX, ct=CT, cb=CB, rx=CRX):
    for y in turns(ct, cb): d.arc([cx - rx, y - CRY, cx + rx, y + CRY], 0, 180, fill=COP, width=8)

def tube(d):
    for x in (CX - 46, CX + 46): d.line([(x, 300), (x, 980)], fill=A(GRAY, 0.55), width=3)

def wires(d):
    d.line([(CX + CRX, CT), (440, CT), (440, 420), (600, 420)], fill=NAVY, width=5)
    d.line([(CX + CRX, CB), (500, CB), (500, 640), (600, 640)], fill=NAVY, width=5)

def meter(d, val, vtxt=""):
    card(d, (580, 330, 1030, 720), fill=WHITE, outline=NAVY, r=26, w=5)
    text(d, (805, 385), "e lớn nhất", 44, NOTE)
    d.rounded_rectangle([610, 430, 1000, 560], radius=14, fill=NAVY)
    text(d, (805, 495), f"{val} mV", 64, (134, 239, 172))
    if vtxt: text(d, (805, 640), vtxt, 46, TEAL)

def rig(d, ny, val, vtxt="", hold=False):
    field(d, ny)
    tube(d); coil_back(d)
    if hold: d.line([(CX, 280), (CX, ny - ML)], fill=NAVY, width=6)          # que giu nam cham
    magnet(d, ny)
    coil_front(d); wires(d)
    meter(d, val, vtxt)
    text(d, (805, 790), "ống dây 1000 vòng", 44, NOTE)
    text(d, (805, 850), "dài 20 cm", 44, NOTE)

# ---------------- do thi e theo v ----------------
GX0, GY0, PXV, PXE = 190, 1540, 760, 1.5        # goc O; px moi m/s; px moi mV
def gp(v, e): return GX0 + v * PXV, GY0 - e * PXE
def graph(d, npt, rest=False, line=0.0, hl=False, alpha=1.0):
    card(d, (40, 1000, 1040, 1665), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    d.line([(GX0, GY0), (GX0 + 1.08 * PXV, GY0)], fill=A(NAVY, alpha), width=4)
    d.line([(GX0, GY0), (GX0, GY0 - 330 * PXE)], fill=A(NAVY, alpha), width=4)
    chevron(d, GX0 + 1.08 * PXV, GY0, 0, A(NAVY, alpha), 18, 4); chevron(d, GX0, GY0 - 330 * PXE, -math.pi / 2, A(NAVY, alpha), 18, 4)
    for v, s in ((0.25, "0,25"), (0.5, "0,50"), (0.75, "0,75"), (1.0, "1,00")):
        x, _ = gp(v, 0); d.line([(x, GY0 - 8), (x, GY0 + 8)], fill=A(NAVY, alpha), width=3)
        text(d, (x, GY0 + 42), s, 40, NOTE, bold=False, alpha=alpha)
    for e in (100, 200, 300):
        _, y = gp(0, e); d.line([(GX0 - 8, y), (GX0 + 8, y)], fill=A(NAVY, alpha), width=3)
        text(d, (GX0 - 18, y), str(e), 40, NOTE, bold=False, anchor="rm", alpha=alpha)
    text(d, (GX0 + 22, 1052), "e (mV)", 42, INK, anchor="lm", alpha=alpha)
    text(d, (1020, GY0 - 40), "v (m/s)", 42, INK, anchor="rm", alpha=alpha)
    text(d, (GX0 - 18, GY0 + 42), "0", 40, NOTE, bold=False, anchor="rm", alpha=alpha)
    if line > 0:
        x1, y1 = gp(1.0 * line, 298.0 * line)
        d.line([gp(0, 0), (x1, y1)], fill=A(ORANGE, 0.55 * alpha), width=5)
    if hl:
        for v, s in ((0.25, "75,5"), (0.5, "149,0")):
            x, y = gp(v, dict((r[0], r[2]) for r in ROWS)[v])
            for k in range(0, int(x - GX0), 22): d.line([(GX0 + k, y), (GX0 + k + 11, y)], fill=A(ORANGE, alpha), width=3)
            text(d, (x + 22, y + 26), s + " mV", 42, ORANGE, anchor="lm", alpha=alpha)
    for r in ROWS[:npt]:
        x, y = gp(r[0], r[2]); dot(d, x, y, 13, A(ORANGE, alpha))
    if rest:
        dot(d, GX0, GY0, 15, A(GREEN, alpha))

# ---------------- canh 1: Du doan ----------------
NY_TOP = 360                                   # dau N luc cam o tren ong
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, NY_TOP, "0,0")
    a = appear(t, M[0] + 1.6, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(42)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", 42, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Nam châm qua ống với v = 0,25 m/s,", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 235), "rồi 0,50 m/s.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 320), "Số e lớn nhất thay đổi thế nào?", 48, INK, alpha=a)
    text(d, (W / 2, y0 + 410), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = M[0] + 2.0, sc["T"] - 0.15
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 490, 940, y0 + 504], radius=7, fill=A(LIGHT, a))
        if p < 1: d.rounded_rectangle([140, y0 + 490, 140 + 800 * (1 - p), y0 + 504], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
DUR = {0.10: 2.4, 0.25: 2.0, 0.50: 1.0, 0.75: 0.67, 1.00: 0.5}       # thoi gian hinh ti le nghich v (0,25/0,50 dung 2:1); 0,10 m/s: rut ngan, KHONG dung ti le (dung ra 5 s)
NY0, NY1 = 300, 1010                                                  # dau N: tu tren ong -> ra khoi day ong
NY_IN = CT + 10                                                       # dau N cham mieng tren cuon -> dong ho nhay so
GAP = 0.25
def drops(sc):
    s = sc["M"][0] + 1.0; out = []
    for r in ROWS:
        out.append((s, s + DUR[r[0]], r)); s += DUR[r[0]] + GAP
    return out
def t_rest(sc): return sc["M"][1] + 0.3

def state_do(t, sc):
    """(ny, so dong ho, nhan v, so diem tren do thi, nam yen?) dong bo tu mot ham."""
    ds = drops(sc); ny, val, vt, npt, rest = NY0, "0,0", "", 0, False
    for j, (a, b, r) in enumerate(ds):
        if t < a: break
        u = clamp((t - a) / (b - a)); ny = lerp(NY0, NY1, u); vt = f"v = {r[1]} m/s"
        if ny >= NY_IN: val, npt = r[3], j + 1          # dau N vao cuon: so dinh hien, diem len do thi CUNG luc
        else: val, npt = "0,0", j
        if t >= b: ny, val, npt = NY1 + 999, r[3], j + 1   # nam cham da ra khoi khung hinh, dong ho giu so lon nhat
    tr = t_rest(sc)
    if t >= tr:
        ny, val, vt, rest = YMID + ML / 2, "0,0", "v = 0", True
    return ny, val, vt, npt, rest

def s_do(img, d, t, sc):
    ny, val, vt, npt, rest = state_do(t, sc)
    rig(d, ny, val, vt, hold=rest)
    graph(d, npt, rest=rest)

# ---------------- canh 3: Dap an + Rut ra ----------------
def ring_view(d, k):
    """Nhin tu tren xuong: vong day, B huong xuong (dau x) dang tang, duong suc dien truong xoay khep kin (CCW)."""
    cx, cy = 260, 600
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

def s_dapan(img, d, t, sc):
    M = sc["M"]
    graph(d, 5, rest=True, line=clamp((t - 0.3) / 1.0), hl=t > M[0] + 0.6)
    kb = appear(t, M[0] + 1.6, 0.4)
    if kb > 0:
        s = "ĐÁP ÁN · tăng gần gấp đôi"; pw = tw(d, s, F(44)) + 60
        card(d, (W / 2 - pw / 2, 880, W / 2 + pw / 2, 952), fill=A(NAVY, kb), r=36)
        text(d, (W / 2, 916), s, 44, WHITE, alpha=kb)
    k = appear(t, M[0] + 0.8, 0.5)
    if k > 0:
        card(d, (40, 300, 1040, 850), fill=A(WHITE, k), outline=A(TEAL, k), w=5)
        ring_view(d, k)
        text(d, (520, 360), "nhìn từ trên xuống", 42, NOTE, anchor="lm", alpha=k)
        text(d, (520, 470), "B hướng xuống,", 44, PURPLE, anchor="lm", alpha=k)
        text(d, (520, 530), "đang tăng", 44, PURPLE, anchor="lm", alpha=k)
        k2 = appear(t, M[1] + 0.2, 0.5)
        text(d, (520, 640), "Điện trường xoáy:", 44, TEAL, anchor="lm", alpha=k2)
        text(d, (520, 700), "khép kín quanh vùng B đổi", 42, TEAL, anchor="lm", alpha=k2)
        text(d, (520, 780), "đẩy electron", 42, NOTE, anchor="lm", alpha=k2)

# ---------------- canh 4: Bay + Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.4)
    mk = M[0] + 2.4; ks = clamp((t - mk) / 0.4); kc = appear(t, mk + 0.25, 0.45)
    y = 300; h = 330 + 330 * kc
    card(d, (40, y, 1040, y + h), fill=A(WHITE, k0), outline=A(RED, k0), w=6)
    pw = tw(d, "BẪY", F(42)) + 52
    card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 94), fill=A(RED, k0), r=32)
    text(d, (W / 2, y + 61), "BẪY", 42, WHITE, alpha=k0)
    q = ["“Điện trường trong dây do", "điện tích nam châm gây ra”"]
    for j, s in enumerate(q):
        yy = y + 170 + j * 66; lw = tw(d, s, F(46))
        text(d, (W / 2, yy), s, 46, mix(INK, GRAY, ks), alpha=k0)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=5)
    if ks > 0.99: text(d, (W / 2 + tw(d, q[1], F(46)) / 2 + 40, y + 236), "✗", 50, RED)
    if kc > 0.95:
        cx, ct, cb = 230, 700, 900
        coil_back(d, cx, ct, cb, 70)
        d.line([(cx, 650), (cx, (ct + cb) / 2 - 60)], fill=A(NAVY, kc), width=5)
        magnet(d, (ct + cb) / 2 + 60, cx, 0.7)
        coil_front(d, cx, ct, cb, 70)
        text(d, (400, 730), "Đứng yên: e = 0,0 mV", 46, GREEN, anchor="lm")
        text(d, (400, 820), "→ nguồn là B đang đổi", 46, PURPLE, anchor="lm")
    k1 = appear(t, M[1], 0.45)
    if k1 > 0:
        yb = 1080
        card(d, (40, yb, 1040, yb + 330), fill=A(WHITE, k1), outline=A(NOTE, k1), w=5)
        pw = tw(d, "CHƯA NÓI ĐƯỢC", F(42)) + 52
        card(d, (W / 2 - pw / 2, yb + 28, W / 2 + pw / 2, yb + 94), fill=A(NOTE, k1), r=32)
        text(d, (W / 2, yb + 61), "CHƯA NÓI ĐƯỢC", 42, WHITE, alpha=k1)
        text(d, (W / 2, yb + 170), "Điện trường quanh ống trông ra sao?", 44, INK, alpha=k1)
        text(d, (W / 2, yb + 250), "Đồng hồ chỉ cho số e", 44, NOTE, alpha=k1)

# ---------------- canh 5: Chot ----------------
def _end_body(d, t, k):
    cx, ct, cb = 540, 1000, 1180
    coil_back(d, cx, ct, cb, 70)
    magnet(d, (ct + cb) / 2 + 55, cx, 0.65)
    coil_front(d, cx, ct, cb, 70)
    arrow(d, (700, 1200), (700, 990), A(TEAL, k), w=7, head=20)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot2(d, t, sc, "B đổi càng nhanh, e càng lớn",
          "Giữ nam châm yên, kéo ống lên qua nó với 0,40 m/s. e lớn nhất khoảng?", "Xem lại đồ thị", _end_body, 3.6)

def chot2(d, t, sc, chot, hoi, goi_y, body, at_goi):
    """Nhu chot_hoi cua engine nhung the THU NGHI co theo noi dung: day o 1290 truoc goi y, gian toi 1600 khi goi y hien."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, chot, 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + at_goi, 0.5)
    card(d, (40, 620, 1040, 1290 + 310 * kh), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 820, hoi, 46, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
    body(d, t, k1)
    if kh > 0:
        card(d, (110, 1320, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1368, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1460, goi_y, 44, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][0] + 1.6, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + a, "tap") for a, _, _ in drops(do)] + [(do["t0"] + t_rest(do), "tap")]
            + [(da["t0"] + da["M"][0] + 1.6, "ding"), (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-dttruong-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Điện từ trường · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nam châm và ống dây", draw=s_hook, tail=0.3, caps=[
   ("Ống dây nối đồng hồ số.", 3.0),
   ("Nghĩ trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Cho nam châm qua ống, v tăng dần.", 9.1),
   ("Giữ nam châm yên giữa ống.", 3.6)]),
 dict(key="dapan", title="Kết quả và cơ chế", draw=s_dapan, tail=0.6, caps=[
   ("So hai điểm được tô màu.", 3.2),
   ("Vì sao dây có điện trường?", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.7, caps=[
   ("Đúng hay sai?", 4.8),
   ("Còn giới hạn.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước.", 6.6)]),
])
