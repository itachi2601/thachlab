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
    text(d, (CX + HALFW + 40, RIM - 70), "đá", 42, (14, 116, 144), anchor="lm", alpha=alpha)
    d.line([(CX + 100, RIM - 30), (CX + HALFW + 30, RIM - 70)], fill=A((14, 116, 144), 0.6 * alpha), width=3)
    text(d, (CX + HALFW + 40, RIM + 20), "màng", 40, FILM, anchor="lm", alpha=alpha)
    text(d, (CX + HALFW + 40, RIM + 68), "bọc", 40, FILM, anchor="lm", alpha=alpha)
    card(d, (CX - 120, WL + 40, CX + 120, WL + 104), fill=A(WHITE, 0.92 * alpha), outline=A(ORANGE, alpha), r=20)
    text(d, (CX, WL + 72), f"nước {temp} °C", 40, ORANGE, alpha=alpha)
    text(d, (410, 300), "đèn bàn", 40, NAVY, anchor="lm", alpha=alpha)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    scene_base(d); lamp(d, appear(t, 0.5, 0.6)); bowl(d); labels(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1080 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 245, "Sau 10 phút, giọt nước\nđọng nhiều nhất ở đâu?", 52, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 420, 940, y0 + 432], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 420, 140 + 800 * (1 - p), y0 + 432], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (tua nhanh 10 phut trong mot canh, lien mach) ----------------
T_ON, T_RUN = 0.6, 7.6            # bat den; ket thuc tua nhanh (ung 10 phut)
T_D1, T_D2 = 5.4, 6.9             # hai giot roi (khong gan phut nao: kho khong co t_giot)
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

def clock(d, k, alpha=1.0):
    cx, cy, R0 = 900, 360, 58
    d.ellipse([cx - R0, cy - R0, cx + R0, cy + R0], fill=A(WHITE, alpha), outline=A(NAVY, alpha), width=5)
    if k > 0: d.pieslice([cx - R0 + 8, cy - R0 + 8, cx + R0 - 8, cy + R0 - 8], -90, -90 + 360 * k, fill=A((254, 215, 170), alpha))
    ang = math.radians(-90 + 360 * k)
    d.line([(cx, cy), (cx + 44 * math.cos(ang), cy + 44 * math.sin(ang))], fill=A(ORANGE, alpha), width=6)
    text(d, (cx, cy + R0 + 36), "tua nhanh", 40, ORANGE, alpha=alpha)
    text(d, (cx, cy + R0 + 84), f"0 → {PHUT} phút", 40, NAVY, alpha=alpha)

def s_do(img, d, t, sc):
    k, r, fall = tien_trinh(t)
    scene_base(d); lamp(d, 1.0); bowl(d, fog=k); labels(d, alpha=0.9)
    vapour(d, t, appear(t, T_ON, 0.6))
    drop(d, r)
    if fall is not None: drop(d, 12, fall)
    clock(d, k)
    # an toan (kho: an_toan)
    card(d, (40, 1080, 1040, 1200), fill=(255, 247, 237), outline=ORANGE, w=4)
    text(d, (W / 2, 1140), "An toàn: nước ấm, không dùng nước sôi", 40, (154, 52, 18))

# ---------------- canh 3: Dap an (vong 3 khau) ----------------
def tag(d, x, y, s, col, alpha=1.0, anchor="m", size=40):
    w = tw(d, s, F(size)) + 34
    x0 = x - w / 2 if anchor == "m" else (x if anchor == "l" else x - w)
    card(d, (x0, y - 34, x0 + w, y + 34), fill=A(WHITE, 0.95 * alpha), outline=A(col, alpha), r=18, w=3)
    text(d, (x0 + w / 2, y), s, size, col, alpha=alpha)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    scene_base(d); lamp(d, 1.0); bowl(d, fog=1.0); drop(d, 20)
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · dưới màng, ngay dưới đá"
    pw = tw(d, lab, F(42)) + 60
    card(d, (W / 2 - pw / 2, 1070, W / 2 + pw / 2, 1144), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 1107), lab, 42, WHITE, alpha=ka)
    # 3 khau, hien theo phu de
    k1 = appear(t, 0.8, 0.4); k2 = appear(t, M[1] - 0.6, 0.4); k3 = appear(t, M[1] + 0.6, 0.4)
    if k1 > 0:
        arrow(d, (CX - 170, WL - 10), (CX - 170, RIM + 22), A(ORANGE, k1), w=7, head=20)
        tag(d, CX - 170, WL + 70, "1 bay hơi", ORANGE, alpha=k1)
    if k2 > 0:
        d.line([(CX + 30, DROP_Y + 10), (800, 600)], fill=A(BLUE, 0.7 * k2), width=3)
        tag(d, 1010, 580, f"2 ngưng tụ · ~{T_DA} °C", BLUE, alpha=k2, anchor="r")
    if k3 > 0:
        arrow(d, (CX, DROP_Y + 50), (CX, WL - 6), A(WATER_D, k3), w=7, head=20)
        tag(d, CX + 40, WL + 70, "3 rơi lại", BLUE, alpha=k3, anchor="l")

