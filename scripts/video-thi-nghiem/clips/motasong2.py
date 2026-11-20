# Clip: tn-l11-motasong-02 - Day lo xo tren san: do buoc song, chu ki roi tinh toc do truyen song (lo 11, 20/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-motasong-02.json (_kiem_so() doi chieu mo_hinh v = sqrt(F/mu), lam = v/f):
#   mu = 0,5 kg/m, day 3 m, luc ke 10 N; so_lieu_mau (F N, v m/s, f Hz, lam m, T s):
#   (2; 2,0; 2; 1,0; 0,5) (2; 2,0; 3; 0,67; 0,33) (4,5; 3,0; 2; 1,5; 0,5) -> 3 lan do trong clip.
#   Quay 240 khung/giay: T = N/240 -> N = 120 (T = 0,5) va 80 (T ~ 0,33). Kho sua 20/11: F cu 8/18/32 N vuot luc ke 10 N.
# Bai l11-mo-ta-song (lesson 27): hop exp nam sau bang 5 dai luong, TRUOC khoi "song doi moi truong: f, T giu nguyen".
#   Tranh trung: Cau 1 (T 0,4 s, v 2,5 m/s -> lam = vT = 1 m), PhET (tang f / tang bien do / tang suc cang: clip khong noi
#   quy luat thanh chu, chi bang so), bai mau V (60 cm/s), Cau 2 (40 cm/s, 20 Hz), Cau 3 (suon truoc dinh), thu thach (T 0,4, lam 2).
# Du doan (K10): giu nhip gay, keo 2 N len 4,5 N: lam va T doi the nao? Dap an: lam dai ra (1,0 -> 1,5 m), T nhu cu (0,5 s).
# Bay = hien_tuong_hay_sai[2] "do lam bang hai dinh bat ki" -> hai dinh cach 2,0 m (x) vs hai dinh lien nhau 1,0 m (v).
# Chua noi duoc: chua doi do manh tay gay (cau PhET bo ngo).
# Thu nghi: keo 4,5 N, nhip gay nhanh hon, do lam = 0,75 m -> bao nhieu khung? (v = 3,0 nhu lan 4,5 N -> T = 0,25 s -> 60;
#   ghi trong ghi_chu kho). Can suy: v khong doi khi chi doi nhip (moi thay o 2 N), roi T = lam/v, N = 240T.
from engine import *

MU, LD, FPS_Q, SLOW = 0.5, 3.0, 240, 4.0          # kg/m, m, khung/giay quay cham, hien cham 4 lan
ROWS = [(2.0, 2.0, 2, 1.0, 0.5, 120), (2.0, 2.0, 3, 0.67, 1 / 3, 80), (4.5, 3.0, 2, 1.5, 0.5, 120)]   # F, v, f, lam, T, N
TXT = [("2", "120", "0,5", "1,0", "2,0"), ("2", "80", "≈ 0,33", "0,67", "2,0"), ("4,5", "120", "0,5", "1,5", "3,0")]
XD = 0.5                                             # diem dem khung (m)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-motasong-02.json")))
    hang = k["so_lieu_mau"]["hang"]; tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["mu"]["gia_tri"] == MU and tp["F"]["max"] <= 10
    for F_, v, f, lam, T, N in ROWS:
        assert any(r[0] == F_ and r[1] == v and r[2] == f and r[3] == lam and abs(r[4] - T) < 0.01 for r in hang), F_
        assert abs(math.sqrt(F_ / MU) - v) < 1e-9 and abs(v / f - lam) < 0.01 and abs(N / FPS_Q - T) < 1e-9
    g = k["so_lieu_mau"]["ghi_chu"]
    assert "Ca tự suy cho câu chốt clip motasong2" in g and "0,75 m" in g and "60 khung" in g
    assert abs(0.75 / 3.0 * FPS_Q - 60) < 1e-9 and tp["f"]["max"] >= 4          # chot: lam 0,75 m o 4,5 N -> 4 Hz
    assert not any(abs(r[3] - 0.75) < 1e-9 for r in hang)                       # so chot khong co tren bang
    assert any("10 N" in x["ten"] for x in k["dung_cu"])
_kiem_so()

# ---------------- day ----------------
XS, XE = 360, 1000                                   # 0 m -> 3 m
S = (XE - XS) / LD
YC = 530; AMP = 62
def env(x):
    e = 1 - 0.25 * x / LD
    if x > LD - 0.25: e *= ease((LD - x) / 0.25)
    return e
