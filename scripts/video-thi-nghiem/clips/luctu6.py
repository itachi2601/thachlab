# Clip: tn-l12-luctu-06 - Hai la nhom song song mang dong dien
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-luctu-06.json (so_lieu_mau, "so lieu minh hoa"):
#   la dai 50 cm, cach 1,0 cm; (I1, I2) = (5, 0) dung yen | (5, 5) cung chieu hut | (5, 5) nguoc chieu day.
#   Ca tu suy cau chot (ghi_chu kho): I1 = 4 A len, I2 = 8 A xuong -> B1 = 0,8e-4 T, F = 3,2e-4 N moi la, DAY
#   (so 3,2 KHONG hien tren man; khung web hoi A-D).
# Ban 2 (21/11/2026, viec 4 lo 20, cong --do-chu moi): danh quan niem sai "cung chieu nhu dien tich cung dau -> day".
#   Du doan: "electron hai la cung dau, cung chay xuong" -> hut hay day? (bai da noi quy tac "cung chieu hut" va
#   Bam xem giai ca dong huong len -> Du doan phai qua mot buoc: electron chay xuong = dong huong len, cung chieu).
#   K10 khong ve nut; dem nguoc 5 cham. Bay: hai o canh nhau "dien tich cung dau: day" | "dong cung chieu: hut",
#   phu de "La khong tich dien." (luc dien bang 0, chi con luc tu). Chot: 4 A len / 8 A xuong, hut hay day, luc moi la.
# Vat li (kiem bang tich co huong o duoi). Hinh nhin truc dien: x sang phai, y len, z huong ve nguoi xem.
#   B1 tai la 2 ~ I1 x r^ (r^ = +x tu la 1 sang la 2); luc len la 2 ~ I2 x B1; luc len la 1 = - luc len la 2 (DL III).
#   Cung chieu len: B1 = -z (vao trong trang), luc len la 2 = -x (ve phia la 1) -> HUT.
#   Electron chay xuong <=> dong huong len (dien tich am).
#   Hinh nhin tu tren xuong: dong huong len = huong ve nguoi nhin (cham trong tron), duong suc la 1 nguoc chieu kim dong ho.
# Toa do mp4 = 65 + 0,88.x (x canh), y mp4 = 285 + 0,88.(y - 200). Chu than canh ve >= 56 px (ra >= 49 px).
from engine import *

def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def force2(s1, s2):
    """Chieu (dau x) luc len la 2; s1, s2 = +1 dong huong len, -1 huong xuong, 0 khong co dong."""
    B1 = cross((0, s1, 0), (1, 0, 0))
    return cross((0, s2, 0), B1)[0]
assert cross((0, 1, 0), (1, 0, 0)) == (0, 0, -1)          # B1 vao trong trang
assert force2(1, 1) < 0 and force2(1, -1) > 0 and force2(1, 0) == 0 and force2(-1, -1) < 0
assert force2(1, -1) > 0                                   # cau chot: 4 A len, 8 A xuong -> day
assert abs(2e-7 * 4 * 8 * 0.5 / 0.01 - 3.2e-4) < 1e-12     # F cau chot (khong hien)

FOIL = (150, 158, 176)
COP = (90, 96, 112)
X1, X2, YT, YB = 440, 640, 312, 900          # hai la (nhin truc dien), dau tren / duoi giu chat
DMAX = 34                                     # do cong lon nhat (px)

def sym(d, x, y, kind, r=26, color=NAVY, w=5):
    """Ve tay: 'o' = dong huong ve nguoi xem, 'x' = huong ra xa (font thieu glyph)."""
    dot(d, x, y, r, WHITE, outline=color); d.ellipse([x - r, y - r, x + r, y + r], outline=color, width=w)
    if kind == "o": dot(d, x, y, r * 0.3, color)
    else:
        q = r * 0.6
        d.line([(x - q, y - q), (x + q, y + q)], fill=color, width=w); d.line([(x - q, y + q), (x + q, y - q)], fill=color, width=w)

def eball(d, x, y, r=18, color=BLUE):
    """Electron: tron trang vien xanh, dau tru ve bang net (khong dung chu)."""
    dot(d, x, y, r, WHITE); d.ellipse([x - r, y - r, x + r, y + r], outline=color, width=4)
    d.line([(x - r * 0.55, y), (x + r * 0.55, y)], fill=color, width=5)

def plus(d, x, y, s, color, w=6):
    d.line([(x - s, y), (x + s, y)], fill=color, width=w); d.line([(x, y - s), (x, y + s)], fill=color, width=w)

