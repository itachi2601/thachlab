"""Bài tập mẫu Bài 7. Lăng kính (KHTN 9) — lesson_id 85. Dạng: 85.dang.md. Chuẩn "một dạng — một hình" (cong_cu tia_sang canh tu_do, de:true).
Hình tính thật bằng python (dò tia qua lăng kính); số n VẼ lệch số liệu đề để không đo thước ra đáp số (tính chất định tính giữ nguyên).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-85.py   (idempotent; không ghi DB)"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import write, inject, sol, M, P, A, buoc

J = os.path.join(HERE, "85.json")
rad, deg = math.radians, math.degrees


def asn(x):
    return deg(math.asin(x))


def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")


def sn(x):
    return math.sin(rad(x))


# ───────────── kiểm số: mọi con số viết tay trong lời giải phải khớp phép tính ─────────────
def kiem_so():
    # dạng 1: A = 25°, n = 1,52, tia ⊥ AB
    x = 1.52 * sn(25)
    r1 = asn(x)
    assert vn(x, 3) == "0,642" and vn(r1) == "40,0" and vn(r1 - 25) == "15,0"
    assert vn(sn(40.0), 3) == "0,643" and vn(sn(25), 3) == "0,423" and vn(sn(40.0) / sn(25), 2) == "1,52"
    assert asn(1 / 1.52) > 25  # tia ló ra được
    assert abs(90 - 25 - 25) > 1  # lựa chọn sai 90° − A khác đáp số

    # dạng 2: n = 1,60 ; A = 35° rồi 40°
    igh = asn(1 / 1.6)
    assert vn(1 / 1.6, 3) == "0,625" and vn(igh) == "38,7"
    assert 35 < igh < 40  # A = 35 ló, A = 40 phản xạ toàn phần
    assert 90 - 35 > igh  # lựa chọn sai "góc tới = 90° − A" cho kết luận ngược (không ló)
    x2 = 1.6 * sn(35)
    r2 = asn(x2)
    assert vn(x2, 3) == "0,918" and vn(r2) == "66,6" and vn(r2 - 35) == "31,6"
    assert vn(1.6 * sn(40), 2) == "1,03" and 1.6 * sn(40) > 1
    assert abs(asn(sn(35) / 1.6) - r2) > 5  # bẫy chia n

    # dạng 4: A = 32°, n_đ = 1,620, n_t = 1,660, L = 1,50 m
    nd, nt, A4, L = 1.620, 1.660, 32, 1.50
    igt, igd = asn(1 / nt), asn(1 / nd)
    assert vn(igt) == "37,0" and A4 < igt < igd  # cả hai ló
    xd, xt = nd * sn(A4), nt * sn(A4)
    rd, rt = asn(xd), asn(xt)
    assert vn(xd, 4) == "0,8585" and vn(xt, 4) == "0,8797"
    assert vn(rd, 2) == "59,15" and vn(rt, 2) == "61,60"
    Dd, Dt = rd - A4, rt - A4
    assert vn(Dd, 2) == "27,15" and vn(Dt, 2) == "29,60" and vn(Dt - Dd, 2) == "2,46"
    assert vn(math.tan(rad(27.15)), 4) == "0,5128" and vn(math.tan(rad(29.60)), 4) == "0,5681"
    ell = L * (math.tan(rad(Dt)) - math.tan(rad(Dd)))
    assert vn(ell * 100, 1) == "8,3" and vn(1.5 * (0.5681 - 0.5128), 3) == "0,083"
    # cách sai cho số khác đáp án
    assert abs(L * math.tan(rad(Dt - Dd)) * 100 - 8.3) > 1.5  # ≈ 6,4 cm
    assert abs(L * (sn(Dt) - sn(Dd)) * 100 - 8.3) > 1.5  # ≈ 5,7 cm
    assert abs(Dd * nt / nd - Dt) > 1  # bẫy tỉ lệ chiết suất

    # dạng 5: năm LED, A = 41,5° ; khoảng A để chỉ đỏ ló
    NS = {"đỏ": 1.48, "vàng": 1.50, "lục": 1.52, "lam": 1.55, "tím": 1.58}
    nmax = 1 / sn(41.5)
    assert vn(nmax, 3) == "1,509" and vn(sn(41.5), 4) == "0,6626"
    lo = [k for k, n in NS.items() if n * sn(41.5) < 1]
    assert lo == ["đỏ", "vàng"], lo
    assert vn(1 / 1.5, 1) == "0,7" and round(nmax, 1) == 1.5  # bẫy làm tròn sớm → tưởng vàng không ló
    gh = {k: asn(1 / n) for k, n in NS.items()}
    assert vn(gh["vàng"], 2) == "41,81" and vn(gh["đỏ"], 2) == "42,51" and vn(gh["tím"]) == "39,3"
    # dò cả khoảng: tập A (bước 0,01°) để CHỈ đỏ ló, đúng một khoảng [i_gh vàng ; i_gh đỏ)
    ok = [a / 100 for a in range(3000, 6000) if [k for k, n in NS.items() if n * sn(a / 100) < 1] == ["đỏ"]]
    assert abs(ok[0] - gh["vàng"]) < 0.011 and abs(ok[-1] - gh["đỏ"]) < 0.011
    assert all(abs((ok[i + 1] - ok[i]) - 0.01) < 1e-9 for i in range(len(ok) - 1))  # liền một khoảng
    assert vn(1.48 * sn(42), 3) == "0,990" and vn(1.50 * sn(42), 3) == "1,004"
    return dict(r1=r1, r2=r2, igh=igh, Dd=Dd, Dt=Dt, ell=ell, gh=gh)


V = kiem_so()


# ───────────── helper hình (toạ độ x 0..20, y xuống; góc = độ toán học) ─────────────
class Fl:
    """Phản chiếu qua y = Y0/2 khi flip (lăng kính đặt ngược): y' = Y0 − y, góc → −góc."""

    def __init__(s, flip=False, Y0=0.0):
        s.f, s.Y0 = flip, Y0

    def p(s, x, y):
        return [round(x, 2), round(s.Y0 - y if s.f else y, 2)]

    def a(s, t):
        return -t if s.f else t

    def vi(s, v):
        return {"t": "b", "b": "t"}.get(v, v) if s.f else v


def vung(H, pts, **kw):
    d = {"loai": "vung", "diem": [H.p(*q) for q in pts], "dam": 0.22, "vien": True}
    d.update(kw)
    return d


def diem(H, q, ten, vi, mau=None):
    d = {"loai": "diem", "tai": H.p(*q), "vi": H.vi(vi), "ten": ten}
    if mau:
        d["mau"] = mau
    return d


def tia(H, qs, mau=None, dut=False, mui=None, het=None):
    d = {"loai": "tia", "qua": [H.p(*q) for q in qs]}
    if mau:
        d["mau"] = mau
    if dut:
        d["dut"] = True
    if mui is False:
        d["mui"] = False
    if het:
        d["het"] = het
    return d


def pn(H, q, huong, dai=2.4):
    return {"loai": "phap_tuyen", "tai": H.p(*q), "huong": round(H.a(huong), 2), "dai": dai}


def goc(H, q, tu, den, nhan, r=1.5, rn=1.0):
    return {"loai": "goc", "tai": H.p(*q), "tu": round(H.a(tu), 2), "den": round(H.a(den), 2), "nhan": nhan, "r": r, "r_nhan": rn}


def chu(x, y, text, a="start", mau=None, het=None):
    d = {"loai": "chu", "x": round(x, 2), "y": round(y, 2), "text": text, "a": a}
    if mau:
        d["mau"] = mau
    if het:
        d["het"] = het
    return d


def ghi(text):
    return {"loai": "ghi", "text": text}


def doan(H, tu, den, kieu="vat", nhan=None):
    d = {"loai": "doan", "tu": H.p(*tu), "den": H.p(*den), "kieu": kieu}
    if nhan:
        d["nhan"] = nhan
    return d


def thuoc(tu, den, nhan, lech):
    return {"loai": "thuoc", "tu": [round(tu[0], 2), round(tu[1], 2)], "den": [round(den[0], 2), round(den[1], 2)], "nhan": nhan, "lech": lech}


def tron(q, r, mau=None, dam=0.9, het=None):
    d = {"loai": "tron", "tam": [round(q[0], 2), round(q[1], 2)], "r": r, "dam": dam}
    if mau:
        d["mau"] = mau
    if het:
        d["het"] = het
    return d


# lăng kính vuông tại B: đỉnh A (xa, ya), AB thẳng đứng dài h, góc chiết quang Ad
def geo(xa, ya, h, Ad):
    t = math.tan(rad(Ad))
    return dict(A=(xa, ya), B=(xa, ya + h), C=(xa + h * t, ya + h), t=t, yb=ya + h)


def Ept(g, yk):  # điểm tới trên AC của tia ngang vào AB ở độ cao yk
    return (g["A"][0] + (yk - g["A"][1]) * g["t"], yk)


def far(E, theta, X):  # điểm của tia xuất phát từ E, hướng theta (độ toán học), tại hoành độ X
    return (X, E[1] - (X - E[0]) * math.tan(rad(theta)))


