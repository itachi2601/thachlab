# Clip: tn-l10-trong-luc-luc-cang-03 - Luc ke keo day vat qua rong roc co dinh theo nhieu huong (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-trong-luc-luc-cang-03.json:
#   so_lieu_mau: beta 0 / 45 / 90 do -> T = 1,0 N ca ba lan ; tham_so: P = 1,0 N, luc ke 0-2,5 N, sai so 0,05 N,
#   beta 0-90 buoc 15 (cau hoi chot dung 60 do, chua tung hien tren man).
# Canh: Du doan (chi cau hoi + hinh, K10: khong ve nut A/B/C) -> Tien hanh (xoay huong keo 0 -> 45 -> 90 trong MOT canh,
#       bang so lieu) -> Dap an B + co che (T hai ben bang nhau, vat dung yen nen T = P) -> Bay + chua noi duoc
#       (ma sat truc) -> Chot + cau hoi tu nho lai (60 do).
# Hinh: day vat qua dinh rong roc; doan ben luc ke roi rong roc tai diem tiep tuyen C + r(cos b, -sin b),
#       huong u = (sin b, cos b) (b = 0: thang xuong, b = 90: nam ngang sang phai).
from engine import *

# ---------------- bo cuc (khung nguon 1080x1920, vung ve y 285..1600) ----------------
CX, CY, R = 400, 450, 64             # tam + ban kinh rong roc
CEIL = 352                           # tran / gia treo
WX = CX - R                          # day ben qua nang (thang dung)
WY0, WY1 = 700, 800                  # qua nang
P_TXT = "1,0 N"                      # tham_so P
ROPE, BODY = 110, 330                # doan day tu rong roc toi moc luc ke ; chieu dai than luc ke
FMAX = 2.5                           # thang luc ke (dung_cu)
ROWS = [("thẳng đứng", 0), ("chếch", 45), ("nằm ngang", 90)]   # so_lieu_mau: T = 1,0 N ca ba
SKIN = (240, 196, 160)
DRED = (185, 28, 28)                 # do dam cho chu tren nen hong/trang

