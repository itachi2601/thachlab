# Clip: tn-l12-hatnhan-03 - Thi nghiem tan xa hat alpha tren la vang cua Rutherford (11/11/2026; dung lai 21/11/2026
# theo KE-HOACH-CAI-TIEN-CLIP viec 4 lo 20: cong --do-chu, chu >= 55 px khi ve, <= 50 s, Du doan khong nut A-D (K10)).
# Quan niem sai can danh (de TN THPT 2026 II.2 y c): "hat alpha lech/bat nguoc la do va vao electron".
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-hatnhan-03.json:
#   rut_ra: electron nhe hon alpha hon 7 000 lan ; dien duong + gan het khoi luong o vung rat nho (hat nhan) ; luc dien day
#   quan_sat: phan lon di thang ; so it lech ; khoang 8 000 hat moi co 1 hat lech qua 90 do, vai hat bat nguoc
#   gia_thuyet: Thomson, dien duong rai deu -> bi bac bo ; khong_chung_minh: chuyen dong cua electron
# Du doan (KHAC cau mo bai cua bai hoc - cau do hoi "cac hat di the nao"): alpha va vao MOT electron, alpha di tiep the nao?
#   -> dap an: gan nhu khong lech (electron vang di). Canh dap an ve ngay sau hop Du doan.
# Cau THU NGHI (= cau_chot khung web): la nhom cung be day -> so hat bat nguoc nhieu hay it hon? -> it hon
#   (buoc suy luan chua chieu: dien tich hat nhan nho hon -> luc dien day yeu hon). Hinh: hai nguyen tu CUNG CO, cham hat
#   nhan nho + o phong to "79+"/"13+" (tham_so Z, Z_Al; cong B v1: hinh cu giong Thomson). Nhom va vang cung be day co so
#   hat nhan/the tich gan bang nhau (Au 0,098 ; Al 0,100 mol/cm3).
# Hinh canh kq: quy dao tinh that bang tich phan luc Coulomb day cua hat nhan, co man chan boi vo electron (ngoai ban kinh
#   nguyen tu luc = 0). Hat nhan ve phong to (that: nho hon nguyen tu co 20 000 lan). Hat bat lai dung truoc hat nhan.
from engine import *

GOLD = (234, 179, 8); GOLDF = (255, 244, 204); PINK = (255, 221, 221); PINKO = (236, 140, 140)
TRK = (95, 110, 150); DORANGE = (154, 52, 18); DRED = (185, 28, 28); EMPTY = (148, 140, 128)

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-hatnhan-03.json")))
    s = json.dumps(k, ensure_ascii=False)
    for frag in ("7 000 lần", "8 000 hạt", "90°"): assert frag in s, frag
    z = {p["ky_hieu"]: p for p in k["tham_so"]}; assert z["Z"]["mac_dinh"] == 79 and z["Z_Al"]["gia_tri"] == 13
_kiem_so()

def chevron(d, x, y, ang, color, s=18, w=5):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def dcircle(d, cx, cy, r, color, w=3, n=28):
    for i in range(n):
        a0 = 2 * math.pi * i / n; a1 = a0 + 2 * math.pi / n * 0.55
        d.line([(cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))], fill=color, width=w)

def dashed(d, p, q, color, w=3, seg=12, gap=10):
    L = math.dist(p, q); s = 0.0
    while s < L:
        e = min(L, s + seg)
        d.line([(lerp(p[0], q[0], s / L), lerp(p[1], q[1], s / L)), (lerp(p[0], q[0], e / L), lerp(p[1], q[1], e / L))], fill=color, width=w)
        s += seg + gap

