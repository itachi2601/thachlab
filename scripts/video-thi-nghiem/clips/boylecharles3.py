# Clip: tn-l12-boylecharles-03 - Ong chu J mot dau kin, rot them chat long.
# So lieu lay tu content/thi-nghiem/tn-l12-boylecharles-03.json (_kiem_so() doi chieu):
#   h = 0 (p0 = 760 mmHg, L = 21,8 cm: cac_buoc.lam + mo_hinh), so_lieu_mau: h 55/85/110/165 mmHg,
#   p 815/845/870/925 mmHg, L 20,3/19,6/19,0/17,9 cm, p.L 1,65/1,66/1,65/1,66 (10^4 mmHg.cm); h = 0 -> 1,66 (mo_hinh).
# Ban 1 (14/11/2026). Ban 2 (26/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32): cong --do-chu (chu ve >= 58 px,
#   <= 180 tu/phut moi canh, nhip >= 2,5 s), <= 50 s, K10 (khong nut A-D, khong "chon dap an"), bay TRUOC rut ra.
# Du doan (khung web, KHONG ve A-D trong mp4): chenh 110 mmHg, khi quyen 760 mmHg -> p khi nhot? A 650 (tru h,
#   hien_tuong_hay_sai[0]) / B 760 / C 870 (dap an, p = p0 + h) / D 110.
# Thu tu: Du doan -> Tien hanh (rot 4 lan, bang h/L/p, dap an 870) -> Do thi p-L (nhanh hypebol)
#   -> Bay "rot them thi p.V tang" (hien_tuong_hay_sai[1]: hai ong truoc/sau, cung so phan tu, p.L ~ 1,66)
#   -> Rut ra (cot chat long: pittong + ap ke) -> Chot + THU NGHI.
# THU NGHI (= cau_chot khung, CA TU SUY ghi trong kho ghi_chu): chenh 150 mmHg -> p = 910 mmHg,
#   L = 760 x 21,8 / 910 ~ 18,2 cm. Dap so khong hien tren man.
from engine import *
import random

HS = [0, 55, 85, 110, 165]
PS = [760, 815, 845, 870, 925]
LS = [21.8, 20.3, 19.6, 19.0, 17.9]
PL = [1.66, 1.65, 1.66, 1.65, 1.66]
P0 = 760

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-boylecharles-03.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    for i in range(1, 5): assert (HS[i], PS[i], LS[i], PL[i]) in hang, i
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["p0"]["gia_tri"] == P0 and "21,8" in k["cac_buoc"]["lam"][0]
    assert abs(P0 * 21.8 / (P0 + 150) - 18.2) < 0.05 and "18,2" in k["so_lieu_mau"]["ghi_chu"]
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
FS = 58
def fmt(v, n=1): return f"{v:.{n}f}".replace(".", ",")

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

def dashed(d, p1, p2, color, w=3, dash=14, gap=10):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

R = random.Random(33)
MOL = [(R.random(), R.random(), R.choice((-1, 1)) * R.uniform(0.25, 0.45), R.choice((-1, 1)) * R.uniform(0.25, 0.45)) for _ in range(12)]
HG = (246, 205, 205); GLASS = (250, 252, 255); GAS = (214, 232, 255)   # thuy ngan do trong (KE-HOACH-MAU-CHAT-LONG)

# ---------------- ong chu J ----------------
XC, YCT, SC = 330, 430, 1.0          # nhanh kin (tam x), dinh nhanh kin (y), ti le
def geo(xc=XC, yct=YCT, s=SC):
    S = 24 * s; w = 20 * s; xo = xc + 200 * s; yb = yct + 600 * s; ytop = yct - 80 * s
    return S, w, xo, yb, ytop

