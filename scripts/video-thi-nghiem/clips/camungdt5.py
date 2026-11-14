# Clip: tn-l12-camungdt-05 - Thanh truot tren hai ray trong tu truong deu, e = B.l.v (ban 1, 12/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-camungdt-05.json (so_lieu_mau, "so lieu minh hoa"):
#   B = 0,40 T, l = 20 cm, R = 2,0 ohm; v = 0 ; 0,25 ; 0,50 ; 1,00 m/s -> e = 0 ; 0,02 ; 0,04 ; 0,08 V ;
#   I = 0 ; 10 ; 20 ; 40 mA ; F keo = 0 ; 0,8 ; 1,6 ; 3,2 mN ; F.v = I^2.R = 0,8 mW o 0,50 m/s ; e/v = 0,08 = B.l.
# Du doan (khung ben canh, K10 khong ve nut): thanh dang truot deu 0,50 m/s thi thao day keo -> cham dan roi dung.
# Vat li (kiem bang tich co huong o duoi). Nhin tu tren xuong: x sang phai, y len man hinh, z huong ve nguoi nhin.
#   B huong len (kho) = +z (cham trong tron). Thanh truot +x: dien tich duong trong thanh chiu q v x B = -y
#   -> dong trong thanh tu ray tren xuong ray duoi -> vong mach CUNG chieu kim dong ho (nhin tu tren).
#   Lenz: dien tich mach tang -> tu thong +z tang -> dong cam ung tao B -z trong mach = cung chieu kim dong ho. Khop.
#   Luc tu len thanh F = I l x B = (-y) x z = -x: NGUOC chieu v (can). Truot -x: dong doi chieu, luc +x, van nguoc v.
# Mach kin: ray tren - nhanh trai (miliampe ke noi tiep R) - ray duoi - thanh; milivon ke mac song song giua hai ray.
from engine import *

def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
BZ = (0, 0, 1)
def bar_current(sv):            # dau y cua dong trong thanh (sv = +1 truot phai, -1 truot trai)
    return cross((sv, 0, 0), BZ)[1]
def bar_force(sv):              # dau x cua luc tu len thanh
    return cross((0, bar_current(sv), 0), BZ)[0]
assert bar_current(1) == -1 and bar_force(1) == -1           # dong xuong (tren man), luc nguoc v
assert bar_current(-1) == 1 and bar_force(-1) == 1
# Lenz: truot phai -> dien tich tang -> dong phai chay cung chieu kim dong ho (nhin tu +z): o canh phai (thanh) dong di xuong
assert bar_current(1) < 0

NOTE = (70, 75, 95)
COP = (184, 115, 51)
CUR = BLUE                                                  # dong dien: xanh duong, tach han khoi luc tu (do)
ROWS = ((0, "0", "0", "0", "0"), (0.25, "0,25", "0,02", "10", "0,8"), (0.5, "0,50", "0,04", "20", "1,6"),
        (1.0, "1,00", "0,08", "40", "3,2"))
FMN = {0: 0, 0.25: 0.8, 0.5: 1.6, 1.0: 3.2}
DOC = {r[0]: (r[2] + " V", r[3] + " mA") for r in ROWS}            # so chi von ke (V) / mA ke = dung hang bang

def sym(d, x, y, kind, r=14, color=PURPLE, w=3, alpha=1.0):
    """Ve tay: 'o' = huong ve nguoi xem (B huong len khi nhin tu tren), 'x' = huong ra xa."""
    c = A(color, alpha)
    d.ellipse([x - r, y - r, x + r, y + r], outline=c, width=w)
    if kind == "o": d.ellipse([x - r * 0.32, y - r * 0.32, x + r * 0.32, y + r * 0.32], fill=c)
    else:
        q = r * 0.6
        d.line([(x - q, y - q), (x + q, y + q)], fill=c, width=w); d.line([(x - q, y + q), (x + q, y - q)], fill=c, width=w)

def chevron(d, x, y, ang, color, s=18, w=6):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def tag(d, xy, s, size, color, anchor="mm", alpha=1.0):
    bb = d.textbbox(xy, s, font=F(size), anchor=anchor)
    d.rounded_rectangle([bb[0] - 8, bb[1] - 6, bb[2] + 8, bb[3] + 6], radius=10, fill=A(WHITE, 0.92 * alpha))
    text(d, xy, s, size, color, anchor=anchor, alpha=alpha)

