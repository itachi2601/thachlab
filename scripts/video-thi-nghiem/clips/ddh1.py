# Clip: tn-l11-daodongdieuhoa-01 - Con lac lo xo TREO DUNG: vat di qua lai quanh moc nao (9/11/2026, L11 Ch.1)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-daodongdieuhoa-01.json:
#   tham_so: A = 5 cm (2-10), T = 1 s (0,5-3); mo_hinh x = A.cos(2.pi.t/T); gia_thiet: bo qua ma sat, tha o bien duong.
#   so_lieu_mau (t s, x cm): 0 5 ; 0,25 0 ; 0,5 -5 ; 0,75 0 ; 1 5 (khong hien li do giua cac moc).
#   hien_tuong_hay_sai[0]: VTCB la cho lo xo khong bien dang (treo thang dung thi khong phai) -> Du doan + Bay.
#   Do gian lo xo khi vat dung yen KHONG co trong kho -> ve moc "lo xo chua gian" khong ghi so, ngoai thuoc.
#   Cau chot: keo xuong 3 cm (A trong khoang tham_so, chua tung hien) -> vat len cao nhat toi dau? (3 cm tren VTCB,
#   khong hien; phan xa sai: toi moc lo xo chua gian). Goi y: moc giua van la cho vat dung yen.
# Dan canh rieng (khac motadddh1 ray ngang): lo xo TREO DUNG, chieu duong huong xuong, thuoc doc canh vat,
#   bang t / x ben phai; quay cham x4 (0,25 s that = 1,0 s video), dung hinh o moi moc ghi so.
# Canh: Du doan (K10: chi cau hoi + hinh, hai moc cung kieu) -> Tien hanh -> Dap an + Rut ra -> Bay roi Chua noi duoc
#       -> Chot + cau hoi tu nho lai (goi y tre 2,5 s, ve qua body).
from engine import *

AMP, PER = 5.0, 1.0
ROWS = [(0.0, 5), (0.25, 0), (0.5, -5), (0.75, 0), (1.0, 5)]      # so_lieu_mau
def xof(tau): return AMP * math.cos(2 * math.pi * tau / PER)
def num(v):
    s = f"{v:g}".replace(".", ",")
    return s.replace("-", "−")
def tlab(tt): return "0" if tt == 0 else f"{tt:g}".replace(".", ",")
DGREEN = (21, 110, 55); DRED = (185, 28, 28); BLOCK = (59, 130, 246)

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

def marks(d, a=1.0, lab_o="vật treo đứng yên", lab_n="lò xo chưa giãn"):
    """Hai moc cung kieu (net dut xam, chu cung co) - khong goi y moc nao la dap an."""
    for y, lab in ((NAT, lab_n), (OY, lab_o)):
        hdash(d, y, 160, 500, A(GRAY, a), w=4)
        if lab: text(d, (690, y), lab, 40, INK, anchor="lm", alpha=a)

RX = 600                                                     # thuoc doc: x = 600..640
def ruler(d, a=1.0):
    c = lambda col: A(col, a)
    d.rectangle([RX, py(-6), RX + 40, py(6)], fill=c((250, 240, 200)), outline=c(NAVY), width=2)
    for k in range(-6, 7):
        L = 26 if k % 5 == 0 else 14
        d.line([(RX, py(k)), (RX + L, py(k))], fill=c(NAVY), width=3)
    for k, s in ((-5, "−5"), (0, "0"), (5, "+5")):
        text(d, (RX + 56, py(k)), s, 40, NAVY, anchor="lm", alpha=a)
    arrow(d, (RX + 20, py(6) + 4), (RX + 20, py(6) + 60), c(NAVY), w=4, head=16)
    text(d, (RX + 56, py(6) + 40), "x (cm)", 40, NAVY, anchor="lm", alpha=a)

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.85, cx + pw / 2, cy + size * 0.85), fill=A(bg, a), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=a)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    kh = ease((t - 1.0) / 0.8)                               # treo vat: tam vat tu moc 1 xuong moc 2
    k = ease((t - 2.4) / 1.0)                                # tay keo vat xuong 5 cm
    rig(d, 0, cy=lerp(NAT, OY, kh) + AMP * PC * k, ab=appear(t, 1.0, 0.3))
    am1 = appear(t, 0.4, 0.4); am2 = appear(t, 2.0, 0.4)
    hdash(d, NAT, 160, 500, A(GRAY, am1), w=4); text(d, (560, NAT), "mốc 1", 40, INK, anchor="lm", alpha=am1)
    hdash(d, OY, 160, 500, A(GRAY, am2), w=4); text(d, (560, OY), "mốc 2", 40, INK, anchor="lm", alpha=am2)
    ka = appear(t, 2.4, 0.4)
    if ka > 0 and k > 0.1:
        arrow(d, (SX - BW / 2 - 40, OY), (SX - BW / 2 - 40, py(AMP * k) - 4), A(ORANGE, ka), w=6, head=20)
        if k > 0.95: text(d, (SX - BW / 2 - 60, py(2.5)), "kéo 5 cm", 40, ORANGE, anchor="rm", alpha=appear(t, 3.4, 0.3))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1120 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 460), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 40, WHITE, PURPLE, a)
    ctext(d, y0 + 160, "Bỏ qua ma sát.", 44, MUTED, maxw=920, alpha=a)
    ctext(d, y0 + 290, "Vật đi qua lại\nquanh mốc nào?", 54, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 410, 940, y0 + 422], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 410, 140 + 800 * (1 - p), y0 + 422], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (quay cham x4, dung o moi moc 0,25 s) ----------------
