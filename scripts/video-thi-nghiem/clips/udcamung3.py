# Clip: tn-l12-udcamung-03 - Nam cham roi trong ong nhua (doi chung) va ong dong cung co
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-udcamung-03.json (so_lieu_mau "minh hoa", tham_so):
#   ong dai 30 cm; nhua 0,25 · 0,24 · 0,26 s (TB 0,25; lech lon nhat 0,01); dong 1,8 · 2,1 · 1,9 s (TB 1,93 ≈ 1,9; lech 0,17 ≈ 0,2);
#   roi tu do t = can(2·0,30/9,8) = 0,247 ≈ 0,25 s; 1,9/0,25 ≈ 7,6 -> "gan 8 lan"; bam tay ±0,1 s (khong_chung_minh 3).
# Ban 2 (26/11/2026, viec 4 lo 32, cong --do-chu moi): canh hook / do / ans / bay / gioi / end nhu mau xoaychieu2.
#   Du doan (K10 khong ve nut; khung web A-D): tha nam cham vao ong dong -> roi the nao? -> cham han, van ra het
#     (hien_tuong_hay_sai #1 dinh vao thanh, #3 dung giua ong).
#   Bay: "dong hut nam cham nen roi cham" -> dua sat thanh dong dung yen: khong hut (khong_chung_minh 2).
#   Chot (khung web A-D, dap an KHONG hien): lat nam cham, cuc S o duoi -> van ≈ 1,9 s (dong Foucault doi chieu,
#     luc tu len nam cham van huong len). Ca suy dinh tinh tu ghi_chu so_lieu_mau.
# Vat li (Lenz): N quay xuong, roi xuong. Vong ong DUOI nam cham: tu thong huong xuong tang -> B cam ung huong len ->
#   nguoc kim dong ho nhin tu tren -> cung truoc (nua duoi elip) chay sang PHAI. Vong TREN: cung truoc sang TRAI.
#   Ca hai vong cho luc tu len nam cham HUONG LEN; gan roi deu nen luc tu gan bang trong luc.
# Toa do mp4 = 65 + 0,88.x; chu >= 56 px (ra >= 49 px).
from engine import *

COP = (184, 115, 51); COP_D = (120, 72, 30); PLA = (196, 202, 214); NOTE = (70, 75, 95)
DGREEN = (21, 128, 61); DARK_OR = (181, 71, 8)
TP = (0.25, 0.24, 0.26)          # ong nhua (s)
TC = (1.8, 2.1, 1.9)             # ong dong (s)
TX = (290, 790)                  # tam hai ong
YT, YB = 440, 900                # mieng / day ong (30 cm)
MW, MH = 76, 112                 # nam cham vien
Y0, YX, YR = YT - MH / 2 - 10, YB + MH / 2, 1040 - MH / 2 - 4
assert abs(sum(TP) / 3 - 0.25) < 1e-9 and max(abs(x - 0.25) for x in TP) <= 0.0100001
assert round(sum(TC) / 3, 1) == 1.9 and round(max(abs(x - sum(TC) / 3) for x in TC), 1) == 0.2
assert round(math.sqrt(2 * 0.30 / 9.8), 2) == 0.25 and round(1.9 / 0.25) == 8

def fs(x): return f"{x:.2f}".replace(".", ",")

def magnet(d, cx, cy, w=MW, h=MH, n_down=True, alpha=1.0, lab=True):
    top, bot = (BLUE, RED) if n_down else (RED, BLUE)
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy], fill=A(top, alpha))
    d.rectangle([cx - w / 2, cy, cx + w / 2, cy + h / 2], fill=A(bot, alpha))
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], outline=A(NAVY, alpha), width=3)
    if lab:
        a, b = ("S", "N") if n_down else ("N", "S")
        text(d, (cx, cy - h / 4), a, 56, WHITE, alpha=alpha); text(d, (cx, cy + h / 4), b, 56, WHITE, alpha=alpha)

def tube(d, cx, col, y0=YT, y1=YB, ro=62, ri=44, tint=0.22):
    d.rectangle([cx - ri, y0, cx + ri, y1], fill=A(col, tint))
    d.rectangle([cx - ro, y0, cx - ri, y1], fill=col); d.rectangle([cx + ri, y0, cx + ro, y1], fill=col)
    d.rectangle([cx - ro, y0, cx + ro, y1], outline=NAVY, width=3)

