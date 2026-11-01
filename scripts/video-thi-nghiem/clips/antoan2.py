# Clip: tn-l10-an-toan-02 - Nhiet do canh ngon den con theo khoang cach (1/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-an-toan-02.json:
#   so_lieu_mau: d = 2; 5; 10; 20 cm -> T = 125; 41; 29; 26 C, phan nong them T - 25 = 100; 16; 4; 1 C.
#   tham_so: T_phong = 25 C, nhiet ke do toi 200 C, sai so 1 C ; mo_hinh: T = 25 + 400/d^2 (chi dung cho cot chat
#   long khi dang doi gia do, KHONG hien so trung gian: khi dang doi, o so chi "dang dời…").
# Ban ve dung ti le: 1 cm = 38 px (thuoc 0-20 cm), bau nhiet ke dat dung d cm tinh tu truc ngon lua.
# Khong ve tay nguoi gan lua (giao vien doi gia do, lop dung xa).
# Du doan (K10: chi cau hoi + hinh): doi ra xa 2 -> 5 -> 10 -> 20 cm, nhiet do giam theo kieu nao?
#   Dap an: giam nhanh luc gan, cham dan khi xa. Nhieu: giam deu moi cm (hien_tuong_hay_sai 1) ; giam cham luc gan,
#   nhanh dan khi xa ; ngoai ngon lua gan nhu khong doi (hien_tuong_hay_sai 2).
# Truc chinh: HINH DUNG CU dung ti le + DO THI T-d (truc co dinh 0-20 cm, 20-130 C), khong bang (antoan1 dung bo
#   nguon + von ke, bo cuc rieng).
# Cau chot: o 4 cm (chua tung hien) phan nong them khoang bao nhieu? -> 25 C (phan xa sai: 50 C, "xa gap doi, con nua").
from engine import *

DS = [2, 5, 10, 20]                 # cm
TS = [125, 41, 29, 26]              # C
T_PH = 25
FX, PX = 180, 38                    # truc ngon lua (x), px moi cm
YB = 660                            # do cao bau nhiet ke = giua ngon lua
YTOP = 440                          # dinh ong nhiet ke (200 C)
LAMP = (200, 225, 240); LAMP_D = (120, 140, 160); FLAME_O = (251, 146, 60); FLAME_I = (59, 130, 246)
LIQ = (220, 38, 38); RULER = (254, 243, 199)

def xd(dcm): return FX + dcm * PX
def t_model(dcm): return T_PH + 400.0 / (dcm * dcm)        # mo_hinh kho (chi de ve cot chat long)

# ---------------- dung cu ----------------
def lamp(d, t):
    d.rounded_rectangle([92, 780, 268, 900], radius=46, fill=LAMP, outline=LAMP_D, width=5)
    d.rectangle([158, 748, 202, 786], fill=(203, 213, 225), outline=LAMP_D, width=4)
    d.rectangle([175, 734, 185, 750], fill=(68, 64, 60))
    w = 1 + 0.04 * math.sin(t * 9)                        # lua lay nhe
    top = 596 + 6 * math.sin(t * 7)
    def drop(cx, yb, hw, yt, col):
        pts = []
        for i in range(25):
            a = math.pi * i / 24
            pts.append((cx - hw * w * math.cos(a), yb - hw * 0.9 * math.sin(a)))
        pts.append((cx, yt))
        d.polygon(pts, fill=col)
    drop(FX, 738, 30, top, FLAME_O)
    drop(FX, 738, 16, top + 70, FLAME_I)

def thermo(d, dcm, tval, alpha=1.0):
    """nhiet ke thuy tinh tren gia do; bau o (xd(dcm), YB). tval: nhiet do cot chat long."""
    x = xd(dcm); c = lambda col: A(col, alpha)
    rx = x + 52
    d.rectangle([x + 22, 885, x + 82, 902], fill=c(NAVY))                       # de gia do
    d.rectangle([rx - 5, 470, rx + 5, 886], fill=c(GRAY), outline=c(NAVY), width=2)  # can
    d.rectangle([x + 6, 512, rx, 526], fill=c(GRAY))                            # tay kep
    d.rectangle([x - 14, 504, x + 14, 534], outline=c(NAVY), width=4)
    d.rounded_rectangle([x - 10, YTOP - 8, x + 10, YB - 8], radius=10, fill=c((241, 245, 249)), outline=c(NAVY), width=3)
    yl = YB - 14 - (YB - 14 - YTOP) * clamp(tval / 200.0)
    d.rectangle([x - 3, yl, x + 3, YB - 10], fill=c(LIQ))
    d.ellipse([x - 16, YB - 16, x + 16, YB + 16], fill=c(LIQ), outline=c(NAVY), width=3)

