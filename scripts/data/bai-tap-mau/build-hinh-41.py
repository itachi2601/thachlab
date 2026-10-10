"""Bài tập mẫu Bài 22 "Cường độ dòng điện" (Vật lí 11) — lesson_id 41. 5 dạng (quét: ket-qua/41.quet-dang.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-41.py   (idempotent) → 41.json (review.checked=false cho tới khi kiểm chéo)."""
import json, os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

J = os.path.join(HERE, "41.json")
TOP_A = "Định nghĩa cường độ dòng điện và mật độ dòng"
TOP_B = "Liên hệ cường độ dòng điện với chuyển động hạt tải điện"
NOTE = "Hình minh hoạ định tính, không đúng tỉ lệ."
GREY = "#94a3b8"

# ═════════════ TỰ GIẢI LẠI SỐ LIỆU (độc lập với lời giải) ═════════════
e = 1.6e-19; n = 8.5e28
# D2
assert abs(0.40 * 50 - 20) < 1e-9 and abs(20 / e - 1.25e20) / 1.25e20 < 1e-9 and abs(32 / 0.40 - 80) < 1e-9
# D3
_I = 0.150; _t = 36 * 60; _q = _I * _t
assert _t == 2160 and abs(_q - 324) < 1e-9 and abs(_q / 3.6 - 90) < 1e-9 and abs(_q / 3.6 / 300 * 100 - 30) < 1e-9
assert abs(150 * 36 / 60 - 90) < 1e-9
# D4
_S1 = 2.5e-6; _S2 = 1.0e-6
_s1 = _S1 * n * e; _s2 = _S2 * n * e
assert abs(_s1 - 3.4e4) < 1e-6 and abs(_s2 - 1.36e4) < 1e-6
_v1 = 10 / _s1; _v2 = 10 / _s2
assert abs(_v1 * 1e3 - 0.2941) < 1e-3 and abs(_v2 * 1e3 - 0.7353) < 1e-3 and abs(_v2 / _v1 - 2.5) < 1e-9
# D5
_S = 6.0e-6; _I5 = 2700 / (1.5 * 60); _N5 = 2700 / e
assert abs(_I5 - 30) < 1e-9 and abs(_N5 / 1e22 - 1.6875) < 1e-9
_v5 = _I5 / (_S * n * e); _j5 = _I5 / _S
assert abs(_v5 * 1e3 - 0.3676) < 1e-3 and abs(_j5 - 5e6) < 1 and abs(n * _v5 * e - _j5) / _j5 < 1e-9
# phương án nhiễu phải khác đáp án đúng
assert 0.40 / 50 != 20 and 0.40 * 32 != 80 and 0.15 * 36 != 324 and 324 * 3.6 != 90
assert abs(300 - 90) != 30 and abs(324 / 300 * 100 - 30) > 1


# ═════════════ TIỆN ÍCH VẼ ═════════════
def rect(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def mover(x, y, dx, dur, r=4.5, c=BLUE):
    """Electron: chạy MỘT lần khi bấm, dịch đoạn dx (âm = sang trái), dừng ở khung cuối."""
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" fill-opacity=".85" stroke="{c}" stroke-width="1">'
            f'{smil("cx", [x, x + dx], dur)}</circle>')

def static_dot(x, y, r=4.5, c=BLUE):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" fill-opacity=".85" stroke="{c}" stroke-width="1"/>'


# ───────────── Dạng 1 · khái niệm (mô phỏng: ampe kế kim dao động; hình dữ kiện: đồ thị I theo t) ─────────────
def d1(kk):
    p = f"d1{kk}"
    if kk == 0:
        cx, cy, r = 130, 150, 92
        b = f'<path d="M{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
        for v in range(0, 9):
            th = math.radians(v / 8 * 180)
            x1, y1 = cx - r * math.cos(th), cy - r * math.sin(th)
            x2, y2 = cx - (r - 10) * math.cos(th), cy - (r - 10) * math.sin(th)
            b += seg(x1, y1, x2, y2, "currentColor", 2)
            if v % 2 == 0:
                lx, ly = cx - (r - 24) * math.cos(th), cy - (r - 24) * math.sin(th)
                b += lbl(lx, ly + 4, str(v), "currentColor", 12, "middle", "600")
        vals = [2, 6, 3, 5.5, 2.5, 6, 4]
        angs = [v / 8 * 180 for v in vals]
        vs = ";".join(f"{a:.1f} {cx} {cy}" for a in angs)
        b += (f'<line x1="{cx}" y1="{cy}" x2="{cx - r + 14}" y2="{cy}" stroke="{RED}" stroke-width="3" '
              f'transform="rotate({angs[0]:.1f} {cx} {cy})">'
              f'<animateTransform attributeName="transform" type="rotate" values="{vs}" dur="7s" begin="indefinite" fill="freeze"/></line>')
        b += dot(cx, cy, 6, "currentColor") + lbl(cx, cy + 30, "A", "currentColor", 18, "middle", "700")
        b += lbl(cx, cy + 50, "ampe kế kim (A)", GREY, 12, "middle", "600")
        b += lbl(262, 70, "Kim dao động", "currentColor", 13) + lbl(262, 90, "trong khoảng 2 A đến 6 A", "currentColor", 13)
        b += lbl(262, 118, "Không lùi về phía", "currentColor", 13) + lbl(262, 138, "âm của vạch 0", "currentColor", 13)
        return fig("d1-0", "0 0 420 210", "Ampe kế kim dao động trong khoảng 2 A đến 6 A, không qua vạch 0", b,
                   "Mô phỏng: kim ampe kế khi nạp ắc quy, dao động trong khoảng đề cho. " + NOTE)
    # đồ thị I(t)
    ox, oy = 70, 160
    b = arrow(p, "g", ox, oy, 390, oy, 2) + arrow(p, "g", ox, oy, ox, 20, 2)
    b += lbl(396, oy + 5, "t", GRN, 13) + lbl(ox + 6, 22, "I (A)", GRN, 13)
    for v in (2, 4, 6):
        y = oy - v * 20
        b += seg(ox - 4, y, ox + 4, y, "currentColor", 1.5) + lbl(ox - 8, y + 4, str(v), "currentColor", 12, "end", "600")
    b += lbl(ox - 8, oy + 4, "0", "currentColor", 12, "end", "600")
    pts = [(ox + 10 + 330 * u / 60, oy - (4 + 2 * math.sin(2 * math.pi * 3.2 * u / 60 + 0.6) * (0.8 + 0.2 * math.cos(u / 5))) * 20) for u in range(61)]
    assert all(oy - 6.01 * 20 <= y <= oy - 1.99 * 20 for _, y in pts)
    b += poly(pts, ORG, 2.4)
    b += lbl(ox + 150, oy + 24, "thời gian nạp", "currentColor", 12, "middle", "600")
    return fig("d1-2", "0 0 420 196", "Đồ thị cường độ dòng nạp theo thời gian dao động trong khoảng 2 A đến 6 A, nằm trên trục thời gian", b,
               "Dữ kiện: cường độ dòng nạp theo thời gian, luôn nằm một phía của trục t. " + NOTE)


