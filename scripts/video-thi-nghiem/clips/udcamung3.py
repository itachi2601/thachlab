# Clip: tn-l12-udcamung-03 - Nam cham roi trong ong nhua (doi chung) va ong dong cung co (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-udcamung-03.json (so_lieu_mau "minh hoa", tham_so, mo_hinh):
#   ong dai 30 cm; nhua 0,25 · 0,24 · 0,26 s (TB 0,25; lech lon nhat 0,01); dong 1,8 · 2,1 · 1,9 s (TB ≈ 1,9; lech ≈ 0,2);
#   roi tu do t = can(2·0,30/9,8) ≈ 0,25 s; bam tay ±0,1 s (khong_chung_minh 3); "dong hut" chua loai (khong_chung_minh 2),
#   muon loai: dua nam cham sat thanh dong dung yen -> khong hut.
# Clip dat o bai 126 muc II.3, TRUOC Cau 3 (ranh xe) va Bay 3 (phanh dien tu): KHONG noi dien tro/ranh xe, KHONG noi
#   "luc ham yeu khi cham / toc do gioi han" -> chi noi luc tu huong len, can roi, nam cham van ra het ong.
# Vat li (Lenz): nam cham N quay xuong, roi xuong. Vong ong DUOI nam cham: tu thong huong xuong tang -> dong cam ung tao B
#   huong len -> nguoc chieu kim dong ho nhin tu tren -> cung truoc (gan nguoi xem, nua duoi elip) chay sang PHAI.
#   Vong ong TREN nam cham: tu thong huong xuong giam -> B cam ung huong xuong -> cung chieu kim dong ho -> cung truoc sang TRAI.
#   Ca hai vong cho luc tu len nam cham HUONG LEN; luc tu len ong huong xuong (dinh luat III).
#
# Hop Du doan (khung web, K10 khong ve nut). Cau: "Hai ong cung co. Trong ong dong, nam cham roi the nao?"
#   A. Roi nhanh, gan nhu trong ong nhua
#   B. Roi cham han nhung van ra het ong      <- dung (huy hieu: "ĐÁP ÁN · chậm hẳn, vẫn ra hết")
#   C. Bi hut dinh vao thanh ong, khong ra
#   D. Cham dan roi dung lo lung giua ong
# Cau chot THU NGHI (ca moi, khong co tren man): "So với lần cực N ở dưới: nhanh hơn, chậm hơn hay như cũ?" (hinh: nam
#   cham cuc S o duoi tren mieng ong dong) - lat nam cham cho cuc S quay xuong roi tha vao ong dong 30 cm.
#   Dap so: van khoang 1,9 s (cham nhu cu); dong Foucault doi chieu nhung luc tu len nam cham van huong len, can roi.
#   Goi y chi la du kien doi: "Đổi: cực S ở dưới".
from engine import *

COP = (184, 115, 51); COP_D = (120, 72, 30); PLA = (196, 202, 214); NOTE = (70, 75, 95)
TP = (0.25, 0.24, 0.26)          # ong nhua (s)
TC = (1.8, 2.1, 1.9)             # ong dong (s)
TX = (290, 790)                  # tam hai ong
YT, YB = 450, 930                # mieng / day ong (480 px = 30 cm)
MW, MH = 60, 96                  # nam cham vien
Y0, YX, YR = YT - MH / 2 - 10, YB + MH / 2, 1040 - MH / 2 - 4   # tam nam cham: luc tha, luc ra khoi day, nam trong khay
assert abs(sum(TP) / 3 - 0.25) < 1e-9 and max(abs(x - 0.25) for x in TP) <= 0.0100001
assert round(sum(TC) / 3, 1) == 1.9 and round(max(abs(x - sum(TC) / 3) for x in TC), 1) == 0.2
assert round(math.sqrt(2 * 0.30 / 9.8), 2) == 0.25

def fs(x): return f"{x:.2f}".replace(".", ",")

