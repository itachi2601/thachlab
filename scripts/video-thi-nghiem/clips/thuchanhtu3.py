# Clip: tn-l12-thuchanhtu-03 - Day hop goc theta voi duong suc: can giam theo sin theta, B khong doi
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanhtu-03.json (ghi chu JSON: "so lieu minh hoa"):
#   tham_so I = 3,0 A; so_lieu_mau (theta, dm g, sin, ti so): 90 1,45 1,0 1,0 | 60 1,26 0,866 0,869 | 30 0,73 0,5 0,503
#   mo_hinh: F = B.I.l.sin theta, B = 0,12 T (nam cham khong doi khi xoay day).
# Du doan (90 do -> +1,45 g; xoay toi 30 do): dap an 0,73 g (khung web hoi A-D, clip khong ve nut - K10).
# Bay (quan niem sai hien_tuong_hay_sai[0]): "can giam -> B giam?" -> ca 90/60 do (khong lap cap 90/30 cua Du doan):
#   duong suc y nguyen, B = 0,12 T ca hai, chi luc tu nho di (khong chieu 0,87 / B tinh ra: Cau 6 cua bai).
# Chot (cau_chot khung, v2): day nghieng sang ben kia, van 60 do voi duong suc -> can +1,26 g (so kho, hang 60 do).
#   Buoc suy luan: luc chi phu thuoc goc giua day va duong suc; I x B van huong len (+z) nen khong doi dau.
#   Ca 0 do (v1) bi bo: chi the sin 0 = 0, qua de.
# Hinh: nhin tu tren xuong; N (trai) -> S (phai), duong suc ngang. Day nghieng goc theta so voi duong suc.
# Ban 2 (21/11/2026, viec 4 lo 20): cong --do-chu moi: chu than canh >= 56 px, bo chu xam, bo do thi Δm-θ (duong cong qua
#   goc toa do lo dap an cau chot), Du doan khong nut A-D + dem nguoc 5 cham, Bay 4 nhip ~3 s hinh tu giai thich, chot moi.
from engine import *
from PIL import ImageFont as _IF

ROWS = [(90, 1.45, 1.0, 1.0), (60, 1.26, 0.866, 0.869), (30, 0.73, 0.5, 0.503)]
COPPER = (184, 115, 51)
FIELD = (120, 145, 200)
SCREEN = (24, 30, 40); SCR_TXT = (134, 239, 172)
DARK_OR = (181, 71, 8)                         # #B54708: chu cam tren nen sang >= 4,5:1


def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")


_FL = {}
def FL(size):
    """l nghieng (Georgia Bold Italic) de khong lan voi I trong phong sans."""
    if size not in _FL: _FL[size] = _IF.truetype("/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf", size)
    return _FL[size]


def seq(d, x, y, parts, alpha=1.0, center=False):
    ws = [tw(d, s, f) + (4 if f in _FL.values() else 0) for s, f, c in parts]
    if center: x -= sum(ws) / 2
    for (s, f, c), w in zip(parts, ws):
        dtext(d, (x, y), s, f, c, alpha, anchor="lm"); x += w


def chevron(d, x, y, ang, color, s=14, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)


def dashed(d, p1, p2, color, w=3, dash=12, gap=9):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))],
               fill=color, width=w)


def pill(d, cx, cy, s, size, bg, alpha=1.0, h=80):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - h / 2, cx + pw / 2, cy + h / 2), fill=A(bg, alpha), r=int(h / 2))
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)


def screen(d, box, s, color=SCR_TXT, size=60, alpha=1.0):
    card(d, box, fill=A(SCREEN, alpha), r=14)
    text(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), s, size, color, alpha=alpha)


# ---------------- hinh nhin tu tren (to): hai cuc + duong suc + day ----------------
BOX = (40, 240, 1040, 800)
CX, CY, HL = 540, 535, 190


def wire_ends(cx, cy, hl, th):
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    return (cx + hl * c, cy - hl * s), (cx - hl * c, cy + hl * s)      # dau tren-phai, dau duoi-trai


