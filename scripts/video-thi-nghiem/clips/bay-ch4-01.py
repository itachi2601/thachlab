# Clip bay phu dao L12 Ch.4 so 01 - Nang luong lien ket khac nang luong lien ket rieng (topic_id 224, lesson_topic 70).
# TU SOAN: chua co luot lam chuong 4 trong 60 ngay toi 12/11/2026 (lop chua hoc toi). Kieu de Bo 2025-2026 "hat nhan cang ben neu...".
#   "X: 235 nuclon, W_lk = 1784 MeV; Y: 56 nuclon, W_lk = 492 MeV. Hat nhan nao ben hon?"
#   A. X, vi nang luong lien ket lon hon  B. X, vi nhieu nuclon hon  C. Y, vi nang luong lien ket rieng lon hon
#   D. Y, vi it nuclon hon -> C. (Cong B vong 1: phuong an viet bang chu, chi so lk/lkr tu ve >= 36 px bang richb.)
# Kiem so: W_lkr X = 1784/235 = 7,5915 ~ 7,59 MeV/nuclon; W_lkr Y = 492/56 = 8,7857 ~ 8,79 MeV/nuclon -> Y ben hon.
#   (So lieu gan dung U-235: 1783,9 MeV; Fe-56: 492,3 MeV — khong ghi ten nguyen to tren man.)
#   Cau THU NGHI: Z 4 nuclon, 28,3 MeV -> 28,3/4 = 7,07 < 8,79 (kem Y); khong so nao cua Z hien tren man ngoai de.
# Nhieu: A = so W_lk tong (bay chinh); B = nhieu nuclon nen "chac" hon; D = hat nhan nho thi ben (dung ket qua, sai ly do).
# Hinh: thanh W_lk (thang 0,22 px/MeV: X 392 px, Y 108 px) -> vach chia deu cho tung nuclon -> thanh W_lkr
#   (thang 300 px ung 8,79: X 259 px, Y 300 px).
from clips.bay_chung import *

QY = 830
Q_LINES = ["Hạt nhân nào bền hơn?"]
OPTS = ["X, vì năng lượng liên kết lớn hơn", "X, vì nhiều nuclôn hơn",
        "Y, vì năng lượng liên kết riêng lớn hơn", "Y, vì ít nuclôn hơn"]
ANS = 2
NUC = (("X", 235, 92, 300, 510, 150), ("Y", 56, 26, 790, 540, 150 * math.sqrt(56 / 235)))
WLK = {"X": 1784, "Y": 492}
WLKR = {k: WLK[k] / n for k, n, *_ in NUC}           # 7,59 ; 8,79
SC1 = 0.22                                           # px / MeV (thanh W_lk)
SC2 = 300 / WLKR["Y"]                                # px / (MeV/nuclon)


def richb(d, cx, cy, base, sub, tail, size, color, alpha=1.0):
    """Ky hieu co chi so duoi tu ve: chi so >= 36 px (rich() cua engine chi 0,6 x co chu). Can giua tai cx."""
    fs = max(36, int(size * 0.78)); f, g = F(size), F(fs)
    wt = tw(d, base, f) + tw(d, sub, g) + tw(d, tail, f); x = cx - wt / 2
    dtext(d, (x, cy), base, f, color, alpha, "lm"); x += tw(d, base, f)
    dtext(d, (x, cy + size * 0.32), sub, g, color, alpha, "lm"); x += tw(d, sub, g)
    dtext(d, (x, cy), tail, f, color, alpha, "lm")


def qcard_r(d, t, sc, y0, lines, opts, think_at, think_end, k=1.0):
    """Nhu qcard (bay_chung) nhung lua chon ve bang rich() (chi so duoi). Cung mau/co/kieu cho ca 4."""
    if k <= 0: return
    nq = len(lines); h = 110 + nq * 50 + len(opts) * 70 + 40
    y = y0 + (1 - k) * 40
    card(d, (60, y, 1020, y + h), fill=A(WHITE, k), outline=A(PURPLE, k), w=5)
    for j, s in enumerate(lines):
        text(d, (W / 2, y + 60 + j * 50), s, 42, INK, alpha=k)
    yo = y + 60 + nq * 50 + 50
    for j, s in enumerate(opts):
        yy = yo + j * 70
        d.rounded_rectangle([100, yy - 28, 980, yy + 28], radius=28, outline=A(LIGHT, k), width=3)
        rich(d, 134, yy, f"{'ABCD'[j]}.  {s}", 40, NAVY, alpha=k, anchor="l")
    q = clamp((t - think_at) / max(0.1, think_end - think_at))
    if t >= think_at - 0.3:
        yb = y + h - 26
        d.rounded_rectangle([140, yb - 5, 940, yb + 5], radius=5, fill=A(LIGHT, k))
        if q < 1: d.rounded_rectangle([140, yb - 5, 140 + 800 * (1 - q), yb + 5], radius=5, fill=A(PURPLE, k))


def pill_r(d, y, letter, s, k):
    if k <= 0: return
    yy = y + (1 - k) * 30
    d.rounded_rectangle([100, yy - 46, 980, yy + 46], radius=46, fill=A(mix(GREEN, WHITE, 0.85), k), outline=A(GREEN, k), width=5)
    rich(d, 150, yy, f"{letter}.  {s}", 46, GREEN, alpha=k, anchor="l")
    text(d, (940, yy), "✓", 52, GREEN, anchor="rm", alpha=k)


