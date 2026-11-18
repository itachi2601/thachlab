# Clip: tn-l9-dongthe-03 - Qua nang roi xuong khay cat: vet lom nao sau hon? (KHTN 9, lo 6, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-dongthe-03.json:
#   so_lieu_mau (m kg, h m, Wt J, x cm): 0,1 0,2 0,2 1,0 ; 0,1 0,4 0,4 2,0 ; 0,2 0,2 0,4 2,0
#   mo_hinh: x = Wt / 20 N ; tham_so m 0,05-0,3 kg, h 0,1-0,6 m.
# Roi tu do that (g = 9,8) chieu cham deu x4; vet lom ve phong to (1 cm = 30 px, co ghi chu tren man).
# Canh: Du doan (100 g tu 40 cm hay 200 g tu 20 cm lom sau hon; K10) -> Tien hanh (3 lan theo cac_buoc, so do sau +
#   hang bang hien dung luc qua nang dung yen trong cat; gat phang cat roi moi nhac qua len) -> DAP AN · sau bang nhau
#   -> Rut ra (cao gap doi / nang gap doi -> lom gap doi) -> Chua noi duoc + bay "the nang chi phu thuoc do cao" ✗
#   -> Chot + THU NGHI (300 g muon lom 1,5 cm: tha tu 10 cm; Wt = 0,3 J).
# Lua chon Du doan (o khung web): A. Qua 100 g tha tu 40 cm · B. Qua 200 g tha tu 20 cm · C. Sau gan bang nhau (dung)
#   · D. Ca hai khong de lai vet lom.
# Cau 3 sau hop hoi Wt qua cam 200 g o 3 m (dung P = 10m) -> clip KHONG hien cong thuc, khong tinh Wt ra J.
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

def weight(d, cx, ybot, g, alpha=1.0, label=True):
    h = WH[g]
    d.rounded_rectangle([cx - WW / 2, ybot - h, cx + WW / 2, ybot], radius=10, fill=A(METAL, alpha), outline=A(NAVY, alpha), width=3)
    d.arc([cx - 18, ybot - h - 34, cx + 18, ybot - h + 2], 180, 360, fill=A(NAVY, alpha), width=5)   # moc
    if label: text(d, (cx, ybot - h / 2), f"{g} g", 40, WHITE, alpha=alpha)

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

def ruler(d, x=150, top=50):
    d.rectangle([x - 14, SAND - top * PXCM - 12, x + 14, SAND], fill=RULER, outline=RULER_D, width=3)
    for c in range(0, top + 1, 5):
        y = SAND - c * PXCM; L = 22 if c % 10 == 0 else 12
        d.line([(x - 14, y), (x - 14 + L, y)], fill=NAVY, width=3)
        if c % 10 == 0 and c > 0: text(d, (x + 26, y), str(c), 40, MUTED, bold=False, anchor="lm")
    text(d, (x + 26, SAND - top * PXCM - 40), "cm", 40, MUTED, bold=False, anchor="lm")

def shelf(d):
    d.rectangle([800, SHELF_Y, 1045, SHELF_Y + 16], fill=(120, 90, 60))
    d.rectangle([915, SHELF_Y + 16, 931, TBOT + 12], fill=(120, 90, 60))

def height_mark(d, cx, h_cm, col, alpha=1.0):
    y = SAND - h_cm * PXCM
    for xx in range(240, int(cx - WW / 2), 26): d.line([(xx, y), (min(xx + 14, cx - WW / 2), y)], fill=A(col, alpha), width=4)

# ---------------- trang thai qua nang theo thoi gian (canh tien hanh) ----------------
def fall_T(h_cm): return math.sqrt(2 * h_cm / 100 / G) * SLOW
SINK = 0.18
REL = [0.6, 4.2, 8.0]                         # moc tha lan 1, 2, 3 (giay trong canh)
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

