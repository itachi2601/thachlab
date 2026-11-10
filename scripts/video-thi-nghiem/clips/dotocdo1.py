# Clip: tn-l10-do-toc-do-01 - Bi qua hai cong quang E, F (MODE A<->B): toc do trung binh + sai so (10/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-toc-do-01.json:
#   tham_so: s = 0,500 m, a = 0,60 m/s2, x_E = 0,100 m (nam cham -> E); dong ho chia 0,001 s; thuoc mm: ds = 0,0005 m.
#   so_lieu_mau: t = 0,835 / 0,838 / 0,837 s, |t - tb| = 0,002 / 0,001 / 0,000.
#   rut_ra: tb = 0,837 s; dt = 0,001 + 0,001 = 0,002 s; delta t ~ 0,24 %; delta s = 0,10 %; v_tb = 0,597 +- 0,002 m/s (0,34 %).
# Khac dotocdo3 (tam chan rong/hep, can canh cong): o day nhin TOAN mang nghieng, hai cong, ba lan tha.
# Du doan hoi DO TAN cua ba so chi (khong hoi "s/t la toc do o dau": do la dap an Cau 2 ngay sau hop trong bai).
# Cau chot: s = 0,250 m (trong mien tham_so 0,2-0,7), thuoc mm -> delta s = 0,20 % (chua tung hien).
# Canh: Du doan -> Tien hanh (3 lan tha, thoi gian that) -> Dap an (truc so 0,834-0,839) -> Rut ra (tb, dt, v, % ,
#       chua noi duoc) -> Bay (MODE A) -> Chot + cau hoi.
from engine import *

S_EF, ACC, X_E = 0.500, 0.60, 0.100
READ = (0.835, 0.838, 0.837)                         # so_lieu_mau
TBAR = 0.837
T_MODEL = (math.sqrt(2 * ACC * (X_E + S_EF)) - math.sqrt(2 * ACC * X_E)) / ACC     # 0,8369 s
TAU_E = math.sqrt(2 * X_E / ACC)                                                   # 0,577 s tu luc tha toi E
BALL = (71, 85, 105); BALL_HI = (203, 213, 225); RAIL = (196, 200, 212); RAIL_D = (150, 155, 170)
POST = (71, 85, 105); MAG = (124, 58, 237)

def vn(x, nd=3): return f"{x:.{nd}f}".replace(".", ",")

