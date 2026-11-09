# Clip: tn-l11-tatdan-02 - Cung mot con lac, tha trong khong khi, nuoc, dau nhot (9/11/2026, chang B L11 Dao dong)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-tatdan-02.json:
#   tham_so: A0 = 5,0 cm ; T = 1,0 s ; t doc dinh = 2,0 s ; beta (khong khi 0,4 ; nuoc 1,15 ; dau 2,8 /s).
#   mo_hinh: x = A0 e^(-beta t) cos(2 pi t / T), bao A(t) = A0 e^(-beta t) (net dut o canh Dap an).
#   so_lieu_mau (lam tron 0,1 cm): sau 2 s con 2,2 ; 0,5 ; 0,0 cm. "Khong phai so do that" -> ghi "so minh hoa".
#   gia_thiet: bo qua viec nuoc/dau lam chu ki doi -> o "Chua noi duoc".
#   hien_tuong_hay_sai[0]: "tat dan van la dieu hoa" -> canh Bay.
# Doan ngay sau hop trong bai: cau tu kiem "Dau dac hon ... ve can bang roi dung" -> clip KHONG noi "nhot hon nua thi
#   dung han" (rut_ra[1] cua kho), khong dung hien_tuong_hay_sai[1] (dau dac van qua lai mai) lam bay.
# Cau chot: chat long nhot hon nuoc, kem dau -> sau 2 s dinh con trong khoang nao? (giua 0,0 va 0,5 cm; chi dung
#   khoang giua hai so da hien, khong noi suy so moi).
from engine import *

A0, PER, TREAD = 5.0, 1.0, 2.0
MED = [("Không khí", 0.4, "2,2", BLUE), ("Nước", 1.15, "0,5", TEAL), ("Dầu nhớt", 2.8, "0,0", ORANGE)]
def xt(beta, t): return A0 * math.exp(-beta * t) * math.cos(2 * math.pi * t / PER)

# ---------------- ba con lac + coc ----------------
CXS = (200, 540, 880)
PY, LP, PXP = 350, 320, 14           # tru treo, day 320 px ~ 25 cm (kho) -> 1 cm ~ 13-14 px
OIL = (217, 160, 40)
def pend(d, cx, xcm, cup=None, a=1.0):
    c = lambda col: A(col, a)
    dx = xcm * PXP; bx, by = cx + dx, PY + math.sqrt(LP * LP - dx * dx)
    if cup:
        d.rectangle([cx - 130, 600, cx + 130, 750], fill=A(cup, 0.30 * a))
    d.line([(cx, PY), (bx, by)], fill=c(NAVY), width=4)
    dot(d, bx, by, 26, c(PURPLE), outline=c(WHITE))
    if cup:
        d.line([(cx - 130, 590), (cx - 130, 752), (cx + 130, 752), (cx + 130, 590)], fill=c(NAVY), width=4)
    d.line([(cx, by + 40), (cx, by + 56)], fill=c(GRAY), width=3)          # vach can bang duoi coc
def rig(d, xs, a=1.0):
    d.rectangle([60, PY - 18, 1020, PY], fill=A((190, 195, 210), a), outline=A(NAVY, a), width=3)
    for (lab, beta, _, col), cx, x in zip(MED, CXS, xs):
        pend(d, cx, x, None if lab == "Không khí" else ((120, 190, 240) if lab == "Nước" else OIL), a)
        text(d, (cx, 800), lab, 42, col, alpha=a)

# ---------------- ba dai x - t (truc co dinh suot clip) ----------------
SX0, SX1 = 300, 1000                  # t = 0 -> 2 s
SYS = (1000, 1230, 1460)              # tam moi dai (x = 0)
PXS = 16                              # 1 cm = 16 px tren dai
def sx(t): return SX0 + t / 2.0 * (SX1 - SX0)
def strips(d, a=1.0, labels=True):
    for (lab, beta, _, col), y in zip(MED, SYS):
        d.line([(SX0, y), (SX1 + 10, y)], fill=A(GRAY, a), width=3)
        d.line([(SX0, y - 5 * PXS - 6), (SX0, y + 5 * PXS + 6)], fill=A(NAVY, a), width=3)
        for v in (-5, 5):
            d.line([(SX0 - 10, y - v * PXS), (SX0, y - v * PXS)], fill=A(NAVY, a), width=3)
        if labels: text(d, (50, y), lab, 40, col, anchor="lm", alpha=a)
    yb = SYS[-1] + 5 * PXS + 40
    for tt in (0, 1, 2):
        d.line([(sx(tt), SYS[-1] + 5 * PXS + 6), (sx(tt), SYS[-1] + 5 * PXS + 16)], fill=A(NAVY, a), width=3)
        text(d, (sx(tt), yb + 6), str(tt) + (" s" if tt == 2 else ""), 40, INK, alpha=a)
    text(d, (SX0 - 22, SYS[0] - 5 * PXS), "5", 36, MUTED, anchor="rm", alpha=a)
    text(d, (SX0 - 22, SYS[0] + 5 * PXS), "−5", 36, MUTED, anchor="rm", alpha=a)

