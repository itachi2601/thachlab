# Clip: tn-l10-luc-can-luc-nang-02 - Chong pheu giay roi deu: luc can khi da roi deu (lo 8, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-luc-can-luc-nang-02.json:
#   so_lieu_mau (so pheu, t s, v m/s): 1 1,38 1,09 ; 2 0,95 1,58 ; 3 0,80 1,88 ; 4 0,67 2,24 (v = 1,50/t)
#   cac_buoc: tha tu 2,5 m, do t doan 1,50 m cuoi, trung binh 3 luot ; mo_hinh F_c = k.v^2, v(y) = v_gh.sqrt(1 - e^(-2gy/v_gh^2)).
# Du doan (K10: chi cau hoi + hinh): chong 4 pheu (nang gap 4), khi da roi deu, luc can khong khi len chong 4 pheu
#   so voi len 1 pheu? A. Bang nhau, vi cung hinh dang ; B. Gap 4 lan, vi trong luong gap 4 (DUNG) ;
#   C. Nho hon, vi roi nhanh nen it bi can.
# KHONG tra loi san: o "Doc so lieu" ngay sau bang trong bai (trong luong gap 4 thi v gap may? -> clip KHONG chia
#   2,24/1,09, khong noi "gap 2", khong noi v^2) ; Cau 1 muc II.1 (truot bang: hinh dang thuon -> clip khong noi hinh dang).
# Bay = hien_tuong_hay_sai[1] (nang roi nhanh hon vi trong luc "thang" luc can) -> da roi deu thi hop luc = 0.
# Cau chot (ca tu suy, ghi trong ghi_chu kho): 4 pheu, do tu luc buong tay qua 0,5 m dau -> 0,5/t KHONG ra toc do
#   roi deu (nho hon 2,24 m/s) vi doan dau pheu con nhanh dan. So 0,5 m chua hien tren man.
# Bo cuc: thuoc 2,5 m + pheu roi ben trai ; dong ho t + thanh toc do + bang ben phai ; dong bo: pheu cham san
#   dung luc dong ho dung o t kho va hang bang hien (_kiem_dong_bo()).
from engine import *

ROWS = [(1, 1.38, 1.09), (2, 0.95, 1.58), (3, 0.80, 1.88), (4, 0.67, 2.24)]   # so_lieu_mau
S_DO, H0, G = 1.50, 2.5, 9.8
DRED = (185, 28, 28); NOTE = (60, 64, 84)
PAPER = (250, 250, 252); PAPER_D = (150, 155, 175)
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

# ---------------- bo cuc ----------------
FLOOR = 1480; PXM = 440                  # y san ; px moi met (2,5 m -> y 380)
def Y(h): return FLOOR - h * PXM        # h: do cao tren san (m)
RX, PX = 205, 340                        # thuoc ; truc roi cua pheu

def ruler(d, a=1.0):
    d.rectangle([RX - 22, Y(H0) - 10, RX + 22, FLOOR], fill=A((250, 236, 200), a), outline=A((176, 124, 74), a), width=3)
    for k in range(26):
        y = Y(k * 0.1); L = 22 if k % 5 == 0 else 10
        d.line([(RX + 22 - L, y), (RX + 22, y)], fill=A(NAVY, a), width=3 if k % 5 == 0 else 2)
    d.rectangle([40, FLOOR, 1040, FLOOR + 26], fill=A((176, 124, 74), a))
    text(d, (RX - 30, Y(H0)), "2,5 m", 44, INK, anchor="rm", alpha=a)
    # vach 1,50 m: bat dau doan do
    for x in range(RX + 30, 480, 30): d.line([(x, Y(S_DO)), (x + 16, Y(S_DO))], fill=A(ORANGE, a), width=5)
    text(d, (RX - 30, Y(S_DO)), "1,50 m", 44, ORANGE, anchor="rm", alpha=a)
    text(d, (RX - 30, FLOOR - 26), "0", 44, INK, anchor="rm", alpha=a)

