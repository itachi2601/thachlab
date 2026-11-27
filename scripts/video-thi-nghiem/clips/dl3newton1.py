# Clip: tn-l10-newton3-01 - Hai luc ke keo nhau (lo 7, 18/11/2026; dung lai 27/11/2026 theo viec 4: cong --do-chu,
# chu >= 55 px khi ve (ca so tren luc ke: co = 56), K10, Bay hinh tu giai thich, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-newton3-01.json (_kiem_so() doi chieu):
#   so_lieu_mau (F_keo, F1, F2 N): 1,0 1,0 1,0 | 2,0 2,0 2,0 | 3,0 3,0 3,1 | 4,0 4,1 4,0 | 5,0 5,0 5,0.
#   dung_cu: luc ke lo xo 5 N -> engine.luc_ke() (vach 0,2 N, nam ngang, ghi so nguyen).
#   Clip chi dung 3 lan keo nhe/vua/manh (hang 1, 2, 5): hang 3, 4 lech 0,1 N la Cau 1 Tu kiem tra ngay sau hop
#   (chenh do sai so doc) -> clip KHONG hien, khong giai thich chenh lech nay.
#   mo_hinh.ghi_chu: keo giat thi kim dao dong quanh gia tri can bang -> canh bay ve hai kim rung CUNG nhau, khong ghi so.
# Du doan (K10: khong nut, khong "Chon dap an..."): giu yen luc ke 1, keo luc ke 2 toi 2,0 N -> luc ke 1 chi bao nhieu?
#   Dap an 2,0 N. Khong trung quiz mo bai (day thanh san), Cau 1-6 cua bai.
# Bay = hien_tuong_hay_sai[0] "ben nguoi keo chi lon hon": the "De tuong" + keo giat (hai kim rung cung nhau) + the "✓".
# Chua noi duoc = mo_hinh.gia_thiet "bo qua khoi luong luc ke".
# Cau chot (ghi_chu kho): luc ke 1 buoc vao tuong, keo luc ke 2 bang 3,5 N -> luc ke 1 chi 3,5 N (nhieu: 7 N, 0 N).
#   Tuong thay tay giu (hien_tuong_hay_sai[1] "dau bi giu co dinh thi khong co luc") -> mot buoc suy luan chua chieu.
from engine import *

ROWS = [("nhẹ", 1.0, 1.0, 1.0), ("vừa", 2.0, 2.0, 2.0), ("mạnh", 5.0, 5.0, 5.0)]   # so_lieu_mau hang 1, 2, 5
FMAX = 5.0
CHOT = 3.5
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-newton3-01.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    assert all(r[1:] in hang for r in ROWS)
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["F_keo"]["min"] <= CHOT <= tp["F_keo"]["max"] and "3,5 N" in k["so_lieu_mau"]["ghi_chu"]
    assert "5 N" in k["dung_cu"][0]["ten"]
_kiem_so()

