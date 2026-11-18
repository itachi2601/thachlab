"""Bài 17. Một số dạng năng lượng tái tạo (KHTN 9, lesson_id 95).
Sinh 3 hình SVG + bảng số liệu thí nghiệm + số liệu tình huống mẫu + 2 file content/thi-nghiem/tn-l9-taitao-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi số liệu tính từ mô hình (assert). Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 16          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên


def vn(x, nd=1):
    """Số cho KaTeX: dấu phẩy thập phân {,}, nhóm nghìn bằng \\,."""
    s = f"{x:,.{nd}f}".replace(",", "@").replace(".", "{,}").replace("@", "\\,")
    return s
def vt(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def T(x, y, s, c="currentColor", size=16, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def sun(cx, cy, r=20):
    g = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(251,146,60,.35)" stroke="{ORG}" stroke-width="2.4"/>'
    for k in range(8):
        a = math.radians(45 * k)
        g += line(cx + (r + 5) * math.cos(a), cy + (r + 5) * math.sin(a), cx + (r + 14) * math.cos(a), cy + (r + 14) * math.sin(a), ORG, 2.4)
    return g
def cloud(cx, cy, s=1.0):
    g = ""
    for dx, dy, r in ((-26, 4, 16), (-6, -8, 20), (18, -2, 17), (34, 8, 12), (4, 10, 15)):
        g += f'<circle cx="{cx + dx * s:.1f}" cy="{cy + dy * s:.1f}" r="{r * s:.1f}" fill="rgba(148,163,184,.30)" stroke="none"/>'
    g += (f'<path d="M{cx - 42 * s:.1f},{cy + 18 * s:.1f} H{cx + 46 * s:.1f}" stroke="currentColor" stroke-width="1.6" opacity=".5"/>')
    return g
def turbine(x, ground, top, L=48, ang0=-90):
    g = f'<path d="M{x - 5},{ground} L{x - 2},{top} L{x + 2},{top} L{x + 5},{ground} z" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="1.8"/>'
    for k in range(3):
        a = math.radians(ang0 + 120 * k)
        ex, ey = x + L * math.cos(a), top + L * math.sin(a)
        nx, ny = -math.sin(a) * 4, math.cos(a) * 4
        g += (f'<path d="M{x + nx:.1f},{top + ny:.1f} L{ex:.1f},{ey:.1f} L{x - nx:.1f},{top - ny:.1f} z" '
              f'fill="rgba(56,189,248,.25)" stroke="currentColor" stroke-width="1.6"/>')
    g += f'<circle cx="{x}" cy="{top}" r="5" fill="currentColor"/>'
    return g

# ---------- Hình 1: cảnh mở bài Ninh Thuận (chỉ cảnh, không nói tác động)
b = sun(48, 46)
G = 200
b += line(10, G, 410, G, "currentColor", 2)
for row, (y0, x0) in enumerate(((120, 30), (156, 18))):
    for k in range(3):
        x = x0 + 62 * k
        b += (f'<path d="M{x},{y0} L{x + 50},{y0} L{x + 40},{y0 + 22} L{x - 10},{y0 + 22} z" fill="rgba(56,189,248,.28)" '
              f'stroke="currentColor" stroke-width="1.8"/>')
        b += line(x + 20, y0 + 6, x + 15, y0 + 17, "currentColor", 1, "", .5)
        b += line(x + 15, y0 + 22, x + 15, 156 if row == 0 else G, "currentColor", 1.6)   # chân hàng trên dừng ở mép hàng dưới
b += turbine(300, G, 78) + turbine(378, G, 98, 40, -60)
b += T(14, 232, "cánh đồng pin mặt trời", BLUE, 16)
b += T(406, 232, "tua-bin gió", BLUE, 16, "end")
fig1 = wrap("0 0 420 248", "Cánh đồng pin mặt trời bên trái, hai tua-bin gió bên phải, Mặt Trời ở góc trên", b,
            "Hình 1. Ven quốc lộ 1 qua Ninh Thuận.<br>Nắng, gió có sẵn và không có khói: thế đã đủ chưa?")

# ---------- Hình 2: chuỗi hồ – ống – tua-bin – máy phát
b = ""
WS, WB = 72, 214            # mặt nước hồ, đáy hồ
b += f'<path d="M10,{WS} L150,{WS} L150,{WB} L10,{WB} z" fill="rgba(56,189,248,.22)" stroke="none"/>'
b += line(10, WS, 150, WS, BLUE, 2.4)
b += '<path d="M150,52 L172,52 L212,236 L150,236 z" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="2"/>'
b += line(6, 236, 420, 236, "currentColor", 1.6, "", .6)
TX, TY = 300, 222           # tâm tua-bin
P0, P1 = (156, 182), (TX - 20, TY - 6)
b += f'<line x1="{P0[0]}" y1="{P0[1]}" x2="{P1[0]}" y2="{P1[1]}" stroke="{BLUE}" stroke-width="11" stroke-linecap="round" opacity=".45"/>'
for f in (0.35, 0.7):        # chiều nước chảy: từ hồ xuống tua-bin
    x, y = P0[0] + (P1[0] - P0[0]) * f, P0[1] + (P1[1] - P0[1]) * f
    b += chevron(x, y, P1[0] - P0[0], P1[1] - P0[1], "currentColor", 2.2, 9)
assert P1[0] > P0[0] and P1[1] > P0[1]                       # nước chảy xuống, sang phải
b += f'<circle cx="{TX}" cy="{TY}" r="18" fill="rgba(52,211,153,.2)" stroke="currentColor" stroke-width="2.4"/>'
for k in range(4):
    a = math.radians(45 * k + 20)
    b += line(TX - 14 * math.cos(a), TY - 14 * math.sin(a), TX + 14 * math.cos(a), TY + 14 * math.sin(a), "currentColor", 2)
b += line(TX, TY - 18, TX, 160, "currentColor", 3)              # trục nối tua-bin – máy phát
b += '<rect x="258" y="112" width="84" height="48" rx="8" fill="rgba(251,146,60,.15)" stroke="currentColor" stroke-width="2.2"/>'
b += T(300, 142, "máy phát", "currentColor", 13, "middle")
b += line(342, 126, 412, 126, "currentColor", 2) + chevron(412, 126, 1, 0, "currentColor", 2, 9)
b += line(TX + 18, TY + 6, 404, 230, BLUE, 2.2, "5 4") + chevron(404, 230, 1, 0.08, BLUE, 2, 9)
b += T(40, 140, "hồ", "currentColor", 17)
b += T(178, 44, "đập", "currentColor", 16)
b += T(TX, 260, "tua-bin", "currentColor", 15, "middle")
b += T(14, 62, "thế năng", ORG, 15)
b += T(206, 182, "động năng", ORG, 14)
b += T(326, 216, "cơ năng", ORG, 15)
b += T(346, 116, "điện năng", ORG, 14)
fig2 = wrap("0 0 430 270", "Nhà máy thuỷ điện: nước hồ sau đập chảy theo ống dẫn xuống tua-bin, tua-bin quay máy phát, điện đi ra lưới; chữ cam ghi dạng năng lượng ở từng chặng", b,
            "Hình 2. Hồ – ống – tua-bin – máy phát.<br>Chữ cam: dạng năng lượng ở từng chặng.")

# ---------- Hình 3: Mặt Trời đưa nước lên núi (vòng nước → hồ thuỷ điện)
b = sun(42, 44)
SEA = 226
b += f'<path d="M6,{SEA} L142,{SEA} L142,262 L6,262 z" fill="rgba(56,189,248,.25)" stroke="none"/>' + line(6, SEA, 142, SEA, BLUE, 2.2)
for x in (60, 104):           # hơi nước bốc lên
    b += line(x, SEA - 6, x, 118, BLUE, 2, "5 4") + chevron(x, 118, 0, -1, BLUE, 2, 9)
b += cloud(282, 60)
SL = lambda x: 246 - (x - 228) * 150 / 102        # sườn trái núi: (228,246) → (330,96)
for k in range(4):            # mưa rơi xuống sườn núi
    x = 262 + 16 * k
    y2 = SL(x - 8) - 12
    assert y2 > 104
    b += line(x, 92, x - 8, y2, BLUE, 2)
b += '<path d="M228,246 L330,96 L420,246 z" fill="rgba(52,211,153,.18)" stroke="currentColor" stroke-width="2"/>'
RS = (250, SL(250))
b += pts_path(cubic(RS, (238, 222), (226, 228), (214, 234)), BLUE, 3)
b += chevron(214, 234, -1, 0.5, BLUE, 2.2, 9)
b += f'<path d="M160,226 L214,226 L214,244 L160,244 z" fill="rgba(56,189,248,.35)" stroke="none"/>'
b += '<rect x="148" y="212" width="12" height="34" fill="rgba(148,163,184,.6)" stroke="currentColor" stroke-width="1.6"/>'
b += line(142, 246, 420, 246, "currentColor", 1.4, "", .5)
b += T(86, 50, "Mặt Trời", ORG, 15)
b += T(114, 160, "bốc hơi", BLUE, 15)
b += T(282, 28, "mây", "currentColor", 15, "middle")
b += T(214, 112, "mưa", BLUE, 15)
b += T(166, 264, "hồ", "currentColor", 15)
b += T(132, 204, "đập", "currentColor", 15)
b += T(20, 256, "biển", "currentColor", 15)
fig3 = wrap("0 0 424 272", "Mặt Trời làm nước biển bốc hơi thành mây, mây mưa trên núi, nước chảy về hồ sau đập thuỷ điện", b,
            "Hình 3. Mặt Trời đưa nước lên cao.<br>Bốc hơi → mây → mưa trên núi → hồ.<br>Thế năng của nước hồ có gốc từ Mặt Trời.")

# ---------- Thí nghiệm 1: tua-bin gió mô hình, U = k·(v − v0), R = 10 Ω
K_TB, V0, R_TB = 0.6, 1.0, 10.0
V_GIO = (2.0, 3.0, 4.0)
LECH = ((-0.03, 0.02, 0.01), (-0.02, 0.03, -0.01), (-0.04, 0.05, -0.01))   # dao động khi đọc (tổng 0)
rows1 = []
for v, d in zip(V_GIO, LECH):
    u = K_TB * (v - V0)
    doc = [round(u + e, 2) for e in d]
    tb = sum(doc) / 3
    assert abs(tb - u) < 1e-9 and abs(sum(d)) < 1e-12
    rows1.append((v, doc, tb, u * u / R_TB))
U_TB = [round(r[2], 2) for r in rows1]
assert U_TB == [0.60, 1.20, 1.80], U_TB
P_TB = [r[3] for r in rows1]
ratio_P, ratio_U = P_TB[2] / P_TB[0], U_TB[2] / U_TB[0]
assert abs(ratio_P - 9) < 1e-9 and abs(ratio_U - 3) < 1e-9 and (4 / 2) ** 2 == 4      # phương án B=3, C=9, D=4, A=2
spread = max(max(r[1]) - min(r[1]) for r in rows1)
assert abs(spread - 0.09) < 1e-9
SEP = ";\\ "
bang1 = "\n".join(f"<tr><td>${vn(v, 1)}$</td><td>${SEP.join(vn(x, 2) for x in doc)}$</td><td>${vn(tb, 2)}$</td></tr>"
                  for v, doc, tb, _ in rows1)
P_OK = (f"$U$ trung bình từ ${vn(U_TB[0], 2)}$ lên ${vn(U_TB[2], 2)}\\ \\text{{V}}{{:}}$ gấp ${round(ratio_U)}$ lần.<br>"
        f"$P = \\dfrac{{U^2}}{{R}}{{:}}$ từ ${vn(P_TB[0], 3)}$ lên ${vn(P_TB[2], 3)}\\ \\text{{W}},$ gấp ${round(ratio_P)}$ lần.<br>"
        f"Ngược lại, gió yếu đi một nửa thì điện giảm mạnh hơn nhiều.")
NX1 = (f"Ba lần đo ở cùng tốc độ gió lệch nhau tới ${vn(spread, 2)}\\ \\text{{V}}{{:}}$ gió quạt thổi không đều, cánh quay lúc nhanh lúc chậm, kim vôn kế dao động.<br>"
       f"Lấy trung bình ba lần đo để giảm sai số ngẫu nhiên.<br>"
       f"Muốn tin hơn: đo nhiều lần hơn, giữ khoảng cách tua-bin – quạt cố định, đo tốc độ gió ngay trước cánh.<br>"
       f"Dưới khoảng ${vn(V0, 1)}\\ \\text{{m/s}}$ cánh không quay nổi: gió quá yếu thì không có điện.")

# ---------- Tình huống mẫu: đảo dùng pin mặt trời (số liệu giả định)
A_DAO, H_NANG, P_TAM, S_TAM, S_SAN = 1200, 4, 500, 2.2, 28 * 15
A1 = P_TAM / 1000 * H_NANG
N_TAM = A_DAO / A1
P_HE = N_TAM * P_TAM / 1000
S_HE = N_TAM * S_TAM
SAN = S_HE / S_SAN
assert A1 == 2 and N_TAM == 600 and P_HE == 300 and P_HE * H_NANG == A_DAO and abs(S_HE - 1320) < 1e-9 and 3 < SAN < 3.2
H_MUA = 3
A1_MUA = P_TAM / 1000 * H_MUA
N_MUA = A_DAO / A1_MUA
assert A1_MUA == 1.5 and N_MUA == 800
P_GIO, H_GIO = 200, 3
A_GIO = P_GIO * H_GIO
A_CON = A_DAO - A_GIO
N_CON = A_CON / A1
assert A_GIO == 600 and A_CON == 600 and N_CON == 300
N_MAI = 20
Q8 = {"A": N_MAI * P_TAM / 1000, "B": N_MAI * P_TAM / 1000 * H_NANG, "C": N_MAI * P_TAM * H_NANG, "D": P_TAM / 1000 * H_NANG}
assert Q8 == {"A": 10, "B": 40, "C": 40000, "D": 2} and len(set(Q8.values())) == 4

TOK = {"__BANG_TN1__": bang1, "__P_OK__": P_OK, "__NHAN_XET_TN1__": NX1, "__PHUT__": str(PHUT),
       "__A_DAO__": vn(A_DAO, 0), "__H_NANG__": str(H_NANG), "__P_TAM__": str(P_TAM), "__P_TAM_KW__": vn(P_TAM / 1000, 1),
       "__A1__": vn(A1, 0), "__N_TAM__": vn(N_TAM, 0), "__P_HE__": vn(P_HE, 0), "__S_TAM__": vn(S_TAM, 1),
       "__S_HE__": vn(S_HE, 0), "__SAN__": str(math.floor(SAN)), "__H_MUA__": str(H_MUA), "__A1_MUA__": vn(A1_MUA, 1),
       "__N_MUA__": vn(N_MUA, 0), "__P_GIO__": vn(P_GIO, 0), "__H_GIO__": str(H_GIO), "__A_GIO__": vn(A_GIO, 0),
       "__A_CON__": vn(A_CON, 0), "__N_CON__": vn(N_CON, 0), "__N_MAI__": str(N_MAI),
       "__Q8_A__": vn(Q8["A"], 0), "__Q8_B__": vn(Q8["B"], 0), "__Q8_C__": vn(Q8["C"], 0), "__Q8_D__": vn(Q8["D"], 0)}

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in TOK.items():
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", ""), [l for l in h.splitlines() if "__" in l][:3]
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 17. Một số dạng năng lượng tái tạo"
SRC = "content/lesson-samples/l9-nang-luong-tai-tao/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 95, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-taitao-01", "ten": "Tua-bin gió mô hình trước quạt: đo hiệu điện thế theo tốc độ gió", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["taitao.chuoi_chuyen_hoa_gio", "taitao.phu_thuoc_thoi_tiet", "congsuat.p_bang_u2_chia_r"],
  "muc_tieu": "Thấy gió làm quay tua-bin, máy phát cho ra điện; gió gấp đôi thì công suất tăng nhiều hơn gấp đôi, gió yếu thì gần như không có điện.",
  "dung_cu": [{"ten": "Động cơ điện một chiều nhỏ (dùng làm máy phát) gắn cánh quạt nhựa 3 cánh", "so_luong": 1},
              {"ten": "Điện trở 10 Ω", "so_luong": 1},
              {"ten": "Vôn kế (GHĐ 3 V, ĐCNN 0,01 V)", "so_luong": 1},
              {"ten": "Quạt bàn 3 tốc độ", "so_luong": 1},
              {"ten": "Máy đo tốc độ gió cầm tay", "so_luong": 1},
              {"ten": "Dây nối, giá đỡ", "so_luong": 1}],
  "cac_buoc": {"lam": ["Gắn cánh quạt vào trục động cơ, nối hai đầu động cơ với điện trở 10 Ω, vôn kế song song với điện trở.",
                       "Đặt tua-bin trước quạt bàn; đo tốc độ gió ngay trước cánh: " + "; ".join(vt(v, 1) for v in V_GIO) + " m/s.",
                       "Mỗi tốc độ gió đọc vôn kế 3 lần, lấy trung bình."],
               "quan_sat": ["Gió càng mạnh, cánh quay càng nhanh, U càng lớn.",
                            "U trung bình: " + "; ".join(vt(u, 2) for u in U_TB) + " V; ba lần đo lệch nhau tới " + vt(spread, 2) + " V."],
               "rut_ra": ["Động năng gió → cơ năng tua-bin → điện năng.",
                          "Gió từ 2 lên 4 m/s: U gấp 3, công suất P = U²/R gấp 9: điện gió phụ thuộc mạnh vào gió."]},
  "tham_so": [{"ky_hieu": "v", "ten": "Tốc độ gió trước cánh", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0, "max": 5, "mac_dinh": 3, "buoc": 0.5},
              {"ky_hieu": "k", "ten": "Hệ số máy phát mô hình", "don_vi": "V·s/m", "kieu": "co_dinh", "gia_tri": K_TB},
              {"ky_hieu": "v0", "ten": "Tốc độ gió tối thiểu để cánh quay", "don_vi": "m/s", "kieu": "co_dinh", "gia_tri": V0},
              {"ky_hieu": "R", "ten": "Điện trở tải", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": R_TB},
              {"ky_hieu": "U", "ten": "Hiệu điện thế trên điện trở", "don_vi": "V", "kieu": "do_duoc", "sai_so_do": 0.05},
              {"ky_hieu": "P", "ten": "Công suất điện trên điện trở", "don_vi": "W", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["U = k·(v − v0) khi v > v0; U = 0 khi v ≤ v0", "P = U²/R"],
              "gia_thiet": ["mô hình tuyến tính gần đúng cho tua-bin đồ chơi trong khoảng 1–5 m/s (tua-bin thật: công suất gió tỉ lệ khoảng v³)",
                            "vôn kế có điện trở rất lớn; dao động khi đọc ±0,05 V do gió quạt không đều"]},
  "so_lieu_mau": {"cot": ["v (m/s)", "U lần 1 (V)", "U lần 2 (V)", "U lần 3 (V)", "U trung bình (V)", "P (W)"],
                  "hang": [[v, *doc, round(tb, 2), round(p, 3)] for v, doc, tb, p in rows1],
                  "ghi_chu": "Số liệu minh hoạ tính từ U = 0,6·(v − 1), cộng dao động đọc số có tổng bằng 0; chưa phải số đo thật."},
  "ket_qua_ky_vong": "U trung bình 0,60 → 1,80 V khi gió 2 → 4 m/s; P tăng 9 lần.",
  "hien_tuong_hay_sai": ["Nghĩ gió gấp đôi thì điện gấp đôi.", "Nghĩ tua-bin gió phát đều đặn như nhau mọi lúc.",
                         "Lấy một lần đo thay vì trung bình ba lần."],
  "sai_so_thuong_gap": "Gió quạt thổi không đều, đọc vôn kế dao động tới 0,09 V ở cùng một tốc độ gió.",
  "an_toan": "Không thò tay vào cánh quạt đang quay; giữ tóc, dây xa quạt.",
  "goi_y_mo_phong": {"loai": "bang_so_lieu+do_thi", "y_tuong": "Kéo thanh tốc độ gió; cánh quay nhanh dần, vôn kế và cột công suất P = U²/R lên theo.",
                     "diem_nhan": "Gió gấp đôi mà công suất gấp 9; dưới 1 m/s cánh đứng yên."}})
tn.append({**base,
  "id": "tn-l9-taitao-02", "ten": "Pin mặt trời mini dưới đèn bàn: che bớt, tắt đèn", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["taitao.pin_quang_dien", "taitao.phu_thuoc_thoi_tiet"],
  "muc_tieu": "Thấy pin quang điện chỉ cho điện khi có ánh sáng; ánh sáng giảm thì điện giảm, tối thì không có điện.",
  "dung_cu": [{"ten": "Tấm pin mặt trời mini 6 V", "so_luong": 1},
              {"ten": "Quạt nhỏ (động cơ một chiều có cánh)", "so_luong": 1},
              {"ten": "Đèn bàn", "so_luong": 1},
              {"ten": "Tấm bìa che", "so_luong": 1}],
  "cac_buoc": {"lam": ["Nối tấm pin với quạt nhỏ.", "Chiếu đèn bàn vào tấm pin; lấy bìa che nửa tấm pin; tắt đèn."],
               "quan_sat": ["Có đèn: quạt quay đều.", "Che bớt: quạt quay chậm hẳn.", "Tắt đèn: quạt dừng."],
               "rut_ra": ["Năng lượng ánh sáng → điện năng, không qua tua-bin.", "Không có ánh sáng thì không có điện: điện mặt trời không phát ban đêm."]},
  "tham_so": [{"ky_hieu": "f", "ten": "Phần diện tích tấm pin được chiếu sáng", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 1, "buoc": 0.25},
              {"ky_hieu": "E", "ten": "Độ sáng tương đối của đèn", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 1, "buoc": 0.25},
              {"ky_hieu": "P0", "ten": "Công suất tấm pin khi chiếu sáng đủ", "don_vi": "W", "kieu": "co_dinh", "gia_tri": 1.0},
              {"ky_hieu": "P", "ten": "Công suất điện tấm pin cho quạt", "don_vi": "W", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["P = P0·f·E (gần đúng)"],
              "gia_thiet": ["coi công suất tỉ lệ diện tích được chiếu và độ sáng",
                            "thực tế che một phần có thể làm công suất giảm mạnh hơn tỉ lệ vì các ô pin mắc nối tiếp"]},
  "so_lieu_mau": {"cot": ["f", "E", "P (W)"],
                  "hang": [[1, 1, 1.0], [0.5, 1, 0.5], [1, 0, 0.0]],
                  "ghi_chu": "Số liệu minh hoạ từ mô hình P = P0·f·E, chưa phải số đo thật."},
  "ket_qua_ky_vong": "Che bớt thì quạt chậm, tắt đèn thì quạt dừng.",
  "hien_tuong_hay_sai": ["Nghĩ tấm pin tích sẵn điện nên tối vẫn chạy.", "Nghĩ pin mặt trời cần nhiệt (nóng) chứ không cần ánh sáng."],
  "an_toan": "Đèn bàn nóng, không chạm tay vào bóng đèn.",
  "goi_y_mo_phong": {"loai": "bang_so_lieu", "y_tuong": "Kéo tấm bìa che và nút tắt đèn; cánh quạt quay chậm dần theo P.",
                     "diem_nhan": "Ánh sáng bằng 0 thì điện bằng 0."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| U_TB", U_TB, "P", [round(p, 3) for p in P_TB], "| đảo N =", N_TAM, "mùa mưa", N_MUA, "| Q8", Q8)
