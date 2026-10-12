"""Bài tập mẫu bài 91 — Bài 13. Năng lượng của dòng điện và công suất điện (KHTN 9). Dựng 4 dạng + hình + lời giải + buoc[] → 91.json.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-91.py   (idempotent: ghi lại toàn bộ 91.json, review.checked=false)
Danh sách dạng: scripts/data/bai-tap-mau/91.dang.md. Mọi số liệu tính ở đầu file, có assert."""
import json, math, os, sys, re as _re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "91.json")
T93 = "Tính điện năng tiêu thụ và tiền điện"
T94 = "Công suất điện của dụng cụ và số ghi trên thiết bị"

# ───────────── Số liệu (tính + kiểm) ─────────────
# Dạng 1: bàn là 220 V – 1 210 W
U1, P1 = 220.0, 1210.0
I1 = P1 / U1
R1 = U1 / I1
assert abs(I1 - 5.5) < 1e-9 and abs(R1 - 40) < 1e-9 and abs(U1 ** 2 / P1 - 40) < 1e-9 and abs(I1 ** 2 * R1 - P1) < 1e-6
assert abs(U1 / P1 - I1) > 1 and abs(P1 * U1 - I1) > 1                 # chia ngược (0,18) · nhân
assert abs(P1 / I1 - R1) > 1 and abs(U1 ** 2 / I1 - R1) > 1             # P/I (220) · U²/I (8 800)

# Dạng 2: điều hoà 1 200 W × 8 h; 5 đèn LED 20 W × 6 h; 30 ngày; 2 500 đồng/kWh
P_dh, h_dh, n_den, P_den, h_den, NGAY, GIA2 = 1200.0, 8, 5, 20.0, 6, 30, 2500
A_dh = P_dh / 1000 * h_dh * NGAY
A_den = n_den * P_den / 1000 * h_den * NGAY
TIEN2 = (A_dh + A_den) * GIA2
assert abs(A_dh - 288) < 1e-9 and abs(A_den - 18) < 1e-9 and abs(TIEN2 - 765000) < 1e-6
assert abs(P_den / 1000 * h_den * NGAY - A_den) > 5                    # quên 5 bóng (3,6)
assert abs(A_dh * GIA2 - TIEN2) > 1000                                  # quên đèn (720 000)

# Dạng 3: Đ1 12 V – 6 W, Đ2 12 V – 18 W, nguồn 12 V, R không đổi
U3, Pa, Pb = 12.0, 6.0, 18.0
Ra, Rb = U3 ** 2 / Pa, U3 ** 2 / Pb
I3 = U3 / (Ra + Rb)
P3a, P3b = I3 ** 2 * Ra, I3 ** 2 * Rb
assert abs(Ra - 24) < 1e-9 and abs(Rb - 8) < 1e-9 and abs(I3 - 0.375) < 1e-12
assert abs(P3a - 3.375) < 1e-9 and abs(P3b - 1.125) < 1e-9 and P3a > P3b
assert abs((Pa + Pb) / U3 - I3) > 1 and abs(U3 / Ra + U3 / Rb - I3) > 1   # hai cách sai đều ra 2 A
assert abs(U3 ** 2 / Ra - P3a) > 1                                       # dùng đủ 12 V cho Đ1 (6 W)
assert abs(I3 * Ra + I3 * Rb - U3) < 1e-9                                # kiểm tra U1 + U2 = U

# Dạng 4: ấm 1 500 W, Q = 504 000 J, H = 84 %, 2 lần/ngày, 30 ngày, 2 000 đồng/kWh
P4, Q4, H4, LAN, GIA4 = 1500.0, 504000.0, 0.84, 2, 2000
A4 = Q4 / H4
t4 = A4 / P4
A4_thang = A4 * LAN * NGAY / 3.6e6
TIEN4 = A4_thang * GIA4
assert abs(A4 - 600000) < 1e-6 and abs(t4 - 400) < 1e-9 and abs(A4_thang - 10) < 1e-9 and abs(TIEN4 - 20000) < 1e-6
assert abs(Q4 * H4 - A4) > 1e4 and abs(Q4 / P4 - t4) > 10               # nhân H (423 360) · bỏ H (336 s)
assert abs(A4 * LAN * NGAY / 1000 - A4_thang) > 1                        # chia 1 000 thay vì 3,6·10⁶

# ───────────── Hình ─────────────
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'

def subt(x, y, base, idx, rest="", c="currentColor", size=17, anchor="start"):
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">{base}'
            f'<tspan dy="5" font-size="{size - 4}">{idx}</tspan><tspan dy="-5">{rest}</tspan></text>')

def lamp(cx, cy, r=15):
    k = r * 0.7071
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(251,146,60,.12)" stroke="currentColor" stroke-width="2.4"/>'
            + seg(cx - k, cy - k, cx + k, cy + k, "currentColor", 2) + seg(cx - k, cy + k, cx + k, cy - k, "currentColor", 2))

def flow(corners, ndots=6, dur=6.0):
    """Chấm chạy theo chiều dòng điện quy ước, MỘT vòng khi bấm (chỉ ghi góc + keyTimes theo chiều dài)."""
    segs = list(zip(corners, corners[1:] + corners[:1]))
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
    tot = sum(lens); cum = [sum(lens[:k]) for k in range(len(lens))]
    def at(sv):
        sv %= tot
        for (a, b), c0, L in zip(segs, cum, lens):
            if sv <= c0 + L:
                f = (sv - c0) / L; return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
    out = ""
    for d in range(ndots):
        s0 = tot * d / ndots
        stops = [s0] + sorted({c if c > s0 else c + tot for c in cum} - {s0}) + [s0 + tot]
        pts = [at(x) for x in stops]; kt = [(x - s0) / tot for x in stops]
        ktx = ";".join(f"{k:.3f}" for k in kt)
        out += (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="4" fill="{ORG}">'
                + "".join(f'<animate attributeName="{a}" values="{";".join(f"{p[n]:.1f}" for p in pts)}" keyTimes="{ktx}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>' for a, n in (("cx", 0), ("cy", 1)))
                + '</circle>')
    return out

# Dạng 1: bàn là cắm ổ điện (điện lưới đổi chiều liên tục → chấm dao động qua lại)
def iron(x0=236, y0=150):
    g = (f'<path d="M{x0},{y0} L{x0 + 150},{y0} L{x0 + 138},{y0 - 34} Q{x0 + 70},{y0 - 52} {x0 + 18},{y0 - 26} Z" '
         f'fill="rgba(248,113,113,.15)" stroke="currentColor" stroke-width="2.4"/>')
    g += f'<path d="M{x0 + 50},{y0 - 40} Q{x0 + 60},{y0 - 78} {x0 + 110},{y0 - 74} L{x0 + 124},{y0 - 42}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    return g

