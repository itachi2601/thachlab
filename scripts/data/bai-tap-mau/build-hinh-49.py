"""Bài 49 (Vật lí 10, Bài 4. Độ dịch chuyển và quãng đường đi được): sinh scripts/data/bai-tap-mau/49.json
(5 dạng dễ → khó + mục tự luận từ ví dụ cũ). Chạy: python3 scripts/data/bai-tap-mau/build-hinh-49.py"""
import json, math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "49.json")
OLD = json.load(open(os.path.join(HERE, "old/49.json")))["questions"]
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
YEL = "#facc15"

# ───────────── helper riêng của bài ─────────────
def lerp_path(way, durs, n=None):
    """Mẫu cách đều thời gian dọc đường gấp khúc `way` (px), mỗi đoạn mất durs[i] giây (đoạn đứng yên: hai điểm trùng nhau)."""
    total = sum(durs); pts = []
    n = n or round(total / 0.5)   # bước 0,5 s: các điểm gãy (đổi chiều, dừng, rẽ) rơi đúng vào mẫu
    for k in range(n + 1):
        t = total * k / n; acc = 0
        for i, d in enumerate(durs):
            if t <= acc + d + 1e-9:
                f = 0 if d == 0 else (t - acc) / d
                a, b = way[i], way[i + 1]
                pts.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)); break
            acc += d
    return pts, total

def mover(pts, total, r=6):
    """Vật chạy MỘT lần khi bấm nút, dừng ở vị trí cuối (B4)."""
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="{r}" fill="{YEL}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cx", [q[0] for q in pts], total)}{smil("cy", [q[1] for q in pts], total)}</circle>')

def ruler(p, y, x0=24, x1=396, name="x"):
    return arrow(p, "g", x0, y, x1, y, 2) + lbl(x1 + 4, y + 5, name, GRN, 13)

def vdot(x, y1, y2, op=.55):
    return seg(x, y1, x, y2, "currentColor", 1.2, "3 4", op)

# ───────────── Dạng 1: A–B–C, khoảng cách ─────────────
def d1(k):
    p = f"d1{k}"; y = 104 if k == 0 else 120; X = lambda m: 44 + 0.36 * m
    A, C, B = X(0), X(300), X(800)
    b = defs(p) + ruler(p, y, 24, 396) + dot(A, y, 5) + dot(C, y, 5) + dot(B, y, 5)
    b += lbl(A, y + 24, "A (nhà)", "currentColor", 12, "middle", "700") + lbl(C, y + 24, "C (tiệm)", "currentColor", 12, "middle", "700") + lbl(B, y + 24, "B (bưu điện)", "currentColor", 12, "middle", "700")
    if k == 0:
        b += lbl(A, y + 40, "gốc O", "currentColor", 12, "middle", "400")
        b += dim(p, "b", A, 52, B, 52, "AB = 800 m", (A + B) / 2 - 38, 44) + dim(p, "b", A, 78, C, 78, "AC = 300 m", (A + C) / 2 - 40, 70)
        b += vdot(A, 52, y - 6) + vdot(C, 78, y - 6) + vdot(B, 52, y - 6)
        b += lbl(24, 168, "Chiều dương Ox: từ nhà tới bưu điện", "currentColor", 12, "start", "400")
        pts, tot = lerp_path([(A, y), (B, y), (C, y), (A, y)], [8, 5, 3])
        b += mover(pts, tot)
        return fig("d1-0", "0 0 420 176", "Đường thẳng có nhà A, tiệm tạp hóa C cách nhà 300 m và bưu điện B cách nhà 800 m; người đi từ A đến B, quay lại C rồi về A", b,
                   "Mô phỏng: đi A → B → C → A, 1 giây trên hình = 100 m (tốc độ minh hoạ). Bấm Chạy mô phỏng.")
    for i, (x1, x2, yy, t, tx, anc) in enumerate([(A, B, 60, "① A → B", B + 8, "start"), (B, C, 76, "② B → C", C - 8, "end"), (C, A, 92, "③ C → A", C + 8, "start")]):
        b += arrow(p, "o", x1, yy, x2, yy, 3) + lbl(tx, yy + 4, t, ORG, 12, anc, "700")
    b += vdot(A, 56, y - 6) + vdot(C, 56, y - 6) + vdot(B, 56, y - 6)
    b += lbl(24, 164, "s = ? cộng dồn các đoạn  ·  d = ? chỉ điểm đầu → điểm cuối", "currentColor", 12, "start", "700")
    return fig("d1-2", "0 0 420 176", "Ba đoạn đường nối tiếp trên một trục: A đến B, B đến C, C về A", b, "Dữ kiện: các đoạn đi nối đuôi nhau (vẽ lệch nhau cho dễ thấy). " + NOTE)

