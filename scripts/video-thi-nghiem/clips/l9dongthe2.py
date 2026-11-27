# Clip: tn-l9-dongthe-02 - Xe lan tren mang ngang qua cong quang: do dong nang Wd = 1/2 m v^2 (KHTN 9, 5/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4 L9, nhom B): chu than canh >= 55 (ra >= 48 px), moi nhip >= 2,5 s,
#   du doan khong nut A-D (K10), thanh dem lien, bo canh rut ra rieng (gop vao dap an), canh tinh cuoi tu ve.
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-dongthe-02.json (_kiem_so()):
#   tham_so: d = 0,02 m (tam chan 2,0 cm) ; m 0,2-0,6 kg (buoc 0,2) ; dong ho do chia 0,0001 s
#   so_lieu_mau (m kg, dt s, v m/s, Wd J): 0,2 0,0198 1,01 0,102 ; 0,2 0,0101 1,98 0,392 ; 0,4 0,0202 0,99 0,196 ;
#                                          0,4 0,0099 2,02 0,816
# Du doan (KHONG trung Cau 4 / Tra bai 5 cua bai = "v gap doi -> Wd gap may"): xe 0,20 kg, ve Wd theo v,
#   noi goc O voi 2 lan day -> duong gi?  Dap an: duong cong, doc dan len (goi_y_mo_phong.diem_nhan: parabol).
# Bay = hien_tuong_hay_sai[1] "tinh v = dt/d": dt : d = 0,99 ; 0,51 (day manh ma nho hon) canh d : dt = 1,01 ; 1,98.
# Chua noi duoc = ghi_chu kho "so lieu minh hoa, chua phai so do that".
# THU NGHI (cau_chot khung web, tu suy trong dai tham_so, "theo mo hinh"): xe 0,60 kg, dt = 0,010 s
#   -> v = 0,020 : 0,010 = 2,0 m/s ; Wd = 1/2 . 0,6 . 2,0^2 = 1,2 J (KHONG hien tren man; truc Wd chi toi 0,8).
from engine import *

ROWS = [(0.20, 0.0198, 1.01, 0.102), (0.20, 0.0101, 1.98, 0.392), (0.40, 0.0202, 0.99, 0.196), (0.40, 0.0099, 2.02, 0.816)]
BAY = [(0.99, "0,99"), (0.51, "0,51")]        # dt : d (sai) cho hai lan day xe 0,20 kg
CHOT_M, CHOT_DT = 0.60, 0.010
def fm(x, n=2): return f"{x:.{n}f}".replace(".", ",")


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-dongthe-02.json")))
    assert [tuple(h) for h in k["so_lieu_mau"]["hang"]] == ROWS
    for m, dt, v, w in ROWS:
        assert round(0.02 / dt, 2) == v and abs(0.5 * m * v * v - w) < 0.0006, (m, dt, v, w)
    assert abs(ROWS[0][1] / 0.02 - BAY[0][0]) < 0.005 and abs(ROWS[1][1] / 0.02 - BAY[1][0]) < 0.006
    tm = k["tham_so"][0]; assert tm["min"] <= CHOT_M <= tm["max"] and k["tham_so"][1]["gia_tri"] == 0.02
    v = 0.02 / CHOT_DT; assert abs(v - 2.0) < 1e-9 and abs(0.5 * CHOT_M * v * v - 1.2) < 1e-9
_kiem_so()

CART = (59, 130, 246); CART_D = (30, 64, 175); MASS = (120, 113, 108); FLAG = (24, 30, 56)
C02, C04 = BLUE, ORANGE
DGREEN = (10, 110, 50); DRED = (185, 28, 28); DINK = (60, 66, 90); DPURP = (76, 29, 149)
FS = 58

# ---------------- mang ngang + xe + cong quang + dong ho ----------------
TY = 600; GATE = 560; X0, XSTOP = 190, 880; FW = 24


