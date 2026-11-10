# Clip: tn-l10-hieu-suat-01 - So vo quat ban sau khi chay (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-hieu-suat-01.json:
#   tham_so: P_tp = 45 W (minh hoa), H 30-90 % buoc 5 (mac dinh 65); cac_buoc: chay 10 phut, mu ban tay len vo dong co
#   roi chan de; quan_sat: vo dong co am hon chan de ro ret, tieng u nhe.
#   so_lieu_mau: H 40 / 65 / 90 % -> P_ci 18 / 29,25 / 40,5 W ; P_hp 27 / 15,75 / 4,5 W (so minh hoa, khong do that).
#   Cau chot dung H = 80 % (trong khoang tham_so, chua hien tren man): P_hp = 45 - 36 = 9 W -> 9 J moi giay.
# An toan (them so voi kho): tat quat, doi canh dung han roi moi so; khong ve tay gan canh dang quay hay o cam.
# Canh: Du doan (chi cau hoi + hinh, K10) -> Tien hanh (tat quat, so vo dong co roi chan de) -> Dap an + Sankey
#       (dien nang = co ich + hao phi, keo H 65 -> 40 -> 90) -> Bay + Chua noi duoc -> Chot + cau hoi tu tinh.
from engine import *

ROWS = {40: ("18", "27"), 65: ("29,25", "15,75"), 90: ("40,5", "4,5")}   # so_lieu_mau: H -> (P_ci, P_hp)
DRED = (185, 28, 28)
SKIN = (241, 200, 166); SKIN_D = (205, 150, 112)
METAL = (214, 218, 228); WARM = (253, 186, 140); BLADE = (96, 165, 250)
CX, CY, RX, RY = 380, 500, 140, 190          # long quat (nhin xien 3/4)

# ---------------- hinh quat ----------------
def fan(d, ang, spin, glow=0.0, press=False, hum=0.0, waves=0.0, t=0.0):
    # chan de + cong tac
    d.ellipse([480, 790, 800, 850], fill=METAL, outline=NAVY, width=4)
    card(d, (560, 808, 604, 834), fill=GRAY if press else RED, r=8)
    d.rectangle([628, 556, 652, 812], fill=METAL, outline=NAVY, width=3)          # than dung
    # vo dong co (sau long quat): am len thi ung cam
    if glow > 0:
        for r, a in ((60, 0.10), (38, 0.14), (18, 0.18)):
            d.rounded_rectangle([500 - r, 440 - r, 770 + r, 560 + r], radius=50 + r, fill=A(ORANGE, a * glow))
    d.rounded_rectangle([500, 440, 770, 560], radius=50, fill=mix(METAL, WARM, glow), outline=NAVY, width=4)
    for x in (690, 715, 740):
        d.line([(x, 470), (x, 530)], fill=NAVY, width=3)
    if hum > 0:                                                                   # tieng u nhe
        for r in (24, 44, 64):
            d.arc([790 - r, 500 - r, 790 + r, 500 + r], -40, 40, fill=A(MUTED, hum), width=4)
    if waves > 0:                                                                 # nhiet toa ra khong khi
        for j, x0 in enumerate((570, 640, 710)):
            pts = [(x0 + 12 * math.sin(2 * math.pi * (s / 40 - t * 0.8 + j * 0.3)), 425 - s) for s in range(0, 110, 6)]
            d.line(pts, fill=A(ORANGE, waves), width=5)
    # canh quat trong mat phang long (nen x theo RX/RY)
    sx = RX / RY
    if spin > 0.02:
        d.ellipse([CX - sx * 165, CY - 165, CX + sx * 165, CY + 165], fill=A((147, 197, 253), 0.45 * spin))
    ab = 1 - 0.7 * spin
    for k in range(3):
        a0 = ang + k * 2 * math.pi / 3; up, lo = [], []
        for i in range(13):
            s = i / 12; r = 22 + 143 * s; w = 0.42 * math.sin(math.pi * s) ** 0.7
            for side, L in ((1, up), (-1, lo)):
                a = a0 + side * w * (40 / max(r, 40))
                L.append((CX + sx * r * math.cos(a), CY + r * math.sin(a)))
        d.polygon(up + lo[::-1], fill=A(BLADE, ab))
    # long quat
    for i in range(8):
        a = i * math.pi / 4
        d.line([(CX, CY), (CX + RX * math.cos(a), CY + RY * math.sin(a))], fill=GRAY, width=2)
    d.ellipse([CX - 0.6 * RX, CY - 0.6 * RY, CX + 0.6 * RX, CY + 0.6 * RY], outline=GRAY, width=3)
    d.ellipse([CX - RX, CY - RY, CX + RX, CY + RY], outline=NAVY, width=5)
    dot(d, CX, CY, 26, NAVY)

