# Clip: tn-l11-dien-tro-ohm-01 - Do U va I cua dien tro 10 Ohm: ti so U/I khi tang U (ban 1, 16/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-tro-ohm-01.json (ghi_chu "Khong phai so do that" -> nhan
#   "số liệu mô phỏng"): so_lieu_mau (U V, I A, U/I Ohm): 1,0 0,10 10 ; 2,0 0,20 10 ; 3,0 0,30 10 ; 4,0 0,40 10 ;
#   5,0 0,50 10. Kiem bang ma: I = U/R voi R = 10 (_kiem_so()).
# Du doan (K10: chi cau hoi + hinh, khung ben canh co lua chon): o 1,0 V thay U/I = 10 Ohm; tang U len 5,0 V, U/I?
#   A. Tang theo U (5,0 V thi 50 Ohm)  [hien_tuong_hay_sai[0]] ; B. Giam dan, dong lon di de hon ; C. Khong doi, van 10 Ohm (DUNG).
# KHONG tra loi san cau trong bai: q3 (hang nao tinh R chinh xac nhat -> khong noi sai so, khong thanh sai so),
#   q2 (doi kOhm/mA -> khong dung bay don vi), q4 (vi sao R den tang -> khong noi nhiet do/nguyen nhan),
#   q7 (doc hon thi R nho hon -> cau chot KHONG hoi doc/thoai). q5 (muc III) trung so lieu kho, khong tranh duoc.
# Bay = hien_tuong_hay_sai[0] "U tang thi R tang vi R = U/I" -> bang do van 10 Ohm.
# Cau chot (tu suy trong dai tham_so R 5-50 Ohm, U 0-6 V): dien tro 40 Ohm, dat 6,0 V -> I = 0,15 A.
#   (Khong dung ca 20 Ohm/5,0 V trong ghi_chu kho: hop exp in san "duong 10 Ohm doc gap doi duong 20 Ohm".)
#   0,15 A khong hien tren man. Nhieu: 0,60 (giu R 10), 0,125 (dung 5,0 V cu), 6,7 (chia nguoc R/U).
# Ban 2 cong moi 27/11/2026: chu >= 56 px, bo nut/chu "Chon dap an", bo the Goi y, nhip Bay >= 3 s.
# Mach: nguon vach dai (+) o TREN -> dong di len day trai, sang phai day tren (K, ampe ke, R), xuong day phai,
#   sang TRAI o day duoi ve (-). Von ke song song hai dau R. Assert chieu: _kiem_chieu().
# Bo cuc (khac ohm3 = dung cu + bang doc): so do mach + 3 o so (von ke, ampe ke, U/I) o tren, DO THI I-U o duoi,
#   cham diem dong bo voi so chi (_kiem_dong_bo()).
from engine import *

ROWS = [(1.0, 0.10, 10), (2.0, 0.20, 10), (3.0, 0.30, 10), (4.0, 0.40, 10), (5.0, 0.50, 10)]   # so_lieu_mau
R_OHM = 10
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def _kiem_so():
    return [r for r in ROWS if abs(r[0] / R_OHM - r[1]) > 1e-9 or round(r[0] / r[1]) != r[2]]
assert not _kiem_so()

WIRE = (60, 66, 92); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100)
DRED = (185, 28, 28); NOTE = (60, 64, 84)

# ---------------- so do mach ----------------
XL, XR, YT, YB = 150, 930, 430, 640          # khung mach
YP, YN = 515, 545                             # vach (+) dai o tren, (-) ngan o duoi
AX, RX0, RX1 = 440, 600, 780                  # ampe ke ; dien tro
NV0, NV1, VY, VX = 570, 810, 315, 690         # nut von ke ; von ke
PLUS_TOP = True

def _kiem_chieu():
    """Dong quy uoc ra tu (+). (+) o tren -> day trai di LEN -> day tren sang PHAI -> day duoi sang TRAI."""
    top_dir = 1 if PLUS_TOP else -1
    bottom_dir = -top_dir
    assert bottom_dir == -1          # mui ten tren day duoi ve sang trai
    return top_dir, bottom_dir
