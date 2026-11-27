# Clip: tn-l9-doanmach-02 - Dong dien re nhanh trong doan mach song song R1 = 10 Ohm // R2 = 15 Ohm, nguon 6 V (KHTN 9, lo 6)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom A): chu than canh >= 56 (ra >= 49 px), dong ho ghi bang ky hieu
#   V / A / A1 / A2 thay nhan dai, khong nut A-D (K10), thanh dem 90 px, khoi chu cach >= 2,5 s, Tien hanh co khung
#   sang lan luot qua 4 dong ho (khong dung hinh), Bay = hai o canh nhau (cong R nhu noi tiep ✗ / R_td song song ✓),
#   bo o "Goi y" o man chot.
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-doanmach-02.json (_kiem_so()):
#   so_lieu_mau (du hai nhanh): U 6,0 V ; I1 0,60 A ; I2 0,40 A ; I 1,00 A. R1 10, R2 15 (cac_buoc.lam[0]).
#   rut_ra: U = U1 = U2 ; I = I1 + I2 ; R_td = 6 Ohm. bay = hien_tuong_hay_sai[2] (cong R1 + R2).
#   chua noi duoc = mo_hinh.gia_thiet[0] (bo qua dien tro nguon, ampe ke).
#   KHONG thao nhanh (Cau 6 cua bai hoi bong song song dut; clip doanmach3 lo phan thao bong).
#   Khac Cau 2 cua bai (6 // 12 Ohm, 12 V -> 3 A): clip khong dung cac so nay.
# Du doan (K10): A1 chi 0,60 A, A2 chi 0,40 A -> ampe ke mach chinh? -> 1,00 A.
# THU NGHI = cau_chot khung web (kho ghi_chu): thay R2 bang 30 Ohm (R1 10, nguon 6 V) -> ampe ke mach chinh? -> 0,80 A
#   (I1 = 0,60 ; I2 = 0,20). Man chot KHONG in 0,20 / 0,80.
import copy, json, os
from engine import *

U, R1, R2 = 6.0, 10.0, 15.0
I1, I2, I = 0.60, 0.40, 1.00
R2_C, I_C = 30.0, 0.80
RTD, R_SAI, I_SAI = 6.0, 25.0, 0.24      # bay: 6 : 25 = 0,24 A
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")


def _kiem_so():
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-doanmach-02.json")))
    assert k["so_lieu_mau"]["hang"][0][1:] == [U, I1, I2, I], k["so_lieu_mau"]["hang"]
    assert "R1 = 10 Ω" in k["cac_buoc"]["lam"][0] and "R2 = 15 Ω" in k["cac_buoc"]["lam"][0]
    assert abs(U / R1 - I1) < 0.005 and abs(U / R2 - I2) < 0.005 and abs(I1 + I2 - I) < 1e-9
    assert abs(R1 * R2 / (R1 + R2) - RTD) < 1e-9 and abs(U / RTD - I) < 1e-9
    assert R1 + R2 == R_SAI and abs(U / R_SAI - I_SAI) < 1e-9
    assert abs(U / R1 + U / R2_C - I_C) < 1e-9
    g = k["so_lieu_mau"]["ghi_chu"]; assert "30 Ω" in g and "0,80 A" in g
_kiem_so()

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); RCOL = (180, 83, 9); DPURP = (76, 29, 149)
C1, C2 = TEAL, ORANGE
FS, FL = 56, 60

# ---------------- so do mach ----------------
XL, XR, NA, NB = 90, 990, 230, 850
YM, Y1, Y2, YB, YV = 520, 420, 620, 890, 765
A1X, RX0, RX1 = 360, 500, 690
AMX, KX0, KX1, SX = 420, 190, 280, 650
AR, VR = 46, 44


def resistor(d, x0, x1, y, name, val, col, a=1.0, vy=None):
    card(d, (x0, y - 36, x1, y + 36), fill=A(mix(WHITE, col, 0.18), a), outline=A(col, a), r=10, w=5)
    if name: text(d, ((x0 + x1) / 2, y + 2), name, FS, mix(col, INK, 0.35), alpha=a)
    if val: text(d, ((x0 + x1) / 2, vy if vy else y - 78), val, FS, mix(col, INK, 0.3), alpha=a)


def meter(d, x, y, ch, col, a=1.0, r=AR):
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(WHITE, a), outline=A(col, a), width=6)
    text(d, (x, y + 2), ch, FS, col, alpha=a)


