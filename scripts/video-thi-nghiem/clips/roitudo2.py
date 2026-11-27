# Clip: tn-l10-roi-tu-do-02 - Day doi va video quay cham: vi tri bi roi sau moi 0,1 s (31/10/2026; dung lai 27/11/2026 theo
# cong moi viec 4: --do-chu 0 LOI, chu >= 56 px khi ve, Du doan khong nut, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-roi-tu-do-02.json (_kiem_so() doi chieu):
#   T = 0,1 s: s = 0; 4,9; 19,6; 44,1; 78,4; 122,5 cm ; khoang 4,9; 14,7; 24,5; 34,3; 44,1 cm ; hieu = g.T^2 = 9,8 cm.
#   tham_so T: 0,05..0,2 s, buoc 0,05 -> clip dung them T = 0,05 s (mo hinh): khoang 1,225; 3,675; 6,125 ... hieu 2,45 cm.
# Du doan (moi, vi Quan sat + Hinh 2 + meo 1:3:5 cua bai da noi "+9,8 cm" o T = 0,1 s): danh dau moi 0,05 s thi moi
#   khoang dai hon khoang truoc bao nhieu? -> 2,45 cm (nho hon 4 lan). Khung: A 2,45 / B 4,9 / C 9,8 / D 19,6 cm.
# Bay = hien_tuong_hay_sai thu 2: doc vi tri o mep bi thay vi tam. So tu dat: bi duong kinh 2 cm (nhu TN1 cua bai),
#   anh 0,3 s doc mep duoi -> 45,1 cm -> hieu 10,8 roi 7,8 cm (khong deu); doc tam -> 9,8 roi 9,8 cm.
# Thu nghi (= cau_chot khung web): hai khoang lien nhau chenh 22,05 cm, g = 9,8 -> T = sqrt(0,2205/9,8) = 0,15 s
#   (trong mien 0,05..0,2). Buoc nguoc + can + doi cm ra m chua chieu; 0,15 khong hien.
#   Nhieu: 0,0225 s (quen can), 1,5 s (quen doi cm ra m), 0,10 s (giu T cua thi nghiem).
from engine import *

G = 9.8
TA, TB, BI_R = 0.1, 0.05, 1.0                            # hai cach danh dau ; ban kinh bi tu dat (cm)
CH_D, CH_T = 22.05, 0.15

def scm(t): return 100 * 0.5 * G * t * t
POS_A = [scm(n * TA) for n in range(6)]
GAP_A = [b - a for a, b in zip(POS_A, POS_A[1:])]
POS_B = [scm(n * TB) for n in range(11)]
GAP_B = [b - a for a, b in zip(POS_B, POS_B[1:])]

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-roi-tu-do-02.json")))
    h = k["so_lieu_mau"]["hang"]
    assert all(abs(r[2] - p) < 1e-6 for r, p in zip(h, POS_A)) and all(abs(r[3] - g) < 1e-6 for r, g in zip(h, GAP_A))
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["T"]["min"] <= TB and ts["T"]["min"] <= CH_T <= ts["T"]["max"] and ts["g"]["gia_tri"] == G
    assert all(abs((b - a) - 100 * G * TA ** 2) < 1e-6 for a, b in zip(GAP_A, GAP_A[1:]))
    assert all(abs((b - a) - 2.45) < 1e-6 for a, b in zip(GAP_B, GAP_B[1:]))
    assert [round(g, 3) for g in GAP_B[:4]] == [1.225, 3.675, 6.125, 8.575]
    g2, g3 = POS_A[3] + BI_R - POS_A[2], POS_A[4] - POS_A[3] - BI_R              # anh 0,3 s doc mep duoi
    assert f"{g2 - GAP_A[1]:.1f}" == "10.8" and f"{g3 - g2:.1f}" == "7.8"
    assert abs(100 * G * CH_T ** 2 - CH_D) < 1e-9 and f"{(CH_D / 100 / G) ** 0.5:.2f}" == "0.15"
    assert f"{CH_D / 100 / G:.4f}" == "0.0225" and f"{(CH_D / G) ** 0.5:.1f}" == "1.5"
_kiem_so()

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")
STEEL = (110, 120, 140); STEEL_L = (200, 205, 216); GHOST = (196, 202, 214); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
DRED = (185, 28, 28); DTEAL = (15, 118, 110); EMPTY = (148, 140, 128); C_S = (37, 99, 235); C_F = (194, 65, 12)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 190 + i * 145
        if i < on: card(d, (x, y, x + 120, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 120, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def badge(d, y, s, col, a=1.0):
    pw = tw(d, s, F(58)) + 64
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 82), fill=A(col, a), r=40)
    text(d, (W / 2, y + 41), s, 58, WHITE, alpha=a)

def ball(d, x, y, a=1.0, r=18):
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(STEEL, a), outline=A(NAVY, a), width=2)
    d.ellipse([x - 8, y - 9, x - 2, y - 3], fill=A(STEEL_L, a))

