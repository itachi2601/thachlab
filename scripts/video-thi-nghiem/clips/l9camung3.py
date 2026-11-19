# Clip: tn-l9-camung-03 - Nam cham quay truoc cuon day noi hai LED song song nguoc chieu (KHTN 9, bai 92, 18/11/2026)
# So lieu lay tu content/thi-nghiem/tn-l9-camung-03.json:
#   so_lieu_mau n = 2 ; 1 ; 0,5 vong/s -> moi LED chop 2 ; 1 ; 0,5 lan/s (mo hinh N_doi = 2n, moi LED sang nua vong).
#   quan_sat: thay nhau chop, khong bao gio cung luc ; quay cang nhanh chop cang nhanh, cang sang ; cham qua: khong sang
#   (LED can khoang 1,8 V). rut_ra: luan phien doi chieu = dong xoay chieu ; doi chieu 2 lan moi vong (chi noi nhu vay,
#   KHONG danh dau +/- tren khung quay). Bay = hien_tuong_hay_sai[2] (LED tat -> ket luan khong co dong).
#   Cong B 18/11: n = 2/1/0,5 vong/s quay tay ma LED 1,8 V sang la phi thuc te -> KHONG hien vong/s tren man, chi
#   "nhanh / cham dan / rat cham" (toc do ben trong giu ti le so_lieu_mau; kho da them ghi_chu "minh hoa ti le").
#   Cau chot: quay deu, dem 10 lan LED do chop -> nam cham quay may vong? -> 10 (moi LED chop 1 lan / vong, _kiem_vat_li).
#   So 10 la so dem dat ra cho cau hoi (khong phai so do), dap an suy tu mo hinh.
#   "Cham hon nua" (n = 0,2 vong/s) CHI de ve, KHONG hien so: kho khong co nguong n de LED tat (theo mo hinh).
#   Chua noi duoc: kho KHONG co khong_chung_minh cho TN nay -> tu viet: do lon dong chua do ; moi thu nam cham quay.
# Tranh tra loi san cau hoi cua bai:
#   - Cau "Doan truoc khi doc tiep" (sang cung luc / thay nhau / khong sang) dung ngay truoc hop: Du doan clip KHAC
#     (quay cham dan thi hai LED the nao).
#   - Kiem tra nhanh cau 6 + thu thach 2 sao (50 vong/s -> 100 lan): khong tinh so lan doi chieu moi giay, khong bang N_doi.
#   - Cau 6 (quay quanh truc doc), Cau 7 (dinamo, bay "quay mot chieu thi dong mot chieu"): khong dung.
#   - Tinh huong mau b) (moi den sang dung nua vong): khong noi "nua vong".
# Hinh: NHIN TU TREN XUONG. Nam cham quay quanh truc thang dung qua giua (cham tron), N do / S xanh, cuon day ben phai
#   truc nam ngang huong vao nam cham. Goc theta tinh tu huong "N nhin vao cuon day", tang nguoc chieu kim dong ho.
#   Tu thong qua cuon ~ cos(theta) -> dong ~ n.sin(theta): doi dau khi theta = 0 (N doi dien cuon) hoac 180 do (S doi dien).
#   LED do sang khi dong > nguong, LED xanh khi dong < -nguong (song song nguoc chieu). _kiem_vat_li() kiem.
import copy
from engine import *

N_BANG = (2.0, 1.0, 0.5)                    # so_lieu_mau n (vong/s)
N_CHAM = 0.2                                # "rat cham": chi de ve (khong hien so)
CHOT_DEM = 10                               # cau chot: dem 10 lan LED do chop
E_TH = 0.3                                  # nguong sang cua LED (don vi n.sin, theo mo hinh)
def vn(x): return (f"{x:g}").replace(".", ",")

