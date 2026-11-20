# Clip: tn-l10-nemngang-01 - Mot bi ban ngang, mot bi tha roi cung luc (lo 11, 19/11/2026; dung lai 20/11/2026 theo
# KE-HOACH-CAI-TIEN-CLIP viec 4: cong --do-chu, chu >= 55 px khi ve, canh Bay ve lai, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-nemngang-01.json (_kiem_so() doi chieu):
#   tham_so: g = 9,8 m/s2 ; so_lieu_mau (h, v0, t, L): 0,5 2 0,319 0,64 | 0,8 2 0,404 0,81 | 0,8 5 0,404 2,02 | 1,25 5 0,505 2,53
#   Clip chieu hang 3 va 4 (cung v0 = 5 m/s, h 0,80 -> 1,25 m). Hang 1 dung cho cau THU NGHI (= cau_chot khung web).
# Du doan (K10: khong nut A-D, chi cau hoi + hinh): giu v0 = 5 m/s, nang mang 0,80 -> 1,25 m: thoi gian roi va tam xa?
#   -> dap an: ca hai tang (0,505 s ; 2,53 m).
# Duong cong (cong B 20/11): lan 1 (0,80 m) mau hong dam, lan 2 (1,25 m) mau xam xanh dam -- khac mau bi A/B va hop ket qua; nhan "lan 1 (0,80 m)"/"lan 2 (1,25 m)".
# Bay = sai_so_thuong_gap "hai vien khong duoc tha dung cung luc": hai khung xep tren duoi, khung tren gat A muon
#   (do tre phong dai de nhin thay, KHONG ghi so), dung hinh luc B cham san ; khung duoi tha cung luc. Khong chu gach ngang.
# Chua noi duoc: gia_thiet "bo qua luc can" -> luc can lon thi sao.
# Thu nghi: h = 0,50 m, v0 = 2 m/s (g = 9,8) -> L = 0,64 m (hang 1, khong hien dap so; khung web hoi A-D).
from engine import *

G = 9.8
ROWS = [(0.8, 5, 0.404, 2.02), (1.25, 5, 0.505, 2.53)]                # so_lieu_mau hang 3, 4
CHOT = (0.5, 2, 0.319, 0.64)                                           # so_lieu_mau hang 1 (cau chot)
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-nemngang-01.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    for r in ROWS + [CHOT]:
        assert any(all(abs(a - b) < 1e-9 for a, b in zip(r, h)) for h in hang), r
        assert abs(math.sqrt(2 * r[0] / G) - r[2]) < 6e-4 and abs(r[1] * r[2] - r[3]) < 6e-3, r
    assert {p["ky_hieu"]: p for p in k["tham_so"]}["g"]["gia_tri"] == G
_kiem_so()


STEEL_A = (37, 99, 235); STEEL_B = (234, 88, 12); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
METAL = (150, 160, 180); EMPTY = (148, 140, 128)
CURVE = ((190, 24, 93), (51, 65, 85))   # lan 1 hong dam, lan 2 xam xanh dam

# ---------------- hinh hoc: (x0 = dau mang, yf = mat san, pxm = px/m) ----------------
GEO = (250, 1000, 280.0)                 # khung chinh: L = 2,53 m -> x = 958, le phai 80 px
GEO_H = (340, 1000, 546.0)               # canh Du doan: chi can do cao, phong to 1,3x
def P(g, x, y): return (g[0] + x * g[2], g[1] - y * g[2])
def xb(g): return g[0] - 55                # bi B kep ngay truoc dau mang, cung do cao

def ball(d, x, y, col, lab=None, side="up", a=1.0, r=22):
    dot(d, x, y, r, A(col, a), outline=A(NAVY, a))
    if lab:
        if side == "up": text(d, (x, y - r - 40), lab, 62, col, alpha=a)
        else: text(d, (x - r - 34, y), lab, 62, col, alpha=a)

def dash_h(d, x1, x2, y, col, w=5):
    x = x1
    while x < x2: d.line([(x, y), (min(x + 18, x2), y)], fill=col, width=w); x += 32

