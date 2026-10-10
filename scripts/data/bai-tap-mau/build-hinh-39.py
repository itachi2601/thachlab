"""Bài tập mẫu Bài 20 "Điện thế" (Vật lí 11, chương 3 Điện trường) — lesson_id 39. 5 dạng (quét: ket-qua/39.quet-dang.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-39.py   (idempotent) → 39.json (review.checked=false cho tới khi kiểm chéo).
Quy ước theo lý thuyết bài 20: V_M = W_M/q · W = qV · U_MN = V_M − V_N = A_MN/q · A_MN = qU_MN · 1 eV = 1,6·10⁻¹⁹ J ·
điện trường đều A_MN = qEd, U = Ed, d = hình chiếu có dấu lên chiều đường sức · mốc ở vô cực: Q>0 → V>0.
  1 công lực điện – thế năng · 2 điện thế, thế năng, đổi điện tích · 3 U và A = qU (electron/proton, eV) · 4 U = Ed (hình chiếu) · 5 tổng hợp hai bản, đổi mốc."""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "39.json")
TOP_A = "Công của lực điện và thế năng điện"
TOP_B = "Điện thế, hiệu điện thế và liên hệ U = Ed"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
E_CH = 1.6e-19

# ═════════════ TỰ GIẢI LẠI SỐ LIỆU (độc lập với lời giải) ═════════════
def near(a, b, tol=1e-9): return abs(a - b) <= tol * max(1, abs(b))
# Dạng 1
A1 = 2.0e-6 * 3000 * 0.040
assert near(A1, 2.4e-4) and near(-A1, -2.4e-4)
# Dạng 2
VM2 = 3.0e-7 / 2.0e-9; WM2 = -4.0e-9 * VM2; WN2 = -4.0e-9 * 60
assert near(VM2, 150) and near(WM2, -6.0e-7) and near(WN2, -2.4e-7) and VM2 > 0
# Dạng 3
U3 = 45 - 15; Ae = -E_CH * U3; Ap = E_CH * U3
assert near(U3, 30) and near(Ae, -4.8e-18) and near(Ae / E_CH, -30) and near(Ap / E_CH, 30)
# Dạng 4
E4 = 240 / 0.060; MP = math.sqrt(5.0 ** 2 - 4.0 ** 2); U4 = E4 * MP / 100; d4 = 60 / E4 * 100
assert near(E4, 4000) and near(MP, 3.0) and near(U4, 120) and near(d4, 1.5) and 5.0 ** 2 == 3.0 ** 2 + 4.0 ** 2
# Dạng 5
E5 = 150 / 0.050; AM = 5.0 - 1.5
VM5 = 0 - E5 * AM / 100; VB5 = -150; UBM = VB5 - VM5; A5 = -E_CH * UBM; VM5b = E5 * 1.5 / 100
assert near(E5, 3000) and near(AM, 3.5) and near(VM5, -105) and near(UBM, -45) and near(A5 / E_CH, 45) and near(A5, 7.2e-18) and near(VM5b, 45)
assert near(VM5 - VM5b, VB5 - 0)          # đổi mốc: mọi điện thế dịch cùng một lượng = hiệu điện thế hai bản
# 4 cách sai của dạng 5 / 4 / 3 cho kết quả KHÁC đáp án đúng (phương án nhiễu phân biệt được)
assert abs(-E5 * 1.5 / 100) != abs(VM5) and (-E_CH * VM5) / E_CH != 45 and 200 != U4 and 160 != U4

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Công của lực điện và độ giảm thế năng trong điện trường đều", topic=TOP_A,
      problem_html=r"""<p>Một điện tích $q=+2{,}0\ \mu\text{C}$ dịch chuyển trong điện trường đều có cường độ $E=3000\ \text{V/m}$, đường sức nằm ngang hướng sang phải. Điện tích đi từ M đến N theo một đường cong bất kì. Hình chiếu của đoạn MN lên đường sức dài $4{,}0\ \text{cm}$, N lệch theo chiều đường sức so với M.</p><ol type="a"><li>Tính công $A_{MN}$ của lực điện.</li><li>Thế năng điện của $q$ tăng hay giảm, và một lượng bằng bao nhiêu?</li><li>Điện tích đi ngược về từ N đến M theo một đường thẳng. Tính công $A_{NM}$ của lực điện.</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Điện thế của một điểm, đổi điện tích đặt vào, thế năng", topic=TOP_B,
      problem_html=r"""<p>Quanh một quả cầu tích điện, chọn mốc điện thế ở vô cực. Điện tích thử $q_1=+2{,}0\ \text{nC}$ đặt tại điểm M có thế năng điện $3{,}0\cdot10^{-7}\ \text{J}$. Điện thế tại điểm N là $60\ \text{V}$.</p><ol type="a"><li>Tính điện thế $V_M$ tại M.</li><li>Quả cầu tích điện dương hay âm?</li><li>Bỏ $q_1$, đặt điện tích $q_2=-4{,}0\ \text{nC}$ vào M. Tính thế năng của $q_2$ tại M.</li><li>Tính thế năng của $q_2$ khi đặt tại N.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Hiệu điện thế và công A = qU với electron, proton; đơn vị eV", topic=TOP_B,
      problem_html=r"""<p>Trong một điện trường tĩnh, chọn mốc điện thế ở Trái Đất. Điện thế tại điểm A là $+45\ \text{V}$ và tại điểm B là $+15\ \text{V}$. Lấy $e=1{,}6\cdot10^{-19}\ \text{C}$, $1\ \text{eV}=1{,}6\cdot10^{-19}\ \text{J}$.</p><ol type="a"><li>Tính hiệu điện thế $U_{AB}$.</li><li>Một electron đi từ A đến B. Tính công của lực điện, theo J và theo eV.</li><li>Một proton cũng đi từ A đến B. Tính công của lực điện, theo eV.</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Liên hệ U = Ed: hình chiếu dọc đường sức và bài ngược", topic=TOP_B,
      problem_html=r"""<p>Hai bản kim loại phẳng song song cách nhau $6{,}0\ \text{cm}$, hiệu điện thế giữa hai bản là $240\ \text{V}$. Coi điện trường giữa hai bản là đều, đường sức vuông góc với các bản. Ba điểm M, N, P nằm giữa hai bản: MP song song với đường sức và cùng chiều đường sức khi đi từ M đến P; tam giác MNP vuông tại P, $MN=5{,}0\ \text{cm}$, $NP=4{,}0\ \text{cm}$.</p><ol type="a"><li>Tính cường độ điện trường giữa hai bản.</li><li>Tính hiệu điện thế $U_{MN}$.</li><li>Tìm khoảng cách từ M đến mặt đẳng thế nằm về phía bản âm, sao cho hiệu điện thế giữa M và mặt đó bằng $60\ \text{V}$.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Hai bản song song: điện thế tại một điểm, công lên electron, đổi mốc", topic=TOP_B,
      problem_html=r"""<p>Hai bản kim loại phẳng song song cách nhau $5{,}0\ \text{cm}$, nối với nguồn $150\ \text{V}$: bản A nối cực dương, bản B nối cực âm. Điểm M nằm giữa hai bản, cách bản B một đoạn $1{,}5\ \text{cm}$. Chọn mốc điện thế ở bản A. Lấy $e=1{,}6\cdot10^{-19}\ \text{C}$.</p><ol type="a"><li>Tính cường độ điện trường giữa hai bản.</li><li>Tính điện thế tại M.</li><li>Một electron đi từ bản B đến M. Tính công của lực điện, theo eV và theo J.</li><li>Chọn lại mốc điện thế ở bản B. Điện thế tại M bằng bao nhiêu? Công ở câu c) có thay đổi không?</li></ol>"""),
]

