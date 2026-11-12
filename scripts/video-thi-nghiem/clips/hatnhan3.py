# Clip: tn-l12-hatnhan-03 - Thi nghiem tan xa hat alpha tren la vang cua Rutherford (11/11/2026)
# Dung de giang tren lop: 3 quan sat -> 3 ket luan ve nguyen tu -> mo hinh "banh pudding" (Thomson) bi bac bo.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-hatnhan-03.json (va bai l12-hat-nhan-mo-hinh-nguyen-tu):
#   gia_thuyet: Thomson 1904, dien duong phan bo deu ; bai: "ban hang van hat alpha", hat alpha mang +2e
#   quan_sat: phan lon di thang ; so it lech ; khoang 8 000 hat moi co 1 hat lech qua 90 do, vai hat bat nguoc
#   rut_ra: Thomson bi bac bo ; dien duong + gan het khoi luong o vung rat nho (hat nhan), con lai gan nhu trong rong ;
#           luc dien day ; electron nhe hon alpha hon 7 000 lan
#   mo_hinh: Thomson -> qua ca la chi tich luy co 1 do ; khong_chung_minh: chuyen dong cua electron, hat nhan gom hat gi
#   cau chot: N ti le Z^2 (mo_hinh.phuong_trinh) ; nhom Z = 13 (thi du trong bai), vang Z = 79 (tham_so mac_dinh)
# Hinh canh 3: quy dao tinh that bang tich phan luc Coulomb day cua hat nhan, co man chan boi vo electron
#   (sua 11/11 ban 2: KQ = 85 de quy dao lech cong tron kieu hyperbol, hat bat lai dung cach hat nhan ~44 px;
#   ve theo THOI GIAN mo phong nen hat cham dan khi toi gan hat nhan roi quay nguoc)
#   (ngoai ban kinh nguyen tu luc = 0). Kich thuoc hat nhan KHONG dung ti le (that: nho hon nguyen tu co 20 000 lan).
#   Hat bat lai dung truoc hat nhan roi bi day nguoc, khong cham hat nhan (hien_tuong_hay_sai thu 3).
# Canh: Du doan -> Tien hanh (dem chop theo goc) -> Dap an + 3 ket luan -> Thomson bi bac bo -> Bay + chua noi duoc -> Chot.
# Dai ~62 s (qua moc 50 s cua clip tu hoc) vi thay dung giang tren lop, dung hinh tung canh.
from engine import *

GOLD = (234, 179, 8); GOLDF = (255, 244, 204); PINK = (255, 221, 221); PINKO = (236, 140, 140)
TRK = (95, 110, 150)

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

def pill(d, cx, cy, s, fill, alpha=1.0, size=38):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - 32, cx + pw / 2, cy + 32), fill=A(fill, alpha), r=32)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def alpha_dot(d, x, y, r=17, alpha=1.0):
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(ORANGE, alpha), outline=A((154, 52, 18), alpha), width=3)

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

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.2, 0.5)
    thomson(d, 600, 590, 215, k)
    ax = 110 + 50 * ease((t - 0.4) / 1.4)
    alpha_dot(d, ax, 590, 20, k)
    arrow(d, (ax + 34, 590), (ax + 130, 590), A(NAVY, k), w=6, head=20)
    text(d, (160, 664), "hạt alpha", 46, NAVY, bold=False, alpha=k)
    text(d, (925, 590), "?", 150, PURPLE, alpha=appear(t, 1.2, 0.5))
    k2 = appear(t, 1.0, 0.5)
    d.line([(370, 842), (402, 842)], fill=A(PINKO, k2), width=6); d.line([(386, 826), (386, 858)], fill=A(PINKO, k2), width=6)
    text(d, (426, 842), "điện dương rải đều", 46, INK, bold=False, anchor="lm", alpha=k2)
    dot(d, 386, 906, 12, A(BLUE, k2)); text(d, (426, 906), "êlectron", 46, INK, bold=False, anchor="lm", alpha=k2)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a, 36)
    ctext(d, y0 + 240, "Bắn hàng vạn hạt alpha vào lá vàng mỏng: các hạt đi thế nào?", 48, INK, maxw=860, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 410, 940, y0 + 424], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 410, 140 + 800 * (1 - p), y0 + 424], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (nhin tu tren xuong) ----------------
