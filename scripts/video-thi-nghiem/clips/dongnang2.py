# Clip: tn-l10-dong-nang-the-nang-02 - Con lac vuong dinh (con lac Galilei) (lo 9, 18/11/2026)
# So lieu lay tu content/thi-nghiem/tn-l10-dong-nang-the-nang-02.json:
#   tham_so: L = 1,0 m, h0 = 0,20 m, d (diem treo - dinh) 0 / 0,5 / 0,7 m; mo_hinh g = 10 m/s2, h1 = h0 khi h0 <= L - d.
#   so_lieu_mau: d 0 / 0,5 / 0,7 -> h1 = 0,20 m ca ba. Cot goc lech ben kia THEM vao kho 18/11/2026:
#   cos(goc) = 1 - h0/(L - d) -> 36,9 / 53,1 / 70,5 do (hien 37°, 53°, 71°); goc tha 36,9° (cos = 0,8).
# Canh: Du doan (khong dinh: len lai 0,20 m; dinh o 0,7 m: ben kia qua nang len toi dau? K10: chi cau hoi + hinh)
#       -> Tien hanh (3 lan tha d = 0 / 0,5 / 0,7; cham dinh ben kia tren cung vach 0,20 m, hang bang hien DUNG luc toi dinh)
#          + DAP AN · len dung 0,20 m
#       -> Rut ra (T vuong goc duong di -> khong sinh cong; hai dinh v = 0 -> cong trong luc xuong = len) + Chua noi duoc
#       -> Bay (day ngan quay nhanh -> len cao hon: sai; o day toc do khong doi) -> Chot + THU NGHI:
#          dinh 0,5 m, tha tu 0,20 m: ben kia o do cao 0,15 m toc do bao nhieu? v = can(2.10.0,05) = 1,0 m/s (chua hien).
# Khac muc L9 (dinh tinh cao hon / thap hon / bang): Du doan dat "cung GOC 37°" canh "cung DO CAO 0,20 m"; chot tinh so.
import copy
from engine import *

G, LM, H0 = 10.0, 1.0, 0.20
DS = [0.0, 0.5, 0.7]                                       # so_lieu_mau d (m)
TH0 = math.acos(1 - H0 / LM)                               # 36,87 do
def phimax(dd): return math.acos(1 - H0 / (LM - dd))       # 36,9 / 53,1 / 70,5 do
ANG = ["37°", "53°", "71°"]
DLAB = ["không đinh", "0,5 m", "0,7 m"]

PX, PY, LPX = 540, 290, 620                                # diem treo, px ung voi 1 m
YB = PY + LPX                                              # tam qua nang o vi tri thap nhat (y 910)
YH = YB - H0 * LPX                                         # vach 0,20 m (y 786)
RB = 30
BOB = (70, 90, 160); BOB_D = (40, 52, 110); STEEL = (150, 155, 172); NAIL = (90, 90, 100)
SLOW = 1.3

def ypos(dd): return PY + dd * LPX

def stand(d):
    d.rounded_rectangle([340, PY - 26, 740, PY], radius=8, fill=STEEL)
    d.polygon([(PX - 18, PY), (PX + 18, PY), (PX, PY + 16)], fill=NAVY)

def nail(d, dd, alpha=1.0, lab=True):
    if dd <= 0 or alpha <= 0: return
    y = ypos(dd)
    d.ellipse([PX - 13, y - 13, PX + 13, y + 13], fill=A(NAIL, alpha), outline=A(NAVY, alpha), width=3)
    if lab: text(d, (PX + 28, y - 30), "đinh", 40, NAIL, anchor="lm", alpha=alpha)

def marks(d, alpha=1.0):
    """Vach phan 0,20 m (net dut) + vach thap nhat + ngoac do cao ben trai."""
    for y, c in ((YH, ORANGE), (YB, GRAY)):
        for xx in range(110, 1010, 26): d.line([(xx, y), (xx + 14, y)], fill=A(c, alpha), width=4)
    xb = 80
    d.line([(xb, YH + 4), (xb, YB - 4)], fill=A(INK, alpha), width=4)
    for y, s in ((YH, 1), (YB, -1)): d.polygon([(xb, y), (xb - 9, y + s * 14), (xb + 9, y + s * 14)], fill=A(INK, alpha))
    text(d, (60, YB + 50), "0,20 m", 40, INK, anchor="lm", alpha=alpha)

def bob_left(theta):                                       # theta > 0: lech sang trai, quanh diem treo
    return PX - LPX * math.sin(theta), PY + LPX * math.cos(theta)

def bob_right(phi, dd):                                     # phi > 0: lech sang phai, quanh dinh (d = 0: diem treo)
    r = (LM - dd) * LPX; cy = ypos(dd)
    return PX + r * math.sin(phi), cy + r * math.cos(phi)

