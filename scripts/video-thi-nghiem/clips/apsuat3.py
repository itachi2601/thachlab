# Clip: tn-l10-klr-apsuat-03 - Chai nhua duc lo theo do sau: tia o lo nao phun manh nhat (lo 8, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-klr-apsuat-03.json:
#   so_lieu_mau (h cm, p du Pa, v m/s): 5 500 1,0 ; 10 1000 1,41 ; 15 1500 1,73 (g = 10, rho = 1000, so tinh tu mo hinh).
#   cac_buoc: chai 1 ba lo doc than, chai 2 bon lo quanh than cung do cao ; quan_sat/rut_ra cua kho.
# Hinh: 16 px/cm ca hai truc ; tia la parabol nem ngang voi v kho, roi toi khay (chai dat tren de cao 20 cm de
#   tia lo sau nhat cung xa nhat, khong gay nham "xa nhat" voi "manh nhat") ; mui ten tai mieng lo dai ti le v.
# Du doan (K10: chi cau hoi + hinh): boc bang dinh ca ba lo, tia o lo nao phun manh nhat ngay tai mieng lo?
#   A. Lo tren cung, gan mat nuoc ; B. Lo o giua ; C. Lo duoi cung, sau nhat (DUNG) ; D. Ba lo manh nhu nhau.
# Khac klr1 (do rho bang can + binh chia do) va klr2 (but chi giua hai ngon): cau hoi, so va bo cuc khac han.
# KHONG tra loi san: Cau 3 muc II.4 (voi tang 1 / tang 5, chenh 12 m) -> clip KHONG tinh hieu ap suat giua hai lo,
#   khong ghi cong thuc delta p.
# Bay = hien_tuong_hay_sai[0] "nuoc chi ep xuong day" -> chai 2 (nhin tu tren) bon tia ngang manh nhu nhau.
# Cau chot (ca tu suy, ghi trong ghi_chu kho): rot them cho mat nuoc dang 5 cm, lo khong doi -> lo giua sau 15 cm,
#   phun manh nhu lo duoi cung luc truoc (1500 Pa). Khong doc duoc tren man, phai suy do sau tinh tu mat nuoc.
from engine import *

ROWS = [(5, 500, 1.0), (10, 1000, 1.41), (15, 1500, 1.73)]   # so_lieu_mau
G = 10.0
DRED = (185, 28, 28); NOTE = (60, 64, 84)
WAT = (147, 197, 253); WAT_D = (37, 99, 235); BOT = (120, 140, 170); TAPE = (250, 214, 120); WOOD = (196, 150, 100)

# ---------------- bo cuc (16 px/cm) ----------------
PXC = 16
CX0, CX1 = 180, 324                    # than chai
WS = 430                               # mat nuoc
YB = WS + 20 * PXC                     # day chai (cot nuoc 20 cm) = 750
TRAY = YB + 20 * PXC                   # khay (de cao 20 cm) = 1070
def yh(h): return WS + h * PXC

def bottle(d, a=1.0, tape=False):
    d.rectangle([CX0 - 10, YB, CX1 + 10, TRAY], fill=A(WOOD, a))                       # de
    d.rectangle([110, TRAY, 1040, TRAY + 26], fill=A((150, 155, 172), a))               # khay
    d.rectangle([CX0 + 3, WS, CX1 - 3, YB - 3], fill=A(WAT, 0.8 * a))
    d.line([(CX0 + 3, WS), (CX1 - 3, WS)], fill=A(WAT_D, a), width=4)
    sh = [(CX0, YB), (CX0, 380), (232, 312), (232, 272), (272, 272), (272, 312), (CX1, 380), (CX1, YB)]
    d.line(sh + [(CX0, YB)], fill=A(BOT, a), width=5, joint="curve")
    d.rectangle([226, 252, 278, 274], fill=A((37, 99, 235), a))                        # nap mo
    for h, _, _ in ROWS:
        y = yh(h); dot(d, CX1, y, 7, A(NAVY, a))
        if tape: d.rectangle([CX1 - 6, y - 18, CX1 + 16, y + 18], fill=A(TAPE, a))