REL, RUN, PAUSE = 1.0, 1.0, 0.7
def tau_do(v):
    """-> (thoi gian that, so hang bang da ghi, dang dung o moc?)"""
    if v < REL: return 0.0, (1 if v >= 0.3 else 0), True
    u = v - REL; tau = 0.0; rows = 1
    for i in range(1, 5):
        if u < RUN: return tau + 0.25 * u / RUN, rows, False
        u -= RUN; tau = 0.25 * i; rows = i + 1
        if i < 4 and u < PAUSE: return tau, rows, True
        if i < 4: u -= PAUSE
    return tau, rows, True

def table(d, rows):
    x0, x1, y0 = 735, 1045, 560
    card(d, (x0, y0, x1, y0 + 500), fill=WHITE, outline=NAVY, r=22, w=3)
    d.line([(880, y0 + 15), (880, y0 + 485)], fill=LIGHT, width=3)
    text(d, (808, y0 + 48), "t (s)", 40, NAVY); text(d, (962, y0 + 48), "x (cm)", 40, NAVY)
    d.line([(x0 + 12, y0 + 92), (x1 - 12, y0 + 92)], fill=NAVY, width=3)
    for i in range(rows):
        tt, xx = ROWS[i]; y = y0 + 140 + i * 78
        text(d, (808, y), tlab(tt), 44, INK)
        text(d, (962, y), num(xx) if xx <= 0 else "+" + num(xx), 44, ORANGE)

