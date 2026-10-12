"""Bài tập mẫu bài 84 — Bài 6. Phản xạ toàn phần (KHTN 9). Dựng 4 dạng + hình + lời giải + buoc[] → 84.json.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-84.py   (idempotent: ghi lại toàn bộ 84.json, review.checked=false)
Danh sách dạng: scripts/data/bai-tap-mau/84.dang.md. Mọi số liệu tính ở đầu file, có assert."""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "84.json")
T82 = "Điều kiện xảy ra phản xạ toàn phần"
T83 = "Tính góc tới hạn, ứng dụng cáp quang"
sin, cos, asin, rad, deg = math.sin, math.cos, math.asin, math.radians, math.degrees

# ───────────── Số liệu (tính + kiểm) ─────────────
# Dạng 1: nhựa n = 1,49 ra không khí và ra nước (1,33)
n1a, nw = 1.49, 1.33
s1a = 1 / n1a; i1a = deg(asin(s1a))
s1b = nw / n1a; i1b = deg(asin(s1b))
assert abs(s1a - 0.671) < 5e-4 and abs(i1a - 42.2) < 0.05 and abs(s1b - 0.893) < 5e-4 and abs(i1b - 63.2) < 0.05
assert i1b > i1a                                                     # hai chiết suất gần nhau → góc tới hạn lớn
assert abs(deg(asin(1 / n1a)) - i1b) > 20                           # dùng 1/n khi ra nước (cách sai) cho số khác
assert n1a / nw > 1                                                  # lật tỉ số → sin > 1
r1_demo = deg(asin(n1a * sin(rad(30))))                              # tia mẫu hình mô phỏng (không phải đáp số)
assert abs(r1_demo - 48.17) < 0.05

# Dạng 2: chất lỏng n = 1,40 ra không khí; tia 1 hợp mặt 40°, tia 2 hợp mặt 60°
n2l = 1.40
ith2 = deg(asin(1 / n2l))
ia, ib = 90 - 40, 90 - 60
sin_rb = n2l * sin(rad(ib)); rb = deg(asin(sin_rb))
assert abs(ith2 - 45.58) < 0.01 and ia == 50 and ib == 30
assert ia > ith2 and ib < ith2                                       # tia 1 phản xạ toàn phần, tia 2 ló
assert abs(sin_rb - 0.70) < 1e-9 and abs(rb - 44.43) < 0.01
assert n2l * sin(rad(40)) < 1 and abs(n2l * sin(rad(60)) - 1.2124) < 1e-3     # dùng nhầm 40°/60° làm góc tới
assert 40 < ith2 and 60 > ith2                                       # nếu lấy góc với mặt: kết luận đảo ngược → đúng là bẫy
assert rb > ib                                                       # ra môi trường kém → r > i
assert abs(deg(asin(sin(rad(ib)) / n2l)) - rb) > 10                  # đảo tỉ số cho số khác (12,3°)
r2_demo = deg(asin(n2l * sin(rad(15))))                              # tia mẫu hình mô phỏng
assert abs(r2_demo - 21.22) < 0.05

# Dạng 3: bán trụ, i_th = 40° trong không khí → n; nhúng nước → i'_th; tia 50°
ith3 = 40.0
n3 = 1 / sin(rad(ith3))
s3 = nw / n3; ith3b = deg(asin(s3))
assert abs(n3 - 1.5557) < 1e-3 and abs(s3 - 0.8549) < 1e-3 and abs(ith3b - 58.75) < 0.01
assert 50 < ith3b and 50 > ith3                                      # trước nhúng: phản xạ toàn phần; sau nhúng: ló
assert abs(deg(asin(nw / 1.56)) - ith3b) < 0.3                       # làm tròn n = 1,56 vẫn nằm trong sai số 0,5°
assert abs(deg(asin(1 / n3)) - ith3b) > 15                           # dùng 1/n (quên nước) → 40°
assert n3 / nw > 1 and 1 / sin(rad(ith3)) > 1                        # lật tỉ số → sin > 1
assert nw > 1

# Dạng 4: sợi quang lõi 1,50, tia hợp trục 30°
n4, alpha4, n4v = 1.50, 30.0, 1.40
i4 = 90 - alpha4
n2max = n4 * sin(rad(i4))
ith4 = deg(asin(n4v / n4)); amax4 = 90 - ith4
assert i4 == 60 and abs(n2max - 1.2990) < 1e-3 and abs(ith4 - 68.96) < 0.01 and abs(amax4 - 21.04) < 0.01
assert i4 < ith4 and n4v > n2max                                     # vỏ 1,40: không phản xạ toàn phần
assert abs(n4 * sin(rad(alpha4)) - n2max) > 0.5                      # dùng góc với trục (0,75)
assert abs(deg(asin(1 / n4)) - ith4) > 1.5                           # dùng 1/n lõi (41,8°)
assert n4 / n4v > 1                                                  # lật tỉ số → sin > 1

# ───────────── Hình ─────────────
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'

def tx(x, y, inner, c="currentColor", size=15, anchor="start", weight="700"):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{inner}</text>'

def sb(base, idx, rest="", size=15):
    """ký hiệu nghiêng + chỉ số dưới (tspan, không dùng chỉ số Unicode)"""
    return f'{it_(base)}<tspan dy="4" font-size="{size - 4}">{idx}</tspan><tspan dy="-4">{rest}</tspan>'

def ray(x0, y0, x1, y1, c, w=2.8, frac=0.5, op=1.0, L=11):
    """Tia sáng: đoạn thẳng + đầu V 30° đặt ở vị trí `frac` dọc tia (không dùng marker-end)."""
    px, py = x0 + (x1 - x0) * frac, y0 + (y1 - y0) * frac
    return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{c}" stroke-width="{w}" opacity="{op}" stroke-linecap="round"/>'
            + chevron(px, py, x1 - x0, y1 - y0, c, 2.4, L))

