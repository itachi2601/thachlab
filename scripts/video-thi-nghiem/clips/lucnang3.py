# Clip: tn-l10-luc-can-luc-nang-03 - Luc ke + binh tran: luc ke giam bao nhieu khi khoi nhom chim han (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-luc-can-luc-nang-03.json:
#   so_lieu_mau (phan chim f, T N, F_A N): 0 2,65 0 ; 0,5 2,16 0,49 ; 1 1,67 0,98 ; quan_sat: nuoc tran 100 cm3, nang 0,98 N.
#   tham_so: V = 100 cm3, rho nhom 2700, g = 9,8 ; mo_hinh T = P - rho.g.f.V. Luc ke ve bang luc_ke() engine.
# Du doan (K10, khong nut): khoi nhom chim han, so chi luc ke giam mot luong bang gi? (dap an: trong luong nuoc tran).
# KHONG tra loi san: Cau 5 bai (ha sau 20 -> 60 cm) -> khong ha sau them ; Cau 6 (5,4 N mot nua) -> khong tinh ;
#   Cau 4 (go noi) -> bay chi dung so cua clip.
# Bay = hien_tuong_hay_sai[1] (dung the tich ca vat khi chi chim mot phan): "chim mot nua: luc day van 0,98 N".
# Chot (ca tu suy, ghi_chu kho): chim han trong nuoc muoi 1200 kg/m3 -> F_A = 1,18 N, luc ke chi 1,47 N.
#   Buoc chua chieu: F_A ti le khoi luong rieng chat long. Khong goi y, khong cong thuc.
from engine import *

P_N, V, RHO_V, G = 2.646, 1e-4, 2700, 9.8
ROWS = [(0.0, 2.65, 0.0, "ngoài không khí"), (0.5, 2.16, 0.49, "chìm một nửa"), (1.0, 1.67, 0.98, "chìm hẳn")]   # so_lieu_mau
FMAX = 3.0                                       # 3 N, vach 0,1 N (~14 px): doc duoc toi 0,01 N bang uoc
NOTE = (60, 64, 84); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128); DGREEN = (21, 110, 55)
AL = (186, 192, 204); AL_D = (120, 128, 145); WAT = (147, 197, 253); WAT_D = (59, 130, 246); GLASS = (110, 130, 160)
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")
def t_model(f, rho=1000): return P_N - rho * G * f * V

# ---------------- bo cuc ----------------
LX = 320; BODY = 520; YR0 = 330                 # truc luc ke ; than ; vong treo luc dau
BW, BH, ROPE = 150, 140, 46                     # khoi nhom ; day tu moc toi khoi
WS = 1076                                       # mat nuoc = mieng voi tran (day khoi luc f = 0: y 1072)
TX0, TX1, TY1 = 150, 500, 1560                  # binh tran
CUP = (640, 1380, 800, 1560)

def stand(d, yr):
    d.rounded_rectangle([46, 270, 74, TY1], radius=8, fill=(170, 175, 190))
    d.rounded_rectangle([46, yr - 34, LX + 30, yr - 14], radius=8, fill=(150, 155, 172))
    d.line([(LX, yr - 14), (LX, yr - 2)], fill=NAVY, width=6)

def scale_block(d, f, f_read, a=1.0):
    """Luc ke + khoi nhom; f: phan chim (0..1) -> do ha. f_read: so kim (None -> '?')."""
    yr = YR0 + f * (BH + 12); stand(d, yr)            # f = 1: dinh khoi duoi mat nuoc 8 px
    yh = yr + 16 + BODY + 20                     # y moc (s = 0)
    Q = lambda s, h=0.0: (LX + h, yh - s)
    luc_ke(d, Q, 0, 20, 20 + BODY, FMAX, f_read, nho=0.1, ben=-1, co=56, alpha=a)
    yt = yh + ROPE
    d.line([(LX, yh + 10), (LX, yt)], fill=NAVY, width=4)
    return yt                                    # dinh khoi

