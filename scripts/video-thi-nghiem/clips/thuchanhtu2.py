# Clip: tn-l12-thuchanhtu-02 - Can dong dien: dao chieu dong, so can doi dau (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanhtu-02.json:
#   tham_so: I = 3,0 A (co dinh), chieu_I = +1 / -1. so_lieu_mau: thuan +1,45 g ; dao -1,45 g ; ngat 0,00 g.
#   Khong tinh B trong clip (thuchanhtu4 da tinh B o bay) ; khong quet I (thuchanhtu4) ; khong doi goc (thuchanhtu3).
# Du doan (khung ben canh, K10 khong ve nut) - KHAC thuchanhtu4 (hoi so can): hoi HUONG luc tu len nam cham khi dao I:
#   A. huong xuong, nhu truoc ; B. huong len (DUNG) ; C. bang 0 vi hai chieu triet tieu (hien_tuong_hay_sai[0]) ;
#   D. nam ngang, doc duong suc.
# Bay: hien_tuong_hay_sai[1] "khoi luong khong giam duoc, can van tang" + khong_chung_minh[1] (so can doi do phan luc
#   len nam cham). Chua noi duoc: khong_chung_minh[0] (F ti le I hay L: can thi nghiem khac).
# Cau chot (ca moi, khong trung du doan): dao chieu I DONG THOI doi cho hai cuc -> luc len day giu chieu cu -> +1,45 g.
#   Ghi chu cho phien chinh: ca chot chua ghi vao ghi_chu kho (brief cam sua kho). Dap an so -1,45 trung Cau 1 cua bai va
#   thuchanhtu4, nhung clip nay hoi chieu luc len nam cham, khong hoi so can.
# Hinh xien: ve bang P(X, Y, Z), X xien len-phai = RA XA nguoi xem, Y phai, Z len (he TAY TRAI - cong B 14/11 bat loi:
#   assert cu tinh tren he nay nen tu khop ma sai). Vat li kiem bang check_F() trong he tay phai (x ve phia nguoi xem).
#   Nam cham chu U dung tren dia can, N trai S phai -> B sang phai. Khung day treo o gia rieng, canh duoi doc chieu sau
#   xuyen khe. Thuan: I HUONG VE PHIA NGUOI XEM -> luc len day huong len; luc len nam cham (DL III) huong xuong -> can
#   +1,45 g. Dao: I ra xa -> luc len day xuong, luc len nam cham huong len -> -1,45 g. Khop thuchanhtu4 (I ra khoi trang,
#   B sang phai -> F len day huong len, can +).
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

check_F((-1, 0, 0), (0, 1, 0), (0, 0, 1))      # thuan: I ve phia nguoi xem -> luc len day huong len (can +)
check_F((1, 0, 0), (0, 1, 0), (0, 0, -1))      # dao: luc len day huong xuong -> nam cham bi keo len (can -)
check_F((1, 0, 0), (0, -1, 0), (0, 0, 1))      # cau chot: dao I + doi cho hai cuc -> nhu thuan (+1,45 g)

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

# ---------------- bo thi nghiem ----------------
P = mkP(330, 470)
COPPER = (184, 115, 51)
MW, MH, MARM, MYOKE, MTIP, MT = 440, 330, 120, 100, 170, 160
DEP = (KX * MT, -KY * MT)
QM = lambda u, v: P(0, u, -v)                              # U dung tren can, N trai S phai
YW, ZC, ZS = MW / 2, -85, 120                              # day: giua khe; Z thanh gia
XW0, XW1 = -40, 200                                        # canh duoi khung (dai hon be day nam cham)
I_THUAN = (70, -75)                                        # mui ten I thuan: X giam = ve phia nguoi xem, keo ra truoc nam cham
check_F((I_THUAN[1] - I_THUAN[0], 0, 0), (0, 1, 0), (0, 0, 1))    # noi assert voi chinh mui ten ve: luc len day huong len
check_F((I_THUAN[0] - I_THUAN[1], 0, 0), (0, 1, 0), (0, 0, -1))   # dao: huong xuong
DM = 1.45                                                  # so_lieu_mau

