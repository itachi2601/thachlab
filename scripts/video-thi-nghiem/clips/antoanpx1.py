# Clip: tn-l12-antoanpx-01 - Do suat lieu theo khoang cach: kiem chung quy luat 1/r^2
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-antoanpx-01.json (so_lieu_mau, tham_so, hien_tuong_hay_sai).
# Ban 1 (28/10/2026): mau boyle/phongxa2 (dung cu + bang + do thi), tieng bao cues.
# Ban 2 (21/11/2026, viec 4 lo 20): dung lai theo cong moi (--do-chu 0 LOI, <= 50 s, chu >= 55 px ve).
#   Quan niem sai can danh: lan 1/d voi 1/d^2 (hien_tuong_hay_sai[0]).
#   Du doan 0,5 m -> 1 m (khong trung cau mo bai 1 -> 3 m, khong trung bang "Bam xem" o 2 m);
#   Bay: cot "Tuong 1/d" canh cot do that o 2 m, 3 m (khong lap cap so cua Du doan);
#   Chot (v2, cong B): 1 m -> 6 m giam may lan (ngoai bang do nen khong chia so da chieu ra duoc; dung mo hinh 360/d^2 cua kho; dap so 36 khong hien).
#   Khong hien N.d^2 o 2 m (o "em tu tinh" trong bang cua bai).
import random
from engine import *

ROWS = [(0.5, 1484, 1454, 364), (1.0, 390, 360, 360), (1.5, 196, 166, 374),
        (2.0, 119, 89, 356), (3.0, 71, 41, 369)]   # so_lieu_mau: d (m), nhip do, nhip thuc, N.d^2
SHOW = [0, 1, 3, 4]                                 # cac hang dung trong clip: 0,5; 1; 2; 3 m
DARK_OR = (194, 65, 12)
def fmt(v): return f"{v:.1f}".replace(".", ",")
def fm(v): return str(int(v)) if v == int(v) else fmt(v)

# ---------------- dung cu: nguon + thuoc + dau do + may dem ----------------
SX, SY = 130, 760          # tam nguon (d = 0)
PXM = 250                  # px moi met tren thuoc
def X(dd): return SX + dd * PXM
RY = 900                   # duong thuoc

RR = random.Random(7)
RAYS = [(RR.random(), RR.uniform(-math.pi, math.pi)) for _ in range(70)]   # hat gamma bay deu moi huong

def rig(d, t, dd, reading=None, top=True, probe_lbl=True):
    for ph, ang in RAYS:       # hat gamma tu nguon
        q = (ph + t * 0.9) % 1; r = 40 + q * 900
        x, y = SX + r * math.cos(ang), SY + r * math.sin(ang)
        if 600 < y < RY - 14 and x < 1010: dot(d, x, y, 6, A(ORANGE, 0.45))
    # thuoc: chi ghi so nguyen, chu >= 55
    d.line([(SX, RY), (X(3.0) + 20, RY)], fill=NAVY, width=6)
    for k in range(7):
        v = k * 0.5; x = X(v); L = 24 if k % 2 == 0 else 14
        d.line([(x, RY), (x, RY + L)], fill=NAVY, width=4)
        if k % 2 == 0: text(d, (x, RY + 62), str(int(v)), 55, NAVY, bold=False)
    text(d, (995, RY + 62), "m", 55, NAVY, bold=False)
    # nguon tren gia
    d.rectangle([SX - 8, SY + 34, SX + 8, RY], fill=GRAY)
    d.rounded_rectangle([SX - 34, SY - 34, SX + 34, SY + 34], radius=12, fill=YELLOW, outline=NAVY, width=5)
    for k in range(3):
        a = 90 + 120 * k
        d.pieslice([SX - 24, SY - 24, SX + 24, SY + 24], a - 30, a + 30, fill=NAVY)
    dot(d, SX, SY, 6, YELLOW)
    text(d, (60, SY - 150), "nguồn", 55, NAVY, bold=False, anchor="lm")
    # dau do (cua so o dau trai, quay ve nguon) tren gia
    x = X(dd)
    d.rectangle([x + 60, SY + 30, x + 76, RY], fill=GRAY)
    d.rounded_rectangle([x, SY - 30, x + 140, SY + 30], radius=26, fill=(214, 220, 232), outline=NAVY, width=5)
    d.rectangle([x - 4, SY - 24, x + 12, SY + 24], fill=(70, 78, 100))
    if probe_lbl:             # o gan nguon: canh trai tu mep dau do de xa nhan "nguon"
        if dd < 1.5: text(d, (x + 4, SY - 82), "đầu dò", 55, NAVY, anchor="lm")
        else: text(d, (x + 70, SY - 82), "đầu dò", 55, NAVY)
    if not top: return
    # khoang cach + may dem
    card(d, (60, 270, 500, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (280, 415), f"d = {fmt(dd)} m", 76, BLUE)
    card(d, (560, 270, 1020, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    d.rounded_rectangle([600, 300, 980, 440], radius=16, fill=NAVY)
    text(d, (790, 370), "···" if reading is None else str(reading), 80, (134, 239, 172))
    text(d, (790, 505), "đã trừ phông", 55, NAVY, bold=False)

# ---------------- canh 1: mo bai + du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    rig(d, t, 0.5, ROWS[0][2])
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1025 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 180), f"0,5 m: {ROWS[0][2]} xung/phút", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 280), "Lùi ra 1 m: còn bao nhiêu?", 60, INK, alpha=a)   # K10: khong ve nut A-D
    # dem nguoc 5 cham (cao 80 px), moi cham tat sau ~1 s
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    n_off = 0 if t < tc else min(5, int((t - tc) / ((tend - tc) / 5)) + 1)
    for j in range(5):
        dot(d, W / 2 + (j - 2) * 140, y0 + 430, 40, A(LIGHT, a) if j >= 5 - n_off else A(PURPLE, a))