def d1(k):
    b = '<rect x="20" y="96" width="44" height="60" rx="8" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    b += seg(64, 118, 254, 118, "currentColor", 2) + seg(64, 134, 254, 134, "currentColor", 2)
    b += iron()
    b += lbl(20, 30, "Bàn là ghi: 220 V – 1 210 W", BLUE, 17, "start", "700")
    b += lbl(20, 186, "ổ điện 220 V", "currentColor", 16, "start", "600")
    if k == 0:
        for j, (y, ph) in enumerate(((118, 0), (134, 1), (118, 2), (134, 3))):
            x0 = 100 + 40 * j
            xs = [x0] + [x0 + (16 if (n + ph) % 2 == 0 else -16) for n in range(8)] + [x0]
            b += f'<circle cx="{x0}" cy="{y}" r="4" fill="{ORG}">{smil("cx", xs, 4.0)}</circle>'
        b += lbl(140, 104, it_("I") + " = ?", RED, 18, "middle", "700")
        b += lbl(310, 186, it_("R") + " = ?", ORG, 18, "middle", "700")
        return fig("d1-0", "0 0 420 200", "Bàn là ghi 220 vôn 1210 oát cắm vào ổ điện 220 vôn; cần tìm cường độ dòng điện và điện trở", b,
                   "Mô phỏng (bấm Chạy mô phỏng): chấm cam là dòng điện trong dây, điện lưới đổi chiều liên tục.<br>Chấm chạy chậm hơn thật rất nhiều, chỉ để minh hoạ.")
    b = lbl(20, 34, "Số ghi trên bàn là:", "currentColor", 17, "start", "700")
    b += subt(20, 70, it_("U"), "đm", " = 220 V", BLUE) + subt(20, 102, it_("P"), "đm", " = 1 210 W", BLUE)
    b += lbl(20, 142, "Dùng đúng 220 V", RED, 17, "start", "700")
    b += lbl(20, 168, "→ bàn là chạy đúng công suất ghi", RED, 17, "start", "700")
    return fig("d1-2", "0 0 420 184", "Số ghi trên bàn là: hiệu điện thế định mức 220 vôn, công suất định mức 1210 oát", b,
               "Dữ kiện: số ghi là định mức.<br>Dùng đúng 220 V nên công suất đúng bằng số ghi.")

# Dạng 2: dòng thời gian một ngày
X0, X24, KH = 40, 400, 15.0
def hx(h): return X0 + KH * h
def timeline(anim, t1="Điều hoà 1 200 W", t2="5 đèn LED, mỗi đèn 20 W"):
    b = seg(X0, 150, X24, 150, "currentColor", 2)
    for h in (0, 6, 12, 18, 24):
        b += seg(hx(h), 150, hx(h), 158, "currentColor", 2) + lbl(hx(h), 178, f"{h} h", "currentColor", 16, "middle", "600")
    b += lbl(X0, 38, t1, BLUE, 16, "start", "700")
    b += f'<rect x="{hx(0)}" y="46" width="{KH * 6}" height="18" rx="3" fill="rgba(56,189,248,.45)"/>'
    b += f'<rect x="{hx(22)}" y="46" width="{KH * 2}" height="18" rx="3" fill="rgba(56,189,248,.45)"/>'
    b += lbl(X0, 96, t2, ORG, 16, "start", "700")
    b += f'<rect x="{hx(18)}" y="104" width="{KH * 6}" height="18" rx="3" fill="rgba(251,146,60,.5)"/>'
    assert hx(24) == X24 and hx(18) + KH * 6 == X24
    if anim:
        b += f'<line x1="{X0}" y1="40" x2="{X0}" y2="150" stroke="{RED}" stroke-width="2.4">{smil("x1", [X0, X24], 6.0)}{smil("x2", [X0, X24], 6.0)}</line>'
    return b

def d2(k):
    b = timeline(True) if k == 0 else timeline(False, "Điều hoà: 8 giờ mỗi ngày", "Mỗi đèn: 6 giờ mỗi ngày")
    if k == 0:
        b += lbl(X0, 214, "Lặp lại 30 ngày.", "currentColor", 16, "start", "700")
        b += lbl(X0, 240, "Tiền điện = ?", RED, 17, "start", "700")
        return fig("d2-0", "0 0 420 254", "Dòng thời gian một ngày: điều hoà bật từ 22 giờ đến 6 giờ sáng, năm đèn LED bật từ 18 giờ đến 24 giờ", b,
                   "Mô phỏng (bấm Chạy mô phỏng): vạch đỏ chạy hết một ngày 24 giờ.<br>Dải xanh: điều hoà đang bật. Dải cam: đèn đang bật.")
    b += lbl(X0, 214, "⚠ Đổi W ra kW, thời gian tính bằng giờ", RED, 16, "start", "700")
    return fig("d2-2", "0 0 420 228", "Mỗi ngày điều hoà bật 8 giờ, mỗi đèn bật 6 giờ", b,
               "Dữ kiện: điều hoà 8 giờ mỗi ngày, mỗi đèn 6 giờ mỗi ngày.")

# Dạng 3: hai đèn nối tiếp (động) / cả hai cách mắc (tĩnh)
def series(x0, x1, y0, y1, anim):
    PX, NX = (x0 + x1) / 2 - 7, (x0 + x1) / 2 + 7
    LA, LB = x0 + 0.3 * (x1 - x0), x1 - 0.3 * (x1 - x0)
    assert LB - LA >= 60
    b = poly([(PX, y1), (x0, y1), (x0, y0), (LA - 15, y0)], "currentColor", 2.4)
    b += poly([(LA + 15, y0), (LB - 15, y0)], "currentColor", 2.4) + poly([(LB + 15, y0), (x1, y0), (x1, y1), (NX, y1)], "currentColor", 2.4)
    b += lamp(LA, y0) + lamp(LB, y0)
    b += subt(LA, y0 - 24, "Đ", "1", "", "currentColor", 18, "middle") + subt(LB, y0 - 24, "Đ", "2", "", "currentColor", 18, "middle")
    b += seg(PX, y1 - 16, PX, y1 + 16, "currentColor", 2.4) + seg(NX, y1 - 8, NX, y1 + 8, "currentColor", 5)
    b += lbl(PX - 6, y1 - 20, "+", "currentColor", 18, "end", "700") + lbl(NX + 6, y1 - 20, "−", "currentColor", 18, "start", "700")
    b += lbl((x0 + x1) / 2, y1 + 32, "12 V", "currentColor", 17, "middle", "700")
    b += chevron(x0 + 30, y1, -1, 0, RED, 2.6, 12) + chevron(x0, (y0 + y1) / 2, 0, -1, RED, 2.6, 12)
    b += chevron((LA + LB) / 2 + 6, y0, 1, 0, RED, 2.6, 12) + chevron(x1, (y0 + y1) / 2, 0, 1, RED, 2.6, 12) + chevron(x1 - 30, y1, -1, 0, RED, 2.6, 12)
    assert x0 + 30 < PX and x1 - 30 > NX
    if anim:
        b += flow([(PX, y1), (x0, y1), (x0, y0), (x1, y0), (x1, y1), (NX, y1)])
    return b

