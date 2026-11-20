# Clip: tn-l10-luc-ma-sat-02 - Ma sat truot khong doi theo dien tich, toc do; ma sat lan rat nho (lo 7, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-luc-ma-sat-02.json: hop 0,40 kg ; so_lieu_mau: nam cham 1,2 N ;
#   dung dung 1,2 N ; nam nhanh hon 1,2 N ; lan tren but chi 0,08 N (luc ke chi doc "duoi 0,1 N") (_kiem_so()).
# Hinh chinh KHAC masat1 (do thi F theo t, dinh 0,7 -> 0,6 N): bon lan keo DEU noi tiep (nam / dung dung / nhanh hon / lan)
#   + COT SO SANH bon so chi. Moi lan keo da o trang thai deu tu dau (kim dung yen) -> khong ve doan ma sat nghi.
# Du doan (K10: chi cau hoi + hinh, khung ben canh co lua chon): ke hop len hai but chi cho lan, so voi khi keo truot
#   luc ke chi the nao?  A. Nhu khi truot ; B. Lon hon ; C. Khoang mot nua ; D. Nho hon rat nhieu (DUNG).
# KHONG tra loi san Cau 1 trong bai (dung dung, dien tich con 1/3 -> ma sat?): clip chi hien so do cua chinh hop nay
#   (giong hop thi nghiem), khong co the/phu de phat bieu quy tac chung ve dien tich, khong noi "1/3".
#   Khong hien mu (cau Doc so lieu sau hop 01 hoi mu).
# Bay = hien_tuong_hay_sai[1] "keo nhanh thi ma sat truot lon hon" -> cham 1,2 N ; nhanh hon 1,2 N (khong dung bay dien tich
#   cua masat1/Cau 1). Chua noi duoc: mat ban uot / danh sap (bai: ma sat phu thuoc tinh trang hai mat).
# Cau chot (ghi trong ghi_chu kho): them 0,10 kg gia trong (tong 0,50 kg), keo truot deu -> F = mu.m.g
#   = 0,30.0,50.9,8 = 1,47 ~ 1,5 N (mu tu 1,2/3,92 = 0,31 cung ra 1,5). KHONG hoi mu tu (0,40 kg; 1,2 N): trung hang 2
#   bang TN 01 ma hop "Doc so lieu" bat HS tinh ; tranh 0,60 / 0,80 kg (co trong bang TN 01 / trung y chot masat1).
#   So 0,50 kg / 1,5 N chua tung hien tren man.
# Tu kiem: python clips/masat2.py --kiem-dong-bo
import math
from engine import *

M_HOP = 0.40
CASES = [("nằm", 1.2, "flat", 20), ("dựng đứng", 1.2, "tall", 20), ("nhanh hơn", 1.2, "flat", 60), ("lăn", 0.08, "roll", 20)]
FMAX = 5.0
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def rd(f): return "dưới 0,1 N" if f < 0.1 else vn(f) + " N"
def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-luc-ma-sat-02.json")))
    assert [h[1] for h in k["so_lieu_mau"]["hang"]] == [c[1] for c in CASES]
    assert k["tham_so"][0]["gia_tri"] == M_HOP
_kiem_so()

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); BOX = (214, 170, 110); BOX_D = (150, 104, 56)
SKIN = (240, 196, 160); SKIN_D = (190, 140, 105); DGREEN = (21, 110, 55); DRED = (185, 28, 28)
PENCIL = (250, 204, 21); PENCIL_D = (161, 98, 7); NOTE = (60, 64, 84)

# ---------------- dan thi nghiem (nhin ngang, keo sang PHAI) ----------------
SURF = 660
XR0 = 290                                   # mep phai hop luc bat dau moi lan keo
ROPE, BODY = 30, 340
DIMS = {"flat": (230, 90), "tall": (90, 210), "roll": (230, 90)}
PR = 15                                     # ban kinh but chi