def lk_items(H, g, vA="t"):
    return [vung(H, [g["A"], g["B"], g["C"]]), diem(H, g["A"], "A", vA), diem(H, g["B"], "B", "b"), diem(H, g["C"], "C", "r")]


def lech(n, Ad):  # hướng tia ló (độ toán học, y lên) khi tia ⊥ AB, đáy ở dưới: θ = A − r
    return Ad - asn(n * math.sin(rad(Ad)))


# ═════════════ DẠNG 1 · lăng kính đặt ngược ═════════════
def cc1():
    Ad, nd = 25, 1.58  # n VẼ 1,58 (đề 1,52)
    H = Fl(True, 12.0)
    g = geo(6.5, 1.4, 7.2, Ad)
    yk = 6.0
    K, E = (g["A"][0], yk), Ept(g, yk)
    th = lech(nd, Ad)
    end = far(E, th, 19.4)
    hinh = lk_items(H, g, "t") + [
        chu(0.3, 1.2, "A = 25°"), chu(0.3, 2.7, "n = 1,52"), chu(8.4, 1.5, "đáy BC", "middle"),
        tia(H, [(0.3, yk), K], mau="max"), chu(0.3, 7.4, "laser đỏ", mau="max"),
    ]
    lop = [
        [tia(H, [K, E], mau="max"), pn(H, E, Ad), goc(H, E, 180, 180 + Ad, "i", 1.5, 1.0), ghi("i = A = 25°")],
        [tia(H, [E, end], mau="max"), goc(H, E, Ad, th, "r", 1.5, 1.0), ghi("sin r = 1,52·sin 25° ⇒ r ≈ 40,0°")],
        [tia(H, [E, far(E, 0, 19.4)], dut=True, mui=False), goc(H, E, 0, th, "D", 2.7, 1.0), ghi("D = r − i ≈ 15,0°")],
        [ghi("lệch về phía đáy BC: lên trên")],
        [ghi("sin 40,0° / sin 25° ≈ 1,52 = n")],
    ]
    return {"loai": "tia_sang", "canh": "tu_do", "cao": 12.2, "de": True, "hinh": hinh, "lop": lop}


# ═════════════ DẠNG 2 · ló ra hay phản xạ toàn phần ═════════════
def cc2():
    nd = 1.58  # n VẼ (đề 1,60)
    H = Fl(False)
    yk = 5.2
    xa, ya, h = 7.0, 2.2, 8.4
    K = (xa, yk)

    def nen(Ad):
        g = geo(xa, ya, h, Ad)
        return g, lk_items(H, g, "t") + [chu(0.3, 1.2, f"A = {Ad}°"), chu(0.3, 2.7, "n = 1,60"), tia(H, [(0.3, yk), K], mau="max"), chu(0.3, 4.5, "tia sáng")]

    g35, hinh35 = nen(35)
    g40, hinh40 = nen(40)
    E35, E40 = Ept(g35, yk), Ept(g40, yk)
    th = lech(nd, 35)
    end35 = far(E35, th, 19.4)
    # tia phản xạ toàn phần ở AC (A = 40°): hướng (−cos2A, sin2A) theo y xuống → đi xuống đáy BC
    d = (-math.cos(rad(80)), math.sin(rad(80)))
    tt = (g40["yb"] - yk) / d[1]
    refl = (E40[0] + tt * d[0], g40["yb"])
    assert refl[0] > xa + 0.5
    lop = [
        [ghi("sin i_{th} = 1/n ⇒ i_{th} ≈ 38,7°")],
        [tia(H, [K, E35], mau="max"), pn(H, E35, 35), goc(H, E35, 180, 215, "i", 1.5, 1.0), ghi("i = 35° < i_{th}: tia ló ra")],
        [tia(H, [E35, end35], mau="max"), goc(H, E35, 35, th, "r", 1.5, 1.0), ghi("sin r = 1,60·sin 35° ⇒ r ≈ 66,6°")],
        [tia(H, [E35, far(E35, 0, 19.4)], dut=True, mui=False), goc(H, E35, 0, th, "D", 2.7, 1.0), ghi("D = r − A ≈ 31,6°")],
        [tia(H, [K, E40], mau="max"), pn(H, E40, 40), goc(H, E40, 180, 220, "i", 1.5, 1.0), tia(H, [E40, refl], mau="max"),
         ghi("góc tới quá lớn: phản xạ toàn phần")],
    ]
    return {"loai": "tia_sang", "canh": "tu_do", "cao": 12.2, "de": True,
            "phan": [{"tu_buoc": 0, "hinh": hinh35}, {"tu_buoc": 4, "hinh": hinh40}], "lop": lop}


# ═════════════ DẠNG 3 · đọc thứ tự vệt màu → vị trí đáy ═════════════
def cc3():
    H = Fl(False)
    yb = 4.6  # độ cao chùm tới
    X0, X1, Y0, Y1 = 6.2, 11.0, 1.6, 7.8  # tấm bìa
    SX0, SX1, SY0, SY1 = 14.0, 18.6, 1.0, 8.8  # màn nhìn từ phía trước
    xs = (SX0 + SX1) / 2 - 0.6
    yt, yl, yv, yd = 2.4, 4.4, 5.8, 7.2  # tím, lục, vàng, đỏ (đáy ở trên → tím trên cùng)
    hinh = [
        tron((1.2, yb), 0.6, mau="vang", dam=0.8), chu(0.3, yb - 1.1, "đèn 3 màu"),
        tia(H, [(1.9, yb), (X0, yb)]),
        vung(H, [(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)], dam=0.55),
        chu((X0 + X1) / 2, (Y0 + Y1) / 2 + 0.4, "?", "middle", het=2),
        chu((X0 + X1) / 2, Y1 + 1.3, "tấm bìa", "middle"),
        vung(H, [(SX0, SY0), (SX1, SY0), (SX1, SY1), (SX0, SY1)], dam=0.04),
        chu((SX0 + SX1) / 2, SY1 + 1.3, "màn", "middle"),
        chu(SX0 - 0.3, SY0 + 0.6, "trên", "end"), chu(SX0 - 0.3, SY1 - 0.2, "dưới", "end"),
        tron((xs, yt), 0.42, mau="min", het=4), chu(xs + 0.8, yt + 0.35, "tím", mau="min", het=4),
        tron((xs, yl), 0.42, mau="chu", het=4), chu(xs + 0.8, yl + 0.35, "lục", het=4),
        tron((xs, yd), 0.42, mau="max", het=4), chu(xs + 0.8, yd + 0.35, "đỏ", mau="max", het=4),
    ]
    # lăng kính hiện ra sau bước 2: cạnh ở dưới, đáy ở trên
    xm = (X0 + X1) / 2
    tri = [(X0 + 0.6, Y0 + 0.6), (X1 - 0.6, Y0 + 0.6), (xm, Y1 - 0.5)]
    lop = [
        [ghi("tím: chiết suất lớn nhất, lệch nhiều nhất")],
        [doan(H, tri[0], tri[1], "mat"), doan(H, tri[1], tri[2], "mat"), doan(H, tri[2], tri[0], "mat"),
         chu(xm, Y0 + 1.6, "đáy", "middle"), ghi("tím gần đáy nhất: đáy ở trên")],
        [tron((xs, yv), 0.42, mau="vang", het=4), chu(xs + 0.8, yv + 0.35, "vàng", het=4),
         ghi("vàng: chiết suất giữa đỏ và lục")],
        [vung(H, [(3.6, yb - 1.3), (4.1, yb - 1.3), (4.1, yb + 1.3), (3.6, yb + 1.3)], mau="vang", dam=0.7),
         chu(3.85, yb + 2.4, "lọc vàng", "middle"),
         tron((xs, yv), 0.42, mau="vang"), chu(xs + 0.8, yv + 0.35, "vàng"),
         ghi("chỉ còn vệt vàng, đúng chỗ ở câu b")],
    ]
    return {"loai": "tia_sang", "canh": "tu_do", "cao": 10.8, "de": True, "hinh": hinh, "lop": lop}


