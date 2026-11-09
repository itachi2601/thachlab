# Clip: tn-l11-tatdan-01 - Quet tan so luc cuong buc, doc bien do on dinh (9/11/2026, chang B L11 Dao dong)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-tatdan-01.json:
#   tham_so: f0 = 2,0 Hz, f 0,5-3,5 Hz buoc 0,5 ; b = 0,5 Hz ; Ar = 6,0 cm ; sai_so = 0,2 cm.
#   so_lieu_mau (f, A lam tron): 1,0 2,7 ; 1,5 4,2 ; 2,0 6,0 ; 2,5 4,2 ; 3,0 2,7 (khong phai so do that -> "so minh hoa").
#   mo_hinh: A(f) = Ar.b / sqrt((f - f0)^2 + b^2) -> duong net dut qua 5 diem o canh Dap an.
#   hien_tuong_hay_sai[0]: "luc manh la cong huong" -> canh Bay (cung mo-to, chi doi f: 2,7 -> 6,0 cm).
# Doan ngay sau hop trong bai: cau tu kiem "Dinh o 2,0 Hz; chenh 1,8 cm vuot nguong 0,4 cm" -> clip KHONG tinh hieu
#   dinh / nguong 0,4 cm, khong nhan manh "1,5 va 2,5 Hz bang nhau" (phuong an C), khong noi tan so vat (phuong an D).
# Cau chot: f = 3,5 Hz (tham_so max, chua tung hien): A lon hon hay nho hon 2,7 cm? (dung: nho hon, ~1,9 cm khong hien).
# Canh: Du doan (K10: chi cau hoi) -> Tien hanh (quet 5 tan so, cham len do thi) -> Dap an + Rut ra + Chua noi duoc
#       -> Bay -> Chot + cau hoi.
from engine import *

F0, AR, B, ERR = 2.0, 6.0, 0.5, 0.2
ROWS = [(1.0, 2.7), (1.5, 4.2), (2.0, 6.0), (2.5, 4.2), (3.0, 2.7)]
def amp(f, ar=AR, b=B): return ar * b / math.sqrt((f - F0) ** 2 + b * b)
def fs(v): return f"{v:.1f}".replace(".", ",")

# ---------------- gia + mo-to + lo xo + vat ----------------
PX = 26                       # 1 cm = 26 px
MX, MY = 330, 330             # truc mo-to (diem treo lo xo)
YEQ = 640                     # tam vat o vi tri can bang
def spring_v(d, x, y0, y1, col, n=11, amp_=26, w=5):
    lead = 16; pts = [(x, y0), (x, y0 + lead)]; L = (y1 - lead) - (y0 + lead)
    for i in range(1, 2 * n):
        pts.append((x + (amp_ if i % 2 else -amp_), y0 + lead + L * i / (2 * n)))
    pts += [(x, y1 - lead), (x, y1)]
    d.line(pts, fill=col, width=w, joint="curve")