# ───────────── Dạng 2: tọa độ có dấu ─────────────
def d2(k):
    p = f"d2{k}"; y = 112; X = lambda km: 40 + 17 * (km + 6)
    x1, x2, x3, O = X(12), X(-3), X(2), X(0)
    b = defs(p) + ruler(p, y, 24, 396, "x") + dot(O, y, 4, "currentColor") + lbl(O, y + 22, "O", "currentColor", 13, "middle", "700")
    b += dot(x1, y, 5, GRN) + dot(x2, y, 5, GRN) + dot(x3, y, 5, GRN)
    if k == 0:
        b += vdot(x1, 82, y - 6) + vdot(x2, 82, y - 6) + vdot(x3, 62, y - 6)
        b += lbl(x1, 76, "x₁ = 12 km", "currentColor", 12, "middle", "700") + lbl(x2, 76, "x₂ = −3 km", "currentColor", 12, "middle", "700") + lbl(x3, 56, "x₃ = 2 km", "currentColor", 12, "middle", "700")
        b += lbl(24, 168, "O: trạm xăng · Ox hướng về phía Đông", "currentColor", 12, "start", "400")
        pts, tot = lerp_path([(x1, y), (x2, y), (x3, y)], [7.5, 2.5])
        b += mover(pts, tot)
        return fig("d2-0", "0 0 420 176", "Trục Ox đi qua trạm xăng O; xe xuất phát ở toạ độ 12 km, chạy tới toạ độ âm 3 km rồi quay lại toạ độ 2 km", b,
                   "Mô phỏng: xe chạy x₁ → x₂ → x₃, 1 giây trên hình = 2 km (tốc độ minh hoạ). Bấm Chạy mô phỏng.")
    b += arrow(p, "o", x1, 66, x2, 66, 3) + lbl(x1 + 6, 62, "① x₁ → x₂", ORG, 12, "start", "700")
    b += arrow(p, "o", x2, 84, x3, 84, 3) + lbl(x3 + 8, 88, "② x₂ → x₃", ORG, 12, "start", "700")
    b += vdot(x1, 60, y - 6) + vdot(x2, 60, y - 6) + vdot(x3, 78, y - 6)
    b += lbl(24, 166, "d = x_cuối − x_đầu (có dấu)  ·  s: cộng độ dài đoạn", "currentColor", 12, "start", "700")
    return fig("d2-2", "0 0 420 176", "Hai đoạn nối tiếp trên trục Ox: xe đi về phía âm rồi quay lại phía dương", b, "Dữ kiện: hai đoạn nối đuôi nhau (vẽ lệch nhau cho dễ thấy). " + NOTE)

# ───────────── Dạng 3: hai đoạn vuông góc ─────────────
def d3(k):
    p = f"d3{k}"; s = 0.16; H = (48, 226); Jn = (48 + s * 900, 226); K = (Jn[0], 226 - s * 1200)
    b = defs(p) + dot(*H, 5) + dot(*Jn, 5) + dot(*K, 5)
    b += lbl(H[0], 248, "nhà", "currentColor", 12, "middle", "700") + lbl(Jn[0], 248, "ngã tư", "currentColor", 12, "middle", "700") + lbl(K[0] + 10, K[1] + 4, "trường", "currentColor", 12, "start", "700")
    if k == 0:
        b += seg(*H, *Jn, ORG, 2.4, "6 4") + seg(*Jn, *K, ORG, 2.4, "6 4")
        b += lbl(84, 214, "① 900 m về Đông", ORG, 12, "start", "700") + lbl(Jn[0] + 8, 134, "② 1200 m về Bắc", ORG, 12, "start", "700")
        b += arrow(p, "g", *H, K[0] - 2, K[1] + 4, 2, "5 4") + lbl(66, 124, "d = ?", GRN, 13, "start", "700")
        b += arrow(p, "g", 330, 230, 330, 192, 2) + lbl(330, 184, "Bắc", "currentColor", 12, "middle", "700") + arrow(p, "g", 330, 230, 366, 230, 2) + lbl(370, 234, "Đông", "currentColor", 12, "start", "700")
        pts, tot = lerp_path([H, Jn, K], [9, 12])
        b += mover(pts, tot)
        return fig("d3-0", "0 0 420 258", "Học sinh đi từ nhà 900 m về phía Đông tới ngã tư rồi rẽ trái 1200 m về phía Bắc tới trường", b,
                   "Mô phỏng: nhà → ngã tư → trường, 1 giây trên hình = 100 m (tốc độ minh hoạ). Bấm Chạy mô phỏng.")
    b += arrow(p, "o", *H, Jn[0] - 2, Jn[1], 3) + arrow(p, "o", Jn[0], Jn[1], K[0], K[1] + 4, 3)
    b += arrow(p, "g", *H, K[0] - 3, K[1] + 6, 2, "5 4") + polyline_sq(Jn)
    b += lbl(120, 248, "① 900 m", ORG, 12, "middle", "700") + lbl(Jn[0] + 8, 134, "② 1200 m", ORG, 12, "start", "700")
    b += arc(H[0], H[1], 34, 0, 53, RED) + lbl(88, 200, "α", RED, 13, "start", "700")
    b += lbl(250, 40, "d: cạnh huyền của tam giác", GRN, 12, "start", "700") + lbl(250, 60, "vuông tạo bởi ① và ②", GRN, 12, "start", "700") + lbl(250, 84, "tanα = ② / ①", RED, 12, "start", "700")
    return fig("d3-2", "0 0 420 258", "Hai đoạn vuông góc nối đuôi nhau; độ dịch chuyển là cạnh huyền của tam giác vuông, góc anpha tính với hướng Đông", b, "Dữ kiện: ① và ② vuông góc; d nối nhà tới trường. " + NOTE)

