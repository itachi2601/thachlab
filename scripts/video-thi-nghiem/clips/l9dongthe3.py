# Clip: tn-l9-dongthe-03 - Qua nang roi xuong khay cat: vet lom nao sau hon? (KHTN 9, lo 6, 18/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4 L9, nhom B): chu than canh >= 55 (ra >= 48 px), moi nhip >= 2,5 s,
#   du doan khong nut A-D (K10), bo dong "Chon dap an...", gop rut ra vao dap an, Bay = hai khay canh nhau, canh chot tu ve.
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-dongthe-03.json (_kiem_so()):
#   so_lieu_mau (m kg, h m, Wt J, x cm): 0,1 0,2 0,2 1,0 ; 0,1 0,4 0,4 2,0 ; 0,2 0,2 0,4 2,0 ; mo hinh x = Wt / 20 N
#   tham_so m 0,05-0,3 kg, h 0,1-0,6 m.
# Du doan (khong trung Cau 3, 5, thu thach ** cua bai): 100 g tu 40 cm hay 200 g tu 20 cm lom sau hon?
#   -> dap an: sau gan bang nhau (2,0 cm).
# Bay = hien_tuong_hay_sai[1] "the nang chi phu thuoc do cao": cung 20 cm, 100 g lom 1,0 cm canh 200 g lom 2,0 cm
#   (cap so khac cap Du doan).
# Chua noi duoc = ghi_chu kho "so lieu minh hoa, chua phai so do that".
# THU NGHI (cau_chot khung web, tu suy trong dai tham_so, "theo mo hinh"): qua 300 g, muon lom 1,5 cm -> tha tu 10 cm
#   (hai buoc: 100 g tu 20 cm lom 1,0 cm -> 1,5 cm can m.h gap 1,5 -> 300 g . h = 1,5 . 100 g . 20 cm -> h = 10 cm;
#   Wt = 10 . 0,3 . 0,1 = 0,3 J -> x = 0,3 : 20 = 0,015 m). Ghi chu kho con neu ca cu (100 g, 3,0 cm -> 60 cm): khong dung
#   vi chi doi so cua chinh quy tac vua chieu. So 10 cm KHONG hien tren man (thuoc chi ghi 20, 40).
from engine import *

G, SLOW = 9.8, 4.0
RUNS = [(100, 20, 1.0), (100, 40, 2.0), (200, 20, 2.0)]        # (g, cm, cm) tu so_lieu_mau
SAND, TBOT, TX0, TX1 = 1050, 1130, 160, 760                     # mat cat, day khay, mep khay
PXCM = 13.0                                                     # 1 cm do cao = 13 px
DPX = 30.0                                                      # 1 cm do sau lom = 30 px (phong to)
WX, WW = 440, 112                                               # tam roi, be rong qua nang
WH = {100: 64, 200: 112, 300: 150}                              # chieu cao qua nang theo khoi luong
SHELF_Y, SLOT = 900, {100: 860, 200: 985}
SANDC = (238, 214, 160); SAND_D = (190, 160, 100); METAL = (71, 85, 105); METAL_L = (148, 163, 184)
RULER = (253, 246, 200); RULER_D = (170, 150, 60)
def fc(x): return f"{x:.1f}".replace(".", ",")
FS = 58; DGREEN = (10, 110, 50); DRED = (185, 28, 28); DINK = (60, 66, 90); DPURP = (76, 29, 149)
CHOT = (300, 1.5, 10)          # g, cm lom, cm tha


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-dongthe-03.json")))
    hang = k["so_lieu_mau"]["hang"]
    assert [(round(h[0] * 1000), round(h[1] * 100), h[3]) for h in hang] == RUNS
    for m, h, wt, x in hang: assert abs(10 * m * h - wt) < 1e-9 and abs(wt / 20 * 100 - x) < 1e-9
    g, x, hc = CHOT; tm, th = k["tham_so"][0], k["tham_so"][1]
    assert tm["min"] <= g / 1000 <= tm["max"] and th["min"] <= hc / 100 <= th["max"]
    assert abs(10 * g / 1000 * hc / 100 / 20 * 100 - x) < 1e-9
_kiem_so()

def weight(d, cx, ybot, g, alpha=1.0, label=True):
    h = WH[g]
    d.rounded_rectangle([cx - WW / 2, ybot - h, cx + WW / 2, ybot], radius=10, fill=A(METAL, alpha), outline=A(NAVY, alpha), width=3)
    d.arc([cx - 18, ybot - h - 34, cx + 18, ybot - h + 2], 180, 360, fill=A(NAVY, alpha), width=5)   # moc
    if label: text(d, (cx + WW / 2 + 20, ybot - h / 2), f"{g} g", FS, INK, anchor="lm", alpha=alpha)

