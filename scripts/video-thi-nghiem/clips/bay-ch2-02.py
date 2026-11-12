# Clip bay phu dao L12 Ch.2 so 02 - Dong nang trung binh phan tu chi phu thuoc T (topic 212 "Dong nang trung binh phan tu va
# nhiet do", lesson_topic 64, bai l12-ap-suat-dong-nang). Theo mau bay-ch1-04 (the sai -> the dung).
# Cau that: de 1300 cau 12 (question_index 0-based), 12/23 luot sai (52 %), 30 ngay toi 12/11/2026. Cau goc gan chu de 61 trong DB.
#   "O cung mot nhiet do, cac loai phan tu khi khac nhau trong khong khi chuyen dong voi"
#   Goc: A. cung toc do  B. toc do khac nhau  C. cung the nang  D. the nang khac nhau -> B.
#   DOI THU TU (rai chu cai dap an trong chuong): A. cung toc do  B. cung the nang  C. toc do khac nhau  D. the nang khac nhau -> C.
#   Bay chinh A: cung nhiet do -> cung Wd -> (sai) cung toc do. B/D: lan dong nang voi the nang.
# Kiem: Wd = (3/2)kT bang nhau moi loai khi cung T; Wd = (1/2)m.v^2 (v: toc do can quan phuong).
#   m(O2)/m(H2) = 32/2 = 16 -> v(H2)/v(O2) = sqrt(16) = 4. O 27 do C: v(H2) = sqrt(3.8,31.300/0,002) ~ 1934 m/s,
#   v(O2) ~ 483 m/s (ti so 4,0) - khong ghi so m/s tren man. Hinh: toc do ve 90 px/s (O2) va 360 px/s (H2), cot v cao 55 / 220 px.
# THU NGHI (ca khac): He (M = 4) va O2 (M = 32) cung 27 do C -> v(He) = sqrt(8) ~ 2,8 lan v(O2). Tren man chi co ti le 16 -> 4,
#   khong co 8 -> 2,8.
from clips.bay_chung import *

BX0, BY0, BX1, BY1 = 120, 360, 960, 700     # hop khi
QY = 830
Q_LINES = ["Ở cùng một nhiệt độ, các loại phân tử khí", "khác nhau trong không khí chuyển động với…"]
OPTS = ["cùng tốc độ", "cùng thế năng", "tốc độ khác nhau", "thế năng khác nhau"]
ANS = 2
R = random.Random(11)
HEAVY = [(R.uniform(0, 1), R.uniform(0, 1), R.uniform(0, 6.28), R.uniform(0.8, 1.2)) for _ in range(7)]
LIGHTP = [(R.uniform(0, 1), R.uniform(0, 1), R.uniform(0, 6.28), R.uniform(0.8, 1.2)) for _ in range(11)]
VO2 = 90                                    # px/s; H2 nhanh gap 4


def pos(u, v, ang, sp, tau, r, y0, y1):
    r += 10   # chua le thanh hop + bien do rung
    x = refl(BX0 + r + u * (BX1 - BX0 - 2 * r) + sp * math.cos(ang) * tau, BX0 + r, BX1 - r)
    y = refl(y0 + r + v * (y1 - y0 - 2 * r) + sp * math.sin(ang) * tau, y0 + r, y1 - r)
    return x, y


def box(d, t, y0, y1, light_col, move=0.0, alpha=1.0):
    """move: thoi diem bat dau chuyen dong (None = dung yen, chi rung nhe). Hat nang tim r 24, hat nhe r 12."""
    d.rectangle([BX0, y0, BX1, y1], fill=A((236, 242, 255), alpha), outline=A(NAVY, alpha), width=8)
    for grp, col, r, v0 in ((HEAVY, PURPLE, 24, VO2), (LIGHTP, light_col, 12, 4 * VO2)):
        for u, v, ang, f in grp:
            sp = v0 * f
            if move is None:
                x, y = pos(u, v, ang, sp, 0, r, y0, y1)
                x += 4 * math.sin(6 * t + 3 * ang); y += 4 * math.cos(5 * t + 2 * ang)
            else:
                tau = max(0.0, t - move)
                pts = [pos(u, v, ang, sp, max(0.0, tau - 0.3 * j / 8), r, y0, y1) for j in range(9)]
                for j in range(8):   # vet: chi noi hai diem lien tiep neu khong bat thanh
                    if math.dist(pts[j], pts[j + 1]) < 60:
                        d.line([pts[j], pts[j + 1]], fill=A(col, alpha * 0.45 * (1 - j / 8)), width=int(r * 0.9))
                x, y = pts[0]
            d.ellipse([x - r, y - r, x + r, y + r], fill=A(col, alpha))


