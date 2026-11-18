# Clip: tn-l11-dotansoam-02 - Do tan so am thoa bang dien thoai: ghi am, phong to dang song, dem chu ki (18/11/2026, lo 5)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dotansoam-02.json:
#   f nguon = 440 Hz (tham_so), N = 10 chu ki; so_lieu_mau t = 22,6 / 22,8 / 22,7 ms -> f = 442,5 / 438,6 / 440,5 Hz,
#   trung binh ~ 440,5 Hz. Kiem: _kiem_so().
# Bo cuc (do thi dang song theo t): man hinh ung dung ghi am (dai "ban ghi" + dang song phong to), chon doan 10 chu ki,
#   dem 1..10 tren tung chu ki, o doc t; bang Lan - t - f. Khac clip dotocdoam3 (hai micro + truc tre).
# Du doan (khung 6 o): "Am thoa 440 Hz. Doan 10 chu ki tren dang song dai co bao lau?"
#   A. khoang 2,3 ms  B. khoang 23 ms  C. khoang 0,23 s  D. khoang 4,4 s   -> dap an B (t do duoc 22,6-22,8 ms).
#   Hop Du doan trong mp4 chi co cau hoi + dang song khong co truc thoi gian (K10).
# Bay = hien_tuong_hay_sai[1]: quen doi ms ra s -> 10/22,6 = 0,44 Hz. (KHONG dung bay [0] "dem dinh": cau Bay 1 ngay sau
#   hop trong bai hoi dung y do - 6 dinh, 8,0 o, 0,5 ms/o -> 1 250 Hz; clip khong noi so nao cua cau do.)
# Cau chot (ghi trong kho ghi_chu): chi dem N = 2 chu ki, doc t van lech 0,1 ms (sai_so_do) -> f lech co 10 Hz
#   (2/4,445 ms = 449,9 ; 2/4,645 ms = 430,6); dem 10 chu ki chi lech co 2 Hz. So 2 va 0,1 ms chua hien tren man.
from engine import *
import copy

F0, N = 440, 10
ROWS = [(1, 22.6, 442.5), (2, 22.8, 438.6), (3, 22.7, 440.5)]
F_TB = 440.5
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

SCR_BG = (18, 26, 48); WAVE = (74, 222, 128); SEL = (250, 204, 21); GRID = (52, 64, 96); SCR_TXT = (190, 200, 225)
DGREEN = (10, 80, 40); HL = (255, 237, 213)

# ---------------- man hinh ung dung ghi am ----------------
PXMS = 34.0                      # px / ms tren dang song phong to
P = 1000.0 / F0 * PXMS           # 1 chu ki = 77,3 px
SX = 150                         # doan chon luon bat dau o mot dinh tai x = 150
AMP = [130, 112, 96]             # am thoa tat dan: doan sau bien do nho hon
WIN = [0.18, 0.5, 0.8]           # vi tri doan trong ban ghi (dai tren cung)

def screen(d, oy, amp, win, shift=0.0, sel=None, counts=0, label=True):
    """oy: dich doc. shift (px): dang song dang cuon. sel = (x0, x1) vung chon. counts: so chu ki da dem (0..10)."""
    X0, X1, Y0, Y1 = 60, 1020, 300 + oy, 800 + oy
    card(d, (X0, Y0, X1, Y1), fill=SCR_BG, r=30)
    # dai ban ghi: bao song tat dan + o vi tri doan dang xem
    by0, by1 = Y0 + 28, Y0 + 82
    if label: text(d, (X0 + 40, (by0 + by1) / 2), "bản ghi", 40, SCR_TXT, bold=False, anchor="lm")
    bx0, bx1 = X0 + 220, X1 - 40
    for i in range(60):
        x = lerp(bx0, bx1, i / 59); h = 22 * math.exp(-1.2 * i / 59) + 3
        d.line([(x, (by0 + by1) / 2 - h), (x, (by0 + by1) / 2 + h)], fill=GRID if i % 2 else (70, 110, 90), width=4)
    wx = lerp(bx0, bx1, win)
    d.rectangle([wx - 22, by0 - 4, wx + 22, by1 + 4], outline=SEL, width=4)
    # dang song phong to
    cy = Y0 + 335
    d.line([(X0 + 30, cy), (X1 - 30, cy)], fill=GRID, width=2)
    if sel:
        x0, x1 = sel
        d.rectangle([x0, cy - 145, x1, cy + 145], fill=(250, 204, 21, 60))
        d.line([(x0, cy - 145), (x0, cy + 145)], fill=SEL, width=5)
        if x1 - x0 > 3: d.line([(x1, cy - 145), (x1, cy + 145)], fill=SEL, width=5)
    pts = []
    for x in range(X0 + 30, X1 - 30, 3):
        pts.append((x, cy - amp * math.cos(2 * math.pi * (x - SX + shift) / P)))
    d.line(pts, fill=WAVE, width=5, joint="curve")
    for j in range(counts):   # so chu ki da dem, ghi tren tung chu ki
        text(d, (SX + (j + 0.5) * P, cy - 182), str(j + 1), 40, SEL)
    return cy

