# Clip bay phu dao L12 Ch.1 so 04 - Dau cua A trong dU = A + Q khi khi dan (topic 200 "Van dung dU = A + Q", lesson_topic 59,
# bai l12-noi-nang-dl1). Theo mau bay-ch3-05 (the sai -> the dung).
# Cau that: de 1300 cau 25 (question_index 0-based), 10/23 luot sai (43 %), 30 ngay toi 12/11/2026:
#   "Truyen Q = 400 J cho khi, khi dan day pit-tong, dV = 0,3 lit, p = 2.10^5 Pa khong doi. Do bien thien noi nang?" -> 340 J.
# Chuyen thanh 4 phuong an (thu tu: A dung): A. 340 J  B. 460 J (sai dau A: cong +60)  C. 400 J (quen cong)  D. -340 J (dao dau ca bieu thuc).
# Kiem so: cong khi sinh ra A' = p.dV = 2.10^5 Pa x 0,3.10^-3 m^3 = 60 J. Quy uoc SGK: dU = A + Q, A la cong khi NHAN,
#   Q la nhiet khi NHAN. Khi dan -> khi sinh cong -> A = -60 J; Q = +400 J -> dU = -60 + 400 = 340 J.
#   Bay: 400 + 60 = 460 J. Hinh: pit-tong di LEN 90 px (minh hoa dV), mui ten Q vao thanh xilanh tu ben trai.
from clips.bay_chung import *

CX0, CX1, CY1 = 400, 680, 790        # xilanh: thanh trai/phai, day
P0, P1 = 560, 470                    # pit-tong: mat duoi truoc/sau khi dan
QY = 860
Q_LINES = ["Truyền Q = 400 J cho khí, khí dãn", "đẩy pit-tông; p = 2·10⁵ Pa không đổi,", "ΔV = 0,3 lít. Nội năng khí biến thiên"]
OPTS = ["340 J", "460 J", "400 J", "−340 J"]
ANS = 0
R = random.Random(3); DOTS = [(R.uniform(0.08, 0.92), R.uniform(0.06, 0.94), R.uniform(0, 6.28)) for _ in range(22)]


def cyl(d, t, py, alpha=1.0):
    """py: mat duoi pit-tong. Khi (cham xanh) trong vung py..CY1, rung theo t."""
    d.rectangle([CX0 + 5, py, CX1 - 5, CY1 - 4], fill=A((224, 236, 255), alpha))
    for u, v, ph in DOTS:
        x = CX0 + 20 + u * (CX1 - CX0 - 40) + 7 * math.sin(9 * t + ph)
        y = py + 18 + v * (CY1 - py - 36) + 7 * math.cos(8 * t + 2 * ph)
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=A(BLUE, alpha))
    d.line([(CX0, 330), (CX0, CY1), (CX1, CY1), (CX1, 330)], fill=A(NAVY, alpha), width=8)
    d.rectangle([CX0 + 6, py - 36, CX1 - 6, py], fill=A(GRAY, alpha))
    d.rectangle([(CX0 + CX1) / 2 - 10, py - 150, (CX0 + CX1) / 2 + 10, py - 36], fill=A(GRAY, alpha))


def heat(d, t, alpha=1.0):
    y = 700; x1 = CX0 - 14; x0 = x1 - 170 + 10 * math.sin(5 * t)
    d.line([(x0, y), (x1 - 6, y)], fill=A(ORANGE, alpha), width=12); chevron(d, x1, y, 0, A(ORANGE, alpha), s=30, w=10)
    text(d, (x1 - 125, y - 62), "Q = 400 J", 42, ORANGE, alpha=alpha)


def given(d, alpha=1.0):
    text(d, (720, 420), "p = 2·10⁵ Pa", 42, INK, anchor="lm", alpha=alpha)
    text(d, (720, 500), "ΔV = 0,3 lít", 42, INK, anchor="lm", alpha=alpha)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    cyl(d, t, P0); heat(d, t); given(d)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    cyl(d, t, P0); heat(d, t); given(d)
    answer_pill(d, 1000, "A", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    py = lerp(P0, P1, ease((t - 0.3) / 1.7))
    cyl(d, t, py); heat(d, t); given(d)
    kp = appear(t, 0.5, 0.4) * (1 - appear(t, 2.6, 0.4))
    if kp > 0:   # khi day pit-tong len: mui ten xanh tren pit-tong
        xm = (CX0 + CX1) / 2 + 70
        d.line([(xm, py - 50), (xm, py - 140)], fill=A(GREEN, kp), width=9); chevron(d, xm, py - 140, -math.pi / 2, A(GREEN, kp), s=24, w=8)
    kb = appear(t, 2.0, 0.4)
    badge(d, 1010, 600, "sinh công 60 J", GREEN, kb, size=36)
    ka = appear(t, 2.6, 0.45)   # sau khi pit-tong dung (2,0 s) va nhan "sinh cong" (2,0 s) >= 0,5 s
    ka = ka * (1 - appear(t, m1 - 0.1, 0.3))
    if ka > 0:   # the sai: cong 60 J vao
        y = 860 + (1 - ka) * 30
        card(d, (60, y, 1020, y + 300), fill=A(WHITE, ka), outline=A(RED, ka), w=5)
        text(d, (W / 2, y + 60), "Sai: lấy A = +60 J", 44, RED, alpha=ka)
        text(d, (W / 2, y + 190), "ΔU = 400 + 60 = 460 J  ✗", 50, RED, alpha=ka)
    kb2 = appear(t, m1 + 0.2, 0.45)
    if kb2 > 0:  # the dung
        y = 860 + (1 - kb2) * 30
        card(d, (60, y, 1020, y + 520), fill=A(WHITE, kb2), outline=A(GREEN, kb2), w=5)
        text(d, (W / 2, y + 60), "A là công khí NHẬN", 44, GREEN, alpha=kb2)
        text(d, (W / 2, y + 160), "khí dãn, sinh 60 J → A = −60 J", 42, INK, alpha=kb2)
        k2 = appear(t, m1 + 1.2, 0.4) * kb2
        text(d, (W / 2, y + 290), "ΔU = A + Q", 50, INK, alpha=k2)
        k3 = appear(t, m1 + 2.0, 0.4) * kb2
        text(d, (W / 2, y + 410), "= −60 + 400 = 340 J", 50, GREEN, alpha=k3)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "A là công khí nhận: khí dãn thì A < 0",
             "Khí bị nén, nhận công 60 J và toả nhiệt 20 J. ΔU bằng bao nhiêu?")


CLIP = dict(id="bay-l12-ch1-04", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Định luật 1 nhiệt động lực học · thachlab.id.vn",
            cues=bay_cues, scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Đun nóng khí trong xilanh.", 2.8),
   ("Chọn một đáp án.", 5.6)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án A.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.9, caps=[
   ("Bẫy: cộng thêm công 60 J.", 4.0),
   ("Khí đẩy pit-tông: khí mất năng lượng.", 4.2)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