# ═════════════ DẠNG 4 · hai vệt màu trên tường ═════════════
def cc4():
    ndv, ntv = 1.48, 1.64  # n VẼ (đề 1,620 / 1,660): phóng đại độ tán sắc, không đo thước ra đáp số
    Ad = 32
    H = Fl(False)
    g = geo(7.0, 1.8, 7.6, Ad)
    yk, XW = 5.8, 18.2
    K, E = (g["A"][0], yk), Ept(g, yk)
    thd, tht = lech(ndv, Ad), lech(ntv, Ad)
    pd, pt_ = far(E, thd, XW), far(E, tht, XW)
    assert pd[1] + 1.2 < pt_[1] < 12.6, (pd, pt_)
    assert far(E, tht, g["C"][0])[1] < g["yb"]  # tia ló nằm ngoài lăng kính
    hinh = lk_items(H, g, "t") + [
        chu(0.3, 1.2, "A = 32°"), chu(0.3, 8.6, "n_đ = 1,620", mau="max"), chu(0.3, 10.2, "n_t = 1,660", mau="min"),
        tia(H, [(0.3, yk), K]), chu(0.3, yk - 0.7, "chùm nắng"),
        diem(H, E, "I", "b"),
        doan(H, (XW, 2.4), (XW, 13.0)), chu(XW, 1.8, "tường", "middle"),
        tia(H, [E, (XW, yk)], dut=True, mui=False),
        thuoc((E[0], 3.6), (XW, 3.6), "1,50 m", 0),
        chu(0.3, 12.8, "hình không theo tỉ lệ"),
    ]
    lop = [
        [ghi("tím: i_{th,t} ≈ 37,0°")],
        [tia(H, [K, E]), pn(H, E, Ad), goc(H, E, 180, 180 + Ad, "i", 1.5, 1.0), ghi("i = 32° < i_{th,t}: cả hai ló")],
        [tia(H, [E, pd], mau="max"), goc(H, E, 0, thd, "D_đ", 2.4, 1.1), ghi("D_đ ≈ 27,15°")],
        [tia(H, [E, pt_], mau="min"), goc(H, E, 0, tht, "D_t", 4.6, 1.1), ghi("D_t ≈ 29,60°")],
        [ghi("Δ = D_t − D_đ ≈ 2,46°")],
        [diem(H, pd, "", "r", mau="max"), diem(H, pt_, "", "r", mau="min"),
         chu(XW + 0.4, pd[1] + 0.35, "đỏ", mau="max"), chu(XW + 0.4, pt_[1] + 0.35, "tím", mau="min"),
         thuoc((XW - 0.6, pd[1]), (XW - 0.6, pt_[1]), "ℓ", 0), ghi("ℓ ≈ 8,3 cm")],
    ]
    return {"loai": "tia_sang", "canh": "tu_do", "cao": 13.6, "de": True, "hinh": hinh, "lop": lop}


# ═════════════ DẠNG 5 · năm LED, chọn A để chỉ đỏ ló ═════════════
def cc5():
    NV = {"do": 1.30, "vang": 1.38}  # n VẼ của hai màu ló (đề 1,48 / 1,50): tách xa mặt AC cho dễ nhìn
    Ad = 41.5
    H = Fl(False)
    g = geo(6.0, 2.4, 7.0, Ad)
    yk, XE = 5.0, 16.8
    K, E = (g["A"][0], yk), Ept(g, yk)
    tips = {k: far(E, lech(n, Ad), XE) for k, n in NV.items()}
    d = (-math.cos(rad(2 * Ad)), math.sin(rad(2 * Ad)))
    tt = (g["yb"] - yk) / d[1]
    refl = (E[0] + tt * d[0], g["yb"])
    assert g["A"][0] + 0.5 < refl[0] < g["C"][0] and tips["do"][1] + 0.8 < tips["vang"][1]
    a_in = deg(math.atan2(-d[0], d[1]))  # góc với pháp tuyến đáy (thẳng đứng)
    a_out = asn(1.53 * math.sin(rad(a_in)))
    out = (refl[0] - 1.6 * math.tan(rad(a_out)), g["yb"] + 1.6)
    hinh = lk_items(H, g, "t") + [
        chu(0.3, 1.2, "A = 41,5°"), tia(H, [(0.3, yk), K]), chu(0.3, yk - 0.7, "5 màu"),
        chu(14.6, 1.0, "n: đỏ 1,48", mau="max"), chu(15.6, 2.2, "vàng 1,50"),
        chu(15.6, 3.4, "lục 1,52"), chu(15.6, 4.6, "lam 1,55"), chu(15.6, 5.8, "tím 1,58", mau="min"),
        chu(0.3, 12.9, "hình không theo tỉ lệ"),
    ]
    lop = [
        [tia(H, [K, E]), pn(H, E, Ad), goc(H, E, 180, 180 + Ad, "i", 1.5, 1.0), ghi("ló ra khi n < 1/sin 41,5° ≈ 1,509")],
        [tia(H, [E, tips["do"]], mau="max"), tia(H, [E, tips["vang"]], mau="vang"),
         chu(XE + 0.3, tips["do"][1] + 0.5, "đỏ", mau="max"), chu(XE + 0.3, tips["vang"][1] + 0.7, "vàng"),
         tia(H, [E, refl, out]), chu(out[0] + 0.6, out[1] + 0.1, "lục, lam, tím"),
         ghi("ló: đỏ, vàng · phản xạ: lục, lam, tím")],
        [ghi("A ≥ i_{th,vàng} ≈ 41,81°")],
        [ghi("A < i_{th,đỏ} ≈ 42,51°")],
        [ghi("A = 42°: đỏ ló, vàng phản xạ")],
    ]
    return {"loai": "tia_sang", "canh": "tu_do", "cao": 13.4, "de": True, "hinh": hinh, "lop": lop}


# ───────────────────────── nội dung chữ ─────────────────────────
DANG = [
    dict(label="Dạng 1 · Dễ · Tia vuông góc mặt bên: góc ló, góc lệch và chiều lệch",
         topic="Đường truyền tia sáng qua lăng kính",
         problem_html=r"""<p>Một lăng kính thuỷ tinh có tiết diện thẳng là tam giác $ABC$ vuông tại $B$, góc chiết quang $A=25^\circ$, chiết suất $n=1{,}52$, đặt trong không khí. Lăng kính được đặt sao cho mặt bên $AB$ thẳng đứng và đáy $BC$ nằm ở phía <strong>trên</strong>. Một tia laser đỏ hẹp nằm ngang chiếu vuông góc vào mặt $AB$. Dùng máy tính cầm tay.</p><ol type="a"><li>Tính góc tới của tia sáng ở mặt $AC$ và góc ló $r$ (góc giữa tia ló và pháp tuyến của $AC$).</li><li>Tính góc lệch $D$ giữa tia ló và phương tia tới. Tia ló lệch lên trên hay xuống dưới so với phương nằm ngang?</li></ol>"""),
    dict(label="Dạng 2 · Trung bình · Tia có ló ra không? So góc tới với góc tới hạn",
         topic="Đường truyền tia sáng qua lăng kính",
         problem_html=r"""<p>Một loại thuỷ tinh có chiết suất $n=1{,}60$ đối với một ánh sáng đơn sắc. Lăng kính làm bằng thuỷ tinh này có tiết diện thẳng là tam giác $ABC$ vuông tại $B$, đặt trong không khí. Chiếu tia sáng đơn sắc đó vuông góc vào mặt bên $AB$. Dùng máy tính cầm tay.</p><ol type="a"><li>Tính góc tới hạn $i_{th}$ khi ánh sáng đi từ thuỷ tinh này ra không khí.</li><li>Góc chiết quang $A=35^\circ$. Tia sáng có ló ra khỏi mặt $AC$ không? Nếu có, tính góc ló $r$ và góc lệch $D$.</li><li>Thay bằng lăng kính cùng loại thuỷ tinh, góc chiết quang $A=40^\circ$. Tia sáng có ló ra khỏi mặt $AC$ không?</li></ol>"""),
    dict(label="Dạng 3 · Trung bình · Đọc thứ tự vệt màu trên màn: đoán vị trí đáy lăng kính",
         topic="Tán sắc ánh sáng qua lăng kính",
         problem_html=r"""<p>Trong phòng tối, một chùm sáng hẹp gồm ba ánh sáng đơn sắc đỏ, lục, tím (trộn từ ba đèn LED) đi theo phương nằm ngang, chiếu vào một mặt bên của lăng kính thuỷ tinh. Lăng kính bị một tấm bìa che khuất; chỉ biết cạnh của nó nằm ngang, đáy hoặc quay lên trên, hoặc quay xuống dưới. Cả ba màu đều ló ra và rọi lên một màn thẳng đứng. Trên màn, ba vệt sáng xếp thành một cột: trên cùng là vệt tím, ở giữa là vệt lục, dưới cùng là vệt đỏ.</p><ol type="a"><li>Màu nào bị lăng kính làm lệch nhiều nhất? Đáy lăng kính quay lên trên hay xuống dưới?</li><li>Giữ nguyên lăng kính, thay chùm ba màu bằng một chùm sáng trắng hẹp đi đúng đường cũ. Trên màn, ánh sáng vàng nằm ở đâu so với chỗ ba vệt cũ?</li><li>Đặt thêm một kính lọc màu vàng chắn chùm sáng trắng ngay trước lăng kính. Trên màn còn thấy gì, ở đâu?</li></ol>"""),
    dict(label="Dạng 4 · Khá · Hai màu qua lăng kính: góc lệch từng màu và khoảng cách hai vệt",
         topic="Tán sắc ánh sáng qua lăng kính",
         problem_html=r"""<p>Một khối thuỷ tinh trang trí đặt trên bậu cửa sổ có tiết diện thẳng là tam giác $ABC$ vuông tại $B$, góc chiết quang $A=32^\circ$, đáy $BC$ nằm ngang ở phía dưới. Chiết suất của thuỷ tinh này (giả định) với ánh sáng đỏ là $n_{\text{đ}}=1{,}620$, với ánh sáng tím là $n_t=1{,}660$. Một chùm nắng hẹp nằm ngang chiếu vuông góc vào mặt $AB$. Coi các tia ló ra khỏi mặt $AC$ cùng xuất phát từ điểm $I$ trên $AC$. Một bức tường thẳng đứng, vuông góc với phương chùm tia tới, cách $I$ một đoạn $L=1{,}50\ \text{m}$ (đo theo phương tia tới). Dùng máy tính cầm tay.</p><ol type="a"><li>Tia đỏ và tia tím có cùng ló ra khỏi mặt $AC$ không? Tính góc lệch của mỗi tia và góc hợp bởi hai tia ló.</li><li>Tính khoảng cách $\ell$ giữa vệt đỏ và vệt tím trên tường (theo cm).</li></ol>"""),
    dict(label="Dạng 5 · Nâng cao · Chùm nhiều màu: màu nào ló ra, chọn góc chiết quang để chỉ một màu ló",
         topic="Tán sắc ánh sáng qua lăng kính",
         problem_html=r"""<p>Một đèn trang trí trộn ánh sáng của năm đèn LED đơn sắc đỏ, vàng, lục, lam, tím thành một chùm hẹp. Chùm này chiếu vuông góc vào mặt $AB$ của một lăng kính có tiết diện thẳng là tam giác $ABC$ vuông tại $B$, đặt trong không khí. Chiết suất của thuỷ tinh (giả định) với năm ánh sáng là: đỏ $1{,}48$; vàng $1{,}50$; lục $1{,}52$; lam $1{,}55$; tím $1{,}58$. Dùng máy tính cầm tay.</p><ol type="a"><li>Với góc chiết quang $A=41{,}5^\circ$, những ánh sáng nào ló ra khỏi mặt $AC$?</li><li>Người ta muốn chọn góc chiết quang $A$ sao cho chỉ ánh sáng đỏ ló ra khỏi mặt $AC$, bốn màu còn lại đều bị phản xạ toàn phần ở $AC$. Góc $A$ phải nằm trong khoảng nào?</li></ol>"""),
]
FORM = ["bai_tap", "bai_tap", "ly_thuyet", "bai_tap", "bai_tap"]  # chủ đề "Tán sắc…" chỉ có câu ly_thuyet; RPC bù khác Dạng

