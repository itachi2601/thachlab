# Clip: tn-l12-hatnhan-02 - Do be day la nhom, dem so lop nguyen tu, so co hat nhan voi nguyen tu
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-hatnhan-02.json (so_lieu_mau, so_lieu_mau_ban_kinh, tham_so, cac_buoc).
# Ban 1-3 (28/10/2026). Dung lai 26/11/2026 theo KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32: cong --do-chu, chu >= 56 px khi ve,
#   <= 50 s, Du doan khong nut A-D (K10); bo phan sai so 3 la (giu trong kho), chot moi.
# Du doan (hien_tuong_hay_sai[1] "la nhom chi vai lop"): doc be day co bao nhieu lop? -> khoang 36 000 lop.
#   d = 0,27.10^-3 / (2700 . 0,1 . 0,1) = 1,0.10^-5 m ; 1,0.10^-5 / 2,8.10^-10 = 35 700 ~ 36 000.
# Bay (hien_tuong_hay_sai[0]): R ti le thuan voi A -> vang gap 7,3 lan nhom; that: 7,0/3,6 = 1,94 (R ti le A^(1/3)).
# Hat nhan nhom: R = 1,2.10^-15 . 27^(1/3) = 3,6.10^-15 m; r nguyen tu 1,4.10^-10 m -> nho hon ~ 39 000 lan (hang van).
# Cau THU NGHI (= cau_chot khung web, CA TU SUY tu mo hinh d = m/(D.a.b), khong co trong so_lieu_mau): la 100 x 100 mm
#   nang 0,54 g -> d = 2,0.10^-5 m -> khoang 71 000 ~ 72 000 lop (gap doi). Khac canh Tien hanh (la 2 nua dien tich, nua khoi luong).
from engine import *

DORANGE = (154, 52, 18); DRED = (185, 28, 28)
SHEETS = [(1, 100, 100, "0,27", "10,0", "36 000"), (2, 100, 50, "0,14", "10,4", "37 000"),
          (3, 150, 100, "0,41", "10,1", "36 000")]
RADII = [("Nhôm", 27, "3,6"), ("Đồng", 63, "4,8"), ("Vàng", 197, "7,0")]   # so_lieu_mau_ban_kinh (10^-15 m)

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-hatnhan-02.json")))
    h = k["so_lieu_mau"]["hang"]
    assert [r[1:] for r in h] == [[10.0, 36000.0], [10.4, 37000.0], [10.1, 36000.0]]
    assert {p["ky_hieu"]: p for p in k["tham_so"]}["D"]["gia_tri"] == 2700
    s = json.dumps(k.get("so_lieu_mau_ban_kinh"), ensure_ascii=False)
    for v in ("3.6", "4.8", "7.0"): assert v in s or v.replace(".", ",") in s, v
    assert abs(0.27e-3 / (2700 * 0.1 * 0.1) / 2.8e-10 - 36000) < 500
    assert abs(0.54e-3 / (2700 * 0.1 * 0.1) / 2.8e-10 - 71400) < 500
_kiem_so()

