# Clip: tn-l9-hoathach-02 - Dot nen parafin dun 200 g nuoc (KHTN 9 Bai 16, lesson 94; 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-hoathach-02.json:
#   so_lieu_mau (t phut, nen chay g, nuoc °C): 0 0,00 28,0 ; 2 0,24 30,6 ; 4 0,48 33,0 ; 6 0,72 35,4 ; 8 0,96 37,6
#   tham_so: m_nuoc = 200 g, q = 42 000 J/g (xap xi); mo_hinh: c = 4,18 J/(g.K), T = 28 + 50(1 - e^(-K t/50)), K = 1,33.
#   Tinh lai (assert trong _kiem_so): Q nen = 0,96 . 42 000 = 40 320 J ~ 40 kJ ; Q nuoc = 200 . 4,18 . 9,6 = 8 026 J ~ 8 kJ
#   -> ~ 20 % (khoang 1/5). Phut 10 theo mo hinh: 39,65 °C -> tang 2,05 < 2,2 (cau chot, KHONG hien dap so).
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
    text(d, (330, CAN_Y0 + 110), f"{M_NUOC} g nước", 40, NAVY)

def readouts(d, temp, burnt, tmin, alpha=1.0):
    for y0, lab, val, col in ((300, "nước", vn(temp) + " °C", RED), (500, "nến đã cháy", vn(burnt, 2) + " g", NAVY)):
        card(d, (680, y0, 1020, y0 + 170), fill=A((70, 78, 100), alpha), r=22)
        text(d, (850, y0 + 42), lab, 40, WHITE, bold=False, alpha=alpha)
        card(d, (705, y0 + 75, 995, y0 + 150), fill=A((220, 240, 225), alpha), r=12)
        text(d, (850, y0 + 113), val, 52, col if col != RED else (153, 27, 27), alpha=alpha)
    if tmin is not None: text(d, (850, 730), f"phút {tmin}", 46, ORANGE, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, 0.0, ROWS[0][2], lit=t > 0.6)
    text(d, (580, TRAY_Y - 120), "nến parafin", 40, INK, anchor="lm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 245, "Nhiệt nến toả ra,\nbao nhiêu phần đi vào nước?", 52, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 420, 940, y0 + 432], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 420, 140 + 800 * (1 - p), y0 + 432], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (moi 2 phut mot lan doc, tua nhanh) ----------------
T_S = (0.6, 1.9, 3.2, 4.5, 5.8)     # luc doc phut 0, 2, 4, 6, 8
T_ROW = 0.4
def do_state(t):
    k = max(0, sum(1 for ts in T_S if t >= ts - 1e-9) - 1)
    n = sum(1 for ts in T_S if t >= ts + T_ROW - 1e-9)
    return k, n

XS = (200, 540, 870)
def table(d, n, y=1060, hl=None, alpha=1.0):
    card(d, (40, y, 1040, y + 580), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, h in zip(XS, ("t (phút)", "nến cháy (g)", "nước (°C)")): text(d, (x, y + 55), h, 42, INK, alpha=alpha)
    d.line([(70, y + 100), (1010, y + 100)], fill=A(LIGHT, alpha), width=3)
    for j, (tm, m, T) in enumerate(ROWS):
        yy = y + 150 + j * 92
        if hl == j: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=20, fill=A((255, 237, 213), alpha))
        if j < n:
            text(d, (XS[0], yy), str(tm), 46, NAVY, alpha=alpha)
            text(d, (XS[1], yy), vn(m, 2), 46, NAVY, alpha=alpha)
            text(d, (XS[2], yy), vn(T), 46, (153, 27, 27), alpha=alpha)
        else:
            for x in XS: text(d, (x, yy), "·", 44, GRAY, alpha=alpha)

def s_do(img, d, t, sc):
    k, n = do_state(t)
    tm, m, T = ROWS[k]
    rig(d, t, m / DM, T); readouts(d, T, m, tm)
    table(d, n, y=1060, hl=(n - 1 if n > 0 else None))
    card(d, (40, 975, 1040, 1045), fill=(255, 247, 237), outline=ORANGE, r=24, w=3)
    text(d, (W / 2, 1010), "An toàn: buộc tóc, nến trên khay kim loại", 40, (154, 52, 18))

# ---------------- canh 3: Dap an (hai thanh nhiet, KHONG cong thuc: THCS chua hoc nhiet dung rieng) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · chỉ khoảng 1/5"
    pw = tw(d, lab, F(46)) + 60
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 350), fill=A(NAVY, ka), r=38)
    text(d, (W / 2, 310), lab, 46, WHITE, alpha=ka)
    x0, x1 = 80, 1000
    k1 = appear(t, 0.7, 0.4)
    card(d, (40, 390, 1040, 1010), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    text(d, (x0, 455), "nến toả", 44, ORANGE, anchor="lm", alpha=k1)
    g1 = clamp((t - 0.8) / 0.6)
    if g1 > 0: d.rounded_rectangle([x0, 500, x0 + (x1 - x0) * g1, 600], radius=14, fill=A(ORANGE, k1))
    text(d, (W / 2, 550), f"≈ {round(Q_NEN / 1000)} kJ", 48, WHITE, alpha=k1 * appear(t, 1.3, 0.3))
    k2 = appear(t, M[0] + 1.6, 0.4)
    text(d, (x0, 690), "nước nhận", 44, BLUE, anchor="lm", alpha=k2)
    g2 = clamp((t - M[0] - 1.7) / 0.5)
    xs = x0 + (x1 - x0) * TI_LE
    if g2 > 0: d.rounded_rectangle([x0, 735, x0 + (xs - x0) * g2, 835], radius=14, fill=A(BLUE, k2))
    text(d, (xs + 30, 785), f"≈ {round(Q_NUOC / 1000)} kJ", 48, BLUE, anchor="lm", alpha=k2 * appear(t, M[0] + 2.1, 0.3))
    text(d, (W / 2, 930), "(tính sẵn từ số đo)", 40, MUTED, bold=False, alpha=k2)
    # thanh chia: phan vao nuoc / phan ra ngoai
    kb = appear(t, M[1] - 0.2, 0.6)
    if kb > 0:
        card(d, (40, 1060, 1040, 1400), fill=A(WHITE, kb), outline=A(NAVY, kb), w=4)
        y0, y1 = 1120, 1260
        d.rectangle([x0, y0, x0 + (xs - x0) * kb, y1], fill=BLUE)
        d.rectangle([xs, y0, xs + (x1 - xs) * kb, y1], fill=(203, 213, 225))
        d.rectangle([x0, y0, x1, y1], outline=NAVY, width=4)
        kl = appear(t, M[1] + 0.5, 0.4)
        text(d, ((xs + x1) / 2, (y0 + y1) / 2), f"≈ {round((Q_NEN - Q_NUOC) / 1000)} kJ ra ngoài", 46, NAVY, alpha=kl)
        text(d, (x0, y1 + 70), "vào nước", 42, BLUE, anchor="lm", alpha=kl)

# ---------------- canh 4: Rut ra (chuoi chuyen hoa) ----------------
def box(d, y, s, col, k, fill=WHITE):
    card(d, (100, y - 75, 980, y + 75), fill=A(fill, k), outline=A(col, k), w=5)
    text(d, (W / 2, y), s, 52, col, alpha=k)
def s_rutra(img, d, t, sc):
    M = sc["M"]
    steps = ((400, "Parafin (từ dầu mỏ)", NAVY), (720, "năng lượng hoá học", ORANGE), (1040, "nhiệt + ánh sáng", RED))
    for j, (y, s, c) in enumerate(steps):
        k = appear(t, 0.3 + 0.9 * j, 0.4)
        if j and k > 0: arrow(d, (W / 2, y - 235), (W / 2, y - 85), A(c, k), w=7, head=22)
        box(d, y, s, c, k)
    kn = appear(t, 3.2, 0.4)
    card(d, (100, 1220, 980, 1400), fill=A((239, 246, 255), kn), outline=A(BLUE, kn), w=4)
    ctext(d, 1310, "≈ 1/5 vào nước", 46, BLUE, maxw=840, alpha=kn)

# ---------------- canh 5: Bay (khi thai) roi Chua noi duoc ----------------
def cup_down(d, cx, base, fog, alpha=1.0):
    """coc thuy tinh up tren ngon nen: thanh coc mo hoi nuoc."""
    d.rounded_rectangle([cx - 120, base - 300, cx + 120, base], radius=18, outline=A(CAN_D, alpha), width=6)
    for i in range(int(26 * fog)):
        x = cx - 100 + (i * 37) % 200; y = base - 270 + (i * 53) % 230
        dot(d, x, y, 6, A((148, 190, 230), alpha))
    d.rectangle([cx - 24, base - 120, cx + 24, base + 60], fill=A(WAX, alpha), outline=A(NAVY, alpha), width=3)
    flame(d, cx, base - 130, 0.3, alpha, s=0.8)

def cup_lime(d, cx, base, cloudy, alpha=1.0):
    d.line([(cx - 110, base - 280), (cx - 100, base), (cx + 100, base), (cx + 110, base - 280)], fill=A(CAN_D, alpha), width=6)
    col = mix(LIME, MILK, cloudy)
    d.polygon([(cx - 106, base - 150), (cx - 100, base - 4), (cx + 100, base - 4), (cx + 106, base - 150)], fill=A(col, alpha))
    if cloudy > 0.2:
        for i in range(18):
            x = cx - 85 + (i * 41) % 170; y = base - 130 + (i * 29) % 110
            dot(d, x, y, 5, A((203, 213, 225), alpha * cloudy))

def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    card(d, (40, 262, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    fog = clamp((t - 0.3) / 1.2); cl = clamp((t - M[0] - 0.8) / 1.0)
    cup_down(d, 290, 760, fog); cup_lime(d, 790, 760, cl)
    text(d, (290, 415), "thành cốc mờ", 42, BLUE, alpha=appear(t, 1.2, 0.4))
    text(d, (790, 830), "nước vôi đục", 42, NAVY, alpha=appear(t, M[0] + 1.4, 0.4))
    a1 = appear(t, 0.1, 0.4) * (1 - k2)
    if a1 > 0:
        y0 = 950
        card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Đốt nến không thải khí gì”"
        ks = clamp((t - M[0] - 1.6) / 0.4)
        f = F(44); lw = tw(d, q, f); yy = y0 + 180
        text(d, (W / 2, yy), q, 44, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        kk = a1 * ks
        card(d, (70, y0 + 270, 1010, y0 + 430), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 350), "✓ Có hơi nước và CO2", 48, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 950 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y0 + 190), "Số liệu tính từ mô hình", 46, INK, alpha=kk)

# ---------------- canh 6: Chot + cau hoi ----------------
HINT_AT = 4.4
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 262, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 391, "Đốt nhiên liệu: nhiệt kèm CO2", 48, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 676), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 643), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    seq = " → ".join(vn(r[2]) for r in ROWS) + " °C"
    text(d, (W / 2, 750), seq, 40, (153, 27, 27), alpha=kq)
    ctext(d, 930, "Phút 8 → 10, nước tăng nhiều hơn\nhay ít hơn lần trước (2,2 °C)?", 46, INK, maxw=920, alpha=kq)
    kh = appear(t, M[0] + HINT_AT, 0.5)
    if kh > 0:
        card(d, (110, 1110, 970, 1360), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1235, "Nhìn từng bước 2 phút", 44, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"), (do["t0"] + T_S[0], "tap")]
    out += [(do["t0"] + ts, "tick") for ts in T_S[1:]]
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + 0.3, "tap"), (b["t0"] + 0.1, "buzz"),
            (b["t0"] + b["M"][0] + 1.6, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-hoathach-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Năng lượng hoá thạch · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đốt nến đun nước", draw=s_hook, tail=0.8, caps=[
   ("Nến đun lon nước 8 phút.", 3.2),
   ("Tự trả lời trước khi xem.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Cứ 2 phút đọc nhiệt độ, cân nến.", 3.8),
   ("Nến ngắn dần.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("So nhiệt nến và nước.", 3.6),
   ("Phần lớn nhiệt thoát ra.", 3.6)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Năng lượng đổi dạng ra sao?", 4.9)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Úp cốc, lắc nước vôi.", 4.4),
   ("Còn chưa nói được.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Tự nghĩ, rồi xem gợi ý.", 6.0)]),
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
    if inc[-1] != 2.2 or not (T(10) - ROWS[-1][2] < 2.2): bad.append(("cau chot", inc, T(10)))
    return bad

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch kho/mô hình:", _kiem_so() or "không")
