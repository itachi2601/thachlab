"""Hình cho bài tập mẫu Bài 21 "Moment lực. Cân bằng của vật rắn" (Vật lí 10), lesson_id 66.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.

Mô phỏng TÍNH THẬT bằng phương trình quay  I·θ'' = τ(θ)  (tích phân số, bỏ qua ma sát), KHÔNG thể hiện đáp số:
  d1 cánh cửa mở dưới lực vuông góc · d2 cối xay đá đẩy xiên · d3 bánh lái hai tay (ngẫu lực) ·
  d4 thanh gắn hai khối đặt THỬ trên giá đỡ ở chính giữa (chưa cân bằng, nghiêng về phía A) ·
  d5 thanh bản lề đổ xuống khi KHÔNG còn dây (chỉ cho thấy dây phải giữ thanh).
Khối lượng/mô-men quán tính dùng để mô phỏng KHÔNG nằm trong đề (nói rõ trong chú thích).
Vectơ lực: vec_luc (độ dài = k·F, đầu V 30°). Marker-end = 0."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import vec_luc

GREY = "#94a3b8"


def quay(tau, I, stop, n=40, dt=2e-5):
    """Tích phân I·θ'' = tau(θ) từ nghỉ tới θ = stop (rad). Trả (danh sách n+1 góc cách đều theo THỜI GIAN, tổng thời gian thật)."""
    th = w = t = 0.0
    ts, ths = [0.0], [0.0]
    step = 0
    while th < stop:
        w += tau(th) / I * dt
        th += w * dt
        t += dt
        step += 1
        if step % 20 == 0:
            ts.append(t); ths.append(th)
    ts.append(t); ths.append(stop)
    T = ts[-1]
    out, j = [], 0
    for i in range(n + 1):
        tt = T * i / n
        while j < len(ts) - 2 and ts[j + 1] < tt:
            j += 1
        a, b = ts[j], ts[j + 1]
        f = 0 if b == a else (tt - a) / (b - a)
        out.append(ths[j] + f * (ths[j + 1] - ths[j]))
    out[-1] = stop
    return out, T


def rot(content, ang_deg, cx, cy, dur):
    """Nhóm quay quanh (cx,cy); ang_deg theo quy ước SVG (dương = cùng chiều kim đồng hồ)."""
    vals = ";".join(f"{a:.2f} {cx:.1f} {cy:.1f}" for a in ang_deg)
    return (f'<g><animateTransform attributeName="transform" type="rotate" values="{vals}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>{content}</g>')


def rect(x, y, w, h, c="currentColor", sw=2, fill="none"):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def dashed(x1, y1, x2, y2, c="currentColor", w=1.4, op=0.8):
    return seg(x1, y1, x2, y2, c, w, "5 4", op)


def leg(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, s, c, size, anchor, weight)


# ───────────── Dạng 1 · cánh cửa 0,90 m, F = 20 N vuông góc, d = 0,75 m ─────────────
H1 = (70, 232)
S1 = 250
XP1 = H1[0] + 0.75 * S1
D1_M = 20 * 0.75
D1_I = (1 / 3) * 10 * 0.9 ** 2          # cửa 10 kg chỉ để mô phỏng


def d1(kk):
    door = rect(H1[0], H1[1] - 3, 0.9 * S1, 6, "currentColor", 2.2)
    fa, _ = vec_luc("r", XP1, H1[1], 0, -1, 20, 2.5)
    content = door + dot(XP1, H1[1], 4.5, RED) + fa
    st = dot(H1[0], H1[1], 5.5, "currentColor") + leg(H1[0] - 6, H1[1] - 12, "bản lề", "currentColor", 12, "end", "400")
    st += dim("d1", "g", H1[0], 254, XP1, 254, "d = 0,75 m", XP1 + 8, 258)
    vb = "0 0 420 284"
    if kk == 0:
        ang, T = quay(lambda th: D1_M, D1_I, math.pi / 2)
        b = rot(content, [-math.degrees(a) for a in ang], H1[0], H1[1], 2 * T) + st
        b += leg(318, 50, "F = 20 N", RED) + leg(318, 70, "M = ?", ORG) + leg(318, 92, "cửa rộng 0,90 m", "currentColor", 12, "start", "400")
        return fig("d1-0", vb, "Nhìn từ trên xuống: cánh cửa rộng 0,90 m quay quanh bản lề dưới lực 20 N luôn vuông góc mặt cửa, đặt cách bản lề 0,75 m",
                   b, "Mô phỏng nhìn từ trên xuống, chạy chậm 2 lần: lực luôn vuông góc mặt cửa, bỏ qua ma sát. Cánh cửa 10 kg chỉ dùng để mô phỏng chuyển động, không dùng khi giải. "
                      "Cửa vẽ đúng tỉ lệ chiều dài; mũi tên vẽ theo tỉ lệ độ lớn lực.")
    b = door + dot(XP1, H1[1], 4.5, RED) + fa + st
    x2 = H1[0] + 0.15 * S1
    b += dot(x2, H1[1], 4.5, BLUE) + dim("d1", "b", H1[0], 270, x2, 270, "d′ = 0,15 m", x2 + 8, 274)
    b += leg(318, 50, "F = 20 N", RED) + leg(318, 70, "M = ?", ORG) + leg(318, 90, "F′ = ?  (tại d′)", BLUE)
    return fig("d1-2", vb, "Dữ kiện: lực 20 N vuông góc cửa tại điểm cách bản lề 0,75 m; điểm thứ hai cách bản lề 0,15 m", b,
               "Dữ kiện: điểm xanh dương là chỗ đẩy thứ hai (câu b). Cửa vẽ đúng tỉ lệ chiều dài; mũi tên vẽ theo tỉ lệ độ lớn lực.")


# ───────────── Dạng 2 · cối xay đá: r = 0,30 m, F = 80 N, α = 40° ─────────────
C2 = (120, 135)
S2 = 180
R2 = 0.40 * S2
RP2 = 0.30 * S2
A2 = math.radians(40)
U2 = (math.cos(A2), -math.sin(A2))     # hướng lực trên màn hình (lên phải)
PEG2 = (C2[0] + RP2, C2[1])
D2_M = 80 * 0.30 * math.sin(A2)
D2_I = 0.5 * 25 * 0.40 ** 2           # đá 25 kg chỉ để mô phỏng


def d2(kk):
    fa, _ = vec_luc("r", PEG2[0], PEG2[1], U2[0], U2[1], 80, 0.7)
    grooves = ""
    for a in (100, 215):
        grooves += seg(C2[0], C2[1], C2[0] + R2 * math.cos(math.radians(a)), C2[1] - R2 * math.sin(math.radians(a)), GREY, 1.6)
    disc = circ(C2[0], C2[1], R2, "currentColor", 2.2) + grooves + dashed(C2[0], C2[1], PEG2[0], PEG2[1]) + dot(*PEG2, 5.5, ORG)
    st = dot(*C2, 3.5, "currentColor")
    vb = "0 0 420 262"
    if kk == 0:
        ang, T = quay(lambda th: D2_M, D2_I, 2 * math.pi / 3)
        b = rot(disc + fa, [-math.degrees(a) for a in ang], C2[0], C2[1], 2 * T) + st
        b += leg(250, 70, "F = 80 N", RED) + leg(250, 90, "r = 0,30 m", "currentColor") + leg(250, 110, "α = 40°", RED) + leg(250, 130, "d = ?   M = ?", ORG)
        return fig("d2-0", vb, "Nhìn từ trên xuống: cối xay đá quay quanh tâm khi đẩy vào núm cầm bằng lực 80 N hợp với đường nối núm và tâm góc 40 độ", b,
                   "Mô phỏng nhìn từ trên xuống, chạy chậm 2 lần: người đẩy giữ nguyên lực và góc so với đường nối núm – tâm, bỏ qua ma sát. "
                   "Đá 25 kg chỉ dùng để mô phỏng, không dùng khi giải. Núm cách tâm vẽ đúng tỉ lệ; mũi tên vẽ theo tỉ lệ độ lớn lực.")
    tip = (PEG2[0] + U2[0] * 56, PEG2[1] + U2[1] * 56)
    b = circ(C2[0], C2[1], R2, "currentColor", 2.2) + grooves + dashed(C2[0], C2[1], PEG2[0] + 34, PEG2[1]) + dot(*PEG2, 5.5, ORG) + fa + st
    b += dashed(PEG2[0] - U2[0] * 40, PEG2[1] - U2[1] * 40, tip[0] + U2[0] * 24, tip[1] + U2[1] * 24, RED, 1.2, 0.7)
    b += arc(PEG2[0], PEG2[1], 24, 0, 40, RED) + leg(PEG2[0] + 28, PEG2[1] - 6, "α", RED, 13)
    b += leg(tip[0] + 6, tip[1] - 6, "giá của lực", RED, 11, "start", "400")
    b += leg(250, 160, "F = 80 N", RED) + leg(250, 180, "r = 0,30 m", "currentColor") + leg(250, 200, "α = 40°", RED) + sub(250, 220, "Hỏi: d ; M ; F", "t", ORG, 13)
    return fig("d2-2", vb, "Dữ kiện: núm cách tâm 0,30 m, lực 80 N nằm trên một đường thẳng hợp với đường nối núm – tâm góc 40 độ", b,
               "Dữ kiện: nét đứt đỏ là giá của lực, nét đứt còn lại là đường nối tâm – núm. Núm cách tâm vẽ đúng tỉ lệ; mũi tên vẽ theo tỉ lệ độ lớn lực.")


# ───────────── Dạng 3 · bánh lái: F = 30 N mỗi tay, hai tay cách nhau 0,90 m ─────────────
C3 = (115, 135)
S3 = 200
R3 = 0.45 * S3
D3_M = 30 * 0.90
D3_I = 3.0                              # bánh lái chỉ để mô phỏng


def d3(kk):
    spokes = ""
    for a in range(0, 360, 60):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        col = BLUE if a == 90 else "currentColor"
        spokes += seg(C3[0], C3[1], C3[0] + (R3 + 8) * ca, C3[1] - (R3 + 8) * sa, col, 2.4 if a == 90 else 1.8)
    wheel = circ(C3[0], C3[1], R3, "currentColor", 2.4) + spokes + circ(C3[0], C3[1], 9, "currentColor", 2, "none")
    xr, xl = C3[0] + R3, C3[0] - R3
    fr, _ = vec_luc("r", xr, C3[1], 0, -1, 30, 1.2)
    fl, _ = vec_luc("r", xl, C3[1], 0, 1, 30, 1.2)
    hands = dot(xr, C3[1], 5, RED) + dot(xl, C3[1], 5, RED)
    vb = "0 0 420 262"
    if kk == 0:
        ang, T = quay(lambda th: D3_M, D3_I, math.pi)
        b = rot(wheel + hands + fr + fl, [-math.degrees(a) for a in ang], C3[0], C3[1], 2 * T)
        b += leg(250, 70, "F = 30 N mỗi tay", RED) + leg(250, 90, "hai tay cách nhau 0,90 m", "currentColor", 12, "start", "400")
        b += leg(250, 118, "hợp lực = ?", ORG) + leg(250, 138, "M = ?", ORG)
        return fig("d3-0", vb, "Nhìn thẳng vào bánh lái: hai tay ở hai đầu một đường kính, mỗi tay đẩy một lực 30 N theo phương tiếp tuyến, ngược chiều nhau, bánh lái quay quanh tâm", b,
                   "Mô phỏng chạy chậm 2 lần: hai tay đẩy tiếp tuyến cùng lúc, bánh lái quay tại chỗ quanh tâm, bỏ qua ma sát. "
                   "Bánh lái nặng chỉ dùng để mô phỏng, không dùng khi giải. Bán kính vẽ đúng tỉ lệ; mũi tên vẽ theo tỉ lệ độ lớn lực.")
    b = wheel + hands + fr + fl
    b += dashed(xr, 60, xr, 218, RED, 1.2, 0.7) + dashed(xl, 60, xl, 218, RED, 1.2, 0.7)
    b += dim("d3", "g", xl, 242, xr, 242, "", 0, 0) + leg((xl + xr) / 2, 258, "d = 0,90 m", GRN, 13, "middle")
    b += leg(xl + 8, 160, "F", RED, 13) + leg(xr - 8, 124, "F", RED, 13, "end")
    b += leg(250, 70, "F = 30 N mỗi tay", RED) + leg(250, 90, "d = 0,90 m", GRN) + leg(250, 118, "Hỏi: hợp lực ; M ; F′", ORG)
    return fig("d3-2", vb, "Dữ kiện: hai lực 30 N song song ngược chiều đặt ở hai đầu một đường kính; hai giá cách nhau 0,90 m", b,
               "Dữ kiện: nét đứt đỏ là giá của hai lực, khoảng cách giữa hai giá là 0,90 m. Bán kính vẽ đúng tỉ lệ; mũi tên vẽ theo tỉ lệ độ lớn lực.")


# ───────────── Dạng 4 · thanh 1,0 m, 20 N; khối A 40 N, khối B 20 N ─────────────
S4 = 250
X4A, X4B = 40, 40 + S4
Y4 = 150
O4 = (X4A + S4 / 2, Y4)                # giá đỡ ĐẶT THỬ ở chính giữa (không phải đáp số)
G4 = 9.8
I4 = (20 / G4) / 12 * 1.0 ** 2 + (40 / G4) * 0.5 ** 2 + (20 / G4) * 0.5 ** 2
TAU4 = 40 * 0.5 - 20 * 0.5


def d4(kk):
    vb = "0 0 420 222"
    if kk == 0:
        rod = rect(X4A, Y4 - 4, S4, 8, "currentColor", 2.2) + rect(X4A, Y4 - 28, 24, 24, ORG, 2) + rect(X4B - 18, Y4 - 22, 18, 18, BLUE, 2)
        rod += leg(X4A + 12, Y4 - 34, "A", ORG, 13, "middle") + leg(X4B - 9, Y4 - 28, "B", BLUE, 13, "middle")
        stop = rect(X4A, 187, 40, 8, GREY, 2)
        piv = f'<polygon points="{O4[0]},{Y4 + 4} {O4[0] - 10},{Y4 + 22} {O4[0] + 10},{Y4 + 22}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
        ang, T = quay(lambda th: TAU4 * math.cos(th), I4, math.radians(15))
        b = stop + rot(rod, [-math.degrees(a) for a in ang], O4[0], O4[1], 4 * T) + piv
        b += leg(14, 20, "Khối A: 40 N", ORG) + leg(14, 38, "Khối B: 20 N", BLUE) + leg(14, 56, "Thanh AB: dài 1,0 m, nặng 20 N", "currentColor", 12, "start", "400")
        b += leg(O4[0], 214, "giá đỡ đặt thử ở chính giữa thanh", "currentColor", 12, "middle", "400") + leg(306, 140, "OA = ?", ORG)
        return fig("d4-0", vb, "Thanh có hai khối gắn ở hai đầu, đặt thử trên giá đỡ ở chính giữa thanh; thanh không nằm ngang", b,
                   "Mô phỏng chạy chậm 4 lần: giá đỡ đặt THỬ ở chính giữa (chưa phải vị trí cần tìm), thanh không giữ được nằm ngang, nghiêng rồi tựa vào gối chặn. "
                   "Chiều dài thanh vẽ đúng tỉ lệ; kích thước khối không theo tỉ lệ.")
    y = 100
    b = rect(X4A, y - 4, S4, 8, "currentColor", 2.2) + rect(X4A, y - 28, 24, 24, ORG, 2) + rect(X4B - 18, y - 22, 18, 18, BLUE, 2)
    pts = ((X4A + 12, 40, "o", "P_A"), (O4[0], 20, "o", "P"), (X4B - 9, 20, "o", "P_B"))
    for x, F, c, nm in pts:
        va, tip = vec_luc(c, x, y + 4, 0, 1, F, 1.2)
        b += va
    b += sub(X4A + 12, y + 4 + 48 + 16, "P", "A", ORG, 13, "middle") + lbl(X4A + 12, y + 4 + 48 + 32, "40 N", ORG, 12, "middle", "700")
    b += sub(O4[0], y + 4 + 24 + 16, "P", "", ORG, 13, "middle") + lbl(O4[0], y + 4 + 24 + 32, "20 N (tại G)", ORG, 12, "middle", "700")
    b += sub(X4B - 9, y + 4 + 24 + 16, "P", "B", ORG, 13, "middle") + lbl(X4B - 9, y + 4 + 24 + 32, "20 N", ORG, 12, "middle", "700")
    b += dot(O4[0], y, 3.5, GREY)
    b += dim("d4", "g", X4A, 196, X4B, 196, "AB = 1,0 m", O4[0] - 34, 214)
    b += leg(300, 40, "giá đỡ O:", "currentColor", 12, "start", "400") + leg(300, 58, "chưa biết vị trí", ORG, 12)
    return fig("d4-2", vb, "Dữ kiện: thanh AB dài 1,0 m; trọng lượng 40 N tại A, 20 N tại trọng tâm G và 20 N tại B; vị trí giá đỡ chưa biết", b,
               "Dữ kiện: giá đỡ O đặt ở đâu là điều cần tìm nên không vẽ. Chiều dài thanh vẽ đúng tỉ lệ; mũi tên vẽ theo tỉ lệ độ lớn lực.")



# ───────────── Dạng 5 · thanh bản lề 1,5 m, 40 N, biển 16 N, dây buộc AC = 1,2 m hợp thanh 30° ─────────────
A5 = (40, 130)
S5 = 150
B5 = (A5[0] + 1.5 * S5, A5[1])
C5 = (A5[0] + 1.2 * S5, A5[1])
D5 = (A5[0], A5[1] - 1.2 * math.tan(math.radians(30)) * S5)
I5 = (40 / G4) / 3 * 1.5 ** 2 + (16 / G4) * 1.5 ** 2
TAU5 = 40 * 0.75 + 16 * 1.5


def _wall(y1, y2):
    b = seg(A5[0], y1, A5[0], y2, "currentColor", 3)
    for y in range(int(y1) + 8, int(y2), 14):
        b += seg(A5[0], y, A5[0] - 9, y + 9, "currentColor", 1.4, "", 0.7)
    return b


def d5(kk):
    rod = rect(A5[0], A5[1] - 3, 1.5 * S5, 6, "currentColor", 2.2) + rect(B5[0] - 12, A5[1] + 3, 24, 22, ORG, 2)
    string = seg(C5[0], C5[1], D5[0], D5[1], ORG, 2.4)
    hinge = dot(*A5, 5.5, "currentColor")
    if kk == 0:
        ang, T = quay(lambda th: TAU5 * math.cos(th), I5, math.radians(60))
        dur = 2 * T
        cut = (f'<g>{string}<animate attributeName="opacity" values="1;0;0" keyTimes="0;0.02;1" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b = _wall(10, 340) + cut + rot(rod, [math.degrees(a) for a in ang], A5[0], A5[1], dur) + hinge
        b += leg(292, 30, "Thanh AB: dài 1,5 m", "currentColor", 12, "start", "400") + leg(292, 48, "Thanh nặng 40 N", "currentColor", 12, "start", "400")
        b += leg(292, 66, "Biển hiệu 16 N gắn ở B", "currentColor", 12, "start", "400") + leg(292, 84, "Dây buộc ở C", "currentColor", 12, "start", "400") + leg(292, 102, "AC = 1,2 m", "currentColor", 12, "start", "400")
        return fig("d5-0", "0 0 420 352", "Thanh gắn tường bằng bản lề, đầu B gắn biển hiệu, dây buộc ở C đỡ thanh nằm ngang; khi dây đứt thanh quay xuống quanh bản lề", b,
                   "Mô phỏng chạy chậm 2 lần: NẾU dây đứt thì thanh quay xuống quanh bản lề (bỏ qua ma sát) — cho thấy dây phải giữ thanh. "
                   "Thanh vẽ đúng tỉ lệ chiều dài, biển hiệu vẽ không theo tỉ lệ; khối lượng dùng để mô phỏng suy từ trọng lượng trong đề.")
    b = _wall(10, 240) + rod + string + hinge
    b += arc(C5[0], C5[1], 30, 150, 180, ORG, 1.8) + leg(C5[0] - 40, C5[1] - 22, "30°", ORG, 12, "end")
    va, _ = vec_luc("o", 40 + 0.75 * S5, A5[1] + 3, 0, 1, 40, 1.2)
    vb_, _ = vec_luc("o", B5[0], A5[1] + 14, 0, 1, 16, 1.2)
    b += va + vb_ + dot(40 + 0.75 * S5, A5[1], 3.5, GREY)
    b += sub(40 + 0.75 * S5 + 8, A5[1] + 58, "P", "", ORG, 13) + lbl(40 + 0.75 * S5 + 8, A5[1] + 76, "40 N (tại G)", ORG, 12, "start", "700")
    b += sub(B5[0] + 12, A5[1] + 44, "P", "1", ORG, 13) + lbl(B5[0] + 12, A5[1] + 62, "16 N", ORG, 12, "start", "700")
    b += dim("d5", "g", A5[0], 232, C5[0], 232, "AC = 1,2 m", C5[0] + 8, 236) + dim("d5", "g", A5[0], 252, B5[0], 252, "AB = 1,5 m", B5[0] + 8, 256)
    b += leg(A5[0] + 6, A5[1] - 10, "A", "currentColor", 13) + leg(C5[0] + 6, C5[1] - 8, "C", "currentColor", 13) + leg(B5[0] + 2, A5[1] - 8, "B", "currentColor", 13)
    b += leg(292, 40, "T = ?  (lực căng dây)", RED, 12) + sub(292, 60, "N", "y", RED, 12) + leg(308, 60, "= ?  (bản lề)", RED, 12)
    return fig("d5-2", "0 0 420 266", "Dữ kiện: thanh nằm ngang gắn tường bằng bản lề ở A; dây buộc ở C hợp với thanh góc 30 độ; trọng lượng thanh 40 N, biển hiệu 16 N", b,
               "Dữ kiện: dây là đoạn màu cam, chưa vẽ lực căng và lực bản lề vì đó là đại lượng cần tìm. Thanh, điểm buộc dây và góc 30° vẽ đúng tỉ lệ; mũi tên trọng lực vẽ theo tỉ lệ độ lớn lực.")