def polyline_sq(Jn, a=10):
    return poly([(Jn[0] - a, Jn[1]), (Jn[0] - a, Jn[1] - a), (Jn[0], Jn[1] - a)], "currentColor", 1.5)

# ───────────── Dạng 4: tốc độ trung bình, có nghỉ ─────────────
def d4(k):
    p = f"d4{k}"; y = 84; X = lambda km: 40 + 55 * km
    N, P_, S = X(0), X(4), X(6)
    ty = 150
    b = defs(p) + ruler(p, y, 24, 396, "") + dot(N, y, 5) + dot(P_, y, 5) + dot(S, y, 5)
    b += lbl(N, y + 24, "nhà", "currentColor", 12, "middle", "700") + lbl(P_, y + 24, "công viên", "currentColor", 12, "middle", "700") + lbl(S, y + 24, "sân bóng", "currentColor", 12, "middle", "700")
    # thanh thời gian (50 phút = 330 px)
    b += f'<rect x="40" y="{ty}" width="330" height="14" fill="none" stroke="currentColor" stroke-width="1.6"/>'
    b += f'<rect x="132" y="{ty}" width="66" height="14" fill="{ORG}" opacity=".3"/>' + seg(132, ty, 132, ty + 14) + seg(198, ty, 198, ty + 14)
    b += lbl(86, ty + 32, "20 phút", "currentColor", 12, "middle", "700") + lbl(165, ty + 32, "nghỉ 10 phút", ORG, 12, "middle", "700") + lbl(284, ty + 32, "20 phút", "currentColor", 12, "middle", "700")
    if k == 0:
        b += arrow(p, "b", N, 52, P_, 52, 1.8) + arrow(p, "b", P_, 52, N, 52, 1.8) + lbl((N + P_) / 2, 44, "4 km", BLUE, 13, "middle", "700")
        b += arrow(p, "b", P_, 52, S, 52, 1.8) + arrow(p, "b", S, 52, P_, 52, 1.8) + lbl((P_ + S) / 2, 44, "2 km", BLUE, 13, "middle", "700")
        pts, tot = lerp_path([(N, y), (P_, y), (P_, y), (S, y)], [8, 4, 8])
        b += mover(pts, tot)
        b += f'<line x1="40" y1="{ty - 6}" x2="40" y2="{ty + 20}" stroke="{BLUE}" stroke-width="3">{smil("x1", [40, 370], tot)}{smil("x2", [40, 370], tot)}</line>'
        return fig("d4-0", "0 0 420 196", "Bạn đạp xe 4 km trong 20 phút, nghỉ 10 phút, rồi đạp thêm 2 km trong 20 phút; thanh bên dưới là đồng hồ", b,
                   "Mô phỏng: chạy nhanh 150 lần (1 giây trên hình = 2,5 phút); vạch xanh trên thanh dưới là đồng hồ. Bấm Chạy mô phỏng.")
    b += arrow(p, "o", N, 56, P_, 56, 3) + lbl((N + P_) / 2, 48, "① 4 km", ORG, 12, "middle", "700")
    b += arrow(p, "o", P_, 56, S, 56, 3) + lbl((P_ + S) / 2, 48, "② 2 km", ORG, 12, "middle", "700")
    b += lbl(24, 20, "⚠ t là toàn bộ thời gian, kể cả lúc nghỉ", RED, 12, "start", "700")
    return fig("d4-2", "0 0 420 196", "Hai đoạn đạp xe nối tiếp và thanh thời gian có một khoảng nghỉ ở giữa", b, "Dữ kiện: s cộng hai đoạn; t cộng cả lúc nghỉ. " + NOTE)

