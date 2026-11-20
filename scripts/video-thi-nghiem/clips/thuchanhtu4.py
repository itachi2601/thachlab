# Clip: tn-l12-thuchanhtu-04 - Can dong dien: tang giam va dao chieu I
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanhtu-04.json (ghi chu JSON: "so lieu minh hoa"):
#   so_lieu_mau (I A, dm g, F mN, B T): 1 0,50 4,91 0,123 | 2 0,97 9,52 0,119 | 3 1,45 14,22 0,119 | 4 1,97 19,33 0,121 | 5 2,44 23,94 0,120
#   mo_hinh: dm_lt = 0,4893.I (g); B = 0,12 T; dung_cu: canh duoi l = 4,0 cm nam trong khe; do doc 0,4885 g/A.
#   ket_qua_ky_vong: dao chieu thi dau so can doi, do lon giu nguyen -> hang "3 A dao chieu" = -1,45 g, -14,22 mN, B 0,119.
# Du doan (3 A ra khoi trang -> +1,45 g; giu 3 A, dao chieu): dap an -1,45 g (khung web hoi A-D, clip khong ve nut - K10).
# Hinh (nhin ngang): cuc N mat trong ben trai, S ben phai -> B nam ngang tu trai sang phai trong khe. Canh duoi khung vuong
#   goc man hinh. I ra khoi trang (+z), B (+x): F = I l x B = +y -> F len (quy tac ban tay trai). Phan luc F' len nam cham
#   huong xuong -> can (da TARE) chi +. Dao chieu: F xuong, F' len, can chi -. Nam cham can bang: Q = P + F'.
# Ban 4 (20/11/2026, viec 4 KE-HOACH-CAI-TIEN-CLIP): cong --do-chu moi: chu than canh >= 56 px (ra >= 49 px), bo chu xam,
#   bo do dung cu phong x1,15 (TF), hop Q-P-F' lon o canh chuoi, canh Bay tach 4 nhip ~3 s (cot 1 A/5 A -> cong thuc + chu
#   thich l bang hinh nhin tu tren -> tinh lai B -> chua noi duoc), canh cuoi THU NGHI hoi dung ca cau_chot (khung web hoi A-D),
#   bo dong "Chon dap an o khung cau hoi" (phu de "Dung lai, tu doan"), dem nguoc bang 5 cham.
# Ban 3 (19/11/2026): cat chu <=200 tu/phut; K10 hop Du doan khong ve nut A-D.
# Ban 2 (11/11/2026): canh 'chuoi' (ban tay trai -> F len DAY; DL III -> F' len NAM CHAM; can do nam cham), N -> Q.
from engine import *

ROWS = [(1, 0.50, 4.91, 0.123), (2, 0.97, 9.52, 0.119), (3, 1.45, 14.22, 0.119), (4, 1.97, 19.33, 0.121), (5, 2.44, 23.94, 0.120)]
REV = ("3 · đảo", -1.45, -14.22, 0.119)            # suy tu hang 3 A + ket_qua_ky_vong (doi dau, giu do lon)

def vn(x, nd=2, sign=False):
    if abs(x) < 1e-9: return "0,00" if nd == 2 else "0"
    s = f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"
    return s.replace(".", ",").replace("-", "−")

