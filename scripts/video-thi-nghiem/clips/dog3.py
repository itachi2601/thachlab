# Clip: tn-l10-do-g-03 - Dem khung hinh: sai so dung cu khi dung dien thoai quay cham (1/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-g-03.json:
#   cac_buoc: s = 0,500 m ; 240 khung/s -> n = 77 khung ; t = 77/240 ~ 0,321 s ; 1 khung = 1/240 ~ 0,0042 s > 0,001 s.
#   so_lieu_mau (s = 0,500 m): 30 khung/s -> n = 10, +-1 khung 0,0333 s ; 240 -> 77, 0,0042 ; 480 -> 154, 0,0021 ;
#                              120 -> 39, 0,0083 (chi dung lam CAU CHOT: 0,0083 va 120 chua tung hien).
#   mo_hinh: bi roi tu do, vi tri day bi o khung k (dem tu khung bi bat dau roi) s_k = g (k/fps)^2 / 2, g = 9,8.
#            Khung dau tien bi cham/qua moc 0,500 m: 240 -> 77 (s = 0,5045 ; khung 76: 0,4913), 30 -> 10 (khung 9: 0,441 ;
#            khung 10: 0,544), 480 -> 154 -> khop n trong bang (kiem bang ma o cuoi file khi chay truc tiep).
# Truc chinh: DAI KHUNG HINH + bo dem khung dong pha (khac dog2: bang + do thi s - t^2).
# Mau: s / thuoc = BLUE, so khung n = YELLOW tren nen NAVY, fps = ORANGE, t = INK, sai so dung cu = RED, dong ho = TEAL,
#      khung du doan = PURPLE.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (phat tung khung, dem 0..77) -> Ket qua (DAP AN, t = n/fps,
#       hai khung 76|77 phong to, thang sai so) -> Doi so khung/giay (30 khung/s, chua noi duoc) -> Bay (480) -> Chot.
from engine import *

G = 9.8
S_MOC = 0.500
N240, N30, N480 = 77, 10, 154
STEEL = (110, 120, 140); STEEL_L = (200, 205, 216); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
FILM = (38, 38, 46); RED_D = (185, 28, 28); PURPLE_BG = (245, 243, 255); GREEN_BG = (236, 253, 243)

def vn(x, nd):
    return f"{x:.{nd}f}".replace(".", ",")

def s_k(k, fps):
    """Vi tri day bi (m) o khung k, khung 0 = luc bi bat dau roi."""
    tt = k / fps
    return 0.5 * G * tt * tt

def segs(d, x, y, parts, size, anchor="m", alpha=1.0, bold=True):
    f = F(size, bold); tot = sum(tw(d, s, f) for s, _c in parts)
    xx = x - tot / 2 if anchor == "m" else x
    for s, c in parts:
        dtext(d, (xx, y), s, f, c, alpha, "lm"); xx += tw(d, s, f)
    return tot

