# Clip: tn-l11-tudien-02 - Do Q theo U (ban 2 cong moi, 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-tudien-02.json:
#   so_lieu_mau (U V, Q uC): 2 980 ; 4 1900 ; 6 2890 ; 8 3820 ; 10 4800 ; tu ghi 470 uF - 16 V (dung_cu).
# Du doan (khung, K10 khong ve nut): ve Q theo U, cac diem nam tren duong nao?
#   A. thang, qua goc (DUNG) ; B. cong, doc dan ; C. cong, thoai dan ; D. thang, khong qua goc.
#   Doi so voi ban cu (Q/U doi the nao?) vi bang Q/U in san trong hop exp va Bay 1 cua bai hoi dung y do.
# KHONG LO QUIZ sau hop ("Tu bang: nen bao C bao nhieu?" A 490, B 470 tren vo, C ~480 trung binh, D 4800):
#   clip KHONG chieu "trung binh 481", khong chieu cot Q/U, khong noi "lan 2 V lech nhieu nhat", khong bay 470.
# Bay (sai_so_thuong_gap[0]): cho lau moi gat K -> tu ro dien, Q do nho hon (hai truong hop canh nhau, khong so moi).
# Cau chot (tu suy trong dai tham_so U 0-12 V, C = 480 uF co_dinh): nap 12 V -> Q = 480 . 12 = 5760 uC.
#   Clip khong chieu so 5760, khong chieu duong thang keo toi 12 V. Nhieu: 40 (C/U), 4800 (Q lon nhat), 6900 (Q ~ U^2).
# Mach (vat li): nguon (+) tren -> K vi tri 1 -> ban + (tren) cua tu ; ban - -> day chung -> nguon (-).
#   Phong: K sang 2, dong tu ban + qua bo do roi ve ban - qua day chung.
from engine import *

ROWS = [(2, 980), (4, 1900), (6, 2890), (8, 3820), (10, 4800)]          # so_lieu_mau
C_MO_HINH = 480
assert round(C_MO_HINH * 12) == 5760 and all(abs(q / u - C_MO_HINH) / C_MO_HINH < 0.025 for u, q in ROWS)
DRED = (185, 28, 28); DGREEN = (21, 110, 55)
WIRE = NAVY; BOXF = (70, 78, 100); SCR = (220, 240, 225); ARR = (194, 65, 12); EMPTY = (148, 140, 128)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- mach ----------------
YT, YR = 320, 820
C1, C2, P = (440, YT), (640, YT), (540, 410)
XC = 540; XS, XM = 140, 925                     # truc nguon, truc bo do

def wire(d, pts, w=6): d.line(pts, fill=WIRE, width=w, joint="curve")

def circuit(d, blade=0.0, ushow="0 V", qread="0 μC", charge=0.0, mode=None):
    wire(d, [(XS, 440), (XS, YT), (C1[0], YT)])
    wire(d, [(C2[0], YT), (XM, YT), (XM, 440)])
    wire(d, [P, (XC, 552)])
    wire(d, [(XC, 612), (XC, YR)])
    wire(d, [(XS, 700), (XS, YR), (XM, YR), (XM, 700)])
    dot(d, XC, YR, 10, WIRE)
    for i, (c, lab) in enumerate(((C1, "1"), (C2, "2"))):
        on = (blade < 0.5) if i == 0 else (blade >= 0.5)
        dot(d, c[0], c[1], 15 if on else 13, WIRE if on else WHITE, outline=WIRE)
        text(d, (c[0] + (-60 if i == 0 else 60), c[1] - 50), lab, 58, INK)
    ang0, ang1 = math.atan2(C1[1] - P[1], C1[0] - P[0]), math.atan2(C2[1] - P[1], C2[0] - P[0])
    ang = lerp(ang0, ang1, ease(blade)); L = math.hypot(C1[0] - P[0], C1[1] - P[1])
    d.line([P, (P[0] + L * math.cos(ang), P[1] + L * math.sin(ang))], fill=WIRE, width=9)
    dot(d, P[0], P[1], 14, WIRE)
    text(d, (P[0] + 40, P[1] + 30), "K", 60, INK, anchor="lm")
    d.rectangle([470, 548, 610, 558], fill=WIRE); d.rectangle([470, 604, 610, 616], fill=WIRE)
    text(d, (455, 540), "470 μF", 56, INK, anchor="rm"); text(d, (455, 625), "16 V", 56, INK, anchor="rm")
    if charge > 0:
        for x in (495, 585):
            text(d, (x, 506), "+", 60, RED, alpha=charge); text(d, (x, 660), "−", 60, BLUE, alpha=charge)
    card(d, (30, 440, 250, 700), fill=BOXF, r=22)
    text(d, (XS, 490), "nguồn", 56, WHITE)
    card(d, (45, 540, 235, 640), fill=SCR, r=10); text(d, (XS, 590), ushow, 60, (20, 60, 30))
    text(d, (XS + 60, 400), "+", 60, RED); text(d, (XS + 60, 745), "−", 60, BLUE)
    card(d, (785, 440, 1045, 700), fill=BOXF, r=22)
    card(d, (797, 460, 1033, 560), fill=SCR, r=10); text(d, (915, 510), qread, 56, (20, 60, 30))
    text(d, (915, 625), "đo Q", 58, WHITE)
    if mode == "nap":
        for p1, p2 in (((XS, 425), (XS, 345)), ((230, YT), (370, YT)), ((XC, 470), (XC, 535)), ((440, YR), (290, YR))):
            arrow(d, p1, p2, ARR, w=11, head=30)
    elif mode == "phong":
        for p1, p2 in (((XC, 535), (XC, 470)), ((690, YT), (840, YT)), ((XM, 345), (XM, 425)), ((840, YR), (690, YR))):
            arrow(d, p1, p2, ARR, w=11, head=30)