_kiem_chieu()

DGREEN = (21, 110, 55); EMPTY = (148, 140, 128)

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

def circuit(d, pulse=0.0):
    d.line([(XL, YP), (XL, YT), (AX - 44, YT)], fill=WIRE, width=6, joint="curve")
    d.line([(AX + 44, YT), (RX0, YT)], fill=WIRE, width=6)
    d.line([(RX1, YT), (XR, YT), (XR, YB), (XL, YB), (XL, YN)], fill=WIRE, width=6, joint="curve")
    d.line([(XL - 56, YP), (XL + 56, YP)], fill=ORANGE, width=7)
    d.line([(XL - 28, YN), (XL + 28, YN)], fill=ORANGE, width=16)
    arrow(d, (XL - 60, YN + 40), (XL + 60, YP - 40), A(NAVY, 0.9), w=4, head=16)
    text(d, (XL - 90, YP - 30), "+", 60, ORANGE)
    text(d, (XL - 90, YN + 30), "−", 60, ORANGE)
    text(d, (XL + 76, (YP + YN) / 2), "nguồn", 56, NOTE, anchor="lm")
    if pulse > 0:
        k = clamp(pulse / 0.15) * clamp((1 - pulse) / 0.4)
        pill(d, 330, 300, "tăng U", ORANGE, k, size=56)
    dot(d, 245, YT, 9, WIRE); dot(d, 325, YT, 9, WIRE); d.line([(245, YT), (325, YT)], fill=NAVY, width=7)
    text(d, (285, YT - 50), "K", 56, NAVY)
    d.ellipse([AX - 44, YT - 44, AX + 44, YT + 44], fill=WHITE, outline=BLUE, width=6); text(d, (AX, YT + 2), "A", 56, BLUE)
    d.rectangle([RX0, YT - 24, RX1, YT + 24], fill=WHITE, outline=NAVY, width=5)
    text(d, ((RX0 + RX1) / 2, YT + 70), "R = 10 Ω", 56, NAVY)
    d.line([(NV0, YT), (NV0, VY), (VX - 44, VY)], fill=WIRE, width=5, joint="curve")
    d.line([(NV1, YT), (NV1, VY), (VX + 44, VY)], fill=WIRE, width=5, joint="curve")
    dot(d, NV0, YT, 8, WIRE); dot(d, NV1, YT, 8, WIRE)
    d.ellipse([VX - 44, VY - 44, VX + 44, VY + 44], fill=WHITE, outline=PURPLE, width=6); text(d, (VX, VY + 2), "V", 56, PURPLE)
    arrow(d, (640, YB - 34), (520, YB - 34), RED, w=7, head=20)
    text(d, (662, YB - 34), "I", 58, RED, anchor="lm")

def readout(d, x0, x1, label, reading, flash=0.0):
    card(d, (x0, 690, x1, 850), fill=BODY, r=20)
    card(d, (x0 + 16, 704, x1 - 16, 784), fill=mix(SCREEN, (255, 237, 160), flash), r=10)
    text(d, ((x0 + x1) / 2, 744), reading, 58, SCR_INK)
    text(d, ((x0 + x1) / 2, 818), label, 56, WHITE)

def readouts(d, j, flash=0.0):
    u, i, r = ROWS[j]
    readout(d, 50, 370, "vôn kế", vn(u) + " V")
    readout(d, 385, 705, "ampe kế", vn(i, 2) + " A")
    readout(d, 720, 1030, "U/I", f"{r} Ω", flash)

# ---------------- do thi I theo U (truc co dinh) ----------------
GX0, GX1, GY0, GY1 = 220, 930, 1470, 1010        # U 0-6 V ; I 0-0,6 A
def gx(u): return GX0 + u / 6 * (GX1 - GX0)
def gy(i): return GY0 - i / 0.6 * (GY0 - GY1)

