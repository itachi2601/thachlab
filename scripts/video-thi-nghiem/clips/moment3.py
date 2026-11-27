# Clip: tn-l10-moment-luc-03 - Ngau luc lam thuoc quay quanh trong tam (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-moment-luc-03.json (_kiem_so() doi chieu):
#   thuoc 30 cm, mat ban nhan; so_lieu_mau F (N) / d (m) / M (N.m): 0,5/0,3/0,15 ; 1,0/0,3/0,3 ; 1,0/0,15/0,15
#   tham_so: F 0,1-2 N, d 0,05-0,3 m.
# Du doan (K10, khong nut): ngau luc 1,0 N dat o vach 5 va vach 20 (d = 0,15 m = hang 3 kho) -> thuoc quay quanh vach nao?
#   (dap an: vach 15, trong tam - khong phai vach 12,5 giua hai luc). Doi ca so voi ban 1 ("thuoc chuyen dong the nao")
#   vi o Quan sat cua hop exp trong bai da ghi san "quay tai cho quanh vach 15 cm, khong truot di".
#   Vi tri vach 5/20 la lua chon dung hinh (kho chi cho d = 0,15 m) -> bao thay.
# Bay = hien_tuong_hay_sai[1] (M = F.(d/2)). CHUA NOI: giu co dinh mot diem.
# Chot (v2 theo kiem-code + coordinator 27/11): moi luc 2,0 N (F max tham_so) o vach 5 va vach 25 -> d tu doc 0,20 m,
#   M = 2,0 . 0,20 = 0,40 N.m (khong trung bang 0,15/0,3/0,15; khong trung Cau 5 7,2 N.m). Ca nay chua co trong ghi_chu kho.
from engine import *

ROWS = [(0.5, 0.3, 0.15), (1.0, 0.3, 0.3), (1.0, 0.15, 0.15)]   # so_lieu_mau
DRED = (185, 28, 28); NOTE = (60, 64, 84); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
WOOD = (247, 214, 120); WOOD_D = (176, 132, 40)
SKIN = (241, 200, 168); SKIN_D = (196, 140, 104)
PX_CM = 26 * 0.95            # px moi cm doc thuoc
HL, HW = 408, 55
ALEN = 170
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def X(c): return (c - 15) * PX_CM            # toa do doc thuoc cua vach c (cm), goc o vach 15

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-moment-luc-03.json")))
    assert [tuple(h) for h in k["so_lieu_mau"]["hang"]] == ROWS
    for f, dd, m in ROWS: assert abs(f * dd - m) < 1e-9
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["F"]["max"] == 2 and ts["d"]["max"] == 0.3
    assert (20 - 5) / 100 == ROWS[2][1]                                    # du doan: vach 5 va 20 -> d = 0,15 m
    assert abs(1.0 * 0.10 + 1.0 * 0.05 - ROWS[2][2]) < 1e-9                  # quanh vach 15: 10 cm + 5 cm
    assert abs(2.0 * (25 - 5) / 100 - 0.4) < 1e-9 and 0.4 not in [r[2] for r in ROWS]   # ca chot
_kiem_so()

_RULER = {}
def ruler_img(s=1.0):
    if s in _RULER: return _RULER[s]
    pad = 6; w, h = int(2 * HL * s), int(2 * HW * s)
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([pad, pad, pad + w, pad + h], radius=int(10 * s), fill=WOOD + (255,), outline=WOOD_D + (255,), width=max(2, int(4 * s)))
    for c in range(31):
        x = pad + int(HL * s + X(c) * s)
        L = (30 if c % 5 == 0 else 16) * s
        dd.line([(x, pad), (x, pad + L)], fill=NAVY + (255,), width=max(2, int(3 * s)))
        if c % 5 == 0 and s >= 0.99:
            dd.text((x, pad + h - 34), str(c), font=F(55), fill=NAVY + (255,), anchor="mm")
    _RULER[s] = im; return im

def rot(p, phi, c):
    a = math.radians(phi); x, y = p
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))

def ruler(img, c, phi, s=1.0):
    r = ruler_img(s).rotate(-phi, resample=Image.BICUBIC, expand=True)
    img.paste(r, (int(c[0] - r.width / 2), int(c[1] - r.height / 2)), r)

def finger(d, c, phi, x, side, s=1.0, alpha=1.0):
    """side=+1: ngon o phia duoi day len; -1: o phia tren day xuong."""
    y0 = side * HW * s; y1 = side * (HW + 150) * s; r = 30 * s
    pts = [rot(p, phi, c) for p in ((x - r, y0 + side * r), (x + r, y0 + side * r), (x + r, y1), (x - r, y1))]
    d.polygon(pts, fill=A(SKIN, alpha), outline=A(SKIN_D, alpha))
    tx, ty = rot((x, y0 + side * r), phi, c); d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=A(SKIN, alpha))

