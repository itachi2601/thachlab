# Clip: tn-l10-trong-luc-luc-cang-02 - Do trong luong cac qua nang bang luc ke (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-trong-luc-luc-cang-02.json:
#   so_lieu_mau: m (kg) 0,05 / 0,10 / 0,15 / 0,20 ; P doc (N) 0,50 / 0,95 / 1,45 / 1,95 ; P/m 10,0 / 9,5 / 9,67 / 9,75
#   tham_so: luc ke 0-2,5 N, vach 0,05 N (sai_so_do), g = 9,8 m/s2, m toi da 0,25 kg.
#   ket_qua_ky_vong: mot vach = 10 % so doc o hang dau, 2,6 % o hang cuoi.
# Canh: Du doan (chi cau hoi + hinh, K10) -> Tien hanh (treo them tung qua, kim dao dong roi dung, ghi bang)
#       -> Dap an C + do thi P-m + cot P/m -> Sai so tuong doi -> Bay (ghi P bang kg) + chua noi duoc
#       -> Chot + cau hoi tu nho lai (0,25 kg: gia tri chua hien tren man).
from engine import *

ROWS = [(0.05, 0.50, "10,0"), (0.10, 0.95, "9,5"), (0.15, 1.45, "9,67"), (0.20, 1.95, "9,75")]   # so_lieu_mau
PM = [10.0, 9.5, 9.67, 9.75]
G = 9.8
def fm(x, n=2): return f"{x:.{n}f}".replace(".", ",")

BRASS = (196, 150, 70); BRASS_D = (140, 100, 40)

def ptext(d, cx, y, s, size, color=INK, maxw=440, alpha=1.0, bold=True, lh=1.22):
    f = F(size, bold); ls = wrap(d, s, f, maxw)
    for j, l in enumerate(ls): dtext(d, (cx, y + j * size * lh), l, f, color, alpha)
    return y + len(ls) * size * lh

# ---------------- gia treo + luc ke + qua nang ----------------
LX = 330                       # truc luc ke
Y0, PXN = 380, 160             # y vach 0 N; px moi N  (2,5 N -> y 780)
BODY = (282, 322, 378, 820)
ROD0 = 842                     # day than luc ke (moc treo khi P = 0)
UNIT = 78                      # chieu cao mot qua (moc + than)

def stand(d):
    d.rounded_rectangle([96, 262, 124, 1550], radius=8, fill=(170, 175, 190))
    d.rounded_rectangle([96, 256, 470, 282], radius=8, fill=(150, 155, 172))
    d.rounded_rectangle([50, 1550, 470, 1598], radius=10, fill=(176, 124, 74))
    text(d, (260, 1574), "giá treo", 38, WHITE)

def mass(d, cx, ytop, alpha=1.0, lbl=True):
    """Mot qua nang co moc: vong moc tren, than tru dong thau, moc duoi."""
    d.arc([cx - 12, ytop, cx + 12, ytop + 22], 180, 360, fill=A(NAVY, alpha), width=4)
    d.line([(cx, ytop + 10), (cx, ytop + 18)], fill=A(NAVY, alpha), width=4)
    d.rounded_rectangle([cx - 64, ytop + 18, cx + 64, ytop + 70], radius=12, fill=A(BRASS, alpha), outline=A(BRASS_D, alpha), width=3)
    if lbl: text(d, (cx, ytop + 44), "50 g", 38, WHITE, alpha=alpha)
    d.line([(cx, ytop + 70), (cx, ytop + UNIT)], fill=A(NAVY, alpha), width=4)

def scale(d, Pshow, n, extra=None, ex_a=0.0, q_mark=False):
    """Luc ke lo xo 0-2,5 N, vach 0,05 N. Pshow: vi tri kim (N). n: so qua dang treo.
       extra: (x, y) cua qua dang dua vao (chua moc)."""
    stand(d)
    d.line([(LX, 282), (LX, BODY[1])], fill=NAVY, width=5)
    x0, y0, x1, y1 = BODY
    d.rounded_rectangle(BODY, radius=18, fill=WHITE, outline=NAVY, width=5)
    d.rectangle([LX - 14, y0 + 30, LX + 14, y1 - 22], fill=(236, 240, 248))
    yk = Y0 + Pshow * PXN
    # lo xo trong khe
    N = 14; pts = []
    for i in range(N + 1):
        yy = lerp(y0 + 28, yk, i / N); pts.append((LX + (10 if i % 2 else -10), yy))
    d.line(pts, fill=GRAY, width=3)
    # vach chia 0,05 N
    for k in range(0, 51):
        y = Y0 + k * 0.05 * PXN; L = 22 if k % 10 == 0 else (15 if k % 5 == 0 else 8)
        d.line([(x0, y), (x0 + L, y)], fill=NAVY, width=3 if k % 10 == 0 else 2)
    for v, s in ((0, "0"), (0.5, "0,5"), (1, "1"), (1.5, "1,5"), (2, "2"), (2.5, "2,5")):
        text(d, (x0 - 14, Y0 + v * PXN), s, 40, INK, anchor="rm")
    text(d, (x0 - 14, y1 + 2), "N", 40, INK, anchor="rm")
    # kim
    d.line([(x0 + 4, yk), (x1 - 4, yk)], fill=RED, width=6)
    d.polygon([(x0 + 2, yk), (x0 + 22, yk - 10), (x0 + 22, yk + 10)], fill=RED)
    # can + moc
    yb = ROD0 + Pshow * PXN
    d.line([(LX, yk), (LX, yb)], fill=NAVY, width=7)
    d.arc([LX - 14, yb - 4, LX + 14, yb + 24], 0, 180, fill=NAVY, width=5)
    for i in range(n): mass(d, LX, yb + 12 + i * UNIT)
    if extra is not None and ex_a > 0: mass(d, extra[0], extra[1], alpha=ex_a)
    return yb