def cross(d, cx, cy, r, color, w=14):
    d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=color, width=w)
    d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=color, width=w)

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def alpha_dot(d, x, y, r=17, alpha=1.0):
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(ORANGE, alpha), outline=A(DORANGE, alpha), width=3)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem LIEN cao 70 px (khong tach o, khong giong nut), ngan dan tu phai sang trai theo 10 nac
    (moi nac 0,5 s: hinh doi du ro de cong --do-chu khong bao dung yen)."""
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

# ---------------- nguyen tu Thomson (banh pudding) ----------------
def thomson(d, cx, cy, R, alpha=1.0, seed=3, ne=7):
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A(PINK, alpha), outline=A(PINKO, alpha), width=4)
    st = R / 3.2; n = int(R / st) + 1
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = cx + (i + 0.5 * (j % 2)) * st, cy + j * st * 0.9
            if math.hypot(x - cx, y - cy) < R - 16:
                a = A(PINKO, alpha)
                d.line([(x - 8, y), (x + 8, y)], fill=a, width=3); d.line([(x, y - 8), (x, y + 8)], fill=a, width=3)
    Rn = random.Random(seed)
    for k in range(ne):
        a = 2 * math.pi * k / ne + Rn.uniform(-0.3, 0.3); rr = R * Rn.uniform(0.3, 0.78)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a); re_ = max(8, R / 14)
        d.ellipse([x - re_, y - re_, x + re_, y + re_], fill=A(BLUE, alpha), outline=A(WHITE, alpha), width=2)

# ---------------- canh 1: Du doan - alpha va vao mot electron ----------------
YA = 470                                   # duong bay cua alpha trong canh hook/dapan
def s_hook(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.2, 0.5)
    card(d, (40, 205, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    ax = 170 + 80 * ease((t - 0.3) / 1.3)
    alpha_dot(d, ax, YA, 62, k)
    arrow(d, (ax + 80, YA), (ax + 250, YA), A(NAVY, k), w=7, head=24)
    text(d, (ax, YA + 115), "alpha", 58, DORANGE, alpha=k)
    dot(d, 780, YA, 13, A(BLUE, k))
    text(d, (780, YA + 115), "êlectron", 58, BLUE, alpha=k)
    text(d, (W / 2, 735), "Êlectron nhẹ hơn alpha", 60, INK, alpha=k)
    text(d, (W / 2, 820), "hơn 7 000 lần", 60, INK, alpha=k)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 940 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 66, "DỰ ĐOÁN", PURPLE, a)
    seg_bar(d, y0 + 140, t, M[1] + 0.2, sc["T"] - 0.6, PURPLE, a)
    text(d, (W / 2, y0 + 320), "Alpha va vào một êlectron.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 420), "Alpha đi tiếp thế nào?", 62, PURPLE, alpha=a)

# ---------------- canh 2: Dap an - alpha gan nhu khong lech ----------------
YD = 640; XE, YE = 600, YD - 16                   # electron hoi lech khoi duong bay de vang ra mot ben
D_T0, D_T1 = 0.3, 2.6
def d_alpha_x(t): return lerp(170, 930, clamp((t - D_T0) / (D_T1 - D_T0)))
T_HIT = D_T0 + (D_T1 - D_T0) * (XE - 75 - 170) / (930 - 170)
def s_dapan(img, d, t, sc):
    card(d, (40, 300, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    dashed(d, (90, YD), (1000, YD), GRAY, w=4)
    ax = d_alpha_x(t)
    d.line([(120, YD), (ax, YD)], fill=A(ORANGE, 0.6), width=8)
    q = max(0.0, t - T_HIT)                                          # electron vang ra phia truoc, chech len
    ang = math.radians(28); sp = 2.0 * (930 - 170) / (D_T1 - D_T0)
    ex = min(XE + sp * q * math.cos(ang), 990); ey = max(YE - sp * q * math.sin(ang), 350)
    if q > 0: d.line([(XE, YE), (ex, ey)], fill=A(BLUE, 0.5), width=4)
    dot(d, ex, ey, 13, BLUE)
    text(d, (min(ex, 900), ey - 60 if q > 0 else YE - 70), "êlectron", 58, BLUE)
    alpha_dot(d, ax, YD, 62)
    if ax > 920: chevron(d, ax + 70, YD, 0, NAVY, s=26, w=7)
    text(d, (ax, YD + 115), "alpha", 58, DORANGE)

# ---------------- canh 3: Tien hanh (nhin tu tren xuong) ----------------
CX, CY, RS = 560, 720, 380
FF = 2.4                                    # bat dau tua nhanh (giay trong canh)
def on_ring(th, r=RS):
    a = math.radians(th); return (CX + r * math.cos(a), CY - r * math.sin(a))

def t_back(sc): return sc["M"][1] - 0.2
def flashes(sc):
    """[(thoi diem, goc, loai)]: loai 0 = thang, 1 = lech, 2 = lech qua 90 do. Giai doan cham chi co chop thang."""
    R = random.Random(5); out = []; tb = t_back(sc)
    t = 1.0
    while t < FF:
        out.append((t, R.uniform(-2.5, 2.5), 0)); t += 0.42
    n = 40
    for i in range(n):
        out.append((FF + (tb - FF) * i / n, R.gauss(0, 2.0), 0))
    for f, th in ((0.08, 14), (0.22, -20), (0.36, 31), (0.5, -9), (0.62, 48), (0.74, -38), (0.86, 70)):
        out.append((FF + (tb - FF) * f, th, 1))
    out.append((tb, 150, 2))
    return sorted(out), tb

def n_fired(t, sc):
    tb = t_back(sc)
    if t < 1.0: return 0
    n0 = int((FF - 1.0) / 0.42) + 1
    if t < FF: return int((t - 1.0) / 0.42) + 1
    k = clamp((t - FF) / (tb - FF))
    return 8000 if k >= 1 else int(round(n0 + (7999 - n0) * k))

def fmt(n): return f"{n:,}".replace(",", " ")

def apparatus(d):
    d.ellipse([CX - RS, CY - RS, CX + RS, CY + RS], outline=TEAL, width=12)                      # man ZnS
    dashed(d, (CX, CY - 92), (CX, CY - RS + 10), GRAY, w=3)
    text(d, (CX + 70, CY - RS + 50), "90°", 56, INK)
    card(d, (215, CY - 66, 335, CY + 66), fill=(120, 126, 142), outline=NAVY, r=14, w=4)          # hop chi
    d.rectangle([300, CY - 7, 337, CY + 7], fill=BG)
    dot(d, 262, CY, 15, ORANGE)
    d.line([(250, 1088), (268, 792)], fill=NAVY, width=3)                                       # nhan ngoai man ZnS
    text(d, (230, 1120), "nguồn alpha", 56, NAVY)
    d.rectangle([CX - 7, CY - 82, CX + 7, CY + 82], fill=GOLD, outline=(161, 98, 7), width=2)       # la vang
    text(d, (CX + 120, CY + 130), "lá vàng", 56, (161, 98, 7))
    d.line([(905, 1062), (848, 1000)], fill=TEAL, width=3)
    text(d, (880, 1100), "màn ZnS", 56, TEAL)

def ff_icon(d, cx, cy, col):
    for dx in (-26, 18):
        d.polygon([(cx + dx - 22, cy - 28), (cx + dx + 22, cy), (cx + dx - 22, cy + 28)], fill=col)

def s_do(img, d, t, sc):
    fl, tb = flashes(sc)
    apparatus(d)
    if t > 0.7:                                                                                   # chum toi
        d.line([(337, CY), (CX - 8, CY)], fill=A(ORANGE, 0.35), width=6)
        for i in range(4):
            x = 337 + ((t * 260 + i * 56) % 215)
            dot(d, x, CY, 7, ORANGE)
        d.line([(CX + 8, CY), on_ring(0, RS - 8)], fill=A(ORANGE, 0.22), width=6)
        for i in range(5):
            x = CX + 8 + ((t * 260 + i * 74) % (RS - 20))
            dot(d, x, CY, 6, A(ORANGE, 0.8))
    for ft, th, kind in fl:
        if t < ft: continue
        P = on_ring(th); age = t - ft
        if kind == 0:
            dot(d, P[0], P[1], 6, A(ORANGE, 0.55))
        else:
            col = RED if kind == 2 else ORANGE
            hold = 1.0 if kind == 2 else clamp(1 - (age - 0.5) / 0.9, 0.3, 1)
            d.line([(CX, CY), P], fill=A(col, hold), width=7 if kind == 2 else 5)
            if kind == 2: chevron(d, *on_ring(th, RS * 0.62), math.atan2(P[1] - CY, P[0] - CX), A(RED, 1), s=26, w=7)
            dot(d, P[0], P[1], 11 if kind == 2 else 8, col)
        if age < 0.45:                                                                             # chop sang
            a = 1 - age / 0.45; r = 16 + 26 * (age / 0.45)
            for q in range(8):
                an = q * math.pi / 4
                d.line([(P[0] + 10 * math.cos(an), P[1] + 10 * math.sin(an)), (P[0] + r * math.cos(an), P[1] + r * math.sin(an))],
                       fill=A(YELLOW if kind < 2 else RED, a), width=5)
            dot(d, P[0], P[1], 12, A(YELLOW, a))
    n = n_fired(t, sc); back_ = 1 if t >= tb else 0
    card(d, (50, 1180, 1030, 1420), fill=WHITE, outline=LIGHT, w=3)
    text(d, (290, 1236), "Đã bắn", 56, INK)
    text(d, (790, 1236), "Lệch quá 90°", 56, INK)
    text(d, (290, 1336), fmt(n), 80, INK)
    text(d, (790, 1336), str(back_), 80, RED if back_ else INK)
    d.line([(540, 1210), (540, 1390)], fill=LIGHT, width=3)
    if FF - 0.05 < t < tb: ff_icon(d, 960, 1490, ORANGE)
    if back_: text(d, (395, 500), "bật lại!", 60, RED, alpha=appear(t, tb + 0.5, 0.4))

# ---------------- canh 4: phong to la vang - quy dao tinh that ----------------
BOX = (50, 225, 1030, 935)
AR, KQ = 130, 160.0                               # may nguyen tu TO (cong B v2-v3): hat bat lai dung cach hat nhan ~78 px, khe thay ro o 283 px
NUC = [(x, y) for x in (370, 700) for y in (400, 760)]

def fly(y0, nuc=NUC, x0=BOX[0] + 22, kq=KQ, R=AR):
    p = [float(x0), float(y0)]; v = [1.0, 0.0]; pts = [tuple(p)]; tt = 0.0; ts = [0.0]
    def acc(p):
        ax = ay = 0.0; rm = 1e9
        for nx, ny in nuc:
            dx, dy = p[0] - nx, p[1] - ny; r = math.hypot(dx, dy); rm = min(rm, r)
            if r < R:
                f = kq * (1 / (r * r) - r / R ** 3)              # hat nhan diem + may electron deu am (man chan)
                ax += f * dx / r; ay += f * dy / r
        return ax, ay, rm
    ax, ay, rm = acc(p)
    for _ in range(400000):
        dt = clamp(rm / 40, 0.005, 0.8)
        v[0] += 0.5 * dt * ax; v[1] += 0.5 * dt * ay
        p[0] += dt * v[0]; p[1] += dt * v[1]
        ax, ay, rm = acc(p)
        v[0] += 0.5 * dt * ax; v[1] += 0.5 * dt * ay; tt += dt
        if math.dist(p, pts[-1]) > 1.5: pts.append(tuple(p)); ts.append(tt)
        if not (BOX[0] + 20 < p[0] < BOX[2] - 20 and BOX[1] + 20 < p[1] < BOX[3] - 20): break
    pts.append(tuple(p)); ts.append(tt)
    return dict(pts=pts, ts=ts, L=sum(math.dist(a, b) for a, b in zip(pts, pts[1:])), ang=math.degrees(math.atan2(-v[1], v[0])),
                rmin=min(min(math.hypot(q[0] - nx, q[1] - ny) for nx, ny in nuc) for q in pts))

Y_STRAIGHT = (256, 580, 903)                                    # ngoai may nguyen tu: khong lech, moi khe mot vach
Y_DEFL = (400 - 90,)                                            # lech ~40°, mot lan tan xa (bo duong lech duoi: cat duong bat lai)
Y_BACK = (760 + 32,)                                            # lech ~119° (cong B v3 chap nhan 110-120°), quay dau cach hat nhan ~78 px
TR = [[fly(y) for y in ys] for ys in (Y_STRAIGHT, Y_DEFL, Y_BACK)]

def upto(pts, ts, s):
    """Doan quy dao tu dau toi thoi diem mo phong s (hat cham dan gan hat nhan thi nhich it)."""
    out = [pts[0]]
    for i in range(1, len(pts)):
        if s <= ts[i]:
            k = (s - ts[i - 1]) / (ts[i] - ts[i - 1]) if ts[i] > ts[i - 1] else 0
            out.append((lerp(pts[i - 1][0], pts[i][0], k), lerp(pts[i - 1][1], pts[i][1], k))); return out, False
        out.append(pts[i])
    return out, True

def draw_track(d, tr, k, color, w):
    if k <= 0: return
    pts, done = upto(tr["pts"], tr["ts"], tr["ts"][-1] * k)
    if len(pts) > 1: d.line(pts, fill=color, width=w, joint="curve")
    if done:
        a, b = tr["pts"][-6], tr["pts"][-1]
        chevron(d, b[0], b[1], math.atan2(b[1] - a[1], b[0] - a[0]), color, s=20, w=w)
    else:
        alpha_dot(d, pts[-1][0], pts[-1][1], 11)

def _bend_pts():
    """Diem tren quy dao dang uon (huong doi > 1,5° giua hai diem cach 6 buoc) - dinh quay va cung uon."""
    out = []
    for g in TR:
        for tr in g:
            p = tr["pts"]
            for i in range(6, len(p) - 6):
                a1 = math.atan2(p[i][1] - p[i - 6][1], p[i][0] - p[i - 6][0]); a2 = math.atan2(p[i + 6][1] - p[i][1], p[i + 6][0] - p[i][0])
                if abs((a2 - a1 + math.pi) % (2 * math.pi) - math.pi) > math.radians(1.5): out.append(p[i])
    return out

def _electrons():
    """4 electron/nguyen tu rai KHONG deu trong may (khong phai vong quy dao), cach moi diem moi quy dao >= 25 px."""
    Rn = random.Random(11); pts_all = [q for g in TR for tr in g for q in tr["pts"]]; out = []
    bend = _bend_pts()
    for nx, ny in NUC:
        mine = []; tries = 0
        while len(mine) < 4:
            tries += 1; assert tries < 5000, (nx, ny)
            a = Rn.uniform(0, 2 * math.pi); r = AR * Rn.uniform(0.35, 0.85)
            e = (nx + r * math.cos(a), ny + r * math.sin(a))
            if min(math.dist(e, q) for q in pts_all) < 25 + 6: continue
            if bend and min(math.dist(e, q) for q in bend) < 90 + 6: continue
            if any(math.dist(e, m) < 60 for m in mine): continue
            if 690 < e[0] < 970 and 345 < e[1] < 485: continue                     # cho nhan "hat nhan"
            mine.append(e)
        out += mine
    return out
ELEC = _electrons()
assert all(min(math.dist(e, q) for q in _bend_pts()) >= 90 for e in ELEC)
assert all(min(math.dist(e, q) for g in TR for tr in g for q in tr["pts"]) >= 25 for e in ELEC)

def atoms(d):
    card(d, BOX, fill=WHITE, outline=LIGHT, r=28, w=3)
    for nx, ny in NUC: d.ellipse([nx - AR, ny - AR, nx + AR, ny + AR], fill=GOLDF)
    for ex, ey in ELEC: dot(d, ex, ey, 6, A(BLUE, 0.7))
    for nx, ny in NUC: dot(d, nx, ny, 7, RED)

def s_kq(img, d, t, sc):
    M = sc["M"]
    atoms(d)
    st = (0.5, M[1] + 0.1, M[2] + 0.1); du = (1.8, 1.8, 2.6)
    for g, (col, w) in enumerate(((TRK, 4), (ORANGE, 7), (RED, 8))):
        k = clamp((t - st[g]) / du[g])
        for j, tr in enumerate(TR[g]):
            kk = clamp((t - st[g] - 0.08 * j) / du[g]) if g == 0 else k
            draw_track(d, tr, kk, A(col, 0.85), w)
    for nx, ny in NUC: dot(d, nx, ny, 7, RED)
    kn = appear(t, M[1] + 0.6, 0.4)                                   # goi ten hat nhan
    if kn > 0:
        text(d, (722, 385), "hạt nhân", 58, RED, anchor="lm", alpha=kn)
        text(d, (722, 449), "phóng to", 56, INK, bold=False, anchor="lm", alpha=kn)
    k1 = appear(t, M[0] + 1.0, 0.45)
    if k1 > 0:
        card(d, (50, 975, 1030, 1135), fill=A(WHITE, k1), outline=A(TRK, k1), r=28, w=5)
        text(d, (W / 2, 1055), "Nguyên tử gần như rỗng", 60, INK, alpha=k1)
    k2 = appear(t, M[2] + 1.0, 0.45)
    if k2 > 0:
        card(d, (50, 1170, 1030, 1330), fill=A((254, 242, 242), k2), outline=A(RED, k2), r=28, w=5)
        text(d, (W / 2, 1250), "Hạt nhân: nhỏ, nặng, điện dương", 58, DRED, alpha=k2)

# ---------------- canh 5: Thomson bi bac bo + chua noi duoc ----------------
def s_ketluan(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.2, 0.45)
    card(d, (50, 225, 1030, 820), fill=A(WHITE, k), outline=A(LIGHT, k), r=28, w=3)
    text(d, (W / 2, 300), "Thomson", 60, INK, alpha=k)
    for i, x in enumerate((330, 540, 750)): thomson(d, x, 540, 108, k, seed=i + 1, ne=5)
    kk = clamp((t - 0.5) / 1.5)
    for j, y in enumerate((460, 500, 540, 580, 620)):
        x1 = lerp(80, 990, clamp(kk * 1.15 - 0.03 * j))
        d.line([(80, y), (x1, y)], fill=A(TRK, 0.9 * k), width=5)
        if x1 > 985: chevron(d, x1, y, 0, A(TRK, k), s=18, w=5)
        else: alpha_dot(d, x1, y, 11, k)
    k3 = appear(t, 2.0, 0.4)
    if k3 > 0:
        cross(d, 540, 540, 150 * back((t - 2.0) / 0.4), A(RED, 0.9 * k3), w=18)
        card(d, (50, 850, 1030, 1020), fill=A((254, 242, 242), k3), outline=A(RED, k3), r=28, w=6)
        text(d, (W / 2, 935), "Thomson bị bác bỏ", 64, RED, alpha=k3)
    k2 = appear(t, M[1] + 0.2, 0.45)
    if k2 > 0:
        y0 = 1060 + (1 - k2) * 30
        card(d, (50, y0, 1030, y0 + 300), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 85), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 200), "Êlectron chuyển động thế nào?", 58, INK, alpha=k2)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def zoom_atom(d, cx, cy, lab, a):
    """Nguyen tu (may nhat, cung co) voi cham hat nhan nho o tam; o phong to ben duoi ghi dien tich hat nhan."""
    d.ellipse([cx - 140, cy - 140, cx + 140, cy + 140], fill=A(GOLDF, a))
    dot(d, cx, cy, 7, A(RED, a))
    zy = cy + 290
    d.line([(cx, cy + 8), (cx - 72, zy - 22)], fill=A(GRAY, a), width=3); d.line([(cx, cy + 8), (cx + 72, zy - 22)], fill=A(GRAY, a), width=3)
    d.ellipse([cx - 78, zy - 78, cx + 78, zy + 78], fill=A(WHITE, a), outline=A(RED, a), width=5)
    text(d, (cx, zy), lab, 60, RED, alpha=a)

def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1500), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    seg_bar(d, 360, t, 0.8, sc["T"] - 0.2, ORANGE, k1)
    zoom_atom(d, 300, 610, "79+", k1); zoom_atom(d, 780, 610, "13+", k1)
    text(d, (300, 1010), "vàng", 62, INK, alpha=k1); text(d, (780, 1010), "nhôm", 62, INK, alpha=k1)
    text(d, (W / 2, 1150), "Lá nhôm cùng bề dày:", 62, DORANGE, alpha=k1)
    text(d, (W / 2, 1245), "bật ngược nhiều hay ít hơn?", 62, DORANGE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, da, do, kq, kl, e = (sc[k] for k in ("hook", "dapan", "do", "kq", "ketluan", "end"))
    fl, tb = flashes(do)
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (da["t0"] + T_HIT, "tap")]
    out += [(do["t0"] + FF, "tick")]
    for ft, _, kind in fl:
        if kind == 1: out.append((do["t0"] + ft, "tick"))
        elif kind == 2: out.append((do["t0"] + ft, "tap"))
    out += [(kq["t0"] + kq["M"][2] + 0.1, "tap"), (kl["t0"] + 2.0, "buzz"), (e["t0"] + 0.15, "open")]
    return sorted(out)

SCENES = [
 dict(key="hook", title="Hạt alpha gặp êlectron", draw=s_hook, tail=0.3, caps=[
   ("Lá vàng chứa rất nhiều êlectron.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=1.2, caps=[
   ("Đáp án: alpha gần như không lệch.", 3.8)]),
 dict(key="do", title="Rutherford bắn alpha vào lá vàng", draw=s_do, tail=0.4, caps=[
   ("Mỗi chớp sáng: một hạt alpha.", 4.4),
   ("Có hạt bật ngược lại!", 3.2)]),
 dict(key="kq", title="Vì sao có hạt bật lại?", draw=s_kq, tail=1.0, caps=[
   ("Xa hạt nhân: đi thẳng.", 3.0),
   ("Gần hơn: lực điện đẩy lệch.", 3.4),
   ("Rất sát: bị đẩy ngược.", 3.0)]),
 dict(key="ketluan", title="Kết luận", draw=s_ketluan, tail=1.2, caps=[
   ("Điện dương loãng: chỉ đẩy nhẹ.", 3.4),
   ("Thí nghiệm này chưa trả lời.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=2.8, caps=[
   ("Hạt nhân đẩy ngược, không phải êlectron.", 3.8)]),
]
SC = {s["key"]: s for s in SCENES}

CLIP = dict(id="tn-l12-hatnhan-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Hạt nhân và mô hình nguyên tử · thachlab.id.vn",
            cues=_cues, scenes=SCENES)