def reading(on, sg): return sg * DM if on else 0.0
def fmt(m): return "0,00 g" if abs(m) < 1e-9 else ("+" if m > 0 else "−") + vn(abs(m)) + " g"

def src_card(d, on, sg):
    card(d, (30, 270, 430, 410), fill=WHITE, outline=NAVY, r=18, w=4)
    text(d, (230, 310), "I = 3,0 A" if on else "I = 0", 46, ORANGE if on else NOTE)
    if on: text(d, (230, 368), "I hướng ra" if sg > 0 else "I hướng vào", 44, NAVY)

def scale(d, m):
    x0, x1, z0, z1, y0, y1 = -20, MT + 30, -MH, -MH - 100, -40, MW + 40
    top = [P(x0, y0, z0), P(x0, y1, z0), P(x1, y1, z0), P(x1, y0, z0)]
    side = [P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)]
    front = [P(x0, y0, z0), P(x0, y1, z0), P(x0, y1, z1), P(x0, y0, z1)]
    d.polygon(top, fill=(241, 245, 249), outline=UM_EDGE, width=3)
    d.polygon(side, fill=(203, 213, 225), outline=UM_EDGE, width=3)
    d.polygon(front, fill=(226, 232, 240), outline=UM_EDGE, width=3)
    cx = (front[0][0] + front[1][0]) / 2; cy = (front[0][1] + front[3][1]) / 2
    d.rounded_rectangle([cx - 150, cy - 34, cx + 150, cy + 34], radius=10, fill=(15, 23, 42))
    col = (134, 239, 172) if m > 0 else ((252, 165, 165) if m < 0 else (226, 232, 240))
    text(d, (cx, cy), fmt(m), 50, col)

def rig(d, on, sg, show=2):
    m = reading(on, sg)
    scale(d, m)
    def mid(dd):
        for z in (-25, -60, -110, -145): fline(dd, P(20, MARM, z), P(20, MW - MARM, z), at=0.25)
        dd.line([P(0, YW, ZC), P(XW1, YW, ZC)], fill=COPPER, width=12)
        dd.line([P(XW1, YW, ZC), P(XW1, YW, ZS)], fill=COPPER, width=6)
    u_magnet_pil(d, QM, MW, MH, MARM, MYOKE, MTIP, DEP, mid=mid)
    d.line([P(XW0, YW, ZC), P(0, YW, ZC)], fill=COPPER, width=12)
    d.line([P(XW0, YW, ZC), P(XW0, YW, ZS)], fill=COPPER, width=6)
    d.line([P(XW0 - 30, YW, ZS), P(XW1 + 30, YW, ZS)], fill=NAVY, width=12)                # gia treo rieng
    pr = P(XW1 + 30, YW, ZS); d.line([pr, (pr[0] + 90, pr[1])], fill=NAVY, width=12)
    d.line([(pr[0] + 90, pr[1]), (pr[0] + 90, 905)], fill=NAVY, width=12)                   # chan gia (ngoai can)
    pl = P(XW0, YW, ZS); d.line([pl, (pl[0] - 60, pl[1] - 15), (430, 330)], fill=COPPER, width=4, joint="curve")
    card(d, (880, 530, 1060, 630), fill=WHITE, outline=PURPLE, r=16, w=3)          # chu thich B o vung trong
    arrow(d, (905, 580), (995, 580), PURPLE, w=7, head=22); text(d, (1028, 580), "B", 50, PURPLE)
    if on and show:                                              # mui ten I ve SAU nam cham (khong bi mat truoc che)
        a0, a1 = I_THUAN if sg > 0 else I_THUAN[::-1]
        arrow(d, P(a0, YW, ZC + 32), P(a1, YW, ZC + 32), ORANGE, w=8, head=24)
        pi = P(min(a0, a1), YW, ZC + 32); lx, ly = pi[0] - 50, pi[1] - 30
        card(d, (lx - 30, ly - 34, lx + 30, ly + 34), fill=WHITE, outline=ORANGE, r=12, w=3)
        text(d, (lx, ly), "I", 56, ORANGE)
    if on and show >= 1:
        p = P(80, YW, ZC); up = 1 if sg > 0 else -1
        arrow(d, p, (p[0], p[1] - up * 95), GREEN, w=9, head=26)
        q = (p[0] + 20, p[1] - up * 95)
        dashed(d, q, (880, 420), GREEN, w=3)
        card(d, (880, 360, 1050, 480), fill=WHITE, outline=GREEN, r=16, w=3)
        text(d, (965, 395), "Lực lên", 44, GREEN); text(d, (965, 446), "dây", 44, GREEN)
    if on and show >= 2:
        b = QM(MW / 2, MH - MYOKE / 2); dn = 1 if sg > 0 else -1
        arrow(d, (b[0], b[1] - dn * 50), (b[0], b[1] + dn * 50), RED, w=9, head=26)
        dashed(d, (b[0] - 30, b[1]), (270, 700), RED, w=3)
        card(d, (30, 640, 270, 760), fill=WHITE, outline=RED, r=16, w=3)
        text(d, (150, 675), "Lực lên", 44, RED); text(d, (150, 726), "nam châm", 44, RED)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; on = t >= M[0] + 0.7
    rig(d, on, 1); src_card(d, on, 1)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 450), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 165), "Đảo chiều dòng, vẫn 3,0 A.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "Lực lên nam châm hướng nào?", 50, INK, alpha=a)
    text(d, (W / 2, y0 + 330), "Chọn đáp án ở khung câu hỏi", 44, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 400, 940, y0 + 414], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 400, 140 + 800 * (1 - p), y0 + 414], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (can + do thi so can theo thoi gian doi CUNG moc) ----------------
