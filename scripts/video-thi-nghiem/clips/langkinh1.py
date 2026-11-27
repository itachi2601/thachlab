# Clip: tn-l9-langkinh-01 - Duong di cua tia laser do qua lang kinh, doi goc toi (KHTN 9, lo 11, 19/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom D): chu than canh >= 55 (ra >= 48 px), K10, moi nhip >= 2,5 s,
#   Bay = hai lang kinh nho canh nhau (di thang ✗ / gay hai lan ✓), bo canh tinh cuoi (cau chot A-D o khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-langkinh-01.json (_kiem()):
#   tham_so A = 60 do, n = 1,5 ; so_lieu_mau (i, D): 30 47,1 | 40 38,5 | 45 37,4 | 50 37,2 | 60 38,9 | 70 42,9.
#   D = i + i2 - A "dung cho mo phong, khong day o lop 9" -> clip KHONG viet cong thuc D, chi "do bang thuoc do goc".
# Du doan (K10, khong nut A-D): tang dan i tu 30 toi 70 do, tia lo lech ve phia nao so voi huong tia toi?
#   -> dap an: ve day, ca 6 lan. KHONG hoi D giam roi tang (goc lech cuc tieu, ngoai KHTN 9).
#   Khong trung cau Tu kiem tra: C1 (mat thu hai: xa phap tuyen) -> clip KHONG noi tia lo gan/xa phap tuyen;
#   C4 (lang kinh dat nguoc -> len/xuong) ; C5 (thu tu mau) ; C6 (A = 20 do).
# THU NGHI (doi 27/11, ca cu "day quay sang phai" trung y Cau 4): tam kinh HAI MAT SONG SONG, tia lo di the nao?
#   -> song song voi tia toi, chi dich ngang. Buoc suy luan chua chieu: lang kinh lech vi hai mat ben NGHIENG nhau;
#   hai mat song song thi lan be o mat ra tra lai dung lan be o mat vao. Man chot khong ve tia trong tam kinh.
# Hinh: lang kinh deu dinh tren, day duoi; diem toi E co dinh tren mat trai, xoay but laser. Duong tia tinh bang Snell
#   va do D tu chinh hai huong ve -> assert khop kho (< 0,06 do), tia lo ra o mat phai, lech ve phia day.
# Bay = hien_tuong_hay_sai[1] (ve tia di thang). Chua noi duoc = ghi_chu kho (so lieu minh hoa, n gia dinh).
from engine import *

AXD, N = 60.0, 1.5
ROWS = [(30, "47,1"), (40, "38,5"), (45, "37,4"), (50, "37,2"), (60, "38,9"), (70, "42,9")]
GLASS = (191, 219, 254); BEAM = (220, 38, 38); DRED = (185, 28, 28); DGREEN = (10, 110, 50); DORG = (176, 64, 8)
DINK = (60, 66, 90)
FS, FM = 58, 56

P = (520.0, 300.0); SIDE = 440.0
BL = (P[0] - SIDE / 2, P[1] + SIDE * math.sqrt(3) / 2); BR = (P[0] + SIDE / 2, BL[1])
E = (lerp(BL[0], P[0], 0.55), lerp(BL[1], P[1], 0.55))
LOUT = 340