def jtube(d, t, L, h, xc=XC, yct=YCT, s=SC, mol=True, pour=0.0, nmol=12):
    S, w, xo, yb, ytop = geo(xc, yct, s)
    yc = yct + L * S; yo = yc - h / 10 * S
    cx, Rm = (xc + xo) / 2, (xo - xc) / 2
    o = 6 * s
    d.rectangle([xc - w - o, yct - o, xc + w + o, yb], fill=NAVY)
    d.rectangle([xo - w - o, ytop, xo + w + o, yb], fill=NAVY)
    d.arc([cx - Rm - w - o, yb - Rm - w - o, cx + Rm + w + o, yb + Rm + w + o], 0, 180, fill=NAVY, width=int(2 * (w + o)))
    d.rectangle([xc - w, yct, xc + w, yb], fill=GLASS)
    d.rectangle([xo - w, ytop - 10, xo + w, yb], fill=GLASS)
    d.arc([cx - Rm - w, yb - Rm - w, cx + Rm + w, yb + Rm + w], 0, 180, fill=HG, width=int(2 * w))
    d.rectangle([xc - w, yct, xc + w, yc], fill=GAS)
    d.rectangle([xc - w, yc, xc + w, yb + 1], fill=HG)
    d.rectangle([xo - w, yo, xo + w, yb + 1], fill=HG)
    for x, y in ((xc, yc), (xo, yo)): d.line([(x - w, y), (x + w, y)], fill=(200, 60, 60), width=max(3, int(5 * s)))
    if mol:
        for (ux, uy, vx, vy) in MOL[:nmol]:
            mx = xc - w + 6 * s + refl(ux + vx * t, 0, 1) * (2 * w - 12 * s)
            my = yct + 8 * s + refl(uy + vy * t, 0, 1) * (yc - yct - 16 * s)
            dot(d, mx, my, max(8, 8 * s), ORANGE)
    if pour > 0:                                         # ong nho giot tren mieng nhanh ho
        d.rounded_rectangle([xo - 14, ytop - 110, xo + 14, ytop - 30], radius=10, fill=WHITE, outline=NAVY, width=4)
        d.ellipse([xo - 30, ytop - 150, xo + 30, ytop - 100], fill=(70, 78, 100))
        ph = (t * 2.2) % 1
        dot(d, xo, lerp(ytop - 30, yo - 10, ph), 9, HG)
    return yc, yo, xo

