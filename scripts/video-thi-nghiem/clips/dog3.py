# Clip: tn-l10-do-g-03 - Dem khung hinh: sai so dung cu khi dung dien thoai quay cham (1/11/2026; dung lai 27/11/2026 theo
# cong moi viec 4: --do-chu 0 LOI, chu >= 56 px khi ve, Du doan khong nut, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-g-03.json (_kiem_so() doi chieu), s = 0,500 m:
#   240 khung/s -> n = 77, +-1 khung 0,0042 s ; 30 khung/s -> n = 10, +-1 khung 0,0333 s. Dong ho cong quang chia 0,001 s.
#   Mo hinh: n = khung dau tien bi cham/qua moc = ceil(fps . sqrt(2s/g)), g = 9,8 -> 240: 77 ; 30: 10 ; 480: 154 ; 120: 39.
#   (Hang 60 khung/s cua kho ghi 19 nhung ceil(60 . 0,3194) = 20: lech mo hinh -> clip KHONG dung 60 khung/s; da bao.)
# Du doan (moi, vi Quan sat/Rut ra cua bai da noi n = 77 va 1/240 > 0,001 s): 240 khung/s dem 77 khung; quay 30 khung/s
#   dem duoc bao nhieu? -> 10 (it hon 8 lan). Khung: A 10 / B 19 / C 77 / D 616 khung.
# Bay = hien_tuong_hay_sai thu 2: dem tu khung bi con nam yen (theo mo hinh, 5 khung thua) -> n = 82 -> t ~ 0,342 s.
#   Khong noi tu du / bi roi muon (Cau 4 cua bai).
# Thu nghi (= cau_chot khung web, s = 0,700 m trong mien 0,2-1,0; 240 khung/s): t = sqrt(1,4/9,8) = 0,378 s -> n = 91.
#   Hai buoc; 91 khong hien. Khong dung 0,800 m (bai co cau 0,800 m / 0,404 s).
from engine import *

G, S = 9.8, 0.500
N240, N30, FA, FB, EXTRA = 77, 10, 240, 30, 5
CH_S = 0.700

def nf(fps, s): return math.ceil(fps * math.sqrt(2 * s / G) - 1e-9)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-do-g-03.json")))
    h = {r[0]: r for r in k["so_lieu_mau"]["hang"]}
    assert h[FA][1] == N240 == nf(FA, S) and h[FB][1] == N30 == nf(FB, S) and h[480][1] == nf(480, S) and h[120][1] == nf(120, S)
    assert f"{1 / FA:.4f}" == "0.0042" and f"{1 / FB:.3f}" == "0.033" and f"{N240 / FA:.3f}" == "0.321" and f"{N30 / FB:.3f}" == "0.333"
    assert f"{(N240 + EXTRA) / FA:.3f}" == "0.342"
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}; assert ts["s"]["min"] <= CH_S <= ts["s"]["max"]
    assert nf(FA, CH_S) == 91 and round(N240 * CH_S / S) == 108 and round(N240 * (CH_S / S) ** 2) == 151
_kiem_so()

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")
STEEL = (110, 120, 140); STEEL_L = (200, 205, 216); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
DRED = (185, 28, 28); DTEAL = (15, 118, 110); EMPTY = (148, 140, 128); C_S = (37, 99, 235); C_F = (194, 65, 12)
FILM = (38, 38, 46)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 190 + i * 145
        if i < on: card(d, (x, y, x + 120, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 120, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def badge(d, y, s, col, a=1.0):
    pw = tw(d, s, F(58)) + 64
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 82), fill=A(col, a), r=40)
    text(d, (W / 2, y + 41), s, 58, WHITE, alpha=a)

def ball(d, x, y, a=1.0, r=20):
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(STEEL, a), outline=A(NAVY, a), width=2)
    d.ellipse([x - 9, y - 10, x - 2, y - 3], fill=A(STEEL_L, a))