def depth_marks(d, a=1.0, mat=True):
    if mat: text(d, (CX1 + 20, WS - 30), "mặt nước", 44, WAT_D, anchor="lm", alpha=a)
    for h, _, _ in ROWS:
        y = yh(h)
        for x in range(120, CX1 - 10, 22): d.line([(x, y), (x + 12, y)], fill=A(MUTED, a), width=3)
        text(d, (112, y), f"{h} cm", 44, INK, anchor="rm", alpha=a)
    text(d, (112, WS), "0", 44, INK, anchor="rm", alpha=a)

def jet(d, h, v, prog, a=1.0):
    """Tia nem ngang tu lo do sau h (cm), toc do v (m/s); prog 0..1 phan quang duong da phun toi."""
    y0 = yh(h); drop = (TRAY - y0) / PXC / 100; T = math.sqrt(2 * drop / G); pts = []
    for k in range(41):
        tau = T * k / 40 * prog
        pts.append((CX1 + v * tau * 100 * PXC, y0 + 0.5 * G * tau * tau * 100 * PXC))
    if prog > 0.01: d.line(pts, fill=A(WAT_D, 0.85 * a), width=9, joint="curve")
    return pts[-1]

def mouth_arrow(d, v, h, a=1.0, lab=False):
    y = yh(h) - 26
    arrow(d, (CX1 + 14, y), (CX1 + 14 + 140 * v, y), A(RED, a), w=7, head=18)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    bottle(d, tape=True); depth_marks(d)
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 1130 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 460), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 150), "Mở cả ba lỗ cùng lúc.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 230), "Tia ở lỗ nào phun mạnh nhất", 50, INK, alpha=a)
    text(d, (W / 2, y0 + 296), "ngay tại miệng lỗ?", 50, INK, alpha=a)
    text(d, (W / 2, y0 + 372), "Chọn đáp án ở khung câu hỏi", 40, NOTE, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([150, y0 + 426, 930, y0 + 440], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([150, y0 + 426, 150 + 780 * (1 - p), y0 + 440], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: tien hanh ----------------
OPEN, FLOW = 0.8, 1.6                    # boc bang dinh ; thoi gian tia phun toi khay (quay cham)
ROW_AT = [4.4 + 0.8 * i for i in range(3)]

def table(d, n, y0=1150, a=1.0, hi=-1):
    card(d, (110, y0, 970, y0 + 420), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (300, y0 + 55), "độ sâu (cm)", 44, INK, alpha=a); text(d, (720, y0 + 55), "p do nước (Pa)", 44, INK, alpha=a)
    d.line([(140, y0 + 95), (940, y0 + 95)], fill=A(LIGHT, a), width=4)
    for i in range(n):
        h, p, _ = ROWS[i]; y = y0 + 150 + i * 80
        if i == hi: d.rounded_rectangle([130, y - 34, 950, y + 34], radius=16, fill=A((255, 237, 213), a))
        text(d, (300, y), str(h), 46, INK, alpha=a); text(d, (720, y), str(p), 46, RED, alpha=a)
    text(d, (540, y0 + 450), "số tính, g = 10 m/s²", 44, NOTE, alpha=a)

def s_do(img, d, t, sc):
    bottle(d, tape=t < OPEN); depth_marks(d)
    prog = ease((t - OPEN) / FLOW) if t > OPEN else 0.0
    for h, _, v in ROWS: jet(d, h, v, prog)
    ka = appear(t, OPEN + FLOW + 0.3, 0.4)
    for h, _, v in ROWS:
        if ka > 0: mouth_arrow(d, v, h, ka)
    if ka > 0: text(d, (CX1 + 290, yh(5) - 70), "tốc độ ra", 44, RED, anchor="lm", alpha=ka)
    n = sum(1 for r in ROW_AT if t >= r)
    if n: table(d, n, hi=n - 1)

# ---------------- canh 3: dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    bottle(d); depth_marks(d, mat=False)
    for h, _, v in ROWS: jet(d, h, v, 1.0, 0.6); mouth_arrow(d, v, h, 1.0)
    ka = appear(t, 0.1, 0.4)
    lab = "ĐÁP ÁN · Lỗ dưới cùng, sâu nhất"
    pw = tw(d, lab, F(42)) + 56
    card(d, (700 - pw / 2, 270, 700 + pw / 2, 338), fill=A(NAVY, ka), r=34)
    text(d, (700, 304), lab, 42, WHITE, alpha=ka)
    k1 = appear(t, 0.5, 0.4)
    if k1 > 0: d.ellipse([CX1 - 30, yh(15) - 60, CX1 + 290, yh(15) + 30], outline=A(ORANGE, k1), width=5)
    table(d, 3, a=1 - appear(t, M[1] - 0.2, 0.4), hi=2)
    kr = appear(t, M[1] - 0.2, 0.45)
    if kr <= 0: return
    y0 = 1150 + (1 - kr) * 30
    card(d, (60, y0, 1020, y0 + 260), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
    pw = tw(d, "RÚT RA", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(GREEN, kr), r=32)
    text(d, (W / 2, y0 + 56), "RÚT RA", 40, WHITE, alpha=kr)
    text(d, (W / 2, y0 + 170), "Càng sâu, áp suất nước càng lớn", 48, INK, alpha=kr)

# ---------------- canh 4: bay (chai 2) + chua noi duoc ----------------
def top_view(d, a, prog):
    cx, cy, r = W / 2, 1180, 80
    L = 300 * prog
    for ang in (0, 90, 180, 270):
        u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
        if L > 2: d.line([(cx + u[0] * r, cy + u[1] * r), (cx + u[0] * (r + L), cy + u[1] * (r + L))], fill=A(WAT_D, 0.85 * a), width=10)
    dot(d, cx, cy, r, A(WAT, a), outline=A(BOT, a))
    text(d, (cx, cy), "chai 2", 44, NAVY, alpha=a)
    text(d, (cx, 1590), "4 lỗ cùng độ sâu", 44, NOTE, alpha=a)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    k2 = appear(t, 2.4, 0.45)
    top_view(d, k2, ease((t - 2.4) / 1.0))
    if a1 > 0:
        card(d, (40, 290, 1040, 750), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, 318, W / 2 + pw / 2, 382), fill=A(DRED, a1), r=32)
        text(d, (W / 2, 350), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 2.0) / 0.4); q = "“Nước chỉ ép xuống đáy chai”"; f = F(48); lw = tw(d, q, f); yy = 490
        text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 - lw / 2 - 50, yy), "✗", 60, DRED, alpha=a1 * ks)
        text(d, (W / 2, 680), "Nước ép cả ngang, như nhau", 48, GREEN, alpha=a1 * k2)
    if k3 > 0:
        y1 = 290 + (1 - k3) * 30
        card(d, (40, y1, 1040, y1 + 390), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        for j, s1 in enumerate(("• Mới thử với nước", "• Mực nước tụt dần")):
            kk = k3 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (100, y1 + 210 + 110 * j), s1, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: mat nuoc cao them 5 cm, lo tren cung manh nhu lo nao luc truoc (-> lo giua); goi y tre 2,6 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 420, "Càng sâu, nước ép càng mạnh", 50, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1320), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 850, "Rót thêm cho mặt nước cao thêm 5 cm. Lỗ trên cùng giờ phun mạnh như lỗ nào lúc trước?",
          48, INK, maxw=900, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.6, 0.5)
    if kh > 0:
        card(d, (110, 1040, 970, 1270), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1095, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1195, "Các lỗ không dịch chỗ", 46, (176, 64, 8), maxw=820, alpha=kh)

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
    return ([(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + OPEN, "tap")]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-klr-apsuat-03", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Khối lượng riêng. Áp suất · thachlab.id.vn", scenes=[
 dict(key="hook", title="Chai nước đục ba lỗ", draw=s_hook, tail=0.3, caps=[
   ("Chai đầy nước.", 3.2),
   ("Nghĩ trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Mở cả ba lỗ", draw=s_do, tail=0.6, caps=[
   ("Quay chậm lúc nước phun.", 4.0),
   ("So tia ngay tại miệng lỗ.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Ba mũi tên đỏ.", 4.2),
   ("Đọc lại bảng.", 4.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 4.6),
   ("Còn bỏ ngỏ.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 8.2)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("lệch:", _kiem() or "không")
