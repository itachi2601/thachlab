# Clip: tn-l12-chuyenthe-03 - Hai dia nuoc 20 ml, mot dia truoc quat, can sau 1 gio (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-chuyenthe-03.json -> so_lieu_mau (minh hoa, phong 30 °C):
#   gio 0 m/s -> 18,4 g · 1 m/s -> 15,6 g · 3 m/s -> 11,2 g · 5 m/s -> 8,1 g (con lai sau 1 gio, ban dau 20 ml = 20 g,
#   khoi luong rieng 1 g/ml theo mo_hinh.gia_thiet). Hang 40 °C (15,2 g; 7,6 g) KHONG hien: de danh cho cau chot.
# Muc nuoc trong hai dia giam tuyen tinh (mo_hinh: m_con(t) = m0 - v.t), chi la hinh; so can chi hien luc 0 va luc 60 phut.
# Du doan (K10: khong ve nut A-D trong mp4). Phong 30 °C, hai dia 20 ml, dia phai truoc quat gio 3 m/s. Sau 1 gio?
#   A. Ca hai van du 20 g vi nuoc chua soi
#   B. Hai dia voi bang nhau, gio khong anh huong
#   C. Ca hai voi, dia truoc quat voi nhieu hon      <- dap an (18,4 g va 11,2 g)
#   D. Chi dia truoc quat voi, dia kia van 20 g
# Bay (hien_tuong_hay_sai 2): "gio thoi bay nuoc di" -> mat nuoc phang, khong giot van; gio cuon hoi (phan tu da thoat).
#   Bay "phai soi moi bay hoi" duoc bac ngay o canh Tien hanh/Dap an (nhan "nuoc 30 °C, chua soi" - mo_hinh.ghi_chu).
# Khong viet "mat thoang" / "soi o 100 °C" tren man: Cau 4 sau hop (bay hoi khac soi o diem nao) hoi dung y nay.
# Chot THU NGHI: phong 40 °C, gio 3 m/s -> sau 1 gio con nhieu hay it hon 11,2 g? Dap so: it hon (7,6 g, so_lieu_mau).
#   Goi y chi la du kien thay doi: "Chi doi: 30 °C -> 40 °C".
from engine import *

ROWS = [(0, 18.4), (1, 15.6), (3, 11.2), (5, 8.1)]   # (gio m/s, nuoc con lai g) o 30 °C - so_lieu_mau
M0 = 20.0
STILL, FAN = 18.4, 11.2                              # dia de yen (0 m/s), dia truoc quat (3 m/s)
NOTE = (70, 75, 95)
WATER = (150, 200, 245); WATER_D = (90, 150, 220)
def vn(x): return f"{x:.1f}".replace(".", ",")

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=28):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.85, cx + wdt / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)

# ---------------- dung cu ----------------
DY = 640                                             # day dia
def dish(d, cx, m, alpha=1.0):
    """dia nong: mieng rong 300, sau 70; muc nuoc ti le khoi luong (20 g = day 56 px)"""
    w0, w1, h = 150, 120, 70
    d.polygon([(cx - w0, DY - h), (cx + w0, DY - h), (cx + w1, DY), (cx - w1, DY)], fill=A((225, 230, 238), alpha))
    lv = 56 * m / M0
    if lv > 2:
        k = lv / h; wl = w1 + (w0 - w1) * k
        d.polygon([(cx - wl + 6, DY - lv), (cx + wl - 6, DY - lv), (cx + w1 - 6, DY - 4), (cx - w1 + 6, DY - 4)], fill=A(WATER, alpha))
        d.line([(cx - wl + 6, DY - lv), (cx + wl - 6, DY - lv)], fill=A(WATER_D, alpha), width=4)
    d.line([(cx - w0, DY - h), (cx - w1, DY), (cx + w1, DY), (cx + w0, DY - h)], fill=A(NAVY, alpha), width=6)

