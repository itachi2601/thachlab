# Clip: tn-l11-the-nang-dien-01 - Khay nuoc muoi hai la dong: the nang cua 1 C (moc la am) ti le khoang cach x (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-the-nang-dien-01.json:
#   tham_so: U = 6,0 V ; D = 10,0 cm ; x 0-10 cm (que do giua hai la).
#   so_lieu_mau (x cm, V do V, V/x V/m): 2,0 1,18 59,0 ; 4,0 2,43 60,8 ; 6,0 3,57 59,5 ; 8,0 4,84 60,5 ; E ~ 60 V/m.
# Khac clip tn-l11-dien-the-01 (cung khay): clip nay nhan "the nang cua 1 C" -- hinh co dien tich +1 C truot giua hai la,
#   do thi W cua 1 C theo x, bay "quen noi moc", cau chot hoi DAU cua W khi doi moc sang la duong (khong hoi so).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (que do 2 cm cham, tua 4-6-8 cm, bang x - so chi)
#       -> Dap an B (do thi W theo x thang qua goc + bang V/x + W = qEx) -> Bay (quen moc) roi Chua noi duoc
#       -> THU NGHI (cong moi 27/11): doi moc sang la duong, W cua 1 C tai x = 2 cm? -> 1,18 - 6,0 ~ -4,8 J (tu suy;
#       khong hien tren man). Khong hop chot xanh; goi y trung tinh 'moc moi o dau?'.
# Cong moi 27/11: chu >= 56, moi canh <= 180 tu/phut, khoi chu cach >= 2,5 s, Bay cac nhip >= 3 s, thanh dem 5 o 70 px.
from engine import *

ROWS = [(2.0, 1.18, 59.0), (4.0, 2.43, 60.8), (6.0, 3.57, 59.5), (8.0, 4.84, 60.5)]   # so_lieu_mau
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
WATER = (205, 230, 250)
DRED = (185, 28, 28)
EFLD = (95, 115, 160)
DGREEN = (0, 82, 36)

# ---------------- khay (nhin tu tren xuong, khung nguon 1080x1920) ----------------
XN, XP = 200, 880                 # la am (trai), la duong (phai): 10,0 cm = 680 px
PXC = (XP - XN) / 10.0            # px / cm
YT, YB = 380, 800                 # mep tren / duoi khay
YPR = 545                         # duong que do / dien tich di
YRU = 700                         # vach thuoc
def px(x): return XN + x * PXC

def measure(d, x, ka=1.0):
    """Doan do x: mui ten hai dau tu la am toi que do, ngay tren thuoc, nhan x."""
    if x is None or x < 0.3 or ka <= 0: return
    y = 662; x1 = px(x)
    d.line([(XN + 14, y), (x1 - 4, y)], fill=A(ORANGE, ka), width=6)
    arrow(d, (XN + 40, y), (XN + 14, y), A(ORANGE, ka), w=6, head=18)
    arrow(d, (x1 - 30, y), (x1 - 4, y), A(ORANGE, ka), w=6, head=18)
    cx = (XN + x1) / 2 if x1 - XN >= 240 else x1 + 48
    card(d, (cx - 34, y - 34, cx + 34, y + 34), fill=A(WHITE, ka), outline=A(ORANGE, ka), r=14, w=3)
    text(d, (cx, y - 2), "x", 56, ORANGE, alpha=ka)

