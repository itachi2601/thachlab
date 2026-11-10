# Clip: tn-l11-tatdan-03 - Xich du: ngoi yen va nhun dung luc (vi_du, hoat canh minh hoa) (9/11/2026, chang B L11 Dao dong)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-tatdan-03.json:
#   tham_so: A0 = 40 cm (bien do tren cung, 20-60 buoc 5) ; beta = 0,08 /s ; T = 2,0 s.
#   so_lieu_mau (nhip n: ngoi yen / nhun): 0 40,0/40,0 ; 1 34,1/40,0 ; 2 29,0/40,0 ; 3 24,8/40,0.
#   gia_thiet: "beta = 0,08 chi de minh hoa" -> ghi "minh hoa" tren man. Luc nhun cung chieu, chi mot phan chu ki.
#   goi_y_mo_phong: hai mui ten song song (chieu di + luc nhun). hien_tuong_hay_sai[1]: "nhun luc nao cung cao" -> Bay.
#   Ve: day 300 px ung ~1 m (T = 2 s), 40 cm tren cung -> goc 0,40 rad.
# Doan ngay sau hop trong bai: cau tu kiem ve dong ho qua lac (dap an "moi nhip chi bu phan da mat; chu ki van la chu ki
#   rieng"; nhieu A "day lien tuc nhu luc cuong buc") -> clip KHONG dung bay "luc cuong buc lien tuc" (hien_tuong_hay_sai[0]),
#   khong noi "chu ki rieng" thanh quy tac chung; chi quan sat "hai du cung 2 s moi nhip".
# Cau chot (sua sau cong B 9/11): tha tu 30 cm (tham_so A0, chua tung hien), NGOI YEN -> sau 3 nhip con khoang bao nhieu?
#   Dung mo hinh kho A_n = A0 e^(-0,16 n): 30 e^(-0,48) = 18,6 cm (= 30 . 24,8/40; khong hien tren man). Khac ca Du doan (nhun).
#   Bo dong 'moi nhip 2 s' o canh Ket qua (tra loi san cau dong ho qua lac sau hop).
from engine import *

A0, BETA, PER = 40.0, 0.08, 2.0
ROWS = [(0, 40.0, 40.0), (1, 34.1, 40.0), (2, 29.0, 40.0), (3, 24.8, 40.0)]
def fs(v): return f"{v:.1f}".replace(".", ",")
def th_amp(acm): return acm / 100.0             # rad, day ~1 m

# ---------------- hai xich du ----------------
CXL, CXR, PY, LR = 280, 800, 370, 300
def theta(t, push):
    a = A0 if push else A0 * math.exp(-BETA * max(0.0, t))
    return th_amp(a) * math.cos(2 * math.pi * t / PER)
def dtheta(t, push):
    a = A0 if push else A0 * math.exp(-BETA * max(0.0, t))
    return -th_amp(a) * (2 * math.pi / PER) * math.sin(2 * math.pi * t / PER)

def frame_(d, cx, a=1.0):
    c = lambda col: A(col, a)
    d.line([(cx - 230, PY), (cx + 230, PY)], fill=c(NAVY), width=8)
    d.line([(cx - 200, PY), (cx - 250, PY + 420)], fill=c(NAVY), width=6)
    d.line([(cx + 200, PY), (cx + 250, PY + 420)], fill=c(NAVY), width=6)
    d.line([(cx - 260, PY + 422), (cx + 260, PY + 422)], fill=c((150, 120, 80)), width=4)

