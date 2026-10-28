# Clip: tn-l12-tutruong-04 - Do cam ung tu theo khoang cach bang cam bien tu truong (dien thoai)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-tutruong-04.json (so_lieu_mau, tham_so, sai_so_thuong_gap).
# Ban 1 (28/10/2026): mau boyle/antoanpx1 (dung cu + bang + do thi), tieng bao cues.
from engine import *

ROWS = [(2, (999, 1001, 1000), 1000, "1000"), (4, (128, 130, 129), 129, "125"), (6, (47, 48, 49), 48, "37,0"),
        (8, (33, 34, 35), 34, "15,6"), (10, (30, 31, 32), 31, "8,0")]   # so_lieu_mau: d (cm), 3 lan doc, TB B, B_lt (µT)
B_TD, SAI_SO = 30, 3                                                      # tham_so: B Trai Dat (µT), sai_so_do B (µT)
BLT = [1000, 125, 37.0, 15.6, 8.0]                                         # cot B_lt, chi de ve cot (nhan in tu ROWS)
# Lua chon nhieu (hop Du doan) suy tu 1000 µT o 2 cm: 1000/2 = 500, 1000/4 = 250, 1000/8 = 125, khong doi = 1000.

# ---------------- dung cu: nam cham tru + thuoc + dien thoai (cam bien tren truc) ----------------
AY = 770                    # truc nam cham (nam ngang)
NX = 170                    # mat cuc Bac (d = 0)
PXC = 77                    # px moi cm
def X(dd): return NX + dd * PXC
RY = 905                    # duong thuoc

def magnet_side(d, xn, cy, w=44, h=110, lbl=True, size=34, bg=False, side=False):
    """Nam cham tru nhin ngang: mat N ben phai (do), mat S ben trai (xanh). Truc tu hoa nam ngang."""
    d.rectangle([xn - w, cy - h / 2, xn - w / 2, cy + h / 2], fill=BLUE)
    d.rectangle([xn - w / 2, cy - h / 2, xn, cy + h / 2], fill=RED)
    d.rectangle([xn - w, cy - h / 2, xn, cy + h / 2], outline=NAVY, width=4)
    if lbl and side:          # nhan hai ben (nam cham nho): S ben trai, N ben phai, nen trang
        for x, s_, col in ((xn - w - 26, "S", BLUE), (xn + 26, "N", RED)):
            d.rounded_rectangle([x - 22, cy - h / 2 - 46, x + 22, cy - h / 2 + 2], radius=10, fill=WHITE)
            text(d, (x, cy - h / 2 - 22), s_, size, col)
        return
    if lbl:
        if bg: d.rounded_rectangle([xn - w - 14, cy - h / 2 - 54, xn + 14, cy - h / 2 - 8], radius=10, fill=WHITE)
        text(d, (xn - 3 * w / 4, cy - h / 2 - 30), "S", size, BLUE)
        text(d, (xn - w / 4, cy - h / 2 - 30), "N", size, RED)

def phone(d, x, cy):
    """Dien thoai dung, cam bien (cham cam) dat dung tren truc o mep trai."""
    d.rounded_rectangle([x - 14, cy - 40, x + 66, cy + 120], radius=16, fill=(60, 66, 90), outline=NAVY, width=4)
    d.rounded_rectangle([x - 4, cy - 28, x + 56, cy + 104], radius=8, fill=(190, 205, 230))
    dot(d, x, cy, 9, ORANGE, WHITE)

