# Clip: tn-l12-noinang-02 - Do nhiet dung rieng cua nuoc bang bep dien co oat ke (ban 1, 14/11/2026)
# Trong tam T7: chieu sai so (nhiet hao -> dt do nho hon li tuong -> c do LON hon 4 180).
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-noinang-02.json (so_lieu_mau, tham_so, mo_hinh):
#   m = 0,500 kg, P = 500 W, t ban dau 25,0 °C, c sach = 4 180 J/(kg.K)
#   tau 0/20/40/60/80 s -> t 25,0/29,6/34,1/38,6/43,1 °C, Q = 0/10 000/20 000/30 000/40 000 J, c ≈ 4 348/4 396/4 412/(4 420)
#   O c moc 80 s KHONG hien (trong bai la o "em tu tinh", dap so 4 420) -> clip ghi "em tự tính".
#   Duong "binh li tuong" (net dut) tinh tu tham_so: t = 25 + P.tau/(m.c_that), khong ghi so tren duong.
# Du doan (khung; K10: trong mp4 KHONG ve nut A-D, chi cau hoi + hinh):
#   "Do bang binh nay, c tinh ra so voi 4 180 J/(kg.K) the nao?"
#   A. Nho hon 4 180   B. Bang dung 4 180   C. Lon hon 4 180 (DUNG)   D. Luc lon, luc nho hon 4 180
#   (ca ba gia tri do 4 348/4 396/4 412 deu lon hon -> chi C khop; D la y "sai so ngau nhien", khong khop so do)
# Bay (hien_tuong_hay_sai[0]): "c lech vi nhiet ke doc sai" -> sai ngau nhien lech hai phia; o day ca ba lech len -> he thong.
# Chua noi duoc (khong_chung_minh): nhiet mat bao nhieu khong do duoc; mot lan do mot m chua noi c co doi theo m.
# THU NGHI (ban 2, sai_so_thuong_gap[2]): nhiet ke dat sat day dien tro -> c do lon hay nho hon 4 348?
#   Dap: NHO hon - so doc cao hon nhiet do trung binh cua nuoc -> dt lon hon -> c = Q/(m.dt) nho hon.
#   Goi y (tre ~4 s, cau hoi trung tinh): "Nhiệt kế đọc cao hay thấp?"
# Ban 2 (14/11/2026, cong B vong 1): bay neu ±0,1 °C khong du gay lech 4–6 % cung chieu; visao ghi Δt 19,1/18,1 K
#   (hop bai); dong ket luan giu ≥ 2,5 s; dau ngat truc t; "c tang dan" kem ly do; thu khoang trong ket/bay.
from engine import *

NOTE = (70, 75, 95)
WIRE_C = (190, 60, 40)
SCREEN = (24, 30, 40); LCD = (134, 239, 172)
M_KG, P_W, T0C, C_THAT = 0.500, 500, 25.0, 4180
ROWS = ((0, 25.0, "25,0", "0", None), (20, 29.6, "29,6", "10 000", "4 348"), (40, 34.1, "34,1", "20 000", "4 396"),
        (60, 38.6, "38,6", "30 000", "4 412"), (80, 43.1, "43,1", "40 000", None))

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=26):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.85, cx + wdt / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def dashed(d, p1, p2, color, w=4, dash=18, gap=12):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

