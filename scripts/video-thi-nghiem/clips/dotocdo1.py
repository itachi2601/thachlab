# Clip: tn-l10-do-toc-do-01 - Bi qua hai cong quang E, F (MODE A<->B): toc do trung binh + sai so (10/11/2026; dung lai
#   27/11/2026 theo cong moi viec 4: --do-chu 0 LOI, chu ve >= 56 px, khong chi so duoi, Bay khong gach, THU NGHI khong goi y).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-toc-do-01.json:
#   tham_so: s = 0,500 m, a = 0,60 m/s2, x_E = 0,100 m (nam cham -> E); dong ho chia 0,001 s; thuoc mm: ds = 0,0005 m.
#   so_lieu_mau: t = 0,835 / 0,838 / 0,837 s, |t - tb| = 0,002 / 0,001 / 0,000.
#   rut_ra: tb = 0,837 s; dt = 0,001 + 0,001 = 0,002 s; delta t ~ 0,24 %; delta s = 0,10 %; v_tb = 0,597 +- 0,002 m/s (0,34 %).
# Khac dotocdo3 (tam chan rong/hep, can canh cong): o day nhin TOAN mang nghieng, hai cong, ba lan tha.
# Du doan hoi DO TAN cua ba so chi (khong hoi "s/t la toc do o dau": do la dap an Cau 2 ngay sau hop trong bai).
# Cau chot: s = 0,250 m (trong mien tham_so 0,2-0,7), thuoc mm -> delta s = 0,20 % (chua tung hien).
# Canh: Du doan -> Tien hanh (3 lan tha, thoi gian that, DAP AN) -> Rut ra (t tb, v tb, ds, delta s) -> Chua noi duoc
#       -> Bay (lay s tu cho tha = 0,600 m; khong dung MODE vi Cau 1 cua bai da hoi) -> THU NGHI (s = 0,250 m, delta s?).
from engine import *

S_EF, ACC, X_E = 0.500, 0.60, 0.100
READ = (0.835, 0.838, 0.837)                         # so_lieu_mau
TBAR = 0.837
BALL = (71, 85, 105); BALL_HI = (203, 213, 225); RAIL = (196, 200, 212); RAIL_D = (150, 155, 170)
POST = (71, 85, 105); MAG = (124, 58, 237)

DRED = (185, 28, 28); DGREEN = (10, 110, 50); DPURP = (91, 33, 182); DORANGE = (176, 64, 8); SUB = (60, 66, 92)

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-do-toc-do-01.json")))
    assert tuple(r[1] for r in k["so_lieu_mau"]["hang"]) == READ
    assert abs(sum(READ) / 3 - TBAR) < 5e-4 and abs(S_EF / TBAR - 0.597) < 5e-4
    assert abs(0.0005 / S_EF - 0.001) < 1e-9 and abs(0.0005 / 0.250 - 0.002) < 1e-9 and abs((X_E + S_EF) / TBAR - 0.717) < 5e-4
_kiem_so()

def cbar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0))
    d.rounded_rectangle([110, y, 970, y + 80], radius=40, fill=A((246, 244, 250), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(80, 860 * (1 - p)), y + 80], radius=40, fill=A(col, a))

def pill(d, y, s, col, k):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 76), fill=A(col, k), r=36)
    text(d, (W / 2, y + 38), s, 56, WHITE, alpha=k)

def vn(x, nd=3): return f"{x:.{nd}f}".replace(".", ",")


# ---------- mang nghieng, nam cham, hai cong ----------
R0 = (205, 420); ANG = math.radians(12); KPX = 1130.0          # px / m doc mang
RU = (math.cos(ANG), math.sin(ANG)); RN = (RU[1], -RU[0])     # RN: phap tuyen huong len
RB = 22
RR = RB / KPX
# Dong ho chay khi mep truoc bi cham tia E, dung khi mep truoc cham tia F.
TAU_E = math.sqrt(2 * (X_E - RR) / ACC)
T_MODEL = math.sqrt(2 * (X_E + S_EF - RR) / ACC) - TAU_E
def RP(s, h=0.0): return (R0[0] + RU[0] * s * KPX + RN[0] * h, R0[1] + RU[1] * s * KPX + RN[1] * h)

