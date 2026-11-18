# Clip: tn-l9-doanmach-02 - Dong dien re nhanh trong doan mach song song R1 = 10 Ohm // R2 = 15 Ohm, nguon 6 V (KHTN 9, lo 6)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-doanmach-02.json:
#   so_lieu_mau (du hai nhanh): U 6,0 V ; I1 0,60 A ; I2 0,40 A ; I 1,00 A. tham_so R1 10, R2 15 (dieu chinh 10..30, buoc 5).
#   rut_ra: U = U1 = U2 ; I = I1 + I2 ; R_td = 6 Ohm nho hon ca 10 va 15. bay = hien_tuong_hay_sai[2] (cong R1 + R2).
#   chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet[0].
#   KHONG thao nhanh (kho chi co hang "du hai nhanh"; Cau 6 muc III hoi bong song song dut -> clip khong tra loi san).
# Du doan (K10: chi cau hoi + hinh): A1 chi 0,60 A, A2 chi 0,40 A -> ampe ke mach chinh chi? -> 1,00 A.
# Cau chot (ghi o kho ghi_chu): thay R2 bang 30 Ohm (R1 = 10 Ohm, nguon 6 V giu nguyen) -> ampe ke mach chinh? -> 0,80 A
#   (I1 = 0,60 ; I2 = 0,20). 30 Ohm chua tung hien; can hai buoc, khong mot phep tinh tu so da hien.
# Mach: nguon (+ ban dai trai, day duoi) -> K -> ampe ke mach chinh (+ trai) -> canh trai len -> nut A -> re hai nhanh
#   (A1 + R1 tren, A2 + R2 duoi) -> nut B -> canh phai xuong -> (-). Von ke song song giua A va B (+ o A).
#   _kiem_dong_bo(): moi 0,05 s K mo <=> moi dong ho 0 ; K dong <=> dung so lieu mau.
import copy
from engine import *

U, R1, R2 = 6.0, 10.0, 15.0
I1, I2, I = 0.60, 0.40, 1.00          # so_lieu_mau
R2_C, I_C = 30.0, 0.80                # cau chot (kho ghi_chu)
RTD = 6.0                             # rut_ra
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); RCOL = (180, 83, 9)
C1, C2 = TEAL, ORANGE

# ---------------- so do mach ----------------
XL, XR, NA, NB = 90, 990, 230, 850
YM, Y1, Y2, YB, YV = 510, 420, 600, 880, 750
A1X, RX0, RX1 = 360, 500, 690
AMX, KX0, KX1, SX = 420, 190, 280, 650
AR, VR = 38, 42

def resistor(d, x0, x1, y, lab, col=RCOL, a=1.0, ly=None):
    card(d, (x0, y - 30, x1, y + 30), fill=A(mix(WHITE, col, 0.18), a), outline=A(col, a), r=10, w=5)
    if lab: text(d, ((x0 + x1) / 2, ly if ly else y - 64), lab, 40, mix(col, INK, 0.3), alpha=a)

def meter(d, x, y, ch, col, a=1.0):
    d.ellipse([x - AR, y - AR, x + AR, y + AR], fill=A(WHITE, a), outline=A(col, a), width=6)
    text(d, (x, y + 2), ch, 42, col, alpha=a)

