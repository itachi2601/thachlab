# Clip: tn-l12-luctu-06 - Hai la nhom song song mang dong dien (ban 1, 12/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-luctu-06.json (so_lieu_mau, "so lieu minh hoa"):
#   la dai 50 cm, cach 1,0 cm; (I1, I2) = (5, 0) dung yen | (5, 5) cung chieu hut | (5, 5) nguoc chieu day |
#   (10, 5) cung chieu: hut, hai la lech nhu nhau, F moi la = 5,0e-4 N (tinh tu F = 2e-7.I1.I2.l/r).
# Du doan (khung ben canh, K10 khong ve nut): hai dong 5 A cung chieu (huong len) -> hai la hut nhau.
# Vat li (kiem bang tich co huong o duoi). Hinh nhin truc dien: x sang phai, y len, z huong ve nguoi xem.
#   B1 tai la 2 ~ I1 x r^ (r^ = +x tu la 1 sang la 2); luc len la 2 ~ I2 x B1; luc len la 1 = - luc len la 2 (DL III).
#   Cung chieu len: B1 = -z (vao trong trang), luc len la 2 = -x (ve phia la 1) -> HUT.
#   Hinh nhin tu tren xuong: dong huong len = huong ve nguoi nhin (cham trong tron), duong suc la 1 nguoc chieu kim dong ho.
# Mach: moi la mot vong kin rieng (day ve o xa, nguon + ampe ke); kho ghi 1 nguon + day doi chieu -> ve gon cho de doc.
from engine import *

def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def force2(s1, s2):
    """Chieu (dau x) luc len la 2; s1, s2 = +1 dong huong len, -1 huong xuong, 0 khong co dong."""
    B1 = cross((0, s1, 0), (1, 0, 0))
    return cross((0, s2, 0), B1)[0]
assert cross((0, 1, 0), (1, 0, 0)) == (0, 0, -1)          # B1 vao trong trang
assert force2(1, 1) < 0 and force2(1, -1) > 0 and force2(1, 0) == 0 and force2(-1, -1) < 0

NOTE = (70, 75, 95)
FOIL = (150, 158, 176)
COP = (90, 96, 112)
X1, X2, YT, YB = 440, 640, 312, 900          # hai la (nhin truc dien), dau tren / duoi giu chat
DMAX = 34                                     # do cong lon nhat (px)

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def sym(d, x, y, kind, r=26, color=NAVY, w=5):
    """Ve tay: 'o' = dong huong ve nguoi xem, 'x' = huong ra xa (font thieu glyph)."""
    dot(d, x, y, r, WHITE, outline=color); d.ellipse([x - r, y - r, x + r, y + r], outline=color, width=w)
    if kind == "o": dot(d, x, y, r * 0.3, color)
    else:
        q = r * 0.6
        d.line([(x - q, y - q), (x + q, y + q)], fill=color, width=w); d.line([(x - q, y + q), (x + q, y - q)], fill=color, width=w)

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
    dot(d, xw, 500, 44, WHITE, outline=NAVY); text(d, (xw, 500), "A", 44, NAVY)
    side = -1 if xw < xs else 1
    text(d, (xw + side * 56, 500), f"{I:g} A", 50, INK, anchor="rm" if side < 0 else "lm")
    yb = 720
    d.rectangle([xw - 26, yb - 34, xw + 26, yb + 34], fill=BG)
    lo, sh = (yb + 12, yb - 12) if s >= 0 else (yb - 12, yb + 12)
    d.line([(xw - 44, lo), (xw + 44, lo)], fill=NAVY, width=6)          # ban dai: cuc +
    d.line([(xw - 22, sh), (xw + 22, sh)], fill=NAVY, width=10)         # ban ngan: cuc -
    yp, ym = (yb + 34, yb - 34) if s >= 0 else (yb - 34, yb + 34)          # cach nhau 68 px: khong doc thanh "±"
    text(d, (xw + side * 74, yp), "+", 44, RED); text(d, (xw + side * 74, ym), "−", 44, NAVY)
    # khoa K: dong khi co dong (I > 0), mo khi I = 0 -> so ampe ke, mui ten I, do cong dong bo theo cung trang thai
    d.rectangle([xw - 8, 588, xw + 8, 632], fill=BG)
    dot(d, xw, 590, 7, NAVY); dot(d, xw, 630, 7, NAVY)
    if I > 0: d.line([(xw, 590), (xw, 630)], fill=NAVY, width=6)
    else: d.line([(xw, 630), (xw - side * 30, 596)], fill=NAVY, width=6)

