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
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom D): chu >= 55 (ra >= 48 px). Du doan DOI: bang tinh chat anh
#   (d > 2f: that, nguoc, nho) dung ngay truoc hop nen khong hoi tinh chat; hoi GIAY CACH KINH BAO NHIEU thi ro
#   (dap an: gan f, khoang 10 cm; hook an diem F'). Chot = ca kho: 2 m thay 4 m -> 10,53 cm (khoang 10,5 cm).
# Canh cu: Du doan (K10) -> Tien hanh (dich giay toi lui, khung "nhin tren to giay" nhoe/ro) -> Dap an + Rut ra
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
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORG = (176, 64, 8); LBLUE = (147, 197, 253); BROWN = (120, 72, 30)
SKY = (186, 222, 250); FRAME = (60, 70, 110)
DP_TXT = "10,3 cm"
FS, FM = 58, 56
DP2_CM = 10.53                              # kho: d = 200 cm


def _kiem():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-thaukinh-02.json")))
    tp = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert tp["f"]["gia_tri"] == F_CM and tp["d"]["mac_dinh"] == D_CM
    h = {r[0]: r[1] for r in k["so_lieu_mau"]["hang"]}
    assert h[400] == DP_CM and h[200] == DP2_CM
    for d_, dp in h.items(): assert abs(1 / F_CM - 1 / d_ - 1 / dp) < 1e-4
_kiem()                          # 10,26 lam tron 1 chu so (buoc cuoi)


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
        text(d, (135, AX - 236), "cửa sổ", FM, INK)
        text(d, (BRK - 20, AX + 70), "cách 4 m", FM, NAVY)
    lens(d)
    if labels: text(d, (LX, AX + LH + 150), "f = 10 cm", FM, BLUE)
    if hint_f:
        dot(d, X_F, AX, 9, NAVY); text(d, (X_F - 34, AX - 40), "F'", FM, NAVY)
    Bp = (X_IMG, AX + HI)
    if rays > 0:
        c = A(ORANGE, 0.9 * rays)
        for yi in RAYS_Y:
            y_in = AX + yi; p0 = (BRK + 24, y_in - SLOPE * (LX - BRK - 24))
            d.line([p0, (LX, y_in)], fill=c, width=5); chev(d, p0, (LX, y_in), c)
            k = (xp - LX) / (Bp[0] - LX)
            q = (xp, y_in + (Bp[1] - y_in) * k)
            d.line([(LX, y_in), q], fill=c, width=5)
    b = blur_px(xp)
    if rays > 0:
        if b < 3: d.rectangle([xp - 5, AX, xp + 5, AX + HI], fill=BLUE)
        else: d.rectangle([xp - 5, AX - b / 2, xp + 5, AX + HI + b / 2], fill=A(BLUE, max(0.25, 0.9 - b / 120)))
    d.rounded_rectangle([xp - 7, AX - 185, xp + 7, AX + 185], radius=4, fill=WHITE, outline=NAVY, width=3)
    if rays > 0 and b < 3: d.rectangle([xp - 7, AX, xp - 2, AX + HI], fill=BLUE)
    if labels: text(d, (min(xp, 960), AX - 226), "tờ giấy", FM, NAVY)
    if dim: dim_line(d, xp)


def dim_line(d, xp, k=1.0, txt=DP_TXT):
    y = AX + LH + 40
    d.line([(LX, y), (xp, y)], fill=A(DGREEN, k), width=5)
    for x in (LX, xp): d.line([(x, y - 14), (x, y + 14)], fill=A(DGREEN, k), width=5)
    text(d, ((LX + xp) / 2 + 40, y + 44), txt, FS, DGREEN, alpha=k)


