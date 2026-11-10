# Clip: tn-l11-motadddh-01 - Con lac lo xo nam ngang: keo lech 4 cm roi tha, vat co ra khoi doan [-A, A] khong
#       (31/10/2026, chang B L11 Dao dong)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-motadddh-01.json:
#   tham_so: A = 4 cm (2-8), T = 2 s (1-4), phi = 0 ; mo_hinh x = 4.cos(pi.t) ; gia_thiet: bo qua ma sat.
#   so_lieu_mau (t s, x cm): 0 4 ; 0,5 0 ; 1,0 -4 ; 1,5 0  (khong noi suy li do -> khong hien x giua cac moc).
#   hien_tuong_hay_sai[1]: hai lan x = 0 (t = 0,5 s va 1,5 s) di nguoc chieu -> bay.
#   Cau chot: keo lech 6 cm (A trong khoang tham_so, chua tung hien), quang duong trong 1,0 s dau? (2A = 12 cm, khong
#   hien; phan xa sai: 6 cm hoac 0 = li do; hien_tuong_hay_sai[0]). Goi y: bien do moi 6 cm, T van 2 s.
# Dan canh: TRUC CHINH la thuoc ngang duoi ray + vet cam (vung vat da quet) + bang 4 moc; khong do thi x-t
#   (motadddh2 dung do thi). Vat chay theo x = 4cos(pi.tau), quay cham x2, dung hinh o moi moc ghi so.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh -> Dap an + Rut ra + Chua noi duoc -> Bay (hai lan x = 0)
#       -> Chot + cau hoi tu nho lai (goi y tre 2,5 s, ve qua body).
from engine import *

AMP, PER = 4.0, 2.0                                    # tham_so A (cm), T (s)
ROWS = [(0.0, 4), (0.5, 0), (1.0, -4), (1.5, 0)]        # so_lieu_mau
def xof(tau): return AMP * math.cos(2 * math.pi * tau / PER)
def num(v, nd=None):
    s = (f"{v:.{nd}f}" if nd is not None else f"{v:g}").replace(".", ",")
    return s.replace("-", "−")

# ---------------- bo con lac (khung nguon 1080x1920) ----------------
OX, S = 600, 50                       # O o x = 600 px; 1 cm = 50 px; thuoc -8..8 cm -> 200..1000 px
WALL = 90                             # mat tuong
BH, BW = 90, 100                      # khoi vat
def px(xcm): return OX + xcm * S

def spring(d, x0, x1, y, col, n=12, amp=22, w=5):
    lead = 18; pts = [(x0, y), (x0 + lead, y)]
    L = (x1 - lead) - (x0 + lead)
    for i in range(1, 2 * n):
        pts.append((x0 + lead + L * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(x1 - lead, y), (x1, y)]
    d.line(pts, fill=col, width=w, joint="curve")

def dash_v(d, x, y0, y1, col, w=4, dash=14, gap=10):
    y = y0
    while y < y1:
        d.line([(x, y), (x, min(y1, y + dash))], fill=col, width=w); y += dash + gap

def rig(d, yb, xcm, ruler=True, a=1.0, olab=True):
    """Ray ngang, tuong trai, lo xo, vat (tam o x cm). yb = day vat = mat ray."""
    c = lambda col: A(col, a)
    d.rectangle([WALL - 30, yb - 150, WALL, yb + 30], fill=c((205, 200, 190)), outline=c(NAVY), width=3)
    for k in range(7):
        yy = yb - 140 + k * 26; d.line([(WALL - 30, yy + 18), (WALL - 8, yy)], fill=c(NAVY), width=2)
    d.rectangle([WALL, yb, 1040, yb + 20], fill=c((190, 195, 210)), outline=c(NAVY), width=3)
    dash_v(d, OX, yb - 140, yb, c(GRAY), w=4)
    if olab: text(d, (OX, yb - 168), "O", 44, INK, alpha=a)
    cx = px(xcm)
    spring(d, WALL, cx - BW / 2, yb - BH / 2, c(NAVY))
    card(d, (cx - BW / 2, yb - BH, cx + BW / 2, yb), fill=c(BLUE), outline=c(NAVY), r=12, w=4)
    if ruler:
        yr = yb + 50
        d.line([(px(-8), yr), (px(8), yr)], fill=c(NAVY), width=3)
        for k in range(-8, 9):
            L = 26 if k % 2 == 0 else 14
            d.line([(px(k), yr), (px(k), yr + L)], fill=c(NAVY), width=3)
            if k % 2 == 0: text(d, (px(k), yr + 54), num(k), 40, NAVY, bold=False, alpha=a)
        text(d, (135, yr + 54), "cm", 40, NAVY, bold=False, alpha=a)
        d.line([(cx, yb + 20), (cx, yr - 2)], fill=c(RED), width=5)          # kim chi vi tri vat tren thuoc
        d.polygon([(cx, yr - 2), (cx - 10, yr - 18), (cx + 10, yr - 18)], fill=c(RED))

YB = 610                              # day vat o cac canh chinh; thuoc y 660, so y 714

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.85, cx + pw / 2, cy + size * 0.85), fill=A(bg, a), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    k = ease((t - 1.0) / 1.4)                  # keo vat tu O ra +4 cm
    xb = AMP * k
    rig(d, YB, xb)
    ka = appear(t, 1.0, 0.4)
    if ka > 0 and xb > 0.3:
        y = YB - BH - 40
        arrow(d, (OX, y), (px(xb) - 6, y), A(ORANGE, ka), w=6, head=20)
        if k > 0.95: text(d, ((OX + px(xb)) / 2 + 20, y - 85), "4 cm", 42, ORANGE, alpha=appear(t, 2.3, 0.3))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 40, WHITE, PURPLE, a)
    ctext(d, y0 + 200, "Thả tay, bỏ qua ma sát.", 46, MUTED, maxw=920, alpha=a)
    ctext(d, y0 + 360, "Phía bên kia O, vật đi\nxa nhất tới đâu?", 54, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 530, 940, y0 + 542], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 530, 140 + 800 * (1 - p), y0 + 542], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (quay cham x2, dung o moi moc) ----------------
