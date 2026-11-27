# Clip: tn-l10-huongtam-04 - Vien bi trong vong co cho ho: roi thanh thi di theo duong nao? (9/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-huongtam-04.json:
#   tham_so: R = 0,1 m (nap ~20 cm), v mac dinh 0,6 m/s, cho ho ~1/6 vong (60 deg), goc_ho 0-330 buoc 30 (dung 0 va 180).
#   so_lieu_mau: m = 0,02 kg, v = 0,6 m/s -> N = 0,072 N (so tinh tu mo hinh, ghi_chu: thi nghiem dinh tinh).
#   mo_hinh: tren thanh N = m.v^2/R huong vao tam ; o cho ho N = 0, bi thang deu theo tiep tuyen tai diem roi thanh.
# Hinh nhin tu tren, bi chay nguoc chieu kim dong ho. Cho ho bat dau o goc g (do, tinh nguoc chieu kim tu huong dong),
#   dai 60 deg; bi roi thanh tai g, di thang theo tiep tuyen (-sin g, cos g). Hinh chieu cham (khong ghi he so: kho khong co).
# Du doan (27/11, cong moi): o Quan sat hop exp cua bai ghi san "toi cho ho, bi lan thang theo tiep tuyen", nen KHONG hoi
#   duong di. Hoi: bung nhanh hay cham, duong di sau cho ho co khac? Dap an: KHONG - cung tiep tuyen tai diem roi thanh
#   (v chi doi do lon N = m.v^2/R, khong doi huong). Lan 1 v = 0,4 ; lan 2 v = 0,8 m/s (so_lieu_mau), cung cho ho goc 0.
# Cau chot dung goc_ho = 270 (day vong, chua tung hien): bi di ngang sang phai. Dap so khong hien.
from engine import *

GAP = 60.0                                   # do dai cho ho (do)
WALL = (148, 163, 184); WALL_D = (71, 85, 105); FLOOR = (241, 236, 226); BALL = (59, 130, 246)
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
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

def state(c, Rb, g, tau, om=OMEGA):
    """-> (vi tri, u hien tai, da roi thanh?, quang thang da di px). Bat dau g - 300 do."""
    gr = math.radians(g); u0 = gr - math.radians(360 - GAP); t1 = (gr - u0) / om
    if tau <= t1:
        u = u0 + om * max(0.0, tau); return P(c, Rb, u), u, False, 0.0
    s = om * Rb * (tau - t1); p0 = P(c, Rb, gr); tx, ty = TG(gr)
    return (p0[0] + s * tx, p0[1] + s * ty), gr, True, s

def run(d, c, R, Rb, g, tau, om=OMEGA, ymin=330, ymax=1000, nlen=125):
    gr = math.radians(g)
    p, u, out, s = state(c, Rb, g, tau, om)
    stop = False
    p0 = P(c, Rb, gr); tx, ty = TG(gr)
    if out:                                                                  # bi dung o mep vung ve
        smax = (p0[1] - ymin) if ty < -0.5 else ((ymax - p0[1]) if ty > 0.5 else 1e9)
        if s > smax: s = smax; p = (p0[0] + s * tx, p0[1] + s * ty); stop = True
        dashed(d, p0, p, (100, 116, 139), w=5, seg=16)
    ball(d, p)
    if not stop:
        vx, vy = TG(u); arrow(d, (p[0] + 20 * vx, p[1] + 20 * vy), (p[0] + 120 * vx, p[1] + 120 * vy), GREEN, w=7, head=22)
        text(d, (p[0] + 150 * vx + 34, p[1] + 150 * vy), "v", 58, DGREEN)
        if not out:                                                          # luc thanh: chi VAO TAM
            nx, ny = IN(u); arrow(d, (p[0] + 22 * nx, p[1] + 22 * ny), (p[0] + (22 + nlen) * nx, p[1] + (22 + nlen) * ny), RED, w=7, head=22)
            text(d, (p[0] + (60 + nlen) * nx, p[1] + (60 + nlen) * ny), "N", 58, DRED)
    return out, stop

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- canh 1: Du doan (K10) ----------------
C, R, RB = (540, 650), 270, 242
def s_hook(img, d, t, sc):
    M = sc["M"]
    ring(d, C, R, 0)
    u = math.radians(100 + 17 * t); p = P(C, RB, u); ball(d, p)            # bi chay cham tren thanh [60, 360), chua toi cho ho
    pts = [P(C, RB - 50, u + math.radians(a)) for a in range(10, 41, 2)]
    d.line(pts, fill=GREEN, width=7, joint="curve"); arrow(d, pts[-3], pts[-1], GREEN, w=7, head=22)
    lb = P(C, R + 70, math.radians(30)); text(d, (lb[0] + 40, lb[1] - 40), "chỗ hở", 55, INK)
    text(d, (C[0], C[1] + 55), "tâm", 55, MUTED)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1085 + (1 - k) * 30
    card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    for j, s1 in enumerate(("Búng nhanh hay chậm,", "đường sau chỗ hở có khác?")):
        text(d, (W / 2, y0 + 190 + j * 85), s1, 60, PURPLE if j == 1 else INK, alpha=k)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh (cung cho ho goc 0, v = 0,4 roi 0,8 m/s) ----------------
