# Clip: tn-l12-thangnhietdo-04 - Ba nhiet ke do cung mot coc nuoc: tiep xuc va hong ngoai (ban 1, 28/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thangnhietdo-04.json -> so_lieu_mau (t_nuoc = 50 °C, eps may 0,95):
#   thuy ngan 49,8 · dien tu 50,2 · HN mat nuoc 5 cm 48,4 · HN thanh coc su 5 cm 47,1 · HN giay bac 5 cm 41,0 · 25 cm 38,5
#   sai so dung cu: thuy ngan +-0,5 °C, dien tu +-0,2 °C (dung_cu); eps giay bac 0,02-0,10 (ghi_chu).
# Canh: Du doan (giay bac) -> Tien hanh (nhung 2 nhiet ke, ban HN 3 cho) -> Dap an B + Rut ra (do thi diem + 3 the)
#       -> Bay (HN "chinh xac hon") + sai so 25 cm + chua noi duoc -> Chot + cau hoi tu nho lai.
from engine import *

# ---------------- bo cuc (khung 1080x1920) ----------------
CUP_L, CUP_R, CUP_T, CUP_B, WALL = 288, 592, 540, 880, 22
WATER_Y = 600
FOIL = (592, 700, 606, 800)                    # mieng giay bac dan ngoai thanh phai
TH_X, PR_X = 345, 450                          # nhiet ke thuy ngan, que do dien tu
PX5 = 56                                        # 5 cm tren hinh (25 cm = 5 lan)
RD_Y = 920                                     # the so doc
TAB_Y = 1090                                   # bang so lieu / hop du doan

# (nozzle x, y, goc than may so voi phuong ngang (do), diem ngam, kieu vet: 'h' mat ngang / 'v' mat dung, ban kinh vet)
def _pose(tx, ty, ang, dist, kind, r):
    a = math.radians(ang)
    return (tx + dist * math.cos(a), ty - dist * math.sin(a), ang, (tx, ty), kind, r)
IDLE = (730, 760, 0, None, None, 0)
P_WATER = _pose(535, WATER_Y, 72, PX5, "h", 12)
P_WALL = _pose(CUP_R, 640, 0, PX5, "v", 12)
P_FOIL = _pose(FOIL[2], 750, 0, PX5, "v", 12)
P_FOIL25 = _pose(FOIL[2], 750, 0, 5 * PX5, "v", 62)

ROWS = [("Thuỷ ngân, trong nước", 49.8), ("Điện tử, trong nước", 50.2), ("Hồng ngoại → mặt nước", 48.4),
        ("Hồng ngoại → thành cốc", 47.1), ("Hồng ngoại → giấy bạc", 41.0)]


def fmt(x): return f"{x:.1f}".replace(".", ",")


def dashed(d, p1, p2, color, w=3, dash=12, gap=9):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))],
               fill=color, width=w)


# ---------------- hinh ve ----------------
def cup(d):
    cream, edge = (246, 240, 228), (150, 140, 120)
    d.arc([CUP_L - 90, 610, CUP_L + 30, 800], 90, 270, fill=edge, width=18)          # quai coc
    d.arc([CUP_L - 90, 610, CUP_L + 30, 800], 90, 270, fill=cream, width=10)
    d.rectangle([CUP_L + WALL, WATER_Y, CUP_R - WALL, CUP_B - 24], fill=(191, 219, 254))   # nuoc (mat cat)
    d.line([(CUP_L + WALL, WATER_Y), (CUP_R - WALL, WATER_Y)], fill=BLUE, width=4)
    for box in ((CUP_L, CUP_T, CUP_L + WALL, CUP_B), (CUP_R - WALL, CUP_T, CUP_R, CUP_B), (CUP_L, CUP_B - 24, CUP_R, CUP_B)):
        d.rectangle(box, fill=cream, outline=edge, width=3)
    text(d, (150, 560), "nước ≈ 50 °C", 34, BLUE)


def foil(d):
    x0, y0, x1, y1 = FOIL
    d.rectangle([x0, y0, x1, y1], fill=(196, 202, 214), outline=(120, 128, 145), width=2)
    for k in range(5):
        y = y0 + 12 + k * 20; d.line([(x0 + 2, y + 8), (x1 - 2, y)], fill=WHITE, width=2)
    text(d, (FOIL[2] + 14, 846), "giấy bạc", 32, MUTED, bold=False, anchor="lm")
    d.line([(FOIL[2] + 2, 802), (FOIL[2] + 40, 826)], fill=MUTED, width=2)


