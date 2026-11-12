# Clip bay phu dao L12 Ch.4 so 04 - Tan xa alpha (Rutherford): lech goc lon do luc day cua hat nhan, khong do electron.
# topic_id 221 "Ki hieu hat nhan, so nuclon, dong vi" (chu de gan nhat co trong ngan hang — chua co chu de rieng cho mo hinh
# nguyen tu Rutherford), lesson_topic 69, bai l12-hat-nhan-mo-hinh-nguyen-tu. Kieu de Bo 2025-2026 (y sai "alpha tan xa do va
# cham electron", "ket qua chung minh quy dao dung").
# TU SOAN: chua co luot lam chuong 4 trong 60 ngay toi 12/11/2026 (lop chua hoc toi).
#   "Vai hat alpha lech goc lon, bat nguoc. Nguyen nhan chinh la"  A. Luc day cua hat nhan  B. Va cham voi electron
#   C. Luc hut cua hat nhan  D. Va cham nguyen tu khac -> A (dap an dung dat o A de 4 clip ch.4 rai C, B, D, A).
# Kiem so: m_alpha = 6,64e-27 kg; m_e = 9,11e-31 kg -> ti so 6,64e-27 / 9,11e-31 = 7289 ~ 7300.
# Quy dao (canh Sai vi): tich phan so, luc day K(1/r^2 - 1/RS^2) chi trong ban kinh RS = 100 px quanh hat nhan (man chan),
#   K = 4e6, v0 = 420 px/s. In kiem (python): b = -40 px -> lech 32 do len, r_min 47 px; b = +6 px -> lech 138 do (bat
#   nguoc), r_min 26 px > ban kinh ve hat nhan 10 px (khong cham). Tia thang b = -170, -110, 110, 150, 190 px: |b| > RS
#   nen khong vao vung luc -> lech 0,00 do (in kiem). (Ban dau b = 75 lech 6,5 do -> da doi thanh 110.)
# Cong B vong 1: bo so 7300 tren man (ti so chi ghi o chu thich nay), chi noi "electron rat nhe so voi alpha".
#   Moi tia lech chi gan MOT hat nhan (chi ve mot nguyen tu). Ghi "hat nhan ve to hon that".
# Cau THU NGHI: hoi y KHONG chung minh duoc (quy dao dung cua electron) — ca khac cau tinh huong, man khong tra loi san.
from clips.bay_chung import *

QY = 830
Q_LINES = ["Vài hạt α lệch góc lớn, bật ngược.", "Nguyên nhân chính là"]
OPTS = ["Lực đẩy của hạt nhân", "Va chạm với êlectron", "Lực hút của hạt nhân", "Va chạm nguyên tử khác"]
ANS = 0
CX, CY, RS, RATOM, K, V0 = 540, 510, 100, 210, 4e6, 420
YMIN, YMAX = 215, 790


def path(b, dt=1 / 240):
    x, y = 40.0, CY + b; vx, vy = V0, 0.0; pts = [(0.0, x, y)]; t = 0.0
    while -60 < x < 1140 and 150 < y < 900 and t < 6:
        dx, dy = x - CX, y - CY; r = math.hypot(dx, dy)
        if r < RS:
            f = K * (1 / r ** 2 - 1 / RS ** 2) / r; vx += f * dx * dt; vy += f * dy * dt
        x += vx * dt; y += vy * dt; t += dt; pts.append((t, x, y))
    return pts


# (b, thoi diem phong so voi dau canh Sai vi / 'm1' = tinh tu M[1])
STRAIGHT = [-170, -110, 110, 150, 190]
P_STR = {b: path(b) for b in STRAIGHT}
P_UP, P_BACK = path(-40), path(6)
EHIT = (470, CY - 110)          # electron nam dung tren tia b = -110
ELEC = [EHIT, (660, CY - 140), (730, CY - 60), (360, CY + 50), (420, CY + 80), (620, CY + 50)]   # tranh cac tia thang
T_HIT = (EHIT[0] - 40) / V0     # thoi diem alpha (b=-110) toi electron, ke tu luc phong


def trail(d, pts, tt, color, alpha=1.0, head=True, tip=False):
    if tt <= 0: return
    seg = [(x, y) for (s, x, y) in pts if s <= tt and YMIN < y < YMAX and -20 < x < 1100]
    if len(seg) > 1: d.line(seg, fill=A(color, 0.55 * alpha), width=4, joint="curve")
    alive = seg and tt < pts[-1][0] and seg[-1] == next(((x, y) for (s, x, y) in reversed(pts) if s <= tt), None)
    if head and alive:
        x, y = seg[-1]; d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=A(ORANGE, alpha))
    elif tip and len(seg) > 8:          # tia da ra khoi khung: chevron o dau cuoi chi huong bay
        (xa, ya), (xb, yb) = seg[-8], seg[-1]
        chevron(d, xb, yb, math.atan2(yb - ya, xb - xa), A(ORANGE, alpha), s=26, w=7)


