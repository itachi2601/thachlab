# Clip: tn-l10-baotoandl-02 - Hai xe cung khoi luong, dem lo xo la: va cham gan dan hoi (lo 9, 18/11/2026; dung lai
# 27/11/2026 theo cong moi L10b: chu >= 55 px khi ve, nhip >= 2,5 s, K10 khong nut A-D, Bay hinh tu giai thich, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-baotoandl-02.json (_kiem_so() doi chieu):
#   tham_so: m = 0,20 kg moi xe ; v1 0,1-1,0 m/s
#   so_lieu_mau (v1, v1', v2'): 0,3 0 0,3 ; 0,5 0 0,5 ; 0,8 0 0,8 (mo hinh dan hoi li tuong; xe that mat vai %)
# Du doan (DOI CA 27/11: ban cu hoi "moi xe chay the nao" o v1 = 0,50 trung phuong an cau bi-a "bi cai dung, bi do di
#   tiep" cua bai): LAN 3, xe 1 toi 0,80 m/s, xe 2 dung yen -> xe 2 bi day di nhanh co nao?
#   Khung web: A. 0,40 m/s ; B. 0,80 m/s (DUNG) ; C. 1,2 m/s ; D. 1,6 m/s.
# Ket qua (lan 3): mui ten dong luong truoc/sau + cot dong nang xe 1 truoc = xe 2 sau (gan dan hoi).
# Bay = hien_tuong_hay_sai[0] (nham voi va cham mem) o LAN 2 (cap so khac Du doan): dinh (sap) 0,25 m/s (ghi_chu kho)
#   canh lo xo la: xe 1 dung, xe 2 0,50 m/s. Chua noi duoc: hai xe khac khoi luong.
# Khong viet cong thuc v1', v2' (hop "Mo rong" ngay sau hop trong bai).
# Cau chot (ca tu suy, ghi trong ghi_chu kho): xe 2 dang chay 0,20 m/s cung chieu, xe 1 toi 0,60 m/s
#   -> v1' = 0,20 m/s ; v2' = 0,60 m/s (cong thuc mo_hinh kho, m1 = m2). Can buoc tong quat "doi van toc" clip chua chieu.
from engine import *

ROWS = [(0.3, 0.0, 0.3), (0.5, 0.0, 0.5), (0.8, 0.0, 0.8)]   # v1, v1', v2'
MX = 0.20
C1, C1D = ORANGE, (154, 52, 18)                 # xe 1
C2, C2D = BLUE, (30, 64, 175)                   # xe 2
RAIL = (148, 163, 184); RAIL_D = (100, 116, 139); LCD = (134, 239, 172)
NOTE = (60, 64, 84); DGREEN = (21, 110, 55); LEAF = (71, 85, 105); DRED = (185, 28, 28); EMPTY = (148, 140, 128)
DORANGE = (176, 64, 8)
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-baotoandl-02.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS and {p["ky_hieu"]: p for p in k["tham_so"]}["m"]["gia_tri"] == MX
    gc = k["so_lieu_mau"]["ghi_chu"]; assert "0,25 m/s" in gc and "v1' = 0,20 m/s, v2' = 0,60 m/s" in gc
    def el(m1, m2, v1, v2): return ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2), ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
    for v1, a, b in ROWS: assert all(abs(x - y) < 1e-9 for x, y in zip(el(MX, MX, v1, 0.0), (a, b)))
    assert [round(x, 2) for x in el(MX, MX, 0.60, 0.20)] == [0.20, 0.60] and round(MX * 0.50 / (2 * MX), 2) == 0.25
_kiem_so()

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

# ---------------- ray dem khi, hai cong quang, hai xe co vong lo xo la ----------------
X0, PXM = 60, 800                     # mp4 x = 65 + 0,88 x
G1, G2 = 0.40, 0.86
CL, RING = 0.14, 0.04                 # chieu dai xe ; be day vong lo xo la (m) gan dau xe 1
X1S, X2S, X2STOP = 0.28, 0.66, 1.06   # tam xe 2 dung o chan cuoi ray
XC1 = X2S - CL - RING                 # tam xe 1 luc vong lo xo cham xe 2
TC = 0.08                             # thoi gian tiep xuc (s)
YB = 790
def sx(s): return X0 + s * PXM

