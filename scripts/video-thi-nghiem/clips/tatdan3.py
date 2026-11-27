# Clip: tn-l11-tatdan-03 - Xich du: ngoi yen va nhun dung luc (vi_du, hoat canh minh hoa) (9/11/2026, chang B L11 Dao dong;
# dung lai 27/11/2026 theo cong moi: chu ve >= 55 px, moi nhip >= 2,5 s, K10, thanh dem day, Bay hai khung, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-tatdan-03.json (_kiem_so()):
#   tham_so: A0 = 40 cm (bien do tren cung, 20-60 buoc 5) ; beta = 0,08 /s ; T = 2,0 s.
#   so_lieu_mau (nhip n: ngoi yen / nhun): 0 40,0/40,0 ; 1 34,1/40,0 ; 2 29,0/40,0 ; 3 24,8/40,0.
#   gia_thiet: "beta = 0,08 chi de minh hoa" -> nhan "minh hoạ" suot clip.
# DOI CA DU DOAN (27/11): ca cu "nhun thi sau 3 nhip cao co nao" da co san trong de cau mo bai ("nhun dung nhip thi giu
#   duoc do cao") va dong Quan sat cua hop exp -> Du doan moi hoi lan NGOI YEN: sau 3 nhip con cao co nao so voi luc tha?
#   -> con hon mot nua (24,8 / 40 cm). Khong ve vach "nua" bang so (20 cm khong co trong kho), chi nhan "nửa".
# Doan ngay sau hop: cau tu kiem dong ho qua lac ("moi nhip chi bu phan da mat; chu ki van la chu ki rieng") -> clip
#   KHONG noi "chu ki rieng", khong dung bay "luc cuong buc lien tuc".
# Bay = hien_tuong_hay_sai[1] "nhun luc nao cung cao them": hai khung canh nhau, luc nhun cung chieu / nguoc chieu chieu di;
#   du chay tiep toi bien: cung chieu cham vach dut (giu do cao), nguoc chieu dung thap hon (khong ghi so).
# THU NGHI (= cau_chot khung web): ngoi yen 1 nhip (40 -> 34,1 cm) roi moi nhun dung luc nhu lan hai -> sau nhip 3 cao?
#   -> 34,1 cm (nhun bu dung phan mat, giu muc luc bat dau nhun). Nhieu: 40 cm (tuong nhun dua ve cao ban dau),
#   24,8 cm (chep lan ngoi yen), 29,0 cm. So 34,1 hien o Tien hanh nhung CAU HOI can buoc "giu muc hien tai" chua chieu.
from engine import *

A0, BETA, PER = 40.0, 0.08, 2.0
ROWS = [(0, 40.0, 40.0), (1, 34.1, 40.0), (2, 29.0, 40.0), (3, 24.8, 40.0)]
DRED, DGREEN, DPURPLE = (185, 28, 28), (21, 110, 55), (91, 33, 182)
def fs(v): return f"{v:.1f}".replace(".", ",")
def th_amp(acm): return acm / 100.0             # rad, day ~1 m

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-tatdan-03.json")))
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["A0"]["mac_dinh"] == A0 and ts["beta"]["gia_tri"] == BETA and ts["T"]["gia_tri"] == PER
    for r, h in zip(ROWS, k["so_lieu_mau"]["hang"]): assert tuple(h[1:]) == r, (r, h)
    for n, al, ap in ROWS: assert abs(A0 * math.exp(-BETA * n * PER) - al) < 0.051
_kiem_so()

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 56
    card(d, (cx - pw / 2, cy - size * 0.82, cx + pw / 2, cy + size * 0.82), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def cbar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = math.floor(p * 10 + 1e-9) / 10
    d.rounded_rectangle([140, y, 940, y + 70], radius=35, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, y, 140 + 800 * (1 - q), y + 70], radius=35, fill=A(col, a))

def tag(d):
    """Nhan 'minh hoạ' goc phai tren, suot clip (vi_du, so khong do that)."""
    pill(d, 900, 252, "minh hoạ", 55, ORANGE, (255, 237, 213))

# ---------------- hai xich du ----------------
CXL, CXR, PY, LR = 280, 800, 330, 300
def theta(t, push, a0=A0):
    a = a0 if push else a0 * math.exp(-BETA * max(0.0, t))
    return th_amp(a) * math.cos(2 * math.pi * t / PER)
def dtheta(t, push):
    a = A0 if push else A0 * math.exp(-BETA * max(0.0, t))
    return -th_amp(a) * (2 * math.pi / PER) * math.sin(2 * math.pi * t / PER)

