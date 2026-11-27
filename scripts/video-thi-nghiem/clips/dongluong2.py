# Clip: tn-l10-dongluong-02 - Bi lan tu mang nghieng va vao khuc go (31/10/2026;
# dung lai 27/11/2026 theo cong moi L10b: chu >= 55 px khi ve, K10 khong nut A-D, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dongluong-02.json (_kiem_so() doi chieu):
#   so_lieu_mau m (kg) / h (m) / v (m/s) / p (kg.m/s): 0,05/0,1/1,18/0,059 ; 0,05/0,2/1,67/0,084 ;
#   0,1/0,1/1,18/0,118 ; 0,1/0,2/1,67/0,167.  tham_so: m 0,02-0,2 kg, h 0,05-0,3 m ; mo_hinh v = sqrt(10gh/7).
#   Quang go di: kho chi dinh tinh -> ve tang theo p, KHONG ghi so.
# Du doan (giu, = goi_y_mo_phong.diem_nhan): bi 50 g tha 20 cm hay bi 100 g tha 10 cm day go xa hon? -> 100 g.
#   Khong trung cau Mo bai (nguoi tren bang, khong so) va Tu kiem tra Cau 1 (hanh khach tren tau).
# Ket qua: lan 2 / lan 3 (cung m.h, khac p: gia_thiet mo hinh) ; m gap doi -> p gap doi ; p = m.v.
# Bay = hien_tuong_hay_sai[1]: "nang gap doi thi lan nhanh gap doi" -> cung 10 cm, ca hai v = 1,18 m/s.
#   Chua noi duoc: quang go di ti le the nao voi p (ghi_chu: dinh tinh).
# Cau chot (tham_so trong mien): bi 200 g tha 5 cm vs bi 50 g tha 20 cm (cung m.h) -> v 0,837 / 1,67 m/s,
#   p 0,167 / 0,084: bi 200 g day xa hon, p gap doi. Buoc "h giam 4 lan -> v giam 2 lan" chua chieu.
from engine import *

ROWS = [("0,05", "0,1", "1,18", "0,059"), ("0,05", "0,2", "1,67", "0,084"),
        ("0,1", "0,1", "1,18", "0,118"), ("0,1", "0,2", "1,67", "0,167")]          # so_lieu_mau
RUNS = [(50, 10, 0.059), (50, 20, 0.084), (100, 10, 0.118), (100, 20, 0.167)]       # (g, cm, p)
CHOT = ((200, 5), (50, 20))

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-dongluong-02.json")))
    for r, h in zip(ROWS, k["so_lieu_mau"]["hang"]):
        assert [float(x.replace(",", ".")) for x in r] == h, ("lech kho", r)
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    for g, cm in CHOT: assert ts["m"]["min"] <= g / 1000 <= ts["m"]["max"] and ts["h"]["min"] <= cm / 100 <= ts["h"]["max"]
    v = lambda h: math.sqrt(10 * 9.8 * h / 7)
    assert round(v(0.1), 2) == 1.18 and round(v(0.2), 2) == 1.67
    pa, pb = 0.2 * v(0.05), 0.05 * v(0.2); assert abs(pa / pb - 2) < 1e-9
_kiem_so()

DRED = (185, 28, 28); NOTE = (60, 64, 84); DGREEN = (21, 110, 55); EMPTY = (148, 140, 128)
WOOD = (222, 184, 135); WOOD_D = (150, 105, 60)
RAMP = (226, 232, 240); RAMP_D = (100, 116, 139)
STEEL = (148, 163, 184); STEEL_D = (71, 85, 105)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------- hinh hoc mang (toa do cuc bo, chan mang o (0,0), y huong xuong) ----------
TOPX, TOPY = -480, -340
SL = math.hypot(TOPX, TOPY); UX, UY = -TOPX / SL, -TOPY / SL
NX, NY = UY, -UX
PXCM = 15                                                         # 1 cm do cao = 15 px
XB, BW, BH = 60, 130, 110
ACC = 1038.0
DMAX = 280
SLIDE = 0.9
def rad(g): return {50: 22, 100: 28, 200: 35}[g]                  # r ti le can bac 3 cua m
def dist(p): return DMAX * p / 0.167

