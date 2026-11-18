# Clip: tn-l10-nang-luong-cong-02 - Dua xe len cung do cao bang nhieu duong (lo 9, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-nang-luong-cong-02.json:
#   tham_so: P = 2,0 N ; h = 0,20 m ; s 0,2..1,2 m ; mu 0..0,1 ; luc ke 0-2,5 N do chia 0,02 N.
#   so_lieu_mau (s m, F N, A = F.s J): 0,20 (thang dung) 2,00 0,400 ; 0,40 1,06 0,424 ; 0,80 0,56 0,448 ; 1,00 0,46 0,460.
#   P.h = 0,40 J (quan_sat) -> cong trong luc khi di len A_P = -P.h = -0,40 J o moi duong (muc 3 cua bai). Kiem: _kiem_so().
# Du doan (K10: chi cau hoi + hinh): hai mang cung cao 0,20 m, mang dai gap doi (0,40 -> 0,80 m): cong keo F.s the nao?
#   A. Giam con mot nua (luc nho hon) ; B. Gap doi (duong dai gap doi) ; C. Gan nhu khong doi (DUNG: 0,424 -> 0,448 J).
# KHONG tra loi san cau sau hop ("Lan nao lech nhieu nhat? Phan cong doi ra di dau?"): khong noi +15 %, khong noi ma sat
#   lan / cong can; "phan doi ra di dau" de o the "Chua noi duoc".
# Bay = hien_tuong_hay_sai[0] (mang dai, luc nho -> ton it cong) -> hinh dien tich F x s.
# Cau chot (ca tu suy, ghi trong ghi_chu kho): mang 0,50 m (trong 0,2-1,2), mu = 0 (trong 0-0,1), keo deu
#   doi ca P va h: xe 3,0 N, dinh 0,30 m, mang 0,75 m (trong 0,2-1,2), mu = 0, keo deu
#   -> F.s = P.h = 0,90 J -> F = 0,90/0,75 = 1,20 N (= P.sin(theta), sin(theta) = 0,4). Khong so nao hien tren man.
# Khuon van nghieng chep tu clips/hieusuat2.py (khong import cheo): dinh mang co dinh o mep be cao 20 cm; 6 px/cm.
from engine import *

ROWS = [(0.20, 2.00, 0.400), (0.40, 1.06, 0.424), (0.80, 0.56, 0.448), (1.00, 0.46, 0.460)]
P_N, H_M, PH = 2.0, 0.20, 0.40
HCM = 20
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def _kiem_so():
    bad = []
    for s, f, a in ROWS:
        if abs(round(f * s, 3) - a) > 1e-9: bad.append(("A", s))
        th = math.asin(H_M / s); fm = P_N * math.sin(th) + 0.03 * P_N * math.cos(th)
        if abs(fm - f) > 0.02 + 1e-9 and s != 0.20: bad.append(("F mo hinh", s, round(fm, 3)))
    if abs(P_N * H_M - PH) > 1e-9: bad.append("P.h")
    if abs(3.0 * 0.30 / 0.75 - 1.20) > 1e-9: bad.append("chot")
    return bad

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); BOARD = (222, 184, 135); CART = (96, 165, 250); CART_D = (37, 99, 235)
SKIN = (240, 196, 160); DRED = (185, 28, 28); NOTE = (60, 64, 84); DGREEN = (21, 110, 55)