# ---------------- hinh chinh (nhin tu tren xuong) ----------------
YT, YB, XR, XV, XE = 420, 760, 236, 82, 1000
def rig(d, xb, v, sv=1, string=True, kI=1.0, show_f=True, kF=1.0, vlab=None, keo=True, doc=None, fv=None):
    """xb: vi tri thanh; v (m/s) quyet dinh do dai mui ten v; fv: v dung cho luc (mac dinh = v); kI: do dam chieu dong."""
    fv = v if fv is None else fv
    for x in range(300, 981, 110):                              # B huong len: cham trong tron
        for y in (455, 725):
            if -56 < x - xb < (90 if y == 725 else 56): continue    # hang duoi: chua cho mui ten dong ben phai thanh
            sym(d, x, y, "o", 14)
    d.line([(XV, YT), (XE, YT)], fill=COP, width=10); d.line([(XV, YB), (XE, YB)], fill=COP, width=10)
    # nhanh milivon ke (song song) va nhanh miliampe ke + R (noi tiep)
    # dong ho hien so: hop chu nhat noi tiep tren day (day dung o mep hop, khong chay qua chu)
    for x, y0, y1 in ((XV, YT, 525), (XV, 655, YB), (XR, YT, 455), (XR, 585, 600), (XR, 700, YB)):
        d.line([(x, y0), (x, y1)], fill=NAVY, width=5)
    for x, y0, y1, nm, j in ((XV, 525, 655, "V", 0), (XR, 455, 585, "mA", 1)):
        d.rounded_rectangle([x - 70, y0, x + 70, y1], radius=12, fill=WHITE, outline=NAVY, width=5)
        text(d, (x, y0 + 34), nm, 40, NAVY)
        if doc: text(d, (x, y0 + 94), doc[j], 40, INK, bold=False)
    d.rectangle([XR - 18, 600, XR + 18, 700], fill=WHITE, outline=NAVY, width=5)
    text(d, (XR + 34, 650), "R", 42, NAVY, anchor="lm")
    # thanh
    d.rounded_rectangle([xb - 9, YT - 30, xb + 9, YB + 30], radius=6, fill=(120, 72, 30))
    if string:
        d.line([(xb + 9, 640), (XE + 40, 640)], fill=NAVY, width=3)
    # chieu dong cam ung (dong bo voi v: kI = 0 khi v = 0)
    if kI > 0:
        cI = A(CUR, kI); cw = 1 if bar_current(sv) < 0 else -1        # cw = +1: cung chieu kim dong ho tren man
        mid = (XR + xb) / 2
        arrow(d, (mid - 40 * cw, YT - 25), (mid + 40 * cw, YT - 25), cI, w=7, head=20)          # ray tren (duoi mui ten v y 355)
        arrow(d, (mid + 40 * cw, YB + 30), (mid - 40 * cw, YB + 30), cI, w=7, head=20)          # ray duoi
        # thanh: ben phai thanh, phan duoi (y 650-740) -- xa mui ten luc (y 540) va nhan luc (y 588)
        arrow(d, (xb + 34, 695 - 45 * cw), (xb + 34, 695 + 45 * cw), cI, w=7, head=20)
        text(d, (mid - 70, YT - 25), "I", 46, CUR, anchor="rm", alpha=kI)
    # v (tren thanh, phia tren ray)
    if v > 0:
        L = 120 * v; lab = vlab if vlab else "v"
        x1 = xb + sv * (L + 30)
        if sv > 0: x1 = min(x1, W - 50 - 18 - tw(d, lab, F(42)))      # nhan cach mep phai >= 50 px
        arrow(d, (xb, 355), (x1, 355), TEAL, w=7, head=20)
        text(d, (x1 + sv * 18, 355), lab, 42, TEAL, anchor="lm" if sv > 0 else "rm")
    # luc tu len thanh (do) va luc keo (xanh): cung do lon khi truot deu
    # mui ten dat tai thanh (y 540, giua hai hang cham y 455/725); nhan ngay duoi mui ten, khong cham cham B
    fm = FMN.get(fv, 0)
    if show_f and kF > 0 and fv > 0:
        L = 80 * (fm if fm else 1.6 * fv / 0.5)                  # 80 px/mN: 0,8 -> 64 px (> dau mui), ti le giu nguyen
        fx = bar_force(sv)
        arrow(d, (xb + fx * 14, 540), (xb + fx * (14 + L), 540), A(RED, kF), w=8, head=22)
        an = "rm" if fx < 0 else "lm"
        text(d, (xb + fx * 24, 590), "lực từ", 42, RED, anchor=an, alpha=kF)
        if string and keo:
            arrow(d, (xb + 14, 540), (xb + 14 + L, 540), A(NAVY, kF), w=8, head=22)
            text(d, (xb + 24, 590), "lực kéo", 42, NAVY, anchor="lm", alpha=kF)

