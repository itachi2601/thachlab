# Clip: tn-l10-luc-can-luc-nang-03 - Luc ke + binh tran: luc ke giam bao nhieu khi khoi nhom chim han (lo 8, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-luc-can-luc-nang-03.json:
#   so_lieu_mau (phan chim f, T N, F_A N): 0 2,65 0 ; 0,5 2,16 0,49 ; 1 1,67 0,98 ; quan_sat: nuoc tran 100 cm3, nang 0,98 N.
#   tham_so: V = 100 cm3, rho nhom 2700, rho long 700-1300 (cau chot 1200), g = 9,8 ; mo_hinh T = P - rho.g.f.V.
#   Luc ke 5 N (dung_cu) ve bang luc_ke() engine, vach 0,2 N (brief lo 8); kim theo mo hinh, so doc lay tu kho.
# Du doan (K10: chi cau hoi + hinh): khoi nhom chim han, so chi luc ke giam mot luong bang
#   A. trong luong nuoc tran ra coc (DUNG) ; B. trong luong khoi nhom ; C. hieu hai trong luong tren.
# KHONG tra loi san: Cau 5 (III, ha sau 20 -> 60 cm) -> clip KHONG ha sau them, khong noi "khong doi theo do sau" ;
#   Cau 6 (V, 5,4 N nhung mot nua) -> clip khong tinh ca 5,4 N ; Cau 4 (go noi, phan chim) -> bay chi dung so cua clip.
# Bay = hien_tuong_hay_sai[1] (dung the tich ca vat khi chi chim mot phan): "chim mot nua: luc day van 0,98 N".
# Cau chot (ca tu suy, ghi trong ghi_chu kho): chim han trong nuoc muoi rho = 1200 -> F_A = 1,18 N, T = 1,47 N.
#   So 1200 / 1,47 chua hien tren man ; hop chot KHONG ghi cong thuc F_A = rho.g.V.
# Bo cuc: luc ke treo doc ben trai (vach ben trai) tren binh tran ; coc hung ben phai duoi ; o so + bang ben phai tren.
#   Dong bo kim <-> o so <-> hang bang: _kiem_dong_bo().
from engine import *

P_N, V, RHO_V, G = 2.646, 1e-4, 2700, 9.8
ROWS = [(0.0, 2.65, 0.0, "ngoài không khí"), (0.5, 2.16, 0.49, "chìm một nửa"), (1.0, 1.67, 0.98, "chìm hẳn")]   # so_lieu_mau
FMAX = 3.0                                       # 3 N, vach 0,1 N (~14 px): doc duoc toi 0,01 N bang uoc
DRED = (185, 28, 28); NOTE = (60, 64, 84)
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
    luc_ke(d, Q, 0, 20, 20 + BODY, FMAX, f_read, nho=0.1, ben=-1, co=44, alpha=a)
    yt = yh + ROPE
    d.line([(LX, yh + 10), (LX, yt)], fill=NAVY, width=4)
    return yt                                    # dinh khoi

def block(img, d, yt, a=1.0, lab=True):
    d.rectangle([LX - BW / 2, yt, LX + BW / 2, yt + BH], fill=AL, outline=AL_D, width=4)
    yc = min(max(WS, yt), yt + BH)               # phan chim: phu mau nuoc mo
    if yc < yt + BH - 6: d.rectangle([LX - BW / 2 + 3, yc, LX + BW / 2 - 3, yt + BH - 3], fill=A(WAT_D, 0.28))
    if lab: text(d, (LX, yt + BH / 2), "nhôm", 44, NAVY)

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