def paper_view(img, d, b, y0=960, a=1.0):
    """khung nhin thang vao to giay"""
    card(d, (200, y0, 880, y0 + 520), fill=A(WHITE, a), outline=A(LIGHT, a), w=4)
    text(d, (540, y0 + 52), "nhìn trên tờ giấy", FM, (80, 86, 105), alpha=a)
    paste_pic(img, window_pic(170, inv=True, blur=min(26, b * 0.35)), 540, y0 + 265, a)
    sharp = b < 3
    text(d, (540, y0 + 465), "rõ nét" if sharp else "nhoè", FS, DGREEN if sharp else DORG, alpha=a)
    return sharp


def pill(d, s, y, a, color=NAVY, size=FM):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh; an F') ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    scene(img, d, 1000, rays=0, hint_f=False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(NAVY, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FM)) + 56
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 96), fill=A(NAVY, a), r=36)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", FM, WHITE, alpha=a)
    for j, s in enumerate(("Giấy cách kính bao nhiêu", "thì hình cửa sổ", "rõ nét?")):
        text(d, (W / 2, y0 + 165 + j * 80), s, 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 440, 970, y0 + 510], radius=35, fill=A((226, 232, 240), a))
        if p < 1: d.rounded_rectangle([110, y0 + 440, 110 + max(70, 860 * (1 - p)), y0 + 510], radius=35, fill=A(NAVY, a))


# ---------------- canh 2: Tien hanh ----------------
MOVES = [(1.4, 3.4, 660.0), (4.0, 5.8, X_IMG)]     # (bat dau, ket thuc, x giay toi)
T_DIM = 8.3                                       # khoang kinh - giay: >= 2,5 s sau chu "ro net"


def paper_x(t):
    x = 1000.0
    for a, b, to in MOVES:
        if t >= a: x = lerp(x, to, ease((t - a) / (b - a)))
    return x


def s_do(img, d, t, sc):
    xp = paper_x(t)
    scene(img, d, xp, rays=appear(t, 0.3, 0.6), hint_f=False)
    if t >= T_DIM: dim_line(d, xp, appear(t, T_DIM, 0.4))
    paper_view(img, d, blur_px(xp))


