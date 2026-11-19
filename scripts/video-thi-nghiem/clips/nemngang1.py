# Clip: tn-l10-nemngang-01 - Mot bi ban ngang, mot bi tha roi cung luc (lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-nemngang-01.json (_kiem_so() doi chieu):
#   tham_so: g = 9,8 m/s2 ; so_lieu_mau (h, v0, t, L): 0,5 2 0,319 0,64 | 0,8 2 0,404 0,81 | 0,8 5 0,404 2,02 | 1,25 5 0,505 2,53
#   Clip chieu hang 2 va 3 (cung h = 0,80 m, v0 2 -> 5 m/s). Hang 1 dung cho cau chot (chua hien), hang 4 khong dung.
# Du doan (K10, khong nut A-D): v0 tang tu 2 len 5 m/s, bi A (ban ngang) va bi B (tha roi) cham san lech nhau the nao?
#   -> dap an: lan nao cung cham cung luc. Khac cau Du doan mo bai (may bay / truc thang) va Cau 2 (20 m, 5 & 20 m/s).
# Khong ve cham bong moi 0,1 s cua bi A (cach deu theo phuong ngang = dap an Cau 3 cua bai) -> chi ve vet lien + vach
#   ngang noi hai bi.
# Bay = sai_so_thuong_gap "hai vien khong duoc tha dung cung luc (lech 1-2 khung hinh)". Khong dung hien_tuong_hay_sai[1]
#   (= dap an du doan), [3] (= Cau 3 / Bay 2 cua bai).
# Chua noi duoc: gia_thiet "bo qua luc can" -> luc can lon thi sao.
# Thu nghi: h = 0,50 m, v0 = 2 m/s, bi B roi het 0,319 s -> bi A cung 0,319 s, L = 2 x 0,319 = 0,64 m (hang 1, chua hien).
from engine import *

G = 9.8
H0 = 0.80
ROWS = [(0.8, 2, 0.404, 0.81), (0.8, 5, 0.404, 2.02)]                 # so_lieu_mau hang 2, 3
CHOT = (0.5, 2, 0.319, 0.64)                                           # so_lieu_mau hang 1 (cau chot)
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-nemngang-01.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    for r in ROWS + [CHOT]:
        assert any(all(abs(a - b) < 1e-9 for a, b in zip(r, h)) for h in hang), r
        assert abs(math.sqrt(2 * r[0] / G) - r[2]) < 6e-4 and abs(r[1] * r[2] - r[3]) < 6e-3, r
    assert {p["ky_hieu"]: p for p in k["tham_so"]}["g"]["gia_tri"] == G
    assert "0,64" in k["so_lieu_mau"]["ghi_chu"] and "câu chốt" in k["so_lieu_mau"]["ghi_chu"]
_kiem_so()

STEEL_A = (59, 130, 246); STEEL_B = (234, 88, 12); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
DGREEN = (10, 110, 50); DRED = (185, 28, 28); GHOST = (196, 202, 216)

# ---------------- khung dung ti le (330 px/m ca hai phuong) ----------------
PXM, YF, X0 = 330.0, 960, 330          # px/m ; mat san ; dau mang (x = 0 cua tam xa)
XB = X0 - 44                           # bi B duoc kep ngay truoc dau mang, cung do cao
def P(x, y): return (X0 + x * PXM, YF - y * PXM)
YL = P(0, H0)[1]                       # do cao mieng mang tren man

def _segs(s, size):
    out = []
    for p in [p for p in TOK.split(s) if p]:
        if p.startswith("_{"): out.append((p[2:-1], max(36, int(size * 0.75)), size * 0.26))
        else: out.append((p, size, 0))
    return out
