# Clip: tn-l9-khucxa-02 - Do goc khuc xa qua khoi nhua ban tru tren dia chia do (KHTN 9, lo 11, 19/11/2026)
# Dung lai 20/11/2026 theo cong moi (KE-HOACH-CAI-TIEN-CLIP viec 4): chu than canh >= 55 (ra >= 48 px), khong chu xam nhat,
#   nhan i, r giu suot Tien hanh, mot nhip rieng "sin = doan ngang toi phap tuyen" truoc cot so, Ket qua neu
#   "≈ 1,5 = chiet suat n", Bay = hai bieu do cot canh nhau (i : r doi / sin i : sin r giu), bo canh tinh cuoi (cau chot A-D o khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-khucxa-02.json (_kiem_so()):
#   so_lieu_mau (i, r doc, sin i / sin r): 20 13 1,52 | 35 22 1,53 | 50 31 1,49 | 65 37 1,51 | 80 41 1,50 ; n = 1,5.
# Du doan (K10, khong nut A-D): i tang deu 20 -> 80 do (moi lan +15 do), r thay doi the nao?
#   -> dap an: r tang, ve sau them it dan (+9 +9 +6 +4). Hop du doan chi co cau hoi + hinh.
# Hop exp: cau "Doc so lieu" sau video hoi TRUNG BINH nam ti so va LAN LECH NHIEU NHAT -> clip KHONG tinh trung binh,
#   KHONG noi lan nao lech.
# Hinh: mat phang khoi ban tru nam ngang qua tam dia, khoi o duoi; tia toi tu tren-trai vao tam, tia khuc xa xuong-phai,
#   di theo ban kinh nen khong gay o mat cong. Goc ve = Snell dung (n = 1,5); so doc = so lam tron trong kho (assert).
# Nhip sin (i = 50, hang kho): dia ban kinh R = 1 -> doan ngang tu dau tia toi phap tuyen = sin i;
#   sin 50 = 0,766 ; sin 31 = 0,515 ; 0,766 : 0,515 = 1,49 (= cot kho). Cac hang khac: bam may tinh.
# Vong 2 (20/11, cong B kiem-code): 10 gop y -> nhip sin co so, phu de bam may, du doan >= 5 s, de THU NGHI hien ngay,
#   o r hien cung luc hang bang, phu de 'Goc r do tu phap tuyen', phong dia nhip sin + quat ket qua, nhan co nen, bay co chuyen dong.
# Bay = hien_tuong_hay_sai[0] (chia i cho r): 20 : 13 ≈ 1,54 ; 80 : 41 ≈ 1,95 canh 1,52 ; 1,50 (bang kho).
# Chua noi duoc = ghi_chu kho "so lieu minh hoa, chua phai so do that".
# THU NGHI = dung ca cau_chot trong content/thi-nghiem/video-khung/tn-l9-khucxa-02.json: r = 25 do -> i ? (dap an 39 do,
#   KHONG in tren man, KHONG ve tia toi; man chot khong ghi cong thuc sin).
from engine import *

N = 1.5
ROWS = [(20, 13, "1,52"), (35, 22, "1,53"), (50, 31, "1,49"), (65, 37, "1,51"), (80, 41, "1,50")]
CHOT_R, CHOT_I = 25, 39
I_SIN = 50          # goc minh hoa nhip sin (mot hang trong bang)
SIN_SO = ("0.766", "0.515")   # sin 50°, sin 31° (r doc cua hang 50°)


def r_of(i): return math.degrees(math.asin(math.sin(math.radians(i)) / N))


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-khucxa-02.json")))
    hang = k["so_lieu_mau"]["hang"]
    assert len(hang) == len(ROWS)
    for (i, r, q), h in zip(ROWS, hang):
        assert [i, r] == h[:2], (i, r, h)
        assert q == f"{h[2]:.2f}".replace(".", ","), (q, h[2])
        assert round(r_of(i)) == r, (i, r_of(i))                       # tia ve dung Snell khop so doc
        assert r < i                                                    # vao nhua: lech gan phap tuyen
        qq = math.sin(math.radians(i)) / math.sin(math.radians(r))
        assert abs(qq - h[2]) < 0.006, (i, qq)
    assert k["tham_so"][1]["gia_tri"] == N
    assert abs(20 / 13 - 1.54) < 0.005 and abs(80 / 41 - 1.95) < 0.005     # so bay
    assert round(math.degrees(math.asin(N * math.sin(math.radians(CHOT_R))))) == CHOT_I
    assert "r = 25°" in k["so_lieu_mau"]["ghi_chu"]
    assert I_SIN in [h[0] for h in hang]
    rs = dict((h[0], h[1]) for h in hang)[I_SIN]
    si, sr = math.sin(math.radians(I_SIN)), math.sin(math.radians(rs))
    assert (f"{si:.3f}", f"{sr:.3f}") == SIN_SO and f"{si / sr:.2f}" == "1.49" == f"{dict((h[0], h[2]) for h in hang)[I_SIN]:.2f}"
    kh = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "video-khung", "tn-l9-khucxa-02.json")))
    assert f"r = {CHOT_R}°" in kh["cau_chot"]["cau_hoi"]                # THU NGHI hoi dung ca cau chot cua khung web