def u(deg): return (math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def path(i):
    """-> (huong tia toi (do, y xuong), diem ra X, huong tia lo (do), D do tu hai huong, vi tri tren mat phai)."""
    th_in = 30.0 - i                                          # phap tuyen vao trong mat trai: +30 do
    r1 = math.degrees(math.asin(math.sin(math.radians(i)) / N))
    th = 30.0 - r1; v = u(th)
    wx, wy = BR[0] - P[0], BR[1] - P[1]
    det = v[0] * (-wy) - v[1] * (-wx)
    s = ((P[0] - E[0]) * (-wy) - (P[1] - E[1]) * (-wx)) / det
    tt = (v[0] * (P[1] - E[1]) - v[1] * (P[0] - E[0])) / det   # vi tri tren mat phai (0 = dinh, 1 = goc day)
    X = (E[0] + s * v[0], E[1] + s * v[1])
    i2 = math.degrees(math.asin(N * math.sin(math.radians(AXD - r1))))
    th_out = -30.0 + i2                                       # phap tuyen ra ngoai mat phai: -30 do
    return th_in, X, th_out, th_out - th_in, tt


def num(x): return f"{x:.1f}".replace(".", ",")


def _kiem():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-langkinh-01.json")))
    tp = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert tp["A"]["gia_tri"] == AXD and tp["n"]["gia_tri"] == N
    hang = k["so_lieu_mau"]["hang"]; assert len(hang) == len(ROWS)
    for (i, ds), h in zip(ROWS, hang):
        th_in, X, th_out, D, tt = path(i)
        assert h[0] == i and num(h[1]) == ds, (i, ds, h)
        assert abs(D - h[1]) < 0.06, (i, D, h[1])              # goc lech do tu hinh ve khop kho
        assert D > 0                                          # quay xuoi chieu kim dong ho (y xuong) = lech ve day
        assert 0.05 < tt < 0.95, (i, tt)                      # tia ra o mat ben phai, khong cham day
    for i, _ in ROWS:                                         # but laser + tia lo trong khung (lề trái/phải)
        v = u(30.0 - i); b = (E[0] - 250 * v[0], E[1] - 250 * v[1]); assert b[0] > 20 and b[1] > 120, (i, b)
        th_in, X, th_out, D, tt = path(i); vo = u(th_out); assert X[0] + LOUT * vo[0] < 1070, i
_kiem()


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


# bien doi toa do: ve hinh goc (P, SIDE) thu nho/dich vao o khac (canh Bay)
def mk_tf(cx=None, top=None, k=1.0):
    if cx is None: return lambda p: p
    return lambda p: (cx + k * (p[0] - P[0]), top + k * (p[1] - P[1]))


def prism(d, tf=None, labs=True, ka=1.0):
    tf = tf or mk_tf()
    d.polygon([tf(P), tf(BR), tf(BL)], fill=A(GLASS, 0.85 * ka), outline=A(BLUE, ka))
    d.line([tf(P), tf(BR), tf(BL), tf(P)], fill=A(BLUE, ka), width=4)
    if labs:
        text(d, (P[0] + 175, P[1] + 15), "A = 60°", FM, BLUE, alpha=ka)
        text(d, ((BL[0] + BR[0]) / 2, BL[1] + 50), "đáy", FM, BLUE, alpha=ka)


def pen(d, i, tf=None, k=1.0):
    tf = tf or mk_tf()
    v = u(30.0 - i); a, b = (E[0] - 120 * v[0], E[1] - 120 * v[1]), (E[0] - 230 * v[0], E[1] - 230 * v[1])
    d.line([tf(a), tf(b)], fill=(55, 60, 75), width=int(30 * k)); pa = tf(a); dot(d, pa[0], pa[1], 9 * k, BEAM)
    return a


def normal_E(d):
    nrm = (-math.sqrt(3) / 2, -0.5)
    dash(d, (E[0] + 120 * nrm[0], E[1] + 120 * nrm[1]), (E[0] - 90 * nrm[0], E[1] - 90 * nrm[1]), A(NAVY, 0.7), w=3)


def ray(d, i, col=BEAM, ka=1.0, arc=True, lab="D", tf=None, k=1.0, straight=False, w=6):
    tf = tf or mk_tf()
    th_in, X, th_out, D, _ = path(i)
    a = pen(d, i, tf, k)
    if straight:                                              # cach ve SAI: tia di thang
        vi = u(th_in); Q = (E[0] + 520 * vi[0], E[1] + 520 * vi[1])
        d.line([tf(a), tf(Q)], fill=A(col, ka), width=w); chev(d, tf(E), tf(Q), A(col, ka))
        return Q
    vo = u(th_out); Z = (X[0] + LOUT * vo[0], X[1] + LOUT * vo[1])
    d.line([tf(a), tf(E)], fill=A(col, ka), width=w); chev(d, tf(a), tf(E), A(col, ka))
    d.line([tf(E), tf(X)], fill=A(col, ka), width=w - 1)
    d.line([tf(X), tf(Z)], fill=A(col, ka), width=w); chev(d, tf(X), tf(Z), A(col, ka))
    if arc:
        vi = u(th_in); dash(d, tf(X), tf((X[0] + LOUT * vi[0], X[1] + LOUT * vi[1])), A(NAVY, 0.75 * ka), w=3)
        Xt = tf(X); R = 150 * k
        d.arc([Xt[0] - R, Xt[1] - R, Xt[0] + R, Xt[1] + R], th_in, th_out, fill=A(ORANGE, ka), width=6)
        if lab:
            m = math.radians((th_in + th_out) / 2)
            text(d, (Xt[0] + 200 * k * math.cos(m), Xt[1] + 200 * k * math.sin(m)), lab, FS, DORG, alpha=ka)
    return X


def readout(d, i, ds, y=830):
    card(d, (80, y - 45, 500, y + 45), fill=WHITE, outline=NAVY, r=24, w=4)
    text(d, (290, y), f"i = {i}°", FS, NAVY)
    card(d, (560, y - 45, 1000, y + 45), fill=WHITE, outline=ORANGE, r=24, w=4)
    if ds: text(d, (780, y), f"D = {ds}°", FS, DORG)
    else: text(d, (780, y), "D = …", FS, DINK)


XS = (290, 700); RH = 68
def table(d, n, y0=910):
    card(d, (60, y0, 1020, y0 + 92 + 6 * RH + 18), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y0 + 48), "i", FS, NAVY); text(d, (XS[1], y0 + 48), "D (thước đo góc)", FM, DORG)
    d.line([(90, y0 + 90), (990, y0 + 90)], fill=LIGHT, width=3)
    for j in range(n):
        i, ds = ROWS[j]; yy = y0 + 128 + RH * j
        text(d, (XS[0], yy), f"{i}°", FS, INK); text(d, (XS[1], yy), f"{ds}°", FS, INK)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    prism(d); normal_E(d)                                     # chi tia toi: tia lo (= dap an) hien tu canh Tien hanh
    ka = appear(t, 0.5, 0.5); a = pen(d, 30)
    d.line([a, E], fill=A(BEAM, ka), width=6); chev(d, a, E, A(BEAM, ka))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FM)) + 56
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 96), fill=A(PURPLE, a), r=36)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", FM, WHITE, alpha=a)
    for j, s in enumerate(("Tăng góc tới từ 30° tới 70°.", "Tia ló lệch về phía nào", "so với hướng tia tới?")):
        text(d, (W / 2, y0 + 165 + j * 80), s, 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1          # thanh dem nguoc lien, day 70 px
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 440, 970, y0 + 510], radius=35, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 440, 110 + max(70, 860 * (1 - p)), y0 + 510], radius=35, fill=A((76, 29, 149), a))


