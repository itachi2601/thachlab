# Clip: tn-l9-hoathach-01 - Mo hinh vong nuoc trong bat thuy tinh (KHTN 9 Bai 16, lesson 94; 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-hoathach-01.json:
#   tham_so: T_nuoc mac dinh 50 °C (min 25), T_da = 5 °C (mat mang duoi da); cac_buoc.lam: 10-15 phut.
#   so_lieu_mau (sau 10 phut): 50 °C -> "mang mo, giot roi duoi cho da"; 25 °C -> "mang hoi mo, chua co giot roi".
#   t_giot (thoi gian toi giot dau) la do_duoc, KHO KHONG CO GIA TRI -> clip khong ghi phut nao giot dau roi.
#   hien_tuong_hay_sai[0] = bay ("giot la nuoc da tan tham qua mang"); chua noi duoc = ghi_chu + gia_thiet[0].
#   an_toan: nuoc am, khong dung nuoc soi voi bat thuy tinh mong.
# Cau Tu kiem tra cua bai (Cau 1-7) khong hoi ve bat nuoc; clip KHONG noi "dia nhiet/hat nhan khong tu Mat Troi" (Cau 1),
#   khong noi nang luong cay (Cau 2), khong noi dau mo (Cau 5, 7).
# Du doan (K10: chi cau hoi + hinh): giot dong nhieu nhat o dau? -> mat duoi mang, ngay duoi da.
# Cau chot: de ho mot goc mang -> giot roi lai it hon (gia_thiet[1]: bat kin nen hoi khong thoat; clip chua chieu ca ho).
import math, random
from engine import *

T_NUOC, T_NGUOI, T_DA, PHUT = 50, 25, 5, 10
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

GLASS = (148, 190, 220); WATER = (147, 197, 253); WATER_D = (96, 165, 250); FILM = (120, 130, 160)
ICE = (224, 242, 254); FOG = (186, 214, 236); DGREEN = (21, 110, 55); DRED = (185, 28, 28); GLOW = (255, 214, 80)

# ---------------- hinh bat ----------------
CX, RIM, BOT, HALFW, WL = 540, 700, 940, 300, 800        # tam x, mieng bat, day bat, nua rong, muc nuoc
SAG = 36                                                 # mang vong xuong o giua do da de
def bowl_y(x):                                           # day bat (nua duoi elip)
    u = clamp((x - CX) / HALFW, -1, 1); return RIM + (BOT - RIM) * math.sqrt(1 - u * u)
def bowl_x(y):                                           # nua rong long bat o do cao y
    v = clamp((y - RIM) / (BOT - RIM), 0, 1); return HALFW * math.sqrt(1 - v * v)
def film_y(x):
    u = clamp(abs(x - CX) / HALFW, 0, 1); return RIM + SAG * (1 - u) ** 1.6
DROP_Y = RIM + SAG + 6                                   # dinh giot (duoi mat mang tai cho da)

def lamp(d, on, x0=150):
    d.rectangle([x0 - 40, 1000, x0 + 60, 1018], fill=NAVY)
    d.line([(x0 + 10, 1000), (x0 + 10, 420), (x0 + 120, 330)], fill=NAVY, width=10, joint="curve")
    d.polygon([(x0 + 90, 300), (x0 + 210, 300), (x0 + 240, 380), (x0 + 60, 380)], fill=(70, 78, 100))
    if on > 0:
        d.polygon([(x0 + 70, 384), (x0 + 230, 384), (CX + 260, RIM - 10), (CX - 190, RIM - 10)], fill=A(GLOW, 0.22 * on))
        d.ellipse([x0 + 120, 368, x0 + 180, 396], fill=A(GLOW, on))

