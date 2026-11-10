# Clip: tn-l10-moment-luc-03 - Ngau luc lam thuoc quay quanh trong tam (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-moment-luc-03.json:
#   thuoc 30 cm, trong tam o vach 15 cm; so_lieu_mau F (N) / d (m) / M (N.m): 0,5/0,3/0,15 ; 1,0/0,3/0,3 ; 1,0/0,15/0,15
#   tham_so: F 0,1-2 N, d 0,05-0,3 m. Cau chot dung F = 2 N (max tham_so), d = 0,3 m -> M = 0,6 N.m (chua hien tren man).
# Canh: Du doan (chi cau hoi + hinh, K10) -> Tien hanh (thuoc quay tai cho, vet hai dau la cung tron quanh vach 15)
#       -> Dap an C -> Vi sao chi quay (F - F = 0; vat tu do quay quanh trong tam) -> M = F.d + bang so lieu
#       -> Bay (M = F.d/2) -> Chua noi duoc gi (canh rieng) -> Chot + cau hoi tu nho lai.
from engine import *

ROWS = [("0,5", "0,3", "0,15"), ("1,0", "0,3", "0,3"), ("1,0", "0,15", "0,15")]   # so_lieu_mau
DRED = (185, 28, 28)            # chu canh Bay: do dam #B91C1C
WOOD = (247, 214, 120); WOOD_D = (176, 132, 40)
SKIN = (241, 200, 168); SKIN_D = (196, 140, 104)
PX_CM = 26                      # 30 cm -> 780 px
HL, HW = 390, 55                # nua dai, nua rong thuoc (px)
XF = 372                        # diem dat luc (sat hai dau), toa do doc thuoc
ALEN = 170                      # do dai vecto F (hai luc bang nhau -> cung do dai)

# ---------- thuoc ve san mot lan (co so cm), xoay bang PIL ----------
_RULER = {}
def ruler_img(s=1.0):
    if s in _RULER: return _RULER[s]
    pad = 6; w, h = int(2 * HL * s), int(2 * HW * s)
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([pad, pad, pad + w, pad + h], radius=int(10 * s), fill=WOOD + (255,), outline=WOOD_D + (255,), width=max(2, int(4 * s)))
    for c in range(31):
        x = pad + int(HL * s + (c - 15) * PX_CM * s * 0.95)
        L = (34 if c % 5 == 0 else 18) * s
        dd.line([(x, pad), (x, pad + L)], fill=NAVY + (255,), width=max(2, int(3 * s)))
        if c % 5 == 0 and s >= 0.99:
            dd.text((x, pad + h - 30), str(c), font=F(40), fill=NAVY + (255,), anchor="mm")
    _RULER[s] = im; return im

def rot(p, phi, c):
    """Quay diem p (toa do doc thuoc) mot goc phi (do, cung chieu kim dong ho tren man hinh) roi doi goc ve c."""
    a = math.radians(phi); x, y = p
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))

def finger(d, cx, cy, phi, side, s=1.0, alpha=1.0):
    """Ngon tay day vao canh thuoc. side=+1: ngon o phia duoi (day len), -1: o phia tren (day xuong)."""
    x = side * -XF * s; y0 = side * HW * s; y1 = side * (HW + 150) * s; r = 30 * s
    pts = [rot(p, phi, (cx, cy)) for p in ((x - r, y0 + side * r), (x + r, y0 + side * r), (x + r, y1), (x - r, y1))]
    d.polygon(pts, fill=A(SKIN, alpha), outline=A(SKIN_D, alpha))
    tx, ty = rot((x, y0 + side * r), phi, (cx, cy))
    d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=A(SKIN, alpha))

def forces(d, cx, cy, phi, s=1.0, alpha=1.0, lbl=True, xf=XF, alen=ALEN):
    """Hai luc song song, nguoc chieu, cung do dai: dau trai day len, dau phai day xuong (vecto ngoai than thuoc)."""
    for side in (1, -1):
        x = -side * xf * s
        p1 = rot((x, -side * HW * s), phi, (cx, cy)); p2 = rot((x, -side * (HW + alen) * s), phi, (cx, cy))
        arrow(d, p1, p2, A(RED, alpha), w=max(5, int(8 * s)), head=int(30 * s))
        if lbl:
            lp = rot((x - side * 52 * s, -side * (HW + alen * 0.62) * s), phi, (cx, cy))
            text(d, lp, "F", int(48 * max(s, 0.85)), RED, alpha=alpha)

