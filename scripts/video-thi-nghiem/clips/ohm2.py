# Clip: tn-l11-dien-tro-ohm-02 - Do U va I cua den soi dot 6 V - 3 W: ha U con mot nua thi I? (ban 2 cong moi, 27/11/2026)
# Ban 2: chu >= 56 px, bang doc 6 hang o Tien hanh, Ket qua = thanh so sanh, bo the Goi y, nhip Bay >= 3 s.
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-tro-ohm-02.json (ghi_chu "Khong phai so do that" -> nhan
#   "số liệu mô phỏng"): so_lieu_mau (U V, I A, U/I Ohm): 1,0 0,17 5,9 ; 2,0 0,26 7,7 ; 3,0 0,33 9,1 ; 4,0 0,39 10,3 ;
#   5,0 0,45 11,1 ; 6,0 0,50 12,0. Kiem: I = round(0,1706.U^0,6; 2) va U/I = round(U/I; 1) (_kiem_so()).
#   Duong cong = mo_hinh I = k.U^0,6 CHI ve tu 1 V tro len (gia_thiet: khong ngoai suy duoi 1 V).
#   Duong thang 12 Ohm O-(6 V; 0,50 A) = goi_y_mo_phong + ket_qua_ky_vong ("diem do nam phia tren").
# Du doan (K10, khung ben canh co lua chon): den o 6,0 V cho 0,50 A; ha U con mot nua (3,0 V), I so voi 0,50 A?
#   A. Dung mot nua, nhu dien tro ; B. Hon mot nua (DUNG: 0,33 A) ; C. Chua toi mot nua ; D. Van 0,50 A.
#   Clip ohm1 (dien tro) KHONG tra loi san: o do ha U con nua thi I con nua -> chinh la moi nhu A.
# KHONG tra loi san cau trong bai: q4 (vi sao R den 7,7 Ohm o 2 V nhung 12 Ohm o 6 V -> clip KHONG noi nguyen nhan
#   nhiet do; "Vi sao U/I tang?" de o the Chua noi duoc), q3 (sai so tung hang -> khong noi).
# Bay = hien_tuong_hay_sai[2] (dien tro nguoi va sang bang nhau) duoi dang "den 6 V - 3 W luon la 12 Ohm".
# Cau chot v2 (tu suy tu hang 4,0 V / 0,39 A cua kho; khong can nho bang): den noi tiep 10 Ohm, von ke tren den 4,0 V,
#   ampe ke 0,39 A (ca hai HIEN tren man chot) -> U_R = 0,39.10 = 3,9 V -> nguon 4,0 + 3,9 = 7,9 V (chua hien).
# Bo cuc: bong den ve that + 2 dong ho o tren, bang doc 6 hang o duoi; dap an = thanh so sanh; do thi chi o canh bay.
# Nhieu cau chot v2: 3,9 V (quen den) ; 4,4 V (cong 4,0 + 0,39) ; 14 V (cong 4,0 + 10).
from engine import *

ROWS = [(1.0, 0.17, 5.9), (2.0, 0.26, 7.7), (3.0, 0.33, 9.1), (4.0, 0.39, 10.3), (5.0, 0.45, 11.1), (6.0, 0.50, 12.0)]
K = 0.1706
def i_mod(u): return K * u ** 0.6
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def _kiem_so():
    return [r for r in ROWS if abs(round(i_mod(r[0]) + 1e-9, 2) - r[1]) > 1e-9 or abs(round(r[0] / r[1], 1) - r[2]) > 1e-9]
assert not _kiem_so()
assert ROWS[2][1] > ROWS[5][1] / 2                                       # dap an B: hon mot nua
_SER = [round(u + 10 * i, 2) for u, i, _ in ROWS]
assert abs(ROWS[3][0] + 10 * ROWS[3][1] - 7.9) < 1e-9                    # cau chot v2: hang 4,0 V

NOTE = (60, 64, 84); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100); DRED = (185, 28, 28)
GLASS = (235, 240, 248); FIL = (90, 80, 70); DGREEN = (21, 110, 55); EMPTY = (148, 140, 128); WIRE = (60, 66, 92)

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

