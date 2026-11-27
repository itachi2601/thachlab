# Clip: tn-l10-luc-can-luc-nang-02 - Chong pheu giay roi deu: luc can khi da roi deu (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-luc-can-luc-nang-02.json:
#   so_lieu_mau (so pheu, t s, v m/s): 1 1,38 1,09 ; 2 0,95 1,58 ; 3 0,80 1,88 ; 4 0,67 2,24 (v = 1,50/t)
#   cac_buoc: tha tu 2,5 m, do t doan 1,50 m cuoi, trung binh 3 luot ; mo_hinh F_c = k.v^2, v(y) = v_gh.sqrt(1 - e^(-2gy/v_gh^2)).
# Du doan (K10, khong nut): chong 4 pheu long khit, da roi deu: luc can len 4 pheu so voi len 1 pheu? (dap an: gap 4).
# KHONG tra loi san o "Doc so lieu" cua bai (v gap may?) -> khong chia 2,24/1,09, khong noi v^2 ; Cau 1 muc II.1 (hinh dang).
# Bay = hien_tuong_hay_sai[1] ("trong luc thang luc can") -> da roi deu thi hai mui ten bang nhau, hop luc = 0.
# Chot (ca tu suy, ghi_chu kho): 4 pheu, bam gio tu luc buong, chi do 0,5 m dau -> 0,5/t nho hon 2,24 m/s
#   (buoc chua chieu: doan dau pheu con nhanh dan). Khong goi y.
# Dong bo: pheu cham san dung luc dong ho dung o t kho va hang bang hien (_kiem_dong_bo()).
from engine import *

ROWS = [(1, 1.38, 1.09), (2, 0.95, 1.58), (3, 0.80, 1.88), (4, 0.67, 2.24)]   # so_lieu_mau
S_DO, H0, G = 1.50, 2.5, 9.8
NOTE = (60, 64, 84); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128); DGREEN = (21, 110, 55)
PAPER = (250, 250, 252); PAPER_D = (150, 155, 175)
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- bo cuc ----------------
FLOOR = 1480; PXM = 440                  # y san ; px moi met (2,5 m -> y 380)
def Y(h): return FLOOR - h * PXM        # h: do cao tren san (m)
RX, PX = 235, 370                        # thuoc ; truc roi cua pheu

def ruler(d, a=1.0):
    d.rectangle([RX - 22, Y(H0) - 10, RX + 22, FLOOR], fill=A((250, 236, 200), a), outline=A((176, 124, 74), a), width=3)
    for k in range(26):
        y = Y(k * 0.1); L = 22 if k % 5 == 0 else 10
        d.line([(RX + 22 - L, y), (RX + 22, y)], fill=A(NAVY, a), width=3 if k % 5 == 0 else 2)
    d.rectangle([40, FLOOR, 1040, FLOOR + 26], fill=A((176, 124, 74), a))
    text(d, (RX - 32, Y(H0)), "2,5 m", 55, INK, anchor="rm", alpha=a)
    for x in range(RX + 30, 450, 30): d.line([(x, Y(S_DO)), (x + 16, Y(S_DO))], fill=A(ORANGE, a), width=5)
    text(d, (RX - 32, Y(S_DO)), "1,50 m", 55, DORANGE, anchor="rm", alpha=a)
    text(d, (RX - 32, FLOOR - 30), "0", 55, INK, anchor="rm", alpha=a)

def funnel(d, cx, yb, n, a=1.0, lab=True):
    """Pheu giay (khuon nuong banh) mieng huong len; n pheu long khit -> vanh day them. yb: day pheu."""
    top, bot, hh = 70, 36, 52
    for j in range(n - 1, -1, -1):
        dy = -j * 7
        pts = [(cx - top, yb - hh + dy), (cx + top, yb - hh + dy), (cx + bot, yb + dy), (cx - bot, yb + dy)]
        d.polygon(pts, fill=A(PAPER, a), outline=A(PAPER_D, a), width=3)
    for k in range(-3, 4):
        d.line([(cx + k * top / 3.6, yb - hh + 4), (cx + k * bot / 3.6, yb - 3)], fill=A(PAPER_D, a), width=2)
    if lab and n > 1: text(d, (cx + top + 16, yb - hh / 2), f"×{n}", 58, INK, anchor="lm", alpha=a)

# ---------------- chuyen dong: v' = g(1 - v^2/vg^2) qua 1 m dau, roi deu vg = 1,50/t qua 1,50 m cuoi ----------------
def _phase1(vg):
    t = s = v = 0.0; dt = 0.0005; tab = [(0.0, 0.0, 0.0)]
    while s < H0 - S_DO:
        v += G * (1 - v * v / (vg * vg)) * dt; s += v * dt; t += dt; tab.append((t, s, v))
    return tab
DROPS = []
for _n, _t, _v in ROWS:
    _vg = S_DO / _t; _tab = _phase1(_vg); DROPS.append(dict(vg=_vg, tab=_tab, t1=_tab[-1][0], tk=_t, tot=_tab[-1][0] + _t))