def draw_pend(d, pos, side, dd, alpha=1.0):
    x, y = pos
    if side == "R" and dd > 0:
        d.line([(PX, PY), (PX, ypos(dd))], fill=A(NAVY, alpha), width=4)
        d.line([(PX, ypos(dd)), (x, y)], fill=A(NAVY, alpha), width=4)
    else: d.line([(PX, PY), (x, y)], fill=A(NAVY, alpha), width=4)
    if alpha >= 0.98: dot(d, x, y, RB, BOB, BOB_D)
    else: d.ellipse([x - RB, y - RB, x + RB, y + RB], fill=A(BOB, alpha), outline=A(BOB_D, alpha), width=3)

def ghost(d, pos, color=PURPLE, alpha=1.0):
    x, y = pos
    for k in range(0, 360, 30): d.arc([x - RB, y - RB, x + RB, y + RB], k, k + 18, fill=A(color, alpha), width=5)

# mot lan tha: xuat hien o trai 0,3 s, giu 0,4 s, tha; qua day sau QL, len toi dinh ben phai sau QR, giu
APP, HOLD = 0.25, 0.3
def ql(): return math.pi / 2 / math.sqrt(G / LM) * SLOW
def qr(dd): return math.pi / 2 / math.sqrt(G / (LM - dd)) * SLOW
def run_len(dd): return APP + HOLD + ql() + qr(dd) + 0.5
def peak_t(dd): return APP + HOLD + ql() + qr(dd)

def run_state(tau, dd):
    """(vi tri, ben, alpha, da toi dinh chua) tau giay sau khi bat dau lan tha."""
    if tau < APP + HOLD: return bob_left(TH0), "L", clamp(tau / APP), False
    s = tau - APP - HOLD
    if s < ql(): return bob_left(TH0 * math.cos(math.pi / 2 * s / ql())), "L", 1.0, False
    s -= ql()
    if s < qr(dd): return bob_right(phimax(dd) * math.sin(math.pi / 2 * s / qr(dd)), dd), "R", 1.0, False
    return bob_right(phimax(dd), dd), "R", 1.0, True

# ---------------- canh 1: du doan ----------------
REL0 = 0.4
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; tau = t - REL0
    marks(d); stand(d)
    for yy in range(PY + 20, PY + 200, 24): d.line([(PX, yy), (PX, yy + 12)], fill=GRAY, width=3)   # duong thang dung tham chieu
    d.arc([PX - 90, PY - 90, PX + 90, PY + 90], 90, 90 + math.degrees(TH0), fill=MUTED, width=4)
    text(d, (PX + 130 * math.cos(math.radians(108.4)), PY + 130 * math.sin(math.radians(108.4))), "37°", 40, MUTED)
    kq = appear(t, M[1] - 0.4, 0.5)
    if tau < run_len(0.0):
        pos, side, al, ok = run_state(tau, 0.0)
        if ok: ghost(d, pos, BLUE); text(d, (pos[0], YH + 60), "37°", 40, BLUE)
        draw_pend(d, pos, side, 0.0, al)
    else:
        nail(d, 0.7, kq, lab=False)
        text(d, (PX + 28, ypos(0.7) - 30), "đinh: 0,7 m dưới điểm treo", 40, NAIL, anchor="lm", alpha=kq)
        draw_pend(d, bob_left(TH0), "L", 0.7, clamp((tau - run_len(0.0)) / 0.3))
    if kq <= 0: return
    y0 = 1130 + (1 - kq) * 30
    card(d, (60, y0, 1020, y0 + 400), fill=A(WHITE, kq), outline=A(PURPLE, kq), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, kq), r=32)
    text(d, (W / 2, y0 + 58), "Dự đoán", 40, WHITE, alpha=kq)
    ctext(d, y0 + 180, "Bên kia, quả nặng lên tới đâu?", 48, INK, maxw=900, alpha=kq)
    text(d, (W / 2, y0 + 290), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=kq)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 345, 880, y0 + 361], radius=8, fill=A(LIGHT, kq))
    if q < 1: d.rounded_rectangle([200, y0 + 345, 200 + 680 * (1 - q), y0 + 361], radius=8, fill=A(PURPLE, kq))

# ---------------- canh 2: tien hanh ----------------
T0S = [0.3]
for _dd in DS[:-1]: T0S.append(T0S[-1] + run_len(_dd))
def row_t(j): return T0S[j] + peak_t(DS[j])

