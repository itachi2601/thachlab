# Clip: tn-l10-klr-apsuat-03 - Chai nhua duc lo theo do sau: tia o lo nao phun manh nhat (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-klr-apsuat-03.json:
#   so_lieu_mau (h cm, p du Pa, v m/s): 5 500 1,0 ; 10 1000 1,41 ; 15 1500 1,73 (g = 10, rho = 1000, so tinh tu mo hinh).
# Hinh: 16 px/cm ca hai truc ; tia la parabol nem ngang voi v kho, roi toi khay (de cao 20 cm de tia lo sau nhat
#   cung xa nhat) ; mui ten tai mieng lo dai ti le v.
# Du doan (K10, khong nut): mo ca ba lo, tia lo nao phun manh nhat ngay tai mieng lo? (dap an: lo duoi cung).
# KHONG tra loi san Cau 3 muc II.4 bai (chenh 12 m) -> khong tinh hieu ap suat giua hai lo, khong ghi cong thuc.
# Bay = hien_tuong_hay_sai[0] "nuoc chi ep xuong day" -> chai 2 (nhin tu tren) bon tia ngang manh nhu nhau.
# Chot (ca tu suy, ghi_chu kho): mat nuoc cao them 5 cm, lo khong doi -> lo tren cung sau 10 cm, manh nhu lo giua
#   luc truoc (1000 Pa). Buoc chua chieu: do sau tinh tu mat nuoc moi. Khong goi y.
from engine import *

ROWS = [(5, 500, 1.0), (10, 1000, 1.41), (15, 1500, 1.73)]   # so_lieu_mau
G = 10.0
NOTE = (60, 64, 84); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128); DGREEN = (21, 110, 55)
WAT = (147, 197, 253); WAT_D = (37, 99, 235); BOT = (120, 140, 170); TAPE = (250, 214, 120); WOOD = (196, 150, 100)

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

# ---------------- bo cuc (16 px/cm) ----------------
PXC = 16
CX0, CX1 = 260, 404                    # than chai
MID = (CX0 + CX1) / 2
WS = 470                               # mat nuoc
YB = WS + 20 * PXC                     # day chai (cot nuoc 20 cm) = 790
TRAY = YB + 20 * PXC                   # khay (de cao 20 cm) = 1110
def yh(h): return WS + h * PXC

def bottle(d, a=1.0, tape=False, ws=WS):
    d.rectangle([CX0 - 10, YB, CX1 + 10, TRAY], fill=A(WOOD, a))                       # de
    d.rectangle([150, TRAY, 1040, TRAY + 26], fill=A((150, 155, 172), a))               # khay
    d.rectangle([CX0 + 3, ws, CX1 - 3, YB - 3], fill=A(WAT, 0.8 * a))
    d.line([(CX0 + 3, ws), (CX1 - 3, ws)], fill=A(WAT_D, a), width=4)
    sh = [(CX0, YB), (CX0, 350), (MID - 20, 292), (MID - 20, 256), (MID + 20, 256), (MID + 20, 292), (CX1, 350), (CX1, YB)]
    d.line(sh + [(CX0, YB)], fill=A(BOT, a), width=5, joint="curve")
    d.rectangle([MID - 26, 236, MID + 26, 258], fill=A((37, 99, 235), a))              # nap mo
    for h, _, _ in ROWS:
        y = yh(h); dot(d, CX1, y, 7, A(NAVY, a))
        if tape: d.rectangle([CX1 - 6, y - 18, CX1 + 16, y + 18], fill=A(TAPE, a))

def depth_marks(d, a=1.0, mat=True):
    if mat: text(d, (CX1 + 24, WS - 34), "mặt nước", 55, WAT_D, anchor="lm", alpha=a)
    for h, _, _ in ROWS:
        y = yh(h)
        for x in range(200, CX1 - 10, 22): d.line([(x, y), (x + 12, y)], fill=A(NOTE, a), width=3)
        text(d, (190, y), f"{h} cm", 55, INK, anchor="rm", alpha=a)
    text(d, (190, WS), "0", 55, INK, anchor="rm", alpha=a)

