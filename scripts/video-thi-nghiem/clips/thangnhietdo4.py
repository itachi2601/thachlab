# Clip: tn-l12-thangnhietdo-04 - Ba nhiet ke do cung mot coc nuoc: tiep xuc va hong ngoai.
# Ban 1 (28/10/2026). Ban 2 (26/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32): cong --do-chu (chu ve >= 58 px,
#   <= 180 tu/phut moi canh, nhip >= 2,5 s), <= 50 s, K10 (khong nut A-D, khong dong "Chon dap an o khung cau hoi").
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thangnhietdo-04.json (_kiem_so() doi chieu so_lieu_mau, dung_cu, ghi_chu):
#   thuy ngan 49,8 · dien tu 50,2 · HN mat nuoc 5 cm 48,4 · HN thanh su 5 cm 47,1 · HN giay bac 5 cm 41,0 · 25 cm 38,5;
#   eps may 0,95; eps giay bac 0,02-0,10.
# Quan niem sai can danh (hien_tuong_hay_sai[1]): hong ngoai "chinh xac hon" nen so tren giay bac la nhiet do that.
# Du doan: ban hong ngoai vao giay bac dan ngoai coc nuoc ~50 °C -> so doc thap hon han (41,0).
# Thu tu: Du doan -> Tien hanh (2 nhiet ke tiep xuc, HN mat nuoc / thanh su / giay bac) -> Vi sao (cung nhiet do,
#   buc xa khac: su nhieu, bac it) -> Bay lui xa 25 cm (vet do hung ca nen) -> Chot + THU NGHI.
# Thu nghi (= cau_chot khung web): dan bang dinh giay (be mat nham, kho: dung_cu "so be mat bong voi be mat nham") de len
#   giay bac, ban HN cach 5 cm -> gan 47 °C nhu thanh su (CA TU SUY: kho khong co so do tren bang dinh; bang dinh nham
#   phat xa manh nhu thanh su va cung nhiet do voi thanh coc). Dap so khong hien o canh chot.
from engine import *

ROWS = [("Thuỷ ngân", 49.8), ("Điện tử", 50.2), ("Hồng ngoại: mặt nước", 48.4),
        ("Hồng ngoại: thành sứ", 47.1), ("Hồng ngoại: giấy bạc", 41.0)]
IR25, EPS_MAY, T_NUOC = 38.5, 0.95, 50

def fmt(x): return f"{x:.1f}".replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-thangnhietdo-04.json")))
    vals = [r[1] for r in k["so_lieu_mau"]["hang"]]
    assert vals == [v for _, v in ROWS] + [IR25], vals
    assert "0,02–0,10" in k["so_lieu_mau"]["ghi_chu"] and "0,95" in k["so_lieu_mau"]["ghi_chu"]
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["t_nuoc"]["mac_dinh"] == T_NUOC and ts["d"]["mac_dinh"] == 5 and ts["eps_be_mat"]["mac_dinh"] == EPS_MAY
    assert any("băng dính" in x["ten"] for x in k["dung_cu"])
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
CREAM, EDGE, SILVER = (246, 240, 228), (150, 140, 120), (196, 202, 214)
FS = 58                                     # chu nho nhat khi ve (x0,88 = 51 px trong mp4)

# ---------------- bo cuc hinh dung cu (khung ve 1080 x 1920, vung hien y 200-1690) ----------------
CUP_L, CUP_R, CUP_T, CUP_B, WALL = 200, 560, 520, 960, 24
WATER_Y = 600
FOIL = (560, 700, 578, 840)                 # giay bac dan ngoai thanh phai
TH_X, PR_X = 290, 440                       # nhiet ke thuy ngan, que do dien tu
PX5 = 70                                    # 5 cm tren hinh
GS = 1.25                                   # co sung hong ngoai

def _pose(tx, ty, ang, dist, kind, r):
    a = math.radians(ang)
    return (tx + dist * math.cos(a), ty - dist * math.sin(a), ang, (tx, ty), kind, r)