def dashed(d, p, q, color, w=3, seg=12, gap=9):
    L = math.dist(p, q); n = int(L // (seg + gap)) + 1
    for k in range(n):
        a = k * (seg + gap) / L; b = min(1, (k * (seg + gap) + seg) / L)
        if a >= 1: break
        d.line([(lerp(p[0], q[0], a), lerp(p[1], q[1], a)), (lerp(p[0], q[0], b), lerp(p[1], q[1], b))], fill=color, width=w)

def tangent(beta):
    b = math.radians(beta)
    return (CX + R * math.cos(b), CY - R * math.sin(b)), (math.sin(b), math.cos(b))

def support(d):
    d.rectangle([260, CEIL - 26, 470, CEIL], fill=(176, 124, 74))     # ngan: so vach luc ke nam ngang nam tren day
    for x in range(270, 440, 34): d.line([(x, CEIL - 26), (x + 22, CEIL - 50)], fill=(150, 105, 62), width=4)
    d.line([(CX, CEIL), (CX, CY)], fill=(120, 125, 140), width=12)

def pulley(d):
    dot(d, CX, CY, R + 6, (90, 98, 120))
    dot(d, CX, CY, R - 10, (200, 205, 218))
    dot(d, CX, CY, 12, NAVY)

def weight(d, label=True):
    d.line([(WX, CY), (WX, WY0)], fill=NAVY, width=5)
    d.line([(WX, WY0), (WX, WY0 - 18)], fill=NAVY, width=7)
    d.rounded_rectangle([WX - 62, WY0, WX + 62, WY1], radius=12, fill=(90, 98, 120))
    if label: text(d, (WX, (WY0 + WY1) / 2), P_TXT, 38, WHITE)

def scale(d, beta, f_read, hand=True, alpha=1.0):
    """Day tu rong roc toi moc luc ke + luc ke lo xo (mau trongluc2: 0-2,5 N, vach 0,05 N) + tay keo, theo huong beta."""
    (tx, ty), (ux, uy) = tangent(beta); nx, ny = -uy, ux
    P = lambda s, n=0.0: (tx + ux * s + nx * n, ty + uy * s + ny * n)
    a0 = 180; a1 = 360 - beta
    d.arc([CX - R, CY - R, CX + R, CY + R], a0, a1, fill=A(NAVY, alpha), width=5)
    d.line([P(0), P(ROPE - 13)], fill=A(NAVY, alpha), width=5)
    se = luc_ke(d, P, ROPE, ROPE + 20, ROPE + 20 + BODY, FMAX, f_read, nho=0.05, so=(0, 1, 2), ben=-1, alpha=alpha)
    if hand:
        hx, hy = P(se + 34)
        d.line([P(se - 16), P(se + 8)], fill=A(NAVY, alpha), width=8)
        dot(d, hx, hy, 34, A(SKIN, alpha), outline=A((190, 140, 105), alpha))

def angle_mark(d, beta, alpha=1.0):
    """Goc beta do tai moc luc ke: giua phuong thang dung (net dut, huong xuong) va day."""
    if beta < 5: return
    (tx, ty), (ux, uy) = tangent(beta)
    hx, hy = tx + ux * ROPE, ty + uy * ROPE
    dashed(d, (hx, hy), (hx, hy + 170), A(MUTED, alpha), w=3)
    rr = 100; edge = math.degrees(math.asin(54 / rr))       # cung dung o mep than luc ke (nua be rong 48 + vien)
    d.arc([hx - rr, hy - rr, hx + rr, hy + rr], 90 - beta + edge, 90, fill=A(ORANGE, alpha), width=5)
    mid = math.radians(90 - (beta - edge) / 2)
    text(d, (hx + 200 * math.cos(mid), hy + 200 * math.sin(mid)), f"{beta}°", 40, ORANGE, alpha=alpha)

def readout(d, val, note=None):
    card(d, (700, 815, 1040, 1028), fill=WHITE, outline=LIGHT, r=26, w=3)
    text(d, (870, 855), "Lực kế chỉ", 38, INK, bold=False)
    text(d, (870, 925), val, 62, INK)
    if note: text(d, (870, 990), note, 36, ORANGE)

def rig(d, beta, f_read, val, note=None, label=True):
    support(d); weight(d, label); scale(d, beta, f_read); pulley(d); angle_mark(d, beta); readout(d, val, note)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong ve nut lua chon) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0, 1.0, P_TXT)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    # huong keo moi (nam ngang) ve net dut + dau hoi
    (tx, ty), _ = tangent(90)
    dashed(d, (tx, ty), (tx + 380, ty), A(ORANGE, a), w=5)
    arrow(d, (tx + 340, ty), (tx + 400, ty), A(ORANGE, a), w=5)
    dot(d, tx + 470, ty, 40, A(ORANGE, a)); text(d, (tx + 470, ty + 2), "?", 50, WHITE, alpha=a)
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 230, "Kéo dây nằm ngang,\nquả nặng vẫn đứng yên.\nLực kế chỉ bao nhiêu?", 46, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 482], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 482], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (xoay huong keo trong MOT canh) ----------------
MOVE = 1.0          # giay xoay huong keo
def beta_at(t, sc):
    M = sc["M"]
    if t < M[1]: return 0.0
    if t < M[2]: return lerp(0, 45, ease((t - M[1]) / MOVE))
    return lerp(45, 90, ease((t - M[2]) / MOVE))
def rows_shown(t, sc):
    M = sc["M"]
    return sum(t >= M[i] + 1.6 for i in range(3))

