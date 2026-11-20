# Clip: tn-l12-phanbach-02 - Chen tam bia vao ban ghim: mo hinh thanh dieu khien hap thu neutron (Bai 16, lesson 17)
# So lieu nguyen tu content/thi-nghiem/tn-l12-phanbach-02.json: luoi 7 x 7 = 49 ghim cach 2 cm (dung_cu, tham_so N0),
# che 0 / 30 / 60 % (tham_so p), so ghim do 36·34·37 / 12·10·11 / 4·5·3, k uoc luong 1,6 / 1,0 / 0,6 (so_lieu_mau),
# "che 30 %: 10-12 ghim" (cac_buoc.quan_sat). Mo hinh DINH TINH (mo_hinh.ghi_chu) - ghi tren man.
# Hinh: tam bia ve thanh dai che tron cot ghim (30 %: 2 cot = 14/49 ghim; 60 %: 4 cot = 28/49) -> ghi "≈ 30 %", "≈ 60 %".
# Day chuyen lan theo the he (ghim do lam do ghim ke ben, 4 huong), ghim duoi bia khong truyen. Mot lan tha moi muc
# duoc ve (36, 12, 4 = lan 1 trong bang); so the he do random co dinh hat giong, khong in so the he len man.
#
# Hop Du doan (cho JSON khung) - "Đặt tấm bìa che 30 % rồi 60 % lưới. Số ghim đổ thay đổi thế nào?"
#   A. Giảm theo đúng tỉ lệ phần bị che
#   B. Gần như không đổi cho tới khi che kín
#   C. Giảm mạnh, có mức che làm dây chuyền tắt sớm      <- ĐÁP ÁN
#   D. Tăng lên vì bi chỉ rơi vào phần còn hở
# Cau chot THU NGHI (vong 3): "Ghim cách 3 cm, che 30 %: lan, giữ hay tắt dần?" - goi y: "Nhớ bảng 3 cm ở thí nghiệm trước".
#   Dap so: tắt dần - 3 cm chưa che đã k ≈ 1 (bảng bàn ghim phanbach-01 trong bài: 9 · 8 · 10 ghim), che thêm làm k < 1.
#   Khong hoi "rut het thanh dieu khien" vi do la cau Nghi tiep ngay sau hop trong bai.
from engine import *
import random

COVER = {0: set(), 30: {1, 5}, 60: {1, 2, 4, 5}}            # cot bi bia che (0..6)
ROWS = [(0, "36 · 34 · 37", "1,6"), (30, "12 · 10 · 11", "1,0"), (60, "4 · 5 · 3", "0,6")]   # so_lieu_mau
SEED = {0: (1489, 36), 30: (14, 12), 60: (48, 4)}           # hat giong cho ra dung so ghim do lan 1
START = (3, 3); Q = 0.62; GEN = 0.26                         # ghim bi roi trung; xac suat do ghim ke; giay/the he

def _sim(cover, seed):
    R = random.Random(seed); fall = {START: (0, None)}; cur = [START]; g = 0
    while cur:
        nxt = []
        for (r, c) in cur:
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < 7 and 0 <= nc < 7 and nc not in cover and (nr, nc) not in fall and R.random() < Q:
                    fall[(nr, nc)] = (g + 1, (r, c)); nxt.append((nr, nc))
        cur = nxt; g += 1
    return fall

FALL = {}
for p, (s, n) in SEED.items():
    FALL[p] = _sim(COVER[p], s); assert len(FALL[p]) == n, (p, len(FALL[p]))
NGEN = {p: max(v[0] for v in f.values()) for p, f in FALL.items()}

# ---------------- ban ghim ----------------
PX0, PY0, SP = 140, 360, 92                  # ghim (0,0) va khoang cach 2 cm tren hinh
def P(r, c): return PX0 + c * SP, PY0 + r * SP
BOARD = (80, 300, 752, 972)
CARDB = (196, 160, 120)                      # mau bia

def n_fallen(p, tl):
    """so ghim da do o thoi diem tl (tinh tu luc bi cham ghim dau) - dung cho bo dem."""
    if tl < 0: return 0
    return sum(1 for g, _ in FALL[p].values() if tl >= g * GEN + 0.12)

