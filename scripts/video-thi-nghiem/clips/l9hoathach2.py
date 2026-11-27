# Clip: tn-l9-hoathach-02 - Dot nen parafin dun 200 g nuoc (KHTN 9 Bai 16, lesson 94; 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-hoathach-02.json:
#   so_lieu_mau (t phut, nen chay g, nuoc °C): 0 0,00 28,0 ; 2 0,24 30,6 ; 4 0,48 33,0 ; 6 0,72 35,4 ; 8 0,96 37,6
#   tham_so: m_nuoc = 200 g, q = 42 000 J/g (xap xi); mo_hinh: c = 4,18 J/(g.K), T = 28 + 50(1 - e^(-K t/50)), K = 1,33.
#   Tinh lai (assert trong _kiem_so): Q nen = 0,96 . 42 000 = 40 320 J ~ 40 kJ ; Q nuoc = 200 . 4,18 . 9,6 = 8 026 J ~ 8 kJ
#   -> ~ 20 % (khoang 1/5). Cau chot 27/11: cung nen, 400 g nuoc, 8 phut -> mo hinh kho (K = 0,663) tang 5,03 ~ 5 °C (KHONG hien dap so).
#   quan_sat: coc kho mo hoi nuoc, nuoc voi trong van duc. hien_tuong_hay_sai[0] = cau Du doan, [1] = bay.
#   an_toan: buoc toc, nen tren khay kim loai, xa giay; lon nong.
# Cau 3 cua bai (che gio, giu lon cach lua co dinh, lam lap 3 lan) -> clip KHONG noi gio, khoang cach, do lap, sai so.
# Thu thach *** (kg CO2 khi dot than) -> clip khong tinh khoi luong CO2. Clip khong noi "nuoc cang nong cang mat nhiet".
import math
from engine import *

ROWS = [(0, 0.00, 28.0), (2, 0.24, 30.6), (4, 0.48, 33.0), (6, 0.72, 35.4), (8, 0.96, 37.6)]   # so_lieu_mau
M_NUOC, C_NUOC, Q_PARAFIN, T0 = 200, 4.18, 42000.0, 28.0
DM, DT = ROWS[-1][1], round(ROWS[-1][2] - ROWS[0][2], 1)            # 0,96 g ; 9,6 °C
Q_NEN = DM * Q_PARAFIN                                               # 40 320 J
Q_NUOC = M_NUOC * C_NUOC * DT                                        # 8 025,6 J
TI_LE = Q_NUOC / Q_NEN                                               # 0,199
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

CAN = (203, 210, 222); CAN_D = (120, 130, 150); WAX = (254, 249, 231); TRAY = (160, 168, 184)
FLAME_O = (249, 115, 22); FLAME_I = (253, 224, 71); LIQ = (220, 38, 38); DGREEN = (21, 110, 55); DRED = (185, 28, 28)
LIME = (241, 245, 249); MILK = (226, 232, 240)

# ---------------- dung cu ----------------
TRAY_Y, CAN_X0, CAN_X1, CAN_Y0, CAN_Y1 = 900, 250, 520, 420, 640
CDX = 385                       # truc nen
H0, H8 = 190, 168               # chieu cao nen luc dau / sau 8 phut (ve minh hoa, khong do)
def flame(d, x, ytop, t, alpha=1.0, s=1.0):
    h = (78 + 8 * math.sin(9 * t) + 4 * math.sin(23 * t)) * s
    for col, w, hh in ((FLAME_O, 22 * s, h), (FLAME_I, 11 * s, h * 0.6)):
        d.polygon([(x - w, ytop - w * 0.9), (x, ytop - hh), (x + w, ytop - w * 0.9)], fill=A(col, alpha))
        d.ellipse([x - w, ytop - 2 * w, x + w, ytop], fill=A(col, alpha))