def d3(k):
    if k == 0:
        b = series(60, 360, 70, 190, True)
        b += subt(20, 262, "Đ", "1", ": 12 V – 6 W", BLUE) + subt(220, 262, "Đ", "2", ": 12 V – 18 W", BLUE)
        return fig("d3-0", "0 0 420 276", "Hai bóng đèn Đ1 12 vôn 6 oát và Đ2 12 vôn 18 oát mắc nối tiếp vào nguồn 12 vôn", b,
                   "Mô phỏng (bấm Chạy mô phỏng): chấm cam chạy theo chiều dòng điện quy ước, qua Đ1 rồi Đ2.<br>Hình không vẽ độ sáng: em tự tính.")
    b = series(30, 200, 70, 180, False)
    b += lbl(20, 266, "(a) nối tiếp: cùng", "currentColor", 16, "start", "700") + lbl(160, 266, it_("I") + " = ?", RED, 16, "start", "700")
    b += seg(212, 14, 212, 276, "currentColor", 1.2, "5 5", .5)
    JL, JR, XC = 240, 400, 320
    b += poly([(JL, 150), (JL, 70), (XC - 15, 70)], "currentColor", 2.4) + poly([(XC + 15, 70), (JR, 70), (JR, 150)], "currentColor", 2.4)
    b += poly([(JL, 150), (XC - 15, 150)], "currentColor", 2.4) + poly([(XC + 15, 150), (JR, 150)], "currentColor", 2.4)
    b += poly([(JL, 150), (JL, 200), (313, 200)], "currentColor", 2.4) + poly([(327, 200), (JR, 200), (JR, 150)], "currentColor", 2.4)
    b += seg(313, 184, 313, 216, "currentColor", 2.4) + seg(327, 192, 327, 208, "currentColor", 5)
    b += dot(JL, 150, 3.5) + dot(JR, 150, 3.5) + lamp(XC, 70) + lamp(XC, 150)
    b += subt(XC, 46, "Đ", "1", "", "currentColor", 18, "middle") + subt(XC, 126, "Đ", "2", "", "currentColor", 18, "middle")
    b += lbl(XC, 236, "12 V", "currentColor", 17, "middle", "700")
    b += lbl(226, 266, "(b) song song: cùng " , "currentColor", 16, "start", "700") + lbl(392, 266, it_("U"), RED, 16, "start", "700")
    b += subt(20, 302, it_("R"), "1", " = ?", ORG) + subt(140, 302, it_("R"), "2", " = ?", ORG)
    return fig("d3-2", "0 0 420 316", "Hai cách mắc: nối tiếp thì hai đèn cùng cường độ dòng điện, song song thì cùng hiệu điện thế 12 vôn", b,
               "Dữ kiện: điện trở mỗi đèn tính từ số ghi.<br>Nối tiếp cùng dòng điện, song song cùng hiệu điện thế.")

# Dạng 4: ấm đun nước, nhiệt kế dâng dần (không ghi thời gian)
def kettle():
    g = '<path d="M60,200 L70,90 Q130,70 190,90 L200,200 Z" fill="rgba(56,189,248,.12)" stroke="currentColor" stroke-width="2.4"/>'
    g += '<path d="M70,110 L30,84" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M190,100 Q232,110 214,170" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    g += '<rect x="50" y="200" width="160" height="14" rx="4" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    return g

def d4(k):
    if k == 0:
        b = kettle()
        b += lbl(20, 32, "Ấm 220 V – 1 500 W", BLUE, 17, "start", "700") + lbl(20, 56, "Hiệu suất 84 %", BLUE, 17, "start", "700")
        tx, ty0, ty1 = 300, 70, 210
        b += f'<rect x="{tx - 10}" y="{ty0}" width="20" height="{ty1 - ty0}" rx="10" fill="none" stroke="currentColor" stroke-width="2.2"/>'
        y20, y100 = ty1 - 0.2 * (ty1 - ty0), ty0 + 6
        b += (f'<rect x="{tx - 6}" y="{y20:.1f}" width="12" height="{ty1 - 4 - y20:.1f}" rx="5" fill="{RED}">'
              f'{smil("y", [y20, y100], 5.0)}{smil("height", [ty1 - 4 - y20, ty1 - 4 - y100], 5.0)}</rect>')
        b += lbl(tx + 18, y20 + 6, "20 °C", "currentColor", 16, "start", "700") + lbl(tx + 18, y100 + 10, "sôi", "currentColor", 16, "start", "700")
        b += lbl(240, 250, it_("t") + " = ?", RED, 18, "start", "700")
        return fig("d4-0", "0 0 420 264", "Ấm điện 1500 oát đun nước, cột nhiệt kế dâng từ 20 độ tới lúc sôi; cần tìm thời gian đun", b,
                   "Mô phỏng (bấm Chạy mô phỏng): cột nhiệt kế dâng tới lúc nước sôi.<br>Hình chạy nhanh hơn thật, không đo thời gian trên hình.")
    b = f'<rect x="16" y="40" width="150" height="60" rx="8" fill="rgba(56,189,248,.12)" stroke="currentColor" stroke-width="2"/>'
    b += lbl(91, 66, "Điện năng", "currentColor", 17, "middle", "700") + lbl(91, 90, it_("A") + " = ?", RED, 17, "middle", "700")
    b += seg(166, 70, 250, 70, ORG, 2.8) + chevron(250, 70, 1, 0, ORG, 2.8, 13)
    b += lbl(208, 58, "84 %", ORG, 16, "middle", "700")
    b += f'<rect x="254" y="40" width="152" height="60" rx="8" fill="rgba(251,146,60,.15)" stroke="currentColor" stroke-width="2"/>'
    b += lbl(330, 66, "Nước nhận", "currentColor", 17, "middle", "700") + lbl(330, 90, "504 000 J", "currentColor", 17, "middle", "700")
    b += seg(91, 100, 91, 150, "currentColor", 2.4, "5 4") + chevron(91, 150, 0, 1, "currentColor", 2.4, 12)
    b += lbl(108, 140, "16 % làm nóng vỏ ấm, không khí", "currentColor", 15, "start", "600")
    b += lbl(16, 190, "⚠ Phần có ích nhỏ hơn điện năng tiêu thụ", RED, 16, "start", "700")
    return fig("d4-2", "0 0 420 204", "Sơ đồ năng lượng: điện năng ấm tiêu thụ, 84 phần trăm thành nhiệt cho nước 504000 jun, 16 phần trăm hao phí", b,
               "Dữ kiện: chỉ 84 % điện năng thành nhiệt cho nước.")

