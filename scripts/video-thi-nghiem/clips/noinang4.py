# Clip: tn-l12-noinang-04 - Xilanh cach nhiet: nen khi, giu yen, keo ve; hai ngan co vach (ban 1, 12/11/2026)
# Kho loai "vi_du" (mo hinh): clip ghi ro "mo hinh · so lieu minh hoa".
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-noinang-04.json (so_lieu_mau):
#   Ban dau 100 cm3, 300 K, 1,0.10^5 Pa | Nen nhanh 50 cm3, ~476 K, ~3,2.10^5 Pa, A ~ +8,8 J, Q = 0, dU ~ +8,8 J
#   Giu yen 50, 476, 3,2, A = Q = dU = 0 | Keo ve 100, 300, 1,0, A ~ -8,8 J, Q = 0, dU ~ -8,8 J
#   Hai ngan: 50 cm3 (ngan trai), 300 K, 2,0.10^5 Pa -> rut vach 100 cm3, 300 K, 1,0.10^5 Pa, A = Q = dU = 0.
# Du doan (khung): nen nhanh trong xilanh cach nhiet thi T khi ... A khong doi (vi cach nhiet) / B giam / C tang (dung) /
#   D tang roi tu giam ve 300 K. Trong mp4 KHONG ve nut A-D (K10), chi cau hoi + hinh.
# Bay chinh: "cach nhiet" != "noi nang khong doi"; dau A, Q trong dU = A + Q; khi tran vao chan khong A = 0.
# Font SF khong co glyph "⊥" -> khong dung.
from engine import *

NOTE = (70, 75, 95)
WALL = (255, 226, 190); HATCH = (214, 120, 40)
X0, YT, YB = 150, 360, 600            # mat trong thanh trai, mat trong thanh tren / duoi
LMAX = 560                            # V = 100 cm3 <-> 560 px
def xp_of(V): return X0 + LMAX * V / 100.0

def vn(x, nd=1, sign=False):
    if abs(x) < 1e-9: return "0"
    s = f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"
    return s.replace(".", ",").replace("-", "−")

def hatch_h(d, x0, x1, y0, y1, step=22):
    d.rectangle([x0, y0, x1, y1], fill=WALL)
    h = y1 - y0; x = x0
    while x < x1:
        xa, xb = x, min(x + h, x1); d.line([(xa, y1), (xb, y1 - (xb - xa))], fill=HATCH, width=3); x += step
    d.rectangle([x0, y0, x1, y1], outline=NAVY, width=3)

def hatch_v(d, x0, x1, y0, y1, step=22):
    d.rectangle([x0, y0, x1, y1], fill=WALL)
    w = x1 - x0; y = y0 + w
    while y < y1 + w:
        ya = min(y, y1); xa = x0 + (y - ya)
        d.line([(xa, ya), (x1, max(y - w, y0))], fill=HATCH, width=3); y += step
    d.rectangle([x0, y0, x1, y1], outline=NAVY, width=3)

# ---- phan tu khi: vi tri xac dinh (seed co dinh), toc do ~ sqrt(T) ----
random.seed(4)
MOL = [(random.random(), random.random(), random.uniform(0.18, 0.32) * random.choice((1, -1)),
        random.uniform(0.18, 0.32) * random.choice((1, -1))) for _ in range(26)]

def phase(t, Tfun, dt=0.05):
    """tich phan sqrt(T/300) theo thoi gian -> quang duong 'chuan hoa' (khong nhay khi T doi)."""
    s, tau = 0.0, 0.0
    while tau < t:
        h = min(dt, t - tau); s += math.sqrt(Tfun(tau) / 300.0) * h; tau += h
    return s

def gas(d, s, xl, xr, yt, yb, n=26, r=10, col=BLUE):
    for u0, v0, vu, vv in MOL[:n]:
        u = refl(u0 + vu * s, 0, 1); v = refl(v0 + vv * s, 0, 1)
        dot(d, xl + r + 2 + u * (xr - xl - 2 * r - 4), yt + r + 2 + v * (yb - yt - 2 * r - 4), r, col)

