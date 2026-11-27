# Clip: tn-l10-thuchanhdl-01 - Va cham mem tren bang dem khi: do t qua cong quang, so p' voi p (lo 9, 18/11/2026;
# dung lai 27/11/2026 theo cong moi L10b: chu >= 55 px khi ve, nhip >= 2,5 s, K10 khong nut A-D, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-thuchanhdl-01.json (_kiem_so() doi chieu):
#   tham_so: s = 0,0500 m (tam can quang 5,00 cm) ; dong ho 0,001 s ; can 0,001 kg
#   so_lieu_mau (lan, m1, m2, t1, t1', v1, p, v', p', delta %, eps %):
#     1 0,205 0,198 0,099 0,199 ... ; 2 0,405 0,198 0,101 0,153 0,495 0,2005 0,327 0,1972 1,6 2,2 ; 3 0,405 0,398 0,105 0,214
# Du doan (DOI CA 27/11): lan 1 (t1' ~ 2 t1) trung vi du giai ngay sau hop -> LAN 2: xe 1 0,405 kg (gap doi xe 2),
#   cong 1 chi 0,101 s ; dinh nhau qua cong 2 -> dong ho chi khoang? Dap an 0,153 s (khoi luong x1,5 -> thoi gian x1,5).
#   Khung web: A. 0,101 s ; B. Khoang 0,15 s (DUNG) ; C. Khoang 0,20 s ; D. Khoang 0,30 s.
# Ket qua lan 2: thanh p, p' gan bang (khong ghi so p, p': de HS tu tinh theo hop) ; delta 1,6 % < eps 2,2 %.
#   Khong tinh lan 3 (Tu kiem tra Cau 1 hoi p lan 3 = 0,193).
# Bay = hien_tuong_hay_sai (quen m2) o LAN 1 (cap so khac Du doan): 0,205 . 0,251 ~ 0,0515 (ghi_chu kho) -> dung 0,403 . 0,251.
#   Chua noi duoc: hai xe nay ra (khong_chung_minh[1]).
# Cau chot (ca tu suy, ghi trong ghi_chu kho): m1 = 0,305 kg, m2 = 0,198 kg, t1 = 0,100 s, t1' = 0,169 s
#   -> v' = 0,0500/0,169 = 0,296 m/s ; p' = 0,503 . 0,296 = 0,1489 ~ 0,149 kg.m/s (khong hien tren man).
from engine import *

ROWS = [(1, 0.205, 0.198, 0.099, 0.199), (2, 0.405, 0.198, 0.101, 0.153), (3, 0.405, 0.398, 0.105, 0.214)]
SW = 0.0500                                     # be rong tam can quang (m)
CHOT = (0, 0.305, 0.198, 0.100, 0.169)          # lan moi o canh chot ; dap so p' = 0,149
DELTA, EPS = 1.6, 2.2                           # lan 2

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-thuchanhdl-01.json")))
    hang = k["so_lieu_mau"]["hang"]
    for r, h in zip(ROWS, hang): assert all(abs(a - b) < 1e-9 for a, b in zip(r, h[:5])), ("lech kho", r)
    assert abs(SW - [p for p in k["tham_so"] if p["ky_hieu"] == "s"][0]["gia_tri"]) < 1e-9
    h2 = hang[1]; assert (h2[9], h2[10]) == (DELTA, EPS)
    assert round(abs(h2[8] - h2[6]) / h2[6] * 100, 1) == DELTA
    g = k["so_lieu_mau"]["ghi_chu"]
    for s in ("0,205·0,251 ≈ 0,0515", "m1 = 0,305 kg", "m2 = 0,198 kg", "t1 = 0,100 s", "t1' = 0,169 s", "0,149"):
        assert s in g, ("ghi_chu thieu", s)
    assert round(SW / CHOT[3], 3) == 0.500 and round((CHOT[1] + CHOT[2]) * round(SW / CHOT[4], 3), 3) == 0.149
_kiem_so()

C1, C1D = ORANGE, (154, 52, 18)                 # xe 1
C2, C2D = BLUE, (30, 64, 175)                   # xe 2
RAIL = (148, 163, 184); RAIL_D = (100, 116, 139); LCD = (134, 239, 172)
NOTE = (60, 64, 84); DGREEN = (21, 110, 55); SAP = (161, 98, 7); DRED = (185, 28, 28)
EMPTY = (148, 140, 128)
def vn(x, n=3): return f"{x:.{n}f}".replace(".", ",")

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

