# Clip: tn-l12-hatnhan-02 - Do be day la nhom, dem so lop nguyen tu, so co hat nhan voi nguyen tu
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-hatnhan-02.json (so_lieu_mau, so_lieu_mau_ban_kinh, tham_so, cac_buoc).
# Ban 1 (28/10/2026): mau boyle/phongxa2 (dung cu + bang), tieng bao cues, chot bang chot_hoi().
# Ban 3 (28/10/2026, cong B vong 2): rich2() so mu 0,75 co (1/3 phong 1,3x), hop du doan >= 8 s, can lai canh ans/why.
# Ban 2 (28/10/2026, cong B vong 1): de du doan du du kien, canh why hien buoc tinh R, bo glyph thieu, cau hoi chot dung du kien clip.
# Lua chon nhieu (suy tu so trong JSON, d = 1,0.10^-5 m cua la 1):
#   A "chi vai lop"  = hien_tuong_hay_sai[1]
#   B "36 lop"       = quen doi ca g->kg lan mm->m (sai_so_thuong_gap[2]): d nho di 10^-3 lan -> 36000/1000
#   D "1,4 ti lop"   = dem bang 2R hat nhan 7,2.10^-15 m (mo_hinh, cac_buoc.lam[2]): 1,0.10^-5 / 7,2.10^-15 = 1,39.10^9
import random
from engine import *

# so_lieu_mau.hang: (la, a mm, b mm, m g, d um, so lop)
SHEETS = [(1, 100, 100, "0,27", "10,0", "36 000"), (2, 100, 50, "0,14", "10,4", "37 000"),
          (3, 150, 100, "0,41", "10,1", "36 000")]
ERR = ["3,9 %", "7,4 %", "2,6 %"]                 # so_lieu_mau.ghi_chu: sai so tuong doi cua d
RADII = [("Nhôm", 27, "3,6"), ("Đồng", 63, "4,8"), ("Vàng", 197, "7,0")]   # so_lieu_mau_ban_kinh (10^-15 m)

