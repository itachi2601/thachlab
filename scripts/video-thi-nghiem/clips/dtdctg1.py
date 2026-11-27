# Clip: tn-l10-dt-dctg-01 - Bot khi trong ong nuoc: ve do thi d-t tu bang so lieu, van toc = do doc (31/10/2026;
# dung lai 27/11/2026 theo cong moi viec 4: --do-chu 0 LOI, chu >= 56 px khi ve, Bay hai khung co nhan, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dt-dctg-01.json (_kiem_so() doi chieu):
#   tham_so: v = 5 cm/s (mien 1-10, buoc 0,5), vach d = 10..50 cm, t bam tay sai so 0,1 s.
#   so_lieu_mau (d, t tinh, t doc, d/t): 10 2,0 2,1 | 20 4,0 3,9 | 30 6,0 6,1 | 40 8,0 7,9 | 50 10,0 10,0.
#   rut_ra: do doc 30 cm / 6 s = 5 cm/s.
# Du doan (K10: khong nut A-D): cham cac diem (t, d) -> do thi d-t dang nao? -> gan mot duong thang qua goc.
# Bay = hien_tuong_hay_sai "noi gap khuc": hai khung phong to x10 quanh diem vach 20 cm xep tren duoi (gap khuc / duong thang,
#   khoang lech 0,1 s = tham_so sai_so_do). Chua noi duoc: gia_thiet "mot do nghieng" -> nghieng hon thi v ra sao.
# Thu nghi (= cau_chot khung web, theo mo hinh d = v.t, v trong mien tham_so): do thi qua goc va (2 s; 8 cm) ->
#   v = 4 cm/s -> qua vach 50 cm luc 12,5 s (ngoai thang dong ho 0-10 s cua clip, khong thoang hien).
from engine import *

V = 5.0
ROWS = [(10, 2.0, 2.1, 4.76), (20, 4.0, 3.9, 5.13), (30, 6.0, 6.1, 4.92),
        (40, 8.0, 7.9, 5.06), (50, 10.0, 10.0, 5.00)]                      # so_lieu_mau: d, t tinh, t doc, d/t
SPEED = 2.0                                                                # tua nhanh 2 lan
CHOT = (2.0, 8.0)                                                          # (t, d) diem cho o cau chot -> v = 4 cm/s

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-dt-dctg-01.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    assert all(any(all(abs(a - b) < 1e-9 for a, b in zip(r, h)) for h in hang) for r in ROWS)
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["v"]["mac_dinh"] == V and ts["t"]["sai_so_do"] == 0.1
    v2 = CHOT[1] / CHOT[0]; assert ts["v"]["min"] <= v2 <= ts["v"]["max"] and abs(50 / v2 - 12.5) < 1e-9
_kiem_so()

WATER = (219, 238, 252); GLASS = (110, 140, 185); STOP = (90, 96, 112); WOOD = (176, 124, 74)
DTEAL = (15, 118, 110); DRED = (185, 28, 28); DORANGE = (176, 64, 8); DBLUE = (29, 78, 216); EMPTY = (148, 140, 128)

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

