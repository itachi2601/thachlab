# Clip: tn-l10-huongtam-02 - Dong xu tren ban xoay: ma sat nghi giu xu di vong (9/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-huongtam-02.json:
#   tham_so: r = 0,10 m (mac dinh), k = 0,3, g = 10 (gia_thiet) ; ghi_chu: nguong a = 3 m/s^2, khoang 52 vong/phut.
#   so_lieu_mau: n = 20 / 30 / 45 / 60 vong/phut -> omega 2,09 / 3,14 / 4,71 / 6,28 rad/s, a_ht 0,44 / 0,99 / 2,22 / 3,95 ;
#   truot: khong / khong / khong / co.
# Du doan (K10; v2 theo kiem-code 27/11): them xu to nang gap doi, cung cach tam 10 cm (doi dien). Quay nhanh dan,
#   xu nao truot truoc? Dap an: cung luc (k = Fms max / P co dinh trong tham_so -> nguong a = k.g khong phu thuoc m;
#   suy tu mo hinh, kho chua ghi thanh cau). Ca cu (huong tiep tuyen) bi bai noi o hop Bai 4 + bang "Dut day".
# Truc chinh: DIA NHIN TU TREN (mui ten ma sat nghi chi vao tam, dai ti le a_ht, chan o 3) + bieu do thanh a_ht vs nguong 3.
# Bay: "luc li tam day xu ra" (kho) -> ma sat nghi toi da 3 < can co 3,95.
# Cau chot (27/11, cong moi): r = 20 cm (tham_so 0,03-0,3 m), n = 45 vong/phut (tham_so 10-90), cung dia, cung xu:
#   a = 4,71^2 x 0,20 = 4,44 > 3 -> TRUOT (nguoc phan xa "45 vong/phut khong truot"). Dap so khong hien tren man.
from engine import *

N_ROWS = [20, 30, 45, 60]
OM = [2.09, 3.14, 4.71, 6.28]
AHT = [0.44, 0.99, 2.22, 3.95]
LIM = 3.0
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
COIN = (212, 160, 23); COIN_D = (146, 104, 8)
DISC = (226, 232, 240); DISC_D = (100, 116, 139); TABLE = (236, 231, 220)

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")

_TI = {}
def TI(size):                                   # Times Bold Italic cho omega (omega cua SF giong w)
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