def ruler(img, d, cx, cy, phi, s=1.0):
    r = ruler_img(s).rotate(-phi, resample=Image.BICUBIC, expand=True)
    img.paste(r, (int(cx - r.width / 2), int(cy - r.height / 2)), r)

def ghost(d, cx, cy, s=1.0):
    d.rounded_rectangle([cx - HL * s, cy - HW * s, cx + HL * s, cy + HW * s], radius=10, outline=(205, 198, 184), width=4)

# ---------------- canh 1: du doan ----------------
YH = 540
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; kf = appear(t, 0.6, 0.5)
    if kf > 0:
        finger(d, W / 2, YH, 0, 1, alpha=kf); finger(d, W / 2, YH, 0, -1, alpha=kf)
    ruler(img, d, W / 2, YH, 0)
    if kf > 0: forces(d, W / 2, YH, 0, alpha=kf)
    text(d, (W / 2, 860), "Thước 30 cm trên mặt bàn nhẵn", 40, MUTED, alpha=appear(t, 0.3))
    k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 940 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 600), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 170, "Đẩy như hình.", 46, INK, alpha=k)
    ctext(d, y0 + 240, "Thước chuyển động thế nào?", 46, INK, alpha=k)
    card(d, (W / 2 - 80, y0 + 310, W / 2 + 80, y0 + 470), fill=A((245, 243, 255), k), outline=A(PURPLE, k), r=26, w=4)
    text(d, (W / 2, y0 + 390), "?", 90, PURPLE, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))      # thanh dem thoi gian nghi
    d.rounded_rectangle([200, y0 + 540, 880, y0 + 556], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 540, 200 + 680 * (1 - q), y0 + 556], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
YD = 720
ROT0, ROTD, PHI = 0.5, 5.8, 150.0
def phi_at(t): return PHI * ease((t - ROT0) / ROTD)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; phi = phi_at(t); c = (W / 2, YD)
    ghost(d, c[0], c[1])
    # vet hai dau thuoc: cung tron quanh vach 15 cm
    for k in range(0, int(phi) + 1, 6):
        for x in (-HL + 8, HL - 8):
            px, py = rot((x, 0), k, c); dot(d, px, py, 6, (150, 155, 170))
    finger(d, c[0], c[1], phi, 1); finger(d, c[0], c[1], phi, -1)
    ruler(img, d, c[0], c[1], phi)
    forces(d, c[0], c[1], phi)
    dot(d, c[0], c[1], 13, RED, WHITE)                       # tam: vach 15 cm, dung yen suot luc quay
    kc = appear(t, M[1], 0.4)
    if kc > 0:
        card(d, (300, 1300, 780, 1420), fill=A((220, 252, 231), kc), outline=A(GREEN, kc), r=26, w=4)
        text(d, (W / 2, 1360), "Đáp án C", 48, GREEN, alpha=kc)

# ---------------- canh 3: vi sao chi quay ----------------
def s_vi_sao(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 270, 1020, 800), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    s = 0.8; c = (W / 2, 500)
    ruler(img, d, c[0], c[1], 0, s); forces(d, c[0], c[1], 0, s, alpha=a)
    text(d, (W / 2, 735), "F − F = 0", 66, NAVY, alpha=appear(t, 0.5))
    b = appear(t, 2.2, 0.45)
    if b <= 0: return
    card(d, (60, 840, 1020, 1580), fill=A(WHITE, b), outline=A(GREEN, b), w=4)
    s = 0.7; c2 = (W / 2, 1170); phi = 40 * ease((t - 2.4) / 2.6)
    ghost(d, c2[0], c2[1], s)
    ruler(img, d, c2[0], c2[1], phi, s); forces(d, c2[0], c2[1], phi, s, alpha=b, lbl=False)
    dot(d, c2[0], c2[1], 15, RED, WHITE)
    text(d, (W / 2, 1520), "trọng tâm · vạch 15 cm", 46, INK, alpha=b)