def tray(d, probe=None, reading=None, token=None, tok_alpha=1.0, mx=None, mk=0.0, la=1.0, vk=True):
    """Khay + hai la + nguon + thuoc + von ke. probe = x (cm) que do; reading = so chi; token = x cua +1 C."""
    card(d, (60, YT, 1020, YB), fill=WATER, outline=NAVY, r=26, w=5)
    for y in (470, 620):          # duong suc: tu la duong sang la am (E huong sang trai)
        for xx in range(int(XP - 40), int(XN + 60), -36): d.line([(xx, y), (xx - 18, y)], fill=EFLD, width=4)
        arrow(d, (XN + 80, y), (XN + 42, y), EFLD, w=4, head=16)
    text(d, (842, 425), "E", 58, EFLD)
    arrow(d, (812, 428), (752, 428), EFLD, w=5, head=18)
    d.rectangle([XN - 11, YT + 25, XN + 11, YB - 25], fill=(184, 115, 51), outline=NAVY, width=3)
    d.rectangle([XP - 11, YT + 25, XP + 11, YB - 25], fill=(184, 115, 51), outline=NAVY, width=3)
    text(d, (140, 440), "−", 64, BLUE); text(d, (940, 440), "+", 64, RED)
    d.line([(XN, YRU), (XP, YRU)], fill=NAVY, width=4)
    for c in range(1, 10):
        d.line([(px(c), YRU), (px(c), YRU + (22 if c % 2 == 0 else 12))], fill=NAVY, width=3)
        if c % 2 == 0: text(d, (px(c), 752), str(c), 56, INK, bold=False)
    text(d, (px(8) + 66, 752), "cm", 56, INK, bold=False)
    d.line([(XN, YB - 25), (XN, 870), (350, 870)], fill=NAVY, width=4)
    d.line([(XP, YB - 25), (XP, 870), (730, 870)], fill=NAVY, width=4)
    card(d, (350, 828, 730, 912), fill=WHITE, outline=NAVY, r=16, w=4)
    text(d, (540, 870), "nguồn 6,0 V", 56, INK, alpha=la)
    if vk:
        d.line([(330, 265), (XN, 265), (XN, YT + 25)], fill=NAVY, width=4)
        if probe is not None:
            tx = px(probe)
            d.line([(540, 318), (540, 345), (tx, 345), (tx, YPR)], fill=RED, width=4, joint="curve")
            dot(d, tx, YPR, 12, RED, outline=WHITE)
        card(d, (330, 212, 750, 318), fill=(70, 78, 100), r=20)
        card(d, (350, 224, 730, 306), fill=(220, 240, 225), r=12)
        text(d, (540, 265), reading if reading else "", 60, (20, 60, 30))
        text(d, (770, 265), "vôn kế", 56, INK, anchor="lm")
    measure(d, mx, mk)
    if token is not None and tok_alpha > 0:
        tx = px(token)
        d.ellipse([tx - 72, YPR - 72, tx + 72, YPR + 72], fill=A(ORANGE, tok_alpha), outline=A(WHITE, tok_alpha), width=4)
        text(d, (tx, YPR), "+1 C", 56, WHITE, alpha=tok_alpha)