def fall(i, tau):
    """-> (do cao m, toc do m/s, dong ho (None neu chua vao doan do), da cham san)."""
    D = DROPS[i]
    if tau <= 0: return H0, 0.0, None, False
    if tau < D["t1"]:
        tab = D["tab"]; lo, hi = 0, len(tab) - 1
        while hi - lo > 1:
            m = (lo + hi) // 2
            if tab[m][0] <= tau: lo = m
            else: hi = m
        return H0 - tab[lo][1], tab[lo][2], None, False
    tt = tau - D["t1"]
    if tt < D["tk"]: return S_DO - D["vg"] * tt, D["vg"], tt, False
    return 0.0, 0.0, D["tk"], True

GAP = 0.7
STARTS = []
_s = 0.6
for _D in DROPS: STARTS.append(_s); _s += _D["tot"] + GAP
def land(i): return STARTS[i] + DROPS[i]["tot"]

def do_state(t):
    """-> (i lan tha dang ve, tau trong lan tha, so hang bang da hien)."""
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    rows = sum(1 for k in range(4) if t >= land(k) - 1e-9)
    return i, t - STARTS[i], rows

def readout(d, clock, v, a=1.0):
    card(d, (470, 290, 1040, 620), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (755, 340), "t: thời gian rơi", 55, NOTE, alpha=a)
    text(d, (755, 400), "1,50 m cuối", 55, DORANGE, alpha=a)
    text(d, (755, 480), ("– – –" if clock is None else vn(clock) + " s"), 66, RED, alpha=a)
    text(d, (500, 565), "tốc độ", 55, NOTE, anchor="lm", alpha=a)
    x0 = 700; w = 300 * v / 2.4
    d.rounded_rectangle([x0, 550, x0 + 300, 582], radius=10, fill=A(LIGHT, a))
    if w > 2: d.rounded_rectangle([x0, 550, x0 + w, 582], radius=10, fill=A(BLUE, a))

