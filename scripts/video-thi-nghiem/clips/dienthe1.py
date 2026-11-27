# Clip: tn-l11-dien-the-01 - Khay nuoc muoi hai la dong: dien the tai mot diem (so von ke) va hieu dien the
#       giua hai diem (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-the-01.json:
#   tham_so: U = 6,0 V ; d = 10 cm ; x 0-10 cm.
#   so_lieu_mau (x cm, V li thuyet, V do, V/x V/m): 2 1,2 1,18 59,0 ; 4 2,4 2,43 60,8 ; 6 3,6 3,57 59,5 ; 8 4,8 4,84 60,5
#   quan_sat: di que do song song la dong -> so chi gan nhu khong doi (ve so chi dung yen 2,43 V o x = 4 cm).
#   hien_tuong_hay_sai[1]: lay U = E.MN khi hai que dat xien -> bay; U = 3,57 - 1,18 ~ 2,4 V (= V li thuyet 3,6 - 1,2).
#   Cau chot (27/11/2026, o khung, khong hien): que den cham LA DUONG, que do o x = 9 cm -> U = V_do - V_den = 5,4 - 6,0 = -0,6 V.
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
DGREEN = (21, 110, 55)
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

def tray(d, red=None, black=None, reading=None, meter=True, field=True, ww=4, lbl=True):
    """Khay doc. red/black = toa do man hinh dau que; black None -> que den cham la am. reading = so chi."""
    card(d, (TX0, TY0, TX1, TY1), fill=WATER, outline=NAVY, r=26, w=5)
    if field:                                # duong suc: tu la duong xuong la am (E huong xuong)
        for xx in (285, 715):
            for yy in range(YP + 30, YN - 50, 34): d.line([(xx, yy), (xx, yy + 17)], fill=EFLD, width=4)
            arrow(d, (xx, YN - 70), (xx, YN - 28), EFLD, w=4, head=16)
        text(d, (690, YP + 62), "E", 56, EFLD, anchor="rm")
    d.rectangle([LX0, YP - 11, LX1, YP + 11], fill=COPPER, outline=NAVY, width=3)
    d.rectangle([LX0, YN - 11, LX1, YN + 11], fill=COPPER, outline=NAVY, width=3)
    text(d, (805, YP), "+", 64, RED); text(d, (805, YN - 4), "−", 64, BLUE)
    # thuoc dung trong khay, sat mep trai; so ghi ngoai khay
    d.rectangle([186, YP, 222, YN], fill=(250, 240, 200), outline=NAVY, width=2)
    for c in range(11):
        y = py(c); d.line([(186, y), (186 + (24 if c % 2 == 0 else 14), y)], fill=NAVY, width=3)
        if c % 2 == 0: text(d, (156, y), str(c), 56, MUTED, bold=False, anchor="rm")
    text(d, (100, YP - 62), "cm", 56, MUTED, bold=False)
    # nguon 6,0 V phia tren: day toi la duong, day vong trai xuong la am
    d.line([(610, 262), (700, 262), (700, YP - 11)], fill=NAVY, width=4)
    d.line([(390, 262), (70, 262), (70, 910), (500, 910), (500, YN + 11)], fill=NAVY, width=4)
    card(d, (390, 222, 610, 302), fill=WHITE, outline=NAVY, r=16, w=4)
    text(d, (500, 262), "6,0 V", 56, INK)
    if not meter: return
    card(d, (830, 460, 1060, 780), fill=(70, 78, 100), r=20)
    card(d, (846, 490, 1044, 600), fill=(220, 240, 225), r=12)
    text(d, (945, 545), reading if reading else "", 56, (20, 60, 30))
    if lbl: text(d, (945, 660), "vôn kế", 56, WHITE, bold=False)
    dot(d, 885, 745, 12, (30, 30, 30), outline=WHITE); dot(d, 1015, 745, 12, RED, outline=WHITE)
    bx, by_ = black if black else (690, YN)
    if black: d.line(bez((885, 745), (720, 840), (bx, by_)), fill=(30, 30, 30), width=ww, joint="curve")
    else: d.line([(885, 745), (bx, by_)], fill=(30, 30, 30), width=ww)
    dot(d, bx, by_, 11, (30, 30, 30), outline=WHITE)
    if red is not None:
        rx, ry = red
        d.line([(1015, 745), (rx, ry)], fill=RED, width=ww); dot(d, rx, ry, 12, RED, outline=WHITE)

def marks(d, n, ka=1.0):
    """So chi da doc ghi ngay tren khay, ben trai diem que do (x = 2, 4, 6, 8 cm)."""
    for i in range(n):
        x, v = ROWS[i]
        text(d, (PX_COL - 28, py(x)), vn(v) + " V", 56, DGREEN, anchor="rm", alpha=ka)

