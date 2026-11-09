# Clip: tn-l10-lam-quen-02 - Sach va to giay roi, 5 buoc nghien cuu (9/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-lam-quen-02.json:
#   tham_so: h = 2 m, video 60 hinh/s, sai so dem ±1 khung.
#   so_lieu_mau: Sach 38 · 38 · 39 khung ; Giay vo tron 41 · 41 · 41 khung ; ghi_chu: sach TB 38,33 khung, chenh 2,67 khung > ±1.
#   mo_hinh: sach roi tu do (t = 0,6389 s -> 38,3 khung), giay vo t = 1,07 · t_sach (0,6833 s -> 41 khung);
#            giay phang chi dinh tinh (khong co so) -> hinh giay phang chi ve "cham han", khong ghi so.
# Sau hop trong bai: "Doc bang: tinh g tu so lieu sach, sai so den tu dau" -> clip KHONG tinh g, KHONG noi nguon sai so ±1 khung.
# Truoc hop: Cau 3 (cau cua Lan la gia thuyet) da hoi -> clip duoc goi "Gia thuyet".
# Dai buoc tren dau man: Thay - Hoi - Doan - Thu - Chot (meo 🧠 cua bai).
# Canh: Thay/Hoi/Doan + Du doan (giay vo roi the nao so voi sach, K10: chi cau hoi + hinh) -> Thu (giay tren sach; giay vo,
#       dem khung 3 lan) -> Chot (chenh > sai so, GT1 bac bo, GT2 duoc ung ho) -> Chua noi duoc gi -> Bay (bac bo = that bai)
#       -> Chot + cau hoi (ong hut het khong khi: ca moi, chua hien).
from engine import *

DRED = (185, 28, 28)
BOOK = (37, 99, 235); BOOK_D = (30, 64, 175)
PAPER_D = (120, 113, 108)
STEPS = ["Thấy", "Hỏi", "Đoán", "Thử", "Chốt"]

def steps(d, cur, alpha=1.0, y=300):
    """Dai 5 buoc; cur = chi so buoc dang lam (cac buoc truoc mo dan, sau xam)."""
    w, g = 172, 15; x = (W - (5 * w + 4 * g)) / 2
    for i, s in enumerate(STEPS):
        on = i == cur; done = i < cur
        fill = ORANGE if on else ((255, 237, 213) if done else WHITE)
        card(d, (x, y - 34, x + w, y + 34), fill=A(fill, alpha), outline=A(ORANGE if (on or done) else LIGHT, alpha), r=30, w=3)
        text(d, (x + w / 2, y), s, 40, WHITE if on else (INK if done else GRAY), alpha=alpha)
        x += w + g

# ---------- ve vat ----------
def book(d, cx, cy, alpha=1.0, paper=False):
    c = lambda col: A(col, alpha)
    d.rectangle([cx - 85, cy - 24, cx + 85, cy + 24], fill=c(BOOK), outline=c(BOOK_D), width=4)
    d.rectangle([cx - 70, cy - 12, cx + 85, cy + 12], fill=c((239, 246, 255)))
    if paper: d.rectangle([cx - 80, cy - 34, cx + 80, cy - 26], fill=c(WHITE), outline=c(PAPER_D), width=2)

def sheet(d, cx, cy, ang, alpha=1.0):
    """To giay phang, nghieng ang (do)."""
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); hx, hy = -uy * 5, ux * 5
    pts = [(cx - 80 * ux - hx, cy - 80 * uy - hy), (cx + 80 * ux - hx, cy + 80 * uy - hy),
           (cx + 80 * ux + hx, cy + 80 * uy + hy), (cx - 80 * ux + hx, cy - 80 * uy + hy)]
    d.polygon(pts, fill=A(WHITE, alpha), outline=A(PAPER_D, alpha))

def ball(d, cx, cy, alpha=1.0, s=1.0):
    r = 32 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A((245, 245, 244), alpha), outline=A(PAPER_D, alpha), width=4)
    for (x0, y0, x1, y1) in ((-18, -10, 6, 4), (-4, 12, 16, -6), (-14, 14, -2, 22), (4, -20, 18, -8)):
        d.line([(cx + x0 * s, cy + y0 * s), (cx + x1 * s, cy + y1 * s)], fill=A(PAPER_D, alpha), width=3)

