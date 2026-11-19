# Clip: tn-l9-pxtp-01 - Khoi ban tru thuy tinh: tang goc toi toi khi tia khuc xa bien mat (KHTN 9, lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-pxtp-01.json (_kiem_so()):
#   so_lieu_mau (i, r doc): 20 31 | 30 49 | 35 60 | 40 74 | 41 80 | 42 "khong con" ; n = 1,5 ; i_th = 41,81 do.
# Du doan (K10, khong nut A-D): tang dan i, toi khoang bao nhieu do thi tia lo ra khong khi bien mat?
#   (khoang 30 / khoang 42 / khoang 60 / khong mat, gan 90 van con) -> dap an: khoang 42 do.
#   Khong trung cau Tu kiem tra: C1 (i_th 40, i 25: co ca hai tia), C2 (thuy tinh -> nuoc 62,5), C4 (khong khi -> nuoc),
#   C5 (30 do voi mat -> 60), C7 (nuoc 50 do), dien buoc (45 do voi thuy tinh) -> khong dung 45 do.
# Hop exp: cau "Doc so lieu" hoi lech doc/tinh toi da va goc toi han nam khoang nao -> clip KHONG hien cot "r tinh",
#   KHONG noi "goc toi han giua 41 va 42", KHONG hien 41,8.
# Hinh: mat phang nam ngang qua tam I, khoi ban tru o duoi. Tia toi tu duoi-trai theo ban kinh vao I (khong gay o mat cong),
#   tia khuc xa len tren-phai (r tu phap tuyen), tia phan xa xuong-phai goc = i, di theo ban kinh ra ngoai. Goc ve = Snell dung.
#   Do sang: tia khuc xa mo dan, tia phan xa sang dan; i >= i_th: chi con tia phan xa, sang nhu tia toi.
# Bay = hien_tuong_hay_sai[2] (do r tu mat phang): o 41 do tia lo hop mat phang 10 do, r dung = 80 do tu phap tuyen.
#   KHONG dung [1] (co khuc xa thi khong phan xa) vi trung dap an Cau 1; [0] trung lua chon nhieu cua Du doan.
# Chua noi duoc = ghi_chu kho (so lieu minh hoa).
# THU NGHI: cung khoi, i = 38 do -> r vao khoang nao? Dap an giua 60 va 74 do (tinh 67,4; ghi vao ghi_chu kho).
from engine import *

N = 1.5
ROWS = [(20, 31), (30, 49), (35, 60), (40, 74), (41, 80), (42, None)]
ITH = math.degrees(math.asin(1 / N))
CHOT_I = 38


def r_of(i):
    x = N * math.sin(math.radians(i))
    return math.degrees(math.asin(x)) if x <= 1 else None


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-pxtp-01.json")))
    hang = k["so_lieu_mau"]["hang"]
    assert len(hang) == len(ROWS)
    for (i, r), h in zip(ROWS, hang):
        assert h[0] == i, (i, h)
        if r is None:
            assert h[1] == "không còn" and r_of(i) is None and i > ITH
        else:
            assert h[1] == r and abs(r_of(i) - r) < 0.65 and r > i, (i, r, r_of(i))   # ra khong khi: lech xa phap tuyen
    assert k["tham_so"][0]["mac_dinh"] == N and "41.81" in k["so_lieu_mau"]["ghi_chu"]
    assert 41 < ITH < 42
    assert round(90 - r_of(41)) == 10                                              # so bay
    rc = r_of(CHOT_I); assert 60 < rc < 74 and "i = 38°" in k["so_lieu_mau"]["ghi_chu"]
_kiem_so()

C = (540, 560); RD, RB = 300, 245
DISK = (246, 243, 236); RING = (120, 115, 105); GLASS = (191, 219, 254); BEAM = (220, 38, 38); DRED = (185, 28, 28)
DGREEN = (10, 110, 50)


def u_src(i):  return (-math.sin(math.radians(i)), math.cos(math.radians(i)))      # tu I ve phia nguon (duoi-trai)
def u_refr(r): return (math.sin(math.radians(r)), -math.cos(math.radians(r)))      # tia khuc xa (tren-phai)
def u_refl(i): return (math.sin(math.radians(i)), math.cos(math.radians(i)))       # tia phan xa (duoi-phai)
def P(u, L): return (C[0] + u[0] * L, C[1] + u[1] * L)


