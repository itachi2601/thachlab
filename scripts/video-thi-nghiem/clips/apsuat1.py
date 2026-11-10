# Clip: tn-l12-apsuatdongnang-01 - Hat dap vao thanh hop: vo so va cham cong thanh luc deu (28/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-apsuatdongnang-01.json:
#   so_lieu_mau (so hat, tan so lac Hz, so va cham vao mot thanh moi giay):
#     100,1,125 ; 100,3,375 ; 200,1,250 ; 200,3,750 ; 400,3,1500  (so tinh tu mo hinh, khong phai so do)
#   mo_hinh: n_va = N_hat.v_hat/(2.l_hop) ; tham_so N mac dinh 200 hat.
# Canh: Du doan (gap ba?) -> Tien hanh (gia su 1 hat -> 200 hat 1 Hz -> 3 Hz, do thi luc len thanh cam cuon theo thoi gian)
#       -> Dap an B + bang so lieu + n = N.v/(2l) + co che -> Bay (hat nam yen de len thanh) + chua noi duoc -> Chot + cau hoi lop xe.
# Hinh hat chuyen dong la minh hoa CHIEU CHAM: so vach tren do thi khong bang 250/750, ti le day/thua moi dung (1:3).
from engine import *
import random as _rnd

# ---------------- bo cuc (khung 1080x1920) ----------------
R = 6                                   # ban kinh hat
LO, HI, TOP, BOT = 130, 700, 352, 888   # mien tam hat; thanh hop cach R
L = HI - LO
WALL = (LO - R, TOP - R, HI + R, BOT + R)
GRAIN = (176, 128, 52)
GX0, GX1, GTOP, GBASE = 110, 1000, 1010, 1340    # do thi luc
WIN = 3.0                               # cua so do thi (giay)
H1 = 50                                 # chieu cao vach o |vx| = 250 px/s, lac 1 Hz
CAVG = 150 / (200 * 9)                  # muc luc trung binh: 200 hat, 3 Hz -> 150 px

# ---------------- hat (tat dinh) ----------------
_r = _rnd.Random(3)
P = [(280.0, 352 + 200.0, 420.0, 200.0)]          # hat 0: dap thanh cam o t = 1,0 s va 3,7 s
for _ in range(199):
    u = _r.uniform(150, 330); a = _r.uniform(0, 2 * math.pi)
    P.append((_r.uniform(LO, HI), _r.uniform(TOP, BOT), u * math.cos(a), u * math.sin(a)))
PILE = []                                          # 200 hat nam yen o day
for j in range(200):
    row, col = divmod(j, 41)
    PILE.append((LO + col * L / 40 + _r.uniform(-2, 2), BOT - row * 12.5 + _r.uniform(-1.5, 1.5)))

# ---------------- thoi gian "hieu dung" S(t): toc do hat x sf(t), sf = 1 -> 3 khi chuyen sang 3 Hz ----------------
_cache = {}
def timing(sc):
    k = id(sc)
    if k not in _cache:
        M = sc["M"]; tOn, tA, dr = M[1], M[2], 0.6
        def sf(t): return 1.0 if t < tA else (3.0 if t >= tA + dr else 1 + 2 * (t - tA) / dr)
        def S(t):
            if t < tA: return t
            if t < tA + dr: return t + (t - tA) ** 2 / dr
            return tA + 2 * dr + 3 * (t - tA - dr)
        ts = np.linspace(-WIN - 1, sc["T"] + 1, 6000); Ss = np.array([S(x) for x in ts])
        _cache[k] = dict(tOn=tOn, tA=tA, dr=dr, sf=sf, S=S, Sinv=lambda s: float(np.interp(s, Ss, ts)))
    return _cache[k]

def hits(tm, i, ta, tb):
    """Cac lan hat i dap thanh phai (cam) trong [ta, tb]: (thoi diem, y, chieu cao vach)."""
    x0, y0, vx, vy = P[i]
    if i > 0: ta = max(ta, tm["tOn"])
    if tb <= ta or abs(vx) < 1e-6: return []
    S, Sinv = tm["S"], tm["Sinv"]
    qa = (x0 + vx * S(ta) - LO - L) / (2 * L); qb = (x0 + vx * S(tb) - LO - L) / (2 * L)
    lo_k, hi_k = sorted((qa, qb))
    out = []
    for k in range(math.ceil(lo_k), math.floor(hi_k) + 1):
        tau = Sinv((LO + L + 2 * L * k - x0) / vx)
        if ta <= tau <= tb:
            out.append((tau, refl(y0 + vy * S(tau), TOP, BOT), H1 * abs(vx) / 250 * tm["sf"](tau)))
    return out

