# Clip: tn-l11-nang-luong-dien-02 - Kiem nhan 12 V - 21 W cua den xe may bang von ke va ampe ke (ban 2 cong moi, 27/11/2026)
# Ban 2: chu >= 56 px, bo the "Dap an" trong canh Tien hanh, bo the chot + Goi y, nhip Bay >= 3 s, Bay o hang 9,0 V
#   (khac cap so cua Du doan 6,0 V).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-nang-luong-dien-02.json:
#   so_lieu_mau (U V, I A, P = UI W, R = U/I Ohm): 12,0 1,75 21,0 6,86 ; 9,0 1,55 13,95 5,81 ; 6,0 1,30 7,8 4,62
#   Du doan: o 6,0 V den tieu thu khoang bao nhieu? -> khoang 8 W (7,80 W).
#   Bay = hien_tuong_hay_sai[1]: coi R = U_dm^2/P_dm = 6,9 Ohm khong doi -> P(9 V) = 21.(9/12)^2 = 11,8 W (tu suy);
#     do that 13,95 W, R(9 V) = 5,81 Ohm (so_lieu_mau).
#   Chua noi duoc = sai_so_thuong_gap[1]: dong trong vai giay dau khi vua bat.
#   Cau hoi chot: den 9 V - 4,5 W sang binh thuong -> I = P/U = 0,5 A (tu suy, khong hien trong clip).
# Mach (vat li): nguon (+) -> ampe ke noi tiep -> den -> (-); von ke song song voi den. Luc xoay num hai dong ho
#   hien "· · ·"; xoay xong so chi + do sang + hang bang doi CUNG luc (_kiem_dong_bo()).
# Canh: Du doan (K10) -> Tien hanh 12 / 9 / 6 V (bang U-I) -> Dap an (cot P = UI) + Rut ra -> Bay (9 V) roi
#       Chua noi duoc -> THU NGHI.
from engine import *

ROWS = [(12.0, 1.75), (9.0, 1.55), (6.0, 1.30)]                 # so_lieu_mau (U, I)
P_DM, U_DM = 21.0, 12.0
R_DM = U_DM ** 2 / P_DM                                          # 6,86 Ohm
def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")
def P_of(i): return ROWS[i][0] * ROWS[i][1]
P_BAY = 9.0 ** 2 / R_DM                                          # 11,81 W (tu suy)
BODY = (70, 78, 100); SCR = (220, 240, 225); WIRE = (60, 66, 90); DRED = (185, 28, 28)
OFF = (205, 208, 215); DGREEN = (21, 110, 55); EMPTY = (148, 140, 128)
assert abs(P_BAY - 11.81) < 0.01 and abs(4.5 / 9 - 0.5) < 1e-9

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
XL, XR, YT, YB = 130, 660, 420, 860          # vong mach chinh
XV, YJ1, YJ2 = 900, 500, 800                 # nhanh von ke + hai diem noi
AMC, VMC, LC = (400, YT), (XV, 650), (XR, 650)

def knob_ang(u): return math.radians(-225 + 270 * u / 15)   # thang 0-15 V

def meter(d, c, reading, name):
    cx, cy = c
    card(d, (cx - 125, cy - 88, cx + 125, cy + 88), fill=BODY, r=20)
    card(d, (cx - 110, cy - 74, cx + 110, cy + 10), fill=SCR, r=10)
    text(d, (cx, cy - 32), reading, 58, (20, 60, 30))
    text(d, (cx, cy + 50), name, 56, WHITE, bold=False)

def lamp(d, b, c=None, r0=62):
    """b = P/P_dm (0 = tat). Do sang + mau day toc theo cong suat."""
    cx, cy = c or LC
    if b > 0:
        for k in range(6, 0, -1):
            r = r0 + (36 + 140 * b) * k / 6
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(YELLOW, 0.10 * b * (7 - k) / 6 + 0.02 * b))
    glass = OFF if b <= 0 else mix((255, 236, 200), (255, 245, 170), b)
    d.ellipse([cx - r0, cy - r0, cx + r0, cy + r0], fill=glass, outline=NAVY, width=5)
    fil = GRAY if b <= 0 else mix((200, 60, 30), (255, 200, 40), clamp((b - 0.3) / 0.7))
    pts = [(cx, cy - r0), (cx, cy - 32)] + [(cx + (22 if i % 2 else -22), cy - 26 + i * 13) for i in range(5)] + \
          [(cx, cy + 32), (cx, cy + r0)]
    d.line(pts, fill=fil, width=6, joint="curve")