def u(x, tp, f, v, ka=1.0): return ka * AMP * env(x) * math.sin(2 * math.pi * f * (tp - x / v))
def crest_t(f, v, k=2): return XD / v + 0.25 / f + k / f          # thoi diem diem XD o dinh
def crests(tp, f, v):
    lam = v / f; x = v * (tp - 0.25 / f); x -= math.floor(x / lam) * lam
    out = []
    while x <= LD - 0.25: out.append(x); x += lam
    return out

def rope(d, yc, tp, f, v, ka=1.0, x0=XS, x1=XE, mark=True, hand=True):
    s = (x1 - x0) / LD; N = 180
    pts = [(x0 + s * LD * i / N, yc - u(LD * i / N, tp, f, v, ka)) for i in range(N + 1)]
    d.rectangle([x1, yc - 80, x1 + 26, yc + 80], fill=(150, 110, 70), outline=(100, 70, 40), width=3)   # gia co dinh
    d.line(pts, fill=BLUE, width=8, joint="curve")
    if hand:
        y0 = pts[0][1]
        d.line([(x0 - 34, yc), (x0, y0)], fill=BLUE, width=8)
        d.rounded_rectangle([x0 - 24, y0 - 30, x0 + 24, y0 + 30], radius=20, fill=(240, 196, 160), outline=(170, 110, 80), width=4)
    if mark:
        y = yc - u(XD, tp, f, v, ka); dot(d, x0 + XD * s, y, 15, RED, outline=WHITE)
    return pts

def lucke(d, Fv, yc=YC):
    Q = lambda s, h: (XS - 34 - s, yc + h)
    luc_ke(d, Q, 14, 40, 200, 10, Fv, nho=1, so=[], hw=38, co=56)
    d.rounded_rectangle([XS - 34 - 262, yc - 34, XS - 34 - 212, yc + 34], radius=20, fill=(240, 196, 160), outline=(170, 110, 80), width=4)