def thermo(d, level):
    """Nhiet ke thuy ngan nhung trong nuoc; level 0..1 = chieu cao cot."""
    d.rounded_rectangle([TH_X - 12, 360, TH_X + 12, 828], radius=12, fill=WHITE, outline=NAVY, width=3)
    dot(d, TH_X, 836, 19, (170, 176, 190), outline=NAVY)
    top = lerp(800, 470, level)
    d.rectangle([TH_X - 5, top, TH_X + 5, 830], fill=(150, 156, 172))
    for k in range(9):
        y = 470 + k * 40; d.line([(TH_X + 4, y), (TH_X + 12, y)], fill=NAVY, width=2)
    text(d, (TH_X - 25, 334), "thuỷ ngân", 32, MUTED, bold=False)


def probe(d):
    d.rounded_rectangle([PR_X - 36, 352, PR_X + 36, 430], radius=12, fill=NAVY)
    d.rounded_rectangle([PR_X - 24, 364, PR_X + 24, 396], radius=6, fill=(160, 220, 200))
    d.line([(PR_X, 430), (PR_X, 828)], fill=(120, 128, 145), width=7)
    dot(d, PR_X, 830, 6, NAVY)
    text(d, (PR_X + 30, 334), "điện tử", 32, MUTED, bold=False)


def gun(d, pose, beam=1.0):
    nx, ny, ang, tgt, kind, r = pose
    a = math.radians(ang); u = (math.cos(a), -math.sin(a)); v = (-u[1], u[0])
    P = lambda x, y: (nx + x * u[0] + y * v[0], ny + x * u[1] + y * v[1])
    if tgt is not None and beam > 0:           # chum tia tu mieng may toi vet do
        tx, ty = tgt
        if kind == "v": e1, e2 = (tx, ty - r), (tx, ty + r)
        else: e1, e2 = (tx - r, ty), (tx + r, ty)
        d.polygon([P(0, -9), P(0, 9), e2, e1], fill=A(RED, 0.22 * beam))
        if kind == "v": d.ellipse([tx - 6, ty - r, tx + 6, ty + r], fill=A(RED, 0.55 * beam))
        else: d.ellipse([tx - r, ty - 6, tx + r, ty + 6], fill=A(RED, 0.55 * beam))
    hc = mix(TEAL, NAVY, 0.35)
    d.polygon([P(118, 26), P(154, 26), P(168, 128), P(130, 128)], fill=hc)
    d.polygon([P(0, -13), P(26, -22), P(26, 22), P(0, 13)], fill=NAVY)
    d.polygon([P(26, -30), P(176, -30), P(176, 30), P(26, 30)], fill=TEAL)
    d.polygon([P(128, -18), P(166, -18), P(166, 14), P(128, 14)], fill=(160, 220, 200))


def gun_pose_at(pa, pb, k):
    k = ease(k)
    if pb[3] is None: return pb
    return (lerp(pa[0], pb[0], k), lerp(pa[1], pb[1], k), lerp(pa[2], pb[2], k), pb[3], pb[4], lerp(pa[5] if pa[5] else pb[5], pb[5], k))


def readouts(d, vals, hl=-1, alpha=1.0):
    names = ("Thuỷ ngân", "Điện tử", "Hồng ngoại"); subs = ("sai số ±0,5", "sai số ±0,2", "ε đặt sẵn 0,95")
    cols = (NAVY, NAVY, ORANGE)
    for j in range(3):
        x0 = 60 + j * 330; box = (x0, RD_Y, x0 + 300, RD_Y + 150)
        card(d, box, fill=A(WHITE, alpha), outline=A(ORANGE if j == hl else LIGHT, alpha), w=5 if j == hl else 3, r=24)
        text(d, (x0 + 150, RD_Y + 30), names[j], 32, MUTED, alpha=alpha)
        s = "—" if vals[j] is None else fmt(vals[j]) + " °C"
        text(d, (x0 + 150, RD_Y + 80), s, 50, cols[j], alpha=alpha)
        text(d, (x0 + 150, RD_Y + 126), subs[j], 32, MUTED, bold=False, alpha=alpha)


