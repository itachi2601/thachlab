"""Bài tập mẫu bài 129 — Bài 2. Động năng. Thế năng (KHTN 9). Dựng 4 dạng + hình + lời giải + buoc[] → 129.json.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-129.py   (idempotent: ghi lại toàn bộ 129.json, review.checked=false)
Danh sách dạng: scripts/data/bai-tap-mau/129.dang.md. Mọi số liệu tính ở đầu file, có assert. Lấy P = 10m (g ≈ 10) như SGK KHTN 9."""
import json, math, os, sys, re as _re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "129.json")
T74 = "Khái niệm động năng và thế năng trọng trường"
T75 = "Tính động năng, thế năng của một vật"

# ───────────── Số liệu (tính + kiểm) ─────────────
Wd = lambda m, v: 0.5 * m * v * v
Wt = lambda m, h: 10 * m * h
# Dạng 2: ô tô 1,2 tấn, 54 km/h; giảm còn 27 km/h; xe máy 120 kg có 6 000 J
m2, v2kmh = 1200.0, 54.0
v2 = v2kmh / 3.6
W2 = Wd(m2, v2)
W2b = Wd(m2, 27 / 3.6)
m2c, W2c = 120.0, 6000.0
v2c = math.sqrt(2 * W2c / m2c)
assert abs(v2 - 15) < 1e-9 and abs(W2 - 135000) < 1e-6 and abs(W2 / W2b - 4) < 1e-9
assert abs(v2c - 10) < 1e-9 and abs(v2c * 3.6 - 36) < 1e-9
assert abs(Wd(m2, v2kmh) - 1749600) < 1e-3 and abs(0.5 * m2 * v2 - 9000) < 1e-9 and abs(m2 * v2 ** 2 - 270000) < 1e-6   # nhiễu
assert abs(math.sqrt(W2c / m2c) - 7.07) < 0.01 and abs(2 * W2c / m2c - 100) < 1e-9                                    # quên 2 · quên căn
# Dạng 3: thùng sơn 5 kg, sàn tầng 2 cao 3,5 m, mái cao 8 m
m3, h3a, h3m = 5.0, 3.5, 8.0
P3 = 10 * m3
W3a, W3m = Wt(m3, h3a), Wt(m3, h3m)
assert P3 == 50 and W3a == 175 and W3m == 400 and W3m - W3a == 225 and abs(P3 * (h3m - h3a) - 225) < 1e-9
assert m3 * h3a == 17.5 and Wt(m3, h3m + h3a) == 575       # quên 10 · cộng độ cao
# Dạng 4: quả dừa 1,5 kg ở 8 m; tại 3 m có v = 10 m/s
m4, H4, h4, v4 = 1.5, 8.0, 3.0, 10.0
W4t0, W4t, W4d = Wt(m4, H4), Wt(m4, h4), Wd(m4, v4)
assert W4t0 == 120 and W4t == 45 and W4d == 75 and W4t + W4d == W4t0
assert abs(v4 ** 2 - 2 * 10 * (H4 - h4)) < 1e-9            # nhất quán rơi tự do g = 10: v² = 2g(H − h)
assert Wt(m4, H4 - h4) == 75 and m4 * v4 ** 2 == 150 and 0.5 * m4 * v4 == 7.5   # nhiễu: h đo từ ngọn cây · quên ½ · quên bình phương

# ───────────── Hình ─────────────
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'

def subt(x, y, base, idx, rest="", c="currentColor", size=17, anchor="start"):
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">{base}'
            f'<tspan dy="5" font-size="{size - 3}">{idx}</tspan><tspan dy="-5">{rest}</tspan></text>')

def slide(dx, dy, dur):
    return (f'<animateTransform attributeName="transform" type="translate" values="0,0;{dx},{dy}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')

def dimv(x, y1, y2, lab, c=ORG, side="end"):
    b = seg(x, y1, x, y2, c, 2) + chevron(x, y1, 0, y1 - y2, c, 2, 10) + chevron(x, y2, 0, y2 - y1, c, 2, 10)
    b += seg(x - 7, y1, x + 7, y1, c, 1.6) + seg(x - 7, y2, x + 7, y2, c, 1.6)
    return b + lbl(x + (-8 if side == "end" else 8), (y1 + y2) / 2 + 6, lab, c, 17, side, "700")

def bike(x, y):      # y = mặt đường
    g = f'<circle cx="{x}" cy="{y - 14}" r="14" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    g += f'<circle cx="{x + 46}" cy="{y - 14}" r="14" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    g += f'<path d="M{x},{y - 14} L{x + 18},{y - 38} L{x + 40},{y - 38} L{x + 46},{y - 14} M{x + 18},{y - 38} L{x + 24},{y - 14} L{x + 40},{y - 38}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>'
    return g

def plane(x, y):
    return (f'<path d="M{x},{y} L{x + 70},{y} Q{x + 84},{y + 6} {x + 70},{y + 12} L{x},{y + 12} Z M{x + 30},{y + 6} L{x + 46},{y + 30} L{x + 52},{y + 30} L{x + 46},{y + 6} '
            f'M{x + 4},{y} L{x - 4},{y - 14} L{x + 6},{y - 14} L{x + 14},{y}" fill="rgba(56,189,248,.18)" stroke="currentColor" stroke-width="2"/>')