def chips(d, cur):
    for j, s in enumerate(("0°", "45°", "90°")):
        x0 = 150 + j * 270; box = (x0, 226, x0 + 240, 284)
        if j == cur: card(d, box, fill=ORANGE, r=27); text(d, (x0 + 120, 255), s, 38, WHITE)
        elif j < cur: card(d, box, fill=LIGHT, r=27); text(d, (x0 + 120, 255), s, 38, INK)
        else: card(d, box, fill=None, outline=LIGHT, r=27, w=3); text(d, (x0 + 120, 255), s, 38, MUTED)

def table(d, n, y=1040, hl=None):
    card(d, (40, y, 1040, y + 520), fill=WHITE, outline=NAVY, w=4)
    xs = (250, 560, 840)
    for x, c in zip(xs, ("Hướng kéo", "góc β", "Lực kế (N)")): text(d, (x, y + 56), c, 38, INK)
    d.line([(70, y + 96), (1010, y + 96)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 170 + i * 120
        if hl is not None and i == hl: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=18, fill=(237, 233, 254))
        text(d, (xs[0], yy), ROWS[i][0], 40, INK)
        text(d, (xs[1], yy), f"{ROWS[i][1]}°", 42, INK)
        text(d, (xs[2], yy), "1,0", 44, BLUE)

def s_do(img, d, t, sc):
    M = sc["M"]; b = beta_at(t, sc); cur = max(0, cur_cap(sc, t))
    moving = any(M[i] <= t < M[i] + MOVE + 0.5 for i in (1, 2))
    chips(d, cur)
    if moving: rig(d, round(b), 1.0, "···", note="giữ yên rồi đọc")
    else: rig(d, round(b), 1.0, P_TXT)
    table(d, rows_shown(t, sc))

# ---------------- canh 3: Dap an + co che ----------------
def harrow(d, p1, p2, color, alpha):
    """Mui ten luc co vien trang (khong lan vao day/than vat)."""
    arrow(d, p1, p2, A(WHITE, alpha), w=16, head=26); arrow(d, p1, p2, A(color, alpha), w=9, head=24)

def forces(d, beta, alpha):
    """Ba mui ten DAI BANG NHAU (L): T day keo qua nang (len), P (xuong), T day keo moc luc ke (doc day, ve phia rong roc).
       Ve song song, cach day 36 px de khong chong len net day. Khong ve luc len rong roc."""
    L = 130
    harrow(d, (WX + 36, WY0), (WX + 36, WY0 - L), RED, alpha)
    text(d, (WX + 66, WY0 - L + 24), "T", 42, RED, anchor="lm", alpha=alpha)
    harrow(d, (WX, WY1), (WX, WY1 + L), BLUE, alpha)
    text(d, (WX + 30, WY1 + L - 24), "P", 42, BLUE, anchor="lm", alpha=alpha)
    (tx, ty), (ux, uy) = tangent(beta); nx, ny = -uy, ux
    o = -36                                              # lech ve phia tren-phai cua day
    sx, sy = tx + ux * ROPE + nx * o, ty + uy * ROPE + ny * o
    harrow(d, (sx, sy), (sx - ux * L, sy - uy * L), RED, alpha)
    text(d, (sx - ux * L / 2 + nx * (o - 34), sy - uy * L / 2 + ny * (o - 34)), "T", 42, RED, alpha=alpha)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    support(d); weight(d); scale(d, 45, 1.0); pulley(d); angle_mark(d, 45)
    ka = appear(t, 0.1, 0.5)
    pw = tw(d, "ĐÁP ÁN B", F(36)) + 52
    card(d, (W - 60 - pw, 236, W - 60, 296), fill=A(NAVY, ka), r=30)
    text(d, (W - 60 - pw / 2, 266), "ĐÁP ÁN B", 36, WHITE, alpha=ka)
    forces(d, 45, appear(t, M[1] - 0.1, 0.5))
    k1 = appear(t, M[0] + 0.3, 0.5)
    card(d, (40, 1080, 1040, 1300), fill=A(WHITE, k1), outline=A(BLUE, k1), w=5)
    ctext(d, 1190, "Ba hướng kéo: cùng 1,0 N", 46, INK, maxw=900, alpha=k1)
    k2 = appear(t, M[1] + 0.3, 0.5)
    card(d, (40, 1340, 1040, 1580), fill=A(WHITE, k2), outline=A(GREEN, k2), w=5)
    ctext(d, 1460, "Vật đứng yên nên T = P", 50, GREEN, maxw=900, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    support(d); weight(d); scale(d, 45, 1.0); pulley(d)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    # hinh cua bay: tuong luc ke chi "thanh phan thang dung" -> net dut do, lech 22 px khoi moc, co nhan
    if a1 > 0:
        (tx, ty), (ux, uy) = tangent(45)
        sx, sy = tx + ux * ROPE - 22, ty + uy * ROPE
        dashed(d, (sx, sy), (sx, sy + 130), A(DRED, a1), w=5)
        arrow(d, (sx, sy + 110), (sx, sy + 150), A(DRED, a1), w=5, head=18)
        bx0, bx1, by0 = sx - 96, sx + 144, sy + 172        # nhan ngay duoi mui ten do, giua day qua nang va than luc ke
        card(d, (bx0, by0, bx1, by0 + 128), fill=A(WHITE, a1), outline=A(DRED, a1), r=16, w=3)
        text(d, (sx + 24, by0 + 38), "thành phần", 38, DRED, alpha=a1)
        text(d, (sx + 24, by0 + 92), "thẳng đứng?", 38, DRED, alpha=a1)
        y0 = 1040
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“Kéo chếch thì lực kế chỉ ít hơn”"
        ks = clamp((t - 1.2) / 0.4)
        f = F(42); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2, yy), q, 42, INK, alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=3)
        ctext(d, y0 + 380, "Dây chỉ truyền lực dọc dây.", 46, DRED, maxw=900, alpha=a1 * appear(t, 1.3, 0.35))
    if k2 > 0:
        y0 = 1040 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 66), "Sai số khi đo thật", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.2, 0.4)
        card(d, (70, y0 + 150, 1010, y0 + 470), fill=A(WHITE, kk), outline=A(DRED, kk), r=24, w=4)
        ctext(d, y0 + 250, "Trục ròng rọc có ma sát", 46, DRED, maxw=880, alpha=kk)
        ctext(d, y0 + 370, "số chỉ lệch khoảng 0,05 N", 44, INK, maxw=880, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: dieu gi o qua nang quyet dinh 1,0 N; goi y hien tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 390, "Đổi hướng kéo, số chỉ không đổi", 50, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1310), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 674), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 642), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 840, "Kéo 45° hay 90° đều 1,0 N.\nĐiều gì ở quả nặng\nquyết định số đó?", 48, INK, maxw=900,
          alpha=appear(t, M[0] + 0.9, 0.5))
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (110, 1000, 970, 1260), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1055, "Gợi ý", 38, INK, alpha=kh)
    ctext(d, 1165, "Nhìn quả nặng, không nhìn hướng kéo.", 42, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.3, "ding"),
            (do["t0"] + M[1], "tap"), (do["t0"] + M[2], "tap"),
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"),
            (e["t0"] + e["M"][0] + 0.6, "open")]

CLIP = dict(id="tn-l10-trong-luc-luc-cang-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Trọng lực và lực căng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Dây vắt qua ròng rọc cố định", draw=s_hook, tail=0.8, caps=[
   ("Kéo thẳng xuống, quả nặng đứng yên.", 3.2),
   ("Tự đoán trước khi xem tiếp.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Kéo thẳng đứng, đọc lực kế.", 3.3),
   ("Xoay dây chếch 45°.", 3.3),
   ("Xoay tiếp tới nằm ngang.", 3.3)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Số chỉ không đổi theo hướng.", 3.8),
   ("Lực căng hai bên dây bằng nhau.", 4.2)]),
 dict(key="bay", title="Bẫy và sai số", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 3.6),
   ("Sai số khi đo thật.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