def table(d, nrows, hl=-1, alpha=1.0):
    y = TAB_Y
    card(d, (60, y, 1020, y + 354), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    text(d, (100, y + 36), "Đo bằng → ở đâu", 32, MUTED, bold=False, anchor="lm", alpha=alpha)
    text(d, (880, y + 36), "Số đọc (°C)", 32, MUTED, bold=False, alpha=alpha)
    d.line([(90, y + 64), (990, y + 64)], fill=A(LIGHT, alpha), width=3)
    for j, (nm, val) in enumerate(ROWS[:nrows]):
        yy = y + 100 + j * 54
        if j == hl: d.rounded_rectangle([80, yy - 25, 1000, yy + 25], radius=14, fill=A(mix(ORANGE, WHITE, 0.85), alpha))
        text(d, (100, yy), nm, 36, INK, bold=False, anchor="lm", alpha=alpha)
        text(d, (880, yy), fmt(val), 40, ORANGE if j >= 2 else NAVY, alpha=alpha)


def apparatus(d, level, pose, beam=1.0, show_foil_label=True):
    cup(d); foil(d); thermo(d, level); probe(d); gun(d, pose, beam)


# ---------------- canh 1: mo dau + Du doan ----------------
def s_hook(img, d, t, sc):
    apparatus(d, 0.15, IDLE)
    text(d, (820, 700), "hồng ngoại", 32, MUTED, bold=False)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    if k <= 0: return
    y0 = TAB_Y - 60 + (1 - k) * 40
    card(d, (60, y0, 1020, y0 + 420), fill=A(WHITE, k), outline=A(PURPLE, k), w=5)
    t1, t2 = sc["M"][1] + 0.4, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))     # thanh dem thoi gian nghi
    d.rounded_rectangle([140, y0 + 396, 940, y0 + 406], radius=5, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, y0 + 396, 140 + 800 * (1 - q), y0 + 406], radius=5, fill=A(PURPLE, k))
    text(d, (W / 2, y0 + 44), "Dự đoán", 40, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 100), "Bắn hồng ngoại vào mảnh GIẤY BẠC", 38, INK, alpha=k)
    text(d, (W / 2, y0 + 148), "dán ngoài cốc. Số đọc sẽ…", 38, INK, alpha=k)
    for j, s in enumerate(("A.  gần bằng 50 °C", "B.  thấp hơn hẳn 50 °C", "C.  cao hơn hẳn 50 °C")):
        yy = y0 + 214 + j * 58
        d.rounded_rectangle([110, yy - 24, 970, yy + 24], radius=24, outline=A(LIGHT, k), width=3)
        text(d, (140, yy), s, 36, NAVY, bold=False, anchor="lm", alpha=k)


# ---------------- canh 2: tien hanh ----------------
def chips(d, cur):
    names = ("1. Nhúng", "2. Mặt nước", "3. Thành cốc", "4. Giấy bạc")
    for j, s in enumerate(names):
        x0 = 60 + j * 245; box = (x0, 236, x0 + 225, 302)
        if j == cur: card(d, box, fill=ORANGE, r=33); text(d, (x0 + 112, 269), s, 32, WHITE)
        elif j < cur: card(d, box, fill=LIGHT, r=33); text(d, (x0 + 112, 269), s, 32, INK)
        else: card(d, box, fill=None, outline=LIGHT, r=33, w=3); text(d, (x0 + 112, 269), s, 32, GRAY)


POSES = [IDLE, P_WATER, P_WALL, P_FOIL]
IRV = [None, 48.4, 47.1, 41.0]


def do_state(t, sc):
    M = sc["M"]; cur = cur_cap(sc, t)
    level = lerp(0.15, 0.9, ease((t - M[0] - 0.3) / 1.2))
    contact = (49.8, 50.2) if t > M[0] + 1.6 else (None, None)
    pose, ir, nrows, beam = IDLE, None, 2 if t > M[0] + 1.6 else 0, 0.0
    for s in (1, 2, 3):
        if cur < s: break
        u = t - M[s]
        pose = gun_pose_at(POSES[s - 1], POSES[s], u / 0.8)
        beam = appear(u, 0.8, 0.3)
        if u > 1.2: ir = IRV[s]; nrows = 2 + s
        else: ir = IRV[s - 1]; nrows = 1 + s if s > 1 else 2
    return level, contact, pose, ir, nrows, beam