_kiem_so()

C = (540, 630); RD, RB = 350, 280
DISK = (246, 243, 236); RING = (95, 90, 80); BLOCK = (191, 219, 254); BEAM = (220, 38, 38); DRED = (185, 28, 28)
DGREEN = (10, 110, 50); DINK = (60, 66, 90); DPURP = (76, 29, 149)
FS, FM = 58, 56     # co chu than canh (ve), ra 51 / 49 px trong mp4


def u_in(i):   # huong tu tam ve phia nguon (tren-trai)
    return (-math.sin(math.radians(i)), -math.cos(math.radians(i)))


def u_out(r):  # huong tia khuc xa (duoi-phai)
    return (math.sin(math.radians(r)), math.cos(math.radians(r)))


def P(u, L, c=C): return (c[0] + u[0] * L, c[1] + u[1] * L)


def _kiem_hinh():
    for i, r, _ in ROWS:
        a, b = u_in(i), u_out(r_of(i))
        assert a[0] < 0 and a[1] < 0 and b[0] > 0 and b[1] > 0          # tia toi, tia khuc xa o hai ben phap tuyen
        assert abs(math.degrees(math.acos(-a[1])) - i) < 1e-6 and abs(math.degrees(math.acos(b[1])) - r_of(i)) < 1e-6
        assert abs(b[0] * b[0] + b[1] * b[1] - 1) < 1e-9                  # tia trong khoi di theo ban kinh
    for i, _, _ in ROWS:                                                  # but laser khong ra ngoai vung an toan
        assert P(u_in(i), RD + 110)[1] >= 190 and P(u_in(i), RD + 110)[0] >= 20
_kiem_hinh()


def dash(d, p1, p2, col, w=3, on=14, off=10):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (on + off)) + 1
    for k in range(n):
        a, b = k * (on + off) / L, min(1, (k * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=col, width=w)


def chev(d, p, q, col, s=18, w=5):
    x, y = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2; ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=col, width=w)


def lab(d, xy, s, size, col, alpha=1.0):
    """Nhan co nen be mo phia sau (khong de chu de len vach chia / mep khoi)."""
    if alpha <= 0: return
    w = tw(d, s, F(size)); h = size * 0.62
    d.rounded_rectangle([xy[0] - w / 2 - 14, xy[1] - h - 4, xy[0] + w / 2 + 14, xy[1] + h + 4], radius=18, fill=A(BG, 0.92 * alpha))
    text(d, xy, s, size, col, alpha=alpha)


def disk(d, normal_lab=False):
    d.ellipse([C[0] - RD, C[1] - RD, C[0] + RD, C[1] + RD], fill=DISK, outline=RING, width=4)
    for deg in range(0, 360, 10):
        a = math.radians(deg); L = 24 if deg % 30 == 0 else 13
        d.line([(C[0] + (RD - L) * math.cos(a), C[1] + (RD - L) * math.sin(a)),
                (C[0] + RD * math.cos(a), C[1] + RD * math.sin(a))], fill=RING, width=3)
    # khoi nhua ban tru: nua duoi, mat phang ngang qua tam
    d.pieslice([C[0] - RB, C[1] - RB, C[0] + RB, C[1] + RB], 0, 180, fill=A(BLOCK, 0.85), outline=BLUE, width=4)
    d.line([(C[0] - RB, C[1]), (C[0] + RB, C[1])], fill=BLUE, width=5)
    dash(d, (C[0], C[1] - RD + 6), (C[0], C[1] + RD - 6), NAVY, w=4)
    lab(d, (C[0] + 0.94 * RD, C[1] + 0.86 * RD), "nhựa", FM, BLUE)
    lab(d, (C[0] + 0.75 * RD, C[1] - 0.45 * RD), "không khí", FM, DINK)
    if normal_lab: lab(d, (C[0] + 150, C[1] - RD + 58), "pháp tuyến", FM, NAVY)


