# Clip: tn-l11-tudien-02 - Do Q theo U de suy ra dien dung (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-tudien-02.json (ghi_chu: "So lieu minh hoa = mo hinh Q = 480.U
#   cong nhieu do" -> nhan "số liệu mô phỏng"):
#   so_lieu_mau (U V, Q uC, Q/U uF): 2 980 490,0 ; 4 1900 475,0 ; 6 2890 481,7 ; 8 3820 477,5 ; 10 4800 480,0
#   trung binh Q/U ~ 481 uF (ghi_chu) ; tu ghi 470 uF - 16 V (dung_cu) ; tu hoa sai so che tao +-20% (rut_ra).
#   Cau hoi chot: U = 12 V (tham_so U max 12, < 16 V an toan; chua tung hien tren man) -> Q = 480.12 = 5760 uC.
# Mach (vat li): nguon (+) -> khoa dao K vi tri 1 -> ban (+) cua tu ; ban (-) -> day chung -> nguon (-).
#   Nap: dong qui uoc tu cuc + nguon vao ban +. Phong: K sang vi tri 2, dong ra tu ban + qua cam bien roi ve ban -.
#   Von ke mac song song voi tu (chi U nap; sau khi phong ve 0,0 V). So chi cam bien, von ke va hang bang doi CUNG luc.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (lan 2 V lam cham, tua nhanh 4..10 V) -> Dap an (do thi Q-U
#       qua goc, duong dong diem 10 V, cot Q/U, lan 2 V lech nhieu nhat) -> Bay (lay 470 uF tren vo) roi Chua noi duoc
#       -> Chot + cau hoi tu nho lai (12 V).
from engine import *

ROWS = [(2, 980, 490.0), (4, 1900, 475.0), (6, 2890, 481.7), (8, 3820, 477.5), (10, 4800, 480.0)]   # so_lieu_mau
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
DRED = (185, 28, 28)
WIRE = NAVY
BOXF = (70, 78, 100)
SCR = (220, 240, 225)
ARR = (194, 65, 12)                    # mui ten chieu dong (cam dam)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
YT, YR = 330, 930                      # day tren / day chung (duoi)
C1, C2, P = (440, YT), (640, YT), (540, 420)  # tiep diem 1 (nap), 2 (phong), chot dao cua khoa K
XC = 540                               # truc tu dien

def wire(d, pts, w=5): d.line(pts, fill=WIRE, width=w, joint="curve")

