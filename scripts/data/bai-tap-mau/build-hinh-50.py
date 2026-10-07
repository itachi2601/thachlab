"""Bài 50 (Bài 5. Tốc độ và vận tốc, Vật lí 10): 6 dạng bài tập mẫu + tự luận.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-50.py  → ghi scripts/data/bai-tap-mau/50.json"""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

_fig = fig
def fig(*a, **k):
    return re.sub(r'<text[^>]*></text>', '', _fig(*a, **k))

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "50.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."

def ball_c(pts, sec, col, r=6):
    n = len(pts); dur = sec * (n - 1)
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="{r}" fill="{col}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cx", [q[0] for q in pts], dur)}{smil("cy", [q[1] for q in pts], dur)}</circle>')

def tick(x, y, h=7):
    return seg(x, y - h, x, y + h, "currentColor", 1.6)

# ───────────── Dạng 1: chạy thẳng hai pha 4 m/s (4 phút) + 3 m/s (6 phút) ─────────────
def d1(k):
    p = f"d1{k}"; Y = 84; X0 = 40; X2 = 380; sc = (X2 - X0) / 2040; X1 = X0 + 960 * sc
    b = defs(p) + seg(X0, Y, X2, Y, "currentColor", 2.2) + tick(X0, Y) + tick(X1, Y) + tick(X2, Y)
    b += arrow(p, "b", X0, Y - 28, X1 - 2, Y - 28, 3) + lbl((X0 + X1) / 2, Y - 36, "4 m/s · 4 phút", BLUE, 13, "middle", "700")
    b += arrow(p, "o", X1, Y - 28, X2 - 2, Y - 28, 3) + lbl((X1 + X2) / 2, Y - 36, "3 m/s · 6 phút", ORG, 13, "middle", "700")
    b += lbl(X0, Y + 24, "xuất phát", "currentColor", 12, "middle", "400")
    if k == 0:
        pts = []
        for i in range(41):
            t = 15 * i; s = 4 * t if t <= 240 else 960 + 3 * (t - 240)
            pts.append((X0 + s * sc, Y))
        b += lbl(X2, Y + 24, "s = ?   d = ?", ORG, 13, "end", "700")
        b += arrow(p, "g", X0, Y + 44, X0 + 60, Y + 44, 2) + lbl(X0 + 66, Y + 49, "chiều chạy (chiều dương)", GRN, 12, "start", "700")
        b += ball(pts, 0, 15 / 60)
        return fig("d1-0", "0 0 420 150", "Bạn chạy bộ trên đường thẳng 4 phút với 4 m/s rồi 6 phút với 3 m/s", b, "Mô phỏng: chạy nhanh 60 lần (10 phút thật chạy trong 10 s; bấm Chạy mô phỏng). Vị trí tính theo công thức.")
    b += lbl((X0 + X1) / 2, Y + 24, "s₁ = v₁·t₁", BLUE, 12, "middle", "700") + lbl((X1 + X2) / 2, Y + 24, "s₂ = v₂·t₂", ORG, 12, "middle", "700")
    b += lbl(X0, Y + 49, "đi thẳng, không đổi chiều: d = s", GRN, 12, "start", "700")
    b += lbl(X0, Y + 69, "v_tb = tổng s : tổng t", RED, 12, "start", "700")
    return fig("d1-2", "0 0 420 170", "Hai đoạn chạy thẳng nối tiếp, quãng đường mỗi đoạn bằng vận tốc nhân thời gian", b, "Dữ kiện: hai đoạn nối tiếp, cùng chiều. " + NOTE)

# ───────────── Dạng 2: lộ trình nhà–trường gấp khúc ABC (480 m, 360 m) ─────────────
def d2(k):
    p = f"d2{k}"; sc = 0.4; A = (50, 170); B = (50 + 480 * sc, 170); C = (B[0], 170 - 360 * sc)
    b = defs(p) + poly([A, B, C], GRN, 2.4, "" if k else "6 4") + dot(*A, 4.5, "currentColor") + dot(*B, 4, "currentColor") + dot(*C, 4.5, "currentColor")
    b += lbl(A[0] - 6, A[1] + 20, "A (nhà)", "currentColor", 13, "start", "700") + lbl(B[0] + 8, B[1] + 18, "B", "currentColor", 13, "start", "700") + lbl(C[0] + 10, C[1] + 5, "C (trường)", "currentColor", 13, "start", "700")
    b += f'<path d="M{B[0] - 10:.1f},{B[1]:.1f} L{B[0] - 10:.1f},{B[1] - 10:.1f} L{B[0]:.1f},{B[1] - 10:.1f}" fill="none" stroke="currentColor" stroke-width="1.4"/>'
    b += arrow(p, "g", 350, 160, 390, 160, 2) + lbl(396, 164, "Đ", GRN, 12, "start", "700") + arrow(p, "g", 350, 160, 350, 124, 2) + lbl(344, 118, "Bắc", GRN, 12, "start", "700")
    if k == 0:
        b += lbl((A[0] + B[0]) / 2 + 36, 200, "AB = 480 m · 6 phút", BLUE, 13, "middle", "700")
        b += lbl(B[0] + 12, 96, "BC = 360 m", ORG, 13, "start", "700") + lbl(B[0] + 12, 114, "4 phút", ORG, 13, "start", "700")
        b += ball([(A[0] + (B[0] - A[0]) * min(i / 24, 1) if i <= 24 else B[0], A[1] if i <= 24 else B[1] - (B[1] - C[1]) * (i - 24) / 16) for i in range(41)], 0, 15 / 60)
        return fig("d2-0", "0 0 420 214", "Bạn A đi từ nhà A tới B rồi rẽ lên phía bắc tới trường C", b, "Mô phỏng: chạy nhanh 60 lần (10 phút thật chạy trong 10 s). Vị trí tính theo công thức.")
    b += arrow(p, "r", A[0], A[1] - 4, C[0] - 3, C[1] + 4, 2.4, "6 4") + lbl(120, 112, "d = ?", RED, 13, "end", "700")
    b += lbl((A[0] + B[0]) / 2 + 36, 200, "AB = 480 m", BLUE, 13, "middle", "700") + lbl(B[0] + 12, 105, "BC = 360 m", ORG, 13, "start", "700")
    b += lbl(16, 24, "s = AB + BC", GRN, 13, "start", "700") + lbl(16, 44, "d = AC (nối thẳng A → C)", RED, 13, "start", "700")
    return fig("d2-2", "0 0 420 214", "Quãng đường là đường gấp khúc ABC, độ dịch chuyển là mũi tên nối thẳng từ A đến C", b, "Dữ kiện: quãng đường theo đường đi, độ dịch chuyển là đoạn thẳng AC. " + NOTE)

