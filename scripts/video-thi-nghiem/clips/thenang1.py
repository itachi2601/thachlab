# Clip: tn-l11-the-nang-dien-01 - Khay nuoc muoi hai la dong: the nang cua 1 C (moc la am) ti le khoang cach x (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-the-nang-dien-01.json:
#   tham_so: U = 6,0 V ; D = 10,0 cm ; x 0-10 cm (que do giua hai la).
#   so_lieu_mau (x cm, V do V, V/x V/m): 2,0 1,18 59,0 ; 4,0 2,43 60,8 ; 6,0 3,57 59,5 ; 8,0 4,84 60,5 ; E ~ 60 V/m.
# Khac clip tn-l11-dien-the-01 (cung khay): clip nay nhan "the nang cua 1 C" -- hinh co dien tich +1 C truot giua hai la,
#   do thi W cua 1 C theo x, bay "quen noi moc", cau chot hoi DAU cua W khi doi moc sang la duong (khong hoi so).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (que do 2 cm cham, tua 4-6-8 cm, bang x - so chi)
#       -> Dap an B (do thi W theo x thang qua goc + bang V/x + W = qEx) -> Bay (quen moc) roi Chua noi duoc
#       -> Chot + cau hoi tu nho lai (moc la duong: W sat la am duong hay am?).
from engine import *

ROWS = [(2.0, 1.18, 59.0), (4.0, 2.43, 60.8), (6.0, 3.57, 59.5), (8.0, 4.84, 60.5)]   # so_lieu_mau
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
WATER = (205, 230, 250)
DRED = (185, 28, 28)
EFLD = (95, 115, 160)
DGREEN = (0, 82, 36)

# ---------------- khay (nhin tu tren xuong, khung nguon 1080x1920) ----------------
# Von ke o TREN khay (day que do tha thang xuong), nguon o DUOI khay, thuoc nam trong long khay sat day:
# khong day nao cat thuoc / duong suc / nhan so (gop y cong B vong 1).
XN, XP = 200, 880                 # la am (trai), la duong (phai): 10,0 cm = 680 px
PXC = (XP - XN) / 10.0            # px / cm
YT, YB = 380, 800                 # mep tren / duoi khay
YPR = 545                         # duong que do / dien tich di
YRU = 700                         # vach thuoc
def px(x): return XN + x * PXC

def measure(d, x, ka=1.0):
    """Doan do x: mui ten hai dau tu la am toi que do, ngay tren thuoc, nhan x cam to."""
    if x is None or x < 0.3 or ka <= 0: return
    y = 662; x1 = px(x)
    d.line([(XN + 14, y), (x1 - 4, y)], fill=A(ORANGE, ka), width=6)
    arrow(d, (XN + 40, y), (XN + 14, y), A(ORANGE, ka), w=6, head=18)
    arrow(d, (x1 - 30, y), (x1 - 4, y), A(ORANGE, ka), w=6, head=18)
    cx = (XN + x1) / 2 if x1 - XN >= 240 else x1 + 44     # x nho: nhan dat ben phai dau mui ten, khong che than
    card(d, (cx - 30, y - 30, cx + 30, y + 30), fill=A(WHITE, ka), outline=A(ORANGE, ka), r=14, w=3)
    text(d, (cx, y - 2), "x", 48, ORANGE, alpha=ka)