def s_do(img, d, t, sc):
    tau, rows, hold = tau_do(t)
    xb = xof(tau)
    marks(d, 1.0, lab_o=None, lab_n=None)
    ruler(d)
    if t >= REL:                                             # vet cam: vung vat da quet tren thuoc
        lo = AMP if tau == 0 else min(AMP, xof(min(tau, PER / 2)))
        d.rectangle([RX - 16, py(lo) - 3, RX - 4, py(AMP) + 3], fill=A(ORANGE, 0.8))
    rig(d, xb)
    for i in range(rows): dot(d, RX - 10, py(ROWS[i][1]), 9, GREEN, outline=WHITE)
    table(d, rows)
    pill(d, 300, 1200, "quay chậm ×4", 40, WHITE, ORANGE)
    card(d, (560, 1150, 1000, 1250), fill=(70, 78, 100), r=22)
    text(d, (780, 1200), (f"t = {tlab(tau)} s" if hold else "▶ đang chạy"), 44, WHITE)

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    xb = xof(t / 4.0)                                        # van chay quay cham x4, khong hien so
    ka = appear(t, 0.1, 0.5)
    marks(d, 1.0, lab_o=None)
    text(d, (720, OY), "đứng yên", 40, INK, anchor="lm")
    ruler(d)
    d.rectangle([RX - 16, py(-AMP) - 3, RX - 4, py(AMP) + 3], fill=A(ORANGE, 0.8))
    rig(d, xb)
    pill(d, 870, 420, "chậm ×4", 40, WHITE, ORANGE)
    pill(d, W / 2, 1185, "ĐÁP ÁN · quanh chỗ đứng yên", 40, WHITE, NAVY, ka)
    k1 = appear(t, M[0] + 0.4, 0.45)
    if k1 > 0:
        card(d, (60, 1250, 1020, 1370), fill=A(WHITE, k1), outline=A(TEAL, k1), r=24, w=4)
        text(d, (W / 2, 1310), "x: +5 cm ↔ −5 cm", 46, INK, alpha=k1)
    k2 = appear(t, M[1] - 0.05, 0.45)
    if k2 > 0:
        card(d, (60, 1400, 1020, 1560), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=24, w=4)
        text(d, (W / 2, 1480), "Chỗ đứng yên = vị trí cân bằng O", 46, DGREEN, alpha=k2)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    rig(d, 0.0)
    marks(d, 1.0, lab_o="O")
    kc = appear(t, 1.8, 0.4)                                 # do gian hien CUNG luc chu ✓
    if kc > 0:
        x = SX + BW / 2 + 110
        arrow(d, (x, NAT + 6), (x, OY - 8), A(ORANGE, kc), w=6, head=20)
        arrow(d, (x, OY - 6), (x, NAT + 8), A(ORANGE, kc), w=6, head=20)
        text(d, (x + 24, (NAT + OY) / 2), "đã giãn", 40, ORANGE, anchor="lm", alpha=kc)
    a1 = appear(t, 0.0, 0.3) * (1 - appear(t, M[1] - 0.3, 0.2))
    if a1 > 0:
        y0 = 1060
        card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y0 + 62, "BẪY", 40, WHITE, DRED, a1)
        q = "“VTCB là chỗ lò xo chưa giãn”"
        yy = y0 + 200; f = F(46); lw = tw(d, q, f)
        text(d, (W / 2, yy), q, 46, DRED, alpha=a1)
        ks = clamp((t - 1.4) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A((140, 15, 15), a1), width=4)
        ctext(d, y0 + 340, "✓ Treo đứng: VTCB thấp hơn", 46, DGREEN, maxw=940, alpha=a1 * kc)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y0 = 1060 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 450), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Ma sát: đã bỏ qua", "• Mới thử A = 5 cm")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 190 + j * 120), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(sc):
    M = sc["M"]
    def body(d, t, k1):
        kq = appear(t, M[0] + 0.4, 0.5)
        bx, b0, oy, pc = 300, 900, 1140, 22                      # hinh nho: keo xuong 3 cm, khong ve vi tri cao nhat
        d.rectangle([200, b0 - 20, 400, b0], fill=A((205, 200, 190), kq), outline=A(NAVY, kq), width=3)
        cy = oy + 3 * pc
        spring(d, b0, cy - 30, A(NAVY, kq), n=9, amp=20, w=4, x=bx)
        card(d, (bx - 45, cy - 30, bx + 45, cy + 30), fill=A(BLOCK, kq), outline=A(NAVY, kq), r=10, w=3)
        hdash(d, oy, 180, 420, A(GRAY, kq), w=4)
        text(d, (450, oy), "đứng yên", 40, INK, anchor="lm", alpha=kq)
        arrow(d, (bx + 80, oy + 4), (bx + 80, cy - 4), A(ORANGE, kq), w=5, head=16)
        text(d, (bx + 104, cy - 10), "3 cm", 40, ORANGE, anchor="lm", alpha=kq)
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)                # goi y tre 2,5 s sau cau hoi
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1360, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1450, "Mốc giữa: chỗ đứng yên", 42, ORANGE, maxw=820, alpha=kh)
    return body

def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Dao động quanh VTCB:\nchỗ vật đứng yên",
             "Kéo xuống 3 cm rồi thả.\nVật lên cao nhất tới đâu?", body=_end_body(sc))

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]            # K9: khong co tieng nao sat diem dung cuoi hook
    out += [(do["t0"] + REL, "tap")]
    out += [(do["t0"] + REL + i * RUN + (i - 1) * PAUSE, "tick") for i in (1, 2, 3, 4)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-daodongdieuhoa-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Dao động điều hoà · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Treo vật vào lò xo", draw=s_hook, tail=0.6, caps=[
   ("Đánh dấu hai mốc, kéo xuống.", 3.6),
   ("Tự đoán trước khi xem tiếp.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Thả tay, ghi li độ mỗi 0,25 s.", 4.2),
   ("Chiều dương hướng xuống.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.9, caps=[
   ("Vật không chạm mốc chưa giãn.", 4.4),
   ("Dao động: qua lại quanh O.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=1.0, caps=[
   ("Bẫy khi treo thẳng đứng.", 4.4),
   ("Kết quả này còn giới hạn.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.7, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