# ───────────── Dạng 3: bể bơi 50 m, đi 20 s, về 25 s ─────────────
def d3(k):
    p = f"d3{k}"; X0, X1, Y0, Y1 = 40, 380, 52, 130; lane = (Y0 + Y1) / 2
    b = defs(p) + f'<rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{Y1 - Y0}" rx="4" fill="none" stroke="currentColor" stroke-width="2"/>'
    b += lbl(X0, 44, "đầu bể", "currentColor", 12, "start", "400") + lbl(X1, 44, "cuối bể", "currentColor", 12, "end", "400")
    b += arrow(p, "g", X0, 18, X0 + 60, 18, 2) + lbl(X0 + 66, 23, "chiều dương", GRN, 12, "start", "700")
    b += dim(p, "b", X0, 150, X1, 150, "50 m", 188, 170)
    if k == 0:
        pts = [(X0 + (X1 - X0) * (2 * i / 40 if i <= 20 else (90 - 2 * i) / 50), lane) for i in range(46)]
        b += lbl(210, lane - 14, "đi: 40 s", BLUE, 13, "middle", "700") + lbl(210, lane + 28, "về: 50 s", ORG, 13, "middle", "700")
        b += ball_c(pts, 2 / 6, GRN)
        return fig("d3-0", "0 0 420 182", "Người bơi đi hết chiều dài bể 50 m trong 40 s rồi bơi về chỗ cũ trong 50 s", b, "Mô phỏng: chạy nhanh 6 lần (90 s thật chạy trong 15 s). Vị trí tính theo công thức.")
    b += arrow(p, "b", X0 + 10, lane - 14, X1 - 10, lane - 14, 3) + lbl(210, lane - 22, "đi: cùng chiều dương → d dương", BLUE, 12, "middle", "700")
    b += arrow(p, "o", X1 - 10, lane + 22, X0 + 10, lane + 22, 3) + lbl(210, lane + 10, "về: ngược chiều dương → d âm", ORG, 12, "middle", "700")
    b += lbl(210, 192, "cả đi lẫn về: trở lại chỗ cũ", RED, 12, "middle", "700")
    return fig("d3-2", "0 0 420 200", "Chiều đi cùng chiều dương nên độ dịch chuyển dương, chiều về ngược chiều dương nên độ dịch chuyển âm", b, "Dữ kiện: dấu của độ dịch chuyển theo chiều dương đã chọn. " + NOTE)

# ───────────── Dạng 4: mô tô đuổi vận động viên (cùng chiều) ─────────────
def d4(k):
    p = f"d4{k}"; Y = 100; sc = 9; xm, xv = 40, 130
    b = defs(p) + ground(Y + 6) + tick(xm, Y + 24, 0) 
    b += seg(xm, Y + 14, xm, Y + 34, "currentColor", 1.4) + seg(xv, Y + 14, xv, Y + 34, "currentColor", 1.4)
    b += seg(xm, Y + 24, xv, Y + 24, "currentColor", 1.8) + lbl((xm + xv) / 2 - 24, Y + 46, "10 km", "currentColor", 13, "start", "700")
    if k == 0:
        b += lbl(16, 24, "● mô tô: 60 km/h so với mặt đường", BLUE, 13, "start", "700") + lbl(16, 44, "● VĐV dẫn đầu: tốc độ ?", GRN, 13, "start", "700")
        b += lbl(232, Y + 46, "mô tô bắt kịp sau 30 phút", "currentColor", 12, "start", "400")
        m = [(xm + sc * 60 * (0.5 * i / 40), Y - 6) for i in range(41)]
        v = [(xv + sc * 40 * (0.5 * i / 40), Y - 6) for i in range(41)]
        b += ball_c(v, 0.25, GRN) + ball_c(m, 0.25, BLUE)
        return fig("d4-0", "0 0 420 170", "Mô tô đuổi theo vận động viên dẫn đầu cách 10 km và bắt kịp sau 30 phút", b, "Mô phỏng: 30 phút thật chạy trong 10 s (nhanh 180 lần). Vị trí đối với mặt đường, tính theo công thức.")
    b += dot(xm, Y - 6, 6, BLUE) + dot(xv, Y - 6, 6, GRN)
    b += arrow(p, "g", xm, Y - 22, xm + 84, Y - 22, 3) + arrow(p, "o", xv, Y - 22, xv + 36, Y - 22, 3, "5 4")
    b += lbl(16, 24, "v₁₃: mô tô so với đường = 60 km/h", GRN, 13, "start", "700") + lbl(16, 44, "v₂₃: VĐV so với đường = ?", ORG, 13, "start", "700") + lbl(16, 64, "v₁₂: mô tô so với VĐV = d : Δt", BLUE, 13, "start", "700")
    b += lbl(232, Y + 46, "mô tô: (1)  VĐV: (2)  đường: (3)", "currentColor", 12, "start", "400")
    return fig("d4-2", "0 0 420 170", "Hai vật cùng chiều trên đường: vận tốc mô tô so với đường, vận tốc vận động viên so với đường và vận tốc mô tô so với vận động viên", b, "Dữ kiện: ba vận tốc cùng chiều. " + NOTE)

# ───────────── Dạng 5: ca nô ngang sông, mũi vuông góc bờ ─────────────
def river(p, xl, xr, yt, yb):
    return seg(xl, yt, xl, yb, "currentColor", 2.4) + seg(xr, yt, xr, yb, "currentColor", 2.4)

