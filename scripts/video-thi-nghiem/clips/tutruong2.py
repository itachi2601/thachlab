# Clip: tn-l12-tutruong-02 - Kim nam cham nho lam dau do huong tu truong quanh thanh nam cham (ban 1, 14/11/2026)
# Kho: content/thi-nghiem/tn-l12-tutruong-02.json (cac_buoc: 8 vi tri = 2 tren truc + 6 hai ben; ve doan theo dau N;
#   noi thanh duong cong; khong_chung_minh: khong do duoc do lon B, khong thay duong suc trong thanh). Clip KHONG dung so
#   B (µT) cua bang: chi can huong, so B "tinh theo mo hinh" khong giup cau hoi nao trong clip.
# Bai 10 muc II.2, ngay sau hop la Cau 2 (quy uoc huong tu truong = chieu nam -> bac cua kim): clip chi noi "ke theo dau N"
#   (buoc lam cua kho), khong viet the quy uoc nam -> bac. Cau 3 (duong suc la duong cong KIN): clip khong noi "kin".
# Vat li: thanh nam cham coi nhu hai cuc tu (N +, S -) dat trong hai dau thanh; huong kim = huong truong tong hop tai diem
#   dat. Hinh ve EP DOC he so SY (minh hoa, giu dung hinh dang: ra o N, vong ngoai, vao o S); huong kim lay theo tiep tuyen
#   CUA DUONG DA EP (bx, SY*by) nen kim, doan ke va duong suc luon khop nhau tren hinh. Diem X (canh than, ngang giua):
#   truong song song than thanh, huong tu phia cuc N sang phia cuc S (nguoc momen tu) -> dau N cua kim chi ve phia cuc S.
#   LUU Y kho: so_lieu_mau hang 3 ghi "chi doc than nam cham, tu nam sang bac" -> SAI chieu (dung: tu bac sang nam,
#   tuc dau N cua kim chi ve phia cuc S cua thanh); da bao phien chinh sua kho.
#
# Hop Du doan (khung web, K10 khong ve nut). Cau: "Dat kim nam cham nho tai X (canh than, ngang giua thanh). Dau N cua kim
#   chi huong nao?"
#   A. Cheo xuong, chi thang vao cuc N cua thanh     <- nhieu "kim luon chi ve cuc bac cua thanh" (hien_tuong_hay_sai 1)
#   B. Song song than thanh, chi ve phia cuc S        <- dung
#   C. Song song than thanh, chi ve phia cuc N        <- nham chieu
#   D. Vuong goc than thanh, chi ra xa thanh
# Cau chot THU NGHI (ca moi, khong co tren man): quay thanh nam cham nua vong (N, S doi cho), X giu nguyen.
#   Dap so: kim quay nua vong; dau N chi sang PHAI, van ve phia cuc S (nay o ben phai). Goi y: du kien doi.
from engine import *

NOTE = (70, 75, 95); EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)
CX, CY = 540, 630                 # tam thanh nam cham tren hinh
BL, BH = 320, 70                  # dai, cao thanh (px)
PQ = 138                          # hai cuc tu (N +, S -) o x = +-PQ trong than thanh
SY = 0.55                         # ep doc hinh duong suc (minh hoa)
BOX = (60, 260, 1020, 1000)
PTS = [(330, 0), (220, -120), (0, -170), (-220, -120), (-330, 0), (-220, 120), (0, 170), (220, 120)]   # thu tu dat kim
IX = 2                            # diem X

def Bf(x, y):
    bx = by = 0.0
    for px, q in ((PQ, 1), (-PQ, -1)):
        dx, dy = x - px, y; r3 = (dx * dx + dy * dy) ** 1.5 + 1e-9; bx += q * dx / r3; by += q * dy / r3
    return bx, by

def ang_at(p):
    """Huong dau N cua kim tai diem p (toa do ve, tuong doi tam): tiep tuyen duong suc DA EP."""
    bx, by = Bf(p[0], p[1] / SY)
    return math.atan2(SY * by, bx)

ANG = [ang_at(p) for p in PTS]
assert abs(math.cos(ANG[IX]) + 1) < 1e-6                 # X: song song than, chi sang TRAI (phia cuc S)
assert abs(ANG[0]) < 1e-6 and abs(ANG[4]) < 1e-6       # tren truc: deu chi sang phai (ra xa N; vao S)

def _trace(p, sgn, st=2.0):
    x, y = p[0], p[1] / SY; out = []
    for _ in range(6000):
        bx, by = Bf(x, y); m = math.hypot(bx, by); x += sgn * st * bx / m; y += sgn * st * by / m
        out.append((x, y * SY))
        if math.hypot(x - sgn * -PQ, y) < 10 or abs(x) > 700 or abs(y) > 900: break
    return out