def rig(d, t, dd, reading, sub, moving=False):
    # truc (net dut mo)
    for xx in range(NX + 8, 1010, 26): d.line([(xx, AY), (xx + 12, AY)], fill=A(GRAY, 0.7), width=3)
    # thuoc 0-10 cm, goc o mat N
    d.line([(NX, RY), (X(10) + 20, RY)], fill=NAVY, width=6)
    for k in range(11):
        x = X(k); L = 22 if k % 2 == 0 else 13
        d.line([(x, RY), (x, RY + L)], fill=NAVY, width=4)
        if k % 2 == 0: text(d, (x, RY + 50), str(k), 34, MUTED, bold=False)
    text(d, (X(10) + 40, RY + 50), "cm", 34, MUTED, bold=False, anchor="lm")
    # gia + nam cham
    d.rectangle([NX - 30, AY + 55, NX - 14, RY], fill=GRAY)
    magnet_side(d, NX, AY)
    # dien thoai tren gia
    x = X(dd)
    d.rectangle([x + 18, AY + 120, x + 34, RY], fill=GRAY)
    phone(d, x, AY)
    text(d, (x + 26, AY - 80), "cảm biến", 34, ORANGE)
    # khoang cach
    card(d, (60, 270, 500, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (280, 320), "từ cực N", 36, MUTED, bold=False)
    text(d, (280, 430), "d = ···" if moving else f"d = {dd:.0f} cm", 66, BLUE)
    # man hinh ung dung
    card(d, (560, 270, 1020, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (790, 320), "Ứng dụng", 36, MUTED, bold=False)
    d.rounded_rectangle([610, 360, 970, 470], radius=16, fill=NAVY)
    text(d, (790, 415), str(reading), 66, (134, 239, 172))
    text(d, (790, 512), sub, 34, MUTED, bold=False)

# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. 500 µT", "B. 250 µT", "C. 125 µT", "D. 1000 µT")
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, 2, ROWS[0][2], "µT")
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 990, 1020, 1600), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1040), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1130, f"2 cm: máy đọc {ROWS[0][2]} µT.\nRa 4 cm (xa gấp đôi): đọc khoảng?", 44, INK, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.15); y = 1258 + i * 76
        card(d, (110, y - 33, 970, y + 33), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=20, w=4)
        text(d, (150, y), s, 44, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1566, 940, 1580], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1566, 140 + 800 * (1 - q), 1580], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: doi dien thoai ra xa dan, ghi bang ----------------
MOVE = 0.6
def row_at(i, sc):
    M = sc["M"]
    return [M[0] + 0.5, M[0] + 1.9, M[1] + 0.3, M[1] + 1.2, M[1] + 2.1][i]

def do_state(t, sc):
    """(d dang ve, chi so dong da toi hoac -1 khi dang di chuyen)"""
    dd, prev = 2.0, 2.0
    for i in range(5):
        a = row_at(i, sc)
        if i == 0:
            if t < a: return 2.0, 0
        else:
            if t < a - MOVE: return dd, i - 1
            if t < a: return lerp(prev, ROWS[i][0], ease((t - (a - MOVE)) / MOVE)), -1
        dd = prev = ROWS[i][0]
    return dd, 4

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    dd, at = do_state(t, sc)
    if at < 0: rig(d, t, dd, "···", "đang dời", moving=True)
    else: rig(d, t, dd, ROWS[at][1][int(t * 3) % 3], "µT")
    card(d, (60, 990, 1020, 1600), fill=WHITE, outline=NAVY, w=4)
    text(d, (W / 2, 1036), "minh hoạ", 36, PURPLE)
    xs = [170, 510, 865]
    for x, c in zip(xs, ["d (cm)", "3 lần đọc", "TB (µT)"]): text(d, (x, 1100), c, 36, MUTED)
    d.line([(90, 1134), (990, 1134)], fill=LIGHT, width=4)
    hl = appear(t, M[1] - 0.1)
    for i, (dm, three, avg, _) in enumerate(ROWS):
        a = appear(t, row_at(i, sc), 0.35); y = 1180 + i * 74
        if a <= 0: continue
        if hl > 0 and i in (0, 1): d.rounded_rectangle([80, y - 32, 1000, y + 32], radius=14, fill=A((220, 252, 231), hl))
        elif i == at: d.rounded_rectangle([80, y - 32, 1000, y + 32], radius=14, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), str(dm), 42, BLUE, alpha=a)
        text(d, (xs[1], y), " · ".join(map(str, three)), 36, INK, bold=False, alpha=a)
        text(d, (xs[2], y), str(avg), 44, GREEN, alpha=appear(t, row_at(i, sc) + 0.3, 0.35))