ANALYSIS = [
    [  # 1
        (r'"góc chiết quang $A=25^\circ$, chiết suất $n=1{,}52$"', r'$A=25^\circ$ ; $n=1{,}52$', 'Góc chiết quang là góc giữa hai mặt nào của lăng kính ?'),
        (r'"đáy $BC$ nằm ở phía <strong>trên</strong>"', 'lăng kính đặt ngược', 'Đáy nằm đối diện đỉnh nào ? Lăng kính bẻ tia về phía nào ?'),
        (r'"tia laser … chiếu vuông góc vào mặt $AB$"', r'tia tới $\perp AB$', r'⚠ Tia có gãy khúc ở $AB$ không ? Góc giữa tia trong thuỷ tinh và pháp tuyến của $AC$ bằng góc nào của hình ?'),
        (r'"góc ló $r$"', r'$r=\,?$', 'Ở mặt $AC$ tia đi từ môi trường nào sang môi trường nào ? Định luật khúc xạ viết cho chiều ấy thế nào ?'),
        (r'"góc lệch $D$ … lên trên hay xuống dưới"', r'$D=\,?$ ; chiều lệch', r'Góc lệch đo giữa hai tia nào ? $r$ đo so với đường nào ?'),
    ],
    [  # 2
        (r'"chiết suất $n=1{,}60$ … đặt trong không khí"', r'$n=1{,}60$ ; ngoài là không khí', 'Ở mặt $AC$, tia đi từ môi trường chiết quang hơn hay kém hơn ?'),
        (r'"góc tới hạn $i_{th}$"', r'$i_{th}=\,?$', 'Khi góc tới bằng góc tới hạn, góc khúc xạ bằng bao nhiêu ?'),
        (r'"chiếu … vuông góc vào mặt bên $AB$"', r'tia tới $\perp AB$', '⚠ Góc tới ở $AC$ bằng góc nào của lăng kính ?'),
        (r'"$A=35^\circ$ … có ló ra … góc ló $r$ và góc lệch $D$"', r'$A=35^\circ$ ; $r=\,?$ ; $D=\,?$', '⚠ Trước khi dùng định luật khúc xạ ở $AC$, cần so góc tới với đại lượng nào ?'),
        (r'"cùng loại thuỷ tinh, góc chiết quang $A=40^\circ$"', r'$A=40^\circ$ ; cùng $n$', 'Góc tới ở $AC$ đổi thế nào ? Góc tới hạn có đổi không ?'),
    ],
    [  # 3
        (r'"ba ánh sáng đơn sắc đỏ, lục, tím … đi theo phương nằm ngang"', 'ba màu, cùng đường tới', 'Cùng góc tới, ba màu khác nhau ở đại lượng nào của thuỷ tinh ?'),
        (r'"đáy hoặc quay lên trên, hoặc quay xuống dưới"', 'chưa biết vị trí đáy', '⚠ Lăng kính bẻ mọi tia về phía cạnh hay phía đáy ?'),
        (r'"trên cùng là vệt tím … dưới cùng là vệt đỏ"', 'từ trên xuống : tím, lục, đỏ', 'Màu nào có chiết suất lớn nhất ? Nó bị bẻ nhiều nhất về phía nào ?'),
        (r'"chùm sáng trắng hẹp đi đúng đường cũ"', 'ánh sáng trắng', 'Ánh sáng trắng gồm những màu nào ? Chiết suất của vàng đứng ở đâu trong dãy màu ?'),
        (r'"kính lọc màu vàng … ngay trước lăng kính"', 'lọc vàng', 'Ánh sáng nào qua được kính lọc ? Qua lăng kính nó còn bị lệch không ?'),
    ],
    [  # 4
        (r'"$A=32^\circ$ … chiếu vuông góc vào mặt $AB$"', r'$A=32^\circ$ ; tia tới $\perp AB$', '⚠ Góc tới ở $AC$ bằng bao nhiêu ? Có khác nhau giữa đỏ và tím không ?'),
        (r'"$n_{\text{đ}}=1{,}620$ … $n_t=1{,}660$"', r'$n_{\text{đ}}=1{,}620$ ; $n_t=1{,}660$', 'Màu nào có góc tới hạn nhỏ hơn, tức khó ló ra hơn ?'),
        (r'"có cùng ló ra khỏi mặt $AC$ không"', 'điều kiện ló', '⚠ So góc tới với góc tới hạn của màu nào thì đủ kết luận cho cả hai ?'),
        (r'"góc lệch của mỗi tia và góc hợp bởi hai tia ló"', r'$D_{\text{đ}}=\,?$ ; $D_t=\,?$ ; $\Delta=\,?$', 'Hai tia lệch về cùng một phía hay hai phía của phương tia tới ?'),
        (r'"cách $I$ một đoạn $L=1{,}50\ \text{m}$ (đo theo phương tia tới)"', r'$L=1{,}50\ \text{m}$', 'Trong tam giác vuông tạo bởi tia ló, phương tia tới và tường, $L$ là cạnh nào ?'),
        (r'"khoảng cách $\ell$ giữa vệt đỏ và vệt tím (theo cm)"', r'$\ell=\,?$ (cm)', 'Hai vệt nằm cùng phía so với đường kéo dài của tia tới không ? Đổi đơn vị lúc nào ?'),
    ],
    [  # 5
        (r'"chiếu vuông góc vào mặt $AB$"', r'tia tới $\perp AB$', '⚠ Góc tới ở $AC$ của năm màu có bằng nhau không, bằng góc nào ?'),
        (r'"đỏ $1{,}48$ ; … tím $1{,}58$"', 'năm chiết suất', 'Chiết suất càng lớn thì góc tới hạn lớn hay nhỏ ?'),
        (r'"$A=41{,}5^\circ$, những ánh sáng nào ló ra"', r'$A=41{,}5^\circ$', '⚠ Một màu ló ra khi góc tới thoả điều kiện gì so với góc tới hạn của chính màu đó ?'),
        (r'"chỉ ánh sáng đỏ ló ra"', 'đỏ : ló ra', 'Điều kiện để một màu ló ra viết thế nào theo $A$ ?'),
        (r'"bốn màu còn lại đều bị phản xạ toàn phần"', 'vàng, lục, lam, tím : phản xạ', '⚠ Muốn chặn cả nhóm màu, ta kiểm tra màu nào trong nhóm ?'),
    ],
]

