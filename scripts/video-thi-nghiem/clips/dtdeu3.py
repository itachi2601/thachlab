# Clip: tn-l11-dien-truong-deu-03 - Ong lech tia dien tu: quy dao parabol cua electron (lo L11, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-truong-deu-03.json (_kiem_so() doi chieu ca cong thuc mo_hinh):
#   so_lieu_mau (U V, v0 m/s, y mm): 0 2e7 0 ; 60 2e7 1,65 ; 120 2e7 3,30 (hai hang 60/120 V them vao kho 18/11 theo
#   cong B, "tinh tu mo hinh"). KHONG dung 91 V -> 2,5 mm (dap so bai mau), 45,5 V -> 1,25 mm (nhieu Thu suc), 182 V -> 5,0 mm (dap an
#   "Dien buoc" bai mau, va hang v0 4e7 -> 0,625 mm = dap an "Thu suc"). tham_so: L 0,05 m ; d 0,02 m (khoang cach
#   hai ban -> moi ban cach tam 10 mm). Clip KHONG hien v0, L, d bang so (de khong ghep thanh de bai mau).
# Ong lech tia that (Teltron): man huynh quang ke luoi nam GIUA hai ban -> chi thay quy dao trong vung hai ban, khong
#   ve doan sau ban (cau Tu kiem tra Bay 2 hoi "ra khoi ban di the nao").
# Cau hinh: ban DUOI (+), ban TREN (-) -> E huong LEN. Electron q < 0 -> F = qE huong XUONG, lech ve ban (+) (assert).
#   Khong dung cau hinh ban tren (+) vi dung y cau Tu kiem tra Bay 1 (tl37-q5). Khong dao cuc trong clip (dao cuc = q5).
# Truc doc phong to: 28 px/mm doc, 15 px/mm ngang (luoi ghi mm doc, chu "trục dọc phóng to").
# Du doan (K10): ban duoi (+), tren (-), tang U: tia lech ve dau? Dap an: xuong, ve ban (+).
# Bay = hien_tuong_hay_sai[0] "lech theo chieu duong suc". Chua noi duoc: moi doi U, chua doi v0.
# Thu nghi: U = 60 V (lech 1,65 mm khi vao giua) ; electron vao cach ban (+) 1,5 mm (gia dinh, ghi trong ghi_chu kho)
#   -> lech ve ban (+) 1,65 mm > 1,5 mm -> cham ban, khong ra duoc.
# Cong B: bo the "F nguoc chieu E" va bay "lech theo chieu E" (chep quy tac/tieu de Bay 1 cua bai) ; clip chi noi
#   "lech ve ban (+)". Bay moi (khong trong hien_tuong_hay_sai cua kho, do phien chinh chon): "Tang U, tia bay nhanh
#   hon nen it lech hon" - U hai ban khong doi v0 ; bang cho U tang thi lech tang.
# Assert chieu luc (F nguoc E) van giu trong ma.
from engine import *

ROWS = [(0, 0.0), (60, 1.65), (120, 3.3)]          # (U V, y mm) voi v0 = 2,0e7 m/s
def vn(x, nd=None):
    s = (f"{x:.{nd}f}" if nd is not None else (f"{x:g}"))
    return s.replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-dien-truong-deu-03.json")))
    hang = k["so_lieu_mau"]["hang"]; tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    for U, y in ROWS:
        assert any(r[0] == U and r[1] == 2e7 and r[2] == y for r in hang), (U, y)
    e, m, L, dd = (tp[s]["gia_tri"] for s in ("e", "m", "L", "d"))
    for U, y in ROWS:                                   # mo_hinh: y = eUL^2/(2 m d v0^2)
        assert abs(e * U * L ** 2 / (2 * m * dd * 4e14) * 1000 - y) < 0.005
    assert dd * 1000 / 2 == 10.0                        # moi ban cach tam 10 mm
    assert "1,5 mm" in k["so_lieu_mau"]["ghi_chu"] and ROWS[1][1] > 1.5   # thu nghi: cham ban
_kiem_so()

# ---------------- vat li: chieu E, chieu luc, chieu lech ----------------
# Toa do anh: +y huong XUONG. Ban duoi (+) o +y, ban tren (-) o -y.
PLUS_SIDE = +1                                         # ban (+) nam phia +y (duoi)
E_DIR = -PLUS_SIDE                                     # E tu ban (+) sang ban (-): huong len (-y)
Q_SIGN = -1                                            # electron
F_DIR = Q_SIGN * E_DIR                                 # F = qE
DEFL = F_DIR                                           # lech theo chieu luc
def _kiem_vat_li():
    assert E_DIR == -1 and F_DIR == +1                  # E len, F xuong
    assert F_DIR == -E_DIR                              # luc len electron NGUOC chieu E
    assert DEFL == PLUS_SIDE                            # lech ve ban duong
    for x in (0.25, 0.5, 1.0):                          # parabol: y ~ x^2
        assert abs(ypx(2.5, x * LPX) / ypx(2.5, LPX) - x * x) < 1e-9

