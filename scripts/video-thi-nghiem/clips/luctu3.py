# Clip: tn-l12-luctu-03 - Khung day quay trong tu truong (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-luctu-03.json:
#   tham_so: khung 3 cm x 4 cm, 20 vong, pin 1,5 V, I mac dinh 0,5 A, B = 0,20 T.
#   so_lieu_mau: (40 vong, 0,5 A) va (20 vong, 1,0 A) cung M_max = 0,0048 N.m -> dap so cau chot (bang nhau); clip KHONG
#   hien so mo-men nao (khong_chung_minh[1]: chua do truc tiep duoc mo-men).
# Du doan (khung ben canh, K10 khong ve nut): khung 20 vong nam ngang (mat khung song song B), noi pin ->
#   A. bi day tinh tien ra khoi nam cham (hien_tuong_hay_sai[0]) ; B. quay mai khong dung (hien_tuong_hay_sai[1]) ;
#   C. quay roi dung khi mat khung vuong goc duong suc (DUNG) ; D. quay roi dung khi mat khung song song duong suc.
# Bay: hien_tuong_hay_sai[1] "quay mai nhu dong co" -> qua vi tri can bang, mo-men keo nguoc lai, dao dong roi dung.
# Chua noi duoc: khong_chung_minh[0] (dong co can co gop), [1] (chua do mo-men).
# Cau chot (ca moi): 40 vong 0,5 A vs 20 vong 1,0 A -> bang nhau (so_lieu_mau hang 2-3). Ghi chu cho phien chinh: ca chot
#   chua ghi vao ghi_chu cua kho (brief cam sua kho). Cau 4 cua bai (vi sao quay ma khong bi day di) dat SAU clip.
# Hinh xien: ve bang P(X, Y, Z), X xien len-phai = RA XA nguoi xem, Y phai, Z len (he TAY TRAI - cong B 14/11 bat loi:
#   assert cu tinh tren he nay nen tu khop ma sai). Vat li kiem bang check_F() trong he tay phai (x ve phia nguoi xem).
#   Nam cham chu U dung, mo mieng len, N trai S phai -> B sang phai. Khung quay quanh truc doc chieu sau giua khe; hai canh
#   dai (4 cm) doc chieu sau. e = (0, cos th, sin th): th = 0 mat khung nam ngang (song song B), th = 90 mat khung dung
#   (vuong goc B). Canh ben phai co I HUONG VE PHIA NGUOI XEM, B sang phai -> F len; canh trai I ra xa -> F xuong:
#   ngau luc quay th tang toi 90 roi dung (vi tri can bang BEN: qua 90 thi mo-men keo nguoc lai). Dao pin: th -> -90.
from engine import *

# ---- kiem vat li that (cong B 14/11): he ve P(X, Y, Z) co X xien RA XA nguoi xem, Y phai, Z len = he TAY TRAI.
# Vat li tinh trong he TAY PHAI x = ve phia nguoi xem = -X. phys() doi vec "huong ve tren man" sang he tay phai.
def _cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def phys(v): return (-v[0], v[1], v[2])
def check_F(I_draw, B_draw, F_draw):
    """F = I x B tinh trong he tay phai phai trung huong F ve tren man."""
    f = _cross(phys(I_draw), phys(B_draw)); g = phys(F_draw)
    nf, ng = math.hypot(*f), math.hypot(*g)
    assert nf > 0 and all(abs(f[i] / nf - g[i] / ng) < 1e-9 for i in range(3)), (I_draw, B_draw, F_draw, f)

EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

check_F((-1, 0, 0), (0, 1, 0), (0, 0, 1))       # canh phai: I ve phia nguoi xem (-X tren man) -> F len
check_F((1, 0, 0), (0, 1, 0), (0, 0, -1))       # canh trai: I ra xa -> F xuong
# on dinh: mo-men quanh truc chieu sau ~ cos th: duong khi th < 90 (keo len), am khi th > 90 (keo ve) -> can bang ben o 90
assert math.cos(math.radians(80)) > 0 > math.cos(math.radians(100))