# ---------------- canh 4: M = F.d + bang ----------------
def s_moment(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 270, 1020, 900), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    s = 0.92; c = (W / 2, 540)
    k = ease((t - M[1] - 0.2) / 0.8)                          # day gan nhau hon: d 0,3 -> 0,15 m
    xf = lerp(XF, XF / 2, k)
    kF = appear(t, 1.4, 0.4)                                # hang 2 (F = 1,0 N) hien: vecto dai gap doi hang 1 (0,5 N)
    alen = lerp(ALEN / 2, ALEN, kF)
    text(d, (W / 2, 318), "Mỗi lực F = 0,5 N" if kF < 0.5 else "Mỗi lực F = 1,0 N", 44, RED)
    ruler(img, d, c[0], c[1], 0, s); forces(d, c[0], c[1], 0, s, xf=xf, alen=alen)
    for x in (-xf, xf):                                     # gia cua hai luc (net dut)
        X = c[0] + x * s
        for yy in range(360, 770, 30): d.line([(X, yy), (X, yy + 16)], fill=GRAY, width=3)
    yb = 800; xl, xr = c[0] - xf * s, c[0] + xf * s
    d.line([(xl, yb), (xr, yb)], fill=NAVY, width=4)
    for X in (xl, xr): d.line([(X, yb - 16), (X, yb + 16)], fill=NAVY, width=4)
    text(d, (W / 2, yb + 50), "d = 0,3 m (30 cm)" if k < 0.5 else "d = 0,15 m (15 cm)", 44, NAVY)
    card(d, (300, 925, 780, 1025), fill=A((239, 246, 255), a), r=26)
    text(d, (W / 2, 975), "M = F · d", 54, BLUE, alpha=a)
    card(d, (60, 1050, 1020, 1490), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 540, 850)
    for x, h in zip(xs, ("F (N)", "d (m)", "M (N·m)")): text(d, (x, 1105), h, 42, INK)
    d.line([(90, 1145), (990, 1145)], fill=LIGHT, width=4)
    for i, row in enumerate(ROWS):
        ra = appear(t, 0.6 + i * 0.8, 0.35); y = 1205 + i * 92
        if ra <= 0: continue
        if i >= 1 and t >= M[1]:
            d.rounded_rectangle([85, y - 38, 995, y + 38], radius=16, fill=A((225, 236, 255), appear(t, M[1], 0.3)))
        for x, v, col in zip(xs, row, (RED, NAVY, BLUE)): text(d, (x, y), v, 46, col, alpha=ra)

# ---------------- canh 5: bay (dung rieng) ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 270, 1020, 760), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 364), fill=A(DRED, a), r=32)
    text(d, (W / 2, 332), "Bẫy", 40, WHITE, alpha=a)
    q = "M = F·(d/2)"; f = F(62); lw = tw(d, q, f); yy = 480
    text(d, (W / 2, yy), q, 62, DRED, alpha=a)
    ks = clamp((t - 1.2) / 0.4)
    if ks > 0: d.line([(W / 2 - lw / 2 - 10, yy + 2), (W / 2 - lw / 2 - 10 + (lw + 20) * ks, yy + 2)], fill=DRED, width=7)
    b = appear(t, M[1] - 0.2, 0.45)
    if b <= 0: return
    card(d, (60, 800, 1020, 1560), fill=A(WHITE, b), outline=A(GREEN, b), w=5)
    s = 0.92; c = (W / 2, 1060)
    ruler(img, d, c[0], c[1], 0, s); forces(d, c[0], c[1], 0, s, alpha=b, lbl=False)
    dot(d, c[0], c[1], 12, RED, WHITE)
    yb = 1320                                               # hai ngoac do cung phia duoi, ngoai than thuoc va ngoai vecto
    for X in (c[0] - XF * s, c[0], c[0] + XF * s):          # duong gióng net dut tu thuoc xuong ngoac
        for yy in range(int(c[1] + HW * s + 8), yb - 10, 26): d.line([(X, yy), (X, yy + 12)], fill=A(GRAY, b), width=3)
    for x0, x1 in ((-XF, 0), (0, XF)):
        X0, X1 = c[0] + x0 * s, c[0] + x1 * s
        d.line([(X0 + 4, yb), (X1 - 4, yb)], fill=A(NAVY, b), width=5)
        for X in (X0 + 4, X1 - 4): d.line([(X, yb - 16), (X, yb + 16)], fill=A(NAVY, b), width=5)
        text(d, ((X0 + X1) / 2, yb + 50), "d/2", 48, NAVY, alpha=b)
    text(d, (W / 2, 1480), "F·(d/2) + F·(d/2) = F·d", 50, GREEN, alpha=appear(t, M[1] + 0.6, 0.45))

