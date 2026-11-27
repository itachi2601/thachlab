# Clip: tn-l9-doanmach-03 - Thao mot bong den trong mach noi tiep va song song (lo 11, 19/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom A): chu than canh >= 56 (ra >= 49 px), so ampe ke dat goc tren phai
#   moi mach, khong nut A-D (K10), thanh dem 90 px, khoi chu cach >= 2,5 s, tach Rut ra thanh canh rieng,
#   Bay = hai mach nho canh nhau (nghi ✗ / do ✓), bo o "Goi y" o man chot.
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-doanmach-03.json (_kiem_so() doi chieu ca mo_hinh):
#   U = 3 V ; R bong = 6 Ω ; so_lieu_mau: noi tiep 0,25 A -> thao mot bong 0 ; song song 0,5 A -> 0,5 A (so minh hoa).
#   Ampe ke mach chinh (ghi_chu): noi tiep 0,25 -> 0 ; song song 1,0 -> 0,5.
# Du doan (K10): ampe ke MACH CHINH, thao Đ1 o ca hai mach -> noi tiep 0 A ; song song 0,5 A.
#   Khac Cau 6 cua bai (2 bong 220 V song song, hoi do sang) va Cau 4 (ba bong noi tiep 0,3 A).
# Bay = hien_tuong_hay_sai[1] (bong dut van cho dong yeu qua). Khong dung [0] (= phuong an C Cau 6).
# Chua noi duoc: mo_hinh.gia_thiet[0] (coi dien tro bong khong doi).
# THU NGHI = cau_chot khung web (kho ghi_chu): ba bong nhu tren song song vao 3 V, thao mot bong -> ampe ke mach chinh
#   2 x 0,5 = 1,0 A. Man chot KHONG in 1,0 A cho ca nay.
from engine import *

U, RB = 3, 6
NT = (0.25, 0.0)
SS = (0.5, 0.5)
MAIN = {"nt": (0.25, 0.0), "ss": (1.0, 0.5)}
def vn(x): return ("%g" % x).replace(".", ",")


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-doanmach-03.json")))
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["U"]["gia_tri"] == U and tp["R_b"]["gia_tri"] == RB
    hang = {r[0]: tuple(r[1:]) for r in k["so_lieu_mau"]["hang"]}
    assert hang["nối tiếp"] == NT and hang["song song"] == SS
    assert abs(U / (2 * RB) - NT[0]) < 1e-9 and abs(U / RB - SS[0]) < 1e-9
    g = k["so_lieu_mau"]["ghi_chu"]
    assert "nối tiếp 0,25 A → tháo một bóng 0 A; song song 1,0 A → tháo một bóng 0,5 A" in g
    assert MAIN["nt"] == NT and MAIN["ss"] == (2 * SS[0], SS[1])
    assert "1,0 A" in g and abs(2 * SS[1] - 1.0) < 1e-9
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); WIRE = (40, 48, 80); GLOW = (250, 204, 21); DPURP = (76, 29, 149)
FS, FL = 56, 60

# ---------------- mach dien ----------------
XL, XR, R = 150, 930, 40
def rails(y0, kind):
    return y0 + 130, (y0 + 245 if kind == "ss" else None), y0 + 345
def bulbs(y0, kind):
    y1, y2, y3 = rails(y0, kind)
    return ({"Đ1": (400, y1), "Đ2": (660, y1)}, (800, y3)) if kind == "nt" else ({"Đ1": (540, y1), "Đ2": (540, y2)}, (800, y3))


def battery(d, x, y):
    d.line([(x - 15, y - 22), (x - 15, y + 22)], fill=WIRE, width=10)
    d.line([(x + 15, y - 40), (x + 15, y + 40)], fill=WIRE, width=4)
    text(d, (x + 50, y - 48), "+", FS, WIRE)


