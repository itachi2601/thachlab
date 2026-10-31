# Clip: tn-l10-do-toc-do-03 - Tam chan rong hay hep: d/t voi xe dang nhanh dan (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-toc-do-03.json:
#   tham_so: v1 = 0,600 m/s (luc mep truoc vao cong), a = 0,50 m/s2, buoc dong ho 0,001 s.
#   so_lieu_mau: d = 10,0 / 5,0 / 2,0 / 1,0 cm -> t that 0,1565 / 0,0806 / 0,0329 / 0,0166 s,
#                t hien 0,156 / 0,081 / 0,033 / 0,017 s, d/t = 0,641 / 0,617 / 0,606 / 0,588 m/s.
#   rut_ra: sai so lam tron khoang 3 % o d = 1,0 cm.
#   Cau chot dung tham_so trong mien cho phep (v1 = 0,90 m/s, d = 1,0 cm) -> dong ho hien 0,011 s, chua tung hien.
# Truc chinh: d/t PHU THUOC be rong tam chan (khac ctbdd1: do thi v-t). Canh tien hanh = can canh cong quang
# (diem tia sang bi tam chan che, dong ho chay dung pha vi tri tam chan) + bang 4 hang; dap an = do lech so voi 0,600.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (4 tam chan, chieu cham 10 lan) -> Dap an + bieu do lech
#       -> Rut ra (tam rong: xe kip nhanh them; tam hep: lam tron; chua noi duoc) -> Bay -> Chot + cau hoi.
from engine import *

V1, ACC = 0.600, 0.50                                   # m/s, m/s^2 (tham_so mac dinh)
ROWS = [(10.0, 0.1565, 0.156, 0.641), (5.0, 0.0806, 0.081, 0.617),
        (2.0, 0.0329, 0.033, 0.606), (1.0, 0.0166, 0.017, 0.588)]          # so_lieu_mau
FLAG = (234, 88, 12); FLAG_D = (180, 60, 8); CART = (59, 130, 246); RAIL = (196, 200, 212); RAIL_D = (150, 155, 170)
POST = (71, 85, 105)

def vn(x, nd=None):
    s = (f"{x:.{nd}f}" if nd is not None else f"{x:g}").replace(".", ",")
    return s.replace("-", "−")

def t_that(dcm):
    """Thoi gian che cong theo mo_hinh (d = v1 t + a t^2/2); khop cot 't that' cua so_lieu_mau."""
    dm = dcm / 100
    return (-V1 + math.sqrt(V1 * V1 + 2 * ACC * dm)) / ACC

# ---------------- hinh dung chung ----------------
def plates_row(d, y, scale=26, labels=None, alpha=1.0, hl=None, gap=110):
    """Bon tam chan dung ti le (scale px/cm). labels: chu duoi moi tam. hl: {chi so: mau} to vien."""
    xs = []; x = 90
    for j, (dcm, *_r) in enumerate(ROWS):
        w = dcm * scale
        col = hl.get(j) if hl else None
        d.rectangle([x, y, x + w, y + 110], fill=A(FLAG, alpha), outline=A(FLAG_D, alpha), width=3)
        if col: d.rounded_rectangle([x - 14, y - 14, x + w + 14, y + 124], radius=12, outline=A(col, alpha), width=6)
        xs.append(x + w / 2); x += w + gap
    if labels:
        for cx, s in zip(xs, labels):
            text(d, (cx, y + 160), s[0], 42, s[1], alpha=alpha)
    return xs

# ---------------- canh 1: Du doan ----------------
R0, R1 = (110, 530), (1000, 608)                        # ~5 do (a = 0,50 m/s2 ung voi ~3 do)                        # mang nghieng (tren-trai -> duoi-phai)
RL = math.hypot(R1[0] - R0[0], R1[1] - R0[1])
RU = ((R1[0] - R0[0]) / RL, (R1[1] - R0[1]) / RL); RN = (RU[1], -RU[0])        # RN: phap tuyen huong len
def RP(s, h): return (R0[0] + RU[0] * s + RN[0] * h, R0[1] + RU[1] * s + RN[1] * h)
S_GATE = 640

