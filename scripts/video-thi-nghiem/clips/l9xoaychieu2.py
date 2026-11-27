# Clip: tn-l9-xoaychieu-02 - Den 6 V - 3 W voi nguon mot chieu va nguon xoay chieu cung 6 V; von ke hai dau den (KHTN 9, bai 93)
# Vong 2 (18/11/2026, theo cong B): Du doan KHONG hoi den/so chi ampe ke (bai noi san) ma hoi VON KE XOAY CHIEU hai dau den:
#   "nho hon 6 V, dung 6 V hay lon hon?" -> 6 V (so chi la gia tri hieu dung; khong giai cong thuc).
#   So lieu: so_lieu_mau (Lan, I mot chieu, I xoay chieu): 0,50/0,49 ; 0,49/0,50 ; 0,50/0,50 A; von ke 6,0/6,0 V ghi trong
#   so_lieu_mau.ghi_chu cua kho (minh hoa, bo qua dien tro ampe ke, day noi = mo_hinh.gia_thiet[1]). Ampe ke GHD 1 A, DCNN 0,01 A.
# Tranh Cau 4 (chenh 0,01 A): khong noi chenh/sai so/trung binh; bay KHONG la "den toi hon" (nhieu A) ma la
#   (vong 3) "6 V~ la luc nao cung dung 6 V", dat TRUOC Rut ra.
# Tranh Cau 6: khong mac ampe ke mot chieu vao mach xoay chieu, bo the "moi loai nguon, mot loai ampe ke".
# Hook chi co ampe ke/von ke MOT chieu, K mo; dung cu xoay chieu chi hien khi doi nguon.
# Cau chot: nguon 9 V~ (minh hoa, ghi kho) -> den 6 V - 3 W the nao? (sang hon dinh muc, de chay). Goi y khong neu dap an.
import math
from engine import *

U, P_DM = 6, 3                                  # tham_so
DC = [0.50, 0.49, 0.50]; AC = [0.49, 0.50, 0.50]   # so_lieu_mau
UV_DC, UV_AC = 6.0, 6.0                         # so_lieu_mau.ghi_chu (minh hoa)
R_A = 0.0                                       # mo_hinh.gia_thiet[1]: bo qua dien tro ampe ke, day noi
U_HOI = 9                                       # cau chot (minh hoa, ghi trong so_lieu_mau.ghi_chu)
I_MAX, DCNN = 1.0, 0.01
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
WIRE = (60, 66, 92); DRED = (185, 28, 28); DGREEN = (21, 110, 55); GLOW = (253, 224, 71)

# ---------------- hinh ----------------
XL, XR, TY, BY, LX, AY, KT, KB = 110, 530, 380, 700, 320, 540, 470, 560
VY = 500                                        # von ke song song den, ben trong vong mach
def lamp(d, x, y, on, a=1.0, r=46):
    if on > 0:
        for k in range(6, 0, -1):
            rr = r + k * 10 * on
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=A(GLOW, a * on * 0.10))
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(mix(WHITE, GLOW, on), a), outline=A(NAVY, a), width=5)
    d.line([(x - 22, y + 10), (x - 10, y - 12), (x, y + 10), (x + 10, y - 12), (x + 22, y + 10)],
           fill=A(ORANGE if on else MUTED, a), width=4)

def vmeter(d, cx, cy, ac, a=1.0, r=46):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(WHITE, a), outline=A(PURPLE, a), width=6)
    text(d, (cx, cy + 2), "V", 54, PURPLE, alpha=a)
    if ac: text(d, (cx + r + 24, cy - r * 0.6), "~", 58, PURPLE, alpha=a)