def track(d, yb, k=1.0, stop=True):
    d.rectangle([X0, yb + 2, X0 + 1.2 * PXM, yb + 26], fill=A(RAIL, k), outline=A(NAVY, k))
    for i in range(1, 40): dot(d, X0 + i * 24, yb + 14, 3, A(RAIL_D, k))
    d.rectangle([90, yb + 26, 120, yb + 60], fill=A(RAIL_D, k)); d.rectangle([960, yb + 26, 990, yb + 60], fill=A(RAIL_D, k))
    if stop:
        xs = sx(X2STOP + CL / 2); d.rectangle([xs, yb - 40, xs + 16, yb + 2], fill=A(NAVY, k))      # chan cuoi ray

def gate_back(d, yb, g):
    x = sx(g)
    for dx in (-30, 30): d.line([(x + dx, yb + 26), (x + dx, yb - 175)], fill=NAVY, width=7)
def gate_front(d, yb, g):
    x = sx(g); d.line([(x - 34, yb - 175), (x + 34, yb - 175)], fill=NAVY, width=9)
    dot(d, x - 30, yb - 110, 8, RED); dot(d, x + 30, yb - 110, 8, RED)

def cart(d, yb, x, col, cold, label, k=1.0, ring=None):
    """x = tam xe (m). ring = be day vong lo xo la (m) o dau phai (None: khong co). Xe cao 74 px, nhan 56 px."""
    c = lambda cc: A(cc, k); w = CL * PXM / 2; X = sx(x)
    d.rectangle([X - 6, yb - 132, X + 6, yb - 76], fill=c(NAVY))
    d.rounded_rectangle([X - w, yb - 76, X + w, yb - 2], radius=12, fill=c(col), outline=c(cold), width=3)
    text(d, (X, yb - 39), label, 56, WHITE, alpha=k)
    if ring is not None:
        rw = max(4, ring * PXM)
        d.ellipse([X + w - 4, yb - 66, X + w - 4 + rw, yb - 12], outline=c(LEAF), width=6)

def lcd(d, x, y, lab, val, col, hi=False):
    text(d, (x, y - 80), lab, 56, col)
    card(d, (x - 150, y - 44, x + 150, y + 44), fill=NAVY, r=14)
    text(d, (x, y), val, 56, YELLOW if hi else LCD)

def kin(v1, u):
    """u: giay tu luc xe 1 chay. -> (x1, x2, be day vong). Tiep xuc: luc lo xo coi nhu khong doi trong TC."""
    uc = (XC1 - X1S) / v1
    if u < uc: return X1S + v1 * max(0.0, u), X2S, RING
    tau = u - uc
    if tau < TC:
        a = v1 / TC
        x1 = XC1 + v1 * tau - a * tau * tau / 2; x2 = X2S + a * tau * tau / 2
        return x1, x2, RING - (v1 * tau - a * tau * tau)
    x1 = XC1 + v1 * TC / 2
    x2 = min(X2STOP, X2S + v1 * TC / 2 + v1 * (tau - TC))
    return x1, x2, RING

def run_len(v1):
    return 0.15 + (XC1 - X1S) / v1 + TC + (G2 + 0.01 - X2S - v1 * TC / 2) / v1 + 0.6

def rig(d, v1, u, k=1.0, x1_hook=None, yc=880):
    card(d, (40, 265, 1040, yc), fill=WHITE, outline=LIGHT, w=3)
    text(d, (70, 320), f"xe 1: {vn(MX)} kg", 56, C1D, anchor="lm", alpha=k)
    text(d, (1010, 320), f"xe 2: {vn(MX)} kg", 56, C2D, anchor="rm", alpha=k)
    if x1_hook is not None: x1, x2, rg = x1_hook, X2S, RING
    else: x1, x2, rg = kin(v1, u)
    hook = x1_hook is not None
    d1 = x1 >= G1 + 0.01; d2 = (not hook) and x2 >= G2 + 0.01
    lcd(d, sx(G1) - 20, 495, "cổng 1", f"{vn(v1)} m/s" if d1 else "– – –", C1D)
    lcd(d, sx(G2) + 20, 495, "cổng 2", "?" if hook else (f"{vn(v1)} m/s" if d2 else "– – –"), C2D, hi=d2)
    track(d, YB); gate_back(d, YB, G1); gate_back(d, YB, G2)
    cart(d, YB, x2, C2, C2D, "2", k)
    cart(d, YB, x1, C1, C1D, "1", k, ring=rg)
    gate_front(d, YB, G1); gate_front(d, YB, G2)
    return x1, x2, d1, d2

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
VH = ROWS[2][0]                                   # lan 3: 0,80 m/s
def s_hook(img, d, t, sc):
    M = sc["M"]
    x1 = lerp(0.16, 0.45, ease((t - 0.6) / 1.9))
    rig(d, VH, None, x1_hook=x1, yc=930)
    text(d, (sx(X2S) + 175, YB + 80), "v = 0", 56, C2D)
    xr = sx(x1) + CL * PXM / 2 + 16
    d.line([(xr, YB - 14), (xr - 40, YB + 46)], fill=LEAF, width=4)
    text(d, (xr - 60, YB + 80), "lò xo lá", 56, LEAF)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 965 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Xe 2 bị đẩy đi", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "nhanh cỡ nào?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 410, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (3 lan) ----------------
