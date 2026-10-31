# Clip: tn-l10-do-g-02 - Do g bang do thi s theo t^2 tu nam do cao (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-g-02.json:
#   so_lieu_mau: s = 0,2..0,6 m -> t (TB 5 lan) = 0,204 / 0,249 / 0,288 / 0,321 / 0,352 s,
#                t^2 = 0,0416 / 0,0620 / 0,0829 / 0,1030 / 0,1239 s^2.
#   rut_ra: do doc (hai diem xa) = 0,400 / 0,0823 = 4,86 m/s^2 ; g = 2 . do doc = 9,72 m/s^2.
#   ket_qua_ky_vong: nam diem lech duong thang duoi 0,004 m (duong qua O, k = 4,86: lech lon nhat 0,0029 m).
#   mo_hinh: t = sqrt(2s/g_that) + tre_ht (g_that = 9,8, tre 0,002 s) -> bi roi trong clip theo g_that,
#            dong ho dung o dung so t cua bang (luc che tia).
#   Cau chot dung s_max = 1,0 m (bien tren tham_so): t^2 = 1,0 / 4,86 = 0,206 s^2, chua tung hien.
# Truc chinh: do thi s - t^2 THANG qua goc -> do doc = g/2 (khac roitudo2: nhieu anh chong theo moc 0,1 s).
# Mau (moi dai luong mot mau): s = BLUE, t^2 = ORANGE, do doc k + duong thang = GREEN, g = TEAL, diem do = NAVY,
#   tia sang = RED, khung du doan/chip cau hoi = PURPLE.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (5 lan tha, chieu cham 4 lan, bang + cham diem, chip cau hoi)
#       -> Dap an (ke duong thang qua O) -> Rut ra (tam giac do doc, g = 2k, chua noi duoc) -> Bay (quen nhan 2) -> Chot.
from engine import *

G_THAT = 9.8
ROWS = [(0.200, 0.204, 0.0416), (0.300, 0.249, 0.0620), (0.400, 0.288, 0.0829),
        (0.500, 0.321, 0.1030), (0.600, 0.352, 0.1239)]           # so_lieu_mau (s m, t s, t^2 s^2)
K = 4.86                                                              # do doc (rut_ra)
STEEL = (110, 120, 140); STEEL_L = (200, 205, 216); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
POST = (71, 85, 105); RED_D = (185, 28, 28); PURPLE_BG = (245, 243, 255)

def vn(x, nd):
    return f"{x:.{nd}f}".replace(".", ",")

def segs(d, x, y, parts, size, anchor="m", alpha=1.0, bold=True):
    """Chu nhieu mau tren mot dong. parts = [(chu, mau)]."""
    f = F(size, bold); tot = sum(tw(d, s, f) for s, _c in parts)
    xx = x - tot / 2 if anchor == "m" else x
    for s, c in parts:
        dtext(d, (xx, y), s, f, c, alpha, "lm"); xx += tw(d, s, f)
    return tot