def circuit(d, closed, r2=R2, src=U):
    card(d, (40, 260, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    # mach chinh
    d.line([(SX - 20, YB), (AMX + AR, YB)], fill=WIRE, width=w)
    d.line([(AMX - AR, YB), (KX1, YB)], fill=WIRE, width=w)
    d.line([(KX0, YB), (XL, YB), (XL, YM), (NA, YM)], fill=WIRE, width=w, joint="curve")
    d.line([(NB, YM), (XR, YM), (XR, YB), (SX + 20, YB)], fill=WIRE, width=w, joint="curve")
    # hai nhanh
    for y in (Y1, Y2):
        d.line([(NA, YM), (NA, y), (A1X - AR, y)], fill=WIRE, width=w, joint="curve")
        d.line([(A1X + AR, y), (RX0, y)], fill=WIRE, width=w)
        d.line([(RX1, y), (NB, y), (NB, YM)], fill=WIRE, width=w, joint="curve")
    resistor(d, RX0, RX1, Y1, f"R1 = {R1:.0f} Ω", C1)
    resistor(d, RX0, RX1, Y2, f"R2 = {r2:.0f} Ω", C2)
    meter(d, A1X, Y1, "A", BLUE); text(d, (A1X, Y1 - 66), "A1", 40, C1); text(d, (A1X - AR - 18, Y1 - 40), "+", 40, BLUE)
    meter(d, A1X, Y2, "A", BLUE); text(d, (A1X, Y2 + 66), "A2", 40, C2); text(d, (A1X - AR - 18, Y2 - 40), "+", 40, BLUE)
    for x, nm in ((NA, "A"), (NB, "B")):
        dot(d, x, YM, 10, WIRE); text(d, (x + (36 if nm == "A" else -36), YM), nm, 44, INK)
    # von ke giua A va B
    d.line([(NA, Y2), (NA, YV), (540 - VR, YV)], fill=PURPLE, width=5, joint="curve")
    d.line([(NB, Y2), (NB, YV), (540 + VR, YV)], fill=PURPLE, width=5, joint="curve")
    dot(d, NA, Y2, 8, WIRE); dot(d, NB, Y2, 8, WIRE)
    d.ellipse([540 - VR, YV - VR, 540 + VR, YV + VR], fill=WHITE, outline=PURPLE, width=6)
    text(d, (540, YV + 2), "V", 42, PURPLE); text(d, (540 - VR - 22, YV - 40), "+", 40, PURPLE)
    # ampe ke mach chinh, khoa K, nguon
    meter(d, AMX, YB, "A", BLUE); text(d, (AMX, YB + 66), "mạch chính", 40, BLUE)
    text(d, (AMX + AR + 18, YB - 40), "+", 40, BLUE)   # dong tu cuc + (ben phai) chay sang trai vao ampe ke
    dot(d, KX0, YB, 9, WIRE); dot(d, KX1, YB, 9, WIRE)
    if closed: d.line([(KX0, YB), (KX1, YB)], fill=NAVY, width=7)
    else: d.line([(KX0, YB), (KX1 - 12, YB - 50)], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, YB + 66), "K", 40, NAVY)
    d.line([(SX - 20, YB - 50), (SX - 20, YB + 50)], fill=NAVY, width=6)
    d.line([(SX + 20, YB - 26), (SX + 20, YB + 26)], fill=NAVY, width=14)
    text(d, (SX - 52, YB - 44), "+", 44, ORANGE); text(d, (SX + 54, YB - 44), "−", 44, ORANGE)
    text(d, (845, YB + 66), f"nguồn {src:.0f} V", 40, INK)
    if closed:   # chieu dong dien
        arrow(d, (XL, 820), (XL, 600), RED, w=7, head=20)
        arrow(d, (XR, 580), (XR, 800), RED, w=7, head=20)
        arrow(d, (RX1 + 30, Y1), (RX1 + 120, Y1), RED, w=7, head=20)
        arrow(d, (RX1 + 30, Y2), (RX1 + 120, Y2), RED, w=7, head=20)

def readings(closed):
    return (U, I1, I2, I) if closed else (0.0, 0.0, 0.0, 0.0)

def panel(d, closed, hide_main=False, y=1020):
    u, i1, i2, i = readings(closed)
    items = [((40, y), "vôn kế (A, B)", vn(u) + " V", PURPLE),
             ((550, y), "ampe kế mạch chính", ("?" if hide_main else vn(i, 2)) + " A", BLUE),
             ((40, y + 190), "A1 (nhánh R1)", vn(i1, 2) + " A", C1),
             ((550, y + 190), "A2 (nhánh R2)", vn(i2, 2) + " A", C2)]
    for (x, yy), lab, val, col in items:
        card(d, (x, yy, x + 490, yy + 170), fill=BODY, r=22)
        text(d, (x + 245, yy + 38), lab, 40, WHITE)
        card(d, (x + 50, yy + 70, x + 440, yy + 155), fill=SCREEN, r=12)
        text(d, (x + 245, yy + 113), val, 52, SCR_INK)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a < 1: panel(d, False)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 580), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 240, "Đóng K: A1 chỉ 0,60 A, A2 chỉ 0,40 A.\nAmpe kế mạch chính chỉ bao nhiêu?", 48, INK,
          maxw=940, alpha=a)
    text(d, (W / 2, y0 + 410), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 512], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 512], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T_CLOSE = 0.9
