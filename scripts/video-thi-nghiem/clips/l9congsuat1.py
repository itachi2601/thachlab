# Clip: tn-l9-congsuat-01 - Do U, I cua bong den 6 V - 3 W, tinh tich U.I (KHTN 9, 05/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-congsuat-01.json:
#   so_lieu_mau (U V, I A, U.I W): 1,5 0,22 0,33 ; 3,0 0,33 0,99 ; 4,5 0,42 1,89 ; 6,0 0,50 3,0 (ghi_chu: so lieu minh hoa).
#   quan_sat: do mo, sang yeu, kha sang, sang binh thuong o 6 V. tham_so: U_dm = 6,0 V, P_dm = 3,0 W.
#   ket_qua_ky_vong: U tang 4 lan thi U.I tang khoang 9 lan (bay = hien_tuong_hay_sai[1]).
#   chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet[1] (bo qua dien tro ampe ke, day noi).
# Cau hoi ngay sau hop trong bai (Cau 1: lam gi cho U.I dang tin hon -> do lap) KHONG duoc giai/goi y trong clip:
#   khong noi do lap, khong noi ampe ke do chia tho, khong noi "qua 6 V".
# Du doan (K10: chi cau hoi + hinh): dat 3,0 V vao den 6 V - 3 W, tich U.I khoang bao nhieu? -> khoang 1 W (0,99).
#   Khac han tn-l9-congsuat-03 (hai bong noi tiep/song song).
# Cau hoi chot: dat 5,0 V (chua tung hien) -> U.I nam giua 1,89 W va 3,0 W (giua hai lan do, khong ngoai suy).
# Mach: nguon (+) -> K -> ampe ke (+ ben trai) -> den -> ve (-); von ke SONG SONG hai dau den (+ ben nut phia nguon +).
#   K mo: 0,0 V ; 0,00 A ; den tat. Moi nac: nguon, so chi, do sang doi CUNG luc; hang bang hien sau 0,4 s.
#   Kiem bang ma moi 0,05 s: _kiem_dong_bo(); P = U.I tung hang: _kiem_so().
# Bo cuc (khac congsuat1/ohm3 cua L10-L11): so do mach + hai o so chi + bang 4 cot; Rut ra = cot U.I kem 4 bong nho.
import math
from engine import *

ROWS = [(1.5, 0.22, 0.33), (3.0, 0.33, 0.99), (4.5, 0.42, 1.89), (6.0, 0.50, 3.0)]   # so_lieu_mau
SANG = ("đỏ mờ", "sáng yếu", "khá sáng", "sáng bình thường")                                  # quan_sat
LV = (0.25, 0.5, 0.75, 1.0)
FIL = ((160, 45, 30), (215, 90, 25), (230, 140, 10), (225, 160, 0))
U_DM, P_DM = 6.0, 3.0
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); GLOW = (255, 214, 80)

# ---------------- so do mach ----------------
TY, BY, XL, XR = 380, 690, 150, 990
KX0, KX1, AX, LX, L1, L2, VY = 250, 330, 450, 760, 640, 880, 560

def bulb(d, cx, cy, r, lvl):
    """lvl = -1 (tat) hoac 0..3."""
    if lvl >= 0:
        b = LV[lvl]
        for i in range(4, 0, -1):
            rr = r + (12 * i * b + 10 * b) * r / 46
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=A(GLOW, 0.10 + 0.07 * b))
    fill = WHITE if lvl < 0 else mix(WHITE, (255, 226, 110), 0.2 + 0.8 * LV[lvl])
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=NAVY, width=6)
    q = r * 0.68; col = NAVY if lvl < 0 else FIL[lvl]
    d.line([(cx - q, cy - q), (cx + q, cy + q)], fill=col, width=6)
    d.line([(cx - q, cy + q), (cx + q, cy - q)], fill=col, width=6)

