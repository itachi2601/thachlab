# Clip: tn-l10-giaibt-dlh-02 - He xe lan va qua nang noi day qua rong roc (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-giaibt-dlh-02.json:
#   tham_so: m1 = 0,40 kg, m2 = 0,10 kg, s = 0,8 m, g = 10 (mo_hinh.gia_thiet), sai_so_do t = 0,02 s
#   so_lieu_mau: t = 0,93 / 0,95 / 0,92 / 0,94 / 0,93 s -> a = 1,85 / 1,77 / 1,89 / 1,81 / 1,85 m/s2;
#   du doan bo ma sat 2,0 m/s2; trung binh ~ 1,83 (ket_qua_ky_vong, rut_ra).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (lan 1, chieu cham 3 lan) -> Dap an C (bang + 5 diem duoi vach 2,0)
#       -> Vi sao 2,0 (dinh luat II tung vat, cong lai) -> Vi sao do nho hon (sai so he thong)
#       -> Bay T = m2 g + chua noi duoc -> Chot + cau hoi tu nho lai (m2 = 0,40 kg, bo ma sat: a = ?).
# Lua chon Du doan (o khung web, khong ve trong mp4): A lon hon 2,0 ca 5 lan · B luc lon luc nho quanh 2,0
#   · C nho hon 2,0 ca 5 lan (dung) · D dung bang 2,0.
from engine import *

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); STEEL = (90, 98, 120)
T_RUN = 0.93                       # s, lan 1 (so_lieu_mau)
SLOW = 3.0                         # chieu cham 3 lan
ROWS = [(1, 0.93, 1.85), (2, 0.95, 1.77), (3, 0.92, 1.89), (4, 0.94, 1.81), (5, 0.93, 1.85)]   # so_lieu_mau
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def rig(d, x0, y0, k, s, gate=True, clock=None, done=False, labels=True):
    """Ban + xe + rong roc + qua nang. (x0, y0) = mep trai mat ban; k = ti le; s = 0..1 phan quang duong 0,80 m."""
    D = 560 * k                                     # 0,80 m tren man
    xp, yp, rp = x0 + 830 * k, y0 - 30 * k, 30 * k  # rong roc kep mep ban
    d.rectangle([x0, y0, x0 + 820 * k, y0 + 30 * k], fill=WOOD, outline=WOOD_D, width=3)
    d.rectangle([x0 + 812 * k, y0 - 6 * k, x0 + 840 * k, y0 + 40 * k], fill=STEEL)          # kep
    d.line([(x0 + 826 * k, y0 - 4 * k), (xp, yp)], fill=STEEL, width=max(3, int(8 * k)))
    cx = x0 + 20 * k + D * s                         # mep sau xe
    cw, ch = 150 * k, 60 * k
    hook_y = y0 - 60 * k
    # day: xe -> dinh rong roc -> xuong qua nang
    my = y0 + 40 * k + D * s
    d.line([(cx + cw, hook_y), (xp, hook_y)], fill=INK, width=3)
    d.line([(xp + rp, yp), (xp + rp, my)], fill=INK, width=3)
    d.ellipse([xp - rp, yp - rp, xp + rp, yp + rp], fill=WHITE, outline=STEEL, width=max(3, int(6 * k)))
    dot(d, xp, yp, 5 * k + 2, STEEL)
    # xe lan
    card(d, (cx, y0 - 28 * k - ch, cx + cw, y0 - 28 * k), fill=BLUE, outline=NAVY, r=int(10 * k), w=3)
    for wx in (cx + 32 * k, cx + cw - 32 * k):
        dot(d, wx, y0 - 14 * k, 14 * k, NAVY); dot(d, wx, y0 - 14 * k, 5 * k, LIGHT)
    # qua nang
    mw, mh = 70 * k, 80 * k
    card(d, (xp + rp - mw / 2, my, xp + rp + mw / 2, my + mh), fill=ORANGE, outline=(160, 60, 10), r=int(10 * k), w=3)
    if labels:
        text(d, (cx + cw / 2, y0 + 30 * k + 40), "0,40 kg", max(36, int(40 * k)), BLUE)
        text(d, (xp + rp - mw / 2 - 18, my + mh / 2), "0,10 kg", max(36, int(40 * k)), ORANGE, anchor="rm")
    if gate:
        g0, g1 = x0 + 170 * k, x0 + 170 * k + D          # vach xuat phat (mui xe) va cong quang o 0,80 m
        for yy in range(int(y0 - 120 * k), int(y0 - 4), 22):
            d.line([(g0, yy), (g0, yy + 11)], fill=GRAY, width=4)
        d.rectangle([g1 - 8, y0 - 150 * k, g1 + 8, y0 - 2], fill=RED)
        d.rectangle([g1 - 30, y0 - 160 * k, g1 + 30, y0 - 130 * k], fill=RED)
        ya = y0 - 190 * k
        arrow(d, (g0 + 40, ya), (g0 + 4, ya), INK, w=4, head=16); arrow(d, (g1 - 40, ya), (g1 - 4, ya), INK, w=4, head=16)
        d.line([(g0 + 40, ya), (g1 - 40, ya)], fill=INK, width=4)
        d.rectangle([(g0 + g1) / 2 - 90, ya - 28, (g0 + g1) / 2 + 90, ya + 28], fill=BG)
        text(d, ((g0 + g1) / 2, ya), "0,80 m", 40, INK)
    if clock is not None:
        bx = (180, y0 + 220 * k, 640, y0 + 340 * k)
        card(d, bx, fill=(236, 253, 243) if done else (255, 247, 237), outline=GREEN if done else ORANGE, r=24, w=4)
        text(d, ((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2), f"t = {vn(clock)} s", 52, GREEN if done else INK)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    rig(d, 90, 560, 0.95, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 175, "Tính theo định luật II: a = 2,0 m/s²", 46, NAVY, maxw=900, alpha=a)
    ctext(d, y0 + 320, "Đo thật 5 lần, a đo so với 2,0 thế nào?", 50, INK, maxw=860, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 514], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 514], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def run_start(sc): return sc["M"][0] + 0.6