# ───────────── Dạng 5: đổi chiều rồi rẽ vuông góc ─────────────
def d5(k):
    p = f"d5{k}"; s = 32; O = (48, 180); A = (O[0] + 7 * s, 180); B = (O[0] + 4 * s, 180); C = (B[0], 180 - 3 * s)
    b = defs(p) + dot(*O, 5) + dot(*C, 5)
    b += lbl(O[0], 210, "O (xuất phát)", "currentColor", 12, "start", "700")
    if k == 0:
        b += arrow(p, "o", O[0], 172, A[0], 172, 2) + arrow(p, "o", A[0], 188, B[0], 188, 2) + arrow(p, "o", B[0], 188, C[0], C[1] + 6, 2)
        b += lbl(186, 160, "① 7 m về Đông", ORG, 12, "start", "700") + lbl(B[0] + 4, 224, "② 3 m về Tây", ORG, 12, "start", "700") + lbl(C[0] + 8, 134, "③ 3 m về Bắc", ORG, 12, "start", "700")
        b += lbl(C[0] + 8, C[1] + 4, "dừng", "currentColor", 12, "start", "700") + lbl(236, 50, "cả hành trình: 26 s", "currentColor", 13, "start", "700")
        b += arrow(p, "g", O[0] + 2, O[1] - 2, C[0] - 2, C[1] + 4, 2, "5 4") + lbl(60, 118, "d = ?", GRN, 13, "start", "700")
        pts, tot = lerp_path([(O[0], 172), (A[0], 172), (A[0], 188), (B[0], 188), (B[0], C[1] + 6)], [14, 0, 6, 6])
        b += mover(pts, tot)
        return fig("d5-0", "0 0 420 244", "Xe mô hình đi 7 m về phía Đông, quay đầu 3 m về phía Tây rồi rẽ 3 m về phía Bắc và dừng", b,
                   "Mô phỏng: chạy đúng thời gian thật (26 s), tốc độ không đổi; ba đoạn vẽ lệch nhau cho dễ thấy. Bấm Chạy mô phỏng.")
    b += arrow(p, "o", O[0], 172, A[0], 172, 2) + arrow(p, "o", A[0], 188, B[0], 188, 2) + arrow(p, "o", B[0], 188, C[0], C[1] + 6, 2)
    b += lbl(230, 164, "①", ORG, 13, "start", "700") + lbl(B[0] + 4, 224, "②", ORG, 13, "start", "700") + lbl(C[0] + 8, 134, "③", ORG, 13, "start", "700")
    b += arrow(p, "g", O[0] + 2, O[1] - 2, C[0] - 2, C[1] + 4, 2, "5 4") + lbl(66, 120, "d", GRN, 13, "start", "700") + arc(O[0], O[1], 34, 0, 37, RED) + lbl(86, 166, "α", RED, 13, "start", "700")
    b += lbl(222, 36, "① − ②: cùng phương", BLUE, 12, "start", "700") + lbl(222, 56, "d² = (① − ②)² + ③²", GRN, 12, "start", "700")
    b += lbl(222, 76, "tanα = ③ / (① − ②)", RED, 12, "start", "700") + lbl(222, 96, "s = ① + ② + ③", ORG, 12, "start", "700")
    return fig("d5-2", "0 0 420 244", "Gộp hai đoạn cùng phương ngược chiều, rồi dùng định lí Pi-ta-go với đoạn vuông góc", b, "Dữ kiện: ① và ② cùng đường, ngược chiều; ③ vuông góc với chúng (vẽ lệch cho dễ thấy). " + NOTE)

BUILD = [d1, d2, d3, d4, d5]

TOPIC_DD = "Phân biệt quãng đường và độ dịch chuyển"
TOPIC_TD = "Tốc độ trung bình và vận tốc trung bình"
DANG = [
 dict(label="Dạng 1 · Dễ · Đi rồi quay lại trên một đường thẳng: tìm d và s", topic=TOPIC_DD,
      problem_html="<p>Trên một đường thẳng, nhà <strong>A</strong> cách bưu điện <strong>B</strong> $800\\ \\text{m}$; tiệm tạp hoá <strong>C</strong> nằm giữa A và B, cách nhà $300\\ \\text{m}$. Chọn nhà A làm gốc $O$, chiều dương hướng từ nhà tới bưu điện. Một người đi từ nhà tới bưu điện, rồi quay lại tiệm tạp hoá.</p>"
                   "<ol type=\"a\"><li>Tìm độ dịch chuyển và quãng đường đi được.</li><li>Người đó đi tiếp từ tiệm về nhà. Tìm độ dịch chuyển và quãng đường đi được trong cả hành trình A → B → C → A.</li></ol>"),
 dict(label="Dạng 2 · Dễ · Dùng toạ độ có dấu: d âm nghĩa là gì", topic=TOPIC_DD,
      problem_html="<p>Một xe tải chạy trên đường thẳng. Chọn trạm xăng làm gốc $O$, trục $Ox$ hướng về phía Đông. Xe xuất phát ở toạ độ $x_1 = 12\\ \\text{km}$, chạy một mạch về phía Tây tới toạ độ $x_2 = -3\\ \\text{km}$, rồi quay đầu chạy về phía Đông tới toạ độ $x_3 = 2\\ \\text{km}$ thì dừng.</p>"
                   "<ol type=\"a\"><li>Tìm độ dịch chuyển và quãng đường đi được của đoạn $x_1 \\to x_2$.</li><li>Tìm độ dịch chuyển và quãng đường đi được trong cả hành trình. Điểm dừng nằm về phía nào của điểm xuất phát?</li></ol>"),
 dict(label="Dạng 3 · Trung bình · Hai đoạn vuông góc: độ lớn và hướng của d", topic=TOPIC_DD,
      problem_html="<p>Một học sinh đi bộ từ nhà tới trường: đi thẳng $900\\ \\text{m}$ về phía Đông tới ngã tư, rồi rẽ trái đi thẳng $1200\\ \\text{m}$ về phía Bắc thì tới trường.</p>"
                   "<ol type=\"a\"><li>Tính quãng đường đi được.</li><li>Tính độ lớn độ dịch chuyển của học sinh.</li><li>Độ dịch chuyển hợp với hướng Đông một góc bao nhiêu?</li></ol>"),
 dict(label="Dạng 4 · Trung bình · Tốc độ trung bình khi có đoạn nghỉ", topic=TOPIC_TD,
      problem_html="<p>Một bạn đạp xe trên đường thẳng, không đổi chiều: đạp $4\\ \\text{km}$ từ nhà tới công viên hết $20$ phút, nghỉ $10$ phút, rồi đạp tiếp $2\\ \\text{km}$ tới sân bóng hết $20$ phút.</p>"
                   "<ol type=\"a\"><li>Tính tốc độ trung bình trên từng đoạn đạp (km/h).</li><li>Tính tốc độ trung bình trên cả hành trình, theo $\\text{km/h}$ và $\\text{m/s}$.</li><li>Tốc độ trung bình cả hành trình có bằng trung bình cộng của hai tốc độ ở câu a không?</li></ol>"),
 dict(label="Dạng 5 · Khó · Quay đầu rồi rẽ vuông góc: d, s và tốc độ trung bình", topic=TOPIC_DD,
      problem_html="<p>Một xe mô hình chạy trên sàn nhà với tốc độ không đổi. Từ điểm $O$, xe đi thẳng $7\\ \\text{m}$ về phía Đông, quay đầu đi $3\\ \\text{m}$ về phía Tây trên cùng đường, rồi rẽ đi thẳng $3\\ \\text{m}$ về phía Bắc thì dừng. Cả hành trình mất $26\\ \\text{s}$.</p>"
                   "<ol type=\"a\"><li>Tính quãng đường đi được.</li><li>Tính độ lớn và hướng của độ dịch chuyển.</li><li>Tính tốc độ trung bình.</li></ol>"),
]