def hand(d, x, y, a=1.0):
    """Ban tay nam ap tren mat phang: dau ngon o x, mat duoi o y; canh tay di len phia phai."""
    if a <= 0: return
    d.line([(x + 200, y - 25), (1130, y - 170)], fill=A(BLUE, a), width=54)
    d.rounded_rectangle([x, y - 50, x + 230, y], radius=24, fill=A(SKIN, a), outline=A(SKIN_D, a), width=3)
    for yy in (y - 34, y - 18):
        d.line([(x + 14, yy), (x + 96, yy)], fill=A(SKIN_D, a), width=3)

def clock(d, u, a=1.0):
    cx, cy, r = 130, 360, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(WHITE, a), outline=A(NAVY, a), width=5)
    ang = -math.pi / 2 + 2 * math.pi * u
    d.line([(cx, cy), (cx + 46 * math.cos(ang), cy + 46 * math.sin(ang))], fill=A(ORANGE, a), width=6)
    dot(d, cx, cy, 7, A(NAVY, a))
    text(d, (cx, cy + 104), f"{int(10 * u)} phút", 40, INK, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    u = clamp((t - 0.6) / 2.4)
    fan(d, 30 * t, 1.0, hum=0.8)
    clock(d, u)
    for (lx, ly), (px, py), s in (((880, 380), (750, 440), "vỏ động cơ"), ((910, 900), (790, 840), "chân đế")):
        d.line([(lx - 80, ly + 22), (px, py)], fill=INK, width=3)
        text(d, (lx, ly), s, 40, INK)
    k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 960 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 56
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 180, "Tắt quạt, sờ hai chỗ.", 46, INK, maxw=880, alpha=k)
    ctext(d, y0 + 320, "Vỏ động cơ so với chân đế thế nào?", 50, INK, maxw=820, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 480, 880, y0 + 494], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 480, 200 + 680 * (1 - q), y0 + 494], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
OFF_T, STOP = 0.6, 2.6                 # bam tat luc 0,6 s; canh cham dan, dung han sau 2,6 s

def blades(t):
    if t < OFF_T: return 30 * (t - OFF_T), 1.0
    u = clamp((t - OFF_T) / STOP)
    return 30 * STOP * (u - u * u / 2), 1 - u

def hand_pos(t, sc):
    M = sc["M"]; a1, b1 = M[1] + 0.1, M[1] + 0.9; a2, b2 = M[2], M[2] + 0.8
    H0, H1, H2 = (1150, 300), (600, 440), (660, 795)
    if t < a1: return None, 0
    if t < b1:
        k = ease((t - a1) / (b1 - a1)); return (lerp(H0[0], H1[0], k), lerp(H0[1], H1[1], k)), 0
    if t < a2: return H1, 1
    if t < b2:
        k = ease((t - a2) / (b2 - a2))
        return (lerp(H1[0], H2[0], k), lerp(H1[1], H2[1], k) - 90 * math.sin(math.pi * k)), 1
    return H2, 2

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    ang, sp = blades(t)
    pos, st = hand_pos(t, sc)
    t_vo = M[1] + 0.9; t_de = M[2] + 0.8                 # luc tay cham vo / cham chan de
    fan(d, ang, sp, glow=appear(t, t_vo, 0.5), press=t >= OFF_T, hum=1 - clamp((t - OFF_T) / 1.0))
    if pos: hand(d, pos[0], pos[1])
    # bang cam giac: o chi dien khi tay da cham dung cho do
    for j, (x0, s, word, col, at) in enumerate(((60, "vỏ động cơ", "ấm hơn rõ", ORANGE, t_vo),
                                                  (560, "chân đế", "mát", BLUE, t_de))):
        card(d, (x0, 930, x0 + 460, 1210), fill=WHITE, outline=LIGHT, w=4)
        text(d, (x0 + 230, 990), s, 42, INK)
        text(d, (x0 + 230, 1110), word, 56, col, alpha=appear(t, at + 0.05, 0.35))
    # the an toan
    card(d, (60, 1270, 1020, 1490), fill=(254, 242, 242), outline=DRED, w=5)
    d.polygon([(140, 1320), (190, 1410), (90, 1410)], fill=DRED)
    text(d, (140, 1385), "!", 48, WHITE)
    text(d, (230, 1335), "Rút phích, đợi cánh dừng hẳn", 42, DRED, anchor="lm")
    text(d, (230, 1425), "Tay không chạm cánh", 42, DRED, anchor="lm")