def real_t(t, sc): return clamp((t - run_start(sc)) / SLOW, 0, T_RUN)

def s_do(img, d, t, sc):
    tr = real_t(t, sc); s = (tr / T_RUN) ** 2                 # tu nghi: x = a t^2 / 2
    done = tr >= T_RUN - 1e-6
    card(d, (40, 265, 1040, 1600), fill=WHITE, outline=LIGHT, w=3)
    rig(d, 80, 640, 1.0, s, clock=tr, done=done)
    k = appear(t, run_start(sc) - 0.6, 0.4) * (1 - appear(t, run_start(sc) + 0.4, 0.3))
    if k > 0:
        card(d, (180, 1380, 640, 1470), fill=A(ORANGE, k), r=40)
        text(d, (410, 1425), "Thả!", 46, WHITE, alpha=k)
    if t > run_start(sc) + 0.4 and not done:
        text(d, (410, 1425), "chiếu chậm 3 lần", 42, INK, alpha=appear(t, run_start(sc) + 0.4, 0.4))
    if done:
        text(d, (410, 1425), "Lần 1", 48, GREEN, alpha=appear(t, run_start(sc) + T_RUN * SLOW, 0.4))

# ---------------- canh 3: Dap an + bang + 5 diem ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    pw = tw(d, "ĐÁP ÁN C", F(38)) + 56
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 314), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 282), "ĐÁP ÁN C", 38, WHITE, alpha=ka)
    card(d, (40, 340, 1040, 460), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5)
    ctext(d, 400, "Cả 5 lần đều nhỏ hơn 2,0", 48, GREEN, maxw=900, alpha=ka)
    # bang so lieu
    y = 490
    card(d, (40, y, 1040, y + 560), fill=WHITE, outline=LIGHT, w=3)
    XS = (230, 540, 850)
    for x, s in zip(XS, ("Lần", "t (s)", "a (m/s²)")): text(d, (x, y + 50), s, 40, INK)
    d.line([(70, y + 92), (1010, y + 92)], fill=LIGHT, width=3)
    for j, (n, tt, a) in enumerate(ROWS):
        k = appear(t, M[0] + 0.1 + 0.25 * j, 0.35); yy = y + 140 + j * 88
        text(d, (XS[0], yy), str(n), 44, INK, alpha=k)
        text(d, (XS[1], yy), vn(tt), 44, NAVY, alpha=k)
        text(d, (XS[2], yy), vn(a), 44, NAVY, alpha=k)
    # do thi diem: a theo lan do, vach 2,0
    py0, py1 = 1080, 1600
    card(d, (40, py0, 1040, py1), fill=WHITE, outline=LIGHT, w=3)
    def ya(v): return py1 - 110 - (v - 1.70) / (2.05 - 1.70) * (py1 - py0 - 200)
    kl = appear(t, M[0] + 0.1, 0.4)
    text(d, (70, py0 + 40), "a (m/s²)", 40, INK, anchor="lm", alpha=kl)
    text(d, (1010, py0 + 40), "trục không bắt đầu từ 0", 38, MUTED, anchor="rm", alpha=kl)
    d.line([(190, ya(1.70)), (190, ya(2.05))], fill=A(INK, kl), width=3)
    d.line([(190, ya(1.70)), (880, ya(1.70))], fill=A(INK, kl), width=3)
    for v in (1.7, 1.8, 1.9):
        d.line([(180, ya(v)), (200, ya(v))], fill=A(INK, kl), width=3)
        text(d, (170, ya(v)), vn(v, 1), 38, INK, anchor="rm", alpha=kl)
    y2 = ya(2.0)
    text(d, (170, y2), "2,0", 40, RED, anchor="rm", alpha=kl)
    for xx in range(200, 860, 36):
        d.line([(xx, y2), (xx + 20, y2)], fill=A(RED, kl), width=5)
    text(d, (900, y2), "tính", 40, RED, anchor="lm", alpha=kl)
    text(d, (940, ya(1.70)), "lần", 38, INK, anchor="lm", alpha=kl)
    for j, (n, tt, a) in enumerate(ROWS):
        k = appear(t, M[0] + 0.1 + 0.25 * j, 0.35)
        if k <= 0: continue
        x = 300 + j * 130
        dot(d, x, ya(a), 18 * k, BLUE)
        text(d, (x, ya(1.70) + 40), str(n), 40, INK, alpha=k)

