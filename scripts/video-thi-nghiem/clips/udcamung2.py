# Clip: tn-l12-udcamung-02 - Hai cuon dat canh nhau: dong o cuon 1 doi thi cuon 2 moi co suat dien dong (28/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-udcamung-02.json:
#   so_lieu_mau: bat 25 A/s -> e2 = -0,05 V ; giu 0 -> 0 ; ngat -25 A/s -> +0,05 V
#   tham_so: M = 2 mH, I0 = 0,5 A, dt = 0,02 s ; dung_cu: pin 1,5 V, dien ke so 0 o giua.
# Canh: Du doan (4 lua chon cung kieu) -> Tien hanh (bat/giu/ngat trong MOT canh, do thi i1 va e2 ve dan, chieu cham)
#       -> Dap an C + bang so lieu + e2 = -M.di/dt -> Bay (dong on dinh) + chua noi duoc -> Chot + cau hoi de sac.
from engine import *

# ---------------- bo cuc (khung 1080x1920) ----------------
CY, CR = 470, 92                      # truc hai cuon, nua chieu cao vong day
C1 = (150, 390); C2 = (470, 710)      # x dau - cuoi cuon 1 / cuon 2 (dat sat nhau)
NT = 8
COL1, COL2 = ORANGE, TEAL
GX, GY, GR, GANG = 790, 915, 165, 48  # dien ke: tam quay, ban kinh, goc lech toi da
I0, EMAX = 0.5, 0.05

def vn(x, nd=2, sign=False):
    if abs(x) < 1e-9: return "0"
    s = f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"
    return s.replace(".", ",").replace("-", "−")

# ---------------- mo hinh theo "u" (0..1, truc thoi gian so do, khong theo ti le) ----------------
U = (0.12, 0.22, 0.72, 0.82)          # bat dau tang, het tang, bat dau giam, het giam
def i1_of(u):
    a, b, c, e = U
    if u < a: return 0.0
    if u < b: return I0 * (u - a) / (b - a)
    if u < c: return I0
    if u < e: return I0 * (1 - (u - c) / (e - c))
    return 0.0
def e2_of(u):                          # e2 = -M.di1/dt : -0,05 V khi tang, +0,05 V khi giam
    a, b, c, e = U
    if a <= u < b: return -EMAX
    if c <= u < e: return EMAX
    return 0.0

# ---------------- hinh ve thiet bi ----------------
def turns(c): return [c[0] + j * (c[1] - c[0]) / (NT - 1) for j in range(NT)]

def coil(d, c, col, front):
    for x in turns(c):
        if front: d.arc([x - 16, CY - CR, x + 16, CY + CR], 270, 90, fill=A(col, 0.95), width=9)
        else: d.arc([x - 16, CY - CR, x + 16, CY + CR], 90, 270, fill=mix(col, BG, 0.5), width=7)