def pen(d, i, on=True):
    u = u_in(i); a, b = P(u, RD + 22), P(u, RD + 110)
    d.line([a, b], fill=(55, 60, 75), width=34)
    if on: dot(d, a[0], a[1], 10, BEAM)


def beam(d, i, ka=1.0, lab=True):
    r = r_of(i); a, ce, b = P(u_in(i), RD + 22), C, P(u_out(r), RD)
    d.line([a, ce], fill=A(BEAM, ka), width=7); chev(d, a, ce, A(BEAM, ka))
    d.line([ce, b], fill=A(BEAM, ka), width=7); chev(d, ce, P(u_out(r), RB), A(BEAM, ka))
    d.arc([C[0] - 130, C[1] - 130, C[0] + 130, C[1] + 130], 270 - i, 270, fill=A(NAVY, ka), width=6)
    d.arc([C[0] - 170, C[1] - 170, C[0] + 170, C[1] + 170], 90 - r, 90, fill=A(DGREEN, ka), width=6)
    if lab:
        m = math.radians(270 - i / 2); text(d, (C[0] + 192 * math.cos(m), C[1] + 192 * math.sin(m)), "i", 62, NAVY, alpha=ka)
        m = math.radians(90 - r / 2); text(d, (C[0] + 232 * math.cos(m), C[1] + 232 * math.sin(m)), "r", 62, DGREEN, alpha=ka)


def readout(d, i, r, ka_r):
    card(d, (90, 1005, 500, 1090), fill=WHITE, outline=NAVY, r=24, w=4)
    text(d, (295, 1047), f"i = {i}°" if i is not None else "i = …", FS, NAVY)
    card(d, (580, 1005, 990, 1090), fill=WHITE, outline=DGREEN, r=24, w=4)
    if ka_r > 0: text(d, (785, 1047), f"r = {r}°", FS, DGREEN, alpha=ka_r)
    else: text(d, (785, 1047), "r = …", FS, DINK)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    disk(d); pen(d, 20); beam(d, 20, appear(t, 0.5, 0.5))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FM)) + 56
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 96), fill=A(PURPLE, a), r=36)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", FM, WHITE, alpha=a)
    for j, s in enumerate(("i tăng từ 20° tới 80°,", "mỗi lần thêm 15°.", "Góc r đổi thế nào?")):
        text(d, (W / 2, y0 + 160 + j * 78), s, 60, INK, alpha=a)
    # thanh dem nguoc day (thay doi du lon de khong tinh la hinh dung yen)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 410, 970, y0 + 480], radius=35, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 410, 110 + max(70, 860 * (1 - p)), y0 + 480], radius=35, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh ----------------
T0, DT, ROT, READ, ROW = 0.6, 1.2, 0.5, 0.8, 0.8   # o r va hang bang hien CUNG luc
def do_state(t):
    """-> (goc i dang chieu, chi so lan do dang dung (-1 khi dang xoay), so hang bang)."""
    rows, ang, k_on = 0, ROWS[0][0], -1
    for k, (i, r, _) in enumerate(ROWS):
        tk = T0 + DT * k
        if t < tk: break
        if k > 0 and t < tk + ROT:
            ang = lerp(ROWS[k - 1][0], i, ease((t - tk) / ROT)); k_on = -1
        else:
            ang = i; k_on = k if t >= tk + READ else -1
        if t >= tk + ROW: rows = k + 1
    return ang, k_on, rows


def table_do(d, n, y0=1115, hl=-1, khl=0.0):
    card(d, (60, y0, 1020, y0 + 92 + 5 * 70 + 18), fill=WHITE, outline=RING, w=3)
    text(d, (330, y0 + 48), "i", 62, NAVY); text(d, (750, y0 + 48), "r", 62, DGREEN)
    d.line([(90, y0 + 90), (990, y0 + 90)], fill=RING, width=3)
    for j in range(n):
        i, r, _ = ROWS[j]; yy = y0 + 128 + 70 * j
        if j == hl and khl > 0: d.rounded_rectangle([90, yy - 32, 990, yy + 32], radius=14, fill=A((255, 237, 213), khl))
        text(d, (330, yy), f"{i}°", FS, INK); text(d, (750, yy), f"{r}°", FS, INK)