def scene(cx, Y, hw, hu, hd, L, i=None, r=None, refl=False, bt=False, top_fill=None, bot_fill="rgba(56,189,248,.16)", ilab=None, rlab=None, nd=None, ipos="left"):
    """Mặt phân cách nằm ngang tại y=Y, tâm tới I=(cx,Y). Môi trường 1 (chiết quang hơn) ở dưới.
    i = góc tới (độ, so với pháp tuyến), r = góc khúc xạ. bt=True: khối bán trụ bán kính L (tia đi theo bán kính)."""
    b = ""
    ybot = Y + (L if bt else (nd if nd is not None else hd))
    if top_fill:
        b += f'<rect x="{cx - hw}" y="{Y - hu}" width="{2 * hw}" height="{hu}" fill="{top_fill}" stroke="none"/>'
    if bt:
        b += f'<path d="M{cx - L},{Y} A{L},{L} 0 0 0 {cx + L},{Y} Z" fill="{bot_fill}" stroke="currentColor" stroke-width="2"/>'
    else:
        b += f'<rect x="{cx - hw}" y="{Y}" width="{2 * hw}" height="{hd}" fill="{bot_fill}" stroke="none"/>'
    b += seg(cx - hw, Y, cx + hw, Y, "currentColor", 2.4)
    b += seg(cx, Y - hu, cx, ybot, "currentColor", 1.3, "5 4", .55)
    geo = {}
    if i is not None:
        s, c = sin(rad(i)), cos(rad(i))
        P0 = (cx - L * s, Y + L * c); geo["P0"] = P0; geo["I"] = (cx, Y)
        b += ray(*P0, cx, Y, ORG, frac=.45)
        b += arc(cx, Y, 34, 270 - i, 270, ORG, 1.8)
        if ilab:
            if ipos == "right":
                b += tx(cx + 8, Y + 38, ilab, ORG, 14)
            else:
                a = rad(270 - i - 13); b += tx(cx + 48 * cos(a), Y - 48 * sin(a) + 5, ilab, ORG, 14, "end")
        if refl:
            Pf = (cx + L * s, Y + L * c); geo["Pf"] = Pf
            b += ray(cx, Y, *Pf, GRN, w=2.6, frac=.62, op=.9)
    if r is not None:
        Lr = L * (0.95 if bt else 0.92)
        Pr = (cx + Lr * sin(rad(r)), Y - Lr * cos(rad(r))); geo["Pr"] = Pr
        b += ray(cx, Y, *Pr, RED, frac=.68)
        b += arc(cx, Y, 42, 90 - r, 90, RED, 1.8)
        if rlab:
            if r > 80:
                b += tx(cx + 48, Y - 50 + 5, rlab, RED, 14)
            else:
                a = rad(90 - r / 2); b += tx(cx + 60 * cos(a), Y - 60 * sin(a) + 5, rlab, RED, 14, "middle")
    return b, geo

def dotpath(pts, c, dur, rr=5.5, op=1.0):
    """Chấm chạy MỘT lần khi bấm (begin=indefinite, fill=freeze), tốc độ đều theo chiều dài (keyTimes)."""
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    tot = sum(lens); kt = [0.0]
    for L_ in lens: kt.append(kt[-1] + L_ / tot)
    kts = ";".join(f"{k:.3f}" for k in kt)
    anim = "".join(f'<animate attributeName="{a}" values="{";".join(f"{p[n]:.1f}" for p in pts)}" keyTimes="{kts}" dur="{dur}s" begin="indefinite" fill="freeze"/>'
                   for a, n in (("cx", 0), ("cy", 1)))
    return f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="{rr}" fill="{c}" stroke="currentColor" stroke-width="1.2" opacity="{op}">{anim}</circle>'

def ilab_t(): return it_("i")
def th_lab(base, extra): return f'{it_(base)}<tspan dy="4" font-size="10">th</tspan><tspan dy="-4"> {extra}</tspan>'

# --- Dạng 1 ---
def d1(k):
    if k == 0:
        cx, Y = 210, 125
        b, g = scene(cx, Y, 190, 100, 110, 90, i=30, r=r1_demo, refl=True, ilab=it_("i"), rlab=it_("r"))
        b += tx(28, 45, "Không khí  " + sb("n", "2", " = 1"), "currentColor", 15)
        b += tx(28, 225, "Nhựa  " + sb("n", "1", " = 1,49"), "currentColor", 15)
        b += tx(392, 45, "tia mẫu: " + it_("i") + " = 30°", ORG, 14, "end")
        b += dotpath([g["P0"], g["I"], g["Pr"]], ORG, 3.0)
        b += dotpath([g["P0"], g["I"], g["Pf"]], GRN, 3.0, op=.85)
        return fig("d1-0", "0 0 420 250", "Tia sáng trong khối nhựa tới mặt phân cách với không khí: một phần ló ra, một phần phản xạ lại vào nhựa", b,
                   "Mô phỏng (bấm Chạy mô phỏng): một tia mẫu có góc tới 30°.<br>Tia tới màu cam, tia ló màu đỏ, tia phản xạ màu xanh lá.<br>Chấm sáng chạy một lần theo từng tia.")
    b = ""
    for cx, ttl, top in ((105, "a) Ra không khí", "Không khí  " + sb("n", "2", " = 1")), (315, "b) Ra nước", "Nước  " + sb("n", "2", " = 1,33"))):
        s, g = scene(cx, 120, 95, 48, 95, 70, i=45, r=90, ilab=th_lab("i", "= ?"), rlab=it_("r") + " = 90°", nd=70)
        b += s + tx(cx - 95 + 4, 24, ttl, "currentColor", 15)
        b += tx(cx - 95 + 4, 60, top, "currentColor", 14)
        b += tx(cx - 95 + 4, 208, "Nhựa  " + sb("n", "1", " = 1,49"), "currentColor", 14)
    return fig("d1-2", "0 0 420 225", "Hai sơ đồ: ánh sáng đi từ nhựa ra không khí và từ nhựa ra nước; tia khúc xạ đi sát mặt phân cách tại góc tới hạn", b,
               "Dữ kiện: hai trường hợp, cùng khối nhựa.<br>Góc tới hạn: tia khúc xạ đi sát mặt phân cách.<br>Hình minh hoạ, góc vẽ không đúng số đo.")

