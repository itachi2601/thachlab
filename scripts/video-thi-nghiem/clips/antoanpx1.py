# Clip: tn-l12-antoanpx-01 - Do suat lieu theo khoang cach: kiem chung quy luat 1/r^2
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-antoanpx-01.json (so_lieu_mau, tham_so, sai_so_thuong_gap).
# Ban 1 (28/10/2026): mau boyle/phongxa2 (dung cu + bang + do thi), tieng bao cues.
import random
from engine import *

ROWS = [(0.5, 1484, 1454, 364), (1.0, 390, 360, 360), (1.5, 196, 166, 374),
        (2.0, 119, 89, 356), (3.0, 71, 41, 369)]   # so_lieu_mau: d (m), nhip do, nhip thuc, N.d^2
PHONG, N1 = 30, 360                                 # phong 30 xung/phut; mo hinh nhip thuc = 360/d^2 (ghi_chu)
NOBG_3M = "≈ 640"                                   # sai_so_thuong_gap: quen tru phong, o 3 m N.d^2 thanh khoang 640
def fmt(v): return f"{v:.1f}".replace(".", ",")
def model(dd): return N1 / dd ** 2                  # chi dung de ve duong mo / mat do hat, khong in so moi

# ---------------- dung cu: nguon + thuoc + dau do + may dem ----------------
SX, SY = 130, 760          # tam nguon (d = 0)
PXM = 250                  # px moi met tren thuoc
def X(dd): return SX + dd * PXM
RY = 900                   # duong thuoc

RR = random.Random(7)
RAYS = [(RR.random(), RR.uniform(-math.pi, math.pi)) for _ in range(70)]   # hat gamma bay deu moi huong
BGR = [(RR.random(), RR.uniform(0, 2 * math.pi)) for _ in range(4)]        # hat phong nen

def rig(d, t, dd, reading, sub, lead=0.0):
    # hat gamma tu nguon (ve truoc de the khac de len)
    if lead < 1:
        for ph, ang in RAYS:
            q = (ph + t * 0.9) % 1; r = 40 + q * 900
            x, y = SX + r * math.cos(ang), SY + r * math.sin(ang)
            if 590 < y < RY - 14 and x < 1050: dot(d, x, y, 6, A(ORANGE, 0.4 * (1 - lead)))
    for ph, ang in BGR:        # phong nen: vai hat le tu ngoai vao dau do
        q = (ph + t * 0.6) % 1
        if q > 0.5: continue
        r = lerp(240, 30, q / 0.5)
        x, y = X(dd) + 60 + r * math.cos(ang), SY + 0.6 * r * math.sin(ang)
        if 590 < y < RY - 14: dot(d, x, y, 6, PURPLE)
    # thuoc
    d.line([(SX, RY), (X(3.0) + 20, RY)], fill=NAVY, width=6)
    for k in range(7):
        v = k * 0.5; x = X(v); L = 22 if k % 2 == 0 else 14
        d.line([(x, RY), (x, RY + L)], fill=NAVY, width=4)
        s = "0" if k == 0 else (str(int(v)) if k % 2 == 0 else fmt(v))
        text(d, (x, RY + 48), s, 34, MUTED, bold=False)
    text(d, (1030, RY + 48), "m", 34, MUTED, bold=False, anchor="rm")
    # nguon tren gia
    d.rectangle([SX - 8, SY + 34, SX + 8, RY], fill=GRAY)
    d.rounded_rectangle([SX - 34, SY - 34, SX + 34, SY + 34], radius=12, fill=YELLOW, outline=NAVY, width=5)
    for k in range(3):
        a = 90 + 120 * k
        d.pieslice([SX - 24, SY - 24, SX + 24, SY + 24], a - 30, a + 30, fill=NAVY)
    dot(d, SX, SY, 6, YELLOW)
    text(d, (SX, SY - 66), "nguồn", 34, MUTED, bold=False)
    if lead > 0:               # hop chi che nguon khi do phong
        yo = -260 * (1 - lead)
        card(d, (SX - 58, SY - 58 + yo, SX + 58, SY + 58 + yo), fill=A((110, 115, 128), lead), outline=A(NAVY, lead), r=14, w=5)
        text(d, (SX, SY + yo), "chì", 32, WHITE, alpha=lead)
    # dau do (cua so o dau trai, quay ve nguon) tren gia
    x = X(dd)
    d.rectangle([x + 60, SY + 30, x + 76, RY], fill=GRAY)
    d.rounded_rectangle([x, SY - 30, x + 140, SY + 30], radius=26, fill=(214, 220, 232), outline=NAVY, width=5)
    d.rectangle([x - 4, SY - 24, x + 12, SY + 24], fill=(70, 78, 100))
    text(d, (x + 70, SY - 62), "đầu dò", 34, NAVY)
    # khoang cach
    card(d, (60, 270, 500, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (280, 320), "Cách tâm nguồn", 34, MUTED, bold=False)
    text(d, (280, 430), f"d = {fmt(dd)} m", 66, BLUE)
    # may dem
    card(d, (560, 270, 1020, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (790, 320), "Máy đếm", 34, MUTED, bold=False)
    d.rounded_rectangle([610, 360, 970, 470], radius=16, fill=NAVY)
    text(d, (790, 415), str(reading), 66, (134, 239, 172))
    text(d, (790, 512), sub, 34, MUTED, bold=False)

# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. Còn khoảng 1/2", "B. Còn khoảng 1/4", "C. Còn khoảng 1/8", "D. Gần như không đổi")
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, 1.0, "···", "chưa đếm")
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 990, 1020, 1600), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1040), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1130, f"Ở 1 m: {N1} xung/phút.\nLùi ra 2 m thì còn bao nhiêu?", 40, INK, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.15); y = 1258 + i * 76
        card(d, (110, y - 33, 970, y + 33), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=20, w=4)
        text(d, (150, y), s, 38, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1566, 940, 1580], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1566, 140 + 800 * (1 - q), 1580], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: do phong, lui dan dau do, ghi bang ----------------