def circuit(d, ac, closed, vtxt, sa=1.0):
    w = 6
    d.line([(XL, AY - 44), (XL, TY), (LX - 46, TY)], fill=WIRE, width=w, joint="curve")
    d.line([(LX + 46, TY), (XR, TY), (XR, KT)], fill=WIRE, width=w, joint="curve")
    d.line([(XR, KB), (XR, BY), (420, BY)], fill=WIRE, width=w, joint="curve")
    d.line([(220, BY), (XL, BY), (XL, AY + 44)], fill=WIRE, width=w, joint="curve")
    # von ke song song den
    d.line([(LX - 90, TY), (LX - 90, VY), (LX - 40, VY)], fill=WIRE, width=5, joint="curve")
    d.line([(LX + 90, TY), (LX + 90, VY), (LX + 40, VY)], fill=WIRE, width=5, joint="curve")
    dot(d, LX - 90, TY, 9, WIRE); dot(d, LX + 90, TY, 9, WIRE)
    vmeter(d, LX, VY, ac)
    text(d, (LX, VY + 82), vtxt, 56, PURPLE if vtxt[0] != "…" else MUTED)
    lamp(d, LX, TY, 1.0 if closed else 0.0)
    text(d, (LX, 300), "đèn 6 V – 3 W", 56, INK)
    d.ellipse([XL - 46, AY - 46, XL + 46, AY + 46], fill=WHITE, outline=BLUE, width=6); text(d, (XL, AY + 2), "A", 54, BLUE)
    dot(d, XR, KT, 9, WIRE); dot(d, XR, KB, 9, WIRE)
    if closed: d.line([(XR, KB), (XR, KT)], fill=NAVY, width=7)
    else: d.line([(XR, KB), (XR - 52, KT + 14)], fill=NAVY, width=7)
    text(d, (XR + 36, (KT + KB) / 2), "K", 58, NAVY)
    card(d, (220, 650, 420, 750), fill=(245, 243, 255), outline=NAVY, r=16, w=4)
    text(d, (320, 700), "6 V ~" if ac else "6 V", 56, mix(BG, ORANGE, sa))
    if not ac:
        text(d, (196, 655), "+", 56, mix(BG, ORANGE, sa)); text(d, (446, 655), "−", 56, mix(BG, ORANGE, sa))

def ang(v): return math.radians(200 + 140 * clamp(v / I_MAX))
def dial(d, cx, cy, r, v, txt, alpha=1.0):
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340, fill=A(NAVY, alpha), width=5)
    for k in range(21):
        a = ang(k * 0.05); L = 30 if k % 10 == 0 else (20 if k % 2 == 0 else 12)
        d.line([(cx + r * math.cos(a), cy + r * math.sin(a)), (cx + (r - L) * math.cos(a), cy + (r - L) * math.sin(a))],
               fill=A(NAVY, alpha), width=4 if k % 2 == 0 else 3)
    for lv in (0, 0.5, 1.0):
        a = ang(lv); s = "0" if lv == 0 else ("1" if lv == 1 else "0,5")
        text(d, (cx + (r - 66) * math.cos(a), cy + (r - 66) * math.sin(a)), s, 60, NAVY, alpha=alpha)
    a = ang(v)
    d.line([(cx, cy), (cx + (r - 18) * math.cos(a), cy + (r - 18) * math.sin(a))], fill=A(RED, alpha), width=7)
    dot(d, cx, cy, 13, A(NAVY, alpha))
    if txt: text(d, (cx, cy + 54), txt, 56, RED if txt[0] != "…" else MUTED, alpha=alpha)

def top(d, ac, closed, needle, txt, vtxt, sa=1.0, amp=True):
    card(d, (40, 260, 1040, 780), fill=WHITE, outline=LIGHT, w=3)
    circuit(d, ac, closed, vtxt, sa)
    if not amp: return
    card(d, (590, 290, 1020, 760), fill=(248, 250, 255), outline=LIGHT, r=24, w=3)
    text(d, (805, 336), "ampe kế", 56, BLUE)
    text(d, (805, 400), "xoay chiều" if ac else "một chiều", 56, mix(BG, NAVY, sa))
    dial(d, 805, 650, 190, needle, txt)

