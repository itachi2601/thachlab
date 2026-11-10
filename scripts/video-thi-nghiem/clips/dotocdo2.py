# Clip: tn-l10-do-toc-do-02 - Bi chan mot cong quang F (MODE B, v = d/t); tia lech tam (10/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-toc-do-02.json:
#   tham_so: d = 20,0 mm (thuoc kep, dd = 0,05 mm), lech 0-8 mm, v_F that = 0,849 m/s, dong ho chia 0,001 s.
#   so_lieu_mau: t = 0,024 / 0,023 / 0,024 s; ghi_chu: t mo hinh 0,0236 s; tia lech 6 mm -> day cung 16 mm, d/t lon hon that 25 %.
#   rut_ra: tb = 0,024 s; dt = 0,001 s; delta t ~ 4,17 %; delta d = 0,25 %; v_F = 0,83 +- 0,04 m/s (4,4 %) > 0,597 m/s tren EF.
# Khac dotocdo3 (4 tam chan rong/hep, d/t voi xe nhanh dan): o day MOT vien bi, can canh do CAO tia so voi tam bi.
# Du doan: tia lech tam -> d/t lon hay nho hon toc do that (dap an: lon hon). Tien hanh dung tia QUA tam (khong lo).
# Cau chot: lech 8 mm (bien tren cua tham_so) -> day cung 2*sqrt(10^2 - 8^2) = 12 mm, chua tung hien.
# Canh: Du doan -> Tien hanh (3 lan, chieu cham 40 lan) -> Dap an (lan lech 6 mm + hinh day cung) -> Rut ra
#       (v_F +- dv, so voi 0,597; chua noi duoc) -> Bay (ban kinh) -> Chot + cau hoi.
from engine import *

D_MM, VF, LECH = 20.0, 0.849, 6.0
READ = (0.024, 0.023, 0.024)                         # so_lieu_mau
T_BLK = 0.0236                                       # ghi_chu: t mo hinh
SLOW = 40.0
PXM = 12.0                                           # px / mm trong can canh
RB = D_MM / 2 * PXM                                  # 120 px
BALL = (71, 85, 105); BALL_HI = (203, 213, 225); RAIL = (196, 200, 212); RAIL_D = (150, 155, 170); POST = (71, 85, 105)
XB = 560                                             # x cua tia sang

def vn(x, nd=3): return f"{x:.{nd}f}".replace(".", ",")