# ---------------- canh 1: du doan ----------------
HX = (300, 600)
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    tray(d, []); ruler(d)
    for cx, (g, h, _) in zip(HX, (RUNS[1], RUNS[2])):
        height_mark(d, cx, h, ORANGE)
        weight(d, cx, SAND - h * PXCM, g)
    text(d, (HX[0] + 70, SAND - 40 * PXCM - 40), "40 cm", 40, ORANGE, anchor="lm")
    text(d, (HX[1] + 70, SAND - 20 * PXCM - 40), "20 cm", 40, ORANGE, anchor="lm")
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1190, 1020, 1530), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1245), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1325, "Vết lõm của quả nào sâu hơn?", 44, INK, alpha=k)
    text(d, (W / 2, 1405), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=appear(t, sc["M"][1] + 0.2))
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1470, 940, 1484], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1470, 140 + 800 * (1 - q), 1484], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
def s_do(img, d, t, sc):
    IMG_REF[0] = img
    i, objs, dp, show, h = state(t)
    tray(d, [(WX, dp)]); ruler(d); shelf(d)
    tau = t - REL[i]
    if tau < fall_T(h) + SINK: height_mark(d, WX, h, ORANGE)
    for g, cx, yb in objs: weight(d, cx, yb, g)
    if tau < 0 and i > 0 and 0.45 <= (tau + PREP) / PREP < 0.95:
        text(d, (WX, SAND + 52), "gạt phẳng", 40, NAVY)
    if show is not None:
        y1 = SAND + dp
        d.line([(WX + WW / 2 + 26, SAND), (WX + WW / 2 + 26, y1)], fill=RED, width=5)
        d.line([(WX + WW / 2 + 14, SAND), (WX + WW / 2 + 38, SAND)], fill=RED, width=4)
        d.line([(WX + WW / 2 + 14, y1), (WX + WW / 2 + 38, y1)], fill=RED, width=4)
    text(d, (1000, 330), "chiếu chậm", 40, MUTED, bold=False, anchor="rm")
    text(d, (1000, 385), "vết lõm vẽ to", 40, MUTED, bold=False, anchor="rm")
    table(d, [1 if (j < i or (j == i and show is not None)) else 0 for j in range(3)])

def ans_dents(d):
    tray(d, [(HX[0], 2.0 * DPX), (HX[1], 2.0 * DPX)])

# ---------------- canh 3: dap an ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    ans_dents(d)
    for cx, (g, h, x) in zip(HX, (RUNS[1], RUNS[2])):
        yr = SAND - h * PXCM
        height_mark(d, cx, h, ORANGE, alpha=0.6)
        weight(d, cx, yr, g, alpha=0.35)                                      # vi tri luc tha (mo)
        for yy in range(int(yr) + 10, SAND - 10, 26): d.line([(cx, yy), (cx, min(yy + 14, SAND - 10))], fill=GRAY, width=4)
        weight(d, cx, SAND + x * DPX, g)
        text(d, (cx, yr - WH[g] - 56), f"thả {h} cm", 40, ORANGE)
        y1 = SAND + x * DPX; xr = cx + WW / 2 + 22
        d.line([(xr, SAND), (xr, y1)], fill=RED, width=5)
    table(d, [1, 1, 1])
    a = appear(t, M[0] + 0.2, 0.4)
    for j in (1, 2):
        y = 1195 + 135 + j * 70
        d.rounded_rectangle([90, y - 32, 990, y + 32], radius=16, outline=A(GREEN, a), width=5)
    a2 = appear(t, M[1] - 0.1, 0.4)
    if a2 > 0:
        card(d, (110, 268, 970, 372), fill=A(GREEN, a2), r=50)
        text(d, (W / 2, 320), "ĐÁP ÁN · sâu bằng nhau: 2,0 cm", 44, WHITE, alpha=a2)

# ---------------- canh 4: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    for k, (yy, at, a_, b_, lom) in enumerate(((300, 0.3, "100 g: 20 cm → 40 cm", "cao gấp đôi", "1,0 → 2,0 cm"),
                                               (700, M[1] - 0.1, "20 cm: 100 g → 200 g", "nặng gấp đôi", "1,0 → 2,0 cm"))):
        a = appear(t, at, 0.4)
        if a <= 0: continue
        card(d, (60, yy, 1020, yy + 340), fill=A(WHITE, a), outline=A(ORANGE if k == 0 else BLUE, a), w=5)
        text(d, (W / 2, yy + 60), a_, 44, ORANGE if k == 0 else BLUE, alpha=a)
        text(d, (W / 2, yy + 150), b_, 44, INK, alpha=a)
        text(d, (W / 2, yy + 250), lom, 44, RED, alpha=appear(t, at + 0.6, 0.4))
    a3 = appear(t, M[1] + 2.0, 0.4)
    if a3 > 0:
        card(d, (60, 1110, 1020, 1300), fill=A((220, 252, 231), a3), outline=A(GREEN, a3), w=5)
        ctext(d, 1205, "Nặng hơn, cao hơn: thế năng lớn hơn", 44, GREEN, maxw=880, alpha=a3)