def bigread(d, reading, note=None):
    """Man so phong to cua von ke (duoi khay)."""
    card(d, (190, 1000, 890, 1300), fill=(70, 78, 100), r=26)
    card(d, (230, 1035, 850, 1195), fill=(220, 240, 225), r=16)
    text(d, (540, 1115), reading if reading else "", 96, (20, 60, 30))
    if note: text(d, (540, 1250), note, 56, WHITE, bold=False)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    tray(d)
    k = appear(t, M[1] - 0.6, 0.5)            # que do o 4 cm + mui ten hai dau chi huong di ngang (khong co so chi)
    if k > 0:
        y = py(4)
        for xx in range(330, 680, 30): d.line([(xx, y - 46), (xx + 15, y - 46)], fill=A(ORANGE, k), width=4)
        arrow(d, (360, y - 46), (318, y - 46), A(ORANGE, k), w=4, head=16)
        arrow(d, (640, y - 46), (682, y - 46), A(ORANGE, k), w=4, head=16)
        d.line([(1015, 745), (PX_COL, y)], fill=A(RED, k), width=4); dot(d, PX_COL, y, 12, A(RED, k), outline=WHITE)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 70, a, PURPLE)
    text(d, (W / 2, y0 + 180), "Dời que đỏ song song lá đồng,", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "số chỉ vôn kế đổi ra sao?", 60, INK, alpha=a)
    seg_bar(d, y0 + 345, t, M[1] + 0.6, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
FF0, FFW = 0.2, 1.0          # tua nhanh 4-6-8 cm
SL0 = FF0 + 3 * FFW + 0.2    # bat dau di ngang o 4 cm (tinh tu M[1])

def xbar(d, x, ka=1.0):      # thuoc do x tu la am toi que do (ben phai cot que)
    xx = PX_COL + 70
    d.line([(xx, YN), (xx, py(x))], fill=A(ORANGE, ka), width=5)
    d.line([(xx - 14, py(x)), (xx + 14, py(x))], fill=A(ORANGE, ka), width=5)
    text(d, (xx + 22, (YN + py(x)) / 2), "x", 56, ORANGE, anchor="lm", alpha=ka)

def s_do(img, d, t, sc):
    M = sc["M"]
    if t < M[1]:                              # que do toi x = 2 cm, lam cham
        if t < 0.4: tray(d); bigread(d, ""); return
        x = lerp(0.5, 2.0, ease((t - 0.4) / 1.1))
        rd = "1,18 V" if t >= 2.1 else ""
        tray(d, red=(PX_COL, py(x)), reading=rd)
        if t >= 1.6: xbar(d, 2.0, appear(t, 1.6, 0.4))
        if t >= 2.1: marks(d, 1)
        bigread(d, rd, "que đỏ: x = 2 cm" if t >= 2.1 else None)
        return
    u = t - M[1]
    if u < SL0:                               # 4, 6, 8 cm: so chi chi hien khi que da dung o diem do
        pill(d, "tua nhanh", 955, 1.0, ORANGE, size=56, cx=250)
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
    d.line([(PX_COL - 10, py(4)), (LX1 - 20, py(4))], fill=A(ORANGE, 0.55), width=3)
    ya = py(4) - 46                           # mui ten hai dau: huong que truot
    for xx in range(530, 680, 30): d.line([(xx, ya), (xx + 15, ya)], fill=ORANGE, width=4)
    arrow(d, (540, ya), (505, ya), ORANGE, w=4, head=16); arrow(d, (670, ya), (705, ya), ORANGE, w=4, head=16)
    tray(d, red=(xs, py(4)), reading="2,43 V")
    marks(d, 4)
    bigread(d, "2,43 V", "dời ngang, vẫn x = 4 cm")

# ---------------- canh 3: Dap an + rut ra ----------------
def eqline(d, x, v, k):
    y = py(x)
    for xx in range(LX0 + 10, LX1 - 10, 30): d.line([(xx, y), (xx + 16, y)], fill=A(GREEN, k), width=6)
    text(d, (860, y), vn(v) + " V", 56, DGREEN, anchor="lm", alpha=k)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.4)
    tray(d, meter=False)
    pill(d, "ĐÁP ÁN: gần như không đổi", 975, ka, NAVY)
    eqline(d, 4, 2.43, ka)                    # nhip 1: duong vua doi ngang
    k2 = appear(t, 2.6, 0.4)                  # nhip 2: ba duong con lai + dien the hai la
    if k2 > 0:
        for x, v in (ROWS[0], ROWS[2], ROWS[3]): eqline(d, x, v, k2)
        text(d, (860, YP - 50), "6,0 V", 56, RED, anchor="lm", alpha=k2)
        text(d, (860, YN + 50), "0 V", 56, BLUE, anchor="lm", alpha=k2)
    kn = appear(t, M[1] - 0.1, 0.4)           # nhip 3: the V/x
    if kn > 0:
        card(d, (40, 1060, 1040, 1180), fill=A((236, 253, 243), kn), outline=A(GREEN, kn), r=20, w=4)
        text(d, (W / 2, 1120), "V/x ≈ 60 V/m = U/d", 60, DGREEN, alpha=kn)
    kE = appear(t, M[1] + 2.4, 0.5)           # nhip 4 (hinh): mui ten E dam, V giam theo chieu duong suc
    if kE > 0:
        d.rectangle([690, YP + 14, 740, YN - 14], fill=A(PURPLE, 0.25 * kE))
        arrow(d, (715, YP + 30), (715, YN - 30), A(PURPLE, kE), w=10, head=30)

