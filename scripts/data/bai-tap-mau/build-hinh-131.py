"""Bài tập mẫu bài 131 — Bài 4. Công và công suất (KHTN 9). Dựng 4 dạng + hình + lời giải + buoc[] → 131.json.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-131.py   (idempotent: ghi lại toàn bộ 131.json, review.checked=true)
Danh sách dạng: scripts/data/bai-tap-mau/131.dang.md. Mọi số liệu tính ở đầu file, có assert."""
import json, math, os, sys, re as _re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "131.json")
T78 = "Tính công của một lực"
T79 = "Tính công suất và ý nghĩa của công suất"

# ───────────── Số liệu (tính + kiểm) ─────────────
# Dạng 1: đẩy xe 150 N × 20 m; xe kẹt; nâng thùng 25 kg lên 1,2 m
F1, S1, M1, H1 = 150.0, 20.0, 25.0, 1.2
A1 = F1 * S1
F1n = 10 * M1
A1n = F1n * H1
assert A1 == 3000 and F1n == 250 and abs(A1n - 300) < 1e-9
assert abs(F1 / S1 - A1) > 100 and abs(M1 * H1 - A1n) > 100            # chia F/s (7,5) · lấy kg làm N (30)

# Dạng 2: máy A 3 m³ lên 8 m trong 10 phút; máy B 1,5 m³ lên 8 m trong 4 phút
VA, VB, H2, TA, TB = 3.0, 1.5, 8.0, 600.0, 240.0
AA, AB = 10 * 1000 * VA * H2, 10 * 1000 * VB * H2
PA, PB = AA / TA, AB / TB
assert AA == 240000 and AB == 120000 and PA == 400 and PB == 500 and PB > PA
assert AA / 10 == 24000 and AB / 4 == 30000                                 # chia phút: thứ tự giữ nguyên nhưng sai đơn vị
assert 1000 * VA * H2 == 24000                                               # quên nhân 10

# Dạng 3: xe tải 54 km/h, lực kéo 3 000 N, 10 phút; lên dốc lực kéo 5 000 N, giữ công suất
V3k, F3, T3, F3d = 54.0, 3000.0, 600.0, 5000.0
V3 = V3k / 3.6
S3 = V3 * T3
A3 = F3 * S3
P3 = A3 / T3
V3d = P3 / F3d
assert abs(V3 - 15) < 1e-9 and abs(S3 - 9000) < 1e-9 and abs(A3 - 2.7e7) < 1e-3 and abs(P3 - 45000) < 1e-6
assert abs(F3 * V3 - P3) < 1e-6 and abs(V3d - 9) < 1e-9 and abs(V3d * 3.6 - 32.4) < 1e-9
assert abs(F3 * V3k - P3) > 1e5                                                # quên đổi km/h (162 000)
assert abs(P3 / F3d * 1 - V3d) < 1e-9 and abs(F3d / P3) < 1                    # chia ngược ra số rất nhỏ

# Dạng 4: thang máy 800 kg, tầng 1 → tầng 9 (mỗi tầng 3 m), động cơ 8 kW, H = 80 %
M4, TANG_DEN, HT, P4, H4 = 800.0, 9, 3.0, 8000.0, 0.80
h4 = (TANG_DEN - 1) * HT
F4 = 10 * M4
A4ci = F4 * h4
A4tp = A4ci / H4
t4 = A4tp / P4
v4 = h4 / t4
assert h4 == 24 and F4 == 8000 and A4ci == 192000 and abs(A4tp - 240000) < 1e-6 and abs(t4 - 30) < 1e-9 and abs(v4 - 0.8) < 1e-9
assert abs(A4ci / P4 - t4) > 5 and abs(A4ci * H4 - A4tp) > 1e4                 # bỏ H (24 s) · nhân H (153 600)
assert TANG_DEN * HT == 27                                                       # đếm 9 tầng
assert abs(A4ci / t4 - H4 * P4) < 1e-9 and abs(F4 * v4 - H4 * P4) < 1e-9        # kiểm tra 6 400 W

# ───────────── Hình ─────────────
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'

def subt(x, y, base, idx, rest="", c="currentColor", size=17, anchor="start"):
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">{base}'
            f'<tspan dy="5" font-size="{max(size - 3, 14)}">{idx}</tspan><tspan dy="-5">{rest}</tspan></text>')

def move(dx, dy, dur):
    return (f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx:.1f} {dy:.1f}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def cart(x, y):
    """Xe đẩy hàng: thùng + hai bánh. (x, y) góc trái dưới thân xe."""
    g = f'<rect x="{x}" y="{y - 40}" width="64" height="40" rx="4" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2.4"/>'
    g += f'<circle cx="{x + 14}" cy="{y + 7}" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    g += f'<circle cx="{x + 50}" cy="{y + 7}" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    return g

