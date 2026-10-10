"""Bài tập mẫu Bài 25 "Năng lượng điện và công suất điện" (Vật lí 11) — lesson_id 44. 5 dạng (quét: ket-qua/44.quet-dang.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-44.py   (idempotent) → 44.json (review.checked=false cho tới khi kiểm chéo)."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

J = os.path.join(HERE, "44.json")
TOP_P = "Năng lượng điện. Công suất điện"
TOP_N = "Công và công suất của nguồn điện"
TOP_H = "Hiệu suất nguồn điện, an toàn điện"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."

# ═════════════ TỰ GIẢI LẠI SỐ LIỆU (độc lập với lời giải) ═════════════
# Dạng 1: bình 220 V – 2000 W, 45 phút/tối, 30 ngày
t1 = 45 * 60; A1 = 2000 * t1
assert t1 == 2700 and A1 == 5.4e6 and abs(A1 / 3.6e6 - 1.5) < 1e-12 and abs(30 * 1.5 - 45) < 1e-12
assert abs(2.0 * 0.75 - 1.5) < 1e-12
# Dạng 2: bàn là 220 V – 1100 W ở 176 V, 30 phút
R2 = 220 ** 2 / 1100; I2 = 176 / R2; P2 = 176 * I2; A2 = P2 / 1000 * 0.5
assert abs(R2 - 44) < 1e-9 and abs(I2 - 4.0) < 1e-9 and abs(P2 - 704) < 1e-9 and abs(A2 - 0.352) < 1e-9
assert abs((176 / 220) ** 2 * 1100 - 704) < 1e-9 and abs(0.8 * 1100 - 880) < 1e-9 and 880 != 704
# Dạng 3: E = 6,0 V ; r = 0,40 ; R = 2,6 ; 5 phút
E3, r3, R3 = 6.0, 0.40, 2.6
I3 = E3 / (R3 + r3); U3 = I3 * R3; Pn = E3 * I3; Pr_ = U3 * I3; Ph = I3 ** 2 * r3; A3 = Pn * 300
assert abs(I3 - 2.0) < 1e-9 and abs(U3 - 5.2) < 1e-9 and abs(Pn - 12) < 1e-9 and abs(Pr_ - 10.4) < 1e-9
assert abs(Ph - 1.6) < 1e-9 and abs(Pr_ + Ph - Pn) < 1e-9 and abs(A3 - 3600) < 1e-6 and abs(E3 - I3 * r3 - U3) < 1e-9
# Dạng 4: E = 12 V ; r = 0,75 ; H = 80 % ; 10 phút
E4, r4, H4 = 12.0, 0.75, 0.80
R4 = H4 * r4 / (1 - H4); I4 = E4 / (R4 + r4); U4 = I4 * R4
Ai = U4 * I4 * 600; Ah = I4 ** 2 * r4 * 600; At = E4 * I4 * 600
assert abs(R4 - 3.0) < 1e-9 and abs(I4 - 3.2) < 1e-9 and abs(U4 - 9.6) < 1e-9 and abs(U4 / E4 - H4) < 1e-9
assert abs(Ai - 18432) < 1e-6 and abs(Ah - 4608) < 1e-6 and abs(Ai + Ah - At) < 1e-6 and abs(Ai / At - 0.8) < 1e-9
# cách sai: H = r/(R+r) cho R khác (kiểm lựa chọn sai khác đáp án)
assert abs(r4 / (R4 + r4) - 0.8) > 0.1
# Dạng 5: E = 12 V ; r = 0,030 ; đèn 2,37 ; chạm 0,010
E5, r5, Rd, Rc = 12.0, 0.030, 2.37, 0.010
I5 = E5 / (Rd + r5); Isc = E5 / (Rc + r5); Pth = Isc ** 2 * r5
assert abs(I5 - 5.0) < 1e-9 and abs(Isc - 300) < 1e-9 and abs(Pth - 2700) < 1e-6 and abs(Isc / 7.5 - 40) < 1e-9
assert abs(E5 / Rc - 1200) < 1e-9 and 5.0 < 7.5 < 30 and 7.5 < Isc

# ═════════════ TIỆN ÍCH VẼ ═════════════
def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, s, c, size, anchor, weight)

def Rr(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d}/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def anim(attr, vals, kts, T, extra=""):
    v = ";".join(f"{x:.1f}" if isinstance(x, float) else str(x) for x in vals)
    k = ";".join(f"{t:.4f}" for t in kts)
    return f'<animate attributeName="{attr}" values="{v}" keyTimes="{k}" dur="{T:.2f}s" begin="indefinite" fill="freeze"{extra}/>'

def iron(x, y, glow=""):
    """Bàn là nhìn nghiêng; (x, y) = góc trái của đế. Rộng 130."""
    body = (f'<path d="M{x},{y} L{x + 130},{y} L{x + 130},{y - 22} Q{x + 80},{y - 52} {x + 36},{y - 40} L{x},{y - 14} Z" '
            f'fill="none" stroke="currentColor" stroke-width="2.4"/>')
    body += (f'<path d="M{x + 44},{y - 40} Q{x + 78},{y - 66} {x + 112},{y - 36}" fill="none" stroke="currentColor" stroke-width="2.4"/>')
    body += f'<rect x="{x}" y="{y}" width="130" height="9" fill="none" stroke="currentColor" stroke-width="2"/>'
    body += glow
    return body

# ───────────── mạch kín: nguồn (ε, r) – điện trở R ─────────────
X0, X1, Y0, Y1 = 110, 350, 44, 176

def loop_path():
    return [(X0, 86), (X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1), (X0, 86)]

def point_at(s):
    pts = loop_path(); per = 0; segs = []
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); segs.append((per, L, a, b)); per += L
    s %= per
    for st, L, a, b in segs:
        if s <= st + L:
            u = (s - st) / L
            return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
    return pts[0]

PER = 42 + 240 + 132 + 240 + 90

def circuit(lab_e, lab_r, lab_R, fuse=False, dots=0, T=5.0, lamp=False, varR=False):
    """Mạch kín. Nguồn bên trái (dấu + ở tấm dài phía trên), điện trở ngoài bên phải."""
    b = seg(X0, Y0, X0, 86) + seg(X0, Y0, X1, Y0) + seg(X1, Y0, X1, 84) + seg(X1, 136, X1, Y1) + seg(X1, Y1, X0, Y1) + seg(X0, 138, X0, Y1)
    # nguồn: tấm dài (+) ở trên, tấm ngắn (−), điện trở trong r là ô dưới
    b += seg(X0 - 18, 86, X0 + 18, 86, "currentColor", 3) + seg(X0 - 10, 96, X0 + 10, 96, "currentColor", 3)
    b += seg(X0, 96, X0, 112) + Rr(X0 - 9, 112, 18, 26, "currentColor", 2)
    b += Rr(X0 - 30, 76, 60, 70, GREY, 1.4, rx=6, dash="4 3")
    b += txt(X0 + 24, 84, "+", RED, 15, "start", "700")
    b += txt(X0 - 38, 96, lab_e, "currentColor", 13, "end") + txt(X0 - 38, 130, lab_r, "currentColor", 13, "end")
    # điện trở ngoài
    if lamp:
        b += circ(X1, 110, 26, "currentColor", 2.2) + seg(X1 - 18, 92, X1 + 18, 128) + seg(X1 - 18, 128, X1 + 18, 92)
        b += seg(X1, 84, X1, 84)
    else:
        b += Rr(X1 - 12, 84, 24, 52, "currentColor", 2.2)
    if varR:
        b += arrow("", "o", X1 - 30, 142, X1 + 28, 80, 2.2)
    b += txt(X1 - 38, 114, lab_R, "currentColor", 13, "end")
    if fuse:
        b += Rr(210, Y0 - 7, 40, 14, "currentColor", 2, "none", 2) + txt(230, Y0 - 14, "cầu chì", "currentColor", 12, "middle")
    for k in range(dots):
        off = k * PER / dots; N = 36; travel = PER * 0.5
        xs = []; ys = []
        for i in range(N + 1):
            x, y = point_at(off + travel * i / N); xs.append(x); ys.append(y)
        b += (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="4.5" fill="{BLUE}" stroke="currentColor" stroke-width="1.2">'
              f'{smil("cx", xs, T)}{smil("cy", ys, T)}</circle>')
    return b

GREY = "#94a3b8"


# ═════════════ HÌNH: Dạng 1 ═════════════
def d1(kk):
    p = f"d1{kk}"
    b = ""
    if kk == 0:
        b += Rr(22, 62, 78, 104, "currentColor", 2.4, rx=12) + txt(61, 108, "220 V", "currentColor", 13, "middle") + txt(61, 128, "2000 W", "currentColor", 13, "middle")
        b += txt(61, 54, "bình nóng lạnh", "currentColor", 12, "middle", "600")
        cx, cy, r = 205, 112, 50
        b += circ(cx, cy, r)
        for k in range(12):
            a = math.radians(30 * k)
            b += seg(cx + (r - 8) * math.sin(a), cy - (r - 8) * math.cos(a), cx + r * math.sin(a), cy - r * math.cos(a), "currentColor", 2)
        b += txt(cx, cy - r - 8, "kim phút", "currentColor", 12, "middle", "600")
        b += (f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r + 10}" stroke="{ORG}" stroke-width="3" stroke-linecap="round">'
              f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="270 {cx} {cy}" dur="6s" begin="indefinite" fill="freeze"/></line>')
        b += dot(cx, cy, 4)
        b += txt(cx, cy + r + 20, "t: 0 → 45 phút", "currentColor", 12, "middle", "600")
        b += Rr(300, 62, 80, 104, "currentColor", 2.4, rx=6)
        b += f'<rect x="304" y="166" width="72" height="0" fill="{BLUE}" fill-opacity=".45">{smil("y", [162, 66], 6)}{smil("height", [0, 96], 6)}</rect>'
        b += txt(340, 54, "công tơ", "currentColor", 12, "middle", "600") + txt(340, 188, "A = ?", ORG, 13, "middle")
        b += arrow("", "b", 106, 114, 148, 114, 2)
        return fig("d1-0", "0 0 420 200", "Kim phút quay 45 phút trong khi cột công tơ điện dâng dần", b,
                   "Mô phỏng: kim phút quay trọn 45 phút trong 6 giây (1 giây tương ứng khoảng 7,5 phút) trong lúc cột công tơ dâng dần. " + NOTE)
    b += Rr(30, 50, 100, 86, "currentColor", 2.4, rx=12) + txt(80, 90, "220 V", "currentColor", 13, "middle") + txt(80, 110, "2000 W", "currentColor", 13, "middle")
    b += txt(80, 44, "bình nóng lạnh", "currentColor", 12, "middle", "600")
    b += txt(160, 78, "dùng đúng 220 V", BLUE, 13) + txt(160, 100, "t = 45 phút mỗi tối", BLUE, 13) + txt(160, 122, "trong 30 ngày", BLUE, 13)
    b += txt(30, 168, "Cần tìm:  A một tối (J và kWh) · A trong 30 ngày (kWh)", ORG, 13)
    return fig("d1-2", "0 0 420 184", "Bình nóng lạnh ghi 220 V – 2000 W, dùng 45 phút mỗi tối trong 30 ngày", b,
               "Dữ kiện: nhãn bình, thời gian dùng mỗi tối và số ngày; điện năng cần tìm ghi bằng dấu hỏi. " + NOTE)


# ═════════════ HÌNH: Dạng 2 ═════════════
def vmeter(cx, cy, r, v):
    a = math.radians(180 * (1 - v / 250))
    return cx + r * math.cos(a), cy - r * math.sin(a)

def d2(kk):
    p = f"d2{kk}"
    b = ""
    if kk == 0:
        cx, cy, r = 105, 146, 78
        b += f'<path d="M{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
        for v in (0, 50, 100, 150, 200, 250):
            x1, y1 = vmeter(cx, cy, r, v); x2, y2 = vmeter(cx, cy, r - 9, v)
            b += seg(x1, y1, x2, y2, "currentColor", 2)
        for v in (0, 100, 200):
            x, y = vmeter(cx, cy, r + 14, v)
            b += txt(x, y + 4, str(v), "currentColor", 12, "middle", "600")
        x, y = vmeter(cx, cy, r + 4, 220); xi, yi = vmeter(cx, cy, r - 12, 220)
        b += seg(x, y, xi, yi, RED, 3) + txt(x + 6, y - 6, "220 (định mức)", RED, 12, "start", "600")
        x0, y0 = vmeter(cx, cy, r - 14, 220)
        a0 = 180 * (1 - 220 / 250); a1 = 180 * (1 - 176 / 250)
        b += (f'<line x1="{cx}" y1="{cy}" x2="{x0:.1f}" y2="{y0:.1f}" stroke="{ORG}" stroke-width="3" stroke-linecap="round">'
              f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="{-(a1 - a0):.1f} {cx} {cy}" dur="4s" begin="indefinite" fill="freeze"/></line>')
        b += dot(cx, cy, 5) + txt(cx, cy + 22, "U (V) ở ổ cắm", "currentColor", 12, "middle", "600")
        glow = f'<rect x="262" y="150" width="130" height="9" fill="{ORG}" stroke="none">{smil("opacity", [1.0, 0.5], 4)}</rect>'
        b += iron(262, 150, glow) + txt(327, 186, "220 V – 1100 W", "currentColor", 13, "middle") + txt(327, 204, "coi R không đổi", BLUE, 12, "middle", "600")
        b += seg(cx + r + 8, cy - 10, 258, 130, GREY, 1.6, "5 4")
        return fig("d2-0", "0 0 420 216", "Hiệu điện thế ở ổ cắm giảm dần trong khi đế bàn là sáng nhạt đi", b,
                   "Mô phỏng: kim vôn kế tụt từ vạch định mức xuống hiệu điện thế thực trong 4 giây, đế bàn là nhạt dần. " + NOTE)
    b += iron(34, 120) + txt(99, 156, "220 V – 1100 W", "currentColor", 13, "middle")
    b += txt(190, 62, "ổ cắm: U = 176 V", BLUE, 13) + txt(190, 84, "R không đổi", BLUE, 13)
    b += txt(190, 116, "Cần tìm:", ORG, 13) + txt(190, 136, "R · I · P thực", ORG, 13) + txt(190, 156, "A trong 30 phút (kWh)", ORG, 13)
    return fig("d2-2", "0 0 420 176", "Bàn là ghi 220 V – 1100 W cắm vào ổ cắm chỉ có 176 V", b,
               "Dữ kiện: nhãn bàn là, hiệu điện thế thực ở ổ cắm; các đại lượng cần tìm ghi bằng dấu hỏi. " + NOTE)


# ═════════════ HÌNH: Dạng 3 ═════════════
def d3(kk):
    if kk == 0:
        b = circuit("ε = 6,0 V", "r = 0,40 Ω", "R = 2,6 Ω", dots=3, T=5.0)
        b += arrow("", "o", 180, Y0, 224, Y0, 2.4) + txt(202, Y0 - 10, "I = ?", ORG, 13, "middle")
        return fig("d3-0", "0 0 420 196", "Các điện tích chạy vòng quanh mạch kín gồm nguồn có điện trở trong và điện trở ngoài", b,
                   "Mô phỏng: điện tích chạy nửa vòng mạch trong 5 giây, chiều từ cực dương qua mạch ngoài. " + NOTE)
    b = circuit("ε = 6,0 V", "r = 0,40 Ω", "R = 2,6 Ω")
    b += txt(20, 200, "Cần tìm:  I · công suất của nguồn · công suất mạch ngoài", ORG, 13)
    b += txt(20, 220, "công suất toả nhiệt trong nguồn · công của nguồn trong 5 phút", ORG, 13)
    return fig("d3-2", "0 0 420 232", "Mạch kín gồm nguồn 6,0 V có điện trở trong 0,40 ôm nối với điện trở 2,6 ôm", b,
               "Dữ kiện: suất điện động, điện trở trong và điện trở ngoài; các đại lượng cần tìm ghi bên dưới. " + NOTE)


# ═════════════ HÌNH: Dạng 4 ═════════════
def d4(kk):
    if kk == 0:
        T = 6.0
        b = Rr(30, 84, 360, 40, "currentColor", 2.4)
        b += f'<rect x="30" y="84" width="0" height="40" fill="{GRN}" fill-opacity=".55">{smil("width", [0, 288], T)}</rect>'
        b += f'<rect x="30" y="84" width="0" height="40" fill="{RED}" fill-opacity=".55">{smil("x", [30, 318], T)}{smil("width", [0, 72], T)}</rect>'
        b += txt(30, 70, "năng lượng nguồn phát ra  →", "currentColor", 13)
        b += circ(40, 160, 6, GRN, 1.6, GRN) + txt(52, 165, "phần mạch ngoài nhận (có ích)", GRN, 12, "start", "600")
        b += circ(40, 184, 6, RED, 1.6, RED) + txt(52, 189, "phần toả ra trong nguồn (hao phí)", RED, 12, "start", "600")
        b += txt(210, 30, "t: 0 → 10 phút", "currentColor", 13, "middle")
        return fig("d4-0", "0 0 420 204", "Thanh năng lượng của nguồn dài dần, chia thành phần có ích và phần hao phí", b,
                   "Mô phỏng: trong 10 phút, thanh năng lượng nguồn phát ra dài dần, chia theo tỉ lệ đề cho (hiệu suất 80 %). 10 phút chạy trong 6 giây. " + NOTE)
    b = circuit("ε = 12 V", "r = 0,75 Ω", "R = ?", varR=True)
    b += txt(20, 200, "Cần tìm:  R để H = 80 % · I · U · A có ích và A hao phí trong 10 phút", ORG, 13)
    return fig("d4-2", "0 0 420 214", "Nguồn 12 V có điện trở trong 0,75 ôm nối với biến trở R, hiệu suất 80 %", b,
               "Dữ kiện: suất điện động, điện trở trong, hiệu suất nguồn; biến trở R và các đại lượng cần tìm ghi bằng dấu hỏi. " + NOTE)


# ═════════════ HÌNH: Dạng 5 ═════════════
def d5(kk):
    if kk == 0:
        T = 3.0
        b = Rr(100, 100, 200, 76, "currentColor", 2.4, rx=6) + Rr(130, 82, 30, 18, "currentColor", 2.2) + Rr(240, 82, 30, 18, "currentColor", 2.2)
        b += txt(145, 76, "+", RED, 15, "middle") + txt(255, 76, "−", BLUE, 15, "middle")
        b += txt(200, 132, "ắc quy: ε = 12 V", "currentColor", 13, "middle") + txt(200, 154, "r = 0,030 Ω", "currentColor", 13, "middle")
        key = (f'<g>{Rr(120, 62, 160, 12, ORG, 2.4, "none", 3)}{circ(108, 68, 12, ORG, 2.4)}'
               f'<animateTransform attributeName="transform" type="translate" values="0 -46;0 0" dur="{T}s" begin="indefinite" fill="freeze"/></g>')
        b += key
        kts = [0, 0.85, 1.0]
        for (sx, sy) in ((145, 82), (255, 82)):
            b += f'<g opacity="0">{anim("opacity", [0, 0, 1], kts, T)}'
            for ang in (-150, -110, -70, -30):
                a = math.radians(ang)
                b += seg(sx + 6 * math.cos(a), sy + 6 * math.sin(a), sx + 20 * math.cos(a), sy + 20 * math.sin(a), RED, 2.4)
            b += circ(sx, sy, 9, ORG, 0, ORG).replace('fill="' + ORG + '"', f'fill="{ORG}" fill-opacity=".5"') + "</g>"
        b += txt(210, 198, "chìa khoá rơi chạm hai cực, điện trở chỗ chạm 0,010 Ω", "currentColor", 12, "middle", "600")
        return fig("d5-0", "0 0 420 210", "Chiếc chìa khoá rơi xuống chạm vào hai cực của ắc quy", b,
                   "Mô phỏng: chìa khoá rơi nối thẳng hai cực ắc quy trong 3 giây, tia lửa xuất hiện ở hai chỗ chạm. " + NOTE)
    b = circuit("ε = 12 V", "r = 0,030 Ω", "đèn 2,37 Ω", fuse=True, lamp=True)
    b += txt(20, 200, "Cần tìm:  dòng làm việc · cầu chì phù hợp (3 A, 7,5 A hay 30 A)", ORG, 13)
    b += txt(20, 220, "dòng khi đoản mạch · nhiệt trong ắc quy · cầu chì có đứt không", ORG, 13)
    return fig("d5-2", "0 0 420 232", "Mạch đèn của ắc quy 12 V có cầu chì, đèn có điện trở 2,37 ôm", b,
               "Dữ kiện: ắc quy, bộ đèn và cầu chì trong mạch; các đại lượng cần tìm ghi bên dưới. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Điện năng tiêu thụ và đổi jun sang kWh", topic=TOP_P,
      problem_html=r"""<p>Một bình nóng lạnh ghi $220\ \text{V} - 2000\ \text{W}$. Mỗi tối gia đình bật bình đúng hiệu điện thế định mức trong $45$ phút.</p><ol type="a"><li>Tính điện năng bình tiêu thụ mỗi tối, theo jun.</li><li>Đổi điện năng đó ra kWh.</li><li>Tính số điện (kWh) bình tiêu thụ trong $30$ ngày.</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Thiết bị dùng ở hiệu điện thế khác định mức", topic=TOP_P,
      problem_html=r"""<p>Một bàn là ghi $220\ \text{V} - 1100\ \text{W}$. Ở khu vực xa trạm điện, ổ cắm chỉ có hiệu điện thế $176\ \text{V}$. Coi điện trở của bàn là không đổi.</p><ol type="a"><li>Tính điện trở của bàn là.</li><li>Tính cường độ dòng điện và công suất thực của bàn là khi cắm vào ổ cắm đó.</li><li>Bàn là chạy liên tục $30$ phút ở hiệu điện thế này. Tính điện năng tiêu thụ theo kWh.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Công suất của nguồn, mạch ngoài và nhiệt trong nguồn", topic=TOP_N,
      problem_html=r"""<p>Một bộ pin có suất điện động $\mathcal{E} = 6{,}0\ \text{V}$, điện trở trong $r = 0{,}40\ \Omega$ được nối kín với một điện trở $R = 2{,}6\ \Omega$ của mạch sưởi nhỏ. Bỏ qua điện trở dây nối.</p><ol type="a"><li>Tính cường độ dòng điện trong mạch.</li><li>Tính công suất của nguồn, công suất mạch ngoài nhận được và công suất toả nhiệt trong nguồn.</li><li>Tính công của nguồn trong $5$ phút.</li></ol>"""),
 dict(label="Dạng 4 · Khó · Hiệu suất nguồn điện và năng lượng có ích, hao phí", topic=TOP_H,
      problem_html=r"""<p>Một bộ pin dự phòng có suất điện động $\mathcal{E} = 12\ \text{V}$, điện trở trong $r = 0{,}75\ \Omega$ được nối kín với một biến trở $R$ cấp điện cho thiết bị sưởi. Người ta chỉnh $R$ sao cho hiệu suất của nguồn bằng $80\ \%$. Bỏ qua điện trở dây nối.</p><ol type="a"><li>Tính giá trị của biến trở $R$.</li><li>Tính cường độ dòng điện trong mạch và hiệu điện thế giữa hai cực của bộ pin.</li><li>Trong $10$ phút, mạch ngoài nhận bao nhiêu năng lượng có ích, bao nhiêu năng lượng toả ra trong bộ pin?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Đoản mạch và chọn cầu chì", topic=TOP_H,
      problem_html=r"""<p>Ắc quy xe máy có suất điện động $\mathcal{E} = 12\ \text{V}$, điện trở trong $r = 0{,}030\ \Omega$. Mạch đèn gồm một bộ đèn có điện trở $2{,}37\ \Omega$ khi sáng và một cầu chì nối tiếp; có ba loại cầu chì với dòng định mức $3\ \text{A}$, $7{,}5\ \text{A}$ và $30\ \text{A}$. Bỏ qua điện trở dây nối.</p><ol type="a"><li>Tính cường độ dòng điện khi đèn sáng bình thường và chọn loại cầu chì phù hợp.</li><li>Dây dẫn bị chập làm bộ đèn bị nối tắt, điện trở mạch ngoài chỉ còn $0{,}010\ \Omega$. Tính cường độ dòng điện và công suất toả nhiệt trong ắc quy lúc đó.</li><li>Dòng điện lúc chập gấp bao nhiêu lần dòng định mức của cầu chì đã chọn? Cầu chì có đứt không?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (⚠ chỉ nêu điều kiện; cột 3 không ghi số, không ghi kết luận) ═════════════
ANALYSIS = [
 [(r'"ghi $220\ \text{V}-2000\ \text{W}$"', r"$U_{\text{đm}}=220$ V ; $P_{\text{đm}}=2000$ W", r"⚠ Công suất ghi trên nhãn chỉ có khi dùng đúng hiệu điện thế định mức ; công suất không đổi suốt lúc bật"),
  (r'"bật đúng hiệu điện thế định mức"', r"$U=U_{\text{đm}}$", r"Công suất thực lúc này so với công suất ghi trên nhãn"),
  (r'"trong $45$ phút"', r"$t=45$ phút", r"Ra jun thì $t$ tính bằng đơn vị nào ? Ra kWh thì $P$ và $t$ tính bằng đơn vị nào ?"),
  (r'"trong $30$ ngày"', r"$30$ ngày, mỗi ngày dùng như nhau", r"Điện năng của nhiều ngày : cộng dồn"),
  (r'"điện năng … theo jun", "đổi ra kWh"', r"Cần tìm : $A$ (J) ; $A$ (kWh)", r"Điện năng theo công suất và thời gian ; liên hệ giữa kWh và jun")],
 [(r'"ghi $220\ \text{V}-1100\ \text{W}$"', r"$U_{\text{đm}}=220$ V ; $P_{\text{đm}}=1100$ W", r"⚠ Công suất trên nhãn ứng với hiệu điện thế định mức ; từ nhãn suy ra được điện trở của bàn là"),
  (r'"ổ cắm chỉ có $176\ \text{V}$"', r"$U=176$ V", r"So với $U_{\text{đm}}$ : công suất thực còn bằng công suất ghi trên nhãn không ?"),
  (r'"coi điện trở của bàn là không đổi"', r"$R$ không đổi", r"Điều kiện cho phép dùng điện trở tính từ nhãn ở hiệu điện thế mới"),
  (r'"điện trở", "cường độ dòng điện và công suất thực"', r"Cần tìm : $R$ ; $I$ ; $P$", r"Điện trở từ nhãn ; định luật Ôm ; công suất theo $U$ và $I$"),
  (r'"chạy liên tục $30$ phút … theo kWh"', r"$t=30$ phút", r"Điện năng theo công suất thực và thời gian ; ra kWh thì $P$, $t$ ở đơn vị nào ?")],
 [(r'"suất điện động $6{,}0$ V, điện trở trong $0{,}40\ \Omega$"', r"$\mathcal{E}=6{,}0$ V ; $r=0{,}40\ \Omega$", r"⚠ Mạch kín một nguồn, mạch ngoài chỉ có điện trở, bỏ qua dây nối ; $\mathcal{E}$ và $r$ không đổi"),
  (r'"điện trở $R=2{,}6\ \Omega$"', r"$R=2{,}6\ \Omega$", r"Mạch ngoài chỉ toả nhiệt : hiệu điện thế hai đầu $R$ liên hệ với $I$ thế nào ?"),
  (r'"cường độ dòng điện trong mạch"', r"Cần tìm : $I$", r"Định luật Ôm cho toàn mạch (mạch có cả điện trở trong)"),
  (r'"công suất của nguồn"', r"Cần tìm : $P_{ng}$", r"Công suất của nguồn theo suất điện động và dòng điện"),
  (r'"công suất mạch ngoài nhận được"', r"Cần tìm : $P_R$", r"Công suất của mạch ngoài theo hiệu điện thế hai cực và dòng điện"),
  (r'"công suất toả nhiệt trong nguồn"', r"Cần tìm : $P_r$", r"Nhiệt toả ra ở điện trở trong theo dòng điện và $r$"),
  (r'"công của nguồn trong $5$ phút"', r"$t=5$ phút", r"Công theo công suất và thời gian ; $t$ ra đơn vị nào để được jun ?")],
 [(r'"suất điện động $12$ V, điện trở trong $0{,}75\ \Omega$"', r"$\mathcal{E}=12$ V ; $r=0{,}75\ \Omega$", r"⚠ Mạch ngoài chỉ có biến trở (thuần điện trở), bỏ qua dây nối : mới dùng được hiệu suất theo $R$ và $r$"),
  (r'"hiệu suất của nguồn bằng $80\ \%$"', r"$H=0{,}80$", r"Hiệu suất nguồn : phần có ích chia phần toàn phần, viết theo $R$ và $r$"),
  (r'"giá trị của biến trở $R$"', r"Cần tìm : $R$", r"Giải ngược từ hiệu suất ; $R$ cùng đơn vị với $r$"),
  (r'"cường độ dòng điện … hiệu điện thế giữa hai cực"', r"Cần tìm : $I$ ; $U$", r"Định luật Ôm toàn mạch ; hiệu điện thế mạch ngoài"),
  (r'"trong $10$ phút … năng lượng có ích"', r"$t=10$ phút", r"Phần mạch ngoài nhận : theo $U$, $I$, $t$ ; $t$ ra giây"),
  (r'"năng lượng toả ra trong bộ pin"', r"Cần tìm : $A_{\text{hp}}$", r"Nhiệt toả ra ở điện trở trong theo $I$, $r$, $t$")],
 [(r'"suất điện động $12$ V, điện trở trong $0{,}030\ \Omega$"', r"$\mathcal{E}=12$ V ; $r=0{,}030\ \Omega$", r"⚠ Dòng điện trong mạch phụ thuộc cả điện trở mạch ngoài lẫn điện trở trong ; dây dẫn bỏ qua điện trở"),
  (r'"bộ đèn có điện trở $2{,}37\ \Omega$ … cầu chì nối tiếp"', r"$R_{\text{đèn}}=2{,}37\ \Omega$", r"Cầu chì nối tiếp thì cùng dòng điện với mạch"),
  (r'"ba loại cầu chì $3$ A, $7{,}5$ A, $30$ A"', r"Dòng định mức : $3$ A ; $7{,}5$ A ; $30$ A", r"Cầu chì phải chịu được dòng làm việc, nhưng đứt trước khi dây quá nóng : chọn loại nào so với dòng làm việc ?"),
  (r'"dây dẫn bị chập … điện trở mạch ngoài chỉ còn $0{,}010\ \Omega$"', r"$R_{\text{ngoài}}=0{,}010\ \Omega$", r"Đoản mạch : điện trở mạch ngoài rất nhỏ ; điện trở trong vẫn còn trong mạch"),
  (r'"cường độ dòng điện và công suất toả nhiệt trong ắc quy"', r"Cần tìm : $I_{\text{cố}}$ ; $P_r$", r"Định luật Ôm toàn mạch ; nhiệt ở điện trở trong"),
  (r'"gấp bao nhiêu lần … cầu chì có đứt không"', r"Cần tìm : $I_{\text{cố}}/I_{\text{đm}}$", r"So dòng thực tế với dòng định mức của cầu chì")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> điện năng tiêu thụ là năng lượng thiết bị nhận từ dòng điện<br>công suất là điện năng mỗi giây.",
      r"<strong>Công thức:</strong> $A=Pt$ (với $P=UI$)<br>$1\ \text{kWh}=3{,}6\cdot10^{6}\ \text{J}$.",
      r"Ra jun : $P$ tính bằng W, $t$ bằng giây. Ra kWh : $P$ bằng kW, $t$ bằng giờ.",
      r"⚠ <strong>Điều kiện:</strong> dùng đúng $U_{\text{đm}}$ thì $P=P_{\text{đm}}$ và không đổi suốt lúc bật."]
R2 = [r"<strong>Khái niệm:</strong> nhãn $U_{\text{đm}}-P_{\text{đm}}$ cho công suất khi dùng đúng $U_{\text{đm}}$<br>từ nhãn suy ra điện trở của thiết bị.",
      r"<strong>Công thức:</strong> $R=\dfrac{U_{\text{đm}}^{2}}{P_{\text{đm}}}$<br>$I=\dfrac{U}{R}$<br>$P=UI=\dfrac{U^{2}}{R}$<br>$A=Pt$.",
      r"⚠ <strong>Điều kiện:</strong> bàn là chỉ toả nhiệt, coi $R$ không đổi khi $U$ thay đổi<br>công suất thực tỉ lệ với $U^{2}$ chứ không tỉ lệ với $U$."]
R3 = [r"<strong>Khái niệm:</strong> nguồn đẩy điện tích qua cả mạch kín<br>điện trở trong $r$ cũng toả nhiệt.",
      r"<strong>Định luật:</strong> $I=\dfrac{\mathcal{E}}{R+r}$<br>$U=IR=\mathcal{E}-Ir$.",
      r"<strong>Công thức:</strong> $P_{ng}=\mathcal{E}I$<br>$P_R=UI$<br>$P_r=I^{2}r$<br>$A_{ng}=P_{ng}t$.",
      r"⚠ <strong>Điều kiện:</strong> mạch kín một nguồn, mạch ngoài chỉ có điện trở<br>$t$ tính bằng giây để ra jun."]
R4 = [r"<strong>Khái niệm:</strong> hiệu suất nguồn là phần năng lượng nguồn phát ra mà mạch ngoài nhận được.",
      r"<strong>Công thức:</strong> $H=\dfrac{U}{\mathcal{E}}=\dfrac{R}{R+r}$<br>$I=\dfrac{\mathcal{E}}{R+r}$<br>$A_{\text{ích}}=UIt$<br>$A_{\text{hp}}=I^{2}rt$.",
      r"⚠ <strong>Điều kiện:</strong> $H=\dfrac{R}{R+r}$ chỉ dùng khi mạch ngoài thuần điện trở<br>$t$ ra giây."]
R5 = [r"<strong>Khái niệm:</strong> đoản mạch là hai cực nguồn nối gần như thẳng, $R\to0$<br>cầu chì phải đứt trước khi dây quá nóng.",
      r"<strong>Định luật:</strong> $I=\dfrac{\mathcal{E}}{R+r}$<br>nhiệt trong nguồn $P_r=I^{2}r$.",
      r"Chọn cầu chì : dòng định mức lớn hơn dòng làm việc một chút.",
      r"⚠ <strong>Điều kiện:</strong> điện trở trong $r$ vẫn nằm trong mạch khi đoản mạch<br>cầu chì nối tiếp thì cùng dòng điện với mạch."]

SOLS = [
 sol(R1, [
  ("Đổi thời gian",
   [P("Ra jun thì thời gian phải tính bằng giây :"), M(r"t=45\cdot60"), A(r"t=2700\ \text{s}")]),
  ("Điện năng mỗi tối theo jun",
   [P("Bình dùng đúng hiệu điện thế định mức nên công suất bằng công suất ghi trên nhãn :"), M(r"A=Pt"), M(r"A=2000\cdot2700"), A(r"A=5{,}4\cdot10^{6}\ \text{J}")]),
  ("Đổi ra kWh",
   [P(r"$1\ \text{kWh}=3{,}6\cdot10^{6}\ \text{J}$ nên chia số jun cho hệ số này :"), M(r"A=\dfrac{5{,}4\cdot10^{6}}{3{,}6\cdot10^{6}}"), A(r"A=1{,}5\ \text{kWh}")]),
  ("Điện năng trong 30 ngày",
   [P("Mỗi ngày dùng như nhau nên nhân với số ngày :"), M(r"A_{30}=30\cdot1{,}5"), A(r"A_{30}=45\ \text{kWh}")]),
  ("Kiểm tra",
   [P(r"Cách khác : $2{,}0\ \text{kW}\cdot0{,}75\ \text{h}=1{,}5\ \text{kWh}$ ✓ khớp."),
    P(r"Đơn vị : W·s = J<br>kW·h = kWh ✓."),
    P(r"$45$ số mỗi tháng cho một bình nóng lạnh : hợp lí so với hoá đơn vài trăm số.")])],
  [r"a) $A=5{,}4\cdot10^{6}\ \text{J}$", r"b) $A=1{,}5\ \text{kWh}$", r"c) $A_{30}=45\ \text{kWh}$"],
  r"Nhận dạng: đề cho <strong>công suất và thời gian dùng</strong>, hỏi <strong>điện năng, jun hay số điện</strong> → $A=Pt$ ; ra jun dùng W–giây, ra kWh dùng kW–giờ."),
 sol(R2, [
  ("Điện trở của bàn là từ nhãn",
   [P("Bàn là chỉ toả nhiệt, công suất định mức ứng với hiệu điện thế định mức :"), M(r"R=\dfrac{U_{\text{đm}}^{2}}{P_{\text{đm}}}"), M(r"R=\dfrac{220^{2}}{1100}"), A(r"R=44\ \Omega")]),
  ("Cường độ dòng điện thực",
   [P(r"Coi $R$ không đổi, dùng hiệu điện thế thực $176\ \text{V}$ :"), M(r"I=\dfrac{U}{R}"), M(r"I=\dfrac{176}{44}"), A(r"I=4{,}0\ \text{A}")]),
  ("Công suất thực",
   [M(r"P=UI"), M(r"P=176\cdot4{,}0"), A(r"P=704\ \text{W}")]),
  ("Điện năng trong 30 phút",
   [P(r"Ra kWh thì $P$ tính bằng kW, $t$ bằng giờ : $P=0{,}704\ \text{kW}$, $t=0{,}5\ \text{h}$."), M(r"A=Pt"), M(r"A=0{,}704\cdot0{,}5"), A(r"A=0{,}352\ \text{kWh}")]),
  ("Kiểm tra",
   [P(r"Cách khác : $P=\dfrac{U^{2}}{R}=\left(\dfrac{176}{220}\right)^{2}\cdot1100$ ✓ khớp."),
    P(r"$U$ giảm thì $P$ giảm, và giảm nhiều hơn $U$ : $P$ tỉ lệ với $U^{2}$ ✓."),
    P(r"Điện năng nhỏ hơn $1{,}1\ \text{kW}\cdot0{,}5\ \text{h}=0{,}55\ \text{kWh}$ khi dùng đúng định mức ✓.")])],
  [r"a) $R=44\ \Omega$", r"b) $I=4{,}0\ \text{A}$ ; $P=704\ \text{W}$", r"c) $A=0{,}352\ \text{kWh}$"],
  r"Nhận dạng: đề cho <strong>nhãn định mức</strong> nhưng thiết bị dùng ở <strong>hiệu điện thế khác</strong>, kèm <strong>coi R không đổi</strong> → tìm $R$ từ nhãn, rồi tính $I$, $P$ theo $U$ thực."),
 sol(R3, [
  ("Cường độ dòng điện",
   [P("Mạch kín có cả điện trở trong :"), M(r"I=\dfrac{\mathcal{E}}{R+r}"), M(r"I=\dfrac{6{,}0}{2{,}6+0{,}40}"), A(r"I=2{,}0\ \text{A}")]),
  ("Hiệu điện thế mạch ngoài",
   [M(r"U=IR=2{,}0\cdot2{,}6"), A(r"U=5{,}2\ \text{V}")]),
  ("Công suất của nguồn",
   [P(r"Nguồn đẩy dòng điện qua cả mạch kín, nên dùng suất điện động :"), M(r"P_{ng}=\mathcal{E}I"), M(r"P_{ng}=6{,}0\cdot2{,}0"), A(r"P_{ng}=12\ \text{W}")]),
  ("Công suất mạch ngoài nhận",
   [P("Mạch ngoài nhận công suất theo hiệu điện thế hai cực :"), M(r"P_R=UI"), M(r"P_R=5{,}2\cdot2{,}0"), A(r"P_R=10{,}4\ \text{W}")]),
  ("Công suất toả nhiệt trong nguồn",
   [M(r"P_r=I^{2}r"), M(r"P_r=2{,}0^{2}\cdot0{,}40"), A(r"P_r=1{,}6\ \text{W}")]),
  ("Công của nguồn trong 5 phút",
   [P(r"$t=5\cdot60=300\ \text{s}$ để ra jun :"), M(r"A_{ng}=P_{ng}t"), M(r"A_{ng}=12\cdot300"), A(r"A_{ng}=3600\ \text{J}=3{,}6\ \text{kJ}")]),
  ("Kiểm tra",
   [P(r"Cân bằng : $P_R+P_r=10{,}4+1{,}6=12\ \text{W}=P_{ng}$ ✓."),
    P(r"Cách khác : $U=\mathcal{E}-Ir=6{,}0-2{,}0\cdot0{,}40=5{,}2\ \text{V}$ ✓."),
    P(r"$I=2{,}0\ \text{A}$ nhỏ hơn $\mathcal{E}/R\approx2{,}3\ \text{A}$ vì còn $r$ ✓.")])],
  [r"a) $I=2{,}0\ \text{A}$", r"b) $P_{ng}=12\ \text{W}$ ; $P_R=10{,}4\ \text{W}$ ; $P_r=1{,}6\ \text{W}$", r"c) $A_{ng}=3600\ \text{J}$"],
  r"Nhận dạng: đề cho <strong>$\mathcal{E}$, $r$, $R$</strong> và hỏi riêng công suất <strong>của nguồn, mạch ngoài, trong nguồn</strong> → tìm $I$ trước, rồi mỗi công suất một công thức riêng."),
 sol(R4, [
  ("Tìm R từ hiệu suất",
   [P(r"Mạch ngoài chỉ có biến trở nên $H=\dfrac{R}{R+r}$ :"), M(r"0{,}80=\dfrac{R}{R+0{,}75}"), M(r"0{,}80R+0{,}60=R"), M(r"R=\dfrac{0{,}60}{0{,}20}"), A(r"R=3{,}0\ \Omega")]),
  ("Cường độ dòng điện",
   [M(r"I=\dfrac{\mathcal{E}}{R+r}"), M(r"I=\dfrac{12}{3{,}0+0{,}75}"), A(r"I=3{,}2\ \text{A}")]),
  ("Hiệu điện thế hai cực",
   [M(r"U=IR=3{,}2\cdot3{,}0"), A(r"U=9{,}6\ \text{V}"), P(r"Kiểm bằng hiệu suất : $U=H\mathcal{E}=0{,}80\cdot12=9{,}6\ \text{V}$ ✓.")]),
  ("Năng lượng có ích trong 10 phút",
   [P(r"$t=10\cdot60=600\ \text{s}$ :"), M(r"A_{\text{ích}}=UIt"), M(r"A_{\text{ích}}=9{,}6\cdot3{,}2\cdot600"), A(r"A_{\text{ích}}\approx1{,}84\cdot10^{4}\ \text{J}\approx18{,}4\ \text{kJ}")]),
  ("Năng lượng toả ra trong bộ pin",
   [M(r"A_{\text{hp}}=I^{2}rt"), M(r"A_{\text{hp}}=3{,}2^{2}\cdot0{,}75\cdot600"), A(r"A_{\text{hp}}\approx4{,}61\cdot10^{3}\ \text{J}\approx4{,}61\ \text{kJ}")]),
  ("Kiểm tra",
   [M(r"A_{\text{tp}}=\mathcal{E}It=12\cdot3{,}2\cdot600=23\,040\ \text{J}"),
    P(r"$A_{\text{ích}}+A_{\text{hp}}=18\,432+4608=23\,040\ \text{J}$ ✓."),
    P(r"$\dfrac{A_{\text{ích}}}{A_{\text{tp}}}=\dfrac{18\,432}{23\,040}=0{,}80$ ✓ khớp hiệu suất đề cho.")])],
  [r"a) $R=3{,}0\ \Omega$", r"b) $I=3{,}2\ \text{A}$ ; $U=9{,}6\ \text{V}$", r"c) $A_{\text{ích}}\approx18{,}4\ \text{kJ}$ ; $A_{\text{hp}}\approx4{,}61\ \text{kJ}$"],
  r"Nhận dạng: đề cho <strong>hiệu suất nguồn</strong> và hỏi <strong>R, dòng điện, năng lượng có ích hay hao phí</strong> → $H=\dfrac{R}{R+r}$ giải ngược tìm $R$, rồi $I=\dfrac{\mathcal{E}}{R+r}$ và tách $A_{\text{ích}}$, $A_{\text{hp}}$."),
 sol(R5, [
  ("Dòng điện khi đèn sáng",
   [P("Cầu chì nối tiếp với đèn nên cùng một dòng điện :"), M(r"I=\dfrac{\mathcal{E}}{R_{\text{đèn}}+r}"), M(r"I=\dfrac{12}{2{,}37+0{,}030}"), A(r"I=5{,}0\ \text{A}")]),
  ("Chọn cầu chì",
   [P(r"Loại $3\ \text{A}$ nhỏ hơn dòng làm việc nên đứt ngay khi bật đèn."),
    P(r"Loại $30\ \text{A}$ quá lớn : dây đã nóng cháy mà cầu chì chưa đứt."),
    P(r"Cần loại lớn hơn dòng làm việc một chút :"), A(r"T:Chọn cầu chì <strong>$7{,}5\ \text{A}$</strong>.")]),
  ("Dòng điện khi đoản mạch",
   [P(r"Điện trở trong vẫn nằm trong mạch :"), M(r"I_{\text{cố}}=\dfrac{\mathcal{E}}{R_{\text{ngoài}}+r}"), M(r"I_{\text{cố}}=\dfrac{12}{0{,}010+0{,}030}"), A(r"I_{\text{cố}}=300\ \text{A}")]),
  ("Nhiệt toả ra trong ắc quy",
   [M(r"P_r=I_{\text{cố}}^{2}r"), M(r"P_r=300^{2}\cdot0{,}030"), A(r"P_r=2700\ \text{W}=2{,}7\ \text{kW}")]),
  ("So với dòng định mức của cầu chì",
   [M(r"\dfrac{I_{\text{cố}}}{I_{\text{đm}}}=\dfrac{300}{7{,}5}"), A(r"\dfrac{I_{\text{cố}}}{I_{\text{đm}}}=40"),
    A(r"T:Dòng lúc chập gấp <strong>40 lần</strong> định mức nên cầu chì <strong>đứt</strong>, ngắt mạch trước khi dây và ắc quy quá nóng.")]),
  ("Kiểm tra",
   [P(r"Dòng đoản mạch $300\ \text{A}$ lớn hơn dòng làm việc $5{,}0\ \text{A}$ gấp $60$ lần : đúng với đoản mạch."),
    P(r"Nếu bỏ qua $r$ sẽ ra $1200\ \text{A}$ : sai, vì $r$ vẫn nằm trong mạch."),
    P(r"Công suất $2{,}7\ \text{kW}$ toả ngay trong ắc quy nhỏ : cháy, nổ nếu không có cầu chì.")])],
  [r"a) $I=5{,}0\ \text{A}$ ; chọn cầu chì $7{,}5\ \text{A}$", r"b) $I_{\text{cố}}=300\ \text{A}$ ; $P_r=2{,}7\ \text{kW}$", r"c) Gấp $40$ lần ; cầu chì đứt"],
  r"Nhận dạng: đề nói <strong>chập, đoản mạch, nối thẳng hai cực</strong> → $R\to0$, $I=\dfrac{\mathcal{E}}{R+r}$ rất lớn ; so với <strong>dòng định mức</strong> để biết cầu chì có đứt."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>công suất, thời gian dùng</b>, hỏi <b>jun hay số điện</b> → <b>A = Pt</b>, đổi <b>kWh</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi thời gian", r"Thời gian dùng mỗi tối là bao nhiêu giây?", 2700, "s", 1,
       loi=r"Để nguyên số phút rồi nhân với công suất, hoặc đổi nhầm $1$ phút thành $100$ giây."),
  buoc("Điện năng mỗi tối theo jun", r"Điện năng mỗi tối là bao nhiêu triệu jun (MJ)?", 5.4, "MJ", 0.05,
       loi=r"Nhân công suất với thời gian tính bằng phút, kết quả nhỏ đi $60$ lần ; hoặc nhân hiệu điện thế $220\ \text{V}$ với thời gian.",
       ke=[(r"Nhân công suất với thời gian tính bằng giây : $A=Pt$", True),
           (r"Nhân công suất với thời gian tính bằng phút", r"Ra jun thì $t$ phải là giây ; dùng phút thì kết quả nhỏ đi $60$ lần."),
           (r"Nhân hiệu điện thế $220\ \text{V}$ với thời gian", r"$U\cdot t$ không phải điện năng ; còn thiếu cường độ dòng điện.")]),
  buoc("Đổi ra kWh", r"Điện năng mỗi tối là bao nhiêu kWh?", 1.5, "kWh", 0.02,
       loi=r"Chia số jun cho $1000$ (ra kJ) rồi gọi là kWh.",
       ke=[(r"Chia số jun cho $3{,}6\cdot10^{6}$", True),
           (r"Chia số jun cho $1000$", r"Chia $1000$ chỉ ra kJ ; $1\ \text{kWh}=1000\ \text{W}\cdot3600\ \text{s}$."),
           (r"Nhân số jun với $3{,}6\cdot10^{6}$", r"$1$ kWh lớn hơn $1$ J rất nhiều nên số kWh phải nhỏ hơn số jun.")]),
  buoc("Điện năng trong 30 ngày", r"Trong $30$ ngày bình tiêu thụ bao nhiêu kWh?", 45, "kWh", 0.5,
       loi=r"Nhân $30$ với số jun nhưng vẫn ghi đơn vị kWh, hoặc nhân $30$ với công suất mà chưa nhân thời gian dùng.",
       ke=[(r"Nhân điện năng một tối (kWh) với $30$", True),
           (r"Nhân số jun với $30$ rồi ghi đơn vị kWh", r"Số jun nhân $30$ vẫn là jun ; phải đổi sang kWh trước."),
           (r"Nhân công suất $2000\ \text{W}$ với $30$", r"Mới nhân công suất với số ngày, chưa nhân với thời gian dùng mỗi ngày.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>nhãn định mức</b>, dùng ở <b>U khác</b>, <b>coi R không đổi</b> → <b>R từ nhãn</b>, tính với <b>U thực</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điện trở của bàn là từ nhãn", r"Điện trở của bàn là bằng bao nhiêu?", 44, "Ω", 0.5,
       loi=r"Dùng $R=\dfrac{P}{U^{2}}$ hoặc $R=\dfrac{U}{P}$ : đảo vị trí các đại lượng, sai đơn vị ôm."),
  buoc("Cường độ dòng điện thực", r"Cường độ dòng điện chạy qua bàn là khi cắm vào ổ cắm đó?", 4.0, "A", 0.05,
       loi=r"Lấy $I=\dfrac{P_{\text{đm}}}{U_{\text{đm}}}$ : đó là dòng định mức, chỉ đúng khi dùng đúng $220\ \text{V}$.",
       ke=[(r"Dùng định luật Ôm với hiệu điện thế thực : $I=\dfrac{U}{R}$", True),
           (r"Lấy dòng định mức $I=\dfrac{P_{\text{đm}}}{U_{\text{đm}}}$", r"Đó là dòng khi dùng đúng $220\ \text{V}$ ; ổ cắm chỉ có $176\ \text{V}$ nên dòng khác."),
           (r"Lấy $I=\dfrac{U_{\text{đm}}}{R}$", r"Vẫn dùng hiệu điện thế định mức thay vì hiệu điện thế thực của ổ cắm.")]),
  buoc("Công suất thực", r"Công suất thực của bàn là ở ổ cắm đó?", 704, "W", 5,
       loi=r"Coi công suất tỉ lệ với hiệu điện thế : lấy $80\ \%$ công suất ghi trên nhãn.",
       ke=[(r"Nhân hiệu điện thế thực với dòng điện thực : $P=UI$", True),
           (r"Giảm công suất tỉ lệ với hiệu điện thế", r"$P=\dfrac{U^{2}}{R}$ tỉ lệ với $U^{2}$ chứ không tỉ lệ với $U$."),
           (r"Giữ nguyên công suất ghi trên nhãn", r"Công suất trên nhãn chỉ có khi dùng đúng $220\ \text{V}$.")]),
  buoc("Điện năng trong 30 phút", r"Điện năng bàn là tiêu thụ trong $30$ phút, theo kWh?", 0.352, "kWh", 0.005,
       loi=r"Dùng công suất ghi trên nhãn thay cho công suất thực, hoặc nhân công suất (kW) với số phút mà không đổi ra giờ.",
       ke=[(r"Nhân công suất thực (kW) với thời gian (h)", True),
           (r"Nhân công suất ghi trên nhãn với thời gian", r"Bàn là đang chạy với công suất thực, nhỏ hơn công suất ghi trên nhãn."),
           (r"Nhân công suất thực (kW) với $30$ phút", r"Ra kWh thì thời gian phải đổi sang giờ.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>ε, r, R</b> và hỏi công suất <b>của nguồn, mạch ngoài, trong nguồn</b> → tìm <b>I</b> trước, mỗi công suất một công thức.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Cường độ dòng điện", r"Cường độ dòng điện trong mạch bằng bao nhiêu?", 2.0, "A", 0.05,
       loi=r"Bỏ qua điện trở trong : chia suất điện động cho riêng $R$."),
  buoc("Hiệu điện thế mạch ngoài", r"Hiệu điện thế giữa hai cực của bộ pin bằng bao nhiêu?", 5.2, "V", 0.05,
       loi=r"Coi hiệu điện thế hai cực bằng suất điện động ; điều đó chỉ đúng khi không có dòng điện.",
       ke=[(r"Nhân dòng điện với điện trở mạch ngoài : $U=IR$", True),
           (r"Lấy $U=\mathcal{E}$", r"Chỉ đúng khi $I=0$ ; có dòng điện thì một phần suất điện động mất trên điện trở trong."),
           (r"Nhân dòng điện với điện trở trong : $U=Ir$", r"Đó là hiệu điện thế rơi trên điện trở trong, không phải giữa hai cực.")]),
  buoc("Công suất của nguồn", r"Công suất của nguồn bằng bao nhiêu?", 12, "W", 0.1,
       loi=r"Lấy công suất mạch ngoài $UI$ làm công suất của nguồn, bỏ sót phần nhiệt trong nguồn.",
       ke=[(r"Nhân suất điện động với dòng điện : $P_{ng}=\mathcal{E}I$", True),
           (r"Nhân hiệu điện thế hai cực với dòng điện : $UI$", r"$UI$ là công suất của mạch ngoài, chưa tính phần toả nhiệt trong nguồn."),
           (r"Tính $I^{2}R$", r"$I^{2}R$ cũng chỉ là công suất mạch ngoài.")]),
  buoc("Công suất mạch ngoài nhận", r"Công suất mạch ngoài nhận được bằng bao nhiêu?", 10.4, "W", 0.1,
       loi=r"Lấy εI (công suất cả nguồn) làm công suất mạch ngoài, hoặc lấy công suất toả nhiệt trong nguồn.",
       ke=[(r"Nhân hiệu điện thế hai cực với dòng điện : $P_R=UI$", True),
           (r"Nhân suất điện động với dòng điện", r"Đó là công suất của nguồn, gồm cả phần toả nhiệt trong nguồn."),
           (r"Tính $I^{2}r$", r"Đó là nhiệt toả trong nguồn, không phải phần mạch ngoài nhận.")]),
  buoc("Công suất toả nhiệt trong nguồn", r"Công suất toả nhiệt trong bộ pin bằng bao nhiêu?", 1.6, "W", 0.05,
       loi=r"Dùng $I^{2}R$ với điện trở mạch ngoài thay cho điện trở trong.",
       ke=[(r"Tính $P_r=I^{2}r$ với điện trở trong", True),
           (r"Tính $I^{2}R$ với điện trở mạch ngoài", r"$R$ là mạch ngoài ; nhiệt trong nguồn toả trên điện trở trong $r$."),
           (r"Tính $\mathcal{E}I$", r"Đó là công suất cả nguồn, không riêng phần toả nhiệt trong nguồn.")]),
  buoc("Công của nguồn trong 5 phút", r"Công của nguồn trong $5$ phút là bao nhiêu kilôjun?", 3.6, "kJ", 0.05,
       loi=r"Dùng $t=5$ thay vì $300$ giây, hoặc nhân công suất mạch ngoài với thời gian.",
       ke=[(r"Nhân công suất của nguồn với $300\ \text{s}$", True),
           (r"Nhân công suất của nguồn với $5$", r"Ra jun thì thời gian phải tính bằng giây."),
           (r"Nhân công suất mạch ngoài với $300\ \text{s}$", r"Đó là năng lượng mạch ngoài nhận, không phải công của nguồn.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>hiệu suất nguồn</b>, hỏi <b>R, dòng điện, năng lượng có ích</b> → <b>H = R/(R + r)</b>, giải ngược.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Tìm R từ hiệu suất", r"Biến trở $R$ phải đặt bằng bao nhiêu để $H=80\ \%$?", 3.0, "Ω", 0.05,
       loi=r"Dùng $H=\dfrac{r}{R+r}$ (đó là tỉ lệ hao phí, không phải hiệu suất) hoặc coi $R=H\cdot r$."),
  buoc("Cường độ dòng điện", r"Cường độ dòng điện trong mạch bằng bao nhiêu?", 3.2, "A", 0.05,
       loi=r"Bỏ qua điện trở trong : chia suất điện động cho riêng $R$.",
       ke=[(r"Dùng định luật Ôm cho toàn mạch : $I=\dfrac{\mathcal{E}}{R+r}$", True),
           (r"Lấy $I=\dfrac{\mathcal{E}}{R}$", r"Bỏ sót điện trở trong, dòng tính ra lớn hơn thực tế."),
           (r"Lấy $I=\dfrac{\mathcal{E}}{r}$", r"Đó là dòng khi đoản mạch ($R\to0$), không phải mạch đang xét.")]),
  buoc("Hiệu điện thế hai cực", r"Hiệu điện thế giữa hai cực của bộ pin bằng bao nhiêu?", 9.6, "V", 0.1,
       loi=r"Lấy $U=\mathcal{E}-IR$ (trừ nhầm điện trở ngoài) thay cho $\mathcal{E}-Ir$, hoặc lấy $U=Ir$.",
       ke=[(r"Nhân dòng điện với điện trở mạch ngoài : $U=IR$", True),
           (r"Lấy $U=\mathcal{E}-IR$", r"Trừ nhầm : phần mất đi trong nguồn là $Ir$ chứ không phải $IR$."),
           (r"Lấy $U=Ir$", r"Đó là hiệu điện thế rơi trên điện trở trong.")]),
  buoc("Năng lượng có ích trong 10 phút", r"Năng lượng có ích mạch ngoài nhận trong $10$ phút là bao nhiêu kilôjun?", 18.4, "kJ", 0.1,
       loi=r"Dùng $\mathcal{E}It$ (toàn phần) thay cho $UIt$, hoặc để $t=10$ thay vì $600$ giây.",
       ke=[(r"Tính $UIt$ với $t=600\ \text{s}$", True),
           (r"Tính $\mathcal{E}It$", r"Đó là năng lượng toàn phần của nguồn, gồm cả phần hao phí."),
           (r"Tính $UIt$ với $t=10$", r"Ra jun thì thời gian phải tính bằng giây.")]),
  buoc("Năng lượng toả ra trong bộ pin", r"Năng lượng toả ra trong bộ pin trong $10$ phút là bao nhiêu kilôjun?", 4.61, "kJ", 0.05,
       loi=r"Dùng $I^{2}Rt$ (điện trở ngoài) thay cho $I^{2}rt$.",
       ke=[(r"Tính $I^{2}rt$ với điện trở trong", True),
           (r"Tính $I^{2}Rt$ với điện trở mạch ngoài", r"$R$ là mạch ngoài ; nhiệt trong bộ pin toả trên điện trở trong $r$."),
           (r"Lấy $80\ \%$ năng lượng có ích", r"Cố định : $80\ \%$ là tỉ lệ có ích so với toàn phần ; hao phí là $20\ \%$ toàn phần (bằng $25\ \%$ phần có ích), không phải $80\ \%$ phần có ích.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>chập, đoản mạch</b> hay <b>chọn cầu chì</b> → <b>I = ε/(R + r)</b> với R rất nhỏ, so với <b>dòng định mức</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Dòng điện khi đèn sáng", r"Cường độ dòng điện khi đèn sáng bình thường bằng bao nhiêu?", 5.0, "A", 0.05,
       loi=r"Bỏ qua điện trở trong : chia suất điện động cho riêng điện trở đèn."),
  buoc("Chọn cầu chì", r"Dòng định mức của cầu chì nên chọn là bao nhiêu (trong ba loại đề cho)?", 7.5, "A", 0.05,
       loi=r"Chọn loại lớn nhất để cầu chì không bao giờ đứt : khi chập, dây đã nóng cháy mà cầu chì chưa kịp đứt.",
       ke=[(r"Chọn loại có dòng định mức lớn hơn dòng làm việc một chút", True),
           (r"Chọn loại lớn nhất cho an toàn", r"Cầu chì quá lớn không đứt khi dòng đã vượt mức dây chịu được ; cháy dây trước khi cầu chì đứt."),
           (r"Chọn loại nhỏ hơn dòng làm việc", r"Cầu chì sẽ đứt ngay khi bật đèn bình thường.")]),
  buoc("Dòng điện khi đoản mạch", r"Cường độ dòng điện lúc dây chập bằng bao nhiêu?", 300, "A", 3,
       loi=r"Bỏ qua điện trở trong : chia suất điện động cho riêng điện trở chỗ chập, được số lớn hơn thực tế nhiều lần.",
       ke=[(r"Dùng định luật Ôm toàn mạch với điện trở mạch ngoài còn $0{,}010\ \Omega$", True),
           (r"Chia suất điện động cho riêng $0{,}010\ \Omega$", r"Điện trở trong $0{,}030\ \Omega$ vẫn nằm trong mạch, lớn hơn cả điện trở chỗ chập."),
           (r"Chia suất điện động cho điện trở đèn cộng điện trở trong", r"Đèn đã bị nối tắt nên không còn nằm trong mạch ngoài.")]),
  buoc("Nhiệt toả ra trong ắc quy", r"Công suất toả nhiệt trong ắc quy lúc chập là bao nhiêu kilôoát?", 2.7, "kW", 0.05,
       loi=r"Tính nhiệt trên điện trở chỗ chập thay vì trên điện trở trong của ắc quy.",
       ke=[(r"Tính $I^{2}r$ với điện trở trong của ắc quy", True),
           (r"Tính $I^{2}$ nhân điện trở chỗ chập", r"Đó là nhiệt toả ở chỗ chập, câu hỏi hỏi nhiệt trong ắc quy."),
           (r"Tính $\mathcal{E}I$", r"Đó là công suất cả nguồn, gồm cả phần toả ở chỗ chập.")]),
  buoc("So với dòng định mức của cầu chì", r"Dòng lúc chập gấp bao nhiêu lần dòng định mức của cầu chì đã chọn?", 40, "lần", 0.5,
       loi=r"Chia ngược (dòng định mức chia dòng chập), được tỉ số nhỏ hơn $1$ nên không nhận ra cầu chì đứt.",
       ke=[(r"Chia dòng lúc chập cho dòng định mức của cầu chì", True),
           (r"Chia dòng định mức của cầu chì cho dòng lúc chập", r"Được tỉ số nhỏ hơn $1$ ; không cho biết dòng đã vượt định mức bao nhiêu lần."),
           (r"Cộng dòng lúc chập với dòng làm việc rồi chia", r"Đèn đã bị nối tắt nên không còn dòng làm việc cộng thêm.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 44, "Bài 25. Năng lượng điện và công suất điện", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["dang_bai"][4]["form"] = "ly_thuyet"        # chủ đề 194 chỉ có câu hiệu suất; dạng đoản mạch/cầu chì không có câu bài tập tương ứng
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code) — đã tự giải lại bằng Python 10/10/2026"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