def setup(d, h, g=GEO, ruler=True, hlab=True):
    YL = P(g, 0, h)[1]; X0, YF = g[0], g[1]; XB = xb(g)
    d.rectangle([45, YL + 22, XB - 45, YF], fill=WOOD, outline=WOOD_D, width=3)                     # ban
    d.rectangle([40, YF, 1040, YF + 18], fill=(205, 196, 180))                                       # san
    d.polygon([(X0 - 192, YL - 62), (X0 - 132, YL + 16), (X0 - 132, YL + 24), (X0 - 200, YL - 56)], fill=METAL)
    d.rectangle([X0 - 132, YL + 16, X0 + 2, YL + 24], fill=METAL)                                    # mang, dau ra ngang
    d.line([(XB, YL - 110), (XB, YL - 30)], fill=NAVY, width=5)                                      # kep giu bi B
    d.line([(XB - 14, YL - 30), (XB + 14, YL - 30)], fill=NAVY, width=5)
    if ruler:                                                                                        # thuoc cuon tren san
        d.rectangle([X0, YF + 18, P(g, 2.6, 0)[0], YF + 40], fill=(253, 224, 71), outline=WOOD_D, width=2)
        for k in range(0, 11):
            xx = P(g, k * 0.25, 0)[0]; L = 22 if k % 2 == 0 else 12
            d.line([(xx, YF + 18), (xx, YF + 18 + L)], fill=NAVY, width=4)
            if k % 2 == 0 and k < 10: text(d, (xx, YF + 80), "0" if k == 0 else vn(k * 0.25, 1).replace(",0", ""), 62, NAVY)
        text(d, (P(g, 2.5, 0)[0] - 12, YF + 80), "2,5 m", 62, NAVY)
    if hlab:                                                                                         # vach do cao
        xm = XB - 90
        d.line([(xm, YL), (xm, YF)], fill=PURPLE, width=5)
        for yy in (YL, YF): d.line([(xm - 12, yy), (xm + 12, yy)], fill=PURPLE, width=5)
        text(d, (XB + 34, (YL + YF) / 2 + 20), vn(h) + " m", 62, PURPLE, anchor="lm")

def path(d, g, h, v0, tau, col, w=7):
    if tau <= 0: return
    pts = [P(g, v0 * tau * s / 40, h - G / 2 * (tau * s / 40) ** 2) for s in range(41)]
    d.line(pts, fill=col, width=w)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o, tat lan luot tu PHAI sang TRAI (mot chieu); o da tat: nen trang, vien dam."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 190 + i * 145
        if i < on: card(d, (x, y, x + 120, y + 40), fill=A(col, a), r=14)
        else: card(d, (x, y, x + 120, y + 40), fill=A(WHITE, a), outline=A(EMPTY, a), r=14, w=4)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; h = ROWS[0][0]; g = GEO_H; YL = P(g, 0, h)[1]
    card(d, (40, 205, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    setup(d, h, g, ruler=False)
    ball(d, g[0] - 6, YL, STEEL_A, "A", r=30); ball(d, xb(g), YL, STEEL_B, "B", side="left", r=30)
    ka = appear(t, 0.8, 0.5)
    arrow(d, (g[0] + 36, YL), (g[0] + 240, YL), A(BLUE, ka), w=8, head=24)
    text(d, (g[0] + 190, YL + 72), "v₀ = 5 m/s", 62, BLUE, alpha=ka)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y2 = P(g, 0, ROWS[1][0])[1]                                              # muc 1,25 m can hoi
    dash_h(d, 60, g[0] + 40, y2, A(PURPLE, a))
    arrow(d, (g[0] - 250, YL - 70), (g[0] - 250, y2 + 14), A(PURPLE, a), w=7, head=22)
    text(d, (g[0] + 60, y2), "1,25 m ?", 64, PURPLE, anchor="lm", alpha=a)
    y0 = 1115 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 98), fill=A(PURPLE, a), r=36)
    text(d, (W / 2, y0 + 60), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 150), "Nâng máng lên 1,25 m,", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 225), "v₀ giữ nguyên.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 305), "Thời gian rơi và tầm xa", 60, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 380), "đổi thế nào?", 60, PURPLE, alpha=a)
    seg_bar(d, y0 + 425, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (2 lan, chieu cham 5 lan) ----------------
SLOW = 5.0
STARTS = (0.6, 4.0)                    # luc gat/tha moi lan (giay trong canh)
LAB = (("lần 1 (0,80 m)", (232, 945)), ("lần 2 (1,25 m)", (640, 600)))   # (232 = can trai), (640 = can giua)
def run_state(t):
    """-> (lan j, tau that (0..t_roi), so hang bang da xong)."""
    j = 1 if t >= STARTS[1] else 0
    tt = ROWS[j][2]
    tau = clamp((t - STARTS[j]) / SLOW, 0.0, tt)
    rows = j + (1 if (t - STARTS[j]) / SLOW >= tt else 0)
    return j, tau, rows

def flight(d, j, tau, labels=(False, False)):
    g = GEO; h, v0, tt, L = ROWS[j]; YL = P(g, 0, h)[1]; XB = xb(g)
    if j == 1:                                                              # duong lan 1 giu lai (tu 0,80 m)
        path(d, g, ROWS[0][0], ROWS[0][1], ROWS[0][2], CURVE[0])
        lx = P(g, ROWS[0][3], 0)[0]; d.line([(lx, g[1] - 24), (lx, g[1] + 2)], fill=CURVE[0], width=8)
    path(d, g, h, v0, tau, CURVE[j])
    ya = P(g, 0, h - G / 2 * tau * tau)[1]; yy = min(ya, g[1] - 22)
    if tau > 0: d.line([(XB, YL), (XB, yy)], fill=A(STEEL_B, 0.55), width=5)
    xa = P(g, v0 * tau, 0)[0]
    if tau > 0: dash_h(d, XB + 28, xa - 28, yy, DGREEN, w=4)                # vach ngang noi hai bi: cung do cao
    if tau >= tt - 1e-9: d.line([(xa, g[1] - 24), (xa, g[1] + 2)], fill=CURVE[j], width=8)
    for i in (0, 1):
        if labels[i]:
            s, (x, y) = LAB[i]
            text(d, (x, y), s, 62, CURVE[i], anchor="lm" if i == 0 else "mm")
    ball(d, XB, yy, STEEL_B, "B", side="left"); ball(d, xa if tau > 0 else g[0] - 4, yy, STEEL_A, "A")

def clock(d, x, lab, col, val):
    card(d, (x - 230, 212, x + 230, 338), fill=WHITE, outline=col, w=5, r=26)
    text(d, (x - 120, 275), lab, 60, col)
    text(d, (x + 95, 275), vn(val, 3) + " s", 62, INK)

def table(d, y, n, hl=-1):
    card(d, (40, y, 1040, y + 340), fill=WHITE, outline=NAVY, w=4)
    xs = (175, 420, 665, 905)
    text(d, (xs[0], y + 58), "h (m)", 62, PURPLE)
    text(d, (xs[1], y + 58), "t A (s)", 62, STEEL_A); text(d, (xs[2], y + 58), "t B (s)", 62, STEEL_B)
    text(d, (xs[3], y + 58), "L (m)", 62, DORANGE)
    d.line([(70, y + 108), (1010, y + 108)], fill=NAVY, width=3)
    for i in range(n):
        yy = y + 172 + i * 100; h, v0, tt, L = ROWS[i]
        if i == hl: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=16, fill=(255, 237, 213))
        text(d, (xs[0], yy), vn(h), 62, INK); text(d, (xs[1], yy), vn(tt, 3), 62, INK)
        text(d, (xs[2], yy), vn(tt, 3), 62, INK); text(d, (xs[3], yy), vn(L), 62, INK)