# ---------------- bang dem khi, hai cong quang, hai xe ----------------
X0, PXM = 60, 800                     # mp4 x = 65 + 0,88 x
G1, G2 = 0.40, 0.86
CL = 0.14
X1S, X2S = 0.30, 0.66
XC1 = X2S - CL
YB = 790
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
    """x = tam xe (m). Tam can quang rong SW ve dung ti le. Xe cao 74 px, nhan 56 px."""
    c = lambda cc: A(cc, k); w = CL * PXM / 2; X = sx(x); hw = SW * PXM / 2
    d.rectangle([X - hw, yb - 132, X + hw, yb - 76], fill=c(NAVY))
    slots = [(-44, 0), (44, 0), (-44, 1), (44, 1)]
    for j in range(n_gt):
        dx, lv = slots[j]
        d.rectangle([X + dx - 14, yb - 104 - 28 * lv, X + dx + 14, yb - 78 - 28 * lv], fill=c(GRAY), outline=c(NAVY), width=2)
    d.rounded_rectangle([X - w, yb - 76, X + w, yb - 2], radius=12, fill=c(col), outline=c(cold), width=3)
    text(d, (X, yb - 39), label, 56, WHITE, alpha=k)
    if front == "kim": d.polygon([(X + w, yb - 46), (X + w + 18, yb - 39), (X + w, yb - 32)], fill=c(NAVY))
    if rear == "sap": d.ellipse([X - w - 14, yb - 52, X - w + 6, yb - 26], fill=c(SAP))

def lcd(d, x, y, lab, val, col, hi=False):
    text(d, (x, y - 80), lab, 56, col)
    card(d, (x - 150, y - 44, x + 150, y + 44), fill=NAVY, r=14)
    text(d, (x, y), val, 56, YELLOW if hi else LCD)

def kin(row, u):
    """u: giay tu luc xe 1 chay. v1 = s/t1, v' = s/t1'. -> (x1, x2)."""
    n, m1, m2, t1, t1p = row; v1, vp = SW / t1, SW / t1p
    uc = (XC1 - X1S) / v1
    if u < uc: return X1S + v1 * max(0.0, u), X2S
    x2 = X2S + vp * (u - uc); return x2 - CL, x2

def gate_done(x, g, v, tp):
    """Dong ho dung (hien t) khi tam can quang (tam x, rong SW) da ra khoi tia o g."""
    return x + SW / 2 >= g and (x + SW / 2 - g) / v >= tp - 1e-9

def run_len(row):
    n, m1, m2, t1, t1p = row
    return 0.15 + (XC1 - X1S) / (SW / t1) + (G2 + SW / 2 - X2S) / (SW / t1p) + 0.6

def ngt(m, base): return int(round((m - base) / 0.1))

def rig(d, row, u, k=1.0, yc=880, freeze=None, show_m=True, q2=False):
    """freeze = (x1, x2): dat xe co dinh. q2: cong 2 hien '?'."""
    n, m1, m2, t1, t1p = row
    card(d, (40, 265, 1040, yc), fill=WHITE, outline=LIGHT, w=3)
    text(d, (70, 320), f"xe 1: {vn(m1)} kg" if show_m else "xe 1", 56, C1D, anchor="lm")
    text(d, (1010, 320), f"xe 2: {vn(m2)} kg" if show_m else "xe 2", 56, C2D, anchor="rm")
    x1, x2 = freeze if freeze else kin(row, u)
    d1 = gate_done(x1, G1, SW / t1, t1); d2 = (not q2) and gate_done(x2, G2, SW / t1p, t1p)
    lcd(d, sx(G1) - 20, 495, "cổng 1", f"{vn(t1)} s" if d1 else "– – –", C1D)
    lcd(d, sx(G2) + 20, 495, "cổng 2", "?" if q2 else (f"{vn(t1p)} s" if d2 else "– – –"), C2D, hi=d2)
    track(d, YB); gate_back(d, YB, G1); gate_back(d, YB, G2)
    cart(d, YB, x2, C2, C2D, "2", ngt(m2, 0.198), k, rear="sap")
    cart(d, YB, x1, C1, C1D, "1", ngt(m1, 0.205), k, front="kim")
    gate_front(d, YB, G1); gate_front(d, YB, G2)
    return d1, d2

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; row = ROWS[1]
    x1 = lerp(0.16, 0.47, ease((t - 0.6) / 1.6))
    rig(d, row, None, yc=930, freeze=(x1, X2S), q2=True)
    text(d, (sx(X2S), YB + 80), "đứng yên", 56, C2D)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 965 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Dính nhau qua cổng 2,", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "đồng hồ chỉ khoảng?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 410, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

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
    u = min(w, run_len(ROWS[i])) - 0.15
    return i, (u if u >= 0 else None), k