def rig(d, t, k, temp, lit=True):
    """k: 0..1 phan nen da chay (theo bang); temp: so nhiet ke."""
    card(d, (40, 262, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 940), (1020, 940)], fill=(180, 170, 150), width=4)
    d.rounded_rectangle([140, TRAY_Y, 630, TRAY_Y + 30], radius=8, fill=TRAY, outline=NAVY, width=3)   # khay kim loai
    for x in (CAN_X0 - 40, CAN_X1 + 40):                                                                  # gia do
        d.line([(x, CAN_Y1 + 10), (x, TRAY_Y)], fill=NAVY, width=8)
    d.line([(CAN_X0 - 50, CAN_Y1 + 10), (CAN_X1 + 50, CAN_Y1 + 10)], fill=NAVY, width=8)
    d.rounded_rectangle([CAN_X0, CAN_Y0, CAN_X1, CAN_Y1], radius=14, fill=CAN, outline=CAN_D, width=4)       # lon nhom
    for yy in (CAN_Y0 + 30, CAN_Y1 - 30): d.line([(CAN_X0 + 6, yy), (CAN_X1 - 6, yy)], fill=CAN_D, width=3)
    h = H0 - (H0 - H8) * k; top = TRAY_Y - h
    d.rectangle([CDX - 26, top, CDX + 26, TRAY_Y], fill=WAX, outline=NAVY, width=3)                      # nen
    d.line([(CDX, top), (CDX, top - 14)], fill=NAVY, width=4)
    if lit: flame(d, CDX, top - 10, t)
    # nhiet ke cam vao nuoc trong lon
    tx = 470
    d.rounded_rectangle([tx - 12, 300, tx + 12, 600], radius=12, fill=(241, 245, 249), outline=NAVY, width=3)
    yl = 590 - 260 * clamp((temp - 20) / 25)
    d.rectangle([tx - 4, yl, tx + 4, 590], fill=LIQ); d.ellipse([tx - 16, 576, tx + 16, 608], fill=LIQ, outline=NAVY, width=3)

def readouts(d, temp, burnt, tmin, alpha=1.0):
    for y0, lab, val, col in ((290, "nước", vn(temp) + " °C", (153, 27, 27)), (510, "nến", vn(burnt, 2) + " g", NAVY)):
        card(d, (660, y0, 1020, y0 + 200), fill=A((70, 78, 100), alpha), r=22)
        text(d, (840, y0 + 48), lab, 56, WHITE, alpha=alpha)
        card(d, (685, y0 + 95, 995, y0 + 180), fill=A((220, 240, 225), alpha), r=12)
        text(d, (840, y0 + 138), val, 58, col, alpha=alpha)
    if tmin is not None: text(d, (840, 790), f"phút {tmin}", 58, ORANGE, alpha=alpha)