def cylinder(d, V, s, push=0, ghost=False, label=True):
    """Xilanh mot ngan nam ngang, day trai kin, pit-tong ben phai. push: -1 day vao, +1 keo ra (mui ten tren can)."""
    hatch_h(d, X0 - 26, 800, YT - 26, YT); hatch_h(d, X0 - 26, 800, YB, YB + 26); hatch_v(d, X0 - 26, X0, YT, YB)
    xp = xp_of(V)
    gas(d, s, X0, xp, YT, YB)
    hatch_v(d, xp, xp + 26, YT + 2, YB - 2)                       # pit-tong cach nhiet
    d.rectangle([xp + 26, 470, xp + 250, 490], fill=NAVY)        # can
    d.rounded_rectangle([xp + 250, 430, xp + 274, 530], radius=8, fill=NAVY)
    if label: text(d, (X0 - 26, YT - 62), "cách nhiệt", 40, HATCH, anchor="lm")
    if ghost:
        xg = xp_of(50)
        for y in range(YT + 6, YB - 6, 28): d.line([(xg, y), (xg, y + 14)], fill=PURPLE, width=5)
        text(d, (xg, YB + 62), "50 cm³", 40, PURPLE)
    if push:
        if push < 0: arrow(d, (xp + 230, 400), (xp + 80, 400), RED, w=8, head=24)
        else: arrow(d, (xp + 80, 400), (xp + 230, 400), RED, w=8, head=24)

def readout(d, vals, y=720, alpha=1.0):
    """3 o: V, T, p. vals = chuoi da dinh dang (khong noi suy so)."""
    xs = ((40, 330), (345, 615), (630, 1040))      # o p rong hon: "10⁵" o co 48
    for (a, b), s, sz in zip(xs, vals, (44, 44, 48)):
        card(d, (a, y - 46, b, y + 46), fill=A(WHITE, alpha), outline=A(NAVY, alpha), r=22, w=3)
        rich(d, (a + b) / 2, y, s, sz, INK, alpha=alpha)

def tag(d, y=1640, alpha=1.0):
    text(d, (1030, y), "mô hình · số liệu minh hoạ", 40, NOTE, bold=False, anchor="rm", alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    cylinder(d, 100, phase(t, lambda _: 300), ghost=t >= M[1] - 0.2)
    readout(d, ("V = 100 cm³", "T = 300 K", "p = 1,0·10⁵ Pa"), y=760)
    tag(d, 1640)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 235, "Nén nhanh khí còn 50 cm³.\nNhiệt độ khí thế nào?", 56, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 410, 940, y0 + 422], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 410, 140 + 800 * (1 - p), y0 + 422], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
C0, C1 = 0.9, 2.1          # nen
R1 = 2.3                   # hang "Nen"
H0, R2 = 4.9, 6.4          # giu yen (dong ho dem) ; hang "Giu yen"
P0, P1 = 7.0, 8.2          # keo ve
R3 = 8.4                   # hang "Keo ve"

def V_at(t):
    if t < C0: return 100.0
    if t < C1: return lerp(100, 50, ease((t - C0) / (C1 - C0)))
    if t < P0: return 50.0
    if t < P1: return lerp(50, 100, ease((t - P0) / (P1 - P0)))
    return 100.0

def T_at(t):  # chi de lam phan tu chay nhanh/cham (khong in so trung gian): T.V^(2/3) khong doi (mo_hinh)
    return 300.0 * (100.0 / V_at(t)) ** (2.0 / 3.0)

ROWS = (("Nén", 8.8, 0, 8.8), ("Giữ yên", 0, 0, 0), ("Kéo về", -8.8, 0, -8.8))
COLX = (180, 470, 690, 900)

def cell(x, nd=1):
    if abs(x) < 1e-9: return "0"
    return "≈ " + vn(x, nd, sign=True)

