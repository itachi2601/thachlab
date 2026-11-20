# Clip: tn-l11-tudien-03 - Tu phang tu che tu hai tam nhom (16/11/2026)
# So lieu tu content/thi-nghiem/tn-l11-tudien-03.json (mo hinh C = eps.S/(9e9.4pi.d), khong phai so do that):
#   so_lieu_mau (S m2, d mm, eps, C pF): 0,04 1 1 354 ; 0,04 2 1 177 ; 0,02 1 1 177 ; 0,04 1 3 1061.
#   Moi lan chi doi mot yeu to roi tra ve goc (d = 1 mm, S = 0,04 m2) - dung cac_buoc.lam.
#   Cau chot THU NGHI (ca tu suy, chua hien tren man): S = 0,02 m2 VA eps = 3 (d = 1 mm) cung luc -> C ~ 531 pF (gap 1,5 lan 354).
# Du doan: truot lech con nua phan chong nhau -> C con khoang mot nua (dap an B). Bay: "phai noi nguon moi co C"
#   (hien_tuong_hay_sai 1). Khong tra loi san quiz cua muc (q1 LED, q2 C trung binh, q3 nang luong gap doi U).
from engine import *

def cap_pf(S, d_mm, eps): return eps * S / (9e9 * 4 * math.pi * d_mm * 1e-3) * 1e12
ROWS = [("ban đầu", 0.04, 1, 1, 354), ("d = 2 mm", 0.04, 2, 1, 177), ("lệch nửa tấm", 0.02, 1, 1, 177),
        ("chèn nhựa", 0.04, 1, 3, 1061)]
for _, S, dm, e, c in ROWS:
    assert round(cap_pf(S, dm, e)) == c, (S, dm, e, cap_pf(S, dm, e))   # khop so_lieu_mau
CHOT = round(cap_pf(0.02, 1, 3)); assert CHOT == 531                      # ca tu suy cau chot
assert CHOT not in [r[4] for r in ROWS]
RATIO = ["", "× 0,5", "× 0,5", "× 3"]
assert abs(ROWS[1][4] / ROWS[0][4] - 0.5) < 0.01 and abs(ROWS[3][4] / ROWS[0][4] - 3) < 0.01

AL = (170, 178, 192); ALD = (95, 105, 125)       # nhom
PLA = (253, 224, 140)                            # tam nhua
OVL = (191, 219, 254)                            # phan doi dien
SCR = (220, 240, 225)
BOXF = (70, 78, 100)
DRED = (185, 28, 28)
X0, L, YB = 120, 600, 800                        # tam duoi: x 120..720 (20 cm), mat tren y = YB
PXMM = 50                                        # khe ve phong to: 1 mm = 50 px

def dash(d, p1, p2, col, w=3, on=14, off=10):
    Ln = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(Ln // (on + off)) + 1
    for i in range(n):
        a, b = i * (on + off) / Ln, min(1, (i * (on + off) + on) / Ln)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=col, width=w)