CX, CY, RS = 560, 720, 380
def on_ring(th, r=RS):
    a = math.radians(th); return (CX + r * math.cos(a), CY - r * math.sin(a))

def flashes(sc):
    """[(thoi diem, goc, loai)]: loai 0 = thang, 1 = lech, 2 = lech qua 90 do. Giai doan cham chi co chop thang."""
    M = sc["M"]; R = random.Random(5); out = []
    t = 1.0
    while t < M[2]:
        out.append((t, R.uniform(-2.5, 2.5), 0)); t += 0.42
    tb = sc["T"] - 2.0
    n = 46
    for i in range(n):
        out.append((M[2] + (tb - M[2]) * i / n, R.gauss(0, 2.0), 0))
    for f, th in ((0.08, 14), (0.22, -20), (0.36, 31), (0.5, -9), (0.62, 48), (0.74, -38), (0.86, 70)):
        out.append((M[2] + (tb - M[2]) * f, th, 1))
    out.append((tb, 150, 2))
    return sorted(out), tb

def n_fired(t, sc):
    M = sc["M"]; _, tb = flashes(sc)
    if t < 1.0: return 0
    if t < M[2]: return int((t - 1.0) / 0.42) + 1
    n0 = int((M[2] - 1.0) / 0.42) + 1
    k = clamp((t - M[2]) / (tb - M[2]))
    return int(round(n0 * (8000 / n0) ** k)) if k < 1 else 8000

def fmt(n): return f"{n:,}".replace(",", " ")

def apparatus(d):
    d.ellipse([CX - RS, CY - RS, CX + RS, CY + RS], outline=TEAL, width=12)                      # man ZnS
    dashed(d, (CX, CY - 92), (CX, CY - RS + 10), GRAY, w=3)
    text(d, (CX, CY - RS - 40), "90°", 44, MUTED)
    card(d, (215, CY - 66, 335, CY + 66), fill=(120, 126, 142), outline=NAVY, r=14, w=4)          # hop chi
    d.rectangle([300, CY - 7, 337, CY + 7], fill=BG)
    dot(d, 262, CY, 15, ORANGE)
    text(d, (330, CY + 110), "nguồn alpha", 44, NAVY, bold=False)
    d.rectangle([CX - 7, CY - 82, CX + 7, CY + 82], fill=GOLD, outline=(161, 98, 7), width=2)       # la vang
    text(d, (CX, CY + 128), "lá vàng", 44, NAVY, bold=False)
    d.line([(905, 1062), (848, 1000)], fill=TEAL, width=3)
    text(d, (910, 1092), "màn ZnS", 44, TEAL)

def s_do(img, d, t, sc):
    M = sc["M"]; fl, tb = flashes(sc)
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
    card(d, (50, 1170, 1030, 1390), fill=WHITE, outline=LIGHT, w=3)
    text(d, (290, 1222), "Đã bắn", 44, MUTED, bold=False)
    text(d, (790, 1222), "Lệch quá 90°", 44, MUTED, bold=False)
    text(d, (290, 1312), ("≈ " if n >= 8000 else "") + fmt(n), 76, INK)
    text(d, (790, 1312), str(back_), 76, RED if back_ else INK)
    d.line([(540, 1200), (540, 1360)], fill=LIGHT, width=3)
    if M[2] - 0.05 < t < tb:
        pill(d, 880, 1440, "TUA NHANH", ORANGE, 1.0, 36)
    if back_:
        k = appear(t, tb + 0.2, 0.4); P = on_ring(150)
        text(d, (420, 455), "bật lại!", 44, RED, alpha=k)

# ---------------- canh 3: phong to la vang - quy dao tinh that ----------------
BOX = (50, 225, 1030, 935)
AR, KQ = 80, 85.0                                 # ban kinh nguyen tu (px), hang so luc: hat bat lai dung cach hat nhan ~44 px
NUC = [(x, y) for x in (400, 650) for y in (375, 580, 785)]

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

