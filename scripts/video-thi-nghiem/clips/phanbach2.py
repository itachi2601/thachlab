# Clip: tn-l12-phanbach-02 - Chen tam bia vao ban ghim: mo hinh thanh dieu khien hap thu neutron (Bai 16, lesson 17)
# So lieu nguyen tu content/thi-nghiem/tn-l12-phanbach-02.json: luoi 7 x 7 = 49 ghim cach 2 cm (dung_cu, tham_so N0),
# che 0 / 30 / 60 % (tham_so p), so ghim do 36·34·37 / 12·10·11 / 4·5·3, k uoc luong 1,6 / 1,0 / 0,6 (so_lieu_mau),
# "che 30 %: 10-12 ghim" (cac_buoc.quan_sat). Mo hinh DINH TINH (mo_hinh.ghi_chu) - ghi tren man.
# Hinh: tam bia ve thanh dai che tron cot ghim (30 %: 2 cot = 14/49 ghim; 60 %: 4 cot = 28/49) -> ghi "≈ 30 %", "≈ 60 %".
# Day chuyen lan theo the he (ghim do lam do ghim ke ben, 4 huong), ghim duoi bia khong truyen. Mot lan tha moi muc
# duoc ve (36, 12, 4 = lan 1 trong bang); so the he do random co dinh hat giong, khong in so the he len man.
#
# Dung lai 26/11/2026 theo KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32: cong --do-chu, chu >= 56 px, <= 50 s, Du doan khong
#   nut A-D (K10), canh Bay (hien_tuong_hay_sai[0]: thanh dieu khien "lam nguoi lo") + THU NGHI theo mau hatnhan3.
# Hop Du doan (cho JSON khung) - "Đặt tấm bìa che 30 % rồi 60 % lưới. Số ghim đổ thay đổi thế nào?"
#   A. Giảm theo đúng tỉ lệ phần bị che
#   B. Gần như không đổi cho tới khi che kín
#   C. Giảm mạnh, có mức che làm dây chuyền tắt sớm      <- ĐÁP ÁN
#   D. Tăng lên vì bi chỉ rơi vào phần còn hở
# Cau chot THU NGHI (vong 3): "Ghim cách 3 cm, che 30 %: lan, giữ hay tắt dần?" - goi y: "Nhớ bảng 3 cm ở thí nghiệm trước".
#   (khung: KHONG con dong goi y chu tren man; hinh hai hang ghim 2 cm / 3 cm)
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

DORANGE = (154, 52, 18); BROWN = (150, 118, 80); NOTE = (70, 75, 95)

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

def spacing_mark(d, a=1.0):
    x0, _ = P(0, 0); x1, _ = P(0, 1); y = BOARD[1] - 30
    d.line([(x0, y), (x1, y)], fill=A(NOTE, a), width=4)
    for x in (x0, x1): d.line([(x, y - 12), (x, y + 12)], fill=A(NOTE, a), width=4)
    text(d, (x1 + 16, y), "2 cm", 56, NOTE, anchor="lm", alpha=a)