# ---------------- hinh nam cham chuan (port PIL tu svg_lib.u_magnet, thay chot 31/10/2026) ----------------
# Ve trong he toa do rieng cua nam cham chu U (nhu SVG: u sang phai, v xuong; mo mieng o v = 0, canh N o u nho,
# canh S o u lon), roi anh xa ra man hinh qua Q(u, v) -> (x, y) => xoay/nghieng tuy y. dep = vec chieu sau (man hinh).
# Mat sau xam dam, mat ben nhin thay (phap tuyen ngoai cung chieu dep) to mau theo vung (cuc N/S/than),
# mat truoc than xam #cbd5e1, vien #334155, dau cuc N do / S xanh, chu N/S trang dam. Khong sua engine (lo song song).
UM_BODY, UM_DARK, UM_EDGE = (203, 213, 225), (148, 163, 184), (51, 65, 85)
UM_N = ((220, 38, 38), (248, 113, 113), (185, 28, 28))      # mat truoc, mat tren, mat ben
UM_S = ((37, 99, 235), (96, 165, 250), (30, 64, 175))

def _arcpts(cx, cy, r, a0, a1, n=8):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]

def _u_outline(w, h, arm, yoke, r, ri):
    yi = h - yoke
    return ([(0, 0)] + _arcpts(r, h - r, r, 180, 90) + _arcpts(w - r, h - r, r, 90, 0) + [(w, 0), (w - arm, 0)]
            + _arcpts(w - arm - ri, yi - ri, ri, 0, 90) + _arcpts(arm + ri, yi - ri, ri, 90, 180) + [(arm, 0)])

def u_magnet_pil(d, Q, w, h, arm, yoke, tip, dep, fs=60, alpha=1.0, mid=None, lab=True, ew=3):
    """Nam cham chu U kieu chuan. mid(d): ve them giua mat ben va mat truoc (vat nam trong khe)."""
    c = lambda col: A(col, alpha)
    r = min(arm, yoke) * 0.7; ri = min(arm, yoke) * 0.35
    L = _u_outline(w, h, arm, yoke, r, ri); S = [Q(u, v) for u, v in L]; n = len(S)
    d.polygon([(x + dep[0], y + dep[1]) for x, y in S], fill=c(UM_DARK), outline=c(UM_EDGE), width=ew)
    area = sum(S[i - 1][0] * S[i][1] - S[i][0] * S[i - 1][1] for i in range(n))
    for i in range(n):
        p, q = S[i], S[(i + 1) % n]; (u0, v0), (u1, v1) = L[i], L[(i + 1) % n]
        ex, ey = q[0] - p[0], q[1] - p[1]
        if ex * ex + ey * ey < 1e-6: continue
        nx, ny = (ey, -ex) if area > 0 else (-ey, ex)
        if nx * dep[0] + ny * dep[1] <= 0: continue                     # mat ben quay vao trong: bi che
        mu, mv = (u0 + u1) / 2, (v0 + v1) / 2
        top = abs(v0) < 1e-6 and abs(v1) < 1e-6
        if mu <= arm + 1 and mv <= tip: col = UM_N[1] if top else UM_N[2]
        elif mu >= w - arm - 1 and mv <= tip: col = UM_S[1] if top else UM_S[2]
        else: col = UM_DARK
        d.polygon([p, q, (q[0] + dep[0], q[1] + dep[1]), (p[0] + dep[0], p[1] + dep[1])], fill=c(col), outline=c(UM_EDGE), width=ew)
    if mid: mid(d)
    d.polygon(S, fill=c(UM_BODY), outline=c(UM_EDGE), width=ew)
    for u0, col in ((0, UM_N[0]), (w - arm, UM_S[0])):
        d.polygon([Q(u0, 0), Q(u0 + arm, 0), Q(u0 + arm, tip), Q(u0, tip)], fill=c(col), outline=c(UM_EDGE), width=ew)
    if lab:
        text(d, Q(arm / 2, tip / 2), "N", fs, WHITE, alpha=alpha)
        text(d, Q(w - arm / 2, tip / 2), "S", fs, WHITE, alpha=alpha)

# Chieu xien: X = chieu sau (ve xien len-phai), Y = sang phai, Z = len tren.
KX, KY = 0.75, 0.45
def mkP(ox, oy): return lambda X, Y, Z: (ox + Y + KX * X, oy - Z - KY * X)

