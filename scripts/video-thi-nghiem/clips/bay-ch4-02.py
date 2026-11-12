# Clip bay phu dao L12 Ch.4 so 02 - Sau 2T con 1/4, khong phai het (topic_id 229 "Dinh luat phong xa va chu ki ban ra", lesson_topic 72).
# TU SOAN: chua co luot lam chuong 4 trong 60 ngay toi 12/11/2026 (lop chua hoc toi).
#   "Chat phong xa co T = 8 ngay. Sau 16 ngay, so hat nhan chua phan ra con lai bang..."
#   A. 0 (da phan ra het)  B. 1/4 so ban dau  C. 1/2 so ban dau  D. 3/4 so ban dau -> B.
# Kiem so: N = N0 . 2^(-t/T) = N0 . 2^(-16/8) = N0/4. Luoi 64 hat: sau 8 ngay con 32, sau 16 ngay con 16 (= 64/4).
#   Do thi: t = 24 ngay -> 1/8, t = 32 ngay -> 1/16 (> 0, khong cham truc).
# Nhieu: A = coi giam deu (mat 1/2 so BAN DAU moi T -> 2T het, duong thang do); C = coi 16 ngay la mot chu ki;
#   D = nham phan da phan ra (3/4) voi phan con lai.
# Cau THU NGHI: T = 5 ngay, 15 ngay -> con 1/8, da phan ra 7/8 (hoi phan DA phan ra: ca khac, khong hien tren man).
# Luoi hat la minh hoa trung binh (thuc te ngau nhien), chon hat phan ra bang Random(seed) co dinh.
from clips.bay_chung import *

QY = 830
Q_LINES = ["T = 8 ngày. Sau 16 ngày, số hạt nhân", "chưa phân rã còn lại là"]
OPTS = ["0 (đã phân rã hết)", "1/4 số ban đầu", "1/2 số ban đầu", "3/4 số ban đầu"]
ANS = 1
GX0, GY0, GS = 150, 330, 50          # luoi 8x8: goc trai tren, buoc
ORDER = list(range(64)); random.Random(12).shuffle(ORDER)
STEP1, STEP2 = set(ORDER[:32]), set(ORDER[32:48])   # phan ra sau 8 ngay / 8 ngay tiep


def grid(d, k1=0.0, k2=0.0, alpha=1.0):
    """k1, k2 (0..1): tien trinh phan ra cua dot 1 (0->8 ngay) va dot 2 (8->16 ngay); hat phan ra loang dan theo thu tu."""
    for i in range(64):
        x = GX0 + (i % 8) * GS; y = GY0 + (i // 8) * GS
        if i in STEP1: f = clamp(k1 * 1.6 - ORDER.index(i) / 32 * 0.6)
        elif i in STEP2: f = clamp(k2 * 1.6 - (ORDER.index(i) - 32) / 16 * 0.6)
        else: f = 0
        c = mix(ORANGE, LIGHT, f); r = 17 - 4 * f
        if f < 0.98: d.ellipse([x - r, y - r, x + r, y + r], fill=A(c, alpha))
        else: d.ellipse([x - 13, y - 13, x + 13, y + 13], outline=A(GRAY, alpha), width=3)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    grid(d)
    text(d, (760, 450), "64 hạt nhân", 44, ORANGE)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    grid(d, 1, 1)
    text(d, (760, 450), "Còn 16/64", 44, GREEN, alpha=appear(t, 0.5, 0.5))
    answer_pill(d, 1000, "B", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def graph(d, y, t, t0, k):
    ox, oy, sx, sy = 190, y + 600, 24.0, 400      # 1 ngay = 24 px (0..32 ngay), N0 = 400 px
    P = lambda day, n: (ox + day * sx, oy - n * sy)
    d.line([(ox, oy), (ox + 33 * sx + 20, oy)], fill=A(NAVY, k), width=4)
    d.line([(ox, oy), (ox, oy - sy - 50)], fill=A(NAVY, k), width=4)
    chevron(d, ox + 33 * sx + 20, oy, 0, A(NAVY, k)); chevron(d, ox, oy - sy - 50, -math.pi / 2, A(NAVY, k))
    text(d, (ox - 20, oy - sy - 40), "N", 40, NAVY, anchor="rm", alpha=k)
    text(d, (ox - 20, oy - sy), "N₀", 40, NAVY, anchor="rm", alpha=k)
    text(d, (ox + 33 * sx + 10, oy + 44), "t (ngày)", 36, NAVY, anchor="rm", alpha=k)
    for day in (8, 16, 24):
        d.line([P(day, 0), (P(day, 0)[0], oy + 12)], fill=A(NAVY, k), width=3)
        text(d, (P(day, 0)[0], oy + 44), str(day), 36, NAVY, alpha=k)
    # bay: giam deu (duong thang, het o 16 ngay) — net dut do, gach ✗
    kw = appear(t, t0 + 0.2, 0.4)
    if kw > 0:
        dash_line(d, P(0, 1), P(16, 0), A(RED, kw), w=5)
        text(d, (ox + 20, oy - 0.30 * sy), "✗ giảm đều", 38, RED, anchor="lm", alpha=kw)
    # dung: N = N0.2^(-t/T), ve dan theo t
    g = ease((t - (t0 + 1.0)) / 1.8); tmax = 32 * g
    if tmax > 0.2:
        pts = [P(u, 2 ** (-u / 8)) for u in [tmax * i / 80 for i in range(81)]]
        d.line(pts, fill=A(GREEN, k), width=7, joint="curve")
    for day, s in ((8, "1/2"), (16, "1/4")):
        if tmax >= day:
            x, yy = P(day, 2 ** (-day / 8))
            dash_line(d, (x, yy), (x, oy), A(GREEN, 0.6 * k), w=3)
            dot(d, x, yy, 11, A(GREEN, k))
            text(d, (x + 20, yy - 34), s, 44, GREEN, anchor="lm", alpha=k)


def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    k1 = ease((t - (m0 + 0.4)) / 1.0); k2 = ease((t - (m0 + 1.9)) / 1.0)
    grid(d, k1, k2)
    for j, (at, s, c) in enumerate(((0, "0 ngày: 64", INK), (m0 + 1.4, "8 ngày: 32", ORANGE), (m0 + 2.9, "16 ngày: 16", GREEN))):
        text(d, (580, 400 + j * 110), s, 44, c, anchor="lm", alpha=appear(t, at, 0.35))
    k = appear(t, m1 - 1.1, 0.45)                 # cong B: the hien som 1 s; do thi ve tu m1 - 0.6
    if k <= 0: return
    y = 820 + (1 - k) * 30
    card(d, (60, y, 1020, y + 760), fill=A(WHITE, k), outline=A(RED, k), w=5)
    text(d, (W / 2, y + 50), "Sai vì tưởng giảm đều", 42, RED, alpha=k)
    graph(d, y, t, m1 - 0.6, k)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Mỗi T: còn một nửa phần đang có",
             "T = 5 ngày. Sau 15 ngày, phần đã phân rã bằng bao nhiêu?")


CLIP = dict(id="bay-l12-ch4-02", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Định luật phóng xạ · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Mỗi chấm là một hạt nhân.", 3.0),
   ("Dừng lại, chọn một đáp án.", 5.4)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án B.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.9, caps=[
   ("Mỗi 8 ngày mất nửa phần đang có.", 3.6),
   ("Đường cong không chạm trục thời gian.", 3.8)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