YT, YF = 520, 1040                       # muc tha (2 m) va san
def ground(d, xs, alpha=1.0, lab=True):
    c = lambda col: A(col, alpha)
    d.line([(xs[0], YF + 30), (xs[1], YF + 30)], fill=c(INK), width=5)
    for x in range(int(xs[0]) + 10, int(xs[1]), 40): d.line([(x, YF + 32), (x - 20, YF + 52)], fill=c(GRAY), width=3)
    if lab:
        arrow(d, (110, (YT + YF) / 2), (110, YT - 10), c(INK), w=4, head=16)
        arrow(d, (110, (YT + YF) / 2), (110, YF + 28), c(INK), w=4, head=16)
        text(d, (130, (YT + YF) / 2), "2 m", 40, INK, anchor="lm", alpha=alpha)
def fall(q):                             # q = t / t_cham -> y (roi nhanh dan)
    return YT + (YF - YT) * clamp(q) ** 2

# ---------------- canh 1: thay - hoi - doan + du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    cur = 0 if t < M[1] - 0.05 else (1 if t < M[1] + 0.9 else 2)
    steps(d, cur, alpha=a)
    kl = a * (1 - appear(t, M[1] + 0.6, 0.4))          # hai lan sach / giay phang, mo di khi sang Doan
    if kl > 0:
        ground(d, (200, 1000), alpha=kl)
        tau = t - 0.8
        text(d, (380, 430), "Sách", 40, BOOK_D, alpha=kl); text(d, (760, 430), "Giấy phẳng", 40, PAPER_D, alpha=kl)
        book(d, 380, fall(tau / T_SACH) if tau > 0 else YT, alpha=kl)
        yp = YT + (YF - YT) * clamp(max(tau, 0) / 7.0) ** 1.2 if tau > 0 else YT
        sheet(d, 760 + 30 * math.sin(max(tau, 0) * 3.2), yp, 14 * math.sin(max(tau, 0) * 3.2 + 1), alpha=kl)
    kg = appear(t, M[1] + 1.0, 0.4)
    if kg > 0:                                          # hai gia thuyet, cung mau cung co
        for i, s in enumerate(("Vật nặng rơi nhanh hơn", "Không khí cản giấy")):
            yy = 510 + i * 120
            card(d, (60, yy - 48, 1020, yy + 48), fill=A(WHITE, kg), outline=A(NAVY, kg), r=26, w=3)
            dot(d, 130, yy, 30, A(NAVY, kg)); text(d, (130, yy), str(i + 1), 40, WHITE, alpha=kg)
            text(d, (190, yy), s, 44, INK, anchor="lm", alpha=kg)
    k = appear(t, M[2] - 0.4, 0.5)
    if k <= 0: return
    y0 = 740 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 640), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 170, "Vo tròn giấy: khối lượng như cũ.", 46, INK, alpha=k)
    book(d, 400, y0 + 270, alpha=k); ball(d, 680, y0 + 270, alpha=k, s=1.4)
    text(d, (400, y0 + 345), "Sách", 40, BOOK_D, alpha=k); text(d, (680, y0 + 345), "Giấy vo", 40, PAPER_D, alpha=k)
    ctext(d, y0 + 460, "Thả cùng sách: giấy vo rơi thế nào?", 46, INK, alpha=k)
    t1, t2 = M[2] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 580, 880, y0 + 596], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 580, 200 + 680 * (1 - q), y0 + 596], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: thu ----------------
SLOW = 20.0                              # khung video / giay man hinh (chieu cham 3 lan)
SACH = [38, 38, 39]; VO = [41, 41, 41]
T_SACH, T_VO = 0.6389 * 60 / SLOW, 0.6833 * 60 / SLOW   # giay man hinh toi khi cham san
def phases(sc):
    M = sc["M"]
    return dict(a0=M[0] + 0.5, b0=M[1] + 0.6, r2=M[2] + 0.3, r3=M[2] + 0.9, badge=M[2] + 1.6)

def counter(d, cx, n, col, alpha=1.0):
    card(d, (cx - 110, 400, cx + 110, 470), fill=A(NAVY, alpha), r=20)
    text(d, (cx, 435), f"khung {n}", 40, WHITE, alpha=alpha)