def scene(img, d, f, f_read, vol=None, stream=0.0):
    tank(d); yt = scale_block(d, f, f_read); block(img, d, yt)
    cup(d, f if vol is None else vol, stream)
    return yt

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    scene(img, d, 0.0, None)
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    x0, x1 = 520, 1040; cx = (x0 + x1) / 2; y0 = 290 + (1 - a) * 30
    card(d, (x0, y0, x1, y0 + 820), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (cx - pw / 2, y0 + 26, cx + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (cx, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Khối nhôm chìm hẳn,", "nước tràn ra cốc.")):
        text(d, (cx, y0 + 160 + j * 64), s, 46, INK, alpha=a)
    for j, s in enumerate(("Số chỉ lực kế", "giảm một lượng", "bằng gì?")):
        text(d, (cx, y0 + 400 + j * 70), s, 50, INK, alpha=a)
    text(d, (cx, y0 + 660), "Chọn đáp án", 40, NOTE, alpha=a)
    text(d, (cx, y0 + 710), "ở khung câu hỏi", 40, NOTE, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([x0 + 50, y0 + 776, x1 - 50, y0 + 790], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([x0 + 50, y0 + 776, x0 + 50 + (x1 - x0 - 100) * (1 - p), y0 + 790], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: tien hanh ----------------
MOVES = [(1.8, 3.4), (5.0, 6.6)]                 # (bat dau ha, xong) toi f = 0,5 roi f = 1
SETTLE = 0.5                                     # doi kim dung yen roi moi ghi
def do_state(t):
    """-> (f, dang ha?, so hang da ghi)."""
    f, moving = 0.0, False
    for i, (a, b) in enumerate(MOVES):
        if t >= a:
            f = lerp(ROWS[i][0], ROWS[i + 1][0], ease((t - a) / (b - a))); moving = t < b + SETTLE
    rows = 1 if t >= 0.6 else 0
    for i, (a, b) in enumerate(MOVES):
        if t >= b + SETTLE: rows = i + 2
    return f, moving, rows

def readout(d, rows, moving, a=1.0):
    card(d, (560, 290, 1040, 500), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (800, 334), "số chỉ", 44, NOTE, alpha=a)
    text(d, (800, 384), "(ước giữa hai vạch)", 40, NOTE, alpha=a)
    s = "…" if (moving or rows == 0) else vn(ROWS[rows - 1][1]) + " N"
    text(d, (800, 450), s, 60, RED, alpha=a)

def table(d, rows, a=1.0, y0=520):
    card(d, (560, y0, 1040, y0 + 380), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    for i in range(rows):
        y = y0 + 56 + i * 110
        text(d, (590, y), ROWS[i][3], 44, INK, anchor="lm", alpha=a)
        text(d, (1010, y + 48), vn(ROWS[i][1]) + " N", 46, RED, anchor="rm", alpha=a)

def s_do(img, d, t, sc):
    f, moving, rows = do_state(t)
    fr = t_model(f)
    scene(img, d, f, fr, stream=1.0 if any(a_ <= t < b_ for a_, b_ in MOVES) else 0.0)
    readout(d, rows, moving); table(d, rows)
    k = appear(t, MOVES[1][1] + SETTLE + 0.4, 0.4)
    if k > 0:
        card(d, (560, 1180, 1040, 1340), fill=A((239, 246, 255), k), outline=A(BLUE, k), r=26, w=4)
        text(d, (800, 1225), "nước tràn: 100 cm³", 44, BLUE, alpha=k)
        text(d, (800, 1295), "nặng 0,98 N", 44, BLUE, alpha=k)

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
    ka = appear(t, 0.1, 0.4)
    card(d, (560, 290, 1040, 470), fill=A(NAVY, ka), r=30)
    text(d, (800, 340), "ĐÁP ÁN ·", 42, WHITE, alpha=ka)
    text(d, (800, 412), "trọng lượng nước tràn", 42, WHITE, alpha=ka)
    k1 = appear(t, 0.6, 0.4)
    text(d, (800, 530), "Lực kế giảm:", 44, INK, alpha=k1)
    text(d, (800, 594), "2,65 − 1,67 = 0,98 N", 46, RED, alpha=k1)
    text(d, (800, 670), "Nước tràn:", 44, INK, alpha=k1)
    text(d, (800, 734), "0,98 N", 46, BLUE, alpha=k1)
    k2 = appear(t, M[1] - 0.2, 0.45)                 # ba luc len khoi nhom: T + F_A = P (do dai ti le)
    if k2 > 0:
        cx, cy = LX, yt + BH / 2; s = 62
        arrow(d, (cx - 40, cy), (cx - 40, cy - 0.98 * s), A(BLUE, k2), w=8, head=22)
        arrow(d, (cx + 40, cy), (cx + 40, cy - 1.67 * s), A(NAVY, k2), w=8, head=22)
        arrow(d, (cx, cy + 10), (cx, cy + 10 + 2.65 * s), A(RED, k2), w=8, head=22)
        for j, (s1, c) in enumerate((("lực đẩy nước: lên nhôm", BLUE), ("lực kế kéo: lên nhôm", NAVY), ("trọng lực: lên nhôm", RED))):
            text(d, (560, 820 + j * 60), s1, 44, c, anchor="lm", alpha=k2)
    kr = appear(t, M[1] + 2.4, 0.45)
    if kr <= 0: return
    y0 = 1010 + (1 - kr) * 30
    card(d, (540, y0, 1050, y0 + 300), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
    pw = tw(d, "RÚT RA", F(40)) + 52
    card(d, (795 - pw / 2, y0 + 24, 795 + pw / 2, y0 + 88), fill=A(GREEN, kr), r=32)
    text(d, (795, y0 + 56), "RÚT RA", 40, WHITE, alpha=kr)
    for j, s1 in enumerate(("Lực đẩy = trọng lượng", "nước bị chiếm chỗ")):
        text(d, (795, y0 + 160 + j * 70), s1, 46, INK, alpha=kr)

# ---------------- canh 4: bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    tank(d); yt = scale_block(d, 0.5, ROWS[1][1]); block(img, d, yt); cup(d, 0.5)
    if a1 > 0:
        x0, x1 = 540, 1050; cx = (x0 + x1) / 2
        card(d, (x0, 290, x1, 870), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (cx - pw / 2, 318, cx + pw / 2, 382), fill=A(DRED, a1), r=32)
        text(d, (cx, 350), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 2.0) / 0.4); f = F(46)
        for j, q in enumerate(("“Chìm một nửa:", "lực đẩy vẫn", "0,98 N”")):
            yy = 470 + j * 64; lw = tw(d, q, f)
            text(d, (cx, yy), q, 46, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0: d.line([(cx - lw / 2 - 6, yy + 2), (cx - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        if ks > 0: text(d, (x0 + 50, 470), "✗", 60, DRED, alpha=a1 * ks)
        k2 = appear(t, 2.4, 0.45) * a1
        text(d, (cx, 720), "Lực kế: 2,16 N", 46, INK, alpha=k2)
        text(d, (cx, 800), "lực đẩy nhỏ hơn 0,98 N", 46, GREEN, alpha=k2)
    if k3 > 0:
        x0, x1 = 540, 1050
        card(d, (x0, 290 + (1 - k3) * 30, x1, 830), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, ((x0 + x1) / 2, 370), "Chưa nói được", 46, NAVY, alpha=k3)
        for j, (s1, s2) in enumerate((("• Chất lỏng", "khác thì sao?"), ("• Vật nổi:", "chưa thử"))):
            kk = k3 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (x0 + 30, 500 + 190 * j), s1, 44, INK, anchor="lm", alpha=kk)
            text(d, (x0 + 30, 562 + 190 * j), s2, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    """Chot (khong ghi cong thuc) -> THU NGHI: nuoc muoi 1200 kg/m3, chim han; goi y tre 2,6 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 420, "Chìm càng nhiều, lực đẩy càng lớn", 50, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1340), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    ctext(d, 830, "Nhúng chìm hẳn vào nước muối 1200 kg/m³: lực kế chỉ bao nhiêu?", 48, INK, maxw=900, alpha=kq)
    ctext(d, 980, "ngoài không khí 2,65 N · nước tràn 100 cm³", 44, NOTE, maxw=920, alpha=kq)
    kh = appear(t, M[0] + 2.6, 0.5)
    if kh > 0:
        card(d, (110, 1060, 970, 1290), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1115, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1215, "Nước: 1000 kg/m³", 46, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + 0.6, "tap")] + [(do["t0"] + b_ + SETTLE, "tap") for a_, b_ in MOVES]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-luc-can-luc-nang-03", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Lực cản và lực nâng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Lực kế và bình tràn", draw=s_hook, tail=0.3, caps=[
   ("Bình đầy tới miệng vòi.", 3.2),
   ("Nghĩ trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Hạ dần khối nhôm", draw=s_do, tail=0.6, caps=[
   ("Đợi kim đứng yên.", 4.4),
   ("Hứng nước tràn.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.9, caps=[
   ("So hai số.", 3.6),
   ("Ba lực.", 5.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 4.2),
   ("Còn bỏ ngỏ.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 8.2)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