IDLE = (720, 760, 0, None, None, 0)
P_WATER = _pose(480, WATER_Y, 45, PX5, "h", 14)
P_WALL = _pose(CUP_R, 640, 0, PX5, "v", 14)
P_FOIL = _pose(FOIL[2], 770, 0, PX5, "v", 14)

def steam(d, t, a=1.0):
    for j, x0 in enumerate((345, 510)):
        pts = [(x0 + 14 * math.sin(3.0 * t + j * 2 + y / 26), y) for y in range(440, 590, 6)]
        sh = (t * 40 + j * 30) % 60
        pts = [(x, y - sh) for x, y in pts]
        d.line(pts, fill=A((205, 212, 226), 0.9 * a), width=8)

def cup(d, t, foil=True):
    d.arc([CUP_L - 110, 620, CUP_L + 30, 840], 90, 270, fill=EDGE, width=20)
    d.arc([CUP_L - 110, 620, CUP_L + 30, 840], 90, 270, fill=CREAM, width=11)
    d.rectangle([CUP_L + WALL, WATER_Y, CUP_R - WALL, CUP_B - 24], fill=(191, 219, 254))
    d.line([(CUP_L + WALL, WATER_Y), (CUP_R - WALL, WATER_Y)], fill=BLUE, width=4)
    for box in ((CUP_L, CUP_T, CUP_L + WALL, CUP_B), (CUP_R - WALL, CUP_T, CUP_R, CUP_B), (CUP_L, CUP_B - 24, CUP_R, CUP_B)):
        d.rectangle(box, fill=CREAM, outline=EDGE, width=3)
    steam(d, t)
    if foil:
        x0, y0, x1, y1 = FOIL
        d.rectangle([x0, y0, x1, y1], fill=SILVER, outline=(120, 128, 145), width=2)
        for k in range(6): d.line([(x0 + 2, y0 + 20 + k * 22), (x1 - 2, y0 + 12 + k * 22)], fill=WHITE, width=2)

def thermo(d, level):
    d.rounded_rectangle([TH_X - 13, 330, TH_X + 13, 900], radius=13, fill=WHITE, outline=NAVY, width=3)
    dot(d, TH_X, 906, 21, (170, 176, 190), outline=NAVY)
    top = lerp(860, 420, level)
    d.rectangle([TH_X - 5, top, TH_X + 5, 900], fill=(150, 156, 172))
    for k in range(10):
        y = 420 + k * 44; d.line([(TH_X + 4, y), (TH_X + 13, y)], fill=NAVY, width=2)

def probe(d):
    d.rounded_rectangle([PR_X - 40, 330, PR_X + 40, 420], radius=12, fill=NAVY)
    d.rounded_rectangle([PR_X - 27, 344, PR_X + 27, 382], radius=6, fill=(160, 220, 200))
    d.line([(PR_X, 420), (PR_X, 900)], fill=(120, 128, 145), width=8)
    dot(d, PR_X, 902, 7, NAVY)

def gun(d, pose, beam=1.0, s=GS):
    nx, ny, ang, tgt, kind, r = pose
    a = math.radians(ang); u = (math.cos(a), -math.sin(a)); v = (-u[1], u[0])
    P = lambda x, y: (nx + s * (x * u[0] + y * v[0]), ny + s * (x * u[1] + y * v[1]))
    if tgt is not None and beam > 0:
        tx, ty = tgt
        e1, e2 = ((tx, ty - r), (tx, ty + r)) if kind == "v" else ((tx - r, ty), (tx + r, ty))
        d.polygon([P(0, -8), P(0, 8), e2, e1], fill=A(RED, 0.22 * beam))
        if kind == "v": d.ellipse([tx - 7, ty - r, tx + 7, ty + r], fill=A(RED, 0.6 * beam))
        else: d.ellipse([tx - r, ty - 7, tx + r, ty + 7], fill=A(RED, 0.6 * beam))
    hc = mix(TEAL, NAVY, 0.35)
    d.polygon([P(118, 26), P(154, 26), P(168, 128), P(130, 128)], fill=hc)
    d.polygon([P(0, -13), P(26, -22), P(26, 22), P(0, 13)], fill=NAVY)
    d.polygon([P(26, -30), P(176, -30), P(176, 30), P(26, 30)], fill=TEAL)
    d.polygon([P(128, -18), P(166, -18), P(166, 14), P(128, 14)], fill=(160, 220, 200))