def rig(d, ycm, phase, f_lab, a=1.0):
    """ycm: li do vat (cm, duong xuong duoi); phase: goc quay dia lech tam; f_lab: chu tren dong ho tan so."""
    c = lambda col: A(col, a)
    d.rectangle([90, MY - 70, 600, MY - 50], fill=c((190, 195, 210)), outline=c(NAVY), width=3)      # gia
    card(d, (MX - 80, MY - 50, MX + 80, MY + 10), fill=c((205, 200, 190)), outline=c(NAVY), r=10, w=3)  # vo mo-to
    ex, ey = MX + 22 * math.cos(phase), MY + 34 + 0 * math.sin(phase)
    d.ellipse([MX - 34, MY - 4 - 30, MX + 34, MY - 4 + 30], outline=c(NAVY), width=4)                  # dia
    dot(d, MX + 22 * math.cos(phase), MY - 4 - 22 * math.sin(phase), 10, c(ORANGE))                    # cuc lech tam
    yb = YEQ + ycm * PX
    spring_v(d, MX, MY + 10, yb - 45, c(NAVY))
    card(d, (MX - 55, yb - 45, MX + 55, yb + 45), fill=c(BLUE), outline=c(NAVY), r=12, w=4)
    # thuoc doc ben phai (0 o can bang, vach moi 1 cm, so moi 2 cm)
    rx = MX + 130
    d.rectangle([rx, YEQ - 7 * PX, rx + 46, YEQ + 7 * PX], fill=c((253, 246, 200)), outline=c(NAVY), width=3)
    for k in range(-7, 8):
        L = 26 if k % 2 == 0 else 14
        d.line([(rx, YEQ + k * PX), (rx + L, YEQ + k * PX)], fill=c(NAVY), width=3)
        if k % 2 == 0 and k != 0: text(d, (rx + 90, YEQ + k * PX), str(abs(k)), 40, INK, alpha=a)
    text(d, (rx + 90, YEQ), "0", 40, INK, alpha=a)
    d.line([(MX + 60, yb), (rx - 4, yb)], fill=c(ORANGE), width=3)                                    # kim chi vi tri vat
    # dong ho tan so cua mo-to
    card(d, (650, 380, 1010, 520), fill=c(WHITE), outline=c(NAVY), r=20, w=4)
    text(d, (830, 418), "tần số lực", 40, MUTED, alpha=a)
    text(d, (830, 478), f_lab, 52, NAVY, alpha=a)

# ---------------- do thi A - f (truc co dinh suot clip) ----------------
GX0, GX1, GY0, GY1 = 200, 980, 960, 1460           # khung truc (nguon)
def gx(f): return GX0 + (f - 0.5) / 3.25 * (GX1 - GX0)     # truc 0,5 -> 3,75 Hz, co vach 3,5 tu dau
def gy(a_): return GY1 - a_ / 7.0 * (GY1 - GY0)
def axes(d, a=1.0):
    c = lambda col: A(col, a)
    d.line([(GX0, GY1), (GX1 + 20, GY1)], fill=c(NAVY), width=4)
    d.line([(GX0, GY1), (GX0, GY0 - 30)], fill=c(NAVY), width=4)
    d.polygon([(GX1 + 34, GY1), (GX1 + 14, GY1 - 10), (GX1 + 14, GY1 + 10)], fill=c(NAVY))
    d.polygon([(GX0, GY0 - 44), (GX0 - 10, GY0 - 24), (GX0 + 10, GY0 - 24)], fill=c(NAVY))
    for f in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5):
        d.line([(gx(f), GY1), (gx(f), GY1 + 12)], fill=c(NAVY), width=3)
        text(d, (gx(f), GY1 + 46), fs(f), 40, INK, alpha=a)
    for v in (2, 4, 6):
        d.line([(GX0 - 12, gy(v)), (GX0, gy(v))], fill=c(NAVY), width=3)
        d.line([(GX0, gy(v)), (GX1, gy(v))], fill=c(LIGHT), width=2)
        text(d, (GX0 - 36, gy(v)), str(v), 40, INK, alpha=a)
    text(d, (GX1 - 10, GY1 + 96), "f (Hz)", 40, INK, anchor="rm", alpha=a)
    text(d, (GX0 + 20, GY0 - 40), "A (cm)", 40, INK, anchor="lm", alpha=a)