# --- Dạng 2 ---
def d2(k):
    if k == 0:
        cx, Y = 210, 125
        b, g = scene(cx, Y, 190, 100, 110, 90, i=15, r=r2_demo, refl=True, ilab=it_("i"), rlab=it_("r"))
        b += tx(28, 45, "Không khí  " + sb("n", "2", " = 1"), "currentColor", 15)
        b += tx(28, 225, "Chất lỏng  " + sb("n", "1", " = 1,40"), "currentColor", 15)
        b += tx(392, 45, "tia mẫu: " + it_("i") + " = 15°", ORG, 14, "end")
        b += dotpath([g["P0"], g["I"], g["Pr"]], ORG, 3.0)
        b += dotpath([g["P0"], g["I"], g["Pf"]], GRN, 3.0, op=.85)
        return fig("d2-0", "0 0 420 250", "Tia sáng trong chất lỏng tới mặt thoáng: một phần ló ra không khí, một phần phản xạ lại", b,
                   "Mô phỏng (bấm Chạy mô phỏng): một tia mẫu có góc tới 15°.<br>Tia tới màu cam, tia ló màu đỏ, tia phản xạ màu xanh lá.<br>Chấm sáng chạy một lần theo từng tia.")
    b = ""
    for cx, ttl, ang in ((105, "a) Tia thứ nhất", 40), (315, "b) Tia thứ hai", 60)):
        i_ = 90 - ang
        s, g = scene(cx, 120, 95, 48, 95, 72, i=i_, ilab=it_("i") + " = ?", nd=70, ipos="right")
        # góc với mặt thoáng (phía trái, giữa mặt và tia tới)
        s += arc(cx, 120, 56, 180, 180 + ang, BLUE, 1.8)
        a = rad(180 + ang / 2); s += tx(cx + 74 * cos(a), 120 - 74 * sin(a) + 5, f"{ang}°", BLUE, 14, "middle")
        b += s + tx(cx - 95 + 4, 24, ttl, "currentColor", 15)
        b += tx(cx - 95 + 4, 60, "Không khí", "currentColor", 14)
        b += tx(cx - 95 + 4, 208, "Chất lỏng  " + sb("n", "1", " = 1,40"), "currentColor", 14)
    return fig("d2-2", "0 0 420 225", "Hai tia trong chất lỏng tới mặt thoáng, hợp với mặt thoáng các góc 40 độ và 60 độ; góc tới chưa biết", b,
               "Dữ kiện: góc xanh là góc giữa tia và mặt thoáng.<br>Góc tới cần tìm nằm giữa tia và pháp tuyến (nét đứt).")

# --- Dạng 3 ---
def d3(k):
    R = 85
    if k == 0:
        cx, Y = 210, 72
        R0 = 130
        b, g = scene(cx, Y, R0, 55, R0, R0, i=40, r=90, refl=True, bt=True, bot_fill="rgba(251,146,60,.16)", ilab=it_("i") + " = 40°", rlab=it_("r") + " = 90°")
        b += tx(28, 50, "Không khí", "currentColor", 15)
        b += tx(cx, Y + R0 - 14, "Khối bán trụ", "currentColor", 15, "middle")
        end = (cx + R0 * 0.95, Y)
        b += dotpath([g["P0"], g["I"], end], ORG, 3.0)
        b += dotpath([g["P0"], g["I"], g["Pf"]], GRN, 3.0, op=.85)
        return fig("d3-0", "0 0 420 215", "Khối bán trụ: tia laser đi theo bán kính tới tâm I của mặt phẳng; ở góc tới 40 độ tia ló đi sát mặt phẳng", b,
                   "Mô phỏng (bấm Chạy mô phỏng): khối đặt trong không khí, góc tới 40°.<br>Tia ló (đỏ) đi sát mặt phẳng; tia phản xạ màu xanh lá.<br>Tia laser đi theo bán kính nên không bị lệch ở mặt cong.")
    b = ""
    R = 100; cx = 260
    Y = 66
    s, g = scene(cx, Y, R, 30, R, R, i=40, r=90, refl=True, bt=True, bot_fill="rgba(251,146,60,.16)", ilab=th_lab("i", "= 40°"), rlab=it_("r") + " = 90°")
    b += s + tx(16, 20, "Ban đầu: trong không khí", "currentColor", 15)
    b += tx(16, Y - 6, "Không khí  " + sb("n", "", " = 1"), "currentColor", 14, weight="600")
    b += tx(16, Y + 70, "Khối bán trụ", "currentColor", 14, weight="600") + tx(16, Y + 92, sb("n", "", " = ?"), "currentColor", 14)
    Y = 246
    s, g = scene(cx, Y, R, 30, R, R, i=50, bt=True, bot_fill="rgba(251,146,60,.16)", top_fill="rgba(56,189,248,.14)", ilab=it_("i") + " = 50°")
    b += s + tx(16, 212, "Sau khi nhúng nước", "currentColor", 15)
    b += tx(16, Y - 6, "Nước  " + sb("n", "", " = 1,33"), "currentColor", 14, weight="600")
    b += tx(cx + 24, Y - 12, "tia ló?", RED, 15)
    b += tx(16, Y + 70, "Khối bán trụ", "currentColor", 14, weight="600") + tx(16, Y + 92, sb("n", "", " = ?"), "currentColor", 14)
    return fig("d3-2", "0 0 420 355", "Hai sơ đồ khối bán trụ: trong không khí với góc tới hạn 40 độ, và sau khi nhúng nước với tia tới 50 độ", b,
               "Dữ kiện: cùng một khối, hai môi trường thứ hai khác nhau.<br>Hình bên phải chưa biết tia có ló ra nước hay không.")

# --- Dạng 4 ---
def fibre_pts():
    t = math.tan(rad(alpha4)); hc = 80
    x0 = 70.0
    pts = [(x0, 130.0)]
    x = x0 + 40 / t; pts.append((x, 90.0))
    x += hc / t; pts.append((x, 170.0))
    x2 = 405.0; pts.append((x2, 170.0 - (x2 - x) * t))
    return pts

def fibre_base():
    b = '<rect x="10" y="40" width="400" height="50" fill="rgba(160,160,160,.2)" stroke="none"/>'
    b += '<rect x="10" y="170" width="400" height="50" fill="rgba(160,160,160,.2)" stroke="none"/>'
    b += '<rect x="10" y="90" width="400" height="80" fill="rgba(56,189,248,.16)" stroke="none"/>'
    b += seg(10, 90, 410, 90, "currentColor", 1.8) + seg(10, 170, 410, 170, "currentColor", 1.8)
    b += seg(10, 130, 410, 130, "currentColor", 1.2, "6 4", .5)
    b += tx(14, 70, "Vỏ  " + sb("n", "2", " = ?"), "currentColor", 14)
    b += tx(14, 200, "Vỏ", "currentColor", 14)
    b += tx(14, 162, "Lõi  " + sb("n", "1", " = 1,50"), "currentColor", 14)
    return b