def rich2(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    segs = []
    for p in [p for p in TOK.split(s) if p]:
        if p.startswith("^{"):
            z = 0.8 if "/" in p else 0.72                 # 1/3 phong ~1,3 lan so voi 0,6 cua rich()
            segs.append((p[2:-1], int(size * z), -size * 0.36))
        elif p.startswith("_{"): segs.append((p[2:-1], int(size * 0.72), size * 0.28))
        else: segs.append((p, size, 0))
    tot = sum(tw(d, t, F(sz)) for t, sz, _ in segs)
    x = cx - tot / 2 if anchor == "m" else cx
    for t, sz, dy in segs:
        dtext(d, (x, cy + dy), t, F(sz), color, alpha, "lm"); x += tw(d, t, F(sz))

# ---------------- dung cu: can dien tu + tam la nhom co kich thuoc ----------------
CX, YB = 500, 800
def sheet(d, a, b, k=1.0):
    w, h = a * 2.6, b * 1.15; sk = h * 0.8; x0 = CX - (w + sk) / 2
    pts = [(x0, YB), (x0 + w, YB), (x0 + w + sk, YB - h), (x0 + sk, YB - h)]
    d.polygon(pts, fill=A((206, 212, 224), k), outline=A(GRAY, k))
    for j in (0.3, 0.55):                                   # anh kim loai
        d.line([lerp(pts[0], pts[3], j)[0] + 30, lerp(pts[0], pts[3], j)[1],
                lerp(pts[0], pts[3], j)[0] + 30 + w * 0.35, lerp(pts[0], pts[3], j)[1]], fill=A(WHITE, 0.8 * k), width=4)
    return pts
def lerp(p, q, k): return (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k) if isinstance(p, tuple) else p + (q - p) * k

def rig(d, t, i, reading, dims=1.0):
    # can dien tu
    d.polygon([(250, 930), (830, 930), (800, 818), (280, 818)], fill=(214, 220, 232), outline=NAVY)
    d.rounded_rectangle([300, 808, 780, 822], radius=6, fill=NAVY)            # dia can
    d.rounded_rectangle([410, 846, 670, 914], radius=12, fill=NAVY)
    text(d, (540, 880), reading, 48, (134, 239, 172))
    text(d, (540, 962), "cân điện tử", 34, MUTED, bold=False)
    _, a, b, *_ = SHEETS[i]
    p = sheet(d, a, b)
    if dims <= 0: return
    # kich thuoc a (canh sau), b (canh phai)
    y = p[3][1] - 34
    arrow(d, ((p[3][0] + p[2][0]) / 2, y), (p[3][0], y), A(BLUE, dims), w=4, head=14)
    arrow(d, ((p[3][0] + p[2][0]) / 2, y), (p[2][0], y), A(BLUE, dims), w=4, head=14)
    text(d, ((p[3][0] + p[2][0]) / 2, y - 40), f"a = {a} mm", 38, BLUE, alpha=dims)
    q1, q2 = (p[1][0] + 26, p[1][1]), (p[2][0] + 26, p[2][1])
    arrow(d, lerp(q1, q2, 0.5), q1, A(BLUE, dims), w=4, head=14)
    arrow(d, lerp(q1, q2, 0.5), q2, A(BLUE, dims), w=4, head=14)
    text(d, (max(q1[0], q2[0]) + 18, (q1[1] + q2[1]) / 2), f"b = {b} mm", 38, BLUE, anchor="lm", alpha=dims)

# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. Chỉ vài lớp", "B. Khoảng 36 lớp", "C. Khoảng 36 000 lớp", "D. Khoảng 1,4 tỉ lớp")
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, 0, "0,27 g", dims=appear(t, 0.8))
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1005, 1020, 1660), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1050), "Dự đoán", 44, PURPLE, alpha=k)
    ctext(d, 1108, "Lá 0,27 g; D = 2700 kg/m³", 40, INK, alpha=k)
    rich2(d, W / 2, 1162, "Nguyên tử nhôm: 2,8×10^{−10} m", 40, INK, alpha=k)
    ctext(d, 1222, "Dọc bề dày có bao nhiêu lớp?", 44, INK, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.15); y = 1298 + i * 76
        card(d, (110, y - 33, 970, y + 33), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=20, w=4)
        text(d, (150, y), s, 38, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1614, 940, 1628], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1614, 140 + 800 * (1 - q), 1628], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: do 3 la, tinh d va so lop ----------------