def rig(d, xr, kind, f_read, alpha=1.0, vlab=None, state=None, roll_dx=0.0):
    c = lambda col: A(col, alpha)
    d.rectangle([40, SURF, 1040, SURF + 40], fill=c(WOOD)); d.line([(40, SURF), (1040, SURF)], fill=c(WOOD_D), width=4)
    bw, bh = DIMS[kind]; lift = 2 * PR if kind == "roll" else 0
    xl = xr - bw; yb = SURF - lift
    if kind == "roll":                       # hai but chi lan: tam chay bang nua toc do hop
        for px in (xl + 45, xr - 45):
            cx = px - roll_dx / 2; cy = SURF - PR
            d.ellipse([cx - PR, cy - PR, cx + PR, cy + PR], fill=c(PENCIL), outline=c(PENCIL_D), width=3)
            ang = -roll_dx / 2 / PR
            d.line([(cx, cy), (cx + PR * math.sin(ang), cy - PR * math.cos(ang))], fill=c(PENCIL_D), width=3)
    d.rounded_rectangle([xl, yb - bh, xr, yb], radius=10, fill=c(BOX), outline=c(BOX_D), width=4)
    hy = yb - 45
    Q = lambda s, h=0.0: (xr + s, hy + h)
    d.line([Q(0), Q(ROPE - 13)], fill=c(NAVY), width=5)
    se = luc_ke(d, Q, ROPE, ROPE + 20, ROPE + 20 + BODY, FMAX, f_read, nho=0.1, so=(0, 1, 2, 3, 4, 5), hw=44, ben=-1,
                co=40, alpha=alpha)
    d.line([Q(se - 16), Q(se + 12)], fill=c(NAVY), width=8)
    hx, hy2 = Q(se + 40); d.ellipse([hx - 28, hy2 - 28, hx + 28, hy2 + 28], fill=c(SKIN), outline=c(SKIN_D), width=3)
    if vlab:                                  # mui ten van toc tren hop
        s, L = vlab; y = yb - bh - 40; x0 = xl + 10
        arrow(d, (x0, y), (x0 + L, y), c(PURPLE), w=6, head=18)
        text(d, (x0, y - 44), s, 40, PURPLE, anchor="lm", alpha=alpha)
    if state:
        text(d, (1010, 310), state, 40, DGREEN, anchor="rm", alpha=alpha)
    return hx + 28