def cart(d, x, heavy, alpha=1.0, ty=TY, n_mass=1):
    c = lambda col: A(col, alpha)
    d.rounded_rectangle([x - 90, ty - 92, x + 90, ty - 30], radius=12, fill=c(CART), outline=c(CART_D), width=4)
    for wx in (x - 55, x + 55):
        d.ellipse([wx - 20, ty - 40, wx + 20, ty], fill=c(NAVY)); d.ellipse([wx - 7, ty - 27, wx + 7, ty - 13], fill=c(GRAY))
    d.rectangle([x - FW / 2, ty - 200, x + FW / 2, ty - 92], fill=c(FLAG))
    if heavy > 0:
        k = alpha * heavy
        for lvl in range(n_mass):
            yb = ty - 94 - 56 * lvl
            d.rounded_rectangle([x - 78, yb - 52, x - 20, yb], radius=8, fill=A(MASS, k), outline=A(NAVY, k), width=3)
            d.rounded_rectangle([x + 20, yb - 52, x + 78, yb], radius=8, fill=A(MASS, k), outline=A(NAVY, k), width=3)


def track(d, ty=TY, gate=GATE, blocked=False, a=1.0):
    d.rectangle([70, ty, 1010, ty + 26], fill=A((90, 98, 122), a))
    for lx in (120, 960): d.rectangle([lx - 10, ty + 26, lx + 10, ty + 70], fill=A(GRAY, a))
    d.rectangle([996, ty - 70, 1012, ty], fill=A(NAVY, a))
    d.rectangle([gate - 9, ty - 165, gate + 9, ty + 26], fill=A(GRAY, a))
    d.rounded_rectangle([gate - 34, ty - 190, gate + 34, ty - 130], radius=10, fill=A(NAVY, a))
    dot(d, gate, ty - 160, 11, A((70, 70, 80) if blocked else RED, a))


def rig(d, x, heavy, blocked, m_txt, dt_txt, ca=1.0, lbl=True):
    track(d, blocked=blocked)
    d.line([(GATE + 9, TY + 42), (760, TY + 42), (760, 700)], fill=GRAY, width=5)
    cart(d, x, heavy, ca)
    if lbl: text(d, (760, 330), "chắn rộng 2,0 cm", FS, INK)
    card(d, (60, 700, 470, 810), fill=WHITE, outline=NAVY, r=24, w=4)
    text(d, (265, 755), "m = " + m_txt + " kg", FS, INK)
    card(d, (500, 700, 1020, 810), fill=NAVY, r=24)
    text(d, (760, 755), "Δt = " + dt_txt + " s", FS, (110, 231, 160))


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, X0, 0, False, "0,20", "0,0000")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 56
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 96), fill=A(PURPLE, a), r=36)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    for j, s in enumerate(("Xe 0,20 kg: vẽ Wđ theo v.", "Nối gốc O với 2 lần đẩy,", "được đường gì?")):
        text(d, (W / 2, y0 + 165 + j * 80), s, 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 390, 970, y0 + 490], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 390, 110 + max(90, 860 * (1 - p)), y0 + 490], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh, 4 lan day ----------------
REL = [0.5, 2.8, 5.4, 7.6]
SPD = [410, 820, 410, 820]
def cart_x(tau, i): return min(XSTOP, X0 + SPD[i] * max(0.0, tau))
def pass_t(i): return REL[i] + (GATE + FW / 2 - X0) / SPD[i]
HEAVY_AT = REL[2] - 0.4


def do_state(t):
    i = max([j for j in range(4) if t >= REL[j] - 0.4], default=0)
    x = cart_x(t - REL[i], i)
    blocked = abs(x - GATE) < FW / 2
    if t >= pass_t(i): dt = fm(ROWS[i][1], 4)
    elif t >= REL[i]: dt = "0,0000"
    else: dt = fm(ROWS[i - 1][1], 4) if i > 0 else "0,0000"
    ca = clamp((t - (REL[i] - 0.4)) / 0.25) if i > 0 else 1.0
    heavy = appear(t, HEAVY_AT, 0.2)
    m_txt = "0,40" if t >= HEAVY_AT + 0.1 else "0,20"
    rows = sum(1 for j in range(4) if t >= pass_t(j) + 0.3)
    return x, blocked, dt, ca, heavy, m_txt, rows


