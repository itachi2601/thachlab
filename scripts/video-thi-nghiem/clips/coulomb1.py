# Clip: tn-l11-coulomb-01 - Thuoc nhua co toc: hut giay vun va lan lon nhom (ban 2 cong moi, 27/11/2026)
# So lieu: thi nghiem DINH TINH (kho: "khong co so do") -> clip khong co con so. so_lieu_mau 3 hang
#   (Giay vun: bay len bam thuoc ; Lon nhom: lan ve phia thuoc ; Thuoc chua co: khong hut) hien nguyen van (_kiem_so()).
#   Mui ten luc hai dau lon chi dinh tinh (mo_hinh: F_hut ~ 1/d^2 - 1/(d+D)^2 > 0, kho khong co D) -> khong ghi so.
# Dau dien tich: kho ghi thuoc nhua co toc nhiem AM ; clip ve thuoc TRON (khong dau) o hook/tien hanh/doi chung, chi
#   canh Rut ra moi ve (-) kem "giả sử (−)" ; "Chua noi duoc": chi thay hut thi chua biet thuoc dau gi (vat trung hoa
#   bi hut boi ca hai dau). Assert: dau gan trai dau thuoc, luc dau gan huong VE thuoc va lon hon luc dau xa.
# Lon nhom nam ngang, nhin tu dau lon (hinh tron) ; thuoc tien tu ben phai roi DUNG YEN ; lon lan toi sat, dung lai
#   cach thuoc >= 30 px (assert moi 0,05 s) ; thuoc nam trong the (x <= 1040).
# Du doan (K10: chi cau hoi + hinh, khong nut A-D): thuoc da co dua lai gan (khong cham) lon nhom trung hoa -> lon?
#   Dap an: lan ve phia thuoc. Khong trung cau Tu kiem tra (quiz mo bai: dien giat o sieu thi tu dau).
# Thu tu: Ket qua (dap an + doi chung + BAY "phai cham moi nhiem dien", bac bang hinh khe ho) -> Rut ra (huong ung)
#   + Chua noi duoc -> THU NGHI = kho quan_sat[2] (dua thuoc ra xa thi lon trung hoa lai) - clip CHUA chieu canh nay;
#   hinh chi ve lon + "?" (khong ve dau dien tich) de khong lo dap an.
# Cong moi 27/11: chu than canh >= 56 (ra >= 49 px), moi canh <= 180 tu/phut, khoi chu cach >= 2 s, thanh dem 5 o 70 px.
from engine import *

ROWS = [("Giấy vụn", "bay lên bám thước"), ("Lon nhôm", "lăn về phía thước"), ("Thước chưa cọ", "không hút")]

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-coulomb-01.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    assert "trung hoà lại" in k["cac_buoc"]["quan_sat"][2]
_kiem_so()

RULER = (170, 205, 240); RULER_D = (70, 110, 160); ALU = (205, 210, 222); ALU_D = (120, 128, 148)
PAPER = (247, 226, 160); PAPER_D = (140, 100, 30); TABLE = (176, 124, 74); TABLE_D = (140, 96, 54)
HAIR = (70, 50, 40); DRED = (185, 28, 28); DGREEN = (10, 80, 40); EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)

TY = 900                       # mat ban
CR = 105                       # ban kinh lon (nhin tu dau lon)
RH = 48                        # be day thuoc

def table_top(d, x0=40, x1=1040, y=TY):
    d.rectangle([x0, y, x1, y + 34], fill=TABLE); d.line([(x0, y), (x1, y)], fill=TABLE_D, width=4)

