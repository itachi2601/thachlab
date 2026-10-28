# Clip: tn-l12-phongxa-02 - Theo doi do phong xa giam theo thoi gian de doc chu ki ban ra
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-phongxa-02.json (so_lieu_mau, tham_so).
# Ban 1 (28/10/2026): mau boyle (dung cu + bang + do thi), tieng bao cues nhu chuyenthe.
import random
from engine import *

ROWS = [(0, 835, 812), (5, 421, 398), (10, 227, 204), (15, 120, 97), (20, 75, 52), (25, 47, 24)]  # so_lieu_mau
PHONG, T_BR, H0 = 23, 5, 810                       # tham_so: phong nen, T mac dinh, H0 (mo hinh trong ghi_chu)
RATIOS = ["2,04", "1,95", "2,10", "1,87", "2,17"]  # so_lieu_mau.ghi_chu: ti so hai lan lien tiep (da tru phong)
def model(m): return H0 * 2 ** (-m / T_BR)          # chi dung de ve mat do hat / duong mo, khong in so

# ---------------- dung cu: nguon + ong dem Geiger + may dem + dong ho ----------------
RP = random.Random(3)
RAYS = [(RP.random(), RP.uniform(-1, 1)) for _ in range(28)]       # (pha, do lech) hat bay tu nguon vao cua so
BGR = [(RP.random(), RP.uniform(0, 2 * math.pi)) for _ in range(6)]  # hat phong nen tu moi phia

SX, SY = 300, 700          # tam nguon
TX0, TX1, TY = 430, 800, 700

def rig(d, t, minute, reading, src=1.0, clock_lbl=None):
    # ban + gia do
    d.line([(110, 920), (970, 920)], fill=NAVY, width=6)
    d.rectangle([(TX0 + TX1) / 2 - 8, TY + 40, (TX0 + TX1) / 2 + 8, 916], fill=GRAY)
    d.rectangle([(TX0 + TX1) / 2 - 70, 900, (TX0 + TX1) / 2 + 70, 918], fill=NAVY)
    # ong dem Geiger (cua so o dau trai, quay ve phia nguon)
    d.rounded_rectangle([TX0, TY - 40, TX1, TY + 40], radius=36, fill=(214, 220, 232), outline=NAVY, width=5)
    d.rectangle([TX0 - 6, TY - 34, TX0 + 14, TY + 34], fill=(70, 78, 100))
    text(d, ((TX0 + TX1) / 2, TY), "ống Geiger", 36, NAVY)
    # cap noi may dem
    d.line([(TX1, TY), (900, TY), (900, 562)], fill=GRAY, width=12, joint="curve")
    # nguon tren gia (truot vao khi dat nguon)
    sx = lerp(-120, SX, ease(src))
    if src > 0:
        d.rectangle([sx - 8, SY + 30, sx + 8, 916], fill=GRAY)
        d.rectangle([sx - 60, 900, sx + 60, 918], fill=NAVY)
        d.rounded_rectangle([sx - 34, SY - 34, sx + 34, SY + 34], radius=12, fill=YELLOW, outline=NAVY, width=5)
        for k in range(3):
            a = math.radians(90 + 120 * k)
            d.pieslice([sx - 24, SY - 24, sx + 24, SY + 24], math.degrees(a) - 30, math.degrees(a) + 30, fill=NAVY)
        dot(d, sx, SY, 6, YELLOW)
        text(d, (sx, 960), "nguồn", 36, MUTED, bold=False)
    # hat phong xa: mat do theo nhip dem mo hinh
    if src >= 1:
        n = int(len(RAYS) * clamp(model(minute) / model(0) + 0.04))
        for ph, dy in RAYS[:n]:
            q = (ph + t * 1.6) % 1
            x = lerp(SX + 40, TX0, q); y = SY + dy * 32 * q
            dot(d, x, y, 6, ORANGE)
    for ph, ang in BGR[:2]:                       # phong nen: vai hat le tu ngoai vao
        q = (ph + t * 0.7) % 1
        if q > 0.5: continue
        r = lerp(260, 40, q / 0.5)
        dot(d, 615 + r * math.cos(ang), TY + 0.8 * r * math.sin(ang), 6, PURPLE)
    # dong ho
    card(d, (70, 270, 520, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (295, 430), clock_lbl or f"phút {minute:.0f}", 68, BLUE)
    # may dem
    card(d, (580, 270, 1010, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    d.rounded_rectangle([620, 360, 970, 470], radius=16, fill=NAVY)
    text(d, (795, 415), str(reading), 66, (134, 239, 172))
    text(d, (795, 512), "xung/phút", 36, MUTED, bold=False)

# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. Mỗi lần giảm như nhau", "B. Còn khoảng một nửa", "C. Sau 5 phút gần hết")
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, 0, ROWS[0][1])
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 990, 1020, 1600), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1045), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1150, "Số đếm sau mỗi 5 phút?", 46, INK, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.15); y = 1270 + i * 100
        card(d, (110, y - 42, 970, y + 42), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=22, w=4)
        text(d, (150, y), s, 40, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1562, 940, 1576], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1562, 140 + 800 * (1 - q), 1576], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: do phong, dem moi 5 phut, ghi bang ----------------