def d1(k):
    if k == 0:
        b = seg(210, 10, 210, 300, "currentColor", 1.2, "5 5", .5) + seg(10, 155, 410, 155, "currentColor", 1.2, "5 5", .5)
        # a) quả táo trên cành
        b += seg(16, 140, 200, 140, "currentColor", 2.4)
        b += f'<path d="M90,140 L90,70 M90,92 L130,62" fill="none" stroke="currentColor" stroke-width="3"/>'
        b += f'<circle cx="60" cy="58" r="30" fill="rgba(52,211,153,.2)" stroke="{GRN}" stroke-width="2"/><circle cx="122" cy="76" r="9" fill="{RED}"/>'
        b += lbl(20, 30, "a)", "currentColor", 18, "start", "700")
        # b) xe đạp chạy trên đường ngang
        b += seg(220, 140, 404, 140, "currentColor", 2.4)
        b += f'<g>{bike(236, 140)}{slide(110, 0, 4.0)}</g>'
        b += lbl(226, 30, "b)", "currentColor", 18, "start", "700")
        # c) máy bay đang bay
        b += f'<g>{plane(30, 214)}{slide(80, -20, 4.0)}</g>' + seg(16, 290, 200, 290, "currentColor", 2.4)
        b += lbl(20, 184, "c)", "currentColor", 18, "start", "700")
        # d) quả bóng nằm yên trên sân
        b += seg(220, 290, 404, 290, "currentColor", 2.4) + f'<circle cx="310" cy="276" r="14" fill="rgba(251,146,60,.35)" stroke="currentColor" stroke-width="2"/>'
        b += lbl(226, 184, "d)", "currentColor", 18, "start", "700")
        b += lbl(300, 232, "nằm yên", "currentColor", 16, "middle", "600")
        return fig("d1-0", "0 0 420 304", "Bốn ô: a quả táo treo trên cành, b xe đạp chạy trên đường nằm ngang, c máy bay đang bay, d quả bóng nằm yên trên sân", b,
                   "Mô phỏng (bấm Chạy mô phỏng): xe đạp và máy bay chuyển động, táo và bóng đứng yên.<br>Mốc: mặt đất.")
    b = f'<rect x="10" y="20" width="195" height="116" rx="10" fill="rgba(248,113,113,.10)" stroke="currentColor" stroke-width="2"/>'
    b += lbl(108, 50, "Đang chuyển động", "currentColor", 17, "middle", "700") + lbl(108, 76, "so với mặt đất?", "currentColor", 17, "middle", "700")
    b += lbl(108, 116, "→ có động năng", RED, 17, "middle", "700")
    b += f'<rect x="215" y="20" width="195" height="116" rx="10" fill="rgba(251,146,60,.12)" stroke="currentColor" stroke-width="2"/>'
    b += lbl(312, 50, "Ở trên cao", "currentColor", 17, "middle", "700") + lbl(312, 76, "so với mặt đất?", "currentColor", 17, "middle", "700")
    b += lbl(312, 116, "→ có thế năng", ORG, 17, "middle", "700")
    b += lbl(210, 168, "⚠ Hỏi riêng từng câu, mỗi vật hai câu", "currentColor", 16, "middle", "700")
    return fig("d1-2", "0 0 420 184", "Hai câu hỏi cho mỗi vật: có đang chuyển động không thì xét động năng, có ở trên cao không thì xét thế năng", b,
               "Dữ kiện: mỗi vật xét hai câu hỏi độc lập.")

def car(x, y):
    g = f'<path d="M{x},{y - 14} L{x},{y - 34} L{x + 16},{y - 34} L{x + 28},{y - 50} L{x + 62},{y - 50} L{x + 76},{y - 34} L{x + 90},{y - 32} L{x + 90},{y - 14} Z" fill="rgba(56,189,248,.2)" stroke="currentColor" stroke-width="2.2"/>'
    g += f'<circle cx="{x + 20}" cy="{y - 12}" r="10" fill="none" stroke="currentColor" stroke-width="2.4"/><circle cx="{x + 70}" cy="{y - 12}" r="10" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    return g

RX0, KPX = 100, 5.0            # mũi xe tại 100 px khi t = 0; 5 px mỗi mét
def d2(k):
    b = seg(10, 160, 410, 160, "currentColor", 2.4)
    for mm in range(0, 61, 15):
        x = RX0 + KPX * mm
        b += seg(x, 160, x, 170, "currentColor", 2) + lbl(x, 190, f"{mm} m", "currentColor", 16, "middle", "600")
    assert RX0 + KPX * 60 <= 410
    if k == 0:
        b += f'<g>{car(RX0 - 90, 160)}{slide(KPX * 60, 0, 60 / v2)}</g>'
        b += lbl(16, 32, "Ô tô 1,2 tấn, 54 km/h", BLUE, 17, "start", "700")
        b += subt(16, 62, it_("W"), "đ", " = ?", RED)
        return fig("d2-0", "0 0 420 204", "Ô tô 1,2 tấn chạy trên đường với tốc độ 54 kilômét mỗi giờ; vạch chia mỗi 15 mét", b,
                   "Mô phỏng (bấm Chạy mô phỏng): xe đi hết 60 m trong 4 s, đúng tốc độ thật.<br>Mỗi giây xe đi 15 m.")
    b += car(RX0 - 90, 160)
    b += lbl(16, 32, "m = 1,2 tấn = ? kg", BLUE, 17, "start", "700")
    b += lbl(16, 62, "v = 54 km/h = ? m/s", BLUE, 17, "start", "700")
    b += lbl(16, 92, "⚠ đổi đơn vị trước khi thế số", RED, 16, "start", "700")
    return fig("d2-2", "0 0 420 204", "Dữ kiện ô tô: khối lượng 1,2 tấn và tốc độ 54 kilômét mỗi giờ cần đổi sang kilôgam và mét trên giây", b,
               "Dữ kiện: tấn ra kg, km/h ra m/s.")