def figure(d, t, L, h, show_L=True, pour=0.0, h_lbl=None, p0=True):
    yc, yo, xo = jtube(d, t, L, h, pour=pour)
    S, w, _, yb, ytop = geo()
    for c in range(0, 23):                              # thuoc do cot khi, 0 o dinh nhanh kin
        y = YCT + c * S; Lm = 26 if c % 5 == 0 else 12
        d.line([(XC + w + 10, y), (XC + w + 10 + Lm, y)], fill=NAVY, width=3)
        if c % 5 == 0: text(d, (XC + w + 48, y), str(c), FS, INK, anchor="lm")
    text(d, (XC + w + 48, YCT - 56), "cm", FS, INK, anchor="lm")
    if show_L:
        my = (YCT + yc) / 2
        text(d, (XC - w - 30, my - 40), "L", 66, BLUE, anchor="rm")
        text(d, (XC - w - 30, my + 36), f"{fmt(L)} cm", FS, BLUE, anchor="rm")
    if pour <= 0: arrow(d, (xo, ytop - 100), (xo, ytop - 12), GRAY, w=7, head=22)
    if p0: text(d, (xo + 60, ytop - 60), "p0 = 760 mmHg", FS, INK, anchor="lm")
    if h > 0.5:
        bx = xo + w + 50
        dashed(d, (XC + w, yc), (bx + 20, yc), NAVY, w=4); d.line([(xo + w, yo), (bx + 20, yo)], fill=NAVY, width=4)
        if yc - yo > 50:
            arrow(d, (bx, (yo + yc) / 2), (bx, yo + 3), RED, w=6, head=18); arrow(d, (bx, (yo + yc) / 2), (bx, yc - 3), RED, w=6, head=18)
        lbl = h_lbl if h_lbl is not None else f"h = {h:.0f} mmHg"
        text(d, (bx + 30, (yo + yc) / 2), lbl, FS, RED, anchor="lm")

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    figure(d, t, LS[3], HS[3])
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1170 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 430), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 160), "Chênh 110 mmHg:", 64, INK, alpha=k)
    text(d, (W / 2, y0 + 245), "khí bị nhốt có áp suất?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 325, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: tien hanh ----------------
STEP = [0.8, 2.6, 4.4]            # moc bat dau rot lan i (h: 0 -> 55 -> 85 -> 110); hang 165 chi o do thi/bay
TR, SETTLE = 0.8, 0.4
def row_at(i): return 0.0 if i == 0 else STEP[i - 1] + TR + SETTLE
def do_state(t):
    """(L, h, pour, i_on_dinh|None) - so tren hinh = hang bang moi nhat khi on dinh."""
    i = sum(1 for s_ in STEP if t >= s_)
    if i == 0: return LS[0], HS[0], 0.0, 0
    k = ease((t - STEP[i - 1]) / TR)
    L = lerp(LS[i - 1], LS[i], k); h = lerp(HS[i - 1], HS[i], k)
    pour = 1.0 if t < STEP[i - 1] + TR else 0.0
    return L, h, pour, (i if t >= row_at(i) else None)

XS = [230, 520, 830]
def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    L, h, pour, ion = do_state(t)
    if ion is None:
        figure(d, t, L, h, show_L=False, pour=pour, h_lbl="h = …", p0=False)
        text(d, (XC - 50, 700), "đợi 1 phút", FS, DORANGE, anchor="rm")
    else:
        figure(d, t, LS[ion], HS[ion], pour=pour, p0=False)
    kp = appear(t, M[2], 0.4)
    card(d, (40, 1160, 1040, 1650), fill=WHITE, outline=NAVY, w=4)
    text(d, (XS[0], 1210), "h (mmHg)", FS, RED); text(d, (XS[1], 1210), "L (cm)", FS, BLUE)
    if kp < 1: text(d, (XS[2], 1210), "p (mmHg)", FS, INK, alpha=1 - kp)
    if kp > 0: text(d, (XS[2], 1210), "p = p0 + h", FS, DGREEN, alpha=kp)
    d.line([(70, 1252), (1010, 1252)], fill=LIGHT, width=4)
    for i in range(4):
        a = appear(t, row_at(i), 0.3); y = 1310 + i * 84
        if a <= 0: continue
        if i == 3 and kp > 0: d.rounded_rectangle([60, y - 34, 1020, y + 34], radius=16, fill=A((220, 252, 231), kp))
        text(d, (XS[0], y), str(HS[i]), 62, RED, alpha=a); text(d, (XS[1], y), fmt(LS[i]), 62, BLUE, alpha=a)
        kpi = appear(t, M[2] + 0.3 + i * 0.15, 0.3)
        if kpi > 0: text(d, (XS[2], y), str(PS[i]), 62, DGREEN if i == 3 else INK, alpha=kpi)

# ---------------- canh 3: do thi p-L ----------------
GX0, GX1, GYB, GYT = 210, 960, 1380, 420
LMIN, LMAX, PMIN, PMAX = 14, 23, 700, 1200
def GX(L): return GX0 + (L - LMIN) / (LMAX - LMIN) * (GX1 - GX0)
def GY(p): return GYB - (p - PMIN) / (PMAX - PMIN) * (GYB - GYT)
def s_graph(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 260, 1040, 1560), fill=WHITE, outline=LIGHT, w=4)
    for p_ in (800, 1000): d.line([(GX0, GY(p_)), (GX1, GY(p_))], fill=(236, 230, 220), width=3)
    d.line([(GX0, GYB), (GX1 + 30, GYB)], fill=NAVY, width=5); d.line([(GX0, GYB), (GX0, GYT - 40)], fill=NAVY, width=5)
    for dy in (0, 18):                                   # dau ngat truc (truc khong bat dau tu 0)
        d.line([(GX0 - 18, GYB - 44 - dy), (GX0 + 18, GYB - 30 - dy)], fill=NAVY, width=4)
        d.line([(GX0 + 34 + dy, GYB + 18), (GX0 + 48 + dy, GYB - 18)], fill=NAVY, width=4)
    text(d, (GX1 + 30, GYB - 60), "L (cm)", FS, BLUE, anchor="rm")
    text(d, (GX0 + 24, GYT - 50), "p (mmHg)", FS, RED, anchor="lm")
    for L_ in (16, 18, 20, 22):
        d.line([(GX(L_), GYB), (GX(L_), GYB + 14)], fill=NAVY, width=4); text(d, (GX(L_), GYB + 56), str(L_), FS, INK)
    for p_ in (800, 1000):
        d.line([(GX0 - 14, GY(p_)), (GX0, GY(p_))], fill=NAVY, width=4); text(d, (GX0 - 22, GY(p_)), str(p_), FS, INK, anchor="rm")
    k = ease((t - M[0] - 0.6) / 1.0)                    # p = 760 x 21,8 / L: lien trong khoang do, net dut ngoai
    if k > 0:
        cur = lambda L_: (GX(L_), GY(PS[0] * LS[0] / L_))
        Ls = [22.8 - (22.8 - 14.0) * j / 106 for j in range(107)]; nn = max(2, int(len(Ls) * k))
        for j in range(nn - 1):
            La, Lb = Ls[j], Ls[j + 1]
            if 17.9 <= Lb and La <= 21.8: d.line([cur(La), cur(Lb)], fill=A(BLUE, 0.9), width=6)
            elif j % 4 < 2: d.line([cur(La), cur(Lb)], fill=A(BLUE, 0.6), width=5)
        text(d, (GX(19.2), GY(1080)), "nhánh hypebol", FS, BLUE, alpha=appear(t, M[0] + 1.4))
    for i in range(5):
        a = appear(t, M[0] + i * 0.12, 0.3)
        if a > 0: dot(d, GX(LS[i]), GY(PS[i]), 18 * back(a), ORANGE, WHITE)