def readout(d, n, Ptxt, a=1.0):
    card(d, (560, 300, 1030, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (795, 360), f"{n} quả · m = {fm(0.05 * n)} kg", 42, BLUE, alpha=a)
    text(d, (795, 470), Ptxt, 72, RED, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    Ps = ROWS[0][1] * ease((t - 0.6) / 0.9)
    scale(d, Ps, 1)
    readout(d, 1, f"{fm(ROWS[0][1])} N" if t > 1.6 else "…")
    M = sc["M"]; k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 600 + (1 - k) * 30
    card(d, (560, y0, 1030, y0 + 860), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (795 - pw / 2, y0 + 28, 795 + pw / 2, y0 + 92), fill=A(PURPLE, k), r=32)
    text(d, (795, y0 + 60), "Dự đoán", 40, WHITE, alpha=k)
    ptext(d, 795, y0 + 150, "Treo 4 quả như thế.", 42, INK, maxw=420, alpha=k)
    ptext(d, 795, y0 + 210, "Lực kế chỉ bao nhiêu?", 42, INK, maxw=420, alpha=k)
    # hinh: 4 qua noi nhau duoi moc, so chi chua biet
    cx = 700; yt = y0 + 300
    d.line([(cx, yt - 30), (cx, yt + 4)], fill=A(NAVY, k), width=5)
    for i in range(4): mass(d, cx, yt + i * UNIT, alpha=k)
    text(d, (cx + 100, yt + 40), "4 ×", 40, INK, anchor="lm", alpha=k)
    card(d, (820, yt + 120, 1000, yt + 220), fill=A((245, 243, 255), k), outline=A(PURPLE, k), r=22, w=4)
    text(d, (910, yt + 170), "? N", 52, PURPLE, alpha=k)
    # thanh dem thoi gian nghi
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([600, y0 + 820, 990, y0 + 834], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([600, y0 + 820, 600 + 390 * (1 - q), y0 + 834], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
ADD = [0.6, 2.6, 4.6]            # moc giay (tinh tu M[0]) treo them qua thu 2, 3, 4
HANG = 0.7                       # thoi gian dua qua vao moc

def p_at(t, sc):
    """Vi tri kim: dao dong tat dan quanh so doc moi roi dung yen (doi dung yen roi doc)."""
    P, n, extra, ex_a, settled = ROWS[0][1], 1, None, 0.0, True
    for i, a in enumerate(ADD):
        s = sc["M"][0] + a
        if t < s: break
        tau = t - s
        if tau < HANG:                       # qua moi dang dua vao
            k = ease(tau / HANG)
            yb = ROD0 + ROWS[i][1] * PXN
            extra = (lerp(470, LX, k), yb + 12 + (i + 1) * UNIT - (1 - k) * 60); ex_a = clamp(k * 3)
            P, n, settled = ROWS[i][1], i + 1, False
        else:
            tt = tau - HANG; p0, p1 = ROWS[i][1], ROWS[i + 1][1]
            P = p1 + (p0 - p1) * math.exp(-3.2 * tt) * math.cos(2 * math.pi * 1.6 * tt)
            n, extra, ex_a, settled = i + 2, None, 0.0, tt > 1.2
    return P, n, extra, ex_a, settled

def row_at(i, sc): return 0.2 if i == 0 else sc["M"][0] + ADD[i - 1] + HANG + 1.2

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    P, n, extra, ex_a, settled = p_at(t, sc)
    scale(d, P, n, extra, ex_a)
    readout(d, n, f"{fm(ROWS[n - 1][1])} N" if settled else "đợi…", 1.0)
    card(d, (560, 600, 1030, 1060), fill=WHITE, outline=NAVY, w=4)
    xs = (690, 900)
    text(d, (xs[0], 650), "m (kg)", 42, INK); text(d, (xs[1], 650), "P (N)", 42, INK)
    d.line([(585, 685), (1005, 685)], fill=LIGHT, width=4)
    last = max([i for i in range(4) if t >= row_at(i, sc)], default=-1)
    for i, (m, p, _) in enumerate(ROWS):
        a = appear(t, row_at(i, sc), 0.35); y = 735 + i * 82
        if a <= 0: continue
        if i == last: d.rounded_rectangle([580, y - 34, 1010, y + 34], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), fm(m), 44, BLUE, alpha=a); text(d, (xs[1], y), fm(p), 44, RED, alpha=a)
    kc = appear(t, sc["M"][1], 0.4)
    if kc > 0:
        card(d, (560, 1100, 1030, 1220), fill=A((220, 252, 231), kc), outline=A(GREEN, kc), r=26, w=4)
        text(d, (795, 1160), "Đáp án C", 48, GREEN, alpha=kc)

# ---------------- canh 3: do thi P-m + cot P/m ----------------
def s_graph(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    x0, x1, yb, yt = 210, 960, 900, 340
    X = lambda m: x0 + m / 0.25 * (x1 - x0); Y = lambda p: yb - p / 2.5 * (yb - yt)
    card(d, (40, 260, 1040, 1010), fill=WHITE, outline=LIGHT, w=3)
    for p_ in (0.5, 1, 1.5, 2, 2.5): d.line([(x0, Y(p_)), (x1, Y(p_))], fill=(240, 236, 228), width=2)
    d.line([(x0, yb), (x1 + 20, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 30)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 26), "P (N)", 40, INK, anchor="lm"); text(d, (x1 + 20, yb - 38), "m (kg)", 40, INK, anchor="rm")
    for m in (0.05, 0.10, 0.15, 0.20, 0.25):
        d.line([(X(m), yb), (X(m), yb + 10)], fill=NAVY, width=3); text(d, (X(m), yb + 42), fm(m), 40, INK)
    for p_, s in ((0, "0"), (0.5, "0,5"), (1, "1"), (1.5, "1,5"), (2, "2"), (2.5, "2,5")):
        d.line([(x0 - 10, Y(p_)), (x0, Y(p_))], fill=NAVY, width=4); text(d, (x0 - 18, Y(p_)), s, 40, INK, anchor="rm")
    for i, (m, p, _) in enumerate(ROWS):
        a = appear(t, 0.2 + i * 0.25, 0.4)
        if a > 0: dot(d, X(m), Y(p), 16 * back(a), ORANGE, WHITE)
    k = ease((t - M[0] - 1.4) / 1.0)          # duong thang qua goc toa do
    if k > 0:
        me = 0.25 * k
        d.line([(X(0), Y(0)), (X(me), Y(G * me))], fill=A(BLUE, 0.6), width=6)
    # cot P/m
    a1 = appear(t, M[1] - 0.2)
    if a1 <= 0: return
    card(d, (40, 1040, 1040, 1600), fill=A(WHITE, a1), outline=A(LIGHT, a1), w=3)
    text(d, (W / 2, 1090), "P/m (N/kg)", 40, MUTED, alpha=a1)
    base, sp = 1480, 30.0                    # px moi N/kg (dinh cot 10,0 o y 1180, cach tieu de ~70 px)
    band = appear(t, M[1] + 1.8, 0.4)
    d.line([(80, base), (1000, base)], fill=NAVY, width=4)
    for i, ((m, p, s), v) in enumerate(zip(ROWS, PM)):
        cx = 160 + i * 190; g = ease((t - M[1] - 0.1 - i * 0.25) / 0.5)
        text(d, (cx, 1522), f"{fm(m)} kg", 38, INK, alpha=a1)
        if g <= 0: continue
        top = base - v * sp * g
        d.rectangle([cx - 60, top, cx + 60, base], fill=ORANGE)
        text(d, (cx, base - 40), s, 40, WHITE, alpha=clamp(g * 2 - 1))
    if band > 0:                              # vach g: net dut de thay dinh cot, nhan ben phai
        yg = base - G * sp
        for xx in range(80, 820, 34): d.line([(xx, yg), (xx + 20, yg)], fill=A(GREEN, band), width=5)
        text(d, (840, yg), "g = 9,8", 42, GREEN, anchor="lm", alpha=band)

# ---------------- canh 4: sai so tuong doi ----------------
def s_saiso(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 270, 1020, 470), fill=A(WHITE, a), outline=A(NAVY, a), w=5)
    text(d, (W / 2, 370), "Một vạch = 0,05 N", 52, NAVY, alpha=a)
    PX = 400                                  # px moi N
    for j, (i, pct, y) in enumerate(((0, "10%", 660), (3, "2,6%", 950))):
        b = appear(t, 0.5 + j * 0.6, 0.45)
        if b <= 0: continue
        p = ROWS[i][1]; x0 = 120
        text(d, (x0, y - 80), f"{fm(ROWS[i][0])} kg: P = {fm(p)} N", 44, INK, anchor="lm", alpha=b)
        d.rounded_rectangle([x0, y - 26, x0 + p * PX, y + 26], radius=10, fill=A(ORANGE, b))
        e0, e1 = x0 + (p - 0.05) * PX, x0 + (p + 0.05) * PX
        d.rectangle([e0, y - 40, e1, y + 40], outline=A(RED, b), width=5)
        text(d, (x0, y + 80), f"± 1 vạch ≈ {pct} số đọc", 44, RED, anchor="lm", alpha=b * appear(t, M[0] + 1.6 + j * 0.6))
    c = appear(t, M[1] + 0.1, 0.45)
    if c > 0:
        card(d, (60, 1110, 1020, 1430), fill=A((220, 252, 231), c), outline=A(GREEN, c), w=5)
        ctext(d, 1215, "Với 0,05 kg: P/m = 10,0,", 44, INK, maxw=880, alpha=c)
        ctext(d, 1310, "lệch do sai số", 44, GREEN, maxw=880, alpha=c)

# ---------------- canh 5: bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45)
    a = appear(t, 0.1, 0.4) * (1 - k3)
    y0 = 270
    card(d, (60, y0, 1020, y0 + 520), fill=A(WHITE, a), outline=A(RED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(RED, a), r=32)
    text(d, (W / 2, y0 + 60), "Bẫy", 40, WHITE, alpha=a)
    q = f"P = {fm(ROWS[3][0])} kg"; f = F(56); lw = tw(d, q, f); yy = y0 + 200
    ks = clamp((t - 1.0) / 0.4)
    text(d, (W / 2, yy), q, 56, mix(INK, MUTED, ks), alpha=a)
    if ks > 0: d.line([(W / 2 - lw / 2 - 8, yy + 2), (W / 2 - lw / 2 - 8 + (lw + 16) * ks, yy + 2)], fill=A(RED, 0.85 * a), width=6)
    k2 = appear(t, 1.6, 0.45)
    text(d, (W / 2, y0 + 310), f"P = {fm(ROWS[3][1])} N", 56, GREEN, alpha=a * k2)
    text(d, (W / 2, y0 + 420), "kg đo khối lượng, N đo lực", 44, INK, alpha=a * k2)
    if k3 > 0:
        y1 = 500 + (1 - k3) * 30
        card(d, (60, y1, 1020, y1 + 440), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 70), "Chưa nói được gì?", 46, NAVY, alpha=k3)
        card(d, (110, y1 + 140, 970, y1 + 400), fill=A((239, 246, 255), k3), r=24)
        ctext(d, y1 + 220, "Chỉ đo ở một nơi:", 44, INK, alpha=k3)
        ctext(d, y1 + 310, "chưa thấy P đổi khi g đổi", 44, BLUE, alpha=k3)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def hint(d, t, k):                        # tu ve goi y de chu >= 40 px (engine ve "Gợi ý" 36 px)
        kh = appear(t, sc["M"][0] + 1.2, 0.5)
        if kh <= 0: return
        card(d, (110, 1290, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1350, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1445, "g ≈ 9,8 m/s²", 44, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "P tỉ lệ với m: P = m·g",
             "Treo vật 0,25 kg: lực kế chỉ khoảng bao nhiêu? Có sát giới hạn thang không?", body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, g, b, e = sc["hook"], sc["do"], sc["graph"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + do["M"][1], "ding"), (g["t0"] + g["M"][1] + 1.8, "tap"),
            (b["t0"] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-trong-luc-luc-cang-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Trọng lực và lực căng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Treo quả nặng vào lực kế", draw=s_hook, tail=0.6, caps=[
   ("Kim ở 0, treo một quả.", 3.0),
   ("Dừng video, tự đoán.", 5.2)]),
 dict(key="do", title="Thêm từng quả, đọc số chỉ", draw=s_do, tail=0.5, caps=[
   ("Đợi kim đứng yên rồi mới đọc.", 6.8),
   ("Bốn quả: gần gấp bốn.", 3.0)]),
 dict(key="graph", title="Đồ thị P theo m", draw=s_graph, tail=0.5, caps=[
   ("Các điểm gần một đường thẳng.", 3.4),
   ("Chia P cho m: gần như không đổi.", 3.4)]),
 dict(key="saiso", title="Hàng nào tin cậy hơn?", draw=s_saiso, tail=0.5, caps=[
   ("Cùng sai một vạch.", 2.6),
   ("Vật nặng hơn, tin cậy hơn.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy hay gặp.", 3.2),
   ("Giới hạn của thí nghiệm.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 4.8)]),
])
