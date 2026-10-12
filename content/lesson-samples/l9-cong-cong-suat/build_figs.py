"""Bài 4. Công và công suất (KHTN 9, lesson_id 131).
Sinh 4 hình SVG + bảng số liệu thí nghiệm + 3 file content/thi-nghiem/tn-l9-congco-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi số liệu tính từ mô hình (assert). Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 14          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên

def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", "{,}")
def vt(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def T(x, y, s, c="currentColor", size=17, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'
def vec(c, x1, y1, x2, y2, w=2.8):
    """Vectơ thân thẳng + đầu V 30° (svg_lib.arrow)."""
    return arrow("", c, x1, y1, x2, y2, w)
def bag(x, y, w=34, h=26, dash=""):
    """Bao gạo / túi: hình chữ nhật bo góc + quai."""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2"{d}/>'
            f'<path d="M{x + 9},{y} q{w / 2 - 9},-12 {w - 18},0" fill="none" stroke="currentColor" stroke-width="2"{d}/>')

# ---------- Hình 1: cầu thang tầng 1 → tầng 3, hai bạn xách bao gạo (chỉ cảnh, không ghi công suất)
G1, TOP1 = 236, 96                    # mặt sàn tầng 1, tầng 3 (6 m ↔ 140 px)
X_ST, X_EN = 96, 270
NB = 10
b = ""
pts = []
for k in range(NB):
    x0 = X_ST + (X_EN - X_ST) * k / NB
    x1 = X_ST + (X_EN - X_ST) * (k + 1) / NB
    y0 = G1 - (G1 - TOP1) * k / NB
    y1 = G1 - (G1 - TOP1) * (k + 1) / NB
    pts += [(x0, y0), (x0, y1), (x1, y1)]
b += pts_path(pts, "currentColor", 2.4)
b += line(14, G1, X_ST, G1, "currentColor", 2.4) + line(X_EN, TOP1, 312, TOP1, "currentColor", 2.4)
b += line(14, G1 - 70, 312, G1 - 70, "currentColor", 1.2, "5 5", .45)
b += T(14, G1 + 24, "tầng 1", "currentColor", 16, "start", "600") + T(262, TOP1 + 24, "tầng 3", "currentColor", 16, "start", "600")
b += bag(40, G1 - 30) + bag(272, TOP1 - 30, dash="4 3")
b += T(14, 30, "Bao gạo 10 kg", ORG, 17)
# kích thước 6 m
b += vec("g", 340, G1, 340, TOP1, 2.2) + vec("g", 340, TOP1, 340, G1, 2.2) + T(350, (G1 + TOP1) / 2 + 6, "6 m", GRN, 17)
b += T(250, 30, "Minh: 20 s", BLUE, 17) + T(250, 56, "Nam: 60 s", RED, 17)
assert abs((G1 - TOP1) - 140) < 1e-9
fig1 = wrap("0 0 420 270", "Cầu thang từ tầng 1 lên tầng 3 cao 6 mét; bao gạo 10 kilôgam ở chân cầu thang và ở đầu cầu thang; Minh mất 20 giây, Nam mất 60 giây", b,
            "Hình 1. Minh mất 20 s.<br>Nam mất 60 s.")

# ---------- Hình 2: đẩy thùng hàng, lực F và quãng đường s cùng hướng
FL = 172                               # mặt sàn
BX0, BW, BH = 118, 60, 56              # thùng lúc đầu
BX1 = 300                              # thùng lúc sau
b = line(14, FL, 410, FL, "currentColor", 2.4)
for k in range(14):
    b += line(24 + 28 * k, FL, 14 + 28 * k, FL + 10, "currentColor", 1.2, "", .5)
# người que đẩy
b += '<circle cx="62" cy="86" r="12" fill="none" stroke="currentColor" stroke-width="2.5"/>'
b += line(66, 98, 82, 136, "currentColor", 2.5) + line(82, 136, 62, FL, "currentColor", 2.5) + line(82, 136, 104, FL, "currentColor", 2.5)
b += line(72, 110, BX0, FL - 34, "currentColor", 2.5) + line(74, 116, BX0, FL - 24, "currentColor", 2.5)
b += f'<rect x="{BX0}" y="{FL - BH}" width="{BW}" height="{BH}" rx="4" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2.4"/>'
b += f'<rect x="{BX1}" y="{FL - BH}" width="{BW}" height="{BH}" rx="4" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4" opacity=".7"/>'
b += vec("r", BX0 + BW, FL - 28, BX0 + BW + 80, FL - 28) + T(BX0 + BW + 40, FL - 40, it_("F"), RED, 20, "middle")
# quãng đường s: từ mép trước thùng lúc đầu tới mép trước thùng lúc sau
b += line(BX0 + BW, FL + 14, BX0 + BW, FL + 40, "currentColor", 1.2, "3 3", .6) + line(BX1 + BW, FL + 14, BX1 + BW, FL + 40, "currentColor", 1.2, "3 3", .6)
b += vec("g", BX0 + BW, FL + 32, BX1 + BW, FL + 32, 2.4) + T((BX0 + BX1) / 2 + BW, FL + 26, it_("s"), GRN, 20, "middle")
b += T(14, 30, "Lực đẩy và dịch chuyển cùng hướng", "currentColor", 16, "start", "600")
assert BX1 - BX0 > BW + 40
fig2 = wrap("0 0 420 222", "Người đẩy thùng hàng trên sàn bằng lực F nằm ngang; thùng dịch chuyển quãng đường s cùng hướng với lực", b,
            "Hình 2. Lực đẩy F làm thùng dịch chuyển quãng đường s.<br>Dịch chuyển cùng hướng với lực.")

# ---------- Hình 3: ba trường hợp, cùng lực tay 30 N hướng lên (cùng độ dài, k = 2 px/N)
K3, F3 = 2.0, 30.0
b = ""
cols = (70, 210, 350)
YB = 150                               # đáy vật
for i, cx in enumerate(cols):
    if i < 2:
        b += f'<rect x="{cx - 24}" y="{YB - 30}" width="48" height="30" rx="5" fill="rgba(56,189,248,.15)" stroke="currentColor" stroke-width="2.2"/>'
        b += f'<path d="M{cx - 10},{YB - 30} q10,-12 20,0" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    else:
        b += f'<path d="M{cx - 24},{YB - 32} L{cx + 24},{YB - 32} L{cx + 17},{YB} L{cx - 17},{YB} Z" fill="rgba(56,189,248,.15)" stroke="currentColor" stroke-width="2.2"/>'
        b += f'<path d="M{cx - 24},{YB - 32} Q{cx},{YB - 56} {cx + 24},{YB - 32}" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    top = YB - 42
    sv, (_, ytip) = vec_luc("r", cx, top, 0, -1, F3, K3)
    b += sv + T(cx + 8, ytip + 14, it_("F"), RED, 18)
    assert abs((top - ytip) - K3 * F3) < 1e-6
# dịch chuyển
b += T(cols[0], YB + 30, "đứng yên", GRN, 16, "middle")
b += vec("g", cols[1] - 30, YB + 22, cols[1] + 40, YB + 22, 2.4) + T(cols[1] + 46, YB + 28, it_("s"), GRN, 18)
b += vec("g", cols[2] + 40, YB - 4, cols[2] + 40, YB - 74, 2.4) + T(cols[2] + 48, YB - 40, it_("s"), GRN, 18)
b += line(140, 14, 140, 250, "currentColor", 1.2, "5 5", .5) + line(280, 14, 280, 250, "currentColor", 1.2, "5 5", .5)
labs = (("(a) giữ yên", "A = 0"), ("(b) đi ngang", "A = 0"), ("(c) kéo gầu lên", "A = F·s"))
for cx, (l1, l2) in zip(cols, labs):
    b += T(cx, 212, l1, "currentColor", 15, "middle", "600") + T(cx, 238, l2, RED, 16, "middle")
fig3 = wrap("0 0 420 250", "Ba trường hợp cùng lực tay hướng lên: giữ cặp đứng yên thì công bằng 0; xách cặp đi ngang thì công bằng 0; kéo gầu nước lên thì công bằng F nhân s", b,
            "Hình 3. Cùng một lực tay hướng lên.<br>Chỉ khi vật đi lên theo hướng lực, lực tay mới thực hiện công.")

# ---------- Hình 4: cầu thang — s theo hướng lực nâng là độ cao h, không phải đường dọc cầu thang
G4, TOP4 = 220, 80
XS4, XE4 = 76, 260
b = ""
pts = []
for k in range(NB):
    x0 = XS4 + (XE4 - XS4) * k / NB
    x1 = XS4 + (XE4 - XS4) * (k + 1) / NB
    y0 = G4 - (G4 - TOP4) * k / NB
    y1 = G4 - (G4 - TOP4) * (k + 1) / NB
    pts += [(x0, y0), (x0, y1), (x1, y1)]
b += pts_path(pts, "currentColor", 2.4)
b += line(XE4, TOP4, 300, TOP4, "currentColor", 2.4) + line(10, G4, XS4, G4, "currentColor", 2.4)
b += line(XS4, G4 - 2, XE4, TOP4 - 2, BLUE, 2.2, "7 5")
b += T(160, 196, "đường dọc", BLUE, 15, "start", "600") + T(160, 214, "cầu thang", BLUE, 15, "start", "600")
b += line(14, (G4 + TOP4) / 2, 300, (G4 + TOP4) / 2, "currentColor", 1.2, "5 5", .45)
b += T(14, G4 + 20, "tầng 1", "currentColor", 15, "start", "600")
b += T(14, (G4 + TOP4) / 2 - 8, "tầng 2", "currentColor", 15, "start", "600")
b += T(258, TOP4 - 10, "tầng 3", "currentColor", 15, "start", "600")
b += vec("g", 320, G4, 320, TOP4, 2.4) + vec("g", 320, TOP4, 320, G4, 2.4)
b += T(330, 140, it_("h"), GRN, 20) + T(330, 162, "= s", GRN, 17)
b += bag(18, G4 - 28) + vec("r", 35, G4 - 34, 35, G4 - 72, 2.6) + T(43, G4 - 52, it_("F"), RED, 18)
b += T(14, 266, "Từ tầng 1 lên tầng 3: 2 khoảng tầng.", "currentColor", 15, "start", "600")
fig4 = wrap("0 0 420 278", "Cầu thang từ tầng 1 lên tầng 3: đường dọc cầu thang vẽ nét đứt xanh; độ cao h theo hướng lực nâng là quãng đường s; từ tầng 1 lên tầng 3 là 2 khoảng tầng", b,
            "Hình 4. Lực nâng hướng thẳng lên.<br>Quãng đường theo hướng lực là độ cao h.")

# ---------- Thí nghiệm 1: kéo đều khối gỗ, lực cản 1,5 N; số đọc lực kế dao động ±1 vạch (0,1 N)
F_THAT = 1.5
DOC = [(1.5, 0.50), (1.6, 0.50), (1.4, 0.50), (1.5, 1.00)]
rows1 = [(f, s, round(f * s, 2)) for f, s in DOC]
assert [r[2] for r in rows1] == [0.75, 0.80, 0.70, 1.50]
A_tb = sum(r[2] for r in rows1[:3]) / 3
assert abs(A_tb - 0.75) < 1e-9 and abs(rows1[3][2] / A_tb - 2) < 1e-9
lech = max(abs(r[2] - A_tb) for r in rows1[:3])
p_lech = lech / A_tb * 100
assert abs(lech - 0.05) < 1e-9 and 6.5 < p_lech < 7
bang1 = "\n".join(f"<tr><td>${vn(f, 1)}$</td><td>${vn(s, 2)}$</td><td>${vn(a, 2)}$</td></tr>" for f, s, a in rows1)
NX1 = (f"Ba lần đầu: trung bình $A = {vn(A_tb, 2)}\\ \\text{{J}}.$<br>"
       f"Mỗi lần lệch tới ${vn(lech, 2)}\\ \\text{{J}},$ khoảng ${round(p_lech)}\\ \\%,$ do kim lực kế rung một vạch.<br>"
       f"Lần 4: $s$ gấp đôi, $A = {vn(rows1[3][2], 2)}\\ \\text{{J}}$ gấp đôi trung bình.")

# ---------- Kiểm số liệu quiz / bài toán mẫu / thử thách
assert 10 * 10 * 6 == 600 and 600 / 20 == 30 and 600 / 60 == 10               # mở bài + Câu 3
assert 600 * 20 == 12000 and 10 * 6 / 20 == 3 and abs(20 / 600 - 0.0333) < 1e-3
assert abs(120 * 4186 - 502320) < 1e-9 and abs(500 * 1000 - 5e5) < 1e-9           # hộp sữa ≈ 5·10⁵ J
assert 200 * 15 == 3000 and abs(200 / 15 - 13.33) < 0.01 and 200 + 15 == 215      # Câu 2
assert 30 * 50 == 1500 and 30 + 50 == 80 and 30 / 50 == 0.6                        # Câu 4
h6 = (5 - 1) * 3
assert h6 == 12 and 600 * h6 == 7200 and 7200 / 20 == 360                          # Câu 6
assert 600 * 15 / 20 == 450 and 600 * 3 / 20 == 90 and 7200 * 20 == 144000
F_m, A_m = 10 * 1200, 10 * 1200 * 15                                                # bài toán mẫu
assert F_m == 12000 and A_m == 180000 and A_m / 30 == 6000 and F_m * 15 / 30 == 6000
assert A_m / 45 == 4000 and 24000 * 15 == 360000 and 360000 / 30 == 12000 and 360000 / 6000 == 60
v7 = 72 / 3.6                                                                        # Câu 7
assert abs(v7 - 20) < 1e-9 and 2000 * v7 == 40000 and 2000 * 72 == 144000 and 2000 / v7 == 100
assert abs(2000 / 72 - 27.8) < 0.05
assert 2 * 4186 == 8372 and 500 * 9 == 4500 and 4500 / 30 == 150                  # thử thách ⭐, ⭐⭐
assert 30000 / 1500 == 20 and 30000 / 3000 == 10 and 20 * 3.6 == 72 and 10 * 3.6 == 36   # ⭐⭐⭐

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in (("__BANG_TN1__", bang1), ("__NHAN_XET_TN1__", NX1), ("__PHUT__", str(PHUT))):
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 4. Công và công suất"
SRC = "content/lesson-samples/l9-cong-cong-suat/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 131, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-congco-01", "ten": "Kéo đều khối gỗ bằng lực kế, tính công A = F·s", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["congco.a_bang_fs", "congco.sai_so_do"],
  "muc_tieu": "Từ số đọc lực kế và quãng đường tính công A = F·s; thấy cùng lực thì quãng đường gấp đôi, công gấp đôi; nhận ra sai số khi đọc lực kế.",
  "dung_cu": [{"ten": "Khối gỗ có móc", "so_luong": 1},
              {"ten": "Lực kế (GHĐ 5 N, ĐCNN 0,1 N)", "so_luong": 1},
              {"ten": "Thước mét (ĐCNN 1 cm)", "so_luong": 1},
              {"ten": "Mặt bàn phẳng nằm ngang", "so_luong": 1}],
  "cac_buoc": {"lam": ["Móc lực kế vào khối gỗ, kéo đều theo phương ngang.",
                       "Ba lần kéo 0,50 m, một lần kéo 1,00 m; mỗi lần đọc lực kế khi khối gỗ đang chạy đều.",
                       "Tính A = F·s cho mỗi lần."],
               "quan_sat": ["Kim lực kế rung nhẹ quanh vạch 1,5 N.", "Ba lần cùng 0,50 m cho A từ 0,70 J đến 0,80 J."],
               "rut_ra": ["Lực kéo đều gần như không đổi.", "Quãng đường gấp đôi thì công gấp đôi.",
                          "Đo nhiều lần lấy trung bình để giảm sai số khi đọc kim."]},
  "tham_so": [{"ky_hieu": "s", "ten": "Quãng đường kéo", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.1, "max": 1.0, "mac_dinh": 0.5, "buoc": 0.1},
              {"ky_hieu": "F_that", "ten": "Lực cản (bằng lực kéo khi kéo đều)", "don_vi": "N", "kieu": "co_dinh", "gia_tri": F_THAT},
              {"ky_hieu": "F", "ten": "Số đọc lực kế", "don_vi": "N", "kieu": "do_duoc", "sai_so_do": 0.1},
              {"ky_hieu": "A", "ten": "Công của lực kéo", "don_vi": "J", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["F_doc = F_that ± 0,1 N (kim rung một vạch)", "A = F_doc·s"],
              "gia_thiet": ["kéo đều nên lực kéo bằng lực cản", "lực kéo song song mặt bàn, cùng hướng dịch chuyển"]},
  "so_lieu_mau": {"cot": ["F (N)", "s (m)", "A (J)"], "hang": [list(r) for r in rows1],
                  "ghi_chu": "Số liệu minh hoạ: lực cản 1,5 N, số đọc lệch ±1 vạch; chưa phải số đo thật."},
  "ket_qua_ky_vong": "A trung bình 0,75 J với s = 0,50 m; 1,50 J với s = 1,00 m.",
  "hien_tuong_hay_sai": ["Giật mạnh lực kế: số chỉ lớn hơn lực cản và không ổn định.", "Kéo xiên lên: chỉ một phần lực cùng hướng dịch chuyển.",
                         "Dùng lực kế độ chia thô (1 N) làm sai số lớn."],
  "sai_so_thuong_gap": "Đọc lệch một vạch 0,1 N trên 1,5 N là khoảng 7 %.",
  "an_toan": "Kéo nhẹ, không để khối gỗ rơi khỏi bàn.",
  "goi_y_mo_phong": {"loai": "bang_so_lieu", "y_tuong": "Kéo thanh s, khối gỗ trượt đều, kim lực kế rung quanh 1,5 N; bảng tự tính A.",
                     "diem_nhan": "Cùng lực, công tỉ lệ với quãng đường theo hướng lực."}})
tn.append({**base,
  "id": "tn-l9-congco-02", "ten": "Hai bạn xách bao gạo lên tầng 3: cùng công, khác công suất", "loai": "vi_du", "muc_do": "co_ban",
  "kien_thuc": ["congco.a_bang_fs", "congsuat.p_bang_a_chia_t"],
  "muc_tieu": "Thấy hai người làm cùng một công nhưng mất thời gian khác nhau; công suất P = A/t cho biết ai làm nhanh hơn.",
  "dung_cu": [{"ten": "Bao gạo 10 kg", "so_luong": 2}, {"ten": "Cầu thang cao 6 m (tầng 1 lên tầng 3)", "so_luong": 1},
              {"ten": "Đồng hồ bấm giờ", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mỗi bạn xách một bao gạo 10 kg từ tầng 1 lên tầng 3, cao hơn 6 m.", "Bấm giờ: Minh 20 s, Nam 60 s."],
               "quan_sat": ["Cả hai: A = 100 N · 6 m = 600 J.", "Minh mất ít thời gian hơn."],
               "rut_ra": ["Cùng công chưa cho biết ai nhanh hơn.", "Công suất: Minh 30 W, Nam 10 W."]},
  "tham_so": [{"ky_hieu": "m", "ten": "Khối lượng bao gạo", "don_vi": "kg", "kieu": "dieu_chinh", "min": 5, "max": 25, "mac_dinh": 10, "buoc": 5},
              {"ky_hieu": "h", "ten": "Độ cao", "don_vi": "m", "kieu": "dieu_chinh", "min": 3, "max": 12, "mac_dinh": 6, "buoc": 3},
              {"ky_hieu": "t", "ten": "Thời gian", "don_vi": "s", "kieu": "dieu_chinh", "min": 10, "max": 90, "mac_dinh": 20, "buoc": 5},
              {"ky_hieu": "A", "ten": "Công nâng bao gạo", "don_vi": "J", "kieu": "tinh_ra"},
              {"ky_hieu": "P", "ten": "Công suất", "don_vi": "W", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["F = 10·m (nâng đều)", "A = F·h", "P = A/t"],
              "gia_thiet": ["chỉ tính công đưa bao gạo lên cao, bỏ qua công nâng chính người xách", "đi lên đều"]},
  "so_lieu_mau": {"cot": ["Bạn", "A (J)", "t (s)", "P (W)"], "hang": [["Minh", 600, 20, 30], ["Nam", 600, 60, 10]],
                  "ghi_chu": "Số liệu minh hoạ tính từ mô hình."},
  "ket_qua_ky_vong": "Cùng 600 J; Minh 30 W gấp ba Nam 10 W.",
  "hien_tuong_hay_sai": ["Nghĩ người đi nhanh làm nhiều công hơn.", "Lấy khối lượng 10 kg làm lực thay vì trọng lượng 100 N."],
  "an_toan": "Không chạy trên cầu thang khi mang vật nặng; ví dụ chỉ để tính.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Hai nhân vật leo cầu thang song song với tốc độ chỉnh được; đồng hồ và bảng A, t, P.",
                     "diem_nhan": "Hai cột A bằng nhau, cột P khác nhau."}})
tn.append({**base,
  "id": "tn-l9-congco-03", "ten": "Ba cách cầm sách: giữ yên, đi ngang, nâng lên", "loai": "vi_du", "muc_do": "co_ban",
  "kien_thuc": ["congco.dieu_kien_co_cong", "congco.vuong_goc_khong_cong"],
  "muc_tieu": "Phân biệt cảm giác mỏi tay với công cơ học: lực tay chỉ thực hiện công khi sách dịch chuyển theo hướng lực.",
  "dung_cu": [{"ten": "Quyển sách", "so_luong": 2}, {"ten": "Thước mét", "so_luong": 1}],
  "cac_buoc": {"lam": ["Cầm hai quyển sách đứng yên 1 phút.", "Cầm sách đi ngang 5 m.", "Nâng sách từ mặt bàn lên cao thêm 0,5 m."],
               "quan_sat": ["Cả ba lần tay đều mỏi.", "Chỉ lần thứ ba sách lên cao hơn."],
               "rut_ra": ["Giữ yên: s = 0, A = 0.", "Đi ngang: dịch chuyển vuông góc với lực tay, A = 0.", "Nâng lên: A = F·s."]},
  "tham_so": [{"ky_hieu": "F", "ten": "Lực tay (bằng trọng lượng sách)", "don_vi": "N", "kieu": "co_dinh", "gia_tri": 10},
              {"ky_hieu": "s_ngang", "ten": "Quãng đường đi ngang", "don_vi": "m", "kieu": "dieu_chinh", "min": 0, "max": 5, "mac_dinh": 5, "buoc": 1},
              {"ky_hieu": "h", "ten": "Độ cao nâng", "don_vi": "m", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0.5, "buoc": 0.1},
              {"ky_hieu": "A", "ten": "Công của lực tay", "don_vi": "J", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["giữ yên: A = 0", "đi ngang đều: A = 0 (lực tay vuông góc dịch chuyển)", "nâng đều: A = F·h"],
              "gia_thiet": ["sách nặng khoảng 10 N", "chuyển động đều, lực tay thẳng đứng"]},
  "so_lieu_mau": {"cot": ["Cách cầm", "s theo hướng lực (m)", "A (J)"], "hang": [["giữ yên", 0, 0], ["đi ngang 5 m", 0, 0], ["nâng 0,5 m", 0.5, 5.0]],
                  "ghi_chu": "Số liệu minh hoạ với sách 10 N."},
  "ket_qua_ky_vong": "Chỉ cách nâng lên có công của lực tay (5 J với sách 10 N, nâng 0,5 m).",
  "hien_tuong_hay_sai": ["Nghĩ mỏi tay là có công cơ học.", "Nhân lực tay với quãng đường đi ngang."],
  "an_toan": "Dùng sách nhẹ, không giơ sách quá đầu.",
  "goi_y_mo_phong": {"loai": "so_do_luc", "y_tuong": "Ba nút: giữ yên, đi ngang, nâng lên; vẽ vectơ lực tay và vectơ dịch chuyển, đồng hồ đếm công.",
                     "diem_nhan": "Công chỉ tăng khi vectơ dịch chuyển cùng hướng vectơ lực."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| TN1 A:", [r[2] for r in rows1], "tb=%.2f lệch=%.0f%%" % (A_tb, p_lech))
