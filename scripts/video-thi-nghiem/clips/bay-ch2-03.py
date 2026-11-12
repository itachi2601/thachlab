# Clip bay phu dao L12 Ch.2 so 03 - Luong khi doi thi khong ap p1V1 = p2V2 may moc (topic 206 "Qua trinh dang nhiet va dinh luat
# Boyle", lesson_topic 62, bai l12-boyle-charles). Theo mau bay-ch1-04 (the sai -> the dung).
# Cau that: de 1296 cau 6 (question_index 0-based), 42/56 luot sai (75 %), 30 ngay toi 12/11/2026:
#   "Binh 6.10^-3 m3 chua khi 2,75.10^6 Pa, xa bom bong 3,3.10^-3 m3 o 10^5 Pa, nhiet do khong doi. So bong?"
#   Goc: A. 50  B. 48  C. 52  D. 49 -> B.  DOI THU TU (rai chu cai dap an): A. 50  B. 52  C. 49  D. 48 -> D.
# Kiem so (pV tinh bang Pa.m3): ca binh 2,75.10^6 x 6.10^-3 = 16 500; moi bong 10^5 x 3,3.10^-3 = 330;
#   khi o lai binh khi binh con 10^5 Pa: 10^5 x 6.10^-3 = 600 -> vao bong 16 500 - 600 = 15 900 -> 15 900 / 330 = 48,18 -> 48 bong
#   (bong 49 chi duoc 0,18 bong). Nhieu: 50 = 16 500 / 330 (quen khi o lai binh); 52 = (16 500 + 600)/330 = 51,8 (cong nham khi
#   o lai); 49 = lam tron len 48,18.
# Hinh: p binh (x10^5 Pa) = (16 500 - 330 n)/600 = 27,5 - 0,55 n; n = 0 -> 27,5; n = 48,18 -> 1,0 (ngung). 27,5.10^5 = 2,75.10^6.
# THU NGHI (ca khac): binh 10 lit khi 20.10^5 Pa, bong 2 lit o 10^5 Pa -> (200 - 10)/2 = 95 bong (bay 100). Khong co so nay tren man.
from clips.bay_chung import *

QY = 830
Q_LINES = ["Bình 6·10⁻³ m³ chứa khí ở 2,75·10⁶ Pa.", "Bơm bóng, mỗi bóng 3,3·10⁻³ m³ ở 10⁵ Pa.",
           "T không đổi. Bơm được bao nhiêu bóng?"]
OPTS = ["50 bóng", "52 bóng", "49 bóng", "48 bóng"]
ANS = 3
NMAX = 15900 / 330                     # 48,18
TX0, TY0, TX1, TY1 = 80, 380, 280, 770  # binh khi
GX0, GY0, CELL = 360, 405, 55          # luoi bong 12 x 5


def ptank(n): return 27.5 - 0.55 * n


def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")


def tank(d, n, kleft=0.0):
    p = ptank(n)
    full = mix((224, 236, 255), BLUE, 0.15 + 0.55 * (p / 27.5))
    col = mix(full, (255, 215, 170), kleft)
    d.rounded_rectangle([TX0, TY0, TX1, TY1], radius=60, fill=col, outline=NAVY, width=8)
    d.rectangle([165, 345, 195, TY0], fill=GRAY)                     # van
    d.line([(180, 345), (180, 322), (330, 322), (330, 372)], fill=GRAY, width=10)   # ong dan
    text(d, ((TX0 + TX1) / 2, 520), vn(p), 52, NAVY)
    text(d, ((TX0 + TX1) / 2, 590), "×10⁵ Pa", 36, NAVY)


def balloon(d, x, y, s, col=RED, outline=False):
    """s: 0..1 muc bom day (ban kinh theo s)."""
    rx, ry = 20 * s, 24 * s
    if outline:
        d.ellipse([x - 20, y - 24, x + 20, y + 24], outline=A(col, 1.0), width=4); return
    if rx < 2: return
    d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=col)
    d.line([(x, y + ry), (x, y + ry + 8)], fill=GRAY, width=3)


def grid(d, n):
    full = int(n)
    for i in range(min(full + 1, 60)):
        r, c = divmod(i, 12)
        s = 1.0 if i < full else (n - full)
        balloon(d, GX0 + 22 + c * CELL, GY0 + r * CELL, s ** 0.5)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    tank(d, 0)
    balloon(d, 382, 405, 1, col=GRAY, outline=True)
    text(d, (382, 405), "?", 36, GRAY)
    text(d, (300, 560), "= 2,75·10⁶ Pa", 40, NAVY, anchor="lm")
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    tank(d, 0)
    balloon(d, 382, 405, 1, col=GRAY, outline=True)
    text(d, (300, 560), "= 2,75·10⁶ Pa", 40, NAVY, anchor="lm")
    answer_pill(d, 1000, "D", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    n = NMAX * ease((t - 0.5) / 3.3)
    kl = appear(t, m1, 0.5)
    tank(d, n, kl); grid(d, n)
    text(d, (690, 340), f"Đã bơm: {int(n)} bóng", 42, INK)
    k49 = appear(t, m1 + 0.2, 0.4)
    if k49 > 0: text(d, (GX0 + 52, GY0 + 4 * CELL), "← bóng 49 chưa đầy", 38, RED, anchor="lm", alpha=k49)
    badge(d, 330, 805, "khí ở lại bình", ORANGE, kl, size=36)
    ka = appear(t, m0 + 0.9, 0.45) * (1 - appear(t, m1 - 0.1, 0.3))
    if ka > 0:   # the sai
        y = 860 + (1 - ka) * 30
        card(d, (60, y, 1020, y + 330), fill=A(WHITE, ka), outline=A(RED, ka), w=5)
        text(d, (W / 2, y + 60), "pV: bình 16 500 Pa·m³, bóng 330 Pa·m³", 40, INK, alpha=ka)
        text(d, (W / 2, y + 160), "Sai: 16 500 : 330 = 50 bóng  ✗", 46, RED, alpha=ka)
        text(d, (W / 2, y + 260), "quên phần khí ở lại trong bình", 40, MUTED, alpha=ka)
    kb = appear(t, m1 + 0.4, 0.45)
    if kb > 0:   # the dung
        y = 860 + (1 - kb) * 30
        card(d, (60, y, 1020, y + 400), fill=A(WHITE, kb), outline=A(GREEN, kb), w=5)
        text(d, (W / 2, y + 60), "Ở lại bình: 10⁵ · 6·10⁻³ = 600", 44, ORANGE, alpha=kb)
        k2 = appear(t, m1 + 1.4, 0.4) * kb
        text(d, (W / 2, y + 170), "Vào bóng: 16 500 − 600 = 15 900", 44, INK, alpha=k2)
        k3 = appear(t, m1 + 2.4, 0.4) * kb
        text(d, (W / 2, y + 290), "15 900 : 330 ≈ 48,2 → 48 bóng", 46, GREEN, alpha=k3)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Khí ở lại bình không vào được bóng",
             "Bình 10 lít, khí 20·10⁵ Pa.\nBóng 2 lít, 10⁵ Pa. Bơm được mấy bóng?")


CLIP = dict(id="bay-l12-ch2-03", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Định luật Boyle · thachlab.id.vn",
            cues=bay_cues, scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Xả khí từ bình vào bóng.", 2.8),
   ("Chọn một đáp án.", 6.4)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án D.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=1.0, caps=[
   ("Bẫy: chia hết khí cho bóng.", 4.0),
   ("Bình còn 10⁵ Pa thì ngừng xả.", 5.0)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