# ═════════════ HÌNH ═════════════
GREY = "#94a3b8"

def rect(x, y, w, h, c="currentColor", sw=2, fill="none", op=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{c}" stroke-width="{sw}" opacity="{op}"/>'

def efield(x0, x1, ys, op=.6):
    return f'<g opacity="{op}">' + "".join(field_line(x0, y, x1, y, "currentColor", 1.6, "6 4", 11) for y in ys) + "</g>"

def chg(x, y, sign, c, r=8):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" fill-opacity=".3" stroke="{c}" stroke-width="2"/>'
            f'<text x="{x:.1f}" y="{y + 4.5:.1f}" fill="currentColor" font-size="13" font-weight="700" text-anchor="middle">{sign}</text>')

def mover(pts, sign, c, dur, r=8):
    n = len(pts); d = dur
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="{r}" fill="{c}" fill-opacity=".3" stroke="{c}" stroke-width="2">'
            f'{smil("cx", xs, d)}{smil("cy", ys, d)}</circle>'
            f'<text x="{xs[0]:.1f}" y="{ys[0] + 4.5:.1f}" fill="currentColor" font-size="13" font-weight="700" text-anchor="middle">{sign}'
            f'{smil("x", xs, d)}{smil("y", [y + 4.5 for y in ys], d)}</text>')

def straight(a, b, n=40):
    return [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]

def pt(x, y, c="currentColor", r=4.5): return dot(x, y, r, c)

