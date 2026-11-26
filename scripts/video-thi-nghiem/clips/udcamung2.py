# Clip: tn-l12-udcamung-02 - Hai cuon dat canh nhau: dong o cuon 1 doi thi cuon 2 moi co suat dien dong
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-udcamung-02.json:
#   so_lieu_mau: bat 25 A/s -> e2 = -0,05 V ; giu 0 -> 0 ; ngat -25 A/s -> +0,05 V
#   tham_so: M = 2 mH, I0 = 0,5 A, dt = 0,02 s ; dung_cu: pin 1,5 V, dien ke so 0 o giua.
# Ban 2 (26/11/2026, viec 4 lo 32, cong --do-chu moi): canh hook / do / ans / bay / gioi / end nhu mau xoaychieu2.
#   Du doan (K10 khong ve nut; khung web A-D): bat K, giu, ngat -> kim dien ke? -> giat 2 lan, nguoc phia
#     (hien_tuong_hay_sai #1 dong on dinh van co e2, #3 bat va ngat cung phia). Bai: Cau 2 hoi U2 bien ap, khong trung.
#   Bay: "dong chay deu thi cuon 2 co dien?" -> giu K dong, dong ho dem giay, kim van o 0.
#   Chot (khung web A-D, dap an KHONG hien): de sac noi thang pin 1,5 V -> khong sac duoc (i1 khong doi)
#     (hien_tuong_hay_sai #2). Ca suy dinh tinh tu rut_ra kho, khong co so moi.
# Toa do mp4 = 65 + 0,88.x; chu than canh ve >= 56 px (ra >= 49 px).
from engine import *

# ---------------- bo cuc (khung 1080x1920) ----------------
CY, CR = 480, 92                      # truc hai cuon, nua chieu cao vong day
C1 = (150, 390); C2 = (470, 710)      # x dau - cuoi cuon 1 / cuon 2 (dat sat nhau)
NT = 8
COL1, COL2 = ORANGE, TEAL
DGREEN = (21, 128, 61); DARK_OR = (181, 71, 8)
GX, GY, GR, GANG = 800, 940, 150, 48  # dien ke: tam quay, ban kinh, goc lech toi da
I0, EMAX = 0.5, 0.05
assert abs(2e-3 * 25 - EMAX) < 1e-12                  # e2 = M.di/dt = 2 mH . 25 A/s

def vn(x, nd=2, sign=False):
    if abs(x) < 1e-9: return "0"
    s = f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"
    return s.replace(".", ",").replace("-", "−")

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
    c = A(PURPLE, 0.75 * alpha)
    for pts in LOOPS:
        dashed_poly(d, pts, c)
        chevron(d, 600, pts[0][1], 0, c)                       # trong long: trai -> phai
        n = len(pts); k = 41 + 31 + 20                          # doan ngoai: phai -> trai
        chevron(d, pts[k][0], pts[k][1], math.pi, c)
    d.line([(XL - 70, CY), (XR + 70, CY)], fill=c, width=4)
    chevron(d, 600, CY, 0, c); chevron(d, XR + 70, CY, 0, c)

def battery_switch(d, closed):
    y = 660
    d.line([(C1[0], CY + CR - 4), (C1[0], y), (200, y)], fill=NAVY, width=5)
    d.line([(200, y - 34), (200, y + 34)], fill=NAVY, width=6)          # ban cuc dai (+)
    d.line([(222, y - 18), (222, y + 18)], fill=NAVY, width=10)         # ban cuc ngan (-)
    d.line([(222, y), (290, y)], fill=NAVY, width=5)
    dot(d, 290, y, 9, NAVY); dot(d, 360, y, 9, NAVY)
    ang = 0 if closed else math.radians(-32)
    d.line([(290, y), (290 + 76 * math.cos(ang), y + 76 * math.sin(ang))], fill=NAVY, width=7)
    d.line([(360, y), (C1[1], y), (C1[1], CY + CR - 4)], fill=NAVY, width=5)
    text(d, (211, y + 52), "1,5 V", 56, INK)
    text(d, (325, y - 50 if closed else y - 78), "K", 56, INK)

