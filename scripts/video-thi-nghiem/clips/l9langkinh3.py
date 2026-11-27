# Clip: tn-l9-langkinh-03 - Do goc lech cua ba tia laser do, luc, tim qua cung lang kinh (KHTN 9, lo 5, 18/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom D): chu than canh >= 55 (ra >= 48 px), K10, moi nhip >= 2,5 s,
#   Bay = hai hang hinh (do lech hon ✗ / tim lech hon ✓), bo goi y o man chot (cau chot A-D o khung web).
# So lieu tu content/thi-nghiem/tn-l9-langkinh-03.json (_kiem()):
#   tham_so: A = 60 do, i = 50 do, n do/luc/tim = 1,612 / 1,627 / 1,652 (gia dinh, thuy tinh pha chi)
#   so_lieu_mau: D trung binh do 47,7 ; luc 49,3 ; tim 52,3 (ba lan do 47;48;48 | 49;50;49 | 52;53;52)
#   Duong tia ve bang Snell dung tung n -> D mo hinh 47,7 / 49,3 / 52,2 do (khop cot "D mo hinh", assert < 0,06).
# Du doan (doi 27/11): bai da noi "do lech it, tim lech nhieu" TRUOC hop -> hoi muc do: ba goc lech chenh nhau co nao?
#   -> dap an: chi vai do (47,7 -> 52,3). Clip KHONG neu hieu 4,6 (bang "Bam xem"), KHONG so chenh lech voi sai so
#   (Cau 2 ngay sau hop), khong thu tu do/vang/lam (Cau 5).
# Bay = hien_tuong_hay_sai[0] (nghi do lech nhieu nhat). Chua noi duoc = ghi_chu kho (so lieu minh hoa, n gia dinh).
# THU NGHI (ca chot cua kho): laser cam, van i = 50 do -> D nam giua do (47,7) va luc (49,3). Khong hien goi y.
from engine import *

AXD, IDEG = 60.0, 50.0
NS = [1.612, 1.627, 1.652]
NAMES = ["đỏ", "lục", "tím"]
COLS = [(220, 38, 38), (22, 150, 70), (124, 58, 237)]
MEANS = ["47,7", "49,3", "52,3"]
GLASS = (191, 219, 254); DRED = (185, 28, 28); DGREEN = (10, 110, 50); DORG = (176, 64, 8); CAM = (234, 88, 12)
FS, FM = 58, 56

P = (400.0, 330.0); SIDE = 460.0
BL = (P[0] - SIDE / 2, P[1] + SIDE * math.sqrt(3) / 2); BR = (P[0] + SIDE / 2, BL[1])
E = (lerp(BL[0], P[0], 0.6), lerp(BL[1], P[1], 0.6))          # diem toi tren mat ben trai
TH_IN = -20.0                                                  # huong tia toi (do, y huong xuong la duong)
DIN = (math.cos(math.radians(TH_IN)), math.sin(math.radians(TH_IN)))
S = (E[0] - 200 * DIN[0], E[1] - 200 * DIN[1])                 # dau but laser
LOUT = 420


def path(n):
    """-> (diem ra X, goc tia lo (do), D (do)) theo Snell"""
    r1 = math.degrees(math.asin(math.sin(math.radians(IDEG)) / n))
    th = 30.0 - r1                                             # phap tuyen trong mat trai = +30 do
    v = (math.cos(math.radians(th)), math.sin(math.radians(th)))
    wx, wy = BR[0] - P[0], BR[1] - P[1]
    det = v[0] * (-wy) - v[1] * (-wx)
    s = ((P[0] - E[0]) * (-wy) - (P[1] - E[1]) * (-wx)) / det
    X = (E[0] + s * v[0], E[1] + s * v[1])
    i2 = math.degrees(math.asin(n * math.sin(math.radians(AXD - r1))))
    the = -30.0 + i2                                           # phap tuyen ngoai mat phai = -30 do
    return X, the, the - TH_IN


PATHS = [path(n) for n in NS]


def zend(c, L=LOUT):
    X, th, _ = PATHS[c]
    return (X[0] + L * math.cos(math.radians(th)), X[1] + L * math.sin(math.radians(th)))


def _kiem():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-langkinh-03.json")))
    tp = {x["ky_hieu"]: x["gia_tri"] for x in k["tham_so"] if "gia_tri" in x}
    assert tp["A"] == AXD and [tp["n_do"], tp["n_luc"], tp["n_tim"]] == NS
    assert next(x for x in k["tham_so"] if x["ky_hieu"] == "i")["mac_dinh"] == IDEG
    for c, h in enumerate(k["so_lieu_mau"]["hang"]):
        assert h[0] == NAMES[c] and h[1] == NS[c]
        assert f"{h[6]:.1f}".replace(".", ",") == MEANS[c], (h, MEANS[c])
        assert abs(PATHS[c][2] - h[2]) < 0.06, (c, PATHS[c][2], h[2])
    assert PATHS[0][2] < PATHS[1][2] < PATHS[2][2]
    for c in range(3): assert zend(c)[0] < 900, zend(c)