def chevron(d, x, y, ang, color, s=14, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def wire(d, x, y, sgn, r=26, ring=NAVY):
    """Day vuong goc man hinh: cham = ra khoi trang, dau x = vao trong trang (ve tay, font khong co glyph)."""
    dot(d, x, y, r, WHITE, outline=NAVY); d.ellipse([x - r, y - r, x + r, y + r], outline=ring, width=6)
    if sgn > 0: dot(d, x, y, r * 0.32, NAVY)
    else:
        q = r * 0.62
        d.line([(x - q, y - q), (x + q, y + q)], fill=NAVY, width=5); d.line([(x - q, y + q), (x + q, y - q)], fill=NAVY, width=5)

def varrow(d, x, y, L, color, w=9, head=24):
    """Mui ten doc tu (x, y), L > 0 huong len, L < 0 huong xuong."""
    if abs(L) < 6: return
    arrow(d, (x, y), (x, y - L), color, w=w, head=head)

# ---------------- bo can + nam cham + khung day: toa do goc, phong x1,15 qua TF ----------------
WX, WY = 510, 540                       # day trong khe (toa do goc)
YOKE = (175, 180, 195)
TF = (1.15, -202, -93.5)                # goc x 280-1010, y 290-952 -> x 120-960, y 240-1001
def X(x): return TF[1] + TF[0] * x
def Y(y): return TF[2] + TF[0] * y
def S(v): return TF[0] * v
def R(x0, y0, x1, y1): return [X(x0), Y(y0), X(x1), Y(y1)]
def kF(I): return 30 * I                # do dai mui ten F, F' (px goc) ti le I

def rig(d, I, sgn, dm, show=2, glow=0.0):
    """show: 0 = chua ve luc, 1 = chi F len day, 2 = F len day + F' len nam cham."""
    # chan de + tru giu khung (dung rieng, khong cham can)
    d.rounded_rectangle(R(830, 930, 1010, 952), radius=8, fill=NAVY)
    d.rectangle(R(942, 296, 962, 932), fill=NAVY)
    d.rectangle(R(WX - 4, 290, 962, 308), fill=NAVY)
    d.line([(X(WX), Y(306)), (X(WX), Y(WY - 26))], fill=NAVY, width=7)
    # can dien tu
    card(d, R(280, 806, 740, 930), fill=WHITE, outline=NAVY, r=20, w=4)
    d.rounded_rectangle(R(300, 790, 720, 808), radius=6, fill=NAVY)
    if glow > 0:
        d.rounded_rectangle(R(282, 814, 594, 922), radius=18, fill=A(ORANGE, glow))
    card(d, R(296, 822, 580, 914), fill=(24, 30, 40), r=12)
    text(d, (X(438), Y(868)), f"{vn(dm, 2, sign=abs(dm) > 1e-9)} g", 60, (134, 239, 172))
    text(d, (X(662), Y(868)), "cân", 58, NAVY)
    # nam cham chu U (gong sat) + hai cuc o mat trong
    d.rectangle(R(330, 700, 690, 790), fill=YOKE)
    d.rectangle(R(330, 440, 410, 700), fill=YOKE); d.rectangle(R(610, 440, 690, 700), fill=YOKE)
    d.rectangle(R(410, 470, 440, 610), fill=RED); d.rectangle(R(580, 470, 610, 610), fill=BLUE)
    text(d, (X(370), Y(490)), "N", 60, RED); text(d, (X(650), Y(490)), "S", 60, BLUE)
    if show >= 2 and I > 0:                     # vien cam: vat chiu F' la nam cham
        U = [(330, 440), (410, 440), (410, 700), (610, 700), (610, 440), (690, 440), (690, 790), (330, 790), (330, 440)]
        d.line([(X(a), Y(b)) for a, b in U], fill=ORANGE, width=6)
    # duong suc trong khe: tu N sang S
    for y in (490, 590, 540):
        if y == 540:
            d.line([(X(442), Y(y)), (X(WX - 28), Y(y))], fill=PURPLE, width=4)
            d.line([(X(WX + 28), Y(y)), (X(578), Y(y))], fill=PURPLE, width=4)
            chevron(d, X(470), Y(y), 0, PURPLE, s=16); chevron(d, X(572), Y(y), 0, PURPLE, s=16)
        else:
            d.line([(X(442), Y(y)), (X(578), Y(y))], fill=PURPLE, width=4); chevron(d, X(515), Y(y), 0, PURPLE, s=16)
    text(d, (X(470), Y(655)), "B", 60, PURPLE)
    wire(d, X(WX), Y(WY), sgn, r=S(26), ring=GREEN if (show >= 1 and I > 0) else NAVY)
    L = sgn * kF(I)
    if I > 0 and show >= 1:                     # luc tu F len day (xanh); nhan F ra ngoai khe, co duong dan
        varrow(d, X(WX + 44), Y(WY), S(L), GREEN, w=10, head=26)
        d.line([(X(WX + 50), Y(WY - L / 2)), (X(560), Y(372))], fill=GREEN, width=4)
        text(d, (X(568), Y(360)), "F", 66, GREEN, anchor="lm")
    if I > 0 and show >= 2:                     # phan luc F' len nam cham (cam): cung do dai, nguoc chieu
        fy = 625 if L > 0 else 775
        varrow(d, X(650), Y(fy), -S(L), ORANGE, w=12, head=28)
        text(d, (X(700), Y(fy + L / 2)), "F′", 66, ORANGE, anchor="lm")

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; a = appear(t, M[1] - 0.2, 0.5)
    rig(d, 3, 1, 0.0 if a <= 0 else 1.45, show=0)
    if a <= 0: return
    y0 = 1025 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 570), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 180), "3 A ra khỏi trang: +1,45 g", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 280), "Đảo chiều dòng: cân chỉ?", 60, INK, alpha=a)   # K10: khong ve nut A-D
    # dem nguoc 5 cham, moi cham tat sau ~0,8 s (dong thoi giu hinh khong dung yen)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    n_off = 0 if t < tc else min(5, int((t - tc) / ((tend - tc) / 5)) + 1)
    for j in range(5):
        x = W / 2 + (j - 2) * 140
        dot(d, x, y0 + 440, 40, A(LIGHT, a) if j >= 5 - n_off else A(PURPLE, a))