def stages(sc):
    M = sc["M"]
    return dict(s1=0.6, s2=M[1], s3=M[1] + 1.4, s4=M[2] + 0.4)

def state_do(t, sc):
    s = stages(sc)
    if t < s["s1"]: return False, 1
    if t < s["s2"]: return True, 1
    if t < s["s3"]: return False, -1
    if t < s["s4"]: return True, -1
    return False, -1

def graph(d, t, sc):
    T = sc["T"]; gx0, gx1, g0, k = 170, 1000, 1250, 100
    card(d, (40, 1010, 1040, 1480), fill=WHITE, outline=LIGHT, w=3)
    text(d, (70, 1050), "Số cân (g)", 44, NAVY, anchor="lm")
    d.line([(gx0, 1100), (gx0, 1420)], fill=INK, width=3)
    d.line([(gx0, g0), (gx1, g0)], fill=INK, width=3)
    for v, s in ((DM, "+1,45"), (0, "0"), (-DM, "−1,45")):
        y = g0 - k * v; text(d, (gx0 - 14, y), s, 44, INK, anchor="rm")
        if v: dashed(d, (gx0, y), (gx1, y), LIGHT, w=2)
    pts = []
    n = int(clamp(t / T) * 300)
    for i in range(n + 1):
        tt = T * i / 300; on, sg = state_do(tt, sc)
        pts.append((gx0 + (gx1 - gx0) * tt / T, g0 - k * reading(on, sg)))
    if len(pts) > 1: d.line(pts, fill=BLUE, width=6)
    if pts: dot(d, pts[-1][0], pts[-1][1], 9, BLUE)