def top_view(d, th, on=True, label=True, mirror=False):
    """mirror=True: day nghieng sang ben kia (dau tren-trai), goc voi duong suc van la th (do tu nua trai)."""
    card(d, BOX, fill=WHITE, outline=LIGHT, w=3)
    for k in range(7):
        y = 345 + 64 * k
        d.line([(150, y), (930, y)], fill=FIELD, width=4)
        for x in (290, 800): chevron(d, x, y, 0, FIELD, s=16, w=4)
    d.rounded_rectangle([60, 320, 140, 760], radius=10, fill=RED)
    d.rounded_rectangle([940, 320, 1020, 760], radius=10, fill=BLUE)
    text(d, (100, 540), "N", 60, WHITE); text(d, (980, 540), "S", 60, WHITE)
    if label: text(d, (70, 282), "nhìn từ trên", 56, INK, anchor="lm")
    arrow(d, (770, 282), (870, 282), BLUE, w=6, head=20); text(d, (892, 282), "B", 60, BLUE, anchor="lm")
    td = 180 - th if mirror else th; sg = -1 if mirror else 1
    pa, pb = wire_ends(CX, CY, HL, td)
    if th > 1:                                    # goc theta giua day va duong suc
        d.line([(CX, CY), (CX + sg * 160, CY)], fill=GREEN, width=6)
        if mirror: d.arc([CX - 100, CY - 100, CX + 100, CY + 100], 180, 180 + th, fill=GREEN, width=7)
        else: d.arc([CX - 100, CY - 100, CX + 100, CY + 100], 360 - th, 360, fill=GREEN, width=7)
        am = math.radians(180 - th / 2 if mirror else th / 2)
        tx, ty = CX + 148 * math.cos(am), CY - 148 * math.sin(am)
        d.rounded_rectangle([tx - 30, ty - 36, tx + 30, ty + 36], radius=10, fill=WHITE)
        text(d, (tx, ty), "θ", 60, GREEN)
    d.line([pa, pb], fill=COPPER, width=18)
    for p in (pa, pb): dot(d, p[0], p[1], 12, COPPER, outline=WHITE)
    if on:                                        # chieu dong: dau tren -> dau duoi; mui ten + nhan I phia khong co goc
        c, s = math.cos(math.radians(td)), math.sin(math.radians(td))
        ox, oy = -sg * 46 * s, -sg * 46 * c
        m1 = (CX + 0.9 * HL * c + ox, CY - 0.9 * HL * s + oy); m2 = (CX + 0.3 * HL * c + ox, CY - 0.3 * HL * s + oy)
        arrow(d, m1, m2, ORANGE, w=9, head=28)
        lx, ly = CX + 0.6 * HL * c - sg * 100 * s, CY - 0.6 * HL * s - sg * 100 * c
        d.rounded_rectangle([lx - 26, ly - 34, lx + 26, ly + 34], radius=10, fill=WHITE)
        text(d, (lx, ly), "I", 60, ORANGE)


def readout(d, th, s, color=SCR_TXT, alpha=1.0):
    """Hang duoi hinh: goc theta + man can."""
    card(d, (40, 820, 1040, 980), fill=WHITE, outline=NAVY, w=4, r=24)
    text(d, (80, 900), f"θ = {round(th)}°", 62, GREEN, anchor="lm")
    text(d, (560, 900), "cân", 60, NAVY, anchor="rm")
    screen(d, (600, 845, 1010, 955), s, color)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    top_view(d, 90)
    readout(d, 90, "+1,45 g")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", 56, PURPLE, a)
    text(d, (W / 2, y0 + 200), "I = 3,0 A giữ nguyên.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 300), "Xoay dây tới θ = 30°.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 400), "Cân chỉ bao nhiêu?", 62, INK, alpha=a)     # K10: khong ve nut A-D
    tc, tend = M[1] + 0.3, sc["T"] - 0.1                # dem nguoc 5 cham
    n_off = 0 if t < tc else min(5, int((t - tc) / ((tend - tc) / 5)) + 1)
    for j in range(5):
        dot(d, W / 2 + (j - 2) * 140, y0 + 540, 40, A(LIGHT, a) if j >= 5 - n_off else A(PURPLE, a))


# ---------------- canh 2: Tien hanh ----------------
def state(t, sc):
    """(theta, dong dien bat?, so hang da ghi)"""
    M = sc["M"]; th = 90.0; on = True; n = 1
    for mk, a0, a1 in ((M[0], 90, 60), (M[1], 60, 30)):
        if t >= mk + 0.1:
            on = False; th = lerp(a0, a1, ease((t - mk - 0.3) / 1.3))
        if t >= mk + 1.8: on = True
        if t >= mk + 2.0: n += 1
    return th, on, n


