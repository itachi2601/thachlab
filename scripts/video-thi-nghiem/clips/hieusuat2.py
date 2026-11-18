# Clip: tn-l10-hieu-suat-02 - Do hieu suat van nghieng o bon goc (lo 9, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-hieu-suat-02.json:
#   tham_so: mg = 4,0 N ; h = 20 cm ; mu = 0,25 ; alpha 10..60 do ; luc ke 0-5 N.
#   so_lieu_mau (alpha, s cm, F N, W_tp J, H %): 15 77,3 2,01 1,55 51,6 ; 25 47,3 2,58 1,22 65,6 ;
#   35 34,9 3,13 1,09 73,4 ; 45 28,3 3,52 1,00 80,0 ; W_ci = mgh = 0,80 J. Kiem: _kiem_so().
# Du doan (K10: chi cau hoi + hinh): cung nang xe len 20 cm, van thoai hon thi H the nao?
#   A. Cao hon ; B. Thap hon (DUNG) ; C. Nhu nhau, vi cung W_ci = 0,80 J.
# KHONG tra loi san cau sau hop ("Vi sao van thoai hao phi nhieu hon? Sai so tu dau?"): khong noi quang duong dai/ma sat
#   tang theo s, khong noi sai so luc ke; "vi sao" de o the "Chua noi duoc".
# Bay = hien_tuong_hay_sai[1] (lay W_tp chia W_ci -> H > 100 %). [0] (van thoai luc nho) khong dung: trung chu de clip nlcong2.
# Cau chot (ca tu suy, ghi trong ghi_chu kho): van 60 do (trong 10-60), luc ke 3,96 N, keo 23,1 cm
#   -> W_tp = 3,96 . 0,231 = 0,915 J ; H = 0,80/0,915 ~ 87 % (mo hinh 1/(1 + 0,25 cot60) = 87,4 %). Chua hien tren man.
# Khuon van nghieng dung chung voi clips/nlcong2.py (chep, khong import cheo): dinh van co dinh o mep be cao 20 cm,
#   chan van truot theo goc; 6 px/cm.
from engine import *

ROWS = [(15, 77.3, 2.01, 1.55, 51.6), (25, 47.3, 2.58, 1.22, 65.6), (35, 34.9, 3.13, 1.09, 73.4), (45, 28.3, 3.52, 1.00, 80.0)]
MG, HCM, WCI = 4.0, 20, 0.80
def vn(x, n=1): return f"{x:.{n}f}".replace(".", ",")

def _kiem_so():
    bad = []
    for a, s, f, w, h in ROWS:
        if abs(HCM / math.sin(math.radians(a)) - s) > 0.06: bad.append(("s", a))
        if abs(round(f * s / 100, 2) - w) > 0.006: bad.append(("W_tp", a))
        if abs(round(WCI / w * 100, 1) - h) > 0.06: bad.append(("H", a))
    if abs(MG * HCM / 100 - WCI) > 1e-9: bad.append("W_ci")
    return bad

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); BOARD = (222, 184, 135); CART = (196, 140, 84)
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

# ---------------- khuon van nghieng ----------------
PXC = 6.0; TX, TY = 660, 740; YF = TY + HCM * PXC          # dinh van (mep be), mat san
CL, CH = 76, 40                                          # xe: dai, cao (px)
ROPE, BODY = 24, 230

def ramp_q(alpha):
    """-> (Q, L): Q(q, h) = diem cach chan van q px doc van, cao h px vuong goc mat van (h > 0 phia tren)."""
    a = math.radians(alpha); ux, uy = math.cos(a), -math.sin(a); nx, ny = -math.sin(a), -math.cos(a)
    L = HCM / math.sin(a) * PXC; fx, fy = TX - L * ux, TY - L * uy
    return (lambda q, h=0.0: (fx + q * ux + h * nx, fy + q * uy + h * ny)), L

def shelf(d):
    d.line([(50, YF), (1030, YF)], fill=INK, width=4)
    d.rectangle([TX, TY, 1010, YF], fill=WOOD, outline=WOOD_D, width=3)
    d.line([(990, TY + 8), (990, YF - 8)], fill=WHITE, width=3)
    for yy in (TY + 8, YF - 8): d.line([(978, yy), (1002, yy)], fill=WHITE, width=3)
    text(d, (830, (TY + YF) / 2), "cao 20 cm", 42, WHITE)

