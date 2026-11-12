# Sua vong 1 cong B: chu "chay" -> "truyen" (tranh cung co y Q la chat long), them chu thich cung chat cung khoi luong.
# Clip bay phu dao L12 Ch.1 so 02 - "Vat chua nhiet luong" (topic 199 "Noi nang va hai cach lam bien doi noi nang",
# lesson_topic 59, bai l12-noi-nang-dl1). Theo mau bay-ch3-01.
# Cau that: de 753 cau 6 (question_index 0-based), Dung-Sai, 36/63 luot sai (57 %), 30 ngay toi 12/11/2026. Cac y goc:
#   a) "Vat chua nhiet luong ben trong." (S)  b) "Nhiet luong chi ton tai trong luc truyen nhiet giua hai vat." (D)
#   c) "Noi 'vat co noi nang 500 J' la dung." (D)  d) "Noi nang la nang luong truyen di trong mot qua trinh." (S)
# CHUYEN TU CAU DUNG-SAI sang 4 phuong an "Phat bieu nao dung?" (mot dung, ba sai):
#   A. Vat nong chua nhieu nhiet luong (= y a, sai)   B. Noi nang la phan truyen di (= y d, sai)
#   C. Nhiet luong chi co khi truyen (= y b, DUNG)     D. Vat lanh khong co noi nang (trai y c: vat nao cung co U, sai) -> C.
# Kiem vat li: noi nang U = tong dong nang + the nang tuong tac cac phan tu, vat nao cung CO; nhiet luong Q = phan noi nang truyen
#   qua cho tiep xuc khi co chenh lech nhiet do, chi co trong qua trinh truyen. Hinh: hai khoi cung chat, cung khoi luong, 80 va 20 do C
#   -> can bang (80 + 20)/2 = 50 do C; thanh U nong giam, thanh U lanh tang cung mot luong (0,80 -> 0,55; 0,30 -> 0,55, minh hoa).
#   Tach ra: khong con Q, U moi vat van con.
from clips.bay_chung import *

BY0, BY1, BW = 380, 660, 300          # khoi: cao, rong
XH0, XC0 = 110, 670                   # vi tri tach roi (mep trai khoi nong / lanh)
XH1, XC1 = 240, 540                   # vi tri cham nhau (mat tiep xuc x = 540)
QY = 860
Q_LINES = ["Phát biểu nào đúng?"]
OPTS = ["Vật nóng chứa nhiều nhiệt lượng", "Nội năng là phần truyền đi",
        "Nhiệt lượng chỉ có khi truyền", "Vật lạnh không có nội năng"]
ANS = 2


def block(d, x0, color, temp, u=None, alpha=1.0):
    d.rounded_rectangle([x0, BY0, x0 + BW, BY1], radius=18, fill=A(mix(color, WHITE, 0.78), alpha),
                        outline=A(color, alpha), width=6)
    text(d, (x0 + BW / 2, BY0 + 46), f"{round(temp)} °C", 44, color, alpha=alpha)
    if u is not None:   # thanh muc noi nang
        gx = x0 + BW / 2 + 20; g0, g1 = BY0 + 95, BY1 - 25
        d.rounded_rectangle([gx - 26, g0, gx + 26, g1], radius=10, fill=A(WHITE, alpha), outline=A(INK, alpha), width=4)
        d.rounded_rectangle([gx - 20, g1 - 6 - (g1 - g0 - 12) * u, gx + 20, g1 - 6], radius=6, fill=A(PURPLE, alpha))
        text(d, (gx - 46, (g0 + g1) / 2), "U", 44, PURPLE, anchor="rm", alpha=alpha)


def pair(d, sl, th, tc, uh=None, uc=None, alpha=1.0):
    block(d, lerp(XH0, XH1, sl), RED, th, uh, alpha)
    block(d, lerp(XC0, XC1, sl), BLUE, tc, uc, alpha)


def flow(d, t, k):
    """Q chay qua mat tiep xuc x = 540: cham cam di tu nong sang lanh."""
    if k <= 0: return
    for i in range(6):
        ph = (t * 0.8 + i / 6) % 1.0; x = 470 + ph * 140; y = 470 + (i % 3) * 60
        r = 11; d.ellipse([x - r, y - r, x + r, y + r], fill=A(ORANGE, k * (1 - abs(ph - 0.5))))
    d.line([(495, 330), (585, 330)], fill=A(ORANGE, k), width=8); chevron(d, 585, 330, 0, A(ORANGE, k), s=24, w=8)
    text(d, (470, 330), "Q", 48, ORANGE, anchor="rm", alpha=k)


def state(t):
    sl = ease((t - 0.3) / 0.8) * (1 - ease((t - 4.0) / 0.8))
    p = ease((t - 1.2) / 2.6)
    return sl, p, 80 - 30 * p, 20 + 30 * p, 0.80 - 0.25 * p, 0.30 + 0.25 * p


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    pair(d, 0, 80, 20)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    pair(d, 0, 80, 20, 0.80, 0.30)
    answer_pill(d, 1000, "C", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    sl, p, th, tc, uh, uc = state(t)
    pair(d, sl, th, tc, uh, uc)
    text(d, (W / 2, 705), "cùng chất, cùng khối lượng", 36, MUTED, bold=False)
    flow(d, t, appear(t, 1.2, 0.3) * (1 - ease((p - 0.85) / 0.15)))
    kb = appear(t, 4.6, 0.4)
    s = "tách ra: hết truyền Q"; badge(d, W / 2 + (tw(d, s, F(36)) + 48) / 2, 775, s, ORANGE, kb, size=36)
    k = appear(t, sc["M"][1] - 0.1, 0.45)
    if k <= 0: return
    y = 830 + (1 - k) * 30
    card(d, (60, y, 1020, y + 440), fill=A(WHITE, k), outline=A(RED, k), w=5)
    text(d, (W / 2, y + 50), "Sai: coi Q là thứ vật chứa", 40, RED, alpha=k)
    # dong 1: noi nang - thanh muc
    gx, gy = 150, y + 180
    d.rounded_rectangle([gx - 22, gy - 60, gx + 22, gy + 60], radius=8, outline=A(INK, k), width=4)
    d.rounded_rectangle([gx - 16, gy - 10, gx + 16, gy + 54], radius=5, fill=A(PURPLE, k))
    text(d, (220, gy), "Nội năng U: vật CÓ", 44, PURPLE, anchor="lm", alpha=k)
    # dong 2: nhiet luong - mui ten di qua
    k2 = appear(t, sc["M"][1] + 1.0, 0.45) * k
    ay = y + 340
    d.line([(110, ay), (190, ay)], fill=A(ORANGE, k2), width=9); chevron(d, 190, ay, 0, A(ORANGE, k2), s=24, w=8)
    text(d, (220, ay), "Nhiệt lượng Q: phần TRUYỀN đi", 44, ORANGE, anchor="lm", alpha=k2)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Vật CÓ nội năng, không CHỨA nhiệt lượng",
             "Xoa hai tay thấy nóng. Tay có nhận nhiệt lượng?")


CLIP = dict(id="bay-l12-ch1-02", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Nội năng · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Hai vật: nóng và lạnh.", 3.3),
   ("Chọn một đáp án.", 5.4)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án C.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.9, caps=[
   ("Chạm nhau: Q truyền sang vật lạnh.", 4.0),
   ("Cùng 50 °C: ngừng truyền.", 4.4)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