# Dạng 1
GR1 = 160
def d1(k):
    if k == 0:
        b = seg(16, GR1 + 14, 410, GR1 + 14, "currentColor", 2.4)
        X0, DX = 24, 260
        b += seg(X0 + 32, GR1 + 24, X0 + 32, GR1 + 40, "currentColor", 2) + lbl(X0 + 32, GR1 + 60, "0", "currentColor", 16, "middle", "700")
        b += seg(X0 + 32 + DX, GR1 + 24, X0 + 32 + DX, GR1 + 40, "currentColor", 2) + lbl(X0 + 32 + DX, GR1 + 60, "20 m", "currentColor", 16, "middle", "700")
        g = cart(X0, GR1) + seg(X0 + 64, GR1 - 20, X0 + 120, GR1 - 20, RED, 2.8) + chevron(X0 + 120, GR1 - 20, 1, 0, RED, 2.8, 12)
        g += lbl(X0 + 120, GR1 - 46, it_("F") + " = 150 N", RED, 16, "end", "700")
        b += f'<g>{g}{move(DX, 0, 4.0)}</g>'
        b += lbl(16, 34, "Lực đẩy theo phương ngang", "currentColor", 16, "start", "700")
        b += lbl(16, 60, it_("A") + " = ?", RED, 18, "start", "700")
        return fig("d1-0", "0 0 420 236", "Xe hàng được đẩy bằng lực 150 niutơn theo phương ngang, đi được 20 mét; cần tìm công của lực đẩy", b,
                   "Mô phỏng (bấm Chạy mô phỏng): xe đi 20 m theo hướng lực đẩy.<br>Hình chạy nhanh hơn thật.")
    b = seg(140, 14, 140, 120, "currentColor", 1.2, "5 5", .5) + seg(280, 14, 280, 120, "currentColor", 1.2, "5 5", .5)
    cols = ((16, ("a) đẩy xe", it_("F") + " = 150 N", it_("s") + " = 20 m")),
            (152, ("b) xe kẹt", it_("F") + " = 150 N", "xe đứng yên")),
            (292, ("c) nâng thùng", it_("m") + " = 25 kg", it_("h") + " = 1,2 m")))
    for x, rows in cols:
        for j, r in enumerate(rows):
            b += lbl(x, 40 + 34 * j, r, "currentColor" if j == 0 else BLUE, 16, "start", "700")
    b += lbl(16, 180, "⚠ Chỉ tính quãng đường theo hướng lực", RED, 16, "start", "700")
    return fig("d1-2", "0 0 420 200", "Dữ kiện ba trường hợp: đẩy xe 150 niutơn đi 20 mét; xe kẹt đứng yên; nâng thùng 25 kilôgam lên 1,2 mét", b,
               "Dữ kiện của ba trường hợp a), b), c).")

# Dạng 2: hai bể nước dâng (chạy nhanh hơn thật 120 lần)
def tank(x, top, bot, w, vol_h, dur, anim):
    g = f'<rect x="{x}" y="{top}" width="{w}" height="{bot - top}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    if anim:
        g += (f'<rect x="{x + 3}" y="{bot}" width="{w - 6}" height="0" fill="rgba(56,189,248,.45)">'
              f'{smil("y", [bot, bot - vol_h], dur)}{smil("height", [0, vol_h], dur)}</rect>')
    return g
KV = 40.0                                     # px cho mỗi m³
def d2(k):
    if k == 0:
        TOP, BOT = 50, 190
        b = tank(40, TOP, BOT, 120, KV * VA, TA / 120, True) + tank(250, TOP, BOT, 120, KV * VB, TB / 120, True)
        b += lbl(100, 34, "Máy A", BLUE, 17, "middle", "700") + lbl(310, 34, "Máy B", BLUE, 17, "middle", "700")
        b += lbl(100, 216, "3 m³ · 10 phút", "currentColor", 16, "middle", "700") + lbl(310, 216, "1,5 m³ · 4 phút", "currentColor", 16, "middle", "700")
        b += lbl(16, 250, "Cùng bơm lên bể cao 8 m.", "currentColor", 16, "start", "700")
        b += lbl(300, 250, "Nhanh hơn: ?", RED, 16, "start", "700")
        assert KV * VA < BOT - TOP
        return fig("d2-0", "0 0 420 262", "Hai bể nước: máy A bơm 3 mét khối trong 10 phút, máy B bơm 1,5 mét khối trong 4 phút, cùng lên cao 8 mét", b,
                   "Mô phỏng (bấm Chạy mô phỏng): nước dâng trong hai bể.<br>Hình chạy nhanh hơn thật 120 lần.")
    b = lbl(16, 34, "Khối lượng nước:", "currentColor", 16, "start", "700")
    b += lbl(16, 64, "Máy A: 3 m³ → 3 000 kg", BLUE, 16, "start", "700") + lbl(16, 92, "Máy B: 1,5 m³ → 1 500 kg", BLUE, 16, "start", "700")
    b += lbl(16, 128, "Cùng độ cao: " + it_("h") + " = 8 m", "currentColor", 16, "start", "700")
    b += lbl(16, 166, "⚠ Đổi phút ra giây trước khi chia", RED, 16, "start", "700")
    return fig("d2-2", "0 0 420 182", "Dữ kiện: máy A bơm 3000 kilôgam nước, máy B 1500 kilôgam, cùng lên cao 8 mét", b,
               "Dữ kiện: 1 m³ nước có khối lượng 1 000 kg.")

# Dạng 3: xe tải chạy đều
def truck(x, y):
    g = f'<rect x="{x}" y="{y - 46}" width="78" height="40" rx="3" fill="rgba(56,189,248,.15)" stroke="currentColor" stroke-width="2.2"/>'
    g += f'<path d="M{x + 78},{y - 6} L{x + 78},{y - 36} L{x + 100},{y - 36} L{x + 112},{y - 20} L{x + 112},{y - 6} Z" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2.2"/>'
    g += f'<circle cx="{x + 20}" cy="{y}" r="8" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="{x + 92}" cy="{y}" r="8" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    return g
