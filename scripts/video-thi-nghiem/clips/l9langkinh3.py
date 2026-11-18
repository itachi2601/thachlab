# Clip: tn-l9-langkinh-03 - Do goc lech cua ba tia laser do, luc, tim qua cung lang kinh (KHTN 9, lo 5, 18/11/2026)
# So lieu tu content/thi-nghiem/tn-l9-langkinh-03.json:
#   tham_so: A = 60 do, i = 50 do, n do/luc/tim = 1,612 / 1,627 / 1,652 (gia dinh, thuy tinh pha chi)
#   so_lieu_mau: D 3 lan: do 47;48;48 (TB 47,7) ; luc 49;50;49 (TB 49,3) ; tim 52;53;52 (TB 52,3)
#   Duong tia ve bang Snell dung tung n (sin i = n sin r1 ; r2 = A - r1 ; sin i2 = n sin r2 ; D = i + i2 - A):
#   D mo hinh 47,7 / 49,3 / 52,2 do (khop cot "D mo hinh" cua kho).
# Cau 2 ngay sau hop (do - luc chenh 1,7 do so voi sai so 1 do) -> clip KHONG so chenh lech voi sai so, KHONG noi "can
#   do them". Bay dung hien_tuong_hay_sai[0] (nghi do lech nhieu nhat), khong dung [1] (= dap an Cau 2).
# Mau tia la thong tin vat li; hop Du doan vien NAVY (khong tim), chu cau hoi mau INK, khong to mau ten ba laser.
# THU NGHI: laser cam, van i = 50 do -> D nam giua do (47,7) va luc (49,3).
from engine import *

AXD, IDEG = 60.0, 50.0
NS = [1.612, 1.627, 1.652]
NAMES = ["đỏ", "lục", "tím"]
COLS = [(220, 38, 38), (22, 150, 70), (124, 58, 237)]
READS = [("47°", "48°", "48°", "47,7°"), ("49°", "50°", "49°", "49,3°"), ("52°", "53°", "52°", "52,3°")]
DRED = (185, 28, 28); DGREEN = (21, 110, 55); GLASS = (191, 219, 254)

P = (400.0, 432.0); SIDE = 460.0
BL = (P[0] - SIDE / 2, P[1] + SIDE * math.sqrt(3) / 2); BR = (P[0] + SIDE / 2, BL[1])
E = (lerp(BL[0], P[0], 0.6), lerp(BL[1], P[1], 0.6))          # diem toi tren mat ben trai
TH_IN = -20.0                                                  # huong tia toi (do, y huong xuong la duong)
DIN = (math.cos(math.radians(TH_IN)), math.sin(math.radians(TH_IN)))
S = (E[0] - 200 * DIN[0], E[1] - 200 * DIN[1])                 # dau but laser
XEND = 900


def path(n):
    """tra ve (diem ra X, goc tia lo (do), D (do)) theo Snell"""
    r1 = math.degrees(math.asin(math.sin(math.radians(IDEG)) / n))
    th = 30.0 - r1                                             # phap tuyen trong mat trai = +30 do
    u = (math.cos(math.radians(th)), math.sin(math.radians(th)))
    # giao voi mat phai P -> BR
    vx, vy = BR[0] - P[0], BR[1] - P[1]
    det = u[0] * (-vy) - u[1] * (-vx)
    s = ((P[0] - E[0]) * (-vy) - (P[1] - E[1]) * (-vx)) / det
    X = (E[0] + s * u[0], E[1] + s * u[1])
    r2 = AXD - r1
    i2 = math.degrees(math.asin(n * math.sin(math.radians(r2))))
    the = -30.0 + i2                                           # phap tuyen ngoai mat phai = -30 do
    return X, the, IDEG + i2 - AXD


PATHS = [path(n) for n in NS]


def ray_end(X, th):
    k = (XEND - X[0]) / math.cos(math.radians(th))
    return (XEND, X[1] + k * math.sin(math.radians(th)))