def jet(d, h, v, prog, a=1.0):
    """Tia nem ngang tu lo do sau h (cm), toc do v (m/s); prog 0..1 phan quang duong da phun toi."""
    y0 = yh(h); drop = (TRAY - y0) / PXC / 100; T = math.sqrt(2 * drop / G); pts = []
    for k in range(41):
        tau = T * k / 40 * prog
        pts.append((CX1 + v * tau * 100 * PXC, y0 + 0.5 * G * tau * tau * 100 * PXC))
    if prog > 0.01: d.line(pts, fill=A(WAT_D, 0.85 * a), width=9, joint="curve")

def mouth_arrow(d, v, h, a=1.0):
    y = yh(h) - 26
    arrow(d, (CX1 + 14, y), (CX1 + 14 + 140 * v, y), A(RED, a), w=7, head=18)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    bottle(d, tape=True); depth_marks(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1152 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 460), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 58, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 145), "Mở cả ba lỗ.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 222), "Tia lỗ nào phun mạnh nhất", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 298), "ngay miệng lỗ?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 352, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: tien hanh ----------------
OPEN, FLOW = 0.8, 1.6                    # boc bang dinh ; thoi gian tia phun toi khay (quay cham)
ROW_AT = [5.4 + 0.8 * i for i in range(3)]

def table(d, n, y0=1170, a=1.0, hi=-1):
    card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (260, y0 + 60), "h: độ sâu (cm)", 55, INK, alpha=a); text(d, (735, y0 + 60), "p: áp suất nước (Pa)", 55, RED, alpha=a)
    d.line([(70, y0 + 105), (1010, y0 + 105)], fill=A(LIGHT, a), width=4)
    for i in range(n):
        h, p, _ = ROWS[i]; y = y0 + 170 + i * 82
        if i == hi: d.rounded_rectangle([60, y - 36, 1020, y + 36], radius=16, fill=A((255, 237, 213), a))
        text(d, (260, y), str(h), 60, INK, alpha=a); text(d, (735, y), str(p), 60, RED, alpha=a)

def s_do(img, d, t, sc):
    bottle(d, tape=t < OPEN); depth_marks(d, mat=False)
    prog = ease((t - OPEN) / FLOW) if t > OPEN else 0.0
    for h, _, v in ROWS: jet(d, h, v, prog)
    ka = appear(t, OPEN + FLOW + 0.3, 0.4)
    if ka > 0:
        for h, _, v in ROWS: mouth_arrow(d, v, h, ka)
        text(d, (CX1 + 30, yh(5) - 90), "→ tốc độ ra", 55, RED, anchor="lm", alpha=ka)
    n = sum(1 for r in ROW_AT if t >= r)
    if n: table(d, n, hi=n - 1)