def swing(d, cx, th, col, a=1.0, pump=0.0):
    """Du + nguoi ngoi (dau, than, tay nam day, dui, cang chan). pump 0..1: nga nguoi ra sau, duoi chan khi nhun."""
    c = lambda cl: A(cl, a)
    ux, uy = math.sin(th), math.cos(th)                      # doc day, huong xuong
    fx, fy = math.cos(th), -math.sin(th)                     # vuong goc day (phia truoc nguoi)
    sx_, sy_ = cx + LR * ux, PY + LR * uy
    d.line([(cx, PY), (sx_, sy_)], fill=c(INK), width=4)
    d.line([(sx_ - 40 * fx, sy_ - 40 * fy), (sx_ + 40 * fx, sy_ + 40 * fy)], fill=c((120, 80, 40)), width=12)
    hip = (sx_ - 12 * ux, sy_ - 12 * uy)
    sh = (hip[0] - 72 * ux - pump * 24 * fx, hip[1] - 72 * uy - pump * 24 * fy)
    hd = (sh[0] - 30 * ux - pump * 10 * fx, sh[1] - 30 * uy - pump * 10 * fy)
    hand = (cx + (LR - 105) * ux, PY + (LR - 105) * uy)
    knee = (hip[0] + 50 * fx, hip[1] + 50 * fy)
    ang = 0.15 + pump * 1.1                                  # cang chan: tu thong xuong toi duoi ra truoc
    foot = (knee[0] + 55 * (ux * math.cos(ang) + fx * math.sin(ang)), knee[1] + 55 * (uy * math.cos(ang) + fy * math.sin(ang)))
    d.line([hip, sh], fill=c(col), width=16)
    d.line([sh, hand], fill=c(col), width=9)
    d.line([hip, knee, foot], fill=c(col), width=11, joint="curve")
    dot(d, hd[0], hd[1], 20, c(col), outline=c(WHITE))
    return sx_, sy_

def peak_marks(d, cx, upto, a=1.0):
    """Cham dinh cua du ngoi yen o moi lan doi chieu (moi nua chu ki) da qua."""
    k = 0
    while k * PER / 2 <= upto + 1e-6:
        th = theta(k * PER / 2, False)
        x, y = cx + (LR + 30) * math.sin(th), PY + (LR + 30) * math.cos(th)
        if upto - k * PER / 2 > 0.3: dot(d, x, y, 6, A(BLUE, a))   # bo cham trung vi tri du hien tai
        k += 1

def push_arrows(d, cx, t, sx_, sy_, a=1.0):
    th, om = theta(t, True), dtheta(t, True)
    if th * om >= 0 or abs(th) < 0.03: return        # chi khi dang di xuong (goc giam ve 0)
    s = 1 if om > 0 else -1
    tx, ty = s * math.cos(th), -s * math.sin(th)      # tiep tuyen theo chieu chuyen dong
    nx, ny = -ty, tx
    for off, col, L in ((26, GREEN, 110), (-26, ORANGE, 110)):
        p1 = (sx_ + nx * off, sy_ + ny * off + 30)
        arrow(d, p1, (p1[0] + tx * L, p1[1] + ty * L), A(col, a), w=7, head=22)

def rig(d, t, a=1.0, run=True):
    frame_(d, CXL, a); frame_(d, CXR, a)
    tl = t if run else 0.0
    if run: peak_marks(d, CXL, tl, a)
    swing(d, CXL, theta(tl, False), BLUE, a)
    th, om = theta(tl, True), dtheta(tl, True)
    pump = clamp(-th * om / (th_amp(A0) ** 2 * math.pi / 2)) if run else 0.0   # 0..1, chi khi di xuong
    sx_, sy_ = swing(d, CXR, th, ORANGE, a, pump)
    if run: push_arrows(d, CXR, tl, sx_, sy_, a)
    text(d, (CXL, 830), "Ngồi yên", 42, BLUE, alpha=a)
    text(d, (CXR, 830), "Nhún đúng lúc", 42, ORANGE, alpha=a)

# ---------------- bieu do cot bien do theo nhip (truc co dinh) ----------------
BASE, HS = 1440, 9.0                 # 1 cm = 9 px -> 40 cm = 360 px
GXS = (300, 500, 700, 900)
def bars(d, nshow, a=1.0, labels=True):
    d.line([(160, BASE), (1000, BASE)], fill=A(NAVY, a), width=4)
    text(d, (60, 960), "biên độ (cm)", 40, INK, anchor="lm", alpha=a)
    text(d, (100, BASE + 46), "nhịp", 40, INK, alpha=a)
    for (n, al, ap), x in zip(ROWS, GXS):
        text(d, (x, BASE + 46), str(n), 40, INK, alpha=a)
        if n >= nshow: continue
        for v, col, dx in ((al, BLUE, -46), (ap, ORANGE, 46)):
            h = v * HS
            if h > 2: d.rounded_rectangle([x + dx - 38, BASE - h, x + dx + 38, BASE], radius=8, fill=A(col, a))
            if labels and n > 0: text(d, (x + dx, BASE - h - 30), fs(v), 38, col, alpha=a)
        if labels and n == 0: text(d, (x, BASE - al * HS - 30), fs(al), 40, INK, alpha=a)   # hai cot bang nhau: mot nhan

