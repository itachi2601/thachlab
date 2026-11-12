# Clip bay phu dao L12 Ch.1 so 01 - Nuoc dang soi van giu 100 do C du van nhan nhiet (topic 196 "Nong chay, dong dac, hoa hoi,
# ngung tu", lesson_topic 57, bai l12-su-chuyen-the). Theo mau bay-ch3-01.
# Tinh huong TU SOAN kieu de Bo: cau that gan nhat (de 933 cau 1, question_index 0-based, 30/47 luot sai, 30 ngay toi 12/11/2026:
#   tron 100 g da 0 do C voi 100 g nuoc soi, chon do thi) can 4 hinh do thi nen khong dung nguyen van.
#   "Nuoc trong am dang soi o 100 do C (ap suat chuan). Dun them 2 phut thi nhiet do nuoc"
#   A. tang len tren 100 do C  B. van giu o 100 do C  C. giam dan duoi 100 do C  D. tang len roi giam -> B (thu tu goc, khong doi).
# Kiem vat li: o ap suat chuan nuoc soi o 100 do C; khi dang soi, nhiet nhan vao Q = L.m dung de hoa hoi (pha vo lien ket),
#   dong nang trung binh phan tu khong tang -> t khong doi cho toi khi can nuoc. Do thi t-tau: doan doc 20 -> 100 do C (tau 0 -> 3 phut,
#   so lieu minh hoa), roi doan NAM NGANG 100 do C (tau 3 -> 8 phut) trong khi bep van cap nhiet. Nhieu A = tuong "nhan nhiet thi nong len";
#   C = tuong "boc hoi lam lanh nuoc"; D = tron hai y. Khong co con so tinh toan nao khac.
from clips.bay_chung import *

BX0, BX1, BY0, BY1 = 190, 530, 450, 740   # coc nuoc
WL = 500                                    # mat nuoc
TX = 455                                    # nhiet ke cam trong nuoc
QY = 860
Q_LINES = ["Nước trong ấm đang sôi ở 100 °C", "(áp suất chuẩn). Đun thêm 2 phút", "thì nhiệt độ nước"]
OPTS = ["tăng lên trên 100 °C", "vẫn giữ ở 100 °C", "giảm dần dưới 100 °C", "tăng lên rồi giảm"]
ANS = 1
CW = (191, 219, 254)   # mau nuoc


def therm(d, temp, alpha=1.0):
    """Nhiet ke: bau trong nuoc, cot do theo temp (0..120 do C ung y 700..310)."""
    y_of = lambda v: 700 - v / 120 * 390
    d.rounded_rectangle([TX - 14, 290, TX + 14, 712], radius=14, fill=A(WHITE, alpha), outline=A(MUTED, alpha), width=4)
    d.ellipse([TX - 26, 690, TX + 26, 742], fill=A(RED, alpha), outline=A(MUTED, alpha), width=4)
    d.rectangle([TX - 6, y_of(temp), TX + 6, 700], fill=A(RED, alpha))
    yy = y_of(100); d.line([(TX + 14, yy), (TX + 30, yy)], fill=A(INK, alpha), width=4)
    # nhan nhiet do ben phai coc, nen trang
    s = f"{round(temp)} °C"; f = F(48); w = tw(d, s, f)
    d.rounded_rectangle([600, yy - 36, 600 + w + 40, yy + 36], radius=18, fill=A(WHITE, alpha), outline=A(RED, alpha), width=4)
    text(d, (620 + w / 2, yy), s, 48, RED, alpha=alpha)
    d.line([(TX + 30, yy), (600, yy)], fill=A(RED, 0.6 * alpha), width=3)


def flame(d, t, alpha=1.0):
    d.rounded_rectangle([170, 800, 550, 830], radius=10, fill=A(GRAY, alpha))
    for i in range(5):
        x = 225 + i * 68; h = 46 + 10 * math.sin(7 * t + i * 1.7)
        d.polygon([(x - 22, 798), (x + 22, 798), (x, 798 - h)], fill=A(ORANGE, alpha))
        d.polygon([(x - 10, 798), (x + 10, 798), (x, 798 - h * 0.55)], fill=A(YELLOW, alpha))


def beaker(d, t, alpha=1.0, steam=1.0):
    d.rectangle([BX0 + 5, WL, BX1 - 5, BY1 - 5], fill=A(CW, alpha))
    # bot khi noi len (tat dinh theo t)
    for i in range(9):
        ph = (t * 0.9 + i * 0.37) % 1.0
        x = BX0 + 40 + (i * 37) % (BX1 - BX0 - 120); y = BY1 - 20 - ph * (BY1 - WL - 30)
        r = 7 + 6 * ph
        d.ellipse([x - r, y - r, x + r, y + r], outline=A(WHITE, alpha), width=4)
    for x0, x1 in ((BX0, BX0), (BX1, BX1)):
        d.line([(x0, BY0), (x1, BY1)], fill=A(NAVY, alpha), width=7)
    d.line([(BX0, BY1), (BX1, BY1)], fill=A(NAVY, alpha), width=7)
    # hoi nuoc boc len
    if steam > 0:
        for i in range(3):
            ph = (t * 0.6 + i / 3) % 1.0; x = 225 + i * 70; y0 = WL - 20 - ph * 160
            pts = [(x + 14 * math.sin(j * 0.8 + t * 3), y0 - j * 8) for j in range(10)]
            d.line(pts, fill=A(GRAY, alpha * steam * (1 - ph)), width=6)


