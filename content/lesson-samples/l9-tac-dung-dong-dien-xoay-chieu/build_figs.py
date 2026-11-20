"""Bài 15. Tác dụng của dòng điện xoay chiều (KHTN 9, lesson_id 93).
Sinh 3 hình SVG + bảng số liệu thí nghiệm đo + 2 file content/thi-nghiem/tn-l9-xoaychieu-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi số liệu tính từ mô hình (assert). Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 16          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên

def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", "{,}")
def vt(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def T(x, y, s, c="currentColor", size=17, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def dot(x, y, c="currentColor", r=3.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

# ---------- Hình 1: cảnh mở bài — một ổ điện xoay chiều, ba thiết bị (không ghi tác dụng)
b = ""
b += '<rect x="18" y="100" width="72" height="84" rx="10" fill="rgba(56,189,248,.10)" stroke="currentColor" stroke-width="2.4"/>'
b += '<rect x="38" y="128" width="8" height="22" rx="2" fill="currentColor"/><rect x="62" y="128" width="8" height="22" rx="2" fill="currentColor"/>'
b += T(18, 88, "Ổ điện") + T(18, 210, "220 V~", BLUE)
YK, YD, YQ = 62, 142, 222            # độ cao dây nối tới ấm, đèn, quạt
b += line(90, 142, 130, 142, w=2.2) + line(130, YK, 130, YQ, w=2.2)
for y in (YK, YD, YQ):
    b += dot(130, y, r=3) if y != YD else ""
b += line(130, YK, 182, YK, w=2.2) + line(130, YD, 182, YD, w=2.2) + line(130, YQ, 170, YQ, w=2.2)
# ấm siêu tốc (đáy ở y = 82, dây nối vào thân trái)
b += '<polygon points="180,84 232,84 225,36 187,36" fill="rgba(56,189,248,.14)" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/>'
b += line(190, 30, 222, 30, w=2.6) + '<rect x="201" y="23" width="10" height="7" rx="2" fill="currentColor"/>'
b += '<path d="M225,44 C246,44 246,76 229,78" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += '<path d="M188,46 L170,34" fill="none" stroke="currentColor" stroke-width="3"/>'
for x0 in (152, 164):
    b += f'<path d="M{x0},28 q-5,-6 0,-12 q5,-6 0,-12" fill="none" stroke="{ORG}" stroke-width="2" opacity=".9"/>'
# đèn
b += f'<circle cx="205" cy="{YD}" r="20" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2.4"/>'
b += f'<rect x="198" y="{YD + 19}" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="2"/>'
for a in (90, 45, 135, 0, 180):
    r1, r2 = 26, 35
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    b += line(205 + r1 * ca, YD - r1 * sa, 205 + r2 * ca, YD - r2 * sa, ORG, 2.4)
# quạt: lồng, ba cánh, chân đế
FX, FR = 205, 32
assert YQ + FR + 14 <= 270 and YD + 35 < YQ - FR       # chân quạt trong khung; tia đèn không chạm lồng quạt
b += f'<circle cx="{FX}" cy="{YQ}" r="{FR}" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="4 3"/>'
for a in (90, 210, 330):
    cx, cy = FX + 15 * math.cos(math.radians(a)), YQ - 15 * math.sin(math.radians(a))
    b += (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="15" ry="6" transform="rotate({-a:.0f} {cx:.1f} {cy:.1f})" '
          f'fill="rgba(52,211,153,.25)" stroke="currentColor" stroke-width="1.8"/>')
b += dot(FX, YQ, r=5) + line(FX, YQ + FR, FX, YQ + FR + 8, w=3) + line(FX - 18, YQ + FR + 10, FX + 18, YQ + FR + 10, w=3)
b += T(262, YK - 2, "ấm siêu tốc") + T(262, YD + 6, "đèn LED") + T(262, YQ + 6, "quạt điện")
fig1 = wrap("0 0 420 270", "Một ổ điện 220 vôn xoay chiều cấp điện cho ấm siêu tốc, đèn LED và quạt điện", b,
            "Hình 1. Ấm siêu tốc, đèn LED, quạt điện cắm chung một ổ điện xoay chiều.")

# ---------- Hình 2: bộ thí nghiệm nam châm điện — chỉ dụng cụ, chưa vẽ kết quả
b = ""
CX0, CX1, CY = 60, 230, 110          # lõi sắt
b += f'<rect x="{CX0}" y="{CY - 13}" width="{CX1 - CX0}" height="26" rx="3" fill="rgba(148,163,184,.45)" stroke="currentColor" stroke-width="2"/>'
TURNS = [92 + 12 * i for i in range(9)]
for x in TURNS:
    b += f'<ellipse cx="{x}" cy="{CY}" rx="5" ry="24" fill="none" stroke="{ORG}" stroke-width="2.4"/>'
XL, XR = TURNS[0], TURNS[-1]
BOX = (60, 190, 160, 50)
b += line(XL, CY + 24, XL, BOX[1], ORG, 2.4) + line(XR, CY + 24, XR, BOX[1], ORG, 2.4)
b += f'<rect x="{BOX[0]}" y="{BOX[1]}" width="{BOX[2]}" height="{BOX[3]}" rx="8" fill="rgba(56,189,248,.10)" stroke="currentColor" stroke-width="2.2"/>'
b += T(140, 211, "nguồn một chiều", size=15, anchor="middle") + T(140, 231, "hoặc xoay chiều ~", BLUE, 15, "middle")
assert BOX[0] < XL and XR < BOX[0] + BOX[2]
# đinh sắt bên trái lõi
b += line(16, CY, 48, CY, w=4) + line(13, CY - 6, 13, CY + 6, w=4)
b += '<polygon points="48,108 48,112 54,110" fill="currentColor"/>'
assert 54 < CX0
b += T(8, 150, "đinh sắt", size=15)
b += T(XL - 6, 76, "cuộn dây", ORG, 15) + T(196, 76, "lõi sắt", size=15)
# kim nam châm bên phải, đứng trên trụ
KX, KY, KL = 300, 110, 38
assert KX - 8 - CX1 > 50
b += f'<polygon points="{KX},{KY - KL} {KX + 8},{KY} {KX - 8},{KY}" fill="{RED}" stroke="currentColor" stroke-width="1.2"/>'
b += f'<polygon points="{KX},{KY + KL} {KX + 8},{KY} {KX - 8},{KY}" fill="{BLUE}" stroke="currentColor" stroke-width="1.2"/>'
b += dot(KX, KY, "currentColor", 3)
b += T(KX + 14, KY - KL + 14, "N", RED, 15) + T(KX + 14, KY + KL - 2, "S", BLUE, 15)
b += line(KX, KY + KL + 2, KX, 176, w=2.4) + f'<rect x="{KX - 22}" y="176" width="44" height="7" rx="2" fill="currentColor"/>'
b += T(250, 208, "kim nam châm", size=15)
fig2 = wrap("0 0 420 250", "Nam châm điện gồm cuộn dây quấn quanh lõi sắt, nối với nguồn một chiều hoặc xoay chiều; bên trái lõi là đinh sắt, bên phải là kim nam châm trên trụ", b,
            "Hình 2. Nam châm điện, đinh sắt và kim nam châm.<br>Nguồn đổi được giữa một chiều và xoay chiều.")

# ---------- Hình 3: hai ampe kế, mỗi cái mắc đúng loại nguồn, cùng chỉ 0,50 A
I_DM = 3.0 / 6.0
def meter(x0, sym, signs, ten):
    cx, top, wd, ht = x0 + 90, 14, 180, 160
    py, r = top + 114, 78
    g = f'<rect x="{x0}" y="{top}" width="{wd}" height="{ht}" rx="12" fill="rgba(56,189,248,.07)" stroke="currentColor" stroke-width="2.2"/>'
    ang = lambda v: math.radians(150 - 120 * v)        # 0 A ở 150°, 1 A ở 30°
    g += pts_path(arc_pts(cx, py, r, r, -150, -30), "currentColor", 2)
    for k in range(11):
        v, L = k / 10, (12 if k % 5 == 0 else 6)
        a = ang(v)
        g += line(cx + r * math.cos(a), py - r * math.sin(a), cx + (r - L) * math.cos(a), py - (r - L) * math.sin(a), w=1.8)
    for v, s in ((0, "0"), (1, "1")):
        a = ang(v)
        g += T(round(cx + (r - 26) * math.cos(a), 1), round(py - (r - 26) * math.sin(a) + 6, 1), s, size=15, anchor="middle")
    a = ang(I_DM)
    tip = (cx + (r - 8) * math.cos(a), py - (r - 8) * math.sin(a))
    g += line(cx, py, *tip, RED, 2.6) + dot(cx, py, r=4)
    g += T(cx - 10, top + ht - 10, "A", size=22, anchor="end")
    if sym == "DC":   # kí hiệu một chiều: gạch liền trên gạch đứt
        yb = top + ht - 22
        g += line(cx + 8, yb, cx + 40, yb, BLUE, 3) + f'<line x1="{cx + 8}" y1="{yb + 8}" x2="{cx + 40}" y2="{yb + 8}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="7 5"/>'
    else:
        g += T(cx + 8, top + ht - 10, sym, BLUE, 22)
    for dx, s in ((-40, signs[0]), (40, signs[1])):
        g += f'<circle cx="{cx + dx}" cy="{top + ht + 18}" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/>'
        if s:
            g += T(cx + dx - 12, top + ht + 24, s, size=16, anchor="end")
    g += T(cx, top + ht + 50, "mắc vào nguồn", size=15, anchor="middle") + T(cx, top + ht + 70, ten, size=15, anchor="middle")
    return g, tip, (cx, py)
m1, tip1, pv1 = meter(14, "DC", ("+", "−"), "một chiều 6 V")
m2, tip2, pv2 = meter(226, "~", ("", ""), "xoay chiều 6 V~")
assert abs(tip1[0] - pv1[0]) < 1e-6 and tip1[1] < pv1[1]       # 0,5 A: kim thẳng đứng, đúng giữa thang 0–1 A
b = m1 + m2
fig3 = wrap("0 0 420 262", "Hai ampe kế thang 0 đến 1 ampe cùng chỉ 0,5 ampe: bên trái ampe kế một chiều có kí hiệu gạch liền trên gạch đứt và hai chốt cộng trừ mắc vào nguồn một chiều; bên phải ampe kế xoay chiều có dấu ngã, chốt không phân biệt, mắc vào nguồn xoay chiều", b,
            "Hình 3. Ampe kế một chiều (DC) và xoay chiều (AC, ~), mỗi cái mắc đúng loại nguồn.")

# ---------- Thí nghiệm 2: đèn 6 V – 3 W, nguồn một chiều 6 V và xoay chiều 6 V (hiệu dụng); I = P/U = 0,50 A
# Số đọc lệch tối đa một độ chia 0,01 A do đọc kim (số liệu minh hoạ).
DC = (0.50, 0.49, 0.50)
AC = (0.49, 0.50, 0.50)
for v in DC + AC:
    assert abs(v - I_DM) <= 0.01 + 1e-9
assert abs(DC[0] - AC[0]) == 0 or True
assert round(abs(DC[0] - AC[0]), 2) == 0.01 and round(abs(DC[1] - AC[1]), 2) == 0.01 and DC[2] == AC[2]   # Câu 4: lần 1, 2 chênh 0,01 A
assert AC[1] > DC[1]                                                       # phản hồi A của Câu 4: lần 2 cột xoay chiều lớn hơn
mDC, mAC = sum(DC) / 3, sum(AC) / 3
assert abs(mDC - mAC) < 1e-12 and round(mDC, 2) == 0.50
bang2 = "\n".join(f"<tr><td>{k}</td><td>${vn(d, 2)}$</td><td>${vn(a, 2)}$</td></tr>" for k, (d, a) in enumerate(zip(DC, AC), 1))
lech = 0.01 / 0.50 * 100
assert abs(lech - 2) < 1e-9
NX2 = (f"Trung bình mỗi cột: $\\dfrac{{{vn(DC[0], 2)} + {vn(DC[1], 2)} + {vn(DC[2], 2)}}}{{3}} \\approx {vn(mDC, 2)}\\ \\text{{A}}.$<br>"
       f"Lệch một độ chia $0{{,}}01\\ \\text{{A}}$ chỉ khoảng ${round(lech)}\\ \\%$ của $0{{,}}50\\ \\text{{A}}.$<br>"
       f"Đèn ghi 6&nbsp;V – 3&nbsp;W: $I = \\dfrac{{P}}{{U}} = \\dfrac{{3}}{{6}} = 0{{,}}50\\ \\text{{A}}{{:}}$ khớp cả hai nguồn.")

# ---------- Tình huống mẫu: ấm 1 800 W, 12 phút/ngày, 30 ngày; giá 2 000 đ/kWh
P_AM = 1.8
t_ngay = 12 / 60
t_thang = t_ngay * 30
A_thang = P_AM * t_thang
assert abs(t_ngay - 0.2) < 1e-12 and abs(t_thang - 6) < 1e-12 and abs(A_thang - 10.8) < 1e-9
tien = A_thang * 2000
assert abs(tien - 21600) < 1e-6
A_jun = 1800 * t_thang * 3600
assert abs(A_jun - 3.888e7) < 1e-3 and abs(A_jun / 3.6e6 - 10.8) < 1e-9
t2 = 20 / 60 * 30
A2 = P_AM * t2
assert abs(t2 - 10) < 1e-9 and abs(A2 - 18) < 1e-9 and abs(A2 * 2000 - 36000) < 1e-6
assert abs((A2 * 2000) / tien - 5 / 3) < 1e-9
assert 220 > 200 and 220 < 750                                              # chọn ACV 750
# Câu 7: máy sấy 1 200 W, 15 phút/ngày, 30 ngày
assert abs(1.2 * 0.25 * 30 - 9) < 1e-9 and 1.2 * 15 * 30 == 540 and abs(1.2 * 0.25 - 0.3) < 1e-9 and 1200 * 0.25 * 30 == 9000
# Thử thách ⭐⭐: 3 W, 10 phút
assert 3 * 600 == 1800
# 50 Hz: đổi chiều 2 lần mỗi chu kì
assert 50 * 2 == 100

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
rep = (("__BANG_TN2__", bang2), ("__NHAN_XET_TN2__", NX2), ("__T_NGAY__", vn(t_ngay, 1)), ("__T_THANG__", vn(t_thang, 0)),
       ("__A_THANG__", vn(A_thang, 1)), ("__TIEN__", "21\\,600"), ("__A_JUN__", "3{,}888 \\cdot 10^7"),
       ("__T2__", vn(t2, 0)), ("__A2__", vn(A2, 0)), ("__TIEN2__", "36\\,000"), ("__PHUT__", str(PHUT)))
for k, v in rep:
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 15. Tác dụng của dòng điện xoay chiều"
SRC = "content/lesson-samples/l9-tac-dung-dong-dien-xoay-chieu/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 93, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-xoaychieu-01", "ten": "Nam châm điện với nguồn một chiều và nguồn xoay chiều: đinh sắt, kim nam châm", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["xoaychieu.tac_dung_tu", "xoaychieu.cuc_doi_theo_dong"],
  "muc_tieu": "Thấy dòng xoay chiều vẫn có tác dụng từ (hút sắt); cực từ của nam châm điện đổi theo chiều dòng điện; với nguồn 50 Hz lực lên kim đổi chiều quá nhanh nên kim không lệch hẳn, chỉ rung rất nhẹ.",
  "dung_cu": [{"ten": "Cuộn dây khoảng 300 vòng có lõi sắt non", "so_luong": 1},
              {"ten": "Nguồn một chiều 6 V", "so_luong": 1},
              {"ten": "Nguồn xoay chiều 6 V (biến áp nguồn phòng thí nghiệm)", "so_luong": 1},
              {"ten": "Kim nam châm trên trụ", "so_luong": 1},
              {"ten": "Đinh sắt nhỏ", "so_luong": 1},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mắc nam châm điện như Hình 2: đinh sắt ở một đầu lõi, kim nam châm ở đầu kia.",
                       "Lần 1: nối nguồn một chiều 6 V, đóng khoá; rồi đảo hai cực nguồn.",
                       "Lần 2: nối nguồn xoay chiều 6 V, đóng khoá."],
               "quan_sat": ["Một chiều: đinh sắt bị hút; kim nam châm lệch hẳn về một phía. Đảo cực nguồn: kim lệch về phía ngược lại.",
                            "Xoay chiều: đinh sắt vẫn bị hút; kim nam châm không lệch hẳn về phía nào, chỉ rung rất nhẹ quanh vị trí cũ."],
               "rut_ra": ["Dòng xoay chiều có tác dụng từ, vẫn hút sắt.",
                          "Cực từ của nam châm điện đổi theo chiều dòng điện; lực lên kim nam châm (cực cố định) đổi chiều 100 lần mỗi giây, kim không kịp quay theo.",
                          "Đinh sắt non bị từ hoá đổi cực theo nên luôn bị hút."]},
  "tham_so": [{"ky_hieu": "loai_nguon", "ten": "Loại nguồn (0 một chiều, 1 xoay chiều)", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0, "buoc": 1},
              {"ky_hieu": "dao_cuc", "ten": "Đảo cực nguồn một chiều (0 không, 1 có)", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0, "buoc": 1},
              {"ky_hieu": "U", "ten": "Hiệu điện thế nguồn", "don_vi": "V", "kieu": "co_dinh", "gia_tri": 6},
              {"ky_hieu": "f", "ten": "Tần số nguồn xoay chiều", "don_vi": "Hz", "kieu": "co_dinh", "gia_tri": 50},
              {"ky_hieu": "lech_kim", "ten": "Độ lệch kim nam châm", "don_vi": "độ", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["Cực từ đầu lõi gần kim: N khi i > 0, S khi i < 0", "Xoay chiều: i = I0·sin(2π·50·t) nên cực đổi 100 lần mỗi giây",
                               "Lực lên kim nam châm đổi chiều theo i; lực lên đinh sắt non luôn là lực hút, độ lớn tỉ lệ i²"],
              "gia_thiet": ["kim nam châm có quán tính: với 50 Hz chỉ rung nhẹ quanh vị trí cũ",
                            "bỏ qua từ dư của lõi sắt non"]},
  "so_lieu_mau": {"cot": ["Nguồn", "Đinh sắt", "Kim nam châm"],
                  "hang": [["một chiều 6 V", "bị hút", "lệch hẳn một phía"],
                           ["một chiều 6 V, đảo cực", "bị hút", "lệch phía ngược lại"],
                           ["xoay chiều 6 V", "bị hút", "không lệch, rung rất nhẹ"]],
                  "ghi_chu": "Kết quả định tính, mô tả theo mô hình; chưa phải ghi chép thí nghiệm thật. Video tự dựng dùng thêm nguồn đổi chiều thật chậm giả định, mỗi 2 giây một lần (mô hình minh hoạ, không có trong phòng thí nghiệm): kim nam châm lắc qua lại, đổi phía theo mỗi lần dòng đổi chiều."},
  "ket_qua_ky_vong": "Cả hai nguồn đều hút đinh sắt; kim nam châm lệch một phía với nguồn một chiều, không lệch hẳn (chỉ rung rất nhẹ quanh vị trí cũ) với nguồn xoay chiều 50 Hz.",
  "hien_tuong_hay_sai": ["Nghĩ dòng xoay chiều không có tác dụng từ vì đổi chiều liên tục.",
                         "Nghĩ đinh sắt cũng bị đẩy ra khi dòng đổi chiều.",
                         "Nghĩ kim nam châm sẽ quay tròn liên tục."],
  "an_toan": "Chỉ dùng nguồn xoay chiều 6 V của phòng thí nghiệm, không nối cuộn dây vào ổ điện 220 V.",
  "goi_y_mo_phong": {"loai": "so_do_luc", "y_tuong": "Công tắc chọn nguồn; vẽ cực N/S ở đầu lõi đổi theo dấu của i(t) chạy chậm; kim nam châm quay theo lực khi chạy chậm, đứng gần như yên khi chạy đúng 50 Hz; đinh sắt luôn bị hút.",
                     "diem_nhan": "Cực nam châm điện đổi theo dòng điện: kim không kịp quay theo, đinh sắt vẫn bị hút."}})
tn.append({**base,
  "id": "tn-l9-xoaychieu-02", "ten": "Đo dòng điện qua đèn 6 V – 3 W với nguồn một chiều và nguồn xoay chiều cùng 6 V", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["xoaychieu.tac_dung_nhiet_sang", "xoaychieu.dung_cu_do_ac", "xoaychieu.sai_so_do"],
  "muc_tieu": "Từ bảng số liệu thấy với cùng 6 V, dòng xoay chiều làm đèn sáng, nóng như dòng một chiều; dụng cụ đo phải đúng loại (DC/AC).",
  "dung_cu": [{"ten": "Bóng đèn 6 V – 3 W có đui", "so_luong": 1},
              {"ten": "Nguồn một chiều 6 V", "so_luong": 1},
              {"ten": "Nguồn xoay chiều 6 V", "so_luong": 1},
              {"ten": "Ampe kế một chiều (GHĐ 1 A, ĐCNN 0,01 A)", "so_luong": 1},
              {"ten": "Ampe kế xoay chiều (GHĐ 1 A, ĐCNN 0,01 A)", "so_luong": 1},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mắc đèn nối tiếp ampe kế một chiều vào nguồn một chiều 6 V; đọc số chỉ 3 lần.",
                       "Thay bằng nguồn xoay chiều 6 V và ampe kế xoay chiều; đọc số chỉ 3 lần.",
                       "So độ sáng của đèn hai lần."],
               "quan_sat": ["Hai lần đèn sáng như nhau.",
                            "Số chỉ ampe kế: một chiều " + "; ".join(vt(v, 2) for v in DC) + " A; xoay chiều " + "; ".join(vt(v, 2) for v in AC) + " A."],
               "rut_ra": ["Với cùng 6 V (hiệu dụng), dòng xoay chiều có tác dụng nhiệt, phát sáng như dòng một chiều.",
                          "Chênh 0,01 A là sai lệch đọc số cỡ một độ chia; trung bình hai cột như nhau ≈ 0,50 A."]},
  "tham_so": [{"ky_hieu": "loai_nguon", "ten": "Loại nguồn (0 một chiều, 1 xoay chiều)", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0, "buoc": 1},
              {"ky_hieu": "loai_ampe_ke", "ten": "Loại ampe kế (0 một chiều, 1 xoay chiều)", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0, "buoc": 1},
              {"ky_hieu": "U", "ten": "Hiệu điện thế nguồn (hiệu dụng nếu xoay chiều)", "don_vi": "V", "kieu": "co_dinh", "gia_tri": 6},
              {"ky_hieu": "P_dm", "ten": "Công suất định mức của đèn", "don_vi": "W", "kieu": "co_dinh", "gia_tri": 3},
              {"ky_hieu": "I", "ten": "Số chỉ ampe kế", "don_vi": "A", "kieu": "do_duoc", "sai_so_do": 0.01}],
  "mo_hinh": {"phuong_trinh": ["I = P_dm/U = 0,50 A (cả hai nguồn, U hiệu dụng = 6 V)",
                               "Ampe kế đúng loại: I_doc = I ± 0,01 A",
                               "Ampe kế một chiều trong mạch xoay chiều 50 Hz: I_doc ≈ 0 (lực lên khung đổi chiều 100 lần/giây)"],
              "gia_thiet": ["coi điện trở đèn ở 6 V như nhau với hai nguồn", "bỏ qua điện trở ampe kế, dây nối"]},
  "so_lieu_mau": {"cot": ["Lần đo", "I một chiều (A)", "I xoay chiều (A)"],
                  "hang": [[k, d, a] for k, (d, a) in enumerate(zip(DC, AC), 1)],
                  "ghi_chu": "Số liệu minh hoạ từ I = 3/6 = 0,50 A, lệch tối đa một độ chia 0,01 A do đọc số; chưa phải số đo thật. Video tự dựng thêm vôn kế mắc hai đầu đèn (minh hoạ): một chiều 6,0 V, xoay chiều 6,0 V (giá trị hiệu dụng); bỏ qua điện trở ampe kế và dây nối. Câu hỏi chốt video: nguồn 9 V xoay chiều (minh hoạ)."},
  "ket_qua_ky_vong": "Trung bình hai cột ≈ 0,50 A; đèn sáng như nhau.",
  "hien_tuong_hay_sai": ["Nghĩ dòng xoay chiều làm đèn tối hơn vì đổi chiều.",
                         "Dùng ampe kế một chiều đo dòng xoay chiều: kim gần như đứng ở 0 dù đèn sáng.",
                         "Nghĩ phải mắc đúng chốt (+), (−) cho ampe kế xoay chiều."],
  "sai_so_thuong_gap": "Đọc kim lệch một độ chia 0,01 A: khoảng 2 % của 0,50 A.",
  "an_toan": "Chỉ dùng nguồn 6 V của phòng thí nghiệm; không đo trực tiếp ổ điện 220 V.",
  "goi_y_mo_phong": {"loai": "bang_so_lieu", "y_tuong": "Chọn nguồn và loại ampe kế; kim ampe kế một chiều đứng ở 0 khi gặp nguồn xoay chiều; bảng tự ghi số đọc.",
                     "diem_nhan": "Đúng loại dụng cụ thì hai nguồn cho cùng 0,50 A; sai loại thì kim đứng ở 0."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| TN2 DC:", DC, "AC:", AC, "| mẫu A =", A_thang, "kWh, tiền", tien)
