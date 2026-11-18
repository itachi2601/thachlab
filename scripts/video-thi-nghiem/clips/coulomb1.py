# Clip: tn-l11-coulomb-01 - Thuoc nhua co toc: hut giay vun va lan lon nhom (lo L11, 18/11/2026)
# So lieu: thi nghiem DINH TINH (kho: "khong co so do") -> clip khong co con so. so_lieu_mau 3 hang
#   (Giay vun: bay len bam thuoc ; Lon nhom: lan ve phia thuoc ; Thuoc chua co: khong hut) hien nguyen van (_kiem_so()).
#   Mui ten luc hai dau lon chi dinh tinh (mo_hinh: F_hut ~ 1/d^2 - 1/(d+D)^2 > 0, kho khong co D) -> khong ghi so.
# Dau dien tich: kho (sua 18/11 theo cong B) ghi thuoc nhua co toc nhiem AM ; clip ve thuoc TRON (khong dau) o hook/
#   tien hanh/doi chung, chi canh Rut ra moi ve (-) kem "giả sử thước (−)" ; "Chua noi duoc": chi thay hut thi chua
#   biet thuoc dau gi (vat trung hoa bi hut boi ca hai dau). Assert: dau gan trai dau thuoc, luc dau gan huong VE
#   thuoc va lon hon luc dau xa (huong RA xa).
# Lon nhom nam ngang, nhin tu dau lon (hinh tron) ; thuoc tien tu ben phai roi DUNG YEN ; lon lan toi sat, dung lai
#   cach thuoc >= 30 px (assert moi 0,05 s) ; thuoc nam trong the (x <= 1040).
# Du doan (K10: chi cau hoi + hinh): thuoc da co dua lai gan (khong cham) lon nhom trung hoa -> lon? Dap an: lan ve
#   phia thuoc. Khong trung cau Tu kiem tra muc 1 (tl35-q1: thanh thuy tinh co lua nhiem duong vi sao).
# Thu tu: Ket qua (dap an + doi chung + BAY "phai cham moi nhiem dien", bac bang chinh hinh vua chieu) -> Rut ra
#   (huong ung) + Chua noi duoc -> Chot. Bay dung TRUOC Rut ra. Thu nghi = kho quan_sat[2] (dua thuoc ra xa thi lon
#   trung hoa lai) - clip CHUA chieu canh nay.
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
HAIR = (70, 50, 40); DRED = (185, 28, 28); DGREEN = (10, 80, 40)

TY = 900                       # mat ban
CR = 105                       # ban kinh lon (nhin tu dau lon)
RH = 44                        # be day thuoc

def table_top(d):
    d.rectangle([40, TY, 1040, TY + 34], fill=TABLE); d.line([(40, TY), (1040, TY)], fill=TABLE_D, width=4)

def ruler(d, xtip, y, ang=0.0, charged=True, alpha=1.0, length=560):
    """Thuoc: dau trai (xtip, y), keo dai sang phai, nghieng ang (rad, duong = dau phai nang len)."""
    c, s = math.cos(ang), math.sin(ang)
    p = lambda u, v: (xtip + u * c + v * s, y - u * s + v * c)
    poly = [p(0, -RH / 2), p(length, -RH / 2), p(length, RH / 2), p(0, RH / 2)]
    d.polygon(poly, fill=A(RULER, alpha)); d.line(poly + [poly[0]], fill=A(RULER_D, alpha), width=3)
    for k in range(1, 12):
        q0, q1 = p(k * 45, -RH / 2), p(k * 45, -RH / 2 + (14 if k % 2 else 22))
        d.line([q0, q1], fill=A(RULER_D, alpha), width=2)
    if charged:
        for k in range(4):
            q = p(40 + k * 62, 2); text(d, q, "−", 44, DRED, alpha=alpha)

def can(d, cx, charges=0.0, roll=0.0):
    cy = TY - CR
    dot(d, cx, cy, CR, ALU, outline=ALU_D)
    dot(d, cx, cy, CR - 26, (222, 226, 236))
    a = roll / CR                                   # vach quay theo lan
    d.line([(cx, cy), (cx + (CR - 10) * math.cos(a - math.pi / 2), cy + (CR - 10) * math.sin(a - math.pi / 2))],
           fill=ALU_D, width=5)
    if charges > 0:                                  # dau gan (phai, sat thuoc) trai dau thuoc ; dau xa cung dau thuoc
        for j, dy in enumerate((-50, 0, 50)):
            text(d, (cx + CR - 30 + (0 if j != 1 else 8), cy + dy), "+", 46, BLUE, alpha=charges)
            text(d, (cx - CR + 30 - (0 if j != 1 else 8), cy + dy), "−", 46, DRED, alpha=charges)

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
    text(d, (x + 80, y - 80), "tóc khô", 40, INK)