def chevron(d, x, y, ang, color, s=16, w=5):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def dashed_circle(d, cx, cy, r, color, w=4, n=56):
    for i in range(n):
        if i % 2: continue
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        d.arc([cx - r, cy - r, cx + r, cy + r], math.degrees(a0), math.degrees(a1), fill=color, width=w)

def strip(d, x0, dx):
    pts = [(x0 + dx * math.sin(math.pi * (y - YT) / (YB - YT)), y) for y in range(YT, YB + 1, 12)]
    d.line(pts, fill=FOIL, width=14, joint="curve")

def loop(d, xs, xw, I, s):
    """Vong kin cua mot la: day tren/duoi ra xa toi day ve xw; ampe ke + nguon tren day ve.
    s = +1: dong trong la huong len -> tren day ve huong xuong; cuc + cua nguon o duoi."""
    d.line([(xs, 330), (xw, 330), (xw, 880), (xs, 880)], fill=COP, width=5)
    dot(d, xw, 470, 46, WHITE, outline=NAVY); text(d, (xw, 470), "A", 56, NAVY)
    side = -1 if xw < xs else 1
    text(d, (xw + side * 58, 470), f"{I:g} A", 56, INK, anchor="rm" if side < 0 else "lm")
    yb = 720
    d.rectangle([xw - 26, yb - 34, xw + 26, yb + 34], fill=BG)
    lo, sh = (yb + 12, yb - 12) if s >= 0 else (yb - 12, yb + 12)
    d.line([(xw - 44, lo), (xw + 44, lo)], fill=NAVY, width=6)          # ban dai: cuc +
    d.line([(xw - 22, sh), (xw + 22, sh)], fill=NAVY, width=10)         # ban ngan: cuc -
    yp, ym = (yb + 40, yb - 40) if s >= 0 else (yb - 40, yb + 40)
    xs_ = xw + side * 70
    plus(d, xs_, yp, 14, RED); d.line([(xs_ - 14, ym), (xs_ + 14, ym)], fill=NAVY, width=6)
    # khoa K: dong khi co dong (I > 0), mo khi I = 0
    d.rectangle([xw - 8, 588, xw + 8, 632], fill=BG)
    dot(d, xw, 590, 7, NAVY); dot(d, xw, 630, 7, NAVY)
    if I > 0: d.line([(xw, 590), (xw, 630)], fill=NAVY, width=6)
    else: d.line([(xw, 630), (xw - side * 30, 596)], fill=NAVY, width=6)

def front(d, I1, s1, I2, s2, k=1.0, arrows=True, plan=False):
    """Hinh truc dien. k: 0..1 muc cong theo luc tu that (tinh tu force2)."""
    d.rectangle([330, 290, 750, YT], fill=NAVY); d.rectangle([330, YB, 750, YB + 22], fill=NAVY)
    loop(d, X1, 200, 0 if plan else I1, s1); loop(d, X2, 880, 0 if plan else I2, s2 if s2 else 1)
    f2 = force2(s1 if I1 else 0, s2 if I2 else 0)
    dx2 = DMAX * k * (1 if f2 > 0 else -1 if f2 < 0 else 0)
    strip(d, X1, -dx2); strip(d, X2, dx2)                               # DL III: la 1 lech nguoc la 2
    if arrows:
        xa1, xa2 = X1 - 0.92 * dx2, X2 + 0.92 * dx2
        if I1: arrow(d, (xa1, 690 if s1 > 0 else 540), (xa1, 540 if s1 > 0 else 690), ORANGE, w=8, head=24)
        text(d, (xa1 - 30, 615), "I1", 58, ORANGE, anchor="rm")
        if I2: arrow(d, (xa2, 690 if s2 > 0 else 540), (xa2, 540 if s2 > 0 else 690), ORANGE, w=8, head=24)
        text(d, (xa2 + 30, 615), "I2" if I2 else "I2 = 0", 58, ORANGE, anchor="lm")
    text(d, (X1 - 20, 966), "lá 1", 58, NAVY); text(d, (X2 + 20, 966), "lá 2", 58, NAVY)
    # vach kich thuoc tren gia treo
    for x in (X1, X2): d.line([(x, 236), (x, 286)], fill=NAVY, width=4)
    arrow(d, (X1 + 4, 258), (X2 - 4, 258), NAVY, w=4, head=14); arrow(d, (X2 - 4, 258), (X1 + 4, 258), NAVY, w=4, head=14)
    text(d, (X2 + 22, 258), "1,0 cm", 56, NAVY, anchor="lm")

