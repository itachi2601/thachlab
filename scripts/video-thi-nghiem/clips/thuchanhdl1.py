# Clip: tn-l10-thuchanhdl-01 - Va cham mem tren bang dem khi: do t qua cong quang, tinh p va p' (lo 9, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-thuchanhdl-01.json:
#   tham_so: s = 0,0500 m (tam can quang 5,00 cm) ; dong ho 0,001 s ; can 0,001 kg ; mat ~ 2,2 %
#   so_lieu_mau (lan, m1, m2, t1, t1', v1, p, v', p', delta %, eps %):
#     1 0,205 0,198 0,099 0,199 0,505 0,1035 0,251 0,1012 2,2 2,5 ; 2 0,405 0,198 0,101 0,153 ... ; 3 0,405 0,398 0,105 0,214 ...
# Trong tam (khac baotoandl1 cung khuon): DO THOI GIAN chan cong -> v = s/t -> p, p' -> so lech voi sai so.
#   Dong ho cong dem thoi gian that tam can quang che tia (dung o dung t1, t1').
# Hop trong bai ghi "Rut ra: tinh p va p' tung lan" -> clip CHI tinh lan 1 (trung vi du giai ngay sau hop), lan 2, 3 de HS.
#   Khong noi p' < p ca ba lan (sai so he thong) ; khong tinh lan 3 (Tu kiem tra Cau 1 hoi p lan 3 = 0,193).
# Du doan (K10), lan 1: t1 = 0,099 s ; hai xe dinh nhau qua cong 2 -> dong ho cong 2 chi khoang?
#   A. 0,050 s ; B. 0,099 s ; C. 0,20 s (DUNG, 0,199) ; D. 0,40 s.
# Bay = hien_tuong_hay_sai[0] (sau va cham quen m2): 0,205 . 0,251 = 0,0515 (them vao ghi_chu kho).
# Cau chot (ca tu suy, ghi trong ghi_chu kho): m1 = 0,305 kg, m2 = 0,198 kg, t1' = 0,169 s
#   -> v' = 0,0500/0,169 = 0,296 m/s ; p' = 0,503 . 0,296 = 0,1489 ~ 0,149 kg.m/s (chua hien).
from engine import *

ROWS = [(1, 0.205, 0.198, 0.099, 0.199), (2, 0.405, 0.198, 0.101, 0.153), (3, 0.405, 0.398, 0.105, 0.214)]
SW = 0.0500                                     # be rong tam can quang (m)
C1, C1D = ORANGE, (154, 52, 18)                 # xe 1
C2, C2D = BLUE, (30, 64, 175)                   # xe 2
RAIL = (148, 163, 184); RAIL_D = (100, 116, 139); LCD = (134, 239, 172)
NOTE = (60, 64, 84); DGREEN = (21, 110, 55); SAP = (161, 98, 7)
def vn(x, n=3): return f"{x:.{n}f}".replace(".", ",")

def _kiem_so():
    """Lan 1 tinh tren man: v, p lam tron theo gia_thiet kho ; bay ; chot."""
    bad = []
    n, m1, m2, t1, t1p = ROWS[0]
    v1 = round(SW / t1, 3); vp = round(SW / t1p, 3)
    if (v1, round(m1 * v1, 4), vp, round((m1 + m2) * vp, 4)) != (0.505, 0.1035, 0.251, 0.1012): bad.append("lan 1")
    if round(abs(0.1012 - 0.1035) / 0.1035 * 100, 1) != 2.2: bad.append("delta")
    if round((0.001 / m1 + 0.001 / t1 + 0.002 / (m1 + m2) + 0.001 / t1p) * 100, 1) != 2.5: bad.append("eps")
    if round(m1 * vp, 4) != 0.0515: bad.append("bay")
    v = 0.305 * 0.500 / 0.503 * (1 - 0.022)                     # chot: mo hinh kho, t1 = 0,100 s
    if round(SW / v, 3) != 0.169 or round(0.503 * round(SW / 0.169, 3), 4) != 0.1489: bad.append("chot")
    return bad

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

# ---------------- bang dem khi, hai cong quang, hai xe ----------------
X0, PXM = 60, 800
G1, G2 = 0.40, 0.86
CL = 0.14
X1S, X2S = 0.30, 0.66
XC1 = X2S - CL
def sx(s): return X0 + s * PXM