def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 700), fill=WHITE, outline=LIGHT, w=3)
    d.polygon([RP(0, 0), RP(RL, 0), RP(RL, -26), RP(0, -26)], fill=RAIL, outline=RAIL_D)
    s0 = 330                                                                  # xe: mep truoc o s0
    d.polygon([RP(s0 - 190, 14), RP(s0, 14), RP(s0, 74), RP(s0 - 190, 74)], fill=CART, outline=NAVY)
    for sw in (s0 - 150, s0 - 40):
        c = RP(sw, 12); d.ellipse([c[0] - 13, c[1] - 13, c[0] + 13, c[1] + 13], fill=NAVY)
    d.polygon([RP(s0 - 120, 74), RP(s0 - 70, 74), RP(s0 - 70, 125), RP(s0 - 120, 125)], fill=FLAG, outline=FLAG_D)
    bp = RP(S_GATE, 100)                                                       # tia sang (vuong goc man hinh)
    d.rectangle([bp[0] - 11, 285, bp[0] + 11, bp[1] - 20], fill=POST)
    d.rectangle([bp[0] - 24, bp[1] - 30, bp[0] + 24, bp[1] + 14], fill=POST)
    dot(d, bp[0], bp[1] - 8, 8, RED)
    text(d, (bp[0] + 40, 320), "cổng quang", 40, INK, anchor="lm")
    ft = RP(s0 - 95, 125)                                                     # nhan "tam chan" chi vao co
    d.line([(ft[0], ft[1] - 6), (ft[0], 355)], fill=FLAG_D, width=4)
    text(d, (ft[0], 330), "tấm chắn", 40, FLAG_D)
    a0, a1 = RP(s0 + 20, 45), RP(s0 + 170, 45)
    arrow(d, a0, a1, ORANGE, w=7, head=20)
    lp = RP(s0 + 95, 100); text(d, lp, "nhanh dần", 40, ORANGE, anchor="mm")
    text(d, (80, 605), "vào cổng:", 40, INK, bold=False, anchor="lm")
    text(d, (80, 658), "0,600 m/s", 46, BLUE, anchor="lm")
    # bon tam chan
    card(d, (40, 720, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    text(d, (1000, 765), "đồng hồ 0,001 s", 40, NAVY, anchor="rm")
    plates_row(d, 800, scale=24, labels=[("10,0", INK), ("5,0", INK), ("2,0", INK), ("1,0 cm", INK)])
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 200, "Tấm chắn nào cho d/t", 52, INK, maxw=880, alpha=a)
    ctext(d, y0 + 285, "sát 0,600 m/s nhất?", 52, INK, maxw=880, alpha=a)
    ctext(d, y0 + 385, "d: bề rộng · t: số đồng hồ", 40, INK, bold=False, maxw=900, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 484], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 484], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (can canh cong quang, chieu cham 10 lan) ----------------
SLOW = 10.0
PXC = 40                       # px / cm trong can canh
XB = 540                       # vi tri tia sang (x)
YB = 560                       # do cao tia sang
APP, EXIT, HOLD = 0.6, 0.5, 0.35
RUN0 = 0.5                     # luot 1 bat dau (giay trong canh)

def schedule():
    out = []; s = RUN0
    for dcm, tt, th, v in ROWS:
        L = APP + t_that(dcm) * SLOW + EXIT + HOLD
        out.append((s, L)); s += L
    return out
SCHED = schedule()

def run_state(t):
    """-> (luot j, tau that (s), do lech mep truoc so voi tia (cm), so dong ho (s), so hang da xong)."""
    j = 0
    for i, (s, L) in enumerate(SCHED):
        if t >= s: j = i
    s, L = SCHED[j]
    dcm, _tk, th, v = ROWS[j]; tt = t_that(dcm)          # t that dung mo hinh (kho lam tron 4 chu so)
    tau = (min(t, s + L) - s - APP) / SLOW
    if t < s: tau = -APP / SLOW
    tau_c = min(tau, tt + EXIT / SLOW)
    x = (V1 * tau_c + ACC * tau_c * tau_c / 2) * 100             # cm, mep truoc so voi tia
    clock = 0.0 if tau < 0 else (th if tau >= tt else round(tau * 1000) / 1000)
    done = j + (1 if tau >= tt else 0)
    return j, tau, x, clock, done