def circuit(d, blade=0.0, vread="0,0 V", qread="0 μC", charge=0.0, mode=None, t=0.0, knob=0.0, lbl=True):
    """blade 0 = K o vi tri 1 (nap), 1 = vi tri 2 (phong). charge 0..1 = dau +/- tren hai ban.
    mode 'nap' / 'phong' ve mui ten chieu dong qui uoc."""
    # day noi
    wire(d, [(170, 440), (170, YT), (C1[0], YT)])
    wire(d, [(C2[0], YT), (920, YT), (920, 440)])
    wire(d, [P, (XC, 560)])
    wire(d, [(XC, 600), (XC, YR)])
    wire(d, [(XC, 480), (380, 480), (380, 500)])
    wire(d, [(380, 660), (380, YR)])
    wire(d, [(170, 700), (170, YR), (920, YR), (920, 700)])
    for x in (380, XC):
        dot(d, x, YR, 9, WIRE)
    dot(d, XC, 480, 9, WIRE)
    # khoa dao K
    for i, (c, lab) in enumerate(((C1, "1"), (C2, "2"))):
        on = (blade < 0.5) if i == 0 else (blade >= 0.5)
        dot(d, c[0], c[1], 14 if on else 12, WIRE if on else WHITE, outline=WIRE)
        text(d, (c[0], c[1] - 46), lab, 38, MUTED)
    ang0, ang1 = math.atan2(C1[1] - P[1], C1[0] - P[0]), math.atan2(C2[1] - P[1], C2[0] - P[0])
    ang = lerp(ang0, ang1, ease(blade)); L = math.hypot(C1[0] - P[0], C1[1] - P[1])
    d.line([P, (P[0] + L * math.cos(ang), P[1] + L * math.sin(ang))], fill=WIRE, width=8)
    dot(d, P[0], P[1], 13, WIRE)
    text(d, (P[0] + 44, P[1] + 4), "K", 40, INK, anchor="lm")
    # tu dien: ban + (tren), ban - (duoi, day hon)
    d.rectangle([480, 554, 600, 563], fill=WIRE)
    d.rectangle([480, 597, 600, 610], fill=WIRE)
    text(d, (610, 556), "+", 40, RED, anchor="lm")
    text(d, (610, 604), "−", 40, BLUE, anchor="lm")
    text(d, (648, 556), "470 μF", 38, INK, anchor="lm")
    text(d, (648, 606), "16 V", 38, INK, anchor="lm")
    if charge > 0:
        for x in (500, 580):
            text(d, (x, 526), "+", 38, RED, alpha=charge)
            text(d, (x, 640), "−", 38, BLUE, alpha=charge)
    # nguon
    card(d, (60, 440, 280, 700), fill=BOXF, r=22)
    text(d, (170, 482), "nguồn", 38, WHITE)
    dot(d, 170, 590, 52, (200, 205, 215), outline=WHITE)
    a = math.radians(-220 + 260 * knob)
    d.line([(170, 590), (170 + 42 * math.cos(a), 590 + 42 * math.sin(a))], fill=NAVY, width=7)
    text(d, (236, 404), "+", 40, RED)
    text(d, (210, 736), "−", 40, BLUE)
    # von ke (song song voi tu)
    card(d, (290, 500, 470, 660), fill=BOXF, r=18)
    text(d, (380, 532), "vôn kế", 36, WHITE)
    card(d, (302, 560, 458, 646), fill=SCR, r=10)
    text(d, (380, 603), vread, 40, (20, 60, 30))
    # cam bien dien tich
    card(d, (800, 440, 1040, 700), fill=BOXF, r=22)
    card(d, (812, 466, 1028, 556), fill=SCR, r=10)
    text(d, (920, 511), qread, 40, (20, 60, 30))
    text(d, (920, 600), "bộ đo", 38, WHITE)
    text(d, (920, 648), "điện lượng", 38, WHITE)
    text(d, (955, 404), "+", 40, RED)
    # chieu dong qui uoc
    if mode:
        col = ARR
        if mode == "nap":                          # nguon + -> K(1) -> ban + ; ban - -> day chung -> nguon -
            arrow(d, (170, 425), (170, 352), col, w=11, head=30)
            arrow(d, (235, YT), (375, YT), col, w=11, head=30)
            arrow(d, (XC, 492), (XC, 546), col, w=11, head=26)
            arrow(d, (490, YR), (330, YR), col, w=11, head=30)
            if lbl: text(d, (300, 276), "dòng nạp", 40, ARR)
        else:                                      # ban + -> K(2) -> bo do ; ve ban - qua day chung
            arrow(d, (XC, 546), (XC, 492), col, w=11, head=26)
            arrow(d, (690, YT), (850, YT), col, w=11, head=30)
            arrow(d, (920, 352), (920, 425), col, w=11, head=30)
            arrow(d, (850, YR), (690, YR), col, w=11, head=30)
            if lbl: text(d, (1000, 276), "phóng qua bộ đo", 40, ARR, anchor="rm")

def table(d, n, qu=0, y=1000, hl=None, ka=1.0):
    """Bang U - Q - Q/U; n hang da co; qu = so hang da hien cot Q/U (con lai '?')."""
    card(d, (40, y, 1040, y + 510), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 530, 830)
    for x, c in zip(xs, ("U (V)", "Q (μC)", "Q/U (μF)")): text(d, (x, y + 50), c, 40, INK)
    d.line([(70, y + 90), (1010, y + 90)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 136 + i * 80; u, q, r = ROWS[i]
        if hl == i: d.rounded_rectangle([60, yy - 36, 1020, yy + 36], radius=18, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), str(u), 44, INK); text(d, (xs[1], yy), str(q), 44, INK)
        if i < qu: text(d, (xs[2], yy), vn(r), 44, BLUE)
        else: text(d, (xs[2], yy), "?", 44, GRAY)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 260, "Nạp tụ ở U càng lớn thì\ntỉ số Q/U tính ra\nthay đổi thế nào?", 50, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 512], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 512], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
FF0, FFW = 0.2, 1.4      # tua nhanh: lan do 4..10 V bat dau tu M[1] + FF0, moi lan FFW giay
SW = 0.7                 # trong moi lan tua nhanh: K sang vi tri 2 o w = SW
TSW = 2.6                # lan 2 V: K sang vi tri 2 o t = TSW