# ───────────── Dạng 2 · I, Δq, Δt, N (mô phỏng: electron trôi qua tiết diện; I = 0,40 A) ─────────────
def tube_h(x0, x1, yc, h, c="currentColor"):
    return seg(x0, yc - h / 2, x1, yc - h / 2, c, 2.4) + seg(x0, yc + h / 2, x1, yc + h / 2, c, 2.4)

def d2(kk):
    p = f"d2{kk}"
    yc, h = 110, 70
    b = tube_h(62, 404, yc, h)
    b += circ_a(40, yc)
    b += seg(210, yc - h / 2 - 8, 210, yc + h / 2 + 8, GRN, 2.4, "5 4")
    b += lbl(210, yc + h / 2 + 26, "tiết diện thẳng", GRN, 12, "middle", "600")
    b += arrow(p, "r", 270, 40, 330, 40, 2.4) + lbl(262, 45, "I", RED, 14, "end", "700") + lbl(338, 45, "chiều dòng", RED, 12, "start", "600")
    b += lbl(40, yc - 30, "I = 0,40 A", "currentColor", 13, "middle", "700")
    rows = [yc - 20, yc, yc + 20]
    xs = [130 + 36 * k for k in range(8)]
    if kk == 0:
        for i, x in enumerate(xs):
            for j, y in enumerate(rows):
                if (i + j) % 2 == 0:
                    b += mover(x, y, -60, 5.0)
        b += lbl(300, 196, "electron trôi ngược chiều dòng điện", BLUE, 12, "middle", "600")
        return fig("d2-0", "0 0 420 206", "Các electron trôi dọc dây qua tiết diện thẳng, ampe kế chỉ 0,40 A", b,
                   "Mô phỏng: electron trôi qua tiết diện thẳng khi dòng không đổi. " + NOTE)
    for i, x in enumerate(xs):
        for j, y in enumerate(rows):
            if (i + j) % 2 == 0:
                b += static_dot(x, y)
    b += lbl(140, 26, "Δt = 50 s ; Δq = ? ; N = ?", ORG, 13, "start", "700")
    b += lbl(210, 196, "Câu c: Δq' = 32 C ; Δt' = ?", ORG, 13, "middle", "700")
    return fig("d2-2", "0 0 420 206", "Dây dẫn có dòng 0,40 A; các đại lượng cần tìm là điện lượng, số electron và thời gian", b,
               "Dữ kiện: dòng không đổi 0,40 A ; các đại lượng cần tìm ghi bằng dấu ?. " + NOTE)

def circ_a(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="18" fill="none" stroke="currentColor" stroke-width="2.2"/>'
            + lbl(x, y + 6, "A", "currentColor", 17, "middle", "700"))


# ───────────── Dạng 3 · đổi đơn vị (mô phỏng: đồng hồ bấm giờ + đồng hồ USB) ─────────────
def d3(kk):
    p = f"d3{kk}"
    if kk == 0:
        cx, cy, r = 105, 105, 70
        b = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
        for m in range(0, 60, 5):
            ph = math.radians(m * 6)
            b += seg(cx + (r - 9) * math.sin(ph), cy - (r - 9) * math.cos(ph), cx + r * math.sin(ph), cy - r * math.cos(ph), "currentColor", 2)
            if m % 15 == 0:
                b += lbl(cx + (r + 14) * math.sin(ph), cy - (r + 14) * math.cos(ph) + 4, str(m), "currentColor", 12, "middle", "600")
        b += (f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r + 12}" stroke="{RED}" stroke-width="3.2" transform="rotate(0 {cx} {cy})">'
              f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};{36 * 6} {cx} {cy}" dur="6s" begin="indefinite" fill="freeze"/></line>')
        b += dot(cx, cy, 5, "currentColor") + lbl(cx, cy + 36, "phút", GREY, 12, "middle", "600")
        b += rect(232, 52, 160, 78, "currentColor", 2.2, rx=8)
        b += lbl(312, 90, "150 mA", "currentColor", 22, "middle", "700") + lbl(312, 112, "dòng không đổi", "currentColor", 12, "middle", "600")
        b += lbl(312, 44, "đồng hồ USB", GREY, 12, "middle", "600")
        b += lbl(312, 152, "đầu ra 5 V", GREY, 12, "middle", "400")
        b += lbl(312, 182, "Δq = ?", ORG, 14, "middle", "700")
        return fig("d3-0", "0 0 420 206", "Kim phút của đồng hồ bấm giờ quay đến vạch 36 trong khi đồng hồ USB chỉ 150 mA", b,
                   "Mô phỏng: kim phút quay từ vạch 0 đến hết thời gian sạc ; chạy nhanh hơn thực tế nhiều lần. " + NOTE)
    ox, oy = 70, 150
    b = arrow(p, "g", ox, oy, 350, oy, 2) + arrow(p, "g", ox, oy, ox, 24, 2)
    b += lbl(356, oy + 5, "t (phút)", GRN, 12) + lbl(ox + 6, 24, "I (mA)", GRN, 13)
    yI = oy - 100; xt = ox + 210
    b += rect(ox, yI, xt - ox, oy - yI, ORG, 2, ORG, 0, "", 0.18)
    b += seg(ox, yI, xt, yI, ORG, 2.6) + seg(xt, yI, xt, oy, "currentColor", 1.6, "4 4")
    b += lbl(ox - 8, yI + 4, "150", "currentColor", 12, "end", "700") + lbl(xt, oy + 18, "36", "currentColor", 12, "middle", "700")
    b += lbl(ox - 8, oy + 4, "0", "currentColor", 12, "end", "600")
    b += lbl((ox + xt) / 2, (yI + oy) / 2 + 5, "Δq = ?", ORG, 15, "middle", "700")
    b += lbl(xt + 12, yI + 4, "đầu ra 5 V", GREY, 12, "start", "400")
    return fig("d3-2", "0 0 420 186", "Đồ thị cường độ dòng 150 mA không đổi trong 36 phút, phần diện tích dưới đồ thị là điện lượng", b,
               "Dữ kiện: dòng không đổi 150 mA trong 36 phút ; phần tô là điện lượng cần tìm. " + NOTE)