def pill(d, s, y, a, color=NAVY, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def stripes(d, x0, y0, x1, y1, t, col, speed=260):
    """soc cheo chay trong khung (chuyen dong vung giua cho cong A)."""
    off = (t * speed) % 120
    for x in range(int(x0 - 200 + off), int(x1), 120):
        a0, a1 = max(x, x0 + 10), min(x + 50, x1 - 10)
        b0, b1 = min(max(x + 120, x0 + 10), x1 - 10), min(max(x + 170, x0 + 10), x1 - 10)
        if a1 > a0 or b1 > b0: d.polygon([(a0, y1 - 10), (a1, y1 - 10), (b1, y0 + 10), (b0, y0 + 10)], fill=col)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.3
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, 0.0, ROWS[0][2], lit=t > 0.6)
    text(d, (580, TRAY_Y - 120), "nến parafin", 56, INK, anchor="lm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 160), "Nhiệt nến toả ra,", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 240), "bao nhiêu phần vào nước?", 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 320, 970, y0 + 420], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 320, 110 + max(90, 860 * (1 - p)), y0 + 420], radius=45, fill=A((76, 29, 149), a))

# ---------------- canh 2: Tien hanh (moi 2 phut mot lan doc, tua nhanh) ----------------
T_S = (0.6, 1.9, 3.2, 4.5, 5.8)     # luc doc phut 0, 2, 4, 6, 8
T_ROW = 0.4
def do_state(t):
    k = max(0, sum(1 for ts in T_S if t >= ts - 1e-9) - 1)
    n = sum(1 for ts in T_S if t >= ts + T_ROW - 1e-9)
    return k, n

XS = (200, 540, 870)
def table(d, n, y=1065, hl=None, alpha=1.0):
    card(d, (40, y, 1040, y + 575), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, h in zip(XS, ("phút", "nến (g)", "nước (°C)")): text(d, (x, y + 52), h, 56, INK, alpha=alpha)
    d.line([(70, y + 100), (1010, y + 100)], fill=A(LIGHT, alpha), width=3)
    for j, (tm, m, T) in enumerate(ROWS):
        yy = y + 148 + j * 90
        if hl == j: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=20, fill=A((255, 237, 213), alpha))
        if j < n:
            text(d, (XS[0], yy), str(tm), 56, NAVY, alpha=alpha)
            text(d, (XS[1], yy), vn(m, 2), 56, NAVY, alpha=alpha)
            text(d, (XS[2], yy), vn(T), 56, (153, 27, 27), alpha=alpha)

def s_do(img, d, t, sc):
    k, n = do_state(t)
    tm, m, T = ROWS[k]
    rig(d, t, m / DM, T); readouts(d, T, m, tm)
    table(d, n, hl=(n - 1 if n > 0 else None))
    card(d, (40, 968, 1040, 1052), fill=(255, 247, 237), outline=ORANGE, r=24, w=3)   # an toan (kho)
    text(d, (W / 2, 1010), "An toàn: buộc tóc, nến trên khay", 56, (154, 52, 18))

# ---------------- canh 3: Dap an (hai thanh nhiet, KHONG cong thuc: THCS chua hoc nhiet dung rieng) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN: khoảng 1/5", 320, ka)
    x0, x1 = 80, 1000
    card(d, (40, 380, 1040, 1010), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    text(d, (x0, 440), "nến toả", 56, ORANGE, anchor="lm", alpha=ka)
    g1 = clamp((t - 0.3) / 1.2)
    if g1 > 0: d.rounded_rectangle([x0, 480, x0 + (x1 - x0) * g1, 580], radius=14, fill=A(ORANGE, ka))
    text(d, (W / 2, 530), f"≈ {round(Q_NEN / 1000)} kJ", 58, WHITE, alpha=ka)
    text(d, (W / 2, 630), f"{vn(DM, 2)} g × 42 kJ/g", 56, MUTED, alpha=ka)          # phep tinh (kiem-v1 muc 2)
    text(d, (x0, 730), "nước nhận", 56, BLUE, anchor="lm", alpha=ka)
    g2 = clamp((t - 0.6) / 1.2)
    xs = x0 + (x1 - x0) * TI_LE
    if g2 > 0: d.rounded_rectangle([x0, 770, x0 + (xs - x0) * g2, 870], radius=14, fill=A(BLUE, ka))
    text(d, (xs + 30, 820), f"≈ {round(Q_NUOC / 1000)} kJ", 58, BLUE, anchor="lm", alpha=ka)
    text(d, (W / 2, 935), f"{M_NUOC} g × 4,18 × {vn(DT)} °C", 56, MUTED, alpha=ka)
    kb = appear(t, M[1] + 0.3, 0.5)          # thanh chia: phan vao nuoc / phan ra ngoai (soc chay = thoat ra)
    if kb > 0:
        y0, y1 = 1080, 1260
        card(d, (40, y0 - 30, 1040, y1 + 30), fill=A(WHITE, kb), outline=A(NAVY, kb), w=4)
        d.rectangle([x0, y0, xs, y1], fill=A(BLUE, kb))
        d.rectangle([xs, y0, x1, y1], fill=A((203, 213, 225), kb))
        stripes(d, xs, y0, x1, y1, t, A((148, 163, 184), kb))
        d.rectangle([x0, y0, x1, y1], outline=A(NAVY, kb), width=4)
        tw_ = tw(d, f"≈ {round((Q_NEN - Q_NUOC) / 1000)} kJ ra ngoài", F(58)) + 40
        cx = (xs + x1) / 2
        card(d, (cx - tw_ / 2, (y0 + y1) / 2 - 45, cx + tw_ / 2, (y0 + y1) / 2 + 45), fill=A(WHITE, kb), r=20)
        text(d, (cx, (y0 + y1) / 2), f"≈ {round((Q_NEN - Q_NUOC) / 1000)} kJ ra ngoài", 58, NAVY, alpha=kb)

# ---------------- canh 4: Rut ra (chuoi chuyen hoa) ----------------
def box(d, y, s, col, k, fill=WHITE):
    card(d, (100, y - 70, 980, y + 70), fill=A(fill, k), outline=A(col, k), w=5)
    text(d, (W / 2, y), s, 58, col, alpha=k)
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k = appear(t, 0.3, 0.4)
    steps = ((360, "Parafin (dầu mỏ)", NAVY), (620, "năng lượng hoá học", ORANGE), (880, "nhiệt + ánh sáng", RED))
    for j, (y, s, c) in enumerate(steps):
        if j: arrow(d, (W / 2, y - 190), (W / 2, y - 78), A(c, k), w=7, head=22)
        box(d, y, s, c, k)
    kn = appear(t, M[1] + 0.3, 0.45)
    if kn > 0:
        card(d, (40, 1020, 1040, 1420), fill=A((239, 246, 255), kn), outline=A(BLUE, kn), w=4)
        text(d, (W / 2, 1095), "≈ 1/5 vào nước", 60, BLUE, alpha=kn)
        x0, x1, y0, y1 = 100, 980, 1170, 1350
        xs = x0 + (x1 - x0) * TI_LE
        d.rectangle([x0, y0, xs, y1], fill=A(BLUE, kn))
        d.rectangle([xs, y0, x1, y1], fill=A((203, 213, 225), kn))
        stripes(d, xs, y0, x1, y1, t, A((148, 163, 184), kn))
        d.rectangle([x0, y0, x1, y1], outline=A(NAVY, kn), width=4)

# ---------------- canh 5: Bay (khi thai) roi Chua noi duoc ----------------
def cup_down(d, cx, base, fog, t, alpha=1.0):
    """coc thuy tinh up tren ngon nen: thanh coc mo hoi nuoc."""
    d.rounded_rectangle([cx - 120, base - 300, cx + 120, base], radius=18, outline=A(CAN_D, alpha), width=6)
    for i in range(int(26 * fog)):
        x = cx - 100 + (i * 37) % 200; y = base - 270 + (i * 53) % 230
        dot(d, x, y, 6, A((148, 190, 230), alpha))
    d.rectangle([cx - 24, base - 120, cx + 24, base + 60], fill=A(WAX, alpha), outline=A(NAVY, alpha), width=3)
    flame(d, cx, base - 130, t, alpha, s=0.8)

def cup_lime(d, cx, base, cloudy, t, alpha=1.0):
    d.line([(cx - 110, base - 280), (cx - 100, base), (cx + 100, base), (cx + 110, base - 280)], fill=A(CAN_D, alpha), width=6)
    col = mix(LIME, MILK, cloudy)
    d.polygon([(cx - 106, base - 150), (cx - 100, base - 4), (cx + 100, base - 4), (cx + 106, base - 150)], fill=A(col, alpha))
    if cloudy > 0.2:
        for i in range(18):
            x = cx - 85 + (i * 41) % 170; y = base - 130 + (i * 29) % 110
            dot(d, x, y, 5, A((203, 213, 225), alpha * cloudy))

BAY_ST = 3.4
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] + 0.3, 0.45)
    card(d, (40, 262, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    fog = clamp((t - 0.3) / 1.2); cl = clamp((t - 1.2) / 1.2)
    cup_down(d, 290, 760, fog, t); cup_lime(d, 790, 760, cl, t)
    kv = appear(t, BAY_ST, 0.4)
    if kv > 0:
        text(d, (290, 400), "→ hơi nước", 58, BLUE, alpha=kv)
        text(d, (790, 400), "→ CO2", 58, NAVY, alpha=kv)
        text(d, (790, 835), "nước vôi đục", 56, NAVY, alpha=kv)            # bang chung (kiem-v1 muc 4)
    y0 = 960
    a1 = appear(t, 0.1, 0.4) * (1 - k2)
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        q = "“Nến không thải khí gì”"
        ks = clamp((t - BAY_ST) / 0.4)
        lw = tw(d, q, F(58)); yy = y0 + 190
        text(d, (W / 2, yy), q, 58, INK, alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 90), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 200), "số liệu theo mô hình", 58, INK, alpha=k2)
    # bot khi bay len trong coc nuoc voi (chuyen dong)
    if cl > 0:
        for i in range(10):
            ph = (t * 0.7 + i / 10) % 1.0
            x = 720 + (i * 37) % 140; y = 750 - ph * 140
            d.ellipse([x - 12, y - 12, x + 12, y + 12], outline=A(CAN_D, cl), width=4)
    gp = 50 + 35 * (0.5 + 0.5 * math.sin(t * 5.2))         # quang lua nhap nhay
    d.ellipse([290 - gp, 640 - gp, 290 + gp, 640 + gp], outline=A(FLAME_I, 0.8), width=10)