def trace(d, beta, y, tmax, col, w=5):
    n = max(2, int(tmax / 0.01) + 1)
    pts = [(sx(i * tmax / (n - 1)), y - xt(beta, i * tmax / (n - 1)) * PXS) for i in range(n)]
    d.line(pts, fill=col, width=w, joint="curve")

def env(d, beta, y, k, col):
    n = 60; pts = [(sx(2.0 * i / n), y - A0 * math.exp(-beta * 2.0 * i / n) * PXS) for i in range(int(n * k) + 1)]
    for j in range(0, len(pts) - 1, 2): d.line([pts[j], pts[j + 1]], fill=col, width=4)

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.85, cx + pw / 2, cy + size * 0.85), fill=A(bg, a), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    k = ease((t - 0.6) / 1.2)
    rig(d, [A0 * k] * 3)
    pill(d, W / 2, 290, "kéo lệch 5,0 cm rồi thả", 40, WHITE, NAVY, appear(t, 0.3, 0.4))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 40, WHITE, PURPLE, a)
    ctext(d, y0 + 180, "Chu kì gần 1 s.", 44, MUTED, maxw=920, alpha=a)
    ctext(d, y0 + 350, "Sau 2 s, đỉnh còn lại của\nba con lắc xếp thế nào?", 52, INK, maxw=930, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 530, 940, y0 + 542], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 530, 140 + 800 * (1 - p), y0 + 542], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
REL, SLOW = 1.0, 2.0                  # tha o giay 1,0 cua canh ; 1 s mo hinh = 2 s video
T_LAB = (REL + 2.0 * SLOW + 0.4, REL + 2.0 * SLOW + 0.9, REL + 2.0 * SLOW + 1.4)
def tsim(t): return clamp((t - REL) / SLOW, 0, 2.0)

def s_do(img, d, t, sc):
    ts = tsim(t)
    rig(d, [xt(b, ts) for _, b, _, _ in MED])
    pill(d, 330, 290, "t = " + f"{ts:.1f}".replace(".", ",") + " s", 44, WHITE, NAVY)
    pill(d, 790, 290, "số minh hoạ", 44, WHITE, ORANGE)
    strips(d)
    for (_, b, v, col), y, tl in zip(MED, SYS, T_LAB):
        if ts > 0: trace(d, b, y, ts, col)
        k = appear(t, tl, 0.3)
        if k > 0:
            yy = y - xt(b, 2.0) * PXS
            dot(d, sx(2.0), yy, 11, A(col, k), outline=A(WHITE, k))
            text(d, (sx(2.0) + 10, y - 5 * PXS - 22), v + " cm", 42, col, anchor="rm", alpha=k)

# ---------------- canh 3: Dap an + Rut ra + Chua noi duoc ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    pill(d, W / 2, 290, "ĐÁP ÁN · không khí > nước > dầu", 40, WHITE, NAVY, ka)
    kr = appear(t, M[0] + 0.6, 0.45)
    if kr > 0:
        card(d, (60, 370, 1020, 530), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=24, w=4)
        ctext(d, 450, "Càng nhớt, biên độ tụt càng nhanh", 48, (21, 110, 55), maxw=900, alpha=kr)
    kn = appear(t, M[1] - 0.05, 0.45)
    if kn > 0:
        card(d, (60, 570, 1020, 810), fill=A(WHITE, kn), outline=A(NAVY, kn), r=24, w=5)
        text(d, (W / 2, 620), "Chưa nói được", 46, NAVY, alpha=kn)
        for j, l in enumerate(("• Nước, dầu đổi chu kì?", "• Số minh hoạ")):
            text(d, (100, 690 + j * 70), l, 44, INK, anchor="lm", alpha=kn * appear(t, M[1] + 0.3 + 0.5 * j, 0.4))
    strips(d)
    ke = clamp((t - 0.6) / 1.6)
    for (_, b, v, col), y in zip(MED, SYS):
        trace(d, b, y, 2.0, A(col, 0.45), w=4)
        env(d, b, y, ke, col)
        dot(d, sx(2.0), y - xt(b, 2.0) * PXS, 11, col, outline=WHITE)