# ───────────────────────── lời giải ─────────────────────────
S1 = sol(
    [r"<strong>Tia vuông góc mặt bên</strong> không bị gãy khúc ở mặt đó.",
     r"<strong>Khúc xạ ra không khí:</strong> $n\sin i=\sin r$ ($i$ trong thuỷ tinh, $r$ trong không khí).",
     r"<strong>Góc lệch</strong> $D$: góc giữa tia ló và phương tia tới ; lăng kính luôn bẻ tia về phía đáy."],
    [("Góc tới ở mặt $AC$", [P(r"Tia vuông góc $AB$ nên đi thẳng. Pháp tuyến của $AC$ vuông góc $AC$, tia vuông góc $AB$, nên góc giữa chúng bằng góc giữa $AB$ và $AC$ :"), A(r"i=A=25^\circ")]),
     ("Góc ló", [P("Tia đi từ thuỷ tinh ra không khí :"), M(r"\sin r=n\sin i"), M(r"\sin r=1{,}52\cdot\sin25^\circ\approx0{,}642"), A(r"r\approx40{,}0^\circ")]),
     ("Góc lệch", [P("Phần kéo dài của tia trong thuỷ tinh và tia ló cùng nằm một phía pháp tuyến tại điểm ló, nên góc giữa chúng là hiệu hai góc :"), M(r"D=r-i=40{,}0^\circ-25^\circ"), A(r"D\approx15{,}0^\circ")]),
     ("Chiều lệch", [P("Lăng kính bẻ tia về phía đáy. Đáy $BC$ nằm ở phía trên nên tia ló chếch lên so với phương nằm ngang."), A("T:Lệch <strong>lên trên</strong>, về phía đáy $BC$.")]),
     ("Kiểm tra", [P("Thay ngược vào định luật khúc xạ :"), M(r"\dfrac{\sin40{,}0^\circ}{\sin25^\circ}\approx\dfrac{0{,}643}{0{,}423}\approx1{,}52=n")])],
    [r"a) $i=25^\circ$ ; $r\approx40{,}0^\circ$", r"b) $D\approx15{,}0^\circ$ ; tia ló lệch <strong>lên trên</strong> (về phía đáy)"],
    "Nhận dạng: tia vuông góc một mặt bên thì góc tới ở mặt kia bằng $A$ ; chiều lệch luôn theo vị trí đáy, không theo trên – dưới.")

S2 = sol(
    [r"<strong>Góc tới hạn</strong> (thuỷ tinh ra không khí): $\sin i_{th}=\dfrac1n$.",
     r"<strong>Phản xạ toàn phần</strong> khi $i\ge i_{th}$ ; nếu $i\lt i_{th}$ tia ló ra theo $\sin r=n\sin i$.",
     r"<strong>Tia vuông góc $AB$:</strong> góc tới ở $AC$ bằng $A$ ; góc lệch $D=r-A$."],
    [("Góc tới hạn", [M(r"\sin i_{th}=\dfrac1n=\dfrac1{1{,}60}=0{,}625"), A(r"i_{th}\approx38{,}7^\circ")]),
     (r"Với $A=35^\circ$: tia có ló ra không ?", [P("Tia vuông góc $AB$ nên góc tới ở $AC$ bằng $A$ :"), M(r"i=35^\circ\lt i_{th}\approx38{,}7^\circ"), A("T:Tia <strong>ló ra</strong> khỏi $AC$.")]),
     ("Góc ló", [M(r"\sin r=n\sin i=1{,}60\cdot\sin35^\circ\approx0{,}918"), A(r"r\approx66{,}6^\circ")]),
     ("Góc lệch", [M(r"D=r-A=66{,}6^\circ-35^\circ"), A(r"D\approx31{,}6^\circ")]),
     (r"Với $A=40^\circ$: tia có ló ra không ?", [M(r"i=40^\circ\gt i_{th}\approx38{,}7^\circ"), P(r"Thử khúc xạ : $1{,}60\cdot\sin40^\circ\approx1{,}03\gt1$, không có góc $r$ nào thoả mãn."), A("T:Phản xạ toàn phần ở $AC$, tia <strong>không ló</strong> ra khỏi $AC$.")])],
    [r"a) $i_{th}\approx38{,}7^\circ$", r"b) tia <strong>ló ra</strong> ; $r\approx66{,}6^\circ$, $D\approx31{,}6^\circ$", r"c) $A=40^\circ$ : <strong>không ló</strong> (phản xạ toàn phần)"],
    "Nhận dạng: trước khi tính góc ló, so góc tới $i=A$ với $i_{th}$ ; nếu $n\\sin i$ vượt $1$ thì không có tia ló.")

S3 = sol(
    [r"<strong>Tán sắc:</strong> chiết suất của thuỷ tinh tăng dần theo dãy đỏ, cam, vàng, lục, lam, chàm, tím.",
     r"<strong>Lăng kính</strong> bẻ mọi tia về phía đáy ; chiết suất càng lớn tia càng lệch nhiều.",
     r"<strong>Kính lọc màu</strong> chỉ cho ánh sáng cùng màu đi qua ; lăng kính không tạo ra màu."],
    [("Màu lệch nhiều nhất", [P("Ba màu cùng góc tới. Tím có chiết suất lớn nhất trong ba màu nên bị bẻ mạnh nhất :"), A("T:<strong>Tím</strong> lệch nhiều nhất, đỏ lệch ít nhất.")]),
     ("Vị trí đáy", [P("Màu lệch nhiều nhất nằm gần đáy nhất. Vệt tím ở trên cùng, vệt đỏ (lệch ít nhất) ở dưới cùng :"), A("T:Đáy lăng kính quay <strong>lên trên</strong>.")]),
     ("Vị trí ánh sáng vàng", [P("Trong dãy màu, vàng đứng sau đỏ và trước lục : $n_{\\text{đ}}\\lt n_{\\text{vàng}}\\lt n_{\\text{lục}}$. Vàng lệch nhiều hơn đỏ, ít hơn lục :"), A("T:Vàng nằm <strong>giữa chỗ vệt đỏ và vệt lục</strong>.")]),
     ("Kính lọc vàng", [P("Kính lọc chỉ cho ánh sáng vàng đi qua. Ánh sáng vàng vẫn khúc xạ hai lần như trước, lệch đúng góc của nó ở câu b :"), A("T:Chỉ còn <strong>một vệt vàng</strong>, giữa chỗ vệt đỏ và vệt lục cũ.")])],
    ["a) <strong>tím</strong> lệch nhiều nhất ; đáy quay <strong>lên trên</strong>", "b) vàng nằm giữa chỗ vệt đỏ và vệt lục", "c) chỉ một vệt vàng, đúng chỗ vàng ở câu b (giữa vệt đỏ và vệt lục cũ)"],
    "Nhận dạng: từ thứ tự vệt màu suy ra đáy — màu có chiết suất lớn nhất luôn nằm phía đáy, dù đáy ở trên hay ở dưới.")

S4 = sol(
    [r"<strong>Tia vuông góc $AB$:</strong> góc tới ở $AC$ bằng $A$ cho mọi màu ; màu ló ra khi $A\lt i_{th}$ của màu đó, $\sin i_{th}=\dfrac1n$.",
     r"<strong>Ra không khí:</strong> $\sin r=n\sin A$ ; góc lệch $D=r-A$, mỗi màu một giá trị.",
     r"<strong>Tam giác vuông:</strong> cạnh đối $=$ cạnh kề $\times\tan$ góc."],
    [("Góc tới hạn của tia tím", [P("Chiết suất lớn nhất thì góc tới hạn nhỏ nhất, nên tím khó ló nhất :"), M(r"\sin i_{th,t}=\dfrac1{1{,}660}"), A(r"i_{th,t}\approx37{,}0^\circ")]),
     ("Hai tia có ló ra không ?", [M(r"i=A=32^\circ\lt i_{th,t}\approx37{,}0^\circ"), P("Tím ló được thì đỏ (góc tới hạn lớn hơn) cũng ló :"), A("T:Cả tia đỏ và tia tím <strong>đều ló ra</strong>.")]),
     ("Góc lệch của tia đỏ", [M(r"\sin r_{\text{đ}}=1{,}620\cdot\sin32^\circ\approx0{,}8585\ \Rightarrow\ r_{\text{đ}}\approx59{,}15^\circ"), M(r"D_{\text{đ}}=r_{\text{đ}}-A=59{,}15^\circ-32^\circ"), A(r"D_{\text{đ}}\approx27{,}15^\circ")]),
     ("Góc lệch của tia tím", [M(r"\sin r_t=1{,}660\cdot\sin32^\circ\approx0{,}8797\ \Rightarrow\ r_t\approx61{,}60^\circ"), M(r"D_t=r_t-A=61{,}60^\circ-32^\circ"), A(r"D_t\approx29{,}60^\circ")]),
     ("Góc hợp bởi hai tia ló", [P("Hai tia cùng lệch về phía đáy so với phương tia tới :"), M(r"\Delta=D_t-D_{\text{đ}}"), P(r"Lấy hiệu từ các giá trị chưa làm tròn ($29{,}602^\circ-27{,}145^\circ$) :"), A(r"\Delta\approx2{,}46^\circ")]),
     ("Khoảng cách hai vệt", [P(r"Mỗi vệt nằm dưới đường kéo dài của tia tới một đoạn $L\tan D$ ($L$ là cạnh kề). Hai vệt cùng phía nên lấy hiệu :"), M(r"\ell=L\,(\tan D_t-\tan D_{\text{đ}})"), M(r"\ell\approx1{,}50\cdot(0{,}5681-0{,}5128)\approx0{,}083\ \text{m}"), A(r"\ell\approx8{,}3\ \text{cm}")])],
    [r"a) cả hai ló ra ; $D_{\text{đ}}\approx27{,}15^\circ$, $D_t\approx29{,}60^\circ$ ; góc giữa hai tia $\approx2{,}46^\circ$", r"b) $\ell\approx8{,}3\ \text{cm}$ (vệt tím ở dưới, gần phía đáy hơn)"],
    "Nhận dạng: hai màu cùng góc tới nhưng khác chiết suất → tính riêng góc lệch từng màu ; khoảng cách trên tường là hiệu hai đoạn $L\\tan D$, không phải $L\\tan\\Delta$.")

