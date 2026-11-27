# Clip: tn-l11-motadddh-01 - Con lac lo xo nam ngang: keo lech 4 cm roi tha - li do va quang duong
#       (31/10/2026, chang B L11 Dao dong; dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu >= 55 px,
#       Du doan K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-motadddh-01.json (_kiem_so() doi chieu):
#   tham_so: A = 4 cm (2-8), T = 2 s (1-4), phi = 0 ; mo_hinh x = 4.cos(pi.t) ; gia_thiet: bo qua ma sat.
#   so_lieu_mau (t s, x cm): 0 4 ; 0,5 0 ; 1,0 -4 ; 1,5 0.
# DOI CA Du doan (27/11): ca cu "ben kia O vat di xa nhat toi dau" da co dap so trong hop exp ngay tren video
#   ([-4; 4] cm). Ca moi = hien_tuong_hay_sai[0] "tuong li do bang quang duong": tha tu 4 cm, toi dau ben kia vat da di
#   quang duong bao nhieu? -> 8 cm (li do luc do -4 cm). Cot "quang duong" trong bang suy tu mo hinh (4, 8, 12 cm).
# Bay = hien_tuong_hay_sai[1]: hai lan x = 0 (t = 0,5 s va 1,5 s) di nguoc chieu.
# Thu nghi (= cau_chot khung web): cung lo xo (T = 2 s), keo lech 6 cm, trong 2,0 s dau di quang duong? = 4A = 24 cm
#   (buoc chua chieu: 2,0 s = mot chu ki, ve lai cho tha). Nhieu: 0 (li do doi = 0), 6, 12 cm. 24 khong hien.
from engine import *

AMP, PER = 4.0, 2.0                                    # tham_so A (cm), T (s)
ROWS = [(0.0, 4), (0.5, 0), (1.0, -4), (1.5, 0)]        # so_lieu_mau
PATH = [0, 4, 8, 12]                                    # quang duong da di toi moi moc (suy tu mo hinh)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-motadddh-01.json")))
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["A"]["mac_dinh"] == AMP and ts["T"]["mac_dinh"] == PER and ts["A"]["min"] <= 6 <= ts["A"]["max"]
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
_kiem_so()

def xof(tau): return AMP * math.cos(2 * math.pi * tau / PER)
def num(v, nd=None):
    s = (f"{v:.{nd}f}" if nd is not None else f"{v:g}").replace(".", ",")
    return s.replace("-", "−")

# ---------------- bo con lac (khung nguon 1080x1920) ----------------
OX, S = 560, 50                       # O o x = 560 px; 1 cm = 50 px; thuoc -8..8 cm -> 160..960 px
WALL = 90
BH, BW = 90, 100
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

def rig(d, yb, xcm, ruler=True, a=1.0):
    """Ray ngang, tuong trai, lo xo, vat (tam o x cm). yb = day vat = mat ray."""
    c = lambda col: A(col, a)
    d.rectangle([WALL - 30, yb - 150, WALL, yb + 30], fill=c((205, 200, 190)), outline=c(NAVY), width=3)
    for k in range(7):
        yy = yb - 140 + k * 26; d.line([(WALL - 30, yy + 18), (WALL - 8, yy)], fill=c(NAVY), width=2)
    d.rectangle([WALL, yb, 1040, yb + 20], fill=c((190, 195, 210)), outline=c(NAVY), width=3)
    dash_v(d, OX, yb - 140, yb, c(GRAY), w=4)
    text(d, (OX - 18, yb - 165), "O", 56, INK, anchor="rm", alpha=a)            # tren dau vach net dut, khong de len vat
    cx = px(xcm)
    spring(d, WALL, cx - BW / 2, yb - BH / 2, c(NAVY))
    card(d, (cx - BW / 2, yb - BH, cx + BW / 2, yb), fill=c(BLUE), outline=c(NAVY), r=12, w=4)
    if ruler:
        yr = yb + 50
        d.line([(px(-8), yr), (px(8), yr)], fill=c(NAVY), width=3)
        for k in range(-8, 9):
            L = 26 if k % 2 == 0 else 14
            d.line([(px(k), yr), (px(k), yr + L)], fill=c(NAVY), width=3)
            if k % 4 == 0: text(d, (px(k) + (28 if k == 8 else 0), yr + 62), num(k) + (" cm" if k == 8 else ""), 56, NAVY, alpha=a)
        d.line([(cx, yb + 20), (cx, yr - 2)], fill=c(RED), width=5)
        d.polygon([(cx, yr - 2), (cx - 10, yr - 18), (cx + 10, yr - 18)], fill=c(RED))

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.8, cx + pw / 2, cy + size * 0.8), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    """Thanh dem lien khoi, tat lan luot tu PHAI sang TRAI; cao 76 px."""
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); wseg = 820 / n
    for i in range(n):
        x = 130 + i * wseg
        if i < on: card(d, (x, y, x + wseg - 14, y + 76), fill=A(col, a), r=16)
        else: card(d, (x, y, x + wseg - 14, y + 76), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

def pull_arrow(d, yb, xcm, lab, a=1.0):
    y = yb - BH - 40
    arrow(d, (OX, y), (px(xcm) - 6, y), A(ORANGE, a), w=7, head=22)
    text(d, ((OX + px(xcm)) / 2, y - 50), lab, 58, DORANGE, alpha=a)

YB = 560

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    k = ease((t - 0.6) / 1.4)                  # keo vat tu O ra +4 cm
    rig(d, YB, AMP * k)
    pull_arrow(d, YB, max(0.4, AMP * k), "4 cm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 860 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 64, "DỰ ĐOÁN", 56, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 160), "Kéo lệch 4 cm rồi thả,", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 235), "bỏ qua ma sát.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 320), "Tới đầu bên kia, vật", 62, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 395), "đi quãng đường bao nhiêu?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 490, t, M[1] + 0.4, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh (quay cham x2, dung o moi moc) ----------------