# ---------------- ong nuoc nghieng ----------------
def tube(d, dbub, flash=None, P0=(110, 500), ang=12, labels=True, s_end=880):
    a = math.radians(ang); TU = (math.cos(a), -math.sin(a)); TN = (math.sin(a), math.cos(a)); HT = 28; PXC = 15; S0 = 70
    TP = lambda s, h: (P0[0] + TU[0] * s + TN[0] * h, P0[1] + TU[1] * s + TN[1] * h)
    d.polygon([TP(0, -HT), TP(s_end, -HT), TP(s_end, HT), TP(0, HT)], fill=WATER)
    for s0, s1 in ((-16, 0), (s_end, s_end + 16)):
        d.polygon([TP(s0, -HT - 4), TP(s1, -HT - 4), TP(s1, HT + 4), TP(s0, HT + 4)], fill=STOP)
    d.line([TP(0, -HT), TP(s_end, -HT)], fill=GLASS, width=5); d.line([TP(0, HT), TP(s_end, HT)], fill=GLASS, width=5)
    if labels:
        for k in range(6):
            dm = k * 10; s = S0 + dm * PXC; fk = (flash or {}).get(dm, 0.0)
            d.line([TP(s, -HT), TP(s, 8)], fill=mix(INK, ORANGE, fk), width=5 + int(5 * fk))
            lb = TP(s, HT + 52)
            text(d, (lb[0] + (26 if k == 5 else 0), lb[1]), f"{dm} cm" if k == 5 else str(dm), 56, DBLUE)
    c = TP(S0 + dbub * PXC, -HT + 15); ra, rb = 28, 12
    pts = [(c[0] + TU[0] * ra * math.cos(u) + TN[0] * rb * math.sin(u),
            c[1] + TU[1] * ra * math.cos(u) + TN[1] * rb * math.sin(u)) for u in [i * math.pi / 18 for i in range(36)]]
    d.polygon(pts, fill=WHITE, outline=GLASS); d.line(pts + [pts[0]], fill=GLASS, width=3)

def stopwatch(d, clock):
    card(d, (60, 222, 420, 330), fill=WHITE, outline=ORANGE, r=22, w=5)
    text(d, (240, 276), vn(clock, 2) + " s", 62, DORANGE)

# ---------------- do thi d-t (truc co dinh) ----------------
GX0, GX1, GYB, GYT = 200, 960, 1185, 690
def X(t): return GX0 + t / 11 * (GX1 - GX0)
def Y(dm): return GYB - dm / 55 * (GYB - GYT)
def axes(d, y0=600, y1=1290):
    card(d, (40, y0, 1040, y1), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GYB), (GX1 + 30, GYB)], fill=NAVY, width=5); d.line([(GX0, GYB), (GX0, GYT - 30)], fill=NAVY, width=5)
    for tt in (2, 4, 6, 8, 10):
        d.line([(X(tt), GYB), (X(tt), GYB + 12)], fill=NAVY, width=4)
        text(d, (X(tt), GYB + 48), str(tt), 56, INK)
    for dm in (10, 20, 30, 40, 50):
        d.line([(GX0 - 12, Y(dm)), (GX0, Y(dm))], fill=NAVY, width=4)
        d.line([(GX0, Y(dm)), (GX1, Y(dm))], fill=(238, 233, 224), width=2)
        text(d, (GX0 - 22, Y(dm)), str(dm), 56, INK, anchor="rm")
    text(d, (1025, GYB - 45), "t (s)", 58, DORANGE, anchor="rm")
    text(d, (GX0 + 25, GYT - 25), "d (cm)", 58, DBLUE, anchor="lm")

def points(d, n, pop=None):
    for i in range(n):
        dm, tt, td, vv = ROWS[i]; k = 1.0 if pop is None else back(clamp(pop[i]))
        if k > 0: dot(d, X(td), Y(dm), 15 * k, NAVY, WHITE)

def fit_line(d, k, col=TEAL, w=8):
    if k > 0: t1 = 10.6 * k; d.line([(X(0), Y(0)), (X(t1), Y(V * t1))], fill=col, width=w)