def rich2(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    segs = []
    for p in [p for p in TOK.split(s) if p]:
        if p.startswith("^{"): segs.append((p[2:-1], max(56, int(size * 0.9)), -size * 0.36))
        elif p.startswith("_{"): segs.append((p[2:-1], int(size * 0.72), size * 0.28))
        else: segs.append((p, size, 0))
    tot = sum(tw(d, t, F(sz)) for t, sz, _ in segs)
    x = cx - tot / 2 if anchor == "m" else cx
    for t, sz, dy in segs:
        dtext(d, (x, cy + dy), t, F(sz), color, alpha, "lm"); x += tw(d, t, F(sz))

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

# ---------------- dung cu: can dien tu + tam la nhom co kich thuoc ----------------
CX, YB = 470, 800
def plerp(p, q, k): return (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)
def sheet(d, a, b, k=1.0):
    w, h = a * 2.6, b * 1.15; sk = h * 0.8; x0 = CX - (w + sk) / 2
    pts = [(x0, YB), (x0 + w, YB), (x0 + w + sk, YB - h), (x0 + sk, YB - h)]
    d.polygon(pts, fill=A((206, 212, 224), k), outline=A(GRAY, k))
    for j in (0.3, 0.55):
        p = plerp(pts[0], pts[3], j)
        d.line([p[0] + 30, p[1], p[0] + 30 + w * 0.35, p[1]], fill=A(WHITE, 0.8 * k), width=4)
    return pts

def rig(d, i, reading, dims=True):
    d.polygon([(220, 950), (800, 950), (770, 818), (250, 818)], fill=(214, 220, 232), outline=NAVY)
    d.rounded_rectangle([270, 808, 750, 822], radius=6, fill=NAVY)
    d.rounded_rectangle([340, 840, 680, 930], radius=14, fill=NAVY)
    text(d, (510, 885), reading, 64, (134, 239, 172))
    _, a, b, *_ = SHEETS[i]
    p = sheet(d, a, b)
    if not dims: return
    y = p[3][1] - 34
    for q in (p[3], p[2]): arrow(d, ((p[3][0] + p[2][0]) / 2, y), (q[0], y), BLUE, w=4, head=14)
    text(d, ((p[3][0] + p[2][0]) / 2, y - 50), f"a = {a} mm", 56, BLUE)
    q1, q2 = (p[1][0] + 26, p[1][1]), (p[2][0] + 26, p[2][1])
    for q in (q1, q2): arrow(d, plerp(q1, q2, 0.5), q, BLUE, w=4, head=14)
    text(d, (max(q1[0], q2[0]) + 14, (q1[1] + q2[1]) / 2), f"b = {b} mm", 56, BLUE, anchor="lm")

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    rig(d, 0, "0,27 g")
    M = sc["M"]; a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 580), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 66, "DỰ ĐOÁN", PURPLE, a)
    seg_bar(d, y0 + 130, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, a)
    text(d, (W / 2, y0 + 285), "Nhôm: D = 2700 kg/m³", 58, INK, alpha=a)
    rich2(d, W / 2, y0 + 380, "nguyên tử cỡ 2,8×10^{−10} m", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 490), "Dọc bề dày có mấy lớp?", 62, PURPLE, alpha=a)

# ---------------- canh 2: Tien hanh - 3 la, tinh d va so lop ----------------
T_D, T_N, T_R = 2.4, 4.8, 7.4           # hien cot d / so lop la 1, roi hang la 2, 3
def s_do(img, d, t, sc):
    i = 0 if t < T_R else (1 if t < T_R + 0.5 else 2)
    rig(d, i, f"{SHEETS[i][3]} g", dims=(i == 0))
    if i > 0: text(d, (W / 2, 640), f"lá {i + 1}: {SHEETS[i][1]} × {SHEETS[i][2]} mm", 56, BLUE)
    rich2(d, W / 2, 330, "d = m : (D·a·b)", 60, INK)
    k2 = appear(t, T_D, 0.45)
    rich2(d, W / 2, 440, "số lớp = d : 2,8×10^{−10} m", 58, GREEN, alpha=k2)
    card(d, (40, 1000, 1040, 1520), fill=WHITE, outline=NAVY, w=4)
    xs = [210, 470, 680, 890]
    for x, c in zip(xs, ["a × b (mm)", "m (g)", "d (µm)", "số lớp"]): text(d, (x, 1060), c, 56, NOTE)
    d.line([(70, 1100), (1010, 1100)], fill=LIGHT, width=4)
    for j, (n, a, b, m, dd, nl) in enumerate(SHEETS):
        y = 1170 + j * 105
        t0 = 0.0 if j == 0 else T_R + 0.4 * (j - 1)
        k1 = 1.0 if j == 0 else appear(t, t0, 0.35)
        if k1 <= 0: continue
        if j == i: d.rounded_rectangle([60, y - 44, 1020, y + 44], radius=14, fill=A((225, 236, 255), k1))
        if j == 0 and T_D < t < T_R:                         # o dang tinh nhap nhay: cot d roi cot so lop
            xc = xs[2] if t < T_N else xs[3]
            pz = 0.5 + 0.5 * math.sin((t - T_D) * 2 * math.pi / 1.0)
            d.rounded_rectangle([xc - 110, y - 44, xc + 110, y + 44], radius=14, fill=A((134, 239, 172), 0.2 + 0.8 * pz))
        text(d, (xs[0], y), f"{a} × {b}", 58, INK, alpha=k1)
        text(d, (xs[1], y), m, 58, INK, alpha=k1)
        text(d, (xs[2], y), dd, 58, BLUE, alpha=appear(t, T_D + 0.3 if j == 0 else t0, 0.35))
        text(d, (xs[3], y), nl, 58, GREEN, alpha=appear(t, T_N if j == 0 else t0, 0.35))
