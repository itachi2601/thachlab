# Clip: tn-l12-nllk-01 - Hai nam cham vong day nhau va chiec dai giu chung lai (28/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-nllk-01.json:
#   so_lieu_mau: khong dai, tha tu do -> 18 mm (lo lung) ; khong dai, ep sat roi tha -> 18 mm (bat ve) ;
#                co dai siet -> 5 mm (ep sat, ca cum dung yen).  Ghi chu: nam cham 12 g, duong kinh ngoai 25 mm.
# Canh: Du doan (4 lua chon cung kieu) -> Tien hanh (tha / ep roi tha / siet dai trong MOT canh, do thi d(t))
#       -> Dap an B + bang so lieu + lien he hat nhan -> Bay (luc dien/hap dan giu proton) + chua noi duoc
#       -> Chot + cau hoi tu nho lai (heli).
# Hinh: hai vong cung cuc N quay vao nhau -> day nhau; cap luc day la luc truc doi (cung do lon, nguoc chieu, dat vao hai vat).
from engine import *

# ---------------- bo cuc (khung 1080x1920) ----------------
S = 12                                # px / mm (chi de ve d dung ti le; duong kinh 25 mm -> 300 px)
RX, RW, RH = 360, 300, 84             # truc que, be rong vong (25 mm), be day vong (ve, khong ghi so)
BASE_Y = 880                          # mat de go
LOW_TOP = BASE_Y - RH                 # mat tren vong duoi
DG = (22, 120, 60)                    # xanh dam: dai
D_EQ, D_BAND = 18, 5                  # so_lieu_mau (mm)
AX = 590                              # cot mui ten luc

def up_bot(dmm): return LOW_TOP - dmm * S          # y mat duoi vong tren