def rig(d, dmm=1.0, shift=0.0, plastic=0.0, reading="354 pF", ghost=False, a=1.0, labels=True, meter=True):
    """Hinh canh hai tam nhom + dong ho do C. dmm: khe (mm), shift 0..1: tam tren truot sang phai toi nua tam,
    plastic 0..1: tam nhua truot vao tu trai."""
    gap = dmm * PXMM; yt = YB - gap                       # mat duoi tam tren
    sx = shift * L / 2
    xa0, xa1 = X0 + sx, X0 + L + sx                      # tam tren
    o0, o1 = max(X0, xa0), min(X0 + L, xa1)              # phan doi dien
    d.rectangle([o0, yt, o1, YB], fill=A(OVL, a))
    if plastic > 0:                                      # nhua day 1 mm kin khe, truot vao tu trai
        px1 = X0 + L * ease(plastic)
        d.rectangle([X0, yt, px1, YB], fill=A(PLA, a), outline=A((180, 140, 40), a), width=2)
    d.rectangle([X0, YB, X0 + L, YB + 16], fill=A(AL, a), outline=A(ALD, a), width=3)
    d.rectangle([xa0, yt - 16, xa1, yt], fill=A(AL, a), outline=A(ALD, a), width=3)
    if ghost:                                            # minh hoa thao tac o canh du doan: tam tren truot nua tam
        g = A(PURPLE, a)
        for (p, q) in (((X0 + L / 2, yt - 16), (X0 + L * 1.5, yt - 16)), ((X0 + L * 1.5, yt - 16), (X0 + L * 1.5, yt)),
                       ((X0 + L / 2, yt), (X0 + L * 1.5, yt))):
            dash(d, p, q, g, w=4)
        arrow(d, (560, yt - 70), (760, yt - 70), g, w=7, head=20)
    # day noi ve dong ho (khong ve khi an dong ho)
    if meter: d.line([(100, 560), (100, YB + 44), (170, YB + 44), (170, YB + 16)], fill=A(NAVY, a), width=5, joint="curve")
    if meter: d.line([(330, 560), (330, yt - 60), (xa0 + 250, yt - 60), (xa0 + 250, yt - 16)], fill=A(NAVY, a), width=5, joint="curve")
    # dong ho
    if not meter: return
    card(d, (60, 330, 420, 560), fill=A(BOXF, a), r=22)
    text(d, (240, 370), "điện dung", 36, WHITE, alpha=a)
    card(d, (80, 410, 400, 530), fill=A(SCR, a), r=12)
    text(d, (240, 470), reading, 52, (20, 60, 30), alpha=a)
    # nhan
    if not labels: return
    text(d, (X0 + L / 2, YB + 66), "20 cm", 38, MUTED, alpha=a)
    text(d, (1030, YB + 66), "khe vẽ phóng to", 36, MUTED, anchor="rm", alpha=a)
    kd = a * (1 - ease(shift * 4))                       # nhan d an khi tam tren truot sang (che cho)
    if kd > 0.02:
        xr = X0 + L + 20
        arrow(d, (xr + 20, yt + gap / 2), (xr + 20, yt + 2), A(INK, kd), w=4, head=12)
        arrow(d, (xr + 20, yt + gap / 2), (xr + 20, YB - 2), A(INK, kd), w=4, head=12)
        text(d, (xr + 44, yt + gap / 2), f"d = {round(dmm)} mm", 40, INK,
             anchor="lm", alpha=kd)

def table(d, n, y=1000, ratio=0, hl=None, ka=1.0):
    """Bang Lan do - C; n hang da hien; ratio = so hang da hien cot 'so voi ban dau'."""
    card(d, (40, y, 1040, y + 470), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 560, 850)
    for x, c in zip(xs, ("", "C (pF)", "so lần đầu")):
        if c: text(d, (x, y + 50), c, 40, INK)
    d.line([(70, y + 90), (1010, y + 90)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 140 + i * 82; lab, *_, c = ROWS[i]
        if hl == i: d.rounded_rectangle([60, yy - 36, 1020, yy + 36], radius=18, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), lab, 42, INK); text(d, (xs[1], yy), str(c), 46, BLUE)
        if i < ratio and RATIO[i]: text(d, (xs[2], yy), RATIO[i], 46, GREEN)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    a = appear(t, M[1] - 0.2, 0.5)
    rig(d, ghost=a > 0.5, labels=False)
    if a <= 0: return
    y0 = 980 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 580), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=33)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 250, "Trượt tấm trên lệch, chỉ còn\nnửa phần chồng nhau.\nC đo được thế nào?", 48, INK,
          maxw=920, alpha=a)
    text(d, (W / 2, y0 + 430), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 515, 940, y0 + 527], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 515, 140 + 800 * (1 - p), y0 + 527], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
# moc (giay trong canh): (bat dau doi, xong doi) ; tra ve goc ; meter + hang bang doi CUNG luc khi xong doi
R1 = 0.6
D_ON, D_OFF = (1.3, 1.9), (3.0, 3.4)
SL_ON, SL_OFF = (4.8, 5.4), (6.4, 6.8)          # SL_ON[0] = M[1] (phu de 2) - kiem trong s_do
PL_ON = (7.1, 7.8)

