# Clip: tn-l9-thaukinh-02 - Hung anh cua so len to giay bang kinh lup (KHTN 9, lo 5, 18/11/2026)
# So lieu tu content/thi-nghiem/tn-l9-thaukinh-02.json:
#   tham_so: f = 10 cm, d mac dinh 400 cm ; so_lieu_mau: d = 400 cm -> d' = 10,26 cm (lam tron hien 10,3 cm)
#   Cau chot THU NGHI dung hang d = 200 cm -> d' = 10,53 cm (giay ra xa kinh hon), so 2 m va 10,5 chua tung hien.
# Hinh: phan kinh - giay ve dung ti le 40 px/cm (f = 400 px, d' = 410,4 px). Cua so o xa ve sau dau ngat truc.
#   Tia tu dinh cua so toi gan song song (vat rat xa), cung do nghieng voi tia qua quang tam O (di thang) ->
#   hoi tu tai B' tren mat phang anh (d'); giay chua dung cho: chum tia cat giay thanh vet -> anh nhoe.
#   Anh that, nguoc chieu: day cua so tren truc chinh -> day anh tren truc, dinh vom cua so -> xuong duoi truc.
# Cau hoi ngay sau hop trong bai (Cau 3: f = 8, d = 12 -> d') va Cau 7 (h' khi d = 30): clip khong tinh d' bang
#   cong thuc, khong noi xu huong "vat cang xa anh cang sat F'" (de clip thaukinh-03 va cau chot con viec de nghi).
# Canh: Du doan (K10) -> Tien hanh (dich giay toi lui, khung "nhin tren to giay" nhoe/ro) -> Dap an + Rut ra
#       -> Bay (anh la bong cua kinh) roi Chua noi duoc -> Chot + THU NGHI (2 m thay 4 m).
from engine import *
from PIL import ImageFilter

AX, LX, LH = 560, 430, 150                  # truc chinh, thau kinh, nua chieu cao kinh
PXCM = 40                                   # 40 px / cm o phan kinh - giay
F_CM, D_CM, DP_CM = 10.0, 400.0, 10.26      # kho: f, d, d'
X_IMG = LX + DP_CM * PXCM                   # mat phang anh ro
X_F = LX + F_CM * PXCM                      # F'
HI = 60                                     # chieu cao anh tren giay (px)
SLOPE = HI / (X_IMG - LX)                   # do nghieng chum tia toi (qua O di thang toi B')
BRK = 262                                   # cho ngat truc
RAYS_Y = (-128, 0, 112)                     # do cao cac tia khi toi kinh
DRED = (185, 28, 28); DGREEN = (21, 110, 55); LBLUE = (147, 197, 253); BROWN = (120, 72, 30)
SKY = (186, 222, 250); FRAME = (60, 70, 110)
DP_TXT = "10,3 cm"                          # 10,26 lam tron 1 chu so (buoc cuoi)


def chev(d, p, q, col, s=16, w=4):
    x, y = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2; ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=col, width=w)


def window_pic(h, inv=False, blur=0.0, bg=WHITE):
    """anh cua so co vom tron phia tren (de nhan ra lon nguoc); tra ve anh RGB vuong canh ~1,35h"""
    S = int(h * 1.35) + 2 * int(blur * 2 + 4); im = Image.new("RGB", (S, S), bg); g = ImageDraw.Draw(im)
    w = h * 0.62; cx, by = S / 2, S / 2 + h / 2; r = w / 2
    top = by - h + r
    g.rectangle([cx - r, top, cx + r, by], fill=SKY, outline=FRAME, width=max(3, int(h / 30)))
    g.pieslice([cx - r, top - r, cx + r, top + r], 180, 360, fill=SKY, outline=FRAME, width=max(3, int(h / 30)))
    g.line([(cx, top - r), (cx, by)], fill=FRAME, width=max(3, int(h / 28)))
    g.line([(cx - r, top + (by - top) * 0.45), (cx + r, top + (by - top) * 0.45)], fill=FRAME, width=max(3, int(h / 28)))
    g.rectangle([cx - r - h * 0.06, by, cx + r + h * 0.06, by + h * 0.05], fill=FRAME)      # bau cua so
    if inv: im = im.rotate(180)
    if blur > 0.4: im = im.filter(ImageFilter.GaussianBlur(blur))
    return im