def chevron(d, x, y, ang, color, s=18, w=5):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def fline(d, p, q, color=PURPLE, w=4, at=0.5, s=18):
    """Duong suc thang p -> q, mot dau V 30 do o giua chi chieu."""
    d.line([p, q], fill=color, width=w)
    m = (lerp(p[0], q[0], at), lerp(p[1], q[1], at))
    chevron(d, m[0], m[1], math.atan2(q[1] - p[1], q[0] - p[0]), color, s=s, w=w)

def dashed(d, p1, p2, color, w=3, dash=12, gap=9):
    Ld = math.dist(p1, p2); n = max(1, int(Ld // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / Ld; b = min(1, (i * (dash + gap) + dash) / Ld)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
NOTE = (70, 75, 95)

# ---------------- bo thi nghiem ----------------
P = mkP(200, 400)
COPPER = (184, 115, 51)
MW, MH, MARM, MYOKE, MTIP, MT = 560, 400, 130, 110, 210, 180   # nam cham (he rieng) + be day chieu X
DEP = (KX * MT, -KY * MT)
QM = lambda u, v: P(0, u, -v)                             # U dung, mo mieng len, N trai S phai
YC, ZC = MW / 2, -MTIP / 2                                # truc quay
XK0, XK1, RK = 10, 170, 82                                # khung: canh dai 4 cm doc X, canh ngan 3 cm (ban kinh 60)
I_TOI = (XK1 - 30, XK0 + 35)                               # mui ten I canh phai khi sg > 0 (X giam: ve phia nguoi xem)
check_F((I_TOI[1] - I_TOI[0], 0, 0), (0, 1, 0), (0, 0, 1))  # noi assert voi chinh huong mui ten ve: canh phai F len
check_F((I_TOI[0] - I_TOI[1], 0, 0), (0, 1, 0), (0, 0, -1)) # canh trai (mui ten nguoc): F xuong

def src_card(d, on, sg=1):
    for (x, y), pos in (((282, 832), sg > 0), ((448, 832), sg < 0)):       # cuc pin: doi cho khi dao cuc
        dot(d, x, y, 32, RED if pos else NAVY); text(d, (x, y - 3), "+" if pos else "−", 62, WHITE)
    card(d, (40, 860, 640, 1005), fill=WHITE, outline=NAVY, r=18, w=4)
    text(d, (340, 898), "Pin 1,5 V" + (" (đảo cực)" if sg < 0 else ""), 58, NAVY)
    text(d, (340, 965), "I = 0,5 A" if on else "I = 0", 58, ORANGE if on else NOTE)

def khung(d, th, on, sg, showF=True):
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    def K(X, r): return P(X, YC + r * c, ZC + r * s)
    poly = [K(XK0, RK), K(XK1, RK), K(XK1, -RK), K(XK0, -RK)]
    d.polygon(poly, fill=A(COPPER, 0.16))
    d.polygon([K(XK0 + 7, RK - 9), K(XK1 - 7, RK - 9), K(XK1 - 7, -RK + 9), K(XK0 + 7, -RK + 9)], outline=COPPER, width=4)
    d.line(poly + [poly[0]], fill=COPPER, width=9, joint="curve")
    d.line([K(XK0, RK), K(XK1, RK)], fill=(150, 20, 60), width=16)          # canh danh dau (r > 0): thay chieu quay tu khung tinh
    if on:
        for r in (RK, -RK):
            dirn = sg * (1 if r > 0 else -1)                     # dirn > 0: I ve phia nguoi xem (X giam)
            a0, a1 = I_TOI if dirn > 0 else I_TOI[::-1]
            arrow(d, K(a0, r * 1.25), K(a1, r * 1.25), ORANGE, w=9, head=24)
            if showF:
                p = K((XK0 + XK1) / 2, r); up = sg * (1 if r > 0 else -1)
                arrow(d, p, (p[0], p[1] - up * 105), GREEN, w=10, head=28)
                fx, fy = p[0] + (-52 if r > 0 else 52), p[1] - up * 85
                card(d, (fx - 34, fy - 40, fx + 34, fy + 40), fill=WHITE, outline=GREEN, r=12, w=3)
                text(d, (fx, fy), "F", 58, GREEN)

def rig(d, th, on, sg=1, showF=True):
    def mid(dd):
        for z in (-15, -55, -95, -135, -175): fline(dd, P(20, MARM, z), P(20, MW - MARM, z), at=0.2)   # B: N -> S
        dd.line([P(0, YC, ZC), P(MT + 40, YC, ZC)], fill=NAVY, width=6)                                # truc quay
        khung(dd, th, on, sg, showF)
    u_magnet_pil(d, QM, MW, MH, MARM, MYOKE, MTIP, DEP, mid=mid)
    pa = P(-50, YC, ZC)
    d.line([pa, P(0, YC, ZC)], fill=NAVY, width=6)
    d.line([pa, P(-50, YC, -MH)], fill=GRAY, width=6)                                                    # gia do truc
    d.line([(pa[0] - 6, pa[1] + 6), (pa[0] - 90, pa[1] + 160), (330, 860)], fill=COPPER, width=4, joint="curve")
    d.line([(pa[0] + 6, pa[1] + 10), (pa[0] - 60, pa[1] + 200), (400, 860)], fill=COPPER, width=4, joint="curve")
    d.ellipse([pa[0] - 10, pa[1] - 10, pa[0] + 10, pa[1] + 10], fill=NAVY)
    card(d, (30, 260, 250, 370), fill=WHITE, outline=PURPLE, r=16, w=3)            # chu thich B o vung trong
    arrow(d, (55, 315), (165, 315), PURPLE, w=7, head=22); text(d, (208, 315), "B", 60, PURPLE)

def settle(tau, target, gam=1.7, om=5.2):
    """Khung buong tu th = 0, mo-men keo ve target: dao dong tat dan (vuot qua roi bi keo lai)."""
    if tau <= 0: return 0.0
    return target * (1 - math.exp(-gam * tau) * (math.cos(om * tau) + gam / om * math.sin(om * tau)))

def blend_rigs(img, k, drawA, drawB):
    if k <= 0: drawA(ImageDraw.Draw(img, "RGBA")); return
    if k >= 1: drawB(ImageDraw.Draw(img, "RGBA")); return
    a, b = img.copy(), img.copy()
    IMG_REF[0] = a; drawA(ImageDraw.Draw(a, "RGBA")); IMG_REF[0] = b; drawB(ImageDraw.Draw(b, "RGBA"))
    img.paste(Image.blend(a, b, k)); IMG_REF[0] = img

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut A-D) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0, False); src_card(d, False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 450), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 175), "Nối pin vào khung 20 vòng.", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Khung sẽ thế nào?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 350, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
def stages(sc):
    M = sc["M"]
    return dict(s1=0.6, s2=M[1], s3=M[2])