def row_at(i, sc):
    M = sc["M"]
    return M[1] + 0.9 + 0.6 * i

def do_state(t, sc):
    """(phut tren dong ho, so tren may dem, nhan dong ho, dang tua nhanh)"""
    M = sc["M"]
    if t < M[1]: return 0, PHONG, "đo phông", False
    if t < row_at(0, sc): return 0, "···", None, False
    for i in range(5):
        a, b = row_at(i, sc), row_at(i + 1, sc)
        if t < b:
            k = clamp((t - a - 0.15) / (b - a - 0.3))
            if k <= 0: return ROWS[i][0], ROWS[i][1], None, False
            return ROWS[i][0] + 5 * k, "···", None, True
    return 25, ROWS[5][1], None, False

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    m, rd, lbl, ff = do_state(t, sc)
    rig(d, t, m, rd, src=clamp((t - sc["M"][1]) / 0.6), clock_lbl=lbl)
    if ff: text(d, (295, 515), "▶▶ tua nhanh", 36, ORANGE)
    card(d, (60, 995, 1020, 1590), fill=WHITE, outline=NAVY, w=4)
    text(d, (W / 2, 1040), f"Phông nền = {PHONG}", 42, PURPLE, alpha=appear(t, 0.9))
    xs = [215, 520, 830]
    for x, c in zip(xs, ["t (phút)", "Đo được", "Trừ phông"]): text(d, (x, 1105), c, 38, MUTED)
    d.line([(90, 1138), (990, 1138)], fill=LIGHT, width=4)
    last = max([i for i in range(6) if t >= row_at(i, sc)], default=-1)
    hl = appear(t, sc["M"][3])
    for i, (tm, hd, hs) in enumerate(ROWS):
        a = appear(t, row_at(i, sc), 0.35); y = 1180 + i * 66
        if a <= 0: continue
        if hl > 0 and i < 3: d.rounded_rectangle([80, y - 30, 1000, y + 30], radius=14, fill=A((220, 252, 231), hl))
        elif i == last and hl <= 0: d.rounded_rectangle([80, y - 30, 1000, y + 30], radius=14, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), str(tm), 42, MUTED, alpha=a)
        text(d, (xs[1], y), str(hd), 42, INK, bold=False, alpha=a)
        text(d, (xs[2], y), str(hs), 44, GREEN, alpha=appear(t, max(row_at(i, sc) + 0.3, sc["M"][2] + 0.2), 0.35))