XS = (170, 470, 830)
def table(d, ndc, nac, hl=None, y=810, alpha=1.0, vdc=None, vac=None):
    vdc = ndc > 0 if vdc is None else vdc; vac = nac > 0 if vac is None else vac
    card(d, (40, y, 1040, y + 540), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, h in zip(XS, ("Lần", "Một chiều", "Xoay chiều")): text(d, (x, y + 52), h, 56, INK, alpha=alpha)
    d.line([(70, y + 96), (1010, y + 96)], fill=A(LIGHT, alpha), width=3)
    for j in range(3):
        yy = y + 160 + j * 95
        text(d, (XS[0], yy), str(j + 1), 56, NAVY, alpha=alpha)
        for col, n, vals, c in ((1, ndc, DC, NAVY), (2, nac, AC, ORANGE)):
            if hl == (col, j): d.rounded_rectangle([XS[col] - 130, yy - 40, XS[col] + 130, yy + 40], radius=18, fill=A((255, 237, 213), alpha))
            if j < n: text(d, (XS[col], yy), vn(vals[j]) + " A", 56, c, alpha=alpha)          # o trong de trong (kiem-v1 muc 5)
    yy = y + 160 + 3 * 95 + 10
    d.line([(70, yy - 52), (1010, yy - 52)], fill=A(LIGHT, alpha), width=3)
    text(d, (XS[0], yy), "Vôn kế", 56, PURPLE, alpha=alpha)
    for col, n, v in ((1, vdc, UV_DC), (2, vac, UV_AC)):
        if n: text(d, (XS[col], yy), vn(v, 1) + " V", 56, PURPLE, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.3


def pill(d, s, y, a, color=NAVY, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_hook(img, d, t, sc):
    M = sc["M"]
    top(d, True, False, 0.0, "0,00 A", "0,0 V", amp=False)        # hook ve nguon xoay chieu, khong cuc +/− (kiem-v1 muc 2)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 840 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 170), f"Nguồn xoay chiều {U} V.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 260), "Vôn kế chỉ bao nhiêu?", 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 350, 970, y0 + 450], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 350, 110 + max(90, 860 * (1 - p)), y0 + 450], radius=45, fill=A((76, 29, 149), a))


# ---------------- canh 2: Tien hanh ----------------
T_C1, T_O1, T_SW, T_C2 = 0.8, 4.2, 5.0, 5.5
READ = [1.4, 2.4, 3.4]; READ2 = [6.0, 7.0, 8.0]
T_N = 0.35
T_V1, T_V2 = T_C1 + T_N + 0.7, T_C2 + T_N + 0.7      # hang von ke ghi sau khi so V hien 0,7 s
def do_state(t):
    """-> (ac?, alpha doi nguon, K dong?, kim, chu ampe ke, chu von ke, so o mot chieu, so o xoay chieu, o dang to)."""
    ac = t >= T_SW; sa = clamp((t - T_SW) / 0.3) if ac else 1.0
    closed = (T_C1 <= t < T_O1) or t >= T_C2
    vals, reads, tc = (AC, READ2, T_C2) if ac else (DC, READ, T_C1)
    k = sum(1 for r in reads if t >= r)
    if not closed:
        prev = DC[-1]; nd = prev * (1 - ease((t - T_O1) / T_N)) if t >= T_O1 else 0.0
        return ac, sa, False, nd, ("0,00 A" if nd < 0.003 else "…"), "0,0 V", 3 if t >= T_O1 else 0, 0, None
    tgt = vals[max(k - 1, 0)]
    if k == 0: nd = tgt * ease((t - tc) / T_N)
    else:
        ts = reads[k - 1]; prev = vals[k - 2] if k >= 2 else vals[0]; nd = lerp(prev, tgt, ease((t - ts) / T_N))
        if k == 1: nd = tgt
    txt = vn(tgt) + " A" if abs(nd - tgt) < 0.002 and (k > 0 or t - tc > T_N) else "…"
    vtxt = vn(UV_AC if ac else UV_DC, 1) + " V" if t - tc > T_N else "…"
    ndc = 3 if ac else sum(1 for r in READ if t >= r + T_N)
    nac = sum(1 for r in READ2 if t >= r + T_N) if ac else 0
    hl = (2, nac - 1) if ac and nac else ((1, ndc - 1) if not ac and ndc else None)
    return ac, sa, True, nd, txt, vtxt, ndc, nac, hl

def s_do(img, d, t, sc):
    ac, sa, closed, nd, txt, vtxt, ndc, nac, hl = do_state(t)
    top(d, ac, closed, nd, txt, vtxt, sa)
    table(d, ndc, nac, hl, vdc=t >= T_V1, vac=t >= T_V2)

def _kiem_dong_bo():
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        ac, sa, closed, nd, txt, vtxt, ndc, nac, hl = do_state(t)
        if txt not in ("…", "0,00 A") and abs(float(txt[:-2].replace(",", ".")) - nd) > 0.003: bad.append((round(t, 2), "chu lech kim", txt, nd))
        if closed and not ac and ndc and txt != "…" and txt != vn(DC[ndc - 1]) + " A" and t < READ[min(ndc, 2)]:
            bad.append((round(t, 2), "bang DC lech so chi", ndc, txt))
        if closed and ac and nac and txt != "…" and txt != vn(AC[nac - 1]) + " A" and (nac == 3 or t < READ2[nac]):
            bad.append((round(t, 2), "bang AC lech so chi", nac, txt))
        if not closed and (txt not in ("…", "0,00 A") or vtxt != "0,0 V"): bad.append((round(t, 2), "K mo ma co so"))
        if (t >= T_V2 and (not ac or vtxt == "…")) or (T_V1 <= t < T_O1 and vtxt == "…"): bad.append((round(t, 2), "bang co U truoc von ke"))
        t += 0.05
    return bad

def _kiem_so():
    bad = []
    if abs(P_DM / U - 0.50) > 1e-9: bad.append("I = P/U khac 0,50")
    for v in DC + AC:
        if abs(v - P_DM / U) > DCNN + 1e-9: bad.append(("lech qua 1 do chia", v))
        if v > I_MAX: bad.append(("qua GHD", v))
    for uv, I in ((UV_DC, P_DM / U), (UV_AC, P_DM / U)):          # von ke chi U hieu dung hai dau den = U - I*R_A
        if abs(uv - (U - I * R_A)) > 1e-9: bad.append(("von ke", uv))
    if not U_HOI > U: bad.append("cau chot phai lon hon U dinh muc")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, f"ĐÁP ÁN: đúng {U} V", 305, ka)
    for x0, nm, uv in ((40, "một chiều", UV_DC), (560, "xoay chiều", UV_AC)):
        card(d, (x0, 370, x0 + 480, 1080), fill=A(WHITE, ka), outline=A(TEAL, ka), w=5)
        text(d, (x0 + 240, 430), nm, 58, NAVY, alpha=ka)
        vmeter(d, x0 + 240, 590, nm == "xoay chiều", a=ka, r=70)
        text(d, (x0 + 240, 730), vn(uv, 1) + " V", 60, PURPLE, alpha=ka)            # kho ghi 6,0 V (kiem-v1 muc 1)
        xs = range(x0 + 50, x0 + 431, 4)              # dang u(t): mot chieu phang, xoay chieu chay ngang
        if nm == "một chiều": d.line([(x0 + 50, 800), (x0 + 430, 800)], fill=A(ORANGE, ka), width=6)
        else: d.line([(x, 800 - 30 * math.sin(2 * math.pi * ((x - x0) / 130 - t / 1.2))) for x in xs], fill=A(ORANGE, ka), width=6)
        kb = appear(t, M[1] - 0.1, 0.4) * ka
        if kb > 0: lamp(d, x0 + 240, 960, kb * (0.85 + 0.15 * math.sin(2 * math.pi * t / 1.2)), a=kb, r=60)
    k1 = appear(t, M[1] + 0.3, 0.45)
    if k1 > 0:
        card(d, (40, 1120, 1040, 1280), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1200), "Nóng, sáng như một chiều", 58, DGREEN, alpha=k1)

# ---------------- canh 4: Bay + Chua noi duoc ----------------
BAY_ST, BAY_OK = 2.0, 2.6
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    vmeter(d, 300, 410, True, r=70)
    xs = range(470, 981, 4)                        # u(t) xoay chieu chay ngang (chi minh hoa dang song)
    d.line([(470, 410), (980, 410)], fill=GRAY, width=3)
    text(d, (450, 410), "0", 56, NAVY, anchor="rm")                    # duong 0 co nhan (kiem-v1 muc 3)
    text(d, (280, 522), "u đổi liên tục", 56, ORANGE, alpha=appear(t, 0.2, 0.45))
    d.line([(x, 410 - 90 * math.sin(2 * math.pi * ((x - 470) / 170 - t / 1.5))) for x in xs], fill=ORANGE, width=6)
    k2 = appear(t, M[1] + 0.3, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    y0 = 600
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        ks = clamp((t - BAY_ST) / 0.4)
        for j, q in enumerate((f"“{U} V~ là lúc nào", f"cũng đúng {U} V”")):
            yy = y0 + 180 + j * 85; lw = tw(d, q, F(58))
            text(d, (W / 2, yy), q, 58, INK, alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, BAY_OK, 0.4)
        card(d, (70, y0 + 340, 1010, y0 + 590), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 420), "✓ Luôn đổi;", 58, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 505), f"{U} V là hiệu dụng", 58, DGREEN, alpha=kk)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 340), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "giá trị lớn nhất của u", 58, INK, alpha=k2)