def d5(k):
    p = f"d5{k}"; xl, xr = 120, 320; A = (xl, 40); C = (xr, 150)
    b = defs(p) + river(p, xl, xr, 16, 206) + dot(*A, 4.5, "currentColor") + lbl(xl - 8, 36, "A", "currentColor", 13, "end", "700")
    b += lbl(344, 24, "↑ Bắc", "currentColor", 12, "start", "400") + lbl(344, 44, "Đông →", "currentColor", 12, "start", "400")
    if k == 0:
        b += arrow(p, "b", xl, 40, xl + 60, 40, 3) + lbl(xl + 6, 29, "v₁₂ = 4 m/s", BLUE, 13, "start", "700")
        b += lbl(180, 118, "nước chảy", ORG, 12, "middle", "700") + arrow(p, "o", 180, 128, 180, 168, 3) + lbl(180, 188, "v₂₃ = 3 m/s", ORG, 12, "middle", "700")
        b += lbl(330, 130, "trôi = ?", ORG, 13, "start", "700")
        b += dim(p, "g", xl, 220, xr, 220, "rộng 200 m", 170, 238)
        b += ball([(A[0] + (C[0] - A[0]) * i / 40, A[1] + (C[1] - A[1]) * i / 40) for i in range(41)], 0, 0.25)
        return fig("d5-0", "0 0 420 244", "Ca nô xuất phát từ bờ tây, mũi hướng đông vuông góc bờ, nước chảy về phía nam nên ca nô bị trôi xuống", b, "Mô phỏng: chạy nhanh 5 lần (50 s thật chạy trong 10 s). Quỹ đạo tính theo công thức; hình không đúng tỉ lệ.")
    P0 = (60, 50); sx = 30
    E1 = (P0[0] + 4 * sx, P0[1]); E2 = (E1[0], P0[1] + 3 * sx)
    b = defs(p) + arrow(p, "b", *P0, *E1, 3) + arrow(p, "o", *E1, *E2, 3) + arrow(p, "g", *P0, *E2, 3)
    b += f'<path d="M{E1[0] - 10:.1f},{E1[1]:.1f} L{E1[0] - 10:.1f},{E1[1] + 10:.1f} L{E1[0]:.1f},{E1[1] + 10:.1f}" fill="none" stroke="currentColor" stroke-width="1.4"/>'
    b += arc(P0[0], P0[1], 28, -36.87, 0, RED) + lbl(P0[0] + 34, P0[1] + 18, "α = ?", RED, 13, "start", "700")
    b += lbl((P0[0] + E1[0]) / 2, P0[1] - 10, "v₁₂ = 4 m/s", BLUE, 13, "middle", "700") + lbl(E1[0] + 10, (E1[1] + E2[1]) / 2 + 4, "v₂₃ = 3 m/s", ORG, 13, "start", "700")
    b += lbl(P0[0] + 52, E2[1] + 4, "v₁₃ = ?", GRN, 13, "end", "700") + lbl(250, 50, "v₁₂ ⊥ v₂₃", "currentColor", 13, "start", "700")
    b += lbl(250, 150, "độ lớn: Pytago", RED, 13, "start", "700") + lbl(250, 170, "hướng: tanα = v₂₃ / v₁₂", RED, 13, "start", "700")
    return fig("d5-2", "0 0 420 200", "Vận tốc của ca nô so với bờ là tổng của vận tốc so với nước và vận tốc của nước, hai vectơ vuông góc", b, "Dữ kiện: hai vận tốc thành phần vuông góc. " + NOTE)

# ───────────── Dạng 6: hướng mũi để tới đúng điểm đối diện ─────────────
def d6(k):
    p = f"d6{k}"; xl, xr = 100, 340; A = (xl, 60); B = (xr, 60); C = (xr, 140)
    if k == 0:
        b = defs(p) + river(p, xl, xr, 30, 200) + seg(*A, *B, "currentColor", 1.4, "5 4", .6) + dot(*A, 4.5, "currentColor") + dot(*B, 4, "currentColor") + dot(*C, 4.5, "currentColor")
        b += lbl(xl - 8, 56, "A", "currentColor", 13, "end", "700") + lbl(xr + 8, 54, "B", "currentColor", 13, "start", "700") + lbl(xr + 8, 156, "C", "currentColor", 13, "start", "700")
        b += arrow(p, "b", xl, 60, xl + 60, 60, 3) + lbl(xl + 6, 49, "v₁₂ = 4 m/s", BLUE, 13, "start", "700")
        b += lbl(180, 120, "nước chảy", ORG, 12, "middle", "700") + arrow(p, "o", 180, 130, 180, 168, 3) + lbl(180, 188, "v₂₃ = ?", ORG, 12, "middle", "700")
        b += dim(p, "o", 358, 60, 358, 140, "", 0, 0) + lbl(364, 104, "200 m", ORG, 12, "start", "700")
        b += ball([(A[0] + (C[0] - A[0]) * i / 40, A[1] + (C[1] - A[1]) * i / 40) for i in range(41)], 0, 0.25)
        return fig("d6-0", "0 0 420 210", "Lần một: ca nô hướng mũi thẳng tới điểm B đối diện nhưng bị nước cuốn tới C, cách B 200 m", b, "Mô phỏng lần 1: mũi hướng thẳng B, sau 100 s cập bờ ở C (chạy nhanh 10 lần). Quỹ đạo tính theo công thức; hình không đúng tỉ lệ.")
    P0 = (60, 140); sx = 40; a = math.radians(30)
    Pt = (P0[0] + 4 * sx * math.cos(a), P0[1] - 4 * sx * math.sin(a)); E = (Pt[0], P0[1])
    b = defs(p) + arrow(p, "b", *P0, *Pt, 3) + arrow(p, "o", *Pt, *E, 3) + arrow(p, "g", *P0, *E, 3)
    b += f'<path d="M{E[0] - 10:.1f},{E[1]:.1f} L{E[0] - 10:.1f},{E[1] - 10:.1f} L{E[0]:.1f},{E[1] - 10:.1f}" fill="none" stroke="currentColor" stroke-width="1.4"/>'
    b += arc(P0[0], P0[1], 34, 0, 30, RED) + lbl(P0[0] + 40, P0[1] - 6, "α = ?", RED, 13, "start", "700")
    b += lbl(122, 86, "v₁₂ = 4 m/s", BLUE, 13, "end", "700") + lbl(E[0] + 8, 106, "v₂₃ (từ lần 1)", ORG, 13, "start", "700")
    b += lbl((P0[0] + E[0]) / 2, 162, "v₁₃ vuông góc bờ (tới đúng B)", GRN, 12, "middle", "700")
    b += lbl(250, 36, "sinα = v₂₃ / v₁₂", RED, 13, "start", "700") + lbl(250, 56, "v₁₃ = √(v₁₂² − v₂₃²)", RED, 13, "start", "700")
    return fig("d6-2", "0 0 420 176", "Lần hai: mũi ca nô lệch ngược dòng một góc để tổng vận tốc vuông góc với bờ", b, "Dữ kiện: v₁₃ vuông góc bờ thì thành phần dọc bờ của v₁₂ cân bằng với v₂₃. " + NOTE)

