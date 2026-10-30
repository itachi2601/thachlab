# Clip: tn-l11-dien-the-01 - Khay nuoc muoi hai la dong: dien the tai mot diem (so von ke) va hieu dien the
#       giua hai diem (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-the-01.json:
#   tham_so: U = 6,0 V ; d = 10 cm ; x 0-10 cm.
#   so_lieu_mau (x cm, V li thuyet, V do, V/x V/m): 2 1,2 1,18 59,0 ; 4 2,4 2,43 60,8 ; 6 3,6 3,57 59,5 ; 8 4,8 4,84 60,5
#   quan_sat: di que do song song la dong -> so chi gan nhu khong doi (ve so chi dung yen 2,43 V o x = 4 cm).
#   hien_tuong_hay_sai[1]: lay U = E.MN khi hai que dat xien -> bay; U = 3,57 - 1,18 ~ 2,4 V (= V li thuyet 3,6 - 1,2).
#   Cau chot: que den o 3 cm, que do o 9 cm (hai vi tri chua tung hien) -> U = 60 V/m . 0,06 m = 3,6 V (khong hien).
# Khac clip thenang1 (cung khay): khay VE DOC (la duong tren, la am duoi, thuoc dung ben trai, von ke ben phai), khong
#   co dien tich +1 C, khong do thi W theo x; Du doan hoi so chi khi di que SONG SONG la dong (dap an C: gan nhu khong
#   doi), bay "hai que xien -> U = E.MN", chot hoi U giua hai que deu khong cham la am.
# Chieu E: tu la duong (tren) xuong la am (duoi); V giam theo chieu duong suc.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (que do 2 cm cham, tua 4-6-8 cm, roi o 4 cm di ngang)
#       -> Dap an C (4 duong dang the co so V, mui ten E, V/x ~ 60 V/m) -> Bay (que xien) roi Chua noi duoc
#       -> Chot + cau hoi tu nho lai.
from engine import *

ROWS = [(2, 1.18), (4, 2.43), (6, 3.57), (8, 4.84)]     # so_lieu_mau: x (cm), V do (V)
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
WATER = (205, 230, 250)
DRED = (185, 28, 28)
EFLD = (120, 140, 175)
COPPER = (184, 115, 51)

# ---------------- khay ve doc (khung nguon 1080x1920) ----------------
TX0, TX1, TY0, TY1 = 170, 770, 330, 880      # khay
LX0, LX1 = 260, 740                          # hai la dong nam ngang
YN, YP = 828, 382                            # la am (duoi), la duong (tren): 10 cm = 446 px
PXC = (YN - YP) / 10.0
def py(x): return YN - x * PXC               # y man hinh cua diem cach la am x cm
PX_COL = 500                                 # cot que do di len

def bez(p0, c, p1, n=24):
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1])
            for u in (i / n for i in range(n + 1))]

def tray(d, red=None, black=None, reading=None, meter=True, field=True, ww=4):
    """Khay doc. red/black = (x_man_hinh, x_cm) cua dau que; black None -> que den cham la am. reading = so chi."""
    card(d, (TX0, TY0, TX1, TY1), fill=WATER, outline=NAVY, r=26, w=5)
    if field:                                # duong suc: tu la duong xuong la am (E huong xuong)
        for xx in (285, 715):
            for yy in range(YP + 30, YN - 50, 34): d.line([(xx, yy), (xx, yy + 17)], fill=EFLD, width=4)
            arrow(d, (xx, YN - 70), (xx, YN - 28), EFLD, w=4, head=16)
        text(d, (735, YP + 60), "E", 40, EFLD, anchor="lm")
    d.rectangle([LX0, YP - 11, LX1, YP + 11], fill=COPPER, outline=NAVY, width=3)
    d.rectangle([LX0, YN - 11, LX1, YN + 11], fill=COPPER, outline=NAVY, width=3)
    text(d, (805, YP), "+", 64, RED); text(d, (805, YN - 4), "−", 64, BLUE)
    # thuoc dung trong khay, sat mep trai; so ghi ngoai khay
    d.rectangle([186, YP, 222, YN], fill=(250, 240, 200), outline=NAVY, width=2)
    for c in range(11):
        y = py(c); d.line([(186, y), (186 + (24 if c % 2 == 0 else 14), y)], fill=NAVY, width=3)
        if c % 2 == 0: text(d, (158, y), str(c), 38, MUTED, bold=False, anchor="rm")
    text(d, (158, YP - 50), "cm", 38, MUTED, bold=False, anchor="rm")
    # nguon 6,0 V phia tren: day toi la duong, day vong trai xuong la am
    d.line([(600, 262), (700, 262), (700, YP - 11)], fill=NAVY, width=4)
    d.line([(400, 262), (70, 262), (70, 910), (500, 910), (500, YN + 11)], fill=NAVY, width=4)
    card(d, (400, 226, 600, 298), fill=WHITE, outline=NAVY, r=16, w=4)
    text(d, (500, 262), "6,0 V", 40, INK)
    if not meter: return
    card(d, (840, 470, 1060, 770), fill=(70, 78, 100), r=20)
    card(d, (856, 500, 1044, 600), fill=(220, 240, 225), r=12)
    text(d, (950, 550), reading if reading else "", 46, (20, 60, 30))
    text(d, (950, 660), "vôn kế", 38, WHITE, bold=False)
    dot(d, 885, 735, 12, (30, 30, 30), outline=WHITE); dot(d, 1015, 735, 12, RED, outline=WHITE)
    bx, by_ = black if black else (690, YN)
    if black: d.line(bez((885, 735), (720, 840), (bx, by_)), fill=(30, 30, 30), width=ww, joint="curve")
    else: d.line([(885, 735), (bx, by_)], fill=(30, 30, 30), width=ww)
    dot(d, bx, by_, 11, (30, 30, 30), outline=WHITE)
    if red is not None:
        rx, ry = red
        d.line([(1015, 735), (rx, ry)], fill=RED, width=ww); dot(d, rx, ry, 12, RED, outline=WHITE)