MOVE = 0.6
def row_at(i, sc):
    M = sc["M"]
    return [M[1] + 0.7, M[1] + 4.2, M[1] + 5.4, M[2] + 0.05, M[2] + 3.6][i]

def do_state(t, sc):
    """(d, so tren may dem, nhan duoi so, muc che chi)"""
    M = sc["M"]
    lead = 1 - ease((t - M[1]) / 0.5)
    if t < M[1]: return 1.0, PHONG, "xung/phút (phông)", lead
    dd, prev = 1.0, 1.0
    for i in range(5):
        a = row_at(i, sc)
        if t < a - MOVE: return dd, "···", "đang đổi chỗ", lead
        if t < a: return lerp(prev, ROWS[i][0], ease((t - (a - MOVE)) / MOVE)), "···", "đang đổi chỗ", lead
        dd = prev = ROWS[i][0]
    return dd, ROWS[4][1], "xung/phút (nhịp đo)", lead

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    dd, rd, sub, lead = do_state(t, sc)
    last = max([i for i in range(5) if t >= row_at(i, sc)], default=-1)
    if last >= 0 and t >= row_at(last, sc) and (last == 4 or t < row_at(last + 1, sc) - MOVE):
        rd, sub = ROWS[last][1], "xung/phút (nhịp đo)"
    rig(d, t, dd, rd, sub, lead=lead)
    card(d, (60, 990, 1020, 1600), fill=WHITE, outline=NAVY, w=4)
    text(d, (W / 2, 1035), f"Phông {PHONG} xung/phút", 40, PURPLE, alpha=appear(t, 0.9))
    xs = [215, 520, 830]
    for x, c in zip(xs, ["d (m)", "Nhịp đo", "Trừ phông"]): text(d, (x, 1100), c, 38, MUTED)
    d.line([(90, 1134), (990, 1134)], fill=LIGHT, width=4)
    hl = appear(t, M[2] + 0.3)
    for i, (dm, nd, nt, _) in enumerate(ROWS):
        a = appear(t, row_at(i, sc), 0.35); y = 1180 + i * 74
        if a <= 0: continue
        if hl > 0 and i in (1, 3): d.rounded_rectangle([80, y - 32, 1000, y + 32], radius=14, fill=A((220, 252, 231), hl))
        elif i == last: d.rounded_rectangle([80, y - 32, 1000, y + 32], radius=14, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), fmt(dm), 42, BLUE, alpha=a)
        text(d, (xs[1], y), str(nd), 42, INK, bold=False, alpha=a)
        text(d, (xs[2], y), str(nt), 44, GREEN, alpha=appear(t, max(row_at(i, sc) + 0.3, M[1] + 4.4), 0.35))