def tl(sc):
    M = sc["M"]   # moc hien: (o nhap, cot d, cot so lop) cho tung la
    return [(M[0] + 0.9, M[0] + 2.0, M[1] + 0.8), (M[1] + 1.5, M[1] + 1.8, M[1] + 2.1), (M[1] + 2.5, M[1] + 2.8, M[1] + 3.1)]

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; T = tl(sc)
    i = 0 if t < T[1][0] - 0.3 else (1 if t < T[2][0] - 0.3 else 2)
    kin = clamp((t - 0.3) / 0.6) if i == 0 else 1.0
    rig(d, t, i, f"{SHEETS[i][3]} g" if kin >= 1 else "0,00 g", dims=kin)
    pw = tw(d, f"Lá {i + 1}", F(38)) + 50
    card(d, (80, 270, 80 + pw, 336), fill=NAVY, r=30); text(d, (80 + pw / 2, 303), f"Lá {i + 1}", 38, WHITE)
    # cong thuc
    f1 = appear(t, M[0] + 1.4)
    rich2(d, 650, 300, "d = m / (D·a·b)", 42, INK, alpha=f1)
    text(d, (650, 356), "D = 2700 kg/m³", 36, MUTED, bold=False, alpha=f1)
    f2 = appear(t, M[1] + 0.2)
    rich2(d, W / 2, 440, "Số lớp = d : (2,8×10^{−10} m)", 42, INK, alpha=f2)
    text(d, (W / 2, 500), "đường kính nguyên tử", 36, MUTED, bold=False, alpha=f2)
    # bang
    card(d, (60, 1010, 1020, 1600), fill=WHITE, outline=NAVY, w=4)
    xs = [130, 310, 520, 700, 880]
    for x, c in zip(xs, ["Lá", "a × b (mm)", "m (g)", "d (µm)", "Số lớp"]): text(d, (x, 1070), c, 36, MUTED)
    d.line([(90, 1108), (990, 1108)], fill=LIGHT, width=4)
    hl = appear(t, M[2] + 0.3)
    for j, (n, a, b, m, dd, nl) in enumerate(SHEETS):
        y = 1170 + j * 90; ta, tb, tc = T[j]
        k1 = appear(t, ta, 0.35)
        if k1 <= 0: continue
        if j == i and hl <= 0: d.rounded_rectangle([80, y - 36, 1000, y + 36], radius=14, fill=A((225, 236, 255), k1))
        text(d, (xs[0], y), str(n), 40, MUTED, alpha=k1)
        text(d, (xs[1], y), f"{a} × {b}", 40, INK, bold=False, alpha=k1)
        text(d, (xs[2], y), m, 40, INK, bold=False, alpha=k1)
        text(d, (xs[3], y), dd, 42, BLUE, alpha=appear(t, tb, 0.35))
        text(d, (xs[4], y), nl, 42, GREEN, alpha=appear(t, tc, 0.35))
    if hl > 0:
        d.rounded_rectangle([xs[4] - 105, 1128, xs[4] + 105, 1392], radius=18, outline=A(GREEN, hl), width=5)
        ctext(d, 1490, "hàng vạn lớp", 44, GREEN, alpha=hl)

# ---------------- canh 3: dap an C + mat cat phong to + sai so ----------------
RA = random.Random(5)
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = back((t - 0.2) / 0.5) if t > 0.2 else 0
    card(d, (60, 250, 1020, 350), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 300), "Đáp án C", int(48 * clamp(k, 0.3, 1.0)), GREEN)
    # mat cat la: vai lop dau + dau ngat + vai lop cuoi (chi minh hoa, khong ve du)
    card(d, (60, 380, 1020, 1000), fill=WHITE, outline=LIGHT, w=3)
    a = appear(t, 0.6, 0.6)
    r = 22; x0 = 210; cols = 15
    rows_top = [470 + j * 2 * r for j in range(4)]
    rows_bot = [770 + j * 2 * r for j in range(4)]
    for yy in rows_top + rows_bot:
        off = r if (rows_top + rows_bot).index(yy) % 2 else 0
        for c in range(cols):
            x = x0 + off + c * 2 * r
            if x > 760: continue
            dot(d, x, yy, r - 2, A((200, 208, 222), a), A(GRAY, a))
    for xx in range(x0 - 20, 640, 36):                     # dau ngat ≈ (nhieu lop bi luoc)
        d.line([(xx, 690), (xx + 18, 680)], fill=A(MUTED, a), width=4)
        d.line([(xx, 714), (xx + 18, 704)], fill=A(MUTED, a), width=4)
    text(d, (490, 650), "··· lược bớt ···", 36, MUTED, bold=False, alpha=a)
    # kich thuoc
    kb = appear(t, 1.4)
    yt, yb = rows_top[0] - r, rows_bot[-1] + r
    arrow(d, (850, (yt + yb) / 2), (850, yt), A(BLUE, kb), w=4, head=14)
    arrow(d, (850, (yt + yb) / 2), (850, yb), A(BLUE, kb), w=4, head=14)
    text(d, (835, (yt + yb) / 2), "d ≈ 10 µm", 36, BLUE, anchor="rm", alpha=kb)
    text(d, (W / 2, 958), "Mặt cắt, chỉ vẽ vài lớp", 36, MUTED, bold=False, alpha=a)
    # sai so: la nang nhat dang tin nhat
    e = appear(t, 1.5)
    if e <= 0: return
    card(d, (60, 1030, 1020, 1600), fill=A(WHITE, e), outline=A(BLUE, e), w=4)
    text(d, (W / 2, 1085), "Sai số của d", 44, BLUE, alpha=e)
    for j, (n, a_, b_, m, *_r) in enumerate(SHEETS):
        y = 1180 + j * 100; aj = appear(t, 1.8 + j * 0.3, 0.35)
        good = j == 2 and t > M[1] + 0.6
        if good: d.rounded_rectangle([100, y - 40, 980, y + 40], radius=16, fill=A((220, 252, 231), appear(t, M[1] + 0.6)))
        text(d, (140, y), f"Lá {n}: m = {m} g", 38, INK, bold=False, anchor="lm", alpha=aj)
        text(d, (940, y), ERR[j], 42, GREEN if good else INK, anchor="rm", alpha=aj)
    ctext(d, 1520, "Đáng tin nhất", 44, GREEN, alpha=appear(t, M[1] + 1.0))

