# Clip: tn-l10-hieu-suat-01 - So vo quat ban sau khi chay (ban 2 theo cong moi, 27/11/2026)
# So lieu lay tu content/thi-nghiem/tn-l10-hieu-suat-01.json:
#   tham_so: P_tp = 45 W (minh hoa), H 30-90 % (mac dinh 65); so_lieu_mau: H 65 % -> P_hp 15,75 W (so minh hoa).
# Du doan (K10, giu y cu): tat quat, so hai cho -> vo dong co so voi chan de? Dap an: vo dong co am hon.
# An toan (them so voi kho): tat quat, doi canh dung han roi moi so; tay khong cham canh.
# Bay: hien_tuong_hay_sai[0] "phan khong thanh chuyen dong thi bien mat" -> song nhiet tu vo, nang luong doi dang.
# Cau chot (tu suy, khac Cau 1-4 cua bai vi can them buoc doi thoi gian): quat 45 W, H = 80 %, chay 10 phut
#   -> P_hp = 9 W -> 9 . 600 = 5 400 J = 5,4 kJ (KHONG hien tren man).
from engine import *

DRED = (185, 28, 28); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
SKIN = (241, 200, 166); SKIN_D = (205, 150, 112)
METAL = (214, 218, 228); WARM = (253, 186, 140); BLADE = (96, 165, 250)
CX, CY, RX, RY = 380, 500, 140, 190          # long quat (nhin xien 3/4)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); w = 780 / n
    for i in range(n):
        x = 150 + i * w
        if i < on: card(d, (x, y, x + w - 20, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w - 20, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

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
            d.arc([790 - r, 500 - r, 790 + r, 500 + r], -40, 40, fill=A(GRAY, hum), width=4)
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
    cx, cy, r = 130, 340, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(WHITE, a), outline=A(NAVY, a), width=5)
    ang = -math.pi / 2 + 2 * math.pi * u
    d.line([(cx, cy), (cx + 46 * math.cos(ang), cy + 46 * math.sin(ang))], fill=A(ORANGE, a), width=6)
    dot(d, cx, cy, 7, A(NAVY, a))
    text(d, (cx + 5, cy + 110), f"{int(10 * u)} phút", 56, INK, alpha=a)

def labels(d, a=1.0):
    for (lx, ly), (px, py), s in (((880, 360), (750, 440), "vỏ động cơ"), ((900, 920), (790, 845), "chân đế")):
        d.line([(lx - 90, ly + 30), (px, py)], fill=A(INK, a), width=3)
        text(d, (lx, ly), s, 56, INK, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    fan(d, 30 * t, 1.0, hum=0.8)
    clock(d, clamp((t - 0.4) / 3.0)); labels(d)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1050 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 175), "Tắt quạt, sờ hai chỗ.", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 265), "Vỏ động cơ so với chân đế?", 62, PURPLE, alpha=k)
    seg_bar(d, y0 + 370, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: tien hanh + dap an ----------------
OFF_T, STOP = 0.3, 2.0
T_VO, T_DE, T_DA = 3.0, 5.5, 8.0           # tay cham vo / cham chan de / the dap an

def blades(t):
    if t < OFF_T: return 30 * (t - OFF_T), 1.0
    u = clamp((t - OFF_T) / STOP)
    return 30 * STOP * (u - u * u / 2), 1 - u

def hand_pos(t):
    H0, H1, H2 = (1150, 300), (600, 440), (660, 795)
    a1, a2 = T_VO - 0.7, T_DE - 0.7
    if t < a1: return None
    if t < T_VO:
        k = ease((t - a1) / 0.7); return lerp(H0[0], H1[0], k), lerp(H0[1], H1[1], k)
    if t < a2: return H1
    if t < T_DE:
        k = ease((t - a2) / 0.7); return lerp(H1[0], H2[0], k), lerp(H1[1], H2[1], k) - 90 * math.sin(math.pi * k)
    return H2

def s_do(img, d, t, sc):
    ang, sp = blades(t); pos = hand_pos(t)
    fan(d, ang, sp, glow=appear(t, T_VO, 0.5), press=t >= OFF_T, hum=1 - clamp((t - OFF_T) / 1.0))
    labels(d, 1 - appear(t, T_VO - 0.9, 0.3))
    if pos: hand(d, pos[0], pos[1])
    for x0, s, word, col, at in ((60, "vỏ động cơ", "ấm hơn rõ", ORANGE, T_VO), (560, "chân đế", "mát", BLUE, T_DE)):
        card(d, (x0, 960, x0 + 460, 1220), fill=WHITE, outline=LIGHT, w=4)
        text(d, (x0 + 230, 1025), s, 56, INK)
        text(d, (x0 + 230, 1135), word, 62, col, alpha=appear(t, at + 0.05, 0.35))
    ka = appear(t, T_DA, 0.4)
    if ka > 0:
        card(d, (60, 1260, 1020, 1390), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1325), "Đáp án: vỏ động cơ ấm hơn", 60, GREEN, alpha=ka)

# ---------------- canh 3: dien nang di dau ----------------
X0, XS, XE, Y0, TH = 80, 400, 840, 520, 300      # Sankey: day 300 px = 45 W
K_CI, K_HP, K_SO, K_MV = 0.3, 2.8, 5.3, 8.2