TX = (160, 400, 660, 900)
def table(d, n, y0=860):
    card(d, (40, y0, 1040, y0 + 100 + 4 * 84 + 20), fill=WHITE, outline=LIGHT, w=3)
    for x, s in zip(TX, ("m", "Δt", "v", "Wđ")): text(d, (x, y0 + 50), s, 60, NAVY)
    d.line([(70, y0 + 98), (1010, y0 + 98)], fill=LIGHT, width=3)
    for j in range(n):
        m, dt, v, w = ROWS[j]; yy = y0 + 145 + 84 * j; col = C02 if m < 0.3 else C04
        for x, s in zip(TX, (fm(m), fm(dt, 4), fm(v), fm(w, 3))): text(d, (x, yy), s, FS, col)
    text(d, (W / 2, y0 + 520), "v = d : Δt  ·  Wđ = ½·m·v²", FS, DINK)


def s_do(img, d, t, sc):
    x, blocked, dt, ca, heavy, m_txt, rows = do_state(t)
    rig(d, x, heavy, blocked, m_txt, dt, ca=ca, lbl=False)
    table(d, rows)


# ---------------- canh 3: Dap an (do thi Wd theo v) ----------------
GX0, GY0, PXV, PYJ = 200, 1380, 340, 900
def gp(v, w): return GX0 + v * PXV, GY0 - w * PYJ


def axes(d):
    d.line([(GX0, GY0), (GX0 + 2.4 * PXV, GY0)], fill=NAVY, width=5)
    d.line([(GX0, GY0), (GX0, GY0 - 0.9 * PYJ)], fill=NAVY, width=5)
    for v in (1, 2):
        x, _ = gp(v, 0); d.line([(x, GY0), (x, GY0 + 14)], fill=NAVY, width=4)
        text(d, (x, GY0 + 50), str(v), FS, DINK)
    for w in (0.4, 0.8):
        _, y = gp(0, w); d.line([(GX0 - 14, y), (GX0, y)], fill=NAVY, width=4)
        d.line([(GX0 + 4, y), (GX0 + 2.35 * PXV, y)], fill=(236, 230, 220), width=2)
        text(d, (GX0 - 24, y), fm(w, 1), FS, DINK, anchor="rm")
    text(d, (GX0 - 30, GY0 + 50), "O", FS, DINK)
    text(d, (GX0 + 2.4 * PXV, GY0 + 52), "v", 60, INK)
    text(d, (GX0 + 30, GY0 - 0.9 * PYJ), "Wđ", 60, INK, anchor="lm")


def curve(d, m, col, k, vmax):
    n = 40; pts = [gp(vmax * k * j / n, 0.5 * m * (vmax * k * j / n) ** 2) for j in range(n + 1)]
    if k > 0: d.line(pts, fill=col, width=7, joint="curve")


def s_dapan(img, d, t, sc):
    M = sc["M"]
    a = appear(t, 0.15, 0.4)
    pw = tw(d, "ĐÁP ÁN: cong, dốc dần lên", F(56)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 342), fill=A(NAVY, a), r=38)
    text(d, (W / 2, 302), "ĐÁP ÁN: cong, dốc dần lên", 56, WHITE, alpha=a)
    axes(d)
    curve(d, 0.20, C02, ease((t - 0.6) / 1.4), 2.1)
    for j, (v, w) in enumerate(((0, 0), (ROWS[0][2], ROWS[0][3]), (ROWS[1][2], ROWS[1][3]))):
        k = appear(t, 0.6 + 0.6 * j, 0.3)
        if k > 0: x, y = gp(v, w); dot(d, x, y, 17, A(C02, k), outline=A(WHITE, k))
    text(d, (GX0 + 170, 650), "xe 0,20 kg", FS, C02, anchor="lm", alpha=a)
    k2 = appear(t, M[1], 0.4)
    if k2 > 0:
        curve(d, 0.40, C04, ease((t - M[1]) / 1.2), 2.08)
        for j in (2, 3):
            x, y = gp(ROWS[j][2], ROWS[j][3]); kk = appear(t, M[1] + 0.3 * (j - 1), 0.3)
            dot(d, x, y, 17, A(C04, kk), outline=A(WHITE, kk))
        text(d, (GX0 + 170, 570), "xe 0,40 kg", FS, C04, anchor="lm", alpha=k2)
    k3 = appear(t, M[1] + 2.6, 0.45)
    if k3 > 0:
        card(d, (50, 1490, 1030, 1595), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), r=26, w=4)
        text(d, (W / 2, 1542), "Wđ = ½·m·v²: v được bình phương", FS, DGREEN, alpha=k3)