XS = (110, 300, 500, 705, 910)
def table(d, cells, hl=None, y=920):
    card(d, (40, y, 1040, y + 660), fill=WHITE, outline=LIGHT, w=3)
    for x, lab, unit, col in ((XS[0], "Lần", "", INK), (XS[1], "m₁", "kg", C1D), (XS[2], "m₂", "kg", C2D),
                              (XS[3], "t₁", "s", C1D), (XS[4], "t₁′", "s", C2D)):
        text(d, (x, y + 60), lab, 60, col)
        if unit: text(d, (x, y + 125), unit, 56, col, bold=False)
    d.line([(70, y + 170), (1010, y + 170)], fill=LIGHT, width=3)
    for j, (cm, c1, c2) in enumerate(cells):
        n, m1, m2, t1, t1p = ROWS[j]; yy = y + 235 + j * 95
        if j == hl: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=20, fill=(255, 247, 237))
        if cm:
            text(d, (XS[0], yy), str(n), 60, INK)
            text(d, (XS[1], yy), vn(m1), 60, C1D); text(d, (XS[2], yy), vn(m2), 60, C2D)
        if c1: text(d, (XS[3], yy), vn(t1), 60, C1D)
        if c2: text(d, (XS[4], yy), vn(t1p), 60, C2D)
    text(d, (W / 2, y + 590), "tấm cản quang rộng 5,00 cm", 56, NOTE)

def cells_at(t):
    i, u, k = do_state(t); out = []
    for j in range(3):
        if t < R0 or j > i: out.append((False, False, False)); continue
        if j < i: out.append((True, True, True)); continue
        n, m1, m2, t1, t1p = ROWS[j]; x1, x2 = kin(ROWS[j], -1 if u is None else u)
        out.append((True, gate_done(x1, G1, SW / t1, t1), gate_done(x2, G2, SW / t1p, t1p)))
    return out

