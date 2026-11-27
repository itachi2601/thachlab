# Clip: tn-l10-baotoandl-01 - Va cham mem tren ray dem khi, cong quang do v (lo 9, 18/11/2026; dung lai 27/11/2026
# theo cong moi L10b: chu >= 55 px khi ve, nhip >= 2,5 s, K10 khong nut A-D, canh Bay hinh tu giai thich, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-baotoandl-01.json (_kiem_so() doi chieu):
#   tham_so: m1 = 0,20 kg (co dinh) ; m2 0,1-1,0 kg ; gia trong 0,10 kg
#   so_lieu_mau (m2, v1, v): 0,2 0,52 0,25 ; 0,3 0,60 0,24 ; 0,4 0,57 0,19 ; 0,6 0,66 0,16
# Du doan (doi ca 27/11: ca m2 = m1 -> "mot nua" trung cau mo bai An-Binh cua bai hoc): LAN 4, xe 2 0,60 kg (gap 3 xe 1),
#   xe 1 toi 0,66 m/s -> hai xe dinh nhau di? Dap an: con khoang 1/4 (do duoc 0,16 m/s).
#   Khung web: A. Van 0,66 m/s ; B. Khoang 0,33 m/s ; C. Khoang 0,16 m/s (DUNG) ; D. Dung han.
# Ket qua: hai hinh chu nhat rong = khoi luong, cao = toc do (lan 4) gan bang dien tich -> m1.v1 ~ (m1 + m2).v.
#   Khong tinh p tung lan (cau "Doc so lieu" sau hop bat HS tu tinh).
# Bay = hien_tuong_hay_sai[1] (dong nang cung bao toan) -> LAN 1 (cap so khac Du doan): dong nang sau ~ 1/2 truoc
#   (0,5.0,4.0,25^2 / 0,5.0,2.0,52^2 = 0,46). Chua noi duoc: hai xe nay ra (va cham dan hoi) chua thu.
# Cau chot (ca tu suy theo mo hinh, KHAC ca ghi_chu kho 0,30 kg -> 0,30 m/s vi so 0,30 hien san tren man):
#   xe 1 0,20 kg chay 0,75 m/s dinh xe 2 dung yen, hai xe di 0,15 m/s -> m1 + m2 = 0,20.0,75/0,15 = 1,0 kg -> m2 = 0,80 kg
#   (trong dai m2 0,1-1,0 kg). Can buoc nguoc + tru m1, clip chua chieu. 0,80 khong hien tren man.
from engine import *

ROWS = [(0.2, 0.52, 0.25), (0.3, 0.60, 0.24), (0.4, 0.57, 0.19), (0.6, 0.66, 0.16)]   # m2, v1, v
M1 = 0.20
CHOT = (0.20, 0.75, 0.15, 0.80)                                                        # m1, v1, v, m2 (dap so)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-baotoandl-01.json")))
    hang = [tuple(r[:3]) for r in k["so_lieu_mau"]["hang"]]
    assert all(any(all(abs(a - b) < 1e-9 for a, b in zip(r, h)) for h in hang) for r in ROWS), "so lieu lech kho"
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["m1"]["gia_tri"] == M1 and ts["m2"]["min"] <= CHOT[3] <= ts["m2"]["max"]
    assert abs(CHOT[0] * CHOT[1] / CHOT[2] - CHOT[0] - CHOT[3]) < 1e-9
_kiem_so()

C1, C1D = ORANGE, (154, 52, 18)                 # xe 1
C2, C2D = BLUE, (30, 64, 175)                   # xe 2
RAIL = (148, 163, 184); RAIL_D = (100, 116, 139); LCD = (134, 239, 172)
NOTE = (60, 64, 84); DGREEN = (21, 110, 55); SAP = (161, 98, 7); DRED = (185, 28, 28)
EMPTY = (148, 140, 128)
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o (cao 70 px), tat lan luot tu phai sang trai."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- ray dem khi, hai cong quang, hai xe ----------------
X0, PXM = 60, 800                     # px tai s = 0 ; px / m (ray 1,20 m) -> mp4 x = 65 + 0,88 x
G1, G2 = 0.40, 0.86                   # vi tri cong (m)
CL = 0.14                             # chieu dai xe (m)
X1S, X2S = 0.30, 0.66                 # tam xe 1 luc bat dau, tam xe 2 dung yen
XC1 = X2S - CL                        # tam xe 1 luc cham xe 2
YB = 790                              # mat ray
def sx(s): return X0 + s * PXM

