# Clip: tn-l12-mayphatdien-01 - May phat mini quay bang dong co: do tan so theo toc do quay de kiem f = np
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-mayphatdien-01.json (so_lieu_mau, tham_so).
# Ban 1 (28/10/2026): mau boyle/phongxa2 (dung cu + bang + do thi), tieng bao cues.
# Lua chon nhieu trong hop Du doan suy thang tu n = 25 vong/s, p = 2 (tham_so/so_lieu_mau):
#   A. 12,5 Hz = n/p (chia nham)   B. 25 Hz = n (quen p, hien_tuong_hay_sai #1)
#   C. 50 Hz  = n.p (dung, so do 50,3)   D. 100 Hz = n.2p (lay p = 4 vi "4 cuc", hien_tuong_hay_sai #3)
from engine import *

ROWS = [(5, 9.8, 1.96), (10, 20.1, 2.01), (15, 30.2, 2.01), (20, 39.6, 1.98), (25, 50.3, 2.01)]  # so_lieu_mau
P = 2                                               # tham_so: p mac dinh = 2 cap cuc (rô-to 2p = 4 cuc)
def fmt(v): return (f"{v:.1f}" if isinstance(v, float) else str(v)).replace(".", ",")
def fmt2(v): return f"{v:.2f}".replace(".", ",")
VIS = 0.05                                          # hinh quay cham: 1 vong/s that -> 0,05 vong/s tren man hinh

# ---------------- ro-to (2p cuc N/S xen ke) + stato co cuon day o dinh ----------------
def rotor(d, cx, cy, r, ang, p=P, a=1.0, lbl=True, mark=False):
    """ang (do, chieu kim dong ho): khi ang = 0 tam cuc N thu nhat nam o dinh (duoi cuon day)."""
    sec = 360 / (2 * p)
    for k in range(2 * p):
        a0 = -90 - sec / 2 + ang + k * sec
        col = (239, 68, 68) if k % 2 == 0 else (59, 130, 246)
        d.pieslice([cx - r, cy - r, cx + r, cy + r], a0, a0 + sec, fill=A(col, a), outline=A(NAVY, a), width=4)
        if lbl:
            m = math.radians(a0 + sec / 2)
            text(d, (cx + 0.62 * r * math.cos(m), cy + 0.62 * r * math.sin(m)), "N" if k % 2 == 0 else "S",
                 int(r * 0.3), WHITE, alpha=a)
    dot(d, cx, cy, r * 0.14, A(GRAY, a), A(NAVY, a))
    if mark:   # cham danh dau de dem vong
        m = math.radians(-90 + ang)
        dot(d, cx + 0.88 * r * math.cos(m), cy + 0.88 * r * math.sin(m), r * 0.09, A(YELLOW, a), A(NAVY, a))

def stator(d, cx, cy, r):
    ri, ro = r + 22, r + 50
    d.ellipse([cx - ro, cy - ro, cx + ro, cy + ro], fill=(200, 204, 214), outline=NAVY, width=4)
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=BG, outline=NAVY, width=4)
    # rang loi thep o dinh + cuon day dong quan quanh
    d.rectangle([cx - 26, cy - ri - 6, cx + 26, cy - r - 8], fill=(200, 204, 214), outline=NAVY, width=3)
    yt, yb = cy - ro - 4, cy - r - 10
    d.rounded_rectangle([cx - 46, yt + 18, cx + 46, yb], radius=10, fill=(214, 140, 60), outline=NAVY, width=3)
    for y in range(int(yt + 26), int(yb - 4), 11):
        d.line([(cx - 46, y), (cx + 46, y + 5)], fill=(150, 85, 30), width=3)
    return (cx - 24, yt + 18), (cx + 24, yt + 18)    # hai dau day ra

def cable(d, pts, a=1.0):
    d.line(pts, fill=A(GRAY, a), width=12, joint="curve")