def tray(d, cx):
    d.polygon([(cx - 80, 1010), (cx + 80, 1010), (cx + 64, 1042), (cx - 64, 1042)], fill=LIGHT, outline=GRAY)

def mpos(i, tau, kind):
    """Tam nam cham sau khi tha lan i. Nhua: roi tu do (y ~ tau^2); dong: gan nhu deu."""
    T = (TP if kind == 0 else TC)[i]
    if tau < 0: return Y0
    if tau >= T: return min(YR, YX + (tau - T) * 600)
    u = tau / T
    return Y0 + (YX - Y0) * (u * u if kind == 0 else (u + 0.02 * math.sin(math.pi * u)))

def rig(d, ys, watch, n_dim=True):
    for j, (cx, col, nm) in enumerate(((TX[0], PLA, "ống nhựa"), (TX[1], COP, "ống đồng"))):
        text(d, (cx, 282), nm, 56, NAVY if j == 0 else COP_D)
        tray(d, cx)
        if ys[j] is not None: magnet(d, cx, ys[j])
        tube(d, cx, col)
        if watch is not None:
            d.rounded_rectangle([cx - 120, 1056, cx + 120, 1130], radius=14, fill=NAVY)
            text(d, (cx, 1093), watch[j] + " s", 56, (134, 239, 172))
    if n_dim:
        x = 540
        d.line([(x, YT), (x, 600)], fill=NOTE, width=3); d.line([(x, 760), (x, YB)], fill=NOTE, width=3)
        for y in (YT, YB): d.line([(x - 18, y), (x + 18, y)], fill=NOTE, width=3)
        text(d, (x, 640), "dài", 56, NOTE, bold=False); text(d, (x, 712), "30 cm", 56, NOTE)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, (Y0, Y0), None)
    M = sc["M"]; a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 1100 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 480), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 180), "Thả nam châm vào ống đồng.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Nó rơi thế nào?", 58, INK, alpha=a)
    tc, te = M[1] + 0.3, sc["T"] - 0.1
    p = clamp((t - tc) / (te - tc))
    d.rounded_rectangle([110, y0 + 340, 970, y0 + 450], radius=24, fill=A(LIGHT, a))
    if p < 1: d.rounded_rectangle([110, y0 + 340, 110 + 860 * (1 - p), y0 + 450], radius=24, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (3 lan, tha CUNG LUC o hai ong) ----------------
GAP = 0.55
def starts(sc):
    s = [sc["M"][0] + 0.6]
    for i in range(2): s.append(s[-1] + TC[i] + GAP)
    return s
def avg_at(sc): return starts(sc)[2] + TC[2] + 0.5

def state(t, sc):
    st = starts(sc); ys = [Y0, Y0]; watch = ["0,00", "0,00"]; nr = [0, 0]
    for i, s in enumerate(st):
        if t < s - 0.3: break
        if t < s:
            ys = [Y0, Y0]; watch = ["0,00", "0,00"]; break
        tau = t - s
        for k in (0, 1):
            T = (TP if k == 0 else TC)[i]
            ys[k] = mpos(i, tau, k); watch[k] = fs(min(tau, T))
            if tau >= T: nr[k] = i + 1
    return ys, watch, nr

COLX = (80, 560, 860)
def table(d, nr, extra, y0=1150):
    card(d, (40, y0, 1040, y0 + 440), fill=WHITE, outline=LIGHT, w=3)
    for x, s, anc in ((COLX[0], "Lần", "lm"), (COLX[1], "Nhựa (s)", "mm"), (COLX[2], "Đồng (s)", "mm")):
        text(d, (x, y0 + 42), s, 56, NOTE, bold=False, anchor=anc)
    d.line([(70, y0 + 80), (1010, y0 + 80)], fill=LIGHT, width=3)
    for i in range(3):
        y = y0 + 118 + 60 * i
        if nr[0] > i or nr[1] > i: text(d, (COLX[0] + 20, y), str(i + 1), 56, INK, anchor="lm")
        if nr[0] > i: text(d, (COLX[1], y), fs(TP[i]), 56, INK)
        if nr[1] > i: text(d, (COLX[2], y), f"{TC[i]:.1f}".replace(".", ","), 56, INK)
    if extra:
        d.line([(70, y0 + 290), (1010, y0 + 290)], fill=LIGHT, width=3)
        for j, (lab, a1, a2, col) in enumerate((("Trung bình", "0,25", "≈ 1,9", DGREEN), ("Lệch lớn nhất", "0,01", "≈ 0,2", DARK_OR))):
            y = y0 + 330 + 64 * j
            text(d, (COLX[0], y), lab, 56, col, anchor="lm")
            text(d, (COLX[1] + 20, y), a1, 56, col); text(d, (COLX[2], y), a2, 56, col)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    ys, watch, nr = state(t, sc)
    rig(d, ys, watch, n_dim=False)
    table(d, nr, t >= avg_at(sc))
    text(d, (540, 990), "minh hoạ", 56, NAVY)

# ---------------- canh 3: Dap an + co che ----------------
DY = 440                                     # dich hinh co che xuong duoi o so sanh
CX4 = 380
def ring(d, y, sgn, k, front):
    if k <= 0: return
    if not front: d.arc((CX4 - 100, y - 30, CX4 + 100, y + 30), 180, 360, fill=A(ORANGE, 0.45 * k), width=5); return
    d.arc((CX4 - 100, y - 30, CX4 + 100, y + 30), 0, 180, fill=A(ORANGE, k), width=9)
    arrow(d, (CX4 - 50 * sgn, y + 29), (CX4 + 50 * sgn, y + 29), A(ORANGE, k), w=10, head=30)

def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    s = "ĐÁP ÁN: chậm hẳn, vẫn ra hết"; pw = tw(d, s, F(56)) + 70          # hien ngay tu 0 s
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 340), fill=GREEN, r=39)
    text(d, (W / 2, 301), s, 56, WHITE)
    # so sanh thoi gian trung binh: thanh dai ti le
    card(d, (40, 370, 1040, 640), fill=WHITE, outline=LIGHT, w=3)
    g = appear(t, 0.2, 1.4)
    for j, (lab, v, col, vs) in enumerate((("nhựa", 0.25, PLA, "0,25 s"), ("đồng", 1.9, COP, "≈ 1,9 s"))):
        y = 445 + 120 * j
        text(d, (80, y), lab, 56, NOTE, anchor="lm")
        L = 560 * v / 1.9 * g
        d.rounded_rectangle([240, y - 30, 240 + max(L, 8), y + 30], radius=14, fill=col)
        text(d, (260 + max(L, 8), y), vs, 56, INK, anchor="lm")
    # co che: dong Foucault quanh nam chan dang roi + luc len nam cham
    k = appear(t, M[1] - 0.1, 0.5)
    card(d, (40, 670, 1040, 1590), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    if k <= 0: return
    yb = 260 + DY + 360 + 20 * (t - M[1])
    for y in (yb - 150, yb + 150): ring(d, y, 0, k, False)
    tube(d, CX4, COP, 300 + DY, 1540, ro=64, ri=46, tint=0.18)
    magnet(d, CX4, yb, alpha=k)
    arrow(d, (CX4 + 112, yb - 40), (CX4 + 112, yb + 40), A(TEAL, k), w=6, head=18)
    text(d, (CX4 + 140, yb), "v", 56, TEAL, anchor="lm", alpha=k)
    for y, sgn in ((yb - 150, -1), (yb + 150, 1)): ring(d, y, sgn, k, True)
    text(d, (160, yb - 210), "dòng", 56, ORANGE, alpha=k); text(d, (160, yb - 145), "Foucault", 56, ORANGE, alpha=k)
    kf = appear(t, M[2] - 0.1, 0.5)
    card(d, (680, 760, 1010, 1540), fill=A((254, 242, 242), kf), r=24)
    if kf > 0:
        magnet(d, 845, 1150, 60, 96, alpha=kf, lab=False)
        arrow(d, (845, 1100), (845, 960), A(RED, kf), w=9, head=26)
        text(d, (845, 900), "lực từ", 56, RED, alpha=kf)
        arrow(d, (845, 1200), (845, 1350), A(NAVY, kf), w=9, head=26)
        text(d, (845, 1420), "trọng lực", 56, NAVY, alpha=kf)

# ---------------- canh 4: Bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    b1, b2, b3 = (m - 0.1 for m in sc["M"])
    k2, k3 = appear(t, b2, 0.4), appear(t, b3, 0.4)
    card(d, (40, 262, 1040, 620), outline=RED, w=5)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 282, W / 2 + pw / 2, 358), fill=RED, r=38)
    text(d, (W / 2, 320), "BẪY", 56, WHITE)
    ks = clamp((t - b3) / 0.4)
    for j, q in enumerate(("“Đồng hút nam châm", "nên nó rơi chậm”")):
        yy = 445 + 85 * j
        text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks))
        if ks > 0:
            lw = tw(d, q, F(60))
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=6)
    if k3 > 0:
        pw2 = tw(d, "SAI", F(56)) + 50
        card(d, (1020 - pw2, 282, 1020, 358), fill=A((127, 29, 29), k3), r=38)
        text(d, (1020 - pw2 / 2, 320), "SAI", 56, WHITE, alpha=k3)
    # thi nghiem: thanh dong dung yen + nam cham treo day dua sat dan (tu b2): day van thang dung
    card(d, (40, 650, 1040, 1380), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([200, 690, 880, 708], fill=GRAY)
    d.rectangle([640, 740, 720, 1340], fill=COP, outline=NAVY, width=3)
    text(d, (760, 1040), "thanh", 56, COP_D, anchor="lm"); text(d, (760, 1110), "đồng", 56, COP_D, anchor="lm")
    xm = 300 + (578 - 300) * ease(clamp((t - b2) / 1.6))
    d.line([(xm, 708), (xm, 980)], fill=NAVY, width=4)
    magnet(d, xm, 1036)
    if k3 > 0:
        card(d, (40, 1410, 1040, 1590), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1500), "Đứng yên: không có lực", 60, DGREEN, alpha=k3)

