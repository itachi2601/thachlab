# Clip bay phu dao L12 Ch.3 so 01 - Cam ung tu va don vi tesla (topic_id 233). MAU cho cac clip bay (chang C, 1/11/2026).
# Tinh huong = cau HS sai nhieu nhat cua chu de trong 30 ngay: de 1056 cau 12 (Kiem tra nhanh Bai 10), 36/54 luot sai (67 %).
#   "Dat mot doan day thu vuong goc voi duong suc tai mot diem trong tu truong deu. Tang cuong do dong dien qua day thu
#    len gap doi thi cam ung tu tai diem do" A. tang gap doi  B. giam mot nua  C. khong thay doi  D. tang gap bon -> C.
# Co che ve dong: I -> 2I thi F -> 2F (mui ten dai gap doi), duong suc giu nguyen; B = F/(Il) tu va mau cung x2.
# Chieu: I vao mat phang, B sang phai -> F = Il x B huong XUONG.
from clips.bay_chung import *

PY0, PY1 = 330, 760                 # nam cham trai (N) / phai (S), cao
LINES_Y = (390, 470, 545, 620, 700)  # 5 duong suc deu, net dut, N -> S
WX, WY, WR = 540, 545, 34           # day thu (I vao mat phang)
F1 = 95                             # do dai mui ten F ung voi I (2I -> 2*F1)
QY = 830                            # the cau hoi
Q_LINES = ["Tăng I qua dây thử gấp đôi.", "Cảm ứng từ B tại đó sẽ…"]
OPTS = ["tăng gấp đôi", "giảm một nửa", "không đổi", "tăng gấp bốn"]
ANS = 2


def field(d, alpha=1.0):
    for x0, x1, c, s in ((60, 160, RED, "N"), (920, 1020, BLUE, "S")):
        d.rounded_rectangle([x0, PY0, x1, PY1], radius=14, fill=A(c, alpha))
        text(d, ((x0 + x1) / 2, (PY0 + PY1) / 2), s, 56, WHITE, alpha=alpha)
    col = A(PURPLE, 0.6 * alpha)
    for y in LINES_Y:
        if abs(y - WY) < 10:   # duong giua: chua cho day thu
            dash_line(d, (176, y), (WX - WR - 14, y), col); dash_line(d, (WX + WR + 14, y), (904, y), col)
        else:
            dash_line(d, (176, y), (904, y), col)
        for x in (330, 760): chevron(d, x, y, 0, col)
    text(d, (900, PY0 - 34), "B", 44, PURPLE, anchor="rm", alpha=alpha)


def wire(d, cur, alpha=1.0):
    """cur = 1 (I) .. 2 (2I): net day dam dan, nhan I / 2I."""
    cross_in(d, WX, WY, WR, ORANGE, w=int(5 + 3 * (cur - 1)), alpha=alpha)
    lab = "I" if cur < 1.5 else "2I"
    text(d, (WX - WR - 22, WY - WR - 18), lab, 44, ORANGE, anchor="rm", alpha=alpha)


def force(d, cur, alpha=1.0, lab=True):
    L = F1 * cur; y0 = WY + WR + 8; y1 = y0 + L
    d.line([(WX, y0), (WX, y1)], fill=A(GREEN, alpha), width=9)
    chevron(d, WX, y1, math.pi / 2, A(GREEN, alpha), s=24, w=8)
    if lab:   # nhan ben trai mui ten, nen trang de khong de len duong suc net dut
        s = "F" if cur < 1.5 else "2F"; yl = (y0 + y1) / 2 + 10; wl = tw(d, s, F(44))
        d.rounded_rectangle([WX - 34 - wl - 10, yl - 30, WX - 24, yl + 30], radius=10, fill=A(BG, alpha))
        text(d, (WX - 34, yl), s, 44, GREEN, anchor="rm", alpha=alpha)


def den(d, cx, cy, coef, alpha):
    """Mau so 'I.l' ve tung phan: I mau cam (nhu nhan day thu), l mau muc — phong SF ve I va l gan giong nhau."""
    parts = [(coef + "I", ORANGE), ("·", INK), ("l", INK)]; f = F(50)
    x = cx - sum(tw(d, s, f) + 4 for s, _ in parts) / 2
    for s, c in parts:
        text(d, (x, cy), s, 50, c, anchor="lm", alpha=alpha); x += tw(d, s, f) + 4


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    field(d); wire(d, 1); force(d, 1)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k)


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    field(d); wire(d, 1); force(d, 1)
    kr = appear(t, 0.5, 0.5)
    answer_pill(d, 1000, "C", OPTS[ANS], kr)


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    g = ease((t - (sc["M"][0] + 0.6)) / 1.6)   # I -> 2I
    cur = 1 + g
    field(d); wire(d, cur)
    if g > 0.02: force(d, 1, alpha=0.3, lab=False)   # bong mui ten cu de so do dai
    force(d, cur)
    kB = appear(t, sc["M"][0] + 2.4, 0.4)
    badge(d, 640, 292, "B giữ nguyên", PURPLE, kB)
    # the cong thuc: B = F/(Il) -> 2F/(2I.l): x2 o tu va mau triet tieu
    k = appear(t, sc["M"][1] - 0.1, 0.45)
    if k <= 0: return
    y = 860 + (1 - k) * 30
    card(d, (60, y, 1020, y + 400), fill=A(WHITE, k), outline=A(RED, k), w=5)
    text(d, (W / 2, y + 46), "Sai vì coi B đổi theo I", 40, RED, alpha=k)
    rich(d, 250, y + 220, "B =", 50, INK, alpha=k)
    frac(d, 440, y + 220, "F", "", 50, INK, alpha=k, wline=150); den(d, 440, y + 256, "", k)
    text(d, (580, y + 220), "=", 50, INK, alpha=k)
    k2 = appear(t, sc["M"][1] + 1.0, 0.45)
    frac(d, 760, y + 220, "2F", "", 50, INK, alpha=k * k2, wline=190); den(d, 760, y + 256, "2", k * k2)
    k3 = appear(t, sc["M"][1] + 2.0, 0.4)
    if k3 > 0:   # gach hai so 2 triet tieu
        for yy in (y + 220 - 36, y + 220 + 36):
            d.line([(690, yy + 18), (726, yy - 18)], fill=A(RED, k3), width=6)
        text(d, (W / 2, y + 350), "chữ l thường: chiều dài dây", 36, MUTED, bold=False, alpha=k3)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "B do từ trường, không do dây thử",
             "Dây thử dài gấp đôi, I giữ nguyên: F gấp mấy lần?")


CLIP = dict(id="bay-l12-ch3-01", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Cảm ứng từ · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Dây thử vuông góc đường sức.", 3.0),
   ("Dừng lại, chọn một đáp án.", 5.2)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án C.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.9, caps=[
   ("Tăng I: lực F gấp đôi.", 3.2),
   ("F, I cùng gấp đôi: tỉ số giữ nguyên.", 3.6)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
