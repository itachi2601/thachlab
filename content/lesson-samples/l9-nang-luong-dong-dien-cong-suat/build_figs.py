"""Bài 13. Năng lượng của dòng điện và công suất điện (KHTN 9, lesson_id 91).
Sinh 4 hình SVG + bảng số liệu thí nghiệm + 3 file content/thi-nghiem/tn-l9-congsuat-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi số liệu tính từ mô hình (assert). Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 14          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên

def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", "{,}")
def vt(x, nd=1):
    """Số thập phân cho <text> SVG (dấu phẩy thường)."""
    return f"{x:.{nd}f}".replace(".", ",")
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def poly(pts, c="currentColor", w=2.4):
    return pts_path(pts, c, w)
def T(x, y, s, c="currentColor", size=18, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def it_(s):
    """Ký hiệu đại lượng trong SVG: chữ nghiêng có chân."""
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'
def subt(x, y, base, idx, rest="", c="currentColor", size=18, anchor="start"):
    """Nhãn có chỉ số dưới bằng <tspan dy> (không dùng chữ số Unicode ₁₂)."""
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">{base}'
            f'<tspan dy="5" font-size="{size - 4}">{idx}</tspan><tspan dy="-5">{rest}</tspan></text>')
def dot(x, y, c="currentColor", r=3.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
def cur(x, y, dx, dy):
    """Đầu V chỉ chiều dòng điện quy ước trên dây."""
    return chevron(x, y, dx, dy, RED, 2.6, 13)
def lamp(cx, cy, r=15):
    """Kí hiệu bóng đèn: vòng tròn có dấu ×, nền trắng che dây."""
    k = r * 0.7071
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(251,146,60,.12)" stroke="currentColor" stroke-width="2.4"/>'
            + line(cx - k, cy - k, cx + k, cy + k, "currentColor", 2) + line(cx - k, cy + k, cx + k, cy - k, "currentColor", 2))

# ---------- Hình 1: cảnh mở bài (chỉ cảnh, không ghi số oát)
b = ""
# ổ cắm trên tường + củ sạc + dây + điện thoại
b += '<rect x="22" y="44" width="56" height="74" rx="8" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += '<rect x="38" y="66" width="6" height="14" rx="2" fill="currentColor"/><rect x="56" y="66" width="6" height="14" rx="2" fill="currentColor"/>'
b += '<rect x="34" y="62" width="34" height="38" rx="6" fill="rgba(56,189,248,.18)" stroke="currentColor" stroke-width="2.2"/>'
b += '<path d="M51,100 C51,150 100,120 112,150" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += '<rect x="104" y="150" width="44" height="76" rx="8" fill="rgba(56,189,248,.12)" stroke="currentColor" stroke-width="2.4"/>'
b += '<rect x="111" y="160" width="30" height="50" rx="2" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".6"/>'
b += '<path d="M126,176 l-6,11 h7 l-5,11" fill="none" stroke="#34d399" stroke-width="2.4"/>'
b += T(12, 24, "Củ sạc điện thoại", "currentColor", 17)
b += T(12, 254, "cắm 24 giờ mỗi ngày", BLUE, 17)
b += line(210, 14, 210, 262, "currentColor", 1.2, "5 5", .5)
# điều hoà + gió lạnh + mặt trăng
b += '<rect x="236" y="56" width="164" height="54" rx="10" fill="rgba(56,189,248,.12)" stroke="currentColor" stroke-width="2.4"/>'
b += line(250, 98, 386, 98, "currentColor", 2) + line(250, 104, 386, 104, "currentColor", 1.4, "", .6)
for k in range(4):
    x0 = 262 + 34 * k
    b += f'<path d="M{x0},122 q8,12 0,24 q-8,12 0,24" fill="none" stroke="{BLUE}" stroke-width="2" opacity=".8"/>'
b += '<path d="M392,36 a20,20 0 1 1 -16,-30 a15,15 0 1 0 16,30 z" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="1.8"/>'
b += T(226, 24, "Điều hoà", "currentColor", 17)
b += T(226, 254, "bật 8 giờ mỗi đêm", BLUE, 17)
fig1 = wrap("0 0 420 270", "Bên trái củ sạc điện thoại cắm ổ điện cả ngày; bên phải máy điều hoà chỉ bật ban đêm", b,
            "Hình 1. Củ sạc cắm cả ngày, điều hoà chỉ bật ban đêm.<br>Thiết bị nào làm tốn điện hơn?")

# ---------- Hình 2: sơ đồ đo U, I của bóng đèn (thí nghiệm 1)
b = ""
X0, X1, Y0, Y1 = 50, 300, 60, 240
AX, VY, RA = 175, 150, 22
PX, NX = 168, 182
J1, J2 = 100, 200
KT, KB = 125, 175
LY = 150                     # tâm đèn trên dây phải
W = 2.4
b += poly([(PX, Y1), (X0, Y1), (X0, KB)], "currentColor", W)
b += poly([(X0, KT), (X0, Y0), (AX - RA, Y0)], "currentColor", W)
b += poly([(AX + RA, Y0), (X1, Y0), (X1, LY - 15)], "currentColor", W)
b += poly([(X1, LY + 15), (X1, Y1), (NX, Y1)], "currentColor", W)
b += dot(X0, KT, "currentColor", 4) + dot(X0, KB, "currentColor", 4) + line(X0, KB, X0, KT, "currentColor", 3)
b += T(X0 + 14, 156, "K", "currentColor", 18)
b += line(PX, Y1 - 18, PX, Y1 + 18, "currentColor", 2.4) + line(NX, Y1 - 9, NX, Y1 + 9, "currentColor", 5)
b += T(PX - 6, Y1 - 24, "+", "currentColor", 20, "end") + T(NX + 6, Y1 - 24, "−", "currentColor", 20)
b += T(175, Y1 + 40, "nguồn chỉnh được", "currentColor", 16, "middle", "600")
b += f'<circle cx="{AX}" cy="{Y0}" r="{RA}" fill="none" stroke="currentColor" stroke-width="2.4"/>' + T(AX, Y0 + 8, "A", "currentColor", 22, "middle")
b += T(AX - RA - 4, Y0 - 12, "+", "currentColor", 20, "end") + T(AX + RA + 4, Y0 - 12, "−", "currentColor", 20)
b += lamp(X1, LY)
b += T(X1 - 24, LY + 7, "Đ", "currentColor", 21, "end")
b += dot(X1, J1) + dot(X1, J2)
b += poly([(X1, J1), (390, J1), (390, VY - RA)], "currentColor", W)
b += poly([(390, VY + RA), (390, J2), (X1, J2)], "currentColor", W)
b += f'<circle cx="390" cy="{VY}" r="{RA}" fill="none" stroke="currentColor" stroke-width="2.4"/>' + T(390, VY + 8, "V", "currentColor", 22, "middle")
b += T(400, VY - RA - 2, "+", "currentColor", 20) + T(400, VY + RA + 18, "−", "currentColor", 20)
b += cur(110, Y1, -1, 0) + cur(X0, 100, 0, -1) + cur(245, Y0, 1, 0) + cur(X1, 225, 0, 1) + cur(240, Y1, -1, 0)
b += T(245, Y0 - 12, it_("I"), RED, 22, "middle")
b += T(20, 312, "Dòng điện: từ (+) qua mạch ngoài về (−)", RED, 16)
assert PX < NX and 110 < PX and 240 > NX
fig2 = wrap("0 0 440 322", "Sơ đồ mạch: nguồn chỉnh được, khoá K, ampe kế nối tiếp, bóng đèn Đ, vôn kế song song với đèn; mũi tên đỏ chỉ chiều dòng điện", b,
            "Hình 2. Ampe kế mắc nối tiếp, vôn kế mắc song song với đèn Đ.<br>Chốt (+) của hai dụng cụ nối về phía cực (+) của nguồn.")

# ---------- Thí nghiệm 1: đèn 6 V – 3 W, dây tóc: I = I_dm·(U/U_dm)^0,6 (điện trở dây tóc tăng khi nóng), đọc tới 0,01 A
U_DM, P_DM, MU = 6.0, 3.0, 0.6
I_DM = P_DM / U_DM
U1 = (1.5, 3.0, 4.5, 6.0)
rows1 = []
for u in U1:
    it = I_DM * (u / U_DM) ** MU
    ido = round(it, 2)
    assert abs(ido - it) <= 0.005 + 1e-9
    rows1.append((u, it, ido, u * ido))
assert [r[2] for r in rows1] == [0.22, 0.33, 0.42, 0.50], [r[2] for r in rows1]
P1 = [round(r[3], 2) for r in rows1]
assert P1 == [0.33, 0.99, 1.89, 3.00], P1
ratio = rows1[3][3] / rows1[0][3]
assert 8.8 < ratio < 9.3, ratio                     # U ×4 → U·I ×9 (không phải ×4, không phải ×16)
p_lech1, p_lech4 = 0.005 / rows1[0][2] * 100, 0.005 / rows1[3][2] * 100
assert 2 < p_lech1 < 2.5 and abs(p_lech4 - 1) < 1e-9
bang1 = "\n".join(f"<tr><td>${vn(u, 1)}$</td><td>${vn(ido, 2)}$</td><td>${vn(p, 2)}$</td></tr>" for u, _, ido, p in rows1)
U_TN1 = ";\\ ".join(vn(u, 1) for u in U1) + "\\ \\text{V}"
NX1 = (f"$U$ tăng $4$ lần $({vn(1.5, 1)} \\to {vn(6.0, 1)}\\ \\text{{V}})$ thì $U \\cdot I$ tăng khoảng ${round(ratio)}$ lần.<br>"
       f"$I$ không tăng tỉ lệ với $U$ vì dây tóc nóng lên, điện trở tăng.<br>"
       f"Lệch nửa vạch $0{{,}}005\\ \\text{{A}}$ so với ${vn(rows1[0][2], 2)}\\ \\text{{A}}$ là khoảng ${round(p_lech1)}\\ \\%,$ "
       f"so với ${vn(rows1[3][2], 2)}\\ \\text{{A}}$ chỉ ${round(p_lech4)}\\ \\%{{:}}$ lần 1 dễ sai nhất.")

# ---------- Ví dụ 2: công tơ khi đun ấm 1 000 W trong 30 phút
P_AM, T_AM = 1000.0, 0.5
CT0 = 1234.6
A_AM = P_AM / 1000 * T_AM
CT1 = round(CT0 + A_AM, 1)
assert abs(A_AM - 0.5) < 1e-12 and abs(CT1 - 1235.1) < 1e-9
CT_TRUOC, CT_SAU = "1\\,234{,}6", "1\\,235{,}1"

# ---------- Hình 3: hai mặt công tơ trước / sau
def meter(x, y, title, digits):
    g = f'<rect x="{x}" y="{y}" width="186" height="132" rx="12" fill="rgba(56,189,248,.08)" stroke="currentColor" stroke-width="2.2"/>'
    g += T(x + 93, y + 28, title, "currentColor", 17, "middle")
    cw, ch, gx0, gy0 = 24, 34, x + 13, y + 46
    for k, dch in enumerate(digits):
        last = k == len(digits) - 1
        g += (f'<rect x="{gx0 + k * (cw + 3)}" y="{gy0}" width="{cw}" height="{ch}" rx="3" '
              f'fill="{"rgba(248,113,113,.18)" if last else "none"}" stroke="{RED if last else "currentColor"}" stroke-width="1.8"/>')
        g += T(gx0 + k * (cw + 3) + cw / 2, gy0 + 25, dch, RED if last else "currentColor", 21, "middle")
    g += T(x + 93, y + 110, "kWh", "currentColor", 17, "middle")
    return g
d0 = f"{int(CT0 * 10):06d}"
d1 = f"{int(round(CT1 * 10)):06d}"
assert d0 == "012346" and d1 == "012351"
b = meter(14, 14, "Trước khi đun", d0) + meter(220, 14, "Sau 30 phút", d1)
b += T(14, 182, "Ô đỏ là phần mười của một số điện.", "currentColor", 16, "start", "600")
fig3 = wrap("0 0 420 194", "Hai mặt công tơ: trước khi đun ấm chỉ 1234,6 kilôoát giờ, sau 30 phút chỉ 1235,1 kilôoát giờ", b,
            "Hình 3. Công tơ trước và sau khi đun ấm 30 phút.<br>Mỗi số điện là 1 kWh.")

# ---------- Hình 4: hai đèn 220 V – 40 W và 220 V – 100 W, nối tiếp (a) và song song (b) — không vẽ độ sáng
b = ""
# (a) nối tiếp — nguồn 220 V là hai chốt trên dây dưới
L, R_, TOP, BOT = 30, 190, 70, 200
b += poly([(92, BOT), (L, BOT), (L, TOP), (65, TOP)]) + poly([(95, TOP), (135, TOP)]) + poly([(165, TOP), (R_, TOP), (R_, BOT), (128, BOT)])
b += lamp(80, TOP) + lamp(150, TOP)
b += subt(80, TOP - 24, "Đ", "1", "", "currentColor", 18, "middle") + subt(150, TOP - 24, "Đ", "2", "", "currentColor", 18, "middle")
b += '<circle cx="97" cy="200" r="5" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="123" cy="200" r="5" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += T(110, 228, "220 V", "currentColor", 17, "middle")
b += T(14, 262, "(a) nối tiếp", "currentColor", 17)
# (b) song song — hai nhánh nằm ngang, nhãn đặt trên mỗi bóng
JL, JR, YB1, YB2, XC = 262, 402, TOP, 150, 332
b += poly([(JL, YB2), (JL, YB1), (XC - 15, YB1)]) + poly([(XC + 15, YB1), (JR, YB1), (JR, YB2)])
b += poly([(JL, YB2), (XC - 15, YB2)]) + poly([(XC + 15, YB2), (JR, YB2)])
b += poly([(JL, YB2), (JL, BOT), (309, BOT)]) + poly([(355, BOT), (JR, BOT), (JR, YB2)])
b += dot(JL, YB2) + dot(JR, YB2)
b += lamp(XC, YB1) + lamp(XC, YB2)
b += subt(XC, YB1 - 24, "Đ", "1", "", "currentColor", 18, "middle") + subt(XC, YB2 - 24, "Đ", "2", "", "currentColor", 18, "middle")
b += '<circle cx="314" cy="200" r="5" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="350" cy="200" r="5" fill="none" stroke="currentColor" stroke-width="2.2"/>'
b += T(332, 228, "220 V", "currentColor", 17, "middle")
b += T(234, 262, "(b) song song", "currentColor", 17)
b += line(212, 14, 212, 270, "currentColor", 1.2, "5 5", .5)
b += subt(14, 298, "Đ", "1", ": 220 V – 40 W", BLUE, 17) + subt(14, 324, "Đ", "2", ": 220 V – 100 W", BLUE, 17)
assert YB2 - 24 - 14 > YB1 + 15 and YB1 - 24 - 14 > 14        # nhãn Đ2 không chạm bóng Đ1, nhãn Đ1 không vượt mép trên
fig4 = wrap("0 0 420 336", "Hai bóng đèn Đ1 40 oát và Đ2 100 oát: bên trái mắc nối tiếp, bên phải mắc song song, cùng nối vào 220 vôn", b,
            "Hình 4. Cùng hai bóng đèn, nối vào 220 V theo hai cách.")

# ---------- Kiểm số liệu quiz / bài toán mẫu / thử thách
assert abs(1000 * 8 / (10 * 24) - 33.3) < 0.1                       # dự đoán: gấp hơn 30 lần
assert abs(60 / 220 - 0.2727) < 1e-4 and 220 * 60 == 13200 and abs(220 / 60 - 3.667) < 1e-3 and abs(0.06 / 220 - 0.000273) < 1e-6  # Câu 2
assert abs(0.6 / 0.5 - 1.2) < 1e-12 and abs(0.6 * 0.5 - 0.3) < 1e-12 and abs(0.6 / 30 * 1000 - 20) < 1e-9   # Câu 3
assert 75 * 7200 == 540000 and 75 * 2 == 150 and 75 * 120 == 9000 and abs(75 * 2 / 1000 - 0.15) < 1e-12      # Câu 5
assert 40 * 18000 == 720000 and abs(0.04 * 5 - 0.2) < 1e-12 and abs(0.2 * 3.6e6 - 720000) < 1e-6           # bảng Bẫy 2
R1q, R2q = 220 ** 2 / 40, 220 ** 2 / 100                            # Câu 6
Iq = 220 / (R1q + R2q)
assert R1q == 1210 and R2q == 484 and Iq ** 2 * R1q > Iq ** 2 * R2q and Iq ** 2 * R1q < 40
assert abs(220 ** 2 / 48.4 - 1000) < 1e-6                           # ví dụ dây nung
I_m, R_m = 800 / 220, 220 ** 2 / 800                                # bài toán mẫu
assert abs(I_m - 3.636) < 1e-3 and abs(R_m - 60.5) < 1e-9
A_m = 0.8 * 1.5 * 30
assert abs(A_m - 36) < 1e-9 and abs(A_m * 2000 - 72000) < 1e-6
assert abs(800 * 45 * 3600 - 1.296e8) < 1 and abs(1.296e8 / 3.6e6 - 36) < 1e-9
assert abs(0.8 * 0.75 * 30 - 18) < 1e-9 and abs(18 * 2000 - 36000) < 1e-6
assert abs(200 ** 2 / R_m - 661.16) < 0.01                          # thử sức 200 V
A_tl = 0.12 * 24 * 30                                               # Câu 7
assert abs(A_tl - 86.4) < 1e-9 and abs(A_tl * 2000 - 172800) < 1e-6
assert abs(120 * 24 * 30 * 2000 - 172800000) < 1e-3 and abs(0.12 * 30 * 2000 - 7200) < 1e-9 and abs(0.12 * 24 * 2000 - 5760) < 1e-9
assert abs(2.5 * 3.6e6 - 9e6) < 1e-6 and abs(10 * 0.051 * 5 * 30 - 76.5) < 1e-9 and 60 / 9 > 6   # thử thách ⭐, ⭐⭐
Ra3, Rb3 = 110 ** 2 / 100, 110 ** 2 / 25
I3c = 220 / (Ra3 + Rb3)
assert Ra3 == 121 and Rb3 == 484 and abs(I3c - 0.3636) < 1e-4 and abs(I3c * Rb3 - 176) < 1e-9   # thử thách ⭐⭐⭐
# thí nghiệm 3 (X 6 V – 3 W, Y 6 V – 6 W, nguồn 6 V, coi R không đổi)
RX, RY = 6 ** 2 / 3, 6 ** 2 / 6
I_nt = 6 / (RX + RY)
PX_nt, PY_nt = I_nt ** 2 * RX, I_nt ** 2 * RY
assert RX == 12 and RY == 6 and abs(I_nt - 1 / 3) < 1e-12 and PX_nt > PY_nt and PY_nt / 6 < 0.12

# ---------- Dựng theory.html
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in (("__U_TN1__", U_TN1), ("__BANG_TN1__", bang1), ("__NHAN_XET_TN1__", NX1),
             ("__CT_TRUOC__", CT_TRUOC), ("__CT_SAU__", CT_SAU), ("__PHUT__", str(PHUT))):
    assert k in h, k
    h = h.replace(k, v)
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 13. Năng lượng của dòng điện và công suất điện"
SRC = "content/lesson-samples/l9-nang-luong-dong-dien-cong-suat/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 91, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-congsuat-01", "ten": "Đo U, I của bóng đèn 6 V – 3 W, tính công suất P = UI", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["congsuat.p_bang_ui", "congsuat.so_dinh_muc", "congsuat.sai_so_do"],
  "muc_tieu": "Từ bảng U–I của bóng đèn thấy tích U·I càng lớn đèn càng sáng; ở đúng hiệu điện thế định mức, U·I bằng công suất ghi trên đèn.",
  "dung_cu": [{"ten": "Nguồn điện chỉnh được 0–6 V", "so_luong": 1},
              {"ten": "Bóng đèn sợi đốt 6 V – 3 W có đui", "so_luong": 1},
              {"ten": "Ampe kế (GHĐ 1 A, ĐCNN 0,01 A)", "so_luong": 1},
              {"ten": "Vôn kế (GHĐ 6 V, ĐCNN 0,1 V)", "so_luong": 1},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mắc mạch như Hình 2: ampe kế nối tiếp với đèn, vôn kế song song với đèn.",
                       "Lần lượt đặt U = " + "; ".join(vt(u, 1) for u in U1) + " V; mỗi lần đọc ampe kế và ghi độ sáng.",
                       "Tính tích U·I cho mỗi lần đo."],
               "quan_sat": ["Dây tóc từ đỏ mờ, sáng yếu, khá sáng tới sáng bình thường ở 6 V.",
                            "Tích U·I tăng từ khoảng 0,33 W lên 3,0 W."],
               "rut_ra": ["Tích U·I (công suất) càng lớn, đèn càng sáng.", "Ở đúng 6 V, U·I = 3,0 W bằng số ghi trên đèn: đó là công suất định mức.",
                          "I không tăng tỉ lệ với U vì điện trở dây tóc tăng khi nóng."]},
  "tham_so": [{"ky_hieu": "U", "ten": "Hiệu điện thế đặt vào đèn", "don_vi": "V", "kieu": "dieu_chinh", "min": 0, "max": 6, "mac_dinh": 6, "buoc": 0.5},
              {"ky_hieu": "U_dm", "ten": "Hiệu điện thế định mức", "don_vi": "V", "kieu": "co_dinh", "gia_tri": U_DM},
              {"ky_hieu": "P_dm", "ten": "Công suất định mức", "don_vi": "W", "kieu": "co_dinh", "gia_tri": P_DM},
              {"ky_hieu": "I", "ten": "Cường độ dòng điện đọc được", "don_vi": "A", "kieu": "do_duoc", "sai_so_do": 0.005},
              {"ky_hieu": "P", "ten": "Công suất P = U·I", "don_vi": "W", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["I = I_dm·(U/U_dm)^0,6 với I_dm = P_dm/U_dm = 0,5 A", "I_doc = lam_tron(I, 0,01 A)", "P = U·I_doc"],
              "gia_thiet": ["dây tóc vonfam: điện trở tăng khi nóng, mô hình gần đúng I tỉ lệ U^0,6",
                            "bỏ qua điện trở ampe kế, dây nối; vôn kế có điện trở rất lớn"]},
  "so_lieu_mau": {"cot": ["U (V)", "I (A)", "U·I (W)"],
                  "hang": [[u, ido, round(p, 2)] for u, _, ido, p in rows1],
                  "ghi_chu": "Số liệu minh hoạ từ mô hình I = 0,5·(U/6)^0,6, làm tròn 0,01 A; chưa phải số đo thật."},
  "ket_qua_ky_vong": "U·I ở 6 V bằng 3,0 W đúng số ghi; U tăng 4 lần thì U·I tăng khoảng 9 lần.",
  "hien_tuong_hay_sai": ["Nghĩ đèn lúc nào cũng có công suất 3 W vì số ghi là 3 W.", "Nghĩ U tăng 4 lần thì công suất cũng tăng 4 lần.",
                         "Dùng ampe kế GHĐ lớn, độ chia thô để 'an toàn' làm sai số lớn."],
  "sai_so_thuong_gap": "Đọc kim ampe kế lệch nửa vạch 0,005 A: khoảng 2 % ở 0,22 A, 1 % ở 0,50 A.",
  "an_toan": "Không đặt quá 6 V vào đèn 6 V – 3 W; bóng đèn nóng, không chạm tay.",
  "goi_y_mo_phong": {"loai": "bang_so_lieu+do_thi", "y_tuong": "Kéo thanh U, dây tóc sáng dần, kim ampe kế nhảy theo độ chia; bảng tự tính U·I.",
                     "diem_nhan": "Chỉ ở đúng 6 V, U·I mới bằng 3 W ghi trên đèn."}})
tn.append({**base,
  "id": "tn-l9-congsuat-02", "ten": "Đọc công tơ điện khi đun ấm điện 1 000 W trong 30 phút", "loai": "vi_du", "muc_do": "co_ban",
  "kien_thuc": ["congsuat.a_bang_pt", "congsuat.kwh_cong_to"],
  "muc_tieu": "Thấy công tơ đo điện năng theo kWh; số tăng thêm khớp A = P·t với P tính bằng kW, t tính bằng giờ.",
  "dung_cu": [{"ten": "Công tơ điện của gia đình (có ô số lẻ phần mười)", "so_luong": 1},
              {"ten": "Ấm điện 220 V – 1 000 W", "so_luong": 1},
              {"ten": "Đồng hồ bấm giờ", "so_luong": 1}],
  "cac_buoc": {"lam": ["Tắt mọi thiết bị khác trong nhà.", "Đọc công tơ, bật ấm ở đúng 220 V trong 30 phút, đọc lại công tơ."],
               "quan_sat": ["Công tơ tăng từ 1234,6 lên 1235,1."],
               "rut_ra": ["Ấm tiêu thụ 0,5 kWh.", "A = P·t = 1 kW · 0,5 h = 0,5 kWh: khớp số đọc trên công tơ."]},
  "tham_so": [{"ky_hieu": "P", "ten": "Công suất thiết bị", "don_vi": "W", "kieu": "dieu_chinh", "min": 100, "max": 2000, "mac_dinh": 1000, "buoc": 100},
              {"ky_hieu": "t", "ten": "Thời gian bật", "don_vi": "h", "kieu": "dieu_chinh", "min": 0.25, "max": 3, "mac_dinh": 0.5, "buoc": 0.25},
              {"ky_hieu": "A", "ten": "Điện năng tiêu thụ", "don_vi": "kWh", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["A = P·t (P tính bằng kW, t bằng h)", "số công tơ sau = số trước + A"],
              "gia_thiet": ["ấm chạy đúng công suất định mức suốt 30 phút", "chỉ có ấm tiêu thụ điện trong thời gian đo"]},
  "so_lieu_mau": {"cot": ["P (W)", "t (h)", "Công tơ trước", "Công tơ sau", "A (kWh)"],
                  "hang": [[P_AM, T_AM, CT0, CT1, A_AM]],
                  "ghi_chu": "Số liệu minh hoạ tính từ A = P·t, chưa phải số đọc thật."},
  "ket_qua_ky_vong": "Công tơ tăng 0,5 số trong 30 phút.",
  "hien_tuong_hay_sai": ["Nghĩ công tơ đo công suất (W).", "Chia cho 30 phút thay vì 0,5 giờ."],
  "an_toan": "Không chạm tay vào công tơ, dây điện; chỉ đọc số.",
  "goi_y_mo_phong": {"loai": "bang_so_lieu", "y_tuong": "Chọn thiết bị và thời gian bật, mặt công tơ quay số theo A = P·t.",
                     "diem_nhan": "Cùng thời gian, thiết bị nhiều oát hơn làm công tơ nhảy nhanh hơn."}})
tn.append({**base,
  "id": "tn-l9-congsuat-03", "ten": "Hai bóng 6 V – 3 W và 6 V – 6 W mắc nối tiếp rồi song song", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["congsuat.noi_tiep_song_song", "congsuat.p_bang_i2r", "congsuat.so_dinh_muc"],
  "muc_tieu": "Thấy khi mắc nối tiếp, đèn ít oát hơn (điện trở lớn hơn) lại sáng hơn; khi mắc song song ở đúng định mức, đèn nhiều oát hơn sáng hơn.",
  "dung_cu": [{"ten": "Nguồn điện 6 V", "so_luong": 1},
              {"ten": "Bóng đèn X 6 V – 3 W, bóng đèn Y 6 V – 6 W, có đui", "so_luong": 2},
              {"ten": "Khoá K và dây nối", "so_luong": 1}],
  "cac_buoc": {"lam": ["Mắc X và Y nối tiếp vào nguồn 6 V, đóng khoá, so độ sáng.", "Mắc X và Y song song vào nguồn 6 V, so độ sáng."],
               "quan_sat": ["Nối tiếp: X sáng hơn, Y chỉ đỏ mờ.", "Song song: cả hai sáng bình thường, Y sáng hơn X."],
               "rut_ra": ["Nối tiếp cùng I: P = I²R, đèn điện trở lớn (ít oát) sáng hơn.",
                          "Song song đúng định mức: đèn nhiều oát sáng hơn."]},
  "tham_so": [{"ky_hieu": "U", "ten": "Hiệu điện thế nguồn", "don_vi": "V", "kieu": "dieu_chinh", "min": 0, "max": 6, "mac_dinh": 6, "buoc": 0.5},
              {"ky_hieu": "cach_mac", "ten": "Cách mắc (0 nối tiếp, 1 song song)", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0, "buoc": 1},
              {"ky_hieu": "R_X", "ten": "Điện trở đèn X (coi không đổi)", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": RX},
              {"ky_hieu": "R_Y", "ten": "Điện trở đèn Y (coi không đổi)", "don_vi": "Ω", "kieu": "co_dinh", "gia_tri": RY},
              {"ky_hieu": "P_X", "ten": "Công suất đèn X", "don_vi": "W", "kieu": "tinh_ra"},
              {"ky_hieu": "P_Y", "ten": "Công suất đèn Y", "don_vi": "W", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["R = U_dm²/P_dm", "nối tiếp: I = U/(R_X + R_Y), P = I²R", "song song: P = U²/R"],
              "gia_thiet": ["coi điện trở mỗi đèn không đổi (thực tế dây tóc nguội có điện trở nhỏ hơn, thứ tự sáng không đổi)",
                            "bỏ qua điện trở dây nối và nguồn"]},
  "so_lieu_mau": {"cot": ["Cách mắc", "Đèn", "U (V)", "I (A)", "P (W)"],
                  "hang": [["nối tiếp", "X", round(I_nt * RX, 2), round(I_nt, 2), round(PX_nt, 2)],
                           ["nối tiếp", "Y", round(I_nt * RY, 2), round(I_nt, 2), round(PY_nt, 2)],
                           ["song song", "X", 6.0, 0.5, 3.0], ["song song", "Y", 6.0, 1.0, 6.0]],
                  "ghi_chu": "Số liệu tính từ mô hình điện trở không đổi, chưa phải số đo thật."},
  "ket_qua_ky_vong": "Nối tiếp: P_X ≈ 1,33 W > P_Y ≈ 0,67 W. Song song: P_Y = 6 W > P_X = 3 W.",
  "hien_tuong_hay_sai": ["Nghĩ đèn ghi nhiều oát hơn lúc nào cũng sáng hơn.", "Nghĩ nối tiếp thì hai đèn sáng như nhau vì cùng dòng điện."],
  "an_toan": "Không mắc hai đèn 6 V song song vào nguồn lớn hơn 6 V.",
  "goi_y_mo_phong": {"loai": "so_do_luc+bang_so_lieu", "y_tuong": "Công tắc đổi nối tiếp/song song; độ sáng mỗi bóng vẽ theo P tính ra.",
                     "diem_nhan": "Đảo thứ tự độ sáng khi đổi cách mắc."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| TN1 I:", [r[2] for r in rows1], "P:", P1, "ratio=%.2f" % ratio,
      "| nt P_X=%.2f P_Y=%.2f" % (PX_nt, PY_nt), "| Câu 6 P1=%.1f P2=%.1f" % (Iq ** 2 * R1q, Iq ** 2 * R2q))