def bowl(d, wl=WL, warm=1.0, ice=1.0, melt=0.0, fog=0.0, film=True):
    # nuoc
    pts = [(CX - bowl_x(wl), wl)] + [(x, bowl_y(x)) for x in range(int(CX - bowl_x(wl)), int(CX + bowl_x(wl)) + 1, 10)] + [(CX + bowl_x(wl), wl)]
    d.polygon(pts, fill=mix(WATER, (253, 186, 140), 0.35 * warm))
    # than bat
    pts = [(x, bowl_y(x)) for x in range(CX - HALFW, CX + HALFW + 1, 8)]
    d.line(pts, fill=GLASS, width=12, joint="curve")
    d.ellipse([CX - 90, BOT - 6, CX + 90, BOT + 26], fill=GLASS)
    if film:
        fp = [(x, film_y(x)) for x in range(CX - HALFW - 20, CX + HALFW + 21, 10)]
        if fog > 0:                                      # hoi nuoc bam mat duoi mang
            R = random.Random(3)
            for i in range(int(90 * fog)):
                x = R.uniform(CX - HALFW + 30, CX + HALFW - 30); r = R.uniform(4, 8)
                dot(d, x, film_y(x) + 8 + R.uniform(0, 6), r, A(FOG, 0.9))
        d.line(fp, fill=FILM, width=5, joint="curve")
    if ice > 0:                                          # da tren mang
        for dx, dy, s in ((-70, -6, 58), (0, 0, 62), (68, -8, 56)):
            x, y = CX + dx, film_y(CX + dx) - 4 + dy
            sh = s * (1 - 0.35 * melt)
            d.rounded_rectangle([x - sh / 2, y - sh, x + sh / 2, y], radius=10, fill=A(ICE, ice), outline=A(WATER_D, ice), width=4)
        if melt > 0:                                     # nuoc da tan nam TREN mang
            d.ellipse([CX - 150, RIM + SAG - 20, CX + 150, RIM + SAG + 2], fill=A(WATER_D, 0.55 * melt))

def drop(d, r, y=None):
    if r < 2: return
    y = DROP_Y if y is None else y
    d.polygon([(CX - r * 0.7, y + r * 0.6), (CX + r * 0.7, y + r * 0.6), (CX, y - r * 0.9)], fill=WATER_D)
    d.ellipse([CX - r, y, CX + r, y + 2 * r], fill=WATER_D)

def vapour(d, t, k):
    if k <= 0: return
    R = random.Random(11)
    for i in range(16):
        x = CX + R.uniform(-0.8, 0.8) * bowl_x(WL); ph = (t * 0.55 + R.random()) % 1.0
        y = WL - 8 - ph * (WL - film_y(x) - 20)
        d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=A(WATER_D, 0.75 * k * (1 - ph * 0.4)), width=3)

def scene_base(d):
    card(d, (40, 262, 1040, 1040), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 1020), (1020, 1020)], fill=(180, 170, 150), width=4)

def labels(d, alpha=1.0, temp=T_NUOC):
    text(d, (CX + HALFW + 40, RIM - 70), "đá", 58, (14, 116, 144), anchor="lm", alpha=alpha)
    d.line([(CX + 100, RIM - 30), (CX + HALFW + 30, RIM - 70)], fill=A((14, 116, 144), 0.6 * alpha), width=3)
    text(d, (CX + HALFW + 30, RIM + 25), "màng", 56, NAVY, anchor="lm", alpha=alpha)
    text(d, (CX + HALFW + 30, RIM + 85), "bọc", 56, NAVY, anchor="lm", alpha=alpha)
    card(d, (CX - 160, WL + 36, CX + 160, WL + 116), fill=A(WHITE, 0.92 * alpha), outline=A(ORANGE, alpha), r=20)
    text(d, (CX, WL + 76), f"nước {temp} °C", 56, ORANGE, alpha=alpha)
    text(d, (410, 300), "đèn bàn", 56, NAVY, anchor="lm", alpha=alpha)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
THINK_END = 0.3


def pill(d, s, y, a, color=NAVY, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_hook(img, d, t, sc):
    M = sc["M"]
    scene_base(d); lamp(d, appear(t, 0.5, 0.6)); bowl(d); labels(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1060 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 510), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 165), f"Sau {PHUT} phút, giọt nước", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "đọng nhiều nhất ở đâu?", 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 330, 970, y0 + 430], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 330, 110 + max(90, 860 * (1 - p)), y0 + 430], radius=45, fill=A((76, 29, 149), a))

# ---------------- canh 2: Tien hanh (tua nhanh 10 phut trong mot canh, lien mach) ----------------
T_ON, T_RUN = 0.6, 7.4            # bat den; ket thuc tua nhanh (ung 10 phut)
T_D1, T_D2 = 5.4, 6.7             # hai giot roi (khong gan phut nao: kho khong co t_giot)
def tien_trinh(t):
    """-> (k tua 0..1, ban kinh giot dang lon, (y giot dang roi hoac None))."""
    k = clamp((t - T_ON) / (T_RUN - T_ON))
    def grow(t0, dur): return 0.0 if t < t0 else 4 + 18 * clamp((t - t0) / dur)
    fall = None
    if t < T_D1: r = grow(T_D1 - 1.4, 1.4)
    elif t < T_D2: r = grow(T_D1 + 0.3, T_D2 - T_D1 - 0.3)
    else: r = grow(T_D2 + 0.3, 1.2)
    for td in (T_D1, T_D2):
        if td <= t < td + 0.35: fall = DROP_Y + 30 + (WL - DROP_Y - 40) * ((t - td) / 0.35) ** 2
    return k, r, fall

