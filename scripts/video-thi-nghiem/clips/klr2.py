# Clip: tn-l10-klr-apsuat-02 - But chi ep giua hai ngon tay: cung ap luc, khac ap suat (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-klr-apsuat-02.json:
#   so_lieu_mau: F (N) 2 / 5 / 8 ; p dau nhon (MPa) 4 / 10 / 16 ; p dau bang (MPa) 0,067 / 0,167 / 0,267
#   S nhon = 0,5 mm2, S bang = 30 mm2 (ti so 60); tham_so S_nhon 0,2-2 mm2 (cau chot dung 0,2 mm2, chua hien tren man).
#   mo_hinh: p = F/S, F nhu nhau o hai dau (but can bang), bo qua trong luong but.
# Canh: Du doan (chi cau hoi + hinh, K10: luc len ngon nao lon hon?) -> Tien hanh (ep 2 -> 5 -> 8 N, ngon tro lom sau, bang so)
#       -> Dap an C (but dung yen: hai luc can bang) + so S, so p (gap 60) -> Bay (rieng) -> Chua noi duoc (rieng)
#       -> Chot + cau hoi tu tinh (S = 0,2 mm2, F = 5 N -> khoang 25 MPa, gia tri chua hien).
from engine import *

ROWS = [(2, "4", "0,067"), (5, "10", "0,167"), (8, "16", "0,267")]   # so_lieu_mau: F, p nhon, p bang
DRED = (185, 28, 28)                                                   # do dam #B91C1C cho chu canh Bay
SKIN = (241, 200, 166); SKIN_D = (205, 150, 112); NAIL = (250, 226, 214)
WOOD = (236, 200, 150); LEAD = (60, 62, 72); PEN = (250, 204, 21); PEN_D = (214, 168, 10)

PY = 560                      # truc but
PB, PT = 260, 820             # x dau bang, x mui nhon

def fingers_pencil(d, Fv, glow=True):
    """Ngon cai (trai) ep dau bang, ngon tro (phai) ep dau nhon. Fv: luc ep (N) -> do lom."""
    dfl = 1 + 0.4 * Fv; dtp = 4 + 3.2 * Fv
    # ngon cai: tu mep trai vao, dau ngon o x = PB + dfl (lun nhe)
    xr = PB + dfl
    d.rounded_rectangle([-60, 488, xr, 632], radius=70, fill=SKIN, outline=SKIN_D, width=4)
    d.rounded_rectangle([xr - 120, 492, xr - 40, 528], radius=16, fill=NAIL, outline=SKIN_D, width=3)
    d.line([(xr - 3, 528), (xr - 3, 592)], fill=SKIN_D, width=4)
    # ngon tro: tu mep phai vao, mui nhon lun sau dtp
    xl = PT - dtp
    d.rounded_rectangle([xl, 488, 1140, 632], radius=70, fill=SKIN, outline=SKIN_D, width=4)
    d.rounded_rectangle([xl + 40, 492, xl + 120, 528], radius=16, fill=NAIL, outline=SKIN_D, width=3)
    # vien da lom thanh pheu quanh mui nhon: rong va sau dan theo F (pheu to nen BG, vien SKIN_D)
    if glow:                                                # da do dan quanh mui nhon (ve truoc vien lom)
        r = 18 + 3 * Fv
        d.ellipse([PT - 4, PY - r, PT - 4 + 2 * r, PY + r], fill=A(RED, 0.08 + 0.025 * Fv))
    w = 1.5 * dtp + 12; up, lo = [], []
    xc = lambda y: xl + 70 - math.sqrt(max(0.0, 70 ** 2 - y ** 2))     # mep tron cua dau ngon (ban kinh 70)
    for i in range(13):
        u = i / 12; y = w * (1 - u) ** 1.4; x = xc(y) + (PT - xc(y)) * (1 - (1 - u) ** 2)
        up.append((x, PY - y)); lo.append((x, PY + y))
    d.polygon(up + lo[::-1], fill=BG)
    d.line(up, fill=SKIN_D, width=5); d.line(lo, fill=SKIN_D, width=5)
    # but chi
    d.rectangle([PB, PY - 28, 700, PY + 28], fill=PEN, outline=PEN_D, width=3)
    d.line([(PB + 4, PY - 9), (700, PY - 9)], fill=PEN_D, width=3); d.line([(PB + 4, PY + 9), (700, PY + 9)], fill=PEN_D, width=3)
    d.rectangle([PB, PY - 28, PB + 10, PY + 28], fill=WOOD)
    d.polygon([(700, PY - 28), (780, PY - 9), (780, PY + 9), (700, PY + 28)], fill=WOOD, outline=(200, 160, 110))
    d.polygon([(780, PY - 9), (PT, PY), (780, PY + 9)], fill=LEAD)