# ---------------- canh 2: Chuoi 3 buoc - luc nao len vat nao ----------------
def chain_at(sc):
    M = sc["M"]; return (0.5, M[1] + 0.1, M[1] + 2.3)

def fbd(d, kP, kQ):
    """So do luc len nam cham (lon, ~1/2 khung): P xuong, F' xuong (phan luc), Q can do len; Q = P + F'."""
    if kP <= 0: return
    card(d, (40, 1020, 600, 1680), fill=A(WHITE, kP), outline=A(ORANGE, kP), w=5, r=26)
    cx, top, bot = 320, 1250, 1350
    d.rounded_rectangle([cx - 110, top, cx + 110, bot], radius=12, fill=A(YOKE, kP))
    varrow(d, cx - 60, bot, -170, A(NAVY, kP), w=13, head=32)
    text(d, (cx - 95, bot + 110), "P", 76, NAVY, anchor="rm", alpha=kP)
    varrow(d, cx + 60, bot, -100, A(ORANGE, kP), w=13, head=32)
    text(d, (cx + 95, bot + 70), "F′", 76, ORANGE, anchor="lm", alpha=kP)
    if kQ > 0:
        varrow(d, cx, top, 190, A(TEAL, kQ), w=13, head=32)
        text(d, (cx - 40, top - 100), "Q", 76, TEAL, anchor="rm", alpha=kQ)
        text(d, (cx, 1605), "Q = P + F′", 68, INK, alpha=kQ)

def s_chuoi(img, d, t, sc):
    at = chain_at(sc)
    rig(d, 3, 1, 1.45, show=2 if t >= at[1] else 1)
    fbd(d, appear(t, at[1], 0.45), appear(t, at[2], 0.45))
    # (dong mang mui ten, mui ten len/xuong)
    rows = ((("F tác dụng", "lên dây"), GREEN, 1, 1), (("F′ ép", "nam châm"), ORANGE, 0, -1), (("Q: cân đỡ", "nam châm"), TEAL, None, 0))
    for j, (ls, col, ia, up) in enumerate(rows):
        k = appear(t, at[j], 0.45)
        if k <= 0: continue
        yy = 1090 + j * 205
        dot(d, 650, yy, 34, A(col, k)); text(d, (650, yy), str(j + 1), 56, WHITE, alpha=k)
        for i, s in enumerate(ls):
            text(d, (700, yy + i * 72), s, 60, col, anchor="lm", alpha=k)
        if ia is not None:
            xa = 700 + tw(d, ls[ia], F(60)) + 36; ya = yy + ia * 72
            varrow(d, xa, ya + (34 if up > 0 else -34), up * 68, A(col, k), w=10, head=24)

# ---------------- canh 3: Tien hanh ----------------
def steps(sc):
    M = sc["M"]
    st = [0.5 + 0.6 * k for k in range(1, 6)]            # moc tang I = 1..5 A
    back3, rev = M[1] + 0.3, M[1] + 1.4
    return st, back3, rev