def surf(hcm):
    hp = hcm * PXCM; return (TOPX * hp / -TOPY, -hp)

def ball_path(hcm, r, tau):
    sx, sy = surf(hcm); x0, y0 = sx + r * NX, sy + r * NY
    L = (-r - y0) / UY
    t1 = math.sqrt(2 * L / ACC); v1 = ACC * t1
    x1 = x0 + L * UX; Lh = (XB - r) - x1; t2 = Lh / v1; ti = t1 + t2
    if tau <= 0: return x0, y0, False, ti
    if tau < t1:
        s = 0.5 * ACC * tau * tau; return x0 + s * UX, y0 + s * UY, False, ti
    if tau < ti: return x1 + v1 * (tau - t1), -r, False, ti
    return XB - r, -r, True, ti

def slide(tau_after, D):
    u = clamp(tau_after / SLIDE); return D * (1 - (1 - u) ** 2)

def P(O, s, x, y): return (O[0] + x * s, O[1] + y * s)

def rig(d, O, s, marks=(10, 20), floor_r=540, alpha=1.0, block_dx=None, loff=80):
    c = lambda col: A(col, alpha)
    tri = [P(O, s, TOPX, TOPY), P(O, s, 0, 0), P(O, s, TOPX, 0)]
    d.polygon(tri, fill=c(RAMP)); d.line(tri + [tri[0]], fill=c(RAMP_D), width=max(3, int(5 * s)))
    d.line([P(O, s, TOPX - 20, 0), P(O, s, floor_r, 0)], fill=c(NAVY), width=max(4, int(6 * s)))
    for hcm in marks:
        sx, sy = surf(hcm)
        d.line([P(O, s, sx, sy), P(O, s, sx - 26 * NX, sy - 26 * NY)], fill=c(NAVY), width=4)
        xa, ya = P(O, s, sx, sy); xb = P(O, s, TOPX, sy)[0]
        for k in range(int(abs(xa - xb) // 24) + 1):
            x1 = xa - k * 24 if xa > xb else xa + k * 24
            d.line([(x1, ya), (x1 - 12 if xa > xb else x1 + 12, ya)], fill=c(NAVY), width=3)
        lx, ly = P(O, s, sx + loff / s * NX - 30, sy + loff / s * NY)
        text(d, (lx, ly), f"{hcm} cm", 56, NAVY, alpha=alpha)
    if block_dx is not None:
        x0 = XB + block_dx
        d.rectangle([P(O, s, x0, -BH), P(O, s, x0 + BW, 0)], fill=c(WOOD), outline=c(WOOD_D), width=max(3, int(4 * s)))

def ball(d, O, s, x, y, r, alpha=1.0):
    cx, cy = P(O, s, x, y); R = r * s
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A(STEEL, alpha), outline=A(NAVY, alpha), width=4)
    d.ellipse([cx - R * 0.55, cy - R * 0.6, cx - R * 0.1, cy - R * 0.15], fill=A(WHITE, alpha * 0.8))

def mini(d, O, g, hcm, s=0.6, tau=None, lab2=None, col=INK):
    """Mang nho: bi g gam o do cao hcm (dung yen, hoac lan theo tau)."""
    rig(d, O, s, marks=(), floor_r=380, block_dx=0 if tau is None else None)
    r = rad(g) * 1.4
    if tau is None:
        sx, sy = surf(hcm); x, y = sx + r * NX, sy + r * NY
    else:
        x, y, hit, _ = ball_path(hcm, r, tau)
    ball(d, O, s, x, y, r)
    text(d, (O[0] + 330, O[1] - 150), f"Bi {g} g", 58, col)
    text(d, (O[0] + 330, O[1] - 75), lab2 or f"thả từ {hcm} cm", 56, col)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    mini(d, (420, 560), 50, 20)
    mini(d, (420, 870), 100, 10)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 965 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Lần thả nào đẩy", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "khúc gỗ đi xa hơn?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 410, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (4 lan tha) ----------------
OD = (450, 820); SD = 0.8; DMAX_DO = 420
R0, RGAP = 0.5, 1.7
XS = (120, 300, 480, 680, 900)

def run_state(i, t):
    g, hcm, p = RUNS[i]; r = rad(g); tau = t - (R0 + RGAP * i)
    x, y, hit, ti = ball_path(hcm, r, tau)
    gd = slide(tau - ti, dist(p) * DMAX_DO / DMAX) if hit else 0.0
    return x, y, r, gd, hit, tau >= ti + SLIDE

def s_do(img, d, t, sc):
    card(d, (40, 265, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    cur = max(0, min(3, int((t - R0) // RGAP))) if t >= R0 else 0
    x, y, r, gd, hit, done = run_state(cur, t)
    rig(d, OD, SD, floor_r=720, block_dx=gd, loff=100)
    for i in range(4):                                            # vach noi go dung cua cac lan da xong
        if not run_state(i, t)[5]: continue
        X = OD[0] + SD * (XB + BW + dist(RUNS[i][2]) * DMAX_DO / DMAX)
        d.line([(X, OD[1] + 6), (X, OD[1] + 34)], fill=INK, width=5)
        d.line([(X, OD[1] + 34), (X, OD[1] + 40 + 60 * (i % 2))], fill=INK, width=3)
        text(d, (X, OD[1] + 75 + 60 * (i % 2)), str(i + 1), 56, INK)
    ball(d, OD, SD, x, y, r)
    text(d, (1010, 330), "h: độ cao, 10 cm = 0,1 m", 56, NAVY, anchor="rm")
    text(d, (1010, 410), "gỗ nặng hơn bi nhiều", 56, WOOD_D, anchor="rm")
    y = 990
    card(d, (40, y, 1040, y + 600), fill=WHITE, outline=LIGHT, w=3)
    for xx, lab, unit in zip(XS, ("Lần", "m", "h", "v", "p"), ("", "kg", "m", "m/s", "kg·m/s")):
        text(d, (xx, y + 55), lab, 58, INK)
        if unit: text(d, (xx, y + 118), unit, 56, NOTE, bold=False)
    d.line([(70, y + 160), (1010, y + 160)], fill=LIGHT, width=3)
    text(d, (W / 2, y + 555), "v: tốc độ chân máng · p: động lượng", 56, NOTE)
    for i, row in enumerate(ROWS):
        if t < R0 + RGAP * i: continue
        yy = y + 215 + i * 86
        if i == cur and not run_state(i, t)[5]:
            d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=18, fill=(239, 246, 255))
        text(d, (XS[0], yy), str(i + 1), 58, INK)
        text(d, (XS[1], yy), row[0], 58, NAVY); text(d, (XS[2], yy), row[1], 58, NAVY)
        if run_state(i, t)[4]:
            text(d, (XS[3], yy), row[2], 58, BLUE); text(d, (XS[4], yy), row[3], 58, BLUE)

# ---------------- canh 3: Ket qua ----------------
def s_kq(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 700), fill=WHITE, outline=LIGHT, w=3)
    for j, (n, g, cm, p, col) in enumerate(((2, 50, 20, 0.084, NOTE), (3, 100, 10, 0.118, ORANGE))):
        yy = 345 + j * 190
        text(d, (80, yy), f"Lần {n}: {g} g, {cm} cm", 58, col, anchor="lm")
        L = 4200 * p * ease((t - 0.5 - 0.4 * j) / 0.6)
        if L > 0: d.rounded_rectangle([80, yy + 50, 80 + L, yy + 110], radius=14, fill=col)
        text(d, (80 + 4200 * p + 30, yy + 80), f"{p:.3f} kg·m/s".replace(".", ","), 56, col, anchor="lm")
    ka = appear(t, M[1] - 0.1, 0.45)
    if ka > 0:
        card(d, (40, 740, 1040, 1100), fill=A(WHITE, ka), outline=A(NAVY, ka), w=4)
        text(d, (W / 2, 810), "cùng h = 10 cm", 56, NOTE, alpha=ka)
        text(d, (W / 2, 910), "m: 0,05 → 0,1 kg", 60, NAVY, alpha=ka)
        text(d, (W / 2, 1010), "p: 0,059 → 0,118 kg·m/s", 60, BLUE, alpha=ka)
    kb = appear(t, M[2] - 0.1, 0.45)
    if kb > 0:
        card(d, (40, 1220, 1040, 1520), fill=A((239, 246, 255), kb), outline=A(BLUE, kb), w=5)
        text(d, (W / 2, 1310), "p = m · v", 72, BLUE, alpha=kb)
        text(d, (W / 2, 1420), "khả năng truyền chuyển động", 58, INK, alpha=kb)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.3, 0.45)
    card(d, (40, 265, 1040, 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 335, "BẪY", RED, a1)
    q = "“Nặng gấp đôi, lăn nhanh gấp đôi”"
    ks = clamp((t - M[1]) / 0.4); lw = tw(d, q, F(58)); yy = 470
    text(d, (W / 2, yy), q, 58, mix(INK, DRED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
    kk = appear(t, M[1] + 0.1, 0.45)
    if kk > 0:
        card(d, (40, 640, 1040, 1230), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
        tau = t - M[1] - 0.6
        mini(d, (380, 900), 50, 10, s=0.55, tau=tau, lab2="v = 1,18 m/s", col=DGREEN)
        mini(d, (380, 1170), 100, 10, s=0.55, tau=tau, lab2="v = 1,18 m/s", col=DGREEN)
    k5 = appear(t, M[2] + 0.1, 0.45)
    if k5 > 0:
        y0 = 1270 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 370), fill=A(WHITE, k5), outline=A(NAVY, k5), w=6)
        pill(d, W / 2, y0 + 70, "CHƯA NÓI ĐƯỢC", NAVY, k5)
        text(d, (W / 2, y0 + 190), "quãng gỗ đi tỉ lệ", 60, INK, alpha=k5)
        text(d, (W / 2, y0 + 285), "thế nào với p", 60, INK, alpha=k5)

# ---------------- canh 5: THU NGHI (cau chot o khung web: bi 200 g, p gap doi) ----------------
def s_end(img, d, t, sc):
    card(d, (40, 265, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    mini(d, (420, 560), 200, 5)
    mini(d, (420, 870), 50, 20)
    y0 = 965
    card(d, (40, y0, 1040, 1665), fill=WHITE, outline=ORANGE, w=6)
    pill(d, W / 2, y0 + 70, "THỬ NGHĨ", ORANGE)
    k1 = appear(t, 2.6, 0.45)
    text(d, (W / 2, y0 + 195), "Cùng máng, cùng khúc gỗ.", 60, INK, alpha=k1)
    k2 = appear(t, 5.0, 0.45)
    text(d, (W / 2, y0 + 300), "Bi nào đẩy gỗ xa hơn?", 62, ORANGE, alpha=k2)
    seg_bar(d, y0 + 370, t, 5.2, sc["T"] - 0.2, ORANGE, k2)
    kh = appear(t, 7.5, 0.45)
    if kh > 0:
        card(d, (90, y0 + 475, 990, y0 + 680), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, y0 + 530), "Gợi ý", 56, INK, alpha=kh)
        text(d, (W / 2, y0 + 620), "tính v từng bi rồi so", 58, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, b, e = sc["hook"], sc["do"], sc["kq"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for i, (g, hcm, p) in enumerate(RUNS):
        out.append((do["t0"] + R0 + RGAP * i + ball_path(hcm, rad(g), 0)[3], "tap"))
    out += [(kq["t0"] + 0.4, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 5.0, "open")]
    return out

CLIP = dict(id="tn-l10-dongluong-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Động lượng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bi lăn va khúc gỗ", draw=s_hook, tail=0.3, caps=[
   ("Cùng khúc gỗ, hai cách thả.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.9, caps=[
   ("Đánh dấu chỗ gỗ dừng.", 3.4),
   ("Đổi bi, độ cao.", 3.4)]),
 dict(key="kq", title="Kết quả", draw=s_kq, tail=0.3, caps=[
   ("Đáp án: bi 100 g, 10 cm.", 3.4),
   ("Nặng gấp đôi, p gấp đôi.", 3.4),
   ("Gộp lại: p = m·v.", 3.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.0),
   ("Sai: cùng độ cao, cùng v.", 4.0),
   ("Thí nghiệm này còn thiếu gì?", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Hai bi mới.", 4.6),
   ("Dừng lại, tự so.", 4.8)]),
])