# ---------------- canh 3: dap an B + do thi + tich N.d^2 ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = back((t - 0.2) / 0.5) if t > 0.2 else 0
    card(d, (60, 250, 1020, 350), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 300), "Đáp án B: d gấp đôi, N còn 1/4", int(40 * clamp(k, 0.3, 1.0)), GREEN)
    x0, x1, yb, yt = 200, 950, 940, 470
    Xg = lambda v: x0 + v / 3 * (x1 - x0); Yg = lambda n: yb - n / 1500 * (yb - yt)
    card(d, (60, 380, 1020, 1040), fill=WHITE, outline=LIGHT, w=3)
    for n in (500, 1000, 1500): d.line([(x0, Yg(n)), (x1, Yg(n))], fill=(240, 236, 228), width=2)
    d.line([(x0, yb), (x1 + 25, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 40)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 50), "N (xung/phút)", 34, MUTED, anchor="lm")
    text(d, (x1 + 25, yb + 80), "d (m)", 34, MUTED, anchor="rm")
    for k2 in range(7):
        v = k2 * 0.5; d.line([(Xg(v), yb), (Xg(v), yb + 10)], fill=NAVY, width=3)
        if k2 % 2 == 0: text(d, (Xg(v), yb + 36), str(int(v)), 36, MUTED, bold=False)
    for n in (0, 500, 1000, 1500):
        d.line([(x0 - 10, Yg(n)), (x0, Yg(n))], fill=NAVY, width=4); text(d, (x0 - 18, Yg(n)), str(n), 36, MUTED, bold=False, anchor="rm")
    kc = ease((t - 1.4) / 1.2)
    if kc > 0:
        vs = [0.49 + (3 - 0.49) * j / 100 for j in range(101)]
        pts = [(Xg(v), Yg(model(v))) for v in vs]
        d.line(pts[:max(2, int(len(pts) * kc))], fill=A(BLUE, 0.45), width=6, joint="curve")
    # danh dau 1 m va 2 m
    km = appear(t, 0.9)
    for dm, n in ((1.0, ROWS[1][2]), (2.0, ROWS[3][2])):
        for yy in range(int(Yg(n)), int(yb), 20):
            d.line([(Xg(dm), yy), (Xg(dm), min(yy + 11, yb))], fill=A(GREEN, km), width=4)
        for xx in range(int(x0), int(Xg(dm)), 22):
            d.line([(xx, Yg(n)), (min(xx + 12, Xg(dm)), Yg(n))], fill=A(GREEN, km), width=4)
        text(d, (Xg(dm) + 28, Yg(n) - 36), str(n), 40, GREEN, anchor="lm", alpha=km)
    for dm, n in ((1.5, ROWS[2][2]), (3.0, ROWS[4][2])):
        text(d, (Xg(dm), Yg(n) - 44), str(n), 36, ORANGE, alpha=appear(t, 1.2))
    for i, (dm, _, nt, _) in enumerate(ROWS):
        a = appear(t, 0.4 + i * 0.15, 0.4)
        if a > 0: dot(d, Xg(dm), Yg(nt), 15 * back(a), ORANGE, WHITE)
    text(d, (Xg(0.5) + 30, Yg(ROWS[0][2])), str(ROWS[0][2]), 36, ORANGE, anchor="lm", alpha=appear(t, 0.6))
    # cot N.d^2
    a1 = appear(t, M[1] - 0.2)
    if a1 <= 0: return
    card(d, (60, 1070, 1020, 1600), fill=A(WHITE, a1), outline=A(LIGHT, a1), w=3)
    band = appear(t, M[1] + 1.8, 0.4)
    base, s_ = 1460, 0.58
    if band > 0: d.rectangle([90, base - 374 * s_, 990, base - 356 * s_], fill=A((187, 247, 208), band))
    title = "Tích N·d²" if band < 0.5 else "N·d² từ 356 đến 374"
    text(d, (W / 2, 1115), title, 40, GREEN if band >= 0.5 else MUTED, alpha=a1)
    d.line([(90, base), (990, base)], fill=NAVY, width=4)
    for i, (dm, _, _, nd2) in enumerate(ROWS):
        cx = 180 + i * 180; g = ease((t - M[1] - 0.3 - i * 0.25) / 0.5)
        text(d, (cx, base + 36), f"{fmt(dm)} m", 34, MUTED, bold=False, alpha=a1)
        if g <= 0: continue
        top = base - nd2 * s_ * g
        d.rectangle([cx - 55, top, cx + 55, base], fill=ORANGE)
        text(d, (cx, top - 30), str(nd2), 40, INK, alpha=clamp(g * 2 - 1))
    ctext(d, 1550, "Lệch vài %: thăng giáng ±√N", 36, MUTED, bold=False, alpha=appear(t, M[1] + 2.8))