NOTE = (70, 75, 95)

# ---------------- canh 3: Dap an - mat cat la ----------------
def s_ans(img, d, t, sc):
    M = sc["M"]
    pill(d, W / 2, 310, "ĐÁP ÁN: khoảng 36 000 lớp", GREEN, appear(t, 0.2, 0.4))
    card(d, (40, 390, 1040, 1300), fill=WHITE, outline=LIGHT, w=3)
    a = appear(t, 0.5, 0.6)
    r = 30; x0 = 170
    rows_top = [470 + j * 2 * r for j in range(4)]
    rows_bot = [930 + j * 2 * r for j in range(4)]
    for n, yy in enumerate(rows_top + rows_bot):
        off = r if n % 2 else 0
        for c in range(11):
            x = x0 + off + c * 2 * r
            if x > 790: continue
            dot(d, x, yy, r - 3, A((200, 208, 222), a), A(GRAY, a))
    for xx in range(x0 - 20, 790, 44):                       # dau ngat: nhieu lop bi luoc
        d.line([(xx, 770), (xx + 22, 756)], fill=A(MUTED, a), width=5)
        d.line([(xx, 800), (xx + 22, 786)], fill=A(MUTED, a), width=5)
    yt, yb = rows_top[0] - r, rows_bot[-1] + r
    kb = appear(t, M[1] + 0.2, 0.45)
    for q in (yt, yb): arrow(d, (880, (yt + yb) / 2), (880, q), A(BLUE, kb), w=5, head=18)
    text(d, (900, (yt + yb) / 2 - 50), "d ≈", 60, BLUE, alpha=kb, anchor="lm")
    text(d, (900, (yt + yb) / 2 + 30), "10 µm", 60, BLUE, alpha=kb, anchor="lm")

# ---------------- canh 4: hat nhan nho co nao ----------------
def s_why(img, d, t, sc):
    M = sc["M"]
    cx, cy, R = 300, 560, 230
    for j in range(10, 0, -1):
        rr = R * j / 10
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=mix((235, 241, 255), (190, 208, 245), 1 - j / 10))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=BLUE, width=4)
    d.line([(cx, cy), (cx + R, cy)], fill=BLUE, width=4)
    text(d, (cx + R / 2, cy - 40), "r", 60, BLUE)
    dot(d, cx, cy, 9, RED, NAVY)
    rich2(d, 790, 470, "r ≈ 1,4×10^{−10} m", 56, BLUE)
    text(d, (790, 570), "nguyên tử", 56, BLUE)
    k1 = appear(t, 2.2, 0.45)
    card(d, (40, 850, 1040, 1100), fill=A(WHITE, k1), outline=A(RED, k1), r=24, w=4)
    rich2(d, W / 2, 920, "R = 1,2×10^{−15} × 27^{1/3}", 58, INK, alpha=k1)
    rich2(d, W / 2, 1030, "= 3,6×10^{−15} m", 62, RED, alpha=k1)
    if k1 > 0:
        d.line([(cx + 8, cy + 6), (cx + 30, 840)], fill=A(RED, k1), width=4)
    k2 = appear(t, M[1] + 1.4, 0.45)
    if k2 > 0:
        card(d, (40, 1150, 1040, 1310), fill=A((239, 246, 255), k2), outline=A(BLUE, k2), r=24, w=5)
        text(d, (W / 2, 1230), "Nhỏ hơn hàng vạn lần", 62, BLUE, alpha=k2)