DK = "⚠ Phải chọn gốc $O$ và chiều dương trước; $d$ có dấu, $s \\ge 0$"
ANALYSIS = [
 [("\"Chọn nhà A làm gốc, chiều dương từ nhà tới bưu điện\"", "$x_A=0$; $x_B=800$ m; $x_C=300$ m", DK),
  ("\"đi từ nhà tới bưu điện, rồi quay lại tiệm tạp hoá\"", "Đổi chiều ở B; điểm cuối là C", "$s$ cộng dồn mọi đoạn; $d=x_{cuối}-x_{đầu}$"),
  ("\"tìm độ dịch chuyển và quãng đường\"", "Cần $d$ và $s$", "Điểm đầu, điểm cuối ở đâu? Có quay đầu không?"),
  ("\"đi tiếp từ tiệm về nhà\"", "Đi từ C về A", "⚠ $d$ chỉ phụ thuộc điểm đầu và điểm cuối; $s$ vẫn cộng dồn. Điểm cuối so với điểm đầu thì sao?"),
  ("\"cả hành trình A → B → C → A\"", "Ba đoạn nối tiếp", "$s$ cộng các đoạn; $d=x_{cuối}-x_{đầu}$")],
 [("\"Chọn trạm xăng làm gốc $O$, trục $Ox$ hướng về phía Đông\"", "Chiều dương = hướng Đông", DK),
  ("\"xuất phát ở toạ độ $x_1=12$ km\"", "$x_1=12$ km", "Toạ độ cho vị trí (có dấu)"),
  ("\"chạy một mạch về phía Tây tới $x_2=-3$ km\"", "$x_2=-3$ km; không đổi chiều", "$d=x_2-x_1$; không đổi chiều nên $s=|d|$"),
  ("\"quay đầu chạy về phía Đông tới $x_3=2$ km\"", "$x_3=2$ km; đổi chiều ở $x_2$", "⚠ Đổi chiều: tách thành hai đoạn rồi cộng $s$"),
  ("\"trong cả hành trình\"", "Đầu $x_1$, cuối $x_3$", "$d=x_3-x_1$ (không phụ thuộc đường đi)"),
  ("\"điểm dừng nằm về phía nào?\"", "Cần hướng của $d$", "Dấu của $d$ cho biết điều gì về hướng?")],
 [("\"đi thẳng $900$ m về phía Đông\"", "$d_1=900$ m, hướng Đông", "Đoạn 1 thẳng, không đổi chiều"),
  ("\"rẽ trái đi thẳng $1200$ m về phía Bắc\"", "$d_2=1200$ m, hướng Bắc", "⚠ Đông ⊥ Bắc: hai đoạn vuông góc → Pi-ta-go, không cộng số"),
  ("\"tính quãng đường đi được\"", "Cần $s$", "$s=d_1+d_2$ (cộng dồn)"),
  ("\"độ lớn độ dịch chuyển\"", "Cần $d$", "$d=\\sqrt{d_1^2+d_2^2}$ (nối nhà tới trường)"),
  ("\"hợp với hướng Đông một góc\"", "Cần $\\alpha$", "$\\tan\\alpha=\\dfrac{d_2}{d_1}$")],
 [("\"đạp $4$ km hết $20$ phút\"", "$s_1=4$ km; $t_1=20$ phút", "$v_{tb}=\\dfrac{s}{t}$ cho từng đoạn"),
  ("\"nghỉ $10$ phút\"", "$t_{nghỉ}=10$ phút", "⚠ Thời gian nghỉ vẫn tính vào $t$ của cả hành trình"),
  ("\"đạp tiếp $2$ km hết $20$ phút\"", "$s_2=2$ km; $t_2=20$ phút", "Đổi $20$ phút $=\\dfrac{1}{3}$ h"),
  ("\"không đổi chiều\"", "Đường thẳng, một chiều", "Nên $s=d$; $v_{tb}$ vẫn dùng $s$"),
  ("\"tốc độ trung bình cả hành trình\"", "Cần $v_{tb}$ (km/h, m/s)", "$v_{tb}=\\dfrac{s_1+s_2}{t_1+t_{nghỉ}+t_2}$; $1$ m/s $=3{,}6$ km/h"),
  ("\"có bằng trung bình cộng …?\"", "So $v_{tb}$ với $\\dfrac{v_1+v_2}{2}$", "Ghi lại định nghĩa $v_{tb}$ rồi so sánh với $\\dfrac{v_1+v_2}{2}$")],
 [("\"đi thẳng $7$ m về phía Đông\"", "① $=7$ m, hướng Đông", "Đoạn thẳng không đổi chiều"),
  ("\"quay đầu đi $3$ m về phía Tây trên cùng đường\"", "② $=3$ m, ngược hướng ①", "⚠ Cùng phương, ngược chiều: gộp $d=|①-②|$, còn $s=①+②$"),
  ("\"rẽ đi thẳng $3$ m về phía Bắc\"", "③ $=3$ m, hướng Bắc", "⚠ ③ ⊥ ①②: dùng Pi-ta-go với đoạn đã gộp"),
  ("\"tính quãng đường đi được\"", "Cần $s$", "$s$ = tổng độ dài ba đoạn"),
  ("\"độ lớn và hướng của độ dịch chuyển\"", "Cần $d$, $\\alpha$", "$d=\\sqrt{(①-②)^2+③^2}$; $\\tan\\alpha=\\dfrac{③}{①-②}$"),
  ("\"cả hành trình mất $26$ s\"", "$t=26$ s", "$v_{tb}=\\dfrac{s}{t}$ (dùng $s$, không dùng $d$)")],
]