def funnel(d, cx, yb, n, a=1.0, lab=True):
    """Pheu giay (khuon nuong banh) mieng huong len; n pheu long khit -> vanh day them. yb: day pheu."""
    top, bot, hh = 70, 36, 52
    for j in range(n - 1, -1, -1):
        dy = -j * 7
        pts = [(cx - top, yb - hh + dy), (cx + top, yb - hh + dy), (cx + bot, yb + dy), (cx - bot, yb + dy)]
        d.polygon(pts, fill=A(PAPER, a), outline=A(PAPER_D, a), width=3)
    for k in range(-3, 4):                                   # nep giay
        d.line([(cx + k * top / 3.6, yb - hh + 4), (cx + k * bot / 3.6, yb - 3)], fill=A(PAPER_D, a), width=2)
    if lab and n > 1: text(d, (cx + top + 18, yb - hh / 2), f"×{n}", 44, INK, anchor="lm", alpha=a)

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

GAP = 0.9
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
    card(d, (520, 300, 1040, 560), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (780, 350), "t trên đoạn 1,50 m", 44, NOTE, alpha=a)
    text(d, (780, 430), ("– – –" if clock is None else vn(clock) + " s"), 64, RED, alpha=a)
    text(d, (560, 510), "tốc độ", 44, NOTE, anchor="lm", alpha=a)
    x0 = 720; w = 290 * v / 2.4
    d.rounded_rectangle([x0, 494, x0 + 290, 526], radius=10, fill=A(LIGHT, a))
    if w > 2: d.rounded_rectangle([x0, 494, x0 + w, 526], radius=10, fill=A(BLUE, a))

