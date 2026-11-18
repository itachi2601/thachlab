"""Bài 1. Giới thiệu một số dụng cụ và hoá chất. Thuyết trình một vấn đề khoa học (KHTN 9, lesson_id 128).
Sinh 4 hình SVG + bảng số liệu thí nghiệm + 2 file content/thi-nghiem/tn-l9-modau-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi số liệu tính từ mô hình (assert). Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 15          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def poly(pts, c="currentColor", w=2.4):
    return pts_path(pts, c, w)
def T(x, y, s, c="currentColor", size=18, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def dot(x, y, c="currentColor", r=3.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
def cur(x, y, dx, dy):
    return chevron(x, y, dx, dy, RED, 2.6, 13)
def lamp(cx, cy, r=15):
    k = r * 0.7071
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(251,146,60,.12)" stroke="currentColor" stroke-width="2.4"/>'
            + line(cx - k, cy - k, cx + k, cy + k, "currentColor", 2) + line(cx - k, cy + k, cx + k, cy - k, "currentColor", 2))
def meter(cx, cy, ch, r=22):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            + T(cx, cy + 8, ch, "currentColor", 22, "middle"))
def cell(xp, xn, y):
    """Kí hiệu nguồn một chiều trên dây ngang: bản dài (+) ở xp, bản ngắn dày (−) ở xn."""
    return (line(xp, y - 18, xp, y + 18, "currentColor", 2.4) + line(xn, y - 9, xn, y + 9, "currentColor", 5)
            + T(xp - 6, y - 22, "+", "currentColor", 20, "end") + T(xn + 6, y - 22, "−", "currentColor", 20))

# ---------- Hình 1: đồng hồ đa năng, núm ở thang 20 mA, màn hình báo quá thang
b = ""
b += '<rect x="60" y="10" width="300" height="330" rx="22" fill="rgba(251,146,60,.10)" stroke="currentColor" stroke-width="2.4"/>'
b += '<rect x="90" y="28" width="240" height="72" rx="6" fill="rgba(56,189,248,.14)" stroke="currentColor" stroke-width="2"/>'
b += ('<text x="104" y="86" fill="currentColor" font-size="54" font-weight="400" '
      'font-family="\'Courier New\', monospace">1</text>')
KX, KY, KR, LR = 210, 205, 34, 72
POS = [("OFF", 0), ("2V", -40), ("20V", -80), ("200V", -120), ("20mA", 40), ("200mA", 80), ("10A", 120)]
def polar(r, a):
    t = math.radians(a)
    return KX + r * math.sin(t), KY - r * math.cos(t)
for lab, a in POS:
    x1, y1 = polar(KR + 6, a); x2, y2 = polar(KR + 16, a)
    b += line(x1, y1, x2, y2, "currentColor", 2)
    x, y = polar(LR, a)
    anc = "middle" if a == 0 else ("end" if a < 0 else "start")
    col = RED if lab == "20mA" else "currentColor"
    b += T(round(x, 1), round(y + 6, 1), lab, col, 16, anc)
b += f'<circle cx="{KX}" cy="{KY}" r="{KR}" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2.4"/>'
px, py = polar(KR - 4, 40)
b += line(KX, KY, px, py, RED, 5)
b += T(74, 132, "DCV", "currentColor", 15, "start", "800") + T(346, 132, "DCA", "currentColor", 15, "end", "800")
for x, lab in ((150, "10A"), (210, "COM"), (270, "VΩmA")):
    b += f'<circle cx="{x}" cy="300" r="10" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    b += T(x, 330, lab, "currentColor", 14, "middle", "600")
fig1 = wrap("0 0 420 350", "Đồng hồ đo điện đa năng: núm vặn chỉ thang 20 mA, màn hình chỉ hiện số 1 ở bên trái", b,
            "Hình 1. Núm vặn ở thang 20&nbsp;mA (vạch đỏ).<br>Màn hình chỉ hiện số 1 ở bên trái.")

# ---------- Hình 2: sơ đồ mắc đúng (ampe kế nối tiếp, vôn kế song song với đèn)
b = ""
X0, X1, Y0, Y1 = 50, 300, 60, 240
AX, VY, RA = 175, 150, 22
PX, NX = 168, 182
J1, J2 = 100, 200
KT, KB = 125, 175
LY = 150
W = 2.4
b += poly([(PX, Y1), (X0, Y1), (X0, KB)], "currentColor", W)
b += poly([(X0, KT), (X0, Y0), (AX - RA, Y0)], "currentColor", W)
b += poly([(AX + RA, Y0), (X1, Y0), (X1, LY - 15)], "currentColor", W)
b += poly([(X1, LY + 15), (X1, Y1), (NX, Y1)], "currentColor", W)
b += dot(X0, KT, "currentColor", 4) + dot(X0, KB, "currentColor", 4) + line(X0, KB, X0, KT, "currentColor", 3)
b += T(X0 + 14, 156, "K", "currentColor", 18)
b += cell(PX, NX, Y1)
b += T(175, Y1 + 40, "biến áp nguồn", "currentColor", 16, "middle", "600")
b += meter(AX, Y0, "A")
b += T(AX - RA - 4, Y0 - 12, "+", "currentColor", 20, "end") + T(AX + RA + 4, Y0 - 12, "−", "currentColor", 20)
b += lamp(X1, LY)
b += T(X1 - 24, LY + 7, "Đ", "currentColor", 21, "end")
b += dot(X1, J1) + dot(X1, J2)
b += poly([(X1, J1), (390, J1), (390, VY - RA)], "currentColor", W)
b += poly([(390, VY + RA), (390, J2), (X1, J2)], "currentColor", W)
b += meter(390, VY, "V")
b += T(400, VY - RA - 2, "+", "currentColor", 20) + T(400, VY + RA + 18, "−", "currentColor", 20)
b += cur(110, Y1, -1, 0) + cur(X0, 100, 0, -1) + cur(245, Y0, 1, 0) + cur(X1, 225, 0, 1)
b += T(20, 312, "Mũi tên đỏ: chiều dòng điện, từ (+) về (−)", RED, 16)
assert PX < NX and 110 < PX and 240 > NX
fig2 = wrap("0 0 440 322", "Sơ đồ mạch đúng: biến áp nguồn, khoá K, ampe kế nối tiếp, bóng đèn Đ, vôn kế song song với đèn", b,
            "Hình 2. Ampe kế nằm ngay trên đường dòng điện (nối tiếp).<br>Vôn kế bắc qua hai đầu đèn (song song).")

# ---------- Hình 3: cấu trúc bài thuyết trình Mở – Thân – Kết
b = ""
boxes = [(10, "MỞ", "1–2 slide", ("nêu câu hỏi", "vì sao đáng", "quan tâm"), BLUE),
         (150, "THÂN", "3–5 slide", ("số liệu, hình", "thí nghiệm", "có nguồn"), ORG),
         (290, "KẾT", "1 slide", ("trả lời", "câu hỏi", "chốt ý chính"), GRN)]
for x, ttl, sl, rows, col in boxes:
    b += f'<rect x="{x}" y="40" width="120" height="130" rx="10" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="2.4"/>'
    b += T(x + 60, 28, sl, "currentColor", 14, "middle", "600")
    b += T(x + 60, 70, ttl, "currentColor", 19, "middle", "800")
    for k, r in enumerate(rows):
        b += T(x + 60, 100 + 24 * k, r, "currentColor", 15, "middle", "600")
for xa in (130, 270):
    b += line(xa + 2, 105, xa + 17, 105, "currentColor", 2.4) + chevron(xa + 18, 105, 1, 0, "currentColor", 2.4, 9)
b += '<rect x="10" y="186" width="400" height="34" rx="8" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4"/>'
b += T(210, 209, "Sau cùng: hỏi – đáp với người nghe", "currentColor", 16, "middle", "700")
fig3 = wrap("0 0 420 228", "Ba khối Mở, Thân, Kết của bài thuyết trình nối nhau bằng mũi tên, dưới cùng là phần hỏi đáp", b,
            "Hình 3. Bài thuyết trình: Mở – Thân – Kết, rồi hỏi – đáp.")

# ---------- Hình 4: hai cách mắc NHẦM (không ghi hậu quả trên hình để khỏi lộ đáp án Câu 4)
def panel(oy, kind):
    g = ""
    X0, X1, Y0, Y1 = 50, 230, oy + 56, oy + 180
    LYc = (Y0 + Y1) / 2
    PX, NX = 133, 147
    g += poly([(PX, Y1), (X0, Y1), (X0, Y0)], "currentColor", W)
    if kind == "a":
        g += poly([(X0, Y0), (X1, Y0), (X1, LYc - 15)], "currentColor", W)
    else:
        VX = 140
        g += poly([(X0, Y0), (VX - 22, Y0)], "currentColor", W) + poly([(VX + 22, Y0), (X1, Y0), (X1, LYc - 15)], "currentColor", W)
        g += meter(VX, Y0, "V")
    g += poly([(X1, LYc + 15), (X1, Y1), (NX, Y1)], "currentColor", W)
    g += lamp(X1, LYc) + T(X1 - 24, LYc + 7, "Đ", "currentColor", 21, "end")
    g += cell(PX, NX, Y1)
    g += T(140, Y1 + 42, "nguồn 6 V", "currentColor", 15, "middle", "600")
    if kind == "a":
        ja, jb = Y0 + 20, Y1 - 20
        g += dot(X1, ja) + dot(X1, jb)
        g += poly([(X1, ja), (330, ja), (330, LYc - 22)], "currentColor", W)
        g += poly([(330, LYc + 22), (330, jb), (X1, jb)], "currentColor", W)
        g += meter(330, LYc, "A")
        g += T(12, oy + 26, "a) Ampe kế mắc song song với đèn", "currentColor", 17)
    else:
        g += T(12, oy + 26, "b) Vôn kế mắc nối tiếp với đèn", "currentColor", 17)
    return g
b = panel(0, "a") + line(10, 236, 410, 236, "currentColor", 1.2, "5 5", .5) + panel(244, "b")
fig4 = wrap("0 0 420 474", "Hai sơ đồ mắc nhầm: a) ampe kế mắc song song với bóng đèn; b) vôn kế mắc nối tiếp với bóng đèn", b,
            "Hình 4. Hai cách mắc nhầm ampe kế và vôn kế.")

# ---------- Thí nghiệm 1: một dòng điện, ba thang (đồng hồ số 3½ chữ số, giới hạn hiển thị 1999)
I_TRUE = 0.15318                       # A, dòng thật qua đèn nhỏ ở nguồn 3 V (minh hoạ)
THANG = [("10 A", 10.0, 0.01, "A"), ("200 mA", 0.2, 0.0001, "mA"), ("20 mA", 0.02, 0.00001, "mA")]
rows1 = []
for ten, ghd, buoc, dv in THANG:
    if I_TRUE > ghd:
        rows1.append((ten, None, None))
        continue
    doc = round(I_TRUE / buoc) * buoc
    rows1.append((ten, doc, dv))
assert rows1[2][1] is None                                  # quá thang 20 mA
I_A = round(rows1[0][1], 2); I_B = round(rows1[1][1] * 1000, 1)
assert I_A == 0.15 and I_B == 153.2, (I_A, I_B)
SS_A = 0.01 / I_A * 100; SS_B = 0.1 / I_B * 100
assert 6.5 < SS_A < 7 and 0.06 < SS_B < 0.07, (SS_A, SS_B)
assert abs(I_B / 1000 - I_A) < 0.005                       # hai kết quả không mâu thuẫn
bang1 = "\n".join([
    "<tr><td>10&nbsp;A</td><td>0.15</td><td>$0{,}15\\ \\text{A}$</td></tr>",
    "<tr><td>200&nbsp;mA</td><td>153.2</td><td>$153{,}2\\ \\text{mA}$</td></tr>",
    "<tr><td>20&nbsp;mA</td><td>1&nbsp;(bên trái)</td><td>quá thang</td></tr>"])
NX1 = ("$153{,}2\\ \\text{mA} = 0{,}1532\\ \\text{A}{:}$ khớp $0{,}15\\ \\text{A}$ ở thang 10&nbsp;A.<br>"
       "Thang 10&nbsp;A chỉ hiện tới phần trăm ampe: lệch một đơn vị là $0{,}01\\ \\text{A},$ khoảng $7\\ \\%.$<br>"
       "Thang 200&nbsp;mA hiện tới $0{,}1\\ \\text{mA}{:}$ lệch một đơn vị chỉ khoảng $0{,}07\\ \\%.$<br>"
       "Thang 20&nbsp;mA nhỏ hơn dòng cần đo nên không đọc được.")

# ---------- Thí nghiệm 2: vôn kế (đồng hồ số, R_V = 10 MΩ) nối tiếp với đèn 6 V – 0,5 A, nguồn 6 V
U_N, R_V, R_D = 6.0, 10e6, 12.0
I2 = U_N / (R_V + R_D)
U_V = I2 * R_V
assert abs(U_V - 6.00) < 0.005 and I2 < 1e-6

# ---------- Kiểm số trong bài
assert 0.5 * 1000 > 200 and 6 > 2 and 6 < 20                 # tình huống mẫu: 10 A, 20 V
assert 0.3 * 1000 > 200 and 2.5 > 2                          # điền bước: 10 A, 20 V
assert 15 < 20 and 3 > 2 and 3 < 20                          # Câu 7: 20 mA, 20 V
assert 2 < 9 < 20                                            # ⭐: 20 V

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in (("__BANG_TN1__", bang1), ("__NHAN_XET_TN1__", NX1), ("__TN1_A__", "0{,}15"), ("__TN1_B__", "153{,}2"),
             ("__SS_A__", "7"), ("__SS_B__", "0{,}07"), ("__PHUT__", str(PHUT))):
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 1. Giới thiệu một số dụng cụ và hoá chất. Thuyết trình một vấn đề khoa học"
SRC = "content/lesson-samples/l9-mo-dau-dung-cu-thuyet-trinh/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 128, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-modau-01", "ten": "Đo một dòng điện ở ba thang của đồng hồ đa năng", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["dungcu.chon_thang_do", "dungcu.ampe_ke_noi_tiep", "dungcu.sai_so_do"],
  "muc_tieu": "Thấy cùng một dòng điện đọc ở thang lớn thì thô, ở thang vừa thì nhiều chữ số nhất, ở thang quá nhỏ thì báo quá thang.",
  "dung_cu": [{"ten": "Đồng hồ đo điện đa năng số (thang DCA 20 mA, 200 mA, 10 A)", "so_luong": 1},
              {"ten": "Bóng đèn nhỏ có đui", "so_luong": 1},
              {"ten": "Nguồn 3 V (hai pin hoặc biến áp nguồn)", "so_luong": 1},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mắc đồng hồ nối tiếp với bóng đèn, que đỏ về phía cực (+) của nguồn.",
                       "Đặt thang 10 A (que đỏ cắm lỗ 10A), đóng khoá, đọc số.",
                       "Tắt khoá, chuyển que đỏ về lỗ mA, đặt thang 200 mA, đọc số; rồi thang 20 mA."],
               "quan_sat": ["Thang 10 A: 0.15 (A).", "Thang 200 mA: 153.2 (mA).", "Thang 20 mA: chỉ hiện số 1 bên trái.", "Đèn sáng như nhau cả ba lần."],
               "rut_ra": ["Dòng điện không đổi, chỉ cách hiển thị đổi theo thang.",
                          "Thang nhỏ nhất mà giới hạn đo vẫn lớn hơn số đo cho nhiều chữ số nhất.",
                          "Thang nhỏ hơn số đo thì báo quá thang, có thể làm đứt cầu chì."]},
  "tham_so": [{"ky_hieu": "I", "ten": "Cường độ dòng điện thật trong mạch", "don_vi": "A", "kieu": "dieu_chinh", "min": 0.001, "max": 5, "mac_dinh": I_TRUE, "buoc": 0.001},
              {"ky_hieu": "GHD", "ten": "Giới hạn đo của thang (0,02 / 0,2 / 10 A)", "don_vi": "A", "kieu": "dieu_chinh", "min": 0.02, "max": 10, "mac_dinh": 10, "buoc": 0.02},
              {"ky_hieu": "I_doc", "ten": "Số hiện trên màn hình", "don_vi": "A", "kieu": "do_duoc", "sai_so_do": 0.01},
              {"ky_hieu": "delta", "ten": "Sai số khi lệch một đơn vị chữ số cuối", "don_vi": "%", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["buoc = GHD/2000 (đồng hồ 3½ chữ số: 10 A → 0,01 A; 200 mA → 0,1 mA; 20 mA → 0,01 mA)",
                               "nếu I > GHD: hiện '1' bên trái (quá thang)", "I_doc = lam_tron(I, buoc)", "delta = buoc / I_doc · 100 %"],
              "gia_thiet": ["thang 10 A hiển thị tới 0,01 A", "bỏ qua điện trở của đồng hồ (dòng thật không đổi khi đổi thang)",
                            "số liệu minh hoạ, chưa đo thật"]},
  "so_lieu_mau": {"cot": ["Thang", "Màn hình", "Đọc ra"],
                  "hang": [["10 A", "0.15", "0,15 A"], ["200 mA", "153.2", "153,2 mA"], ["20 mA", "1 (bên trái)", "quá thang"]],
                  "ghi_chu": f"Số liệu minh hoạ từ dòng thật {I_TRUE} A, làm tròn theo bước của từng thang; chưa phải số đo thật."},
  "ket_qua_ky_vong": "Thang 200 mA cho 153,2 mA (sai số ~0,07 %), thang 10 A cho 0,15 A (~7 %), thang 20 mA quá thang.",
  "hien_tuong_hay_sai": ["Nghĩ thang nhỏ nhất luôn chính xác nhất.", "Đọc số 1 bên trái thành 1 mA.",
                         "Đọc 153.2 ở thang 200 mA thành 153,2 A (quên đơn vị của thang)."],
  "sai_so_thuong_gap": "Lệch một đơn vị chữ số cuối: 0,01 A trên 0,15 A ≈ 7 %; 0,1 mA trên 153,2 mA ≈ 0,07 %.",
  "an_toan": "Đổi thang khi đã ngắt khoá. Dòng lớn hơn 200 mA phải dùng lỗ 10A.",
  "goi_y_mo_phong": {"loai": "bang_so_lieu", "y_tuong": "Vặn núm đồng hồ ảo qua các thang; màn hình hiện số theo bước làm tròn, quá thang thì hiện 1.",
                     "diem_nhan": "Thang nhỏ quá thì không đọc được; thang lớn quá thì mất chữ số."}})
tn.append({**base,
  "id": "tn-l9-modau-02", "ten": "Vôn kế mắc nối tiếp với bóng đèn: đèn tắt, vôn kế chỉ gần bằng hiệu điện thế nguồn", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["dungcu.von_ke_song_song", "dungcu.mac_nham_dung_cu"],
  "muc_tieu": "Thấy vôn kế (điện trở rất lớn) mắc nối tiếp làm mạch gần như hở: đèn không sáng, vôn kế đo hiệu điện thế của nguồn chứ không phải của đèn.",
  "dung_cu": [{"ten": "Đồng hồ đo điện đa năng số, thang DCV 20 V (điện trở vào khoảng 10 MΩ)", "so_luong": 1},
              {"ten": "Bóng đèn 6 V – 0,5 A có đui", "so_luong": 1},
              {"ten": "Biến áp nguồn chỉnh ra 6 V một chiều", "so_luong": 1},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Tắt nguồn, mắc đồng hồ (thang 20 V) nối tiếp với bóng đèn.", "Bật nguồn 6 V, đóng khoá, quan sát đèn và đọc đồng hồ."],
               "quan_sat": ["Đèn không sáng.", "Đồng hồ chỉ khoảng 6,00 V."],
               "rut_ra": ["Điện trở vôn kế rất lớn nên dòng gần như bằng 0.",
                          "Gần như cả hiệu điện thế nguồn rơi trên vôn kế: nó không đo hiệu điện thế của đèn.",
                          "Muốn đo hiệu điện thế của đèn, vôn kế phải mắc song song với đèn."]},
  "tham_so": [{"ky_hieu": "U_n", "ten": "Hiệu điện thế nguồn", "don_vi": "V", "kieu": "dieu_chinh", "min": 0, "max": 12, "mac_dinh": U_N, "buoc": 0.5},
              {"ky_hieu": "R_V", "ten": "Điện trở vôn kế", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": R_V},
              {"ky_hieu": "R_D", "ten": "Điện trở bóng đèn (nguội, coi không đổi)", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": R_D},
              {"ky_hieu": "I", "ten": "Cường độ dòng trong mạch", "don_vi": "A", "kieu": "tinh_ra"},
              {"ky_hieu": "U_V", "ten": "Số chỉ vôn kế", "don_vi": "V", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["I = U_n / (R_V + R_D)", "U_V = I · R_V"],
              "gia_thiet": ["bỏ qua điện trở dây nối và nguồn", "coi điện trở đèn không đổi"]},
  "so_lieu_mau": {"cot": ["U_n (V)", "I (A)", "U_V (V)"],
                  "hang": [[U_N, float(f"{I2:.2e}"), round(U_V, 2)]],
                  "ghi_chu": "Số liệu tính từ mô hình, chưa phải số đo thật."},
  "ket_qua_ky_vong": "Dòng khoảng 0,6 µA, đèn tắt; vôn kế chỉ 6,00 V.",
  "hien_tuong_hay_sai": ["Nghĩ vôn kế nối tiếp vẫn đo đúng hiệu điện thế của đèn.", "Nghĩ mắc nhầm vôn kế cũng nguy hiểm như mắc nhầm ampe kế."],
  "an_toan": "Chỉ làm thử với vôn kế. KHÔNG làm thử ampe kế mắc song song (nối tắt nguồn, dòng rất lớn).",
  "goi_y_mo_phong": {"loai": "so_do_luc+bang_so_lieu", "y_tuong": "Kéo thả vôn kế/ampe kế vào vị trí nối tiếp hoặc song song; đèn sáng/tắt và số chỉ đổi theo.",
                     "diem_nhan": "Vôn kế nối tiếp: đèn tắt, số chỉ bằng U nguồn. Ampe kế song song: báo nối tắt."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| TN1:", I_A, "A,", I_B, "mA, SS %.1f%% / %.3f%%" % (SS_A, SS_B), "| TN2 U_V=%.3f I=%.2e" % (U_V, I2))
