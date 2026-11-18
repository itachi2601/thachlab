# Clip: tn-l10-newton3-01 - Hai luc ke keo nhau (lo 7, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-newton3-01.json:
#   so_lieu_mau (F_keo, F1, F2 N): 1,0 1,0 1,0 ; 2,0 2,0 2,0 ; 3,0 3,0 3,1 ; 4,0 4,1 4,0 ; 5,0 5,0 5,0.
#   dung_cu: luc ke lo xo 5 N (luc_ke engine, vach 0,2 N, nam ngang chi ghi so nguyen).
#   Clip chi dung 3 lan keo nhe/vua/manh (1,0 / 2,0 / 5,0): hang 3, 4 lech 0,1 N la cau Tu kiem tra 1 ngay sau hop
#   (chenh 0,1 N do sai so doc) -> clip KHONG hien, khong giai thich chenh lech nay.
#   mo_hinh.ghi_chu: keo giat thi kim dao dong quanh gia tri can bang -> canh bay chi ve hai kim rung cung nhau, khong ghi so.
# Du doan (K10: chi cau hoi + hinh): giu yen luc ke 1, keo luc ke 2 toi 2,0 N -> luc ke 1 chi bao nhieu? Dap an: 2,0 N.
# Bay = hien_tuong_hay_sai[0] (ben nguoi keo chi lon hon). Chua noi duoc = mo_hinh.gia_thiet (bo qua khoi luong luc ke)
#   + mo_hinh.ghi_chu (keo giat chi thay kim rung).
# Chot: luc ke 1 buoc vao tuong, keo luc ke 2 bang 3,5 N (so chua hien) -> luc ke 1 chi 3,5 N (nhieu hay gap: 7 N, 0 N).
# Tu kiem: python clips/dl3newton1.py --kiem
import math
from engine import *

ROWS = [("nhẹ", 1.0, 1.0, 1.0), ("vừa", 2.0, 2.0, 2.0), ("mạnh", 5.0, 5.0, 5.0)]   # so_lieu_mau hang 1, 2, 5
FMAX = 5.0
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

SKIN = (240, 196, 160); SKIN_D = (190, 140, 105); DGREEN = (21, 110, 55); DRED = (185, 28, 28)
WOOD = (176, 124, 74); WOOD_D = (140, 96, 54)
C1, C2 = BLUE, ORANGE                       # mau luc ke 1, luc ke 2 (va luc dat len no)
T1, T2 = (219, 234, 254), (255, 237, 213)   # nen nhat cung mau

# ---------------- dan thi nghiem: hai luc ke nam ngang moc vao nhau ----------------
XC, Y = 540, 470
ROPE, BODY = 22, 330

def one_meter(d, side, f_read, xh, body=BODY, so=(0, 1, 2, 3, 4, 5), hand=True, alpha=1.0):
    """side -1: luc ke 1 (than ben trai, moc o xh); +1: luc ke 2. Tra ve x tay."""
    Q = lambda s, h=0.0: (xh + side * s, Y + h)
    se = luc_ke(d, Q, 0, 20, 20 + body, FMAX, f_read, nho=0.2, so=so, hw=46, ben=-1, co=40, alpha=alpha)
    if not hand: return None
    d.line([Q(se - 16), Q(se + 12)], fill=NAVY, width=8)
    hx, hy = Q(se + 40); dot(d, hx, hy, 28, SKIN, outline=SKIN_D)
    return hx