S5 = sol(
    [r"<strong>Tia vuông góc $AB$:</strong> góc tới ở $AC$ bằng $A$, như nhau với mọi màu.",
     r"<strong>Một màu ló ra</strong> khi $A\lt i_{th}$ của màu đó, tức $n\sin A\lt1$ ; ngược lại thì phản xạ toàn phần.",
     r"<strong>Chiết suất càng lớn</strong> thì $\sin i_{th}=\dfrac1n$ càng nhỏ: màu đó phản xạ toàn phần sớm hơn."],
    [("Chiết suất lớn nhất còn ló ra", [M(r"n\sin41{,}5^\circ\lt1\ \Rightarrow\ n\lt\dfrac1{\sin41{,}5^\circ}"), A(r"n\lt1{,}509")]),
     ("Những màu ló ra", [P(r"Đỏ $1{,}48$ và vàng $1{,}50$ nhỏ hơn $1{,}509$ : ló ra. Lục $1{,}52$, lam $1{,}55$, tím $1{,}58$ lớn hơn : phản xạ toàn phần."), A("T:Ló ra : <strong>đỏ và vàng</strong>.")]),
     ("Cận dưới của $A$", [P(r"Bốn màu cần chặn, màu khó phản xạ toàn phần nhất là màu có chiết suất nhỏ nhất trong chúng : vàng. Vàng phản xạ toàn phần thì lục, lam, tím cũng vậy :"), M(r"A\ge i_{th,\text{vàng}},\quad \sin i_{th,\text{vàng}}=\dfrac1{1{,}50}"), A(r"A\ge41{,}81^\circ")]),
     ("Cận trên của $A$", [P("Đỏ phải ló ra :"), M(r"A\lt i_{th,\text{đ}},\quad \sin i_{th,\text{đ}}=\dfrac1{1{,}48}"), A(r"A\lt42{,}51^\circ")]),
     ("Kiểm tra", [P(r"Thử $A=42^\circ$ (nằm trong khoảng) :"), M(r"1{,}48\cdot\sin42^\circ\approx0{,}990\lt1\ \text{(đỏ ló)}"), M(r"1{,}50\cdot\sin42^\circ\approx1{,}004\gt1\ \text{(vàng phản xạ)}")])],
    [r"a) ló ra : <strong>đỏ và vàng</strong> ; lục, lam, tím phản xạ toàn phần", r"b) $41{,}81^\circ\le A\lt42{,}51^\circ$"],
    "Nhận dạng: chùm nhiều màu và hỏi màu nào ló → mỗi màu một góc tới hạn ; muốn chặn một nhóm màu thì xét màu khó chặn nhất trong nhóm.")
SOLS = [S1, S2, S3, S4, S5]

# ───────────────────────── buoc[] ─────────────────────────
ST1 = dict(
    nhan_dang="Thấy <b>tia chiếu vuông góc mặt bên</b> → <b>góc tới ở mặt kia bằng A</b>, tia ló lệch về phía đáy",
    cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2},
    tom_de={"cho": [r"lăng kính $A=25^\circ$, $n=1{,}52$, đáy $BC$ ở trên", r"tia laser nằm ngang, vuông góc $AB$"],
            "tim": [r"a) góc tới ở $AC$ ; góc ló $r$", r"b) góc lệch $D$ ; tia ló lệch lên hay xuống"]},
    buoc=[
        buoc("Góc tới ở mặt AC", "Góc tới của tia sáng ở mặt AC bằng bao nhiêu độ?", 25, "°", 0.5,
             r"Lấy góc tới bằng $0^\circ$ vì thấy chữ “vuông góc”, hoặc lấy $90^\circ-A$ : tia vuông góc với mặt $AB$, không phải với $AC$."),
        buoc("Góc ló", "Góc ló r ra khỏi mặt AC bằng bao nhiêu độ?", 39.97, "°", 0.3,
             r"Viết $\sin r=\dfrac{\sin i}{n}$ (chiều từ không khí vào thuỷ tinh) nên ra góc nhỏ hơn góc tới, trái với “ra không khí thì xa pháp tuyến”.",
             ke=[(r"$\sin r=n\sin i$", True),
                 (r"$\sin r=\dfrac{\sin i}{n}$", "Đó là chiều từ không khí vào thuỷ tinh. Ở mặt AC tia đi từ thuỷ tinh ra không khí nên nhân với n."),
                 (r"$r=n\cdot i$", "Định luật khúc xạ liên hệ sin của các góc, không phải chính các góc.")]),
        buoc("Góc lệch", "Góc lệch D của tia ló bằng bao nhiêu độ?", 14.97, "°", 0.3,
             r"Lấy $D=r$ : $r$ đo từ pháp tuyến của $AC$, còn $D$ đo từ phương tia tới.",
             ke=[(r"$D=r-i$", True),
                 (r"$D=r$", r"$r$ đo từ pháp tuyến của $AC$ ; pháp tuyến này nghiêng một góc bằng $A$ so với phương tia tới."),
                 (r"$D=r+i$", "Phần kéo dài của tia trong thuỷ tinh và tia ló cùng một phía pháp tuyến nên hai góc trừ nhau.")]),
        buoc("Chiều lệch", "Tia ló lệch về phía nào so với phương nằm ngang?", None, None, None,
             "Nhớ máy móc “tia ló đi xuống” từ hình lăng kính đáy dưới, quên rằng đáy bây giờ ở trên.",
             ke=[("Xem đáy BC đang ở phía nào", True),
                 ("Xem đỉnh A đang ở phía nào", "Lăng kính bẻ tia về phía đáy, không về phía đỉnh."),
                 ("Lấy chiều quen thuộc: tia ló luôn đi xuống", "Chiều lệch theo vị trí đáy, không cố định trên – dưới.")],
             lua_chon=[("Lệch lên trên, về phía đáy BC", True),
                       ("Lệch xuống dưới, về phía đỉnh A", "Lăng kính luôn bẻ tia về phía đáy ; ở đây đáy BC nằm ở trên."),
                       ("Không lệch, vì tia tới vuông góc mặt AB", "Tia không gãy ở AB nhưng gãy ở AC (góc tới ở AC khác 0) nên vẫn lệch.")]),
        buoc("Kiểm tra: thay ngược vào định luật khúc xạ"),
    ])

ST2 = dict(
    nhan_dang="Thấy hỏi <b>tia có ló ra không</b> → so <b>góc tới ở mặt ra</b> với <b>góc tới hạn</b> trước khi tính",
    cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1},
    tom_de={"cho": [r"thuỷ tinh $n=1{,}60$, tia tới vuông góc $AB$", r"lăng kính $A=35^\circ$, rồi $A=40^\circ$"],
            "tim": [r"a) góc tới hạn $i_{th}$", r"b) $A=35^\circ$ : ló không ? $r$, $D$", r"c) $A=40^\circ$ : ló không ?"]},
    buoc=[
        buoc("Góc tới hạn", r"Góc tới hạn $i_{th}$ khi ánh sáng đi từ thuỷ tinh ra không khí bằng bao nhiêu độ?", 38.68, "°", 0.2,
             r"Viết $\sin i_{th}=n$ (lớn hơn 1, máy báo lỗi) thay vì $\sin i_{th}=\dfrac1n$ ; hoặc quên bấm $\sin^{-1}$ để đổi ra góc."),
        buoc(r"Với $A=35^\circ$: ló ra không?", r"Với $A=35^\circ$, tia sáng có ló ra khỏi mặt $AC$ không?", None, None, None,
             r"Lấy góc tới ở $AC$ bằng $90^\circ-A$ (nhầm góc với mặt và góc với pháp tuyến), hoặc tính luôn góc ló mà chưa so góc tới với góc tới hạn.",
             ke=[(r"So góc tới $i=A$ ở $AC$ với $i_{th}$", True),
                 (r"So góc $90^\circ-A$ với $i_{th}$", r"$90^\circ-A$ là góc giữa tia và mặt $AC$, không phải góc tới (góc với pháp tuyến)."),
                 (r"So góc chiết quang $A$ với $90^\circ$", "Góc tới nhỏ hơn 90° chưa đủ để ló ; phải nhỏ hơn góc tới hạn.")],
             lua_chon=[("Ló ra, vì góc tới ở AC nhỏ hơn góc tới hạn", True),
                       (r"Không ló, vì góc tới ở $AC$ bằng $90^\circ-A$, lớn hơn góc tới hạn", r"Tia vuông góc $AB$ nên góc tới ở $AC$ bằng $A$, không phải $90^\circ-A$."),
                       ("Không ló, vì tia đi từ thuỷ tinh ra không khí luôn bị phản xạ toàn phần", "Phản xạ toàn phần còn cần góc tới lớn hơn hoặc bằng góc tới hạn.")]),
        buoc("Góc ló", "Góc ló r ra khỏi mặt AC bằng bao nhiêu độ?", 66.6, "°", 0.3,
             r"Dùng $\sin r=\dfrac{\sin A}{n}$ nên ra góc ló nhỏ hơn góc tới, trái với “ra không khí thì xa pháp tuyến”.",
             ke=[(r"$\sin r=n\sin A$", True),
                 (r"$\sin r=\dfrac{\sin A}{n}$", "Đó là chiều từ không khí vào thuỷ tinh ; ở AC tia đi từ thuỷ tinh ra."),
                 (r"$r=n\cdot A$", "Định luật khúc xạ liên hệ sin của các góc, không phải chính các góc.")]),
        buoc("Góc lệch", "Góc lệch D bằng bao nhiêu độ?", 31.6, "°", 0.3,
             r"Dừng ở góc ló $r$ và coi đó là góc lệch, quên rằng $r$ đo từ pháp tuyến của $AC$.",
             ke=[(r"$D=r-A$", True),
                 (r"$D=r$", r"$r$ đo từ pháp tuyến của $AC$, pháp tuyến này đã nghiêng góc $A$ so với phương tia tới."),
                 (r"$D=r+A$", "Phần kéo dài của tia trong thuỷ tinh và tia ló cùng một phía pháp tuyến nên hai góc trừ nhau.")]),
        buoc(r"Với $A=40^\circ$: ló ra không?", r"Với $A=40^\circ$, tia sáng có ló ra khỏi mặt $AC$ không?", None, None, None,
             r"Giữ kết luận của câu b vì cùng thuỷ tinh : chưa so lại góc tới mới với góc tới hạn, chưa thử $n\sin A$ với $1$.",
             ke=[(r"So góc tới mới $i=A$ với $i_{th}$", True),
                 (r"So góc mới $90^\circ-A$ với $i_{th}$", r"$90^\circ-A$ là góc giữa tia và mặt $AC$ ; góc tới đo từ pháp tuyến, bằng $A$."),
                 (r"So góc lệch $D$ của câu b với $i_{th}$", "Góc lệch đo từ phương tia tới, không phải góc tới ở AC ; điều kiện ló chỉ phụ thuộc góc tới.")],
             lua_chon=[("Không ló: tia bị phản xạ toàn phần ở AC", True),
                       ("Ló ra và lệch nhiều hơn, vì A lớn hơn", "Góc tới đã vượt góc tới hạn ; thử tính thì n·sin A lớn hơn 1, không có góc ló."),
                       ("Ló ra, đi sát mặt AC", "Tia chỉ đi sát mặt khi góc tới đúng bằng góc tới hạn ; ở đây góc tới lớn hơn.")]),
    ])