# ---------------- cot so sanh ----------------
CX = [170, 400, 640, 890]; BASE = 1420; SP = 300            # px / N
def chart(d, hs, hl=(), alpha=1.0, top=880):
    """hs[i] in 0..1: muc moc cot i."""
    card(d, (40, top, 1040, 1560), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    d.line([(90, BASE), (1010, BASE)], fill=A(NAVY, alpha), width=4)
    for i, (lab, f, kind, v) in enumerate(CASES):
        g = hs[i]; h = f * SP * g; cx = CX[i]
        col = ORANGE if i < 3 else TEAL
        if i in hl:
            hw = max(90, tw(d, rd(f), F(40)) / 2 + 22)
            d.rounded_rectangle([cx - hw, BASE - f * SP - 88, cx + hw, BASE + 8], radius=18, outline=A(DRED, alpha), width=5)
        if h > 2: d.rectangle([cx - 60, BASE - h, cx + 60, BASE], fill=A(col, alpha))
        if g > 0.97: text(d, (cx, BASE - h - 44), rd(f), 40, col, alpha=alpha)
        text(d, (cx, BASE + 50), lab, 40, INK, alpha=alpha)

def readout(d, s, y=830, alpha=1.0):
    card(d, (W / 2 - 190, y - 42, W / 2 + 190, y + 42), fill=A((254, 242, 242), alpha), r=24)
    text(d, (W / 2, y), s, 50, RED, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    rig(d, XR0, "roll", None)
    text(d, (XR0 - 115, SURF - 2 * PR - 45), "0,40 kg", 40, WHITE)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Kê hộp lên bút chì cho lăn.", "So với khi trượt,", "lực kế chỉ thế nào?")):
        text(d, (W / 2, y0 + 190 + j * 82), s, 50, INK, alpha=a)
    text(d, (W / 2, y0 + 515), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 585, 940, y0 + 599], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 585, 140 + 800 * (1 - p), y0 + 599], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (4 lan keo deu) ----------------
FADE, T_READ, T_BAR, BAR_D = 0.3, 0.6, 1.4, 0.5
def do_state(t, M):
    """-> (k, mep phai hop, so kim, alpha dan, o so chi, muc cot[4])."""
    k = max(0, sum(1 for m in M if t >= m) - 1); tk = t - M[k]
    lab, f, kind, v = CASES[k]
    xr = XR0 + v * max(0.0, tk)
    al = appear(tk, 0.0, FADE) if k > 0 else 1.0
    read = rd(f) if tk >= T_READ else "…"
    hs = []
    for i in range(4):
        if i < k: hs.append(1.0)
        elif i == k: hs.append(ease((tk - T_BAR) / BAR_D))
        else: hs.append(0.0)
    return k, xr, f, al, read, hs

def s_do(img, d, t, sc):
    M = sc["M"]; k, xr, f, al, read, hs = do_state(t, M)
    card(d, (40, 260, 1040, 880 - 20), fill=WHITE, outline=LIGHT, w=3)
    lab, _, kind, v = CASES[k]
    vl = ("nhanh hơn", 170) if v > 30 else ("chậm", 60)
    rig(d, xr, kind, f, alpha=al, vlab=vl, state="lăn đều" if kind == "roll" else "trượt đều",
        roll_dx=xr - XR0)
    readout(d, read, y=800, alpha=al)
    chart(d, hs, top=880)

def _kiem_dong_bo():
    """Moi 0,05 s: kim = so cua lan dang keo ; o so chi (khi hien) = kim ; cot chi moc sau khi o so da hien ; cot cac lan
    truoc day du ; tay khong ra ngoai khung ; toc do hop dung voi lan keo."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; M = sc["M"]; t = 0.0; bad = []
    while t < sc["T"]:
        k, xr, f, al, read, hs = do_state(t, M); tk = t - M[k]
        if f != CASES[k][1]: bad.append((round(t, 2), "kim"))
        if read != "…" and read != rd(f): bad.append((round(t, 2), "o so != kim"))
        if hs[k] > 0 and read == "…": bad.append((round(t, 2), "cot truoc so"))
        if any(h > 0 for h in hs[k + 1:]) or any(h < 1 for h in hs[:k]): bad.append((round(t, 2), "cot sai lan"))
        if xr + ROPE + 20 + BODY + 30 + 40 + 28 > 1036: bad.append((round(t, 2), "tay ra ngoai", round(xr)))
        if tk > 0 and abs((xr - XR0) / tk - CASES[k][3]) > 1e-6: bad.append((round(t, 2), "toc do"))
        if k < 3 and M[k + 1] - M[k] < T_BAR + BAR_D + 0.3: bad.append((k, "lan qua ngan"))
        t += 0.05
    if T_BAR + BAR_D + 0.3 > sc["T"] - M[3]: bad.append("cot lan chua moc xong")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN · Nhỏ hơn rất nhiều", 320, ka)
    kh = appear(t, 0.5, 0.4)
    chart(d, [1, 1, 1, 1], hl=(3,) if kh > 0.5 else (), top=880)
    kr = appear(t, M[1] - 0.1, 0.45)
    if kr > 0:
        y0 = 420 + (1 - kr) * 20
        card(d, (40, y0, 1040, y0 + 320), fill=A((255, 247, 237), kr), outline=A(ORANGE, kr), w=5)
        pw = tw(d, "RÚT RA", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(ORANGE, kr), r=32)
        text(d, (W / 2, y0 + 58), "RÚT RA", 40, WHITE, alpha=kr)
        text(d, (W / 2, y0 + 170), "Ba lần trượt: cùng 1,2 N", 48, (154, 52, 18), alpha=kr)
        text(d, (W / 2, y0 + 250), "Lăn: dưới 0,1 N", 48, TEAL, alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    ke = appear(t, 2.8, 0.4)
    chart(d, [1, 1, 1, 1], hl=(0, 2) if ke > 0.5 and k3 < 0.5 else (), top=880)
    y = 270
    if a1 > 0:
        card(d, (40, y, 1040, y + 380), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 60), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 2.4) / 0.4)
        for j, q in enumerate(("“Kéo nhanh thì", "ma sát trượt lớn hơn”")):
            f = F(48); lw = tw(d, q, f); yy = y + 180 + j * 76
            text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)],
                       fill=A(DRED, 0.85 * a1), width=6)
        if ks > 0: text(d, (W / 2 + tw(d, "ma sát trượt lớn hơn”", F(48)) / 2 + 40, y + 256), "✗", 48, DRED, alpha=a1 * ks)
    if k3 > 0:
        card(d, (40, y, 1040, y + 340), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 230), "Mặt bàn ướt, đánh sáp thì sao?", 46, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: them 0,10 kg (tong 0,50 kg) -> F ? (~1,5 N) ; goi y tre 3 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 400), "Lăn nhẹ hơn trượt rất nhiều", 52, GREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 674), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 642), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Thêm 0,10 kg gia trọng (tổng 0,50 kg),", "kéo trượt đều.", "Lực kế chỉ khoảng bao nhiêu?")):
        text(d, (W / 2, 790 + j * 80), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1100, 970, 1360), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1160), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1270), "Cùng mặt bàn, cùng hộp", 48, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + m, "tap") for m in do["M"]]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 2.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-luc-ma-sat-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực ma sát · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Trượt hay lăn?", draw=s_hook, tail=0.3, caps=[
   ("Kéo hộp gỗ bằng lực kế.", 3.4),
   ("Nghĩ trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Hộp nằm, kéo trượt đều.", 3.0),
   ("Dựng đứng hộp, kéo như cũ.", 3.0),
   ("Kéo trượt đều nhanh hơn.", 3.0),
   ("Kê lên hai bút chì, kéo đều.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("So bốn cột số chỉ.", 3.0),
   ("Lăn: lực kế gần như không nhích.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 4.2),
   ("Câu còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
