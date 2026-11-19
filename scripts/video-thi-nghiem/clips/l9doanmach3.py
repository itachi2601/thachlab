# Clip: tn-l9-doanmach-03 - Thao mot bong den trong mach noi tiep va song song (lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-doanmach-03.json (_kiem_so() doi chieu ca mo_hinh):
#   U = 3 V ; R bong = 6 Ω ; so_lieu_mau: noi tiep 0,25 A -> thao mot bong 0 ; song song 0,5 A -> 0,5 A (so minh hoa).
# KHTN 9: chi dung I nhu nhau (noi tiep), moi nhanh nhan du U (song song), I = I1 + I2 (bai nay) ; khong P = UI.
# Du doan (K10, khong nut A-D): thao Đ1 o ca hai mach, ampe kế o Đ2 chi bao nhieu? -> noi tiep 0 A, song song van 0,5 A.
#   Khac Cau 6 cua bai (2 bong 220 V song song, hoi do sang) va Du doan mo bai (day den Tet).
# Bay = hien_tuong_hay_sai[1] (bong dut van cho dong yeu qua). Khong dung [0] (= phuong an C Cau 6).
# Chua noi duoc: gia_thiet "dien tro bong coi khong doi" -> so that khi day toc nguoi.
# Thu nghi: ba bong nhu tren song song vao 3 V, thao mot bong -> ampe ke mach chinh 2 x 0,5 = 1,0 A (ghi trong ghi_chu kho,
#   khong hien tren man). Khac Cau 4 (ba bong noi tiep 0,3 A).
from engine import *

U, RB = 3, 6
NT = (0.25, 0.0)            # noi tiep: dong moi bong ; thao mot bong
SS = (0.5, 0.5)             # song song
def vn(x): return ("%g" % x).replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-doanmach-03.json")))
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["U"]["gia_tri"] == U and tp["R_b"]["gia_tri"] == RB
    hang = {r[0]: tuple(r[1:]) for r in k["so_lieu_mau"]["hang"]}
    assert hang["nối tiếp"] == NT and hang["song song"] == SS
    assert abs(U / (2 * RB) - NT[0]) < 1e-9 and abs(U / RB - SS[0]) < 1e-9          # mo_hinh
    assert "1,0 A" in k["so_lieu_mau"]["ghi_chu"] and abs(2 * SS[1] - 1.0) < 1e-9     # ca chot
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); WIRE = (40, 48, 80); GLOW = (250, 204, 21)

# ---------------- mach dien ----------------
XL, XR = 150, 930
def rails(y0, kind):
    y1 = y0 + 100; y2 = y0 + 215; y3 = y0 + 320
    return y1, (y2 if kind == "ss" else None), y3
def bulbs(y0, kind):
    y1, y2, y3 = rails(y0, kind)
    return ({"Đ1": (330, y1), "Đ2": (540, y1)}, (750, y1)) if kind == "nt" else ({"Đ1": (540, y1), "Đ2": (440, y2)}, (660, y2))

def battery(d, x, y):
    d.line([(x - 15, y - 22), (x - 15, y + 22)], fill=WIRE, width=10)          # cuc am: ngan, day
    d.line([(x + 15, y - 40), (x + 15, y + 40)], fill=WIRE, width=4)           # cuc duong: dai, manh
    text(d, (x - 40, y - 46), "−", 44, WIRE); text(d, (x + 44, y - 50), "+", 44, WIRE)
    text(d, (x, y + 58), "3 V", 40, INK)

# Chieu dong: ra tu cuc + (ben phai pin) -> sang phai -> len canh phai -> sang trai tren cac thanh ngang -> xuong canh trai.
PLUS_SIDE = +1   # cuc + o ben phai pin
def _kiem_chieu():
    # canh phai: dong di len (dy < 0) ; thanh tren: sang trai (dx < 0) ; canh trai: xuong (dy > 0) -- dung voi PLUS_SIDE = +1
    assert PLUS_SIDE == +1
_kiem_chieu()