def track(d, yb, k=1.0):
    d.rectangle([X0, yb + 2, X0 + 1.2 * PXM, yb + 26], fill=A(RAIL, k), outline=A(NAVY, k))
    for i in range(1, 40): dot(d, X0 + i * 24, yb + 14, 3, A(RAIL_D, k))
    d.rectangle([90, yb + 26, 120, yb + 60], fill=A(RAIL_D, k)); d.rectangle([960, yb + 26, 990, yb + 60], fill=A(RAIL_D, k))

def gate_back(d, yb, g):
    x = sx(g)
    for dx in (-30, 30): d.line([(x + dx, yb + 26), (x + dx, yb - 175)], fill=NAVY, width=7)
def gate_front(d, yb, g):
    x = sx(g); d.line([(x - 34, yb - 175), (x + 34, yb - 175)], fill=NAVY, width=9)
    dot(d, x - 30, yb - 110, 8, RED); dot(d, x + 30, yb - 110, 8, RED)

def cart(d, yb, x, col, cold, label, n_gt=0, k=1.0, front=None, rear=None):
    """x = tam xe (m). n_gt: so gia trong 0,10 kg tren xe. Xe cao 74 px, nhan 56 px."""
    c = lambda cc: A(cc, k); w = CL * PXM / 2; X = sx(x)
    d.rectangle([X - 6, yb - 132, X + 6, yb - 76], fill=c(NAVY))                  # tam can quang
    slots = [(-34, 0), (34, 0), (-34, 1), (34, 1)]
    for j in range(n_gt):
        dx, lv = slots[j]
        d.rectangle([X + dx - 18, yb - 104 - 28 * lv, X + dx + 18, yb - 78 - 28 * lv], fill=c(GRAY), outline=c(NAVY), width=2)
    d.rounded_rectangle([X - w, yb - 76, X + w, yb - 2], radius=12, fill=c(col), outline=c(cold), width=3)
    text(d, (X, yb - 39), label, 56, WHITE, alpha=k)
    if front == "kim": d.polygon([(X + w, yb - 46), (X + w + 18, yb - 39), (X + w, yb - 32)], fill=c(NAVY))
    if rear == "sap": d.ellipse([X - w - 14, yb - 52, X - w + 6, yb - 26], fill=c(SAP))

def lcd(d, x, y, lab, val, col, hi=False):
    text(d, (x, y - 80), lab, 56, col)
    card(d, (x - 150, y - 44, x + 150, y + 44), fill=NAVY, r=14)
    text(d, (x, y), val, 56, YELLOW if hi else LCD)

def kin(row, u):
    """u: giay tu luc xe 1 bat dau chay. -> (x1, x2, da qua cong 1, da qua cong 2)."""
    m2, v1, v = row
    uc = (XC1 - X1S) / v1
    if u < uc: x1, x2 = X1S + v1 * max(0.0, u), X2S
    else: x2 = X2S + v * (u - uc); x1 = x2 - CL
    return x1, x2, x1 >= G1 + 0.01, x2 >= G2 + 0.01

def run_len(row):
    m2, v1, v = row
    return 0.15 + (XC1 - X1S) / v1 + (G2 + 0.01 - X2S) / v + 0.55

