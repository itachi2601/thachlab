# Clip: tn-l10-thuchanhthl-01 - Ba luc ke keo nut O: so F ve (hinh binh hanh) voi luc do duoc (ban 1, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-thuchanhthl-01.json:
#   lan 1: F1 1,6 ; F2 2,1 ; alpha 80 ; F3 2,9 N | lan 2: 2,0 ; 2,0 ; 60 ; 3,5 N (cheo 6,9 cm -> F ve 3,45 N, delta 0,05)
#   lan 3: 1,4 ; 1,6 ; 110 ; F3 doc 2,1 N gom so 0 lech 0,3 N (luc ke 3 khac chua chinh) -> 1,8 N, delta 0,05.
#   ti le xich 1 cm ung 0,5 N ; Delta = 0,3 N. Huong cac day: tinh tu mo hinh (nut O can bang, F3 thang dung).
# Du doan (K10: chi cau hoi + hinh): lan 2, F1 = F2 = 2,0 N, goc 60 do: luc ke 3 chi khoang?
#   A. khoang 4,0 N (cong hai so chi) [hien_tuong_hay_sai[0]] ; B. khoang 3,5 N (DUNG) ; C. khoang 2,0 N (bang moi luc).
# Bay = hien_tuong_hay_sai[2]: lan 3 delta = 0,35 N > Delta roi ket luan quy tac sai -> luc ke 3 chua chinh so 0 (0,3 N).
# Cau chot (ca tu suy, ghi trong ghi_chu kho): F1 = F2 = 1,5 N, hai day vuong goc -> F = 2,12 N, luc ke 3 chi khoang 2,1 N.
# Khong tra loi san cau trong muc: Cau 1 (1,2 & 1,6 N vuong goc -> 2,0 N): khong co so nay ; Cau 2 (1,0 & 1,0 vuong goc,
#   F3 1,9 -> delta 0,5 > Delta): khong tinh ca nay, khong neu ket luan "chua hop" cho so cua cau.
# Hinh binh hanh (canh Ket qua) ve dung ti le: 1 cm giay = 45 px, canh 2,0 N = 4,0 cm, goc 60 do; assert do dai cheo.
# Bo cuc (khac tonghopluc2 = van nghieng): bang giay dung, nut O o giua, hai luc ke xien len, luc ke 3 treo vat; bang 3 lan.
from engine import *

DRED = (185, 28, 28); NOTE = (60, 64, 84)
BRASS = (196, 150, 70); BRASS_D = (140, 100, 40); PAPER = (250, 250, 245)
LAN = [(1.6, 2.1, 80, 2.9), (2.0, 2.0, 60, 3.5), (1.4, 1.6, 110, 2.1)]       # so_lieu_mau (F1, F2, alpha, F3 doc)
XICH, DELTA = 0.5, 0.3
# alpha ve bang Times New Roman Bold Italic: alpha cua SF de doc nham thanh "a" (nhat ky 30/10).
_GK = "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf"; _gc = {}
def FG(size):
    size = int(size)
    if size not in _gc: _gc[size] = ImageFont.truetype(_GK, size)
    return _gc[size]
def atext(d, xy, s, size, color=INK, alpha=1.0):
    runs = [(p, FG(size * 1.12) if p == "α" else F(size)) for p in re.split(r"(α)", s) if p]
    x = xy[0] - sum(tw(d, p, f) for p, f in runs) / 2
    for p, f in runs: dtext(d, (x, xy[1]), p, f, color, alpha, "lm"); x += tw(d, p, f)
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def fmodel(f1, f2, a): return math.sqrt(f1 * f1 + f2 * f2 + 2 * f1 * f2 * math.cos(math.radians(a)))
def betas(f1, f2, a):
    b1 = math.degrees(math.atan2(f2 * math.sin(math.radians(a)), f1 + f2 * math.cos(math.radians(a))))
    return b1, a - b1