def d3(k):
    if k == 0:
        GR = 170
        b = seg(10, GR + 8, 412, GR + 8, "currentColor", 2.4)
        g = truck(14, GR) + seg(126, GR - 26, 176, GR - 26, RED, 2.8) + chevron(176, GR - 26, 1, 0, RED, 2.8, 12)
        g += lbl(150, GR - 36, it_("F"), RED, 18, "middle", "700")
        b += f'<g>{g}{move(220, 0, 4.0)}</g>'
        b += lbl(16, 34, "Đường bằng, chạy đều", "currentColor", 16, "start", "700")
        b += lbl(16, 62, it_("v") + " = 54 km/h; " + it_("F") + " = 3 000 N", BLUE, 16, "start", "700")
        b += lbl(16, 90, it_("P") + " = ?", RED, 18, "start", "700")
        return fig("d3-0", "0 0 420 196", "Xe tải chạy đều trên đường bằng với tốc độ 54 kilômét giờ, lực kéo 3000 niutơn; cần tìm công suất", b,
                   "Mô phỏng (bấm Chạy mô phỏng): xe tải chạy đều, lực kéo không đổi.<br>Hình chạy nhanh hơn thật.")
    b = lbl(16, 34, "Đường bằng:", "currentColor", 16, "start", "700")
    b += lbl(16, 62, it_("F") + " = 3 000 N; " + it_("v") + " = 54 km/h", BLUE, 16, "start", "700")
    b += lbl(16, 100, "Lên dốc:", "currentColor", 16, "start", "700")
    b += subt(16, 128, it_("F"), "dốc", " = 5 000 N", BLUE, 16) + subt(220, 128, it_("v"), "dốc", " = ?", RED, 16)
    b += lbl(16, 166, "⚠ Giữ nguyên công suất", RED, 16, "start", "700")
    b += lbl(16, 192, "⚠ Đổi km/h ra m/s: chia 3,6", RED, 16, "start", "700")
    return fig("d3-2", "0 0 420 206", "Dữ kiện: đường bằng lực kéo 3000 niutơn, tốc độ 54 kilômét giờ; lên dốc lực kéo 5000 niutơn, công suất giữ nguyên", b,
               "Dữ kiện: hai đoạn đường, cùng công suất động cơ.")

# Dạng 4: thang máy đi lên đều (tầng 1 → tầng 9)
FY0, DY = 236, 25                            # sàn tầng 1, khoảng cách mỗi tầng trên hình
def d4(k):
    if k == 0:
        b = f'<rect x="150" y="{FY0 - 8 * DY - 30}" width="80" height="{8 * DY + 34}" fill="none" stroke="currentColor" stroke-width="2"/>'
        for n in range(9):
            y = FY0 - n * DY
            b += seg(130, y, 150, y, "currentColor", 2)
            if n in (0, 4, 8):
                b += lbl(124, y + 5, f"tầng {n + 1}", "currentColor", 15, "end", "700")
        CH = 24
        b += (f'<rect x="158" y="{FY0 - CH}" width="64" height="{CH}" rx="3" fill="rgba(251,146,60,.35)" stroke="currentColor" stroke-width="2">'
              f'{smil("y", [FY0 - CH, FY0 - 8 * DY - CH], 6.0)}</rect>')
        b += lbl(250, 60, it_("m") + " = 800 kg", BLUE, 16, "start", "700") + lbl(250, 88, "động cơ 8 kW", BLUE, 16, "start", "700")
        b += lbl(250, 116, "hiệu suất 80 %", BLUE, 16, "start", "700") + lbl(250, 160, it_("t") + " = ?", RED, 18, "start", "700")
        assert FY0 - 8 * DY - CH > 0
        return fig("d4-0", "0 0 420 250", "Thang máy 800 kilôgam đi lên đều từ tầng 1 tới tầng 9; động cơ 8 kilôoát, hiệu suất 80 phần trăm; cần tìm thời gian", b,
                   "Mô phỏng (bấm Chạy mô phỏng): cabin đi lên đều từ tầng 1 tới tầng 9.<br>Hình không đúng thời gian thật.")
    b = '<rect x="16" y="40" width="150" height="60" rx="8" fill="rgba(56,189,248,.12)" stroke="currentColor" stroke-width="2"/>'
    b += lbl(91, 66, "Công động cơ", "currentColor", 16, "middle", "700") + subt(91, 90, it_("A"), "tp", " = ?", RED, 16, "middle")
    b += seg(166, 70, 250, 70, ORG, 2.8) + chevron(250, 70, 1, 0, ORG, 2.8, 13)
    b += lbl(208, 58, "80 %", ORG, 16, "middle", "700")
    b += '<rect x="254" y="40" width="152" height="60" rx="8" fill="rgba(251,146,60,.15)" stroke="currentColor" stroke-width="2"/>'
    b += lbl(330, 66, "Nâng thang", "currentColor", 16, "middle", "700") + subt(330, 90, it_("A"), "có ích", " = ?", RED, 16, "middle")
    b += seg(91, 100, 91, 146, "currentColor", 2.4, "5 4") + chevron(91, 146, 0, 1, "currentColor", 2.4, 12)
    b += lbl(108, 136, "20 % hao phí (ma sát, nóng máy)", "currentColor", 15, "start", "600")
    b += lbl(16, 182, "⚠ Đếm khoảng tầng, không đếm số tầng", RED, 16, "start", "700")
    return fig("d4-2", "0 0 420 196", "Sơ đồ năng lượng: công của động cơ, 80 phần trăm thành công nâng thang, 20 phần trăm hao phí", b,
               "Dữ kiện: chỉ 80 % công của động cơ dùng để nâng thang.")

BUILD = [d1, d2, d3, d4]