GY3, K3 = 276, 28.0            # mặt đất, px mỗi mét
def y3(h): return GY3 - K3 * h
def d3(k):
    b = seg(10, GY3, 410, GY3, "currentColor", 2.6)
    b += seg(120, y3(h3a), 330, y3(h3a), "currentColor", 3) + seg(120, y3(h3m), 330, y3(h3m), "currentColor", 3)
    b += seg(120, GY3, 120, y3(h3m), "currentColor", 2)
    b += lbl(130, y3(h3a) - 8, "sàn tầng 2", "currentColor", 16, "start", "600") + lbl(130, y3(h3m) - 8, "mái", "currentColor", 16, "start", "600")
    PX = 318
    b += seg(330, y3(h3m), 346, y3(h3m) - 22, "currentColor", 2.4) + f'<circle cx="{PX + 22}" cy="{y3(h3m) - 26:.1f}" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    b += dimv(60, y3(h3a), GY3, "3,5 m", ORG) + dimv(96, y3(h3m), GY3, "8 m", BLUE)
    y0, y1 = y3(h3a) - 26, y3(h3m) - 26        # mép trên thùng: trên sàn tầng 2 → trên mái
    if k == 0:
        b += (f'<line x1="{PX + 15}" y1="{y3(h3m) - 26:.1f}" x2="{PX + 15}" y2="{y0:.1f}" stroke="currentColor" stroke-width="1.6">'
              f'{smil("y2", [y0, y1], 4.5)}</line>')
        b += (f'<rect x="{PX + 2}" y="{y0:.1f}" width="26" height="26" rx="3" fill="rgba(251,146,60,.45)" stroke="currentColor" stroke-width="2">'
              f'{smil("y", [y0, y1], 4.5)}</rect>')
        b += lbl(PX - 8, y3(h3a) + 24, "5 kg", "currentColor", 17, "start", "700")
        b += subt(250, GY3 - 16, it_("W"), "t", " = ?", RED)
        return fig("d3-0", "0 0 420 290", "Thùng sơn 5 kg được kéo bằng ròng rọc từ sàn tầng 2 cao 3,5 mét lên mái cao 8 mét so với mặt đất", b,
                   "Mô phỏng (bấm Chạy mô phỏng): ròng rọc kéo thùng từ sàn tầng 2 lên mái.<br>Hình chạy nhanh hơn thật.")
    b += f'<rect x="{PX + 2}" y="{y0:.1f}" width="26" height="26" rx="3" fill="rgba(251,146,60,.45)" stroke="currentColor" stroke-width="2"/>'
    b += lbl(250, GY3 - 30, "mốc 1: mặt đất", RED, 16, "start", "700")
    b += lbl(250, GY3 - 8, "mốc 2: sàn tầng 2", RED, 16, "start", "700")
    return fig("d3-2", "0 0 420 290", "Độ cao sàn tầng 2 là 3,5 mét và mái là 8 mét, đo từ mặt đất; hai cách chọn mốc là mặt đất hoặc sàn tầng 2", b,
               "Dữ kiện: độ cao ghi trên hình đo từ mặt đất.<br>⚠ Đổi mốc thì đo lại h từ mốc mới.")

GY4, K4, XD = 270, 25.0, 190
def y4(h): return GY4 - K4 * h
def tree():
    g = f'<path d="M150,{GY4} L150,{y4(H4) + 4:.1f}" fill="none" stroke="currentColor" stroke-width="5"/>'
    for a in (-60, -20, 20, 60):
        x2 = 150 + 50 * math.sin(math.radians(a)); yy = y4(H4) + 4 - 26 * math.cos(math.radians(a)) + 18
        g += f'<path d="M150,{y4(H4) + 4:.1f} Q{(150 + x2) / 2:.1f},{yy - 22:.1f} {x2:.1f},{yy:.1f}" fill="none" stroke="{GRN}" stroke-width="3"/>'
    return g
def d4(k):
    b = seg(10, GY4, 410, GY4, "currentColor", 2.6) + tree()
    b += dimv(60, y4(H4), GY4, "8 m", BLUE) + dimv(100, y4(h4), GY4, "3 m", ORG)
    b += seg(110, y4(h4), 330, y4(h4), ORG, 1.4, "5 4", .8)
    if k == 0:
        T = math.sqrt(2 * H4 / 10); N = 12
        pts = [(XD, y4(H4 - 5 * (T * i / N) ** 2) - 9) for i in range(N + 1)]
        b += ball(pts, 0, 3 * T / N)
        b += lbl(XD + 18, y4(H4) + 6, "1,5 kg", "currentColor", 17, "start", "700")
        b += lbl(XD + 18, y4(h4) - 10, "tại đây: v = 10 m/s", RED, 17, "start", "700")
        b += subt(XD + 18, y4(h4) + 22, it_("W"), "đ", " = ?   ", RED) + subt(XD + 112, y4(h4) + 22, it_("W"), "t", " = ?", RED)
        return fig("d4-0", "0 0 420 284", "Quả dừa 1,5 kg rơi từ ngọn cây cao 8 mét; vạch nét đứt ở độ cao 3 mét, tại đó quả có tốc độ 10 mét trên giây", b,
                   "Mô phỏng (bấm Chạy mô phỏng): quả rơi theo đúng quy luật rơi, chạy chậm 3 lần.<br>Mốc: mặt đất.")
    b += dot(XD, y4(H4) - 9, 7, GRN) + dot(XD, y4(h4) - 9, 7, GRN)
    b += lbl(XD + 16, y4(H4) - 4, "A: đứng yên", "currentColor", 17, "start", "700")
    b += lbl(XD + 16, y4(h4) - 16, "B: v = 10 m/s", "currentColor", 17, "start", "700")
    b += lbl(XD + 16, GY4 - 14, "⚠ h đo từ mặt đất", RED, 16, "start", "700")
    return fig("d4-2", "0 0 420 284", "Hai vị trí của quả dừa: A ở ngọn cây cao 8 mét, đứng yên; B ở độ cao 3 mét, tốc độ 10 mét trên giây", b,
               "Dữ kiện: A trên ngọn cây (đứng yên), B cách đất 3 m.")