def s_do(img, d, t, sc):
    ang, k_on, rows = do_state(t)
    disk(d); pen(d, ang)
    if t >= T0: beam(d, ang, 1.0)            # nhan i, r giu suot canh, ke ca luc dang xoay
    i_show = next((r_[0] for r_ in ROWS if abs(ang - r_[0]) < 1e-9), None)   # chi so trong kho; dang xoay -> "…"
    if k_on >= 0: readout(d, i_show, ROWS[k_on][1], 1.0)
    else: readout(d, i_show, 0, 0.0)
    hl = rows - 1; khl = 1 - appear(t, T0 + DT * hl + ROW + 0.6, 0.3) if rows > 0 else 0
    table_do(d, rows, hl=hl, khl=khl)


def _kiem_dong_bo():
    """Moi 0,05 s: so r chi hien khi laser dung yen o dung goc cua hang do; hang bang chi hien sau khi doc."""
    bad = []; t = 0.0
    while t < 8.0:
        ang, k_on, rows = do_state(t)
        if k_on >= 0 and abs(ang - ROWS[k_on][0]) > 1e-9: bad.append((round(t, 2), "r hien khi chua dung"))
        if k_on >= 0 and round(r_of(ang)) != ROWS[k_on][1]: bad.append((round(t, 2), "r lech tia"))
        if rows > 0:
            done = max(k for k in range(5) if t >= T0 + DT * k)
            if rows > done + 1: bad.append((round(t, 2), "hang som"))
            if t < T0 + DT * (rows - 1) + READ: bad.append((round(t, 2), "hang truoc khi doc"))
        t += 0.05
    if do_state(6.3)[2] != 5: bad.append("chua du 5 hang")
    return bad


# ---------------- canh 3: sin la gi (bang hinh, dia phong to, mot ca co so) ----------------
def s_sin(img, d, t, sc):
    global C, RD, RB
    old = (C, RD, RB); C, RD, RB = (540, 650), 440, 350
    try:
        i = I_SIN; r = r_of(i)
        disk(d, normal_lab=True); pen(d, i); beam(d, i)
        A_ = P(u_in(i), RD); B_ = P(u_out(r), RD)
        m = P(u_in(i), 385); lab(d, (m[0] - 0.643 * 70, m[1] + 0.766 * 70), "R = 1", FM, NAVY)
        gi, gr = appear(t, 0.5, 0.6), appear(t, 1.3, 0.6)
        if gi > 0:
            d.line([(C[0], A_[1]), (lerp(C[0], A_[0], gi), A_[1])], fill=NAVY, width=12)
            dot(d, A_[0], A_[1], 9, NAVY)
            lab(d, ((C[0] + A_[0]) / 2, A_[1] - 48), "sin i", FS, NAVY, alpha=gi)
        if gr > 0:
            d.line([(C[0], B_[1]), (lerp(C[0], B_[0], gr), B_[1])], fill=DGREEN, width=12)
            dot(d, B_[0], B_[1], 9, DGREEN)
            lab(d, ((C[0] + B_[0]) / 2, B_[1] + 100), "sin r", FS, DGREEN, alpha=gr)
        # hai doan truot xuong cho trong, xep canh nhau, kem so (hang 50° cua bang)
        k = appear(t, 2.2, 0.8)
        if k > 0:
            Li, Lr = C[0] - A_[0], B_[0] - C[0]; x0 = 300
            for L, y_end, y_from, col, s_, v in ((Li, 1215, A_[1], NAVY, "sin i", SIN_SO[0]), (Lr, 1300, B_[1], DGREEN, "sin r", SIN_SO[1])):
                y = lerp(y_from, y_end, k)
                d.rounded_rectangle([x0, y - 16, x0 + L, y + 16], radius=10, fill=A(col, k))
                text(d, (x0 - 25, y), s_, FS, col, anchor="rm", alpha=k)
                text(d, (x0 + L + 25, y), v.replace(".", ","), FS, col, anchor="lm", alpha=appear(t, 2.9, 0.4))
    finally:
        C, RD, RB = old
    kq = appear(t, SIN_Q, 0.45)
    if kq > 0:
        card(d, (110, 1365, 970, 1465), fill=A((236, 253, 243), kq), outline=A(GREEN, kq), r=26, w=4)
        text(d, (W / 2, 1415), f"{SIN_SO[0]} : {SIN_SO[1]} ≈ 1,49".replace(".", ","), 60, DGREEN, alpha=kq)
SIN_Q = 3.8


