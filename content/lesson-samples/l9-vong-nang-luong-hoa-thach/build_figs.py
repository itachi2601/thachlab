"""Bài 16. Vòng năng lượng trên Trái Đất. Năng lượng hoá thạch (KHTN 9, lesson_id 94).
Sinh 4 hình SVG + bảng số liệu thí nghiệm đốt nến + số liệu "Thử sức"/thử thách + 3 file
content/thi-nghiem/tn-l9-hoathach-0N.json, thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi số liệu tính từ mô hình (assert). Chạy: cd <thư mục bài> && python3 build_figs.py
Biến môi trường TN_DIR: ghi file thí nghiệm vào thư mục khác (kiểm trên bản sao kho, không đụng kho thật).
"""
import json, math, os, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TN_DIR = pathlib.Path(os.environ.get("TN_DIR", ROOT / "content" / "thi-nghiem"))
PHUT = 17          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên
GRAY = "#94a3b8"
BROWN = "#a16207"

def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", "{,}")
def vt(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def T(x, y, s, c="currentColor", size=16, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def rect(x, y, w, h, fill="none", c="currentColor", sw=2, rx=6, op=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}" opacity="{op}"/>'
def arr(x1, y1, x2, y2, c, w=2.4, L=11):
    return line(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L)
def tree(x, ground, s=1.0):
    g = line(x, ground, x, ground - 22 * s, BROWN, 3)
    g += f'<circle cx="{x}" cy="{ground - 34 * s:.0f}" r="{14 * s:.0f}" fill="rgba(52,211,153,.35)" stroke="{GRN}" stroke-width="2"/>'
    return g

# ---------- Hình 1: cảnh mở bài (không vẽ Mặt Trời, không lộ đáp án dự đoán)
b = ""
b += line(14, 210, 186, 210, "currentColor", 2.4)                                         # mặt bàn
b += f'<polygon points="70,124 130,124 160,206 40,206" fill="rgba(251,191,36,.22)"/>'      # vùng sáng
b += rect(70, 196, 66, 10, "rgba(56,189,248,.18)", "currentColor", 1.8, 2)               # quyển sách
b += rect(30, 202, 50, 8, "currentColor", "currentColor", 1, 2)                           # đế đèn
b += f'<path d="M55,202 L55,136 L90,99" fill="none" stroke="currentColor" stroke-width="3"/>'
b += f'<path d="M84,98 L116,98 L130,124 L70,124 Z" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2.2"/>'
b += rect(160, 176, 16, 24, "none", "currentColor", 2, 3)                                 # ổ cắm
b += f'<path d="M80,206 C110,214 140,214 160,192" fill="none" stroke="currentColor" stroke-width="1.8"/>'
# cột điện
b += line(215, 80, 200, 210, "currentColor", 2) + line(215, 80, 230, 210, "currentColor", 2)
b += line(203, 96, 227, 96, "currentColor", 2) + line(207, 140, 223, 140, "currentColor", 1.8)
b += f'<path d="M215,80 Q190,120 168,176" fill="none" stroke="currentColor" stroke-width="1.4"/>'
b += f'<path d="M215,80 Q240,96 262,140" fill="none" stroke="currentColor" stroke-width="1.4"/>'
# nhà máy + ống khói + khói + đống than
b += rect(262, 128, 82, 82, "rgba(148,163,184,.18)", "currentColor", 2.2, 3)
b += rect(318, 56, 16, 72, "rgba(148,163,184,.25)", "currentColor", 2, 1)
for cx, cy, r in ((330, 44, 9), (343, 31, 11), (360, 20, 12)):
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GRAY}" opacity=".45"/>'
b += f'<path d="M350,210 L378,184 L408,210 Z" fill="currentColor" opacity=".85"/>'
b += line(250, 210, 412, 210, "currentColor", 2.4)
b += T(12, 26, "Đèn bàn học", "currentColor", 17)
b += T(364, 176, "than", "currentColor", 15)
b += T(196, 244, "Nhà máy nhiệt điện than", BLUE, 16)
fig1 = wrap("0 0 420 258", "Bên trái đèn bàn chiếu sáng quyển sách, dây cắm vào ổ điện; bên phải cột điện nối tới nhà máy nhiệt điện có ống khói và đống than",
            b, "Hình 1. Đèn học sáng nhờ điện từ nhà máy đốt than.<br>Năng lượng ấy lúc đầu từ đâu?")

# ---------- Hình 2: Mặt Trời và các nhánh của vòng năng lượng
PHAN_XA, O_LAI, BAY_HOI = 30, 70, 23
assert PHAN_XA + O_LAI == 100 and BAY_HOI < O_LAI
b = ""
b += f'<circle cx="50" cy="52" r="26" fill="rgba(251,146,60,.35)" stroke="{ORG}" stroke-width="2.4"/>'
for k in range(8):
    a = math.radians(45 * k)
    b += line(50 + 32 * math.cos(a), 52 + 32 * math.sin(a), 50 + 40 * math.cos(a), 52 + 40 * math.sin(a), ORG, 2.2)
b += T(98, 46, "Ánh sáng Mặt Trời tới", "currentColor", 16)
b += T(98, 68, "Trái Đất: 100%", "currentColor", 16)
b += arr(50, 96, 50, 140, ORG, 2.8)
b += arr(50, 112, 140, 98, ORG, 2.2)
b += T(150, 102, f"≈ {PHAN_XA}% phản xạ ra", "currentColor", 15, weight="600")
b += T(150, 122, "không gian", "currentColor", 15, weight="600")
b += rect(14, 142, 240, 36, "rgba(251,146,60,.14)", ORG, 2)
b += T(26, 166, f"≈ {O_LAI}% ở lại Trái Đất", "currentColor", 16)
b += line(34, 178, 34, 329, ORG, 2.4)
rows = [(192, 42, [("Nước:", BLUE, f" bay hơi (≈ {BAY_HOI}%) → mây, mưa → sông")]),
        (246, 42, [("Gió:", GRN, " nóng không đều → gió, sóng, hải lưu")]),
        (300, 58, [("Cây:", "#16a34a", " quang hợp → chuỗi thức ăn"), ("", "", "chôn vùi triệu năm → than, dầu, khí")])]
for y, hgt, lines in rows:
    yc = y + hgt / 2 if len(lines) == 1 else y + 29
    b += line(34, yc, 58, yc, ORG, 2.4) + chevron(60, yc, 1, 0, ORG, 2.4, 10)
    b += rect(62, y, 350, hgt, "none", "currentColor", 1.6, 6, .8)
    for i, (lab, col, rest) in enumerate(lines):
        ty = y + 26 + 22 * i
        lab_s = f'<tspan fill="{col}">{lab}</tspan>' if lab else ""
        b += f'<text x="72" y="{ty}" fill="currentColor" font-size="14" font-weight="600">{lab_s}{rest}</text>'
fig2 = wrap("0 0 420 368", "Sơ đồ: ánh sáng Mặt Trời tới Trái Đất, khoảng 30 phần trăm phản xạ, 70 phần trăm ở lại rồi chia thành ba nhánh nước, gió, cây",
            b, "Hình 2. Ba nhánh của vòng năng lượng: Nước – Gió – Cây.<br>Số liệu làm tròn.")

# ---------- Hình 3: nhiên liệu hoá thạch hình thành (Chôn – Ép – Lâu)
b = ""
X0, X1 = 14, 210
def panel(y0):
    return rect(X0, y0, X1 - X0, 86, "none", "currentColor", 1.6, 4, .7)
# ô 1: rừng đầm lầy cổ
y0 = 12
b += panel(y0)
b += f'<rect x="{X0}" y="{y0 + 68}" width="{X1 - X0}" height="18" fill="rgba(56,189,248,.22)"/>'
for x, s in ((44, 1.0), (92, 1.15), (142, 0.95), (184, 1.05)):
    b += tree(x, y0 + 70, s)
# ô 2: bị chôn
y0 = 110
b += panel(y0)
for i, col in enumerate(("rgba(148,163,184,.25)", "rgba(148,163,184,.4)", "rgba(148,163,184,.55)")):
    b += f'<rect x="{X0}" y="{y0 + 10 + 16 * i}" width="{X1 - X0}" height="16" fill="{col}"/>'
b += f'<rect x="{X0}" y="{y0 + 58}" width="{X1 - X0}" height="16" fill="rgba(52,211,153,.45)"/>'
for x in (60, 112, 164):
    b += arr(x, y0 + 4, x, y0 + 26, "currentColor", 2, 8)
# ô 3: thành vỉa than
y0 = 208
b += panel(y0)
for i in range(4):
    b += f'<rect x="{X0}" y="{y0 + 4 + 13 * i}" width="{X1 - X0}" height="13" fill="rgba(148,163,184,{.25 + .12 * i:.2f})"/>'
b += f'<rect x="{X0}" y="{y0 + 58}" width="{X1 - X0}" height="12" fill="currentColor" opacity=".9"/>'
b += f'<rect x="{X0}" y="{y0 + 70}" width="{X1 - X0}" height="12" fill="rgba(148,163,184,.75)"/>'
labels = [(12, ["1. Rừng đầm lầy cổ", "cây quang hợp,", "rồi chết đi"]),
          (110, ["2. Chôn", "bùn đất phủ kín", "xác cây"]),
          (208, ["3. Ép – Lâu", "nóng, ép triệu năm", "→ vỉa than (đen)"])]
for y0, ls in labels:
    for i, s in enumerate(ls):
        b += T(222, y0 + 24 + 22 * i, s, ORG if i == 0 else "currentColor", 15 if i == 0 else 14, weight="700" if i == 0 else "600")
fig3 = wrap("0 0 420 304", "Ba ô từ trên xuống: rừng đầm lầy cổ; xác cây bị các lớp bùn đất phủ lên; sau hàng triệu năm thành vỉa than đen nằm sâu dưới các lớp đá",
            b, "Hình 3. Than hình thành: Chôn – Ép – Lâu.<br>Dầu mỏ, khí tự nhiên hình thành tương tự từ sinh vật biển nhỏ.")

# ---------- Hình 4: sơ đồ nhà máy nhiệt điện than (dữ liệu của tình huống mẫu, không ghi dạng năng lượng)
b = ""
b += f'<path d="M14,206 L40,178 L68,206 Z" fill="currentColor" opacity=".85"/>'
b += T(18, 170, "Than", "currentColor", 15)
b += arr(64, 196, 84, 182, "currentColor", 2.2, 9)
b += rect(86, 100, 72, 106, "rgba(148,163,184,.18)", "currentColor", 2.2, 4)
b += f'<path d="M104,198 C98,180 112,172 108,156 C120,166 126,150 122,140 C136,156 140,178 132,198 Z" fill="rgba(251,146,60,.55)" stroke="{ORG}" stroke-width="1.6"/>'
b += T(122, 124, "Lò hơi", "currentColor", 14, "middle")
b += rect(132, 30, 16, 70, "rgba(148,163,184,.25)", "currentColor", 2, 1)
for cx, cy, r in ((144, 20, 8), (158, 12, 9)):
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GRAY}" opacity=".45"/>'
b += T(156, 44, "Ống khói", "currentColor", 14, weight="600")
b += line(158, 120, 196, 120, BLUE, 3) + chevron(198, 120, 1, 0, BLUE, 2.6, 10)
b += T(162, 112, "hơi", BLUE, 13, weight="600")
b += f'<path d="M200,98 L246,88 L246,152 L200,142 Z" fill="rgba(56,189,248,.18)" stroke="currentColor" stroke-width="2.2"/>'
b += T(196, 80, "Tua bin", "currentColor", 15)
b += line(246, 120, 272, 120, "currentColor", 3)
b += f'<circle cx="296" cy="120" r="24" fill="rgba(251,191,36,.18)" stroke="currentColor" stroke-width="2.2"/>'
b += T(296, 126, "G", "currentColor", 16, "middle")
b += T(262, 166, "Máy phát", "currentColor", 15)
b += f'<path d="M223,148 L223,222 L122,222 L122,208" fill="none" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="5 4"/>'
b += chevron(122, 208, 0, -1, BLUE, 1.8, 9)
b += line(320, 120, 368, 120, "currentColor", 2) + line(368, 120, 368, 160, "currentColor", 2)
b += f'<path d="M352,170 L384,150 L410,170 L410,206 L352,206 Z" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += T(410, 228, "Tới nhà em", "currentColor", 15, "end")
fig4 = wrap("0 0 420 240", "Sơ đồ nhà máy nhiệt điện than: than vào lò hơi có lửa và ống khói, hơi nước sang tua bin, tua bin quay máy phát, dây điện tới nhà",
            b, "Hình 4. Sơ đồ đơn giản nhà máy nhiệt điện than.<br>Nét đứt: hơi nước ngưng lại, quay về lò.")