def pose_at(pa, pb, k):
    k = ease(k)
    return (lerp(pa[0], pb[0], k), lerp(pa[1], pb[1], k), lerp(pa[2], pb[2], k), pb[3], pb[4], pb[5])

def bubble(d, val, col=ORANGE, a=1.0, sub=None):
    card(d, (720, 280, 1020, 400 if sub is None else 490), fill=A(WHITE, a), outline=A(col, a), r=26, w=5)
    text(d, (870, 340), val, 66, col, alpha=a)
    if sub: text(d, (870, 435), sub, FS, RED, alpha=a)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o cao 70 px, tat lan luot tu PHAI sang TRAI (khong chia theo so nao cua dap an)."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    ka = appear(t, M[1] - 0.2, 0.6)
    cup(d, t); thermo(d, 0.85); probe(d)
    gun(d, pose_at(IDLE, P_FOIL, (t - M[1] + 0.2) / 0.7), beam=ka)
    text(d, (TH_X, 285), "thuỷ ngân", FS, INK)
    text(d, (PR_X + 70, 455), "điện tử", FS, INK, anchor="lm")
    text(d, (860, 990), "hồng ngoại", FS, INK)
    text(d, (620, 610), "giấy bạc", FS, INK, anchor="lm")
    d.line([(600, 640), (575, 700)], fill=INK, width=4)
    if ka > 0: bubble(d, "?", PURPLE, ka)
    if ka <= 0: return
    y0 = 1065 + (1 - ka) * 30
    card(d, (60, y0, 1020, y0 + 470), fill=A(WHITE, ka), outline=A(PURPLE, ka), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, ka)
    text(d, (W / 2, y0 + 175), "Nước ấm 50 °C.", 64, INK, alpha=ka)
    text(d, (W / 2, y0 + 265), "Số đọc trên giấy bạc?", 64, PURPLE, alpha=ka)
    seg_bar(d, y0 + 360, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, ka)

# ---------------- canh 2: Tien hanh ----------------
STEP = 3.0                                    # moi nhip 3 s (moc phu de)
POSES = [IDLE, P_WATER, P_WALL, P_FOIL]
def row_t(i, M):                              # luc hang i hien (hai hang tiep xuc cung luc)
    return M[0] + 0.6 if i < 2 else M[i - 1] + 1.0

def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]; cur = cur_cap(sc, t)
    level = lerp(0.2, 0.9, ease((t - 0.1) / 0.8))
    pose, beam, ir = IDLE, 0.0, None
    for s in (1, 2, 3):
        if cur < s: break
        u = t - M[s]
        pose = pose_at(POSES[s - 1], POSES[s], u / 0.7); beam = appear(u, 0.6, 0.3)
        ir = ROWS[s + 1][1] if t >= row_t(s + 1, M) else (ROWS[s][1] if s > 1 else None)
    cup(d, t); thermo(d, level); probe(d); gun(d, pose, beam)
    if ir is not None: bubble(d, fmt(ir) + " °C", ORANGE, a=appear(t, row_t(2, M), 0.3), sub="cách 5 cm")
    card(d, (60, 1060, 1020, 1530), fill=WHITE, outline=NAVY, w=4)
    for i, (nm, v) in enumerate(ROWS):
        a = appear(t, row_t(i, M), 0.3); y = 1120 + i * 88
        if a <= 0: continue
        if i == 4 and a >= 1: d.rounded_rectangle([80, y - 40, 1000, y + 40], radius=16, fill=(255, 237, 213))
        col = NAVY if i < 2 else (DRED if i == 4 else DORANGE)
        text(d, (100, y), nm, FS, INK, anchor="lm", alpha=a)
        text(d, (980, y), fmt(v) + " °C", 62, col, anchor="rm", alpha=a)