def s_do(img, d, t, sc):
    j, tau, rows = run_state(t)
    card(d, (40, 205, 1040, 1110), fill=WHITE, outline=LIGHT, w=3)
    setup(d, ROWS[j][0], hlab=(rows == 0))
    clock(d, 290, "Bi A", STEEL_A, tau); clock(d, 790, "Bi B", STEEL_B, tau)
    text(d, (W / 2, 395), "chiếu chậm 5 lần", 60, INK)
    text(d, (1010, 475), "v₀ = 5 m/s", 62, BLUE, anchor="rm")
    flight(d, j, tau, labels=(rows >= 1, j == 1))
    table(d, 1140, rows, hl=rows - 1 if rows > j else -1)

def _kiem_dong_bo():
    """Moi 0,05 s: hai dong ho bang nhau va dung dung luc cham san; hang bang chi hien khi bi da cham."""
    bad = []; t = 0.0
    while t < 8.0:
        j, tau, rows = run_state(t)
        h, v0, tt, L = ROWS[j]
        if h - G / 2 * tau * tau < -1e-6: bad.append((round(t, 2), "bi xuyen san"))
        if rows > j and abs(tau - tt) > 1e-9: bad.append((round(t, 2), "hang hien truoc khi cham"))
        if abs(tau - tt) < 1e-9 and rows <= j: bad.append((round(t, 2), "da cham ma chua co hang"))
        t += 0.05
    if run_state(STARTS[1] - 0.05)[2] != 1: bad.append("lan 1 chua xong truoc lan 2")
    if run_state(7.0)[2] != 2: bad.append("chua du 2 hang")
    return bad