# ---------------- dung cu (thuoc + nam cham + cong quang + dong ho) ----------------
SY0, SPX = 340, 720.0                       # y cua s = 0 (day bi luc con o nam cham) ; px / m
def SYp(s): return SY0 + SPX * s
BX, BR = 185, 16                            # tam bi (x), ban kinh
def rig(d, gate_s, ball_s, clock, hook=False, ball_a=1.0):
    card(d, (40, 265, 505, 830), fill=WHITE, outline=LIGHT, w=3)
    # thuoc
    d.rectangle([110, SY0 - 18, 140, SYp(0.6) + 18], fill=WOOD, outline=WOOD_D, width=3)
    for i in range(7):
        y = SYp(i / 10)
        d.line([(110, y), (136, y)], fill=INK, width=3)
        text(d, (102, y), "0" if i == 0 else vn(i / 10, 1), 38, INK, anchor="rm")
    text(d, (48, 300), "s (m)", 38, BLUE, anchor="lm")
    # nam cham dien
    d.rectangle([150, 272, 220, SY0 - 2 * BR], fill=NAVY)
    # cac vi tri cong quang con lai (chi o canh du doan)
    if hook:
        for s, *_r in ROWS[1:]:
            y = SYp(s)
            for x0 in range(140, 232, 18): d.line([(x0, y), (x0 + 10, y)], fill=GRAY, width=3)
    # cong quang: den phat (trai) + dau thu (phai), tia do giua
    yg = SYp(gate_s)
    d.line([(160, yg), (210, yg)], fill=RED, width=4)
    d.rectangle([136, yg - 18, 160, yg + 18], fill=POST)
    d.rectangle([210, yg - 18, 240, yg + 18], fill=POST)
    text(d, (250, yg), "cổng quang", 40, INK, anchor="lm")
    # bi (day bi o ball_s)
    if ball_s is not None and ball_a > 0.02:
        y = SYp(ball_s) - BR
        if y + BR < 822:
            d.ellipse([BX - BR, y - BR, BX + BR, y + BR], fill=A(STEEL, ball_a), outline=A(NAVY, ball_a), width=2)
            d.ellipse([BX - 8, y - 9, BX - 2, y - 3], fill=A(STEEL_L, ball_a))
    # dong ho
    text(d, (395, 305), "đồng hồ", 40, INK)
    card(d, (295, 330, 495, 400), fill=NAVY, r=16)
    text(d, (395, 365), vn(clock, 3) + " s", 44, YELLOW if clock > 0 else GRAY)
    if hook:                                                     # nhan nam cham co duong dan
        d.line([(222, 300), (300, 428)], fill=INK, width=3)
        text(d, (305, 440), "nam châm", 40, INK, anchor="lm")

# ---------------- do thi s theo t^2 (truc co dinh ca clip) ----------------
OX, OY, XS, YS = 180, 1500, 5143.0, 760.0      # goc ; px / s^2 ; px / m
def P(t2, s): return (OX + XS * t2, OY - YS * s)
def graph(d, n_pts=5, line_k=0.0, alpha=1.0, tri=0.0):
    c = lambda col: A(col, alpha)
    card(d, (40, 905, 1040, 1590), fill=c(WHITE), outline=c(LIGHT), w=3)
    arrow(d, (OX, OY), (965, OY), c(INK), w=4, head=18)
    arrow(d, (OX, OY), (OX, 940), c(INK), w=4, head=18)
    for i in range(1, 8):                                       # t^2: 0,02 .. 0,14
        x = OX + XS * i * 0.02
        d.line([(x, OY - 10), (x, OY + 10)], fill=c(INK), width=3)
        if i % 2 == 0: text(d, (x, OY + 38), vn(i * 0.02, 2), 38, INK, alpha=alpha)
    for i in range(1, 8):                                       # s: 0,1 .. 0,7
        y = OY - YS * i * 0.1
        d.line([(OX - 10, y), (OX + 10, y)], fill=c(INK), width=3)
        text(d, (OX - 18, y), vn(i * 0.1, 1), 36, INK, anchor="rm", alpha=alpha)
    text(d, (OX - 18, OY + 38), "O", 36, INK, anchor="rm", alpha=alpha)
    text(d, (OX + 22, 945), "s (m)", 38, BLUE, anchor="lm", alpha=alpha)
    text(d, (1020, 1452), "t² (s²)", 38, ORANGE, anchor="rm", alpha=alpha)
    if line_k > 0:
        t2e = 0.14 * line_k
        d.line([P(0, 0), P(t2e, K * t2e)], fill=c(GREEN), width=6)
    if tri > 0:                                                 # tam giac do doc: diem 1 -> diem 5
        a, b = P(ROWS[0][2], ROWS[0][0]), P(ROWS[4][2], ROWS[4][0])
        for x0 in range(int(a[0]), int(b[0]), 22):
            d.line([(x0, a[1]), (min(x0 + 12, b[0]), a[1])], fill=A(ORANGE, alpha * tri), width=4)
        for y0 in range(int(a[1]), int(b[1]), -22):
            d.line([(b[0], y0), (b[0], max(y0 - 12, b[1]))], fill=A(BLUE, alpha * tri), width=4)
        segs(d, (a[0] + b[0]) / 2, a[1] + 44, [("Δ(t²) = 0,0823 s²", ORANGE)], 38, alpha=alpha * tri)
        text(d, (b[0] + 18, 1175), "Δs =", 38, BLUE, anchor="lm", alpha=alpha * tri)
        text(d, (b[0] + 18, 1225), "0,400 m", 38, BLUE, anchor="lm", alpha=alpha * tri)
    for i in range(n_pts):
        x, y = P(ROWS[i][2], ROWS[i][0])
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=c(NAVY), outline=c(WHITE), width=3)