# ---------------- canh 3: dap an C + do thi B(d) + so voi mo hinh 1/d^3 ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = back((t - 0.2) / 0.5) if t > 0.2 else 0
    card(d, (60, 250, 1020, 350), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 300), "Đáp án C: B còn 1/8", int(46 * clamp(k, 0.3, 1.0)), GREEN)
    x0, x1, yb, yt = 210, 950, 945, 480
    Xg = lambda v: x0 + v / 10 * (x1 - x0); Yg = lambda b: yb - b / 1000 * (yb - yt)
    card(d, (60, 380, 1020, 1045), fill=WHITE, outline=LIGHT, w=3)
    for b in (250, 500, 750, 1000): d.line([(x0, Yg(b)), (x1, Yg(b))], fill=(240, 236, 228), width=2)
    d.line([(x0, yb), (x1 + 25, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 40)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 52), "B (µT)", 34, MUTED, anchor="lm")
    text(d, (x1 + 25, yb + 78), "d (cm)", 34, MUTED, anchor="rm")
    for v in range(0, 11, 2):
        d.line([(Xg(v), yb), (Xg(v), yb + 10)], fill=NAVY, width=3); text(d, (Xg(v), yb + 36), str(v), 34, MUTED, bold=False)
    for b in (0, 500, 1000):
        d.line([(x0 - 10, Yg(b)), (x0, Yg(b))], fill=NAVY, width=4); text(d, (x0 - 18, Yg(b)), str(b), 34, MUTED, bold=False, anchor="rm")
    # hai duong so sanh qua diem 2 cm: "kieu 1/d" (o 4 cm = 500) va "kieu 1/d²" (o 4 cm = 250), net dut, khong in so
    vs = [2 + 8 * j / 80 for j in range(81)]
    for fn, col, at, lbl, lxy in ((lambda v: 2000 / v, GRAY, M[0] + 0.2, "kiểu 1/d", (7.4, 2000 / 7.4, -40, "mm")),
                                  (lambda v: 4000 / v ** 2, PURPLE, M[0] + 0.5, "kiểu 1/d²", (3.0, 4000 / 9, 0, "lm"))):
        kc = ease((t - at) / 1.0)
        if kc <= 0: continue
        pts = [(Xg(v), Yg(fn(v))) for v in vs][:max(2, int(81 * kc))]
        for j in range(0, len(pts) - 1, 2): d.line([pts[j], pts[j + 1]], fill=A(col, 0.8), width=5)
        lx, ly, dy, anc = lxy
        text(d, (Xg(lx) + (22 if anc == "lm" else 0), Yg(ly) + dy), lbl, 34, col, anchor=anc, alpha=appear(t, at + 0.6))
    # duong cong muot qua cac diem do (mo hinh luong cuc cong vecto voi Trai Dat), chi ve
    ka = ease((t - 0.3) / 0.9)
    if ka > 0:
        vs2 = [2 + 8 * j / 120 for j in range(121)]
        pts = [(Xg(v), Yg(math.hypot(8000 / v ** 3, B_TD))) for v in vs2][:max(2, int(121 * ka))]
        d.line(pts, fill=A(ORANGE, 0.6), width=5, joint="curve")
    km = appear(t, 0.9)
    for yy in range(int(Yg(129)) + 16, int(yb), 20): d.line([(Xg(4), yy), (Xg(4), min(yy + 11, yb))], fill=A(GREEN, km), width=4)
    for i, (dm, _, avg, _) in enumerate(ROWS):
        a = appear(t, 0.3 + i * 0.15, 0.4)
        if a > 0: dot(d, Xg(dm), Yg(avg), 14 * back(a), ORANGE, WHITE)
        if i == 0: text(d, (Xg(dm) + 30, Yg(avg) + 4), str(avg), 36, ORANGE, anchor="lm", alpha=a)
    # o phong to 4-10 cm (thang 0-150 µT) de doc ro cac diem nho
    kz = appear(t, 1.0)
    if kz > 0:
        zx0, zx1, zb, zt = 650, 920, 700, 540
        Zx = lambda v: zx0 + (v - 4) / 6 * (zx1 - zx0); Zy = lambda b: zb - b / 150 * (zb - zt)
        card(d, (600, 455, 990, 755), fill=A((250, 250, 252), kz), outline=A(GRAY, kz), r=18, w=3)
        text(d, (795, 485), "phóng to", 36, MUTED, alpha=kz)
        d.line([(zx0 - 20, zb), (zx1 + 20, zb)], fill=A(NAVY, kz), width=3)
        for v in (4, 6, 8, 10): text(d, (Zx(v), zb + 28), str(v), 32, MUTED, bold=False, alpha=kz)
        for i in range(1, 5):
            dm, avg = ROWS[i][0], ROWS[i][2]
            dot(d, Zx(dm), Zy(avg), 11, A(ORANGE, kz), WHITE)
            text(d, (Zx(dm), Zy(avg) - 32), str(avg), 36, GREEN if i == 1 else ORANGE, alpha=kz)
    # so sanh voi mo hinh
    a1 = appear(t, M[1] - 1.0)
    if a1 <= 0: return
    card(d, (60, 1075, 1020, 1600), fill=A(WHITE, a1), outline=A(BLUE, a1), w=4)
    text(d, (120, 1215), "Đo:", 44, MUTED, bold=False, anchor="lm", alpha=a1)
    text(d, (520, 1215), f"{ROWS[0][2]} → {ROWS[1][2]} µT", 46, ORANGE, anchor="lm", alpha=a1)
    a2 = appear(t, M[1] - 0.5)
    text(d, (120, 1305), "Mô hình:", 44, MUTED, bold=False, anchor="lm", alpha=a2)
    text(d, (520, 1305), f"{ROWS[0][3]} → {ROWS[1][3]} µT", 46, BLUE, anchor="lm", alpha=a2)
    a3 = appear(t, M[1] + 1.0)
    card(d, (110, 1375, 970, 1560), fill=A((236, 244, 255), a3), r=24)
    ctext(d, 1468, "d gấp 2: B chia 8", 52, BLUE, alpha=a3)

