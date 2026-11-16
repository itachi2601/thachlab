# Clip: tn-l12-tdhphantu-01 - Hat khoi trong hop kinh soi qua kinh hien vi (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-tdhphantu-01.json:
#   so_lieu_mau (minh hoa, thang 1-5): 10 °C -> 2 · 25 °C -> 3 · 40 °C -> 4 · 55 °C -> 5
#   tham_so: duong kinh hat khoi d mac dinh 1 µm, max 5 µm; T mac dinh 27 °C (clip dung hang 25 °C cua so_lieu_mau).
# Duong di Brown: buoc ngau nhien seed co dinh (random.Random(14 / 23)), moi khung re <= 50° (kiem bang ma), toc do
#   moi khung ti le muc nhay cua hang dang doc -> nhiet ke, hang to sang va toc do hat cung mot ham state().
# Du doan (K10: khong ve nut A-D trong mp4). Hop kin, khong gio; moi cham sang (hat khoi) chuyen dong the nao?
#   A. Dung yen, lo lung mot cho trong hop
#   B. Roi cham, thang xuong day hop
#   C. Nhay hon loan theo duong gap khuc      <- dap an
#   D. Cung troi deu ve mot phia cua hop
# Bay (hien_tuong_hay_sai 1): "hat nhay vi co luong gio" -> gio thi moi hat troi cung chieu; thay hai hat canh nhau
#   di hai kieu -> khong phai gio. KHONG dung bay "duong gap khuc = duong di phan tu": cau Tu kiem tra ngay sau hop
#   (Cau 1, y D) hoi dung y nay -> clip khong giai san.
# Chot THU NGHI: cung 25 °C, thay hat 1 µm bang hat 5 µm (tham_so d max) -> hat nhay YEU hon (mo_hinh.ghi_chu: hat nho
#   thi quy dao gap khuc ro hon; hat to nang hon, va dap cac phia bu tru nhieu hon). Goi y chi la du kien thay doi.
import random
from engine import *

ROWS = [(10, 2), (25, 3), (40, 4), (55, 5)]   # (nhiet do hop °C, muc nhay thang 1-5) - so_lieu_mau
DARK = (14, 18, 36)
P_COL = ((255, 236, 170), (170, 225, 255))      # hai hat khoi
NOTE = (70, 75, 95)

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=28):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.85, cx + wdt / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)

# ---------------- trang thai canh Tien hanh (mot ham cho nhiet ke, bang, toc do hat) ----------------
def row_times(sc):
    pb = sc["M"][1]
    return [pb + 0.3 + 0.95 * k for k in range(4)]

def state(t, sc):
    """-> (nhiet do dang doc, muc nhay, chi so hang dang to sang (-1: chua co bang))"""
    rt = row_times(sc); k = -1
    for i, x in enumerate(rt):
        if t >= x: k = i
    if k < 0: return 25, 3, -1
    return ROWS[k][0], ROWS[k][1], k

# ---------------- duong di Brown: buoc ngau nhien seed co dinh ----------------
MC, MR = (540, 600), 300                         # kinh hien vi: tam, ban kinh
_PATHS = {}
def brown_path(seed, start, speeds):
    R = random.Random(seed); x, y = start; h = R.uniform(0, 2 * math.pi)
    pts = [(x, y)]; turn_left = 0.0; seg = 0
    for v in speeds:
        if seg <= 0 and abs(turn_left) < 1e-6:
            seg = R.randint(3, 7)
            turn_left = math.radians(R.uniform(40, 150)) * (1 if R.random() < 0.5 else -1)
        dx, dy = x - MC[0], y - MC[1]
        if math.hypot(dx, dy) > MR - 70 and abs(turn_left) < 1e-6:     # gan mep: quay ve phia tam
            want = math.atan2(-dy, -dx); diff = (want - h + math.pi) % (2 * math.pi) - math.pi
            turn_left = diff
        st = max(-math.radians(50), min(math.radians(50), turn_left))
        h += st; turn_left -= st; seg -= 1
        x += v * math.cos(h); y += v * math.sin(h)
        r = math.hypot(x - MC[0], y - MC[1])
        if r > MR - 30:                                                   # chan cung (hiem): keo vao trong
            x = MC[0] + (x - MC[0]) * (MR - 30) / r; y = MC[1] + (y - MC[1]) * (MR - 30) / r
        pts.append((x, y))
    return pts