def sankey(d, h, k_ci, k_hp):
    ci = TH * h / 100
    d.rectangle([X0, Y0, XS, Y0 + TH], fill=BLUE)
    if k_ci > 0:
        text(d, (X0, Y0 - 60), "điện năng 45 W", 58, BLUE, anchor="lm", alpha=k_ci)
        d.rectangle([XS, Y0, XE, Y0 + ci], fill=A(GREEN, k_ci))
        d.polygon([(XE, Y0 - 18), (XE + 70, Y0 + ci / 2), (XE, Y0 + ci + 18)], fill=A(GREEN, k_ci))
        text(d, (1010, Y0 - 60), "có ích: gió", 58, GREEN, anchor="rm", alpha=k_ci)
    if k_hp > 0:
        off = lambda x: 240 * ease((x - XS) / 340)
        xs = list(range(XS, 781, 10)); top = Y0 + ci
        up = [(x, top + off(x)) for x in xs]; lo = [(x, Y0 + TH + off(x)) for x in xs]
        d.polygon(up + lo[::-1], fill=A(ORANGE, k_hp))
        yt, yb = top + 240, Y0 + TH + 240
        d.polygon([(780, yt - 16), (820, (yt + yb) / 2), (780, yb + 16)], fill=A(ORANGE, k_hp))
        text(d, (1010, yb + 70), "hao phí: nhiệt, âm", 58, ORANGE, anchor="rm", alpha=k_hp)

def s_rut(img, d, t, sc):
    h = lerp(65, 90, ease((t - K_MV) / 0.8))
    sankey(d, h, appear(t, K_CI, 0.45), appear(t, K_HP, 0.45))
    ks = appear(t, K_SO, 0.4) * (1 - appear(t, K_MV - 0.3, 0.3))
    if ks > 0:
        card(d, (60, 1260, 1020, 1390), fill=A(WHITE, ks), outline=A(ORANGE, ks), r=28, w=4)
        text(d, (W / 2, 1325), "H = 65 %: hao phí 15,75 W", 60, DORANGE, alpha=ks)

# ---------------- canh 4: bay + gioi han ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    fan(d, 0.0, 0.0, glow=1.0, press=True, waves=1.0, t=t)
    k0 = appear(t, 0.2, 0.4); k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3); y = 1000
    if a1 > 0:
        card(d, (40, y, 1040, y + 420), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", RED, a1)
        q = "“Không thành gió thì mất”"
        ks = clamp((t - mk) / 0.4); lw = tw(d, q, F(58)); yy = y + 190
        text(d, (W / 2, yy), q, 58, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        k2 = appear(t, mk + 0.2, 0.45)
        if k2 > 0: text(d, (W / 2, y + 320), "Thành nhiệt, âm: vẫn còn", 60, DORANGE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 210), "Mới so bằng tay", 60, INK, alpha=k3)

# ---------------- canh 5: thu nghi (cau chot o khung: 5 400 J) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1620), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    cx, cy = 540, 600; ang = 30 * t
    d.ellipse([cx - 170, cy - 170, cx + 170, cy + 170], outline=A(NAVY, k), width=5)
    for j in range(3):
        a0 = ang + j * 2 * math.pi / 3
        pts = [(cx + r * math.cos(a0 + s), cy + r * math.sin(a0 + s)) for r, s in ((20, -0.35), (150, -0.18), (150, 0.18), (20, 0.35))]
        d.polygon(pts, fill=A(BLADE, k))
    dot(d, cx, cy, 24, A(NAVY, k))
    text(d, (W / 2, 900), "Quạt 45 W, H = 80 %,", 62, INK, alpha=k)
    text(d, (W / 2, 990), "chạy 10 phút.", 62, INK, alpha=k)
    text(d, (W / 2, 1120), "Nhiệt và âm toả ra", 64, DORANGE, alpha=k)
    text(d, (W / 2, 1210), "bao nhiêu kJ?", 64, DORANGE, alpha=k)
    seg_bar(d, 1360, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.05, "ding"),
            (do["t0"] + OFF_T, "tap"), (do["t0"] + T_VO, "tap"), (do["t0"] + T_DE, "tap"), (do["t0"] + T_DA, "ding"),
            (r["t0"] + K_HP, "tap"), (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
            (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-hieu-suat-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Hiệu suất · thachlab.id.vn", scenes=[
 dict(key="hook", title="Quạt bàn chạy 10 phút", draw=s_hook, tail=0.3, caps=[
   ("Bật quạt, nghe tiếng ù nhẹ.", 3.2),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tắt quạt rồi mới sờ", draw=s_do, tail=0.5, caps=[
   ("Tắt quạt, đợi cánh dừng hẳn.", 3.4),
   ("Mu bàn tay sờ vỏ, rồi chân đế.", 6.6)]),
 dict(key="rut", title="Điện năng đi đâu?", draw=s_rut, tail=0.4, caps=[
   ("Điện năng không thành hết gió.", 6.8),
   ("H lớn hơn, hao phí nhỏ hơn.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Đúng không?", 3.2),
   ("Sai: năng lượng chỉ đổi dạng.", 3.4),
   ("Giới hạn của lần đo.", 3.1)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])
