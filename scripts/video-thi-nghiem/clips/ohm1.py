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
# Cau chot (ca tu suy, ghi trong ghi_chu kho): thay dien tro 20 Ohm (tham_so R 5-50), van 5,0 V -> I = 0,25 A,
#   bang mot nua 0,50 A cua lan 10 Ohm. So 20 Ohm / 0,25 A chua tung hien tren man.
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

def circuit(d, pulse=0.0):
    d.line([(XL, YP), (XL, YT), (AX - 44, YT)], fill=WIRE, width=6, joint="curve")
    d.line([(AX + 44, YT), (RX0, YT)], fill=WIRE, width=6)
    d.line([(RX1, YT), (XR, YT), (XR, YB), (XL, YB), (XL, YN)], fill=WIRE, width=6, joint="curve")
    # nguon dieu chinh: vach dai (+) tren, vach ngan day (-) duoi, mui ten cheo = dieu chinh duoc
    d.line([(XL - 56, YP), (XL + 56, YP)], fill=ORANGE, width=7)
    d.line([(XL - 28, YN), (XL + 28, YN)], fill=ORANGE, width=16)
    arrow(d, (XL - 60, YN + 40), (XL + 60, YP - 40), A(NAVY, 0.9), w=4, head=16)
    text(d, (XL - 84, YP - 26), "+", 44, ORANGE)
    text(d, (XL - 84, YN + 26), "−", 44, ORANGE)
    text(d, (XL + 76, (YP + YN) / 2), "nguồn", 40, NOTE, anchor="lm")
    if pulse > 0:
        k = clamp(pulse / 0.15) * clamp((1 - pulse) / 0.4)
        card(d, (170, 330, 340, 392), fill=A(ORANGE, k), r=24)
        text(d, (255, 361), "tăng U", 38, WHITE, alpha=k)
    # khoa K (dong)
    dot(d, 245, YT, 9, WIRE); dot(d, 325, YT, 9, WIRE); d.line([(245, YT), (325, YT)], fill=NAVY, width=7)
    text(d, (285, YT + 44), "K", 40, NAVY)
    # ampe ke noi tiep
    d.ellipse([AX - 44, YT - 44, AX + 44, YT + 44], fill=WHITE, outline=BLUE, width=6); text(d, (AX, YT + 2), "A", 42, BLUE)
    # dien tro
    d.rectangle([RX0, YT - 24, RX1, YT + 24], fill=WHITE, outline=NAVY, width=5)
    text(d, ((RX0 + RX1) / 2, YT + 66), "điện trở", 40, NAVY)
    # von ke song song
    d.line([(NV0, YT), (NV0, VY), (VX - 44, VY)], fill=WIRE, width=5, joint="curve")
    d.line([(NV1, YT), (NV1, VY), (VX + 44, VY)], fill=WIRE, width=5, joint="curve")
    dot(d, NV0, YT, 8, WIRE); dot(d, NV1, YT, 8, WIRE)
    d.ellipse([VX - 44, VY - 44, VX + 44, VY + 44], fill=WHITE, outline=PURPLE, width=6); text(d, (VX, VY + 2), "V", 42, PURPLE)
    # chieu dong quy uoc tren day duoi: sang trai (_kiem_chieu)
    arrow(d, (640, YB - 34), (520, YB - 34), RED, w=7, head=20)
    text(d, (662, YB - 34), "I", 50, RED, anchor="lm")

def readout(d, x0, x1, label, reading, flash=0.0):
    card(d, (x0, 690, x1, 820), fill=BODY, r=20)
    card(d, (x0 + 16, 704, x1 - 16, 768), fill=mix(SCREEN, (255, 237, 160), flash), r=10)
    text(d, ((x0 + x1) / 2, 736), reading, 46, SCR_INK)
    text(d, ((x0 + x1) / 2, 794), label, 38, WHITE)

def readouts(d, j, flash=0.0):
    u, i, r = ROWS[j]
    readout(d, 50, 370, "vôn kế", vn(u) + " V")
    readout(d, 385, 705, "ampe kế", vn(i, 2) + " A")
    readout(d, 720, 1030, "U/I", f"{r} Ω", flash)

# ---------------- do thi I theo U (truc co dinh) ----------------
GX0, GX1, GY0, GY1 = 200, 950, 1470, 960        # U 0-6 V ; I 0-0,6 A
def gx(u): return GX0 + u / 6 * (GX1 - GX0)
def gy(i): return GY0 - i / 0.6 * (GY0 - GY1)

