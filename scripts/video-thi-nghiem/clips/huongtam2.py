# Clip: tn-l10-huongtam-02 - Dong xu tren ban xoay: ma sat nghi giu xu di vong (9/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-huongtam-02.json:
#   tham_so: r = 0,10 m (mac dinh), k = 0,3, g = 10 (gia_thiet) ; ghi_chu: nguong a = 3 m/s^2, khoang 52 vong/phut.
#   so_lieu_mau: n = 20 / 30 / 45 / 60 vong/phut -> omega 2,09 / 3,14 / 4,71 / 6,28 rad/s, a_ht 0,44 / 0,99 / 2,22 / 3,95 ;
#   truot: khong / khong / khong / co.
# Du doan (K10: chi cau hoi + hinh): ngay khi truot, xu di theo huong nao? Dap an: gan theo tiep tuyen (kho:
#   hien_tuong_hay_sai "roi di gan theo tiep tuyen"). Nhieu (khung): theo ban kinh ra xa, vao tam, nguoc chieu quay.
# Truc chinh: DIA NHIN TU TREN (mui ten ma sat nghi chi vao tam, dai ti le a_ht, chan o 3) + bieu do thanh a_ht vs nguong 3.
# Bay: "luc li tam day xu ra" (kho) -> ma sat nghi toi da 3 < can co 3,95.
# Cau chot: r = 5 cm (chua tung hien, trong mien tham_so 3-30 cm), van 60 vong/phut: a = 1,97 < 3 -> KHONG truot
#   (nguoc phan xa "60 vong/phut la truot").
from engine import *

N_ROWS = [20, 30, 45, 60]
OM = [2.09, 3.14, 4.71, 6.28]
AHT = [0.44, 0.99, 2.22, 3.95]
LIM = 3.0
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
    """chu co chi so duoi/tren (>= 40 px) va omega Times nghieng."""
    segs = []
    for p in [p for p in TOKR.split(s) if p]:
        if p.startswith("_{"): segs.append((p[2:-1], F(max(40, int(size * 0.7))), size * 0.26))
        elif p.startswith("^{"): segs.append((p[2:-1], F(max(40, int(size * 0.7))), -size * 0.34))
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

def coin(d, x, y, k=1.0):
    d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=A(COIN, k), outline=A(COIN_D, k), width=4)
    d.ellipse([x - 14, y - 14, x + 14, y + 14], outline=A(COIN_D, k), width=3)

# ---------------- dong thoi gian canh Tien hanh ----------------
ST = [0.4, 2.4, 4.4, 6.4]                         # moc bat dau tung n
TS = 7.2                                          # luc xu bat dau truot
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

def coin_pos(t):
    if t < TS:
        return P(theta(t), RP)
    s = min(S_MAX, (t - TS) * V_SLOW)
    p0 = P(TH_S, RP); u = UT(TH_S)
    return (p0[0] + u[0] * s, p0[1] + u[1] * s)

def a_now(t, scene_do=True):
    if t < ST[0]: return AHT[0]
    j = stage(t)
    return AHT[j] if j == 0 else lerp(AHT[j - 1], AHT[j], clamp((t - ST[j]) / 0.6))

# ---------------- bieu do thanh a_ht ----------------
X0B, PXU = 200, 160
ROWY = [1190, 1280, 1370, 1460]
def bars(d, grow):
    """grow[i] in [0,1]: thanh hang i da moc toi dau."""
    card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    eqr(d, W / 2, 1080, "a_{ht} cần có (m/s^{2})", 46, INK)
    text(d, (140, 1135), "vòng/phút", 40, INK, bold=False)
    xl = X0B + LIM * PXU
    for yy in range(1150, 1505, 24):
        d.line([(xl, yy), (xl, min(yy + 13, 1505))], fill=RED, width=5)
    text(d, (xl, 1545), "ma sát tối đa: 3", 40, RED)
    for i in range(4):
        g = grow[i]
        y = ROWY[i]
        text(d, (110, y), str(N_ROWS[i]), 44, INK if g > 0 else LIGHT)
        if g <= 0: continue
        x1 = X0B + AHT[i] * PXU * g
        d.rectangle([X0B, y - 26, min(x1, xl), y + 26], fill=BLUE)
        if x1 > xl: d.rectangle([xl, y - 26, x1, y + 26], fill=(248, 113, 113))
        if g > 0.95: text(d, (x1 + 16, y), vn(AHT[i], 2), 40, RED if AHT[i] > LIM else BLUE, anchor="lm")

def grows(t):
    out = []
    for i in range(4):
        out.append(clamp((t - ST[i]) / 0.6) if t >= ST[i] else 0.0)
    return out

def legend(d, k=1.0):
    arrow(d, (700, 700), (760, 700), A(RED, k), w=6, head=18)
    text(d, (775, 700), "ma sát nghỉ", 40, RED, anchor="lm", alpha=k)
    arrow(d, (700, 790), (760, 790), A(BLUE, k), w=6, head=18)
    text(d, (775, 790), "vận tốc", 40, BLUE, anchor="lm", alpha=k)