def rig(d, ball_s=None, ball_a=1.0, mag_on=True, beam_cut=(False, False), alpha=1.0, lab=True):
    c = lambda col: A(col, alpha)
    d.polygon([RP(-0.075, 0), RP(0.735, 0), RP(0.735, -26), RP(-0.075, -26)], fill=c(RAIL), outline=c(RAIL_D))
    for k in range(0, 15):
        s = k * 0.05; L = 14 if k % 2 == 0 else 8
        d.line([RP(s, -26), RP(s, -26 + L)], fill=c(RAIL_D), width=2)
    m = [RP(-0.07, 2), RP(-0.022, 2), RP(-0.022, 56), RP(-0.07, 56)]
    d.polygon(m, fill=c(MAG if mag_on else (196, 181, 253)), outline=c(NAVY))
    if lab:
        text(d, (70, 690), "nam châm điện", 56, DPURP, anchor="lm", alpha=alpha)
        q = RP(-0.046, -30); d.line([(q[0], q[1]), (150, 650)], fill=c(MAG), width=3)
    for s, nm in ((X_E, "E"), (X_E + S_EF, "F")):
        b = RP(s, RB)
        d.rectangle([b[0] - 10, 300, b[0] + 10, b[1] - 18], fill=c(POST))
        d.rectangle([b[0] - 22, b[1] - 26, b[0] + 22, b[1] - 12], fill=c(POST))
        text(d, (b[0] + 46, 322), nm, 60, INK, alpha=alpha)
    if ball_s is not None and ball_a > 0.02:
        p = RP(ball_s, RB)
        d.ellipse([p[0] - RB, p[1] - RB, p[0] + RB, p[1] + RB], fill=A(BALL, ball_a * alpha), outline=A(NAVY, ball_a * alpha), width=2)
        d.ellipse([p[0] - 11, p[1] - 13, p[0] - 3, p[1] - 5], fill=A(BALL_HI, ball_a * alpha))
    for s, cut in ((X_E, beam_cut[0]), (X_E + S_EF, beam_cut[1])):
        b = RP(s, RB)
        if not cut: dot(d, b[0], b[1], 7, c(RED))
    if lab:
        a0, a1 = RP(X_E, -70), RP(X_E + S_EF, -70); mid = ((a0[0] + a1[0]) / 2, (a0[1] + a1[1]) / 2)
        arrow(d, mid, a1, c(BLUE), w=4, head=16); arrow(d, mid, a0, c(BLUE), w=4, head=16)
        for s in (X_E, X_E + S_EF): d.line([RP(s, -30), RP(s, -84)], fill=c(BLUE), width=3)
        text(d, (590, 380), "s = 0,500 m", 56, BLUE, alpha=alpha)

def clock(d, y, val, hot=False, alpha=1.0):
    card(d, (40, y, 1040, y + 170), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    card(d, (80, y + 20, 600, y + 150), fill=A(NAVY, alpha), r=18)
    text(d, (340, y + 85), vn(val) + " s", 80, YELLOW if (hot or val > 0) else GRAY, alpha=alpha)
    text(d, (820, y + 85), "MODE A ↔ B", 56, NAVY, alpha=alpha)

def s_at(tau, tk):
    if tau <= TAU_E: return ACC * tau * tau / 2
    tm = TAU_E + (tau - TAU_E) * T_MODEL / tk
    return ACC * tm * tm / 2

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    rig(d, ball_s=0.0)
    clock(d, 785, 0.0)
    k = appear(t, M[1] - 0.3, 0.45)
    if k <= 0: return
    y0 = 985 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, y0 + 22, "DỰ ĐOÁN", PURPLE, k)
    cbar(d, y0 + 118, t, M[1] + 0.3, sc["T"] - 0.15, DPURP, k)
    text(d, (W / 2, y0 + 300), "Thả bi 3 lần.", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 400), "Ba số chỉ lệch cỡ nào?", 62, PURPLE, alpha=k)
    for j in range(3):
        bx = 225 + j * 230; by = y0 + 480 + 10 * math.sin(t * 3 + j)
        card(d, (bx, by, bx + 170, by + 110), fill=A((245, 243, 255), k), outline=A(PURPLE, k), r=18, w=3)
        text(d, (bx + 85, by + 55), "?", 64, PURPLE, alpha=k)

# ---------------- canh 2: Tien hanh (3 lan tha, thoi gian that) ----------------
RUN0, RST, HOLD = 0.5, 0.45, 0.6
def schedule():
    out = []; s = RUN0
    for tk in READ:
        L = RST + TAU_E + tk + 0.35 + HOLD
        out.append((s, L)); s += L
    return out
SCHED = schedule()
BADGE = SCHED[-1][0] + SCHED[-1][1] + 0.2

def run_state(t):
    if t < SCHED[0][0]: return 0, -1, 0.0, 0.0, 0
    j = 0
    for i, (s, L) in enumerate(SCHED):
        if t >= s: j = i
    s, L = SCHED[j]; tk = READ[j]
    tau = t - s - RST
    if tau < 0: return j, tau, 0.0, 0.0, j
    te = tau - TAU_E
    clk = 0.0 if te < 0 else (tk if te >= tk else math.floor(te * 1000) / 1000)
    done = j + (1 if te >= tk else 0)
    return j, tau, s_at(tau, tk), clk, done

