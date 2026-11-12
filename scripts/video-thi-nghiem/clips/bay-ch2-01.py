# Clip bay phu dao L12 Ch.2 so 01 - Doc do thi dang qua trinh (topic 208 "Doc do thi cac dang qua trinh", lesson_topic 62,
# bai l12-boyle-charles). Theo mau bay-ch3-05 / bay-ch1-04 (the sai -> the dung).
# TU SOAN (khong co cau that cung bay can hinh). Hai cau that gan nhat (30 ngay toi 12/11/2026, question_index 0-based):
#   de 1296 cau 1, 47/56 luot sai: do thi khoi luong rieng rho theo T trong qua trinh dang ap;
#   de 1295 cau 20, 31/46 luot sai: A->B dang tich roi B->C dang nhiet tren do thi.
# Cau: "Mot luong khi bien doi dang tich. Do thi p theo nhiet do t (do C) la..."
#   A. duong thang qua goc O                 (bay: lan t voi T, coi p ti le voi t)
#   B. duong thang, keo dai cat truc t o -273 do C   <- DUNG (thu tu tu dat)
#   C. mot nhanh hypebol                     (bay: lan voi dang nhiet p theo V)
#   D. duong thang song song truc t          (bay: lan voi dang ap, p khong doi)
# Kiem: dang tich p/T = const -> p = p1.(t + 273)/(t1 + 273): tuyen tinh theo t, p = 0 khi t = -273 do C; tai t = 0 p = 273/300 p1 khac 0.
# So tren hinh (minh hoa): 27 do C (300 K), p = 1,0 -> 177 do C (450 K), p = 1,5 (x10^5 Pa): 1,5/1,0 = 450/300 dung.
#   Duong sai "qua O" (do): noi O voi diem cuoi (177 do C; 1,5) -> tai 27 do C chi 0,23: khong qua diem dau -> sai ro.
# THU NGHI (ca khac, khong ve tren man): dang tich 27 do C, 1,5.10^5 Pa, dun toi 127 do C -> p = 1,5.400/300 = 2,0.10^5 Pa
#   (bay 1,5.127/27 = 7,06). Do thi tren man dung 27 -> 177 do C nen khong doc san duoc.
from clips.bay_chung import *

QY = 830
Q_LINES = ["Một lượng khí biến đổi đẳng tích.", "Đồ thị p theo nhiệt độ t (°C) là…"]
OPTS = ["đường thẳng qua gốc O", "đường thẳng, kéo dài cắt trục t ở −273 °C",
        "một nhánh hypebol", "đường thẳng song song trục t"]
ANS = 1
R = random.Random(5); DOTS = [(R.uniform(0.08, 0.92), R.uniform(0.08, 0.92), R.uniform(0, 6.28)) for _ in range(18)]
P1, P2 = 1.0, 1.5        # x10^5 Pa
T1, T2 = 300, 450        # K  (27 -> 177 do C)


# ---------------- binh kin + den ----------------
def vessel(d, t, heat=0.0, alpha=1.0):
    x0, y0, x1, y1 = 380, 360, 700, 680
    col = mix((224, 236, 255), (255, 228, 205), heat)
    d.rectangle([x0, y0, x1, y1], fill=A(col, alpha))
    amp = 5 + 6 * heat
    for u, v, ph in DOTS:
        x = x0 + 24 + u * (x1 - x0 - 48) + amp * math.sin((8 + 6 * heat) * t + ph)
        y = y0 + 24 + v * (y1 - y0 - 48) + amp * math.cos((7 + 6 * heat) * t + 2 * ph)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=A(BLUE, alpha))
    d.rectangle([x0, y0, x1, y1], outline=A(NAVY, alpha), width=12)
    for bx in (x0, x1):
        for by in (y0, y1): d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=A(GRAY, alpha))
    for i in range(4):   # ngon lua
        cx = 430 + i * 74; hh = 52 + 10 * math.sin(7 * t + i)
        d.polygon([(cx - 24, 772), (cx + 24, 772), (cx, 772 - hh)], fill=A(ORANGE, alpha))
    text(d, (350, 520), "V", 48, NAVY, anchor="rm", alpha=alpha)
    text(d, (722, 500), "đun nóng", 40, ORANGE, anchor="lm", alpha=alpha)


# ---------------- do thi nho p-V va p-T ----------------
def axes(d, ox, oy, wx, hy, xl, alpha=1.0):
    c = A(INK, alpha)
    d.line([(ox, oy), (ox + wx, oy)], fill=c, width=5); chevron(d, ox + wx, oy, 0, c, s=20, w=5)
    d.line([(ox, oy), (ox, oy - hy)], fill=c, width=5); chevron(d, ox, oy - hy, -math.pi / 2, c, s=20, w=5)
    text(d, (ox - 16, oy - hy + 10), "p", 40, INK, anchor="rm", alpha=alpha)
    text(d, (ox + wx, oy + 40), xl, 40, INK, anchor="rm", alpha=alpha)
    text(d, (ox - 14, oy + 30), "O", 38, INK, anchor="rm", alpha=alpha)


PY = lambda oy, p: oy - 230 * p          # 1,0 -> 230 px; 1,5 -> 345 px