# ---------------- ve hop, hat, bang dem ----------------
def box(d, dx=0.0):
    x0, y0, x1, y1 = WALL
    d.rounded_rectangle([x0 - 6 + dx, y0 - 6, x1 + 6 + dx, y1 + 6], radius=18, fill=(250, 252, 255), outline=NAVY, width=6)
    d.line([(x1 + 6 + dx, y0 + 10), (x1 + 6 + dx, y1 - 10)], fill=ORANGE, width=14)

def counter(d, n, f, c, ccol=ORANGE):
    card(d, (750, WALL[1] - 6, 1040, WALL[3] + 6), fill=WHITE, outline=LIGHT, r=26, w=3)
    text(d, (895, 400), "Số hạt", 32, MUTED, bold=False); text(d, (895, 452), n, 50, INK)
    text(d, (895, 540), "Lắc", 32, MUTED, bold=False); text(d, (895, 592), f, 46, INK)
    text(d, (895, 700), "Cú đập/giây", 32, MUTED, bold=False)
    text(d, (895, 810), c, 58 if c[:1].isdigit() else 40, ccol)

def pile(d, alpha=1.0):
    for x, y in PILE: dot(d, x, y, R, A(GRAIN, alpha))

# ---------------- canh 1: Du doan ----------------
OPTS = ("không đổi, vẫn 200 hạt", "tăng gấp ba lần", "tăng gấp chín lần",
        "giảm, hạt bay nhanh")

def s_hook(img, d, t, sc):
    box(d); pile(d)
    M = sc["M"]; a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 940 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Số cú đập vào thành cam sẽ…", 44, INK, alpha=a)
    for j, s in enumerate(OPTS):
        k = appear(t, M[1] + 0.15 * j, 0.4); yy = y0 + 270 + j * 76
        d.rounded_rectangle([90, yy - 30, 990, yy + 30], radius=30, outline=A(LIGHT, k), width=3)
        text(d, (120, yy), f"{'ABCD'[j]}.  {s}", 36, NAVY, bold=False, anchor="lm", alpha=k)
    tc, tend = M[1] + 0.8, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 572, 940, y0 + 584], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 572, 140 + 800 * (1 - p), y0 + 584], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (1 hat -> 200 hat 1 Hz -> 3 Hz, lien mach) ----------------
def chips(d, cur):
    for j, s in enumerate(("1 hạt", "1 Hz", "3 Hz")):
        x0 = 60 + j * 330; bx = (x0, 240, x0 + 300, 296)
        if j == cur: card(d, bx, fill=ORANGE, r=28); text(d, (x0 + 150, 268), s, 32, WHITE)
        elif j < cur: card(d, bx, fill=LIGHT, r=28); text(d, (x0 + 150, 268), s, 32, INK)
        else: card(d, bx, fill=None, outline=LIGHT, r=28, w=3); text(d, (x0 + 150, 268), s, 32, GRAY)

def dashed(d, pts, color, w=4, seg=14, gap=10):
    acc, on, cur = 0.0, True, [pts[0]]
    for p, q in zip(pts, pts[1:]):
        acc += math.dist(p, q); cur.append(q)
        if acc >= (seg if on else gap):
            if on and len(cur) > 1: d.line(cur, fill=color, width=w)
            on, acc, cur = not on, 0.0, [q]
    if on and len(cur) > 1: d.line(cur, fill=color, width=w)