def end_labels(d, a=1.0, names=True):
    text(d, (PB + 90, 440), "đầu bằng", 40, INK, alpha=a)
    text(d, (PT - 70, 440), "đầu nhọn", 40, INK, alpha=a)
    if names:
        text(d, (150, 800), "ngón cái", 40, INK, alpha=a)
        text(d, (930, 800), "ngón trỏ", 40, INK, alpha=a)

def forces(d, Fv, a=1.0, lab=True):
    """Luc but ep len moi ngon: cung do lon -> cung do dai mui ten."""
    L = 30 + 16 * Fv
    arrow(d, (PB - 10, 700), (PB - 10 - L, 700), A(BLUE, a), w=7, head=22)
    arrow(d, (PT + 10, 700), (PT + 10 + L, 700), A(BLUE, a), w=7, head=22)
    if lab:
        s = f"{Fv:g} N".replace(".", ",")
        text(d, (PB + 70, 700), s, 42, BLUE, alpha=a)
        text(d, (PT - 70, 700), s, 42, BLUE, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    fingers_pencil(d, 1.0 * ease((t - 0.6) / 1.0), glow=False); end_labels(d)
    k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    for x in (PB - 90, PT + 90):                          # chua biet luc: hai o "? N" giong het nhau
        card(d, (x - 70, 670, x + 70, 730), fill=A((245, 243, 255), k), outline=A(PURPLE, k), r=20, w=3)
        text(d, (x, 700), "? N", 40, PURPLE, alpha=k)
    y0 = 880 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 620), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 56
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 190, "Bút nằm yên.", 46, INK, maxw=880, alpha=k)
    ctext(d, y0 + 330, "Lực ép lên ngón nào lớn hơn?", 50, INK, maxw=820, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 540, 880, y0 + 554], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 540, 200 + 680 * (1 - q), y0 + 554], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
STEP = [(0.4, 1.3), (2.6, 3.4), (4.8, 5.6)]     # (bat dau tang, xong) luc 2 -> 5 -> 8 N

def f_at(t):
    v, row = 1.0, -1
    prev = 1.0
    for i, (a, b) in enumerate(STEP):
        if t < a: break
        k = ease((t - a) / (b - a)); v = lerp(prev, ROWS[i][0], k)
        if t >= b: row = i
        prev = ROWS[i][0]
    return v, row