def front(d, I1, s1, I2, s2, k=1.0, arrows=True, plan=False):
    """Hinh truc dien. k: 0..1 muc cong theo luc tu that (tinh tu force2)."""
    d.rectangle([330, 290, 750, YT], fill=NAVY); d.rectangle([330, YB, 750, YB + 22], fill=NAVY)
    # plan=True (canh Du doan): khoa con mo, ampe ke 0 A; mui ten chi chieu dong SE cho qua
    loop(d, X1, 200, 0 if plan else I1, s1); loop(d, X2, 880, 0 if plan else I2, s2 if s2 else 1)
    f2 = force2(s1 if I1 else 0, s2 if I2 else 0)
    dx2 = DMAX * k * (1 if f2 > 0 else -1 if f2 < 0 else 0)
    strip(d, X1, -dx2); strip(d, X2, dx2)                               # DL III: la 1 lech nguoc la 2
    if arrows:
        xa1, xa2 = X1 - 0.92 * dx2, X2 + 0.92 * dx2                      # tren la cong (y 540-690 ~ 0,92 do cong)
        if I1: arrow(d, (xa1, 690 if s1 > 0 else 540), (xa1, 540 if s1 > 0 else 690), ORANGE, w=8, head=24)
        text(d, (xa1 - 30, 615), "I1", 50, ORANGE, anchor="rm")
        if I2: arrow(d, (xa2, 690 if s2 > 0 else 540), (xa2, 540 if s2 > 0 else 690), ORANGE, w=8, head=24)
        text(d, (xa2 + 30, 615), "I2" if I2 else "I2 = 0", 50 if I2 else 44, ORANGE, anchor="lm")
    text(d, (X1, 962), "lá 1", 46, NAVY); text(d, (X2, 962), "lá 2", 46, NAVY)
    # vach kich thuoc tren gia treo: khong bao gio cham la dang cong
    for x in (X1, X2): d.line([(x, 236), (x, 286)], fill=NOTE, width=4)
    arrow(d, (X1 + 4, 258), (X2 - 4, 258), NOTE, w=4, head=14); arrow(d, (X2 - 4, 258), (X1 + 4, 258), NOTE, w=4, head=14)
    text(d, (X2 + 22, 258), "1,0 cm", 44, NOTE, anchor="lm")