def s_do(img, d, t, sc):
    k, r, fall = tien_trinh(t)
    scene_base(d); lamp(d, 1.0); bowl(d, fog=k)
    vapour(d, t, appear(t, T_ON, 0.6))
    drop(d, r)
    if fall is not None: drop(d, 12, fall)
    text(d, (W / 2, 1085), f"tua nhanh: 0 → {PHUT} phút", 56, ORANGE)
    d.rounded_rectangle([110, 1125, 970, 1305], radius=50, fill=(255, 237, 213))
    if k > 0:
        xe = 110 + max(100, 860 * k)
        d.rounded_rectangle([110, 1125, xe, 1305], radius=50, fill=ORANGE)
        off = (t * 260) % 120                       # soc cheo chay (chuyen dong vung giua)
        for x in range(int(110 - 200 + off), int(xe), 120):
            x0, x1 = max(x, 140), min(x + 180, xe - 30)
            if x1 > x0 + 10: d.polygon([(x0, 1305 - 20), (x0 + 50, 1305 - 20), (min(x0 + 50 + 140, xe - 30), 1145), (min(x0 + 140, xe - 30), 1145)], fill=(154, 52, 18))
    kz = appear(t, sc["M"][1], 0.4)               # khung phong to mat duoi mang (kiem-v1 muc 3)
    if kz > 0:
        zx, zy, zr = 870, 420, 125
        d.line([(CX + 25, DROP_Y + 8), (zx - zr * 0.8, zy + zr * 0.6)], fill=A(NAVY, kz), width=3)
        d.ellipse([zx - zr, zy - zr, zx + zr, zy + zr], fill=A(WHITE, kz), outline=A(NAVY, kz), width=4)
        d.line([(zx - zr + 10, zy - 45), (zx + zr - 10, zy - 45)], fill=A(FILM, kz), width=6)
        d.rounded_rectangle([zx - 45, zy - 105, zx + 45, zy - 48], radius=8, fill=A(ICE, kz), outline=A(WATER_D, kz), width=3)
        rz = max(r, 6) * 1.6
        for dx, s_ in ((-55, 0.6), (0, 1.0), (55, 0.7)):
            rr = rz * s_; x_ = zx + dx; y_ = zy - 42
            d.polygon([(x_ - rr * 0.7, y_ + rr * 0.6), (x_ + rr * 0.7, y_ + rr * 0.6), (x_, y_ - rr * 0.9)], fill=A(WATER_D, kz))
            d.ellipse([x_ - rr, y_, x_ + rr, y_ + 2 * rr], fill=A(WATER_D, kz))
        tag(d, 1030, 592, "mặt dưới màng", NAVY, alpha=kz, anchor="r")
    card(d, (40, 1340, 1040, 1460), fill=(255, 247, 237), outline=ORANGE, w=4)   # an toan (kho: an_toan)
    text(d, (W / 2, 1400), "An toàn: không dùng nước sôi", 56, (154, 52, 18))

# ---------------- canh 3: Dap an (vong 3 khau) ----------------
def tag(d, x, y, s, col, alpha=1.0, anchor="m", size=56):
    w = tw(d, s, F(size)) + 34
    x0 = x - w / 2 if anchor == "m" else (x if anchor == "l" else x - w)
    card(d, (x0, y - 42, x0 + w, y + 42), fill=A(WHITE, 0.95 * alpha), outline=A(col, alpha), r=20, w=3)
    text(d, (x0 + w / 2, y), s, size, col, alpha=alpha)

DA_1, DA_3 = 2.6, 7.2
def s_dapan(img, d, t, sc):
    M = sc["M"]
    scene_base(d); lamp(d, 1.0); bowl(d, fog=1.0); drop(d, 20)
    vapour(d, t, 1.0)
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN: ngay dưới đá", 1110, ka)
    k1 = appear(t, DA_1, 0.4); k2 = appear(t, M[1] + 0.3, 0.4); k3 = appear(t, DA_3, 0.4)
    if k1 > 0:
        arrow(d, (CX - 170, WL - 10), (CX - 170, RIM + 22), A(ORANGE, k1), w=7, head=20)
        tag(d, 250, WL + 90, "1 bay hơi", ORANGE, alpha=k1)
    if k2 > 0:
        d.line([(CX + 30, DROP_Y + 10), (800, 600)], fill=A(BLUE, 0.7 * k2), width=3)
        tag(d, 1020, 560, f"2 ngưng tụ, ~{T_DA} °C", BLUE, alpha=k2, anchor="r")
    if k3 > 0:
        arrow(d, (CX, DROP_Y + 50), (CX, WL - 6), A(WATER_D, k3), w=7, head=20)
        tag(d, CX + 40, WL + 90, "3 rơi lại", BLUE, alpha=k3, anchor="l")