# ---------------- canh 4: Dap an + Ket qua ----------------
def pill(d, s, y, a, color=NAVY, size=FM):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


XD = (150, 450, 830); Y0D, RH = 370, 80
def table_kq(d, plus, ratio, hdr):
    card(d, (40, Y0D, 1040, Y0D + 92 + 5 * RH + 20), fill=WHITE, outline=RING, w=3)
    text(d, (XD[0], Y0D + 48), "i", 62, NAVY); text(d, (XD[1], Y0D + 48), "r", 62, DGREEN)
    if hdr > 0: text(d, (XD[2], Y0D + 48), "sin i / sin r", FS, INK, alpha=hdr)
    d.line([(70, Y0D + 90), (1010, Y0D + 90)], fill=RING, width=3)
    for j in range(5):
        i, r, q = ROWS[j]; yy = Y0D + 132 + RH * j
        text(d, (XD[0], yy), f"{i}°", FS, INK); text(d, (XD[1], yy), f"{r}°", FS, INK)
        if j > 0 and plus[j] > 0:
            text(d, (XD[0] + 135, yy - RH / 2), "+15°", 55, DINK, alpha=plus[j])
            text(d, (XD[1] + 130, yy - RH / 2), f"+{r - ROWS[j - 1][1]}°", 55, ORANGE, alpha=plus[j])
        if ratio[j] > 0: text(d, (XD[2], yy), q, FS, BLUE, alpha=ratio[j])


C2, RB2 = (540, 960), 370
def fan_kq(d, ks):
    d.pieslice([C2[0] - RB2, C2[1] - RB2, C2[0] + RB2, C2[1] + RB2], 0, 180, fill=A(BLOCK, 0.85), outline=BLUE, width=4)
    d.line([(C2[0] - RB2 - 40, C2[1]), (C2[0] + RB2 + 40, C2[1])], fill=BLUE, width=5)
    dash(d, (C2[0], C2[1] - 48), (C2[0], C2[1] + RB2), NAVY, w=4)
    for k, (i, r, _) in zip(ks, ROWS):
        if k <= 0: continue
        d.line([P(u_in(i), 48, C2), C2], fill=A(BEAM, k), width=6)
        d.line([C2, P(u_out(r_of(i)), RB2, C2)], fill=A(BEAM, k), width=6)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: r tăng, thêm ít dần", 300, appear(t, 0.15, 0.4))
    ks = [appear(t, 0.6 + 0.5 * j, 0.35) for j in range(5)]
    rt = [appear(t, M[1] + 0.1 + 0.3 * j, 0.35) for j in range(5)]
    table_kq(d, ks, rt, appear(t, M[1] + 0.1, 0.4))
    fan_kq(d, ks)
    k = appear(t, M[1] + 2.2, 0.5)
    if k > 0:
        card(d, (50, 1370, 1030, 1480), fill=A((236, 253, 243), k), outline=A(GREEN, k), r=26, w=4)
        text(d, (W / 2, 1425), "≈ 1,5 = chiết suất n của nhựa", 58, DGREEN, alpha=k)


# ---------------- canh 5: Bay + chua noi duoc ----------------
BAY_X, BAY_ST, BAY_E = 2.2, 4.2, 6.3
def bars(d, x0, vals, lab, col, k, ka):
    """Bieu do 2 cot (20°, 80°) trong o rong 460 bat dau x0; k = ti le moc cot, ka = do hien."""
    text(d, (x0 + 230, 530), lab, 60, col, alpha=ka)
    base = 1130
    d.line([(x0 + 20, base), (x0 + 440, base)], fill=A(INK, ka), width=4)
    for j, (v, s, g) in enumerate(vals):
        cx = x0 + 120 + 220 * j; h = 230 * v * k
        if h > 0: d.rectangle([cx - 55, base - h, cx + 55, base], fill=A(col, ka))
        text(d, (cx, base - 230 * v - 40), s, FS, col, alpha=ka * k)
        text(d, (cx, base + 45), g, FS, INK, alpha=ka)