def dashed(d, p1, p2, color, w=3, dash=14, gap=10):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for k in range(n):
        a = k * (dash + gap) / L; b = min(1, (k * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

# ---------------- den + dong ho ----------------
LX, LY, LR = 270, 470, 135
def bright(j):           # do sang ~ cong suat U.I so voi 3 W
    if j < 0: return 0.0
    u, i, _ = ROWS[j]; return clamp(u * i / 3.0) ** 0.5

def lamp(d, b):
    if b > 0:
        for r, al in ((LR + 120, 0.10), (LR + 75, 0.16), (LR + 35, 0.24)):
            d.ellipse([LX - r, LY - r, LX + r, LY + r], fill=A((255, 214, 90), al * b))
    d.ellipse([LX - LR, LY - LR, LX + LR, LY + LR], fill=mix(GLASS, (255, 244, 190), b), outline=NAVY, width=5)
    d.rectangle([LX - 62, LY + LR - 20, LX + 62, LY + LR + 70], fill=(170, 170, 180), outline=NAVY, width=4)
    for k in range(3): d.line([(LX - 62, LY + LR + 5 + 22 * k), (LX + 62, LY + LR + 15 + 22 * k)], fill=NAVY, width=3)
    d.line([(LX - 40, LY + LR - 20), (LX - 40, LY + 10)], fill=FIL, width=4)
    d.line([(LX + 40, LY + LR - 20), (LX + 40, LY + 10)], fill=FIL, width=4)
    zz = [(LX - 40 + 80 * k / 8, LY + 10 + (-26 if k % 2 else 0)) for k in range(9)]
    d.line(zz, fill=mix(FIL, (255, 150, 30), b), width=6 if b > 0.3 else 4, joint="curve")
    text(d, (LX, 280), "đèn 6 V – 3 W", 56, INK)

def readout(d, y0, label, reading, flash=0.0):
    card(d, (560, y0, 1030, y0 + 160), fill=BODY, r=20)
    card(d, (578, y0 + 16, 1012, y0 + 96), fill=mix(SCREEN, (255, 237, 160), flash), r=10)
    text(d, (795, y0 + 56), reading, 58, SCR_INK)
    text(d, (795, y0 + 128), label, 56, WHITE)

def circuit(d):
    """Mach kin: nguon (duoi) - den - ampe ke noi tiep (day phai); von ke song song hai dau den (nhanh duoi den)."""
    c = WIRE; yt, yb = LY + LR + 30, 800
    d.line([(LX - 62, yt), (110, yt), (110, yb), (430, yb)], fill=c, width=5, joint="curve")
    d.line([(455, yb), (520, yb), (520, yt), (LX + 62, yt)], fill=c, width=5, joint="curve")
    d.line([(430, yb - 40), (430, yb + 40)], fill=ORANGE, width=7)
    d.line([(455, yb - 22), (455, yb + 22)], fill=ORANGE, width=14)
    text(d, (442, yb + 66), "nguồn", 56, NOTE)
    d.ellipse([520 - 46, 712 - 46, 520 + 46, 712 + 46], fill=WHITE, outline=BLUE, width=6); text(d, (520, 714), "A", 56, BLUE)
    for x in (160, 400): dot(d, x, yt, 8, c)
    d.line([(160, yt), (160, 700), (229, 700)], fill=c, width=4, joint="curve")
    d.line([(400, yt), (400, 700), (331, 700)], fill=c, width=4, joint="curve")
    d.ellipse([280 - 46, 700 - 46, 280 + 46, 700 + 46], fill=WHITE, outline=PURPLE, width=6); text(d, (280, 702), "V", 56, PURPLE)

def meters(d, j, flash=0.0):
    u, i = (ROWS[j][0], ROWS[j][1]) if j >= 0 else (0.0, 0.0)
    circuit(d)
    readout(d, 340, "vôn kế", vn(u) + " V", flash)
    readout(d, 540, "ampe kế", vn(i, 2) + " A", flash)

# ---------------- bang doc 6 hang ----------------
CX = (250, 540, 830)
def vtable(d, y0, n, hl=None):
    card(d, (60, y0, 1020, y0 + 100 + 72 * 6), fill=WHITE, outline=NAVY, w=4)
    for x, c in zip(CX, ("U (V)", "I (A)", "U/I (Ω)")): text(d, (x, y0 + 50), c, 56, INK)
    d.line([(90, y0 + 92), (990, y0 + 92)], fill=LIGHT, width=4)
    for k in range(n):
        yy = y0 + 132 + 72 * k; u, i, q = ROWS[k]
        if hl == k: d.rounded_rectangle([80, yy - 34, 1000, yy + 34], radius=16, fill=(255, 237, 213))
        for x, s, col in zip(CX, (vn(u), vn(i, 2), vn(q)), (INK, BLUE, DGREEN)): text(d, (x, yy), s, 56, col)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    lamp(d, bright(5)); meters(d, 5)
    a = appear(t, M[1] - 0.2, 0.4)
    if a <= 0: return
    y0 = 910 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 650), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 190), "Ở 6,0 V: I = 0,50 A.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "Hạ U còn một nửa: 3,0 V.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 400), "I so với 0,50 A thế nào?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 540, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
TS = [0.6 + 1.3 * k for k in range(6)]       # lan do k: U = ROWS[k][0]; den, dong ho, hang bang doi CUNG luc