def frame_(d, cx, py=PY):
    d.line([(cx - 230, py), (cx + 230, py)], fill=NAVY, width=8)
    d.line([(cx - 200, py), (cx - 250, py + 420)], fill=NAVY, width=6)
    d.line([(cx + 200, py), (cx + 250, py + 420)], fill=NAVY, width=6)
    d.line([(cx - 260, py + 422), (cx + 260, py + 422)], fill=(150, 120, 80), width=4)

def swing(d, cx, th, col, pump=0.0, py=PY):
    """Du + nguoi ngoi. pump 0..1: nga nguoi ra sau, duoi chan khi nhun."""
    ux, uy = math.sin(th), math.cos(th)
    fx, fy = math.cos(th), -math.sin(th)
    sx_, sy_ = cx + LR * ux, py + LR * uy
    d.line([(cx, py), (sx_, sy_)], fill=INK, width=4)
    d.line([(sx_ - 40 * fx, sy_ - 40 * fy), (sx_ + 40 * fx, sy_ + 40 * fy)], fill=(120, 80, 40), width=12)
    hip = (sx_ - 12 * ux, sy_ - 12 * uy)
    sh = (hip[0] - 72 * ux - pump * 24 * fx, hip[1] - 72 * uy - pump * 24 * fy)
    hd = (sh[0] - 30 * ux - pump * 10 * fx, sh[1] - 30 * uy - pump * 10 * fy)
    hand = (cx + (LR - 105) * ux, py + (LR - 105) * uy)
    knee = (hip[0] + 50 * fx, hip[1] + 50 * fy)
    ang = 0.15 + pump * 1.1
    foot = (knee[0] + 55 * (ux * math.cos(ang) + fx * math.sin(ang)), knee[1] + 55 * (uy * math.cos(ang) + fy * math.sin(ang)))
    d.line([hip, sh], fill=col, width=16)
    d.line([sh, hand], fill=col, width=9)
    d.line([hip, knee, foot], fill=col, width=11, joint="curve")
    dot(d, hd[0], hd[1], 20, col, outline=WHITE)
    return sx_, sy_

def peak_marks(d, cx, upto):
    k = 0
    while k * PER / 2 <= upto + 1e-6:
        th = theta(k * PER / 2, False)
        x, y = cx + (LR + 30) * math.sin(th), PY + (LR + 30) * math.cos(th)
        if upto - k * PER / 2 > 0.3: dot(d, x, y, 8, BLUE)
        k += 1

def push_arrows(d, t, sx_, sy_):
    th, om = theta(t, True), dtheta(t, True)
    if th * om >= 0 or abs(th) < 0.03: return        # chi khi dang di xuong
    s = 1 if om > 0 else -1
    tx, ty = s * math.cos(th), -s * math.sin(th)
    nx, ny = -ty, tx
    for off, col in ((26, GREEN), (-26, ORANGE)):
        p1 = (sx_ + nx * off, sy_ + ny * off + 30)
        arrow(d, p1, (p1[0] + tx * 110, p1[1] + ty * 110), col, w=7, head=22)

def rig(d, t, run=True):
    frame_(d, CXL); frame_(d, CXR)
    tl = t if run else 0.0
    if run: peak_marks(d, CXL, tl)
    swing(d, CXL, theta(tl, False), BLUE)
    th, om = theta(tl, True), dtheta(tl, True)
    pump = clamp(-th * om / (th_amp(A0) ** 2 * math.pi / 2)) if run else 0.0
    sx_, sy_ = swing(d, CXR, th, ORANGE, pump)
    if run: push_arrows(d, tl, sx_, sy_)
    text(d, (CXL, 800), "Ngồi yên", 58, BLUE)
    text(d, (CXR, 800), "Nhún", 58, ORANGE)

