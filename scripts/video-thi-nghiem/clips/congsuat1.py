# Clip: tn-l10-cong-suat-01 - Leo cau thang bon lan, moi lan nhanh hon (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-cong-suat-01.json:
#   tham_so: m = 50 kg, h = 3,0 m, g = 10 m/s2, sai_so_do t = 0,3 s.
#   so_lieu_mau: t (s) 12,0 / 8,5 / 6,0 / 4,0 ; P (W) 125 / 176 / 250 / 375 ; A = 1500 J (ghi_chu).
#   ghi_chu: sai so bam gio 0,3 s = 7,5 % o lan 4.
# Canh: Du doan (chi cau hoi + hinh, K10: lan 4 gap may lan lan 1) -> Tien hanh (nguoi leo, dong ho dong pha,
#       tua nhanh x4, bang t) -> Dap an "gap 3 lan" + cot P -> Rut ra (A khong doi, cot P tang theo ti le)
#       -> Bay (leo nhanh thi cong lon) + chua noi duoc -> Chot + cau hoi tu nho lai (300 W -> t = ?, so chua hien).
from engine import *

ROWS = [(1, 12.0, 125), (2, 8.5, 176), (3, 6.0, 250), (4, 4.0, 375)]   # so_lieu_mau
A_J = 1500
SPEED = 4.0          # tua nhanh 4 lan
GAP = 0.5            # nghi giua hai lan leo (giay tren man)
NST = 10             # so bac
def f1(x): return f"{x:.1f}".replace(".", ",")

STONE = (214, 206, 192); STONE_D = (150, 140, 124)

# ---------------- cau thang + nguoi ----------------
def stairs(d, x0, yb, w, h, n=NST, alpha=1.0, label=True):
    sw, sh = w / n, h / n
    d.line([(x0 - 80, yb), (x0 + w + 30, yb)], fill=A(INK, alpha), width=4)          # san
    pts = [(x0, yb)]
    for i in range(n):
        pts += [(x0 + i * sw, yb - (i + 1) * sh), (x0 + (i + 1) * sw, yb - (i + 1) * sh)]
    pts += [(x0 + w, yb)]
    d.polygon(pts, fill=A(STONE, alpha))
    d.line(pts[:-1], fill=A(STONE_D, alpha), width=4)
    if label:   # mui ten do cao h
        xa = x0 + w + 55
        arrow(d, (xa, yb - h / 2), (xa, yb - h + 2), A(NAVY, alpha), w=5, head=18)
        arrow(d, (xa, yb - h / 2), (xa, yb - 2), A(NAVY, alpha), w=5, head=18)
        d.line([(x0 + w + 10, yb - h), (xa + 20, yb - h)], fill=A(NAVY, alpha), width=3)
    return sw, sh

def person(d, x, yf, s=1.0, alpha=1.0, col=ORANGE):
    """Nguoi dung, ban chan o y = yf."""
    lw = int(9 * s)
    d.line([(x - 12 * s, yf), (x, yf - 45 * s), (x + 12 * s, yf)], fill=A(NAVY, alpha), width=lw, joint="curve")
    d.rounded_rectangle([x - 20 * s, yf - 105 * s, x + 20 * s, yf - 40 * s], radius=int(14 * s), fill=A(col, alpha))
    dot(d, x, yf - 128 * s, 21 * s, A((240, 196, 150), alpha))

def person_on(d, x0, yb, w, h, p, s=1.0, alpha=1.0):
    """p = 0 (chan cau thang) .. 1 (dinh). Di tung bac."""
    sw, sh = w / NST, h / NST
    i = int(round(p * NST)) - 1
    if i < 0: person(d, x0 - 40, yb, s, alpha); return
    person(d, x0 + (i + 0.5) * sw, yb - (i + 1) * sh, s, alpha)