# ---------------- canh 5: Bay R ti le thuan voi A ----------------
def s_trap(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.4)
    card(d, (40, 260, 1040, 1150), fill=A(WHITE, k0), outline=A(RED, k0), w=6)
    pill(d, W / 2, 330, "BẪY", RED, k0)
    text(d, (W / 2, 440), "“R tỉ lệ thuận với A”?", 60, INK, alpha=k0)
    rich2(d, W / 2, 530, "R (×10^{−15} m)", 56, NOTE, alpha=k0)
    x0, px = 340, 70
    for j, (nm, A_, Rv) in enumerate(RADII):
        y = 640 + j * 150; aj = appear(t, 0.5 + j * 0.4, 0.4)
        text(d, (80, y - 24), nm, 58, INK, anchor="lm", alpha=aj)
        text(d, (80, y + 34), f"A = {A_}", 56, NOTE, anchor="lm", alpha=aj)
        L = float(Rv.replace(",", ".")) * px * ease((t - 0.5 - j * 0.4) / 0.6)
        if L > 2: d.rounded_rectangle([x0, y - 30, x0 + L, y + 30], radius=14, fill=A(BLUE, aj))
        text(d, (x0 + L + 18, y), Rv, 58, BLUE, anchor="lm", alpha=aj)
    g = appear(t, M[1] + 0.2, 0.45)                         # vang neu ti le thuan: 3,6 x 7,3 = 26 -> vuot khung
    if g > 0:
        y = 1060; Lg = (1000 - x0) * ease((t - M[1] - 0.2) / 1.0)
        for xx in range(x0, int(x0 + Lg), 34):
            d.line([(xx, y), (min(xx + 18, x0 + Lg), y)], fill=A(RED, g), width=10)
        if Lg > 600: arrow(d, (980, y), (1025, y), A(RED, g), w=8, head=18)
        text(d, (80, y), "×7,3?", 58, RED, anchor="lm", alpha=g)
    kp = appear(t, M[1] + 1.4, 0.3)                        # nhap nhay vang that: R chi ~ gap doi nhom
    if kp > 0:
        pz = 0.5 + 0.5 * math.sin((t - M[1] - 1.4) * 2 * math.pi / 1.2)
        y = 640 + 2 * 150
        d.rounded_rectangle([x0 - 16, y - 50, x0 + 7.0 * px + 130, y + 50], radius=20, outline=A(GREEN, kp * (0.3 + 0.7 * pz)), width=8)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 260, 1040, 1540), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 340, "THỬ NGHĨ", ORANGE, k1)
    seg_bar(d, 420, t, 0.8, sc["T"] - 0.2, ORANGE, k1)
    text(d, (W / 2, 570), "Lá 100 × 100 mm nặng 0,54 g:", 60, INK, alpha=k1)
    text(d, (W / 2, 670), "dày khoảng bao nhiêu lớp?", 60, DORANGE, alpha=k1)
    d2 = ImageDraw.Draw(img, "RGBA")
    global YB
    yb0 = YB; YB = 1280
    try:
        d.polygon([(220, 1430), (800, 1430), (770, 1298), (250, 1298)], fill=A((214, 220, 232), k1), outline=A(NAVY, k1))
        d.rounded_rectangle([340, 1320, 680, 1410], radius=14, fill=A(NAVY, k1))
        text(d, (510, 1365), "0,54 g", 64, (134, 239, 172), alpha=k1)
        sheet(d, 100, 100, k1)
    finally:
        YB = yb0

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + T_N, "tap"), (an["t0"] + 0.2, "ding"),
            (tr["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]

SCENES = [
 dict(key="hook", title="Lá nhôm dày mấy lớp nguyên tử?", draw=s_hook, tail=0.3, caps=[
   ("Đo hai cạnh, rồi cân lá.", 3.2),
   ("Dừng lại, tự đoán.", 6.4)]),
 dict(key="do", title="Đo ba lá, tính bề dày", draw=s_do, tail=0.3, caps=[
   ("Tính bề dày d trước.", 2.8),
   ("Chia d cho cỡ nguyên tử.", 5.0)]),
 dict(key="ans", title="Đếm được bao nhiêu lớp?", draw=s_ans, tail=0.4, caps=[
   ("Hình chỉ vẽ vài lớp.", 2.8),
   ("Lá mỏng vẫn hàng vạn lớp.", 3.4)]),
 dict(key="why", title="Còn hạt nhân nhỏ cỡ nào?", draw=s_why, tail=0.4, caps=[
   ("Hạt nhân nhôm, A = 27:", 3.0),
   ("Công thức R chỉ gần đúng.", 3.4)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.6, caps=[
   ("Đúng hay sai?", 2.8),
   ("Vàng: R chỉ gấp đôi nhôm.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=3.0, caps=[
   ("Lá mỏng: hàng vạn lớp nguyên tử.", 3.8)]),
]

CLIP = dict(id="tn-l12-hatnhan-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Hạt nhân và nguyên tử · thachlab.id.vn", scenes=SCENES)
