# Clip: tn-l9-ohm-02 - Doi U, doc I cua mot doan day constantan, ve do thi I theo U (KHTN 9, lo 6, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-ohm-02.json:
#   so_lieu_mau (U V, I A, U/I Ohm): 1,5 0,08 18,75 ; 3,0 0,15 20,0 ; 4,5 0,22 20,45 ; 6,0 0,30 20,0. R = 20 Ohm (tham_so).
#   rut_ra: I ti le thuan U ; U/I quanh 20 Ohm ; do thi thang qua goc. bay = hien_tuong_hay_sai[1] (noi gap khuc).
#   KHONG nhan xet vi sao lan 1 lech (Cau 2 ngay sau hop hoi dung dieu nay) ; KHONG dung bay "tang U thi R tang" (Cau 4 muc III).
#   chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet[0] (chi dung cho day constantan, R gan nhu khong doi khi nong).
# Khuon tu clips/l9ohm1.py (da duyet) nhung DOI dan canh: do thi I-U lon lam truc chinh, mach thu gon thanh dai tren,
#   dong ho so dang chip, bang nam ngang. Du doan khac ohm-01 (ohm-01: cung U, doi day ; o day: cung day, U gap doi).
# Du doan (K10): cham 4 diem (U; I) -> duong qua cac diem co dang nao? -> thang qua goc (khong hoi '3 V len 6 V': trung Cau 4).
# Cau chot (ghi o kho ghi_chu): day khac 2,0 V -> 0,05 A ; muon 0,12 A thi U? -> 4,8 V (hai buoc, nguoc chieu Du doan).
#   O chot "I ti le thuan voi U" chi hien SAU thoi gian nghi (nhu ohm-01), khong dung chot_hoi.
# Mach: nguon chinh duoc (+ ban dai trai) -> K -> canh trai len -> ampe ke (+ trai) -> day constantan -> canh phai xuong -> (-);
#   von ke song song voi day (+ o dau phia ampe ke). Ngat K giua cac lan do (an_toan).
#   _kiem_dong_bo(): moi 0,05 s K mo <=> 0 V, 0 A ; K dong <=> dung hang dang do ; cham/o bang chi co sau khi da doc.
import copy
from engine import *

ROWS = [(1.5, 0.08, 18.75), (3.0, 0.15, 20.0), (4.5, 0.22, 20.45), (6.0, 0.30, 20.0)]   # so_lieu_mau
R = 20.0
U_C0, I_C0, I_C, U_C = 2.0, 0.05, 0.12, 4.8   # cau chot: day khac 2,0 V -> 0,05 A (R = 40 Ohm); 0,12 A -> U = 4,8 V
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def vq(x): return vn(x, 2) if abs(x * 10 - round(x * 10)) > 1e-6 else vn(x, 1)        # 18,75 ; 20,0 ; 20,45

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); CON = (180, 83, 9)

# ---------------- dai mach thu gon ----------------
XL, XR, TY, BY = 80, 690, 340, 540
AX, C0, C1, VX, VY = 185, 290, 560, 425, 440
SX, KX0, KX1 = 320, 450, 540
AR = 36

def coil(d, x0, x1, y, a=1.0):
    pts = [(x0, y)]; n = 9
    for k in range(n):
        pts.append((x0 + (k + 0.5) * (x1 - x0) / n, y + (-26 if k % 2 == 0 else 26)))
    pts.append((x1, y))
    d.line(pts, fill=A(CON, a), width=6, joint="curve")