def chip(d, s, x0, x1, y=870, col=PURPLE, bg=PURPLE_BG, tc=None, alpha=1.0):
    card(d, (x0, y - 30, x1, y + 30), fill=A(bg, alpha), outline=A(col, alpha), r=30, w=3)
    text(d, ((x0 + x1) / 2, y), s, 36, tc or col, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0.2, 0.0, 0.0, hook=True)
    card(d, (515, 265, 1040, 830), fill=WHITE, outline=LIGHT, w=3)
    segs(d, 545, 330, [("s", BLUE), (": quãng rơi (m)", INK)], 40, anchor="l")
    segs(d, 545, 400, [("t", INK), (": thời gian rơi (s)", INK)], 40, anchor="l")
    text(d, (545, 520), "Thả ở 5 độ cao:", 40, INK, anchor="lm")
    text(d, (545, 600), "0,2; 0,3; 0,4;", 44, BLUE, anchor="lm")
    text(d, (545, 670), "0,5; 0,6 m", 44, BLUE, anchor="lm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 870 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 700), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 61), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    segs(d, W / 2, y0 + 200, [("Chấm 5 điểm (", INK), ("t²", ORANGE), (", ", INK), ("s", BLUE), (")", INK)], 52, alpha=a)
    segs(d, W / 2, y0 + 285, [("lên đồ thị ", INK), ("s", BLUE), (" theo ", INK), ("t²", ORANGE), (".", INK)], 52, alpha=a)
    ctext(d, y0 + 420, "Năm điểm nằm thế nào?", 52, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 580, 940, y0 + 594], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 580, 140 + 800 * (1 - p), y0 + 594], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (5 lan tha, chieu cham 4 lan) ----------------
SLOW, MOVE, PAUSE, HOLD, RUN0 = 4.0, 0.3, 0.12, 0.42, 0.5
def t_fall(i): return math.sqrt(2 * ROWS[i][0] / G_THAT)          # = t bang - tre 0,002 s (mo_hinh)
def schedule():
    out = []; s = RUN0
    for i in range(5):
        mv = 0.0 if i == 0 else MOVE
        f0 = s + mv + PAUSE                                          # luc ngat nam cham
        out.append((s, mv, f0, f0 + t_fall(i) * SLOW)); s = f0 + t_fall(i) * SLOW + HOLD
    return out
SCHED = schedule()

def run_state(t):
    """-> (s cong quang, s day bi | None, alpha bi, so dong ho, so hang xong, luot j)."""
    j = 0
    for i, (s0, *_r) in enumerate(SCHED):
        if t >= s0: j = i
    s0, mv, f0, f1 = SCHED[j]
    prev = ROWS[j - 1][0] if j > 0 else ROWS[0][0]
    gate = lerp(prev, ROWS[j][0], ease((t - s0) / mv)) if mv > 0 else ROWS[j][0]
    if t < f0:                                                   # bi moi o nam cham; dong ho giu so lan truoc toi luc tha
        return gate, 0.0, 1.0, (ROWS[j - 1][1] if j > 0 else 0.0), j, j
    tau = (t - f0) / SLOW
    if t < f1:
        return gate, 0.5 * G_THAT * tau * tau, 1.0, round(tau * 1000) / 1000, j, j
    a = 1 - clamp((t - f1) / 0.3)                                # qua cong roi mo di
    return gate, 0.5 * G_THAT * tau * tau, a, ROWS[j][1], j + 1, j