# v = giay trong canh. Dung o tau = 0 tu MK0; chay 0,5 s that trong RUN giay video; dung PAUSE o moi moc.
MK0, REL, RUN, PAUSE = 0.4, 1.2, 1.0, 0.8
def tau_do(v):
    """Thoi gian that (s) va so hang bang da ghi."""
    if v < REL: return 0.0, (1 if v >= MK0 else 0)
    u = v - REL; tau = 0.0; rows = 1
    for i in range(1, 5):                      # chay toi moc i (tau = 0,5 i), roi dung PAUSE (i = 4: tau = 2,0 giu yen)
        if u < RUN: return tau + 0.5 * u / RUN, rows
        u -= RUN; tau = 0.5 * i
        if i < 4: rows = i + 1
        if i < 4 and u < PAUSE: return tau, rows
        if i < 4: u -= PAUSE
    return tau, rows

def band_min(tau): return xof(min(tau, PER / 2))   # dau am xa nhat da toi (cm)

def table(d, rows, y0=800):
    card(d, (300, y0, 1020, y0 + 520), fill=WHITE, outline=NAVY, r=24, w=4)
    d.line([(660, y0 + 20), (660, y0 + 500)], fill=LIGHT, width=3)
    text(d, (480, y0 + 60), "t (s)", 44, NAVY); text(d, (840, y0 + 60), "x (cm)", 44, NAVY)
    d.line([(320, y0 + 105), (1000, y0 + 105)], fill=NAVY, width=3)
    for i in range(rows):
        tt, xx = ROWS[i]; y = y0 + 160 + i * 95
        text(d, (480, y), num(tt, 1) if tt else "0", 48, INK)
        text(d, (840, y), num(xx), 48, ORANGE)

def clock(d, tau, y=860):
    card(d, (40, y - 60, 270, y + 130), fill=(70, 78, 100), r=22)
    card(d, (56, y - 44, 254, y + 50), fill=(220, 240, 225), r=14)
    text(d, (155, y + 3), num(tau, 1), 54, (20, 60, 30))
    text(d, (155, y + 92), "t (s)", 40, WHITE, bold=False)

def s_do(img, d, t, sc):
    tau, rows = tau_do(t)
    xb = xof(tau)
    pill(d, 230, 330, "quay chậm ×2", 40, WHITE, ORANGE)
    # vet cam: vung vat da quet tren thuoc (tu +4 xuong dau am xa nhat da toi)
    if t >= REL:
        lo = band_min(tau)
        d.rectangle([px(lo) - 4, YB + 26, px(AMP) + 4, YB + 42], fill=A(ORANGE, 0.75))
    rig(d, YB, xb)
    for i in range(rows):                      # moc da ghi: cham xanh tren thuoc
        dot(d, px(ROWS[i][1]), YB + 50, 9, GREEN, outline=WHITE)
    clock(d, tau)
    table(d, rows)

