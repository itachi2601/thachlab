# Clip: tn-l10-klr-apsuat-02 - But chi ep giua hai ngon tay: cung ap luc, khac ap suat (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-klr-apsuat-02.json:
#   so_lieu_mau: F (N) 2 / 5 / 8 ; p dau nhon (MPa) 4 / 10 / 16 ; p dau bang (MPa) 0,067 / 0,167 / 0,267
#   S nhon = 0,5 mm2, S bang = 30 mm2 (ti so 60). mo_hinh: p = F/S, F nhu nhau o hai dau, bo qua trong luong but.
# Du doan (K10, khong nut): but nam yen, luc ep len ngon nao lon hon? (dap an: bang nhau).
# Bay = hien_tuong_hay_sai[1] (lan ap luc N voi ap suat MPa): "ngon tro chiu luc 10 N".
# Chot (tu suy, S_nhon 0,2 mm2 trong tham_so, bai khong co): p nhon gap may lan p bang? = 30 : 0,2 = 150
#   (buoc chua chieu: F nhu nhau nen ti so p chi con ti so S). 150 khong hien tren man.
from engine import *

ROWS = [(2, "4", "0,067"), (5, "10", "0,167"), (8, "16", "0,267")]   # so_lieu_mau: F, p nhon, p bang
DRED = (185, 28, 28)
NOTE = (60, 64, 84); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128); DGREEN = (21, 110, 55)
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

def end_labels(d, a=1.0, names=True):
    text(d, (PB + 100, 420), "đầu bằng", 55, INK, alpha=a)
    text(d, (PT - 80, 420), "đầu nhọn", 55, INK, alpha=a)
    if names:
        text(d, (170, 800), "ngón cái", 55, INK, alpha=a)
        text(d, (900, 800), "ngón trỏ", 55, INK, alpha=a)