def forces(d, c, phi, xa, xb, lab=None, s=1.0, alpha=1.0, fing=True):
    """Luc huong len dat o xa (vecto ve tu canh tren), luc huong xuong o xb (tu canh duoi); ngon tay o phia doi dien."""
    for x, side in ((xa * s, 1), (xb * s, -1)):
        if fing: finger(d, c, phi, x, side, s, alpha)
        p1 = rot((x, -side * HW * s), phi, c); p2 = rot((x, -side * (HW + ALEN) * s), phi, c)
        arrow(d, p1, p2, A(RED, alpha), w=max(5, int(8 * s)), head=int(30 * s))
        if lab:
            lp = rot((x - math.copysign(95, x if x else 1) * s, -side * (HW + ALEN * 0.62) * s), phi, c)
            text(d, lp, lab, 55, RED, alpha=alpha)

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

def dim(d, c, x0, x1, y, s_lab, col=NAVY, a=1.0):
    X0, X1 = c[0] + x0, c[0] + x1
    for XX in (X0, X1):
        for yy in range(int(c[1] + HW + 8), int(y) - 6, 26): d.line([(XX, yy), (XX, yy + 12)], fill=A(GRAY, a), width=3)
    d.line([(X0 + 4, y), (X1 - 4, y)], fill=A(col, a), width=5)
    for XX in (X0 + 4, X1 - 4): d.line([(XX, y - 16), (XX, y + 16)], fill=A(col, a), width=5)
    text(d, ((X0 + X1) / 2, y + 48), s_lab, 55, col, alpha=a)

# ---------------- canh 1: Du doan (K10) ----------------
CH = (W / 2, 560)
def s_hook(img, d, t, sc):
    M = sc["M"]; kf = appear(t, 0.5, 0.5)
    if kf > 0:
        finger(d, CH, 0, X(5), 1, alpha=kf); finger(d, CH, 0, X(20), -1, alpha=kf)
    ruler(img, CH, 0)
    forces(d, CH, 0, X(5), X(20), lab="1,0 N", fing=False)
    dim(d, CH, X(5), X(20), CH[1] + HW + 200, "15 cm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Đẩy ở vạch 5 và vạch 20.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 300), "Thước quay quanh vạch nào?", 60, PURPLE, alpha=a)
    seg_bar(d, y0 + 440, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2, 3: Tien hanh ----------------
CD = (W / 2, 800)
R0, RD, PHI = 0.5, 5.6, 120.0
def phi_at(t): return PHI * ease((t - R0) / RD)

def spin(img, d, t, xa, xb, lab):
    phi = phi_at(t)
    d.rounded_rectangle([CD[0] - HL, CD[1] - HW, CD[0] + HL, CD[1] + HW], radius=10, outline=(205, 198, 184), width=4)
    for k in range(0, int(phi) + 1, 6):                      # vet hai dau thuoc
        for x in (-HL + 8, HL - 8):
            px, py = rot((x, 0), k, CD); dot(d, px, py, 6, (150, 155, 170))
    finger(d, CD, phi, xa, 1); finger(d, CD, phi, xb, -1)
    ruler(img, CD, phi)
    forces(d, CD, phi, xa, xb, lab=lab, fing=False)
    dot(d, CD[0], CD[1], 14, RED, WHITE)                    # vach 15 cm (trong tam) dung yen

def s_do1(img, d, t, sc):
    spin(img, d, t, X(0), X(30), "0,5 N")

def s_do2(img, d, t, sc):
    M = sc["M"]
    spin(img, d, t, X(5), X(20), "1,0 N")
    if t >= M[1] - 0.1: text(d, (W / 2, 1360), "vạch 15 đứng yên", 60, DGREEN)

# ---------------- canh 4: M = F.d + bang ----------------
def s_moment(img, d, t, sc):
    M = sc["M"]
    s = 0.92; c = (W / 2, 540)
    k = ease((t - M[1] - 0.2) / 0.8)                          # gia gan nhau hon: d 0,3 -> 0,15 m
    kF = appear(t, 1.4, 0.4)
    xf = lerp(X(30), (X(30)) / 2, k)
    text(d, (720, 300), "Mỗi lực F = 0,5 N" if kF < 0.5 else "Mỗi lực F = 1,0 N", 55, RED)
    ruler(img, c, 0, s)
    for x, side in ((-xf, 1), (xf, -1)):
        al = lerp(ALEN / 2, ALEN, kF)
        p1 = (c[0] + x * s, c[1] - side * HW * s); p2 = (c[0] + x * s, c[1] - side * (HW + al) * s)
        arrow(d, p1, p2, RED, w=7, head=26)
    yb = 790
    dim(d, (c[0], c[1]), -xf * s, xf * s, yb, "d = 0,3 m" if k < 0.999 else "d = 0,15 m")
    card(d, (300, 905, 780, 1000), fill=(239, 246, 255), r=26)
    text(d, (W / 2, 952), "M = F · d", 58, BLUE)
    card(d, (60, 1030, 1020, 1480), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 540, 850)
    for x, h in zip(xs, ("F (N)", "d (m)", "M (N·m)")): text(d, (x, 1090), h, 55, INK)
    d.line([(90, 1135), (990, 1135)], fill=LIGHT, width=4)
    for i, (f, dd, m) in enumerate(ROWS):
        at = 0.6 + i * 0.8 if i < 2 else M[1] + 1.0
        if t < at: continue
        y = 1195 + i * 92
        if i == 2: d.rounded_rectangle([85, y - 38, 995, y + 38], radius=16, fill=(225, 236, 255))
        for x, v, col in zip(xs, (vn(f), vn(dd, 2 if dd < 0.2 else 1), vn(m, 2 if m < 0.2 else 1)), (RED, NAVY, BLUE)):
            text(d, (x, y), v, 55, col)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[2] - 0.1, 0.4)
    if k3 < 1:
        a = 1 - k3
        card(d, (40, 270, 1040, 640), fill=A(WHITE, a), outline=A(DRED, a), w=6)
        pill(d, W / 2, 340, "BẪY", DRED, a)
        q = "M = F · (d/2)"; lw = tw(d, q, F(64)); yy = 480
        text(d, (W / 2, yy), q, 64, DRED, alpha=a)
        ks = clamp((t - M[0] - 1.2) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 10, yy + 2), (W / 2 - lw / 2 - 10 + (lw + 20) * ks, yy + 2)], fill=A(DRED, a), width=7)
    if k3 > 0:
        yk = 270 + (1 - k3) * 30
        card(d, (40, yk, 1040, yk + 370), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, yk + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, yk + 200), "Giữ cố định một điểm", 58, INK, alpha=k3)
        text(d, (W / 2, yk + 290), "của thước thì sao?", 58, INK, alpha=k3)
    s = 0.92; c = (W / 2, 900)
    ruler(img, c, 0, s)
    xf = X(30)
    for x, side in ((-xf, 1), (xf, -1)):
        p1 = (c[0] + x * s, c[1] - side * HW * s); p2 = (c[0] + x * s, c[1] - side * (HW + ALEN) * s)
        arrow(d, p1, p2, RED, w=7, head=26)
        text(d, (p2[0] + 50, (p1[1] + p2[1]) / 2), "F", 55, RED)
    dot(d, c[0], c[1], 12, RED, WHITE)
    b = appear(t, M[1] - 0.2, 0.45)
    if b <= 0: return
    yb = 1190
    for x0, x1 in ((-xf, 0), (0, xf)):
        X0, X1 = c[0] + x0 * s, c[0] + x1 * s
        for XX in (X0, X1):
            for yy in range(int(c[1] + HW * s + 8), yb - 10, 26): d.line([(XX, yy), (XX, yy + 12)], fill=A(GRAY, b), width=3)
        d.line([(X0 + 4, yb), (X1 - 4, yb)], fill=A(NAVY, b), width=5)
        for XX in (X0 + 4, X1 - 4): d.line([(XX, yb - 16), (XX, yb + 16)], fill=A(NAVY, b), width=5)
        text(d, ((X0 + X1) / 2, yb + 50), "d/2", 55, NAVY, alpha=b)
    text(d, (W / 2, 1380), "F · (d/2) + F · (d/2) = F · d", 58, DGREEN, alpha=b)