# ---------------- canh 4: Bay - "tat dan van la dieu hoa" ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    y0 = 300
    card(d, (40, y0, 1040, y0 + 330), fill=WHITE, outline=(185, 28, 28), w=6)
    pill(d, W / 2, y0 + 62, "BẪY", 40, WHITE, (185, 28, 28))
    q = "✗ “Tắt dần vẫn là điều hoà”"
    f = F(48); lw = tw(d, q, f); yy = y0 + 200
    text(d, (W / 2, yy), q, 48, (185, 28, 28))
    ks = clamp((t - (M[1] + 2.0)) / 0.4)
    if ks > 0:
        d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=(140, 15, 15), width=7)
    # mot dai khong khi: dieu hoa (bien do giu 5,0 cm, xam) va tat dan (xanh)
    y = 920; kb = appear(t, 0.3, 0.4)
    d.line([(SX0, y), (SX1 + 10, y)], fill=A(GRAY, kb), width=3)
    d.line([(SX0, y - 5 * PXS - 6), (SX0, y + 5 * PXS + 6)], fill=A(NAVY, kb), width=3)
    n = 200
    ghost = [(sx(2.0 * i / n), y - A0 * math.cos(2 * math.pi * 2.0 * i / n) * PXS) for i in range(n + 1)]
    for j in range(0, n, 2): d.line([ghost[j], ghost[j + 1]], fill=A(GRAY, kb), width=4)
    text(d, (50, y - 60), "điều hoà", 40, MUTED, anchor="lm", alpha=kb)
    kt = appear(t, M[1] + 2.0, 0.4)
    if kt > 0:
        trace(d, 0.4, y, 2.0, A(BLUE, kt))
        text(d, (50, y + 60), "tắt dần", 40, BLUE, anchor="lm", alpha=kt)
        text(d, (sx(0) + 10, y - 5 * PXS - 34), "5,0 cm", 40, INK, anchor="lm", alpha=kt)
        text(d, (sx(2.0) - 10, y - 5 * PXS - 34), "2,2 cm", 40, BLUE, anchor="rm", alpha=kt)
    kc = appear(t, M[1] + 2.4, 0.5)
    if kc > 0:
        card(d, (60, 1140, 1020, 1330), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=24, w=4)
        text(d, (W / 2, 1200), "✓ Biên độ giảm theo thời gian", 46, (21, 110, 55), alpha=kc)
        text(d, (W / 2, 1272), "không còn là điều hoà", 44, (21, 110, 55), alpha=kc)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 290, 1020, 510), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Lực cản càng lớn,\ndao động tắt càng nhanh", 50, GREEN, maxw=900, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 570, 1040, 1520), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 600, W / 2 + pw / 2, 664), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 632), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 860, "Chất lỏng nhớt hơn nước\nnhưng kém dầu. Đỉnh sau 2 s\nnằm trong khoảng nào?",
          48, INK, maxw=930, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
    if kh > 0:
        card(d, (110, 1220, 970, 1420), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1270), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1355), "Nhìn lại ba đỉnh lúc 2 s", 44, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]
    out += [(do["t0"] + REL, "tap"), (do["t0"] + REL + 2.0 * SLOW, "tap")]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-tatdan-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Tắt dần · cưỡng bức · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Một con lắc, ba môi trường", draw=s_hook, tail=0.6, caps=[
   ("Không khí, nước, rồi dầu nhớt.", 3.4),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Mỗi chỗ thả một lần, ghép cạnh nhau.", 5.0),
   ("Đọc đỉnh còn lại lúc 2 s.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Nối các đỉnh thành nét đứt.", 5.0),
   ("Mới thử một con lắc.", 5.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: chỉ biên độ nhỏ đi?", 3.0),
   ("Có đúng không?", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.2)]),
])