MK0, REL, RUN, PAUSE = 0.0, 2.2, 1.2, 0.9               # cac hang bang cach nhau >= 2,1 s
def tau_do(v):
    """Thoi gian that (s) va so hang bang da ghi."""
    if v < REL: return 0.0, 1
    u = v - REL; tau = 0.0; rows = 1
    for i in range(1, 5):
        if u < RUN: return tau + 0.5 * u / RUN, rows
        u -= RUN; tau = 0.5 * i
        if i < 4: rows = i + 1
        if i < 4 and u < PAUSE: return tau, rows
        if i < 4: u -= PAUSE
    return tau, rows

def path_of(tau):                                       # quang duong da di (cm) theo mo hinh
    q = int(tau // 0.5); r = tau - 0.5 * q
    return 4 * q + abs(xof(0.5 * q) - xof(0.5 * q + r))

def table(d, rows, y0=820):
    card(d, (60, y0, 1020, y0 + 560), fill=WHITE, outline=NAVY, r=24, w=4)
    xs = (220, 540, 860)
    for x, h in zip(xs, ("t (s)", "x (cm)", "s (cm)")): text(d, (x, y0 + 62), h, 56, NAVY)
    d.line([(80, y0 + 110), (1000, y0 + 110)], fill=NAVY, width=3)
    for i in range(rows):
        tt, xx = ROWS[i]; y = y0 + 170 + i * 98
        text(d, (xs[0], y), num(tt, 1) if tt else "0", 58, INK)
        text(d, (xs[1], y), num(xx), 58, BLUE)
        text(d, (xs[2], y), str(PATH[i]), 58, DORANGE)

def s_do(img, d, t, sc):
    tau, rows = tau_do(t)
    xb = xof(tau)
    pill(d, 200, 320, "chậm ×2", 56, WHITE, ORANGE)
    pill(d, 700, 320, f"t = {num(tau, 2)} s", 56, WHITE, NAVY)
    if t >= REL:                                        # vet cam: quang duong da di (cong don, ve theo chieu di)
        s_ = path_of(tau); y = YB + 30
        lo = px(max(-AMP, AMP - s_)) if s_ <= 8 else px(-AMP)
        d.rectangle([lo - 4, y - 6, px(AMP) + 4, y + 10], fill=A(ORANGE, 0.8))
        if s_ > 8: d.rectangle([px(-AMP) - 4, y + 12, px(-AMP + (s_ - 8)) + 4, y + 26], fill=A(ORANGE, 0.8))
    rig(d, YB, xb)
    table(d, rows)

# ---------------- canh 3: Ket qua + rut ra + chua noi duoc ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    k = clamp((t - 0.3) / 2.0)
    xb = AMP * math.cos(math.pi * k)                    # tha lai tu +4 toi -4 (quay cham), roi dung o -4
    if t > 2.6: xb = xof((t - 2.6) / 4.0 + 1.0)          # tiep tuc dao dong cham (khong dung hinh)
    lo = px(AMP - 8 * k) if t <= 2.6 else px(-AMP)
    y = YB + 30
    d.rectangle([lo - 4, y - 6, px(AMP) + 4, y + 10], fill=A(ORANGE, 0.8))
    rig(d, YB, xb)
    kb = appear(t, 2.4, 0.4)
    if kb > 0:
        yb = YB - BH - 60
        d.line([(px(-AMP), yb), (px(AMP), yb)], fill=A(DORANGE, kb), width=6)
        for xx in (px(-AMP), px(AMP)): d.line([(xx, yb - 16), (xx, yb + 16)], fill=A(DORANGE, kb), width=6)
        text(d, (OX + 120, yb - 50), "8 cm", 58, DORANGE, alpha=kb)
        card(d, (60, 830, 1020, 1040), fill=A((255, 247, 237), kb), outline=A(ORANGE, kb), r=24, w=5)
        text(d, (W / 2, 890), "Li độ: x = −4 cm", 60, BLUE, alpha=kb)
        text(d, (W / 2, 980), "Quãng đường: 4 + 4 = 8 cm", 60, DORANGE, alpha=kb)
    kn = appear(t, M[2] - 0.05, 0.45)
    if kn > 0:
        card(d, (60, 1090, 1020, 1400), fill=A(WHITE, kn), outline=A(NAVY, kn), r=24, w=5)
        text(d, (W / 2, 1150), "Chưa nói được", 60, NAVY, alpha=kn)
        text(d, (100, 1240), "• Có ma sát: A giảm?", 58, INK, anchor="lm", alpha=kn)
        text(d, (100, 1330), "• Kéo quá xa: lò xo hỏng?", 58, INK, anchor="lm", alpha=appear(t, M[2] + 2.5, 0.4))

# ---------------- canh 4: Bay - hai lan x = 0 ----------------
BYA, BYB = 470, 860
def s_bay(img, d, t, sc):
    M = sc["M"]
    for yb, lab, sgn in ((BYA, "t = 0,5 s", -1), (BYB, "t = 1,5 s", 1)):
        ph = ((t * 0.5) % 1.0)                         # vat nhich quanh O theo chieu di (chay lap, khong dung hinh)
        rig(d, yb, sgn * 1.2 * ph, ruler=False)
        text(d, (60, yb - 200), lab, 58, INK, anchor="lm")
        ya = yb + 70
        arrow(d, (OX, ya), (OX + sgn * 200, ya), DGREEN, w=8, head=26)
        text(d, (OX + sgn * 340, ya), "chiều đi", 56, DGREEN)
    y0 = 1060
    card(d, (40, y0, 1040, y0 + 150), fill=(254, 242, 242), outline=DRED, r=24, w=5)
    text(d, (W / 2, y0 + 75), "✗ Cùng x = 0 là như nhau", 60, DRED)
    kc = appear(t, M[1] - 0.1, 0.4)
    if kc > 0:
        card(d, (40, y0 + 190, 1040, y0 + 340), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=24, w=5)
        text(d, (W / 2, y0 + 265), "✓ Cùng ở O, ngược chiều", 60, DGREEN, alpha=kc)

# ---------------- canh 5: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    if t < 0.15: return
    card(d, (40, 215, 1040, 1585), fill=WHITE, outline=ORANGE, w=6)
    pill(d, W / 2, 280, "THỬ NGHĨ", 56, WHITE, ORANGE)
    yb = 640
    rig(d, yb, 6.0, ruler=False)
    pull_arrow(d, yb, 6.0, "6 cm")
    text(d, (W / 2, 820), "Cùng lò xo, T = 2 s.", 60, INK)
    text(d, (W / 2, 905), "Kéo lệch 6 cm rồi thả.", 60, INK)
    text(d, (W / 2, 1020), "Quãng đường đi được", 64, DORANGE)
    text(d, (W / 2, 1105), "trong 2,0 s đầu?", 64, DORANGE)
    seg_bar(d, 1260, t, 0.8, sc["T"] - 0.2, ORANGE)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + REL, "tap")]
    out += [(do["t0"] + REL + i * RUN + (i - 1) * PAUSE, "tick") for i in (1, 2, 3)]
    out += [(da["t0"] + 2.4, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-motadddh-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Mô tả dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kéo lệch rồi thả", draw=s_hook, tail=0.3, caps=[
   ("O: chỗ vật đứng yên.", 4.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thả tay, ghi bốn mốc thời gian.", 4.6),
   ("Cột s cộng dồn đường đã đi.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Thả lại, xem tới đầu kia.", 4.0),
   ("Li độ âm, quãng đường vẫn dương.", 4.4),
   ("Mới thử một ca, bỏ ma sát.", 4.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Bẫy: hai lần qua O là một?", 3.6),
   ("Nhìn chiều đi của vật.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 6.6)]),
])