def _kiem_so():
    assert abs(round(fmodel(2.0, 2.0, 60) / XICH, 1) - 6.9) < 1e-9 and abs(6.9 * XICH - 3.45) < 1e-9
    assert abs(round(fmodel(1.6, 2.1, 80) / XICH, 1) - 5.7) < 1e-9
    assert abs(round(fmodel(1.4, 1.6, 110) / XICH, 1) - 3.5) < 1e-9
    assert abs(abs(3.45 - 3.5) - 0.05) < 1e-9 and abs((2.1 - 0.3) - 1.8) < 1e-9 and abs(abs(1.75 - 2.1) - 0.35) < 1e-9
    assert abs(fmodel(1.5, 1.5, 90) - 2.121) < 1e-3                                  # ca chot
    for f1, f2, a, _ in LAN:                                                         # day can bang: thanh phan ngang triet tieu
        b1, b2 = betas(f1, f2, a); assert abs(f1 * math.sin(math.radians(b1)) - f2 * math.sin(math.radians(b2))) < 1e-9
_kiem_so()

OX, OY = 540, 720
def ux(beta, side):   # don vi theo day: side -1 = trai, +1 = phai ; beta tinh tu phuong thang dung huong len
    r = math.radians(beta); return (side * math.sin(r), -math.cos(r))

def meter_on(d, beta, side, f, alpha=1.0):
    u = ux(beta, side); nv = (u[1], -u[0])
    Q = lambda s, h: (OX + u[0] * s + nv[0] * h, OY + u[1] * s + nv[1] * h)
    d.line([(OX, OY), Q(60, 0)], fill=A(NAVY, alpha), width=4)
    se = luc_ke(d, Q, 70, 90, 420, 5.0, f, nho=0.2, so=(0, 1, 2, 3, 4, 5), hw=38, ben=1 if side < 0 else -1, alpha=alpha, co=40)
    p = Q(se + 10, 0); dot(d, p[0], p[1], 15, A((90, 95, 110), alpha), A(WHITE, alpha))       # chot tren gia

def meter3(d, f, weight=True, alpha=1.0, y_ring=None):
    """Luc ke 3 thang dung duoi nut O: vong treo o tren (noi day len O), moc o duoi treo vat."""
    yb = (y_ring or OY + 50) + 416
    Q = lambda s, h: (OX + h, yb - s)
    if y_ring is None: d.line([(OX, OY), (OX, OY + 50)], fill=A(NAVY, alpha), width=4)
    luc_ke(d, Q, 0, 20, 400, 5.0, f, nho=0.2, so=(0, 1, 2, 3, 4, 5), hw=38, ben=1, alpha=alpha, co=40)
    if weight:
        d.line([(OX, yb + 12), (OX, yb + 30)], fill=A(NAVY, alpha), width=4)
        d.rounded_rectangle([OX - 55, yb + 30, OX + 55, yb + 120], radius=12, fill=A(BRASS, alpha), outline=A(BRASS_D, alpha), width=3)

def board(d):
    card(d, (70, 260, 1010, 1010), fill=PAPER, outline=LIGHT, r=18, w=3)

def chip(d, box, s, col, a=1.0):
    card(d, box, fill=A(WHITE, a), outline=A(col, a), r=24, w=4)
    text(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), s, 44, col, alpha=a)

def rig(d, b1, b2, f1, f2, f3, al, show, hide3=False, tag=None):
    board(d)
    meter_on(d, b1, -1, f1); meter_on(d, b2, 1, f2); meter3(d, None if hide3 else f3)
    dot(d, OX, OY, 14, NAVY, WHITE)
    text(d, (OX + 70, OY + 10), "O", 44, NAVY)
    r = 90; a0 = -90 - b1; a1 = -90 + b2                                            # cung goc alpha giua hai day
    d.arc([OX - r, OY - r, OX + r, OY + r], a0, a1, fill=ORANGE, width=5)
    s = "α = ···" if not show else f"α = {al:g}°"
    atext(d, (OX, OY - 215), s, 44, ORANGE)
    v = lambda x: "···" if not show else vn(x) + " N"
    chip(d, (80, 800, 340, 870), "F1 = " + v(f1), BLUE)
    chip(d, (740, 800, 1000, 870), "F2 = " + v(f2), BLUE)
    chip(d, (680, 1060, 960, 1130), "F3 = " + ("?" if hide3 else v(f3)), RED)
    if tag: text(d, (780, 1180), tag, 40, NOTE)