# ---------------- canh 3: vi sao ----------------
def packets(d, t, x0, x1, ys, col, w, speed=170, gap=150):
    L = x1 - x0
    for j, y in enumerate(ys):
        for n in range(4):
            p = (t * speed + n * gap + j * 50) % (gap * 4)
            if p > L - 60: continue
            xa = x0 + p
            pts = [(xa + q, y + 13 * math.sin(q / 9.0)) for q in range(0, 60, 3)]
            d.line(pts, fill=col, width=w)
            hh = 12 + w
            d.polygon([(xa + 62 + hh, y), (xa + 58, y - hh), (xa + 58, y + hh)], fill=col)

def panel_surface(d, t, x0, kind):
    card(d, (x0, 280, x0 + 460, 1000), fill=WHITE, outline=LIGHT, w=4)
    sx = x0 + 50
    d.rectangle([sx, 420, sx + 60, 900], fill=CREAM, outline=EDGE, width=3)
    if kind == "bac":
        d.rectangle([sx + 60, 470, sx + 76, 850], fill=SILVER, outline=(120, 128, 145), width=2)
        packets(d, t, sx + 90, x0 + 290, (660,), ORANGE, 6)
    else:
        packets(d, t, sx + 76, x0 + 290, (540, 610, 680, 750), ORANGE, 11)
    gun(d, (x0 + 300, 650, 0, None, None, 0), 0, s=0.8)

def s_why(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    panel_surface(d, t, 60, "su"); panel_surface(d, t, 560, "bac")
    text(d, (290, 345), "Thành sứ", 62, INK); text(d, (790, 345), "Giấy bạc", 62, INK)
    text(d, (290, 950), "ε ≈ 0,95", FS, DGREEN); text(d, (790, 950), "ε 0,02–0,10", FS, DRED)
    text(d, (W / 2, 1080), "ε: độ phát xạ", 62, INK)
    k = appear(t, M[1], 0.4)
    if k > 0:
        card(d, (60, 1160, 1020, 1560), fill=A(WHITE, k), outline=A(NAVY, k), w=4)
        text(d, (W / 2, 1235), "Máy đặt sẵn ε = 0,95", 62, INK, alpha=k)
        for j, (v, col) in enumerate(((ROWS[3][1], DORANGE), (ROWS[4][1], DRED))):
            cx = 290 + 500 * j
            text(d, (cx, 1355), ("sứ" if j == 0 else "bạc"), 62, INK, alpha=k)
            text(d, (cx, 1465), fmt(v) + " °C", 80, col, alpha=k)

# ---------------- canh 4: bay lui xa (nhin thang vao coc: vet do 5 cm nam gon trong giay bac, 25 cm trum ra nen phong) ----------------
def spot(d, cx, cy, r, t, a=1.0):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(RED, 0.16 * a))
    n = max(8, int(r / 7)); off = t * 35
    for i in range(n):
        a0 = off + i * 360 / n
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 360 / n * 0.55, fill=A(RED, a), width=7)
    dot(d, cx, cy, 9 + 3 * math.sin(6 * t), A(RED, a))

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    for j, (x0, lab) in enumerate(((60, "cách 5 cm"), (560, "cách 25 cm"))):
        card(d, (x0, 280, x0 + 460, 1000), fill=(232, 233, 238), outline=(DGREEN if j == 0 else DRED), w=5)
        cx = x0 + 230
        d.rectangle([cx - 80, 400, cx + 80, 880], fill=CREAM, outline=EDGE, width=4)
        d.rectangle([cx - 80, 490, cx + 80, 790], fill=SILVER, outline=(120, 128, 145), width=3)
        for k in range(7): d.line([(cx - 78, 520 + k * 40), (cx + 78, 500 + k * 40)], fill=WHITE, width=3)
        r = 28 if j == 0 else lerp(28, 140, ease((t - 0.6) / 1.4))     # vet do to theo khoang cach (25/5 = 5 lan)
        spot(d, cx, 640, r, t)
        text(d, (cx, 340), lab, FS, INK)
        if j == 1:
            text(d, (cx, 945), "nền phòng", FS, INK)
            arrow(d, (cx - 120, 910), (cx - 120, 790), INK, w=9, head=24)
    k2 = appear(t, M[1], 0.4)
    if k2 > 0:
        for j, (x0, v, col) in enumerate(((60, ROWS[4][1], DORANGE), (560, IR25, DRED))):
            card(d, (x0, 1060, x0 + 460, 1260), fill=A(WHITE, k2), outline=A(col, k2), w=5)
            text(d, (x0 + 230, 1160), fmt(v) + " °C", 76, col, alpha=k2)
        text(d, (W / 2, 1380), "vết đo trùm ra ngoài", FS, DRED, alpha=k2)