def dash(d, p1, p2, col, w=3, on=14, off=10):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (on + off)) + 1
    for i in range(n):
        a, b = i * (on + off) / L, min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=col, width=w)


def chev(d, p, q, col, s=16, w=4):
    x, y = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2; ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=col, width=w)


def prism(d):
    d.polygon([P, BR, BL], fill=A(GLASS, 0.8), outline=BLUE)
    d.line([P, BR, BL, P], fill=BLUE, width=4)
    text(d, (P[0], P[1] - 40), "A = 60°", 42, BLUE)
    text(d, ((BL[0] + BR[0]) / 2, BL[1] + 44), "lăng kính", 40, BLUE)


def pen(d, beam_col=None):
    a = (S[0] - 110 * DIN[0], S[1] - 110 * DIN[1])
    d.line([a, S], fill=(55, 60, 75), width=30)
    if beam_col: dot(d, S[0], S[1], 9, beam_col)


def normal_at_E(d, col=None, lab=True):
    nrm = (-math.sqrt(3) / 2, -0.5)                             # phap tuyen ngoai mat trai
    col = col or A(NAVY, 0.7)
    dash(d, (E[0] + 110 * nrm[0], E[1] + 110 * nrm[1]), (E[0] - 90 * nrm[0], E[1] - 90 * nrm[1]), col, w=3)
    if lab:
        d.arc([E[0] - 80, E[1] - 80, E[0] + 80, E[1] + 80], 160, 210, fill=NAVY, width=4)
        text(d, (E[0] - 140, E[1] - 18), "50°", 42, NAVY)


def beam(d, c, u, kd=1.0):
    """ve tia mau c: toi -> trong -> lo ; u (0..1) tien do tia di"""
    X, th, _ = PATHS[c]; Z = ray_end(X, th); col = COLS[c]
    segs = [(S, E, 0.0, 0.35), (E, X, 0.35, 0.6), (X, Z, 0.6, 1.0)]
    for p, q, a, b in segs:
        k = clamp((u - a) / (b - a))
        if k <= 0: break
        q2 = (lerp(p[0], q[0], k), lerp(p[1], q[1], k))
        d.line([p, q2], fill=A(col, kd), width=5)
        if k > 0.6: chev(d, p, q, A(col, kd))


def trace(d, c, kd=0.55):
    X, th, _ = PATHS[c]; Z = ray_end(X, th)
    d.line([X, Z], fill=A(COLS[c], kd), width=3)


def ref_dir(d, X, ka=1.0):
    """duong net dut: huong tia toi keo dai tu diem ra"""
    dash(d, X, (X[0] + 400 * DIN[0], X[1] + 400 * DIN[1]), A(NAVY, 0.75 * ka), w=3)


def d_arc(d, c, r, ka=1.0, lab=True):
    X, th, _ = PATHS[c]
    d.arc([X[0] - r, X[1] - r, X[0] + r, X[1] + r], TH_IN, th, fill=A(COLS[c], ka), width=5)
    if lab:
        mid = math.radians((TH_IN + th) / 2)
        text(d, (X[0] + (r + 34) * math.cos(mid), X[1] + (r + 34) * math.sin(mid)), "D", 44, COLS[c], alpha=ka)


LAB_Y = [770, 836, 902]                                       # cot nhan ben phai dau tia, cach nhau 66 px


def end_label(d, c, ka=1.0):
    X, th, _ = PATHS[c]; Z = ray_end(X, th)
    d.line([Z, (950, LAB_Y[c])], fill=A(COLS[c], 0.8 * ka), width=2)
    text(d, (960, LAB_Y[c]), NAMES[c], 42, COLS[c], anchor="lm", alpha=ka)