def tray(d, dents, x0=TX0, x1=TX1):
    """dents: [(x tam, sau px)]. Ve khay + mat cat co vet lom."""
    d.rectangle([x0 - 14, SAND - 30, x1 + 14, TBOT + 12], fill=(120, 90, 60))
    pts = [(x0, SAND)]
    for cx, dp in sorted(dents):
        if dp <= 0.5: continue
        for k in range(0, 41):
            u = -1 + k / 20; xx = cx + u * (WW / 2 + 14)
            pts.append((xx, SAND + dp * max(0.0, 1 - u ** 4)))
    pts += [(x1, SAND), (x1, TBOT), (x0, TBOT)]
    d.polygon(pts, fill=SANDC)
    d.line(pts[:-2], fill=SAND_D, width=4)

def ruler(d, x=200, top=50):
    d.rectangle([x - 14, SAND - top * PXCM - 12, x + 14, SAND], fill=RULER, outline=RULER_D, width=3)
    for c in range(0, top + 1, 5):
        y = SAND - c * PXCM; L = 22 if c % 10 == 0 else 12
        d.line([(x - 14, y), (x - 14 + L, y)], fill=NAVY, width=3)
        if c in (20, 40): text(d, (x - 30, y), str(c), FS, DINK, anchor="rm")
    text(d, (x - 30, SAND - top * PXCM), "cm", FS, DINK, anchor="rm")

def shelf(d):
    d.rectangle([800, SHELF_Y, 1045, SHELF_Y + 16], fill=(120, 90, 60))
    d.rectangle([915, SHELF_Y + 16, 931, TBOT + 12], fill=(120, 90, 60))

def height_mark(d, cx, h_cm, col, alpha=1.0):
    y = SAND - h_cm * PXCM
    for xx in range(240, int(cx - WW / 2), 26): d.line([(xx, y), (min(xx + 14, cx - WW / 2), y)], fill=A(col, alpha), width=4)

# ---------------- trang thai qua nang theo thoi gian (canh tien hanh) ----------------
def fall_T(h_cm): return math.sqrt(2 * h_cm / 100 / G) * SLOW
SINK = 0.18
REL = [1.6, 4.6, 8.0]                         # moc tha lan 1, 2, 3 (giay trong canh)
def settle(i): return REL[i] + fall_T(RUNS[i][1]) + SINK          # luc qua nang dung yen, doc do sau
PREP = 1.2                                     # thoi gian chuan bi (gat phang, nhac qua) truoc moi lan tha
def state(t):
    """Tra ve (i lan, cac qua nang [(g, cx, ybot)], do sau lom px tai WX, so do sau dang hien hay None)."""
    i = max([j for j in range(3) if t >= REL[j] - PREP], default=0)
    g, h, x = RUNS[i]; tau = t - REL[i]
    objs = []; dp = 0.0; show = None
    hy = SAND - h * PXCM
    if tau < 0:                                # chuan bi: gat phang cat, dua qua len vi tri tha
        k = clamp((tau + PREP) / PREP)
        if i == 0:
            objs.append((100, WX, hy))
        elif i == 1:
            dp0 = RUNS[0][2] * DPX; dp = dp0 * (1 - ease(clamp((k - 0.45) / 0.4)))      # nhac qua len truoc, roi gat phang
            y0 = SAND + dp0; objs.append((100, WX, lerp(y0, hy, ease(clamp(k / 0.45)))))
        else:
            dp0 = RUNS[1][2] * DPX; dp = dp0 * (1 - ease(clamp((k - 0.5) / 0.35)))
            k2 = ease(clamp(k / 0.5)); k3 = ease(clamp((k - 0.5) / 0.5))
            objs.append((100, lerp(WX, SLOT[100], k2), lerp(SAND + dp0, SHELF_Y, k2) - 150 * math.sin(math.pi * k2)))      # 100 g cat len ke
            objs.append((200, lerp(SLOT[200], WX, k3), lerp(SHELF_Y, hy, k3) - 220 * math.sin(math.pi * k3)))              # 200 g tu ke ra vi tri tha
    else:
        T = fall_T(h)
        if tau < T:
            s = tau / SLOW; yb = hy + 0.5 * G * s * s * 100 * PXCM
            objs.append((g, WX, min(yb, SAND)))
        else:
            k = clamp((tau - T) / SINK); dp = x * DPX * ease(k)
            objs.append((g, WX, SAND + dp))
            if tau >= T + SINK: show = x
        if i == 2: objs.append((100, SLOT[100], SHELF_Y))
    if i < 2: objs.append((200, SLOT[200], SHELF_Y))
    return i, objs, dp, show, h