def point(d, f, a_, k=1.0, lab=True, col=ORANGE):
    if k <= 0: return
    x, y = gx(f), gy(a_)
    e = ERR / 7.0 * (GY1 - GY0)
    d.line([(x, y - e), (x, y + e)], fill=A(col, k), width=4)
    d.line([(x - 10, y - e), (x + 10, y - e)], fill=A(col, k), width=4)
    d.line([(x - 10, y + e), (x + 10, y + e)], fill=A(col, k), width=4)
    dot(d, x, y, 12, A(col, k), outline=A(WHITE, k))
    if lab: text(d, (x, y - 44), fs(a_), 40, col, alpha=k)

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.85, cx + pw / 2, cy + size * 0.85), fill=A(bg, a), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi, khong nut A/B/C) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0.0, 0.0, "? Hz")
    kf = appear(t, 0.6, 0.4)
    card(d, (650, 570, 1010, 690), fill=A((236, 253, 243), kf), outline=A(GREEN, kf), r=20, w=4)
    text(d, (830, 604), "tần số riêng", 40, MUTED, alpha=kf)
    rich(d, 830, 656, "f_{0} = 2,0 Hz", 46, GREEN, alpha=kf)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 860 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 620), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 40, WHITE, PURPLE, a)
    ctext(d, y0 + 180, "Đặt lần lượt f = 1,0 → 3,0 Hz.", 44, MUTED, maxw=920, alpha=a)
    ctext(d, y0 + 360, "Biên độ ổn định A\nđổi thế nào theo f?", 54, INK, maxw=930, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 550, 940, y0 + 562], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 550, 140 + 800 * (1 - p), y0 + 562], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (quet 5 tan so) ----------------
T0S, STEP, SETTLE, READ = 1.0, 1.6, 0.7, 0.95
def step_of(t):
    if t < T0S: return -1
    return min(4, int((t - T0S) / STEP))

def s_do(img, d, t, sc):
    i = step_of(t)
    card(d, (650, 640, 1010, 800), fill=WHITE, outline=NAVY, r=20, w=3)
    text(d, (830, 685), "số minh hoạ", 40, ORANGE)
    text(d, (830, 755), "sai số ±0,2 cm", 40, INK)
    if i < 0:
        rig(d, 0.0, 0.0, "? Hz")
    else:
        f, a_ = ROWS[i]
        tl = t - (T0S + i * STEP)
        if i == 4: tl = min(tl, 99)
        g = ease(tl / SETTLE)                         # bien do lon dan toi luc on dinh
        y = a_ * g * math.sin(2 * math.pi * f * tl)
        rig(d, y, 2 * math.pi * f * tl, fs(f) + " Hz")
        if tl >= READ: text(d, (830, 580), "A = " + fs(a_) + " cm", 44, ORANGE)
    axes(d)
    for j, (f, a_) in enumerate(ROWS):
        tr = T0S + j * STEP + READ
        point(d, f, a_, appear(t, tr, 0.3))

# ---------------- canh 3: Dap an + Rut ra + Chua noi duoc ----------------
def curve(d, k, ar=AR, b=B, col=ORANGE, w=5, dash=True):
    n = 90; pts = []
    for j in range(int(n * k) + 1):
        f = 0.5 + 3.0 * j / n
        pts.append((gx(f), gy(ar * b / math.sqrt((f - F0) ** 2 + b * b))))
    if len(pts) < 2: return
    if dash:
        for j in range(0, len(pts) - 1, 2): d.line([pts[j], pts[j + 1]], fill=col, width=w)
    else: d.line(pts, fill=col, width=w, joint="curve")

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    pill(d, W / 2, 300, "ĐÁP ÁN · A lớn nhất ở 2,0 Hz", 42, WHITE, NAVY, ka)
    kr = appear(t, M[0] + 0.3, 0.45)
    if kr > 0:
        card(d, (60, 380, 1020, 560), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=24, w=4)
        rich(d, W / 2, 470, "Đỉnh cộng hưởng: f = f_{0}", 54, (21, 110, 55), alpha=kr)
    kn = appear(t, M[1] - 0.05, 0.45)
    if kn > 0:
        card(d, (60, 600, 1020, 840), fill=A(WHITE, kn), outline=A(NAVY, kn), r=24, w=5)
        text(d, (W / 2, 650), "Chưa nói được", 46, NAVY, alpha=kn)
        for j, l in enumerate(("• Cản lớn hơn: đỉnh ra sao?", "• Số minh hoạ, chưa đo thật")):
            text(d, (100, 720 + j * 70), l, 44, INK, anchor="lm", alpha=kn * appear(t, M[1] + 0.3 + 0.5 * j, 0.4))
    axes(d)
    kv = appear(t, 0.8, 0.4)
    if kv > 0:
        for y in range(int(GY0 - 10), int(GY1), 24):
            d.line([(gx(F0), y), (gx(F0), y + 12)], fill=A(GREEN, kv), width=4)
        rich(d, gx(F0) + 60, GY0 - 10, "f_{0}", 44, GREEN, alpha=kv)
    curve(d, clamp((t - 1.0) / 1.6))
    for f, a_ in ROWS: point(d, f, a_, 1.0)

