# Clip: tn-l10-trong-luc-luc-cang-03 - Luc ke keo day vat qua rong roc co dinh theo nhieu huong (30/10/2026; dung lai
# 27/11/2026 theo cong moi viec 4: chu ve >= 55 px, thanh dem lien, Bay hinh tu giai thich, cau chot A-D o khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-trong-luc-luc-cang-03.json (_kiem_so() doi chieu):
#   so_lieu_mau: beta 0 / 45 / 90 do -> T = 1,0 N ca ba lan ; tham_so: P = 1,0 N, sai_so_do 0,05 N; dung_cu luc ke 0-2,5 N.
# Du doan (K10: chi cau hoi + hinh): treo thang qua nang vao luc ke chi 1,0 N; vat day qua rong roc co dinh, keo thang
#   xuong -> luc ke chi bao nhieu? (hien_tuong_hay_sai[1]: tuong rong roc co dinh loi ve luc). Dap an: van 1,0 N.
#   (Ban cu hoi "keo nam ngang" -> trung cau Quan sat cua hop exp trong bai.)
# Tien hanh: xoay huong keo 0 -> 45 -> 90 trong MOT canh, bang so lieu 3 hang.
# Bay = hien_tuong_hay_sai[0]: keo chech tuong luc ke chi "phan thang dung" -> net dut do (x) roi hai mui ten T bang nhau.
# Chua noi duoc = so_lieu_mau.ghi_chu + sai_so_thuong_gap: ma sat truc, so chi lech ~0,05 N.
# Chot (khung web A-D, kiem-v1 27/11): luc ke treo TRUC rong roc nhe, day vat qua, hai dau treo hai qua 1,0 N dung yen
#   -> moi doan day T = P = 1,0 N (mo_hinh), rong roc can bang: luc ke chi 2T = 2,0 N (ngoai moc 1,0 N da chieu).
#   Bay: 1,0 N (chi lay T), 0 N (tuong hai ben triet tieu), 1,4 N (cong vecto vuong goc).
from engine import *

# ---------------- bo cuc (khung nguon 1080x1920, vung ve y 285..1600) ----------------
CX, CY, R = 400, 450, 64             # tam + ban kinh rong roc
CEIL = 352                           # tran / gia treo
WX = CX - R                          # day ben qua nang (thang dung)
WY0, WY1 = 700, 800                  # qua nang
P = 1.0; P_TXT = "1,0 N"             # tham_so P
ROPE, BODY = 110, 330                # doan day tu rong roc toi moc luc ke ; chieu dai than luc ke
FMAX = 2.5; SAI = 0.05               # thang luc ke (dung_cu) ; sai_so_do
ROWS = [("thẳng đứng", 0), ("chếch", 45), ("nằm ngang", 90)]   # so_lieu_mau: T = 1,0 N ca ba
SKIN = (240, 196, 160)
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DPURPLE = (88, 28, 135); DORANGE = (176, 64, 8)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-trong-luc-luc-cang-03.json")))
    assert [tuple(h) for h in k["so_lieu_mau"]["hang"]] == [(b, P) for _, b in ROWS]
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["P"]["gia_tri"] == P and ts["T"]["sai_so_do"] == SAI
_kiem_so()