def state_do(t, sc):
    """(goc, on, sg, so hang) dong bo: the pin, mui ten I/F, goc khung, bang quan sat."""
    s = stages(sc)
    if t < s["s1"]: th, on, sg = 0.0, False, 1
    elif t < s["s2"]: th, on, sg = settle(t - s["s1"], 90), True, 1
    elif t < s["s3"]: th, on, sg = 90 * (1 - ease((t - s["s2"] - 0.3) / 0.9)), False, 1
    else: th, on, sg = settle(t - s["s3"], -90), True, -1
    n = 2 * (t >= s["s1"] + 2.4) + (t >= s["s3"] + 2.4)                 # hang hien khi khung da dung
    return th, on, sg, n

ROWS = (("Nối pin", "quay rồi dừng"), ("Lúc dừng", "khung vuông góc B"), ("Đảo cực pin", "quay ngược"))
def obs_card(d, n, y0=1030):
    if n <= 0: return
    card(d, (40, y0, 1040, y0 + 40 + 110 * n), fill=WHITE, outline=LIGHT, w=3)
    for j in range(n):
        yy = y0 + 75 + 110 * j
        text(d, (80, yy), ROWS[j][0], 58, NAVY, anchor="lm")
        text(d, (395, yy), "→ " + ROWS[j][1], 58, INK, anchor="lm")