# ---------------- dung cu: nhiet luong ke + oat ke + nhiet ke ----------------
def rig(d, t, k, on, ff=False):
    """k: chi so hang so_lieu_mau dang doc (0..4) -> oat ke (tau) va nhiet ke (t) CUNG mot hang; on: dang dun."""
    tau, tv, ts = ROWS[k][0], ROWS[k][1], ROWS[k][2]
    heat = k / 4
    # binh vo xop + nap
    card(d, (90, 300, 430, 730), fill=(232, 226, 214), outline=(170, 160, 140), r=30, w=4)
    for j in range(8):
        y = 330 + j * 50; d.line([(100, y), (118, y + 18)], fill=(200, 192, 176), width=3); d.line([(402, y), (420, y + 18)], fill=(200, 192, 176), width=3)
    d.rounded_rectangle([125, 325, 395, 705], radius=18, fill=(250, 252, 255), outline=(150, 175, 205), width=4)
    yw = 705 - 380 * 0.78
    d.rounded_rectangle([129, yw, 391, 701], radius=14, fill=mix((175, 212, 250), (250, 190, 160), heat))
    d.line([(131, yw), (389, yw)], fill=(110, 160, 220), width=4)
    d.rounded_rectangle([75, 282, 445, 312], radius=10, fill=(120, 126, 140))          # nap
    # dien tro chim trong nuoc
    zz = [(190 + 16 * j, 660 + (13 if j % 2 else -13)) for j in range(10)]
    d.line(zz, fill=WIRE_C if on else (120, 90, 80), width=7, joint="curve")
    if on:
        g = 0.35 + 0.25 * math.sin(t * 6); d.line(zz, fill=A((255, 140, 60), g), width=15, joint="curve")
    d.line([(190, 660), (190, 225), (470, 225), (470, 330), (500, 330)], fill=NAVY, width=5, joint="curve")
    d.line([(334, 660), (334, 242), (455, 242), (455, 380), (500, 380)], fill=NAVY, width=5, joint="curve")
    # que khuay
    sw = math.sin(t * 3.0) * 10 if on else 0
    d.line([(150 + sw, 255), (160 + sw * 0.3, 690)], fill=(150, 110, 70), width=10)
    # dau do nhiet ke (xa dien tro)
    d.line([(370, 600), (370, 272)], fill=(90, 96, 110), width=10); dot(d, 370, 602, 10, NAVY)
    d.line([(370, 272), (440, 272), (440, 700), (500, 700)], fill=(90, 96, 110), width=5, joint="curve")
    # oat ke: P va tau
    card(d, (500, 250, 1030, 560), fill=WHITE, outline=NAVY, w=5, r=24)
    text(d, (765, 292), "oát kế", 44, INK)
    card(d, (525, 330, 1005, 540), fill=SCREEN, r=14)
    text(d, (765, 385), "P = 500 W", 52, LCD)
    text(d, (765, 480), f"τ = {tau} s", 52, LCD)
    # nhiet ke
    card(d, (500, 590, 1030, 820), fill=WHITE, outline=NAVY, w=5, r=24)
    text(d, (765, 632), "nhiệt kế", 44, INK)
    card(d, (525, 675, 1005, 800), fill=SCREEN, r=14)
    text(d, (765, 738), ts + " °C", 56, LCD)
    pill(d, 260, 790, "m = 0,500 kg", 44, WHITE, NAVY)
    if ff:
        wdt = tw(d, "TUA NHANH", F(44)) + 96
        card(d, (765 - wdt / 2, 850, 765 + wdt / 2, 916), fill=ORANGE, r=33)
        text(d, (765 + 22, 883), "TUA NHANH", 44, WHITE)
        for j in range(2):
            tx = 765 - wdt / 2 + 22 + j * 16; d.polygon([(tx, 868), (tx, 898), (tx + 16, 883)], fill=WHITE)