# ---------------- canh 4: hat nhan nho co nao (tinh R tung buoc) + chua noi duoc gi ----------------
def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    cx, cy, R = 290, 470, 190                              # nguyen tu co dinh tu dau canh
    for j in range(10, 0, -1):                             # dam may electron
        rr = R * j / 10
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=mix((235, 241, 255), (190, 208, 245), 1 - j / 10))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=BLUE, width=3)
    d.line([(cx, cy), (cx + R, cy)], fill=BLUE, width=3)
    text(d, (cx + R / 2 + 20, cy - 26), "r", 38, BLUE)
    dot(d, cx, cy, 9, RED, NAVY)                           # hat nhan: van ve qua to
    rich2(d, 780, 392, "r ≈ 1,4×10^{−10} m", 42, BLUE)
    text(d, (780, 500), "chấm đỏ: hạt nhân", 40, RED)
    k1, k2, k3 = appear(t, 0.8), appear(t, 1.6), appear(t, 2.4)
    card(d, (60, 690, 1020, 1010), fill=A(WHITE, k1), outline=A(LIGHT, k1), r=24, w=3)
    text(d, (W / 2, 735), "Nhôm, A = 27", 40, MUTED, bold=False, alpha=k1)
    rich2(d, W / 2, 810, "R = 1,2×10^{−15} × 27^{1/3}", 44, INK, alpha=k1)
    rich2(d, W / 2, 885, "= 1,2×10^{−15} × 3", 44, INK, alpha=k2)
    rich2(d, W / 2, 962, "= 3,6×10^{−15} m", 48, RED, alpha=k3)
    kv = appear(t, 2.8)
    card(d, (60, 1030, 1020, 1160), fill=A(WHITE, kv), outline=A(LIGHT, kv), r=24, w=3)
    rich2(d, W / 2, 1095, "R tỉ lệ với A^{1/3}", 44, INK, alpha=kv)
    b = appear(t, M[1] + 0.1)
    card(d, (60, 1180, 1020, 1390), fill=A(WHITE, b), outline=A(BLUE, b), w=5)
    ctext(d, 1238, "Hạt nhân nhỏ hơn nguyên tử", 40, INK, alpha=b)
    ctext(d, 1322, "hàng chục nghìn lần", 48, BLUE, alpha=b)
    c = appear(t, M[1] + 1.2)
    card(d, (60, 1410, 1020, 1660), fill=A(WHITE, c), outline=A(PURPLE, c), w=5)
    text(d, (W / 2, 1455), "Chưa nói được gì?", 40, PURPLE, alpha=c)
    ctext(d, 1560, "Chỉ gần đúng:\nghi kèm sai số.", 42, INK, bold=False, alpha=c, lh=1.3)