def s_do(img, d, t, sc):
    cur = cur_cap(sc, t)
    level, contact, pose, ir, nrows, beam = do_state(t, sc)
    chips(d, cur)
    apparatus(d, level, pose, beam)
    if pose[3] is not None and beam > 0.5:
        tx, ty = pose[3]; mx, my = (pose[0] + tx) / 2, (pose[1] + ty) / 2
        text(d, (mx + (26 if pose[4] == "h" else 0), my - (0 if pose[4] == "h" else 52)), "5 cm", 32, RED, anchor="lm" if pose[4] == "h" else "mm", alpha=beam)
    readouts(d, (contact[0], contact[1], ir), hl=2 if cur >= 1 else -1)
    table(d, nrows, hl=nrows - 1 if nrows > 2 else -1)
    ka = appear(t, sc["M"][3] + 1.4, 0.4)
    if ka > 0:
        pw = tw(d, "ĐÁP ÁN B", F(34)) + 48
        card(d, (1020 - pw, 336, 1020, 394), fill=A(GREEN, ka), r=29)
        text(d, (1020 - pw / 2, 365), "ĐÁP ÁN B", 34, WHITE, alpha=ka)


# ---------------- canh 3: rut ra ----------------
def chart(d, t, sc):
    card(d, (60, 236, 1020, 800), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 276), "Cùng một cốc nước, năm số đọc", 36, MUTED)
    x0, x1, v0, v1 = 470, 980, 38.0, 52.0
    X = lambda v: x0 + (v - v0) / (v1 - v0) * (x1 - x0)
    ay = 716
    d.line([(x0, ay), (x1, ay)], fill=NAVY, width=4)
    for v in range(38, 53, 2):
        d.line([(X(v), ay - 8), (X(v), ay + 8)], fill=NAVY, width=3)
        text(d, (X(v), ay + 32), str(v), 32, MUTED, bold=False)
    text(d, (x1, ay - 30), "°C", 32, MUTED, bold=False, anchor="rm")
    dashed(d, (X(50), 316), (X(50), ay - 10), A(GREEN, 0.9), w=4)
    text(d, (X(50) - 10, 330), "nước 50", 32, GREEN, anchor="rm")
    errs = (0.5, 0.2, 0, 0, 0)
    for j, (nm, val) in enumerate(ROWS):
        k = appear(t, sc["M"][0] + 0.15 * j - 0.2, 0.35)
        if k <= 0: continue
        y = 380 + j * 66; col = NAVY if j < 2 else ORANGE
        lab = nm.replace("Hồng ngoại → ", "HN: ").replace(", trong nước", "")
        text(d, (100, y), lab, 34, INK, bold=False, anchor="lm", alpha=k)
        if errs[j]: d.line([(X(val - errs[j]), y), (X(val + errs[j]), y)], fill=A(col, 0.6 * k), width=4)
        dot(d, X(val), y, 12 * k, col, outline=WHITE)
        text(d, (X(val) - 22, y), fmt(val), 32, col, anchor="rm", alpha=k)


def kcard(d, y, title, ev, color, k, h=160):
    if k <= 0: return
    yy = y + (1 - k) * 30
    card(d, (60, yy, 1020, yy + h), fill=A(WHITE, k), outline=A(color, k), w=5)
    text(d, (W / 2, yy + 50), title, 42, color, alpha=k)
    text(d, (W / 2, yy + h - 40), ev, 34, MUTED, bold=False, alpha=k)


def s_rut(img, d, t, sc):
    chart(d, t, sc)
    kcard(d, 830, "Tiếp xúc: đo đúng chỗ nó chạm vào", "49,8 và 50,2 °C: lệch trong sai số ±0,5", GREEN,
          appear(t, sc["M"][0] + 0.6, 0.45))
    kcard(d, 1010, "Hồng ngoại: đo bề mặt qua bức xạ", "mặt nước bay hơi nên nguội hơn: 48,4 °C", ORANGE,
          appear(t, sc["M"][1], 0.45))
    kcard(d, 1190, "Mặt bóng phát xạ yếu → số thấp giả", "giấy bạc ε ≈ 0,02–0,10, máy đặt 0,95", PURPLE,
          appear(t, sc["M"][2], 0.45))