def circuit(d, u, ra, rv, b):
    """u = vi tri num (V); ra/rv = chuoi so chi ampe ke/von ke; b = do sang den 0..1."""
    w = 7
    d.line([(XL, 540), (XL, YT), (AMC[0] - 125, YT)], fill=WIRE, width=w, joint="curve")
    d.line([(AMC[0] + 125, YT), (XR, YT), (XR, LC[1] - 62)], fill=WIRE, width=w, joint="curve")
    d.line([(XR, LC[1] + 62), (XR, YB), (XL, YB), (XL, 800)], fill=WIRE, width=w, joint="curve")
    d.line([(XR, YJ1), (XV, YJ1), (XV, VMC[1] - 88)], fill=WIRE, width=w, joint="curve")
    d.line([(XV, VMC[1] + 88), (XV, YJ2), (XR, YJ2)], fill=WIRE, width=w, joint="curve")
    for y in (YJ1, YJ2): dot(d, XR, y, 12, WIRE)
    card(d, (35, 540, 225, 800), fill=WHITE, outline=NAVY, r=20, w=5)
    text(d, (130, 590), "nguồn", 56, INK, bold=False)
    dot(d, 130, 700, 46, (225, 228, 236), outline=NAVY)
    a = knob_ang(u); d.line([(130, 700), (130 + 38 * math.cos(a), 700 + 38 * math.sin(a))], fill=RED, width=8)
    text(d, (180, 505), "+", 58, RED); text(d, (180, 836), "−", 58, INK)
    meter(d, AMC, ra, "ampe kế")
    meter(d, VMC, rv, "vôn kế")
    lamp(d, b)
    card(d, (265, 605, 585, 695), fill=WHITE, outline=ORANGE, r=22, w=4)
    text(d, (425, 650), "12 V – 21 W", 56, ORANGE)

def table(d, n, y=1080, hl=None, pcol=False):
    card(d, (60, y, 1020, y + 400), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 540, 850) if pcol else (300, 760)
    hd = ("U (V)", "I (A)", "P (W)") if pcol else ("U (V)", "I (A)")
    for x, c in zip(xs, hd): text(d, (x, y + 56), c, 56, INK)
    d.line([(90, y + 100), (990, y + 100)], fill=LIGHT, width=4)
    for i in range(3):
        yy = y + 160 + i * 84
        if i < n:
            if hl == i: d.rounded_rectangle([80, yy - 38, 1000, yy + 38], radius=18, fill=(255, 237, 213))
            uu, ii = ROWS[i]
            text(d, (xs[0], yy), vn(uu, 1), 58, INK); text(d, (xs[1], yy), vn(ii, 2), 58, INK)
            if pcol: text(d, (xs[2], yy), vn(P_of(i), 2), 58, BLUE)
        else:
            for x in xs: text(d, (x, yy), "·", 58, GRAY)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, 0, "0,00 A", "0,0 V", 0)
    a = appear(t, M[1] - 0.2, 0.4)
    if a <= 0: return
    y0 = 990 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 190), "Hạ nguồn để vôn kế chỉ 6,0 V.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "Đèn còn tiêu thụ", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 380), "khoảng bao nhiêu W?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 485, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (3 muc U trong MOT canh) ----------------
TURN = 0.6
def steps(sc):   # luc bat dau xoay num toi muc k (xoay xong -> so chi + den + hang bang)
    M = sc["M"]
    return [0.3, M[1] + 0.3, M[1] + 2.9]

def do_state(t, sc):
    """-> (u num, so chi ampe, so chi von, do sang, so hang da ghi, hang dang chi hoac None)."""
    st = steps(sc); k = -1
    for j, s0 in enumerate(st):
        if t >= s0: k = j
    if k < 0:
        return 0.0, "0,00 A", "0,0 V", 0.0, 0, None
    s0 = st[k]; u_from = 0.0 if k == 0 else ROWS[k - 1][0]; u_to = ROWS[k][0]
    if t < s0 + TURN:
        x = ease((t - s0) / TURN)
        b0 = 0.0 if k == 0 else P_of(k - 1) / P_DM
        return lerp(u_from, u_to, x), "· · ·", "· · ·", lerp(b0, P_of(k) / P_DM, x), k, None
    return u_to, vn(ROWS[k][1], 2) + " A", vn(u_to, 1) + " V", P_of(k) / P_DM, k + 1, k

def s_do(img, d, t, sc):
    u, ra, rv, b, n, cur = do_state(t, sc)
    circuit(d, u, ra, rv, b)
    table(d, n, hl=cur)