# ---------------- canh 2: lui dan dau do, ghi bang ----------------
MOVE = 0.8
def row_at(i, sc):        # i = chi so trong SHOW
    return 0.0 if i == 0 else sc["M"][i]

def do_state(t, sc):
    dd = ROWS[SHOW[0]][0]
    for i in range(1, len(SHOW)):
        a = row_at(i, sc); nx = ROWS[SHOW[i]][0]
        if t < a - MOVE: return dd, ROWS[SHOW[i - 1]][2]
        if t < a: return lerp(dd, nx, ease((t - (a - MOVE)) / MOVE)), None
        dd = nx
    return dd, ROWS[SHOW[-1]][2]

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    dd, rd = do_state(t, sc)
    rig(d, t, dd, rd)
    card(d, (60, 1000, 1020, 1600), fill=WHITE, outline=NAVY, w=4)
    text(d, (250, 1060), "d (m)", 55, NAVY)
    text(d, (690, 1060), "N thực (xung/phút)", 55, NAVY)
    d.line([(90, 1100), (990, 1100)], fill=LIGHT, width=4)
    last = max(i for i in range(len(SHOW)) if t >= row_at(i, sc))
    for i, r in enumerate(SHOW):
        a = appear(t, row_at(i, sc), 0.35); y = 1160 + i * 105
        if a <= 0: continue
        if i == last: d.rounded_rectangle([80, y - 44, 1000, y + 44], radius=16, fill=A((225, 236, 255), a))
        text(d, (250, y), fmt(ROWS[r][0]), 64, BLUE, alpha=a)
        text(d, (690, y), str(ROWS[r][2]), 64, INK, alpha=a)
        if i == 1: text(d, (915, y), "≈ 1/4", 58, DARK_OR, alpha=a)

# ---------------- canh 3: vi sao giam theo d^2 + chua noi duoc gi ----------------
S0 = (130, 600); H1 = 62; GAP = 250
def P(r, z, y):   # diem tren mat vuong goc truc, cach nguon r buoc; chieu xien (z = sau)
    return (S0[0] + r * GAP + 0.42 * z, S0[1] - y - 0.28 * z)

def square(d, r, n, a, lbl, frac):
    h = r * H1
    c = [P(r, -h, -h), P(r, h, -h), P(r, h, h), P(r, -h, h)]
    d.polygon(c, fill=A((236, 244, 255), a), outline=A(NAVY, a))
    cell = h * 2 / n           # o to mau: o goc duoi-truoc, cung kich thuoc o moi khoang cach
    q = [P(r, -h, -h), P(r, -h + cell, -h), P(r, -h + cell, -h + cell), P(r, -h, -h + cell)]
    d.polygon(q, fill=A(ORANGE, a))
    for j in range(1, n):
        u = -h + j * cell
        d.line([P(r, u, -h), P(r, u, h)], fill=A(NAVY, a), width=3)
        d.line([P(r, -h, u), P(r, h, u)], fill=A(NAVY, a), width=3)
    d.line(c + [c[0]], fill=A(NAVY, a), width=4)
    for i in range(6):          # 36 hat trai deu tren mat: o to mau co 36 / 9 / 4 hat
        for j in range(6):
            dot(d, *P(r, -h + (i + 0.5) * h / 3, -h + (j + 0.5) * h / 3), 4, A(NAVY, a))
    bx = S0[0] + r * GAP
    text(d, (bx, 905), lbl, 60, BLUE, alpha=a)
    text(d, (bx, 985), frac, 64, DARK_OR, alpha=a)