def s_do(img, d, t, sc):
    i, u, k = do_state(t)
    rig(d, ROWS[i], -1 if u is None else u, k=k, show_m=False)
    table(d, cells_at(t), hl=i if t >= R0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: o bang = dong ho da dung ; hai dong ho dung truoc het luot ; xe khong ra khoi bang."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, u, k = do_state(t)
        if t >= R0:
            n, m1, m2, t1, t1p = ROWS[i]; x1, x2 = kin(ROWS[i], -1 if u is None else u)
            c = cells_at(t)[i]
            if (c[1], c[2]) != (gate_done(x1, G1, SW / t1, t1), gate_done(x2, G2, SW / t1p, t1p)): bad.append(("bang", round(t, 2)))
            if 65 + 0.88 * sx(x2 + CL / 2) > 1040: bad.append(("ra khoi bang", round(t, 2)))
        t += 0.05
    for row in ROWS:
        x1, x2 = kin(row, run_len(row) - 0.15 - 0.6 + 0.01)
        if not gate_done(x2, G2, SW / row[4], row[4]): bad.append(("cong 2 chua dung", row[0]))
    if DO_END > sc["T"] - 0.2: bad.append(("lan 3 sat cuoi canh", round(DO_END, 2), round(sc["T"], 2)))
    return bad

# ---------------- canh 3: Ket qua lan 2 ----------------
def s_kq(img, d, t, sc):
    M = sc["M"]; n, m1, m2, t1, t1p = ROWS[1]
    card(d, (40, 265, 1040, 700), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 330), "Lần 2", 56, INK, anchor="lm")
    lcd(d, 290, 530, "cổng 1", f"{vn(t1)} s", C1D)
    lcd(d, 790, 530, "cổng 2", f"{vn(t1p)} s", C2D, hi=True)
    ka = appear(t, M[1] - 0.1, 0.45)
    if ka > 0:
        card(d, (40, 740, 1040, 1150), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
        text(d, (W / 2, 805), "động lượng lần 2 (kg·m/s)", 56, INK, alpha=ka)
        L = 3400                                              # px / (kg.m/s)
        for j, (lab, val, col) in enumerate((("p", 0.2005, C1), ("p′", 0.1972, PURPLE))):
            y = 925 + j * 125; g = ease((t - M[1] - 0.3 - 0.5 * j) / 0.6)
            text(d, (150, y), lab, 64, col)
            if g > 0: d.rounded_rectangle([220, y - 38, 220 + L * val * g, y + 38], radius=12, fill=col)
    kb = appear(t, M[2] - 0.1, 0.45)
    if kb > 0:
        card(d, (40, 1190, 1040, 1560), fill=A((236, 253, 243), kb), outline=A(GREEN, kb), w=5)
        text(d, (W / 2, 1290), f"lệch δ = {vn(DELTA, 1)} %", 62, ORANGE, alpha=kb)
        text(d, (W / 2, 1390), f"sai số ε = {vn(EPS, 1)} %", 62, NOTE, alpha=kb)
        text(d, (W / 2, 1490), "bảo toàn trong sai số", 60, DGREEN, alpha=kb)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.3, 0.45)
    card(d, (40, 265, 1040, 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 335, "BẪY", RED, a1)
    q, q0 = "p′ = 0,205 · 0,251", "Lần 1:  "
    ks = clamp((t - M[1]) / 0.4); lw = tw(d, q, F(62)); l0 = tw(d, q0, F(62)); yy = 470
    xl = W / 2 - (lw + l0) / 2
    text(d, (xl, yy), q0, 62, INK, anchor="lm", alpha=a1)
    text(d, (xl + l0, yy), q, 62, mix(INK, DRED, ks), anchor="lm", alpha=a1)
    if ks > 0: d.line([(xl + l0 - 6, yy + 2), (xl + l0 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
    kk = appear(t, M[1] + 0.1, 0.45)
    if kk > 0:
        card(d, (40, 640, 1040, 1230), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
        yb = 900
        track(d, yb, kk)
        cart(d, yb, 0.64, C2, C2D, "2", 0, kk, rear="sap")
        cart(d, yb, 0.50, C1, C1D, "1", 0, kk, front="kim")
        X1, X2 = sx(0.50), sx(0.64); w = CL * PXM / 2
        text(d, (260, yb - 170), "0,205 kg", 56, C1D, alpha=kk)
        text(d, (800, yb - 170), "0,198 kg", 56, C2D, alpha=kk)
        y = yb + 70
        d.line([(X1 - w, y), (X2 + w, y)], fill=A(DGREEN, kk), width=5)
        for xx in (X1 - w, X2 + w): d.line([(xx, y - 18), (xx, y)], fill=A(DGREEN, kk), width=5)
        text(d, (W / 2, y + 60), "cả hai xe cùng chạy", 56, DGREEN, alpha=kk)
        text(d, (W / 2, 1150), "p′ = 0,403 · 0,251 ✓", 62, DGREEN, alpha=kk)
    k5 = appear(t, M[2] + 0.1, 0.45)
    if k5 > 0:
        y0 = 1270 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 290), fill=A(WHITE, k5), outline=A(NAVY, k5), w=6)
        pill(d, W / 2, y0 + 70, "CHƯA NÓI ĐƯỢC", NAVY, k5)
        text(d, (W / 2, y0 + 200), "hai xe nảy ra, không dính", 60, INK, alpha=k5)

# ---------------- canh 5: THU NGHI (cau chot o khung web: p' = 0,149) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; n, m1, m2, t1, t1p = CHOT; k = 1.0
    rig(d, CHOT, None, yc=930, freeze=(0.94, 1.08))
    y0 = 965
    card(d, (40, y0, 1040, 1665), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, y0 + 70, "THỬ NGHĨ", ORANGE, k)
    k1 = appear(t, 2.6, 0.45)
    text(d, (W / 2, y0 + 195), "Lần mới, hai xe dính nhau.", 60, INK, alpha=k1)
    k2 = appear(t, 5.0, 0.45)
    text(d, (W / 2, y0 + 300), "Động lượng p′ bằng bao nhiêu?", 62, ORANGE, alpha=k2)
    seg_bar(d, y0 + 370, t, 5.2, sc["T"] - 0.2, ORANGE, k2)
    kh = appear(t, 7.5, 0.45)
    if kh > 0:
        card(d, (90, y0 + 475, 990, y0 + 680), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, y0 + 530), "Gợi ý", 56, INK, alpha=kh)
        text(d, (W / 2, y0 + 620), "đổi 5,00 cm ra mét trước", 58, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, b, e = sc["hook"], sc["do"], sc["kq"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for j, row in enumerate(ROWS):                            # dong ho cong 2 dung
        n, m1, m2, t1, t1p = row
        out.append((do["t0"] + STARTS[j] + 0.15 + (XC1 - X1S) / (SW / t1) + (G2 + SW / 2 - X2S) / (SW / t1p), "tap"))
    out += [(kq["t0"] + 0.4, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 5.0, "open")]
    return out

CLIP = dict(id="tn-l10-thuchanhdl-01", header="VẬT LÍ 10 · THỰC HÀNH", footer="Thực hành động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo thời gian chắn cổng quang", draw=s_hook, tail=0.3, caps=[
   ("Xe 1 chắn tia hết 0,101 s.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đọc số đầu tiên mỗi cổng.", 3.4),
   ("Thêm gia trọng, đo ba lần.", 3.4)]),
 dict(key="kq", title="Kết quả", draw=s_kq, tail=0.3, caps=[
   ("Đáp án: cổng 2 chỉ 0,153 s.", 3.2),
   ("Tính p, p′: gần bằng nhau.", 3.4),
   ("Độ lệch nhỏ hơn sai số đo.", 3.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.0),
   ("Sai: hai xe dính, cùng chạy.", 4.0),
   ("Thí nghiệm này còn thiếu gì?", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Thêm một lần đo.", 2.8),
   ("Dừng lại, tự tính.", 6.6)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("đồng bộ:", _kiem_dong_bo() or "không lệch")