def g_pV(d, g, alpha=1.0):
    ox, oy = 110, 760; axes(d, ox, oy, 330, 420, "V", alpha)
    xv = ox + 170; p = lerp(P1, P2, g)
    dash_line(d, (xv, oy), (xv, PY(oy, P1)), A(GRAY, 0.7 * alpha), w=3)
    if g > 0.01: d.line([(xv, PY(oy, P1)), (xv, PY(oy, p))], fill=A(GREEN, alpha), width=8)
    dot(d, xv, PY(oy, p), 12, A(GREEN, alpha))
    text(d, (ox + 165, 330), "p theo V", 40, MUTED, alpha=alpha)


def g_pT(d, g, kd, alpha=1.0):
    ox, oy, kx = 590, 760, 0.8           # 0,8 px/K: 300 K -> 240, 450 K -> 360
    axes(d, ox, oy, 420, 420, "T (K)", alpha)
    T = lerp(T1, T2, g); p = lerp(P1, P2, g)
    xa, ya = ox + kx * T1, PY(oy, P1)
    if kd > 0: dash_line(d, (ox, oy), (xa, ya), A(GREEN, kd * alpha), w=5)
    if g > 0.01: d.line([(xa, ya), (ox + kx * T, PY(oy, p))], fill=A(GREEN, alpha), width=8)
    dot(d, ox + kx * T, PY(oy, p), 12, A(GREEN, alpha))
    text(d, (ox + 200, 330), "p theo T", 40, MUTED, alpha=alpha)


# ---------------- do thi lon p-t trong the ----------------
def g_pt(d, y, kw, kr, alpha=1.0):
    """kw: duong sai qua O (do); kr: duong dung (xanh) + nét dut keo dai toi -273."""
    ox, oy, kx = 600, y + 520, 1.25      # 0 do C tai x 600; -273 -> 259; 27 -> 634; 177 -> 821
    py = lambda p: oy - 260 * p
    c = A(INK, alpha)
    d.line([(150, oy), (900, oy)], fill=c, width=5); chevron(d, 900, oy, 0, c, s=20, w=5)
    d.line([(ox, oy), (ox, oy - 430)], fill=c, width=5); chevron(d, ox, oy - 430, -math.pi / 2, c, s=20, w=5)
    text(d, (ox - 16, oy - 420), "p", 40, INK, anchor="rm", alpha=alpha)
    text(d, (1000, oy + 40), "t (°C)", 40, INK, anchor="rm", alpha=alpha)
    text(d, (ox + 14, oy + 34), "O", 38, INK, anchor="lm", alpha=alpha)
    xa, xb = ox + kx * 27, ox + kx * 177
    if kw > 0:
        a = kw * (1 - 0.65 * kr)
        d.line([(ox, oy), (xb, py(P2))], fill=A(RED, a), width=6)
        text(d, (xb + 24, py(P2) + 80), "✗ sai", 44, RED, anchor="lm", alpha=a)
    if kr > 0:
        x273 = ox - kx * 273
        dash_line(d, (x273, oy), (xa, py(P1)), A(GREEN, kr * alpha), w=5)
        d.line([(xa, py(P1)), (xb, py(P2))], fill=A(GREEN, kr * alpha), width=8)
        text(d, (xb + 24, py(P2) - 10), "đúng", 44, GREEN, anchor="lm", alpha=kr * alpha)
        dot(d, x273, oy, 12, A(ORANGE, kr * alpha))
        text(d, (x273, oy + 44), "−273", 40, ORANGE, alpha=kr * alpha)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    vessel(d, t)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    vessel(d, t, heat=0.5)
    answer_pill(d, 1000, "B", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    g = ease((t - 0.5) / 2.0)                       # cung mot qua trinh, hai do thi cung chay
    g_pV(d, g); g_pT(d, g, appear(t, 2.6, 0.5))
    kO = appear(t, 2.6, 0.4)
    badge(d, 900, 420, "đúng với T (K)", GREEN, kO, size=36)
    kc = appear(t, 2.9, 0.45)
    if kc <= 0: return
    y = 860 + (1 - kc) * 30
    card(d, (60, y, 1020, y + 690), fill=A(WHITE, kc), outline=A(RED, kc), w=5)
    text(d, (W / 2, y + 50), "Trục t (°C): sai nếu vẽ qua O", 42, RED, alpha=kc)
    kw = appear(t, 3.3, 0.4) * kc
    kr = appear(t, m1 + 0.3, 0.5) * kc
    g_pt(d, y, kw, kr, alpha=kc)
    k3 = appear(t, m1 + 1.6, 0.4) * kc
    text(d, (W / 2, y + 640), "t = −273 °C  ứng với  T = 0 K", 40, ORANGE, alpha=k3)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "p tỉ lệ với T (K), không với t (°C)",
             "Đẳng tích: khí ở 27 °C, 1,5·10⁵ Pa.\nĐun tới 127 °C thì p bằng bao nhiêu?")


CLIP = dict(id="bay-l12-ch2-01", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Đồ thị đẳng quá trình · thachlab.id.vn",
            cues=bay_cues, scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Bình kín, thể tích không đổi.", 2.8),
   ("Chọn một đáp án.", 6.2)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án B.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.9, caps=[
   ("Cùng một lần đun, vẽ trên hai trục.", 3.6),
   ("Đổi sang °C: gốc dịch về −273.", 4.6)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