def graph(d, tm, t):
    card(d, (40, 930, 1040, 1400), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 968), "Lực lên thành cam", 34, INK, anchor="lm")
    d.line([(GX0, GTOP - 10), (GX0, GBASE)], fill=NAVY, width=4)
    d.line([(GX0, GBASE), (GX1 + 16, GBASE)], fill=NAVY, width=4)
    arrow(d, (GX0, GTOP + 10), (GX0, GTOP - 12), NAVY, w=4, head=16)
    arrow(d, (GX1, GBASE), (GX1 + 18, GBASE), NAVY, w=4, head=16)
    text(d, (GX0 + 18, GTOP - 4), "F", 32, INK, anchor="lm")
    text(d, (GX1 + 10, GBASE + 32), "t · chiếu chậm", 32, MUTED, bold=False, anchor="rm")
    X = lambda tau: GX1 - (t - tau) / WIN * (GX1 - GX0)
    ta = max(-0.01, t - WIN)
    for i in range(len(P)):
        for tau, y, h in hits(tm, i, ta, t):
            x = X(tau); d.line([(x, GBASE - 2), (x, GBASE - 2 - h)], fill=A(ORANGE, 0.85), width=3)
    # chu giai
    card(d, (40, 1425, 1040, 1530), fill=WHITE, outline=LIGHT, w=3)
    d.line([(100, 1455), (100, 1500)], fill=ORANGE, width=5); text(d, (124, 1477), "một cú đập", 34, INK, bold=False, anchor="lm")

def s_do(img, d, t, sc):
    tm = timing(sc); M = sc["M"]
    S = tm["S"](t); dx = 7 * math.sin(2 * math.pi * S)
    stage = 0 if t < M[1] else (1 if t < M[2] else 2)
    chips(d, stage)
    box(d, dx)
    ka = appear(t, tm["tOn"], 0.4)
    for i, (x0, y0, vx, vy) in enumerate(P):
        al = 1.0 if i == 0 else ka
        if al <= 0.01: continue
        dot(d, refl(x0 + vx * S, LO, HI) + dx, refl(y0 + vy * S, TOP, BOT), R, A(RED if (i == 0 and stage == 0) else GRAIN, al))
        if i == 0 and stage == 0: dot(d, refl(x0 + vx * S, LO, HI) + dx, refl(y0 + vy * S, TOP, BOT), R + 6, RED, outline=WHITE)
    for i in range(len(P)):                                 # loe sang o thanh cam khi vua dap
        for tau, y, h in hits(tm, i, t - 0.15, t):
            k = 1 - (t - tau) / 0.15
            d.arc([HI + R + 6 + dx - 22, y - 22, HI + R + 6 + dx + 22, y + 22], 300, 60, fill=A(ORANGE, k), width=5)
    if stage == 0: counter(d, "1", "1 Hz", "—", MUTED)
    elif stage == 1: counter(d, "200", "1 Hz", "250")
    else: counter(d, "200", "3 Hz", "750" if t >= tm["tA"] + tm["dr"] else "…")
    graph(d, tm, t)

