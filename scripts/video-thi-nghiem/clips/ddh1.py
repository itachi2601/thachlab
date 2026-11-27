# Clip: tn-l11-daodongdieuhoa-01 - Con lac lo xo TREO DUNG: keo xuong roi tha (9/11/2026, L11 Ch.1;
#       dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu >= 55 px, Du doan K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-daodongdieuhoa-01.json (_kiem_so() doi chieu):
#   tham_so: A = 5 cm (2-10), T = 1 s (0,5-3); mo_hinh x = A.cos(2.pi.t/T); gia_thiet: bo qua ma sat, tha o bien duong.
#   so_lieu_mau (t s, x cm): 0 5 ; 0,25 0 ; 0,5 -5 ; 0,75 0 ; 1 5. Chieu duong huong xuong.
# DOI CA Du doan (27/11): ca cu "vat qua lai quanh moc nao" da co dap an trong hop exp ngay tren video.
#   Ca moi: keo xuong 5 cm, tha -> vat len cao nhat toi dau? -> 5 cm tren cho vat dung yen (x = -5, t = 0,5 s);
#   nhieu = moc lo xo chua gian (hien_tuong_hay_sai[0]), cho dung yen, 10 cm. Do gian khi dung yen KHONG co trong kho
#   -> moc "lo xo chua gian" khong ghi so.
# Bay = hien_tuong_hay_sai[0]: VTCB la cho lo xo chua gian.
# Thu nghi (= cau_chot khung web): cung lo xo (T = 1 s), keo xuong 3 cm, luc t = 1,5 s vat o dau? -> 3 cm tren VTCB
#   (buoc chua chieu: 1,5 s = T + T/2). Nhieu: cho tha (3 cm duoi), O, moc lo xo chua gian.
from engine import *

AMP, PER = 5.0, 1.0
ROWS = [(0.0, 5), (0.25, 0), (0.5, -5), (0.75, 0), (1.0, 5)]      # so_lieu_mau
def xof(tau): return AMP * math.cos(2 * math.pi * tau / PER)
def num(v):
    s = f"{v:g}".replace(".", ",")
    return s.replace("-", "−")
def tlab(tt): return "0" if tt == 0 else f"{tt:g}".replace(".", ",")
DGREEN = (21, 110, 55); DRED = (185, 28, 28); BLOCK = (59, 130, 246); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-daodongdieuhoa-01.json")))
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["A"]["mac_dinh"] == AMP and ts["T"]["mac_dinh"] == PER and ts["A"]["min"] <= 3 <= ts["A"]["max"]
    assert [(r[2], r[3]) for r in k["so_lieu_mau"]["hang"]] == [(a, float(b)) for a, b in ROWS]
_kiem_so()

# ---------------- con lac treo (khung nguon 1080x1920; vung thay y 200..1690) ----------------
SX = 330                       # truc lo xo
BEAM = 250                     # mat duoi gia treo
OY, PC = 820, 40               # VTCB o y 820; 40 px/cm; chieu duong huong XUONG
NAT = 500                      # moc lo xo chua gian (tam vat khi lo xo chua gian) - khong ghi so
BW, BH = 120, 80
def py(xcm): return OY + xcm * PC

def spring(d, y0, y1, col, n=14, amp=26, w=5, x=SX):
    lead = 16; pts = [(x, y0), (x, y0 + lead)]
    L = (y1 - lead) - (y0 + lead)
    for i in range(1, 2 * n):
        pts.append((x + (amp if i % 2 else -amp), y0 + lead + L * i / (2 * n)))
    pts += [(x, y1 - lead), (x, y1)]
    d.line(pts, fill=col, width=w, joint="curve")

def hdash(d, y, x0, x1, col, w=4, dash=18, gap=12):
    x = x0
    while x < x1:
        d.line([(x, y), (min(x1, x + dash), y)], fill=col, width=w); x += dash + gap

def rig(d, xcm, a=1.0, cy=None, ab=1.0):
    """cy: ghi de tam vat (px); ab: do hien cua vat (0 = lo xo chua treo vat, dau lo xo o cy - BH/2)."""
    c = lambda col: A(col, a)
    d.rectangle([170, BEAM - 26, 490, BEAM], fill=c((205, 200, 190)), outline=c(NAVY), width=3)
    for k in range(9):
        xx = 180 + k * 36; d.line([(xx, BEAM - 26), (xx + 22, BEAM - 4)], fill=c(NAVY), width=2)
    if cy is None: cy = py(xcm)
    spring(d, BEAM, cy - BH / 2, c(NAVY))
    if ab <= 0.02: return
    card(d, (SX - BW / 2, cy - BH / 2, SX + BW / 2, cy + BH / 2), fill=A(BLOCK, a * ab), outline=A(NAVY, a * ab), r=12, w=4)
    d.line([(SX + BW / 2, cy), (RX - 12, cy)], fill=A(RED, a * ab), width=5)          # kim chi vi tri tam vat, toi sat thuoc