# ---------------- canh 6: Thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 290, 1040, 1500), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 360, "THỬ NGHĨ", ORANGE, k)
    c = (W / 2, 760)
    if k > 0.05:
        ruler(img, c, 0)
        forces(d, c, 0, X(5), X(25), lab="2,0 N", alpha=k, fing=False)
    text(d, (W / 2, 1060), "Đẩy ở vạch 5 và vạch 25.", 60, INK, alpha=k)
    text(d, (W / 2, 1160), "Moment ngẫu lực bao nhiêu?", 60, DORANGE, alpha=k)
    seg_bar(d, 1290, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, d1, d2, mo, b, e = sc["hook"], sc["do1"], sc["do2"], sc["moment"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (d1["t0"] + R0, "tap"),
            (d2["t0"] + R0, "tap"), (d2["t0"] + d2["M"][1] - 0.1, "ding"), (b["t0"] + b["M"][0] + 1.2, "buzz"),
            (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-moment-luc-03", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Moment lực · thachlab.id.vn", scenes=[
 dict(key="hook", title="Thước 30 cm trên bàn nhẵn", draw=s_hook, tail=0.2, caps=[
   ("Hai lực bằng nhau, ngược chiều.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do1", title="Đẩy hai đầu thước", draw=s_do1, tail=0.3, caps=[
   ("Thước quay, không trượt đi.", 3.2),
   ("Dấu chấm: vạch 15 cm.", 3.2)]),
 dict(key="do2", title="Đẩy ở vạch 5 và 20", draw=s_do2, tail=0.3, caps=[
   ("Hai giá cách nhau 15 cm.", 3.4),
   ("Đáp án: quanh vạch 15.", 3.2)]),
 dict(key="moment", title="Moment ngẫu lực", draw=s_moment, tail=0.3, caps=[
   ("d: khoảng cách hai giá.", 3.0),
   ("Giá gần nhau hơn, M nhỏ hơn.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Lấy nửa d: quên một lực.", 3.4),
   ("Mỗi lực cách tâm nửa d.", 3.4),
   ("Còn bỏ ngỏ.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])
