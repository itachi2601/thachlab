# Clip: tn-l12-thuchanhtu-04 - Can dong dien: tang giam va dao chieu I (ban 1, 28/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanhtu-04.json (ghi chu JSON: "so lieu minh hoa"):
#   so_lieu_mau (I A, dm g, F mN, B T): 1 0,50 4,91 0,123 | 2 0,97 9,52 0,119 | 3 1,45 14,22 0,119 | 4 1,97 19,33 0,121 | 5 2,44 23,94 0,120
#   mo_hinh: dm_lt = 0,4893.I (g) -> "moi nac them co 0,49 g"; B = 0,12 T, l = 4,0 cm; do doc 0,4885 g/A.
#   ket_qua_ky_vong: dao chieu thi dau so can doi, do lon giu nguyen -> hang "3 A dao chieu" = -1,45 g, -14,22 mN, B 0,119.
# Du doan (3 A ra khoi trang -> +1,45 g; giu 3 A, dao chieu): A +2,90 g = 2 x 1,45 (tuong "dao chieu cong them");
#   B +1,45 g (tuong luc khong phu thuoc chieu) ; C 0,00 g (hien_tuong_hay_sai: "dao chieu lam can ve 0") ; D -1,45 g (dung).
# Hinh (nhin ngang): cuc N mat trong ben trai, S ben phai -> B nam ngang tu trai sang phai trong khe. Canh duoi khung vuong
#   goc man hinh. I ra khoi trang (+z), B (+x): F = I l x B = +y -> F len (quy tac ban tay trai). Phan luc F' len nam cham
#   huong xuong -> can (da TARE) chi +. Dao chieu: F xuong, F' len, can chi -. Nam cham can bang: N = P + F' (hoac P - F').
from engine import *

ROWS = [(1, 0.50, 4.91, 0.123), (2, 0.97, 9.52, 0.119), (3, 1.45, 14.22, 0.119), (4, 1.97, 19.33, 0.121), (5, 2.44, 23.94, 0.120)]
REV = ("3 · đảo", -1.45, -14.22, 0.119)            # suy tu hang 3 A + ket_qua_ky_vong (doi dau, giu do lon)
NOTE = (70, 75, 95)

def vn(x, nd=2, sign=False):
    if abs(x) < 1e-9: return "0,00" if nd == 2 else "0"
    s = f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"
    return s.replace(".", ",").replace("-", "−")