def axes(d, y_top=880, note=True):
    card(d, (40, y_top, 1040, 1580), fill=WHITE, outline=LIGHT, w=3)
    if note: text(d, (1010, y_top + 45), "số liệu mô phỏng", 56, NOTE, bold=False, anchor="rm")
    for i in (0.2, 0.4, 0.6):
        d.line([(GX0, gy(i)), (GX1, gy(i))], fill=LIGHT, width=3)
        text(d, (GX0 - 18, gy(i)), vn(i), 56, NOTE, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 36), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 36, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 22, GY1 - 40), "I (A)", 56, INK, anchor="lm")
    text(d, (1020, GY0 - 50), "U (V)", 56, INK, anchor="rm")
    for u in range(1, 7):
        d.line([(gx(u), GY0), (gx(u), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(u), GY0 + 50), str(u), 56, NOTE)

def pts(d, n, pop=None, col=BLUE):
    for j in range(n):
        r = 15 if (pop is None or j < n - 1) else 15 + 10 * (1 - pop)
        dot(d, gx(ROWS[j][0]), gy(ROWS[j][1]), r, col, outline=WHITE)

def line_origin(d, k, col=BLUE, w=6):
    if k <= 0: return
    u1 = 5.0 * k
    d.line([(gx(0), gy(0)), (gx(u1), gy(u1 / R_OHM))], fill=A(col, 0.85), width=w)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d); readouts(d, 0)
    a = appear(t, M[1] - 0.2, 0.4)
    if a <= 0: return
    y0 = 900 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 660), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 190), "Ở 1,0 V: U/I = 10 Ω.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "Tăng dần U lên 5,0 V.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 400), "Tỉ số U/I sẽ thế nào?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 540, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
TS = [0.6 + 1.6 * k for k in range(5)]        # lan do k: chinh U = ROWS[k][0], so chi + diem moi hien CUNG luc

def do_state(t):
    """-> (n diem da cham, hang dang chi tren dong ho, pop 0..1 cua diem moi, pulse 'tang U')."""
    n = sum(1 for ts in TS if t >= ts - 1e-9)
    j = max(0, n - 1)
    pop = clamp((t - TS[n - 1]) / 0.3) if n > 0 else None
    pulse = (t - TS[n - 1] + 0.25) / 1.0 if n > 1 and t - TS[n - 1] < 0.75 else 0.0
    return n, j, pop, pulse

def s_do(img, d, t, sc):
    n, j, pop, pulse = do_state(t)
    circuit(d, pulse); flash = 1 - clamp((t - TS[n - 1]) / 0.6) if n > 0 else 0
    readouts(d, j, flash)
    axes(d); pts(d, n, pop)

