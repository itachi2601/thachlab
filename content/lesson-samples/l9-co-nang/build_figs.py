"""Bài 3. Cơ năng (KHTN 9, lesson_id 130).
Sinh 4 hình SVG + số liệu thí nghiệm + 3 file content/thi-nghiem/tn-l9-conang-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi số liệu tính từ mô hình (assert). Chạy: cd <thư mục bài> && python3 build_figs.py
Quy ước KHTN 9: W_t = Ph = 10mh (g ≈ 10), W_đ = ½mv².
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 15          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên

def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", "{,}")
def vt(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def T(x, y, s, c="currentColor", size=17, anchor="start", weight="700"):
    return text(round(x, 1), round(y, 1), s, c, size, anchor, weight)
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'
def W_(idx, c="currentColor"):
    """Kí hiệu W có chỉ số dưới (t, đ) trong <text>."""
    return f'{it_("W")}<tspan dy="5" font-size="14">{idx}</tspan><tspan dy="-5"> </tspan>'
def circ(x, y, r, fill, w=2.2, op=1, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="currentColor" stroke-width="{w}" opacity="{op}"{d}/>'

# ---------- Hình 1: máng chữ U, người trượt ở mép trái (không lộ đáp án)
b = ""
b += line(8, 70, 60, 70, "currentColor", 3) + line(360, 70, 412, 70, "currentColor", 3)
b += ('<path d="M60,70 C60,215 90,222 210,222 C330,222 360,215 360,70" fill="rgba(56,189,248,.10)" '
      'stroke="currentColor" stroke-width="3"/>')
# người trên ván
X, DECK = 34, 70
b += line(X - 18, DECK - 7, X + 18, DECK - 7, BLUE, 4)
b += circ(X - 11, DECK - 3, 3, "none", 2) + circ(X + 11, DECK - 3, 3, "none", 2)
b += line(X, DECK - 36, X - 7, DECK - 9, "currentColor", 2.6) + line(X, DECK - 36, X + 7, DECK - 9, "currentColor", 2.6)
b += line(X, DECK - 36, X, DECK - 56, "currentColor", 2.6)
b += line(X, DECK - 52, X - 13, DECK - 40, "currentColor", 2.4) + line(X, DECK - 52, X + 13, DECK - 42, "currentColor", 2.4)
b += circ(X, DECK - 63, 7, "none", 2.4)
b += T(66, 44, "Nam xuất phát", "currentColor", 16)
b += T(386, 52, "?", RED, 30, "middle")
b += T(210, 246, "đáy máng", "currentColor", 16, "middle", "600")
fig1 = wrap("0 0 420 256", "Máng trượt hình chữ U; Nam đứng trên ván ở mép trái; dấu hỏi ở mép phải", b,
            "Hình 1. Nam thả mình trượt từ mép trái, không đạp thêm.<br>Sang bên phải, Nam lên được tới đâu?")

# ---------- Hình 2: con lắc đơn A – O – B
PX, PY, L, TH = 210, 26, 178, 38.0
def bob(th):
    r = math.radians(th)
    return PX + L * math.sin(r), PY + L * math.cos(r)
Ax, Ay = bob(-TH); Ox, Oy = bob(0); Bx, By = bob(TH)
h_px = Oy - Ay
assert abs(Ax - (420 - Bx)) < 1e-9 and 30 < h_px < 45
b = line(160, PY, 260, PY, "currentColor", 3)
for k in range(6):
    b += line(166 + 18 * k, PY, 158 + 18 * k, PY - 10, "currentColor", 1.6)
b += line(PX, PY, Ax, Ay, "currentColor", 2.2)
b += line(PX, PY, Ox, Oy, "currentColor", 1.6, "5 5", .6) + line(PX, PY, Bx, By, "currentColor", 1.6, "5 5", .6)
arcpts = [bob(t) for t in [-TH + 2 * TH * i / 40 for i in range(41)]]
b += pts_path(arcpts, GRN, 2.2, "7 5")
b += chevron(*bob(-6), *(lambda p, q: (q[0] - p[0], q[1] - p[1]))(bob(-8), bob(-6)), GRN, 2.2, 11)
b += line(40, Oy, 400, Oy, "currentColor", 1.6, "6 5", .7)
b += line(56, Ay, Ax - 14, Ay, "currentColor", 1.4, "4 4", .7)
b += line(66, Ay + 3, 66, Oy - 3, ORG, 2.2) + chevron(66, Ay + 1, 0, -1, ORG, 2.2, 9) + chevron(66, Oy - 1, 0, 1, ORG, 2.2, 9)
b += T(48, (Ay + Oy) / 2 + 6, it_("h"), ORG, 20, "middle")
b += circ(Ax, Ay, 12, "rgba(251,146,60,.35)", 2.4)
b += circ(Ox, Oy, 12, "none", 1.8, .55, "4 3") + circ(Bx, By, 12, "none", 1.8, .55, "4 3")
b += T(Ax - 20, Ay - 6, "A", "currentColor", 19, "end") + T(Bx + 20, By - 6, "B", "currentColor", 19, "start")
b += T(Ox, Oy + 34, "O", "currentColor", 19, "middle")
b += T(400, Oy - 8, "gốc thế năng", "currentColor", 15, "end", "600")
fig2 = wrap("0 0 420 252", "Con lắc đơn: vật kéo lên vị trí A cao h so với vị trí cân bằng O rồi thả, vật đi theo cung tròn qua O tới B", b,
            "Hình 2. Kéo vật lên A, cao <i>h</i> so với O, rồi thả nhẹ.<br>Vật đi A → O → B → O → A…")

# ---------- Hình 3: cột năng lượng của bóng rơi (0,5 kg, từ 4 m, bỏ qua cản)
M3, H3 = 0.5, 4.0
Z3 = (4.0, 2.0, 0.0)
W3 = 10 * M3 * H3
rows3 = [(z, 10 * M3 * z, W3 - 10 * M3 * z) for z in Z3]
assert [r[1] for r in rows3] == [20, 10, 0] and [r[2] for r in rows3] == [0, 10, 20] and W3 == 20
for z, wt, wd in rows3:                          # W_đ = ½mv² khớp v² = 2·10·(H − z)
    v = math.sqrt(2 * 10 * (H3 - z))
    assert abs(0.5 * M3 * v * v - wd) < 1e-9
GY, ZPX = 262, 50                                # mặt đất, px mỗi mét
b = line(14, GY, 132, GY, "currentColor", 2.6)
for k in range(7):
    b += line(20 + 18 * k, GY, 12 + 18 * k, GY + 9, "currentColor", 1.4)
for n, (z, _, _) in enumerate(rows3, 1):
    y = GY - ZPX * z - (11 if z == 0 else 0)
    b += circ(74, y, 11, "rgba(251,146,60,.35)" if n == 1 else "none", 2.2, 1 if n == 1 else .75, "" if n == 1 else "4 3")
    b += T(98, y + 6, str(n), "currentColor", 17, "start")
    if z > 0:
        b += line(14, GY - ZPX * z, 56, GY - ZPX * z, "currentColor", 1.4, "4 3", .7)
b += T(12, GY - ZPX * 4 - 14, "4 m", "currentColor", 15, "start", "600") + T(12, GY - ZPX * 2 - 8, "2 m", "currentColor", 15, "start", "600")
b += line(74, GY - ZPX * 4 + 16, 74, GY - 26, "currentColor", 1.2, "3 5", .5) + chevron(74, GY - 26, 0, 1, "currentColor", 1.6, 9)
KJ, BW = 8.0, 22                                 # px mỗi J, bề rộng cột
COLS = ((ORG, "t"), (BLUE, "đ"), (GRN, ""))
b += line(150, GY, 412, GY, "currentColor", 2)
for g, (z, wt, wd) in enumerate(rows3):
    cx = 196 + 86 * g
    for j, val in enumerate((wt, wd, W3)):
        x = cx - 34 + 25 * j
        hgt = KJ * val
        col = COLS[j][0]
        if hgt > 0:
            b += f'<rect x="{x}" y="{GY - hgt:.1f}" width="{BW}" height="{hgt:.1f}" fill="{col}" opacity=".85"/>'
        else:
            b += line(x, GY - 1.5, x + BW, GY - 1.5, col, 3)
        b += T(x + BW / 2, GY - hgt - 6, vt(val, 0), "currentColor", 14, "middle")
    b += T(cx - 34 + 36, GY + 24, f"vị trí {g + 1}", "currentColor", 15, "middle", "600")
    assert cx - 34 >= 150 and cx - 34 + 50 + BW <= 414
assert KJ * W3 + 30 < GY
# chú giải
LX, LY = 170, 22
for j, (col, idx) in enumerate(COLS):
    x = LX + 80 * j
    b += f'<rect x="{x}" y="{LY - 13}" width="16" height="16" fill="{col}" opacity=".85"/>'
    lab = (it_("W") + f'<tspan dy="5" font-size="14">{idx}</tspan>') if idx else it_("W")
    b += T(x + 22, LY + 1, lab, "currentColor", 16, "start")
b += T(170, 50, "đơn vị: J", "currentColor", 14, "start", "600")
fig3 = wrap("0 0 420 300", "Bóng 0,5 kg rơi từ 4 m: ở vị trí 1 thế năng 20 J động năng 0; vị trí 2 mỗi loại 10 J; vị trí 3 thế năng 0 động năng 20 J; cơ năng luôn 20 J", b,
            "Hình 3. Bóng $0{,}5\\ \\text{kg}$ rơi từ $4\\ \\text{m}.$<br>Cột cam: thế năng.<br>Cột xanh dương: động năng.<br>Cột xanh lá: cơ năng.")

# ---------- Hình 4: bóng nảy thấp dần (mỗi lần còn 80 % độ cao)
K_NAY = 0.80
H_LAN = [1.00]
for _ in range(3):
    H_LAN.append(H_LAN[-1] * K_NAY)
H_DOC = [round(x, 2) for x in H_LAN]
assert H_DOC == [1.00, 0.80, 0.64, 0.51], H_DOC
FY, SC, HW = 214, 160, 34                        # sàn, px mỗi mét, nửa bề rộng cung khi h = 1 m
b = line(14, FY, 300, FY, "currentColor", 2.6)
for k in range(15):
    b += line(22 + 19 * k, FY, 14 + 19 * k, FY + 9, "currentColor", 1.3)
pts, x = [], 26.0
for i in range(21):                              # lần rơi đầu: nửa parabol
    u = i / 20
    pts.append((x + HW * u, FY - SC * H_LAN[0] * (1 - u * u)))
x += HW
peaks = [(26.0, FY - SC * H_LAN[0])]
for hh in H_LAN[1:]:
    w = HW * math.sqrt(hh)
    for i in range(1, 41):
        u = -1 + 2 * i / 40
        pts.append((x + w * (u + 1), FY - SC * hh * (1 - u * u)))
    peaks.append((x + w, FY - SC * hh))
    x += 2 * w
assert x < 300
b += pts_path(pts, GRN, 2.4)
b += circ(26, FY - SC * H_LAN[0] - 10, 10, "rgba(251,146,60,.35)", 2.2)
for (px_, py_), hh in zip(peaks, H_DOC):
    b += line(px_, py_, 312, py_, "currentColor", 1.3, "4 4", .7)
    b += T(318, py_ + 6, vt(hh, 2) + " m", BLUE, 16, "start")
fig4 = wrap("0 0 420 232", "Quả bóng thả từ 1,00 m, nảy lên lần lượt 0,80 m; 0,64 m; 0,51 m", b,
            "Hình 4. Bóng cao su thả từ $1{,}00\\ \\text{m},$ mỗi lần nảy lên thấp hơn.<br>Số liệu minh hoạ, chưa phải số đo thật.")

# ---------- Thí nghiệm 1: khối trượt trên máng đệm khí, m = 0,20 kg; hao hụt 4 % (lực cản nhỏ)
M1, F_HAO = 0.20, 0.04
H1 = (0.10, 0.20, 0.30, 0.40)
rows1 = []
for h in H1:
    v = math.sqrt(2 * 10 * h * (1 - F_HAO))
    vd = round(v, 2)
    wt = 10 * M1 * h
    wd = 0.5 * M1 * vd ** 2
    rows1.append((h, v, vd, wt, wd))
assert [r[2] for r in rows1] == [1.39, 1.96, 2.40, 2.77], [r[2] for r in rows1]
WD1 = [round(r[4], 3) for r in rows1]
assert WD1 == [0.193, 0.384, 0.576, 0.767], WD1
hao = [(r[3] - r[4]) / r[3] * 100 for r in rows1]
assert all(3 < x < 4.2 for x in hao), hao
ss = [2 * 0.005 / r[2] * 100 for r in rows1]     # sai số tương đối của ½mv² do đọc v tới 0,01 m/s
assert max(ss) < 0.75 and max(ss) < min(hao) / 4, ss
bang1 = "\n".join(f"<tr><td>${vn(h, 2)}$</td><td>${vn(wt, 3)}$</td><td>${vn(wd, 3)}$</td></tr>" for h, _, _, wt, wd in rows1)
H_TN1 = ";\\ ".join(vn(h, 2) for h in H1) + "\\ \\text{m}"
V_TN1 = ";\\ ".join(vn(r[2], 2) for r in rows1) + "\\ \\text{m/s}"
NX1 = (f"Động năng ở chân dốc chỉ hụt khoảng ${round(min(hao))}$–${round(max(hao))}\\ \\%$ so với thế năng lúc thả.<br>"
       f"$h$ tăng gấp đôi thì cả hai cột gần như tăng gấp đôi.<br>"
       f"Đọc $v$ tới $0{{,}}01\\ \\text{{m/s}}$ chỉ làm $\\frac{{1}}{{2}}mv^2$ sai chừng ${vn(max(ss), 1)}\\ \\%,$ nhỏ hơn phần hụt nhiều.<br>"
       f"Vậy phần hụt là thật: do lực cản, không phải do đọc sai.")

# ---------- Bài toán mẫu, quiz, thử thách: kiểm số
assert 10 * 0.5 * 8 + 0.5 * 0.5 * 36 == 49 and 10 * 0.5 * 8 + 0.5 * 36 == 58 and 0.5 * 8 + 9 == 13          # Câu 1
Wm = 10 * 0.4 * 1.5 + 0.5 * 0.4 * 36
assert abs(Wm - 13.2) < 1e-9 and abs(Wm / 4 - 3.3) < 1e-9 and abs(math.sqrt(2 * Wm / 0.4) - 8.124) < 1e-3     # bài toán mẫu
W2 = 10 * 0.4 * 1.5 + 0.5 * 0.4 * 16
assert abs(W2 - 9.2) < 1e-9 and abs(W2 / 4 - 2.3) < 1e-9                                                      # điền bước
assert 10 * 0.2 * 2 == 4 and 10 * 0.2 * 3 == 6 and 10 * 0.2 * 1 == 2 and 10 * 0.2 * 4 == 8                     # Câu 6
Wq = 10 * 0.5 * 5
assert Wq == 25 and math.sqrt(2 * Wq / 0.5) == 10 and abs(math.sqrt(Wq / 0.5) - 7.07) < 0.01                  # Câu 7
assert abs(math.sqrt(2 * (0.5 * 5) / 0.5) - 3.16) < 0.01
assert 10 * 2 * 5 + 0.5 * 2 * 9 == 109                                                                         # ⭐
assert math.sqrt(20 * 5) == 10                                                                                 # ⭐⭐⭐
W_NAY = [10 * 0.05 * h for h in H_LAN]
assert abs(W_NAY[0] - 0.5) < 1e-12 and all(abs(W_NAY[i + 1] / W_NAY[i] - 0.8) < 1e-12 for i in range(3))
H_NAY = ";\\ ".join(vn(h, 2) for h in H_DOC[1:]) + "\\ \\text{m}"

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in (("__H_TN1__", H_TN1), ("__V_TN1__", V_TN1), ("__BANG_TN1__", bang1), ("__NHAN_XET_TN1__", NX1),
             ("__H_NAY__", H_NAY), ("__PHUT__", str(PHUT))):
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 3. Cơ năng"
SRC = "content/lesson-samples/l9-co-nang/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 130, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-conang-01", "ten": "Khối trượt trên máng đệm khí nghiêng: so thế năng lúc thả với động năng ở chân dốc", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["conang.bao_toan", "conang.wt_bang_10mh", "conang.wd_bang_nua_mv2", "conang.sai_so_do"],
  "muc_tieu": "Từ bảng số liệu thấy động năng ở chân dốc gần bằng thế năng lúc thả: cơ năng gần như được bảo toàn; phần hụt vài phần trăm do lực cản.",
  "dung_cu": [{"ten": "Máng đệm khí có thể nghiêng, kèm bơm khí", "so_luong": 1},
              {"ten": "Khối trượt 0,20 kg", "so_luong": 1},
              {"ten": "Cổng quang điện + đồng hồ đo thời gian số (đo v tới 0,01 m/s)", "so_luong": 1},
              {"ten": "Thước đo độ cao (ĐCNN 1 mm)", "so_luong": 1}],
  "cac_buoc": {"lam": ["Nghiêng máng, đặt cổng quang ở chân dốc.",
                       "Thả khối trượt không vận tốc đầu từ độ cao h = " + "; ".join(vt(x, 2) for x in H1) + " m so với chân dốc.",
                       "Ghi vận tốc v ở chân dốc; tính 10mh và ½mv²."],
               "quan_sat": ["v đo được: " + "; ".join(vt(r[2], 2) for r in rows1) + " m/s.",
                            "½mv² luôn nhỏ hơn 10mh một chút (hụt khoảng 3–4 %)."],
               "rut_ra": ["Thế năng lúc thả gần như chuyển hết thành động năng ở chân dốc.",
                          "Cơ năng gần như bảo toàn; phần hụt nhỏ thành nhiệt do lực cản."]},
  "tham_so": [{"ky_hieu": "h", "ten": "Độ cao lúc thả so với chân dốc", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.05, "max": 0.5, "mac_dinh": 0.2, "buoc": 0.05},
              {"ky_hieu": "m", "ten": "Khối lượng khối trượt", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": M1},
              {"ky_hieu": "f", "ten": "Phần cơ năng mất do lực cản", "don_vi": "", "kieu": "co_dinh", "gia_tri": F_HAO},
              {"ky_hieu": "v", "ten": "Vận tốc ở chân dốc", "don_vi": "m/s", "kieu": "do_duoc", "sai_so_do": 0.005},
              {"ky_hieu": "W_d", "ten": "Động năng ở chân dốc ½mv²", "don_vi": "J", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["W_t = 10·m·h", "v = sqrt(2·10·h·(1 − f)) với f = 0,04", "v_doc = lam_tron(v, 0,01 m/s)", "W_d = ½·m·v_doc²"],
              "gia_thiet": ["g ≈ 10 m/s² theo quy ước KHTN 9 (W_t = 10mh)", "lực cản nhỏ, coi lấy đi 4 % cơ năng ở mọi độ cao (số minh hoạ, cố ý lớn cho dễ thấy; máng đệm khí thật thường hụt 1–2 %)"]},
  "so_lieu_mau": {"cot": ["h (m)", "v (m/s)", "10mh (J)", "½mv² (J)"],
                  "hang": [[r[0], r[2], round(r[3], 3), round(r[4], 3)] for r in rows1],
                  "ghi_chu": "Số liệu minh hoạ từ mô hình v = sqrt(20h·0,96), làm tròn 0,01 m/s; chưa phải số đo thật."},
  "ket_qua_ky_vong": "½mv² ≈ 0,96·10mh ở mọi độ cao; sai số đọc v (≤ 0,7 %) nhỏ hơn phần hụt.",
  "hien_tuong_hay_sai": ["Nghĩ ở chân dốc thế năng bằng 0 nên cơ năng 'mất'.", "Nghĩ phần hụt là do đọc đồng hồ sai.",
                         "Nghĩ vật nặng hơn thì xuống chân dốc nhanh hơn."],
  "sai_so_thuong_gap": "Đọc v tới 0,01 m/s làm ½mv² sai khoảng 0,4–0,7 %; đo h sai 1 mm làm 10mh sai 1 % ở h = 0,10 m.",
  "an_toan": "Giữ khối trượt ở chân dốc bằng tay hoặc tấm chặn mềm.",
  "goi_y_mo_phong": {"loai": "bang_so_lieu+do_thi", "y_tuong": "Kéo thanh h, khối trượt chạy xuống; hai cột 10mh và ½mv² mọc lên cạnh nhau; nút bật/tắt lực cản.",
                     "diem_nhan": "Tắt lực cản thì hai cột bằng nhau đúng."}})
tn.append({**base,
  "id": "tn-l9-conang-02", "ten": "Con lắc vướng đinh: vật trở lại đúng độ cao cũ", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["conang.bao_toan", "conang.chuyen_hoa"],
  "muc_tieu": "Thấy con lắc vẫn lên tới gần đúng độ cao lúc thả dù dây vướng đinh làm đường đi đổi: cơ năng được bảo toàn.",
  "dung_cu": [{"ten": "Quả nặng 100–200 g treo dây mảnh dài khoảng 1 m", "so_luong": 1},
              {"ten": "Bảng gỗ có giá treo, một cái đinh đóng dưới điểm treo", "so_luong": 1},
              {"ten": "Thước kẻ, phấn để kẻ vạch ngang", "so_luong": 1}],
  "cac_buoc": {"lam": ["Treo con lắc trước bảng, kẻ vạch ngang ngang tầm vị trí A.", "Đóng đinh trên đường thẳng đứng dưới điểm treo.",
                       "Kéo vật lên A rồi thả nhẹ."],
               "quan_sat": ["Dây vướng đinh, vật đi cung tròn bán kính nhỏ hơn.", "Vật lên tới gần đúng vạch ngang."],
               "rut_ra": ["Vật trở lại gần đúng độ cao cũ dù đường đi đổi.", "Cơ năng gần như được bảo toàn."]},
  "tham_so": [{"ky_hieu": "h", "ten": "Độ cao A so với vị trí thấp nhất", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.05, "max": 0.2, "mac_dinh": 0.15, "buoc": 0.01},
              {"ky_hieu": "d", "ten": "Khoảng cách đinh dưới điểm treo", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.3, "max": 0.7, "mac_dinh": 0.5, "buoc": 0.05},
              {"ky_hieu": "h_len", "ten": "Độ cao vật lên được phía bên kia", "don_vi": "m", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["h_len = h (bỏ qua lực cản)", "điều kiện vật còn đi trên cung tròn: h nhỏ hơn bán kính phần dây dưới đinh (L − d)"],
              "gia_thiet": ["dây không dãn, bỏ qua lực cản", "dây dài 1 m; giới hạn h ≤ 0,2 m và d ≤ 0,7 m để h nhỏ hơn L − d, dây luôn căng"]},
  "so_lieu_mau": {"cot": ["h lúc thả (m)", "h lên được (m)"], "hang": [[0.15, 0.15]],
                  "ghi_chu": "Kết quả lí tưởng; thực tế thấp hơn 1–2 mm do lực cản."},
  "ket_qua_ky_vong": "Vật lên tới gần đúng vạch ngang ở cả hai phía.",
  "hien_tuong_hay_sai": ["Nghĩ cung ngắn hơn thì vật lên thấp hơn.", "Nghĩ vướng đinh làm vật 'mất đà' rất nhiều."],
  "an_toan": "Không kéo dây quá cao để vật quật vào đinh hoặc người đứng gần.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Kéo đinh lên xuống, thả con lắc; vạch ngang của A luôn hiện.",
                     "diem_nhan": "Mọi vị trí đinh, vật đều chạm lại vạch ngang."}})
tn.append({**base,
  "id": "tn-l9-conang-03", "ten": "Đo độ cao bóng cao su nảy lên sau mỗi lần chạm sàn", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["conang.co_luc_can", "conang.bao_toan_nang_luong"],
  "muc_tieu": "Thấy cơ năng của bóng giảm sau mỗi lần va sàn; phần giảm thành nhiệt năng và âm thanh, năng lượng toàn phần vẫn bảo toàn.",
  "dung_cu": [{"ten": "Bóng cao su 50 g", "so_luong": 1}, {"ten": "Thước dài 1 m dựng đứng", "so_luong": 1},
              {"ten": "Điện thoại quay video chậm", "so_luong": 1}],
  "cac_buoc": {"lam": ["Thả bóng từ 1,00 m cạnh thước, quay video.", "Xem lại từng khung, đọc độ cao ba lần nảy đầu."],
               "quan_sat": ["Độ cao: " + "; ".join(vt(x, 2) for x in H_DOC[1:]) + " m."],
               "rut_ra": ["Mỗi lần nảy cơ năng còn khoảng 80 % lần trước.", "Phần mất thành nhiệt năng, âm thanh."]},
  "tham_so": [{"ky_hieu": "h0", "ten": "Độ cao thả", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.5, "max": 2, "mac_dinh": 1, "buoc": 0.1},
              {"ky_hieu": "k", "ten": "Tỉ số độ cao hai lần nảy liên tiếp", "don_vi": "", "kieu": "dieu_chinh", "min": 0.5, "max": 0.95, "mac_dinh": K_NAY, "buoc": 0.05},
              {"ky_hieu": "m", "ten": "Khối lượng bóng", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": 0.05},
              {"ky_hieu": "W_n", "ten": "Cơ năng sau lần nảy n", "don_vi": "J", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["h_n = h0·k^n", "W_n = 10·m·h_n"], "gia_thiet": ["bỏ qua sức cản không khí giữa hai lần chạm", "mỗi lần va sàn mất cùng một tỉ lệ cơ năng"]},
  "so_lieu_mau": {"cot": ["Lần", "h (m)", "W = 10mh (J)"],
                  "hang": [[n, H_DOC[n], round(W_NAY[n], 3)] for n in range(4)],
                  "ghi_chu": "Số liệu minh hoạ từ mô hình h_n = 1,00·0,8^n; chưa phải số đo thật."},
  "ket_qua_ky_vong": "Độ cao và cơ năng giảm theo cấp số nhân, mỗi lần còn khoảng 80 %.",
  "hien_tuong_hay_sai": ["Nghĩ năng lượng của bóng mất đi, trái bảo toàn năng lượng.", "Nghĩ bóng vẫn bảo toàn cơ năng."],
  "an_toan": "Thả bóng ở chỗ trống, không gần đồ dễ vỡ.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Bóng nảy với thanh k; cột cơ năng và cột nhiệt năng cộng dồn hiện cạnh nhau.",
                     "diem_nhan": "Cơ năng + nhiệt năng luôn bằng cơ năng lúc thả."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| TN1 v:", [r[2] for r in rows1], "Wd:", WD1, "hao %:", [round(x, 2) for x in hao], "| nảy:", H_DOC)