def paths(sc):
    key = (sc["key"], round(sc["T"], 3))
    if key not in _PATHS:
        n = int(sc["T"] * FPS) + 4
        sp = [1.9 * state(i / FPS, sc)[1] for i in range(n)]
        _PATHS[key] = (brown_path(14, (490, 590), sp), brown_path(23, (600, 630), sp))
    return _PATHS[key]

def max_turn_deg(pts):
    mx = 0
    for i in range(2, len(pts)):
        a1 = math.atan2(pts[i - 1][1] - pts[i - 2][1], pts[i - 1][0] - pts[i - 2][0])
        a2 = math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0])
        mx = max(mx, abs(math.degrees((a2 - a1 + math.pi) % (2 * math.pi) - math.pi)))
    return mx

def scope(d, t, sc, trail=50):
    d.ellipse([MC[0] - MR - 14, MC[1] - MR - 14, MC[0] + MR + 14, MC[1] + MR + 14], fill=(60, 64, 80))
    d.ellipse([MC[0] - MR, MC[1] - MR, MC[0] + MR, MC[1] + MR], fill=DARK)
    P = paths(sc); i = min(int(t * FPS), len(P[0]) - 1)
    for k, pts in enumerate(P):
        j0 = max(0, i - trail)
        for j in range(j0, i):
            a = 0.15 + 0.75 * (j - j0) / max(1, i - j0)
            d.line([pts[j], pts[j + 1]], fill=A(P_COL[k], a), width=4)
        x, y = pts[i]
        dot(d, x, y, 20, A(P_COL[k], 0.25)); dot(d, x, y, 11, P_COL[k])

# ---------------- canh 1: Du doan ----------------
def apparatus(d, t, y0=300):
    # nen toi + hop kinh + den roi ngang + kinh lup
    card(d, (300, y0, 1000, y0 + 470), fill=(30, 32, 44), r=18)
    bx0, by0, bx1, by1 = 400, y0 + 120, 860, y0 + 420
    d.rectangle([bx0, by0, bx1, by1], fill=(70, 76, 96), outline=(200, 214, 235), width=6)
    d.rectangle([bx0 - 12, by0 - 22, bx1 + 12, by0], fill=(200, 214, 235))          # nap day kin
    for k in range(7):                                                                # khoi mo (tinh)
        cx = bx0 + 70 + k * 55; cy = by0 + 110 + 40 * math.sin(k * 1.7)
        dot(d, cx, cy, 46, A((190, 195, 210), 0.18))
    # den pin ben trai, chum sang ngang qua hop
    d.rounded_rectangle([110, y0 + 230, 270, y0 + 300], radius=14, fill=(90, 96, 110))
    d.polygon([(270, y0 + 222), (300, y0 + 210), (300, y0 + 320), (270, y0 + 308)], fill=(120, 126, 140))
    d.polygon([(300, y0 + 230), (bx1, y0 + 215), (bx1, y0 + 315), (300, y0 + 300)], fill=A((255, 236, 150), 0.42))
    # kinh lup phia tren
    # kinh hien vi nhin xuong vung sang (thi kinh - than - vat kinh - tay can)
    MCOL = (215, 222, 236)
    d.rounded_rectangle([592, y0 - 44, 668, y0 - 20], radius=8, fill=MCOL)               # thi kinh
    d.rectangle([606, y0 - 20, 654, y0 + 70], fill=MCOL)                                    # ong kinh
    d.polygon([(612, y0 + 70), (648, y0 + 70), (640, y0 + 100), (620, y0 + 100)], fill=MCOL) # vat kinh
    d.line([(654, y0 + 10), (720, y0 + 10), (720, y0 + 60)], fill=MCOL, width=14)           # tay can
    text(d, (630, y0 + 520), "hộp kín", 44, NOTE)