# ───────────── Đề ─────────────
DE = [
 dict(label="Dạng 1 · Tính công của lực, khi nào lực không thực hiện công", topic=T78,
      problem_html=r"<p>Một công nhân đẩy xe hàng bằng lực $150\ \text{N}$ theo phương ngang, xe đi được $20\ \text{m}$ theo hướng đẩy.</p>"
                   r"<ol type=\"a\"><li>Tính công của lực đẩy.</li>"
                   r"<li>Sau đó bánh xe kẹt vào ổ gà. Người vẫn đẩy $150\ \text{N}$ nhưng xe không nhúc nhích. Lực đẩy lúc này có thực hiện công không?</li>"
                   r"<li>Người đó nâng đều một thùng hàng $25\ \text{kg}$ từ sàn lên kệ cao $1{,}2\ \text{m}$. Tính công của lực nâng.</li></ol>"),
 dict(label="Dạng 2 · Tính và so sánh công suất của hai máy", topic=T79,
      problem_html=r"<p>Hai máy bơm cùng bơm nước lên một bể chứa đặt cao $8\ \text{m}$.</p>"
                   r"<p>Máy A bơm được $3\ \text{m}^3$ nước trong $10$ phút.</p>"
                   r"<p>Máy B bơm được $1{,}5\ \text{m}^3$ nước trong $4$ phút.</p>"
                   r"<p>Biết $1\ \text{m}^3$ nước có khối lượng $1\,000\ \text{kg}$.</p>"
                   r"<ol type=\"a\"><li>Tính công mỗi máy thực hiện để đưa nước lên bể.</li><li>Tính công suất của mỗi máy.</li>"
                   r"<li>Máy nào làm việc nhanh hơn?</li></ol>"),
 dict(label="Dạng 3 · Công suất và tốc độ: P = F·v", topic=T79,
      problem_html=r"<p>Một xe tải chạy đều trên đường bằng với tốc độ $54\ \text{km/h}$. Lực kéo của động cơ là $3\,000\ \text{N}$.</p>"
                   r"<ol type=\"a\"><li>Tính quãng đường xe đi trong $10$ phút.</li><li>Tính công của lực kéo trong $10$ phút đó.</li>"
                   r"<li>Tính công suất của động cơ.</li>"
                   r"<li>Lên một đoạn dốc, động cơ giữ nguyên công suất, lực kéo tăng lên $5\,000\ \text{N}$. Tính tốc độ của xe trên dốc, ra $\text{km/h}$.</li></ol>"),
 dict(label="Dạng 4 · Tổng hợp: thang máy có hiệu suất, thời gian và tốc độ", topic=T79,
      problem_html=r"<p>Một thang máy chở tổng khối lượng $800\ \text{kg}$ (cả cabin và người) đi lên đều từ tầng 1 tới tầng 9. Mỗi tầng cao $3\ \text{m}$.</p>"
                   r"<p>Động cơ thang máy có công suất $8\ \text{kW}$, hiệu suất $80\ \%$: $80\ \%$ công của động cơ dùng để nâng thang, phần còn lại hao phí.</p>"
                   r"<ol type=\"a\"><li>Tính công nâng thang (công có ích).</li><li>Tính công của động cơ (công toàn phần).</li>"
                   r"<li>Tính thời gian thang đi lên và tốc độ của thang.</li></ol>"),
]
for d_ in DE:
    d_["problem_html"] = d_["problem_html"].replace('\\"', '"')

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [(r"&quot;đẩy xe hàng bằng lực 150&nbsp;N theo phương ngang&quot;", r"$F=150\ \text{N}$", r"Lực tác dụng lên xe"),
  (r"&quot;xe đi được 20&nbsp;m theo hướng đẩy&quot;", r"$s=20\ \text{m}$", r"⚠ Điều kiện: dịch chuyển theo hướng lực thì dùng $A=F\,s$"),
  (r"&quot;Tính công của lực đẩy&quot;", r"Cần $A$", r"$A=F\,s$"),
  (r"&quot;xe không nhúc nhích&quot;", r"Xe đứng yên", r"Có lực nhưng quãng đường bằng bao nhiêu?"),
  (r"&quot;nâng đều một thùng hàng 25&nbsp;kg&quot;", r"$m=25\ \text{kg}$", r"⚠ Nâng đều: lực nâng bằng trọng lượng $10\,m$"),
  (r"&quot;lên kệ cao 1,2&nbsp;m&quot;", r"$h=1{,}2\ \text{m}$", r"Quãng đường theo hướng lực nâng là độ cao"),
  (r"&quot;Tính công của lực nâng&quot;", r"Cần $A$", r"$A=F\,h$")],
 [(r"&quot;bể chứa đặt cao 8&nbsp;m&quot;", r"$h=8\ \text{m}$", r"Quãng đường theo hướng lực nâng nước"),
  (r"&quot;3&nbsp;m³ nước&quot;, &quot;1,5&nbsp;m³ nước&quot;", r"Thể tích nước mỗi máy", r"Khối lượng → trọng lượng $10\,m$"),
  (r"&quot;1&nbsp;m³ nước có khối lượng 1&nbsp;000&nbsp;kg&quot;", r"Đổi thể tích ra khối lượng", r"$m$ (kg) = số m³ × $1\,000$"),
  (r"&quot;trong 10 phút&quot;, &quot;trong 4 phút&quot;", r"Thời gian mỗi máy", r"⚠ Muốn $P$ ra oát: $t$ tính bằng giây"),
  (r"&quot;Tính công suất của mỗi máy&quot;", r"Cần $P_A$, $P_B$", r"$P=\dfrac{A}{t}$"),
  (r"&quot;Máy nào làm việc nhanh hơn?&quot;", r"So sánh", r"⚠ Nhanh hơn là công suất lớn hơn, không phải công lớn hơn")],
 [(r"&quot;chạy đều trên đường bằng&quot;", r"Lực kéo cùng hướng chuyển động", r"⚠ Chạy đều, lực kéo cùng hướng: dùng được $P=F\,v$"),
  (r"&quot;tốc độ 54&nbsp;km/h&quot;", r"$v=54\ \text{km/h}$", r"⚠ Đổi ra m/s: chia cho $3{,}6$"),
  (r"&quot;Lực kéo của động cơ là 3&nbsp;000&nbsp;N&quot;", r"$F=3\,000\ \text{N}$", r"Lực thực hiện công"),
  (r"&quot;quãng đường xe đi trong 10 phút&quot;", r"$t=10$ phút", r"$s=v\,t$ ($v$ m/s, $t$ s)"),
  (r"&quot;Tính công của lực kéo&quot;", r"Cần $A$", r"$A=F\,s$"),
  (r"&quot;Tính công suất của động cơ&quot;", r"Cần $P$", r"$P=\dfrac{A}{t}$ hoặc $P=F\,v$"),
  (r"&quot;giữ nguyên công suất, lực kéo tăng lên 5&nbsp;000&nbsp;N&quot;", r"$P$ không đổi; $F_{\text{dốc}}=5\,000\ \text{N}$", r"$v_{\text{dốc}}=\dfrac{P}{F_{\text{dốc}}}$")],
 [(r"&quot;tổng khối lượng 800&nbsp;kg&quot;", r"$m=800\ \text{kg}$", r"Trọng lượng $10\,m$"),
  (r"&quot;đi lên đều&quot;", r"Lực nâng = trọng lượng", r"⚠ Đều nên lực nâng bằng trọng lượng"),
  (r"&quot;từ tầng 1 tới tầng 9. Mỗi tầng cao 3&nbsp;m&quot;", r"Độ cao $h$", r"⚠ Đếm khoảng tầng giữa hai tầng"),
  (r"&quot;công suất 8&nbsp;kW, hiệu suất 80&nbsp;%&quot;", r"$P=8\,000\ \text{W}$; $H=80\ \%$", r"$H=\dfrac{A_{\text{có ích}}}{A_{\text{tp}}}\cdot100\ \%$"),
  (r"&quot;Tính công nâng thang&quot;", r"Cần $A_{\text{có ích}}$", r"$A=F\,h$"),
  (r"&quot;Tính công của động cơ&quot;", r"Cần $A_{\text{tp}}$", r"$A_{\text{tp}}=\dfrac{A_{\text{có ích}}}{H}$"),
  (r"&quot;thời gian thang đi lên và tốc độ của thang&quot;", r"Cần $t$, $v$", r"$t=\dfrac{A_{\text{tp}}}{P}$; $v=\dfrac{h}{t}$")],
]

