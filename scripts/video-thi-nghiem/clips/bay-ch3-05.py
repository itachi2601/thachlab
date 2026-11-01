# Clip bay phu dao L12 Ch.3 so 05 - Tinh luc tu F = B.I.l.sin(theta): day treo lech. Theo mau bay-ch3-01/02.
# Tinh huong = de 1288 cau 9, 33/55 luot sai (60 %) trong 30 ngay (cau HS sai nhieu nhat cua chu de "Tinh luc tu"):
#   "Doan day MN = 5 cm, khoi luong 10 g treo bang hai day manh MC, ND sao cho MN nam ngang, CMND trong mat phang thang dung.
#    Tu truong deu B = 0,25 T huong thang dung tu duoi len. Cho dong I qua MN thi day treo lech 30 do so voi phuong thang dung.
#    g = 10 m/s2. I gan gia tri nao nhat?" A. 4,62 A  B. 6,93 A  C. 4,12 A  D. 6,62 A -> A.
# Kiem so: P = mg = 0,01.10 = 0,1 N; F = P.tan30 = 0,0577 N; I = F/(B.l) = 0,0577/(0,25.0,05) = 4,62 A (A).
#   B 6,93 A = 0,0866/0,0125 voi 0,0866 = P.cos30 (nham F = P.cos30 thay vi P.tan30). C 4,12 A, D 6,62 A: khong ung cach sai don gian nao
#   (nhieu nhat: 4,12 ~ 4,62 - 0,5; 6,62 ~ 6,93 - 0,3) -> chi neu bay co that (B). tan60 cho 13,86 A: khong co trong dap an nen khong dung.
# Hinh NHIN DOC THEO MN (mat phang giay thang dung): B huong LEN (nhu de); I VAO mat phang (X) -> F = I.l x B:
#   l = -z (vao), B = +y (len): (-z) x (+y) = +x -> F nam NGANG, HUONG SANG PHAI; day lech sang phai.
#   Can bang: T.cos30 = P, T.sin30 = F -> tan30 = F/P. Thang do: P = 100 px ung 0,1 N -> F dung = 57,7 px; F sai (P.cos30) = 86,6 px.
from clips.bay_chung import *

PVX, PVY, LS = 380, 345, 300         # diem treo, chieu dai day treo (hinh)
SP = 100                             # P = 100 px
QY = 830
Q_LINES = ["MN: 5 cm, 10 g. B = 0,25 T thẳng đứng.", "Dây treo lệch 30°, g = 10 m/s².", "I gần giá trị nào nhất?"]
OPTS = ["4,62 A", "6,93 A", "4,12 A", "6,62 A"]
ANS = 0
TH = math.radians(30)
CP, CF, CT = BLUE, GREEN, TEAL


def bob_pos(th): return PVX + LS * math.sin(th), PVY + LS * math.cos(th)


def vec(d, x, y, dx, dy, color, alpha=1.0, dashed=False, w=9):
    L = math.hypot(dx, dy)
    if L < 4 or alpha <= 0: return
    xe, ye = x + dx, y + dy; c = A(color, alpha)
    (dash_line(d, (x, y), (xe, ye), c, w=w) if dashed else d.line([(x, y), (xe, ye)], fill=c, width=w))
    chevron(d, xe, ye, math.atan2(dy, dx), c, s=24, w=8)


def field(d, alpha=1.0):
    col = A(PURPLE, 0.55 * alpha)
    for x in (700, 820, 940):
        dash_line(d, (x, 745), (x, 385), col)
        for y in (480, 650): chevron(d, x, y, -math.pi / 2, col)
    text(d, (820, 345), "B", 44, PURPLE, alpha=alpha)


def hang(d, th, alpha=1.0):
    bx, by = bob_pos(th)
    d.line([(PVX - 90, PVY), (PVX + 90, PVY)], fill=A(GRAY, alpha), width=10)
    dash_line(d, (PVX, PVY), (PVX, PVY + 330), A(GRAY, 0.7 * alpha), w=4)
    d.line([(PVX, PVY), (bx, by)], fill=A(NAVY, alpha), width=6)
    d.ellipse([PVX - 9, PVY - 9, PVX + 9, PVY + 9], fill=A(NAVY, alpha))
    if th > 0.05:   # cung goc lech + nhan
        r = 150; pts = [(PVX + r * math.sin(a * th / 12), PVY + r * math.cos(a * th / 12)) for a in range(13)]
        d.line(pts, fill=A(ORANGE, alpha), width=5)
        text(d, (PVX + 195 * math.sin(th / 2) + 8, PVY + 195 * math.cos(th / 2)), f"{round(math.degrees(th))}°", 40, ORANGE, alpha=alpha)
    cross_in(d, bx, by, 26, ORANGE, w=6, alpha=alpha)
    text(d, (bx - 44, by + 12), "I", 44, ORANGE, anchor="rm", alpha=alpha)
    return bx, by