def which(t):
    j = max([i for i in range(3) if t >= T0S[i]], default=-1)
    return j

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; j = which(t)
    marks(d); stand(d)
    for i in range(3):                                      # dinh da dat: vong tron cham + goc (giu lai)
        if t >= row_t(i):
            a = appear(t, row_t(i), 0.25); p = bob_right(phimax(DS[i]), DS[i])
            ghost(d, p, BLUE, a); text(d, (p[0], YH + (105 if i == 2 else 60)), ANG[i], 40, BLUE, alpha=a)
    if j >= 0:
        dd = DS[j]; nail(d, dd)
        pos, side, al, ok = run_state(t - T0S[j], dd)
        draw_pend(d, pos, side, dd, al)
    ka = appear(t, M[1], 0.4)
    if ka > 0:
        card(d, (60, 990, 1020, 1090), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1040), "ĐÁP ÁN · lên đúng 0,20 m", 46, GREEN, alpha=ka)
    nr = sum(1 for i in range(3) if t >= row_t(i))
    if nr == 0: return                                      # chua co hang: chua ve the bang
    card(d, (60, 1115, 1020, 1280 + (nr - 1) * 95 + 55), fill=WHITE, outline=NAVY, w=4)
    xs = (250, 560, 840)
    for x, s in zip(xs, ("đinh", "lên cao", "góc lệch")): text(d, (x, 1170), s, 40, INK)
    d.line([(90, 1210), (990, 1210)], fill=LIGHT, width=4)
    for i in range(3):
        a = appear(t, row_t(i), 0.3); yy = 1280 + i * 95
        if a <= 0: continue
        if ka > 0: d.rounded_rectangle([450, yy - 38, 670, yy + 38], radius=16, fill=A((220, 252, 231), ka))
        text(d, (xs[0], yy), DLAB[i], 42, NAIL if i else INK, alpha=a)
        text(d, (xs[1], yy), "0,20 m", 42, ORANGE, alpha=a); text(d, (xs[2], yy), ANG[i], 42, BLUE, alpha=a)

# ---------------- canh 3: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; dd = 0.7
    # hinh: day vuong dinh, qua nang dang len ben phai; T huong ve dinh, v tiep tuyen
    phi = math.radians(35); r = (LM - dd) * LPX; cx, cy = PX, ypos(dd)
    stand(d); nail(d, dd, lab=False)
    for i in range(0, 72, 4):
        a1, a2 = math.radians(i), math.radians(i + 2)
        d.line([bob_right(a1, dd), bob_right(a2, dd)], fill=(200, 194, 180), width=4)
    bx, by = bob_right(phi, dd)
    draw_pend(d, (bx, by), "R", dd)
    k0 = appear(t, M[0] - 0.1, 0.4)
    if k0 > 0:
        ut = (-math.sin(phi), -math.cos(phi)); uv = (math.cos(phi), -math.sin(phi))
        arrow(d, (bx, by), (bx + 150 * ut[0], by + 150 * ut[1]), A(PURPLE, k0), w=7, head=22)
        text(d, (bx + 150 * ut[0] - 40, by + 150 * ut[1] + 10), "T", 46, PURPLE, alpha=k0)
        arrow(d, (bx, by), (bx + 170 * uv[0], by + 170 * uv[1]), A(BLUE, k0), w=7, head=22)
        text(d, (bx + 170 * uv[0] + 34, by + 170 * uv[1]), "v", 46, BLUE, alpha=k0)
        s = 26
        p1 = (bx + s * ut[0], by + s * ut[1]); p3 = (bx + s * uv[0], by + s * uv[1]); p2 = (p1[0] + s * uv[0], p1[1] + s * uv[1])
        d.line([p1, p2, p3], fill=A(INK, k0), width=4)
        card(d, (60, 960, 1020, 1060), fill=A((243, 238, 255), k0), outline=A(PURPLE, k0), r=28, w=4)
        text(d, (W / 2, 1010), "T vuông góc đường đi: không sinh công", 40, PURPLE, alpha=k0)
    k1 = appear(t, M[1] - 0.1, 0.4)
    if k1 > 0:
        card(d, (60, 1080, 1020, 1260), fill=A(WHITE, k1), outline=A(ORANGE, k1), r=28, w=4)
        ctext(d, 1130, "Hai đỉnh đều v = 0:", 42, INK, alpha=k1)
        ctext(d, 1205, "công trọng lực xuống = lên", 42, ORANGE, alpha=k1)
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y1 = 1280 + (1 - k3) * 20
        card(d, (40, y1, 1040, y1 + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 55), "Chưa nói được gì?", 44, NAVY, alpha=k3)
        card(d, (80, y1 + 105, 1000, y1 + 270), fill=A((239, 246, 255), k3), r=24)
        ctext(d, y1 + 150, "Dây dưới đinh ngắn hơn 0,20 m:", 42, INK, alpha=k3)
        ctext(d, y1 + 225, "dây chùng, chưa xét", 42, BLUE, alpha=k3)