FLY = [(RR.random(), RR.uniform(-1, 1), RR.uniform(-1, 1)) for _ in range(40)]
def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 1040), fill=WHITE, outline=LIGHT, w=3)
    hmax = 3 * H1
    for z, y in ((-hmax, -hmax), (hmax, -hmax), (hmax, hmax), (-hmax, hmax)):   # 4 canh cua chum tia
        d.line([S0, P(3, z, y)], fill=GRAY, width=3)
    for ph, u, v in FLY:        # hat bay thang tu nguon ra, trong chum
        q = (ph + t * 0.35) % 1; r = 0.15 + q * 2.85
        dot(d, *P(r, u * r * H1, v * r * H1), 7, A(ORANGE, 0.55))
    sq = [(1, 1, 0.2, "d", "1"), (2, 2, M[0] + 0.2, "2d", "1/4"), (3, 3, M[1] + 0.2, "3d", "1/9")]
    for r, n, at, lbl, fr in sq:
        square(d, r, n, appear(t, at), lbl, fr)
    dot(d, S0[0], S0[1], 16, YELLOW, NAVY)
    b = appear(t, M[2] + 0.1)
    if b <= 0: return
    card(d, (60, 1080, 1020, 1420), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
    text(d, (W / 2, 1150), "Chưa nói được gì?", 60, PURPLE, alpha=b)
    text(d, (W / 2, 1250), "Tác hại lên cơ thể", 60, INK, alpha=b)
    text(d, (W / 2, 1345), "(cần liều Sv)", 60, INK, alpha=b)

# ---------------- canh 4: bay lan 1/d voi 1/d^2 ----------------
def hatch_bar(d, x0, x1, top, base, a):
    d.rectangle([x0, top, x1, base], fill=A((238, 238, 242), a))
    for k in range(-int(base - top), int(x1 - x0), 22):     # gach cheo
        p0 = (x0 + max(k, 0), top + max(-k, 0)); xe = x0 + k + (base - top)
        p1 = (min(xe, x1), base - max(xe - x1, 0))
        if p0[0] < x1 and p0[1] < base: d.line([p0, p1], fill=A(GRAY, a), width=3)
    for yy in range(int(top), int(base), 18):               # vien net dut
        d.line([(x0, yy), (x0, min(yy + 10, base))], fill=A(GRAY, a), width=4)
        d.line([(x1, yy), (x1, min(yy + 10, base))], fill=A(GRAY, a), width=4)
    for xx in range(int(x0), int(x1), 18):
        d.line([(xx, top), (min(xx + 10, x1), top)], fill=A(GRAY, a), width=4)

def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    base, hmax = 900, 440
    hh = lambda n: hmax * n / ROWS[1][2]
    card(d, (60, 260, 1020, 1050), fill=WHITE, outline=LIGHT, w=3)
    a0 = appear(t, M[0]); a1 = appear(t, M[1]); g1 = ease((t - M[1]) / 0.8)
    # chu giai
    hatch_bar(d, 110, 160, 300, 350, a0)
    text(d, (180, 325), "Tưởng: 1/d", 55, RED, anchor="lm", alpha=a0)
    d.rectangle([600, 300, 650, 350], fill=A(ORANGE, a1))
    text(d, (670, 325), "Đo được", 55, GREEN, anchor="lm", alpha=a1)
    d.line([(90, base), (990, base)], fill=NAVY, width=5)
    # 1 m: cot chung (moc so sanh)
    d.rectangle([190, base - hh(360) * ease((t - 0.2) / 0.6), 310, base], fill=ORANGE)
    text(d, (250, base - hh(360) - 40), str(ROWS[1][2]), 58, INK, alpha=appear(t, 0.6))
    for cx, dm, k, r in ((560, 2, "1/2", 3), (870, 3, "1/3", 4)):
        text(d, (cx, base + 62), f"{dm} m", 58, NAVY)
        top_g = base - hmax / dm
        hatch_bar(d, cx - 115, cx - 5, top_g, base, a0)
        text(d, (cx - 60, top_g - 40), k, 58, RED, alpha=a0)
        n = ROWS[r][2]; top_o = base - hh(n) * g1
        if g1 > 0: d.rectangle([cx + 5, top_o, cx + 115, base], fill=ORANGE)
        text(d, (cx + 60, base - hh(n) - 40), str(n), 58, INK, alpha=a1)
    text(d, (250, base + 62), "1 m", 58, NAVY)
    c = appear(t, M[2])
    if c <= 0: return
    card(d, (60, 1100, 1020, 1330), fill=A((254, 242, 242), c), outline=A(RED, c), r=28, w=5)
    text(d, (W / 2, 1215), "Còn 1/9, không phải 1/3", 62, RED, alpha=c)

# ---------------- canh 5: tu kiem tra (cau_chot cua khung) ----------------
EX0, EPX = 130, 130                                      # so do cau chot: 130 px moi met, 6 m o x = 910
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    ex = lambda v: EX0 + v * EPX
    for ph, ang in RAYS:       # hat gamma tu nguon
        q = (ph + t * 0.9) % 1; r = 40 + q * 900
        x, y = EX0 + r * math.cos(ang), SY + r * math.sin(ang)
        if 600 < y < RY - 14 and x < 1010: dot(d, x, y, 6, A(ORANGE, 0.45))
    d.line([(EX0, RY), (ex(6) + 90, RY)], fill=NAVY, width=6)
    d.rectangle([EX0 - 8, SY + 34, EX0 + 8, RY], fill=GRAY)
    d.rounded_rectangle([EX0 - 34, SY - 34, EX0 + 34, SY + 34], radius=12, fill=YELLOW, outline=NAVY, width=5)
    for k in range(3):
        a = 90 + 120 * k
        d.pieslice([EX0 - 24, SY - 24, EX0 + 24, SY + 24], a - 30, a + 30, fill=NAVY)
    text(d, (60, SY - 150), "nguồn", 55, NAVY, bold=False, anchor="lm")
    dd = lerp(1.0, 6.0, ease((t - 0.6) / 1.8))
    x = ex(dd)                 # dau do: cua so (mep trai) dung tai vach
    d.rectangle([x + 60, SY + 30, x + 76, RY], fill=GRAY)
    d.rounded_rectangle([x, SY - 30, x + 140, SY + 30], radius=26, fill=(214, 220, 232), outline=NAVY, width=5)
    d.rectangle([x - 4, SY - 24, x + 12, SY + 24], fill=(70, 78, 100))
    for v, col in ((1.0, BLUE), (6.0, DARK_OR)):            # hai vi tri, nhan duoi thuoc
        if v == 6.0 and t < 2.4: continue
        d.polygon([(ex(v), RY + 6), (ex(v) - 20, RY + 40), (ex(v) + 20, RY + 40)], fill=col)
        text(d, (ex(v), RY + 90), f"{int(v)} m", 58, col)
    k = appear(t, 0.3, 0.5)
    if k <= 0: return
    card(d, (50, 1025, 1030, 1600), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    text(d, (W / 2, 1140), "Lùi từ 1 m ra 6 m.", 64, INK, alpha=k)
    text(d, (W / 2, 1250), "Nhịp thực giảm mấy lần?", 64, DARK_OR, alpha=k)
    kh = appear(t, M[1] + 0.1, 0.5)
    if kh <= 0: return
    card(d, (110, 1350, 970, 1540), fill=A((255, 247, 237), kh), r=24)
    text(d, (W / 2, 1445), "Khoảng cách gấp mấy lần?", 56, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, wy, tr, e = sc["hook"], sc["do"], sc["why"], sc["trap"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + row_at(i, do) - MOVE, "tick") for i in (1, 2, 3)]
            + [(do["t0"] + row_at(1, do), "ding"), (wy["t0"] + wy["M"][2], "tap"),
               (tr["t0"] + tr["M"][0] - 0.1, "buzz"), (tr["t0"] + tr["M"][2] - 0.1, "tap"),
               (e["t0"] + 0.3, "open")])

CLIP = dict(id="tn-l12-antoanpx-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="An toàn phóng xạ · thachlab.id.vn", scenes=[
 dict(key="hook", title="Lùi xa nguồn phóng xạ", draw=s_hook, tail=0.3, caps=[
   "Máy đếm gamma.",
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Lùi dần đầu dò", draw=s_do, tail=0.3, caps=[
   ("Lùi đầu dò ra 1 m.", 3.0),
   "Đáp án: giảm khoảng 4 lần.",
   ("Ra 2 m.", 2.5),
   ("Rồi 3 m.", 2.5)]),
 dict(key="why", title="Vì sao giảm nhanh vậy?", draw=s_why, tail=0.3, caps=[
   "Xa gấp 2: diện tích gấp 4.",
   ("Xa gấp 3: gấp 9.", 3.0),
   ("Máy chỉ đếm xung.", 4.2)]),
 dict(key="trap", title="Bẫy", draw=s_trap, tail=0.3, caps=[
   ("Lẫn 1/d với 1/d².", 3.0),
   ("Số đo ở 2 m, 3 m.", 3.0),
   ("Thấp hơn nhiều.", 3.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.4, caps=[
   ("Thử áp dụng.", 2.7),
   ("Dừng lại, tự đoán.", 4.2)]),
])