def table(d, n, y=1040, hl=None):
    card(d, (140, y, 940, y + 500), fill=WHITE, outline=NAVY, w=4)
    xs = (340, 740)
    for x, c in zip(xs, ("x (cm)", "Số chỉ (V)")): text(d, (x, y + 52), c, 56, NAVY)
    d.line([(170, y + 95), (910, y + 95)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 150 + i * 92; x, v, _ = ROWS[i]
        if hl == i: d.rounded_rectangle([160, yy - 40, 920, yy + 40], radius=18, fill=(255, 237, 213))
        text(d, (xs[0], yy), vn(x), 58, INK); text(d, (xs[1], yy), vn(v, 2), 58, BLUE)

def pill(d, s, y, a, color=NAVY, size=58, cx=W / 2):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, y - 40, cx + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (cx, y), s, size, WHITE, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A((148, 140, 128), a), r=18, w=4)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    tray(d, token=2.6)                            # +1 C dung yen gan la am (cong B v1: bo chuyen dong thua luc HS doan)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 170), "Từ lá âm sang lá dương,", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 255), "thế năng của 1 C đổi ra sao?", 60, PURPLE, alpha=a)
    seg_bar(d, y0 + 345, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

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
    pill(d, "tua nhanh", 975, 1.0, ORANGE)
    u = t - M[1] - FF0
    if u < 0:
        tray(d, probe=2.0, reading="1,18 V", mx=2.0, mk=1.0); table(d, 1); return
    j = 1 + max(0, min(2, int(u // FFW))); w = u - (j - 1) * FFW
    x, v, _ = ROWS[j]
    pr = lerp(ROWS[j - 1][0], x, ease(w / 0.45))
    got = w >= 0.45
    rd = vn(v, 2) + " V" if got else vn(ROWS[j - 1][1], 2) + " V"
    tray(d, probe=pr, reading=rd, mx=pr, mk=1.0)
    table(d, j + (1 if got else 0))

# ---------------- canh 3: Dap an + rut ra ----------------
GX0, GX1, GY0, GY1 = 200, 880, 800, 440         # truc: x 0-10 cm, W 0-6 J
def gx(x): return GX0 + x / 10 * (GX1 - GX0)
def gy(w): return GY0 - w / 6 * (GY0 - GY1)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: tăng tỉ lệ x", 290, 1.0)
    card(d, (40, 340, 1040, 950), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 40, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 16, GY0), (GX1 + 40, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 24, GY1 - 30), "W của 1 C (J)", 56, INK, anchor="lm")
    text(d, (GX1 + 40, GY0 - 45), "x (cm)", 56, INK, anchor="rm")
    for x in (2, 4, 6, 8):
        d.line([(gx(x), GY0), (gx(x), GY0 + 12)], fill=NAVY, width=3); text(d, (gx(x), GY0 + 48), str(x), 56, INK, bold=False)
    for w in (2, 4, 6):
        d.line([(GX0 - 12, gy(w)), (GX0, gy(w))], fill=NAVY, width=3); text(d, (GX0 - 22, gy(w)), str(w), 56, INK, bold=False, anchor="rm")
    text(d, (gx(0) + 20, GY0 + 110), "lá âm", 56, BLUE)
    text(d, (gx(10) - 30, GY0 + 110), "lá dương", 56, RED)
    kl = appear(t, 2.6, 0.8)                      # mo hinh W = 0,6 x (J, x tinh bang cm) cho q = 1 C
    if kl > 0:
        x1 = 10 * kl
        d.polygon([(gx(0), gy(0)), (gx(x1), gy(0.6 * x1)), (gx(x1), gy(0))], fill=A(GREEN, 0.22))
        d.line([(gx(0), gy(0)), (gx(x1), gy(0.6 * x1))], fill=A(GREEN, 0.9), width=7)
    for i, (x, v, _) in enumerate(ROWS):
        k = appear(t, 0.2 + 0.15 * i, 0.3)
        if k > 0: dot(d, gx(x), gy(v), 14, A(BLUE, k), outline=WHITE)
    y = 975; kh = appear(t, M[1] + 2.6, 0.5)
    card(d, (140, y, 940, y + 470), fill=WHITE, outline=NAVY, w=4)
    xs = (340, 740)
    text(d, (xs[0], y + 52), "x (cm)", 56, NAVY); text(d, (xs[1], y + 52), "W của 1 C (J)", 56, ORANGE)
    d.line([(170, y + 95), (910, y + 95)], fill=LIGHT, width=4)
    for i, (x, v, r) in enumerate(ROWS):
        yy = y + 150 + i * 88
        if kh > 0: d.rounded_rectangle([160, yy - 38, 920, yy + 38], radius=16, fill=A((255, 237, 213), kh))
        text(d, (xs[0], yy), vn(x), 58, INK); text(d, (xs[1], yy), vn(v, 2), 58, BLUE)
    kn = appear(t, M[1] - 0.1, 0.4)
    if kn > 0:
        card(d, (40, 1465, 1040, 1565), fill=A((236, 253, 243), kn), outline=A(GREEN, kn), r=20, w=3)
        text(d, (W / 2, 1515), "W = qEx, E ≈ 60 V/m", 58, DGREEN, alpha=kn)

# ---------------- canh 4: Bay roi Chua noi duoc (nhip >= 3 s) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = 1.0 - k2
    tray(d, probe=2.0, reading="1,18 V")
    y0 = 1040
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 65, a1, DRED)
        q = "“W = 1,18 J”"
        ks = clamp((t - 0.3) / 0.4); f = F(60); lw = tw(d, q, f); yy = y0 + 185
        text(d, (W / 2, yy), q, 60, DRED, alpha=a1)
        text(d, (W / 2, yy + 80), "không nói mốc", 58, DRED, alpha=a1)
        if ks > 0:                              # gach cheo manh, chu van doc ro
            x0 = W / 2 - lw / 2 - 6; d.line([(x0, yy + 30), (x0 + (lw + 12) * ks, yy + 30 - 64 * ks)], fill=A(DRED, 0.8 * a1), width=4)
        text(d, (W / 2, y0 + 410), "✓ 1,18 J, mốc ở lá âm", 58, DGREEN, alpha=a1 * appear(t, 3.0, 0.4))
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        pill(d, "CHƯA NÓI ĐƯỢC", y0 + 65, k2, NAVY)
        text(d, (W / 2, y0 + 250), "Sát mép lá: chưa đo.", 60, INK, alpha=k2)

# ---------------- canh 5: THU NGHI (cau chot o khung: moc la duong, x = 2 cm -> ~ -4,8 J, khong hien) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.15, 0.4)
    tray(d, token=2.0, la=k, vk=False)
    y0 = 1020
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, "THỬ NGHĨ", y0 + 60, k, ORANGE)
    text(d, (W / 2, y0 + 165), "Đổi mốc sang lá dương.", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 250), "Tại x = 2 cm, W của 1 C?", 62, (176, 64, 8), alpha=k)
    seg_bar(d, y0 + 315, t, 1.0, sc["T"] - 0.2, ORANGE, k)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, y0 + 420, 970, y0 + 525), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, y0 + 472), "Gợi ý: mốc mới ở đâu?", 58, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
           (do["t0"] + 1.7, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW, "tick") for j in range(3)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-the-nang-dien-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Thế năng điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Khay nước muối, hai lá đồng", draw=s_hook, tail=0.3, caps=[
   ("Mốc thế năng chọn ở lá âm.", 3.0),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Que đo cách lá âm 2 cm.", 4.0),
   ("Dời que tới 4, 6, 8 cm.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Với 1 C, số vôn = số jun.", 4.4),
   ("Thế năng tăng đều theo x.", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy thường gặp.", 5.8),
   ("Que chỉ dời giữa hai lá.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng lại, tự tính.", 7.6)]),
])