def table(d, y0, ks, hlq=0.0):
    rh = 100; h = 90 + rh * 3
    card(d, (40, y0, 1040, y0 + h), fill=WHITE, outline=LIGHT, w=3)
    if hlq > 0:
        d.rounded_rectangle([600, y0 + 10, 780, y0 + h - 10], radius=18, fill=A((255, 237, 213), hlq), outline=A(ORANGE, hlq), width=4)
    text(d, (COLX[0], y0 + 46), "Bước", 40, NOTE, bold=False)
    for x, s in zip(COLX[1:], ("A (J)", "Q (J)", "ΔU (J)")): text(d, (x, y0 + 46), s, 40, NAVY)
    d.line([(70, y0 + 88), (1010, y0 + 88)], fill=LIGHT, width=3)
    for j, (r, k) in enumerate(zip(ROWS, ks)):
        yy = y0 + 88 + rh * (j + 0.5) + 2
        if k <= 0:                                     # tieu de hang hien san, mo
            text(d, (COLX[0], yy), r[0], 42, LIGHT); continue
        text(d, (COLX[0], yy), r[0], 42, INK, alpha=k)
        for x, v in zip(COLX[1:], r[1:]):
            col = GREEN if v > 0 else (RED if v < 0 else INK)
            text(d, (x, yy), cell(v), 42, col, alpha=k)
    return h