# ---------------- canh 5: chua noi duoc + bay ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.1)
    card(d, (60, 270, 1020, 470), fill=WHITE, outline=BLUE, w=6)
    text(d, (W / 2, 325), "Chưa nói được:", 46, BLUE, alpha=a)
    text(d, (W / 2, 405), "Bao nhiêu jun: chưa tính.", 42, INK, alpha=a)
    b = appear(t, M[1] - 0.05, 0.3)
    if b <= 0: return
    x = appear(t, M[1] + 2.3, 0.3)
    card(d, (60, 590, 1020, 1130 if x > 0 else 760), fill=A(WHITE, b), outline=A(RED, b), w=6)
    text(d, (W / 2, 650), "Bẫy:", 44, RED, alpha=b)
    q = "“Thế năng chỉ phụ thuộc độ cao”"; qw = tw(d, q, F(44))
    text(d, (W / 2, 715), q, 44, INK, alpha=b)
    if x <= 0: return
    d.line([(W / 2 - qw / 2 - 6, 717), (W / 2 + qw / 2 + 6, 717)], fill=A(RED, x), width=6)
    text(d, (W / 2 + qw / 2 + 30, 715), "✗", 48, RED, anchor="lm", alpha=x)
    # hinh nho: cung 20 cm, hai vet lom 1,0 va 2,0 cm
    sy, s = 1010, 0.8
    d.rectangle([140, sy, 940, sy + 80], fill=A(SANDC, x))
    for cx, g, xc in ((330, 100, 1.0), (720, 200, 2.0)):
        dp = xc * DPX * s
        d.pieslice([cx - 60, sy - dp, cx + 60, sy + dp], 0, 180, fill=A((214, 186, 128), x))
        hh = WH[g] * s
        d.rounded_rectangle([cx - 45, sy + dp - hh, cx + 45, sy + dp], radius=8, fill=A(METAL, x), outline=A(NAVY, x), width=3)
        text(d, (cx, sy + dp - hh - 34), f"{g} g", 40, INK, alpha=x)
        text(d, (cx + 70, sy + 40), fc(xc) + " cm", 40, RED, anchor="lm", alpha=x)
    text(d, (W / 2, 800), "✓ Quả nặng hơn lõm sâu hơn", 42, GREEN, alpha=x)
    text(d, (W / 2, 868), "cùng 20 cm", 40, ORANGE, alpha=x)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def body(d, t, k1):
        sy = 1200
        d.rectangle([200, sy, 880, sy + 60], fill=A(SANDC, k1)); d.line([(200, sy), (880, sy)], fill=A(SAND_D, k1), width=4)
        cx, yb = 440, sy - 150
        d.rounded_rectangle([cx - 60, yb - 80, cx + 60, yb], radius=10, fill=A(METAL, k1), outline=A(NAVY, k1), width=3)
        text(d, (cx, yb - 40), "100 g", 40, WHITE, alpha=k1)
        arrow(d, (cx + 100, sy), (cx + 100, yb + 4), A(ORANGE, k1), w=5, head=16)
        text(d, (cx + 124, (sy + yb) / 2), "thả từ ? cm", 40, ORANGE, anchor="lm", alpha=k1)
        text(d, (W / 2, sy + 30), "lõm sâu 3,0 cm", 40, RED, alpha=k1)
        kh = appear(t, sc["M"][0] + 2.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1470), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1345), "Gợi ý", 40, ORANGE, alpha=kh)
        ctext(d, 1415, "Cùng khay cát", 42, INK, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Vật ở trên cao có thế năng",
             "Quả 100 g: thả từ độ cao nào?", None, body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.5, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + REL[i] + fall_T(RUNS[i][1]), "tap") for i in range(3)]
    out += [(an["t0"] + an["M"][1] - 0.1, "ding"), (tr["t0"] + tr["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-dongthe-03", header="KHTN 9 · THÍ NGHIỆM", cues=_cues,
    footer="Động năng. Thế năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Quả nặng và khay cát", draw=s_hook, tail=0.6, caps=[
   ("Khay cát mịn, gạt phẳng.", 2.6),
   ("Nghĩ kĩ rồi mới xem tiếp.", 5.6)]),
 dict(key="do", title="Thả ba lần, đo vết lõm", draw=s_do, tail=0.6, caps=[
   ("Quả 100 g: 20 rồi 40 cm.", 6.6),
   ("Rồi quả 200 g.", 3.0)]),
 dict(key="ans", title="So lần 2 và lần 3", draw=s_ans, tail=0.6, caps=[
   ("Thả khác nhau.", 2.6),
   ("Vết lõm sâu như nhau.", 3.0)]),
 dict(key="rut", title="Thế năng phụ thuộc gì?", draw=s_rut, tail=0.5, caps=[
   ("Đổi một thứ mỗi lần.", 2.6),
   ("Lõm sâu gấp đôi.", 3.2)]),
 dict(key="trap", title="Giới hạn và cái bẫy", draw=s_trap, tail=0.5, caps=[
   ("Giới hạn của thí nghiệm.", 3.2),
   ("Đúng không? Nhìn vết lõm.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Tự trả lời trước khi xem.", 6.2)]),
])