# ───────────── Dạng 4 · I = Snve (mô phỏng: hai đoạn dây nối tiếp, cùng I) ─────────────
def d4(kk):
    p = f"d4{kk}"
    yc = 100
    h1, h2 = 64, 42
    b = tube_h(26, 212, yc, h1) + tube_h(212, 396, yc, h2) + seg(212, yc - h1 / 2, 212, yc - h2 / 2, "currentColor", 2.4) + seg(212, yc + h1 / 2, 212, yc + h2 / 2, "currentColor", 2.4)
    b += seg(120, yc - h1 / 2 - 6, 120, yc + h1 / 2 + 6, GRN, 2, "5 4") + seg(304, yc - h2 / 2 - 6, 304, yc + h2 / 2 + 6, GRN, 2, "5 4")
    b += lbl(120, yc + h1 / 2 + 24, "S₁ = 2,5 mm²", "currentColor", 12, "middle", "700") + lbl(304, yc + h2 / 2 + 24, "S₂ = 1,0 mm²", "currentColor", 12, "middle", "700")
    b += arrow(p, "r", 150, 28, 240, 28, 2.4) + lbl(144, 33, "I = 10 A", RED, 13, "end", "700") + lbl(250, 33, "cùng một dòng", RED, 12, "start", "600")
    rows1 = [yc - 18, yc, yc + 18]; rows2 = [yc - 10, yc + 10]
    d1x = [44 + 30 * k for k in range(6)]; d2x = [292 + 28 * k for k in range(3)]
    if kk == 0:
        for i, x in enumerate(d1x):
            for j, y in enumerate(rows1):
                if (i + j) % 2 == 0:
                    b += mover(x, y, -24, 5.0)
        for i, x in enumerate(d2x):
            for j, y in enumerate(rows2):
                if (i + j) % 2 == 0:
                    b += mover(x, y, -56, 5.0)
        b += lbl(210, 190, "electron trôi ngược chiều dòng điện", BLUE, 12, "middle", "600")
        return fig("d4-0", "0 0 420 202", "Hai đoạn dây đồng tiết diện khác nhau nối tiếp, electron trôi trong mỗi đoạn", b,
                   "Mô phỏng: hai đoạn dây nối tiếp, cùng dòng, electron trôi nhanh hơn ở đoạn dây nhỏ, chỉ so sánh định tính. " + NOTE)
    for x in d1x:
        for j, y in enumerate(rows1):
            b += static_dot(x, y)
    for x in d2x:
        for y in rows2:
            b += static_dot(x, y)
    b += lbl(120, 60, "v₁ = ?", ORG, 14, "middle", "700") + lbl(304, 60, "v₂ = ?", ORG, 14, "middle", "700")
    return fig("d4-2", "0 0 420 202", "Hai đoạn dây đồng nối tiếp mang cùng dòng 10 A, tốc độ trôi trong mỗi đoạn cần tìm", b,
               "Dữ kiện: hai đoạn dây nối tiếp, cùng dòng 10 A ; tốc độ trôi mỗi đoạn là đại lượng cần tìm. " + NOTE)