def strip(d, closed, u_src, u_v, i_a):
    card(d, (40, 260, 1040, 600), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    d.line([(XL, BY), (XL, TY), (AX - AR, TY)], fill=WIRE, width=w, joint="curve")
    d.line([(AX + AR, TY), (C0, TY)], fill=WIRE, width=w)
    d.line([(C1, TY), (XR, TY), (XR, BY), (KX1, BY)], fill=WIRE, width=w, joint="curve")
    d.line([(KX0, BY), (SX + 20, BY)], fill=WIRE, width=w)
    d.line([(SX - 20, BY), (XL, BY)], fill=WIRE, width=w)
    coil(d, C0, C1, TY)
    text(d, ((C0 + C1) / 2, 286), "dây constantan", 40, mix(CON, INK, 0.3))
    d.ellipse([AX - AR, TY - AR, AX + AR, TY + AR], fill=WHITE, outline=BLUE, width=6); text(d, (AX, TY + 2), "A", 40, BLUE)
    text(d, (AX - AR - 18, TY - 40), "+", 40, BLUE)
    # von ke song song voi day
    for x in (C0, C1): dot(d, x, TY, 8, WIRE)
    d.line([(C0, TY), (C0, VY), (VX - AR, VY)], fill=PURPLE, width=5, joint="curve")
    d.line([(C1, TY), (C1, VY), (VX + AR, VY)], fill=PURPLE, width=5, joint="curve")
    d.ellipse([VX - AR, VY - AR, VX + AR, VY + AR], fill=WHITE, outline=PURPLE, width=6); text(d, (VX, VY + 2), "V", 40, PURPLE)
    text(d, (VX - AR - 18, VY - 38), "+", 40, PURPLE)
    # nguon chinh duoc: ban dai (+) ben trai, mui ten cheo = chinh duoc
    d.line([(SX - 20, BY - 46), (SX - 20, BY + 46)], fill=NAVY, width=6)
    d.line([(SX + 20, BY - 24), (SX + 20, BY + 24)], fill=NAVY, width=14)
    arrow(d, (SX - 50, BY + 40), (SX + 50, BY - 40), ORANGE, w=4, head=16)
    text(d, (SX - 60, BY - 36), "+", 40, ORANGE)
    if u_src: text(d, (150, 576), f"đặt {vn(u_src)} V", 40, ORANGE)
    # khoa K
    dot(d, KX0, BY, 9, WIRE); dot(d, KX1, BY, 9, WIRE)
    if closed: d.line([(KX0, BY), (KX1, BY)], fill=NAVY, width=7)
    else: d.line([(KX0, BY), (KX1 - 12, BY - 46)], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2 + 4, BY - 60 if not closed else BY - 40), "K", 40, NAVY)
    if closed:
        arrow(d, (XL, 500), (XL, 400), RED, w=7, head=20)
        arrow(d, (XR, 380), (XR, 480), RED, w=7, head=20)
    # chip so chi
    for y, lab, val, col in ((276, "vôn kế", vn(u_v) + " V", PURPLE), (440, "ampe kế", vn(i_a, 2) + " A", BLUE)):
        card(d, (720, y, 1024, y + 148), fill=BODY, r=20)
        text(d, (872, y + 34), lab, 40, WHITE)
        card(d, (746, y + 62, 998, y + 136), fill=SCREEN, r=12)
        text(d, (872, y + 99), val, 50, SCR_INK)

# ---------------- do thi I theo U ----------------
OX, OY, SU, SI = 190, 1210, 125.0, 1700.0
def P(u, i): return (OX + u * SU, OY - i * SI)
def axes(d, a=1.0, y0=630, y1=1300):
    card(d, (40, y0, 1040, y1), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    for i in (0.1, 0.2, 0.3):
        y = OY - i * SI
        d.line([(OX, y), (OX + 6.3 * SU, y)], fill=A((236, 232, 222), a), width=2)
        text(d, (OX - 50, y), vn(i), 40, MUTED, alpha=a)
    for u in (1.5, 3.0, 4.5, 6.0):
        x = OX + u * SU
        d.line([(x, OY - 0.32 * SI), (x, OY)], fill=A((236, 232, 222), a), width=2)
        text(d, (x, OY + 42), vn(u), 40, MUTED, alpha=a)
    arrow(d, (OX, OY), (OX + 6.6 * SU, OY), A(NAVY, a), w=5, head=18)
    arrow(d, (OX, OY), (OX, OY - 0.34 * SI), A(NAVY, a), w=5, head=18)
    text(d, (OX - 50, OY + 40), "0", 40, MUTED, alpha=a)
    text(d, (OX + 100, OY - 0.34 * SI + 14), "I (A)", 40, NAVY, alpha=a)
    text(d, (OX + 6.6 * SU - 20, OY - 46), "U (V)", 40, NAVY, alpha=a)

def pt(d, u, i, col=BLUE, a=1.0, r=14):
    x, y = P(u, i); d.ellipse([x - r, y - r, x + r, y + r], fill=A(col, a), outline=A(WHITE, a), width=3)

# ---------------- bang nam ngang ----------------
TXS = (430, 580, 730, 880)
def table(d, n, y=1330, ui=0.0, hl=None):
    hh = 210 + (90 if ui > 0 else 0)
    card(d, (40, y, 1040, y + hh), fill=WHITE, outline=LIGHT, w=3)
    labs = (("U (V)", NAVY), ("I (A)", BLUE)) + ((("U/I (Ω)", DGREEN),) if ui > 0 else ())
    for r, (lab, col) in enumerate(labs):
        yy = y + 60 + r * 90
        text(d, (80, yy), lab, 42, col, anchor="lm", alpha=ui if r == 2 else 1.0)
        if r < 2: d.line([(70, yy + 45), (1010, yy + 45)], fill=LIGHT, width=3)
    for k, (u, i, q) in enumerate(ROWS):
        x = TXS[k]
        if hl == k: d.rounded_rectangle([x - 68, y + 18, x + 68, y + 192], radius=18, fill=(255, 237, 213))
        if k < n:
            text(d, (x, y + 60), vn(u), 44, NAVY); text(d, (x, y + 150), vn(i, 2), 44, BLUE)
        else:
            text(d, (x, y + 60), "·", 44, GRAY); text(d, (x, y + 150), "·", 44, GRAY)
        if ui > 0: text(d, (x, y + 240), vq(q), 44, DGREEN, alpha=appear(ui, 0.2 + 0.15 * k, 0.3))

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    strip(d, False, None, 0.0, 0.0)
    axes(d); table(d, 0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 630 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 935), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ax, ay = 420, y0 + 380   # do thi phac, chua co gi
    arrow(d, (ax, ay), (ax + 280, ay), A(NAVY, a), w=5, head=18); arrow(d, (ax, ay), (ax, ay - 200), A(NAVY, a), w=5, head=18)
    text(d, (ax + 310, ay - 30), "U", 42, NAVY, alpha=a); text(d, (ax - 36, ay - 190), "I", 42, NAVY, alpha=a)
    text(d, (ax + 140, ay - 100), "?", 64, MUTED, alpha=a)
    ctext(d, y0 + 540, "Chấm 4 điểm (U; I) lên đồ thị.\nĐường qua các điểm có dạng nào?", 50, INK, maxw=940, alpha=a)
    text(d, (W / 2, y0 + 720), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 810, 940, y0 + 822], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 810, 140 + 800 * (1 - p), y0 + 822], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T0, STEP, D_CLOSE, D_OPEN, T_PT = 0.5, 2.4, 0.5, 1.9, 0.35