def ruler(d, xtip, y, ang=0.0, charged=True, alpha=1.0, length=560):
    """Thuoc: dau trai (xtip, y), keo dai sang phai, nghieng ang (rad, duong = dau phai nang len)."""
    c, s = math.cos(ang), math.sin(ang)
    p = lambda u, v: (xtip + u * c + v * s, y - u * s + v * c)
    poly = [p(0, -RH / 2), p(length, -RH / 2), p(length, RH / 2), p(0, RH / 2)]
    d.polygon(poly, fill=A(RULER, alpha)); d.line(poly + [poly[0]], fill=A(RULER_D, alpha), width=3)
    for k in range(1, 12):
        if k * 45 > length - 12: break
        q0, q1 = p(k * 45, -RH / 2), p(k * 45, -RH / 2 + (14 if k % 2 else 22))
        d.line([q0, q1], fill=A(RULER_D, alpha), width=2)
    if charged:
        for k in range(4):
            q = p(40 + k * 70, 4); text(d, q, "−", 58, DRED, alpha=alpha)

def can(d, cx, cy=TY - CR, r=CR, charges=0.0, roll=0.0, alpha=1.0):
    dot(d, cx, cy, r, A(ALU, alpha), outline=A(ALU_D, alpha))
    dot(d, cx, cy, r - 26, A((222, 226, 236), alpha))
    a = roll / r                                    # vach quay theo lan
    d.line([(cx, cy), (cx + (r - 10) * math.cos(a - math.pi / 2), cy + (r - 10) * math.sin(a - math.pi / 2))],
           fill=A(ALU_D, alpha), width=5)
    if charges > 0:                                  # dau gan (phai, sat thuoc) trai dau thuoc ; dau xa cung dau thuoc
        for j, dy in enumerate((-52, 0, 52)):
            text(d, (cx + r - 30 + (0 if j != 1 else 8), cy + dy), "+", 58, BLUE, alpha=charges)
            text(d, (cx - r + 30 - (0 if j != 1 else 8), cy + dy), "−", 58, DRED, alpha=charges)

PAPERS = [(150, 0.0), (205, 0.5), (262, 0.2), (318, 0.8), (372, 0.35)]
def papers(d, k, ruler_y, ruler_x0):
    """k: 0 nam tren ban -> 1 da bam mat duoi thuoc."""
    for i, (x, ph) in enumerate(PAPERS):
        kk = clamp(k * 1.6 - ph * 0.6)
        y = lerp(TY - 11, ruler_y + RH / 2 + 11, ease(kk))
        xx = lerp(x, max(x, ruler_x0 + 34 + i * 48), ease(kk))
        rot = (1 - kk) * (12 if i % 2 else -10)
        w, h = 38, 20
        pp = [(xx - w / 2, y - h / 2 + rot / 3), (xx + w / 2, y - h / 2 - rot / 3),
              (xx + w / 2, y + h / 2 - rot / 3), (xx - w / 2, y + h / 2 + rot / 3)]
        d.polygon(pp, fill=PAPER); d.line(pp + [pp[0]], fill=PAPER_D, width=3)

def hair(d, x, y):
    for k in range(9):
        xx = x + k * 20
        d.arc([xx - 30, y - 50, xx + 30, y + 60], 200, 340, fill=HAIR, width=8)
    text(d, (x + 80, y - 95), "tóc khô", 56, INK)