def forces(d, Fv, a=1.0, lab=True):
    """Luc but ep len moi ngon: cung do lon -> cung do dai mui ten."""
    L = 30 + 16 * Fv
    arrow(d, (PB - 10, 700), (PB - 10 - L, 700), A(BLUE, a), w=7, head=22)
    arrow(d, (PT + 10, 700), (PT + 10 + L, 700), A(BLUE, a), w=7, head=22)
    if lab:
        s = f"{round(Fv):d} N"
        text(d, (PB + 80, 700), s, 58, BLUE, alpha=a)
        text(d, (PT - 80, 700), s, 58, BLUE, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    fingers_pencil(d, 1.0 * ease((t - 0.6) / 1.0), glow=False); end_labels(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 180), "Bút nằm yên.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "Ngón nào chịu lực", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 360), "lớn hơn?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 450, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: tien hanh ----------------
STEP = [(0.4, 1.2), (2.4, 3.2), (4.6, 5.4)]     # (bat dau tang, xong) luc 2 -> 5 -> 8 N

def f_at(t):
    v, row, prev = 1.0, -1, 1.0
    for i, (a, b) in enumerate(STEP):
        if t < a: break
        k = ease((t - a) / (b - a)); v = lerp(prev, ROWS[i][0], k)
        if t >= b: row = i
        prev = ROWS[i][0]
    return v, row

def table(d, nrow, hi=-1, a=1.0):
    card(d, (40, 870, 1040, 1440), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    xs = (190, 530, 860)
    text(d, (xs[0], 940), "F (N)", 58, BLUE, alpha=a)
    text(d, (xs[1], 940), "p nhọn", 58, RED, alpha=a); text(d, (xs[2], 940), "p bằng", 58, INK, alpha=a)
    text(d, (xs[1], 1005), "(MPa)", 55, NOTE, bold=False, alpha=a); text(d, (xs[2], 1005), "(MPa)", 55, NOTE, bold=False, alpha=a)
    d.line([(80, 1045), (1000, 1045)], fill=A(LIGHT, a), width=4)
    for i in range(nrow):
        y = 1115 + i * 105; (f, pn, pb) = ROWS[i]
        if i == hi: d.rounded_rectangle([70, y - 44, 1010, y + 44], radius=18, fill=A((255, 237, 213), a))
        text(d, (xs[0], y), str(f), 60, BLUE, alpha=a); text(d, (xs[1], y), pn, 60, RED, alpha=a)
        text(d, (xs[2], y), pb, 60, INK, alpha=a)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    Fv, row = f_at(t)
    fingers_pencil(d, Fv); end_labels(d, names=False); forces(d, Fv)
    table(d, row + 1, hi=row)
    text(d, (W / 2, 1510), "F: lực ép · p: áp suất", 58, NOTE)
    text(d, (W / 2, 1590), "p tính từ p = F/S", 55, NOTE, bold=False)

# ---------------- canh 3: dap an + so S, so p ----------------
def s_dapan(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    fingers_pencil(d, 5.0); forces(d, 5.0, lab=False)
    ka = appear(t, 0.2, 0.45); kb = appear(t, M[1], 0.45)
    a1 = ka * (1 - kb)
    if a1 > 0:
        card(d, (40, 880, 1040, 1100), fill=A((220, 252, 231), a1), outline=A(GREEN, a1), w=6)
        text(d, (W / 2, 950), "Hai lực bằng nhau", 64, DGREEN, alpha=a1)
        text(d, (W / 2, 1040), "(hai mũi tên dài bằng nhau)", 55, NOTE, bold=False, alpha=a1)
    if kb <= 0: return
    card(d, (40, 860, 1040, 1640), fill=A(WHITE, kb), outline=A(NAVY, kb), w=5)
    text(d, (W / 2, 930), "S: diện tích bị ép", 60, INK, alpha=kb)
    cx = (290, 790)
    text(d, (cx[0], 1010), "đầu bằng", 58, INK, alpha=kb); text(d, (cx[1], 1010), "đầu nhọn", 58, RED, alpha=kb)
    s1 = 150; s2 = s1 / math.sqrt(60)                 # canh ti le can S -> dien tich dung ti le 30 : 0,5
    yc = 1140
    d.rectangle([cx[0] - s1 / 2, yc - s1 / 2, cx[0] + s1 / 2, yc + s1 / 2], fill=A((219, 234, 254), kb), outline=A(BLUE, kb), width=4)
    d.rectangle([cx[1] - s2 / 2, yc - s2 / 2, cx[1] + s2 / 2, yc + s2 / 2], fill=A(RED, kb))
    d.ellipse([cx[1] - 48, yc - 48, cx[1] + 48, yc + 48], outline=A(RED, kb), width=4)
    text(d, (cx[0], 1290), "30 mm²", 60, INK, alpha=kb); text(d, (cx[1], 1290), "0,5 mm²", 60, RED, alpha=kb)
    k3 = appear(t, M[2], 0.45)
    if k3 <= 0: return
    d.line([(100, 1360), (980, 1360)], fill=A(LIGHT, k3), width=3)
    text(d, (W / 2, 1420), "p = F/S, cùng F = 5 N", 58, INK, alpha=k3)
    text(d, (cx[0], 1540), "0,167 MPa", 60, INK, alpha=k3); text(d, (cx[1], 1540), "10 MPa", 62, RED, alpha=k3)

# ---------------- canh 4: bay roi chua noi duoc ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    fingers_pencil(d, 5.0); forces(d, 5.0)
    k3 = appear(t, M[2] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k3)
    if a1 > 0:
        card(d, (40, 870, 1040, 1110), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, 935, "BẪY", RED, a1)
        q = "“Ngón trỏ chịu lực 10 N”"
        ks = clamp((t - M[1]) / 0.4); f = F(60); lw = tw(d, q, f); yy = 1040
        text(d, (W / 2, yy), q, 60, mix(RED, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        ok = appear(t, M[1], 0.4) * a1
        if ok > 0:
            card(d, (40, 1140, 1040, 1350), fill=A(WHITE, ok), outline=A(NAVY, ok), w=4)
            text(d, (100, 1200), "F = 5 N: áp lực", 58, BLUE, anchor="lm", alpha=ok)
            text(d, (100, 1290), "p = 10 MPa: áp suất", 58, RED, anchor="lm", alpha=ok)
        k2 = appear(t, M[1] + 3.0, 0.45) * a1
        if k2 > 0:
            card(d, (40, 1380, 1040, 1520), fill=A((220, 252, 231), k2), outline=A(GREEN, k2), w=5)
            text(d, (W / 2, 1450), "Hai đại lượng khác nhau", 60, DGREEN, alpha=k2)
    if k3 > 0:
        card(d, (40, 870, 1040, 1300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 940, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 1070), "Đau chỉ để so, chưa đo p.", 60, INK, alpha=k3)
        text(d, (W / 2, 1170), "S đầu nhọn là giả định.", 60, INK, alpha=k3)

# ---------------- canh 5: thu nghi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    fingers_pencil(d, 5.0)
    k = appear(t, 0.15, 0.4)
    card(d, (40, 880, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 945, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 1065), "Đầu nhọn còn 0,2 mm².", 62, INK, alpha=k)
    text(d, (W / 2, 1165), "Áp suất lên ngón trỏ", 62, INK, alpha=k)
    text(d, (W / 2, 1255), "gấp mấy lần ngón cái?", 64, DORANGE, alpha=k)
    seg_bar(d, 1400, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + STEP[1][0], "tap"), (do["t0"] + STEP[2][0], "tap"),
            (da["t0"] + 0.2, "ding"), (da["t0"] + da["M"][1], "tap"),
            (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-klr-apsuat-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Khối lượng riêng. Áp suất · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bút chì kẹp giữa hai ngón", draw=s_hook, tail=0.2, caps=[
   ("Kẹp bút, ép nhẹ.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Ép mạnh dần", draw=s_do, tail=0.4, caps=[
   ("Ép mạnh dần.", 3.8),
   ("Ngón trỏ lõm sâu hơn.", 3.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Bút đứng yên.", 3.6),
   ("S nhỏ hơn 60 lần.", 3.4),
   ("Nên p lớn gấp 60.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 3.0),
   ("Lực hay áp suất?", 6.1),
   ("Chưa nói được.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự tính.", 6.6)]),
])