# ---------------- hinh nhin tu tren xuong ----------------
WY = 880
WA, WB = (400, WY), (700, WY)
def top(d, s1, s2, kB=1.0, kF2=1.0, kF1=1.0, cx=(400, 700)):
    xa, xb = cx; r = xb - xa
    if kB > 0:
        dashed_circle(d, xa, WY, r, A(PURPLE, kB), w=5)
        for ang in (90, 180, 270):
            a = math.radians(ang); x, y = xa + r * math.cos(a), WY - r * math.sin(a)
            chevron(d, x, y, -(a + math.pi / 2) * s1, A(PURPLE, kB))
        B1 = cross((0, s1, 0), (1, 0, 0))            # (x, y, z) -> tren man nhin tu tren: x -> x, z -> xuong
        yb = WY + 140 * B1[2]
        arrow(d, (xb, WY - 32 * (1 if B1[2] < 0 else -1)), (xb, yb), A(PURPLE, kB), w=8, head=24)
        text(d, (xb + 36, yb + 10), "B1", 60, PURPLE, anchor="lm", alpha=kB)
    for x, kk in ((xb, kF2), (xa, kF1)):                 # quang xanh nhat: la dang xet luc (doi hinh ro moi nhip)
        if kk > 0: dot(d, x, WY, 78, A((220, 245, 228), kk)); d.ellipse([x - 78, WY - 78, x + 78, WY + 78], outline=A(GREEN, kk), width=5)
    sym(d, xa, WY, "o" if s1 > 0 else "x", 30, ORANGE)
    sym(d, xb, WY, "o" if s2 > 0 else "x", 30, ORANGE)
    text(d, (xa - 92, WY), "lá 1", 58, NAVY, anchor="rm"); text(d, (xb + 92, WY), "lá 2", 58, NAVY, anchor="lm")
    f2 = force2(s1, s2); L = 110
    if kF2 > 0:
        x0 = xb - 34 * (1 if f2 < 0 else -1)
        arrow(d, (x0, WY), (x0 + L * (1 if f2 > 0 else -1), WY), A(GREEN, kF2), w=13, head=30)
        text(d, (x0 + L / 2 * (1 if f2 > 0 else -1), WY + 120), "F2", 60, GREEN, alpha=kF2)
    if kF1 > 0:
        x0 = xa + 34 * (1 if f2 < 0 else -1)
        arrow(d, (x0, WY), (x0 - L * (1 if f2 > 0 else -1), WY), A(GREEN, kF1), w=13, head=30)
        text(d, (x0 - L / 2 * (1 if f2 > 0 else -1), WY + 120), "F1", 60, GREEN, alpha=kF1)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; front(d, 5, 1, 5, 1, k=0, arrows=False, plan=True)
    # Khoa con MO, ampe ke 0 A: electron dung yen trong kim loai (co san); chieu chay SE CO khi dong khoa ve bang
    # mui ten NET DUT, chi hien cung the "Dong khoa: ..." (dong khoa that thi la phai cong ngay -> lo dap an).
    ke = appear(t, 1.2, 0.5)
    if ke > 0:
        for x in (X1, X2):
            for y in (470, 600, 730): eball(d, x, y, 19, A(BLUE, ke))
    ka = appear(t, M[1] - 0.2, 0.5)
    if ka > 0:
        for xa in (X1 - 62, X2 + 62):
            for y in range(500, 680, 36): d.line([(xa, y), (xa, y + 20)], fill=A(BLUE, ka), width=8)
            arrow(d, (xa, 690), (xa, 722), A(BLUE, ka), w=8, head=26)
        text(d, (X1 - 100, 610), "e⁻", 60, BLUE, anchor="rm", alpha=ka)
        text(d, (X2 + 100, 610), "e⁻", 60, BLUE, anchor="lm", alpha=ka)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 175), "Đóng khoá: êlectron hai lá", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 255), "cùng dấu, cùng chạy xuống.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 360), "Hai lá hút hay đẩy nhau?", 60, INK, alpha=a)   # K10: khong ve nut A-D
    # dem nguoc 5 cham (>= 70 px, trong vung y 200-1580)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    n_off = 0 if t < tc else min(5, int((t - tc) / ((tend - tc) / 5)) + 1)
    for j in range(5):
        x = W / 2 + (j - 2) * 140
        dot(d, x, y0 + 490, 38, A(LIGHT, a) if j >= 5 - n_off else A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
ROWS = (("5", "0", "đứng yên"), ("5", "5 cùng chiều", "hút"), ("5", "5 ngược chiều", "đẩy"))
def stages(sc):
    M = sc["M"]; return (M[0], M[1] + 0.1, M[2] + 0.1)

def state_do(t, sc):
    """(I2, s2, k cong, so hang) dong bo: ampe ke, mui ten I2, do cong, bang."""
    st = stages(sc)
    if t >= st[2]:
        u = t - st[2]; k = abs(1 - 2 * clamp(u / 1.0)) if u < 0.5 else clamp((u - 0.5) / 0.6)
        return 5, (1 if u < 0.5 else -1), k, (3 if u >= 1.1 else 2)
    if t >= st[1]: return 5, 1, clamp((t - st[1]) / 0.6), (2 if t >= st[1] + 0.6 else 1)
    return 0, 1, 0.0, 1

COLX = ((150, "I1 (A)"), (420, "I2 (A)"), (835, "Hiện tượng"))
def table(d, y0, n):
    rh = 86
    card(d, (40, y0, 1040, y0 + 96 + rh * 3 + 20), fill=WHITE, outline=NAVY, w=3)
    for x, s in COLX: text(d, (x, y0 + 50), s, 56, NAVY)
    d.line([(70, y0 + 96), (1010, y0 + 96)], fill=NAVY, width=3)
    for j, r in enumerate(ROWS[:n]):
        yy = y0 + 96 + rh * (j + 0.5) + 6
        for (x, _), s in zip(COLX, r):
            col = INK if x < 700 else (GREEN if s == "hút" else RED if s == "đẩy" else INK)
            text(d, (x, yy), s, 58, col)

def s_do(img, d, t, sc):
    I2, s2, k, n = state_do(t, sc)
    front(d, 5, 1, I2, s2, k=k)
    table(d, 1060, n)

# ---------------- canh 3: Dap an + co che (nhin tu tren) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.3, 0.4)
    s = "ĐÁP ÁN: hút nhau"
    pw = tw(d, s, F(58)) + 64
    card(d, (W / 2 - pw / 2, 236, W / 2 + pw / 2, 316), fill=A(NAVY, ka), r=40)
    text(d, (W / 2, 276), s, 58, WHITE, alpha=ka)
    if ka > 0:                                                   # chu giai ky hieu, mot lan
        sym(d, 230, 400, "o", 28, A(ORANGE, ka))
        text(d, (276, 400), ": I hướng về phía em", 58, INK, anchor="lm", alpha=ka)
    top(d, 1, 1, kB=appear(t, M[0] + 0.5, 0.45), kF2=appear(t, M[1] + 0.2, 0.45), kF1=appear(t, M[2] + 0.2, 0.45))

# ---------------- canh 4: Bay (dien tich cung dau vs dong cung chieu) + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] - 0.1, 0.3); k2 = appear(t, M[1] - 0.1, 0.3); k3 = appear(t, M[2] - 0.1, 0.3)
    pw = tw(d, "BẪY", F(58)) + 60
    card(d, (W / 2 - pw / 2, 236, W / 2 + pw / 2, 316), fill=A(RED, k1), r=40)
    text(d, (W / 2, 276), "BẪY", 58, WHITE, alpha=k1)
    # o trai: hai dien tich am cung dau -> day
    if k1 > 0:
        card(d, (40, 350, 505, 1000), fill=A(WHITE, k1), outline=A(RED, k1), w=5)
        text(d, (272, 430), "điện tích", 58, INK, alpha=k1)
        text(d, (272, 505), "cùng dấu", 58, INK, alpha=k1)
        for x in (190, 355):
            dot(d, x, 690, 40, A(WHITE, k1)); d.ellipse([x - 40, 650, x + 40, 730], outline=A(BLUE, k1), width=6)
            d.line([(x - 22, 690), (x + 22, 690)], fill=A(BLUE, k1), width=7)
        arrow(d, (140, 690), (70, 690), A(RED, k1), w=9, head=24); arrow(d, (405, 690), (475, 690), A(RED, k1), w=9, head=24)
        text(d, (272, 880), "đẩy", 72, RED, alpha=k1)
    text(d, (540, 690), "≠", 72, NAVY, alpha=k2)
    # o phai: hai dong cung chieu (nhin tu tren) -> hut
    if k2 > 0:
        card(d, (575, 350, 1040, 1000), fill=A(WHITE, k2), outline=A(GREEN, k2), w=5)
        text(d, (808, 430), "dòng điện", 58, INK, alpha=k2)
        text(d, (808, 505), "cùng chiều", 58, INK, alpha=k2)
        for x in (640, 976): sym(d, x, 690, "o", 34, A(ORANGE, k2), w=6)
        arrow(d, (684, 690), (796, 690), A(GREEN, k2), w=12, head=32); arrow(d, (932, 690), (820, 690), A(GREEN, k2), w=12, head=32)
        text(d, (808, 880), "hút", 72, GREEN, alpha=k2)
    if k3 > 0:
        card(d, (40, 1060, 1040, 1420), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, 1150), "Chưa nói được", 60, NAVY, alpha=k3)
        text(d, (W / 2, 1300), "Chưa so được độ lớn", 60, INK, alpha=k3)