# ---------------- hai lan quay: 240 khung/s (trai) va 30 khung/s (phai) ----------------
SY0, SPX = 345, 1560.0
def SYp(s): return SY0 + SPX * s
def lane(d, x0, fps, tf, n_show, strobe, bottom=1290):
    """tf: thoi gian roi that (s) da troi; n_show: so hien o bo dem (None -> '?')."""
    card(d, (x0, 215, x0 + 490, bottom), fill=WHITE, outline=LIGHT, w=3)
    text(d, (x0 + 245, 262), f"{fps} khung/s", 58, C_F)
    rx = x0 + 110
    d.rectangle([rx, SY0 - 6, rx + 28, SYp(S) + 8], fill=WOOD, outline=WOOD_D, width=3)
    for i in range(6): d.line([(rx, SYp(i / 10)), (rx + 24, SYp(i / 10))], fill=INK, width=3)
    text(d, (rx - 12, SY0), "0", 56, C_S, anchor="rm"); text(d, (rx - 12, SYp(S)), "0,5", 56, C_S, anchor="rm")
    for xx in range(rx + 40, x0 + 470, 26): d.line([(xx, SYp(S)), (xx + 13, SYp(S))], fill=RED, width=4)
    text(d, (x0 + 470, SYp(S) - 45), "s (m)", 56, C_S, anchor="rm")
    bx = x0 + 300
    if strobe:
        k = 0
        while k / fps <= tf + 1e-9:
            s = 0.5 * G * (k / fps) ** 2
            if SYp(s) < bottom - 150: ball(d, bx, SYp(s) - 20, 1.0 if abs(k / fps - tf) < 1 / fps else 0.45)
            k += 1
    else:
        s = min(0.5 * G * tf * tf, 0.53); ball(d, bx, SYp(s) - 20)
    card(d, (x0 + 20, bottom - 125, x0 + 470, bottom - 20), fill=NAVY, r=24)
    text(d, (x0 + 245, bottom - 72), "n = " + ("?" if n_show is None else str(n_show)) + " khung", 60, YELLOW)