def readout(d, y, t_txt, ka=1.0):
    card(d, (60, y, 1020, y + 116), fill=WHITE, outline=LIGHT, w=3)
    text(d, (290, y + 58), f"N = {N} chu kì", 46, INK)
    d.line([(540, y + 24), (540, y + 92)], fill=LIGHT, width=3)
    text(d, (780, y + 58), t_txt, 46, BLUE if t_txt != "t = …" else MUTED)

# ---------------- canh 1: Du doan (K10: cau hoi + hinh, khong nut lua chon) ----------------
Q_AT = 1.1
def s_hook(img, d, t, sc):
    screen(d, 520, AMP[0], WIN[0])
    a = appear(t, Q_AT, 0.5)
    if a <= 0: return
    y0 = 250 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 215, "Âm thoa 440 Hz.\nĐoạn gồm 10 chu kì trên dạng sóng\ndài cỡ bao lâu?", 46, INK, maxw=920, alpha=a)
    text(d, (W / 2, y0 + 385), "Chọn đáp án ở khung câu hỏi", 38, MUTED, bold=False, alpha=a)
    tc, tend = Q_AT + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 450, 940, y0 + 462], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 450, 140 + 800 * (1 - p), y0 + 462], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (chon doan, dem chu ki, doc t, ghi bang) ----------------
SEG = [(0.8, 2.4), (4.6, 1.4), (7.3, 1.4)]   # (bat dau keo vung chon, thoi gian keo) moi lan
SCROLL = 0.5                                 # cuon sang doan moi ngay sau khi ghi xong lan truoc (+0,7 s)
T_ANS = 9.4
def do_state(t):
    """-> (lan k, shift px, bien do, x1 vung chon hoac None, so chu ki da dem, chuoi t, so hang da ghi)."""
    k = 0
    for i in range(1, len(SEG)):
        if t >= SEG[i - 1][0] + SEG[i - 1][1] + 0.7: k = i
    s, g = SEG[k]; shift, amp, scrolling = 0.0, AMP[k], False
    if k > 0:   # cuon tu doan truoc sang doan k: dich 3 chu ki (lien mach ca hai dau), bien do nho dan
        tc = SEG[k - 1][0] + SEG[k - 1][1] + 0.7
        q = clamp((t - tc) / SCROLL)
        if q < 1: scrolling = True; shift = ease(q) * 3 * P; amp = lerp(AMP[k - 1], AMP[k], ease(q))
    rows = sum(1 for (s2, g2) in SEG if t >= s2 + g2 - 1e-9)
    if t < s or scrolling: return k, shift, amp, None, 0, "t = …", rows
    q = clamp((t - s) / g)
    L = ROWS[k][1] * PXMS
    x1 = SX + L * ease(q)
    cnt = min(N, int((x1 - SX) / P + 1e-6))
    done = t >= s + g - 1e-9
    return k, shift, amp, x1, (N if done else cnt), (f"t = {vn(ROWS[k][1])} ms" if done else "t = …"), rows

TX = [190, 540, 860]; TY0, RH = 1020, 92
def table(d, rows, kf=None, hl=-1, TY0=TY0):
    """kf: danh sach do hien cot f moi hang (None = chua co cot f)."""
    if rows <= 0: return                         # an bang toi khi co hang 1
    card(d, (60, TY0 - 56, 1020, TY0 + 46 + rows * RH + 16), fill=WHITE, outline=LIGHT, w=3)   # co theo so hang
    text(d, (TX[0], TY0), "Lần", 40, INK); text(d, (TX[1], TY0), "t (ms)", 40, INK)
    if kf is not None: text(d, (TX[2], TY0), "f (Hz)", 40, INK)
    d.line([(80, TY0 + 36), (1000, TY0 + 36)], fill=LIGHT, width=3)
    for j in range(rows):
        y = TY0 + 46 + RH * j + RH / 2
        if j == hl: d.rounded_rectangle([80, y - 38, 1000, y + 38], radius=14, fill=HL)
        n, tt, f = ROWS[j]
        text(d, (TX[0], y), str(n), 44, NAVY); text(d, (TX[1], y), vn(tt), 44, INK)
        if kf is not None and kf[j] > 0: text(d, (TX[2], y), vn(f), 44, BLUE, alpha=kf[j])