# ---------------- canh 4: bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1, 0.4); dd = 0.7
    marks(d); stand(d); nail(d, dd)
    ks = clamp((t - 1.0) / 0.4)
    # cach nghi sai: qua nang len cao hon vach (bong ma do, dau ?) hien cung cau sai
    wx, wy = bob_right(math.radians(95), dd)
    for k in range(0, 360, 30): d.arc([wx - RB, wy - RB, wx + RB, wy + RB], k, k + 18, fill=A(RED, a * (1 - 0.6 * ks)), width=5)
    text(d, (wx + 50, wy), "?", 48, RED, anchor="lm", alpha=a * (1 - 0.6 * ks))
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        draw_pend(d, bob_right(phimax(dd), dd), "R", dd, k2)
        text(d, (bob_right(phimax(dd), dd)[0], YH + 60), "0,20 m", 40, GREEN, alpha=k2)
    card(d, (60, 990, 1020, 1240), fill=A(WHITE, a), outline=A(RED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 1016, W / 2 + pw / 2, 1080), fill=A(RED, a), r=32)
    text(d, (W / 2, 1048), "Bẫy", 40, WHITE, alpha=a)
    q = "Dây ngắn quay nhanh → lên cao hơn"; f = F(42); lw = tw(d, q, f); yy = 1170
    text(d, (W / 2, yy), q, 42, mix(INK, MUTED, ks), alpha=a)
    if ks > 0: d.line([(W / 2 - lw / 2 - 8, yy + 2), (W / 2 - lw / 2 - 8 + (lw + 16) * ks, yy + 2)], fill=A(RED, 0.85 * a), width=6)
    text(d, (W / 2 - lw / 2 - 10, yy), "✗", 42, RED, anchor="rm", alpha=ks)
    if k2 > 0:
        card(d, (60, 1270, 1020, 1520), fill=A((220, 252, 231), k2), outline=A(GREEN, k2), w=5)
        ctext(d, 1345, "Vướng đinh không đổi tốc độ ở đáy", 42, INK, alpha=k2)
        ctext(d, 1440, "→ lên đúng vạch 0,20 m", 44, GREEN, alpha=k2)

# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 262, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 350, "Công trọng lực chỉ phụ thuộc", 48, GREEN, maxw=900, alpha=k0)
    ctext(d, 430, "độ cao đầu và cuối", 48, GREEN, maxw=900, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1240), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 676), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 643), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    ctext(d, 760, "Đinh 0,5 m, thả từ 0,20 m.", 46, INK, alpha=kq)
    ctext(d, 830, "Bên kia, ở độ cao 0,15 m,", 46, INK, alpha=kq)
    ctext(d, 900, "tốc độ bao nhiêu?", 46, INK, alpha=kq)
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh > 0:
        card(d, (110, 990, 970, 1200), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1040, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1120, "g = 10 m/s²", 42, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + do["M"][1], "ding"), (r["t0"] + r["M"][2] - 0.1, "tap"),
            (b["t0"] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-dong-nang-the-nang-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Động năng, thế năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Con lắc dây 1,0 m", draw=s_hook, tail=0.6, caps=[
   ("Thả từ vạch 0,20 m, chưa có đinh.", 3.8),
   ("Dừng video, tự đoán.", 5.4)]),
 dict(key="do", title="Dời đinh, thả lại", draw=s_do, tail=0.6, caps=[
   ("Thả nhẹ từ vạch cũ, không đẩy.", 6.4),
   ("Góc khác nhau, độ cao như nhau.", 3.6)]),
 dict(key="rut", title="Vì sao cùng độ cao?", draw=s_rut, tail=0.6, caps=[
   ("Lực căng vuông góc đường đi.", 3.4),
   ("Định lí động năng, hai đỉnh.", 3.4),
   ("Giới hạn của thí nghiệm.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Dây ngắn, tưởng lên cao hơn.", 3.0),
   ("Đinh chỉ đổi tâm quay.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 5.8)]),
])

def _kiem_dong_bo():
    """Moi 0,05 s canh Tien hanh: so hang bang = so lan da toi dinh; luc hang hien qua nang o dung vach 0,20 m;
    dinh ve dung lan tha; cao nhat ben phai khong vuot vach."""
    c = copy.deepcopy(CLIP); build(c); sc = c["scenes"][1]; t = 0.0; loi = 0
    while t < sc["T"]:
        j = which(t); rows = sum(1 for i in range(3) if t >= row_t(i))
        if j >= 0:
            pos, side, al, ok = run_state(t - T0S[j], DS[j])
            done = j + (1 if ok else 0)
            if rows != done: loi += 1
            if pos[1] < YH - 0.5: loi += 1
            if ok and abs(pos[1] - YH) > 0.5: loi += 1
        t += 0.05
    return loi
