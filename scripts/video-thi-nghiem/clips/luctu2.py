# Clip: tn-l12-luctu-02 - Day treo giua hai cuc nam cham chu U (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-luctu-02.json:
#   tham_so: I mac dinh 2,0 A; B = 0,1 T; l = 0,05 m (ghi "dai 5 cm"); alpha 90 (vuong goc) va 0 (song song).
#   so_lieu_mau: (2,0 A, 30 do) -> F = 5,0 mN = dap so cau chot (KHONG hien o dau trong clip). Clip khong hien so mN nao
#   khac: khong_chung_minh ghi "do lech chi cho biet luc lon hay nho, chua do duoc F".
# Du doan (khung ben canh, K10 khong ve nut): da thay chieu 1 day lech sang phai; giu I = 2,0 A, dao chieu dong ->
#   A. van lech sang phai, it hon (hien_tuong_hay_sai[0]) ; B. lech sang trai, do lech nhu cu (DUNG) ;
#   C. dung yen ; D. bi keo doc theo day (hien_tuong_hay_sai[2]).
# Bay: hien_tuong_hay_sai[1] "day trong tu truong luon bi day" -> day doc duong suc dung yen (F = B.I.L.sin 0 = 0).
# Cau chot (ca moi, so moi): I = 2,0 A, day hop duong suc 30 do -> co lech, F = 5,0 mN (so_lieu_mau hang 3).
# Hinh xien: ve bang P(X, Y, Z) voi X xien len-phai = RA XA nguoi xem, Y sang phai, Z len (he TAY TRAI - cong B 14/11
#   bat loi: assert cu tinh tren he nay nen tu khop ma sai). Vat li kiem bang check_F() trong he tay phai (x ve phia nguoi
#   xem). Nam cham chu U nam nghieng, mo mieng sang phai, canh N tren, S duoi -> B huong xuong. Day doc X xuyen khe, treo
#   bang hai soi chi. Chieu 1: I HUONG VE PHIA NGUOI XEM, B xuong -> F sang phai (ban tay trai: B xuyen long ban tay, bon
#   ngon theo I ra phia nguoi xem, ngon cai chi sang phai). Dao chieu: I ra xa -> sang trai. Song song: xoay nam cham 90 do
#   -> B doc theo day -> F = 0.
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