# ---------------- canh 3: dap an + Sankey ----------------
def h_at(t, sc):
    """Tra ve (H dang ve, H dang dung yen hoac None khi dang keo)."""
    m = sc["M"][2]
    seg = [(m + 0.2, m + 0.8, 65, 40), (m + 2.4, m + 3.0, 40, 90)]
    h = 65
    for a, b, h0, h1 in seg:
        if t < a: return h, h
        if t < b: return lerp(h0, h1, ease((t - a) / (b - a))), None
        h = h1
    return h, h

X0, XS, XE, Y0, TH = 80, 420, 860, 470, 270      # Sankey: dau vao x 80-420, tach o 420; day 270 px = 45 W

def sankey(d, h, k_ci, k_hp):
    ci = TH * h / 100
    d.rectangle([X0, Y0, XS, Y0 + TH], fill=BLUE)
    if k_ci > 0:
        d.rectangle([XS, Y0, XE, Y0 + ci], fill=A(GREEN, k_ci))
        d.polygon([(XE, Y0 - 18), (XE + 70, Y0 + ci / 2), (XE, Y0 + ci + 18)], fill=A(GREEN, k_ci))
    if k_hp > 0:
        off = lambda x: 260 * ease((x - XS) / 340)
        xs = list(range(XS, 801, 10)); top = Y0 + ci
        up = [(x, top + off(x)) for x in xs]; lo = [(x, Y0 + TH + off(x)) for x in xs]
        d.polygon(up + lo[::-1], fill=A(ORANGE, k_hp))
        yt, yb = top + 260, Y0 + TH + 260
        d.polygon([(800, yt - 16), (840, (yt + yb) / 2), (800, yb + 16)], fill=A(ORANGE, k_hp))
        yc = (yt + yb) / 2
        text(d, (860, yc - 26), "hao phí", 42, ORANGE, anchor="lm", alpha=k_hp)
        text(d, (860, yc + 24), "nhiệt, âm", 38, INK, bold=False, anchor="lm", alpha=k_hp)
    text(d, (X0, 430), "điện năng 45 W", 42, BLUE, anchor="lm")
    text(d, (1000, 430), "có ích: gió", 42, GREEN, anchor="rm", alpha=k_ci)

def s_dapan(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    ka = appear(t, 0.2, 0.45)
    s = "ĐÁP ÁN · vỏ động cơ ấm hơn"
    pw = tw(d, s, F(42)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 334), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 298), s, 42, WHITE, alpha=ka)
    k_ci = appear(t, M[0] + 0.2, 0.45); k_hp = appear(t, M[1] - 0.3, 0.45)
    h, hold = h_at(t, sc)
    sankey(d, h, k_ci, k_hp)
    # thanh H + so doc: so chi hien khi thanh dung yen o hang so_lieu_mau
    card(d, (40, 1060, 1040, 1540), fill=WHITE, outline=LIGHT, w=4)
    kx = 200 + 680 * (h - 30) / 60
    d.rounded_rectangle([200, 1172, 880, 1188], radius=8, fill=LIGHT)
    d.rounded_rectangle([200, 1172, kx, 1188], radius=8, fill=NAVY)
    dot(d, kx, 1180, 24, WHITE, outline=NAVY)
    text(d, (200, 1230), "30 %", 36, INK, bold=False); text(d, (880, 1230), "90 %", 36, INK, bold=False)
    text(d, (W / 2, 1290), "H = có ích ÷ toàn phần", 40, INK, bold=False)
    if hold is not None:
        ci, hp = ROWS[hold]
        text(d, (W / 2, 1115), f"H = {hold} %", 50, NAVY)
        text(d, (W / 2, 1365), f"Có ích: {ci} W", 48, GREEN, alpha=k_ci)
        text(d, (W / 2, 1440), f"Hao phí: {hp} W", 48, ORANGE, alpha=k_hp)
    text(d, (W / 2, 1505), "(số minh hoạ)", 36, INK, bold=False)