def bulb(d, x, y, b, al=1.0, broken=False):
    if b > 0 and al > 0:
        for k in range(5, 0, -1):
            rr = R + 8 * k * (0.6 + 0.8 * b)
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=A(GLOW, 0.13 * b * al))
    if al > 0.02:
        d.ellipse([x - R, y - R, x + R, y + R], fill=A(WHITE if b == 0 else (255, 250, 205), al), outline=A(WIRE, al), width=5)
        c = R * 0.7
        if broken:
            d.line([(x - c, y - c), (x - 8, y - 8)], fill=A(WIRE, al), width=4); d.line([(x + 10, y + 10), (x + c, y + c)], fill=A(WIRE, al), width=4)
        else: d.line([(x - c, y - c), (x + c, y + c)], fill=A(WIRE, al), width=4)
        d.line([(x - c, y + c), (x + c, y - c)], fill=A(WIRE, al), width=4)


def circuit(d, y0, kind, rm=0.0):
    """rm: 0 = Đ1 dang lap ; >0 = Đ1 dang/da thao (0..1 hoat canh nhac len)."""
    y1, y2, y3 = rails(y0, kind)
    bl, am = bulbs(y0, kind)
    opened = rm > 0
    on2 = not (opened and kind == "nt"); on1 = not opened
    card(d, (60, y0, 1020, y0 + 400), fill=WHITE, outline=LIGHT, w=3)
    text(d, (90, y0 + 48), ("Nối tiếp" if kind == "nt" else "Song song"), FS, NAVY, anchor="lm")
    gaps = {1: [], 2: []}
    for nm, (x, y) in bl.items(): gaps[1 if y == y1 else 2].append((x - R, x + R))
    for r, yy in ((1, y1), (2, y2)):
        if yy is None: continue
        xs = [XL] + [v for g in sorted(gaps[r]) for v in g] + [XR]
        for i in range(0, len(xs), 2): d.line([(xs[i], yy), (xs[i + 1], yy)], fill=WIRE, width=5)
    d.line([(XL, y1), (XL, y3)], fill=WIRE, width=5); d.line([(XR, y1), (XR, y3)], fill=WIRE, width=5)
    if y2 is not None:
        for x in (XL, XR): dot(d, x, y2, 9, WIRE)
    xb = 560
    d.line([(XL, y3), (300, y3)], fill=WIRE, width=5); d.line([(300, y3), (370, y3 - 4)], fill=WIRE, width=5)
    dot(d, 300, y3, 8, WIRE); dot(d, 372, y3, 8, WIRE); text(d, (336, y3 - 52), "K", FS, INK)
    d.line([(372, y3), (xb - 15, y3)], fill=WIRE, width=5)
    d.line([(xb + 15, y3), (am[0] - R, y3)], fill=WIRE, width=5); d.line([(am[0] + R, y3), (XR, y3)], fill=WIRE, width=5)
    battery(d, xb, y3)
    for nm, (x, y) in bl.items():
        lift, al = 0.0, 1.0
        if nm == "Đ1" and rm > 0: lift = 70 * ease(rm); al = 1 - ease(rm)
        dot(d, x - R, y, 7, WIRE); dot(d, x + R, y, 7, WIRE)
        lit = on1 if nm == "Đ1" else on2
        b = (0.45 if kind == "nt" else 1.0) if lit else 0.0
        bulb(d, x, y - lift, b, al)
        text(d, (x + R + 45, y - lift - 42), nm, FS, INK, alpha=al)
    x, y = am
    d.ellipse([x - R, y - R, x + R, y + R], fill=WHITE, outline=BLUE, width=5); text(d, (x, y + 2), "A", FS, BLUE)
    s = vn(MAIN[kind][1 if opened else 0]) + " A"
    card(d, (790, y0 + 14, 1000, y0 + 84), fill=NAVY, r=14)
    text(d, (895, y0 + 49), s, FS, (253, 224, 71))
    if on2:
        arrow(d, (XR + 26, y3 - 30), (XR + 26, (y2 if y2 else y1) + 40), ORANGE, w=7, head=20)
        arrow(d, (XL - 26, (y2 if y2 else y1) + 30), (XL - 26, y3 - 40), ORANGE, w=7, head=20)
    return opened