# ---------------- canh 1: Du doan ----------------
CX0 = 470                                            # tam lon ban dau
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 980), fill=WHITE, outline=LIGHT, w=3)
    table_top(d)
    can(d, CX0)
    text(d, (CX0, TY - 2 * CR - 40), "lon nhôm", 40, INK)
    if t < M[1] - 0.3:                                # co thuoc vao toc (qua lai)
        hair(d, 600, 420)
        sw = math.sin(t * 7) * 60
        ruler(d, 560 + sw, 470, charged=False, length=400)
    else:
        k = appear(t, M[1] - 0.3, 0.8)
        ruler(d, lerp(800, CX0 + CR + 70, k), TY - CR, charged=False, length=360)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Thước đã cọ lại gần lon nhôm,", "không chạm. Lon sẽ thế nào?")):
        text(d, (W / 2, y0 + 190 + j * 80), s, 48, INK, alpha=a)
    text(d, (W / 2, y0 + 440), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 505, 940, y0 + 519], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 505, 140 + 800 * (1 - p), y0 + 519], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
GAP = 70                       # khe thuoc - lon o hinh Rut ra
RX2, RL2 = 760, 260            # thuoc dung yen o pha 2 (dau trai x 760, het o 1020)
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
        text(d, (260, TY + 57), "giấy vụn", 40, INK)
        can(d, 860)
    else:
        can(d, cx, roll=roll)
        ruler(d, rx, ry, charged=False, length=RL2, alpha=appear(t - M[1], 0.0, 0.6))
        papers(d, 1, ry, rx)
        if roll > 0:
            arrow(d, (cx - 40, TY - 2 * CR - 40), (cx + 60, TY - 2 * CR - 40), ORANGE, w=6, head=20)
            text(d, (cx + 10, TY - 2 * CR - 90), "lăn", 40, ORANGE)
    # bang ket qua (hang hien sau su kien)
    n = 0
    if ph == 1 and kp >= 1: n = 1
    if ph == 2: n = 1 + (1 if roll > 0.8 * ROLL_MAX else 0)
    obs_table(d, 1020, n)

def obs_table(d, y, n, hl=-1, alpha=1.0):
    card(d, (40, y, 1040, y + 110 + 3 * 86), fill=A(WHITE, alpha), outline=A(NAVY, alpha), w=4)
    text(d, (250, y + 52), "Vật", 42, INK, alpha=alpha); text(d, (720, y + 52), "Hiện tượng", 42, INK, alpha=alpha)
    d.line([(70, y + 95), (1010, y + 95)], fill=A(LIGHT, alpha), width=4)
    for i in range(n):
        yy = y + 145 + i * 86
        if i == hl: card(d, (60, yy - 38, 1020, yy + 38), fill=A((255, 237, 213), alpha), r=16)
        text(d, (250, yy), ROWS[i][0], 42, INK, alpha=alpha)
        text(d, (720, yy), ROWS[i][1], 42, BLUE if i < 2 else MUTED, alpha=alpha)

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