# ---------------- canh 3: Dap an + Rut ra (t va L hai nhip rieng, sau phu de tuong ung) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; tt = ROWS[1][2]
    card(d, (40, 205, 1040, 1110), fill=WHITE, outline=LIGHT, w=3)
    setup(d, ROWS[1][0], hlab=False)
    clock(d, 290, "Bi A", STEEL_A, tt); clock(d, 790, "Bi B", STEEL_B, tt)
    text(d, (1010, 475), "v₀ = 5 m/s", 62, BLUE, anchor="rm")
    flight(d, 1, tt, labels=(True, True))
    k1 = appear(t, M[1] - 0.1, 0.5)
    if k1 > 0:
        card(d, (60, 1150, 1020, 1370), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=5)
        text(d, (W / 2, 1210), "t = √(2h/g)", 64, DGREEN, alpha=k1)
        text(d, (W / 2, 1305), "0,404 s → 0,505 s", 62, DGREEN, alpha=k1)
    k2 = appear(t, M[2] - 0.1, 0.5)
    if k2 > 0:
        card(d, (60, 1400, 1020, 1620), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), r=24, w=5)
        text(d, (W / 2, 1460), "L = v₀·t", 64, DORANGE, alpha=k2)
        text(d, (W / 2, 1555), "2,02 m → 2,53 m", 62, DORANGE, alpha=k2)

# ---------------- canh 4: Bay - hai bi tha lech nhau (khung tren) / tha cung luc (khung duoi) ----------------
GEO_T = (200, 715, 400.0); GEO_D = (200, 1410, 400.0)
LECH = 0.08                            # do tre phong dai de nhin thay (giay that), khong hien so
B_START = (0.6, 7.7)
RB = 40                                # ban kinh bi trong canh bay (ra 283 px: ~21 px)
def panel(d, g, t, start, tre, col, lab=None):
    h, v0, tt, L = ROWS[0]; YL = P(g, 0, h)[1]; XB = xb(g); YF = g[1]
    card(d, (40, YF - 510, 1040, YF + 45), fill=WHITE, outline=col, w=6)
    setup(d, h, g, ruler=False, hlab=False)
    if lab: text(d, (1010, YF - 445), lab, 64, col, anchor="rm")
    tb = clamp((t - start) / SLOW, 0.0, tt)                                  # dung hinh luc B cham san
    ta = clamp(tb - tre, 0.0, tt)
    yb = min(P(g, 0, h - G / 2 * tb * tb)[1], YF - RB); ya = min(P(g, 0, h - G / 2 * ta * ta)[1], YF - RB)
    path(d, g, h, v0, ta, STEEL_A, w=6)
    if tb > 0: d.line([(XB, YL), (XB, yb)], fill=A(STEEL_B, 0.55), width=6)
    xa = P(g, v0 * ta, 0)[0] if ta > 0 else g[0] - 4
    landed = tb >= tt - 1e-9
    if tre == 0 and tb > 0: dash_h(d, XB + RB + 6, xa - RB - 6, yb, DGREEN, w=5)
    if tre > 0 and landed:                                                   # ngoac do: A con cach san
        bx = xa + RB + 26
        d.line([(bx, ya), (bx, YF)], fill=DRED, width=6)
        for yy in (ya, YF): d.line([(bx - 14, yy), (bx + 14, yy)], fill=DRED, width=6)
        text(d, (xa - RB - 24, ya - 6), "A còn cách sàn", 60, DRED, anchor="rm")
        text(d, (XB + RB + 20, YF - 32), "B đã chạm sàn", 60, STEEL_B, anchor="lm")
    ball(d, XB, yb, STEEL_B, "B", side="left", r=RB); ball(d, xa, ya, STEEL_A, "A", r=RB)
    return landed

def tag(d, y, s, col, fill, a):
    card(d, (60, y, 1020, y + 105), fill=A(fill, a), outline=A(col, a), r=24, w=6)
    text(d, (W / 2, y + 52), s, 62, col, alpha=a)

def s_bay(img, d, t, sc):
    M = sc["M"]
    panel(d, GEO_T, t, B_START[0], LECH, DRED, "Gạt A muộn")
    tag(d, 772, "✗ Dễ tưởng: A rơi lâu hơn", DRED, (254, 242, 242), appear(t, M[1] + 0.5, 0.45))
    kd = appear(t, M[2] - 0.1, 0.4)
    if kd > 0:
        landed = panel(d, GEO_D, t, B_START[1], 0.0, DGREEN)
        if landed: tag(d, 1470, "✓ Chạm sàn cùng lúc", DGREEN, (236, 253, 243), 1.0)