# ---------------- canh 1: Du doan ----------------
Y_NT, Y_SS = 268, 683
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, Y_NT, "nt"); circuit(d, Y_SS, "ss")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1105 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 525), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FS)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 102), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", FS, WHITE, alpha=a)
    text(d, (W / 2, y0 + 180), "Tháo Đ1 ở cả hai mạch.", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Ampe kế mạch chính chỉ?", FL, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 375, 970, y0 + 465], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 375, 110 + max(90, 860 * (1 - p)), y0 + 465], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh ----------------
T_NT, T_SS = 1.2, 4.3
def rm_at(t, t0): return 0.0 if t < t0 else max(1e-3, clamp((t - t0) / 0.7))


def meter_icon(d, x, y):
    d.ellipse([x - R, y - R, x + R, y + R], fill=WHITE, outline=BLUE, width=5); text(d, (x, y + 2), "A", FS, BLUE)


def table(d, y, n_nt, n_ss):
    card(d, (60, y, 1020, y + 350), fill=WHITE, outline=NAVY, w=4)
    xs = (225, 565, 870)
    meter_icon(d, xs[0], y + 125)
    text(d, (xs[1], y + 125), "trước", FS, MUTED); text(d, (xs[2], y + 125), "sau", FS, MUTED)
    d.line([(90, y + 168), (990, y + 168)], fill=LIGHT, width=4)
    for i, (nm, v, n) in enumerate((("Nối tiếp", MAIN["nt"], n_nt), ("Song song", MAIN["ss"], n_ss))):
        yy = y + 225 + i * 85
        text(d, (xs[0], yy), nm, FS, NAVY)
        text(d, (xs[1], yy), vn(v[0]), FL, INK)
        text(d, (xs[2], yy), vn(v[1]) if n else "…", FL, DGREEN if n else MUTED)


def do_state(t):
    r1, r2 = rm_at(t, T_NT), rm_at(t, T_SS)
    return r1, r2, t >= T_NT + 1.0, t >= T_SS + 1.0


def s_do(img, d, t, sc):
    r1, r2, n1, n2 = do_state(t)
    circuit(d, Y_NT, "nt", rm=r1); circuit(d, Y_SS, "ss", rm=r2)
    table(d, 1110, n1, n2)


def _kiem_dong_bo():
    bad = []; t = 0.0
    while t < 10.0:
        r1, r2, n1, n2 = do_state(t)
        if n1 and r1 == 0: bad.append((round(t, 2), "hang noi tiep truoc khi thao"))
        if n2 and r2 == 0: bad.append((round(t, 2), "hang song song truoc khi thao"))
        if (r1 > 0) != (t >= T_NT): bad.append((round(t, 2), "thao noi tiep lech moc"))
        t += 0.05
    return bad


# ---------------- canh 3: Dap an ----------------
def pill(d, s, y, a, color=NAVY, size=FS):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, y - 42, W / 2 + pw / 2, y + 42), fill=A(color, a), r=40)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    circuit(d, Y_NT, "nt", rm=1.0); circuit(d, Y_SS, "ss", rm=1.0)
    pill(d, "ĐÁP ÁN: 0 A và 0,5 A", 1150, 1.0)
    k1 = appear(t, M[1] - 0.1, 0.5)
    if k1 > 0:
        card(d, (60, 1235, 1020, 1400), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        text(d, (W / 2, 1318), "song song: 1,0 − 0,5 = 0,5", 64, DGREEN, alpha=k1)


# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 280, 1040, 580), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=5)
    text(d, (W / 2, 360), "Nối tiếp:", 64, DGREEN, alpha=k0)
    text(d, (W / 2, 480), "hở một chỗ, hở cả mạch", FL, DGREEN, alpha=k0)
    k1 = appear(t, M[1] - 0.1, 0.4)
    if k1 > 0:
        card(d, (40, 690, 1040, 990), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 770), "Song song:", 64, DGREEN, alpha=k1)
        text(d, (W / 2, 890), "nhánh khác vẫn sáng", FL, DGREEN, alpha=k1)
        # nhanh Đ1 da thao (net dut), nhanh Đ2 con dong: cham dong dien chay vong (khong dung hinh)
        xl, xr, ya, yb2, yc = 200, 880, 1080, 1220, 1400
        for x in range(xl, xr, 34): d.line([(x, ya), (x + 16, ya)], fill=A(GRAY, k1), width=4)
        d.line([(xl, ya), (xl, yc), (500, yc)], fill=A(WIRE, k1), width=5, joint="curve")
        d.line([(580, yc), (xr, yc), (xr, ya)], fill=A(WIRE, k1), width=5, joint="curve")
        d.line([(xl, yb2), (xr, yb2)], fill=A(WIRE, k1), width=5)
        d.line([(520, yc - 40), (520, yc + 40)], fill=A(WIRE, k1), width=5); d.line([(560, yc - 22), (560, yc + 22)], fill=A(WIRE, k1), width=12)
        bulb(d, 540, yb2, 1.0 * k1, k1)
        # vong: (+) phai -> len canh phai -> sang trai nhanh Đ2 -> xuong canh trai -> ve (-)
        pts = [(580, yc), (xr, yc), (xr, yb2), (xl, yb2), (xl, yc), (500, yc)]
        segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        Ltot = sum(abs(q[0] - p[0]) + abs(q[1] - p[1]) for p, q in segs)
        for n in range(14):
            u = ((t * 260 + n * Ltot / 14) % Ltot)
            for p0, q0 in segs:
                l = abs(q0[0] - p0[0]) + abs(q0[1] - p0[1])
                if u <= l:
                    f = u / l; x, y = p0[0] + (q0[0] - p0[0]) * f, p0[1] + (q0[1] - p0[1]) * f
                    if not (500 < x < 580 and y == yc) and not (abs(x - 540) < R + 4 and y == yb2):
                        dot(d, x, y, 18, A(ORANGE, k1))
                    break
                u -= l