def s_do(img, d, t, sc):
    M = sc["M"]
    if t < M[1]:                                   # lan 2 V, lam cham
        u, q, _ = ROWS[0]
        done = t >= TSW                            # K sang 2: von ke 0, bo do hien Q, hang bang hien CUNG luc
        blade = 1.0 if done else 0.0
        charged = 0.0 if done else clamp((t - 0.6) / 1.0)
        vr = vn(u) + " V" if 1.6 <= t < TSW else "0,0 V"
        mode = "nap" if 0.6 <= t < 1.7 else ("phong" if TSW <= t < TSW + 0.9 else None)
        circuit(d, blade, vr, f"{q} μC" if done else "0 μC", charged, mode, t, knob=u / 10 * appear(t, 0.2, 0.4))
        table(d, 1 if done else 0)
        return
    card(d, (760, 214, 1000, 274), fill=ORANGE, r=30); text(d, (880, 244), "tua nhanh", 38, WHITE)
    w_all = t - M[1] - FF0
    if w_all < 0:
        u, q, _ = ROWS[0]
        circuit(d, 1, "0,0 V", f"{q} μC", 0, None, t, knob=u / 10); table(d, 1); return
    j = 1 + max(0, min(3, int(w_all // FFW))); w = w_all - (j - 1) * FFW
    u, q, _ = ROWS[j]
    if w < SW:                                     # K o 1: nap, von ke chi U, cam bien ve 0
        circuit(d, 0.0, vn(u) + " V", "0 μC", clamp(w / 0.25), "nap" if w < 0.45 else None, t,
                knob=u / 10, lbl=False)
        table(d, j)
    else:                                          # K o 2: phong; Q, von ke 0 va hang bang doi cung luc
        circuit(d, 1, "0,0 V", f"{q} μC", 0, None, t, knob=u / 10)
        table(d, j + 1)

# ---------------- canh 3: Dap an + rut ra ----------------
GX0, GX1, GY0, GY1 = 200, 940, 880, 420        # truc Q theo U: U 0-11 V, Q 0-5500 uC
def gx(u): return GX0 + u / 11 * (GX1 - GX0)
def gy(q): return GY0 - q / 5500 * (GY0 - GY1)

def dash(d, p1, p2, col, w=3, on=12, off=10):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (on + off)) + 1
    for i in range(n):
        a, b = i * (on + off) / L, min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=col, width=w)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · Q/U gần như không đổi"
    pw = tw(d, lab, F(40)) + 52
    card(d, (W - 60 - pw, 234, W - 60, 298), fill=A(NAVY, ka), r=32)
    text(d, (W - 60 - pw / 2, 266), lab, 40, WHITE, alpha=ka)
    card(d, (40, 320, 1040, 970), fill=WHITE, outline=LIGHT, w=3)
    text(d, (1000, 362), "số liệu mô phỏng", 36, MUTED, bold=False, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 34, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 20, GY1 - 40), "Q (μC)", 38, INK, anchor="lm")
    text(d, (1000, GY0 - 44), "U (V)", 38, INK, anchor="rm")
    for u in (2, 4, 6, 8, 10):
        d.line([(gx(u), GY0), (gx(u), GY0 + 12)], fill=NAVY, width=3); text(d, (gx(u), GY0 + 40), str(u), 38, MUTED, bold=False)
    kd = appear(t, M[0] + 1.6, 0.4)                # duong dong diem (10 V ; 4800 uC); nhan 4000 tat khi 4800 hien
    for q in (2000, 4000):
        d.line([(GX0 - 12, gy(q)), (GX0, gy(q))], fill=NAVY, width=3)
        text(d, (GX0 - 20, gy(q)), str(q), 38, MUTED, bold=False, anchor="rm", alpha=1 - kd if q == 4000 else 1)
    kl = appear(t, M[0] + 0.6, 0.8)                # duong thang qua goc, he so goc 480 uF
    if kl > 0:
        u1 = 10.5 * kl
        d.line([(gx(0), gy(0)), (gx(u1), gy(480 * u1))], fill=A(GREEN, 0.9), width=5)
        if kl >= 1: text(d, (465, 770), "đường thẳng qua gốc", 38, GREEN, anchor="lm")
    if kd > 0:
        col = A(BLUE, kd)
        dash(d, (gx(10), gy(4800)), (gx(10), GY0), col); dash(d, (gx(10), gy(4800)), (GX0, gy(4800)), col)
        text(d, (GX0 - 20, gy(4800)), "4800", 38, BLUE, anchor="rm", alpha=kd)
    for i, (u, q, r) in enumerate(ROWS):
        k = appear(t, 0.2 + 0.15 * i, 0.3)
        if k > 0: dot(d, gx(u), gy(q), 13, A(ORANGE if (i == 0 and t >= M[1] - 0.1) else BLUE, k), outline=WHITE)
    hl = 0 if t >= M[1] - 0.1 else None
    table(d, 5, qu=sum(t >= 0.3 + 0.2 * i for i in range(5)), y=990, hl=hl, ka=appear(t, M[1] - 0.1, 0.3))
    k1 = appear(t, 1.4, 0.4) * (1 - appear(t, M[1] - 0.1, 0.3))
    k2 = appear(t, M[1] + 0.2, 0.4)
    if k1 > 0:
        card(d, (40, 1515, 1040, 1605), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=20, w=3)
        text(d, (W / 2, 1560), "Trung bình: C = Q/U ≈ 481 μF", 42, (21, 110, 55), alpha=k1)
    if k2 > 0:
        card(d, (40, 1515, 1040, 1605), fill=A((255, 237, 213), k2), outline=A(ORANGE, k2), r=20, w=3)
        text(d, (W / 2, 1560), "Lần đo ở 2 V lệch nhiều nhất", 42, (154, 52, 18), alpha=k2)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def can(d):
    """Tu hoa phong to: than tru, soc mau nhat ben phai ghi '−', chu tren vo 470 uF / 16 V; chan + dai hon."""
    x0, x1, y0, y1 = 400, 680, 360, 860
    d.line([(480, y1), (480, 970)], fill=GRAY, width=8); d.line([(600, y1), (600, 930)], fill=GRAY, width=8)
    text(d, (440, 950), "+", 44, RED); text(d, (640, 920), "−", 44, BLUE)
    d.rounded_rectangle([x0, y0, x1, y1], radius=28, fill=(40, 52, 110), outline=NAVY, width=4)
    d.rectangle([x1 - 70, y0 + 20, x1 - 14, y1 - 20], fill=(150, 165, 200))
    for yy in (470, 610, 750): text(d, (x1 - 42, yy), "−", 40, NAVY)
    d.line([(x0 + 60, y0 + 30), (x1 - 100, y0 + 30)], fill=(90, 105, 160), width=4)
    text(d, ((x0 + x1 - 70) / 2, 580), "470 μF", 46, WHITE)
    text(d, ((x0 + x1 - 70) / 2, 650), "16 V", 40, WHITE)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    can(d)
    if a1 > 0:
        y0 = 1000
        card(d, (40, y0, 1040, y0 + 580), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        k3 = a1 * appear(t, 0.5, 0.5); k4 = a1 * appear(t, 1.6, 0.5)
        ctext(d, y0 + 230, "Trên vỏ: 470 μF\n(số danh định, ±20%)", 44, INK, maxw=920, alpha=k3)
        ctext(d, y0 + 430, "Đo được: ≈ 481 μF,\nvẫn trong khoảng đó", 44, (21, 110, 55), maxw=920, alpha=k4)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 580), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• C phụ thuộc gì ở cấu tạo tụ?", "• Tụ trữ năng lượng bao nhiêu?")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 230 + j * 150), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: nap tu nay o 12 V thi Q bao nhieu (Q = C.U); goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Q/U không đổi: đó là điện dung C của tụ", 50, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1590), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 880, "Nạp tụ này ở 12 V thì\nđiện tích Q khoảng\nbao nhiêu μC?", 50, INK, maxw=920,
          alpha=appear(t, M[0] + 0.9, 0.5))
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (110, 1140, 970, 1480), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1215, "Gợi ý", 40, INK, alpha=kh)
    ctext(d, 1340, "Q = C · U", 56, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.3, "ding"),
           (do["t0"] + TSW, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW + SW, "tick") for j in range(4)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out

CLIP = dict(id="tn-l11-tudien-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Tụ điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nạp tụ, đo điện tích", draw=s_hook, tail=0.8, caps=[
   ("Nạp tụ ở U, rồi đo điện tích Q.", 2.8),
   ("Tự đoán trước khi xem tiếp.", 6.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Nạp ở 2 V, rồi phóng qua bộ đo.", 4.2),
   ("Lặp lại ở 4, 6, 8, 10 V.", 6.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Q tăng tỉ lệ thuận với U.", 3.6),
   ("Sai số mỗi lần đo ≤ 2,5%.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.9, caps=[
   ("Bẫy: lấy số trên vỏ.", 3.8),
   ("Thí nghiệm này mới đo một tụ.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.4)]),
])