def state_do(t, sc):
    st, back3, rev = steps(sc)
    if t >= rev: return 3, -1, -1.45, 5
    if t >= back3: return 3, 1, 1.45, 2
    n = sum(1 for s in st if t >= s)
    return n, 1, (ROWS[n - 1][1] if n else 0.0), n - 1

COLS = ((190, "I (A)"), (530, "Δm (g)"), (860, "B (T)"))      # bo cot F' (mN) cho thoang
def table(d, y0, ks, cur, rh=72):
    rows = ROWS + [REV]
    card(d, (40, y0, 1040, y0 + 84 + rh * 6 + 34), fill=WHITE, outline=NAVY, w=3)
    for x, s in COLS: text(d, (x, y0 + 44), s, 62, NAVY)
    d.line([(70, y0 + 84), (1010, y0 + 84)], fill=NAVY, width=3)
    for j, (r, k) in enumerate(zip(rows, ks)):
        if k <= 0: continue
        yy = y0 + 84 + rh * (j + 0.5) + 6; neg = r[1] < 0
        if j == cur:
            d.rounded_rectangle([60, yy - rh / 2 + 3, 1020, yy + rh / 2 - 3], radius=14, fill=A((255, 237, 213), k))
        col = RED if neg else INK
        text(d, (190, yy), str(r[0]), 60, col, alpha=k)
        text(d, (530, yy), vn(r[1], 2, sign=neg), 60, col, alpha=k)
        text(d, (860, yy), vn(r[3], 3), 60, col, alpha=k)

def s_do(img, d, t, sc):
    I, sgn, dm, cur = state_do(t, sc)
    st, back3, rev = steps(sc)
    if rev - 0.25 <= t < rev + 0.25:            # mui ten doi chieu muot: co ve 0 roi dai ra phia kia
        kk = abs(t - rev) / 0.25; Ieff = 3 * kk; sgn_eff = 1 if t < rev else -1
    else: Ieff, sgn_eff = I, sgn
    rig(d, Ieff, sgn_eff, dm, show=2)
    # thanh I + chieu
    card(d, (40, 1015, 1040, 1105), fill=WHITE, outline=NAVY, w=4, r=24)
    text(d, (70, 1060), f"I = {I} A", 58, INK, anchor="lm")
    d.rounded_rectangle([270, 1048, 470, 1072], radius=12, fill=LIGHT)
    if I > 0: d.rounded_rectangle([270, 1048, 270 + 200 * I / 5, 1072], radius=12, fill=ORANGE)
    wire(d, 530, 1060, sgn, r=26)
    text(d, (575, 1060), "ra khỏi trang" if sgn > 0 else "vào trong trang", 56, INK if sgn > 0 else RED, anchor="lm")
    ks = [appear(t, st[j], 0.3) for j in range(5)] + [1.0 if t >= rev else 0.0]
    table(d, 1120, ks, cur)

# ---------------- canh 4: Dap an + rut ra ----------------
def mini(d, cx, sgn, k):
    """Khe nam cham thu nho: F len day va F' len nam cham, so can."""
    if k <= 0: return
    card(d, (cx - 245, 240, cx + 245, 900), fill=A(WHITE, k), outline=A(GREEN if sgn > 0 else RED, k), w=5, r=28)
    text(d, (cx, 300), "I ra" if sgn > 0 else "I vào", 60, INK, alpha=k)
    d.rectangle([cx - 135, 380, cx - 95, 690], fill=YOKE); d.rectangle([cx + 95, 380, cx + 135, 690], fill=YOKE)
    d.rectangle([cx - 135, 690, cx + 135, 740], fill=YOKE)
    d.rectangle([cx - 95, 410, cx - 74, 570], fill=RED); d.rectangle([cx + 74, 410, cx + 95, 570], fill=BLUE)
    text(d, (cx - 172, 470), "N", 60, RED, alpha=k); text(d, (cx + 172, 470), "S", 60, BLUE, alpha=k)
    for y in (440, 540):
        d.line([(cx - 72, y), (cx + 72, y)], fill=PURPLE, width=4); chevron(d, cx + 46, y, 0, PURPLE)
    gy = 490
    wire(d, cx, gy, sgn, r=24)
    L = sgn * 110
    varrow(d, cx, gy - 24 if L > 0 else gy + 24, L, GREEN, w=10, head=24)
    text(d, (cx + 28, 372), "F", 68, GREEN, anchor="lm", alpha=k) if L > 0 else text(d, (cx - 30, 640), "F", 68, GREEN, anchor="rm", alpha=k)
    fy = 585 if L > 0 else 715
    varrow(d, cx + 115, fy, -L * 0.9, ORANGE, w=10, head=24)
    text(d, (cx + 152, 650 if L > 0 else 620), "F′", 68, ORANGE, anchor="lm", alpha=k)
    card(d, (cx - 150, 785, cx + 150, 865), fill=(24, 30, 40), r=12)
    text(d, (cx, 825), "+1,45 g" if sgn > 0 else "−1,45 g", 60, (134, 239, 172) if sgn > 0 else (252, 165, 165), alpha=k)