def s_do(img, d, t, sc):
    gate, bs, ba, clock, done, j = run_state(t)
    rig(d, gate, bs, clock, ball_a=ba)
    card(d, (515, 265, 1040, 830), fill=WHITE, outline=LIGHT, w=3)
    XC = (600, 780, 955)
    text(d, (XC[0], 312), "s (m)", 40, BLUE)
    text(d, (XC[1], 312), "t (s)", 40, INK)
    text(d, (XC[2], 312), "t² (s²)", 40, ORANGE)
    d.line([(535, 345), (1020, 345)], fill=LIGHT, width=3)
    for i, (s, tt, t2) in enumerate(ROWS):
        yy = 400 + i * 80
        if i == j and done <= i:
            d.rounded_rectangle([530, yy - 34, 1025, yy + 34], radius=16, fill=(255, 247, 237))
        if i < done:
            text(d, (XC[0], yy), vn(s, 3), 42, BLUE)
            text(d, (XC[1], yy), vn(tt, 3), 42, INK)
            text(d, (XC[2], yy), vn(t2, 4), 42, ORANGE)
    chip(d, "Câu hỏi: 5 điểm nằm thế nào?", 45, 640)
    chip(d, "chiếu chậm 4 lần", 670, 1035, col=NAVY, bg=NAVY, tc=YELLOW)
    graph(d, n_pts=done)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · thẳng, qua gốc O"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 318), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 284), lb, 40, WHITE, alpha=ka)
    k1 = appear(t, M[0] + 1.0, 0.5)
    card(d, (40, 400, 1040, 640), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
    segs(d, W / 2, 520, [("s", BLUE), (" tỉ lệ thuận với ", GREEN), ("t²", ORANGE)], 56, alpha=k1)
    graph(d, line_k=ease((t - 0.5) / 1.2))

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 870), fill=WHITE, outline=LIGHT, w=3)
    segs(d, W / 2, 320, [("Độ dốc ", INK), ("k", GREEN), (" = ", INK), ("Δs", BLUE), (" / ", INK), ("Δ(t²)", ORANGE)], 46)
    segs(d, W / 2, 395, [("k", GREEN), (" = ", INK), ("0,400 m", BLUE), (" / ", INK), ("0,0823 s²", ORANGE)], 46,
         alpha=appear(t, M[0] + 0.9, 0.5))
    segs(d, W / 2, 470, [("k ≈ 4,86 m/s²", GREEN)], 50, alpha=appear(t, M[0] + 1.8, 0.5))
    k2 = appear(t, M[1] - 0.1, 0.5)
    if k2 > 0:
        d.line([(90, 520), (990, 520)], fill=A(LIGHT, k2), width=3)
        segs(d, W / 2, 575, [("Đường qua O: ", INK), ("s", BLUE), (" = ", INK), ("k", GREEN), (" · ", INK), ("t²", ORANGE)], 46, alpha=k2)
        segs(d, W / 2, 655, [("s", BLUE), (" = ", INK), ("(g/2)", GREEN), (" · ", INK), ("t²", ORANGE),
                             ("  →  ", INK), ("k", GREEN), (" = ", INK), ("g/2", GREEN)], 46, alpha=appear(t, M[1] + 0.8, 0.5))
        segs(d, W / 2, 735, [("g", TEAL), (" = 2 × ", INK), ("4,86 m/s²", GREEN)], 46, alpha=appear(t, M[1] + 1.6, 0.5))
        segs(d, W / 2, 815, [("g ≈ 9,72 m/s²", TEAL)], 52, alpha=appear(t, M[1] + 2.4, 0.5))
    kc = appear(t, M[2] - 0.1, 0.45)
    graph(d, line_k=1.0, tri=appear(t, 0.5, 0.6), alpha=1 - kc)
    if kc > 0:
        y0 = 905 + (1 - kc) * 30
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, kc), outline=A(NAVY, kc), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=kc)
        kk = kc * appear(t, M[2] + 0.3, 0.4)
        card(d, (80, y0 + 150, 1000, y0 + 520), fill=A(WHITE, kk), outline=A(RED_D, kk), r=24, w=4)
        text(d, (W / 2, y0 + 270), "Bi khác có cho cùng g?", 48, RED_D, alpha=kk)
        text(d, (W / 2, y0 + 400), "mới thử một viên bi", 44, RED_D, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    card(d, (40, 265, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    f = F(60); parts = [("s", BLUE), (" = ", INK), ("(g/2)", TEAL), (" · ", INK), ("t²", ORANGE)]
    tot = segs(d, W / 2, 370, parts, 60)
    x0 = W / 2 - tot / 2 + tw(d, "s = ", f); x1 = x0 + tw(d, "(g/2)", f)
    d.rounded_rectangle([x0 - 10, 325, x1 + 10, 415], radius=14, outline=GREEN, width=5)
    segs(d, (x0 + x1) / 2, 475, [("độ dốc ", GREEN), ("k", GREEN)], 40)
    a1 = appear(t, 0.2, 0.45); y0 = 600
    card(d, (40, y0, 1040, y0 + 960), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    q = "“g = độ dốc = 4,86 m/s²”"
    ks = clamp((t - 1.0) / 0.4); fq = F(52); lw = tw(d, q, fq); yy = y0 + 240
    text(d, (W / 2, yy), q, 52, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0:                                                   # khong gach ngang qua so: dan nhan SAI ben duoi
        pw2 = tw(d, "SAI", F(40)) + 48
        card(d, (W / 2 - pw2 / 2, yy + 62, W / 2 + pw2 / 2, yy + 126), fill=A(RED, ks * a1), r=32)
        text(d, (W / 2, yy + 94), "SAI", 40, WHITE, alpha=ks * a1)
    kk = a1 * appear(t, 1.5, 0.5)
    card(d, (90, y0 + 400, 990, y0 + 860), fill=A((236, 253, 243), kk), r=24)
    segs(d, W / 2, y0 + 520, [("Độ dốc ", GREEN), ("k", GREEN), (" chỉ là ", GREEN), ("g", TEAL), ("/2", GREEN)], 52, alpha=kk)
    segs(d, W / 2, y0 + 680, [("g", TEAL), (" = 2", INK), ("k", GREEN), (" ≈ 9,72 m/s²", TEAL)], 54, alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        ctext(d, 860, "Kéo dài đường thẳng tới s = 1,0 m.\nKhi đó t² khoảng bao nhiêu?", 46, INK, maxw=900,
              alpha=appear(t, M[0] + 0.4, 0.5))
        kh = appear(t, M[0] + 3.7, 0.5)
        if kh <= 0: return
        card(d, (110, 1080, 970, 1330), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=3)
        ctext(d, 1140, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1245, "Đáp số có đơn vị s²", 42, INK, alpha=kh)
    chot_hoi(d, t, sc, "s theo t²: đường thẳng qua O,\nđộ dốc bằng g/2", "", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for s0, mv, f0, f1 in SCHED: cs.append((do["t0"] + f1, "tap"))           # bi che tia, dong ho dung
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-do-g-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Thực hành đo gia tốc rơi tự do · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Năm độ cao, một đồ thị", draw=s_hook, tail=0.8, caps=[
   ("Thả bi ở năm độ cao.", 3.0),
   ("Dừng video, chọn câu trả lời.", 6.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Thả 5 lần ở mỗi độ cao.", 4.4),
   ("Lấy t trung bình, chấm điểm (t², s).", 4.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Đặt thước kẻ qua các điểm.", 3.6)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Lấy hai điểm cách xa nhau.", 3.2),
   ("So với công thức quãng đường rơi.", 3.9),
   ("Còn một điều chưa biết.", 3.6)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.5, caps=[
   ("Bước cuối hay bị quên.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.2, caps=[
   ("Dừng video, tự trả lời.", 5.4)]),
])
