# Clip bay phu dao L12 Ch.4 so 03 - Phong xa khong doi theo nhiet do, ap suat; binh chi chi chan tia
# (topic_id 229 "Dinh luat phong xa va chu ki ban ra", lesson_topic 72). Kieu de Bo 2025-2026 "nguon phong xa trong binh chi".
# TU SOAN: chua co luot lam chuong 4 trong 60 ngay toi 12/11/2026 (lop chua hoc toi).
#   Hinh: hai nguon giong het; nguon phai trong binh chi day, lam lanh. "Vi sao (may dem) ben phai dem it han?"
#   A. Lanh lam T tang  B. Hat nhan ngung phan ra  C. Chi lam phan ra cham  D. Chi chan bot tia ra ngoai -> D.
# Kien thuc SGK: phong xa la qua trinh tu phat, khong chiu tac dong cua cac yeu to ben ngoai (nhiet do, ap suat...);
#   chi (vat lieu day) hap thu tia phong xa -> che chan. Khong neu so lieu ngoai SGK; may dem ve bang thanh muc, khong so.
# Nhieu: A = nghi lanh lam cham "phan ung"; B = nghi chan het tia nghia la het phong xa; C = nghi vo boc tac dong len hat nhan.
# Hinh: hai nguon GIONG NHAU, cung danh sach su kien phan ra (Random(7)) -> chop cung nhip; nguon trai de ngoai, tia toi may dem;
#   nguon phai trong binh chi, tia dung o thanh binh. Dai thoi gian trong the: hai hang vach trung nhau.
# Cau THU NGHI: T = 4 ngay, de tu lanh 8 ngay -> con 1/4 (ket hop clip 02; khong so nao hien tren man).
from clips.bay_chung import *

QY = 830
Q_LINES = ["Hai nguồn giống hệt.", "Vì sao bên phải đếm ít hẳn?"]
OPTS = ["Lạnh làm T tăng", "Hạt nhân ngừng phân rã",
        "Chì làm phân rã chậm", "Chì chặn bớt tia ra ngoài"]
ANS = 3
SY = 430                                  # tam nguon
LX, RX = 290, 790                         # nguon trai (de ngoai) / phai (trong binh chi)
BOX = 120                                 # nua canh trong binh chi
WALL = 30
DET_Y = 700                               # may dem
_r = random.Random(7); EV = []; _t = 0.2
while _t < 40: EV.append((_t, _r.uniform(0, 2 * math.pi))); _t += _r.uniform(0.25, 0.6)
RAY_V = 520                               # px/s


def source(d, cx, gt):
    d.ellipse([cx - 24, SY - 24, cx + 24, SY + 24], fill=A(ORANGE, 1), outline=A(mix(ORANGE, NAVY, 0.4), 1), width=3)
    for te, ang in EV:
        a = gt - te
        if 0 <= a < 0.3:   # chop khi phan ra
            r = 30 + 60 * a; d.ellipse([cx - r, SY - r, cx + r, SY + r], outline=A(YELLOW, 1 - a / 0.3), width=6)


def rays(d, cx, gt, rmax, alpha=1.0):
    """Tia bay tu nguon theo goc su kien; dung o ban kinh rmax(ang)."""
    for i, (te, ang) in enumerate(EV):
        a = gt - te
        if a <= 0 or a > 1.6: continue
        L = min(RAY_V * a, rmax(ang, i)); L0 = max(28, L - 70)
        if L <= 28: continue
        fade = 1 - clamp((a - 1.2) / 0.4)
        p0 = (cx + L0 * math.cos(ang), SY + L0 * math.sin(ang)); p1 = (cx + L * math.cos(ang), SY + L * math.sin(ang))
        d.line([p0, p1], fill=A(PURPLE, alpha * fade), width=5)


def r_out(a):
    """Tia ra ngoai: dai 300 px, rieng tia huong xuong dung o y <= SY + 215 (khong cham may dem)."""
    return min(300, 215 / math.sin(a)) if math.sin(a) > 0.1 else 300


def lead_box(d):
    o = BOX + WALL
    d.rectangle([RX - o, SY - o, RX + o, SY + o], fill=A(GRAY, 1))
    d.rectangle([RX - BOX, SY - BOX, RX + BOX, SY + BOX], fill=A((225, 236, 250), 1))   # long binh lanh (xanh nhat)
    text(d, (RX, SY - o - 30), "chì, lạnh", 40, NAVY)


def detector(d, cx, level, alpha=1.0):
    x0, x1 = cx - 130, cx + 130
    card(d, (x0, DET_Y - 40, x1, DET_Y + 40), fill=A(WHITE, alpha), outline=A(NAVY, alpha), r=14, w=4)
    d.rectangle([x0 + 20, DET_Y - 14, x1 - 20, DET_Y + 14], fill=A(LIGHT, alpha))
    if level > 0.01: d.rectangle([x0 + 20, DET_Y - 14, x0 + 20 + (x1 - x0 - 40) * level, DET_Y + 14], fill=A(GREEN, alpha))
    text(d, (cx, DET_Y + 72), "máy đếm", 36, INK, alpha=alpha)