def table(d, nrow, hi=-1, a=1.0, y0=650):
    card(d, (470, y0, 1040, y0 + 500), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    xs = (550, 730, 930)
    text(d, (xs[0], y0 + 55), "n", 58, INK, alpha=a); text(d, (xs[1], y0 + 55), "t (s)", 58, RED, alpha=a)
    text(d, (xs[2], y0 + 55), "v (m/s)", 58, BLUE, alpha=a)
    d.line([(490, y0 + 100), (1020, y0 + 100)], fill=A(LIGHT, a), width=4)
    for i in range(nrow):
        n, tk, v = ROWS[i]; y = y0 + 160 + i * 88
        if i == hi: d.rounded_rectangle([486, y - 38, 1024, y + 38], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), str(n), 60, INK, alpha=a); text(d, (xs[1], y), vn(tk), 60, RED, alpha=a)
        text(d, (xs[2], y), vn(v), 60, BLUE, alpha=a)
    text(d, (755, y0 + 560), "n: số phễu", 55, NOTE, alpha=a)
    text(d, (755, y0 + 630), "v: tốc độ = 1,50 m : t", 55, NOTE, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    ruler(d)
    h, v, clk, _ = fall(0, t - 0.6 if t < 3.0 else -1)        # tha thu 1 pheu roi dua ve
    funnel(d, PX, Y(h) + 20, 1)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    x0, x1 = 470, 1040; cx = (x0 + x1) / 2; y0 = 290 + (1 - a) * 30
    card(d, (x0, y0, x1, y0 + 1000), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, cx, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (cx, y0 + 170), "4 phễu lồng khít", 58, INK, alpha=a)
    funnel(d, cx - 130, y0 + 330, 1, a, lab=False); funnel(d, cx + 90, y0 + 330, 4, a)
    for j, s1 in enumerate(("Đã rơi đều:", "lực cản lên 4 phễu", "so với 1 phễu?")):
        text(d, (cx, y0 + 470 + j * 85), s1, 60, PURPLE if j == 2 else INK, alpha=a)
    seg_bar(d, y0 + 820, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a, x0=x0 + 40, step=100, w=86)

# ---------------- canh 2: tien hanh ----------------
def s_do(img, d, t, sc):
    ruler(d)
    i, tau, rows = do_state(t)
    h, v, clk, landed = fall(i, tau)
    funnel(d, PX, Y(h) - 1, ROWS[i][0])
    readout(d, clk, v)
    table(d, rows, hi=rows - 1)

def _kiem_dong_bo():
    """Moi 0,05 s: dong ho = t kho dung luc hang moi hien; pheu cham san dung luc do; khong chay qua cuoi canh."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []; t = 0.0
    while t < sc["T"]:
        i, tau, rows = do_state(t); h, v, clk, landed = fall(i, tau)
        if landed and rows != i + 1: bad.append(("hang", round(t, 2)))
        if rows == i + 1 and (not landed or abs(clk - ROWS[i][1]) > 1e-9): bad.append(("dong ho", round(t, 2)))
        if clk is not None and clk > ROWS[i][1] + 1e-9: bad.append(("vuot", round(t, 2)))
        t += 0.05
    for D, (n, tk, v) in zip(DROPS, ROWS):
        if abs(S_DO / tk - D["vg"]) > 1e-9 or abs(round(S_DO / tk, 2) - v) > 0.011: bad.append(("v", n))
    if land(3) + 0.8 > sc["T"]: bad.append("lan cuoi sat cuoi canh")
    return bad

# ---------------- canh 3: dap an + rut ra ----------------
def forces(d, cx, n, a=1.0, yb=900):
    """Hai luc len pheu dang roi deu: luc can (len) = trong luc (xuong), do dai ti le n."""
    funnel(d, cx, yb, n, a)
    L = 62 * n; yc = yb - 26
    arrow(d, (cx, yc - 30), (cx, yc - 30 - L), A(BLUE, a), w=8, head=24)
    arrow(d, (cx, yc + 10), (cx, yc + 10 + L), A(RED, a), w=8, head=24)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, -0.5, 0.4)
    card(d, (300, 250, 780, 340), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), w=5)
    text(d, (540, 295), "Gấp 4 lần", 62, DGREEN, alpha=ka)
    text(d, (80, 400), "↑ lực cản không khí", 58, BLUE, anchor="lm", alpha=ka)
    text(d, (80, 470), "↓ trọng lực", 58, RED, anchor="lm", alpha=ka)
    forces(d, 300, 1, ka); forces(d, 740, 4, appear(t, 1.0, 0.45))
    kr = appear(t, M[1], 0.45)
    if kr <= 0: return
    y0 = 1260 + (1 - kr) * 30
    card(d, (40, y0, 1040, y0 + 250), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
    pill(d, W / 2, y0 + 62, "RÚT RA", GREEN, kr)
    text(d, (W / 2, y0 + 170), "Rơi đều: lực cản = trọng lượng", 60, DGREEN, alpha=kr)

# ---------------- canh 4: bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    kf = appear(t, M[1], 0.45)
    funnel(d, 300, 760, 1, 1.0); funnel(d, 740, 760, 4, 1.0)
    if kf > 0:
        forces(d, 300, 1, kf, yb=760); forces(d, 740, 4, kf, yb=760)
    if a1 > 0:
        card(d, (40, 1120, 1040, 1350), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, 1185, "BẪY", RED, a1)
        q = "“Trọng lực thắng lực cản”"
        ks = clamp((t - M[1]) / 0.4); f = F(60); lw = tw(d, q, f); yy = 1285
        text(d, (W / 2, yy), q, 60, mix(RED, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        kv = appear(t, M[1] + 3.0, 0.45) * a1
        if kv > 0:
            card(d, (40, 1380, 1040, 1520), fill=A((220, 252, 231), kv), outline=A(GREEN, kv), w=5)
            text(d, (W / 2, 1450), "Rơi đều: hợp lực bằng 0", 60, DGREEN, alpha=kv)
    if k3 > 0:
        card(d, (40, 1120, 1040, 1520), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 1190, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 1320), "Cản tăng theo tốc độ ra sao?", 60, INK, alpha=k3)
        text(d, (W / 2, 1420), "Phễu chao lật: chưa thấy.", 60, INK, alpha=k3)

# ---------------- canh 5: thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 300, 1040, 1150), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 375, "THỬ NGHĨ", ORANGE, k)
    funnel(d, W / 2, 560, 4, k)
    text(d, (W / 2, 690), "4 phễu, đo 0,5 m đầu,", 62, INK, alpha=k)
    text(d, (W / 2, 780), "tính từ lúc buông.", 62, INK, alpha=k)
    text(d, (W / 2, 880), "0,5 m : t so với 2,24 m/s?", 62, DORANGE, alpha=k)
    seg_bar(d, 1000, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + land(k), "tap") for k in range(4)]
            + [(da["t0"] + 0.1, "ding"), (da["t0"] + da["M"][1], "tap"), (b["t0"] + b["M"][1], "buzz"),
               (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-luc-can-luc-nang-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Lực cản và lực nâng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Phễu giấy rơi", draw=s_hook, tail=0.2, caps=[
   ("Thả phễu từ 2,5 m.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Chồng 1, 2, 3, 4 phễu", draw=s_do, tail=0.5, caps=[
   ("Bấm giờ trên 1,50 m cuối.", 4.6),
   ("Chồng càng nhiều, t càng ngắn.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Đã rơi đều: hai lực cân bằng.", 3.8),
   ("Rơi đều: lực cản = trọng lượng.", 4.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.0),
   ("Lúc rơi đều thì sao?", 6.1),
   ("Chưa nói được.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 6.8)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