# ---------------- canh 4: Vi sao 2,0 (dinh luat II tung vat) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 860), fill=WHITE, outline=LIGHT, w=3)
    # xe tach rieng: P, N bang nhau; T goc o mep truoc xe
    card(d, (200, 520, 380, 600), fill=BLUE, outline=NAVY, r=12, w=3)
    for wx in (240, 340):
        dot(d, wx, 614, 14, NAVY); dot(d, wx, 614, 5, LIGHT)
    text(d, (290, 560), "xe", 40, WHITE)
    arrow(d, (290, 520), (290, 380), GREEN, w=7)
    rich(d, 330, 400, "N", 44, GREEN)
    arrow(d, (290, 628), (290, 768), BLUE, w=7)
    rich(d, 330, 748, "P", 44, BLUE)
    arrow(d, (380, 560), (530, 560), TEAL, w=7)
    rich(d, 490, 515, "T", 44, TEAL)
    kpn = appear(t, M[0] + 0.6, 0.4)
    text(d, (290, 815), "P, N triệt tiêu", 40, INK, alpha=kpn)
    # qua nang tach rieng: T = 0,8 N, m2 g = 1,0 N -> ti le 160 : 200
    card(d, (755, 510, 845, 610), fill=ORANGE, outline=(160, 60, 10), r=12, w=3)
    arrow(d, (800, 510), (800, 350), TEAL, w=7)
    rich(d, 840, 380, "T", 44, TEAL)
    arrow(d, (800, 610), (800, 810), BLUE, w=7)
    rich(d, 830, 780, "m_{2}g", 44, BLUE, anchor="l")
    text(d, (860, 560), "quả nặng", 40, ORANGE, anchor="lm")
    k1 = appear(t, 0.3, 0.45)
    card(d, (40, 880, 1040, 1600), fill=A(WHITE, k1), outline=A(NAVY, k1), w=5)
    rich(d, W / 2, 935, "m_{1} = 0,40 kg   m_{2} = 0,10 kg   g = 10 m/s²", 40, INK, alpha=k1)
    text(d, (W / 2, 995), "Bỏ ma sát · chiều (+) là chiều chuyển động", 38, MUTED, alpha=k1)
    kx = appear(t, M[0] + 1.0, 0.45)
    text(d, (110, 1080), "Xe:", 44, MUTED, anchor="lm", alpha=kx)
    rich(d, 420, 1080, "T = m_{1}a", 52, INK, alpha=kx, anchor="l")
    k2 = appear(t, M[0] + 1.8, 0.45)
    text(d, (110, 1170), "Quả nặng:", 44, MUTED, anchor="lm", alpha=k2)
    rich(d, 420, 1170, "m_{2}g − T = m_{2}a", 52, INK, alpha=k2, anchor="l")
    st = clamp((t - M[1] - 0.3) / 0.6)
    if st > 0:                                                                # gach T o hai dong
        for (xa, yy) in ((420, 1080), (420 + tw(d, "m", F(52)) + tw(d, "2", F(31)) + tw(d, "g − ", F(52)), 1170)):
            wt = tw(d, "T", F(52))
            d.line([(xa - 4, yy + 18), (xa - 4 + (wt + 8) * st, yy - 18)], fill=RED, width=6)
    k3 = appear(t, M[1] + 1.0, 0.5)
    if k3 > 0:
        arrow(d, (W / 2, 1215), (W / 2, 1265), A(MUTED, k3), w=6, head=16)
        card(d, (90, 1280, 990, 1420), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        rich(d, W / 2, 1350, "a = m_{2}g / (m_{1} + m_{2})", 54, GREEN, alpha=k3)
        k4 = appear(t, M[1] + 1.8, 0.5)
        text(d, (W / 2, 1505), "= 2,0 m/s²", 56, GREEN, alpha=k4)

# ---------------- canh 5: Vi sao do nho hon ----------------
def s_heso(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 860), fill=WHITE, outline=LIGHT, w=3)
    x0, y0, k = 90, 520, 0.95
    rig(d, x0, y0, k, 0.1, gate=False, labels=False)
    D = 560 * k; cx = x0 + 20 * k + D * 0.1; cw = 150 * k
    xp, yp, rp = x0 + 830 * k, y0 - 30 * k, 30 * k
    kf = appear(t, M[0] + 0.3, 0.4)
    for wx in (cx + 32 * k, cx + cw - 32 * k):                              # vong do o truc banh, rong roc
        d.ellipse([wx - 26, y0 - 14 * k - 26, wx + 26, y0 - 14 * k + 26], outline=A(RED, kf), width=6)
    d.ellipse([xp - rp - 14, yp - rp - 14, xp + rp + 14, yp + rp + 14], outline=A(RED, kf), width=6)
    arrow(d, (cx + 130, y0 + 90), (cx + 10, y0 + 90), A(RED, kf), w=7, head=18)
    text(d, (cx + 160, y0 + 90), "lực cản", 44, RED, anchor="lm", alpha=kf)
    k1 = appear(t, 0.3, 0.5)
    card(d, (40, 900, 1040, 1160), fill=A(WHITE, k1), outline=A(NAVY, k1), w=5)
    text(d, (W / 2, 975), "trung bình ≈ 1,83", 52, NAVY, alpha=k1)
    text(d, (W / 2, 1075), "luôn dưới 2,0 (tính bỏ ma sát)", 44, RED, alpha=k1)
    k2 = appear(t, M[0] + 0.8, 0.5)
    card(d, (90, 1220, 990, 1380), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), w=5)
    text(d, (W / 2, 1300), "Sai số hệ thống", 56, ORANGE, alpha=k2)

