"""Bài tập mẫu bài 9 (lesson 10) — Khái niệm từ trường. 4 dạng, dễ → khó.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-10.py  → ghi scripts/data/bai-tap-mau/10.json
Hình tính thật: đường sức thanh nam châm = tích phân số trường của hai cực điểm (N, S); kim la bàn quay đến góc arctan(B_dây/B_đ)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "10.json")
VB = "0 0 420 250"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
MUTE = "#94a3b8"

# ───────────── hàm chung ─────────────
def needle(cx, cy, angles, dur, L=50):
    """Kim la bàn nhìn từ trên xuống, bắc = lên. Đầu N (đỏ) ở phía trên khi angle = 0; angle > 0 quay theo chiều kim đồng hồ (về đông).
    angles: danh sách góc (độ) theo thời gian, chạy một lần khi bấm; phần tử đầu là vị trí xuất phát."""
    vals = ";".join(f"{a:.1f} {cx} {cy}" for a in angles)
    n = (f'<polygon points="{cx - 7},{cy} {cx + 7},{cy} {cx},{cy - L}" fill="{RED}" stroke="currentColor" stroke-width="1.4"/>'
         f'<polygon points="{cx - 7},{cy} {cx + 7},{cy} {cx},{cy + L}" fill="none" stroke="currentColor" stroke-width="1.4"/>'
         f'<circle cx="{cx}" cy="{cy}" r="3" fill="currentColor"/>')
    return (f'<g transform="rotate({angles[0]:.1f} {cx} {cy})"><animateTransform attributeName="transform" type="rotate" values="{vals}" '
            f'dur="{dur}s" begin="indefinite" fill="freeze"/>{n}</g>')

def compass(cx, cy, r=70):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="2"/>'
    for a in range(0, 360, 45):
        c, sn = math.cos(math.radians(a)), math.sin(math.radians(a))
        s += seg(cx + (r - 6) * c, cy - (r - 6) * sn, cx + r * c, cy - r * sn, "currentColor", 1.5)
    s += lbl(cx, cy - r - 8, "Bắc", "currentColor", 13, "middle", "700") + lbl(cx, cy + r + 20, "Nam", "currentColor", 13, "middle", "400")
    s += lbl(cx - r - 8, cy + 5, "Tây", "currentColor", 13, "end", "400") + lbl(cx + r + 8, cy + 5, "Đông", "currentColor", 13, "start", "400")
    return s

def damped(final, n=6):
    """Kim dao động tắt dần rồi dừng đúng ở góc `final` (độ). Số mẫu cố định; mẫu cuối là góc cuối."""
    return [0.0, final * 1.35, final * 0.82, final * 1.1, final * 0.95, final]

def wire_ns(p, cx, cy, up=True, label="dây dẫn (nằm trên la bàn)", lx=None, ly=None):
    """Dây thẳng nằm theo phương bắc – nam nhìn từ trên xuống: đoạn thẳng đứng + mũi tên dòng điện."""
    y1, y2 = (cy + 100, cy - 100) if up else (cy - 100, cy + 100)
    s = seg(cx, cy - 100, cx, cy + 100, ORG, 5, "", 0.45) + arrow(p, "o", cx, y1 - (-25 if up else 25), cx, y2 + (25 if up else -25), 3)
    return s

# ───────────── Dạng 1: thanh nam châm, đường sức ─────────────
NP, SP = (255, 130), (165, 130)

def _B(x, y):
    bx = by = 0.0
    for (px, py), q in ((NP, 1), (SP, -1)):
        dx, dy = x - px, y - py
        r = math.hypot(dx, dy)
        bx += q * dx / r ** 3
        by += q * dy / r ** 3
    return bx, by

def mag_line(phi, r0=8):
    x = NP[0] + r0 * math.cos(math.radians(phi))
    y = NP[1] - r0 * math.sin(math.radians(phi))
    pts = [(x, y)]
    for _ in range(4000):
        bx, by = _B(x, y); n = math.hypot(bx, by); h = 2
        bx, by = _B(x + bx / n * h / 2, y + by / n * h / 2); n = math.hypot(bx, by)
        x += bx / n * h; y += by / n * h
        pts.append((x, y))
        if math.hypot(x - SP[0], y - SP[1]) < r0:
            break
    out = [q for q in pts if not (150 <= q[0] <= 270 and 118 <= q[1] <= 142)]   # bỏ phần nằm trong thanh
    return out

def magnet():
    return (f'<rect x="150" y="118" width="60" height="24" fill="{BLUE}" fill-opacity="0.35" stroke="currentColor" stroke-width="2"/>'
            f'<rect x="210" y="118" width="60" height="24" fill="{RED}" fill-opacity="0.35" stroke="currentColor" stroke-width="2"/>'
            + lbl(180, 135, "S", "currentColor", 14, "middle", "700") + lbl(240, 135, "N", "currentColor", 14, "middle", "700"))

def d1(k):
    p = f"d1{k}"
    b = ""
    lines = [mag_line(a) for a in (78, 95, 112, 130)]
    if k == 0:
        for i, pts in enumerate(lines):
            for sgn in (1, -1):
                q = [(x, 130 + sgn * (y - 130)) for x, y in pts]
                # mạt sắt: chuỗi hạt hiện dần, mỗi đường một nhịp (keyTimes); trạng thái nền = đã hiện đủ
                t0 = 0.12 * i
                b += (f'<polyline fill="none" stroke="{MUTE}" stroke-width="3" stroke-dasharray="1 6" stroke-linecap="round" points="'
                      + " ".join(f"{x:.1f},{y:.1f}" for x, y in q) + f'"><animate attributeName="opacity" values="0;0;1" keyTimes="0;{t0:.2f};{min(t0 + 0.5, 1):.2f}" dur="3s" begin="indefinite" fill="freeze"/></polyline>')
        b += magnet()
        b += lbl(296, 190, "Rắc mạt sắt quanh", "currentColor", 13, "start", "400")
        b += lbl(296, 208, "thanh nam châm;", "currentColor", 13, "start", "400") + lbl(296, 226, "kim đặt tại M, P, Q", "currentColor", 13, "start", "400")
        for nm, (x, y) in (("M", (210, 74)), ("P", (322, 130)), ("Q", (210, 130))):
            b += dot(x, y, 4.5, ORG if nm != "Q" else "currentColor") + lbl(x + 8, y - 8, nm, ORG, 14, "start", "700")
        return fig("d1-0", VB, "Mạt sắt rắc quanh thanh nam châm thẳng xếp thành các chuỗi hạt cong từ cực này sang cực kia", b, "Mô phỏng: mạt sắt xếp thành chuỗi quanh thanh nam châm (từ phổ), hình dạng tính từ mô hình hai cực. Bấm Chạy mô phỏng.")
    for pts in lines:
        for sgn in (1, -1):
            q = [(x, 130 + sgn * (y - 130)) for x, y in pts]
            b += poly(q, MUTE, 1.8, "", 0.9)
    b += magnet()
    for nm, (x, y), c in (("M", (210, 74), ORG), ("P", (322, 130), ORG), ("Q", (210, 130), "currentColor"), ("A", (282, 98), BLUE), ("B", (210, 28), BLUE)):
        b += dot(x, y, 4.5, c) + lbl(x + 8, y - 8, nm, c, 14, "start", "700")
    b += lbl(296, 190, "Đường sức quy ước:", "currentColor", 13, "start", "700")
    b += lbl(296, 208, "A: mau · B: thưa", BLUE, 13, "start", "700")
    return fig("d1-2", VB, "Thanh nam châm thẳng với các điểm M, P, Q đặt kim và hai điểm A, B để so sánh độ mạnh", b, "Dữ kiện: vị trí các điểm cần xét. " + NOTE)

# ───────────── Dạng 2: dây thẳng, nắm tay phải ─────────────
W = (210, 125)   # tâm dây

def wire_dot(p):
    return (f'<circle cx="{W[0]}" cy="{W[1]}" r="9" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            f'<circle cx="{W[0]}" cy="{W[1]}" r="3" fill="currentColor"/>')

def d2(k):
    p = f"d2{k}"
    b = defs(p)
    rs = (30, 60, 90)
    if k == 0:
        for i, r in enumerate(rs):
            b += (f'<circle cx="{W[0]}" cy="{W[1]}" r="{r}" fill="none" stroke="{MUTE}" stroke-width="3" stroke-dasharray="1 6" stroke-linecap="round">'
                  f'<animate attributeName="r" values="0;{r}" dur="{1.2 + 0.4 * i:.1f}s" begin="indefinite" fill="freeze"/></circle>')
        b += wire_dot(p)
        for nm, (x, y) in (("A", (W[0] + 30, W[1])), ("B", (W[0], W[1] - 30)), ("C", (W[0] - 90, W[1]))):
            b += dot(x, y, 4.5, ORG) + lbl(x + 8, y - 8, nm, ORG, 14, "start", "700")
        b += lbl(16, 14, "I hướng ra phía người nhìn", "currentColor", 13, "start", "700")
        b += lbl(16, 30, "(dây vuông góc trang giấy)", "currentColor", 13, "start", "400")
        b += lbl(W[0] + 4, W[1] + 24, "dây", "currentColor", 13, "start", "400")
        return fig("d2-0", VB, "Dây thẳng dài vuông góc trang giấy; mạt sắt rắc quanh dây xếp thành các vòng tròn đồng tâm", b, "Mô phỏng: mạt sắt quanh dây xếp thành vòng tròn đồng tâm (từ phổ). Bấm Chạy mô phỏng.")
    for r in rs:
        b += f'<circle cx="{W[0]}" cy="{W[1]}" r="{r}" fill="none" stroke="{MUTE}" stroke-width="1.8"/>'
    b += wire_dot(p)
    for nm, (x, y) in (("A", (W[0] + 30, W[1])), ("B", (W[0], W[1] - 30)), ("C", (W[0] - 90, W[1]))):
        b += dot(x, y, 4.5, ORG) + lbl(x + 8, y - 8, nm, ORG, 14, "start", "700")
    b += lbl(W[0] + 4, W[1] + 24, "dây", "currentColor", 13, "start", "400")
    b += dim(p, "b", W[0], W[1] + 60, W[0] + 30, W[1] + 60, "", 0, 0) + lbl(W[0] + 34, W[1] + 66, "2 cm", BLUE, 12, "start", "700")
    b += dim(p, "b", W[0] - 90, W[1] + 90, W[0], W[1] + 90, "6 cm", W[0] - 62, W[1] + 106, "start")
    b += lbl(16, 14, "Đề cho: dòng điện ra phía người nhìn", "currentColor", 13, "start", "700")
    b += lbl(16, 30, "Hỏi: chiều từ trường tại A, B, C", ORG, 13, "start", "700")
    return fig("d2-2", VB, "Mặt cắt dây thẳng với dòng điện hướng ra phía người nhìn và ba điểm A, B, C cách dây 2 cm, 2 cm, 6 cm", b, "Dữ kiện: mặt cắt vuông góc dây, A và B cách dây 2 cm, C cách dây 6 cm. " + NOTE)

# ───────────── Dạng 3: la bàn dưới dây, đảo chiều dòng ─────────────
C3 = (150, 125)

def d3(k):
    p = f"d3{k}"
    cx, cy = C3
    b = defs(p) + (compass(cx, cy) if k == 0 else "")
    if k == 0:
        b += seg(cx, cy - 100, cx, cy + 100, ORG, 5, "", 0.4) + arrow(p, "o", cx, cy + 92, cx, cy - 92, 3)
        b += needle(cx, cy, damped(-37), 3)
        b += lbl(cx + 10, cy - 100, "I", ORG, 14, "start", "700")
        b += arrow(p, "b", 330, 130, 330, 60, 3) + sub(338, 90, "B", "đ", BLUE, 14) + lbl(338, 108, "= 40 μT", BLUE, 13, "start", "700")
        b += lbl(262, 150, "Dây nằm trên la bàn,", "currentColor", 13, "start", "400") + lbl(262, 168, "dòng nam → bắc", "currentColor", 13, "start", "400")
        b += lbl(262, 196, "Kim lệch 37° về Tây", RED, 13, "start", "700")
        return fig("d3-0", VB, "La bàn nhìn từ trên xuống, dây nằm theo phương bắc nam ngay trên la bàn; khi có dòng điện kim dao động rồi lệch 37 độ về phía tây", b, "Mô phỏng: kim la bàn dao động rồi dừng lệch 37° về Tây khi đóng mạch (nhìn từ trên xuống, bấm Chạy mô phỏng).")
    # k == 2: vectơ
    o = (150, 185)
    b += arrow(p, "b", *o, o[0], o[1] - 120, 3) + sub(o[0] - 10, o[1] - 128, "B", "đ", BLUE, 14, "end")
    b += arrow(p, "o", *o, o[0] - 90, o[1], 3) + sub(o[0] - 96, o[1] - 8, "B", "dây", ORG, 14, "end")
    b += arrow(p, "r", *o, o[0] - 90, o[1] - 120, 3) + lbl(o[0] - 20, o[1] - 70, "B", RED, 15, "start", "700")
    b += seg(o[0] - 90, o[1], o[0] - 90, o[1] - 120, "currentColor", 1.4, "5 4") + seg(o[0], o[1] - 120, o[0] - 90, o[1] - 120, "currentColor", 1.4, "5 4")
    b += arc(*o, 52, 90, 127, RED) + lbl(o[0] + 8, o[1] - 62, "37°", RED, 13, "start", "700")
    b += lbl(250, 70, "Bđ = 40 μT (bắc)", BLUE, 13, "start", "700") + lbl(250, 92, "Bdây = ? (⊥ Bđ)", ORG, 13, "start", "700") + lbl(250, 114, "kim chỉ theo B", RED, 13, "start", "700")
    return fig("d3-2", VB, "Hai từ trường vuông góc: từ trường Trái Đất hướng bắc và từ trường của dây hướng tây; tổng hợp lệch 37 độ so với hướng bắc", b, "Dữ kiện: hai vectơ vuông góc, tổng hợp lệch 37° so với bắc. " + NOTE)

# ───────────── Dạng 4: hai dây, la bàn ở giữa ─────────────
def d4(k):
    p = f"d4{k}"
    cx, cy = C3
    b = defs(p) + (compass(cx, cy) if k == 0 else "")
    if k == 0:
        b += seg(cx - 4, cy - 100, cx - 4, cy + 100, ORG, 5, "", 0.4) + arrow(p, "o", cx - 4, cy + 92, cx - 4, cy - 92, 3)
        b += seg(cx + 4, cy - 100, cx + 4, cy + 100, ORG, 5, "", 0.4) + arrow(p, "o", cx + 4, cy - 92, cx + 4, cy + 92, 3)
        b += needle(cx, cy, damped(-45), 3)
        b += lbl(cx - 8, cy - 102, "(1)", ORG, 13, "end", "700") + lbl(cx + 8, cy - 102, "(2)", ORG, 13, "start", "700")
        b += arrow(p, "b", 330, 130, 330, 60, 3) + sub(338, 90, "B", "đ", BLUE, 14) + lbl(338, 108, "= 40 μT", BLUE, 13, "start", "700")
        b += lbl(262, 150, "(1) trên · (2) dưới la bàn", "currentColor", 13, "start", "400") + lbl(262, 168, "(1) nam → bắc", "currentColor", 13, "start", "400") + lbl(262, 186, "(2) bắc → nam", "currentColor", 13, "start", "400")
        b += lbl(262, 214, "Kim lệch 45° về Tây", RED, 13, "start", "700")
        return fig("d4-0", VB, "La bàn nhìn từ trên xuống giữa hai dây song song theo phương bắc nam, dòng ngược chiều nhau; kim dao động rồi lệch 45 độ về phía tây", b, "Mô phỏng: kim dao động rồi dừng lệch 45° về Tây khi cả hai dây có dòng (nhìn từ trên xuống; dây (1) nằm trên, dây (2) nằm dưới la bàn; bấm Chạy mô phỏng).")
    o = (150, 185)
    b += arrow(p, "b", *o, o[0], o[1] - 120, 3) + sub(o[0] - 10, o[1] - 128, "B", "đ", BLUE, 14, "end")
    b += arrow(p, "o", *o, o[0] - 90, o[1], 3) + sub(o[0] - 96, o[1] - 8, "B", "1", ORG, 14, "end")
    b += arrow(p, "o", o[0] - 90, o[1], o[0] - 120, o[1], 3, "") + sub(o[0] - 126, o[1] + 18, "B", "2", ORG, 14, "end")
    b += arrow(p, "r", *o, o[0] - 120, o[1] - 120, 3) + lbl(o[0] - 36, o[1] - 70, "B", RED, 15, "start", "700")
    b += arc(*o, 52, 90, 135, RED) + lbl(o[0] + 6, o[1] - 62, "45°", RED, 13, "start", "700")
    b += lbl(250, 70, "Bđ = 40 μT (bắc)", BLUE, 13, "start", "700") + lbl(250, 92, "B₁ = 30 μT (dây 1)", ORG, 13, "start", "700") + lbl(250, 114, "B₂ = ? (dây 2)", ORG, 13, "start", "700")
    return fig("d4-2", VB, "Từ trường Trái Đất hướng bắc cộng với từ trường của hai dây; tổng hợp lệch 45 độ về phía tây", b, "Dữ kiện: B₁ hướng tây, tổng hợp lệch 45° về tây. " + NOTE)

BUILD = [d1, d2, d3, d4]

# ───────────── đề ─────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Chiều từ trường và độ mạnh quanh thanh nam châm",
      topic="Đường sức từ và từ phổ",
      problem_html=("<p>Một thanh nam châm thẳng nằm ngang, cực bắc (N) ở bên phải, cực nam (S) ở bên trái. Kim nam châm nhỏ lần lượt đặt tại: "
                    "<strong>M</strong> — phía trên, chính giữa thanh, ngoài thanh; <strong>P</strong> — trên đường thẳng chứa thanh, bên phải cực N, ngoài thanh; "
                    "<strong>Q</strong> — chính giữa, bên trong thanh.</p>"
                    "<p>a) Tại mỗi điểm M, P, Q, từ trường hướng sang trái hay sang phải (đầu N của kim nam châm nhỏ nằm cân bằng chỉ về phía nào)?</p>"
                    "<p>b) Trên hình vẽ đường sức, điểm A gần cực N có đường sức mau, điểm B ở xa có đường sức thưa. Từ trường ở điểm nào mạnh hơn?</p>"
                    "<p>c) Rắc mạt sắt quanh thanh thì thấy các chuỗi hạt cong. Chuỗi hạt đó có phải là đường sức từ không?</p>")),
 dict(label="Dạng 2 · Dễ · Chiều từ trường quanh dây thẳng (nắm tay phải)",
      topic="Từ trường của nam châm và của dòng điện",
      problem_html=("<p>Một dây dẫn thẳng dài đặt vuông góc với mặt phẳng trang giấy, có dòng điện chạy <strong>hướng ra phía người nhìn</strong>. "
                    "Kim nam châm nhỏ đặt tại ba điểm trong mặt phẳng trang giấy: <strong>A</strong> — bên phải dây, cách dây 2 cm; "
                    "<strong>B</strong> — phía trên dây, cách dây 2 cm; <strong>C</strong> — bên trái dây, cách dây 6 cm.</p>"
                    "<p>a) Xác định chiều từ trường tại A, B, C (đầu N của kim chỉ lên, xuống, sang trái hay sang phải).</p>"
                    "<p>b) Đảo chiều dòng điện. Chiều từ trường tại A thay đổi thế nào?</p>"
                    "<p>c) Từ trường tại B hay tại C mạnh hơn? Vì sao?</p>")),
 dict(label="Dạng 3 · Trung bình · La bàn đặt dưới dây: tổng hợp hai từ trường vuông góc",
      topic="Từ trường của nam châm và của dòng điện",
      problem_html=("<p>Một la bàn nằm ngang. Thành phần nằm ngang của từ trường Trái Đất tại đó là $B_{\\text{đ}} = 40\\ \\mu\\text{T}$, hướng bắc. "
                    "Một dây dẫn thẳng dài nằm ngang, đặt theo phương bắc – nam, ngay phía trên la bàn. Khi dòng điện chạy từ nam đến bắc, kim lệch $37^\\circ$ về phía tây. "
                    "Chỉ xét từ trường của dây và của Trái Đất; từ trường của dây tại kim nằm ngang. Lấy $\\tan 37^\\circ \\approx 0{,}754$, $\\cos 37^\\circ \\approx 0{,}799$.</p>"
                    "<p>a) Tính cảm ứng từ $B_{\\text{dây}}$ của dây tại vị trí la bàn.</p>"
                    "<p>b) Tính cảm ứng từ tổng hợp tại vị trí kim.</p>"
                    "<p>c) Đảo chiều dòng điện (độ lớn không đổi). Kim lệch về phía nào, bao nhiêu độ?</p>")),
 dict(label="Dạng 4 · Khó · Hai dây quanh la bàn: chiều từ trường rồi tổng hợp",
      topic="Từ trường của nam châm và của dòng điện",
      problem_html=("<p>Hai dây dẫn thẳng dài, song song, nằm ngang theo phương bắc – nam; dây (1) ngay phía <strong>trên</strong> la bàn, dây (2) ngay phía <strong>dưới</strong> la bàn. "
                    "Thành phần nằm ngang của từ trường Trái Đất là $B_{\\text{đ}} = 40\\ \\mu\\text{T}$ hướng bắc. Khi chỉ dây (1) có dòng chạy từ nam đến bắc thì từ trường của nó tại la bàn là $B_1 = 30\\ \\mu\\text{T}$.</p>"
                    "<p>Cho dòng điện vào cả hai dây: dây (1) chạy từ nam đến bắc, dây (2) chạy từ bắc đến nam, kim lệch $45^\\circ$ về phía tây. Từ trường của mỗi dây tại kim đều nằm ngang.</p>"
                    "<p>a) Xác định chiều từ trường của mỗi dây tại la bàn.</p>"
                    "<p>b) Tính cảm ứng từ $B_2$ của dây (2) tại la bàn.</p>"
                    "<p>c) Đổi chiều dòng điện ở dây (2) (độ lớn không đổi, dây (1) giữ nguyên). Tính cảm ứng từ tổng hợp tại kim và góc lệch của kim; kim lệch về phía nào?</p>")),
]

# ───────────── bảng phân tích đề ─────────────
ANALYSIS = [
 [("\"thanh nam châm thẳng, cực bắc ở bên phải\"", "N bên phải, S bên trái", "⚠ Ngoài thanh, đường sức đi từ cực N sang cực S; trong thanh đi từ S sang N (đường cong kín)"),
  ("\"kim nam châm nhỏ ... nằm cân bằng\"", "Kim đủ nhỏ, đã đứng yên", "Chiều từ trường tại điểm = chiều nam → bắc của kim = hướng đầu N của kim"),
  ("\"M — phía trên, chính giữa thanh\"", "Ngoài thanh, trên đường sức từ N sang S", "Từ trường hướng từ phía cực N sang phía cực S"),
  ("\"P — bên phải cực N\"", "Ngoài thanh, ở phía cực N", "Đường sức từ cực N đi ra xa cực"),
  ("\"Q — bên trong thanh\"", "Trong thanh", "Đường sức khép kín: trong thanh đi từ S sang N"),
  ("\"đường sức mau ... thưa\"", "A mau, B thưa", "Mật độ đường sức biểu diễn độ mạnh: mau → mạnh, thưa → yếu"),
  ("\"chuỗi hạt cong\"", "Từ phổ", "Từ phổ là ảnh thật cho thấy hình dạng; đường sức là đường vẽ theo quy ước")],
 [("\"dây thẳng dài, vuông góc trang giấy\"", "Mặt phẳng trang vuông góc dây", "⚠ Đường sức quanh dây thẳng là các đường tròn đồng tâm nằm trong mặt phẳng vuông góc với dây"),
  ("\"dòng điện hướng ra phía người nhìn\"", "$I$ ra khỏi trang", "Quy tắc nắm tay phải: ngón cái chỉ chiều dòng điện, các ngón khum lại chỉ chiều đường sức"),
  ("\"A bên phải, B phía trên, C bên trái\"", "Ba điểm trên ba hướng khác nhau", "Chiều từ trường là tiếp tuyến của đường tròn tại điểm đó"),
  ("\"xác định chiều từ trường\"", "Cần chiều tại A, B, C", "Đầu N của kim chỉ theo tiếp tuyến"),
  ("\"đảo chiều dòng điện\"", "$I$ vào trang", "Đổi chiều dòng điện thì đổi chiều từ trường"),
  ("\"cách dây 2 cm ... 6 cm\"", "$d_B=2$ cm, $d_C=6$ cm", "Càng xa dây từ trường càng yếu; gần dây đường sức mau")],
 [("\"$B_{\\text{đ}} = 40\\ \\mu\\text{T}$, hướng bắc\"", "$B_{\\text{đ}}=40\\ \\mu\\text{T}$", "Từ trường Trái Đất định hướng kim về phía bắc"),
  ("\"dây ... ngay phía trên la bàn\"", "Từ trường của dây nằm ngang, vuông góc với dây", "⚠ Từ trường dây (hướng tây hoặc đông) vuông góc $B_{\\text{đ}}$ (hướng bắc)"),
  ("\"kim lệch $37^\\circ$ về phía tây\"", "$\\alpha=37^\\circ$", "⚠ Kim chỉ theo từ trường tổng hợp, chỉ xét hai từ trường này"),
  ("\"tính $B_{\\text{dây}}$\"", "Cần $B_{\\text{dây}}$", "Hai vectơ vuông góc: $\\tan\\alpha=\\dfrac{B_{\\text{dây}}}{B_{\\text{đ}}}$"),
  ("\"cảm ứng từ tổng hợp\"", "Cần $B$", "$B=\\sqrt{B_{\\text{đ}}^2+B_{\\text{dây}}^2}$ hoặc $B=\\dfrac{B_{\\text{đ}}}{\\cos\\alpha}$"),
  ("\"đảo chiều dòng điện\"", "Đổi chiều dòng điện", "Đổi chiều dòng thì đổi chiều từ trường của dây; độ lớn không đổi")],
 [("\"dây (1) phía trên, dây (2) phía dưới la bàn\"", "Hai dây ở hai phía của la bàn", "⚠ Quy tắc nắm tay phải dùng riêng cho từng dây; từ trường tổng = vectơ tổng các từ trường"),
  ("\"dây (1) nam → bắc; dây (2) bắc → nam\"", "Hai dòng ngược chiều", "Nắm tay phải cho từng dây; so hai chiều từ trường tại la bàn"),
  ("\"$B_1 = 30\\ \\mu\\text{T}$\"", "$B_1=30\\ \\mu\\text{T}$", "Từ trường của dây (1) tại la bàn"),
  ("\"kim lệch $45^\\circ$ về phía tây\"", "$\\alpha=45^\\circ$", "⚠ Kim chỉ theo tổng hợp: $\\tan\\alpha=\\dfrac{B_{\\text{dây}}}{B_{\\text{đ}}}$ với $B_{\\text{dây}}$ là tổng hai từ trường của dây"),
  ("\"tính $B_2$\"", "Cần $B_2$", "Cộng hay trừ đại số tuỳ hai từ trường cùng chiều hay ngược chiều"),
  ("\"đổi chiều dòng điện ở dây (2)\"", "Đổi chiều $\\vec B_2$", "Xét lại chiều từ trường dây (2), tìm $B_{\\text{dây}}$ rồi tổng hợp với $B_{\\text{đ}}$")],
]

# ───────────── lời giải ─────────────
R1 = ["<strong>Khái niệm:</strong> hướng từ trường tại một điểm là chiều nam → bắc của kim nam châm nhỏ nằm cân bằng tại đó.",
      "<strong>Định luật:</strong> đường sức từ khép kín; ngoài nam châm đi ra từ cực N, vào cực S; trong nam châm đi từ S sang N.",
      "<strong>Quy ước:</strong> đường sức mau thì từ trường mạnh, thưa thì yếu; qua mỗi điểm chỉ một đường sức.",
      "⚠ <strong>Điều kiện:</strong> kim đủ nhỏ, đã nằm cân bằng."]
R2 = ["<strong>Khái niệm:</strong> hướng từ trường tại một điểm là chiều nam → bắc của kim nam châm nhỏ nằm cân bằng tại đó.",
      "<strong>Hình dạng:</strong> đường sức quanh dây thẳng dài là các đường tròn đồng tâm, tâm trên dây.",
      "<strong>Quy tắc nắm tay phải:</strong> ngón cái chỉ chiều dòng điện, các ngón khum lại chỉ chiều đường sức.",
      "⚠ <strong>Điều kiện:</strong> xét điểm trong mặt phẳng vuông góc với dây; càng xa dây từ trường càng yếu."]
R3 = ["<strong>Khái niệm:</strong> cảm ứng từ $B$ đo độ mạnh từ trường, đơn vị tesla; $1\\ \\mu\\text{T}=10^{-6}\\ \\text{T}$.",
      "<strong>Định luật:</strong> từ trường tại một điểm là vectơ tổng của các từ trường thành phần; kim chỉ theo vectơ tổng.",
      "<strong>Hai vectơ vuông góc:</strong> $B=\\sqrt{B_1^2+B_2^2}$ · góc lệch so với $\\vec B_{\\text{đ}}$: $\\tan\\alpha=\\dfrac{B_{\\text{dây}}}{B_{\\text{đ}}}$",
      "⚠ <strong>Điều kiện:</strong> chỉ xét từ trường Trái Đất và từ trường của dây; từ trường dây vuông góc $\\vec B_{\\text{đ}}$."]
R4 = R3 + ["<strong>Quy tắc nắm tay phải</strong> cho từng dây; hai từ trường cùng phương thì cộng hoặc trừ đại số."]

SOLS = [
 sol(R1, [
  ("Tại M (phía trên, ngoài thanh)", [P("M ở ngoài thanh, trên đường sức đi từ cực N sang cực S. Ở chính giữa phía trên, đường sức đi từ phía bên phải (cực N) sang phía bên trái (cực S):"), A("T:Đầu N của kim tại M chỉ <strong>sang trái</strong>.")]),
  ("Tại P (bên phải cực N, ngoài thanh)", [P("Đường sức đi ra từ cực N nên ở phía bên phải cực N chúng đi ra xa cực, hướng sang phải:"), A("T:Đầu N của kim tại P chỉ <strong>sang phải</strong>.")]),
  ("Tại Q (bên trong thanh)", [P("Đường sức khép kín nên trong thanh nó đi tiếp từ cực S sang cực N, tức từ trái sang phải:"), A("T:Từ trường tại Q hướng <strong>sang phải</strong>.")]),
  ("So sánh A và B", [P("Đường sức mau ở A, thưa ở B. Mật độ đường sức biểu diễn độ mạnh của từ trường:"), A("T:Từ trường tại A <strong>mạnh hơn</strong> tại B.")]),
  ("Mạt sắt và đường sức", [P("Mạt sắt xếp thành chuỗi là ảnh thật (từ phổ), cho thấy hình dạng nhưng không cho biết chiều. Đường sức là đường vẽ theo quy ước, có mũi tên chỉ chiều:"), A("T:Chuỗi mạt sắt <strong>không phải</strong> chính là đường sức từ.")])],
  ["a) M: sang trái · P: sang phải · Q: sang phải", "b) Từ trường tại A mạnh hơn tại B", "c) Không: từ phổ chỉ cho thấy hình dạng, đường sức là đường vẽ theo quy ước"],
  "Nhận dạng: đề hỏi <strong>chiều hoặc độ mạnh từ trường quanh nam châm</strong> → ngoài thanh đi từ N sang S, trong thanh đi từ S sang N; mau thì mạnh."),
 sol(R2, [
  ("Xác định chiều đường sức", [P("Dòng điện ra phía người nhìn: để ngón cái chỉ ra phía người nhìn, các ngón khum lại chỉ chiều <strong>ngược chiều kim đồng hồ</strong> khi nhìn từ phía người nhìn."), A("T:Đường sức là các vòng tròn ngược chiều kim đồng hồ.")]),
  ("Chiều từ trường tại A, B, C", [P("Từ trường là tiếp tuyến của vòng tròn, theo chiều ngược kim đồng hồ:"),
                                 P("A (bên phải dây): hướng <strong>lên</strong>."), P("B (phía trên dây): hướng <strong>sang trái</strong>."), P("C (bên trái dây): hướng <strong>xuống</strong>.")]),
  ("Đảo chiều dòng điện", [P("Dòng điện vào trang thì đường sức quay <strong>cùng chiều kim đồng hồ</strong>."), A("T:Tại A, từ trường hướng <strong>xuống</strong> (ngược lại lúc đầu).")]),
  ("So sánh B và C", [P("B cách dây 2 cm, C cách dây 6 cm. Càng xa dây từ trường càng yếu, đường sức càng thưa."), A("T:Từ trường tại B <strong>mạnh hơn</strong> tại C.")])],
  ["a) A: lên · B: sang trái · C: xuống", "b) Tại A, từ trường đổi sang hướng xuống", "c) Tại B mạnh hơn (gần dây hơn)"],
  "Nhận dạng: đề cho <strong>dòng điện thẳng và chiều dòng</strong> → nắm tay phải; chiều từ trường là tiếp tuyến của đường tròn tại điểm đó."),
 sol(R3, [
  ("Chiều từ trường của dây", [P("Dòng nam → bắc, la bàn ở phía dưới dây: nắm tay phải cho từ trường tại la bàn hướng <strong>tây</strong> — vuông góc với $\\vec B_{\\text{đ}}$ (hướng bắc), khớp với đề (kim lệch về tây).")]),
  ("Câu a: $B_{\\text{dây}}$", [P("Hai vectơ vuông góc, kim chỉ theo tổng hợp:"), M(r"\tan\alpha=\dfrac{B_{\text{dây}}}{B_{\text{đ}}}"), M(r"B_{\text{dây}}=B_{\text{đ}}\tan\alpha=40\cdot0{,}754"), A(r"B_{\text{dây}}\approx30{,}2\ \mu\text{T}")]),
  ("Câu b: cảm ứng từ tổng hợp", [M(r"B=\dfrac{B_{\text{đ}}}{\cos\alpha}=\dfrac{40}{0{,}799}"), A(r"B\approx50{,}1\ \mu\text{T}"), P("Kiểm tra bằng căn bậc hai:"), M(r"\sqrt{40^2+30{,}2^2}\approx50{,}1\ \mu\text{T}")]),
  ("Câu c: đảo chiều dòng điện", [P("$\\vec B_{\\text{dây}}$ quay sang hướng đông, độ lớn không đổi nên $\\tan\\alpha'$ vẫn bằng $0{,}754$:"), A("T:Kim lệch <strong>37° về phía đông</strong>, đối xứng với lúc đầu qua phương bắc.")]),
  ("Kiểm tra", [P("$B\\gt B_{\\text{đ}}$ vì có thêm thành phần vuông góc ✓."), P("Đơn vị: tesla (μT) ✓.")])],
  ["a) $B_{\\text{dây}}\\approx30{,}2\\ \\mu\\text{T}$", "b) $B\\approx50{,}1\\ \\mu\\text{T}$", "c) Lệch $37^\\circ$ về phía đông"],
  "Nhận dạng: đề cho <strong>góc lệch của kim</strong> và hai từ trường vuông góc → $\\tan\\alpha=B_{\\text{dây}}/B_{\\text{đ}}$; đảo dòng thì kim lệch đối xứng."),
 sol(R4, [
  ("Câu a: chiều từ trường mỗi dây", [P("Dây (1) trên la bàn, dòng nam → bắc: từ trường tại la bàn hướng <strong>tây</strong>."),
                                      P("Dây (2) dưới la bàn, dòng bắc → nam: từ trường tại la bàn cũng hướng <strong>tây</strong>."),
                                      A("T:Hai dây ở hai phía đối nhau, dòng ngược chiều → từ trường <strong>cùng chiều</strong> (cùng hướng tây).")]),
  ("Câu b: tìm $B_2$", [P("Kim lệch $45^\\circ$, hai từ trường của dây cùng chiều nên cộng đại số:"), M(r"\tan45^\circ=\dfrac{B_1+B_2}{B_{\text{đ}}}=1"), M(r"B_1+B_2=B_{\text{đ}}=40\ \mu\text{T}"), M(r"B_2=40-30"), A(r"B_2=10\ \mu\text{T}")]),
  ("Câu c: đổi chiều dòng ở dây (2)", [P("$\\vec B_2$ quay sang hướng đông, ngược chiều $\\vec B_1$ nên trừ đại số (hướng tây vì $B_1\\gt B_2$):"), M(r"B_{\text{dây}}=B_1-B_2=30-10"), A(r"B_{\text{dây}}=20\ \mu\text{T}\ \ (\text{hướng tây})")]),
  ("Tổng hợp với Trái Đất", [P("$\\vec B_{\\text{dây}}\\perp\\vec B_{\\text{đ}}$ nên:"), M(r"B=\sqrt{40^2+20^2}=\sqrt{2000}"), A(r"B\approx44{,}7\ \mu\text{T}"), M(r"\tan\alpha=\dfrac{20}{40}=0{,}5"), A(r"\alpha\approx26{,}6^\circ\ \ (\text{về phía tây})")]),
  ("Kiểm tra", [P("Dòng ngược nhau thì từ trường dây yếu đi: $20\\lt40$, kim lệch ít hơn ($26{,}6^\\circ\\lt45^\\circ$) ✓.")])],
  ["a) Cả hai dây: từ trường hướng tây", "b) $B_2=10\\ \\mu\\text{T}$", "c) $B\\approx44{,}7\\ \\mu\\text{T}$; kim lệch $\\approx26{,}6^\\circ$ về phía tây"],
  "Nhận dạng: <strong>nhiều dây quanh một điểm</strong> → nắm tay phải cho từng dây, cộng/trừ đại số các từ trường cùng phương, rồi tổng hợp với Trái Đất."),
]

write(J, 10, "Bài 9. Khái niệm từ trường", DANG, BUILD, ANALYSIS, SOLS)