def track(d, yb, k=1.0):
    d.rectangle([X0, yb + 2, X0 + 1.2 * PXM, yb + 26], fill=A(RAIL, k), outline=A(NAVY, k))
    for i in range(1, 40): dot(d, X0 + i * 24, yb + 14, 3, A(RAIL_D, k))
    d.rectangle([90, yb + 26, 120, yb + 70], fill=A(RAIL_D, k)); d.rectangle([960, yb + 26, 990, yb + 70], fill=A(RAIL_D, k))

def gate_back(d, yb, g):
    x = sx(g); d.line([(x - 28, yb + 26), (x - 28, yb - 140)], fill=NAVY, width=7); d.line([(x + 28, yb + 26), (x + 28, yb - 140)], fill=NAVY, width=7)
def gate_front(d, yb, g):
    x = sx(g); d.line([(x - 32, yb - 140), (x + 32, yb - 140)], fill=NAVY, width=9)
    dot(d, x - 28, yb - 80, 7, RED); dot(d, x + 28, yb - 80, 7, RED)

def cart(d, yb, x, col, cold, label, n_gt=0, k=1.0, front=None, rear=None):
    """x = tam xe (m). Tam can quang rong SW (5,00 cm) ve dung ti le."""
    c = lambda cc: A(cc, k); w = CL * PXM / 2; X = sx(x); hw = SW * PXM / 2
    d.rectangle([X - hw, yb - 104, X + hw, yb - 46], fill=c(NAVY))
    slots = [(-44, 0), (44, 0), (-44, 1), (44, 1)]
    for j in range(n_gt):
        dx, lv = slots[j]
        d.rectangle([X + dx - 14, yb - 70 - 24 * lv, X + dx + 14, yb - 48 - 24 * lv], fill=c(GRAY), outline=c(NAVY), width=2)
    d.rounded_rectangle([X - w, yb - 46, X + w, yb - 2], radius=10, fill=c(col), outline=c(cold), width=3)
    text(d, (X, yb - 24), label, 40, WHITE, alpha=k)
    if front == "kim": d.polygon([(X + w, yb - 30), (X + w + 16, yb - 24), (X + w, yb - 18)], fill=c(NAVY))
    if rear == "sap": d.ellipse([X - w - 12, yb - 36, X - w + 6, yb - 12], fill=c(SAP))

def lcd(d, x, y, lab, val, col, hi=False):
    text(d, (x, y - 66), lab, 40, col)
    card(d, (x - 125, y - 40, x + 125, y + 40), fill=NAVY, r=14)
    text(d, (x, y), val, 44, YELLOW if hi else LCD)

def kin(row, u):
    """u: giay tu luc xe 1 chay. v1 = s/t1, v' = s/t1'. -> (x1, x2)."""
    n, m1, m2, t1, t1p = row; v1, vp = SW / t1, SW / t1p
    uc = (XC1 - X1S) / v1
    if u < uc: return X1S + v1 * max(0.0, u), X2S
    x2 = X2S + vp * (u - uc); return x2 - CL, x2

def gate_read(x, g, v, tp):
    """So dong ho: dem thoi gian tam can quang (tam x, rong SW) che tia o g; ra khoi tia thi dung o tp."""
    if x + SW / 2 < g: return 0.0, False
    e = (x + SW / 2 - g) / v
    return (tp, True) if e >= tp - 1e-9 else (e, False)

def run_len(row):
    n, m1, m2, t1, t1p = row
    return 0.15 + (XC1 - X1S) / (SW / t1) + (G2 + SW / 2 - X2S) / (SW / t1p) + 0.6