def pill(d, s, y, a, color=NAVY, size=58, cx=W / 2):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, y - 40, cx + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (cx, y), s, size, WHITE, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o day 70 px: tat dan tung o (moi o mot lan hinh doi)."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
CX0 = 470                                            # tam lon ban dau
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 980), fill=WHITE, outline=LIGHT, w=3)
    table_top(d)
    can(d, CX0)
    text(d, (CX0, TY - 2 * CR - 50), "lon nhôm", 56, INK)
    if t < M[1] - 0.3:                                # co thuoc vao toc (qua lai)
        hair(d, 600, 440)
        sw = math.sin(t * 7) * 60
        ruler(d, 560 + sw, 490, charged=False, length=360)
    else:
        k = appear(t, M[1] - 0.3, 0.8)
        ruler(d, lerp(800, CX0 + CR + 70, k), TY - CR, charged=False, length=320)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 550), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    for j, s in enumerate(("Thước đã cọ lại gần lon,", "không chạm.", "Lon sẽ thế nào?")):
        text(d, (W / 2, y0 + 175 + j * 85), s, 62, PURPLE if j == 2 else INK, alpha=a)
    seg_bar(d, y0 + 440, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
GAP = 70                       # khe thuoc - lon o hinh Rut ra
RX2, RL2 = 760, 220            # thuoc dung yen o pha 2 (dau trai x 760, het o 980)
ROLL_MAX = RX2 - 36 - CR - CX0 # lon lan toi khi khe con 36 px
def do_state(t, M):
    """-> (pha, ruler_x, ruler_y, k_giay, cx_lon, roll). Pha 1: giay vun ; pha 2: thuoc hien dan o vi tri dung yen, lon lan toi sat."""
    t2 = M[1]
    if t < t2:
        ry = lerp(560, 760, ease((t - 0.3) / 1.2))
        kp = clamp((t - 1.5) / 1.4)
        return 1, 120, ry, kp, None, 0
    tk = t - t2
    if tk < 1.3: return 2, RX2, TY - CR, 1, CX0, 0
    s = ROLL_MAX * (1 - (1 - clamp((tk - 1.3) / 2.6)) ** 2)      # nhanh dan roi cham lai, dung sat thuoc
    return 2, RX2, TY - CR, 1, CX0 + s, s

def s_do(img, d, t, sc):
    M = sc["M"]; ph, rx, ry, kp, cx, roll = do_state(t, M)
    card(d, (40, 260, 1040, 980), fill=WHITE, outline=LIGHT, w=3)
    table_top(d)
    if ph == 1:
        ruler(d, rx, ry, charged=False)
        papers(d, kp, ry, rx)
        text(d, (260, TY + 62), "giấy vụn", 56, INK)
        can(d, 860)
    else:
        can(d, cx, roll=roll)
        ruler(d, rx, ry, charged=False, length=RL2, alpha=appear(t - M[1], 0.0, 0.6))
        papers(d, 1, ry, rx)
        if roll > 0:
            arrow(d, (cx - 50, TY - 2 * CR - 40), (cx + 60, TY - 2 * CR - 40), ORANGE, w=7, head=22)
            text(d, (cx + 5, TY - 2 * CR - 100), "lăn", 56, ORANGE)
    n = 0                                             # bang ket qua (hang hien sau su kien)
    if ph == 1 and kp >= 1: n = 1
    if ph == 2: n = 1 + (1 if roll > 0.8 * ROLL_MAX else 0)
    obs_table(d, 1020, n)

def obs_table(d, y, n):
    card(d, (40, y, 1040, y + 110 + 3 * 96), fill=WHITE, outline=NAVY, w=4)
    text(d, (250, y + 55), "Vật", 56, NAVY); text(d, (720, y + 55), "Hiện tượng", 56, NAVY)
    d.line([(70, y + 100), (1010, y + 100)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 155 + i * 96
        text(d, (250, yy), ROWS[i][0], 56, INK)
        text(d, (720, yy), ROWS[i][1], 56, BLUE if i < 2 else INK)

def _kiem_dong_bo():
    """Moi 0,05 s canh Tien hanh: thuoc khong bao gio cham lon ; hang bang chi hien sau su kien."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; M = sc["M"]; t = 0.0; bad = []
    while t < sc["T"]:
        ph, rx, ry, kp, cx, roll = do_state(t, M)
        if ph == 2 and rx - (cx + CR) < 30: bad.append((round(t, 2), "khe < 30 px"))
        if ph == 2 and rx + RL2 > 1040: bad.append((round(t, 2), "thuoc ra mep"))
        if ph == 1 and rx + 560 > 1040: bad.append((round(t, 2), "thuoc ra mep"))
        t += 0.05
    if do_state(M[1] - 0.05, M)[3] < 1: bad.append("giay chua bam het truoc pha 2")
    return bad

# ---------------- canh 3: Dap an + doi chung + Bay ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN: lăn về phía thước", 320, ka)
    card(d, (40, 390, 1040, 780), fill=WHITE, outline=LIGHT, w=3)       # doi chung: thuoc CHUA co, giay + lon nam yen
    d.rectangle([60, 730, 1020, 758], fill=TABLE)
    ruler(d, 140, 560, charged=False, length=560)
    for i, (x, ph) in enumerate(PAPERS):
        pp = [(x - 19, 710), (x + 19, 710), (x + 19, 729), (x - 19, 729)]
        d.polygon(pp, fill=PAPER); d.line(pp + [pp[0]], fill=PAPER_D, width=3)
    can(d, 830, 730 - 75, 75)                       # lon nam yen canh dau thuoc (khe 55 px)
    text(d, (400, 470), "thước chưa cọ", 56, NAVY, alpha=ka)
    text(d, (830, 470), "đều nằm yên", 56, NAVY, alpha=ka)
    a1 = appear(t, M[1] - 0.1, 0.45)                # BAY nhip 1: cau sai + hinh khe ho (lon chua lan)
    if a1 <= 0: return
    y = 810 + (1 - a1) * 20
    card(d, (40, y, 1040, y + 750), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pill(d, "BẪY", y + 62, a1, DRED)
    t2 = M[1] + 2.9                                  # nhip 2 (>= 3 s sau nhip 1): lon lan toi + gach cau sai + dau tick
    ks = clamp((t - t2) / 0.4)
    q = "“Phải chạm mới nhiễm điện”"
    f = F(60); lw = tw(d, q, f); yy = y + 175
    text(d, (W / 2, yy), q, 60, INK, alpha=a1)
    if ks > 0:
        d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=4)
    yb = y + 600
    d.rectangle([90, yb, 990, yb + 22], fill=A(TABLE, a1))
    r2 = 75; cx = 280 + 110 * ease(clamp((t - t2) / 1.6)); cy = yb - r2
    can(d, cx, cy, r2, alpha=a1)
    ruler(d, 640, cy, charged=False, length=300, alpha=a1)
    gx0, gx1 = cx + r2 + 4, 636
    if gx1 - gx0 > 30:
        arrow(d, ((gx0 + gx1) / 2, cy - r2 - 18), (gx0, cy - r2 - 18), A(DRED, a1), w=5, head=16)
        arrow(d, ((gx0 + gx1) / 2, cy - r2 - 18), (gx1, cy - r2 - 18), A(DRED, a1), w=5, head=16)
    text(d, (560, y + 330), "không chạm", 56, DRED, alpha=a1)
    kt = appear(t, t2, 0.4)
    if kt > 0:
        text(d, (W / 2, yb + 75), "✓ vẫn lăn tới", 56, DGREEN, alpha=a1 * kt)

# ---------------- canh 4: Rut ra (huong ung) + chua noi duoc ----------------
SIGN_RULER, SIGN_NEAR, SIGN_FAR = -1, +1, -1
L_NEAR, L_FAR = 190, 80
def _kiem_vat_li():
    assert SIGN_NEAR * SIGN_RULER < 0 and SIGN_FAR * SIGN_RULER > 0           # dau gan trai dau, dau xa cung dau thuoc
    dir_near = +1 if SIGN_NEAR * SIGN_RULER < 0 else -1                      # trai dau -> hut (ve phia thuoc, +x)
    dir_far = +1 if SIGN_FAR * SIGN_RULER < 0 else -1
    assert dir_near == +1 and dir_far == -1
    assert L_NEAR > L_FAR                                                     # 1/d^2 > 1/(d+D)^2
_kiem_vat_li()

def induction(d, cx, cy, k, kf):
    """Hinh Rut ra: lon (tam cx, cy) + thuoc (-) ben phai + hai mui ten luc."""
    can(d, cx, cy, charges=k, alpha=k)
    ruler(d, cx + CR + GAP, cy, alpha=k, length=330)
    text(d, (cx + CR + GAP + 165, cy - 80), "giả sử (−)", 56, INK, alpha=k)
    if kf > 0:
        yn = cy + CR + 50
        arrow(d, (cx + CR - 10, yn), (cx + CR - 10 + L_NEAR * kf, yn), A(BLUE, kf), w=9, head=24)
        arrow(d, (cx - CR + 10, yn), (cx - CR + 10 - L_FAR * kf, yn), A(DRED, kf), w=9, head=24)
        text(d, (cx + CR + 110, yn + 60), "hút mạnh", 56, BLUE, alpha=kf)
        text(d, (cx - CR - 15, yn + 60), "đẩy yếu", 56, DRED, alpha=kf)

def s_rutra(img, d, t, sc):
    M = sc["M"]
    kr = appear(t, 0.1, 0.45)
    card(d, (40, 270, 1040, 960), fill=A((255, 247, 237), kr), outline=A(ORANGE, kr), w=5)
    text(d, (W / 2, 340), "Lon nhiễm điện do hưởng ứng", 60, DORANGE, alpha=kr)
    induction(d, 300, 600, kr, appear(t, M[1], 0.5))
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y = 1000 + (1 - k3) * 20
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, "CHƯA NÓI ĐƯỢC", y + 70, k3, NAVY)
        text(d, (W / 2, y + 200), "Thước (+) hay (−)?", 62, INK, alpha=k3)

# ---------------- canh 5: THU NGHI (cau chot o khung: dua thuoc ra xa -> lon trung hoa lai) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1570), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, "THỬ NGHĨ", 305, k, ORANGE)
    yb = 740; d.rectangle([90, yb, 990, yb + 26], fill=A(TABLE, k))
    can(d, 300, yb - CR, alpha=k)
    text(d, (300, yb - CR), "?", 80, DORANGE, alpha=k)
    xr = lerp(430, 760, ease(clamp((t - 0.6) / 2.2)))              # thuoc lui dan ra xa
    ruler(d, xr, yb - CR, charged=False, length=260, alpha=k)
    arrow(d, (620, yb - 2 * CR - 40), (820, yb - 2 * CR - 40), A(ORANGE, k), w=7, head=22)
    text(d, (W / 2, 880), "Đưa thước ra thật xa.", 62, INK, alpha=k)
    text(d, (W / 2, 970), "Lon còn nhiễm điện?", 62, DORANGE, alpha=k)
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh > 0:
        card(d, (90, 1060, 990, 1200), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1130), "Gợi ý: thước đi xa, điều gì đổi?", 58, DORANGE, alpha=kh)
    seg_bar(d, 1300, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, rr, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + 1.5, "tap"), (do["t0"] + do["M"][1] + 1.3, "tap")]
            + [(da["t0"] + 0.15, "ding"), (da["t0"] + da["M"][1] - 0.1, "buzz"), (rr["t0"] + rr["M"][1], "tap"),
               (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l11-coulomb-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Lực Coulomb · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Thước nhựa và lon nhôm", draw=s_hook, tail=0.3, caps=[
   ("Cọ thước nhựa vào tóc.", 3.4),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Đưa thước lại gần giấy vụn.", 4.0),
   ("Rồi lại gần lon, không chạm.", 5.4)]),
 dict(key="dapan", title="Kết quả và bẫy", draw=s_dapan, tail=0.5, caps=[
   ("Đối chứng: không cọ thước.", 4.0),
   ("Bẫy thường gặp.", 5.6)]),
 dict(key="rutra", title="Vì sao lon bị hút?", draw=s_rutra, tail=0.6, caps=[
   ("Hai đầu lon trái dấu.", 3.0),
   ("Đầu gần sát thước hơn.", 3.4),
   ("Chỉ thấy hút: chưa đủ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự trả lời.", 7.2)]),
])

_b = _kiem_dong_bo(); assert not _b, _b

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