def table(d, n, y=900, hl=()):
    card(d, (140, y, 940, y + 110 + 80 * 5), fill=WHITE, outline=NAVY, w=4)
    xs = (360, 720)
    for x, c in zip(xs, ("U (V)", "Q (μC)")): text(d, (x, y + 55), c, 58, INK)
    d.line([(170, y + 100), (910, y + 100)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 145 + i * 80; u, q = ROWS[i]
        if i in hl: d.rounded_rectangle([160, yy - 37, 920, yy + 37], radius=18, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(u), 58, INK); text(d, (xs[1], yy), str(q), 58, INK)

# ---------------- truc Q-U ----------------
def axes(d, x0, y0, x1, y1, umax, qmax, a=1.0, ticks=(2, 4, 6, 8, 10), lq="Q", lu="U"):
    gx = lambda u: x0 + u / umax * (x1 - x0); gy = lambda q: y0 - q / qmax * (y0 - y1)
    c = A(NAVY, a)
    d.line([(x0, y1 - 20), (x0, y0)], fill=c, width=5); d.line([(x0, y0), (x1 + 20, y0)], fill=c, width=5)
    arrow(d, (x0, y1 - 10), (x0, y1 - 36), c, w=5, head=18); arrow(d, (x1 + 10, y0), (x1 + 36, y0), c, w=5, head=18)
    text(d, (x0 + 25, y1 - 30), lq, 60 if len(lq) < 2 else 56, INK, anchor="lm", alpha=a)
    text(d, (x1 + 30, y0 - 50), lu, 60 if len(lu) < 2 else 56, INK, anchor="rm", alpha=a)
    for u in ticks:
        d.line([(gx(u), y0), (gx(u), y0 + 12)], fill=c, width=4); text(d, (gx(u), y0 + 48), str(u), 56, INK, alpha=a)
    return gx, gy

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, ushow="2 V" if t > 1.4 else "0 V")
    a = appear(t, M[1] - 0.2, 0.4)
    if a <= 0: return
    y0 = 870 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 710), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 185), "Vẽ Q theo U, năm điểm đo", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "nằm trên đường nào?", 62, PURPLE, alpha=a)
    axes(d, 400, y0 + 560, 680, y0 + 410, 10, 5000, a=a, ticks=())
    seg_bar(d, y0 + 605, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
FF0, FFW, SW, TSW = 0.2, 1.5, 0.75, 2.8

def s_do(img, d, t, sc):
    M = sc["M"]
    if t < M[1]:
        u, q = ROWS[0]; done = t >= TSW
        circuit(d, 1.0 if done else 0.0, f"{u} V", f"{q} μC" if done else "0 μC",
                0.0 if done else clamp((t - 0.6) / 1.0),
                "nap" if 0.6 <= t < 1.8 else ("phong" if TSW <= t < TSW + 1.0 else None))
        table(d, 1 if done else 0)
        return
    w_all = t - M[1] - FF0
    if w_all < 0:
        circuit(d, 1, "2 V", "980 μC"); table(d, 1)
    else:
        j = 1 + max(0, min(3, int(w_all // FFW))); w = w_all - (j - 1) * FFW
        u, q = ROWS[j]
        if w < SW: circuit(d, 0.0, f"{u} V", "0 μC", clamp(w / 0.25), "nap" if w < 0.5 else None); table(d, j)
        else: circuit(d, 1, f"{u} V", f"{q} μC", 0, "phong" if w < SW + 0.45 else None); table(d, j + 1)
    pill(d, 900, 245, "tua nhanh", ORANGE, appear(t, M[1], 0.25), size=56)

# ---------------- canh 3: Ket qua ----------------
GX0, GY0, GX1, GY1 = 200, 860, 900, 360

def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 980), fill=WHITE, outline=LIGHT, w=3)
    gx, gy = axes(d, GX0, GY0, GX1, GY1, 11, 5500, lq="Q (μC)", lu="U (V)")
    for i, (u, q) in enumerate(ROWS):
        k = appear(t, 0.3 + 0.15 * i, 0.3)
        if k > 0: dot(d, gx(u), gy(q), 16, A(BLUE, k), outline=WHITE)
    kl = appear(t, 1.6, 0.9)
    if kl > 0:
        u1 = 10.5 * kl
        d.line([(gx(0), gy(0)), (gx(u1), gy(C_MO_HINH * u1))], fill=A(GREEN, 0.9), width=6)
    ka = appear(t, 2.4, 0.4)
    if ka > 0:
        card(d, (40, 1020, 1040, 1180), fill=A(WHITE, ka), outline=A(NAVY, ka), w=6)
        text(d, (W / 2, 1100), "Thẳng, đi qua gốc toạ độ", 64, NAVY, alpha=ka)
    k2 = appear(t, M[1] + 0.4, 0.4)
    if k2 > 0:
        for i in (1, 3):
            u, q = ROWS[i]
            d.ellipse([gx(u) - 34, gy(q) - 34, gx(u) + 34, gy(q) + 34], outline=A(ORANGE, k2), width=7)
        card(d, (40, 1220, 1040, 1380), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1300), "U gấp đôi, Q gần gấp đôi", 62, DGREEN, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
SIGN_X = [-45, 45, -88, 88, -130, 130]   # thu tu hien dau; tranh truc day dan o giua (khong cat hang dau)
def capq(d, cx, n, a=1.0):
    """Tu nho, n dau + / - con lai tren hai ban. Hai day dan: tren cham ban tren, duoi cham ban duoi (khong qua khe)."""
    c = A(WIRE, a)
    d.rectangle([cx - 155, 560, cx + 155, 572], fill=c); d.rectangle([cx - 155, 618, cx + 155, 630], fill=c)
    d.line([(cx, 470), (cx, 560)], fill=c, width=6); d.line([(cx, 630), (cx, 720)], fill=c, width=6)
    for dx in SIGN_X[:n]:
        text(d, (cx + dx, 522), "+", 58, RED, alpha=a); text(d, (cx + dx, 672), "−", 58, BLUE, alpha=a)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    pill(d, W / 2, 290, "BẪY", DRED, k0)
    text(d, (280, 400), "gạt K ngay", 58, DGREEN, alpha=k0)
    text(d, (800, 400), "chờ lâu mới gạt", 58, DRED, alpha=k0)
    lk = appear(t, M[1] - 0.2, 1.4)
    capq(d, 280, 6, k0); capq(d, 800, 6 - int(round(4 * lk)), k0)
    if lk > 0:
        for j in range(4):
            kk = appear(t, M[1] - 0.2 + 0.3 * j, 0.6)
            dx = SIGN_X[5 - j]
            if 0 < kk < 1: text(d, (800 + dx + (40 if dx > 0 else -40) * kk, 522 - 90 * kk), "+", 58, RED, alpha=k0 * (1 - kk))
    kd = appear(t, M[1], 0.4)
    card(d, (120, 780, 440, 880), fill=A(SCR, k0), r=12); text(d, (280, 830), "4800 μC", 58, (20, 60, 30), alpha=k0)
    if kd > 0:
        card(d, (640, 780, 960, 880), fill=A(SCR, kd), r=12); text(d, (800, 830), "nhỏ hơn", 58, DRED, alpha=kd)
    text(d, (W / 2, 960), "cùng nạp ở 10 V", 58, INK, alpha=k0)
    k3 = appear(t, M[2] - 0.1, 0.4)
    if k3 > 0:
        card(d, (40, 1080, 1040, 1420), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 1150, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 1300), "C phụ thuộc gì ở cấu tạo tụ?", 60, INK, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    gx, gy = axes(d, 220, 880, 880, 440, 12.5, 6500, a=k, ticks=(2, 4, 6, 8, 10, 12))
    for u, q in ROWS: dot(d, gx(u), gy(q), 15, A(BLUE, k), outline=WHITE)
    for yy in range(450, 870, 34): d.line([(gx(12), yy), (gx(12), yy + 18)], fill=A(ORANGE, k), width=5)
    text(d, (gx(12) - 50, 470), "?", 72, DRED, alpha=k)
    text(d, (W / 2, 1060), "Nạp tụ này ở 12 V.", 64, INK, alpha=k)
    text(d, (W / 2, 1160), "Q khoảng bao nhiêu μC?", 64, DRED, alpha=k)
    seg_bar(d, 1330, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + TSW, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW + SW, "tick") for j in range(4)]
    out += [(da["t0"] + 2.4, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-tudien-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Tụ điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nạp tụ, đo điện tích", draw=s_hook, tail=0.3, caps=[
   ("Nạp tụ ở U, rồi đo Q.", 3.2),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("K ở 1 nạp; K ở 2 phóng qua bộ đo.", 4.6),
   ("Lặp lại ở 4, 6, 8, 10 V.", 6.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Năm điểm và gốc thẳng hàng.", 4.0),
   ("Q tỉ lệ thuận với U.", 3.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy: chờ lâu mới gạt K.", 3.6),
   ("Tụ rò điện, Q đo hụt.", 3.6),
   ("Mới đo một tụ.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng lại, tự trả lời.", 7.2)]),
])