# ---------- Thí nghiệm 2: đốt nến đun 200 g nước (mô hình)
M_NUOC, C_NUOC, Q_PARAFIN = 200, 4.18, 42.0e3       # g, J/(g·K), J/g (giá trị tra cứu xấp xỉ)
TOC_DO, ETA0, T0, T_LOSS = 0.12, 0.22, 28.0, 50.0   # g/phút; phần nhiệt vào nước lúc đầu; °C; hệ số mất nhiệt
# Nghiệm đúng của m·c·dT/dt = eta0·(1 − (T − T0)/T_LOSS)·q·v  →  T = T0 + T_LOSS·(1 − e^(−K·t/T_LOSS)),
# K = eta0·q·v/(m·c) (°C/phút). Đây là NGUỒN SỰ THẬT duy nhất cho bảng, so_lieu_mau, quan_sat, ket_qua_ky_vong.
import math
K_TANG = ETA0 * Q_PARAFIN * TOC_DO / (M_NUOC * C_NUOC)
def T_nuoc(t):
    return T0 + T_LOSS * (1 - math.exp(-K_TANG * t / T_LOSS))
rows2 = [(t, round(TOC_DO * t, 2), round(T_nuoc(t), 1)) for t in (0, 2, 4, 6, 8)]
assert [r[0] for r in rows2] == [0, 2, 4, 6, 8], rows2
inc = [rows2[i + 1][2] - rows2[i][2] for i in range(4)]
assert all(inc[i] >= inc[i + 1] - 1e-9 for i in range(3)) and inc[0] > inc[-1] and 2.0 < inc[0] < 3.0, inc
bang2 = "\n".join(f"<tr><td>${t}$</td><td>${vn(m, 2)}$</td><td>${vn(T, 1)}$</td></tr>" for t, m, T in rows2)
NX2 = (f"Mỗi $2$ phút nến cháy khoảng ${vn(rows2[1][1], 2)}\\ \\text{{g}},$ nước nóng thêm khoảng ${vn(inc[0], 1)}$ đến ${vn(inc[-1], 1)}\\ ^\\circ\\text{{C}}.$<br>"
       f"Nến cháy gấp đôi (${vn(rows2[1][1], 2)}$ lên ${vn(rows2[2][1], 2)}\\ \\text{{g}}$) thì nước nóng thêm gần gấp đôi.<br>"
       "Về cuối nước nóng chậm hơn một chút: nước càng nóng càng mất nhiệt ra không khí.<br>"
       "Sai số đến từ gió làm lửa lệch, khoảng cách lửa – đáy lon, và cân chỉ chính xác tới $0{,}01\\ \\text{g}.$")