def do_closed(t): return t >= T_CLOSE
def s_do(img, d, t, sc):
    c = do_closed(t)
    circuit(d, c); panel(d, c)

def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        c = do_closed(t); r = readings(c)
        if not c and any(r): bad.append((round(t, 2), "K mo ma co so"))
        if c and r != (U, I1, I2, I): bad.append((round(t, 2), "K dong sai so"))
        t += 0.05
    return bad

def _kiem_so():
    bad = []
    if abs(U / R1 - I1) > 0.005 or abs(U / R2 - I2) > 0.005: bad.append("I nhanh = U/R")
    if abs(I1 + I2 - I) > 1e-9: bad.append("I = I1 + I2")
    if abs(R1 * R2 / (R1 + R2) - RTD) > 1e-9 or abs(U / RTD - I) > 1e-9: bad.append("R_td")
    if abs(U / R1 + U / R2_C - I_C) > 1e-9: bad.append("chot")
    return bad

# ---------------- canh 3: Dap an (thanh cong don) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · 1,00 A"
    pw = tw(d, lab, F(44)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 348), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 310), lab, 44, WHITE, alpha=ka)
    kb = appear(t, 0.5, 0.4)
    card(d, (40, 390, 1040, 1200), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
    X0, L = 120, 800                       # 1,00 A <-> 800 px
    rows = (("A1", I1, C1, 0.7), ("A2", I2, C2, 1.2), ("mạch chính", I, BLUE, M[1] - 0.1))
    for j, (nm, val, col, at) in enumerate(rows):
        yy = 480 + j * 220
        g = ease((t - at) / 0.5) * kb
        if g <= 0: continue
        text(d, (X0, yy), nm, 42, mix(col, INK, 0.2), anchor="lm", alpha=g)
        x0 = X0 + (L * I1 if nm == "A2" else 0)       # thanh A2 noi tiep sau thanh A1 de thay phep cong
        wbar = L * val * g
        if wbar > 2: d.rounded_rectangle([x0, yy + 45, x0 + wbar, yy + 125], radius=14, fill=A(col, kb))
        if g > 0.95: text(d, (x0 + L * val / 2, yy + 85), vn(val, 2) + " A", 44, WHITE)
    k3 = appear(t, M[1] + 0.8, 0.4) * kb
    if k3 > 0:
        for xx in (X0 + L * I1, X0 + L):          # khong ke net dut o X0: tranh nhan A2, mach chinh
            for y in range(540, 1060, 22): d.line([(xx, y), (xx, y + 12)], fill=A(DGREEN, k3), width=4)
        text(d, (W / 2, 1130), "0,60 + 0,40 = 1,00", 50, DGREEN, alpha=k3)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 270, 1040, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=5)
    text(d, (W / 2, 350), "Dòng tới A rẽ hai nhánh,", 46, DGREEN, alpha=k0)
    text(d, (W / 2, 420), "tới B nhập lại", 46, DGREEN, alpha=k0)
    text(d, (W / 2, 505), "I = I1 + I2", 52, DGREEN, alpha=k0)
    k1 = appear(t, M[1] - 0.1, 0.4)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1180), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    # hai nhanh cung noi vao A va B -> von ke A, B do ca hai nhanh
    xa, xb = 170, 910
    for y, lab, col in ((720, "R1", C1), (880, "R2", C2)):
        d.line([(xa, y), (420, y)], fill=A(WIRE, k1), width=6); d.line([(660, y), (xb, y)], fill=A(WIRE, k1), width=6)
        resistor(d, 420, 660, y, None, col, a=k1); text(d, (540, y + 2), lab, 42, mix(col, INK, 0.3), alpha=k1)
        kv = appear(t, M[1] + 0.6 + (0.5 if lab == "R2" else 0), 0.4) * k1
        text(d, (790, y - 50), "6,0 V", 44, PURPLE, alpha=kv)
    d.line([(xa, 720), (xa, 880)], fill=A(WIRE, k1), width=6); d.line([(xb, 720), (xb, 880)], fill=A(WIRE, k1), width=6)
    text(d, (xa - 40, 800), "A", 44, INK, alpha=k1); text(d, (xb + 40, 800), "B", 44, INK, alpha=k1)
    k2 = appear(t, M[1] + 1.6, 0.4) * k1
    if k2 > 0:
        d.rounded_rectangle([70, 970, 1010, 1150], radius=24, fill=A((236, 253, 243), k2))
        text(d, (W / 2, 1020), "U = U1 = U2", 50, DGREEN, alpha=k2)
        text(d, (W / 2, 1100), "mỗi nhánh nhận đủ 6,0 V", 44, DGREEN, alpha=k2)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 330), "Điện trở tương đương?", 44, INK)
    text(d, (300, 440), "R1 = 10 Ω", 44, C1); text(d, (780, 440), "R2 = 15 Ω", 44, C2)
    text(d, (540, 440), "song song", 40, MUTED, bold=False)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 600
        card(d, (40, y0, 1040, y0 + 820), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[0] - 1.6) / 0.4)
        q = "“10 + 15 = 25 Ω”"; yy = y0 + 220; lw = tw(d, q, F(56))
        text(d, (W / 2, yy), q, 56, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 + lw / 2 + 40, yy), "✗", 56, DRED, alpha=a1 * ks)
        text(d, (W / 2, y0 + 310), "cộng như nối tiếp", 44, MUTED, bold=False, alpha=a1)
        kk = a1 * appear(t, M[0] + 2.2, 0.4)
        card(d, (70, y0 + 400, 1010, y0 + 780), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 490), "✓ Song song: 6 Ω", 52, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 590), "nhỏ hơn cả 10 Ω và 15 Ω", 46, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 690), "6,0 V : 6 Ω = 1,00 A", 46, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 600 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 630), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 95), "Chưa nói được", 52, NAVY, alpha=k2)
        for j, (l1, l2) in enumerate((("• Số liệu minh hoạ", ""),
                                      ("• Bỏ qua điện trở", "nguồn, ampe kế"))):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y0 + 260 + j * 230), l1, 50, INK, anchor="lm", alpha=kk)
            if l2: text(d, (132, y0 + 335 + j * 230), l2, 50, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def end_body(d, t, k):
    """Hinh nho: hai nhanh R1 10 Ohm, R2 30 Ohm giua A, B; ampe ke mach chinh '?'."""
    xa, xb = 250, 830
    for y, lab, col in ((990, "10 Ω", C1), (1130, "30 Ω", C2)):
        d.line([(xa, y), (430, y)], fill=A(WIRE, k), width=6); d.line([(650, y), (xb, y)], fill=A(WIRE, k), width=6)
        resistor(d, 430, 650, y, None, col, a=k); text(d, (540, y + 2), lab, 40, mix(col, INK, 0.3), alpha=k)
    d.line([(xa, 990), (xa, 1130)], fill=A(WIRE, k), width=6); d.line([(xb, 990), (xb, 1130)], fill=A(WIRE, k), width=6)
    d.line([(xa, 1060), (110 + AR + 30, 1060)], fill=A(WIRE, k), width=6)
    meter(d, 110 + AR + 30 - AR, 1060, "A", BLUE, a=k)
    text(d, (110 + 30, 1135), "?", 48, BLUE, alpha=k)
    d.line([(xb, 1060), (960, 1060)], fill=A(WIRE, k), width=6)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Song song: U như nhau, I cộng lại",
             "Thay R2 bằng 30 Ω. Ampe kế mạch chính chỉ bao nhiêu?", body=end_body)
    kh = appear(t, M[0] + 2.8, 0.5)
    if kh > 0:
        card(d, (110, 1300, 970, 1560), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1360, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1470, "Nguồn 6 V, R1 = 10 Ω giữ nguyên", 42, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"),
            (do["t0"] + T_CLOSE, "tap"), (da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"),
            (b["t0"] + 0.2, "buzz"), (b["t0"] + b["M"][0] + 2.2, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l9-doanmach-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Mạch song song · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai nhánh song song", draw=s_hook, tail=0.8, caps=[
   ("R1 và R2 nối chung A, B.", 2.9),
   ("Ba ampe kế, một vôn kế.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đóng K, đọc bốn đồng hồ.", 3.6),
   ("Ghi lại bốn số chỉ.", 2.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Ghép hai thanh nhánh.", 2.6),
   ("Vừa khít thanh mạch chính.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Mạch chính chia cho hai nhánh.", 3.4),
   ("Hai nhánh cùng hai đầu A, B.", 3.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Có đúng không?", 4.4),
   ("Còn chưa nói được.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Tự trả lời trước khi xem.", 5.6)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