ST3 = dict(
    nhan_dang="Thấy <b>thứ tự các vệt màu</b> trên màn → màu <b>lệch nhiều nhất nằm phía đáy</b>",
    cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1},
    tom_de={"cho": ["chùm đỏ + lục + tím nằm ngang, lăng kính bị che", "trên màn từ trên xuống : tím, lục, đỏ"],
            "tim": ["a) màu lệch nhiều nhất ; đáy ở trên hay dưới", "b) chùm trắng : vàng nằm ở đâu", "c) thêm kính lọc vàng : còn thấy gì"]},
    buoc=[
        buoc("Màu lệch nhiều nhất", "Màu nào bị lăng kính làm lệch nhiều nhất?", None, None, None,
             "Nghĩ đỏ là màu “mạnh” nên lệch nhiều nhất ; thật ra đỏ có chiết suất nhỏ nhất nên lệch ít nhất.",
             lua_chon=[("Tím", True),
                       ("Đỏ", "Đỏ có chiết suất nhỏ nhất nên lệch ít nhất."),
                       ("Ba màu lệch như nhau vì cùng góc tới", "Cùng góc tới nhưng chiết suất mỗi màu khác nhau nên lệch khác nhau.")]),
        buoc("Vị trí đáy", "Đáy lăng kính quay lên trên hay xuống dưới?", None, None, None,
             "Đọc theo hình quen thuộc “đỏ trên, tím dưới thì đáy dưới” rồi áp ngược ; phải hỏi màu nào lệch nhiều nhất và nó nằm phía nào.",
             ke=[("Màu lệch nhiều nhất nằm phía đáy", True),
                 ("Màu lệch nhiều nhất nằm phía cạnh (đỉnh)", "Lăng kính bẻ tia về phía đáy, không về phía cạnh."),
                 ("Đỏ luôn nằm trên cùng", "Thứ tự trên – dưới phụ thuộc vị trí đáy ; đỏ chỉ ở trên cùng khi đáy ở dưới.")],
             lua_chon=[("Quay lên trên", True),
                       ("Quay xuống dưới", "Nếu đáy ở dưới thì tím (lệch nhiều nhất) phải nằm dưới cùng ; ở đây tím nằm trên cùng."),
                       ("Không xác định được", "Thứ tự màu đủ để biết : màu lệch nhiều nhất luôn nằm phía đáy.")]),
        buoc("Vị trí ánh sáng vàng", "Trên màn, ánh sáng vàng nằm ở đâu?", None, None, None,
             "Đặt vàng ở giữa dải vì “vàng là màu giữa” ; phải xếp theo chiết suất : vàng đứng giữa đỏ và lục.",
             ke=[("Xếp chiết suất của vàng vào dãy đỏ – lục – tím", True),
                 ("Coi lăng kính tạo thêm màu vàng ở chính giữa dải", "Lăng kính không tạo màu ; vàng có sẵn trong ánh sáng trắng và lệch theo chiết suất riêng."),
                 ("Coi vàng nằm ngoài cùng vì là màu sáng nhất", "Độ sáng không quyết định độ lệch ; chiết suất mới quyết định.")],
             lua_chon=[("Giữa chỗ vệt đỏ và vệt lục", True),
                       ("Giữa chỗ vệt lục và vệt tím", "Vàng đứng trước lục trong dãy Đỏ Cam Vàng Lục Lam Chàm Tím, chiết suất nhỏ hơn lục nên lệch ít hơn lục."),
                       ("Dưới chỗ vệt đỏ", "Vàng có chiết suất lớn hơn đỏ nên lệch nhiều hơn đỏ, tức nằm gần đáy hơn vệt đỏ.")]),
        buoc("Thêm kính lọc vàng", "Trên màn còn thấy gì?", None, None, None,
             "Nghĩ ánh sáng đã lọc không bị lệch nữa, hoặc lăng kính vẫn tách ra đủ màu ; lăng kính chỉ tách màu có sẵn và vẫn bẻ tia vàng như ở câu b.",
             ke=[("Xét ánh sáng nào qua được kính lọc, rồi nó lệch thế nào", True),
                 ("Coi lăng kính nhuộm lại đủ các màu", "Lăng kính không tạo màu ; chùm tới chỉ còn vàng thì sau lăng kính chỉ có vàng."),
                 ("Coi kính lọc chặn hết ánh sáng", "Kính lọc vàng cho phần ánh sáng vàng trong chùm trắng đi qua.")],
             lua_chon=[("Một vệt vàng, giữa chỗ vệt đỏ và vệt lục cũ", True),
                       ("Một vệt vàng ngang tầm chùm tới, không bị lệch", "Ánh sáng vàng qua lăng kính vẫn khúc xạ hai lần và lệch về đáy như ở câu b."),
                       ("Đủ dải màu nhưng ngả vàng", "Sau kính lọc chỉ còn ánh sáng vàng ; lăng kính không có màu khác để tách.")]),
    ])