def table(d, rows_alpha, q=None, y0=1195):
    card(d, (60, y0, 1020, y0 + 330), fill=WHITE, outline=NAVY, w=4)
    xs = (250, 540, 830)
    for x_, s_, c_ in zip(xs, ("Quả nặng", "Thả từ", "Lõm sâu"), (INK, ORANGE, RED)): text(d, (x_, y0 + 50), s_, 40, c_)
    d.line([(100, y0 + 92), (980, y0 + 92)], fill=LIGHT, width=4)
    for j, (g, h, x) in enumerate(RUNS):
        a = rows_alpha[j]; y = y0 + 135 + j * 70
        if a <= 0: continue
        text(d, (xs[0], y), f"{g} g", 42, INK, alpha=a); text(d, (xs[1], y), f"{h} cm", 42, ORANGE, alpha=a)
        text(d, (xs[2], y), (fc(x) + " cm") if q is None or j not in q else "?", 42, RED if q is None or j not in q else PURPLE, alpha=a)

def table(d, rows_alpha, y0=1190):
    card(d, (60, y0, 1020, y0 + 100 + 3 * 80 + 20), fill=WHITE, outline=NAVY, w=4)
    xs = (250, 540, 830)
    for x_, s_, c_ in zip(xs, ("Quả", "Thả từ", "Lõm sâu"), (INK, ORANGE, RED)): text(d, (x_, y0 + 50), s_, FS, c_)
    d.line([(100, y0 + 95), (980, y0 + 95)], fill=LIGHT, width=4)
    for j, (g, h, x) in enumerate(RUNS):
        a = rows_alpha[j]; y = y0 + 145 + j * 80
        if a <= 0: continue
        text(d, (xs[0], y), f"{g} g", FS, INK, alpha=a); text(d, (xs[1], y), f"{h} cm", FS, ORANGE, alpha=a)
        text(d, (xs[2], y), fc(x) + " cm", FS, RED, alpha=a)


def pill(d, s, y, a, color=NAVY, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


# ---------------- canh 1: Du doan ----------------
HX = (380, 700)
def s_hook(img, d, t, sc):
    M = sc["M"]
    tray(d, []); ruler(d)
    for cx, (g, h, _) in zip(HX, (RUNS[1], RUNS[2])):
        height_mark(d, cx, h, ORANGE)
        weight(d, cx, SAND - h * PXCM, g)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1180 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 450), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 60, a, PURPLE)
    text(d, (W / 2, y0 + 170), "Thả cả hai xuống cát.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "Vết lõm quả nào sâu hơn?", 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 320, 970, y0 + 420], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 320, 110 + max(90, 860 * (1 - p)), y0 + 420], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh ----------------
def s_do(img, d, t, sc):
    i, objs, dp, show, h = state(t)
    tray(d, [(WX, dp)]); ruler(d); shelf(d)
    tau = t - REL[i]
    if tau < fall_T(h) + SINK: height_mark(d, WX, h, ORANGE)
    for g, cx, yb in objs: weight(d, cx, yb, g, label=(cx == WX))
    if show is not None:
        y1 = SAND + dp; xm = WX - WW / 2 - 26
        d.line([(xm, SAND), (xm, y1)], fill=RED, width=5)
        d.line([(xm - 12, SAND), (xm + 12, SAND)], fill=RED, width=4)
        d.line([(xm - 12, y1), (xm + 12, y1)], fill=RED, width=4)
    text(d, (1030, 300), "vết lõm vẽ to", FS, DINK, anchor="rm")
    table(d, [1 if (j < i or (j == i and show is not None)) else 0 for j in range(3)])


# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    tray(d, [(HX[0], 2.0 * DPX), (HX[1], 2.0 * DPX)]); ruler(d)
    for cx, (g, h, x) in zip(HX, (RUNS[1], RUNS[2])):
        yr = SAND - h * PXCM
        height_mark(d, cx, h, ORANGE, alpha=0.6)
        for yy in range(int(yr) + 10, SAND - 10, 26): d.line([(cx, yy), (cx, min(yy + 14, SAND - 10))], fill=GRAY, width=4)
        weight(d, cx, SAND + x * DPX, g)
    a = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN: sâu bằng nhau", 300, a, NAVY)
    for cx, x in zip(HX, (RUNS[1][2], RUNS[2][2])):
        y1 = SAND + x * DPX; xr = cx - WW / 2 - 18
        d.line([(xr, SAND), (xr, y1)], fill=A(RED, a), width=6)
        text(d, (cx, 1205), fc(x) + " cm", FS, RED, alpha=a)
    k2 = appear(t, M[1] + 0.4, 0.45)
    if k2 > 0:
        card(d, (50, 1340, 1030, 1560), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=26, w=4)
        text(d, (W / 2, 1400), "Cao gấp đôi bù cho", FS, DGREEN, alpha=k2)
        text(d, (W / 2, 1490), "nặng gấp đôi", FS, DGREEN, alpha=k2)


# ---------------- canh 4: Bay + chua noi duoc ----------------
BAY_X, BAY_ST, BAY_E = 3.4, 5.6, 8.2
def mini(d, x0, g, xc, col, ka, k):
    """O nho: khay cat + qua nang roi tu 20 cm, lom xc cm (k = tien do roi)."""
    sy = 960; hh = WH[g] * 0.8; top = sy - 20 * PXCM
    d.rectangle([x0 + 30, sy, x0 + 450, sy + 90], fill=A(SANDC, ka))
    cx = x0 + 240; dp = xc * DPX * clamp((k - 0.7) / 0.3)
    if dp > 0: d.pieslice([cx - 64, sy - dp, cx + 64, sy + dp], 0, 180, fill=A((214, 186, 128), ka))
    yb = lerp(top, sy, ease(clamp(k / 0.7))) + dp
    d.rounded_rectangle([cx - 48, yb - hh, cx + 48, yb], radius=8, fill=A(METAL, ka), outline=A(NAVY, ka), width=3)
    text(d, (cx, 560), f"{g} g", 60, col, alpha=ka)
    text(d, (cx, 650), "từ 20 cm", FS, ORANGE, alpha=ka)
    if k >= 1: text(d, (cx, sy + 145), fc(xc) + " cm", FS, RED, alpha=ka)


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pill(d, "BẪY", 300, a1, DRED)
    text(d, (W / 2, 410), "“Thế năng chỉ tuỳ độ cao”", 60, INK, alpha=a1)
    card(d, (50, 470, 530, 1200), fill=A(WHITE, a1), outline=A(NAVY, a1), w=5)
    mini(d, 50, 100, 1.0, INK, a1, clamp((t - 1.8) / 1.2))
    a2 = appear(t, BAY_X, 0.45)
    card(d, (550, 470, 1030, 1200), fill=A(WHITE, a2), outline=A(NAVY, a2), w=5)
    if a2 > 0: mini(d, 550, 200, 2.0, INK, a2, clamp((t - BAY_X) / 1.2))
    k = appear(t, BAY_ST, 0.45)
    if k > 0:
        qw = tw(d, "“Thế năng chỉ tuỳ độ cao”", F(60))
        d.line([(W / 2 - qw / 2 - 6, 412), (W / 2 + qw / 2 + 6, 412)], fill=A(DRED, k), width=7)
        text(d, (W / 2, 1265), "✓ nặng hơn thì lõm sâu hơn", 56, DGREEN, alpha=k)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (50, 1340, 1030, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1395), "Chưa nói được:", FS, NAVY, alpha=k3)
        text(d, (W / 2, 1490), "số liệu minh hoạ, chưa đo thật", 56, INK, alpha=k3)