def circuit(d, y0, kind, rm=0.0, broken=False, a_on=True):
    """rm: 0 = Đ1 dang lap ; >0 = Đ1 dang/da thao (0..1 hoat canh nhac len). broken: Đ1 con trong đui nhung dut day toc."""
    y1, y2, y3 = rails(y0, kind)
    bl, am = bulbs(y0, kind)
    opened = rm > 0 or broken
    on2 = not (opened and kind == "nt")                     # Đ2 con dong?
    on1 = not opened
    card(d, (60, y0, 1020, y0 + 400), fill=WHITE, outline=LIGHT, w=3)
    text(d, (90, y0 + 40), "Nối tiếp" if kind == "nt" else "Song song", 42, NAVY, anchor="lm")
    R = 34
    gaps = {1: [], 2: []}                                   # cac khoang ho tren moi thanh (bong, ampe ke)
    for nm, (x, y) in bl.items(): gaps[1 if y == y1 else 2].append((x - R, x + R))
    gaps[1 if am[1] == y1 else 2].append((am[0] - R, am[0] + R))
    for r, yy in ((1, y1), (2, y2)):
        if yy is None: continue
        xs = [XL] + [v for g in sorted(gaps[r]) for v in g] + [XR]
        for i in range(0, len(xs), 2): d.line([(xs[i], yy), (xs[i + 1], yy)], fill=WIRE, width=5)
    d.line([(XL, y1), (XL, y3)], fill=WIRE, width=5); d.line([(XR, y1), (XR, y3)], fill=WIRE, width=5)
    if y2 is not None:
        for x in (XL, XR): dot(d, x, y2, 9, WIRE)
    # thanh duoi: khoa K (dong) + pin
    xb = 560
    d.line([(XL, y3), (300, y3)], fill=WIRE, width=5); d.line([(300, y3), (370, y3 - 4)], fill=WIRE, width=5)
    dot(d, 300, y3, 8, WIRE); dot(d, 372, y3, 8, WIRE); text(d, (336, y3 + 46), "K", 40, INK)
    d.line([(372, y3), (xb - 15, y3)], fill=WIRE, width=5); d.line([(xb + 15, y3), (XR, y3)], fill=WIRE, width=5)
    d.rectangle([xb - 14, y3 - 45, xb + 14, y3 + 45], fill=WHITE)
    battery(d, xb, y3)
    # bong
    for nm, (x, y) in bl.items():
        lift, al = 0.0, 1.0
        if nm == "Đ1" and rm > 0: lift = 70 * ease(rm); al = 1 - ease(rm)
        d.line([(x - R, y), (x - R + 6, y)], fill=WIRE, width=5); d.line([(x + R - 6, y), (x + R, y)], fill=WIRE, width=5)
        dot(d, x - R, y, 7, WIRE); dot(d, x + R, y, 7, WIRE)                     # hai tiep diem cua đui
        lit = (on1 if nm == "Đ1" else on2) and a_on
        b = (0.45 if kind == "nt" else 1.0) if lit else 0.0                     # noi tiep mo, song song ro
        yy = y - lift
        if b > 0 and al > 0:
            for k in range(5, 0, -1):
                rr = R + 8 * k * (0.6 + 0.8 * b)
                d.ellipse([x - rr, yy - rr, x + rr, yy + rr], fill=A(GLOW, 0.13 * b * al))
        if al > 0.02:
            d.ellipse([x - R, yy - R, x + R, yy + R], fill=A(WHITE if b == 0 else (255, 250, 205), al), outline=A(WIRE, al), width=5)
            c = R * 0.7
            if nm == "Đ1" and broken:
                d.line([(x - c, yy - c), (x - 6, yy - 6)], fill=A(WIRE, al), width=4); d.line([(x + 8, yy + 8), (x + c, yy + c)], fill=A(WIRE, al), width=4)
                d.line([(x - c, yy + c), (x + c, yy - c)], fill=A(WIRE, al), width=4)
            else:
                d.line([(x - c, yy - c), (x + c, yy + c)], fill=A(WIRE, al), width=4); d.line([(x - c, yy + c), (x + c, yy - c)], fill=A(WIRE, al), width=4)
            text(d, (x, yy - R - 30), nm, 40, INK, alpha=al)
    # ampe ke + so chi (dong bo voi trang thai)
    x, y = am
    d.ellipse([x - R, y - R, x + R, y + R], fill=WHITE, outline=WIRE, width=5); text(d, (x, y), "A", 40, WIRE)
    val = (NT if kind == "nt" else SS)[1 if opened else 0]
    s = vn(val) + " A"
    bw = tw(d, s, F(46)) + 40
    card(d, (x + R + 14, y - 32, x + R + 14 + bw, y + 32), fill=NAVY, r=14)
    text(d, (x + R + 14 + bw / 2, y), s, 46, (253, 224, 71))
    # mui ten chieu dong (chi khi co dong), w=7 head=20, dai >= 70 px
    if a_on and on2:
        AR = ORANGE
        arrow(d, (XR + 26, y3 - 30), (XR + 26, (y2 if y2 else y1) + 40), AR, w=7, head=20)     # canh phai: len
        arrow(d, (XL - 26, (y2 if y2 else y1) + 30), (XL - 26, y3 - 40), AR, w=7, head=20)     # canh trai: xuong
        if kind == "nt":
            arrow(d, (480, y1 - 70), (390, y1 - 70), AR, w=7, head=20)                       # thanh tren: sang trai
        else:
            arrow(d, (380, y2 + 50), (230, y2 + 50), AR, w=7, head=20)                       # nhanh Đ2: sang trai
            if on1: arrow(d, (860, y1 - 30), (720, y1 - 30), AR, w=7, head=20)               # nhanh Đ1: sang trai
    return opened

# ---------------- canh 1: Du doan ----------------
Y_NT, Y_SS = 270, 690
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, Y_NT, "nt"); circuit(d, Y_SS, "ss")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1110 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 54), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 160), "Tháo bóng Đ1 ở cả hai mạch.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 235), "Ampe kế ở Đ2 chỉ bao nhiêu?", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 330), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 405, 940, y0 + 419], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 405, 140 + 800 * (1 - p), y0 + 419], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T_NT, T_SS = 1.2, 5.6       # luc thao Đ1 o tung mach (giay trong canh)
def rm_at(t, t0): return 0.0 if t < t0 else max(1e-3, clamp((t - t0) / 0.7))