BUILD = [d1, d2, d3, d4, d5, d6]

DANG = [
 dict(label="Dạng 1 · Dễ · Tốc độ trung bình khi đi nhiều đoạn nối tiếp", topic="Tốc độ trung bình và vận tốc trung bình",
  problem_html="<p>Một bạn chạy bộ trên đường thẳng, không đổi chiều, trong $10$ phút. Trong $4$ phút đầu bạn chạy với vận tốc $4\\ \\text{m/s}$, thời gian còn lại giảm xuống còn $3\\ \\text{m/s}$.</p><ol type=\"a\"><li>Tính quãng đường chạy được và độ dịch chuyển.</li><li>Tính tốc độ trung bình và vận tốc trung bình cả quãng chạy (ra m/s và km/h).</li><li>Có thể lấy $\\dfrac{4+3}{2}$ làm tốc độ trung bình không? Vì sao?</li></ol>"),
 dict(label="Dạng 2 · Dễ · Quãng đường và độ dịch chuyển trên lộ trình gấp khúc", topic="Phân biệt quãng đường và độ dịch chuyển",
  problem_html="<p>Bạn A đi học từ nhà (A) đến trường (C) theo lộ trình ABC: đoạn $AB=480\\ \\text{m}$ hướng đông, đi hết $6$ phút; đoạn $BC=360\\ \\text{m}$ hướng bắc, đi hết $4$ phút ($AB\\perp BC$).</p><ol type=\"a\"><li>Tính quãng đường và độ lớn độ dịch chuyển của bạn A từ nhà đến trường.</li><li>Tính tốc độ trung bình và vận tốc trung bình (độ lớn, hướng) của bạn A trên cả lộ trình.</li></ol>"),
 dict(label="Dạng 3 · Trung bình · Đi rồi quay lại: dấu của vận tốc, vận tốc trung bình bằng 0", topic="Tốc độ trung bình và vận tốc trung bình",
  problem_html="<p>Một người bơi dọc bể bơi dài $50\\ \\text{m}$. Bơi từ đầu bể đến cuối bể hết $40\\ \\text{s}$, rồi bơi tiếp từ cuối bể quay về đầu bể hết $50\\ \\text{s}$. Chọn chiều dương là chiều từ đầu bể đến cuối bể. Xác định tốc độ trung bình và vận tốc trung bình trong ba trường hợp:</p><ol type=\"a\"><li>Bơi từ đầu bể đến cuối bể.</li><li>Bơi từ cuối bể về đầu bể.</li><li>Bơi cả đi lẫn về.</li></ol>"),
 dict(label="Dạng 4 · Trung bình · Cộng vận tốc cùng chiều: đuổi kịp", topic="Tổng hợp vận tốc, tính tương đối của chuyển động",
  problem_html="<p>Trong một giải đua xe đạp, xe mô tô của đài truyền hình chạy cùng chiều với các vận động viên (VĐV) để ghi hình. Khi mô tô đang quay VĐV cuối cùng thì VĐV dẫn đầu cách mô tô $10\\ \\text{km}$. Mô tô giữ tốc độ $60\\ \\text{km/h}$ so với mặt đường và bắt kịp VĐV dẫn đầu sau $30$ phút. Coi các xe chuyển động thẳng đều.</p><ol type=\"a\"><li>Tính tốc độ của VĐV dẫn đầu so với mặt đường.</li><li>Trong $30$ phút đó, mô tô và VĐV dẫn đầu mỗi bên đi được bao xa so với mặt đường?</li></ol>"),
 dict(label="Dạng 5 · Trung bình · Cộng vận tốc vuông góc: ca nô ngang sông", topic="Tổng hợp vận tốc, tính tương đối của chuyển động",
  problem_html="<p>Một ca nô có tốc độ tối đa $14{,}4\\ \\text{km/h}$ so với nước yên lặng. Ca nô chạy hết tốc độ ngang một khúc sông rộng $200\\ \\text{m}$, mũi luôn hướng thẳng về phía đông, vuông góc với bờ. Nước chảy về phía nam với tốc độ $3\\ \\text{m/s}$ so với bờ.</p><ol type=\"a\"><li>Tính độ lớn và hướng vận tốc của ca nô so với bờ.</li><li>Ca nô qua sông hết bao lâu? Khi cập bờ bên kia, nó cách điểm đối diện chỗ xuất phát bao xa?</li></ol>"),
 dict(label="Dạng 6 · Khó · Chọn hướng mũi để tới đúng điểm đối diện", topic="Tổng hợp vận tốc, tính tương đối của chuyển động",
  problem_html="<p>Ca nô có tốc độ $4\\ \\text{m/s}$ so với nước (giữ nguyên ở mọi lần chạy), xuất phát từ A ở một bờ sông, cần sang điểm B ở bờ đối diện ($AB$ vuông góc với bờ). Lần 1, mũi ca nô hướng thẳng tới B: sau $100\\ \\text{s}$ ca nô cập bờ ở điểm C, cách B $200\\ \\text{m}$ về phía hạ lưu. Lần 2, người lái hướng mũi theo AD lệch về phía thượng lưu, vẫn giữ tốc độ máy như cũ, và cập bờ đúng ở B.</p><ol type=\"a\"><li>Tìm vận tốc của nước so với bờ.</li><li>Tìm chiều rộng của sông.</li><li>Tìm góc giữa AD và AB, và thời gian qua sông ở lần 2.</li></ol>"),
]