def board(d, t, p, tl, cover_k=1.0, ball=True, show_fall=True):
    """p: muc che; tl: thoi gian tu luc bi cham (am = chua tha); cover_k: do truot vao cua bia (0..1)."""
    card(d, BOARD, fill=(244, 236, 220), outline=(214, 200, 176), r=24, w=4)
    fall = FALL[p] if show_fall else {}
    for r in range(7):
        for c in range(7):
            x, y = P(r, c)
            st = fall.get((r, c))
            k = 0.0 if (st is None or tl < 0) else clamp((tl - st[0] * GEN) / 0.22)
            if k <= 0:
                d.ellipse([x - 8, y + 4, x + 18, y + 16], fill=(214, 200, 176))     # bong
                dot(d, x, y, 14, NAVY); dot(d, x - 4, y - 4, 4, WHITE)
            else:
                pr = st[1]
                if pr is None: ang = math.radians(35)
                else:
                    px, py = P(*pr); ang = math.atan2(y - py, x - px)
                L = 44 * k; ex, ey = x + L * math.cos(ang), y + L * math.sin(ang)
                d.line([(x, y), (ex, ey)], fill=mix(NAVY, ORANGE, k), width=9)
                dot(d, ex, ey, 11, mix(NAVY, ORANGE, k))
    # tam bia: truot tu tren xuong che tron cot
    if cover_k > 0 and COVER[p]:
        y1 = BOARD[1] + 14 + (BOARD[3] - BOARD[1] - 28) * ease(cover_k)
        for c in COVER[p]:
            x, _ = P(0, c)
            d.rounded_rectangle([x - 36, BOARD[1] + 14, x + 36, y1], radius=10, fill=A(CARDB, 0.93),
                                outline=A((150, 118, 80), 1.0), width=4)
    # bi thep roi xuong ghim dau
    if ball and tl > -0.4:
        x, y = P(*START); q = clamp((tl + 0.4) / 0.4)
        rr = lerp(40, 20, q); yy = lerp(y - 120, y - 6, ease(q))
        dot(d, x + 22, yy, rr, (170, 176, 190), NAVY); dot(d, x + 16, yy - 6, rr * 0.3, WHITE)

def spacing_mark(d, a=1.0):
    x0, _ = P(0, 0); x1, _ = P(0, 1); y = BOARD[1] - 26
    d.line([(x0, y), (x1, y)], fill=A(MUTED, a), width=4)
    for x in (x0, x1): d.line([(x, y - 12), (x, y + 12)], fill=A(MUTED, a), width=4)
    text(d, (x1 + 16, y), "2 cm", 40, MUTED, anchor="lm", alpha=a)

def side(d, p_lbl, cnt, a=1.0, cnt_col=ORANGE):
    """cot ben phai: muc che + bo dem ghim do"""
    card(d, (780, 300, 1020, 560), fill=WHITE, outline=LIGHT, r=24, w=4)
    text(d, (900, 352), "Che", 42, MUTED, bold=False)
    text(d, (900, 460), p_lbl, 56, (150, 118, 80) if p_lbl != "0 %" else INK)
    card(d, (780, 590, 1020, 972), fill=WHITE, outline=LIGHT, r=24, w=4)
    text(d, (900, 642), "Đổ", 42, MUTED, bold=False)
    text(d, (900, 760), cnt, 84, cnt_col)
    text(d, (900, 880), "/ 49", 46, MUTED, bold=False)

# ---------------- canh 1: mo bai + du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    board(d, t, 0, -1, ball=False)
    spacing_mark(d, appear(t, 0.3))
    k = appear(t, M[1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1010, 1020, 1420), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1062), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1170, "Lấy bìa che 30 % rồi 60 % lưới.\nSố ghim đổ sẽ ra sao?", 46, INK, alpha=k)
    text(d, (W / 2, 1290), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=k * appear(t, M[1] + 0.2))
    t1, t2 = M[1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1356, 940, 1370], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1356, 140 + 800 * (1 - q), 1370], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tha bi o ba muc che ----------------
def do_plan(sc):
    """moc (giay trong canh): tha bi (cham ghim dau) va luc hang bang hien, cho tung muc che"""
    M = sc["M"]
    d0 = M[0] + 0.5
    d30 = M[1] + 0.7                      # bia truot vao trong 0,5 s truoc do
    d60 = d30 + NGEN[30] * GEN + 1.4
    plan = []
    for p, dt in ((0, d0), (30, d30), (60, d60)):
        plan.append((p, dt, dt + NGEN[p] * GEN + 0.45))
    return plan

