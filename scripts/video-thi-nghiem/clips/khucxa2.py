# Clip: tn-l9-khucxa-02 - Do goc khuc xa qua khoi nhua ban tru tren dia chia do (KHTN 9, lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-khucxa-02.json (_kiem_so()):
#   so_lieu_mau (i, r doc, sin i / sin r): 20 13 1,52 | 35 22 1,53 | 50 31 1,49 | 65 37 1,51 | 80 41 1,50 ; n = 1,5.
# Du doan (K10, khong nut A-D): i tang deu 20 -> 80 do (moi lan +15 do), r thay doi the nao?
#   (them 15 do nhu i / them deu 10 do / them it dan / giam dan) -> dap an: r tang, ve sau them it dan (+9 +9 +6 +4).
#   Khong trung cau Tu kiem tra cua bai (C1 i = 0, C2 v, C3 60 do -> 35,3, C4 nuoc ra 40 do, C5 60 do voi mat, C7 30 do).
# Hop exp: cau "Doc so lieu" sau video hoi TRUNG BINH nam ti so va LAN LECH NHIEU NHAT -> clip KHONG tinh trung binh,
#   KHONG noi lan nao lech, KHONG noi "goc nho sai lech tuong doi lon" (rut_ra[1] cua kho).
# Hinh: mat phang khoi ban tru nam ngang qua tam dia, khoi o duoi; tia toi tu tren-trai vao tam, tia khuc xa xuong-phai,
#   di theo ban kinh nen khong gay o mat cong. Goc ve = Snell dung (n = 1,5); so doc = so lam tron trong kho (assert).
# Bay = hien_tuong_hay_sai[0] (chia i cho r): 20 : 13 = 1,54 ; 80 : 41 = 1,95 (tinh ngay tren man tu so kho).
# Chua noi duoc = ghi_chu kho "so lieu minh hoa, chua phai so do that".
# THU NGHI: cung khoi, doc r = 25 do -> i ? Dap an i = 39 do (sin i = 1,5 . sin 25 = 0,634; ghi them vao ghi_chu kho).
#   Hop chot KHONG ghi ti so sin/chiet suat (cach giai); goi y chi cho du kien "n = 1,5".
from engine import *

N = 1.5
ROWS = [(20, 13, "1,52"), (35, 22, "1,53"), (50, 31, "1,49"), (65, 37, "1,51"), (80, 41, "1,50")]
CHOT_R, CHOT_I = 25, 39


def r_of(i): return math.degrees(math.asin(math.sin(math.radians(i)) / N))


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-khucxa-02.json")))
    hang = k["so_lieu_mau"]["hang"]
    assert len(hang) == len(ROWS)
    for (i, r, q), h in zip(ROWS, hang):
        assert [i, r] == h[:2], (i, r, h)
        assert q == f"{h[2]:.2f}".replace(".", ","), (q, h[2])
        assert round(r_of(i)) == r, (i, r_of(i))                       # tia ve dung Snell khop so doc
        assert r < i                                                    # vao nhua: lech gan phap tuyen
        qq = math.sin(math.radians(i)) / math.sin(math.radians(r))
        assert abs(qq - h[2]) < 0.006, (i, qq)
    assert k["tham_so"][1]["gia_tri"] == N
    assert abs(20 / 13 - 1.54) < 0.005 and abs(80 / 41 - 1.95) < 0.005     # so bay
    assert round(math.degrees(math.asin(N * math.sin(math.radians(CHOT_R))))) == CHOT_I
    assert "r = 25°" in k["so_lieu_mau"]["ghi_chu"]
_kiem_so()

C = (540, 660); RD, RB = 320, 255
DISK = (246, 243, 236); RING = (120, 115, 105); BLOCK = (191, 219, 254); BEAM = (220, 38, 38); DRED = (185, 28, 28)
DGREEN = (10, 110, 50)


def u_in(i):   # huong tu tam ve phia nguon (tren-trai)
    return (-math.sin(math.radians(i)), -math.cos(math.radians(i)))


def u_out(r):  # huong tia khuc xa (duoi-phai)
    return (math.sin(math.radians(r)), math.cos(math.radians(r)))


def P(u, L): return (C[0] + u[0] * L, C[1] + u[1] * L)


def _kiem_hinh():
    for i, r, _ in ROWS:
        a, b = u_in(i), u_out(r_of(i))
        assert a[0] < 0 and a[1] < 0 and b[0] > 0 and b[1] > 0          # tia toi, tia khuc xa o hai ben phap tuyen
        # goc voi phap tuyen (truc thang dung) dung bang i va r
        assert abs(math.degrees(math.acos(-a[1])) - i) < 1e-6 and abs(math.degrees(math.acos(b[1])) - r_of(i)) < 1e-6
        # tia trong khoi di theo ban kinh -> vuong goc mat cong: tich vo huong voi phap tuyen mat cong (= chinh b) bang 1
        assert abs(b[0] * b[0] + b[1] * b[1] - 1) < 1e-9
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
    # khoi nhua ban tru: nua duoi, mat phang ngang qua tam
    d.pieslice([C[0] - RB, C[1] - RB, C[0] + RB, C[1] + RB], 0, 180, fill=A(BLOCK, 0.85), outline=BLUE, width=4)
    d.line([(C[0] - RB, C[1]), (C[0] + RB, C[1])], fill=BLUE, width=5)
    dash(d, (C[0], C[1] - RD + 6), (C[0], C[1] + RD - 6), A(NAVY, 0.7), w=3)
    text(d, (C[0] + 300, C[1] + 250), "nhựa", 40, BLUE)
    text(d, (C[0] + 300, C[1] - 260), "không khí", 40, MUTED, bold=False)