def _kiem_dong_bo():
    """Moi 0,05 s: diem cuoi da cham = hang dang chi tren dong ho (sau lan do dau)."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        n, j, pop, pulse = do_state(t)
        if n > 0 and j != n - 1: bad.append(round(t, 2))
        t += 0.05
    if TS[-1] + 0.6 > sc["T"]: bad.append("diem cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def htable(d, y0, a=1.0, hl=0.0):
    """Bang ngang: hang U, I, U/I ; 5 cot. hl: to sang hang U/I."""
    card(d, (40, y0, 1040, y0 + 330), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    if hl > 0: d.rounded_rectangle([55, y0 + 225, 1025, y0 + 315], radius=18, fill=A((220, 252, 231), a * hl))
    labs = ("U (V)", "I (A)", "U/I (Ω)"); xs = [360 + 150 * k for k in range(5)]
    for r, lab in enumerate(labs):
        yy = y0 + 65 + 100 * r
        text(d, (70, yy), lab, 56, INK, anchor="lm", alpha=a)
        for k, row in enumerate(ROWS):
            s = vn(row[0]) if r == 0 else (vn(row[1], 2) if r == 1 else str(row[2]))
            text(d, (xs[k], yy), s, 56, GREEN if r == 2 else (BLUE if r == 1 else INK), alpha=a)
    d.line([(60, y0 + 215), (1020, y0 + 215)], fill=A(LIGHT, a), width=3)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = 1.0
    pill(d, W / 2, 300, "ĐÁP ÁN · vẫn 10 Ω", NAVY, ka)
    kr = appear(t, M[1] + 0.1, 0.45)
    if kr < 1: htable(d, 400, ka * (1 - kr), appear(t, 2.0, 0.4))
    axes(d); line_origin(d, appear(t, M[0] + 1.2, 1.0)); pts(d, 5)
    if kr > 0:
        y0 = 380 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pill(d, W / 2, y0 + 70, "RÚT RA", GREEN, kr)
        text(d, (W / 2, y0 + 190), "I tỉ lệ thuận với U", 62, INK, alpha=kr)
        text(d, (W / 2, y0 + 290), "(khi R không đổi)", 58, DGREEN, alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    axes(d); line_origin(d, 1.0); pts(d, 5)
    k2 = appear(t, M[1] - 0.1, 0.4); k3 = appear(t, M[2] - 0.1, 0.45)
    if k2 > 0:
        for j, (u, i, r) in enumerate(ROWS):
            text(d, (gx(u) - 62, gy(i) - 50), "10 Ω", 56, GREEN, alpha=k2 * (1 - k3))
    a1 = 1.0 - k3; y = 300
    if a1 > 0:
        card(d, (40, y, 1040, y + 520), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", DRED, a1)
        q = "“U tăng thì R tăng”"
        f = F(64); lw = tw(d, q, f); yy = y + 220
        text(d, (W / 2, yy), q, 64, mix(INK, GRAY, k2), alpha=a1)
        if k2 > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * k2, yy + 2)], fill=A(DRED, 0.85 * a1), width=7)
            text(d, (W / 2, y + 380), "U/I vẫn 10 Ω ở cả 5 hàng", 60, DGREEN, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 520), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 240), "Thay bằng bóng đèn,", 62, INK, alpha=k3)
        text(d, (W / 2, y + 340), "đường còn thẳng?", 62, INK, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    """THU NGHI: dien tro 40 Ohm, dat 6,0 V -> ampe ke? (0,15 A, khong hien)."""
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    d.line([(150, 560), (900, 560)], fill=A(WIRE, k), width=6)
    d.rectangle([450, 530, 630, 590], fill=A(WHITE, k), outline=A(NAVY, k), width=5)
    text(d, (540, 650), "R = 40 Ω", 60, NAVY, alpha=k)
    d.ellipse([250 - 50, 560 - 50, 250 + 50, 560 + 50], fill=A(WHITE, k), outline=A(BLUE, k), width=6)
    text(d, (250, 562), "A", 58, BLUE, alpha=k); text(d, (250, 460), "? A", 60, DRED, alpha=k)
    card(d, (700, 420, 960, 500), fill=A(SCREEN, k), r=10); text(d, (830, 460), "U = 6,0 V", 56, SCR_INK, alpha=k)
    text(d, (W / 2, 900), "Điện trở 40 Ω, đặt 6,0 V.", 64, INK, alpha=k)
    text(d, (W / 2, 1010), "Ampe kế chỉ bao nhiêu?", 64, DRED, alpha=k)
    seg_bar(d, 1330, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + ts, "tap") for ts in TS]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l11-dien-tro-ohm-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện trở · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo U và I của điện trở", draw=s_hook, tail=0.3, caps=[
   ("Ampe kế đo I, vôn kế đo U.", 3.6),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Tăng U từng 1,0 V, ghi I.", 4.0),
   ("Mỗi lần đo, chấm một điểm.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Năm điểm thẳng hàng, qua gốc.", 4.2),
   ("U gấp mấy, I gấp bấy nhiêu.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy: nhìn R = U/I.", 3.6),
   ("Chia lại U cho I từng điểm.", 3.6),
   ("Mới đo một điện trở.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng lại, tự trả lời.", 7.2)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
