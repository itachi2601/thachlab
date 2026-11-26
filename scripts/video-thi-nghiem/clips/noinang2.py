# Clip: tn-l12-noinang-02 - Do nhiet dung rieng cua nuoc bang bep dien co oat ke.
# Trong tam T7: chieu sai so (nhiet hao -> dt do nho hon li tuong -> c do LON hon 4 180).
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-noinang-02.json (so_lieu_mau, tham_so, mo_hinh):
#   m = 0,500 kg, P = 500 W, t ban dau 25,0 °C, c sach = 4 180 J/(kg.K)
#   tau 0/20/40/60/80 s -> t 25,0/29,6/34,1/38,6/43,1 °C, Q = 0/10 000/20 000/30 000/40 000 J, c ≈ 4 348/4 396/4 412/(4 420)
#   O c moc 80 s KHONG hien (trong bai la o "em tu tinh", dap so 4 420).
#   Duong "li tuong" (net dut) tinh tu tham_so: t = 25 + P.tau/(m.c_that) -> 44,1 °C o 80 s (dt 19,1 K so voi do 18,1 K).
# Ban 1, 2 (14/11/2026). Ban 3 (26/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32): cong --do-chu (chu ve >= 58 px,
#   <= 180 tu/phut moi canh, nhip >= 2 s), <= 50 s, K10 (khong nut A-D), bo canh "chua noi duoc" (giu trong khung web),
#   Bay ve hai hinh canh nhau: sai ngau nhien (lech hai phia) / do that (ca ba lech len).
# Du doan (khung web): c do duoc so voi 4 180? A nho hon / B bang / C lon hon (DUNG) / D luc lon luc nho.
# THU NGHI (= cau_chot khung, CA TU SUY ghi trong kho): dat dau nhiet ke sat day dien tro -> c tinh ra NHO hon
#   (nhiet ke chi cao hon nhiet do trung binh cua nuoc -> dt lon hon).
from engine import *

M_KG, P_W, T0C, C_THAT = 0.500, 500, 25.0, 4180
ROWS = ((0, 25.0), (20, 29.6), (40, 34.1), (60, 38.6), (80, 43.1))
CS = {20: 4348, 40: 4396, 60: 4412}

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-noinang-02.json")))
    hang = {r[0]: r for r in k["so_lieu_mau"]["hang"]}
    for tau, tv in ROWS:
        assert hang[tau][1] == tv and hang[tau][2] == P_W * tau
    for tau, c in CS.items():
        assert hang[tau][3] == c and abs(P_W * tau / (M_KG * (hang[tau][1] - T0C)) - c) < 1
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["c_that"]["gia_tri"] == C_THAT and ts["m"]["mac_dinh"] == M_KG and ts["P"]["mac_dinh"] == P_W
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
FS = 58
WIRE_C = (190, 60, 40)
SCREEN = (24, 30, 40); LCD = (134, 239, 172)
def vn(x): return f"{x:.1f}".replace(".", ",")
def sp(n): return f"{n:,}".replace(",", " ")

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

def dashed(d, p1, p2, color, w=4, dash=18, gap=12):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

# ---------------- dung cu ----------------
def calor(d, t, ox, oy, heat, on, probe_near=False, s=1.0):
    """binh nhiet luong ke: goc trai tren (ox, oy), rong 340*s, cao 430*s"""
    P = lambda x, y: (ox + x * s, oy + y * s)
    card(d, (*P(0, 0), *P(340, 430)), fill=(232, 226, 214), outline=(170, 160, 140), r=30, w=4)
    d.rounded_rectangle([*P(35, 25), *P(305, 405)], radius=18, fill=(250, 252, 255), outline=(150, 175, 205), width=4)
    yw = 405 - 380 * 0.78
    d.rounded_rectangle([*P(39, yw), *P(301, 401)], radius=14, fill=mix((175, 212, 250), (250, 190, 160), heat))
    d.line([P(41, yw), P(299, yw)], fill=(110, 160, 220), width=4)
    d.rounded_rectangle([*P(-15, -18), *P(355, 12)], radius=10, fill=(120, 126, 140))
    zz = [P(100 + 16 * j, 360 + (13 if j % 2 else -13)) for j in range(10)]
    d.line(zz, fill=WIRE_C if on else (120, 90, 80), width=7, joint="curve")
    if on:
        g = 0.35 + 0.25 * math.sin(t * 6); d.line(zz, fill=A((255, 140, 60), g), width=15, joint="curve")
    d.line([P(100, 360), P(100, -75)], fill=NAVY, width=5); d.line([P(244, 360), P(244, -58)], fill=NAVY, width=5)
    sw = math.sin(t * 3.0) * 10
    d.line([P(60 + sw, -45), P(70 + sw * 0.3, 390)], fill=(150, 110, 70), width=10)
    px, py = (255, 330) if probe_near else (280, 300)
    d.line([P(px, py), P(px, -28)], fill=(90, 96, 110), width=10); dot(d, *P(px, py + 2), 10, NAVY)