def _kiem_hinh():
    for i in [20, 30, 35, 40, 41, 42, CHOT_I]:
        s, f = u_src(i), u_refl(i)
        # tia toi di vao I theo huong -s; goc voi phap tuyen (truc dung) = i ; phan xa: goc = i, doi xung qua phap tuyen
        assert abs(math.degrees(math.acos(s[1])) - i) < 1e-9 and abs(math.degrees(math.acos(f[1])) - i) < 1e-9
        assert abs(s[0] + f[0]) < 1e-12 and abs(s[1] - f[1]) < 1e-12
        r = r_of(i)
        if r is not None:
            g = u_refr(r); assert g[0] > 0 and g[1] < 0 and abs(math.degrees(math.acos(-g[1])) - r) < 1e-9
            assert abs(math.sin(math.radians(r)) - N * math.sin(math.radians(i))) < 1e-9          # 1.sin r = n.sin i
_kiem_hinh()


def dash(d, p1, p2, col, w=3, on=14, off=10):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (on + off)) + 1
    for k in range(n):
        a, b = k * (on + off) / L, min(1, (k * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=col, width=w)


def chev(d, p, q, col, s=16, w=4):
    x, y = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2; ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=col, width=w)


def disk(d):
    d.ellipse([C[0] - RD, C[1] - RD, C[0] + RD, C[1] + RD], fill=DISK, outline=RING, width=4)
    for deg in range(0, 360, 10):
        a = math.radians(deg); L = 22 if deg % 30 == 0 else 12
        d.line([(C[0] + (RD - L) * math.cos(a), C[1] + (RD - L) * math.sin(a)),
                (C[0] + RD * math.cos(a), C[1] + RD * math.sin(a))], fill=RING, width=3)
    d.pieslice([C[0] - RB, C[1] - RB, C[0] + RB, C[1] + RB], 0, 180, fill=A(GLASS, 0.85), outline=BLUE, width=4)
    d.line([(C[0] - RB, C[1]), (C[0] + RB, C[1])], fill=BLUE, width=5)
    dash(d, (C[0], C[1] - RD + 6), (C[0], C[1] + RD - 6), A(NAVY, 0.7), w=3)
    text(d, (C[0] - 330, C[1] - 250), "không khí", 40, MUTED, bold=False)
    text(d, (C[0] + 330, C[1] + 250), "thuỷ tinh", 40, BLUE)
    text(d, (C[0] - 24, C[1] - 30), "I", 40, NAVY)


def pen(d, i):
    u = u_src(i); a, b = P(u, RD + 25), P(u, RD + 130)
    d.line([a, b], fill=(55, 60, 75), width=30); dot(d, a[0], a[1], 9, BEAM)


def weights(i):
    """(do sang tia khuc xa, do sang tia phan xa) - khuc xa mo dan, phan xa sang dan; vuot i_th: chi con phan xa."""
    x = N * math.sin(math.radians(i))
    if x > 1: return 0.0, 1.0
    return 0.3 + 0.7 * (1 - x ** 4), 0.2 + 0.45 * x ** 4


def rays(d, i, arcs=True, lab=None):
    a = P(u_src(i), RD + 25); r = r_of(i); kr, kf = weights(i)
    d.line([a, C], fill=BEAM, width=6); chev(d, P(u_src(i), RB + 40), P(u_src(i), 60), BEAM)
    f_end = P(u_refl(i), RD)
    d.line([C, f_end], fill=A(BEAM, kf), width=6 if kf > 0.9 else 4); chev(d, C, P(u_refl(i), RB), A(BEAM, kf))
    if r is not None:
        g_end = P(u_refr(r), RD)
        d.line([C, g_end], fill=A(BEAM, kr), width=5); chev(d, C, P(u_refr(r), RB), A(BEAM, kr))
    if arcs:
        d.arc([C[0] - 110, C[1] - 110, C[0] + 110, C[1] + 110], 90, 90 + i, fill=NAVY, width=5)
        if r is not None: d.arc([C[0] - 140, C[1] - 140, C[0] + 140, C[1] + 140], 270, 270 + r, fill=DGREEN, width=5)
        if lab:
            m = math.radians(90 + i + 25); text(d, (C[0] + 150 * math.cos(m), C[1] + 150 * math.sin(m)), lab[0], 42, NAVY)  # ngoai goc, khong de tia toi
            if r is not None:
                m = math.radians(270 + r / 2); text(d, (C[0] + 195 * math.cos(m), C[1] + 195 * math.sin(m)), lab[1], 42, DGREEN)