def rig(d, row, u, yb=700, k=1.0, hook=False):
    n, m1, m2, t1, t1p = row
    card(d, (40, 265, 1040, 830), fill=WHITE, outline=LIGHT, w=3)
    text(d, (70, 305), f"xe 1: {vn(m1)} kg", 42, C1D, anchor="lm", alpha=k)
    text(d, (1010, 305), f"xe 2: {vn(m2)} kg", 42, C2D, anchor="rm", alpha=k)
    if hook: x1, x2 = 0.47, X2S; r1, d1 = t1, True; r2, d2 = None, False
    else:
        x1, x2 = kin(row, u)
        r1, d1 = gate_read(x1, G1, SW / t1, t1); r2, d2 = gate_read(x2, G2, SW / t1p, t1p)
    lcd(d, sx(G1), 440, "cổng 1", f"{vn(r1)} s", C1D)
    lcd(d, sx(G2), 440, "cổng 2", "?" if hook else f"{vn(r2)} s", C2D, hi=d2)
    track(d, yb); gate_back(d, yb, G1); gate_back(d, yb, G2)
    cart(d, yb, x2, C2, C2D, "2", int(round((m2 - 0.198) / 0.1)), k, rear="sap")
    cart(d, yb, x1, C1, C1D, "1", int(round((m1 - 0.205) / 0.1)), k, front="kim")
    gate_front(d, yb, G1); gate_front(d, yb, G2)
    text(d, (70, yb + 90), "tấm cản quang rộng 5,00 cm", 40, NOTE, bold=False, anchor="lm")
    return (r1, d1), (r2, d2)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, ROWS[0], None, hook=True)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 870 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 250, "Hai xe dính nhau qua cổng 2. Đồng hồ cổng 2 chỉ khoảng?", 50, INK, maxw=880, alpha=a)
    text(d, (W / 2, y0 + 385), "Chọn đáp án ở khung câu hỏi", 38, NOTE, bold=False, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 440, 940, y0 + 454], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 440, 140 + 800 * (1 - p), y0 + 454], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (3 lan) ----------------
R0, FADE = 0.5, 0.2
STARTS = []
_s = R0
for _r in ROWS: STARTS.append(_s); _s += run_len(_r)
DO_END = _s

def do_state(t):
    if t < R0: return 0, None, 1.0
    i = max(j for j in range(3) if t >= STARTS[j]); w = t - STARTS[i]
    k = appear(w, 0.0, FADE) if i > 0 else 1.0
    if i < 2: k *= 1.0 - appear(w, run_len(ROWS[i]) - FADE, FADE)
    u = min(w, run_len(ROWS[i])) - 0.15                    # lan cuoi: xe dung yen sau luot (khong troi khoi bang)
    return i, (u if u >= 0 else None), k

XS = (110, 300, 500, 720, 920)
def table(d, cells, hl=None, y=860):
    card(d, (40, y, 1040, y + 450), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y + 58), "Lần", 42, INK)
    rs(d, XS[1], y + 52, "m_{1} (kg)", 44, C1D); rs(d, XS[2], y + 52, "m_{2} (kg)", 44, C2D)
    rs(d, XS[3], y + 52, "t_{1} (s)", 44, C1D); rs(d, XS[4], y + 52, "t_{1}′ (s)", 44, C2D)
    d.line([(70, y + 110), (1010, y + 110)], fill=LIGHT, width=3)
    for j, (cm, c1, c2) in enumerate(cells):
        n, m1, m2, t1, t1p = ROWS[j]; yy = y + 180 + j * 95
        if j == hl: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=20, fill=(255, 247, 237))
        text(d, (XS[0], yy), str(n), 46, INK if cm else MUTED)
        if cm: text(d, (XS[1], yy), vn(m1), 46, C1D); text(d, (XS[2], yy), vn(m2), 46, C2D)
        if c1: text(d, (XS[3], yy), vn(t1), 46, C1D)
        if c2: text(d, (XS[4], yy), vn(t1p), 46, C2D)

def cells_at(t):
    i, u, k = do_state(t); out = []
    for j in range(3):
        if t < R0 or j > i: out.append((False, False, False)); continue
        if j < i: out.append((True, True, True)); continue
        n, m1, m2, t1, t1p = ROWS[j]; x1, x2 = kin(ROWS[j], -1 if u is None else u)
        _, d1 = gate_read(x1, G1, SW / t1, t1); _, d2 = gate_read(x2, G2, SW / t1p, t1p)
        out.append((True, d1, d2))
    return out

