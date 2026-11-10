# Clip: tn-l12-xoaychieu-03 - Mot chieu 12 V so voi xoay chieu 12 V hieu dung (ban 1, 28/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-xoaychieu-03.json:
#   tham_so: U = 12 V (mac dinh), R = 12 ohm; so_lieu_mau hang (12; 16,97; 12,0) va (24; 33,94; 48,0);
#   rut_ra: "Dinh ... 12.sqrt(2) ~ 17 V". Dinh p(t) = U0^2/R KHONG in so (khong co trong JSON), chi ghi ky hieu.
# Hop Du doan (dinh tinh, suy tu hien_tuong_hay_sai): A. Khong sang (trung binh u = 0 -> khong toa nhiet),
#   B. Toi hon, C. Sang nhu nhau (dung), D. Sang hon (lay dinh 17 V thay cho 12 V).
# Mau: chuyenthe/thangnhietdo4 (do thi theo thoi gian) + mayphat3 (hop Du doan, chot_hoi, cues).
from engine import *

U, R = 12, 12                       # tham_so
U0_TXT = "12√2 ≈ 17 V"              # cac_buoc.rut_ra
P_TXT = "12,0 W"                    # so_lieu_mau hang U = 12
AMB = (255, 214, 102)
LAMP_GLOW = (255, 196, 61)


# ---------------- ky hieu mach ----------------
def lamp(d, cx, cy, lit, lab=True):
    """Bong den soi dot; lit 0..1 = do sang."""
    if lit > 0:
        for k in range(7, 0, -1):
            r = 50 + k * 16
            dot(d, cx, cy, r, A(LAMP_GLOW, 0.07 * lit))
        for j in range(8):                                      # tia sang
            a = math.radians(j * 45 + 22.5)
            d.line([(cx + 82 * math.cos(a), cy + 82 * math.sin(a)), (cx + 102 * math.cos(a), cy + 102 * math.sin(a))],
                   fill=A(ORANGE, lit), width=6)
    dot(d, cx, cy, 52, mix(WHITE, AMB, lit), outline=NAVY)
    d.line([(cx - 37, cy - 37), (cx + 37, cy + 37)], fill=NAVY, width=5)   # ky hieu den: vong tron + dau X
    d.line([(cx - 37, cy + 37), (cx + 37, cy - 37)], fill=NAVY, width=5)


def battery(d, cx, cy):
    """Ky hieu nguon mot chieu: vach dai mong (+), vach ngan day (-)."""
    d.line([(cx - 14, cy - 48), (cx - 14, cy + 48)], fill=NAVY, width=6)
    d.line([(cx + 14, cy - 26), (cx + 14, cy + 26)], fill=NAVY, width=14)
    text(d, (cx - 40, cy - 56), "+", 40, RED)
    text(d, (cx + 44, cy - 56), "−", 44, NAVY)


def ac_src(d, cx, cy):
    """Ky hieu nguon xoay chieu: vong tron co song sin."""
    dot(d, cx, cy, 46, WHITE, outline=NAVY)
    pts = [(cx - 28 + j * 56 / 30, cy - 15 * math.sin(2 * math.pi * j / 30)) for j in range(31)]
    d.line(pts, fill=ORANGE, width=6, joint="curve")


def vmeter(d, cx, cy, reading):
    card(d, (cx - 74, cy - 58, cx + 74, cy + 58), fill=(255, 236, 160), outline=NAVY, r=18, w=4)
    d.rounded_rectangle([cx - 60, cy - 46, cx + 60, cy + 10], radius=8, fill=NAVY)
    text(d, (cx, cy - 18), reading, 38, (134, 239, 172))
    text(d, (cx, cy + 34), "V~", 32, INK)