def paste_pic(img, pic, cx, cy, alpha=1.0):
    if alpha <= 0.02: return
    m = Image.new("L", pic.size, int(255 * clamp(alpha)))
    img.paste(pic, (int(cx - pic.size[0] / 2), int(cy - pic.size[1] / 2)), m)


def lens(d, a=1.0):
    pts = []
    for j in range(41):
        y = -LH + 2 * LH * j / 40; pts.append((LX + 3 + 14 * (1 - (y / LH) ** 2), AX + y))
    for j in range(41):
        y = LH - 2 * LH * j / 40; pts.append((LX - 3 - 14 * (1 - (y / LH) ** 2), AX + y))
    d.rounded_rectangle([LX - 9, AX + LH - 4, LX + 9, AX + LH + 105], radius=6, fill=A(BROWN, a))   # can kinh lup
    d.polygon(pts, fill=A(LBLUE, 0.75 * a), outline=A(BLUE, a))


def blur_px(xp):
    """do loe (px) cua chum tia tu dinh cua so tren mat giay"""
    return (RAYS_Y[2] - RAYS_Y[0]) * abs(xp - X_IMG) / (X_IMG - LX)


def scene(img, d, xp, rays=1.0, dim=False, hint_f=True, labels=True):
    """mat cat: cua so o xa | ngat truc | kinh lup | giay o xp"""
    d.line([(40, AX), (BRK - 14, AX)], fill=A(NAVY, 0.6), width=3)
    d.line([(BRK + 14, AX), (1060, AX)], fill=A(NAVY, 0.6), width=3)
    for dx in (-10, 10):
        d.line([(BRK + dx - 9, AX + 22), (BRK + dx + 9, AX - 22)], fill=NAVY, width=4)
    paste_pic(img, window_pic(170, bg=BG), 135, AX - 170 / 2 - 6)
    if labels:
        text(d, (135, AX - 236), "cửa sổ", 40, INK)
        text(d, (BRK, AX + 66), "cách 4 m", 40, NAVY)
    lens(d)
    if labels: text(d, (LX, AX + LH + 150), "kính lúp, f = 10 cm", 40, BLUE)
    if hint_f:
        dot(d, X_F, AX, 8, NAVY); text(d, (X_F - 30, AX - 36), "F'", 40, NAVY)
    Bp = (X_IMG, AX + HI)
    if rays > 0:
        c = A(ORANGE, 0.9 * rays)
        for yi in RAYS_Y:
            y_in = AX + yi; p0 = (BRK + 24, y_in - SLOPE * (LX - BRK - 24))
            d.line([p0, (LX, y_in)], fill=c, width=4); chev(d, p0, (LX, y_in), c)
            k = (xp - LX) / (Bp[0] - LX)                                    # dung tia o mat giay
            q = (xp, y_in + (Bp[1] - y_in) * k)
            d.line([(LX, y_in), q], fill=c, width=4)
    b = blur_px(xp)
    if rays > 0:                                                           # vet sang tren giay (nhin ngang)
        if b < 3: d.rectangle([xp - 5, AX, xp + 5, AX + HI], fill=BLUE)
        else: d.rectangle([xp - 5, AX - b / 2, xp + 5, AX + HI + b / 2], fill=A(BLUE, max(0.25, 0.9 - b / 120)))
    d.rounded_rectangle([xp - 7, AX - 185, xp + 7, AX + 185], radius=4, fill=WHITE, outline=NAVY, width=3)
    if rays > 0:
        if b < 3: d.rectangle([xp - 7, AX, xp - 2, AX + HI], fill=BLUE)
    if labels: text(d, (xp + 10, AX - 222), "tờ giấy", 40, NAVY)
    if dim:
        y = AX + LH + 40
        d.line([(LX, y), (xp, y)], fill=DGREEN, width=4)
        for x in (LX, xp): d.line([(x, y - 12), (x, y + 12)], fill=DGREEN, width=4)
        text(d, ((LX + xp) / 2 + 30, y + 38), DP_TXT, 42, DGREEN)