def forces(d, bx, by, k, kf=1.0, ftrue=1.0):
    """k: P va T; kf: F. ftrue 0 = F sai (86,6 px, do) .. 1 = F dung (57,7 px, xanh)."""
    Fp = SP * math.tan(TH); Fw = SP * math.cos(TH)
    Fl = lerp(Fw, Fp, ftrue); fc = mix(RED, CF, ftrue)
    if k > 0:
        vec(d, bx, by + 30, 0, SP, CP, k)
        text(d, (bx - 22, by + 30 + SP * 0.6), "P", 44, CP, anchor="rm", alpha=k)
        Tl = SP / math.cos(TH); u = (-math.sin(TH), -math.cos(TH))
        vec(d, bx + u[0] * 30, by + u[1] * 30, u[0] * Tl, u[1] * Tl, CT, k)
        text(d, (bx + 45, by - Tl * 0.5 - 20), "T", 44, CT, anchor="lm", alpha=k)
    if kf > 0:
        vec(d, bx + 30, by, Fl, 0, fc, kf)
        text(d, (bx + 44, by + 56), "F" if ftrue > 0.5 else "F sai", 44, fc, anchor="lm", alpha=kf)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    field(d); bx, by = hang(d, TH)
    text(d, (bx + 40, by - 44), "MN", 36, NAVY, anchor="lm")   # chi canh nay: chua co T nen khong de
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    field(d); bx, by = hang(d, TH)
    forces(d, bx, by, appear(t, 0.9, 0.5), appear(t, 0.9, 0.5))
    answer_pill(d, 1000, "A", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def tam_giac(d, k):
    ax, ay, Lp = 150, 850, 300; Lf = Lp * math.tan(TH)
    cx, cy = ax, ay + Lp; ex = ax + Lf
    vec(d, ax, ay, 0, Lp, CP, k); vec(d, cx, cy, Lf, 0, CF, k); vec(d, ex, cy, ax - ex, ay - cy, CT, k)
    text(d, (ax - 22, ay + Lp / 2), "P", 44, CP, anchor="rm", alpha=k)
    text(d, (ax + Lf / 2, cy + 40), "F", 44, CF, alpha=k)
    text(d, (ax + Lf / 2 + 46, ay + Lp / 2 - 6), "T", 44, CT, anchor="lm", alpha=k)
    pts = [(ax + 110 * math.sin(a * TH / 12), ay + 110 * math.cos(a * TH / 12)) for a in range(13)]
    d.line(pts, fill=A(ORANGE, k), width=5)
    text(d, (ax + 40, ay + 160), "30°", 40, ORANGE, alpha=k)


def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    th = TH * ease((t - 0.1) / 1.0)
    field(d); bx, by = hang(d, th)
    g = ease((t - (m1 + 0.3)) / 1.0)     # F sai -> F dung
    forces(d, bx, by, appear(t, 1.0, 0.4), appear(t, 1.3, 0.4), ftrue=g)
    ka = appear(t, m0 + 0.9, 0.45) * (1 - appear(t, m1 - 0.1, 0.3))
    if ka > 0:   # the sai: F = P.cos30 -> 6,93 A
        y = 820 + (1 - ka) * 30
        card(d, (60, y, 1020, y + 360), fill=A(WHITE, ka), outline=A(RED, ka), w=5)
        text(d, (W / 2, y + 48), "Sai: F = P·cos30°", 44, RED, alpha=ka)
        text(d, (W / 2, y + 120), "F ≈ 0,0866 N", 44, INK, alpha=ka)
        text(d, (250, y + 260), "I =", 50, ORANGE, anchor="rm", alpha=ka)
        frac(d, 480, y + 260, "0,0866", "0,25·0,05", 46, INK, alpha=ka)
        text(d, (680, y + 260), "≈ 6,93 A", 50, RED, anchor="lm", alpha=ka)
    kb = appear(t, m1 + 0.2, 0.45)
    if kb > 0:   # the dung: tam giac luc dong kin
        y = 820 + (1 - kb) * 30
        card(d, (60, y, 1020, y + 620), fill=A(WHITE, kb), outline=A(GREEN, kb), w=5)
        tam_giac(d, kb)
        text(d, (680, y + 70), "tan30° = F / P", 46, GREEN, alpha=kb)
        k2 = appear(t, m1 + 1.2, 0.4)
        text(d, (680, y + 170), "F = 0,1·tan30°", 42, INK, alpha=k2)
        text(d, (680, y + 235), "≈ 0,0577 N", 42, INK, alpha=k2)
        k3 = appear(t, m1 + 2.0, 0.4)
        text(d, (250 + 280, y + 420), "I =", 50, ORANGE, anchor="rm", alpha=k3)
        frac(d, 760, y + 420, "0,0577", "0,25·0,05", 46, INK, alpha=k3)
        text(d, (W / 2, y + 560), "≈ 4,62 A", 50, GREEN, alpha=k3)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "tan(góc lệch so với phương thẳng đứng) = F / P",
             "Dây lệch 45°, P = 0,1 N. Lực từ F bằng bao nhiêu?")


CLIP = dict(id="bay-l12-ch3-05", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Lực từ lên dây dẫn · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Nhìn dọc theo dây MN.", 2.6),
   ("Chọn một đáp án.", 5.4)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án A.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.8, caps=[
   ("Bẫy: F = P·cos30° ra 6,93 A.", 3.8),
   ("Đúng: tan30° = F/P.", 4.0)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 5.0)]),
])