def chevron(d, x, y, ang, color, s=14, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def wire(d, x, y, sgn, r=26):
    """Day vuong goc man hinh: cham = ra khoi trang, dau x = vao trong trang (ve tay, font khong co glyph)."""
    dot(d, x, y, r, WHITE, outline=NAVY); d.ellipse([x - r, y - r, x + r, y + r], outline=NAVY, width=5)
    if sgn > 0: dot(d, x, y, 8, NAVY)
    else:
        q = r * 0.62
        d.line([(x - q, y - q), (x + q, y + q)], fill=NAVY, width=5); d.line([(x - q, y + q), (x + q, y - q)], fill=NAVY, width=5)

def varrow(d, x, y, L, color, w=9, head=24):
    """Mui ten doc tu (x, y), L > 0 huong len, L < 0 huong xuong."""
    if abs(L) < 6: return
    arrow(d, (x, y), (x, y - L), color, w=w, head=head)

# ---------------- bo can + nam cham + khung day (khung 1080 x 1920) ----------------
WX, WY = 510, 540                       # day trong khe
YOKE = (175, 180, 195)
def kF(I): return 24 * I                # do dai mui ten F, F' (px) ti le I

def rig(d, I, sgn, dm, fbd=True, label=True):
    # chan de + tru giu khung (dung rieng, khong cham can)
    d.rounded_rectangle([830, 930, 1010, 952], radius=8, fill=NAVY)
    d.rectangle([942, 296, 962, 932], fill=NAVY)
    d.rectangle([WX - 4, 290, 962, 308], fill=NAVY)
    d.line([(WX, 306), (WX, WY - 26)], fill=NAVY, width=6)
    if label: text(d, (952, 260), "giá giữ khung", 32, NOTE, bold=False, anchor="rm")
    # can dien tu
    card(d, (280, 806, 740, 930), fill=WHITE, outline=NAVY, r=20, w=4)
    d.rounded_rectangle([300, 790, 720, 808], radius=6, fill=NAVY)
    card(d, (300, 828, 520, 908), fill=(24, 30, 40), r=12)
    text(d, (410, 868), f"{vn(dm, 2, sign=abs(dm) > 1e-9)} g", 44, (134, 239, 172))
    text(d, (690, 868), "cân", 34, NAVY)
    # nam cham chu U (gong sat) + hai cuc o mat trong
    d.rectangle([330, 700, 690, 790], fill=YOKE)
    d.rectangle([330, 440, 410, 700], fill=YOKE); d.rectangle([610, 440, 690, 700], fill=YOKE)
    d.rectangle([410, 470, 440, 610], fill=RED); d.rectangle([580, 470, 610, 610], fill=BLUE)
    text(d, (370, 540), "N", 44, RED); text(d, (650, 540), "S", 44, BLUE)
    # duong suc trong khe: tu N sang S
    for y in (490, 590, 540):
        if y == 540:
            d.line([(442, y), (WX - 28, y)], fill=PURPLE, width=4); d.line([(WX + 28, y), (578, y)], fill=PURPLE, width=4)
            chevron(d, 470, y, 0, PURPLE); chevron(d, 572, y, 0, PURPLE)
        else:
            d.line([(442, y), (578, y)], fill=PURPLE, width=4); chevron(d, 515, y, 0, PURPLE)
    text(d, (476, 640), "B", 36, PURPLE)
    wire(d, WX, WY, sgn)
    L = sgn * kF(I)
    # luc tu F len day (xanh) va phan luc F' len nam cham (cam): cung do dai, nguoc chieu
    if I > 0:
        fx = WX + 40                            # canh thanh giu, goc o ngang day
        varrow(d, fx, WY, L, GREEN)
        text(d, (WX - 16, WY - L / 2), "F", 40, GREEN, anchor="rm")
        # F' goc o nam cham, nam tron trong nam cham (khong vao o so can)
        fy = 620 if L > 0 else 772
        varrow(d, 590, fy, -L, ORANGE)
        text(d, (572, 655 if L > 0 else 740), "F′", 40, ORANGE, anchor="rm")
    if fbd: free_body(d, I, sgn)

def free_body(d, I, sgn):
    """Luc len nam cham: P xuong, F' (phan luc), N do dia can day len = P + F' (da quy uoc chieu xuong la +)."""
    cx, cy, P = 150, 610, 90
    card(d, (52, 268, 252, 950), fill=WHITE, outline=LIGHT, r=22, w=3)
    text(d, (152, 310), "Lực lên", 32, NAVY); text(d, (152, 350), "nam châm", 32, NAVY)
    Fp = sgn * 18 * I                   # > 0: F' xuong
    N = P + Fp
    d.rounded_rectangle([cx - 46, cy - 26, cx + 46, cy + 26], radius=8, fill=YOKE)
    xn, xf = cx - 22, cx + 28           # N, P o cot trai; F' cot phai, nhan hai phia -> khong chong
    varrow(d, xn, cy - 26, N, TEAL, w=8, head=20)
    text(d, (xn - 14, cy - 26 - N / 2), "N", 36, TEAL, anchor="rm")
    varrow(d, xn, cy + 26, -P, NAVY, w=8, head=20)
    text(d, (xn - 14, cy + 26 + P / 2), "P", 36, NAVY, anchor="rm")
    if I > 0:
        y0 = cy + 26 if Fp > 0 else cy - 26
        varrow(d, xf, y0, -Fp, ORANGE, w=8, head=20)
        text(d, (xf + 14, y0 + Fp / 2), "F′", 36, ORANGE, anchor="lm")
    text(d, (152, 830), "N = P ± F′", 32, NOTE, bold=False)
    text(d, (152, 872), "không theo", 32, NOTE, bold=False); text(d, (152, 910), "tỉ lệ", 32, NOTE, bold=False)

# ---------------- bang so lieu ----------------
COLS = ((150, "I (A)"), (395, "Δm (g)"), (640, "F (mN)"), (880, "B (T)"))
def table(d, y0, rows, ks, hl=0.0, minh_hoa=True, rh=64):
    h = 76 + rh * len(ROWS + [REV])
    card(d, (40, y0, 1040, y0 + h + 20), fill=WHITE, outline=LIGHT, w=3)
    if hl > 0:
        d.rounded_rectangle([790, y0 + 12, 970, y0 + h + 8], radius=18, fill=A((255, 237, 213), hl), outline=A(ORANGE, hl), width=4)
    for x, s in COLS: text(d, (x, y0 + 44), s, 34, NOTE, bold=False)
    d.line([(70, y0 + 78), (1010, y0 + 78)], fill=LIGHT, width=3)
    for j, (r, k) in enumerate(zip(rows, ks)):
        if k <= 0: continue
        yy = y0 + 78 + rh * (j + 0.5) + 4; neg = r[1] < 0
        col = RED if neg else INK
        text(d, (150, yy), str(r[0]), 38, col, alpha=k)
        text(d, (395, yy), vn(r[1], 2, sign=neg), 38, col, alpha=k)
        text(d, (640, yy), vn(r[2], 2, sign=neg), 38, col, alpha=k)
        text(d, (880, yy), vn(r[3], 3), 38, col, alpha=k)
    if minh_hoa: text(d, (1020, y0 + h + 48), "Số liệu minh hoạ", 32, NOTE, bold=False, anchor="rm")
    return h

# ---------------- canh 1: Du doan ----------------
OPTS = ("+2,90 g", "+1,45 g", "0,00 g", "−1,45 g")

def s_hook(img, d, t, sc):
    rig(d, 3, 1, 1.45)
    M = sc["M"]; a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0:
        k = appear(t, 0.5, 0.5)
        card(d, (60, 1010, 1020, 1300), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
        text(d, (W / 2, 1080), "Cân đã TARE (về 0) khi I = 0.", 40, INK, alpha=k)
        text(d, (W / 2, 1150), "Đoạn dây trong khe dài l = 4,0 cm", 38, NOTE, bold=False, alpha=k)
        text(d, (W / 2, 1220), "I = 3 A, chạy ra khỏi trang", 40, INK, alpha=k)
        return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 610), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    text(d, (W / 2, y0 + 136), "Cân đã TARE (về 0) khi I = 0.", 40, INK, alpha=a)
    text(d, (W / 2, y0 + 188), "3 A ra khỏi trang: cân chỉ +1,45 g.", 40, INK, alpha=a)
    text(d, (W / 2, y0 + 240), "Giữ 3 A, đảo chiều dòng. Cân chỉ…", 40, INK, alpha=a)
    for j, s in enumerate(OPTS):
        k = appear(t, M[1] + 0.15 * j, 0.4); yy = y0 + 312 + j * 66
        d.rounded_rectangle([90, yy - 29, 990, yy + 29], radius=29, outline=A(LIGHT, k), width=3)
        text(d, (130, yy), f"{'ABCD'[j]}.   {s}", 38, NAVY, bold=False, anchor="lm", alpha=k)
    tc, tend = M[1] + 0.8, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 580, 940, y0 + 592], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 580, 140 + 800 * (1 - p), y0 + 592], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def steps(sc):
    M = sc["M"]
    st = [0.7 + 1.15 * k for k in range(1, 6)]           # moc tang I = 1..5 A
    back3, rev = M[2] + 0.3, M[2] + 1.6
    return st, back3, rev