# ---------------- canh 6: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Nhiệt nến như cũ, nước gấp đôi", 58, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 518, k1, ORANGE)
    text(d, (W / 2, 625), "Cùng nến, đun 400 g nước", 60, INK, alpha=k1)
    text(d, (W / 2, 705), "8 phút: tăng mấy độ?", 60, INK, alpha=k1)
    if k1 <= 0: return
    # lon to (gap doi nuoc) tren ngon nen; quang lua nhap nhay; nhiet ke cot do nhap nho (chua biet)
    cx, top, bot = 470, 820, 1150
    gp = 70 + 55 * (0.5 + 0.5 * math.sin(t * 5.2))
    d.ellipse([cx - gp, 1300 - gp, cx + gp, 1300 + gp], fill=A((254, 215, 170), 0.9 * k1))
    d.rounded_rectangle([cx - 260, top, cx + 260, bot], radius=18, fill=A(CAN, k1), outline=A(CAN_D, k1), width=5)
    d.rectangle([cx - 250, top + 90, cx + 250, bot - 10], fill=A((147, 197, 253), k1))
    text(d, (cx, (top + bot) / 2 + 45), "400 g nước", 58, NAVY, alpha=k1)
    d.rectangle([cx - 26, 1300, cx + 26, 1480], fill=A(WAX, k1), outline=A(NAVY, k1), width=3)
    flame(d, cx, 1290, t, k1)
    tx = 880
    d.rounded_rectangle([tx - 16, 800, tx + 16, 1320], radius=16, fill=A((241, 245, 249), k1), outline=A(NAVY, k1), width=3)
    d.ellipse([tx - 26, 1300, tx + 26, 1352], fill=A(LIQ, k1), outline=A(NAVY, k1), width=3)
    text(d, (tx, 760), "?", 66, ORANGE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + T_S[0], "tap")]
    out += [(do["t0"] + ts, "tick") for ts in T_S[1:]]
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 0.3, "tap"), (b["t0"] + 0.1, "buzz"),
            (b["t0"] + BAY_ST, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-hoathach-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Năng lượng hoá thạch · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đốt nến đun nước", draw=s_hook, tail=THINK_END, caps=[
   ("Nến đun 200 g nước 8 phút.", 3.4),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Cứ 2 phút: đọc nhiệt độ, cân nến.", 6.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So nhiệt nến và nước.", 3.6),
   ("Phần lớn nhiệt thoát ra.", 3.8)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Năng lượng đổi dạng.", 3.0),
   ("Một phần vào nước.", 3.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Úp cốc, lắc nước vôi.", 5.2),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự nghĩ.", 7.0)]),
])

