# Clip: tn-l10-nang-luong-cong-02 - Dua xe len cung do cao bang nhieu duong (ban 2 theo cong moi, 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-nang-luong-cong-02.json:
#   tham_so: P = 2,0 N ; h = 0,20 m ; luc ke 0-2,5 N do chia 0,02 N.
#   so_lieu_mau (s m, F N, A = F.s J): 0,20 (thang dung) 2,00 0,400 ; 0,40 1,06 0,424 ; 0,80 0,56 0,448 ; 1,00 0,46 0,460.
# Du doan (K10, diem_nhan kho): mang dai gap doi (0,40 -> 0,80 m), cung cao 0,20 m: cong keo F.s? -> gan nhu khong doi.
#   KHONG tra loi san Bam xem cua bai ("lan nao lech nhieu nhat, phan doi ra di dau"): khong noi +15 %, khong noi ma sat lan.
# Bay (27/11, theo kiem v1): "mang dai: cong trong luc lon hon" -> A_P = -P.h = -0,40 J moi mang (muc 3 cua bai).
#   Khong dung hien_tuong_hay_sai[0] (trung cap Du doan) va [1] (trung Tu kiem tra Cau 5, lech ky hieu alpha).
# Cau chot (ghi_chu kho, chua hien): xe 3,0 N, dinh 0,30 m, mang tron 0,75 m, keo deu -> F.s = P.h = 0,90 J -> F = 1,20 N.
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
    sub = max(56, int(size * 0.72)); segs = []
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

def shelf(d, lab="cao 0,20 m"):
    d.line([(50, YF), (1030, YF)], fill=INK, width=4)
    d.rectangle([TX, TY, 1010, YF], fill=WOOD, outline=WOOD_D, width=3)
    d.line([(990, TY + 8), (990, YF - 8)], fill=WHITE, width=3)
    for yy in (TY + 8, YF - 8): d.line([(978, yy), (1002, yy)], fill=WHITE, width=3)
    text(d, (835, (TY + YF) / 2), lab, 56, WHITE)

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
                alpha=alpha_k, co=56)
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
                alpha=alpha_k, co=56)
    d.line([Qk(se - 16), Qk(se + 8)], fill=c(NAVY), width=8)
    hx, hy = Qk(se + 34); dot(d, hx, hy, 26, c(SKIN), outline=c((190, 140, 105)))

def rig_card(d):
    card(d, (40, 265, 1040, 945), fill=WHITE, outline=LIGHT, w=3)

EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); w = 780 / n
    for i in range(n):
        x = 150 + i * w
        if i < on: card(d, (x, y, x + w - 20, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w - 20, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def arrow(d, p, q, col, w=7, hl=26):
    d.line([p, q], fill=col, width=w); ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for s in (1, -1):
        a2 = ang + math.pi - s * math.radians(30)
        d.line([q, (q[0] + hl * math.cos(a2), q[1] + hl * math.sin(a2))], fill=col, width=w)

# ---------------- canh 1: Du doan ----------------
def legend(d, l1, l2):
    card(d, (60, 290, 600, 480), fill=WHITE, outline=LIGHT, w=3)
    d.line([(90, 345), (170, 345)], fill=WOOD_D, width=10)
    text(d, (190, 345), l1, 56, INK, anchor="lm")
    dash(d, (90, 425), (170, 425), NAVY, w=5)
    text(d, (190, 425), l2, 56, INK, anchor="lm")

def s_hook(img, d, t, sc):
    M = sc["M"]
    rig_card(d); shelf(d)
    ramp(d, ang_of(0.80), ghost=True)
    Q, L = ramp(d, ang_of(0.40))
    qa, qb = CL / 2 + 8, L - CL / 2; q = lerp(qa, qb, clamp((t - 0.6) / 2.4))
    cart(d, Q, q); meter_ramp(d, Q, q, None)
    legend(d, "máng 0,40 m", "máng 0,80 m")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 990 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 175), "Cùng cao 0,20 m, máng dài gấp đôi.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Công kéo F·s thế nào?", 60, PURPLE, alpha=a)
    seg_bar(d, y0 + 370, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (4 duong) ----------------
R0, RUN, ROT, PULL = 0.6, 2.7, 0.6, 1.5

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
    card(d, (40, y, 1040, y + 540), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y + 58), "s (m)", 56, INK); text(d, (XS[1], y + 58), "F (N)", 56, INK)
    text(d, (XS[2], y + 58), "F·s (J)", 56, ORANGE)
    d.line([(70, y + 110), (1010, y + 110)], fill=LIGHT, width=3)
    for j in range(4):
        yy = y + 170 + j * 92
        if j == hl: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=20, fill=(255, 247, 237))
        s, f, a = ROWS[j]
        lab = "0,20 (đứng)" if j == 0 else vn(s)
        text(d, (XS[0], yy), lab, 58, GRAY if j >= rows else INK)
        if j < rows:
            text(d, (XS[1], yy), vn(f), 58, NAVY); text(d, (XS[2], yy), vn(a, 3), 58, ORANGE)

