# Clip: tn-l10-dt-dctg-01 - Bot khi trong ong nuoc: ve do thi d-t tu bang so lieu, van toc = do doc (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dt-dctg-01.json:
#   tham_so: v = 5 cm/s (mien 1-10, buoc 0,5), vach d = 10..50 cm, t bam tay sai so 0,1 s; dong ho do chia 0,01 s.
#   so_lieu_mau: t doc 2,1 / 3,9 / 6,1 / 7,9 / 10,0 s ; d/t 4,76 / 5,13 / 4,92 / 5,06 / 5,00 cm/s.
#   ket_qua_ky_vong: 0,1 s la ~5 % cua 2,1 s, ~1 % cua 10,0 s ; rut_ra: do doc 30 cm / 6 s = 5 cm/s.
#   Cau chot dung tham_so trong mien cho phep (v = 8 cm/s, vach 50 cm) -> 6,25 s, chua tung hien.
# Truc chinh: do thi d-t tu bang so lieu (khac dotocdo3: cong quang, khac tdvt3: he quy chieu).
# Mau: d = BLUE, t = ORANGE, van toc (d/t, do doc, duong ke) = TEAL, sai so = RED, diem do (t, d) = NAVY.
# Dong ho = thoi gian that; bam tay o dung t doc -> hang bang/diem do hien dung luc dong ho chi so do
#   (bot khi luc do o d = 5 * t doc, lech vach toi 0,5 cm: chinh la sai so bam tay).
# Canh: Du doan dang do thi (K10: chi cau hoi + hinh) -> Tien hanh (tua nhanh 2 lan, chip nhac cau hoi) -> Dap an
#       (thuoc dat doc cac diem) -> Rut ra (duong thang, do doc, chua noi duoc) -> Bay (noi gap khuc) -> Chot + cau hoi.
from engine import *

V = 5.0                                                                    # cm/s (tham_so mac dinh)
ROWS = [(10, 2.0, 2.1, 4.76), (20, 4.0, 3.9, 5.13), (30, 6.0, 6.1, 4.92),
        (40, 8.0, 7.9, 5.06), (50, 10.0, 10.0, 5.00)]                      # so_lieu_mau: d, t tinh, t doc, d/t
WATER = (219, 238, 252); GLASS = (110, 140, 185); STOP = (90, 96, 112); WOOD = (176, 124, 74)
SPEED = 2.0                                                                # tua nhanh 2 lan

def vn(x, nd=None):
    s = (f"{x:.{nd}f}" if nd is not None else f"{x:g}").replace(".", ",")
    return s.replace("-", "−")

# ---------------- ong nuoc nghieng ----------------
P0 = (110, 650); ANG = math.radians(12)
TU = (math.cos(ANG), -math.sin(ANG)); TN = (math.sin(ANG), math.cos(ANG))     # TU: doc ong len phai ; TN: phap tuyen xuong
PXC = 15; S_D0 = 70; S_END = 880; HT = 26
def TP(s, h): return (P0[0] + TU[0] * s + TN[0] * h, P0[1] + TU[1] * s + TN[1] * h)
def S_OF(dcm): return S_D0 + dcm * PXC