# ───────────── Lời giải ─────────────
RA = [r"<strong>Khái niệm:</strong> lực làm vật dịch chuyển theo hướng của lực thì thực hiện công.",
      r"Công thức: $A=F\,s$.",
      r"Nâng đều: lực nâng bằng trọng lượng $10\,m$, quãng đường là độ cao $h$.",
      r"Đơn vị: $F$ (N), $s$ (m), $A$ (J).",
      r"⚠ <strong>Điều kiện:</strong> vật đứng yên hoặc dịch chuyển vuông góc với lực thì $A=0$."]
RP = [r"<strong>Khái niệm:</strong> công suất là công thực hiện trong một đơn vị thời gian.",
      r"Công thức: $P=\dfrac{A}{t}$; công $A=F\,s$.",
      r"Đơn vị: $A$ (J), $t$ (s), $P$ (W).",
      r"⚠ <strong>Điều kiện:</strong> so ai làm nhanh hơn thì so công suất, không so công."]

SOLS = [
 sol(RA, [
  ("Công đẩy xe", [P("Xe đi theo hướng lực đẩy:"), M(r"A_1=F\,s"), M(r"A_1=150\cdot20"), A(r"A_1=3\,000\ \text{J}")]),
  ("Xe bị kẹt", [P("Xe đứng yên: quãng đường $s=0$."), A("T:Lực đẩy không thực hiện công, $A=0$."), P("Người vẫn mỏi vì cơ bắp làm việc bên trong.")]),
  ("Lực nâng thùng", [P("Nâng đều nên lực nâng bằng trọng lượng:"), M(r"F=10\,m"), M(r"F=10\cdot25"), A(r"F=250\ \text{N}")]),
  ("Công nâng thùng", [M(r"A_3=F\,h"), M(r"A_3=250\cdot1{,}2"), A(r"A_3=300\ \text{J}")]),
  ("Kiểm tra", [P("Đơn vị: N nhân m ra J ✓"), P("Nâng thùng nặng hơn lực đẩy nhưng quãng đường ngắn hơn nhiều.<br>Công nhỏ hơn: hợp lí ✓")])],
  [r"a) $A_1=3\,000\ \text{J}$", r"b) Không thực hiện công, $A=0$", r"c) $A_3=300\ \text{J}$"],
  "Nhận dạng: đề cho <strong>lực và quãng đường theo hướng lực</strong> → $A=F\\,s$; <strong>nâng đều</strong> → $F=10\\,m$, $s=h$."),
 sol(RP, [
  ("Công của máy A", [P("Khối lượng nước $3\\,000$ kg, trọng lượng $30\\,000$ N:"), M(r"A_A=F\,h"), M(r"A_A=30\,000\cdot8"), A(r"A_A=240\,000\ \text{J}")]),
  ("Công của máy B", [P("Khối lượng nước $1\\,500$ kg, trọng lượng $15\\,000$ N:"), M(r"A_B=15\,000\cdot8"), A(r"A_B=120\,000\ \text{J}")]),
  ("Công suất máy A", [P("Đổi $10$ phút $=600$ s:"), M(r"P_A=\dfrac{A_A}{t_A}"), M(r"P_A=\dfrac{240\,000}{600}"), A(r"P_A=400\ \text{W}")]),
  ("Công suất máy B", [P("Đổi $4$ phút $=240$ s:"), M(r"P_B=\dfrac{120\,000}{240}"), A(r"P_B=500\ \text{W}")]),
  ("So sánh", [M(r"P_B\gt P_A"), A("T:Máy B làm việc nhanh hơn."), P("Máy A làm được nhiều công hơn, nhưng chậm hơn.")]),
  ("Kiểm tra", [P("Đơn vị: J chia s ra W ✓"), P("Máy B: một nửa lượng nước, chưa tới một nửa thời gian.<br>Nhanh hơn: hợp lí ✓")])],
  [r"a) $A_A=240\,000\ \text{J}$", r"$A_B=120\,000\ \text{J}$", r"b) $P_A=400\ \text{W}$", r"$P_B=500\ \text{W}$", r"c) Máy B nhanh hơn"],
  "Nhận dạng: đề hỏi <strong>máy nào nhanh hơn</strong> → tính $P=\\dfrac{A}{t}$ cho từng máy (t ra giây) rồi so công suất."),
 sol(RP[:3] + [r"Chuyển động đều: $s=v\,t$ nên $P=F\,v$ ($v$ tính bằng m/s).",
               r"⚠ <strong>Điều kiện:</strong> $P=F\,v$ dùng khi lực kéo cùng hướng chuyển động và xe chạy đều."], [
  ("Đổi tốc độ", [M(r"v=\dfrac{54}{3{,}6}"), A(r"v=15\ \text{m/s}")]),
  ("Quãng đường", [P("Đổi $10$ phút $=600$ s:"), M(r"s=v\,t=15\cdot600"), A(r"s=9\,000\ \text{m}")]),
  ("Công của lực kéo", [M(r"A=F\,s"), M(r"A=3\,000\cdot9\,000"), A(r"A=2{,}7\cdot10^7\ \text{J}")]),
  ("Công suất", [M(r"P=\dfrac{A}{t}=\dfrac{2{,}7\cdot10^7}{600}"), A(r"P=45\,000\ \text{W}=45\ \text{kW}")]),
  ("Tốc độ trên dốc", [P("Công suất giữ nguyên:"), M(r"v_{\text{dốc}}=\dfrac{P}{F_{\text{dốc}}}"), M(r"v_{\text{dốc}}=\dfrac{45\,000}{5\,000}=9\ \text{m/s}"), A(r"v_{\text{dốc}}=32{,}4\ \text{km/h}")]),
  ("Kiểm tra", [M(r"P=F\,v=3\,000\cdot15=45\,000\ \text{W}\ ✓"), P("Lên dốc lực kéo lớn hơn thì tốc độ nhỏ hơn.<br>Hợp lí ✓")])],
  [r"a) $s=9\,000\ \text{m}$", r"b) $A=2{,}7\cdot10^7\ \text{J}$", r"c) $P=45\ \text{kW}$", r"d) $v_{\text{dốc}}=32{,}4\ \text{km/h}$"],
  "Nhận dạng: đề cho <strong>chạy đều, lực kéo và tốc độ</strong> → $P=F\\,v$ với $v$ (m/s); <strong>giữ nguyên công suất</strong> → $v=\\dfrac{P}{F}$."),
 sol([r"<strong>Khái niệm:</strong> hiệu suất là phần trăm công của động cơ thành công có ích.", r"Công thức: $A=F\,h$; $H=\dfrac{A_{\text{có ích}}}{A_{\text{tp}}}\cdot100\ \%$.",
      r"Công suất: $P=\dfrac{A_{\text{tp}}}{t}$; tốc độ đều: $v=\dfrac{h}{t}$.",
      r"Đơn vị: $A$ (J), $P$ (W), $t$ (s), $v$ (m/s).",
      r"⚠ <strong>Điều kiện:</strong> đi lên đều nên lực nâng bằng trọng lượng; độ cao tính theo số khoảng tầng."], [
  ("Độ cao", [P("Từ tầng 1 tới tầng 9 là $8$ khoảng tầng:"), M(r"h=8\cdot3"), A(r"h=24\ \text{m}")]),
  ("Công nâng thang", [M(r"F=10\,m=8\,000\ \text{N}"), M(r"A_{\text{có ích}}=F\,h=8\,000\cdot24"), A(r"A_{\text{có ích}}=192\,000\ \text{J}")]),
  ("Công của động cơ", [M(r"A_{\text{tp}}=\dfrac{A_{\text{có ích}}}{H}"), M(r"A_{\text{tp}}=\dfrac{192\,000}{0{,}8}"), A(r"A_{\text{tp}}=240\,000\ \text{J}")]),
  ("Thời gian đi lên", [M(r"t=\dfrac{A_{\text{tp}}}{P}"), M(r"t=\dfrac{240\,000}{8\,000}"), A(r"t=30\ \text{s}")]),
  ("Tốc độ của thang", [M(r"v=\dfrac{h}{t}=\dfrac{24}{30}"), A(r"v=0{,}8\ \text{m/s}")]),
  ("Kiểm tra", [P("Công suất có ích:"), M(r"F\,v=8\,000\cdot0{,}8=6\,400\ \text{W}"), M(r"\dfrac{6\,400}{8\,000}=80\ \%\ ✓"), P("Công động cơ lớn hơn công có ích.<br>Hợp lí ✓")])],
  [r"a) $A_{\text{có ích}}=192\,000\ \text{J}$", r"b) $A_{\text{tp}}=240\,000\ \text{J}$", r"c) $t=30\ \text{s}$", r"$v=0{,}8\ \text{m/s}$"],
  "Nhận dạng: đề cho <strong>công suất động cơ và hiệu suất</strong> → $A_{\\text{tp}}=\\dfrac{A_{\\text{có ích}}}{H}$, rồi $t=\\dfrac{A_{\\text{tp}}}{P}$."),
]