def readouts(d, tau, ts):
    card(d, (470, 250, 1040, 520), fill=WHITE, outline=NAVY, w=5, r=24)
    text(d, (755, 298), "oát kế", FS, INK)
    card(d, (495, 345, 1015, 500), fill=SCREEN, r=14)
    text(d, (755, 385), "P = 500 W", 58, LCD)
    text(d, (755, 460), f"τ = {tau} s", 58, LCD)
    card(d, (470, 550, 1040, 790), fill=WHITE, outline=NAVY, w=5, r=24)
    text(d, (755, 598), "nhiệt kế", FS, INK)
    card(d, (495, 645, 1015, 770), fill=SCREEN, r=14)
    text(d, (755, 708), ts + " °C", 62, LCD)

def rig(d, t, k, on):
    calor(d, t, 80, 330, k / 4, on)
    pill(d, 250, 840, "m = 0,500 kg", NAVY, size=FS)
    readouts(d, ROWS[k][0], vn(ROWS[k][1]))

# ---------------- do thi t(tau) ----------------
YLO, YHI = 23, 47
def plot(d, box, npts, ideal=0.0):
    x0, ytop, x1, y0 = box
    X = lambda s: x0 + s / 80 * (x1 - x0); Y = lambda T: y0 - (T - YLO) / (YHI - YLO) * (y0 - ytop)
    for T in (25, 35, 45):
        d.line([(x0, Y(T)), (x1, Y(T))], fill=LIGHT, width=3)
        text(d, (x0 - 24, Y(T)), str(T), FS, INK, anchor="rm")
    d.line([(x0, y0), (x1 + 10, y0)], fill=NAVY, width=5); d.line([(x0, y0), (x0, ytop - 10)], fill=NAVY, width=5)
    d.polygon([(x1 + 26, y0), (x1 + 8, y0 - 10), (x1 + 8, y0 + 10)], fill=NAVY)
    d.polygon([(x0, ytop - 26), (x0 - 10, ytop - 8), (x0 + 10, ytop - 8)], fill=NAVY)
    text(d, (x0 + 24, ytop - 10), "t (°C)", FS, INK, anchor="lm")
    yb = y0 - 12
    d.rectangle([x0 - 12, yb - 5, x0 + 12, yb + 5], fill=WHITE)
    for dy in (-5, 5): d.line([(x0 - 14, yb + dy + 5), (x0 + 14, yb + dy - 5)], fill=NAVY, width=4)
    for s in (0, 40, 80):
        d.line([(X(s), y0), (X(s), y0 + 12)], fill=NAVY, width=4)
        text(d, (X(s), y0 + 48), str(s), FS, INK)
    text(d, (x1 + 26, y0 + 112), "τ (s)", FS, INK, anchor="rm")
    if ideal > 0:
        e = T0C + P_W * 80 / (M_KG * C_THAT)
        dashed(d, (X(0), Y(T0C)), (lerp(X(0), X(80), ideal), lerp(Y(T0C), Y(e), ideal)), GREEN, 6)
    pts = [(X(r[0]), Y(r[1])) for r in ROWS[:npts]]
    if len(pts) >= 2: d.line(pts, fill=BLUE, width=6, joint="curve")
    for p in pts: dot(d, p[0], p[1], 13, ORANGE, outline=WHITE)
    return X, Y

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    rig(d, t, 0, False)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1000 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 520), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 175), "Sách: c = 4 180 J/(kg·K)", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 265), "c đo được sẽ", 64, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 345), "so với 4 180 thế nào?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 420, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh ----------------
def k_of(t, sc):
    a, b = sc["M"][0] + 0.4, sc["M"][1] + 1.6
    return min(4, int(4 * clamp((t - a) / (b - a)) + 1e-6))