def table(d, nrow, hi=-1, a=1.0):
    card(d, (40, 880, 1040, 1420), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    xs = (200, 540, 870)
    text(d, (xs[0], 950), "F (N)", 42, INK, alpha=a)
    text(d, (xs[1], 935), "p đầu nhọn", 40, RED, alpha=a); text(d, (xs[2], 935), "p đầu bằng", 40, INK, alpha=a)
    text(d, (xs[1], 985), "(MPa)", 40, INK, bold=False, alpha=a); text(d, (xs[2], 985), "(MPa)", 40, INK, bold=False, alpha=a)
    d.line([(80, 1025), (1000, 1025)], fill=A(LIGHT, a), width=4)
    for i in range(nrow):
        y = 1095 + i * 105; (f, pn, pb) = ROWS[i]
        if i == hi: d.rounded_rectangle([70, y - 42, 1010, y + 42], radius=18, fill=A((255, 237, 213), a))
        text(d, (xs[0], y), str(f), 46, BLUE, alpha=a); text(d, (xs[1], y), pn, 46, RED, alpha=a)
        text(d, (xs[2], y), pb, 46, INK, alpha=a)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    Fv, row = f_at(t)
    fingers_pencil(d, Fv); end_labels(d, names=False); forces(d, Fv, lab=(row >= 0 and abs(Fv - ROWS[row][0]) < 1e-6))
    card(d, (W / 2 - 150, 300, W / 2 + 150, 370), fill=(255, 247, 237), outline=ORANGE, r=30, w=3)
    text(d, (W / 2, 335), "ép nhẹ thôi", 40, ORANGE)
    table(d, row + 1, hi=row)
    text(d, (W / 2, 1480), "Số tính từ p = F/S", 40, INK, bold=False)

# ---------------- canh 3: dap an + so S, so p ----------------
def s_dapan(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    ka = appear(t, 0.2, 0.45)
    pw = tw(d, "Đáp án C", F(44)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 334), fill=A(GREEN, ka), r=36)
    text(d, (W / 2, 298), "Đáp án C", 44, WHITE, alpha=ka)
    kb = appear(t, M[2] - 0.3, 0.4); top = 1 - kb             # phan 1 (bon luc) nhuong cho phan 2 (so S, p)
    if top > 0.01:
        fingers_pencil(d, 5.0)
        L = 30 + 16 * 5.0                                    # bon mui ten cung do dai (cung do lon F = 5 N)
        k1 = appear(t, M[0], 0.4) * top
        if k1 > 0:                                           # luc hai ngon ep len but: huong vao but
            arrow(d, (PB + 6, 455), (PB + 6 + L, 455), A(GREEN, k1), w=7, head=22)
            arrow(d, (PT - 6, 455), (PT - 6 - L, 455), A(GREEN, k1), w=7, head=22)
            text(d, (W / 2, 455), "lực lên bút", 40, GREEN, alpha=k1)
            text(d, (W / 2, 830), "Bỏ qua trọng lượng bút", 40, INK, bold=False, alpha=k1)
        k2 = appear(t, M[1], 0.4) * top
        if k2 > 0:                                           # but ep lai len ngon: huong ra ngoai (dinh luat III)
            arrow(d, (PB - 10, 700), (PB - 10 - L, 700), A(BLUE, k2), w=7, head=22)
            arrow(d, (PT + 10, 700), (PT + 10 + L, 700), A(BLUE, k2), w=7, head=22)
            text(d, (W / 2, 700), "lực lên ngón", 40, BLUE, alpha=k2)
            card(d, (60, 920, 1020, 1120), fill=A((239, 246, 255), k2), outline=A(BLUE, k2), w=4)
            ctext(d, 1020, "Bút ép lại ngón đúng bằng lực ấy", 42, INK, maxw=880, alpha=k2)
    if kb <= 0: return
    card(d, (60, 360, 1020, 1600), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=4)
    cx = (290, 790)
    text(d, (cx[0], 430), "đầu bằng", 42, INK, alpha=kb); text(d, (cx[1], 430), "đầu nhọn", 42, RED, alpha=kb)
    s1 = 200; s2 = s1 / math.sqrt(60)                   # canh ti le can S -> dien tich dung ti le 30 : 0,5 (s2 ~ 26 px)
    d.rectangle([cx[0] - s1 / 2, 590 - s1 / 2, cx[0] + s1 / 2, 590 + s1 / 2], fill=A((219, 234, 254), kb), outline=A(BLUE, kb), width=4)
    d.rectangle([cx[1] - s2 / 2, 590 - s2 / 2, cx[1] + s2 / 2, 590 + s2 / 2], fill=A(RED, kb))
    d.ellipse([cx[1] - 52, 590 - 52, cx[1] + 52, 590 + 52], outline=A(RED, kb), width=4)   # vong khoanh o nho
    text(d, (cx[0], 760), "S = 30 mm²", 44, INK, alpha=kb); text(d, (cx[1], 760), "S = 0,5 mm²", 44, INK, alpha=kb)
    text(d, (W / 2, 860), "30 : 0,5 = 60", 46, ORANGE, alpha=kb)
    k3 = appear(t, M[3] - 0.4, 0.4)                     # hang p hien TRUOC phu de "p gap khoang 60"
    if k3 <= 0: return
    d.line([(120, 930), (960, 930)], fill=A(LIGHT, k3), width=3)
    text(d, (W / 2, 990), "F = 5 N", 42, BLUE, alpha=k3)
    text(d, (cx[0], 1090), "p = 0,167 MPa", 44, INK, alpha=k3); text(d, (cx[1], 1090), "p = 10 MPa", 44, RED, alpha=k3)
    text(d, (W / 2, 1180), "(1 MPa = 1 N/mm²)", 40, INK, bold=False, alpha=k3)
    text(d, (W / 2, 1290), "10 : 0,167 ≈ 60", 46, ORANGE, alpha=k3)
    text(d, (W / 2, 1410), "p = F / S", 48, GREEN, alpha=appear(t, M[3] + 0.6, 0.45))

# ---------------- canh 4: bay (rieng) roi chua noi duoc (rieng) ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    fingers_pencil(d, 5.0)
    k3 = appear(t, M[1] - 0.1, 0.45)
    a = appear(t, 0.1, 0.4) * (1 - k3)
    if a > 0:
        forces(d, 5.0, a=appear(t, 1.6, 0.4) * a)
        y0 = 880
        card(d, (60, y0, 1020, y0 + 640), fill=A(WHITE, a), outline=A(DRED, a), w=6)
        pw = tw(d, "Bẫy", F(40)) + 60
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a), r=32)
        text(d, (W / 2, y0 + 60), "Bẫy", 40, WHITE, alpha=a)
        q = "“Bút đẩy đầu nhọn mạnh hơn”"
        ks = clamp((t - 1.0) / 0.4); f = F(48); yy = y0 + 210; lw = tw(d, q, f)
        text(d, (W / 2, yy), q, 48, INK, alpha=a)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a), width=3)
        k2 = appear(t, 1.6, 0.45) * a
        ctext(d, y0 + 420, "Sai: lực bằng nhau, khác S", 50, DRED, maxw=900, alpha=k2)
    if k3 > 0:
        y1 = 880 + (1 - k3) * 30
        card(d, (60, y1, 1020, y1 + 640), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 70), "Chưa nói được gì?", 46, NAVY, alpha=k3)
        items = ("• Đau: chỉ so sánh, chưa đo p", "• S đầu nhọn: giả định, chưa đo")
        for j, s in enumerate(items):
            kk = k3 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (110, y1 + 240 + j * 150), s, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def hint(d, t, k):                        # tu ve goi y de chu >= 40 px (engine ve "Gợi ý" 36 px)
        kh = appear(t, sc["M"][0] + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 1290, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1350, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1445, "p = F/S, giữ N/mm²", 46, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Cùng áp lực: S nhỏ thì p lớn",
             "S đầu nhọn còn 0,2 mm², vẫn ép 5 N. Áp suất bao nhiêu?", body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + STEP[1][0], "tap"), (do["t0"] + STEP[2][0], "tap"),
            (da["t0"] + 0.2, "ding"), (b["t0"] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-klr-apsuat-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Khối lượng riêng. Áp suất · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bút chì kẹp giữa hai ngón", draw=s_hook, tail=0.6, caps=[
   ("Kẹp bút, giữ yên, ép nhẹ.", 3.0),
   ("Dừng video, tự đoán.", 5.4)]),
 dict(key="do", title="Ép mạnh dần", draw=s_do, tail=0.5, caps=[
   ("Tăng dần lực ép của hai ngón.", 4.0),
   ("Ngón trỏ lõm sâu, đau hơn hẳn.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Bút đứng yên: lực cân bằng.", 3.2),
   ("Định luật III Newton.", 3.0),
   ("S nhỏ 60 lần.", 3.0),
   ("p gấp khoảng 60.", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy hay gặp.", 3.6),
   ("Giới hạn.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự tính.", 5.6)]),
])