def scale(d, cx, s, alpha=1.0, hl=0.0):
    d.rounded_rectangle([cx - 160, DY + 6, cx + 160, DY + 40], radius=8, fill=A((120, 126, 140), alpha))
    d.rounded_rectangle([cx - 140, DY + 40, cx + 140, DY + 150], radius=14, fill=A((60, 66, 84), alpha))
    d.rounded_rectangle([cx - 110, DY + 58, cx + 110, DY + 132], radius=10, fill=A((205, 230, 200) if s else (90, 100, 90), alpha))
    if hl > 0: d.rounded_rectangle([cx - 116, DY + 52, cx + 116, DY + 138], radius=12, outline=A(ORANGE, hl), width=6)
    if s: text(d, (cx, DY + 95), s, 50, NAVY, alpha=alpha)

def fan(d, t, cx, cy, on=1.0):
    d.line([(cx + 20, cy), (cx + 40, DY + 150)], fill=(90, 96, 110), width=14)
    d.rounded_rectangle([cx - 30, DY + 140, cx + 110, DY + 160], radius=8, fill=(90, 96, 110))
    d.ellipse([cx - 90, cy - 120, cx + 50, cy + 120], outline=NAVY, width=7, fill=(240, 244, 250))
    for k in range(3):
        a = t * 14 * on + k * 2 * math.pi / 3
        d.ellipse([cx - 20 - 55 * abs(math.cos(a)) * 0.5, cy + 95 * math.sin(a) - 22, cx - 20 + 55 * abs(math.cos(a)) * 0.5,
                   cy + 95 * math.sin(a) + 22], fill=A(BLUE, 0.35 + 0.4 * (1 - on)))
    dot(d, cx - 20, cy, 16, NAVY)

def wind(d, t, x0, x1, ys, alpha=1.0):
    for j, y in enumerate(ys):
        u = (t * 1.3 + j * 0.37) % 1
        xa = x1 - u * (x1 - x0); al = alpha * min(1, u / 0.15, (1 - u) / 0.15)
        d.line([(xa, y), (xa - 90, y)], fill=A(TEAL, al), width=5)
        d.line([(xa - 90, y), (xa - 76, y - 10)], fill=A(TEAL, al), width=5)

def therm_card(d, s="30 °C"):
    card(d, (40, 260, 330, 400), fill=WHITE, outline=NAVY, w=4, r=22)
    text(d, (185, 300), "Phòng", 44, MUTED, bold=False)
    text(d, (185, 360), s, 52, INK)

