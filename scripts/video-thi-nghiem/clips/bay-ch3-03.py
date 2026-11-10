# Clip bay phu dao L12 Ch.3 so 03 - Bo cam ung (pickup) guitar dien. Dinh luat Faraday va dinh luat Lenz. Theo mau bay-ch3-01/02.
# Tinh huong = de 1288 cau 7, 34/55 luot sai (62 %) trong 30 ngay:
#   "Guitar dien: moi bo cam ung gom mot cuon day va mot nam cham vinh cuu dat duoi day dan kim loai nhiem tu duoc.
#    Phat bieu nao SAI ve nguyen li bo cam ung?" A. Day dan dao dong tao ra dong cam ung xuat hien truc tiep trong no va
#    truyen den loa  B. Suat dien dong cam ung xuat hien do tu thong qua cuon day bien thien theo thoi gian
#    C. Hoat dong dua tren hien tuong cam ung dien tu  D. Day dan bi tu hoa dong vai tro nam cham dao dong -> A.
# Chu lua chon rut gon (giu nghia) de dat mat do chu; nhan A. B. C. D. (E1).
# Co che ve dong (nhin ngang): day dan nhiem tu rung len xuong tren nam cham thang dung (N o tren) co cuon day quanh no;
#   khoang cach day-nam cham doi -> tu thong qua CUON DAY doi -> dong cam ung o cuon day (doi chieu theo nhip rung) ra loa.
#   Duong suc net dut ra N vao S; dong cam ung ti le -d(Phi)/dt: day di xuong (Phi tang) va di len (Phi giam) -> hai chieu nguoc nhau.
from clips.bay_chung import *

MX, MY0, MY1, MHW = 540, 560, 740, 22      # nam cham: tam x, dinh N, day S, nua be rong
CY = (590, 610, 630, 650, 670, 690)        # cac vong cuon day
CRX, CRY = 95, 14
SY0, SA = 420, 36                          # day dan: vi tri can bang, bien do
SX0, SX1 = 120, 960
LX0, LX1, LY0, LY1 = 800, 1000, 590, 700   # loa
QY = 830
Q_LINES = ["Bộ cảm ứng guitar: phát biểu SAI?"]
OPTS = ["Dòng nằm ngay trong dây đàn", "Từ thông biến thiên gây suất điện động",
        "Dựa vào cảm ứng điện từ", "Dây đàn nhiễm từ như nam châm"]
ANS = 0
OMEGA = 2 * math.pi * 0.75                  # ~0,75 vong/s (chuyen dong chay cham de nhin; thuc te hang tram Hz)


def bez(p0, p1, p2, p3, n=24):
    pts = []
    for i in range(n + 1):
        u = i / n; a = (1 - u) ** 3; b = 3 * u * (1 - u) ** 2; c = 3 * u * u * (1 - u); e = u ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + e * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + e * p3[1]))
    return pts


def dash_poly(d, pts, color, w=4, seg=16, gap=12):
    """Net dut doc theo da tuyen; tra ve cac diem de dat mui ten."""
    L = [0.0]
    for a, b in zip(pts, pts[1:]): L.append(L[-1] + math.dist(a, b))
    def at(s):
        for i in range(1, len(L)):
            if s <= L[i]:
                k = (s - L[i - 1]) / max(1e-6, L[i] - L[i - 1]); a, b = pts[i - 1], pts[i]
                return (lerp(a[0], b[0], k), lerp(a[1], b[1], k))
        return pts[-1]
    s = 0.0
    while s < L[-1]:
        e = min(L[-1], s + seg); sub = [at(s + (e - s) * j / 4) for j in range(5)]
        d.line(sub, fill=color, width=w); s += seg + gap
    return at, L[-1]


def field(d, alpha=1.0):
    """Duong suc: tu mat tren N, vong ra hai ben, ve mat duoi S (net dut, mui chevron 30 do, ra N vao S)."""
    col = A(PURPLE, 0.55 * alpha)
    for rx in (150, 215):
        for sg in (-1, 1):
            p0 = (MX + sg * MHW * 0.6, MY0); pm = (MX + sg * rx, 650); p3 = (MX + sg * MHW * 0.6, MY1)
            up = bez(p0, (MX + sg * 40, MY0 - 70), (MX + sg * rx, 650 - 120), pm)
            dn = bez(pm, (MX + sg * rx, 650 + 120), (MX + sg * 40, MY1 + 70), p3)
            at, Ltot = dash_poly(d, up + dn[1:], col)
            x, y = at(Ltot * 0.25); x2, y2 = at(Ltot * 0.25 + 6)
            chevron(d, x2, y2, math.atan2(y2 - y, x2 - x), col, s=22, w=5)
            x, y = at(Ltot * 0.75); x2, y2 = at(Ltot * 0.75 + 6)
            chevron(d, x2, y2, math.atan2(y2 - y, x2 - x), col, s=22, w=5)


