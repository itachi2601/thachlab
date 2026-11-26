# Clip: tn-l12-tutruong-04 - Do cam ung tu theo khoang cach bang cam bien tu truong (dien thoai)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-tutruong-04.json (so_lieu_mau, tham_so, hien_tuong_hay_sai).
# Ban 1 (28/10/2026). Ban 2 (26/11/2026): chu >= 58, hop Du doan / THU NGHI tu ve, bo canh mat do duong suc
#   (gon duoi 50 s), bay "ra xa thi B ve 0" + chua noi duoc gop chung mot canh.
from engine import *

ROWS = [(2, (999, 1001, 1000), 1000, "1000"), (4, (128, 130, 129), 129, "125"), (6, (47, 48, 49), 48, "37,0"),
        (8, (33, 34, 35), 34, "15,6"), (10, (30, 31, 32), 31, "8,0")]   # so_lieu_mau: d (cm), 3 lan doc, TB B, B_lt (µT)
B_TD = 30                                                                 # tham_so: B Trai Dat (µT)
# Hop Du doan (dap an o khung): 1000 µT o 2 cm -> 4 cm doc khoang 125-129 µT (con ~1/8), khong phai 500 (chia 2).
# Cau chot (khung): mo hinh luong cuc B ~ 1/d^3 -> 4 cm -> 12 cm (gap 3) con 1/27 (125 -> 4,6 µT theo cot B_lt).
NOTE = (70, 75, 95); EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)

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

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",").replace(",0", "")

# ---------------- dung cu: nam cham tru + thuoc + dien thoai (cam bien tren truc) ----------------
AY = 760                    # truc nam cham (nam ngang)
NX = 170                    # mat cuc Bac (d = 0)
PXC = 74                    # px moi cm
def X(dd): return NX + dd * PXC
RY = 900                    # duong thuoc

def magnet_side(d, xn, cy, w=48, h=116):
    """Nam cham tru nhin ngang: mat N ben phai (do), mat S ben trai (xanh). Truc tu hoa nam ngang."""
    d.rectangle([xn - w, cy - h / 2, xn - w / 2, cy + h / 2], fill=BLUE)
    d.rectangle([xn - w / 2, cy - h / 2, xn, cy + h / 2], fill=RED)
    d.rectangle([xn - w, cy - h / 2, xn, cy + h / 2], outline=NAVY, width=4)
    for x, s_, col in ((xn - w - 34, "S", BLUE), (xn + 34, "N", RED)):
        d.rounded_rectangle([x - 30, cy - h / 2 - 70, x + 30, cy - h / 2 - 4], radius=12, fill=WHITE)
        text(d, (x, cy - h / 2 - 37), s_, 58, col)

def phone(d, x, cy):
    """Dien thoai dung, cam bien (cham cam) dat dung tren truc o mep trai."""
    d.rounded_rectangle([x - 14, cy - 40, x + 66, cy + 120], radius=16, fill=(60, 66, 90), outline=NAVY, width=4)
    d.rounded_rectangle([x - 4, cy - 28, x + 56, cy + 104], radius=8, fill=(190, 205, 230))
    dot(d, x, cy, 11, ORANGE, WHITE)

def rig(d, dd, reading):
    for xx in range(NX + 8, 1010, 26): d.line([(xx, AY), (xx + 12, AY)], fill=A(GRAY, 0.7), width=3)
    d.line([(NX, RY), (X(10) + 20, RY)], fill=NAVY, width=6)                 # thuoc 0-10 cm, goc o mat N
    for k in range(11):
        x = X(k); L = 24 if k % 2 == 0 else 14
        d.line([(x, RY), (x, RY + L)], fill=NAVY, width=4)
        if k % 2 == 0: text(d, (x, RY + 62), str(k), 58, NOTE)
    text(d, (X(10) + 78, RY + 62), "cm", 58, NOTE)
    d.rectangle([NX - 32, AY + 58, NX - 16, RY], fill=GRAY)
    magnet_side(d, NX, AY)
    x = X(dd)
    d.rectangle([x + 18, AY + 120, x + 34, RY], fill=GRAY)
    phone(d, x, AY)
    card(d, (60, 270, 500, 520), fill=WHITE, outline=LIGHT, r=28, w=4)       # khoang cach tu mat N
    text(d, (280, 395), f"d = {vn(dd)} cm", 66, BLUE)
    card(d, (560, 270, 1020, 520), fill=WHITE, outline=LIGHT, r=28, w=4)     # man hinh ung dung
    d.rounded_rectangle([610, 300, 970, 420], radius=16, fill=NAVY)
    text(d, (790, 360), str(reading), 70, (134, 239, 172))
    text(d, (790, 470), "µT", 58, NOTE)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut A-D) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 2, ROWS[0][2])
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 170), "Ở 2 cm: 1000 µT.", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 260), "Ra 4 cm (xa gấp đôi),", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 350), "máy đọc khoảng bao nhiêu?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 430, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: doi dien thoai ra xa dan, ghi bang ----------------
R4, MV = 2.2, 0.6                                          # moc ghi dong 4 cm; thoi gian doi may
def do_d(t, sc):
    M = sc["M"]
    if t < R4 - MV: return 2.0
    if t < R4: return lerp(2, 4, ease((t - R4 + MV) / MV))
    legs = [(4, 6), (6, 8), (8, 10)]
    for j, (a, b) in enumerate(legs):                       # 4 -> 6 -> 8 -> 10, moi chang 0,4 s, nghi 0,2 s
        s0 = M[1] - 1.8 + 0.6 * j
        if t < s0: return a
        if t < s0 + 0.4: return lerp(a, b, ease((t - s0) / 0.4))
    return 10.0