DK = "⚠ Đi thẳng, không đổi chiều: $d=s$ và vận tốc trung bình bằng tốc độ trung bình"
ANALYSIS = [
 [("\"chạy bộ trên đường thẳng, không đổi chiều\"", "Chuyển động thẳng, một chiều", DK),
  ("\"$4$ phút đầu … $4\\ \\text{m/s}$\"", "$t_1=4$ phút $=240$ s; $v_1=4$ m/s", "Đoạn đều: $s_1=v_1t_1$"),
  ("\"thời gian còn lại … $3\\ \\text{m/s}$\"", "$t_2=10-4=6$ phút $=360$ s; $v_2=3$ m/s", "$s_2=v_2t_2$"),
  ("\"quãng đường chạy được, độ dịch chuyển\"", "Cần $s$, $d$", "$s=s_1+s_2$; $d=s$"),
  ("\"tốc độ trung bình … vận tốc trung bình cả quãng\"", "$t=10$ phút $=600$ s", "$v_{tb}=\\dfrac{s}{t}$; $v=\\dfrac{d}{t}$ (tổng $s$ chia tổng $t$)"),
  ("\"lấy $\\dfrac{4+3}{2}$ được không?\"", "Hai đoạn khác thời gian", "⚠ Chỉ đúng khi hai đoạn có cùng thời gian")],
 [("\"lộ trình ABC\"", "Đường gấp khúc, đổi hướng ở B", "⚠ Đường không thẳng: $d\\lt s$, vận tốc trung bình khác tốc độ trung bình"),
  ("\"$AB=480\\ \\text{m}$ hướng đông, $6$ phút\"", "$AB=480$ m; $t_1=6$ phút", "Quãng đường đoạn 1"),
  ("\"$BC=360\\ \\text{m}$ hướng bắc, $4$ phút\"", "$BC=360$ m; $t_2=4$ phút; $AB\\perp BC$", "Quãng đường đoạn 2; tam giác $ABC$ vuông tại $B$"),
  ("\"quãng đường\"", "Cần $s$", "$s=AB+BC$"),
  ("\"độ dịch chuyển\"", "Cần $d$", "Mũi tên nối $A\\to C$: $d=AC=\\sqrt{AB^2+BC^2}$"),
  ("\"tốc độ trung bình, vận tốc trung bình (độ lớn, hướng)\"", "$t=6+4=10$ phút $=600$ s", "$v_{tb}=\\dfrac{s}{t}$; $v=\\dfrac{d}{t}$, hướng theo $\\vec d$; $\\tan\\alpha=\\dfrac{BC}{AB}$")],
 [("\"bể bơi dài $50\\ \\text{m}$\"", "Bơi thẳng dọc bể", "Mỗi lượt đi hoặc về: $s=50$ m"),
  ("\"chọn chiều dương từ đầu đến cuối bể\"", "Chiều dương đã chọn", "⚠ $d$ và $v$ mang dấu: cùng chiều dương là $+$, ngược chiều là $-$; $s$ và tốc độ luôn không âm"),
  ("\"đầu → cuối hết $40\\ \\text{s}$\"", "$t_a=40$ s", "Đi một chiều: $d=s$, $v=v_{tb}$"),
  ("\"cuối → đầu hết $50\\ \\text{s}$\"", "$t_b=50$ s", "Đổi chiều: $d$ mang dấu âm; $s$ vẫn dương"),
  ("\"bơi cả đi lẫn về\"", "$t=t_a+t_b$", "$s=s_a+s_b$; về đúng điểm đầu: độ dịch chuyển bằng không"),
  ("\"tốc độ trung bình, vận tốc trung bình\"", "Cần ở cả ba trường hợp", "$v_{tb}=\\dfrac{s}{t}$; $v=\\dfrac{d}{t}$")],
 [("\"mô tô cùng chiều … VĐV\"", "Cùng chiều, thẳng đều", "⚠ Cùng chiều: $v_{13}=v_{12}+v_{23}$"),
  ("đánh số", "(1) mô tô; (2) VĐV; (3) mặt đường", "$\\vec v_{13}=\\vec v_{12}+\\vec v_{23}$ (mẹo \"khử số 2\")"),
  ("\"mô tô giữ $60\\ \\text{km/h}$ so với mặt đường\"", "$v_{13}=60$ km/h", "Vận tốc tuyệt đối của mô tô"),
  ("\"VĐV dẫn đầu cách mô tô $10\\ \\text{km}$\"", "$d=10$ km", "Khoảng cách ban đầu giữa hai xe"),
  ("\"bắt kịp sau $30$ phút\"", "$\\Delta t=30$ phút $=0{,}5$ h", "Trong hệ gắn VĐV, mô tô tiến lại gần với $v_{12}=\\dfrac{d}{\\Delta t}$"),
  ("\"tốc độ của VĐV so với mặt đường\"", "Cần $v_{23}$", "$v_{23}=v_{13}-v_{12}$"),
  ("\"mỗi bên đi được bao xa\"", "Cần $s_1$, $s_2$ so với đường", "$s=v\\cdot\\Delta t$ với vận tốc so với đường")],
 [("\"ca nô … $14{,}4\\ \\text{km/h}$ so với nước yên lặng\"", "$v_{12}=14{,}4$ km/h $=4$ m/s", "Vận tốc tương đối $v_{12}$; đổi km/h → m/s: chia $3{,}6$"),
  ("\"nước chảy về phía nam $3\\ \\text{m/s}$ so với bờ\"", "$v_{23}=3$ m/s", "Vận tốc kéo theo $v_{23}$; (1) ca nô, (2) nước, (3) bờ"),
  ("\"mũi hướng đông, vuông góc với bờ\"", "$\\vec v_{12}\\perp\\vec v_{23}$", "⚠ Vuông góc: $v_{13}=\\sqrt{v_{12}^2+v_{23}^2}$; $\\vec v_{13}=\\vec v_{12}+\\vec v_{23}$"),
  ("\"độ lớn và hướng vận tốc so với bờ\"", "Cần $v_{13}$, $\\alpha$", "$\\tan\\alpha=\\dfrac{v_{23}}{v_{12}}$ (góc so với hướng mũi)"),
  ("\"sông rộng $200\\ \\text{m}$ … hết bao lâu\"", "Rộng $200$ m", "Chỉ $v_{12}$ đưa ca nô sang ngang bờ: $t=\\dfrac{200}{v_{12}}$"),
  ("\"cách điểm đối diện bao xa\"", "Cần độ trôi", "Chỉ $v_{23}$ làm trôi dọc bờ: $x=v_{23}t$")],
 [("\"lần 1: mũi hướng thẳng B … cập bờ ở C, cách B $200\\ \\text{m}$\"", "$t_1=100$ s; $BC=200$ m", "Dọc bờ chỉ có dòng nước: $v_{23}=\\dfrac{BC}{t_1}$"),
  ("\"tốc độ $4\\ \\text{m/s}$ so với nước (giữ nguyên)\"", "$v_{12}=4$ m/s", "⚠ $v_{12}$ không đổi, chỉ đổi hướng mũi; $\\vec v_{13}=\\vec v_{12}+\\vec v_{23}$"),
  ("\"chiều rộng của sông\"", "Cần $AB$", "Lần 1: $v_{12}\\perp$ bờ nên $AB=v_{12}t_1$"),
  ("\"lần 2: hướng mũi AD … cập đúng B\"", "$\\vec v_{13}$ dọc $AB$ (vuông góc bờ)", "⚠ Thành phần dọc bờ của $v_{12}$ cân bằng $v_{23}$: $v_{23}=v_{12}\\sin\\alpha$"),
  ("\"góc giữa AD và AB\"", "Cần $\\alpha$", "$\\sin\\alpha=\\dfrac{v_{23}}{v_{12}}$"),
  ("\"thời gian qua sông ở lần 2\"", "Cần $t_2$", "$v_{13}=\\sqrt{v_{12}^2-v_{23}^2}$; $t_2=\\dfrac{AB}{v_{13}}$")],
]