# ---------------- canh 5: Bay (hai mach nho canh nhau) ; chua noi duoc ----------------
BAY_R, BAY_C = 3.4, 6.4
def mini(d, x0, glow, ka):
    """Mach noi tiep nho trong o rong 490: Đ1 dut day toc, Đ2 ; ampe ke duoi."""
    yt, yb, xl, xr = 720, 960, x0 + 50, x0 + 440
    d.line([(xl, yt), (xl, yb), (xr, yb), (xr, yt)], fill=A(WIRE, ka), width=5)
    d.line([(xl, yt), (xr, yt)], fill=A(WIRE, ka), width=5)
    bulb(d, x0 + 150, yt, 0.0, ka, broken=True)
    bulb(d, x0 + 340, yt, 0.45 if glow else 0.0, ka)
    text(d, (x0 + 150, yt - 75), "Đ1", FS, INK, alpha=ka); text(d, (x0 + 340, yt - 75), "Đ2", FS, INK, alpha=ka)
    d.ellipse([x0 + 205, yb - R, x0 + 285, yb + R], fill=A(WHITE, ka), outline=A(BLUE, ka), width=5)
    text(d, (x0 + 245, yb + 2), "A", FS, BLUE, alpha=ka)


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FS)) + 64
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 348), fill=A(DRED, a1), r=40)
    text(d, (W / 2, 308), "BẪY", FS, WHITE, alpha=a1)
    text(d, (W / 2, 410), "“Bóng đứt vẫn cho dòng”", FL, INK, alpha=a1)
    card(d, (40, 470, 530, 1260), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    text(d, (285, 540), "nghĩ", FL, DRED, alpha=a1)
    mini(d, 40, True, a1)
    text(d, (285, 1080), "Đ2 sáng yếu", FS, DRED, alpha=a1)
    text(d, (285, 1190), "✗ sai", FS, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (550, 470, 1040, 1260), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        text(d, (795, 540), "đo", FL, DGREEN, alpha=a2)
        mini(d, 550, False, a2)
        text(d, (795, 1080), "ampe kế 0 A", FS, DGREEN, alpha=a2)
        text(d, (795, 1190), "✓ mạch hở", FS, DGREEN, alpha=a2)
    k3 = appear(t, BAY_C, 0.45)
    if k3 > 0:
        card(d, (40, 1300, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1370), "Chưa nói được:", FL, NAVY, alpha=k3)
        text(d, (W / 2, 1475), "coi R bóng không đổi", FL, INK, alpha=k3)


# ---------------- canh 6: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 415), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 340), "Song song: nhánh độc lập", FS, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 450, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FS)) + 60
    card(d, (W / 2 - pw / 2, 478, W / 2 + pw / 2, 558), fill=A(ORANGE, k1), r=40)
    text(d, (W / 2, 518), "THỬ NGHĨ", FS, WHITE, alpha=k1)
    text(d, (W / 2, 650), "Ba bóng song song, 3 V.", FL, INK, alpha=k1)
    text(d, (W / 2, 735), "Tháo một bóng: ampe kế?", FL, INK, alpha=k1)
    # ba nhanh song song, bong tren cung da thao (net dut), ampe ke mach chinh
    xl, xr = 220, 860
    ys = (880, 1010, 1140)
    for j, y in enumerate(ys):
        if j == 0:
            for x in range(xl, xr, 34): d.line([(x, y), (x + 16, y)], fill=A(GRAY, k1), width=4)
            d.ellipse([540 - R, y - R - 40, 540 + R, y + R - 40], outline=A(GRAY, k1), width=4)
        else:
            d.line([(xl, y), (xr, y)], fill=A(WIRE, k1), width=5)
            bulb(d, 540, y, 1.0 * k1, k1)
    d.line([(xl, ys[0]), (xl, 1280), (500, 1280)], fill=A(WIRE, k1), width=5, joint="curve")
    d.line([(580, 1280), (xr, 1280), (xr, ys[0])], fill=A(WIRE, k1), width=5, joint="curve")
    d.line([(520, 1240), (520, 1320)], fill=A(WIRE, k1), width=5); d.line([(560, 1258), (560, 1302)], fill=A(WIRE, k1), width=12)
    d.ellipse([360 - R, 1280 - R, 360 + R, 1280 + R], fill=A(WHITE, k1), outline=A(BLUE, k1), width=5)
    text(d, (360, 1282), "A", FS, BLUE, alpha=k1)
    card(d, (300, 1400, 780, 1530), fill=A((220, 240, 225), k1), r=20)
    text(d, (540, 1465), "? A", 72, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + T_NT, "tap"), (do["t0"] + T_SS, "tap"), (da["t0"] + 0.15, "ding"),
            (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.3, "buzz"), (b["t0"] + BAY_R, "tap"),
            (e["t0"] + END_Q + 0.1, "open")]


CLIP = dict(id="tn-l9-doanmach-03", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Nối tiếp, song song · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tháo một bóng đèn", draw=s_hook, tail=0.3, caps=[
   ("Hai bóng giống nhau, nguồn 3 V.", 3.2),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Tháo Đ1 ở mạch nối tiếp.", 3.4),
   ("Tháo Đ1 ở mạch song song.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Nối tiếp: Đ2 tắt theo.", 2.9),
   ("Song song: Đ2 vẫn sáng.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Hở mạch thì sao?", 3.0),
   ("Mỗi nhánh nối thẳng nguồn.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Có dòng qua không?", 3.0),
   ("Mạch hở.", 3.0),
   ("Còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
