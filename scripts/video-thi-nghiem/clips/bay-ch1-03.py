# Clip bay phu dao L12 Ch.1 so 03 - Thang Celsius va thang Kelvin: lech goc 273, khoang chia bang nhau (topic 197
# "Thang Celsius va thang Kelvin", lesson_topic 58, bai l12-thang-nhiet-do). Theo mau bay-ch3-01.
# Cau that: de 1295 cau 23 (question_index 0-based), tra loi ngan, 25/46 luot sai (54 %), 30 ngay toi 12/11/2026:
#   "Do nhiet do coc nuoc am duoc 55 do C. Trong thang Kelvin ung voi bao nhieu K?" -> 328 K (dung 273).
# CHUYEN TU TRA LOI NGAN sang 4 phuong an (doi thu tu de dap an la D):
#   A. 218 K (lay 273 - 55: tru thay vi cong)  B. 55 K (giu nguyen so)  C. -218 K (tru 273 nguoc chieu: t - 273)  D. 328 K -> D.
# Kiem so: T = t + 273 = 55 + 273 = 328 K (dung 273,15 thi 328,15 K, lam tron 328 K). 273 - 55 = 218; 55 - 273 = -218.
# Hinh: hai thang dat canh nhau, cung mot vi tri do cao: y(t) = 760 - (t + 20)/130*440; vach moi 10 do o ca hai thang
#   (khoang chia bang nhau). Moc: 0 do C <-> 273 K, 55 do C <-> 328 K, 100 do C <-> 373 K. Cot hai ben dang cung do cao.
from clips.bay_chung import *

CX, KX = 330, 750                       # truc thang Celsius / Kelvin
QY = 860
Q_LINES = ["Cốc nước ấm có nhiệt độ 55 °C.", "Theo thang Kelvin, nhiệt độ đó là"]
OPTS = ["218 K", "55 K", "−218 K", "328 K"]
ANS = 3


def ty(c): return 760 - (c + 20) / 130 * 440


def scales(d, lvl, marks, alpha=1.0, hi=None):
    """lvl: muc cot (do C) dang dang; marks: so moc da hien; hi: do C cua moc to cam."""
    for x, head, off, side in ((CX, "°C", 0, -1), (KX, "K", 273, 1)):
        d.rounded_rectangle([x - 22, ty(110) - 10, x + 22, ty(-20) + 10], radius=20, fill=A(WHITE, alpha),
                            outline=A(INK, alpha), width=4)
        for c in range(-20, 111, 10):
            d.line([(x + side * 22, ty(c)), (x + side * 40, ty(c))], fill=A(INK, alpha), width=3)
        if lvl is not None:
            d.rounded_rectangle([x - 14, ty(lvl), x + 14, ty(-20) + 4], radius=10, fill=A(RED, alpha))
        text(d, (x, ty(110) - 50), head, 48, INK, alpha=alpha)
        for j, c in enumerate((0, 55, 100)[:marks]):
            col = ORANGE if c == hi else INK
            text(d, (x + side * 56, ty(c)), str(c + off), 42, col, anchor="lm" if side > 0 else "rm", alpha=alpha)
    for j, c in enumerate((0, 55, 100)[:marks]):
        col = ORANGE if c == hi else MUTED
        dash_line(d, (CX + 48, ty(c)), (KX - 48, ty(c)), A(col, alpha), w=4)


def cup(d, alpha=1.0):
    x0, x1, y0, y1, wl = 170, 470, 430, 740, 520
    d.rectangle([x0 + 5, wl, x1 - 5, y1 - 5], fill=A((191, 219, 254), alpha))
    d.line([(x0, y0), (x0, y1), (x1, y1), (x1, y0)], fill=A(NAVY, alpha), width=7)
    tx = 400
    d.rounded_rectangle([tx - 14, 330, tx + 14, 702], radius=14, fill=A(WHITE, alpha), outline=A(MUTED, alpha), width=4)
    d.ellipse([tx - 26, 680, tx + 26, 732], fill=A(RED, alpha), outline=A(MUTED, alpha), width=4)
    d.rectangle([tx - 6, 560, tx + 6, 690], fill=A(RED, alpha))
    d.line([(tx + 14, 560), (560, 560)], fill=A(RED, 0.6 * alpha), width=3)
    d.rounded_rectangle([560, 524, 740, 596], radius=18, fill=A(WHITE, alpha), outline=A(RED, alpha), width=4)
    text(d, (650, 560), "55 °C", 48, RED, alpha=alpha)
    d.rounded_rectangle([800, 524, 980, 596], radius=18, fill=A(WHITE, alpha), outline=A(PURPLE, alpha), width=4)
    text(d, (890, 560), "? K", 48, PURPLE, alpha=alpha)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    cup(d)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    cup(d)
    answer_pill(d, 1000, "D", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    ks = appear(t, 0.1, 0.4)
    lvl = lerp(-20, 0, ease((t - 0.6) / 0.8)) if t < 2.0 else lerp(0, 55, ease((t - 2.0) / 1.4))
    marks = 1 if t < 3.3 else (2 if t < m1 + 1.2 else 3)
    scales(d, lvl, marks, ks, hi=55 if t >= 3.3 else 0)
    k = appear(t, m1 - 0.1, 0.45)
    if k <= 0: return
    y = 880 + (1 - k) * 30
    card(d, (60, y, 1020, y + 460), fill=A(WHITE, k), outline=A(RED, k), w=5)
    text(d, (W / 2, y + 50), "Sai: giữ 55 · lấy 273 − 55 · lấy 55 − 273", 40, RED, alpha=k)
    text(d, (W / 2, y + 190), "T = t + 273", 52, INK, alpha=k)
    k2 = appear(t, m1 + 1.0, 0.45) * k
    text(d, (W / 2, y + 330), "= 55 + 273 = 328 K", 52, GREEN, alpha=k2)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Hai thang lệch gốc 273: T = t + 273",
             "Nước nóng thêm 30 °C. Nhiệt độ tăng thêm bao nhiêu kelvin?")


CLIP = dict(id="bay-l12-ch1-03", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Thang nhiệt độ · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Nhiệt kế chỉ theo độ C.", 2.8),
   ("Chọn một đáp án.", 5.4)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án D.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.9, caps=[
   ("Hai cột dâng cao như nhau.", 3.4),
   ("Gốc hai thang lệch nhau 273.", 3.6)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