def pen(d, i, on=True):
    u = u_in(i); a, b = P(u, RD + 30), P(u, RD + 140)
    d.line([a, b], fill=(55, 60, 75), width=30)
    if on: dot(d, a[0], a[1], 9, BEAM)


def beam(d, i, ka=1.0, arcs=True, lab=True):
    r = r_of(i); a, ce, b = P(u_in(i), RD + 30), C, P(u_out(r), RD)
    d.line([a, ce], fill=A(BEAM, ka), width=6); chev(d, a, ce, A(BEAM, ka))
    d.line([ce, b], fill=A(BEAM, ka), width=6); chev(d, ce, P(u_out(r), RB), A(BEAM, ka))
    if arcs:
        d.arc([C[0] - 115, C[1] - 115, C[0] + 115, C[1] + 115], 270 - i, 270, fill=A(NAVY, ka), width=5)
        d.arc([C[0] - 150, C[1] - 150, C[0] + 150, C[1] + 150], 90 - r, 90, fill=A(DGREEN, ka), width=5)
        if lab:
            m = math.radians(270 - i / 2); text(d, (C[0] + 155 * math.cos(m), C[1] + 155 * math.sin(m)), "i", 46, NAVY, alpha=ka)
            m = math.radians(90 - r / 2); text(d, (C[0] + 190 * math.cos(m), C[1] + 190 * math.sin(m)), "r", 46, DGREEN, alpha=ka)


def readout(d, i, r, ka_r):
    card(d, (90, 1000, 500, 1070), fill=WHITE, outline=NAVY, r=22, w=3)
    text(d, (295, 1035), f"i = {i}°", 44, NAVY)
    card(d, (580, 1000, 990, 1070), fill=WHITE, outline=DGREEN, r=22, w=3)
    if ka_r > 0: text(d, (785, 1035), f"r = {r}°", 44, DGREEN, alpha=ka_r)
    else: text(d, (785, 1035), "r = …", 44, MUTED, bold=False)


XS = (230, 430, 800)
def table(d, n, y0=1100, plus=0.0, ratio=0.0, hl=-1):
    card(d, (60, y0, 1020, y0 + 92 + 5 * 64 + 20), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y0 + 48), "i", 44, NAVY); text(d, (XS[1], y0 + 48), "r", 44, DGREEN)
    if ratio > 0: text(d, (XS[2], y0 + 48), "sin i / sin r", 42, INK, alpha=ratio)
    d.line([(90, y0 + 88), (990, y0 + 88)], fill=LIGHT, width=3)
    for j in range(n):
        i, r, q = ROWS[j]; yy = y0 + 125 + 64 * j
        if j == hl: d.rounded_rectangle([80, yy - 30, 1000, yy + 30], radius=14, fill=(255, 237, 213))
        text(d, (XS[0], yy), f"{i}°", 44, INK); text(d, (XS[1], yy), f"{r}°", 44, INK)
        if plus > 0 and j > 0:
            text(d, (XS[0] + 110, yy - 32), "+15°", 38, MUTED, bold=False, alpha=plus)
            text(d, (XS[1] + 150, yy - 32), f"+{r - ROWS[j - 1][1]}°", 40, ORANGE, alpha=plus)
        if ratio > 0: text(d, (XS[2], yy), q, 44, BLUE, alpha=ratio)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    disk(d); pen(d, 20); beam(d, 20, appear(t, 0.5, 0.5), lab=True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Tăng i từ 20° tới 80°,", "mỗi lần thêm 15°.", "Góc r thay đổi thế nào?")):
        text(d, (W / 2, y0 + 160 + j * 76), s, 48, INK, alpha=a)
    text(d, (W / 2, y0 + 420), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 485, 940, y0 + 499], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 485, 140 + 800 * (1 - p), y0 + 499], radius=7, fill=A(PURPLE, a))


# ---------------- canh 2: Tien hanh ----------------
T0, DT, ROT, READ, ROW = 0.6, 1.8, 0.6, 0.9, 1.3
def do_state(t):
    """-> (goc i dang chieu, chi so lan do dang dung (-1 khi dang xoay), so hang bang)."""
    rows, ang, k_on = 0, ROWS[0][0], -1
    for k, (i, r, _) in enumerate(ROWS):
        tk = T0 + DT * k
        if t < tk: break
        if k > 0 and t < tk + ROT:
            ang = lerp(ROWS[k - 1][0], i, ease((t - tk) / ROT)); k_on = -1
        else:
            ang = i; k_on = k if t >= tk + READ else -1
        if t >= tk + ROW: rows = k + 1
    return ang, k_on, rows


