# Clip: tn-l10-huongtam-04 - Vien bi trong vong co cho ho: roi thanh thi di theo duong nao? (9/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-huongtam-04.json:
#   tham_so: R = 0,1 m (nap ~20 cm), v mac dinh 0,6 m/s, cho ho ~1/6 vong (60 deg), goc_ho 0-330 buoc 30 (dung 0 va 180).
#   so_lieu_mau: m = 0,02 kg, v = 0,6 m/s -> N = 0,072 N (so tinh tu mo hinh, ghi_chu: thi nghiem dinh tinh).
#   mo_hinh: tren thanh N = m.v^2/R huong vao tam ; o cho ho N = 0, bi thang deu theo tiep tuyen tai diem roi thanh.
# Hinh nhin tu tren, bi chay nguoc chieu kim dong ho. Cho ho bat dau o goc g (do, tinh nguoc chieu kim tu huong dong),
#   dai 60 deg; bi roi thanh tai g, di thang theo tiep tuyen (-sin g, cos g). Hinh chieu cham (khong ghi he so: kho khong co).
# Du doan (K10: chi cau hoi + hinh): toi cho ho, bi di theo duong nao? Dap an: thang theo tiep tuyen.
#   Nhieu (khung): ra xa tam theo ban kinh ; tiep tuc cong mot doan roi moi thang.
# Cau chot dung goc_ho = 270 (day vong, chua tung hien): bi di ngang sang phai.
from engine import *

GAP = 60.0                                   # do dai cho ho (do)
WALL = (148, 163, 184); WALL_D = (71, 85, 105); FLOOR = (241, 236, 226); BALL = (59, 130, 246)
OMEGA = 2.0                                  # toc do goc tren man (rad/s canh) - chieu cham

def P(c, R, u): return (c[0] + R * math.cos(u), c[1] - R * math.sin(u))     # u (rad) nguoc chieu kim tu huong dong
def TG(u): return (-math.sin(u), -math.cos(u))                               # tiep tuyen theo chieu chuyen dong (man hinh)
def IN(u): return (-math.cos(u), math.sin(u))                                # huong vao tam (man hinh)

def ring(d, c, R, g, k=1.0, w=20):
    """thanh vong ban kinh R (px) tru cho ho [g, g + 60] do."""
    d.ellipse([c[0] - R - 20, c[1] - R - 20, c[0] + R + 20, c[1] + R + 20], fill=A(FLOOR, k))
    a0 = (-(g + 360)) % 360; span = 360 - GAP
    d.arc([c[0] - R - w / 2, c[1] - R - w / 2, c[0] + R + w / 2, c[1] + R + w / 2], a0, a0 + span, fill=A(WALL, k), width=w)
    for u in (g + GAP, g + 360):                                             # hai dau thanh
        p = P(c, R, math.radians(u)); d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=A(WALL_D, k))
    d.ellipse([c[0] - 7, c[1] - 7, c[0] + 7, c[1] + 7], fill=A(NAVY, k))

def ball(d, p, r=18, k=1.0):
    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=A(BALL, k), outline=A(NAVY, k), width=3)
    d.ellipse([p[0] - r * 0.5, p[1] - r * 0.55, p[0] - r * 0.1, p[1] - r * 0.15], fill=A(WHITE, 0.8 * k))

def dashed(d, a, b, col, w=5, seg=18):
    L = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(1, int(L / seg))
    for i in range(0, n, 2):
        d.line([(lerp(a[0], b[0], i / n), lerp(a[1], b[1], i / n)), (lerp(a[0], b[0], min(1, (i + 1) / n)), lerp(a[1], b[1], min(1, (i + 1) / n)))], fill=col, width=w)