def legend(d, full=True):
    sym(d, 110, 252, "o", 18, PURPLE, 4)
    text(d, (146, 252), "B = 0,40 T, hướng lên", 40, PURPLE, anchor="lm")
    if full: text(d, (W - 60, 303), "ray cách nhau 20 cm · R = 2,0 Ω", 44, INK, anchor="rm")

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; legend(d, False)
    xb = 520 + 12 * t                                       # truot deu (hinh), khong ve dong/luc: chua lo ket qua
    rig(d, xb, 0.5, kI=0, show_f=False, vlab="v = 0,50 m/s", doc=DOC[0.5])
    text(d, (W - 60, 600), "dây kéo", 44, NOTE, anchor="rm")
    a = appear(t, 0.5, 0.5)
    y0 = 860 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Thanh trượt đều thì tháo dây kéo.", 44, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "Bỏ qua ma sát.", 44, NOTE, alpha=a)
    text(d, (W / 2, y0 + 330), "Sau đó thanh chuyển động thế nào?", 46, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 412, 940, y0 + 426], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 412, 140 + 800 * (1 - p), y0 + 426], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
PXV, X0 = 20, 500                                           # px moi giay o 1 m/s (hinh); vi tri dau thanh
def stages(sc):                                             # moc doi toc do = moc hang bang + dong ho moi (cung luc)
    s1 = sc["M"][1] + 1.1; return (s1, s1 + 2.2, s1 + 4.4)

def state_do(t, sc):
    """(v, xb, so hang bang) dong bo: mui ten v, chieu dong, luc, hang bang tu mot ham."""
    st = stages(sc); vs = (0.25, 0.5, 1.0); xb = float(X0); v = 0.0
    for j, s in enumerate(st):
        e = st[j + 1] if j + 1 < len(st) else 1e9
        if t > s: xb += PXV * vs[j] * (min(t, e) - s); v = vs[j]
    n = 1 if t >= 1.2 else 0
    n += sum(1 for s in st if t > s)
    return v, xb, n