def rig(d, row, u, k=1.0, x1_hook=None, yc=880):
    """Hinh trong the y 265-yc. u = None + x1_hook: xe 1 o vi tri x1_hook (canh Du doan)."""
    m2, v1, v = row
    card(d, (40, 265, 1040, yc), fill=WHITE, outline=LIGHT, w=3)
    text(d, (70, 320), f"xe 1: {vn(M1)} kg", 56, C1D, anchor="lm", alpha=k)
    text(d, (1010, 320), f"xe 2: {vn(m2)} kg", 56, C2D, anchor="rm", alpha=k)
    if x1_hook is not None: x1, x2, d1, d2 = x1_hook, X2S, x1_hook >= G1 + 0.01, False
    else: x1, x2, d1, d2 = kin(row, u)
    lcd(d, sx(G1) - 20, 495, "cổng 1", f"{vn(v1)} m/s" if d1 else "– – –", C1D)
    lcd(d, sx(G2) + 20, 495, "cổng 2", "?" if x1_hook is not None else (f"{vn(v)} m/s" if d2 else "– – –"), C2D, hi=d2)
    track(d, YB); gate_back(d, YB, G1); gate_back(d, YB, G2)
    n_gt = int(round((m2 - 0.2) / 0.1))
    cart(d, YB, x2, C2, C2D, "2", n_gt, k, rear="sap")
    cart(d, YB, x1, C1, C1D, "1", 0, k, front="kim")
    gate_front(d, YB, G1); gate_front(d, YB, G2)
    return x1, x2

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut A-D) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    x1 = lerp(0.18, 0.47, ease((t - 0.6) / 1.9))
    rig(d, ROWS[3], None, x1_hook=x1, yc=930)
    text(d, (sx(X2S), YB + 80), "v = 0", 56, C2D)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 965 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Dính nhau, hai xe đi", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "nhanh cỡ nào?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 410, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (4 lan) ----------------
R0, FADE = 0.5, 0.2
STARTS = []
_s = R0
for _r in ROWS: STARTS.append(_s); _s += run_len(_r)
DO_END = _s

def do_state(t):
    """-> (lan i, u tu luc xe 1 chay (None: chua), do mo hinh)."""
    if t < R0: return 0, None, 1.0
    i = max(j for j in range(4) if t >= STARTS[j]); w = t - STARTS[i]
    k = appear(w, 0.0, FADE) if i > 0 else 1.0
    if i < 3: k *= 1.0 - appear(w, run_len(ROWS[i]) - FADE, FADE)
    u = min(w, run_len(ROWS[i])) - 0.15
    return i, (u if u >= 0 else None), k

XS = (120, 360, 620, 880)
def table(d, cells, hl=None, y=920):
    card(d, (40, y, 1040, y + 650), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y + 65), "Lần", 56, INK)
    text(d, (XS[1], y + 65), "m₂ (kg)", 56, C2D); text(d, (XS[2], y + 65), "v₁ (m/s)", 56, C1D)
    text(d, (XS[3], y + 65), "v (m/s)", 56, PURPLE)
    d.line([(70, y + 120), (1010, y + 120)], fill=LIGHT, width=3)
    for j, (cm, c1, c2) in enumerate(cells):
        m2, v1, v = ROWS[j]; yy = y + 185 + j * 95
        if j == hl: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=20, fill=(255, 247, 237))
        if cm: text(d, (XS[0], yy), str(j + 1), 60, INK)
        if cm: text(d, (XS[1], yy), vn(m2), 60, C2D)
        if c1: text(d, (XS[2], yy), vn(v1), 60, C1D)
        if c2: text(d, (XS[3], yy), vn(v), 60, PURPLE)
    text(d, (W / 2, y + 590), "v: hai xe đã dính nhau", 56, PURPLE)

def cells_at(t):
    i, u, k = do_state(t); out = []
    for j in range(4):
        if t < R0 or j > i: out.append((False, False, False)); continue
        if j < i: out.append((True, True, True)); continue
        _, _, d1, d2 = kin(ROWS[j], -1 if u is None else u)
        out.append((True, d1 and u is not None, d2 and u is not None))
    return out