def chevron(d, x, y, ang, color, s=14, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def dashed_poly(d, pts, color, w=4, seg=12, gap=9):
    acc, on, cur = 0.0, True, [pts[0]]
    for p, q in zip(pts, pts[1:]):
        acc += math.dist(p, q); cur.append(q)
        if acc >= (seg if on else gap):
            if on and len(cur) > 1: d.line(cur, fill=color, width=w)
            on, acc, cur = not on, 0.0, [q]
    if on and len(cur) > 1: d.line(cur, fill=color, width=w)

XL, XR = 120, 740                     # doan thang trong long hai cuon
def loop(off, reach, rx, sg):
    """Duong suc kin: di trong long hai cuon (trai -> phai), ra o dau phai, vong ngoai, vao lai o dau trai."""
    yi, yo = CY + sg * off, CY + sg * reach
    cy, ry = (yi + yo) / 2, abs(yo - yi) / 2
    pts = [(XL + (XR - XL) * k / 40, yi) for k in range(41)]
    pts += [(XR + rx * math.sin(math.pi * k / 30), cy - sg * ry * math.cos(math.pi * k / 30)) for k in range(31)]
    pts += [(XR - (XR - XL) * k / 40, yo) for k in range(41)]
    pts += [(XL - rx * math.sin(math.pi * k / 30), cy + sg * ry * math.cos(math.pi * k / 30)) for k in range(31)]
    return pts

LOOPS = [loop(off, reach, rx, sg) for off, reach, rx in ((30, 128, 80), (60, 104, 40)) for sg in (-1, 1)]

def field(d, alpha):
    if alpha <= 0.02: return
    c = A(PURPLE, 0.6 * alpha)
    for pts in LOOPS:
        dashed_poly(d, pts, c)
        chevron(d, 600, pts[0][1], 0, c)                       # trong long: trai -> phai
        n = len(pts); k = 41 + 31 + 20                          # doan ngoai: phai -> trai
        chevron(d, pts[k][0], pts[k][1], math.pi, c)
    d.line([(XL - 70, CY), (XR + 70, CY)], fill=c, width=4)
    chevron(d, 600, CY, 0, c); chevron(d, XR + 70, CY, 0, c)

def battery_switch(d, closed):
    y = 655
    d.line([(C1[0], CY + CR - 4), (C1[0], y), (200, y)], fill=NAVY, width=5)
    d.line([(200, y - 34), (200, y + 34)], fill=NAVY, width=6)          # ban cuc dai (+)
    d.line([(222, y - 18), (222, y + 18)], fill=NAVY, width=10)         # ban cuc ngan (-)
    d.line([(222, y), (290, y)], fill=NAVY, width=5)
    dot(d, 290, y, 9, NAVY); dot(d, 360, y, 9, NAVY)
    ang = 0 if closed else math.radians(-32)
    d.line([(290, y), (290 + 76 * math.cos(ang), y + 76 * math.sin(ang))], fill=NAVY, width=7)
    d.line([(360, y), (C1[1], y), (C1[1], CY + CR - 4)], fill=NAVY, width=5)
    text(d, (C1[0] - 14, y), "1,5 V", 32, MUTED, bold=False, anchor="rm")
    text(d, (325, y - 46 if closed else y - 70), "K", 34, INK)

def galvo_wires(d):
    d.line([(C2[0], CY + CR - 4), (C2[0], 670), (640, 670), (640, 712)], fill=NAVY, width=5)
    d.line([(C2[1], CY + CR - 4), (C2[1], 640), (940, 640), (940, 712)], fill=NAVY, width=5)
    for x in (640, 940): dot(d, x, 712, 10, NAVY)

def galvo(d, e):
    card(d, (560, 712, 1020, 975), fill=WHITE, outline=NAVY, r=26, w=4)
    d.arc([GX - GR, GY - GR, GX + GR, GY + GR], 270 - GANG - 4, 270 + GANG + 4, fill=NAVY, width=4)
    for v in range(-4, 5):
        a = math.radians(v / 4 * GANG); big = v == 0 or abs(v) == 4
        r0 = GR - (28 if big else 16)
        d.line([(GX + r0 * math.sin(a), GY - r0 * math.cos(a)), (GX + GR * math.sin(a), GY - GR * math.cos(a))], fill=NAVY, width=5 if big else 3)
    text(d, (GX, GY - GR - 26), "0", 34, NAVY)
    text(d, (GX - GR - 6, GY - 40), "−", 40, BLUE); text(d, (GX + GR + 6, GY - 40), "+", 40, RED)
    a = math.radians(clamp(e / EMAX, -1.05, 1.05) * GANG * 0.85)
    d.line([(GX, GY), (GX + (GR - 10) * math.sin(a), GY - (GR - 10) * math.cos(a))], fill=RED, width=8)
    dot(d, GX, GY, 15, NAVY)
    text(d, (GX, 952), "điện kế", 36, MUTED, bold=False)

def legend(d):
    text(d, (950, 360), "cuộn 1", 38, COL1); text(d, (950, 406), "pin", 36, MUTED, bold=False)
    text(d, (950, 520), "cuộn 2", 38, COL2); text(d, (950, 566), "điện kế", 36, MUTED, bold=False)

def readout(d, i, state, scol):
    card(d, (60, 712, 520, 975), fill=WHITE, outline=LIGHT, r=26, w=3)
    text(d, (290, 754), "Dòng i₁", 36, MUTED, bold=False)
    d.rounded_rectangle([100, 800, 480, 836], radius=18, fill=LIGHT)
    if i > 0.005: d.rounded_rectangle([100, 800, 100 + 380 * i / I0, 836], radius=18, fill=COL1)
    text(d, (100, 866), "0", 32, MUTED, bold=False, anchor="lm"); text(d, (480, 866), "0,5 A", 32, MUTED, bold=False, anchor="rm")
    if state: text(d, (290, 928), state, 36, scol)

def apparatus(d, i, e, closed, state="", scol=INK):
    field(d, i / I0)
    coil(d, C1, COL1, False); coil(d, C2, COL2, False)
    coil(d, C1, COL1, True); coil(d, C2, COL2, True)
    legend(d)
    battery_switch(d, closed)
    galvo_wires(d)
    galvo(d, e)
    readout(d, i, state, scol)

# ---------------- do thi i1(t) va e2(t) chong nhau ----------------
def plot(d, box, u, pen=True, bands=0.0, alpha=1.0):
    x0, y0, x1, y1 = box
    X = lambda uu: x0 + uu * (x1 - x0)
    h = y1 - y0; it, ib = y0 + 0.08 * h, y0 + 0.40 * h           # khung i1
    ez = y0 + 0.73 * h; es = 0.22 * h                              # khung e2: truc 0, nua bien do
    Yi = lambda v: ib - v / I0 * (ib - it); Ye = lambda v: ez - v / EMAX * es
    if bands > 0:
        for a, b in ((U[0], U[1]), (U[2], U[3])):
            d.rounded_rectangle([X(a) - 10, it - 18, X(b) + 10, ez + es + 18], radius=14, fill=A((187, 247, 208), bands), outline=A(GREEN, bands), width=3)
    for yy, lab in ((Yi(I0), "0,5"), (ib, "0")):
        if lab != "0": d.line([(x0, yy), (x1, yy)], fill=LIGHT, width=2)
        text(d, (x0 - 14, yy), lab, 32, MUTED, bold=False, anchor="rm")
    for yy, lab in ((Ye(EMAX), "+0,05"), (ez, "0"), (Ye(-EMAX), "−0,05")):
        if lab != "0": d.line([(x0, yy), (x1, yy)], fill=LIGHT, width=2)
        text(d, (x0 - 14, yy), lab, 32, MUTED, bold=False, anchor="rm")
    for yy0, yy1, yz, lab in ((it - 30, ib, ib, "i₁ (A)"), (ez - es - 30, ez + es + 10, ez, "e₂ (V)")):
        d.line([(x0, yy0), (x0, yy1)], fill=NAVY, width=4); chevron(d, x0, yy0, -math.pi / 2, NAVY, s=16)
        d.line([(x0, yz), (x1 + 14, yz)], fill=NAVY, width=4); chevron(d, x1 + 14, yz, 0, NAVY, s=16)
        text(d, (x0 + 20, yy0 + 4), lab, 32, INK, anchor="lm")
    text(d, (x1 + 10, ez + 40), "t", 32, INK, anchor="rm")
    for uu, lab in (((U[0] + U[1]) / 2, "bật"), ((U[1] + U[2]) / 2, "giữ"), ((U[2] + U[3]) / 2, "ngắt")):
        text(d, (X(uu), y1 - 4), lab, 36, MUTED, bold=False)
    if u > 0:
        us = sorted(set([k / 400 * u for k in range(401)] + [x for x in U if x <= u]))
        d.line([(X(v), Yi(i1_of(v))) for v in us], fill=COL1, width=7, joint="curve")
        pts = []
        for v in us:
            if pts and abs(e2_of(v) - e2_of(pts[-1][2])) > 1e-9:
                pts.append((X(v), Ye(e2_of(pts[-1][2])), v))
            pts.append((X(v), Ye(e2_of(v)), v))
        d.line([(p[0], p[1]) for p in pts], fill=PURPLE, width=7)
        if pen and u < 0.999:
            dot(d, X(u), Yi(i1_of(u)), 12, RED, outline=WHITE); dot(d, X(u), Ye(e2_of(u)), 12, RED, outline=WHITE)
    return X, Yi, Ye

# ---------------- canh 1: Du doan ----------------
OPTS = ("lệch một phía, giữ nguyên", "giật 2 lần, cùng phía", "giật 2 lần, ngược phía", "đứng yên ở số 0")

def s_hook(img, d, t, sc):
    apparatus(d, 0.0, 0.0, False, "K mở", MUTED)
    M = sc["M"]; a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    text(d, (W / 2, y0 + 140), "Bật K, giữ, rồi ngắt.", 44, INK, alpha=a)
    text(d, (W / 2, y0 + 196), "Kim điện kế sẽ…", 44, INK, alpha=a)
    for j, s in enumerate(OPTS):
        k = appear(t, M[1] + 0.15 * j, 0.4); yy = y0 + 270 + j * 76
        d.rounded_rectangle([90, yy - 30, 990, yy + 30], radius=30, outline=A(LIGHT, k), width=3)
        text(d, (120, yy), f"{'ABCD'[j]}.  {s}", 42, NAVY, bold=False, anchor="lm", alpha=k)
    tc, tend = M[1] + 0.8, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 572, 940, y0 + 584], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 572, 140 + 800 * (1 - p), y0 + 584], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (bat - giu - ngat lien mach) ----------------