def state(c, Rb, g, tau):
    """-> (vi tri, u hien tai, da roi thanh?, quang thang da di px). Bat dau g - 300 do."""
    gr = math.radians(g); u0 = gr - math.radians(360 - GAP); t1 = (gr - u0) / OMEGA
    if tau <= t1:
        u = u0 + OMEGA * max(0.0, tau); return P(c, Rb, u), u, False, 0.0
    s = OMEGA * Rb * (tau - t1); p0 = P(c, Rb, gr); tx, ty = TG(gr)
    return (p0[0] + s * tx, p0[1] + s * ty), gr, True, s

def run(d, c, R, Rb, g, tau, vec=True, ymin=350, ymax=1000):
    ring(d, c, R, g)
    gr = math.radians(g)
    p, u, out, s = state(c, Rb, g, tau)
    stop = False
    if out:                                                                  # bi dung o mep vung ve (vet khong lo ra ngoai)
        p0 = P(c, Rb, gr); tx, ty = TG(gr)
        smax = (p0[1] - ymin) if ty < -0.5 else ((ymax - p0[1]) if ty > 0.5 else 1e9)
        if s > smax: s = smax; p = (p0[0] + s * tx, p0[1] + s * ty); stop = True
    if out:                                                                  # vet thang (giu lai)
        p0 = P(c, Rb, gr); dashed(d, p0, p, (100, 116, 139), w=5, seg=16)
    if ymin - 1 <= p[1] <= ymax + 1 and 40 < p[0] < 1040:
        ball(d, p)
        if vec and not stop:
            tx, ty = TG(u); arrow(d, p, (p[0] + 120 * tx, p[1] + 120 * ty), GREEN, w=7, head=22)
            text(d, (p[0] + 150 * tx + 30, p[1] + 150 * ty), "v", 44, GREEN)
            if not out:
                nx, ny = IN(u); arrow(d, (p[0] + 22 * nx, p[1] + 22 * ny), (p[0] + 125 * nx, p[1] + 125 * ny), RED, w=7, head=22)
                text(d, (p[0] + 160 * nx, p[1] + 160 * ny - 10), "N", 44, RED)
    return out