# Hinh chinh: cau thang trong the (40, 265, 1040, 900)
SX0, SYB, SW, SH = 150, 870, 560, 420
def scene_stairs(d, p, alpha=1.0):
    card(d, (40, 265, 1040, 900), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    stairs(d, SX0, SYB, SW, SH, alpha=alpha)
    text(d, (SX0 + SW + 85, SYB - SH / 2), "h = 3,0 m", 44, NAVY, anchor="lm", alpha=alpha)
    person_on(d, SX0, SYB, SW, SH, p, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    scene_stairs(d, 0.0)
    text(d, (150, 655), "m = 50 kg", 42, ORANGE)
    for j, (lab, tt) in enumerate((("Lần 1", "12,0 s"), ("Lần 4", "4,0 s"))):
        y = 320 + j * 92
        card(d, (70, y, 470, y + 76), fill=(255, 247, 237), outline=ORANGE, r=22, w=3)
        text(d, (100, y + 38), lab, 42, INK, anchor="lm")
        text(d, (440, y + 38), tt, 44, NAVY, anchor="rm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 200, "Lần 4 leo nhanh hơn lần 1.", 50, INK, maxw=880, alpha=a)
    ctext(d, y0 + 340, "Công suất lần 4 gấp mấy lần lần 1?", 50, INK, maxw=860, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 510, 940, y0 + 524], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 510, 140 + 800 * (1 - p), y0 + 524], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def run_start(sc): return sc["M"][0] + 0.4
def schedule(sc):
    """[(bat dau tren man, ket thuc tren man, t that)] cho 4 lan leo."""
    out, s = [], run_start(sc)
    for _, tt, _ in ROWS:
        out.append((s, s + tt / SPEED, tt)); s += tt / SPEED + GAP
    return out
def state(t, sc):
    """(lan dang/vua leo, vi tri p, so dong ho, so lan da xong)."""
    st = schedule(sc); cur, p, clk, done = 0, 0.0, 0.0, 0
    for i, (a, b, tt) in enumerate(st):
        if t >= a:
            cur = i; clk = min(tt, (t - a) * SPEED); p = clk / tt
            if t >= b: done = i + 1
    return cur, p, clk, done

XS = (210, 520, 840)
def table(d, t, done, ty=930, show_p=0.0, pk=None, bg=True):
    if bg: card(d, (40, ty, 1040, ty + 640), fill=WHITE, outline=LIGHT, w=3)
    else: d.rounded_rectangle((40, ty, 1040, ty + 640), radius=34, outline=LIGHT, width=3)
    heads = ("Lần", "t (s)", "P (W)")
    for j, (x, s) in enumerate(zip(XS, heads)):
        if j < 2: text(d, (x, ty + 60), s, 44, INK)
        elif show_p > 0: text(d, (x, ty + 60), s, 44, ORANGE, alpha=show_p)
    d.line([(70, ty + 110), (1010, ty + 110)], fill=LIGHT, width=3)
    for j, (n, tt, P) in enumerate(ROWS):
        yy = ty + 180 + j * 118
        if j < done:
            text(d, (XS[0], yy), str(n), 50, INK)
            text(d, (XS[1], yy), f1(tt), 52, NAVY)
        if pk is not None:
            k = pk(j)
            if k > 0: text(d, (XS[2], yy), str(P), 52, ORANGE, alpha=k)

def s_do(img, d, t, sc):
    cur, p, clk, done = state(t, sc)
    scene_stairs(d, p)
    card(d, (70, 300, 470, 470), fill=(255, 247, 237), outline=ORANGE, r=22, w=3)
    text(d, (100, 345), f"Lần {cur + 1}", 46, INK, anchor="lm")
    text(d, (440, 420), f"{f1(clk)} s", 60, NAVY, anchor="rm")
    if t > run_start(sc) - 0.2:
        text(d, (270, 520), "tua nhanh ×4", 44, MUTED)
    table(d, t, done)

# ---------------- canh 3: Dap an + cot P ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    s = "ĐÁP ÁN · gấp 3 lần"
    pw = tw(d, s, F(40)) + 60
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 340), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 305), s, 40, WHITE, alpha=ka)
    card(d, (40, 380, 1040, 540), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5)
    text(d, (W / 2, 460), "P = A / t", 62, GREEN, alpha=ka)
    TY = 590
    pk = lambda j: appear(t, 0.3 + 0.3 * j, 0.4)
    card(d, (40, TY, 1040, TY + 640), fill=WHITE)
    for j in (0, 3):
        k = appear(t, 1.6, 0.4)
        if k > 0:
            yy = TY + 180 + j * 118
            d.rounded_rectangle([60, yy - 50, 1020, yy + 50], radius=20, fill=A((255, 247, 237), k))
    table(d, t, 4, ty=TY, show_p=appear(t, 0.2, 0.4), pk=pk, bg=False)
    k = appear(t, 1.6, 0.4)
    if k > 0:
        arrow(d, (XS[2] + 90, TY + 180 + 20), (XS[2] + 90, TY + 180 + 3 * 118 - 20), A(ORANGE, k), w=5, head=18)
        text(d, (XS[2] + 120, TY + 180 + 1.5 * 118), "×3", 52, ORANGE, anchor="lm", alpha=k)