def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k = k_of(t, sc)
    on = t < M[1] + 1.8
    rig(d, t, k, on)
    if on:
        wdt = tw(d, "TUA NHANH", F(FS)) + 100
        card(d, (755 - wdt / 2, 805, 755 + wdt / 2, 885), fill=ORANGE, r=38)
        text(d, (755 + 24, 845), "TUA NHANH", FS, WHITE)
        for kk in range(2):
            tx = 755 - wdt / 2 + 26 + kk * 18; d.polygon([(tx, 827), (tx, 863), (tx + 18, 845)], fill=WHITE)
    card(d, (40, 940, 1040, 1560), fill=WHITE, outline=LIGHT, w=4)
    plot(d, (190, 1040, 940, 1400), k + 1)

# ---------------- canh 3: Ket qua ----------------
def s_ket(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 250, 1040, 1150), fill=WHITE, outline=LIGHT, w=4)
    xs = (150, 380, 620, 860)
    text(d, (1010, 1110), "số minh hoạ", FS, PURPLE, anchor="rm")
    for x, h in zip(xs, ("τ (s)", "t (°C)", "Q (J)", "c")):
        text(d, (x, 320), h, FS, INK)
    d.line([(70, 370), (1010, 370)], fill=LIGHT, width=4)
    for j, tau in enumerate((20, 40, 60, 80)):
        y = 440 + 115 * j
        text(d, (xs[0], y), str(tau), FS, INK)
        text(d, (xs[1], y), vn(dict(ROWS)[tau]), FS, INK)
        text(d, (xs[2], y), sp(P_W * tau), FS, INK)
        text(d, (xs[3], y), sp(CS[tau]) if tau in CS else "?", FS, DORANGE)
    d.line([(70, 860), (1010, 860)], fill=LIGHT, width=4)
    text(d, (xs[0] + 60, 930), "Sách:", FS, DGREEN)
    text(d, (xs[3], 930), "4 180", FS, DGREEN)
    text(d, (W / 2 - 120, 1060), "c = P·τ / (m·Δt)", 62, NAVY)
    k = appear(t, M[1], 0.4)
    if k > 0:
        for j in range(3):
            y = 440 + 115 * j
            arrow(d, (975, y + 26), (975, y - 26), A(DRED, k), w=8, head=22)
        d.rounded_rectangle([755, 395, 1010, 720], radius=20, outline=A(DRED, k), width=6)

# ---------------- canh 4: vi sao ----------------
def heat_arrow(d, x, y, dx, dy, alpha):
    if alpha > 0: arrow(d, (x, y), (x + dx, y + dy), A(ORANGE, alpha), w=8, head=24)