_kiem()


def dash(d, p1, p2, col, w=3, on=14, off=10):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (on + off)) + 1
    for i in range(n):
        a, b = i * (on + off) / L, min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=col, width=w)


def chev(d, p, q, col, s=18, w=5):
    x, y = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2; ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=col, width=w)


def mk_tf(cx=None, top=None, k=1.0):
    if cx is None: return lambda p: p
    return lambda p: (cx + k * (p[0] - P[0]), top + k * (p[1] - P[1]))


def prism(d, tf=None, labs=True, ka=1.0):
    tf = tf or mk_tf()
    d.polygon([tf(P), tf(BR), tf(BL)], fill=A(GLASS, 0.85 * ka), outline=A(BLUE, ka))
    d.line([tf(P), tf(BR), tf(BL), tf(P)], fill=A(BLUE, ka), width=4)
    if labs: text(d, (P[0] + 190, P[1] + 10), "A = 60°", FM, BLUE, alpha=ka)


def pen(d, tf=None, k=1.0, col=None):
    tf = tf or mk_tf()
    a = (S[0] - 110 * DIN[0], S[1] - 110 * DIN[1])
    d.line([tf(a), tf(S)], fill=(55, 60, 75), width=int(30 * k))
    if col: q = tf(S); dot(d, q[0], q[1], 9 * k, col)


def normal_E(d, lab=True):
    nrm = (-math.sqrt(3) / 2, -0.5)                             # phap tuyen ngoai mat trai
    dash(d, (E[0] + 120 * nrm[0], E[1] + 120 * nrm[1]), (E[0] - 90 * nrm[0], E[1] - 90 * nrm[1]), A(NAVY, 0.7), w=3)
    if lab:
        d.arc([E[0] - 85, E[1] - 85, E[0] + 85, E[1] + 85], 160, 210, fill=NAVY, width=5)
        text(d, (E[0] - 150, E[1] - 30), "50°", FM, NAVY)


def incident(d, col, ka=1.0, tf=None, w=6):
    tf = tf or mk_tf()
    d.line([tf(S), tf(E)], fill=A(col, ka), width=w); chev(d, tf(S), tf(E), A(col, ka))


def beam(d, c, u=1.0, ka=1.0, tf=None, colc=None, w=6):
    """tia mau c: toi -> trong -> lo ; u (0..1) tien do. colc: mau ve (canh Bay ve sai)."""
    tf = tf or mk_tf(); col = colc or COLS[c]
    X, th, _ = PATHS[c]; Z = zend(c)
    for p, q, a, b in ((S, E, 0.0, 0.3), (E, X, 0.3, 0.5), (X, Z, 0.5, 1.0)):
        k = clamp((u - a) / (b - a))
        if k <= 0: break
        q2 = (lerp(p[0], q[0], k), lerp(p[1], q[1], k))
        d.line([tf(p), tf(q2)], fill=A(col, ka), width=w if p != E else w - 2)
        if k > 0.6 and p != E: chev(d, tf(p), tf(q), A(col, ka))


def d_arc(d, c, r, ka=1.0, lab=True, sweep=1.0):
    X, th, _ = PATHS[c]
    dash(d, X, (X[0] + LOUT * DIN[0], X[1] + LOUT * DIN[1]), A(NAVY, 0.75 * ka), w=3)
    d.arc([X[0] - r, X[1] - r, X[0] + r, X[1] + r], TH_IN, lerp(TH_IN, th, sweep), fill=A(COLS[c], ka), width=6)
    if lab:
        m = math.radians((TH_IN + th) / 2)
        text(d, (X[0] + (r + 40) * math.cos(m), X[1] + (r + 40) * math.sin(m)), "D", FS, COLS[c], alpha=ka)


LAB_X = 960
def end_name(d, c, ka=1.0):
    Z = zend(c); ty = zend(1)[1] + (c - 1) * 84                # cot nhan cach nhau 84 px (kiem-v1 muc 3), noi bang vach manh
    d.line([Z, (LAB_X - 50, ty)], fill=A(COLS[c], 0.8 * ka), width=2)
    text(d, (LAB_X, ty), NAMES[c], FM, COLS[c], alpha=ka)


TY0, RH = 1010, 92
def table(d, n):
    card(d, (60, TY0, 1020, TY0 + 100 + 3 * RH + 20), fill=WHITE, outline=LIGHT, w=3)
    text(d, (270, TY0 + 52), "Màu", FM, NAVY); text(d, (720, TY0 + 52), "D trung bình", FM, NAVY)
    d.line([(90, TY0 + 100), (990, TY0 + 100)], fill=LIGHT, width=3)
    for j in range(n):
        yy = TY0 + 150 + RH * j
        text(d, (270, yy), NAMES[j], FS, COLS[j]); text(d, (720, yy), MEANS[j] + "°", FS, INK)