def state_do(t, sc):
    st, back3, rev = steps(sc)
    if t >= rev: return 3, -1, -1.45, 6
    if t >= back3: return 3, 1, 1.45, 5
    n = sum(1 for s in st if t >= s)
    return n, 1, (ROWS[n - 1][1] if n else 0.0), n

def s_do(img, d, t, sc):
    I, sgn, dm, nrow = state_do(t, sc)
    st, back3, rev = steps(sc)
    # mui ten doi chieu muot: co ve 0 roi dai ra phia kia
    if rev - 0.25 <= t < rev + 0.25:
        kk = abs(t - rev) / 0.25; Ieff = 3 * kk; sgn_eff = 1 if t < rev else -1
    else: Ieff, sgn_eff = I, sgn
    rig(d, Ieff, sgn_eff, dm, label=not (rev - 0.2 <= t < rev + 1.6))
    # thanh I + chieu
    card(d, (40, 975, 1040, 1075), fill=WHITE, outline=NAVY, w=4, r=24)
    text(d, (80, 1025), f"I = {I} A", 46, INK, anchor="lm")
    d.rounded_rectangle([280, 1012, 600, 1038], radius=13, fill=LIGHT)
    if I > 0: d.rounded_rectangle([280, 1012, 280 + 320 * I / 5, 1038], radius=13, fill=ORANGE)
    wire(d, 660, 1025, sgn, r=22)
    text(d, (696, 1025), "ra khỏi trang" if sgn > 0 else "vào trong trang", 34, INK if sgn > 0 else RED, anchor="lm")
    rows = ROWS + [REV]
    ks = []
    for j in range(6):
        at = st[j] if j < 5 else rev
        ks.append(appear(t, at, 0.35))
    table(d, 1095, rows, ks)
    if rev - 0.2 <= t < rev + 1.6:
        wdt = tw(d, "ĐẢO CHIỀU", F(32)) + 44
        card(d, (1020 - wdt, 236, 1020, 284), fill=RED, r=24); text(d, (1020 - wdt / 2, 260), "ĐẢO CHIỀU", 32, WHITE)

