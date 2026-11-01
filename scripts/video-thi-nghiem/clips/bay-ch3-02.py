# Clip bay phu dao L12 Ch.3 so 02 - Luc tu tac dung len khung day. Ngau luc tu (topic_id 234). Theo mau bay-ch3-01.
# Tinh huong = de 1056 cau 6 (Kiem tra nhanh Bai 10), 38/54 luot sai (70 %) trong 30 ngay:
#   "Mot khung day chu nhat mang dong dien dat trong tu truong deu. Luc tu tac dung len hai canh doi dien cua khung tao
#    thanh ngau luc vi hai luc do" A. cung do lon, cung chieu, cung gia  B. khac do lon, nguoc chieu, cung gia
#    C. cung do lon, nguoc chieu, cung gia  D. cung do lon, nguoc chieu, khac gia -> D.
# Hinh NHIN TU TREN XUONG: B sang phai; khung (mat phang dung) thanh mot doan qua truc quay O; hai canh dung la hai cham:
#   canh trai I ra khoi mat phang (cham), canh phai I vao (X). F = Il x B: ra x phai = LEN, vao x phai = XUONG.
#   -> khung quay cung chieu kim dong ho tren man hinh; luc luon vuong goc B (thang dung) du khung quay.
from clips.bay_chung import *

PY0, PY1 = 330, 760
LINES_Y = (390, 470, 620, 700)       # bo duong y = 545 de khong de len truc quay
OX, OY, R = 540, 545, 210            # truc quay O, nua chieu rong khung
FL = 120                             # do dai mui ten luc
QY = 830
Q_LINES = ["Lực từ lên hai cạnh đối diện khung", "là ngẫu lực vì chúng…"]
OPTS = ["bằng nhau, cùng chiều, cùng giá", "không bằng nhau, ngược chiều, cùng giá",
        "bằng nhau, ngược chiều, cùng giá", "bằng nhau, ngược chiều, khác giá"]   # "bằng nhau" = cùng độ lớn (đề gốc)
ANS = 3


def field(d, alpha=1.0):
    for x0, x1, c, s in ((60, 160, RED, "N"), (920, 1020, BLUE, "S")):
        d.rounded_rectangle([x0, PY0, x1, PY1], radius=14, fill=A(c, alpha))
        text(d, ((x0 + x1) / 2, (PY0 + PY1) / 2), s, 56, WHITE, alpha=alpha)
    col = A(PURPLE, 0.45 * alpha)
    for y in LINES_Y:
        dash_line(d, (176, y), (904, y), col)
        for x in (250, 830): chevron(d, x, y, 0, col)
    text(d, (900, PY0 - 34), "B", 44, PURPLE, anchor="rm", alpha=alpha)


def dot_out(d, x, y, r, color, w=6):
    d.ellipse([x - r, y - r, x + r, y + r], outline=color, width=w, fill=WHITE)
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=color)


def sides(phi):
    """phi (rad) quay cung chieu kim dong ho tren man hinh. Tra (canh I ra, canh I vao)."""
    c, s = math.cos(phi), math.sin(phi)
    return (OX - R * c, OY - R * s), (OX + R * c, OY + R * s)


def frame_top(d, phi, forces=0.0, gia=0.0):
    (x1, y1), (x2, y2) = sides(phi)
    d.line([(x1, y1), (x2, y2)], fill=ORANGE, width=12)
    d.ellipse([OX - 12, OY - 12, OX + 12, OY + 12], fill=NAVY)
    text(d, (OX - 30, OY + 44), "O", 36, NAVY, anchor="rm")
    if gia > 0:   # gia cua hai luc: duong thang dung net dut qua moi canh
        for x in (x1, x2): dash_line(d, (x, PY0 - 10), (x, PY1 + 10), A(GREEN, 0.55 * gia), w=4)
    if forces > 0:
        for (x, y), sg in (((x1, y1), -1), ((x2, y2), 1)):
            ye = y + sg * (30 + FL * forces)
            d.line([(x, y + sg * 30), (x, ye)], fill=A(GREEN, forces), width=9)
            chevron(d, x, ye, sg * math.pi / 2, A(GREEN, forces), s=24, w=8)
    dot_out(d, x1, y1, 26, ORANGE); cross_in(d, x2, y2, 26, ORANGE, w=6)


def view_tag(d, k=1.0):
    text(d, (180, PY1 + 44), "Nhìn từ trên xuống", 36, MUTED, bold=False, anchor="lm", alpha=k)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    field(d); frame_top(d, 0.0)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    kf = appear(t, 0.4, 0.6)
    field(d); frame_top(d, 0.0, forces=kf, gia=appear(t, 1.0, 0.5))
    answer_pill(d, 1000, "D", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    # nua dau (chon C): hai luc keo ve CUNG mot gia qua O -> triet tieu, khung dung yen
    u = ease((t - (m0 + 0.5)) / 0.9) * (1 - ease((t - (m1 - 0.6)) / 0.5))
    phi = 0.0
    if t >= m1:   # nua sau: dung la khac gia -> khung quay (toi ~60 do)
        phi = math.radians(60) * ease((t - (m1 + 0.4)) / 2.6)
    field(d)
    if u > 0.01:   # ve gia thuyet C: hai luc cung gia (dat tai O), ghost khung
        (x1, y1), (x2, y2) = sides(0.0)
        d.line([(x1, y1), (x2, y2)], fill=A(ORANGE, 0.35), width=12)
        for sg in (-1, 1):
            xa = lerp(x1 if sg < 0 else x2, OX, u)
            ye = OY + sg * (30 + FL)
            d.line([(xa, OY + sg * 30), (xa, ye)], fill=A(RED, 0.9), width=9)
            chevron(d, xa, ye, sg * math.pi / 2, A(RED, 0.9), s=24, w=8)
        for sg in (-1, 1):   # net dut tu canh khung toi gia chung qua O: luc van dat o canh, chi cung gia
            dash_line(d, (x1 if sg < 0 else x2, OY), (OX, OY), A(RED, 0.5 * u), w=4)
        badge(d, 680, 800, "Không quay", RED, appear(t, m0 + 1.4, 0.4))
    else:
        frame_top(d, phi, forces=1.0, gia=1.0)
    note(d, 900, "Cùng giá: triệt tiêu", RED, appear(t, m0, 0.45) * (1 - appear(t, m1 - 0.1, 0.3)))
    note(d, 900, "Khác giá: khung quay", GREEN, appear(t, m1, 0.45))


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Ngẫu lực: ngược chiều, khác giá",
             "Mặt khung vuông góc B: hai lực có giá thế nào?")


CLIP = dict(id="bay-l12-ch3-02", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Ngẫu lực từ · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Nhìn từ trên xuống.", 3.0),
   ("Chọn một đáp án.", 7.0)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án D.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.6, caps=[
   ("Chọn C: hai lực cùng giá.", 3.4),
   ("Thật ra: khác giá.", 3.8)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 5.6)]),
])