TFALL = math.sqrt(2 * S / G)
SLOW, RUN0 = 15.0, 0.4
def counts(tf): return min(N240, math.floor(tf * FA)), min(N30, math.floor(tf * FB))

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    lane(d, 40, FA, TFALL, N240, False); lane(d, 550, FB, 0.0, None, True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 620 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    badge(d, y0 + 26, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 175), "240 khung/s: đếm được 77.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "30 khung/s: bao nhiêu khung?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 350, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (chieu cham x10, hai lan song song) ----------------
def s_do(img, d, t, sc):
    tf = clamp((t - RUN0) / SLOW, 0, TFALL)
    na, nb = counts(tf)
    if tf >= TFALL - 1e-9: na, nb = N240, N30
    lane(d, 40, FA, tf, na, False); lane(d, 550, FB, tf, nb, True)
    card(d, (40, 1310, 1040, 1430), fill=NAVY, r=30)
    text(d, (W / 2, 1370), "chiếu chậm ×15", 58, YELLOW)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = 1.0
    for x0, fps, n in ((40, FA, N240), (550, FB, N30)):
        card(d, (x0, 600, x0 + 490, 1000), fill=NAVY, r=30)
        text(d, (x0 + 245, 710), f"{fps} khung/s", 58, ORANGE)
        text(d, (x0 + 245, 860), f"n = {n} khung", 64, YELLOW)
    text(d, (540, 1140), "240 : 30 = 8  →  77 : 8 ≈ 10", 58, C_F)
    card(d, (40, 215, 1040, 560), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=6)
    badge(d, 240, "ĐÁP ÁN", DTEAL, ka)
    text(d, (W / 2, 400), "10 khung,", 64, DTEAL, alpha=ka)
    text(d, (W / 2, 485), "ít hơn 8 lần", 64, DTEAL, alpha=ka)
    k2 = appear(t, M[1] + 0.1, 0.45)
    card(d, (40, 1310, 1040, 1590), fill=A(WHITE, k2), outline=A(C_F, k2), w=5)
    text(d, (W / 2, 1390), "t = 77 : 240 ≈ 0,321 s", 60, INK, alpha=k2)
    text(d, (W / 2, 1500), "t = 10 : 30 ≈ 0,333 s", 60, INK, alpha=k2)

# ---------------- canh 4: Rut ra (lech 1 khung = 1/fps) ----------------
BARS = [("đồng hồ", 0.001, "0,001 s", DTEAL), ("240 khung/s", 1 / FA, "0,0042 s", C_F), ("30 khung/s", 1 / FB, "0,033 s", DRED)]
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 330), "Lệch 1 khung", 60, INK)
    text(d, (W / 2, 440), "= 1 : (số khung/s)", 60, INK)
    card(d, (40, 580, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    for i, (lab, v, vs, col) in enumerate(BARS):
        y = 790 + i * 260; k = ease(clamp((t - 1.4) / 0.8)) if i < 2 else ease(clamp((t - M[1] - 0.1) / 0.8))
        text(d, (90, y), lab, 58, col, anchor="lm")
        L = max(14, 860 * v / (1 / FB)) * k
        if L > 0: d.rounded_rectangle([90, y + 50, 90 + L, y + 110], radius=12, fill=col)
        text(d, (90 + max(L, 14) + 20 if L < 600 else 90 + L - 20, y + 80), vs, 58, col if L < 600 else WHITE,
             anchor="lm" if L < 600 else "rm", alpha=1.0 if k > 0.95 else 0.0)

# ---------------- canh 5: Bay (dem tu luc bi nam yen) ----------------
def strip(d, y, n_still, hi, col):
    """Dai 8 khung: n_still khung dau bi nam yen, sau do roi."""
    for i in range(8):
        x = 70 + i * 120
        card(d, (x, y, x + 105, y + 200), fill=FILM, r=10)
        d.rectangle([x + 10, y + 12, x + 95, y + 188], fill=(235, 238, 244))
        k = max(0, i - n_still + 1) if i >= n_still else 0
        by = y + 45 + min(130, 9 * k * k)
        ball(d, x + 52, by, r=16)
        if i < hi: d.rounded_rectangle([x - 4, y - 4, x + 109, y + 204], radius=12, outline=col, width=6)

def s_bay(img, d, t, sc):
    M = sc["M"]; ok = t >= M[1] - 0.1
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=DRED, w=6)
    text(d, (W / 2, 300), "✗ Tính cả lúc nằm yên:", 60, DRED)
    text(d, (W / 2, 420), "n = 82 → t ≈ 0,342 s", 60, DRED)
    card(d, (40, 580, 1040, 1290), fill=WHITE, outline=LIGHT, w=3)
    strip(d, 760, EXTRA, 0 if ok else EXTRA, DRED)
    if not ok: text(d, (W / 2, 1060), "5 khung thừa", 58, DRED)
    if ok:
        x = 70 + EXTRA * 120; wpx = 5 + int(4 * (0.5 + 0.5 * math.sin(t * 5)))
        d.rounded_rectangle([x - 4, 756, x + 109, 964], radius=12, outline=DTEAL, width=wpx)
        arrow(d, (x + 52, 1100), (x + 52, 990), DTEAL, w=7, head=22)
        text(d, (x + 52, 1185), "khung bi rời", 56, DTEAL)
        card(d, (40, 1310, 1040, 1590), fill=WHITE, outline=DTEAL, w=6)
        text(d, (W / 2, 1395), "✓ Từ khung bi rời:", 60, DTEAL)
        text(d, (W / 2, 1500), "n = 77 → t ≈ 0,321 s", 60, DTEAL)

# ---------------- canh 6: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    lane(d, 40, FA, (t * 0.12) % TFALL, None, False)
    card(d, (550, 215, 1040, 1290), fill=WHITE, outline=NAVY, w=6)
    text(d, (795, 320), "Chưa nói được", 58, NAVY)
    text(d, (795, 520), "Mới quay ở", 58, INK); text(d, (795, 610), "s = 0,500 m.", 58, C_S)
    text(d, (795, 820), "Độ cao khác:", 58, INK); text(d, (795, 910), "cùng g?", 62, DTEAL, alpha=appear(t, 1.6, 0.4))

# ---------------- canh 7: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    badge(d, 235, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 345), "s = 0,700 m · g ≈ 9,8 m/s²", 58, INK, alpha=k)
    text(d, (W / 2, 435), "quay 240 khung/s.", 58, C_F, alpha=k)
    text(d, (W / 2, 535), "Khung bi rời → khung chạm mốc:", 56, INK, alpha=k)
    text(d, (W / 2, 630), "bao nhiêu khung?", 62, ORANGE, alpha=k)
    hi = int(t * 2.5) % 6
    for i in range(6):
        x = 135 + i * 140
        card(d, (x, 760, x + 120, 990), fill=A(FILM, k), r=10)
        d.rectangle([x + 12, 774, x + 108, 976], fill=A((235, 238, 244), k))
        ball(d, x + 60, 800 + 150 * (i / 5) ** 2, a=k, r=16)
        if i == hi: d.rounded_rectangle([x - 4, 756, x + 124, 994], radius=12, outline=A(ORANGE, k), width=5)
    text(d, (W / 2, 1090), "n = ? khung", 62, NAVY, alpha=k)
    seg_bar(d, 1290, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    cs += [(do["t0"] + RUN0 + k / FB * SLOW, "tap") for k in range(1, N30) if k % 3 == 0]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-do-g-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Thực hành đo gia tốc rơi tự do · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đếm khung hình", draw=s_hook, tail=0.3, caps=[
   ("Quay chậm, đếm khung hình.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cùng lần thả, hai cách quay.", 3.4),
   ("Mỗi khung: một ảnh của bi.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Ít khung hơn tám lần.", 3.2),
   ("t bằng số khung chia khung/s.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Lệch một khung là bao lâu?", 3.4),
   ("Quay thưa, sai số lớn.", 3.6)]),
 dict(key="bay", title="Bẫy: đếm từ lúc bi nằm yên", draw=s_bay, tail=0.3, caps=[
   ("Đếm từ lúc bi nằm yên?", 3.4),
   ("Đếm từ khung bi rời.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Mới quay ở một độ cao.", 3.5)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Thử tính, rồi chọn đáp án.", 6.0)]),
])