# ---------------- canh 1: Du doan ----------------
C, R, RB = (540, 650), 270, 242
def s_hook(img, d, t, sc):
    M = sc["M"]
    ring(d, C, R, 0)
    u = math.radians(-50); p = P(C, RB, u); ball(d, p)
    pts = [P(C, RB - 50, math.radians(a)) for a in range(-40, -9, 2)]          # mui ten chieu chay (cong theo vong)
    d.line(pts, fill=GREEN, width=7, joint="curve"); arrow(d, pts[-3], pts[-1], GREEN, w=7, head=22)
    text(d, P(C, R - 10, math.radians(30)), "?", 72, PURPLE)
    lb = P(C, R + 70, math.radians(30)); text(d, (lb[0] + 40, lb[1] - 40), "chỗ hở", 40, INK)
    text(d, (C[0], C[1] + 50), "tâm", 40, MUTED)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 55), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 170, "Bi chạy sát thành theo mũi tên.", 46, INK, maxw=920, alpha=a)
    ctext(d, y0 + 300, "Tới chỗ hở, bi đi theo đường nào?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 1.4, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 460, 940, y0 + 474], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 460, 140 + 800 * (1 - p), y0 + 474], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (hai lan, cho ho o 0 va 180 do) ----------------
TR = [(0.6, 0), (6.2, 180)]                   # (luc bung, goc_ho)
def s_do(img, d, t, sc):
    j = 1 if t >= TR[1][0] - 0.4 else 0
    t0, g = TR[j]
    out = run(d, C, R, RB, g, t - t0)
    text(d, (W / 2, 300), f"Lần {j + 1}", 44, INK)
    if j == 1:
        k = appear(t, TR[1][0] - 0.4, 0.4)
        text(d, (C[0], C[1] + 50), "chỗ hở bên trái", 40, MUTED, alpha=k)
    text(d, (980, 1000), "chiếu chậm", 40, MUTED, anchor="rm")
    card(d, (40, 1050, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 1120), "m = 0,02 kg · v = 0,6 m/s", 40, INK, bold=False)
    if not out:
        text(d, (W / 2, 1260), "Thành đẩy bi vào tâm", 46, RED)
        text(d, (W / 2, 1360), "N = 0,072 N", 54, RED)
    else:
        text(d, (W / 2, 1260), "Chỗ hở: hết thành đẩy", 46, NAVY)
        text(d, (W / 2, 1360), "N = 0", 54, NAVY)

# ---------------- canh 3: Dap an ----------------
def mini(d, c, R, g, k):
    ring(d, c, R, g, k=k, w=12)
    gr = math.radians(g); Rb = R - 12; p0 = P(c, Rb, gr); tx, ty = TG(gr)
    p1 = (p0[0] + 230 * tx, p0[1] + 230 * ty)
    dashed(d, p0, p1, A((100, 116, 139), k), w=5, seg=14); ball(d, p1, r=14, k=k)

def s_dapan(img, d, t, sc):
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · thẳng theo tiếp tuyến"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 330), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 296), lb, 40, WHITE, alpha=ka)
    c = (440, 700); Rr, Rb = 230, 212
    ring(d, c, Rr, 0)
    p0 = P(c, Rb, 0.0); p1 = (p0[0], 380)
    kr = appear(t, 0.8, 0.4)
    dashed(d, (c[0] - 60, c[1]), (p0[0] + 180, p0[1]), A(GRAY, kr), w=4, seg=14)        # ban kinh keo dai
    text(d, (c[0] + 90, c[1] + 40), "bán kính", 40, MUTED, alpha=kr)
    d.line([p0, p1], fill=GREEN, width=8); ball(d, p1, r=16)
    sq = 30; d.line([(p0[0], p0[1] - sq), (p0[0] + sq, p0[1] - sq), (p0[0] + sq, p0[1])], fill=A(NAVY, kr), width=4)
    kv = appear(t, 1.6, 0.4)
    text(d, (p0[0] + 50, 460), "vuông góc", 40, GREEN, anchor="lm", alpha=kv)
    text(d, (p0[0] + 50, 510), "bán kính", 40, GREEN, anchor="lm", alpha=kv)
    km = appear(t, 2.4, 0.4)
    card(d, (40, 1050, 1040, 1590), fill=A(WHITE, km), outline=A(LIGHT, km), w=3)
    mini(d, (300, 1350), 120, 0, km); mini(d, (780, 1300), 120, 180, km)
    text(d, (300, 1110), "Lần 1", 40, INK, alpha=km); text(d, (780, 1110), "Lần 2", 40, INK, alpha=km)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    c = (540, 650); ring(d, c, R, 0)
    u = math.radians(200); p = P(c, RB, u); ball(d, p)
    nx, ny = IN(u); arrow(d, (p[0] + 22 * nx, p[1] + 22 * ny), (p[0] + 140 * nx, p[1] + 140 * ny), RED, w=8, head=24)
    text(d, (p[0] + 90 * nx, p[1] + 90 * ny - 45), "N", 44, RED)
    tx, ty = TG(u); arrow(d, p, (p[0] + 120 * tx, p[1] + 120 * ty), GREEN, w=7, head=22)
    text(d, (p[0] + 120 * tx - 40, p[1] + 120 * ty), "v", 44, GREEN)
    if t < M[1] - 0.1:
        k1 = appear(t, 0.5, 0.45)
        card(d, (40, 1050, 1040, 1470), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
        text(d, (W / 2, 1140), "Còn thành: N vào tâm, đi cong", 46, RED, alpha=k1)
        k2 = appear(t, 1.6, 0.45)
        text(d, (W / 2, 1290), "Mất thành: N = 0", 46, NAVY, alpha=k2)
        text(d, (W / 2, 1385), "đi thẳng theo quán tính", 46, NAVY, alpha=k2)
    else:
        k2 = appear(t, M[1] - 0.1, 0.45)
        card(d, (40, 1050, 1040, 1590), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, 1120), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        card(d, (80, 1180, 1000, 1550), fill=A((254, 242, 242), kk), r=24)
        text(d, (W / 2, 1290), "Chưa đo được N", 46, RED, alpha=kk)
        text(d, (W / 2, 1440), "0,072 N chỉ là số tính", 46, RED, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1500), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
    text(d, (W / 2, y0 + 165), "✗ “Lực li tâm” hất bi ra", 46, RED, alpha=a1)
    c = (400, 900); Rr, Rb = 200, 182
    ring(d, c, Rr, 0, k=a1, w=16)
    p0 = P(c, Rb, 0.0); ball(d, p0, r=16, k=a1)
    dashed(d, p0, (p0[0] + 300, p0[1]), A(RED, a1), w=6, seg=16)                      # sai: theo ban kinh
    arrow(d, (p0[0] + 270, p0[1]), (p0[0] + 300, p0[1]), A(RED, a1), w=6, head=20)
    text(d, (p0[0] + 160, p0[1] + 45), "✗ theo bán kính", 40, RED, alpha=a1)
    pts = [P(c, Rb, math.radians(a)) for a in range(0, 41, 4)]                        # sai: cong tiep
    for i in range(0, len(pts) - 1, 2): d.line([pts[i], pts[i + 1]], fill=A(RED, a1), width=6)
    text(d, (420, 800), "✗ cong tiếp", 40, RED, alpha=a1)
    kk = appear(t, M[0] + 2.3, 0.5)
    d.line([p0, (p0[0], p0[1] - 330)], fill=A(GREEN, kk), width=8)
    arrow(d, (p0[0], p0[1] - 300), (p0[0], p0[1] - 330), A(GREEN, kk), w=8, head=22)
    text(d, (p0[0] + 30, p0[1] - 260), "✓ tiếp tuyến", 44, GREEN, anchor="lm", alpha=kk)
    card(d, (90, y0 + 980, 990, y0 + 1190), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, y0 + 1085), "✓ Không lực nào đẩy ra", 48, GREEN, alpha=kk)

# ---------------- canh 6: Chot ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):
        c = (500, 1110); Rr, Rb = 150, 134; g = 270                  # cho ho bat dau o day vong (chua ve duong ra)
        ring(d, c, Rr, g, k=k, w=12)
        u = math.radians(215); p = P(c, Rb, u); ball(d, p, r=13, k=k)
        pts = [P(c, Rb - 32, math.radians(a)) for a in range(195, 246, 3)]
        d.line(pts, fill=A(GREEN, k), width=6, joint="curve"); arrow(d, pts[-3], pts[-1], A(GREEN, k), w=6, head=18)
        text(d, P(c, Rr - 30, math.radians(300)), "?", 56, PURPLE, alpha=k)
        kh = appear(t, M[0] + 2.8, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Tiếp tuyến tại điểm rời thành", 40, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Mất lực hướng tâm:\nđi thẳng theo tiếp tuyến",
             "Chỗ hở ở đáy vòng:\nbi rời thành đi về đâu?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    t1 = math.radians(360 - GAP) / OMEGA
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for a, _ in TR: cs += [(do["t0"] + a, "tap"), (do["t0"] + a + t1, "tap")]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + 0.15, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-huongtam-04", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực hướng tâm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Viên bi trong vòng hở", draw=s_hook, tail=0.5, caps=[
   ("Vòng tròn hở một đoạn.", 3.0),
   ("Dừng video, chọn câu trả lời.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Búng bi chạy sát thành.", 5.6),
   ("Dời chỗ hở, búng lại.", 5.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Hai lần, cùng một kiểu đường.", 5.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Thành vòng đóng vai lực hướng tâm.", 4.4),
   ("Còn điều chưa biết.", 3.8)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("Bi có bị hất ra ngoài?", 5.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 6.4)]),
])