Y_STRAIGHT = (290, 465, 478, 491, 670, 683, 696, 870)          # ngoai vo nguyen tu: khong lech
Y_DEFL = (375 - 55, 785 + 55)                                   # lech ~35°, mot lan tan xa
Y_BACK = (580 + 16,)                                            # lech ~127° (chu U mo), dung cach hat nhan ~46 px
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

def atoms(d, alpha=1.0):
    card(d, BOX, fill=A(WHITE, alpha), outline=A(LIGHT, alpha), r=28, w=3)
    for nx, ny in NUC:
        d.ellipse([nx - AR, ny - AR, nx + AR, ny + AR], fill=A(GOLDF, alpha))
        dcircle(d, nx, ny, AR, A(GOLD, alpha), w=4)
    for nx, ny in NUC: dot(d, nx, ny, 7, A(RED, alpha))

ROWS = (("Phần lớn đi thẳng", ("Nguyên tử gần như rỗng",), TRK),
        ("Số ít bị lệch", ("Tâm điện dương, đẩy alpha", "bằng lực điện"), ORANGE),
        ("≈ 1/8 000 lệch quá 90°", ("Tâm rất nhỏ, gần hết khối lượng",), RED))
ROW_Y = (955, 1165, 1425); ROW_H = (190, 240, 190)

def s_kq(img, d, t, sc):
    M = sc["M"]
    atoms(d)
    st = (0.5, M[1] + 0.1, M[2] + 0.1); du = (1.8, 1.8, 2.6)
    cur = 2 if t >= st[2] else (1 if t >= st[1] else 0)
    for g, (col, w) in enumerate(((TRK, 4), (ORANGE, 7), (RED, 8))):
        k = clamp((t - st[g]) / du[g])
        a = 0.85 if g == cur or g > 0 else 0.4
        for j, tr in enumerate(TR[g]):
            kk = clamp((t - st[g] - 0.08 * j) / du[g]) if g == 0 else k
            draw_track(d, tr, kk, A(col, a), w)
    for nx, ny in NUC: dot(d, nx, ny, 7, RED)
    kn = appear(t, M[2] + 1.6, 0.4)                                   # goi ten hat nhan
    if kn > 0:
        d.line([(744, 572), (660, 580)], fill=A(RED, kn), width=3)
        text(d, (752, 566), "hạt nhân", 46, RED, anchor="lm", alpha=kn)
        text(d, (752, 616), "vẽ to hơn thật", 42, MUTED, bold=False, anchor="lm", alpha=kn)
    for j, (obs, con, col) in enumerate(ROWS):
        k = appear(t, st[j] + (1.0 if j == 0 else 1.2), 0.5)
        if k <= 0: continue
        y0, hh = ROW_Y[j], ROW_H[j]
        card(d, (50, y0, 1030, y0 + hh), fill=A(WHITE, k), outline=A(col, k), r=28, w=5)
        dot(d, 118, y0 + hh / 2, 38, A(col, k)); text(d, (118, y0 + hh / 2), str(j + 1), 46, WHITE, alpha=k)
        text(d, (185, y0 + 54), obs, 46, INK, bold=False, anchor="lm", alpha=k)
        kc = appear(t, st[j] + (1.6 if j == 0 else 1.8), 0.5)
        arrow(d, (188, y0 + 128), (236, y0 + 128), A(col, kc), w=5, head=16)
        for i, c in enumerate(con): text(d, (256, y0 + 126 + 56 * i), c, 44, INK, anchor="lm", alpha=kc)

# ---------------- canh 4: vi sao banh pudding bi bac bo ----------------
MINI = fly(596, nuc=[(400, 580)])