# ---------------- bo cuc (khung 1080x1920) ----------------
MX, MY, MR, MT = 330, 560, 150, 36          # tam quay, nua chieu dai, nua be day nam cham (72 px > 60: giu chu N/S)
CL, CRR, CY, CR, NT = 610, 890, 560, 110, 9 # cuon day (nhin tu tren)
LX0, LX1, YR, YG, LXC = 520, 980, 990, 1170, 750   # khoi hai LED: nut trai/phai, nhanh do/xanh, tam diot

def turns(): return [CL + j * (CRR - CL) / (NT - 1) for j in range(NT)]

def chevron(d, x, y, ang, color, s=18, w=5):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def coil(d):
    for x in turns(): d.arc([x - 17, CY - CR, x + 17, CY + CR], 90, 270, fill=mix(ORANGE, BG, 0.45), width=7)
    for x in turns(): d.arc([x - 17, CY - CR, x + 17, CY + CR], 270, 90, fill=A(ORANGE, 0.95), width=9)
    text(d, ((CL + CRR) / 2, CY - CR - 40), "cuộn dây", 40, mix(ORANGE, INK, 0.3))

def magnet(d, th):
    ux, uy = math.cos(th), -math.sin(th); px, py = math.sin(th), math.cos(th)
    def half(s):
        a0, a1 = 0, s * MR
        return [(MX + ux * a + px * b, MY + uy * a + py * b) for a, b in ((a0, -MT), (a1, -MT), (a1, MT), (a0, MT))]
    d.polygon(half(-1), fill=BLUE); d.polygon(half(1), fill=RED)
    text(d, (MX + ux * MR * 0.55, MY + uy * MR * 0.55), "N", 44, WHITE)
    text(d, (MX - ux * MR * 0.55, MY - uy * MR * 0.55), "S", 44, WHITE)
    dot(d, MX, MY, 10, NAVY, outline=WHITE)

def spin_arrow(d, a=1.0):
    R = MR + 40; c = A(PURPLE, a)
    d.arc([MX - R, MY - R, MX + R, MY + R], -125, -55, fill=c, width=5)
    x, y = MX + R * math.cos(math.radians(-125)), MY + R * math.sin(math.radians(-125))
    s_, c_ = math.sin(math.radians(-125)), -math.cos(math.radians(-125))
    chevron(d, x, y, math.atan2(c_, s_), c)

def diode(d, y, right, col, b):
    """Diot nhanh y; right = cho dong tu trai sang phai. b: do sang 0..1 (0 = tat)."""
    if b > 0:
        for r, al in ((86, 0.18), (64, 0.30), (46, 0.45)):
            d.ellipse([LXC - r, y - r, LXC + r, y + r], fill=A(col, al * (0.35 + 0.65 * b)))
    s = 1 if right else -1; h = 30
    tri = [(LXC - s * 28, y - h), (LXC - s * 28, y + h), (LXC + s * 26, y)]
    d.polygon(tri, fill=mix(col, WHITE, 0.2) if b > 0 else mix(col, WHITE, 0.7), outline=NAVY)
    d.line([(LXC + s * 28, y - h), (LXC + s * 28, y + h)], fill=NAVY, width=6)

def circuit(d, e):
    w = 5
    d.line([(CL, CY + CR - 4), (CL, 760), (LX0, 760), (LX0, YG)], fill=NAVY, width=w)
    d.line([(CRR, CY + CR - 4), (CRR, 760), (LX1, 760), (LX1, YG)], fill=NAVY, width=w)
    for y in (YR, YG):
        d.line([(LX0, y), (LXC - 30, y)], fill=NAVY, width=w); d.line([(LXC + 30, y), (LX1, y)], fill=NAVY, width=w)
        dot(d, LX0, y, 9, NAVY); dot(d, LX1, y, 9, NAVY)
    br, bg = led(e)
    diode(d, YR, True, RED, br); diode(d, YG, False, GREEN, bg)
    text(d, (LX0 - 24, YR), "đỏ", 40, RED, anchor="rm"); text(d, (LX0 - 24, YG), "xanh", 40, GREEN, anchor="rm")