BUILD = [d1, d2, d3, d4]

# ───────────── Đề ─────────────
DE = [
 dict(label="Dạng 1 · Nhận biết vật có động năng, thế năng", topic=T74,
      problem_html=r"<p>Chọn mốc thế năng ở mặt đất, vật làm mốc của chuyển động là mặt đất. Xét các vật:</p>"
                   r"<p>a) quả táo đang treo trên cành;</p><p>b) xe đạp đang chạy trên đường nằm ngang;</p>"
                   r"<p>c) máy bay đang bay;</p><p>d) quả bóng nằm yên trên sân.</p>"
                   r"<p>Mỗi vật có động năng, thế năng, cả hai hay không có dạng nào? Giải thích.</p>"),
 dict(label="Dạng 2 · Tính động năng có đổi đơn vị; tìm tốc độ từ động năng", topic=T75,
      problem_html=r"<p>Một ô tô khối lượng $1{,}2$ tấn chạy trên đường với tốc độ $54\ \text{km/h}$.</p>"
                   r"<ol type=\"a\"><li>Tính động năng của ô tô.</li>"
                   r"<li>Ô tô giảm tốc còn $27\ \text{km/h}$. Động năng giảm đi mấy lần?</li>"
                   r"<li>Một xe máy cùng người lái có tổng khối lượng $120\ \text{kg}$ và động năng $6\,000\ \text{J}$. Tính tốc độ của xe máy, ra $\text{km/h}$.</li></ol>"),
 dict(label="Dạng 3 · Tính thế năng trọng trường khi đổi mốc", topic=T75,
      problem_html=r"<p>Một thùng sơn khối lượng $5\ \text{kg}$ đặt trên sàn tầng 2, sàn cao $3{,}5\ \text{m}$ so với mặt đất. Người thợ dùng ròng rọc kéo thùng lên mái nhà cao $8\ \text{m}$ so với mặt đất.</p>"
                   r"<ol type=\"a\"><li>Tính thế năng của thùng khi đặt trên sàn tầng 2, chọn mốc ở mặt đất.</li>"
                   r"<li>Tính lại thế năng đó nếu chọn mốc ở sàn tầng 2.</li>"
                   r"<li>Chọn mốc ở mặt đất. Tính thế năng của thùng khi đã lên mái và phần thế năng tăng thêm.</li></ol>"),
 dict(label="Dạng 4 · Vật rơi: động năng và thế năng ở hai vị trí", topic=T75,
      problem_html=r"<p>Một quả dừa khối lượng $1{,}5\ \text{kg}$ đang đứng yên trên ngọn cây cao $8\ \text{m}$ so với mặt đất thì rụng. Khi cách mặt đất $3\ \text{m}$, quả dừa có tốc độ $10\ \text{m/s}$. Chọn mốc thế năng ở mặt đất.</p>"
                   r"<ol type=\"a\"><li>Tính động năng và thế năng của quả dừa lúc còn trên ngọn cây.</li>"
                   r"<li>Tính động năng và thế năng của quả dừa khi cách mặt đất $3\ \text{m}$.</li>"
                   r"<li>So sánh tổng động năng và thế năng ở hai vị trí trên.</li></ol>"),
]
for d_ in DE:
    d_["problem_html"] = d_["problem_html"].replace('\\"', '"')

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [(r"&quot;Chọn mốc thế năng ở mặt đất&quot;", r"$h$ đo từ mặt đất", r"⚠ Vật ở mặt đất thì $h=0$, không có thế năng"),
  (r"&quot;vật làm mốc của chuyển động là mặt đất&quot;", r"$v$ so với mặt đất", r"⚠ Đứng yên so với mặt đất thì $v=0$, không có động năng"),
  (r"&quot;quả táo đang treo trên cành&quot;", r"Đứng yên; ở trên cao", r"Thế năng: vật ở trên cao so với mốc"),
  (r"&quot;xe đạp đang chạy trên đường nằm ngang&quot;", r"Đang chạy; ở mặt đường", r"Động năng: vật đang chuyển động"),
  (r"&quot;máy bay đang bay&quot;", r"Đang chuyển động; ở trên cao", r"Một vật có thể có cả hai dạng"),
  (r"&quot;quả bóng nằm yên trên sân&quot;", r"Đứng yên; ở mặt đất", r"Xét cả hai câu hỏi")],
 [(r"&quot;khối lượng 1,2 tấn&quot;", r"$m=1{,}2\ \text{tấn}$", r"⚠ Đổi ra kg: $1\ \text{tấn}=1\,000\ \text{kg}$"),
  (r"&quot;tốc độ 54 km/h&quot;", r"$v=54\ \text{km/h}$", r"⚠ Đổi ra m/s: chia $3{,}6$"),
  (r"&quot;Tính động năng của ô tô&quot;", r"Cần $W_{\text{đ}}$", r"$W_{\text{đ}}=\dfrac{1}{2}mv^2$"),
  (r"&quot;giảm tốc còn 27 km/h. Động năng giảm đi mấy lần?&quot;", r"Tốc độ giảm một nửa", r"$W_{\text{đ}}$ tỉ lệ với $v^2$"),
  (r"&quot;tổng khối lượng 120 kg và động năng 6&nbsp;000 J&quot;", r"$m=120\ \text{kg}$; $W_{\text{đ}}=6\,000\ \text{J}$", r"Biết $W_{\text{đ}}$, tìm $v$: $v^2=\dfrac{2W_{\text{đ}}}{m}$"),
  (r"&quot;ra km/h&quot;", r"Đổi kết quả", r"m/s nhân $3{,}6$ ra km/h")],
 [(r"&quot;thùng sơn khối lượng 5 kg&quot;", r"$m=5\ \text{kg}$", r"Trọng lượng $P=10m$"),
  (r"&quot;sàn cao 3,5 m so với mặt đất&quot;", r"$h_1=3{,}5\ \text{m}$ (từ mặt đất)", r"$W_{\text{t}}=P\,h$"),
  (r"&quot;chọn mốc ở mặt đất&quot;", r"$h$ đo từ mặt đất", r"⚠ Độ cao luôn đo từ mốc đã chọn"),
  (r"&quot;nếu chọn mốc ở sàn tầng 2&quot;", r"Mốc mới", r"⚠ Thùng nằm đúng mốc thì $h=0$"),
  (r"&quot;mái nhà cao 8 m so với mặt đất&quot;", r"$h_2=8\ \text{m}$", r"$W_{\text{t}}=P\,h_2$"),
  (r"&quot;phần thế năng tăng thêm&quot;", r"Cần hiệu", r"Thế năng sau trừ thế năng trước")],
 [(r"&quot;khối lượng 1,5 kg&quot;", r"$m=1{,}5\ \text{kg}$", r"$P=10m$"),
  (r"&quot;đứng yên trên ngọn cây cao 8 m&quot;", r"$v_A=0$; $h_A=8\ \text{m}$", r"Đứng yên: $W_{\text{đ}}=0$"),
  (r"&quot;Chọn mốc thế năng ở mặt đất&quot;", r"$h$ đo từ mặt đất", r"⚠ Không đo $h$ từ ngọn cây"),
  (r"&quot;cách mặt đất 3 m, … tốc độ 10 m/s&quot;", r"$h_B=3\ \text{m}$; $v_B=10\ \text{m/s}$", r"$W_{\text{đ}}=\dfrac{1}{2}mv^2$; $W_{\text{t}}=10\,m\,h$"),
  (r"&quot;So sánh tổng động năng và thế năng&quot;", r"Cần $W_{\text{đ}}+W_{\text{t}}$ ở A và B", r"Cộng hai dạng ở mỗi vị trí rồi so")],
]