def circuit(d, closed, lvl, u):
    card(d, (40, 260, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    d.line([(XL, 445), (XL, TY), (KX0, TY)], fill=WIRE, width=w, joint="curve")
    d.line([(KX1, TY), (AX - 44, TY)], fill=WIRE, width=w)
    d.line([(AX + 44, TY), (LX - 46, TY)], fill=WIRE, width=w)
    d.line([(LX + 46, TY), (XR, TY), (XR, BY), (XL, BY), (XL, 625)], fill=WIRE, width=w, joint="curve")
    d.line([(L1, TY), (L1, VY), (LX - 44, VY)], fill=WIRE, width=5, joint="curve")
    d.line([(LX + 44, VY), (L2, VY), (L2, TY)], fill=WIRE, width=5, joint="curve")
    for p in ((L1, TY), (L2, TY)): dot(d, p[0], p[1], 9, WIRE)
    # nguon chinh duoc: hop + nup xoay
    card(d, (95, 445, 205, 625), fill=BODY, r=16)
    dot(d, 150, 535, 34, WHITE)
    ang = math.radians(-225 + 270 * u / U_DM)
    d.line([(150, 535), (150 + 26 * math.cos(ang), 535 + 26 * math.sin(ang))], fill=ORANGE, width=7)
    text(d, (70, 462), "+", 44, ORANGE); text(d, (70, 608), "−", 44, ORANGE)
    text(d, (225, 535), "nguồn", 40, INK, anchor="lm")
    # khoa K
    dot(d, KX0, TY, 9, WIRE); dot(d, KX1, TY, 9, WIRE)
    if closed: d.line([(KX0, TY), (KX1, TY)], fill=NAVY, width=7)
    else: d.line([(KX0, TY), (KX0 + 80 * math.cos(math.radians(32)), TY - 80 * math.sin(math.radians(32)))], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, TY + 46), "K", 40, NAVY)
    # ampe ke noi tiep, von ke song song
    d.ellipse([AX - 44, TY - 44, AX + 44, TY + 44], fill=WHITE, outline=BLUE, width=6); text(d, (AX, TY + 2), "A", 44, BLUE)
    text(d, (AX - 66, TY + 40), "+", 40, BLUE)
    d.ellipse([LX - 44, VY - 44, LX + 44, VY + 44], fill=WHITE, outline=PURPLE, width=6); text(d, (LX, VY + 2), "V", 44, PURPLE)
    text(d, (LX - 66, VY - 40), "+", 40, PURPLE)
    bulb(d, LX, TY, 46, lvl if closed else -1)
    text(d, (655, 300), "đèn 6 V – 3 W", 40, INK, anchor="rm")
    if closed:
        arrow(d, (560, BY + 34), (480, BY + 34), RED, w=5, head=16)
        text(d, (580, BY + 34), "I", 40, RED, anchor="lm")

def readouts(d, uv, ia, alpha=1.0):
    for x0, lab, val in ((60, "hiệu điện thế U", uv), (560, "cường độ dòng điện I", ia)):
        card(d, (x0, 790, x0 + 460, 950), fill=A(BODY, alpha), r=22)
        text(d, (x0 + 230, 830), lab, 40, WHITE, bold=False, alpha=alpha)
        card(d, (x0 + 30, 862, x0 + 430, 934), fill=A(SCREEN, alpha), r=12)
        text(d, (x0 + 230, 898), val, 54, SCR_INK, alpha=alpha)

XS = (160, 365, 630, 895)
def table(d, n, y=980, ui=None, hl=None, alpha=1.0):
    """n = so hang da ghi; ui(j) -> alpha cot U.I (None = an cot)."""
    card(d, (40, y, 1040, y + 560), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, h in zip(XS[:3], ("U (V)", "I (A)", "đèn")): text(d, (x, y + 60), h, 44, INK, alpha=alpha)
    if ui is not None: text(d, (XS[3], y + 60), "U·I (W)", 44, ORANGE, alpha=alpha * ui(-1))
    d.line([(70, y + 110), (1010, y + 110)], fill=A(LIGHT, alpha), width=3)
    for j, (u, i, p) in enumerate(ROWS):
        yy = y + 170 + j * 100
        if hl == j: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=20, fill=A((255, 237, 213), alpha))
        if j < n:
            text(d, (XS[0], yy), vn(u), 48, NAVY, alpha=alpha)
            text(d, (XS[1], yy), vn(i, 2), 48, BLUE, alpha=alpha)
            text(d, (XS[2], yy), SANG[j], 44, mix(FIL[j], INK, 0.3), alpha=alpha)
        else:
            for x in XS[:3]: text(d, (x, yy), "·", 44, GRAY, alpha=alpha)
        if ui is not None:
            k = ui(j)
            if k > 0: text(d, (XS[3], yy), vn(p, 2 if p < 2.99 else 1), 48, ORANGE, alpha=alpha * k)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
THINK_END = 0.7          # thanh dem + tieng 'ding' ket thuc truoc het canh 0,7 s (diem dung khung = T - 0,15)
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, False, -1, 0.0)
    readouts(d, "? V", "? A")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 990 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 245, "Đặt U = 3,0 V vào đèn.\nTích U·I khoảng\nbao nhiêu oát?", 50, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 420, 940, y0 + 432], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 420, 140 + 800 * (1 - p), y0 + 432], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T_S = (0.8, 2.8, 4.8, 6.8)    # dong K + dat nac 1 ; nac 2..4