def do_state(t):
    """-> (so hang da ghi, hang dang chi (-1 = chua bat), flash 0..1)."""
    n = sum(1 for ts in TS if t >= ts - 1e-9)
    j = n - 1
    flash = 1 - clamp((t - TS[j]) / 0.6) if j >= 0 else 0.0
    return n, j, flash

def s_do(img, d, t, sc):
    n, j, flash = do_state(t)
    lamp(d, bright(j)); meters(d, j, flash)
    vtable(d, 930, n, hl=j if j >= 0 and flash > 0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: hang cuoi da ghi = hang dang chi tren dong ho = do sang den."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        n, j, flash = do_state(t)
        if j != n - 1: bad.append(round(t, 2))
        t += 0.05
    if TS[-1] + 0.6 > sc["T"]: bad.append("hang cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
BX0, BX1 = 300, 900                             # thanh I: 0 -> 0,50 A dai 600 px
def bx(i): return BX0 + i / 0.50 * (BX1 - BX0)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, W / 2, 300, "ĐÁP ÁN · hơn một nửa", NAVY)
    card(d, (40, 380, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    text(d, (BX0, 430), "dòng điện I", 56, MUTED, anchor="lm")
    for r, (j, yy) in enumerate(((5, 560), (2, 760))):
        u, i, _ = ROWS[j]
        kk = ease(clamp((t - 0.2) / 1.0))
        text(d, (80, yy), vn(u) + " V", 58, INK, anchor="lm")
        d.rounded_rectangle([BX0, yy - 40, BX0 + (bx(i) - BX0) * kk, yy + 40], radius=14, fill=BLUE)
        if j == 5: text(d, (bx(i) - 16, yy), vn(i, 2) + " A", 56, WHITE, anchor="rm")
        else: text(d, (bx(i) + 18, yy), vn(i, 2) + " A", 56, BLUE, anchor="lm")
    km = appear(t, 2.5, 0.4)
    if km > 0:
        xm = bx(ROWS[5][1] / 2)
        dashed(d, (xm, 500), (xm, 820), A(ORANGE, km), w=6)
        card(d, (xm - 130, 1000 - 50, xm + 130, 1000 + 50), fill=A((255, 247, 237), km), outline=A(ORANGE, km), r=20, w=4)
        text(d, (xm, 1000), "một nửa", 58, ORANGE, alpha=km)
        d.line([(xm, 830), (xm, 950)], fill=A(ORANGE, km), width=4)
    kr = appear(t, M[1] + 0.1, 0.45)
    if kr > 0:
        y0 = 1100 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 440), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pill(d, W / 2, y0 + 70, "RÚT RA", GREEN, kr)
        text(d, (W / 2, y0 + 200), "Đèn: U/I tăng dần theo U", 60, INK, alpha=kr)
        text(d, (W / 2, y0 + 320), "5,9 Ω → 12,0 Ω", 60, DGREEN, alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc (do thi I-U) ----------------
GX0, GX1, GY0, GY1 = 220, 930, 1450, 1010        # U 0-6 V ; I 0-0,6 A
def gx(u): return GX0 + u / 6 * (GX1 - GX0)
def gy(i): return GY0 - i / 0.6 * (GY0 - GY1)

def axes(d, note=False):
    card(d, (40, 880, 1040, 1580), fill=WHITE, outline=LIGHT, w=3)
    for i in (0.2, 0.4, 0.6):
        d.line([(GX0, gy(i)), (GX1, gy(i))], fill=LIGHT, width=3)
        text(d, (GX0 - 18, gy(i)), vn(i), 56, NOTE, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 36), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 36, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 22, GY1 - 40), "I (A)", 56, INK, anchor="lm")
    text(d, (1020, GY0 - 50), "U (V)", 56, INK, anchor="rm")
    if note: text(d, (1010, 925), "số liệu mô phỏng", 56, NOTE, anchor="rm")
    for u in range(1, 7):
        d.line([(gx(u), GY0), (gx(u), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(u), GY0 + 50), str(u), 56, NOTE)

def s_bay(img, d, t, sc):
    M = sc["M"]
    axes(d)
    pc = [(gx(1 + 5 * k / 60), gy(i_mod(1 + 5 * k / 60))) for k in range(61)]       # chi tu 1 V (mo_hinh)
    d.line(pc, fill=A(BLUE, 0.85), width=6, joint="curve")
    for u, i, _ in ROWS: dot(d, gx(u), gy(i), 15, BLUE, outline=WHITE)
    text(d, (gx(2.2), gy(i_mod(2.2)) - 60), "đèn", 56, BLUE)
    k2 = appear(t, M[1] - 0.1, 0.4); k3 = appear(t, M[2] - 0.5, 0.45)
    if k2 > 0:
        dashed(d, (gx(0), gy(0)), (gx(6 * k2), gy(0.50 * k2)), ORANGE, w=6)
        xl, yl = gx(4.6), gy(0.50 * 4.6 / 6) + 145
        card(d, (xl - 130, yl - 40, xl + 130, yl + 40), fill=A(WHITE, k2), outline=A(ORANGE, k2), r=18, w=4)
        text(d, (xl, yl), "12 Ω", 56, ORANGE, alpha=k2)
    a1 = 1.0 - k3; y = 300
    if a1 > 0:
        card(d, (40, y, 1040, y + 520), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", DRED, a1)
        q = "“Đèn này luôn là 12 Ω”"
        f = F(58); lw = tw(d, q, f); yy = y + 210
        text(d, (W / 2, yy), q, 58, mix(INK, GRAY, k2), alpha=a1)
        if k2 > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * k2, yy + 2)], fill=A(DRED, 0.85 * a1), width=7)
            text(d, (W / 2, y + 340), "Chỉ 6,0 V trên đường 12 Ω", 58, BLUE, alpha=a1 * k2)
            text(d, (W / 2, y + 430), "Các điểm khác ở phía trên", 58, BLUE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 520), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 290), "Vì sao U/I của đèn tăng?", 62, INK, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def _series(d, k):
    """So do v2: den - dien tro 10 Ohm - ampe ke noi tiep; von ke tren DEN chi 4,0 V, ampe ke 0,39 A; nguon '?'."""
    c = A(WIRE, k); y1, y2 = 620, 840
    d.line([(150, y1), (150, y2), (930, y2), (930, y1), (150, y1)], fill=c, width=6)
    d.ellipse([290, y1 - 50, 390, y1 + 50], fill=A(WHITE, k), outline=A(NAVY, k), width=5)
    d.line([(305, y1 - 35), (375, y1 + 35)], fill=A(NAVY, k), width=4); d.line([(305, y1 + 35), (375, y1 - 35)], fill=A(NAVY, k), width=4)
    text(d, (340, y1 + 90), "đèn", 58, NAVY, alpha=k)
    d.rectangle([620, y1 - 28, 800, y1 + 28], fill=A(WHITE, k), outline=A(NAVY, k), width=5)
    text(d, (710, y1 + 80), "10 Ω", 58, NAVY, alpha=k)
    d.line([(250, y1), (250, 470), (294, 470)], fill=c, width=4); d.line([(430, y1), (430, 470), (386, 470)], fill=c, width=4)
    d.ellipse([294, 424, 386, 516], fill=A(WHITE, k), outline=A(PURPLE, k), width=6); text(d, (340, 472), "V", 56, PURPLE, alpha=k)
    text(d, (440, 400), "4,0 V", 58, PURPLE, anchor="lm", alpha=k)
    d.ellipse([254, y2 - 46, 346, y2 + 46], fill=A(WHITE, k), outline=A(BLUE, k), width=6); text(d, (300, y2 + 2), "A", 56, BLUE, alpha=k)
    text(d, (300, y2 + 85), "0,39 A", 58, BLUE, alpha=k)
    d.line([(520, y2 - 44), (520, y2 + 44)], fill=A(ORANGE, k), width=7)
    d.line([(550, y2 - 24), (550, y2 + 24)], fill=A(ORANGE, k), width=14)
    d.rectangle([523, y2 - 4, 547, y2 + 4], fill=A(WHITE, k))
    text(d, (560, y2 + 85), "nguồn ?", 58, DRED, alpha=k)

def s_end(img, d, t, sc):
    """THU NGHI v2: den 4,0 V / 0,39 A noi tiep 10 Ohm -> nguon? (4,0 + 3,9 = 7,9 V, khong hien)."""
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    _series(d, k)
    text(d, (W / 2, 1080), "Đèn này nối tiếp 10 Ω.", 60, INK, alpha=k)
    text(d, (W / 2, 1180), "Nguồn bao nhiêu vôn?", 62, DRED, alpha=k)
    seg_bar(d, 1360, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + ts, "tap") for ts in TS]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l11-dien-tro-ohm-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện trở · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo U và I của bóng đèn", draw=s_hook, tail=0.3, caps=[
   ("Đèn sáng đủ ở 6,0 V.", 3.6),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Tăng U từng 1,0 V, chờ đèn ổn định.", 4.0),
   ("Ghi I, tính U/I mỗi lần.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("So dòng ở 3,0 V với 6,0 V.", 4.0),
   ("Đèn càng sáng, U/I càng lớn.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Hay nhầm.", 3.6),
   ("Kẻ thử đường qua gốc.", 3.6),
   ("Chưa đo dưới 1,0 V.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng lại, tự trả lời.", 7.2)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