def closeup(d, j, x):
    """Ve len anh phu (1000 x 470), toa do anh phu = toa do khung tru (40, 290)."""
    sub = Image.new("RGB", (1000, 470), WHITE); sd = ImageDraw.Draw(sub, "RGBA")
    old = IMG_REF[0]; IMG_REF[0] = sub
    ox, oy = 40, 290
    X = lambda xx: xx - ox; Y = lambda yy: yy - oy
    dcm = ROWS[j][0]
    xL = XB + x * PXC; xT = xL - dcm * PXC; cx = (xL + xT) / 2
    sd.rectangle([X(XB - 11), Y(390), X(XB + 11), Y(YB - 26)], fill=POST)           # cang sau cua cong
    sd.rectangle([X(XB - 26), Y(YB - 34), X(XB + 26), Y(YB + 34)], fill=POST)
    dot(sd, X(XB), Y(YB), 10, RED)
    sd.rectangle([X(xT), Y(470), X(xL), Y(630)], fill=FLAG, outline=FLAG_D, width=3)  # tam chan (che tia)
    if xT <= XB <= xL:                                                       # tia bi che: chi con vien rong
        sd.ellipse([X(XB - 12), Y(YB - 12), X(XB + 12), Y(YB + 12)], outline=(254, 202, 202), width=4)
    sd.rounded_rectangle([X(cx - 280), Y(630), X(cx + 280), Y(692)], radius=12, fill=CART, outline=NAVY, width=4)
    arrow(sd, (X(cx - 250), Y(661)), (X(cx - 130), Y(661)), WHITE, w=6, head=16)
    dtext(sd, (X(cx - 110), Y(661)), "nhanh dần", F(36), WHITE, 1.0, "lm")
    for wx in (cx - 200, cx + 200): sd.ellipse([X(wx - 22), Y(692), X(wx + 22), Y(736)], fill=NAVY)
    sd.rectangle([0, Y(736), 1000, Y(760)], fill=RAIL_D)
    IMG_REF[0] = old
    return sub

def s_do(img, d, t, sc):
    j, tau, x, clock, done = run_state(t)
    card(d, (40, 265, 1040, 790), fill=WHITE, outline=LIGHT, w=3)
    sub = closeup(d, j, x)
    m = Image.new("L", sub.size, 0); ImageDraw.Draw(m).rounded_rectangle([3, 0, 996, 466], radius=10, fill=255)
    img.paste(sub, (40, 290), m)
    blocked = 0 <= tau < t_that(ROWS[j][0])
    card(d, (560, 290, 1010, 390), fill=NAVY, r=18)
    text(d, (785, 340), vn(clock, 3) + " s", 56, YELLOW if blocked or clock > 0 else GRAY)
    text(d, (80, 340), "d = " + vn(ROWS[j][0], 1) + " cm", 48, FLAG_D, anchor="lm")
    text(d, (XB - 60, 430), "tia sáng", 40, RED, anchor="rm")
    d.line([(XB - 55, 445), (XB - 12, YB - 12)], fill=RED, width=3)                 # duong dan toi cham tia
    text(d, (W / 2, 830), "chiếu chậm 10 lần", 40, INK, bold=False)
    # bang
    y = 875
    card(d, (40, y, 1040, y + 560), fill=WHITE, outline=LIGHT, w=3)
    XS = (230, 540, 850)
    for xx, s in zip(XS, ("d (cm)", "t đồng hồ (s)", "d/t (m/s)")): text(d, (xx, y + 60), s, 44, INK)
    d.line([(70, y + 108), (1010, y + 108)], fill=LIGHT, width=3)
    for i, (dcm, tt, th, v) in enumerate(ROWS):
        yy = y + 175 + i * 105
        if i == j and done <= i:
            d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=18, fill=(255, 247, 237))
        if i < done:
            text(d, (XS[0], yy), vn(dcm, 1), 50, INK)
            text(d, (XS[1], yy), vn(th, 3), 50, NAVY)
            text(d, (XS[2], yy), vn(v, 3), 50, NAVY)
    text(d, (W / 2, y + 600), "d/t: đổi d ra mét", 40, INK, bold=False)
    text(d, (W / 2, y + 665), "vào cổng: 0,600 m/s", 42, BLUE)