def table(d, nrow, hi=-1, a=1.0, y0=600):
    card(d, (520, y0, 1040, y0 + 520), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    xs = (600, 780, 950)
    text(d, (xs[0], y0 + 55), "Số", 44, INK, alpha=a); text(d, (xs[1], y0 + 55), "t (s)", 44, RED, alpha=a)
    text(d, (xs[2], y0 + 55), "v (m/s)", 44, BLUE, alpha=a)
    d.line([(540, y0 + 95), (1020, y0 + 95)], fill=A(LIGHT, a), width=4)
    for i in range(nrow):
        n, tk, v = ROWS[i]; y = y0 + 150 + i * 90
        if i == hi: d.rounded_rectangle([536, y - 38, 1024, y + 38], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), str(n), 46, INK, alpha=a); text(d, (xs[1], y), vn(tk), 46, RED, alpha=a)
        text(d, (xs[2], y), vn(v), 46, BLUE, alpha=a)
    text(d, (780, y0 + 560), "t: trung bình 3 lượt", 44, NOTE, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    ruler(d)
    h, v, clk, _ = fall(0, t - 0.8 if t < 3.2 else -1)        # tha thu 1 pheu roi dua ve
    funnel(d, PX, Y(h) + 20, 1)
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    x0, x1 = 480, 1040; cx = (x0 + x1) / 2; y0 = 300 + (1 - a) * 30
    card(d, (x0, y0, x1, y0 + 960), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (cx - pw / 2, y0 + 26, cx + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (cx, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (cx, y0 + 160), "4 phễu lồng khít:", 46, INK, alpha=a)
    text(d, (cx, y0 + 222), "nặng gấp 4", 46, INK, alpha=a)
    funnel(d, cx - 120, y0 + 380, 1, a, lab=False); funnel(d, cx + 110, y0 + 380, 4, a)
    for j, s in enumerate(("Đã rơi đều:", "lực cản lên 4 phễu", "so với lên 1 phễu?")):
        text(d, (cx, y0 + 580 + j * 70), s, 48, INK, alpha=a)
    text(d, (cx, y0 + 830), "Chọn đáp án ở khung câu hỏi", 40, NOTE, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([x0 + 60, y0 + 900, x1 - 60, y0 + 914], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([x0 + 60, y0 + 900, x0 + 60 + (x1 - x0 - 120) * (1 - p), y0 + 914], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: tien hanh ----------------
def s_do(img, d, t, sc):
    ruler(d)
    i, tau, rows = do_state(t)
    h, v, clk, landed = fall(i, tau)
    n = ROWS[i][0]
    funnel(d, PX, Y(h) - 1 + (0 if landed else 0), n)
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
    ka = appear(t, 0.1, 0.4)
    lab = "ĐÁP ÁN · Gấp 4 lần"
    pw = tw(d, lab, F(44)) + 60
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 342), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 306), lab, 44, WHITE, alpha=ka)
    k1 = appear(t, 0.5, 0.45)
    text(d, (110, 400), "↑ lực cản không khí: lên phễu", 44, BLUE, anchor="lm", alpha=k1)
    text(d, (110, 460), "↓ trọng lực: lên phễu", 44, RED, anchor="lm", alpha=k1)
    forces(d, 300, 1, k1); forces(d, 760, 4, appear(t, 1.0, 0.45))
    kr = appear(t, M[1] - 0.2, 0.45)
    if kr <= 0: return
    y0 = 1250 + (1 - kr) * 30
    card(d, (60, y0, 1020, y0 + 330), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
    pw = tw(d, "RÚT RA", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(GREEN, kr), r=32)
    text(d, (W / 2, y0 + 56), "RÚT RA", 40, WHITE, alpha=kr)
    text(d, (W / 2, y0 + 165), "Rơi đều: lực cản = trọng lượng", 48, INK, alpha=kr)
    text(d, (W / 2, y0 + 260), "Cản mạnh hơn khi rơi nhanh hơn", 46, (21, 110, 55), alpha=appear(t, M[1] + 0.6, 0.45))

# ---------------- canh 4: bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3); y = 330
    forces(d, 300, 1, a1, yb=700); forces(d, 760, 4, a1, yb=700)
    if a1 > 0:
        card(d, (40, 960, 1040, 1350), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, 988, W / 2 + pw / 2, 1052), fill=A(DRED, a1), r=32)
        text(d, (W / 2, 1020), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 2.0) / 0.4); f = F(46)
        for j, q in enumerate(("“4 phễu rơi đều nhanh hơn", "vì trọng lực thắng lực cản”")):
            yy = 1130 + j * 64; lw = tw(d, q, f)
            text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        if ks > 0: text(d, (110, 1162), "✗", 60, DRED, alpha=a1 * ks)
        k2 = appear(t, 2.4, 0.45) * a1
        text(d, (W / 2, 1285), "Rơi đều: hai mũi tên bằng nhau", 48, GREEN, alpha=k2)
    if k3 > 0:
        y1 = 330 + (1 - k3) * 30
        card(d, (40, y1, 1040, y1 + 520), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        for j, s1 in enumerate(("• Lực cản tăng theo v thế nào?", "• Phễu chao lật, bảng không thấy")):
            kk = k3 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y1 + 240 + 150 * j), s1, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: do tu luc buong tay qua 0,5 m dau; goi y tre 2,6 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 420, "Rơi đều: lực cản bằng trọng lượng", 48, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1290), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 840, "4 phễu: bấm giờ từ lúc buông, đo 0,5 m đầu. 0,5/t lớn hơn, bằng hay nhỏ hơn 2,24 m/s?",
          46, INK, maxw=900, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.6, 0.5)
    if kh > 0:
        card(d, (110, 1010, 970, 1250), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1065, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1170, "Đoạn đầu, tốc độ phễu đang thế nào?", 46, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + land(k), "tap") for k in range(4)]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-luc-can-luc-nang-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Lực cản và lực nâng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Phễu giấy rơi", draw=s_hook, tail=0.3, caps=[
   ("Thả phễu từ độ cao 2,5 m.", 3.2),
   ("Nghĩ trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Chồng 1, 2, 3, 4 phễu", draw=s_do, tail=1.0, caps=[
   ("Bấm giờ trên 1,50 m cuối.", 4.6),
   ("Chồng càng nhiều, t càng ngắn.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So hai mũi tên.", 4.0),
   ("Lực cản gấp 4.", 4.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 4.3),
   ("Còn bỏ ngỏ.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 7.8)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