# ---------------- canh 3: dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    bottle(d); depth_marks(d, mat=False)
    for h, _, v in ROWS: jet(d, h, v, 1.0, 0.6); mouth_arrow(d, v, h, 1.0)
    ke = appear(t, 1.4, 0.5)
    if ke > 0: d.ellipse([CX1 - 30, yh(15) - 64, CX1 + 290, yh(15) + 30], outline=A(ORANGE, ke), width=6)
    card(d, (470, 250, 1040, 420), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (755, 300), "Lỗ dưới cùng,", 58, DGREEN)
    text(d, (755, 375), "sâu nhất", 58, DGREEN)
    kr = appear(t, M[1], 0.45)
    table(d, 3, a=1 - kr, hi=(2 if t > 2.6 else -1))
    if kr <= 0: return
    y0 = 1170 + (1 - kr) * 30
    card(d, (40, y0, 1040, y0 + 300), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
    pill(d, W / 2, y0 + 62, "RÚT RA", GREEN, kr)
    text(d, (W / 2, y0 + 170), "Càng sâu,", 62, INK, alpha=kr)
    text(d, (W / 2, y0 + 245), "áp suất nước càng lớn", 62, DGREEN, alpha=kr)

# ---------------- canh 4: bay (chai 2) + chua noi duoc ----------------
def top_view(d, a, prog):
    cx, cy, r = W / 2, 1290, 80
    L = 190 * prog
    for ang in (0, 90, 180, 270):
        u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
        if L > 2: d.line([(cx + u[0] * r, cy + u[1] * r), (cx + u[0] * (r + L), cy + u[1] * (r + L))], fill=A(WAT_D, 0.85 * a), width=10)
    dot(d, cx, cy, r, A(WAT, a), outline=A(BOT, a))
    text(d, (W / 2, 950), "chai 2, nhìn từ trên", 58, NAVY, alpha=a)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    k2 = appear(t, M[1], 0.45)
    top_view(d, k2, ease((t - M[1]) / 1.0))
    if a1 > 0:
        card(d, (40, 250, 1040, 470), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, 315, "BẪY", RED, a1)
        ks = clamp((t - M[1]) / 0.4); q = "“Nước chỉ ép xuống đáy chai”"; f = F(58); lw = tw(d, q, f); yy = 410
        text(d, (W / 2, yy), q, 58, mix(RED, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        kv = appear(t, M[1] + 3.0, 0.45) * a1
        if kv > 0:
            card(d, (40, 500, 1040, 640), fill=A((220, 252, 231), kv), outline=A(GREEN, kv), w=5)
            text(d, (W / 2, 570), "Nước ép ngang, như nhau", 58, DGREEN, alpha=kv)
    if k3 > 0:
        card(d, (40, 250, 1040, 640), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 320, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 445), "Mới thử với nước.", 60, INK, alpha=k3)
        text(d, (W / 2, 545), "Mực nước tụt dần: tia yếu đi?", 60, INK, alpha=k3)

# ---------------- canh 5: thu nghi ----------------
def s_end(img, d, t, sc):
    k = 1.0
    ws2 = WS - 5 * PXC
    bottle(d, ws=ws2); depth_marks(d, mat=False)
    d.line([(CX0 + 6, WS), (CX1 - 6, WS)], fill=NOTE, width=3)                       # muc cu (net mong)
    bx = CX1 + 30                                                                     # ngoac 5 cm (ben phai chai)
    d.line([(bx, ws2), (bx, WS)], fill=ORANGE, width=6)
    for y in (ws2, WS): d.line([(bx - 12, y), (bx + 12, y)], fill=ORANGE, width=6)
    text(d, (bx + 24, (ws2 + WS) / 2), "mặt nước +5 cm", 58, DORANGE, anchor="lm")
    card(d, (40, 1160, 1040, 1580), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1222, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 1320), "Tại miệng lỗ, lỗ trên cùng", 62, INK, alpha=k)
    text(d, (W / 2, 1400), "giờ mạnh như lỗ nào trước?", 64, DORANGE, alpha=k)
    seg_bar(d, 1470, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _kiem():
    """Tia: lo sau hon xa hon (khong gay nham) ; v kho = sqrt(2gh) ; p kho = rho.g.h."""
    bad = []; xs = []
    for h, p, v in ROWS:
        if abs(math.sqrt(2 * G * h / 100) - v) > 0.006 or abs(1000 * G * h / 100 - p) > 1e-6: bad.append(("kho", h))
        y0 = yh(h); drop = (TRAY - y0) / PXC / 100; xs.append(CX1 + v * math.sqrt(2 * drop / G) * 100 * PXC)
    if not (xs[0] < xs[1] < xs[2] <= 1040): bad.append(("tam xa", [round(x) for x in xs]))
    return bad

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + OPEN, "tap")]
            + [(da["t0"] + 0.1, "ding"), (da["t0"] + da["M"][1], "tap"), (b["t0"] + b["M"][1], "buzz"),
               (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-klr-apsuat-03", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Khối lượng riêng. Áp suất · thachlab.id.vn", scenes=[
 dict(key="hook", title="Chai nước đục ba lỗ", draw=s_hook, tail=0.3, caps=[
   ("Chai đầy nước.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Mở cả ba lỗ", draw=s_do, tail=0.4, caps=[
   ("Bóc băng dính, quay chậm.", 4.2),
   ("So tia ngay tại miệng lỗ.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Lỗ dưới cùng, sâu nhất: mạnh nhất.", 4.2),
   ("Càng sâu, áp suất nước càng lớn.", 4.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 3.0),
   ("Bốn lỗ cùng độ sâu.", 6.1),
   ("Chưa nói được.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự nghĩ.", 7.4)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("lệch:", _kiem() or "không")