def tube(d, dbub, flash=None):
    """Ong + vach + bot khi o vi tri dbub (cm, tinh tu vach 0). flash: {vach: do sang 0..1} to cam vach vua bam."""
    lo = TP(20, HT); d.rectangle([lo[0] - 26, lo[1], lo[0] + 26, 715], fill=WOOD)       # gia do
    hi = TP(760, HT); d.rectangle([hi[0] - 14, hi[1] - 4, hi[0] + 14, 715], fill=WOOD)
    d.polygon([TP(0, -HT), TP(S_END, -HT), TP(S_END, HT), TP(0, HT)], fill=WATER)
    for s0, s1 in ((-16, 0), (S_END, S_END + 16)):                          # nut kin hai dau
        d.polygon([TP(s0, -HT - 4), TP(s1, -HT - 4), TP(s1, HT + 4), TP(s0, HT + 4)], fill=STOP)
    d.line([TP(0, -HT), TP(S_END, -HT)], fill=GLASS, width=5)
    d.line([TP(0, HT), TP(S_END, HT)], fill=GLASS, width=5)
    for k in range(6):
        dm = k * 10; s = S_OF(dm); fk = (flash or {}).get(dm, 0.0)
        d.line([TP(s, -HT), TP(s, 6)], fill=mix(INK, ORANGE, fk), width=5 + int(4 * fk))
        if fk > 0.5:
            cc = TP(s, -HT + 10); d.ellipse([cc[0] - 34, cc[1] - 34, cc[0] + 34, cc[1] + 34], outline=ORANGE, width=5)
        lb = TP(s, HT + 40)
        text(d, (lb[0] + (18 if k == 5 else 0), lb[1]), f"{dm} cm" if k == 5 else str(dm), 38, BLUE)
    # bot khi: elip dep sat thanh tren cua ong
    c = TP(S_OF(dbub), -HT + 15); a, b = 26, 11
    pts = [(c[0] + TU[0] * a * math.cos(u) + TN[0] * b * math.sin(u),
            c[1] + TU[1] * a * math.cos(u) + TN[1] * b * math.sin(u)) for u in [i * math.pi / 18 for i in range(36)]]
    d.polygon(pts, fill=WHITE, outline=GLASS)
    d.line(pts + [pts[0]], fill=GLASS, width=3)
    hl = (c[0] - 8, c[1] - 3); d.ellipse([hl[0] - 5, hl[1] - 3, hl[0] + 5, hl[1] + 3], fill=(200, 225, 250))

def stopwatch(d, clock, note=None):
    card(d, (60, 360, 420, 470), fill=WHITE, outline=ORANGE, r=22, w=4)
    text(d, (240, 415), vn(clock, 2) + " s", 56, ORANGE)
    if note:
        text(d, (240, 505), note, 40, INK)
        text(d, (445, 415), "bấm tay lệch ≤ 0,1 s", 40, INK, anchor="lm")

# ---------------- bang ngang + do thi (truc co dinh ca clip) ----------------
CX = (340, 495, 650, 805, 960)
def htable(d, y, n_t, n_v=0, ys=(0, 115, 230), labx=165):
    """Hang d (BLUE), t (ORANGE), d/t (TEAL). n_t: so o t da co; n_v: so o d/t da co (None = khong ve hang)."""
    text(d, (labx, y + ys[0]), "d (cm)", 40, BLUE)
    text(d, (labx, y + ys[1]), "t (s)", 40, ORANGE)
    if n_v is not None: text(d, (labx, y + ys[2]), "d/t (cm/s)", 36, TEAL)
    for i, (dm, tt, td, vv) in enumerate(ROWS):
        text(d, (CX[i], y + ys[0]), str(dm), 46, BLUE)
        text(d, (CX[i], y + ys[1]), vn(td, 1) if i < n_t else "?", 46, ORANGE if i < n_t else GRAY)
        if n_v is not None and i < n_v: text(d, (CX[i], y + ys[2]), vn(vv, 2), 46, TEAL)

GX0, GX1, GYB, GYT = 170, 975, 1205, 800
def X(t): return GX0 + t / 11 * (GX1 - GX0)
def Y(dm): return GYB - dm / 55 * (GYB - GYT)
def axes(d):
    card(d, (40, 735, 1040, 1290), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GYB), (GX1 + 25, GYB)], fill=NAVY, width=5)
    d.line([(GX0, GYB), (GX0, GYT - 30)], fill=NAVY, width=5)
    for tt in (2, 4, 6, 8, 10):
        d.line([(X(tt), GYB), (X(tt), GYB + 10)], fill=NAVY, width=3)
        text(d, (X(tt), GYB + 40), str(tt), 36, INK, bold=False)
    for dm in (10, 20, 30, 40, 50):
        d.line([(GX0 - 10, Y(dm)), (GX0, Y(dm))], fill=NAVY, width=3)
        d.line([(GX0, Y(dm)), (GX1, Y(dm))], fill=(242, 238, 230), width=2)
        text(d, (GX0 - 18, Y(dm)), str(dm), 36, INK, bold=False, anchor="rm")
    text(d, (1015, GYB - 38), "t (s)", 38, ORANGE, anchor="rm")
    text(d, (GX0 + 22, GYT - 22), "d (cm)", 38, BLUE, anchor="lm")
    text(d, (GX0 - 18, GYB + 6), "0", 36, INK, bold=False, anchor="rm")