# ---------------- canh 3: Dap an + Rut ra (huong ung) ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# luc len hai dau lon (dinh tinh): dau gan (+) bi thuoc (-) HUT -> huong ve thuoc (+x) ; dau xa (-) bi DAY -> -x.
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
    dot(d, cx, cy, CR, A(ALU, k), outline=A(ALU_D, k)); dot(d, cx, cy, CR - 26, A((222, 226, 236), k))
    for j, dy in enumerate((-50, 0, 50)):
        text(d, (cx + CR - 30 + (8 if j == 1 else 0), cy + dy), "+", 46, BLUE, alpha=k)
        text(d, (cx - CR + 30 - (8 if j == 1 else 0), cy + dy), "−", 46, DRED, alpha=k)
    ruler(d, cx + CR + GAP, cy, alpha=k, length=330)
    text(d, (cx + CR + GAP + 165, cy - 70), "giả sử thước (−)", 36, MUTED, alpha=k)
    if kf > 0:
        yn = cy + CR + 50
        arrow(d, (cx + CR - 10, yn), (cx + CR - 10 + L_NEAR * kf, yn), A(BLUE, kf), w=8, head=22)
        arrow(d, (cx - CR + 10, yn), (cx - CR + 10 - L_FAR * kf, yn), A(DRED, kf), w=8, head=22)
        text(d, (cx + CR + 90, yn + 50), "hút mạnh", 40, BLUE, alpha=kf)
        text(d, (cx - CR - 30, yn + 50), "đẩy yếu", 40, DRED, alpha=kf)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN · Lăn về phía thước", 320, ka)
    kc = appear(t, M[0] + 0.5, 0.45)                 # doi chung: thuoc CHUA co, giay nam yen
    card(d, (40, 390, 1040, 770), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([60, 720, 1020, 748], fill=TABLE)
    ruler(d, 140, 560, charged=False, length=560)
    for i, (x, ph) in enumerate(PAPERS):
        pp = [(x - 19, 700), (x + 19, 700), (x + 19, 719), (x - 19, 719)]
        d.polygon(pp, fill=PAPER); d.line(pp + [pp[0]], fill=PAPER_D, width=3)
    if kc > 0:
        card(d, (300, 420, 1000, 500), fill=A(WHITE, kc), outline=A(MUTED, kc), r=20, w=3)
        text(d, (650, 460), "Thước chưa cọ: không hút", 42, MUTED, alpha=kc)
    a1 = appear(t, M[1] - 0.1, 0.45)                # BAY: dung TRUOC canh Rut ra
    if a1 > 0:
        y = 810 + (1 - a1) * 20
        card(d, (40, y, 1040, y + 420), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[1] - 1.2) / 0.4)
        for j, q in enumerate(("“Phải chạm thước,", "lon mới nhiễm điện”")):
            f = F(48); lw = tw(d, q, f); yy = y + 160 + j * 76
            text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)],
                       fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 350), "✓ Không chạm vẫn lăn", 44, DGREEN, alpha=a1 * appear(t, M[1] + 1.8, 0.4))

# ---------------- canh 4: Rut ra (huong ung) + chua noi duoc ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    kr = appear(t, 0.1, 0.45)
    card(d, (40, 270, 1040, 960), fill=A((255, 247, 237), kr), outline=A(ORANGE, kr), w=5)
    pw = tw(d, "RÚT RA", F(40)) + 52
    card(d, (W / 2 - pw / 2, 296, W / 2 + pw / 2, 360), fill=A(ORANGE, kr), r=32)
    text(d, (W / 2, 328), "RÚT RA", 40, WHITE, alpha=kr)
    text(d, (W / 2, 420), "Lon nhiễm điện do hưởng ứng", 46, INK, alpha=kr)
    induction(d, 330, 620, kr, appear(t, 1.2, 0.5))
    k3 = appear(t, M[1] - 0.1, 0.45)
    if k3 > 0:
        y = 1000 + (1 - k3) * 20
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        text(d, (W / 2, y + 200), "Chỉ thấy hút: thước dấu gì?", 48, INK, alpha=k3 * appear(t, M[1] + 0.3, 0.4))

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: dua thuoc ra xa, lon con nhiem dien? (kho: trung hoa lai) ; goi y tre."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Vật trung hoà vẫn bị hút", 50, DGREEN, alpha=k0)
    text(d, (W / 2, 450), "nhờ hưởng ứng", 50, DGREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Đưa thước ra thật xa lon.", "Lon còn nhiễm điện không?")):
        text(d, (W / 2, 800 + j * 80), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1100, 970, 1360), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1160), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1270), "Electron trong lon dời đi đâu?", 46, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, rr, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + 1.5, "tap"), (do["t0"] + do["M"][1] + 1.3, "tap")]
            + [(da["t0"] + 0.1, "ding"), (da["t0"] + da["M"][1] + 1.2, "buzz"), (rr["t0"] + 0.1, "tap"),
               (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l11-coulomb-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Lực Coulomb · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Thước nhựa và lon nhôm", draw=s_hook, tail=0.3, caps=[
   ("Cọ thước nhựa vào tóc.", 3.4),
   ("Tự trả lời trước khi xem.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đưa thước lại gần giấy vụn.", 4.2),
   ("Rồi lại gần lon, không chạm.", 5.6)]),
 dict(key="dapan", title="Kết quả và bẫy", draw=s_dapan, tail=0.6, caps=[
   ("Đối chứng: thước chưa cọ.", 3.2),
   ("Bẫy thường gặp.", 5.0)]),
 dict(key="rutra", title="Vì sao lon bị hút?", draw=s_rutra, tail=0.6, caps=[
   ("Đầu gần ở gần thước hơn.", 5.0),
   ("Câu còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 7.0)]),
])

_b = _kiem_dong_bo(); assert not _b, _b

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
