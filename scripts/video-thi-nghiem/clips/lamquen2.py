# Clip: tn-l10-lam-quen-02 - Sach va to giay roi, 5 buoc nghien cuu (9/11/2026; dung lai 27/11/2026 theo cong moi viec 4:
#   --do-chu 0 LOI, chu ve >= 56 px, moi nhip >= 3 s co phu de, Du doan khong nut A-D (K10), thanh dem lien, cau chot A-D o khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-lam-quen-02.json (_kiem_so() doi chieu):
#   tham_so: h = 2 m, video 60 hinh/s, sai so dem +-1 khung.
#   so_lieu_mau: Sach 38 · 38 · 39 khung ; Giay vo tron 41 · 41 · 41 khung ; ghi_chu: sach TB 38,33 khung, chenh 2,67 khung > +-1.
#   mo_hinh: sach roi tu do (t = 0,6389 s -> 38,3 khung), giay vo t = 1,07 · t_sach (0,6833 s -> 41 khung);
#            giay phang chi dinh tinh (khong co so) -> hinh giay phang chi ve "cham han", khong ghi so.
# Trong bai (46): khoi video dung TRUOC hop exp; sau hop "Doc bang: tinh g" -> clip KHONG tinh g, KHONG noi nguon sai so.
#   Cau 3 (cau cua Lan la gia thuyet) -> clip goi "gia thuyet"; Cau 5 (bac bo = that bai) la Bay cua clip (cung y bai, khong
#   phai ca Du doan/chot); Cau 6 (38/41 khung, chenh vuot sai so) -> clip chi chieu chenh 2,7 > +-1, khong hoi lai.
# Du doan (K10: chi cau hoi + hinh): vo tron giay (khoi luong nhu cu), tha cung sach -> roi the nao? Dap an: cham hon sach chut it.
# Chot (khung web, ca moi, khong co trong bai): ong hut het khong khi, tha sach + giay phang -> cham day cung luc
#   (mo hinh: k_can = 1 khi khong co khong khi, goi_y_mo_phong.diem_nhan cua kho).
from engine import *

SACH = [38, 38, 39]; VO = [41, 41, 41]; FPS_V = 60; H_THA = 2.0
TB_SACH = sum(SACH) / 3; CHENH = VO[0] - TB_SACH                      # 38,33 ; 2,67

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-lam-quen-02.json")))
    hang = {r[0]: r[1:4] for r in k["so_lieu_mau"]["hang"]}
    assert hang["Sách"] == SACH and hang["Giấy vo tròn"] == VO
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["fps"]["gia_tri"] == FPS_V and ts["h"]["mac_dinh"] == H_THA and ts["n_khung"]["sai_so_do"] == 1
    assert abs(CHENH - 2.67) < 0.01 and abs(TB_SACH - 38.33) < 0.01
_kiem_so()

DRED = (185, 28, 28); DORANGE = (176, 64, 8); DGREEN = (10, 110, 50); DPURP = (91, 33, 182)
BOOK = (37, 99, 235); BOOK_D = (30, 64, 175); PAPER_D = (87, 83, 78)
STEPS = ["Thấy", "Hỏi", "Đoán", "Thử", "Chốt"]
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def steps(d, cur, alpha=1.0, y=292):
    """Dai 5 buoc (meo cua bai); cur = buoc dang lam."""
    w, g = 184, 10; x = (W - (5 * w + 4 * g)) / 2
    for i, s in enumerate(STEPS):
        on = i == cur; done = i < cur
        fill = ORANGE if on else ((255, 237, 213) if done else WHITE)
        card(d, (x, y - 42, x + w, y + 42), fill=A(fill, alpha), outline=A(ORANGE if (on or done) else (190, 180, 165), alpha), r=34, w=4)
        text(d, (x + w / 2, y), s, 56, WHITE if on else INK, alpha=alpha)
        x += w + g

# ---------- ve vat ----------
def book(d, cx, cy, alpha=1.0, paper=False):
    c = lambda col: A(col, alpha)
    d.rectangle([cx - 95, cy - 26, cx + 95, cy + 26], fill=c(BOOK), outline=c(BOOK_D), width=4)
    d.rectangle([cx - 78, cy - 13, cx + 95, cy + 13], fill=c((239, 246, 255)))
    if paper: d.rectangle([cx - 88, cy - 38, cx + 88, cy - 28], fill=c(WHITE), outline=c(PAPER_D), width=3)