def scene_top(d, gt, lv=(0.85, 0.12)):
    lead_box(d)
    rays(d, LX, gt, lambda a, i: r_out(a))
    # trong binh: tia dung o thanh trong; cu 6 tia co 1 tia xuyen qua thanh chi ("chan bot", khong chan het)
    rays(d, RX, gt, lambda a, i: r_out(a) if i % 6 == 0 else BOX / max(abs(math.cos(a)), abs(math.sin(a))))
    source(d, LX, gt); source(d, RX, gt)
    detector(d, LX, lv[0]); detector(d, RX, lv[1])
    pw = tw(d, "ngoài", F(40)) + 30   # nhan ve sau tia, nen trang de tia khong de chu
    card(d, (LX - pw / 2, SY - BOX - WALL - 58, LX + pw / 2, SY - BOX - WALL - 2), fill=A(BG, 1), r=12)
    text(d, (LX, SY - BOX - WALL - 30), "ngoài", 40, NAVY)


# ---------------- canh 1: tinh huong ----------------
def s_hoi(img, d, t, sc):
    scene_top(d, sc["t0"] + t)
    k = appear(t, sc["M"][1] - 0.15, 0.45)
    qcard(d, t, sc, QY, Q_LINES, OPTS, sc["M"][1] + 0.6, sc["T"] - 0.1, k=k, head="")


# ---------------- canh 2: dap an ----------------
def s_dapan(img, d, t, sc):
    scene_top(d, sc["t0"] + t)
    answer_pill(d, 1000, "D", OPTS[ANS], appear(t, 0.5, 0.5))


# ---------------- canh 3: sai vi ... ----------------
def s_saivi(img, d, t, sc):
    m0, m1 = sc["M"]; gt = sc["t0"] + t
    scene_top(d, gt)
    m1 = m1 - 1.0                                   # cong B: the Sai vi hien som 1 s
    k = appear(t, m1 - 0.1, 0.45)
    if k <= 0: return
    y = 830 + (1 - k) * 30
    card(d, (60, y, 1020, y + 620), fill=A(WHITE, k), outline=A(RED, k), w=5)
    text(d, (W / 2, y + 50), "Sai: phân rã không chậm lại", 42, RED, alpha=k)
    ts = sc["t0"] + m1 - 0.1; x0, x1, pps = 150, 920, 170           # dai thoi gian: 170 px/s
    for j, (lab, yy) in enumerate((("ngoài", y + 150), ("chì, lạnh", y + 300))):
        text(d, (x0, yy - 46), lab, 38, NAVY, anchor="lm", alpha=k)
        d.line([(x0, yy), (x1, yy)], fill=A(NAVY, k), width=3)
        text(d, (x1 + 36, yy), "t →", 36, NAVY, alpha=k)
        for te, ang in EV:
            if ts <= te <= gt and x0 + (te - ts) * pps <= x1:
                x = x0 + (te - ts) * pps
                d.line([(x, yy - 22), (x, yy + 22)], fill=A(ORANGE, k), width=6)
    text(d, (W / 2, y + 375), "mỗi vạch = một lần phân rã", 38, MUTED, bold=False, alpha=k)
    k2 = appear(t, m1 + 2.2, 0.45)                 # ket luan hien khi hai hang vach da du dai de so
    if k2 > 0:
        pw = tw(d, "T giữ nguyên", F(42)) + 48
        badge(d, W / 2 + pw / 2, y + 520, "T giữ nguyên", GREEN, k * k2, size=42)


# ---------------- canh 4: quy tac + cau hoi tu nho ----------------
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "T không đổi theo nhiệt độ, áp suất",
             "T = 4 ngày, ướp lạnh 8 ngày: còn bao nhiêu phần hạt nhân chưa phân rã?")


CLIP = dict(id="bay-l12-ch4-03", header="VẬT LÍ 12 · BẪY HAY SAI", footer="Phóng xạ · thachlab.id.vn", cues=bay_cues,
            scenes=[
 dict(key="hoi", title="Tình huống", draw=s_hoi, tail=0.5, caps=[
   ("Nhìn máy đếm.", 3.0),
   ("Dừng lại, chọn một đáp án.", 6.4)]),
 dict(key="dapan", title="Đáp án", draw=s_dapan, tail=0.6, caps=[
   ("Đáp án D.", 2.8)]),
 dict(key="saivi", title="Sai vì…", draw=s_saivi, tail=1.6, caps=[
   ("Chớp: hạt nhân phân rã.", 3.4),
   ("Hai nguồn: cùng nhịp.", 4.2)]),
 dict(key="end", title="Quy tắc", draw=s_end, tail=1.0, caps=[
   ("Tự nhớ lại.", 6.6)]),
])
