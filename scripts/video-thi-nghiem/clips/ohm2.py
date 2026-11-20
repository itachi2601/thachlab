# Clip: tn-l11-dien-tro-ohm-02 - Do U va I cua den soi dot 6 V - 3 W: ha U con mot nua thi I? (ban 1, 16/11/2026)
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
# Cau chot (ca tu suy, ghi trong ghi_chu kho): den noi tiep dien tro 10 Ohm, nguon 6,3 V. Thu hang: 3,0 + 10.0,33 = 6,3
#   -> von ke tren dien tro chi 3,3 V (hon 3,0 V cua den), I = 0,33 A. Hang khac: 2 + 2,6 = 4,6 ; 4 + 3,9 = 7,9 -> duy nhat.
#   So 6,3 V va 3,3 V chua tung hien tren man.
# Bo cuc (khac ohm1 = so do mach + do thi, khac ohm3 = dung cu + bang doc): bong den ve that + 2 dong ho xep doc o tren,
#   BANG NGANG 6 cot o duoi; dap an = thanh so sanh; do thi chi o canh bay.
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
assert _SER.count(6.3) == 1 and abs(6.3 - ROWS[2][0] - 10 * ROWS[2][1]) < 1e-9   # cau chot: duy nhat hang 3,0 V

NOTE = (60, 64, 84); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100); DRED = (185, 28, 28)
GLASS = (235, 240, 248); FIL = (90, 80, 70)

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
    text(d, (LX, 280), "đèn 6 V – 3 W", 40, INK)

def readout(d, y0, label, reading, flash=0.0):
    card(d, (560, y0, 1030, y0 + 150), fill=BODY, r=20)
    card(d, (578, y0 + 16, 1012, y0 + 90), fill=mix(SCREEN, (255, 237, 160), flash), r=10)
    text(d, (795, y0 + 53), reading, 50, SCR_INK)
    text(d, (795, y0 + 120), label, 38, WHITE)

def circuit(d):
    """Mach kin: nguon (duoi) - den - ampe ke noi tiep (day phai); von ke song song hai dau den (nhanh duoi den)."""
    c = (60, 66, 92); yt, yb = LY + LR + 30, 800
    d.line([(LX - 62, yt), (110, yt), (110, yb), (430, yb)], fill=c, width=5, joint="curve")
    d.line([(455, yb), (520, yb), (520, yt), (LX + 62, yt)], fill=c, width=5, joint="curve")
    d.line([(430, yb - 40), (430, yb + 40)], fill=ORANGE, width=7)                  # (+) vach dai
    d.line([(455, yb - 22), (455, yb + 22)], fill=ORANGE, width=14)                 # (-) vach ngan
    text(d, (380, yb + 64), "nguồn", 40, NOTE)
    d.ellipse([520 - 40, 712 - 40, 520 + 40, 712 + 40], fill=WHITE, outline=BLUE, width=6); text(d, (520, 714), "A", 40, BLUE)
    for x in (160, 400): dot(d, x, yt, 8, c)
    d.line([(160, yt), (160, 720), (235, 720)], fill=c, width=4, joint="curve")
    d.line([(400, yt), (400, 720), (325, 720)], fill=c, width=4, joint="curve")
    d.ellipse([280 - 40, 720 - 40, 280 + 40, 720 + 40], fill=WHITE, outline=PURPLE, width=6); text(d, (280, 722), "V", 40, PURPLE)

def meters(d, j, flash=0.0):
    u, i = (ROWS[j][0], ROWS[j][1]) if j >= 0 else (0.0, 0.0)
    circuit(d)
    readout(d, 350, "vôn kế V", vn(u) + " V", flash)
    readout(d, 540, "ampe kế A", vn(i, 2) + " A", flash)

# ---------------- bang ngang ----------------
XS = [290 + 136 * k for k in range(6)]
def htable(d, y0, n, hl=(), a=1.0, note=True):
    card(d, (40, y0, 1040, y0 + 330), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    for k in hl:
        d.rounded_rectangle([XS[k] - 64, y0 + 14, XS[k] + 64, y0 + 316], radius=18, fill=A((255, 237, 213), a))
    labs = ("U (V)", "I (A)", "U/I (Ω)")
    for r, lab in enumerate(labs):
        yy = y0 + 70 + 100 * r
        text(d, (62, yy), lab, 40, INK, anchor="lm", alpha=a)
        for k in range(6):
            if k < n:
                u, i, q = ROWS[k]
                s = vn(u) if r == 0 else (vn(i, 2) if r == 1 else vn(q))
                text(d, (XS[k], yy), s, 40, (INK, BLUE, GREEN)[r], alpha=a)
            else:
                text(d, (XS[k], yy), "·", 40, GRAY, alpha=a)
    d.line([(60, y0 + 220), (1020, y0 + 220)], fill=A(LIGHT, a), width=3)
    if note: text(d, (1030, y0 + 360), "số liệu mô phỏng", 38, NOTE, anchor="rm", alpha=a)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    lamp(d, bright(5)); meters(d, 5)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Ở 6,0 V: I = 0,50 A.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "Hạ U còn một nửa: 3,0 V.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 350), "I so với 0,50 A thế nào?", 52, INK, alpha=a)
    text(d, (W / 2, y0 + 450), "Chọn đáp án ở khung câu hỏi", 40, NOTE, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 530, 940, y0 + 544], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 530, 140 + 800 * (1 - p), y0 + 544], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