def marks(d, a=1.0, lab_o="vật đứng yên", lab_n="lò xo chưa giãn", x_lab=560):
    """Hai moc cung kieu (net dut xam, chu cung co)."""
    for y, lab in ((NAT, lab_n), (OY, lab_o)):
        hdash(d, y, 160, 500, A(GRAY, a), w=4)
        if lab: text(d, (x_lab, y), lab, 56, INK, anchor="lm", alpha=a)

RX = 600                                                     # thuoc doc: x = 600..640
def ruler(d, a=1.0):
    c = lambda col: A(col, a)
    d.rectangle([RX, py(-6), RX + 40, py(6)], fill=c((250, 240, 200)), outline=c(NAVY), width=2)
    for k in range(-6, 7):
        L = 26 if k % 5 == 0 else 14
        d.line([(RX, py(k)), (RX + L, py(k))], fill=c(NAVY), width=3)
    for k, s in ((-5, "−5"), (0, "0"), (5, "+5")):
        text(d, (RX + 60, py(k)), s, 56, NAVY, anchor="lm", alpha=a)
    text(d, (RX + 160, py(6) - 10), "x (cm) ↓", 56, NAVY, anchor="lm", alpha=a)

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.8, cx + pw / 2, cy + size * 0.8), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    """Thanh dem lien khoi, tat lan luot tu PHAI sang TRAI; cao 76 px."""
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); wseg = 820 / n
    for i in range(n):
        x = 130 + i * wseg
        if i < on: card(d, (x, y, x + wseg - 14, y + 76), fill=A(col, a), r=16)
        else: card(d, (x, y, x + wseg - 14, y + 76), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    kh = ease((t - 0.6) / 0.8)                               # treo vat: tam vat tu moc lo xo chua gian xuong cho dung yen
    k = ease((t - 2.0) / 1.0)                                # tay keo vat xuong 5 cm
    rig(d, 0, cy=lerp(NAT, OY, kh) + AMP * PC * k, ab=appear(t, 0.6, 0.3))
    marks(d)
    if k > 0.1:
        arrow(d, (SX - BW / 2 - 40, OY), (SX - BW / 2 - 40, py(AMP * k) - 4), ORANGE, w=7, head=22)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1100 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 64, "DỰ ĐOÁN", 56, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 160), "Kéo xuống 5 cm rồi thả,", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 235), "bỏ qua ma sát.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 330), "Vật lên cao nhất tới đâu?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 440, t, M[1] + 0.4, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh (quay cham x4, dung o moi moc 0,25 s) ----------------
REL, RUN, PAUSE = 0.6, 1.0, 0.7
def tau_do(v):
    """-> (thoi gian that, so hang bang da ghi, dang dung o moc?)"""
    if v < REL: return 0.0, 1, True
    u = v - REL; tau = 0.0; rows = 1
    for i in range(1, 5):
        if u < RUN: return tau + 0.25 * u / RUN, rows, False
        u -= RUN; tau = 0.25 * i; rows = i + 1
        if i < 4 and u < PAUSE: return tau, rows, True
        if i < 4: u -= PAUSE
    return tau, rows, True

def table(d, rows, y0=1150):
    card(d, (30, y0, 1050, y0 + 220), fill=WHITE, outline=NAVY, r=22, w=3)
    d.line([(30, y0 + 110), (1050, y0 + 110)], fill=LIGHT, width=3)
    text(d, (130, y0 + 55), "t (s)", 56, NAVY); text(d, (130, y0 + 165), "x (cm)", 56, NAVY)
    for i in range(5):
        tt, xx = ROWS[i]; cx = 330 + i * 170
        text(d, (cx, y0 + 55), tlab(tt), 58, INK)
        if i < rows: text(d, (cx, y0 + 165), num(xx) if xx <= 0 else "+" + num(xx), 58, DORANGE)

def s_do(img, d, t, sc):
    tau, rows, hold = tau_do(t)
    xb = xof(tau)
    marks(d, 1.0, lab_o=None, lab_n=None)
    ruler(d)
    if t >= REL:                                             # vet cam: vung vat da quet tren thuoc
        lo = AMP if tau == 0 else min(AMP, xof(min(tau, PER / 2)))
        d.rectangle([RX - 16, py(lo) - 3, RX - 4, py(AMP) + 3], fill=A(ORANGE, 0.8))
    rig(d, xb)
    table(d, rows)
    pill(d, 230, 1470, "chậm ×4", 56, WHITE, ORANGE)
    pill(d, 750, 1470, f"t = {tlab(round(tau, 2)) if hold else vn2(tau)} s", 56, WHITE, NAVY)

def vn2(v): return f"{v:.2f}".replace(".", ",")

