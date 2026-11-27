# Clip: tn-l9-dongthe-01 - Vien bi lan xuong mang nghieng va vao khuc go (KHTN 9, 5/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom A): chu than canh >= 56, nhan hang bieu do hien san tu dau canh
#   (khong noi khoi chu moi theo tung lan), so s chi ghi so (don vi o tieu de), khong nut A-D (K10), thanh dem 90 px,
#   tach Ket qua / Rut ra thanh canh rieng, Bay = hai bieu do canh nhau (nghi nhu nhau ✗ / do xa hon ✓), bo o "Goi y".
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-dongthe-01.json (_kiem_so()):
#   so_lieu_mau (m g, h cm, s cm): 50 10 4,0 ; 50 20 8,0 ; 100 10 8,0   (ghi_chu: minh hoa, chua phai so do that)
#   bay = hien_tuong_hay_sai[0] (chi toc do quan trong, khoi luong khong). chua noi duoc = mo_hinh.gia_thiet[0]
#   (chi so sanh dinh tinh -> dong nang tang may lan chua noi duoc).
# Du doan (K10): cung tha 10 cm, thay bi 50 g bang bi 100 g -> khuc go di xa hon.
# THU NGHI = cau_chot khung web: bi 50 g tha 15 cm (tham_so h buoc 5 cm, chua hien) -> s trong khoang 4,0-8,0 cm.
#   Kho khong co ghi_chu chot; giu y chot cua clip cu. Man chot KHONG in dap an.
# Lop 9: khong dung "dong luong", khong cong thuc dong nang (TN sau cua bai).
import copy, json, os
from engine import *

WOOD = (214, 170, 118); WOOD_D = (140, 96, 52); STEEL = (148, 163, 184); STEEL_D = (51, 65, 85)
RAIL = (203, 213, 225); RAIL_D = (71, 85, 105); RULER = (253, 246, 200); RULER_D = (170, 150, 60)
DRED = (185, 28, 28); OR_BG = (255, 237, 213); DGREEN = (21, 110, 55); DPURP = (76, 29, 149)
FS, FL = 56, 60

# ---------------- hinh hoc (toa do khung 1080x1920) ----------------
Y0 = 820                         # mat san
PXH = 14                         # 1 cm do cao = 14 px
RB_X, RT_X, RT_H = 640, 330, 300  # chan mang, dau mang (x), do cao dau mang (px)
UX, UY = (RB_X - RT_X) / math.hypot(RB_X - RT_X, RT_H), RT_H / math.hypot(RB_X - RT_X, RT_H)   # huong xuong doc
NX, NY = UY, -UX                 # phap tuyen phia tren mat mang
POLE_X = 150                     # cot thuoc do cao
XB, BW, BH = 690, 92, 84         # mep sau khuc go luc dau, rong, cao
PXCM = 30                        # thuoc san: 1 cm = 30 px
ACC = 700.0                      # gia toc doc mang (px/s2): tha 20 cm mat ~1,1 s
SLIDE, HOLD = 0.9, 0.6
RUNS = [(50, 10, 4.0), (50, 20, 8.0), (100, 10, 8.0)]       # so_lieu_mau
H_C = 15
def vn(x): return f"{x:.1f}".replace(".", ",")
def rad(g): return 21 if g == 50 else 27                     # bi thep: r ti le can bac 3 cua m


def _kiem_so():
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-dongthe-01.json")))
    assert [tuple(h) for h in k["so_lieu_mau"]["hang"]] == RUNS, k["so_lieu_mau"]["hang"]
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["h"]["min"] * 100 <= H_C <= ts["h"]["max"] * 100
    assert abs((H_C / 100 / ts["h"]["buoc"]) - round(H_C / 100 / ts["h"]["buoc"])) < 1e-9
    assert H_C not in [r[1] for r in RUNS]
_kiem_so()