VS, NS = [0.4, 0.8], [0.032, 0.128]
OMS = [1.4, 2.8]                              # toc do goc tren man ti le v (chieu cham)
TR = [0.6, 5.6]                               # luc bung
def table(d, nrow, k=1.0):
    card(d, (40, 1050, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 1115), "m = 0,02 kg", 55, INK)
    for x, h, col in ((200, "lần", INK), (520, "v (m/s)", DGREEN), (840, "N (N)", DRED)):
        text(d, (x, 1210), h, 58, col)
    d.line([(70, 1260), (1010, 1260)], fill=LIGHT, width=3)
    for i in range(nrow):
        y = 1340 + i * 110
        text(d, (200, y), str(i + 1), 58, INK)
        text(d, (520, y), vn(VS[i], 1), 58, DGREEN)
        text(d, (840, y), vn(NS[i], 3), 58, DRED)

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")

def s_do(img, d, t, sc):
    j = 1 if t >= TR[1] - 0.3 else 0
    ring(d, C, R, 0)
    if j == 1:                                                               # vet lan 1 giu lai
        p0 = P(C, RB, 0.0); dashed(d, p0, (p0[0], 330), (100, 116, 139), w=5, seg=16)
    run(d, C, R, RB, 0, t - TR[j], om=OMS[j], nlen=60 + 65 * j)
    text(d, (180, 330), f"Lần {j + 1}", 58, INK)
    text(d, (1000, 990), "chiếu chậm", 55, MUTED, anchor="rm")
    table(d, j + 1 if (j == 1 or t > TR[0] + 1.0) else 0)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ring(d, C, R, 0)
    p0 = P(C, RB, 0.0); p1 = (p0[0], 330)
    k1 = appear(t, 0.4, 0.4)
    d.line([p0, p1], fill=(100, 116, 139), width=12)                          # hai vet chong khit
    d.line([p0, p1], fill=A(GREEN, k1), width=5)
    dashed(d, C, (p0[0] + 160, p0[1]), A(GRAY, k1), w=4, seg=14)              # ban kinh keo dai
    sq = 30; d.line([(p0[0], p0[1] - sq), (p0[0] - sq, p0[1] - sq), (p0[0] - sq, p0[1])], fill=A(NAVY, k1), width=4)
    text(d, (p0[0] + 30, 400), "lần 1", 55, MUTED, anchor="lm", alpha=k1)
    text(d, (p0[0] + 30, 470), "lần 2", 55, DGREEN, anchor="lm", alpha=k1)
    text(d, (C[0] + 120, C[1] + 55), "bán kính", 55, MUTED, alpha=k1)
    ka = appear(t, M[1], 0.45)
    if ka <= 0: return
    yk = 1085 + (1 - ka) * 30
    card(d, (40, yk, 1040, yk + 420), fill=A(WHITE, ka), outline=A(NAVY, ka), w=6)
    pill(d, W / 2, yk + 70, "ĐÁP ÁN", NAVY, ka)
    text(d, (W / 2, yk + 200), "đường đi như cũ", 64, BLUE, alpha=ka)
    text(d, (W / 2, yk + 310), "tiếp tuyến tại chỗ rời", 58, DGREEN, alpha=ka)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    ring(d, C, R, 0)
    k1 = appear(t, 0.4, 0.4)
    u = math.radians(120 + 25 * t); p = P(C, RB, u); ball(d, p)
    nx, ny = IN(u); arrow(d, (p[0] + 22 * nx, p[1] + 22 * ny), (p[0] + 150 * nx, p[1] + 150 * ny), RED, w=8, head=24)
    text(d, (p[0] + 195 * nx, p[1] + 195 * ny), "N", 58, DRED)
    yk = 1085
    card(d, (40, yk, 1040, yk + 500), fill=A(WHITE, k1), outline=A(GREEN, k1), w=6)
    pill(d, W / 2, yk + 70, "RÚT RA", GREEN, k1)
    text(d, (W / 2, yk + 190), "Thành đẩy bi vào tâm", 60, DRED, alpha=k1)
    k2 = appear(t, M[1], 0.4)
    text(d, (W / 2, yk + 300), "Mất thành, bi đi thẳng", 60, NAVY, alpha=k2)
    text(d, (W / 2, yk + 390), "theo tiếp tuyến", 60, NAVY, alpha=k2)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pill(d, W / 2, y0 + 70, "BẪY", DRED, a1)
    q = "Lực li tâm hất bi ra"
    ks = clamp((t - M[1]) / 0.4); lw = tw(d, q, F(58)); yy = 450
    text(d, (W / 2, yy), q, 58, mix(INK, GRAY, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
    c = (330, 900); Rr, Rb = 200, 182
    ring(d, c, Rr, 0, k=a1, w=16)
    p0 = P(c, Rb, 0.0); ball(d, p0, r=16, k=a1)
    kw = a1 * (1 - 0.6 * ks)                                                    # hai duong sai mo dan khi gach
    dashed(d, p0, (p0[0] + 300, p0[1]), A(RED, kw), w=6, seg=16)               # sai: theo ban kinh
    arrow(d, (p0[0] + 270, p0[1]), (p0[0] + 300, p0[1]), A(RED, kw), w=6, head=20)
    text(d, (p0[0] + 170, p0[1] + 50), "✗ bán kính", 55, DRED, alpha=kw)
    pts = [P(c, Rb, math.radians(a)) for a in range(0, 41, 4)]                 # sai: cong tiep
    for i in range(0, len(pts) - 1, 2): d.line([pts[i], pts[i + 1]], fill=A(RED, kw), width=6)
    text(d, (p0[0] + 170, 760), "✗ cong tiếp", 55, DRED, alpha=kw)
    kk = appear(t, M[1], 0.5)
    if kk > 0:
        gl = 0.1 + 0.9 * ease(clamp((t - M[1]) / 1.4))
        d.line([p0, (p0[0], p0[1] - 330 * gl)], fill=A(GREEN, kk), width=8)
        arrow(d, (p0[0], p0[1] - 330 * gl + 30), (p0[0], p0[1] - 330 * gl), A(GREEN, kk), w=8, head=22)
        text(d, (p0[0] + 30, p0[1] - 330), "✓ tiếp tuyến", 55, DGREEN, anchor="lm", alpha=kk)
    k3 = appear(t, M[2] - 0.1, 0.4)
    if k3 > 0:
        yk = 1180 + (1 - k3) * 30
        card(d, (40, yk, 1040, yk + 400), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, yk + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, yk + 200), "N chỉ là số tính", 58, INK, alpha=k3)
        text(d, (W / 2, yk + 290), "chưa đo thật", 58, INK, alpha=k3)

# ---------------- canh 6: Thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    g = 270                                                                  # cho ho bat dau o day vong
    ring(d, C, R, g, k=k)
    u = math.radians(120 + 18 * t); p = P(C, RB, u); ball(d, p, k=k)        # bi toi gan cho ho, chua roi
    pts = [P(C, RB - 50, u + math.radians(a)) for a in range(10, 41, 2)]
    d.line(pts, fill=A(GREEN, k), width=7, joint="curve"); arrow(d, pts[-3], pts[-1], A(GREEN, k), w=7, head=22)
    q = P(C, R, math.radians(300)); text(d, (q[0], q[1] + 10), "?", 72, PURPLE, alpha=k)
    text(d, (C[0], C[1] + 55), "tâm", 55, MUTED, alpha=k)
    card(d, (40, 1030, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1100, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 1215), "Chỗ hở ở đáy vòng.", 60, INK, alpha=k)
    text(d, (W / 2, 1310), "Rời thành, bi đi về đâu?", 60, DORANGE, alpha=k)
    seg_bar(d, 1420, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for a, om in zip(TR, OMS): cs += [(do["t0"] + a, "tap"), (do["t0"] + a + math.radians(360 - GAP) / om, "tap")]
    cs += [(da["t0"] + da["M"][1], "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-huongtam-04", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực hướng tâm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Viên bi trong vòng hở", draw=s_hook, tail=0.2, caps=[
   ("Nhìn từ trên xuống.", 2.6),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Lần 1: búng nhẹ.", 5.0),
   ("Lần 2: búng mạnh gấp đôi.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Chồng hai vệt lên nhau.", 3.0),
   ("Đáp án: đường đi như cũ.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Thành đẩy bi vào tâm.", 3.4),
   ("Mất thành, bi đi thẳng theo tiếp tuyến.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Lực li tâm hất bi ra?", 3.4),
   ("Không lực đẩy ra.", 3.0),
   ("N chỉ là số tính.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])