# ---------- Thử sức đổi nhiên liệu (số liệu bảng của tài liệu nguồn) + thử thách CO2
Q_CUI, Q_THANBUN, Q_KHI = 10, 14, 44        # MJ/kg
M_TB = 1.8
E_TB = M_TB * Q_THANBUN
M_CUI, M_KHI = E_TB / Q_CUI, E_TB / Q_KHI
assert abs(E_TB - 25.2) < 1e-9 and abs(M_CUI - 2.52) < 1e-9 and abs(M_KHI - 0.5727) < 1e-3
C_PT = 80
M_C = C_PT / 100
M_CO2 = M_C * 44 / 12
assert abs(M_CO2 - 2.933) < 1e-3 and M_CO2 > 1

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in (("__BANG_TN2__", bang2), ("__NX_TN2__", NX2), ("__PHUT__", str(PHUT)),
             ("__TB_KG__", vn(M_TB, 1)), ("__TB_MJ__", vn(E_TB, 1)), ("__CUI_KG__", vn(M_CUI, 2)), ("__KHI_KG__", vn(M_KHI, 2)),
             ("__C_PT__", str(C_PT)), ("__C_KG__", vn(M_C, 1)), ("__CO2_KG__", vn(M_CO2, 1))):
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 16. Vòng năng lượng trên Trái Đất. Năng lượng hoá thạch"
SRC = "content/lesson-samples/l9-vong-nang-luong-hoa-thach/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 94, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-hoathach-01", "ten": "Mô hình vòng tuần hoàn nước trong bát thuỷ tinh", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["vongnangluong.vong_nuoc", "vongnangluong.mat_troi_nguon_goc"],
  "muc_tieu": "Thấy nhiệt làm nước bay hơi, hơi gặp lạnh ngưng thành giọt và rơi lại: mô hình thu nhỏ vòng nước do Mặt Trời duy trì.",
  "dung_cu": [{"ten": "Bát thuỷ tinh trong", "so_luong": 1}, {"ten": "Nước ấm khoảng 50 °C", "so_luong": 1},
              {"ten": "Màng bọc thực phẩm", "so_luong": 1}, {"ten": "Vài viên nước đá", "so_luong": 1},
              {"ten": "Đèn bàn hoặc nắng trực tiếp", "so_luong": 1}],
  "cac_buoc": {"lam": ["Rót nước ấm vào bát, bọc kín miệng bát bằng màng bọc thực phẩm.",
                       "Đặt vài viên đá lên giữa màng, để bát dưới nắng hoặc đèn bàn 10–15 phút."],
               "quan_sat": ["Mặt dưới màng mờ hơi nước.", "Giọt nước to dần ngay dưới chỗ đá rồi nhỏ xuống bát."],
               "rut_ra": ["Nhiệt làm nước bay hơi; hơi gặp lạnh ngưng thành giọt; giọt rơi lại: một vòng khép kín.",
                          "Ngoài trời, Mặt Trời là nguồn nhiệt, không khí lạnh trên cao đóng vai viên đá."]},
  "tham_so": [{"ky_hieu": "T_nuoc", "ten": "Nhiệt độ nước ban đầu", "don_vi": "°C", "kieu": "dieu_chinh", "min": 25, "max": 60, "mac_dinh": 50, "buoc": 5},
              {"ky_hieu": "T_da", "ten": "Nhiệt độ mặt màng dưới đá", "don_vi": "°C", "kieu": "co_dinh", "gia_tri": 5},
              {"ky_hieu": "t_giot", "ten": "Thời gian tới giọt đầu tiên rơi", "don_vi": "phút", "kieu": "do_duoc", "sai_so_do": 0.5}],
  "mo_hinh": {"phuong_trinh": ["tốc độ bay hơi tăng khi T_nuoc tăng", "hơi ngưng ở chỗ màng lạnh nhất (dưới đá)"],
              "gia_thiet": ["định tính, không đo lượng nước", "bát kín nên hơi không thoát ra ngoài"]},
  "so_lieu_mau": {"cot": ["Nước ban đầu", "Hiện tượng sau 10 phút"],
                  "hang": [["nước ấm 50 °C", "màng mờ, giọt rơi dưới chỗ đá"], ["nước nguội 25 °C", "màng hơi mờ, chưa có giọt rơi"]],
                  "ghi_chu": "Mô tả định tính minh hoạ, chưa phải quan sát ghi thật."},
  "ket_qua_ky_vong": "Có giọt nước rơi lại vào bát ngay dưới chỗ đặt đá.",
  "hien_tuong_hay_sai": ["Nghĩ giọt nước dưới màng là nước đá tan thấm qua màng.", "Nghĩ mưa không liên quan Mặt Trời."],
  "an_toan": "Dùng nước ấm, không dùng nước sôi với bát thuỷ tinh mỏng.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Hạt hơi nước bốc lên khi bật nguồn nhiệt, gặp lớp lạnh thì gom thành giọt rơi.",
                     "diem_nhan": "Tắt nguồn nhiệt thì vòng chậm hẳn: nước chỉ quay vòng khi có năng lượng cấp vào."}})