def info(d, s_txt, f_txt):
    card(d, (60, 290, 600, 480), fill=WHITE, outline=LIGHT, w=3)
    text(d, (90, 345), "kéo", 56, INK, anchor="lm"); text(d, (575, 345), s_txt, 56, NAVY, anchor="rm")
    text(d, (90, 425), "lực kế", 56, INK, anchor="lm"); text(d, (575, 425), f_txt, 56, RED, anchor="rm")

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
BX0, BX1, BY0, BY1, VMAX = 200, 1000, 520, 1000, 0.5
def yv(v): return BY1 - v / VMAX * (BY1 - BY0)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 280, 1040, 1150), fill=WHITE, outline=LIGHT, w=3)
    d.line([(BX0, BY0 - 30), (BX0, BY1)], fill=INK, width=4); d.line([(BX0, BY1), (BX1, BY1)], fill=INK, width=4)
    for v in (0.2, 0.4):
        d.line([(BX0 - 12, yv(v)), (BX0, yv(v))], fill=INK, width=3)
        text(d, (BX0 - 20, yv(v)), vn(v, 1), 56, INK, anchor="rm")
    text(d, (70, 340), "F·s (J)", 56, INK, anchor="lm")
    dash(d, (BX0, yv(PH)), (BX1, yv(PH)), DGREEN, w=5)
    text(d, (BX1, 340), "P·h = 2,0 · 0,20 = 0,40 J", 56, DGREEN, anchor="rm")
    for j, (s, f, a) in enumerate(ROWS):
        k = ease((t - 0.3) / 0.7); cx = 330 + j * 200
        text(d, (cx, BY1 + 50), "đứng" if j == 0 else vn(s), 56, INK)
        pu = 0.85 + 0.15 * math.sin(5.0 * t + j) if t > 1.2 else 1.0
        d.rectangle([cx - 60, yv(a * k), cx + 60, BY1], fill=mix(WHITE, ORANGE, pu))
    text(d, (115, BY1 + 50), "s (m)", 56, INK)
    ka = appear(t, M[0] + 2.4, 0.4)
    if ka > 0:
        card(d, (60, 1180, 1020, 1300), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1240), "Đáp án: gần như không đổi", 58, GREEN, alpha=ka)
    kr = appear(t, M[1] + 0.3, 0.4)
    if kr > 0:
        card(d, (60, 1340, 1020, 1580), fill=A(WHITE, kr), outline=A(NAVY, kr), r=28, w=5)
        text(d, (W / 2, 1410), "Mặt nghiêng lợi về lực,", 58, NAVY, alpha=kr)
        text(d, (W / 2, 1505), "không lợi về công", 58, NAVY, alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    rig_card(d); shelf(d, "h = 0,20 m")
    Q, L = ramp(d, ang_of(1.00))
    Qg, Lg = ramp_q(ang_of(0.40)); dash(d, Qg(0), Qg(Lg), NAVY, w=8)
    q = L * 0.72; cart(d, Q, q)
    cx, cy = Q(q, 36)
    arrow(d, (cx, cy), (cx, cy + 95), RED)
    text(d, (cx - 25, cy + 20), "P = 2,0 N", 56, RED, anchor="rm")
    legend(d, "máng 1,00 m", "máng 0,40 m")
    ks = clamp((t - mk) / 0.4)
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = 1 - k3; y = 1000
    if a1 > 0:
        card(d, (40, y, 1040, y + 430), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", RED, a1)
        yy = y + 195; q_ = "“Máng dài: công trọng lực lớn hơn”"
        lw = tw(d, q_, F(56))
        text(d, (W / 2, yy), q_, 56, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 4), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 4)], fill=A(RED, 0.85 * a1), width=6)
        k2 = appear(t, mk + 0.2, 0.45)
        if k2 > 0: rs(d, W / 2, y + 330, "Mọi máng: A_{P} = −P·h = −0,40 J", 60, DORANGE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 340), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 230), "Chưa thử kéo không đều", 62, INK, alpha=k3)

# ---------------- canh 5: thu nghi (cau chot o khung: 1,20 N) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 300, 1040, 1150), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 380, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 540), "Máng trơn dài 0,75 m,", 62, INK, alpha=k)
    text(d, (W / 2, 630), "đỉnh cao 0,30 m, xe 3,0 N.", 62, INK, alpha=k)
    text(d, (W / 2, 770), "Kéo đều: lực kế chỉ?", 62, DORANGE, alpha=k)
    seg_bar(d, 940, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.05, "ding")]
            + [(do["t0"] + R0 + i * RUN + ROT + PULL, "tap") for i in range(4)]
            + [(da["t0"] + da["M"][0] + 2.4, "ding"), (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
               (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-nang-luong-cong-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Năng lượng. Công cơ học · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Lên cùng độ cao, nhiều đường", draw=s_hook, tail=0.3, caps=[
   ("Kéo đều xe 2,0 N lên máng.", 3.4),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Bốn đường lên", draw=s_do, tail=0.4, caps=[
   ("Lần đầu kéo thẳng đứng.", 3.4),
   ("Rồi kéo song song máng.", 8.0)]),
 dict(key="dapan", title="So công kéo", draw=s_dapan, tail=0.4, caps=[
   ("Cột nào cũng sát vạch xanh.", 4.6),
   ("Lợi về lực, đổi bằng đường đi.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 3.2),
   ("Sai: chỉ tuỳ độ cao h.", 3.4),
   ("Giới hạn của lần đo.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 6.0)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("số:", _kiem_so() or "khớp kho"); print("đồng bộ:", _kiem_dong_bo() or "không lệch")