BUILD = [d1, d2, d3, d4]

# ───────────── Đề ─────────────
DE = [
 dict(label="Dạng 1 · Từ số ghi trên thiết bị: tính cường độ dòng điện và điện trở", topic=T94,
      problem_html=r"<p>Một bàn là ghi 220&nbsp;V – 1&nbsp;210&nbsp;W được dùng ở đúng hiệu điện thế $220\ \text{V}$. Coi điện trở của bàn là không đổi.</p>"
                   r"<ol type=\"a\"><li>Nêu ý nghĩa của số 1&nbsp;210&nbsp;W ghi trên bàn là.</li><li>Tính cường độ dòng điện qua bàn là.</li><li>Tính điện trở của bàn là.</li></ol>"),
 dict(label="Dạng 2 · Điện năng tiêu thụ và tiền điện trong một tháng", topic=T93,
      problem_html=r"<p>Trong một tháng ($30$ ngày), nhà bạn Lan dùng:</p>"
                   r"<p>một điều hoà 220&nbsp;V – 1&nbsp;200&nbsp;W, bật $8$ giờ mỗi ngày;</p>"
                   r"<p>năm bóng đèn LED cùng loại 220&nbsp;V – 20&nbsp;W, mỗi bóng bật $6$ giờ mỗi ngày.</p>"
                   r"<p>Các thiết bị dùng ở đúng $220\ \text{V}$. Giá điện coi là $2\,500$&nbsp;đồng cho mỗi $\text{kWh}$ (giá minh hoạ).</p>"
                   r"<ol type=\"a\"><li>Tính điện năng điều hoà tiêu thụ trong tháng, ra $\text{kWh}$.</li><li>Tính điện năng năm bóng đèn tiêu thụ trong tháng.</li>"
                   r"<li>Tính tiền điện phải trả cho các thiết bị này.</li></ol>"),
 dict(label="Dạng 3 · So sánh độ sáng hai bóng đèn khi mắc nối tiếp và song song", topic=T94,
      problem_html=r"<p>Hai bóng đèn: Đ<sub>1</sub> ghi 12&nbsp;V – 6&nbsp;W, Đ<sub>2</sub> ghi 12&nbsp;V – 18&nbsp;W. Coi điện trở mỗi đèn không đổi.</p>"
                   r"<ol type=\"a\"><li>Tính điện trở của mỗi đèn.</li>"
                   r"<li>Mắc hai đèn nối tiếp vào nguồn $12\ \text{V}$. Tính cường độ dòng điện trong mạch và công suất của đèn Đ<sub>1</sub>. Đèn nào sáng hơn?</li>"
                   r"<li>Mắc hai đèn song song vào nguồn $12\ \text{V}$. Đèn nào sáng hơn?</li></ol>"),
 dict(label="Dạng 4 · Tổng hợp: ấm điện có hiệu suất, thời gian đun và tiền điện", topic=T93,
      problem_html=r"<p>Một ấm điện siêu tốc ghi 220&nbsp;V – 1&nbsp;500&nbsp;W, dùng ở đúng $220\ \text{V}$. Muốn đun sôi một ấm nước, nước cần nhận nhiệt lượng $504\,000\ \text{J}$.</p>"
                   r"<p>Hiệu suất của ấm là $84\ \%$: $84\ \%$ điện năng ấm tiêu thụ chuyển thành nhiệt cho nước, phần còn lại làm nóng vỏ ấm và không khí.</p>"
                   r"<ol type=\"a\"><li>Tính điện năng ấm tiêu thụ cho một lần đun.</li><li>Tính thời gian đun một lần.</li>"
                   r"<li>Mỗi ngày đun $2$ lần như vậy. Tính điện năng ấm tiêu thụ trong $30$ ngày, ra $\text{kWh}$, và tiền điện, biết giá $2\,000$&nbsp;đồng cho mỗi $\text{kWh}$ (giá minh hoạ).</li></ol>"),
]
for d_ in DE:
    d_["problem_html"] = d_["problem_html"].replace('\\"', '"')

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [(r"&quot;Nêu ý nghĩa của số 1&nbsp;210&nbsp;W ghi trên bàn là&quot;", r"Số ghi bằng oát", r"Oát là đơn vị đại lượng nào? Số ghi trên thiết bị là giá trị <strong>định mức</strong>"),
  (r"&quot;ghi 220&nbsp;V – 1&nbsp;210&nbsp;W&quot;", r"$U_{\text{đm}}=220\ \text{V}$; $P_{\text{đm}}=1\,210\ \text{W}$", r"Số ghi là hiệu điện thế và công suất <strong>định mức</strong>"),
  (r"&quot;dùng ở đúng hiệu điện thế 220&nbsp;V&quot;", r"$U=U_{\text{đm}}$", r"⚠ Điều kiện: dùng đúng định mức thì công suất thật bằng số ghi"),
  (r"&quot;Tính cường độ dòng điện qua bàn là&quot;", r"Cần $I$", r"$P=UI$"),
  (r"&quot;Coi điện trở của bàn là không đổi&quot;", r"$R$ giữ nguyên", r"⚠ Điều kiện để dùng định luật Ohm cho bàn là"),
  (r"&quot;Tính điện trở của bàn là&quot;", r"Cần $R$", r"$R=\dfrac{U}{I}$ hoặc $R=\dfrac{U^2}{P}$")],
 [(r"&quot;điều hoà 220&nbsp;V – 1&nbsp;200&nbsp;W, bật 8 giờ mỗi ngày&quot;", r"$P=1\,200\ \text{W}$; $8\ \text{h}$/ngày", r"⚠ Muốn ra kWh: $P$ (kW), $t$ (h)"),
  (r"&quot;trong một tháng (30 ngày)&quot;", r"$30$ ngày", r"Thời gian cả tháng = giờ mỗi ngày × số ngày"),
  (r"&quot;năm bóng đèn LED cùng loại 220&nbsp;V – 20&nbsp;W, mỗi bóng bật 6 giờ mỗi ngày&quot;", r"$5$ bóng; $20\ \text{W}$; $6\ \text{h}$/ngày", r"Có mấy bóng cùng tiêu thụ?"),
  (r"&quot;dùng ở đúng 220&nbsp;V&quot;", r"Chạy đúng công suất ghi", r"⚠ Điều kiện để lấy công suất ghi làm $P$"),
  (r"&quot;2&nbsp;500 đồng cho mỗi kWh&quot;", r"Giá điện", r"Tiền = tổng điện năng (kWh) × giá")],
 [(r"&quot;Đ<sub>1</sub> ghi 12&nbsp;V – 6&nbsp;W, Đ<sub>2</sub> ghi 12&nbsp;V – 18&nbsp;W&quot;", r"$U_{\text{đm}}=12\ \text{V}$; $P_1=6\ \text{W}$; $P_2=18\ \text{W}$", r"Số ghi là định mức của từng đèn"),
  (r"&quot;Tính điện trở của mỗi đèn&quot;", r"Cần $R_1$, $R_2$", r"$R=\dfrac{U_{\text{đm}}^2}{P_{\text{đm}}}$ cho từng đèn"),
  (r"&quot;Coi điện trở mỗi đèn không đổi&quot;", r"$R_1$, $R_2$ giữ nguyên", r"⚠ Điều kiện: dùng được $R$ tính từ số ghi ở mọi cách mắc"),
  (r"&quot;Mắc hai đèn nối tiếp vào nguồn 12&nbsp;V&quot;", r"$U=12\ \text{V}$ chia cho hai đèn", r"Nối tiếp: điện trở tương đương? Dòng qua hai đèn thế nào?"),
  (r"&quot;công suất của đèn Đ<sub>1</sub>. Đèn nào sáng hơn?&quot;", r"Cần $P$ thật của mỗi đèn", r"⚠ Số oát ghi chỉ đúng khi đèn có đủ $12\ \text{V}$"),
  (r"&quot;Mắc hai đèn song song vào nguồn 12&nbsp;V&quot;", r"Mỗi đèn có $12\ \text{V}$", r"Mỗi đèn chạy ở điều kiện nào?")],
 [(r"&quot;ghi 220&nbsp;V – 1&nbsp;500&nbsp;W, dùng ở đúng 220&nbsp;V&quot;", r"$P=1\,500\ \text{W}$", r"⚠ Đúng định mức nên công suất thật bằng số ghi"),
  (r"&quot;nước cần nhận nhiệt lượng 504&nbsp;000&nbsp;J&quot;", r"$A_{\text{có ích}}=504\,000\ \text{J}$", r"Phần có ích, chưa phải điện năng tiêu thụ"),
  (r"&quot;Hiệu suất của ấm là 84&nbsp;%&quot;", r"$H=84\ \%$", r"$H=\dfrac{A_{\text{có ích}}}{A}\cdot100\ \%$; điện năng tiêu thụ lớn hơn hay nhỏ hơn phần có ích?"),
  (r"&quot;Tính thời gian đun một lần&quot;", r"Cần $t$", r"$A=P\,t$"),
  (r"&quot;Mỗi ngày đun 2 lần như vậy.&quot;", r"$2$ lần/ngày", r"Số lần đun cả tháng = số lần mỗi ngày × số ngày"),
  (r"&quot;Tính điện năng ấm tiêu thụ trong 30 ngày, ra kWh&quot;", r"$30$ ngày; cần $A$ (kWh)", r"⚠ $1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$"),
  (r"&quot;giá 2&nbsp;000 đồng cho mỗi kWh&quot;", r"Giá điện", r"Tiền = số kWh × giá")],
]