def d4(k):
    pts = fibre_pts()
    b = fibre_base()
    for a, c in zip(pts, pts[1:]):
        b += ray(a[0], a[1], c[0], c[1], ORG, frac=.5)
    if k == 0:
        b += dotpath(pts, ORG, 4.0)
        return fig("d4-0", "0 0 420 250", "Sợi quang: tia sáng hợp với trục sợi một góc nhỏ, phản xạ liên tiếp trên mặt lõi và vỏ", b,
                   "Mô phỏng (bấm Chạy mô phỏng): tia hợp trục 30° đi dọc sợi, phản xạ liên tiếp ở thành.<br>Hình vẽ cho trường hợp vỏ đủ nhỏ chiết suất; trục sợi là nét đứt.")
    x0, y0 = pts[1]
    b += seg(x0, 62, x0, 118, "currentColor", 1.3, "5 4", .6)
    b += arc(x0, y0, 26, 210, 270, ORG, 1.8)
    b += tx(x0 - 8, 142, it_("i") + " = ?", ORG, 14, "end")
    b += arc(70, 130, 40, 0, 30, BLUE, 1.8)
    b += tx(64, 124, it_("α") + " = 30°", BLUE, 13, "end")
    return fig("d4-2", "0 0 420 250", "Sợi quang với lõi chiết suất 1,50: tia sáng hợp với trục một góc 30 độ; góc tới tại thành sợi chưa biết", b,
               "Dữ kiện: góc xanh là góc giữa tia và trục sợi.<br>Góc tới tại thành sợi nằm giữa tia và pháp tuyến (nét đứt).")

BUILD = [d1, d2, d3, d4]

# ───────────── Đề ─────────────
DE = [
 dict(label="Dạng 1 · Tính góc tới hạn khi ra không khí và ra nước", topic=T83,
      problem_html=r"<p>Một khối nhựa trong suốt có chiết suất $1{,}49$.</p>"
                   r'<ol type="a"><li>Ánh sáng đi từ khối nhựa ra không khí. Tính góc tới hạn.</li>'
                   r"<li>Nhúng khối nhựa vào nước (chiết suất $1{,}33$). Tính góc tới hạn khi ánh sáng đi từ nhựa ra nước.</li></ol>"),
 dict(label="Dạng 2 · Xét phản xạ toàn phần khi đề cho góc với mặt thoáng", topic=T82,
      problem_html=r"<p>Một chất lỏng trong suốt có chiết suất $1{,}40$, mặt thoáng tiếp xúc với không khí. Hai tia sáng từ trong chất lỏng tới mặt thoáng.</p>"
                   r'<ol type="a"><li>Tia thứ nhất hợp với mặt thoáng góc $40^\circ$. Tia này có bị phản xạ toàn phần không?</li>'
                   r"<li>Tia thứ hai hợp với mặt thoáng góc $60^\circ$. Tia này có ló ra không khí không? Nếu có, tính góc khúc xạ.</li></ol>"),
 dict(label="Dạng 3 · Từ góc tới hạn đo được, tìm chiết suất rồi đổi môi trường", topic=T83,
      problem_html=r"<p>Một khối bán trụ trong suốt đặt trong không khí. Tia laser đi theo bán kính, tới tâm $I$ của mặt phẳng. Tăng dần góc tới: khi góc tới đạt $40^\circ$ thì tia ló đi sát mặt phẳng.</p>"
                   r'<ol type="a"><li>Tính chiết suất của khối.</li>'
                   r"<li>Nhúng khối vào nước (chiết suất $1{,}33$) sao cho mặt phẳng tiếp xúc với nước. Tính góc tới hạn mới.</li>"
                   r"<li>Tia laser tới $I$ với góc tới $50^\circ$. Tia có ló ra nước không?</li></ol>"),
 dict(label="Dạng 4 · Sợi quang: điều kiện của lớp vỏ để tia được dẫn", topic=T83,
      problem_html=r"<p>Một sợi quang có lõi chiết suất $1{,}50$. Tia sáng truyền trong lõi, hợp với trục sợi góc $30^\circ$.</p>"
                   r'<ol type="a"><li>Chiết suất lớn nhất của lớp vỏ là bao nhiêu để tia này vẫn bị phản xạ toàn phần tại mặt lõi – vỏ?</li>'
                   r"<li>Thực tế dùng vỏ chiết suất $1{,}40$. Tia hợp trục $30^\circ$ có còn được dẫn trong lõi không? Giải thích.</li></ol>"),
]

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [(r"&quot;khối nhựa … chiết suất $1{,}49$&quot;", r"$n_1=1{,}49$", r"Nhựa chiết quang hơn hay kém hơn không khí? hơn nước?"),
  (r"&quot;Ánh sáng đi từ khối nhựa ra không khí&quot;", r"$n_2=1$", r"⚠ Điều kiện: có góc tới hạn khi ánh sáng đi từ môi trường chiết quang hơn sang kém hơn ($n_1\gt n_2$)"),
  (r"&quot;Tính góc tới hạn&quot;", r"Cần $i_{th}$", r"Tia khúc xạ đi sát mặt phân cách ($r=90^\circ$); $\sin i_{th}=\dfrac{n_2}{n_1}$"),
  (r"&quot;Nhúng khối nhựa vào nước (chiết suất $1{,}33$)&quot;", r"$n_2=1{,}33$", r"⚠ Môi trường thứ hai không còn là không khí: thế đúng $n_2$ vào công thức"),
  (r"&quot;từ nhựa ra nước&quot;", r"Cần $i_{th}$ mới", r"Cùng công thức, đổi $n_2$")],
 [(r"&quot;chất lỏng … chiết suất $1{,}40$, mặt thoáng tiếp xúc với không khí&quot;", r"$n_1=1{,}40$; $n_2=1$", r"⚠ Điều kiện 1: ánh sáng đi từ chất lỏng ra không khí, $n_1\gt n_2$"),
  (r"&quot;hợp với mặt thoáng góc $40^\circ$&quot;", r"Góc giữa tia và mặt thoáng $=40^\circ$", r"⚠ Góc tới đo từ pháp tuyến (vuông góc với mặt), không đo từ mặt thoáng"),
  (r"&quot;bị phản xạ toàn phần không?&quot;", r"Cần so $i$ với $i_{th}$", r"Điều kiện 2: $i\ge i_{th}$; $\sin i_{th}=\dfrac{n_2}{n_1}$"),
  (r"&quot;hợp với mặt thoáng góc $60^\circ$&quot;", r"Góc giữa tia và mặt thoáng $=60^\circ$", r"Làm như tia thứ nhất: góc tới, rồi so với $i_{th}$"),
  (r"&quot;Nếu có, tính góc khúc xạ&quot;", r"Cần $r$ (chỉ khi có tia ló)", r"Định luật khúc xạ: $n_1\sin i=n_2\sin r$")],
 [(r"&quot;đặt trong không khí&quot;", r"$n_2=1$", r"Không khí là môi trường thứ hai"),
  (r"&quot;tia ló đi sát mặt phẳng khi góc tới $40^\circ$&quot;", r"$i_{th}=40^\circ$", r"Tia khúc xạ sát mặt phân cách ($r=90^\circ$) là dấu hiệu của góc tới hạn"),
  (r"&quot;Tính chiết suất của khối&quot;", r"Cần $n_1$", r"$\sin i_{th}=\dfrac{n_2}{n_1}$"),
  (r"&quot;Nhúng khối vào nước (chiết suất $1{,}33$)&quot;", r"$n_2=1{,}33$; $n_1$ giữ nguyên", r"⚠ Góc tới hạn phụ thuộc cả hai môi trường: sau khi nhúng, $n_2$ không còn bằng $1$"),
  (r"&quot;Tính góc tới hạn mới&quot;", r"Cần $i'_{th}$", r"Cùng công thức, thay $n_2$ mới"),
  (r"&quot;góc tới $50^\circ$ … có ló ra nước không?&quot;", r"$i=50^\circ$", r"⚠ Điều kiện 2: so $i$ với góc tới hạn của cặp môi trường lúc này")],
 [(r"&quot;lõi chiết suất $1{,}50$&quot;", r"$n_1=1{,}50$; vỏ $n_2$", r"⚠ Điều kiện 1: lõi chiết quang hơn vỏ ($n_1\gt n_2$) thì mới có phản xạ toàn phần ở mặt lõi – vỏ"),
  (r"&quot;hợp với trục sợi góc $30^\circ$&quot;", r"Góc với trục $=30^\circ$", r"⚠ Góc tới đo từ pháp tuyến (vuông góc với thành sợi), không đo từ trục"),
  (r"&quot;Chiết suất lớn nhất của lớp vỏ … vẫn bị phản xạ toàn phần&quot;", r"Cần $n_{2,\max}$", r"Điều kiện 2: $i\ge i_{th}$; $\sin i_{th}=\dfrac{n_2}{n_1}$"),
  (r"&quot;vỏ chiết suất $1{,}40$ … còn được dẫn không?&quot;", r"$n_2=1{,}40$", r"So góc tới với góc tới hạn của cặp lõi – vỏ này")],
]