def led(e):
    """-> (do sang LED do, do sang LED xanh); 0 = tat. e = n.sin(theta)."""
    b = clamp((abs(e) - E_TH) / (N_BANG[0] - E_TH)) if abs(e) > E_TH else 0.0
    if abs(e) > E_TH: b = max(b, 0.02)
    return (b, 0.0) if e > 0 else (0.0, b)

def apparatus(d, th, n, nlab=None, spin=True):
    coil(d); magnet(d, th)
    if spin and n > 0: spin_arrow(d)
    circuit(d, n * math.sin(th))
    if nlab: text(d, (MX, 820), nlab, 46, PURPLE)

# ---------------- mo phong canh Tien hanh: n(t) -> theta(t) ----------------
DT = 1 / 240
def knots(sc):
    M, T = sc["M"], sc["T"]
    return [(0, 0), (0.4, 0), (1.0, 2.0), (M[1] + 0.2, 2.0), (M[1] + 0.7, 1.0), (M[1] + 2.9, 1.0), (M[1] + 3.4, 0.5),
            (M[2] + 0.1, 0.5), (M[2] + 0.6, N_CHAM), (T + 1, N_CHAM)]

_SIM = {}
def sim(sc):
    key = (tuple(sc["M"]), sc["T"])
    if key not in _SIM:
        kx, ky = zip(*knots(sc)); ts = np.arange(0, sc["T"] + DT, DT)
        ns = np.interp(ts, kx, ky); th = math.radians(100) + np.concatenate([[0], np.cumsum(2 * math.pi * ns[:-1] * DT)])
        _SIM[key] = (ts, ns, th, ns * np.sin(th))
    return _SIM[key]

def at(sc, t):
    ts, ns, th, es = sim(sc); k = int(clamp(t / DT, 0, len(ts) - 1))
    return ns[k], th[k], es[k]

def nlabel(t, sc):
    """Nhan toc do bang chu (khong so): nhanh -> cham dan -> rat cham (chi khi n da xuong N_CHAM, LED tat)."""
    M = sc["M"]
    if t < 0.4: return None
    if t < M[1] + 0.2: return "nhanh"
    if t < M[2] + 0.6: return "chậm dần"
    return "rất chậm"

# dai "den sang theo thoi gian": hai hang (do, xanh), cua so 5 s gan nhat (canh Tien hanh) hoac ca canh (Dap an)
def strip(d, sc, t0, t1, y=1270, head=True, upto=None):
    card(d, (40, y, 1040, y + 340), fill=WHITE, outline=LIGHT, w=3)
    if head: text(d, (W / 2, y + 40), "đèn sáng theo thời gian", 38, MUTED, bold=False)
    ts, ns, th, es = sim(sc); x0, x1 = 200, 1000
    for row, (yy, col, lab) in enumerate(((y + 140, RED, "đỏ"), (y + 260, GREEN, "xanh"))):
        text(d, (x0 - 30, yy), lab, 40, col, anchor="rm")
        d.line([(x0, yy), (x1, yy)], fill=LIGHT, width=4)
        for k in range(max(0, int(t0 / DT)), min(len(ts), int((t1 if upto is None else upto) / DT))):
            b = led(es[k])[row]
            if b > 0:
                x = x0 + (ts[k] - t0) / (t1 - t0) * (x1 - x0); hh = 14 + 30 * b
                d.line([(x, yy - hh), (x, yy + hh)], fill=A(col, 0.5 + 0.5 * b), width=3)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.6
TH_HOOK = math.radians(100)
def s_hook(img, d, t, sc):
    M = sc["M"]
    apparatus(d, TH_HOOK, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1270 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 340), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 55), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 150), "Quay nam châm nhanh, rồi chậm dần.", 42, INK, alpha=a)
    text(d, (W / 2, y0 + 228), "Hai LED sẽ thế nào?", 50, PURPLE, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 300, 940, y0 + 312], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 300, 140 + 800 * (1 - p), y0 + 312], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def s_do(img, d, t, sc):
    n, th, e = at(sc, t)
    apparatus(d, th, n, nlabel(t, sc))
    strip(d, sc, t - 5.0, t)
    d.line([(1000, 1360), (1000, 1580)], fill=A(NAVY, 0.6), width=3)

