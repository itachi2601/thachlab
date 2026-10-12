"""Bài 2. Động năng. Thế năng (KHTN 9, lesson_id 129).
Sinh 4 hình SVG + bảng số liệu thí nghiệm đo + 3 file content/thi-nghiem/tn-l9-dongthe-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi số liệu tính từ mô hình (assert). Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 13          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên

def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", "{,}")
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def T(x, y, s, c="currentColor", size=17, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'
def dimv(x, y1, y2, lab, c=ORG, side="end"):
    """Kích thước dọc hai đầu V + nhãn bên trái (side=end) hoặc phải."""
    b = line(x, y1, x, y2, c, 2) + chevron(x, y1, 0, y1 - y2, c, 2, 10) + chevron(x, y2, 0, y2 - y1, c, 2, 10)
    b += line(x - 8, y1, x + 8, y1, c, 1.6) + line(x - 8, y2, x + 8, y2, c, 1.6)
    dx = -10 if side == "end" else 10
    return b + T(x + dx, (y1 + y2) / 2 + 6, lab, c, 18, side)
def dimh(y, x1, x2, lab, c=ORG):
    b = line(x1, y, x2, y, c, 2) + chevron(x1, y, x1 - x2, 0, c, 2, 10) + chevron(x2, y, x2 - x1, 0, c, 2, 10)
    b += line(x1, y - 8, x1, y + 8, c, 1.6) + line(x2, y - 8, x2, y + 8, c, 1.6)
    return b + T((x1 + x2) / 2, y + 24, lab, c, 18, "middle")

# ---------- Hình 1: chung cư, chậu cây trên lan can tầng 8 (không ghi số, không lộ đáp án)
b = ""
GY = 286                                   # mặt sân
BX0, BX1 = 70, 230
b += f'<rect x="{BX0}" y="20" width="{BX1 - BX0}" height="{GY - 20}" fill="rgba(56,189,248,.08)" stroke="currentColor" stroke-width="2.2"/>'
FL = (GY - 20) / 8                          # 8 tầng
for k in range(1, 8):
    y = GY - k * FL
    b += line(BX0, y, BX1, y, "currentColor", 1, "", .35)
for k in range(8):
    y = GY - (k + 1) * FL + 9
    for x in (88, 140):
        b += f'<rect x="{x}" y="{y:.1f}" width="34" height="{FL - 16:.1f}" rx="2" fill="none" stroke="currentColor" stroke-width="1.2" opacity=".5"/>'
# lan can tầng 8 và tầng 2 nhô ra bên phải
for fl in (8, 2):
    yb = GY - (fl - 1) * FL                 # sàn của tầng fl
    b += line(BX1, yb, BX1 + 44, yb, "currentColor", 2.4) + line(BX1 + 44, yb, BX1 + 44, yb - 18, "currentColor", 2.4)
    b += T(BX1 + 52, yb - 2, f"tầng {fl}", "currentColor", 17, "start")
yb8 = GY - 7 * FL
# chậu cây trên thành lan can tầng 8
cx, cy = BX1 + 44, yb8 - 18
b += f'<path d="M{cx - 12},{cy - 22} L{cx + 12},{cy - 22} L{cx + 8},{cy} L{cx - 8},{cy} Z" fill="rgba(251,146,60,.35)" stroke="currentColor" stroke-width="2"/>'
b += f'<path d="M{cx},{cy - 22} q-14,-14 -6,-28 M{cx},{cy - 22} q4,-18 16,-24 M{cx},{cy - 22} q-2,-12 -18,-12" fill="none" stroke="{GRN}" stroke-width="2.4"/>'
b += line(cx, cy + 6, cx, GY - 8, "currentColor", 1.2, "4 6", .45)
b += line(16, GY, 404, GY, "currentColor", 2.4)
b += T(300, GY - 8, "sân", "currentColor", 17, "start")
b += T(cx - 34, cy - 30, "?", RED, 26, "middle")
fig1 = wrap("0 0 420 300", "Toà chung cư tám tầng; một chậu cây đặt trên thành lan can tầng 8, bên dưới là sân", b,
            "Hình 1. Chậu cây đứng yên trên lan can tầng 8.<br>Nó có năng lượng không?")

# ---------- Hình 2: viên bi lăn xuống máng nghiêng va khúc gỗ (thí nghiệm 1, định tính)
b = ""
Y0 = 196                                     # mặt bàn
AX, AY, BXm = 40, 70, 200                    # đỉnh máng (AX,AY) xuống chân máng (BXm, Y0)
b += line(AX, AY, BXm, Y0, "currentColor", 2.6) + line(BXm, Y0, 404, Y0, "currentColor", 2.6)
b += f'<path d="M{AX},{AY} L{AX},{Y0} L{BXm},{Y0}" fill="rgba(148,163,184,.12)" stroke="none"/>'
ang = math.atan2(Y0 - AY, BXm - AX)
r = 11
bx, by = AX + 26 * math.cos(ang) + r * math.sin(ang), AY + 26 * math.sin(ang) - r * math.cos(ang)
b += f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{r}" fill="rgba(148,163,184,.5)" stroke="currentColor" stroke-width="2"/>'
# mũi tên chiều lăn
ux, uy = math.cos(ang), math.sin(ang)
b += line(bx + 22 * ux + 14 * uy, by + 22 * uy - 14 * ux, bx + 70 * ux + 14 * uy, by + 70 * uy - 14 * ux, RED, 2.6)
b += chevron(bx + 70 * ux + 14 * uy, by + 70 * uy - 14 * ux, ux, uy, RED, 2.6, 12)
# khúc gỗ trước và sau
G0, GW, GH = 250, 46, 30
b += f'<rect x="{G0}" y="{Y0 - GH}" width="{GW}" height="{GH}" rx="3" fill="rgba(251,146,60,.3)" stroke="currentColor" stroke-width="2.2"/>'
G1 = 340
b += f'<rect x="{G1}" y="{Y0 - GH}" width="{GW}" height="{GH}" rx="3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="5 4" opacity=".7"/>'
b += dimv(22, by, Y0, it_("h"), ORG)
b += dimh(Y0 + 22, G0, G1, it_("s"))
b += T(70, 34, "viên bi thép", "currentColor", 17, "start")
b += T(G0 - 4, Y0 - GH - 14, "khúc gỗ", "currentColor", 17, "start")
fig2 = wrap("0 0 420 250", "Viên bi thép lăn xuống máng nghiêng từ độ cao h, va vào khúc gỗ trên mặt bàn, đẩy khúc gỗ đi một quãng s", b,
            "Hình 2. Bi lăn từ độ cao <em>h</em>, đẩy khúc gỗ đi quãng <em>s</em>.<br>Nét đứt: chỗ khúc gỗ dừng lại.")

# ---------- Thí nghiệm 2: xe lăn qua cổng quang, d = 2,0 cm, đồng hồ 0,0001 s
D = 0.020
DO2 = [(0.20, 0.0198), (0.20, 0.0101), (0.40, 0.0202), (0.40, 0.0099)]
rows2 = []
for m, dt in DO2:
    v = round(D / dt, 2)
    W = 0.5 * m * v * v
    rows2.append((m, dt, v, round(W, 3)))
assert [r_[2] for r_ in rows2] == [1.01, 1.98, 0.99, 2.02]
assert [r_[3] for r_ in rows2] == [0.102, 0.392, 0.196, 0.816]
k_v = rows2[1][3] / rows2[0][3]; k_m = rows2[2][3] / rows2[0][3]; k_mv = rows2[3][3] / rows2[2][3]
assert 3.7 < k_v < 4.1 and 1.85 < k_m < 2.1 and 3.9 < k_mv < 4.3
bang2 = "\n".join(f"<tr><td>${vn(m, 2)}$</td><td>${vn(dt, 4)} \\to {vn(v, 2)}$</td><td>${vn(W, 3)}$</td></tr>"
                  for m, dt, v, W in rows2)
NX2 = (f"Cùng $m = 0{{,}}20\\ \\text{{kg}}{{:}}$ $v$ từ ${vn(rows2[0][2], 2)}$ lên ${vn(rows2[1][2], 2)}$ (gần gấp 2), "
       f"$W_{{\\text{{đ}}}}$ gấp ${vn(k_v, 2)}$ lần, gần 4.<br>"
       f"Cùng $v$ gần $1\\ \\text{{m/s}}{{:}}$ $m$ gấp 2, $W_{{\\text{{đ}}}}$ gấp ${vn(k_m, 2)}$ lần, gần 2.<br>"
       f"Lệch một chút vì mỗi lượt đẩy xe không đúng y một tốc độ.")
U_TN2 = None

# ---------- Hình 3: xe lăn, tấm chắn sáng, cổng quang, đồng hồ
b = ""
RY = 176
b += line(16, RY, 404, RY, "currentColor", 2.6)
CX0, CX1 = 60, 160
b += f'<rect x="{CX0}" y="{RY - 40}" width="{CX1 - CX0}" height="30" rx="4" fill="rgba(56,189,248,.18)" stroke="currentColor" stroke-width="2.2"/>'
for wx in (CX0 + 18, CX1 - 18):
    b += f'<circle cx="{wx}" cy="{RY - 8}" r="8" fill="none" stroke="currentColor" stroke-width="2.2"/>'
FX0, FX1 = 100, 122                          # tấm chắn sáng, bề rộng d theo phương chuyển động
b += f'<rect x="{FX0}" y="{RY - 84}" width="{FX1 - FX0}" height="44" fill="rgba(251,146,60,.45)" stroke="currentColor" stroke-width="1.8"/>'
b += line(FX0, RY - 96, FX1, RY - 96, ORG, 1.8) + line(FX0, RY - 102, FX0, RY - 88, ORG, 1.6) + line(FX1, RY - 102, FX1, RY - 88, ORG, 1.6)
b += T((FX0 + FX1) / 2, RY - 108, it_("d"), ORG, 18, "middle")
# vectơ vận tốc
b += line(CX1 + 6, RY - 26, CX1 + 56, RY - 26, RED, 2.6) + chevron(CX1 + 56, RY - 26, 1, 0, RED, 2.6, 12)
b += T(CX1 + 30, RY - 36, it_("v"), RED, 18, "middle")
# cổng quang hình chữ U ngược, chùm sáng ngang tấm chắn
GX = 270
b += f'<path d="M{GX - 16},{RY} L{GX - 16},{RY - 92} L{GX + 16},{RY - 92} L{GX + 16},{RY}" fill="none" stroke="currentColor" stroke-width="3"/>'
b += line(GX - 16, RY - 62, GX + 16, RY - 62, RED, 2, "3 3")
b += T(GX - 24, RY - 100, "cổng quang", "currentColor", 17, "end")
# đồng hồ
b += f'<rect x="300" y="24" width="104" height="44" rx="6" fill="rgba(52,211,153,.12)" stroke="currentColor" stroke-width="2"/>'
b += T(352, 54, "Δ" + it_("t"), GRN, 20, "middle")
b += f'<path d="M{GX + 16},{RY - 80} C{GX + 40},{RY - 80} 330,100 340,68" fill="none" stroke="currentColor" stroke-width="1.6"/>'
b += T(16, 30, "xe lăn", "currentColor", 17, "start") + line(40, 36, 80, RY - 42, "currentColor", 1.2, "", .6)
fig3 = wrap("0 0 420 200", "Xe lăn mang tấm chắn sáng bề rộng d chạy trên máng ngang qua cổng quang; đồng hồ đo thời gian chắn sáng delta t", b,
            "Hình 3. Tấm chắn rộng <em>d</em> đi qua chùm sáng trong thời gian Δ<em>t</em>.<br>Tốc độ xe: <em>v</em> = <em>d</em> : Δ<em>t</em>.")

# ---------- Thí nghiệm 3: quả nặng rơi xuống cát. Mô hình: độ sâu lõm x = Wt / F_cản, F_cản = 20 N
FC = 20.0
DO3 = [(0.1, 0.20), (0.1, 0.40), (0.2, 0.20)]
rows3 = [(m, h, round(10 * m * h, 2), round(10 * m * h / FC * 100, 1)) for m, h in DO3]
assert [r_[2] for r_ in rows3] == [0.2, 0.4, 0.4] and [r_[3] for r_ in rows3] == [1.0, 2.0, 2.0]

# ---------- Hình 4: hai lần thả quả nặng 100 g từ 20 cm và 40 cm xuống khay cát (không vẽ vết lõm)
b = ""
SY = 228                                     # mặt cát
K = 4.0                                      # px / cm
for x0, hcm, tag in ((40, 20, "(a)"), (240, 40, "(b)")):
    b += f'<rect x="{x0 - 10}" y="{SY}" width="130" height="24" rx="3" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2"/>'
    b += T(x0 + 55, SY + 18, "khay cát", "currentColor", 15, "middle", "600")
    cx = x0 + 55
    ybot = SY - K * hcm
    b += f'<rect x="{cx - 12}" y="{ybot - 26:.1f}" width="24" height="26" rx="4" fill="rgba(148,163,184,.55)" stroke="currentColor" stroke-width="2"/>'
    b += line(cx, ybot - 26, cx, ybot - 34, "currentColor", 2) + f'<circle cx="{cx}" cy="{ybot - 38:.1f}" r="4" fill="none" stroke="currentColor" stroke-width="2"/>'
    b += line(cx, ybot + 6, cx, SY - 8, BLUE, 1.8, "5 4") + chevron(cx, SY - 6, 0, 1, BLUE, 2, 10)
    b += dimv(cx + 36, ybot, SY, f"{hcm} cm", ORG, "start")
    b += T(cx - 18, ybot - 8, "100 g", "currentColor", 17, "end")
    b += T(x0 + 55, SY + 50, tag, "currentColor", 17, "middle")
assert SY - K * 40 - 42 > 8
fig4 = wrap("0 0 420 286", "Hai lần thả quả nặng 100 gam xuống khay cát: lần a từ độ cao 20 xentimét, lần b từ 40 xentimét", b,
            "Hình 4. Thả cùng quả nặng 100 g từ hai độ cao.<br>Lần nào vết lõm sâu hơn?")

# ---------- Kiểm số liệu quiz / bài toán mẫu / thử thách
Wd = lambda m, v: 0.5 * m * v * v
assert Wd(0.45, 20) == 90                                                     # ví dụ bóng đá
assert Wd(1000, 10) == 50000 and Wd(1000, 36) == 648000 and 0.5 * 1000 * 10 == 5000 and 1000 * 100 == 100000   # Câu 2
assert 10 * 0.2 * 3 == 6 and abs(10 * 200 * 3 - 6000) < 1e-9 and abs(0.2 * 3 - 0.6) < 1e-12 and abs(0.5 * 10 * 0.2 * 3 - 3) < 1e-12  # Câu 3
assert Wd(1, 60 / 3.6) / Wd(1, 30 / 3.6) - 4 < 1e-9                           # Câu 4
assert 10 * 0.5 * 0.8 == 4 and abs(0.5 * 0.8 - 0.4) < 1e-12 and 10 * 0.5 == 5  # Câu 5
v1, v2 = 36 / 3.6, 54 / 3.6
assert abs(Wd(150, v1) - 7500) < 1e-6 and abs(Wd(150, v2) - 16875) < 1e-6 and abs(Wd(150, v2) - Wd(150, v1) - 9375) < 1e-6
vc = math.sqrt(2 * 7500 / 3000)
assert abs(vc ** 2 - 5) < 1e-9 and abs(vc - 2.236) < 1e-3 and abs(vc * 3.6 - 8.05) < 0.01           # bài toán mẫu
assert abs(Wd(150, 5) - 1875) < 1e-9 and Wd(150, v1) / Wd(150, 5) == 4                              # điền bước
vb = math.sqrt(2 * 7500 / 60)
assert abs(vb - 15.81) < 0.01 and abs(vb * 3.6 - 56.9) < 0.1                                         # thử sức
assert Wd(0.5, 4) == 4 and 10 * 0.5 * 2 == 10 and 0.5 * 0.5 * 4 == 1 and 0.5 * 16 == 8 and 0.5 * 2 == 1   # Câu 7
assert Wd(2000, 20) == 400000 and abs(math.sqrt(5 / 0.5) - 3.162) < 1e-3                             # thử thách

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in (("__BANG_TN2__", bang2), ("__NHAN_XET_TN2__", NX2), ("__PHUT__", str(PHUT))):
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 2. Động năng. Thế năng"
SRC = "content/lesson-samples/l9-dong-nang-the-nang/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 129, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-dongthe-01", "ten": "Viên bi lăn xuống máng nghiêng va vào khúc gỗ", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["dongnang.khai_niem", "dongnang.phu_thuoc_m_v"],
  "muc_tieu": "Thấy vật đang chuyển động có năng lượng (đẩy được khúc gỗ); bi càng nặng, tới càng nhanh thì khúc gỗ đi càng xa.",
  "dung_cu": [{"ten": "Máng nghiêng có thước đo độ cao", "so_luong": 1},
              {"ten": "Viên bi thép 50 g và 100 g", "so_luong": 2},
              {"ten": "Khúc gỗ nhỏ", "so_luong": 1},
              {"ten": "Thước đo quãng đường", "so_luong": 1}],
  "cac_buoc": {"lam": ["Thả bi 50 g từ độ cao 10 cm, đo quãng s khúc gỗ bị đẩy đi.",
                       "Thả bi 50 g từ 20 cm, đo s.",
                       "Thả bi 100 g từ 10 cm, đo s."],
               "quan_sat": ["Thả cao hơn: bi tới nhanh hơn, khúc gỗ đi xa hơn.",
                            "Bi nặng hơn, cùng độ cao: khúc gỗ đi xa hơn."],
               "rut_ra": ["Vật đang chuyển động có năng lượng: động năng.",
                          "Khối lượng càng lớn, tốc độ càng lớn thì động năng càng lớn."]},
  "tham_so": [{"ky_hieu": "m", "ten": "Khối lượng bi", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.02, "max": 0.2, "mac_dinh": 0.05, "buoc": 0.01},
              {"ky_hieu": "h", "ten": "Độ cao thả bi", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.05, "max": 0.3, "mac_dinh": 0.1, "buoc": 0.05},
              {"ky_hieu": "s", "ten": "Quãng khúc gỗ bị đẩy đi", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.5}],
  "mo_hinh": {"phuong_trinh": ["s = k·m·h với k = 8 cm/(kg·m) (gần đúng)"],
              "gia_thiet": ["coi phần năng lượng bi truyền cho khúc gỗ là như nhau giữa các lần (gần đúng, chỉ dùng để so sánh định tính)",
                            "bi lăn không trượt; không dùng mgh = ½mv² cho bi lăn vì có động năng quay"]},
  "so_lieu_mau": {"cot": ["m (g)", "h (cm)", "s (cm)"],
                  "hang": [[50, 10, 4.0], [50, 20, 8.0], [100, 10, 8.0]],
                  "ghi_chu": "Số liệu minh hoạ từ mô hình gần đúng s tỉ lệ m·h, chỉ để so sánh xa/gần; chưa phải số đo thật."},
  "ket_qua_ky_vong": "Tăng độ cao thả hoặc khối lượng bi thì khúc gỗ đi xa hơn.",
  "hien_tuong_hay_sai": ["Nghĩ chỉ có tốc độ quyết định, khối lượng bi không quan trọng.",
                         "Nghĩ bi đứng yên ở đỉnh máng không có năng lượng gì."],
  "an_toan": "Đặt vật chắn ở cuối bàn để bi không lăn rơi xuống chân.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Thanh trượt m và h; bi lăn xuống, va khúc gỗ, khúc gỗ trượt rồi dừng, ghi s.",
                     "diem_nhan": "Cho học sinh đoán trước: bi nặng gấp đôi thì khúc gỗ đi xa hơn hay như cũ."}})
tn.append({**base,
  "id": "tn-l9-dongthe-02", "ten": "Đo động năng xe lăn bằng cổng quang", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["dongnang.cong_thuc", "dongnang.ti_le_v_binh_phuong", "dongnang.sai_so_do"],
  "muc_tieu": "Từ bảng m, Δt tính v = d/Δt và Wđ = ½mv²; thấy v gấp đôi thì Wđ gấp bốn, m gấp đôi thì Wđ gấp đôi.",
  "dung_cu": [{"ten": "Máng ngang ít ma sát", "so_luong": 1},
              {"ten": "Xe lăn 0,20 kg và gia trọng 0,20 kg", "so_luong": 1},
              {"ten": "Tấm chắn sáng rộng 2,0 cm gắn trên xe", "so_luong": 1},
              {"ten": "Cổng quang điện và đồng hồ đo thời gian hiện số (độ chia 0,0001 s)", "so_luong": 1}],
  "cac_buoc": {"lam": ["Gắn tấm chắn 2,0 cm lên xe, đặt cổng quang giữa máng.",
                       "Đẩy xe cho chạy qua cổng quang, đọc Δt; đẩy mạnh hơn, đọc Δt.",
                       "Thêm gia trọng cho xe nặng 0,40 kg, lặp lại hai lần đẩy.",
                       "Tính v = d/Δt và Wđ = ½mv²."],
               "quan_sat": ["Δt: " + "; ".join(f"{dt:.4f}".replace(".", ",") for _, dt in DO2) + " s.",
                            "Wđ: " + "; ".join(f"{W:.3f}".replace(".", ",") for *_, W in rows2) + " J."],
               "rut_ra": ["Cùng m, v gần gấp đôi thì Wđ gần gấp bốn.", "Cùng v, m gấp đôi thì Wđ gần gấp đôi.",
                          "Đo lặp và lấy trung bình Δt để kết luận đáng tin hơn."]},
  "tham_so": [{"ky_hieu": "m", "ten": "Khối lượng xe", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.2, "max": 0.6, "mac_dinh": 0.2, "buoc": 0.2},
              {"ky_hieu": "d", "ten": "Bề rộng tấm chắn", "don_vi": "m", "kieu": "co_dinh", "gia_tri": D},
              {"ky_hieu": "dt", "ten": "Thời gian chắn sáng", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.0001},
              {"ky_hieu": "v", "ten": "Tốc độ v = d/Δt", "don_vi": "m/s", "kieu": "tinh_ra"},
              {"ky_hieu": "Wd", "ten": "Động năng ½mv²", "don_vi": "J", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["v = d/Δt (làm tròn 0,01 m/s)", "Wđ = ½·m·v²"],
              "gia_thiet": ["xe chạy gần như đều khi qua cổng quang (máng ngang, tấm chắn hẹp)",
                            "mỗi lượt đẩy tốc độ lệch ngẫu nhiên vài phần trăm"]},
  "so_lieu_mau": {"cot": ["m (kg)", "Δt (s)", "v (m/s)", "Wđ (J)"],
                  "hang": [[m, dt, v, W] for m, dt, v, W in rows2],
                  "ghi_chu": "Số liệu minh hoạ (Δt chọn lệch nhẹ quanh 0,020 s và 0,010 s), tính đúng theo v = d/Δt, Wđ = ½mv²; chưa phải số đo thật."},
  "ket_qua_ky_vong": "Tỉ số Wđ lần 2/lần 1 ≈ 3,84 (gần 4); lần 3/lần 1 ≈ 1,92 (gần 2).",
  "hien_tuong_hay_sai": ["Nghĩ v gấp đôi thì động năng gấp đôi.", "Tính v = Δt/d.", "Dùng đồng hồ độ chia 0,01 s cho Δt cỡ 0,01 s."],
  "sai_so_thuong_gap": "Δt cỡ 0,01 s mà đồng hồ chỉ tới 0,01 s thì sai số tương đối tới 50 %; độ chia 0,0001 s cho sai số khoảng 1 %.",
  "an_toan": "Đặt vật chắn ở cuối máng để xe không lao khỏi bàn.",
  "goi_y_mo_phong": {"loai": "bang_so_lieu+do_thi", "y_tuong": "Kéo thanh lực đẩy, xe qua cổng quang, đồng hồ hiện Δt; bảng tự tính v và Wđ, vẽ Wđ theo v.",
                     "diem_nhan": "Đồ thị Wđ theo v là đường cong (parabol), không phải đường thẳng."}})
tn.append({**base,
  "id": "tn-l9-dongthe-03", "ten": "Thả quả nặng xuống khay cát từ các độ cao khác nhau", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["thenang.khai_niem", "thenang.phu_thuoc_m_h"],
  "muc_tieu": "Thấy vật ở trên cao có năng lượng (làm lõm cát khi rơi); càng nặng, càng cao thì vết lõm càng sâu.",
  "dung_cu": [{"ten": "Khay cát mịn, gạt phẳng", "so_luong": 1},
              {"ten": "Quả nặng 100 g và 200 g có móc", "so_luong": 2},
              {"ten": "Thước đo độ cao và thước đo độ sâu", "so_luong": 1}],
  "cac_buoc": {"lam": ["Thả quả nặng 100 g từ 20 cm, đo độ sâu vết lõm.", "Gạt phẳng cát, thả quả 100 g từ 40 cm.",
                       "Gạt phẳng cát, thả quả 200 g từ 20 cm."],
               "quan_sat": ["Thả cao hơn, vết lõm sâu hơn.", "Quả nặng hơn, cùng độ cao, vết lõm sâu hơn."],
               "rut_ra": ["Vật ở trên cao có thế năng.", "Khối lượng càng lớn, độ cao càng lớn thì thế năng càng lớn."]},
  "tham_so": [{"ky_hieu": "m", "ten": "Khối lượng quả nặng", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.05, "max": 0.3, "mac_dinh": 0.1, "buoc": 0.05},
              {"ky_hieu": "h", "ten": "Độ cao thả so với mặt cát", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.1, "max": 0.6, "mac_dinh": 0.2, "buoc": 0.1},
              {"ky_hieu": "Wt", "ten": "Thế năng lúc thả (mốc mặt cát)", "don_vi": "J", "kieu": "tinh_ra"},
              {"ky_hieu": "x", "ten": "Độ sâu vết lõm", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.2}],
  "mo_hinh": {"phuong_trinh": ["Wt = 10·m·h", "x = Wt / F_can với F_can = 20 N (gần đúng)"],
              "gia_thiet": ["lấy P = 10m (g ≈ 10 m/s²) như SGK KHTN 9", "coi lực cản của cát không đổi; bỏ qua phần độ sâu lõm khi tính h"]},
  "so_lieu_mau": {"cot": ["m (kg)", "h (m)", "Wt (J)", "x (cm)"],
                  "hang": [list(r_) for r_ in rows3],
                  "ghi_chu": "Số liệu minh hoạ từ mô hình lực cản cát không đổi, chưa phải số đo thật."},
  "ket_qua_ky_vong": "Gấp đôi độ cao hoặc gấp đôi khối lượng thì vết lõm sâu gần gấp đôi.",
  "hien_tuong_hay_sai": ["Nghĩ quả nặng đứng yên trên tay không có năng lượng.", "Nghĩ thế năng chỉ phụ thuộc độ cao, không phụ thuộc khối lượng."],
  "an_toan": "Không thả quả nặng gần tay, chân bạn khác; giữ cát không bắn vào mắt.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Thanh trượt m và h; quả nặng rơi, cắm vào cát, hiện độ sâu lõm và Wt.",
                     "diem_nhan": "Cùng Wt (100 g ở 40 cm và 200 g ở 20 cm) cho cùng độ sâu lõm."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| TN2 v:", [r_[2] for r_ in rows2], "Wd:", [r_[3] for r_ in rows2], "k_v=%.2f k_m=%.2f" % (k_v, k_m))