# ---------------- canh 4: bay "rot them thi p.V tang" ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    for j, (cx, lab, L_, h_) in enumerate(((270, "Trước", LS[0], HS[0]), (790, "Sau", LS[4], HS[4]))):
        card(d, (cx - 250, 270, cx + 250, 1420), fill=WHITE, outline=NAVY if j == 0 else ORANGE, w=5)
        text(d, (cx, 335), lab, 62, INK)
        xc = cx - 70
        jtube(d, t, L_, h_, xc=xc, yct=460, s=0.75, nmol=12, pour=0.0)
        S, w, xo, yb, ytop = geo(xc, 460, 0.75)
        if h_ > 0:
            yc = 460 + L_ * S; yo = yc - h_ / 10 * S
            d.line([(xo + w + 8, yo), (xo + w + 40, yo)], fill=RED, width=4); d.line([(xc + w, yc), (xo + w + 40, yc)], fill=RED, width=3)
            d.line([(xo + w + 30, yo), (xo + w + 30, yc)], fill=RED, width=5)
        text(d, (cx, 1100), f"{PS[0] if j == 0 else PS[4]} mmHg", FS, RED)
        text(d, (cx, 1185), f"{fmt(L_)} cm", FS, BLUE)
        ka = appear(t, M[1], 0.4)
        if ka > 0:
            d.rounded_rectangle([cx - 225, 1235, cx + 225, 1395], radius=22, fill=A((220, 252, 231), ka))
            text(d, (cx, 1280), "p·L ≈ 1,66·10⁴", 60, DGREEN, alpha=ka)
            text(d, (cx, 1350), "mmHg·cm", FS, DGREEN, alpha=ka)
    kc = appear(t, 1.8, 0.4)
    text(d, (W / 2, 1500), "12 hạt khí → vẫn 12 hạt", FS, DORANGE, alpha=kc)