# ---------------- canh 3: Dap an + bieu do lech so voi 0,600 ----------------
GY0, GK = 880, 8000.0            # y cua duong 0,600 ; px / (m/s): 0,001 m/s -> 8 px
GXS = (340, 530, 720, 910)
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · tấm 2,0 cm"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 318), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 284), lb, 40, WHITE, alpha=ka)
    card(d, (40, 350, 1040, 1200), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 405), "d/t (m/s)", 42, INK, anchor="lm")
    for i in range(18):                                                   # duong cham 0,600
        x0 = 270 + i * 42; d.line([(x0, GY0), (x0 + 24, GY0)], fill=BLUE, width=5)
    text(d, (250, GY0), "0,600", 44, BLUE, anchor="rm")
    for i, (dcm, tt, th, v) in enumerate(ROWS):
        k = appear(t, 0.5 + 0.35 * i, 0.4)
        if k <= 0: continue
        gx, gy = GXS[i], GY0 - (v - V1) * GK
        col = GREEN if i == 2 else (RED if i == 3 else ORANGE)
        d.line([(gx, GY0), (gx, gy)], fill=A(col, k), width=10)
        dot(d, gx, gy, 15, A(col, k))
        ly = gy - 60 if v > V1 else gy + 52
        text(d, (gx, ly), vn(v, 3), 44, col, alpha=k)
        if i == 2: d.ellipse([gx - 30, gy - 30, gx + 30, gy + 30], outline=A(GREEN, k), width=5)
    d.line([(270, 1060), (1010, 1060)], fill=LIGHT, width=3)
    for i, (dcm, *_r) in enumerate(ROWS): text(d, (GXS[i], 1115), vn(dcm, 1), 44, INK)
    text(d, (250, 1115), "d (cm)", 40, INK, anchor="rm")
    k2 = appear(t, M[0] + 0.3, 0.5)
    card(d, (40, 1240, 1040, 1590), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
    ctext(d, 1340, "Hẹp dần: sát 0,600 dần", 48, GREEN, maxw=900, alpha=k2)
    ctext(d, 1450, "1,0 cm: lại lệch xa hơn", 48, RED, maxw=900, alpha=appear(t, M[0] + 1.3, 0.5))

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    # A: tam rong -> xe kip nhanh them trong luc tam chan qua (mui ten ti le dung: 0,600 -> ra khoi cong 0,678 = 1,13 lan)
    card(d, (40, 265, 1040, 680), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 320), "Tấm 10,0 cm", 46, FLAG_D, anchor="lm")
    v_ra = V1 + ACC * ROWS[0][1]                       # 0,600 + 0,50 . 0,1565 = 0,678 m/s (mep sau ra khoi cong)
    L0 = 300                                           # px cho 0,600 m/s; ba mui ten cung ti le
    rows = [("vào", V1, BLUE, 0.0), ("d/t", ROWS[0][3], ORANGE, M[0] + 1.2), ("ra", v_ra, BLUE, 0.6)]
    for (lb, v, col, at), yy in zip(rows, (410, 500, 590)):
        k = 1.0 if at == 0 else appear(t, at, 0.5)
        if k <= 0: continue
        text(d, (80, yy), lb, 42, INK, anchor="lm", alpha=k)
        arrow(d, (180, yy), (180 + L0 * v / V1 * k, yy), A(col, k), w=8, head=22)
        text(d, (180 + L0 * v / V1 + 22, yy), vn(v, 3) + " m/s", 42, col, anchor="lm", alpha=k)
    kb = appear(t, M[0] + 1.2, 0.5)
    text(d, (880, 500), "trung bình", 42, INK, alpha=kb)
    # B: tam hep -> lam tron cua dong ho
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (40, 705, 1040, 1150), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
        text(d, (80, 760), "Tấm 1,0 cm", 46, FLAG_D, anchor="lm", alpha=k1)
        ry, x0, px = 920, 100, 180                        # thuoc thoi gian: vach dong ho moi 0,001 s
        d.line([(x0 - 20, ry), (x0 + 3 * px + 20, ry)], fill=A(INK, k1), width=4)
        for i, lb in enumerate(("0,015", "0,016", "0,017", "0,018")):
            xx = x0 + i * px; d.line([(xx, ry - 22), (xx, ry + 22)], fill=A(INK, k1), width=4)
            text(d, (xx, ry + 58), lb, 38, GREEN if i == 2 else INK, alpha=k1)
        text(d, (x0 - 20, ry + 120), "vạch đồng hồ (s)", 38, INK, bold=False, anchor="lm", alpha=k1)
        xt, xh = x0 + 1.6 * px, x0 + 2 * px              # 0,0166 (that) ; 0,017 (dong ho)
        kt = appear(t, M[1] + 0.4, 0.4)
        dot(d, xt, ry, 14, A(ORANGE, kt))
        text(d, (xt - 20, ry - 75), "thật 0,0166 s", 42, ORANGE, alpha=kt)
        kh = appear(t, M[1] + 1.2, 0.4)
        if kh > 0:
            arrow(d, (xt + 16, ry - 32), (xt + 16 + (xh - xt - 16) * kh, ry - 32), A(GREEN, kh), w=6, head=14)
            dot(d, xh, ry, 12, A(GREEN, kh))
        kc = appear(t, M[1] + 0.8, 0.5)
        text(d, (875, 790), "t thật:", 38, INK, bold=False, alpha=kc)
        text(d, (875, 840), "d/t = 0,602", 44, ORANGE, alpha=kc)
        kd = appear(t, M[1] + 1.9, 0.5)
        text(d, (875, 925), "t đồng hồ:", 38, INK, bold=False, alpha=kd)
        text(d, (875, 975), "d/t = 0,588", 44, RED, alpha=kd)
        text(d, (840, 1080), "làm tròn khoảng 3 %", 38, RED, alpha=kd)
    # C: chua noi duoc
    k2 = appear(t, M[2] - 0.1, 0.45)
    if k2 > 0:
        y0 = 1175 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 60), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[2] + 0.3, 0.4)
        card(d, (80, y0 + 115, 1000, y0 + 385), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, y0 + 190), "d nào tốt nhất?", 48, RED, alpha=kk)
        text(d, (W / 2, y0 + 300), "mới thử 4 tấm", 44, RED, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    card(d, (40, 265, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    plates_row(d, 300, scale=22, gap=130, labels=[("0,641", ORANGE), ("0,617", ORANGE), ("0,606", GREEN), ("0,588", RED)],
               hl={2: GREEN, 3: RED})
    text(d, (975, 355), "d/t", 44, INK)
    text(d, (975, 415), "(m/s)", 40, INK, bold=False)
    a1 = appear(t, 0.2, 0.45); y0 = 600
    card(d, (40, y0, 1040, y0 + 960), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    q = "“Tấm càng hẹp càng tốt”"
    ks = clamp((t - 1.0) / 0.4); f = F(50); lw = tw(d, q, f); yy = y0 + 240
    text(d, (W / 2, yy), q, 50, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
    kk = a1 * appear(t, 1.5, 0.5)
    card(d, (90, y0 + 400, 990, y0 + 880), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, y0 + 500), "Hẹp vừa đủ:", 56, GREEN, alpha=kk)
    text(d, (W / 2, y0 + 640), "t dài hơn nhiều", 54, GREEN, alpha=kk)
    text(d, (W / 2, y0 + 740), "bước chia 0,001 s", 54, GREEN, alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):                       # goi y tu ve: nhan "Goi y" >= 36 px (engine dung 36 nhat)
        kh = appear(t, M[0] + 1.2, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Làm tròn tới 0,001 s", 44, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "d/t: tốc độ trung bình trên bề rộng d",
             "Vào cổng 0,90 m/s, tấm 1,0 cm: đồng hồ hiện bao nhiêu?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.3, "ding")]
    for s, L in SCHED: cs.append((do["t0"] + s + APP, "tap"))                    # mep truoc cham tia
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 1.2, "tap"),
           (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-do-toc-do-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Đo tốc độ của vật · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tấm chắn rộng hay hẹp?", draw=s_hook, tail=0.8, caps=[
   ("Bốn tấm chắn, cùng một xe.", 3.0),
   ("Dừng video, chọn câu trả lời.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đồng hồ chạy khi tia bị che.", 4.0),
   ("Lần lượt bốn tấm chắn.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So với tốc độ vào cổng.", 4.2)]),
 dict(key="rutra", title="Vì sao?", draw=s_rutra, tail=0.6, caps=[
   ("Tấm rộng: xe kịp nhanh thêm.", 3.4),
   ("Tấm hẹp: đồng hồ làm tròn.", 3.4),
   ("Còn một điều chưa biết.", 4.0)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.5, caps=[
   ("Nhìn hàng 1,0 cm.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.2, caps=[
   ("Dừng video, tự trả lời.", 5.4)]),
])