# ---------------- canh 4: co che + chua noi duoc gi ----------------
S0 = (130, 600); H1 = 62; GAP = 250
def P(r, z, y):   # diem tren mat vuong goc truc, cach nguon r buoc; chieu xien (z = sau)
    return (S0[0] + r * GAP + 0.42 * z, S0[1] - y - 0.28 * z)

def square(d, r, n, hl_col, a, lbl, frac):
    h = r * H1
    c = [P(r, -h, -h), P(r, h, -h), P(r, h, h), P(r, -h, h)]
    d.polygon(c, fill=A((236, 244, 255), a), outline=A(NAVY, a))
    # o to mau: o goc duoi-truoc
    cell = h * 2 / n
    q = [P(r, -h, -h), P(r, -h + cell, -h), P(r, -h + cell, -h + cell), P(r, -h, -h + cell)]
    d.polygon(q, fill=A(hl_col, a))
    for j in range(1, n):
        u = -h + j * cell
        d.line([P(r, u, -h), P(r, u, h)], fill=A(NAVY, a), width=3)
        d.line([P(r, -h, u), P(r, h, u)], fill=A(NAVY, a), width=3)
    d.line(c + [c[0]], fill=A(NAVY, a), width=4)
    for i in range(6):          # 36 hat moi giay, trai deu tren mat: o to mau co 36 / 9 / 4 hat
        for j in range(6):
            dot(d, *P(r, -h + (i + 0.5) * h / 3, -h + (j + 0.5) * h / 3), 4, A(NAVY, a))
    bx = S0[0] + r * GAP
    text(d, (bx, 900), lbl, 40, BLUE, alpha=a)
    text(d, (bx, 955), frac, 38, ORANGE, alpha=a)