def s_do(img, d, t, sc):
    j, tau, bs, clk, done = run_state(t)
    card(d, (40, 265, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    ba = 1.0 if bs < 0.70 else clamp(1 - (bs - 0.70) / 0.04)
    cutE = abs(bs - X_E) * KPX < RB; cutF = abs(bs - X_E - S_EF) * KPX < RB
    rig(d, ball_s=bs, ball_a=ba, mag_on=tau < 0, beam_cut=(cutE, cutF))
    run = 0 <= tau - TAU_E < READ[j]
    clock(d, 785, clk, hot=run)
    y = 985
    card(d, (40, y, 1040, y + 420), fill=WHITE, outline=LIGHT, w=3)
    XS = (300, 700)
    text(d, (XS[0], y + 60), "Lần", 56, INK); text(d, (XS[1], y + 60), "t (s)", 56, INK)
    d.line([(90, y + 115), (990, y + 115)], fill=LIGHT, width=3)
    for i, tk in enumerate(READ):
        yy = y + 180 + i * 85
        if i == j and done <= i and t >= SCHED[0][0]:
            d.rounded_rectangle([80, yy - 40, 1000, yy + 40], radius=16, fill=(255, 247, 237))
        text(d, (XS[0], yy), str(i + 1), 56, MUTED)
        if i < done: text(d, (XS[1], yy), vn(tk), 60, NAVY)
    ka = appear(t, BADGE, 0.4)
    if ka > 0:
        s_ = "ĐÁP ÁN: lệch vài phần nghìn giây"; pw = tw(d, s_, F(56)) + 60
        card(d, (W / 2 - pw / 2, 1440, W / 2 + pw / 2, 1540), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1490), s_, 56, DGREEN, alpha=ka)

# ---------------- canh 3: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 260, 1020, 840), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (W / 2, 350), "t trung bình = 0,837 s", 62, DGREEN, alpha=a)
    text(d, (W / 2, 490), "v trung bình = s : t", 62, INK, alpha=a)
    text(d, (W / 2, 600), "= 0,500 m : 0,837 s", 62, INK, alpha=a)
    pu = 0.55 + 0.45 * math.sin(t * 4)
    yb = 720 + 8 * math.sin(t * 3)
    d.rounded_rectangle([320, yb - 52, 760, yb + 52], radius=24, fill=A((219, 234, 254), a * pu), outline=A(BLUE, a), width=5)
    text(d, (W / 2, yb), "≈ 0,597 m/s", 66, BLUE, alpha=a)
    card(d, (60, 880, 1020, 1480), fill=A(WHITE, a), outline=A(ORANGE, a), w=4)
    for x in range(110, 980, 29):                                         # thuoc chia mm (hien san, chu hien sau)
        L = 44 if (x - 110) % 290 == 0 else 22
        d.line([(x, 930), (x, 930 + L)], fill=A(INK, a), width=3)
    xc = 110 + 29 * 15 + 14.5 * math.sin(t * 3)                         # mep vat lech toi nua vach
    d.polygon([(xc, 1000), (xc - 16, 1028), (xc + 16, 1028)], fill=A(ORANGE, a))
    k = appear(t, M[1] - 0.05, 0.4)
    if k <= 0: return
    text(d, (W / 2, 1100), "sai số Δs = 0,0005 m", 62, DORANGE, alpha=k)
    text(d, (W / 2, 1220), "tỉ đối δs = 0,0005 : 0,500", 60, INK, alpha=k)
    yb = 1360 + 8 * math.sin(t * 3)
    d.rounded_rectangle([380, yb - 52, 700, yb + 52], radius=24, fill=A((255, 237, 213), k * (0.55 + 0.45 * math.sin(t * 4))), outline=A(ORANGE, k), width=5)
    text(d, (W / 2, yb), "= 0,10 %", 66, DORANGE, alpha=k)

# ---------------- canh 4: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    k = appear(t, 0.05, 0.35)
    card(d, (40, 265, 1040, 760), fill=A(WHITE, k), outline=LIGHT, w=3)
    rig(d, ball_s=X_E + S_EF, alpha=k, lab=False)
    p = RP(X_E + S_EF, RB); pu = 0.5 + 0.5 * math.sin(t * 5)
    d.ellipse([p[0] - 50, p[1] - 50, p[0] + 50, p[1] + 50], outline=A(PURPLE, k * pu), width=6)
    card(d, (60, 840, 1020, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 950), "Chưa nói được", 62, NAVY, alpha=k)
    text(d, (W / 2, 1080), "Tốc độ tại F?", 62, BLUE, alpha=k)
    text(d, (W / 2, 1200 + 12 * math.sin(t * 3)), "?", 72, PURPLE, alpha=k)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 260, 1020, 520), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    text(d, (W / 2, 340), "✗ s = 0,600 m (từ chỗ thả)", 60, DRED, alpha=a)
    text(d, (W / 2, 440), "v ≈ 0,717 m/s", 60, DRED, alpha=a)
    ok = appear(t, M[1] - 0.05, 0.4)
    card(d, (60, 560, 1020, 1480), fill=A(WHITE, a), outline=A(GREEN if ok > 0 else NAVY, a), w=5)
    gx = lambda m: 150 + 1250 * m                                             # mang nam ngang, 0,6 m -> 750 px
    yr = 900
    d.rectangle([gx(-0.04), yr, gx(0.66), yr + 22], fill=A(RAIL, a), outline=A(RAIL_D, a))
    d.rectangle([gx(-0.04), yr - 60, gx(-0.005), yr], fill=A(MAG, a))
    for m, nm in ((X_E, "E"), (X_E + S_EF, "F")):
        d.rectangle([gx(m) - 8, yr - 120, gx(m) + 8, yr], fill=A(POST, a)); dot(d, gx(m), yr - 22, 7, A(RED, a))
        text(d, (gx(m) + 40, yr - 150), nm, 60, INK, alpha=a)
    if ok <= 0:
        pu = 0.6 + 0.4 * math.sin(t * 4)
        ya = yr + 110
        arrow(d, (gx(0.3), ya), (gx(0), ya), A(DRED, a), w=6, head=20); arrow(d, (gx(0.3), ya), (gx(0.6), ya), A(DRED, a), w=6, head=20)
        d.line([(gx(0), yr + 30), (gx(0), ya + 30)], fill=A(DRED, a * pu), width=4)
        text(d, (W / 2, ya + 90), "0,600 m", 60, DRED, alpha=a)
        return
    ya = yr + 110
    arrow(d, (gx(0.35), ya), (gx(X_E), ya), A(GREEN, ok), w=7, head=22); arrow(d, (gx(0.35), ya), (gx(0.6), ya), A(GREEN, ok), w=7, head=22)
    for m in (X_E, 0.6): d.line([(gx(m), yr + 30), (gx(m), ya + 30)], fill=A(GREEN, ok), width=4)
    text(d, (gx(0.35), ya + 90), "0,500 m", 60, DGREEN, alpha=ok)
    text(d, (W / 2, 1260), "✓ s = EF = 0,500 m", 62, DGREEN, alpha=ok)
    text(d, (W / 2, 1370), "→ 0,597 m/s", 62, DGREEN, alpha=ok)