def s_do(img, d, t, sc):
    i, u, k = do_state(t)
    rig(d, ROWS[i], -1 if u is None else u, k=k)
    table(d, cells_at(t), hl=i if t >= R0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: o bang = dong ho da dung ; so dung = t cua hang ; hai dong ho dung truoc khi het luot."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, u, k = do_state(t)
        if t >= R0:
            n, m1, m2, t1, t1p = ROWS[i]; x1, x2 = kin(ROWS[i], -1 if u is None else u)
            r1, d1 = gate_read(x1, G1, SW / t1, t1); r2, d2 = gate_read(x2, G2, SW / t1p, t1p)
            c = cells_at(t)[i]
            if (c[1], c[2]) != (d1, d2): bad.append(("bang/dong ho", round(t, 2)))
            if d1 and r1 != t1 or d2 and r2 != t1p: bad.append(("so dong ho", round(t, 2)))
            if x2 + CL / 2 > 1.18: bad.append(("ra khoi bang", round(t, 2)))
        t += 0.05
    for j, row in enumerate(ROWS):
        n, m1, m2, t1, t1p = row; x1, x2 = kin(row, run_len(row) - 0.15 - 0.6 + 0.01)
        if not gate_read(x2, G2, SW / t1p, t1p)[1]: bad.append(("cong 2 chua dung", n))
    if DO_END > sc["T"] - 0.2: bad.append(("lan 3 sat cuoi canh", round(DO_END, 2), round(sc["T"], 2)))
    return bad

# ---------------- canh 3: Dap an + tinh lan 1 ----------------
def badge(d, y, lab, col, alpha=1.0, size=40):
    pw = tw(d, lab, F(size)) + 56
    card(d, (W / 2 - pw / 2, y - 34, W / 2 + pw / 2, y + 34), fill=A(col, alpha), r=34)
    text(d, (W / 2, y), lab, size, WHITE, alpha=alpha)

def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.15, 0.4)
    badge(d, 300, "ĐÁP ÁN · khoảng 0,20 s", NAVY, ka)
    card(d, (40, 360, 1040, 560), fill=(236, 253, 243), outline=GREEN, w=5)
    rs(d, W / 2, 425, "Lần 1: t_{1}′ = 0,199 s ≈ 2·t_{1}", 48, DGREEN)
    text(d, (W / 2, 500), "→ hai xe chậm còn khoảng nửa", 42, DGREEN)
    k1 = appear(t, M[1] - 0.1, 0.4)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 960), fill=A(WHITE, k1), outline=A(NAVY, k1), w=5)
    text(d, (80, 660), "Lần 1 (kg·m/s)", 44, INK, anchor="lm", alpha=k1)
    rs(d, 120, 770, "trước:  p ≈ 0,1035", 48, C1D, alpha=appear(t, M[1] + 0.3, 0.4), anchor="l")
    rs(d, 120, 880, "sau:  p′ ≈ 0,1012", 48, C2D, alpha=appear(t, M[1] + 1.2, 0.4), anchor="l")