def legend(d, light_name, light_col, badge_s, alpha=1.0):
    dot(d, 150, 312, 22, A(PURPLE, alpha)); text(d, (184, 312), "O₂", 40, PURPLE, anchor="lm", alpha=alpha)
    dot(d, 300, 312, 12, A(light_col, alpha)); text(d, (322, 312), light_name, 40, light_col, anchor="lm", alpha=alpha)
    if badge_s: badge(d, 960, 312, badge_s, ORANGE, alpha, size=36)


def bars(d, kw, kv):
    card(d, (60, 740, 1020, 1120), fill=WHITE, outline=LIGHT, w=4)
    base = 1040
    if kw > 0:
        text(d, (300, 790), "Wđ trung bình", 40, INK, alpha=kw)
        for x, c, nm in ((200, PURPLE, "O₂"), (320, BLUE, "H₂")):
            h = 200 * kw
            if h > 2: d.rectangle([x, base - h, x + 80, base], fill=A(c, 1.0))
            text(d, (x + 40, base + 40), nm, 40, c, alpha=kw)
    if kv > 0:
        text(d, (780, 790), "Tốc độ trung bình", 40, INK, alpha=kv)
        for x, c, nm, hv in ((680, PURPLE, "O₂", 50), (800, BLUE, "H₂", 200)):
            h = hv * kv
            if h > 2: d.rectangle([x, base - h, x + 80, base], fill=A(c, 1.0))
            text(d, (x + 40, base + 40), nm, 40, c, alpha=kv)
        text(d, (896, base - 200 * kv), "× 4", 40, BLUE, anchor="lm", alpha=appear(kv, 0.8, 0.2))


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    legend(d, "N₂", TEAL, ""); box(d, t, BY0, BY1, TEAL, move=None)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    legend(d, "N₂", TEAL, ""); box(d, t, BY0, BY1, TEAL, move=None)
    answer_pill(d, 1000, "C", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    legend(d, "H₂", BLUE, "cùng 27 °C"); text(d, (575, 312), "xét O₂ và H₂", 40, INK); box(d, t, 360, 690, BLUE, move=0.5)
    bars(d, appear(t, m0 + 0.3, 0.8), appear(t, m1 + 0.3, 0.8))
    ka = appear(t, m0 + 1.2, 0.45) * (1 - appear(t, m1 - 0.1, 0.3))
    if ka > 0:
        y = 1160 + (1 - ka) * 30
        card(d, (60, y, 1020, y + 320), fill=A(WHITE, ka), outline=A(RED, ka), w=5)
        text(d, (W / 2, y + 60), "Sai: cùng Wđ trung bình", 44, RED, alpha=ka)
        text(d, (W / 2, y + 140), "→ cùng tốc độ trung bình  ✗", 44, RED, alpha=ka)
        text(d, (W / 2, y + 250), "Wđ = ½mv², m khác nhau", 42, INK, alpha=ka)
    kb = appear(t, m1 + 0.4, 0.45)
    if kb > 0:
        y = 1160 + (1 - kb) * 30
        card(d, (60, y, 1020, y + 230), fill=A(WHITE, kb), outline=A(GREEN, kb), w=5)
        text(d, (W / 2, y + 66), "m(O₂) = 16 · m(H₂)", 44, INK, alpha=kb)
        k2 = appear(t, m1 + 1.4, 0.4) * kb
        text(d, (W / 2, y + 160), "→  v(H₂) = 4 · v(O₂)", 46, GREEN, alpha=k2)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Cùng T: cùng Wđ trung bình, khác tốc độ trung bình",
             "He và O₂ cùng ở 27 °C.\nTốc độ He gấp mấy lần O₂?")


CLIP = dict(id="bay-l12-ch2-02", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Động năng phân tử · thachlab.id.vn",
            cues=bay_cues, scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Hai loại phân tử trong không khí.", 2.8),
   ("Chọn một đáp án.", 6.4)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án C.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.9, caps=[
   ("Cùng T: Wđ trung bình như nhau.", 3.8),
   ("Phân tử nặng hơn chạy chậm hơn.", 4.4)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