def surf(hcm):
    hp = hcm * PXH; return RB_X - hp * UX / UY, Y0 - hp


def ball_path(g, hcm, tau):
    """(x, y tam bi, da cham go, thoi diem cham) sau khi tha tau giay."""
    r = rad(g); sx, sy = surf(hcm); x0, y0 = sx + r * NX, sy + r * NY
    L = ((Y0 - r) - y0) / UY; t1 = math.sqrt(2 * L / ACC); v1 = ACC * t1
    x1 = x0 + L * UX; t2 = max(0.0, (XB - r) - x1) / v1; ti = t1 + t2
    if tau <= 0: return x0, y0, False, ti
    if tau < t1: s = 0.5 * ACC * tau * tau; return x0 + s * UX, y0 + s * UY, False, ti
    if tau < ti: return x1 + v1 * (tau - t1), Y0 - r, False, ti
    return XB - r, Y0 - r, True, ti


def run_len(i):
    g, h, _ = RUNS[i]; return ball_path(g, h, 0)[3] + SLIDE + HOLD


def slide(u, D): u = clamp(u / SLIDE); return D * (1 - (1 - u) ** 2)


# ---------------- ve dung cu ----------------
def ruler(d):
    y = Y0 + 12
    d.rectangle([XB - 14, y, XB + 10.6 * PXCM, y + 44], fill=RULER, outline=RULER_D, width=2)
    for k in range(11):
        x = XB + k * PXCM; L = 30 if k % 2 == 0 else 16
        d.line([(x, y), (x, y + L)], fill=NAVY, width=3 if L == 30 else 2)
        if k % 4 == 0: text(d, (x, y + 80), str(k), FS, INK)


def pole(d, hl=None, labels=True, marks=(10, 20)):
    d.rectangle([POLE_X - 7, Y0 - 330, POLE_X + 7, Y0], fill=RULER, outline=RULER_D, width=2)
    for hcm in marks:
        y = Y0 - hcm * PXH; on = hl == hcm
        d.line([(POLE_X - 16, y), (POLE_X + 16, y)], fill=NAVY, width=4)
        if labels: text(d, (POLE_X - 30, y), f"{hcm}", FS, ORANGE if on else INK, anchor="rm")
        if on:   # net dut tu cot toi diem tha
            sx, _ = surf(hcm)
            for xx in range(POLE_X + 20, int(sx) - 6, 18):
                d.line([(xx, y), (min(xx + 9, sx), y)], fill=ORANGE, width=3)


def ramp(d):
    sx0, sy0 = RT_X, Y0 - RT_H
    d.line([(sx0 + 30, sy0 + 30), (sx0 + 30, Y0)], fill=RAIL_D, width=8)
    th = 20
    d.polygon([(sx0, sy0), (RB_X, Y0), (RB_X - th / UY, Y0), (sx0 - th * NX, sy0 - th * NY)], fill=RAIL, outline=RAIL_D)
    d.line([(sx0, sy0), (RB_X, Y0)], fill=RAIL_D, width=5)


def floor(d):
    d.line([(60, Y0), (1020, Y0)], fill=NAVY, width=6)


def block(d, dx, ghost=False):
    x0 = XB + dx
    if ghost:
        for yy in range(int(Y0 - BH), Y0, 16):
            d.line([(XB, yy), (XB, yy + 8)], fill=GRAY, width=3)
    d.rectangle([x0, Y0 - BH, x0 + BW, Y0], fill=WOOD, outline=WOOD_D, width=4)
    for k in (1, 2):
        d.line([(x0 + 10, Y0 - BH * k / 3), (x0 + BW - 10, Y0 - BH * k / 3)], fill=WOOD_D, width=2)


def ball(d, x, y, g, label=True):
    r = rad(g)
    d.ellipse([x - r, y - r, x + r, y + r], fill=STEEL, outline=STEEL_D, width=4)
    d.ellipse([x - r * 0.55, y - r * 0.6, x - r * 0.1, y - r * 0.15], fill=A(WHITE, 0.85))
    if label: text(d, (x, y - r - 40), f"{g} g", FS, NAVY)