# ---------------- canh 2: Tien hanh ----------------
T0, DT, ROT, READ, ROW = 0.6, 1.5, 0.5, 0.9, 0.9
def do_state(t):
    rows, ang, k_on = 0, ROWS[0][0], -1
    for k, (i, _) in enumerate(ROWS):
        tk = T0 + DT * k
        if t < tk: break
        if k > 0 and t < tk + ROT:
            ang = lerp(ROWS[k - 1][0], i, ease((t - tk) / ROT)); k_on = -1
        else:
            ang = i; k_on = k if t >= tk + READ else -1
        if t >= tk + ROW: rows = k + 1
    return ang, k_on, rows


def card_state(ang, k_on, rows):
    """(i hien, D hien hoac None). Laser con dung o goc hang vua ghi -> giu so cua hang do (khop bang)."""
    if k_on >= 0: return ROWS[k_on][0], ROWS[k_on][1]
    if rows > 0 and abs(ang - ROWS[rows - 1][0]) < 0.5: return ROWS[rows - 1][0], ROWS[rows - 1][1]
    return round(ang), None


def s_do(img, d, t, sc):
    ang, k_on, rows = do_state(t)
    prism(d); normal_E(d)
    ray(d, ang, arc=k_on >= 0, lab=None)
    readout(d, *card_state(ang, k_on, rows))
    table(d, rows)