XL, XR, XF = 240, 620, 930                            # dia trai, dia phai, quat

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    therm_card(d)
    dish(d, XL, M0); dish(d, XR, M0); fan(d, t, XF, 460)
    wind(d, t, XR - 120, XF - 110, (470, 510, 550))
    text(d, (XL, DY + 60), "để yên", 44, NOTE)
    text(d, (XR, DY + 60), "trước quạt", 44, NOTE)
    pill(d, 700, 300, "gió 3 m/s", 44, WHITE, TEAL)
    text(d, (W / 2 - 40, DY + 140), "mỗi đĩa 20 ml", 46, INK, alpha=appear(t, 0.5, 0.5))
    a = appear(t, sc["M"][1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", 44, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 230), "Sau 1 giờ, hai đĩa ra sao?", 52, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 400), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = sc["M"][1] + 0.6, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 490, 940, y0 + 502], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 490, 140 + 800 * (1 - p), y0 + 502], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (tua nhanh 1 gio, can lai) ----------------
def tau_of(t, sc):                                    # phut da troi
    a, b = sc["M"][0] + 0.3, sc["M"][1] - 0.3
    return 60.0 * clamp((t - a) / (b - a))

def readings(tau):
    """so can hien tren man: chi luc 0 phut va 60 phut (khong noi suy)"""
    if tau <= 1e-6: return vn(M0) + " g", vn(M0) + " g"
    if tau >= 60 - 1e-6: return vn(STILL) + " g", vn(FAN) + " g"
    return None, None

DBG = []
def s_do(img, d, t, sc):
    tau = tau_of(t, sc)
    therm_card(d)
    mL = M0 - (M0 - STILL) * tau / 60; mR = M0 - (M0 - FAN) * tau / 60
    dish(d, XL, mL); dish(d, XR, mR); fan(d, t, XF, 460)
    wind(d, t, XR - 120, XF - 110, (470, 510, 550))
    rl, rr = readings(tau); hl = appear(t, sc["M"][1] + 0.1, 0.4)
    scale(d, XL, rl, hl=hl); scale(d, XR, rr, hl=hl)
    DBG.append((t, tau, rl, rr))
    # dong ho
    card(d, (370, 260, 610, 400), fill=WHITE, outline=NAVY, w=4, r=22)
    text(d, (490, 300), "Đồng hồ", 44, MUTED, bold=False)
    text(d, (490, 360), f"{int(tau + 1e-6)} phút", 52, INK)
    if 0 < tau < 60:
        wdt = tw(d, "TUA NHANH", F(44)) + 90
        card(d, (W / 2 - wdt / 2, 860, W / 2 + wdt / 2, 930), fill=ORANGE, r=34)
        text(d, (W / 2 + 22, 895), "TUA NHANH", 44, WHITE)
        for k in range(2):
            tx = W / 2 - wdt / 2 + 24 + k * 16; d.polygon([(tx, 880), (tx, 910), (tx + 16, 895)], fill=WHITE)
    # nhiet do nuoc: chua soi
    k2 = appear(t, sc["M"][1] + 0.6, 0.4)
    if k2 > 0:
        card(d, (90, 1000, 990, 1150), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1075), "Nước vẫn 30 °C: chưa hề sôi", 50, GREEN, alpha=k2)

# ---------------- canh 3: Dap an + bang/bieu do ----------------
def s_ket(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.2, 0.4)
    pill(d, W / 2, 300, "ĐÁP ÁN · Cả hai vơi; có gió vơi hơn", 44, WHITE, NAVY, ka)
    card(d, (40, 380, 1040, 1300), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 440), "Còn sau 1 giờ (g)", 46, INK, anchor="lm")
    text(d, (1000, 500), "minh hoạ", 44, PURPLE, bold=False, anchor="rm")
    X0, KX = 330, 620 / 20                            # truc tu 0 g, 20 g = 620 px
    yb = 1130
    d.line([(X0, 560), (X0, yb)], fill=INK, width=4); d.line([(X0, yb), (X0 + KX * 20 + 20, yb)], fill=INK, width=4)
    for v in (0, 10, 20):
        x = X0 + KX * v; d.line([(x, yb), (x, yb + 14)], fill=INK, width=4)
        text(d, (x, yb + 46), str(v), 44, INK, bold=False)
    xs = X0 + KX * 20
    for yy in range(565, yb, 28): d.line([(xs, yy), (xs, yy + 14)], fill=GREEN, width=4)
    order = (0, 2, 1, 3)                              # hai dia vua can hien truoc, roi hai lan lap
    for n, j in enumerate(order):
        v, m = ROWS[j]; y = 610 + 128 * j
        at = 0.3 + 0.25 * n if n < 2 else M[1] - 0.1 + 0.4 * (n - 2)
        k = appear(t, at, 0.4)
        if k <= 0: continue
        text(d, (X0 - 24, y), f"gió {v} m/s", 44, INK, anchor="rm", alpha=k)
        L = KX * m * ease((t - at) / 0.6)
        if L > 2: d.rounded_rectangle([X0, y - 30, X0 + L, y + 30], radius=10, fill=A(BLUE if v == 0 else TEAL, k))
        if L > 2: text(d, (X0 + L - 14, y), vn(m), 44, WHITE, anchor="rm", alpha=appear(t, at + 0.5, 0.3))