def bars(d, y0, n, hl=None, alpha=1.0):
    """Bang so do: goc + so can + thanh dai ti le Δm."""
    card(d, (40, y0, 1040, y0 + 620), fill=A(WHITE, alpha), outline=A(NAVY, alpha), w=4)
    text(d, (140, y0 + 60), "θ", 62, NAVY, alpha=alpha)
    text(d, (350, y0 + 60), "Δm (g)", 62, NAVY, alpha=alpha)
    d.line([(70, y0 + 110), (1010, y0 + 110)], fill=A(NAVY, alpha), width=3)
    for j, (a, dm, _, _) in enumerate(ROWS[:n]):
        yy = y0 + 200 + j * 160
        if hl == j: d.rounded_rectangle([60, yy - 66, 1020, yy + 66], radius=16, fill=A((255, 237, 213), alpha))
        text(d, (140, yy), f"{a}°", 62, INK, alpha=alpha)
        text(d, (350, yy), vn(dm), 62, INK, alpha=alpha)
        d.rounded_rectangle([480, yy - 28, 480 + 500 * dm / 1.45, yy + 28], radius=10, fill=A(ORANGE, alpha))


def s_do(img, d, t, sc):
    th, on, n = state(t, sc)
    top_view(d, th, on=on)
    if on: readout(d, th, f"+{vn(ROWS[n - 1][1])} g")
    else: readout(d, th, "– – –", color=(252, 165, 165))
    bars(d, 1010, n, hl=n - 1)


# ---------------- canh 3: Dap an + ti so ----------------
def glyph(d, x, y, th, L=50, alpha=1.0):
    """Hinh nho: mot duong suc ngang + doan day nghieng goc th."""
    d.line([(x - 60, y), (x + 60, y)], fill=A(FIELD, alpha), width=4); chevron(d, x + 60, y, 0, A(FIELD, alpha))
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    d.line([(x - L * c, y + L * s), (x + L * c, y - L * s)], fill=A(COPPER, alpha), width=12)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, M[0], 0.4)
    if ka > 0: pill(d, W / 2, 300, "ĐÁP ÁN: 0,73 g", 58, GREEN, ka)
    card(d, (40, 370, 1040, 1010), fill=WHITE, outline=NAVY, w=4)
    for x, h in ((300, "θ"), (640, "Δm (g)")): text(d, (x, 430), h, 56, NAVY)
    d.line([(70, 475), (1010, 475)], fill=NAVY, width=3)
    for j, (a, dm, sn, rt) in enumerate(ROWS):
        yy = 580 + j * 165
        if j == 2: d.rounded_rectangle([60, yy - 75, 1020, yy + 75], radius=16, fill=(255, 237, 213))
        glyph(d, 140, yy, a)
        text(d, (300, yy), f"{a}°", 62, INK)
        text(d, (640, yy), vn(dm), 62, INK)
    kc = appear(t, M[1] - 0.1, 0.45)
    if kc > 0:                                    # chi kiem ca 30 do (khong chieu 0,87 = sin 60, Cau 6 cua bai)
        card(d, (40, 1050, 1040, 1250), fill=A(WHITE, kc), outline=A(GREEN, kc), w=5)
        text(d, (W / 2, 1150), "0,73 : 1,45 ≈ 0,50 = sin 30°", 62, GREEN, alpha=kc)
    ke = appear(t, M[1] + 2.0, 0.45)
    if ke > 0:
        card(d, (40, 1290, 1040, 1490), fill=A((236, 253, 243), ke), outline=A(GREEN, ke), w=5)
        text(d, (W / 2, 1390), "Δm = 1,45 g · sin θ", 66, GREEN, alpha=ke)


# ---------------- canh 4: Bay (4 nhip ~3 s, moi nhip mot phu de) ----------------
MINI = ((40, 90, 1.45), (555, 60, 1.26))          # (x0, theta, so can) - khong lap cap 90/30 cua Du doan


def mini(d, x0, th, field_hl=0.0, proj=0.0):  # proj: khong dung (v2)
    y0, y1 = 450, 960; cx, cy = x0 + 225, 705; hl = 150
    card(d, (x0, y0, x0 + 485, y1), fill=WHITE, outline=LIGHT, w=3)
    d.rounded_rectangle([x0 + 14, 480, x0 + 54, 930], radius=8, fill=RED)
    d.rounded_rectangle([x0 + 431, 480, x0 + 471, 930], radius=8, fill=BLUE)
    col = mix(FIELD, PURPLE, field_hl)
    for k in range(6):
        y = 535 + 68 * k
        d.line([(x0 + 64, y), (x0 + 421, y)], fill=col, width=4 + int(3 * field_hl))
        chevron(d, x0 + 105, y, 0, col, s=15, w=4 + int(2 * field_hl))
    pa, pb = wire_ends(cx, cy, hl, th)
    d.line([pa, pb], fill=COPPER, width=16)
    for p in (pa, pb): dot(d, p[0], p[1], 10, COPPER, outline=WHITE)
    if proj > 0:                                  # phan day vuong goc duong suc: doan xanh doc ben phai + gióng
        xp = cx + 130; h = hl * math.sin(math.radians(th))
        for p in (pa, pb):
            if abs(p[0] - xp) > 30: dashed(d, (p[0] + 12, p[1]), (xp - 4, p[1]), A(GREEN, proj), w=4)
        d.line([(xp, cy - h), (xp, cy + h)], fill=A(GREEN, proj), width=12)
        for yy in (cy - h, cy + h): d.line([(xp - 20, yy), (xp + 20, yy)], fill=A(GREEN, proj), width=7)