COLX = ((165, "v (m/s)"), (400, "e (V)"), (630, "I (mA)"), (880, "F kéo (mN)"))
def table(d, y0, n, alpha=1.0, hl=-1):
    card(d, (40, y0, 1040, y0 + 390), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, s in COLX: text(d, (x, y0 + 46), s, 40, NOTE, bold=False, alpha=alpha)
    d.line([(70, y0 + 84), (1010, y0 + 84)], fill=A(LIGHT, alpha), width=3)
    for j, r in enumerate(ROWS[:n]):
        yy = y0 + 84 + 72 * (j + 0.5) + 4
        if j == hl: d.rounded_rectangle([60, yy - 32, 1020, yy + 32], radius=14, fill=A((255, 237, 213), alpha))
        for (x, _), s in zip(COLX, r[1:]): text(d, (x, yy), s, 42, INK, alpha=alpha)
    text(d, (1020, y0 + 425), "số liệu minh hoạ", 42, NOTE, anchor="rm", alpha=alpha)

def s_do(img, d, t, sc):
    legend(d)
    v, xb, n = state_do(t, sc)
    vr = ROWS[n - 1][0] if n else 0.0                      # dong ho, chieu dong, luc doi CUNG LUC hang bang moi hien
    rig(d, xb, v, kI=1.0 if vr > 0 else 0.0, string=True, doc=DOC[vr] if n else None, fv=vr)
    table(d, 860, n)
    k = appear(t, sc["M"][2], 0.45)                         # rut ra cong thuc e (sau ca ba hang)
    if k > 0:
        card(d, (40, 1312, 1040, 1588), fill=A((239, 246, 255), k), outline=A(BLUE, k), w=5)
        text(d, (W / 2, 1365), "e : v = 0,08 V·s/m = 0,40 T × 0,20 m", 42, INK, alpha=k)
        k2 = appear(t, sc["M"][2] + 0.6, 0.45)
        text(d, (W / 2, 1450), "e = B × (khoảng cách hai ray) × v", 46, NAVY, alpha=k2)
        text(d, (W / 2, 1532), "e: suất điện động cảm ứng", 42, MUTED, alpha=k2)

# ---------------- canh 3: Dap an + Rut ra ----------------
TAU = 0.8
def meter(v):
    """So chi chay theo v luc tha thanh: I = 40.v lam tron theo buoc 5 mA, e = I.R (buoc 0,01 V) -> e, I luon khop R = 2,0
    va so V vua hop dong ho (khong can 3 chu so thap phan)."""
    i = 5 * round(8 * v)
    if v <= 0.02 or i == 0: return ("0 V", "0 mA")
    return (f"{i * 2.0 / 1000:.2f}".replace(".", ",") + " V", f"{i} mA")
assert meter(0.5) == DOC[0.5] and meter(0.0) == ("0 V", "0 mA") and meter(0.2) == ("0,02 V", "10 mA") and meter(0.08) == ("0,01 V", "5 mA")
def s_dapan(img, d, t, sc):
    M = sc["M"]
    rel = 0.6
    if t < rel: v, xb = 0.5, 600 + 15 * t
    else:
        u = t - rel; v = 0.5 * math.exp(-u / TAU); xb = 600 + 15 * rel + 30 * 0.5 * TAU * (1 - math.exp(-u / TAU))
    kv = v / 0.5
    rig(d, xb, v if v > 0.02 else 0, kI=kv if v > 0.02 else 0, string=t < rel, kF=1.0, vlab="v",
        doc=DOC[0.5] if t < rel else meter(v))
    if t >= rel: text(d, (W - 60, 280), "minh hoạ", 44, NOTE, anchor="rm")
    ka = appear(t, M[0] + 2.4, 0.4)
    if ka > 0:
        s = "ĐÁP ÁN · chậm dần rồi dừng"
        pw = tw(d, s, F(40)) + 56
        card(d, (W / 2 - pw / 2, 830, W / 2 + pw / 2, 896), fill=A(NAVY, ka), r=33)
        text(d, (W / 2, 863), s, 40, WHITE, alpha=ka)
    k1 = appear(t, M[0] + 2.8, 0.45)
    card(d, (40, 940, 1040, 1290), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    if k1 > 0:
        text(d, (W / 2, 1015), "Lực từ ngược chiều v: lực cản", 46, RED, alpha=k1)
        k2 = appear(t, M[0] + 3.4, 0.45)
        text(d, (W / 2, 1120), "kéo: 1,6 mN × 0,50 m/s = 0,8 mW", 44, NAVY, alpha=k2)
        k3 = appear(t, M[0] + 4.0, 0.45)
        text(d, (W / 2, 1220), "nhiệt: (0,020 A)²·2,0 Ω = 0,8 mW", 44, ORANGE, alpha=k3)

# ---------------- canh 4: Bay (bo the 'Chua noi duoc' 12/11: hoc sinh ao che thua; o chua_noi van o khung web) ----------------
def mini(d, x0, sv, k, kc):
    """Mach thu nho: ray x0+30..x0+450, R ben trai, thanh o giua; chieu dong + luc tinh tu tich co huong."""
    yt, yb = 420, 640; xr = x0 + 50; xb = x0 + 300; xe = x0 + 450
    card(d, (x0, 250, x0 + 470, 780), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    for x in (x0 + 130, x0 + 210, x0 + 400):
        sym(d, x, 452, "o", 12, PURPLE, 3, alpha=0.8 * k); sym(d, x, 608, "o", 12, PURPLE, 3, alpha=0.8 * k)
    d.line([(xr, yt), (xe, yt)], fill=COP, width=8); d.line([(xr, yb), (xe, yb)], fill=COP, width=8)
    d.line([(xr, yt), (xr, yb)], fill=NAVY, width=4)
    d.rectangle([xr - 14, 490, xr + 14, 570], fill=WHITE, outline=NAVY, width=4)
    d.rounded_rectangle([xb - 8, yt - 24, xb + 8, yb + 24], radius=5, fill=(120, 72, 30))
    arrow(d, (xb, 336), (xb + sv * 100, 336), A(TEAL, k), w=7, head=20)
    text(d, (xb + sv * 118, 336), "v", 42, TEAL, anchor="lm" if sv > 0 else "rm", alpha=k)
    if kc <= 0: return
    cw = 1 if bar_current(sv) < 0 else -1; cI = A(CUR, kc)             # chieu dong + luc: hien SAU khi gach cau sai
    mid = (xr + xb) / 2; fx = bar_force(sv)
    arrow(d, (mid - 36 * cw, yt - 36), (mid + 36 * cw, yt - 36), cI, w=7, head=20)
    arrow(d, (mid + 36 * cw, yb + 26), (mid - 36 * cw, yb + 26), cI, w=7, head=20)
    # dong trong thanh: phia KHONG co luc, dai 100 px; luc tu: tai thanh (y 505), nhan ngay duoi
    arrow(d, (xb - fx * 30, 530 - 50 * cw), (xb - fx * 30, 530 + 50 * cw), cI, w=8, head=22)
    text(d, (mid - 62, yt - 36), "I", 44, CUR, anchor="rm", alpha=kc)
    arrow(d, (xb + fx * 12, 505), (xb + fx * 110, 505), A(RED, kc), w=8, head=22)
    text(d, (xb + fx * 70, 552), "lực từ", 42, RED, alpha=kc)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    y = 830; mk = M[0] + 2.4; kc = appear(t, mk + 0.2, 0.45)
    mini(d, 40, 1, k0, kc); mini(d, 570, -1, k0, kc)
    a1 = k0
    if a1 > 0:
        card(d, (40, y, 1040, y + 250 + 230 * kc), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(RED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Trượt ngược lại, dòng vẫn như cũ”"
        ks = clamp((t - mk) / 0.4); f = F(46); lw = tw(d, q, f); yy = y + 170
        text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        k2 = a1 * kc
        text(d, (W / 2, y + 290), "Dòng đổi chiều", 46, CUR, alpha=k2)
        text(d, (W / 2, y + 400), "Lực từ vẫn ngược v", 46, RED, alpha=k2)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    yt, yb = 1040, 1220
    d.line([(300, yt), (800, yt)], fill=A(COP, k), width=8); d.line([(300, yb), (800, yb)], fill=A(COP, k), width=8)
    d.line([(300, yt), (300, yb)], fill=A(NAVY, k), width=4)
    d.rectangle([286, 1095, 314, 1165], fill=A(WHITE, k), outline=A(NAVY, k), width=4)
    text(d, (340, 1130), "R", 40, NAVY, anchor="lm", alpha=k)
    d.rounded_rectangle([592, yt - 22, 608, yb + 22], radius=5, fill=A((120, 72, 30), k))
    arrow(d, (600, 1130), (690, 1130), A(TEAL, k), w=7, head=20)
    text(d, (708, 1130), "v", 42, TEAL, anchor="lm", alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Lực từ lên thanh luôn cản chuyển động",
             "Kéo đều 0,50 m/s, thay R = 4,0 Ω. Công suất kéo thay đổi thế nào?", None, body=_end_body)
    kh = appear(t, M[0] + 2.6, 0.5)
    if kh > 0:
        card(d, (110, 1320, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1368, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1460, "R: 2,0 → 4,0 Ω; B, v giữ nguyên", 44, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tap") for s in stages(do)]
            + [(da["t0"] + 0.6, "tap"), (da["t0"] + da["M"][0] + 2.4, "ding"),
               (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-camungdt-05", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Thanh trượt trên hai ray", draw=s_hook, tail=0.3, caps=[
   ("Nhìn từ trên xuống: mạch kín.", 3.0),
   ("Chọn đáp án ở khung câu hỏi.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Thanh đứng yên: không có dòng.", 3.4),
   ("Kéo đều: 0,25; 0,50; 1,00 m/s.", 6.6),
   ("Rút ra: e tỉ lệ với v.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Tháo dây kéo, thanh chậm dần.", 7.4)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.8, caps=[
   ("Đúng hay sai?", 5.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video và trả lời.", 7.4)]),
])