def tag(d):
    """Nhan 'minh hoa' goc phai tren, suot clip (vi_du, so khong do that)."""
    card(d, (850, 208, 1030, 252), fill=(255, 237, 213), r=22)
    text(d, (940, 230), "minh hoạ", 36, ORANGE)

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.85, cx + pw / 2, cy + size * 0.85), fill=A(bg, a), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi) ----------------
def s_hook(img, d, t, sc):
    tag(d)
    M = sc["M"]
    rig(d, 0.0, run=False)
    pill(d, W / 2, 290, "thả từ 40 cm", 40, WHITE, NAVY, appear(t, 0.3, 0.4))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 40, WHITE, PURPLE, a)
    ctext(d, y0 + 180, "Nhún cùng chiều chuyển động.", 42, MUTED, maxw=930, alpha=a)
    ctext(d, y0 + 350, "Sau 3 nhịp, đu lần hai\ncao cỡ nào?", 52, INK, maxw=930, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 530, 940, y0 + 542], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 530, 140 + 800 * (1 - p), y0 + 542], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
REL = 1.0
def s_do(img, d, t, sc):
    tag(d)
    ts = clamp(t - REL, 0, 3 * PER)
    rig(d, ts, run=t >= REL)
    n = min(3, int(ts / PER + 1e-6))
    pill(d, W / 2, 290, f"t = {ts:.0f} s", 40, WHITE, NAVY)
    ka = appear(t, REL + 0.6, 0.4)
    arrow(d, (150, 900), (230, 900), A(GREEN, ka), w=7, head=20); text(d, (250, 900), "chiều đi", 40, GREEN, anchor="lm", alpha=ka)
    arrow(d, (560, 900), (640, 900), A(ORANGE, ka), w=7, head=20); text(d, (660, 900), "lực nhún", 40, ORANGE, anchor="lm", alpha=ka)
    nshow = 0 if t < REL else 1 + n
    bars(d, nshow)

# ---------------- canh 3: Dap an + Rut ra + Chua noi duoc ----------------
def s_dapan(img, d, t, sc):
    tag(d)
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    pill(d, W / 2, 290, "ĐÁP ÁN · giữ độ cao", 40, WHITE, NAVY, ka)
    kr = appear(t, M[0] + 0.6, 0.45)
    if kr > 0:
        card(d, (60, 400, 1020, 560), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=24, w=4)
        ctext(d, 480, "Nhún bù phần ma sát lấy đi", 50, (21, 110, 55), maxw=900, alpha=kr)
    kn = appear(t, M[1] - 0.05, 0.45)
    if kn > 0:
        card(d, (60, 620, 1020, 840), fill=A(WHITE, kn), outline=A(NAVY, kn), r=24, w=5)
        text(d, (W / 2, 675), "Chưa nói được", 46, NAVY, alpha=kn)
        text(d, (W / 2, 770), "• Nhún mạnh hơn thì sao?", 46, INK, alpha=kn * appear(t, M[1] + 0.3, 0.4))
    bars(d, 4, labels=True)