# ---------------- canh 5: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1100), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Độ lớn dòng Foucault?", "• Bấm tay: khó đo 0,25 s")):
        text(d, (100, 560 + j * 260), s, 66, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 700), "?", 200, NAVY, alpha=k * (1 - kb))

# ---------------- canh 6: THU NGHI (cau_chot cua khung; dap an KHONG hien) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.3, 0.5)
    card(d, (40, 260, 1040, 1180), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 285, W / 2 + pw / 2, 365), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 325), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 450), "Lật nam châm: S ở dưới.", 60, INK, alpha=k)
    text(d, (W / 2, 540), "Thả vào ống đồng: t = ? s", 60, DARK_OR, alpha=k)
    tube(d, 540, COP, 760, 1130, ro=62, ri=44, tint=0.18)
    yy = 668 + 8 * math.sin(2.2 * t)
    magnet(d, 540, yy, n_down=False, alpha=k)
    kh = appear(t, 3.3, 0.5)
    if kh > 0:
        card(d, (90, 1230, 990, 1380), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1305), "Gợi ý: Lenz chống gì?", 60, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, g, e = (sc[k] for k in ("hook", "do", "ans", "bay", "gioi", "end"))
    return ([(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tap") for s in starts(do)]
            + [(an["t0"] + 0.1, "ding"), (an["t0"] + an["M"][2] - 0.1, "tap"),
               (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
               (g["t0"] + 2.4, "tap"), (e["t0"] + 0.3, "open")])

CLIP = dict(id="tn-l12-udcamung-03", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
            footer="Ứng dụng cảm ứng điện từ · thachlab.id.vn", scenes=[
 dict(key="hook", title="Ống nhựa và ống đồng", draw=s_hook, tail=0.3, caps=[
   ("Hai ống cùng cỡ.", 3.0),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thả cùng lúc, bấm giờ.", 4.4),
   ("Lặp lại ba lần.", 4.0)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("Ống đồng chậm gần 8 lần.", 3.0),
   ("Từ thông qua ống đổi.", 3.0),
   ("Lực từ cản, hướng lên.", 3.0)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("Đưa sát thanh đồng.", 3.0),
   ("Đồng không hút nam châm.", 3.0)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Chưa trả lời được:", 4.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 6.6)]),
])