def chot_box(d, t, sc, chot, hoi, body, goi_y, y_hint, y_bot):
    """Nhu engine.chot_hoi nhung hop THU NHO theo noi dung (khong de trong 40 %)."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, chot, 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, y_bot), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 795, hoi, 46, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
    body(d, t, k1)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, y_hint, 970, y_hint + 200), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, y_hint + 52, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, y_hint + 135, goi_y, 48, (176, 64, 8), maxw=820, alpha=kh)

XI0, XI1 = -5, -90                                          # mui ten I chieu 1: tu sau ra truoc (ve phia nguoi xem)
check_F((XI1 - XI0, 0, 0), (0, 0, -1), (0, 1, 0))          # chieu 1: lech phai
check_F((XI0 - XI1, 0, 0), (0, 0, -1), (0, -1, 0))         # dao chieu: lech trai
assert _cross(phys((1, 0, 0)), phys((1, 0, 0))) == (0, 0, 0)  # day doc duong suc: F = 0

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

def u_magnet_pil(d, Q, w, h, arm, yoke, tip, dep, fs=48, alpha=1.0, mid=None, lab=True, ew=3):
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

def b_legend(d, p, q):
    """Chu thich chieu B o vung trong (khong de len nam cham/duong suc)."""
    card(d, (min(p[0], q[0]) - 30, min(p[1], q[1]) - 30, max(p[0], q[0]) + 90, max(p[1], q[1]) + 30), fill=WHITE, outline=PURPLE, r=16, w=3)
    arrow(d, p, q, PURPLE, w=7, head=22)
    text(d, (max(p[0], q[0]) + 50, (p[1] + q[1]) / 2), "B", 50, PURPLE)

# ---------------- bo thi nghiem ----------------
P = mkP(700, 470)
WIRE = (125, 135, 155); COPPER = (184, 115, 51)
MW, MH, MARM, MYOKE, MTIP = 360, 430, 95, 110, 150      # nam cham (he rieng)
T1 = 100; DEP1 = (KX * T1, -KY * T1)                     # be day nam cham khi dung (chieu X)
Q1 = lambda u, v: P(0, -v, -u)                           # U nghieng: mo mieng sang phai (+Y), canh N o tren
YW, ZC, ZP, XF, XB, DX = -75, -180, 120, -90, 190, 40    # day: Y can bang, Z giua khe; Z diem treo; hai dau day; do lech
T2 = 70; DEP2 = (0, T2); ZF = -150
Q2 = lambda u, v: P(u - 180, -v, ZF)                     # U nam ngang (xoay 90 do quanh Y): canh N truoc, S sau

def src_card(d, on):
    card(d, (60, 880, 330, 965), fill=WHITE, outline=NAVY, r=18, w=4)
    text(d, (195, 922), "I = 2,0 A" if on else "I = 0", 46, ORANGE if on else NOTE)

def rig_perp(d, dx, on, sgn, showF=True):
    pb = P(XB, YW + dx, ZC)
    d.line([P(XB, YW, ZP), pb], fill=NAVY, width=3)                                         # chi treo phia sau
    d.line([pb, (pb[0] + 40, pb[1] + 180), (pb[0] + 30, 905), (330, 925)], fill=COPPER, width=4, joint="curve")
    def mid(dd):
        for yy in (-135, -105, -75, -45, -15): fline(dd, P(50, yy, -95), P(50, yy, -265))     # B tu N xuong S
        dd.line([P(0, YW + dx, ZC), pb], fill=WIRE, width=12)                                # doan day trong khe + sau
    u_magnet_pil(d, Q1, MW, MH, MARM, MYOKE, MTIP, DEP1, mid=mid)
    b_legend(d, (930, 500), (930, 630))
    dashed(d, P(XF, YW, ZP), P(XF, YW, ZC - 34), GRAY, w=3)                                # vi tri can bang
    pf = P(XF, YW + dx, ZC)
    d.line([P(XF, YW, ZP), pf], fill=NAVY, width=3)                                         # chi treo phia truoc
    d.line([pf, P(0, YW + dx, ZC)], fill=WIRE, width=12)
    d.line([pf, (pf[0] - 120, pf[1] + 120), (200, 880)], fill=COPPER, width=4, joint="curve")
    if on:
        a0, a1 = (XI0, XI1) if sgn > 0 else (XI1, XI0)
        arrow(d, P(a0, YW + dx, ZC + 34), P(a1, YW + dx, ZC + 34), ORANGE, w=7, head=20)
        pi = P(a1, YW + dx, ZC + 34); lx = pi[0] - 40
        card(d, (lx - 30, pi[1] - 82, lx + 30, pi[1] - 14), fill=WHITE, outline=ORANGE, r=12, w=3)
        text(d, (lx, pi[1] - 48), "I", 56, ORANGE)
        if showF:
            p = P(-45, YW + dx, ZC); q = (p[0] + sgn * 105, p[1])
            arrow(d, p, q, GREEN, w=9, head=26)
            fx = q[0] + sgn * 44
            card(d, (fx - 30, q[1] - 34, fx + 30, q[1] + 34), fill=WHITE, outline=GREEN, r=12, w=3)
            text(d, (fx, q[1]), "F", 56, GREEN)
    d.line([P(XF - 25, YW, ZP), P(XB + 25, YW, ZP)], fill=NAVY, width=10)                    # gia treo

def rig_par(d, on):
    def mid(dd):                                                   # trong khe: sau mat truoc nam cham (khong de len chu N)
        for yy in (-135, -105, -75, -45, -15): fline(dd, P(-85, yy, ZF - 20), P(85, yy, ZF - 20), w=5)
        for x in (-80, 80): dd.line([P(x, YW, ZP), P(x, YW, ZF - 20)], fill=NAVY, width=3)
        dd.line([P(-80, YW, ZF - 20), P(80, YW, ZF - 20)], fill=(51, 65, 85), width=14)
    u_magnet_pil(d, Q2, MW, MH, MARM, MYOKE, MTIP, DEP2, mid=mid)
    b_legend(d, (870, 650), (870 + KX * 130, 650 - KY * 130))
    if on:
        arrow(d, P(60, YW, ZF + 14), P(-40, YW, ZF + 14), ORANGE, w=7, head=20)        # I ve phia nguoi xem
        pm = P(10, YW, ZF + 14); lx, ly = pm[0] + 10, pm[1] - 62
        card(d, (lx - 30, ly - 34, lx + 30, ly + 34), fill=WHITE, outline=ORANGE, r=12, w=3)
        text(d, (lx, ly), "I", 56, ORANGE)
    d.line([P(-105, YW, ZP), P(105, YW, ZP)], fill=NAVY, width=10)

def blend_rigs(img, k, drawA, drawB):
    """Chuyen mo giua hai hinh (xoay nam cham): ve tung hinh len ban sao roi tron."""
    if k <= 0: drawA(ImageDraw.Draw(img, "RGBA")); return
    if k >= 1: drawB(ImageDraw.Draw(img, "RGBA")); return
    a, b = img.copy(), img.copy()
    IMG_REF[0] = a; drawA(ImageDraw.Draw(a, "RGBA")); IMG_REF[0] = b; drawB(ImageDraw.Draw(b, "RGBA"))
    img.paste(Image.blend(a, b, k)); IMG_REF[0] = img

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; k = appear(t, M[0] + 0.7, 0.5)
    rig_perp(d, DX * k, on=t >= M[0] + 0.7, sgn=1)
    src_card(d, t >= M[0] + 0.7)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 450), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 165), "Giữ I = 2,0 A, đảo chiều dòng điện.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "Dây sẽ thế nào?", 50, INK, alpha=a)
    text(d, (W / 2, y0 + 330), "Chọn đáp án ở khung câu hỏi", 44, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 400, 940, y0 + 414], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 400, 140 + 800 * (1 - p), y0 + 414], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def stages(sc):
    M = sc["M"]; s4 = M[2]
    return dict(s1=0.6, s2=M[1], s3=M[1] + 1.3, s4=s4, r0=s4 + 0.5, r1=s4 + 1.3, s5=s4 + 1.9)

def state_do(t, sc):
    """(dx, on, sgn, k xoay, so hang) dong bo: am pe ke, mui ten I, do lech, bang quan sat."""
    s = stages(sc)
    if t < s["s1"]: dx, on, sg = 0.0, False, 1
    elif t < s["s2"]: dx, on, sg = DX * ease((t - s["s1"]) / 0.5), True, 1
    elif t < s["s3"]: dx, on, sg = DX * (1 - ease((t - s["s2"]) / 0.5)), False, 1
    elif t < s["s4"]: dx, on, sg = -DX * ease((t - s["s3"]) / 0.5), True, -1
    else: dx, on, sg = -DX * (1 - ease((t - s["s4"]) / 0.45)), t >= s["s5"], 1
    kr = clamp((t - s["r0"]) / (s["r1"] - s["r0"]))
    n = (t >= s["s1"] + 0.6) + (t >= s["s3"] + 0.6) + (t >= s["s5"] + 0.6)
    return dx, on, sg, kr, n

ROWS = (("Chiều 1", "dây lệch sang phải"), ("Chiều 2", "dây lệch sang trái"), ("B dọc theo dây", "dây đứng yên"))
def obs_card(d, n, y0=1010):
    if n <= 0: return
    card(d, (40, y0, 1040, y0 + 40 + 95 * n), fill=WHITE, outline=LIGHT, w=3)
    for j in range(n):
        yy = y0 + 68 + 95 * j
        text(d, (90, yy), ROWS[j][0], 46, NAVY, anchor="lm")
        text(d, (470, yy), "→  " + ROWS[j][1], 46, INK, anchor="lm")

def s_do(img, d, t, sc):
    dx, on, sg, kr, n = state_do(t, sc)
    blend_rigs(img, kr, lambda dd: rig_perp(dd, dx, on and kr <= 0, sg), lambda dd: rig_par(dd, on))
    d = ImageDraw.Draw(img, "RGBA")
    src_card(d, on); obs_card(d, n)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    rig_perp(d, -DX, True, -1)
    src_card(d, True)
    ka = appear(t, 0.4, 0.4); s = "ĐÁP ÁN · sang trái, độ lệch như cũ"
    pw = tw(d, s, F(40)) + 56
    card(d, (W / 2 - pw / 2, 1000, W / 2 + pw / 2, 1064), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 1032), s, 40, WHITE, alpha=ka)
    k1 = appear(t, M[0] + 1.4, 0.45); k2 = appear(t, M[1] + 0.3, 0.45)
    nb = (k1 > 0) + (k2 > 0)
    if nb:
        card(d, (40, 1095, 1040, 1135 + 100 * nb), fill=WHITE, outline=LIGHT, w=3)
        text(d, (W / 2, 1165), "Độ lớn F = B·I·L: không đổi", 48, INK, alpha=k1)
        if k2 > 0: text(d, (W / 2, 1265), "F vuông góc dây và đường sức", 48, GREEN, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    rig_par(d, True); src_card(d, True)
    k0 = appear(t, 0.2, 0.4); k2 = appear(t, mk + 0.2, 0.45)
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3); y = 1010
    if a1 > 0:
        card(d, (40, y, 1040, y + 250 + 200 * k2), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(RED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Dây trong từ trường luôn bị đẩy”"
        ks = clamp((t - mk) / 0.4); f = F(46); lw = tw(d, q, f); yy = y + 170
        text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        text(d, (W / 2, y + 280), "Góc giữa dây và B: 0°", 48, ORANGE, alpha=a1 * k2)
        text(d, (W / 2, y + 370), "F = B·I·L·sin 0° = 0", 52, INK, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        for j, s in enumerate(("• Độ lệch chưa cho số đo F", "• Từ trường có đều? Chưa kiểm")):
            kk = k3 * appear(t, M[2] + 0.2 + 0.5 * j, 0.4)
            text(d, (100, y + 200 + 105 * j), s, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    for j in range(5):                                           # duong suc deu (nhin tu tren, chieu B sang phai)
        yy = 1000 + 50 * j; fline(d, (110, yy), (520, yy), A(PURPLE, k), w=4, at=0.5)
    c, L = (320, 1100), 230; a = math.radians(30)
    p0, p1 = (c[0] - L * math.cos(a), c[1] + L * math.sin(a)), (c[0] + L * math.cos(a), c[1] - L * math.sin(a))
    d.line([p0, p1], fill=A((51, 65, 85), k), width=12)
    dashed(d, p1, (p1[0] + 230, p1[1]), A(PURPLE, k), w=3)                      # phuong duong suc, ngoai vung ve
    dashed(d, p1, (p1[0] + 140 * math.cos(a), p1[1] - 140 * math.sin(a)), A((51, 65, 85), k), w=3)
    d.arc([p1[0] - 130, p1[1] - 130, p1[0] + 130, p1[1] + 130], 330, 360, fill=A(ORANGE, k), width=5)
    text(d, (p1[0] + 190, p1[1] - 38), "30°", 44, ORANGE, alpha=k)

def s_end(img, d, t, sc):
    chot_box(d, t, sc, "Lực từ vuông góc dây và đường sức, đổi chiều theo I",
             "I = 2,0 A, dây hợp đường sức 30°. Dây có lệch không? Lực bao nhiêu mN?", _end_body,
             "B = 0,10 T, dây dài 5 cm", 1260, 1500)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    s = stages(do)
    return ([(h["t0"] + h["M"][0] + 0.7, "tap"), (h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s[k], "tap") for k in ("s1", "s3", "r0", "s5")]
            + [(da["t0"] + 0.4, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-luctu-02", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Lực từ · Cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Dây treo trong nam châm", draw=s_hook, tail=0.3, caps=[
   ("Đóng mạch: dây lệch sang phải.", 3.6),
   ("Nghĩ trước khi xem tiếp.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đóng mạch, I = 2,0 A.", 3.2),
   ("Ngắt, đảo hai đầu nguồn.", 3.6),
   ("Xoay nam châm 90°, đóng lại.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Đảo I thì lực đổi chiều.", 3.4),
   ("Chiều lực: quy tắc bàn tay trái.", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 2.5),
   ("Sai: dọc đường sức thì không lệch.", 3.4),
   ("Giới hạn thí nghiệm.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video và trả lời.", 6.8)]),
])