def s_do(img, d, t, sc):
    on, sg = state_do(t, sc)
    rig(d, on, sg, show=1); src_card(d, on, sg); graph(d, t, sc)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    rig(d, True, -1); src_card(d, True, -1)
    ka = appear(t, 0.4, 0.4); s = "ĐÁP ÁN · hướng lên"
    pw = tw(d, s, F(40)) + 56
    card(d, (W / 2 - pw / 2, 1000, W / 2 + pw / 2, 1064), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 1032), s, 40, WHITE, alpha=ka)
    kt = appear(t, M[0] + 0.8, 0.45)
    if kt <= 0: return
    card(d, (40, 1095, 1040, 1490), fill=A(WHITE, kt), outline=A(LIGHT, kt), w=3)
    text(d, (690, 1145), "Thuận", 44, NAVY, alpha=kt); text(d, (920, 1145), "Đảo", 44, NAVY, alpha=kt)
    rows = (("Lực lên dây", "lên", "xuống", GREEN), ("Lực lên nam châm", "xuống", "lên", RED),
            ("Số cân", "+1,45 g", "−1,45 g", INK))
    for j, (lab, a1, a2, col) in enumerate(rows):
        kk = kt * appear(t, M[0] + 1.0 + 0.6 * j, 0.4); y = 1240 + 95 * j
        d.line([(60, y - 48), (1020, y - 48)], fill=A(LIGHT, kk), width=2)
        text(d, (70, y), lab, 44, col, anchor="lm", alpha=kk)
        text(d, (690, y), a1, 46, INK, alpha=kk); text(d, (920, y), a2, 46, ORANGE, alpha=kk)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    rig(d, True, -1); src_card(d, True, -1)
    k0 = appear(t, 0.2, 0.4); k2 = appear(t, mk + 0.2, 0.45)
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3); y = 1010
    if a1 > 0:
        card(d, (40, y, 1040, y + 250 + 200 * k2), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(RED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Khối lượng không giảm, cân phải tăng”"
        ks = clamp((t - mk) / 0.4); f = F(44); lw = tw(d, q, f); yy = y + 170
        text(d, (W / 2, yy), q, 44, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        text(d, (W / 2, y + 280), "Cân đo lực ép nam châm", 48, ORANGE, alpha=a1 * k2)
        text(d, (W / 2, y + 370), "Bị kéo lên → ép ít hơn", 48, INK, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        for j, s in enumerate(("• F tỉ lệ với I hay với L?",)):
            kk = k3 * appear(t, M[2] + 0.2 + 0.5 * j, 0.4)
            text(d, (100, y + 200 + 105 * j), s, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    w, h, arm, yoke, tip = 300, 200, 80, 60, 100
    Qr = lambda u, v: (390 + (w - u), 905 + v)                 # doi cho hai cuc: N phai, S trai
    u_magnet_pil(d, Qr, w, h, arm, yoke, tip, (40, -24), fs=44, alpha=k)
    text(d, (850, 975), "Hai cực", 44, NAVY, alpha=k); text(d, (850, 1025), "đổi chỗ", 44, NAVY, alpha=k)
    text(d, (220, 975), "Dòng I", 44, ORANGE, alpha=k); text(d, (220, 1025), "đảo chiều", 44, ORANGE, alpha=k)

def s_end(img, d, t, sc):
    chot_box(d, t, sc, "Cân đọc lực lên nam châm: dấu đổi theo chiều I",
             "Đảo I và đổi chỗ hai cực. Cân chỉ bao nhiêu?", _end_body, "Lực lên dây hướng nào?", 1150, 1390)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    s = stages(do)
    return ([(h["t0"] + h["M"][0] + 0.7, "tap"), (h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s[k], "tap") for k in ("s1", "s2", "s3", "s4")]
            + [(da["t0"] + 0.4, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-thuchanhtu-02", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thực hành đo cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Cân dòng điện", draw=s_hook, tail=0.3, caps=[
   ("Dòng thuận: cân chỉ +1,45 g.", 3.6),
   ("Nghĩ trước khi xem tiếp.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đóng mạch, I = 3,0 A.", 3.4),
   ("Ngắt, đảo chiều dòng, đóng lại.", 4.2),
   ("Ngắt mạch: cân về 0.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Lực lên dây đổi chiều.", 3.0),
   ("Nam châm bị kéo lên: số âm.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=1.5, caps=[
   ("Đúng hay sai?", 2.5),
   ("Sai: khối lượng không đổi.", 3.4),
   ("Giới hạn thí nghiệm.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.3, caps=[
   ("Dừng video và trả lời.", 6.8)]),
])