def ramp(d, alpha, ghost=False):
    Q, L = ramp_q(alpha)
    if ghost:
        dash(d, Q(0), Q(L), NAVY, w=5); return Q, L
    d.polygon([Q(0), Q(L), (TX, YF)], fill=(241, 245, 249))
    d.polygon([Q(0, 0), Q(L, 0), Q(L, -12), Q(0, -12)], fill=BOARD, outline=WOOD_D)
    fx, fy = Q(0); r = 80
    d.arc([fx - r, fy - r, fx + r, fy + r], 360 - alpha, 360, fill=NAVY, width=4)
    return Q, L

def cart(d, Q, q, alpha_k=1.0):
    c = lambda col: A(col, alpha_k)
    for dq in (-22, 22):
        x, y = Q(q + dq, 9); d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=c(NAVY))
    d.polygon([Q(q - CL / 2, 16), Q(q + CL / 2, 16), Q(q + CL / 2, 16 + CH), Q(q - CL / 2, 16 + CH)], fill=c(CART), outline=c(WOOD_D))

def meter(d, Q, q, f_read, fmax=5.0, alpha_k=1.0):
    """Luc ke song song van, moc vao dau tren cua xe; f_read None: che thang do bang "?"."""
    q0 = q + CL / 2
    Qk = lambda s, h=0.0: Q(q0 + s, 36 + h)
    d.line([Qk(0), Qk(ROPE - 13)], fill=A(NAVY, alpha_k), width=5)
    se = luc_ke(d, Qk, ROPE, ROPE + 16, ROPE + 16 + BODY, fmax, f_read, nho=0.5, so=(0, 2, 4), hw=30, ben=1,
                alpha=alpha_k, co=40)
    d.line([Qk(se - 16), Qk(se + 8)], fill=A(NAVY, alpha_k), width=8)
    hx, hy = Qk(se + 34); dot(d, hx, hy, 26, A(SKIN, alpha_k), outline=A((190, 140, 105), alpha_k))

def rig_card(d):
    card(d, (40, 265, 1040, 945), fill=WHITE, outline=LIGHT, w=3)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig_card(d); shelf(d)
    ramp(d, 45, ghost=True)
    Q, L = ramp(d, 15)
    cart(d, Q, CL / 2 + 8); meter(d, Q, CL / 2 + 8, None)
    card(d, (60, 290, 560, 480), fill=WHITE, outline=LIGHT, w=3)
    d.line([(90, 345), (170, 345)], fill=WOOD_D, width=10)
    text(d, (190, 345), "ván thoải 15°", 42, INK, anchor="lm")
    dash(d, (90, 425), (170, 425), NAVY, w=5)
    text(d, (190, 425), "ván dốc 45°", 42, INK, anchor="lm")
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 975 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 165), "Cùng nâng xe lên cao 20 cm.", 46, INK, alpha=a)
    ctext(d, y0 + 300, "Ván thoải hơn thì hiệu suất H thế nào?", 52, INK, maxw=840, alpha=a)
    text(d, (W / 2, y0 + 440), "Chọn đáp án ở khung câu hỏi", 38, NOTE, bold=False, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 505, 940, y0 + 519], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 505, 140 + 800 * (1 - p), y0 + 519], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (4 goc) ----------------
R0, RUN, ROT, PULL = 0.8, 2.8, 0.6, 1.6