def s_thomson(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.2, 0.45)
    card(d, (50, 265, 1030, 800), fill=A(WHITE, k), outline=A(LIGHT, k), r=28, w=3)
    text(d, (90, 318), "Nếu Thomson đúng", 46, INK, anchor="lm", alpha=k)
    for i, x in enumerate((330, 540, 750)): thomson(d, x, 520, 108, k, seed=i + 1, ne=5)
    kk = clamp((t - 0.6) / 1.6)
    for j, y in enumerate((440, 480, 520, 560, 600)):
        x1 = lerp(80, 990, clamp(kk * 1.15 - 0.03 * j))
        d.line([(80, y), (x1, y)], fill=A(TRK, 0.9 * k), width=5)
        if x1 > 985: chevron(d, x1, y, 0, A(TRK, k), s=18, w=5)
        else: alpha_dot(d, x1, y, 11, k)
    text(d, (W / 2, 718), "mọi hạt lệch chỉ cỡ 1°", 48, INK, bold=False, alpha=appear(t, 1.6, 0.5))
    k2 = appear(t, M[1] - 0.2, 0.45)
    if k2 <= 0: return
    card(d, (50, 830, 1030, 1215), fill=A(WHITE, k2), outline=A(LIGHT, k2), r=28, w=3)
    text(d, (90, 883), "Thực tế", 46, INK, anchor="lm", alpha=k2)
    ox, oy = 130, 1040 - 580                                        # ve lai quy dao bat nguoc quanh mot hat nhan
    sel = [(x + ox - 70, y + oy, s) for (x, y), s in zip(MINI["pts"], MINI["ts"]) if math.hypot(x - 400, y - 580) < 150]
    pts = [(x, y) for x, y, _ in sel]; ts = [s for _, _, s in sel]
    kb = clamp((t - M[1] - 0.2) / 1.6)                              # theo thoi gian: cham dan, dung truoc hat nhan, quay ve
    seg, done = upto(pts, ts, lerp(ts[0], ts[-1], kb))
    if len(seg) > 1: d.line(seg, fill=A(RED, k2), width=7, joint="curve")
    if done: chevron(d, pts[-1][0], pts[-1][1], math.atan2(pts[-1][1] - pts[-6][1], pts[-1][0] - pts[-6][0]), A(RED, k2), s=22, w=7)
    else: alpha_dot(d, seg[-1][0], seg[-1][1], 12, k2)
    dot(d, 400 + ox - 70, 580 + oy, 8, A(RED, k2))
    text(d, (540, 1040), "có hạt lệch quá 90°", 44, RED, anchor="lm", alpha=k2)
    k3 = appear(t, M[1] + 1.7, 0.4)
    if k3 > 0:
        cross(d, 540, 520, 150 * back((t - M[1] - 1.7) / 0.4), A(RED, 0.9 * k3), w=18)
        card(d, (50, 1245, 1030, 1480), fill=A((254, 242, 242), k3), outline=A(RED, k3), r=28, w=6)
        ctext(d, 1362, "Mô hình Thomson bị bác bỏ", 56, RED, alpha=k3)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; k1 = appear(t, 0.3, 0.45)
    y0 = 265 + (1 - k1) * 30
    card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, k1), outline=A(RED, k1), w=6)       # hop co theo noi dung
    pill(d, W / 2, y0 + 58, "BẪY", RED, k1)
    q = "“Alpha lệch do va vào êlectron”"
    ks = clamp((t - 1.3) / 0.4); lw = tw(d, q, F(44)); yy = y0 + 160
    text(d, (W / 2, yy), q, 44, mix(INK, GRAY, ks), alpha=k1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * k1), width=5)
    ym = y0 + 320; p = clamp((t - 0.5) / 2.2)                       # alpha lon gap electron be: alpha van di thang
    xa = lerp(170, 900, p); xe = 540
    d.line([(120, ym), (xa, ym)], fill=A(ORANGE, 0.45 * k1), width=6)
    if xa > xe - 40:
        q2 = clamp((xa - (xe - 40)) / 330)
        ex, ey = xe + 240 * q2, ym - 110 * q2
        d.line([(xe, ym), (ex, ey)], fill=A(BLUE, 0.4 * k1), width=3)
    else: ex, ey = xe, ym
    dot(d, ex, ey, 7, A(BLUE, k1))
    alpha_dot(d, xa, ym, 36, k1)
    text(d, (170, ym + 82), "alpha", 46, ORANGE, alpha=k1); text(d, (xe, ym + 82), "êlectron", 46, BLUE, alpha=k1)
    ctext(d, y0 + 520, "Êlectron nhẹ hơn alpha hơn 7 000 lần", 46, RED, maxw=920, alpha=appear(t, 1.7, 0.5))
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y0 = 905 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 360), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được:", 48, NAVY, alpha=k2)
        ka = k2 * appear(t, M[1] + 0.3, 0.4)
        text(d, (90, y0 + 170), "•  Êlectron chuyển động thế nào", 46, INK, bold=False, anchor="lm", alpha=ka)
        text(d, (90, y0 + 260), "•  Hạt nhân gồm những hạt gì", 46, INK, bold=False, anchor="lm", alpha=ka)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