def seq(d, x, y, parts, size, color=INK, alpha=1.0, anchor="m"):
    """parts: chuoi, ('bar','t') gach tren, ('sub','v','F') chi so duoi."""
    f = F(size); fs = F(max(36, int(size * 0.62)))
    def wid(p):
        if isinstance(p, str): return tw(d, p, f)
        if p[0] == "bar": return tw(d, p[1], f)
        return tw(d, p[1], f) + tw(d, p[2], fs) + 2
    tot = sum(wid(p) for p in parts); xx = x - tot / 2 if anchor == "m" else x
    for p in parts:
        if isinstance(p, str): dtext(d, (xx, y), p, f, color, alpha, "lm")
        elif p[0] == "bar":
            dtext(d, (xx, y), p[1], f, color, alpha, "lm"); w = tw(d, p[1], f)
            d.line([(xx + 1, y - size * 0.62), (xx + w + 1, y - size * 0.62)], fill=A(color, alpha), width=max(3, size // 14))
        else:
            dtext(d, (xx, y), p[1], f, color, alpha, "lm")
            dtext(d, (xx + tw(d, p[1], f) + 2, y + size * 0.28), p[2], fs, color, alpha, "lm")
        xx += wid(p)

# ---------- can canh cong F: bi lan tren ray, tia sang vuong goc man hinh ----------
def gate(d, top, rail_y, beam_y, bx, blocked, lech_lab=None, show_center=False, chord=False, alpha=1.0):
    c = lambda col: A(col, alpha)
    cy = rail_y - RB
    d.rectangle([60, rail_y, 1020, rail_y + 22], fill=c(RAIL), outline=c(RAIL_D))
    d.rectangle([XB - 11, top, XB + 11, beam_y - 30], fill=c(POST))                 # cang cua cong (o sau)
    d.rectangle([XB - 26, beam_y - 34, XB + 26, beam_y - 18], fill=c(POST))
    if bx is not None:
        d.ellipse([bx - RB, cy - RB, bx + RB, cy + RB], fill=c(BALL), outline=c(NAVY), width=3)
        d.ellipse([bx - 70, cy - 82, bx - 30, cy - 42], fill=c(BALL_HI))
        th = (bx - XB) / RB                                                             # lan khong truot: goc = x / r
        d.line([(bx, cy), (bx + RB * 0.82 * math.sin(th), cy - RB * 0.82 * math.cos(th))], fill=c((148, 163, 184)), width=6)
        if show_center:
            d.line([(bx - 14, cy), (bx + 14, cy)], fill=c(WHITE), width=4); d.line([(bx, cy - 14), (bx, cy + 14)], fill=c(WHITE), width=4)
        if chord and abs(beam_y - cy) < RB:
            hc = math.sqrt(RB * RB - (beam_y - cy) ** 2)
            d.line([(bx - hc, beam_y), (bx + hc, beam_y)], fill=c(ORANGE), width=7)
    if blocked: d.ellipse([XB - 13, beam_y - 13, XB + 13, beam_y + 13], outline=c((254, 202, 202)), width=4)
    else: dot(d, XB, beam_y, 11, c(RED))
    text(d, (XB + 170, top + 30), "cổng F", 42, INK, alpha=alpha)
    text(d, (XB + 170, top + 100), "tia sáng", 40, RED, alpha=alpha)
    d.line([(XB + 100, top + 112), (XB + 14, beam_y - 10)], fill=c(RED), width=3)

def clock(d, y, val, hot=False):
    card(d, (40, y, 1040, y + 160), fill=WHITE, outline=LIGHT, w=3)
    card(d, (80, y + 22, 540, y + 138), fill=NAVY, r=18)
    text(d, (310, y + 80), vn(val) + " s", 62, YELLOW if (hot or val > 0) else GRAY)
    text(d, (790, y + 58), "đồng hồ 0,001 s", 40, INK, bold=False)
    text(d, (790, y + 112), "MODE B", 44, NAVY)

def dim_d(d, cx, y, alpha=1.0, lab="d = 20,0 mm"):
    a0, a1 = (cx - RB, y), (cx + RB, y)
    arrow(d, (cx, y), a0, A(BLUE, alpha), w=4, head=16); arrow(d, (cx, y), a1, A(BLUE, alpha), w=4, head=16)
    text(d, (cx, y - 36), lab, 42, BLUE, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
RAIL1, BEAM_C = 740, 740 - RB                          # tia qua tam: cao bang tam bi
BEAM_L = BEAM_C - LECH * PXM                           # tia lech 6 mm (72 px)
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    bx = XB - RB - 150
    gate(d, 290, RAIL1, BEAM_L, bx, False, show_center=True)
    cy = RAIL1 - RB
    for i in range(14):                                               # net dut ngang tam bi -> toi cot tia
        x0 = bx + 20 + i * 28; d.line([(x0, cy), (x0 + 14, cy)], fill=GRAY, width=3)
    d.line([(XB + 46, BEAM_L), (XB + 46, cy)], fill=ORANGE, width=4)
    for yy in (BEAM_L, cy): d.line([(XB + 34, yy), (XB + 58, yy)], fill=ORANGE, width=4)
    text(d, (XB + 76, (BEAM_L + cy) / 2), "lệch 6 mm", 40, ORANGE, anchor="lm")
    text(d, (bx, cy + 52), "tâm", 38, WHITE)
    for xx in (bx - RB, bx + RB): d.line([(xx, cy - RB - 44), (xx, cy - 8)], fill=BLUE, width=2)
    dim_d(d, bx, cy - RB - 28, lab="d = 20,0 mm")
    clock(d, 815, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 570), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 175, "Tia sáng lệch khỏi tâm bi.", 46, INK, bold=False, maxw=900, alpha=a)
    ctext(d, y0 + 290, "d/t tính ra so với", 54, INK, maxw=900, alpha=a)
    ctext(d, y0 + 365, "tốc độ thật của bi?", 54, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 480, 940, y0 + 494], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 480, 140 + 800 * (1 - p), y0 + 494], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (tia qua tam, 3 lan, chieu cham 40 lan) ----------------
APP, EXIT, HOLD, RST = 0.55, 0.45, 0.75, 0.35
RUN0 = 0.5
VPX = VF * 1000 / SLOW * PXM                           # px/s tren man: 255 px/s
BLK = T_BLK * SLOW                                     # 0,944 s chan tia tren man
def schedule():
    out = []; s = RUN0
    for _ in READ:
        L = RST + APP + BLK + EXIT + HOLD; out.append((s, L)); s += L
    return out
SCHED = schedule()

def run_state(t):
    """-> (lan j, tau tren man ke tu luc mep truoc cham tia, x tam bi, so dong ho, so hang xong)."""
    if t < SCHED[0][0]: return 0, -9, None, 0.0, 0
    j = 0
    for i, (s, L) in enumerate(SCHED):
        if t >= s: j = i
    s, L = SCHED[j]; tk = READ[j]
    u = t - s - RST - APP                              # 0 = mep truoc cham tia
    if t - s < RST: return j, u, None, 0.0, j          # RESET: dong ho ve 0, bi chua vao khung
    uc = min(u, BLK + EXIT)
    bx = XB - RB + uc * VPX
    real = u / SLOW
    clk = 0.0 if u < 0 else (tk if u >= BLK else min(tk, math.floor(real * 1000) / 1000))
    return j, u, bx, clk, j + (1 if u >= BLK else 0)

def s_do(img, d, t, sc):
    j, u, bx, clk, done = run_state(t)
    card(d, (40, 265, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    blocked = bx is not None and 0 <= u < BLK
    sub = Image.new("RGB", (1000, 535), WHITE); sd = ImageDraw.Draw(sub, "RGBA")
    old = IMG_REF[0]; IMG_REF[0] = sub
    def sh(y): return y - 265
    # ve can canh len anh phu de bi cat dung mep khung
    cy = RAIL1 - RB
    sd.rectangle([20, sh(RAIL1), 980, sh(RAIL1) + 22], fill=RAIL, outline=RAIL_D)
    sd.rectangle([XB - 40 - 11, sh(290), XB - 40 + 11, sh(BEAM_C) - 30], fill=POST)
    sd.rectangle([XB - 40 - 26, sh(BEAM_C) - 34, XB - 40 + 26, sh(BEAM_C) - 18], fill=POST)
    if bx is not None:
        x = bx - 40
        sd.ellipse([x - RB, sh(cy) - RB, x + RB, sh(cy) + RB], fill=BALL, outline=NAVY, width=3)
        sd.ellipse([x - 70, sh(cy) - 82, x - 30, sh(cy) - 42], fill=BALL_HI)
        th = (bx - XB) / RB
        sd.line([(x, sh(cy)), (x + RB * 0.82 * math.sin(th), sh(cy) - RB * 0.82 * math.cos(th))], fill=(148, 163, 184), width=6)
    if blocked: sd.ellipse([XB - 40 - 13, sh(BEAM_C) - 13, XB - 40 + 13, sh(BEAM_C) + 13], outline=(254, 202, 202), width=4)
    else: dot(sd, XB - 40, sh(BEAM_C), 11, RED)
    IMG_REF[0] = old
    m = Image.new("L", sub.size, 0); ImageDraw.Draw(m).rounded_rectangle([3, 3, 996, 531], radius=30, fill=255)
    img.paste(sub, (40, 265), m)
    d.rounded_rectangle((40, 265, 1040, 800), radius=34, outline=LIGHT, width=3)
    text(d, (XB + 170, 320), "cổng F", 42, INK)
    text(d, (XB + 190, 390), "tia qua tâm", 40, RED)
    d.line([(XB + 100, 402), (XB + 14, BEAM_C - 10)], fill=RED, width=3)
    text(d, (180, 320), "chậm 40 lần", 38, INK, bold=False)
    clock(d, 815, clk, hot=blocked)
    y = 1000
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

# ---------------- canh 3: Dap an (lan tia lech 6 mm + hinh day cung) ----------------
RAIL3 = 760
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · lớn hơn thật"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 318), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 284), lb, 40, WHITE, alpha=ka)
    card(d, (40, 340, 1040, 810), fill=WHITE, outline=LIGHT, w=3)
    beam = RAIL3 - RB - LECH * PXM
    u = t - 0.9 - APP                                       # 0 = bi bat dau che tia (lech: khi |x - XB| = 8 mm)
    hc = math.sqrt(RB * RB - (LECH * PXM) ** 2)             # 96 px = 8 mm
    blk = 2 * hc / VPX
    bx = XB - hc + clamp(u, -APP, blk + EXIT) * VPX
    blocked = 0 <= u < blk
    gate(d, 360, RAIL3, beam, bx, blocked, chord=blocked or u >= blk)
    text(d, (180, 395), "lệch 6 mm", 40, ORANGE)
    # hinh day cung tinh (ti le 15 px/mm)
    kg = appear(t, M[0] + 1.0, 0.5)
    if kg > 0:
        card(d, (40, 830, 1040, 1250), fill=A(WHITE, kg), outline=A(LIGHT, kg), w=3)
        cx, cy, R = 330, 1040, 150; k = R / 10.0
        d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A((226, 232, 240), kg), outline=A(NAVY, kg), width=4)
        yb = cy - 6 * k; hx = 8 * k
        d.line([(cx - R, cy), (cx + R, cy)], fill=A(BLUE, kg), width=4)                       # duong kinh
        d.line([(cx - hx, yb), (cx + hx, yb)], fill=A(ORANGE, kg), width=7)                   # day cung
        d.line([(cx, cy), (cx, yb)], fill=A(INK, kg), width=3)
        d.line([(cx, cy), (cx + hx, yb)], fill=A(INK, kg), width=3)
        dot(d, cx, cy, 6, A(INK, kg))
        text(d, (cx - 30, (cy + yb) / 2), "6", 38, INK, alpha=kg)
        text(d, (cx + hx / 2 + 10, (cy + yb) / 2 + 30), "10", 38, INK, alpha=kg)
        text(d, (cx + hx / 2, yb - 30), "8", 38, ORANGE, alpha=kg)
        k2 = appear(t, M[1] + 0.2, 0.5)
        text(d, (560, 930), "bi che tia trên", 40, INK, bold=False, anchor="lm", alpha=k2)
        text(d, (560, 990), "16 mm", 54, ORANGE, anchor="lm", alpha=k2)
        text(d, (560, 1070), "phép tính lấy", 40, INK, bold=False, anchor="lm", alpha=k2)
        text(d, (560, 1130), "20 mm", 54, BLUE, anchor="lm", alpha=k2)
    k3 = appear(t, M[1] + 1.6, 0.5)
    card(d, (40, 1275, 1040, 1560), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
    ctext(d, 1360, "t ngắn lại, d giữ nguyên:", 46, GREEN, maxw=900, alpha=k3)
    ctext(d, 1460, "d/t lớn hơn thật 25 %", 52, GREEN, maxw=900, alpha=k3)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1010), fill=WHITE, outline=LIGHT, w=3)
    k1 = appear(t, 0.3, 0.45)
    seq(d, 90, 340, [("bar", "t"), " ≈ 0,024 s;  Δt = 0,001 s"], 50, INK, alpha=k1, anchor="l")
    k2 = appear(t, 1.2, 0.45)
    seq(d, 90, 450, [("sub", "v", "F"), " = 0,0200 : 0,024 ≈ 0,83 m/s"], 50, INK, alpha=k2, anchor="l")
    text(d, (370, 512), "20,0 mm", 38, MUTED, bold=False, alpha=k2)
    k3 = appear(t, M[1] - 0.1, 0.45)
    seq(d, 90, 620, ["δv = 0,25 % + 4,17 % ≈ 4,4 %"], 50, INK, alpha=k3, anchor="l")
    text(d, (250, 682), "δd: thước kẹp", 38, MUTED, bold=False, alpha=k3)
    text(d, (520, 682), "δt", 38, MUTED, bold=False, alpha=k3)
    k4 = appear(t, M[1] + 1.2, 0.5)
    card(d, (90, 735, 990, 865), fill=A((236, 253, 243), k4), outline=A(GREEN, k4), r=24, w=4)
    seq(d, W / 2, 800, [("sub", "v", "F"), " = 0,83 ± 0,04 m/s"], 54, GREEN, alpha=k4)
    k5 = appear(t, M[1] + 2.2, 0.5)
    seq(d, W / 2, 935, ["trên EF: ", ("sub", "v", "tb"), " = 0,597 m/s"], 44, BLUE, alpha=k5)
    k6 = appear(t, M[2] - 0.1, 0.45)
    if k6 > 0:
        y0 = 1040 + (1 - k6) * 30
        card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, k6), outline=A(NAVY, k6), w=6)
        text(d, (W / 2, y0 + 65), "Chưa nói được", 46, NAVY, alpha=k6)
        kk = k6 * appear(t, M[2] + 0.4, 0.4)
        card(d, (80, y0 + 125, 1000, y0 + 420), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, y0 + 210), "Tốc độ ở điểm khác", 48, RED, alpha=kk)
        text(d, (W / 2, y0 + 320), "trên máng", 48, RED, alpha=kk)