RV = ["<strong>Khái niệm:</strong> quãng đường $s$ (độ dài đường đi), độ dịch chuyển $d$ (nối điểm đầu tới điểm cuối).",
      "<strong>Công thức:</strong> tốc độ trung bình $v_{tb}=\\dfrac{s}{t}$ · vận tốc trung bình $v=\\dfrac{d}{t}$.",
      "Đoạn chuyển động đều: $s_i=v_it_i$; tổng $s$ chia tổng $t$.",
      "⚠ <strong>Điều kiện:</strong> đi thẳng, không đổi chiều thì $d=s$ và $v=v_{tb}$."]
RC = ["<strong>Khái niệm:</strong> vận tốc có tính tương đối; (1) vật, (2) hệ chuyển động, (3) hệ đứng yên.",
      "<strong>Công thức cộng:</strong> $\\vec v_{13}=\\vec v_{12}+\\vec v_{23}$.",
      "Cùng chiều: $v_{13}=v_{12}+v_{23}$ · ngược chiều: $v_{13}=\\lvert v_{12}-v_{23}\\rvert$.",
      "Vuông góc: $v_{13}=\\sqrt{v_{12}^2+v_{23}^2}$.",
      "⚠ <strong>Điều kiện:</strong> các vận tốc không đổi; vẽ vectơ trước, tính độ lớn sau."]