def table(d, n, y0, ka=1.0):
    card(d, (60, y0, 1020, y0 + 330), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    text(d, (170, y0 + 50), "Màu", 40, MUTED, bold=False, alpha=ka)
    text(d, (490, y0 + 50), "D ba lần đo", 40, MUTED, bold=False, alpha=ka)
    text(d, (860, y0 + 50), "Trung bình", 40, MUTED, bold=False, alpha=ka)
    d.line([(90, y0 + 90), (990, y0 + 90)], fill=A(LIGHT, ka), width=3)
    for j in range(n):
        yy = y0 + 140 + 72 * j
        text(d, (170, yy), NAMES[j], 44, COLS[j], alpha=ka)
        text(d, (490, yy), " ; ".join(READS[j][:3]), 44, INK, bold=False, alpha=ka)
        text(d, (860, yy), READS[j][3], 46, INK, alpha=ka)
    text(d, (1010, y0 + 370), "số liệu minh hoạ", 40, MUTED, bold=False, anchor="rm", alpha=ka)


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh; vien NAVY, chu INK) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    prism(d); pen(d)
    dash(d, S, E, A(GRAY, 0.9), w=4)
    normal_at_E(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(NAVY, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(42)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 92), fill=A(NAVY, a), r=32)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", 42, WHITE, alpha=a)
    ctext(d, y0 + 270, "Chiếu laser đỏ, lục, tím\nvào cùng điểm, cùng góc tới.\nTia ló nào lệch nhiều nhất?",
          46, INK, maxw=940, alpha=a)
    text(d, (W / 2, y0 + 455), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 515, 940, y0 + 527], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 515, 140 + 800 * (1 - p), y0 + 527], radius=6, fill=A(NAVY, a))


# ---------------- canh 2: Tien hanh ----------------
T0, DT = 0.6, 3.4          # mau c: bat tia T0 + DT.c ; tia di 1,0 s ; cung D sau 1,3 s ; hang bang sau 1,8 s ; tat sau 3,1 s
B_RUN, B_ARC, B_ROW, B_OFF = 1.0, 1.3, 1.8, 3.1


def state_do(t):
    """(mau dang chieu hoac -1, tien do tia, cung D dang hien, so hang bang, cac vet da vach)"""
    cur, u, arc, n, traced = -1, 0.0, False, 0, []
    for c in range(3):
        tc = T0 + DT * c
        if t >= tc + B_ROW: n = c + 1
        if t >= tc + B_OFF: traced.append(c)
        elif t >= tc:
            cur, u, arc = c, clamp((t - tc) / B_RUN), t >= tc + B_ARC
    return cur, u, arc, n, traced


def s_do(img, d, t, sc):
    cur, u, arc, n, traced = state_do(t)
    prism(d); normal_at_E(d, lab=False)
    for c in traced: trace(d, c); end_label(d, c, 0.8)
    pen(d, COLS[cur] if cur >= 0 else None)
    if cur >= 0:
        beam(d, cur, u)
        if u >= 1: end_label(d, cur)
        if arc:
            X = PATHS[cur][0]; ka = 1.0
            ref_dir(d, X, ka); d_arc(d, cur, 130, ka)
    if n > 0: table(d, n, 1040)


# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · tia tím lệch nhiều nhất"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 226, W / 2 + pw / 2, 292), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 259), lab, 42, WHITE, alpha=ka)
    prism(d); pen(d); normal_at_E(d, lab=False)
    d.line([S, E], fill=A(GRAY, 0.9), width=5)
    for c in range(3):
        X, th, _ = PATHS[c]
        d.line([E, X], fill=A(COLS[c], 0.7), width=3)
        d.line([X, ray_end(X, th)], fill=COLS[c], width=4)
        end_label(d, c)
    ref_dir(d, PATHS[1][0])
    k1 = appear(t, M[0] + 0.4, 0.4)
    for c, r in zip(range(3), (120, 165, 210)):
        if k1 > 0: d_arc(d, c, r, k1, lab=False)
    k2 = appear(t, M[0] + 1.0, 0.4)
    if k2 > 0:                                               # chi chot tim; khong so do < luc (Cau 2 sau hop)
        card(d, (60, 1040, 1020, 1180), fill=A(WHITE, k2), outline=A(LIGHT, k2), w=3)
        text(d, (W / 2, 1110), "Tím: D = 52,3°, lớn nhất", 46, COLS[2], alpha=k2)
    k3 = appear(t, M[1] + 0.2, 0.4)
    if k3 > 0:
        card(d, (60, 1220, 1020, 1470), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), r=22, w=3)
        text(d, (W / 2, 1280), "n giả định của mô hình", 42, MUTED, bold=False, alpha=k3)
        text(d, (W / 2, 1345), "tím: n = 1,652, lớn nhất", 46, DGREEN, alpha=k3)
        text(d, (W / 2, 1415), "n lớn → lệch nhiều", 44, DGREEN, alpha=appear(t, M[1] + 1.2, 0.4))


# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    prism(d); pen(d)
    d.line([S, E], fill=A(GRAY, 0.9), width=5)
    for c in range(3):
        X, th, _ = PATHS[c]
        d.line([E, X], fill=A(COLS[c], 0.7), width=3)
        d.line([X, ray_end(X, th)], fill=COLS[c], width=4)
        end_label(d, c)
    ref_dir(d, PATHS[0][0])
    if a1 > 0:
        k3 = a1 * appear(t, 0.3, 0.5); k4 = a1 * appear(t, 2.3, 0.5)          # ✓ tre 2 s, con >= 3 s
        if k4 > 0: d_arc(d, 0, 140, k4, lab=False)
        y0 = 1040
        card(d, (40, y0, 1040, y0 + 360), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(42)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 61), "BẪY", 42, WHITE, alpha=a1)
        text(d, (470, y0 + 150), "Tia đỏ lệch nhiều nhất", 46, DRED, alpha=k3)
        text(d, (900, y0 + 152), "✗", 70, DRED, alpha=k3)
        text(d, (470, y0 + 235), "Đỏ gần hướng tia tới nhất", 44, DGREEN, alpha=k4)
        text(d, (470, y0 + 300), "→ đỏ lệch ít nhất", 44, DGREEN, alpha=k4)
        text(d, (900, y0 + 268), "✓", 70, DGREEN, alpha=k4)
    if k2 > 0:
        y0 = 1060 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 330), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Số liệu minh hoạ", "• n chỉ là giả định")):
            kk = k2 * appear(t, M[1] + 0.1 + 0.3 * j, 0.4)
            text(d, (90, y0 + 170 + j * 95), l1, 44, INK, anchor="lm", alpha=kk)


# ---------------- canh 5: Chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    """Chot (khong neu thu tu mau) -> THU NGHI: laser cam, i = 50 do -> D khoang nao? (giua 47,7 va 49,3); goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Cùng góc tới: mỗi màu\nlệch một góc riêng", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (40, 600, 1040, lerp(1060, 1340, kh)), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(42)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 696), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 663), "THỬ NGHĨ", 42, WHITE, alpha=k1)
    ctext(d, 870, "Laser màu cam, vẫn góc tới\n50°: góc lệch D vào khoảng nào?",
          48, INK, maxw=940, alpha=appear(t, M[0] + 0.9, 0.5))
    if kh > 0:
        card(d, (110, 1040, 970, 1310), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1095, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1205, "Cam nằm đâu giữa\ncác màu đã đo?", 44, ORANGE, maxw=820, alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    cs += [(do["t0"] + T0 + DT * c, "tap") for c in range(3)]
    cs += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.5, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return cs


CLIP = dict(id="tn-l9-langkinh-03", header="KHTN 9 · THÍ NGHIỆM", footer="Lăng kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ba tia laser, một lăng kính", draw=s_hook, tail=0.8, caps=[
   ("Góc tới 50° cho cả ba lần.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Chiếu lần lượt từng màu.", 4.6),
   ("Vạch tia ló, đo góc lệch D.", 5.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Cùng lăng kính, cùng góc tới.", 3.6),
   ("Mỗi màu một chiết suất.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.8, caps=[
   ("Màu nào lệch ít nhất?", 5.0),
   ("Chưa nói được điều gì?", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 6.6)]),
])
