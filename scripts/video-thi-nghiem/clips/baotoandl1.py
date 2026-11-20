# Clip: tn-l10-baotoandl-01 - Va cham mem tren ray dem khi, cong quang do v (lo 9, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-baotoandl-01.json:
#   tham_so: m1 = 0,20 kg (co dinh) ; m2 0,1-1,0 kg ; gia trong 0,10 kg
#   so_lieu_mau (m2, v1, v): 0,2 0,52 0,25 ; 0,3 0,60 0,24 ; 0,4 0,57 0,19 ; 0,6 0,66 0,16
#   rut_ra: Wd sau / Wd truoc = m1/(m1 + m2) -> lan 1 (m2 = m1) con 1/2.
# Trong tam (khac thuchanhdl1 cung khuon): TOC DO sau va cham, m1.v1 ~ (m1 + m2).v (hinh chu nhat "khoi luong x toc do").
# KHONG tinh p truoc / p sau tung lan, khong % lech: cau "Doc so lieu" ngay sau hop bat HS tu tinh.
#   Khong noi ma sat (cau sau hop hoi vi sao p sau thuong khong lon hon p truoc).
# Du doan (K10: chi cau hoi + hinh), lan 1 m2 = m1 = 0,20 kg, v1 = 0,52 m/s: hai xe dinh nhau di voi toc do?
#   A. Van 0,52 m/s ; B. Khoang 0,26 m/s (DUNG, do duoc 0,25) ; C. Khoang 0,13 m/s ; D. Dung han.
# Bay = hien_tuong_hay_sai[1] (dong nang cung bao toan) -> lan 1 dong nang con 1/2.
# Cau chot (ca tu suy, ghi trong ghi_chu kho): m2 = 0,30 kg, v1 = 0,75 m/s -> v = 0,20.0,75/0,50 = 0,30 m/s (chua hien).
from engine import *

ROWS = [(0.2, 0.52, 0.25), (0.3, 0.60, 0.24), (0.4, 0.57, 0.19), (0.6, 0.66, 0.16)]   # m2, v1, v
M1 = 0.20
C1, C1D = ORANGE, (154, 52, 18)                 # xe 1
C2, C2D = BLUE, (30, 64, 175)                   # xe 2
RAIL = (148, 163, 184); RAIL_D = (100, 116, 139); LCD = (134, 239, 172)
NOTE = (60, 64, 84); DGREEN = (21, 110, 55); SAP = (161, 98, 7)
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