def do_state(t):
    """-> (lan i, goc dang ve, q tam xe (px), F dang chi hoac None, so hang da ghi, do mo xe)."""
    if t < R0:
        a = ROWS[0][0]; _, L = ramp_q(a); return 0, a, CL / 2 + 8, None, 0, 1.0
    i = min(3, int((t - R0) // RUN)); u = t - R0 - i * RUN
    a1 = ROWS[i][0]; a0 = ROWS[i - 1][0] if i > 0 else a1
    if u < ROT:
        a = lerp(a0, a1, ease(u / ROT)); q = CL / 2 + 8; f = None; rows = i
        k = appear(u, 0.0, 0.2) if i > 0 else 1.0
    else:
        a = a1; _, L = ramp_q(a); qa, qb = CL / 2 + 8, L - CL / 2
        p = clamp((u - ROT) / PULL); p = 1.0 if p > 1 - 1e-9 else p; q = qb if p >= 1 else lerp(qa, qb, p); f = ROWS[i][2]
        rows = i + (1 if p >= 1 else 0); k = 1.0 - (appear(u, RUN - 0.25, 0.2) if i < 3 else 0.0)
    return i, a, q, f, rows, k

XS = (150, 380, 620, 870)
def table(d, rows, hl=None, y=975):
    card(d, (40, y, 1040, y + 560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y + 58), "α", 46, INK)
    text(d, (XS[1], y + 58), "F (N)", 44, INK)
    text(d, (XS[2], y + 58), "s (cm)", 44, INK)
    rs(d, XS[3], y + 52, "W_{tp} (J)", 44, ORANGE)
    d.line([(70, y + 110), (1010, y + 110)], fill=LIGHT, width=3)
    for j in range(4):
        yy = y + 170 + j * 95
        if j == hl: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=20, fill=(255, 247, 237))
        text(d, (XS[0], yy), f"{ROWS[j][0]}°", 46, MUTED if j >= rows else INK)
        if j < rows:
            a, s, f, w, h = ROWS[j]
            text(d, (XS[1], yy), vn(f, 2), 48, NAVY); text(d, (XS[2], yy), vn(s), 48, BLUE)
            text(d, (XS[3], yy), vn(w, 2), 48, ORANGE)

def info(d, a_txt, f_txt):
    card(d, (60, 290, 560, 480), fill=WHITE, outline=LIGHT, w=3)
    text(d, (90, 345), "góc α", 42, INK, anchor="lm"); text(d, (530, 345), a_txt, 46, NAVY, anchor="rm")
    text(d, (90, 425), "lực kế", 42, INK, anchor="lm"); text(d, (530, 425), f_txt, 46, RED, anchor="rm")

def s_do(img, d, t, sc):
    i, a, q, f, rows, k = do_state(t)
    rig_card(d); shelf(d)
    Q, L = ramp(d, a)
    cart(d, Q, q, k); meter(d, Q, q, f if f is not None else 0.0, alpha_k=k)
    info(d, f"{ROWS[i][0]}°", "– – –" if f is None else f"{vn(f, 2)} N")
    table(d, rows, hl=i if t >= R0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: so hang = so lan keo xong; luc ke chi F dung hang dang keo; xe o dinh <=> hang lan do da ghi."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, a, q, f, rows, k = do_state(t)
        _, L = ramp_q(a); at_top = abs(q - (L - CL / 2)) < 1e-6
        if t >= R0 and at_top != (rows == i + 1): bad.append(("dinh/hang", round(t, 2)))
        if f is not None and f != ROWS[i][2]: bad.append(("F", round(t, 2)))
        if rows not in (i, i + 1): bad.append(("hang", round(t, 2)))
        t += 0.05
    if R0 + 3 * RUN + ROT + PULL + 0.6 > sc["T"]: bad.append("hang cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
BX0, BX1, BY0, BY1, VMAX = 200, 1000, 470, 960, 1.6
def yv(v): return BY1 - v / VMAX * (BY1 - BY0)

def chart(d, t0, t, alpha=1.0):
    card(d, (40, 360, 1040, 1100), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    d.line([(BX0, BY0 - 30), (BX0, BY1)], fill=A(INK, alpha), width=4); d.line([(BX0, BY1), (BX1, BY1)], fill=A(INK, alpha), width=4)
    for v in (0, 0.4, 0.8, 1.2, 1.6):
        d.line([(BX0 - 12, yv(v)), (BX0, yv(v))], fill=A(INK, alpha), width=3)
        text(d, (BX0 - 22, yv(v)), "0" if v == 0 else vn(v), 40, INK, anchor="rm", alpha=alpha)
    text(d, (BX0 - 140, BY0 - 75), "công kéo (J)", 40, NOTE, bold=False, anchor="lm", alpha=alpha)
    dash(d, (BX0, yv(WCI)), (BX1, yv(WCI)), A(DGREEN, alpha), w=4)
    for j, (a, s, f, w, h) in enumerate(ROWS):
        k = ease((t - t0 - 0.5 * j) / 0.6); cx = 320 + j * 200
        text(d, (cx, BY1 + 40), f"{a}°", 42, INK, alpha=alpha)
        if k <= 0: continue
        top = w * k
        d.rectangle([cx - 55, yv(min(top, WCI)), cx + 55, BY1], fill=A(GREEN, alpha))
        if top > WCI + 0.01: d.rectangle([cx - 55, yv(top), cx + 55, yv(WCI)], fill=A(ORANGE, alpha))
        if k > 0.97: text(d, (cx, yv(w) - 36), f"{vn(h)} %", 40, NAVY, alpha=alpha)
    d.rectangle([90, 1036, 124, 1066], fill=A(GREEN, alpha))
    rs(d, 140, 1046, "có ích W_{ci} = 0,80 J", 40, DGREEN, alpha=alpha, anchor="l")
    d.rectangle([700, 1036, 734, 1066], fill=A(ORANGE, alpha))
    text(d, (750, 1051), "hao phí", 40, ORANGE, anchor="lm", alpha=alpha)

def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, M[0] + 2.4, 0.4)   # sau khi cot 45 do moc xong (t0 + 0,5*3 + 0,6)
    lab = "ĐÁP ÁN · H thấp hơn"
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
        rs(d, W / 2, y0 + 175, "H = W_{ci} ÷ W_{tp} < 100 %", 52, INK, alpha=kr)
        text(d, (W / 2, y0 + 300), "vì có ma sát giữa xe và ván", 46, DGREEN, alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    # thanh so sanh: co ich nam TRONG toan phan (goc 15 do)
    kt = appear(t, 2.6, 0.4)          # hien cung the xanh, sau khi cong thuc sai bi gach
    if kt > 0:
        card(d, (40, 1180, 1040, 1520), fill=A(WHITE, kt), outline=A(LIGHT, kt), w=3)
        x0, x1 = 90, 990; xc = x0 + (x1 - x0) * WCI / ROWS[0][3]
        rs(d, x0, 1240, "góc 15°: W_{tp} = 1,55 J", 42, INK, anchor="l", alpha=kt)
        d.rectangle([x0, 1300, x1, 1400], fill=A((255, 237, 213), kt), outline=A(ORANGE, kt), width=4)
        d.rectangle([x0, 1300, xc, 1400], fill=A(GREEN, kt))
        rs(d, (x0 + xc) / 2, 1344, "W_{ci} 0,80 J", 42, WHITE, alpha=kt)
        text(d, (W / 2, 1460), "có ích nằm trong toàn phần", 42, DGREEN, alpha=kt)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3); y = 300
    if a1 > 0:
        card(d, (40, y, 1040, y + 800), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 1.4) / 0.4); yy = y + 200
        lw = rs(d, W / 2, yy, "“H = W_{tp} ÷ W_{ci}”", 56, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 4), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 4)], fill=A(DRED, 0.85 * a1), width=6)
        kb = appear(t, 1.6, 0.4) * a1
        text(d, (W / 2, y + 340), "1,55 ÷ 0,80 > 1  →  H > 100 %  ✗", 46, DRED, alpha=kb)
        kg = appear(t, 2.6, 0.4) * a1
        card(d, (100, y + 450, 980, y + 760), fill=A((236, 253, 243), kg), r=24)
        rs(d, W / 2, y + 540, "H = W_{ci} ÷ W_{tp}", 52, DGREEN, alpha=kg)
        text(d, (W / 2, y + 670), "= 0,80 ÷ 1,55 = 51,6 %  ✓", 50, DGREEN, alpha=kg)
    if k3 > 0:
        card(d, (40, y, 1040, y + 720), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 90), "Chưa nói được", 50, NAVY, alpha=k3)
        for j, s in enumerate(("• Vì sao ván thoải", "  hao phí nhiều hơn?", "• Bôi trơn ván thì", "  H đổi ra sao?")):
            kk = k3 * appear(t, M[1] + 0.3 + 0.6 * (j // 2), 0.4)
            text(d, (110, y + 240 + 110 * j + 60 * (j // 2)), s, 48, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot khong chua cong thuc giai -> THU NGHI ca 60 do (so moi) ; goi y la du kien, tre 2,6 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, "Máy nào cũng có hao phí: H < 100 %", 50, GREEN, maxw=840, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 2.6, 0.5)
    card(d, (40, 600, 1040, 1040 + 340 * kh), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)   # co theo noi dung, noi khi co goi y
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 850, "Ván nghiêng 60°: lực kế chỉ 3,96 N,\nkéo xe đi 23,1 cm.\nHiệu suất H bằng bao nhiêu?", 48, INK,
          maxw=900, alpha=appear(t, M[0] + 0.4, 0.5))
    if kh > 0:
        card(d, (110, 1060, 970, 1340), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1125), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1240), "Xe 4,0 N, vẫn nâng cao 20 cm", 46, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + R0 + i * RUN + ROT + PULL, "tap") for i in range(4)]
            + [(da["t0"] + da["M"][0] + 2.4, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-hieu-suat-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Hiệu suất · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ván nghiêng ở bốn góc", draw=s_hook, tail=0.6, caps=[
   ("Kéo đều xe lên 20 cm.", 3.2),
   ("Dừng video, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Lực kế luôn song song mặt ván.", 6.2),
   ("Đổi góc, vẫn nâng 20 cm.", 5.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Mỗi cột: công kéo ở một góc.", 4.2),
   ("Phần cam không nâng được xe.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Chia ngược hai công.", 4.2),
   ("Hai câu còn bỏ ngỏ.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự tính.", 6.8)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("số:", _kiem_so() or "khớp kho"); print("đồng bộ:", _kiem_dong_bo() or "không lệch")