# ---------------- canh 3: Dap an + rut ra ----------------
DA_C, DA_R = 2.6, 5.2
def s_dapan(img, d, t, sc):
    scene(img, d, X_IMG, rays=appear(t, 0.3, 1.2), labels=False)
    pill(d, "ĐÁP ÁN: khoảng 10 cm, gần F'", 260, appear(t, 0.15, 0.4))
    k1 = appear(t, DA_C, 0.5)
    if k1 > 0:
        dim_line(d, X_IMG, k1)
        card(d, (60, 900, 1020, 1210), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
        paste_pic(img, window_pic(170), 290, 1030, k1)
        text(d, (290, 1178), "cửa sổ", FM, INK, alpha=k1)
        arrow(d, (480, 1040), (600, 1040), A(NAVY, k1), w=6, head=22)
        paste_pic(img, window_pic(80, inv=True), 790, 1040, k1)
        text(d, (790, 1170), "ảnh", FM, BLUE, alpha=k1)
    k2 = appear(t, DA_R, 0.5)
    if k2 > 0:
        rr = 22 + 14 * math.sin(2.6 * (t - DA_R)) ** 2           # diem anh B' nhap nhay: tia gap nhau that
        d.ellipse([X_IMG - rr, AX + HI - rr, X_IMG + rr, AX + HI + rr], fill=A(ORANGE, 0.7 * k2))
        card(d, (60, 1250, 1020, 1480), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=26, w=4)
        text(d, (W / 2, 1320), "Ảnh thật: nhỏ, lộn ngược", FS, DGREEN, alpha=k2)
        text(d, (W / 2, 1410), "nằm gần tiêu điểm F'", FS, DGREEN, alpha=k2)


# ---------------- canh 4: Bay + chua noi duoc ----------------
BAY_R, BAY_E = 3.4, 6.6
def s_bay(img, d, t, sc):
    scene(img, d, X_IMG, rays=0.35, labels=False)
    a1 = appear(t, 0.3, 0.45)
    if a1 > 0:
        pill(d, "BẪY", 880, a1, color=DRED)
        card(d, (40, 935, 1040, 1140), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
        d.ellipse([90, 960, 250, 1120], fill=A((200, 200, 205), a1), outline=A(GRAY, a1), width=4)   # vet tron mo
        text(d, (290, 1000), "“Bóng của kính”", FS, DRED, anchor="lm", alpha=a1)
        text(d, (290, 1080), "vệt tròn, không hình", FM, INK, anchor="lm", alpha=a1)
        text(d, (960, 1040), "✗", 80, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (40, 1160, 1040, 1350), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        paste_pic(img, window_pic(130, inv=True), 170, 1255, a2)
        text(d, (290, 1215), "Ảnh của cửa sổ", FS, DGREEN, anchor="lm", alpha=a2)
        text(d, (290, 1295), "có khung, lộn ngược", FM, INK, anchor="lm", alpha=a2)
        text(d, (960, 1255), "✓", 80, DGREEN, alpha=a2)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (40, 1370, 1040, 1565), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1420), "Chưa nói được:", FS, NAVY, alpha=k3)
        text(d, (W / 2, 1505), "số liệu minh hoạ", FM, INK, alpha=k3)


# ---------------- canh 5: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 4.3
EY = 1200; ELX, EPX = 560, 900
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Ảnh thật hứng được trên giấy", FM, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FM)) + 56
    card(d, (W / 2 - pw / 2, 480, W / 2 + pw / 2, 556), fill=A(ORANGE, k1), r=38)
    text(d, (W / 2, 518), "THỬ NGHĨ", FM, WHITE, alpha=k1)
    text(d, (W / 2, 630), "Đứng cách cửa sổ 2 m.", FS, INK, alpha=k1)
    text(d, (W / 2, 712), "Giấy cách kính bao nhiêu?", FS, INK, alpha=k1)
    if k1 > 0:   # hinh: cua so - 2 m - kinh - giay "? cm"; khong ve tia
        d.line([(90, EY), (1000, EY)], fill=A(NAVY, 0.6 * k1), width=3)
        paste_pic(img, window_pic(150), 170, EY - 81, k1)
        for x0, x1 in ((240, ELX - 30),):
            d.line([(x0, EY + 70), (x1, EY + 70)], fill=A(NAVY, k1), width=4)
            for x in (x0, x1): d.line([(x, EY + 56), (x, EY + 84)], fill=A(NAVY, k1), width=4)
        text(d, ((240 + ELX - 30) / 2, EY + 120), "2 m", FS, NAVY, alpha=k1)
        d.ellipse([ELX - 22, EY - 130, ELX + 22, EY + 130], fill=A(LBLUE, 0.8 * k1), outline=A(BLUE, k1), width=4)
        d.rounded_rectangle([EPX - 7, EY - 150, EPX + 7, EY + 150], radius=4, fill=A(WHITE, k1), outline=A(NAVY, k1), width=3)
        kq = 0.55 + 0.45 * math.sin(2.4 * t) ** 2
        text(d, ((ELX + EPX) / 2, EY + 120), "? cm", FS, ORANGE, alpha=k1 * kq)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + MOVES[-1][1], "tap"), (da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"),
            (e["t0"] + END_Q + 0.1, "open")]


CLIP = dict(id="tn-l9-thaukinh-02", header="KHTN 9 · THÍ NGHIỆM", footer="Thấu kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hứng ảnh cửa sổ", draw=s_hook, tail=0.3, caps=[
   ("Kính lúp hướng về cửa sổ.", 3.4),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Dịch giấy tới lui sau kính.", 5.0),
   ("Hình rõ thì đo kính tới giấy.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Tia ló gặp nhau trên giấy.", 4.4),
   ("Giấy ở gần tiêu điểm F'.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("So hai cách hiểu.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 8.2)]),
])