def block(img, d, yt, a=1.0, lab=True):
    d.rectangle([LX - BW / 2, yt, LX + BW / 2, yt + BH], fill=AL, outline=AL_D, width=4)
    yc = min(max(WS, yt), yt + BH)               # phan chim: phu mau nuoc mo
    if yc < yt + BH - 6: d.rectangle([LX - BW / 2 + 3, yc, LX + BW / 2 - 3, yt + BH - 3], fill=A(WAT_D, 0.28))
    if lab: text(d, (LX, yt + BH / 2), "nhôm", 56, NAVY)

def tank(d, wet=True):
    d.rectangle([TX0 + 4, WS, TX1 - 4, TY1 - 4], fill=A(WAT, 0.75))
    d.line([(TX0, 1020), (TX0, TY1), (TX1, TY1), (TX1, 1020)], fill=GLASS, width=6)
    d.line([(TX1, WS - 6), (TX1 + 90, WS + 34)], fill=GLASS, width=10)          # voi tran
    d.line([(TX0 + 4, WS), (TX1 - 4, WS)], fill=WAT_D, width=4)

def cup(d, vol, stream=0.0):
    x0, y0, x1, y1 = CUP
    if stream > 0:
        for k in range(3): d.line([(TX1 + 86 + k * 3, WS + 34), (TX1 + 100 + k * 3, y1 - 8 - 150 * vol)], fill=A(WAT_D, 0.7 * stream), width=4)
    h = 150 * vol
    if h > 2: d.rectangle([x0 + 5, y1 - 5 - h, x1 - 5, y1 - 5], fill=A(WAT, 0.85))
    d.line([(x0, y0), (x0, y1), (x1, y1), (x1, y0)], fill=GLASS, width=6)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def scene(img, d, f, f_read, vol=None, stream=0.0):
    tank(d); yt = scale_block(d, f, f_read); block(img, d, yt)
    cup(d, f if vol is None else vol, stream)
    return yt

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    scene(img, d, 0.0, None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    x0, x1 = 500, 1040; cx = (x0 + x1) / 2; y0 = 290 + (1 - a) * 30
    card(d, (x0, y0, x1, y0 + 720), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, cx, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    for j, s1 in enumerate(("Nhôm chìm hẳn,", "nước tràn ra cốc.", "Lực kế giảm", "một lượng bằng gì?")):
        text(d, (cx, y0 + 175 + j * 85 + (40 if j >= 2 else 0)), s1, 58, PURPLE if j == 3 else INK, alpha=a)
    seg_bar(d, y0 + 590, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a, x0=x0 + 30, step=98, w=84)

# ---------------- canh 2: tien hanh ----------------
MOVES = [(1.8, 3.4), (5.0, 6.6)]                 # (bat dau ha, xong) toi f = 0,5 roi f = 1
SETTLE = 0.5                                     # doi kim dung yen roi moi ghi
LABS = ("không khí", "chìm một nửa", "chìm hẳn")
def do_state(t):
    """-> (f, dang ha?, so hang da ghi)."""
    f, moving = 0.0, False
    for i, (a, b) in enumerate(MOVES):
        if t >= a:
            f = lerp(ROWS[i][0], ROWS[i + 1][0], ease((t - a) / (b - a))); moving = t < b + SETTLE
    rows = 1
    for i, (a, b) in enumerate(MOVES):
        if t >= b + SETTLE: rows = i + 2
    return f, moving, rows

def readout(d, rows, moving, a=1.0):
    card(d, (520, 290, 1040, 470), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (780, 340), "số chỉ lực kế", 56, NOTE, alpha=a)
    s = "…" if (moving or rows == 0) else vn(ROWS[rows - 1][1]) + " N"
    text(d, (780, 418), s, 64, RED, alpha=a)

def table(d, rows, a=1.0, y0=500):
    card(d, (520, y0, 1040, y0 + 400), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    for i in range(rows):
        y = y0 + 60 + i * 120
        text(d, (550, y), LABS[i], 56, INK, anchor="lm", alpha=a)
        text(d, (1010, y + 52), vn(ROWS[i][1]) + " N", 58, RED, anchor="rm", alpha=a)

def s_do(img, d, t, sc):
    f, moving, rows = do_state(t)
    fr = t_model(f)
    scene(img, d, f, fr, stream=1.0 if (f > 0.02 and any(a_ <= t < b_ for a_, b_ in MOVES)) else 0.0)
    readout(d, rows, moving); table(d, rows)
    if rows == 3:
        card(d, (520, 930, 1040, 1100), fill=(239, 246, 255), outline=BLUE, r=26, w=4)
        text(d, (780, 975), "nước tràn: 100 cm³", 56, BLUE)
        text(d, (780, 1050), "nặng 0,98 N", 56, BLUE)

def _kiem_dong_bo():
    """Moi 0,05 s: khi dung yen, kim (mo hinh) = o so = hang cuoi bang (lech <= 0,006 N); khong chay qua cuoi canh."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []; t = 0.0
    while t < sc["T"]:
        f, moving, rows = do_state(t)
        if rows and not moving:
            fr, fk, _, _ = ROWS[rows - 1]
            if abs(f - fr) > 1e-9 or abs(t_model(f) - ROWS[rows - 1][1]) > 0.006: bad.append(round(t, 2))
        t += 0.05
    for fr, T, FA, _ in ROWS:
        if abs(t_model(fr) - T) > 0.006 or abs(1000 * G * fr * V - FA) > 0.006: bad.append(("kho", fr))
    if abs(RHO_V * V * G - P_N) > 1e-3: bad.append("P")
    if MOVES[1][1] + SETTLE + 1.2 > sc["T"]: bad.append("sat cuoi canh")
    return bad

# ---------------- canh 3: dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    tank(d); yt = scale_block(d, 1.0, ROWS[2][1]); block(img, d, yt, lab=False); cup(d, 1.0)
    ka = appear(t, -0.5, 0.4)
    card(d, (520, 290, 1040, 470), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), w=5)
    text(d, (780, 340), "Trọng lượng", 58, DGREEN, alpha=ka)
    text(d, (780, 415), "nước tràn", 58, DGREEN, alpha=ka)
    text(d, (780, 530), "Lực kế giảm 0,98 N", 56, RED, alpha=ka)
    text(d, (780, 600), "Nước tràn: 0,98 N", 56, BLUE, alpha=ka)
    kc = min(1.0, appear(t, 2.2, 0.2) * (1 - appear(t, M[1], 0.2)) + appear(t, M[1] + 2.6, 0.2))   # khoanh coc nuoc tran
    if kc > 0:
        x0c, y0c, x1c, y1c = CUP; d.ellipse([x0c - 40, y0c - 50, x1c + 40, y1c + 30], outline=A(ORANGE, kc), width=12)
    k2 = appear(t, M[1], 0.45)                       # ba luc len khoi nhom: T + F_A = P (do dai ti le)
    if k2 > 0:
        cx, cy = LX, yt + BH / 2; s = 62
        arrow(d, (cx - 40, cy), (cx - 40, cy - 0.98 * s), A(BLUE, k2), w=8, head=22)
        arrow(d, (cx + 40, cy), (cx + 40, cy - 1.67 * s), A(NAVY, k2), w=8, head=22)
        arrow(d, (cx, cy + 10), (cx, cy + 10 + 2.65 * s), A(RED, k2), w=8, head=22)
        kb = appear(t, M[1] + 2.6, 0.2)                # khoanh mui ten luc day
        if kb > 0: d.ellipse([cx - 80, cy - 0.98 * s - 40, cx, cy + 20], outline=A(ORANGE, kb), width=12)
        for j, (s1, c) in enumerate((("↑ lực đẩy", BLUE), ("↑ lực kế kéo", NAVY), ("↓ trọng lực", RED))):
            text(d, (540, 690 + j * 68), s1, 56, c, anchor="lm", alpha=k2)
        y0 = 1000 + (1 - k2) * 30
        card(d, (520, y0, 1040, y0 + 320), fill=A(WHITE, k2), outline=A(GREEN, k2), w=6)
        pill(d, 780, y0 + 58, "RÚT RA", GREEN, k2)
        text(d, (780, y0 + 145), "Lực đẩy =", 56, DGREEN, alpha=k2)
        text(d, (780, y0 + 210), "trọng lượng nước", 56, DGREEN, alpha=k2)
        text(d, (780, y0 + 275), "bị chiếm chỗ", 56, DGREEN, alpha=k2)

# ---------------- canh 4: bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    tank(d); yt = scale_block(d, 0.5, ROWS[1][1]); block(img, d, yt); cup(d, 0.5)
    x0, x1 = 520, 1040; cx = (x0 + x1) / 2
    if a1 > 0:
        card(d, (x0, 290, x1, 700), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, cx, 355, "BẪY", RED, a1)
        ks = clamp((t - M[1]) / 0.4); f = F(56)
        for j, q in enumerate(("“Chìm một nửa:", "lực đẩy vẫn", "0,98 N”")):
            yy = 450 + j * 78; lw = tw(d, q, f)
            text(d, (cx, yy), q, 56, mix(RED, GRAY, ks), alpha=a1)
            if ks > 0: d.line([(cx - lw / 2 - 6, yy + 2), (cx - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        ok = appear(t, M[1], 0.4) * a1
        if ok > 0:
            card(d, (x0, 730, x1, 850), fill=A(WHITE, ok), outline=A(NAVY, ok), w=4)
            text(d, (cx, 790), "Lực kế chỉ 2,16 N", 58, RED, alpha=ok)
        kv = appear(t, M[1] + 3.0, 0.45) * a1
        if kv > 0:
            card(d, (x0, 880, x1, 1020), fill=A((220, 252, 231), kv), outline=A(GREEN, kv), w=5)
            text(d, (cx, 950), "Lực đẩy chỉ 0,49 N", 58, DGREEN, alpha=kv)
    if k3 > 0:
        card(d, (x0, 290, x1, 700), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, cx, 360, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (cx, 470), "Mới thử một", 58, INK, alpha=k3)
        text(d, (cx, 545), "khối nhôm.", 58, INK, alpha=k3)
        text(d, (cx, 640), "Vật nổi thì sao?", 58, INK, alpha=k3)

# ---------------- canh 5: thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 300, 1040, 1100), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 375, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 490), "Cùng khối nhôm ấy,", 62, INK, alpha=k)
    text(d, (W / 2, 575), "chìm hẳn trong nước muối", 62, INK, alpha=k)
    text(d, (W / 2, 660), "khối lượng riêng 1200 kg/m³.", 62, INK, alpha=k)
    text(d, (W / 2, 770), "Lực kế chỉ bao nhiêu?", 64, DORANGE, alpha=k)
    seg_bar(d, 900, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + b_ + SETTLE, "tap") for a_, b_ in MOVES]
            + [(da["t0"] + 0.1, "ding"), (da["t0"] + da["M"][1], "tap"), (b["t0"] + b["M"][1], "buzz"),
               (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-luc-can-luc-nang-03", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Lực cản và lực nâng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Lực kế và bình tràn", draw=s_hook, tail=0.2, caps=[
   ("Bình đầy tới miệng vòi.", 3.2),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Hạ dần khối nhôm", draw=s_do, tail=0.3, caps=[
   ("Đợi kim đứng yên.", 3.8),
   ("Hứng nước tràn.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Giảm đúng bằng trọng lượng nước tràn.", 4.6),
   ("Lực đẩy = trọng lượng nước bị chiếm chỗ.", 5.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.0),
   ("Lực kế chỉ bao nhiêu?", 6.1),
   ("Chưa nói được.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự tính.", 7.2)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