def plot(d, box, k_line, k):
    x0, y0, x1, y1 = box
    X_ = lambda I: x0 + I / 5.4 * (x1 - x0)
    Y_ = lambda m: y1 - (m + 2.3) / (2.8 + 2.3) * (y1 - y0)
    for m in (-2, -1, 1, 2):
        d.line([(x0, Y_(m)), (x1, Y_(m))], fill=LIGHT, width=3)
        text(d, (x0 - 16, Y_(m)), vn(m, 0, sign=m < 0), 62, INK, anchor="rm", alpha=k)
    text(d, (x0 - 16, Y_(0)), "0", 62, INK, anchor="rm", alpha=k)
    d.line([(x0, y1), (x0, y0)], fill=NAVY, width=5); chevron(d, x0, y0, -math.pi / 2, NAVY, s=18, w=5)
    d.line([(x0, Y_(0)), (x1 + 14, Y_(0))], fill=NAVY, width=5); chevron(d, x1 + 14, Y_(0), 0, NAVY, s=18, w=5)
    text(d, (x0 + 22, y0 + 12), "Δm (g)", 62, INK, anchor="lm", alpha=k)
    text(d, (x1 + 10, Y_(0) - 50), "I (A)", 62, INK, anchor="rm", alpha=k)
    for I in range(1, 6):
        d.line([(X_(I), Y_(0) - 10), (X_(I), Y_(0) + 10)], fill=NAVY, width=4)
        text(d, (X_(I), Y_(0) + 46), str(I), 62, INK, alpha=k)
    if k_line > 0:
        d.line([(X_(0), Y_(0)), (X_(0) + (X_(5.3) - X_(0)) * k_line, Y_(0.4885 * 5.3 * k_line))], fill=A(GREEN, 0.85), width=6)
    for I, m, _, _ in ROWS: dot(d, X_(I), Y_(m), 15, BLUE, outline=WHITE)
    # diem dao chieu: dung I = 3, Δm = -1,45 (giua moc -1 va -2), duong dong toi truc
    yr = Y_(-1.45)
    for xx in range(int(x0), int(X_(3)) - 20, 28): d.line([(xx, yr), (xx + 14, yr)], fill=A(RED, 0.7 * k), width=3)
    d.line([(X_(3), Y_(0)), (X_(3), yr)], fill=A(RED, 0.5 * k), width=3)
    dot(d, X_(3), yr, 17, RED, outline=WHITE)
    text(d, (X_(3) + 32, yr - 34), "đảo chiều", 58, RED, anchor="lm", alpha=k)
    text(d, (X_(3) + 32, yr + 34), "−1,45 g", 58, RED, anchor="lm", alpha=k)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    mini(d, 290, 1, 1.0); mini(d, 790, -1, appear(t, 0.05, 0.3))
    ka = appear(t, M[0] + 0.1, 0.4)
    if ka > 0:
        pw = tw(d, "ĐÁP ÁN: −1,45 g", F(56)) + 60
        card(d, (W / 2 - pw / 2, 912, W / 2 + pw / 2, 982), fill=A(NAVY, ka), r=35)
        text(d, (W / 2, 947), "ĐÁP ÁN: −1,45 g", 56, WHITE, alpha=ka)
    k2 = appear(t, M[1] - 0.3, 0.4)
    if k2 > 0:
        card(d, (40, 998, 1040, 1680), fill=A(WHITE, k2), outline=A(NAVY, k2), w=3)
        plot(d, (240, 1070, 950, 1630), appear(t, M[1], 1.0), k2)