# ---------------- do thi t(tau) ----------------
YLO, YHI = 23, 47
def plot(d, box, npts, ideal=0.0, prog=1.0):
    """npts: so diem do da hien (1..5); ideal: do hien duong binh li tuong (net dut, khong ghi so)."""
    x0, ytop, x1, y0 = box
    X = lambda s: x0 + s / 80 * (x1 - x0); Y = lambda T: y0 - (T - YLO) / (YHI - YLO) * (y0 - ytop)
    for T in (25, 35, 45):
        d.line([(x0, Y(T)), (x1, Y(T))], fill=LIGHT, width=3)
        text(d, (x0 - 26, Y(T)), str(T), 44, NOTE, bold=False, anchor="rm")
    d.line([(x0, y0), (x1 + 10, y0)], fill=NAVY, width=5); d.line([(x0, y0), (x0, ytop - 10)], fill=NAVY, width=5)
    d.polygon([(x1 + 26, y0), (x1 + 8, y0 - 10), (x1 + 8, y0 + 10)], fill=NAVY)
    d.polygon([(x0, ytop - 26), (x0 - 10, ytop - 8), (x0 + 10, ytop - 8)], fill=NAVY)
    text(d, (x0 + 24, ytop - 8), "t (°C)", 44, INK, anchor="lm")
    yb = y0 - 12                                       # dau ngat truc t (truc bat dau tu 23 °C), duoi nhan "25"
    d.rectangle([x0 - 12, yb - 5, x0 + 12, yb + 5], fill=WHITE)
    for dy in (-5, 5): d.line([(x0 - 14, yb + dy + 5), (x0 + 14, yb + dy - 5)], fill=NAVY, width=4)
    for s in (0, 20, 40, 60, 80):
        d.line([(X(s), y0), (X(s), y0 + 12)], fill=NAVY, width=4)
        text(d, (X(s), y0 + 42), str(s), 44, NOTE, bold=False)
    text(d, (x1 + 26, y0 + 98), "τ (s)", 44, INK, anchor="rm")
    if ideal > 0:
        e = (80, T0C + P_W * 80 / (M_KG * C_THAT))
        dashed(d, (X(0), Y(T0C)), (lerp(X(0), X(e[0]), ideal), lerp(Y(T0C), Y(e[1]), ideal)), GREEN, 5)
    pts = [(X(r[0]), Y(r[1])) for r in ROWS[:npts]]
    if len(pts) >= 2:
        last = pts[-1]; prev = pts[-2]
        seg = pts[:-1] + [(lerp(prev[0], last[0], prog), lerp(prev[1], last[1], prog))]
        d.line(seg, fill=BLUE, width=6, joint="curve")
    for i, p in enumerate(pts):
        if i < len(pts) - 1 or prog >= 0.99: dot(d, p[0], p[1], 12, ORANGE, outline=WHITE)
    return X, Y

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    rig(d, t, 0, False)
    M = sc["M"]
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 44, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 160), "Sách: c = 4 180 J/(kg·K)", 48, INK, alpha=a)
    text(d, (W / 2, y0 + 228), "c: nhiệt dung riêng", 44, NOTE, bold=False, alpha=a)
    ctext(d, y0 + 340, "c đo được so với 4 180?", 52, PURPLE, maxw=920, alpha=a)
    text(d, (W / 2, y0 + 460), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 515, 940, y0 + 527], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 515, 140 + 800 * (1 - p), y0 + 527], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
MARKS = (1.4, 2.9, 4.4, 5.9)        # moc doc 20/40/60/80 s (giay trong canh)
def k_at(t):
    return sum(1 for m in MARKS if t >= m)

def s_do(img, d, t, sc):
    k = k_at(t)
    rig(d, t, k, 0.6 <= t < MARKS[-1], ff=0.6 <= t < MARKS[-1])
    card(d, (40, 950, 1040, 1600), fill=WHITE, outline=LIGHT, w=3)
    prog = clamp((t - (MARKS[k - 1] if k else 0)) / 0.35)
    plot(d, (180, 1010, 950, 1460), k + 1, prog=prog)