def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.3, 0.45); fl = a1
    pw = tw(d, "BẪY", F(FM)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 338), fill=A(DRED, a1), r=38)
    text(d, (W / 2, 300), "BẪY", FM, WHITE, alpha=a1)
    text(d, (W / 2, 410), "“Chia góc i cho góc r”", 60, INK, alpha=a1)
    card(d, (50, 470, 530, 1300), fill=A(WHITE, a1), outline=A(DRED, fl), w=5)
    bars(d, 60, ((20 / 13, "1,54", "20°"), (80 / 41, "1,95", "80°")), "i : r", DRED, appear(t, 0.6, 1.0), fl)
    text(d, (290, 1245), "✗ tăng dần", 60, DRED, alpha=appear(t, BAY_X, 0.45) * fl / max(a1, 1e-6))
    a2 = appear(t, BAY_ST, 0.45)
    if a2 > 0:
        card(d, (550, 470, 1030, 1300), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        bars(d, 560, ((1.52, "1,52", "20°"), (1.50, "1,50", "80°")), "sin i : sin r", DGREEN, appear(t, BAY_ST, 0.8), a2)
        text(d, (790, 1245), "✓ giữ ≈ 1,5", 60, DGREEN, alpha=a2)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (50, 1345, 1030, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1400), "Chưa nói được:", 58, NAVY, alpha=k3)
        text(d, (W / 2, 1490), "số liệu minh hoạ, chưa đo thật", 56, INK, alpha=k3)


# ---------------- canh 6: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_H, END_C = 0.2, 0.2, 3.0   # de + hinh hien ngay; cau chot (tom tat) hien sau
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Vào nhựa: r nhỏ hơn i, tăng chậm dần", 55, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FM)) + 56
    card(d, (W / 2 - pw / 2, 480, W / 2 + pw / 2, 556), fill=A(ORANGE, k1), r=38)
    text(d, (W / 2, 518), "THỬ NGHĨ", FM, WHITE, alpha=k1)
    text(d, (W / 2, 615), "Cùng khối nhựa (n ≈ 1,5),", 60, INK, alpha=k1)
    text(d, (W / 2, 695), f"đọc r = {CHOT_R}°.", 60, INK, alpha=k1)
    text(d, (W / 2, 775), "Góc tới i khoảng bao nhiêu?", 60, INK, alpha=k1)
    kh = appear(t, END_H, 0.6)
    c3, rb = (540, 1190), 280
    if kh > 0:   # hinh: chi co tia khuc xa r = 25°, tia toi de trong (dau ?)
        d.pieslice([c3[0] - rb, c3[1] - rb, c3[0] + rb, c3[1] + rb], 0, 180, fill=A(BLOCK, 0.85 * kh), outline=A(BLUE, kh), width=4)
        d.line([(c3[0] - rb - 40, c3[1]), (c3[0] + rb + 40, c3[1])], fill=A(BLUE, kh), width=5)
        dash(d, (c3[0], c3[1] - 240), (c3[0], c3[1] + rb), A(NAVY, kh), w=4)
        b = P(u_out(CHOT_R), rb, c3)
        d.line([c3, b], fill=A(BEAM, kh), width=7); chev(d, c3, b, A(BEAM, kh))
        d.arc([c3[0] - 150, c3[1] - 150, c3[0] + 150, c3[1] + 150], 90 - CHOT_R, 90, fill=A(DGREEN, kh), width=6)
        lab(d, (c3[0] + 215, c3[1] + 75), f"r = {CHOT_R}°", FS, DGREEN, alpha=kh)
        text(d, (c3[0] - 110, c3[1] - 150), "i = ?", 64, NAVY, alpha=kh)   # chi dau hoi canh phap tuyen, khong ve cung/nan goi so


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, si, da, b, e = sc["hook"], sc["do"], sc["sin"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + T0 + DT * k + READ, "tap") for k in range(5)]
    out += [(si["t0"] + 0.5, "tap"), (si["t0"] + SIN_Q, "tap"), (da["t0"] + 0.1, "ding"), (b["t0"] + BAY_X, "buzz"), (e["t0"] + END_Q + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-khucxa-02", header="KHTN 9 · THÍ NGHIỆM", footer="Khúc xạ ánh sáng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Khối nhựa bán trụ", draw=s_hook, tail=0.3, caps=[
   ("Laser chiếu vào tâm đĩa.", 2.94),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Xoay laser quanh tâm đĩa.", 2.94),
   ("Góc r đo từ pháp tuyến.", 2.94)]),
 dict(key="sin", title="sin là gì?", draw=s_sin, tail=0.3, caps=[
   ("Đĩa bán kính 1: sin là đoạn ngang.", 4.4),
   ("Hàng khác: bấm máy tính.", 2.94)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Tia khúc xạ sát nhau dần.", 3.4),
   ("Bấm máy sin i, sin r rồi chia.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("So hai cách chia.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 6.7)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