TOKR = re.compile(r"(_\{[^}]*\}|\^\{[^}]*\}|ω)")
def eqr(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """chu co chi so duoi/tren (>= 55 px) va omega Times nghieng."""
    segs = []
    for p in [p for p in TOKR.split(s) if p]:
        if p.startswith("_{"): segs.append((p[2:-1], F(max(55, int(size * 0.8))), size * 0.26))
        elif p.startswith("^{"): segs.append((p[2:-1], F(max(55, int(size * 0.8))), -size * 0.34))
        elif p == "ω": segs.append((p, TI(size * 1.12), 0))
        else: segs.append((p, F(size), 0))
    tot = sum(tw(d, t, f) for t, f, _ in segs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for t, f, dy in segs:
        dtext(d, (x, cy + dy), t, f, color, alpha, "lm"); x += tw(d, t, f)
    return tot

def dashed(d, p, q, color, w=4, on=14, off=10):
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    if L < 1: return
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L; s = 0.0
    while s < L:
        e = min(L, s + on)
        d.line([(p[0] + ux * s, p[1] + uy * s), (p[0] + ux * e, p[1] + uy * e)], fill=color, width=w); s = e + off

# ---------------- dia xoay nhin tu tren (quay cung chieu kim dong ho) ----------------
CX, CY, RD = 360, 680, 270
RP = 180                                          # r = 10 cm -> 180 px
def P(th, r): return (CX + r * math.sin(th), CY - r * math.cos(th))
def UT(th): return (math.cos(th), math.sin(th))   # tiep tuyen theo chieu quay
def UR(th): return (math.sin(th), -math.cos(th))  # ban kinh huong ra

def disc(d, th, path=True):
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    d.rounded_rectangle((60, 290, 660, 985), radius=26, fill=TABLE)
    d.ellipse([CX - RD, CY - RD, CX + RD, CY + RD], fill=DISC, outline=DISC_D, width=6)
    for k in range(6):                            # nan ve tren dia cho thay dia quay
        a = th + k * math.pi / 3
        d.line([P(a, 40), P(a, RD - 10)], fill=(203, 213, 225), width=4)
    if path:
        for i in range(0, 72, 2):
            a0, a1 = i * 5, i * 5 + 5
            d.arc([CX - RP, CY - RP, CX + RP, CY + RP], a0, a1, fill=(148, 163, 184), width=3)
    d.ellipse([CX - 30, CY - 30, CX + 30, CY + 30], fill=(148, 163, 184), outline=DISC_D, width=4)
    dot(d, CX, CY, 8, NAVY)

def coin(d, x, y, k=1.0, big=False):
    r1, r2 = (38, 22) if big else (26, 14)
    d.ellipse([x - r1, y - r1, x + r1, y + r1], fill=A(COIN, k), outline=A(COIN_D, k), width=5 if big else 4)
    d.ellipse([x - r2, y - r2, x + r2, y + r2], outline=A(COIN_D, k), width=3)

# ---------------- dong thoi gian canh Tien hanh ----------------
ST = [0.4, 1.9, 3.4, 4.9]                         # moc bat dau tung n
TS = 6.0                                          # luc xu bat dau truot
SLOW = 4.0                                        # sau khi truot: quay cham x4

def stage(t):
    j = 0
    for i, s in enumerate(ST):
        if t >= s: j = i
    return j

def om_vis(t):
    if t < ST[0]: return OM[0]
    j = stage(t)
    w = OM[j] if j == 0 else lerp(OM[j - 1], OM[j], clamp((t - ST[j]) / 0.3))
    return w / SLOW if t >= TS else w

_TH = {}
def theta_raw(t):
    key = round(t, 2)
    if key in _TH: return _TH[key]
    s, x = 0.0, 0.0
    while x < key - 1e-9:
        s += om_vis(x) * 0.01; x += 0.01
    _TH[key] = s
    return s
TH0 = 1.5 * math.pi - theta_raw(TS)               # xu o ben trai tam (3pi/2) dung luc truot -> roi di thang len

def theta(t): return TH0 + theta_raw(t)
TH_S = 1.5 * math.pi
V_SLOW = OM[3] / SLOW * RP                        # px/s luc quay cham
S_MAX = 330
S_MAX2 = 270                                      # xu to (ben phai tam) roi xuong: dung truoc mep khung dia

def coin_pos(t):
    if t < TS:
        return P(theta(t), RP)
    s = min(S_MAX, (t - TS) * V_SLOW)
    p0 = P(TH_S, RP); u = UT(TH_S)
    return (p0[0] + u[0] * s, p0[1] + u[1] * s)

def coin2_pos(t):                                 # xu to, doi dien: cung nguong a = k.g -> truot cung luc TS
    if t < TS:
        return P(theta(t) + math.pi, RP)
    s = min(S_MAX2, (t - TS) * V_SLOW)
    p0 = P(TH_S + math.pi, RP); u = UT(TH_S + math.pi)
    return (p0[0] + u[0] * s, p0[1] + u[1] * s)

def trail(d, th0, s_end):
    p0 = P(th0, RP); u = UT(th0)
    for i in range(0, int(s_end), 22): dot(d, p0[0] + u[0] * i, p0[1] + u[1] * i, 5, COIN_D)

def a_now(t, scene_do=True):
    if t < ST[0]: return AHT[0]
    j = stage(t)
    return AHT[j] if j == 0 else lerp(AHT[j - 1], AHT[j], clamp((t - ST[j]) / 0.6))

# ---------------- chung ----------------
def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- bieu do thanh a_ht ----------------
X0B, PXU = 200, 160
ROWY = [1235, 1320, 1405, 1490]
def bars(d, grow):
    """grow[i] in [0,1]: thanh hang i da moc toi dau."""
    card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    eqr(d, W / 2, 1085, "gia tốc hướng tâm (m/s^{2})", 55, INK)
    text(d, (120, 1160), "vòng/phút", 55, INK, anchor="lm")
    xl = X0B + LIM * PXU
    for yy in range(1195, 1525, 24):
        d.line([(xl, yy), (xl, min(yy + 13, 1525))], fill=RED, width=5)
    text(d, (xl + 20, 1160), "tối đa 3", 55, RED, anchor="lm")
    for i in range(4):
        g = grow[i]
        y = ROWY[i]
        text(d, (120, y), str(N_ROWS[i]), 55, INK if g > 0 else LIGHT)
        if g <= 0: continue
        x1 = X0B + AHT[i] * PXU * g
        d.rectangle([X0B, y - 28, min(x1, xl), y + 28], fill=BLUE)
        if x1 > xl: d.rectangle([xl, y - 28, x1, y + 28], fill=(248, 113, 113))
        if g > 0.95:
            lw = tw(d, vn(AHT[i], 2), F(55))
            d.rectangle([x1 + 8, y - 30, x1 + 24 + lw, y + 30], fill=WHITE)      # che net dut gioi han sau nhan
            text(d, (x1 + 16, y), vn(AHT[i], 2), 55, DRED if AHT[i] > LIM else BLUE, anchor="lm")

def grows(t):
    return [clamp((t - ST[i]) / 0.6) if t >= ST[i] else 0.0 for i in range(4)]

def legend(d, k=1.0):
    arrow(d, (800, 630), (900, 630), A(RED, k), w=7, head=20)
    text(d, (850, 690), "ma sát nghỉ", 55, DRED, alpha=k)
    arrow(d, (800, 770), (900, 770), A(BLUE, k), w=7, head=20)
    text(d, (850, 830), "vận tốc", 55, BLUE, alpha=k)

def forces(d, th, a, w):
    x, y = P(th, RP)
    ur = UR(th); ut = UT(th)
    L = 24 + 45 * min(a, LIM)                     # ma sat nghi: chi VAO TAM (nguoc UR)
    arrow(d, (x - ur[0] * 28, y - ur[1] * 28), (x - ur[0] * (28 + L), y - ur[1] * (28 + L)), RED, w=7, head=14)
    V = 25 * w                                    # van toc: theo tiep tuyen, chieu quay
    arrow(d, (x + ut[0] * 28, y + ut[1] * 28), (x + ut[0] * (28 + V), y + ut[1] * (28 + V)), BLUE, w=7, head=18)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    th = TH0 + OM[0] * t
    disc(d, th, path=False)
    x, y = P(th, RP); x2, y2 = P(th + math.pi, RP)
    dashed(d, (CX, CY), (x, y), ORANGE, w=5); dashed(d, (CX, CY), (x2, y2), ORANGE, w=5)
    coin(d, x, y); coin(d, x2, y2, big=True)
    text(d, (850, 420), "Cùng cách", 55, INK)
    text(d, (850, 500), "tâm 10 cm", 55, INK)
    text(d, (850, 650), "Xu to:", 55, COIN_D)
    text(d, (850, 730), "nặng gấp đôi", 55, COIN_D)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1085 + (1 - k) * 30
    card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    for j, s1 in enumerate(("Quay nhanh dần:", "xu nào trượt trước?")):
        text(d, (W / 2, y0 + 190 + j * 85), s1, 60, PURPLE if j == 1 else INK, alpha=k)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh ----------------
def s_do(img, d, t, sc):
    th = theta(t)
    disc(d, th)
    cx, cy = coin_pos(t); c2 = coin2_pos(t)
    if t >= TS:
        trail(d, TH_S, min(S_MAX, (t - TS) * V_SLOW)); trail(d, TH_S + math.pi, min(S_MAX2, (t - TS) * V_SLOW))
        coin(d, cx, cy); coin(d, *c2, big=True)
    else:
        coin(d, *c2, big=True); coin(d, cx, cy)
        forces(d, th, a_now(t), om_vis(t))
    j = stage(t)
    card(d, (690, 310, 1010, 500), fill=NAVY, r=26)
    text(d, (850, 405), str(N_ROWS[j]), 80, WHITE)
    text(d, (850, 545), "vòng/phút", 55, INK)
    legend(d)
    if t >= TS:
        k = appear(t, TS, 0.3)
        cw = tw(d, "chậm ×4", F(55)) + 40
        card(d, (850 - cw / 2, 890, 850 + cw / 2, 970), fill=A((241, 245, 249), k), outline=A(DISC_D, k), r=30, w=3)
        text(d, (850, 930), "chậm ×4", 55, MUTED, alpha=k)
    bars(d, grows(t))

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    th = theta(TS) + OM[3] / SLOW * t
    disc(d, th)
    p0 = P(TH_S, RP); u = UT(TH_S)
    ke = (p0[0] + u[0] * S_MAX, p0[1] + u[1] * S_MAX)
    q0 = P(TH_S + math.pi, RP); v = UT(TH_S + math.pi)
    k1 = appear(t, 0.5, 0.4)
    dashed(d, (p0[0] - u[0] * 260, p0[1] - u[1] * 260), (p0[0] + u[0] * 360, p0[1] + u[1] * 360), A(BLUE, k1), w=5)
    trail(d, TH_S, S_MAX); trail(d, TH_S + math.pi, S_MAX2)
    coin(d, *ke); coin(d, q0[0] + v[0] * S_MAX2, q0[1] + v[1] * S_MAX2, big=True)
    text(d, (p0[0] + 45, p0[1] - 330), "tiếp tuyến", 55, BLUE, anchor="lm", alpha=k1)
    text(d, (850, 600), "60", 80, NAVY, alpha=k1)
    text(d, (850, 690), "vòng/phút", 55, INK, alpha=k1)
    ka = appear(t, M[1], 0.45)
    card(d, (40, 1060, 1040, 1440), fill=A(WHITE, ka), outline=A(NAVY, ka), w=6)
    pill(d, W / 2, 1140, "ĐÁP ÁN", NAVY, ka)
    text(d, (W / 2, 1255), "cùng lúc", 64, BLUE, alpha=ka)
    text(d, (W / 2, 1360), "nặng gấp đôi, ma sát gấp đôi", 55, INK, alpha=ka)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, 0.4, 0.45)
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    pill(d, W / 2, 340, "RÚT RA", GREEN, k1)
    text(d, (W / 2, 500), "Ma sát nghỉ đóng vai", 60, DRED, alpha=k1)
    text(d, (W / 2, 590), "lực hướng tâm", 60, DRED, alpha=k1)
    g = clamp((t - 0.6) / 1.8)                    # mui ten ma sat chi vao tam moc dan (hinh khong dung yen)
    dot(d, 300, 820, 14, NAVY); text(d, (300, 890), "tâm", 55, NAVY)
    coin(d, 800, 820)
    if g > 0: arrow(d, (760, 820), (760 - 400 * g, 820), A(RED, k1), w=8, head=24)
    k4 = appear(t, M[1] - 0.1, 0.45)
    if k4 <= 0: return
    yk = 1085 + (1 - k4) * 30
    card(d, (40, yk, 1040, yk + 420), fill=A(WHITE, k4), outline=A(NAVY, k4), w=6)
    pill(d, W / 2, yk + 70, "CHƯA NÓI ĐƯỢC", NAVY, k4)
    eqr(d, W / 2, yk + 200, "Giới hạn 3 m/s^{2}", 60, DRED, alpha=k4)
    text(d, (W / 2, yk + 300), "chỉ là giả định", 60, DRED, alpha=k4)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pill(d, W / 2, y0 + 70, "BẪY", DRED, a1)
    q = "Lực li tâm đẩy xu ra"
    ks = clamp((t - M[1]) / 0.4); lw = tw(d, q, F(58)); yy = 470
    text(d, (W / 2, yy), q, 58, mix(INK, GRAY, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
    # hinh: xu ben phai, tam ben trai ; hai mui ten deu chi VAO TAM
    xc, xt, L = 900, 170, 170
    kk = appear(t, M[1], 0.5)
    g = 0.05 + 0.95 * clamp((t - M[1]) / 3.6)
    dot(d, xt, 900, 14, A(NAVY, a1)); text(d, (xt, 970), "tâm", 55, NAVY, alpha=a1)
    coin(d, xc, 900, a1)
    if kk <= 0: return
    card(d, (80, 560, 1000, 760), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, 615), "Ma sát không đủ", 58, DGREEN, alpha=kk)
    text(d, (W / 2, 700), "kéo vào tâm", 58, DGREEN, alpha=kk)
    x2 = xc - 40 - 3.95 * L * g
    dashed(d, (xc - 40, 1090), (x2 + 20, 1090), A(PURPLE, kk), w=7)
    arrow(d, (x2 + 22, 1090), (x2, 1090), A(PURPLE, kk), w=7, head=22)
    text(d, (W / 2, 1170), "cần 3,95 m/s²", 58, PURPLE, alpha=kk)
    x3 = xc - 40 - 3.0 * L * g
    arrow(d, (xc - 40, 1300), (x3, 1300), A(RED, kk), w=8, head=22)
    text(d, (W / 2, 1380), "tối đa 3 m/s²", 58, DRED, alpha=kk)

# ---------------- canh 6: Thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 290, 1040, 1530), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 350, "THỬ NGHĨ", ORANGE, k)
    cx, cy, R, r2 = 400, 760, 300, 260            # 20 cm = 260 px (hinh rieng, khong cung ti le canh tren)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A(DISC, k), outline=A(DISC_D, k), width=6)
    th = 1.2 + 0.6 * t
    for j in range(6):
        a = th + j * math.pi / 3
        d.line([(cx + 40 * math.sin(a), cy - 40 * math.cos(a)), (cx + (R - 10) * math.sin(a), cy - (R - 10) * math.cos(a))], fill=A((203, 213, 225), k), width=4)
    dot(d, cx, cy, 10, A(NAVY, k))
    xx, yy = cx + r2 * math.sin(th), cy - r2 * math.cos(th)
    dashed(d, (cx, cy), (xx, yy), A(ORANGE, k), w=5)
    coin(d, xx, yy, k)
    text(d, (860, 560), "cách tâm", 55, INK, alpha=k)
    text(d, (860, 635), "20 cm", 55, DORANGE, alpha=k)
    text(d, (860, 800), "45", 55, DORANGE, alpha=k)
    text(d, (860, 875), "vòng/phút", 55, INK, alpha=k)
    text(d, (W / 2, 1170), "Gia tốc hướng tâm?", 60, DORANGE, alpha=k)
    text(d, (W / 2, 1260), "Có trượt không?", 60, DORANGE, alpha=k)
    seg_bar(d, 1380, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for s in ST[1:]: cs.append((do["t0"] + s, "tick"))
    cs.append((do["t0"] + TS, "tap"))
    cs += [(da["t0"] + da["M"][1], "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-huongtam-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực hướng tâm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xu trên bàn xoay", draw=s_hook, tail=0.2, caps=[
   ("Nhìn từ trên xuống.", 2.6),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Tăng dần tốc độ quay.", 2.6),
   ("Mũi tên đỏ dài dần.", 3.0),
   ("Cần hơn 3 m/s²: xu trượt.", 3.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Hai xu trượt ở 60 vòng/phút.", 3.4),
   ("Đáp án: cùng lúc.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Ma sát nghỉ đóng vai lực hướng tâm.", 4.3),
   ("Giới hạn 3 m/s² chỉ là giả định.", 4.3)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Lực li tâm đẩy xu ra?", 3.4),
   ("Ma sát không đủ kéo vào tâm.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.0)]),
])