def points(d, n, alpha=1.0, pop=None):
    for i in range(n):
        dm, tt, td, vv = ROWS[i]
        k = 1.0 if pop is None else back(clamp(pop[i]))
        if k > 0: dot(d, X(td), Y(dm), 14 * k, A(NAVY, alpha), WHITE)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 730), fill=WHITE, outline=LIGHT, w=3)
    tube(d, -4)
    stopwatch(d, 0.0)
    card(d, (40, 755, 1040, 985), fill=WHITE, outline=LIGHT, w=3)
    htable(d, 815, 0, None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 570), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 160, "Bọt khí đi lên trong ống.", 44, INK, maxw=900, alpha=a)
    ctext(d, y0 + 225, "Chấm các điểm (t, d) ở vạch 10–50 cm.", 44, INK, maxw=900, alpha=a)
    ctext(d, y0 + 360, "Đồ thị d–t có dạng nào?", 52, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 514], radius=7, fill=A(LIGHT, a))
        if p < 1: d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 514], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
RUN0 = 0.6                                       # giay trong canh luc bot khi qua vach 0 (dong ho bat dau)
def tau(t): return (t - RUN0) * SPEED            # thoi gian that (s) tinh tu vach 0
def bub(t): return clamp(max(V * tau(t), -4.0) if t >= 0.2 else -4.0, -4.0, 53.0)
def clock(t): return clamp(math.floor(tau(t) * 100 + 1e-6) / 100, 0.0, ROWS[-1][2])
def n_done(t): return sum(1 for r in ROWS if clock(t) >= r[2] - 1e-9)
def lap_at(i): return RUN0 + ROWS[i][2] / SPEED  # giay trong canh luc bam vach i

def chip(d, y=290):
    card(d, (60, y, 1020, y + 56), fill=(245, 243, 255), outline=PURPLE, r=24, w=3)
    text(d, (W / 2, y + 28), "Câu hỏi: đồ thị d–t có dạng nào?", 36, PURPLE)