def pill(d, s, y, a, color=NAVY, size=FM):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh; vien NAVY, chu INK) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    prism(d); normal_E(d)
    pen(d); incident(d, GRAY, appear(t, 0.5, 0.5))
    kd = appear(t, 1.2, 0.5)                                   # kiem-v1 muc 2: chi ro "goc lech D" tren hinh (mot tia lo xam,
    if kd > 0:                                                 #   khong mau -> khong lo do chenh giua cac mau)
        X, th, _ = PATHS[1]; Z = zend(1)
        d.line([E, X], fill=A(GRAY, 0.6 * kd), width=4); d.line([X, Z], fill=A(GRAY, 0.8 * kd), width=5)
        dash(d, X, (X[0] + LOUT * DIN[0], X[1] + LOUT * DIN[1]), A(NAVY, 0.6 * kd), w=3)
        d.arc([X[0] - 150, X[1] - 150, X[0] + 150, X[1] + 150], TH_IN, th, fill=A(NAVY, kd), width=6)
        m = math.radians((TH_IN + th) / 2)
        text(d, (X[0] + 190 * math.cos(m), X[1] + 190 * math.sin(m)), "D", FS, NAVY, alpha=kd)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(NAVY, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FM)) + 56
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 96), fill=A(NAVY, a), r=36)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", FM, WHITE, alpha=a)
    for j, s in enumerate(("Đỏ, lục, tím cùng góc tới 50°.", "Ba góc lệch D chênh nhau", "cỡ bao nhiêu độ?")):
        text(d, (W / 2, y0 + 165 + j * 80), s, 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1          # thanh dem nguoc lien, day 70 px
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 440, 970, y0 + 510], radius=35, fill=A((226, 232, 240), a))
        if p < 1: d.rounded_rectangle([110, y0 + 440, 110 + max(70, 860 * (1 - p)), y0 + 510], radius=35, fill=A(NAVY, a))


# ---------------- canh 2: Tien hanh ----------------
T0, DT = 0.6, 3.2          # mau c: bat T0 + DT.c ; tia di 1,0 s ; cung D sau 1,2 s ; hang bang sau 2,0 s ; tat sau 3,1 s
B_RUN, B_ARC, B_ROW, B_OFF = 1.0, 1.2, 2.0, 3.1


def state_do(t):
    cur, u, arc, n, traced = -1, 0.0, -1.0, 0, []
    for c in range(3):
        tc = T0 + DT * c
        if t >= tc + B_ROW: n = c + 1
        if t >= tc + B_OFF: traced.append(c)
        elif t >= tc:
            cur, u, arc = c, clamp((t - tc) / B_RUN), t - tc - B_ARC
    return cur, u, arc, n, traced


def s_do(img, d, t, sc):
    cur, u, arc, n, traced = state_do(t)
    prism(d); normal_E(d, lab=False)
    for c in traced:
        X = PATHS[c][0]; Z = zend(c)
        d.line([X, Z], fill=A(COLS[c], 0.6), width=4); end_name(d, c, 0.85)
    pen(d, col=COLS[cur] if cur >= 0 else None)
    if cur >= 0:
        beam(d, cur, u)
        if u >= 1: end_name(d, cur)
        if arc >= 0: d_arc(d, cur, 150, lab=True, sweep=clamp(arc / 0.5))
    table(d, n)


# ---------------- canh 3: Dap an + Rut ra ----------------
DA_V, DA_R = 2.4, 5.0
def s_dapan(img, d, t, sc):
    pill(d, "ĐÁP ÁN: chênh vài độ", 240 + 0, appear(t, 0.15, 0.4))
    prism(d, labs=False); pen(d); normal_E(d, lab=False)
    incident(d, GRAY, 0.9)
    for c in range(3):
        k = appear(t, 0.4 + 0.45 * c, 0.5)
        if k <= 0: continue
        X = PATHS[c][0]
        d.line([E, X], fill=A(COLS[c], 0.7 * k), width=4)
        L = LOUT * k; Z = zend(c, L)
        d.line([X, Z], fill=A(COLS[c], k), width=6)
        rr = 26 + (14 * math.sin(3.0 * (t - DA_R)) ** 2 if (c == 2 and t > DA_R) else 0)
        dot(d, Z[0], Z[1], rr * k, COLS[c])
    kv = appear(t, DA_V, 0.5)
    if kv > 0:
        card(d, (60, 1010, 1020, 1130), fill=A(WHITE, kv), outline=A(NAVY, kv), r=26, w=4)
        for c, x in zip(range(3), (230, 540, 850)):
            text(d, (x, 1070), MEANS[c] + "°", FS, COLS[c], alpha=kv)
    kr = appear(t, DA_R, 0.5)
    if kr > 0:
        card(d, (60, 1170, 1020, 1420), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=26, w=4)
        text(d, (W / 2, 1240), "Chiết suất lớn → lệch nhiều", FS, DGREEN, alpha=kr)
        text(d, (W / 2, 1340), "Đỏ ít nhất, tím nhiều nhất", FS, DGREEN, alpha=kr)