# ---------------- canh 4: mat do duong suc + chua noi duoc gi ----------------
# Nam cham tru tu hoa doc truc: coi nhu hai mat tich dien tu (N +, S -). Lan theo truong -> duong suc ra o mat N,
# vong ra ngoai, vao o mat S; khong cat nhau (moi duong la mot duong dong cua cung mot truong).
MW, MH = 26, 60             # nam cham trong so do (px), phong to so voi thang 66 px/cm
def _B(x, y):
    bx = by = 0.0
    for sx, q in ((MW / 2, 1), (-MW / 2, -1)):
        for j in range(11):
            py = -MH / 2 + 5 + j * (MH - 10) / 10
            dx, dy = x - sx, y - py; r3 = (dx * dx + dy * dy) ** 1.5 + 1e-9
            bx += q * dx / r3; by += q * dy / r3
    return bx, by

def _line(y0):
    x, y = MW / 2 + 2, y0; pts = [(x, y)]
    for _ in range(40000):
        bx, by = _B(x, y); n = math.hypot(bx, by); st = 2.5 + 0.03 * math.hypot(x, y)   # buoc lon dan khi ra xa
        x += st * bx / n; y += st * by / n; pts.append((x, y))
        if x < -MW / 2 and abs(y) < MH / 2: break
        if math.hypot(x, y) > 30000: break
    return pts

FL = [_line(y0) for y0 in (2.5, 5, 8, 17, 21, 25)]   # diem xuat phat deu tren mat N, nua tren; nua duoi doi xung
CX, CY2, BOX = 330, 600, (70, 264, 1010, 936)          # tam nam cham + vung ve doi xung quanh truc (x0, y0, x1, y1)
SC2 = 66                                               # px moi cm trong so do
def _inbox(p): return BOX[0] < p[0] < BOX[2] and BOX[1] < p[1] < BOX[3]

def _chev(d, x, y, ang, c, s=16, w=5):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=c, width=w)

def field_lines(d, a):
    if a <= 0: return
    c = A(PURPLE, 0.75 * a)
    for ln in FL:
        for sg in (1, -1):
            pts = [(CX + x, CY2 + sg * y) for x, y in ln]
            seg, on, acc = [], True, 0.0
            for p, q in zip(pts, pts[1:]):
                if not (_inbox(p) and _inbox(q)): seg = []; continue
                acc += math.dist(p, q)
                if on: d.line([p, q], fill=c, width=4)
                if acc > (14 if on else 9): on, acc = not on, 0.0
            vis = [i for i, p in enumerate(pts) if _inbox(p)]
            top = min(vis, key=lambda i: -abs(pts[i][1] - CY2))            # dinh cung (xa truc nhat trong khung)
            i0, i1 = max(0, top - 4), min(len(pts) - 1, top + 4)
            _chev(d, pts[top][0], pts[top][1], math.atan2(pts[i1][1] - pts[i0][1], pts[i1][0] - pts[i0][0]), c)
    # duong truc: ra khoi N sang phai, vao S tu ben trai
    d.line([(CX + MW / 2 + 4, CY2), (BOX[2] - 10, CY2)], fill=c, width=4)
    _chev(d, CX + MW / 2 + 70, CY2, 0, c)
    d.line([(BOX[0] + 10, CY2), (CX - MW / 2 - 4, CY2)], fill=c, width=4)
    _chev(d, CX - MW / 2 - 50, CY2, 0, c)