def s_do(img, d, t, sc):
    M = sc["M"]
    dd = do_d(t, sc)
    i = min(range(5), key=lambda n: abs(ROWS[n][0] - dd))
    moving = abs(ROWS[i][0] - dd) > 0.05
    at_i = 0.0 if i == 0 else (R4 if i == 1 else M[1])          # dong bang da ghi -> man hinh dung o so trung binh
    rig(d, dd, "···" if moving else (ROWS[i][2] if t > at_i + 0.6 and (i > 0 or t > 1.0) else ROWS[i][1][int(t * 3) % 3]))
    card(d, (60, 1010, 1020, 1580), fill=WHITE, outline=NAVY, w=4)
    xs = [175, 490, 880]
    for x, c in zip(xs, ["d (cm)", "3 lần đọc", "TB"]): text(d, (x, 1075), c, 58, NOTE)
    d.line([(90, 1112), (990, 1112)], fill=LIGHT, width=4)
    hl = appear(t, M[1] + 2.2, 0.4)                           # to sang dong 2 cm va 4 cm de so
    for r, (dm, three, avg, _) in enumerate(ROWS):
        at = 0.0 if r == 0 else (R4 if r == 1 else M[1])
        a = 1.0 if r == 0 else appear(t, at, 0.35)
        if a <= 0: continue
        y = 1160 + r * 76
        if hl > 0 and r < 2: d.rounded_rectangle([80, y - 38, 1000, y + 38], radius=14, fill=A((220, 252, 231), hl))
        text(d, (xs[0], y), str(dm), 60, BLUE, alpha=a)
        text(d, (xs[1], y), " · ".join(map(str, three)), 58, INK, alpha=a)
        text(d, (xs[2], y), str(avg), 62, GREEN, alpha=a)
    text(d, (W / 2, 1542), "số liệu minh hoạ", 58, NOTE)

# ---------------- canh 3: dap an: B con ~1/8 + do thi, so voi "chia 2" va mo hinh ----------------
def s_ans(img, d, t, sc):
    M = sc["M"]
    card(d, (60, 250, 1020, 360), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 305), "2 → 4 cm: còn ≈ 1/8", 64, GREEN)
    x0, x1, yb, yt = 190, 900, 1000, 490
    Xg = lambda v: x0 + v / 10 * (x1 - x0); Yg = lambda b: yb - b / 1000 * (yb - yt)
    card(d, (60, 390, 1020, 1110), fill=WHITE, outline=LIGHT, w=3)
    d.line([(x0, yb), (x1 + 30, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 40)], fill=NAVY, width=5)
    text(d, (x0 - 50, yt - 20), "B", 60, NOTE)
    for v in range(2, 11, 2):
        d.line([(Xg(v), yb), (Xg(v), yb + 12)], fill=NAVY, width=3); text(d, (Xg(v), yb + 52), str(v), 58, NOTE)
    text(d, (x1 + 70, yb + 52), "cm", 58, NOTE)
    vs = [2 + 8 * j / 80 for j in range(81)]
    kc = ease((t - 2.0) / 0.8)                                  # "chia 2" (kieu 1/d) qua diem 2 cm, net dut xam
    if kc > 0:
        pts = [(Xg(v), Yg(2000 / v)) for v in vs][:max(2, int(81 * kc))]
        for j in range(0, len(pts) - 1, 2): d.line([pts[j], pts[j + 1]], fill=GRAY, width=6)
        text(d, (Xg(4) + 40, Yg(500) - 46), "nếu chia 2", 58, GRAY, anchor="lm", alpha=appear(t, 2.0, 0.3))
    km = ease((t - M[1] - 0.2) / 1.2)                           # mo hinh luong cuc (cot B_lt) - net lien xanh
    if km > 0:
        pts = [(Xg(v), Yg(8000 / v ** 3)) for v in vs][:max(2, int(81 * km))]
        d.line(pts, fill=A(BLUE, 0.8), width=6, joint="curve")
    for i, (dm, _, avg, _) in enumerate(ROWS):                 # diem do (TB)
        a = appear(t, 0.2 + i * 0.12, 0.4)
        if a > 0: dot(d, Xg(dm), Yg(avg), 16 * back(a), ORANGE, WHITE)
    text(d, (Xg(2) + 34, Yg(1000) + 6), "1000", 58, ORANGE, anchor="lm")
    text(d, (Xg(4) + 10, Yg(129) - 52), "129", 58, ORANGE, anchor="lm", alpha=appear(t, 0.5, 0.3))
    a1 = appear(t, M[1], 0.45)
    hg = appear(t, M[1] + 2.6, 0.5)
    card(d, (60, 1150, 1020, 1330), fill=A(mix(WHITE, (219, 234, 254), hg), a1), outline=A(BLUE, a1), w=5)
    text(d, (W / 2, 1240), "Mô hình: 1000 → 125 µT", 62, BLUE, alpha=a1)