def ball(d, x, ybot, r, alpha=1.0):
    y = ybot - r
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(STEEL, alpha), outline=A(NAVY, alpha), width=2)
    q = max(3, r // 3)
    d.ellipse([x - r // 2 - q // 2, y - r // 2 - q // 2, x - r // 2 + q, y - r // 2 + q], fill=A(STEEL_L, alpha))

# ---------------- dung cu (thuoc + nam cham + moc) ----------------
SY0, SPX = 345, 800.0                       # y cua s = 0 ; px / m
def SYp(s): return SY0 + SPX * s
BX = 215
def rig(d, k):
    card(d, (40, 265, 505, 830), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([120, SY0 - 14, 150, SYp(0.55) + 10], fill=WOOD, outline=WOOD_D, width=3)
    for i in range(6):
        y = SYp(i / 10)
        d.line([(120, y), (146, y)], fill=INK, width=3)
        text(d, (112, y), "0" if i == 0 else vn(i / 10, 1), 38, INK, anchor="rm")
    text(d, (52, 295), "s (m)", 38, BLUE, anchor="lm")
    d.rectangle([180, 270, 250, SY0 - 30], fill=NAVY)                       # nam cham
    ym = SYp(S_MOC)                                                         # moc 0,500 m
    for x0 in range(150, 300, 20): d.line([(x0, ym), (x0 + 12, ym)], fill=RED, width=4)
    text(d, (310, ym), "mốc", 40, RED, anchor="lm")
    ball(d, BX, SYp(min(s_k(k, 240), 0.56)), 15)
    d.line([(252, 300), (300, 330)], fill=INK, width=3)
    text(d, (305, 340), "nam châm", 38, INK, anchor="lm")

def phone(d, n, done=False, hook=False):
    card(d, (515, 265, 1040, 830), fill=WHITE, outline=LIGHT, w=3)
    text(d, (777, 315), "camera", 38, INK)
    segs(d, 777, 375, [("240", ORANGE), (" khung/s", ORANGE)], 44)
    if hook:
        card(d, (560, 450, 995, 610), fill=NAVY, r=18)
        text(d, (777, 495), "đồng hồ", 38, WHITE)
        text(d, (777, 560), "0,000 s", 48, TEAL)
        text(d, (777, 665), "độ chia 0,001 s", 40, TEAL)
        return
    text(d, (777, 465), "bộ đếm", 40, INK)
    card(d, (600, 500, 955, 650), fill=NAVY, r=18)
    segs(d, 777, 575, [("n = ", WHITE), (str(n), YELLOW)], 64)
    if done:
        text(d, (777, 720), "bi chạm mốc", 40, GREEN)
    else:
        text(d, (777, 720), "khung 0: bi bắt đầu rời", 40, MUTED)

# ---------------- dai khung hinh (phim) ----------------
TW, TGAP, TX0, TY0 = 176, 14, 70, 1000      # o khung: rong, khe, x dau, y dinh (s = 0 o TY0 + 20)
def strip(d, k, alpha=1.0):
    c = lambda col: A(col, alpha)
    card(d, (40, 880, 1040, 1520), fill=c(FILM), r=20)
    for x0 in range(60, 1030, 46):                                         # lo phim
        d.rounded_rectangle([x0, 896, x0 + 22, 912], radius=4, fill=c(BG))
        d.rounded_rectangle([x0, 1488, x0 + 22, 1504], radius=4, fill=c(BG))
    first = k - 4
    for j in range(5):
        kk = first + j
        x0 = TX0 + j * (TW + TGAP); x1 = x0 + TW
        if kk < 0:
            continue
        cur = (j == 4)
        d.rectangle([x0, TY0, x1, TY0 + 460], fill=c(WHITE), outline=c(YELLOW if cur else GRAY), width=5 if cur else 2)
        text(d, ((x0 + x1) / 2, 950), f"khung {kk}", 40, YELLOW if cur else WHITE, alpha=alpha)
        ys = lambda s: TY0 + 20 + SPX * s                                    # cung ti le 800 px/m voi thuoc lon
        d.rectangle([x0 + 12, TY0 + 10, x0 + 30, ys(0.55)], fill=c(WOOD))
        for i in range(6):
            d.line([(x0 + 12, ys(i / 10)), (x0 + 30, ys(i / 10))], fill=c(INK), width=2)
        d.line([(x0 + 34, ys(S_MOC)), (x1 - 6, ys(S_MOC))], fill=c(RED), width=3)
        ball(d, (x0 + x1) / 2 + 10, ys(min(s_k(kk, 240), 0.56)), 14, alpha)

# ---------------- hai khung lien tiep phong to (cung cua so 0,40-0,58 m) ----------------
ZS0, ZS1 = 0.40, 0.58
def zoom_pair(d, x0, y0, fps, k2, alpha=1.0, h=440, tw_=160, head=True):
    """Hai o khung k2-1 | k2 (nhan o tren), cua so s = 0,40..0,58 m (cao h px); ten fps o duoi. Tra ve ham y(s)."""
    c = lambda col: A(col, alpha)
    ys = lambda s: y0 + 50 + h * (s - ZS0) / (ZS1 - ZS0)
    if head:
        segs(d, x0 + 90 + tw_, y0 + h + 95, [(str(fps), ORANGE), (" khung/s", ORANGE)], 40, alpha=alpha)
    for i in range(4):                                                     # vach 0,40 .. 0,55
        s = 0.40 + 0.05 * i
        text(d, (x0 + 62, ys(s)), vn(s, 2), 36, INK, anchor="rm", alpha=alpha)
    for j, kk in enumerate((k2 - 1, k2)):
        bx0 = x0 + 75 + j * (tw_ + 30); bx1 = bx0 + tw_
        d.rectangle([bx0, y0 + 50, bx1, y0 + 50 + h], fill=c(WHITE), outline=c(GRAY), width=3)
        d.rectangle([bx0 + 6, y0 + 50, bx0 + 22, y0 + 50 + h], fill=c(WOOD))
        for i in range(4):
            d.line([(bx0 + 6, ys(0.40 + 0.05 * i)), (bx0 + 26, ys(0.40 + 0.05 * i))], fill=c(INK), width=2)
        d.line([(bx0 + 26, ys(S_MOC)), (bx1, ys(S_MOC))], fill=c(RED), width=4)
        ball(d, (bx0 + bx1) / 2 + 10, ys(s_k(kk, fps)), 14, alpha)
        text(d, ((bx0 + bx1) / 2, y0 + 20), f"khung {kk}", 40, INK, alpha=alpha)
    return ys

# ---------------- thang sai so dung cu (truc co dinh tu canh Ket qua) ----------------
BAR0, BSC = 390, 13000.0                     # x goc thanh ; px / s
ROWS = [("đồng hồ", 0.001, TEAL), ("240 khung/s", 0.0042, RED), ("30 khung/s", 0.0333, RED), ("480 khung/s", 0.0021, RED)]
def chart(d, shown, grow=None, hi=None, alpha=1.0, dim=()):
    """shown: so hang da hien; grow: (hang, 0..1) dang moc."""
    c = lambda col: A(col, alpha)
    card(d, (40, 1210, 1040, 1585), fill=c(WHITE), outline=c(LIGHT), w=3)
    text(d, (W / 2, 1255), "Sai số dụng cụ (s)", 40, INK, alpha=alpha)
    d.line([(BAR0, 1290), (BAR0, 1570)], fill=c(INK), width=3)
    slot = 0
    for i, (lb, v, col) in enumerate(ROWS):
        if i in dim: continue                                              # canh bay: chi giu dong ho + 480, xep sat nhau
        k = 1.0 if i < shown else (grow[1] if grow and grow[0] == i else 0.0)
        y = 1325 + slot * 70; slot += 1
        if k <= 0: continue
        if hi == i:
            d.rounded_rectangle([50, y - 30, 1030, y + 30], radius=14, fill=c((254, 242, 242)))
        text(d, (BAR0 - 18, y), lb, 38, INK, anchor="rm", alpha=alpha)
        L = BSC * v * ease(k)
        if L > 2:
            d.rectangle([BAR0, y - 18, BAR0 + L, y + 18], fill=c(col))
        if k >= 1:
            text(d, (BAR0 + L + 16, y), vn(v, 3 if v == 0.001 else 4) + " s", 38, col, anchor="lm", alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0)
    phone(d, 0, hook=True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 690), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 61), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    card(d, (110, y0 + 125, 470, y0 + 345), fill=A(FILM, a), r=14)          # hai o phim nho: "khung" la gi
    for j, kk in enumerate((40, 41)):
        bx0 = 135 + j * 170; bx1 = bx0 + 140
        d.rectangle([bx0, y0 + 145, bx1, y0 + 325], fill=A(WHITE, a))
        d.rectangle([bx0 + 8, y0 + 150, bx0 + 22, y0 + 320], fill=A(WOOD, a))
        ball(d, (bx0 + bx1) / 2 + 8, y0 + 165 + 300 * s_k(kk, 240), 12, a)
    text(d, (745, y0 + 200), "khung =", 44, INK, alpha=a)
    text(d, (745, y0 + 265), "một ảnh của video", 44, INK, alpha=a)
    segs(d, W / 2, y0 + 425, [("240 khung/s", ORANGE), (": thời gian giữa", INK)], 48, alpha=a)
    segs(d, W / 2, y0 + 495, [("2 khung so với ", INK), ("0,001 s", TEAL), ("?", INK)], 48, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 590, 940, y0 + 604], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 590, 140 + 800 * (1 - p), y0 + 604], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (phat tung khung, dem 0..77) ----------------
P0 = 0.6
def p1(sc): return sc["M"][1] - 0.05            # khung 77 hien dung luc phu de "Khung 77" len
def frame_k(t, sc):
    """So khung dang chieu: 0..77, cham dan ve cuoi de dem kip. Moi thu (bi, bo dem, dai phim) doc tu day."""
    if t < P0: return 0
    p = clamp((t - P0) / (p1(sc) - P0))
    if p >= 1: return N240
    return min(N240 - 1, int(N240 * (1 - (1 - p) ** 2)))

def s_do(img, d, t, sc):
    k = frame_k(t, sc)
    rig(d, k)
    phone(d, k, done=(k == N240))
    strip(d, k)

# ---------------- canh 3: Ket qua ----------------
def s_kq(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · lớn hơn 0,001 s"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 318), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 284), lb, 40, WHITE, alpha=ka)
    card(d, (40, 345, 1040, 610), fill=WHITE, outline=LIGHT, w=3)
    k1 = appear(t, M[0] + 0.3, 0.5)
    segs(d, W / 2, 405, [("t", INK), (" = ", INK), ("n", NAVY), (" / ", INK), ("fps", ORANGE)], 52, alpha=k1)
    segs(d, W / 2, 470, [("n", NAVY), (": số khung · ", MUTED), ("fps", ORANGE), (": khung mỗi giây", MUTED)], 40, alpha=k1)
    segs(d, W / 2, 555, [("t", INK), (" = ", INK), ("77", NAVY), (" / ", INK), ("240", ORANGE), (" ≈ 0,321 s", INK)], 52,
         alpha=appear(t, M[0] + 1.7, 0.5))
    kz = appear(t, M[1] - 0.1, 0.5)
    if kz > 0:
        card(d, (40, 635, 1040, 1185), fill=A(WHITE, kz), outline=A(LIGHT, kz), w=3)
        zoom_pair(d, 50, 640, 240, N240, alpha=kz, head=False)
        k2 = appear(t, M[1] + 0.9, 0.5)
        text(d, (765, 760), "t lệch tới", 40, INK, alpha=k2)
        segs(d, 765, 825, [("1 khung = 1/fps", RED)], 44, alpha=k2)
        k3 = appear(t, M[1] + 2.0, 0.5)
        d.line([(590, 880), (940, 880)], fill=A(LIGHT, k3), width=3)
        segs(d, 765, 945, [("= 1/", RED), ("240", ORANGE), (" s", RED)], 44, alpha=k3)
        text(d, (765, 1030), "≈ 0,0042 s", 52, RED, alpha=k3)
    kc = appear(t, M[2] - 0.1, 0.5)
    if kc > 0:
        chart(d, 1, grow=(1, clamp((t - M[2] - 0.8) / 0.6)), alpha=kc)

# ---------------- canh 4: Doi so khung/giay ----------------
def s_fps(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1185), fill=WHITE, outline=LIGHT, w=3)
    zoom_pair(d, 50, 300, 240, N240)
    text(d, (290, 960), "1 khung ≈ 0,0042 s", 38, RED)
    k2 = appear(t, 0.3, 0.5)
    zoom_pair(d, 545, 300, 30, N30, alpha=k2)
    d.line([(525, 300), (525, 1000)], fill=A(LIGHT, k2), width=3)
    k3 = appear(t, M[0] + 1.4, 0.5)
    text(d, (785, 960), "1 khung ≈ 0,0333 s", 38, RED, alpha=k3)
    chart(d, 2, grow=(2, clamp((t - M[0] - 2.0) / 0.7)), hi=2 if t > M[0] + 2.0 else None)
    kc = appear(t, M[1] - 0.1, 0.45)
    if kc > 0:
        y0 = 290 + (1 - kc) * 30
        card(d, (28, y0 - 10, 1052, y0 + 620), fill=A(WHITE, kc), outline=A(NAVY, kc), w=6)
        text(d, (W / 2, y0 + 90), "Chưa nói được", 46, NAVY, alpha=kc)
        kk = kc * appear(t, M[1] + 0.3, 0.4)
        card(d, (80, y0 + 190, 1000, y0 + 560), fill=A(WHITE, kk), outline=A(RED_D, kk), r=24, w=4)
        text(d, (W / 2, y0 + 340), "Bi chạm mốc lúc nào", 48, RED_D, alpha=kk)
        text(d, (W / 2, y0 + 410), "giữa khung 76 và 77?", 48, RED_D, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    a1 = appear(t, 0.2, 0.45)
    card(d, (40, 265, 1040, 1185), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 295, W / 2 + pw / 2, 359), fill=A(RED, a1), r=32)
    text(d, (W / 2, 327), "BẪY", 38, WHITE, alpha=a1)
    ks = clamp((t - 1.0) / 0.4)
    text(d, (W / 2, 500), "“480 khung/s: hết sai số”", 54, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0:
        pw2 = tw(d, "SAI", F(40)) + 48
        card(d, (W / 2 - pw2 / 2, 600, W / 2 + pw2 / 2, 664), fill=A(RED, ks), r=32)
        text(d, (W / 2, 632), "SAI", 40, WHITE, alpha=ks)
        card(d, (90, 720, 990, 1140), fill=A(GREEN_BG, ks), r=24)
        segs(d, W / 2, 830, [("1 khung ≈ ", RED), ("0,0021 s", RED)], 52, alpha=ks)
        segs(d, W / 2, 1000, [("vẫn lớn hơn ", INK), ("0,001 s", TEAL)], 50, alpha=ks)
    chart(d, 3, grow=(3, ks), hi=3 if ks > 0 else None, dim=(1, 2))

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        ctext(d, 880, "Lệch 1 khung ≈ 0,0083 s.\nĐiện thoại quay bao nhiêu khung/s?", 46, INK,
              maxw=900, alpha=appear(t, M[0] + 0.4, 0.5))
        kh = appear(t, M[0] + 2.9, 0.5)
        if kh <= 0: return
        card(d, (110, 1100, 970, 1350), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=3)
        ctext(d, 1160, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1265, "Nhìn lại cảnh Kết quả", 42, INK, alpha=kh)
    chot_hoi(d, t, sc, "Đếm khung:\nt lệch tới 1 khung.", "", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, b, e = sc["hook"], sc["do"], sc["kq"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + P0, "tap"), (do["t0"] + p1(do), "tap"),
            (kq["t0"] + 0.15, "ding"), (b["t0"] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-do-g-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Thực hành đo gia tốc rơi tự do · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đếm khung hình để đo t", draw=s_hook, tail=0.6, caps=[
   ("Quay chậm cảnh bi rơi 0,500 m.", 3.0),
   ("Dừng video, chọn câu trả lời.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Phát từng khung, bộ đếm tăng dần.", 4.6),
   ("Khung 77: bi chạm mốc.", 3.0)]),
 dict(key="kq", title="Kết quả", draw=s_kq, tail=0.4, caps=[
   ("Đổi số khung ra thời gian.", 3.3),
   ("Bi chạm mốc giữa hai khung.", 3.3),
   ("So với độ chia của đồng hồ.", 3.3)]),
 dict(key="fps", title="Đổi số khung mỗi giây", draw=s_fps, tail=0.4, caps=[
   ("Quay 30 khung/s thì sao?", 3.3),
   ("Còn một điều chưa biết.", 3.7)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("Quay thật chậm là hết sai số?", 4.7)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.9, caps=[
   ("Dừng video, tự trả lời.", 5.4)]),
])

if __name__ == "__main__":                      # tu kiem: n khop bang, bo dem dong pha voi bi/dai phim
    import copy
    for fps, n in ((30, N30), (240, N240), (480, N480)):
        kk = next(k for k in range(1000) if s_k(k, fps) >= S_MOC)
        print(fps, "khung/s: khung dau cham moc =", kk, "kho", n, "OK" if kk == n else "LECH")
    print("240: s76 =", round(s_k(76, 240), 4), " s77 =", round(s_k(77, 240), 4), " t =", round(77 / 240, 4))
    print("30 : s9 =", round(s_k(9, 30), 4), " s10 =", round(s_k(10, 30), 4))
    c = copy.deepcopy(CLIP); build(c); sc = {s["key"]: s for s in c["scenes"]}["do"]
    t = 0.0; prev = -1; bad = 0
    while t < sc["T"]:
        k = frame_k(t, sc)
        if k < prev: bad += 1
        if (k == N240) != (t >= p1(sc)): bad += 1
        prev = k; t += 0.05
    print("dem khung: don dieu & khung 77 dung luc phu de 2:", "OK" if bad == 0 else f"LOI {bad}",
          " p1 =", round(p1(sc), 2), " M =", [round(m, 2) for m in sc["M"]])