TS = [0.6 + 1.15 * k for k in range(6)]       # lan do k: U = ROWS[k][0]; den, dong ho, cot bang doi CUNG luc

def do_state(t):
    """-> (so cot da ghi, hang dang chi (-1 = chua bat), flash 0..1)."""
    n = sum(1 for ts in TS if t >= ts - 1e-9)
    j = n - 1
    flash = 1 - clamp((t - TS[j]) / 0.6) if j >= 0 else 0.0
    return n, j, flash

def s_do(img, d, t, sc):
    n, j, flash = do_state(t)
    lamp(d, bright(j)); meters(d, j, flash)
    htable(d, 900, n, hl=(j,) if j >= 0 and flash > 0 else ())

def _kiem_dong_bo():
    """Moi 0,05 s: cot cuoi da ghi = hang dang chi tren dong ho = do sang den."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        n, j, flash = do_state(t)
        if j != n - 1: bad.append(round(t, 2))
        t += 0.05
    if TS[-1] + 0.6 > sc["T"]: bad.append("cot cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
BX0, BX1 = 330, 930                             # thanh I: 0 -> 0,50 A dai 600 px
def bx(i): return BX0 + i / 0.50 * (BX1 - BX0)

def dashed(d, p1, p2, color, w=3, dash=14, gap=10):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for k in range(n):
        a = k * (dash + gap) / L; b = min(1, (k * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.4)
    lab = "ĐÁP ÁN · Hơn một nửa"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 358), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 324), lab, 42, WHITE, alpha=ka)
    htable(d, 390, 6, hl=(2, 5), note=False)
    kb = appear(t, 0.6, 0.4)
    card(d, (40, 760, 1040, 1140), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
    for r, (j, yy) in enumerate(((5, 860), (2, 1040))):
        u, i, _ = ROWS[j]
        kk = appear(t, 0.7 + 0.5 * r, 0.6)
        text(d, (80, yy), vn(u) + " V", 42, INK, anchor="lm", alpha=kb)
        d.rounded_rectangle([BX0, yy - 30, BX0 + (bx(i) - BX0) * kk, yy + 30], radius=12, fill=A(BLUE, kb))
        ka2 = kb * clamp((kk - 0.8) / 0.2)
        if j == 5: text(d, (bx(i) - 14, yy), vn(i, 2) + " A", 40, WHITE, anchor="rm", alpha=ka2)
        else: text(d, (bx(i) + 16, yy), vn(i, 2) + " A", 40, BLUE, anchor="lm", alpha=ka2)
    km = appear(t, 1.9, 0.4)
    if km > 0:
        xm = bx(ROWS[5][1] / 2)
        dashed(d, (xm, 800), (xm, 1072), A(ORANGE, km), w=5)
        card(d, (xm - 95, 1080, xm + 95, 1132), fill=A((255, 247, 237), km), outline=A(ORANGE, km), r=16, w=3)
        text(d, (xm, 1106), "một nửa", 40, ORANGE, alpha=km)
    kr = appear(t, M[1] + 0.1, 0.45)
    if kr > 0:
        y0 = 1180 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pw = tw(d, "RÚT RA", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(GREEN, kr), r=32)
        text(d, (W / 2, y0 + 60), "RÚT RA", 40, WHITE, alpha=kr)
        text(d, (W / 2, y0 + 190), "Đèn: U/I tăng dần theo U", 48, INK, alpha=kr)
        text(d, (W / 2, y0 + 290), "I không tỉ lệ thuận với U", 46, (21, 110, 55), alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc (do thi I-U) ----------------
GX0, GX1, GY0, GY1 = 200, 950, 1460, 960        # U 0-6 V ; I 0-0,6 A
def gx(u): return GX0 + u / 6 * (GX1 - GX0)
def gy(i): return GY0 - i / 0.6 * (GY0 - GY1)

def axes(d):
    card(d, (40, 860, 1040, 1580), fill=WHITE, outline=LIGHT, w=3)
    for i in (0.2, 0.4, 0.6):
        d.line([(GX0, gy(i)), (GX1, gy(i))], fill=LIGHT, width=3)
        text(d, (GX0 - 18, gy(i)), vn(i), 40, NOTE, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 36), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 36, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 22, GY1 - 40), "I (A)", 40, INK, anchor="lm")
    text(d, (1020, GY0 - 44), "U (V)", 40, INK, anchor="rm")
    text(d, (GX0 - 18, GY0 + 6), "0", 40, NOTE, anchor="rm")
    text(d, (1010, 900), "số liệu mô phỏng", 38, NOTE, anchor="rm")
    for u in range(1, 7):
        d.line([(gx(u), GY0), (gx(u), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(u), GY0 + 44), str(u), 40, NOTE)

def s_bay(img, d, t, sc):
    M = sc["M"]
    axes(d)
    pc = [(gx(1 + 5 * k / 60), gy(i_mod(1 + 5 * k / 60))) for k in range(61)]       # chi tu 1 V (mo_hinh)
    d.line(pc, fill=A(BLUE, 0.85), width=6, joint="curve")
    for u, i, _ in ROWS: dot(d, gx(u), gy(i), 15, BLUE, outline=WHITE)
    text(d, (gx(2.6), gy(i_mod(2.6)) - 50), "đèn", 42, BLUE)
    kl = appear(t, 0.8, 0.8)
    if kl > 0.02:
        dashed(d, (gx(0), gy(0)), (gx(6 * kl), gy(0.50 * kl)), ORANGE, w=5)
        kt = appear(t, 1.5, 0.3); xl, yl = gx(4.3), gy(0.50 * 4.3 / 6) + 95
        card(d, (xl - 110, yl - 32, xl + 110, yl + 32), fill=A(WHITE, kt), outline=A(ORANGE, kt), r=16, w=3)
        text(d, (xl, yl), "luôn 12 Ω", 42, ORANGE, alpha=kt)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3); y = 320
    if a1 > 0:
        card(d, (40, y, 1040, y + 480), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Đèn 6 V – 3 W luôn là 12 Ω”"
        ks = clamp((t - 2.0) / 0.4); f = F(46); lw = tw(d, q, f); yy = y + 190
        text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 320), "Điểm đo nằm phía trên đường 12 Ω", 44, BLUE, alpha=a1 * appear(t, 2.2, 0.4))
    if k3 > 0:
        card(d, (40, y, 1040, y + 480), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        for j, s in enumerate(("• Vì sao U/I của đèn tăng?", "• Dưới 1,0 V thì sao?")):
            kk = k3 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (100, y + 230 + 120 * j), s, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _series(d, k):
    """So do nho: nguon 6,3 V - den - dien tro 10 Ohm noi tiep (khong ghi so chi nao)."""
    c = A((60, 66, 92), k); y1, y2 = 1010, 1130
    d.line([(250, y1), (250, y2), (830, y2), (830, y1), (250, y1)], fill=c, width=5)
    d.ellipse([400, y1 - 40, 480, y1 + 40], fill=A(WHITE, k), outline=A(NAVY, k), width=5)
    d.line([(412, y1 - 28), (468, y1 + 28)], fill=A(NAVY, k), width=4); d.line([(412, y1 + 28), (468, y1 - 28)], fill=A(NAVY, k), width=4)
    text(d, (440, y1 - 70), "đèn", 40, NAVY, alpha=k)
    d.rectangle([600, y1 - 22, 740, y1 + 22], fill=A(WHITE, k), outline=A(NAVY, k), width=5)
    text(d, (670, y1 - 62), "10 Ω", 40, NAVY, alpha=k)
    d.line([(520, y2 - 40), (520, y2 + 40)], fill=A(ORANGE, k), width=7)
    d.line([(548, y2 - 22), (548, y2 + 22)], fill=A(ORANGE, k), width=14)
    d.rectangle([522, y2 - 4, 546, y2 + 4], fill=A(WHITE, k))
    text(d, (534, y2 + 80), "6,3 V", 42, ORANGE, alpha=k)

def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: den noi tiep 10 Ohm, nguon 6,3 V; goi y tre 2,9 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 270, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 395, "Đèn: đường I–U cong", 50, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 560, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 590, W / 2 + pw / 2, 654), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 622), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 780, "Đèn nối tiếp 10 Ω, nguồn 6,3 V.\nVôn kế trên điện trở chỉ mấy vôn?\nHơn hay kém đèn?",
          44, INK, maxw=920, alpha=appear(t, M[0] + 0.4, 0.5))
    _series(d, appear(t, M[0] + 0.6, 0.5))
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1290, 970, 1540), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1345, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1450, "Cùng một dòng qua cả hai", 46, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + ts, "tap") for ts in TS]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l11-dien-tro-ohm-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện trở · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo U và I của bóng đèn", draw=s_hook, tail=0.3, caps=[
   ("Đèn đang sáng đủ ở 6,0 V.", 3.6),
   ("Nghĩ trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Tăng U từng 1,0 V, chờ đèn ổn định.", 4.0),
   ("Ghi I, tính U/I mỗi lần.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So hai cột 3,0 V và 6,0 V.", 3.4),
   ("Mỗi lần đo, U/I một khác.", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Kẻ thử đường 12 Ω không đổi.", 4.0),
   ("Hai câu còn bỏ ngỏ.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 7.8)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