# ---------------- canh 5: Bay (3 nhip ~3 s, moi nhip mot phu de) ----------------
from PIL import ImageFont as _IF
_FL = {}
def FL(size):
    """l nghieng (Georgia Bold Italic, da kiem co glyph 'l') de khong lan voi I trong phong sans."""
    if size not in _FL: _FL[size] = _IF.truetype("/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf", size)
    return _FL[size]

def seq(d, x, y, parts, alpha=1.0, center=False):
    """Ve noi tiep cac doan (chu, font, mau) tren mot dong; center=True thi x la tam."""
    ws = [tw(d, s, f) + (4 if f in _FL.values() else 0) for s, f, c in parts]
    if center: x -= sum(ws) / 2
    for (s, f, c), w in zip(parts, ws):
        dtext(d, (x, y), s, f, c, alpha, anchor="lm"); x += w

def topview(d, k):
    """Nhin tu tren xuong khe: hai cuc N, S; doan day trong khe (xanh) + doan kich thuoc l hai vach chan."""
    d.rectangle([110, 1030, 190, 1200], fill=A(RED, k)); d.rectangle([300, 1030, 380, 1200], fill=A(BLUE, k))
    text(d, (150, 1115), "N", 58, WHITE, alpha=k); text(d, (340, 1115), "S", 58, WHITE, alpha=k)
    d.line([(245, 990), (245, 1235)], fill=A(GRAY, k), width=8)
    d.line([(245, 1030), (245, 1200)], fill=A(GREEN, k), width=12)
    # duong gióng tu hai dau doan day ra doan kich thuoc (x = 420), hai vach chan
    for yy in (1030, 1200):
        for xx in range(255, 420, 22): d.line([(xx, yy), (xx + 11, yy)], fill=A(GREEN, k), width=4)
        d.line([(402, yy), (438, yy)], fill=A(GREEN, k), width=7)
    d.line([(420, 1030), (420, 1200)], fill=A(GREEN, k), width=7)
    dtext(d, (446, 1115), "l", FL(76), GREEN, k, anchor="lm")

def s_bay(img, d, t, sc):
    M = sc["M"]; b1, b2, b3 = (m - 0.1 for m in M)
    k1 = appear(t, b1, 0.4); k2 = appear(t, b2, 0.4); k3 = appear(t, b3, 0.4)
    # nhip 1: BAY + hai cot 1 A / 5 A, cot Δm cao gap 5
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 326), fill=A(RED, k1), r=38)
    text(d, (W / 2, 288), "BẪY", 56, WHITE, alpha=k1)
    text(d, (W / 2, 390), "I tăng 5 lần, B tăng?", 62, INK, alpha=k1)
    if k3 > 0:
        pw2 = tw(d, "SAI", F(56)) + 50
        card(d, (1030 - pw2, 250, 1030, 326), fill=A(RED, k3), r=38)
        text(d, (1030 - pw2 / 2, 288), "SAI", 56, WHITE, alpha=k3)
    base = 790
    for cx, (I, m, _, _), side in ((300, ROWS[0], 0), (800, ROWS[4], 1)):
        h = m * 115
        d.rounded_rectangle([cx - 70, base - h * k1, cx + 70, base], radius=10, fill=A(ORANGE, k1))
        if side: text(d, (cx - 95, base - h + 40), f"Δm = {vn(m)} g", 58, INK, anchor="rm", alpha=k1)   # nhan ben trai cot cao
        else: text(d, (cx, base - h - 44), f"Δm = {vn(m)} g", 58, INK, alpha=k1)
        text(d, (cx, base + 46), f"{I} A", 60, NAVY, alpha=k1)
    d.line([(120, base), (960, base)], fill=A(NAVY, k1), width=5)
    # nhip 2: cong thuc + chu thich l bang hinh
    if k2 > 0:
        card(d, (40, 898, 1040, 1248), fill=A(WHITE, k2), outline=A(NAVY, k2), w=4)
        seq(d, W / 2, 950, [("B = Δm·g / (I·", F(64), INK), ("l", FL(70), INK), (")", F(64), INK)], k2, center=True)
        topview(d, k2)
        seq(d, 520, 1075, [("l", FL(66), GREEN), (": dây trong khe", F(60), GREEN)], k2)
        seq(d, 520, 1165, [("l", FL(66), INK), (" = 4,0 cm", F(60), INK)], k2)
    # nhip 3: tinh lai B cho tung cot
    if k3 > 0:
        card(d, (40, 1260, 1040, 1680), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1335), "1 A: B = 0,123 T", 60, INK, alpha=k3)
        text(d, (W / 2, 1425), "5 A: B = 0,120 T", 60, INK, alpha=k3)
        text(d, (W / 2, 1565), "B không đổi theo I", 64, GREEN, alpha=k3)