tn.append({**base,
  "id": "tn-l9-hoathach-02", "ten": "Đốt nến parafin đun 200 g nước: năng lượng hoá học thành nhiệt, kèm CO2", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["hoathach.dot_chay_toa_nhiet", "hoathach.thai_co2", "hoathach.sai_so_do"],
  "muc_tieu": "Từ bảng số liệu thấy nến (sản phẩm dầu mỏ) cháy càng nhiều thì nước càng nóng; nhận ra phần lớn nhiệt thất thoát và có CO2 thải ra.",
  "dung_cu": [{"ten": "Nến parafin", "so_luong": 1}, {"ten": "Lon nhôm chứa 200 g nước, giá đỡ", "so_luong": 1},
              {"ten": "Nhiệt kế (ĐCNN 0,1 °C)", "so_luong": 1}, {"ten": "Cân điện tử (ĐCNN 0,01 g)", "so_luong": 1},
              {"ten": "Cốc thuỷ tinh khô, nước vôi trong", "so_luong": 1}, {"ten": "Đồng hồ bấm giờ", "so_luong": 1}],
  "cac_buoc": {"lam": ["Cân nến, đặt lon chứa 200 g nước trên ngọn nến ở khoảng cách cố định.",
                       "Cứ 2 phút ghi nhiệt độ nước và cân lại nến, trong 8 phút.",
                       "Úp cốc khô lên ngọn nến, rồi lắc cốc với nước vôi trong."],
               "quan_sat": ["Nhiệt độ nước tăng từ " + vt(rows2[0][2]) + " °C lên " + vt(rows2[-1][2]) + " °C khi nến cháy " + vt(rows2[-1][1], 2) + " g.",
                            "Thành cốc mờ hơi nước; nước vôi trong vẩn đục."],
               "rut_ra": ["Đốt nhiên liệu chuyển năng lượng hoá học thành nhiệt (và ánh sáng).",
                          "Đốt nhiên liệu từ dầu mỏ thải CO2 và hơi nước.",
                          "Phần lớn nhiệt thoát ra không khí, chỉ một phần vào nước."]},
  "tham_so": [{"ky_hieu": "t", "ten": "Thời gian đốt", "don_vi": "phút", "kieu": "dieu_chinh", "min": 0, "max": 8, "mac_dinh": 8, "buoc": 2},
              {"ky_hieu": "m_nuoc", "ten": "Khối lượng nước", "don_vi": "g", "kieu": "co_dinh", "gia_tri": M_NUOC},
              {"ky_hieu": "v_chay", "ten": "Tốc độ cháy của nến", "don_vi": "g/phút", "kieu": "co_dinh", "gia_tri": TOC_DO},
              {"ky_hieu": "q", "ten": "Nhiệt toả ra khi đốt 1 g parafin (xấp xỉ)", "don_vi": "J/g", "kieu": "co_dinh", "gia_tri": Q_PARAFIN},
              {"ky_hieu": "eta0", "ten": "Phần nhiệt vào nước lúc đầu", "don_vi": "", "kieu": "co_dinh", "gia_tri": ETA0},
              {"ky_hieu": "T", "ten": "Nhiệt độ nước", "don_vi": "°C", "kieu": "do_duoc", "sai_so_do": 0.1},
              {"ky_hieu": "dm", "ten": "Khối lượng nến đã cháy", "don_vi": "g", "kieu": "do_duoc", "sai_so_do": 0.01}],
  "mo_hinh": {"phuong_trinh": ["dm/dt = v_chay", "eta = eta0·(1 − (T − T0)/50)", "m_nuoc·c·dT/dt = eta·q·v_chay, c = 4,18 J/(g·K), T0 = 28 °C",
                                  "nghiệm: T = T0 + 50·(1 − e^(−K·t/50)), K = eta0·q·v_chay/(m_nuoc·c) ≈ 1,33 °C/phút"],
              "gia_thiet": ["q parafin xấp xỉ 42 kJ/g (giá trị tra cứu, dao động 41–46 kJ/g)",
                            "phần nhiệt vào nước giảm dần khi nước nóng lên do mất nhiệt ra không khí",
                            "bỏ qua nhiệt làm nóng lon"]},
  "so_lieu_mau": {"cot": ["t (phút)", "Nến đã cháy (g)", "Nước (°C)"],
                  "hang": [[t, m, T] for t, m, T in rows2],
                  "ghi_chu": "Số liệu minh hoạ tính từ mô hình, chưa phải số đo thật."},
  "ket_qua_ky_vong": "Nước tăng khoảng " + vt(rows2[-1][2] - rows2[0][2]) + " °C trong 8 phút; mức tăng mỗi 2 phút giảm dần nhẹ.",
  "hien_tuong_hay_sai": ["Nghĩ toàn bộ nhiệt của nến đi vào nước.", "Nghĩ đốt nến chỉ sinh nhiệt, không thải khí gì.",
                         "Nghĩ lửa to hơn thì sai số nhỏ đi."],
  "sai_so_thuong_gap": "Gió làm lửa lệch, khoảng cách lửa – đáy lon thay đổi, cân chỉ chính xác 0,01 g (khoảng 4 % ở 0,24 g).",
  "an_toan": "Có lửa: buộc gọn tóc, đặt nến trên khay kim loại, không để gần giấy; lon và nước nóng.",
  "goi_y_mo_phong": {"loai": "bang_so_lieu+do_thi", "y_tuong": "Kéo thời gian, nến ngắn dần, nhiệt kế tăng; mũi tên nhiệt chia phần vào nước và phần thoát ra.",
                     "diem_nhan": "Phần nhiệt vào nước chỉ là một phần nhỏ, và kèm theo luôn có CO2."}})