# ───────────── Lời giải ─────────────
SOLS = [
 sol([r"<strong>Khái niệm:</strong> vật đang chuyển động có động năng.", r"Vật ở trên cao so với mốc có thế năng.",
      r"Hai câu hỏi độc lập: một vật có thể có một, cả hai hoặc không dạng nào.",
      r"⚠ <strong>Điều kiện:</strong> chuyển động xét so với mặt đất; độ cao đo từ mốc là mặt đất."], [
  ("Quả táo trên cành", [P("Đứng yên: không có động năng."), P("Ở trên cao: có thế năng."), A("T:Chỉ có thế năng.")]),
  ("Xe đạp trên đường ngang", [P("Đang chạy: có động năng."), P("Ở mặt đất: $h=0$, không có thế năng."), A("T:Chỉ có động năng.")]),
  ("Máy bay đang bay", [P("Đang chuyển động và ở trên cao."), A("T:Có cả động năng lẫn thế năng.")]),
  ("Quả bóng nằm yên trên sân", [P("Đứng yên và ở mặt đất."), A("T:Không có động năng, không có thế năng.")]),
  ("Kiểm tra", [P("Mỗi vật đã trả lời đủ hai câu: chuyển động? trên cao? ✓"), P("Đổi mốc thế năng lên mặt bàn thì kết luận về bóng có thể khác.")])],
  [r"a) Chỉ có thế năng", r"b) Chỉ có động năng", r"c) Có cả hai", r"d) Không có dạng nào"],
  "Nhận dạng: đề hỏi <strong>vật nào có động năng, thế năng</strong> → hỏi riêng: có chuyển động không? có ở trên cao so với mốc không?"),
 sol([r"<strong>Công thức:</strong> $W_{\text{đ}}=\dfrac{1}{2}mv^2$.", r"Đơn vị: $m$ (kg), $v$ (m/s), $W_{\text{đ}}$ (J).",
      r"Đổi: $1\ \text{tấn}=1\,000\ \text{kg}$; km/h chia $3{,}6$ ra m/s.",
      r"Tốc độ gấp $n$ lần thì động năng gấp $n^2$ lần.",
      r"⚠ <strong>Điều kiện:</strong> đổi đơn vị xong mới thế số."], [
  ("Đổi đơn vị", [M(r"m=1{,}2\ \text{tấn}=1\,200\ \text{kg}"), M(r"v=\dfrac{54}{3{,}6}"), A(r"v=15\ \text{m/s}")]),
  ("Động năng của ô tô", [M(r"W_{\text{đ}}=\dfrac{1}{2}mv^2"), M(r"W_{\text{đ}}=\dfrac{1}{2}\cdot1\,200\cdot15^2"), A(r"W_{\text{đ}}=135\,000\ \text{J}")]),
  ("Giảm tốc còn 27 km/h", [P("Tốc độ giảm 2 lần nên $v^2$ giảm $2^2$ lần:"), M(r"W_{\text{đ}}'=\dfrac{1}{2}\cdot1\,200\cdot7{,}5^2=33\,750\ \text{J}"), M(r"\dfrac{135\,000}{33\,750}=4"), A("T:Động năng giảm 4 lần.")]),
  ("Tốc độ của xe máy", [M(r"v^2=\dfrac{2W_{\text{đ}}}{m}=\dfrac{2\cdot6\,000}{120}=100"), M(r"v=10\ \text{m/s}"), M(r"v=10\cdot3{,}6"), A(r"v=36\ \text{km/h}")]),
  ("Kiểm tra", [M(r"\dfrac{1}{2}\cdot120\cdot10^2=6\,000\ \text{J}\ ✓"), P("Đơn vị: kg nhân (m/s)² ra J ✓")])],
  [r"a) $W_{\text{đ}}=135\,000\ \text{J}$", r"b) Giảm 4 lần", r"c) $v=36\ \text{km/h}$"],
  "Nhận dạng: đề cho <strong>tấn, km/h</strong> → đổi ra kg, m/s rồi $W_{\\text{đ}}=\\dfrac{1}{2}mv^2$; biết động năng thì $v=\\sqrt{\\dfrac{2W_{\\text{đ}}}{m}}$."),
 sol([r"<strong>Công thức:</strong> $W_{\text{t}}=P\,h=10\,m\,h$.", r"Đơn vị: $P$ (N), $h$ (m), $W_{\text{t}}$ (J).",
      r"$h$ là độ cao so với <strong>mốc</strong> (gốc thế năng).",
      r"⚠ <strong>Điều kiện:</strong> đổi mốc thì đo lại $h$ từ mốc mới; vật ở đúng mốc có $W_{\text{t}}=0$."], [
  ("Trọng lượng thùng", [M(r"P=10m=10\cdot5"), A(r"P=50\ \text{N}")]),
  ("Thế năng trên sàn tầng 2, mốc mặt đất", [M(r"W_{\text{t1}}=P\,h_1"), M(r"W_{\text{t1}}=50\cdot3{,}5"), A(r"W_{\text{t1}}=175\ \text{J}")]),
  ("Đổi mốc về sàn tầng 2", [P("Thùng nằm đúng mốc nên $h=0$:"), A(r"W_{\text{t1}}'=0")]),
  ("Thế năng trên mái, mốc mặt đất", [M(r"W_{\text{t2}}=P\,h_2"), M(r"W_{\text{t2}}=50\cdot8"), A(r"W_{\text{t2}}=400\ \text{J}")]),
  ("Phần tăng thêm", [M(r"\Delta W_{\text{t}}=W_{\text{t2}}-W_{\text{t1}}"), M(r"\Delta W_{\text{t}}=400-175"), A(r"\Delta W_{\text{t}}=225\ \text{J}")]),
  ("Kiểm tra", [P("Thùng được nâng thêm $8-3{,}5=4{,}5$ m:"), M(r"50\cdot4{,}5=225\ \text{J}\ ✓"), P("Phần tăng thêm không phụ thuộc chọn mốc nào.")])],
  [r"a) $175\ \text{J}$", r"b) $0$", r"c) $400\ \text{J}$; tăng thêm $225\ \text{J}$"],
  "Nhận dạng: đề có <strong>chọn mốc ở …</strong> → đo $h$ từ đúng mốc đó rồi $W_{\\text{t}}=10\\,m\\,h$."),
 sol([r"<strong>Công thức:</strong> $W_{\text{đ}}=\dfrac{1}{2}mv^2$; $W_{\text{t}}=10\,m\,h$.", r"Đứng yên: $W_{\text{đ}}=0$.",
      r"Một vật vừa chuyển động vừa ở trên cao thì có cả hai dạng.",
      r"⚠ <strong>Điều kiện:</strong> mốc thế năng ở mặt đất: $h$ đo từ mặt đất, không đo từ ngọn cây."], [
  ("Trên ngọn cây", [P("Đứng yên: $W_{\\text{đ}A}=0$."), M(r"W_{\text{t}A}=10\cdot1{,}5\cdot8"), A(r"W_{\text{t}A}=120\ \text{J}")]),
  ("Thế năng khi cách đất 3 m", [M(r"W_{\text{t}B}=10\cdot1{,}5\cdot3"), A(r"W_{\text{t}B}=45\ \text{J}")]),
  ("Động năng khi cách đất 3 m", [M(r"W_{\text{đ}B}=\dfrac{1}{2}\cdot1{,}5\cdot10^2"), A(r"W_{\text{đ}B}=75\ \text{J}")]),
  ("So sánh tổng", [M(r"A:\ 0+120=120\ \text{J}"), M(r"B:\ 75+45=120\ \text{J}"), A("T:Tổng ở hai vị trí bằng nhau.")]),
  ("Kiểm tra", [P("Hai tổng cùng $120$ J ✓"), P("Vì sao tổng không đổi: học ở Bài 3. Cơ năng.")])],
  [r"a) $W_{\text{đ}}=0$; $W_{\text{t}}=120\ \text{J}$", r"b) $W_{\text{đ}}=75\ \text{J}$; $W_{\text{t}}=45\ \text{J}$", r"c) Tổng bằng nhau, cùng $120\ \text{J}$"],
  "Nhận dạng: <strong>vật đang rơi, cho độ cao và tốc độ</strong> → tính riêng $W_{\\text{đ}}$, $W_{\\text{t}}$ ở từng vị trí, $h$ đo từ mốc."),
]