def marks(d, n, ka=1.0):
    """So chi da doc ghi ngay tren khay, ben trai diem que do (x = 2, 4, 6, 8 cm)."""
    for i in range(n):
        x, v = ROWS[i]
        text(d, (PX_COL - 28, py(x)), vn(v) + " V", 38, (21, 110, 55), anchor="rm", alpha=ka)

def bigread(d, reading, note=None):
    """Man so phong to cua von ke (duoi khay)."""
    card(d, (190, 1000, 890, 1290), fill=(70, 78, 100), r=26)
    card(d, (230, 1040, 850, 1200), fill=(220, 240, 225), r=16)
    text(d, (540, 1120), reading if reading else "", 96, (20, 60, 30))
    text(d, (540, 1245), note if note else "số chỉ vôn kế", 40, WHITE, bold=False)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    tray(d)
    k = appear(t, M[1] - 0.6, 0.5)            # que do o 4 cm + mui ten hai dau chi huong di ngang (khong co so chi)
    if k > 0:
        y = py(4)
        for xx in range(330, 680, 30): d.line([(xx, y - 46), (xx + 15, y - 46)], fill=A(ORANGE, k), width=4)
        arrow(d, (360, y - 46), (318, y - 46), A(ORANGE, k), w=4, head=16)
        arrow(d, (640, y - 46), (682, y - 46), A(ORANGE, k), w=4, head=16)
        d.line([(1015, 735), (PX_COL, y)], fill=A(RED, k), width=4); dot(d, PX_COL, y, 12, A(RED, k), outline=WHITE)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 270, "Dời que đỏ song song\nvới lá đồng, số chỉ\nvôn kế thay đổi thế nào?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 512], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 512], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
FF0, FFW = 0.2, 1.0          # tua nhanh 4-6-8 cm
SL0 = FF0 + 3 * FFW + 0.2    # bat dau di ngang o 4 cm (tinh tu M[1])

def xbar(d, x, ka=1.0):      # thuoc do x tu la am toi que do (ben phai cot que)
    xx = PX_COL + 70
    d.line([(xx, YN), (xx, py(x))], fill=A(ORANGE, ka), width=5)
    d.line([(xx - 14, py(x)), (xx + 14, py(x))], fill=A(ORANGE, ka), width=5)
    text(d, (xx + 22, (YN + py(x)) / 2), "x", 44, ORANGE, anchor="lm", alpha=ka)