# ---------------- canh 5: chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    # coc thu nho + giay bac + bang dinh giay dan de len
    ox, oy, s = 150, 400, 0.9
    d.rectangle([ox, oy, ox + 300 * s, oy + 380 * s], fill=CREAM, outline=EDGE, width=4)
    d.rectangle([ox + 22, oy + 60, ox + 300 * s - 22, oy + 380 * s - 22], fill=(191, 219, 254))
    fx = ox + 300 * s
    d.rectangle([fx, oy + 110, fx + 18, oy + 270], fill=SILVER, outline=(120, 128, 145), width=2)
    d.rectangle([fx + 18, oy + 130, fx + 34, oy + 250], fill=(222, 196, 150), outline=(160, 130, 90), width=2)
    gun(d, (fx + 34 + 70, oy + 190, 0, (fx + 34, oy + 190), "v", 14), k1, s=1.0)
    text(d, (760, 400), "băng dính giấy", FS, INK, alpha=k1)
    d.line([(700, 435), (fx + 30, oy + 135)], fill=A(INK, k1), width=4)
    text(d, (W / 2, 940), "Dán đè lên giấy bạc,", 64, INK, alpha=k1)
    text(d, (W / 2, 1040), "vẫn cách 5 cm.", 64, INK, alpha=k1)
    text(d, (W / 2, 1170), "Số đọc gần bao nhiêu?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1330, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, w, b, e = (sc[k] for k in ("hook", "do", "why", "bay", "end"))
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + row_t(4, do["M"]), "ding"), (w["t0"] + w["M"][1], "tap"),
            (b["t0"] + 0.6, "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l12-thangnhietdo-04", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thang nhiệt độ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ba nhiệt kế, một cốc nước", draw=s_hook, tail=0.3, caps=[
   ("Hai cái nhúng, một cái bắn.", 3.6),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Đo lần lượt", draw=s_do, tail=0.5, caps=[
   ("Chờ số ổn định.", STEP),
   ("Bắn vào mặt nước.", STEP),
   ("Rồi bắn thành cốc.", STEP),
   ("Giấy bạc: thấp hơn hẳn.", 3.4)]),
 dict(key="why", title="Cùng ấm, sao khác số?", draw=s_why, tail=0.4, caps=[
   ("Mặt bóng phát bức xạ rất yếu.", 3.8),
   ("Máy tính ra nhiệt độ thấp giả.", 4.2)]),
 dict(key="bay", title="Bẫy: lùi xa hơn", draw=s_bay, tail=0.4, caps=[
   ("Cùng mảnh giấy bạc, lùi ra xa.", 3.4),
   ("Hứng cả nền phòng: số còn thấp nữa.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.6, caps=[
   ("Hồng ngoại đo bức xạ bề mặt.", 6.6)]),
])