RX, RY, RR = 300, 720, 140
def rig(d, t, n, ang, reading, lit):
    """n: toc do hien tren nhan (None = dung yen); reading: chuoi tren tan so ke; lit: 0..1 do sang den."""
    l1, l2 = stator(d, RX, RY, RR)
    rotor(d, RX, RY, RR, ang, mark=True)
    if n: arrow(d, (RX + RR + 70, RY - 70), (RX + RR + 70, RY + 40), ORANGE, w=6, head=18)
    text(d, (RX, RY + RR + 90), "rô-to: p = 2 cặp cực", 36, NAVY)
    # day noi: cuon day -> tan so ke, song song -> bong den
    cable(d, [l1, (l1[0], 490), (600, 490)])
    cable(d, [l2, (l2[0], 520), (580, 520), (580, 660), (805, 660), (805, 690)])
    # nhan toc do
    card(d, (60, 265, 560, 455), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (310, 310), "Tốc độ quay", 36, MUTED, bold=False)
    text(d, (310, 385), f"n = {n} vòng/s" if n else "n = 0", 54, BLUE)  # n: so (vong/s) hoac "···" khi dang tang toc
    if n: text(d, (310, 432), "(quay chậm lại)", 36, MUTED, bold=False)
    # tan so ke
    card(d, (600, 265, 1010, 600), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (805, 310), "Tần số kế", 36, MUTED, bold=False)
    d.rounded_rectangle([630, 350, 980, 470], radius=16, fill=NAVY)
    text(d, (805, 410), reading, 66, (134, 239, 172))
    text(d, (805, 520), "Hz", 40, MUTED)
    text(d, (805, 568), "sai số ±0,1 Hz", 36, MUTED, bold=False)
    # bong den nho mac song song
    if lit > 0:
        for rr, al in ((120, 0.18), (90, 0.28), (66, 0.4)):
            dot(d, 805, 770, rr * (0.6 + 0.4 * lit), A(YELLOW, al * lit))
    dot(d, 805, 770, 52, mix((235, 235, 235), (255, 236, 140), lit), NAVY)
    d.rectangle([785, 818, 825, 860], fill=GRAY, outline=NAVY, width=3)
    text(d, (805, 900), "đèn nhỏ", 36, MUTED, bold=False)

# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. 12,5 Hz", "B. 25 Hz", "C. 50 Hz", "D. 100 Hz")
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, None, 0, "– – –", 0)
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1000, 1020, 1600), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1055), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1155, "n = 25 vòng/s.\nTần số kế chỉ bao nhiêu?", 46, INK, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.15)
        x0 = 110 + (i % 2) * 440; y = 1300 + (i // 2) * 110
        card(d, (x0, y - 44, x0 + 420, y + 44), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=22, w=4)
        text(d, (x0 + 40, y), s, 42, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1540, 940, 1554], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1540, 140 + 800 * (1 - q), 1554], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh, ghi bang ----------------
RAMP = 0.6
def row_at(i, sc):
    M = sc["M"]
    return [M[1] + 0.5, M[2] + 0.6, M[2] + 1.6, M[2] + 2.6, M[3] + 0.7][i]

def n_at(t, sc):
    """toc do quay that (vong/s) tai thoi diem t: tang dan toi n cua hang i trong RAMP giay truoc row_at(i)."""
    if t < row_at(0, sc): return ROWS[0][0] * ease((t - 0.3) / 0.8)
    n = ROWS[0][0]
    for i in range(1, 5):
        s = row_at(i, sc) - RAMP
        if t < s: break
        n = lerp(ROWS[i - 1][0], ROWS[i][0], ease((t - s) / RAMP))
    return n

def do_state(t, sc):
    last = max([i for i in range(5) if t >= row_at(i, sc)], default=-1)
    ramping = any(row_at(i, sc) - RAMP <= t < row_at(i, sc) for i in range(1, 5))
    if last < 0 or ramping: return None if last < 0 else ROWS[last][0], "···", last
    return ROWS[last][0], fmt(ROWS[last][1]), last