def galvo_wires(d):
    d.line([(C2[0], CY + CR - 4), (C2[0], 680), (650, 680), (650, 742)], fill=NAVY, width=5)
    d.line([(C2[1], CY + CR - 4), (C2[1], 650), (950, 650), (950, 742)], fill=NAVY, width=5)
    for x in (650, 950): dot(d, x, 742, 10, NAVY)

def galvo(d, e):
    card(d, (580, 742, 1020, 1000), fill=WHITE, outline=NAVY, r=26, w=4)
    d.arc([GX - GR, GY - GR, GX + GR, GY + GR], 270 - GANG - 4, 270 + GANG + 4, fill=NAVY, width=4)
    for v in range(-4, 5):
        a = math.radians(v / 4 * GANG); big = v == 0 or abs(v) == 4
        r0 = GR - (28 if big else 16)
        d.line([(GX + r0 * math.sin(a), GY - r0 * math.cos(a)), (GX + GR * math.sin(a), GY - GR * math.cos(a))], fill=NAVY, width=5 if big else 3)
    text(d, (GX, GY - GR - 30), "0", 56, NAVY)
    text(d, (GX - GR - 30, GY - 60), "−", 60, BLUE); text(d, (GX + GR + 30, GY - 60), "+", 60, RED)
    a = math.radians(clamp(e / EMAX, -1.05, 1.05) * GANG * 0.85)
    d.line([(GX, GY), (GX + (GR - 10) * math.sin(a), GY - (GR - 10) * math.cos(a))], fill=RED, width=8)
    dot(d, GX, GY, 15, NAVY)

def legend(d):
    text(d, (270, 276), "cuộn 1", 56, COL1); text(d, (590, 276), "cuộn 2", 56, COL2)

def readout(d, i, state, scol):
    card(d, (40, 762, 560, 1000), fill=WHITE, outline=LIGHT, r=26, w=3)
    text(d, (300, 806), "Dòng i₁", 56, INK)
    d.rounded_rectangle([90, 844, 510, 884], radius=20, fill=LIGHT)
    if i > 0.005: d.rounded_rectangle([90, 844, 90 + 420 * i / I0, 884], radius=20, fill=COL1)
    if state: text(d, (300, 948), state, 56, scol)

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
def plot(d, box, u, pen=True, bands=0.0, alpha=1.0, phase=False):
    x0, y0, x1, y1 = box
    X = lambda uu: x0 + uu * (x1 - x0)
    h = y1 - y0; it, ib = y0 + 0.10 * h, y0 + 0.40 * h           # khung i1
    ez = y0 + 0.72 * h; es = 0.22 * h                              # khung e2
    Yi = lambda v: ib - v / I0 * (ib - it); Ye = lambda v: ez - v / EMAX * es
    if bands > 0:
        for a, b in ((U[0], U[1]), (U[2], U[3])):
            d.rounded_rectangle([X(a) - 12, it - 14, X(b) + 12, ez + es + 6], radius=14, fill=A((187, 247, 208), bands), outline=A(GREEN, bands), width=3)
    d.line([(x0, Yi(I0)), (x1, Yi(I0))], fill=LIGHT, width=2)
    text(d, (x0 - 14, Yi(I0)), "0,5 A", 56, INK, anchor="rm")
    text(d, (x0 - 14, (it + ib) / 2 + 10), "i₁", 60, COL1, anchor="rm")
    for yy, lab in ((Ye(EMAX), "+0,05"), (Ye(-EMAX), "−0,05")):
        d.line([(x0, yy), (x1, yy)], fill=LIGHT, width=2)
        text(d, (x0 - 14, yy), lab, 56, INK, anchor="rm")
    text(d, (x0 - 14, ez), "e₂ (V)", 56, PURPLE, anchor="rm")
    for yy0, yy1, yz in ((it - 30, ib, ib), (ez - es - 30, ez + es + 10, ez)):
        d.line([(x0, yy0), (x0, yy1)], fill=NAVY, width=4); chevron(d, x0, yy0, -math.pi / 2, NAVY, s=16)
        d.line([(x0, yz), (x1 + 14, yz)], fill=NAVY, width=4); chevron(d, x1 + 14, yz, 0, NAVY, s=16)
    if phase:
        for uu, lab in (((U[0] + U[1]) / 2, "bật"), ((U[2] + U[3]) / 2, "ngắt")):
            text(d, (X(uu), it - 52), lab, 56, DGREEN, alpha=bands)
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