def rig(d, f1, f2, lab1=None, lab2=None, top=260, hands=True):
    card(d, (40, top, 1040, top + 470), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([40, Y + 70, 1040, Y + 96], fill=WOOD); d.line([(40, Y + 70), (1040, Y + 70)], fill=WOOD_D, width=3)
    h1 = one_meter(d, -1, f1, XC - ROPE); h2 = one_meter(d, 1, f2, XC + ROPE)
    d.ellipse([XC - 34, Y - 12, XC + 34, Y + 12], outline=NAVY, width=5)          # khuyen noi hai moc
    if hands:
        text(d, (h1, Y + 140), "giữ yên", 40, INK)
        text(d, (h2, Y + 140), "kéo", 40, INK)
        arrow(d, (h2 - 40, Y + 190), (h2 + 40, Y + 190), INK, w=5, head=16)
    for x, c, s in ((XC - 210, C1, "lực kế 1"), (XC + 210, C2, "lực kế 2")):
        text(d, (x, Y + 140), s, 42, c)
    for x, c, tt, lab in ((XC - 210, C1, T1, lab1), (XC + 210, C2, T2, lab2)):
        if lab is None: continue
        card(d, (x - 120, Y + 176, x + 120, Y + 244), fill=tt, r=22)
        text(d, (x, Y + 210), lab, 46, c)

def think_bar(d, t, t1, t2, y, a):
    q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, y, 940, y + 12], radius=6, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, y, 140 + 800 * (1 - q), y + 12], radius=6, fill=A(PURPLE, a))

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    f2 = 2.0 * ease((t - 0.8) / 1.0)
    rig(d, None, f2, "? N", vn(2.0) + " N" if t > 1.9 else "…")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 790 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 250, "Lực kế 2 chỉ 2,0 N.\nLực kế 1 chỉ bao nhiêu?", 56, INK,
          maxw=900, alpha=a)
    text(d, (W / 2, y0 + 440), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    if t > M[1] + 0.6: think_bar(d, t, M[1] + 0.6, sc["T"] - THINK_END, y0 + 510, a)

# ---------------- canh 2: Tien hanh ----------------
T_S = (0.4, 2.3, 4.2)        # bat dau moi lan tang luc keo
RAMP, T_ROW = 0.9, 0.35      # kim di toi so moi trong 0,9 s; hang bang hien 0,35 s sau khi kim dung

def do_state(t):
    """-> (f hai kim, so dang doc (None khi kim dang chay), so hang da ghi). Hai kim LUON cung mot so."""
    k = sum(1 for ts in T_S if t >= ts - 1e-9) - 1
    n = sum(1 for j in range(3) if t >= T_S[j] + RAMP + T_ROW - 1e-9)
    if k < 0: return 0.0, None, n
    f0 = ROWS[k - 1][1] if k > 0 else 0.0
    q = (t - T_S[k]) / RAMP
    f = lerp(f0, ROWS[k][1], ease(q))
    return f, (ROWS[k][1] if q >= 1 else None), n

XS = (190, 520, 840)
def table(d, n, y=790, hl=None, a=1.0):
    card(d, (40, y, 1040, y + 470), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    text(d, (XS[1], y + 60), "lực kế 1 (N)", 42, C1, alpha=a)
    text(d, (XS[2], y + 60), "lực kế 2 (N)", 42, C2, alpha=a)
    d.line([(70, y + 110), (1010, y + 110)], fill=A(LIGHT, a), width=3)
    for j, (lab, fk, f1, f2) in enumerate(ROWS):
        yy = y + 180 + j * 100
        if hl == j: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=20, fill=A((237, 233, 254), a))
        text(d, (XS[0], yy), lab, 46, INK, alpha=a)
        if j < n:
            text(d, (XS[1], yy), vn(f1), 52, C1, alpha=a); text(d, (XS[2], yy), vn(f2), 52, C2, alpha=a)
        else:
            for x in XS[1:]: text(d, (x, yy), "·", 46, GRAY, alpha=a)

def s_do(img, d, t, sc):
    f, read, n = do_state(t)
    lab = vn(read) + " N" if read is not None else "…"
    rig(d, f, f, lab, lab, hands=False)
    table(d, n, hl=(n - 1 if n > 0 else None))

def _kiem_dong_bo():
    """Moi 0,05 s: hai kim cung so; o so chi chi hien khi kim dung dung so cua hang; hang j chi hien sau lan j."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        f, read, n = do_state(t)
        k = sum(1 for ts in T_S if t >= ts - 1e-9) - 1
        if read is not None and abs(f - read) > 1e-9: bad.append((round(t, 2), "so o != kim", f, read))
        if read is not None and abs(read - ROWS[k][1]) > 1e-9: bad.append((round(t, 2), "so o != hang", read))
        if n > 0 and k >= 0 and n - 1 > k: bad.append((round(t, 2), "hang som", n, k))
        if n > 0 and abs(do_state(T_S[n - 1] + RAMP + 1e-3)[0] - ROWS[n - 1][1]) > 1e-6: bad.append((round(t, 2), "kim lech hang"))
        if not (0 <= f <= FMAX): bad.append((round(t, 2), "kim ngoai thang", f))
        t += 0.05
    if T_S[-1] + RAMP + T_ROW > sc["T"] - 0.6: bad.append("hang cuoi hien qua muon")
    return bad

# ---------------- canh 3: Dap an + rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    rig(d, 2.0, 2.0, "2,0 N", "2,0 N", hands=False)
    table(d, 3, hl=1)
    ka = appear(t, 0.15, 0.4)
    card(d, (40, 1280, 1040, 1380), fill=A(WHITE, ka), r=30)
    pill(d, "ĐÁP ÁN · 2,0 N", 1330, ka)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        y0 = 1400 + (1 - k1) * 20
        card(d, (40, y0, 1040, y0 + 190), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, y0 + 62), "Lực và phản lực:", 46, DGREEN, alpha=k1)
        text(d, (W / 2, y0 + 132), "bằng nhau, cùng lúc", 46, DGREEN, alpha=k1)

# ---------------- canh 4: moi luc ke chiu luc nao (tach rieng hai luc ke) ----------------
SB = 260                     # than luc ke nho hon de tach rieng hai vat tren cung mot gia
XH1, XH2 = 380, 700          # moc luc ke 1, luc ke 2
LA = 140                     # px cho 2,0 N (hai mui ten dai bang nhau)
def s_luc(img, d, t, sc):
    global Y
    M = sc["M"]
    card(d, (40, 260, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    yy = Y + 130   # truc chung cua hai luc ke trong canh nay
    y_old = Y; Y = yy
    try:
        ka = appear(t, 0.2, 0.4)
        for xh, side, tint in ((XH1, -1, T1), (XH2, 1, T2)):
            x_end = xh + side * (20 + SB + 30)
            d.rounded_rectangle([min(xh, x_end) - 8, Y - 70, max(xh, x_end) + 8, Y + 70], radius=26, fill=A(tint, ka))
        one_meter(d, -1, 2.0, XH1, body=SB, hand=False)
        one_meter(d, 1, 2.0, XH2, body=SB, hand=False)
        text(d, (XH1 - 170, Y + 110), "lực kế 1", 42, C1); text(d, (XH2 + 170, Y + 110), "lực kế 2", 42, C2)
        k1 = appear(t, M[0] + 0.3, 0.4)
        if k1 > 0:      # luc do luc ke 2 keo, dat len luc ke 1 (tai moc 1), huong sang phai
            arrow(d, (XH1, Y), (XH1 + LA * ease(k1), Y), A(C1, k1), w=8, head=24)
            text(d, (XH1 + 10, Y - 215), "do lực kế 2 kéo", 40, C1, anchor="lm", alpha=k1)
            text(d, (XH1 + 10, Y - 165), "lên lực kế 1", 42, C1, anchor="lm", alpha=k1)
            dot(d, XH1, Y, 9, C1)
        k2 = appear(t, M[0] + 1.3, 0.4)
        if k2 > 0:      # luc do luc ke 1 keo, dat len luc ke 2 (tai moc 2), huong sang trai
            arrow(d, (XH2, Y), (XH2 - LA * ease(k2), Y), A(C2, k2), w=8, head=24)
            text(d, (XH2 - 10, Y + 150), "do lực kế 1 kéo", 40, C2, anchor="rm", alpha=k2)
            text(d, (XH2 - 10, Y + 200), "lên lực kế 2", 42, C2, anchor="rm", alpha=k2)
            dot(d, XH2, Y, 9, C2)
    finally:
        Y = y_old
    k3 = appear(t, M[1] + 0.2, 0.45)
    if k3 > 0:
        y0 = 1040 + (1 - k3) * 20
        card(d, (40, y0, 1040, y0 + 220), fill=A((239, 246, 255), k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, y0 + 70), "Cùng giá, ngược chiều,", 46, NAVY, alpha=k3)
        text(d, (W / 2, y0 + 150), "cùng độ lớn 2,0 N", 46, NAVY, alpha=k3)

# ---------------- canh 5: Bay (keo giat) roi Chua noi duoc ----------------
def jerk(t):
    """Keo giat: hai kim rung CUNG NHAU quanh vi tri can bang (khong ghi so)."""
    tau = t - 0.4
    if tau < 0: return 2.0
    return 2.5 - 0.5 * math.exp(-4 * tau) + 1.8 * math.exp(-0.9 * tau) * math.sin(2 * math.pi * 1.4 * tau)

def s_bay(img, d, t, sc):
    M = sc["M"]
    f = clamp(jerk(t), 0, FMAX)
    k2 = appear(t, M[1] - 0.1, 0.45)
    rig(d, f, f, hands=False)
    a1 = appear(t, 0.1, 0.4) * (1 - k2)
    if a1 > 0:
        y0 = 790
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        q = "“Bên kéo chỉ số lớn hơn”"
        ks = clamp((t - M[0] - 1.6) / 0.4)
        lw = tw(d, q, F(44)); yy = y0 + 200
        text(d, (W / 2 - 24, yy), q, 44, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            xa = W / 2 - 24 - lw / 2 - 6
            d.line([(xa, yy + 2), (xa + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 - 24 + lw / 2 + 34, yy), "✗", 46, DRED, alpha=a1 * ks)
        kk = a1 * appear(t, M[0] + 1.9, 0.4)
        card(d, (70, y0 + 300, 1010, y0 + 520), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 410), "✓ Hai kim vẫn đi cùng nhau", 48, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 790 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 280), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        text(d, (90, y0 + 180), "• Đã coi lực kế rất nhẹ", 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        global Y
        y_old = Y; Y = 1130
        try:
            Q1 = lambda s_, h=0.0: (XC + 60 - ROPE - s_, Y + h)
            se1 = luc_ke(d, Q1, 0, 20, 240, FMAX, None, nho=0.2, so=(0, 5), hw=46, ben=-1, co=40, alpha=k)
            hx1 = Q1(se1 + 40)[0]
            hx2 = one_meter(d, 1, None, XC + 60 + ROPE, body=220, so=(0, 5), alpha=k)
            arrow(d, (hx2 + 34, Y), (hx2 + 130, Y), A(INK, k), w=6, head=18)
            xw = hx1 - 40                                     # tuong giu dau luc ke 1 (thay tay)
            d.rectangle([xw - 40, Y - 120, xw, Y + 120], fill=A(LIGHT, k)); d.line([(xw, Y - 120), (xw, Y + 120)], fill=A(INK, k), width=5)
            for yy in range(int(Y - 110), int(Y + 120), 30): d.line([(xw - 40, yy + 26), (xw, yy)], fill=A(MUTED, k), width=3)
            d.line([(xw, Y), Q1(se1 - 16)], fill=A(NAVY, k), width=5)
            text(d, (xw - 20, Y - 160), "tường", 40, INK, alpha=k)
            d.ellipse([XC + 60 - 34, Y - 12, XC + 60 + 34, Y + 12], outline=A(NAVY, k), width=5)
        finally:
            Y = y_old
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1355, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1450, "Tường giữ đầu lực kế 1", 44, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Lực và phản lực:\nbằng nhau, cùng lúc",
             "Lực kế 1 buộc vào tường.\nKéo lực kế 2 bằng 3,5 N.\nLực kế 1 chỉ bao nhiêu?", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, lu, b, e = sc["hook"], sc["do"], sc["dapan"], sc["luc"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"), (do["t0"] + T_S[0], "tap")]
    out += [(do["t0"] + ts, "tick") for ts in T_S[1:]]
    out += [(da["t0"] + 0.15, "ding"), (lu["t0"] + lu["M"][1] + 0.2, "tap"), (b["t0"] + b["M"][0] + 1.6, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l10-newton3-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Định luật III Newton · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai lực kế móc vào nhau", draw=s_hook, tail=0.8, caps=[
   ("Giữ lực kế 1, kéo lực kế 2.", 3.0),
   ("Dừng video, chọn đáp án.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Kéo nhẹ, vừa, rồi mạnh.", 3.2),
   ("Đọc cả hai số.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Lực kế 1 cũng chỉ 2,0 N.", 3.0),
   ("Hai kim luôn đổi cùng nhau.", 3.0)]),
 dict(key="luc", title="Lực nào lên vật nào?", draw=s_luc, tail=0.6, caps=[
   ("Mỗi lực kế đo lực lên nó.", 3.4),
   ("Hai lực đặt lên hai vật.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Kéo giật thật mạnh thì sao?", 4.4),
   ("Chưa nói được gì?", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