def u_of(t, sc):
    M = sc["M"]
    return float(np.interp(t, [M[0] + 0.3, M[0] + 0.9, M[0] + 1.9, M[1] - 0.1, M[1] + 0.9, sc["T"] - 0.4],
                           [0, U[0], U[1], U[2], U[3], 1.0]))

def chips(d, cur):
    for j, s in enumerate(("Bật", "Giữ", "Ngắt")):
        x0 = 60 + j * 330; box = (x0, 240, x0 + 300, 296)
        if j == cur: card(d, box, fill=ORANGE, r=28); text(d, (x0 + 150, 268), s, 38, WHITE)
        elif j < cur: card(d, box, fill=LIGHT, r=28); text(d, (x0 + 150, 268), s, 38, INK)
        else: card(d, box, fill=None, outline=LIGHT, r=28, w=3); text(d, (x0 + 150, 268), s, 38, GRAY)

def s_do(img, d, t, sc):
    u = u_of(t, sc); i = i1_of(u)
    closed = U[0] - 0.004 <= u < U[2] + 0.004
    # kim: theo e2, them tre nho (quan tinh) de nhin thay giat ra - ve
    lag = 0.02; e = 0.0
    for k in range(6): e += e2_of(max(0, u - lag * k / 5)) / 6
    a, b, c, f = U
    if u < a: st, col = "K mở", MUTED
    elif u < b: st, col = "i₁ tăng", ORANGE
    elif u < c: st, col = "i₁ không đổi", GREEN
    elif u < f: st, col = "i₁ giảm", ORANGE
    else: st, col = "i₁ = 0", MUTED
    chips(d, 0 if u < b else (1 if u < c else 2))
    apparatus(d, i, e, closed, st, col)
    card(d, (40, 995, 1040, 1610), fill=WHITE, outline=LIGHT, w=3)
    plot(d, (210, 1020, 960, 1600), u)
    if (a <= u < b) or (c <= u < f):
        wdt = tw(d, "CHIẾU CHẬM", F(36)) + 44
        card(d, (1020 - wdt, 1006, 1020, 1052), fill=ORANGE, r=23); text(d, (1020 - wdt / 2, 1029), "CHIẾU CHẬM", 36, WHITE)