def s_do(img, d, t, sc):
    i, u, k = do_state(t)
    rig(d, ROWS[i], -1 if u is None else u, k=k)
    table(d, cells_at(t), hl=i if t >= R0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: o bang = so cong quang dang hien ; lan cuoi xong truoc het canh ; xe khong ra khoi ray."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, u, k = do_state(t)
        if t >= R0:
            _, _, d1, d2 = kin(ROWS[i], -1 if u is None else u)
            c = cells_at(t)[i]
            if (c[1], c[2]) != (d1 and u is not None, d2 and u is not None): bad.append(("bang/cong", round(t, 2)))
        t += 0.05
    if DO_END > sc["T"] - 0.2: bad.append(("lan 4 sat cuoi canh", round(DO_END, 2), round(sc["T"], 2)))
    for m2, v1, v in ROWS:
        x2_end = X2S + v * (run_len((m2, v1, v)) - 0.15 - (XC1 - X1S) / v1)
        if 65 + 0.88 * (sx(x2_end) + CL * PXM / 2) > 1040: bad.append(("cham mep phai", m2))
    return bad

# ---------------- canh 3: Ket qua (dap an + rut ra) ----------------
MX, VY, BY = 700, 640, 860             # px / kg ; px / (m/s) ; day hai hinh
def s_kq(img, d, t, sc):
    M = sc["M"]; m2, v1, v = ROWS[3]
    card(d, (40, 265, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 330), "Lần 4", 56, INK, anchor="lm")
    x0 = 150; w1 = M1 * MX; k1 = ease((t - 0.3) / 0.6); h1 = v1 * VY * k1
    if h1 > 2: d.rectangle([x0, BY - h1, x0 + w1, BY], fill=(254, 215, 170), outline=C1, width=5)
    if k1 > 0.95: text(d, (x0 + w1 / 2, BY - h1 - 40), vn(v1), 56, C1D)
    text(d, (x0 + w1 / 2, BY + 50), "trước", 56, C1D)
    x2 = 380; w2 = (M1 + m2) * MX; k2 = ease((t - 1.1) / 0.6); h2 = v * VY * k2
    if h2 > 2: d.rectangle([x2, BY - h2, x2 + w2, BY], fill=(221, 214, 254), outline=PURPLE, width=5)
    if k2 > 0.95: text(d, (x2 + w2 / 2, BY - h2 - 40), vn(v), 56, PURPLE)
    text(d, (x2 + w2 / 2, BY + 50), "sau", 56, PURPLE)
    d.line([(100, BY), (1000, BY)], fill=INK, width=4)
    card(d, (40, 1000, 1040, 1560), fill=WHITE, outline=LIGHT, w=3)
    ka = appear(t, M[1] - 0.6, 0.4)
    if ka > 0:
        text(d, (W / 2, 1090), "rộng = khối lượng", 60, INK, alpha=ka)
        d.line([(x2, 560), (x2 + w2, 560)], fill=A(NAVY, ka), width=5)
        for xx in (x2, x2 + w2): d.line([(xx, 540), (xx, 580)], fill=A(NAVY, ka), width=5)
    kb = appear(t, M[1] + 1.9, 0.4)
    if kb > 0:
        text(d, (W / 2, 1210), "cao = tốc độ", 60, INK, alpha=kb)
        xa = x0 + w1 + 40
        d.line([(xa, BY - v1 * VY), (xa, BY)], fill=A(NAVY, kb), width=5)
        for yy in (BY - v1 * VY, BY): d.line([(xa - 20, yy), (xa + 20, yy)], fill=A(NAVY, kb), width=5)
    kc = appear(t, M[1] + 4.4, 0.45)
    if kc > 0:
        card(d, (90, 1310, 990, 1480), fill=A((236, 253, 243), kc), r=24)
        text(d, (W / 2, 1395), "m₁·v₁ ≈ (m₁ + m₂)·v", 66, DGREEN, alpha=kc)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.3, 0.45)
    card(d, (40, 265, 1040, 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 335, "BẪY", RED, a1)
    q = "“Động năng cũng giữ nguyên”"
    ks = clamp((t - M[1]) / 0.4); f = F(62); lw = tw(d, q, f); yy = 470
    text(d, (W / 2, yy), q, 62, mix(INK, DRED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
    kk = appear(t, M[1] + 0.1, 0.45)
    if kk > 0:
        card(d, (40, 640, 1040, 1230), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
        text(d, (W / 2, 715), "Lần 1: động năng", 60, INK, alpha=kk)
        by, H0 = 1110, 300
        for j, (lab, fr, col, colD) in enumerate((("trước", 1.0, C1, C1D), ("sau", 0.46, PURPLE, PURPLE))):
            x = 330 + j * 380; g = ease((t - M[1] - 0.5 - 0.6 * j) / 0.5); h = H0 * fr * g
            if h > 2: d.rectangle([x - 90, by - h, x + 90, by], fill=col)
            text(d, (x, by + 55), lab, 56, colD, alpha=kk)
        d.line([(180, by), (900, by)], fill=INK, width=4)
        k3 = appear(t, M[1] + 2.0, 0.4)
        text(d, (710 + 120, by - H0 * 0.46 - 10), "≈ ½", 64, PURPLE, anchor="lm", alpha=k3)
    k5 = appear(t, M[2] + 0.1, 0.45)
    if k5 > 0:
        y0 = 1270 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 290), fill=A(WHITE, k5), outline=A(NAVY, k5), w=6)
        pill(d, W / 2, y0 + 70, "CHƯA NÓI ĐƯỢC", NAVY, k5)
        text(d, (W / 2, y0 + 200), "hai xe nảy ra, không dính", 60, INK, alpha=k5)

# ---------------- canh 5: THU NGHI (cau chot o khung web: m2 = 0,80 kg) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.2, 0.4)
    card(d, (40, 265, 1040, 1570), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 335, "THỬ NGHĨ", ORANGE, k)
    yb = 660
    d.rectangle([80, yb + 2, 1000, yb + 26], fill=A(RAIL, k), outline=A(NAVY, k))
    cart(d, yb, 0.25, C1, C1D, "1", 0, k, front="kim")
    cart(d, yb, 0.85, C2, C2D, "2", 0, k, rear="sap")
    text(d, (sx(0.25), yb - 190), vn(CHOT[0]) + " kg", 56, C1D, alpha=k)
    text(d, (sx(0.85), yb - 190), "? kg", 56, C2D, alpha=k)
    X = sx(0.25)
    arrow(d, (X - 70, yb + 75), (X + 80, yb + 75), A(C1, k), w=8, head=22)
    text(d, (X, yb + 140), vn(CHOT[1]) + " m/s", 56, C1D, alpha=k)
    text(d, (sx(0.85), yb + 100), "v = 0", 56, C2D, alpha=k)
    k1 = appear(t, 2.6, 0.45)
    text(d, (W / 2, 950), f"Dính nhau, đi {vn(CHOT[2])} m/s.", 62, INK, alpha=k * k1)
    k2 = appear(t, 5.0, 0.45)
    text(d, (W / 2, 1060), "Xe 2 nặng bao nhiêu?", 64, ORANGE, alpha=k2)
    seg_bar(d, 1160, t, 5.2, sc["T"] - 0.2, ORANGE, k2)
    kh = appear(t, 7.5, 0.45)
    if kh > 0:
        card(d, (90, 1300, 990, 1520), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 56, INK, alpha=kh)
        text(d, (W / 2, 1450), "sau va chạm, gì đang chạy?", 58, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, b, e = sc["hook"], sc["do"], sc["kq"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for j, (m2, v1, v) in enumerate(ROWS):                    # cong 2 hien so
        out.append((do["t0"] + STARTS[j] + 0.15 + (XC1 - X1S) / v1 + (G2 + 0.01 - X2S) / v, "tap"))
    out += [(kq["t0"] + 1.4, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 5.0, "open")]
    return out

CLIP = dict(id="tn-l10-baotoandl-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Bảo toàn động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe 1 đâm vào xe 2 đứng yên", draw=s_hook, tail=0.3, caps=[
   ("Xe 2 gắn sáp, đứng yên.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cổng quang đo tốc độ.", 3.4),
   ("Thêm gia trọng cho xe 2.", 5.6)]),
 dict(key="kq", title="Kết quả", draw=s_kq, tail=0.6, caps=[
   ("Đáp án: còn khoảng một phần tư.", 3.8),
   ("Hai hình gần bằng diện tích.", 4.8)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 2.5),
   ("Sai: dính nhau mất động năng.", 3.8),
   ("Thí nghiệm này còn thiếu gì?", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Đổi chiều câu hỏi.", 2.8),
   ("Dừng lại, tự tính.", 6.6)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("đồng bộ:", _kiem_dong_bo() or "không lệch")