ST4 = dict(
    nhan_dang="Thấy <b>hai màu, chiết suất khác nhau</b>, hỏi <b>vệt trên tường</b> → tính <b>riêng từng màu</b> rồi mới so",
    cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 5},
    tom_de={"cho": [r"$A=32^\circ$, tia nắng vuông góc $AB$", r"$n_{\text{đ}}=1{,}620$ ; $n_t=1{,}660$", r"tường cách $I$ : $L=1{,}50\ \text{m}$ theo phương tia tới"],
            "tim": [r"a) cả hai ló không ? $D_{\text{đ}}$, $D_t$, góc giữa hai tia", r"b) khoảng cách $\ell$ giữa hai vệt (cm)"]},
    buoc=[
        buoc("Góc tới hạn của tia tím", "Góc tới hạn của ánh sáng tím (thuỷ tinh ra không khí) bằng bao nhiêu độ?", 37.04, "°", 0.15,
             r"Viết $\sin i_{th}=n$ (lớn hơn 1, máy báo lỗi) thay vì $\dfrac1n$."),
        buoc("Hai tia có ló ra không?", "Tia đỏ và tia tím có cùng ló ra khỏi mặt AC không?", None, None, None,
             "So góc tới với góc tới hạn của đỏ (dễ ló nhất) rồi kết luận cho cả hai ; phải xét màu khó ló nhất là tím.",
             ke=[(r"So góc tới $i=A$ với góc tới hạn của tím", True),
                 (r"So góc tới $i=A$ với góc tới hạn của đỏ", "Đỏ có góc tới hạn lớn nhất, dễ ló nhất ; đỏ ló chưa chắc tím ló."),
                 (r"So góc $90^\circ-A$ với góc tới hạn của tím", r"$90^\circ-A$ là góc giữa tia và mặt $AC$ ; góc tới đo từ pháp tuyến, bằng $A$.")],
             lua_chon=[("Cả hai cùng ló ra", True),
                       ("Chỉ tia đỏ ló, tia tím phản xạ toàn phần", "Góc tới ở AC nhỏ hơn cả góc tới hạn của tím vừa tính, nên tím cũng ló."),
                       ("Cả hai phản xạ toàn phần vì thuỷ tinh có n > 1", "n > 1 chỉ cho biết chiều đi ra môi trường kém chiết quang ; còn phải so góc tới với góc tới hạn.")]),
        buoc("Góc lệch của tia đỏ", "Góc lệch của tia đỏ bằng bao nhiêu độ?", 27.15, "°", 0.15,
             r"Dừng ở góc ló $r_{\text{đ}}$ (đo từ pháp tuyến), quên trừ $A$.",
             ke=[(r"$\sin r_{\text{đ}}=n_{\text{đ}}\sin A$, rồi $D_{\text{đ}}=r_{\text{đ}}-A$", True),
                 (r"$\sin r_{\text{đ}}=\dfrac{\sin A}{n_{\text{đ}}}$, rồi $D_{\text{đ}}=r_{\text{đ}}-A$", "Đó là chiều từ không khí vào thuỷ tinh ; ở AC tia đi từ thuỷ tinh ra."),
                 (r"$D_{\text{đ}}=r_{\text{đ}}$", "Góc ló đo từ pháp tuyến của AC, góc lệch đo từ phương tia tới.")]),
        buoc("Góc lệch của tia tím", "Góc lệch của tia tím bằng bao nhiêu độ?", 29.6, "°", 0.15,
             r"Nhân góc lệch của đỏ với tỉ số $\dfrac{n_t}{n_{\text{đ}}}$ ; góc lệch không tỉ lệ với chiết suất, phải tính lại qua sin.",
             ke=[(r"Làm như tia đỏ, thay $n_t$ vào $\sin r_t=n_t\sin A$", True),
                 (r"$D_t=D_{\text{đ}}\cdot\dfrac{n_t}{n_{\text{đ}}}$", "Góc lệch không tỉ lệ với chiết suất ; định luật khúc xạ đi qua sin của các góc."),
                 (r"$D_t=D_{\text{đ}}$ vì cùng góc tới", "Cùng góc tới nhưng chiết suất khác nhau nên góc ló khác nhau.")]),
        buoc("Góc hợp bởi hai tia ló", "Góc hợp bởi tia đỏ và tia tím bằng bao nhiêu độ?", 2.457, "°", 0.06,
             r"Cộng hai góc lệch ; hai tia cùng lệch về phía đáy nên góc giữa chúng là hiệu.",
             ke=[(r"$\Delta=D_t-D_{\text{đ}}$", True),
                 (r"$\Delta=D_t+D_{\text{đ}}$", "Hai tia lệch cùng một phía (về đáy) so với phương tia tới nên góc giữa chúng là hiệu, không phải tổng."),
                 (r"$\Delta=D_t$", "D_t là góc giữa tia tím và phương tia tới, không phải góc giữa tia tím và tia đỏ.")]),
        buoc("Khoảng cách hai vệt", "Khoảng cách giữa vệt đỏ và vệt tím trên tường bằng bao nhiêu cm?", 8.3, "cm", 0.2,
             r"Tính $L\tan\Delta$ như thể tia đỏ đi thẳng theo phương tia tới, hoặc quên đổi m ra cm.",
             ke=[(r"$\ell=L\,(\tan D_t-\tan D_{\text{đ}})$", True),
                 (r"$\ell=L\tan\Delta$", "Đó là khoảng cách khi một tia đi dọc phương tia tới ; tia đỏ cũng lệch nên phải lấy hiệu hai đoạn."),
                 (r"$\ell=L\,(\sin D_t-\sin D_{\text{đ}})$", "L là cạnh kề (đo theo phương tia tới), không phải cạnh huyền dọc tia ló, nên dùng tan.")]),
    ])

ST5 = dict(
    nhan_dang="Thấy <b>chùm nhiều màu</b>, hỏi <b>màu nào ló ra</b> → so góc tới với <b>góc tới hạn của từng màu</b>",
    cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2},
    tom_de={"cho": ["chùm 5 màu vuông góc $AB$", r"$n$ : đỏ $1{,}48$ ; vàng $1{,}50$ ; lục $1{,}52$ ; lam $1{,}55$ ; tím $1{,}58$"],
            "tim": [r"a) $A=41{,}5^\circ$ : màu nào ló ra", r"b) khoảng $A$ để chỉ đỏ ló ra"]},
    buoc=[
        buoc("Chiết suất lớn nhất còn ló ra", r"Với $A=41{,}5^\circ$, một màu ló ra khỏi AC khi chiết suất của nó nhỏ hơn giá trị nào?", 1.509, "", 0.003,
             r"Viết điều kiện ló là $n\lt\sin A$ (quên nghịch đảo), hoặc đảo chiều thành $n\gt\dfrac1{\sin A}$."),
        buoc("Những màu ló ra", r"Với $A=41{,}5^\circ$, những màu nào ló ra khỏi mặt AC?", None, None, None,
             r"Làm tròn $\dfrac1{\sin41{,}5^\circ}$ thành $1{,}5$ quá sớm nên tưởng vàng ($1{,}50$) bị phản xạ toàn phần.",
             ke=[("So chiết suất từng màu với giá trị vừa tìm", True),
                 (r"So góc tới $41{,}5^\circ$ với $90^\circ$", "Góc tới nhỏ hơn 90° chưa đủ để ló ; phải nhỏ hơn góc tới hạn của từng màu."),
                 ("Tính góc lệch D của từng màu rồi so", "Chưa biết màu nào ló thì chưa tính được D ; với màu phản xạ toàn phần, n·sin A vượt 1.")],
             lua_chon=[("Đỏ và vàng", True),
                       ("Chỉ đỏ", "Làm tròn ngưỡng thành 1,5 quá sớm ; giữ ba chữ số thập phân thì chiết suất của vàng vẫn nhỏ hơn ngưỡng."),
                       ("Lục, lam và tím", "Ngược chiều : chiết suất lớn thì góc tới hạn nhỏ, dễ bị phản xạ toàn phần hơn.")]),
        buoc("Cận dưới của A", "Để bốn màu kia đều phản xạ toàn phần, A phải lớn hơn hoặc bằng bao nhiêu độ?", 41.81, "°", 0.1,
             "Lấy góc tới hạn của tím (màu phản xạ toàn phần sớm nhất) : khi đó vàng, lục vẫn còn ló ra.",
             ke=[("Xét màu vàng : chiết suất nhỏ nhất trong bốn màu cần chặn", True),
                 ("Xét màu tím : chiết suất lớn nhất", "Tím phản xạ toàn phần sớm nhất ; chặn được tím chưa chắc chặn được vàng, lục."),
                 ("Xét màu đỏ", "Đỏ là màu cần cho ló ra ; điều kiện của đỏ chặn A từ phía trên, không phải từ phía dưới.")]),
        buoc("Cận trên của A", "Để ánh sáng đỏ vẫn ló ra, A phải nhỏ hơn bao nhiêu độ?", 42.51, "°", 0.1,
             r"Lấy $A\le90^\circ$ (chặn hình học) hoặc dùng chiết suất của vàng ; phải dùng góc tới hạn của chính màu đỏ.",
             ke=[(r"$\sin A\lt\dfrac1{n_{\text{đ}}}$", True),
                 (r"$\sin A\lt\dfrac1{n_{\text{vàng}}}$", "Vàng phải bị phản xạ toàn phần nên A không được nhỏ hơn góc tới hạn của vàng ; điều kiện này ngược với yêu cầu."),
                 (r"$A\lt90^\circ$", "Đó chỉ là chặn hình học ; đỏ có thể đã phản xạ toàn phần từ trước.")]),
        buoc("Kiểm tra: thử một giá trị A trong khoảng"),
    ])
STEPS = [ST1, ST2, ST3, ST4, ST5]
CC = [cc1(), cc2(), cc3(), cc4(), cc5()]

# ───────────────────────── ghép ─────────────────────────
assert len(DANG) == len(ANALYSIS) == len(SOLS) == len(STEPS) == len(CC) == len(FORM) == 5
for st, cc in zip(STEPS, CC):
    assert len(cc["lop"]) == len(st["buoc"]), (len(cc["lop"]), len(st["buoc"]))
    st["cong_cu"] = cc
BUILD = [lambda k: "" for _ in DANG]
write(J, 85, "Bài 7. Lăng kính", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
for q, f in zip(d["dang_bai"], FORM):
    q["form"] = f
d["generated_at"] = "2026-11-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo"}
# chuỗi raw r'...\'...' giữ nguyên gạch chéo → KaTeX hiểu \' là dấu sắc; bỏ gạch chéo trước dấu nháy
text = json.dumps(d, ensure_ascii=False, indent=1).replace("\\\\'", "'")
open(J, "w").write(text + "\n")
print("ghi", J, len(d["dang_bai"]), "dạng")