def readout(d, i, r_txt):
    card(d, (90, 975, 500, 1045), fill=WHITE, outline=NAVY, r=22, w=3)
    text(d, (295, 1010), f"i = {i}°", 44, NAVY)
    card(d, (560, 975, 990, 1045), fill=WHITE, outline=DGREEN, r=22, w=3)
    if r_txt: text(d, (775, 1010), r_txt, 44, DGREEN)
    else: text(d, (775, 1010), "r = …", 44, MUTED, bold=False)


XS = (330, 720)
def table(d, n, y0=1080, hl=()):
    card(d, (60, y0, 1020, y0 + 92 + 6 * 60 + 18), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y0 + 48), "i", 44, NAVY); text(d, (XS[1], y0 + 48), "r đọc được", 42, DGREEN)
    d.line([(90, y0 + 88), (990, y0 + 88)], fill=LIGHT, width=3)
    for j in range(n):
        i, r = ROWS[j]; yy = y0 + 122 + 60 * j
        if j in hl: d.rounded_rectangle([80, yy - 28, 1000, yy + 28], radius=14, fill=(255, 237, 213))
        text(d, (XS[0], yy), f"{i}°", 44, INK)
        text(d, (XS[1], yy), f"{r}°" if r is not None else "không còn", 44, INK if r is not None else DRED)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    disk(d); pen(d, 20); rays(d, 20, lab=("20°", "31°"))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Tăng dần góc tới i.", "Khoảng bao nhiêu độ thì", "tia ló ra không khí biến mất?")):
        text(d, (W / 2, y0 + 160 + j * 76), s, 48, INK, alpha=a)
    text(d, (W / 2, y0 + 420), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 485, 940, y0 + 499], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 485, 140 + 800 * (1 - p), y0 + 499], radius=7, fill=A(PURPLE, a))


# ---------------- canh 2: Tien hanh ----------------
T0, DT, ROT, READ, ROW = 0.6, 1.5, 0.5, 0.8, 0.8
def do_state(t):
    """-> (goc i dang chieu, chi so lan do dang dung (-1 khi dang xoay), so hang bang)."""
    rows, ang, k_on = 0, ROWS[0][0], -1
    for k, (i, r) in enumerate(ROWS):
        tk = T0 + DT * k
        if t < tk: break
        if k > 0 and t < tk + ROT:
            ang = lerp(ROWS[k - 1][0], i, ease((t - tk) / ROT)); k_on = -1
        else:
            ang = i; k_on = k if t >= tk + READ else -1
        if t >= tk + ROW: rows = k + 1
    return ang, k_on, rows


def r_txt(k): return f"r = {ROWS[k][1]}°" if ROWS[k][1] is not None else "không còn tia ló"


def card_state(ang, k_on, rows):
    """(i hien, chu r hoac None). Laser con dung o goc hang vua ghi -> giu so cua hang do (khop bang)."""
    if k_on >= 0: return ROWS[k_on][0], r_txt(k_on)
    if rows > 0 and abs(ang - ROWS[rows - 1][0]) < 0.5: return ROWS[rows - 1][0], r_txt(rows - 1)
    return round(ang), None


def s_do(img, d, t, sc):
    ang, k_on, rows = do_state(t)
    disk(d); pen(d, ang); rays(d, ang)
    readout(d, *card_state(ang, k_on, rows))
    table(d, rows)


def _kiem_dong_bo():
    """Moi 0,05 s: so r chi hien khi laser dung yen o dung goc cua hang; 'khong con' chi khi hinh khong ve tia khuc xa."""
    bad = []; t = 0.0
    while t < 11.0:
        ang, k_on, rows = do_state(t)
        if k_on >= 0:
            if abs(ang - ROWS[k_on][0]) > 1e-9: bad.append((round(t, 2), "r hien khi chua dung"))
            r = r_of(ang)
            if (r is None) != (ROWS[k_on][1] is None): bad.append((round(t, 2), "tia khuc xa khong khop so"))
            if r is not None and abs(r - ROWS[k_on][1]) > 0.65: bad.append((round(t, 2), "r lech tia"))
        ci, cr = card_state(ang, k_on, rows)
        if cr is not None and ci not in [x[0] for x in ROWS[:rows]]: bad.append((round(t, 2), "the r co so ma bang chua ghi"))
        if cr is None and ci in [x[0] for x in ROWS[:rows]]: bad.append((round(t, 2), "the r = … o goc da ghi"))
        if rows > 0:
            done = max(k for k in range(6) if t >= T0 + DT * k)
            if rows > done + 1: bad.append((round(t, 2), "hang som"))
        t += 0.05
    if do_state(10.5)[2] != 6: bad.append("chua du 6 hang")
    return bad


# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    disk(d); pen(d, 42); rays(d, 42, arcs=False)
    pill(d, "ĐÁP ÁN: khoảng 42°", 985, appear(t, 0.15, 0.4))
    table(d, 6, hl=(4, 5))
    k = appear(t, M[1] + 0.6, 0.5)
    if k > 0:
        card(d, (110, 1580, 970, 1660), fill=A((236, 253, 243), k), outline=A(GREEN, k), r=22, w=3)
        text(d, (W / 2, 1620), "Phản xạ toàn phần", 46, DGREEN, alpha=k)


# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    disk(d); pen(d, 41); rays(d, 41, arcs=False)
    r41 = r_of(41)
    kx = a1 * appear(t, 0.9, 0.4); kv = a1 * appear(t, 2.6, 0.4)
    if kx > 0:                                                        # goc voi mat phang (sai)
        d.arc([C[0] - 230, C[1] - 230, C[0] + 230, C[1] + 230], 270 + r41, 360, fill=A(DRED, kx), width=6)
        text(d, (C[0] + 368, C[1] - 22), "10°", 42, DRED, alpha=kx)
    if kv > 0:                                                        # goc voi phap tuyen (dung)
        d.arc([C[0] - 130, C[1] - 130, C[0] + 130, C[1] + 130], 270, 270 + r41, fill=A(DGREEN, kv), width=6)
        m = math.radians(270 + r41 / 2); text(d, (C[0] + 175 * math.cos(m), C[1] + 175 * math.sin(m)), "80°", 42, DGREEN, alpha=kv)
    y = 1040
    if a1 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        text(d, (W / 2, y + 160), "“Ở 41°, r = 10°”", 48, INK, alpha=a1)
        text(d, (820, y + 160), "✗", 64, DRED, alpha=a1 * appear(t, 1.6, 0.4))
        text(d, (W / 2, y + 245), "10° là góc với mặt phẳng", 44, DRED, alpha=kx)
        text(d, (W / 2, y + 330), "✓ Đo từ pháp tuyến: r = 80°", 46, DGREEN, alpha=kv)
    if k3 > 0:
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 170), "Số liệu minh hoạ (n = 1,5),", 46, INK, alpha=kk)
        text(d, (W / 2, y + 235), "chưa phải số đo thật", 46, INK, alpha=kk)


# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Thuỷ tinh ra không khí: i đủ lớn", 50, DGREEN, alpha=k0)
    text(d, (W / 2, 450), "thì không còn tia ló", 50, DGREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1290), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate((f"Cùng khối, chiếu i = {CHOT_I}°.", "Góc khúc xạ r vào khoảng nào?")):
        text(d, (W / 2, 800 + j * 78), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.2, 0.5)
    if kh > 0:
        card(d, (90, 1030, 990, 1260), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1105), "Gợi ý: gần 42°, r tăng", 44, INK, alpha=kh)
        text(d, (W / 2, 1180), "càng lúc càng nhanh", 44, (176, 64, 8), alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + T0 + DT * k + READ, "tap") for k in range(6)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.6, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-pxtp-01", header="KHTN 9 · THÍ NGHIỆM", footer="Phản xạ toàn phần · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Khối bán trụ thuỷ tinh", draw=s_hook, tail=0.3, caps=[
   ("Laser từ thuỷ tinh ra không khí.", 3.6),
   ("Tự trả lời trước khi xem.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Xoay laser, luôn hướng vào tâm I.", 4.6),
   ("Đọc góc r ở mỗi lần.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Ở 41°, tia ló gần sát mặt phẳng.", 4.0),
   ("Vượt qua: ánh sáng bật lại hết.", 4.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 5.2),
   ("Câu còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 7.6)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