TOK2 = re.compile(r"(_\{[^}]*\})")
def rs(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chu co chi so duoi; chi so >= 40 px (brief lo 9)."""
    sub = max(40, int(size * 0.72)); segs = []
    for p in [p for p in TOK2.split(s) if p]:
        segs.append((p[2:-1], sub, size * 0.30) if p.startswith("_{") else (p, size, 0))
    tot = sum(tw(d, x, F(z)) for x, z, _ in segs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for s_, z, dy in segs:
        dtext(d, (x, cy + dy), s_, F(z), color, alpha, "lm"); x += tw(d, s_, F(z))
    return tot

def dash(d, p, q, color, w=4, seg=16, gap=12):
    L = math.dist(p, q); n = int(L // (seg + gap)) + 1
    for i in range(n):
        a = i * (seg + gap) / L; b = min(1, (i * (seg + gap) + seg) / L)
        if a >= 1: break
        d.line([(lerp(p[0], q[0], a), lerp(p[1], q[1], a)), (lerp(p[0], q[0], b), lerp(p[1], q[1], b))], fill=color, width=w)

# ---------------- khuon mang nghieng (chep tu hieusuat2) ----------------
PXC = 6.0; TX, TY = 660, 740; YF = TY + HCM * PXC
CL, CH = 76, 40
ROPE, BODY = 24, 230
XV = 590                                                 # duong keo thang dung (sat be)

def ang_of(s): return math.degrees(math.asin(H_M / s))

def ramp_q(alpha):
    a = math.radians(alpha); ux, uy = math.cos(a), -math.sin(a); nx, ny = -math.sin(a), -math.cos(a)
    L = HCM / math.sin(a) * PXC; fx, fy = TX - L * ux, TY - L * uy
    return (lambda q, h=0.0: (fx + q * ux + h * nx, fy + q * uy + h * ny)), L

def shelf(d):
    d.line([(50, YF), (1030, YF)], fill=INK, width=4)
    d.rectangle([TX, TY, 1010, YF], fill=WOOD, outline=WOOD_D, width=3)
    d.line([(990, TY + 8), (990, YF - 8)], fill=WHITE, width=3)
    for yy in (TY + 8, YF - 8): d.line([(978, yy), (1002, yy)], fill=WHITE, width=3)
    text(d, (830, (TY + YF) / 2), "cao 0,20 m", 42, WHITE)

def ramp(d, alpha, ghost=False, k=1.0):
    Q, L = ramp_q(alpha)
    if ghost:
        dash(d, Q(0), Q(L), A(NAVY, k), w=5); return Q, L
    d.polygon([Q(0), Q(L), (TX, YF)], fill=A((241, 245, 249), k))
    d.polygon([Q(0, 0), Q(L, 0), Q(L, -12), Q(0, -12)], fill=A(BOARD, k), outline=A(WOOD_D, k))
    return Q, L

def cart(d, Q, q, alpha_k=1.0):
    c = lambda col: A(col, alpha_k)
    for dq in (-22, 22):
        x, y = Q(q + dq, 9); d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=c(NAVY))
    d.polygon([Q(q - CL / 2, 16), Q(q + CL / 2, 16), Q(q + CL / 2, 16 + CH), Q(q - CL / 2, 16 + CH)], fill=c(CART), outline=c(CART_D))

def meter_ramp(d, Q, q, f_read, alpha_k=1.0):
    q0 = q + CL / 2
    Qk = lambda s, h=0.0: Q(q0 + s, 36 + h)
    d.line([Qk(0), Qk(ROPE - 13)], fill=A(NAVY, alpha_k), width=5)
    se = luc_ke(d, Qk, ROPE, ROPE + 16, ROPE + 16 + BODY, 2.5, f_read, nho=0.1, so=(0, 1, 2), hw=30, ben=1,
                alpha=alpha_k, co=40)
    d.line([Qk(se - 16), Qk(se + 8)], fill=A(NAVY, alpha_k), width=8)
    hx, hy = Qk(se + 34); dot(d, hx, hy, 26, A(SKIN, alpha_k), outline=A((190, 140, 105), alpha_k))

def lift(d, yb, f_read, alpha_k=1.0):
    """Keo thang dung: xe treo duoi luc ke, day xe o do cao yb (px)."""
    # xe dung: banh duoi, than tren
    c = lambda col: A(col, alpha_k)
    for dx in (-22, 22): d.ellipse([XV + dx - 9, yb - 18, XV + dx + 9, yb], fill=c(NAVY))
    d.rectangle([XV - CL / 2, yb - 16 - CH, XV + CL / 2, yb - 16], fill=c(CART), outline=c(CART_D), width=3)
    y0 = yb - 16 - CH
    Qk = lambda s, h=0.0: (XV + h, y0 - s)
    d.line([Qk(0), Qk(ROPE - 13)], fill=c(NAVY), width=5)
    se = luc_ke(d, Qk, ROPE, ROPE + 16, ROPE + 16 + BODY, 2.5, f_read, nho=0.1, so=(0, 1, 2), hw=30, ben=1,
                alpha=alpha_k, co=40)
    d.line([Qk(se - 16), Qk(se + 8)], fill=c(NAVY), width=8)
    hx, hy = Qk(se + 34); dot(d, hx, hy, 26, c(SKIN), outline=c((190, 140, 105)))

def rig_card(d):
    card(d, (40, 265, 1040, 945), fill=WHITE, outline=LIGHT, w=3)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig_card(d); shelf(d)
    ramp(d, ang_of(0.80), ghost=True)
    Q, L = ramp(d, ang_of(0.40))
    cart(d, Q, CL / 2 + 8); meter_ramp(d, Q, CL / 2 + 8, None)
    card(d, (60, 290, 560, 480), fill=WHITE, outline=LIGHT, w=3)
    d.line([(90, 345), (170, 345)], fill=WOOD_D, width=10)
    text(d, (190, 345), "máng 0,40 m", 42, INK, anchor="lm")
    dash(d, (90, 425), (170, 425), NAVY, w=5)
    text(d, (190, 425), "máng 0,80 m", 42, INK, anchor="lm")
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 975 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 165), "Hai máng cùng cao 0,20 m.", 46, INK, alpha=a)
    ctext(d, y0 + 300, "Máng dài gấp đôi thì công kéo F·s thế nào?", 52, INK, maxw=860, alpha=a)
    text(d, (W / 2, y0 + 440), "Chọn đáp án ở khung câu hỏi", 38, NOTE, bold=False, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 505, 940, y0 + 519], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 505, 140 + 800 * (1 - p), y0 + 519], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (4 duong) ----------------
R0, RUN, ROT, PULL = 0.6, 2.8, 0.6, 1.6

def do_state(t):
    """-> (lan i, goc mang (None = thang dung), tien do keo p 0..1, F dang chi hoac None, so hang, do mo xe, do mo mang)."""
    if t < R0: return 0, None, 0.0, None, 0, 1.0, 0.0
    i = min(3, int((t - R0) // RUN)); u = t - R0 - i * RUN
    k_out = 1.0 - (appear(u, RUN - 0.25, 0.2) if i < 3 else 0.0)
    if i == 0:
        p = clamp((u - ROT) / PULL) if u >= ROT else 0.0
        f = ROWS[0][1] if u >= ROT else None
        return 0, None, p, f, (1 if p >= 1 else 0), k_out, 0.0
    a1 = ang_of(ROWS[i][0]); a0 = ang_of(ROWS[i - 1][0]) if i > 1 else a1
    if u < ROT:
        kin = appear(u, 0.0, 0.2)
        return i, lerp(a0, a1, ease(u / ROT)), 0.0, None, i, kin, (ease(u / ROT) if i == 1 else 1.0)
    p = clamp((u - ROT) / PULL)
    return i, a1, p, ROWS[i][1], i + (1 if p >= 1 else 0), k_out, 1.0

XS = (230, 560, 860)
def table(d, rows, hl=None, y=975):
    card(d, (40, y, 1040, y + 560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y + 58), "s (m)", 44, INK); text(d, (XS[1], y + 58), "F (N)", 44, INK)
    text(d, (XS[2], y + 58), "F·s (J)", 44, ORANGE)
    d.line([(70, y + 110), (1010, y + 110)], fill=LIGHT, width=3)
    for j in range(4):
        yy = y + 170 + j * 95
        if j == hl: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=20, fill=(255, 247, 237))
        s, f, a = ROWS[j]
        lab = "0,20 (đứng)" if j == 0 else vn(s)
        text(d, (XS[0], yy), lab, 44 if j == 0 else 48, MUTED if j >= rows else INK)
        if j < rows:
            text(d, (XS[1], yy), vn(f), 48, NAVY); text(d, (XS[2], yy), vn(a, 3), 48, ORANGE)

def info(d, s_txt, f_txt):
    card(d, (60, 290, 560, 480), fill=WHITE, outline=LIGHT, w=3)
    text(d, (90, 345), "kéo", 42, INK, anchor="lm"); text(d, (530, 345), s_txt, 44, NAVY, anchor="rm")
    text(d, (90, 425), "lực kế", 42, INK, anchor="lm"); text(d, (530, 425), f_txt, 46, RED, anchor="rm")

def s_do(img, d, t, sc):
    i, a, p, f, rows, k, kr = do_state(t)
    rig_card(d); shelf(d)
    fr = f if f is not None else 0.0
    if a is None:
        lift(d, lerp(YF, TY, p), fr, k)
        dash(d, (XV - 70, YF - 4), (XV - 70, TY + 4), A(NAVY, 0.6), w=4)
        info(d, "thẳng đứng", "– – –" if f is None else f"{vn(f)} N")
    else:
        Q, L = ramp(d, a, k=kr)
        q = lerp(CL / 2 + 8, L - CL / 2, p)
        cart(d, Q, q, k); meter_ramp(d, Q, q, fr, alpha_k=k)
        info(d, f"máng {vn(ROWS[i][0])} m", "– – –" if f is None else f"{vn(f)} N")
    table(d, rows, hl=i if t >= R0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: so hang = so lan keo xong; luc ke chi F dung lan dang keo; xe toi dinh <=> hang lan do da ghi."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, a, p, f, rows, k, kr = do_state(t)
        if t >= R0 and (p >= 1) != (rows == i + 1): bad.append(("dinh/hang", round(t, 2)))
        if f is not None and f != ROWS[i][1]: bad.append(("F", round(t, 2)))
        if (a is None) != (i == 0) and t >= R0: bad.append(("duong", round(t, 2)))
        t += 0.05
    if R0 + 3 * RUN + ROT + PULL + 0.6 > sc["T"]: bad.append("hang cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
BX0, BX1, BY0, BY1, VMAX = 200, 1000, 470, 960, 0.5
def yv(v): return BY1 - v / VMAX * (BY1 - BY0)

def chart(d, t0, t):
    card(d, (40, 360, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    d.line([(BX0, BY0 - 30), (BX0, BY1)], fill=INK, width=4); d.line([(BX0, BY1), (BX1, BY1)], fill=INK, width=4)
    for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5):
        d.line([(BX0 - 12, yv(v)), (BX0, yv(v))], fill=INK, width=3)
        text(d, (BX0 - 22, yv(v)), "0" if v == 0 else vn(v, 1), 40, INK, anchor="rm")
    text(d, (BX0 - 140, BY0 - 75), "F·s (J)", 40, NOTE, bold=False, anchor="lm")
    dash(d, (BX0, yv(PH)), (BX1, yv(PH)), DGREEN, w=4)
    for j, (s, f, a) in enumerate(ROWS):
        k = ease((t - t0 - 0.45 * j) / 0.6); cx = 320 + j * 200
        text(d, (cx, BY1 + 40), "đứng" if j == 0 else vn(s), 42, INK)
        if k <= 0: continue
        d.rectangle([cx - 55, yv(a * k), cx + 55, BY1], fill=ORANGE)
        if k > 0.97: text(d, (cx, yv(a) - 36), vn(a, 3), 40, NAVY)
    dash(d, (90, 1051), (150, 1051), DGREEN, w=4)
    text(d, (170, 1051), "P·h = 2,0 × 0,20 = 0,40 J", 40, DGREEN, anchor="lm")

def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.1, 0.4)
    lab = "ĐÁP ÁN · Gần như không đổi"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 338), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 304), lab, 42, WHITE, alpha=ka)
    chart(d, M[0] + 0.2, t)
    kr = appear(t, M[1] - 0.2, 0.45)
    if kr > 0:
        y0 = 1130 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pw = tw(d, "RÚT RA", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(GREEN, kr), r=32)
        text(d, (W / 2, y0 + 58), "RÚT RA", 40, WHITE, alpha=kr)
        rs(d, W / 2, y0 + 170, "Công trọng lực A_{P} = −P·h = −0,40 J", 46, INK, alpha=kr)
        text(d, (W / 2, y0 + 250), "ở cả bốn đường", 44, DGREEN, alpha=kr)
        text(d, (W / 2, y0 + 325), "Mặt nghiêng không lợi về công", 46, NAVY, alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
SXP, FYP = 500, 120                     # hinh dien tich: 500 px / m, 120 px / N
def s_bay(img, d, t, sc):
    M = sc["M"]
    kd = appear(t, 1.6, 0.4)          # hinh dien tich hien luc cau sai bi gach + ✗, khong truoc
    card(d, (40, 650, 1040, 1300), fill=A(WHITE, kd), outline=A(LIGHT, kd), w=3)
    x0 = 110; yb1 = 950
    s0, f0, a0 = ROWS[0]; s3, f3, a3 = ROWS[3]
    d.rectangle([x0, yb1 - f0 * FYP, x0 + s0 * SXP, yb1], fill=A((253, 186, 116), kd), outline=A(ORANGE, kd), width=4)
    text(d, (x0 + s0 * SXP + 30, yb1 - 170), "kéo thẳng", 42, INK, anchor="lm", alpha=kd)
    text(d, (x0 + s0 * SXP + 30, yb1 - 90), "2,00 N × 0,20 m = 0,400 J", 42, NAVY, anchor="lm", alpha=kd)
    yb2 = 1120
    d.rectangle([x0, yb2 - f3 * FYP, x0 + s3 * SXP, yb2], fill=A((253, 186, 116), kd), outline=A(ORANGE, kd), width=4)
    text(d, (x0 + s3 * SXP + 30, yb2 - 28), "máng 1,00 m", 42, INK, anchor="lm", alpha=kd)
    text(d, (x0, yb2 + 50), "0,46 N × 1,00 m = 0,460 J", 42, NAVY, anchor="lm", alpha=kd)
    text(d, (W / 2, 1245), "Lực nhỏ, đường dài: F·s không giảm", 44, DGREEN, alpha=appear(t, 2.6, 0.4))
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3); y = 300
    if a1 > 0:
        card(d, (40, y, 1040, y + 320), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Máng dài, lực nhỏ → đỡ tốn công”"
        ks = clamp((t - 1.4) / 0.4); f = F(48); lw = tw(d, q, f); yy = y + 200
        text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 + lw / 2 + 20, yy), "✗", 48, DRED, anchor="lm", alpha=a1 * ks)
    if k3 > 0:
        card(d, (40, y, 1040, y + 320), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 70), "Chưa nói được", 48, NAVY, alpha=k3)
        for j, s in enumerate(("• Phần F·s dôi ra đi đâu?", "• Kéo không đều thì sao?")):
            kk = k3 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (110, y + 170 + 95 * j), s, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot khong chua cong thuc giai -> THU NGHI xe 3,0 N, dinh 0,30 m, mang 0,75 m, mu = 0 (so moi) ; goi y la du kien doi, tre 2,6 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, "Công trọng lực tuỳ độ cao, không tuỳ đường đi", 50, GREEN, maxw=840, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 2.6, 0.5)
    card(d, (40, 600, 1040, 1040 + 340 * kh), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)   # co theo noi dung
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 850, "Xe 3,0 N, máng dài 0,75 m,\nđỉnh cao 0,30 m, không ma sát.\nKéo đều: lực kế chỉ?", 48, INK,
          maxw=920, alpha=appear(t, M[0] + 0.4, 0.5))
    if kh > 0:
        card(d, (110, 1060, 970, 1340), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1125), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1240), "Cả P lẫn h đều đã đổi", 46, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + R0 + i * RUN + ROT + PULL, "tap") for i in range(4)]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-nang-luong-cong-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Năng lượng. Công cơ học · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Lên cùng độ cao, nhiều đường", draw=s_hook, tail=0.6, caps=[
   ("Kéo đều xe 2,0 N.", 3.0),
   ("Dừng video, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Lần đầu kéo thẳng đứng.", 3.4),
   ("Rồi kéo song song máng.", 8.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Cột nào cũng sát vạch xanh.", 4.2),
   ("Đi lên: trọng lực sinh công âm.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("So diện tích hai hình.", 4.4),
   ("Hai câu còn bỏ ngỏ.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự tính.", 6.8)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("số:", _kiem_so() or "khớp kho"); print("đồng bộ:", _kiem_dong_bo() or "không lệch")