def full_line(p):
    """Duong suc qua p, sap tu phia N (dau) toi phia S (cuoi)."""
    return list(reversed(_trace(p, -1))) + [p] + _trace(p, 1)

LINES = [full_line(PTS[i]) for i in (2, 1, 6, 5)]        # 4 vong (tren trong, tren ngoai, duoi trong, duoi ngoai)
for ln in LINES:                                          # vong kin trong khung: ra o N, vao o S
    assert ln[0][0] > 100 and ln[-1][0] < -100 and min(abs(y) for _, y in ln) < 12
    assert all(BOX[1] + 10 < CY + y < BOX[3] - 10 and BOX[0] + 10 < CX + x < BOX[2] - 10 for x, y in ln)

def P(p): return (CX + p[0], CY + p[1])
def inbar(q): return abs(q[0] - CX) < BL / 2 + 2 and abs(q[1] - CY) < BH / 2 + 2

def dashed(d, pts, col, w=4, seg=14, gap=9):
    acc, on, cur = 0.0, True, [pts[0]]
    for a, b in zip(pts, pts[1:]):
        acc += math.dist(a, b); cur.append(b)
        if acc >= (seg if on else gap):
            if on and len(cur) > 1: d.line(cur, fill=col, width=w)
            on, acc, cur = not on, 0.0, [b]
    if on and len(cur) > 1: d.line(cur, fill=col, width=w)

def chev(d, x, y, ang, col, s=26, w=6):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=col, width=w)

def field(d, k, a=1.0, hole=None):
    """Ve duong suc (k = phan da ve, tu phia N), chevron o dinh cung khi ve xong. Truc: ra N sang phai, vao S tu trai."""
    if k <= 0 or a <= 0: return
    col = A(PURPLE, 0.9 * a)
    for ln in LINES:
        pts = [P(q) for q in ln][: max(2, int(len(ln) * k))]
        run = []
        for q in pts + [None]:                         # bo diem trong thanh va quanh kim (hole) -> tach thanh doan
            if q is not None and not inbar(q) and not (hole and math.dist(q, hole) < 66): run.append(q); continue
            if len(run) > 1: dashed(d, run, col, w=6)
            run = []
        if k >= 1:
            j = min(range(len(ln)), key=lambda n: -abs(ln[n][1]))
            (x0, y0), (x1, y1) = ln[max(0, j - 3)], ln[min(len(ln) - 1, j + 3)]
            chev(d, CX + ln[j][0], CY + ln[j][1], math.atan2(y1 - y0, x1 - x0), col)
    xr = CX + BL / 2 + 4 + (BOX[2] - 20 - CX - BL / 2) * k
    d.line([(CX + BL / 2 + 4, CY), (xr, CY)], fill=col, width=4)
    xl0 = BOX[0] + 20; xl = xl0 + (CX - BL / 2 - 4 - xl0) * clamp(k * 1.3 - 0.3)
    if xl > xl0: d.line([(xl0, CY), (xl, CY)], fill=col, width=4)
    if k >= 1:
        chev(d, CX + 270, CY, 0, col); chev(d, CX - 250, CY, 0, col)

def magnet(d, n_right=True, cx=CX, cy=CY, L=BL, H=BH, fs=60, alpha=1.0):
    lc, rc = (BLUE, RED) if n_right else (RED, BLUE)
    d.rectangle([cx - L / 2, cy - H / 2, cx, cy + H / 2], fill=A(lc, alpha))
    d.rectangle([cx, cy - H / 2, cx + L / 2, cy + H / 2], fill=A(rc, alpha))
    d.rectangle([cx - L / 2, cy - H / 2, cx + L / 2, cy + H / 2], outline=A(NAVY, alpha), width=4)
    ls, rs = ("S", "N") if n_right else ("N", "S")
    text(d, (cx - L / 4, cy + 1), ls, fs, WHITE, alpha=alpha); text(d, (cx + L / 4, cy + 1), rs, fs, WHITE, alpha=alpha)

def needle(d, x, y, ang, L=110, hw=15, alpha=1.0):
    """Kim nam cham nho: nua mui N do (huong ang), nua S xanh, truc trang."""
    if alpha <= 0: return
    c, s = math.cos(ang), math.sin(ang); px, py = -s * hw, c * hw
    n = (x + c * L / 2, y + s * L / 2); so = (x - c * L / 2, y - s * L / 2)
    d.polygon([(x + px, y + py), n, (x - px, y - py)], fill=A(RED, alpha), outline=A(NAVY, alpha))
    d.polygon([(x + px, y + py), so, (x - px, y - py)], fill=A(BLUE, alpha), outline=A(NAVY, alpha))
    dot(d, x, y, 6, A(WHITE, alpha), A(NAVY, alpha))