def axes(d, y_top=860, note=True):
    card(d, (40, y_top, 1040, 1580), fill=WHITE, outline=LIGHT, w=3)
    if note: text(d, (1010, y_top + 40), "số liệu mô phỏng", 38, NOTE, anchor="rm")
    for i in (0.2, 0.4, 0.6):
        d.line([(GX0, gy(i)), (GX1, gy(i))], fill=LIGHT, width=3)
        text(d, (GX0 - 18, gy(i)), vn(i), 40, NOTE, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 36), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 36, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 22, GY1 - 40), "I (A)", 40, INK, anchor="lm")
    text(d, (1020, GY0 - 44), "U (V)", 40, INK, anchor="rm")
    text(d, (GX0 - 18, GY0 + 6), "0", 40, NOTE, anchor="rm")
    for u in range(1, 7):
        d.line([(gx(u), GY0), (gx(u), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(u), GY0 + 44), str(u), 40, NOTE)

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
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Ở 1,0 V: U/I = 10 Ω.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "Tăng dần U lên 5,0 V.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 350), "Tỉ số U/I sẽ thế nào?", 52, INK, alpha=a)
    text(d, (W / 2, y0 + 450), "Chọn đáp án ở khung câu hỏi", 40, NOTE, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 530, 940, y0 + 544], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 530, 140 + 800 * (1 - p), y0 + 544], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
TS = [0.6 + 1.3 * k for k in range(5)]        # lan do k: chinh U = ROWS[k][0], so chi + diem moi hien CUNG luc

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
def htable(d, y0, a=1.0):
    """Bang ngang: hang U, I, U/I ; 5 cot."""
    card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    labs = ("U (V)", "I (A)", "U/I (Ω)"); xs = [330 + 160 * k for k in range(5)]
    for r, lab in enumerate(labs):
        yy = y0 + 60 + 90 * r
        text(d, (80, yy), lab, 40, INK, anchor="lm", alpha=a)
        for k, row in enumerate(ROWS):
            s = vn(row[0]) if r == 0 else (vn(row[1], 2) if r == 1 else str(row[2]))
            text(d, (xs[k], yy), s, 42, GREEN if r == 2 else (BLUE if r == 1 else INK), alpha=a)
    d.line([(60, y0 + 195), (1020, y0 + 195)], fill=A(LIGHT, a), width=3)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.4)
    lab = "ĐÁP ÁN · Không đổi, vẫn 10 Ω"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 368), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 334), lab, 42, WHITE, alpha=ka)
    kr = appear(t, M[1] + 0.1, 0.45)
    if kr < 1: htable(d, 420, appear(t, 0.3, 0.4) * (1 - kr))
    axes(d); line_origin(d, appear(t, M[0] + 0.2, 1.0)); pts(d, 5)
    if kr > 0:
        y0 = 400 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pw = tw(d, "RÚT RA", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(GREEN, kr), r=32)
        text(d, (W / 2, y0 + 60), "RÚT RA", 40, WHITE, alpha=kr)
        text(d, (W / 2, y0 + 190), "I tỉ lệ thuận với U", 50, INK, alpha=kr)
        text(d, (W / 2, y0 + 290), "(khi R không đổi)", 44, (21, 110, 55), alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    axes(d); line_origin(d, 1.0); pts(d, 5)
    for j, (u, i, r) in enumerate(ROWS):           # nhan U/I tung diem (bang chung bac bay)
        kk = appear(t, 0.4 + 0.12 * j, 0.2) * (1 - appear(t, M[1] - 0.1, 0.3))
        if kk > 0: text(d, (gx(u) - 30, gy(i) - 60), "10", 42, GREEN, alpha=kk)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3); y = 330
    if a1 > 0:
        card(d, (40, y, 1040, y + 470), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Điện trở này: U tăng thì R tăng”"
        ks = clamp((t - 2.6) / 0.4); f = F(48); lw = tw(d, q, f); yy = y + 190
        text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 330), "U/I vẫn 10 Ω ở cả 5 hàng", 46, GREEN, alpha=a1 * appear(t, 3.0, 0.4))
    if k3 > 0:
        card(d, (40, y, 1040, y + 470), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        for j, s in enumerate(("• Đổi linh kiện khác, còn thẳng?", "• Quá 5,0 V thì sao?")):
            kk = k3 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (100, y + 220 + 120 * j), s, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: doi R thanh 20 Ohm, van 5,0 V (so voi lan 10 Ohm); goi y tre 2,6 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 420, "Điện trở: đường I–U thẳng, qua gốc", 50, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 870, "Thay điện trở 20 Ω, vẫn đặt 5,0 V.\nAmpe kế chỉ bao nhiêu?\nSo với lần dùng 10 Ω?", 48, INK,
          maxw=900, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1100, 970, 1360), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1160, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1270, "R gấp đôi, U giữ 5,0 V", 48, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + ts, "tap") for ts in TS]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.6, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l11-dien-tro-ohm-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện trở · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đo U và I của điện trở", draw=s_hook, tail=0.3, caps=[
   ("Ampe kế đo dòng I, vôn kế đo U.", 3.6),
   ("Nghĩ trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Tăng U từng 1,0 V, ghi dòng I.", 3.6),
   ("Mỗi lần đo, chấm một điểm.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Năm điểm thẳng hàng, qua gốc.", 3.4),
   ("U gấp mấy, I gấp bấy nhiêu.", 3.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 3.6),
   ("Hai câu còn bỏ ngỏ.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 7.4)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