def rich_w(d, s, size): return sum(tw(d, q, F(sz)) for q, sz, _ in _segs(s, size))
def rx(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    x = cx - rich_w(d, s, size) / 2 if anchor == "m" else (cx - rich_w(d, s, size) if anchor == "r" else cx)
    for q, sz, dy in _segs(s, size):
        dtext(d, (x, cy + dy), q, F(sz), color, alpha, "lm"); x += tw(d, q, F(sz))

def ball(d, x, y, col, lab=None, a=1.0):
    dot(d, x, y, 15, A(col, a), outline=A(NAVY, a))
    if lab: text(d, (x, y - 44), lab, 40, col, alpha=a)

def setup(d, a=1.0):
    c = lambda col: A(col, a)
    d.rectangle([150, YL + 22, XB - 50, YF], fill=c(WOOD), outline=c(WOOD_D), width=3)            # ban
    d.rectangle([40, YF, 1040, YF + 18], fill=c((205, 196, 180)))                                  # san
    d.polygon([(118, YL - 62), (176, YL + 16), (176, YL + 24), (110, YL - 56)], fill=c((150, 160, 180)))
    d.rectangle([176, YL + 16, X0 + 2, YL + 24], fill=c((150, 160, 180)))                         # mang, dau ra nam ngang
    d.line([(XB, YL - 150), (XB, YL - 18)], fill=c(GRAY), width=5)                                 # kep giu bi B
    d.line([(XB - 14, YL - 18), (XB + 14, YL - 18)], fill=c(GRAY), width=5)
    # thuoc cuon tren san: vach moi 0,25 m, so moi 0,5 m
    d.rectangle([X0, YF + 18, P(2.08, 0)[0], YF + 40], fill=c((253, 224, 71)), outline=c(WOOD_D), width=2)
    for k in range(0, 9):
        xx = P(k * 0.25, 0)[0]; L = 22 if k % 2 == 0 else 12
        d.line([(xx, YF + 18), (xx, YF + 18 + L)], fill=c(NAVY), width=3)
        if k % 2 == 0: text(d, (xx, YF + 74), "0" if k == 0 else vn(k * 0.25, 1).replace(",0", ""), 38, INK, alpha=a)
    text(d, (1022, YF + 74), "m", 38, MUTED, alpha=a)
    # vach do cao 0,80 m (giua mep ban va duong roi cua bi B), chu ben phai duong roi
    xm = XB - 26
    d.line([(xm, YL), (xm, YF)], fill=c(PURPLE), width=3)
    for yy in (YL, YF): d.line([(xm - 12, yy), (xm + 12, yy)], fill=c(PURPLE), width=3)
    text(d, (XB + 22, (YL + YF) / 2 + 20), "0,80 m", 40, PURPLE, anchor="lm", alpha=a)

def clock(d, x, lab, col, val, a=1.0):
    card(d, (x - 210, 290, x + 210, 410), fill=A(WHITE, a), outline=A(col, a), w=4, r=24)
    text(d, (x - 120, 350), lab, 40, col, alpha=a)
    text(d, (x + 90, 350), vn(val, 3) + " s", 46, INK, alpha=a)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1110), fill=WHITE, outline=LIGHT, w=3)
    setup(d)
    ball(d, X0 - 4, YL, STEEL_A, "A"); ball(d, XB, YL, STEEL_B, "B")
    ka = appear(t, 0.8, 0.5)
    arrow(d, (X0 + 20, YL), (X0 + 170, YL), A(BLUE, ka), w=7, head=20)
    rx(d, X0 + 100, YL + 50, "v_{0}", 46, BLUE, alpha=ka)
    text(d, (1000, 330), "bi A: bắn ngang", 40, STEEL_A, anchor="rm")
    text(d, (1000, 390), "bi B: thả rơi", 40, STEEL_B, anchor="rm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1130 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 450), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 54), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    rx(d, W / 2, y0 + 150, "Bắn bi A với v_{0} = 2 m/s, rồi 5 m/s.", 44, INK, alpha=a)
    text(d, (W / 2, y0 + 225), "Hai bi chạm sàn lệch nhau thế nào?", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 315), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 385, 940, y0 + 399], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 385, 140 + 800 * (1 - p), y0 + 399], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (2 lan, chieu cham 5 lan) ----------------
SLOW = 5.0
STARTS = (0.6, 5.0)                    # luc gat/tha moi lan (giay trong canh)
def run_state(t):
    """-> (lan j, tau that (0..t_roi), so hang bang da xong)."""
    j = 1 if t >= STARTS[1] else 0
    tt = ROWS[j][2]
    tau = clamp((t - STARTS[j]) / SLOW, 0.0, tt)
    rows = j + (1 if (t - STARTS[j]) / SLOW >= tt else 0)
    return j, tau, rows