def circuit(d, closed):
    card(d, (40, 262, 1040, 1005), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    d.line([(SX - 20, YB), (AMX + AR, YB)], fill=WIRE, width=w)
    d.line([(AMX - AR, YB), (KX1, YB)], fill=WIRE, width=w)
    d.line([(KX0, YB), (XL, YB), (XL, YM), (NA, YM)], fill=WIRE, width=w, joint="curve")
    d.line([(NB, YM), (XR, YM), (XR, YB), (SX + 20, YB)], fill=WIRE, width=w, joint="curve")
    for y in (Y1, Y2):
        d.line([(NA, YM), (NA, y), (A1X - AR, y)], fill=WIRE, width=w, joint="curve")
        d.line([(A1X + AR, y), (RX0, y)], fill=WIRE, width=w)
        d.line([(RX1, y), (NB, y), (NB, YM)], fill=WIRE, width=w, joint="curve")
    resistor(d, RX0, RX1, Y1, "R1", "10 Ω", C1, vy=Y1 - 78)
    resistor(d, RX0, RX1, Y2, "R2", "15 Ω", C2, vy=Y2 - 78)
    meter(d, A1X, Y1, "A", BLUE); text(d, (A1X, Y1 - 78), "A1", FS, C1)
    meter(d, A1X, Y2, "A", BLUE); text(d, (A1X, Y2 - 78), "A2", FS, C2)
    dot(d, NA, YM, 10, WIRE); text(d, (NA + 40, YM), "A", FS, INK)
    dot(d, NB, YM, 10, WIRE); text(d, (NB - 40, YM), "B", FS, INK)
    d.line([(NA, Y2), (NA, YV), (540 - VR, YV)], fill=PURPLE, width=5, joint="curve")
    d.line([(NB, Y2), (NB, YV), (540 + VR, YV)], fill=PURPLE, width=5, joint="curve")
    dot(d, NA, Y2, 8, WIRE); dot(d, NB, Y2, 8, WIRE)
    meter(d, 540, YV, "V", PURPLE, r=VR)
    meter(d, AMX, YB, "A", BLUE); text(d, (AMX + 10, YB + 72), "mạch chính", FS, BLUE)
    dot(d, KX0, YB, 9, WIRE); dot(d, KX1, YB, 9, WIRE)
    if closed: d.line([(KX0, YB), (KX1, YB)], fill=NAVY, width=7)
    else: d.line([(KX0, YB), (KX1 - 12, YB - 50)], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, YB - 80), "K", FS, NAVY)
    d.line([(SX - 20, YB - 50), (SX - 20, YB + 50)], fill=NAVY, width=6)
    d.line([(SX + 20, YB - 26), (SX + 20, YB + 26)], fill=NAVY, width=14)
    text(d, (SX - 58, YB - 46), "+", FS, ORANGE)
    text(d, (850, YB + 72), "nguồn", FS, INK)
    if closed:
        arrow(d, (XL, 830), (XL, 620), RED, w=7, head=20)
        arrow(d, (XR, 590), (XR, 800), RED, w=7, head=20)
        arrow(d, (RX1 + 30, Y1), (RX1 + 120, Y1), RED, w=7, head=20)
        arrow(d, (RX1 + 30, Y2), (RX1 + 120, Y2), RED, w=7, head=20)


def readings(closed):
    return (U, I, I1, I2) if closed else (0.0, 0.0, 0.0, 0.0)


PANEL = (("V", PURPLE, PURPLE, " V", 1), ("A", BLUE, BLUE, " A", 2), ("A1", BLUE, C1, " A", 2), ("A2", BLUE, C2, " A", 2))
def panel(d, closed, hl=None, y=1030):
    vals = readings(closed)
    for j, ((ch, col, lcol, unit, nd), v) in enumerate(zip(PANEL, vals)):
        x = 40 + 510 * (j % 2); yy = y + 190 * (j // 2)
        card(d, (x, yy, x + 490, yy + 170), fill=BODY, r=22, outline=YELLOW if hl == j else None, w=8)
        d.ellipse([x + 30, yy + 35, x + 130, yy + 135], fill=WHITE, outline=lcol, width=6)
        text(d, (x + 80, yy + 87), ch, FS if len(ch) == 1 else 50 + 6, lcol)
        card(d, (x + 160, yy + 40, x + 460, yy + 130), fill=SCREEN, r=12)
        text(d, (x + 310, yy + 87), vn(v, nd) + unit, 60, SCR_INK)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a < 1: panel(d, False)
    if a <= 0: return
    y0 = 1020 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FS)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 102), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", FS, WHITE, alpha=a)
    text(d, (W / 2, y0 + 185), "Đóng K: A1 chỉ 0,60 A,", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "A2 chỉ 0,40 A.", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 355), "Ampe kế mạch chính chỉ?", FL, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 470, 970, y0 + 560], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 470, 110 + max(90, 860 * (1 - p)), y0 + 560], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh ----------------