def dashed(d, p, q, color, w=3, seg=12, gap=9):
    L = math.dist(p, q); n = int(L // (seg + gap)) + 1
    for k in range(n):
        a = k * (seg + gap) / L; b = min(1, (k * (seg + gap) + seg) / L)
        if a >= 1: break
        d.line([(lerp(p[0], q[0], a), lerp(p[1], q[1], a)), (lerp(p[0], q[0], b), lerp(p[1], q[1], b))], fill=color, width=w)

def think_bar(d, t, t1, t2, y, a, col=DPURPLE, x0=80, x1=1000, h=92):
    """Thanh dem LIEN (khong chia o), cao 92 px, mau dam -> --do-chu thay hinh doi."""
    q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([x0, y, x1, y + h], radius=h // 2, fill=A(WHITE, a), outline=A((148, 140, 128), a), width=4)
    if q < 1: d.rounded_rectangle([x0, y, x0 + max(h, (x1 - x0) * (1 - q)), y + h], radius=h // 2, fill=A(col, a))

def pill(d, s, y, a, color=NAVY, size=56, cx=W / 2):
    pw = tw(d, s, F(size)) + 64
    card(d, (cx - pw / 2, y - 40, cx + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (cx, y), s, size, WHITE, alpha=a)

def tangent(beta, cx=CX, cy=CY):
    b = math.radians(beta)
    return (cx + R * math.cos(b), cy - R * math.sin(b)), (math.sin(b), math.cos(b))

def support(d, cx=CX, a=1.0):
    d.rectangle([cx - 140, CEIL - 26, cx + 70, CEIL], fill=A((176, 124, 74), a))
    for x in range(cx - 130, cx + 40, 34): d.line([(x, CEIL - 26), (x + 22, CEIL - 50)], fill=A((150, 105, 62), a), width=4)
    d.line([(cx, CEIL), (cx, CY)], fill=A((120, 125, 140), a), width=12)

def pulley(d, cx=CX, cy=CY, a=1.0):
    dot(d, cx, cy, R + 6, A((90, 98, 120), a))
    dot(d, cx, cy, R - 10, A((200, 205, 218), a))
    dot(d, cx, cy, 12, A(NAVY, a))

def weight(d, x=WX, y0=WY0, a=1.0, lab=None, side=-1):
    d.line([(x, y0), (x, y0 - 18)], fill=A(NAVY, a), width=7)
    d.rounded_rectangle([x - 55, y0, x + 55, y0 + 100], radius=12, fill=A((90, 98, 120), a))
    if lab: text(d, (x + side * 75, y0 + 50), lab, 58, INK, anchor="rm" if side < 0 else "lm", alpha=a)

def scale(d, beta, f_read, hand=True, alpha=1.0, an=False):
    """Day tu rong roc toi moc luc ke + luc ke (engine.luc_ke: 0-2,5 N, vach 0,05 N) + tay keo, theo huong beta."""
    (tx, ty), (ux, uy) = tangent(beta); nx, ny = -uy, ux
    Q = lambda s, n=0.0: (tx + ux * s + nx * n, ty + uy * s + ny * n)
    d.arc([CX - R, CY - R, CX + R, CY + R], 180, 360 - beta, fill=A(NAVY, alpha), width=5)
    d.line([(WX, CY), (WX, WY0 - 16)], fill=A(NAVY, alpha), width=5)                 # doan day ben qua nang
    d.line([Q(0), Q(ROPE - 13)], fill=A(NAVY, alpha), width=5)
    se = luc_ke(d, Q, ROPE, ROPE + 20, ROPE + 20 + BODY, FMAX, None if an else f_read, nho=SAI, so=(0, 1, 2), ben=-1,
                alpha=alpha, co=56, an=an)
    if hand:
        hx, hy = Q(se + 34)
        d.line([Q(se - 16), Q(se + 8)], fill=A(NAVY, alpha), width=8)
        dot(d, hx, hy, 34, A(SKIN, alpha), outline=A((190, 140, 105), alpha))

def angle_mark(d, beta, alpha=1.0):
    """Goc beta do tai moc luc ke: giua phuong thang dung (net dut, huong xuong) va day."""
    if beta < 5: return
    (tx, ty), (ux, uy) = tangent(beta)
    hx, hy = tx + ux * ROPE, ty + uy * ROPE
    dashed(d, (hx, hy), (hx, hy + 190), A(INK, alpha), w=4)
    rr = 110; edge = math.degrees(math.asin(54 / rr))
    d.arc([hx - rr, hy - rr, hx + rr, hy + rr], 90 - beta + edge, 90, fill=A(DORANGE, alpha), width=6)
    mid = math.radians(90 - (beta - edge) / 2)
    text(d, (hx + 175 * math.cos(mid), hy + 175 * math.sin(mid)), f"{beta}°", 58, DORANGE, alpha=alpha)

def readout(d, val, a=1.0):
    card(d, (700, 830, 1040, 1010), fill=A(WHITE, a), outline=A(LIGHT, a), r=26, w=3)
    text(d, (870, 878), "Lực kế chỉ", 56, INK, alpha=a)
    text(d, (870, 958), val, 64, RED, alpha=a)

def rig(d, beta, f_read, val=None, an=False):
    support(d); weight(d, lab=P_TXT); scale(d, beta, f_read, an=an); pulley(d); angle_mark(d, beta)
    if val: readout(d, val)

# ---------------- canh 1: Du doan (treo thang | qua rong roc ?) ----------------
DX = 820                                              # luc ke treo thang (khung phai)
def direct(d, t):
    yh = CEIL + BODY + 36 + 14
    d.rectangle([DX - 110, CEIL - 26, DX + 110, CEIL], fill=(176, 124, 74))
    d.line([(DX, CEIL), (DX, CEIL + 16)], fill=NAVY, width=5)
    tau = max(0.0, t - 0.4)
    f = P * (1 - math.exp(-2.6 * tau) * math.cos(2 * math.pi * 1.3 * tau)) if t > 0.4 else 0.0
    Q = lambda s, h=0.0: (DX + h, yh - s)
    luc_ke(d, Q, 0, 20, 20 + BODY, FMAX, f, nho=SAI, so=(0, 1, 2), ben=-1, co=56)
    y0 = yh + 12 if t > 0.4 else yh - 40 + 52 * ease(t / 0.4)
    weight(d, DX, y0 + 18)
    if tau > 1.8:
        b0, b1 = 20, 20 + BODY; z0, zf = b1 - 58, b0 + 40; yk = yh - (z0 - (z0 - zf) * P / FMAX)
        d.polygon([(DX + 56, yk), (DX + 76, yk - 14), (DX + 76, yk + 14)], fill=RED)
        text(d, (DX + 84, yk), P_TXT, 60, RED, anchor="lm")
    text(d, (DX, yh + 190), "treo thẳng", 56, INK)

def s_hook(img, d, t, sc):
    M = sc["M"]
    support(d); weight(d); scale(d, 0, None, an=True); pulley(d)
    direct(d, t)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 70, a, PURPLE)
    text(d, (W / 2, y0 + 190), "Vắt dây qua ròng rọc, kéo xuống.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "Lực kế chỉ bao nhiêu?", 64, DPURPLE, alpha=a)
    think_bar(d, t, M[1] + 0.4, sc["T"] - 0.2, y0 + 410, a)

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

def table(d, n, y=1050, hl=None):
    card(d, (40, y, 1040, y + 510), fill=WHITE, outline=NAVY, w=4)
    xs = (250, 560, 850)
    for x, c in zip(xs, ("Hướng", "β", "Số chỉ (N)")): text(d, (x, y + 60), c, 56, INK)
    d.line([(70, y + 108), (1010, y + 108)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 180 + i * 115
        if hl is not None and i == hl: d.rounded_rectangle([60, yy - 48, 1020, yy + 48], radius=18, fill=(237, 233, 254))
        text(d, (xs[0], yy), ROWS[i][0], 58, INK)
        text(d, (xs[1], yy), f"{ROWS[i][1]}°", 58, INK)
        text(d, (xs[2], yy), "1,0", 60, BLUE)

def s_do(img, d, t, sc):
    M = sc["M"]; b = beta_at(t, sc)
    moving = any(M[i] <= t < M[i] + MOVE + 0.5 for i in (1, 2))
    rig(d, round(b), P, "···" if moving else P_TXT)
    n = rows_shown(t, sc); table(d, n, hl=n - 1 if n else None)

def _kiem_dong_bo():
    """Hang bang chi hien khi day da dung o dung goc cua hang; readout '1,0 N' chi khi da dung xoay."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []; t = 0.0
    while t < sc["T"]:
        n = rows_shown(t, sc)
        if n and abs(beta_at(t, sc) - ROWS[n - 1][1]) > 1e-6 and n - 1 == max(0, cur_cap(sc, t)):
            bad.append((round(t, 2), "hang hien khi day chua dung goc"))
        t += 0.05
    if rows_shown(sc["T"] - 0.5, sc) != 3: bad.append("chua du 3 hang")
    return bad

# ---------------- canh 3: Dap an + co che ----------------
def harrow(d, p1, p2, color, alpha):
    arrow(d, p1, p2, A(WHITE, alpha), w=16, head=26); arrow(d, p1, p2, A(color, alpha), w=9, head=24)

def forces(d, beta, alpha, L=130):
    """T day keo qua nang (len), P (xuong), T day keo moc luc ke (doc day, ve phia rong roc): ba mui ten dai bang nhau."""
    harrow(d, (WX + 36, WY0), (WX + 36, WY0 - L), RED, alpha)
    text(d, (WX + 68, WY0 - L + 30), "T", 60, RED, anchor="lm", alpha=alpha)
    harrow(d, (WX, WY1), (WX, WY1 + L), BLUE, alpha)
    text(d, (WX + 34, WY1 + L - 30), "P", 60, BLUE, anchor="lm", alpha=alpha)
    (tx, ty), (ux, uy) = tangent(beta); nx, ny = -uy, ux
    o = -36                                                    # phia tren-phai day: khong chong rong roc
    sx, sy = tx + ux * ROPE + nx * o, ty + uy * ROPE + ny * o
    L3 = 80                                                    # kiem-v1: ngan lai, khong de len rong roc ; co nhan T
    harrow(d, (sx, sy), (sx - ux * L3, sy - uy * L3), RED, alpha)
    text(d, (sx - ux * L3 / 2 - nx * 46, sy - uy * L3 / 2 - ny * 46), "T", 60, RED, alpha=alpha)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    support(d); weight(d); scale(d, 45, P); pulley(d); angle_mark(d, 45)
    forces(d, 45, appear(t, M[1] - 0.1, 0.5))
    pill(d, "Đáp án: vẫn 1,0 N", 1130, appear(t, 0.3, 0.45), GREEN)
    k2 = appear(t, M[1] + 0.4, 0.5)
    if k2 > 0:
        card(d, (60, 1230, 1020, 1380), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1305), "Vật đứng yên nên T = P", 60, DGREEN, alpha=k2)

# ---------------- canh 4: Bay - "chi do phan thang dung" (x) -> luc doc day, T hai ben bang nhau (v) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    support(d); weight(d); scale(d, 45, P); pulley(d)
    (tx, ty), (ux, uy) = tangent(45)
    hx, hy = tx + ux * ROPE, ty + uy * ROPE
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 1.8, 0.45) * (1 - k2)
    if a1 > 0:                                                    # quan niem sai: net dut do, co dau x
        dashed(d, (hx - 30, hy), (hx - 30, hy + 170), A(DRED, a1), w=6)
        arrow(d, (hx - 30, hy + 150), (hx - 30, hy + 190), A(DRED, a1), w=6, head=20)
        text(d, (hx - 70, hy + 150), "?", 72, DRED, anchor="rm", alpha=a1)
    k1 = appear(t, 1.8, 0.45)
    card(d, (60, 1060, 1020, 1170), fill=A((254, 242, 242), k1), outline=A(DRED, k1), r=24, w=6)
    text(d, (W / 2, 1115), "✗ Dễ tưởng: kéo chếch chỉ ít hơn", 56, DRED, alpha=k1)
    if k2 > 0:
        forces(d, 45, k2)
        card(d, (60, 1210, 1020, 1320), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=24, w=6)
        text(d, (W / 2, 1265), "✓ Dây kéo dọc dây: T như nhau", 56, DGREEN, alpha=k2)

# ---------------- canh 5: Chua noi duoc - ma sat truc (hien lan luot, kim rung quanh 1,0 N) ----------------
def s_gioihan(img, d, t, sc):
    """kiem-v1: ve rong roc + day + luc ke keo thang xuong; kim rung quanh 1,0 N; truc khoanh do; chu 'ma sat truc'."""
    f = P + SAI * math.sin(2 * math.pi * 0.8 * t)
    support(d); weight(d); scale(d, 0, f); pulley(d)
    k2 = appear(t, 0.8, 0.45)
    if k2 > 0:
        rr = 40 + 16 * math.sin(2 * math.pi * 0.9 * t)          # vong do nhip nhe quanh truc
        d.ellipse([CX - rr, CY - rr, CX + rr, CY + rr], outline=A(DRED, k2), width=6)
    k0 = appear(t, 0.3, 0.45)
    card(d, (40, 1180, 1040, 1400), fill=A(WHITE, k0), outline=A(NAVY, k0), w=6)
    text(d, (W / 2, 1240), "Chưa nói được", 60, NAVY, alpha=k0)
    text(d, (W / 2, 1335), "ma sát trục: lệch cỡ 0,05 N", 60, INK, alpha=k0)

# ---------------- canh 6: Chot (phu de) + THU NGHI: hai qua 1,0 N, luc ke giua doan day ben phai ----------------
EX = 540
def s_end(img, d, t, sc):
    """THU NGHI: luc ke treo truc rong roc nhe; day vat qua, hai qua 1,0 N dung yen -> luc ke chi ? (2,0 N)."""
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1590), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 300, k1, ORANGE)
    top = 380
    d.rectangle([EX - 110, top, EX + 110, top + 24], fill=A((176, 124, 74), k1))
    d.line([(EX, top + 24), (EX, top + 40)], fill=A(NAVY, k1), width=5)
    yh = top + 24 + BODY + 36 + 14
    Q = lambda s, h=0.0: (EX + h, yh - s)
    luc_ke(d, Q, 0, 20, 20 + BODY, FMAX, None, nho=SAI, so=(0, 1, 2), ben=-1, co=56, alpha=k1, an=True)
    ey = yh + 30 + R
    d.line([(EX, yh), (EX, ey)], fill=A((120, 125, 140), k1), width=12)          # quai giu truc
    lx, rx = EX - R, EX + R
    d.arc([EX - R, ey - R, EX + R, ey + R], 180, 360, fill=A(NAVY, k1), width=5)
    for x, side in ((lx, -1), (rx, 1)):
        d.line([(x, ey), (x, 1060)], fill=A(NAVY, k1), width=5)
        weight(d, x, 1060, a=k1, lab=P_TXT, side=side)
    pulley(d, EX, ey, k1)
    text(d, (W / 2, 1270), "Ròng rọc nhẹ, hệ đứng yên.", 58, INK, alpha=k1)
    text(d, (W / 2, 1370), "Lực kế chỉ bao nhiêu?", 64, DORANGE, alpha=k1)
    think_bar(d, t, 1.0, sc["T"] - 0.2, 1450, k1, col=DORANGE)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 1.0, "ding"),
            (do["t0"] + M[1], "tap"), (do["t0"] + M[2], "tap"),
            (da["t0"] + 0.3, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-trong-luc-luc-cang-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Trọng lực và lực căng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Treo thẳng và qua ròng rọc", draw=s_hook, tail=0.3, caps=[
   ("Treo thẳng: lực kế chỉ 1,0 N.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Kéo thẳng xuống, đọc lực kế.", 3.2),
   ("Xoay dây chếch 45°.", 3.2),
   ("Xoay tiếp tới nằm ngang.", 3.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Ba hướng kéo, cùng một số chỉ.", 3.6),
   ("Lực căng hai bên dây bằng nhau.", 3.8)]),
 dict(key="bay", title="Bẫy: kéo chếch", draw=s_bay, tail=0.4, caps=[
   ("Kéo chếch thì sao?", 3.8),
   ("Lực kế đo lực dọc dây.", 3.8)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.6, caps=[
   ("Đo thật, số chỉ lệch chút.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Thử tính, rồi chọn đáp án.", 5.8)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