# Tu ve thay chot_hoi(): hop THU NGHI co theo cau hoi (khong de trong nua man hinh), goi y la hop rieng hien sau 3,2 s.
def s_end(img, d, t, sc):
    M = (0.4,); k0 = appear(t, 0.2, 0.5)
    card(d, (60, 300, 1020, 580), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 440, "Alpha bật lại: nguyên tử có hạt nhân", 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    y0 = 650 + (1 - k1) * 30
    card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, y0 + 64, "THỬ NGHĨ", ORANGE, k1, 38)
    ctext(d, y0 + 240, "Đổi lá vàng thành lá nhôm: số hạt lệch mạnh tăng hay giảm?", 50, INK, maxw=880,
          alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 3.2, 0.5)
    if kh <= 0: return
    y1 = 1110 + (1 - kh) * 30
    card(d, (110, y1, 970, y1 + 260), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
    ctext(d, y1 + 66, "Gợi ý", 44, ORANGE, alpha=kh)
    ctext(d, y1 + 170, "Số prôtôn: vàng 79 · nhôm 13", 48, INK, maxw=800, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, th, b, e = (sc[k] for k in ("hook", "do", "kq", "thomson", "bay", "end"))
    fl, tb = flashes(do)
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.3, "ding")]
    for ft, _, kind in fl:
        if kind == 1: out.append((do["t0"] + ft, "tick"))
        elif kind == 2: out.append((do["t0"] + ft, "tap"))
    out += [(kq["t0"] + kq["M"][0] + 0.1, "ding"), (th["t0"] + th["M"][1] + 1.7, "buzz"),
            (b["t0"] + 0.3, "buzz"), (e["t0"] + 0.5, "open")]
    return sorted(out)

SCENES = [
 dict(key="hook", title="Nguyên tử giống bánh pudding?", draw=s_hook, tail=0.6, caps=[
   ("Thomson: nguyên tử như bánh pudding.", 3.2),
   ("Dự đoán trước khi xem.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=1.5, caps=[
   ("Rutherford bắn alpha vào lá vàng.", 3.2),
   ("Mỗi chớp sáng: một hạt alpha.", 2.9),
   ("Đếm chớp ở mọi góc.", 4.2)]),
 dict(key="kq", title="Ba quan sát, ba kết luận", draw=s_kq, tail=1.2, caps=[
   ("Đáp án: đa số thẳng, số ít lệch.", 4.2),
   ("Đi sát tâm mới bị đẩy.", 4.2),
   ("Rất sát tâm: bị đẩy ngược lại.", 4.6)]),
 dict(key="thomson", title="Bánh pudding có giải thích được?", draw=s_thomson, tail=1.2, caps=[
   ("Điện dương loãng chỉ đẩy nhẹ.", 3.4),
   ("Không tạo nổi cú bật lại.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Êlectron quá nhẹ.", 3.6),
   ("Thí nghiệm chưa trả lời.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=8.2, caps=[]),    # khong phu de: hop THU NGHI tu noi
]
SC = {s["key"]: s for s in SCENES}

CLIP = dict(id="tn-l12-hatnhan-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Hạt nhân và mô hình nguyên tử · thachlab.id.vn",
            cues=_cues, scenes=SCENES)
