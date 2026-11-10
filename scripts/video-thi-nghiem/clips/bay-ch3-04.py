# Clip bay phu dao L12 Ch.3 so 04 - Tu thong qua khung day (topic "Tu thong qua khung day"). Theo mau bay-ch3-01/02.
# Tinh huong = de 259 cau 8, 35/42 luot sai (83 %) trong 30 ngay:
#   "Trong hinh ve nao sau day, tu thong gui qua dien tich cua khung day dan co gia tri lon nhat?" (4 hinh) -> hinh (4).
#   Phuong an nhieu cua de: chi dem so duong suc ma chua xet duong suc co vuong goc qua khung khong; quen Phi phu thuoc cos(alpha).
# Hinh goc: (1),(2) duong suc nam ngang song song mat khung (Phi = 0); (3),(4) duong suc thang dung xuyen qua khung, (4) nhieu duong hon.
# Clip VE LAI 4 khung cung B, cung dien tich S (nhin ngang: khung la mot doan dai nhu nhau, duong suc thang dung, cach deu),
# chi khac GOC giua mat khung va duong suc. Anh xa hinh goc -> nhan trong clip (E1):
#   (1) -> A: mat khung SONG SONG duong suc (theta = 0, Phi = 0)            [goc (1): song song]
#   (2) -> B: mat khung hop duong suc 25 do (gan song song, xuyen it)      [goc (2): song song; clip cho nghieng 25 do de 4 hinh khac nhau]
#   (3) -> C: mat khung hop duong suc 55 do (xien, nhin "hung nhieu")      [goc (3): vuong goc, it duong; clip doi thanh khung xien de lam bay]
#   (4) -> D: mat khung VUONG GOC duong suc (theta = 90) = DAP AN          [goc (4): vuong goc, nhieu duong nhat]
# Phi = B.S.cos(alpha), alpha = goc giua B va phap tuyen n; theta = goc giua mat khung va duong suc -> alpha = 90 - theta.
# So duong suc xuyen qua (khoang cach 40 px, doan khung 300 px): A 0, B 4, C 6, D 8.
from clips.bay_chung import *

NL, LSP, LOFF = 10, 40, 24           # 10 duong suc, cach nhau 40, duong dau o x = 24 (tu mep trai panel)
PW, PH = 430, 350                    # kich thuoc panel (o he so 1)
LFR = 300                            # do dai doan khung (nhin ngang)
ANS = 3
THETAS = (0, 25, 55, 90)             # A B C D
QY = 290


def line_x(i, s): return (LOFF + LSP * i) * s


def crossing(theta, s=1.0):
    """chi so cac duong suc cat doan khung (tam o x = PW/2 * s)."""
    h = LFR / 2 * math.sin(math.radians(theta)) * s; cx = PW / 2 * s
    return [i for i in range(NL) if abs(line_x(i, s) - cx) <= h + 1e-6]