def atom(d, t, t_hit, k=1.0, ring_at=None):
    n = 72
    for i in range(0, n, 2):   # vo nguyen tu: duong tron net dut
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        d.arc([CX - RATOM, CY - RATOM, CX + RATOM, CY + RATOM], math.degrees(a0), math.degrees(a1), fill=A(GRAY, k), width=3)
    d.ellipse([CX - 10, CY - 10, CX + 10, CY + 10], fill=A(RED, k))
    d.line([(CX + 14, CY + 10), (CX + 100, CY + 44)], fill=A(RED, 0.7 * k), width=3)   # cheo xuong: khong trung tia bat nguoc
    text(d, (CX + 108, CY + 44), "hạt nhân (+)", 38, RED, anchor="lm", alpha=k)
    if ring_at is not None:             # khoanh electron sap bi alpha di qua
        kr = appear(t, ring_at, 0.3) * (1 - appear(t, t_hit + 0.2, 0.3))
        if kr > 0:
            ex, ey = EHIT; d.ellipse([ex - 26, ey - 26, ex + 26, ey + 26], outline=A(BLUE, kr), width=4)
        kl = 1 - appear(t, t_hit + 0.5, 0.4)
        text(d, (EHIT[0], EHIT[1] + 52), "êlectron", 38, BLUE, alpha=kl)
    for j, (ex, ey) in enumerate(ELEC):
        if j == 0 and t > t_hit:            # electron bi hat alpha hat ra, alpha khong doi huong
            u = t - t_hit; ex, ey = ex + 150 * u, ey - 240 * u
            if ey < YMIN + 10: continue
        d.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=A(BLUE, k))


def macro(d, t):
    """Nhin lon: nguon alpha -> la vang; da so tia di thang, mot tia lech, mot tia bat nguoc."""
    card(d, (60, 460, 200, 560), fill=A(NAVY, 1), r=12)
    text(d, (150, 600), "nguồn α", 38, INK)
    d.rectangle([592, 330, 604, 690], fill=A(GOLD, 1))
    text(d, (598, 295), "lá vàng", 40, GOLD)
    col = A(ORANGE, 0.7)
    for yy in (470, 490, 510, 530, 550):
        d.line([(200, yy), (1000, yy)], fill=col, width=4); chevron(d, 1000, yy, 0, col)
    d.line([(200, 500), (598, 500), (880, 340)], fill=col, width=4); chevron(d, 880, 340, math.atan2(-160, 282), col)
    d.line([(200, 520), (598, 520), (330, 700)], fill=col, width=4); chevron(d, 330, 700, math.atan2(180, -268), col)
    for yy, ph in ((470, 0.0), (510, 0.4), (550, 0.8)):      # hat alpha chay tren cac tia thang
        x = 200 + ((t * 300 + ph * 800) % 800); d.ellipse([x - 9, yy - 9, x + 9, yy + 9], fill=A(ORANGE, 1))


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    macro(d, t)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    macro(d, sc["t0"] + t)
    answer_pill(d, 1000, "A", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]
    t_hit = m0 + 2.0                      # alpha cham electron (electron duoc khoanh tu m0 + 0,3 -> thay ro 1,7 s)
    atom(d, t, t_hit, ring_at=m0 + 0.3)
    for i, b in enumerate(STRAIGHT):
        if b == -110: trail(d, P_STR[b], t - (t_hit - T_HIT), ORANGE)
        else: trail(d, P_STR[b], t - 0.2 - 0.15 * i, ORANGE)
    t_def = t - (m1 - 0.6)                # hai tia lech phong de toi gan hat nhan ngay sau phu de 2
    trail(d, P_UP, t_def, ORANGE, tip=True); trail(d, P_BACK, t_def - 0.1, ORANGE, tip=True)
    text(d, (CX + 108, CY + 44), "vẽ to hơn thật", 36, MUTED, bold=False, anchor="lm")
    k = appear(t, t_hit + 0.4, 0.45)       # the Sai vi hien NGAY sau khi thay electron bi hat ra, alpha di thang
    if k <= 0: return
    y = 860 + (1 - k) * 30
    card(d, (60, y, 1020, y + 230), fill=A(WHITE, k), outline=A(RED, k), w=5)
    text(d, (W / 2, y + 66), "✗ Do va chạm êlectron", 44, RED, alpha=k)
    text(d, (W / 2, y + 160), "êlectron rất nhẹ so với α", 42, INK, alpha=k)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Lệch mạnh khi bay sát hạt nhân",
             "Thí nghiệm có chứng minh quỹ đạo dừng của êlectron không?")


CLIP = dict(id="bay-l12-ch4-04", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Mô hình nguyên tử · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Chùm α bắn vào lá vàng.", 3.0),
   ("Dừng lại, chọn một đáp án.", 6.0)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án A.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=1.5, caps=[
   ("Chạm êlectron, α vẫn đi thẳng.", 3.4),
   ("Chỉ sát hạt nhân mới lệch mạnh.", 3.8)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.0)]),
])