CX = (360, 505, 650, 795, 940)
def htable(d, n_t):
    card(d, (40, 1310, 1040, 1585), fill=WHITE, outline=LIGHT, w=3)
    text(d, (170, 1385), "d (cm)", 56, DBLUE); text(d, (170, 1510), "t (s)", 56, DORANGE)
    d.line([(70, 1447), (1010, 1447)], fill=LIGHT, width=3)
    for i, (dm, tt, td, vv) in enumerate(ROWS):
        text(d, (CX[i], 1385), str(dm), 58, DBLUE)
        if i < n_t: text(d, (CX[i], 1510), vn(td), 58, DORANGE)
        else: text(d, (CX[i], 1510), "…", 58, EMPTY)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o (cao 70 px), tat lan luot tu phai sang trai."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 190 + i * 145
        if i < on: card(d, (x, y, x + 120, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 120, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def badge(d, y, s, col, a=1.0):
    pw = tw(d, s, F(58)) + 64
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 82), fill=A(col, a), r=40)
    text(d, (W / 2, y + 41), s, 58, WHITE, alpha=a)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 205, 1040, 640), fill=WHITE, outline=LIGHT, w=3)
    tube(d, -4 + 2.5 * ease(t / 3.0)); stopwatch(d, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 680 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 860), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    badge(d, y0 + 30, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Chấm các điểm (t, d)", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 285), "ở vạch 10 … 50 cm.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 430), "Đồ thị d–t", 66, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 520), "có dạng nào?", 66, PURPLE, alpha=a)
    seg_bar(d, y0 + 650, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
RUN0 = 0.6
def tau(t): return (t - RUN0) * SPEED
def bub(t): return clamp(V * tau(t), -1.5, 52.0) if t >= RUN0 else -1.5
def clock(t): return clamp(math.floor(tau(t) * 100 + 1e-6) / 100, 0.0, ROWS[-1][2])
def n_done(t): return sum(1 for r in ROWS if clock(t) >= r[2] - 1e-9)
def lap_at(i): return RUN0 + ROWS[i][2] / SPEED

def s_do(img, d, t, sc):
    card(d, (40, 205, 1040, 580), fill=WHITE, outline=LIGHT, w=3)
    fl = {}
    for i, r in enumerate(ROWS):
        if 0 <= t - lap_at(i) < 0.6: fl[r[0]] = 1.0
    tube(d, bub(t), fl); stopwatch(d, clock(t))
    text(d, (1020, 268), "tua nhanh ×2", 58, INK, anchor="rm")
    axes(d); nd = n_done(t)
    points(d, nd, pop=[(t - lap_at(i)) / 0.4 for i in range(5)])
    htable(d, nd)
    for i in range(nd):
        if t - lap_at(i) < 0.8: d.rounded_rectangle([CX[i] - 70, 1330, CX[i] + 70, 1565], radius=18, outline=ORANGE, width=5)

# ---------------- canh 3: Dap an ----------------
def ruler(d, k):
    if k <= 0: return
    t1 = 10.6 * k; a = math.atan2(Y(V * t1) - Y(0), X(t1) - X(0)); nx, ny = -math.sin(a) * 24, math.cos(a) * 24
    p0, p1 = (X(0), Y(0)), (X(t1), Y(V * t1))
    d.polygon([(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)],
              fill=(120, 130, 150, 130))

def steps(d, k):
    """Bac thang deu tren duong d = 5t: moi 2 s them 10 cm (nhin bang hinh: deu); moi bac hien tron mot luc."""
    for i in range(min(5, int(k * 5 + 1e-9))):
        t0, t1 = 2 * i, 2 * i + 2
        d.polygon([(X(t0), Y(V * t0)), (X(t1), Y(V * t0)), (X(t1), Y(V * t1))], fill=(254, 215, 170))
        d.line([(X(t0), Y(V * t0)), (X(t1), Y(V * t0))], fill=ORANGE, width=12)
        d.line([(X(t1), Y(V * t0)), (X(t1), Y(V * t1))], fill=BLUE, width=12)

def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 540), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=6)
    badge(d, 240, "ĐÁP ÁN", DTEAL, ka)
    text(d, (W / 2, 420), "Gần một đường thẳng", 64, DTEAL, alpha=ka)
    axes(d)
    steps(d, clamp((t - M[1] - 0.1) / 2.2))
    ruler(d, ease((t - 0.6) / 1.2)) if t < M[1] else None
    fit_line(d, 1.0) if t >= M[1] else None
    points(d, 5)

# ---------------- canh 4: Rut ra (do doc) ----------------
def slope_tri(d, k):
    if k <= 0: return
    xa, ya, xb, yb = X(2), Y(10), X(8), Y(40)
    d.line([(xa, ya), (xa + (xb - xa) * clamp(k * 2), ya)], fill=ORANGE, width=7)
    k2 = clamp(k * 2 - 1)
    if k2 > 0: d.line([(xb, ya), (xb, ya + (yb - ya) * k2)], fill=BLUE, width=7)
    for p in ((xa, ya), (xb, yb)):
        dot(d, p[0], p[1], 13, ORANGE if p == (xa, ya) else BLUE)