# ---------------- canh 3: dap an B + do thi + ti so ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = back((t - 0.2) / 0.5) if t > 0.2 else 0
    card(d, (60, 250, 1020, 350), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 300), "Đáp án B", int(48 * clamp(k, 0.3, 1.0)), GREEN)
    x0, x1, yb, yt = 190, 950, 950, 470
    X = lambda m: x0 + m / 25 * (x1 - x0); Y = lambda h: yb - h / 900 * (yb - yt)
    card(d, (60, 380, 1020, 1050), fill=WHITE, outline=LIGHT, w=3)
    for h in (200, 400, 600, 800): d.line([(x0, Y(h)), (x1, Y(h))], fill=(240, 236, 228), width=2)
    d.line([(x0, yb), (x1 + 25, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 40)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 50), "H (xung/phút)", 34, MUTED, anchor="lm")
    text(d, (x1 + 25, yb + 76), "t (phút)", 34, MUTED, anchor="rm")
    for m in range(0, 26, 5):
        d.line([(X(m), yb), (X(m), yb + 10)], fill=NAVY, width=3)
        text(d, (X(m), yb + 34), str(m), 34, MUTED, bold=False)
    for h in (0, 200, 400, 600, 800):
        d.line([(x0 - 10, Y(h)), (x0, Y(h))], fill=NAVY, width=4); text(d, (x0 - 18, Y(h)), str(h), 34, MUTED, bold=False, anchor="rm")
    kc = ease((t - M[0] - 1.2) / 1.2)
    if kc > 0:
        pts = [(X(25 * j / 100), Y(model(25 * j / 100))) for j in range(101)]
        d.line(pts[:max(2, int(len(pts) * kc))], fill=A(BLUE, 0.45), width=6, joint="curve")
    for i, (tm, _, hs) in enumerate(ROWS):
        a = appear(t, 0.5 + i * 0.2, 0.4)
        if a <= 0: continue
        dot(d, X(tm), Y(hs), 15 * back(a), ORANGE, WHITE)
        if i < 3: text(d, (X(tm) + 30, Y(hs) - 30), str(hs), 36, ORANGE, anchor="lm", alpha=a)
    # T: tu 812 xuong 398 mat 5 phut
    kt = appear(t, M[2] + 0.2)
    if kt > 0:
        for xx in range(int(X(0)), int(X(5)), 22):
            d.line([(xx, Y(398)), (min(xx + 12, X(5)), Y(398))], fill=A(GREEN, kt), width=4)
        d.line([(X(5), Y(398)), (X(5), yb)], fill=A(GREEN, kt), width=4)
        d.rectangle([X(0), yb - 8, X(5), yb], fill=A(GREEN, kt))
        text(d, (X(5) + 20, yb - 40), "T ≈ 5 phút", 42, GREEN, anchor="lm", alpha=kt)
    # day ti so
    a1 = appear(t, M[1] - 0.2)
    if a1 <= 0: return
    card(d, (60, 1080, 1020, 1430), fill=A(WHITE, a1), outline=A(LIGHT, a1), w=3)
    text(d, (W / 2, 1130), "Số trước chia số sau", 38, MUTED, alpha=a1)
    vx = [130 + i * 164 for i in range(6)]
    for i, (_, _, hs) in enumerate(ROWS):
        text(d, (vx[i], 1230), str(hs), 44, INK, alpha=a1)
    for i, r in enumerate(RATIOS):
        a = appear(t, M[1] + 0.3 + i * 0.25, 0.35)
        cx = (vx[i] + vx[i + 1]) / 2
        arrow(d, (vx[i] + 34, 1290), (vx[i + 1] - 34, 1290), A(ORANGE, a), w=4, head=14)
        text(d, (cx, 1345), r, 38, ORANGE, alpha=a)