# ---------------- canh 4: Rut ra ----------------
def bars(d, x0, y0, w, h, vals, vmax, col, alpha, labels, title, grow=1.0):
    d.line([(x0, y0), (x0, y0 + h)], fill=A(INK, alpha), width=4)
    d.line([(x0, y0 + h), (x0 + w, y0 + h)], fill=A(INK, alpha), width=4)
    text(d, (x0 + w / 2, y0 - 44), title, 46, col, alpha=alpha)
    bw = w / len(vals)
    for j, v in enumerate(vals):
        bh = h * v / vmax * grow
        xa = x0 + j * bw + bw * 0.2; xb = x0 + (j + 1) * bw - bw * 0.2
        d.rectangle([xa, y0 + h - bh, xb, y0 + h], fill=A(col, alpha))
        text(d, ((xa + xb) / 2, y0 + h + 42), str(j + 1), 42, INK, alpha=alpha)
        if labels and j == len(vals) - 1 and grow > 0.98:      # chia cot cuoi thanh khoi bang cot 1 -> thay x3
            u = h * vals[0] / vmax
            for q in range(1, int(round(v / vals[0]))):
                d.line([(xa, y0 + h - q * u), (xb, y0 + h - q * u)], fill=A(WHITE, alpha), width=5)
        if labels: text(d, ((xa + xb) / 2, y0 + h - bh - 32), str(v), 42, col, alpha=alpha * clamp(grow * 3 - 2))