def scene_top(d, t, temp=100, alpha=1.0):
    flame(d, t, alpha); beaker(d, t, alpha); therm(d, temp, alpha)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    scene_top(d, t)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    scene_top(d, t)
    answer_pill(d, 1000, "B", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
GX0, GY0, GWD, GHT = 230, 1430, 700, 330    # goc do thi, rong, cao (trong the)


def gpt(tau, tc): return GX0 + tau / 8 * GWD, GY0 - tc / 120 * GHT


def graph(d, t, sc, k):
    m0, m1 = sc["M"]
    y = 860 + (1 - k) * 30; dy = y - 860
    card(d, (60, y, 1020, y + 680), fill=A(WHITE, k), outline=A(RED, k), w=5)
    text(d, (W / 2, y + 50), "Sai vì nghĩ nhận nhiệt là nóng lên", 40, RED, alpha=k)
    ox, oy = GX0, GY0 + dy
    d.line([(ox, oy), (ox + GWD + 30, oy)], fill=A(INK, k), width=4); chevron(d, ox + GWD + 30, oy, 0, A(INK, k), s=20, w=4)
    d.line([(ox, oy), (ox, oy - GHT - 40)], fill=A(INK, k), width=4); chevron(d, ox, oy - GHT - 40, -math.pi / 2, A(INK, k), s=20, w=4)
    text(d, (ox + 20, oy - GHT - 40), "t (°C)", 36, INK, anchor="lm", alpha=k)
    text(d, (ox + GWD + 30, oy + 44), "τ (phút)", 36, INK, anchor="rm", alpha=k)
    for v in (20, 100):
        yy = oy - v / 120 * GHT
        d.line([(ox - 10, yy), (ox, yy)], fill=A(INK, k), width=4)
        text(d, (ox - 18, yy), str(v), 36, INK, anchor="rm", alpha=k)
    # doan doc (dang nong len) ve dan
    g1 = ease((t - (m0 + 0.6)) / 1.2)
    p0 = gpt(0, 20); p1 = gpt(3, 100)
    if g1 > 0:
        d.line([(p0[0], p0[1] + dy), (lerp(p0[0], p1[0], g1), lerp(p0[1], p1[1], g1) + dy)], fill=A(BLUE, k), width=8)
    # bay: duong do net dut tiep tuc doc len (tuong nhan nhiet la nong len), roi gach
    kb = appear(t, m0 + 1.9, 0.5) * (1 - 0.7 * appear(t, m1 + 0.3, 0.4))
    if kb > 0:
        pe = gpt(3.8, 125)
        dash_line(d, (p1[0], p1[1] + dy), (pe[0], pe[1] + dy), A(RED, kb), w=6)
        text(d, (pe[0] + 40, pe[1] + dy + 10), "✗", 48, RED, alpha=kb)
    # doan dung: nam ngang 100 do C trong khi van dun
    g2 = ease((t - (m1 + 0.2)) / 1.4)
    if g2 > 0:
        p2 = gpt(3 + 5 * g2, 100)
        d.line([(p1[0], p1[1] + dy), (p2[0], p2[1] + dy)], fill=A(GREEN, k), width=9)
    k3 = appear(t, m1 + 1.0, 0.45)
    if k3 > 0:
        cx = gpt(5.5, 100)[0]
        text(d, (cx + 40, gpt(0, 100)[1] + dy + 50), "đang sôi", 40, GREEN, alpha=k3 * k)
        text(d, (W / 2, y + 125), "Q nhận vào dùng để hoá hơi", 40, INK, alpha=k3 * k)


def s_saivi(img, d, t, sc):
    scene_top(d, t)
    kB = appear(t, sc["M"][0] + 0.4, 0.4)
    badge(d, 820, 800, "bếp vẫn đun", ORANGE, kB, size=36)
    graph(d, t, sc, appear(t, sc["M"][0] + 0.1, 0.45))


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Đang sôi: nhiệt nhận vào dùng để hoá hơi",
             "Đá đang tan ở 0 °C, vẫn đun tiếp. Nhiệt độ thay đổi thế nào?")


CLIP = dict(id="bay-l12-ch1-01", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Sự chuyển thể · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Nước đang sôi, bếp vẫn cháy.", 2.8),
   ("Chọn một đáp án.", 5.4)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án B.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.9, caps=[
   ("Nước nóng dần tới lúc sôi.", 3.0),
   ("Sôi rồi: nhiệt độ đứng yên.", 4.2)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