# ---------------- canh 3: Dap an + Rut ra + Chua noi duoc ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    xb = xof(t / 2.0)                          # van chay quay cham x2 (khong hien dong ho, khong hien so li do)
    ka = appear(t, 0.1, 0.5)
    pill(d, W / 2, 330, "ĐÁP ÁN · x = −4 cm", 40, WHITE, NAVY, ka)
    d.rectangle([px(-AMP) - 4, YB + 26, px(AMP) + 4, YB + 42], fill=A(ORANGE, 0.75))
    for s_ in (-1, 1): dash_v(d, px(s_ * AMP), YB - 130, YB + 48, A(PURPLE, ka), w=4)
    rig(d, YB, xb)
    text(d, (px(-AMP), 790), "−A", 46, PURPLE, alpha=ka); text(d, (px(AMP), 790), "+A", 46, PURPLE, alpha=ka)
    k1 = appear(t, M[0] + 0.4, 0.45)
    if k1 > 0:
        card(d, (60, 850, 1020, 1130), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        text(d, (W / 2, 930), "−A ≤ x ≤ +A", 64, (21, 110, 55), alpha=k1)
        ctext(d, 1050, "A = 4 cm: lệch lớn nhất, do cách kéo", 42, INK, maxw=880, alpha=appear(t, M[0] + 1.0, 0.45))
    k2 = appear(t, M[1] - 0.05, 0.45)
    if k2 > 0:
        card(d, (60, 1180, 1020, 1500), fill=A(WHITE, k2), outline=A(NAVY, k2), r=24, w=5)
        text(d, (W / 2, 1240), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l in enumerate(("• Có ma sát: A giảm ra sao?", "• Kéo quá xa: lò xo hỏng?")):
            text(d, (100, 1340 + j * 95), l, 42, INK, anchor="lm", alpha=k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4))

# ---------------- canh 4: Bay - hai lan x = 0 ----------------
BYA, BYB = 470, 800                   # day vat hai ray
def s_bay(img, d, t, sc):
    M = sc["M"]
    for yb, lab, sgn in ((BYA, "t = 0,5 s", -1), (BYB, "t = 1,5 s", 1)):
        rig(d, yb, 0.0, ruler=False)
        text(d, (60, yb - 175), lab, 44, INK, anchor="lm")
        text(d, (1020, yb - 45), "x = 0", 42, ORANGE, anchor="rm")
        ya = yb + 62                          # mui ten chieu di, duoi ray (dao ham x = 4cos(pi t): am o 0,5 s, duong o 1,5 s)
        arrow(d, (OX, ya), (OX + sgn * 170, ya), GREEN, w=7, head=24)
        text(d, (OX + sgn * 280, ya), "chiều đi", 40, (21, 110, 55))
    y0 = 980
    card(d, (40, y0, 1040, y0 + 500), fill=WHITE, outline=(185, 28, 28), w=6)
    pill(d, W / 2, y0 + 62, "BẪY", 40, WHITE, (185, 28, 28))
    q = "“Hai lần x = 0 là như nhau”"
    yy = y0 + 200; f = F(48); lw = tw(d, q, f)
    text(d, (W / 2, yy), q, 48, (185, 28, 28))
    ks = clamp((t - (M[0] + 1.6)) / 0.4)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=(140, 15, 15), width=7)
    kc = appear(t, M[1] + 0.8, 0.5)
    ctext(d, y0 + 330, "✓ Cùng ở O, nhưng đi", 46, (21, 110, 55), maxw=920, alpha=kc)
    ctext(d, y0 + 400, "ngược chiều nhau", 46, (21, 110, 55), maxw=920, alpha=kc)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k1):
    """Hinh: cung lo xo, keo lech 6 cm (khong ghi li do luc 1,0 s). Goi y tu ve, tre 2,5 s sau cau hoi."""
    yb = 1170
    rig(d, yb, 6.0, ruler=False, a=k1, olab=False)
    text(d, (OX, yb - 168), "O", 44, INK, alpha=k1)
    y = yb - BH - 34
    arrow(d, (OX, y), (px(6) - 6, y), A(ORANGE, k1), w=6, head=20)
    text(d, ((OX + px(6)) / 2, y - 36), "6 cm", 42, ORANGE, alpha=k1)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Li độ luôn trong đoạn [−A; A]",
             "Cùng lò xo, kéo lệch 6 cm rồi thả.\nTrong 1,0 s đầu, vật đi được\nquãng đường bao nhiêu?", body=_end_body)
    kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
    if kh > 0:
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1355), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Biên độ mới 6 cm, T vẫn là 2 s", 44, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]            # K9: khong co tieng nao sat diem dung cuoi hook
    out += [(do["t0"] + MK0, "tick"), (do["t0"] + REL, "tap")]
    out += [(do["t0"] + REL + i * RUN + (i - 1) * PAUSE, "tick") for i in (1, 2, 3)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-motadddh-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Mô tả dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kéo lệch rồi thả", draw=s_hook, tail=0.6, caps=[
   ("Đánh dấu O: chỗ vật đứng yên.", 3.4),
   ("Tự đoán trước khi xem tiếp.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Thả tay, bấm giờ, ghi bốn mốc.", 4.4),
   ("Vệt cam: vùng vật đã đi qua.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Hai đầu đối xứng qua O.", 5.0),
   ("Mới thử một ca, bỏ ma sát.", 5.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: hai lần x = 0 là một?", 3.8),
   ("Nhìn chiều đi của vật.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