# ───────────── Lời giải ─────────────
RT = [r"<strong>Khái niệm:</strong> phản xạ toàn phần là toàn bộ ánh sáng bị phản xạ, không còn tia khúc xạ.",
      r"Góc tới hạn $i_{th}$: góc tới mà tia khúc xạ đi sát mặt phân cách ($r=90^\circ$).",
      r"Công thức: $\sin i_{th}=\dfrac{n_2}{n_1}$ (nhỏ trên lớn).",
      r"Góc tới đo từ pháp tuyến: tia hợp mặt phân cách (hoặc trục) góc $\beta$ thì $i=90^\circ-\beta$.",
      r"⚠ <strong>Điều kiện:</strong> $n_1\gt n_2$ (ra môi trường chiết quang kém hơn) và $i\ge i_{th}$."]

SOLS = [
 sol([RT[0], RT[1], RT[2], RT[4]], [
  ("Sin của góc tới hạn khi ra không khí", [P(r"Nhựa $n_1=1{,}49$ lớn hơn không khí $n_2=1$: có góc tới hạn."), M(r"\sin i_{th}=\dfrac{n_2}{n_1}=\dfrac{1}{1{,}49}"), A(r"\sin i_{th}\approx0{,}671")]),
  ("Góc tới hạn khi ra không khí", [P(r"Bấm máy ở chế độ độ:"), M(r"i_{th}=\sin^{-1}\dfrac{1}{1{,}49}"), A(r"i_{th}\approx42{,}2^\circ")]),
  ("Góc tới hạn khi ra nước", [P(r"Môi trường thứ hai là nước: $n_2=1{,}33$ ($n_1\gt n_2$ vẫn đúng)."), M(r"\sin i_{th}=\dfrac{n_2}{n_1}=\dfrac{1{,}33}{1{,}49}\approx0{,}893"), M(r"i_{th}=\sin^{-1}\dfrac{1{,}33}{1{,}49}"), A(r"i_{th}\approx63{,}2^\circ")]),
  ("Kiểm tra", [P(r"Hai chiết suất càng gần nhau, góc tới hạn càng lớn:"), M(r"63{,}2^\circ\gt42{,}2^\circ\ ✓"), P(r"Cả hai giá trị $\sin i_{th}$ đều nhỏ hơn $1$ ✓")])],
  [r"a) $i_{th}\approx42{,}2^\circ$ (ra không khí)", r"b) $i_{th}\approx63{,}2^\circ$ (ra nước)"],
  r"Nhận dạng: đề hỏi <strong>góc tới hạn</strong> và cho <strong>hai chiết suất</strong> → $\sin i_{th}=\dfrac{n_2}{n_1}$ (nhỏ trên lớn); đổi môi trường thứ hai thì thế lại $n_2$."),
 sol(RT + [r"Định luật khúc xạ: $n_1\sin i=n_2\sin r$."], [
  ("Góc tới của tia thứ nhất", [P(r"Tia hợp mặt thoáng $40^\circ$. Góc tới đo từ pháp tuyến:"), M(r"i=90^\circ-40^\circ"), A(r"i=50^\circ")]),
  ("Góc tới hạn", [P(r"Chất lỏng $n_1=1{,}40$ ra không khí $n_2=1$:"), M(r"\sin i_{th}=\dfrac{n_2}{n_1}=\dfrac{1}{1{,}40}"), A(r"i_{th}\approx45{,}6^\circ")]),
  ("Tia thứ nhất có phản xạ toàn phần không?", [P(r"Điều kiện 1: ánh sáng đi từ chất lỏng ra không khí, $n_1\gt n_2$ ✓."), P(r"Điều kiện 2:"), M(r"i=50^\circ\gt i_{th}\approx45{,}6^\circ"), A(r"T:Có phản xạ toàn phần, không có tia ló.")]),
  ("Tia thứ hai", [P(r"Hợp mặt thoáng $60^\circ$ nên góc tới:"), M(r"i=90^\circ-60^\circ=30^\circ"), P(r"$30^\circ\lt45{,}6^\circ$: tia ló ra không khí. Định luật khúc xạ:"), M(r"n_1\sin i=n_2\sin r"), M(r"\sin r=1{,}40\cdot\sin30^\circ=0{,}70"), A(r"r\approx44{,}4^\circ")]),
  ("Kiểm tra", [P(r"Ra môi trường chiết quang kém hơn, tia ló lệch xa pháp tuyến:"), M(r"r=44{,}4^\circ\gt i=30^\circ\ ✓"), P(r"$\sin r=0{,}70\le1$ nên có nghiệm ✓")])],
  [r"a) Có phản xạ toàn phần ($50^\circ\gt45{,}6^\circ$)", r"b) Tia ló ra không khí, $r\approx44{,}4^\circ$"],
  r"Nhận dạng: đề cho góc <strong>hợp với mặt</strong> → đổi sang góc với pháp tuyến, rồi so với $i_{th}$; chỉ khi $i\lt i_{th}$ mới dùng định luật khúc xạ để tính $r$."),
 sol(RT[:3] + [r"Cùng một khối: đổi môi trường thứ hai thì góc tới hạn đổi.", RT[4]], [
  ("Chiết suất của khối", [P(r"Khối trong không khí ($n_2=1$), $i_{th}=40^\circ$:"), M(r"\sin i_{th}=\dfrac{1}{n}"), M(r"\sin40^\circ\approx0{,}6428"), M(r"n=\dfrac{1}{\sin40^\circ}=\dfrac{1}{0{,}6428}"), A(r"n\approx1{,}556")]),
  ("Sin góc tới hạn khi nhúng nước", [P(r"Môi trường thứ hai bây giờ là nước: $n_2=1{,}33$."), M(r"\sin i'_{th}=\dfrac{n_2}{n}=\dfrac{1{,}33}{1{,}556}"), A(r"\sin i'_{th}\approx0{,}855")]),
  ("Góc tới hạn mới", [M(r"i'_{th}=\sin^{-1}\dfrac{1{,}33}{1{,}556}"), A(r"i'_{th}\approx58{,}7^\circ")]),
  (r"Tia tới với góc $50^\circ$", [P(r"Khối ($n=1{,}556$) sang nước ($1{,}33$): $n_1\gt n_2$ ✓."), P(r"Điều kiện 2:"), M(r"i=50^\circ\lt i'_{th}\approx58{,}7^\circ"), A(r"T:Tia ló ra nước, không phản xạ toàn phần.")]),
  ("Kiểm tra", [P(r"Nước chiết quang hơn không khí nên góc tới hạn lớn lên:"), M(r"58{,}7^\circ\gt40^\circ\ ✓"), P(r"Tia $50^\circ$ trong không khí sẽ phản xạ toàn phần ($50^\circ\gt40^\circ$); trong nước thì ló: hợp lí.")])],
  [r"a) $n\approx1{,}556$", r"b) $i'_{th}\approx58{,}7^\circ$", r"c) Tia ló ra nước"],
  r"Nhận dạng: đề cho <strong>góc tới hạn đo được</strong> rồi <strong>đổi môi trường</strong> → tìm $n$ trước ($n=\dfrac{1}{\sin i_{th}}$), sau đó thay $n_2$ mới; so góc tới với góc tới hạn <em>mới</em>."),
 sol(RT[:3] + [RT[3], r"Phản xạ toàn phần khi $i\ge i_{th}$, tức $\sin i\ge\dfrac{n_2}{n_1}$.", RT[4]], [
  ("Góc tới tại mặt lõi – vỏ", [P(r"Thành sợi song song với trục, nên góc tới đo từ pháp tuyến:"), M(r"i=90^\circ-30^\circ"), A(r"i=60^\circ")]),
  ("Chiết suất lớn nhất của vỏ", [P(r"Để phản xạ toàn phần: $\sin i\ge\dfrac{n_2}{n_1}$, suy ra:"), M(r"n_2\le n_1\sin i=1{,}50\cdot\sin60^\circ"), A(r"n_{2,\max}\approx1{,}30")]),
  (r"Góc tới hạn với vỏ $1{,}40$", [P(r"Mặt tiếp xúc là lõi – vỏ: $n_1=1{,}50$, $n_2=1{,}40$."), M(r"\sin i_{th}=\dfrac{1{,}40}{1{,}50}\approx0{,}933"), A(r"i_{th}\approx69{,}0^\circ")]),
  (r"Kết luận cho tia hợp trục $30^\circ$", [M(r"i=60^\circ\lt i_{th}\approx69{,}0^\circ"), A(r"T:Không phản xạ toàn phần: một phần ánh sáng lọt ra vỏ, tia không được dẫn tốt.")]),
  ("Kiểm tra", [P(r"Vỏ $1{,}40\gt n_{2,\max}\approx1{,}30$ nên không thoả: khớp kết luận."), P(r"Với vỏ $1{,}40$, tia chỉ được dẫn khi $i\ge69{,}0^\circ$, tức hợp trục tối đa:"), M(r"\alpha_{\max}=90^\circ-69{,}0^\circ\approx21{,}0^\circ\lt30^\circ\ ✓")])],
  [r"a) $n_{2,\max}\approx1{,}30$", r"b) Không: $60^\circ\lt69{,}0^\circ$, ánh sáng lọt ra vỏ"],
  r"Nhận dạng: <strong>sợi quang</strong> và <strong>góc hợp với trục</strong> → đổi sang góc tới ($90^\circ-\alpha$), rồi so với $i_{th}$ của cặp lõi – vỏ."),
]