# ---------------- bieu do cot (truc co dinh) ----------------
BASE, HS = 1500, 8.5                 # 1 cm = 8,5 px -> 40 cm = 340 px
GXS = (330, 530, 730, 930)
def bars(d, nshow, diffs=False):
    d.line([(150, BASE), (1010, BASE)], fill=NAVY, width=4)
    text(d, (110, BASE + 56), "nhịp", 55, INK, anchor="mm")
    y40 = BASE - A0 * HS; x = 230
    while x < 1010: d.line([(x, y40), (min(x + 18, 1010), y40)], fill=A(ORANGE, 0.8), width=4); x += 32
    text(d, (40, y40), "40 cm", 55, ORANGE, anchor="lm")
    for (n, al, ap), x in zip(ROWS, GXS):
        text(d, (x, BASE + 56), str(n), 55, INK)
        if n >= nshow: continue
        for v, col, dx in ((al, BLUE, -42), (ap, ORANGE, 42)):
            d.rounded_rectangle([x + dx - 36, BASE - v * HS, x + dx + 36, BASE], radius=8, fill=col)
        if n > 0: text(d, (x, BASE - A0 * HS - 70), fs(al), 55, BLUE)      # hang so rieng tren vach 40 cm

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    tag(d); M = sc["M"]
    rig(d, 0.0, run=False)
    pill(d, 330, 252, "thả từ 40 cm", 56, WHITE, NAVY)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 700), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 80, "DỰ ĐOÁN", 58, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 270), "Ngồi yên, sau 3 nhịp", 66, INK, alpha=a)
    text(d, (W / 2, y0 + 400), "còn cao cỡ nào?", 66, DPURPLE, alpha=a)
    cbar(d, y0 + 560, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
REL = 0.8
def s_do(img, d, t, sc):
    tag(d)
    ts = clamp(t - REL, 0, 3 * PER)
    rig(d, ts, run=t >= REL)
    n = min(3, int(ts / PER + 1e-6))
    pill(d, 330, 252, f"t = {ts:.0f} s", 56, WHITE, NAVY)
    arrow(d, (60, 905), (150, 905), GREEN, w=8, head=22); text(d, (170, 905), "chiều đi", 56, GREEN, anchor="lm")
    arrow(d, (560, 905), (650, 905), ORANGE, w=8, head=22); text(d, (670, 905), "lực nhún", 56, ORANGE, anchor="lm")
    bars(d, 0 if t < REL else 1 + n)

# ---------------- canh 3: Ket qua + Rut ra ----------------
def s_dapan(img, d, t, sc):
    tag(d); M = sc["M"]
    card(d, (60, 330, 1020, 470), fill=WHITE, outline=NAVY, r=26, w=5)
    text(d, (W / 2, 400), "ĐÁP ÁN · còn hơn một nửa", 60, NAVY)
    kr = appear(t, M[1] - 0.1, 0.45)
    if kr > 0:
        card(d, (60, 500, 1020, 640), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=26, w=5)
        text(d, (W / 2, 570), "Nhún bù phần đã mất", 60, DGREEN, alpha=kr)
    text(d, (60, 760), "Ngồi yên", 58, BLUE, anchor="lm"); text(d, (1020, 760), "Nhún", 58, ORANGE, anchor="rm")
    bars(d, 4)
    # vach "nua" (khong ghi so) + nhap nhay cot nhip 3 cho hinh khong dung yen
    yh = BASE - A0 / 2 * HS; x = 230
    while x < 1010: d.line([(x, yh), (min(x + 18, 1010), yh)], fill=DPURPLE, width=4); x += 32
    text(d, (40, yh), "nửa", 55, DPURPLE, anchor="lm")
    if t > 0.3:
        u = 0.5 + 0.5 * math.cos(2 * math.pi * (t - 0.3) / 1.6)
        x3 = GXS[3] - 42
        d.rounded_rectangle([x3 - 48, BASE - ROWS[3][1] * HS - 12, x3 + 48, BASE + 4], radius=12, outline=A(DPURPLE, u), width=8)
    if t > M[1]:
        u = 0.5 + 0.5 * math.cos(2 * math.pi * (t - M[1]) / 1.6)
        for x in GXS:
            d.rounded_rectangle([x + 2, BASE - A0 * HS - 12, x + 82, BASE + 4], radius=12, outline=A(DGREEN, u), width=8)

# ---------------- canh 4: Bay - "nhun luc nao cung cao them" ----------------
BR, BTH, BLOW = 330, 0.75, 0.2
def mini(d, cx, th, col):
    py = 330
    d.line([(cx - 120, py), (cx + 120, py)], fill=NAVY, width=7)
    sx_, sy_ = cx + BR * math.sin(th), py + BR * math.cos(th)
    d.line([(cx, py), (sx_, sy_)], fill=INK, width=4)
    fx, fy = math.cos(th), -math.sin(th)
    d.line([(sx_ - 38 * fx, sy_ - 38 * fy), (sx_ + 38 * fx, sy_ + 38 * fy)], fill=(120, 80, 40), width=14)
    dot(d, sx_ - 40 * math.sin(th), sy_ - 40 * math.cos(th), 22, col, outline=WHITE)
    return sx_, sy_

def bay_panel(d, cx, t, M, same):
    col = ORANGE if same else DRED
    card(d, (cx - 250, 215, cx + 250, 1000), fill=WHITE, outline=col, w=6)
    text(d, (cx, 280), "cùng chiều" if same else "ngược chiều", 58, col)
    py = 330
    yt = py + BR * math.cos(BTH)                                  # muc bien luc dau (vach dut)
    x = cx - 240
    while x < cx + 240: d.line([(x, yt), (min(x + 16, cx + 240), yt)], fill=A(INK, 0.6), width=4); x += 28
    # nhip 1 (0 -> M1): du qua lai tu do ; nhip 2 (M1 -> M2): dung o giua duong xuong (ben phai) de hien hai mui ten ;
    # nhip 3 (sau M2): chay tiep toi bien trai: cung chieu -> toi vach dut ; nguoc chieu -> dung thap hon.
    if t < M[1]:
        th = BTH * math.cos(2 * math.pi * (t - 0.3) / 2.0) if t > 0.3 else BTH
        mini(d, cx, th, col); return
    if t < M[2]:
        th = 0.35
        sx_, sy_ = mini(d, cx, th, col)
        tx, ty = -math.cos(th), math.sin(th)                       # chieu di: sang trai, xuong
        arrow(d, (sx_ + 60 * tx - 30 * ty, sy_ + 60 * ty + 70), (sx_ + 170 * tx - 30 * ty, sy_ + 170 * ty + 70), GRAY, w=10, head=28)
        k = appear(t, M[1] + 0.8, 0.4)
        s = 1 if same else -1
        p0 = (sx_ - 10 * tx + 80 * ty * 0 - 20, sy_ + 150)
        if k > 0: arrow(d, (sx_ - 30, sy_ + 150), (sx_ - 30 + s * 120 * tx, sy_ + 150 + s * 120 * ty), A(col, k), w=11, head=30)
        return
    u = ease((t - M[2]) / 1.4)
    th_end = -BTH if same else -BLOW
    th = 0.35 + (th_end - 0.35) * u
    mini(d, cx, th, col)
    if u >= 1:
        lab = "✓ giữ độ cao" if same else "✗ thấp đi"
        text(d, (cx, 920), lab, 58, DGREEN if same else DRED)

def s_bay(img, d, t, sc):
    tag(d); M = sc["M"]
    bay_panel(d, 285, t, M, True); bay_panel(d, 795, t, M, False)
    k = appear(t, M[1] - 0.1, 0.4)
    if k > 0:
        arrow(d, (70, 1080), (160, 1080), A(GRAY, k), w=10, head=26); text(d, (180, 1080), "chiều đi", 56, INK, anchor="lm", alpha=k)
        arrow(d, (560, 1080), (650, 1080), A(ORANGE, k), w=10, head=26); text(d, (670, 1080), "lực nhún", 56, INK, anchor="lm", alpha=k)

# ---------------- canh 5: Gioi han ----------------
def s_gioi(img, d, t, sc):
    tag(d)
    card(d, (40, 330, 1040, 640), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 410), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 545), "Nhún mạnh hơn thì sao?", 62, INK)
    frame_(d, W / 2, 760)
    th = theta(t, True)
    swing(d, W / 2, th, ORANGE, clamp(-th * dtheta(t, True) / (th_amp(A0) ** 2 * math.pi / 2)), py=760)