# ---------------- canh 5: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), f"{U} V~ là giá trị hiệu dụng", 58, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 518, k1, ORANGE)
    text(d, (W / 2, 625), f"Nguồn {U_HOI} V xoay chiều.", 60, INK, alpha=k1)
    text(d, (W / 2, 705), f"Đèn {U} V – {P_DM} W thế nào?", 60, INK, alpha=k1)
    if k1 > 0:   # song u(t) chay ngang + den chua sang; KHONG ve den sang
        lamp(d, 300, 1000, 0.0, a=k1, r=70)
        xs = range(470, 981, 4)
        d.line([(470, 1000), (980, 1000)], fill=A(LIGHT, k1), width=3)
        d.line([(x, 1000 - 110 * math.sin(2 * math.pi * ((x - 470) / 170 - t / 1.5))) for x in xs], fill=A(ORANGE, k1), width=6)
        text(d, (720, 1200), f"{U_HOI} V ~", 60, ORANGE, alpha=k1)
        text(d, (300, 1200), "?", 64, PURPLE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
          (do["t0"] + T_C1, "tap"), (do["t0"] + T_C2, "tap"),
          (da["t0"] + 0.15, "ding"), (b["t0"] + BAY_ST, "buzz"), (b["t0"] + BAY_OK, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return sorted(cs)

CLIP = dict(id="tn-l9-xoaychieu-02", header="KHTN 9 · THÍ NGHIỆM", footer="Dòng điện xoay chiều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Một đèn, hai loại nguồn", draw=s_hook, tail=THINK_END, caps=[
   ("Vôn kế mắc hai đầu đèn.", 3.4),
   ("Dừng lại, tự đoán.", 5.5)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Một chiều: đọc 3 lần.", 4.4),
   ("Đổi sang xoay chiều, đọc 3 lần.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Vôn kế chỉ như nhau.", 3.0),
   ("Đèn sáng, nóng như nhau.", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 5.0),
   ("Còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự nghĩ.", 7.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