def circuit(d, x0, kind, lit, vread="?", lab=True):
    """Mot o mach: den o tren, nguon o duoi, day noi chu nhat. x0 = mep trai o (rong 460)."""
    cx = x0 + 230
    l, r, top, bot = x0 + 60, x0 + 400, 430, 720
    d.line([(l, top), (r, top)], fill=NAVY, width=5)
    d.line([(l, top), (l, bot)], fill=NAVY, width=5); d.line([(r, top), (r, bot)], fill=NAVY, width=5)
    d.line([(l, bot), (cx - 46, bot)], fill=NAVY, width=5); d.line([(cx + 46, bot), (r, bot)], fill=NAVY, width=5)
    d.rectangle([cx - 60, top - 8, cx + 60, top + 8], fill=BG)
    lamp(d, cx, top, lit)
    if kind == "dc":
        d.rectangle([cx - 46, bot - 8, cx + 46, bot + 8], fill=BG)
        d.line([(cx - 46, bot), (cx - 14, bot)], fill=NAVY, width=5); d.line([(cx + 14, bot), (cx + 46, bot)], fill=NAVY, width=5)
        battery(d, cx, bot)
        text(d, (cx, 820), "một chiều", 44, GREEN)
    else:
        ac_src(d, cx, bot)
        for sg in (-1, 1):                                       # von ke mac song song hai dau nguon
            d.line([(cx + sg * 74, 590), (cx + sg * 112, 590), (cx + sg * 112, bot)], fill=NAVY, width=4, joint="curve")
            dot(d, cx + sg * 112, bot, 11, NAVY)
        vmeter(d, cx, 590, vread)
        text(d, (cx, 820), "xoay chiều", 44, ORANGE)
    if lab: text(d, (cx, 285), "bóng 12 Ω", 38, INK, bold=False)


def two_circuits(d, lit_dc, lit_ac, vread):
    card(d, (40, 250, 530, 870), fill=WHITE, outline=LIGHT, w=3)
    card(d, (550, 250, 1040, 870), fill=WHITE, outline=LIGHT, w=3)
    circuit(d, 55, "dc", lit_dc)
    circuit(d, 565, "ac", lit_ac, vread)


# ---------------- do thi theo thoi gian ----------------
GX0, GX1 = 190, 990
def axes(d, ytop, ybot, vmin, vmax, ticks, ylab, ycol=INK):
    Y = lambda v: ybot - (v - vmin) / (vmax - vmin) * (ybot - ytop)
    y0 = Y(0)
    for v, s in ticks:
        d.line([(GX0, Y(v)), (GX1, Y(v))], fill=(236, 232, 222), width=2)
        d.line([(GX0 - 10, Y(v)), (GX0, Y(v))], fill=NAVY, width=4)
        text(d, (GX0 - 18, Y(v)), s, 34, INK, bold=False, anchor="rm")
    d.line([(GX0, y0), (GX1 + 20, y0)], fill=NAVY, width=5)
    d.line([(GX0, ybot + 10), (GX0, ytop - 30)], fill=NAVY, width=5)
    text(d, (GX0 + 16, ytop - 34), ylab, 36, ycol, anchor="lm")
    text(d, (GX1 + 20, y0 + 34), "t", 36, INK, anchor="rm")
    return Y


PER = 2.6                                     # so chu ki ve tren truc t
def u_ac(x): return U * math.sqrt(2) * math.cos(2 * math.pi * PER * x)


def curve(d, f, Y, k, color, w=6, x0=0.0):
    if k <= 0: return
    n = int(240 * k); pts = []
    for j in range(n + 1):
        x = x0 + (1 - x0) * j / 240
        pts.append((lerp(GX0, GX1, x), Y(f(x))))
    if len(pts) > 1: d.line(pts, fill=color, width=w, joint="curve")


def dashed_h(d, y, x0, x1, color, w=4, dash=18, gap=12, a=1.0):
    x = x0
    while x < x1:
        d.line([(x, y), (min(x + dash, x1), y)], fill=A(color, a), width=w); x += dash + gap


# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. Không sáng", "B. Tối hơn", "C. Sáng như nhau", "D. Sáng hơn")
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    two_circuits(d, 0, 0, "12 V")
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 960, 1020, 1640), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1015), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1135, "Đèn xoay chiều so với một chiều sẽ:", 46, INK, maxw=860, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.12)
        x0 = 100 + (i % 2) * 450; y = 1310 + (i // 2) * 120
        card(d, (x0, y - 48, x0 + 430, y + 48), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=22, w=4)
        text(d, (x0 + 34, y), s, 42, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1580, 940, 1594], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1580, 140 + 800 * (1 - q), 1594], radius=7, fill=A(PURPLE, k))