def s_arrow(d, dx):
    if dx < 30: return
    ya = Y0 - BH - 34
    arrow(d, (XB + 4, ya), (XB + dx, ya), GREEN, w=5, head=16)
    text(d, (XB + dx / 2, ya - 40), "s", FS, GREEN)


def rig(d, g, hcm, bx, by, dx, ghost=False, hl=None, label=True, plabels=True, marks=(10, 20)):
    card(d, (40, 262, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    text(d, (POLE_X - 30, 410), "h (cm)", FS, MUTED, anchor="lm")
    pole(d, hl, plabels, marks); ramp(d); floor(d); ruler(d)
    block(d, dx, ghost); s_arrow(d, dx)
    ball(d, bx, by, g, label)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    x, y, _, _ = ball_path(50, 10, 0)
    rig(d, 50, 10, x, y, 0, hl=10)
    k0 = appear(t, 0.6, 0.4)
    if k0 > 0:
        p, q = surf(16), surf(4)
        arrow(d, (p[0] + 70 * NX, p[1] + 70 * NY), (q[0] + 70 * NX, q[1] + 70 * NY), A(BLUE, k0), w=5, head=18)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 580), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FS)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 102), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", FS, WHITE, alpha=a)
    text(d, (W / 2, y0 + 180), "Cùng thả từ 10 cm,", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "bi 100 g đẩy gỗ đi", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 350), "xa hay gần hơn bi 50 g?", FL, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 440, 970, y0 + 530], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 440, 110 + max(90, 860 * (1 - p)), y0 + 530], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh ----------------
R0 = 0.8
ST = [R0, R0 + run_len(0), max(R0 + run_len(0) + run_len(1), 4.2)]


def state(i, t):
    """(bi x, y, go dx, da cham, da dung) cua lan i luc t."""
    g, h, s = RUNS[i]; tau = t - ST[i]
    x, y, hit, ti = ball_path(g, h, tau)
    dx = slide(tau - ti, s * PXCM) if hit else 0.0
    if hit: x += 0.3 * dx
    return x, y, dx, hit, tau >= ti + SLIDE


def cur_run(t):
    c = 0
    for i, s in enumerate(ST):
        if t >= s - 0.3: c = i
    return c


BX0, BSC = 420, 64
def bars(d, t, y=965, hl=(), alpha=1.0, rows=(0, 1, 2), gap=150):
    hh = 110 + gap * len(rows) + 10
    card(d, (40, y, 1040, y + hh), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    text(d, (230, y + 60), "bi · h", FS, MUTED, alpha=alpha)
    text(d, (BX0 + 20, y + 60), "s (cm)", FS, GREEN, anchor="lm", alpha=alpha)
    for j, i in enumerate(rows):
        g, h, s = RUNS[i]; yy = y + 110 + gap / 2 + gap * j
        hb = 56
        if i in hl: d.rounded_rectangle([56, yy - hb, 1024, yy + hb], radius=20, fill=A(OR_BG, alpha))
        text(d, (230, yy), f"{g} g · {h}", FS, NAVY, alpha=alpha)
        _, _, dx, hit, done = state(i, t)
        L = dx / PXCM * BSC
        d.line([(BX0, yy - hb + 8), (BX0, yy + hb - 8)], fill=A(MUTED, alpha), width=3)
        if L > 2: d.rounded_rectangle([BX0, yy - 26, BX0 + L, yy + 26], radius=12, fill=A(GREEN, alpha))
        if done: text(d, (BX0 + L + 20, yy), vn(s), FS, DGREEN, anchor="lm", alpha=alpha)


def s_do(img, d, t, sc):
    i = cur_run(t); g, h, _ = RUNS[i]
    x, y, dx, hit, done = state(i, t)
    rig(d, g, h, x, y, dx, ghost=dx > 0, hl=h)
    bars(d, t, hl=(i,))


def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []
    end3 = ST[2] + ball_path(*RUNS[2][:2], 0)[3] + SLIDE
    if sc["T"] < end3 + 1.0: bad.append(("canh ngan", sc["T"], end3))
    for i in range(2):
        if ST[i + 1] < ST[i] + run_len(i) - 1e-9: bad.append(("chong lan", i))
    return bad


# ---------------- canh 3: Ket qua ----------------
def pill(d, s, y, a, color=NAVY, size=FS):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, y - 42, W / 2 + pw / 2, y + 42), fill=A(color, a), r=40)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: xa hơn", 310, 1.0)
    # bieu do lan 1 vs lan 3 moc lai tu dau
    bars(d, ST[2] - 0.2 + min(t * 1.4, 3.0), y=390, rows=(0, 2), hl=(2,) if t > 1.6 else ())
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y1 = 880 + (1 - k2) * 30
        card(d, (40, y1, 1040, y1 + 300), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, y1 + 150), "Bi nặng hơn → gỗ xa hơn", FL, DGREEN, alpha=k2)


# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    tau = (t - 0.3) % 3.2
    x, y, hit, ti = ball_path(50, 20, tau)
    dx = slide(tau - ti, 8.0 * PXCM) if hit else 0.0
    if hit: x += 0.3 * dx
    rig(d, 50, 20, x, y, dx, ghost=dx > 0, hl=20, label=False, plabels=False, marks=(20,))
    k1 = appear(t, 0.2, 0.45)
    card(d, (40, 965, 1040, 1205), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
    text(d, (W / 2, 1045), "Động năng", 72, DGREEN, alpha=k1)
    text(d, (W / 2, 1140), "do chuyển động", FL, INK, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y2 = 1250 + (1 - k2) * 30
        card(d, (40, y2, 1040, y2 + 300), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), w=5)
        text(d, (W / 2, y2 + 95), "Nặng hơn, cao hơn", FL, (154, 52, 18), alpha=k2)
        text(d, (W / 2, y2 + 200), "→ gỗ đi xa hơn", FL, (154, 52, 18), alpha=k2)


# ---------------- canh 5: Bay (hai bieu do canh nhau) roi Chua noi duoc ----------------
BAY_R, BAY_C = 3.4, 6.4
def vbars(d, x0, vals, col, k, ka):
    base = 1060
    d.line([(x0 + 40, base), (x0 + 430, base)], fill=A(INK, ka), width=4)
    for j, (g, v) in enumerate(vals):
        cx = x0 + 145 + 190 * j; h = 330 * v / 8.0 * k
        if h > 0: d.rectangle([cx - 55, base - h, cx + 55, base], fill=A(col, ka))
        text(d, (cx, base - 330 * v / 8.0 - 42), vn(v), FL, mix(col, INK, 0.3), alpha=ka * k)
        r = rad(g) * 1.3
        d.ellipse([cx - r, base + 60 - r, cx + r, base + 60 + r], fill=A(STEEL, ka), outline=A(STEEL_D, ka), width=4)


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FS)) + 64
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 348), fill=A(DRED, a1), r=40)
    text(d, (W / 2, 308), "BẪY", FS, WHITE, alpha=a1)
    text(d, (W / 2, 410), "“Nặng nhẹ như nhau”", FL, INK, alpha=a1)
    card(d, (40, 470, 530, 1260), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    text(d, (285, 540), "s (cm) nghĩ", FS, DRED, alpha=a1)
    vbars(d, 50, ((50, RUNS[0][2]), (100, RUNS[0][2])), DRED, appear(t, 0.6, 1.0), a1)
    text(d, (285, 1195), "✗ như nhau", FS, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (550, 470, 1040, 1260), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        text(d, (795, 540), "s (cm) đo", FS, DGREEN, alpha=a2)
        vbars(d, 560, ((50, RUNS[0][2]), (100, RUNS[2][2])), DGREEN, appear(t, BAY_R, 0.9), a2)
        text(d, (795, 1195), "✓ xa hơn", FS, DGREEN, alpha=a2)
    k3 = appear(t, BAY_C, 0.45)
    if k3 > 0:
        card(d, (40, 1300, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1370), "Chưa nói được:", FL, NAVY, alpha=k3)
        text(d, (W / 2, 1475), "động năng tăng mấy lần", FL, INK, alpha=k3)


# ---------------- canh 6: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 415), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 340), "Nặng, nhanh → động năng lớn", FS, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 450, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FS)) + 60
    card(d, (W / 2 - pw / 2, 478, W / 2 + pw / 2, 558), fill=A(ORANGE, k1), r=40)
    text(d, (W / 2, 518), "THỬ NGHĨ", FS, WHITE, alpha=k1)
    text(d, (W / 2, 650), "Bi 50 g, thả 15 cm.", FL, INK, alpha=k1)
    text(d, (W / 2, 735), "Gỗ đi bao xa?", FL, INK, alpha=k1)
    if k1 > 0.5:
        # mang nho: cot do cao co vach 15, khuc go, thuoc "?"
        ox, oy, sc_ = 120, 1330, 0.8
        d.line([(ox + 60, oy), (ox + 860, oy)], fill=NAVY, width=6)
        d.rectangle([ox + 40, oy - 300, ox + 54, oy], fill=RULER, outline=RULER_D, width=2)
        yh = oy - 15 * PXH * 1.1
        d.line([(ox + 30, yh), (ox + 64, yh)], fill=NAVY, width=4)
        text(d, (ox + 20, yh), "15", FS, ORANGE, anchor="rm")
        d.polygon([(ox + 200, oy - 260), (ox + 520, oy), (ox + 500, oy), (ox + 186, oy - 246)], fill=RAIL, outline=RAIL_D)
        xr = ox + 200 + (yh - (oy - 260)) / 260 * 320          # diem tren mat mang o do cao 15
        for xx in range(ox + 70, int(xr) - 30, 18): d.line([(xx, yh), (xx + 9, yh)], fill=ORANGE, width=3)
        d.ellipse([xr + 8 - 21, yh - 40 - 21, xr + 8 + 21, yh - 40 + 21], fill=STEEL, outline=STEEL_D, width=4)
        d.rectangle([ox + 560, oy - 84, ox + 652, oy], fill=WOOD, outline=WOOD_D, width=4)
        arrow(d, (ox + 660, oy - 110), (ox + 820, oy - 110), ORANGE, w=6, head=18)
    card(d, (330, 1400, 750, 1520), fill=A((255, 247, 237), k1), r=20)
    text(d, (540, 1460), "s = ? cm", 64, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + ST[i] + ball_path(*RUNS[i][:2], 0)[3], "tap") for i in range(3)]
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.3, "buzz"),
            (b["t0"] + BAY_R, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-dongthe-01", header="KHTN 9 · THÍ NGHIỆM", footer="Động năng · thachlab.id.vn", cues=_cues, scenes=[
 dict(key="hook", title="Viên bi và khúc gỗ", draw=s_hook, tail=0.3, caps=[
   ("Bi lăn, va khúc gỗ.", 2.9),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thả bi 50 g: 10, 20 cm.", 3.4),
   ("Giữ 10 cm, đổi bi 100 g.", 3.4),
   ("Đo quãng s gỗ đi.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("So lần 1, 3.", 3.0),
   ("Khối lượng có tác dụng.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Vì sao gỗ đi?", 3.0),
   ("Khi nào nó lớn?", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Nghe hợp lí?", 3.0),
   ("Đo thử xem.", 3.0),
   ("Còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Dừng lại, tự ước lượng.", 6.4)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
