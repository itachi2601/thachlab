# Clip: tn-l12-tdhphantu-01 - Hat khoi trong hop kinh soi qua kinh hien vi.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-tdhphantu-01.json:
#   so_lieu_mau (minh hoa, thang 1-5): 10 °C -> 2 · 25 °C -> 3 · 40 °C -> 4 · 55 °C -> 5
#   tham_so: duong kinh hat khoi d mac dinh 1 µm, max 5 µm.
# Duong di Brown: buoc ngau nhien seed co dinh, moi khung re <= 50°, toc do moi khung ti le muc nhay cua hang dang doc
#   -> the nhiet do, hang to sang va toc do hat cung mot ham state().
# Ban 1 (14/11/2026). Ban 2 (26/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32): cong --do-chu (chu ve >= 58 px,
#   <= 180 tu/phut moi canh, nhip >= 2 s), <= 50 s, K10 (khong nut A-D), bo canh "chua noi duoc" (giu trong khung web).
# Du doan (khung web): hop kin, khong gio; moi cham sang chuyen dong the nao? A dung yen / B roi thang / C nhay hon loan,
#   gap khuc (DUNG) / D troi deu mot phia.
# Bay (hien_tuong_hay_sai[0]): "hat nhay vi co gio" -> gio thi moi hat troi cung chieu; hai hat canh nhau di hai kieu.
#   KHONG dung bay "duong gap khuc = duong di phan tu": cau Tu kiem tra ngay sau hop hoi dung y nay.
# THU NGHI (= cau_chot khung, CA TU SUY ghi trong kho): cung 25 °C, hat 5 µm thay 1 µm -> nhay YEU hon.
import random
from engine import *

ROWS = [(10, 2), (25, 3), (40, 4), (55, 5)]   # (nhiet do hop °C, muc nhay thang 1-5) - so_lieu_mau

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-tdhphantu-01.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["d"]["mac_dinh"] == 1 and ts["d"]["max"] == 5
_kiem_so()

DARK = (14, 18, 36)
P_COL = ((255, 236, 170), (170, 225, 255))
DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8); BROWN = (140, 95, 25)
FS = 58

def pill(d, cx, cy, s, fill, alpha=1.0, size=56, fg=WHITE):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

# ---------------- trang thai (canh doi nhiet do) ----------------
RT = [0.4 + 1.7 * k for k in range(4)]               # moc doi hang trong canh "nhiet"
def state(t, sc):
    """-> (nhiet do, muc nhay, chi so hang)"""
    if sc["key"] != "nhiet": return 25, 3, 1
    k = 0
    for i, x in enumerate(RT):
        if t >= x: k = i
    return ROWS[k][0], ROWS[k][1], k

# ---------------- duong di Brown ----------------
MC, MR = (540, 700), 430                              # vong kinh to (~80% be rong) - cong B v1 muc 1
GEO = {"do": ((540, 700), 430), "nhiet": ((540, 640), 360)}
UM = 32                                               # 1 µm = 32 px (duong kinh hat 1 µm)
_PATHS = {}
def brown_path(seed, start, speeds, mc=None, mr=None):
    mc = mc or MC; mr = mr or MR
    R = random.Random(seed); x, y = start; h = R.uniform(0, 2 * math.pi)
    pts = [(x, y)]; turn_left = 0.0; seg = 0
    for v in speeds:
        if seg <= 0 and abs(turn_left) < 1e-6:
            seg = R.randint(3, 7)
            turn_left = math.radians(R.uniform(40, 150)) * (1 if R.random() < 0.5 else -1)
        dx, dy = x - mc[0], y - mc[1]
        if math.hypot(dx, dy) > mr - 70 and abs(turn_left) < 1e-6:
            want = math.atan2(-dy, -dx); diff = (want - h + math.pi) % (2 * math.pi) - math.pi
            turn_left = diff
        st = max(-math.radians(50), min(math.radians(50), turn_left))
        h += st; turn_left -= st; seg -= 1
        x += v * math.cos(h); y += v * math.sin(h)
        r = math.hypot(x - mc[0], y - mc[1])
        if r > mr - 30:
            x = mc[0] + (x - mc[0]) * (mr - 30) / r; y = mc[1] + (y - mc[1]) * (mr - 30) / r
        pts.append((x, y))
    return pts

def paths(sc):
    key = (sc["key"], round(sc["T"], 3))
    if key not in _PATHS:
        n = int(sc["T"] * FPS) + 4; (cx, cy), mr = GEO[sc["key"]]
        sp = [3.4 * state(i / FPS, sc)[1] for i in range(n)]
        _PATHS[key] = (brown_path(14, (cx - 0.45 * mr, cy - 0.1 * mr), sp, (cx - 0.45 * mr, cy), 0.55 * mr),
                       brown_path(23, (cx + 0.45 * mr, cy + 0.1 * mr), sp, (cx + 0.45 * mr, cy), 0.55 * mr))
    return _PATHS[key]