# ---------------- canh 5: Bay (lay ban kinh) ----------------
def s_bay(img, d, t, sc):
    a1 = appear(t, 0.2, 0.45); y0 = 265
    card(d, (40, y0, 1040, y0 + 1300), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    q = "“Lấy d = 10,0 mm”"
    ks = clamp((t - 0.9) / 0.4); f = F(50); lw = tw(d, q, f); yy = y0 + 210
    text(d, (W / 2, yy), q, 50, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0:
        d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        text(d, (W / 2 + lw / 2 + 40, yy), "✗", 54, RED, alpha=ks * a1)
    kk = a1 * appear(t, 1.4, 0.5)                      # hinh + ket luan hien cung luc
    cx, cy, R = 540, y0 + 520, 150
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A((226, 232, 240), kk), outline=A(NAVY, kk), width=4)
    dot(d, cx, cy, 7, A(INK, kk))
    d.line([(cx, cy), (cx, cy - R)], fill=A(MUTED, kk), width=4)
    text(d, (cx + 70, cy - R / 2), "10,0", 40, MUTED, alpha=kk)
    arrow(d, (cx, cy + R + 50), (cx - R, cy + R + 50), A(GREEN, kk), w=5, head=18)
    arrow(d, (cx, cy + R + 50), (cx + R, cy + R + 50), A(GREEN, kk), w=5, head=18)
    for xx in (cx - R, cx + R): d.line([(xx, cy), (xx, cy + R + 66)], fill=A(GREEN, kk), width=3)
    text(d, (cx, cy + R + 100), "20,0 mm", 46, GREEN, alpha=kk)
    card(d, (90, y0 + 900, 990, y0 + 1240), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, y0 + 990), "Bi che tia suốt", 54, GREEN, alpha=kk)
    text(d, (W / 2, y0 + 1090), "cả đường kính", 54, GREEN, alpha=kk)
    text(d, (W / 2, y0 + 1180), "d = 20,0 mm = 0,0200 m", 44, NAVY, alpha=kk)