def s_bay(img, d, t, sc):
    M = sc["M"]; b1, b2, b3 = (m - 0.1 for m in M)
    k1 = appear(t, b1, 0.4); k2 = appear(t, b2, 0.5); k3 = appear(t, b3, 0.4)
    pill(d, W / 2, 290, "BẪY", 56, RED, k1)
    text(d, (W / 2, 392), "Cân giảm → B giảm?", 62, INK, alpha=k1)
    if k3 > 0:
        pw = tw(d, "SAI", F(56)) + 50
        card(d, (1030 - pw, 250, 1030, 330), fill=A(RED, k3), r=40)
        text(d, (1030 - pw / 2, 290), "SAI", 56, WHITE, alpha=k3)
    for x0, th, dm in MINI:
        mini(d, x0, th, field_hl=k2)
        text(d, (x0 + 95, 1040), f"{th}°", 62, GREEN)
        screen(d, (x0 + 170, 990, x0 + 470, 1090), f"+{vn(dm)} g")
        if k2 > 0: text(d, (x0 + 242, 1170), "B = 0,12 T", 62, PURPLE, alpha=k2)
    if k3 > 0:
        card(d, (40, 1260, 1040, 1640), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1360), "B không đổi", 66, GREEN, alpha=k3)
        text(d, (W / 2, 1520), "Chỉ lực từ nhỏ đi", 64, INK, alpha=k3)


# ---------------- canh 5: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Chưa đổi chiều dài dây", "• Số liệu minh hoạ")):
        text(d, (100, 600 + j * 300), s, 62, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 800), "?", 260, NAVY, alpha=k * (1 - kb))


# ---------------- canh 6: THU NGHI (dung ca cau_chot cua khung) ----------------
def s_end(img, d, t, sc):
    top_view(d, 60, on=True, label=False, mirror=True)
    kq = appear(t, 2.6, 0.4)
    card(d, (40, 820, 1040, 980), fill=WHITE, outline=NAVY, w=4, r=24)
    text(d, (80, 900), "θ = 60°", 62, GREEN, anchor="lm")
    text(d, (560, 900), "cân", 60, NAVY, anchor="rm")
    card(d, (600, 845, 1010, 955), fill=SCREEN, r=14)
    if kq > 0:
        d.rounded_rectangle([588, 833, 1022, 967], radius=20, outline=A(ORANGE, kq), width=10)
        text(d, (805, 900), "?", 80, SCR_TXT, alpha=kq)
    k = appear(t, 0.3, 0.5)
    if k <= 0: return
    card(d, (50, 1025, 1030, 1600), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1100, "THỬ NGHĨ", 56, DARK_OR, k)
    text(d, (W / 2, 1270), "Dây nghiêng sang bên kia.", 62, INK, alpha=k)
    text(d, (W / 2, 1400), "Cân chỉ bao nhiêu?", 64, DARK_OR, alpha=k)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, g, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "gioi", "end"))
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][0] + 2.0, "tap"), (do["t0"] + do["M"][1] + 2.0, "tap"),
            (da["t0"] + da["M"][0], "ding"),
            (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"), (g["t0"] + 2.4, "tap"),
            (e["t0"] + 0.3, "open")]


CLIP = dict(id="tn-l12-thuchanhtu-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Đo cảm ứng từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xoay dây trong từ trường", draw=s_hook, tail=0.3, caps=[
   "Dây vuông góc đường sức.",
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Ngắt mạch, xoay tới 60°.", 3.2),
   ("Xoay tiếp tới 30°.", 3.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("So với 1,45 g: còn một nửa.", 3.0),
   ("Thử tỉ số ở 30°.", 3.4)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("Nam châm vẫn y nguyên.", 3.2),
   ("Sai: cùng một nam châm.", 3.4)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Còn chưa xét gì?", 4.2)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự đoán.", 4.4)]),
])