def side(d, p_lbl, cnt, cnt_col=ORANGE):
    card(d, (780, 300, 1020, 560), fill=WHITE, outline=LIGHT, r=24, w=4)
    text(d, (900, 360), "Che", 56, NOTE)
    text(d, (900, 470), p_lbl, 60, BROWN if p_lbl != "0 %" else INK)
    card(d, (780, 590, 1020, 972), fill=WHITE, outline=LIGHT, r=24, w=4)
    text(d, (900, 650), "Đổ", 56, NOTE)
    text(d, (900, 770), cnt, 84, cnt_col)
    text(d, (900, 890), "/ 49", 56, NOTE)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    board(d, t, 0, -1, ball=False)
    spacing_mark(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 66, "DỰ ĐOÁN", PURPLE, a)
    seg_bar(d, y0 + 130, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, a)
    text(d, (W / 2, y0 + 300), "Bìa che 30 % rồi 60 % lưới.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 405), "Số ghim đổ thay đổi ra sao?", 60, PURPLE, alpha=a)

# ---------------- canh 2: tha bi o ba muc che ----------------
def do_plan(sc):
    M = sc["M"]
    d0 = 0.9
    d30 = d0 + NGEN[0] * GEN + 1.9
    d60 = d30 + NGEN[30] * GEN + 1.9
    return [(p, dt, dt + NGEN[p] * GEN + 0.45) for p, dt in ((0, d0), (30, d30), (60, d60))]

def do_state(t, sc):
    plan = do_plan(sc); cur = plan[0]
    for pl in plan:
        if t >= pl[1] - 0.75: cur = pl
    return cur, plan

def s_do(img, d, t, sc):
    (p, dt, rt), plan = do_state(t, sc)
    ck = 1.0 if p == 0 else clamp((t - (dt - 0.75)) / 0.5)
    tl = t - dt
    board(d, t, p, tl, cover_k=ck)
    spacing_mark(d)
    side(d, "0 %" if p == 0 else f"≈ {p} %", "···" if tl < 0 else str(n_fallen(p, tl)), cnt_col=NOTE if tl < 0 else ORANGE)
    card(d, (60, 1040, 1020, 1500), fill=WHITE, outline=NAVY, w=4)
    xs = [220, 640]
    text(d, (xs[0], 1100), "Che", 56, NOTE); text(d, (xs[1], 1100), "Đổ (3 lần)", 56, NOTE)
    d.line([(90, 1145), (990, 1145)], fill=LIGHT, width=4)
    for i, (pp, three, _) in enumerate(ROWS):
        a = 1.0 if i == 0 and t >= plan[0][2] else appear(t, plan[i][2], 0.35)
        if a <= 0: continue
        y = 1215 + i * 95
        if pp == p: d.rounded_rectangle([80, y - 42, 1000, y + 42], radius=14, fill=A((255, 237, 213), a))
        text(d, (xs[0], y), f"{pp} %", 58, BLUE, alpha=a)
        text(d, (xs[1], y), three, 58, INK, alpha=a)

# ---------------- canh 3: Dap an - k theo muc che ----------------
def s_ans(img, d, t, sc):
    M = sc["M"]
    pill(d, W / 2, 310, "ĐÁP ÁN: giảm mạnh", GREEN)
    card(d, (40, 390, 1040, 1130), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 450), "k ước lượng", 56, NOTE)
    yb, s = 960, 250
    d.line([(90, yb), (990, yb)], fill=NAVY, width=5)
    for xx in range(90, 990, 30): d.line([(xx, yb - s), (xx + 16, yb - s)], fill=RED, width=4)
    text(d, (985, yb - s - 40), "k = 1", 56, RED, anchor="rm")
    for i, (pp, _, kv) in enumerate(ROWS):
        cx = 220 + i * 320; g = ease((t - 0.3 - 0.5 * i) / 0.8)
        text(d, (cx, yb + 60), f"che {pp} %", 56, NOTE)
        if g <= 0: continue
        h = float(kv.replace(",", ".")) * s * g
        if h > 2: d.rectangle([cx - 70, yb - h, cx + 70, yb], fill=(BLUE, ORANGE, GRAY)[i])
        text(d, (cx + (0 if i != 1 else 0), yb - h - 40 if i != 1 else yb - h + 40), kv, 58, INK if i != 1 else WHITE, alpha=g)
    k2 = appear(t, M[1] + 0.3, 0.45)
    if k2 > 0:
        card(d, (40, 1180, 1040, 1420), fill=A((239, 246, 255), k2), outline=A(BLUE, k2), w=5)
        text(d, (230, 1300), "bìa", 62, BROWN, alpha=k2)
        arrow(d, (320, 1300), (470, 1300), A(INK, k2), w=8, head=26)
        text(d, (750, 1300), "thanh điều khiển", 60, BLUE, alpha=k2)
        pz = 0.5 + 0.5 * math.sin((t - M[1]) * 2 * math.pi / 1.2)
        d.rounded_rectangle([60, 1200, 1020, 1400], radius=26, outline=A(BLUE, k2 * (0.2 + 0.8 * pz)), width=6)