# ---------------- canh 4: cai bay + sai so + gioi han ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    u = t - M[1]
    pose = gun_pose_at(P_FOIL, P_FOIL25, (u - 0.4) / 1.2) if u > 0 else P_FOIL
    apparatus(d, 0.9, pose, 1.0)
    ir = 38.5 if u > 1.8 else 41.0
    lab = "25 cm" if u > 1.0 else "5 cm"
    tx, ty = pose[3]; text(d, ((pose[0] + tx) / 2, ty - (100 if u > 1.0 else 52)), lab, 32, RED)
    readouts(d, (49.8, 50.2, ir), hl=2)
    k1 = appear(t, 0.3, 0.45); k2 = appear(t, M[1] - 0.1, 0.45); k3 = appear(t, M[2] - 0.1, 0.45)
    a1 = k1 * (1 - k2); a2 = k2 * (1 - k3)
    y = TAB_Y
    if a1 > 0:
        card(d, (60, y, 1020, y + 300), fill=A(WHITE, a1), outline=A(RED, a1), w=5)
        text(d, (W / 2, y + 46), "Cái bẫy", 42, RED, alpha=a1)
        text(d, (W / 2, y + 108), "“Hồng ngoại chính xác hơn” → SAI.", 38, INK, alpha=a1)
        text(d, (W / 2, y + 158), "Giấy bạc ấm như thành cốc vẫn ra 41,0", 36, INK, bold=False, alpha=a1)
        text(d, (W / 2, y + 236), "Số đọc phụ thuộc cả loại bề mặt", 36, GREEN, alpha=a1)
    if a2 > 0:
        card(d, (60, y, 1020, y + 300), fill=A(WHITE, a2), outline=A(ORANGE, a2), w=5)
        text(d, (W / 2, y + 46), "Sai số hay gặp", 42, ORANGE, alpha=a2)
        text(d, (W / 2, y + 108), "Lùi xa: vết đo rộng, tràn ra ngoài", 36, INK, bold=False, alpha=a2)
        text(d, (W / 2, y + 158), "giấy bạc, hứng thêm bức xạ nền của phòng", 36, INK, bold=False, alpha=a2)
        text(d, (W / 2, y + 236), "So sánh: cùng chỗ, cùng khoảng cách", 36, GREEN, alpha=a2)
    if k3 > 0:
        card(d, (60, y, 1020, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, y + 46), "Thí nghiệm chưa nói được", 40, NAVY, alpha=k3)
        for j, s in enumerate(("• Nhiệt kế nào tốt hơn: mỗi cái đo", "  một chỗ khác nhau.",
                               "• Số liệu là minh hoạ, chưa phải số đo thật.")):
            text(d, (100, y + 112 + j * 56), s, 36, INK, bold=False, anchor="lm", alpha=k3)


# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Hồng ngoại đo bề mặt: mặt bóng cho số thấp giả",
             "Giấy bạc ấm như thành cốc. Vì sao máy hồng ngoại chỉ 41,0 °C?",
             "So độ phát xạ ε của giấy bạc\nvới số máy đặt sẵn (0,95)")


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][1], "tap"), (do["t0"] + do["M"][3] + 1.4, "ding"),
            (r["t0"] + r["M"][0], "tap"), (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]


CLIP = dict(id="tn-l12-thangnhietdo-04", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thang nhiệt độ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ba nhiệt kế, một cốc nước", draw=s_hook, tail=0.3, caps=[
   ("Cốc nước ấm khoảng 50 °C, ba nhiệt kế.", 2.9),
   ("Dự đoán trước, rồi xem tiếp.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Nhúng hai nhiệt kế vào nước, chờ ổn định.", 3.0),
   ("Hồng ngoại bắn mặt nước, cách 5 cm.", 3.0),
   ("Bắn vào thành cốc sứ.", 2.6),
   ("Bắn vào giấy bạc: 41,0 °C, đáp án B.", 3.4)]),
 dict(key="rut", title="Kết luận", draw=s_rut, tail=0.7, caps=[
   ("Tiếp xúc: đo đúng chỗ nó chạm vào.", 2.8),
   ("Hồng ngoại: đo bề mặt qua bức xạ.", 2.8),
   ("Giấy bạc phát xạ yếu nên số thấp giả.", 3.0)]),
 dict(key="bay", title="Bẫy và sai số", draw=s_bay, tail=0.4, caps=[
   ("Bẫy: 41,0 °C không phải nhiệt độ thật.", 3.0),
   ("Lùi ra 25 cm: chỉ còn 38,5 °C.", 3.2),
   ("Thí nghiệm này chưa nói được gì?", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.9, caps=[
   ("Thử nghĩ: vì sao giấy bạc chỉ 41,0 °C?", 4.4)]),
])