# ---------------- canh 4: Rut ra (nuoc nguoi + ngoai troi) ----------------
def mini(d, x0, temp, warm, fogk, rr, title_col, t=0.0):
    card(d, (x0, 270, x0 + 470, 800), fill=WHITE, outline=LIGHT, w=3)
    cx, rim, bot, hw, wl = x0 + 235, 470, 640, 180, 540
    def by(x):
        u = clamp((x - cx) / hw, -1, 1); return rim + (bot - rim) * math.sqrt(1 - u * u)
    def bx(y):
        v = clamp((y - rim) / (bot - rim), 0, 1); return hw * math.sqrt(1 - v * v)
    pts = [(cx - bx(wl), wl)] + [(x, by(x)) for x in range(int(cx - bx(wl)), int(cx + bx(wl)) + 1, 8)] + [(cx + bx(wl), wl)]
    d.polygon(pts, fill=mix(WATER, (253, 186, 140), 0.35 * warm))
    d.line([(x, by(x)) for x in range(cx - hw, cx + hw + 1, 6)], fill=GLASS, width=9, joint="curve")
    def fy(x):
        u = clamp(abs(x - cx) / hw, 0, 1); return rim + 24 * (1 - u) ** 1.6
    R = random.Random(5)
    for i in range(int(60 * fogk)):
        x = R.uniform(cx - hw + 20, cx + hw - 20); dot(d, x, fy(x) + 7 + R.uniform(0, 4), R.uniform(3, 6), FOG)
    d.line([(x, fy(x)) for x in range(cx - hw - 14, cx + hw + 15, 8)], fill=FILM, width=4, joint="curve")
    for dx in (-40, 40):
        x = cx + dx; y = fy(x) - 3
        d.rounded_rectangle([x - 28, y - 52, x + 28, y], radius=8, fill=ICE, outline=WATER_D, width=3)
    if rr > 0:                                       # giot lon roi roi lap lai (1,6 s)
        y = rim + 30; ph = (t % 1.6) / 1.6
        d.ellipse([cx - rr, y, cx + rr, y + 2 * rr], fill=WATER_D)
        if ph > 0.5: yy = y + 2 * rr + (wl - y - 2 * rr) * ((ph - 0.5) / 0.5) ** 2; d.ellipse([cx - 9, yy, cx + 9, yy + 18], fill=WATER_D)
    text(d, (cx, 330), f"nước {temp} °C", 56, title_col)
    return cx

def s_rutra(img, d, t, sc):
    M = sc["M"]
    mini(d, 40, T_NUOC, 1.0, 1.0, 14, ORANGE, t)
    mini(d, 570, T_NGUOI, 0.0, 0.35, 0, BLUE, t)
    text(d, (275, 730), "giọt rơi", 56, INK); text(d, (805, 730), "chưa có giọt", 56, INK)
    k2 = appear(t, M[1] + 0.3, 0.45)
    if k2 > 0:
        y0 = 850 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 240), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, y0 + 75), "đèn → Mặt Trời", 58, DGREEN, alpha=k2)
        text(d, (W / 2, y0 + 170), "đá → khí lạnh trên cao", 58, DGREEN, alpha=k2)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
BAY_ST = 2.5
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] + 0.3, 0.45)
    a1 = appear(t, 0.1, 0.4) * (1 - k2)
    melt = clamp((t - 0.6) / 1.6)
    scene_base(d); lamp(d, 1.0); bowl(d, fog=1.0, melt=melt, ice=1.0); drop(d, 20); vapour(d, t, 1.0)
    kv = appear(t, BAY_ST, 0.4)
    if kv > 0:                    # nhan bac bay giu toi het canh (cong B 18/11)
        d.line([(760, RIM - 108), (CX + 40, RIM - 40)], fill=A(WATER_D, kv), width=4)      # duong noi nhan -> vat (muc 4)
        d.line([(CX + 60, DROP_Y + 62), (CX + 8, DROP_Y + 30)], fill=A(BLUE, kv), width=4)
        tag(d, 1020, RIM - 150, "đá tan: trên màng", WATER_D, alpha=kv, anchor="r")
        tag(d, CX + 40, DROP_Y + 100, "giọt: từ hơi", BLUE, alpha=kv, anchor="l")
    y0 = 1070
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        q = "“Giọt là đá tan thấm xuống”"
        ks = clamp((t - BAY_ST) / 0.4)
        lw = tw(d, q, F(58)); yy = y0 + 190
        text(d, (W / 2, yy), q, 58, INK, alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 90), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 200), "lượng nước chưa đo", 58, INK, alpha=k2)