def _kiem_dong_bo():
    """Moi 0,05 s: von ke = muc num khi khong xoay; ampe ke, do sang, hang cuoi bang cung mot hang; P = U.I."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        u, ra, rv, b, n, cur = do_state(t, sc)
        if cur is not None:
            U, I = ROWS[cur]
            ok = (rv == vn(U, 1) + " V" and abs(u - U) < 1e-9 and ra == vn(I, 2) + " A"
                  and abs(b - U * I / P_DM) < 1e-9 and n == cur + 1)
            if not ok: bad.append(round(t, 2))
        elif ra != "· · ·" and not (ra == "0,00 A" and rv == "0,0 V" and b == 0): bad.append(round(t, 2))
        t += 0.05
    for (U, I), (p, r) in zip(ROWS, ((21.0, 6.86), (13.95, 5.81), (7.8, 4.62))):
        if abs(U * I - p) > 0.005 or abs(U / I - r) > 0.005: bad.append(("so", U))
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, W / 2, 290, "ĐÁP ÁN · khoảng 8 W", NAVY)
    table(d, 3, y=380, hl=2 if t >= M[1] - 0.1 else None, pcol=True)
    k = appear(t, M[1] - 0.1, 0.35)
    if k > 0:
        card(d, (40, 830, 1040, 990), fill=A((255, 237, 213), k), outline=A(ORANGE, k), r=20, w=4)
        text(d, (W / 2, 910), "6,0 V × 1,30 A ≈ 7,8 W", 62, (154, 52, 18), alpha=k)
    kr = appear(t, M[2] - 0.1, 0.45)
    if kr > 0:
        y0 = 1040 + (1 - kr) * 30
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pill(d, W / 2, y0 + 70, "RÚT RA", GREEN, kr)
        text(d, (W / 2, y0 + 200), "Đúng 21 W chỉ khi đặt 12 V.", 60, INK, alpha=kr)
        text(d, (W / 2, y0 + 310), "U nhỏ hơn: P nhỏ hơn nhiều.", 60, INK, alpha=kr)

# ---------------- canh 4: Bay (den o 9,0 V) roi Chua noi duoc ----------------
BX0, BXW, PMAX = 100, 640, 16.0
def bar(d, y, label, val, col, k):
    if k <= 0: return
    text(d, (BX0, y), label, 56, INK, anchor="lm", alpha=k)
    L = BXW * val / PMAX
    d.rounded_rectangle([BX0, y + 40, BX0 + L, y + 120], radius=14, fill=A(col, k))
    text(d, (BX0 + L + 20, y + 80), vn(val, 2 if abs(val - round(val, 1)) > 1e-6 else 1) + " W", 58, col, anchor="lm", alpha=k)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.4); k3 = appear(t, M[2] - 0.1, 0.45)
    card(d, (40, 250, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 330), "Đèn ở 9,0 V", 60, INK)
    bar(d, 430, "Nếu R không đổi", round(P_BAY, 1), GRAY, 1.0)
    if k2 > 0:
        bar(d, 640, "Đo thật", P_of(1), GREEN, k2)
    a1 = 1.0 - k3; y0 = 1040
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 520), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y0 + 70, "BẪY", DRED, a1)
        q = "“Đèn có R không đổi”"
        f = F(60); lw = tw(d, q, f); yy = y0 + 210
        text(d, (W / 2, yy), q, 60, mix(INK, GRAY, k2), alpha=a1)
        if k2 > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * k2, yy + 2)], fill=A(DRED, 0.85 * a1), width=7)
            text(d, (W / 2, y0 + 370), "Đèn nguội: R nhỏ hơn", 60, BLUE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y0, 1040, y0 + 520), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y0 + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y0 + 290), "Vừa bật đèn thì sao?", 60, INK, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    """THU NGHI: den 9 V - 4,5 W sang binh thuong -> ampe ke chi bao nhieu? (0,5 A, khong hien)."""
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    if k > 0.5: lamp(d, 0.9, c=(300, 560), r0=70)
    card(d, (560, 460, 900, 660), fill=A(BODY, k), r=22)
    card(d, (575, 475, 885, 570), fill=A(SCR, k), r=10)
    text(d, (730, 522), "? A", 62, (20, 60, 30), alpha=k)
    text(d, (730, 615), "ampe kế", 56, WHITE, bold=False, alpha=k)
    text(d, (W / 2, 820), "Đèn 9 V – 4,5 W", 64, INK, alpha=k)
    text(d, (W / 2, 920), "đang sáng bình thường.", 64, INK, alpha=k)
    text(d, (W / 2, 1040), "Ampe kế chỉ bao nhiêu?", 64, DRED, alpha=k)
    seg_bar(d, 1330, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    st = steps(do)
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + s + TURN, "tick") for s in st]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-nang-luong-dien-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Công suất điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kiểm nhãn đèn xe máy", draw=s_hook, tail=0.3, caps=[
   ("Đèn xe máy, nguồn chỉnh được.", 3.4),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Chỉnh tới 12,0 V, đọc hai đồng hồ.", 4.0),
   ("Hạ xuống 9,0 V rồi 6,0 V.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Nhân U với I ở từng hàng.", 3.6),
   ("Hàng 6,0 V: đèn đỏ mờ.", 3.6),
   ("Nhãn ghi số định mức.", 3.0)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.6, caps=[
   ("Hay nhầm.", 3.6),
   ("Đo được nhiều oát hơn.", 3.6),
   ("Đọc khi số ổn định.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng lại, tự trả lời.", 6.6)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