def _kiem_dong_bo():
    """Moi 0,05 s: so D chi hien khi laser dung yen o goc cua hang do va khop goc ve; hang bang hien sau khi doc."""
    bad = []; t = 0.0
    while t < 11.0:
        ang, k_on, rows = do_state(t)
        if k_on >= 0:
            if abs(ang - ROWS[k_on][0]) > 1e-9: bad.append((round(t, 2), "D hien khi chua dung"))
            if num(path(ang)[3]) != ROWS[k_on][1]: bad.append((round(t, 2), "D lech hinh"))
        ci, cd = card_state(ang, k_on, rows)
        if cd is not None and (ci, cd) not in ROWS[:rows]: bad.append((round(t, 2), "the D co so ma bang chua ghi"))
        if rows > 0:
            done = max(k for k in range(6) if t >= T0 + DT * k)
            if rows > done + 1: bad.append((round(t, 2), "hang som"))
        t += 0.05
    if do_state(10.5)[2] != 6: bad.append("chua du 6 hang")
    return bad


# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=FM):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


DA_MARK = 3.2
def s_dapan(img, d, t, sc):
    prism(d); normal_E(d)
    for j, (i, _) in enumerate(ROWS):                       # ca 6 tia lo (mo) hien lan luot: cung nga ve phia day
        k = appear(t, 0.3 + 0.35 * j, 0.3)
        if k <= 0: continue
        th_in, X, th_out, D, _ = path(i); vo = u(th_out)
        d.line([X, (X[0] + LOUT * vo[0], X[1] + LOUT * vo[1])], fill=A(BEAM, 0.45 * k), width=4)
    X = ray(d, 50, lab=None, arc=False)
    km = appear(t, DA_MARK, 0.5)                           # hai cho gay: 1 o mat vao, 2 o mat ra
    if km > 0:
        for (x, y), s in ((E, "1"), (X, "2")):
            d.ellipse([x - 44 * km, y - 44 * km, x + 44 * km, y + 44 * km], fill=A(ORANGE, 0.55 * km), outline=A(ORANGE, km), width=7)
        text(d, (E[0] - 20, E[1] + 90), "1", FS, DORG, alpha=km)
        text(d, (X[0] + 30, X[1] + 75), "2", FS, DORG, alpha=km)
    pill(d, "ĐÁP ÁN: lệch về phía đáy", 900, appear(t, 0.15, 0.4))
    ka = appear(t, DA_MARK + 2.6, 0.6)                    # tia minh hoa i = 50: cung D giua tia toi keo dai va tia lo
    if ka > 0:
        th_in, X, th_out, D, _ = path(50); vi = u(th_in)
        dash(d, X, (X[0] + LOUT * vi[0], X[1] + LOUT * vi[1]), A(NAVY, 0.75 * ka), w=4)
        d.arc([X[0] - 150, X[1] - 150, X[0] + 150, X[1] + 150], th_in, lerp(th_in, th_out, ka), fill=A(ORANGE, ka), width=7)
        card(d, (140, 1000, 940, 1100), fill=A(WHITE, ka), outline=A(ORANGE, ka), r=26, w=4)
        text(d, (W / 2, 1050), "i = 50°  →  D = 37,2°", FS, DORG, alpha=ka)