R1 = ["<strong>Khái niệm:</strong> $s$ là độ dài cộng dồn, $s\\ge0$; độ dịch chuyển $\\vec d$ chỉ nối điểm đầu → điểm cuối.",
      "Trên trục $Ox$: $d=x_{cuối}-x_{đầu}$, có dấu.",
      "Đổi chiều: $d\\lt s$. Quay về chỗ cũ: $d=0$.",
      "⚠ <strong>Điều kiện:</strong> chọn gốc $O$ và chiều dương trước khi ghi toạ độ."]
R2 = ["<strong>Khái niệm:</strong> $d=x_{cuối}-x_{đầu}$, dấu của $d$ cho biết hướng so với chiều dương.",
      "$s$ cộng độ dài từng đoạn không đổi chiều: $s=|d|$ trên mỗi đoạn.",
      "Đổi chiều thì tách đoạn rồi cộng $s$.",
      "⚠ <strong>Điều kiện:</strong> trục $Ox$ hướng về phía Đông (chiều dương)."]
R3 = ["<strong>Khái niệm:</strong> $s$ cộng dồn; $\\vec d$ nối nhà tới trường.",
      "Hai đoạn vuông góc: $d=\\sqrt{d_1^2+d_2^2}$ · $\\tan\\alpha=\\dfrac{d_2}{d_1}$",
      "$s=d_1+d_2$",
      "⚠ <strong>Điều kiện:</strong> Pi-ta-go chỉ dùng khi hai đoạn vuông góc."]
R4 = ["<strong>Khái niệm:</strong> tốc độ trung bình cho biết nhanh hay chậm, không âm, không có hướng.",
      "$v_{tb}=\\dfrac{s}{t}$ · $1\\ \\text{m/s}=3{,}6\\ \\text{km/h}$",
      "⚠ <strong>Điều kiện:</strong> $t$ là toàn bộ thời gian, kể cả lúc nghỉ; $s$ là quãng đường, không phải $d$."]
R5 = ["<strong>Khái niệm:</strong> $s$ cộng dồn; $d$ chỉ đầu → cuối; $v_{tb}=\\dfrac{s}{t}$.",
      "Cùng phương: ngược chiều lấy hiệu, cùng chiều lấy tổng.",
      "Vuông góc: $d=\\sqrt{d_1^2+d_2^2}$ · $\\tan\\alpha=\\dfrac{d_2}{d_1}$",
      "⚠ <strong>Điều kiện:</strong> gộp đoạn cùng phương trước, rồi mới dùng Pi-ta-go."]