# ---------------- canh 4: Bay "ra xa thi B ve 0" + chua noi duoc ----------------
def s_trap(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    card(d, (40, 240, 1040, 470), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, 305, "BẪY", RED)
    q = "“Ra xa thì máy đọc về 0”"
    ks = clamp((t - mk) / 0.4); f = F(60); lw = tw(d, q, f); yy = 400
    text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks))
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=6)
    card(d, (40, 500, 1040, 1150), fill=WHITE, outline=LIGHT, w=3)
    yb, yt = 1030, 620; Yb = lambda b: yb - b / 60 * (yb - yt)
    d.line([(150, yb), (980, yb)], fill=NAVY, width=5)
    for j, i in enumerate((2, 3, 4)):
        dm, _, avg, _ = ROWS[i]; cx = 230 + j * 175
        g = ease((t - 0.1 - 0.15 * j) / 0.5)
        text(d, (cx, yb + 55), f"{dm} cm", 58, NOTE)
        if g <= 0: continue
        top = Yb(avg * g)
        d.rectangle([cx - 60, top, cx + 60, yb], fill=ORANGE)
        text(d, (cx, top - 40), str(avg), 58, ORANGE)
    ke = appear(t, mk, 0.4)                                    # nen Trai Dat ~30 µT (tham_so B_TD)
    if ke > 0:
        for xx in range(150, 990, 30): d.line([(xx, Yb(B_TD)), (xx + 18, Yb(B_TD))], fill=A(GREEN, ke), width=6)
        text(d, (1005, Yb(B_TD) - 42), "Trái Đất ≈ 30", 58, GREEN, anchor="rm", alpha=ke)
    b = appear(t, M[2], 0.45)
    if b <= 0: return
    card(d, (40, 1180, 1040, 1440), fill=A(WHITE, b), outline=A(NAVY, b), w=5)
    pill(d, W / 2, 1250, "CHƯA NÓI ĐƯỢC", NAVY, b)
    text(d, (W / 2, 1360), "Ở xa: số đọc lẫn Trái Đất", 60, INK, alpha=b)

# ---------------- canh 5: THU NGHI (cau chot o khung: 4 cm -> 12 cm) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1180), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k)
    ny, sx0, px = 520, 200, 56
    d.line([(sx0, ny), (sx0 + 13.5 * px, ny)], fill=A(GRAY, k), width=5)
    d.rectangle([sx0 - 44, ny - 46, sx0 - 22, ny + 46], fill=A(BLUE, k))
    d.rectangle([sx0 - 22, ny - 46, sx0, ny + 46], fill=A(RED, k))
    text(d, (sx0 - 11, ny - 90), "N", 58, RED, alpha=k)
    for dm, col in ((4, GREEN), (12, ORANGE)):
        x = sx0 + dm * px
        dot(d, x, ny, 16, A(col, k), WHITE)
        text(d, (x, ny + 72), f"{dm} cm", 58, col, alpha=k)
    text(d, (sx0 + 12 * px, ny - 72), "?", 64, DORANGE, alpha=k)
    text(d, (W / 2, 760), "Ra từ 4 cm tới 12 cm:", 64, INK, alpha=k)
    text(d, (W / 2, 850), "theo mô hình, B nam châm", 64, DORANGE, alpha=k)
    text(d, (W / 2, 940), "còn mấy phần?", 64, DORANGE, alpha=k)
    seg_bar(d, 1060, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + R4, "tap"), (do["t0"] + do["M"][1], "tap"),
            (an["t0"] + an["M"][1], "tap"), (tr["t0"] + tr["M"][1], "buzz"), (tr["t0"] + tr["M"][2], "tap"),
            (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l12-tutruong-04", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Khái niệm từ trường · thachlab.id.vn", scenes=[
 dict(key="hook", title="Ra xa nam châm gấp đôi", draw=s_hook, tail=0.3, caps=[
   ("Cảm biến trên trục.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Dời máy ra xa dần", draw=s_do, tail=0.4, caps=[
   ("Đọc 3 lần mỗi chỗ.", 4.2),
   ("Dời ra 6, 8, 10 cm.", 4.4)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.5, caps=[
   ("Giảm nhanh hơn chia 2.", 3.6),
   ("Khớp mô hình lưỡng cực.", 5.0)]),
 dict(key="trap", title="Bẫy và giới hạn", draw=s_trap, tail=0.6, caps=[
   ("Đúng không?", 2.6),
   ("Sai: chững ở nền Trái Đất.", 3.4),
   ("Chưa nói được.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự tính.", 6.8)]),
])