# ---------------- canh 4: Bay + chua noi duoc ----------------
BAY_R, BAY_E = 3.4, 6.6
def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FM)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 338), fill=A(DRED, a1), r=38)
    text(d, (W / 2, 300), "BẪY", FM, WHITE, alpha=a1)
    text(d, (W / 2, 405), "“Tia đi thẳng qua lăng kính”", FS, INK, alpha=a1)
    if a1 > 0:                                              # hang tren: cach ve sai
        card(d, (40, 465, 1040, 885), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
        tf = mk_tf(330, 500, 0.75)
        prism(d, tf, labs=False, ka=a1)
        ray(d, 50, col=DRED, ka=a1 * appear(t, 0.5, 1.2), tf=tf, k=0.8, straight=True, w=7)
        text(d, (850, 640), "đi thẳng", FS, DRED, alpha=a1)
        text(d, (850, 750), "✗", 80, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:                                              # hang duoi: cach ve dung
        card(d, (40, 905, 1040, 1325), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        tf = mk_tf(330, 940, 0.75)
        prism(d, tf, labs=False, ka=a2)
        ray(d, 50, col=BEAM, ka=a2 * appear(t, BAY_R + 0.2, 1.2), tf=tf, k=0.8, arc=False, w=7)
        text(d, (850, 1080), "gãy hai lần", FS, DGREEN, alpha=a2)
        text(d, (850, 1190), "✓", 80, DGREEN, alpha=a2)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (40, 1350, 1040, 1565), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1405), "Chưa nói được:", FS, NAVY, alpha=k3)
        text(d, (W / 2, 1495), "số liệu minh hoạ, n giả định", FM, INK, alpha=k3)


# ---------------- canh 5: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 4.3
SL_Y0, SL_Y1, SL_X = 1080, 1260, 470           # tam kinh hai mat song song (nam ngang); diem toi tren mat tren
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Khúc xạ hai lần, lệch về đáy", FM, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FM)) + 56
    card(d, (W / 2 - pw / 2, 480, W / 2 + pw / 2, 556), fill=A(ORANGE, k1), r=38)
    text(d, (W / 2, 518), "THỬ NGHĨ", FM, WHITE, alpha=k1)
    text(d, (W / 2, 630), "Tấm kính hai mặt song song:", FS, INK, alpha=k1)
    text(d, (W / 2, 712), "tia ló đi thế nào?", FS, INK, alpha=k1)
    if k1 > 0:   # hinh: chi tia toi + phap tuyen; KHONG ve tia trong kinh, KHONG ve tia lo
        d.rectangle([150, SL_Y0, 930, SL_Y1], fill=A(GLASS, 0.85 * k1), outline=A(BLUE, k1), width=4)
        dash(d, (SL_X, SL_Y0 - 170), (SL_X, SL_Y1 + 110), A(NAVY, 0.7 * k1), w=3)
        v = u(45 + 0.0); a = (SL_X - 260 * v[0], SL_Y0 - 260 * v[1])
        d.line([a, (SL_X, SL_Y0)], fill=A(BEAM, k1), width=7); chev(d, a, (SL_X, SL_Y0), A(BEAM, k1))
        dot(d, a[0], a[1], 9, BEAM)
        kq = 0.55 + 0.45 * math.sin(2.4 * t) ** 2          # dau ? nhap nhay nhe o phia duoi tam kinh
        text(d, (680, SL_Y1 + 140), "?", 96, ORANGE, alpha=k1 * kq)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + T0 + DT * k + READ, "tap") for k in range(6)]
    out += [(da["t0"] + 0.1, "ding"), (da["t0"] + DA_MARK, "tap"), (b["t0"] + 0.3, "buzz"), (e["t0"] + END_Q + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-langkinh-01", header="KHTN 9 · THÍ NGHIỆM", footer="Lăng kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tia laser đỏ qua lăng kính", draw=s_hook, tail=0.3, caps=[
   ("Laser đỏ chiếu vào mặt bên.", 3.0),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Xoay bút laser, giữ điểm tới.", 4.6),
   ("Đo D bằng thước đo góc.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("So sáu tia ló với tia tới.", 3.4),
   ("Mỗi lần đều khúc xạ hai lần.", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("So hai cách vẽ.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 8.2)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