# ---------------- canh 4: Bay - "luc manh moi la cong huong" ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    y0 = 300
    card(d, (40, y0, 1040, y0 + 330), fill=WHITE, outline=(185, 28, 28), w=6)
    pill(d, W / 2, y0 + 62, "BẪY", 40, WHITE, (185, 28, 28))
    q = "✗ “Lực mạnh mới gây cộng hưởng”"
    f = F(46); lw = tw(d, q, f); yy = y0 + 200
    text(d, (W / 2, yy), q, 46, (185, 28, 28))
    ks = clamp((t - (M[1] + 2.0)) / 0.4)
    if ks > 0:
        d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=(140, 15, 15), width=7)
    # hai lan do, cung mo-to (cung luc), chi doi f -> thanh bien do cung thang 95 px/cm
    kb = appear(t, 0.3, 0.4)
    text(d, (W / 2, 730), "Cùng mô-tơ, chỉ đổi f", 44, NAVY, alpha=kb)
    for j, (f_, a_, col) in enumerate(((3.0, 2.7, BLUE), (2.0, 6.0, ORANGE))):
        y = 850 + j * 150
        text(d, (60, y), fs(f_) + " Hz", 44, INK, anchor="lm", alpha=kb)
        w_ = a_ * 95
        if w_ > 2: d.rounded_rectangle([260, y - 32, 260 + w_, y + 32], radius=12, fill=A(col, kb))
        text(d, (260 + w_ + 20, y), fs(a_) + " cm", 44, col, anchor="lm", alpha=kb)
    kc = appear(t, M[1] + 2.4, 0.5)
    if kc > 0:
        card(d, (60, 1140, 1020, 1330), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=24, w=4)
        rich(d, W / 2, 1200, "✓ Cộng hưởng khi f trùng f_{0}", 48, (21, 110, 55), alpha=kc)
        text(d, (W / 2, 1272), "không phải khi lực mạnh", 44, (21, 110, 55), alpha=kc)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 290, 1020, 510), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    rich(d, W / 2, 400, "Biên độ cực đại khi f = f_{0}", 54, GREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 570, 1040, 1520), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 600, W / 2 + pw / 2, 664), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 632), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 800, "Đặt f = 3,5 Hz. Biên độ ổn định\nlớn hơn hay nhỏ hơn 2,7 cm?",
          48, INK, maxw=930, alpha=appear(t, M[0] + 0.4, 0.5))
    # hinh nho: dong ho tan so 3,5 Hz, thanh bien do de trong "?"
    card(d, (330, 980, 750, 1100), fill=A(WHITE, k1), outline=A(NAVY, k1), r=20, w=4)
    text(d, (540, 1040), "3,5 Hz", 52, NAVY, alpha=k1)
    text(d, (540, 1170), "A = ? cm", 48, ORANGE, alpha=k1)
    kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
    if kh > 0:
        card(d, (110, 1260, 970, 1460), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1310), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1395), "Nhìn lại đồ thị vừa quét", 44, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]
    out += [(do["t0"] + T0S + j * STEP + READ, "tap") for j in range(5)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-tatdan-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Tắt dần · cưỡng bức · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Mô-tơ lắc con lắc lò xo", draw=s_hook, tail=0.6, caps=[
   ("Mô-tơ lệch tâm lắc lò xo.", 3.4),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Mỗi tần số, chờ ổn định rồi đọc.", 4.8),
   ("Chấm từng số đọc lên đồ thị.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Đỉnh trùng tần số riêng.", 5.0),
   ("Mới thử một mức lực cản.", 5.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: lực mạnh là cộng hưởng?", 3.0),
   ("Có đúng không?", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.2)]),
])