def table(d, y, n_nt, n_ss):
    card(d, (60, y, 1020, y + 330), fill=WHITE, outline=NAVY, w=4)
    text(d, (W / 2, y + 45), "Dòng qua Đ2 (A)", 40, INK)
    xs = (230, 560, 850)
    text(d, (xs[1], y + 105), "lắp cả hai", 40, MUTED, bold=False); text(d, (xs[2], y + 105), "tháo Đ1", 40, MUTED, bold=False)
    d.line([(90, y + 140), (990, y + 140)], fill=LIGHT, width=4)
    for i, (nm, v, n) in enumerate((("Nối tiếp", NT, n_nt), ("Song song", SS, n_ss))):
        yy = y + 195 + i * 85
        text(d, (xs[0], yy), nm, 42, NAVY)
        text(d, (xs[1], yy), vn(v[0]), 46, INK)
        if n: text(d, (xs[2], yy), vn(v[1]), 46, DGREEN)

def do_state(t):
    r1, r2 = rm_at(t, T_NT), rm_at(t, T_SS)
    return r1, r2, t >= T_NT + 1.0, t >= T_SS + 1.0

def s_do(img, d, t, sc):
    r1, r2, n1, n2 = do_state(t)
    circuit(d, Y_NT, "nt", rm=r1); circuit(d, Y_SS, "ss", rm=r2)
    table(d, 1120, n1, n2)

def _kiem_dong_bo():
    """Moi 0,05 s: so ampe ke doi dung luc Đ1 roi đui ; hang bang chi hien sau khi mach da doi."""
    bad = []; t = 0.0
    while t < 10.0:
        r1, r2, n1, n2 = do_state(t)
        if n1 and r1 == 0: bad.append((round(t, 2), "hang noi tiep truoc khi thao"))
        if n2 and r2 == 0: bad.append((round(t, 2), "hang song song truoc khi thao"))
        if (r1 > 0) != (t >= T_NT): bad.append((round(t, 2), "thao noi tiep lech moc"))
        t += 0.05
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=40):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    circuit(d, Y_NT, "nt", rm=1.0); circuit(d, Y_SS, "ss", rm=1.0)
    pill(d, "ĐÁP ÁN: nối tiếp 0 A, song song 0,5 A", 1140, appear(t, 0.15, 0.4))
    k1 = appear(t, M[0] - 0.1, 0.5)
    if k1 > 0:
        card(d, (60, 1215, 1020, 1470), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        text(d, (W / 2, 1285), "Nối tiếp: hở một chỗ, hở cả mạch", 46, DGREEN, alpha=k1)
        k2 = appear(t, M[1] - 0.1, 0.5)
        text(d, (W / 2, 1395), "Song song: Đ2 vẫn nhận đủ 3 V", 46, DGREEN, alpha=k2)

# ---------------- canh 4: Bay ; chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    ks = clamp((t - 1.8) / 0.4); kg = appear(t, 2.5, 0.4)
    circuit(d, Y_NT, "nt", broken=True)
    text(d, (330, Y_NT + 190), "dây tóc đứt", 40, DRED)
    y = 720
    if a1 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        for j, q in enumerate(("“Bóng đứt vẫn cho dòng yếu qua”",)):
            f = F(46); lw = tw(d, q, f); yy = y + 180 + j * 70
            text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 300), "✓ Ampe kế chỉ 0 A: mạch hở", 46, DGREEN, alpha=a1 * kg)
    if k3 > 0:
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 200), "Dây tóc nguội: dòng có đúng thế?", 46, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Nối tiếp: hỏng một, tắt hết.", 48, DGREEN, alpha=k0)
    text(d, (W / 2, 450), "Song song: nhánh khác vẫn sáng.", 48, DGREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1330), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Ba bóng như trên mắc song song,", "nguồn 3 V. Tháo một bóng:", "ampe kế mạch chính chỉ bao nhiêu?")):
        text(d, (W / 2, 790 + j * 78), s, 46, INK, alpha=kq)
    kh = appear(t, M[0] + 4.2, 0.5)
    if kh > 0:
        card(d, (90, 1060, 990, 1290), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1115), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1215), "Đếm nhánh còn sáng", 44, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + T_NT, "tap"), (do["t0"] + T_SS, "tap")]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.8, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-doanmach-03", header="KHTN 9 · THÍ NGHIỆM", footer="Đoạn mạch nối tiếp, song song · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tháo một bóng đèn", draw=s_hook, tail=0.3, caps=[
   ("Hai bóng giống nhau, nguồn 3 V.", 3.2),
   ("Tự trả lời trước khi xem.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Tháo Đ1 ở mạch nối tiếp.", 4.4),
   ("Tháo Đ1 ở mạch song song.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Nối tiếp chỉ có một đường.", 4.2),
   ("Song song: mỗi nhánh riêng.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy khi bóng đứt dây tóc.", 5.0),
   ("Câu còn bỏ ngỏ.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 8.7)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
