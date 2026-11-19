# Clip: tn-l9-langkinh-01 - Duong di cua tia laser do qua lang kinh, doi goc toi (KHTN 9, lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-langkinh-01.json (_kiem_so()):
#   tham_so A = 60 do, n = 1,5 ; so_lieu_mau (i, D): 30 47,1 | 40 38,5 | 45 37,4 | 50 37,2 | 60 38,9 | 70 42,9.
#   D = i + i2 - A "dung cho mo phong, khong day o lop 9" -> clip KHONG viet cong thuc D, chi "do bang thuoc do goc".
# Du doan (K10, khong nut A-D): tang dan i tu 30 toi 70 do, tia lo lech ve phia nao so voi huong tia toi?
#   (ve day / ve canh (dinh) / khong lech / tuy goc toi) -> dap an: ve day, ca 6 lan.
#   KHONG hoi D giam roi tang (can goc lech cuc tieu, ngoai KHTN 9): bang chi giu cot D, khong nhan "nho nhat".
#   Khong trung cau Tu kiem tra: C1 (mat thu hai: xa phap tuyen) -> clip KHONG noi tia lo gan/xa phap tuyen;
#   C4 (lang kinh dat nguoc, laser nam ngang -> len/xuong) -> THU NGHI dung lang kinh xoay day sang phai, laser chieu
#   tu tren xuong; C5 (thu tu mau) ; C6 (A = 20 do).
# Hinh: lang kinh deu dinh tren, day duoi; diem toi E co dinh tren mat trai, xoay but laser. Duong tia tinh bang Snell
#   (sin i = n sin r1 ; r2 = A - r1 ; sin i2 = n sin r2) va do D tu chinh hai huong ve -> assert khop kho (< 0,06 do),
#   tia lo ra o mat phai (khong cham day), lech ve phia day (quay xuoi chieu kim dong ho = xuong).
# Bay = hien_tuong_hay_sai[1] (ve tia di thang). KHONG dung [0] (lech ve dinh, gan Cau 4) va [2] (= dap an Cau 1).
# Chua noi duoc = ghi_chu kho (so lieu minh hoa, n gia dinh).
# THU NGHI: xoay lang kinh cho day quay sang phai, chieu laser tu tren xuong -> tia lo lech sang phai (ve phia day).
from engine import *

AXD, N = 60.0, 1.5
ROWS = [(30, "47,1"), (40, "38,5"), (45, "37,4"), (50, "37,2"), (60, "38,9"), (70, "42,9")]
GLASS = (191, 219, 254); BEAM = (220, 38, 38); DRED = (185, 28, 28); DGREEN = (10, 110, 50)

P = (470.0, 330.0); SIDE = 440.0
BL = (P[0] - SIDE / 2, P[1] + SIDE * math.sqrt(3) / 2); BR = (P[0] + SIDE / 2, BL[1])
E = (lerp(BL[0], P[0], 0.55), lerp(BL[1], P[1], 0.55))
LOUT = 340