# ---------------- canh 3: Dap an + rut ra ----------------
ROWS = [("Bật K", 25, -0.05, -1), ("Giữ K đóng", 0, 0.0, 0), ("Ngắt K", -25, 0.05, 1)]   # so_lieu_mau

def mini_needle(d, cx, cy, s, alpha):
    d.arc([cx - 30, cy - 22, cx + 30, cy + 38], 220, 320, fill=A(NAVY, alpha), width=3)
    a = math.radians(s * 38)
    d.line([(cx, cy + 8), (cx + 30 * math.sin(a), cy + 8 - 30 * math.cos(a))], fill=A(RED, alpha), width=5)
    dot(d, cx, cy + 8, 5, A(NAVY, alpha))

def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 245, 1040, 905), fill=WHITE, outline=LIGHT, w=3)
    hb = appear(t, M[1] - 0.1, 0.5)
    X, Yi, Ye = plot(d, (200, 330, 960, 890), 1.0, pen=False, bands=0.85 * hb)
    ka = appear(t, M[0] + 0.1, 0.5)
    pw = tw(d, "ĐÁP ÁN C", F(36)) + 52
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 322), fill=A(NAVY, ka), r=30)
    text(d, (W / 2, 292), "ĐÁP ÁN C", 36, WHITE, alpha=ka)
    text(d, ((X(U[1]) + X(U[2])) / 2, Yi(I0) + 44), "i₁ không đổi: e₂ = 0", 36, GREEN, alpha=hb)
    # bang so lieu
    kt = appear(t, M[0] + 0.6, 0.5)
    y = 930
    card(d, (40, y, 1040, y + 320), fill=A(WHITE, kt), outline=A(LIGHT, kt), w=3)
    for x, s in ((90, "Thao tác"), (520, "Δi₁/Δt (A/s)"), (760, "e₂ (V)"), (940, "Kim")):
        text(d, (x, y + 40), s, 32, MUTED, bold=False, anchor="lm" if x == 90 else "mm", alpha=kt)
    d.line([(70, y + 70), (1010, y + 70)], fill=A(LIGHT, kt), width=3)
    for j, (nm, di, e2, s) in enumerate(ROWS):
        k = appear(t, M[0] + 0.8 + 0.25 * j, 0.4); yy = y + 118 + j * 70
        col = BLUE if e2 < 0 else (RED if e2 > 0 else GREEN)
        text(d, (90, yy), nm, 38, INK, anchor="lm", alpha=k)
        text(d, (520, yy), str(di).replace("-", "−"), 38, INK, alpha=k)
        text(d, (760, yy), vn(e2, 2, sign=e2 != 0), 38, col, alpha=k)
        mini_needle(d, 940, yy - 8, s, k)
    # co che + cong thuc
    k1 = appear(t, M[1] + 0.2, 0.5); k2 = appear(t, M[1] + 1.6, 0.5)
    card(d, (40, 1280, 1040, 1610), fill=A(WHITE, k1), outline=A(GREEN, k1), w=5)
    text(d, (W / 2, 1335), "i₁ đổi → B đổi → có e₂", 46, GREEN, alpha=k1)
    text(d, (W / 2, 1440), "e₂ = −M · Δi₁/Δt", 58, INK, alpha=k2)
    text(d, (W / 2, 1530), "M = 2 mH: 25 A/s → −0,05 V", 38, MUTED, bold=False, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    apparatus(d, I0, 0.0, True, "không đổi", GREEN)
    k1 = appear(t, 0.3, 0.45); k2 = appear(t, M[1] - 0.1, 0.45); a1 = k1 * (1 - k2)
    if a1 > 0:
        y0 = 1000 + (1 - k1) * 30
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“Có dòng ở cuộn 1 là cuộn 2 có e₂”"
        ks = clamp((t - 1.0) / 0.4)
        f = F(42); lw = tw(d, q, f); yy = y0 + 170
        text(d, (W / 2, yy), q, 42, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * a1), width=4)
        ctext(d, y0 + 300, "Sai: kim vẫn ở 0.", 50, RED, maxw=900, alpha=a1 * appear(t, 1.6, 0.5))
        ctext(d, y0 + 450, "Từ trường không ĐỔI.", 46, INK, maxw=880, alpha=a1 * appear(t, 2.8, 0.5))
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 62), "Chưa nói được", 48, NAVY, alpha=k2)
        lines = (("• Độ lớn e₂: chưa đo", ""), ("• ±0,05 V: số minh hoạ", ""), ("• Hai cuộn xa: kim ít lệch", ""))
        for j, (l1, l2) in enumerate(lines):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4); yy = y0 + 200 + j * 130
            text(d, (90, yy), l1, 46, INK, bold=False, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Chỉ khi i₁ đang ĐỔI, cuộn 2 mới có e₂",
             "Đế sạc nối thẳng vào pin 1,5 V. Điện thoại có sạc được không? Vì sao?",
             "e₂ = −M · Δi₁/Δt\nGiữ K đóng: kim chỉ ở đâu?")

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.3, "ding"),
            (do["t0"] + M[0] + 0.9, "tap"), (do["t0"] + M[1] - 0.1, "tap"),
            (da["t0"] + da["M"][0] + 0.1, "ding"), (b["t0"] + b["M"][0], "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-udcamung-02", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Ứng dụng cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai cuộn dây đặt sát nhau", draw=s_hook, tail=0.6, caps=[
   "Quan sát kim điện kế.",
   ("Dừng video, chọn A, B, C hay D.", 5.5)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Bật K rồi giữ đóng.", 5.2),
   ("Ngắt K: kim giật phía kia.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Kim giật ngược phía: đáp án C.", 3.4),
   ("Chỉ khi i₁ đang đổi mới có e₂.", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 5.0),
   ("Giới hạn của thí nghiệm.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video và trả lời.", 7.4)]),
])