T_ROW = 0.4                   # hang bang hien sau khi so chi doi
def do_state(t):
    """-> (K dong?, chi so nac dang dat hoac -1, so hang da ghi)."""
    k = sum(1 for ts in T_S if t >= ts - 1e-9) - 1
    n = sum(1 for ts in T_S if t >= ts + T_ROW - 1e-9)
    return k >= 0, k, n

def s_do(img, d, t, sc):
    closed, k, n = do_state(t)
    if closed:
        u, i, _ = ROWS[k]; circuit(d, True, k, u); readouts(d, vn(u) + " V", vn(i, 2) + " A")
    else:
        circuit(d, False, -1, 0.0); readouts(d, "0,0 V", "0,00 A")
    table(d, n, hl=(n - 1 if n > 0 else None))

def _kiem_dong_bo():
    """Moi 0,05 s: K mo <=> chua hang nao, den tat; K dong <=> so chi = nac k, hang cuoi da ghi la k hoac k - 1."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        closed, k, n = do_state(t)
        if not closed and n != 0: bad.append((round(t, 2), "mo", k, n))
        if closed and n not in (k, k + 1): bad.append((round(t, 2), "dong", k, n))
        t += 0.05
    return bad

def _kiem_so():
    return [r for r in ROWS if abs(r[0] * r[1] - r[2]) > 0.006] + \
           ([] if (ROWS[-1][0], ROWS[-1][2]) == (U_DM, P_DM) else ["dinh muc"])

# ---------------- canh 3: Ket qua ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · khoảng 1 W"
    pw = tw(d, lab, F(42)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 344), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 308), lab, 42, WHITE, alpha=ka)
    ui = lambda j: appear(t, 0.3, 0.4) if j < 0 else appear(t, 0.6 + 0.35 * j, 0.35)
    table(d, 4, y=390, ui=ui, hl=1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 300), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, y0 + 90), "P = U·I", 64, GREEN, alpha=k2)
        text(d, (W / 2, y0 + 200), "P: công suất điện (oát, W)", 42, DGREEN, alpha=k2)

# ---------------- canh 4: Rut ra (cot U.I + 4 bong nho) ----------------
GX0, GBASE, GTOP = 150, 840, 400
def gy(p): return GBASE - p / 3.4 * (GBASE - GTOP)
BXS = (280, 470, 660, 850)
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 1060), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GTOP - 30), (GX0, GBASE)], fill=NAVY, width=4)
    d.line([(GX0, GBASE), (990, GBASE)], fill=NAVY, width=4)
    text(d, (GX0 + 20, 320), "U·I (W)", 42, ORANGE, anchor="lm")
    for j, (u, i, p) in enumerate(ROWS):
        g = ease((t - 0.3 - 0.3 * j) / 0.6)
        h = (GBASE - gy(p)) * g
        if h > 2: d.rectangle([BXS[j] - 55, GBASE - h, BXS[j] + 55, GBASE], fill=ORANGE)
        if g > 0.95: text(d, (BXS[j], gy(p) - 32), vn(p, 2 if p < 2.99 else 1), 42, ORANGE)
        text(d, (BXS[j], GBASE + 38), vn(u) + " V", 40, INK)
        bulb(d, BXS[j], 985, 30, j if g > 0.95 else -1)
    kd = appear(t, M[1] - 0.2, 0.4)
    if kd > 0:
        yd = gy(P_DM)
        for x in range(GX0, 990, 30): d.line([(x, yd), (x + 16, yd)], fill=A(DGREEN, kd), width=4)
        text(d, (GX0 + 20, yd - 34), "ghi trên đèn: 3 W", 40, DGREEN, anchor="lm", alpha=kd)
    k1 = appear(t, M[0] + 1.2, 0.45)
    card(d, (40, 1100, 1040, 1250), fill=A((255, 247, 237), k1), outline=A(ORANGE, k1), w=4)
    text(d, (W / 2, 1175), "U·I lớn hơn → đèn sáng hơn", 46, (154, 52, 18), alpha=k1)
    k2 = appear(t, M[1] + 0.2, 0.45)
    card(d, (40, 1290, 1040, 1500), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
    text(d, (W / 2, 1355), "Đúng 6,0 V: U·I = 3,0 W", 46, DGREEN, alpha=k2)
    text(d, (W / 2, 1435), "khớp số ghi trên đèn", 46, DGREEN, alpha=k2)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 700), fill=WHITE, outline=LIGHT, w=3)
    rows = (("U", "1,5 V", "6,0 V", "× 4", NAVY), ("I", "0,22 A", "0,50 A", "tăng", BLUE),
            ("U·I", "0,33 W", "3,0 W", "× 9", ORANGE))
    kv = appear(t, M[0] + 2.4, 0.4)
    for j, (s, a, b, r, c) in enumerate(rows):
        yy = 350 + j * 130
        text(d, (90, yy), s, 46, c, anchor="lm")
        text(d, (330, yy), a, 46, c); arrow(d, (430, yy), (500, yy), c, w=5, head=16); text(d, (600, yy), b, 46, c)
        if j < 2 or kv > 0: text(d, (845, yy), r, 44, c, alpha=1.0 if j < 2 else kv)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 760
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        q = "“U gấp 4 thì U·I gấp 4”"
        ks = clamp((t - M[0] - 2.2) / 0.4)
        f = F(48); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2, yy), q, 48, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 + lw / 2 + 40, yy), "✗", 48, DRED, alpha=a1 * ks)
        kk = a1 * kv
        card(d, (70, y0 + 290, 1010, y0 + 520), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 360), "✓ U gấp 4 nhưng U·I gấp khoảng 9:", 44, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 445), "không tỉ lệ", 46, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 760 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, (l1, l2) in enumerate((("• Số liệu minh hoạ,", "chưa đo thật"),
                                      ("• Bỏ qua điện trở", "ampe kế, dây nối"))):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (80, y0 + 190 + j * 160), l1, 44, INK, anchor="lm", alpha=kk)
            text(d, (118, y0 + 250 + j * 160), l2, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
        card(d, (110, 1260, 970, 1500), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1315, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1415, "So 5,0 V với các lần đo", 44, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Đủ 3 W chỉ khi đặt đúng 6 V",
             "Đặt 5,0 V vào đèn. U·I trong khoảng nào?", body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"), (do["t0"] + T_S[0], "tap")]
    out += [(do["t0"] + ts, "tick") for ts in T_S[1:]]
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.2, "tap"), (b["t0"] + 0.2, "buzz"),
            (b["t0"] + b["M"][0] + 2.4, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-congsuat-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Công suất điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bóng đèn ghi 6 V – 3 W", draw=s_hook, tail=0.8, caps=[
   ("Mạch đo U và I của đèn.", 2.9),
   ("Dừng video, chọn câu trả lời.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đóng K, tăng U từng nấc.", 4.0),
   ("Mỗi nấc: đọc I, xem độ sáng.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Nhân U với I mỗi lần.", 3.2),
   ("Một nửa U, U·I chưa tới một nửa.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("So độ sáng với cột.", 3.2),
   ("Đó là công suất định mức.", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Có đúng không?", 3.8),
   ("Còn chưa nói được.", 3.9)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch P = U·I:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