def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 1000), fill=WHITE, outline=LIGHT, w=3)
    field_lines(d, appear(t, 0.2, 0.6))
    magnet_side(d, CX + MW / 2, CY2, MW, MH, side=True)
    text(d, (W / 2, 968), "hình phóng to", 36, MUTED, bold=False, alpha=appear(t, 0.2))
    # hai vi tri cam bien 2 cm va 4 cm tren truc
    for i, col in ((0, GREEN), (1, ORANGE)):
        dm, avg = ROWS[i][0], ROWS[i][2]
        x = CX + MW / 2 + dm * SC2; a = appear(t, 0.6 + 0.4 * i)
        if a <= 0: continue
        d.rounded_rectangle([x - 24, CY2 - 54, x + 24, CY2 + 54], radius=10, outline=A(col, a), width=5)
        wd = ("mau", "thưa")[i]
        d.rounded_rectangle([x - 50, CY2 + 66, x + 50, CY2 + 112], radius=10, fill=A(WHITE, a))
        text(d, (x, CY2 + 89), wd, 36, col, alpha=a)
        lx, anc = (x + 30, "rm") if i == 0 else (x - 30, "lm")      # tach hai nhan cho khoi dinh nhau
        text(d, (lx, 300), f"{dm} cm", 36, col, anchor=anc, alpha=a)
        text(d, (lx, 345), f"{avg} µT", 36, INK, anchor=anc, alpha=a)
    a = appear(t, M[0] + 0.3)
    card(d, (60, 1030, 1020, 1240), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    ctext(d, 1090, "Mau: B lớn", 46, GREEN, alpha=a)
    ctext(d, 1180, "Thưa: B nhỏ", 46, ORANGE, alpha=appear(t, M[0] + 1.0))
    b = appear(t, M[1] - 0.6)
    card(d, (60, 1280, 1020, 1560), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
    text(d, (W / 2, 1340), "Chưa nói được", 46, PURPLE, alpha=b)
    ctext(d, 1450, f"Đừng tin số lẻ: ±{SAI_SO} µT", 46, INK, alpha=b)

# ---------------- canh 5: bay "ra xa thi B ve 0" ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 340), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 295), "Bẫy: ra xa thì B về 0?", 46, RED, alpha=appear(t, 0.05, 0.3))
    card(d, (60, 370, 1020, 1110), fill=WHITE, outline=LIGHT, w=3)
    x0, x1, yb, yt = 190, 980, 960, 520
    Yb = lambda b: yb - b / 60 * (yb - yt)
    d.line([(x0, yb), (x1, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 30)], fill=NAVY, width=5)
    text(d, (x0 + 16, yt - 46), "B (µT)", 34, MUTED, anchor="lm")
    for b in (0, 20, 40, 60):
        d.line([(x0 - 10, Yb(b)), (x0, Yb(b))], fill=NAVY, width=4); text(d, (x0 - 18, Yb(b)), str(b), 34, MUTED, bold=False, anchor="rm")
    # duong Trai Dat
    ke = appear(t, 0.1, 0.3)
    for xx in range(x0, x1, 28): d.line([(xx, Yb(B_TD)), (xx + 16, Yb(B_TD))], fill=A(GREEN, ke), width=5)
    for xx in range(600, 660, 28): d.line([(xx, 440), (xx + 16, 440)], fill=A(GREEN, ke), width=5)
    text(d, (x1, 440), f"Trái Đất ≈ {B_TD} µT", 34, GREEN, anchor="rm", alpha=ke)
    for j, i in enumerate((2, 3, 4)):
        dm, _, avg, lt = ROWS[i]; cx = 330 + j * 250
        g = ease((t - 0.1 - 0.15 * j) / 0.4)
        text(d, (cx, yb + 38), f"{dm} cm", 36, MUTED, bold=False)
        if g <= 0: continue
        top = Yb(avg * g); d.rectangle([cx - 85, top, cx - 5, yb], fill=ORANGE)
        text(d, (cx - 45, top - 28), str(avg), 36, ORANGE)
        g2 = appear(t, M[1] - 0.2 + 0.2 * j)
        if g2 > 0:
            top2 = Yb(BLT[i] * g2); d.rectangle([cx + 5, top2, cx + 85, yb], fill=BLUE)
            text(d, (cx + 45, top2 - 28), lt, 36, BLUE)
    # chu giai
    for k2, (col, s) in enumerate(((ORANGE, "số đọc"), (BLUE, "mô hình"))):
        a = 1.0 if k2 == 0 else appear(t, M[1] - 0.2)
        yy = 1045 + 0
        xb = 110 if k2 == 0 else 400
        d.rectangle([xb, yy - 16, xb + 32, yy + 16], fill=A(col, a))
        text(d, (xb + 46, yy), s, 34, INK, bold=False, anchor="lm", alpha=a)
    c = appear(t, 0.5)
    card(d, (60, 1140, 1020, 1560), fill=A((254, 242, 242), c), r=28)
    ctext(d, 1260, "Chững ở mức Trái Đất", 48, RED, alpha=appear(t, M[1] + 0.3))
    ctext(d, 1410, "Đo nền khi chưa có nam châm", 46, GREEN, alpha=appear(t, M[1] + 1.2))

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    chot_hoi(d, t, sc, "Xa gấp đôi: từ trường nam châm còn khoảng 1/8",
             "Từ 4 cm ra 12 cm (xa gấp 3): B nam châm còn mấy phần?")
    ks = appear(t, M[0] + 0.6, 0.5)            # so do nho: hai vi tri 4 cm va 12 cm (khong ghi dap so)
    if ks > 0:
        ny, sx0 = 1450, 230; px = 52
        d.line([(sx0, ny), (sx0 + 13.5 * px, ny)], fill=A(GRAY, ks), width=4)
        d.rectangle([sx0 - 26, ny - 30, sx0 - 13, ny + 30], fill=A(BLUE, ks))
        d.rectangle([sx0 - 13, ny - 30, sx0, ny + 30], fill=A(RED, ks))
        text(d, (sx0 - 13, ny - 58), "N", 34, RED, alpha=ks)
        for dm, col in ((4, GREEN), (12, ORANGE)):
            x = sx0 + dm * px
            dot(d, x, ny, 12, A(col, ks), WHITE)
            text(d, (x, ny + 50), f"{dm} cm", 36, col, alpha=ks)
        text(d, (sx0 + 12 * px, ny - 48), "B = ?", 38, INK, alpha=ks)
    kh = appear(t, M[0] + 3.0, 0.5)            # goi y tu ve, hien tre ~2,5 s
    if kh <= 0: return
    card(d, (110, 1100, 970, 1310), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
    text(d, (W / 2, 1155), "Gợi ý", 40, ORANGE, alpha=kh)
    ctext(d, 1238, "Nhớ lại: gấp đôi ra 1/8", 46, INK, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + row_at(0, do), "tap"), (do["t0"] + do["M"][1], "ding"),
            (an["t0"] + an["M"][1] + 1.0, "tap"), (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-tutruong-04", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Khái niệm từ trường · thachlab.id.vn", scenes=[
 dict(key="hook", title="Ra xa nam châm gấp đôi", draw=s_hook, tail=0.6, caps=[
   "Cảm biến trên trục nam châm.",
   ("Chọn một đáp án, rồi xem tiếp.", 5.8)]),
 dict(key="do", title="Dời máy ra xa dần", draw=s_do, tail=0.6, caps=[
   ("Đọc 3 lần, lấy trung bình.", 3.8),
   ("Dời ra 6, 8, 10 cm.", 4.0)]),
 dict(key="ans", title="Đồ thị B theo d", draw=s_ans, tail=0.7, caps=[
   ("Nhanh hơn 1/d và 1/d².", 3.0),
   ("Mô hình gần khớp số đo.", 4.6)]),
 dict(key="why", title="Mật độ đường sức", draw=s_why, tail=0.9, caps=[
   ("Nhìn hai chỗ đặt cảm biến.", 3.8),
   ("Giới hạn của số đo.", 4.0)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.9, caps=[
   ("Nhìn hai cột.", 3.0),
   ("10 cm vẫn đọc 31 µT.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video và trả lời.", 7.8)]),
])