# ---------------- canh 4: So trong sai so ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 320), "Lần 1", 44, INK, anchor="lm")
    bx, S = 380, 200                                       # px / %
    for j, (lab, sub, v, col, at) in enumerate((("độ lệch", "δ", 2.2, ORANGE, 0.3), ("sai số đo", "ε", 2.5, GRAY, 1.0))):
        y = 470 + j * 190; g = ease((t - at) / 0.6)
        text(d, (bx - 30, y - 22), lab, 42, INK, anchor="rm")
        text(d, (bx - 30, y + 30), sub, 44, col if j == 0 else NOTE, anchor="rm")
        if g > 0:
            d.rounded_rectangle([bx, y - 40, bx + max(8, S * v * g), y + 40], radius=12, fill=col)
            if g > 0.95: text(d, (bx + S * v + 20, y), f"{vn(v, 1)} %", 46, INK, anchor="lm")
    kk = appear(t, M[0] + 2.0, 0.45)
    if kk > 0:
        card(d, (90, 790, 990, 920), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, 855), "δ ≤ ε: bảo toàn trong sai số", 48, DGREEN, alpha=kk)
    k5 = appear(t, M[1] - 0.1, 0.45)
    if k5 > 0:
        y0 = 1000 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 290), fill=A((254, 242, 242), k5), outline=A(RED, k5), w=5)
        text(d, (W / 2, y0 + 62), "Chưa nói được", 44, NAVY, alpha=k5)
        rs(d, W / 2, y0 + 170, "lần 2, 3 có còn p′ < p?", 48, RED, alpha=k5)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.2, 0.45)
    card(d, (40, 265, 1040, 640), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    badge(d, 322, "BẪY", RED, a1, 38)
    ks = clamp((t - M[0] - 1.2) / 0.4)
    q = "p′ = 0,205 · 0,251 ≈ 0,0515"
    f = F(48); lw = tw(d, q, f); yy = 440
    rs(d, W / 2, yy, q, 48, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * a1), width=5)
    text(d, (W / 2 + lw / 2 + 50, yy), "✗", 60, RED, alpha=ks)
    text(d, (W / 2, 550), "“mất nửa động lượng?”", 44, mix(INK, MUTED, ks), alpha=a1)
    kk = appear(t, M[1] - 0.1, 0.45)
    if kk <= 0: return
    card(d, (40, 680, 1040, 1380), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
    yb = 960
    track(d, yb, kk)
    cart(d, yb, 0.62, C2, C2D, "2", 0, kk, rear="sap")
    cart(d, yb, 0.48, C1, C1D, "1", 0, kk, front="kim")
    X1, X2 = sx(0.48), sx(0.62); w = CL * PXM / 2
    text(d, (X1 - 70, yb - 150), "0,205 kg", 42, C1D, alpha=kk)
    text(d, (X2 + 60, yb - 205), "0,198 kg", 42, C2D, alpha=kk)
    k2 = appear(t, M[1] + 0.6, 0.4)
    if k2 > 0:
        y = yb + 80
        d.line([(X1 - w, y), (X2 + w, y)], fill=A(DGREEN, k2), width=4)
        for xx in (X1 - w, X2 + w): d.line([(xx, y - 16), (xx, y)], fill=A(DGREEN, k2), width=4)
        text(d, ((X1 + X2) / 2, y + 50), "cả hai xe cùng chạy", 42, DGREEN, alpha=k2)
    k3 = appear(t, M[1] + 1.4, 0.4)
    rs(d, W / 2, 1260, "p′ = 0,403 · 0,251 ≈ 0,1012 ✓", 48, DGREEN, alpha=k3)

# ---------------- canh 6: Chot ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        if k < 0.02: return
        yb = 1150
        track(d, yb, k)
        x = sx(0.86); d.line([(x - 28, yb + 26), (x - 28, yb - 140)], fill=A(NAVY, k), width=7)
        cart(d, yb, 0.70, C2, C2D, "2", 0, k, rear="sap")
        cart(d, yb, 0.56, C1, C1D, "1", 1, k, front="kim")
        d.line([(x + 28, yb + 26), (x + 28, yb - 140)], fill=A(NAVY, k), width=7)
        d.line([(x - 32, yb - 140), (x + 32, yb - 140)], fill=A(NAVY, k), width=9)
        text(d, (sx(0.56) - 40, 975), "0,305 kg", 42, C1D, alpha=k)
        text(d, (sx(0.70), yb + 85), "0,198 kg", 42, C2D, alpha=k)
        card(d, (x - 120, 940, x + 120, 1010), fill=A(NAVY, k), r=14)
        text(d, (x, 975), "0,169 s", 44, A(LCD, k), alpha=k)
        kh = appear(t, M[0] + 2.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1290, 970, 1520), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1350), "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1440, "Tấm cản quang vẫn rộng 5,00 cm", 42, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Lệch nhỏ hơn sai số: vẫn là bảo toàn",
             "Lần mới, cổng 2 chỉ 0,169 s. Động lượng p′ bằng bao nhiêu?", None, body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for j, row in enumerate(ROWS):                            # dong ho cong 2 dung
        n, m1, m2, t1, t1p = row
        out.append((do["t0"] + STARTS[j] + 0.15 + (XC1 - X1S) / (SW / t1) + (G2 + SW / 2 - X2S) / (SW / t1p), "tap"))
    out += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l10-thuchanhdl-01", header="VẬT LÍ 10 · THỰC HÀNH", footer="Thực hành động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo thời gian chắn cổng quang", draw=s_hook, tail=0.6, caps=[
   ("Cổng quang đo thời gian.", 3.0),
   ("Dừng video, chọn câu trả lời.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đọc số đầu tiên mỗi cổng.", 3.4),
   ("Thêm gia trọng, làm ba lần.", 3.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Thời gian gấp đôi, tốc độ nửa.", 3.4),
   ("Lần 1: p′ hơi nhỏ hơn p.", 4.0)]),
 dict(key="rutra", title="So p′ với p", draw=s_rutra, tail=0.5, caps=[
   ("Độ lệch nhỏ hơn sai số đo.", 3.4),
   ("Lần 2, 3: em tự tính.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Sau va chạm chỉ nhân m1?", 3.0),
   ("Hai xe dính, cùng chạy.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự tính.", 6.0)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("số:", _kiem_so() or "khớp kho"); print("đồng bộ:", _kiem_dong_bo() or "không lệch")