# ---------------- canh 2: tien hanh, ve u(t) ----------------
UY0, UY1 = 960, 1520                           # vung do thi u(t)
def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    on_dc = appear(t, M[0] + 0.5, 0.4)
    mac = M[0] + 3.0
    on_ac = appear(t, mac + 0.6, 0.4)
    vr = "12 V" if t > mac + 0.4 else "0 V"
    two_circuits(d, on_dc, on_ac, vr)
    card(d, (40, 900, 1040, 1580), fill=WHITE, outline=LIGHT, w=3)
    Y = axes(d, UY0 + 40, UY1, -20, 20, [(-17, "−17"), (12, "12"), (17, "17"), (0, "0")], "u (V)")
    text(d, (1010, 1552), "minh hoạ", 36, MUTED, anchor="rm")
    curve(d, lambda x: U, Y, ease((t - M[0] - 0.6) / 1.0), GREEN, w=7)
    if t > M[0] + 1.2:
        text(d, (lerp(GX0, GX1, 0.19), Y(U) - 30), "một chiều", 34, GREEN)
    curve(d, u_ac, Y, ease((t - mac - 0.7) / 1.6), ORANGE, w=6)
    a = appear(t, M[1] - 0.2)
    if a > 0:                                                     # danh dau dinh U0
        xp = lerp(GX0, GX1, 1 / PER)
        dashed_h(d, Y(17), GX0, GX1, RED, a=a)
        dot(d, xp, Y(U * math.sqrt(2)), 13, RED, outline=WHITE)
        card(d, (580, 935, 980, 1007), fill=A(WHITE, a), outline=A(RED, a), r=20)   # tren vung duong cong (dinh o Y(17))
        text(d, (780, 971), "U₀ = " + U0_TXT, 36, RED, alpha=a)
        d.line([(580, 990), (xp + 14, Y(17) - 10)], fill=A(RED, a), width=4)
    b = appear(t, M[1] + 2.0, 0.4)
    if b > 0:
        card(d, (60, 1590, 1020, 1662), fill=A((220, 252, 231), b), outline=A(GREEN, b), r=24, w=4)
        text(d, (W / 2, 1626), "Đáp án C", 52, GREEN, alpha=b)


# ---------------- canh 3: vi sao - cong suat p(t) ----------------
PY0, PY1 = 300, 860
def p_ac(x): return u_ac(x) ** 2 / R


def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (40, 250, 1040, 1040), fill=WHITE, outline=LIGHT, w=3)
    Y = axes(d, PY0 + 60, PY1, 0, 30, [(0, "0"), (12, "12")], "p = u²/R (W)")
    text(d, (1010, PY0 - 6), "minh hoạ", 36, MUTED, anchor="rm")
    kp = ease((t - 0.5) / 1.6)
    curve(d, p_ac, Y, kp, ORANGE, w=6)
    if kp >= 1:
        xp = lerp(GX0, GX1, 1 / PER)
        dashed_h(d, Y(U * U * 2 / R), GX0, GX1, ORANGE, w=3, dash=10, gap=12)
        text(d, (600, 412), "đỉnh gấp 2", 40, ORANGE)      # vung trong 360-460, duong cong khong toi
    a = appear(t, M[1] - 0.2)
    if a > 0:                                                     # mot chieu + duong trung binh
        d.line([(GX0, Y(U * U / R)), (GX1, Y(U * U / R))], fill=A(GREEN, a), width=10)   # net dut de len net lien: trung
        dashed_h(d, Y(U * U / R), GX0, GX1, PURPLE, w=5, a=a)
        d.line([(110, 893), (180, 893)], fill=A(GREEN, a), width=10)
        text(d, (200, 893), "một chiều: " + P_TXT, 38, GREEN, anchor="lm", alpha=a)
        dashed_h(d, 940, 110, 180, PURPLE, w=5, a=a)
        text(d, (200, 940), "xoay chiều: p trung bình " + P_TXT, 38, PURPLE, anchor="lm", alpha=a)
    # the giai thich
    c2 = appear(t, M[1] + 2.0) * (1 - appear(t, M[2] - 0.3))
    if c2 > 0:
        card(d, (60, 1110, 1020, 1330), fill=A((236, 253, 243), c2), outline=A(GREEN, c2), w=5)
        text(d, (W / 2, 1220), "12 V gọi là HIỆU DỤNG", 54, GREEN, alpha=c2)
    c3 = appear(t, M[2] - 0.3)
    if c3 > 0:
        card(d, (60, 1070, 1020, 1520), fill=A(WHITE, c3), outline=A(NAVY, c3), w=5)
        text(d, (W / 2, 1130), "Chưa nói được", 48, NAVY, alpha=c3)
        for j, s in enumerate(("Chưa đo công suất", "Chưa thấy √2 từ đâu")):
            y = 1260 + j * 110
            text(d, (W / 2, y), s, 46, INK, alpha=c3)