def s_hook(img, d, t, sc):
    apparatus(d, t)
    pill(d, 800, 880, "hạt khói cỡ 1 µm", 44, INK, LIGHT, appear(t, 0.6, 0.5))
    a = appear(t, sc["M"][1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 980 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", 44, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 190), "Chấm sáng (hạt khói)", 48, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "chuyển động thế nào?", 48, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 410), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = sc["M"][1] + 0.6, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 490, 940, y0 + 502], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 490, 140 + 800 * (1 - p), y0 + 502], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
DBG = []
def s_do(img, d, t, sc):
    T, lv, k = state(t, sc)
    scope(d, t, sc)
    # the nhiet ke (goc phai tren)
    card(d, (800, 260, 1040, 400), fill=WHITE, outline=NAVY, w=4, r=22)
    text(d, (920, 300), "Hộp", 44, MUTED, bold=False)
    text(d, (920, 360), f"{T} °C", 52, ORANGE if T >= 40 else (BLUE if T <= 10 else INK))
    DBG.append((t, T, k, lv))
    # bang so lieu
    ka = appear(t, sc["M"][1], 0.4)
    if ka <= 0: return
    card(d, (40, 1000, 1040, 1600), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    text(d, (290, 1060), "Nhiệt độ hộp", 44, NOTE, bold=False, alpha=ka)
    text(d, (770, 1060), "Mức nhảy (1–5)", 44, NOTE, bold=False, alpha=ka)
    text(d, (1010, 1130), "Minh hoạ", 44, PURPLE, bold=False, anchor="rm", alpha=ka)
    d.line([(70, 1170), (1010, 1170)], fill=A(LIGHT, ka), width=3)
    rt = row_times(sc)
    for j, (Tj, lj) in enumerate(ROWS):
        yy = 1230 + 92 * j; kr = appear(t, rt[j], 0.3)
        if kr <= 0: continue
        if j == k: d.rounded_rectangle([70, yy - 40, 1010, yy + 40], radius=18, fill=A((255, 237, 213), kr))
        text(d, (290, yy), f"{Tj} °C", 48, INK, alpha=kr)
        text(d, (770, yy), str(lj), 48, ORANGE, alpha=kr)

# ---------------- canh 3: Dap an + co che ----------------
NM = 16
def hits(t):
    """phan tu khi lao vao hat theo huong ngau nhien (moi chu ki mot goc moi) -> vi tri va vecto va dap gan day"""
    out = []; net = [0.0, 0.0]
    for i in range(NM):
        per = 0.9 + 0.35 * ((i * 7) % 5) / 5; ph = i / NM
        u = t / per + ph; cyc = int(u); f = u - cyc
        R = random.Random(1000 * i + cyc); ang = R.uniform(0, 2 * math.pi)
        dist = abs(1 - 2 * f)                                  # 1 -> 0 (cham hat) -> 1
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
        mx, my = px + r * math.cos(ang), py + r * math.sin(ang)
        dot(d, mx, my, 12, A(BLUE, alpha))
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
    M = sc["M"]
    ka = appear(t, 0.2, 0.4)
    pill(d, W / 2, 300, "ĐÁP ÁN · Nhảy hỗn loạn, gấp khúc", 46, WHITE, NAVY, ka)
    card(d, (40, 370, 1040, 1080), fill=WHITE, outline=LIGHT, w=3)
    km = appear(t, M[0] - 0.1, 0.4)
    if km > 0:
        px, py = mech_pos(t, 540, 700)
        ex, ey = px - 95 * 0.72, py - 95 * 0.69                                  # gach noi nhan -> mep hat
        d.line([(170, 438), (ex, ey)], fill=A((160, 110, 30), km), width=4)   # ve TRUOC phan tu: cham phan tu de len, khong bi cat
        mech(d, t, 540, 700, km)
        dot(d, ex, ey, 7, A((160, 110, 30), km))
        text(d, (80, 410), "hạt khói", 44, (160, 110, 30), anchor="lm", alpha=km)
        text(d, (1000, 410), "phân tử (vẽ to)", 44, BLUE, anchor="rm", alpha=km)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        y = 1120 + (1 - k1) * 25
        card(d, (60, y, 1020, y + 260), fill=A(WHITE, k1), outline=A(GREEN, k1), w=6)
        text(d, (W / 2, y + 130), "Phân tử khí: hỗn loạn, không ngừng", 50, GREEN, alpha=k1)

# ---------------- canh 4: Chua noi duoc gi ----------------
def s_chua(img, d, t, sc):
    k = appear(t, 0.3, 0.45)
    card(d, (40, 300, 1040, 960), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 380), "Chưa nói được", 52, NAVY, alpha=k)
    items = (("• Không thấy phân tử,", "không đo tốc độ"), ("• Một hạt: chưa tách", "được dòng đối lưu"))
    for j, (l1, l2) in enumerate(items):
        kk = appear(t, 0.7 + 0.6 * j, 0.4); y = 540 + 260 * j
        text(d, (90, y), l1, 48, INK, anchor="lm", alpha=kk)
        text(d, (130, y + 70), l2, 48, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Bay ----------------
def mini_box(d, x0, y0, x1, y1, a):
    d.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=A(DARK, a))

def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[0] + 1.0
    card(d, (40, 250, 1040, 560), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, 310, "BẪY", 44, WHITE, RED)
    q = "“Hạt nhảy vì có luồng gió”"
    text(d, (W / 2, 420), q, 50, mix(INK, GRAY, clamp((t - mk) / 0.4)))
    ks = clamp((t - mk) / 0.4)
    if ks > 0:
        lw = tw(d, q, F(50)); d.line([(W / 2 - lw / 2, 422), (W / 2 - lw / 2 + lw * ks, 422)], fill=RED, width=6)
        text(d, (W / 2 + lw / 2 + 40, 420), "✗", 50, RED, alpha=ks)
    ka = appear(t, mk + 0.2, 0.45)
    if ka <= 0: return
    card(d, (40, 600, 1040, 1500), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    # trai: neu do gio -> moi hat troi cung chieu
    text(d, (290, 660), "Nếu do gió", 46, NOTE, alpha=ka)
    mini_box(d, 70, 710, 510, 1150, ka)
    for j, (x, y) in enumerate(((130, 790), (170, 930), (120, 1070), (260, 860), (240, 1010))):
        xx = 100 + (x - 100 + (t - mk) * 75) % 380                    # troi deu sang phai, ra mep phai thi mo roi vao lai
        fa = ka * clamp((xx - 100) / 40) * clamp((480 - xx) / 40)
        d.line([(xx - 70, y), (xx - 12, y)], fill=A(P_COL[0], 0.5 * fa), width=4)
        dot(d, xx, y, 10, A(P_COL[0], fa))
    arrow(d, (150, 1190), (430, 1190), A(TEAL, ka), w=8, head=24)
    text(d, (290, 1260), "trôi một phía", 44, TEAL, alpha=ka)
    # phai: thay trong hop -> hai hat canh nhau, hai duong gap khuc khac nhau
    text(d, (790, 660), "Thấy thật", 46, NOTE, alpha=ka)
    mini_box(d, 570, 710, 1010, 1150, ka)
    P = BAY_P
    i = min(len(P[0]) - 1, int(max(0, t - mk) * FPS))
    for k, pts in enumerate(P):
        j0 = max(0, i - 60)
        for j in range(j0, i):
            d.line([pts[j], pts[j + 1]], fill=A(P_COL[k], ka * (0.2 + 0.7 * (j - j0) / max(1, i - j0))), width=4)
        dot(d, pts[i][0], pts[i][1], 10, A(P_COL[k], ka))
    kc = appear(t, mk + 2.4, 0.45)
    text(d, (790, 1220), "✓", 64, GREEN, alpha=kc)
    text(d, (W / 2, 1400), "→ không phải một luồng gió chung", 50, GREEN, alpha=appear(t, mk + 2.6, 0.45))

def _bay_paths():
    global MC, MR
    mc, mr = MC, MR
    MC, MR = (790, 930), 190
    sp = [5.0] * 400
    P = (brown_path(31, (760, 910), sp), brown_path(47, (820, 950), sp))
    MC, MR = mc, mr
    return P
BAY_P = _bay_paths()

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
KH = [0.0]                                       # do hien goi y: hinh ha thap luc chua co goi y, truot len khi goi y hien
def _end_body(d, t, k):
    dy = 185 * (1 - KH[0]) - 15                  # sau khi truot len: nhan cach hop goi y >= 35 px
    for x, r, lab in ((380, 14, "1 µm"), (700, 70, "5 µm")):         # ti le ban kinh 1 : 5
        dot(d, x, 1110 + dy, r, A((240, 214, 150), k), outline=A(NAVY, k))
        text(d, (x, 1225 + dy), lab, 46, INK, alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]; KH[0] = appear(t, M[0] + 2.9, 0.5)
    chot_hoi(d, t, sc, "Phân tử khí đập → hạt khói nhảy",
             "Hạt 5 µm thay hạt 1 µm, cùng 25 °C: nhảy mạnh hơn hay yếu hơn?", None, body=_end_body)
    kh = appear(t, M[0] + 2.9, 0.5)              # goi y tre ~2,5 s sau cau hoi (cau hoi hien o M0+0,4)
    if kh > 0:
        card(d, (110, 1300, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1355), "Gợi ý", 44, INK, bold=False, alpha=kh)
        text(d, (W / 2, 1455), "Chỉ đổi cỡ hạt", 48, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, ch, b, e = sc["hook"], sc["do"], sc["ket"], sc["chua"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + 0.05, "ding")]
    out += [(do["t0"] + x, "tap") for x in row_times(do)]
    out += [(k["t0"] + 0.2, "ding"), (ch["t0"] + 0.3, "tap"), (b["t0"] + b["M"][0] + 1.0, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-tdhphantu-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thuyết động học phân tử · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hạt khói trong hộp kính", draw=s_hook, tail=0.3, caps=[
   ("Rọi đèn ngang qua hộp khói.", 3.4),
   ("Nghĩ trước khi xem.", 6.0)]),
 dict(key="do", title="Soi qua kính hiển vi", draw=s_do, tail=0.4, caps=[
   ("Hai chấm cạnh nhau, khác đường.", 3.4),
   ("Đổi nhiệt độ, ghi mức nhảy.", 3.5),
   ("Ấm hơn, nhảy mạnh hơn.", 2.8)]),
 dict(key="ket", title="Vì sao hạt nhảy?", draw=s_ket, tail=0.4, caps=[
   ("Phân tử khí đập vào hạt.", 3.0),
   ("Đập không đều: hạt bị đẩy.", 3.0)]),
 dict(key="chua", title="Giới hạn của thí nghiệm", draw=s_chua, tail=0.3, caps=[
   ("Hai giới hạn.", 5.4)]),
 dict(key="bay", title="Cái bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Nếu do gió thì sao?", 3.0),
   ("Hai hạt, hai đường.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Tự trả lời trước.", 6.6)]),
])