def scope(d, t, sc, trail=50):
    (cx, cy), mr = GEO[sc["key"]]
    d.ellipse([cx - mr - 14, cy - mr - 14, cx + mr + 14, cy + mr + 14], fill=(60, 64, 80))
    d.ellipse([cx - mr, cy - mr, cx + mr, cy + mr], fill=DARK)
    yb = cy + 0.62 * mr; x0 = cx - 0.42 * mr                 # thanh ti le 5 µm + nhan "mo phong" (cong B v1 muc 4, 8)
    d.line([(x0, yb), (x0 + 5 * UM, yb)], fill=(200, 205, 220), width=6)
    d.line([(x0, yb - 14), (x0, yb + 14)], fill=(200, 205, 220), width=4); d.line([(x0 + 5 * UM, yb - 14), (x0 + 5 * UM, yb + 14)], fill=(200, 205, 220), width=4)
    text(d, (x0 + 2.5 * UM, yb - 52), "5 µm", FS, (200, 205, 220))
    text(d, (cx, cy - 0.72 * mr), "mô phỏng", FS, (150, 158, 185))
    P = paths(sc); i = min(int(t * FPS), len(P[0]) - 1)
    for k, pts in enumerate(P):
        j0 = max(0, i - trail)
        for j in range(j0, i):
            a = 0.15 + 0.75 * (j - j0) / max(1, i - j0)
            d.line([pts[j], pts[j + 1]], fill=A(P_COL[k], a), width=7)
        x, y = pts[i]
        dot(d, x, y, 28, A(P_COL[k], 0.25)); dot(d, x, y, UM // 2, P_COL[k])

def temp_card(d, T):
    card(d, (830, 250, 1050, 420), fill=WHITE, outline=NAVY, w=4, r=22)
    text(d, (940, 297), "Hộp", FS, INK)
    text(d, (940, 372), f"{T} °C", 62, DORANGE if T >= 40 else (BLUE if T <= 10 else INK))

# ---------------- canh 1: Du doan ----------------
def apparatus(d, t, y0=300):
    card(d, (300, y0, 1000, y0 + 470), fill=(30, 32, 44), r=18)
    bx0, by0, bx1, by1 = 400, y0 + 120, 860, y0 + 420
    d.rectangle([bx0, by0, bx1, by1], fill=(70, 76, 96), outline=(200, 214, 235), width=6)
    d.rectangle([bx0 - 12, by0 - 22, bx1 + 12, by0], fill=(200, 214, 235))
    for k in range(7):
        cx = bx0 + 70 + k * 55 + 6 * math.sin(t * 0.7 + k); cy = by0 + 110 + 40 * math.sin(k * 1.7)
        dot(d, cx, cy, 46, A((190, 195, 210), 0.18))
    for k in range(9):                                    # cham sang trong chum den (cong B v1 muc 6), dung yen: khong lo dap an
        dot(d, 330 + k * 58, y0 + 245 + 22 * math.sin(k * 2.3), 6, (255, 250, 220))
    d.rounded_rectangle([110, y0 + 230, 270, y0 + 300], radius=14, fill=(90, 96, 110))
    d.polygon([(270, y0 + 222), (300, y0 + 210), (300, y0 + 320), (270, y0 + 308)], fill=(120, 126, 140))
    d.polygon([(300, y0 + 230), (bx1, y0 + 215), (bx1, y0 + 315), (300, y0 + 300)], fill=A((255, 236, 150), 0.32 + 0.1 * math.sin(t * 3)))
    MCOL = (215, 222, 236)
    d.rounded_rectangle([592, y0 - 44, 668, y0 - 20], radius=8, fill=MCOL)
    d.rectangle([606, y0 - 20, 654, y0 + 70], fill=MCOL)
    d.polygon([(612, y0 + 70), (648, y0 + 70), (640, y0 + 100), (620, y0 + 100)], fill=MCOL)
    d.line([(654, y0 + 10), (720, y0 + 10), (720, y0 + 60)], fill=MCOL, width=14)
    text(d, (190, y0 + 400), "đèn", FS, INK)

def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    apparatus(d, t)
    pill(d, 650, 860, "hộp kín, hạt khói 1 µm", LIGHT, size=FS, fg=INK)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1000 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 430), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 180), "Không gió: chấm sáng", 64, INK, alpha=k)
    text(d, (W / 2, y0 + 265), "chuyển động ra sao?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 335, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: soi o 25 °C ----------------
def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    scope(d, t, sc)
    card(d, (40, 1170, 1040, 1570), fill=WHITE, outline=LIGHT, w=4)
    for j, (lab, col) in enumerate((("hạt A", P_COL[0]), ("hạt B", P_COL[1]))):
        x = 110 + 300 * j
        dot(d, x, 1240, 24, DARK); dot(d, x, 1240, 14, col)
        text(d, (x + 45, 1240), lab, FS, INK, anchor="lm")
    text(d, (1000, 1240), "25 °C", FS, INK, anchor="rm")
    k = appear(t, M[1], 0.4)
    text(d, (W / 2, 1390), "hai đường khác nhau", FS, DGREEN, alpha=k)

# ---------------- canh 3: doi nhiet do ----------------
def s_nhiet(img, d, t, sc):
    IMG_REF[0] = img
    T, lv, kk = state(t, sc)
    scope(d, t, sc)
    card(d, (40, 1030, 1040, 1580), fill=WHITE, outline=LIGHT, w=4)
    text(d, (290, 1080), "Nhiệt độ", FS, INK)
    text(d, (740, 1080), "Mức nhảy", FS, INK)
    text(d, (W / 2, 1530), "minh hoạ, chênh thật nhỏ hơn", FS, PURPLE)   # cong B v1 muc 3
    d.line([(70, 1120), (1010, 1120)], fill=LIGHT, width=3)
    for j, (Tj, lj) in enumerate(ROWS):
        yy = 1170 + 80 * j
        if j == kk: d.rounded_rectangle([70, yy - 38, 1010, yy + 38], radius=18, fill=(255, 237, 213))
        text(d, (290, yy), f"{Tj} °C", FS, INK)
        for b in range(5):
            x = 610 + b * 56
            d.rounded_rectangle([x, yy - 22, x + 44, yy + 22], radius=8, fill=ORANGE if b < lj else LIGHT)
        if j == kk: d.polygon([(88, yy - 18), (88, yy + 18), (116, yy)], fill=DORANGE)

# ---------------- canh 4: co che ----------------
NM = 16
def hits(t):
    out = []; net = [0.0, 0.0]
    for i in range(NM):
        per = 0.9 + 0.35 * ((i * 7) % 5) / 5; ph = i / NM
        u = t / per + ph; cyc = int(u); f = u - cyc
        R = random.Random(1000 * i + cyc); ang = R.uniform(0, 2 * math.pi)
        dist = abs(1 - 2 * f)
        out.append((ang, dist, f))
        if abs(f - 0.5) < 0.12: net[0] -= math.cos(ang); net[1] -= math.sin(ang)
    return out, net

def mech_pos(t, cx, cy):
    return (cx + 14 * math.sin(t * 2.3) + 9 * math.sin(t * 5.1), cy + 12 * math.cos(t * 1.9) + 8 * math.sin(t * 4.3))

def mech(d, t, cx, cy, alpha=1.0):
    px, py = mech_pos(t, cx, cy); RP = 95
    hs, net = hits(t)
    for ang, dist, f in hs:
        r = RP + 12 + dist * 190
        dot(d, px + r * math.cos(ang), py + r * math.sin(ang), 12, A(BLUE, alpha))
        if abs(f - 0.5) < 0.12:
            bx, by = px + (RP + 8) * math.cos(ang), py + (RP + 8) * math.sin(ang)
            d.line([(bx, by), (bx + 26 * math.cos(ang), by + 26 * math.sin(ang))], fill=A(ORANGE, alpha), width=6)
    dot(d, px, py, RP, A((240, 214, 150), alpha), outline=A(NAVY, alpha))
    L = math.hypot(*net)
    if L > 0.3:
        s = min(150, 70 * L)
        arrow(d, (px, py), (px + s * net[0] / L, py + s * net[1] / L), A(RED, alpha), w=10, head=30)
    return px, py

def s_ket(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 250, 1040, 1080), fill=WHITE, outline=LIGHT, w=4)
    px, py = mech_pos(t, 540, 690)
    ex, ey = px - 95 * 0.72, py - 95 * 0.69
    d.line([(170, 345), (ex, ey)], fill=BROWN, width=4)
    mech(d, t, 540, 690)
    dot(d, ex, ey, 7, BROWN)
    text(d, (70, 320), "hạt khói", FS, BROWN, anchor="lm")
    text(d, (1010, 320), "phân tử (vẽ to)", FS, BLUE, anchor="rm")
    arrow(d, (90, 1020), (190, 1020), RED, w=10, head=28)          # cong B v1 muc 5: chu thich mui ten
    text(d, (220, 1020), "tổng lực đẩy", FS, RED, anchor="lm")
    k1 = appear(t, M[1], 0.45)
    if k1 > 0:
        card(d, (60, 1130, 1020, 1300), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1215), "Phân tử: hỗn loạn, không ngừng", 60, DGREEN, alpha=k1)