SKIN = (240, 196, 160); SKIN_D = (190, 140, 105); DGREEN = (21, 110, 55); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); EMPTY = (148, 140, 128)
C1, C2 = BLUE, ORANGE                       # mau luc ke 1, luc ke 2 (va luc dat len no)
T1, T2 = (219, 234, 254), (255, 237, 213)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem LIEN (tut tung nac 10 %), cao 70 px: khong chia o de khoi goi y so (brief 27/11)."""
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (175, y, 905, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (175, y, 175 + max(70, 730 * q), y + 70), fill=A(col, a), r=35)

def tag(d, y, s, col, fill, a):
    card(d, (40, y, 1040, y + 110), fill=A(fill, a), outline=A(col, a), r=24, w=6)
    text(d, (W / 2, y + 55), s, 60, col, alpha=a)

# ---------------- dan thi nghiem: hai luc ke nam ngang moc vao nhau (mp4 x = 65 + 0,88x) ----------------
XC, Y0 = 540, 480
ROPE, BODY = 22, 330

def one_meter(d, side, f_read, xh, y, body=BODY, hand=True, alpha=1.0):
    """side -1: luc ke 1 (than ben trai, moc o xh); +1: luc ke 2. Tra ve x tay."""
    Q = lambda s, h=0.0: (xh + side * s, y + h)
    se = luc_ke(d, Q, 0, 20, 20 + body, FMAX, f_read, nho=0.2, so=(0, 1, 2, 3, 4, 5), hw=46, ben=-1, co=56, alpha=alpha)
    if not hand: return Q(se)[0]
    d.line([Q(se - 16), Q(se + 12)], fill=A(NAVY, alpha), width=8)
    hx, hy = Q(se + 40); dot(d, hx, hy, 28, A(SKIN, alpha), outline=A(SKIN_D, alpha))
    return hx

def rig(d, f1, f2, lab1=None, lab2=None, top=250, dx=0.0, roles=True):
    card(d, (40, top, 1040, top + 520), fill=WHITE, outline=LIGHT, w=3)
    y = Y0
    d.rectangle([40, y + 70, 1040, y + 96], fill=WOOD); d.line([(40, y + 70), (1040, y + 70)], fill=WOOD_D, width=3)
    one_meter(d, -1, f1, XC - ROPE + dx, y); one_meter(d, 1, f2, XC + ROPE + dx, y)
    d.ellipse([XC + dx - 34, y - 12, XC + dx + 34, y + 12], outline=NAVY, width=5)          # khuyen noi hai moc
    for x, c, s in ((XC - 230, C1, "lực kế 1"), (XC + 230, C2, "lực kế 2")):
        text(d, (x, y + 150), s, 58, c)
    if roles:
        text(d, (60, y + 220), "giữ yên", 58, INK, anchor="lm")
        text(d, (1020, y + 220), "kéo →", 58, INK, anchor="rm")
    for x, c, tt, lab in ((XC - 230, C1, T1, lab1), (XC + 230, C2, T2, lab2)):
        if lab is None: continue
        card(d, (x - 120, y - 210, x + 120, y - 130), fill=tt, r=22)
        text(d, (x, y - 170), lab, 60, c)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    f2 = 2.0 * ease((t - 0.8) / 1.0)
    rig(d, None, f2, "? N", "2,0 N" if t > 1.9 else "…")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 810 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 195), "Lực kế 2 chỉ 2,0 N.", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 300), "Lực kế 1 chỉ bao nhiêu?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 420, t, M[1] + 0.2, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
T_S = (0.4, 2.3, 4.2)        # bat dau moi lan tang luc keo
RAMP, T_ROW = 0.9, 0.35

def do_state(t):
    """-> (f hai kim, so dang doc (None khi kim dang chay), so hang da ghi). Hai kim LUON cung mot so."""
    k = sum(1 for ts in T_S if t >= ts - 1e-9) - 1
    n = sum(1 for j in range(3) if t >= T_S[j] + RAMP + T_ROW - 1e-9)
    if k < 0: return 0.0, None, n
    f0 = ROWS[k - 1][1] if k > 0 else 0.0
    q = (t - T_S[k]) / RAMP
    f = lerp(f0, ROWS[k][1], ease(q))
    return f, (ROWS[k][1] if q >= 1 else None), n

XS = (190, 500, 830)
def table(d, n, y=820, hl=None, a=1.0):
    card(d, (40, y, 1040, y + 450), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    text(d, (XS[1], y + 62), "lực kế 1", 58, C1, alpha=a)
    text(d, (XS[2], y + 62), "lực kế 2", 58, C2, alpha=a)
    d.line([(70, y + 115), (1010, y + 115)], fill=A(LIGHT, a), width=3)
    for j, (lab, fk, f1, f2) in enumerate(ROWS):
        yy = y + 180 + j * 96
        if hl == j: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=20, fill=A((237, 233, 254), a))
        text(d, (XS[0], yy), lab, 60, INK, alpha=a)
        if j < n:
            text(d, (XS[1], yy), vn(f1) + " N", 62, C1, alpha=a); text(d, (XS[2], yy), vn(f2) + " N", 62, C2, alpha=a)
        else:
            for x in XS[1:]: text(d, (x, yy), "·", 60, GRAY, alpha=a)

def s_do(img, d, t, sc):
    f, read, n = do_state(t)
    lab = vn(read) + " N" if read is not None else "…"
    rig(d, f, f, lab, lab)
    table(d, n, hl=(n - 1 if n > 0 else None))

def _kiem_dong_bo():
    """Moi 0,05 s: hai kim cung so; o so chi hien khi kim dung dung so cua hang; hang j chi hien sau lan j."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        f, read, n = do_state(t)
        k = sum(1 for ts in T_S if t >= ts - 1e-9) - 1
        if read is not None and abs(f - read) > 1e-9: bad.append((round(t, 2), "so o != kim", f, read))
        if read is not None and abs(read - ROWS[k][1]) > 1e-9: bad.append((round(t, 2), "so o != hang", read))
        if n > 0 and k >= 0 and n - 1 > k: bad.append((round(t, 2), "hang som", n, k))
        if not (0 <= f <= FMAX): bad.append((round(t, 2), "kim ngoai thang", f))
        t += 0.05
    if T_S[-1] + RAMP + T_ROW > sc["T"] - 0.6: bad.append("hang cuoi hien qua muon")
    return bad