def ruler(d, marks=()):
    d.rectangle([FX - 20, 906, xd(20) + 36, 976], fill=RULER, outline=(180, 150, 80), width=3)
    for k in range(0, 21):
        L = 24 if k % 5 == 0 else 12
        d.line([(xd(k), 906), (xd(k), 906 + L)], fill=NAVY, width=3 if k % 5 == 0 else 2)
    for k in (0, 5, 10, 15, 20):
        text(d, (xd(k), 952), str(k), 40, INK)
    text(d, (xd(17.5), 952), "cm", 40, MUTED, bold=False)
    for m in marks:
        dot(d, xd(m), 898, 7, PURPLE)

def bench(d, t, dcm, tval, read=None, status=None, marks=(), alpha_th=1.0, dline=True, panel=True):
    """khung dung cu. read: (d_so, T_so) hien tren o so; status: chu thay so khi chua on dinh."""
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 902), (1020, 902)], fill=(180, 170, 150), width=4)            # mat ban
    ruler(d, marks)
    lamp(d, t)
    if dcm is not None:
        if dline:
            for yy in range(YB + 22, 902, 18):
                d.line([(xd(dcm), yy), (xd(dcm), min(yy + 9, 902))], fill=PURPLE, width=3)
        thermo(d, dcm, tval, alpha_th)
    # o so chi (co dinh, khong di theo nhiet ke)
    if not panel: return
    card(d, (330, 285, 1020, 420), fill=(248, 250, 252), outline=LIGHT, r=24, w=3)
    if read is not None:
        text(d, (360, 322), f"cách ngọn lửa {read[0]} cm", 40, PURPLE, anchor="lm")
        text(d, (360, 385), f"nhiệt kế {read[1]} °C", 48, RED, anchor="lm")
    else:
        text(d, (360, 322), "cách ngọn lửa", 40, MUTED, bold=False, anchor="lm")
        text(d, (360, 385), status or "nhiệt kế ?", 44, MUTED, anchor="lm")

# ---------------- do thi T theo d (truc co dinh) ----------------
GX0, GX1, GY0, GY1 = 200, 980, 1460, 1110          # d 0..20 cm ; T 20..130 C
def gx(dcm): return GX0 + (GX1 - GX0) * dcm / 20.0
def gy(T): return GY0 - (GY0 - GY1) * (T - 20) / 110.0