# ---------------- canh 5: Bay (hai hinh canh nhau) ----------------
BMC = (790, 700)
BAY_P = (brown_path(31, (760, 680), [5.0] * 400, BMC, 190), brown_path(47, (820, 720), [5.0] * 400, BMC, 190))

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]; ka = appear(t, 0.3, 0.3)
    for cx, lab, col in ((290, "Nếu do gió", DRED), (790, "Quan sát", DGREEN)):
        card(d, (cx - 240, 250, cx + 240, 1230), fill=WHITE, outline=col, w=6)
        text(d, (cx, 320), lab, 62, col, alpha=ka)
        d.rounded_rectangle([cx - 220, 480, cx + 220, 920], radius=20, fill=DARK)
    for j, y in enumerate((540, 640, 720, 800, 870)):
        xx = 80 + (40 * j + t * 75) % 400
        fa = clamp((xx - 80) / 40) * clamp((490 - xx) / 40)
        d.line([(xx - 70, y), (xx - 12, y)], fill=A(P_COL[0], 0.5 * fa), width=4)
        dot(d, xx, y, 10, A(P_COL[0], fa))
    arrow(d, (150, 980), (430, 980), TEAL, w=8, head=24)
    text(d, (290, 1060), "trôi", FS, DRED, alpha=ka)
    text(d, (290, 1135), "cùng một phía", FS, DRED, alpha=ka)
    i = min(len(BAY_P[0]) - 1, int(t * FPS))
    for k, pts in enumerate(BAY_P):
        j0 = max(0, i - 60)
        for j in range(j0, i):
            d.line([pts[j], pts[j + 1]], fill=A(P_COL[k], 0.2 + 0.7 * (j - j0) / max(1, i - j0)), width=6)
        dot(d, pts[i][0], pts[i][1], 14, P_COL[k])
    k = appear(t, M[1], 0.4)
    text(d, (790, 1060), "hai hạt,", FS, DGREEN, alpha=k)
    text(d, (790, 1135), "hai kiểu đi", FS, DGREEN, alpha=k)