def angle(t, f):  # tich phan toc do hien thi (do)
    s, x, dt = 0.0, 0.0, 1 / 60
    while x < t: s += 360 * VIS * f(x) * dt; x += dt
    return s

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    n_now = n_at(t, sc)
    nl, rd, last = do_state(t, sc)
    lbl = "···" if rd == "···" and n_now > 0.05 else nl
    rig(d, t, lbl, angle(t, lambda x: n_at(x, sc)), rd, n_now / ROWS[-1][0])
    # dong ho bam giay: dem vong trong 10 s (kim quay 1 vong tuong trung, truoc khi ghi hang dau)
    kw = appear(t, 0.4, 0.3) * (1 - appear(t, row_at(0, sc) + 0.6, 0.3))
    if kw > 0:
        q = clamp((t - 1.2) / (row_at(0, sc) - 1.4)); sx, sy, sr = 575, 860, 52
        d.rectangle([sx - 10, sy - sr - 18, sx + 10, sy - sr], fill=A(NAVY, kw))
        dot(d, sx, sy, sr, A(WHITE, kw), A(NAVY, kw))
        if q > 0: d.pieslice([sx - sr + 8, sy - sr + 8, sx + sr - 8, sy + sr - 8], -90, -90 + 360 * q, fill=A((191, 219, 254), kw))
        m = math.radians(-90 + 360 * q)
        d.line([(sx, sy), (sx + (sr - 10) * math.cos(m), sy + (sr - 10) * math.sin(m))], fill=A(RED, kw), width=5)
        text(d, (sx, sy + sr + 30), "đếm 10 s", 36, BLUE, alpha=kw)
    card(d, (60, 1000, 1020, 1590), fill=WHITE, outline=NAVY, w=4)
    xs = [190, 470, 790]
    for x, c in zip(xs, ["Lần", "n (vòng/s)", "f đo (Hz)"]): text(d, (x, 1055), c, 38, MUTED)
    d.line([(90, 1090), (990, 1090)], fill=LIGHT, width=4)
    for i, (n, f, _) in enumerate(ROWS):
        a = appear(t, row_at(i, sc) - 0.3, 0.3); y = 1145 + i * 84
        if a <= 0: continue
        if i == last: d.rounded_rectangle([80, y - 34, 1000, y + 34], radius=16, fill=A((225, 236, 255), a))
        for x, s, col in zip(xs, [str(i + 1), str(n), fmt(f)], [MUTED, BLUE, RED]):
            text(d, (x, y), s, 44, col, alpha=a)

# ---------------- canh 3: dap an C + do thi f(n) + ti so f/n ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = back((t - 0.2) / 0.5) if t > 0.2 else 0
    card(d, (60, 250, 1020, 350), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 300), "Đáp án C", int(48 * clamp(k, 0.3, 1.0)), GREEN)
    x0, x1, yb, yt = 190, 950, 940, 470
    X = lambda n: x0 + n / 30 * (x1 - x0); Y = lambda f: yb - f / 60 * (yb - yt)
    card(d, (60, 380, 1020, 1050), fill=WHITE, outline=LIGHT, w=3)
    for f in (20, 40, 60): d.line([(x0, Y(f)), (x1, Y(f))], fill=(240, 236, 228), width=2)
    d.line([(x0, yb), (x1 + 25, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 40)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 50), "f đo (Hz)", 36, MUTED, anchor="lm")
    text(d, (x1 + 25, yb + 78), "n (vòng/s)", 36, MUTED, anchor="rm")
    for n in range(0, 31, 5):
        d.line([(X(n), yb), (X(n), yb + 10)], fill=NAVY, width=3); text(d, (X(n), yb + 36), str(n), 36, MUTED, bold=False)
    for f in (0, 20, 40, 60):
        d.line([(x0 - 10, Y(f)), (x0, Y(f))], fill=NAVY, width=4); text(d, (x0 - 18, Y(f)), str(f), 36, MUTED, bold=False, anchor="rm")
    kc = ease((t - M[1] - 0.2) / 1.2)
    if kc > 0:
        d.line([(X(0), Y(0)), (X(30 * kc), Y(2 * 30 * kc))], fill=A(BLUE, 0.5), width=7)
        text(d, (X(9), Y(30)), "f = 2n", 44, BLUE, alpha=appear(t, M[1] + 1.2))
        dot(d, X(0), Y(0), 10, BLUE)
    for i, (n, f, _) in enumerate(ROWS):
        a = appear(t, 0.5 + i * 0.2, 0.4)
        if a > 0: dot(d, X(n), Y(f), 15 * back(a), ORANGE, WHITE)
    a = appear(t, 0.5 + 4 * 0.2, 0.4)
    text(d, (X(25) + 28, Y(ROWS[4][1]) + 34), "50,3", 38, ORANGE, anchor="lm", alpha=a)
    # day ti so f/n
    a1 = appear(t, M[2] - 0.9)
    if a1 <= 0: return
    card(d, (60, 1080, 1020, 1590), fill=A(WHITE, a1), outline=A(LIGHT, a1), w=3)
    text(d, (W / 2, 1130), "Tỉ số f/n", 44, MUTED, alpha=a1)
    vx = [160 + i * 190 for i in range(5)]
    for i, (n, f, r) in enumerate(ROWS):
        text(d, (vx[i], 1210), f"{fmt(f)}/{n}", 38, MUTED, bold=False, alpha=a1)
        text(d, (vx[i], 1285), fmt2(r), 48, ORANGE, alpha=appear(t, M[2] - 0.6 + i * 0.15, 0.3))
    c = appear(t, M[2] + 0.2, 0.3)
    card(d, (130, 1360, 950, 1550), fill=A((220, 252, 231), c), r=24)
    ctext(d, 1415, "f/n ≈ 2 = số cặp cực p", 50, GREEN, alpha=c)
    ctext(d, 1495, "lệch chút: quay không đều", 40, MUTED, bold=False, alpha=c)