SOLS = [
 sol(RV, [
  ("Đổi đơn vị", [M(r"t_1=4\ \text{phút}=240\ \text{s}"), M(r"t_2=10-4=6\ \text{phút}=360\ \text{s}")]),
  ("Quãng đường từng đoạn", [P("Mỗi đoạn chạy đều:"), M(r"s_1=v_1t_1=4\cdot240=960\ \text{m}"), M(r"s_2=v_2t_2=3\cdot360=1080\ \text{m}")]),
  ("Quãng đường và độ dịch chuyển", [M(r"s=s_1+s_2=960+1080"), A(r"s=2040\ \text{m}"), P("Đi thẳng, không đổi chiều nên:"), A(r"d=s=2040\ \text{m}")]),
  ("Tốc độ trung bình và vận tốc trung bình", [P("Tổng thời gian $t=600$ s:"), M(r"v_{tb}=\dfrac{s}{t}=\dfrac{2040}{600}"), A(r"v_{tb}=3{,}4\ \text{m/s}"), P("Vận tốc trung bình bằng tốc độ trung bình, hướng theo chiều chạy:"), A(r"v=3{,}4\ \text{m/s}"), M(r"3{,}4\cdot3{,}6\approx12{,}2\ \text{km/h}")]),
  ("Có lấy trung bình cộng được không?", [M(r"\dfrac{4+3}{2}=3{,}5\ \text{m/s}\neq3{,}4\ \text{m/s}"), P("Bạn chạy ở $3$ m/s lâu hơn ($6$ phút so với $4$ phút) nên tốc độ trung bình bị kéo về gần $3$ m/s."), P("Kiểm tra: $3\\lt3{,}4\\lt4$ ✓")])],
  ["a) $s=2040\\ \\text{m}$ · $d=2040\\ \\text{m}$", "b) $v_{tb}=v=3{,}4\\ \\text{m/s}\\approx12{,}2\\ \\text{km/h}$", "c) Không: hai đoạn khác thời gian; phải lấy tổng $s$ chia tổng $t$"],
  "Nhận dạng: đề cho <strong>tốc độ từng đoạn kèm thời gian từng đoạn</strong> → tính $s$ từng đoạn, rồi tổng $s$ chia tổng $t$."),
 sol(RV + ["Tam giác vuông: $AC=\\sqrt{AB^2+BC^2}$ · $\\tan\\alpha=\\dfrac{BC}{AB}$."], [
  ("Quãng đường", [P("Theo đường đi thật:"), M(r"s=AB+BC=480+360"), A(r"s=840\ \text{m}")]),
  ("Độ dịch chuyển", [P("Mũi tên nối thẳng $A\\to C$, tam giác $ABC$ vuông tại $B$:"), M(r"d=AC=\sqrt{AB^2+BC^2}=\sqrt{480^2+360^2}=\sqrt{360000}"), A(r"d=600\ \text{m}")]),
  ("Thời gian", [M(r"t=6+4=10\ \text{phút}=600\ \text{s}")]),
  ("Tốc độ trung bình", [M(r"v_{tb}=\dfrac{s}{t}=\dfrac{840}{600}"), A(r"v_{tb}=1{,}4\ \text{m/s}")]),
  ("Vận tốc trung bình", [M(r"v=\dfrac{d}{t}=\dfrac{600}{600}"), A(r"v=1{,}0\ \text{m/s}"), P("Hướng theo $\\vec d$ (từ $A$ đến $C$), lệch khỏi hướng đông về phía bắc góc $\\alpha$:"), M(r"\tan\alpha=\dfrac{BC}{AB}=\dfrac{360}{480}=0{,}75"), A(r"\alpha\approx36{,}9^\circ")]),
  ("Kiểm tra", [P("$d\\lt s$ nên $v\\lt v_{tb}$ ($1{,}0\\lt1{,}4$) ✓."), P("Đường gấp khúc: đi qua $B$ dài hơn đi thẳng $A\\to C$.")])],
  ["a) $s=840\\ \\text{m}$ · $d=600\\ \\text{m}$", "b) $v_{tb}=1{,}4\\ \\text{m/s}$ · $v=1{,}0\\ \\text{m/s}$, hướng $A\\to C$ (lệch đông về bắc $\\approx36{,}9^\\circ$)"],
  "Nhận dạng: lộ trình có <strong>chỗ rẽ</strong> → $s$ cộng các đoạn, $d$ nối thẳng đầu–cuối (Pytago nếu vuông góc)."),
 sol(RV + ["Chọn chiều dương: $d$ và $v$ mang dấu."], [
  ("Bơi từ đầu bể đến cuối bể", [P("Cùng chiều dương, không quay đầu: $s=d=50$ m, $t=40$ s."), M(r"v_{tb}=v=\dfrac{50}{40}"), A(r"v_{tb}=v=1{,}25\ \text{m/s}")]),
  ("Bơi từ cuối bể về đầu bể", [P("Ngược chiều dương: $s=50$ m, $d=-50$ m, $t=50$ s."), M(r"v_{tb}=\dfrac{50}{50}=1\ \text{m/s}"), M(r"v=\dfrac{-50}{50}"), A(r"v=-1\ \text{m/s}"), P("Dấu trừ cho biết hướng ngược chiều dương.")]),
  ("Bơi cả đi lẫn về", [P("$s=50+50=100$ m; $t=40+50=90$ s; về đúng chỗ cũ nên $d=0$."), M(r"v_{tb}=\dfrac{100}{90}"), A(r"v_{tb}\approx1{,}11\ \text{m/s}"), M(r"v=\dfrac{0}{90}"), A(r"v=0")]),
  ("Kiểm tra", [P("Tốc độ không âm; vận tốc có thể âm hoặc bằng $0$."), P("$\\dfrac{1{,}25+1}{2}=1{,}125\\neq1{,}11$: không lấy trung bình cộng được.")])],
  ["a) $v_{tb}=v=1{,}25\\ \\text{m/s}$", "b) $v_{tb}=1\\ \\text{m/s}$ · $v=-1\\ \\text{m/s}$", "c) $v_{tb}\\approx1{,}11\\ \\text{m/s}$ · $v=0$"],
  "Nhận dạng: đề có <strong>đi rồi quay lại</strong> → chọn chiều dương, $d$ mang dấu; về chỗ cũ thì $v=0$ dù $v_{tb}\\gt0$."),
 sol(RC, [
  ("Đánh số và đổi đơn vị", [P("(1) mô tô; (2) VĐV dẫn đầu; (3) mặt đường. Cùng chiều nên:"), M(r"v_{13}=v_{12}+v_{23}"), M(r"\Delta t=30\ \text{phút}=0{,}5\ \text{h}")]),
  ("Vận tốc của mô tô so với VĐV", [P("Trong hệ gắn với VĐV, mô tô tiến lại gần $d=10$ km và bắt kịp sau $\\Delta t$:"), M(r"v_{12}=\dfrac{d}{\Delta t}=\dfrac{10}{0{,}5}"), A(r"v_{12}=20\ \text{km/h}")]),
  ("Tốc độ của VĐV so với mặt đường", [M(r"v_{23}=v_{13}-v_{12}=60-20"), A(r"v_{23}=40\ \text{km/h}")]),
  ("Quãng đường mỗi bên so với mặt đường", [M(r"s_{\text{mô tô}}=v_{13}\Delta t=60\cdot0{,}5=30\ \text{km}"), M(r"s_{\text{VĐV}}=v_{23}\Delta t=40\cdot0{,}5=20\ \text{km}")]),
  ("Kiểm tra", [P("Mô tô phải đi nhiều hơn VĐV đúng khoảng cách ban đầu:"), M(r"30-20=10\ \text{km}\ ✓")])],
  ["a) $v_{23}=40\\ \\text{km/h}$", "b) Mô tô $30$ km · VĐV $20$ km"],
  "Nhận dạng: đề cho <strong>khoảng cách ban đầu và thời gian đuổi kịp</strong> → $v_{12}=\\dfrac{d}{\\Delta t}$ rồi cộng vận tốc."),
 sol(RC, [
  ("Đánh số và đổi đơn vị", [P("(1) ca nô; (2) nước; (3) bờ."), M(r"v_{12}=14{,}4\ \text{km/h}=\dfrac{14{,}4}{3{,}6}=4\ \text{m/s}"), M(r"v_{23}=3\ \text{m/s}")]),
  ("Độ lớn vận tốc so với bờ", [P("Mũi vuông góc bờ nên $\\vec v_{12}\\perp\\vec v_{23}$:"), M(r"v_{13}=\sqrt{v_{12}^2+v_{23}^2}=\sqrt{4^2+3^2}"), A(r"v_{13}=5\ \text{m/s}")]),
  ("Hướng của vận tốc", [M(r"\tan\alpha=\dfrac{v_{23}}{v_{12}}=\dfrac{3}{4}=0{,}75"), A(r"\alpha\approx36{,}9^\circ"), P("$\\alpha$ là góc lệch so với hướng mũi (đông), về phía nam (xuôi dòng).")]),
  ("Thời gian qua sông", [P("Chỉ $v_{12}$ đưa ca nô sang ngang bờ:"), M(r"t=\dfrac{200}{v_{12}}=\dfrac{200}{4}"), A(r"t=50\ \text{s}")]),
  ("Độ trôi xuôi dòng", [P("Chỉ $v_{23}$ làm ca nô trôi dọc bờ:"), M(r"x=v_{23}t=3\cdot50"), A(r"x=150\ \text{m}"), P("Kiểm tra: $\\sqrt{200^2+150^2}=250=v_{13}t=5\\cdot50$ ✓")])],
  ["a) $v_{13}=5\\ \\text{m/s}$, hướng đông nam, lệch $\\approx36{,}9^\\circ$ so với hướng đông", "b) $t=50\\ \\text{s}$ · cách điểm đối diện $150\\ \\text{m}$ về phía hạ lưu"],
  "Nhận dạng: <strong>hai vận tốc vuông góc</strong> (mũi vuông góc bờ, dòng chảy dọc bờ) → Pytago cho độ lớn, mỗi thành phần lo một phương."),
 sol(RC, [
  ("Đánh số", [P("(1) ca nô; (2) nước; (3) bờ. $v_{12}=4$ m/s không đổi ở cả hai lần."), M(r"\vec v_{13}=\vec v_{12}+\vec v_{23}")]),
  ("Lần 1: vận tốc nước", [P("Mũi vuông góc bờ: dọc bờ chỉ có dòng nước kéo ca nô đoạn $BC=200$ m trong $100$ s:"), M(r"v_{23}=\dfrac{BC}{t_1}=\dfrac{200}{100}"), A(r"v_{23}=2\ \text{m/s}")]),
  ("Chiều rộng sông", [P("Ngang bờ chỉ có $v_{12}$:"), M(r"AB=v_{12}t_1=4\cdot100"), A(r"AB=400\ \text{m}")]),
  ("Lần 2: góc hướng mũi", [P("Muốn $\\vec v_{13}$ vuông góc bờ, thành phần dọc bờ của $\\vec v_{12}$ phải triệt tiêu $\\vec v_{23}$:"), M(r"v_{23}=v_{12}\sin\alpha"), M(r"\sin\alpha=\dfrac{2}{4}=0{,}5"), A(r"\alpha=30^\circ"), P("Mũi lệch $30^\\circ$ so với $AB$, về phía thượng lưu.")]),
  ("Lần 2: thời gian qua sông", [M(r"v_{13}=\sqrt{v_{12}^2-v_{23}^2}=\sqrt{4^2-2^2}=\sqrt{12}\approx3{,}46\ \text{m/s}"), M(r"t_2=\dfrac{AB}{v_{13}}=\dfrac{400}{3{,}46}"), A(r"t_2\approx115\ \text{s}")]),
  ("Kiểm tra", [P("$t_2\\gt t_1$ ($115\\gt100$): một phần tốc độ máy dùng để chống dòng."), P("Kiểm bằng $v_{13}=v_{12}\\cos30^\\circ=4\\cdot0{,}866\\approx3{,}46$ m/s ✓")])],
  ["a) $v_{23}=2\\ \\text{m/s}$", "b) $AB=400\\ \\text{m}$", "c) $\\alpha=30^\\circ$ (lệch về thượng lưu) · $t_2\\approx115\\ \\text{s}$"],
  "Nhận dạng: đề muốn <strong>tới đúng điểm đối diện</strong> → $\\vec v_{13}$ vuông góc bờ, $v_{23}=v_{12}\\sin\\alpha$."),
]