# ---------------- canh 4: hai cai bay ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 340), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 295), "Hai bẫy", 48, RED)
    # bay 1: u trung binh 0 -> van toa nhiet (hinh co ngay tu dau canh)
    card(d, (40, 370, 1040, 1060), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 410), "1. u trung bình = 0?", 42, INK, anchor="lm")
    Yu = axes(d, 500, 700, -20, 20, [(0, "0")], "u")
    for j in range(240):                                          # to phan am do, phan duong cam
        x = j / 240; v = u_ac(x)
        col = RED if v < 0 else ORANGE
        d.line([(lerp(GX0, GX1, x), Yu(0)), (lerp(GX0, GX1, x), Yu(v))], fill=A(col, 0.25), width=4)
    curve(d, u_ac, Yu, 1.0, ORANGE, w=5)
    Yp = axes(d, 800, 1000, 0, 26, [(0, "0")], "p")
    curve(d, p_ac, Yp, ease((t - 0.6) / 1.2), ORANGE, w=5)
    a1 = appear(t, 1.4)
    text(d, (GX1, 770), "p luôn ≥ 0: vẫn toả nhiệt", 40, GREEN, anchor="rm", alpha=a1)
    # bay 2: dung U0 thay U
    a2 = appear(t, M[1] - 0.3)
    if a2 <= 0: return
    card(d, (40, 1090, 1040, 1620), fill=A(WHITE, a2), outline=A(RED, a2), w=5)
    text(d, (80, 1140), "2. Dùng U₀ thay U", 44, INK, anchor="lm", alpha=a2)
    # dong sai
    y = 1300
    d.line([(110, y - 20), (150, y + 20)], fill=A(RED, a2), width=9); d.line([(150, y - 20), (110, y + 20)], fill=A(RED, a2), width=9)
    text(d, (180, y), "U₀ ≈ 17 V: P gấp đôi", 44, RED, anchor="lm", alpha=a2)
    a3 = appear(t, M[1] + 1.8)
    y = 1420
    d.line([(108, y + 2), (126, y + 22)], fill=A(GREEN, a3), width=9); d.line([(126, y + 22), (156, y - 20)], fill=A(GREEN, a3), width=9)
    rich(d, 180, y, "P = U^{2}/R = 12^{2}/12 = " + P_TXT, 42, GREEN, alpha=a3, anchor="l")
    text(d, (W / 2, 1530), "U: giá trị hiệu dụng", 46, INK, alpha=a3)


# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    chot_hoi(d, t, sc, "Xoay chiều 12 V hiệu dụng\ntoả nhiệt như một chiều 12 V",
             "Vôn kế xoay chiều chỉ 24 V, bóng 12 Ω. Công suất toả nhiệt trung bình bao nhiêu?")
    kh = appear(t, sc["M"][0] + 3.0, 0.4)                # goi y hien sau 3 s
    if kh > 0:
        card(d, (110, 1120, 970, 1400), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1175), "Gợi ý", 38, INK, alpha=kh)
        ctext(d, 1295, "Dùng U hay U₀?", 50, ORANGE, maxw=800, alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, wy, tr, e = sc["hook"], sc["do"], sc["why"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][0] + 0.5, "tap"), (do["t0"] + do["M"][0] + 3.6, "tap"),
            (do["t0"] + do["M"][1] + 1.9, "ding"), (wy["t0"] + wy["M"][2] - 0.3, "tap"),
            (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]


CLIP = dict(id="tn-l12-xoaychieu-03", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Dòng điện xoay chiều · thachlab.id.vn", scenes=[
 dict(key="hook", title="Một chiều hay xoay chiều?", draw=s_hook, tail=0.4, caps=[
   "Một đèn, hai nguồn 12 V.",
   ("Dừng video, chọn một đáp án.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Một chiều, rồi xoay chiều.", 5.4),
   ("Hai đèn sáng như nhau.", 4.5)]),
 dict(key="why", title="Vì sao sáng như nhau?", draw=s_why, tail=0.6, caps=[
   ("Công suất p luôn dương.", 4.0),
   ("Cùng công suất trung bình 12 W.", 4.4),
   ("Giới hạn của thí nghiệm.", 3.4)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.5, caps=[
   ("Nhìn đồ thị p.", 4.2),
   ("Bẫy 2: nhầm U với U₀.", 5.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.9, caps=[
   ("Dừng video và trả lời.", 7.4)]),
])