# ───────────── Lời giải ─────────────
RP = [r"<strong>Khái niệm:</strong> công suất điện cho biết điện năng tiêu thụ trong mỗi giây.",
      r"Số ghi: hiệu điện thế định mức và công suất định mức.",
      r"Công thức: $P=UI$; định luật Ohm $R=\dfrac{U}{I}$.",
      r"Đơn vị: $P$ (W), $U$ (V), $I$ (A), $R$ ($\Omega$).",
      r"⚠ <strong>Điều kiện:</strong> chỉ khi dùng đúng hiệu điện thế định mức, công suất thật mới bằng số ghi."]
RA = [r"<strong>Khái niệm:</strong> điện năng tiêu thụ cho biết thiết bị tốn bao nhiêu điện.",
      r"Công thức: $A=P\,t$.",
      r"Đơn vị: $P$ (kW), $t$ (h) thì $A$ (kWh); $1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$.",
      r"Tiền điện = số kWh × giá.",
      r"⚠ <strong>Điều kiện:</strong> thiết bị dùng đúng định mức thì $P$ bằng công suất ghi."]

SOLS = [
 sol(RP, [
  ("Ý nghĩa số ghi", [P("1&nbsp;210&nbsp;W là <strong>công suất định mức</strong>:"), A("T:công suất của bàn là khi dùng đúng 220 V.")]),
  ("Cường độ dòng điện", [P("Dùng đúng 220 V nên $P=1\\,210$ W:"), M(r"I=\dfrac{P}{U}"), M(r"I=\dfrac{1\,210}{220}"), A(r"I=5{,}5\ \text{A}")]),
  ("Điện trở", [M(r"R=\dfrac{U}{I}"), M(r"R=\dfrac{220}{5{,}5}"), A(r"R=40\ \Omega")]),
  ("Kiểm tra", [P("Tính bằng cách khác:"), M(r"R=\dfrac{U^2}{P}=\dfrac{220^2}{1\,210}=40\ \Omega\ ✓"), P("Đơn vị: W chia V ra A ✓")])],
  [r"a) Công suất của bàn là khi dùng đúng 220 V là 1&nbsp;210&nbsp;W", r"b) $I=5{,}5\ \text{A}$", r"c) $R=40\ \Omega$"],
  "Nhận dạng: đề cho <strong>số ghi … V – … W</strong> và dùng đúng định mức → $I=\\dfrac{P}{U}$, $R=\\dfrac{U^2}{P}$."),
 sol(RA, [
  ("Điện năng của điều hoà", [P("Đổi $1\\,200$ W $=1{,}2$ kW. Thời gian cả tháng:"), M(r"t=8\cdot30=240\ \text{h}"), M(r"A_1=1{,}2\cdot240"), A(r"A_1=288\ \text{kWh}")]),
  ("Điện năng của năm bóng đèn", [P("Mỗi bóng $20$ W $=0{,}02$ kW; năm bóng:"), M(r"t=6\cdot30=180\ \text{h}"), M(r"A_2=5\cdot0{,}02\cdot180"), A(r"A_2=18\ \text{kWh}")]),
  ("Tiền điện", [M(r"A=A_1+A_2=288+18=306\ \text{kWh}"), M(r"306\cdot2\,500"), A(r"\text{Tiền}=765\,000\ \text{đồng}")]),
  ("Kiểm tra", [P("Điều hoà công suất lớn, bật lâu: chiếm phần lớn tiền điện ✓"), P("Đơn vị: kW nhân h ra kWh ✓")])],
  [r"a) $A_1=288\ \text{kWh}$", r"b) $A_2=18\ \text{kWh}$", r"c) $765\,000$ đồng"],
  "Nhận dạng: đề cho <strong>số oát, số giờ mỗi ngày, số ngày, giá điện</strong> → đổi kW, $A=P\\,t$ cho từng loại, cộng lại, nhân giá."),
 sol(RP[:2] + [r"Công thức: $P=UI=I^2R=\dfrac{U^2}{R}$.", r"Nối tiếp: $R_{\text{tđ}}=R_1+R_2$, cùng $I$. Song song: cùng $U$.",
               r"⚠ <strong>Điều kiện:</strong> coi điện trở đèn không đổi; đèn nào có công suất thật lớn hơn thì sáng hơn."], [
  ("Điện trở đèn Đ<sub>1</sub>", [M(r"R_1=\dfrac{U_{\text{đm}}^2}{P_1}=\dfrac{12^2}{6}"), A(r"R_1=24\ \Omega")]),
  ("Điện trở đèn Đ<sub>2</sub>", [M(r"R_2=\dfrac{12^2}{18}"), A(r"R_2=8\ \Omega")]),
  ("Dòng điện khi nối tiếp", [M(r"I=\dfrac{U}{R_1+R_2}"), M(r"I=\dfrac{12}{24+8}"), A(r"I=0{,}375\ \text{A}")]),
  ("Công suất đèn Đ<sub>1</sub> khi nối tiếp", [M(r"P_1'=I^2R_1"), M(r"P_1'=0{,}375^2\cdot24"), A(r"P_1'\approx3{,}38\ \text{W}")]),
  ("So sánh khi nối tiếp", [M(r"P_2'=0{,}375^2\cdot8\approx1{,}13\ \text{W}"), A(r"T:$P_1'\gt P_2'$ nên đèn Đ<sub>1</sub> sáng hơn."), P("Đèn ghi ít oát hơn lại sáng hơn.")]),
  ("So sánh khi song song", [P("Mỗi đèn có đúng $12$ V: chạy đúng định mức."), M(r"P_2=18\ \text{W}\gt P_1=6\ \text{W}"), A("T:Đèn Đ<sub>2</sub> sáng hơn.")]),
  ("Kiểm tra", [M(r"U_1=0{,}375\cdot24=9\ \text{V}"), M(r"U_2=0{,}375\cdot8=3\ \text{V}"), M(r"U_1+U_2=12\ \text{V}\ ✓"), P("Nối tiếp, hai đèn đều dưới định mức.<br>Không đèn nào cháy ✓")])],
  [r"a) $R_1=24\ \Omega$", r"$R_2=8\ \Omega$", r"b) $I=0{,}375\ \text{A}$", r"$P_1'\approx3{,}38\ \text{W}$, đèn Đ<sub>1</sub> sáng hơn", r"c) Đèn Đ<sub>2</sub> sáng hơn"],
  "Nhận dạng: <strong>hai đèn khác số oát, mắc nối tiếp</strong> → tính $R$ từ số ghi, cùng $I$ nên so $I^2R$; song song đúng định mức thì so số oát."),
 sol([r"<strong>Khái niệm:</strong> hiệu suất là phần trăm điện năng chuyển thành phần có ích.", r"Công thức: $H=\dfrac{A_{\text{có ích}}}{A}\cdot100\ \%$.",
      r"Điện năng: $A=P\,t$.", r"Đổi: $1\ \text{kWh}=3{,}6\cdot10^6\ \text{J}$; tiền = số kWh × giá.",
      r"⚠ <strong>Điều kiện:</strong> ấm dùng đúng 220 V nên $P=1\,500$ W."], [
  ("Điện năng cho một lần đun", [P("Từ $H=\\dfrac{A_{\\text{có ích}}}{A}$:"), M(r"A=\dfrac{A_{\text{có ích}}}{H}"), M(r"A=\dfrac{504\,000}{0{,}84}"), A(r"A=600\,000\ \text{J}")]),
  ("Thời gian đun", [M(r"t=\dfrac{A}{P}"), M(r"t=\dfrac{600\,000}{1\,500}"), A(r"t=400\ \text{s}\approx6{,}7\ \text{phút}")]),
  ("Điện năng trong 30 ngày", [M(r"A_{30}=600\,000\cdot2\cdot30=3{,}6\cdot10^7\ \text{J}"), M(r"A_{30}=\dfrac{3{,}6\cdot10^7}{3{,}6\cdot10^6}"), A(r"A_{30}=10\ \text{kWh}")]),
  ("Tiền điện", [M(r"10\cdot2\,000"), A(r"\text{Tiền}=20\,000\ \text{đồng}")]),
  ("Kiểm tra", [P("Tính bằng kW và h:"), M(r"t=\dfrac{400}{3\,600}\ \text{h}"), M(r"A_{30}=1{,}5\cdot\dfrac{400}{3\,600}\cdot2\cdot30"), M(r"A_{30}=10\ \text{kWh}\ ✓"), P("Điện năng tiêu thụ lớn hơn phần nước nhận.<br>Hợp lí ✓")])],
  [r"a) $A=600\,000\ \text{J}$", r"b) $t=400\ \text{s}$", r"c) $10\ \text{kWh}$", r"Tiền điện $20\,000$ đồng"],
  "Nhận dạng: đề cho <strong>nhiệt lượng nước cần</strong> và <strong>hiệu suất</strong> → $A=\\dfrac{A_{\\text{có ích}}}{H}$, rồi $t=\\dfrac{A}{P}$, đổi J ra kWh."),
]