def s_do(img, d, t, sc):
    k, shift, amp, x1, cnt, ttxt, rows = do_state(t)
    screen(d, 0, amp, WIN[k], shift=shift, sel=(SX, x1) if x1 is not None else None, counts=cnt)
    readout(d, 830, ttxt)
    hl = rows - 1 if rows > 0 and ttxt != "t = …" else -1
    table(d, rows, hl=hl)
    ka = appear(t, T_ANS, 0.15)
    if ka > 0:
        card(d, (60, 1420, 1020, 1530), fill=A((21, 110, 52), ka), r=30)
        text(d, (W / 2, 1475), "ĐÁP ÁN · khoảng 22,7 ms", 44, WHITE, alpha=ka)

# ---------------- canh 3: Rut ra (f = N/t, doi ms ra s) + Chua noi duoc ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, 0.2, 0.45)
    card(d, (50, 250, 1030, 560), fill=A(WHITE, k1), outline=A(BLUE, k1), w=6)
    text(d, (W / 2, 330), "f = N / t   (t tính bằng giây)", 48, BLUE, alpha=k1)
    k2 = appear(t, 0.9, 0.45)
    text(d, (W / 2, 470), "10 / 0,0226 s ≈ 442,5 Hz", 50, INK, alpha=k2)
    kf = [appear(t, 0.9, 0.4), appear(t, M[1] - 0.2, 0.4), appear(t, M[1] + 0.3, 0.4)]
    table(d, 3, kf=kf, hl=0 if t < M[1] - 0.2 else -1, TY0=690)
    km = appear(t, M[1] + 0.9, 0.45)
    if km > 0:
        card(d, (60, 1080, 1020, 1190), fill=A((236, 253, 243), km), outline=A(GREEN, km), w=5)
        text(d, (W / 2, 1135), "Trung bình ≈ 440,5 Hz", 48, DGREEN, alpha=km)
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y = 1250 + (1 - k3) * 20
        card(d, (50, y, 1030, y + 250), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 55), "Chưa nói được", 42, NAVY, alpha=k3)
        ctext(d, y + 165, "Giọng nói, sóng không đều: đếm sao?", 44, INK, maxw=900,
              alpha=k3 * appear(t, M[2] + 0.3, 0.4))