R0, FADE = 0.5, 0.2
STARTS = []
_s = R0
for _r in ROWS: STARTS.append(_s); _s += run_len(_r[0])
DO_END = _s

def do_state(t):
    if t < R0: return 0, None, 1.0
    i = max(j for j in range(3) if t >= STARTS[j]); w = t - STARTS[i]; L = run_len(ROWS[i][0])
    k = appear(w, 0.0, FADE) if i > 0 else 1.0
    if i < 2: k *= 1.0 - appear(w, L - FADE, FADE)
    u = min(w, L) - 0.15
    return i, (u if u >= 0 else None), k

def stopped(v1, u):
    return u is not None and u >= (XC1 - X1S) / v1 + TC

XS = (120, 370, 630, 890)
def table(d, cells, hl=None, y=920):
    card(d, (40, y, 1040, y + 560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y + 65), "Lần", 56, INK)
    text(d, (XS[1], y + 65), "v₁", 60, C1D); text(d, (XS[2], y + 65), "v₁′", 60, C1D); text(d, (XS[3], y + 65), "v₂′", 60, C2D)
    d.line([(70, y + 120), (1010, y + 120)], fill=LIGHT, width=3)
    for j, (c0, c1, c2) in enumerate(cells):
        v1, a, b = ROWS[j]; yy = y + 190 + j * 100
        if j == hl: d.rounded_rectangle([60, yy - 46, 1020, yy + 46], radius=20, fill=(255, 247, 237))
        if c0 or j == hl: text(d, (XS[0], yy), str(j + 1), 60, INK)
        if c0: text(d, (XS[1], yy), vn(v1), 60, C1D)
        if c1: text(d, (XS[2], yy), "0", 60, C1D)
        if c2: text(d, (XS[3], yy), vn(b), 60, C2D)
    text(d, (W / 2, y + 500), "đơn vị m/s · số liệu mô hình", 56, NOTE)

def cells_at(t):
    i, u, k = do_state(t); out = []
    for j in range(3):
        if t < R0 or j > i: out.append((False, False, False)); continue
        if j < i: out.append((True, True, True)); continue
        v1 = ROWS[j][0]; x1, x2, _ = kin(v1, -1 if u is None else u)
        out.append((u is not None and x1 >= G1 + 0.01, stopped(v1, u), u is not None and x2 >= G2 + 0.01))
    return out