# ---------------- canh 4: co che + chua noi duoc gi ----------------
NC, NR = 10, 6
RN = random.Random(8)
_q = [(k + 0.5) / (NC * NR) for k in range(NC * NR)]; RN.shuffle(_q)
DEC = [-T_BR * math.log(u) / math.log(2) for u in _q]      # phut phan ra cua tung hat nhan (phan bo mu, T = 5)
def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    st = [0.6, 1.6, 2.6]                                   # dong ho mo phong: 0 -> 5 -> 10 -> 15 phut, dung o moi moc
    m = 5 * sum(clamp((t - a) / 0.6) for a in st)
    card(d, (60, 250, 1020, 330), fill=WHITE, outline=LIGHT, r=24, w=3)
    FR = {0: "đủ", 5: "½", 10: "¼", 15: "⅛"}
    mm = 5 * round(m / 5)
    text(d, (W / 2, 290), f"phút {5 * math.ceil(m / 5 - 1e-6)}" + (f" · {FR[mm]}" if abs(m - mm) < 0.05 else ""), 48, BLUE)
    for i in range(NC * NR):
        cx = 150 + (i % NC) * 87; cy = 400 + (i // NC) * 92
        if DEC[i] <= m:
            dot(d, cx, cy, 20, LIGHT)
            fl = 1 - clamp((m - DEC[i]) / 2.5)
            if fl > 0:
                arrow(d, (cx + 18, cy - 18), (cx + 18 + 40 * (1 - fl) + 10, cy - 18 - 40 * (1 - fl) - 10), A(ORANGE, fl), w=4, head=10)
        else:
            dot(d, cx, cy, 20, ORANGE, NAVY)
            if t > M[1] + 0.5: text(d, (cx, cy), "?", 30, WHITE, alpha=appear(t, M[1] + 0.5))
    lg = [(ORANGE, "chưa rã"), (LIGHT, "đã rã")]
    for j, (c, s) in enumerate(lg):
        dot(d, 200 + j * 400, 975, 18, c, NAVY if c == ORANGE else None)
        text(d, (230 + j * 400, 975), s, 36, MUTED, bold=False, anchor="lm")
    a = appear(t, 0.3)
    card(d, (60, 1040, 1020, 1210), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    rich(d, W / 2, 1125, "N giảm → H = λN giảm theo", 48, BLUE, alpha=appear(t, 1.2))
    b = appear(t, M[1] + 0.2)
    card(d, (60, 1260, 1020, 1450), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
    text(d, (W / 2, 1355), "Chưa nói được gì?", 48, PURPLE, alpha=b)

# ---------------- canh 5: bay quen tru phong ----------------
def strip(d, y, title, vals, rats, col, a):
    card(d, (60, y, 1020, y + 330), fill=A(WHITE, a), outline=A(col, a), w=5)
    text(d, (W / 2, y + 50), title, 40, col, alpha=a)
    xs = [250, 540, 830]
    for x, tm in zip(xs, (15, 20, 25)): text(d, (x, y + 120), f"phút {tm}", 36, MUTED, bold=False, alpha=a)
    for x, v in zip(xs, vals): text(d, (x, y + 185), str(v), 52, INK, alpha=a)
    for j, r in enumerate(rats):
        cx = (xs[j] + xs[j + 1]) / 2
        arrow(d, (xs[j] + 60, y + 245), (xs[j + 1] - 60, y + 245), A(col, a), w=4, head=14)
        text(d, (cx, y + 290), r, 40, col, alpha=a)

def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 340), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 295), "Bẫy: quên trừ phông", 48, RED, alpha=appear(t, 0.1))
    strip(d, 370, "Chưa trừ phông", [r[1] for r in ROWS[3:]], ["1,60", "1,60"], RED, appear(t, M[1] - 0.2))
    strip(d, 730, "Đã trừ phông", [r[2] for r in ROWS[3:]], RATIOS[3:], GREEN, appear(t, M[1] + 0.8))
    c = appear(t, M[2])
    card(d, (60, 1095, 1020, 1400), fill=A((254, 242, 242), c), r=28)
    ctext(d, 1250, "→ T đọc ra LỚN HƠN thật", 54, RED, alpha=c)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    chot_hoi(d, t, sc, "Chu kì T: số đếm (trừ phông) còn một nửa",
             "Bớt một nửa lượng nguồn thì T còn 5 phút không?")

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for i in range(5):                                   # tich tac khi dong ho tua nhanh 5 phut
        a, b = row_at(i, do) + 0.15, row_at(i + 1, do) - 0.15
        x = a
        while x < b: out.append((do["t0"] + x, "tick")); x += 0.25
    out += [(do["t0"] + do["M"][3], "tap"), (an["t0"] + 0.2, "ding"),
            (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-phongxa-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Chu kì bán rã · thachlab.id.vn", scenes=[
 dict(key="hook", title="Số đếm phóng xạ theo thời gian", draw=s_hook, tail=0.6, caps=[
   ("Nguồn trước ống Geiger.", 2.4),
   ("Dừng video, chọn A, B hoặc C.", 5.0)]),
 dict(key="do", title="Đếm cứ 5 phút một lần", draw=s_do, tail=0.8, caps=[
   ("Đo phông nền trước.", 2.5),
   ("Đặt nguồn, đếm mỗi 5 phút.", 4.0),
   ("Trừ phông mỗi số.", 2.5),
   ("Còn một nửa.", 2.5)]),
 dict(key="ans", title="Đọc chu kì bán rã", draw=s_ans, tail=0.6, caps=[
   ("Cứ 5 phút: một nửa.", 2.5),
   ("Tỉ số gần bằng 2.", 2.5),
   ("Đọc T trên đồ thị.", 2.4)]),
 dict(key="why", title="Vì sao còn một nửa?", draw=s_why, tail=0.6, caps=[
   ("Mỗi hạt có cùng xác suất phân rã.", 3.6),
   ("Từng hạt: ngẫu nhiên.", 4.0)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.6, caps=[
   ("Nhìn số cuối bảng.", 2.5),
   ("Giảm chậm hơn.", 2.5),
   ("Trừ phông trước.", 2.5)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 5.5)]),
])
