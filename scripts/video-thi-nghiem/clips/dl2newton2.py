# Clip: tn-l10-dl2-newton-02 - Gia toc cua xe theo khoi luong, luc keo khong doi (lo 7, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dl2-newton-02.json:
#   tham_so F = 0,40 N, gia trong 0,25 kg x 4 ; so_lieu_mau (m kg, a m/s2, m.a N): 0,50 0,80 0,40 ; 0,75 0,53 0,40 ;
#   1,00 0,40 0,40 ; 1,50 0,27 0,41 (_kiem_so()). Khong hien t (kho khong co cot t): xe chay voi thoi gian
#   t = can(2s/a), s = 0,50 m (bo thi nghiem 01) chi de ve -> xe nang chay cham hon that; so tren man chi la a.
# Bo cuc KHAC dl2newton1 (do thi a-F la hinh chinh): o day hinh chinh la BANG m | a (| m.a) + gia trong chat len xe,
#   canh ket qua la do thi a theo m (duong cong), khong phai duong thang.
# Du doan (K10: chi cau hoi + hinh, khung ben canh co lua chon): giu F = 0,40 N, m 0,50 -> 1,50 kg, do thi a theo m?
#   A. Duong thang di xuong ; B. Duong cong di xuong, thoai dan (DUNG) ; C. Duong nam ngang ; D. Duong thang di len.
# Cau 2 trong bai (m gap 3 -> a?): bang Ket qua van co du 4 hang (ca 0,50 va 1,50 kg, giong hop thi nghiem trong bai
#   da liet ke du 4 so) - khong bo diem du lieu ; clip chi khong TU NOI phep so 0,50/1,50 (khong phu de, khong mui ten
#   noi hai hang), bay dung cap 0,50 / 1,00 kg, khong dung bay "m gap 3 thi a giam 9 lan".
#   Mo bai (40 kg / 80 kg) da duoc muc II tra loi.
# Bay = hien_tuong_hay_sai[0] "Cung luc thi moi vat co cung gia toc" -> 0,50 kg: 0,80 ; 1,00 kg: 0,40 m/s2.
# Cau chot (ghi trong ghi_chu kho): F van 0,40 N, xe rong 0,50 kg, muon a = 0,32 m/s2 -> m = 1,25 kg (tham_so 0,5-1,5),
#   them 0,75 kg = 3 gia trong. So 0,32 / 1,25 / 0,75 chua tung hien tren man.
from engine import *

ROWS = [(0.50, 0.80, 0.40), (0.75, 0.53, 0.40), (1.00, 0.40, 0.40), (1.50, 0.27, 0.41)]   # so_lieu_mau
F_N, S_M, M0, GT = 0.40, 0.50, 0.50, 0.25
NB = [0, 1, 2, 4]                                  # so gia trong tren xe
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
def _kiem_so():
    bad = [r for r in ROWS if abs(round(F_N / r[0], 2) - r[1]) > 1e-9 or abs(round(r[0] * r[1] + 1e-9, 2) - r[2]) > 1e-9]
    bad += [n for n, r in zip(NB, ROWS) if abs(M0 + n * GT - r[0]) > 1e-9]
    return bad
assert not _kiem_so()
TRUN = [math.sqrt(2 * S_M / a) for _, a, _ in ROWS]   # chi de ve chuyen dong (khong hien so)

DRED = (185, 28, 28); NOTE = (60, 64, 84); TRACK = (176, 184, 200); TRACK_D = (110, 118, 140)
SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100); BLOCK = (120, 92, 60); BLOCK_D = (84, 62, 38)
CART = (13, 148, 136); CART_D = (8, 90, 84)

TY = 400; PPM = 720; X0 = 300                     # mep truoc xe khi tha ; di 0,50 m = 360 px
PUX, PUY, PUR = 960, TY + 6, 26; MY0 = 420
CW, CH = 240, 56