SOLS = [
 sol(R1, [
  ("Ghi toạ độ các điểm", [P("Gốc $O\\equiv A$, chiều dương tới B:"), M(r"x_A=0\ \text{m}\ ;\ x_C=300\ \text{m}\ ;\ x_B=800\ \text{m}")]),
  ("Câu a: A → B → C", [P("Quãng đường: đi $AB$ rồi quay lại $BC$:"), M(r"BC=800-300=500\ \text{m}"), M(r"s=AB+BC=800+500"), A(r"s=1300\ \text{m}"),
                       P("Độ dịch chuyển: điểm đầu A, điểm cuối C:"), M(r"d=x_C-x_A"), M(r"d=300-0"), A(r"d=+300\ \text{m}\ \ (\text{cùng chiều dương})")]),
  ("Câu b: đi tiếp C → A", [P("Quãng đường: cộng thêm $CA=300$ m:"), M(r"s=1300+300"), A(r"s=1600\ \text{m}"),
                           P("Điểm cuối trùng điểm đầu:"), M(r"d=x_A-x_A"), A(r"d=0")]),
  ("Kiểm tra", [P("Câu a: $d=300\\lt s=1300$ vì có quay đầu ✓"), P("Câu b: $d=0$ nhưng $s\\ne0$ — đồng hồ đo quãng đường vẫn đếm ✓")])],
  ["a) $d=+300\\ \\text{m}$ · $s=1300\\ \\text{m}$", "b) $d=0$ · $s=1600\\ \\text{m}$"],
  "Nhận dạng: đề cho <strong>các đoạn nối tiếp có quay đầu</strong> → $s$ cộng từng đoạn, $d$ chỉ nhìn điểm đầu và điểm cuối."),
 sol(R2, [
  ("Đoạn $x_1\\to x_2$", [P("Độ dịch chuyển:"), M(r"d_1=x_2-x_1"), M(r"d_1=-3-12"), A(r"d_1=-15\ \text{km}"),
                         P("Không đổi chiều nên quãng đường bằng độ lớn của $d_1$:"), A(r"s_1=15\ \text{km}")]),
  ("Đoạn $x_2\\to x_3$", [P("Quay đầu, chạy về phía Đông:"), M(r"d_2=x_3-x_2"), M(r"d_2=2-(-3)"), A(r"d_2=+5\ \text{km}"), M(r"s_2=5\ \text{km}")]),
  ("Cả hành trình", [P("Quãng đường cộng hai đoạn:"), M(r"s=s_1+s_2=15+5"), A(r"s=20\ \text{km}"),
                    P("Độ dịch chuyển chỉ cần điểm đầu và điểm cuối:"), M(r"d=x_3-x_1"), M(r"d=2-12"), A(r"d=-10\ \text{km}")]),
  ("Hướng", [P("$d\\lt0$: ngược chiều dương, nên điểm dừng nằm <strong>phía Tây</strong> điểm xuất phát, cách $10$ km.")]),
  ("Kiểm tra", [P("$|d|=10\\lt s=20$ vì có quay đầu ✓"), P("Cộng hai độ dịch chuyển đoạn: $-15+5=-10$ khớp ✓")])],
  ["a) $d=-15\\ \\text{km}$ · $s=15\\ \\text{km}$", "b) $d=-10\\ \\text{km}$ (về phía Tây) · $s=20\\ \\text{km}$"],
  "Nhận dạng: đề cho <strong>toạ độ có dấu</strong> → $d=x_{cuối}-x_{đầu}$; đổi chiều thì tách đoạn để cộng $s$."),
 sol(R3, [
  ("Quãng đường", [P("Cộng dồn hai đoạn:"), M(r"s=d_1+d_2=900+1200"), A(r"s=2100\ \text{m}")]),
  ("Độ lớn độ dịch chuyển", [P("Đông vuông góc Bắc, $\\vec d$ nối nhà tới trường là cạnh huyền:"), M(r"d=\sqrt{d_1^2+d_2^2}=\sqrt{900^2+1200^2}=\sqrt{2\,250\,000}"), A(r"d=1500\ \text{m}")]),
  ("Góc so với hướng Đông", [M(r"\tan\alpha=\dfrac{d_2}{d_1}=\dfrac{1200}{900}\approx1{,}333"), A(r"\alpha\approx53^\circ"), P("Lệch từ hướng Đông về phía Bắc.")]),
  ("Kiểm tra", [P("$d=1500$ lớn hơn từng đoạn ($900$; $1200$), nhỏ hơn tổng $2100$ ✓"), P("$d\\lt s$ vì có rẽ ✓")])],
  ["a) $s=2100\\ \\text{m}$", "b) $d=1500\\ \\text{m}$", "c) $\\alpha\\approx53^\\circ$ so với hướng Đông"],
  "Nhận dạng: đề cho <strong>hai hướng vuông góc</strong> (Đông–Bắc) → $s$ cộng số, $d$ dùng Pi-ta-go."),
 sol(R4, [
  ("Tốc độ từng đoạn", [P("Đổi $20$ phút $=\\dfrac{1}{3}$ h:"), M(r"v_1=\dfrac{s_1}{t_1}=\dfrac{4}{1/3}"), A(r"v_1=12\ \text{km/h}"), M(r"v_2=\dfrac{s_2}{t_2}=\dfrac{2}{1/3}"), A(r"v_2=6\ \text{km/h}")]),
  ("Quãng đường và thời gian cả hành trình", [M(r"s=4+2=6\ \text{km}"), P("Tính cả lúc nghỉ:"), M(r"t=20+10+20=50\ \text{phút}=\dfrac{5}{6}\ \text{h}")]),
  ("Tốc độ trung bình", [M(r"v_{tb}=\dfrac{s}{t}=\dfrac{6}{5/6}"), A(r"v_{tb}=7{,}2\ \text{km/h}"), P("Đổi đơn vị:"), M(r"v_{tb}=\dfrac{7{,}2}{3{,}6}"), A(r"v_{tb}=2\ \text{m/s}")]),
  ("So với trung bình cộng", [M(r"\dfrac{v_1+v_2}{2}=\dfrac{12+6}{2}=9\ \text{km/h}"), P("$9\\ne7{,}2$: <strong>không bằng</strong>. Hai đoạn đạp dài bằng nhau về thời gian nhưng còn thêm $10$ phút nghỉ kéo $v_{tb}$ xuống.")]),
  ("Kiểm tra", [P("$v_{tb}=7{,}2\\lt v_1=12$ vì có nghỉ ✓"), P("Đơn vị: km ÷ h = km/h ✓")])],
  ["a) $v_1=12\\ \\text{km/h}$ · $v_2=6\\ \\text{km/h}$", "b) $v_{tb}=7{,}2\\ \\text{km/h}=2\\ \\text{m/s}$", "c) Không bằng ($9\\ \\text{km/h}$)"],
  "Nhận dạng: đề cho <strong>nhiều đoạn, có nghỉ</strong> → $v_{tb}=\\dfrac{\\text{tổng }s}{\\text{tổng }t}$, không lấy trung bình cộng các tốc độ."),
 sol(R5, [
  ("Quãng đường", [P("Cộng dồn ba đoạn (đoạn quay đầu vẫn tính):"), M(r"s=7+3+3"), A(r"s=13\ \text{m}")]),
  ("Gộp hai đoạn cùng phương", [P("Đông rồi Tây, ngược chiều: lấy hiệu."), M(r"d_{Đ}=7-3=4\ \text{m}\ \ (\text{về phía Đông})"), P("Đoạn Bắc: $d_B=3$ m, vuông góc với phương Đông–Tây.")]),
  ("Độ lớn và hướng của $\\vec d$", [M(r"d=\sqrt{d_Đ^2+d_B^2}=\sqrt{4^2+3^2}=\sqrt{25}"), A(r"d=5\ \text{m}"), M(r"\tan\alpha=\dfrac{d_B}{d_Đ}=\dfrac{3}{4}=0{,}75"), A(r"\alpha\approx37^\circ"), P("So với hướng Đông, lệch về phía Bắc.")]),
  ("Tốc độ trung bình", [P("Dùng quãng đường, không dùng $d$:"), M(r"v_{tb}=\dfrac{s}{t}=\dfrac{13}{26}"), A(r"v_{tb}=0{,}5\ \text{m/s}")]),
  ("Kiểm tra", [P("$d=5\\lt s=13$ vì có quay đầu và rẽ ✓"), P("Xe đi tốc độ không đổi: $v=0{,}5$ m/s, khớp mô phỏng ($7$ m mất $14$ s) ✓")])],
  ["a) $s=13\\ \\text{m}$", "b) $d=5\\ \\text{m}$, $\\alpha\\approx37^\\circ$ so với hướng Đông (về phía Bắc)", "c) $v_{tb}=0{,}5\\ \\text{m/s}$"],
  "Nhận dạng: đề <strong>quay đầu rồi rẽ vuông góc</strong> → gộp đoạn cùng phương trước, rồi Pi-ta-go; tốc độ dùng $s$."),
]

# ví dụ cũ (0-based) chưa biên tập: ví dụ 1→D1, 6→D2, 11→D3, 13→D5 đã dùng làm gốc
ORDER = [4, 13, 11, 6, 2, 1, 3, 7, 9, 8, 14]
MUC = {4: "Dễ", 13: "Dễ", 11: "Dễ", 6: "Dễ", 2: "Dễ", 1: "Trung bình", 3: "Trung bình", 7: "Trung bình", 9: "Trung bình", 8: "Trung bình", 14: "Khó"}
TU_LUAN = tu_luan_tu(OLD, ORDER, MUC)

write(J, 49, "Bài 4. Độ dịch chuyển và quãng đường đi được", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