def do_state(t, sc):
    plan = do_plan(sc); cur = plan[0]
    for pl in plan:
        if t >= pl[1] - 0.75: cur = pl
    return cur, plan

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    (p, dt, rt), plan = do_state(t, sc)
    ck = 1.0 if p == 0 else clamp((t - (dt - 0.75)) / 0.5)
    tl = t - dt
    board(d, t, p, tl, cover_k=ck)
    spacing_mark(d)
    if p:
        a = appear(t, dt - 0.75, 0.3)
        x0, _ = P(0, min(COVER[p])); x1, _ = P(0, max(COVER[p]))
        text(d, ((x0 + x1) / 2, BOARD[3] + 34), "bìa = vật hấp thụ", 40, (150, 118, 80), alpha=a)
    side(d, "0 %" if p == 0 else f"≈ {p} %", "···" if tl < 0 else str(n_fallen(p, tl)), cnt_col=MUTED if tl < 0 else ORANGE)
    # bang so lieu
    card(d, (60, 1040, 1020, 1600), fill=WHITE, outline=NAVY, w=4)
    xs = [190, 640]
    text(d, (xs[0], 1094), "Che", 42, MUTED); text(d, (xs[1], 1094), "Đổ (3 lần)", 42, MUTED)
    d.line([(90, 1130), (990, 1130)], fill=LIGHT, width=4)
    for i, (pp, three, _) in enumerate(ROWS):
        a = appear(t, plan[i][2], 0.35)
        if a <= 0: continue
        y = 1186 + i * 84
        if pp == p: d.rounded_rectangle([80, y - 36, 1000, y + 36], radius=14, fill=A((255, 237, 213), a))
        text(d, (xs[0], y), f"{pp} %", 46, BLUE, alpha=a)
        text(d, (xs[1], y), three, 46, INK, alpha=a)
    text(d, (W / 2, 1500), "Mô hình định tính, số minh hoạ", 44, PURPLE)