# ---------------- canh 6: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    lines = ("• Từ trường rò mép khe", "• Góc khác 90°", "• Số liệu minh hoạ")
    for j, s in enumerate(lines):
        text(d, (100, 470 + j * 250), s, 62, INK, anchor="lm", alpha=kb)
    # dau hoi lon truoc khi hien gach (giu hinh khong dung yen > 2 s)
    text(d, (W / 2, 800), "?", 260, NAVY, alpha=k * (1 - kb))

# ---------------- canh 7: THU NGHI (dung ca cau_chot cua khung) ----------------
DARK_OR = (181, 71, 8)                         # #B54708: chu cam tren nen sang >= 4,5:1
def s_end(img, d, t, sc):
    kq = appear(t, 2.6, 0.4)                    # sau ~2 s: vien cam + dau ? chi vao so can (giu hinh khong dung yen)
    rig(d, 3, 1, 1.45, show=0)
    if kq > 0:
        d.rounded_rectangle(R(268, 794, 752, 942), radius=24, outline=A(ORANGE, kq), width=12)
        text(d, (X(800), Y(868)), "?", 120, DARK_OR, alpha=kq)
    k = appear(t, 0.3, 0.5)
    if k <= 0: return
    card(d, (50, 1025, 1030, 1600), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 1050, W / 2 + pw / 2, 1130), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 1090), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 1250), "Dây không chạm cân.", 64, INK, alpha=k)
    text(d, (W / 2, 1360), "Sao cân vẫn tăng?", 64, DARK_OR, alpha=k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, ch, do, da, b, g, e = (sc[k] for k in ("hook", "chuoi", "do", "dapan", "bay", "gioi", "end"))
    st, back3, rev = steps(do)
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(ch["t0"] + a, "tap") for a in chain_at(ch)]
            + [(do["t0"] + s, "tick") for s in st]
            + [(do["t0"] + rev, "tap"), (da["t0"] + da["M"][0] + 0.1, "ding"),
               (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"), (g["t0"] + 2.4, "tap"),
               (e["t0"] + 0.3, "open")])

CLIP = dict(id="tn-l12-thuchanhtu-04", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thực hành đo cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Cân dòng điện", draw=s_hook, tail=0.3, caps=[
   "Cân đã về 0.",
   ("Dừng lại, tự đoán.", 4.2)]),
 dict(key="chuoi", title="Lực nào lên vật nào?", draw=s_chuoi, tail=0.3, caps=[
   "Bàn tay trái: F lên dây.",
   ("Định luật III: F′ ngược F.", 4.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Tăng I từ 1 A đến 5 A.", 3.6),
   ("Về 3 A, rồi đảo chiều.", 3.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Đảo chiều: cân đổi dấu.", 3.0),
   ("Δm tỉ lệ thuận với I.", 2.9)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.1),
   ("Công thức tính B.", 3.1),
   ("Tính lại B từng cột.", 3.2)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Còn chưa xét gì?", 5.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự đoán.", 3.8)]),
])