# ───────────── Tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>lực</b> và <b>quãng đường theo hướng lực</b> → $A=F\,s$; <b>nâng đều</b> → $F=10\,m$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Công đẩy xe", "Công của lực đẩy xe bằng bao nhiêu?", 3000, "J", 10,
       loi=r"Hay chia $\dfrac{F}{s}$ hoặc cộng $F+s$. Công là tích lực với quãng đường theo hướng lực."),
  buoc("Xe bị kẹt", "Khi xe kẹt, lực đẩy có thực hiện công không?",
       loi=r"Hay nghĩ người mỏi là có công. Công cơ học cần vật dịch chuyển theo hướng lực; xe đứng yên thì không có.",
       lua_chon=[("Không, vì xe không dịch chuyển", True),
                 ("Có, vì người vẫn tác dụng lực", r"Có lực mà vật đứng yên thì quãng đường bằng 0, công bằng 0."),
                 ("Có, vì người vẫn mỏi và tốn sức", r"Mỏi là do cơ bắp làm việc bên trong, không phải lực đẩy sinh công lên xe.")],
       ke=[(r"Xét xem xe có dịch chuyển theo hướng lực không", True),
           (r"Lấy lại $A=150\cdot20$ như câu a", r"Câu a xe đi $20$ m; bây giờ xe đứng yên."),
           (r"Nhân lực với thời gian đẩy", r"Công là lực nhân quãng đường, không nhân thời gian.")]),
  buoc("Lực nâng thùng", "Lực nâng thùng hàng bằng bao nhiêu niutơn?", 250, "N", 1,
       loi=r"Hay lấy luôn khối lượng làm lực. Nâng đều thì lực nâng bằng trọng lượng, $F=10\,m$.",
       ke=[(r"$F=10\,m$ (nâng đều, lực bằng trọng lượng)", True),
           (r"$F=m$", r"Khối lượng đo bằng kg, lực đo bằng N: phải nhân $10$."),
           (r"$F=150\ \text{N}$ như lực đẩy xe", r"Lực đẩy xe là lực khác; nâng thùng cần lực bằng trọng lượng thùng.")]),
  buoc("Công nâng thùng", "Công của lực nâng thùng bằng bao nhiêu?", 300, "J", 2,
       loi=r"Hay nhân lực nâng với quãng đường đẩy xe. Nâng lên kệ thì quãng đường theo hướng lực là độ cao của kệ.",
       ke=[(r"$A=F\,h$ với $h$ là độ cao của kệ", True),
           (r"$A=F\cdot20\ \text{m}$", r"$20$ m là quãng đường đẩy xe, không phải độ cao nâng thùng."),
           (r"$A=m\,h$", r"Phải dùng lực (N), không dùng khối lượng (kg).")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy hỏi <b>máy nào nhanh hơn</b> → tính $P=\dfrac{A}{t}$ từng máy, $t$ ra giây, rồi so.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Công của máy A", "Công máy A thực hiện bằng bao nhiêu jun?", 240000, "J", 1000,
       loi=r"Hay quên nhân $10$ khi đổi khối lượng ra trọng lượng: kết quả nhỏ đi $10$ lần."),
  buoc("Công của máy B", "Công máy B thực hiện bằng bao nhiêu jun?", 120000, "J", 1000,
       loi=r"Hay dùng nhầm thể tích của máy A. Mỗi máy tính với lượng nước của chính nó.",
       ke=[(r"$A_B=10\,m_B\,h$ với $m_B$ là khối lượng nước máy B bơm", True),
           (r"$A_B=A_A$ vì cùng bể cao $8$ m", r"Cùng độ cao nhưng lượng nước khác nhau nên công khác nhau."),
           (r"$A_B=m_B\,h$", r"Phải nhân $10$ để có trọng lượng (N).")]),
  buoc("Công suất máy A", "Công suất máy A bằng bao nhiêu oát?", 400, "W", 2,
       loi=r"Hay chia cho $10$ phút. Muốn ra oát thì thời gian phải tính bằng giây.",
       ke=[(r"$P_A=\dfrac{A_A}{t_A}$ với $t_A$ tính bằng giây", True),
           (r"$P_A=\dfrac{A_A}{10}$", r"$10$ là số phút; chia cho phút không ra oát."),
           (r"$P_A=A_A\cdot t_A$", r"Công suất là công chia thời gian, không nhân.")]),
  buoc("Công suất máy B", "Công suất máy B bằng bao nhiêu oát?", 500, "W", 2,
       loi=r"Hay quên đổi $4$ phút ra giây như máy A.",
       ke=[(r"$P_B=\dfrac{A_B}{t_B}$ với $t_B$ tính bằng giây", True),
           (r"$P_B=P_A\cdot\dfrac{1{,}5}{3}$", r"Hai máy chạy thời gian khác nhau, không suy theo tỉ lệ nước được."),
           (r"$P_B=\dfrac{A_B}{10\ \text{phút}}$", r"Máy B chạy $4$ phút, không phải $10$ phút.")]),
  buoc("So sánh", "Máy nào làm việc nhanh hơn?",
       loi=r"Hay chọn máy làm được nhiều công hơn. Nhanh hay chậm là so công suất.",
       lua_chon=[("Máy B", True),
                 ("Máy A, vì bơm được nhiều nước hơn", r"Nhiều nước hơn là công lớn hơn, chưa nói nhanh hơn; máy A mất nhiều thời gian hơn."),
                 ("Hai máy nhanh như nhau vì cùng bơm lên 8 m", r"Cùng độ cao nhưng công và thời gian khác nhau, công suất khác nhau.")],
       ke=[(r"So hai công suất $P_A$ và $P_B$", True),
           (r"So hai công $A_A$ và $A_B$", r"Công lớn hơn chưa chắc làm nhanh hơn."),
           (r"So hai thời gian bơm", r"Hai máy bơm lượng nước khác nhau nên không so thời gian được.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>chạy đều</b>, cho <b>lực kéo và tốc độ</b> → $P=F\,v$ với $v$ (m/s).",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đổi tốc độ", "Tốc độ của xe bằng bao nhiêu m/s?", 15, "m/s", 0.1,
       loi=r"Hay nhân $3{,}6$ thay vì chia. Đổi km/h ra m/s thì số nhỏ đi."),
  buoc("Quãng đường", "Quãng đường xe đi trong 10 phút bằng bao nhiêu mét?", 9000, "m", 20,
       loi=r"Hay nhân tốc độ (m/s) với $10$ phút. Phải đổi phút ra giây cho cùng hệ đơn vị.",
       ke=[(r"$s=v\,t$ với $v$ (m/s), $t$ (s)", True),
           (r"$s=54\cdot10$", r"km/h nhân phút không ra mét; đổi cả hai về m/s và s."),
           (r"$s=\dfrac{v}{t}$", r"Quãng đường là tốc độ nhân thời gian.")]),
  buoc("Công của lực kéo", "Công của lực kéo trong 10 phút bằng bao nhiêu jun?", 2.7e7, "J", 1e5,
       loi=r"Hay nhân lực kéo với thời gian. Công là lực nhân quãng đường.",
       ke=[(r"$A=F\,s$", True),
           (r"$A=F\,t$", r"Nhân lực với thời gian không ra công."),
           (r"$A=F\,v$", r"$F\,v$ là công suất (W), không phải công (J).")]),
  buoc("Công suất", "Công suất của động cơ bằng bao nhiêu oát?", 45000, "W", 100,
       loi=r"Hay dùng $P=F\,v$ với $v=54$ (km/h): kết quả lớn gấp $3{,}6$ lần.",
       ke=[(r"$P=\dfrac{A}{t}$ (hoặc $P=F\,v$ với $v$ m/s)", True),
           (r"$P=F\cdot54$", r"$54$ là km/h; phải đổi ra m/s."),
           (r"$P=A\cdot t$", r"Công suất là công chia thời gian.")]),
  buoc("Tốc độ trên dốc", "Tốc độ của xe trên dốc bằng bao nhiêu km/h?", 32.4, "km/h", 0.2,
       loi=r"Hay giữ nguyên tốc độ cũ. Công suất giữ nguyên mà lực kéo tăng thì tốc độ phải giảm.",
       ke=[(r"$v_{\text{dốc}}=\dfrac{P}{F_{\text{dốc}}}$ rồi đổi ra km/h", True),
           (r"$v_{\text{dốc}}=\dfrac{F_{\text{dốc}}}{P}$", r"Chia ngược: từ $P=F\,v$ suy ra $v=\dfrac{P}{F}$."),
           (r"$v_{\text{dốc}}=v$ vì công suất không đổi", r"Công suất không đổi nhưng lực tăng thì tốc độ giảm theo $v=\dfrac{P}{F}$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>công suất động cơ</b> và <b>hiệu suất</b> → $A_{\text{tp}}=\dfrac{A_{\text{có ích}}}{H}$, $t=\dfrac{A_{\text{tp}}}{P}$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Độ cao", "Thang đi lên cao bao nhiêu mét?", 24, "m", 0.1,
       loi=r"Hay nhân số tầng đích với chiều cao một tầng. Đứng ở tầng 1 thì mới lên số khoảng tầng ít hơn số tầng một đơn vị."),
  buoc("Công nâng thang", "Công nâng thang (công có ích) bằng bao nhiêu jun?", 192000, "J", 500,
       loi=r"Hay nhân khối lượng với độ cao, quên nhân $10$ để có trọng lượng.",
       ke=[(r"$A_{\text{có ích}}=10\,m\,h$", True),
           (r"$A_{\text{có ích}}=m\,h$", r"Lực nâng là trọng lượng $10\,m$ (N), không phải khối lượng."),
           (r"$A_{\text{có ích}}=P\,h$", r"$P$ ở đây là công suất động cơ, không phải lực.")]),
  buoc("Công của động cơ", "Công của động cơ (công toàn phần) bằng bao nhiêu jun?", 240000, "J", 500,
       loi=r"Hay nhân công có ích với $0{,}8$: ra số nhỏ hơn công có ích, vô lí. Công toàn phần lớn hơn nên chia cho $H$.",
       ke=[(r"$A_{\text{tp}}=\dfrac{A_{\text{có ích}}}{H}$", True),
           (r"$A_{\text{tp}}=A_{\text{có ích}}\cdot H$", r"Nhân với $0{,}8$ ra số nhỏ hơn công có ích; công toàn phần phải lớn hơn."),
           (r"$A_{\text{tp}}=A_{\text{có ích}}$", r"Có $20\ \%$ hao phí nên động cơ phải làm nhiều công hơn.")]),
  buoc("Thời gian đi lên", "Thời gian thang đi lên bằng bao nhiêu giây?", 30, "s", 0.2,
       loi=r"Hay chia công có ích cho công suất động cơ: bỏ quên hiệu suất, thời gian tính ra ngắn hơn thật.",
       ke=[(r"$t=\dfrac{A_{\text{tp}}}{P}$", True),
           (r"$t=\dfrac{A_{\text{có ích}}}{P}$", r"$P$ là công suất toàn phần của động cơ, phải chia công toàn phần."),
           (r"$t=A_{\text{tp}}\cdot P$", r"Từ $P=\dfrac{A}{t}$ suy ra $t=\dfrac{A}{P}$.")]),
  buoc("Tốc độ của thang", "Tốc độ của thang bằng bao nhiêu m/s?", 0.8, "m/s", 0.02,
       loi=r"Hay chia thời gian cho độ cao. Tốc độ là quãng đường chia thời gian.",
       ke=[(r"$v=\dfrac{h}{t}$", True),
           (r"$v=\dfrac{t}{h}$", r"Chia ngược: tốc độ là quãng đường chia thời gian."),
           (r"$v=\dfrac{P}{m}$", r"Chia công suất cho khối lượng không ra tốc độ; tốc độ đều là $h/t$.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Ghi JSON ─────────────
d = {"lesson_id": 131, "lesson_title": "Bài 4. Công và công suất", "generated_at": "2026-10-12",
     "review": {"checked": True, "checked_at": "2026-10-12", "notes": "Soạn 12/10/2026 (chặng 3). Đã kiểm chéo kiem-code 2026-10-12: đáp số đúng, sửa 1 lời giải thích lựa chọn sai. Bài 131 chưa có topic gắn lesson_id; dùng topic 78/79 (lesson_id null). Chưa đếm question_bank."},
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
        for fs in _re.findall(r'font-size="(\d+)"', s_):
            assert int(fs) >= 14, fs
print("xong 131.json")