def magnet(d, cx, cy, w=MW, h=MH, n_down=True, alpha=1.0, lab=True):
    top, bot = (BLUE, RED) if n_down else (RED, BLUE)
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy], fill=A(top, alpha))
    d.rectangle([cx - w / 2, cy, cx + w / 2, cy + h / 2], fill=A(bot, alpha))
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], outline=A(NAVY, alpha), width=3)
    if lab:
        a, b = ("S", "N") if n_down else ("N", "S")
        text(d, (cx, cy - h / 4), a, 40, WHITE, alpha=alpha); text(d, (cx, cy + h / 4), b, 40, WHITE, alpha=alpha)

def tube(d, cx, col, y0=YT, y1=YB, ro=62, ri=42, tint=0.22):
    d.rectangle([cx - ri, y0, cx + ri, y1], fill=A(col, tint))
    d.rectangle([cx - ro, y0, cx - ri, y1], fill=col); d.rectangle([cx + ri, y0, cx + ro, y1], fill=col)
    d.rectangle([cx - ro, y0, cx + ro, y1], outline=NAVY, width=3)

def tray(d, cx):
    d.polygon([(cx - 80, 1010), (cx + 80, 1010), (cx + 64, 1042), (cx - 64, 1042)], fill=LIGHT, outline=GRAY)

def mpos(i, tau, kind):
    """Tam nam cham o thoi diem tau (s) sau khi tha lan i. Nhua: roi tu do (y ~ tau^2); dong: gan nhu deu."""
    T = (TP if kind == 0 else TC)[i]
    if tau < 0: return Y0
    if tau >= T: return min(YR, YX + (tau - T) * 600)
    u = tau / T
    return Y0 + (YX - Y0) * (u * u if kind == 0 else (u + 0.02 * math.sin(math.pi * u)))