def seg(d, p, ang, k=1.0, col=PURPLE):
    """Doan ke theo dau N (mui ten), tam o diem dat kim."""
    if k <= 0: return
    x, y = P(p); c, s = math.cos(ang), math.sin(ang); h = 46
    a, b = (x - c * h, y - s * h), (x - c * h + 2 * h * c * k, y - s * h + 2 * h * s * k)
    d.line([a, b], fill=A(col, 1.0), width=7)
    if k >= 1: chev(d, b[0], b[1], ang, A(col, 1.0), s=22, w=7)

def paper(d):
    card(d, BOX, fill=WHITE, outline=LIGHT, w=3)

def xmark(d, p, alpha=1.0, q=True, r=62, lab="X"):
    x, y = P(p)
    for i in range(24):
        if i % 2 == 0: d.arc((x - r, y - r, x + r, y + r), i * 15, i * 15 + 15, fill=A(PURPLE, alpha), width=4)
    if q: text(d, (x, y), "?", 60, PURPLE, alpha=alpha)
    if lab: text(d, (x + r + 16, y - r + 10), lab, 60, PURPLE, anchor="lm", alpha=alpha)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut A-D) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    paper(d); magnet(d); xmark(d, PTS[IX], appear(t, 0.6))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 170), "Đặt kim nhỏ tại X,", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 255), "cạnh thân, ngang giữa thanh.", 58, NOTE, alpha=a)
    text(d, (W / 2, y0 + 345), "Đầu N của kim chỉ đâu?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 435, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh: dat kim o 8 diem, ke doan theo dau N ----------------
STEP, T0 = 1.0, 0.5
def kim_state(t, i):
    """(alpha kim, goc kim, phan doan da ke) cua diem i o thoi diem t trong canh."""
    s = T0 + STEP * i; u = t - s
    if u < 0: return 0.0, ANG[i], 0.0
    amp = math.radians(75) * (1 if i % 2 == 0 else -1)
    g = ANG[i] + amp * math.exp(-u / 0.22) * math.cos(2 * math.pi * u / 0.36)
    al = appear(t, s, 0.12) * (1 - appear(t, s + 0.86, 0.12))
    return al, g, clamp((u - 0.62) / 0.2)

def legend(d, a=1.0):
    needle(d, 130, 318, 0, L=90, hw=13, alpha=a)
    text(d, (196, 318), "kim nhỏ: đầu đỏ là N", 58, NOTE, anchor="lm", alpha=a)

def s_do(img, d, t, sc):
    paper(d); legend(d)
    for p in PTS: dot(d, *P(p), 13, NOTE)
    magnet(d)
    for i, p in enumerate(PTS):
        al, g, ks = kim_state(t, i)
        seg(d, p, ANG[i], ks)
        if al > 0: needle(d, *P(p), g, alpha=al)
    card(d, (60, 1040, 1020, 1280), fill=(250, 248, 255), outline=LIGHT, w=3)
    n = sum(1 for i in range(8) if kim_state(t, i)[2] >= 1)
    text(d, (W / 2, 1120), f"Đã kẻ: {n}/8 điểm", 60, PURPLE)
    d.rounded_rectangle([140, 1200, 940, 1224], radius=12, fill=LIGHT)
    if n: d.rounded_rectangle([140, 1200, 140 + 100 * n, 1224], radius=12, fill=PURPLE)

# ---------------- canh 3: Dap an tai X + noi cac doan thanh duong suc ----------------
def s_noi(img, d, t, sc):
    M = sc["M"]
    paper(d)
    kf = ease((t - 1.6) / 1.2)
    field(d, kf, hole=P(PTS[IX]))
    for i, p in enumerate(PTS):
        if i != IX: seg(d, p, ANG[i])
    magnet(d)
    u = t - 0.3                                            # kim o X: dao dong roi dung dung huong (dap an)
    g = ANG[IX] + (math.radians(70) * math.exp(-u / 0.35) * math.cos(2 * math.pi * u / 0.5) if u > 0 else math.radians(70))
    needle(d, *P(PTS[IX]), g, alpha=1 - 0.6 * appear(t, M[1], 0.4))
    card(d, (60, 1040, 1020, 1170), fill=WHITE, outline=NAVY, w=5)
    text(d, (W / 2, 1105), "Dọc thân, chỉ về phía S", 62, NAVY)
    k2 = appear(t, M[1] + 1.4, 0.45)
    card(d, (60, 1210, 1020, 1350), fill=A(WHITE, k2), outline=A(PURPLE, k2), w=4)
    text(d, (W / 2, 1280), "Ra ở cực N, vào ở cực S", 62, PURPLE, alpha=k2)

# ---------------- canh 4: Rut ra (moi diem mot huong) + chua noi duoc ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    paper(d); field(d, 1.0, hole=P(PTS[IX]))
    for i, p in enumerate(PTS):
        if i != IX: seg(d, p, ANG[i])
    magnet(d)
    u = t - 0.3                                            # dat lai kim o X: dao dong roi dung DUNG huong cu
    g = ANG[IX] + (math.radians(-80) * math.exp(-u / 0.25) * math.cos(2 * math.pi * u / 0.4) if u > 0 else math.radians(-80))
    needle(d, *P(PTS[IX]), g)
    a = appear(t, M[0] + 0.9, 0.45)
    card(d, (60, 1040, 1020, 1170), fill=A(WHITE, a), outline=A(BLUE, a), w=4)
    text(d, (W / 2, 1105), "Đặt lại: vẫn hướng ấy", 62, BLUE, alpha=a)
    b = appear(t, M[1], 0.45)
    card(d, (60, 1210, 1020, 1520), fill=A(WHITE, b), outline=A(NAVY, b), w=5)
    pill(d, W / 2, 1280, "CHƯA NÓI ĐƯỢC", NAVY, b)
    text(d, (W / 2, 1380), "Độ lớn B", 60, INK, alpha=b)
    text(d, (W / 2, 1460), "Đường sức trong thanh", 60, INK, alpha=b)

# ---------------- canh 5: Bay "kim luon chi ve cuc N cua thanh" ----------------
BP = (0, 1)                                                # hai diem soi: tren truc canh N, cheo tren canh N
def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = 1.0; mk = M[1]; kc = appear(t, mk + 0.2, 0.45)
    paper(d); field(d, 1.0, kc); magnet(d)
    for i in BP:
        xmark(d, PTS[i], k0 * (1 - kc), lab=None, r=58)
        needle(d, *P(PTS[i]), ANG[i], alpha=kc)
    y = 1030
    card(d, (40, y, 1040, y + 300 + 140 * kc), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, y + 70, "BẪY", RED)
    q = "“Kim luôn chỉ về cực N”"
    ks = clamp((t - mk) / 0.4); f = F(60); lw = tw(d, q, f); yy = y + 200
    text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks))
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=6)
    if kc > 0: text(d, (W / 2, y + 340), "Kim nằm dọc đường sức", 62, DORANGE, alpha=kc)