# ---------------- canh 4: Bay roi Chua noi duoc (nhip 0 / 3,0 / M1-0,1) ----------------
MX, NX = 560, 420                            # M o x = 2 cm (ben phai), N o x = 6 cm (lech trai)
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = 1.0 - k2
    kt = appear(t, 3.0, 0.4)
    mxy, nxy = (MX, py(2)), (NX, py(6))
    tray(d, red=nxy, black=mxy, reading="2,39 V" if t >= 3.0 else "", field=True, ww=3)
    for i in range(0, 12, 2):                # canh MN: net dut xam dam (khac day que do)
        p0 = (lerp(MX, NX, i / 12), lerp(py(2), py(6), i / 12)); p1 = (lerp(MX, NX, (i + 1) / 12), lerp(py(2), py(6), (i + 1) / 12))
        d.line([p0, p1], fill=(70, 75, 95), width=6)
    if kt > 0:                               # tam giac: chi canh doc duong suc (4 cm) moi tinh
        d.polygon([(NX, py(2)), (MX, py(2)), (NX, py(6))], fill=A(ORANGE, 0.22 * kt))
        for xx in range(NX + 20, MX, 28): d.line([(xx, py(2)), (xx + 14, py(2))], fill=A(ORANGE, kt), width=4)
        d.line([(NX, py(2)), (NX, py(6))], fill=A(ORANGE, kt), width=7)
        text(d, (NX - 14, (py(2) + py(6)) / 2), "4 cm", 56, ORANGE, anchor="rm", alpha=kt)
    text(d, (MX + 40, py(2) + 40), "M", 56, INK); text(d, (NX + 10, py(6) - 50), "N", 56, INK)
    y0 = 1010
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 65, a1, DRED)
        q = "“U = E · MN”"
        ks = clamp((t - 0.3) / 0.4); f = F(60); lw = tw(d, q, f); yy = y0 + 210
        text(d, (W / 2, yy), q, 60, mix(DRED, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=6)
        text(d, (W / 2, y0 + 400), "✓ Chỉ tính 4 cm dọc E", 56, DGREEN, alpha=a1 * kt)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        pill(d, "CHƯA NÓI ĐƯỢC", y0 + 65, k2, NAVY)
        text(d, (W / 2, y0 + 250), "Sát mép: đường sức cong.", 60, INK, alpha=k2)

# ---------------- canh 5: THU NGHI (cau chot o khung: que den o la duong, que do x = 9 cm -> -0,6 V, khong hien) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.15, 0.4)
    tray(d, red=(PX_COL, py(9)), black=(620, YP), reading="? V", field=False, ww=3, lbl=False)
    y9 = py(9)
    d.line([(222, y9), (PX_COL - 20, y9)], fill=A(ORANGE, k), width=4)
    y0 = 1010
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, "THỬ NGHĨ", y0 + 60, k, ORANGE)
    text(d, (W / 2, y0 + 160), "Que đen chạm lá dương,", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 240), "que đỏ ở x = 9 cm.", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 320), "Vôn kế chỉ bao nhiêu?", 62, (176, 64, 8), alpha=k)
    seg_bar(d, y0 + 380, t, 1.0, sc["T"] - 0.2, ORANGE, k)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (60, y0 + 470, 1020, y0 + 565), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, y0 + 517), "Gợi ý: điện thế từng que?", 56, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
           (do["t0"] + 2.1, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW, "tick") for j in range(3)]
    out += [(do["t0"] + M[1] + SL0, "tap")]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-dien-the-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện thế · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Vôn kế trong khay nước muối", draw=s_hook, tail=0.4, caps=[
   ("Que đen ở lá âm: mốc 0 V.", 3.0),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Que đỏ cách lá âm 2 cm.", 4.0),
   ("Thêm 4, 6, 8 cm, rồi dời ngang.", 6.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Song song lá đồng: cùng điện thế.", 4.4),
   ("V giảm theo chiều đường sức.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy: hai que đặt xiên.", 5.8),
   ("Mới đo một khay nước muối.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng lại, tự tính.", 7.6)]),
])