# ---------------- canh 4: bay roi chua noi duoc ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    fan(d, 0.0, 0.0, glow=1.0, press=True, waves=appear(t, 0.3, 0.5), t=t)
    text(d, (640, 290), "nhiệt", 44, ORANGE, alpha=appear(t, 0.5, 0.4))
    k3 = appear(t, M[1] - 0.1, 0.45)
    a = appear(t, 0.1, 0.4) * (1 - k3)
    if a > 0:
        y0 = 920
        card(d, (60, y0, 1020, y0 + 600), fill=A(WHITE, a), outline=A(DRED, a), w=6)
        pw = tw(d, "Bẫy", F(40)) + 60
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a), r=32)
        text(d, (W / 2, y0 + 60), "Bẫy", 40, WHITE, alpha=a)
        q = "“Phần không thành gió thì mất”"
        ks = clamp((t - 1.0) / 0.4); f = F(48); yy = y0 + 200; lw = tw(d, q, f)
        text(d, (W / 2, yy), q, 48, INK, alpha=a)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a), width=4)
        ctext(d, y0 + 400, "Sai: thành nhiệt, âm; vẫn bảo toàn", 48, DRED, maxw=860,
              alpha=appear(t, 1.6, 0.45) * a)
    if k3 > 0:
        y1 = 920 + (1 - k3) * 30
        card(d, (60, y1, 1020, y1 + 600), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 70), "Chưa nói được gì?", 46, NAVY, alpha=k3)
        items = ("• Tay chỉ so sánh, chưa đo nhiệt độ", "• 45 W và H: số minh hoạ")
        for j, s in enumerate(items):
            kk = k3 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (100, y1 + 230 + j * 140), s, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def hint(d, t, k):                        # tu ve goi y, chu >= 40 px, hien tre 2,5 s
        kh = appear(t, sc["M"][0] + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 1290, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1350, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1445, "1 W = 1 J mỗi giây", 46, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Hao phí không mất, chỉ đổi dạng",
             "Quạt 45 W, H = 80 %. Mỗi giây bao nhiêu J thành nhiệt và âm?", body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    ticks = [(h["t0"] + 0.6 + 0.24 * i, "tick") for i in range(10)]
    m2 = da["t0"] + da["M"][2]
    return ticks + [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + OFF_T, "tap"), (do["t0"] + do["M"][1] + 0.9, "tap"), (do["t0"] + do["M"][2] + 0.8, "tap"),
            (da["t0"] + 0.2, "ding"), (m2 + 0.8, "tap"), (m2 + 3.0, "tap"),
            (b["t0"] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-hieu-suat-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Hiệu suất · thachlab.id.vn", scenes=[
 dict(key="hook", title="Quạt bàn chạy 10 phút", draw=s_hook, tail=0.6, caps=[
   ("Bật quạt, nghe tiếng ù nhẹ.", 3.0),
   ("Dừng video, tự đoán.", 5.4)]),
 dict(key="do", title="Tắt quạt rồi mới sờ", draw=s_do, tail=0.5, caps=[
   ("An toàn trước khi sờ.", 3.4),
   ("Sờ vỏ động cơ trước.", 3.2),
   ("Rồi sang chân đế nhựa.", 3.0)]),
 dict(key="dapan", title="Điện năng đi đâu?", draw=s_dapan, tail=0.6, caps=[
   ("Điện năng không thành hết gió.", 3.2),
   ("Phần dư làm vỏ ấm lên.", 3.4),
   ("H càng lớn, hao phí càng nhỏ.", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy hay gặp.", 4.6),
   ("Giới hạn của thí nghiệm.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự tính.", 5.6)]),
])