# ---------------- canh 5: bay R ti le thuan voi A ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 340), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 295), "Bẫy: R tỉ lệ thuận với A", 44, RED, alpha=appear(t, 0.1))
    card(d, (60, 370, 1020, 1000), fill=WHITE, outline=LIGHT, w=3)
    rich2(d, W / 2, 420, "Bán kính hạt nhân R (×10^{−15} m)", 36, MUTED)
    x0, px = 330, 85
    for j, (nm, A_, Rv) in enumerate(RADII):
        y = 520 + j * 150; aj = appear(t, 0.4 + j * 0.35, 0.4)
        text(d, (100, y - 14), nm, 40, INK, anchor="lm", alpha=aj)
        text(d, (100, y + 30), f"A = {A_}", 34, MUTED, bold=False, anchor="lm", alpha=aj)
        L = float(Rv.replace(",", ".")) * px * ease((t - 0.4 - j * 0.35) / 0.6)
        if L > 2: d.rounded_rectangle([x0, y - 26, x0 + L, y + 26], radius=12, fill=A(BLUE, aj))
        text(d, (x0 + L + 16, y), Rv, 40, BLUE, anchor="lm", alpha=aj)
    # vang neu ti le thuan: gap 7,3 lan nhom -> vuot khung
    g = appear(t, 1.8)
    if g > 0:
        y = 820; Lg = 3.6 * px * lerp(1, 7.3, ease((t - 1.8) / 1.2))
        for xx in range(x0, int(min(x0 + Lg, 975)), 30):
            d.line([(xx, y + 70), (min(xx + 16, 975), y + 70)], fill=A(RED, g), width=8)
        if x0 + Lg > 975: arrow(d, (950, y + 70), (992, y + 70), A(RED, g), w=6, head=16)
        text(d, (W / 2, y + 125), "Nếu tỉ lệ: gấp 7,3 lần", 38, RED, alpha=g)
    c = appear(t, M[1] + 1.6)
    card(d, (60, 1030, 1020, 1600), fill=A((254, 242, 242), c), r=28)
    ctext(d, 1200, "A tăng 7,3 lần", 48, INK, alpha=c)
    ctext(d, 1290, "R chỉ tăng khoảng 2 lần", 52, GREEN, alpha=c)
    e = appear(t, M[1] + 2.4)
    rich2(d, W / 2, 1450, "Vì R tỉ lệ với A^{1/3}", 46, GREEN, alpha=e)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    chot_hoi(d, t, sc, "Lá nhôm hàng vạn lớp; hạt nhân rất nhỏ",
             "Lá to gấp đôi: số lớp thay đổi thế nào?")
    kh = appear(t, sc["M"][0] + 2.6, 0.5)                  # goi y hien muon ~2,5 s sau cau hoi
    if kh <= 0: return
    card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1360, "Gợi ý", 36, MUTED, bold=False, alpha=kh)
    ctext(d, 1445, "Diện tích gấp đôi: m thay đổi?", 42, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][2] + 0.3, "tap"), (an["t0"] + 0.2, "ding"),
            (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-hatnhan-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Hạt nhân và nguyên tử · thachlab.id.vn", scenes=[
 dict(key="hook", title="Lá nhôm dày mấy lớp nguyên tử?", draw=s_hook, tail=0.6, caps=[
   ("Đo hai cạnh, rồi cân.", 2.3),
   ("Chọn đáp án.", 9.0)]),
 dict(key="do", title="Đo ba lá, tính bề dày", draw=s_do, tail=0.6, caps=[
   ("Đo a, b, m; tính d.", 3.0),
   ("Chia cho đường kính.", 3.6),
   ("Ba lá, cùng cỡ.", 2.6)]),
 dict(key="ans", title="Đếm được bao nhiêu lớp?", draw=s_ans, tail=0.6, caps=[
   ("C: khoảng 36 000 lớp.", 3.0),
   ("Lá nặng nhất, sai số 2,6 %.", 3.0)]),
 dict(key="why", title="Còn hạt nhân nhỏ cỡ nào?", draw=s_why, tail=0.6, caps=[
   ("Mỗi lớp là nguyên tử.", 3.8),
   ("Hạt nhân ở tâm.", 3.8)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.6, caps=[
   ("Bẫy hay gặp.", 3.0),
   ("R chỉ tăng ≈ 2 lần.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Thử nghĩ.", 6.0)]),
])