def track(d):
    d.rectangle([40, TY, 930, TY + 30], fill=TRACK); d.line([(40, TY), (930, TY)], fill=TRACK_D, width=4)
    d.rectangle([60, TY + 30, 84, 560], fill=TRACK_D); d.rectangle([880, TY + 30, 904, 560], fill=TRACK_D)
    d.line([(40, 560), (1040, 560)], fill=INK, width=4)
    d.line([(930, TY + 15), (PUX, PUY)], fill=TRACK_D, width=8)
    d.ellipse([PUX - PUR, PUY - PUR, PUX + PUR, PUY + PUR], fill=WHITE, outline=NAVY, width=5); dot(d, PUX, PUY, 6, NAVY)
    for x in (X0, X0 + S_M * PPM):                  # hai cong quang (khong nhan, nhu thi nghiem truoc)
        d.rectangle([x - 7, TY - 120, x + 7, TY], fill=A(PURPLE, 0.55))

def shelf(d):
    pass   # gia trong cho nam tren san, duoi mang (khong ve ke: tranh cat day keo)

def block(d, cx, y, alpha=1.0):
    d.rectangle([cx - 52, y - 34, cx + 52, y], fill=A(BLOCK, alpha), outline=A(BLOCK_D, alpha), width=3)

def cart(d, xf, nb, drop=None):
    """Mep truoc xe xf, nb gia trong da nam tren xe ; drop = (j, k 0..1): gia trong thu j dang roi xuong."""
    x0 = xf - CW; cx = xf - CW / 2
    d.rounded_rectangle([x0, TY - CH, xf, TY], radius=10, fill=CART, outline=CART_D, width=4)
    d.rectangle([xf - 4, TY - 46, xf + 26, TY - 16], fill=ORANGE, outline=NAVY, width=3)       # cam bien luc
    yb = TY - CH
    slot = lambda j: (cx + (-55 if j % 2 == 0 else 55), yb - (j // 2) * 36)   # 2 cot, vi tri co dinh
    for j in range(nb): block(d, *slot(j))
    if drop:
        j, k = drop; tx, ty = slot(j)
        block(d, tx, lerp(ty - 110, ty, ease(k)), alpha=clamp(k * 3))
    hx, hy = xf + 26, TY - 31
    d.line([(hx, hy), (PUX, PUY - PUR)], fill=NAVY, width=3)
    my = MY0 + (xf - X0)
    d.line([(PUX + PUR, PUY), (PUX + PUR, my)], fill=NAVY, width=3)
    d.rectangle([PUX + PUR - 24, my, PUX + PUR + 24, my + 50], fill=BODY, outline=NAVY, width=3)

def readout(d, x0, x1, label, reading, flash=0.0, y=640):
    card(d, (x0, y, x1, y + 130), fill=BODY, r=20)
    card(d, (x0 + 16, y + 14, x1 - 16, y + 78), fill=mix(SCREEN, (255, 237, 160), flash), r=10)
    text(d, ((x0 + x1) / 2, y + 46), reading, 44, SCR_INK)
    text(d, ((x0 + x1) / 2, y + 104), label, 40, WHITE)

def readouts(d, a_s, flash=0.0):
    readout(d, 40, 420, "lực kéo F (giữ)", "0,40 N")
    readout(d, 440, 840, "gia tốc a", a_s, flash)

def table(d, n, y=850, ma=0.0, hi=-1, alpha=1.0):
    h = 190 + 4 * 84 + 20
    card(d, (40, y, 1040, y + h), fill=A(WHITE, alpha), outline=A(NAVY, alpha), w=4)
    xs = (230, 540, 850)
    text(d, (xs[0], y + 60), "m (kg)", 44, INK, alpha=alpha)
    text(d, (xs[1], y + 60), "a (m/s²)", 44, INK, alpha=alpha)
    text(d, (xs[2], y + 60), "m·a (N)", 44, GREEN, alpha=alpha * ma)
    text(d, (W / 2, y + 128), "gia trọng 0,25 kg / khối", 40, NOTE, alpha=alpha)
    d.line([(70, y + 166), (1010, y + 166)], fill=A(LIGHT, alpha), width=4)
    for i in range(n):
        yy = y + 220 + i * 84
        if i == hi: card(d, (70, yy - 38, 1010, yy + 38), fill=A((255, 237, 213), alpha), r=18)
        text(d, (xs[0], yy), vn(ROWS[i][0]), 46, INK, alpha=alpha)
        text(d, (xs[1], yy), vn(ROWS[i][1]), 46, BLUE, alpha=alpha)
        text(d, (xs[2], yy), vn(ROWS[i][2]), 46, GREEN, alpha=alpha * ma)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    track(d); cart(d, X0, 0); readouts(d, "?")
    shelf(d)
    for j in range(4): block(d, 160 + (j % 2) * 110, 560 - (j // 2) * 36)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 860 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 660), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Giữ lực kéo 0,40 N.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "Xe nặng dần: 0,50 → 1,50 kg.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 355), "Vẽ a theo m,", 52, INK, alpha=a)
    text(d, (W / 2, y0 + 425), "đồ thị có dạng nào?", 52, INK, alpha=a)
    text(d, (W / 2, y0 + 530), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 600, 940, y0 + 614], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 600, 140 + 800 * (1 - p), y0 + 614], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (chat gia trong, 4 lan) ----------------
DROP, GAP, BACK = 0.5, 0.45, 0.4
def run_starts():
    ts = [0.6]
    for k in range(3): ts.append(ts[-1] + TRUN[k] + GAP + BACK + DROP + 0.1)
    return ts
RS = run_starts()

def do_state(t):
    """-> (k lan, mep truoc xe, so gia trong tren xe, gia trong dang roi (j, tien do) | None, so hang da do)."""
    k = max(0, sum(1 for r in RS if t >= r) - 1)
    if t < RS[0]: return 0, X0, 0, None, 0
    tau = t - RS[k]; tk = TRUN[k]
    if tau < tk: return k, X0 + S_M * PPM * (tau / tk) ** 2, NB[k], None, k
    if k == 3 or tau < tk + GAP: return k, X0 + S_M * PPM, NB[k], None, k + 1
    x = (tau - tk - GAP)
    if x < BACK: return k, lerp(X0 + S_M * PPM, X0, ease(x / BACK)), NB[k], None, k + 1
    x -= BACK; nadd = NB[k + 1] - NB[k]; kk = clamp(x / DROP)       # gia trong roi xuong (1 hoac 2 khoi)
    j = NB[k] + min(nadd - 1, int(kk * nadd)); kj = kk * nadd - (j - NB[k])
    return k, X0, j, (j, clamp(kj)), k + 1

def s_do(img, d, t, sc):
    k, xf, nb, drop, n = do_state(t)
    track(d); cart(d, xf, nb, drop)
    done = n > k
    flash = 1 - clamp((t - RS[k] - TRUN[k]) / 0.6) if done else 0
    readouts(d, vn(ROWS[k][1]) + " m/s²" if done else "—", flash)
    table(d, n, hi=k if done else -1)
    left = 4 - (nb + (1 if drop else 0))                              # gia trong con cho tren ban
    shelf(d)
    for j in range(left): block(d, 160 + (j % 2) * 110, 560 - (j // 2) * 36)

def _kiem_dong_bo():
    """Moi 0,05 s: so gia trong tren xe khi chay = NB[k] ; hang + so a hien CUNG luc xe toi cong 2."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        k, xf, nb, drop, n = do_state(t)
        tau = t - RS[k]
        if t >= RS[0] and tau < TRUN[k] and (nb != NB[k] or n != k or drop): bad.append(("chay", round(t, 2)))
        if t >= RS[0] and tau >= TRUN[k] and n != k + 1: bad.append(("hang", round(t, 2)))
        if abs(M0 + nb * GT - ROWS[k][0]) > 1e-9 and tau < TRUN[k] + GAP: bad.append(("m", round(t, 2)))
        t += 0.05
    if RS[-1] + TRUN[-1] + 0.8 > sc["T"]: bad.append("lan cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an (do thi a theo m) + Rut ra (cot m.a) ----------------
GX0, GX1, GY0, GY1 = 210, 950, 1530, 1150      # m 0-1,6 kg ; a 0-1,0
def gx(m): return GX0 + m / 1.6 * (GX1 - GX0)
def gy(a): return GY0 - a / 1.0 * (GY0 - GY1)

def axes(d, y_top=1040):
    card(d, (40, y_top, 1040, 1600), fill=WHITE, outline=LIGHT, w=3)
    for a in (0.2, 0.4, 0.6, 0.8, 1.0):
        d.line([(GX0, gy(a)), (GX1, gy(a))], fill=LIGHT, width=3)
    for a in (0.4, 0.8):
        text(d, (GX0 - 18, gy(a)), vn(a, 1), 40, NOTE, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 36), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 36, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 22, GY1 - 50), "a (m/s²)", 40, INK, anchor="lm")
    text(d, (1020, GY0 - 44), "m (kg)", 40, INK, anchor="rm")
    text(d, (GX0 - 18, GY0 + 6), "0", 40, NOTE, anchor="rm")
    for m in (0.5, 1.0, 1.5):
        d.line([(gx(m), GY0), (gx(m), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(m), GY0 + 40), vn(m, 1), 40, NOTE)

def curve(d, k):
    if k <= 0: return
    m1 = lerp(0.5, 1.5, k); pts_ = [(gx(m), gy(F_N / m)) for m in np.linspace(0.5, m1, 40)]
    d.line(pts_, fill=A(GREEN, 0.85), width=6, joint="curve")

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.4)
    lab = "ĐÁP ÁN · Đường cong đi xuống, thoải dần"
    pw = tw(d, lab, F(40)) + 52
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 336), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 303), lab, 40, WHITE, alpha=ka)
    kma = appear(t, M[1] + 0.1, 0.5)
    table(d, 4, y=380, ma=kma)
    axes(d); curve(d, appear(t, M[0] + 0.3, 1.0))
    for m, a, _ in ROWS: dot(d, gx(m), gy(a), 15, BLUE, outline=WHITE)
    kr = appear(t, M[1] + 0.9, 0.45)
    if kr > 0:
        card(d, (60, 940, 1020, 1020), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=24, w=4)
        text(d, (W / 2, 980), "RÚT RA: a tỉ lệ nghịch với m", 46, (21, 110, 55), alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    track(d); cart(d, X0, 2)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3); y = 700
    if a1 > 0:
        card(d, (40, y, 1040, y + 620), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 2.4) / 0.4)
        for j, q in enumerate(("“Cùng lực kéo thì xe nào", "cũng cùng gia tốc”")):
            yy = y + 175 + j * 66; lw = tw(d, q, F(48))
            text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        if ks > 0: text(d, (990, y + 175), "✗", 52, DRED, alpha=a1 * ks)
        ke = a1 * appear(t, 2.8, 0.4)
        text(d, (W / 2, y + 360), "Cùng 0,40 N:", 46, INK, alpha=ke)
        text(d, (W / 2, y + 440), "0,50 kg → a = 0,80 m/s²", 46, BLUE, alpha=ke)
        text(d, (W / 2, y + 520), "1,00 kg → a = 0,40 m/s²", 46, BLUE, alpha=ke)
    if k3 > 0:
        card(d, (40, y, 1040, y + 460), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 230), "Máng có ma sát:", 46, INK, alpha=kk)
        text(d, (W / 2, y + 320), "m·a còn bằng lực kéo không?", 46, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong chua quy tac giai) -> THU NGHI: a = 0,32 m/s2 -> them may gia trong ; goi y (du kien) tre 3 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 400), "Giữ lực: xe càng nặng, a càng nhỏ", 48, GREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 674), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 642), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Lực kéo vẫn 0,40 N.", "Thêm bao nhiêu gia trọng", "để a = 0,32 m/s²?")):
        text(d, (W / 2, 790 + j * 80), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1100, 970, 1360), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1160), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1270), "Xe rỗng 0,50 kg; khối 0,25 kg", 46, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + r, "tap") for r in RS]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-dl2-newton-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Định luật 2 Newton · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Chất thêm gia trọng lên xe", draw=s_hook, tail=0.3, caps=[
   ("Cảm biến giữ lực kéo không đổi.", 3.4),
   ("Nghĩ trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=1.2, caps=[
   ("Lần đầu: xe rỗng.", 2.6),
   ("Mỗi lần chất thêm gia trọng.", 7.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Bốn điểm nằm trên một đường cong.", 3.4),
   ("Nhân m với a ở từng hàng.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 4.2),
   ("Câu còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