def _kiem_vat_li():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]
    ts, ns, th, es = sim(sc); bad = []
    for k in range(1, len(ts)):
        r, g = led(es[k])
        if r > 0 and g > 0: bad.append((round(ts[k], 2), "hai LED cung sang"))
        if es[k - 1] * es[k] < 0 and abs(math.cos(th[k])) < 0.99: bad.append((round(ts[k], 2), "doi chieu khi khong cuc nao doi dien cuon"))
    def window(n):   # doan n khong doi dai nhat (lien tuc)
        best, cur = (0, 0), None
        for k in range(len(ts)):
            if abs(ns[k] - n) < 1e-9:
                cur = (cur[0], ts[k]) if cur else (ts[k], ts[k])
                if cur[1] - cur[0] > best[1] - best[0]: best = cur
            else: cur = None
        return best
    peaks = []
    for n in N_BANG:
        a, b = window(n); per = 1 / n
        if b - a < per: bad.append((n, "chieu chua du mot vong")); continue
        ks = [k for k in range(len(ts)) if a <= ts[k] <= a + per]
        flips = sum(1 for k in ks[1:] if es[k - 1] * es[k] < 0)
        if flips != 2: bad.append((n, f"{flips} lan doi chieu / vong (phai 2)"))
        on_r = sum(1 for k in ks[1:] if led(es[k])[0] > 0 and led(es[k - 1])[0] == 0)
        if on_r != 1: bad.append((n, f"LED do chop {on_r} lan / vong (phai 1 -> {vn(n)} lan/s nhu bang)"))
        peaks.append(max(max(led(es[k])) for k in ks))
    if not (peaks == sorted(peaks, reverse=True) and len(set(peaks)) == len(peaks)): bad.append(("do sang", peaks))
    a, b = window(N_CHAM)
    if any(max(led(es[k])) > 0 for k in range(len(ts)) if a <= ts[k] <= b): bad.append("cham qua ma LED van sang")
    if N_CHAM * 1.0 > E_TH: bad.append("N_CHAM du lam LED sang")
    t_rc = min(ts[k] for k in range(len(ts)) if nlabel(ts[k], sc) == "rất chậm")
    if any(max(led(es[k])) > 0 for k in range(len(ts)) if ts[k] >= t_rc): bad.append("nhan 'rat cham' ma LED van sang")
    if abs(ns[int(t_rc / DT)] - N_CHAM) > 1e-9: bad.append("nhan 'rat cham' truoc khi n xuong N_CHAM")
    return bad

def _kiem_so():
    bad = []
    bang = {0.5: (1, 0.5), 1: (2, 1), 2: (4, 2)}    # so_lieu_mau: n -> (doi chieu/s, moi LED chop/s)
    for n in N_BANG:
        if bang[n] != (2 * n, n): bad.append(n)
    if CHOT_DEM * 1 != 10: bad.append("cau chot: moi LED chop 1 lan / vong -> 10 vong")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · mờ dần rồi tắt"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 336), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 299), lab, 42, WHITE, alpha=ka)
    dsc = do_scene()
    g = clamp((t - 0.4) / 1.4)
    strip(d, dsc, 0.0, dsc["T"], y=420, head=False, upto=dsc["T"] * g)
    for x, s, tm in ((330, "nhanh", 0.2), (620, "chậm dần", 0.55), (900, "rất chậm", 0.9)):
        if g >= tm: text(d, (x, 480), s, 40, MUTED, bold=False)
    k3 = appear(t, 2.0, 0.45)
    if k3 > 0:
        card(d, (40, 830, 1040, 1050), fill=A(WHITE, k3), outline=A(ORANGE, k3), w=5)
        text(d, (W / 2, 940), "Quay nhanh: sáng hơn", 48, ORANGE, alpha=k3)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (40, 1110, 1040, 1380), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1245), "Dòng luân phiên đổi chiều", 52, GREEN, alpha=k1)