def s_thu(img, d, t, sc):
    M = sc["M"]; P = phases(sc); a = appear(t, 0.1)
    steps(d, 3, alpha=a)
    if t < M[1] - 0.1:                                  # thu 1: giay dat tren sach
        ka = a * (1 - appear(t, M[1] - 0.4, 0.3))
        ground(d, (240, 840), alpha=ka)
        q = (t - P["a0"]) / 1.3
        book(d, 540, fall(q) if q > 0 else YT, alpha=ka, paper=True)
        kr = appear(t, P["a0"] + 1.4, 0.3) * ka
        if kr > 0: ctext(d, 1170, "Giấy rơi cùng sách", 46, GREEN, alpha=kr)
        return
    kb = appear(t, M[1] - 0.05, 0.4)                    # thu 2: sach va giay vo, dem khung
    ground(d, (200, 1000), alpha=kb)
    tau = t - P["b0"]
    n_s = min(SACH[0], int(max(tau, 0) * SLOW)); n_v = min(VO[0], int(max(tau, 0) * SLOW))
    if t >= P["r2"]: n_s, n_v = SACH[1], VO[1]
    if t >= P["r3"]: n_s, n_v = SACH[2], VO[2]
    counter(d, 380, n_s, BOOK_D, kb); counter(d, 760, n_v, PAPER_D, kb)
    yb = fall(tau / T_SACH) if tau > 0 else YT; yv = fall(tau / T_VO) if tau > 0 else YT
    if t >= P["r2"]: yb = yv = YF                       # lan 2, 3: tua nhanh, chi hien so
    book(d, 380, yb, alpha=kb); ball(d, 760, yv, alpha=kb)
    text(d, (380, YF + 100), "Sách", 40, BOOK_D, alpha=kb); text(d, (760, YF + 100), "Giấy vo", 40, PAPER_D, alpha=kb)
    text(d, (W / 2, YF + 170), "60 hình/giây, chiếu chậm", 40, MUTED, bold=False, alpha=kb)
    # bang 3 lan
    ky = appear(t, P["b0"] + T_VO + 0.1, 0.3)
    if ky > 0:
        y0 = 1300; card(d, (60, y0, 1020, y0 + 230), fill=A(WHITE, ky), outline=A(NAVY, ky), w=4, r=24)
        for j, (nm, arr, col) in enumerate((("Sách", SACH, BOOK_D), ("Giấy vo", VO, PAPER_D))):
            yy = y0 + 62 + j * 105
            text(d, (110, yy), nm, 44, col, anchor="lm", alpha=ky)
            for i in range(3):
                ki = ky if i == 0 else appear(t, P["r2"] if i == 1 else P["r3"], 0.3)
                if ki > 0: text(d, (520 + i * 170, yy), str(arr[i]), 48, INK, alpha=ki)
    kd = appear(t, P["badge"], 0.4)
    if kd > 0:
        s_ = "ĐÁP ÁN · chậm hơn sách chút ít"; pw = tw(d, s_, F(42)) + 70
        card(d, (W / 2 - pw / 2, 1560, W / 2 + pw / 2, 1656), fill=A((220, 252, 231), kd), outline=A(GREEN, kd), r=26, w=4)
        text(d, (W / 2, 1608), s_, 42, GREEN, alpha=kd)

# ---------------- canh 3: chot ----------------
def s_chot(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    steps(d, 4, alpha=a)
    card(d, (60, 400, 1020, 720), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (W / 2, 480), "Chênh ≈ 2,7 khung", 54, INK, alpha=a)
    kc = appear(t, M[0] + 1.0, 0.4)
    text(d, (W / 2, 545), "(41 − 38,3)", 40, MUTED, alpha=a)
    text(d, (W / 2, 640), "> độ lệch giữa các lần đo", 44, INK, alpha=kc)
    for i, (s, col, mk) in enumerate((("Giả thuyết 1: bác bỏ", DRED, "✗"), ("Giả thuyết 2: được ủng hộ", GREEN, "✓"))):
        kk = appear(t, M[1] + 1.1 + 0.8 * i, 0.4)
        if kk <= 0: continue
        yy = 860 + i * 130
        card(d, (60, yy - 50, 1020, yy + 50), fill=A(WHITE, kk), outline=A(col, kk), r=26, w=4)
        text(d, (130, yy), mk, 52, col, alpha=kk)
        text(d, (190, yy), s, 44, col, anchor="lm", alpha=kk)

# ---------------- canh 4: chua noi duoc gi ----------------
def s_gioihan(img, d, t, sc):
    k = appear(t, 0.05, 0.35); y1 = 290
    card(d, (60, y1, 1020, y1 + 900), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, y1 + 85), "Chưa nói được gì?", 54, NAVY, alpha=k)
    card(d, (110, y1 + 170, 970, y1 + 420), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 295, "Giấy phẳng: chưa đo", 50, BLUE, alpha=k)
    ctext(d, y1 + 560, "số liệu minh hoạ", 42, MUTED, bold=False, alpha=k)