def forces(d, th, a, w):
    x, y = P(th, RP)
    ur = UR(th); ut = UT(th)
    L = 24 + 45 * min(a, LIM)
    arrow(d, (x - ur[0] * 28, y - ur[1] * 28), (x - ur[0] * (28 + L), y - ur[1] * (28 + L)), RED, w=7, head=14)
    V = 25 * w
    arrow(d, (x + ut[0] * 28, y + ut[1] * 28), (x + ut[0] * (28 + V), y + ut[1] * (28 + V)), BLUE, w=7, head=18)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    th = TH0 + OM[0] * t
    disc(d, th, path=False)
    x, y = P(th, RP)
    dashed(d, (CX, CY), (x, y), ORANGE, w=5)
    coin(d, x, y)
    text(d, (850, 420), "đồng xu", 44, COIN_D)
    text(d, (850, 500), "cách tâm 10 cm", 40, INK)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=33)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 175, "Quay nhanh dần tới khi trượt.", 48, INK, maxw=920, alpha=a)
    ctext(d, y0 + 300, "So với mặt bàn, xu đi hướng nào?", 48, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 1.4, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 484], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 484], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def s_do(img, d, t, sc):
    th = theta(t)
    disc(d, th)
    cx, cy = coin_pos(t)
    if t >= TS:
        p0 = P(TH_S, RP)
        for i in range(0, int(math.hypot(cx - p0[0], cy - p0[1])), 22):
            u = UT(TH_S); dot(d, p0[0] + u[0] * i, p0[1] + u[1] * i, 5, COIN_D)
        coin(d, cx, cy)
        k = appear(t, TS + 0.2, 0.3)
        text(d, (cx + 70, cy + 10), "trượt!", 44, RED, anchor="lm", alpha=k)
    else:
        coin(d, cx, cy)
        forces(d, th, a_now(t), om_vis(t))
    j = stage(t)
    card(d, (690, 310, 1010, 520), fill=NAVY, r=26)
    text(d, (850, 415), str(N_ROWS[j]), 80, WHITE)
    text(d, (850, 580), "vòng/phút", 40, INK)
    legend(d)
    if t >= TS:
        k = appear(t, TS, 0.3)
        cw = tw(d, "chậm ×4", F(40)) + 40
        card(d, (850 - cw / 2, 880, 850 + cw / 2, 940), fill=A((241, 245, 249), k), outline=A(DISC_D, k), r=30, w=3)
        text(d, (850, 910), "chậm ×4", 40, MUTED, alpha=k)
    bars(d, grows(t))

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    th = theta(TS) + OM[3] / SLOW * t
    disc(d, th)
    p0 = P(TH_S, RP); u = UT(TH_S)
    ke = (p0[0] + u[0] * S_MAX, p0[1] + u[1] * S_MAX)
    k1 = appear(t, 0.6, 0.4)
    dashed(d, (p0[0] - u[0] * 260, p0[1] - u[1] * 260), (p0[0] + u[0] * 360, p0[1] + u[1] * 360), A(BLUE, k1), w=5)
    rb = (p0[0] + UR(TH_S)[0] * 120, p0[1] + UR(TH_S)[1] * 120)
    dashed(d, (CX, CY), rb, A(GRAY, k1), w=5)
    for i in range(0, S_MAX, 22): dot(d, p0[0] + u[0] * i, p0[1] + u[1] * i, 5, COIN_D)
    coin(d, *ke)
    text(d, (p0[0] + 45, p0[1] - 340), "tiếp tuyến", 40, BLUE, anchor="lm", alpha=k1)
    text(d, (400, CY + 95), "bán kính", 40, MUTED, anchor="lm", alpha=k1)
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · gần theo tiếp tuyến"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 1050, W / 2 + pw / 2, 1118), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 1084), lb, 40, WHITE, alpha=ka)
    card(d, (40, 1150, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    k2, k3 = appear(t, 1.4, 0.4), appear(t, 2.6, 0.4)
    ctext(d, 1290, "Thiếu lực kéo vào", 48, RED, alpha=k2)
    ctext(d, 1440, "→ xu đi theo vận tốc", 48, BLUE, alpha=k3)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    k1, k2, k3 = appear(t, 0.5, 0.45), appear(t, 1.5, 0.45), appear(t, 2.7, 0.45)
    ctext(d, 380, "Ma sát nghỉ đóng vai", 52, RED, alpha=k1)
    ctext(d, 455, "lực hướng tâm", 52, RED, alpha=k1)
    eqr(d, W / 2, 630, "a_{ht} cần có = ω^{2}·r", 54, PURPLE, alpha=k2)
    eqr(d, W / 2, 810, "Vượt 3 m/s^{2}: xu trượt", 54, INK, alpha=k3)
    k4 = appear(t, M[1] - 0.1, 0.45)
    card(d, (40, 1030, 1040, 1590), fill=A(WHITE, k4), outline=A(NAVY, k4), w=6)
    text(d, (W / 2, 1100), "Chưa nói được", 46, NAVY, alpha=k4)
    kk = k4 * appear(t, M[1] + 0.3, 0.4)
    card(d, (80, 1180, 1000, 1500), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
    eqr(d, W / 2, 1300, "Giới hạn 3 m/s^{2}", 48, RED, alpha=kk)
    text(d, (W / 2, 1390), "chỉ là giả định", 48, RED, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 96), fill=A(RED, a1), r=33)
    text(d, (W / 2, y0 + 63), "BẪY", 40, WHITE, alpha=a1)
    s = "✗ Lực li tâm đẩy xu ra"
    text(d, (W / 2, 470), s, 50, RED, alpha=a1)
    sw = tw(d, s, F(50))
    d.line([(W / 2 - sw / 2 + 60, 472), (W / 2 + sw / 2, 472)], fill=A(RED, a1), width=5)
    # hinh 1: mui ten "day ra" bi gach
    dot(d, 260, 640, 12, A(NAVY, a1))
    coin(d, 560, 640, a1)
    dashed(d, (600, 640), (800, 640), A(RED, a1), w=6)
    arrow(d, (790, 640), (810, 640), A(RED, a1), w=6, head=22)
    d.line([(660, 590), (760, 690)], fill=A(RED, a1), width=8); d.line([(660, 690), (760, 590)], fill=A(RED, a1), width=8)
    kk = appear(t, M[0] + 2.3, 0.5)
    if kk <= 0: return
    card(d, (80, 830, 1000, 1550), fill=A((236, 253, 243), kk), r=24)
    ctext(d, 905, "✓ Ma sát nghỉ không đủ", 48, GREEN, alpha=kk)
    ctext(d, 970, "kéo vào tâm", 48, GREEN, alpha=kk)
    xc, xt = 860, 160                                       # xu ben phai, tam ben trai
    dot(d, xt, 1260, 12, A(NAVY, kk))
    coin(d, xc + 40, 1260, kk)
    L = 170
    dashed(d, (xc, 1170), (xc - 3.95 * L, 1170), A(PURPLE, kk), w=7)
    arrow(d, (xc - 3.95 * L + 20, 1170), (xc - 3.95 * L, 1170), A(PURPLE, kk), w=7, head=22)
    eqr(d, xc - 1.97 * L, 1110, "cần có: 3,95 m/s^{2}", 40, PURPLE, alpha=kk)
    arrow(d, (xc, 1350), (xc - 3.0 * L, 1350), A(RED, kk), w=8, head=22)
    eqr(d, xc - 1.5 * L, 1410, "tối đa: 3 m/s^{2}", 40, RED, alpha=kk)

# ---------------- canh 6: Chot ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):
        cx, cy, rr = 330, 1110, 150                          # dia nho: 15 cm = 150 px
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=A(DISC, k), outline=A(DISC_D, k), width=4)
        dot(d, cx, cy, 7, A(NAVY, k))
        d.ellipse([cx + 100 - 22, cy - 22, cx + 100 + 22, cy + 22], outline=A(DISC_D, k), width=4)
        d.ellipse([cx + 50 - 22, cy - 22, cx + 50 + 22, cy + 22], fill=A(COIN, k), outline=A(COIN_D, k), width=4)
        arrow(d, (cx + 98, cy + 46), (cx + 56, cy + 46), A(NAVY, k), w=5, head=14)
        d.line([(cx + 100, cy - 24), (560, 1040)], fill=A(NAVY, k), width=3)
        text(d, (570, 1040), "10 cm", 40, NAVY, anchor="lm", alpha=k)
        d.line([(cx + 50, cy + 24), (560, 1190)], fill=A(COIN_D, k), width=3)
        text(d, (570, 1190), "5 cm", 40, COIN_D, anchor="lm", alpha=k)
        kh = appear(t, M[0] + 2.8, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        eqr(d, W / 2, 1450, "So a_{ht} với 3 m/s^{2}", 44, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Ma sát nghỉ giữ xu đi vòng tròn",
             "Xu cách tâm 5 cm, 60 vòng/phút:\ncó trượt?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for s in ST[1:]: cs.append((do["t0"] + s, "tick"))
    cs.append((do["t0"] + TS, "tap"))
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + 0.15, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-huongtam-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực hướng tâm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đồng xu trên bàn xoay", draw=s_hook, tail=0.5, caps=[
   ("Nhìn từ trên xuống.", 2.6),
   ("Dừng video, chọn đáp án.", 6.3)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Tăng dần tốc độ quay.", 3.0),
   ("Mũi tên đỏ dài dần.", 3.8),
   ("Cần hơn 3 m/s²: xu trượt.", 3.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("So vệt xu với hai đường.", 5.6)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Lực nào giữ xu đi vòng?", 3.8),
   ("Còn điều chưa biết.", 4.2)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("Xu trượt vì bị đẩy?", 5.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])