# ---------------- canh 3: dap an + k theo muc che ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = back((t - 0.2) / 0.5) if t > 0.2 else 0
    card(d, (60, 250, 1020, 400), fill=(220, 252, 231), outline=GREEN, w=5)
    ctext(d, 325, "ĐÁP ÁN · Giảm mạnh, có mức che tắt sớm", 46, GREEN, maxw=920, alpha=clamp(k))
    # cot k
    card(d, (60, 430, 1020, 1120), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 476), "k ước lượng", 42, MUTED)
    yb, s = 960, 250                                 # day cot, px moi don vi k
    d.line([(110, yb), (980, yb)], fill=NAVY, width=5)
    k1 = appear(t, M[0] + 0.2)
    for xx in range(110, 980, 30): d.line([(xx, yb - s), (xx + 16, yb - s)], fill=A(RED, k1), width=4)
    text(d, (975, yb - s - 30), "k = 1", 40, RED, anchor="rm", alpha=k1)
    lab = ["lan rộng", "giữ, không lan", "tắt dần"]
    for i, (pp, _, kv) in enumerate(ROWS):
        cx = 240 + i * 300; g = ease((t - 0.4 - 0.25 * i) / 0.6)
        text(d, (cx, yb + 40), f"che {pp} %", 40, MUTED, bold=False)
        if g <= 0: continue
        h = float(kv.replace(",", ".")) * s * g
        if h > 2: d.rectangle([cx - 60, yb - h, cx + 60, yb], fill=(BLUE, ORANGE, GRAY)[i])
        text(d, (cx, yb - h - 32), f"≈ {kv}", 44, INK, alpha=g)
        text(d, (cx, yb + 92), lab[i], 42, (BLUE, ORANGE, MUTED)[i], alpha=appear(t, M[1] - 0.2 + 0.3 * i))
    # co che: ban do mo hinh -> lo
    a = appear(t, M[1] + 0.3)
    if a <= 0: return
    card(d, (60, 1160, 1020, 1400), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    for j, (l, r) in enumerate((("ghim đổ", "neutron"), ("tấm bìa", "thanh điều khiển"))):
        aj = appear(t, M[1] + 0.3 + 0.5 * j); y = 1230 + j * 100
        text(d, (330, y), l, 46, ORANGE, anchor="rm", alpha=aj)
        text(d, (390, y), "↔", 46, MUTED, alpha=aj)
        text(d, (450, y), r, 46, BLUE, anchor="lm", alpha=aj)

# ---------------- canh 4: chua noi duoc gi ----------------
def s_lim(img, d, t, sc):
    IMG_REF[0] = img
    board(d, t, 60, 9, show_fall=True, ball=False)
    b = appear(t, 0.3)
    card(d, (60, 1030, 1020, 1560), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
    text(d, (W / 2, 1100), "Chưa nói được", 48, PURPLE, alpha=b)
    for j, s in enumerate(("• k thật của lò", "• vì sao bo hấp thụ tốt")):
        text(d, (150, 1240 + j * 110), s, 48, INK, anchor="lm", alpha=appear(t, 0.6 + 0.6 * j))

# ---------------- canh 5: bay ----------------
TRAP = [("Thanh điều khiển làm nguội lò", "hấp thụ neutron, giảm k"),
        ("Che ít: không ảnh hưởng", "che 30 %: còn 10–12 ghim"),
        ("Giảm công suất = tắt lò", "k < 1 mới tắt")]
def trap_t(i, sc):
    r0 = 0.3 + 2.0 * i
    return r0, r0 + 1.0, r0 + 1.3                   # hien cau sai, gach, hien cau dap
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    n = sum(1 for i in range(3) if t >= trap_t(i, sc)[0])
    if n == 0: return
    y1 = 300 + n * 300 + 20
    card(d, (60, 300, 1020, y1), fill=(254, 242, 242), outline=RED, r=28, w=4)
    for i in range(n):
        r0, rs, ra = trap_t(i, sc); y = 390 + i * 300
        a = appear(t, r0, 0.35)
        f = F(46); wdt = tw(d, TRAP[i][0], f)
        text(d, (W / 2, y), TRAP[i][0], 46, INK, alpha=a)
        ks = clamp((t - rs) / 0.35)
        if ks > 0:
            x0 = W / 2 - wdt / 2 - 10
            d.line([(x0, y + 6), (x0 + (wdt + 20) * ks, y + 6)], fill=RED, width=4)
            text(d, (W / 2 - wdt / 2 - 50, y), "✗", 50, RED, alpha=ks)
        kb = appear(t, ra, 0.35)
        if kb > 0:
            text(d, (W / 2, y + 100), "→ " + TRAP[i][1], 46, GREEN, alpha=kb)

# ---------------- canh 6: chot + thu nghi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    def rows(d, t, k):                               # hai hang ghim: 2 cm (da thu) va 3 cm (ca moi), khong ghi dap so
        ks = appear(t, M[0] + 0.8, 0.5) * k
        if ks <= 0: return
        for j, (sp, lb, col) in enumerate(((60, "2 cm", MUTED), (90, "3 cm ?", ORANGE))):
            y = 1010 + j * 110
            text(d, (150, y), lb, 44, col, anchor="lm", alpha=ks)
            for n in range(int(600 / sp) + 1):
                dot(d, 360 + n * sp, y, 13, A(NAVY, ks))
    chot_hoi(d, t, sc, "Hấp thụ và hệ số k",
             "Ghim cách 3 cm, che 30 %: lan, giữ hay tắt dần?", body=rows)
    kh = appear(t, M[0] + 3.0, 0.5)                  # goi y tu ve, hien tre ~2,5 s
    if kh <= 0: return
    card(d, (110, 1330, 970, 1540), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
    text(d, (W / 2, 1385), "Gợi ý", 40, ORANGE, alpha=kh)
    ctext(d, 1468, "Nhớ bảng 3 cm ở thí nghiệm trước", 44, INK, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.5, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for p, dt, rt in do_plan(do): cs.append((do["t0"] + dt, "tap"))
    cs += [(an["t0"] + 0.2, "ding"), (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l12-phanbach-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Phân hạch và lò phản ứng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Che bớt bàn ghim", draw=s_hook, tail=0.5, caps=[
   "Thả bi vào giữa.",
   ("Nghĩ trước khi xem.", 6.0)]),
 dict(key="do", title="Thả bi ở ba mức che", draw=s_do, tail=0.6, caps=[
   "Thả bi, đếm số ghim đổ.",
   ("Bìa chắn đường lan của ghim.", 5.6)]),
 dict(key="ans", title="Che càng nhiều, k càng nhỏ", draw=s_ans, tail=0.7, caps=[
   ("k dưới 1: tắt dần.", 3.2),
   ("Bìa nuốt ghim như thanh nuốt neutron.", 3.8)]),
 dict(key="lim", title="Giới hạn của mô hình", draw=s_lim, tail=0.5, caps=[
   ("Chỉ là mô hình.", 4.2)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.8, caps=[
   ("Câu nào sai?", 5.4),
   ("k so với 1.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Tự trả lời.", 6.6)]),
])