# ---------------- canh 4: Bay + chua noi duoc ----------------
BAY_X, BAY_ST, BAY_E = 2.4, 5.2, 7.8
def bars(d, x0, vals, lab, col, k, ka):
    text(d, (x0 + 230, 520), lab, 60, col, alpha=ka)
    base = 1080
    d.line([(x0 + 20, base), (x0 + 440, base)], fill=A(INK, ka), width=4)
    for j, (v, s) in enumerate(vals):
        cx = x0 + 120 + 220 * j; h = 200 * v * k
        if h > 0: d.rectangle([cx - 55, base - h, cx + 55, base], fill=A(col, ka))
        text(d, (cx, base - 200 * v - 42), s, FS, col, alpha=ka * k)
        text(d, (cx, base + 48), ("nhẹ", "mạnh")[j], FS, INK, alpha=ka)


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 338), fill=A(DRED, a1), r=38)
    text(d, (W / 2, 300), "BẪY", 56, WHITE, alpha=a1)
    text(d, (W / 2, 410), "“Lấy Δt chia cho d”", 60, INK, alpha=a1)
    card(d, (50, 460, 530, 1290), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    bars(d, 60, BAY, "Δt : d", DRED, appear(t, 0.6, 1.0), a1)
    text(d, (290, 1225), "✗ mạnh mà nhỏ", 56, DRED, alpha=appear(t, BAY_X, 0.45))
    a2 = appear(t, BAY_ST, 0.45)
    if a2 > 0:
        card(d, (550, 460, 1030, 1290), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        bars(d, 560, ((ROWS[0][2], fm(ROWS[0][2])), (ROWS[1][2], fm(ROWS[1][2]))), "d : Δt", DGREEN, appear(t, BAY_ST, 0.8), a2)
        text(d, (790, 1225), "✓ mạnh thì lớn", 56, DGREEN, alpha=a2)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (50, 1330, 1030, 1550), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1385), "Chưa nói được:", FS, NAVY, alpha=k3)
        text(d, (W / 2, 1480), "số liệu minh hoạ, chưa đo thật", 56, INK, alpha=k3)


# ---------------- canh 5: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Đồ thị Wđ theo v: đường cong", FS, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 56
    card(d, (W / 2 - pw / 2, 480, W / 2 + pw / 2, 556), fill=A(ORANGE, k1), r=38)
    text(d, (W / 2, 518), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    text(d, (W / 2, 620), "Xe 0,60 kg, chắn 2,0 cm,", 60, INK, alpha=k1)
    text(d, (W / 2, 700), "đo được Δt = 0,010 s.", 60, INK, alpha=k1)
    text(d, (W / 2, 780), "Wđ khoảng bao nhiêu?", 60, INK, alpha=k1)
    if k1 > 0:   # hinh: xe 3 tang gia trong qua cong quang, khong ghi dap so
        ty = 1260
        track(d, ty=ty, gate=640, a=k1)
        cart(d, 200 + 45 * t, 1.0, k1, ty=ty, n_mass=2)   # xe tu tu lan toi cong (chua qua)
        text(d, (800, ty - 230), "Wđ = ?", 62, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + pass_t(i), "tap") for i in range(4)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + BAY_X, "buzz"), (e["t0"] + END_Q + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-dongthe-02", header="KHTN 9 · THÍ NGHIỆM", footer="Động năng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe lăn qua cổng quang", draw=s_hook, tail=0.3, caps=[
   ("Tấm chắn che tia sáng.", 3.2),
   ("Dừng lại, tự đoán.", 6.2)]),
 dict(key="do", title="Đẩy xe bốn lần", draw=s_do, tail=0.4, caps=[
   ("Đẩy nhẹ, rồi đẩy mạnh hơn.", 4.6),
   ("Thêm gia trọng, lặp lại.", 4.2)]),
 dict(key="dapan", title="Wđ theo v", draw=s_dapan, tail=0.4, caps=[
   ("Nối ba điểm xanh.", 3.4),
   ("Xe nặng gấp đôi, cong dốc hơn.", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("So hai cách tính v.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 7.5)]),
])