def s_visao(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    calor(d, t, 80, 360, 1.0, True, s=0.75)
    ka = appear(t, 0.6, 0.4)
    u = (t * 0.7) % 1                                  # mui ten nhiet troi ra ngoai, lap lai
    for (x, y, dx, dy) in ((60, 520, -45, 0), (350, 520, 50, 0), (200, 310, 0, -55)):
        ox, oy = (dx / 45 * 50 * u, 0) if dy == 0 else (0, -50 * u)
        heat_arrow(d, x + ox, y + oy, dx, dy, ka * min(1, (1 - u) / 0.3))
    text(d, (230, 790), "mất nhiệt", FS, DORANGE)
    card(d, (440, 250, 1040, 900), fill=WHITE, outline=LIGHT, w=4)
    ki = ease(clamp((t - 1.0) / 1.2))
    X, Y = plot(d, (560, 330, 960, 760), 5, ideal=ki)
    text(d, (975, Y(29)), "lí tưởng", FS, DGREEN, anchor="rm", alpha=appear(t, 2.2, 0.4))
    kb = appear(t, M[1], 0.4)
    if kb > 0:
        xb = X(80) + 22; ya, yb2 = Y(T0C + P_W * 80 / (M_KG * C_THAT)), Y(43.1)
        d.line([(xb, ya), (xb + 14, ya), (xb + 14, yb2), (xb, yb2)], fill=A(DRED, kb), width=5)
    k3 = appear(t, M[1], 0.4)
    if k3 > 0:
        card(d, (60, 960, 1020, 1180), fill=A(WHITE, k3), outline=A(DRED, k3), w=5)
        text(d, (W / 2, 1030), "Δt lí tưởng 19,1 K", FS, DGREEN, alpha=k3)
        text(d, (W / 2, 1110), "Δt đo được 18,1 K", FS, BLUE, alpha=k3)

# ---------------- canh 5: Bay (hai hinh canh nhau) ----------------
def strip(d, cx, vals, col, g=1.0):
    """truc doc c tu 4 100 den 4 500, vach 4 180"""
    yA, yB = 1200, 460
    Yc = lambda c: yA + (c - 4100) / 400 * (yB - yA)
    d.line([(cx - 170, Yc(4180)), (cx + 170, Yc(4180))], fill=DGREEN, width=6)
    text(d, (cx, Yc(4180) + 50), "4 180", FS, DGREEN)
    for j, c in enumerate(vals):
        x = cx - 110 + 110 * j
        c = 4180 + (c - 4180) * ease(clamp(g * 3 - j))
        if abs(c - 4180) > 3: dashed(d, (x, Yc(4180)), (x, Yc(c)), A(col, 0.6), 4, 10, 8)
        dot(d, x, Yc(c), 18, col, outline=WHITE)

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    for cx, lab, col in ((285, "Nếu đọc sai", DRED), (795, "Số liệu mẫu", DGREEN)):
        card(d, (cx - 245, 250, cx + 245, 1330), fill=WHITE, outline=col, w=6)
        text(d, (cx, 310), lab, 62, col)
    SETS = ((4120, 4250, 4230), (4250, 4230, 4110), (4130, 4260, 4150))
    strip(d, 285, SETS[int(t / 1.4) % 3], DRED)
    strip(d, 795, (CS[20], CS[40], CS[60]), BLUE)
    text(d, (285, 1260), "lên, xuống", FS, DRED)
    k = appear(t, M[1], 0.4)
    text(d, (795, 1260), "đều lệch lên", FS, DGREEN, alpha=k)

# ---------------- canh 6: chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    if k1 > 0.5:
        calor(d, t, 330, 450, 0.4, True, probe_near=True, s=0.9)
        arrow(d, (760, 600), (580, 720), ORANGE, w=7, head=22)
    text(d, (W / 2, 1060), "Mốc 20 s, nhiệt kế sát dây:", 62, INK, alpha=k1)
    text(d, (W / 2, 1150), "c tính ra lớn hơn hay", 64, DORANGE, alpha=k1)
    text(d, (W / 2, 1240), "nhỏ hơn 4 348?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1360, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, v, b, e = (sc[x] for x in ("hook", "do", "ket", "visao", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding"), (do["t0"] + do["M"][0] + 0.4, "tap")]
    out += [(k["t0"] + 0.3, "ding"), (k["t0"] + k["M"][1], "tap"), (v["t0"] + v["M"][1], "tap"),
            (b["t0"] + 0.6, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l12-noinang-02", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Nhiệt dung riêng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo c của nước", draw=s_hook, tail=0.3, caps=[
   ("Dây đốt chìm trong nước.", 3.0),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Đun, ghi mỗi 20 s", draw=s_do, tail=0.4, caps=[
   ("Khuấy đều, cứ 20 s ghi một lần.", 3.8),
   ("Nước nóng lên gần như đều.", 3.6)]),
 dict(key="ket", title="Kết quả", draw=s_ket, tail=0.4, caps=[
   ("Đáp án: c lớn hơn 4 180.", 3.6),
   ("Cả ba mốc đều lệch lên.", 3.6)]),
 dict(key="visao", title="Vì sao lớn hơn?", draw=s_visao, tail=0.4, caps=[
   ("Một phần nhiệt không vào nước.", 4.4),
   ("Δt nhỏ hơn, nên c tính ra lớn hơn.", 4.2)]),
 dict(key="bay", title="Bẫy: do nhiệt kế đọc sai?", draw=s_bay, tail=0.4, caps=[
   ("Đọc sai: lệch cả hai phía.", 3.4),
   ("Ba mốc đều lệch lên.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Nhớ lại: c = P·τ / (m·Δt).", 6.2)]),
])