def magnet(d, alpha=1.0):
    d.rounded_rectangle([MX - MHW, MY0, MX + MHW, (MY0 + MY1) // 2], radius=6, fill=A(RED, alpha))
    d.rounded_rectangle([MX - MHW, (MY0 + MY1) // 2, MX + MHW, MY1], radius=6, fill=A(BLUE, alpha))
    text(d, (MX, 605), "N", 36, WHITE, alpha=alpha); text(d, (MX, 695), "S", 36, WHITE, alpha=alpha)


def coil(d, glow=0.0, alpha=1.0):
    col = A(mix(ORANGE, GREEN, glow), alpha)
    for y in CY: d.arc([MX - CRX, y - CRY, MX + CRX, y + CRY], 180, 360, fill=A(col[:3], 0.4 * alpha), width=7)
    magnet(d, alpha)
    for y in CY: d.arc([MX - CRX, y - CRY, MX + CRX, y + CRY], 0, 180, fill=col, width=9)


def string_y(x, t, amp=1.0):
    s = math.sin(math.pi * (x - SX0) / (SX1 - SX0))
    return SY0 + SA * amp * s * math.sin(OMEGA * t)


def string(d, t, color=INK, amp=1.0, alpha=1.0, w=9):
    pts = [(x, string_y(x, t, amp)) for x in range(SX0, SX1 + 1, 20)]
    d.line(pts, fill=A(color, alpha), width=w, joint="curve")
    for x in (SX0, SX1): d.ellipse([x - 12, SY0 - 12, x + 12, SY0 + 12], fill=A(NAVY, alpha))
    return pts


def loa(d, alpha=1.0):
    d.rounded_rectangle([LX0, LY0, LX1, LY1], radius=18, fill=A(NAVY, alpha))
    text(d, ((LX0 + LX1) / 2, (LY0 + LY1) / 2), "Loa", 40, WHITE, alpha=alpha)


def wires(d, sgn=0.0, alpha=1.0):
    """Day noi cuon day - loa (mach kin). sgn in [-1,1]: chieu va do lon dong cam ung (mui ten chevron tren day)."""
    col = A(GRAY, alpha)
    d.line([(MX + CRX, CY[0]), (LX0, CY[0])], fill=col, width=6)
    d.line([(MX - CRX, CY[-1]), (MX - CRX, 775), (900, 775), (900, LY1)], fill=col, width=6)
    if abs(sgn) > 0.08:
        g = A(GREEN, min(1, abs(sgn) * 1.6) * alpha); a0 = 0 if sgn > 0 else math.pi
        chevron(d, 720, CY[0], a0, g, s=30, w=9)
        chevron(d, 700, 775, a0 + math.pi, g, s=30, w=9)
        d.line([(660, CY[0]), (740, CY[0])], fill=g, width=9)
        d.line([(680, 775), (720, 775)], fill=g, width=9)


def labels(d, k=0):
    """k=2: du ba nhan (canh dap an); canh hoi khong nhan de giam chu."""
    if k <= 1: return
    text(d, (540, 345), "Dây đàn", 38, INK)
    text(d, (60, 720), "Nam châm", 36, PURPLE, anchor="lm")
    text(d, (60, 640), "Cuộn dây", 36, ORANGE, anchor="lm")


def phi(t):
    """Tu thong qua cuon day (tuong doi 0..1): lon khi day dan o gan nam cham nhat (y lon nhat)."""
    return 0.5 + 0.5 * math.sin(OMEGA * t)


def dphi(t):   # d(Phi)/dt chuan hoa; dong cam ung ti le -d(Phi)/dt
    return -math.cos(OMEGA * t)


def scene_base(d, t, sgn=0.0, glow=0.0, amp=1.0, scol=INK, lab=0.0):
    field(d); coil(d, glow); wires(d, sgn); loa(d); labels(d, lab)
    return string(d, t, scol, amp)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    scene_base(d, t, amp=0.55, lab=1)
    k = appear(t, sc["M"][0] + 0.2, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][0] + 0.9, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    scene_base(d, t, amp=0.55, lab=2)
    answer_pill(d, 1000, "A", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    if t < m1:   # gia thuyet A: dong chay ngay trong day dan -> day do + mui ten doc day, khong co dong o cuon day
        pts = scene_base(d, t, scol=RED)
        ka = appear(t, m0 + 0.5, 0.5)
        for x in (300, 780):
            y = string_y(x, t); chevron(d, x, y, 0, A(RED, ka), s=32, w=10)
        note(d, 900, "Dây đàn: không có dòng", RED, appear(t, m0, 0.45) * (1 - appear(t, m1 - 0.1, 0.3)))
        return
    k = appear(t, m1, 0.5); tt = t - m1 + 0.2
    pts = scene_base(d, t, sgn=dphi(t) * k, glow=k)
    note(d, 900, "Cuộn dây: Φ biến thiên", GREEN, k)
    # thanh Phi: tu thong qua cuon day bien thien theo khoang cach day dan
    kb = appear(t, m1 + 0.8, 0.5)
    if kb > 0:
        text(d, (W / 2, 1090), "Φ", 44, INK, alpha=kb)
        d.rounded_rectangle([180, 1130, 900, 1166], radius=18, outline=A(LIGHT, kb), width=3, fill=A(WHITE, kb))
        d.rounded_rectangle([184, 1134, 184 + 712 * phi(t), 1162], radius=14, fill=A(GREEN, kb))


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Dòng cảm ứng nằm ở cuộn dây",
             "Dây đàn đứng yên trên nam châm: loa có tiếng không?")


CLIP = dict(id="bay-l12-ch3-03", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Cảm ứng điện từ · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Chọn một đáp án.", 9.6)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án A.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=0.6, caps=[
   ("Chọn A: dòng trong dây đàn.", 3.2),
   ("Thật ra: dòng trong cuộn dây.", 3.6)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 5.6)]),
])