# ---------------- hinh nhin tu tren xuong ----------------
WA, WB, WY = (400, 660), (700, 660), 660      # ban kinh 300, mep trai x = 100
def top(d, s1, s2, flab=True, Ilab=None, k=1.0, kB=1.0, kF2=1.0, kF1=1.0):
    r = WB[0] - WA[0]
    if kB > 0:
        dashed_circle(d, WA[0], WY, r, A(PURPLE, kB), w=4)
        for ang in (90, 180, 270):                  # chevron theo chieu duong suc (dong ra -> nguoc kim dong ho tren man)
            a = math.radians(ang); x, y = WA[0] + r * math.cos(a), WY - r * math.sin(a)
            chevron(d, x, y, -(a + math.pi / 2) * s1, A(PURPLE, kB))
        B1 = cross((0, s1, 0), (1, 0, 0))            # (x, y, z) -> tren man nhin tu tren: x -> x, z -> xuong
        arrow(d, (WB[0], WY), (WB[0], WY + 130 * B1[2]), A(PURPLE, kB), w=8, head=24)
        text(d, (WB[0], WY + 130 * B1[2] - 46 * (1 if B1[2] < 0 else -1)), "B1", 50, PURPLE, alpha=kB)   # o dau mui ten
    sym(d, WA[0], WY, "o" if s1 > 0 else "x", 28, ORANGE)
    sym(d, WB[0], WY, "o" if s2 > 0 else "x", 28, ORANGE)
    lb1, lb2 = ("lá 1", "lá 2") if Ilab is None else Ilab
    text(d, (WA[0] - 50, WY), lb1, 46, NAVY, anchor="rm"); text(d, (WB[0] + 50, WY), lb2, 46, NAVY, anchor="lm")
    f2 = force2(s1, s2); L = 90
    if kF2 > 0:
        x0 = WB[0] - 30 * (1 if f2 < 0 else -1)
        arrow(d, (x0, WY), (x0 + L * (1 if f2 > 0 else -1), WY), A(GREEN, kF2), w=9, head=26)
        if flab: text(d, (WB[0] - 24, WY - 66), "lực lên lá 2", 46, GREEN, anchor="rm", alpha=kF2)
    if kF1 > 0:
        x0 = WA[0] + 30 * (1 if f2 < 0 else -1)
        arrow(d, (x0, WY), (x0 - L * (1 if f2 > 0 else -1), WY), A(ORANGE, kF1), w=9, head=26)
        if flab: text(d, (WA[0] + 12, WY + 66), "lực lên lá 1", 46, ORANGE, anchor="lm", alpha=kF1)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; front(d, 5, 1, 5, 1, k=0, plan=True)
    a = appear(t, 0.5, 0.5)
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 400), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Đóng mạch: hai dòng 5 A cùng chiều.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 255), "Hai lá nhôm sẽ thế nào?", 48, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 340, 940, y0 + 354], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 340, 140 + 800 * (1 - p), y0 + 354], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
ROWS = (("5", "0", "đứng yên"), ("5", "5 cùng chiều", "hút"), ("5", "5 ngược chiều", "đẩy"))
def stages(sc):
    M = sc["M"]; return (0.4, M[1] + 0.2, M[1] + 2.6)

def state_do(t, sc):
    """(I2, s2, k cong, so hang) dong bo: ampe ke, mui ten I2, do cong, bang."""
    st = stages(sc)
    if t >= st[2]:
        u = t - st[2]; k = abs(1 - 2 * clamp(u / 1.0)) if u < 0.5 else clamp((u - 0.5) / 0.6)
        return 5, (1 if u < 0.5 else -1), k, (3 if u >= 1.1 else 2)
    if t >= st[1]: return 5, 1, clamp((t - st[1]) / 0.6), (2 if t >= st[1] + 0.6 else 1)
    return 0, 1, 0.0, 1