def s_do(img, d, t, sc):
    i, u, k = do_state(t); v1 = ROWS[i][0]
    x1, x2, d1, d2 = rig(d, v1, -1 if u is None else u, k=k)
    if stopped(v1, u):
        ks = appear(u, (XC1 - X1S) / v1 + TC, 0.3) * k
        text(d, (sx(x1), YB + 70), "v₁′ = 0", 56, C1D, alpha=ks)
    table(d, cells_at(t), hl=i if t >= R0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: o bang = cong quang / xe 1 da dung ; xe 2 khong qua chan cuoi ; vong lo xo khong am ; mep phai."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, u, k = do_state(t); v1 = ROWS[i][0]
        if t >= R0:
            x1, x2, rg = kin(v1, -1 if u is None else u)
            c = cells_at(t)[i]
            if c != (u is not None and x1 >= G1 + 0.01, stopped(v1, u), u is not None and x2 >= G2 + 0.01): bad.append(("bang", round(t, 2)))
            if rg < 0.004: bad.append(("lo xo", round(t, 2)))
            if x2 - x1 < CL + rg - 1e-6: bad.append(("xe chong", round(t, 2)))
            if 65 + 0.88 * (sx(x2) + CL * PXM / 2) > 1040: bad.append(("mep phai", round(t, 2)))
        t += 0.05
    if DO_END > sc["T"] - 0.2: bad.append(("lan 3 sat cuoi canh", round(DO_END, 2), round(sc["T"], 2)))
    for v1, a, b in ROWS:
        x1, x2, _ = kin(v1, run_len(v1) - 0.15 - 0.6 + 0.01)
        if x2 < G2 + 0.01: bad.append(("cong 2 chua doc", v1))
    return bad

# ---------------- canh 3: Ket qua (lan 3): dong luong + dong nang chuyen sang xe 2 ----------------
def s_kq(img, d, t, sc):
    M = sc["M"]; L = 0.80 * 330                                 # mui ten dong luong dai theo m.v
    card(d, (40, 265, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 330), "Lần 3", 56, INK, anchor="lm")
    for j, at in enumerate((-1.0, 2.8)):
        yb = 520 + j * 290; kk = appear(t, at, 0.45)
        if kk <= 0: continue
        text(d, (1000, yb - 150), "trước" if j == 0 else "sau", 56, NOTE, anchor="rm", alpha=kk)
        track(d, yb, kk, stop=False)
        g = ease((t - at - 0.3) / 0.4)
        if j == 0:
            cart(d, yb, 0.30, C1, C1D, "1", kk, ring=RING); cart(d, yb, X2S, C2, C2D, "2", kk)
            X = sx(0.30)
            if g > 0: arrow(d, (X - 70, yb + 75), (X - 70 + L * g, yb + 75), C1, w=9, head=24)
            text(d, (X - 70 + L + 30, yb + 75), "p xe 1", 56, C1D, anchor="lm", alpha=kk)
        else:
            x1 = XC1 + 0.8 * TC / 2
            cart(d, yb, x1, C1, C1D, "1", kk, ring=RING); cart(d, yb, 0.92, C2, C2D, "2", kk)
            text(d, (sx(x1) - 40, yb + 75), "dừng", 56, C1D, alpha=kk)
            X = sx(0.92) - L + 40
            if g > 0: arrow(d, (X, yb + 75), (X + L * g, yb + 75), C2, w=9, head=24)
            text(d, (X - 30, yb + 140), "p xe 2", 56, C2D, anchor="lm", alpha=g)
    k2 = appear(t, M[1] + 1.0, 0.45)
    if k2 <= 0: return
    card(d, (40, 1000, 1040, 1570), fill=A(WHITE, k2), outline=A(LIGHT, k2), w=3)
    text(d, (W / 2, 1070), "Động năng", 60, INK, alpha=k2)
    by, H0 = 1420, 230
    for j, (lab, col, cd, at) in enumerate((("xe 1 trước", C1, C1D, M[1] + 1.3), ("xe 2 sau", C2, C2D, M[1] + 2.1))):
        cx = 300 + j * 480; g = ease((t - at) / 0.5); h = H0 * g
        if h > 2: d.rectangle([cx - 90, by - h, cx + 90, by], fill=col)
        text(d, (cx, by + 55), lab, 56, cd, alpha=k2)
    d.line([(150, by), (930, by)], fill=A(INK, k2), width=4)
    d.line([(390, by - H0), (690, by - H0)], fill=A(NAVY, ease((t - M[1] - 2.6) / 0.4)), width=5)

# ---------------- canh 4: Bay (lan 2, cap so khac Du doan) + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.3, 0.45)
    card(d, (40, 265, 1040, 560), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 335, "BẪY", RED, a1)
    q = "“Va chạm nào cũng đi chung”"
    ks = clamp((t - M[1]) / 0.4); f = F(62); lw = tw(d, q, f); yy = 465
    text(d, (W / 2, yy), q, 62, mix(INK, DRED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
    kk = appear(t, M[1] + 0.1, 0.45)
    if kk > 0: card(d, (40, 600, 1040, 1275), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
    for j, (lab, at) in enumerate((("Sáp, dính nhau", M[1] + 0.1), ("Lò xo lá", M[1] + 2.7))):
        yb = 830 + j * 320; g = appear(t, at, 0.4)
        if g <= 0: continue
        text(d, (80, yb - 170), lab, 56, PURPLE if j == 0 else DGREEN, anchor="lm", alpha=g)
        text(d, (1000, yb - 170), "tới 0,50 m/s", 56, NOTE, anchor="rm", alpha=g)
        track(d, yb, g, stop=False)
        if j == 0:
            cart(d, yb, 0.48, C1, C1D, "1", g); cart(d, yb, 0.62, C2, C2D, "2", g)
            X = sx(0.55); arrow(d, (X - 60, yb + 75), (X + 60, yb + 75), A(PURPLE, g), w=8, head=22)
            text(d, (X + 90, yb + 75), "0,25 m/s", 56, PURPLE, anchor="lm", alpha=g)
        else:
            x1 = XC1 + 0.5 * TC / 2
            cart(d, yb, x1, C1, C1D, "1", g, ring=RING); cart(d, yb, 0.92, C2, C2D, "2", g)
            text(d, (sx(x1), yb - 170), "dừng", 56, C1D, alpha=g)
            X = sx(0.92); arrow(d, (X - 120, yb + 75), (X + 40, yb + 75), A(C2, g), w=8, head=22)
            text(d, (X - 150, yb + 75), "0,50 m/s", 56, C2D, anchor="rm", alpha=g)
    k5 = appear(t, M[2] + 0.1, 0.45)
    if k5 > 0:
        y0 = 1300 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 270), fill=A(WHITE, k5), outline=A(NAVY, k5), w=6)
        pill(d, W / 2, y0 + 70, "CHƯA NÓI ĐƯỢC", NAVY, k5)
        text(d, (W / 2, y0 + 190), "hai xe khác khối lượng", 60, INK, alpha=k5)

# ---------------- canh 5: THU NGHI (cau chot o khung web: v1' = 0,20 ; v2' = 0,60 m/s) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.2, 0.4)
    card(d, (40, 265, 1040, 1570), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 335, "THỬ NGHĨ", ORANGE, k)
    yb = 600
    track(d, yb, k, stop=False)
    cart(d, yb, 0.25, C1, C1D, "1", k, ring=RING); cart(d, yb, 0.75, C2, C2D, "2", k)
    X1, X2 = sx(0.25), sx(0.75)
    arrow(d, (X1 - 80, yb + 75), (X1 + 100, yb + 75), A(C1, k), w=8, head=22)          # 0,60 m/s ~ 180 px
    text(d, (X1 + 10, yb + 140), "0,60 m/s", 56, C1D, alpha=k)
    arrow(d, (X2 - 30, yb + 75), (X2 + 30, yb + 75), A(C2, k), w=8, head=22)           # 0,20 m/s ~ 60 px
    text(d, (X2, yb + 140), "0,20 m/s", 56, C2D, alpha=k)
    k1 = appear(t, 2.6, 0.45)
    text(d, (W / 2, 920), "Hai xe cùng 0,20 kg.", 62, INK, alpha=k1)
    k2 = appear(t, 5.0, 0.45)
    text(d, (W / 2, 1075), "Ngay sau, mỗi xe đi bao nhanh?", 60, ORANGE, alpha=k2)
    seg_bar(d, 1160, t, 5.2, sc["T"] - 0.2, ORANGE, k2)
    kh = appear(t, 7.5, 0.45)
    if kh > 0:
        card(d, (90, 1290, 990, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1350), "Gợi ý", 56, INK, alpha=kh)
        text(d, (W / 2, 1445), "kiểm cả động lượng, động năng", 56, DORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, b, e = sc["hook"], sc["do"], sc["kq"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for j, (v1, a, bb) in enumerate(ROWS):                   # va cham
        out.append((do["t0"] + STARTS[j] + 0.15 + (XC1 - X1S) / v1, "tap"))
    out += [(kq["t0"] + 3.1, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 5.0, "open")]
    return out

CLIP = dict(id="tn-l10-baotoandl-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Bảo toàn động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai xe có đệm lò xo", draw=s_hook, tail=0.3, caps=[
   ("Xe 2 đứng yên giữa ray.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Ba lần, đổi tốc độ xe 1.", 3.6),
   ("Nhìn xe 1 sau va chạm.", 3.4)]),
 dict(key="kq", title="Kết quả", draw=s_kq, tail=0.6, caps=[
   ("Xe 1 dừng, xe 2 đi 0,80 m/s.", 3.8),
   ("Động lượng chuyển hết sang xe 2.", 4.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 2.5),
   ("Sai: chỉ dính nhau mới đi chung.", 5.6),
   ("Thí nghiệm này còn thiếu gì?", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Xe 2 cũng đang chạy.", 2.8),
   ("Dừng lại, tự tính.", 6.6)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("đồng bộ:", _kiem_dong_bo() or "không lệch")