def flight(d, j, tau, ghost_prev=True, line=True):
    h, v0, tt, L = ROWS[j]
    if ghost_prev and j == 1:                                              # vet lan 1 mo
        d.line([P(ROWS[0][1] * s / 40 * ROWS[0][2], h - G / 2 * (s / 40 * ROWS[0][2]) ** 2) for s in range(41)], fill=GHOST, width=3)
        lx = P(ROWS[0][3], 0)[0]; d.line([(lx, YF - 16), (lx, YF + 2)], fill=GHOST, width=5)
    n = max(1, int(40 * tau / tt))
    pts = [P(v0 * tau * s / n, h - G / 2 * (tau * s / n) ** 2) for s in range(n + 1)]
    if tau > 0: d.line(pts, fill=A(STEEL_A, 0.45), width=4)
    ya = P(0, h - G / 2 * tau * tau)[1]
    if tau > 0: d.line([(XB, YL), (XB, ya)], fill=A(STEEL_B, 0.45), width=4)
    xa = P(v0 * tau, 0)[0]
    land = tau >= tt - 1e-9
    yy = min(ya, YF - 15)
    if line and 0 < tau:                                                    # vach ngang noi hai bi: cung do cao
        for x in range(int(XB) + 18, int(xa) - 18, 26): d.line([(x, yy), (x + 13, yy)], fill=DGREEN, width=4)
    if land:
        d.line([(xa, YF - 18), (xa, YF + 2)], fill=ORANGE, width=6)
    ball(d, XB, yy, STEEL_B, "B"); ball(d, xa if tau > 0 else X0 - 4, yy, STEEL_A, "A")