# ---------------- hai cach danh dau cung mot lan roi: moi 0,1 s (trai) va moi 0,05 s (phai) ----------------
SY0, SPX = 360, 18.0                                      # y vach 0 ; px / cm
def SYp(c): return SY0 + SPX * c
def lane(d, x0, T, tf, bottom=1290):
    """tf: thoi gian roi that (s) da troi; dau danh o moi k.T <= tf."""
    card(d, (x0, 215, x0 + 490, bottom), fill=WHITE, outline=LIGHT, w=3)
    text(d, (x0 + 245, 268), "mỗi " + vn(T, 2 if T < 0.1 else 1) + " s", 58, C_F)
    rx = x0 + 135
    d.rectangle([rx, SY0 - 8, rx + 30, SYp(50)], fill=WOOD, outline=WOOD_D, width=3)
    for c in range(0, 51, 10): d.line([(rx, SYp(c)), (rx + 26, SYp(c))], fill=INK, width=3)
    text(d, (rx - 12, SY0), "0", 56, C_S, anchor="rm"); text(d, (rx - 12, SYp(40)), "40", 56, C_S, anchor="rm")
    px = x0 + 275
    d.line([(px, 330), (px, SYp(50))], fill=NAVY, width=3)                       # day doi
    n = 0
    while n * T <= tf + 1e-9 and n * T <= TEND + 1e-9:
        y = SYp(scm(n * T)); d.line([(px + 40, y), (px + 185, y)], fill=C_S, width=4); n += 1
    ball(d, px + 22, SYp(scm(min(tf, TEND))))
    text(d, (x0 + 470, bottom - 60), "s (cm)", 56, C_S, anchor="rm")
    return n

SLOW, RUN0 = 18.0, 0.4
TEND = 0.3                                                # chi ve toi 0,3 s (44,1 cm) cho lan 0,05 s du rong

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    lane(d, 40, TA, TEND); lane(d, 550, TB, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 620 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    badge(d, y0 + 26, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 165), "Mỗi 0,1 s: khoảng sau dài thêm 9,8 cm.", 56, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Mỗi 0,05 s: dài thêm bao nhiêu?", 60, PURPLE, alpha=a)
    seg_bar(d, y0 + 350, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (chieu cham x12, hai cach danh dau song song) ----------------
def s_do(img, d, t, sc):
    tf = clamp((t - RUN0) / SLOW, 0, TEND)
    lane(d, 40, TA, tf); lane(d, 550, TB, tf)
    card(d, (40, 1310, 1040, 1430), fill=NAVY, r=30)
    text(d, (W / 2, 1370), "chiếu chậm ×18", 58, YELLOW)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 560), fill=(236, 253, 243), outline=GREEN, w=6)
    badge(d, 240, "ĐÁP ÁN", DTEAL)
    text(d, (W / 2, 400), "2,45 cm,", 64, DTEAL)
    text(d, (W / 2, 485), "nhỏ hơn 4 lần", 64, DTEAL)
    card(d, (40, 590, 1040, 1100), fill=WHITE, outline=C_F, w=5)
    text(d, (W / 2, 670), "Mỗi 0,05 s, các khoảng:", 58, C_F)
    text(d, (W / 2, 790), "1,225 · 3,675 · 6,125 cm", 60, C_S)
    pu = 0.5 + 0.5 * math.sin(t * 5)
    text(d, (W / 2, 920), "+2,45      +2,45", 64, mix(GREEN, DTEAL, pu))
    k2 = appear(t, M[1] + 0.1, 0.45)
    card(d, (40, 1130, 1040, 1590), fill=A(WHITE, k2), outline=A(NAVY, k2), w=5)
    text(d, (W / 2, 1210), "Mỗi 0,1 s, các khoảng:", 58, NAVY, alpha=k2)
    text(d, (W / 2, 1330), "4,9 · 14,7 · 24,5 cm", 60, C_S, alpha=k2)
    text(d, (W / 2, 1460), "+9,8      +9,8", 64, GREEN, alpha=k2)