def rig(d, ys, watch, n_dim=True, labels=True):
    """ys: tam y hai nam cham (None = an); watch: chuoi so chi hai dong ho (None = an dong ho)."""
    for j, (cx, col, nm) in enumerate(((TX[0], PLA, "ống nhựa"), (TX[1], COP, "ống đồng"))):
        if labels: text(d, (cx, 296), nm, 46, NAVY if j == 0 else COP_D)
        tray(d, cx)
        if ys[j] is not None: magnet(d, cx, ys[j])
        tube(d, cx, col)
        if watch is not None:
            d.rounded_rectangle([cx - 110, 1062, cx + 110, 1128], radius=14, fill=NAVY)
            text(d, (cx, 1095), watch[j] + " s", 44, (134, 239, 172))
    if n_dim:   # kich thuoc chung
        x = 540
        d.line([(x, YT), (x, 620)], fill=NOTE, width=3); d.line([(x, 740), (x, YB)], fill=NOTE, width=3)
        for y in (YT, YB): d.line([(x - 18, y), (x + 18, y)], fill=NOTE, width=3)
        text(d, (x, 660), "dài", 40, NOTE, bold=False); text(d, (x, 706), "30 cm", 42, NOTE)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, (Y0, Y0), None)
    a = appear(t, M[0] + 2.2, 0.5)
    if a <= 0: return
    y0 = 1070 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 190), "Trong ống đồng,", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "nam châm rơi thế nào?", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 400), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a * appear(t, M[0] + 2.8))
    tc, tend = M[0] + 2.9, sc["T"] - 0.15
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 452, 940, y0 + 466], radius=7, fill=A(LIGHT, a))
        if p < 1: d.rounded_rectangle([140, y0 + 452, 140 + 800 * (1 - p), y0 + 466], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (3 lan, tha CUNG LUC o hai ong) ----------------
GAP = 0.55
def starts(sc):
    s = [sc["M"][0] + 0.6]
    for i in range(2): s.append(s[-1] + TC[i] + GAP)
    return s
def avg_at(sc): return starts(sc)[2] + TC[2] + 0.5

def state(t, sc):
    """(ys, watch, so hang nhua, so hang dong) dong bo tu MOT ham: so dong ho = thoi gian da roi, dung o luc ra khoi day."""
    st = starts(sc); ys = [Y0, Y0]; watch = ["0,00", "0,00"]; nr = [0, 0]
    for i, s in enumerate(st):
        if t < s - 0.3:
            break
        if t < s:                         # dat lai nam cham len mieng ong (luc truoc nam trong khay)
            ys = [Y0, Y0]; watch = ["0,00", "0,00"]; break
        tau = t - s
        for k in (0, 1):
            T = (TP if k == 0 else TC)[i]
            ys[k] = mpos(i, tau, k); watch[k] = fs(min(tau, T))
            if tau >= T: nr[k] = i + 1
    return ys, watch, nr

COLX = (90, 560, 850)
def table(d, nr, n_extra, alpha=1.0, y0=1150):
    card(d, (40, y0, 1040, y0 + 445), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, s, anc in ((COLX[0], "Lần", "lm"), (COLX[1], "Nhựa (s)", "mm"), (COLX[2], "Đồng (s)", "mm")):
        text(d, (x, y0 + 40), s, 40, NOTE, bold=False, anchor=anc, alpha=alpha)
    d.line([(70, y0 + 70), (1010, y0 + 70)], fill=A(LIGHT, alpha), width=3)
    for i in range(3):
        y = y0 + 104 + 56 * i
        if nr[0] > i or nr[1] > i: text(d, (COLX[0], y), str(i + 1), 42, INK, anchor="lm", alpha=alpha)
        if nr[0] > i: text(d, (COLX[1], y), f"{TP[i]:.2f}".replace(".", ","), 42, INK, alpha=alpha)
        if nr[1] > i: text(d, (COLX[2], y), f"{TC[i]:.1f}".replace(".", ","), 42, INK, alpha=alpha)
    rows = (("Trung bình", "0,25", "≈ 1,9", GREEN), ("Lệch lớn nhất", "0,01", "≈ 0,2", ORANGE))
    for j, (lab, a1, a2, col) in enumerate(rows[:n_extra]):
        y = y0 + 290 + 60 * j
        if j == 0: d.line([(70, y - 32), (1010, y - 32)], fill=A(LIGHT, alpha), width=3)
        text(d, (COLX[0], y), lab, 40, col, anchor="lm", alpha=alpha)
        text(d, (COLX[1], y), a1, 44, col, alpha=alpha); text(d, (COLX[2], y), a2, 44, col, alpha=alpha)
    text(d, (1010, y0 + 412), "minh hoạ", 40, NOTE, bold=False, anchor="rm", alpha=alpha)

def s_do(img, d, t, sc):
    ys, watch, nr = state(t, sc)
    rig(d, ys, watch, n_dim=False)
    av = avg_at(sc)
    table(d, nr, (1 if t >= av else 0) + (1 if t >= av + 0.7 else 0))

# ---------------- canh 3: Dap an + kiem ong nhua + chua noi duoc ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    rig(d, (YR, YR), (fs(TP[2]), fs(TC[2])), n_dim=False, labels=False)
    ka = appear(t, 0.3, 0.4)
    s = "ĐÁP ÁN · chậm hẳn, vẫn ra hết"
    pw = tw(d, s, F(40)) + 56
    card(d, (W / 2 - pw / 2, 1150, W / 2 + pw / 2, 1216), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 1183), s, 40, WHITE, alpha=ka)
    k1 = appear(t, M[0] + 0.6, 0.45)
    card(d, (40, 1240, 1040, 1405), fill=A(WHITE, k1), outline=A(BLUE, k1), w=4)
    text(d, (W / 2, 1290), "Rơi tự do 30 cm: √(2h/g) ≈ 0,25 s", 44, BLUE, alpha=k1)
    # bo 14/11 (cong B: canh day)     text(d, (W / 2, 1360), "Cỡ ống không làm chậm", 44, INK, alpha=appear(t, M[0] + 1.4, 0.45))
    k2 = appear(t, M[0] + 2.4, 0.45)
    card(d, (40, 1425, 1040, 1590), fill=A((245, 243, 255), k2), outline=A(PURPLE, k2), w=4)
    text(d, (W / 2, 1472), "Chưa nói được", 42, PURPLE, alpha=k2)
    text(d, (W / 2, 1542), "Bấm tay ±0,1 s: chỉ so nhanh–chậm", 42, INK, alpha=k2)

# ---------------- canh 4: Co che: dong Foucault + luc tu len nam cham ----------------
CX4, CY4 = 420, 650
RY4 = (500, 800)                     # vong dong tren / duoi nam cham
def ring_back(d, y, k):
    if k > 0: d.arc((CX4 - 72, y - 22, CX4 + 72, y + 22), 180, 360, fill=A(ORANGE, 0.45 * k), width=5)
def ring_front(d, y, sgn, k):
    """Nua truoc vong dong (gan nguoi xem) + mui ten chieu dong: sgn=+1 sang phai."""
    if k <= 0: return
    d.arc((CX4 - 72, y - 22, CX4 + 72, y + 22), 0, 180, fill=A(ORANGE, k), width=7)
    arrow(d, (CX4 - 30 * sgn, y + 21), (CX4 + 30 * sgn, y + 21), A(ORANGE, k), w=7, head=20)

def s_coche(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    k0 = appear(t, M[0] + 0.2, 0.5)
    for y in RY4: ring_back(d, y, k0)                     # nua sau vong dong: ve truoc than ong
    tube(d, CX4, COP, 300, 980, ro=62, ri=42, tint=0.18)
    yb = CY4 + 6 * t                                        # nam cham dang roi (cham)
    magnet(d, CX4, yb)
    arrow(d, (CX4 + 100, yb - 34), (CX4 + 100, yb + 36), TEAL, w=6, head=18)   # v canh ong, xa vong duoi
    text(d, (CX4 + 126, yb), "v", 44, TEAL, anchor="lm")
    for y, sgn in zip(RY4, (-1, 1)):                        # tren: sang trai, duoi: sang phai (Lenz, xem dau file)
        ring_front(d, y, sgn, k0)
        text(d, (180, y - 22), "dòng", 40, ORANGE, alpha=k0); text(d, (180, y + 24), "Foucault", 40, ORANGE, alpha=k0)
    k1 = appear(t, M[1] + 0.2, 0.5)                         # luc len NAM CHAM (o rieng)
    card(d, (650, 300, 1010, 960), fill=A((254, 242, 242), k1), r=24)
    if k1 > 0:
        magnet(d, 830, 630, 50, 80, alpha=k1, lab=False)
        arrow(d, (830, 588), (830, 470), A(RED, k1), w=8, head=24)          # ngan hon trong luc: van roi nhanh dan
        text(d, (830, 435), "lực từ", 42, RED, alpha=k1)
        arrow(d, (830, 672), (830, 820), A(NAVY, k1), w=8, head=24)
        text(d, (830, 870), "trọng lực", 42, NAVY, alpha=k1)
    a = appear(t, M[0] + 0.4, 0.45)
    card(d, (40, 1030, 1040, 1260 + 330 * k1), fill=A(WHITE, a), outline=A(BLUE, a), w=4)
    text(d, (W / 2, 1110), "Từ thông qua thành ống thay đổi", 46, INK, alpha=a)
    text(d, (W / 2, 1200), "→ dòng Foucault", 46, ORANGE, alpha=appear(t, M[0] + 1.2, 0.45))
    text(d, (W / 2, 1360), "Lực từ lên nam châm: hướng lên", 46, RED, alpha=k1)
    text(d, (W / 2, 1490), "Lên ống: hướng xuống", 42, NOTE, alpha=appear(t, M[1] + 2.4, 0.45))

# ---------------- canh 5: Bay "dong hut nam cham" (+ chua noi duoc cua phep so voi ong nhua) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.05, 0.35)
    mk = M[0] + 2.6
    # hinh: thanh dong dung yen + nam cham treo day dat sat
    card(d, (40, 260, 1040, 860), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    d.rectangle([300, 300, 760, 318], fill=A(GRAY, k0))                       # gia treo
    d.rectangle([600, 360, 660, 840], fill=A(COP, k0), outline=A(NAVY, k0), width=3)   # thanh dong
    text(d, (690, 600), "thanh đồng", 42, COP_D, anchor="lm", alpha=k0)
    d.line([(540, 318), (540, 560)], fill=A(NAVY, k0), width=3)               # day treo thang dung
    magnet(d, 540, 608, 56, 96, alpha=k0)
    kc = appear(t, mk + 0.6, 0.45)                         # sau khi gach xong (mk + 0,4) >= 0,2 s
    if kc > 0:
        text(d, (330, 610), "không hút", 46, GREEN, alpha=kc)
    y = 890
    card(d, (40, y, 1040, y + 310 + 140 * kc), fill=A(WHITE, k0), outline=A(RED, k0), w=6)
    pw = tw(d, "BẪY", F(40)) + 52
    card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(RED, k0), r=32)
    text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=k0)
    q = "“Đồng hút nam châm nên rơi chậm”"
    ks = clamp((t - mk) / 0.4); f = F(46); lw = tw(d, q, f); yy = y + 160
    text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=k0)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * k0), width=5)
    if ks >= 1: text(d, (W / 2 - lw / 2 - 42, yy), "✗", 48, RED, alpha=k0)
    text(d, (W / 2, y + 250), "Ống nhựa chưa loại được ý này", 42, PURPLE, alpha=appear(t, 0.8, 0.4))
    if kc > 0:
        text(d, (W / 2, y + 380), "Lực hãm do dòng Foucault", 46, NAVY, alpha=kc)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    tube(d, 640, COP, 1040, 1240, ro=40, ri=27, tint=0.18)
    magnet(d, 640, 990, 40, 64, n_down=False, alpha=k, lab=False)
    text(d, (690, 970), "N", 40, RED, anchor="lm", alpha=k); text(d, (690, 1015), "S", 40, BLUE, anchor="lm", alpha=k)
    text(d, (440, 1140), "t = ?", 46, INK, alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Dòng Foucault hãm nam châm rơi",
             "Cực N ở dưới lần trước. Lần này trong ống đồng: nhanh hơn, chậm hơn hay như cũ?", None, body=_end_body)
    kh = appear(t, M[0] + 1.4, 0.5)
    if kh > 0:
        card(d, (110, 1320, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1368, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1460, "Đổi: cực S ở dưới", 44, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, co, b, e = sc["hook"], sc["do"], sc["dapan"], sc["coche"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][0] + 2.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tap") for s in starts(do)]
            + [(do["t0"] + avg_at(do), "ding"), (da["t0"] + 0.3, "ding"), (co["t0"] + co["M"][1] + 0.2, "tap"),
               (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-udcamung-03", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
            footer="Ứng dụng cảm ứng điện từ · thachlab.id.vn", scenes=[
 dict(key="hook", title="Ống nhựa và ống đồng", draw=s_hook, tail=0.3, caps=[
   ("Hai ống cùng cỡ.", 8.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thả cùng lúc, bấm giờ từng ống.", 5.0),
   ("Lặp lại ba lần.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Ống nhựa gần rơi tự do.", 6.4)]),
 dict(key="coche", title="Vì sao ống đồng hãm?", draw=s_coche, tail=0.4, caps=[
   ("Nam châm đang rơi.", 3.8),
   ("Lực nào cản?", 3.6)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.8, caps=[
   ("Thử thanh đồng đứng yên.", 5.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video và trả lời.", 6.8)]),
])