# ---------------- canh 5: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 205, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 290), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 440), "Lực cản lớn thì sao?", 62, INK)
    k = appear(t, 2.0, 0.5)                                                   # luc can NGUOC chieu van toc moi bi
    if k <= 0: return
    card(d, (40, 590, 1040, 1300), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    x0, y0, xa, yb = 300, 650, 760, 1000
    d.line([(x0, y0), (x0, yb - 34)], fill=A(STEEL_B, 0.6 * k), width=6)                    # B roi thang
    s2 = lambda u: (x0 + (xa - x0) * u, y0 + (yb - y0) * u * u)                            # A: parabol toi (xa, yb)
    d.line([s2(i / 30) for i in range(31)], fill=A(STEEL_A, 0.6 * k), width=6)
    # B: van toc huong xuong -> luc can huong len
    arrow(d, (x0, yb - 36), (x0, yb - 200), A(DRED, k), w=9, head=28)
    text(d, (x0 + 30, yb - 150), "lực cản", 60, DRED, anchor="lm", alpha=k)
    # A: van toc theo tiep tuyen (xuong, sang phai) -> luc can nguoc lai (len, sang trai)
    vx, vy = (xa - x0), 2 * (yb - y0); n = math.hypot(vx, vy); ux, uy = -vx / n, -vy / n
    arrow(d, (xa + ux * 36, yb + uy * 36), (xa + ux * 200, yb + uy * 200), A(DRED, k), w=9, head=28)
    for x, col, lab in ((x0, STEEL_B, "B"), (xa, STEEL_A, "A")):
        dot(d, x, yb, 32, A(col, k), outline=A(NAVY, k))
        text(d, (x - 70 if lab == "B" else x + 75, yb), lab, 64, col, alpha=k)
    d.rectangle([60, 1060, 1020, 1080], fill=A((205, 196, 180), k))

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web), hinh ca h = 0,50 m ----------------
GEO_E = (330, 1060, 600.0)
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1520), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 238, W / 2 + pw / 2, 314), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 276), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    g = GEO_E; h, v0 = CHOT[0], CHOT[1]; YL = P(g, 0, h)[1]; XB = xb(g); YF = g[1]
    d.rectangle([45, YL + 22, XB - 20, YF], fill=A(WOOD, k1), outline=A(WOOD_D, k1), width=3)
    d.rectangle([60, YF, 1020, YF + 18], fill=A((205, 196, 180), k1))
    d.polygon([(g[0] - 192, YL - 62), (g[0] - 132, YL + 16), (g[0] - 132, YL + 24), (g[0] - 200, YL - 56)], fill=A(METAL, k1))
    d.rectangle([g[0] - 132, YL + 16, g[0] + 2, YL + 24], fill=A(METAL, k1))
    xm = XB + 40
    d.line([(xm, YL + 40), (xm, YF)], fill=A(PURPLE, k1), width=5)
    for yy in (YL + 40, YF): d.line([(xm - 12, yy), (xm + 12, yy)], fill=A(PURPLE, k1), width=5)
    text(d, (xm + 24, (YL + YF) / 2 + 30), "0,50 m", 62, PURPLE, anchor="lm", alpha=k1)
    ball(d, g[0] - 6, YL, STEEL_A, "A", r=30, a=k1)
    arrow(d, (g[0] + 36, YL), (g[0] + 240, YL), A(BLUE, k1), w=8, head=24)
    text(d, (g[0] + 330, YL), "v₀ = 2 m/s", 62, BLUE, anchor="lm", alpha=k1)
    text(d, (1010, 400), "g = 9,8 m/s²", 60, INK, anchor="rm", alpha=k1)
    text(d, (850, YF - 60), "?", 90, DORANGE, alpha=k1)
    text(d, (W / 2, 1230), "Bi A bay xa bao nhiêu?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1360, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + s + r[2] * SLOW, "tap") for s, r in zip(STARTS, ROWS)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + b["M"][1] + 0.5, "buzz"), (b["t0"] + B_START[1] + ROWS[0][2] * SLOW, "tap"),
            (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l10-nemngang-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động ném · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bắn ngang và thả rơi", draw=s_hook, tail=0.3, caps=[
   ("Bi A bắn ngang, bi B thả rơi.", 3.4),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Lần 1: máng cao 0,80 m.", 3.6),
   ("Lần 2: nâng máng lên 1,25 m.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Hai đồng hồ bằng nhau.", 3.0),
   ("Cao hơn: rơi lâu hơn.", 3.0),
   ("Cùng v₀ nên bay xa hơn.", 3.0)]),
 dict(key="bay", title="Bẫy: thả lệch nhau", draw=s_bay, tail=0.4, caps=[
   ("Hai bi thả lệch nhau.", 3.4),
   ("Đừng vội kết luận.", 3.8),
   ("Thả lại cho cùng lúc.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.6, caps=[
   ("Ở đây bỏ qua lực cản.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Độ cao quyết định thời gian rơi.", 4.6)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