def s_do(img, d, t, sc):
    card(d, (40, 265, 1040, 730), fill=WHITE, outline=LIGHT, w=3)
    chip(d)
    fl = {}
    for i, r in enumerate(ROWS):
        dt_ = t - lap_at(i)
        if 0 <= dt_ < 0.6: fl[r[0]] = 1.0 if int(dt_ / 0.15) % 2 == 0 else 0.25    # nhap nhay dung luc bam (tap)
    tube(d, bub(t), fl)
    stopwatch(d, clock(t), "tua nhanh ×2")
    axes(d)
    nd = n_done(t)
    points(d, nd, pop=[(t - lap_at(i)) / 0.4 for i in range(5)])
    card(d, (40, 1315, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    for i in range(nd):
        if t - lap_at(i) < 0.8:
            d.rounded_rectangle([CX[i] - 72, 1340, CX[i] + 72, 1565], radius=18, outline=ORANGE, width=4)
    htable(d, 1395, nd, None)

# ---------------- canh 3: Dap an (diem gan mot duong thang) ----------------
def mini(d, box, kind, on, alpha=1.0):
    """Bon dang do thi nho (khong chu cai): line / curve / flat / zigzag; on = dang dung (vien dam)."""
    x0, y0, x1, y1 = box; col = NAVY if on else (205, 205, 215)
    card(d, box, fill=A(WHITE, alpha), outline=A(col, alpha), r=18, w=6 if on else 3)
    ox, oy, wx, hy = x0 + 26, y1 - 26, x1 - x0 - 52, y1 - y0 - 52
    d.line([(ox, oy), (ox + wx, oy)], fill=A(INK, alpha), width=3); d.line([(ox, oy), (ox, oy - hy)], fill=A(INK, alpha), width=3)
    if kind == "line": pts = [(ox, oy), (ox + wx, oy - hy)]
    elif kind == "curve": pts = [(ox + wx * u / 10, oy - hy * (u / 10) ** 2) for u in range(11)]
    elif kind == "flat": pts = [(ox, oy - hy * 0.5), (ox + wx, oy - hy * 0.5)]
    else: pts = [(ox, oy), (ox + wx * 0.3, oy - hy * 0.55), (ox + wx * 0.55, oy - hy * 0.4), (ox + wx, oy - hy)]
    d.line(pts, fill=A(TEAL if on else GRAY, alpha), width=7 if on else 5)

def ruler(d, k):
    """Thuoc ke trong dat doc cac diem: dai mo qua goc, doc 5 cm/s (truc giua = duong d = 5t)."""
    if k <= 0: return
    t1 = 10.6 * k; a = math.atan2(Y(V * t1) - Y(0), X(t1) - X(0)); nx, ny = -math.sin(a) * 22, math.cos(a) * 22
    p0, p1 = (X(0), Y(0)), (X(t1), Y(V * t1))
    d.polygon([(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)],
              fill=(150, 155, 170, 70))

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · gần một đường thẳng"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 318), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 284), lb, 40, WHITE, alpha=ka)
    for j, kind in enumerate(("line", "curve", "flat", "zigzag")):
        x0 = 60 + j * 245
        mini(d, (x0, 370, x0 + 225, 560), kind, kind == "line", alpha=1.0 if kind == "line" else 0.6)
    km = appear(t, 0.6, 0.4)
    text(d, (W / 2, 640), "thẳng, qua gốc", 44, TEAL, alpha=km)
    axes(d)
    ruler(d, ease((t - M[0] - 0.4) / 1.2))
    points(d, 5)
    card(d, (40, 1305, 1040, 1595), fill=WHITE, outline=LIGHT, w=3)
    nv = sum(1 for i in range(5) if t >= M[1] + 0.2 + 0.3 * i)
    htable(d, 1365, 5, nv, ys=(0, 85, 170))

# ---------------- canh 4: Rut ra ----------------
def slope_tri(d, k):
    """Tam giac do doc tren duong d = 5t: tu (2 s; 10 cm) toi (8 s; 40 cm)."""
    if k <= 0: return
    xa, ya, xb, yb = X(2), Y(10), X(8), Y(40)
    for i in range(14):                                             # net dut ngang (Delta t, cam)
        u0, u1 = i / 14, (i + 0.55) / 14
        if u0 < k: d.line([(xa + (xb - xa) * u0, ya), (xa + (xb - xa) * min(u1, k), ya)], fill=ORANGE, width=6)
    k2 = clamp(k * 2 - 1)
    for i in range(10):                                             # net dut dung (Delta d, xanh duong)
        u0, u1 = i / 10, (i + 0.55) / 10
        if u0 < k2: d.line([(xb, ya + (yb - ya) * u0), (xb, ya + (yb - ya) * min(u1, k2))], fill=BLUE, width=6)
    text(d, ((xa + xb) / 2, ya + 44), "Δt = 6 s", 40, ORANGE, alpha=clamp(k * 2))
    text(d, (xb + 22, (ya + yb) / 2 + 30), "Δd = 30 cm", 40, BLUE, anchor="lm", alpha=k2)

def fit_line(d, k, alpha=1.0):
    if k <= 0: return
    t1 = 10.6 * k
    d.line([(X(0), Y(0)), (X(t1), Y(V * t1))], fill=A(TEAL, alpha), width=7)

def s_rutra(img, d, t, sc):
    M = sc["M"]
    axes(d); fit_line(d, ease((t - 0.3) / 1.2)); points(d, 5)
    slope_tri(d, clamp((t - M[1] - 0.2) / 1.2))
    k0 = appear(t, M[0] + 1.4, 0.5)
    card(d, (40, 265, 1040, 710), fill=A(WHITE, k0), outline=A(TEAL, k0), w=5)
    ctext(d, 350, "Đường thẳng → đi thẳng đều", 44, INK, maxw=920, alpha=k0)
    k1 = appear(t, M[1] + 1.4, 0.5)
    d.line([(90, 420), (990, 420)], fill=A(LIGHT, k1), width=3)
    text(d, (W / 2, 505), "v = Δd / Δt = 30 cm / 6 s", 52, TEAL, alpha=k1)
    text(d, (W / 2, 615), "= 5 cm/s", 56, TEAL, alpha=appear(t, M[1] + 2.0, 0.5))
    k2 = appear(t, M[2] - 0.1, 0.45)
    if k2 <= 0: return
    y0 = 1315 + (1 - k2) * 30
    card(d, (40, y0, 1040, y0 + 275), fill=A((254, 242, 242), k2), outline=A(NAVY, k2), w=5)
    text(d, (W / 2, y0 + 60), "Chưa nói được", 42, NAVY, alpha=k2)
    kk = k2 * appear(t, M[2] + 0.3, 0.4)
    text(d, (W / 2, y0 + 140), "Mới thử một độ nghiêng.", 44, RED, alpha=kk)
    text(d, (W / 2, y0 + 210), "Nghiêng hơn thì v ra sao?", 44, RED, alpha=kk)

# ---------------- canh 5: Bay (phong to quanh diem vach 20 cm) ----------------
ZI, ZK = 1, 10.0                                      # diem phong to (3,9 s; 20 cm), he so phong to
def inset(d, k_line):
    """Kinh lup 992 x 170 tai (44, 1358): cung ti le x/y nhu do thi chinh, phong to ZK lan quanh diem vach 20 cm.
    Goc gap cua duong do chi ~5 do (d/t lech +-10 %) -> khong lam lo ra duoc ma khong meo hinh; thay bang khoang
    cach ngang 0,1 s tu diem toi duong thang (tham_so sai_so_do)."""
    sub = Image.new("RGB", (992, 170), WHITE); sd = ImageDraw.Draw(sub, "RGBA")
    old = IMG_REF[0]; IMG_REF[0] = sub
    sx, sy = (GX1 - GX0) / 11 * ZK, (GYB - GYT) / 55 * ZK            # px/s, px/cm
    tc, dc = ROWS[ZI][2], ROWS[ZI][0]
    P = lambda tt, dm: (496 + (tt - tc) * sx, 85 - (dm - dc) * sy)
    seg = [(ROWS[ZI - 1][2], ROWS[ZI - 1][0]), (tc, dc), (ROWS[ZI + 1][2], ROWS[ZI + 1][0])]
    sd.line([P(*q) for q in seg], fill=RED, width=7)
    if k_line > 0: sd.line([P(0, 0), P(10.6 * k_line, V * 10.6 * k_line)], fill=TEAL, width=8)
    dot(sd, *P(tc, dc), 16, NAVY, WHITE)
    if k_line > 0.5:                                                    # khoang lech 0,1 s (mau t = cam)
        ka = clamp((k_line - 0.5) * 3)
        xa, xb = P(tc, dc)[0] + 18, P(dc / V, dc)[0] - 6
        sd.line([(xa, 85), (xb, 85)], fill=A(ORANGE, ka), width=5)
        for xx in (xa, xb): sd.line([(xx, 72), (xx, 98)], fill=A(ORANGE, ka), width=5)
        text(sd, ((xa + xb) / 2 + 15, 138), "0,1 s", 38, ORANGE, alpha=ka)
    IMG_REF[0] = old
    return sub

def s_bay(img, d, t, sc):
    M = sc["M"]
    axes(d)
    a1 = appear(t, 0.15, 0.4)
    pts = [(X(0), Y(0))] + [(X(r[2]), Y(r[0])) for r in ROWS]
    ks = clamp((t - 2.2) / 0.4)
    d.line(pts, fill=A(RED, a1), width=6)
    kl = ease((t - 2.6) / 0.8)
    fit_line(d, kl)
    points(d, 5)
    kr = appear(t, 0.6, 0.4)
    px, py = X(ROWS[ZI][2]), Y(ROWS[ZI][0])
    if kr > 0:
        d.ellipse([px - 34, py - 34, px + 34, py + 34], outline=A(RED, kr), width=6)
        d.line([(px, py + 34), (px, GYB - 4)], fill=A(RED, kr), width=4)          # ngat qua nhan truc t
        d.line([(px, GYB + 66), (px, 1305)], fill=A(RED, kr), width=4)
    card(d, (40, 265, 1040, 710), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 295, W / 2 + pw / 2, 359), fill=A(RED, a1), r=32)
    text(d, (W / 2, 327), "BẪY", 38, WHITE, alpha=a1)
    q = "Nối từng điểm thành gấp khúc"
    f = F(46); lw = tw(d, q, f); yy = 460
    text(d, (W / 2, yy), q, 46, mix(RED, MUTED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
    kk = appear(t, 2.6, 0.5)
    text(d, (W / 2, 600), "Đúng: một đường thẳng", 42, TEAL, alpha=kk)
    ki = appear(t, 0.9, 0.45)
    if ki > 0:
        card(d, (40, 1305, 1040, 1595), fill=A(WHITE, ki), outline=A(RED, ki), w=4)
        sub = inset(d, kl)
        m = Image.new("L", sub.size, 0); ImageDraw.Draw(m).rectangle([0, 0, 991, 169], fill=int(255 * ki))
        img.paste(sub, (44, 1358), m)
        text(d, (W / 2, 1335), f"phóng to ×{ZK:g}", 38, INK, alpha=ki)
        text(d, (W / 2, 1560), "Điểm lệch nhỏ: do bấm giờ tay", 40, RED, alpha=appear(t, 3.2, 0.5))

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):                       # goi y tu ve, hien tre ~3,6 s (cong B lo 31/10)
        kh = appear(t, M[0] + 3.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1200, 970, 1340), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1270), "Đáp số ghi tới 0,01 s", 44, ORANGE, alpha=kh)
    def body(d, t, k):                       # khoi cau hoi + goi y canh giua the Thu nghi (y 714-1600)
        ctext(d, 1040, HOI, 46, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
        hint(d, t, k)
    chot_hoi(d, t, sc, "Đồ thị d–t thẳng: độ dốc là vận tốc", "", None, body=body)

HOI = "Bọt khác đi lên đều 8 cm/s. Từ vạch 0 đến 50 cm mất mấy giây?"

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for i in range(5): cs.append((do["t0"] + lap_at(i), "tap"))             # moi lan bam dong ho
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 0.2, "tap"),
           (b["t0"] + 0.15, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-dt-dctg-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Đồ thị độ dịch chuyển – thời gian · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bọt khí trong ống nước", draw=s_hook, tail=0.7, caps=[
   "Ống nước nghiêng.",
   ("Dừng video, chọn câu trả lời.", 6.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Bấm giờ khi bọt qua từng vạch.", 4.4),
   ("Mỗi lần bấm: thêm một điểm.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Đặt thước dọc các điểm.", 3.0),
   ("d/t lệch quanh 5 cm/s: do bấm tay.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Kẻ một đường thẳng.", 2.9),
   ("Độ dốc là vận tốc.", 3.0),
   ("Còn điều chưa biết.", 3.2)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.5, caps=[
   ("Nhìn kính lúp.", 4.9)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.2, caps=[
   ("Tự trả lời.", 5.8)]),
])