def u(deg): return (math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def path(i):
    """-> (huong tia toi (do, y xuong), diem ra X, huong tia lo (do), D do tu hai huong)."""
    th_in = 30.0 - i                                          # phap tuyen vao trong mat trai: +30 do
    r1 = math.degrees(math.asin(math.sin(math.radians(i)) / N))
    th = 30.0 - r1; v = u(th)
    wx, wy = BR[0] - P[0], BR[1] - P[1]
    det = v[0] * (-wy) - v[1] * (-wx)
    s = ((P[0] - E[0]) * (-wy) - (P[1] - E[1]) * (-wx)) / det
    tt = (v[0] * (P[1] - E[1]) - v[1] * (P[0] - E[0])) / det   # vi tri tren mat phai (0 = dinh, 1 = goc day)
    X = (E[0] + s * v[0], E[1] + s * v[1])
    i2 = math.degrees(math.asin(N * math.sin(math.radians(AXD - r1))))
    th_out = -30.0 + i2                                       # phap tuyen ra ngoai mat phai: -30 do
    return th_in, X, th_out, th_out - th_in, tt


def num(x): return f"{x:.1f}".replace(".", ",")


def _kiem():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-langkinh-01.json")))
    tp = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert tp["A"]["gia_tri"] == AXD and tp["n"]["gia_tri"] == N
    hang = k["so_lieu_mau"]["hang"]; assert len(hang) == len(ROWS)
    for (i, ds), h in zip(ROWS, hang):
        th_in, X, th_out, D, tt = path(i)
        assert h[0] == i and num(h[1]) == ds, (i, ds, h)
        assert abs(D - h[1]) < 0.06, (i, D, h[1])              # goc lech do tu hinh ve khop kho
        assert D > 0                                          # quay xuoi chieu kim dong ho (y xuong) = lech ve day
        assert 0.05 < tt < 0.95, (i, tt)                      # tia ra o mat ben phai, khong cham day
        r1 = math.degrees(math.asin(math.sin(math.radians(i)) / N))
        assert r1 < i                                         # vao thuy tinh: gan phap tuyen
    assert "đáy quay sang phải" in k["so_lieu_mau"]["ghi_chu"]
_kiem()


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


def prism(d):
    d.polygon([P, BR, BL], fill=A(GLASS, 0.85), outline=BLUE)
    d.line([P, BR, BL, P], fill=BLUE, width=4)
    text(d, (P[0], P[1] - 40), "A = 60°", 42, BLUE)
    text(d, ((BL[0] + BR[0]) / 2, BL[1] + 42), "đáy", 40, BLUE)


def pen(d, i):
    v = u(30.0 - i); a, b = (E[0] - 120 * v[0], E[1] - 120 * v[1]), (E[0] - 230 * v[0], E[1] - 230 * v[1])
    d.line([a, b], fill=(55, 60, 75), width=30); dot(d, a[0], a[1], 9, BEAM)
    return a


def normal_E(d, i=None):
    nrm = (-math.sqrt(3) / 2, -0.5)
    dash(d, (E[0] + 120 * nrm[0], E[1] + 120 * nrm[1]), (E[0] - 90 * nrm[0], E[1] - 90 * nrm[1]), A(NAVY, 0.7), w=3)
    if i is not None:
        d.arc([E[0] - 75, E[1] - 75, E[0] + 75, E[1] + 75], 210 - i, 210, fill=NAVY, width=4)


def ray(d, i, col=BEAM, ka=1.0, arc=True, lab="D"):
    th_in, X, th_out, D, _ = path(i)
    a = pen(d, i); vo = u(th_out); Z = (X[0] + LOUT * vo[0], X[1] + LOUT * vo[1])
    d.line([a, E], fill=A(col, ka), width=6); chev(d, a, E, A(col, ka))
    d.line([E, X], fill=A(col, ka), width=5)
    d.line([X, Z], fill=A(col, ka), width=6); chev(d, X, Z, A(col, ka))
    if arc:
        vi = u(th_in); dash(d, X, (X[0] + LOUT * vi[0], X[1] + LOUT * vi[1]), A(NAVY, 0.75 * ka), w=3)
        d.arc([X[0] - 150, X[1] - 150, X[0] + 150, X[1] + 150], th_in, th_out, fill=A(ORANGE, ka), width=5)
        if lab:
            m = math.radians((th_in + th_out) / 2)
            text(d, (X[0] + 190 * math.cos(m), X[1] + 190 * math.sin(m)), lab, 44, ORANGE, alpha=ka)
    return X


def readout(d, i, ds):
    card(d, (90, 880, 500, 950), fill=WHITE, outline=NAVY, r=22, w=3)
    text(d, (295, 915), f"i = {i}°", 44, NAVY)
    card(d, (560, 880, 990, 950), fill=WHITE, outline=ORANGE, r=22, w=3)
    text(d, (775, 915), f"D = {ds}°" if ds else "D = …", 44, (176, 64, 8) if ds else MUTED, bold=bool(ds))


XS = (300, 640)
def table(d, n, y0=990):
    card(d, (60, y0, 1020, y0 + 92 + 6 * 60 + 18), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y0 + 48), "i", 44, NAVY); text(d, (XS[1], y0 + 48), "D (thước đo góc)", 42, (176, 64, 8))
    d.line([(90, y0 + 88), (990, y0 + 88)], fill=LIGHT, width=3)
    for j in range(n):
        i, ds = ROWS[j]; yy = y0 + 122 + 60 * j
        text(d, (XS[0], yy), f"{i}°", 44, INK); text(d, (XS[1], yy), f"{ds}°", 44, INK)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    prism(d); normal_E(d, 30); ray(d, 30, ka=appear(t, 0.5, 0.5))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Tăng dần góc tới i từ 30° tới 70°.", "Tia ló lệch về phía nào", "so với hướng tia tới?")):
        text(d, (W / 2, y0 + 160 + j * 76), s, 48, INK, alpha=a)
    text(d, (W / 2, y0 + 420), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 485, 940, y0 + 499], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 485, 140 + 800 * (1 - p), y0 + 499], radius=7, fill=A(PURPLE, a))


# ---------------- canh 2: Tien hanh ----------------
T0, DT, ROT, READ, ROW = 0.6, 1.5, 0.5, 0.9, 0.9
def do_state(t):
    rows, ang, k_on = 0, ROWS[0][0], -1
    for k, (i, _) in enumerate(ROWS):
        tk = T0 + DT * k
        if t < tk: break
        if k > 0 and t < tk + ROT:
            ang = lerp(ROWS[k - 1][0], i, ease((t - tk) / ROT)); k_on = -1
        else:
            ang = i; k_on = k if t >= tk + READ else -1
        if t >= tk + ROW: rows = k + 1
    return ang, k_on, rows


def card_state(ang, k_on, rows):
    """(i hien, D hien hoac None). Laser con dung o goc hang vua ghi -> giu so cua hang do (khop bang)."""
    if k_on >= 0: return ROWS[k_on][0], ROWS[k_on][1]
    if rows > 0 and abs(ang - ROWS[rows - 1][0]) < 0.5: return ROWS[rows - 1][0], ROWS[rows - 1][1]
    return round(ang), None