# ---------------- canh 6: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        card(d, (40, 265, 1040, 1600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 364), fill=A(RED, a1), r=32)
        text(d, (W / 2, 332), "BẪY", 38, WHITE, alpha=a1)
        # qua nang dang roi nhanh dan: P dai hon T
        mx, my = 300, 760
        card(d, (mx - 60, my - 70, mx + 60, my + 70), fill=A(ORANGE, a1), outline=A((160, 60, 10), a1), r=14, w=3)
        d.line([(mx, 400), (mx, my - 70)], fill=A(INK, a1), width=3)
        arrow(d, (mx, my - 70), (mx, my - 310), A(TEAL, a1), w=9)              # T : m2 g = 0,8 N : 1,0 N = 240 : 300
        rich(d, mx + 50, my - 280, "T", 48, TEAL, alpha=a1)
        arrow(d, (mx, my + 70), (mx, my + 370), A(BLUE, a1), w=9)
        rich(d, mx + 90, my + 340, "m_{2}g", 48, BLUE, alpha=a1)
        arrow(d, (560, 700), (560, 860), A(PURPLE, a1), w=7)
        text(d, (600, 780), "a hướng xuống", 42, PURPLE, anchor="lm", alpha=a1)
        ks = clamp((t - 1.0) / 0.4)
        f = F(60); lw = tw(d, "“T = mg”", f) + tw(d, "2", F(36)); yy = 1250
        rich(d, W / 2, yy, "“T = m_{2}g”", 60, INK, alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * a1), width=6)
        kk = a1 * appear(t, 1.5, 0.5)
        card(d, (190, 1350, 890, 1500), fill=A((236, 253, 243), kk), r=24)
        rich(d, W / 2, 1425, "T < m_{2}g", 60, GREEN, alpha=kk)
    if k2 > 0:
        y0 = 700 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 620), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 80), "Thí nghiệm chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.2, 0.4)
        card(d, (70, y0 + 170, 1010, y0 + 480), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        ctext(d, y0 + 270, "Cản ở bánh xe", 48, RED, alpha=kk)
        ctext(d, y0 + 370, "hay ở ròng rọc?", 48, RED, alpha=kk)

def _goi_y(d, t, sc):                       # goi y tre 2,5 s sau cau hoi
    kh = appear(t, sc["M"][0] + 2.5, 0.5)
    if kh <= 0: return
    card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1360, "Gợi ý", 40, INK, alpha=kh)
    ctext(d, 1450, "Xem lại mẫu số · g = 10 m/s²", 42, ORANGE, maxw=820, alpha=kh)