def s_do(img, d, t, sc):
    V = V_at(t)
    push = -1 if C0 - 0.3 < t < C1 else (1 if P0 - 0.3 < t < P1 else 0)
    cylinder(d, V, phase(t, T_at), push=push, label=False)
    if t < C0: vals = ("V = 100 cm³", "T = 300 K", "p = 1,0·10⁵ Pa")
    elif t < C1: vals = ("V ↓", "T ↑", "p ↑")
    elif t < P0: vals = ("V = 50 cm³", "T ≈ 476 K", "p ≈ 3,2·10⁵ Pa")
    elif t < P1: vals = ("V ↑", "T ↓", "p ↓")
    else: vals = ("V = 100 cm³", "T = 300 K", "p = 1,0·10⁵ Pa")
    readout(d, vals, y=700)
    if H0 <= t < R2:                                   # giu yen: dem thoi gian, T van 476
        k = appear(t, H0, 0.3)
        card(d, (740, 438, 1040, 522), fill=A(WHITE, k), outline=A(NAVY, k), r=20, w=3)
        text(d, (890, 480), "giữ yên…", 40, NAVY, alpha=k)
    ks = [appear(t, R1, 0.4), appear(t, R2, 0.4), appear(t, R3, 0.4)]
    table(d, 820, ks, hlq=appear(t, R3 + 0.6, 0.4))
    k = appear(t, R3 + 0.6, 0.4)
    if k > 0: text(d, (690, 1290), "Q luôn bằng 0", 42, ORANGE, alpha=k)
    text(d, (W / 2, 1420), "ΔU = A + Q", 60, INK)
    tag(d, 1530)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, M[0] + 0.1, 0.4)
    pw = tw(d, "ĐÁP ÁN C", F(40)) + 56
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 336), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 303), "ĐÁP ÁN C", 40, WHITE, alpha=ka)
    text(d, (W / 2, 410), "300 K  →  ≈ 476 K", 60, RED, alpha=ka)
    k1 = appear(t, M[0] + 1.4, 0.45)
    card(d, (40, 480, 1040, 860), fill=A(WHITE, k1), outline=A(GREEN, k1), w=5)
    if k1 > 0:
        text(d, (W / 2, 550), "ΔU = A + Q", 64, INK, alpha=k1)
        text(d, (90, 650), "Q = 0", 46, ORANGE, anchor="lm", alpha=k1)
        text(d, (330, 650), "(cách nhiệt)", 42, NOTE, bold=False, anchor="lm", alpha=k1)
        text(d, (90, 730), "A > 0", 46, GREEN, anchor="lm", alpha=k1)
        text(d, (330, 730), "(bị nén)", 42, NOTE, bold=False, anchor="lm", alpha=k1)
        text(d, (90, 810), "ΔU = A > 0", 46, GREEN, anchor="lm", alpha=k1)
        text(d, (390, 810), "→ T tăng", 42, NOTE, bold=False, anchor="lm", alpha=k1)
    k2 = appear(t, M[1] + 0.2, 0.5)
    card(d, (40, 900, 1040, 1410), fill=A(WHITE, k2), outline=A(LIGHT, k2), w=3)
    if k2 > 0:
        # co che: pit-tong tien sang trai, phan tu bat ra nhanh hon
        px = 700
        hatch_v(d, px, px + 26, 960, 1200) if k2 > 0.5 else None
        arrow(d, (px + 150, 1080), (px + 46, 1080), A(RED, k2), w=8, head=22)
        dot(d, 676, 1030, 18, A(BLUE, k2))
        arrow(d, (520, 1030), (652, 1030), A(BLUE, k2), w=6, head=18)
        text(d, (470, 1030), "v", 44, BLUE, alpha=k2)
        kb = appear(t, M[1] + 1.0, 0.4)
        if kb > 0:
            dot(d, 676, 1150, 18, A(BLUE, kb))
            arrow(d, (652, 1150), (400, 1150), A(BLUE, kb), w=6, head=18)
            text(d, (300, 1150), "v′ > v", 44, BLUE, alpha=kb)
        ctext(d, 1330, "Phân tử bật khỏi pit-tông nhanh hơn", 44, INK, maxw=920, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
BX0, BX1, BY0, BY1, MID = 150, 930, 400, 580, 540
V0, V1 = 1.2, 1.7          # vach rut len
S0, S1 = 1.7, 3.3          # khi tran sang

def two_cells(d, t):
    hatch_h(d, BX0 - 24, BX1 + 24, BY0 - 24, BY0); hatch_h(d, BX0 - 24, BX1 + 24, BY1, BY1 + 24)
    hatch_v(d, BX0 - 24, BX0, BY0, BY1); hatch_v(d, BX1, BX1 + 24, BY0, BY1)
    kr = ease((t - S0) / (S1 - S0))
    xr = lerp(MID - 10, BX1, kr)
    gas(d, phase(t, lambda _: 300) * 1.4, BX0, xr, BY0, BY1, r=9)
    if kr < 0.5: text(d, ((MID + BX1) / 2, (BY0 + BY1) / 2), "chân không", 40, NOTE, bold=False, alpha=1 - 2 * kr)
    lift = ease((t - V0) / (V1 - V0))
    yv = BY0 - lift * 150
    if lift < 1:
        d.rectangle([MID - 10, yv, MID + 10, yv + (BY1 - BY0)], fill=A(NAVY, 1 - lift))
    if V0 - 0.4 < t < V1 + 0.6:
        arrow(d, (MID + 50, BY0 - 36), (MID + 50, BY0 - 140), RED, w=7, head=20)
    p = "p = 2,0·10⁵ Pa" if t < S0 else ("p ↓" if t < S1 else "p = 1,0·10⁵ Pa")
    vv = "V = 50 cm³" if t < S0 else ("V ↑" if t < S1 else "V = 100 cm³")
    readout(d, (vv, "T = 300 K", p), y=680)

def strike_q(d, y, q, ks, alpha):
    f = F(44); ls = wrap(d, q, f, 880)
    for i, l in enumerate(ls):
        yy = y + i * 56
        text(d, (W / 2, yy), l, 44, mix(INK, GRAY, ks), alpha=alpha)
        if ks > 0:
            lw = tw(d, l, f)
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * alpha), width=5)
    return len(ls)