COLX = ((170, "I1 (A)"), (440, "I2 (A)"), (800, "Hiện tượng"))
def table(d, y0, n, alpha=1.0):
    card(d, (40, y0, 1040, y0 + 330), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, s in COLX: text(d, (x, y0 + 46), s, 40, NOTE, bold=False, alpha=alpha)
    d.line([(70, y0 + 84), (1010, y0 + 84)], fill=A(LIGHT, alpha), width=3)
    for j, r in enumerate(ROWS[:n]):
        yy = y0 + 84 + 76 * (j + 0.5) + 4
        for (x, _), s in zip(COLX, r): text(d, (x, yy), s, 42, INK if x < 700 else NAVY, alpha=alpha)

def s_do(img, d, t, sc):
    I2, s2, k, n = state_do(t, sc)
    front(d, 5, 1, I2, s2, k=k)
    table(d, 1040, n)

# ---------------- canh 3: Dap an + co che ----------------
CHAIN = (("Nắm tay phải → B1 tại lá 2", PURPLE),
         ("Bàn tay trái → F lên lá 2", GREEN),
         ("Định luật III → F lên lá 1", ORANGE))
def chain_at(sc):
    return (0.5, 3.3, 6.1)          # moi buoc hien cung nhip voi phan hinh tuong ung (B1 -> F2 -> F1)

def s_dapan(img, d, t, sc):
    M = sc["M"]; at = chain_at(sc)
    ka = appear(t, 0.4, 0.4)
    s = "ĐÁP ÁN · hút nhau"
    pw = tw(d, s, F(40)) + 56
    card(d, (W / 2 - pw / 2, 236, W / 2 + pw / 2, 300), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 268), s, 40, WHITE, alpha=ka)
    top(d, 1, 1, kB=appear(t, at[0], 0.45), kF2=appear(t, at[1], 0.45), kF1=appear(t, at[2], 0.45))
    kt = appear(t, 0.3, 0.4)
    text(d, (W / 2, 1052), "Nhìn từ trên xuống", 50, INK, alpha=kt)
    if kt > 0:                                                   # chu giai ky hieu, mot lan
        sym(d, 250, 1118, "o", 24, A(ORANGE, kt))
        text(d, (286, 1118), ": dòng điện hướng ra phía em", 46, INK, anchor="lm", alpha=kt)
    k0 = appear(t, at[0] - 0.2, 0.4)
    nb = sum(appear(t, a, 0.45) for a in at)                     # the co theo so buoc da hien
    card(d, (40, 1166, 1040, 1166 + 20 + 150 * max(1.0, nb)), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    for j, (to, col) in enumerate(CHAIN):
        k = appear(t, at[j], 0.45); yy = 1244 + j * 150
        if k <= 0: continue
        dot(d, 110, yy, 32, A(col, k)); text(d, (110, yy), str(j + 1), 40, WHITE, alpha=k)
        text(d, (175, yy), to, 48, col, anchor="lm", alpha=k)
        if j < 2 and appear(t, at[j + 1], 0.3) > 0: arrow(d, (110, yy + 38), (110, yy + 112), GRAY, w=6, head=18)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    y = 1000; mk = M[1]                       # gach cau bay dung luc phu de doi sang "Sai: ..."
    k2 = appear(t, mk + 0.2, 0.45)
    top(d, 1, 1, Ilab=("lá 1: 10 A", "lá 2: 5 A"), kB=0.0, kF2=k2, kF1=k2)
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3)
    if a1 > 0:
        card(d, (40, y, 1040, y + 250 + 200 * k2), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(RED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Dòng lớn chịu lực lớn hơn”"
        ks = clamp((t - mk) / 0.4); f = F(46); lw = tw(d, q, f); yy = y + 170
        text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
        k2 = a1 * k2
        text(d, (W / 2, y + 290), "F ≈ 5,0·10⁻⁴ N mỗi lá", 50, ORANGE, alpha=k2)
        text(d, (W / 2, y + 375), "tính từ B1 tại lá 2", 46, NOTE, alpha=k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 320), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[2] + 0.2, 0.4)
        text(d, (W / 2, y + 215), "Chỉ thấy lá lệch, chưa đo lực", 46, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    for x, s in ((440, 1), (640, -1)):
        d.line([(x, 1010), (x, 1230)], fill=A(FOIL, k), width=14)
        arrow(d, (x, 1175 if s > 0 else 1065), (x, 1065 if s > 0 else 1175), A(ORANGE, k), w=8, head=22)
    text(d, (420, 1120), "I1 = 4 A", 44, ORANGE, anchor="rm", alpha=k)
    text(d, (712, 1120), "I2 = 8 A", 44, ORANGE, anchor="lm", alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Mỗi lá chịu lực từ của từ trường lá kia",
             "I1 = 4 A lên, I2 = 8 A xuống. Lực lên mỗi lá bao nhiêu, hút hay đẩy?", None, body=_end_body)
    kh = appear(t, M[0] + 2.6, 0.5)
    if kh > 0:
        card(d, (110, 1320, 970, 1540), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1372, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1462, "dài 50 cm, cách nhau 1,0 cm", 48, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    st = stages(do)
    return ([(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tap") for s in st[1:]]
            + [(da["t0"] + 0.4, "ding")] + [(da["t0"] + a, "tap") for a in chain_at(da)]
            + [(b["t0"] + b["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-luctu-06", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Lực từ · Cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai lá nhôm song song", draw=s_hook, tail=0.3, caps=[
   ("Mỗi lá một mạch kín riêng.", 3.0),
   ("Chọn đáp án ở khung câu hỏi.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Chỉ lá 1 có dòng 5 A.", 3.4),
   ("Lá 2 cùng chiều, rồi ngược chiều.", 4.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Cùng chiều thì hút nhau.", 9.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 2.5),
   ("Sai: hai lực bằng nhau.", 4.3),
   ("Giới hạn thí nghiệm.", 2.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video và trả lời.", 7.6)]),
])