# ---------------- canh 4: Bay - "nhun luc nao cung cao them" ----------------
def s_bay(img, d, t, sc):
    tag(d)
    M = sc["M"]
    y0 = 300
    card(d, (40, y0, 1040, y0 + 330), fill=WHITE, outline=(185, 28, 28), w=6)
    pill(d, W / 2, y0 + 62, "BẪY", 40, WHITE, (185, 28, 28))
    q = "✗ “Nhún lúc nào cũng cao thêm”"
    f = F(46); lw = tw(d, q, f); yy = y0 + 200
    text(d, (W / 2, yy), q, 46, (185, 28, 28))
    ks = clamp((t - (M[1] + 2.0)) / 0.4)
    if ks > 0:
        d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=(140, 15, 15), width=7)
    # so do cung du (goc ve phong dai, khong co so). Soat 10/11 (xem mp4): ban cu ghi "Chi nhun khi di xuong" + "khong nhun"
    #   o nua di len -> sai vat li (luc cung chieu van tang nang luong ca luc di len) va mau thuan o "Chua noi duoc".
    #   Ban moi: du di tu bien phai sang trai (mui ten xam ngoai cung = chieu di); trong cung: nhun CUNG chieu (cam, them)
    #   va nhun NGUOC chieu (do, bot) -> bac "luc nao cung cao them" bang dau cong cua luc so voi chieu di.
    cx, cy, R = W / 2, 650, 440
    kb = appear(t, 0.3, 0.4)
    th0 = 0.85
    RED = (185, 28, 28)
    def P(th, r=R): return (cx + r * math.sin(th), cy + r * math.cos(th))
    arc = [P(th0 - 2 * th0 * i / 80) for i in range(81)]          # bien phai -> bien trai
    dot(d, cx, cy, 10, A(NAVY, kb))
    d.line([(cx, cy), P(th0)], fill=A(INK, kb * 0.6), width=4)
    d.line(arc, fill=A(GRAY, kb), width=12)
    # chieu di (xam, ngoai cung), hien ngay khi phu de len
    for a0, a1 in ((0.70, 0.35), (-0.15, -0.50)):
        arrow(d, P(a0, R + 50), P(a1, R + 50), A(GRAY, kb), w=8, head=26)
    card(d, (P(th0)[0] - 40, P(th0)[1] - 8, P(th0)[0] + 40, P(th0)[1] + 8), fill=A((120, 80, 40), kb), r=6)
    kt = appear(t, M[1] + 2.0, 0.4)
    if kt > 0:
        arrow(d, P(0.62, R - 60), P(0.22, R - 60), A(ORANGE, kt), w=10, head=30)      # cung chieu di
        arrow(d, P(-0.62, R - 60), P(-0.22, R - 60), A(RED, kt), w=10, head=30)       # nguoc chieu di
        text(d, (P(0.40)[0] + 20, 1150), "cùng chiều", 40, ORANGE, alpha=kt)
        text(d, (P(-0.40)[0] - 20, 1150), "ngược chiều", 40, RED, alpha=kt)
    kc = appear(t, M[1] + 2.4, 0.5)
    if kc > 0:
        card(d, (60, 1220, 1020, 1390), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=24, w=4)
        text(d, (W / 2, 1305), "✓ Ngược chiều: bớt độ cao", 48, (21, 110, 55), alpha=kc)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    tag(d)
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 290, 1020, 510), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Nhún đúng lúc\ngiữ độ cao", 48, GREEN, maxw=900, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 570, 1040, 1180), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 600, W / 2 + pw / 2, 664), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 632), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 790, "Thả từ 30 cm, ngồi yên.\nSau 3 nhịp còn khoảng bao nhiêu?",
          48, INK, maxw=930, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
    if kh > 0:
        card(d, (110, 940, 970, 1140), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 990), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1075), "Mỗi nhịp giảm cùng một tỉ lệ", 44, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]
    out += [(do["t0"] + REL + k * PER, "tap") for k in range(4)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-tatdan-03", header="VẬT LÍ 11 · VÍ DỤ", footer="Tắt dần · duy trì · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai lần trên xích đu", draw=s_hook, tail=0.6, caps=[
   ("Lần một ngồi yên, lần hai nhún.", 3.4),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Hai lần làm, đặt cạnh nhau.", 3.6),
   ("Ghi biên độ sau mỗi nhịp.", 4.1)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So cột xanh với cột cam.", 5.0),
   ("Mới thử nhún đúng lúc.", 5.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: nhún lúc nào cũng được?", 3.0),
   ("Có đúng không?", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.2)]),
])