# ───────────── Tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>số ghi … V – … W</b> và <b>dùng đúng … V</b> → $I=\dfrac{P}{U}$, $R=\dfrac{U^2}{P}$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Ý nghĩa số ghi", "Số 1 210 W ghi trên bàn là cho biết gì?",
       loi=r"Hay coi oát là lượng điện tiêu thụ. Oát đo công suất, và số ghi chỉ đúng khi dùng đúng hiệu điện thế ghi kèm.",
       lua_chon=[("Công suất của bàn là khi dùng đúng 220 V", True),
                 ("Điện năng bàn là tiêu thụ trong mỗi giờ", r"W là đơn vị công suất. Điện năng mỗi giờ phải tính bằng kWh, không phải W."),
                 ("Công suất của bàn là ở mọi hiệu điện thế", r"Số ghi là định mức: dùng hiệu điện thế thấp hơn thì công suất nhỏ hơn.")]),
  buoc("Cường độ dòng điện", "Cường độ dòng điện qua bàn là bằng bao nhiêu?", 5.5, "A", 0.05,
       loi=r"Hay chia ngược $\dfrac{U}{P}$ ra một số nhỏ hơn 1, vô lí với bàn là công suất lớn. Từ $P=UI$ suy ra $I=\dfrac{P}{U}$.",
       ke=[(r"$I=\dfrac{P}{U}$", True),
           (r"$I=\dfrac{U}{P}$", r"Chia ngược: từ $P=UI$ phải chia $P$ cho $U$."),
           (r"$I=P\cdot U$", r"Nhân thì đơn vị là W·V, không phải ampe.")]),
  buoc("Điện trở", "Điện trở của bàn là bằng bao nhiêu?", 40, "Ω", 0.3,
       loi=r"Hay lấy $\dfrac{P}{I}$: kết quả đó là hiệu điện thế (V), không phải điện trở.",
       ke=[(r"$R=\dfrac{U}{I}$ (hoặc $\dfrac{U^2}{P}$)", True),
           (r"$R=\dfrac{P}{I}$", r"$\dfrac{P}{I}$ bằng $U$, đơn vị vôn, không phải ôm."),
           (r"$R=\dfrac{U^2}{I}$", r"Sai mẫu số: $R=\dfrac{U^2}{P}$, không chia cho $I$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>số oát, số giờ mỗi ngày, số ngày, giá mỗi kWh</b> → đổi kW, $A=P\,t$ từng loại, cộng rồi nhân giá.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Điện năng của điều hoà", "Điện năng điều hoà tiêu thụ trong tháng bằng bao nhiêu kWh?", 288, "kWh", 1,
       loi=r"Hay giữ $1\,200$ W mà không đổi ra kW: kết quả lớn gấp một nghìn lần. Muốn ra kWh thì $P$ (kW), $t$ (h)."),
  buoc("Điện năng của năm bóng đèn", "Điện năng năm bóng đèn tiêu thụ trong tháng bằng bao nhiêu kWh?", 18, "kWh", 0.2,
       loi=r"Hay chỉ tính một bóng. Năm bóng cùng bật nên điện năng gấp năm lần một bóng.",
       ke=[(r"$A=5\cdot P\cdot t$ với $P$ (kW), $t$ (h) cả tháng", True),
           (r"$A=P\cdot t$ của một bóng", r"Có năm bóng cùng bật, phải nhân thêm 5."),
           (r"$A=5\cdot P\cdot t$ với $P$ (W), $t$ (h)", r"Để $P$ theo W thì $A$ ra Wh, chưa phải kWh.")]),
  buoc("Tiền điện", "Tiền điện phải trả cho các thiết bị này là bao nhiêu đồng?", 765000, "đồng", 500,
       loi=r"Hay chỉ nhân giá với điện năng của điều hoà, quên phần của đèn.",
       ke=[(r"Cộng điện năng hai loại rồi nhân giá", True),
           (r"Chỉ nhân giá với điện năng của điều hoà", r"Đề hỏi tiền điện của các thiết bị này: phải tính cả đèn."),
           (r"Nhân giá với tổng công suất (kW)", r"Tiền điện tính theo điện năng (kWh), không theo công suất.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hai đèn khác số oát mắc nối tiếp</b> → $R=\dfrac{U^2}{P}$ từ số ghi, cùng $I$ nên so $I^2R$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Điện trở đèn Đ1", "Điện trở của đèn Đ1 bằng bao nhiêu?", 24, "Ω", 0.2,
       loi=r"Hay tính $\dfrac{P}{U}$ (đó là cường độ dòng định mức) hoặc $\dfrac{U}{P}$. Điện trở là $\dfrac{U^2}{P}$."),
  buoc("Điện trở đèn Đ2", "Điện trở của đèn Đ2 bằng bao nhiêu?", 8, "Ω", 0.1,
       loi=r"Hay nghĩ đèn nhiều oát hơn thì điện trở lớn hơn. Cùng $U$, $R=\dfrac{U^2}{P}$ nên $P$ lớn thì $R$ nhỏ.",
       ke=[(r"$R_2=\dfrac{U_{\text{đm}}^2}{P_2}$", True),
           (r"$R_2=\dfrac{P_2}{U_{\text{đm}}}$", r"$\dfrac{P}{U}$ là cường độ dòng định mức (A), không phải điện trở."),
           (r"$R_2=R_1\cdot\dfrac{P_2}{P_1}$", r"Cùng $U$, $R$ tỉ lệ nghịch với $P$: phải chia, không nhân.")]),
  buoc("Dòng điện khi nối tiếp", "Cường độ dòng điện trong mạch nối tiếp bằng bao nhiêu?", 0.375, "A", 0.005,
       loi=r"Hay cộng hai dòng định mức $\dfrac{P_1}{U}+\dfrac{P_2}{U}$. Nối tiếp thì điện trở cộng lại, dòng đi qua cả hai đèn như nhau.",
       ke=[(r"$I=\dfrac{U}{R_1+R_2}$", True),
           (r"$I=\dfrac{U}{R_1}+\dfrac{U}{R_2}$", r"Đó là dòng tổng khi mắc song song; nối tiếp thì điện trở cộng lại."),
           (r"$I=\dfrac{P_1+P_2}{U}$", r"Công suất ghi chỉ đúng khi mỗi đèn có đủ $12$ V; nối tiếp mỗi đèn chỉ nhận một phần.")]),
  buoc("Công suất đèn Đ1 khi nối tiếp", "Công suất thật của đèn Đ1 khi nối tiếp bằng bao nhiêu?", 3.375, "W", 0.03,
       loi=r"Hay lấy luôn $6$ W ghi trên đèn. Khi nối tiếp, Đ1 không có đủ $12$ V nên công suất nhỏ hơn số ghi.",
       ke=[(r"$P_1'=I^2R_1$", True),
           (r"$P_1'=6\ \text{W}$ vì đèn ghi $6$ W", r"Số ghi chỉ đúng khi đèn có đủ $12$ V; nối tiếp thì không."),
           (r"$P_1'=\dfrac{12^2}{R_1}$", r"Đèn Đ1 không có đủ $12$ V khi nối tiếp; dùng $I^2R$ với dòng trong mạch.")]),
  buoc("So sánh khi nối tiếp", "Khi nối tiếp, đèn nào sáng hơn?",
       loi=r"Hay chọn đèn ghi nhiều oát hơn. Nối tiếp cùng $I$, đèn có $R$ lớn hơn có $I^2R$ lớn hơn.",
       lua_chon=[("Đèn Đ1", True),
                 ("Đèn Đ2, vì ghi nhiều oát hơn", r"Số oát ghi chỉ đúng khi đủ $12$ V. Nối tiếp, $P_2'=I^2R_2$ nhỏ hơn vì $R_2$ nhỏ."),
                 ("Hai đèn sáng như nhau vì cùng dòng điện", r"Cùng $I$ nhưng $R$ khác nhau thì $I^2R$ khác nhau.")],
       ke=[(r"Tính $P_2'=I^2R_2$ rồi so với $P_1'$", True),
           (r"So hai số oát ghi trên đèn", r"Số ghi là định mức, không phải công suất thật khi nối tiếp."),
           (r"So hai hiệu điện thế định mức", r"Hai đèn cùng ghi $12$ V nên không so được gì.")]),
  buoc("So sánh khi song song", "Khi mắc song song vào 12 V, đèn nào sáng hơn?",
       loi=r"Hay giữ kết quả của mạch nối tiếp. Song song thì mỗi đèn có đủ $12$ V, chạy đúng định mức.",
       lua_chon=[("Đèn Đ2", True),
                 ("Đèn Đ1, giống khi nối tiếp", r"Mạch đã đổi: song song mỗi đèn có đủ $12$ V, công suất bằng số ghi."),
                 ("Hai đèn sáng như nhau vì cùng hiệu điện thế", r"Cùng $U$ nhưng $R$ khác nhau thì $\dfrac{U^2}{R}$ khác nhau.")],
       ke=[(r"Mỗi đèn có đúng $12$ V: so hai công suất định mức", True),
           (r"Dùng lại dòng điện của mạch nối tiếp", r"Đó là mạch khác; song song mỗi đèn có dòng riêng."),
           (r"So hai điện trở: đèn $R$ lớn sáng hơn", r"Quy tắc đó chỉ đúng khi cùng $I$ (nối tiếp). Song song cùng $U$ thì đèn $R$ nhỏ sáng hơn.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>nhiệt lượng nước cần</b> và <b>hiệu suất</b> → $A=\dfrac{A_{\text{có ích}}}{H}$, $t=\dfrac{A}{P}$, đổi J ra kWh.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Điện năng cho một lần đun", "Điện năng ấm tiêu thụ cho một lần đun bằng bao nhiêu jun?", 600000, "J", 1000,
       loi=r"Hay nhân $504\,000\cdot0{,}84$: ra số nhỏ hơn phần nước nhận, vô lí. Điện năng tiêu thụ phải lớn hơn phần có ích nên chia cho $H$."),
  buoc("Thời gian đun", "Thời gian đun một lần bằng bao nhiêu giây?", 400, "s", 2,
       loi=r"Hay chia thẳng nhiệt lượng nước nhận cho công suất, bỏ quên hiệu suất: thời gian tính ra ngắn hơn thật.",
       ke=[(r"$t=\dfrac{A}{P}$ với $A$ là điện năng tiêu thụ", True),
           (r"$t=\dfrac{504\,000}{P}$", r"$P$ là công suất điện tiêu thụ, phải chia điện năng tiêu thụ, không phải phần nước nhận."),
           (r"$t=A\cdot P$", r"Từ $A=P\,t$ suy ra $t=\dfrac{A}{P}$; nhân sẽ sai cả đơn vị.")]),
  buoc("Điện năng trong 30 ngày", "Điện năng ấm tiêu thụ trong 30 ngày bằng bao nhiêu kWh?", 10, "kWh", 0.05,
       loi=r"Hay đổi J ra kWh bằng cách chia cho $1\,000$. Đúng là chia cho $3{,}6\cdot10^6$ vì $1\ \text{kWh}=1\,000\ \text{W}\cdot3\,600\ \text{s}$.",
       ke=[(r"Nhân với số lần đun cả tháng ($2$ lần/ngày), rồi chia cho số jun trong một kWh", True),
           (r"Nhân với số lần đun cả tháng, rồi chia cho $1\,000$", r"Chia $1\,000$ chỉ đổi J ra kJ; một kWh là $1\,000\ \text{W}$ nhân $3\,600\ \text{s}$."),
           (r"Chỉ nhân với số ngày, rồi chia cho số jun trong một kWh", r"Mỗi ngày đun $2$ lần, phải nhân thêm 2.")]),
  buoc("Tiền điện", "Tiền điện cho ấm trong 30 ngày là bao nhiêu đồng?", 20000, "đồng", 100,
       loi=r"Hay nhân giá với số jun. Giá điện tính cho mỗi kWh nên phải dùng số kWh.",
       ke=[(r"Số kWh × giá", True),
           (r"Số jun × giá", r"Giá điện tính theo kWh; nhân với số jun ra số tiền khổng lồ, vô lí."),
           (r"Công suất (kW) × giá", r"Tiền điện tính theo điện năng, không theo công suất.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Ghi JSON ─────────────
d = {"lesson_id": 91, "lesson_title": "Bài 13. Năng lượng của dòng điện và công suất điện", "generated_at": "2026-10-12",
     "review": {"checked": False, "notes": "Soạn 12/10/2026 (chặng 3). Chưa kiểm chéo kiem-code. Chưa đối chiếu ngân hàng câu hỏi (topic 93/94)."},
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
print("xong 91.json")