# ---------------- canh 3: Ket qua (bang + dap an) ----------------
COLX = ((150, "τ (s)"), (350, "t (°C)"), (590, "Q (J)"), (860, "c"))
def table(d, y0, kc, hl=0.0, rh=86):
    if hl > 0:
        d.rounded_rectangle([735, y0 + 46, 985, y0 + 52 + rh * 5], radius=18, fill=A((255, 237, 213), hl), outline=A(ORANGE, hl), width=4)
    for x, s in COLX: text(d, (x, y0), s, 44, NOTE, bold=False)
    d.line([(70, y0 + 40), (1010, y0 + 40)], fill=LIGHT, width=3)
    for j, r in enumerate(ROWS):
        yy = y0 + 46 + rh * (j + 0.5)
        for x, s in ((150, str(r[0])), (350, r[2]), (590, r[3])): text(d, (x, yy), s, 46, INK)
        if j == 0: text(d, (860, yy), "—", 46, NOTE)
        elif r[4] and kc[j - 1] > 0: text(d, (860, yy), "≈ " + r[4], 46, ORANGE, alpha=kc[j - 1])
        elif r[4] is None and kc[2] > 0: text(d, (860, yy), "em tự tính", 44, PURPLE, alpha=kc[2])

def s_ket(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 255, 1040, 880), fill=WHITE, outline=LIGHT, w=3)
    kc = [appear(t, M[0] + 0.5 + 0.5 * j, 0.35) for j in range(3)]
    table(d, 305, kc, hl=appear(t, M[1] - 0.2, 0.4), rh=94)
    text(d, (W / 2, 945), "Q = P·τ   ·   c = Q / (m·Δt)", 50, INK)
    text(d, (W / 2, 1015), "Δt = t − 25,0 °C", 44, NOTE, bold=False)
    ka = appear(t, M[1] + 0.1, 0.4)
    if ka > 0:
        pw = tw(d, "ĐÁP ÁN · Lớn hơn", F(44)) + 60
        card(d, (W / 2 - pw / 2, 1100, W / 2 + pw / 2, 1174), fill=A(NAVY, ka), r=37)
        text(d, (W / 2, 1137), "ĐÁP ÁN · Lớn hơn", 44, WHITE, alpha=ka)
    kb = appear(t, M[1] + 1.2, 0.4)
    if kb > 0:
        card(d, (90, 1230, 990, 1450), fill=A((255, 247, 237), kb), r=24)
        text(d, (W / 2, 1295), "c tăng dần theo τ", 48, ORANGE, alpha=kb)
        text(d, (W / 2, 1385), "(mất nhiệt tăng theo t)", 44, NOTE, bold=False, alpha=kb)

# ---------------- canh 4: Vi sao lon hon + chua noi duoc ----------------
def heat_arrow(d, x, y, dx, dy, alpha):
    """Mui ten luon song (nhiet thoat ra) tu (x, y) theo (dx, dy)."""
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    pts = [(x + dx * u - uy * 9 * math.sin(u * 9.4), y + dy * u + ux * 9 * math.sin(u * 9.4)) for u in [i / 15 for i in range(16)]]
    d.line(pts, fill=A(RED, alpha), width=6, joint="curve")
    arrow(d, (x + dx - ux * 4, y + dy - uy * 4), (x + dx + ux * 8, y + dy + uy * 8), A(RED, alpha), w=6, head=20)

def vbar(d, x, ya, yb, col, alpha):
    d.line([(x, ya), (x, yb)], fill=A(col, alpha), width=6)
    for y in (ya, yb): d.line([(x - 12, y), (x + 12, y)], fill=A(col, alpha), width=6)