# ---------------- canh 5: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Nặng hơn, cao hơn: lõm sâu hơn", FS, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 518, k1, ORANGE)
    text(d, (W / 2, 620), "Quả 300 g.", 60, INK, alpha=k1)
    text(d, (W / 2, 700), "Muốn lõm 1,5 cm,", 60, INK, alpha=k1)
    text(d, (W / 2, 780), "thả từ độ cao nào?", 60, INK, alpha=k1)
    if k1 > 0:
        sy = 1420
        d.rectangle([150, sy, 930, sy + 110], fill=A(SANDC, k1)); d.line([(150, sy), (930, sy)], fill=A(SAND_D, k1), width=4)
        cx = 470; yb = 1100 + 60 * math.sin(t * 1.6)        # tay nhac qua len xuong, chua tha
        d.rounded_rectangle([cx - 60, yb - WH[300], cx + 60, yb], radius=10, fill=A(METAL, k1), outline=A(NAVY, k1), width=3)
        arrow(d, (cx + 110, sy - 6), (cx + 110, yb + 4), A(ORANGE, k1), w=6, head=18)
        text(d, (cx + 140, (sy + yb) / 2), "h = ?", 62, ORANGE, anchor="lm", alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + REL[i] + fall_T(RUNS[i][1]), "tap") for i in range(3)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + BAY_ST, "buzz"), (e["t0"] + END_Q + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-dongthe-03", header="KHTN 9 · THÍ NGHIỆM", footer="Động năng. Thế năng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Quả nặng và khay cát", draw=s_hook, tail=0.3, caps=[
   ("Khay cát mịn, gạt phẳng.", 3.0),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Thả ba lần, đo vết lõm", draw=s_do, tail=0.6, caps=[
   ("Quả 100 g: 20 rồi 40 cm.", 6.6),
   ("Gạt phẳng, thả quả 200 g.", 3.0)]),
 dict(key="dapan", title="So lần 2 và lần 3", draw=s_dapan, tail=0.4, caps=[
   ("Thả khác nhau, lõm như nhau.", 3.6),
   ("Thế năng lúc thả như nhau.", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Cùng độ cao, khác khối lượng.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 7.5)]),
])