# ---------------- canh 3: Dap an + rut ra ----------------
def mini(d, cx, sgn, k):
    """Khe nam cham thu nho: F len day va F' len nam cham, so can."""
    if k <= 0: return
    x0 = cx - 235
    card(d, (x0, 240, x0 + 470, 820), fill=A(WHITE, k), outline=A(GREEN if sgn > 0 else RED, k), w=4, r=28)
    text(d, (cx, 286), "I ra khỏi trang" if sgn > 0 else "I vào trong trang", 36, INK, alpha=k)
    gy = 470
    d.rectangle([cx - 130, 380, cx - 90, 620], fill=YOKE); d.rectangle([cx + 90, 380, cx + 130, 620], fill=YOKE)
    d.rectangle([cx - 130, 620, cx + 130, 665], fill=YOKE)
    d.rectangle([cx - 90, 405, cx - 70, 535], fill=RED); d.rectangle([cx + 70, 405, cx + 90, 535], fill=BLUE)
    text(d, (cx - 110, 360), "N", 34, RED); text(d, (cx + 110, 360), "S", 34, BLUE)
    for y in (425, 515):
        d.line([(cx - 68, y), (cx + 68, y)], fill=PURPLE, width=4); chevron(d, cx + 40, y, 0, PURPLE)
    wire(d, cx, gy, sgn, r=22)
    L = sgn * 96
    varrow(d, cx, gy - 24 if L > 0 else gy + 24, L, GREEN, w=8, head=20)
    text(d, (cx - 26, gy - 24 - L / 2 if L > 0 else gy + 24 - L / 2), "F", 36, GREEN, anchor="rm")
    fy = 560 if L > 0 else 660
    varrow(d, cx + 52, fy, -L, ORANGE, w=8, head=20)
    text(d, (cx + 70, fy + L / 2), "F′", 36, ORANGE, anchor="lm")
    text(d, (cx, 770), "+1,45 g" if sgn > 0 else "−1,45 g", 48, GREEN if sgn > 0 else RED, alpha=k)