def table(d, n, y=1330, hl=-1):
    card(d, (40, y, 1040, y + 330), fill=WHITE, outline=NAVY, w=4)
    xs = (130, 300, 480, 680, 900)
    for x, h in zip(xs, ("Lần", "F1 (N)", "F2 (N)", "α", "F3 (N)")): atext(d, (x, y + 48), h, 42, INK)
    d.line([(60, y + 86), (1020, y + 86)], fill=LIGHT, width=4)
    for i in range(n):
        f1, f2, a, f3 = LAN[i]; yy = y + 132 + i * 72
        if i == hl: d.rounded_rectangle([55, yy - 32, 1025, yy + 32], radius=14, fill=(255, 237, 213))
        for x, s, col in zip(xs, (str(i + 1), vn(f1), vn(f2), f"{a}°", vn(f3)), (INK, BLUE, BLUE, ORANGE, RED)):
            text(d, (x, yy), s, 46, col)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; f1, f2, a, f3 = LAN[1]; b1, b2 = betas(f1, f2, a)
    rig(d, b1, b2, f1, f2, f3, a, True, hide3=True)
    k = appear(t, M[1] - 0.3, 0.5)
    if k <= 0: return
    y0 = 1230 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 440), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 54), "DỰ ĐOÁN", 40, WHITE, alpha=k)
    text(d, (W / 2, y0 + 150), "F1 = F2 = 2,0 N, góc 60°.", 46, INK, alpha=k)
    text(d, (W / 2, y0 + 225), "Lực kế 3 chỉ khoảng bao nhiêu?", 50, INK, alpha=k)
    text(d, (W / 2, y0 + 310), "Chọn đáp án ở khung câu hỏi", 40, NOTE, alpha=k)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 380, 940, y0 + 394], radius=7, fill=A(LIGHT, k))
        d.rounded_rectangle([140, y0 + 380, 140 + 800 * (1 - p), y0 + 394], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: Tien hanh ----------------
TS = [0.5, 2.9, 5.3]              # bat dau lan 1, 2, 3: doi chot/vat (MOVE), cho O dung yen roi doc so
MOVE, SETTLE = 1.0, 0.4

def do_state(t):
    """-> (b1, b2, f1, f2, f3 kim, so hien?, so hang bang)."""
    k = -1
    for i, s in enumerate(TS):
        if t >= s: k = i
    if k < 0:
        b1, b2 = betas(*LAN[1][:3]); return b1, b2, 0.0, 0.0, 0.0, False, 0
    x = t - TS[k]; cur = LAN[k]; prev = LAN[k - 1] if k > 0 else (0.0, 0.0, 60, 0.0)
    cb = betas(*cur[:3]); pb = betas(*prev[:3]) if k > 0 else betas(*LAN[1][:3])
    if x < MOVE + SETTLE:
        e = ease(x / MOVE)
        return (lerp(pb[0], cb[0], e), lerp(pb[1], cb[1], e), lerp(prev[0], cur[0], e), lerp(prev[1], cur[1], e),
                lerp(prev[3], cur[3], e), False, k)
    return cb[0], cb[1], cur[0], cur[1], cur[3], True, k + 1

def s_do(img, d, t, sc):
    b1, b2, f1, f2, f3, show, n = do_state(t)
    k = max(0, min(2, n - 1 if show else n))
    rig(d, b1, b2, f1, f2, f3, LAN[k][2], show, tag=None)
    table(d, n, hl=n - 1 if show else -1)

def _kiem_dong_bo():
    """Moi 0,05 s: khi so hien thi kim = so tren chip = hang cuoi bang, goc day dung mo hinh; khi chua on dinh thi an so."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        b1, b2, f1, f2, f3, show, n = do_state(t)
        if show:
            row = LAN[n - 1]; bb = betas(*row[:3])
            if (f1, f2, f3) != (row[0], row[1], row[3]) or abs(b1 - bb[0]) > 1e-9 or abs(b2 - bb[1]) > 1e-9: bad.append(round(t, 2))
        t += 0.05
    if TS[-1] + MOVE + SETTLE + 0.5 > sc["T"]: bad.append("lan cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + hinh binh hanh lan 2 (dung ti le) ----------------
PXCM = 45                          # px moi cm tren giay
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.4)
    lab = "ĐÁP ÁN · Khoảng 3,5 N"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 358), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 324), lab, 42, WHITE, alpha=ka)
    card(d, (60, 390, 1020, 1110), fill=PAPER, outline=LIGHT, r=18, w=3)
    text(d, (1000, 430), "1 cm ứng 0,5 N", 40, NOTE, anchor="rm")
    f1, f2, a, f3 = LAN[1]; b1, b2 = betas(f1, f2, a); o = (540, 760)
    u1, u2 = ux(b1, -1), ux(b2, 1)
    L1, L2 = f1 / XICH * PXCM, f2 / XICH * PXCM
    p1 = (o[0] + u1[0] * L1, o[1] + u1[1] * L1); p2 = (o[0] + u2[0] * L2, o[1] + u2[1] * L2)
    pf = (p1[0] + p2[0] - o[0], p1[1] + p2[1] - o[1])
    diag_cm = math.dist(o, pf) / PXCM
    assert abs(diag_cm - fmodel(f1, f2, a) / XICH) < 1e-6 and abs(round(diag_cm, 1) - 6.9) < 1e-9
    k1 = appear(t, 0.4, 0.4); k2 = appear(t, M[0] + 0.6, 0.5); k3 = appear(t, M[1] + 0.1, 0.5)
    for q, p in ((p1, pf), (p2, pf)):                                               # canh song song (net dut)
        for j in range(12):
            s0, s1 = j / 12, (j + 0.55) / 12
            d.line([(lerp(q[0], p[0], s0), lerp(q[1], p[1], s0)), (lerp(q[0], p[0], s1), lerp(q[1], p[1], s1))], fill=A(GRAY, k2), width=4)
    arrow(d, o, p1, A(BLUE, k1), w=7, head=24); arrow(d, o, p2, A(BLUE, k1), w=7, head=24)
    text(d, (p1[0] - 60, p1[1] + 10), "F1 = 2,0 N", 42, BLUE, anchor="rm", alpha=k1)              # nhan ngoai mui ten, lech do cao
    text(d, (p2[0] + 60, p2[1] + 70), "F2 = 2,0 N", 42, BLUE, anchor="lm", alpha=k1)
    text(d, (o[0] - 50, o[1] + 40), "O", 44, NAVY, alpha=k1)
    if k2 > 0:
        arrow(d, o, pf, A(GREEN, k2), w=9, head=28)
        text(d, (pf[0] + 150, pf[1] + 40), "F vẽ", 44, GREEN, alpha=k2)
        text(d, (pf[0] + 150, pf[1] + 92), "lên nút O", 40, GREEN, alpha=k2)
    if k3 > 0:                                                                       # F3 do duoc: nguoc chieu, dung ti le 3,5 N = 7,0 cm
        L3 = f3 / XICH * PXCM; p3 = (o[0], o[1] + L3)
        arrow(d, o, p3, A(RED, k3), w=9, head=28)
        text(d, (o[0] + 160, o[1] + L3 * 0.55), "F3 = 3,5 N", 42, RED, alpha=k3)
        text(d, (o[0] + 160, o[1] + L3 * 0.55 + 50), "lực kế 3 kéo O", 40, RED, alpha=k3)
    dot(d, o[0], o[1], 10, NAVY, WHITE)
    kc = appear(t, M[0] + 1.2, 0.45)
    card(d, (40, 1140, 1040, 1250), fill=A(WHITE, kc), outline=A(GREEN, kc), r=24, w=4)
    text(d, (W / 2, 1195), "chéo 6,9 cm → F vẽ = 3,45 N", 46, GREEN, alpha=kc)
    kd = appear(t, M[1] + 0.8, 0.45)
    card(d, (40, 1275, 1040, 1385), fill=A(WHITE, kd), outline=A(NAVY, kd), r=24, w=4)
    text(d, (W / 2, 1330), "δ = |3,45 − 3,5| = 0,05 N ≤ Δ = 0,3 N", 44, NAVY, alpha=kd)

# ---------------- canh 4: Bay (lan 3) + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    kz = appear(t, 2.8, 0.45)
    board(d)
    if kz <= 0:
        f1, f2, a, f3 = LAN[2]; b1, b2 = betas(f1, f2, a)
        meter_on(d, b1, -1, f1); meter_on(d, b2, 1, f2); meter3(d, f3); dot(d, OX, OY, 14, NAVY, WHITE)
        chip(d, (680, 1060, 960, 1130), "F3 = 2,1 N", RED)
        text(d, (W / 2, 330), "Lần 3: F vẽ = 1,75 N", 46, GREEN)
    else:                                                                            # luc ke 3 thao ra, treo thang dung, chua moc vat
        meter3(d, 0.3, weight=False, alpha=kz, y_ring=420)
        text(d, (W / 2, 330), "Lực kế 3, chưa móc vật:", 46, NAVY, alpha=kz)
        chip(d, (680, 700, 960, 770), "chỉ 0,3 N", DRED, a=kz)
    y = 1200                                                                         # duoi than luc ke 3 (1186), tren phu de (1597)
    if a1 > 0:
        card(d, (40, y, 1040, y + 390), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 2.3) / 0.4)
        for j, q in enumerate(("“δ = 0,35 N > Δ:", "bỏ lần 3, nghi quy tắc”")):
            yy = y + 150 + 64 * j; lw = tw(d, q, F(48))
            text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        kk = a1 * appear(t, 3.2, 0.4)
        text(d, (W / 2, y + 280), "2,1 − 0,3 = 1,8 N", 48, GREEN, alpha=kk)
        text(d, (W / 2, y + 345), "δ = 0,05 N ≤ Δ", 48, GREEN, alpha=kk)
    if k3 > 0:
        card(d, (40, y, 1040, y + 390), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        for j, s in enumerate(("• Sai số vẽ chưa tính vào Δ", "• Hai lực song song?")):
            kk = k3 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (100, y + 190 + 110 * j), s, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot khong chua quy tac/cong thuc giai -> THU NGHI: F1 = F2 = 1,5 N vuong goc (so moi); goi y tre >= 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 420, "F vẽ khớp lực đo được, trong sai số", 50, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 870, "F1 = F2 = 1,5 N,\nhai dây vuông góc.\nLực kế 3 chỉ khoảng bao nhiêu?", 48, INK,
          maxw=920, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1100, 970, 1360), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1160, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1270, "So với lần 2: 1,5 N, góc 90°", 46, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s + MOVE + SETTLE, "tap") for s in TS]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.3, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-thuchanhthl-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Thực hành tổng hợp lực · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ba lực kế kéo nút O", draw=s_hook, tail=0.3, caps=[
   ("Lực kế 3 treo vật nặng.", 2.8),
   ("Tự đoán trước.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("O đứng yên mới đọc số.", 3.6),
   ("Đổi chốt hoặc đổi vật.", 3.6)]),
 dict(key="dapan", title="Vẽ hình bình hành lần 2", draw=s_dapan, tail=0.5, caps=[
   ("Cạnh 4,0 cm, góc 60°.", 3.6),
   ("So với lực đo được.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Lần 3 vượt Δ. Kết luận gì?", 5.0),
   ("Còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 7.2)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
