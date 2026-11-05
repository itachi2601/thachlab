"""Bài tập mẫu bài 45 — Bài 26. Thực hành: Đo suất điện động và điện trở trong của pin điện hoá (Lớp 11). 3 dạng, dễ → khó.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-45.py  → ghi scripts/data/bai-tap-mau/45.json (review.checked=false)
Số liệu tính ở đầu file và có assert. Chủ đề ngân hàng: 'Suất điện động và điện trở trong của nguồn' (bài 43)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "45.json")
VB = "0 0 420 240"
NOTE = "Hình minh hoạ, không theo tỉ lệ."
TOPIC = "Suất điện động và điện trở trong của nguồn"

# ───────────── số liệu (tự kiểm) ─────────────
# Dạng 1
I1, U1, I2, U2 = 0.20, 1.36, 0.60, 1.00
r1 = (U1 - U2) / (I2 - I1); E1 = U1 + I1 * r1
assert abs(r1 - 0.90) < 1e-9 and abs(E1 - 1.54) < 1e-9 and abs(E1 - I2 * r1 - U2) < 1e-9
# Dạng 2
E2, r2, R0, Rx = 1.55, 0.60, 2.0, 3.0
Iq = E2 / (R0 + Rx + r2); Uq = E2 - Iq * r2
Isc = E2 / r2; Imax = E2 / (R0 + r2)
assert round(Iq, 3) == 0.277 and round(Uq, 2) == 1.38 and abs(Uq - Iq * (R0 + Rx)) < 1e-9
assert round(Isc, 2) == 2.58 and Isc > 2 and round(Imax, 3) == 0.596
# Dạng 3: pin E=1,55, r=0,45 (giấu trong bài), R0 = 2,0
RXS = [100, 20, 10, 5, 2, 0]
TB = []
for rx in RXS:
    I = 1.55 / (R0 + rx + 0.45); TB.append((round(I, 3), round(I * (R0 + rx), 2)))
assert TB == [(0.015, 1.54), (0.069, 1.52), (0.124, 1.49), (0.208, 1.46), (0.348, 1.39), (0.633, 1.27)], TB
r3 = (TB[0][1] - TB[5][1]) / (TB[5][0] - TB[0][0]); E3 = TB[0][1] + TB[0][0] * r3
rel = (0.01 + 0.01) / (TB[0][1] - TB[5][1]) + (0.002 + 0.002) / (TB[5][0] - TB[0][0]); dr = r3 * rel
assert round(r3, 2) == 0.44 and round(E3, 2) == 1.55 and round(rel, 3) == 0.081 and round(dr, 2) == 0.04, (r3, E3, rel, dr)
assert abs(1.55 - TB[3][0] * 0.44 - TB[3][1]) < 0.005
# vì sao không chọn cặp gần nhau: hiệu U của lần 3-4 chỉ 0,03 V so với sai số 0,02 V
assert round(TB[2][1] - TB[3][1], 2) == 0.03

# ───────────── hàm vẽ ─────────────
OX, OY = 62, 208

def axes_ui():
    return (seg(OX, OY, OX + 320, OY) + chevron(OX + 320, OY, 1, 0) + seg(OX, OY, OX, 24) + chevron(OX, 24, 0, -1)
            + lbl(OX + 318, OY + 22, "I (A)", "currentColor", 13, "end", "700") + lbl(OX + 8, 26, "U (V)", "currentColor", 13, "start", "700"))

def fade_in(t0, t1=None, dur=4.0):
    t1 = min(1.0, t0 + 0.12) if t1 is None else t1
    return f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{t0:.2f};{t1:.2f}" dur="{dur}s" begin="indefinite" fill="freeze"/>'

def circuit(anim, with_q):
    """Mạch đo: pin (M, N), R0 và Rx nối tiếp, ampe kế nối tiếp, vôn kế song song hai cực pin."""
    b = ""
    b += seg(90, 60, 150, 60) + f'<rect x="150" y="50" width="60" height="20" fill="none" stroke="currentColor" stroke-width="2"/>' + seg(210, 60, 260, 60)
    b += f'<rect x="260" y="50" width="60" height="20" fill="none" stroke="currentColor" stroke-width="2"/>' + seg(320, 60, 370, 60)
    b += lbl(180, 40, "R₀ = 2,0 Ω", ORG, 13, "middle", "700") + lbl(290, 40, "Rₓ = 3,0 Ω", ORG, 13, "middle", "700")
    b += seg(370, 60, 370, 190) + seg(370, 190, 244, 190) + seg(216, 190, 90, 190)
    b += f'<circle cx="230" cy="190" r="14" fill="none" stroke="currentColor" stroke-width="2"/>' + lbl(230, 195, "A", BLUE, 14, "middle", "700")
    b += seg(90, 60, 90, 100) + seg(90, 100, 90, 130) + seg(90, 142, 90, 190)
    b += seg(76, 130, 104, 130, "currentColor", 3) + seg(83, 142, 97, 142, "currentColor", 3) + lbl(72, 138, "pin", "currentColor", 13, "end", "700")
    b += seg(90, 100, 150, 100) + seg(150, 100, 150, 124) + seg(150, 152, 150, 190)
    b += f'<circle cx="150" cy="138" r="14" fill="none" stroke="currentColor" stroke-width="2"/>' + lbl(150, 143, "V", GRN, 14, "middle", "700")
    b += dot(90, 100, 3.5) + lbl(98, 92, "M", "currentColor", 12, "start", "700") + dot(90, 190, 3.5) + lbl(98, 208, "N", "currentColor", 12, "start", "700")
    if with_q:
        b += lbl(230, 226, "I = ?", BLUE, 14, "middle", "700") + lbl(168, 138, "U = ?", GRN, 14, "start", "700")
    return b

# ───────────── Dạng 1: hai cặp (I, U) → r, E ─────────────
def px1(I): return OX + I / 0.7 * 300
def py1(U): return OY - (U - 0.9) / 0.7 * 170

def d1(k):
    P1 = (px1(I1), py1(U1)); P2 = (px1(I2), py1(U2))
    b = axes_ui() + seg(*P1, *P2, MUTEDC, 1.8, "5 4")
    if k == 0:
        pts = [(P1[0] + (P2[0] - P1[0]) * t / 20, P1[1] + (P2[1] - P1[1]) * t / 20) for t in range(21)]
        b += dot(*P1, 5, ORG) + dot(*P2, 5, ORG) + lbl(P1[0] + 8, P1[1] - 10, "lần 1: 0,20 A · 1,36 V", ORG, 13, "start", "700")
        b += lbl(P2[0] - 10, P2[1] + 18, "lần 2: 0,60 A · 1,00 V", ORG, 13, "end", "700")
        b += lbl(OX + 160, OY + 20, "vặn Rₓ nhỏ dần: I tăng, U giảm", "currentColor", 12, "middle", "400")
        b += ball(pts, 0, 0.1)
        return fig("d1-0", VB, "Hai điểm đo (I, U) của một pin; chấm chạy từ lần 1 sang lần 2 khi vặn biến trở", b,
                   "Mô phỏng: chấm chạy từ lần đo 1 sang lần đo 2 khi vặn biến trở (1 s thật = 1 s). " + NOTE)
    b += dot(*P1, 5, ORG) + dot(*P2, 5, ORG)
    b += seg(P1[0], P1[1], P1[0], OY, "currentColor", 1, "3 4") + seg(P2[0], P2[1], P2[0], OY, "currentColor", 1, "3 4")
    b += seg(OX, P1[1], P1[0], P1[1], "currentColor", 1, "3 4") + seg(OX, P2[1], P2[0], P2[1], "currentColor", 1, "3 4")
    b += sub(P1[0], OY + 18, "I", "1", "currentColor", 13, "middle") + sub(P2[0], OY + 18, "I", "2", "currentColor", 13, "middle")
    b += sub(OX - 6, P1[1] + 4, "U", "1", "currentColor", 13, "end") + sub(OX - 6, P2[1] + 4, "U", "2", "currentColor", 13, "end")
    b += lbl(OX + 8, 56, "ℰ = ?", RED, 14, "start", "700") + lbl(P1[0] + 70, P1[1] + 50, "r = ?", RED, 14, "start", "700")
    return fig("d1-2", VB, "Đồ thị U theo I với hai điểm đo; cần tìm r và ℰ", b, "Dữ kiện: hai điểm đo (I₁, U₁) và (I₂, U₂). " + NOTE)

MUTEDC = "#94a3b8"

# ───────────── Dạng 2: mạch đo, dự đoán số chỉ ─────────────
def d2(k):
    b = circuit(k == 0, k == 2)
    if k == 0:
        perim = [(90, 60), (370, 60), (370, 190), (90, 190), (90, 60)]
        pts = []
        tot = sum(math.hypot(perim[i + 1][0] - perim[i][0], perim[i + 1][1] - perim[i][1]) for i in range(4))
        for n in range(61):
            s = tot * n / 60
            for i in range(4):
                L = math.hypot(perim[i + 1][0] - perim[i][0], perim[i + 1][1] - perim[i][1])
                if s <= L + 1e-9:
                    f = s / L; pts.append((perim[i][0] + (perim[i + 1][0] - perim[i][0]) * f, perim[i][1] + (perim[i + 1][1] - perim[i][1]) * f)); break
                s -= L
        b += ball(pts, 0, 0.07)
        return fig("d2-0", VB, "Mạch đo gồm pin, R0, Rx, ampe kế nối tiếp và vôn kế song song hai cực pin; chấm chạy một vòng", b,
                   "Mô phỏng: chấm là dòng điện quy ước chạy một vòng quanh mạch kín (chạy chậm, không theo tỉ lệ). " + NOTE)
    return fig("d2-2", VB, "Sơ đồ mạch đo với số chỉ ampe kế và vôn kế cần tìm", b, "Dữ kiện: pin ℰ = 1,55 V, r = 0,60 Ω; R₀ = 2,0 Ω; Rₓ = 3,0 Ω. " + NOTE)

# ───────────── Dạng 3: bảng 6 lần đo ─────────────
def px3(I): return OX + I / 0.7 * 300
def py3(U): return OY - (U - 1.2) / 0.4 * 170

def d3(k):
    b = axes_ui()
    for n, (I, U) in enumerate(TB):
        x, y = px3(I), py3(U)
        t0 = 0.1 + 0.13 * n
        g = dot(x, y, 5, ORG) + lbl(x + 7, y - 9, str(n + 1), ORG, 13, "start", "700")
        if k == 0:
            g = f'<g>{g}{fade_in(t0, t0 + 0.08)}</g>'
        b += g
    if k == 0:
        b += lbl(OX + 160, OY - 6, "6 lần đo, Rₓ giảm từ 100 Ω về 0", "currentColor", 12, "middle", "400")
        return fig("d3-0", VB, "Sáu điểm đo (I, U) của một pin lần lượt hiện ra khi biến trở giảm dần", b,
                   "Mô phỏng: sáu điểm đo lần lượt hiện ra (số trên điểm là lần đo). " + NOTE)
    b += lbl(OX + 250, 120, "gần một đường thẳng dốc xuống", MUTEDC, 12, "middle", "400")
    return fig("d3-2", VB, "Sáu điểm đo (I, U) đánh số theo lần đo", b, "Dữ kiện: sáu điểm đo theo bảng trong đề. " + NOTE)

BUILD = [d1, d2, d3]

# ───────────── đề ─────────────
def table3():
    rows = "".join(f"<tr><td>{n + 1}</td><td>{rx}</td><td>{I:.3f}</td><td>{U:.2f}</td></tr>".replace(".", ",") for n, (rx, (I, U)) in enumerate(zip(RXS, TB)))
    return ('<div class="table-scroll"><table class="tl-table"><thead><tr><th>Lần</th><th>$R_x\\ (\\Omega)$</th><th>$I$ (A)</th><th>$U$ (V)</th></tr></thead><tbody>'
            + rows + '</tbody></table></div>')

DANG = [
 dict(label="Dạng 1 · Dễ · Hai cặp (I, U) của pin: tìm điện trở trong và suất điện động", topic=TOPIC,
      problem_html=(r"<p>Một nhóm đo một viên pin: mắc pin với điện trở bảo vệ, biến trở, ampe kế nối tiếp và vôn kế song song hai cực pin. "
                    r"Vặn biến trở hai lần, đọc được:</p>"
                    r"<ul><li>Lần 1: $I_1 = 0{,}20\ \text{A}$, $U_1 = 1{,}36\ \text{V}$;</li><li>Lần 2: $I_2 = 0{,}60\ \text{A}$, $U_2 = 1{,}00\ \text{V}$.</li></ul>"
                    r"<p>$U$ là số chỉ vôn kế (hiệu điện thế hai cực pin). Hai lần đo cùng một pin, $\mathcal{E}$ và $r$ không đổi.</p>"
                    r"<p>a) Tính điện trở trong $r$ của pin.</p><p>b) Tính suất điện động $\mathcal{E}$ của pin.</p>")),
 dict(label="Dạng 2 · Trung bình · Dự đoán số chỉ ampe kế, vôn kế và vai trò điện trở bảo vệ", topic=TOPIC,
      problem_html=(r"<p>Mạch đo như hình: pin cũ có $\mathcal{E} = 1{,}55\ \text{V}$, $r = 0{,}60\ \Omega$; điện trở bảo vệ $R_0 = 2{,}0\ \Omega$ nối tiếp biến trở, "
                    r"đang vặn ở $R_x = 3{,}0\ \Omega$. Ampe kế có điện trở không đáng kể, vôn kế mắc song song hai cực pin có điện trở rất lớn. Khoá K đóng.</p>"
                    r"<p>a) Ampe kế chỉ bao nhiêu?</p><p>b) Vôn kế chỉ bao nhiêu?</p>"
                    r"<p>c) Giả sử bạn học sinh bỏ $R_0$ rồi vặn $R_x$ về $0$. Dòng qua pin lúc đó là bao nhiêu? Ampe kế thang $2\ \text{A}$ có chịu được không?</p>")),
 dict(label="Dạng 3 · Khó · Xử lý bảng số liệu: chọn cặp điểm, tính r, ℰ và sai số", topic=TOPIC,
      problem_html=(r"<p>Bảng số liệu đo một viên pin AA, điện trở bảo vệ $R_0 = 2{,}0\ \Omega$; vôn kế sai số $\pm 0{,}01\ \text{V}$, ampe kế sai số $\pm 0{,}002\ \text{A}$:</p>"
                    + table3() +
                    r"<p>a) Chọn hai lần đo cho giá trị $r$ đáng tin nhất (không vẽ đồ thị) và tính $r$.</p>"
                    r"<p>b) Tính suất điện động $\mathcal{E}$.</p>"
                    r"<p>c) Coi $r$ là thương của hai hiệu; ước lượng $\Delta r$ bằng cách cộng sai số tỉ đối của tử số và mẫu số, rồi ghi kết quả $r = \ldots \pm \ldots$</p>")),
]

# ───────────── bảng phân tích đề ─────────────
ANALYSIS = [
 [("\"vôn kế song song hai cực pin\"", "$U$ là hiệu điện thế hai cực pin",
   r"⚠ Có dòng $I \gt 0$ chạy thì $U \lt \mathcal{E}$: số vôn kế chỉ không phải $\mathcal{E}$ (chỉ khi mạch hở mới bằng nhau)."),
  ("\"Lần 1: $I_1 = 0{,}20\\ \\text{A}$, $U_1 = 1{,}36\\ \\text{V}$\"", "Điểm $(0{,}20\\ \\text{A};\\ 1{,}36\\ \\text{V})$", r"Mỗi cặp $(I, U)$ thoả hệ thức $U = \mathcal{E} - Ir$."),
  ("\"Lần 2: $I_2 = 0{,}60\\ \\text{A}$, $U_2 = 1{,}00\\ \\text{V}$\"", "Điểm $(0{,}60\\ \\text{A};\\ 1{,}00\\ \\text{V})$", r"Hai cặp cho hai phương trình cùng $\mathcal{E}$, $r$: trừ vế thì mất đại lượng nào?"),
  ("\"Tính điện trở trong $r$\"", "Cần tìm $r$", r"$r = \dfrac{U_1 - U_2}{I_2 - I_1}$"),
  ("\"Tính suất điện động $\\mathcal{E}$\"", "Cần tìm $\\mathcal{E}$", r"Thế một cặp $(I, U)$ và $r$ vừa tìm: $\mathcal{E} = U + Ir$.")],
 [("\"pin cũ có $\\mathcal{E} = 1{,}55\\ \\text{V}$, $r = 0{,}60\\ \\Omega$\"", "$\\mathcal{E}$, $r$ đã biết", r"Hai đại lượng có mặt trong định luật Ohm toàn mạch."),
  ("\"$R_0 = 2{,}0\\ \\Omega$ nối tiếp biến trở, $R_x = 3{,}0\\ \\Omega$\"", "Mạch ngoài $R_0 + R_x$", r"Điện trở mắc nối tiếp: điện trở tương đương? Điện trở trong $r$ cũng nằm nối tiếp trong toàn mạch."),
  ("\"ampe kế điện trở không đáng kể; vôn kế điện trở rất lớn\"", "$R_A \\approx 0$, $R_V \\to \\infty$",
   r"⚠ Ampe kế nối tiếp, vôn kế song song: ampe kế có làm đổi điện trở toàn mạch không? Vôn kế có kéo dòng không?"),
  ("\"Ampe kế chỉ bao nhiêu?\"", "Cần tìm $I$", r"Định luật Ohm toàn mạch: $I = \dfrac{\mathcal{E}}{R_{\text{ngoài}} + r}$"),
  ("\"Vôn kế chỉ bao nhiêu?\"", "Cần tìm $U$", r"Hệ thức giữa $U$, $\mathcal{E}$, $I$, $r$."),
  ("\"bỏ $R_0$, vặn $R_x$ về $0$\"", "Điện trở ngoài thay đổi", r"Điện trở ngoài thay đổi thì dòng trong mạch đổi thế nào?")],
 [("\"bảng 6 lần đo, $R_x$ từ $100\\ \\Omega$ về $0$\"", "$I$ tăng, $U$ giảm dần", r"Đồ thị $U$–$I$ của pin có dạng gì? Hệ thức nào mô tả?"),
  ("\"vôn kế $\\pm 0{,}01\\ \\text{V}$, ampe kế $\\pm 0{,}002\\ \\text{A}$\"", "$\\Delta U$, $\\Delta I$ của mỗi số đọc",
   r"⚠ Một hiệu hai số đo mang sai số của cả hai số: hiệu càng nhỏ so với sai số thì sai số tỉ đối càng lớn."),
  ("\"chọn hai lần đo cho $r$ đáng tin nhất\"", "Hai lần đo nào?", r"So sai số tỉ đối của hiệu $U$ ở một cặp xa nhau và một cặp gần nhau."),
  ("\"tính $r$\"", "Cần tìm $r$", r"Hai cặp $(I, U)$ cho hệ thức nào chứa $r$ mà không cần biết $\mathcal{E}$?"),
  ("\"tính $\\mathcal{E}$\"", "Cần tìm $\\mathcal{E}$", r"Đã biết $r$, dùng một cặp $(I, U)$ với hệ thức nào? Số hạng $Ir$ mang dấu gì?"),
  ("\"ước lượng $\\Delta r$ ... ghi kết quả\"", "Cần tìm $\\Delta r$", r"$r$ là thương của hai hiệu: sai số tỉ đối của một thương tính thế nào? $\Delta r$ giữ mấy chữ số có nghĩa?")],
]

# ───────────── lời giải ─────────────
R1 = [r"<strong>Khái niệm:</strong> hiệu điện thế hai cực pin khi có dòng: $U = \mathcal{E} - Ir$; chỉ khi $I = 0$ mới có $U = \mathcal{E}$.",
      r"<strong>Định luật:</strong> hai cặp $(I, U)$ của cùng một pin cùng thoả hệ thức này.",
      r"<strong>Công thức:</strong> $r = \dfrac{U_1 - U_2}{I_2 - I_1}$ · $\mathcal{E} = U + Ir$.",
      r"⚠ <strong>Điều kiện:</strong> hai lần đo cùng một pin; $\mathcal{E}$ và $r$ không đổi giữa hai lần."]
R2 = [r"<strong>Khái niệm:</strong> $\mathcal{E}$ là suất điện động của pin; $r$ là điện trở trong; dòng chạy qua cả mạch ngoài và $r$.",
      r"<strong>Định luật Ohm toàn mạch:</strong> $I = \dfrac{\mathcal{E}}{R_{\text{ngoài}} + r}$.",
      r"<strong>Hiệu điện thế hai cực pin:</strong> $U = \mathcal{E} - Ir$.",
      r"⚠ <strong>Điều kiện:</strong> ampe kế điện trở không đáng kể (nối tiếp); vôn kế điện trở rất lớn (song song, không kéo dòng)."]
R3 = [r"<strong>Khái niệm:</strong> sai số của hiệu hai số đo bằng tổng hai sai số; sai số tỉ đối của thương bằng tổng sai số tỉ đối của tử và mẫu.",
      r"<strong>Hệ thức:</strong> $U = \mathcal{E} - Ir$ ⇒ $r = \dfrac{U_1 - U_2}{I_2 - I_1}$, $\mathcal{E} = U + Ir$.",
      r"<strong>Sai số tỉ đối:</strong> $\dfrac{\Delta r}{r} = \dfrac{\Delta(U_1 - U_2)}{U_1 - U_2} + \dfrac{\Delta(I_2 - I_1)}{I_2 - I_1}$.",
      r"⚠ <strong>Điều kiện:</strong> hai lần đo xa nhau thì hiệu lớn, sai số tỉ đối nhỏ. Không dùng $U/I$ của một cặp (đó là điện trở mạch ngoài)."]

SOLS = [
 sol(R1, [
  ("Tìm điện trở trong $r$", [P(r"Viết $U = \mathcal{E} - Ir$ cho hai lần đo rồi trừ vế, $\mathcal{E}$ mất đi:"), M(r"U_1 - U_2 = (I_2 - I_1)\,r"),
                              M(r"r = \dfrac{U_1 - U_2}{I_2 - I_1}"), M(r"r = \dfrac{1{,}36 - 1{,}00}{0{,}60 - 0{,}20}"), A(r"r = 0{,}90\ \Omega")]),
  ("Tìm suất điện động $\\mathcal{E}$", [P(r"Thế lần 1 vào $U_1 = \mathcal{E} - I_1 r$:"), M(r"\mathcal{E} = U_1 + I_1 r"), M(r"\mathcal{E} = 1{,}36 + 0{,}20 \cdot 0{,}90"),
                                          A(r"\mathcal{E} = 1{,}54\ \text{V}")]),
  ("Kiểm tra", [P(r"Thế vào lần 2 phải ra đúng số đo:"), M(r"U_2 = 1{,}54 - 0{,}60 \cdot 0{,}90 = 1{,}00\ \text{V}"),
                P(r"Khớp. $\mathcal{E}$ lớn hơn cả hai số vôn kế đọc vì có dòng chạy; $r \approx 1\ \Omega$ là cỡ của một viên pin AA đã dùng.")])],
  [r"a) $r = 0{,}90\ \Omega$", r"b) $\mathcal{E} = 1{,}54\ \text{V}$"],
  r"Nhận dạng: đề cho <strong>hai cặp $(I, U)$ của cùng một pin</strong> → trừ vế hai hệ thức $U = \mathcal{E} - Ir$ để tìm $r$, rồi thế lại tìm $\mathcal{E}$."),
 sol(R2, [
  ("Tính dòng điện qua mạch", [P(r"Mạch ngoài $R_0 + R_x$ nối tiếp, cộng thêm $r$ của pin:"), M(r"I = \dfrac{\mathcal{E}}{R_0 + R_x + r}"),
                               M(r"I = \dfrac{1{,}55}{2{,}0 + 3{,}0 + 0{,}60}"), A(r"I \approx 0{,}277\ \text{A}")]),
  ("Số chỉ vôn kế", [P(r"Vôn kế đo hiệu điện thế hai cực pin, nhỏ hơn $\mathcal{E}$ vì có dòng chạy:"), M(r"U = \mathcal{E} - Ir"),
                     M(r"U = 1{,}55 - 0{,}277 \cdot 0{,}60"), A(r"U \approx 1{,}38\ \text{V}")]),
  ("Dòng khi bỏ $R_0$ và vặn $R_x$ về $0$", [P(r"Mạch ngoài chỉ còn dây nối, điện trở coi bằng $0$, toàn mạch chỉ còn $r$:"), M(r"I = \dfrac{\mathcal{E}}{r}"),
                                              M(r"I = \dfrac{1{,}55}{0{,}60}"), A(r"I \approx 2{,}58\ \text{A}")]),
  ("Kiểm tra với thang ampe kế", [P(r"$2{,}58\ \text{A}$ vượt thang $2\ \text{A}$: ampe kế quá tải, pin nóng nhanh."),
                                  P(r"Khi có $R_0$ và $R_x = 0$: $I = \dfrac{1{,}55}{2{,}0 + 0{,}60} \approx 0{,}596\ \text{A}$, an toàn. Đó là lí do mắc điện trở bảo vệ.")])],
  [r"a) $I \approx 0{,}277\ \text{A}$", r"b) $U \approx 1{,}38\ \text{V}$", r"c) $I \approx 2{,}58\ \text{A}$, vượt thang $2\ \text{A}$: không chịu được"],
  r"Nhận dạng: đề cho <strong>pin có điện trở trong và các điện trở nối tiếp</strong> → định luật Ohm toàn mạch tìm $I$, rồi $U = \mathcal{E} - Ir$."),
 sol(R3, [
  ("Chọn hai lần đo", [P(r"Sai số mỗi số đo cố định, nên hiệu hai số càng lớn thì sai số tỉ đối của hiệu càng nhỏ. Chọn lần 1 và lần 6 (xa nhau nhất):"),
                       A(r"T:Hiệu $U$: $1{,}54 - 1{,}27 = 0{,}27\ \text{V}$; hiệu $I$: $0{,}633 - 0{,}015 = 0{,}618\ \text{A}$."),
                       P(r"Hai lần liền kề, chẳng hạn lần 3 và 4, có hiệu $U$ chỉ $0{,}03\ \text{V}$ so với sai số $0{,}02\ \text{V}$: không dùng được.")]),
  ("Tính $r$", [M(r"r = \dfrac{U_1 - U_6}{I_6 - I_1}"), M(r"r = \dfrac{1{,}54 - 1{,}27}{0{,}633 - 0{,}015}"), A(r"r \approx 0{,}44\ \Omega")]),
  ("Tính $\\mathcal{E}$", [P(r"Thế lần 1 và $r$ vừa tìm vào $U = \mathcal{E} - Ir$:"), M(r"\mathcal{E} = U_1 + I_1 r"), M(r"\mathcal{E} = 1{,}54 + 0{,}015 \cdot 0{,}437"),
                          A(r"\mathcal{E} \approx 1{,}55\ \text{V}")]),
  ("Sai số của $r$", [P(r"Tử $U_1 - U_6$ mang sai số $0{,}01 + 0{,}01$ V; mẫu $I_6 - I_1$ mang $0{,}002 + 0{,}002$ A:"),
                      M(r"\dfrac{\Delta r}{r} = \dfrac{0{,}01 + 0{,}01}{0{,}27} + \dfrac{0{,}002 + 0{,}002}{0{,}618} \approx 0{,}081"),
                      M(r"\Delta r = 0{,}437 \cdot 0{,}081"), A(r"\Delta r \approx 0{,}04\ \Omega")]),
  ("Ghi kết quả và kiểm tra", [P(r"$\Delta r$ giữ 1 chữ số có nghĩa, $r$ viết cùng bậc thập phân với $\Delta r$:"), A(r"r = (0{,}44 \pm 0{,}04)\ \Omega"),
                               P(r"Kiểm tra bằng lần 4: $U = 1{,}55 - 0{,}208 \cdot 0{,}44 \approx 1{,}46\ \text{V}$, khớp bảng.")])],
  [r"a) Chọn lần 1 và lần 6; $r \approx 0{,}44\ \Omega$", r"b) $\mathcal{E} \approx 1{,}55\ \text{V}$", r"c) $\Delta r \approx 0{,}04\ \Omega$; $r = (0{,}44 \pm 0{,}04)\ \Omega$"],
  r"Nhận dạng: đề cho <strong>bảng $(I, U)$ kèm sai số dụng cụ</strong> → chọn hai điểm xa nhau, trừ vế tìm $r$, thế tìm $\mathcal{E}$, cộng sai số tỉ đối của tử và mẫu."),
]

# ───────────── tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>hai cặp (I, U) của cùng một pin</b> → nghĩ tới <b>trừ vế hai hệ thức</b> U = ℰ − Ir để tìm r",
      cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Tìm điện trở trong r", "Điện trở trong r của pin bằng bao nhiêu (Ω)?", dap_so=0.9, don_vi="Ω", sai_so=0.03,
       loi=r"Lấy $U_1/I_1$ của một lần đo: đó là điện trở mạch ngoài, không phải điện trở trong."),
  buoc("Tìm suất điện động ℰ", "Suất điện động ℰ của pin bằng bao nhiêu (V)?", dap_so=1.54, don_vi="V", sai_so=0.02,
       loi=r"Lấy ℰ bằng số vôn kế đọc lớn hơn, quên cộng phần $Ir$ mất trong pin; hoặc trừ $Ir$ thay vì cộng.",
       ke=[(r"Thế một cặp (I, U) và r vừa tìm vào U = ℰ − Ir rồi giải ra ℰ", True),
           (r"Lấy ℰ bằng số vôn kế đọc ở lần có dòng nhỏ hơn", r"Cả hai lần đều có dòng I > 0 nên U < ℰ; ℰ chỉ bằng U khi I = 0."),
           (r"Lấy ℰ bằng trung bình cộng của hai số vôn kế đọc", r"Trung bình hai U không ứng với I = 0 nên không phải ℰ.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>pin có r và điện trở nối tiếp</b> → nghĩ tới <b>Ohm toàn mạch</b>, rồi U = ℰ − Ir",
      cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tính dòng điện qua mạch", "Ampe kế chỉ bao nhiêu (A)?", dap_so=0.277, don_vi="A", sai_so=0.003,
       loi=r"Quên cộng điện trở trong $r$ vào mẫu số, chỉ chia cho $R_0 + R_x$."),
  buoc("Số chỉ vôn kế", "Vôn kế (hai cực pin) chỉ bao nhiêu (V)?", dap_so=1.38, don_vi="V", sai_so=0.02,
       loi=r"Cho rằng vôn kế đọc đúng ℰ của pin dù đang có dòng chạy.",
       ke=[(r"Hiệu điện thế hai cực pin: U = ℰ − Ir", True),
           (r"Vôn kế mắc ở hai cực pin nên chỉ đúng ℰ", r"Có dòng I > 0 thì một phần Ir mất ngay trong pin; vôn kế chỉ đọc ℰ khi hở mạch."),
           (r"Hiệu điện thế hai cực pin là U = I·r", r"I·r là phần sụt bên trong pin, không phải hiệu điện thế giữa hai cực.")]),
  buoc("Dòng khi bỏ R₀ và vặn Rₓ về 0", "Dòng qua pin lúc đó bằng bao nhiêu (A)?", dap_so=2.58, don_vi="A", sai_so=0.05,
       loi=r"Cho dòng không đổi vì pin không đổi, hoặc cho dòng bằng 0 vì \"không còn điện trở\".",
       ke=[(r"Mạch ngoài chỉ còn dây nối nên toàn mạch chỉ còn r: I = ℰ/r", True),
           (r"Dòng vẫn như ở câu a vì pin không đổi", r"Dòng phụ thuộc điện trở toàn mạch; bỏ hai điện trở ngoài thì mạch chỉ còn r."),
           (r"Dòng bằng 0 vì không còn điện trở ngoài", r"Điện trở ngoài càng nhỏ thì dòng càng lớn; I = ℰ/(R + r) không bằng 0.")]),
  buoc("Kiểm tra với thang ampe kế")]),
 dict(nhan_dang=r"Thấy <b>bảng (I, U) kèm sai số</b> → nghĩ tới <b>hai điểm xa nhau</b>, trừ vế tìm r, cộng sai số tỉ đối",
      cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Chọn hai lần đo", "Chọn cặp lần đo nào để tính r đáng tin nhất?",
       loi=r"Chọn hai lần liền kề cho \"gần nhau, sát đường thẳng\": hiệu hai số quá nhỏ so với sai số.",
       lua_chon=[(r"Lần 1 và lần 6 (xa nhau nhất)", True),
                 (r"Lần 3 và lần 4 (ở giữa bảng)", r"Hiệu U của hai lần này chỉ 0,03 V so với sai số 0,02 V của hiệu, nên r sai số rất lớn."),
                 (r"Lần 2 và lần 3 (liền kề)", r"Hiệu U của hai lần liền kề chỉ 0,03 V, so với sai số 0,02 V thì sai số tỉ đối của hiệu rất lớn.")]),
  buoc("Tính r", "Điện trở trong r bằng bao nhiêu (Ω)?", dap_so=0.44, don_vi="Ω", sai_so=0.02,
       loi=r"Lấy $U_6/I_6$ của một lần đo: đó là điện trở mạch ngoài $R_0 + R_x$.",
       ke=[(r"Lấy hiệu hai U chia hiệu hai I (vôn tụt chia ampe tăng)", True),
           (r"Lấy U₆ chia I₆ của lần đo cuối", r"U/I của một cặp là điện trở mạch ngoài, không phải điện trở trong."),
           (r"Lấy hiệu hai U chia tổng hai I", r"Mẫu số phải là hiệu hai dòng I₆ − I₁, không phải tổng.")]),
  buoc("Tính ℰ", "Suất điện động ℰ bằng bao nhiêu (V)?", dap_so=1.55, don_vi="V", sai_so=0.01,
       loi=r"Trừ $Ir$ thay vì cộng, hoặc lấy ℰ bằng trung bình hai số vôn kế.",
       ke=[(r"Thế một cặp (I, U) và r vừa tìm vào U = ℰ − Ir", True),
           (r"Lấy ℰ bằng trung bình cộng U₁ và U₆", r"Trung bình hai U không ứng với I = 0 nên không phải ℰ."),
           (r"Lấy ℰ = U₁ − I₁·r", r"Sai dấu: U = ℰ − Ir nên ℰ = U + Ir, phần Ir phải cộng thêm.")]),
  buoc("Sai số của r", "Sai số tuyệt đối Δr bằng bao nhiêu (Ω)?", dap_so=0.04, don_vi="Ω", sai_so=0.01,
       loi=r"Lấy $\Delta r$ bằng luôn sai số của vôn kế, quên rằng tử và mẫu đều là hiệu hai số đo.",
       ke=[(r"Cộng sai số tỉ đối của tử và mẫu: Δr/r = ΔX/X + ΔY/Y", True),
           (r"Lấy Δr bằng ΔU chia ΔI của dụng cụ", r"Tử và mẫu là hiệu hai số đo nên mang sai số của cả hai số; phải cộng sai số tỉ đối chứ không chia sai số tuyệt đối."),
           (r"Lấy Δr bằng sai số của vôn kế", r"r phụ thuộc cả U lẫN I; đơn vị V cũng không phải Ω.")]),
  buoc("Ghi kết quả và kiểm tra")]),
]

write(J, 45, "Bài 26. Thực hành: Đo suất điện động và điện trở trong của pin điện hoá", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