# ---------------- canh 6: Chot (phu de) + THU NGHI ----------------
def s_end(img, d, t, sc):
    k1 = 1.0
    card(d, (40, 330, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 410, "THỬ NGHĨ", 58, WHITE, ORANGE, k1)
    text(d, (W / 2, 560), "Nhịp 1 ngồi yên: 40 → 34,1 cm", 60, BLUE, alpha=k1)
    text(d, (W / 2, 690), "Rồi nhún như lần hai", 62, ORANGE, alpha=k1)
    text(d, (W / 2, 880), "Hết nhịp 3,", 66, INK, alpha=k1)
    text(d, (W / 2, 975), "đu cao bao nhiêu?", 66, INK, alpha=k1)
    cbar(d, 1200, t, 1.2, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]
    out += [(do["t0"] + REL + k * PER, "tap") for k in range(4)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (b["t0"] + b["M"][2] + 1.4, "ding"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-tatdan-03", header="VẬT LÍ 11 · VÍ DỤ", footer="Tắt dần · duy trì · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai lần trên xích đu", draw=s_hook, tail=0.3, caps=[
   ("Cùng một đu, hai cách.", 3.6),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Hai lần làm, đặt cạnh nhau.", 3.6),
   ("Ghi độ cao sau mỗi nhịp.", 3.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Đu thật tắt chậm.", 3.4),
   ("Lần nhún giữ nguyên.", 3.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Nhún lúc nào cũng cao thêm?", 3.4),
   ("So lực nhún với chiều đi.", 3.4),
   ("Cùng chiều mới bù được.", 3.0)]),
 dict(key="gioi", title="Giới hạn", draw=s_gioi, tail=0.3, caps=[
   ("Số minh hoạ, chưa đo thật.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Không bù thì tắt.", 7.2)]),
])