def s_do(img, d, t, sc):
    ang, k_on, rows = do_state(t)
    disk(d); pen(d, ang)
    if t >= T0: beam(d, ang, 1.0, lab=False)
    i_show = round(ang) if k_on < 0 else ROWS[k_on][0]
    if k_on >= 0: readout(d, i_show, ROWS[k_on][1], 1.0)
    else: readout(d, i_show, 0, 0.0)
    table(d, rows)


def _kiem_dong_bo():
    """Moi 0,05 s: so r chi hien khi laser dung yen o dung goc cua hang do; hang bang chi hien sau khi doc."""
    bad = []; t = 0.0
    while t < 11.0:
        ang, k_on, rows = do_state(t)
        if k_on >= 0 and abs(ang - ROWS[k_on][0]) > 1e-9: bad.append((round(t, 2), "r hien khi chua dung"))
        if k_on >= 0 and round(r_of(ang)) != ROWS[k_on][1]: bad.append((round(t, 2), "r lech tia"))
        if rows > 0:
            done = max(k for k in range(5) if t >= T0 + DT * k)
            if rows > done + 1: bad.append((round(t, 2), "hang som"))
        t += 0.05
    if do_state(10.5)[2] != 5: bad.append("chua du 5 hang")
    return bad


# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def fan(d, ka=1.0):
    disk(d)
    for i, r, _ in ROWS:
        a, b = P(u_in(i), RD), P(u_out(r_of(i)), RD)
        d.line([a, C], fill=A(GRAY, 0.9 * ka), width=4)
        d.line([C, b], fill=A(BEAM, ka), width=5)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    fan(d)
    pill(d, "ĐÁP ÁN: r tăng, về sau thêm ít dần", 300, appear(t, 0.15, 0.4), size=40)
    table(d, 5, plus=appear(t, 0.6, 0.45), ratio=appear(t, M[1] + 0.3, 0.5))
    k = appear(t, M[1] + 1.6, 0.5)
    if k > 0:
        card(d, (110, 1530, 970, 1600), fill=A((236, 253, 243), k), outline=A(GREEN, k), r=22, w=3)
        text(d, (W / 2, 1565), "sin i / sin r gần như không đổi", 44, DGREEN, alpha=k)


# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    fan(d)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    y = 1040
    if a1 > 0:
        card(d, (40, y, 1040, y + 470), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        text(d, (W / 2, y + 150), "“Chia góc i cho góc r”", 48, INK, alpha=a1)
        text(d, (W / 2, y + 235), "20 : 13 ≈ 1,54    80 : 41 ≈ 1,95", 46, DRED, alpha=a1 * appear(t, 0.9, 0.4))
        text(d, (900, y + 150), "✗", 64, DRED, alpha=a1 * appear(t, 1.6, 0.4))
        kk = a1 * appear(t, 2.6, 0.4)
        text(d, (W / 2, y + 330), "✓ Chia sin i cho sin r:", 46, DGREEN, alpha=kk)
        text(d, (W / 2, y + 400), "tỉ số gần như đứng yên", 46, DGREEN, alpha=kk)
    if k3 > 0:
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 170), "Số liệu minh hoạ,", 46, INK, alpha=kk)
        text(d, (W / 2, y + 235), "chưa phải số đo thật", 46, INK, alpha=kk)


# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Vào nhựa: r luôn nhỏ hơn i,", 50, DGREEN, alpha=k0)
    text(d, (W / 2, 450), "i càng lớn, r tăng càng chậm", 50, DGREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1290), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Cùng khối nhựa, đọc được", f"r = {CHOT_R}°. Góc tới i khoảng bao nhiêu?")):
        text(d, (W / 2, 800 + j * 78), s, 46, INK, alpha=kq)
    kh = appear(t, M[0] + 3.2, 0.5)
    if kh > 0:
        card(d, (90, 1030, 990, 1260), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1080), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1180), "Chiết suất của nhựa: 1,5", 46, (176, 64, 8), alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + T0 + DT * k + READ, "tap") for k in range(5)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.6, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-khucxa-02", header="KHTN 9 · THÍ NGHIỆM", footer="Khúc xạ ánh sáng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Khối nhựa bán trụ", draw=s_hook, tail=0.3, caps=[
   ("Laser chiếu vào đúng tâm khối nhựa.", 3.6),
   ("Tự trả lời trước khi xem.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Xoay laser quanh tâm đĩa.", 4.6),
   ("Đọc góc r trên vạch chia.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Các tia khúc xạ sát nhau dần.", 4.0),
   ("Thử chia sin i cho sin r.", 4.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 5.2),
   ("Câu còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 7.6)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