# ---------------- canh 5: Chot + THU NGHI (cau_chot khung web) ----------------
DARK_OR = (181, 71, 8)                         # #B54708: chu cam tren nen sang >= 4,5:1
def s_end(img, d, t, sc):
    k0 = appear(t, 0.2, 0.5)
    card(d, (50, 240, 1030, 440), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 340), "Mỗi lá trong từ trường lá kia", 58, GREEN, alpha=k0)
    k1 = appear(t, 2.8, 0.5)
    if k1 <= 0: return
    card(d, (50, 490, 1030, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 520, W / 2 + pw / 2, 600), fill=A(DARK_OR, k1), r=40)
    text(d, (W / 2, 560), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    xa, xb, ya, yb = 420, 660, 730, 1090
    for x in (xa, xb): d.line([(x, 720), (x, 1100)], fill=A(FOIL, k1), width=14)
    arrow(d, (xa, 990), (xa, 830), A(ORANGE, k1), w=8, head=24)            # la 1: len
    arrow(d, (xb, 830), (xb, 990), A(ORANGE, k1), w=8, head=24)            # la 2: xuong
    text(d, (xa - 40, 910), "I1 = 4 A", 58, ORANGE, anchor="rm", alpha=k1)
    text(d, (xb + 40, 910), "I2 = 8 A", 58, ORANGE, anchor="lm", alpha=k1)
    # kich thuoc: cach 1,0 cm (tren), dai 50 cm (ben phai)
    arrow(d, (xa + 4, 690), (xb - 4, 690), A(NAVY, k1), w=4, head=14); arrow(d, (xb - 4, 690), (xa + 4, 690), A(NAVY, k1), w=4, head=14)
    text(d, (W / 2, 645), "1,0 cm", 56, NAVY, alpha=k1)
    for yy in (720, 1100): d.line([(950, yy), (990, yy)], fill=A(NAVY, k1), width=4)
    arrow(d, (970, 724), (970, 1096), A(NAVY, k1), w=4, head=14); arrow(d, (970, 1096), (970, 724), A(NAVY, k1), w=4, head=14)
    text(d, (945, 790), "50 cm", 56, NAVY, anchor="rm", alpha=k1)
    text(d, (W / 2, 1200), "Hút hay đẩy? Lực mỗi lá?", 60, INK, alpha=k1)
    kh = appear(t, 5.6, 0.5)
    if kh > 0:
        card(d, (150, 1290, 930, 1420), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1355), "Gợi ý: tính B1 trước", 58, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    st = stages(do)
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tap") for s in st[1:]]
            + [(da["t0"] + 0.3, "ding")] + [(da["t0"] + da["M"][j] + dt, "tap") for j, dt in ((0, 0.5), (1, 0.2), (2, 0.2))]
            + [(b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][1] - 0.1, "tap"), (b["t0"] + b["M"][2] - 0.1, "tap"),
               (e["t0"] + 2.8, "open")])

CLIP = dict(id="tn-l12-luctu-06", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Lực từ · Cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai lá nhôm song song", draw=s_hook, tail=0.3, caps=[
   ("Mỗi lá một mạch riêng.", 3.0),
   ("Dừng lại, tự đoán.", 6.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Chỉ lá 1 có dòng.", 3.0),
   ("Lá 2: cùng chiều.", 3.0),
   ("Lá 2: ngược chiều.", 3.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Nắm tay phải: B1 tại lá 2.", 3.8),
   ("Bàn tay trái: F2 về lá 1.", 3.8),
   ("Định luật III: F1 = F2.", 3.0)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Cùng chiều như cùng dấu?", 3.4),
   ("Lá không tích điện.", 3.4),
   ("Giới hạn thí nghiệm.", 2.5)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự tính.", 7.6)]),
])