GLOW = (34, 197, 94); GLOW_D = (21, 128, 61); SCREEN = (236, 248, 238); GRID = (196, 224, 202)
PLATE = (150, 156, 172); DRED = (185, 28, 28); DGREEN = (10, 80, 40)
XL, LPX = 170, 760                                     # ban tu x 170 den 930 (50 mm -> 15,2 px/mm)
VS = 28                                                # px / mm (truc doc)
def ypx(ymm, x):
    """Do lech (px, chieu +y) tai hoanh do x (px tu mep vao) khi do lech o mep ra la ymm."""
    return DEFL * ymm * VS * (x / LPX) ** 2
_kiem_vat_li()

def tube(d, yc, beams=(), cur=None, kcur=1.0, show_e=0.0, show_f=0.0, scale=True):
    """beams: list (ymm, mau) da ve xong ; cur: ymm cua tia dang chay, kcur 0..1 tien do."""
    top, bot = yc - 10 * VS, yc + 10 * VS
    d.rectangle([XL, top, XL + LPX, bot], fill=SCREEN)
    for k in range(-9, 10):
        y = yc + k * VS; d.line([(XL, y), (XL + LPX, y)], fill=GRID, width=2 if k % 2 else 3)
    for k in range(1, 10):
        x = XL + k * LPX / 10; d.line([(x, top), (x, bot)], fill=GRID, width=2)
    d.rectangle([XL - 6, top - 22, XL + LPX + 6, top], fill=PLATE, outline=NAVY, width=3)
    d.rectangle([XL - 6, bot, XL + LPX + 6, bot + 22], fill=PLATE, outline=NAVY, width=3)
    for k in range(6):
        x = XL + 70 + k * 125
        text(d, (x, top - 50), "−", 48, DRED); text(d, (x, bot + 52), "+", 48, BLUE)
    # sung dien tu
    d.rounded_rectangle([50, yc - 34, XL - 14, yc + 34], radius=10, fill=(90, 98, 120))
    d.line([(XL - 14, yc), (XL, yc)], fill=GLOW, width=6)
    if scale:
        for v in (0, 2, 4):
            y = yc + DEFL * v * VS
            d.line([(XL + LPX, y), (XL + LPX + 14, y)], fill=NAVY, width=3)
            text(d, (XL + LPX + 24, y), str(v), 38, INK, anchor="lm")
        text(d, (XL + LPX + 24, yc + DEFL * 6.4 * VS), "mm", 38, INK, anchor="lm")
        text(d, (XL + 18, yc - 8 * VS), "trục dọc phóng to", 36, MUTED, anchor="lm")
    for ymm, col in beams: _beam(d, yc, ymm, 1.0, col)
    if cur is not None: _beam(d, yc, cur, kcur, GLOW, head=True)
    if show_e > 0:                                     # E tu ban (+) sang ban (-)
        for x in (XL + 40, XL + 110):
            arrow(d, (x, yc + 7 * VS), (x, yc - 7 * VS), A(ORANGE, show_e), w=6, head=20) if E_DIR < 0 else None
        text(d, (XL + 75, yc - 8.4 * VS), "E", 44, ORANGE, alpha=show_e)
    if show_f > 0:
        xm = LPX * 0.55; yb = yc + ypx(2.5, xm)
        arrow(d, (XL + xm, yb), (XL + xm, yb + F_DIR * 130), A(PURPLE, show_f), w=7, head=22)
        text(d, (XL + xm + 40, yb + F_DIR * 100), "F", 46, PURPLE, anchor="lm", alpha=show_f)

def _beam(d, yc, ymm, k, col, head=False):
    n = max(2, int(60 * k)); pts = [(XL + LPX * k * i / (n - 1), yc + ypx(ymm, LPX * k * i / (n - 1))) for i in range(n)]
    d.line(pts, fill=col, width=6)
    if head: dot(d, pts[-1][0], pts[-1][1], 10, (220, 255, 220), outline=GLOW_D)

FAINT = (150, 200, 165)

# ---------------- canh 1: Du doan ----------------
YC = 620
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    tube(d, YC, cur=0.0, kcur=clamp((t - 0.4) / 1.0), scale=False)
    text(d, (110, YC + 80), "súng", 38, INK)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1020 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Bản dưới (+), bản trên (−).", "Tăng U: tia lệch về đâu?")):
        text(d, (W / 2, y0 + 190 + j * 80), s, 48, INK, alpha=a)
    text(d, (W / 2, y0 + 420), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 485, 940, y0 + 499], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 485, 140 + 800 * (1 - p), y0 + 499], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
RUN = 1.0                                             # giay tia chay het ban
def do_state(t, M):
    """-> (i hang dang chay, k tien do, so hang da ghi)."""
    starts = [0.5, 2.6, M[1] + 0.8]
    i = max(j for j, s in enumerate(starts) if t >= s) if t >= starts[0] else -1
    if i < 0: return -1, 0.0, 0
    k = clamp((t - starts[i]) / RUN)
    rows = i + (1 if t >= starts[i] + RUN + 0.2 else 0)
    return i, k, rows