def plot(d, box, k_line, k_rev, alpha=1.0):
    x0, y0, x1, y1 = box
    X = lambda I: x0 + I / 5.4 * (x1 - x0)
    Y = lambda m: y1 - (m + 1.7) / (2.8 + 1.7) * (y1 - y0)
    for m in (-1, 1, 2):
        d.line([(x0, Y(m)), (x1, Y(m))], fill=LIGHT, width=2)
        text(d, (x0 - 14, Y(m)), vn(m, 0, sign=m < 0), 32, NOTE, bold=False, anchor="rm")
    text(d, (x0 - 14, Y(0)), "0", 32, NOTE, bold=False, anchor="rm")
    d.line([(x0, y1), (x0, y0)], fill=NAVY, width=4); chevron(d, x0, y0, -math.pi / 2, NAVY, s=16)
    d.line([(x0, Y(0)), (x1 + 14, Y(0))], fill=NAVY, width=4); chevron(d, x1 + 14, Y(0), 0, NAVY, s=16)
    text(d, (x0 + 18, y0 + 6), "Δm (g)", 34, INK, anchor="lm")
    text(d, (x1 + 10, Y(0) - 34), "I (A)", 34, INK, anchor="rm")
    for I in range(1, 6):
        d.line([(X(I), Y(0) - 8), (X(I), Y(0) + 8)], fill=NAVY, width=3)
        text(d, (X(I), Y(0) + 32), str(I), 32, NOTE, bold=False)
    if k_line > 0:
        d.line([(X(0), Y(0)), (X(0) + (X(5.3) - X(0)) * k_line, Y(0.4885 * 5.3 * k_line))], fill=A(GREEN, 0.8), width=5)
    for I, m, _, _ in ROWS: dot(d, X(I), Y(m), 12, BLUE, outline=WHITE)
    if k_rev > 0:
        dot(d, X(3), Y(-1.45), 13, A(RED, k_rev), outline=WHITE)
        text(d, (X(3) + 28, Y(-1.45)), "đảo chiều: −1,45 g", 40, RED, anchor="lm", alpha=k_rev)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, M[0] + 0.1, 0.4)
    mini(d, 295, 1, 1.0); mini(d, 785, -1, appear(t, 0.1, 0.4))
    if ka > 0:
        pw = tw(d, "ĐÁP ÁN D", F(36)) + 52
        card(d, (W / 2 - pw / 2, 832, W / 2 + pw / 2, 892), fill=A(NAVY, ka), r=30)
        text(d, (W / 2, 862), "ĐÁP ÁN D", 36, WHITE, alpha=ka)
    k1 = appear(t, M[1] + 0.1, 0.45)
    if k1 > 0:
        text(d, (W / 2, 940), "Đảo I: F và F′ đổi chiều, độ lớn giữ nguyên", 36, INK, alpha=k1)
    k2 = appear(t, M[2] - 0.6, 0.5)
    card(d, (40, 985, 1040, 1660), fill=A(WHITE, k2), outline=A(LIGHT, k2), w=3)
    if k2 > 0:
        plot(d, (190, 1040, 960, 1560), appear(t, M[2] - 0.3, 1.0), k2)
        text(d, (W / 2, 1612), "Số liệu minh hoạ · F = B·I·l", 34, NOTE, bold=False, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    table(d, 240, ROWS + [REV], [1.0] * 6, hl=appear(t, 0.2, 0.4))
    k1 = appear(t, 0.2, 0.4); k3 = appear(t, M[2] - 0.1, 0.45); a1 = k1 * (1 - k3)
    y = 820
    if a1 > 0:
        card(d, (40, y, 1040, y + 820), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y + 30, W / 2 + pw / 2, y + 94), fill=A(RED, a1), r=32)
        text(d, (W / 2, y + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“I tăng 5 lần thì B cũng tăng”"
        ks = clamp((t - M[1]) / 0.4); f = F(44); lw = tw(d, q, f); yy = y + 180
        text(d, (W / 2, yy), q, 44, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        k0 = a1 * appear(t, 0.5, 0.45)          # nua duoi co hinh ngay tu dau: ly do HS de tin bay
        text(d, (W / 2, y + 285), "1 A: Δm = 0,50 g   ·   5 A: Δm = 2,44 g", 40, NAVY, alpha=k0)
        kq = k0 * (1 - appear(t, M[1] - 0.3, 0.3))
        text(d, (W / 2, y + 345), "Δm tăng gần 5 lần…", 40, NOTE, bold=False, alpha=kq)
        text(d, (W / 2, y + 470), "Vậy B cũng tăng 5 lần?", 46, INK, alpha=kq)
        text(d, (W / 2, y + 620), "B = ?", 88, ORANGE, alpha=kq)
        k2 = a1 * appear(t, M[1], 0.45)
        text(d, (W / 2, y + 420), "B = Δm·g / (I·l)", 56, INK, alpha=k2)
        text(d, (W / 2, y + 520), "1 A → 0,123 T   ·   5 A → 0,120 T", 40, ORANGE, alpha=k2)
        ctext(d, y + 635, "Δm và I cùng tăng, tỉ số giữ nguyên: B ≈ 0,12 T là của khe nam châm.", 40, INK, maxw=880, alpha=k2)
        text(d, (W / 2, y + 750), "Lệch 0,119–0,123 T: sai số đo nhỏ", 36, NOTE, bold=False, alpha=k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 820), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 70), "Thí nghiệm chưa nói được", 44, NAVY, alpha=k3)
        lines = (("• Từ trường ở mép khe", "  (đã bỏ qua từ trường rò)"),
                 ("• Dây không vuông góc B", "  (chỉ làm ở góc 90°)"),
                 ("• Số đo thật", "  (đây là số liệu minh hoạ)"))
        for j, (l1, l2) in enumerate(lines):
            kk = k3 * appear(t, M[2] + 0.2 + 0.4 * j, 0.4); yy = y + 210 + j * 200
            text(d, (100, yy), l1, 44, INK, anchor="lm", alpha=kk)
            text(d, (100, yy + 62), l2, 38, NOTE, bold=False, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    text(d, (W / 2, 1110), "Biết: 3 A ra khỏi trang → +1,45 g", 40, NOTE, bold=False, alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Lực từ tỉ lệ với I; B là của khe nam châm",
             "Cân chỉ −0,97 g. Dòng điện bao nhiêu ampe, chạy chiều nào?", None, body=_end_body)
    kh = appear(t, M[0] + 2.6, 0.5)                 # goi y hien sau, de HS tu nghi truoc
    if kh > 0:
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1350, "Gợi ý", 36, MUTED, bold=False, alpha=kh)
        ctext(d, 1440, "Δm tỉ lệ với I. Dấu trừ nghĩa là gì?", 42, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    st, back3, rev = steps(do)
    return ([(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tick") for s in st]
            + [(do["t0"] + rev, "tap"), (da["t0"] + da["M"][0] + 0.1, "ding"),
               (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-thuchanhtu-04", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thực hành đo cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Cân dòng điện", draw=s_hook, tail=0.3, caps=[
   ("Nam châm trên cân, dây nằm trong khe.", 2.6),
   ("Giữ 3 A, đảo chiều: cân chỉ bao nhiêu?", 2.8),
   ("Dừng vài giây, chọn A, B, C hay D.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Tăng I từng nấc, từ 1 A đến 5 A.", 3.2),
   ("Số cân, mũi tên F tăng đều theo I.", 3.4),
   ("Về 3 A rồi đảo chiều dòng điện.", 2.8),
   ("Cân chỉ −1,45 g, F quay xuống.", 2.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Đảo chiều: −1,45 g. Đáp án D.", 2.8),
   ("Lực đổi chiều, độ lớn giữ nguyên.", 2.8),
   ("Δm tỉ lệ thuận với I: F = BIl.", 2.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: I tăng thì B tính ra cũng tăng?", 2.8),
   ("Sai: B = Δmg/(Il) luôn cỡ 0,12 T.", 3.0),
   ("Thí nghiệm này chưa nói được gì?", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Thử nghĩ: cân chỉ −0,97 g thì I ra sao?", 4.4)]),
])