def do_state(t):
    """-> (K dong?, U nguon dang dat, so diem da ghi, chi so lan dang do)."""
    k = int(clamp((t - T0) / STEP, 0, 3.999)) if t >= T0 else -1
    if k < 0: return False, 0.0, 0, -1
    ts = T0 + k * STEP
    closed = ts + D_CLOSE <= t < ts + D_OPEN
    n = sum(1 for j in range(4) if t >= T0 + j * STEP + D_CLOSE + T_PT)
    return closed, ROWS[k][0], n, k

def s_do(img, d, t, sc):
    closed, us, n, k = do_state(t)
    u, i = (ROWS[k][0], ROWS[k][1]) if closed else (0.0, 0.0)
    strip(d, closed, us, u, i)
    axes(d)
    for j in range(n): pt(d, ROWS[j][0], ROWS[j][1], a=appear(t, T0 + j * STEP + D_CLOSE + T_PT, 0.25))
    table(d, n, hl=k if k >= 0 else None)

def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        closed, us, n, k = do_state(t)
        if closed and n > k + 1: bad.append((round(t, 2), "cham truoc khi doc"))
        if not closed and k >= 0 and n not in (k, k + 1): bad.append((round(t, 2), "so cham lech lan do"))
        if closed and us != ROWS[k][0]: bad.append((round(t, 2), "U nguon lech hang"))
        t += 0.05
    if do_state(sc["T"] - 0.01)[2] != 4: bad.append("cuoi canh thieu diem")
    if T0 + 3 * STEP + D_OPEN > sc["T"]: bad.append("lan 4 chua mo K")
    return bad

def _kiem_so():
    bad = [r for r in ROWS if abs(r[0] / r[1] - r[2]) > 0.01]
    if abs(U_C0 / I_C0 * I_C - U_C) > 1e-9 or U_C > 6: bad.append("chot")
    return bad

# ---------------- canh 3: Dap an (duong thang qua goc) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · thẳng, qua gốc toạ độ"
    pw = tw(d, lab, F(44)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 348), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 310), lab, 44, WHITE, alpha=ka)
    axes(d)
    g = ease((t - 0.6) / 0.9)
    if g > 0:   # ke thuoc: duong I = U/R tu goc, ve dan
        u1 = 6.3 * g; d.line([P(0, 0), P(u1, u1 / R)], fill=DGREEN, width=6)
    for u, i, q in ROWS: pt(d, u, i)
    k0 = appear(t, 1.4, 0.4)
    if k0 > 0:
        d.ellipse([OX - 22, OY - 22, OX + 22, OY + 22], outline=A(ORANGE, k0), width=5)
        text(d, (OX + 150, OY - 50), "gốc", 42, ORANGE, alpha=k0)
    k3 = appear(t, 1.9, 0.4)
    if k3 > 0:
        card(d, (40, 1330, 1040, 1560), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1395), "Các điểm sát một đường thẳng", 46, DGREEN, alpha=k3)
        text(d, (W / 2, 1490), "đi qua gốc", 46, DGREEN, alpha=k3)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 270, 1040, 450), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=5)
    text(d, (W / 2, 360), "I tỉ lệ thuận với U", 54, DGREEN, alpha=k0)
    k1 = appear(t, M[1] - 0.1, 0.4)
    table(d, 4, y=500, ui=clamp((t - 0.8) / 1.6))
    if k1 > 0:
        text(d, (W / 2, 880), "U/I gần như không đổi, quanh 20 Ω", 44, DGREEN, alpha=k1)
    k2 = appear(t, M[1] + 1.2, 0.4)
    if k2 > 0:
        card(d, (40, 960, 1040, 1250), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1050), "Định luật Ohm", 46, DGREEN, alpha=k2)
        text(d, (W / 2, 1160), "I = U : R", 60, DGREEN, alpha=k2)