def s_do(img, d, t, sc):
    ang, k_on, rows = do_state(t)
    prism(d); normal_E(d)
    ray(d, ang, arc=k_on >= 0, lab=None)
    readout(d, *card_state(ang, k_on, rows))
    table(d, rows)


def _kiem_dong_bo():
    """Moi 0,05 s: so D chi hien khi laser dung yen o goc cua hang do va khop goc ve; hang bang hien sau khi doc."""
    bad = []; t = 0.0
    while t < 11.0:
        ang, k_on, rows = do_state(t)
        if k_on >= 0:
            if abs(ang - ROWS[k_on][0]) > 1e-9: bad.append((round(t, 2), "D hien khi chua dung"))
            if num(path(ang)[3]) != ROWS[k_on][1]: bad.append((round(t, 2), "D lech hinh"))
        ci, cd = card_state(ang, k_on, rows)
        if cd is not None and (ci, cd) not in ROWS[:rows]: bad.append((round(t, 2), "the D co so ma bang chua ghi"))
        if cd is None and any(r[0] == ci for r in ROWS[:rows]): bad.append((round(t, 2), "the D = … o goc da ghi"))
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
    prism(d); normal_E(d)
    k2 = appear(t, M[1] + 0.2, 0.5)
    if k2 > 0:                                                  # ca 6 tia lo (mo) cung nga ve phia day
        for i, _ in ROWS:
            th_in, X, th_out, D, _ = path(i); vo = u(th_out)
            d.line([X, (X[0] + LOUT * vo[0], X[1] + LOUT * vo[1])], fill=A(BEAM, 0.35 * k2), width=3)
    ray(d, 50)
    pill(d, "ĐÁP ÁN: lệch về phía đáy", 870, appear(t, 0.15, 0.4))
    table(d, 6)
    if k2 > 0:
        card(d, (90, 1560, 990, 1730), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=22, w=3)
        text(d, (W / 2, 1610), "Cả 6 lần: ngả về phía đáy", 44, DGREEN, alpha=k2)
        text(d, (W / 2, 1685), "Đáy ở đâu thì tia lệch về đó", 44, DGREEN, alpha=k2)


# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    prism(d); normal_E(d)
    kx = a1 * appear(t, 0.9, 0.4); kv = appear(t, 2.6, 0.4)
    ray(d, 50, col=DGREEN if kv > 0.5 else BEAM, arc=kv > 0.5, lab=None)
    if kx > 0:                                                  # duong "di thang" (sai): keo dai tia toi
        vi = u(path(50)[0]); Q = (E[0] + 560 * vi[0], E[1] + 560 * vi[1])
        dash(d, E, Q, A(DRED, kx), w=5, on=18, off=12)
        text(d, (Q[0] - 10, Q[1] - 50), "đi thẳng?", 40, DRED, alpha=kx)
    y = 1000
    if a1 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        text(d, (W / 2, y + 160), "“Tia đi thẳng qua lăng kính”", 46, INK, alpha=a1)
        text(d, (W / 2, y + 240), "✗", 64, DRED, alpha=a1 * appear(t, 1.6, 0.4))
        text(d, (W / 2, y + 330), "✓ Gãy ở cả hai mặt bên, lệch 37,2°", 44, DGREEN, alpha=a1 * kv)
    if k3 > 0:
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 170), "Số liệu minh hoạ,", 46, INK, alpha=kk)
        text(d, (W / 2, y + 235), "n = 1,5 chỉ là giả định", 46, INK, alpha=kk)


# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Tia đơn sắc qua lăng kính:", 50, DGREEN, alpha=k0)
    text(d, (W / 2, 450), "khúc xạ hai lần, lệch về đáy", 50, DGREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1290), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Đáy quay sang phải, laser chiếu xuống.", "Tia ló lệch trái hay phải?")):
        text(d, (W / 2, 800 + j * 78), s, 46, INK, alpha=kq)
    kh = appear(t, M[0] + 3.2, 0.5)
    if kh > 0:
        card(d, (90, 1030, 990, 1260), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1145), "Gợi ý: vẽ ra, tô đậm cạnh đáy", 44, (176, 64, 8), alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + T0 + DT * k + READ, "tap") for k in range(6)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.6, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-langkinh-01", header="KHTN 9 · THÍ NGHIỆM", footer="Lăng kính · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tia laser đỏ qua lăng kính", draw=s_hook, tail=0.3, caps=[
   ("Góc lệch D: giữa tia tới, tia ló.", 3.6),
   ("Tự trả lời trước khi xem.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Xoay bút laser, giữ điểm tới.", 4.6),
   ("Đo D bằng thước đo góc.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So sáu tia ló với tia tới.", 4.0),
   ("Mỗi lần đều khúc xạ hai lần.", 4.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 5.2),
   ("Câu còn bỏ ngỏ.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 8.2)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