def sheet(d, cx, cy, ang, alpha=1.0):
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); hx, hy = -uy * 6, ux * 6
    pts = [(cx - 95 * ux - hx, cy - 95 * uy - hy), (cx + 95 * ux - hx, cy + 95 * uy - hy),
           (cx + 95 * ux + hx, cy + 95 * uy + hy), (cx - 95 * ux + hx, cy - 95 * uy + hy)]
    d.polygon(pts, fill=A(WHITE, alpha), outline=A(PAPER_D, alpha))

def ball(d, cx, cy, alpha=1.0, s=1.0):
    r = 34 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A((245, 245, 244), alpha), outline=A(PAPER_D, alpha), width=4)
    for (x0, y0, x1, y1) in ((-18, -10, 6, 4), (-4, 12, 16, -6), (-14, 14, -2, 22), (4, -20, 18, -8)):
        d.line([(cx + x0 * s, cy + y0 * s), (cx + x1 * s, cy + y1 * s)], fill=A(PAPER_D, alpha), width=3)

def ground(d, x0, x1, yf, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.line([(x0, yf + 30), (x1, yf + 30)], fill=c(INK), width=6)
    for x in range(int(x0) + 10, int(x1), 40): d.line([(x, yf + 32), (x - 20, yf + 52)], fill=c(MUTED), width=3)

def hmark(d, x, yt, yf, alpha=1.0):
    d.line([(x, yt - 26), (x, yf + 28)], fill=A(INK, alpha), width=5)
    for yy in (yt - 26, yf + 28): d.line([(x - 14, yy), (x + 14, yy)], fill=A(INK, alpha), width=5)
    text(d, (x + 22, (yt + yf) / 2), "2 m", 56, INK, anchor="lm", alpha=alpha)

def fall(q, yt, yf): return yt + (yf - yt) * clamp(q) ** 2      # roi nhanh dan

def cbar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem lien day 80 px, rut tu phai sang trai."""
    p = clamp((t - t0) / (t1 - t0))
    d.rounded_rectangle([110, y, 970, y + 80], radius=40, fill=A((246, 244, 250), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(80, 860 * (1 - p)), y + 80], radius=40, fill=A(col, a))

SLOW = 20.0                              # khung video / giay man hinh (chieu cham 3 lan)
T_SACH, T_VO = 0.6389 * FPS_V / SLOW, 0.6833 * FPS_V / SLOW   # giay man hinh toi khi cham san (1,92 s ; 2,05 s)

# ---------------- canh 1: Thay - Hoi - Doan + Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    cur = 0 if t < M[1] - 0.05 else (1 if t < M[2] - 0.3 else 2)
    steps(d, cur, alpha=a)
    YT, YF = 480, 930
    ground(d, 210, 1000, YF, a); hmark(d, 120, YT, YF, a)
    text(d, (360, 395), "Sách", 56, BOOK_D, alpha=a); text(d, (770, 395), "Giấy phẳng", 56, PAPER_D, alpha=a)
    tau = max(t - 0.6, 0)
    book(d, 360, fall(tau / T_SACH, YT, YF) if tau > 0 else YT, alpha=a)
    yp = YT + (YF - YT) * clamp(tau / 9.0) ** 1.2                      # giay phang roi cham, chao lieng
    sheet(d, 770 + 34 * math.sin(tau * 3.0), yp, 16 * math.sin(tau * 3.0 + 1), alpha=a)
    kg = appear(t, M[1] + 0.5, 0.4)
    if kg > 0:                                                         # hai gia thuyet, cung mau cung co
        for i, s in enumerate(("Do nặng", "Do không khí cản")):
            yy = 1150 + i * 150
            card(d, (90, yy - 58, 990, yy + 58), fill=A(WHITE, kg), outline=A(NAVY, kg), r=28, w=4)
            dot(d, 165, yy, 36, A(NAVY, kg)); text(d, (165, yy), str(i + 1), 56, WHITE, alpha=kg)
            text(d, (235, yy), s, 60, INK, anchor="lm", alpha=kg)
    k = appear(t, M[2] - 0.3, 0.45)
    if k <= 0: return
    y0 = 1020 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 660), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 98), fill=A(PURPLE, k), r=36)
    text(d, (W / 2, y0 + 60), "DỰ ĐOÁN", 56, WHITE, alpha=k)
    cbar(d, y0 + 118, t, M[2] + 0.3, sc["T"] - 0.15, DPURP, k)         # thanh dem trong vung do hinh dong (y < 1580)
    book(d, 360, y0 + 290, alpha=k); ball(d, 720, y0 + 285, alpha=k, s=1.3)
    text(d, (360, y0 + 370), "Sách", 56, BOOK_D, alpha=k); text(d, (720, y0 + 370), "Giấy vo", 56, PAPER_D, alpha=k)
    text(d, (W / 2, y0 + 455), "Vo tròn tờ giấy,", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 530), "khối lượng như cũ.", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 605), "Giấy vo rơi thế nào?", 60, PURPLE, alpha=k)

# ---------------- canh 2: Thu (giay tren sach; sach + giay vo, dem khung 3 lan) ----------------
def phases(sc):
    M = sc["M"]
    return dict(a0=M[0] + 0.1, b0=M[1] + 0.5, r2=M[2] + 0.3, r3=M[2] + 0.9, badge=M[2] + 1.5)

def counter(d, cx, n, col, alpha=1.0):
    card(d, (cx - 165, 375, cx + 165, 465), fill=A(NAVY, alpha), r=24)
    text(d, (cx, 420), f"khung {n}", 58, WHITE, alpha=alpha)

def s_thu(img, d, t, sc):
    M = sc["M"]; P = phases(sc); a = appear(t, 0.05, 0.3)
    steps(d, 3, alpha=a)
    YT, YF = 560, 1000
    if t < M[1] - 0.1:                                                 # thu 1: giay dat tren sach
        ka = a * (1 - appear(t, M[1] - 0.4, 0.3))
        ground(d, 210, 870, YF, ka); hmark(d, 120, YT, YF, ka)
        q = (t - P["a0"]) / 1.0
        book(d, 540, fall(q, YT, YF) if q > 0 else YT, alpha=ka, paper=True)
        kr = appear(t, P["a0"] + 1.05, 0.3) * ka
        if kr > 0: text(d, (W / 2, 1180), "Giấy rơi cùng sách", 60, DGREEN, alpha=kr)
        return
    kb = appear(t, M[1] - 0.05, 0.3)                                   # thu 2: sach va giay vo, dem khung
    ground(d, 210, 1000, YF, kb); hmark(d, 120, YT, YF, kb)
    tau = t - P["b0"]
    n_s = min(SACH[0], int(max(tau, 0) * SLOW)); n_v = min(VO[0], int(max(tau, 0) * SLOW))
    for j, key in ((1, "r2"), (2, "r3")):                              # lan 2, 3 tua nhanh: bo dem chay lai tu 0
        if t >= P[key]:
            q = clamp((t - P[key]) / 0.5); n_s, n_v = int(q * SACH[j]), int(q * VO[j])
    counter(d, 360, n_s, BOOK_D, kb); counter(d, 770, n_v, PAPER_D, kb)
    yb = fall(tau / T_SACH, YT, YF) if tau > 0 else YT; yv = fall(tau / T_VO, YT, YF) if tau > 0 else YT
    if t >= P["r2"]:                                                   # lan 2, 3: tua nhanh (tha lai tu dau)
        tr = (t - (P["r3"] if t >= P["r3"] else P["r2"])) / 0.5
        yb = yv = fall(tr, YT, YF)
    book(d, 360, yb, alpha=kb); ball(d, 770, yv, alpha=kb)
    text(d, (360, YF + 105), "Sách", 56, BOOK_D, alpha=kb); text(d, (770, YF + 105), "Giấy vo", 56, PAPER_D, alpha=kb)
    text(d, (W / 2, YF + 190), "60 hình/giây", 56, INK, alpha=kb)
    ky = appear(t, P["b0"] + T_VO + 0.1, 0.3)                          # bang 3 lan
    if ky > 0:
        y0 = 1250; card(d, (60, y0, 1020, y0 + 230), fill=A(WHITE, ky), outline=A(NAVY, ky), w=4, r=24)
        for j, (nm, arr, col) in enumerate((("Sách", SACH, BOOK_D), ("Giấy vo", VO, PAPER_D))):
            yy = y0 + 62 + j * 106
            text(d, (100, yy), nm, 58, col, anchor="lm", alpha=ky)
            for i in range(3):
                ki = ky if i == 0 else appear(t, P["r2"] + 0.5 if i == 1 else P["r3"] + 0.5, 0.25)
                if ki > 0: text(d, (560 + i * 170, yy), str(arr[i]), 60, INK, alpha=ki)
    kd = appear(t, P["badge"], 0.4)
    if kd > 0:
        s_ = "ĐÁP ÁN: chậm hơn chút ít"; pw = tw(d, s_, F(58)) + 70
        card(d, (W / 2 - pw / 2, 1520, W / 2 + pw / 2, 1625), fill=A((220, 252, 231), kd), outline=A(GREEN, kd), r=28, w=5)
        text(d, (W / 2, 1572), s_, 58, DGREEN, alpha=kd)

# ---------------- canh 3: Rut ra (chenh so voi sai so -> gia thuyet nao dung vung) ----------------
def s_chot(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    steps(d, 4, alpha=a)
    PX = 14.0; X0 = 90                                                 # 14 px / khung
    g = ease((t - 0.3) / 1.8)
    for j, (nm, v, col) in enumerate((("Sách", TB_SACH, BOOK), ("Giấy vo", VO[0], PAPER_D))):
        yy = 470 + j * 130
        d.rounded_rectangle([X0, yy - 48, X0 + PX * v * max(g, 0.12), yy + 48], radius=18, fill=A(col, a))
        text(d, (X0 + 30, yy), nm, 58, WHITE, anchor="lm", alpha=a)
        kn = appear(t, 2.6, 0.4)                                       # so hien cung the "Chenh" (mot nhip)
        if kn > 0: text(d, (X0 + PX * v + 24, yy), (vn(v) if j == 0 else str(v)) + " khung", 58, INK, anchor="lm", alpha=kn)
    kc = appear(t, 2.6, 0.4)
    if kc > 0:
        xs, xv = X0 + PX * TB_SACH, X0 + PX * VO[0]
        for xx in (xs, xv): d.line([(xx, 640), (xx, 720)], fill=A(DRED, kc), width=5)
        d.line([(xs, 720), (xv, 720)], fill=A(DRED, kc), width=5)
        card(d, (90, 770, 990, 880), fill=A((254, 242, 242), kc), outline=A(DRED, kc), r=26, w=5)
        text(d, (W / 2, 825), f"Chênh {vn(CHENH)} khung > sai số ±1", 60, DRED, alpha=kc)
    kg = appear(t, M[1] + 0.9, 0.4)
    for i, (s, col, mk) in enumerate((("Do nặng", DRED, "✗"), ("Do không khí cản", DGREEN, "✓"))):
        if kg <= 0: break
        yy = 1020 + i * 150
        card(d, (90, yy - 58, 990, yy + 58), fill=A(WHITE, kg), outline=A(col, kg), r=28, w=5)
        text(d, (165, yy), mk, 64, col, alpha=kg)
        text(d, (235, yy), s, 60, col, anchor="lm", alpha=kg)

# ---------------- canh 4: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    k = appear(t, 0.05, 0.35)
    card(d, (60, 230, 1020, 560), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 320), "Chưa nói được", 62, NAVY, alpha=k)
    text(d, (W / 2, 450), "Giấy phẳng chậm bao nhiêu?", 60, INK, alpha=k)
    YT, YF = 700, 1250                                                 # giay phang chao lieng, khong co dong ho
    ground(d, 200, 880, YF, k)
    sheet(d, 540 + 60 * math.sin(t * 2.6), YT + (YF - YT) * clamp(t / 5.0) ** 1.2, 18 * math.sin(t * 2.6 + 1), alpha=k)
    text(d, (860, 760), "?", 120, NAVY, alpha=k)

# ---------------- canh 5: Bay (bac bo = that bai) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (50, 230, 1030, 760), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    yy = 400
    card(d, (110, yy - 62, 760, yy + 62), fill=A(WHITE, a), outline=A(NAVY, a), r=28, w=4)
    dot(d, 185, yy, 36, A(NAVY, a)); text(d, (185, yy), "1", 56, WHITE, alpha=a)
    text(d, (255, yy), "Do nặng", 60, INK, anchor="lm", alpha=a)
    ks = clamp((t - 0.6) / 0.4)
    if ks > 0:                                                         # dau X do de len gia thuyet 1
        cx, cy, r = 870, yy, 70 * ks
        d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=DRED, width=12); d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=DRED, width=12)
    text(d, (W / 2, 610), "Dễ tưởng: thí nghiệm hỏng", 60, DRED, alpha=a)
    kb = appear(t, M[1] - 0.05, 0.4)
    if kb <= 0: return
    card(d, (50, 800, 1030, 1560), fill=A(WHITE, kb), outline=A(GREEN, kb), w=6)
    pos = {"Đoán": (290, 960), "Thử": (790, 960)}
    for s, (cx, cy) in pos.items():
        card(d, (cx - 150, cy - 55, cx + 150, cy + 55), fill=A((255, 237, 213), kb), outline=A(ORANGE, kb), r=30, w=5)
        text(d, (cx, cy), s, 60, INK, alpha=kb)
    arrow(d, (450, 960), (630, 960), A(INK, kb), w=7, head=24)
    d.line([(790, 1020), (790, 1150), (290, 1150)], fill=A(DRED, kb), width=7)
    arrow(d, (290, 1150), (290, 1022), A(DRED, kb), w=7, head=24)
    text(d, (540, 1210), "không khớp", 58, DRED, alpha=kb)
    tl = (t - M[1]) % 3.0 / 3.0                                        # cham chay quanh vong lap
    L = [(450, 960), (630, 960), (790, 1020), (790, 1150), (290, 1150), (290, 1022)]
    seg = [math.dist(p, q) for p, q in zip(L, L[1:])]; s_ = tl * sum(seg)
    for (p, q), ln in zip(zip(L, L[1:]), seg):
        if s_ <= ln: dot(d, p[0] + (q[0] - p[0]) * s_ / ln, p[1] + (q[1] - p[1]) * s_ / ln, 16, A(PURPLE, kb)); break
        s_ -= ln
    text(d, (W / 2, 1390), "✓ Bác bỏ cũng là kết quả", 60, DGREEN, alpha=kb)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 220, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 326), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 288), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    x0, x1, y0, y1 = 290, 790, 430, 1130                               # ong thuy tinh, da hut khong khi
    d.rounded_rectangle([x0, y0, x1, y1], radius=40, fill=A((241, 245, 249), k1), outline=A(NAVY, k1), width=6)
    d.line([(W / 2, y0 - 50), (W / 2, y0)], fill=A(NAVY, k1), width=10)
    arrow(d, (W / 2 + 60, y0 - 30), (W / 2 + 200, y0 - 30), A(NAVY, k1), w=6, head=20)
    book(d, 430, 520, alpha=k1); sheet(d, 660, 515, 0, alpha=k1)
    text(d, (W / 2, 1210), "Hút hết khí, thả cùng lúc", 60, NAVY, alpha=k1)
    text(d, (W / 2, 1310), "Vật nào chạm đáy trước?", 60, ORANGE, alpha=k1)
    text(d, (880, 780 + 18 * math.sin(t * 3.0)), "?", 110, ORANGE, alpha=k1)
    cbar(d, 1420, t, 1.0, sc["T"] - 0.2, DORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, th, b, e = sc["hook"], sc["thu"], sc["bay"], sc["end"]; P = phases(th)
    return [(h["t0"] + h["M"][2] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (th["t0"] + P["a0"] + 1.0, "tap"), (th["t0"] + P["b0"] + T_SACH, "tap"), (th["t0"] + P["b0"] + T_VO, "tap"),
            (th["t0"] + P["r2"] + 0.5, "tick"), (th["t0"] + P["r3"] + 0.5, "tick"),
            (th["t0"] + P["badge"], "ding"), (b["t0"] + 0.6, "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-lam-quen-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Làm quen với Vật lí · thachlab.id.vn", scenes=[
 dict(key="hook", title="Sách và tờ giấy rơi", draw=s_hook, tail=0.2, caps=[
   ("Thả cùng lúc.", 3.0),
   ("Vì sao giấy chậm?", 3.0),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="thu", title="Kiểm tra", draw=s_thu, tail=0.3, caps=[
   ("Thử 1: giấy đặt trên sách.", 3.4),
   ("Thử 2: đếm khung hình.", 3.8),
   ("Thả thêm hai lần.", 3.0)]),
 dict(key="chot", title="Rút ra", draw=s_chot, tail=0.3, caps=[
   ("So chênh với sai số.", 3.6),
   ("Giấy vo nặng như cũ.", 3.8)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Chưa đo bằng số.", 3.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Khác dự đoán: hỏng ư?", 3.4),
   ("Đoán lại, thử tiếp.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Giả thuyết phải được kiểm chứng.", 5.6)]),
])