def _kiem_so():
    import json, os
    bad = []
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "content", "thi-nghiem", "tn-l9-hoathach-02.json")
    k = json.load(open(p)); ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    if [tuple(r) for r in k["so_lieu_mau"]["hang"]] != [tuple(r) for r in ROWS]: bad.append("so_lieu_mau")
    if ts["m_nuoc"]["gia_tri"] != M_NUOC or ts["q"]["gia_tri"] != Q_PARAFIN: bad.append("tham_so")
    if abs(Q_NEN - 40320) > 1e-6 or abs(Q_NUOC - 8025.6) > 1e-6 or not (0.19 < TI_LE < 0.21): bad.append(("Q", Q_NEN, Q_NUOC, TI_LE))
    if round(Q_NEN / 1000) != 40 or round(Q_NUOC / 1000) != 8 or round((Q_NEN - Q_NUOC) / 1000) != 32: bad.append("lam tron")
    # mo hinh kho: T = T0 + 50(1 - e^(-K t/50)), K = eta0.q.v/(m.c)
    K = ts["eta0"]["gia_tri"] * Q_PARAFIN * ts["v_chay"]["gia_tri"] / (M_NUOC * C_NUOC)
    T = lambda tm: T0 + 50 * (1 - math.exp(-K * tm / 50))
    if any(abs(round(T(tm), 1) - Tv) > 1e-9 for tm, _, Tv in ROWS): bad.append("bang lech mo hinh")
    if any(abs(ts["v_chay"]["gia_tri"] * tm - m) > 1e-9 for tm, m, _ in ROWS): bad.append("nen chay lech v_chay")
    inc = [round(ROWS[i + 1][2] - ROWS[i][2], 1) for i in range(4)]
    K4 = ts["eta0"]["gia_tri"] * Q_PARAFIN * ts["v_chay"]["gia_tri"] / (2 * M_NUOC * C_NUOC)     # cau chot: 400 g, 8 phut (mo hinh kho)
    if round(50 * (1 - math.exp(-K4 * 8 / 50))) != 5: bad.append(("cau chot 400 g", 50 * (1 - math.exp(-K4 * 8 / 50))))
    return bad

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch kho/mô hình:", _kiem_so() or "không")