# ---------------- canh 6: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Bọc kín: hơi nước không thoát ra", 58, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 518, k1, ORANGE)
    text(d, (W / 2, 625), "Hở một góc màng.", 60, INK, alpha=k1)
    text(d, (W / 2, 705), "Giọt rơi lại ra sao?", 60, INK, alpha=k1)
    if k1 <= 0: return
    cx, ry, hw, bot = 540, 950, 300, 1230
    pr = 70 + 55 * (0.5 + 0.5 * math.sin(t * 5.2))   # vong sang nhap nhay o goc ho (chuyen dong vung giua)
    gx, gy = cx + hw - 80, ry - 20
    d.ellipse([gx - pr, gy - pr, gx + pr, gy + pr], fill=A((254, 215, 170), 0.9 * k1))          # bat nho, mang ho goc phai; hoi boc len trong bat (KHONG ve hoi thoat ra)
    pts = [(x, ry + (bot - ry) * math.sqrt(max(0, 1 - ((x - cx) / hw) ** 2))) for x in range(cx - hw, cx + hw + 1, 8)]
    wl = 1060
    wp = [(x, y) for x, y in pts if y >= wl]
    if wp: d.polygon([(wp[0][0], wl)] + wp + [(wp[-1][0], wl)], fill=A(mix(WATER, (253, 186, 140), 0.35), k1))
    d.line(pts, fill=A(GLASS, k1), width=10, joint="curve")
    d.line([(cx - hw - 20, ry), (cx + hw - 110, ry + 4)], fill=A(FILM, k1), width=5)
    arrow(d, (905, 845), (800, 915), A(DRED, k1), w=6, head=18)               # chi cho ho (kiem-v1 muc 1)
    text(d, (945, 830), "hở", 66, DRED, alpha=k1)
    d.line([(cx + hw - 110, ry + 4), (cx + hw - 60, ry - 50)], fill=A(FILM, k1), width=5)   # goc mang lat len
    for dx in (-60, 20):
        d.rounded_rectangle([cx + dx - 28, ry - 54, cx + dx + 28, ry - 2], radius=8, fill=A(ICE, k1), outline=A(WATER_D, k1), width=3)
    R = random.Random(11)
    for i in range(14):
        x = cx + R.uniform(-0.7, 0.5) * hw; ph = (t * 0.55 + R.random()) % 1.0
        y = wl - 8 - ph * (wl - ry - 30)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=A(WATER_D, 0.8 * k1), width=3)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + T_ON, "tap")]
    out += [(do["t0"] + T_ON + i * 0.7, "tick") for i in range(1, 10)]
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 0.3, "tap"), (b["t0"] + 0.1, "buzz"),
            (b["t0"] + BAY_ST, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-hoathach-01", header="KHTN 9 · THÍ NGHIỆM", footer="Vòng năng lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bát nước ấm dưới đèn", draw=s_hook, tail=THINK_END, caps=[
   ("Bọc kín, đặt đá lên.", 3.0),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Bật đèn, chờ 10 phút.", 3.4),
   ("Nhìn kĩ mặt dưới màng.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Ba khâu thành vòng kín.", 4.0),
   ("Đá làm lạnh chỗ đó.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Thử với nước nguội.", 3.0),
   ("Ngoài trời cũng vậy.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Đúng không?", 5.0),
   ("Còn bỏ ngỏ.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự nghĩ.", 7.0)]),
])

def _kiem_so():
    bad = []
    if (T_NUOC, T_NGUOI, T_DA) != (50, 25, 5): bad.append("nhiet do khac kho")
    import json, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "content", "thi-nghiem", "tn-l9-hoathach-01.json")
    k = json.load(open(p))
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    if ts["T_nuoc"]["mac_dinh"] != T_NUOC or ts["T_nuoc"]["min"] != T_NGUOI or ts["T_da"]["gia_tri"] != T_DA: bad.append("tham_so")
    h = k["so_lieu_mau"]["hang"]
    if "50" not in h[0][0] or "25" not in h[1][0] or "chưa có giọt" not in h[1][1] or str(PHUT) not in k["so_lieu_mau"]["cot"][1]:
        bad.append("so_lieu_mau")
    return bad

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch kho:", _kiem_so() or "không")