# ---------------- canh 6: chua noi duoc gi (canh rieng) ----------------
def s_gioihan(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.05, 0.35); y1 = 290
    card(d, (60, y1, 1020, y1 + 1260), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, y1 + 85), "Chưa nói được gì?", 54, NAVY, alpha=k)
    card(d, (110, y1 + 170, 970, y1 + 580), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 250, "Chỉ thử thước tự do.", 50, INK, alpha=k)
    ctext(d, y1 + 375, "Chưa thử giữ cố định", 50, BLUE, alpha=k)
    ctext(d, y1 + 470, "một điểm của thước", 50, BLUE, alpha=k)
    s = 0.85; c = (W / 2, y1 + 840)                         # thuoc co mot diem bi giu (dinh xam) + dau hoi
    ruler(img, d, c[0], c[1], 0, s)
    px = c[0] - 300 * s
    dot(d, px, c[1], 20, (120, 125, 140), WHITE)
    d.line([(px - 11, c[1]), (px + 11, c[1])], fill=WHITE, width=4); d.line([(px, c[1] - 11), (px, c[1] + 11)], fill=WHITE, width=4)
    text(d, (W / 2, y1 + 1080), "?", 110, PURPLE, alpha=k)

# ---------------- canh 7: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def hint(d, t, k):                        # tu ve cau hoi (to hon) + goi y chu toi >= 40 px, goi y hien tre ~2,5 s
        ctext(d, 900, "Mỗi lực 2 N ở hai đầu\nthước 30 cm: moment bao nhiêu?", 56, INK,
              maxw=860, alpha=appear(t, sc["M"][0] + 0.4, 0.5))
        kh = appear(t, sc["M"][0] + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 1230, 970, 1530), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=3)
        ctext(d, 1300, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1420, "Đổi cm ra m trước khi tính", 48, (154, 52, 18), maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Ngẫu lực chỉ làm quay", "", body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + do["M"][1], "ding"), (b["t0"] + 1.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-moment-luc-03", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Moment lực · thachlab.id.vn", scenes=[
 dict(key="hook", title="Đẩy hai đầu thước", draw=s_hook, tail=0.6, caps=[
   ("Hai lực ngược chiều, bằng nhau.", 3.4),
   ("Dừng video, tự đoán.", 5.0)]),
 dict(key="do", title="Đẩy và quan sát", draw=s_do, tail=0.5, caps=[
   ("Thước quay tại chỗ, không trượt đi.", 3.6),
   ("Vạch 15 cm đứng yên.", 3.0)]),
 dict(key="visao", title="Vì sao chỉ quay?", draw=s_vi_sao, tail=0.5, caps=[
   ("Tổng lực bằng 0: không trượt.", 4.6)]),
 dict(key="moment", title="Moment ngẫu lực", draw=s_moment, tail=0.5, caps=[
   ("d: khoảng cách hai giá.", 2.6),
   ("Giá gần nhau hơn, M nhỏ hơn.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.5, caps=[
   ("Lấy nửa d: quên một lực.", 3.0),
   ("Mỗi lực cách tâm nửa d.", 3.0)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.5, caps=[
   ("Giới hạn của thí nghiệm.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])