def table(d, y, n, hl=-1):
    card(d, (40, y, 1040, y + 300), fill=WHITE, outline=NAVY, w=4)
    xs = (190, 430, 660, 890)
    rx(d, xs[0], y + 50, "v_{0} (m/s)", 40, BLUE)
    text(d, (xs[1], y + 50), "t bi A (s)", 40, STEEL_A); text(d, (xs[2], y + 50), "t bi B (s)", 40, STEEL_B)
    text(d, (xs[3], y + 50), "L (m)", 40, ORANGE)
    d.line([(70, y + 92), (1010, y + 92)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 150 + i * 90; h, v0, tt, L = ROWS[i]
        if i == hl: d.rounded_rectangle([60, yy - 36, 1020, yy + 36], radius=14, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(v0), 46, INK); text(d, (xs[1], yy), vn(tt, 3), 46, INK)
        text(d, (xs[2], yy), vn(tt, 3), 46, INK); text(d, (xs[3], yy), vn(L), 46, INK)

def s_do(img, d, t, sc):
    j, tau, rows = run_state(t)
    card(d, (40, 265, 1040, 1110), fill=WHITE, outline=LIGHT, w=3)
    setup(d)
    clock(d, 290, "Bi A", STEEL_A, tau); clock(d, 790, "Bi B", STEEL_B, tau)
    text(d, (W / 2, 460), "chiếu chậm 5 lần", 40, MUTED, bold=False)
    rx(d, 1000, 530, "v_{0} = " + str(ROWS[j][1]) + " m/s", 46, BLUE, anchor="r")
    flight(d, j, tau)
    if rows > j:
        text(d, (1000, 600), "L = " + vn(ROWS[j][3]) + " m", 46, ORANGE, anchor="rm")
    table(d, 1140, rows, hl=rows - 1 if rows > j else -1)

def _kiem_dong_bo():
    """Moi 0,05 s: hai dong ho bang nhau va dung dung luc cham san; hang bang chi hien khi bi da cham."""
    bad = []; t = 0.0
    while t < 11.0:
        j, tau, rows = run_state(t)
        h, v0, tt, L = ROWS[j]
        ya = h - G / 2 * tau * tau
        if ya < -1e-6: bad.append((round(t, 2), "bi xuyen san"))
        if rows > j and abs(tau - tt) > 1e-9: bad.append((round(t, 2), "hang hien truoc khi cham"))
        if abs(tau - tt) < 1e-9 and rows <= j: bad.append((round(t, 2), "da cham ma chua co hang"))
        if j == 1 and t < STARTS[1]: bad.append((round(t, 2), "lan 2 som"))
        if j == 1 and run_state(STARTS[1] - 0.05)[2] != 1: bad.append("lan 1 chua xong truoc lan 2")
        t += 0.05
    if run_state(10.5)[2] != 2: bad.append("chua du 2 hang")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1110), fill=WHITE, outline=LIGHT, w=3)
    setup(d)
    clock(d, 290, "Bi A", STEEL_A, ROWS[1][2]); clock(d, 790, "Bi B", STEEL_B, ROWS[1][2])
    flight(d, 1, ROWS[1][2], line=False)
    lx1 = P(ROWS[0][3], 0)[0]; lx2 = P(ROWS[1][3], 0)[0]
    text(d, (lx1, YF - 50), "0,81", 40, MUTED); text(d, (lx2, YF - 50), "2,02", 40, ORANGE)
    pill(d, "ĐÁP ÁN: lần nào cũng chạm cùng lúc", 1160, appear(t, 0.15, 0.4), size=40)
    k1 = appear(t, M[1] - 0.1, 0.5)
    if k1 > 0:
        card(d, (60, 1240, 1020, 1580), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        text(d, (W / 2, 1310), "t = √(2h/g) = 0,404 s", 48, DGREEN, alpha=k1)
        rx(d, W / 2, 1395, "Công thức không chứa v_{0}", 44, DGREEN, alpha=k1)
        k2 = appear(t, M[2] - 0.1, 0.5)
        rx(d, W / 2, 1500, "L = v_{0}·t: 0,81 m → 2,02 m", 46, ORANGE, alpha=k2)

# ---------------- canh 4: Bay ; chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    ks = clamp((t - 1.8) / 0.4); kg = appear(t, 2.5, 0.4)
    card(d, (40, 265, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    # khung hinh quay cham: hai bi gan san, lech nhau mot chut (tha khong cung luc)
    yf = 820
    d.rectangle([80, yf, 1000, yf + 14], fill=(205, 196, 180))
    off = 46 * (1 - kg)
    ball(d, 330, yf - 15 - 120, STEEL_B, "B"); ball(d, 720, yf - 15 - 120 - off, STEEL_A, "A")
    if off > 2:
        d.line([(330, yf - 135), (720, yf - 135)], fill=A(DRED, 0.8), width=3)
        text(d, (870, yf - 160 - off / 2), "lệch", 40, DRED)
    else:
        for x in range(352, 700, 26): d.line([(x, yf - 135), (x + 13, yf - 135)], fill=DGREEN, width=4)
        text(d, (W / 2, yf - 215), "thả lại", 40, DGREEN)
    y = 930
    if a1 > 0:
        card(d, (40, y, 1040, y + 500), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        for j, q in enumerate(("Lệch 1–2 khung hình:", "A rơi lâu hơn")):
            f = F(46); lw = tw(d, q, f); yy = y + 170 + j * 70
            text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 400), "✓ Do thả không cùng lúc", 46, DGREEN, alpha=a1 * kg)
    if k3 > 0:
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 210), "Lực cản không khí lớn thì sao?", 46, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Bắn mạnh hay nhẹ, thả cùng lúc:", 48, DGREEN, alpha=k0)
    text(d, (W / 2, 450), "phần rơi như nhau", 48, DGREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1330), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    rx(d, W / 2, 790, "Máng cao 0,50 m, bắn v_{0} = 2 m/s.", 46, INK, alpha=kq)
    text(d, (W / 2, 868), "Bi B rơi hết 0,319 s.", 46, INK, alpha=kq)
    text(d, (W / 2, 946), "Bi A bay xa bao nhiêu?", 46, INK, alpha=kq)
    kh = appear(t, M[0] + 4.2, 0.5)
    if kh > 0:
        card(d, (90, 1050, 990, 1290), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1105), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1210), "Hai bi rời tay cùng một lúc", 44, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + s + r[2] * SLOW, "tap") for s, r in zip(STARTS, ROWS)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.8, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l10-nemngang-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động ném · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bắn ngang và thả rơi", draw=s_hook, tail=0.3, caps=[
   ("Hai bi cùng độ cao, cùng lúc.", 3.2),
   ("Tự trả lời trước khi xem.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Lần 1: bắn chậm, chiếu chậm.", 4.2),
   ("Lần 2: bắn mạnh hơn.", 4.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Hai đồng hồ dừng cùng lúc.", 3.2),
   ("Thời gian rơi chỉ do độ cao.", 3.4),
   ("Bắn mạnh: chỉ bay xa hơn.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy khi xem video quay chậm.", 4.6),
   ("Câu còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 7.6)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