# ---------------- canh 4: co che - moi vong cho p chu ki ----------------
WX0, WX1, WY = 150, 950, 1110
def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    th = 360 * ease((t - M[0] - 0.4) / 4.1)           # quay dung 1 vong, cham
    cx, cy, r = W / 2, 590, 150
    stator(d, cx, cy, r)
    rotor(d, cx, cy, r, th)
    text(d, (cx + r + 140, cy - 150), "cuộn dây", 36, (150, 85, 30))
    arrow(d, (cx + r + 70, cy - 150), (cx + 60, cy - r - 40), (150, 85, 30), w=4, head=14)
    text(d, (cx, cy + r + 80), f"góc quay: {round(th)}°", 40, BLUE)
    # do thi suat dien dong theo goc quay: e ~ sin(p.theta)
    card(d, (60, 900, 1020, 1320), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 945), "Điện áp trên cuộn dây", 36, MUTED)
    d.line([(WX0, WY), (WX1, WY)], fill=NAVY, width=4)
    for deg in (0, 180, 360):
        xx = WX0 + deg / 360 * (WX1 - WX0)
        d.line([(xx, WY - 8), (xx, WY + 8)], fill=NAVY, width=3)
        text(d, (xx, WY + 150), f"{deg}°", 36, MUTED, bold=False)
    nseg = int(200 * th / 360)
    if nseg >= 2:
        pts = [(WX0 + j / 200 * (WX1 - WX0), WY - 110 * math.sin(math.radians(P * 360 * j / 200))) for j in range(nseg + 1)]
        d.line(pts, fill=ORANGE, width=6, joint="curve")
    cyc = int(P * th / 360 + 1e-6)
    a = appear(t, 0.3)
    card(d, (60, 1350, 1020, 1590), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    text(d, (W / 2, 1410), f"Số chu kì: {cyc}", 46, ORANGE, alpha=a)
    rich(d, W / 2, 1515, "1 vòng = p chu kì → f = n·p", 46, BLUE, alpha=appear(t, M[1] + 0.3))

# ---------------- canh 5: chua noi duoc gi + bay p = 4 ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 250, 1020, 520), fill=WHITE, outline=BLUE, w=6)
    text(d, (W / 2, 305), "Chưa nói được gì?", 44, BLUE, alpha=a)
    ctext(d, 420, "Chỉ một máy p = 2:\nchưa kiểm f tỉ lệ p.", 44, INK, alpha=a, lh=1.25)
    b = appear(t, 0.3)
    if b <= 0: return
    card(d, (60, 560, 1020, 1590), fill=A(WHITE, b), outline=A(RED, b), w=6)
    text(d, (W / 2, 615), "Bẫy: đếm cực thay vì cặp cực", 44, RED, alpha=b)
    cx, cy, r = W / 2, 860, 150
    rotor(d, cx, cy, r, 45, a=b)   # xoay 45 do: cap 1 = nua phai (N tren + S duoi), cap 2 = nua trai (N duoi + S tren)
    g = appear(t, M[2] - 0.2)
    if g > 0:   # ghep hai mui N-S ke nhau thanh mot cap: vien nua dia + cung ngoai + nhan
        for k, col in ((0, PURPLE), (1, TEAL)):
            a0 = -90 + k * 180
            d.pieslice([cx - r, cy - r, cx + r, cy + r], a0, a0 + 180, outline=A(col, g), width=9)
            d.arc([cx - r - 26, cy - r - 26, cx + r + 26, cy + r + 26], a0 + 5, a0 + 175, fill=A(col, g), width=10)
            m = math.radians(a0 + 90)
            text(d, (cx + (r + 100) * math.cos(m), cy), f"cặp {k + 1}", 40, col, alpha=g)
    c1 = appear(t, M[1] + 0.4)
    text(d, (W / 2, 1110), "4 cực → lấy p = 4", 42, RED, alpha=c1)
    text(d, (W / 2, 1180), "f = 25 × 4 = 100 Hz  ✗", 46, RED, alpha=c1)
    c2 = appear(t, M[2] + 0.4)
    card(d, (110, 1250, 970, 1550), fill=A((220, 252, 231), c2), r=24)
    ctext(d, 1320, "p = 2", 52, GREEN, alpha=c2)
    ctext(d, 1400, "f = 25 × 2 = 50 Hz  ✓", 50, GREEN, alpha=c2)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    chot_hoi(d, t, sc, "f = n·p (n vòng/s, p cặp cực)",
             "p = 2, quay 900 vòng/phút. Tần số bằng bao nhiêu?",
             "đổi ra vòng/s")

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + row_at(i, do), "tap") for i in range(5)]
    out += [(an["t0"] + 0.2, "ding"), (an["t0"] + an["M"][2], "tap"),
            (tr["t0"] + tr["M"][1] + 0.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-mayphatdien-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Máy phát điện xoay chiều · thachlab.id.vn", scenes=[
 dict(key="hook", title="Máy phát mini và tần số", draw=s_hook, tail=0.6, caps=[
   ("Quay rô-to, đọc tần số.", 2.4),
   ("Chọn đáp án.", 5.6)]),
 dict(key="do", title="Quay nhanh dần, đọc tần số", draw=s_do, tail=0.6, caps=[
   ("Đếm vòng trong 10 s.", 2.6),
   ("n = 5 → f = 9,8 Hz.", 2.2),
   ("Tăng n: 10, 15, 20.", 3.2),
   ("n = 25 → f = 50,3 Hz.", 2.4)]),
 dict(key="ans", title="Đồ thị f theo n", draw=s_ans, tail=0.6, caps=[
   ("C: khoảng 50 Hz.", 2.6),
   ("Điểm nằm trên đường thẳng.", 2.4),
   ("f/n gần bằng p = 2.", 2.8)]),
 dict(key="why", title="Vì sao f = n·p?", draw=s_why, tail=0.6, caps=[
   ("Mỗi cặp cực qua cuộn: 1 chu kì.", 3.0),
   ("1 vòng = 2 chu kì.", 2.8)]),
 dict(key="trap", title="Giới hạn và cái bẫy", draw=s_trap, tail=0.6, caps=[
   ("Một máy duy nhất.", 2.4),
   ("Bẫy: đếm cực.", 2.6),
   ("4 cực = 2 cặp.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Thử nghĩ: bao nhiêu Hz?", 4.6)]),
])