def s_rutra(img, d, t, sc):
    M = sc["M"]
    axes(d); fit_line(d, 1.0); points(d, 5)
    slope_tri(d, clamp((t - 0.6) / 1.4))
    a1 = appear(t, 1.3, 0.4)
    text(d, ((X(2) + X(8)) / 2, Y(10) + 56), "Δt = 6 s", 58, DORANGE, alpha=a1)
    text(d, (X(8) + 25, Y(25) - 36), "Δd =", 58, DBLUE, anchor="lm", alpha=a1)
    text(d, (X(8) + 25, Y(25) + 36), "30 cm", 58, DBLUE, anchor="lm", alpha=a1)
    k = appear(t, M[1] + 0.3, 0.45)
    card(d, (40, 1320, 1040, 1585), fill=A(WHITE, k), outline=A(TEAL, k), w=6)
    text(d, (W / 2, 1400), "v = Δd / Δt", 62, DTEAL, alpha=k)
    text(d, (W / 2, 1505), "= 30 cm / 6 s = 5 cm/s", 62, DTEAL, alpha=k)

# ---------------- canh 5: Bay (hai khung phong to x10 quanh diem vach 20 cm) ----------------
ZK = 10.0
def zoom_panel(d, y0, straight, t, lab, col, at):
    """Khung 1000 x 470: cung ti le x/y nhu do thi chinh, phong to ZK lan quanh diem (3,9 s; 20 cm)."""
    card(d, (40, y0, 1040, y0 + 500), fill=WHITE, outline=col, w=6)
    sx, sy = (GX1 - GX0) / 11 * ZK, (GYB - GYT) / 55 * ZK
    tc, dc = ROWS[1][2], ROWS[1][0]; cx, cy = 560, y0 + 290
    P = lambda tt, dm: (cx + (tt - tc) * sx, cy - (dm - dc) * sy)
    sub = Image.new("RGB", (988, 400), WHITE); sd = ImageDraw.Draw(sub, "RGBA")
    Q = lambda tt, dm: (P(tt, dm)[0] - 46, P(tt, dm)[1] - (y0 + 90))
    k = ease((t - at) / 0.9)
    if straight:
        t1 = 3.5 + 0.9 * k; sd.line([Q(3.5, V * 3.5), Q(t1, V * t1)], fill=TEAL, width=9)
    else:
        a, b, c = (ROWS[0][2], ROWS[0][0]), (tc, dc), (ROWS[2][2], ROWS[2][0])
        u = lambda p, q, s: (p[0] + (q[0] - p[0]) * s, p[1] + (q[1] - p[1]) * s)
        s1 = clamp(k * 2); s2 = clamp(k * 2 - 1)
        sd.line([Q(*u(a, b, 0.75)), Q(*u(a, b, 0.75 + 0.25 * s1))], fill=DRED, width=9)
        if s2 > 0: sd.line([Q(*b), Q(*u(b, c, 0.2 * s2))], fill=DRED, width=9)
    img = IMG_REF[0]; img.paste(sub, (46, y0 + 90))
    dot(d, *P(tc, dc), 18, NAVY, WHITE)
    text(d, (75, y0 + 55), lab, 60, col, anchor="lm")
    text(d, (1010, y0 + 55), "×10", 58, INK, anchor="rm")
    if straight and k >= 1:
        xa, xb = P(tc, dc)[0] + 22, P(dc / V, dc)[0] - 8; yy = P(tc, dc)[1]
        d.line([(xa, yy), (xb, yy)], fill=DORANGE, width=6)
        for xx in (xa, xb): d.line([(xx, yy - 16), (xx, yy + 16)], fill=DORANGE, width=6)
        text(d, ((xa + xb) / 2, yy - 62), "0,1 s", 58, DORANGE)