def chevron(d, x, y, ang, color, s=14, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def dashed(d, p, q, color, w=3, seg=12, gap=9):
    L = math.dist(p, q); n = int(L // (seg + gap)) + 1
    for k in range(n):
        a = k * (seg + gap) / L; b = min(1, (k * (seg + gap) + seg) / L)
        if a >= 1: break
        d.line([(lerp(p[0], q[0], a), lerp(p[1], q[1], a)), (lerp(p[0], q[0], b), lerp(p[1], q[1], b))], fill=color, width=w)

# ---------------- thiet bi ----------------
def stand(d):
    d.rounded_rectangle([RX - 7, 300, RX + 7, BASE_Y], radius=6, fill=(170, 175, 190))
    d.rounded_rectangle([150, BASE_Y, 570, BASE_Y + 46], radius=10, fill=(176, 124, 74))
    text(d, (360, BASE_Y + 23), "đế gỗ", 32, WHITE)

def ring(d, ybot, top_pole):
    """Vong nam cham nhin ngang: nua tren / nua duoi la hai mat cuc; que xuyen qua lo (net dut)."""
    x0, x1, ym = RX - RW // 2, RX + RW // 2, ybot - RH // 2
    ct, cb = (RED, BLUE) if top_pole == "N" else (BLUE, RED)
    lt, lb = (("N", "S") if top_pole == "N" else ("S", "N"))
    d.rounded_rectangle([x0, ybot - RH, x1, ym + 6], radius=10, fill=ct)
    d.rounded_rectangle([x0, ym - 6, x1, ybot], radius=10, fill=cb)
    d.rectangle([x0, ym - 6, x1, ym], fill=ct); d.rectangle([x0, ym, x1, ym + 6], fill=cb)
    for xx in (RX - 18, RX + 18): dashed(d, (xx, ybot - RH + 4), (xx, ybot - 4), A(WHITE, 0.85), w=3, seg=8, gap=6)
    for xx in (x0 + 60, x1 - 60):
        text(d, (xx, ybot - RH * 3 // 4 + 1), lt, 34, WHITE); text(d, (xx, ybot - RH // 4 + 1), lb, 34, WHITE)

def bracket(d, dmm, label=True):
    ya, yb = up_bot(dmm), LOW_TOP
    if yb - ya < 10: return
    x = 150
    d.line([(x, ya), (x, yb)], fill=INK, width=4)
    for yy in (ya, yb): d.line([(x - 14, yy), (x + 14, yy)], fill=INK, width=4)
    if label and dmm in (D_EQ, D_BAND): text(d, (x - 22, (ya + yb) / 2), f"{dmm} mm", 36, INK, anchor="rm")

def strap(d, dmm, alpha):
    if alpha <= 0.02: return
    c = A((22, 120, 60), alpha); top = up_bot(dmm) - RH - 10
    x0, x1 = RX - RW // 2 - 16, RX + RW // 2 + 16
    for xx in (x0, x1): d.rounded_rectangle([xx - 7, top, xx + 7, BASE_Y - 2], radius=6, fill=c)
    d.line([(x0, top + 4), (RX - 22, top + 4)], fill=c, width=12); d.line([(RX + 22, top + 4), (x1, top + 4)], fill=c, width=12)

def forces(d, dmm, mode, alpha=1.0):
    """'free': vong tren F day (goc o mat duoi, len) = P (goc o tam, xuong); vong duoi F day (goc o mat tren, xuong).
       Cap F day la luc truc doi: dai bang nhau. 'band': F day lon hon (gan hon); dai keo vong tren xuong, vong duoi len."""
    if alpha <= 0.02: return
    yb_u = up_bot(dmm); yt_u = yb_u - RH; yU = yb_u - RH / 2
    L = 100 if mode == "free" else 150
    for yy in (yb_u, LOW_TOP): dashed(d, (RX + RW // 2 + 6, yy), (AX - 6, yy), A(RED, 0.55 * alpha), w=3, seg=8, gap=6)
    arrow(d, (AX, yb_u), (AX, yb_u - L), A(RED, alpha), w=7)
    text(d, (AX + 18, yb_u - L + 12), "F đẩy", 36, RED, anchor="lm", alpha=alpha)
    arrow(d, (AX, LOW_TOP), (AX, LOW_TOP + L), A(RED, alpha), w=7)
    text(d, (AX + 18, LOW_TOP + L - 12), "F đẩy", 36, RED, anchor="lm", alpha=alpha)
    if mode == "free":
        arrow(d, (AX + 60, yU), (AX + 60, yU + L), A(BLUE, alpha), w=7)
        text(d, (AX + 80, yU + L - 14), "P", 38, BLUE, anchor="lm", alpha=alpha)
    else:
        arrow(d, (AX + 60, yt_u), (AX + 60, yt_u + L), A(DG, alpha), w=7)
        text(d, (AX + 80, yt_u + 24), "đai", 36, DG, anchor="lm", alpha=alpha)
        arrow(d, (AX + 120, BASE_Y), (AX + 120, BASE_Y - L), A(DG, alpha), w=7)
        text(d, (AX + 140, BASE_Y - 24), "đai", 36, DG, anchor="lm", alpha=alpha)

def readout(d, dmm_txt, state, scol=INK, note=None):
    card(d, (770, 330, 1040, 700), fill=WHITE, outline=LIGHT, r=26, w=3)
    text(d, (905, 372), "khoảng cách d", 34, INK)
    text(d, (905, 446), dmm_txt, 60, INK)
    f = F(34); yy = 524
    for l in wrap(d, state, f, 240):
        dtext(d, (905, yy), l, f, scol); yy += 44
    if note:
        f2 = F(32, False); yy += 8
        for l in wrap(d, note, f2, 240):
            dtext(d, (905, yy), l, f2, INK); yy += 40

def apparatus(d, dmm, band=0.0, push=False):
    stand(d)
    strap_alpha = band
    ring(d, BASE_Y, "N")                      # vong duoi: mat tren N
    ring(d, up_bot(dmm), "S")                 # vong tren: mat duoi N (N doi N)
    strap(d, dmm, strap_alpha)
    if push:
        yt = up_bot(dmm) - RH
        arrow(d, (RX + 90, yt - 120), (RX + 90, yt - 12), MUTED, w=8, head=24)
        text(d, (RX + 120, yt - 90), "tay ép xuống", 34, INK, anchor="lm")

# ---------------- canh 1: Du doan ----------------
OPTS = ("dính luôn vào vòng dưới, nằm yên",
        "bật lên, rồi lơ lửng cách vòng dưới",
        "bay vọt khỏi đầu que, rơi ra ngoài",
        "trượt dần xuống, nằm sát vòng dưới")

def s_hook(img, d, t, sc):
    apparatus(d, 2, push=True)
    text(d, (905, 560), "hai mặt N", 36, INK); text(d, (905, 606), "quay vào nhau", 34, INK, bold=False)
    M = sc["M"]; a = appear(t, M[1] - 0.2, 0.5)
    kd = appear(t, 0.5, 0.5) * (1 - a)
    if kd > 0.02:
        card(d, (50, 1000, 1030, 1560), fill=A(WHITE, kd), outline=A(LIGHT, kd), w=4)
        text(d, (W / 2, 1060), "Dụng cụ", 42, NAVY, alpha=kd)
        for j, s in enumerate(("• 2 nam châm vòng, cùng cực đối nhau", "• que thẳng đứng cắm trên đế gỗ",
                               "• đai nhựa (dùng ở bước sau)")):
            text(d, (100, 1160 + j * 100), s, 40, INK, anchor="lm", alpha=kd * appear(t, 0.7 + 0.3 * j, 0.4))
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    text(d, (W / 2, y0 + 140), "Ép sát hai vòng rồi buông tay.", 40, INK, alpha=a)
    text(d, (W / 2, y0 + 192), "Không có đai, vòng trên sẽ…", 40, INK, alpha=a)
    for j, s in enumerate(OPTS):
        k = appear(t, M[1] + 0.15 * j, 0.4); yy = y0 + 270 + j * 76
        d.rounded_rectangle([90, yy - 30, 990, yy + 30], radius=30, outline=A(LIGHT, k), width=3)
        text(d, (120, yy), f"{'ABCD'[j]}.  {s}", 36, NAVY, bold=False, anchor="lm", alpha=k)
    tc, tend = M[1] + 0.8, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 572, 940, y0 + 584], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 572, 140 + 800 * (1 - p), y0 + 584], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (mo hinh d theo "u", truc thoi gian so do) ----------------
U = (0.04, 0.30, 0.36, 0.42, 0.66, 0.74, 0.84)   # tha / on dinh / bat dau ep / buong / on dinh / bat dau siet / siet xong
D_HI, D_LO = 30, 2                                # vi tri tay giu ban dau / ep sat (chi de ve, khong ghi so)

def damp(s, a0):
    return D_EQ + a0 * math.exp(-5.5 * s) * math.cos(2 * math.pi * 2.2 * s)

def d_of(u):
    a, b, c, e, f, g, h = U
    if u < a: return D_HI
    if u < c: return damp((u - a) / (b - a), D_HI - D_EQ) if u < b else D_EQ
    if u < e: return lerp(D_EQ, D_LO, ease((u - c) / (e - c)))
    if u < f: return damp((u - e) / (f - e), D_LO - D_EQ)
    if u < g: return D_EQ
    if u < h: return lerp(D_EQ, D_BAND, ease((u - g) / (h - g)))
    return D_BAND

def u_of(t, sc):
    M = sc["M"]
    return float(np.interp(t, [M[0] + 0.2, M[0] + 0.5, M[0] + 2.9, M[1] + 0.1, M[1] + 0.7, M[1] + 2.4,
                               M[2] + 0.4, M[2] + 1.6, sc["T"] - 0.3],
                           [0, U[0], U[1], U[2], U[3], U[4], U[5], U[6], 1.0]))

def chips(d, cur):
    for j, s in enumerate(("1. Thả tự do", "2. Ép rồi thả", "3. Siết đai")):
        x0 = 60 + j * 330; box = (x0, 240, x0 + 300, 296)
        if j == cur: card(d, box, fill=ORANGE, r=28); text(d, (x0 + 150, 268), s, 32, WHITE)
        elif j < cur: card(d, box, fill=LIGHT, r=28); text(d, (x0 + 150, 268), s, 32, INK)
        else: card(d, box, fill=None, outline=LIGHT, r=28, w=3); text(d, (x0 + 150, 268), s, 32, MUTED)

def plot(d, box, u):
    x0, y0, x1, y1 = box
    X = lambda uu: x0 + uu * (x1 - x0)
    yb, yt = y1 - 70, y0 + 60
    Y = lambda v: yb - v / 32 * (yb - yt)
    d.line([(x0, yt - 20), (x0, yb)], fill=NAVY, width=4); chevron(d, x0, yt - 20, -math.pi / 2, NAVY, s=16)
    d.line([(x0, yb), (x1 + 14, yb)], fill=NAVY, width=4); chevron(d, x1 + 14, yb, 0, NAVY, s=16)
    text(d, (x0 + 20, yt - 16), "d (mm)", 32, INK, anchor="lm"); text(d, (x1 + 10, yb + 36), "t", 32, INK, anchor="rm")
    text(d, (x0 - 14, yb), "0", 32, INK, bold=False, anchor="rm")
    for v, col in ((D_EQ, GREEN), (D_BAND, (22, 120, 60))):
        dashed(d, (x0, Y(v)), (x1, Y(v)), A(col, 0.7), w=3)
        text(d, (x0 - 14, Y(v)), str(v), 34, col, anchor="rm")
    for uu, lab in (((U[0] + U[2]) / 2, "thả"), ((U[2] + U[5]) / 2, "ép rồi thả"), ((U[5] + 1) / 2, "siết đai")):
        text(d, (X(uu), y1 - 22), lab, 32, INK, bold=False)
    if u > 0:
        us = [k / 500 * u for k in range(501)]
        d.line([(X(v), Y(d_of(v))) for v in us], fill=ORANGE, width=7, joint="curve")
        if u < 0.999: dot(d, X(u), Y(d_of(u)), 12, RED, outline=WHITE)

def s_do(img, d, t, sc):
    u = u_of(t, sc); dm = d_of(u)
    a, b, c, e, f, g, h = U
    band = clamp((u - g) / 0.04)
    if u < a: st, txt, col = "tay giữ vòng trên", "", MUTED
    elif u < b: st, txt, col = "dao động dọc que", "", ORANGE
    elif u < c: st, txt, col = "lơ lửng, cân bằng trọng lượng", "18 mm", GREEN
    elif u < e: st, txt, col = "tay ép sát", "", MUTED
    elif u < f: st, txt, col = "bật lên", "", ORANGE
    elif u < g: st, txt, col = "bật về khoảng cách cân bằng", "18 mm", GREEN
    elif u < h: st, txt, col = "đai siết lại", "", ORANGE
    else: st, txt, col = "ép sát, cả cụm đứng yên", "5 mm", (22, 120, 60)
    chips(d, max(0, cur_cap(sc, t)))
    apparatus(d, dm, band=band, push=(c <= u < e))
    settled = txt != ""
    if settled: bracket(d, int(txt.split()[0]))
    forces(d, dm, "band" if u >= h else "free", alpha=1.0 if settled else 0.0)
    readout(d, txt if txt else "…", st, col, note="P nhỏ so với F, không vẽ" if u >= h else None)
    card(d, (40, 995, 1040, 1610), fill=WHITE, outline=LIGHT, w=3)
    plot(d, (210, 1020, 960, 1600), u)

# ---------------- canh 3: Dap an + rut ra ----------------
ROWS = [("Thả tự do", 18, "lơ lửng"), ("Ép sát rồi thả", 18, "bật về"), ("Có đai siết", 5, "đứng yên")]   # so_lieu_mau

def proton(d, x, y, r, alpha=1.0):
    dot(d, x, y, r, A(RED, alpha), outline=A(WHITE, alpha))
    text(d, (x, y + 2), "p⁺", 36, WHITE, alpha=alpha)

def nucleus_pair(d, cx, cy, alpha, strong=True, grav=False):
    """Hai proton (tam cach nhau 340 px). Vecto dat goc o tam proton chiu luc.
       Do (tren) = luc dien day ra; xanh (duoi, cung do cao) = luc hat nhan, moi proton bi hut ve proton kia, dai hon do.
       Hai vecto cung mau la mot cap luc truc doi. Xam = hap dan rat nho."""
    xl, xr = cx - 170, cx + 170
    proton(d, xl, cy, 46, alpha); proton(d, xr, cy, 46, alpha)
    for x, sg in ((xl, -1), (xr, 1)):
        d.line([(x, cy - 46), (x, cy - 75)], fill=A(RED, 0.5 * alpha), width=3)
        arrow(d, (x, cy - 75), (x + sg * 105, cy - 75), A(RED, alpha), w=7)
        if strong or grav:
            col = GREEN if strong else MUTED
            d.line([(x, cy + 46), (x, cy + 75)], fill=A(col, 0.5 * alpha), width=3)
            if strong: arrow(d, (x, cy + 75), (x - sg * 150, cy + 75), A(GREEN, alpha), w=7)
            else: arrow(d, (x, cy + 75), (x - sg * 36, cy + 75), A(MUTED, alpha), w=5, head=14)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, M[0] + 0.1, 0.5)
    pw = tw(d, "ĐÁP ÁN B", F(36)) + 52
    card(d, (W / 2 - pw / 2, 248, W / 2 + pw / 2, 308), fill=A(NAVY, ka), r=30)
    text(d, (W / 2, 278), "ĐÁP ÁN B", 36, WHITE, alpha=ka)
    y = 330
    card(d, (40, y, 1040, y + 330), fill=WHITE, outline=LIGHT, w=3)
    for x, s, an in ((80, "Cấu hình", "lm"), (700, "d (mm)", "mm"), (900, "Trạng thái", "mm")):
        text(d, (x, y + 44), s, 34, INK, anchor=an)
    d.line([(70, y + 76), (1010, y + 76)], fill=LIGHT, width=3)
    for j, (nm, dm, st) in enumerate(ROWS):
        k = appear(t, M[0] + 0.3 + 0.25 * j, 0.4); yy = y + 128 + j * 66
        hl = j == 1
        if hl and k > 0: d.rounded_rectangle([60, yy - 30, 1020, yy + 30], radius=16, fill=A((237, 233, 254), k))
        col = (22, 120, 60) if dm == D_BAND else INK
        text(d, (80, yy), nm, 38, INK, anchor="lm", alpha=k)
        text(d, (700, yy), str(dm), 40, col, alpha=k)
        text(d, (900, yy), st, 36, col, bold=False, alpha=k)
    # co che: day nhau -> phai co luc giu
    k1 = appear(t, M[0] + 1.3, 0.5)
    card(d, (40, 690, 1040, 900), fill=A(WHITE, k1), outline=A(GREEN, k1), w=5)
    ctext(d, 750, "Thiếu lực giữ: hai vật đẩy nhau luôn tách ra", 38, INK, maxw=900, alpha=k1)
    ctext(d, 840, "Đai siết: vẫn đẩy nhau mà cả cụm đứng yên", 38, (22, 120, 60), maxw=900, alpha=k1)
    # lien he hat nhan
    k2 = appear(t, M[2] + 0.1, 0.5)
    card(d, (40, 930, 1040, 1610), fill=A(WHITE, k2), outline=A(NAVY, k2), w=5)
    text(d, (W / 2, 990), "Trong hạt nhân", 42, NAVY, alpha=k2)
    nucleus_pair(d, W / 2, 1180, k2)
    text(d, (W / 2 - 240, 1060), "đẩy tĩnh điện", 36, RED, alpha=k2)
    text(d, (W / 2 + 240, 1060), "đẩy tĩnh điện", 36, RED, alpha=k2)
    text(d, (W / 2, 1360), "lực hạt nhân: hút, mạnh hơn hẳn", 38, GREEN, alpha=k2)
    ctext(d, 1480, "Lực giữ các nuclôn không phải lực tĩnh điện", 38, INK, maxw=900, alpha=appear(t, M[2] + 0.8, 0.5))

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    # hinh minh hoa ngay tu dau canh
    card(d, (40, 250, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    nucleus_pair(d, W / 2, 520, 1.0, strong=False, grav=True)
    text(d, (W / 2 - 240, 400), "điện: đẩy", 36, RED); text(d, (W / 2 + 240, 400), "điện: đẩy", 36, RED)
    text(d, (W / 2, 650), "hấp dẫn: quá nhỏ", 36, INK)
    dashed(d, (120, 760), (960, 760), A(GRAY, 0.8), w=3)
    dot(d, 180, 760, 22, BLUE); text(d, (180, 762), "e", 30, WHITE)
    ctext(d, 860, "êlectron ở vỏ, cách rất xa hạt nhân", 36, INK, maxw=900)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 1000
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“Lực điện hay hấp dẫn giữ các prôtôn”"
        ks = clamp((t - 1.0) / 0.4)
        f = F(40); lw = tw(d, q, f); yy = y0 + 170
        text(d, (W / 2, yy), q, 40, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * a1), width=4)
        ctext(d, y0 + 300, "Sai: giữa hai prôtôn, lực điện chỉ đẩy.", 44, RED, maxw=900, alpha=a1 * appear(t, 1.3, 0.5))
        text(d, (W / 2, y0 + 420), "Hấp dẫn: quá nhỏ.", 42, INK, alpha=a1 * appear(t, 1.8, 0.5))
        text(d, (W / 2, y0 + 500), "Êlectron: ở ngoài vỏ, rất xa.", 42, INK, alpha=a1 * appear(t, 2.1, 0.5))
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 62), "Thí nghiệm chưa nói được", 42, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.2, 0.4)
        card(d, (70, y0 + 115, 1010, y0 + 345), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, y0 + 170), "Đai bó từ ngoài KHÁC lực hạt nhân", 42, RED, alpha=kk)
        text(d, (W / 2, y0 + 240), "Lực hạt nhân hút trực tiếp", 40, INK, alpha=kk)
        text(d, (W / 2, y0 + 296), "giữa các nuclôn sát nhau", 40, INK, alpha=kk)
        kk = k2 * appear(t, M[1] + 0.6, 0.4)
        text(d, (90, y0 + 420), "• 18 mm, 5 mm: chỉ là số minh hoạ", 40, INK, anchor="lm", alpha=kk)
        text(d, (90, y0 + 500), "• Chưa đo được độ lớn lực", 40, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def heli(d, t, k):
    """Hat nhan heli so do: 2 proton (do, p+) + 2 notron (xam, n), xep sat nhau."""
    if k <= 0.02: return
    cx, cy, r = W / 2, 1150, 40
    for (dx, dy, kind) in ((-38, -36, "n"), (38, 36, "n"), (38, -36, "p"), (-38, 36, "p")):
        x, y = cx + dx, cy + dy
        dot(d, x, y, r, A(RED if kind == "p" else GRAY, k), outline=A(WHITE, k))
        text(d, (x, y + 2), "p⁺" if kind == "p" else "n", 32, WHITE, alpha=k)
    text(d, (cx + 150, cy), "heli", 38, INK, anchor="lm", alpha=k)

def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Đẩy nhau mà vẫn đứng yên: phải có lực giữ lại",
             "Hạt nhân heli có 2 prôtôn đẩy nhau. Lực nào giữ chúng lại? Vì sao không phải lực điện?",
             "Hai prôtôn: lực điện hút hay đẩy?", body=heli)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.3, "ding"),
            (do["t0"] + M[1] + 0.7, "tap"), (do["t0"] + M[2] + 0.4, "tap"),
            (da["t0"] + da["M"][0] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-nllk-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Năng lượng liên kết hạt nhân · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai nam châm vòng trên một que", draw=s_hook, tail=0.8, caps=[
   ("Hai vòng nam châm, mặt N quay vào nhau.", 3.0),
   ("Ép sát hai vòng rồi buông tay ra.", 3.2),
   ("Dừng lại vài giây, chọn A, B, C hay D.", 3.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Thả tự do: đo khoảng cách d.", 3.6),
   ("Ép sát rồi thả: vòng trên bật về 18 mm.", 3.8),
   ("Siết đai: hai vòng chỉ còn cách 5 mm.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Ép sát vẫn bật về. Đáp án B.", 2.8),
   ("Không có gì giữ, hai vòng luôn tách ra.", 3.2),
   ("Hạt nhân: lực hạt nhân giữ các prôtôn.", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: tưởng lực điện giữ được prôtôn.", 3.8),
   ("Thí nghiệm này chưa nói được gì?", 4.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Thử nghĩ: lực nào giữ 2 prôtôn của heli?", 4.4)]),
])