# ---------------- canh 4: Rut ra (nuoc nguoi + ngoai troi) ----------------
def mini(d, x0, temp, warm, fogk, rr, title_col):
    card(d, (x0, 270, x0 + 470, 820), fill=WHITE, outline=LIGHT, w=3)
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
    if rr > 0:
        y = rim + 30
        d.ellipse([cx - rr, y, cx + rr, y + 2 * rr], fill=WATER_D)
        arrow(d, (cx, y + 2 * rr + 12), (cx, wl - 8), WATER_D, w=5, head=14)
    text(d, (cx, 330), f"nước {temp} °C", 44, title_col)
    return cx

def s_rutra(img, d, t, sc):
    M = sc["M"]
    mini(d, 40, T_NUOC, 1.0, 1.0, 14, ORANGE)
    kb = appear(t, 0.5, 0.5)
    if kb > 0:
        mini(d, 570, T_NGUOI, 0.0, 0.35, 0, BLUE)
    rows = (("màng mờ,", "giọt rơi"), ("hơi mờ,", "chưa có giọt"))
    for j, (l1, l2) in enumerate(rows):
        kk = 1.0 if j == 0 else appear(t, 1.2, 0.4)
        cx = 275 + j * 530
        text(d, (cx, 700), l1, 38, INK, alpha=kk); text(d, (cx, 752), l2, 38, INK, alpha=kk)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y0 = 920 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 470), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        for j, (a_, b_) in enumerate((("đèn", "Mặt Trời"), ("viên đá", "khí lạnh trên cao"))):
            kk = k2 * appear(t, M[1] + 0.4 + 0.9 * j, 0.4)
            yy = y0 + 150 + j * 170
            text(d, (90, yy), a_, 46, INK, anchor="lm", alpha=kk)
            arrow(d, (300, yy), (380, yy), A(DGREEN, kk), w=5, head=16)
            text(d, (410, yy), b_, 46, DGREEN, anchor="lm", alpha=kk)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.1, 0.4) * (1 - k2)
    melt = clamp((t - 0.6) / 1.6)
    # hinh phong to: da tan nam TREN mang, giot DUOI mang (hien ngay tu dau canh)
    scene_base(d); lamp(d, 1.0); bowl(d, fog=1.0, melt=melt, ice=1.0); drop(d, 20)
    kv = appear(t, M[0] + 1.6, 0.4)
    if kv > 0:                    # nhan bac bay giu toi het canh (cong B 18/11)
        text(d, (CX - 320, RIM - 120), "đá tan: trên màng", 42, WATER_D, anchor="lm", alpha=kv)
        text(d, (CX + 50, DROP_Y + 80), "giọt: hơi từ bát", 42, BLUE, anchor="lm", alpha=kv)
    if a1 > 0:
        y0 = 1070
        card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Giọt là đá tan thấm qua màng”"
        ks = clamp((t - M[0] - 1.4) / 0.4)
        f = F(46); lw = tw(d, q, f); yy = y0 + 180
        text(d, (W / 2, yy), q, 46, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2 + lw / 2 + 40, yy), "✗", 46, DRED, alpha=a1 * ks)
    if k2 > 0:
        y0 = 1070 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y0 + 190), "Chưa đo lượng nước", 44, INK, alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
HINT_AT = 4.4                     # goi y hien sau >= 4 s nghi (nhat ky 18/11)
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 262, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 391, "Cần nhiệt, nước mới quay vòng", 50, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1300), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 676), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 643), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    ctext(d, 830, "Hở một góc màng: giọt rơi lại\nnhiều hơn hay ít hơn bọc kín?", 48, INK, maxw=900, alpha=kq)
    kh = appear(t, M[0] + HINT_AT, 0.5)
    if kh > 0:
        card(d, (110, 1070, 970, 1230), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1150, "Hơi nước đi đâu?", 44, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"), (do["t0"] + T_ON, "tap")]
    out += [(do["t0"] + T_ON + i * 0.7, "tick") for i in range(1, 10)]
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.1, "buzz"),
            (b["t0"] + b["M"][0] + 1.4, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-hoathach-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Vòng năng lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bát nước ấm dưới đèn", draw=s_hook, tail=0.8, caps=[
   ("Bọc kín miệng bát, đặt đá lên.", 3.2),
   ("Tự trả lời trước khi xem.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Bật đèn, chờ khoảng 10 phút.", 3.6),
   ("Nhìn kĩ mặt dưới màng.", 3.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Ba khâu thành vòng kín.", 3.2),
   ("Đá làm chỗ đó lạnh nhất.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Thử lại với nước nguội.", 3.0),
   ("Ngoài trời cũng có vòng này.", 3.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Nước đá tan rồi đi đâu?", 4.2),
   ("Còn chưa nói được.", 3.9)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Tự nghĩ, rồi xem gợi ý.", 5.6)]),
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