# ---------------- canh 6: chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    for x, r, lab in ((330, 22, "1 µm"), (720, 110, "5 µm")):
        wob = 6 * math.sin(t * 4 + r) if k1 > 0.5 else 0
        dot(d, x + wob, 560, r, A((240, 214, 150), k1), outline=A(NAVY, k1))
        text(d, (x, 720), lab, 64, INK, alpha=k1)
    text(d, (W / 2, 1000), "Cùng 25 °C, hạt 5 µm:", 64, INK, alpha=k1)
    text(d, (W / 2, 1090), "mức nhảy lớn hơn hay", 64, DORANGE, alpha=k1)
    text(d, (W / 2, 1180), "nhỏ hơn hạt 1 µm?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1320, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, nh, k, b, e = (sc[x] for x in ("hook", "do", "nhiet", "ket", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding"), (do["t0"] + do["M"][1], "tap")]
    out += [(nh["t0"] + x, "tap") for x in RT[1:]]
    out += [(k["t0"] + k["M"][1], "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l12-tdhphantu-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thuyết động học phân tử · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hạt khói trong hộp kính", draw=s_hook, tail=0.3, caps=[
   ("Rọi đèn ngang qua hộp khói.", 3.4),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Soi qua kính hiển vi", draw=s_do, tail=0.4, caps=[
   ("Đáp án: nhảy hỗn loạn, gấp khúc.", 4.0),
   ("Hai hạt cạnh nhau đi hai kiểu.", 3.6)]),
 dict(key="nhiet", title="Đổi nhiệt độ hộp", draw=s_nhiet, tail=0.4, caps=[
   ("Lạnh thì nhảy yếu.", 3.2),
   ("Ấm hơn, nhảy mạnh hơn.", 3.6)]),
 dict(key="ket", title="Vì sao hạt nhảy?", draw=s_ket, tail=0.4, caps=[
   ("Phân tử khí đập từ mọi phía.", 3.8),
   ("Đập không đều: hạt bị lệch.", 4.8)]),
 dict(key="bay", title="Bẫy: hạt nhảy vì có gió?", draw=s_bay, tail=0.4, caps=[
   ("Gió đẩy mọi hạt cùng một phía.", 3.8),
   ("Ở đây hai hạt đi hai kiểu.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Hạt khói nhảy: phân tử đập không đều.", 6.0)]),
])