def s_vi_sao(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 255, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    ki = clamp((t - 0.6) / 1.0)
    X, Y = plot(d, (180, 330, 940, 800), 5, ideal=ki)
    kl = appear(t, 1.2, 0.4)
    if kl > 0:                                   # Δt so voi 25,0 °C o moc 80 s: li tuong ≈ 19,1 K, do 18,1 K (hop bai)
        text(d, (X(30), Y(42.5)), "bình lí tưởng", 44, GREEN, alpha=kl)
        vbar(d, 968, Y(T0C), Y(43.1), BLUE, kl)
        vbar(d, 1004, Y(T0C), Y(T0C + P_W * 80 / (M_KG * C_THAT)), GREEN, kl)
        text(d, (930, Y(31.5)), "Δt lí tưởng ≈ 19,1 K", 44, GREEN, anchor="rm", alpha=kl)
        text(d, (930, Y(28.5)), "Δt đo = 18,1 K", 44, BLUE, anchor="rm", alpha=kl)
    kn = appear(t, M[1] - 0.15, 0.45)              # the "chua noi duoc" thay the co che
    am = appear(t, 1.6, 0.45) * (1 - kn)
    if am > 0:
        card(d, (40, 1000, 1040, 1590), fill=A(WHITE, am), outline=A(RED, am), w=5)
        # binh nho + nhiet thoat ra (mui ten khong cham vien the)
        card(d, (110, 1130, 330, 1360), fill=A((232, 226, 214), am), outline=A((170, 160, 140), am), r=20, w=3)
        d.rounded_rectangle([135, 1200, 305, 1340], radius=12, fill=A((250, 190, 160), am))
        d.rounded_rectangle([100, 1112, 340, 1132], radius=8, fill=A((120, 126, 140), am))
        for (x, y, dx, dy) in ((220, 1100, 0, -70), (335, 1250, 72, 0), (118, 1160, -50, -50)):
            heat_arrow(d, x, y, dx, dy, am)
        text(d, (440, 1140), "Nhiệt vào bình, ra ngoài", 46, INK, anchor="lm", alpha=am)
        k2 = appear(t, 2.2, 0.4) * (1 - kn)
        text(d, (440, 1260), "→ Δt nhỏ hơn", 48, RED, anchor="lm", alpha=k2)
        k3 = appear(t, 2.8, 0.4) * (1 - kn)
        text(d, (W / 2, 1460), "c = P·τ / (m·Δt) lớn hơn", 52, ORANGE, alpha=k3)
    if kn > 0:
        card(d, (40, 1000, 1040, 1590), fill=A(WHITE, kn), outline=A(NAVY, kn), w=6)
        text(d, (W / 2, 1075), "Chưa nói được", 50, NAVY, alpha=kn)
        for j, l1 in enumerate(("• Nhiệt mất bao nhiêu", "• c có đổi theo m")):
            kk = kn * appear(t, M[1] + 0.2 + 0.5 * j, 0.35)
            text(d, (90, 1230 + 190 * j), l1, 48, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Bay ----------------
NX0, NX1, NV0, NV1 = 150, 930, 4100, 4500
def nx(v): return NX0 + (v - NV0) / (NV1 - NV0) * (NX1 - NX0)

def s_bay(img, d, t, sc):
    M = sc["M"]
    mk = M[0] + 2.0
    card(d, (40, 255, 1040, 700), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, 315, "BẪY", 44, WHITE, RED)
    q = "“c lệch vì nhiệt kế đọc sai”"
    ks = clamp((t - mk) / 0.4)
    text(d, (W / 2, 420), q, 48, mix(INK, GRAY, ks))
    if ks > 0:
        lw = tw(d, q, F(48)); d.line([(W / 2 - lw / 2 - 6, 422), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, 422)], fill=RED, width=6)
    k1 = appear(t, mk + 0.2, 0.4)
    text(d, (W / 2, 535), "±0,1 °C: lệch hai phía,", 48, INK, alpha=k1)
    text(d, (W / 2, 605), "không thể cả ba cùng lên", 48, INK, alpha=k1)
    # truc so c (hien ngay) - diem do hien SAU khi gach cau sai
    card(d, (40, 740, 1040, 1300), fill=WHITE, outline=LIGHT, w=3)
    ya = 1020
    d.line([(NX0, ya), (NX1, ya)], fill=INK, width=5)
    for v in (4100, 4300, 4500):
        d.line([(nx(v), ya), (nx(v), ya + 16)], fill=INK, width=4)
        if v != 4300: text(d, (nx(v), ya + 56), f"{v:,}".replace(",", " "), 44, NOTE, bold=False)
    text(d, (W / 2, 1200), "c (J/(kg·K))", 44, NOTE, bold=False)
    xg = nx(4180)
    for yy in range(860, ya - 6, 26): d.line([(xg, yy), (xg, yy + 14)], fill=GREEN, width=5)
    text(d, (xg, 815), "4 180", 44, GREEN)
    for j, v in enumerate((4348, 4396, 4412)):
        kd = appear(t, mk + 0.3 + 0.25 * j, 0.3)
        if kd > 0: dot(d, nx(v), ya - 2, 16 * kd + 0.1, ORANGE, outline=WHITE)
    k2 = appear(t, mk + 1.2, 0.4)
    if k2 > 0:
        arrow(d, (xg + 30, 910), (nx(4412) + 40, 910), A(ORANGE, k2), w=6, head=20)
    k3 = appear(t, M[1] + 0.3, 0.45)
    if k3 > 0:
        card(d, (60, 1350, 1020, 1560), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1415), "✓ Sai số hệ thống:", 48, GREEN, alpha=k3)
        text(d, (W / 2, 1495), "nhiệt mất ra ngoài", 48, GREEN, alpha=k3)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    """Dau nhiet ke dat sat day dien tro (khong noi chieu lech)."""
    if k <= 0: return
    card(d, (250, 960, 830, 1280), fill=A((250, 252, 255), k), outline=A((150, 175, 205), k), r=20, w=4)
    d.rounded_rectangle([256, 1030, 824, 1274], radius=16, fill=A((175, 212, 250), k))
    zz = [(360 + 26 * j, 1200 + (16 if j % 2 else -16)) for j in range(12)]
    d.line(zz, fill=A(WIRE_C, k), width=8, joint="curve")
    d.line(zz, fill=A((255, 140, 60), 0.4 * k), width=18, joint="curve")
    d.line([(560, 940), (560, 1170)], fill=A((90, 96, 110), k), width=12)
    dot(d, 560, 1172, 11, A(NAVY, k))
    text(d, (545, 1080), "nhiệt kế", 44, INK, anchor="rm", alpha=k)
    text(d, (600, 1080), "điện trở", 44, WIRE_C, anchor="lm", alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Mất nhiệt: Δt nhỏ đi,\nc đo lớn hơn thật",
             "Nhiệt kế sát điện trở: c lớn hay nhỏ hơn 4 348?", None, body=_end_body)
    kh = appear(t, M[0] + 4.5, 0.5)                 # goi y tre >= 4 s; cau hoi trung tinh, khong neu cach lam
    if kh > 0:
        card(d, (110, 1320, 970, 1560), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1375), "Gợi ý", 44, MUTED, bold=False, alpha=kh)
        text(d, (W / 2, 1475), "Nhiệt kế đọc cao hay thấp?", 48, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, v, b, e = sc["hook"], sc["do"], sc["ket"], sc["visao"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + m, "tap") for m in MARKS]
    out += [(k["t0"] + k["M"][1] + 0.1, "ding"), (v["t0"] + v["M"][1] - 0.15, "tap"),
            (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-noinang-02", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Nội năng · Định luật 1 NĐLH · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo c của nước", draw=s_hook, tail=0.3, caps=[
   ("Bình có nắp đậy.", 2.6),
   ("Tự đoán trước.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Khuấy đều, cứ 20 s ghi một lần.", 4.0),
   ("Gần như thẳng hàng.", 3.0)]),
 dict(key="ket", title="Kết quả", draw=s_ket, tail=0.4, caps=[
   ("Tính c ở từng mốc.", 2.8),
   ("So với sách.", 3.4)]),
 dict(key="visao", title="Vì sao lớn hơn?", draw=s_vi_sao, tail=0.3, caps=[
   ("Nhiệt không vào hết nước.", 5.4),
   ("Chưa nói được?", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Do nhiệt kế?", 3.4),
   ("Một phía.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 7.8)]),
])