# ---------------- canh 3: Ket qua + rut ra + chua noi duoc ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    xb = xof(t / 4.0)                                        # van chay quay cham x4
    marks(d, 1.0, lab_n="chưa giãn", lab_o="đứng yên", x_lab=720)
    ruler(d)
    d.rectangle([RX - 16, py(-AMP) - 3, RX - 4, py(AMP) + 3], fill=A(ORANGE, 0.8))
    rig(d, xb)
    k1 = appear(t, 2.2, 0.45)
    if k1 > 0:
        card(d, (40, 1110, 1040, 1230), fill=A((255, 247, 237), k1), outline=A(ORANGE, k1), r=24, w=5)
        text(d, (W / 2, 1170), "Cao nhất: x = −5 cm", 60, DORANGE, alpha=k1)
    k2 = appear(t, M[1] - 0.05, 0.45)
    if k2 > 0:
        card(d, (40, 1260, 1040, 1380), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=24, w=5)
        text(d, (W / 2, 1320), "Chỗ đứng yên = VTCB O", 60, DGREEN, alpha=k2)
    k3 = appear(t, M[2] - 0.05, 0.45)
    if k3 > 0:
        card(d, (40, 1410, 1040, 1660), fill=A(WHITE, k3), outline=A(NAVY, k3), r=24, w=5)
        text(d, (W / 2, 1460), "Chưa nói được", 58, NAVY, alpha=k3)
        text(d, (80, 1540), "• Ma sát: đã bỏ qua", 56, INK, anchor="lm", alpha=k3)
        text(d, (80, 1615), "• Mới thử A = 5 cm", 56, INK, anchor="lm", alpha=appear(t, M[2] + 2.5, 0.4))

# ---------------- canh 4: Bay - VTCB la cho lo xo chua gian ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    rig(d, 1.5 * math.sin(2 * math.pi * t / 3.0))            # dao dong nho quanh O (khong dung hinh)
    marks(d, 1.0, lab_o="đứng yên (O)")
    y0 = 1110
    card(d, (40, y0, 1040, y0 + 150), fill=(254, 242, 242), outline=DRED, r=24, w=5)
    text(d, (W / 2, y0 + 75), "✗ VTCB: chỗ lò xo chưa giãn", 58, DRED)
    kc = appear(t, M[1] - 0.1, 0.4)                          # nhip 2 cach nhip 1 >= 3 s
    if kc > 0:
        x = SX + BW / 2 + 90
        arrow(d, (x, NAT + 6), (x, OY - 8), A(ORANGE, kc), w=7, head=22)
        text(d, (x + 24, (NAT + OY) / 2), "đã giãn", 56, DORANGE, anchor="lm", alpha=kc)
        card(d, (40, y0 + 190, 1040, y0 + 340), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=24, w=5)
        text(d, (W / 2, y0 + 265), "✓ VTCB thấp hơn", 58, DGREEN, alpha=kc)

# ---------------- canh 5: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    if t < 0.15: return
    card(d, (40, 215, 1040, 1585), fill=WHITE, outline=ORANGE, w=6)
    pill(d, W / 2, 280, "THỬ NGHĨ", 56, WHITE, ORANGE)
    bx, b0, oy, pc = 300, 380, 640, 30                       # hinh nho: keo xuong 3 cm, khong ve vi tri luc 1,5 s
    d.rectangle([200, b0 - 22, 400, b0], fill=(205, 200, 190), outline=NAVY, width=3)
    cy = oy + 3 * pc
    spring(d, b0, cy - 32, NAVY, n=10, amp=22, w=4, x=bx)
    card(d, (bx - 50, cy - 32, bx + 50, cy + 32), fill=BLOCK, outline=NAVY, r=10, w=3)
    hdash(d, oy, 160, 440, GRAY, w=4)
    text(d, (470, oy), "đứng yên", 56, INK, anchor="lm")
    arrow(d, (bx + 90, oy + 4), (bx + 90, cy - 4), ORANGE, w=6, head=18)
    text(d, (bx + 116, cy + 20), "kéo 3 cm", 56, DORANGE, anchor="lm")
    text(d, (W / 2, 900), "Cùng lò xo, T = 1 s.", 60, INK)
    text(d, (W / 2, 985), "Kéo xuống 3 cm rồi thả.", 60, INK)
    text(d, (W / 2, 1100), "Lúc t = 1,5 s,", 64, DORANGE)
    text(d, (W / 2, 1185), "vật ở đâu?", 64, DORANGE)
    seg_bar(d, 1320, t, 0.8, sc["T"] - 0.2, ORANGE)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + REL, "tap")]
    out += [(do["t0"] + REL + i * RUN + (i - 1) * PAUSE, "tick") for i in (1, 2, 3, 4)]
    out += [(da["t0"] + 0.5, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-daodongdieuhoa-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Dao động điều hoà · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Treo vật vào lò xo", draw=s_hook, tail=0.3, caps=[
   ("Treo vật rồi kéo xuống.", 4.4),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thả tay, ghi li độ mỗi 0,25 s.", 4.4),
   ("Chiều dương hướng xuống.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Hai đầu cách đều chỗ đứng yên.", 4.2),
   ("Không chạm mốc chưa giãn.", 4.4),
   ("Mới thử một biên độ.", 4.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Bẫy khi treo thẳng đứng.", 3.6),
   ("Nhìn lại hai mốc.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])