TOK2 = re.compile(r"(_\{[^}]*\})")
def rs(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chu co chi so duoi; chi so >= 40 px."""
    sub = max(40, int(size * 0.72)); segs = []
    for p in [p for p in TOK2.split(s) if p]:
        segs.append((p[2:-1], sub, size * 0.30) if p.startswith("_{") else (p, size, 0))
    tot = sum(tw(d, x, F(z)) for x, z, _ in segs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for s_, z, dy in segs:
        dtext(d, (x, cy + dy), s_, F(z), color, alpha, "lm"); x += tw(d, s_, F(z))
    return tot

# ---------------- ray dem khi, hai cong quang, hai xe ----------------
X0, PXM = 60, 800                     # px tai s = 0 ; px / m (ray 1,20 m)
G1, G2 = 0.40, 0.86                   # vi tri cong (m)
CL = 0.14                             # chieu dai xe (m)
X1S, X2S = 0.30, 0.66                 # tam xe 1 luc bat dau, tam xe 2 dung yen
XC1 = X2S - CL                        # tam xe 1 luc cham xe 2
def sx(s): return X0 + s * PXM

def track(d, yb):
    d.rectangle([X0, yb + 2, X0 + 1.2 * PXM, yb + 26], fill=RAIL, outline=NAVY)
    for i in range(1, 40): dot(d, X0 + i * 24, yb + 14, 3, RAIL_D)
    d.rectangle([90, yb + 26, 120, yb + 70], fill=RAIL_D); d.rectangle([960, yb + 26, 990, yb + 70], fill=RAIL_D)

def gate_back(d, yb, g):
    x = sx(g); d.line([(x - 28, yb + 26), (x - 28, yb - 140)], fill=NAVY, width=7); d.line([(x + 28, yb + 26), (x + 28, yb - 140)], fill=NAVY, width=7)
def gate_front(d, yb, g):
    x = sx(g); d.line([(x - 32, yb - 140), (x + 32, yb - 140)], fill=NAVY, width=9)
    dot(d, x - 28, yb - 80, 7, RED); dot(d, x + 28, yb - 80, 7, RED)

def cart(d, yb, x, col, cold, label, n_gt=0, k=1.0, front=None, rear=None):
    """x = tam xe (m). n_gt: so gia trong 0,10 kg tren xe. front/rear: 'kim' | 'sap' o dau phai / dau trai."""
    c = lambda cc: A(cc, k); w = CL * PXM / 2; X = sx(x)
    d.rectangle([X - 6, yb - 100, X + 6, yb - 46], fill=c(NAVY))                  # tam can quang
    slots = [(-30, 0), (30, 0), (-30, 1), (30, 1)]
    for j in range(n_gt):
        dx, lv = slots[j]
        d.rectangle([X + dx - 15, yb - 70 - 24 * lv, X + dx + 15, yb - 48 - 24 * lv], fill=c(GRAY), outline=c(NAVY), width=2)
    d.rounded_rectangle([X - w, yb - 46, X + w, yb - 2], radius=10, fill=c(col), outline=c(cold), width=3)
    text(d, (X, yb - 24), label, 40, WHITE, alpha=k)
    if front == "kim": d.polygon([(X + w, yb - 30), (X + w + 16, yb - 24), (X + w, yb - 18)], fill=c(NAVY))
    if rear == "sap": d.ellipse([X - w - 12, yb - 36, X - w + 6, yb - 12], fill=c(SAP))

def lcd(d, x, y, lab, val, col, hi=False):
    text(d, (x, y - 66), lab, 40, col)
    card(d, (x - 125, y - 40, x + 125, y + 40), fill=NAVY, r=14)
    text(d, (x, y), val, 44, YELLOW if hi else LCD)

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

def rig(d, row, u, yb=700, k=1.0, r2_txt=None):
    """Hinh trong the y 265-820. u = None: xe 1 dung o vi tri hook."""
    m2, v1, v = row
    card(d, (40, 265, 1040, 845), fill=WHITE, outline=LIGHT, w=3)
    text(d, (70, 305), f"xe 1: {vn(M1)} kg", 42, C1D, anchor="lm", alpha=k)
    text(d, (1010, 305), f"xe 2: {vn(m2)} kg", 42, C2D, anchor="rm", alpha=k)
    if u is None: x1, x2, d1, d2 = 0.47, X2S, True, False
    else: x1, x2, d1, d2 = kin(row, u)
    lcd(d, sx(G1), 440, "cổng 1", f"{vn(v1)} m/s" if d1 else "– – –", C1D)
    lcd(d, sx(G2), 440, "cổng 2", r2_txt or (f"{vn(v)} m/s" if d2 else "– – –"), C2D, hi=d2)
    track(d, yb); gate_back(d, yb, G1); gate_back(d, yb, G2)
    n_gt = int(round((m2 - 0.2) / 0.1))
    cart(d, yb, x2, C2, C2D, "2", n_gt, k, rear="sap")
    cart(d, yb, x1, C1, C1D, "1", 0, k, front="kim")
    gate_front(d, yb, G1); gate_front(d, yb, G2)
    return x1, x2

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; yb = 700
    rig(d, ROWS[0], None, yb, r2_txt="?")
    x1 = sx(0.47)
    arrow(d, (x1 - 60, yb + 70), (x1 + 60, yb + 70), C1, w=7, head=20)
    rs(d, x1, yb + 108, "v_{1} xe 1", 42, C1D)
    text(d, (sx(X2S) + 60, yb + 80), "đứng yên", 40, C2D)
    text(d, (sx(X2S) - CL * PXM / 2 - 30, yb - 150), "sáp", 40, SAP)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 875 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 250, "Dính nhau rồi, hai xe đi với tốc độ nào?", 50, INK, maxw=880, alpha=a)
    text(d, (W / 2, y0 + 385), "Chọn đáp án ở khung câu hỏi", 38, NOTE, bold=False, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 440, 940, y0 + 454], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 440, 140 + 800 * (1 - p), y0 + 454], radius=7, fill=A(PURPLE, a))

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
    u = min(w, run_len(ROWS[i])) - 0.15                    # lan cuoi: xe dung yen sau luot
    return i, (u if u >= 0 else None), k

XS = (130, 360, 610, 860)
def table(d, cells, hl=None, y=875):
    card(d, (40, y, 1040, y + 540), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y + 58), "Lần", 42, INK)
    rs(d, XS[1], y + 52, "m_{2} (kg)", 44, C2D); rs(d, XS[2], y + 52, "v_{1} (m/s)", 44, C1D)
    text(d, (XS[3], y + 58), "v (m/s)", 44, INK)
    text(d, (XS[3], y + 108), "hai xe", 40, MUTED, bold=False)
    d.line([(70, y + 140), (1010, y + 140)], fill=LIGHT, width=3)
    for j, (cm, c1, c2) in enumerate(cells):
        m2, v1, v = ROWS[j]; yy = y + 205 + j * 90
        if j == hl: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=20, fill=(255, 247, 237))
        text(d, (XS[0], yy), str(j + 1), 46, INK if cm else MUTED)
        if cm: text(d, (XS[1], yy), vn(m2), 46, C2D)
        if c1: text(d, (XS[2], yy), vn(v1), 46, C1D)
        if c2: text(d, (XS[3], yy), vn(v), 46, INK)

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
    """Moi 0,05 s: o bang = so cong quang dang hien ; lan cuoi xong truoc het canh."""
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
    for m2, v1, v in ROWS:                                      # hai xe dinh nhau khong ra khoi ray
        x2_end = X2S + v * (run_len((m2, v1, v)) - 0.15 - (XC1 - X1S) / v1)
        if x2_end + CL / 2 > 1.18: bad.append(("ra khoi ray", m2))
    return bad

# ---------------- canh 3: Dap an ----------------
def badge(d, y, lab, col, alpha=1.0, size=40):
    pw = tw(d, lab, F(size)) + 56
    card(d, (W / 2 - pw / 2, y - 34, W / 2 + pw / 2, y + 34), fill=A(col, alpha), r=34)
    text(d, (W / 2, y), lab, size, WHITE, alpha=alpha)

def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.15, 0.4)
    badge(d, 300, "ĐÁP ÁN · khoảng một nửa", NAVY, ka)
    card(d, (40, 360, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 410), "Lần 1", 42, INK, anchor="lm")
    bx = 330; S = 900                                        # px / (m/s)
    for j, (lab, v, col, at) in enumerate((("xe 1 trước", 0.52, C1, 0.4), ("hai xe sau", 0.25, PURPLE, 1.0))):
        y = 540 + j * 170; kk = ease((t - at) / 0.6)
        text(d, (bx - 24, y), lab, 42, C1D if j == 0 else PURPLE, anchor="rm")
        if kk > 0:
            d.rounded_rectangle([bx, y - 36, bx + max(8, S * v * kk), y + 36], radius=12, fill=col)
            if kk > 0.95: text(d, (bx + S * v + 20, y), f"{vn(v)} m/s", 44, INK, anchor="lm")
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 <= 0: return
    # cot v (hai xe) ca 4 lan, truc tu 0, cung ti le 0-0,30 m/s
    card(d, (40, 940, 1040, 1460), fill=A(WHITE, k2), outline=A(LIGHT, k2), w=3)
    rs(d, 120, 990, "v (m/s)", 42, INK, alpha=k2, anchor="l")
    by, top = 1330, 1060
    def yv(v): return by - v / 0.30 * (by - top)
    d.line([(150, by), (960, by)], fill=A(INK, k2), width=4)
    for j, (m2, v1, v) in enumerate(ROWS):
        cx = 260 + j * 200; g = ease((t - M[1] - 0.1 - 0.3 * j) / 0.45); h = (by - yv(v)) * g
        if h > 2: d.rectangle([cx - 55, by - h, cx + 55, by], fill=PURPLE)
        if g > 0.95: text(d, (cx, yv(v) - 32), vn(v), 42, INK)
        text(d, (cx, by + 42), vn(m2, 1), 42, C2D, alpha=k2)
    rs(d, 960, by + 100, "m_{2} (kg)", 42, C2D, alpha=k2, anchor="r")

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1010), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 315), "Lần 4", 42, INK, anchor="lm")
    by = 880; MX, VY = 700, 700                              # px / kg ; px / (m/s), cung ti le cho hai hinh
    m2, v1, v = ROWS[3]
    # truoc: chu nhat rong m1, cao v1 (xe 1) ; sau: rong m1 + m2, cao v (hai xe)
    k1 = ease((t - 0.3) / 0.6)
    x0 = 100; w1 = M1 * MX; h1 = v1 * VY * k1
    if h1 > 2: d.rectangle([x0, by - h1, x0 + w1, by], fill=(254, 215, 170), outline=C1, width=4)
    text(d, (x0 + w1 / 2, by + 46), "trước", 42, C1D)
    k2 = ease((t - 1.0) / 0.6)
    x2 = 300; w2 = (M1 + m2) * MX; h2 = v * VY * k2
    if h2 > 2: d.rectangle([x2, by - h2, x2 + w2, by], fill=(221, 214, 254), outline=PURPLE, width=4)
    text(d, (x2 + w2 / 2, by + 46), "sau", 42, PURPLE)
    ka = appear(t, M[0] + 1.0, 0.4)
    text(d, (690, 470), "rộng: khối lượng", 40, INK, alpha=ka)
    text(d, (690, 530), "cao: tốc độ", 40, INK, alpha=ka)
    kb = appear(t, M[0] + 2.2, 0.45)
    if kb > 0:
        card(d, (110, 1040, 970, 1170), fill=A((236, 253, 243), kb), r=24)
        rs(d, W / 2, 1105, "m_{1}·v_{1} ≈ (m_{1} + m_{2})·v", 50, DGREEN, alpha=kb)
    k5 = appear(t, M[1] - 0.1, 0.45)
    if k5 > 0:
        y0 = 1200 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 270), fill=A((254, 242, 242), k5), outline=A(RED, k5), w=5)
        text(d, (W / 2, y0 + 62), "Thí nghiệm chưa nói được", 44, NAVY, alpha=k5)
        ctext(d, y0 + 170, "hai xe nảy ra, không dính", 46, RED, alpha=k5)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.2, 0.45)
    card(d, (40, 265, 1040, 700), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    badge(d, 322, "BẪY", RED, a1, 38)
    q1, q2 = "“Động lượng giữ nguyên", "thì động năng cũng vậy”"
    ks = clamp((t - M[0] - 1.0) / 0.4); f = F(46)
    for j, q in enumerate((q1, q2)):
        yy = 450 + j * 70; lw = tw(d, q, f)
        text(d, (W / 2, yy), q, 46, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * a1), width=5)
    text(d, (W / 2 + 380, 485), "✗", 60, RED, alpha=ks)
    kk = appear(t, M[1] - 0.1, 0.45)
    if kk <= 0: return
    card(d, (40, 740, 1040, 1450), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
    text(d, (W / 2, 800), "Lần 1: động năng hai xe", 44, INK, alpha=kk)
    by, H0 = 1260, 340
    for j, (lab, fr, col, colD) in enumerate((("trước", 1.0, C1, C1D), ("sau", 0.5, PURPLE, PURPLE))):
        x = 340 + j * 400; g = ease((t - M[1] - 0.2 - 0.5 * j) / 0.5); h = H0 * fr * g
        if h > 2: d.rectangle([x - 80, by - h, x + 80, by], fill=col)
        text(d, (x, by + 46), lab, 42, colD, alpha=kk)
    d.line([(200, by), (880, by)], fill=INK, width=4)
    k3 = appear(t, M[1] + 1.3, 0.4)
    text(d, (740 + 120, by - H0 / 2 - 10), "≈ ½", 52, PURPLE, anchor="lm", alpha=k3)
    ctext(d, 1395, "Va chạm mềm: động năng giảm", 44, DGREEN, alpha=k3)

# ---------------- canh 6: Chot ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        if k < 0.02: return
        yb = 1120; y = yb
        d.rectangle([80, yb + 2, 1000, yb + 26], fill=A(RAIL, k), outline=A(NAVY, k))
        cart(d, yb, 0.22, C1, C1D, "1", 0, k, front="kim")
        cart(d, yb, 0.62, C2, C2D, "2", 1, k, rear="sap")
        text(d, (sx(0.22), yb - 160), "0,20 kg", 42, C1D, alpha=k)
        text(d, (sx(0.62), yb - 160), "0,30 kg", 42, C2D, alpha=k)
        X = sx(0.22)
        arrow(d, (X - 60, yb + 70), (X + 70, yb + 70), A(C1, k), w=7, head=20)
        text(d, (X, yb + 120), "0,75 m/s", 42, C1D, alpha=k)
        text(d, (sx(0.62), yb + 70), "đứng yên", 40, C2D, alpha=k)
        kh = appear(t, M[0] + 2.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1520), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1440, "Xe 2 lúc đầu đứng yên", 44, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Dính nhau: đi chung, chậm hơn xe 1",
             "Hai xe dính nhau chạy với tốc độ nào?", None, body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for j, (m2, v1, v) in enumerate(ROWS):                    # cong 2 hien so
        out.append((do["t0"] + STARTS[j] + 0.15 + (XC1 - X1S) / v1 + (G2 + 0.01 - X2S) / v, "tap"))
    out += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l10-baotoandl-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Bảo toàn động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe 1 đâm vào xe 2 đứng yên", draw=s_hook, tail=0.6, caps=[
   ("Ray đệm khí nằm ngang.", 3.0),
   ("Dừng video, chọn câu trả lời.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cổng quang đo tốc độ.", 3.6),
   ("Thêm gia trọng cho xe 2.", 5.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Lần 1: còn khoảng một nửa.", 3.0),
   ("Xe 2 càng nặng, càng chậm.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Hai hình gần bằng diện tích.", 3.4),
   ("Còn điều gì chưa thử?", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Động năng có giữ nguyên không?", 3.2),
   ("Hai xe dính nhau mất động năng.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("đồng bộ:", _kiem_dong_bo() or "không lệch")