def s_do(img, d, t, sc):
    M = sc["M"]
    if t < M[1]:                              # que do toi x = 2 cm, lam cham
        if t < 0.4: tray(d); bigread(d, ""); return
        x = lerp(0.5, 2.0, ease((t - 0.4) / 1.1))
        rd = "1,18 V" if t >= 1.7 else ""
        tray(d, red=(PX_COL, py(x)), reading=rd)
        if t >= 1.6: xbar(d, 2.0, appear(t, 1.6, 0.4))
        if t >= 1.9: marks(d, 1, appear(t, 1.9, 0.3))
        bigread(d, rd, "que đỏ: x = 2 cm" if t >= 1.7 else None)
        return
    u = t - M[1]
    if u < SL0:                               # 4, 6, 8 cm: so chi chi hien khi que da dung o diem do
        card(d, (60, 928, 300, 988), fill=ORANGE, r=30); text(d, (180, 958), "tua nhanh", 38, WHITE)
        v = u - FF0
        if v < 0:
            tray(d, red=(PX_COL, py(2)), reading="1,18 V"); marks(d, 1); bigread(d, "1,18 V", "que đỏ: x = 2 cm"); return
        j = 1 + max(0, min(2, int(v // FFW))); w = v - (j - 1) * FFW
        x, val = ROWS[j]
        if v >= 3 * FFW:                      # tro lai 4 cm truoc khi di ngang (dang chay: an so)
            tray(d, red=(PX_COL, py(lerp(8.0, 4.0, ease((v - 3 * FFW) / 0.2))))); marks(d, 4); bigread(d, ""); return
        xp = lerp(ROWS[j - 1][0], x, ease(w / 0.45))
        st = w >= 0.5                         # que da dung han o x
        rd = vn(val) + " V" if st else ""
        tray(d, red=(PX_COL, py(xp)), reading=rd)
        marks(d, j + (1 if st else 0))
        bigread(d, rd, f"que đỏ: x = {x} cm" if st else None)
        return
    # o 4 cm, di que do sang ngang (ve phia phai, tranh cot so): so chi dung yen
    s = u - SL0
    xs = PX_COL + 190 * math.sin(math.pi * s / 2.4) if s < 2.4 else PX_COL
    d.line([(PX_COL - 10, py(4)), (LX1 - 20, py(4))], fill=A(ORANGE, 0.55), width=3)   # bat dau sau nhan 2,43 V
    ya = py(4) - 46                           # mui ten hai dau: huong que truot
    for xx in range(530, 680, 30): d.line([(xx, ya), (xx + 15, ya)], fill=ORANGE, width=4)
    arrow(d, (540, ya), (505, ya), ORANGE, w=4, head=16); arrow(d, (670, ya), (705, ya), ORANGE, w=4, head=16)
    tray(d, red=(xs, py(4)), reading="2,43 V")
    marks(d, 4)
    bigread(d, "2,43 V", "dời ngang ở x = 4 cm")

# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · gần như không đổi"
    pw = tw(d, lab, F(42)) + 56
    tray(d, meter=False, field=t >= M[1] - 0.1)
    card(d, (W / 2 - pw / 2, 928, W / 2 + pw / 2, 992), fill=A(NAVY, ka), r=32)   # duoi khay + day nguon (y 910)
    text(d, (W / 2, 960), lab, 42, WHITE, alpha=ka)
    text(d, (870, YP), "6,0 V", 40, RED, anchor="lm", alpha=ka)
    text(d, (870, YN), "0 V", 40, BLUE, anchor="lm", alpha=ka)
    for i, (x, v) in enumerate(ROWS):         # 4 duong dang the, moi duong mot so V
        k = appear(t, M[0] + 0.3 + 0.3 * i, 0.35)
        if k <= 0: continue
        y = py(x)
        for xx in range(LX0 + 10, LX1 - 10, 30): d.line([(xx, y), (xx + 16, y)], fill=A(GREEN, k), width=5)
        text(d, (870, y), vn(v) + " V", 40, (21, 110, 55), anchor="lm", alpha=k)
    kE = appear(t, M[1] - 0.1, 0.45)          # mui ten E lon: V giam theo chieu duong suc
    if kE > 0:
        arrow(d, (1045, YP + 40), (1045, YN - 40), A(PURPLE, kE), w=8, head=28)
        text(d, (1045, YP - 34), "E", 44, PURPLE, alpha=kE)
    kn = appear(t, M[1] + 0.6, 0.4)
    if kn > 0:
        card(d, (40, 1030, 1040, 1150), fill=A((236, 253, 243), kn), outline=A(GREEN, kn), r=20, w=3)
        text(d, (W / 2, 1090), "V/x ≈ 60 V/m = U/d", 48, (21, 110, 55), alpha=kn)

# ---------------- canh 4: Bay roi Chua noi duoc (khong hien cung luc) ----------------
MX, NX = 560, 420                            # giua khay: M o x = 2 cm (ben phai), N o x = 6 cm (lech trai)
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k2)
    mxy, nxy = (MX, py(2)), (NX, py(6))
    tray(d, red=nxy, black=mxy, reading="", field=True, ww=3)
    for i in range(0, 12, 2):                # canh MN: net dut xam dam (khac day que do)
        p0 = (lerp(MX, NX, i / 12), lerp(py(2), py(6), i / 12)); p1 = (lerp(MX, NX, (i + 1) / 12), lerp(py(2), py(6), (i + 1) / 12))
        d.line([p0, p1], fill=(70, 75, 95), width=6)
    kt = appear(t, 1.2, 0.4)
    if kt > 0:                               # tam giac: chi canh doc duong suc (4 cm) moi tinh
        for xx in range(NX + 20, MX, 28): d.line([(xx, py(2)), (xx + 14, py(2))], fill=A(ORANGE, kt), width=4)
        d.line([(NX, py(2)), (NX, py(6))], fill=A(ORANGE, kt), width=6)
        text(d, (NX - 8, (py(2) + py(6)) / 2), "4 cm", 38, ORANGE, anchor="rm", alpha=kt)
    text(d, (MX - 42, py(2) + 30), "M", 40, INK); text(d, (NX, py(6) - 45), "N", 40, INK)
    if a1 > 0:
        y0 = 1010
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“U = E · MN”"
        ks = clamp((t - 1.2) / 0.4); f = F(50); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2, yy), q, 50, DRED, alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A((140, 15, 15), a1), width=7)
        kc = a1 * appear(t, 1.7, 0.5)
        ctext(d, y0 + 340, "✓ Chỉ tính 4 cm dọc đường sức", 46, (21, 110, 55), maxw=920, alpha=kc)
        ctext(d, y0 + 450, "U = 3,57 − 1,18 ≈ 2,4 V", 46, INK, maxw=920, alpha=kc)
    if k2 > 0:
        y0 = 1010 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Sát mép lá: đường sức cong", "• Muối không đều: chưa thử")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 220 + j * 140), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: que den 3 cm, que do 9 cm, von ke chi bao nhieu; goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 390, "Số chỉ = hiệu điện thế giữa hai que", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1170), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 674), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 642), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.9, 0.5)
    ctext(d, 780, "Que đen ở 3 cm, que đỏ ở 9 cm.\nVôn kế chỉ khoảng bao nhiêu?", 48, INK, maxw=920, alpha=kq)
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (110, 900, 970, 1140), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 950, "Gợi ý", 38, INK, alpha=kh)
    ctext(d, 1060, "E ≈ 60 V/m;\nđổi cm ra m", 44, ORANGE, maxw=820, alpha=kh)
    # hinh: hai la + thuoc 0-10 cm + hai que tren cung mot duong suc (khong ghi so von); cach the >= 40 px, day cach phu de >= 60 px
    yp, yn = 1250, 1580; pc = (yn - yp) / 10
    if kq > 0:
        for yy in (yp, yn): d.rectangle([330, yy - 8, 750, yy + 8], fill=A(COPPER, kq), outline=A(NAVY, kq), width=2)
        text(d, (785, yp), "+", 52, RED, alpha=kq); text(d, (785, yn - 4), "−", 52, BLUE, alpha=kq)
        d.rectangle([270, yp, 300, yn], fill=A((250, 240, 200), kq), outline=A(NAVY, kq), width=2)
        for c in range(11):
            y = yn - c * pc; d.line([(270, y), (270 + (20 if c % 5 == 0 else 11), y)], fill=A(NAVY, kq), width=3)
        text(d, (255, yn), "0", 38, MUTED, bold=False, anchor="rm", alpha=kq)
        text(d, (255, yp), "10", 38, MUTED, bold=False, anchor="rm", alpha=kq)
        for xc, col, lab in ((3, (30, 30, 30), "3 cm"), (9, RED, "9 cm")):
            y = yn - xc * pc
            d.line([(316, y), (520, y)], fill=A(GRAY, kq), width=2)
            dot(d, 540, y, 15, A(col, kq), outline=WHITE)
            text(d, (572, y), lab, 40, col, anchor="lm", alpha=kq)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.3, "ding"),
           (do["t0"] + 1.7, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW, "tick") for j in range(3)]
    out += [(do["t0"] + M[1] + SL0, "tap")]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out

CLIP = dict(id="tn-l11-dien-the-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện thế · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Vôn kế trong khay nước muối", draw=s_hook, tail=0.8, caps=[
   ("Que đen chạm lá âm: mốc 0 V.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Que đỏ cách lá âm 2 cm.", 3.6),
   ("Thêm 4, 6, 8 cm, rồi dời ngang.", 6.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Song song lá đồng: cùng điện thế.", 3.6),
   ("V giảm theo chiều đường sức.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: hai que đặt xiên, lệch đường sức.", 4.4),
   ("Mới đo một khay nước muối.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