_DO = []
def do_scene():
    """Canh Tien hanh da build (tu tinh, khong phu thuoc thu tu ve)."""
    if not _DO:
        clip = copy.deepcopy(CLIP); build(clip)
        _DO.append([s for s in clip["scenes"] if s["key"] == "do"][0])
    return _DO[0]

# ---------------- canh 4: Bay + Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    th = TH_HOOK + 2 * math.pi * N_CHAM * t
    apparatus(d, th, N_CHAM)
    k2 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 1270
        card(d, (40, y0, 1040, y0 + 340), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 86), fill=A(RED, a1), r=31)
        text(d, (W / 2, y0 + 55), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[0] - 1.6) / 0.4)
        q = "“LED tắt là không có dòng”"
        lw = tw(d, q, F(46)); yy = y0 + 160
        text(d, (W / 2, yy), q, 46, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        text(d, (W / 2, y0 + 262), "✓ LED cần dòng đủ lớn mới sáng", 44, GREEN, alpha=a1 * appear(t, M[0] + 2.2, 0.4))
    if k2 > 0:
        y0 = 1270
        card(d, (40, y0, 1040, y0 + 340), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 62), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, s in enumerate(("• Dòng lớn bao nhiêu: chưa đo", "• Mới thử nam châm quay")):
            text(d, (90, y0 + 160 + j * 100), s, 44, INK, bold=False, anchor="lm", alpha=k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4))

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
T_CHOT = 4.0
def s_end(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 620, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(38)) + 52
        card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 682), "THỬ NGHĨ", 38, WHITE, alpha=k1)
        ctext(d, 830, "Quay đều, đếm " + str(CHOT_DEM) + " lần LED đỏ chớp.\nNam châm quay mấy vòng?", 46, INK,
              maxw=940, alpha=appear(t, M[0] + 0.4, 0.5))
        ka = appear(t, M[0] + 0.6, 0.5) * k1
        y = 1080
        d.line([(300, y), (500, y)], fill=A(NAVY, ka), width=5); d.line([(580, y), (780, y)], fill=A(NAVY, ka), width=5)
        tri = [(512, y - 30), (512, y + 30), (566, y)]
        d.polygon(tri, fill=A(mix(RED, WHITE, 0.2), ka), outline=A(NAVY, ka)); d.line([(568, y - 30), (568, y + 30)], fill=A(NAVY, ka), width=6)
        text(d, (860, y), "?", 72, PURPLE, alpha=ka)
        kh = appear(t, M[0] + 2.9, 0.5)
        card(d, (110, 1260, 970, 1500), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1380, "Mỗi vòng, LED đỏ chớp mấy lần?", 44, ORANGE, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 410, "Đổi chiều luân phiên: dòng xoay chiều", 50, GREEN, maxw=880, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"),
            (do["t0"] + 0.4, "tap"), (do["t0"] + M[1] + 0.2, "tap"), (do["t0"] + M[2] + 0.1, "tap"),
            (da["t0"] + 0.15, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]


CLIP = dict(id="tn-l9-camung-03", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Dòng điện xoay chiều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nam châm quay, hai LED", draw=s_hook, tail=THINK_END, caps=[
   ("Nhìn từ trên xuống.", 3.0),
   ("Tự trả lời trước khi xem.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Quay nhanh.", 3.6),
   ("Quay chậm dần.", 6.0),
   ("Chậm hơn nữa.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Hai đèn không cùng sáng.", 3.6),
   ("Đó là dòng điện xoay chiều.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Có đúng không?", 4.4),
   ("Chưa nói được.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.2, caps=[
   ("Tự trả lời trước khi xem.", 6.4)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch vật lí:", _kiem_vat_li() or "không")