# ───────────── Tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>vật nào có động năng, thế năng</b> → hỏi riêng: <b>đang chuyển động?</b> <b>ở trên cao so với mốc?</b>",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Quả táo trên cành", "Quả táo đang treo trên cành có dạng năng lượng nào?",
       loi=r"Hay nghĩ đứng yên là không có năng lượng. Đứng yên chỉ là không có động năng; ở trên cao vẫn có thế năng.",
       lua_chon=[("Chỉ có thế năng", True),
                 ("Không có dạng nào, vì đang đứng yên", r"Đứng yên chỉ loại động năng. Quả táo ở trên cao so với mặt đất nên có thế năng."),
                 ("Có cả hai dạng", r"Quả táo đứng yên so với mặt đất nên không có động năng.")]),
  buoc("Xe đạp trên đường ngang", "Xe đạp đang chạy trên đường nằm ngang có dạng năng lượng nào?",
       loi=r"Hay cho xe đạp có thế năng vì xe có khối lượng. Mốc ở mặt đất, xe ở mặt đường nên h = 0.",
       lua_chon=[("Chỉ có động năng", True),
                 ("Có cả hai dạng", r"Xe ở mặt đường, đúng mốc mặt đất, nên h = 0, không có thế năng."),
                 ("Chỉ có thế năng", r"Xe đang chạy so với mặt đất nên chắc chắn có động năng.")]),
  buoc("Máy bay đang bay", "Máy bay đang bay có dạng năng lượng nào?",
       loi=r"Hay chỉ chọn một dạng. Một vật có thể vừa chuyển động vừa ở trên cao.",
       lua_chon=[("Có cả động năng lẫn thế năng", True),
                 ("Chỉ có động năng", r"Máy bay còn ở trên cao so với mặt đất nên có thêm thế năng."),
                 ("Chỉ có thế năng", r"Máy bay đang chuyển động nên có động năng.")]),
  buoc("Quả bóng nằm yên trên sân", "Quả bóng nằm yên trên sân có dạng năng lượng nào?",
       loi=r"Hay nghĩ vật nào cũng có thế năng. Bóng ở đúng mốc mặt đất nên h = 0, và đứng yên nên v = 0.",
       lua_chon=[("Không có dạng nào", True),
                 ("Chỉ có thế năng", r"Bóng nằm trên mặt sân, đúng mốc, nên h = 0: thế năng bằng 0."),
                 ("Chỉ có động năng", r"Bóng nằm yên so với mặt đất nên v = 0.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>tấn</b>, <b>km/h</b> trong bài động năng → đổi ra kg, m/s rồi mới thế vào $W_{\text{đ}}=\dfrac{1}{2}mv^2$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đổi đơn vị", "Tốc độ ô tô bằng bao nhiêu m/s?", v2, "m/s", 0.1,
       loi=r"Hay giữ nguyên 54 hoặc nhân 3,6. Từ km/h sang m/s phải chia cho 3,6."),
  buoc("Động năng của ô tô", "Động năng của ô tô bằng bao nhiêu?", W2, "J", 500,
       loi=r"Hay quên bình phương tốc độ hoặc quên hệ số một nửa.",
       ke=[(r"Thế m = 1 200 kg, v = 15 m/s vào ½mv²", True),
           (r"Thế m = 1,2 và v = 54 vào ½mv²", r"Chưa đổi đơn vị: kết quả lệch hàng trăm lần."),
           (r"Tính m·v", r"Đó không phải công thức động năng; thiếu bình phương và hệ số ½.")]),
  buoc("Giảm tốc còn 27 km/h", "Động năng giảm đi mấy lần?", 4, "lần", 0.01,
       loi=r"Hay trả lời giảm 2 lần vì tốc độ giảm 2 lần. Động năng tỉ lệ với bình phương tốc độ.",
       ke=[(r"So bình phương tốc độ trước và sau", True),
           (r"So tốc độ trước và sau", r"Động năng tỉ lệ với v², không tỉ lệ với v."),
           (r"So khối lượng trước và sau", r"Khối lượng ô tô không đổi, chỉ tốc độ đổi.")]),
  buoc("Tốc độ của xe máy", "Tốc độ của xe máy bằng bao nhiêu km/h?", 36, "km/h", 0.5,
       loi=r"Hay quên nhân 2 trước khi chia cho m, hoặc quên lấy căn bậc hai, hoặc quên đổi m/s ra km/h.",
       ke=[(r"v = căn bậc hai của 2W/m, rồi nhân 3,6", True),
           (r"v = W/m", r"Bỏ mất hệ số 2 và căn bậc hai: W = ½mv² nên v² = 2W/m."),
           (r"v = căn bậc hai của 2W/m, rồi chia 3,6", r"Từ m/s sang km/h phải nhân 3,6, không chia.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>chọn mốc ở …</b> → đo $h$ từ đúng mốc đó, rồi $W_{\text{t}}=10\,m\,h$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Trọng lượng thùng", "Trọng lượng của thùng bằng bao nhiêu?", P3, "N", 0.5,
       loi=r"Hay dùng thẳng khối lượng 5 làm trọng lượng. Trọng lượng P = 10m tính bằng niutơn."),
  buoc("Thế năng trên sàn tầng 2, mốc mặt đất", "Thế năng của thùng trên sàn tầng 2 (mốc mặt đất) bằng bao nhiêu?", W3a, "J", 1,
       loi=r"Hay nhân khối lượng với độ cao, quên nhân 10.",
       ke=[(r"W = P·h với h = 3,5 m", True),
           (r"W = m·h", r"Thiếu hệ số 10: thế năng là trọng lượng nhân độ cao."),
           (r"W = ½·P·h", r"Hệ số ½ thuộc công thức động năng, thế năng không có.")]),
  buoc("Đổi mốc về sàn tầng 2", "Chọn mốc ở sàn tầng 2, thế năng của thùng trên sàn đó bằng bao nhiêu?", 0, "J", 0.01,
       loi=r"Hay giữ nguyên độ cao 3,5 m. Đổi mốc thì đo lại h từ mốc mới; thùng nằm đúng mốc nên h = 0.",
       ke=[(r"Đo lại h từ sàn tầng 2", True),
           (r"Giữ h = 3,5 m vì thùng không di chuyển", r"Thùng không đổi chỗ nhưng mốc đã đổi, h phải đo từ mốc mới."),
           (r"Lấy h = 8 m", r"8 m là độ cao mái, thùng vẫn đang ở sàn tầng 2.")]),
  buoc("Thế năng trên mái, mốc mặt đất", "Thế năng của thùng trên mái (mốc mặt đất) bằng bao nhiêu?", W3m, "J", 1,
       loi=r"Hay đo h từ sàn tầng 2 dù đề đã quay về mốc mặt đất.",
       ke=[(r"W = P·h với h = 8 m", True),
           (r"W = P·h với h = 8 + 3,5 m", r"8 m đã đo từ mặt đất, không cộng thêm độ cao sàn tầng 2."),
           (r"W = P·h với h = 3,5 m", r"Thùng đã lên mái, độ cao mới là 8 m.")]),
  buoc("Phần tăng thêm", "Thế năng của thùng tăng thêm bao nhiêu?", W3m - W3a, "J", 1,
       loi=r"Hay cộng hai giá trị thay vì trừ. Phần tăng thêm là sau trừ trước.",
       ke=[(r"Lấy thế năng trên mái trừ thế năng trên sàn tầng 2", True),
           (r"Cộng hai thế năng", r"Cộng lại không cho phần tăng thêm."),
           (r"Lấy luôn thế năng trên mái", r"Đó là toàn bộ thế năng ở mái, chưa trừ phần thùng đã có.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vật đang rơi</b>, cho <b>độ cao và tốc độ</b> → tính riêng $W_{\text{đ}}$, $W_{\text{t}}$ ở từng vị trí.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Trên ngọn cây", "Thế năng của quả dừa trên ngọn cây bằng bao nhiêu?", W4t0, "J", 1,
       loi=r"Hay quên nhân 10 (dùng m thay cho P). Thế năng là P·h với P = 10m."),
  buoc("Thế năng khi cách đất 3 m", "Thế năng khi quả cách mặt đất 3 m bằng bao nhiêu?", W4t, "J", 1,
       loi=r"Hay lấy h = 8 − 3 = 5 m (quãng đã rơi). Mốc ở mặt đất nên h là 3 m.",
       ke=[(r"W = 10·m·h với h = 3 m", True),
           (r"W = 10·m·h với h = 5 m", r"5 m là quãng đã rơi, đo từ ngọn cây; mốc là mặt đất nên h = 3 m."),
           (r"Thế năng bằng 0 vì quả đang rơi", r"Đang rơi vẫn ở trên cao so với mặt đất nên vẫn có thế năng.")]),
  buoc("Động năng khi cách đất 3 m", "Động năng khi quả cách mặt đất 3 m bằng bao nhiêu?", W4d, "J", 1,
       loi=r"Hay quên hệ số ½ hoặc quên bình phương tốc độ.",
       ke=[(r"W = ½·m·v² với v = 10 m/s", True),
           (r"W = m·v²", r"Thiếu hệ số ½."),
           (r"W = ½·m·v", r"Thiếu bình phương tốc độ.")]),
  buoc("So sánh tổng", "Tổng động năng và thế năng ở hai vị trí thế nào?",
       loi=r"Hay so riêng từng dạng rồi kết luận ngay. Phải cộng hai dạng ở mỗi vị trí rồi mới so.",
       lua_chon=[("Bằng nhau", True),
                 ("Ở trên cây lớn hơn", r"Cộng lại: trên cây 0 + 120, ở độ cao 3 m là 75 + 45, hai tổng như nhau."),
                 ("Ở độ cao 3 m lớn hơn", r"Cộng lại: 0 + 120 = 120 J, còn 75 + 45 = 120 J. Hai tổng bằng nhau.")],
       ke=[(r"Cộng động năng và thế năng ở mỗi vị trí rồi so", True),
           (r"Chỉ so hai thế năng", r"Đề hỏi tổng hai dạng, phải cộng cả động năng."),
           (r"Chỉ so hai động năng", r"Đề hỏi tổng hai dạng, phải cộng cả thế năng.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Ghi JSON ─────────────
d = {"lesson_id": 129, "lesson_title": "Bài 2. Động năng. Thế năng", "generated_at": "2026-10-12",
     "review": {"checked": True, "checked_at": "2026-10-12", "notes": "Soạn 12/10/2026 (chặng 3). Kiểm chéo kiem-code 12/10/2026: không lỗi chặn, đáp số khớp; đã sửa cỡ chỉ số dưới SVG 14, bỏ câu lấn Bài 3 ở dạng 4. Chưa đối chiếu ngân hàng câu hỏi (topic 74/75)."},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DE]}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
assert all(len(s["buoc"]) == SOLS[i].count('class="bt-step"') for i, s in enumerate(STEPS))
inject(J, BUILD, ANALYSIS, SOLS, STEPS)

raw = open(J, encoding="utf8").read()
assert not _re.search(r"\\u000[0-8bcef]|\\t", raw.replace("\\\\t", "")), "ký tự điều khiển trong JSON"
assert "marker-end" not in raw
for q in json.load(open(J))["dang_bai"]:
    for f in ("problem_html", "analysis_html", "solution_html"):
        h_ = _re.sub(r"<svg.*?</svg>", "", q[f], flags=_re.S)
        ms = _re.findall(r"\$\$(.+?)\$\$", h_, flags=_re.S)
        ms += _re.findall(r"\$([^$]+)\$", _re.sub(r"\$\$.+?\$\$", "", h_, flags=_re.S))
        for m in ms:
            assert "<" not in m and ">" not in m, (f, m)
    assert len(_re.findall(r"<svg", q["problem_html"])) == 1
    for s_ in _re.findall(r"<svg.*?</svg>", q["problem_html"] + q["analysis_html"], flags=_re.S):
        assert len(s_) < 6500, len(s_)
print("xong 129.json")