# ---------------- canh 5: bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 270, 1020, 640), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 364), fill=A(DRED, a), r=32)
    text(d, (W / 2, 332), "Bẫy", 40, WHITE, alpha=a)
    for j, q in enumerate(("Bác bỏ = thí nghiệm hỏng",)):
        yy = 490 + j * 80; f = F(50); lw = tw(d, q, f)
        text(d, (W / 2, yy), q, 50, DRED, alpha=a)
        ks = clamp((t - 0.9 - 0.25 * j) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 10, yy + 2), (W / 2 - lw / 2 - 10 + (lw + 20) * ks, yy + 2)], fill=DRED, width=7)
    # vong lap Doan -> Thu -> khong khop -> Doan lai (hien cung phu de thu hai)
    kb = appear(t, M[1] - 0.05, 0.4)
    if kb > 0:
        for cx, s in ((300, "Đoán"), (780, "Thử")):
            card(d, (cx - 130, 760, cx + 130, 850), fill=A((255, 237, 213), kb), outline=A(ORANGE, kb), r=30, w=4)
            text(d, (cx, 805), s, 46, INK, alpha=kb)
        arrow(d, (440, 805), (640, 805), A(INK, kb), w=5, head=20)
        d.line([(780, 860), (780, 960), (300, 960)], fill=A(DRED, kb), width=5)
        arrow(d, (300, 960), (300, 862), A(DRED, kb), w=5, head=20)
        text(d, (540, 1010), "không khớp", 42, DRED, alpha=kb)
    kc = appear(t, M[1] + 2.0, 0.4)
    if kc > 0: ctext(d, 1180, "✓ Bác bỏ cũng là kết quả", 48, GREEN, alpha=kc)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    def body(d, t, k):
        ka = appear(t, sc["M"][0] + 0.4, 0.5)
        ctext(d, 840, "Ống chân không: thả sách\nvà giấy phẳng. Vật nào chạm trước?", 46, INK, maxw=900, alpha=ka)
        x0, x1 = 300, 780
        d.rounded_rectangle([x0, 960, x1, 1260], radius=20, outline=A(NAVY, ka), width=5)
        book(d, 440, 1010, alpha=ka); sheet(d, 640, 1010, 0, alpha=ka)
        kh = appear(t, sc["M"][0] + 2.9, 0.5)
        card(d, (110, 1300, 970, 1500), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1400, "Gợi ý: giấy chậm vì đâu?", 44, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Giả thuyết cần kiểm chứng", "", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, th, b, e = sc["hook"], sc["thu"], sc["bay"], sc["end"]; P = phases(th)
    return [(h["t0"] + h["M"][2] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (th["t0"] + P["a0"] + 1.3, "tap"), (th["t0"] + P["b0"] + T_SACH, "tap"), (th["t0"] + P["b0"] + T_VO, "tap"),
            (th["t0"] + P["r2"], "tick"), (th["t0"] + P["r3"], "tick"),
            (th["t0"] + P["badge"], "ding"), (b["t0"] + 0.9, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-lam-quen-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Làm quen với Vật lí · thachlab.id.vn", scenes=[
 dict(key="hook", title="Sách và tờ giấy rơi", draw=s_hook, tail=0.4, caps=[
   ("Thả cùng lúc.", 2.9),
   ("Vì sao giấy chậm?", 3.4),
   ("Dừng video, tự đoán.", 5.4)]),
 dict(key="thu", title="Kiểm tra", draw=s_thu, tail=0.4, caps=[
   ("Thử 1: giấy đặt trên sách.", 3.4),
   ("Thử 2: đếm khung hình.", 3.6),
   ("Thả 3 lần.", 3.2)]),
 dict(key="chot", title="Rút ra", draw=s_chot, tail=0.4, caps=[
   ("Vượt cả ba lần đo.", 3.4),
   ("Nặng như cũ, bị cản ít.", 4.0)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Còn thiếu.", 3.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Có đúng không?", 2.5),
   ("Không khớp thì đoán lại.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 6.4)]),
])