def graph(d, n, alpha=1.0, seg=None, bars=0.0, lab=True):
    card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    for T in (20, 40, 60, 80, 100, 120):
        d.line([(GX0, gy(T)), (GX1, gy(T))], fill=(240, 236, 228), width=2)
        text(d, (GX0 - 18, gy(T)), str(T), 40, INK, bold=False, anchor="rm")
    for k in (0, 5, 10, 15, 20):
        d.line([(gx(k), GY0), (gx(k), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(k), GY0 + 40), str(k), 40, INK, bold=False)
    d.line([(GX0, GY0), (GX1 + 20, GY0)], fill=NAVY, width=4)
    d.line([(GX0, GY0), (GX0, GY1 - 30)], fill=NAVY, width=4)
    text(d, (GX0 + 16, 1068), "T: nhiệt kế (°C)", 40, INK, anchor="lm")
    text(d, (GX1 + 20, 1556), "d: cách lửa (cm)", 40, INK, anchor="rm")
    for xx in range(GX0, GX1, 26):                                              # phong 25 C
        d.line([(xx, gy(25)), (min(xx + 13, GX1), gy(25))], fill=TEAL, width=3)
    if lab: text(d, (785, gy(25) - 34), "phòng 25 °C", 40, TEAL)
    if seg:                                                                      # to mau doan
        for (i, col, k) in seg:
            if k > 0:
                d.line([(gx(DS[i]), gy(TS[i])), (gx(DS[i + 1]), gy(TS[i + 1]))], fill=A(col, k), width=9)
    if bars > 0:                                                                 # phan nong them = T - 25
        for i in range(4):
            y0, y1 = gy(TS[i]), gy(T_PH)
            if y1 - y0 > 2:
                d.rectangle([gx(DS[i]) - 14, y0, gx(DS[i]) + 14, y1], fill=A(ORANGE, bars * 0.85))
    for i in range(n):
        x, y = gx(DS[i]), gy(TS[i])
        dot(d, x, y, 14, BLUE, WHITE)
        if not lab: continue
        s = ("+" + str(TS[i] - T_PH)) if bars > 0 else str(TS[i])
        col = ORANGE if bars > 0 else BLUE
        if i == 0: text(d, (x + 30, y + 4), s, 40, col, anchor="lm")
        elif i == 3: text(d, (x - 6, y - 44), s, 40, col, anchor="rm")
        else: text(d, (x, y - 44), s, 40, col)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    bench(d, t, 2, t_model(2), status="nhiệt kế ?", marks=DS, dline=False)
    text(d, (xd(2) + 90, 600), "nhiệt kế", 40, RED, anchor="lm")
    text(d, (FX, 845), "đèn cồn", 40, NAVY)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 55), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 170, "Dời nhiệt kế ra xa:", 48, INK, alpha=a)
    ctext(d, y0 + 245, "2 → 5 → 10 → 20 cm.", 48, PURPLE, alpha=a)
    ctext(d, y0 + 345, "Nhiệt độ giảm theo kiểu nào?", 50, INK, alpha=a)
    tc, tend = M[1] + 1.4, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 484], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 484], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
ARR = [0.8, 4.0, 7.2, 10.4]          # luc nhiet ke on dinh o tung vi tri (t canh)
MOVE = 1.0                            # doi gia do mat 1,0 s, roi doi on dinh
def state(t):
    """-> (d hien tai cm, chi so vi tri da on dinh hoac -1, nhiet do cot chat long)."""
    if t < ARR[0]:                                                   # vua dat o 2 cm, cot dang dang len
        k = ease(t / ARR[0]); return 2.0, -1, lerp(T_PH, TS[0], k)
    for i in range(3):
        dep = ARR[i + 1] - MOVE
        if t < dep: return float(DS[i]), i, float(TS[i])
        if t < ARR[i + 1]:
            dd = lerp(DS[i], DS[i + 1], ease((t - dep) / MOVE)); return dd, -1, t_model(dd)
    return float(DS[3]), 3, float(TS[3])