def subq(x, y, base, s, rest, c="currentColor", size=13, anchor="start"):
    """Nhãn dạng V_M = ? : chỉ số dưới rồi quay lại đường cơ sở cho phần chữ sau."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{s}</tspan><tspan dy="-4">{rest}</tspan></text>')


# ───────────── Dạng 1 ─────────────
M1, N1 = (70, 150), (290, 100)
def d1(kk):
    p = f"d1{kk}"
    path = cubic(M1, (130, 40), (200, 215), N1, 48)
    b = efield(16, 404, [30, 75, 120, 165])
    b += lbl(16, 17, "Điện trường đều", "currentColor", 12, "start", "400")
    b += poly(path, GRN, 2, "4 4", .8)
    b += seg(M1[0], M1[1] + 8, M1[0], 214, GREY, 1.4, "3 3") + seg(N1[0], N1[1] + 8, N1[0], 214, GREY, 1.4, "3 3")
    b += dim(p, "o", M1[0], 214, N1[0], 214, "d = 4,0 cm", 180, 207, "middle")
    b += pt(*M1) + lbl(M1[0] - 22, M1[1] + 22, "M") + pt(*N1) + lbl(N1[0] + 10, N1[1] - 8, "N")
    b += lbl(316, 143, "E = 3000 V/m", "currentColor", 13, "start", "700") + lbl(316, 159, "q = +2,0 μC", RED, 13, "start", "700")
    b += subq(316, 106, "A", "MN", " = ?", ORG, 13)
    if kk == 0:
        b += mover(path, "+", RED, 5.5)
        return fig("d1-0", "0 0 420 222", "Điện tích dương đi từ M đến N theo một đường cong trong điện trường đều", b,
                   "Mô phỏng: điện tích dương dịch chuyển từ M đến N theo một đường cong minh hoạ; tốc độ chỉ để minh hoạ. " + NOTE)
    b += chg(M1[0], M1[1], "+", RED)
    return fig("d1-2", "0 0 420 222", "Điện tích dương, điện trường đều, hình chiếu của MN lên đường sức và đại lượng cần tìm", b,
               "Dữ kiện: E, q và hình chiếu d đã cho; đường cong chỉ là một trong vô số đường đi. " + NOTE)


# ───────────── Dạng 2 ─────────────
C2 = (115, 120)
def d2(kk):
    p = f"d2{kk}"
    rM, rN = 44, 98
    aM, aN = math.radians(-38), math.radians(18)
    M = (C2[0] + rM * math.cos(aM), C2[1] + rM * math.sin(aM)); N = (C2[0] + rN * math.cos(aN), C2[1] + rN * math.sin(aN))
    b = f'<circle cx="{C2[0]}" cy="{C2[1]}" r="{rM}" fill="none" stroke="{GREY}" stroke-width="1.6" stroke-dasharray="5 4"/>'
    b += f'<circle cx="{C2[0]}" cy="{C2[1]}" r="{rN}" fill="none" stroke="{GREY}" stroke-width="1.6" stroke-dasharray="5 4"/>'
    b += f'<circle cx="{C2[0]}" cy="{C2[1]}" r="17" fill="currentColor" fill-opacity=".12" stroke="currentColor" stroke-width="2.2"/>' + lbl(C2[0], C2[1] + 5, "Q", "currentColor", 14, "middle", "700")
    b += pt(*M) + lbl(M[0] + 9, M[1] - 8, "M") + pt(*N) + lbl(N[0] + 9, N[1] + 16, "N")
    b += subq(M[0] - 4, M[1] - 22, "V", "M", " = ?", ORG, 13, "end")
    b += subq(N[0] - 2, N[1] + 32, "V", "N", " = 60 V", "currentColor", 13, "end")
    b += lbl(250, 40, "Mốc: V = 0 ở vô cực", "currentColor", 13, "start", "400")
    b += lbl(250, 70, "q₁ = +2,0 nC", RED, 13, "start", "700") + lbl(250, 90, "đặt tại M", "currentColor", 13, "start", "400") + lbl(250, 110, "thế năng 3,0·10⁻⁷ J", "currentColor", 13, "start", "400")
    b += lbl(250, 140, "q₂ = −4,0 nC", BLUE, 13, "start", "700") + lbl(250, 160, "thay q₁ tại M", "currentColor", 13, "start", "400")
    if kk == 0:
        T = 6.0
        b += (f'<g opacity="1">{chg(M[0] + 0, M[1] - 0, "+", RED)}'
              f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.4;0.5;1" dur="{T}s" begin="indefinite" fill="freeze"/></g>')
        b += (f'<g opacity="0">{chg(M[0], M[1], "−", BLUE)}'
              f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.5;0.6;1" dur="{T}s" begin="indefinite" fill="freeze"/></g>')
        return fig("d2-0", "0 0 420 228", "Điện tích q1 tại M được thay bằng điện tích q2, điện thế tại M chưa biết", b,
                   "Mô phỏng: q₁ đặt tại M rồi được thay bằng q₂; vòng nét đứt là mặt đẳng thế qua M và qua N. Chạy trong 6 s, không đúng tỉ lệ. ")
    b += chg(M[0], M[1], "+", RED)
    return fig("d2-2", "0 0 420 228", "Quả cầu tích điện, mặt đẳng thế qua M và N, các dữ kiện và đại lượng cần tìm", b,
               "Dữ kiện: mốc ở vô cực, q₁ tại M và điện thế tại N; quả cầu chưa ghi dấu điện tích. " + NOTE)


# ───────────── Dạng 3 ─────────────
A3, B3 = (90, 100), (330, 100)
def d3(kk):
    p = f"d3{kk}"
    b = seg(A3[0], 36, A3[0], 172, GREY, 1.6, "5 4") + seg(B3[0], 36, B3[0], 172, GREY, 1.6, "5 4")
    b += subq(A3[0], 24, "V", "A", " = +45 V", "currentColor", 13, "middle")
    b += subq(B3[0], 24, "V", "B", " = +15 V", "currentColor", 13, "middle")
    b += pt(*A3) + lbl(A3[0] - 22, A3[1] + 20, "A") + pt(*B3) + lbl(B3[0] + 10, B3[1] + 20, "B")
    b += arrow(p, "o", A3[0], 150, B3[0], 150, 2) + arrow(p, "o", B3[0], 150, A3[0], 150, 2) + subq(210, 142, "U", "AB", " = ?", ORG, 13, "middle")
    b += lbl(16, 196, "Mốc điện thế: Trái Đất (0 V)", "currentColor", 12, "start", "400")
    if kk == 0:
        b += mover(straight((A3[0] + 14, A3[1]), (B3[0] - 20, B3[1]), 40), "−", BLUE, 5.0)
        return fig("d3-0", "0 0 420 206", "Electron đi từ điểm A có điện thế 45 V đến điểm B có điện thế 15 V", b,
                   "Mô phỏng: electron đi từ A đến B; tốc độ trên hình không thể hiện lực điện tăng hay giảm tốc electron. " + NOTE)
    b += chg(A3[0] + 14, A3[1], "−", BLUE)
    b += lbl(210, 70, "electron: q = −e", BLUE, 13, "middle", "700") + lbl(210, 92, "proton: q = +e", RED, 13, "middle", "700")
    return fig("d3-2", "0 0 420 206", "Hai điểm A và B với điện thế đã cho và hiệu điện thế cần tìm", b,
               "Dữ kiện: điện thế tại A, B; electron và proton đều đi từ A đến B. " + NOTE)


# ───────────── Dạng 4 ─────────────
M4, P4, N4 = (130, 100), (200, 100), (200, 185)
def d4(kk):
    p = f"d4{kk}"
    b = rect(28, 24, 10, 190, "currentColor", 2.2, "currentColor", .15) + rect(382, 24, 10, 190, "currentColor", 2.2, "currentColor", .15)
    b += lbl(33, 18, "+", RED, 15, "middle", "700") + lbl(387, 18, "−", BLUE, 15, "middle", "700")
    b += efield(44, 374, [58, 100, 205])
    b += lbl(210, 18, "U = 240 V", "currentColor", 13, "middle", "700")
    b += dim(p, "b", 38, 230, 382, 230, "d = 6,0 cm", 210, 224, "middle")
    b += seg(*M4, *P4, GREY, 1.8, "5 4") + seg(*P4, *N4, GREY, 1.8, "5 4") + seg(*M4, *N4, "currentColor", 2.2)
    b += f'<path d="M190,100 L190,110 L200,110" fill="none" stroke="currentColor" stroke-width="1.4"/>'
    b += pt(*M4) + pt(*P4) + pt(*N4)
    b += lbl(M4[0] - 14, M4[1] - 10, "M") + lbl(P4[0] + 8, P4[1] - 8, "P") + lbl(N4[0] + 10, N4[1] + 16, "N")
    b += lbl(M4[0] - 8, 160, "MN = 5,0 cm", "currentColor", 13, "end", "700") + lbl(N4[0] + 12, 148, "NP = 4,0 cm", "currentColor", 13, "start", "700")
    b += lbl(175, 78, "hình chiếu ?", ORG, 13, "middle", "700")
    if kk == 0:
        T = 5.0; n = 40
        path = straight(M4, N4, n)
        xs = [q[0] for q in path]; ys = [q[1] for q in path]
        b += (f'<line x1="{M4[0]}" y1="{M4[1]}" x2="{M4[0]}" y2="{M4[1]}" stroke="{ORG}" stroke-width="1.6" stroke-dasharray="3 3">'
              f'{smil("x1", xs, T)}{smil("x2", xs, T)}{smil("y1", ys, T)}</line>')
        b += f'<circle cx="{M4[0]}" cy="{M4[1]}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">{smil("cx", xs, T)}</circle>'
        b += f'<circle cx="{M4[0]}" cy="{M4[1]}" r="6.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{smil("cx", xs, T)}{smil("cy", ys, T)}</circle>'
        return fig("d4-0", "0 0 420 240", "Một điểm chạy từ M đến N, bóng của nó trên đường sức chạy từ M đến P", b,
                   "Mô phỏng: chấm xanh chạy từ M đến N, chấm cam là hình chiếu của nó lên đường sức. Tốc độ chỉ để minh hoạ. " + NOTE)
    return fig("d4-2", "0 0 420 240", "Hai bản song song, tam giác MNP vuông tại P với MP dọc đường sức và NP vuông góc đường sức", b,
               "Dữ kiện: hai bản, hiệu điện thế và hai cạnh MN, NP; độ dài MP và hình chiếu cần tìm. " + NOTE)


# ───────────── Dạng 5 ─────────────
M5 = (279, 110)
def d5(kk):
    p = f"d5{kk}"
    b = rect(34, 30, 10, 160, "currentColor", 2.2, "currentColor", .15) + rect(380, 30, 10, 160, "currentColor", 2.2, "currentColor", .15)
    b += lbl(39, 24, "+", RED, 15, "middle", "700") + lbl(385, 24, "−", BLUE, 15, "middle", "700")
    b += lbl(39, 206, "A", "currentColor", 13, "middle", "700") + lbl(385, 206, "B", "currentColor", 13, "middle", "700")
    b += efield(52, 370, [50, 170])
    b += lbl(210, 20, "U = 150 V", "currentColor", 13, "middle", "700")
    b += pt(*M5) + lbl(M5[0] - 18, M5[1] + 24, "M")
    b += subq(M5[0], M5[1] - 14, "V", "M", " = ?", ORG, 13, "middle")
    b += dim(p, "b", M5[0], 140, 380, 140, "1,5 cm", 330, 134, "middle")
    b += dim(p, "g", 44, 218, 380, 218, "d = 5,0 cm", 212, 212, "middle")
    b += lbl(16, 242, "Mốc V = 0 ở bản A", "currentColor", 12, "start", "400")
    if kk == 0:
        b += mover(straight((366, M5[1]), (M5[0] + 18, M5[1]), 40), "−", BLUE, 4.5)
        return fig("d5-0", "0 0 420 250", "Electron đi từ bản âm B đến điểm M giữa hai bản", b,
                   "Mô phỏng: electron đi từ bản B đến M; tốc độ trên hình không thể hiện lực điện tăng hay giảm tốc electron. " + NOTE)
    return fig("d5-2", "0 0 420 250", "Hai bản song song nối nguồn 150 V, điểm M cách bản B 1,5 cm, mốc điện thế ở bản A", b,
               "Dữ kiện: hiệu điện thế, khoảng cách hai bản, vị trí M tính từ bản B, mốc ở bản A. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (⚠ chỉ nêu điều kiện; cột 3 không ghi kết luận) ═════════════
ANALYSIS = [
 [(r'"điện trường đều có cường độ $E=3000$ V/m"', r"$E=3000$ V/m", r"⚠ Công thức công cho điện trường đều chỉ dùng khi điện trường đều trên cả đường điện tích đi qua"),
  (r'"$q=+2{,}0\ \mu\text{C}$"', r"$q=2{,}0\cdot10^{-6}$ C", r"Đổi đơn vị trước khi thế số"),
  (r'"theo một đường cong bất kì"', r"Không cho dạng đường đi", r"Công của lực điện phụ thuộc những yếu tố nào"),
  (r'"hình chiếu của MN lên đường sức dài $4{,}0$ cm"', r"$|d|=4{,}0$ cm", r"Ý nghĩa của $d$ trong công thức công ; đổi cm ra m"),
  (r'"N lệch theo chiều đường sức so với M"', r"Chiều dịch chuyển so với $\vec E$", r"Dấu của $d$"),
  (r'"tính công $A_{MN}$"', r"Cần: $A_{MN}$", r"Công thức công trong điện trường đều"),
  (r'"thế năng tăng hay giảm, bao nhiêu"', r"Cần: biến thiên thế năng", r"Liên hệ giữa công của lực điện và thế năng"),
  (r'"đi ngược về từ N đến M theo đường thẳng"', r"Điểm đầu N, điểm cuối M", r"Đổi điểm đầu và điểm cuối thì đại lượng nào đổi dấu")],
 [(r'"chọn mốc điện thế ở vô cực"', r"$V_\infty=0$", r"⚠ Điện thế của một điểm luôn đo so với mốc đã chọn"),
  (r'"$q_1=+2{,}0$ nC đặt tại M … thế năng $3{,}0\cdot10^{-7}$ J"', r"$q_1=2{,}0\cdot10^{-9}$ C ; $W_M=3{,}0\cdot10^{-7}$ J", r"Định nghĩa điện thế ; đổi nC ra C"),
  (r'"tính điện thế $V_M$"', r"Cần: $V_M$", r"Liên hệ điện thế với thế năng và điện tích thử"),
  (r'"quả cầu tích điện dương hay âm"', r"Cần: dấu của $Q$", r"Dấu của điện thế khi mốc ở vô cực"),
  (r'"đặt $q_2=-4{,}0$ nC vào M"', r"$q_2=-4{,}0\cdot10^{-9}$ C", r"Điện thế của M có phụ thuộc điện tích đặt vào không"),
  (r'"thế năng của $q_2$ tại M"', r"Cần: $W$ của $q_2$ tại M", r"Liên hệ giữa thế năng, điện tích và điện thế"),
  (r'"điện thế tại điểm N là $60$ V"', r"$V_N=60$ V", r"Điện thế đã cho riêng cho N"),
  (r'"thế năng của $q_2$ khi đặt tại N"', r"Cần: $W$ của $q_2$ tại N", r"Liên hệ giữa thế năng, điện tích và điện thế")],
 [(r'"chọn mốc điện thế ở Trái Đất"', r"$V_{\text{đất}}=0$", r"⚠ Hiệu điện thế không phụ thuộc mốc ; điện thế thì có"),
  (r'"điện thế tại A là $+45$ V, tại B là $+15$ V"', r"$V_A=45$ V ; $V_B=15$ V", r"Định nghĩa hiệu điện thế giữa hai điểm"),
  (r'"tính hiệu điện thế $U_{AB}$"', r"Cần: $U_{AB}$", r"Thứ tự hai điểm trong kí hiệu $U_{AB}$"),
  (r'"một electron đi từ A đến B"', r"$q=-e=-1{,}6\cdot10^{-19}$ C ; đầu A, cuối B", r"Công của lực điện và hiệu điện thế ; dấu của $q$"),
  (r'"theo J và theo eV"', r"$1\ \text{eV}=1{,}6\cdot10^{-19}$ J", r"Đổi đơn vị năng lượng"),
  (r'"một proton cũng đi từ A đến B"', r"$q=+e$ ; cùng điểm đầu, điểm cuối", r"Dấu của $q$ ảnh hưởng thế nào đến công")],
 [(r'"cách nhau $6{,}0$ cm, hiệu điện thế $240$ V"', r"$d=6{,}0$ cm ; $U=240$ V", r"⚠ Hệ thức giữa $E$ và $U$ chỉ dùng trong điện trường đều, $d$ đo dọc đường sức ; đổi cm ra m"),
  (r'"coi điện trường giữa hai bản là đều … tính cường độ điện trường"', r"Điện trường đều ; cần: $E$", r"Hệ thức giữa cường độ điện trường và hiệu điện thế"),
  (r'"MP song song và cùng chiều đường sức"', r"MP dọc đường sức, từ M đến P", r"Đoạn dọc đường sức dùng làm $d$"),
  (r'"tam giác MNP vuông tại P, $MN=5{,}0$ cm, $NP=4{,}0$ cm"', r"$MN=5{,}0$ cm ; $NP=4{,}0$ cm ; NP vuông góc MP", r"Quan hệ giữa các cạnh tam giác vuông ; NP nằm vuông góc với đường sức"),
  (r'"tính hiệu điện thế $U_{MN}$"', r"Cần: $U_{MN}$", r"Cách chọn $d$ khi MN xiên so với đường sức"),
  (r'"cách M … hiệu điện thế giữa M và mặt đó bằng $60$ V"', r"$U=60$ V ; cần: khoảng cách", r"Đặt ẩn là $d$ trong hệ thức giữa $E$ và $U$")],
 [(r'"cách nhau $5{,}0$ cm, nối với nguồn $150$ V"', r"$d=5{,}0$ cm ; $U=150$ V", r"⚠ Điện thế của mỗi điểm tính từ đúng bản được chọn làm mốc ; đổi cm ra m"),
  (r'"bản A nối cực dương, bản B nối cực âm"', r"Chiều đường sức: từ A sang B", r"Điện thế thay đổi thế nào dọc theo đường sức"),
  (r'"M cách bản B một đoạn $1{,}5$ cm"', r"$BM=1{,}5$ cm", r"Khoảng cách từ M đến bản mốc là bao nhiêu"),
  (r'"chọn mốc điện thế ở bản A"', r"$V_A=0$", r"Điện thế tại điểm bất kì so với mốc"),
  (r'"tính cường độ điện trường … điện thế tại M"', r"Cần: $E$ ; $V_M$", r"Hệ thức giữa $E$ và $U$ ; điện thế tại điểm từ khoảng cách tới mốc"),
  (r'"electron đi từ bản B đến M"', r"$q=-e$ ; đầu B, cuối M", r"Công của lực điện và hiệu điện thế ; đổi eV ra J"),
  (r'"chọn lại mốc ở bản B"', r"$V_B=0$", r"Mốc đổi thì đại lượng nào đổi, đại lượng nào giữ nguyên")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> công của lực điện không phụ thuộc đường đi, chỉ phụ thuộc điểm đầu và điểm cuối.",
      r"<strong>Công thức:</strong> điện trường đều $A_{MN}=qEd$, $d$ là hình chiếu có dấu của MN lên chiều đường sức.",
      r"<strong>Công thức:</strong> $A_{MN}=W_M-W_N$ (công bằng độ giảm thế năng).",
      r"⚠ <strong>Điều kiện:</strong> $d \gt 0$ khi N lệch theo chiều đường sức so với M ; đổi $\mu\text{C}$, cm ra C, m."]
R2 = [r"<strong>Khái niệm:</strong> điện thế $V_M=\dfrac{W_M}{q}$ là đại lượng của điểm, không phụ thuộc điện tích đặt vào.",
      r"<strong>Công thức:</strong> $W=qV$ (thế năng đổi theo $q$) ; $1\ \text{V}=1\ \text{J/C}$.",
      r"Mốc ở vô cực : $Q \gt 0$ cho $V \gt 0$, $Q \lt 0$ cho $V \lt 0$.",
      r"⚠ <strong>Điều kiện:</strong> giữ dấu của $q$ khi thế số ; đổi nC ra C."]
R3 = [r"<strong>Khái niệm:</strong> hiệu điện thế $U_{AB}=V_A-V_B=\dfrac{A_{AB}}{q}$ ; đổi thứ tự hai điểm thì đổi dấu.",
      r"<strong>Công thức:</strong> $A_{AB}=qU_{AB}$ ; $1\ \text{eV}=1{,}6\cdot10^{-19}$ J.",
      r"Electron $q=-e$ ; proton $q=+e$.",
      r"⚠ <strong>Điều kiện:</strong> giữ đủ dấu của $q$ và của $U$ ; điểm đầu viết trước trong $U_{AB}$."]
R4 = [r"<strong>Khái niệm:</strong> điện trường đều giữa hai bản ; điện thế giảm theo chiều đường sức ; đoạn vuông góc đường sức cùng điện thế.",
      r"<strong>Công thức:</strong> $E=\dfrac{U}{d}$ ; $U_{MN}=Ed_{MN}$, $d_{MN}$ là hình chiếu có dấu của MN lên đường sức.",
      r"⚠ <strong>Điều kiện:</strong> $d$ đo dọc đường sức, không đo theo đoạn xiên ; đổi cm ra m."]
R5 = [r"<strong>Khái niệm:</strong> điện thế đo so với mốc ; điện thế giảm theo chiều đường sức ; đổi mốc thì mọi $V$ đổi, $U$ giữ nguyên.",
      r"<strong>Công thức:</strong> $E=\dfrac{U}{d}$ ; $U_{MN}=V_M-V_N$ ; $A_{MN}=qU_{MN}$.",
      r"Electron $q=-e$ ; $1\ \text{eV}=1{,}6\cdot10^{-19}$ J.",
      r"⚠ <strong>Điều kiện:</strong> khoảng cách tính từ điểm đến đúng bản làm mốc ; điểm đầu viết trước trong $U$."]

SOLS = [
 sol(R1, [
  ("Chọn d cho đường đi cong",
   [P(r"Công không phụ thuộc đường đi nên bỏ qua đường cong ; chỉ lấy hình chiếu của MN lên đường sức."),
    M(r"d=+4{,}0\ \text{cm}=+0{,}040\ \text{m}"),
    P(r"N lệch theo chiều đường sức nên $d \gt 0$. Đổi điện tích:"),
    M(r"q=2{,}0\ \mu\text{C}=2{,}0\cdot10^{-6}\ \text{C}")]),
  ("Công A_MN",
   [P("Điện trường đều:"), M(r"A_{MN}=qEd"), M(r"A_{MN}=2{,}0\cdot10^{-6}\cdot3000\cdot0{,}040"), A(r"A_{MN}=2{,}4\cdot10^{-4}\ \text{J}")]),
  ("Biến thiên thế năng",
   [P("Công bằng độ giảm thế năng:"), M(r"W_M-W_N=A_{MN}=2{,}4\cdot10^{-4}\ \text{J}"),
    A(r"T:Thế năng <strong>giảm</strong> một lượng $2{,}4\cdot10^{-4}\ \text{J}$.")]),
  ("Đi ngược lại từ N về M",
   [P("Đổi điểm đầu và điểm cuối thì $d$ đổi dấu ; đường đi thẳng hay cong không ảnh hưởng:"),
    M(r"d_{NM}=-0{,}040\ \text{m}"), M(r"A_{NM}=qEd_{NM}=2{,}0\cdot10^{-6}\cdot3000\cdot(-0{,}040)"), A(r"A_{NM}=-2{,}4\cdot10^{-4}\ \text{J}")]),
  ("Kiểm tra",
   [P(r"Đơn vị: $\text{C}\cdot\text{V/m}\cdot\text{m}=\text{C}\cdot\text{V}=\text{J}$ ✓."),
    P(r"Điện tích dương đi theo chiều $\vec E$, lực điện cùng chiều dịch chuyển nên $A_{MN} \gt 0$ ✓."),
    P(r"$A_{MN}+A_{NM}=0$ ✓ : đi một vòng kín thì công bằng $0$.")])],
  [r"a) $A_{MN}=2{,}4\cdot10^{-4}\ \text{J}$", r"b) Thế năng giảm $2{,}4\cdot10^{-4}\ \text{J}$", r"c) $A_{NM}=-2{,}4\cdot10^{-4}\ \text{J}$"],
  r"Nhận dạng: đề cho <strong>điện trường đều</strong> và <strong>hình chiếu dọc đường sức</strong> → $A=qEd$ với $d$ có dấu, rồi $A_{MN}=W_M-W_N$."),
 sol(R2, [
  ("Điện thế tại M",
   [P("Thế năng của điện tích thử chia cho điện tích đó:"), M(r"V_M=\dfrac{W_M}{q_1}=\dfrac{3{,}0\cdot10^{-7}}{2{,}0\cdot10^{-9}}"), A(r"V_M=150\ \text{V}")]),
  ("Dấu của điện tích quả cầu",
   [P(r"Mốc ở vô cực và $V_M \gt 0$ nên điện tích nguồn dương."), A(r"T:Quả cầu tích điện <strong>dương</strong>.")]),
  ("Thế năng của q₂ tại M",
   [P(r"Điện thế của M không phụ thuộc điện tích đặt vào, nên vẫn $V_M=150\ \text{V}$."),
    M(r"W_M'=q_2V_M=(-4{,}0\cdot10^{-9})\cdot150"), A(r"W_M'=-6{,}0\cdot10^{-7}\ \text{J}")]),
  ("Thế năng của q₂ tại N",
   [P("Dùng điện thế của chính điểm N:"), M(r"W_N'=q_2V_N=(-4{,}0\cdot10^{-9})\cdot60"), A(r"W_N'=-2{,}4\cdot10^{-7}\ \text{J}")]),
  ("Kiểm tra",
   [P(r"Đơn vị: $\text{C}\cdot\text{V}=\text{J}$ ✓."),
    P(r"$q_2 \lt 0$, $V \gt 0$ nên thế năng âm ✓."),
    P(r"$V_N \lt V_M$ nên $|W_N'| \lt |W_M'|$ ✓.")])],
  [r"a) $V_M=150\ \text{V}$", r"b) Quả cầu tích điện dương", r"c) $V_M$ vẫn $150\ \text{V}$ ; $W=-6{,}0\cdot10^{-7}\ \text{J}$", r"d) $W=-2{,}4\cdot10^{-7}\ \text{J}$"],
  r"Nhận dạng: đề cho <strong>thế năng của điện tích thử</strong> rồi <strong>đổi điện tích khác</strong> → $V=\dfrac{W}{q}$ trước, giữ nguyên $V$, rồi $W=qV$."),
 sol(R3, [
  ("Hiệu điện thế U_AB",
   [P("Điện thế điểm đầu trừ điện thế điểm cuối:"), M(r"U_{AB}=V_A-V_B=45-15"), A(r"U_{AB}=30\ \text{V}")]),
  ("Công của lực điện lên electron (J)",
   [P(r"Electron có $q=-e$ ; giữ cả dấu của $q$:"), M(r"A_{AB}=qU_{AB}=(-1{,}6\cdot10^{-19})\cdot30"), A(r"A_{AB}=-4{,}8\cdot10^{-18}\ \text{J}")]),
  ("Đổi sang eV",
   [P(r"$1\ \text{eV}=1{,}6\cdot10^{-19}\ \text{J}$ nên chia cho hệ số này:"), M(r"A_{AB}=\dfrac{-4{,}8\cdot10^{-18}}{1{,}6\cdot10^{-19}}"), A(r"A_{AB}=-30\ \text{eV}")]),
  ("Công của lực điện lên proton",
   [P(r"Proton có $q=+e$, cùng điểm đầu A và điểm cuối B:"), M(r"A_{AB}=eU_{AB}=(+1)\,e\cdot30\ \text{V}"), A(r"A_{AB}=+30\ \text{eV}")]),
  ("Kiểm tra",
   [P(r"Cùng đường đi A → B, hai công đối nhau vì $q$ đối dấu ✓."),
    P(r"Công của electron theo eV có cùng độ lớn với $U_{AB}$ tính bằng vôn ✓."),
    P(r"Đổi thứ tự điểm cho kết quả ngược dấu ; đề hỏi đi từ A đến B nên dùng $U_{AB}$ ✓.")])],
  [r"a) $U_{AB}=30\ \text{V}$", r"b) $A=-4{,}8\cdot10^{-18}\ \text{J}=-30\ \text{eV}$", r"c) $A=+30\ \text{eV}$"],
  r"Nhận dạng: đề cho <strong>điện thế hai điểm</strong> và <strong>electron hoặc proton đi từ điểm này đến điểm kia</strong> → $U=V_{\text{đầu}}-V_{\text{cuối}}$, rồi $A=qU$ giữ đủ dấu."),
 sol(R4, [
  ("Cường độ điện trường",
   [P("Đổi khoảng cách hai bản ra mét:"), M(r"E=\dfrac{U}{d}=\dfrac{240}{0{,}060}"), A(r"E=4{,}0\cdot10^{3}\ \text{V/m}")]),
  ("Hình chiếu của MN lên đường sức",
   [P(r"NP vuông góc đường sức, MP dọc đường sức. Tam giác MNP vuông tại P:"),
    M(r"MP=\sqrt{MN^2-NP^2}=\sqrt{5{,}0^2-4{,}0^2}"), A(r"d_{MN}=MP=3{,}0\ \text{cm}=0{,}030\ \text{m}")]),
  ("Hiệu điện thế U_MN",
   [P(r"Chỉ phần dọc đường sức góp vào hiệu điện thế:"), M(r"U_{MN}=Ed_{MN}=4{,}0\cdot10^{3}\cdot0{,}030"), A(r"U_{MN}=120\ \text{V}")]),
  ("Khoảng cách ứng với 60 V",
   [P("Rút $d$ từ hệ thức $U=Ed$:"), M(r"d=\dfrac{U}{E}=\dfrac{60}{4{,}0\cdot10^{3}}"), A(r"d=0{,}015\ \text{m}=1{,}5\ \text{cm}")]),
  ("Kiểm tra",
   [P(r"Dùng cả đoạn xiên $MN=5{,}0$ cm sẽ ra $200\ \text{V}$, lớn hơn kết quả vì MN dài hơn hình chiếu ✓."),
    P(r"$U_{MN}=120$ V bằng nửa $240$ V, ứng với $3{,}0$ cm bằng nửa $6{,}0$ cm ✓."),
    P(r"$60$ V bằng nửa $120$ V, ứng với $1{,}5$ cm bằng nửa $3{,}0$ cm ✓.")])],
  [r"a) $E=4{,}0\cdot10^{3}\ \text{V/m}$", r"b) $U_{MN}=120\ \text{V}$", r"c) $d=1{,}5\ \text{cm}$"],
  r"Nhận dạng: đề cho <strong>hai bản song song</strong> hoặc <strong>đoạn xiên so với đường sức</strong> → $E=\dfrac{U}{d}$, rồi $U=Ed$ với $d$ là hình chiếu dọc đường sức."),
 sol(R5, [
  ("Cường độ điện trường",
   [M(r"E=\dfrac{U}{d}=\dfrac{150}{0{,}050}"), A(r"E=3{,}0\cdot10^{3}\ \text{V/m}")]),
  ("Điện thế tại M (mốc ở bản A)",
   [P(r"Đường sức đi từ A sang B, mốc ở A nên điện thế giảm dần từ $0$. Khoảng cách từ M đến bản mốc A:"),
    M(r"AM=5{,}0-1{,}5=3{,}5\ \text{cm}=0{,}035\ \text{m}"),
    M(r"V_M=V_A-E\cdot AM=0-3{,}0\cdot10^{3}\cdot0{,}035"), A(r"V_M=-105\ \text{V}"),
    P(r"Bản B có $V_B=-150\ \text{V}$.")]),
  ("Công của lực điện lên electron (B → M)",
   [P("Điểm đầu là bản B, điểm cuối là M:"), M(r"U_{BM}=V_B-V_M=-150-(-105)=-45\ \text{V}"),
    M(r"A_{BM}=qU_{BM}=(-e)\cdot(-45\ \text{V})"), A(r"A_{BM}=+45\ \text{eV}=45\cdot1{,}6\cdot10^{-19}=7{,}2\cdot10^{-18}\ \text{J}")]),
  ("Điện thế tại M khi mốc ở bản B",
   [P(r"Mốc mới ở B ; M cách B là $0{,}015$ m và nằm về phía có điện thế cao hơn B:"),
    M(r"V_M'=V_B'+E\cdot BM=0+3{,}0\cdot10^{3}\cdot0{,}015"), A(r"V_M'=+45\ \text{V}")]),
  ("Công khi đổi mốc",
   [M(r"U_{BM}=V_B'-V_M'=0-45=-45\ \text{V}"),
    A(r"T:Điện thế đổi theo mốc ; $U_{BM}$ giữ nguyên nên công vẫn là <strong>$+45$ eV</strong>.")]),
  ("Kiểm tra",
   [P(r"$-105\ \text{V}$ nằm giữa $0$ và $-150\ \text{V}$ ✓."),
    P(r"Mốc dời từ A sang B làm mọi điện thế tăng cùng $150\ \text{V}$ : $-105+150=45$ ✓."),
    P(r"Electron đi về phía điện thế cao hơn nên lực điện sinh công dương ✓.")])],
  [r"a) $E=3{,}0\cdot10^{3}\ \text{V/m}$", r"b) $V_M=-105\ \text{V}$", r"c) $A=+45\ \text{eV}=7{,}2\cdot10^{-18}\ \text{J}$", r"d) $V_M=+45\ \text{V}$ ; công không đổi"],
  r"Nhận dạng: đề cho <strong>hai bản song song</strong>, <strong>chọn mốc</strong> hoặc <strong>đổi mốc</strong> → điện thế từ khoảng cách tới bản mốc ; công từ $A=qU$ không phụ thuộc mốc."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>điện trường đều</b> và <b>hình chiếu dọc đường sức</b> → nghĩ tới <b>A = qEd</b>, rồi <b>A = W_M − W_N</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Chọn d cho đường đi cong", r"Đường đi cong thì $d$ trong $A=qEd$ lấy thế nào?",
       loi=r"Đi đo chiều dài đường cong rồi nhân với $E$, trong khi công không phụ thuộc đường đi.",
       lua_chon=[(r"Chiều dài của đường cong từ M đến N", r"Công của lực điện không phụ thuộc hình dạng đường đi nên không cần độ dài đường cong."),
                 (r"Hình chiếu có dấu của MN lên chiều đường sức", True),
                 (r"Độ dài đoạn thẳng nối M với N", r"Chỉ thành phần dọc đường sức mới góp vào công, không phải cả đoạn MN.")]),
  buoc("Công A_MN", r"Công $A_{MN}$ của lực điện theo đơn vị $10^{-4}\ \text{J}$?", 2.4, "×10⁻⁴ J", 0.05,
       loi=r"Quên đổi cm ra m hoặc $\mu\text{C}$ ra C nên kết quả lệch nhiều bậc.",
       ke=[(r"Thế số vào công thức công của điện trường đều với $d$ đã đổi ra mét", True),
           (r"Tìm độ dài đường cong rồi nhân với lực điện", r"Công của lực điện không phụ thuộc đường đi, nên không cần độ dài đường cong."),
           (r"Lấy $q$ nhân $E$ rồi dừng lại", r"Tích $qE$ mới là lực ; muốn có công phải nhân thêm quãng dịch chuyển dọc đường sức.")]),
  buoc("Biến thiên thế năng", r"Thế năng điện của $q$ thay đổi thế nào khi đi từ M đến N?",
       loi=r"Nhầm dấu : tưởng công dương thì thế năng tăng.",
       lua_chon=[(r"Giảm một lượng đúng bằng công $A_{MN}$", True),
                 (r"Tăng một lượng bằng công $A_{MN}$", r"Công dương nghĩa là lực điện sinh công, thế năng phải giảm, giống vật trượt xuống dốc."),
                 (r"Không đổi, vì công không phụ thuộc đường đi", r"Công không phụ thuộc đường đi nhưng vẫn phụ thuộc điểm đầu, điểm cuối ; M và N khác thế năng nên thế năng vẫn đổi.")],
       ke=[(r"Dùng $A_{MN}=W_M-W_N$ rồi xét dấu của công", True),
           (r"Dùng $A_{MN}=W_N-W_M$", r"Công bằng thế năng đầu trừ thế năng cuối, không phải ngược lại."),
           (r"Lấy thế năng tại N bằng $qEd$", r"Thế năng chỉ có nghĩa khi đã chọn mốc ; $qEd$ là công giữa hai điểm, không phải thế năng tại một điểm.")]),
  buoc("Đi ngược lại từ N về M", r"Công $A_{NM}$ theo đơn vị $10^{-4}\ \text{J}$ (kể cả dấu)?", -2.4, "×10⁻⁴ J", 0.05,
       loi=r"Cho rằng đi theo đường thẳng thì công khác, hoặc quên đổi dấu khi đổi chiều đi.",
       ke=[(r"Đổi điểm đầu và điểm cuối rồi xét lại dấu của $d$", True),
           (r"Đường thẳng ngắn hơn đường cong nên công nhỏ hơn", r"Công không phụ thuộc đường đi, chỉ phụ thuộc điểm đầu và điểm cuối."),
           (r"Lực điện vẫn cùng chiều $\vec E$ nên công vẫn dương", r"Lực điện cùng chiều $\vec E$ nhưng lần này dịch chuyển ngược chiều $\vec E$ nên $d \lt 0$ và công mang dấu khác.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>thế năng điện tích thử</b> rồi <b>đổi điện tích</b> → tính <b>V = W/q</b>, giữ V, dùng <b>W = qV</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điện thế tại M", r"Điện thế $V_M$ bằng bao nhiêu vôn?", 150, "V", 1.5,
       loi=r"Nhân $W$ với $q$ thay vì chia, hoặc quên đổi nC ra C nên lệch nhiều bậc."),
  buoc("Dấu của điện tích quả cầu", "Quả cầu tích điện dấu gì?",
       loi=r"Dựa vào dấu của điện tích thử $q_1$ để kết luận dấu của quả cầu.",
       lua_chon=[(r"Dương", True),
                 (r"Âm", r"Mốc ở vô cực thì điện tích nguồn âm cho điện thế âm ; điện thế tìm được ở bước trước mang dấu ngược lại."),
                 (r"Không xác định được", r"Khi mốc ở vô cực, dấu của điện thế so với $0$ cho biết dấu của điện tích nguồn.")],
       ke=[(r"Đối chiếu dấu của $V_M$ với quy tắc về mốc ở vô cực", True),
           (r"Dựa vào dấu của $q_1$", r"$q_1$ chỉ là điện tích thử ; dấu của nó không quyết định dấu điện thế."),
           (r"So độ lớn của $V_M$ với $V_N$", r"Độ lớn không cho biết dấu của $Q$ ; dấu của $V$ so với mốc mới cho biết.")]),
  buoc("Thế năng của q₂ tại M", r"Thế năng của $q_2$ tại M theo đơn vị $10^{-7}\ \text{J}$ (kể cả dấu)?", -6.0, "×10⁻⁷ J", 0.1,
       loi=r"Giữ nguyên thế năng của $q_1$ khi đổi sang $q_2$, hoặc cho rằng điện thế của M đổi dấu theo $q_2$.",
       ke=[(r"Giữ nguyên $V_M$ rồi nhân với $q_2$", True),
           (r"Lấy $V=\dfrac{W}{q_2}$ để tìm điện thế mới", r"$W$ của $q_2$ chưa biết ; điện thế của M không phụ thuộc điện tích đặt vào nên giữ nguyên."),
           (r"Giữ nguyên thế năng của $q_1$ vì M không đổi", r"Thế năng phụ thuộc điện tích đặt vào : $W=qV$ đổi khi $q$ đổi.")]),
  buoc("Thế năng của q₂ tại N", r"Thế năng của $q_2$ tại N theo đơn vị $10^{-7}\ \text{J}$ (kể cả dấu)?", -2.4, "×10⁻⁷ J", 0.05,
       loi=r"Dùng nhầm điện thế của M cho điểm N.",
       ke=[(r"Nhân $q_2$ với điện thế của chính điểm N", True),
           (r"Nhân $q_2$ với điện thế của M", r"N là điểm khác ; điện thế tại N đã cho riêng."),
           (r"Nhân $q_2$ với hiệu hai điện thế M và N", r"Tích đó là công khi đi từ M đến N, không phải thế năng tại N.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>điện thế hai điểm</b> và <b>electron đi từ A đến B</b> → <b>U = V_đầu − V_cuối</b>, rồi <b>A = qU</b> đủ dấu.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Hiệu điện thế U_AB", r"Hiệu điện thế $U_{AB}$ bằng bao nhiêu vôn?", 30, "V", 0.5,
       loi=r"Lấy $V_B-V_A$ (đảo thứ tự), hoặc cộng hai điện thế."),
  buoc("Công của lực điện lên electron (J)", r"Công của lực điện lên electron theo đơn vị $10^{-18}\ \text{J}$ (kể cả dấu)?", -4.8, "×10⁻¹⁸ J", 0.05,
       loi=r"Dùng độ lớn $e$ mà bỏ dấu âm của electron nên công sai dấu.",
       ke=[(r"Dùng $A=qU_{AB}$ với $q=-e$ và giữ cả hai dấu", True),
           (r"Dùng $A=eU_{AB}$ vì chỉ cần độ lớn điện tích", r"Electron mang điện âm ; bỏ dấu của $q$ làm sai dấu của công."),
           (r"Dùng $A=q(V_A+V_B)$", r"Công của lực điện phụ thuộc hiệu hai điện thế, không phải tổng.")]),
  buoc("Đổi sang eV", r"Công đó bằng bao nhiêu eV (kể cả dấu)?", -30, "eV", 0.5,
       loi=r"Nhân thay vì chia cho $1{,}6\cdot10^{-19}$, hoặc giữ nguyên số vì cho rằng J và eV như nhau.",
       ke=[(r"Chia công theo J cho $1{,}6\cdot10^{-19}\ \text{J}$ ứng với mỗi eV", True),
           (r"Nhân công theo J với $1{,}6\cdot10^{-19}$", r"$1\ \text{eV}=1{,}6\cdot10^{-19}$ J, nên từ J sang eV phải chia ; nhân cho số rất nhỏ."),
           (r"Giữ nguyên số vì eV và J cùng là đơn vị năng lượng", r"eV nhỏ hơn J rất nhiều nên con số phải đổi theo.")]),
  buoc("Công của lực điện lên proton", r"Công của lực điện lên proton đi từ A đến B theo eV (kể cả dấu)?", 30, "eV", 0.5,
       loi=r"Lấy lại kết quả của electron mà không đổi dấu theo điện tích.",
       ke=[(r"Lấy $q=+e$ rồi dùng $A=qU_{AB}$ với cùng $U_{AB}$", True),
           (r"Dùng lại kết quả của electron", r"Proton mang điện dương, dấu của $q$ đổi nên dấu của công đổi."),
           (r"Dùng $U_{BA}$ cho proton", r"Đề cho đi từ A đến B nên dùng $U_{AB}$ ; thứ tự phải theo điểm đầu và điểm cuối.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>hai bản song song</b> hoặc <b>đoạn xiên</b> → <b>E = U/d</b>, rồi <b>U = Ed</b> với <b>d dọc đường sức</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Cường độ điện trường", r"Cường độ điện trường giữa hai bản theo đơn vị $10^{3}\ \text{V/m}$?", 4.0, "×10³ V/m", 0.05,
       loi=r"Dùng khoảng cách tính bằng cm trực tiếp nên $E$ lệch $100$ lần."),
  buoc("Hình chiếu của MN lên đường sức", r"Hình chiếu của MN lên phương đường sức dài bao nhiêu cm?", 3.0, "cm", 0.05,
       loi=r"Lấy luôn độ dài MN, hoặc lấy cạnh NP làm hình chiếu.",
       ke=[(r"Lấy cạnh MP song song đường sức, tính từ hai cạnh còn lại của tam giác vuông", True),
           (r"Lấy luôn độ dài MN vì M và N là hai điểm cần xét", r"MN xiên so với đường sức ; chỉ phần dọc đường sức góp vào hiệu điện thế."),
           (r"Lấy cạnh NP", r"NP vuông góc đường sức, nằm trên một mặt đẳng thế nên không góp vào hiệu điện thế.")]),
  buoc("Hiệu điện thế U_MN", r"Hiệu điện thế $U_{MN}$ bằng bao nhiêu vôn?", 120, "V", 1.5,
       loi=r"Nhân $E$ với độ dài MN, hoặc để hình chiếu ở đơn vị cm.",
       ke=[(r"Nhân $E$ với hình chiếu vừa tìm, đã đổi ra mét", True),
           (r"Nhân $E$ với độ dài MN", r"MN là đoạn xiên ; $U=Ed$ chỉ đúng với $d$ đo dọc đường sức."),
           (r"Nhân $E$ với cạnh NP", r"NP vuông góc đường sức nên hiệu điện thế giữa N và P bằng $0$.")]),
  buoc("Khoảng cách ứng với 60 V", r"Khoảng cách từ M đến mặt đẳng thế đó bằng bao nhiêu cm?", 1.5, "cm", 0.05,
       loi=r"Chia ngược $\dfrac{E}{U}$, hoặc cộng $60$ V với hiệu điện thế vừa tìm.",
       ke=[(r"Rút $d$ từ $U=Ed$ với $U=60$ V", True),
           (r"Lấy $d=U\cdot E$", r"Tích $U\cdot E$ có đơn vị $\text{V}^2/\text{m}$, không phải mét."),
           (r"Cộng $60$ V với $U_{MN}$ rồi chia cho $E$", r"$60$ V là hiệu điện thế tính từ M đến mặt cần tìm, không cộng thêm $U_{MN}$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>chọn mốc</b> và <b>đổi mốc</b> → điện thế từ <b>khoảng cách tới bản mốc</b> ; công <b>A = qU</b> không đổi.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Cường độ điện trường", r"Cường độ điện trường giữa hai bản theo đơn vị $10^{3}\ \text{V/m}$?", 3.0, "×10³ V/m", 0.03,
       loi=r"Dùng khoảng cách tính bằng cm trực tiếp nên $E$ lệch $100$ lần."),
  buoc("Điện thế tại M (mốc ở bản A)", r"Điện thế tại M bằng bao nhiêu vôn (kể cả dấu)?", -105, "V", 1.5,
       loi=r"Lấy khoảng cách từ M đến bản B thay vì đến bản mốc A, hoặc quên rằng điện thế giảm dần từ mốc.",
       ke=[(r"Tìm khoảng cách từ M đến bản làm mốc rồi xét điện thế giảm dọc đường sức", True),
           (r"Lấy khoảng cách $1{,}5$ cm từ M đến bản B", r"Mốc ở bản A nên khoảng cách phải tính từ M đến bản A, không phải đến bản B."),
           (r"Lấy $V_M$ bằng hiệu điện thế hai bản", r"Hiệu điện thế hai bản là $U$ ; điện thế tại M chỉ là một phần của nó, tính so với mốc.")]),
  buoc("Công của lực điện lên electron (B → M)", r"Công của lực điện lên electron đi từ B đến M theo eV (kể cả dấu)?", 45, "eV", 0.5,
       loi=r"Dùng $A=qV_M$ thay vì hiệu hai điện thế, hoặc đảo thứ tự hai điểm.",
       ke=[(r"Dùng $A=qU_{BM}$ với điểm đầu là bản B", True),
           (r"Dùng $A=qV_M$ vì M là điểm cuối", r"Công phụ thuộc hiệu hai điện thế ; riêng $V_M$ còn thay đổi theo mốc."),
           (r"Dùng $A=qU_{MB}$", r"Điểm đầu là bản B nên phải viết B trước rồi đến M.")]),
  buoc("Điện thế tại M khi mốc ở bản B", r"Khi mốc ở bản B, điện thế tại M bằng bao nhiêu vôn (kể cả dấu)?", 45, "V", 0.5,
       loi=r"Giữ nguyên điện thế cũ, hoặc chỉ đổi dấu điện thế cũ.",
       ke=[(r"Tính lại từ khoảng cách tới mốc mới và xét M cao hay thấp hơn mốc", True),
           (r"Giữ nguyên $V_M$ vì M không di chuyển", r"Điện thế đo so với mốc nên đổi mốc là đổi giá trị."),
           (r"Chỉ đổi dấu điện thế cũ", r"Đổi mốc không đơn giản là đổi dấu ; giá trị mới tính lại từ khoảng cách tới mốc mới.")]),
  buoc("Công khi đổi mốc", r"Khi đổi mốc sang bản B, công ở câu c) thay đổi thế nào?",
       loi=r"Cho rằng đổi mốc thì công cũng đổi theo điện thế.",
       lua_chon=[(r"Không đổi, vì công phụ thuộc hiệu điện thế giữa hai điểm", True),
                 (r"Đổi theo điện thế mới của M", r"Điện thế đổi theo mốc nhưng hiệu điện thế giữa hai điểm giữ nguyên nên công không đổi."),
                 (r"Đổi dấu, vì điện thế đổi dấu", r"Hiệu điện thế $U_{BM}$ không đổi dấu khi đổi mốc ; công giữ nguyên.")],
       ke=[(r"Tính lại hiệu điện thế giữa hai điểm với mốc mới rồi so sánh", True),
           (r"Thế điện thế mới của M vào $A=qV$", r"Công cần hiệu hai điện thế, không cần điện thế riêng lẻ."),
           (r"Giữ nguyên mọi điện thế cũ", r"Đổi mốc là đổi điện thế các điểm ; phải xét xem hiệu của chúng có đổi không.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 39, "Bài 20. Điện thế", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code) — đã tự giải lại bằng Python 10/10/2026"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