def s_do(img, d, t, sc):
    th, on, sg, n = state_do(t, sc)
    rig(d, th, on, sg); src_card(d, on, sg); obs_card(d, n)

# ---------------- canh 3: Dap an + rut ra (chieu lai: khung nam ngang -> ngau luc -> dung o 90 do) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; t0 = M[1] - 0.2
    th = settle(t - t0, 90) if t > t0 else 0.0
    rig(d, th, True); src_card(d, True)
    k1 = appear(t, M[0] + 1.2, 0.45); k2 = appear(t, M[1] + 2.6, 0.45)
    if k1 > 0:
        card(d, (40, 1030, 1040, 1250 + 120 * (k2 > 0)), fill=A(WHITE, k1), outline=A(NAVY, k1), w=5)
        text(d, (W / 2, 1100), "Hai lực ngược chiều:", 62, INK, alpha=k1)
        text(d, (W / 2, 1185), "ngẫu lực làm khung quay", 62, INK, alpha=k1)
    if k2 > 0: text(d, (W / 2, 1310), "Khung vuông góc B: M = 0", 62, DORANGE, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    th = settle(t - (mk + 0.2), 90, gam=1.0, om=4.2) if t > mk + 0.2 else 0.0
    on = t > mk + 0.2
    rig(d, th, on, 1, showF=False); src_card(d, on)
    k0 = 1.0; k2 = appear(t, mk + 0.2, 0.45)
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3); y = 1030
    if a1 > 0:
        card(d, (40, y, 1040, y + 300 + 140 * k2), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", RED, a1)
        q = "“Khung quay mãi như động cơ”"
        ks = clamp((t - mk) / 0.4); f = F(60); lw = tw(d, q, f); yy = y + 200
        text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        if k2 > 0: text(d, (W / 2, y + 340), "Quá 90°: kéo ngược lại", 62, DORANGE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 200), "Vì sao động cơ quay mãi?", 62, INK, alpha=k3)

# ---------------- canh 5: THU NGHI (cau chot o khung: hai khung cung M_max) ----------------
def coil(d, cx, cy, n, k):
    for j in range(n):                                            # so net vien ~ so vong (40 vong: 4 net, 20 vong: 2 net)
        o = 9 * j; d.rectangle([cx - 95 + o, cy - 70 + o, cx + 95 - o, cy + 70 - o], outline=A(COPPER, k), width=5)

def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k)
    for j, (n, i, nn) in enumerate((("40 vòng", "I = 0,5 A", 4), ("20 vòng", "I = 1,0 A", 2))):
        x0 = 80 + 470 * j
        card(d, (x0, 380, x0 + 450, 800), fill=A((255, 250, 245), k), outline=A(COPPER, k), r=20, w=4)
        cx = x0 + 225; coil(d, cx, 500, nn, k)
        text(d, (cx, 650), n, 60, INK, alpha=k)
        text(d, (cx, 735), i, 60, ORANGE, alpha=k)
    text(d, (W / 2, 880), "Cùng nam châm, khung 3×4 cm", 58, NOTE, alpha=k)
    text(d, (W / 2, 1000), "Mômen cực đại:", 64, INK, alpha=k)
    text(d, (W / 2, 1090), "khung nào lớn hơn?", 64, DORANGE, alpha=k)
    seg_bar(d, 1230, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    s = stages(do)
    return ([(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s[k], "tap") for k in ("s1", "s2", "s3")]
            + [(da["t0"] + da["M"][1] - 0.2, "tap"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l12-luctu-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Lực từ · Cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Khung dây trong nam châm", draw=s_hook, tail=0.3, caps=[
   ("Khung nằm ngang giữa hai cực.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Nối pin: khung quay.", 3.8),
   ("Ngắt, đặt khung nằm ngang lại.", 3.4),
   ("Đảo cực pin, nối lại.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Giữ khung: hai lực từ.", 3.2),
   ("Thả ra: quay rồi dừng.", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.9, caps=[
   ("Đúng không?", 2.5),
   ("Sai: lắc rồi dừng.", 3.4),
   ("Chưa nói được.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng lại, tự so sánh.", 6.8)]),
])