# ---------------- canh 4: Bay - "thanh dieu khien lam nguoi lo" ----------------
def s_trap(img, d, t, sc):
    M = sc["M"]; k1 = appear(t, 0.2, 0.4)
    card(d, (40, 260, 1040, 1100), fill=A(WHITE, k1), outline=A(RED, k1), w=6)
    pill(d, W / 2, 330, "BẪY", RED, k1)
    text(d, (W / 2, 445), "“Thanh điều khiển làm nguội lò”?", 58, INK, alpha=k1)
    # neutron bay tu trai sang, gap thanh thi bi nuot (bien mat) - lap lai
    rx = 640
    d.rounded_rectangle([rx - 30, 540, rx + 30, 900], radius=14, fill=A((90, 96, 112), k1))
    for j in range(5):
        y = 580 + j * 75; ph = ((t * 0.9 + j * 0.37) % 1.0)
        x = 120 + ph * 640
        if x < rx - 40: dot(d, x, y, 18, A(ORANGE, k1))
        else:
            q = clamp((x - rx + 40) / 60)
            if q < 1: dot(d, rx - 40, y, 18 * (1 - q), A(ORANGE, k1))
    text(d, (870, 720), "thanh", 56, NOTE, alpha=k1)
    kv = appear(t, M[1] + 0.2, 0.4)
    if kv > 0:
        card(d, (340, 950, 740, 1060), fill=A((254, 226, 226), kv), outline=A(RED, kv), r=30, w=5)
        text(d, (W / 2, 1005), "SAI", 72, RED, alpha=kv)
    k3 = appear(t, M[2] + 0.2, 0.45)
    if k3 > 0:
        card(d, (40, 1150, 1040, 1330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, 1240), "Hấp thụ neutron, k giảm", 62, NAVY, alpha=k3)

# ---------------- canh 5: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 260, 1040, 1500), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 340, "THỬ NGHĨ", ORANGE, k1)
    seg_bar(d, 420, t, 0.8, sc["T"] - 0.2, ORANGE, k1)
    text(d, (W / 2, 570), "Ghim cách 3 cm, che 30 %:", 60, INK, alpha=k1)
    text(d, (W / 2, 665), "lan, giữ hay tắt dần?", 60, DORANGE, alpha=k1)
    for j, (sp, lb, col) in enumerate(((60, "2 cm", NOTE), (90, "3 cm", ORANGE))):
        y = 900 + j * 220
        text(d, (110, y), lb, 60, col, anchor="lm", alpha=k1)
        for n in range(int(600 / sp) + 1):
            dot(d, 360 + n * sp, y, 16, A(NAVY, k1))
        if j == 1: text(d, (W / 2, y + 110), "?", 80, ORANGE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for p, dt, rt in do_plan(do): cs.append((do["t0"] + dt, "tap"))
    cs += [(an["t0"] + 0.2, "ding"), (tr["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return cs

SCENES = [
 dict(key="hook", title="Che bớt bàn ghim", draw=s_hook, tail=0.2, caps=[
   ("Lưới 49 ghim, thả bi vào giữa.", 3.2),
   ("Dừng lại, tự đoán.", 4.8)]),
 dict(key="do", title="Thả bi ở ba mức che", draw=s_do, tail=0.4, caps=[
   ("Thả bi, đếm số ghim đổ.", 3.6),
   ("Bìa chặn đường lan của ghim.", 6.4)]),
 dict(key="ans", title="Che càng nhiều, k càng nhỏ", draw=s_ans, tail=0.4, caps=[
   ("k dưới 1: dây chuyền tắt.", 3.8),
   ("Bìa đóng vai thanh điều khiển.", 3.8)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.4, caps=[
   ("Đúng hay sai?", 2.8),
   ("Thanh không làm nguội lò.", 3.2),
   ("Nó nuốt neutron đang lan.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=2.8, caps=[
   ("Hấp thụ hạt đang lan: k giảm.", 3.8)]),
]

CLIP = dict(id="tn-l12-phanbach-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Phân hạch và lò phản ứng · thachlab.id.vn", scenes=SCENES)