T_CLOSE, T_HL, HL_STEP = 0.9, 1.6, 1.7
def do_closed(t): return t >= T_CLOSE
def do_hl(t):
    if t < T_HL: return None
    k = int((t - T_HL) / HL_STEP); return k if k < 4 else None


def s_do(img, d, t, sc):
    c = do_closed(t)
    circuit(d, c); panel(d, c, hl=do_hl(t))


def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    if sc["T"] < T_HL + 4 * HL_STEP: bad.append(("canh ngan hon 4 lan soi", round(sc["T"], 2)))
    while t < sc["T"]:
        c = do_closed(t); r = readings(c)
        if not c and any(r): bad.append((round(t, 2), "K mo ma co so"))
        if c and r != (U, I, I1, I2): bad.append((round(t, 2), "K dong sai so"))
        if do_hl(t) is not None and not c: bad.append((round(t, 2), "soi dong ho khi K mo"))
        t += 0.05
    return bad


# ---------------- canh 3: Dap an (thanh cong don) ----------------
def pill(d, s, y, a, color=NAVY, size=FS):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, y - 42, W / 2 + pw / 2, y + 42), fill=A(color, a), r=40)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: 1,00 A", 310, appear(t, 0.15, 0.4))
    kb = appear(t, 0.4, 0.4)
    card(d, (40, 390, 1040, 1250), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
    X0, L = 120, 820
    rows = (("A1", I1, C1, 0.7, 0), ("A2", I2, C2, 1.3, L * I1), ("mạch chính", I, BLUE, M[1] - 0.1, 0))
    for j, (nm, val, col, at, xoff) in enumerate(rows):
        yy = 480 + j * 230
        g = ease((t - at) / 0.5) * kb
        if g <= 0: continue
        x0 = X0 + xoff
        text(d, (x0, yy), nm, FS, mix(col, INK, 0.2), anchor="lm", alpha=g)
        wbar = L * val * g
        if wbar > 2: d.rounded_rectangle([x0, yy + 45, x0 + wbar, yy + 135], radius=14, fill=A(col, kb))
        if g > 0.95: text(d, (x0 + L * val / 2, yy + 90), vn(val, 2), FL, WHITE)
    k3 = appear(t, M[1] - 0.1, 0.5) * kb
    if k3 > 0:
        for xx in (X0 + L * I1, X0 + L):
            for y in range(540, 1110, 24): d.line([(xx, y), (xx, y + 12)], fill=A(DGREEN, k3), width=4)
        text(d, (W / 2, 1180), "0,60 + 0,40 = 1,00", 64, DGREEN, alpha=k3)


# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 270, 1040, 500), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=5)
    text(d, (W / 2, 345), "Rẽ ở A, nhập lại ở B", FL, DGREEN, alpha=k0)
    text(d, (W / 2, 435), "I = I1 + I2", 64, DGREEN, alpha=k0)
    k1 = appear(t, M[1] - 0.1, 0.4)
    if k1 <= 0: return
    card(d, (40, 540, 1040, 1200), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    xa, xb = 170, 910
    for y, nm, col in ((680, "R1", C1), (860, "R2", C2)):
        d.line([(xa, y), (420, y)], fill=A(WIRE, k1), width=6); d.line([(660, y), (xb, y)], fill=A(WIRE, k1), width=6)
        resistor(d, 420, 660, y, nm, None, col, a=k1)
        text(d, (790, y - 60), "6,0 V", FL, PURPLE, alpha=k1)
    d.line([(xa, 680), (xa, 860)], fill=A(WIRE, k1), width=6); d.line([(xb, 680), (xb, 860)], fill=A(WIRE, k1), width=6)
    text(d, (xa - 45, 770), "A", FS, INK, alpha=k1); text(d, (xb + 45, 770), "B", FS, INK, alpha=k1)
    d.rounded_rectangle([70, 990, 1010, 1160], radius=24, fill=A((236, 253, 243), k1))
    text(d, (W / 2, 1075), "U = U1 = U2", 64, DGREEN, alpha=k1)


# ---------------- canh 5: Bay (hai o canh nhau) roi Chua noi duoc ----------------
BAY_R, BAY_C = 3.4, 6.4
def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FS)) + 64
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 348), fill=A(DRED, a1), r=40)
    text(d, (W / 2, 308), "BẪY", FS, WHITE, alpha=a1)
    text(d, (W / 2, 410), "“Cộng R như nối tiếp”", FL, INK, alpha=a1)
    card(d, (40, 470, 530, 1260), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    for j, s in enumerate(("10 + 15", "= 25 Ω", "6 V : 25 Ω", "= 0,24 A")):
        text(d, (285, 570 + j * 110), s, FL, DRED if j % 2 else INK, alpha=a1)
    text(d, (285, 1170), "✗ ≠ 1,00 A", FS, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (550, 470, 1040, 1260), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        for j, s in enumerate(("song song:", "R = 6 Ω", "6 V : 6 Ω", "= 1,00 A")):
            text(d, (795, 570 + j * 110), s, FL, DGREEN if j % 2 else INK, alpha=a2)
        text(d, (795, 1170), "✓ khớp", FS, DGREEN, alpha=a2)
    k3 = appear(t, BAY_C, 0.45)
    if k3 > 0:
        card(d, (40, 1300, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1370), "Chưa nói được:", FL, NAVY, alpha=k3)
        text(d, (W / 2, 1475), "bỏ qua điện trở nguồn, ampe kế", FS, INK, alpha=k3)


# ---------------- canh 6: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 415), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 340), "Song song: U như nhau, I cộng", FS, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 450, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FS)) + 60
    card(d, (W / 2 - pw / 2, 478, W / 2 + pw / 2, 558), fill=A(ORANGE, k1), r=40)
    text(d, (W / 2, 518), "THỬ NGHĨ", FS, WHITE, alpha=k1)
    text(d, (W / 2, 650), "Thay R2 bằng 30 Ω.", FL, INK, alpha=k1)
    text(d, (W / 2, 735), "Ampe kế mạch chính chỉ?", FL, INK, alpha=k1)
    xa, xb = 300, 900
    for y, nm, val, col in ((900, "R1", "10 Ω", C1), (1080, "R2", "30 Ω", C2)):
        d.line([(xa, y), (480, y)], fill=A(WIRE, k1), width=6); d.line([(720, y), (xb, y)], fill=A(WIRE, k1), width=6)
        resistor(d, 480, 720, y, nm, None, col, a=k1)
        text(d, (820, y - 50), val, FS, mix(col, INK, 0.3), alpha=k1)
    d.line([(xa, 900), (xa, 1080)], fill=A(WIRE, k1), width=6); d.line([(xb, 900), (xb, 1080)], fill=A(WIRE, k1), width=6)
    d.line([(xa, 990), (206, 990)], fill=A(WIRE, k1), width=6)
    meter(d, 160, 990, "A", BLUE, a=k1)
    d.line([(160, 1036), (160, 1220), (520, 1220)], fill=A(WIRE, k1), width=6, joint="curve")
    d.line([(560, 1220), (980, 1220), (980, 990), (xb, 990)], fill=A(WIRE, k1), width=6, joint="curve")
    d.line([(520, 1170), (520, 1270)], fill=A(NAVY, k1), width=6); d.line([(560, 1194), (560, 1246)], fill=A(NAVY, k1), width=14)
    text(d, (680, 1275), "6 V", FL, INK, alpha=k1)
    card(d, (290, 1360, 790, 1490), fill=A(SCREEN, k1), r=20)
    text(d, (540, 1425), "? A", 72, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + T_CLOSE, "tap"),
            (da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.3, "buzz"),
            (b["t0"] + BAY_R, "tap"), (e["t0"] + END_Q + 0.1, "open")]


CLIP = dict(id="tn-l9-doanmach-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Mạch song song · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai nhánh song song", draw=s_hook, tail=0.3, caps=[
   ("R1 và R2 nối chung A, B.", 2.9),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đóng K, đọc từng đồng hồ.", 3.4),
   ("Vôn kế đo giữa A và B.", 3.4),
   ("Mỗi nhánh một ampe kế.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Ghép hai thanh nhánh.", 2.9),
   ("Vừa khít thanh mạch chính.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Dòng chia cho hai nhánh.", 3.0),
   ("Hai nhánh chung hai đầu.", 3.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Cộng như nối tiếp?", 3.0),
   ("R song song nhỏ hơn.", 3.0),
   ("Còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Dừng lại, tự tính.", 6.1)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