# ---------------- canh 6: THU NGHI ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 220, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 250, "THỬ NGHĨ", ORANGE, k1)
    gx = lambda m: 200 + 2400 * m                                             # 0,250 m -> 600 px
    yr = 560
    d.rectangle([110, yr, 970, yr + 22], fill=A(RAIL, k1), outline=A(RAIL_D, k1))
    for x in range(120, 970, 24): d.line([(x, yr + 22), (x, yr + 34)], fill=A(RAIL_D, k1), width=2)
    for m, nm in ((0.0, "E"), (0.25, "F")):
        d.rectangle([gx(m) - 8, yr - 120, gx(m) + 8, yr], fill=A(POST, k1)); dot(d, gx(m), yr - 22, 7, A(RED, k1))
        text(d, (gx(m) + 40, yr - 150), nm, 60, INK, alpha=k1)
    ya = yr + 110
    arrow(d, (gx(0.125), ya), (gx(0), ya), A(BLUE, k1), w=5, head=18); arrow(d, (gx(0.125), ya), (gx(0.25), ya), A(BLUE, k1), w=5, head=18)
    text(d, (gx(0.125), ya + 85), "s = 0,250 m", 60, BLUE, alpha=k1)
    text(d, (W / 2, 960), "Dời F lại gần E.", 60, INK, alpha=k1)
    text(d, (W / 2, 1060), "Vẫn thước chia mm:", 60, ORANGE, alpha=k1)
    text(d, (W / 2, 1160), "δs bằng bao nhiêu?", 60, ORANGE, alpha=k1)
    cbar(d, 1300, t, 1.0, sc["T"] - 0.2, DORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for s, L in SCHED: cs.append((do["t0"] + s + RST + TAU_E, "tap"))
    cs += [(do["t0"] + BADGE, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1], "ding"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-do-toc-do-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Đo tốc độ của vật · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai cổng quang E, F", draw=s_hook, tail=0.3, caps=[
   ("Bi lăn từ E tới F.", 2.8),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Thả bi ba lần", draw=s_do, tail=0.3, caps=[
   ("Tia E: chạy. Tia F: dừng.", 5.0),
   ("Thả lại, cùng một chỗ.", 6.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Lấy trung bình ba lần.", 3.0),
   ("Thước chia mm: lệch nửa vạch.", 6.6)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Đây là trung bình cả đoạn.", 3.5)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đo s từ chỗ thả?", 3.3),
   ("Đồng hồ chỉ đếm từ E.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])