def paper_view(img, d, b, y0=930, a=1.0):
    """khung nhin thang vao to giay"""
    card(d, (230, y0, 850, y0 + 470), fill=A(WHITE, a), outline=A(LIGHT, a), w=4)
    text(d, (540, y0 + 46), "nhìn trên tờ giấy", 40, MUTED, bold=False, alpha=a)
    paste_pic(img, window_pic(150, inv=True, blur=min(26, b * 0.35)), 540, y0 + 240, a)
    sharp = b < 3
    text(d, (540, y0 + 425), "rõ nét" if sharp else "nhoè", 44, DGREEN if sharp else ORANGE, alpha=a)
    return sharp


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    scene(img, d, 1000, rays=0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 920 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 610), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 255, "Hình cửa sổ rõ nét trên giấy\nso với cửa sổ thật thế nào?",
          50, INK, maxw=920, alpha=a)
    text(d, (W / 2, y0 + 470), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 548, 940, y0 + 560], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 548, 140 + 800 * (1 - p), y0 + 560], radius=6, fill=A(PURPLE, a))


# ---------------- canh 2: Tien hanh ----------------
MOVES = [(2.2, 4.4, 660.0), (5.0, 6.6, X_IMG)]     # (bat dau, ket thuc, x giay toi)
T_DIM = 6.9                                       # hien khoang kinh - giay sau khi giay dung han


def paper_x(t):
    x = 1000.0
    for a, b, to in MOVES:
        if t >= a: x = lerp(x, to, ease((t - a) / (b - a)))
    return x


def do_state(t):
    xp = paper_x(t); b = blur_px(xp)
    return dict(xp=xp, sharp=b < 3, dim=t >= T_DIM, stopped=t >= MOVES[-1][1])


def s_do(img, d, t, sc):
    st = do_state(t)
    scene(img, d, st["xp"], rays=appear(t, 0.3, 0.6), dim=False)
    if st["dim"]:
        k = appear(t, T_DIM, 0.4); y = AX + LH + 40
        d.line([(LX, y), (st["xp"], y)], fill=A(DGREEN, k), width=4)
        for x in (LX, st["xp"]): d.line([(x, y - 12), (x, y + 12)], fill=A(DGREEN, k), width=4)
        text(d, ((LX + st["xp"]) / 2 + 30, y + 38), DP_TXT, 42, DGREEN, alpha=k)
    paper_view(img, d, blur_px(st["xp"]), a=appear(t, 0.5, 0.5))


# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · nhỏ hơn, lộn ngược"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 226, W / 2 + pw / 2, 292), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 259), lab, 42, WHITE, alpha=ka)
    scene(img, d, X_IMG, rays=0.5, dim=True, labels=False)
    k1 = appear(t, M[0] + 0.3, 0.4)
    if k1 > 0:
        card(d, (60, 930, 1020, 1250), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
        paste_pic(img, window_pic(200), 300, 1080, k1)
        text(d, (300, 1205), "cửa sổ", 40, INK, alpha=k1)
        arrow(d, (480, 1080), (600, 1080), A(NAVY, k1), w=5, head=20)
        paste_pic(img, window_pic(80, inv=True), 780, 1080, k1)
        text(d, (780, 1205), "ảnh", 40, BLUE, alpha=k1)
    k2 = appear(t, M[1] + 0.2, 0.4)
    if k2 > 0:
        card(d, (60, 1280, 1020, 1480), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=22, w=3)
        text(d, (W / 2, 1340), "Ảnh thật, hứng được", 44, DGREEN, alpha=k2)
        text(d, (W / 2, 1415), "10,3 cm ≈ f", 44, INK, alpha=k2)


# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    scene(img, d, X_IMG, rays=0.35, dim=False, labels=False)
    if a1 > 0:
        k3 = a1 * appear(t, 0.5, 0.5); k4 = a1 * appear(t, M[0] + 2.3, 0.5)    # sai: cung luc chu ; dung: tre
        y0 = 930
        card(d, (40, y0, 1040, lerp(y0 + 330, y0 + 560, k4 / max(a1, 1e-3))), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        if k3 > 0:                                                         # vet tron mo = "bong kinh"
            d.ellipse([110, y0 + 140, 270, y0 + 300], fill=A((200, 200, 205), k3), outline=A(GRAY, k3), width=4)
        text(d, (300, y0 + 190), "Hình là bóng", 48, DRED, anchor="lm", alpha=k3)
        text(d, (300, y0 + 255), "của kính lúp", 48, DRED, anchor="lm", alpha=k3)
        if k3 > 0:
            for yy, s1 in ((y0 + 192, "Hình là bóng"), (y0 + 257, "của kính lúp")):
                d.line([(296, yy), (304 + tw(d, s1, F(48)), yy)], fill=A(DRED, k3), width=5)
        text(d, (900, y0 + 222), "✗", 100, DRED, alpha=k3)
        if k4 > 0: paste_pic(img, window_pic(130, inv=True), 190, y0 + 445, k4)
        text(d, (300, y0 + 410), "Là ảnh: có", 48, DGREEN, anchor="lm", alpha=k4)
        text(d, (300, y0 + 475), "khung, lộn ngược", 48, DGREEN, anchor="lm", alpha=k4)
        text(d, (900, y0 + 440), "✓", 100, DGREEN, alpha=k4)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 320), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Số liệu minh hoạ", "• Mới thử cửa sổ cách 4 m")):
            kk = k2 * appear(t, M[1] + 0.1 + 0.3 * j, 0.4)
            text(d, (90, y0 + 165 + j * 95), l1, 44, INK, anchor="lm", alpha=kk)


# ---------------- canh 5: Chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    """Chot -> THU NGHI: cach cua so 2 m (thay 4 m), giay dich lai gan hay ra xa kinh? (ra xa, d' = 10,53 cm)."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 490, 1020, 790), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 640, "Vật rất xa: ảnh thật,\nnhỏ, ngược, gần F'", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 0.9 + 2.6, 0.5)
    card(d, (40, 850, 1040, lerp(1270, 1570, kh)), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 880, W / 2 + pw / 2, 944), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 912), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 1110, "Cách cửa sổ 2 m (so với\nlúc 4 m): giấy dịch lại gần\nhay ra xa kính?",
          48, INK, maxw=920, alpha=appear(t, M[0] + 0.9, 0.5))
    if kh > 0:
        card(d, (110, 1290, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1345, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1445, "Kính lúp giữ nguyên", 46, ORANGE, maxw=820, alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + MOVES[-1][1], "tap"), (da["t0"] + 0.1, "ding"), (b["t0"] + 0.5, "buzz"),
            (e["t0"] + e["M"][0] + 0.6, "open")]


CLIP = dict(id="tn-l9-thaukinh-02", header="KHTN 9 · THÍ NGHIỆM", footer="Thấu kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hứng ảnh cửa sổ", draw=s_hook, tail=0.8, caps=[
   ("Kính lúp hướng về cửa sổ.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Dịch giấy tới lui sau kính.", 5.2),
   ("Hình rõ thì đo kính tới giấy.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Tia ló gặp nhau ngay trên giấy.", 4.2),
   ("Giấy ở gần tiêu điểm F'.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.8, caps=[
   ("Đó chỉ là bóng của kính?", 3.8),
   ("Chưa nói được điều gì?", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.3, caps=[
   ("Dừng video, tự trả lời.", 6.8)]),
])