# ---------------- canh 5: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    xc, yct, s = 300, 460, 1.0
    yc, yo, xo = jtube(d, t, LS[4], HS[4], xc=xc, yct=yct, s=s)
    S, w, _, yb, ytop = geo(xc, yct, s)
    k0 = appear(t, 0.3)
    ya = (yo + yb) / 2
    arrow(d, (xo, yo - 120), (xo, yo - 10), A(ORANGE, k0), w=9, head=26)
    text(d, (xo + 70, yo - 70), "như pittông", 62, DORANGE, anchor="lm", alpha=k0)
    text(d, (xo - 40, yo - 150), "p0", 62, INK, anchor="rm", alpha=k0)
    k1 = appear(t, M[1], 0.45); bx = xo + w + 40
    d.line([(xc + w, yc), (bx + 16, yc)], fill=A(RED, k1), width=4); d.line([(xo + w, yo), (bx + 16, yo)], fill=A(RED, k1), width=4)
    d.line([(bx, yo), (bx, yc)], fill=A(RED, k1), width=7)
    text(d, (bx + 30, (yo + yc) / 2 + 40), "như áp kế", 62, RED, anchor="lm", alpha=k1)
    if k1 > 0:
        card(d, (80, 1260, 1000, 1500), fill=A(WHITE, k1), outline=A(RED, k1), w=5)
        text(d, (W / 2, 1380), "p = p0 + h", 84, RED, alpha=k1)

# ---------------- canh 6: chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    if k1 > 0.5:
        xc, yct, s = 330, 420, 0.8
        L_ = PS[0] * LS[0] / (PS[0] + 150)
        yc, yo, xo = jtube(d, t, L_, 150, xc=xc, yct=yct, s=s, mol=False)
        S, w, _, yb, ytop = geo(xc, yct, s)
        text(d, (xc - w - 26, (yct + yc) / 2), "L = ?", 66, PURPLE, anchor="rm", alpha=k1)
        bx = xo + w + 36
        d.line([(xc + w, yc), (bx + 14, yc)], fill=RED, width=4); d.line([(xo + w, yo), (bx + 14, yo)], fill=RED, width=4)
        d.line([(bx, yo), (bx, yc)], fill=RED, width=6)
        text(d, (bx + 28, (yo + yc) / 2), "150 mmHg", 62, RED, anchor="lm", alpha=k1)
    text(d, (W / 2, 1150), "Lúc đầu 760 mmHg, 21,8 cm.", FS, INK, alpha=k1)
    text(d, (W / 2, 1245), "Chênh 150 mmHg:", 64, INK, alpha=k1)
    text(d, (W / 2, 1335), "cột khí dài bao nhiêu?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1430, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, g, tr, r, e = (sc[k] for k in ("hook", "do", "graph", "trap", "rut", "end"))
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + do["M"][2], "ding"), (g["t0"] + g["M"][0] + 1.4, "tap"),
            (tr["t0"] + 0.4, "buzz"), (tr["t0"] + tr["M"][1], "tap"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l12-boylecharles-03", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Định luật Boyle · thachlab.id.vn", scenes=[
 dict(key="hook", title="Ống chữ J một đầu kín", draw=s_hook, tail=0.3, caps=[
   ("Khí nhốt trong nhánh kín.", 3.0),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Rót thêm thuỷ ngân", draw=s_do, tail=0.3, caps=[
   ("Rót thêm, đợi 1 phút mỗi lần.", 3.9),
   ("Cột khí ngắn dần.", 3.0),
   ("Đáp án: p = p0 + h = 870 mmHg.", 4.0)]),
 dict(key="graph", title="Đồ thị p theo L", draw=s_graph, tail=0.3, caps=[
   ("Đường đẳng nhiệt: p·L không đổi.", 3.8)]),
 dict(key="trap", title="Bẫy: rót thêm, p·L tăng?", draw=s_trap, tail=0.3, caps=[
   ("Rót thêm chất lỏng, không thêm khí.", 3.8),
   ("Tích p·L giữ nguyên.", 3.4)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.3, caps=[
   ("Cột chất lỏng đè lên khí.", 3.6),
   ("Độ chênh h: phần áp suất thêm.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Nhiệt độ không đổi: p·L không đổi.", 6.4)]),
])