# ---------------- canh 6: THU NGHI (cau chot o khung: quay thanh nua vong) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k)
    magnet(d, n_right=False, cx=540, cy=640, L=470, H=104, fs=60, alpha=k)
    x, y, r = 540, 470, 62
    for i in range(24):
        if i % 2 == 0: d.arc((x - r, y - r, x + r, y + r), i * 15, i * 15 + 15, fill=A(PURPLE, k), width=5)
    text(d, (x, y), "?", 60, PURPLE, alpha=k); text(d, (x + r + 16, y), "X", 60, PURPLE, anchor="lm", alpha=k)
    text(d, (W / 2, 850), "Quay thanh nửa vòng:", 64, INK, alpha=k)
    text(d, (W / 2, 940), "N và S đổi chỗ, X giữ nguyên.", 60, INK, alpha=k)
    text(d, (W / 2, 1060), "Đầu N của kim chỉ đâu?", 64, DORANGE, alpha=k)
    seg_bar(d, 1190, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, no, ru, b, e = sc["hook"], sc["do"], sc["noi"], sc["rut"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + T0, "tap"),
             (no["t0"] + 0.3, "ding"), (no["t0"] + no["M"][1] + 0.2, "tap"), (ru["t0"] + ru["M"][1], "tap"),
             (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l12-tutruong-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
            footer="Khái niệm từ trường · thachlab.id.vn", scenes=[
 dict(key="hook", title="Kim nam châm làm đầu dò", draw=s_hook, tail=0.3, caps=[
   ("Thanh nam châm trên tờ giấy.", 3.6),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Chờ kim đứng yên, kẻ theo đầu N.", 4.6),
   ("Lần lượt 8 điểm quanh thanh.", 4.2)]),
 dict(key="noi", title="Kết quả", draw=s_noi, tail=0.5, caps=[
   ("Nhìn lại kim ở điểm X.", 3.0),
   ("Nối các đoạn thành đường cong.", 4.4)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.5, caps=[
   ("Đặt lại kim ở X.", 3.6),
   ("Kim chưa cho biết gì?", 3.4)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.7, caps=[
   ("Đúng không?", 2.5),
   ("Sai: tùy chỗ đặt kim.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự đoán.", 6.8)]),
])