def s_do(img, d, t, sc):
    M = sc["M"]; assert abs(M[1] - SL_ON[0]) < 0.05, M
    dmm = 1 + ease((t - D_ON[0]) / (D_ON[1] - D_ON[0])) - ease((t - D_OFF[0]) / (D_OFF[1] - D_OFF[0]))
    sh = ease((t - SL_ON[0]) / (SL_ON[1] - SL_ON[0])) - ease((t - SL_OFF[0]) / (SL_OFF[1] - SL_OFF[0]))
    pl = clamp((t - PL_ON[0]) / (PL_ON[1] - PL_ON[0]))
    n = 0; rd = "354 pF"
    if t >= R1: n = 1
    if t >= D_ON[1]: n = 2; rd = "177 pF" if t < D_OFF[1] else "354 pF"
    if t >= SL_ON[1]: n = 3; rd = "177 pF" if t < SL_OFF[1] else "354 pF"
    if t >= PL_ON[1]: n = 4; rd = "1061 pF"
    if n >= 2: assert rd == f"{ROWS[n - 1][4]} pF" or rd == "354 pF"
    rig(d, dmm, sh, pl if t >= PL_ON[0] else 0, rd)
    table(d, n)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN B"
    pw = tw(d, lab, F(40)) + 52
    card(d, (W - 60 - pw, 300, W - 60, 364), fill=A(NAVY, ka), r=32)
    text(d, (W - 60 - pw / 2, 332), lab, 40, WHITE, alpha=ka)
    rig(d, 1, 1, 0, "177 pF", labels=False, meter=False)
    table(d, 4, y=930, ratio=sum(t >= 0.5 + 0.3 * i for i in range(4)), hl=2, ka=appear(t, 0.2, 0.3))
    k1 = appear(t, M[1] + 0.3, 0.45)
    if k1 > 0:
        card(d, (40, 1430, 1040, 1590), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        ctext(d, 1510, "C tăng theo S đối diện, ε\nC giảm khi d tăng", 44, (21, 110, 55), maxw=920, alpha=k1)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    rig(d, labels=False)
    if a1 > 0:
        y0 = 1000
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 96), fill=A(DRED, a1), r=33)
        text(d, (W / 2, y0 + 63), "BẪY", 40, WHITE, alpha=a1)
        k3 = a1 * appear(t, 0.5, 0.5); k4 = a1 * appear(t, 1.8, 0.5)
        ctext(d, y0 + 210, "Tưởng phải nối nguồn\nmới có C", 46, INK, maxw=920, alpha=k3)
        ctext(d, y0 + 420, "Không nguồn,\nvẫn đo được C", 46, (21, 110, 55), maxw=920, alpha=k4)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Dây đo thêm C", "• Năng lượng của tụ?")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (80, y0 + 220 + j * 150), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot -> THU NGHI: lech nua tam VA chen nhua eps = 3 (531 pF, chua hien tren man); goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Đổi từng yếu tố một", 50, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1590), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 696), fill=A(ORANGE, k1), r=33)
    text(d, (W / 2, 663), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 880, "Lệch nửa tấm và chèn nhựa\nε = 3: C bao nhiêu, so với\nlần đầu 354 pF?", 48, INK,
          maxw=940, alpha=appear(t, M[0] + 0.9, 0.5))
    th = M[0] + 0.9; kh = appear(t, th + 2.5, 0.5)
    card(d, (110, 1140, 970, 1480), fill=A((255, 247, 237), k1), r=24)
    ctext(d, 1215, "Gợi ý", 40, INK, alpha=k1)
    if t > th and kh < 1:
        p = clamp((t - th) / 2.5); kb = k1 * (1 - kh)
        d.rounded_rectangle([200, 1334, 880, 1346], radius=6, fill=A(LIGHT, kb))
        d.rounded_rectangle([200, 1334, 200 + 680 * (1 - p), 1346], radius=6, fill=A(ORANGE, kb))
    ctext(d, 1350, "Hai yếu tố\nđổi một lúc", 48, (154, 52, 18), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + x, "tap") for x in (D_ON[1], SL_ON[1], PL_ON[1])]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out

CLIP = dict(id="tn-l11-tudien-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Tụ điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tụ tự chế từ hai tấm nhôm", draw=s_hook, tail=0.3, caps=[
   ("Hai tấm nhôm cách nhau 1 mm.", 3.0),
   ("Nghĩ trước khi xem tiếp.", 6.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Mỗi lần chỉ đổi một yếu tố.", 4.4),
   ("Trượt lệch nửa tấm, rồi chèn nhựa.", 3.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=1.2, caps=[
   ("Lệch nửa tấm: C còn một nửa.", 4.0),
   ("Chỉ phần đối diện mới tính.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=1.0, caps=[
   ("Bẫy về nguồn điện.", 4.4),
   ("Hai điều bỏ ngỏ.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.4)]),
])