# ---------------- canh 3: Dap an + rut ra ----------------
ROWS = [(100, 1, 125), (100, 3, 375), (200, 1, 250), (200, 3, 750), (400, 3, 1500)]   # so_lieu_mau

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, M[0] + 0.1, 0.5)
    pw = tw(d, "ĐÁP ÁN B", F(36)) + 52
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 310), fill=A(NAVY, ka), r=30)
    text(d, (W / 2, 280), "ĐÁP ÁN B", 36, WHITE, alpha=ka)
    card(d, (40, 335, 1040, 905), fill=WHITE, outline=LIGHT, w=3)
    for x, s in ((300, "Số hạt"), (540, "Lắc (Hz)"), (800, "Cú đập/giây")):
        text(d, (x, 385), s, 32, MUTED, bold=False)
    d.line([(150, 415), (970, 415)], fill=LIGHT, width=3)
    yr = lambda j: 465 + j * 76
    k3 = appear(t, M[0] + 0.1, 0.4) * (1 - appear(t, M[1] - 0.1, 0.4))
    k2 = appear(t, M[1] - 0.1, 0.4)
    if k3 > 0:
        for j in (2, 3): d.rounded_rectangle([170, yr(j) - 32, 950, yr(j) + 32], radius=22, fill=A((255, 237, 213), k3))
    if k2 > 0:
        for j in (0, 2): d.rounded_rectangle([170, yr(j) - 32, 950, yr(j) + 32], radius=22, fill=A((220, 252, 231), k2))
    for j, (n, f, c) in enumerate(ROWS):
        text(d, (300, yr(j)), str(n), 40, INK); text(d, (540, yr(j)), str(f), 40, INK); text(d, (800, yr(j)), str(c), 40, ORANGE)
    ka3 = appear(t, M[0] + 0.1, 0.4)                          # ngoac x3 ben phai: 250 -> 750
    if ka3 > 0:
        c = A(ORANGE, ka3); y2, y3 = yr(2), yr(3)
        d.line([(962, y2), (985, y2), (985, y3), (962, y3)], fill=c, width=4)
        text(d, (1012, (y2 + y3) / 2), "×3", 34, ORANGE, alpha=ka3)
    if k2 > 0:                                                # ngoac x2 ben trai: 125 -> 250
        c = A(GREEN, k2); y0_, y2 = yr(0), yr(2)
        d.line([(158, y0_), (135, y0_), (135, y2), (158, y2)], fill=c, width=4)
        text(d, (96, (y0_ + y2) / 2), "×2", 34, GREEN, alpha=k2)
    text(d, (W / 2, 866), "Số tính từ mô hình", 32, MUTED, bold=False)
    # cong thuc + co che
    k1 = appear(t, M[1] + 0.2, 0.5); kc = appear(t, M[1] + 2.4, 0.5)
    card(d, (40, 935, 1040, 1600), fill=A(WHITE, k1), outline=A(GREEN, k1), w=5)
    rich(d, W / 2, 1010, "n = N · v / (2L)", 58, INK, alpha=k1)
    d.line([(120, 1140), (960, 1140)], fill=A(LIGHT, k1), width=3)
    text(d, (W / 2, 1210), "Một cú đập: lực nhỏ", 44, INK, alpha=kc)
    text(d, (W / 2, 1330), "Vô số cú đập → lực đều", 44, INK, alpha=appear(t, M[1] + 3.0, 0.4))
    text(d, (W / 2, 1450), "= áp suất", 54, GREEN, alpha=appear(t, M[1] + 3.6, 0.4))

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    box(d); pile(d)
    kb = appear(t, 0.5, 0.4)
    if kb > 0:
        for x in (250, 415, 580): arrow(d, (x, 740), (x, 815), A(NAVY, kb), w=5, head=18)
    k1 = appear(t, 0.3, 0.45); k2 = appear(t, M[1] - 0.1, 0.45); a1 = k1 * (1 - k2)
    if a1 > 0:
        y0 = 940 + (1 - k1) * 30
        card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“Hạt nằm yên đè lên thành”"
        ks = clamp((t - 1.0) / 0.4)
        f = F(40); lw = tw(d, q, f); yy = y0 + 170
        text(d, (W / 2, yy), q, 40, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * a1), width=4)
        ctext(d, y0 + 360, "Sai: hạt chuyển động mới đập thành.", 46, RED, maxw=900, alpha=a1 * appear(t, 1.0, 0.4))
    if k2 > 0:
        y0 = 940 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 62), "Chưa nói được", 42, NAVY, alpha=k2)
        lines = ("• Số cú đập: từ mô hình", "• Độ lớn một cú đập", "• Lắc không đều tay")
        for j, l1 in enumerate(lines):
            kk = k2 * appear(t, M[1] + 0.3 + 0.4 * j, 0.4); yy = y0 + 190 + j * 130
            text(d, (90, yy), l1, 42, INK, bold=False, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Áp suất khí = vô số va chạm nhỏ",
             "Bơm khí vào lốp, nhiệt độ giữ nguyên. Vì sao lốp căng?",
             "Số cú đập mỗi giây\nphụ thuộc vào gì?")

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.3, "ding"),
            (do["t0"] + M[1], "tap"), (do["t0"] + M[2], "tap"),
            (da["t0"] + da["M"][0] + 0.1, "ding"), (b["t0"] + b["M"][0], "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-apsuatdongnang-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Áp suất - động năng phân tử khí · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Lắc hộp gạo, áp tai nghe", draw=s_hook, tail=0.6, caps=[
   ("Lắc 1 Hz rồi 3 Hz.", 2.8),
   ("Chọn A, B, C hay D.", 7.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Một hạt: đập rồi bật ra.", 3.6),
   ("200 hạt, 1 Hz: 250 cú/giây.", 6.4),
   ("3 Hz: 750 cú/giây.", 5.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("250 lên 750: gấp ba.", 3.2),
   ("Hạt ×2: cú đập ×2.", 5.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Hạt nằm yên thì sao?", 4.0),
   ("Giới hạn.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Số cú đập?", 5.0)]),
])