# ---------------- canh 5: Bay (noi gap khuc) roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if k2 < 0.5: axes(d)   # hop 'Chua noi duoc' (day ~1260) khong che nhan truc y~1252
    for u, i, q in ROWS: pt(d, u, i)
    if a1 > 0:
        card(d, (40, 260, 1040, 600), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, 284, W / 2 + pw / 2, 348), fill=A(DRED, a1), r=32)
        text(d, (W / 2, 316), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[0] - 1.6) / 0.4)
        for j, q in enumerate(("“Nối từng điểm thành", "đường gấp khúc”")):
            yy = 420 + j * 70; lw = tw(d, q, F(50))
            text(d, (W / 2, yy), q, 50, mix(INK, MUTED, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2 + 330, 490), "✗", 56, DRED, alpha=a1 * ks)
        # hinh sai hien cung cau bay: duong gap khuc noi tung diem (khong qua goc)
        pts = [P(u, i) for u, i, q in ROWS]
        d.line(pts, fill=A(DRED, a1 * (1 - 0.6 * ks)), width=5)
        kk = a1 * appear(t, M[0] + 2.2, 0.4)
        if kk > 0:
            p1 = P(6.3, 6.3 / R)
            d.line([P(0, 0), p1], fill=A(DGREEN, kk), width=6)
            card(d, (40, 1330, 1040, 1560), fill=A((236, 253, 243), kk), outline=A(GREEN, kk), w=5)
            text(d, (W / 2, 1395), "✓ Một đường thẳng qua gốc,", 46, DGREEN, alpha=kk)
            text(d, (W / 2, 1490), "sát các điểm", 46, DGREEN, alpha=kk)
    if k2 > 0:
        d.line([P(0, 0), P(6.3, 6.3 / R)], fill=A(DGREEN, 1 - k2), width=6)
        y0 = 620 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 95), "Chưa nói được", 52, NAVY, alpha=k2)
        for j, (l1, l2) in enumerate((("• Số liệu minh hoạ", ""),
                                      ("• Mới thử dây constantan,", "R gần như không đổi"))):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y0 + 270 + j * 230), l1, 50, INK, anchor="lm", alpha=kk)
            if l2: text(d, (132, y0 + 345 + j * 230), l2, 50, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
T_CHOT = 4.0
def s_end(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 620, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(38)) + 52
        card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 682), "THỬ NGHĨ", 38, WHITE, alpha=k1)
        ctext(d, 830, "Dây khác: 2,0 V thì 0,05 A.\nMuốn 0,12 A, đặt U bao nhiêu?", 46, INK, maxw=920,
              alpha=appear(t, M[0] + 0.4, 0.5))
        ka = appear(t, M[0] + 0.6, 0.5) * k1
        coil(d, 330, 750, 1060, a=ka)
        text(d, (540, 1140), "dây khác", 42, MUTED, alpha=ka)
        text(d, (870, 1060), "? V", 46, PURPLE, alpha=ka)
        kh = appear(t, M[0] + 2.9, 0.5)
        card(d, (110, 1260, 970, 1500), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1320, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1415, "Dây khác, R khác", 44, ORANGE, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 410, "Cùng một dây: I tỉ lệ thuận với U", 50, GREEN, maxw=860, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding")]
    cs += [(do["t0"] + T0 + j * STEP + D_CLOSE, "tap") for j in range(4)]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.2, "buzz"),
           (b["t0"] + b["M"][0] + 2.2, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l9-ohm-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Định luật Ohm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đổi U, đọc I", draw=s_hook, tail=0.8, caps=[
   ("Một đoạn dây constantan.", 2.5),
   ("Bốn lần đo, bốn điểm.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Mỗi lần: đặt U, đóng K, đọc I.", 3.8),
   ("Ngắt K giữa các lần đo.", 3.0),
   ("Chấm từng điểm lên đồ thị.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Kẻ thẳng sát các điểm.", 4.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Tính U chia I mỗi lần.", 2.9),
   ("Thương này là điện trở dây.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Có đúng không?", 4.2),
   ("Còn chưa nói được.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Tự trả lời trước khi xem.", 6.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