# ---------------- canh 6: Chot + cau hoi ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        kb = appear(t, M[0] + 0.6, 0.5)
        if kb > 0:
            cx, cy, R = 540, 1090, 110; yb = cy - 8 * R / 10
            d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A((226, 232, 240), kb), outline=A(NAVY, kb), width=4)
            for i in range(16):
                x0 = cx - 260 + i * 34; d.line([(x0, yb), (x0 + 18, yb)], fill=A(RED, kb), width=4)
            dot(d, cx, cy, 6, A(INK, kb))
            d.line([(cx + R + 40, cy), (cx + R + 40, yb)], fill=A(ORANGE, kb), width=4)
            for yy in (cy, yb): d.line([(cx + R + 28, yy), (cx + R + 52, yy)], fill=A(ORANGE, kb), width=4)
            text(d, (cx + R + 70, (cy + yb) / 2), "8 mm", 42, ORANGE, anchor="lm", alpha=kb)
        kh = appear(t, M[0] + 2.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Bán kính 10,0 mm", 44, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Tia phải đi qua tâm bi",
             "Lệch tâm 8 mm: bi che tia trên bao nhiêu mm?", None, body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.3, "ding")]
    for s, L in SCHED: cs.append((do["t0"] + s + RST + APP, "tap"))           # mep truoc cham tia
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 1.2, "tap"),
           (b["t0"] + 0.9, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-do-toc-do-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Đo tốc độ của vật · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tia sáng ở đâu trên bi?", draw=s_hook, tail=0.8, caps=[
   ("Một cổng quang, MODE B.", 2.5),
   ("Dừng video, chọn câu trả lời.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Bi chắn tia: đồng hồ chạy.", 4.2),
   ("Tia qua tâm. Lặp 3 lần.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Cùng viên bi, tia lệch tâm.", 3.4),
   ("Thời gian chắn tia ngắn lại.", 4.0)]),
 dict(key="rutra", title="Ghi kết quả", draw=s_rutra, tail=0.5, caps=[
   ("Đổi mm ra m rồi chia.", 3.2),
   ("Chia thì cộng phần trăm.", 3.6),
   ("Còn một điều chưa biết.", 3.2)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("Nhìn con số d.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 5.4)]),
])