# ---------- chu co gach tren (t trung binh) va chi so duoi ----------
def seq(d, x, y, parts, size, color=INK, alpha=1.0, anchor="m"):
    """parts: chuoi thuong, ('bar','t') = t gach tren, ('sub','v','tb') = v chi so duoi. Ve mot dong, can giua neu anchor m."""
    f = F(size); fs = F(max(36, int(size * 0.62)))
    def wid(p):
        if isinstance(p, str): return tw(d, p, f)
        if p[0] == "bar": return tw(d, p[1], f)
        return tw(d, p[1], f) + tw(d, p[2], fs) + 2
    tot = sum(wid(p) for p in parts)
    xx = x - tot / 2 if anchor == "m" else x
    for p in parts:
        if isinstance(p, str):
            dtext(d, (xx, y), p, f, color, alpha, "lm")
        elif p[0] == "bar":
            dtext(d, (xx, y), p[1], f, color, alpha, "lm")
            w = tw(d, p[1], f)
            d.line([(xx + 1, y - size * 0.62), (xx + w + 1, y - size * 0.62)], fill=A(color, alpha), width=max(3, size // 14))
        else:
            dtext(d, (xx, y), p[1], f, color, alpha, "lm")
            dtext(d, (xx + tw(d, p[1], f) + 2, y + size * 0.28), p[2], fs, color, alpha, "lm")
        xx += wid(p)
    return tot

# ---------- mang nghieng, nam cham, hai cong ----------
R0 = (205, 395); ANG = math.radians(12); KPX = 1130.0          # px / m doc mang
RU = (math.cos(ANG), math.sin(ANG)); RN = (RU[1], -RU[0])     # RN: phap tuyen huong len
RB = 22                                                         # ban kinh bi (phong to cho de nhin)
def RP(s, h=0.0): return (R0[0] + RU[0] * s * KPX + RN[0] * h, R0[1] + RU[1] * s * KPX + RN[1] * h)

def rig(d, ball_s=None, ball_a=1.0, mag_on=True, beam_cut=(False, False), alpha=1.0):
    c = lambda col: A(col, alpha)
    d.polygon([RP(-0.075, 0), RP(0.735, 0), RP(0.735, -26), RP(-0.075, -26)], fill=c(RAIL), outline=c(RAIL_D))
    for k in range(0, 15):                                        # vach thuoc moi 5 cm
        s = k * 0.05; L = 14 if k % 2 == 0 else 8
        d.line([RP(s, -26), RP(s, -26 + L)], fill=c(RAIL_D), width=2)
    # nam cham dien (dau tren mang)
    m = [RP(-0.07, 2), RP(-0.022, 2), RP(-0.022, 56), RP(-0.07, 56)]
    d.polygon(m, fill=c(MAG if mag_on else (196, 181, 253)), outline=c(NAVY))
    text(d, (62, 490), "nam châm", 40, MAG, anchor="lm", alpha=alpha)
    text(d, (62, 538), "điện", 40, MAG, anchor="lm", alpha=alpha)
    q = RP(-0.046, -30); d.line([(q[0], q[1]), (q[0] - 20, 462)], fill=c(MAG), width=3)
    # hai cong quang: cot dung + cham tia (tia vuong goc man hinh, ngang tam bi)
    for s, nm, cut in ((X_E, "E", beam_cut[0]), (X_E + S_EF, "F", beam_cut[1])):
        b = RP(s, RB)
        d.rectangle([b[0] - 10, 300, b[0] + 10, b[1] - 18], fill=c(POST))
        d.rectangle([b[0] - 22, b[1] - 26, b[0] + 22, b[1] - 12], fill=c(POST))
        text(d, (b[0] + 44, 318), nm, 48, INK, alpha=alpha)
    # bi
    if ball_s is not None and ball_a > 0.02:
        p = RP(ball_s, RB)
        d.ellipse([p[0] - RB, p[1] - RB, p[0] + RB, p[1] + RB], fill=A(BALL, ball_a * alpha), outline=A(NAVY, ball_a * alpha), width=2)
        d.ellipse([p[0] - 11, p[1] - 13, p[0] - 3, p[1] - 5], fill=A(BALL_HI, ball_a * alpha))
    for s, cut in ((X_E, beam_cut[0]), (X_E + S_EF, beam_cut[1])):   # cham tia ve SAU bi -> bi che thi tia bi che
        b = RP(s, RB)
        if not cut: dot(d, b[0], b[1], 7, c(RED))
    # kich thuoc s
    a0, a1 = RP(X_E, -70), RP(X_E + S_EF, -70)
    for q in (a0, a1): pass
    arrow(d, ((a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2), a1, c(BLUE), w=4, head=16)
    arrow(d, ((a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2), a0, c(BLUE), w=4, head=16)
    for s in (X_E, X_E + S_EF): d.line([RP(s, -30), RP(s, -84)], fill=c(BLUE), width=3)
    mid = RP(X_E + S_EF / 2, -125)
    text(d, (mid[0] + 10, mid[1] + 8), "s = 0,500 m", 44, BLUE, alpha=alpha)

def clock(d, y, val, mode="MODE A ↔ B", hot=False, alpha=1.0, flash=0.0):
    card(d, (40, y, 1040, y + 160), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    card(d, (80, y + 22, 540, y + 138), fill=A(NAVY, alpha), r=18)
    if flash > 0: card(d, (80, y + 22, 540, y + 138), fill=A((250, 204, 21), 0.35 * flash), r=18)
    text(d, (310, y + 80), vn(val) + " s", 62, YELLOW if (hot or val > 0) else GRAY, alpha=alpha)
    text(d, (790, y + 58), "đồng hồ 0,001 s", 40, INK, bold=False, alpha=alpha)
    text(d, (790, y + 112), mode, 44, NAVY, alpha=alpha)

def s_at(tau, tk):
    """Vi tri bi (m tu nam cham) sau tau giay ke tu luc tha; doan E->F keo dan de toi F dung luc so chi tk."""
    if tau <= TAU_E: return ACC * tau * tau / 2
    tm = TAU_E + (tau - TAU_E) * T_MODEL / tk
    return ACC * tm * tm / 2

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    rig(d, ball_s=0.0)
    clock(d, 785, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 975 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 180, "Thả bi 3 lần bằng nam châm điện.", 46, INK, bold=False, maxw=900, alpha=a)
    ctext(d, y0 + 300, "Ba số chỉ của đồng hồ", 54, INK, maxw=900, alpha=a)
    ctext(d, y0 + 375, "lệch nhau cỡ nào?", 54, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 490, 940, y0 + 504], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 490, 140 + 800 * (1 - p), y0 + 504], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (3 lan tha, thoi gian that) ----------------
RUN0, RST, HOLD = 0.6, 0.55, 0.85
def schedule():
    out = []; s = RUN0
    for tk in READ:
        L = RST + TAU_E + tk + 0.35 + HOLD
        out.append((s, L)); s += L
    return out
SCHED = schedule()

def run_state(t):
    """-> (lan j, tau tu luc tha (<0: dang RESET), vi tri bi, so dong ho, so hang da xong, do loe RESET)."""
    if t < SCHED[0][0]: return 0, -1, 0.0, 0.0, 0, 0.0
    j = 0
    for i, (s, L) in enumerate(SCHED):
        if t >= s: j = i
    s, L = SCHED[j]; tk = READ[j]
    tau = t - s - RST
    flash = clamp(1 - (t - s) / 0.5) if t - s < 0.5 else 0.0
    if tau < 0:                                   # dang RESET: dong ho ve 0, bi o nam cham
        return j, tau, 0.0, 0.0, j, flash
    te = tau - TAU_E
    clk = 0.0 if te < 0 else (tk if te >= tk else math.floor(te * 1000) / 1000)
    done = j + (1 if te >= tk else 0)
    return j, tau, s_at(tau, tk), clk, done, flash

def s_do(img, d, t, sc):
    j, tau, bs, clk, done, flash = run_state(t)
    card(d, (40, 265, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    on = tau < 0
    ba = 1.0 if bs < 0.70 else clamp(1 - (bs - 0.70) / 0.04)
    if t < SCHED[0][0] + RST: ba = 1.0
    cutE = abs(bs - X_E) * KPX < RB; cutF = abs(bs - X_E - S_EF) * KPX < RB
    rig(d, ball_s=bs, ball_a=ba, mag_on=on or t < SCHED[0][0], beam_cut=(cutE, cutF))
    if flash > 0:
        text(d, (800, 700), "RESET", 44, ORANGE, alpha=flash)
    run = 0 <= tau - TAU_E < READ[j]
    clock(d, 785, clk, hot=run, flash=0.0)
    # bang 3 lan
    y = 975
    card(d, (40, y, 1040, y + 520), fill=WHITE, outline=LIGHT, w=3)
    XS = (300, 700)
    text(d, (XS[0], y + 60), "Lần", 46, INK); text(d, (XS[1], y + 60), "t (s)", 46, INK)
    d.line([(90, y + 110), (990, y + 110)], fill=LIGHT, width=3)
    for i, tk in enumerate(READ):
        yy = y + 185 + i * 110
        if i == j and done <= i and t >= SCHED[0][0]:
            d.rounded_rectangle([80, yy - 46, 1000, yy + 46], radius=18, fill=(255, 247, 237))
        text(d, (XS[0], yy), str(i + 1), 52, INK)
        if i < done: text(d, (XS[1], yy), vn(tk), 54, NAVY)

# ---------------- canh 3: Dap an (truc so 0,834 - 0,839 s) ----------------
NX0, NPX, NY = 165, 150, 760          # x cua 0,834 ; px / 0,001 s ; y truc
def nx(v): return NX0 + (v - 0.834) / 0.001 * NPX

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · lệch vài phần nghìn giây"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 318), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 284), lb, 40, WHITE, alpha=ka)
    card(d, (40, 350, 1040, 1040), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 420), "t (s)", 42, INK, anchor="lm")
    d.line([(NX0 - 50, NY), (nx(0.839) + 50, NY)], fill=INK, width=4)
    for k in range(6):
        v = 0.834 + k * 0.001; x = nx(v)
        d.line([(x, NY - 18), (x, NY + 18)], fill=INK, width=4)
        text(d, (x, NY + 62), vn(v), 38, INK, bold=False)
    for i, tk in enumerate(READ):                    # moi lan mot cham, cung mau
        k = appear(t, 0.5 + 0.35 * i, 0.4)
        if k <= 0: continue
        x = nx(tk); yy = NY - 110 - (60 if i == 2 else 0)
        d.line([(x, NY - 14), (x, yy + 26)], fill=A(BLUE, k), width=4)
        dot(d, x, yy, 24, A(BLUE, k))
        text(d, (x, yy), str(i + 1), 36, WHITE, alpha=k)
    kb = appear(t, 1.8, 0.5)                          # chieu rong vung tan: 0,835 -> 0,838
    if kb > 0:
        x0, x1 = nx(0.835), nx(0.838); yb = NY + 140
        d.line([(x0, yb), (x1, yb)], fill=A(ORANGE, kb), width=5)
        for xx in (x0, x1): d.line([(xx, yb - 16), (xx, yb + 16)], fill=A(ORANGE, kb), width=5)
        text(d, ((x0 + x1) / 2, yb + 52), "0,003 s", 40, ORANGE, alpha=kb)
    k2 = appear(t, M[0] + 1.4, 0.5)
    card(d, (40, 1080, 1040, 1420), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
    ctext(d, 1180, "Thả cùng một chỗ,", 50, GREEN, maxw=900, alpha=k2)
    ctext(d, 1300, "máy tự bấm giờ", 50, GREEN, maxw=900, alpha=k2)

# ---------------- canh 4: Rut ra (trung binh, sai so, ket qua) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1010), fill=WHITE, outline=LIGHT, w=3)
    k1 = appear(t, 0.3, 0.45)
    seq(d, 90, 340, [("bar", "t"), " ≈ 0,837 s"], 50, INK, alpha=k1, anchor="l")
    text(d, (990, 340), "trung bình 3 lần", 38, INK, bold=False, anchor="rm", alpha=k1)
    k2 = appear(t, 1.3, 0.45)
    seq(d, 90, 450, ["Δt = 0,001 + 0,001 = 0,002 s"], 50, INK, alpha=k2, anchor="l")
    text(d, (265, 512), "lệch TB", 38, MUTED, bold=False, alpha=k2)
    text(d, (450, 512), "đồng hồ", 38, MUTED, bold=False, alpha=k2)
    k3 = appear(t, M[1] - 0.1, 0.45)
    seq(d, 90, 620, [("sub", "v", "tb"), " = 0,500 : 0,837 ≈ 0,597 m/s"], 50, INK, alpha=k3, anchor="l")
    k4 = appear(t, M[1] + 1.0, 0.45)
    seq(d, 90, 730, ["δv = 0,10 % + 0,24 % = 0,34 %"], 50, INK, alpha=k4, anchor="l")
    text(d, (250, 792), "δs: thước mm", 38, MUTED, bold=False, alpha=k4)
    text(d, (520, 792), "δt", 38, MUTED, bold=False, alpha=k4)
    k5 = appear(t, M[1] + 2.0, 0.5)
    card(d, (90, 845, 990, 975), fill=A((236, 253, 243), k5), outline=A(GREEN, k5), r=24, w=4)
    seq(d, W / 2, 910, [("sub", "v", "tb"), " = 0,597 ± 0,002 m/s"], 54, GREEN, alpha=k5)
    k6 = appear(t, M[2] - 0.1, 0.45)
    if k6 > 0:
        y0 = 1040 + (1 - k6) * 30
        card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, k6), outline=A(NAVY, k6), w=6)
        text(d, (W / 2, y0 + 65), "Chưa nói được", 46, NAVY, alpha=k6)
        kk = k6 * appear(t, M[2] + 0.4, 0.4)
        card(d, (80, y0 + 125, 1000, y0 + 420), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, y0 + 210), "Trên EF bi lăn đều", 48, RED, alpha=kk)
        text(d, (W / 2, y0 + 320), "hay nhanh dần?", 48, RED, alpha=kk)

# ---------------- canh 5: Bay (MODE A) ----------------
def s_bay(img, d, t, sc):
    a1 = appear(t, 0.2, 0.45); y0 = 265
    card(d, (40, y0, 1040, y0 + 1300), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    q = "“Để MODE A cũng được”"
    ks = clamp((t - 0.9) / 0.4); f = F(50); lw = tw(d, q, f); yy = y0 + 210
    text(d, (W / 2, yy), q, 50, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0:
        d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        text(d, (W / 2 + lw / 2 + 40, yy), "✗", 54, RED, alpha=ks * a1)
    # hinh: cong E, bi dang che tia, ngoac "chi dem doan nay" (hien cung luc chu ket luan)
    kk = a1 * appear(t, 1.4, 0.5)
    gx, gy = 540, y0 + 560; R = 70
    d.rectangle([gx - 14, y0 + 330, gx + 14, gy - 40], fill=A(POST, kk))
    d.rectangle([gx - 32, gy - 50, gx + 32, gy - 26], fill=A(POST, kk))
    d.rectangle([140, gy + R, 940, gy + R + 26], fill=A(RAIL, kk), outline=A(RAIL_D, kk))
    bx = gx + 20
    d.ellipse([bx - R, gy - R, bx + R, gy + R], fill=A(BALL, kk), outline=A(NAVY, kk), width=3)
    d.ellipse([gx - 12, gy - 12, gx + 12, gy + 12], outline=A((254, 202, 202), kk), width=4)
    text(d, (gx - 120, gy - 120), "E", 52, INK, alpha=kk)
    yb = gy + R + 70
    d.line([(bx - R, yb), (bx + R, yb)], fill=A(ORANGE, kk), width=5)
    for xx in (bx - R, bx + R): d.line([(xx, yb - 16), (xx, yb + 16)], fill=A(ORANGE, kk), width=5)
    card(d, (90, y0 + 800, 990, y0 + 1240), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, y0 + 890), "MODE A: chỉ đếm", 54, GREEN, alpha=kk)
    text(d, (W / 2, y0 + 990), "lúc bi che tia E", 54, GREEN, alpha=kk)
    text(d, (W / 2, y0 + 1130), "Đo E → F: MODE A ↔ B", 46, NAVY, alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):
        kb = appear(t, M[0] + 0.6, 0.5)                   # phac hoa hai cong cach 0,250 m (khong co dap so)
        if kb > 0:
            for x in (330, 750):
                d.rectangle([x - 9, 960, x + 9, 1060], fill=A(POST, kb)); dot(d, x, 1068, 8, A(RED, kb))
            d.rectangle([200, 1100, 880, 1118], fill=A(RAIL, kb))
            arrow(d, (540, 1170), (330, 1170), A(BLUE, kb), w=4, head=16); arrow(d, (540, 1170), (750, 1170), A(BLUE, kb), w=4, head=16)
            text(d, (540, 1225), "0,250 m", 44, BLUE, alpha=kb)
            text(d, (300, 945), "E", 44, INK, alpha=kb); text(d, (780, 945), "F", 44, INK, alpha=kb)
        kh = appear(t, M[0] + 2.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Thước mm: Δs = 0,0005 m", 44, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Tốc độ trung bình = s chia t trung bình, kèm ± Δv",
             "Đặt s = 0,250 m, vẫn thước mm: δs bằng bao nhiêu?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.3, "ding")]
    for s, L in SCHED: cs.append((do["t0"] + s + RST + TAU_E, "tap"))          # bi cham tia E: dong ho chay
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 2.0, "tap"),
           (b["t0"] + 0.9, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-do-toc-do-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Đo tốc độ của vật · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai cổng quang E, F", draw=s_hook, tail=0.8, caps=[
   ("Bi lăn từ E tới F.", 2.6),
   ("Dừng video, chọn câu trả lời.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Bi chắn tia E: đồng hồ chạy.", 4.4),
   ("Chắn tia F thì dừng. Lặp 3 lần.", 4.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.9, caps=[
   ("Ba số trên cùng một trục.", 4.2)]),
 dict(key="rutra", title="Ghi kết quả", draw=s_rutra, tail=0.5, caps=[
   ("Lấy trung bình, cộng sai số đồng hồ.", 3.4),
   ("Chia thì cộng phần trăm.", 3.6),
   ("Còn một điều chưa biết.", 3.4)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("Nhìn núm MODE.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 5.4)]),
])