def utable(d, y, n, hl=-1, ka=1.0, ratio=0.0):
    card(d, (40, y, 1040, y + 110 + 3 * 80), fill=WHITE, outline=NAVY, w=4)
    text(d, (290, y + 52), "U (V)", 42, INK); text(d, (740, y + 52), "y ở mép bản (mm)", 42, INK)
    d.line([(70, y + 95), (1010, y + 95)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 140 + i * 80; U, ym = ROWS[i]
        if i == hl or (ratio > 0 and i >= 1):
            d.rounded_rectangle([60, yy - 34, 1020, yy + 34], radius=16, fill=A((255, 237, 213), max(ka, ratio)))
        text(d, (290, yy), vn(U), 44, INK); text(d, (740, yy), "0" if ym == 0 else vn(ym, 2), 44, BLUE)
    if ratio > 0:
        yy = y + 140 + 1.5 * 80
        arrow(d, (110, yy - 40), (110, yy + 40), A(ORANGE, ratio), w=5, head=14)
        text(d, (150, yy), "×2", 40, ORANGE, anchor="lm", alpha=ratio)
        arrow(d, (970, yy - 40), (970, yy + 40), A(ORANGE, ratio), w=5, head=14)
        text(d, (930, yy), "×2", 40, ORANGE, anchor="rm", alpha=ratio)

def s_do(img, d, t, sc):
    M = sc["M"]; i, k, rows = do_state(t, M)
    card(d, (40, 260, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    beams = [(ROWS[j][1], FAINT) for j in range(max(0, i))]
    tube(d, YC, beams=beams, cur=ROWS[i][1] if i >= 0 else None, kcur=k)
    utable(d, 1030, rows, hl=rows - 1)
    if i >= 0:
        card(d, (330, 1410, 750, 1490), fill=(254, 242, 242), r=24)
        text(d, (540, 1450), "U = " + vn(ROWS[i][0]) + " V", 46, RED)

def _kiem_dong_bo():
    """Moi 0,05 s: hang bang chi hien sau khi tia chay het ban ; o U luon khop tia dang ve."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; M = sc["M"]; t = 0.0; bad = []
    while t < sc["T"]:
        i, k, rows = do_state(t, M)
        if rows > i + 1: bad.append((round(t, 2), "hang som"))
        if i >= 0 and rows == i + 1 and k < 1: bad.append((round(t, 2), "hang truoc khi tia toi mep"))
        t += 0.05
    if do_state(sc["T"] - 0.05, M)[2] != 3: bad.append("chua du 3 hang cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

YC2 = 700
def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN · Xuống, về bản (+)", 310, appear(t, 0.15, 0.4))
    tube(d, YC2, beams=[(ROWS[0][1], FAINT), (ROWS[1][1], FAINT), (ROWS[2][1], GLOW)])
    kr = appear(t, M[1] - 0.1, 0.45)
    utable(d, 1080, 3, ratio=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    tube(d, YC, beams=[(ROWS[1][1], FAINT), (ROWS[2][1], GLOW)], scale=False)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    y = 1030
    if a1 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 1.4) / 0.4)
        for j, q in enumerate(("“Tăng U, tia bay nhanh hơn", "nên ít lệch hơn”")):
            f = F(48); lw = tw(d, q, f); yy = y + 160 + j * 76
            text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)],
                       fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 335), "✓ U tăng thì lệch nhiều hơn", 46, DGREEN, alpha=a1 * appear(t, 2.0, 0.4))
    if k3 > 0:
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 200), "Mới đổi U. Còn yếu tố nào nữa?", 48, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: U = 60 V lech 1,65 mm ; vao cach ban (+) 1,5 mm -> co ra duoc?"""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Electron cong về bản (+)", 50, DGREEN, alpha=k0)
    text(d, (W / 2, 450), "theo parabol", 50, DGREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1440), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("U = 60 V: vào giữa, lệch 1,65 mm.", "Nếu vào cách bản (+) 1,5 mm,", "electron có ra khỏi hai bản?")):
        text(d, (W / 2, 790 + j * 80), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.2, 0.5)
    if kh > 0:
        card(d, (110, 1110, 970, 1380), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1170), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1280), "Vẽ thử đường đi của tia", 46, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + s, "tap") for s in (0.5, 2.6, do["M"][1] + 0.8)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-dien-truong-deu-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện trường đều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ống lệch tia điện tử", draw=s_hook, tail=0.3, caps=[
   ("Tia electron bay ngang giữa hai bản.", 3.4),
   ("Tự trả lời trước khi xem.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("U = 0 trước, rồi tăng U.", 4.6),
   ("Gấp đôi U, đọc độ lệch.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Đường cong giống vật ném ngang.", 4.2),
   ("U gấp đôi, độ lệch gấp đôi.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 4.4),
   ("Câu còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 7.8)]),
])

_b = _kiem_dong_bo(); assert not _b, _b

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