def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 1000), fill=WHITE, outline=LIGHT, w=3)
    a3 = appear(t, 0.3)
    hmax = 3 * H1
    for z, y in ((-hmax, -hmax), (hmax, -hmax), (hmax, hmax), (-hmax, hmax)):   # 4 canh cua chum tia
        d.line([S0, P(3, z, y)], fill=A(GRAY, a3), width=3)
    for r, n, at in ((1, 1, 0.3), (2, 2, 0.9), (3, 3, 1.5)):
        square(d, r, n, ORANGE, appear(t, at), ["d", "2d", "3d"][r - 1], ["1", "1/4", "1/9"][r - 1])
    dot(d, S0[0], S0[1], 16, YELLOW, NAVY)
    text(d, (S0[0], S0[1] - 50), "nguồn", 34, MUTED, bold=False)
    a = appear(t, 0.3)
    card(d, (60, 1030, 1020, 1250), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    ctext(d, 1095, "Cùng số hạt, diện tích tăng theo d²", 38, INK, alpha=a)
    ctext(d, 1185, "d gấp 2 → diện tích gấp 4 → N còn 1/4", 42, BLUE, alpha=appear(t, M[1]))
    b = appear(t, M[1] + 0.3)
    card(d, (60, 1290, 1020, 1520), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
    text(d, (W / 2, 1345), "Chưa nói được gì?", 40, PURPLE, alpha=b)
    ctext(d, 1440, "Tác hại (cần liều Sv)", 42, INK, alpha=b)

# ---------------- canh 5: bay quen tru phong ----------------
def strip(d, y, title, rows, verdict, col, a):
    card(d, (60, y, 1020, y + 330), fill=A(WHITE, a), outline=A(col, a), w=5)
    text(d, (W / 2, y + 48), title, 40, col, alpha=a)
    for j, (lbl, expr) in enumerate(rows):
        yy = y + 120 + j * 72
        text(d, (120, yy), lbl, 38, MUTED, bold=False, anchor="lm", alpha=a)
        text(d, (330, yy), expr, 42, INK, anchor="lm", alpha=a)
    text(d, (W / 2, y + 285), verdict, 40, col, alpha=a)

def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 340), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 295), "Bẫy: quên trừ phông", 42, RED, alpha=appear(t, 0.1))
    strip(d, 370, "Chưa trừ phông",
          [("ở 3 m", f"{ROWS[4][1]} × 9 {NOBG_3M}")],
          "Tưởng sai quy luật", RED, appear(t, 0.3))
    strip(d, 730, "Đã trừ phông",
          [("ở 3 m", f"{ROWS[4][2]} × 9 = {ROWS[4][3]}")],
          "Gần không đổi", GREEN, appear(t, M[1] + 0.2))
    c = appear(t, M[1] + 1.2)
    card(d, (60, 1095, 1020, 1420), fill=A((254, 242, 242), c), r=28)
    ctext(d, 1230, f"Ở xa, phông chiếm gần nửa số đo {ROWS[4][1]}", 42, RED, alpha=c)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    chot_hoi(d, t, sc, "Nguồn điểm: d gấp đôi → còn 1/4",
             "Từ 0,5 m lùi ra 1,5 m, nhịp thực giảm khoảng bao nhiêu lần?",
             "Nhớ lại cột N·d²")

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + do["M"][1], "tap"), (do["t0"] + row_at(3, do), "ding"),
            (an["t0"] + an["M"][1] + 1.8, "tap"), (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-antoanpx-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="An toàn phóng xạ · thachlab.id.vn", scenes=[
 dict(key="hook", title="Lùi xa nguồn phóng xạ", draw=s_hook, tail=0.6, caps=[
   ("Đầu dò cách nguồn 1 m.", 2.4),
   ("Chọn một đáp án.", 5.0)]),
 dict(key="do", title="Đo phông, rồi lùi dần đầu dò", draw=s_do, tail=0.6, caps=[
   ("Hộp chì che nguồn: đo phông.", 3.5),
   ("Trừ phông ra nhịp thực.", 6.5),
   ("2 m: còn khoảng 1/4.", 4.6)]),
 dict(key="ans", title="Đồ thị và tích N·d²", draw=s_ans, tail=0.6, caps=[
   ("Đáp án B.", 3.0),
   ("N·d² gần như không đổi.", 4.5)]),
 dict(key="why", title="Vì sao giảm theo d²?", draw=s_why, tail=1.2, caps=[
   ("Hạt trải đều mọi hướng.", 2.4),
   ("Nhìn ô màu cam.", 3.2)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.8, caps=[
   ("Nhân N với d² khi chưa trừ.", 3.4),
   ("Rồi trừ phông.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Lùi từ 0,5 ra 1,5 m.", 5.0)]),
])