old = json.load(open(os.path.join(HERE, "old", "50.json")))["questions"]
# Biên tập thành dạng: VD1(0)→D2, VD6(5)→D4, VD7(6)→D5, VD9(8)→D1, VD10(9)→D3, VD16(15)→D6. Còn lại → tự luận (dễ→khó).
ORDER = [3, 1, 2, 4, 10, 7, 11, 14, 13, 12, 16]
MUC = {3: "Dễ", 1: "Dễ", 2: "Dễ", 4: "Dễ", 10: "Dễ", 7: "Dễ", 11: "Trung bình", 14: "Trung bình", 13: "Trung bình", 12: "Khó", 16: "Khó"}
def _rep(i, a, b):
    h = old[i]["body_html"]; assert a in h, (i, a); old[i]["body_html"] = h.replace(a, b)
_rep(2, "\\frac{200}{2.25}=4", "\\frac{200}{2\\cdot25}=\\frac{200}{50}=4")
_rep(2, "\\frac{-200}{2.25}=-4", "\\frac{-200}{2\\cdot25}=\\frac{-200}{50}=-4")
_rep(10, "với tốc độ 15 hải lí/h.", "với tốc độ 15 hải lí/h so với nước.")
_rep(12, "$v_{13}=60km/hv_{23}=40km/h$", "$v_{13}=60km/h$<br />$v_{23}=40km/h$")
_rep(16, "$d_{1}=u.t_{1}d_{2}=u.t_{2}d=d_{1}-d_{2}=u.(t_{1}-t_{2})(2)$", "$d_{1}=u.t_{1}$<br />$d_{2}=u.t_{2}$<br />$d=d_{1}-d_{2}=u.(t_{1}-t_{2})(2)$")
TU_LUAN = tu_luan_tu(old, ORDER, MUC)

write(J, 50, "Bài 5. Tốc độ và vận tốc", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