# ---------------- canh 4: Bay + chua noi duoc ----------------
BAY_R, BAY_E = 3.4, 6.6
def bay_row(d, y_top, ka, grow, wrong):
    tf = mk_tf(300, y_top + 30, 0.62)
    prism(d, tf, labs=False, ka=ka); pen(d, tf, 0.7)
    X1 = PATHS[1][0]                                          # kiem-v1 muc 1: keo dai tia toi lam moc "lech hon"
    dash(d, tf(X1), tf((X1[0] + LOUT * DIN[0], X1[1] + LOUT * DIN[1])), A(NAVY, 0.7 * ka), w=3)
    for c in (0, 2):                                          # chi ve do va tim
        geo = (2 - c) if wrong else c                         # ve sai: do di duong cua tim
        beam(d, geo, grow, ka, tf=tf, colc=COLS[c], w=6)
        if grow >= 1:                                         # ten mau o dau tia: tia tren ghi tren, tia duoi ghi duoi
            Z = tf(zend(geo)); low = (geo == 2)
            text(d, (Z[0] + 10, Z[1] + (40 if low else -40)), NAMES[c], FM, COLS[c], alpha=ka)


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pill(d, "BẪY", 300, a1, color=DRED)
    text(d, (W / 2, 405), "“Đỏ lệch nhiều nhất”", FS, INK, alpha=a1)
    if a1 > 0:
        card(d, (40, 465, 1040, 885), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
        bay_row(d, 465, a1, appear(t, 0.5, 1.4), True)
        text(d, (870, 620), "đỏ lệch hơn", FM, DRED, alpha=a1)
        text(d, (870, 740), "✗", 80, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (40, 905, 1040, 1325), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        bay_row(d, 905, a2, appear(t, BAY_R + 0.2, 1.4), False)
        text(d, (870, 1060), "tím lệch hơn", FM, DGREEN, alpha=a2)
        text(d, (870, 1180), "✓", 80, DGREEN, alpha=a2)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (40, 1350, 1040, 1565), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1405), "Chưa nói được:", FS, NAVY, alpha=k3)
        text(d, (W / 2, 1495), "số liệu minh hoạ, n giả định", FM, INK, alpha=k3)


# ---------------- canh 5: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 4.3
def s_end(img, d, t, sc):
    # GD2 kiem-v1 muc 4: bo the xanh nhac lai dieu da biet
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FM)) + 56
    card(d, (W / 2 - pw / 2, 480, W / 2 + pw / 2, 556), fill=A(ORANGE, k1), r=38)
    text(d, (W / 2, 518), "THỬ NGHĨ", FM, WHITE, alpha=k1)
    text(d, (W / 2, 630), "Laser màu cam, góc tới 50°:", FS, INK, alpha=k1)
    text(d, (W / 2, 712), "góc lệch D vào khoảng nào?", FS, INK, alpha=k1)
    if k1 > 0:   # hinh: chi tia toi mau cam; KHONG ve tia lo
        tf = mk_tf(470, 830, 0.85)
        prism(d, tf, labs=False, ka=k1); pen(d, tf, 0.85, CAM)
        incident(d, CAM, k1, tf=tf, w=7)
        kq = 0.55 + 0.45 * math.sin(2.4 * t) ** 2
        q = tf(PATHS[1][0])
        d.rounded_rectangle([q[0] + 60, q[1] + 60, q[0] + 400, q[1] + 180], radius=24, fill=A((253, 186, 116), k1 * (kq - 0.55) / 0.45))  # nhap nhay
        text(d, (q[0] + 230, q[1] + 120), "D = ?", 80, ORANGE, alpha=k1 * kq)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + T0 + DT * c, "tap") for c in range(3)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + END_Q + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-langkinh-03", header="KHTN 9 · THÍ NGHIỆM", footer="Lăng kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ba tia laser, một lăng kính", draw=s_hook, tail=0.3, caps=[
   ("Ba laser chiếu vào cùng một điểm.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Chiếu lần lượt từng màu.", 4.4),
   ("Đo D ba lần, lấy trung bình.", 5.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Ba tia ló tách nhau rất ít.", 4.4),
   ("Mỗi màu một chiết suất.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("So hai cách vẽ.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 8.2)]),
])