def tray(d, probe=None, reading=None, token=None, tok_alpha=1.0, mx=None, mk=0.0):
    """Khay + hai la + nguon + thuoc + von ke. probe = x (cm) que do; reading = chuoi so chi; token = x cua +1 C;
    mx = x cua doan do (mk = do hien)."""
    card(d, (60, YT, 1020, YB), fill=WATER, outline=NAVY, r=26, w=5)
    for y in (470, 620):          # duong suc: tu la duong sang la am (E huong sang trai)
        for xx in range(int(XP - 40), int(XN + 60), -36): d.line([(xx, y), (xx - 18, y)], fill=EFLD, width=4)
        arrow(d, (XN + 80, y), (XN + 42, y), EFLD, w=4, head=16)
    text(d, (842, 428), "E", 44, EFLD)                     # nhan E (x 8-10 cm, ngoai duong day que do), mui ten ve la am
    arrow(d, (818, 428), (760, 428), EFLD, w=5, head=18)
    d.rectangle([XN - 11, YT + 25, XN + 11, YB - 25], fill=(184, 115, 51), outline=NAVY, width=3)
    d.rectangle([XP - 11, YT + 25, XP + 11, YB - 25], fill=(184, 115, 51), outline=NAVY, width=3)
    text(d, (145, 440), "−", 64, BLUE); text(d, (935, 440), "+", 64, RED)
    # thuoc ke dat duoi day khay (nhin xuyen qua nuoc)
    d.line([(XN, YRU), (XP, YRU)], fill=NAVY, width=4)
    for c in range(1, 10):
        d.line([(px(c), YRU), (px(c), YRU + (22 if c % 2 == 0 else 12))], fill=NAVY, width=3)
        if c % 2 == 0: text(d, (px(c), 752), str(c), 40, INK, bold=False)
    text(d, (160, 752), "0", 40, INK, bold=False)
    text(d, (900, 752), "10 cm", 40, INK, bold=False, anchor="lm")
    # nguon 6,0 V phia duoi
    d.line([(XN, YB - 25), (XN, 870), (390, 870)], fill=NAVY, width=4)
    d.line([(XP, YB - 25), (XP, 870), (690, 870)], fill=NAVY, width=4)
    card(d, (390, 832, 690, 908), fill=WHITE, outline=NAVY, r=16, w=4)
    text(d, (540, 870), "nguồn 6,0 V", 40, INK)
    # von ke phia tren: cuc am noi la am, que do tha thang xuong
    d.line([(330, 265), (XN, 265), (XN, YT + 25)], fill=NAVY, width=4)
    if probe is not None:
        tx = px(probe)
        d.line([(540, 318), (540, 345), (tx, 345), (tx, YPR)], fill=RED, width=4, joint="curve")
        dot(d, tx, YPR, 12, RED, outline=WHITE)
    card(d, (330, 212, 750, 318), fill=(70, 78, 100), r=20)
    card(d, (350, 224, 600, 306), fill=(220, 240, 225), r=12)
    text(d, (475, 265), reading if reading else "", 50, (20, 60, 30))
    text(d, (675, 265), "vôn kế", 40, WHITE, bold=False)
    measure(d, mx, mk)
    if token is not None and tok_alpha > 0:
        tx = px(token)
        d.ellipse([tx - 52, YPR - 52, tx + 52, YPR + 52], fill=A(ORANGE, tok_alpha), outline=A(WHITE, tok_alpha), width=4)
        text(d, (tx, YPR), "+1 C", 36, WHITE, alpha=tok_alpha)