def s_bay(img, d, t, sc):
    M = sc["M"]
    zoom_panel(d, 230, False, t, "✗ Gấp khúc", DRED, 0.4)
    if t >= M[1] - 0.1: zoom_panel(d, 790, True, t, "✓ Một đường thẳng", DTEAL, M[1])

# ---------------- canh 6: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 450), "Nghiêng hơn thì v ra sao?", 62, INK)
    card(d, (40, 590, 1040, 1300), fill=WHITE, outline=LIGHT, w=3)
    ang = 12 + 18 * ease((t - 0.6) / 1.6)
    tube(d, 20, P0=(140, 1180), ang=12, labels=False, s_end=760)
    tube(d, 20, P0=(140, 1180), ang=ang, labels=False, s_end=760)
    text(d, (870, 760), "v = ?", 62, DTEAL, alpha=appear(t, 2.2, 0.4))

# ---------------- canh 7: Chot + THU NGHI (= cau_chot khung web) ----------------
EX0, EX1, EYB, EYT = 200, 960, 1290, 780
def EX(t): return EX0 + t / 11 * (EX1 - EX0)
def EY(dm): return EYB - dm / 55 * (EYB - EYT)
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    badge(d, 235, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 400), "Bọt khác, cũng đi đều.", 62, INK, alpha=k)
    text(d, (W / 2, 485), "Qua vạch 50 cm lúc nào?", 64, DORANGE, alpha=k)
    d.line([(EX0, EYB), (EX1 + 30, EYB)], fill=A(NAVY, k), width=5); d.line([(EX0, EYB), (EX0, EYT - 30)], fill=A(NAVY, k), width=5)
    for tt in (2, 4, 6, 8, 10):
        d.line([(EX(tt), EYB), (EX(tt), EYB + 12)], fill=A(NAVY, k), width=4); text(d, (EX(tt), EYB + 48), str(tt), 56, INK, alpha=k)
    for dm in (10, 20, 30, 40, 50):
        d.line([(EX0 - 12, EY(dm)), (EX0, EY(dm))], fill=A(NAVY, k), width=4); text(d, (EX0 - 22, EY(dm)), str(dm), 56, INK, anchor="rm", alpha=k)
    text(d, (1025, EYB - 45), "t (s)", 58, DORANGE, anchor="rm", alpha=k)
    text(d, (EX0 + 25, EYT - 25), "d (cm)", 58, DBLUE, anchor="lm", alpha=k)
    x = EX0
    while x < EX1: d.line([(x, EY(50)), (min(x + 22, EX1), EY(50))], fill=A(DORANGE, k), width=5); x += 40
    text(d, (EX1 + 20, EY(50) - 50), "?", 80, DORANGE, alpha=k)
    d.line([(EX(0), EY(0)), (EX(10), EY(40))], fill=A(TEAL, k), width=8)
    dot(d, EX(CHOT[0]), EY(CHOT[1]), 16, A(NAVY, k), WHITE)
    text(d, (EX(CHOT[0]) + 30, EY(CHOT[1]) + 40), "(2 s; 8 cm)", 58, NAVY, anchor="lm", alpha=k)
    seg_bar(d, 1430, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    cs += [(do["t0"] + lap_at(i), "tap") for i in range(5)]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-dt-dctg-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Đồ thị độ dịch chuyển – thời gian · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bọt khí trong ống nước", draw=s_hook, tail=0.3, caps=[
   ("Bọt khí đi lên trong ống.", 3.4),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Bấm giờ ở từng vạch.", 3.0),
   ("Mỗi lần bấm: thêm một điểm.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Đặt thước dọc các điểm.", 3.0),
   ("Mỗi 2 s thêm 10 cm: đều.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Lấy hai điểm xa nhau.", 3.0),
   ("Độ dốc là vận tốc.", 3.2)]),
 dict(key="bay", title="Bẫy: nối từng điểm", draw=s_bay, tail=0.3, caps=[
   ("Nối từng điểm một?", 3.2),
   ("Điểm lệch do bấm giờ tay.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.6, caps=[
   ("Mới thử một độ nghiêng.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Đồ thị thẳng: vận tốc không đổi.", 6.4)]),
])