# ---------------- canh 4: Co che + Rut ra ----------------
def panel(d, t, x0, x1, windy, alpha=1.0, dy=0):
    y0, ys, y1 = 420 + dy, 700 + dy, 900 + dy                         # dinh panel, mat nuoc, day
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=A((247, 248, 252), alpha))
    d.rectangle([x0 + 4, ys, x1 - 4, y1 - 4], fill=A((214, 230, 250), alpha))
    d.line([(x0 + 4, ys), (x1 - 4, ys)], fill=A(WATER_D, alpha), width=5)
    cx = (x0 + x1) / 2
    for i in range(10):                                  # phan tu trong nuoc: rung tai cho
        px = x0 + 40 + (i % 5) * (x1 - x0 - 80) / 4 + 8 * math.sin(t * 9 + i)
        py = ys + 50 + (i // 5) * 90 + 8 * math.cos(t * 8 + 2 * i)
        dot(d, px, py, 16, A(BLUE, alpha), outline=A(WHITE, alpha))
    for i in range(4):                                   # phan tu nhanh thoat len thanh hoi
        u = (t * 0.55 + i / 4) % 1
        bx = x0 + 60 + i * (x1 - x0 - 120) / 3
        if windy:
            x = bx + u * u * 420; y = ys - 20 - u * 150
            al = alpha * clamp((1 - u) / 0.2) * clamp((x1 - 20 - x) / 40)
        else:
            up = 1 - abs(1 - 2 * u)                       # len roi roi lai mat nuoc
            x = bx + 18 * math.sin(t * 2 + i); y = ys - 20 - up * 190
            al = alpha
        if al > 0.02: dot(d, x, y, 16, A(BLUE, al), outline=A(WHITE, al))
        if not windy and i == 1 and u > 0.55:
            arrow(d, (x + 40, y - 10), (x + 40, y + 50), A(ORANGE, alpha), w=5, head=14)
    if windy: wind(d, t, x0 + 20, x1 - 10, (480 + dy, 540 + dy), alpha)

def s_coche(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 250, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    text(d, (290, 340), "Không gió", 46, NOTE); text(d, (790, 340), "Có gió", 46, TEAL)
    panel(d, t, 70, 510, False); panel(d, t, 570, 1010, True)
    text(d, (290, 925), "quay lại", 44, ORANGE, alpha=appear(t, M[0] + 0.6, 0.4))
    text(d, (790, 925), "bị cuốn đi", 44, TEAL, alpha=appear(t, M[1] - 0.1, 0.4))
    k = appear(t, M[1] + 0.4, 0.45)
    if k > 0:
        y = 1020 + (1 - k) * 25
        card(d, (60, y, 1020, y + 220), fill=A(WHITE, k), outline=A(GREEN, k), w=6)
        text(d, (W / 2, y + 110), "→ Bay hơi nhanh hơn", 50, GREEN, alpha=k)

# ---------------- canh 5: Chua noi duoc gi ----------------
def s_chua(img, d, t, sc):
    k = appear(t, 0.3, 0.45)
    card(d, (40, 300, 1040, 940), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 380), "Chưa nói được", 52, NAVY, alpha=k)
    items = (("• Diện tích mặt nước:", "hai đĩa giống hệt nhau"), ("• Độ ẩm:", "coi như không đổi"))
    for j, (l1, l2) in enumerate(items):
        kk = appear(t, 0.7 + 0.6 * j, 0.4); y = 540 + 260 * j
        text(d, (90, y), l1, 48, INK, anchor="lm", alpha=kk)
        text(d, (130, y + 70), l2, 48, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[0] + 1.0
    card(d, (40, 250, 1040, 560), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, 310, "BẪY", 44, WHITE, RED)
    q = "“Gió thổi bay nước đi”"
    ks = clamp((t - mk) / 0.4)
    text(d, (W / 2, 420), q, 50, mix(INK, GRAY, ks))
    if ks > 0:
        lw = tw(d, q, F(50)); d.line([(W / 2 - lw / 2, 422), (W / 2 - lw / 2 + lw * ks, 422)], fill=RED, width=6)
        text(d, (W / 2 + lw / 2 + 40, 420), "✗", 50, RED, alpha=ks)
    ka = appear(t, mk + 0.2, 0.45)
    if ka <= 0: return
    card(d, (40, 600, 1040, 1420), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    panel(d, t, 300, 780, True, ka, dy=220)
    text(d, (W / 2, 1185), "không văng giọt nào", 46, INK, alpha=appear(t, mk + 0.6, 0.4))
    kc = appear(t, mk + 2.4, 0.45)
    text(d, (W / 2, 1300), "hơi bị cuốn đi", 50, GREEN, alpha=kc)
    text(d, (W / 2 + 230, 1300), "✓", 64, GREEN, alpha=kc)

# ---------------- canh 7: Chot + cau hoi tu nho lai ----------------
KH = [0.0]                                       # do hien goi y: hinh ha thap luc chua co goi y, truot len khi goi y hien
def _end_body(d, t, k):
    # nhiet ke phong + quat nho (khong chu, khong so moi ngoai cau hoi)
    o = 150 * (1 - KH[0])
    d.rounded_rectangle([350, 1010 + o, 380, 1200 + o], radius=15, outline=A(NAVY, k), width=5, fill=A(WHITE, k))
    d.rectangle([358, 1080 + o, 372, 1190 + o], fill=A(RED, k)); dot(d, 365, 1215 + o, 26, A(RED, k))
    d.ellipse([600, 1020 + o, 720, 1200 + o], outline=A(NAVY, k), width=6)
    dot(d, 660, 1110 + o, 12, A(NAVY, k))
    for j, y in enumerate((1070, 1110, 1150)):
        d.line([(560 - 20 * j, y + o), (480 - 20 * j, y + o)], fill=A(TEAL, k), width=5)

def s_end(img, d, t, sc):
    M = sc["M"]; KH[0] = appear(t, M[0] + 2.9, 0.5)
    chot_hoi(d, t, sc, "Chưa sôi vẫn bay hơi",
             "Phòng 40 °C, gió 3 m/s. Sau 1 giờ còn nhiều hay ít hơn 11,2 g?", None, body=_end_body)
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh > 0:
        card(d, (110, 1300, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1355), "Gợi ý", 44, INK, bold=False, alpha=kh)
        text(d, (W / 2, 1455), "Chỉ đổi: 30 °C → 40 °C", 48, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, c, ch, b, e = (sc[x] for x in ("hook", "do", "ket", "coche", "chua", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + 0.05, "ding")]
    tt = do["M"][0] + 0.3
    while tt < do["M"][1] - 0.3: out.append((do["t0"] + tt, "tick")); tt += 0.5
    out += [(do["t0"] + do["M"][1] + 0.1, "tap"), (k["t0"] + 0.2, "ding"), (c["t0"] + c["M"][1] + 0.4, "tap"),
            (ch["t0"] + 0.3, "tap"), (b["t0"] + b["M"][0] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-chuyenthe-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Sự chuyển thể · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai đĩa nước, một chiếc quạt", draw=s_hook, tail=0.3, caps=[
   ("Một đĩa đặt trước quạt.", 3.0),
   ("Nghĩ trước khi xem.", 5.6)]),
 dict(key="do", title="Chờ 1 giờ rồi cân", draw=s_do, tail=0.4, caps=[
   ("Bật quạt, giữ nguyên 1 giờ.", 3.4),
   ("Cân lại hai đĩa.", 3.0)]),
 dict(key="ket", title="Kết quả", draw=s_ket, tail=0.4, caps=[
   ("Đĩa để yên cũng vơi đi.", 3.0),
   ("Gió càng mạnh, còn càng ít.", 3.4)]),
 dict(key="coche", title="Vì sao gió làm khô nhanh?", draw=s_coche, tail=0.4, caps=[
   ("Phân tử nhanh thoát khỏi nước.", 2.9),
   ("Gió cuốn hơi đi.", 2.9)]),
 dict(key="chua", title="Giới hạn của thí nghiệm", draw=s_chua, tail=0.3, caps=[
   ("Hai giới hạn.", 4.6)]),
 dict(key="bay", title="Cái bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Gió hất nước ra?", 2.5),
   ("Không: chỉ hơi bị cuốn.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Tự trả lời trước.", 5.6)]),
])