def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.5)
    card(d, (40, 265, 1040, 520), fill=A(WHITE, k0), outline=A(NAVY, k0), w=5)
    text(d, (W / 2, 335), "A = m·g·h", 52, INK, alpha=k0)
    text(d, (W / 2, 440), "= 50·10·3,0 = 1500 J", 52, GREEN, alpha=appear(t, 0.8, 0.5))
    card(d, (40, 560, 1040, 1250), fill=WHITE, outline=LIGHT, w=3)
    ka = appear(t, M[0] + 0.3, 0.5)
    gA = ease((t - M[0] - 0.3) / 0.8)
    bars(d, 110, 680, 360, 420, [A_J] * 4, 1750, GREEN, ka, False, "A (J)", gA)
    if gA > 0.98:
        text(d, (290, 680 + 420 - 420 * A_J / 1750 - 32), "1500", 42, GREEN)
    kp = appear(t, M[1] - 0.2, 0.5)
    gP = ease((t - M[1] + 0.2) / 0.8)
    bars(d, 600, 680, 340, 420, [r[2] for r in ROWS], 440, ORANGE, kp, True, "P (W)", gP)
    if gP > 0.98:                                   # vach chuan o muc cot 1 (125 W)
        yr = 680 + 420 - 420 * 125 / 440
        for x in range(600, 940, 28): d.line([(x, yr), (x + 14, yr)], fill=ORANGE, width=4)
        text(d, (936, 680 + 420 - 420 * 375 / 440 / 2), "×3", 46, ORANGE, anchor="lm")
    text(d, (W / 2, 1205), "lần leo", 40, MUTED, alpha=ka)
    k3 = appear(t, M[1] + 1.2, 0.5)
    card(d, (110, 1300, 970, 1480), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
    text(d, (W / 2, 1360), "A không đổi", 46, GREEN, alpha=k3)
    text(d, (W / 2, 1430), "t ngắn hơn → P lớn hơn", 46, GREEN, alpha=k3)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def mini(d, cx, lab, tt, alpha=1.0):
    x0, yb, w, h = cx - 170, 800, 300, 330
    stairs(d, x0, yb, w, h, alpha=alpha, label=False)
    person_on(d, x0, yb, w, h, 1.0, s=0.8, alpha=alpha)
    text(d, (cx - 20, 335), lab, 46, INK, alpha=alpha)
    text(d, (cx - 20, 860), tt, 46, NAVY, alpha=alpha)

def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    mini(d, 300, "chậm", "12,0 s"); mini(d, 780, "nhanh", "4,0 s")
    d.line([(540, 300), (540, 930)], fill=LIGHT, width=3)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 1000
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“Leo nhanh thì công lớn hơn”"
        ks = clamp((t - 2.4) / 0.4)
        f = F(48); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2, yy), q, 48, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * a1), width=5)
        kk = a1 * appear(t, 2.9, 0.5)
        card(d, (110, y0 + 300, 970, y0 + 470), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 385), "Hai lần cùng A = 1500 J", 50, GREEN, alpha=kk)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Thí nghiệm chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.2, 0.4)
        card(d, (70, y0 + 140, 1010, y0 + 330), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, y0 + 195), "Chưa biết:", 44, RED, alpha=kk)
        text(d, (W / 2, y0 + 270), "năng lượng cơ thể tốn thật", 44, RED, alpha=kk)
        kq = k2 * appear(t, M[1] + 0.9, 0.4)
        card(d, (70, y0 + 370, 1010, y0 + 560), fill=A((255, 247, 237), kq), outline=A(ORANGE, kq), r=24, w=4)
        text(d, (W / 2, y0 + 425), "Bấm tay lệch 0,3 s:", 44, ORANGE, alpha=kq)
        text(d, (W / 2, y0 + 500), "P lần 4 lệch cỡ 7,5 %", 44, ORANGE, alpha=kq)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Cùng công: t càng ngắn, P càng lớn",
             "Bạn 50 kg leo cầu thang này với công suất 300 W. Hết mấy giây?",
             body=lambda d, t, k: text(d, (W / 2, 1120), "cầu thang cao 3,0 m", 44, MUTED, alpha=appear(t, sc["M"][0] + 0.6, 0.5)))

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.3, "ding")]
    for a, bb, _ in schedule(do):
        out += [(do["t0"] + a, "tap")]
        x = a + 0.5
        while x < bb - 0.1: out.append((do["t0"] + x, "tick")); x += 0.5
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.2, "tap"),
            (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l10-cong-suat-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Công suất · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Leo cầu thang bốn lần", draw=s_hook, tail=0.8, caps=[
   ("Cùng người, cùng cầu thang.", 2.9),
   ("Dừng video, chọn câu trả lời.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Bạn khác bấm giờ từ chân tới đỉnh.", 6.0),
   ("Thời gian giảm dần.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("t giảm 3 lần, P tăng 3 lần.", 3.6)]),
 dict(key="rutra", title="Vì sao?", draw=s_rutra, tail=0.6, caps=[
   ("Công nâng người như nhau mỗi lần.", 3.6),
   ("Chia cho t nhỏ hơn.", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Bẫy thường gặp.", 4.4),
   ("Giới hạn của phép đo.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 5.6)]),
])