def ruler(d, y):
    d.line([(XS, y), (XE, y)], fill=NAVY, width=3)
    for k in range(7):
        x = XS + k * 0.5 * S; L = 20 if k % 2 == 0 else 11
        d.line([(x, y), (x, y + L)], fill=NAVY, width=3)
        if k % 2 == 0: text(d, (x, y + 50), str(k // 2), 58, INK)
    text(d, (XE + 45, y + 50), "m", 58, INK)

def fpill(d, Fs, a=1.0, ngan=False):
    s = f"F = {Fs} N" if ngan else f"Lực căng F = {Fs} N"
    pw = tw(d, s, F(56)) + 50
    card(d, (60, 300, 60 + pw, 370), fill=A((254, 242, 242), a), r=30)
    text(d, (60 + pw / 2, 335), s, 56, RED, alpha=a)

def stage(d, Fv, Fs, pill=True, ngan=False):
    card(d, (40, 260, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    ruler(d, 760); lucke(d, Fv)
    if pill: fpill(d, Fs, ngan=ngan)

def bracket(d, xa, xb, y, lab, a=1.0, col=ORANGE, tc=(176, 64, 8), below=True):
    pa, pb = XS + xa * S, XS + xb * S
    d.line([(pa, y), (pb, y)], fill=A(col, a), width=6)
    for p in (pa, pb): d.line([(p, y - 18), (p, y + 18)], fill=A(col, a), width=6)
    yy = y + 46 if below else y - 46
    pw = tw(d, lab, F(56)) + 30
    card(d, ((pa + pb) / 2 - pw / 2, yy - 32, (pa + pb) / 2 + pw / 2, yy + 32), fill=A(WHITE, a), r=14)
    text(d, ((pa + pb) / 2, yy), lab, 56, tc, alpha=a)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; F0, v, f = ROWS[0][0], ROWS[0][1], ROWS[0][2]
    stage(d, F0, "2", ngan=True)
    rope(d, YC, crest_t(f, v) + t / SLOW, f, v, ka=appear(t, 0.2, 0.8), mark=False)
    ka = appear(t, 0.8, 0.5)
    if ka > 0:
        text(d, (600, 670), "sóng chạy", 58, BLUE, alpha=ka)
        arrow(d, (740, 670), (900, 670), A(BLUE, ka), w=7, head=24)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 100), fill=A(PURPLE, a), r=36)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    for j, s in enumerate(("Giữ nhịp gảy, kéo căng", "từ 2 N lên 4,5 N.", "Bước sóng λ, chu kì T", "đổi thế nào?")):
        text(d, (W / 2, y0 + 175 + j * 80), s, 58, INK, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 490, 940, y0 + 506], radius=8, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 490, 140 + 800 * (1 - p), y0 + 506], radius=8, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
RUNS, HOLD = (0.6, 2.6, 0.6), 1.4                   # giay chay truoc khi dem (lan nhip nhanh chieu lau hon) ; giay dung hinh
def plan():
    out, s = [], 0.4
    for (F_, v, f, lam, T, N), run in zip(ROWS, RUNS):
        c = s + run; e = c + T * SLOW
        out.append((s, c, e)); s = e + HOLD
    return out
def do_state(t):
    """-> (i, tp, ka, so khung, dung hinh?, so hang da ghi, F kim)."""
    P = plan()
    if t < P[0][0]: return -1, 0.0, 0.0, 0, False, 0, ROWS[0][0]
    i = max(j for j, p in enumerate(P) if t >= p[0]); s, c, e = P[i]
    F_, v, f, lam, T, N = ROWS[i]
    fz = t >= e
    tp = crest_t(f, v) + (min(t, e) - c) / SLOW
    n = 0 if t < c else min(N, 8 * int(FPS_Q * (min(t, e) - c) / SLOW / 8 + 0.5))   # buoc 8 khung: khong hien 60 (dap so chot)
    ka = ease((t - s) / 0.5)
    rows = i + (1 if t >= e + 0.9 else 0)
    Fk = F_ if i == 0 else lerp(ROWS[i - 1][0], F_, ease((t - s) / 0.6))
    return i, tp, ka, n, fz, rows, Fk

def ntable(d, y, n, hl=()):
    card(d, (60, y, 1020, y + 96 + 3 * 76), fill=WHITE, outline=NAVY, w=4)
    xs = (140, 335, 535, 720, 910)
    for x, h in zip(xs, ("F (N)", "khung", "T (s)", "λ (m)", "v (m/s)")): text(d, (x, y + 48), h, 58, INK)
    d.line([(90, y + 92), (990, y + 92)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 132 + i * 76
        if i in hl: d.rounded_rectangle([80, yy - 33, 1000, yy + 33], radius=16, fill=(255, 237, 213))
        for j, (x, s) in enumerate(zip(xs, TXT[i])):
            text(d, (x, yy), s, 58, BLUE if j >= 3 else INK)

def s_do(img, d, t, sc):
    i, tp, ka, n, fz, rows, Fk = do_state(t)
    ii = max(i, 0); F_, v, f, lam, T, N = ROWS[ii]
    stage(d, Fk, TXT[ii][0])
    rope(d, YC, tp, f, v, ka=ka if i >= 0 else 0.0)
    # bo dem khung
    s = f"số khung = {n}"; pw = tw(d, s, F(56)) + 50
    card(d, (1020 - pw, 384, 1020, 450), fill=(239, 246, 255), r=30); text(d, (1020 - pw / 2, 417), s, 56, BLUE)
    text(d, (W / 2, 950), "quay 240 khung mỗi giây", 58, INK)
    if fz:
        a = appear(t, plan()[i][2] + 0.1, 0.3)
        cs = crests(tp, f, v); c0 = min(cs, key=lambda x: abs(x - XD))
        bracket(d, c0, c0 + lam, 630, "λ = " + TXT[i][3] + " m", a)
        text(d, (W / 2, 878), f"T = {N} : 240 {'≈' if N == 80 else '='} {TXT[i][2].replace('≈ ', '')} s", 56, INK, alpha=a)
    ntable(d, 1030, rows, hl=(rows - 1,))

def _kiem_dong_bo():
    """Moi 0,05 s: diem dem o dinh luc bat dau va ket thuc dem; so khung cuoi = N; hang ghi sau khi dung; khoang do = lam."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    for i, (s, c, e) in enumerate(plan()):
        F_, v, f, lam, T, N = ROWS[i]
        for tt in (c, e):
            ph = (2 * math.pi * f * (do_state(tt)[1] - XD / v)) % (2 * math.pi)
            if abs(ph - math.pi / 2) > 1e-6: bad.append((i, tt, "diem dem khong o dinh"))
        if do_state(e)[3] != N: bad.append((i, "so khung", do_state(e)[3]))
        cs = crests(do_state(e)[1], f, v); c0 = min(cs, key=lambda x: abs(x - XD))
        if abs(c0 - XD) > 1e-6 or c0 + lam > LD - 0.25: bad.append((i, "dinh do", cs))
    while t < sc["T"]:
        i, tp, ka, n, fz, rows, Fk = do_state(t)
        if rows > i + 1 or (i >= 0 and rows == i + 1 and not fz): bad.append((round(t, 2), "hang lech"))
        if fz and ka < 0.999: bad.append((round(t, 2), "bien do chua du"))
        t += 0.05
    if do_state(sc["T"] - 0.05)[5] != 3: bad.append("chua du 3 hang")
    if plan()[-1][2] + 0.9 > sc["T"] - 0.6: bad.append("hang cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=36)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: λ dài ra, T như cũ", 310, 1.0)
    card(d, (40, 380, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    for (F_, v, f, lam, T, N), yc, lab in ((ROWS[0], 490, "2 N"), (ROWS[2], 690, "4,5 N")):
        text(d, (120, yc), lab, 56, RED)
        rope(d, yc, crest_t(f, v) + t / SLOW, f, v, x0=230, x1=990, hand=False)
    ntable(d, 840, 3, hl=(0, 2))
    k2 = appear(t, M[1] + 0.3, 0.45)
    if k2 > 0:
        k3 = appear(t, M[1] + 2.4, 0.45); h = 170 if k3 <= 0 else 260
        card(d, (60, 1200, 1020, 1200 + h), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1265), "T theo nhịp tay gảy", 56, (21, 128, 61), alpha=k2)
        if k3 > 0: text(d, (W / 2, 1360), "λ: quãng sóng đi trong 1 T", 56, (21, 128, 61), alpha=k3)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; F_, v, f, lam, T, N = ROWS[0]
    stage(d, F_, "2", pill=False)
    tp = crest_t(f, v)                                  # hinh dung lai de do
    rope(d, YC, tp, f, v, mark=False)
    cs = crests(tp, f, v)                               # 0,5 ; 1,5 ; 2,5 m
    kb = appear(t, 0.3, 0.4)                            # hai cach do hien cung luc
    if kb > 0:
        bracket(d, cs[0], cs[2], 625, "2λ ✗", kb, col=RED, tc=RED)
        bracket(d, cs[0], cs[1], 420, "λ ✓", kb, col=GREEN, tc=(10, 80, 40), below=False)
    k3 = appear(t, M[1] + 0.9, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    y = 1040
    if a1 > 0:
        k2 = appear(t, 2.4, 0.4); h = 230 if k2 <= 0 else 320
        card(d, (40, y, 1040, y + h), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(56)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 102), fill=A(RED, a1), r=36)
        text(d, (W / 2, y + 64), "BẪY", 56, WHITE, alpha=a1)
        text(d, (W / 2, y + 170), "Sai: hai đỉnh bất kì", 58, RED, alpha=a1 * kb)
        if k2 > 0: text(d, (W / 2, y + 260), "Đúng: hai đỉnh liền nhau", 58, (10, 80, 40), alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 180), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 90), "Gảy mạnh (biên độ lớn): chưa đo", 58, INK, alpha=k3)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """THU NGHI: 4,5 N, nhip gay nhanh hon, lam = 0,75 m -> bao nhieu khung? (60: v = 3,0 nhu lan 4,5 N, T = 0,25 s)."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "λ: đo bằng thước", 58, (21, 128, 61), alpha=k0)
    text(d, (W / 2, 450), "T: đếm khung hình", 58, (21, 128, 61), alpha=k0)
    k1 = appear(t, M[0] + 2.1, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 5.4, 0.5); hb = 1290 if kh <= 0 else 1560
    card(d, (40, 600, 1040, hb), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 706), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 668), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    for j, s in enumerate(("Kéo 4,5 N, nhịp gảy nhanh hơn:", "λ = 0,75 m.", "Bao nhiêu khung?")):
        text(d, (W / 2, 790 + j * 80), s, 58, INK, alpha=k1)
    rope(d, 1150, 2 + t / SLOW, 4, 3.0, ka=k1, x0=150, x1=900, mark=False, hand=False)
    if kh > 0:
        card(d, (110, 1310, 970, 1530), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1420), "Lực căng như lần 4,5 N", 56, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + p[0], "tap") for p in plan()]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + e["M"][0] + 2.1, "open")]
    return out

CLIP = dict(id="tn-l11-motasong-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Mô tả sóng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Dây lò xo trên sàn", draw=s_hook, tail=0.3, caps=[
   ("Đầu phải buộc, tay gảy.", 3.8),
   ("Tự trả lời trước khi xem.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đếm khung: chấm đỏ đỉnh tới đỉnh.", 4.2),
   ("Đổi nhịp gảy, rồi đổi lực căng.", 8.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Hai chấm đỏ cùng nhịp.", 3.4),
   ("Vì sao λ đổi mà T không?", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy khi đo λ.", 4.2),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Tự trả lời trước gợi ý.", 7.6)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