# ───────────── Tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>góc tới hạn</b> và <b>hai chiết suất</b> → nghĩ tới <b>$\sin i_{th}=\dfrac{n_2}{n_1}$</b> (nhỏ trên lớn).",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Sin của góc tới hạn khi ra không khí", r"$\sin i_{th}$ khi ánh sáng đi từ nhựa ra không khí bằng bao nhiêu?", 0.671, "", 0.005,
       loi=r"Hay viết tỉ số lớn trên nhỏ: $\dfrac{n_1}{n_2}=1{,}49$, lớn hơn $1$ nên không có góc nào. Quy tắc “nhỏ trên lớn”: $\sin i_{th}=\dfrac{n_2}{n_1}$."),
  buoc("Góc tới hạn khi ra không khí", r"Góc tới hạn $i_{th}$ bằng bao nhiêu độ?", 42.2, "°", 0.3,
       loi=r"Bấm máy sai chế độ (radian) hoặc lấy $\sin$ thay vì $\sin^{-1}$ nên ra số lạ.",
       ke=[(r"$i_{th}=\sin^{-1}$ của giá trị vừa tính, máy ở chế độ độ", True),
           (r"$i_{th}=90^\circ\cdot\sin i_{th}$", r"Góc không tỉ lệ thuận với sin của nó; phải dùng hàm ngược $\sin^{-1}$."),
           (r"$i_{th}=90^\circ-\sin^{-1}(\ldots)$", r"Đó là góc với mặt phân cách, không phải góc tới (góc tới đo từ pháp tuyến).")]),
  buoc("Góc tới hạn khi ra nước", r"Khi ánh sáng đi từ nhựa ra nước, góc tới hạn bằng bao nhiêu độ?", 63.2, "°", 0.4,
       loi=r"Dùng lại $\sin i_{th}=\dfrac{1}{n_1}$ của câu a: công thức đó chỉ đúng khi môi trường thứ hai là không khí ($n_2=1$).",
       ke=[(r"$\sin i_{th}=\dfrac{n_{nước}}{n_{nhựa}}$", True),
           (r"$\sin i_{th}=\dfrac{1}{n_{nhựa}}$ như câu a", r"Môi trường thứ hai bây giờ là nước ($n_2=1{,}33$), không phải không khí; chỉ khi $n_2=1$ mới rút về $\dfrac{1}{n_1}$."),
           (r"$\sin i_{th}=\dfrac{n_{nhựa}}{n_{nước}}$", r"Tỉ số lớn trên nhỏ lớn hơn $1$, mà $\sin$ không vượt quá $1$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>tia hợp với mặt</b> (không phải pháp tuyến) → đổi <b>$i=90^\circ-\beta$</b>, rồi so $i$ với $i_{th}$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Góc tới của tia thứ nhất", r"Tia hợp mặt thoáng $40^\circ$. Góc tới $i$ bằng bao nhiêu độ?", 50, "°", 0.5,
       loi=r"Lấy luôn $40^\circ$ (góc với mặt thoáng) làm góc tới. Góc tới đo từ pháp tuyến, vuông góc với mặt."),
  buoc("Góc tới hạn", r"Góc tới hạn $i_{th}$ của chất lỏng với không khí bằng bao nhiêu độ?", 45.6, "°", 0.3,
       loi=r"Viết $\sin i_{th}=n_1=1{,}40$ (lớn hơn $1$, vô lí) hoặc quên rằng $n_2=1$ nên $\sin i_{th}=\dfrac{1}{n_1}$.",
       ke=[(r"$\sin i_{th}=\dfrac{1}{1{,}40}$", True),
           (r"$\sin i_{th}=1{,}40$", r"$\sin$ không vượt quá $1$; tỉ số đúng là nhỏ trên lớn."),
           (r"$i_{th}=90^\circ-i$", r"Góc tới hạn do chiết suất hai môi trường quyết định, không phụ thuộc tia đang xét.")]),
  buoc("Tia thứ nhất có phản xạ toàn phần không?", r"Tia thứ nhất có bị phản xạ toàn phần không?",
       loi=r"Chỉ kiểm điều kiện chiều truyền (ra không khí) rồi kết luận, quên so góc tới với góc tới hạn.",
       lua_chon=[(r"Có: ánh sáng đi từ chất lỏng ra không khí và $i\gt i_{th}$", True),
                 (r"Không: ánh sáng đi ra không khí nên luôn ló ra", r"Đi ra môi trường chiết quang kém mới là điều kiện 1; còn cần điều kiện 2: $i\ge i_{th}$."),
                 (r"Không: $40^\circ\lt i_{th}$", r"$40^\circ$ là góc với mặt thoáng, chưa phải góc tới; góc tới mới là số cần so với $i_{th}$.")],
       ke=[(r"Xét chiều truyền, rồi so góc tới với $i_{th}$", True),
           (r"Tính ngay góc khúc xạ rồi bỏ qua việc so với $i_{th}$ và chiều truyền", r"Cách này chỉ đúng nếu nhận ra $\sin r\gt1$ (không có tia ló); nhiều bạn tính ra số lạ rồi bỏ dở. So với $i_{th}$ trước cho kết luận rõ hơn."),
           (r"So góc tới với $45^\circ$ cho tròn số", r"Mốc $45^\circ$ không có cơ sở; mốc đúng là $i_{th}$, tính từ $\dfrac{n_2}{n_1}$ của hai môi trường.")]),
  buoc("Tia thứ hai", r"Nếu có tia ló, góc khúc xạ của tia thứ hai bằng bao nhiêu độ?", 44.4, "°", 0.4,
       loi=r"Thế thẳng $60^\circ$ (góc với mặt) vào định luật khúc xạ: khi đó $1{,}40\cdot\sin60^\circ\gt1$, không có nghiệm.",
       ke=[(r"Đổi sang góc tới rồi so với $i_{th}$; nếu nhỏ hơn thì dùng $n_1\sin i=n_2\sin r$", True),
           (r"Góc tới $60^\circ\gt i_{th}$ nên không có tia ló", r"$60^\circ$ là góc với mặt thoáng; góc tới là $90^\circ-60^\circ$."),
           (r"$\sin r=\dfrac{\sin i}{1{,}40}$", r"Đảo tỉ số: ra không khí tia lệch xa pháp tuyến nên $r\gt i$, theo $n_1\sin i=n_2\sin r$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>góc tới hạn đo được</b> rồi <b>đổi môi trường</b> → tìm $n$ trước, thay $n_2$ mới; so với góc tới hạn mới.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Chiết suất của khối", r"Chiết suất $n$ của khối bằng bao nhiêu?", 1.556, "", 0.01,
       loi=r"Viết $n=\sin40^\circ$ (quên rằng $\sin i_{th}=\dfrac{1}{n}$), ra $n\lt1$: vô lí vì chiết suất luôn lớn hơn hoặc bằng $1$."),
  buoc("Sin góc tới hạn khi nhúng nước", r"Khi khối ở trong nước, $\sin i'_{th}$ bằng bao nhiêu?", 0.855, "", 0.005,
       loi=r"Dùng lại $\sin i_{th}=\dfrac{1}{n}$ (môi trường thứ hai vẫn coi là không khí) nên ra lại đúng góc ban đầu.",
       ke=[(r"$\sin i'_{th}=\dfrac{1{,}33}{n}$ với $n$ vừa tìm", True),
           (r"$\sin i'_{th}=\dfrac{1}{n}$", r"Môi trường thứ hai bây giờ là nước ($n_2=1{,}33$), không phải không khí."),
           (r"$\sin i'_{th}=\dfrac{n}{1{,}33}$", r"Tỉ số lớn trên nhỏ lớn hơn $1$, mà $\sin$ không vượt quá $1$.")]),
  buoc("Góc tới hạn mới", r"Góc tới hạn mới $i'_{th}$ bằng bao nhiêu độ?", 58.7, "°", 0.5,
       loi=r"Giữ nguyên góc tới hạn cũ vì “khối không đổi”. Góc tới hạn phụ thuộc cả hai môi trường.",
       ke=[(r"$i'_{th}=\sin^{-1}$ của giá trị vừa tính", True),
           (r"$i'_{th}=40^\circ$ vì khối không đổi", r"Góc tới hạn phụ thuộc cả hai môi trường; đổi môi trường thứ hai thì đổi."),
           (r"$i'_{th}=\sin^{-1}(1{,}33)$", r"$\sin$ không vượt quá $1$; phải chia $1{,}33$ cho chiết suất của khối.")]),
  buoc(r"Tia tới với góc $50^\circ$", r"Tia tới với góc $50^\circ$ có ló ra nước không?",
       loi=r"Còn nhớ “$50^\circ\gt40^\circ$ nên phản xạ toàn phần” mà quên rằng $40^\circ$ chỉ đúng khi khối ở trong không khí.",
       lua_chon=[(r"Ló ra nước vì $50^\circ\lt i'_{th}$", True),
                 (r"Phản xạ toàn phần vì $50^\circ\gt40^\circ$", r"$40^\circ$ là góc tới hạn khi ở trong không khí; trong nước góc tới hạn đã đổi."),
                 (r"Phản xạ toàn phần vì khối chiết quang hơn nước", r"Chiết quang hơn mới là điều kiện 1; còn phải có $i\ge i_{th}$.")],
       ke=[(r"So $50^\circ$ với góc tới hạn mới", True),
           (r"So $50^\circ$ với $40^\circ$", r"$40^\circ$ là góc tới hạn của khối trong không khí, không còn dùng được sau khi nhúng nước."),
           (r"Khối chiết quang hơn nước nên luôn phản xạ toàn phần", r"Đó mới là điều kiện 1; còn phải so góc tới với góc tới hạn.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>sợi quang</b> và <b>góc hợp với trục</b> → đổi thành góc tới ($90^\circ-\alpha$), so với $i_{th}$ của lõi – vỏ.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Góc tới tại mặt lõi – vỏ", r"Góc tới $i$ tại thành sợi bằng bao nhiêu độ?", 60, "°", 0.5,
       loi=r"Lấy luôn $30^\circ$ (góc với trục) làm góc tới. Góc tới đo từ pháp tuyến, vuông góc với thành sợi."),
  buoc("Chiết suất lớn nhất của vỏ", r"Chiết suất lớn nhất của vỏ để tia còn phản xạ toàn phần bằng bao nhiêu?", 1.30, "", 0.01,
       loi=r"Dùng góc hợp trục: $n_2=n_1\sin30^\circ$, ra giá trị quá nhỏ. Hoặc đổi chiều bất đẳng thức: vỏ càng chiết quang thì càng khó phản xạ toàn phần.",
       ke=[(r"$i\ge i_{th}$ nên $n_2\le n_1\sin i$", True),
           (r"$n_2\ge n_1\sin i$", r"Ngược chiều: vỏ có $n_2$ lớn thì $i_{th}$ lớn, điều kiện $i\ge i_{th}$ càng khó đạt."),
           (r"$n_2=n_1\sin\alpha$ với $\alpha$ là góc hợp trục", r"$\alpha$ đo từ trục, không phải từ pháp tuyến; góc tới là $90^\circ-\alpha$.")]),
  buoc("Góc tới hạn với vỏ $1{,}40$", r"Với vỏ $1{,}40$, góc tới hạn của mặt lõi – vỏ bằng bao nhiêu độ?", 69.0, "°", 0.4,
       loi=r"Dùng $\sin i_{th}=\dfrac{1}{n_1}$ như khi ra không khí: mặt tiếp xúc là lõi – vỏ chứ không phải lõi – không khí.",
       ke=[(r"$\sin i_{th}=\dfrac{n_{vỏ}}{n_{lõi}}$", True),
           (r"$\sin i_{th}=\dfrac{1}{n_{lõi}}$", r"Môi trường thứ hai là vỏ ($n_2=1{,}40$), không phải không khí."),
           (r"$\sin i_{th}=\dfrac{n_{lõi}}{n_{vỏ}}$", r"Tỉ số lớn trên nhỏ lớn hơn $1$, mà $\sin$ không vượt quá $1$.")]),
  buoc(r"Kết luận cho tia hợp trục $30^\circ$", r"Với vỏ $1{,}40$, tia hợp trục $30^\circ$ có còn được dẫn không?",
       loi=r"Chỉ thấy lõi chiết quang hơn vỏ ($1{,}50\gt1{,}40$) rồi kết luận có phản xạ toàn phần, quên điều kiện về góc tới.",
       lua_chon=[(r"Không: $i\lt i_{th}$, một phần ánh sáng lọt ra vỏ", True),
                 (r"Vẫn dẫn: lõi chiết quang hơn vỏ nên luôn phản xạ toàn phần", r"Mới thoả điều kiện 1; điều kiện 2 ($i\ge i_{th}$) không còn."),
                 (r"Vẫn dẫn vì $30^\circ$ nhỏ hơn góc tới hạn", r"$30^\circ$ là góc với trục, không phải góc tới; phải đổi sang góc tới trước khi so.")],
       ke=[(r"So góc tới $i$ với $i_{th}$ của cặp lõi – vỏ", True),
           (r"So góc hợp trục $\alpha$ với $i_{th}$", r"$\alpha$ đo từ trục còn $i_{th}$ đo từ pháp tuyến; hai góc khác gốc nên không so trực tiếp được."),
           (r"Chỉ cần lõi chiết quang hơn vỏ là đủ", r"Đó mới là điều kiện 1; còn phải có $i\ge i_{th}$.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Ghi JSON ─────────────
d = {"lesson_id": 84, "lesson_title": "Bài 6. Phản xạ toàn phần", "generated_at": "2026-10-12",
     "review": {"checked": True, "notes": "Soạn 12/10/2026 (chặng 3). Kiểm chéo kiem-code 12/10: đáp số 4 dạng đúng, đã sửa 6 mục. Chưa đối chiếu số câu ngân hàng cho chủ đề 82/83 (không có DB trong phiên này)."},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DE]}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
assert all(len(s["buoc"]) == SOLS[i].count('class="bt-step"') for i, s in enumerate(STEPS))
inject(J, BUILD, ANALYSIS, SOLS, STEPS)

# Quét ký tự điều khiển (\t, \b… do chuỗi thường chứa `\text`, `\beta`) và `<`/`>` trần trong $…$
raw = open(J, encoding="utf8").read()
import re as _re
assert not _re.search(r"\\u000[0-8bcef]|\\t", raw.replace("\\\\t", "")), "ký tự điều khiển trong JSON"
for q in json.load(open(J))["dang_bai"]:
    for f in ("problem_html", "analysis_html", "solution_html"):
        h_ = _re.sub(r"<svg.*?</svg>", "", q[f], flags=_re.S)
        ms = _re.findall(r"\$\$(.+?)\$\$", h_, flags=_re.S)
        ms += _re.findall(r"\$([^$]+)\$", _re.sub(r"\$\$.+?\$\$", "", h_, flags=_re.S))
        for m in ms:
            assert "<" not in m and ">" not in m, (f, m)
print("xong 84.json")