def table(d, n, y=1040, hl=None):
    card(d, (140, y, 940, y + 500), fill=WHITE, outline=NAVY, w=4)
    xs = (340, 740)
    for x, c in zip(xs, ("x (cm)", "Số chỉ (V)")): text(d, (x, y + 52), c, 40, INK)
    d.line([(170, y + 92), (910, y + 92)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 150 + i * 92; x, v, _ = ROWS[i]
        if hl == i: d.rounded_rectangle([160, yy - 40, 920, yy + 40], radius=18, fill=(255, 237, 213))
        text(d, (xs[0], yy), vn(x), 44, INK); text(d, (xs[1], yy), vn(v, 2), 46, BLUE)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    tok = refl(1.5 + 1.6 * t, 1.5, 8.5)          # dien tich +1 C truot qua lai, cach moi la >= 1,5 cm
    ka = appear(t, 0.3, 0.5)
    tray(d, token=tok, tok_alpha=ka)
    text(d, (W / 2, 972), "+1 C được dời bằng tay", 40, INK, bold=False, alpha=ka)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 270, "Đi từ lá âm sang lá dương,\nthế năng của 1 C\nthay đổi thế nào?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 512], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 512], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
FF0, FFW = 0.2, 1.3

def s_do(img, d, t, sc):
    M = sc["M"]
    if t < M[1]:                                  # que do toi x = 2 cm, lam cham
        pr = lerp(5.0, 2.0, ease((t - 0.4) / 1.1)) if t >= 0.4 else None
        got = t >= 1.7                            # so chi + hang 1 hien CUNG luc
        tray(d, probe=pr, reading="1,18 V" if got else "", mx=pr if t >= 1.5 else None, mk=appear(t, 1.5, 0.3))
        table(d, 1 if got else 0)
        return
    card(d, (420, 1560, 660, 1620), fill=ORANGE, r=30); text(d, (540, 1590), "tua nhanh", 38, WHITE)
    u = t - M[1] - FF0
    if u < 0:
        tray(d, probe=2.0, reading="1,18 V", mx=2.0, mk=1.0); table(d, 1); return
    j = 1 + max(0, min(2, int(u // FFW))); w = u - (j - 1) * FFW
    x, v, _ = ROWS[j]
    pr = lerp(ROWS[j - 1][0], x, ease(w / 0.45))
    got = w >= 0.45                               # toi noi: so chi moi + hang moi cung luc; dang doi: giu so cu = hang cuoi
    rd = vn(v, 2) + " V" if got else vn(ROWS[j - 1][1], 2) + " V"
    tray(d, probe=pr, reading=rd, mx=pr, mk=1.0)
    table(d, j + (1 if got else 0))

# ---------------- canh 3: Dap an + rut ra ----------------
GX0, GX1, GY0, GY1 = 200, 900, 800, 420         # truc: x 0-10 cm, W 0-6 J
def gx(x): return GX0 + x / 10 * (GX1 - GX0)
def gy(w): return GY0 - w / 6 * (GY0 - GY1)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · tăng tỉ lệ x"
    pw = tw(d, lab, F(40)) + 52
    card(d, (W - 60 - pw, 236, W - 60, 296), fill=A(NAVY, ka), r=30)
    text(d, (W - 60 - pw / 2, 266), lab, 40, WHITE, alpha=ka)
    card(d, (40, 320, 1040, 950), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 40, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 16, GY0), (GX1 + 40, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 20, GY1 - 40), "W của 1 C (J)", 40, INK, anchor="lm")
    text(d, (GX1 + 40, GY0 - 40), "x (cm)", 40, INK, anchor="rm")
    for x in (2, 4, 6, 8, 10):
        d.line([(gx(x), GY0), (gx(x), GY0 + 12)], fill=NAVY, width=3); text(d, (gx(x), GY0 + 40), str(x), 40, INK, bold=False)
    for w in (2, 4, 6):
        d.line([(GX0 - 12, gy(w)), (GX0, gy(w))], fill=NAVY, width=3); text(d, (GX0 - 22, gy(w)), str(w), 40, INK, bold=False, anchor="rm")
    text(d, (gx(0), GY0 + 95), "lá âm", 40, BLUE, anchor="mm")
    text(d, (gx(10), GY0 + 95), "lá dương", 40, RED, anchor="mm")
    kl = appear(t, M[0] + 0.6, 0.8)              # mo hinh W = 0,6 x (J, x tinh bang cm) cho q = 1 C
    if kl > 0:
        x1 = 10 * kl
        d.line([(gx(0), gy(0)), (gx(x1), gy(0.6 * x1))], fill=A(GREEN, 0.9), width=5)
    for i, (x, v, _) in enumerate(ROWS):
        k = appear(t, 0.2 + 0.15 * i, 0.3)
        if k > 0: dot(d, gx(x), gy(v), 13, A(BLUE, k), outline=WHITE)
    # bang: x - W cua 1 C - V/x (T8)
    y = 970; kt = appear(t, 0.3, 0.4)
    card(d, (40, y, 1040, y + 470), fill=WHITE, outline=NAVY, w=4)
    xs = (190, 520, 860)
    km = appear(t, 0.3, 0.6)
    text(d, (xs[0], y + 50), "x (cm)", 40, INK); text(d, (xs[2], y + 50), "V/x (V/m)", 40, INK)
    if km < 1: text(d, (xs[1], y + 50), "Số chỉ (V)", 40, INK, alpha=1 - km)
    if km > 0: text(d, (xs[1], y + 50), "W = 1 C × V (J)", 40, ORANGE, alpha=km)
    d.line([(70, y + 88), (1010, y + 88)], fill=LIGHT, width=4)
    if kt > 0: d.rounded_rectangle([370, y + 12, 670, y + 456], radius=18, outline=A(ORANGE, kt), width=5)
    for i, (x, v, r) in enumerate(ROWS):
        yy = y + 140 + i * 88
        text(d, (xs[0], yy), vn(x), 42, INK); text(d, (xs[1], yy), vn(v, 2), 44, BLUE)
        if t >= 0.3 + 0.2 * i: text(d, (xs[2], yy), vn(r), 44, INK)
    kq = appear(t, 0.3, 0.4)
    if kq > 0:
        card(d, (40, 1452, 1040, 1536), fill=A((255, 237, 213), kq), outline=A(ORANGE, kq), r=20, w=3)
        text(d, (W / 2, 1494), "q = 1 C nên số vôn = số jun (1 V = 1 J/C)", 40, (154, 52, 18), alpha=kq)
    kn = appear(t, M[1] + 0.5, 0.4)
    if kn > 0:
        card(d, (40, 1550, 1040, 1630), fill=A((236, 253, 243), kn), outline=A(GREEN, kn), r=20, w=3)
        text(d, (W / 2, 1590), "E đều giữa hai lá: W = qEx, E ≈ 60 V/m", 40, DGREEN, alpha=kn)

# ---------------- canh 4: Bay roi Chua noi duoc (khong hien cung luc) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k2)
    tray(d, probe=2.0, reading="1,18 V")
    if a1 > 0:
        y0 = 1040
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“W = 1,18 J”"
        ks = clamp((t - 1.2) / 0.4); f = F(52); lw = tw(d, q, f); yy = y0 + 190
        text(d, (W / 2, yy), q, 52, DRED, alpha=a1)
        text(d, (W / 2, yy + 72), "không nói mốc", 42, DRED, bold=True, alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=5)
        kc = a1 * appear(t, 1.7, 0.5)
        if kc > 0:
            s1, s2 = "✓ W = 1,18 J ", "(mốc ở lá âm)"; f1, f2 = F(48), F(50)
            w1, w2 = tw(d, s1, f1), tw(d, s2, f2); x0 = W / 2 - (w1 + w2) / 2; yc = y0 + 410
            dtext(d, (x0, yc), s1, f1, DGREEN, kc, "lm"); dtext(d, (x0 + w1, yc), s2, f2, DGREEN, kc, "lm")
            d.line([(x0 + w1, yc + 34), (x0 + w1 + w2, yc + 34)], fill=A(DGREEN, kc), width=5)
    if k2 > 0:
        y0 = 1040 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Gần mép lá: chưa đo", "• Lực lên 1 C: không đo trực tiếp")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 220 + j * 140), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: doi moc sang la duong, W sat la am mang dau gi; goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 390, "Mốc ở lá âm: thế năng tỉ lệ với x", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1330), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 674), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 642), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 830, "Mốc ở lá dương.\nSát lá âm, W của 1 C\nmang dấu + hay −?", 48, INK, maxw=920,
          alpha=appear(t, M[0] + 0.9, 0.5))
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (110, 1030, 970, 1280), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1085, "Gợi ý", 38, INK, alpha=kh)
    ctext(d, 1190, "Về phía lá âm, W giảm", 44, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.3, "ding"),
           (do["t0"] + 1.7, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW, "tick") for j in range(3)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out

CLIP = dict(id="tn-l11-the-nang-dien-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Thế năng điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Khay nước muối, hai lá đồng", draw=s_hook, tail=0.8, caps=[
   ("Mốc thế năng chọn ở lá âm.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Que đo cách lá âm 2 cm.", 4.0),
   ("Dời que tới 4, 6, 8 cm.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Với 1 C, số vôn = số jun.", 4.4),
   ("Thế năng tăng đều theo x.", 5.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: quên nói mốc.", 3.6),
   ("Que đo chỉ dời giữa hai lá.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