# ---------------- canh 4: Rut ra (hieu = g.T^2) ----------------
BARS = [("T = 0,1 s", 9.8, "9,8 cm", NAVY), ("T = 0,05 s", 2.45, "2,45 cm", C_F)]
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 320), "Hiệu hai khoảng liền nhau", 58, INK)
    text(d, (W / 2, 440), "= g · T²", 66, DTEAL)
    card(d, (40, 580, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    for i, (lab, v, vs, col) in enumerate(BARS):
        y = 720 + i * 300; k = ease(clamp((t - 2.1) / 0.8))
        text(d, (90, y), lab, 58, col, anchor="lm")
        L = 860 * v / 9.8 * k
        if L > 0: d.rounded_rectangle([90, y + 55, 90 + max(L, 14), y + 125], radius=12, fill=col)
        text(d, (990, y), vs, 58, col, anchor="rm")
    k2 = appear(t, M[1] - 0.1, 0.45)
    text(d, (W / 2, 1360), "T nhỏ 2 lần", 60, INK, alpha=k2)
    text(d, (W / 2, 1470), "→ hiệu nhỏ 4 lần", 60, DTEAL, alpha=k2)

# ---------------- canh 5: Bay (doc o mep bi) ----------------
def zoom_ball(d, cx, y, ok, t):
    R = 70
    d.rectangle([cx - 230, y - 120, cx - 190, y + 120], fill=WOOD, outline=WOOD_D, width=3)
    d.ellipse([cx - R, y - R, cx + R, y + R], fill=STEEL, outline=NAVY, width=3)
    d.ellipse([cx - 30, y - 34, cx - 8, y - 12], fill=STEEL_L)
    yy, col = (y, DTEAL) if ok else (y + R, DRED)
    wpx = 5 + int(3 * (0.5 + 0.5 * math.sin(t * 6)))
    d.line([(cx - 190, yy), (cx + R + 40, yy)], fill=col, width=wpx)
    text(d, (cx + R + 60, yy), "tâm" if ok else "mép dưới", 56, col, anchor="lm")

def s_bay(img, d, t, sc):
    M = sc["M"]; ok = t >= M[1] - 0.1
    card(d, (40, 215, 1040, 655), fill=WHITE, outline=DRED, w=6)
    text(d, (W / 2, 285), "✗ Đọc ở mép bi:", 58, DRED)
    text(d, (W / 2, 375), "mốc 0,3 s: 44,1 → 45,1 cm", 58, DRED)
    text(d, (W / 2, 470), "khoảng 25,5 · 33,3 cm", 58, DRED)
    text(d, (W / 2, 565), "hiệu 10,8 rồi 7,8 cm", 58, DRED)
    card(d, (40, 675, 1040, 1065), fill=WHITE, outline=LIGHT, w=3)
    zoom_ball(d, 400, 850, ok, t)
    if not ok: text(d, (W / 2, 1015), "lệch 1 cm", 56, DRED)
    if ok:
        card(d, (40, 1085, 1040, 1475), fill=WHITE, outline=DTEAL, w=6)
        f = F(58); w1 = tw(d, "Luôn đọc ở tâm bi", f); w0 = tw(d, "✓ ", f)
        text(d, (W / 2 - w1 / 2 - w0 / 2, 1160), "✓", 58, DTEAL)
        text(d, (W / 2 + w0 / 2, 1160), "Luôn đọc ở tâm bi", 58, DTEAL)
        text(d, (W / 2, 1270), "khoảng 24,5 · 34,3 cm", 58, DTEAL)
        text(d, (W / 2, 1380), "hiệu 9,8 rồi 9,8 cm", 58, DTEAL)

# ---------------- canh 6: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    lane(d, 40, TA, (t * 0.08) % TEND)
    card(d, (550, 215, 1040, 1290), fill=WHITE, outline=NAVY, w=6)
    text(d, (795, 520), "Mới thử", 58, INK); text(d, (795, 610), "một viên bi.", 58, INK)
    text(d, (795, 820), "Bi nặng hơn:", 58, INK); text(d, (795, 910), "rơi khác?", 62, DTEAL, alpha=appear(t, 1.6, 0.4))

# ---------------- canh 7: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    badge(d, 235, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 400), "Hai khoảng kề nhau", 60, INK, alpha=k)
    text(d, (W / 2, 495), "chênh 22,05 cm.", 60, C_S, alpha=k)
    text(d, (W / 2, 590), "g ≈ 9,8 m/s².", 60, INK, alpha=k)
    text(d, (W / 2, 715), "Đánh dấu mỗi", 60, ORANGE, alpha=k)
    text(d, (W / 2, 805), "bao nhiêu giây?", 62, ORANGE, alpha=k)
    hi = int(t * 2.5) % 4
    for i in range(4):
        y = 880 + 20 * i * i + 14 * i
        d.line([(380, y), (700, y)], fill=A(C_F if i == hi else C_S, k), width=7 if i == hi else 5)
    text(d, (W / 2, 1195), "T = ? s", 62, NAVY, alpha=k)
    seg_bar(d, 1290, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    cs += [(do["t0"] + RUN0 + n * TA * SLOW, "tap") for n in range(4)]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-roi-tu-do-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Sự rơi tự do · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đánh dấu bi rơi", draw=s_hook, tail=0.3, caps=[
   ("Bi rơi cạnh dây dọi.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cùng lần rơi, hai cách đánh dấu.", 3.8),
   ("Dấu đặt ở tâm bi.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Trừ hai khoảng liền nhau.", 3.2),
   ("So với mỗi 0,1 s.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Hiệu không đổi: nhanh dần đều.", 3.4),
   ("Bình phương của T.", 3.6)]),
 dict(key="bay", title="Bẫy: đọc ở mép bi", draw=s_bay, tail=0.3, caps=[
   ("Đọc ở mép bi?", 3.2),
   ("Luôn đọc ở tâm bi.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Mới thử một viên bi.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Thử tính, rồi chọn đáp án.", 6.0)]),
])