tn.append({**base,
  "id": "tn-l9-hoathach-03", "ten": "Đổi nhiên liệu đun nấu: củi khô, than bùn, khí tự nhiên cho cùng nhiệt lượng", "loai": "vi_du", "muc_do": "co_ban",
  "kien_thuc": ["hoathach.nhiet_toa_moi_kg", "hoathach.uu_diem"],
  "muc_tieu": "So khối lượng các nhiên liệu cần để cho cùng một nhiệt lượng; thấy nhiên liệu hoá thạch như khí tự nhiên toả nhiều nhiệt trên mỗi kg.",
  "dung_cu": [{"ten": "Bảng nhiệt toả ra khi đốt cháy hoàn toàn 1 kg nhiên liệu", "so_luong": 1}],
  "cac_buoc": {"lam": ["Tính nhiệt toả ra khi đốt 1,8 kg than bùn.", "Chia nhiệt ấy cho nhiệt toả ra của 1 kg củi khô, 1 kg khí tự nhiên."],
               "quan_sat": [f"1,8 kg than bùn cho {vt(E_TB)} MJ.", f"Cần {vt(M_CUI, 2)} kg củi khô hoặc {vt(M_KHI, 2)} kg khí tự nhiên."],
               "rut_ra": ["Cùng nhiệt lượng, khí tự nhiên cần ít khối lượng nhất: một ưu điểm của nhiên liệu hoá thạch."]},
  "tham_so": [{"ky_hieu": "m_tb", "ten": "Khối lượng than bùn mỗi ngày", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.5, "max": 5, "mac_dinh": M_TB, "buoc": 0.1},
              {"ky_hieu": "q_cui", "ten": "Nhiệt toả ra của 1 kg củi khô", "don_vi": "MJ/kg", "kieu": "co_dinh", "gia_tri": Q_CUI},
              {"ky_hieu": "q_tb", "ten": "Nhiệt toả ra của 1 kg than bùn", "don_vi": "MJ/kg", "kieu": "co_dinh", "gia_tri": Q_THANBUN},
              {"ky_hieu": "q_khi", "ten": "Nhiệt toả ra của 1 kg khí tự nhiên", "don_vi": "MJ/kg", "kieu": "co_dinh", "gia_tri": Q_KHI},
              {"ky_hieu": "m_cui", "ten": "Khối lượng củi khô tương đương", "don_vi": "kg", "kieu": "tinh_ra"},
              {"ky_hieu": "m_khi", "ten": "Khối lượng khí tự nhiên tương đương", "don_vi": "kg", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["Q = m_tb·q_tb", "m_cui = Q/q_cui", "m_khi = Q/q_khi"],
              "gia_thiet": ["đốt cháy hoàn toàn", "hiệu suất bếp như nhau với mọi nhiên liệu",
                            "số liệu nhiệt toả ra lấy từ bảng trong tài liệu KHTN 9 (Kết nối tri thức)"]},
  "so_lieu_mau": {"cot": ["Nhiên liệu", "Nhiệt toả ra (MJ/kg)", "Khối lượng cho 25,2 MJ (kg)"],
                  "hang": [["than bùn", Q_THANBUN, M_TB], ["củi khô", Q_CUI, round(M_CUI, 2)], ["khí tự nhiên", Q_KHI, round(M_KHI, 3)]],
                  "ghi_chu": "Tính từ bảng số liệu của tài liệu nguồn."},
  "ket_qua_ky_vong": f"Củi khô {vt(M_CUI, 2)} kg, khí tự nhiên khoảng {vt(M_KHI, 2)} kg.",
  "hien_tuong_hay_sai": ["Nhân thay vì chia khi đổi sang nhiên liệu khác.", "Nghĩ nhiên liệu nặng hơn thì toả nhiều nhiệt hơn."],
  "goi_y_mo_phong": {"loai": "bang_so_lieu", "y_tuong": "Kéo khối lượng than bùn, ba cột khối lượng nhiên liệu tương đương đổi theo.",
                     "diem_nhan": "Khí tự nhiên cần ít khối lượng nhất cho cùng nhiệt lượng."}})
TN_DIR.mkdir(parents=True, exist_ok=True)
for dct in tn:
    (TN_DIR / f"{dct['id']}.json").write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| TN2:", rows2, "inc:", [round(x, 2) for x in inc],
      "| than bùn:", E_TB, M_CUI, round(M_KHI, 3), "| CO2:", round(M_CO2, 3))