def s_bay(img, d, t, sc):
    M = sc["M"]
    two_cells(d, t)
    k1 = appear(t, 0.2, 0.4); k3 = appear(t, M[1] - 0.1, 0.45)
    mk = 2.0; a1 = k1 * (1 - k3)
    y = 770
    if a1 > 0:
        card(d, (40, y, 1040, y + 580), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(RED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        strike_q(d, y + 170, "“V gấp đôi: khí sinh công, lạnh đi”", clamp((t - mk) / 0.4), a1)
        k2 = a1 * appear(t, mk, 0.45)
        text(d, (W / 2, y + 330), "Khí không đẩy vật nào", 46, INK, alpha=k2)
        for j, s in enumerate(("A = 0", "Q = 0", "ΔU = 0")):
            cx = 210 + j * 330
            card(d, (cx - 140, y + 400, cx + 140, y + 500), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=22, w=4)
            text(d, (cx, y + 450), s, 46, GREEN, alpha=k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 700), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 70), "Chưa nói được", 48, NAVY, alpha=k3)
        lines = ("• Thành xilanh thật dẫn nhiệt chậm", "• Chỉ đúng khí lí tưởng", "• A suy ra, không đo trực tiếp")
        for j, l in enumerate(lines):
            kk = k3 * appear(t, M[1] + 0.2 + 0.4 * j, 0.4)
            text(d, (90, y + 240 + j * 170), l, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    """Xilanh thuong (khong cach nhiet) thu nho, mui ten nen, so chi T = 300 K: minh hoa cau hoi."""
    if k <= 0: return
    x0, x1, y0, y1 = 200, 640, 1000, 1180
    d.rectangle([x0 - 16, y0 - 16, x1, y0], fill=A(GRAY, k)); d.rectangle([x0 - 16, y1, x1, y1 + 16], fill=A(GRAY, k))
    d.rectangle([x0 - 16, y0, x0, y1], fill=A(GRAY, k))
    xp = 470
    d.rectangle([xp, y0 + 2, xp + 18, y1 - 2], fill=A(NAVY, k)); d.rectangle([xp + 18, y0 + 80, xp + 160, y0 + 98], fill=A(NAVY, k))
    for i, (u, v) in enumerate(((0.2, 0.3), (0.5, 0.7), (0.8, 0.4), (0.35, 0.8), (0.65, 0.2), (0.1, 0.6))):
        dot(d, x0 + 20 + u * (xp - x0 - 40), y0 + 20 + v * (y1 - y0 - 40), 9, A(BLUE, k))
    arrow(d, (xp + 250, y0 + 40), (xp + 190, y0 + 40), A(RED, k), w=7, head=20)
    card(d, (720, y0 + 40, 960, y0 + 140), fill=A(WHITE, k), outline=A(NAVY, k), r=20, w=3)
    text(d, (840, y0 + 90), "T = 300 K", 42, INK, alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Cách nhiệt: Q = 0,\nnhưng ΔU vẫn đổi theo A",
             "Xilanh không cách nhiệt, nén khí, T giữ 300 K. Q dương hay âm?", None, body=_end_body)
    kh = appear(t, M[0] + 3.0, 0.5)                 # goi y hien tre: chi du kien
    if kh > 0:
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1350, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1450, "Quy ước: khí nhận công A > 0,\nnhận nhiệt Q > 0", 42, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + C0, "tap"), (do["t0"] + P0, "tap"),
            (da["t0"] + da["M"][0] + 0.1, "ding"),
            (b["t0"] + b["M"][0], "buzz"), (b["t0"] + V0, "tap"),
            (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-noinang-04", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Nội năng · Định luật 1 NĐLH · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xilanh cách nhiệt", draw=s_hook, tail=0.3, caps=[
   ("Xilanh, pit-tông cách nhiệt.", 3.2),
   ("Dừng lại, tự đoán.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Nén nhanh, ghi A, Q, ΔU.", 4.4),
   ("Giữ yên, rồi kéo về.", 5.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Nhiệt độ tăng. Đáp án C.", 3.6),
   ("Nội năng tăng nhờ nhận công.", 4.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Rút vách: khí sinh công?", 6.8),
   ("Chưa nói được gì?", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, trả lời.", 6.0)]),
])