PB = (330, 1050, 980, 1580)                 # o do thi trong canh Tien hanh

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    apparatus(d, 0.0, 0.0, False, "K mở", INK)
    M = sc["M"]; a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 530), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 180), "Bật K, giữ, rồi ngắt.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "Kim điện kế thế nào?", 60, INK, alpha=a)
    tc, te = M[1] + 0.3, sc["T"] - 0.1
    p = clamp((t - tc) / (te - tc))
    d.rounded_rectangle([110, y0 + 375, 970, y0 + 495], radius=24, fill=A(LIGHT, a))
    if p < 1: d.rounded_rectangle([110, y0 + 375, 110 + 860 * (1 - p), y0 + 495], radius=24, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (bat - giu - ngat lien mach) ----------------
def u_of(t, sc):
    M = sc["M"]
    return float(np.interp(t, [M[0] + 0.3, M[0] + 0.9, M[0] + 1.9, M[1] - 0.1, M[1] + 0.9, sc["T"] - 0.4],
                           [0, U[0], U[1], U[2], U[3], 1.0]))

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    u = u_of(t, sc); i = i1_of(u)
    closed = U[0] - 0.004 <= u < U[2] + 0.004
    lag = 0.02; e = 0.0
    for k in range(6): e += e2_of(max(0, u - lag * k / 5)) / 6
    a, b, c, f = U
    if u < a: st, col = "K mở", INK
    elif u < b: st, col = "i₁ tăng", ORANGE
    elif u < c: st, col = "i₁ không đổi", DGREEN
    elif u < f: st, col = "i₁ giảm", ORANGE
    else: st, col = "i₁ = 0", INK
    apparatus(d, i, e, closed, st, col)
    card(d, (40, 1020, 1040, 1600), fill=WHITE, outline=LIGHT, w=3)
    plot(d, PB, u)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    s = "ĐÁP ÁN: hai lần, ngược phía"; pw = tw(d, s, F(56)) + 70      # hien ngay tu 0 s
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 340), fill=GREEN, r=39)
    text(d, (W / 2, 301), s, 56, WHITE)
    card(d, (40, 370, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    hb = appear(t, 0.5, 0.5)
    X, Yi, Ye = plot(d, (330, 440, 980, 950), 1.0, pen=False, bands=0.85 * hb, phase=True)
    k1 = appear(t, sc["M"][1] - 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 1000, 1040, 1420), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1090), "i₁ đổi → B đổi → có e₂", 62, DGREEN, alpha=k1)
        text(d, (W / 2, 1210), "e₂ = −ΔΦ₂/Δt", 72, NAVY, alpha=k1)
        text(d, (W / 2, 1330), "i₁ không đổi: e₂ = 0", 60, INK, alpha=appear(t, sc["M"][1] + 2.2, 0.4))

# ---------------- canh 4: Bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    b1, b2, b3 = (m - 0.1 for m in sc["M"])
    k1, k2, k3 = 1.0, appear(t, b2, 0.4), appear(t, b3, 0.4)   # the BAY hien ngay (mot khoi chu luc 0 s)
    apparatus(d, I0, 0.0, True, "i₁ = 0,5 A", DGREEN)
    card(d, (40, 1020, 1040, 1600), fill=A(WHITE, k1), outline=A(RED, k1), w=5)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 1040, W / 2 + pw / 2, 1116), fill=A(RED, k1), r=38)
    text(d, (W / 2, 1078), "BẪY", 56, WHITE, alpha=k1)
    text(d, (W / 2, 1190), "Dòng chạy đều mãi:", 62, INK, alpha=k1)
    text(d, (W / 2, 1275), "cuộn 2 có dòng điện?", 62, RED, alpha=k1)
    if k2 > 0:                                  # dong ho dem giay giu K: kim van o 0
        sec = int(clamp((t - b2) / 0.6, 0, 9)) + 1
        card(d, (110, 1340, 970, 1450), fill=A((241, 245, 249), k2), outline=A(NAVY, k2), r=24, w=3)
        text(d, (W / 2, 1395), f"giữ K {sec} s · kim: 0", 60, NAVY, alpha=k2)
    if k3 > 0:
        pw2 = tw(d, "SAI", F(56)) + 50
        card(d, (1020 - pw2, 1040, 1020, 1116), fill=A((127, 29, 29), k3), r=38)
        text(d, (1020 - pw2 / 2, 1078), "SAI", 56, WHITE, alpha=k3)
        text(d, (W / 2, 1530), "B không đổi → e₂ = 0", 62, DGREEN, alpha=k3)