def s_do(img, d, t, sc):
    dd, k, tv = state(t)
    if k >= 0: bench(d, t, dd, tv, read=(DS[k], TS[k]), marks=DS)
    else: bench(d, t, dd, tv, status="nhiệt kế …", marks=DS)
    n = sum(1 for a in ARR if t >= a)
    graph(d, n)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · gần tụt nhanh, xa tụt chậm"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 330), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 296), lb, 40, WHITE, alpha=ka)
    card(d, (40, 370, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    k1, k2 = appear(t, 0.7, 0.4), appear(t, 2.0, 0.4)
    d.rounded_rectangle([90, 470, 150, 500], radius=8, fill=A(RED, k1))
    text(d, (180, 460), "2 → 5 cm", 44, INK, anchor="lm", alpha=k1)
    text(d, (180, 540), "tụt 84 °C", 52, RED, anchor="lm", alpha=k1)
    d.rounded_rectangle([90, 730, 150, 760], radius=8, fill=A(BLUE, k2))
    text(d, (180, 720), "10 → 20 cm", 44, INK, anchor="lm", alpha=k2)
    text(d, (180, 800), "tụt 3 °C", 52, BLUE, anchor="lm", alpha=k2)
    text(d, (180, 900), "125 − 41 = 84 ;  29 − 26 = 3", 40, INK, bold=False, anchor="lm", alpha=k2)
    graph(d, 4, seg=[(0, RED, k1), (2, BLUE, k2)])

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    kb = appear(t, 0.6, 0.6)
    if t < M[1] - 0.1:
        card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
        k0 = appear(t, 0.3, 0.4)
        text(d, (W / 2, 470), "Phần nóng thêm = T − 25", 50, ORANGE, alpha=k0)
        k1 = appear(t, 1.6, 0.4)
        text(d, (W / 2, 700), "5 → 10 cm:  16 → 4 °C", 52, RED, alpha=k1)
    else:
        k = appear(t, M[1] - 0.1, 0.45)
        card(d, (40, 265, 1040, 1000), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
        text(d, (W / 2, 350), "Chưa nói được quy luật chính xác", 46, NAVY, alpha=k)
        kk = k * appear(t, M[1] + 0.3, 0.4)
        card(d, (80, 560, 1000, 820), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, 690), "Số minh hoạ, chưa là quy luật", 48, RED, alpha=kk)
    graph(d, 4, bars=kb)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    bench(d, t, 5, TS[1], panel=False)
    text(d, (xd(5) + 90, 470), "41 °C", 52, RED, anchor="lm")
    d.line([(FX + 34, 640), (xd(5) - 22, 640)], fill=PURPLE, width=3)
    text(d, (xd(5) + 90, 600), "ngoài ngọn lửa", 40, PURPLE, anchor="lm")
    a1 = appear(t, 0.15, 0.4); y0 = 1030
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 58), "BẪY", 38, WHITE, alpha=a1)
    cl = "✗ “Ra khỏi ngọn lửa là hết nóng”"
    text(d, (W / 2, y0 + 170), cl, 46, RED, alpha=a1)
    hw = tw(d, cl, F(46)) / 2
    d.line([(W / 2 - hw + 50, y0 + 172), (W / 2 + hw, y0 + 172)], fill=A(RED, a1), width=4)
    kk = appear(t, M[0] + 2.6, 0.5)
    card(d, (90, y0 + 270, 990, y0 + 470), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, y0 + 370), "✓ Vẫn hơn phòng 16 °C", 48, GREEN, alpha=kk)

# ---------------- canh 6: Chot ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):
        y = 1150; x0, s = 150, 36                       # thuoc nho: 1 cm = 36 px (0..20 cm), dung ti le
        d.polygon([(x0 - 18, y - 10), (x0 + 18, y - 10), (x0, y - 80)], fill=A(FLAME_O, k))
        d.line([(x0, y), (x0 + 20 * s + 20, y)], fill=A(NAVY, k), width=4)
        for c in (0, 5, 10, 15, 20):
            d.line([(x0 + c * s, y), (x0 + c * s, y + 16)], fill=A(NAVY, k), width=3)
            text(d, (x0 + c * s, y + 46), str(c), 40, INK, bold=False, alpha=k)
        text(d, (x0 + 20 * s + 30, y + 46), "cm", 40, MUTED, bold=False, anchor="lm", alpha=k)
        for c, lb, col in ((10, "+4 °C", BLUE), (15, "?", ORANGE), (20, "+1 °C", BLUE)):
            dot(d, x0 + c * s, y - 30, 12, A(col, k))
            text(d, (x0 + c * s, y - 74), lb, 52 if lb == "?" else 40, col, alpha=k)
        kh = appear(t, M[0] + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Xem lại cặp 10 cm và 20 cm.", 42, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Nung nóng: luôn đứng xa an toàn",
             "Ở 15 cm, phần nóng thêm\nkhoảng bao nhiêu?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    cs += [(do["t0"] + a, "tap") for a in ARR]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + 0.15, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-an-toan-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="An toàn phòng thực hành · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đèn cồn và nhiệt kế", draw=s_hook, tail=0.5, caps=[
   ("Lớp đứng xa. Phòng 25 °C.", 2.9),
   ("Dừng video, chọn câu trả lời.", 6.3)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Dời giá đỡ, đợi số ổn định.", 6.0),
   ("Chấm điểm lên đồ thị.", 5.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("So hai đoạn tô màu.", 4.8)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Tính từ mức phòng 25 °C.", 4.0),
   ("Chưa đủ số để kết luận.", 4.4)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("Có đúng không?", 4.7)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])