# ───────────── Dạng 5 · tổng hợp (mô phỏng: chuyển động nhiệt hỗn loạn + trôi chậm) ─────────────
def d5(kk):
    p = f"d5{kk}"
    yc, h = 100, 120
    b = tube_h(30, 400, yc, h)
    ions = [(60 + 46 * i, yc - 36 + 36 * j) for i in range(8) for j in range(3)]
    for ix, iy in ions:
        b += lbl(ix, iy + 4, "+", GREY, 13, "middle", "700")
    b += arrow(p, "r", 150, 26, 240, 26, 2.4) + lbl(142, 31, "I", RED, 14, "end", "700") + lbl(250, 31, "chiều dòng điện", RED, 12, "start", "600")
    b += lbl(210, yc + h / 2 + 22, "S = 6,0 mm²", "currentColor", 12, "middle", "700")
    if kk == 0:
        rnd = random.Random(41)
        starts = [(310, yc - 20), (230, yc + 14), (150, yc - 12), (95, yc + 26)]
        for (x0, y0) in starts:
            xs, ys = [x0], [y0]
            for t in range(24):
                nx = xs[-1] + rnd.uniform(-9, 9) - 0.9
                ny = ys[-1] + rnd.uniform(-9, 9)
                nx = min(max(nx, 44), 392); ny = min(max(ny, yc - h / 2 + 10), yc + h / 2 - 10)
                xs.append(nx); ys.append(ny)
            b += (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="5" fill="{BLUE}" fill-opacity=".85" stroke="{BLUE}" stroke-width="1">'
                  f'{smil("cx", xs, 6)}{smil("cy", ys, 6)}</circle>')
        b += lbl(210, 196, "rung nhiệt hỗn loạn + trôi có hướng rất chậm", BLUE, 12, "middle", "600")
        return fig("d5-0", "0 0 420 206", "Các electron tự do chuyển động nhiệt hỗn loạn giữa các ion dương trong dây đồng", b,
                   "Mô phỏng: electron dao động hỗn loạn, chỉ lệch dần theo một hướng. " + NOTE)
    b += seg(210, yc - h / 2 - 6, 210, yc + h / 2 + 6, GRN, 2.2, "5 4")
    b += lbl(60, 66, "2700 C trong 1,5 phút", ORG, 13, "start", "700")
    b += lbl(60, 90, "I = ?   N = ?", ORG, 13, "start", "700")
    b += lbl(60, 114, "v = ?   j = ?", ORG, 13, "start", "700")
    return fig("d5-2", "0 0 420 206", "Dây đồng tiết diện 6,0 mm² có 2700 C chuyển qua trong 1,5 phút; cần tìm I, N, v và j", b,
               "Dữ kiện: điện lượng và thời gian cho trước ; các đại lượng cần tìm ghi bằng dấu ?. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Khái niệm: cách mắc ampe kế, chiều electron, dòng một chiều và dòng không đổi", topic=TOP_A,
      problem_html=r"""<p>Bộ sạc ắc quy xe máy gồm nguồn một chiều, dây đồng, ampe kế kim và ắc quy cần nạp. Khi nạp, kim ampe kế dao động trong khoảng $2$ A đến $6$ A nhưng luôn nằm ở một phía của vạch $0$, không lùi về phía âm.</p><ol type="a"><li>Ampe kế cần mắc thế nào với ắc quy để đo cường độ dòng nạp?</li><li>Trong dây đồng, các electron tự do trôi theo chiều nào so với chiều dòng điện quy ước?</li><li>Dòng nạp này là dòng không đổi, dòng một chiều hay cả hai?</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Tính điện lượng, số electron và thời gian từ cường độ dòng không đổi", topic=TOP_A,
      problem_html=r"""<p>Một quạt mini USB đang chạy. Ampe kế mắc nối tiếp chỉ $0{,}40$ A và giữ không đổi. Lấy $e=1{,}6\cdot10^{-19}$ C.</p><ol type="a"><li>Trong $50$ s, điện lượng chuyển qua tiết diện thẳng của dây là bao nhiêu?</li><li>Trong khoảng thời gian đó có bao nhiêu electron chuyển qua tiết diện?</li><li>Cần bao lâu để có $32$ C chuyển qua tiết diện đó?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Đổi đơn vị mA, phút, mAh khi tính điện lượng", topic=TOP_A,
      problem_html=r"""<p>Bộ sạc đồng hồ thông minh ghi đầu ra $5$ V. Khi sạc, nó cấp cho đồng hồ dòng điện không đổi $150$ mA trong $36$ phút. Pin của đồng hồ có dung lượng $300$ mAh.</p><ol type="a"><li>Tính điện lượng chuyển qua dây sạc trong $36$ phút, theo đơn vị cu-lông (C).</li><li>Đổi điện lượng đó ra mAh. Biết $1$ mAh $=3{,}6$ C.</li><li>Sau lần sạc này, pin được nạp thêm bao nhiêu phần trăm dung lượng của nó?</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Tốc độ trôi của electron từ $I=Snve$ khi đổi tiết diện", topic=TOP_B,
      problem_html=r"""<p>Dây điện nối bình nước nóng có lõi đồng tiết diện $2{,}5\ \text{mm}^2$, mang dòng điện không đổi $10$ A. Mật độ electron tự do của đồng $n=8{,}5\cdot10^{28}\ \text{m}^{-3}$ ; $e=1{,}6\cdot10^{-19}$ C.</p><ol type="a"><li>Tính tốc độ trôi của electron trong lõi dây, theo mm/s.</li><li>Nối nối tiếp thêm một đoạn dây lõi đồng tiết diện $1{,}0\ \text{mm}^2$ vào cùng mạch, dòng vẫn là $10$ A. Tính tốc độ trôi của electron trong đoạn dây này, theo mm/s.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Bài tổng hợp: cường độ, số electron, tốc độ trôi và mật độ dòng điện", topic=TOP_B,
      problem_html=r"""<p>Dây đồng dẫn điện cho một bếp từ có tiết diện $6{,}0\ \text{mm}^2$. Khi nấu, dòng điện không đổi : trong $1{,}5$ phút có $2700$ C điện lượng chuyển qua tiết diện thẳng của dây. Mật độ electron tự do của đồng $n=8{,}5\cdot10^{28}\ \text{m}^{-3}$ ; $e=1{,}6\cdot10^{-19}$ C.</p><ol type="a"><li>Tính cường độ dòng điện trong dây.</li><li>Có bao nhiêu electron chuyển qua tiết diện đó trong thời gian trên?</li><li>Tính tốc độ trôi của electron trong dây, theo mm/s.</li><li>Tính mật độ dòng điện trong dây, theo A/mm².</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (⚠ chỉ nêu điều kiện; cột 3 không ghi công thức/kết luận) ═════════════
ANALYSIS = [
 [(r'"ampe kế … để đo cường độ dòng nạp"', r"Cần: cách mắc ampe kế", r"⚠ Ampe kế đo dòng chạy qua chính nó, nên vị trí mắc trong mạch quyết định chỉ số"),
  (r'"dây đồng … electron tự do"', r"Hạt tải trong kim loại là electron", r"Chiều dòng điện quy ước ; dấu điện tích của electron"),
  (r'"dao động trong khoảng $2$ A đến $6$ A"', r"$I$ thay đổi giữa hai giá trị", r"Cường độ có đổi theo thời gian hay không"),
  (r'"luôn nằm ở một phía của vạch $0$"', r"Dấu của số chỉ không đổi", r"Chiều dòng có đổi hay không"),
  (r'"dòng không đổi, dòng một chiều hay cả hai"', r"Cần: phân loại dòng", r"⚠ Hai khái niệm khác nhau ở số điều kiện phải thoả, kiểm từng điều kiện")],
 [(r'"ampe kế mắc nối tiếp chỉ $0{,}40$ A, giữ không đổi"', r"$I=0{,}40$ A, không đổi", r"⚠ Dòng không đổi thì cường độ như một hằng số trong mọi khoảng thời gian"),
  (r'"trong $50$ s"', r"$\Delta t=50$ s", r"Thời gian đã tính bằng giây"),
  (r'"điện lượng chuyển qua tiết diện thẳng"', r"Cần: $\Delta q$", r"Định nghĩa cường độ dòng điện"),
  (r'"bao nhiêu electron" ; $e=1{,}6\cdot10^{-19}$ C', r"Cần: $N$ ; $e=1{,}6\cdot10^{-19}$ C", r"Liên hệ giữa điện lượng, số hạt và điện tích mỗi hạt"),
  (r'"$32$ C … bao lâu"', r"$\Delta q'=32$ C ; cần: $\Delta t'$", r"Cùng dòng không đổi như câu a, dùng định nghĩa theo chiều ngược lại")],
 [(r'"đầu ra $5$ V"', r"$U=5$ V", r"⚠ Xét xem đại lượng này có trong định nghĩa cường độ dòng điện hay không"),
  (r'"dòng điện không đổi $150$ mA"', r"$I=150$ mA ; không đổi", r"⚠ Điều kiện: dòng không đổi mới coi cường độ là hằng số trong cả khoảng thời gian. Đơn vị SI của $I$"),
  (r'"trong $36$ phút"', r"$\Delta t=36$ phút", r"Đơn vị thời gian trong hệ SI"),
  (r'"điện lượng … theo đơn vị cu-lông"', r"Cần: $\Delta q$ (C)", r"Định nghĩa cường độ dòng điện"),
  (r'"đổi ra mAh. Biết $1$ mAh $=3{,}6$ C"', r"Hệ số đổi cho trước", r"mAh là đơn vị điện lượng, tích của cường độ (mA) và thời gian (giờ)"),
  (r'"pin … $300$ mAh … bao nhiêu phần trăm"', r"Dung lượng $300$ mAh ; cần: tỉ lệ", r"Tỉ lệ phần trăm là phần so với toàn bộ, hai số phải cùng đơn vị")],
 [(r'"lõi đồng tiết diện $2{,}5\ \text{mm}^2$"', r"$S=2{,}5\ \text{mm}^2$", r"⚠ Đổi $\text{mm}^2$ sang $\text{m}^2$ trước khi thế vào ; dây đồng chất, tiết diện đều"),
  (r'"dòng điện không đổi $10$ A"', r"$I=10$ A", r"Liên hệ cường độ dòng điện với chuyển động hạt tải điện"),
  (r'"$n=8{,}5\cdot10^{28}\ \text{m}^{-3}$ ; $e=1{,}6\cdot10^{-19}$ C"', r"$n$ ; $e$", r"Mật độ hạt tải ; độ lớn điện tích mỗi hạt"),
  (r'"tốc độ trôi của electron … mm/s"', r"Cần: $v_1$ (mm/s)", r"⚠ $v$ là tốc độ trôi trung bình có hướng, khác tốc độ chuyển động nhiệt"),
  (r'"nối tiếp thêm … $1{,}0\ \text{mm}^2$ … dòng vẫn là $10$ A"', r"$S_2=1{,}0\ \text{mm}^2$ ; $I$ như cũ", r"Mạch nối tiếp thì dòng ở mọi tiết diện như nhau"),
  (r'"tốc độ trôi … đoạn dây này"', r"Cần: $v_2$ (mm/s)", r"Cùng $n$, $e$, $I$ : đại lượng nào thay đổi")],
 [(r'"tiết diện $6{,}0\ \text{mm}^2$"', r"$S=6{,}0\ \text{mm}^2$", r"Đổi sang $\text{m}^2$ trong hệ SI"),
  (r'"dòng điện không đổi"', r"Dòng không đổi", r"⚠ Dòng không đổi mới tính $I$ được từ điện lượng và thời gian ; $v$ là tốc độ trôi trung bình, khác chuyển động nhiệt hỗn loạn"),
  (r'"trong $1{,}5$ phút có $2700$ C"', r"$\Delta t=1{,}5$ phút ; $\Delta q=2700$ C", r"Định nghĩa cường độ dòng điện ; đơn vị thời gian trong hệ SI"),
  (r'"$n=8{,}5\cdot10^{28}\ \text{m}^{-3}$ ; $e=1{,}6\cdot10^{-19}$ C"', r"$n$ ; $e$", r"Hạt tải trong kim loại"),
  (r'"bao nhiêu electron"', r"Cần: $N$", r"Liên hệ giữa điện lượng, số hạt và điện tích mỗi hạt"),
  (r'"tốc độ trôi của electron … mm/s"', r"Cần: $v$ (mm/s)", r"Liên hệ cường độ dòng điện với $S$, $n$, $v$, $e$"),
  (r'"mật độ dòng điện … A/mm²"', r"Cần: $j$ (A/mm²)", r"Mật độ dòng điện là cường độ trên một đơn vị tiết diện ; liên hệ với hạt tải")],
]

# ═════════════ LỜI GIẢI + CÁC BƯỚC (tiêu đề dùng chung để khớp 1-1) ═════════════
T1 = ["Cách mắc ampe kế", "Chiều chuyển động của electron", "Phân loại dòng nạp", "Kiểm tra"]
T2 = ["Điện lượng trong 50 s", "Số electron", "Thời gian để có 32 C", "Kiểm tra"]
T3 = ["Đổi đơn vị về SI", "Điện lượng theo cu-lông", "Đổi điện lượng ra mAh", "Phần trăm dung lượng pin", "Kiểm tra"]
T4 = ["Tích S·n·e của lõi 2,5 mm²", "Tốc độ trôi v₁", "Tốc độ trôi v₂ ở đoạn 1,0 mm²", "Kiểm tra"]
T5 = ["Cường độ dòng điện", "Số electron", "Tốc độ trôi", "Mật độ dòng điện", "Kiểm tra"]

R1 = [r"Ampe kế đo dòng chạy qua nó ; mắc <strong>nối tiếp</strong> với đoạn mạch cần đo.",
      r"Chiều dòng điện quy ước là chiều chuyển động của hạt mang điện <strong>dương</strong> ; electron mang điện âm.",
      r"Dòng <strong>một chiều</strong>: chiều không đổi. Dòng <strong>không đổi</strong>: chiều <strong>và</strong> cường độ đều không đổi.",
      r"⚠ Mọi dòng không đổi là dòng một chiều, ngược lại không đúng."]
R2 = [r"$I=\dfrac{\Delta q}{\Delta t}$ ; $1\ \text{A}=1\ \text{C/s}$.",
      r"Điện lượng bằng số hạt nhân điện tích mỗi hạt : $\Delta q=Ne$.",
      r"⚠ Dòng không đổi: $I$ giữ nguyên nên dùng được cho mọi khoảng thời gian."]
R3 = [r"$I=\dfrac{\Delta q}{\Delta t}$, nên $\Delta q=I\,\Delta t$ khi $I$ không đổi.",
      r"⚠ Dùng đơn vị SI: $I$ theo A, $\Delta t$ theo s, $\Delta q$ theo C.",
      r"$1\ \text{mA}=10^{-3}\ \text{A}$ ; $1$ phút $=60$ s ; $1\ \text{mAh}=3{,}6$ C.",
      r"Điện áp $U$ không có mặt trong định nghĩa cường độ dòng điện."]
R4 = [r"$I=S\,n\,v\,e$ ; $S$ (m²), $n$ (m⁻³), $v$ (m/s), $e$ (C).",
      r"Rút ra $v=\dfrac{I}{S\,n\,e}$.",
      r"⚠ Đổi $1\ \text{mm}^2=10^{-6}\ \text{m}^2$ ; $v$ là tốc độ trôi trung bình có hướng.",
      r"Mạch nối tiếp: cường độ như nhau ở mọi tiết diện."]
R5 = [r"$I=\dfrac{\Delta q}{\Delta t}$ ; $\Delta q=Ne$ ; $I=S\,n\,v\,e$.",
      r"Mật độ dòng điện $j=\dfrac{I}{S}=n\,v\,e$ (A/m²).",
      r"⚠ Dòng không đổi mới dùng $I=\Delta q/\Delta t$ cho cả khoảng thời gian ; $v$ là tốc độ trôi, không phải tốc độ nhiệt.",
      r"Đổi sang SI: phút → s ; mm² → m²."]

SOLS = [
 sol(R1, [
  (T1[0], [P(r"Ampe kế đo dòng điện chạy qua chính nó, nên dòng cần đo phải đi vào ampe kế."),
           A(r"T:Mắc ampe kế <strong>nối tiếp</strong> với ắc quy trong mạch nạp."),
           P(r"Mắc song song hoặc nối thẳng hai cực nguồn thì ampe kế (điện trở rất nhỏ) gần như nối tắt nguồn, dòng rất lớn, hỏng dụng cụ.")]),
  (T1[1], [P(r"Chiều quy ước là chiều chuyển động của hạt mang điện dương."),
           P(r"Electron mang điện âm nên bị lực điện kéo ngược chiều điện trường trong dây."),
           A(r"T:Electron trôi <strong>ngược chiều</strong> dòng điện quy ước.")]),
  (T1[2], [P(r"Xét hai điều kiện riêng. Chiều: không đổi (kim luôn ở một phía vạch $0$)."),
           P(r"Cường độ: không đổi hay không (kim dao động từ $2$ A đến $6$ A)."),
           A(r"T:Đây là <strong>dòng một chiều</strong>, <strong>không phải</strong> dòng không đổi.")]),
  (T1[3], [P(r"Dòng không đổi thì chắc chắn là dòng một chiều, nên không thể gọi dòng này là cả hai."),
           P(r"Dòng nạp ắc quy có cường độ thay đổi nhưng chiều giữ nguyên : đúng với dòng một chiều.")])],
  [r"a) Mắc nối tiếp với ắc quy", r"b) Electron trôi ngược chiều dòng điện quy ước", r"c) Dòng một chiều, không phải dòng không đổi"],
  r"Nhận dạng: đề hỏi <strong>cách mắc, chiều electron hoặc loại dòng</strong> → nhớ nối tiếp, chiều quy ước là chiều điện tích dương, và kiểm riêng điều kiện chiều với điều kiện cường độ."),
 sol(R2, [
  (T2[0], [P(r"Từ định nghĩa, rút điện lượng:"), M(r"\Delta q=I\,\Delta t"), M(r"\Delta q=0{,}40\cdot50"), A(r"\Delta q=20\ \text{C}")]),
  (T2[1], [P(r"Điện lượng bằng số electron nhân điện tích mỗi electron:"), M(r"N=\dfrac{\Delta q}{e}"), M(r"N=\dfrac{20}{1{,}6\cdot10^{-19}}"),
           A(r"N=1{,}25\cdot10^{20}\ \text{electron}")]),
  (T2[2], [P(r"Dòng không đổi như câu a, rút thời gian từ định nghĩa:"), M(r"\Delta t'=\dfrac{\Delta q'}{I}"), M(r"\Delta t'=\dfrac{32}{0{,}40}"), A(r"\Delta t'=80\ \text{s}")]),
  (T2[3], [P(r"Đơn vị: $\text{A}\cdot\text{s}=\text{C}$ ; $\text{C}/\text{A}=\text{s}$ ✓."),
           P(r"Điện lượng $32$ C lớn hơn $20$ C nên thời gian cũng lớn hơn $50$ s ✓."),
           P(r"Số electron cỡ $10^{20}$ vì mỗi electron mang điện tích rất nhỏ ✓.")])],
  [r"a) $\Delta q=20$ C", r"b) $N=1{,}25\cdot10^{20}$ electron", r"c) $\Delta t'=80$ s"],
  r"Nhận dạng: đề cho <strong>dòng không đổi</strong> kèm một trong ba đại lượng điện lượng, thời gian hoặc số electron → nối ba đại lượng bằng $I=\Delta q/\Delta t$ và $\Delta q=Ne$."),
 sol(R3, [
  (T3[0], [P(r"Đưa cường độ và thời gian về đơn vị SI:"), M(r"I=150\ \text{mA}=0{,}150\ \text{A}"), M(r"\Delta t=36\cdot60"), A(r"\Delta t=2160\ \text{s}")]),
  (T3[1], [P(r"Dòng không đổi nên điện lượng bằng cường độ nhân thời gian (bỏ qua $U=5$ V, không liên quan):"), M(r"\Delta q=I\,\Delta t"), M(r"\Delta q=0{,}150\cdot2160"),
           A(r"\Delta q=324\ \text{C}")]),
  (T3[2], [P(r"$1$ mAh ứng với $3{,}6$ C, nên số mAh nhỏ hơn số cu-lông:"), M(r"q_{\text{mAh}}=\dfrac{\Delta q}{3{,}6}"), M(r"q_{\text{mAh}}=\dfrac{324}{3{,}6}"),
           A(r"q_{\text{mAh}}=90\ \text{mAh}")]),
  (T3[3], [P(r"Phần trăm là số mAh vừa nạp so với dung lượng, cùng đơn vị mAh:"), M(r"\dfrac{90}{300}\cdot100\%"), A(r"30\ \%")]),
  (T3[4], [P(r"Cách khác: $150\ \text{mA}\cdot\dfrac{36}{60}\ \text{h}=90$ mAh ✓ khớp."),
           P(r"Nếu quên đổi phút, $0{,}150\cdot36=5{,}4$ C, nhỏ vô lí cho một lần sạc."),
           P(r"Số vôn $5$ V không dùng tới ✓.")])],
  [r"a) $\Delta q=324$ C", r"b) $90$ mAh", r"c) $30\ \%$ dung lượng pin"],
  r"Nhận dạng: đề có <strong>mA, phút hoặc mAh</strong> kèm dòng không đổi → đổi hết về A, s, C rồi mới nhân ; số vôn là dữ kiện thừa."),
 sol(R4, [
  (T4[0], [P(r"Đổi tiết diện sang mét vuông, rồi nhân với $n$ và $e$:"), M(r"S_1=2{,}5\ \text{mm}^2=2{,}5\cdot10^{-6}\ \text{m}^2"),
           M(r"S_1\,n\,e=2{,}5\cdot10^{-6}\cdot8{,}5\cdot10^{28}\cdot1{,}6\cdot10^{-19}"), A(r"S_1\,n\,e=3{,}4\cdot10^{4}\ \text{C/m}")]),
  (T4[1], [P(r"Rút $v$ từ $I=S\,n\,v\,e$:"), M(r"v_1=\dfrac{I}{S_1\,n\,e}"), M(r"v_1=\dfrac{10}{3{,}4\cdot10^{4}}\approx2{,}94\cdot10^{-4}\ \text{m/s}"),
           A(r"v_1\approx0{,}294\ \text{mm/s}")]),
  (T4[2], [P(r"Nối tiếp nên $I=10$ A vẫn như cũ ; chỉ đổi tiết diện:"), M(r"S_2\,n\,e=1{,}0\cdot10^{-6}\cdot8{,}5\cdot10^{28}\cdot1{,}6\cdot10^{-19}=1{,}36\cdot10^{4}\ \text{C/m}"),
           M(r"v_2=\dfrac{I}{S_2\,n\,e}=\dfrac{10}{1{,}36\cdot10^{4}}\approx7{,}35\cdot10^{-4}\ \text{m/s}"), A(r"v_2\approx0{,}735\ \text{mm/s}")]),
  (T4[3], [P(r"Cùng $I$, $n$, $e$ nên $v$ tỉ lệ nghịch với $S$:"), M(r"\dfrac{v_2}{v_1}=\dfrac{0{,}735}{0{,}294}\approx2{,}5=\dfrac{S_1}{S_2}\ ✓"),
           P(r"Dây nhỏ hơn thì electron trôi nhanh hơn, giống nước chảy nhanh hơn ở đoạn ống hẹp."),
           P(r"Cả hai đều dưới $1$ mm/s, cùng cỡ với ví dụ trong bài ✓.")])],
  [r"a) $v_1\approx0{,}294$ mm/s", r"b) $v_2\approx0{,}735$ mm/s"],
  r"Nhận dạng: đề hỏi <strong>tốc độ trôi</strong> hoặc đổi <strong>tiết diện</strong> với $n$ cho trước → dùng $v=\dfrac{I}{Sne}$, nhớ đổi mm² sang m²."),
 sol(R5, [
  (T5[0], [P(r"Đổi thời gian ra giây, rồi chia điện lượng cho thời gian:"), M(r"\Delta t=1{,}5\cdot60=90\ \text{s}"), M(r"I=\dfrac{\Delta q}{\Delta t}=\dfrac{2700}{90}"),
           A(r"I=30\ \text{A}")]),
  (T5[1], [P(r"Chia điện lượng cho điện tích mỗi electron:"), M(r"N=\dfrac{\Delta q}{e}=\dfrac{2700}{1{,}6\cdot10^{-19}}"), A(r"N\approx1{,}69\cdot10^{22}\ \text{electron}")]),
  (T5[2], [P(r"Đổi tiết diện sang m², rồi rút $v$ từ $I=S\,n\,v\,e$:"), M(r"S=6{,}0\cdot10^{-6}\ \text{m}^2"),
           M(r"v=\dfrac{I}{S\,n\,e}=\dfrac{30}{6{,}0\cdot10^{-6}\cdot8{,}5\cdot10^{28}\cdot1{,}6\cdot10^{-19}}\approx3{,}68\cdot10^{-4}\ \text{m/s}"),
           A(r"v\approx0{,}368\ \text{mm/s}")]),
  (T5[3], [P(r"Mật độ dòng điện là cường độ trên một đơn vị tiết diện ($1\ \text{mm}^2$):"), M(r"j=\dfrac{I}{S}=\dfrac{30}{6{,}0}"), A(r"j=5{,}0\ \text{A/mm}^2")]),
  (T5[4], [P(r"Kiểm lại bằng $j=nve$:"), M(r"8{,}5\cdot10^{28}\cdot3{,}68\cdot10^{-4}\cdot1{,}6\cdot10^{-19}\approx5{,}0\cdot10^{6}\ \text{A/m}^2=5{,}0\ \text{A/mm}^2\ ✓"),
           P(r"Quên đổi phút ra giây sẽ ra cường độ lớn gấp $60$ lần, vô lí cho một dây dẫn ✓."),
           P(r"Tốc độ trôi dưới $1$ mm/s, cùng cỡ với các ví dụ trong bài ✓.")])],
  [r"a) $I=30$ A", r"b) $N\approx1{,}69\cdot10^{22}$ electron", r"c) $v\approx0{,}368$ mm/s", r"d) $j=5{,}0$ A/mm²"],
  r"Nhận dạng: đề cho <strong>điện lượng, thời gian, tiết diện</strong> rồi hỏi <strong>số electron, tốc độ trôi, mật độ dòng</strong> → đi theo chuỗi $I$ → $N$ → $v$ → $j$, mỗi bước dùng lại kết quả trước."),
]

# ═════════════ CÁC BƯỚC TỰ GIẢI ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>ampe kế</b>, <b>chiều electron</b> hoặc <b>dòng một chiều</b> → nghĩ tới <b>cách mắc, chiều quy ước, điều kiện dòng không đổi</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(T1[0], "Để đo dòng nạp, ampe kế được mắc thế nào so với ắc quy?",
       loi=r"Mắc song song vì thấy hai đầu ampe kế đều nối vào mạch. Ampe kế đo dòng chạy QUA nó, chỉ vôn kế mới mắc song song.",
       lua_chon=[(r"Song song với ắc quy", r"Mắc song song thì dòng không đi qua ampe kế, chỉ số sai, và ampe kế gần như nối tắt hai cực."),
                 (r"Nối tiếp với ắc quy trong mạch nạp", True),
                 (r"Nối thẳng vào hai cực của nguồn", r"Ampe kế gần như không cản dòng, nối thẳng vào nguồn tạo dòng rất lớn, hỏng cả nguồn và ampe kế.")]),
  buoc(T1[1], "Electron tự do trong dây đồng trôi theo chiều nào so với chiều dòng điện quy ước?",
       loi=r"Coi electron trôi cùng chiều dòng điện vì quên rằng chiều quy ước là chiều của điện tích dương.",
       lua_chon=[(r"Cùng chiều dòng điện quy ước", r"Chiều quy ước là chiều của hạt mang điện dương ; electron mang điện âm nên ngược lại."),
                 (r"Không có chiều xác định vì chỉ chuyển động hỗn loạn", r"Ngoài chuyển động nhiệt hỗn loạn, electron còn trôi có hướng ; chính chuyển động có hướng đó tạo ra dòng điện."),
                 (r"Ngược chiều dòng điện quy ước", True)],
       ke=[(r"Chiều quy ước là chiều hạt dương, electron âm nên đi ngược lại", True),
           (r"Electron là hạt tải nên đi cùng chiều dòng điện", r"Electron là hạt tải thật nhưng mang điện âm ; chiều quy ước lấy theo hạt dương nên hai chiều ngược nhau."),
           (r"Lấy chiều từ cực âm sang cực dương của nguồn trong mạch ngoài làm chiều dòng điện", r"Ngoài nguồn, dòng điện quy ước đi từ cực dương qua mạch ngoài về cực âm.")]),
  buoc(T1[2], "Dòng nạp này thuộc loại nào?",
       loi=r"Thấy chiều không đổi thì kết luận ngay là dòng không đổi, bỏ qua điều kiện cường độ.",
       lua_chon=[(r"Dòng không đổi, vì chiều không đổi", r"Dòng không đổi cần cả chiều và cường độ đều không đổi ; ở đây cường độ thay đổi."),
                 (r"Dòng xoay chiều, vì cường độ thay đổi", r"Xoay chiều là chiều đổi qua lại, còn ở đây kim luôn ở một phía vạch $0$."),
                 (r"Dòng một chiều nhưng không phải dòng không đổi", True)],
       ke=[(r"Kiểm riêng điều kiện chiều và điều kiện cường độ", True),
           (r"Chỉ cần kiểm điều kiện chiều", r"Dòng không đổi đòi cả hai điều kiện ; chỉ xét chiều sẽ nhầm hai loại dòng."),
           (r"Chỉ cần kiểm điều kiện cường độ", r"Cường độ thay đổi không đủ để kết luận xoay chiều ; chiều còn quyết định loại dòng.")]),
  buoc(T1[3])]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>điện lượng</b>, <b>thời gian</b> hoặc <b>số electron</b> với dòng không đổi → nghĩ tới <b>Δq = I·Δt</b> và <b>Δq = N·e</b>.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(T2[0], "Điện lượng chuyển qua tiết diện trong $50$ s bằng bao nhiêu?", 20, "C", 0.2,
       loi=r"Chia thay vì nhân ($I/\Delta t$) : đơn vị A/s không phải cu-lông."),
  buoc(T2[1], r"Số electron chuyển qua tiết diện, theo đơn vị $10^{20}$ electron?", 1.25, "×10²⁰ electron", 0.02,
       loi=r"Nhân điện lượng với $e$ thay vì chia, ra số cỡ $10^{-18}$ : số hạt không thể nhỏ hơn $1$.",
       ke=[(r"Chia điện lượng cho điện tích mỗi electron", True),
           (r"Nhân điện lượng với điện tích mỗi electron", r"Phép nhân cho số cỡ $10^{-18}$ ; số hạt không thể nhỏ hơn $1$."),
           (r"Chia điện lượng cho cường độ dòng điện", r"Phép chia này cho một thời gian, không phải số hạt.")]),
  buoc(T2[2], r"Thời gian để $32$ C chuyển qua tiết diện bằng bao nhiêu giây?", 80, "s", 0.8,
       loi=r"Nhân điện lượng với cường độ thay vì chia, ra đơn vị $\text{C}\cdot\text{A}$, không phải giây.",
       ke=[(r"Rút $\Delta t$ từ định nghĩa : chia điện lượng cho cường độ", True),
           (r"Nhân điện lượng với cường độ", r"Phép nhân cho đơn vị $\text{C}\cdot\text{A}$, không phải giây."),
           (r"Chia điện lượng cho điện tích mỗi electron", r"Đó là số hạt, không phải thời gian.")]),
  buoc(T2[3])]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>mA</b>, <b>phút</b> hoặc <b>mAh</b> trong đề → nghĩ tới <b>đổi về A, s, C</b> rồi mới nhân với cường độ.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(T3[0], r"$36$ phút bằng bao nhiêu giây?", 2160, "s", 1,
       loi=r"Quên đổi phút ra giây, hoặc đổi mA ra A theo hệ số sai ($10^{-2}$ thay vì $10^{-3}$)."),
  buoc(T3[1], r"Điện lượng chuyển qua dây sạc trong $36$ phút bằng bao nhiêu cu-lông?", 324, "C", 3,
       loi=r"Nhân thêm $5$ V vào điện lượng, hoặc nhân $150$ với $36$ mà chưa đổi đơn vị.",
       ke=[(r"Nhân cường độ (A) với thời gian (s)", True),
           (r"Nhân $5$ V với thời gian vì đề cho điện áp", r"Điện áp không có trong định nghĩa cường độ dòng điện ; điện lượng chỉ cần cường độ và thời gian."),
           (r"Nhân $150$ với $36$ rồi ghi đơn vị C", r"Chưa đổi mA ra A và phút ra giây nên kết quả không phải số cu-lông.")]),
  buoc(T3[2], "Điện lượng đó bằng bao nhiêu mAh?", 90, "mAh", 1,
       loi=r"Nhân với $3{,}6$ thay vì chia : $1$ mAh lớn hơn $1$ C nên số mAh phải nhỏ hơn số cu-lông.",
       ke=[(r"Chia số cu-lông cho $3{,}6$", True),
           (r"Nhân số cu-lông với $3{,}6$", r"$1$ mAh $=3{,}6$ C nên một lượng cho trước tính bằng mAh phải nhỏ hơn số cu-lông."),
           (r"Chia số cu-lông cho $3600$ rồi ghi luôn đơn vị mAh", r"Chia cho $3600$ được A·h, còn phải nhân $1000$ mới ra mAh.")]),
  buoc(T3[3], "Phần trăm dung lượng pin được nạp thêm?", 30, "%", 0.5,
       loi=r"Lấy số cu-lông chia cho dung lượng của pin (mAh) vì quên hai đại lượng khác đơn vị.",
       ke=[(r"Lấy số mAh vừa nạp chia cho dung lượng của pin", True),
           (r"Lấy số cu-lông chia cho dung lượng của pin (mAh)", r"Hai số khác đơn vị (C và mAh), không so sánh trực tiếp được."),
           (r"Lấy dung lượng của pin trừ số mAh vừa nạp", r"Đó là phần dung lượng còn thiếu, không phải phần đã nạp thêm.")]),
  buoc(T3[4])]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>tốc độ trôi</b>, <b>tiết diện</b> hoặc <b>mật độ electron</b> trong đề → nghĩ tới <b>I = S·n·v·e</b>, rút <b>v = I/(S·n·e)</b>.",
  cap_do=2, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(T4[0], r"Tích $S\,n\,e$ của lõi dây $2{,}5\ \text{mm}^2$ bằng bao nhiêu, theo đơn vị $10^{4}$ C/m?", 3.4, "×10⁴ C/m", 0.05,
       loi=r"Thế thẳng $2{,}5$ vào mà chưa đổi $\text{mm}^2$ sang $\text{m}^2$, kết quả lớn hơn $10^{6}$ lần."),
  buoc(T4[1], r"Tốc độ trôi $v_1$ trong lõi dây bằng bao nhiêu mm/s?", 0.294, "mm/s", 0.005,
       loi=r"Đổi m/s sang mm/s sai hệ số (nhân $100$ hoặc chia $1000$ thay vì nhân $1000$).",
       ke=[(r"Chia cường độ cho tích $S\,n\,e$", True),
           (r"Nhân cường độ với tích $S\,n\,e$", r"Từ $I=S\,n\,v\,e$ phải chia hai vế cho $S\,n\,e$ ; nhân sẽ cho đơn vị không phải m/s."),
           (r"Chia tích $S\,n\,e$ cho cường độ", r"Đó là nghịch đảo : cùng $S$ mà dòng lớn hơn thì $v$ phải lớn hơn, không nhỏ đi.")]),
  buoc(T4[2], r"Tốc độ trôi $v_2$ ở đoạn dây $1{,}0\ \text{mm}^2$ bằng bao nhiêu mm/s?", 0.735, "mm/s", 0.01,
       loi=r"Cho rằng dây nhỏ hơn thì electron trôi chậm hơn, hoặc giữ nguyên $v_1$ vì dòng vẫn như cũ.",
       ke=[(r"Làm lại với $S=1{,}0\ \text{mm}^2$, giữ nguyên $I$, $n$, $e$", True),
           (r"Giữ nguyên $v_1$ vì dòng vẫn như cũ", r"Cùng dòng nhưng tiết diện khác thì $v$ khác : $S$ nằm ở mẫu của $v$."),
           (r"Giảm dòng đi vì dây nhỏ hơn rồi tính lại", r"Hai đoạn nối tiếp nên dòng ở mọi tiết diện như nhau.")]),
  buoc(T4[3])]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>bao nhiêu electron</b>, <b>tốc độ trôi</b> và <b>mật độ dòng điện</b> cùng lúc → nghĩ tới chuỗi <b>I, N, v, j</b>.",
  cap_do=3, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc(T5[0], "Cường độ dòng điện trong dây bằng bao nhiêu ampe?", 30, "A", 0.3,
       loi=r"Quên đổi phút ra giây : chia $2700$ cho $1{,}5$ ra $1800$ A, quá lớn cho một dây dân dụng."),
  buoc(T5[1], r"Số electron chuyển qua tiết diện, theo đơn vị $10^{22}$ electron?", 1.69, "×10²² electron", 0.02,
       loi=r"Nhân điện lượng với $e$ thay vì chia, hoặc dùng cường độ thay điện lượng.",
       ke=[(r"Chia điện lượng cho điện tích mỗi electron", True),
           (r"Chia cường độ dòng điện cho điện tích mỗi electron", r"Đó là số electron qua tiết diện trong mỗi giây, không phải trong cả $1{,}5$ phút."),
           (r"Nhân điện lượng với điện tích mỗi electron", r"Phép nhân cho số cỡ $10^{-16}$ ; số hạt không thể nhỏ hơn $1$.")]),
  buoc(T5[2], r"Tốc độ trôi của electron trong dây bằng bao nhiêu mm/s?", 0.368, "mm/s", 0.005,
       loi=r"Chưa đổi $\text{mm}^2$ sang $\text{m}^2$, hoặc dùng $I=\Delta q/\Delta t$ rồi nhầm với $v$.",
       ke=[(r"Rút $v$ từ $I=S\,n\,v\,e$ với $I$ vừa tìm", True),
           (r"Lấy $v=\dfrac{\Delta q}{\Delta t}$", r"Đó là cường độ dòng điện (C/s), không phải tốc độ trôi (m/s)."),
           (r"Lấy $v=\dfrac{N}{\Delta t}$", r"Đó là số electron qua tiết diện mỗi giây, đơn vị 1/s không phải m/s.")]),
  buoc(T5[3], r"Mật độ dòng điện trong dây bằng bao nhiêu A/mm²?", 5.0, "A/mm²", 0.05,
       loi=r"Chia cường độ cho tiết diện đã đổi sang $\text{m}^2$ nhưng vẫn ghi đơn vị $\text{A/mm}^2$.",
       ke=[(r"Chia cường độ dòng điện cho tiết diện", True),
           (r"Nhân cường độ dòng điện với tiết diện", r"Mật độ dòng là cường độ trên một đơn vị tiết diện, nên phải chia."),
           (r"Chia điện lượng cho tiết diện", r"Điện lượng chia diện tích không cho đại lượng nào của dòng điện đang cần.")]),
  buoc(T5[4])]),
]

# ═════════════ GHI FILE ═════════════
write(J, 41, "Bài 22. Cường độ dòng điện", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["dang_bai"][0]["form"] = "ly_thuyet"   # dạng khái niệm định tính
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code) — đã tự giải lại bằng Python 10/10/2026"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