# ---------------- canh 5: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Độ lớn e₂ thật: cần đo", "• Hai cuộn xa thì sao?")):
        text(d, (100, 600 + j * 260), s, 66, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 800), "?", 200, NAVY, alpha=k * (1 - kb))

# ---------------- canh 6: THU NGHI (cau_chot cua khung; dap an KHONG hien) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.3, 0.5)
    card(d, (40, 260, 1040, 1180), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 285, W / 2 + pw / 2, 365), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 325), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 450), "Đế sạc nối thẳng pin 1,5 V.", 60, INK, alpha=k)
    text(d, (W / 2, 540), "Điện thoại sạc được không?", 60, DARK_OR, alpha=k)
    # de sac (cuon phang) + dien thoai dat len, dau "?" nhap nhay; pin ben trai
    cx, cy = W / 2 + 80, 880
    d.ellipse([cx - 230, cy + 40, cx + 230, cy + 120], fill=(203, 213, 225), outline=NAVY, width=4)
    for r in (60, 110, 160):
        d.ellipse([cx - r, cy + 80 - r * 0.17, cx + r, cy + 80 + r * 0.17], outline=COL1, width=5)
    ph = 1 - 0.5 * (0.5 + 0.5 * math.sin(3 * t))
    d.rounded_rectangle([cx - 110, cy - 200, cx + 110, cy + 60], radius=26, fill=NAVY)
    d.rounded_rectangle([cx - 95, cy - 185, cx + 95, cy + 40], radius=18, fill=(226, 232, 240))
    text(d, (cx, cy - 72), "?", 110, DARK_OR, alpha=k * ph)
    bx, by = 190, 900
    d.line([(bx, by - 130), (bx, by - 160), (cx - 200, by - 160), (cx - 200, cy + 62)], fill=NAVY, width=6)   # day (+) -> de
    d.line([(bx, by + 110), (bx, by + 160), (cx + 200, by + 160), (cx + 200, cy + 98)], fill=NAVY, width=6)   # day (-) -> de
    d.rounded_rectangle([bx - 84, by - 110, bx + 84, by + 110], radius=14, fill=(250, 204, 21), outline=NAVY, width=4)
    d.rectangle([bx - 24, by - 130, bx + 24, by - 110], fill=NAVY)
    text(d, (bx, by), "1,5 V", 56, NAVY, alpha=k)
    kh = appear(t, 3.3, 0.5)
    if kh > 0:
        card(d, (90, 1230, 990, 1380), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1305), "Gợi ý: dòng pin có đổi?", 60, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, g, e = (sc[k] for k in ("hook", "do", "ans", "bay", "gioi", "end"))
    M = do["M"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + M[0] + 0.9, "tap"), (do["t0"] + M[1] - 0.1, "tap"),
            (an["t0"] + 0.1, "ding"), (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
            (g["t0"] + 2.4, "tap"), (e["t0"] + 0.3, "open")]

CLIP = dict(id="tn-l12-udcamung-02", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Ứng dụng cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai cuộn dây đặt sát nhau", draw=s_hook, tail=0.3, caps=[
   ("Cuộn 2 nối điện kế.", 3.0),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Bật K rồi giữ đóng.", 5.2),
   ("Rồi ngắt K.", 3.8)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("Nhìn hai dải xanh.", 3.4),
   ("Chỉ khi i₁ đang đổi.", 4.4)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("Giữ K đóng thật lâu.", 3.0),
   ("Kim vẫn đứng ở 0.", 3.0)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Chưa trả lời được:", 4.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 6.8)]),
])