def panel(d, x0, y0, theta, s=1.0, letter=None, k=1.0, hl=0.0, outline=LIGHT, normal=False, ow=3):
    """Mot khung nhin ngang: duong suc thang dung (B xuong), doan khung cam, hl>0 to xanh cac duong xuyen qua."""
    if k <= 0: return
    d.rounded_rectangle([x0, y0, x0 + PW * s, y0 + PH * s], radius=24, fill=A(WHITE, k), outline=A(outline, k), width=ow)
    cross = set(crossing(theta, s))
    for i in range(NL):
        x = x0 + line_x(i, s); on = i in cross and hl > 0
        col = A(mix(PURPLE, GREEN, hl), k * (0.95 if on else 0.5)) if on else A(PURPLE, 0.5 * k)
        w = 7 if on else 4
        dash_line(d, (x, y0 + 64 * s), (x, y0 + (PH - 20) * s), col, w=w)
        for yc in (100, 290): chevron(d, x, y0 + yc * s, math.pi / 2, col, s=18 * s, w=int(5 * s) if s > 1 else 5)
    cx, cy = x0 + PW / 2 * s, y0 + 195 * s; h = LFR / 2 * s; th = math.radians(theta)
    p, q = (cx - h * math.sin(th), cy + h * math.cos(th)), (cx + h * math.sin(th), cy - h * math.cos(th))
    d.line([p, q], fill=A(ORANGE, k), width=int(12 * s)); 
    for e in (p, q): d.ellipse([e[0] - 7 * s, e[1] - 7 * s, e[0] + 7 * s, e[1] + 7 * s], fill=A(ORANGE, k))
    if normal:   # phap tuyen n = (cos, sin) tu tam khung
        n = 105 * s; ex, ey = cx + n * math.cos(th), cy + n * math.sin(th)
        d.line([(cx, cy), (ex, ey)], fill=A(TEAL, k), width=8)
        chevron(d, ex, ey, th, A(TEAL, k), s=24, w=8)
        text(d, (ex + 30 * math.cos(th) + 24, ey + 30 * math.sin(th) + 6), "n", 40, TEAL, alpha=k)
    if letter: text(d, (x0 + 40 * s, y0 + 36 * s), letter, max(40, int(48 * s)), NAVY, alpha=k)
    text(d, (x0 + (PW - 30) * s, y0 + 36 * s), "B", max(36, int(38 * s)), PURPLE, anchor="rm", alpha=k)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    k = appear(t, 0.1, 0.5); th0, th1 = sc["M"][1] + 0.6, sc["T"] - 0.1
    if k <= 0: return
    card(d, (40, QY, 1040, 1230), fill=A(WHITE, k), outline=A(PURPLE, k), w=5)
    text(d, (W / 2, QY + 52), "Từ thông qua khung nào lớn nhất?", 44, INK, alpha=k)
    for j in range(4):
        panel(d, 90 + (j % 2) * 470, QY + 110 + (j // 2) * 380, THETAS[j], letter="ABCD"[j], k=k)
    q = clamp((t - th0) / max(0.1, th1 - th0))
    if t >= th0 - 0.3:
        yb = 1190
        d.rounded_rectangle([140, yb - 5, 940, yb + 5], radius=5, fill=A(LIGHT, k))
        if q < 1: d.rounded_rectangle([140, yb - 5, 140 + 800 * (1 - q), yb + 5], radius=5, fill=A(PURPLE, k))


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    kr = appear(t, 0.4, 0.6)
    panel(d, 217, 330, THETAS[ANS], s=1.5, letter="D", hl=kr, outline=mix(LIGHT, GREEN, kr), ow=5)
    answer_pill(d, 1000, "D", "khung vuông góc đường sức", appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    th = 90.0
    th = lerp(90, 55, ease((t - (m0 + 0.5)) / 1.5))
    if t >= m1 + 0.2: th = lerp(55, 0, ease((t - (m1 + 0.2)) / 2.4))
    panel(d, 217, 420, th, s=1.5, hl=1.0, normal=True)
    n = len(crossing(th, 1.5))
    badge(d, 520, 360, f"α = {int(round(90 - th))}°", TEAL, appear(t, 0.2, 0.4))
    badge(d, 1000, 360, f"Xuyên qua: {n}", GREEN, appear(t, 0.2, 0.4))
    k = appear(t, m1 + 1.2, 0.45)
    note(d, 980, "Φ = BS·cosα", INK, k, sub="α: góc giữa B và pháp tuyến n")


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Φ = BS·cosα: chỉ đếm đường xuyên qua mặt khung",
             "Khung đang vuông góc B xoay đi 60°. Φ còn mấy phần so với lúc đầu?")


CLIP = dict(id="bay-l12-ch3-04", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Từ thông · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Cùng B, cùng diện tích S.", 3.0),
   ("Dừng lại, chọn một hình.", 6.0)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án D.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.6, caps=[
   ("Khung xiên: đường sức lướt qua.", 3.4),
   ("Xoay song song: Φ giảm về 0.", 3.4)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 5.6)]),
])