# ---------------- canh 7: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Lệch một phía: sai số hệ thống",
             "Quả nặng 0,40 kg, bỏ ma sát: a = ?",
             body=lambda d, t, k1: _goi_y(d, t, sc))

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, hs, b, e = (sc[k] for k in ("hook", "do", "dapan", "rutra", "heso", "bay", "end"))
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.3, "ding"),
            (do["t0"] + run_start(do), "tap"), (do["t0"] + run_start(do) + T_RUN * SLOW, "tap"),
            (da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 0.3, "tap"),
            (hs["t0"] + hs["M"][0] + 0.8, "tap"),
            (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-giaibt-dlh-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Giải bài toán động lực học · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe lăn và quả nặng", draw=s_hook, tail=0.8, caps=[
   ("Hệ hai vật nối dây.", 2.5),
   ("Dừng video, chọn câu trả lời.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Thả từ nghỉ, nhìn đồng hồ.", 4.2)]),
 dict(key="dapan", title="Kết quả 5 lần đo", draw=s_dapan, tail=0.6, caps=[
   ("Lệch cùng một phía, không lung tung.", 4.8)]),
 dict(key="rutra", title="Vì sao tính ra 2,0?", draw=s_rutra, tail=0.6, caps=[
   ("Định luật II cho từng vật.", 3.8),
   ("Cộng lại, T triệt tiêu.", 3.8)]),
 dict(key="heso", title="Vì sao đo nhỏ hơn?", draw=s_heso, tail=0.6, caps=[
   ("Ma sát ở trục và ròng rọc.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Bẫy thường gặp.", 3.0),
   ("Giới hạn thí nghiệm.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 6.2)]),
])