# ---------------- canh 3: Ket qua + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    rig(d, 2.0, 2.0, "2,0 N", "2,0 N", roles=False)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        y0 = 830 + (1 - k1) * 20
        card(d, (40, y0, 1040, y0 + 330), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=6)
        pill(d, W / 2, y0 + 70, "RÚT RA", GREEN, k1)
        text(d, (W / 2, y0 + 180), "Lực và phản lực:", 62, DGREEN, alpha=k1)
        text(d, (W / 2, y0 + 265), "bằng nhau, cùng lúc", 62, DGREEN, alpha=k1)

# ---------------- canh 4: moi luc ke chiu luc nao (tach rieng hai luc ke) ----------------
SB = 400
XH1, XH2 = 560, 520          # moc luc ke 1 (hang tren), luc ke 2 (hang duoi): hai vat tach hai hang
LA = 200                     # px cho 2,0 N (hai mui ten dai bang nhau)
def s_luc(img, d, t, sc):
    """kiem-v1: tach hai hang (moi luc ke mot hang), luc ke dai SB = 400, mui ten LA = 200, nhan mot dong sat mui ten."""
    M = sc["M"]
    card(d, (40, 250, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    rows = ((-1, XH1, 480, T1, C1, "lực kế 1", M[0] + 1.8, "Lực kế 2 kéo lực kế 1: 2,0 N"),
            (1, XH2, 860, T2, C2, "lực kế 2", M[1] + 0.1, "Lực kế 1 kéo lực kế 2: 2,0 N"))
    for side, xh, y, tint, col, name, tk, lab in rows:
        x_end = xh + side * (20 + SB + 30)
        d.rounded_rectangle([min(xh, x_end) - 8, y - 70, max(xh, x_end) + 8, y + 70], radius=26, fill=tint)
        one_meter(d, side, 2.0, xh, y, body=SB, hand=False)
        text(d, ((xh + x_end) / 2, y + 112), name, 58, col)
        k = appear(t, tk, 0.4)
        if k > 0:          # luc dat len moc cua chinh luc ke nay, huong ve phia luc ke kia
            arrow(d, (xh, y), (xh - side * LA * ease(k), y), A(col, k), w=10, head=30)
            dot(d, xh, y, 11, col)
            text(d, (W / 2, y - 170), lab, 58, col, alpha=k)

# ---------------- canh 5: Bay (keo giat) ----------------
def jerk(t, t0):
    """Keo giat: hai kim rung CUNG NHAU quanh vi tri can bang (khong ghi so)."""
    tau = t - t0
    if tau < 0: return 2.0
    return 2.5 - 0.5 * math.exp(-4 * tau) + 1.8 * math.exp(-0.9 * tau) * math.sin(2 * math.pi * 1.4 * tau)

def s_bay(img, d, t, sc):
    M = sc["M"]
    f = clamp(jerk(t, M[0] + 0.8), 0, FMAX)
    rig(d, f, f, roles=False)
    tag(d, 830, "✗ Dễ tưởng: bên kéo lớn hơn", DRED, (254, 242, 242), appear(t, 2.0, 0.45))
    k2 = appear(t, M[1] + 0.5, 0.45)
    if k2 > 0: tag(d, 990, "✓ Hai số vẫn bằng nhau", DGREEN, (236, 253, 243), k2)

# ---------------- canh 6: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 250, 1040, 540), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 330), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 450), "Lực kế nặng thì sao?", 64, INK)
    card(d, (40, 580, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    y = 880; dx = -40 + 80 * ease(t / 2.5)
    one_meter(d, -1, 2.0, XC - ROPE + dx, y, hand=False); one_meter(d, 1, 2.0, XC + ROPE + dx, y, hand=False)
    d.ellipse([XC + dx - 34, y - 12, XC + dx + 34, y + 12], outline=NAVY, width=5)
    k = appear(t, 1.2, 0.5)
    for xx in (XC - 230 + dx, XC + 230 + dx): text(d, (xx, y + 130), "?", 90, PURPLE, alpha=k)

# ---------------- canh 7: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1500), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k1)
    y = 620
    xw = 80                                                      # tuong giu dau luc ke 1 (thay tay)
    d.rectangle([xw - 40, y - 130, xw, y + 130], fill=A(LIGHT, k1)); d.line([(xw, y - 130), (xw, y + 130)], fill=A(INK, k1), width=5)
    for yy in range(y - 120, y + 130, 30): d.line([(xw - 40, yy + 26), (xw, yy)], fill=A(MUTED, k1), width=3)
    e1 = one_meter(d, -1, None, XC - ROPE, y, body=300, hand=False, alpha=k1)
    d.line([(xw, y), (e1, y)], fill=A(NAVY, k1), width=6)
    one_meter(d, 1, None, XC + ROPE, y, body=300, alpha=k1)
    d.ellipse([XC - 34, y - 12, XC + 34, y + 12], outline=A(NAVY, k1), width=5)
    text(d, (xw + 10, y + 180), "tường", 58, INK, anchor="lm", alpha=k1)
    text(d, (W / 2, 930), "Kéo lực kế 2: 3,5 N.", 64, INK, alpha=k1)
    text(d, (W / 2, 1060), "Lực kế 1 chỉ?", 66, DORANGE, alpha=k1)
    seg_bar(d, 1230, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, lu, b, e = (sc[k] for k in ("hook", "do", "dapan", "luc", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + ts, "tap") for ts in T_S]
    out += [(da["t0"] + 0.15, "ding"), (lu["t0"] + lu["M"][1] + 0.1, "tap"), (b["t0"] + 2.0, "buzz"),
            (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l10-newton3-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Định luật III Newton · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai lực kế móc vào nhau", draw=s_hook, tail=0.3, caps=[
   ("Một tay giữ, một tay kéo.", 3.4),
   ("Dừng lại, tự đoán.", 5.3)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Kéo nhẹ, vừa, rồi mạnh.", 3.2),
   ("Đọc cả hai số.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.9, caps=[
   ("Lực kế 1 cũng chỉ 2,0 N.", 3.0),
   ("Kim luôn đổi cùng nhau.", 3.0)]),
 dict(key="luc", title="Lực nào lên vật nào?", draw=s_luc, tail=0.4, caps=[
   ("Mỗi lực kế đo lực lên nó.", 3.4),
   ("Hai lực đặt lên hai vật.", 3.0)]),
 dict(key="bay", title="Bẫy: kéo giật", draw=s_bay, tail=0.4, caps=[
   ("Kéo giật thật mạnh.", 3.4),
   ("Hai kim rung cùng nhau.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Coi lực kế rất nhẹ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Thử tính, rồi chọn đáp án.", 4.9)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