def nucleus(d, cx, cy, R, n, z, alpha=1.0, seed=3):
    """Hat nhan ve bang n qua cau xep kieu hoa huong duong; z qua do (proton), con lai xam (notron)."""
    rnd = random.Random(seed); prot = set(rnd.sample(range(n), z)); r = R * math.sqrt(1 / n) * 0.98
    for i in range(n - 1, -1, -1):
        rr = R * math.sqrt((i + 0.5) / n); th = i * 2.39996
        x, y = cx + rr * math.cos(th), cy + rr * math.sin(th)
        c = RED if i in prot else GRAY
        d.ellipse([x - r, y - r, x + r, y + r], fill=A(mix(c, WHITE, 0.15), alpha), outline=A(mix(c, NAVY, 0.4), alpha), width=1)


def nuclei(d, alpha=1.0):
    for name, n, z, cx, cy, R in NUC:
        nucleus(d, cx, cy, R, n, z, alpha, seed=n)
        text(d, (cx, 712), f"{name}: {n} nuclôn", 40, INK, alpha=alpha)
        richb(d, cx, 768, "W", "lk", f" = {WLK[name]} MeV", 40, ORANGE, alpha=alpha)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    nuclei(d)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    nuclei(d)
    answer_pill(d, 1000, "C", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
BASE1 = 700


def bars_total(d, t, m0):
    richb(d, 640, 340, "W", "lk", "", 46, ORANGE)
    ks = appear(t, m0 + 1.2, 0.6)                     # vach chia deu cho tung nuclon
    for name, n, z, cx, cy, R in NUC:
        h = WLK[name] * SC1; x0, x1 = cx - 70, cx + 70
        d.rectangle([x0, BASE1 - h, x1, BASE1], fill=A(mix(ORANGE, WHITE, 0.55), 1), outline=A(ORANGE, 1), width=4)
        if ks > 0:
            step = h / n
            for i in range(1, n):
                yy = BASE1 - i * step
                d.line([(x0 + 3, yy), (x1 - 3, yy)], fill=A(ORANGE, 0.55 * ks), width=1)
            pw = tw(d, f"÷ {n}", F(36)) + 48
            badge(d, x1 + 20 + pw, BASE1 - h / 2 if name == "X" else BASE1 - 70, f"÷ {n}", ORANGE, ks, size=36)
        text(d, (cx, BASE1 - h - 32), f"{WLK[name]} MeV", 40, ORANGE)
        text(d, (cx, BASE1 + 36), name, 40, INK)
    d.line([(180, BASE1), (900, BASE1)], fill=A(NAVY, 1), width=4)


def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    bars_total(d, t, m0)
    m1 = m1 - 1.0                                  # cong B: the Sai vi hien som 1 s (moi moc ben duoi tinh tu day)
    k = appear(t, m1 - 0.1, 0.45)
    if k <= 0: return
    y = 800 + (1 - k) * 30
    card(d, (60, y, 1020, y + 790), fill=A(WHITE, k), outline=A(RED, k), w=5)
    text(d, (W / 2, y + 46), "Sai: chưa chia cho số nuclôn", 42, RED, alpha=k)
    richb(d, W / 2 - 75, y + 125, "W", "lkr", " =", 48, GREEN, alpha=k)
    richb(d, W / 2 + 75, y + 125, "W", "lk", " : A", 48, GREEN, alpha=k)
    g = ease((t - (m1 + 0.5)) / 1.2)               # thanh W_lkr moc len
    base = y + 560
    for name, n, z, cx, cy, R in NUC:
        h = WLKR[name] * SC2 * g
        if h > 2:
            d.rectangle([cx - 70, base - h, cx + 70, base], fill=A(mix(GREEN, WHITE, 0.6), k), outline=A(GREEN, k), width=4)
        text(d, (cx, base + 40), f"{name} ({n})", 40, INK, alpha=k)
    d.line([(180, base), (900, base)], fill=A(NAVY, k), width=4)
    kv = appear(t, m1 + 1.8, 0.4)                  # so lieu + ket luan hien cung luc khi thanh dung han
    for name, n, z, cx, cy, R in NUC:
        text(d, (cx, base - WLKR[name] * SC2 - 34), f"{WLKR[name]:.2f}".replace(".", ","), 44, GREEN, alpha=kv)
    text(d, (W / 2, base + 100), "MeV/nuclôn", 40, INK, alpha=kv)
    if kv > 0:
        pw = tw(d, "Y bền hơn", F(40)) + 48
        badge(d, W / 2 + pw / 2, y + 730, "Y bền hơn", GREEN, kv, size=40)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Độ bền: so năng lượng liên kết riêng",
             "Z có 4 nuclôn, năng lượng liên kết 28,3 MeV. Z bền hơn Y không?")


CLIP = dict(id="bay-l12-ch4-01", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Năng lượng liên kết · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Hai hạt nhân X, Y.", 3.0),
   ("Dừng lại, chọn một đáp án.", 6.2)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án C.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.9, caps=[
   ("Tổng lớn chưa chắc bền hơn.", 3.2),
   ("Chia đều cho từng nuclôn rồi so.", 4.2)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.4)]),
])