# ---------------- canh 4: Bay - quen doi ms ra s ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.1, 0.4)
    card(d, (40, 260, 1040, 640), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(RED, a1), r=32)
    text(d, (W / 2, 322), "BẪY", 38, WHITE, alpha=a1)
    s1 = "f = 10 / 22,6 = 0,44 Hz"
    text(d, (W / 2, 450), s1, 52, RED, alpha=a1)
    ks = clamp((t - (M[1] + 0.5)) / 0.4)
    if ks > 0:
        lw = tw(d, s1, F(52))
        d.line([(W / 2 - lw / 2 - 8, 452), (W / 2 - lw / 2 - 8 + (lw + 16) * ks, 452)], fill=RED, width=7)
        text(d, (W / 2, 560), "✗ chia cho số mili giây", 44, RED, alpha=ks)
    # hinh: doan 10 chu ki va nhan t (cung luc voi phu de dau)
    a2 = appear(t, 0.3, 0.4)
    if a2 > 0:
        X0, X1, cy = 90, 990, 860
        card(d, (60, 700, 1020, 1060), fill=A(SCR_BG, a2), r=26)
        x0, x1 = 160, 160 + 10 * P * 0.95
        d.rectangle([x0, cy - 120, x1, cy + 120], fill=(250, 204, 21, int(60 * a2)))
        pts = [(x, cy - 95 * math.cos(2 * math.pi * (x - x0) / (P * 0.95))) for x in range(X0 + 10, X1 - 10, 3)]
        d.line(pts, fill=A(WAVE, a2), width=5, joint="curve")
        arrow(d, ((x0 + x1) / 2, 1000), (x0 + 6, 1000), A(SEL, a2), w=4, head=16)
        arrow(d, ((x0 + x1) / 2, 1000), (x1 - 6, 1000), A(SEL, a2), w=4, head=16)
        lw = tw(d, "22,6 ms", F(42)) + 30
        d.rectangle([(x0 + x1) / 2 - lw / 2, 975, (x0 + x1) / 2 + lw / 2, 1025], fill=A(SCR_BG, a2))
        text(d, ((x0 + x1) / 2, 1000), "22,6 ms", 42, SEL, alpha=a2)
    ka = appear(t, M[1] + 1.3, 0.5)
    if ka > 0:
        card(d, (60, 1130, 1020, 1430), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5)
        text(d, (W / 2, 1210), "✓ 22,6 ms = 0,0226 s", 48, DGREEN, alpha=ka)
        text(d, (W / 2, 1330), "0,44 Hz: tai không nghe thấy", 44, INK, alpha=ka)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 290, 1020, 590), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 440, "Đếm nhiều chu kì\nđể sai số nhỏ", 50, GREEN, maxw=900, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 2.9, 0.5)
    yb = lerp(1000, 1270, kh)                     # hop THU NGHI co theo noi dung, dai ra khi goi y hien
    card(d, (40, 650, 1040, yb), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 680, W / 2 + pw / 2, 744), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 712), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 865, "Chỉ đếm 2 chu kì, đọc t\nvẫn lệch 0,1 ms. Tần số\nlệch cỡ bao nhiêu Hz?", 44, INK, maxw=950, alpha=appear(t, M[0] + 0.4, 0.5))
    if kh <= 0: return
    card(d, (110, 1010, 970, 1230), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1065, "Gợi ý", 40, (154, 52, 18), alpha=kh)
    ctext(d, 1160, "Một chu kì dài 1/f", 42, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + Q_AT, "open"), (h["t0"] + h["T"] - 0.9, "ding")]
    out += [(do["t0"] + s + g, "tick") for s, g in SEG]
    out += [(do["t0"] + T_ANS, "ding"), (r["t0"] + 0.9, "tap"), (b["t0"] + 0.1, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

# ---------------- kiem so va dong bo ----------------
def _kiem_so():
    bad = []
    for n, tt, f in ROWS:
        if abs(N / (tt / 1000) - f) > 0.05: bad.append((n, tt, f))
        if abs(tt - N * 1000 / F0) > 0.15: bad.append(("t xa mo hinh", tt))
    if abs(sum(r[2] for r in ROWS) / 3 - F_TB) > 0.05: bad.append("trung binh")
    if abs(10 / 22.6 - 0.44) > 0.005: bad.append("bay 0,44")
    if abs(10 / 0.0226 - 442.5) > 0.05: bad.append("cong thuc 442,5")
    hi, lo = 2 / (2000 / F0 - 0.1) * 1000, 2 / (2000 / F0 + 0.1) * 1000          # cau chot: N = 2, lech 0,1 ms
    if not (9 < hi - F0 < 11 and 9 < F0 - lo < 11): bad.append(("chot N=2", hi, lo))
    hi10 = 10 / (10000 / F0 - 0.1) * 1000
    if not (1.5 < hi10 - F0 < 2.5): bad.append(("chot N=10", hi10))
    return bad

def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        k, shift, amp, x1, cnt, ttxt, rows = do_state(t)
        done = ttxt != "t = …"
        if done:
            if ttxt != f"t = {vn(ROWS[k][1])} ms" or rows != k + 1 or cnt != N: bad.append((round(t, 2), "ghi", k, rows))
            if abs((x1 - SX) - ROWS[k][1] * PXMS) > 0.5: bad.append((round(t, 2), "vung chon", x1))
        else:
            if rows != k: bad.append((round(t, 2), "hang som", k, rows))
        if cnt > 0 and x1 is not None and x1 - SX < cnt * P - 0.2 * PXMS: bad.append((round(t, 2), "dem truoc vung chon"))
        t += 0.05
    if T_ANS < SEG[-1][0] + SEG[-1][1]: bad.append("dap an truoc lan do cuoi")
    return bad

CLIP = dict(id="tn-l11-dotansoam-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Đo tần số âm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Âm thoa và điện thoại", draw=s_hook, tail=0.4, caps=[
   ("Ghi âm tiếng âm thoa.", 2.6),
   ("Nghĩ trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Phóng to, chọn đúng 10 chu kì.", 4.8),
   ("Làm lại ở hai đoạn khác.", 5.8)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.6, caps=[
   ("Đổi t ra giây rồi chia.", 2.8),
   ("Ba lần cho số gần nhau.", 2.8),
   ("Còn bỏ ngỏ.", 4.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=1.0, caps=[
   ("Lỗi hay gặp.", 2.5),
   ("Quên đổi mili giây ra giây.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__":
    print("số lệch:", _kiem_so() or "không")
    print("lệch đồng bộ:", _kiem_dong_bo() or "không")
