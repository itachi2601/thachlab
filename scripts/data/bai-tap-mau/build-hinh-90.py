"""Bài tập mẫu bài 90 — Bài 12. Đoạn mạch nối tiếp, song song (KHTN 9). Dựng 4 dạng + hình + lời giải + buoc[] → 90.json.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-90.py   (idempotent: ghi lại toàn bộ 90.json, review.checked=false)
Danh sách dạng: scripts/data/bai-tap-mau/90.dang.md. Mọi số liệu tính ở đầu file, có assert.
Số liệu KHÁC lý thuyết bài 90 (10/20; 10//15; 6//12; 2+(6//6); 20//30; 4+(12//6) 12 V; 3+(6//3) 10 V)."""
import json, math, os, sys, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "90.json")
T1 = "Điện trở tương đương của đoạn mạch"
T2 = "Tính U, I trong mạch hỗn hợp"
def ss(a, b): return a * b / (a + b)

# ───────────── Số liệu (tính + kiểm) ─────────────
# Dạng 1: nối tiếp R1 = 15, R2 = 25, U = 12 V
a1, b1, U1 = 15.0, 25.0, 12.0
Rt1 = a1 + b1; I1 = U1 / Rt1; U1a, U1b = I1 * a1, I1 * b1
assert Rt1 == 40 and abs(I1 - 0.3) < 1e-12 and abs(U1a - 4.5) < 1e-12 and abs(U1b - 7.5) < 1e-12
assert abs(ss(a1, b1) - Rt1) > 1 and abs(U1 / a1 - I1) > 0.1 and abs(U1 / 2 - U1a) > 1      # cách sai: song song (9,4) · dùng R1 (0,8 A) · chia đôi U (6 V)

# Dạng 2: song song R1 = 40, R2 = 60, U = 12 V
a2, b2, U2 = 40.0, 60.0, 12.0
Rt2 = ss(a2, b2); I21, I22 = U2 / a2, U2 / b2; I2 = I21 + I22
assert abs(Rt2 - 24) < 1e-12 and abs(I21 - 0.3) < 1e-12 and abs(I22 - 0.2) < 1e-12 and abs(I2 - 0.5) < 1e-12
assert abs(U2 / Rt2 - I2) < 1e-12
assert abs((a2 + b2) - Rt2) > 1 and abs((a2 + b2) / 2 - Rt2) > 1 and abs(1 / a2 + 1 / b2 - Rt2) > 1   # 100 · 50 · 0,042
assert abs((U2 / 2) / a2 - I21) > 0.1 and abs(U2 / (a2 + b2) - I2) > 0.1                    # chia đôi U (0,15) · cộng R (0,12)

# Dạng 3: R1 = 5 nt (R2 = 15 // R3 = 30), U = 18 V
a3, b3, c3, U3 = 5.0, 15.0, 30.0, 18.0
R23 = ss(b3, c3); Rt3 = a3 + R23; I3 = U3 / Rt3; U23 = I3 * R23; I32, I33 = U23 / b3, U23 / c3
assert abs(R23 - 10) < 1e-12 and abs(Rt3 - 15) < 1e-12 and abs(I3 - 1.2) < 1e-12 and abs(U23 - 12) < 1e-12
assert abs(I32 - 0.8) < 1e-12 and abs(I33 - 0.4) < 1e-12 and abs(I32 + I33 - I3) < 1e-12
assert abs(a3 + b3 + c3 - Rt3) > 1 and abs(ss(a3 + b3, c3) - Rt3) > 1                       # 50 · 12
assert abs(U3 / a3 - I3) > 1 and abs(U3 / b3 + U3 / c3 - I3) > 0.5                         # U/R1 (3,6) · coi cụm nhận đủ U (1,8)
assert abs(U3 / 2 - U23) > 1 and abs(I3 * b3 - U23) > 1 and abs(U3 - U23) > 1                 # chia đôi U (9) · I·R2 (18) · U nguồn (18)
assert abs(U3 / c3 - I33) > 0.1 and abs(I3 / 2 - I33) > 0.1                                   # U nguồn chia R3 (0,6) · chia đôi I (0,6)

# Dạng 4: đèn sáng bình thường khi Uđ = 6 V, Rđ = 12 Ω; nguồn 9 V; Rx nối tiếp
Ud, Rd, U4 = 6.0, 12.0, 9.0
Id = Ud / Rd; Rt4 = U4 / Id; Rx = Rt4 - Rd
Id_sai = U4 / Rd                     # lỡ mắc Rx song song với đèn rồi nối thẳng vào nguồn: đèn nhận đủ 9 V
assert abs(Id - 0.5) < 1e-12 and abs(Rt4 - 18) < 1e-12 and abs(Rx - 6) < 1e-12 and abs(Id_sai - 0.75) < 1e-12
assert abs(U4 / Id - Rx) > 1 and abs((U4 - Ud) / Id - Rx) < 1e-12 and abs(U4 / Rd - Id) > 0.1   # quên trừ Rđ (18)
assert abs(Rx * Id + Ud - U4) < 1e-12

# ───────────── Hình ─────────────
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'
def L(x, y, base, idx="", rest="", c="currentColor", size=17, anchor="start"):
    """Nhãn ký hiệu nghiêng, chỉ số dưới bằng tspan dy (không dùng ₁₂)."""
    sub_ = f'<tspan dy="4" font-size="{size - 4}">{idx}</tspan><tspan dy="-4">{rest}</tspan>' if idx else rest
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">{it_(base)}{sub_}</text>')
W = "currentColor"
def res(cx, cy, w=46, h=20, vert=False):
    if vert:
        return f'<rect x="{cx - h / 2:.1f}" y="{cy - w / 2:.1f}" width="{h}" height="{w}" fill="rgba(251,146,60,.2)" stroke="currentColor" stroke-width="2.4"/>'
    return f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w}" height="{h}" fill="rgba(251,146,60,.2)" stroke="currentColor" stroke-width="2.4"/>'
def meter(cx, cy, t, r=18):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>' + lbl(cx, cy + 7, t, W, 18, "middle", "700")
def lamp(cx, cy, r=15):
    k = r * 0.7
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            + seg(cx - k, cy - k, cx + k, cy + k, W, 2) + seg(cx - k, cy + k, cx + k, cy - k, W, 2))
def batt(px, nx, y, txt=None):
    b = seg(px, y - 17, px, y + 17, W, 2.4) + seg(nx, y - 9, nx, y + 9, W, 5)
    b += lbl(px - 6, y - 21, "+", W, 18, "end", "700") + lbl(nx + 6, y - 21, "−", W, 18, "start", "700")
    if txt: b += lbl((px + nx) / 2, y + 40, txt, BLUE, 16, "middle", "700")
    return b
def nf(v):
    t = f"{v:.1f}"
    return t[:-2] if t.endswith(".0") else t
def chev(x, y, dx, dy, c, w=2.6, Ln=12):
    """Đầu V 30° như svg_lib.chevron nhưng toạ độ làm tròn 0,1 và bỏ thuộc tính thừa (hình nhỏ hơn)."""
    n_ = math.hypot(dx, dy); ux, uy = dx / n_, dy / n_; pts = []
    for sg in (1, -1):
        t = math.radians(30 * sg); bx, by = ux * math.cos(t) - uy * math.sin(t), ux * math.sin(t) + uy * math.cos(t)
        pts.append((x - Ln * bx, y - Ln * by))
    return f'<path d="M{nf(pts[0][0])},{nf(pts[0][1])}L{nf(x)},{nf(y)}L{nf(pts[1][0])},{nf(pts[1][1])}" fill="none" stroke="{c}" stroke-width="{w}"/>'
def wire(pts): return '<polyline fill="none" stroke="currentColor" stroke-width="2.4" points="' + " ".join(f"{nf(x)},{nf(y)}" for x, y in pts) + '"/>'

def flow(corners, ndots=3, dur=6.0, off=0.0):
    """Chấm chạy theo chiều dòng điện quy ước, MỘT vòng khi bấm. Chỉ ghi các góc + keyTimes (hình nhỏ)."""
    segs = list(zip(corners, corners[1:] + corners[:1]))
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
    tot = sum(lens); cum = [sum(lens[:k]) for k in range(len(lens))]
    def at(sv):
        sv %= tot
        for (a, b), c0, Ln in zip(segs, cum, lens):
            if sv <= c0 + Ln + 1e-9:
                f = (sv - c0) / Ln; return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
    out = ""
    for d in range(ndots):
        s0 = tot * (d + off) / ndots
        stops = [s0] + sorted({c if c > s0 else c + tot for c in cum} - {s0}) + [s0 + tot]
        pts = [at(x) for x in stops]; kt = [(x - s0) / tot for x in stops]
        ktx = ";".join(f"{k:.3f}".rstrip("0").rstrip(".") for k in kt)
        out += (f'<circle cx="{nf(pts[0][0])}" cy="{nf(pts[0][1])}" r="4" fill="{ORG}">'
                + "".join(f'<animate attributeName="{a}" values="{";".join(nf(p[n]) for p in pts)}" keyTimes="{ktx}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>' for a, n in (("cx", 0), ("cy", 1)))
                + '</circle>')
    return out
CAP_FLOW = "Chấm cam chạy theo chiều dòng điện quy ước: từ cực (+), qua mạch, về cực (−).<br>Chấm chỉ minh hoạ chiều dòng điện, không cho biết cường độ.<br>Tốc độ chấm chỉ để minh hoạ, không đúng thời gian thật."

# ---- Dạng 1: nối tiếp
XL, XR, YT, YB, PX, NX = 40, 380, 120, 236, 203, 217
def d1(k):
    b = wire([(XL, 160), (XL, YT), (127, YT)]) + res(150, YT) + wire([(173, YT), (245, YT)]) + res(268, YT)
    b += wire([(291, YT), (XR, YT), (XR, YB), (NX, YB)]) + wire([(PX, YB), (XL, YB), (XL, 196)])
    b += meter(XL, 178, "A") + batt(PX, NX, YB)
    b += wire([(95, YT), (95, 48), (192, 48)]) + meter(210, 48, "V") + wire([(228, 48), (325, 48), (325, YT)])
    b += dot(95, YT, 4) + dot(325, YT, 4) + lbl(88, YT + 26, "A", W, 16, "end", "700") + lbl(332, YT + 26, "B", W, 16, "start", "700")
    b += chev(70, YT, 1, 0, RED, 2.6, 12) + chev(352, YT, 1, 0, RED, 2.6, 12) + chev(XR, 180, 0, 1, RED, 2.6, 12) + chev(120, YB, -1, 0, RED, 2.6, 12)
    if k == 0:
        b += L(150, YT - 18, "R", "1", "", W, 17, "middle") + L(268, YT - 18, "R", "2", "", W, 17, "middle")
        b += lbl(150, YT + 34, "15 Ω", ORG, 16, "middle", "700") + lbl(268, YT + 34, "25 Ω", ORG, 16, "middle", "700")
        b += lbl(252, 30, "12 V", BLUE, 16, "start", "700") + lbl(XL + 24, 214, "?", RED, 18, "start", "700")
        b += flow([(PX, YB), (XL, YB), (XL, YT), (XR, YT), (XR, YB), (NX, YB)], 4, 6.0)
        return fig("d1-0", "0 0 420 262", "Đoạn mạch nối tiếp: R1 15 ôm và R2 25 ôm nối tiếp giữa A và B, vôn kế chỉ 12 vôn giữa A và B, ampe kế nối tiếp chưa biết số chỉ", b,
                   "Mô phỏng (bấm Chạy mô phỏng).<br>" + CAP_FLOW)
    b += L(150, YT - 18, "R", "1", " = 15 Ω", ORG, 16, "middle") + L(268, YT - 18, "R", "2", " = 25 Ω", ORG, 16, "middle")
    b += L(252, 30, "U", "AB", " = 12 V", BLUE, 15)
    b += lbl(16, 282, "Một đường đi: ampe kế đo I chung", RED, 15, "start", "700")
    return fig("d1-2", "0 0 420 292", "Sơ đồ mạch nối tiếp với dữ kiện: hai điện trở, hiệu điện thế giữa A và B", b,
               "Dữ kiện: vôn kế đo $U_{AB}$ của cả đoạn mạch.<br>Ampe kế nối tiếp đo dòng chung của $R_1$ và $R_2.$")

# ---- Dạng 2: song song (ampe kế mạch chính + vôn kế giữa A, B)
XA, XB, YU, YLo = 120, 330, 110, 190
YM = (YU + YLo) / 2
YB2 = 272
def d2(k):
    b = wire([(XA, YU), (XA, YLo)]) + wire([(XB, YU), (XB, YLo)])
    for y in (YU, YLo):
        b += wire([(XA, y), (202, y)]) + res(225, y) + wire([(248, y), (XB, y)]) + chev(175, y, 1, 0, RED, 2.6, 12)
    b += wire([(XA, YM), (XL, YM), (XL, 202)]) + meter(XL, 220, "A") + wire([(XL, 238), (XL, YB2), (PX, YB2)])
    b += batt(PX, NX, YB2) + wire([(NX, YB2), (385, YB2), (385, YM), (XB, YM)])
    b += wire([(XA, YU), (XA, 40), (207, 40)]) + meter(225, 40, "V") + wire([(243, 40), (XB, 40), (XB, YU)])
    b += dot(XA, YM, 4) + dot(XB, YM, 4) + lbl(XA - 8, YM + 24, "A", W, 16, "end", "700") + lbl(XB + 8, YM + 24, "B", W, 16, "start", "700")
    if k == 0:
        b += L(225, YU - 18, "R", "1", "", W, 17, "middle") + L(225, YLo + 34, "R", "2", "", W, 17, "middle")
    b += chev(80, YM, 1, 0, RED, 2.6, 12) + chev(385, 230, 0, 1, RED, 2.6, 12) + chev(300, YB2, -1, 0, RED, 2.6, 12)
    if k == 0:
        b += lbl(258, YU - 16, "40 Ω", ORG, 16, "start", "700") + lbl(258, YLo + 32, "60 Ω", ORG, 16, "start", "700")
        b += lbl(268, 28, "12 V", BLUE, 16, "start", "700") + lbl(XL + 24, 254, "?", RED, 18, "start", "700")
        up = [(PX, YB2), (XL, YB2), (XL, YM), (XA, YM), (XA, YU), (XB, YU), (XB, YM), (385, YM), (385, YB2), (NX, YB2)]
        lo = [(PX, YB2), (XL, YB2), (XL, YM), (XA, YM), (XA, YLo), (XB, YLo), (XB, YM), (385, YM), (385, YB2), (NX, YB2)]
        b += flow(up, 1, 6.0) + flow(lo, 1, 6.0, 0.5)
        return fig("d2-0", "0 0 420 300", "Đoạn mạch song song: R1 40 ôm và R2 60 ôm nối chung hai điểm A và B, vôn kế chỉ 12 vôn, ampe kế mạch chính chưa biết số chỉ", b,
                   "Mô phỏng (bấm Chạy mô phỏng): tới A dòng điện rẽ hai nhánh, tới B nhập lại.<br>" + CAP_FLOW)
    b += L(225, YU - 18, "R", "1", " = 40 Ω", ORG, 16, "middle") + L(225, YLo + 34, "R", "2", " = 60 Ω", ORG, 16, "middle")
    b += L(268, 28, "U", "AB", " = 12 V", BLUE, 15)
    return fig("d2-2", "0 0 420 300", "Sơ đồ mạch song song với dữ kiện: hai điện trở cùng nối vào A và B, hiệu điện thế giữa A và B", b,
               "Dữ kiện: hai nhánh cùng nối vào $A$ và $B.$<br>Ampe kế ở dây bên trái đo dòng mạch chính.")

# ---- Dạng 3: R1 nối tiếp (R2 // R3), vôn kế giữa M, N
XM, XN, YU3, YL3, YT3 = 160, 330, 82, 152, 117
YB3 = 262
def d3(k):
    b = wire([(XL, 170), (XL, YT3), (77, YT3)]) + res(100, YT3) + wire([(123, YT3), (XM, YT3)])
    b += wire([(XM, YU3), (XM, YL3)]) + wire([(XN, YU3), (XN, YL3)])
    for y in (YU3, YL3):
        b += wire([(XM, y), (222, y)]) + res(245, y) + wire([(268, y), (XN, y)]) + chev(197, y, 1, 0, RED, 2.6, 12)
    b += wire([(XN, YT3), (XR, YT3), (XR, YB3), (NX, YB3)]) + wire([(PX, YB3), (XL, YB3), (XL, 206)]) + meter(XL, 188, "A")
    b += batt(PX, NX, YB3)
    b += wire([(XM, YU3), (XM, 34), (227, 34)]) + meter(245, 34, "V") + wire([(263, 34), (XN, 34), (XN, YU3)])
    b += dot(XM, YT3, 4) + dot(XN, YT3, 4) + lbl(XM - 8, YT3 + 24, "M", W, 16, "end", "700") + lbl(XN + 8, YT3 + 24, "N", W, 16, "start", "700")
    if k == 0:
        b += L(100, YT3 - 18, "R", "1", "", W, 17, "middle") + L(245, YU3 - 16, "R", "2", "", W, 17, "middle") + L(245, YL3 + 32, "R", "3", "", W, 17, "middle")
    b += chev(XL, 140, 0, -1, RED, 2.6, 12) + chev(360, YT3, 1, 0, RED, 2.6, 12) + chev(300, YB3, -1, 0, RED, 2.6, 12)
    if k == 0:
        b += lbl(100, YT3 + 34, "5 Ω", ORG, 16, "middle", "700") + lbl(274, YU3 - 14, "15 Ω", ORG, 16, "start", "700") + lbl(274, YL3 + 32, "30 Ω", ORG, 16, "start", "700")
        b += lbl(XR - 4, YB3 + 40, "nguồn 18 V", BLUE, 16, "end", "700")
        b += lbl(XL + 24, 226, "?", RED, 18, "start", "700") + lbl(272, 24, "?", RED, 18, "start", "700")
        up = [(PX, YB3), (XL, YB3), (XL, YT3), (XM, YT3), (XM, YU3), (XN, YU3), (XN, YT3), (XR, YT3), (XR, YB3), (NX, YB3)]
        lo = [(PX, YB3), (XL, YB3), (XL, YT3), (XM, YT3), (XM, YL3), (XN, YL3), (XN, YT3), (XR, YT3), (XR, YB3), (NX, YB3)]
        b += flow(up, 1, 6.0) + flow(lo, 1, 6.0, 0.5)
        return fig("d3-0", "0 0 420 312", "Mạch: R1 5 ôm nối tiếp cụm R2 15 ôm song song R3 30 ôm, nguồn 18 vôn", b,
                   "Mô phỏng: qua $R_1,$ tới $M$ rẽ hai nhánh, tới $N$ nhập lại.<br>" + CAP_FLOW)
    b += L(100, YT3 - 18, "R", "1", " = 5 Ω", ORG, 16, "middle") + L(245, YU3 - 16, "R", "2", " = 15 Ω", ORG, 16, "middle") + L(245, YL3 + 32, "R", "3", " = 30 Ω", ORG, 16, "middle")
    b += L(XR - 4, YB3 + 40, "U", "", " = 18 V", BLUE, 15, "end")
    b += lbl(16, 300, "Cụm nằm giữa M và N: gộp trước", RED, 15, "start", "700")
    return fig("d3-2", "0 0 420 312", "Sơ đồ mạch hỗn hợp với dữ kiện: R1 nối tiếp cụm R2 song song R3 giữa hai điểm M và N", b,
               "Dữ kiện: $R_2,$ $R_3$ cùng nối vào $M$ và $N.$<br>Vôn kế đo hiệu điện thế giữa $M$ và $N.$")

# ---- Dạng 4: đèn nối tiếp điện trở Rx
def d4(k):
    if k == 0:
        b = wire([(XL, YB), (XL, YT), (148, YT)]) + lamp(165, YT) + wire([(180, YT), (255, YT)]) + res(278, YT) + wire([(301, YT), (XR, YT), (XR, YB), (NX, YB)])
        b += wire([(PX, YB), (XL, YB)]) + batt(PX, NX, YB, "9 V")
        b += lbl(165, YT - 26, "đèn", W, 16, "middle", "700") + lbl(165, YT + 40, "6 V", ORG, 15, "middle", "700") + lbl(165, YT + 60, "12 Ω", ORG, 15, "middle", "700")
        b += L(278, YT - 20, "R", "x", " = ?", RED, 17, "middle")
        b += chev(XL, 180, 0, -1, RED, 2.6, 12) + chev(220, YT, 1, 0, RED, 2.6, 12) + chev(XR, 180, 0, 1, RED, 2.6, 12) + chev(120, YB, -1, 0, RED, 2.6, 12)
        b += flow([(PX, YB), (XL, YB), (XL, YT), (XR, YT), (XR, YB), (NX, YB)], 4, 6.0)
        return fig("d4-0", "0 0 420 290", "Mạch: nguồn 9 vôn, đèn sáng bình thường ở 6 vôn có điện trở 12 ôm, mắc nối tiếp với điện trở Rx chưa biết", b,
                   "Mô phỏng (bấm Chạy mô phỏng).<br>" + CAP_FLOW)
    # hình dữ kiện: (a) cách mắc đúng (nối tiếp), (b) cách mắc nhầm (song song)
    b = lbl(10, 24, "(a) nối tiếp (câu a, b)", W, 15, "start", "700")
    y = 70
    b += wire([(20, y), (48, y)]) + lamp(63, y) + wire([(78, y), (115, y)]) + res(138, y, 40, 18) + wire([(158, y), (195, y)])
    b += L(138, y - 16, "R", "x", "", W, 16, "middle") + lbl(63, y + 36, "đèn", W, 15, "middle", "700")
    b += lbl(10, 140, "nối vào nguồn 9 V", BLUE, 15, "start", "700")
    b += seg(210, 10, 210, 210, W, 1.2, "5 5", .5)
    b += lbl(220, 24, "(b) mắc nhầm (câu c)", W, 15, "start", "700")
    yu, yl = 70, 124
    b += wire([(222, 97), (250, 97)]) + wire([(250, yu), (250, yl)]) + wire([(370, yu), (370, yl)]) + wire([(370, 97), (400, 97)])
    b += wire([(250, yu), (295, yu)]) + lamp(310, yu) + wire([(325, yu), (370, yu)])
    b += wire([(250, yl), (290, yl)]) + res(310, yl, 40, 18) + wire([(330, yl), (370, yl)])
    b += L(310, yl + 32, "R", "x", "", W, 16, "middle") + lbl(310, yu - 22, "đèn", W, 15, "middle", "700")
    b += lbl(220, 184, "nối thẳng vào nguồn 9 V", BLUE, 15, "start", "700")
    b += lbl(220, 206, "đèn nhận bao nhiêu vôn?", RED, 15, "start", "700")
    return fig("d4-2", "0 0 420 216", "Hai cách mắc: đèn nối tiếp điện trở Rx; và mắc nhầm đèn song song với Rx rồi nối vào nguồn 9 vôn", b,
               "Dữ kiện: (a) đèn nối tiếp $R_x.$ (b) đèn song song với $R_x.$<br>Hình minh hoạ, không đúng tỉ lệ.")

BUILD = [d1, d2, d3, d4]

# ───────────── Đề ─────────────
GT = r" Coi nguồn điện lí tưởng, điện trở của dây nối và ampe kế không đáng kể, vôn kế có điện trở rất lớn."
DE = [
 dict(label="Dạng 1 · Đoạn mạch nối tiếp: tính điện trở tương đương, I, U từng điện trở", topic=T1,
      problem_html=r"<p>Cho đoạn mạch $AB$ gồm $R_1 = 15\ \Omega$ mắc nối tiếp với $R_2 = 25\ \Omega$ như hình. Vôn kế mắc giữa $A$ và $B$ chỉ $12\ \text{V}$." + GT + "</p>"
                   r"<ol type='a'><li>Tính điện trở tương đương của đoạn mạch.</li><li>Ampe kế chỉ bao nhiêu?</li><li>Tính hiệu điện thế giữa hai đầu mỗi điện trở.</li></ol>"),
 dict(label="Dạng 2 · Đoạn mạch song song: điện trở tương đương, dòng từng nhánh, dòng mạch chính", topic=T1,
      problem_html=r"<p>Cho đoạn mạch $AB$ gồm $R_1 = 40\ \Omega$ mắc song song với $R_2 = 60\ \Omega$ như hình. Vôn kế mắc giữa $A$ và $B$ chỉ $12\ \text{V}$." + GT + "</p>"
                   r"<ol type='a'><li>Tính điện trở tương đương của đoạn mạch.</li><li>Tính cường độ dòng điện qua mỗi điện trở.</li><li>Ampe kế ở mạch chính chỉ bao nhiêu?</li></ol>"),
 dict(label="Dạng 3 · Mạch hỗn hợp: R₁ nối tiếp (R₂ song song R₃)", topic=T2,
      problem_html=r"<p>Cho mạch điện như hình: $R_1 = 5\ \Omega$ mắc nối tiếp với cụm gồm $R_2 = 15\ \Omega$ song song $R_3 = 30\ \Omega$ (giữa hai điểm $M$, $N$). Hiệu điện thế giữa hai cực nguồn là $18\ \text{V}$." + GT + "</p>"
                   r"<ol type='a'><li>Tính điện trở tương đương của cả mạch.</li><li>Ampe kế ở mạch chính chỉ bao nhiêu?</li><li>Vôn kế mắc giữa $M$ và $N$ chỉ bao nhiêu?</li><li>Tính cường độ dòng điện qua $R_3$.</li></ol>"),
 dict(label="Dạng 4 · Tìm điện trở cần mắc thêm để đèn sáng bình thường", topic=T1,
      problem_html=r"<p>Một bóng đèn sáng bình thường khi hiệu điện thế giữa hai đầu đèn là $6\ \text{V}$; khi đó điện trở của đèn là $12\ \Omega$. Chỉ có nguồn $9\ \text{V}$. Coi nguồn lí tưởng, điện trở của đèn không đổi, điện trở dây nối không đáng kể.</p>"
                   r"<ol type='a'><li>Khi đèn sáng bình thường, cường độ dòng điện qua đèn bằng bao nhiêu?</li><li>Phải mắc nối tiếp với đèn một điện trở $R_x$ bằng bao nhiêu để đèn sáng bình thường?</li>"
                   r"<li>Một bạn mắc nhầm: $R_x$ song song với đèn rồi nối thẳng vào nguồn $9\ \text{V}$. Tính cường độ dòng điện qua đèn. Đèn sẽ thế nào?</li></ol>"),
]

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [(r"&quot;mắc nối tiếp&quot;", r"Một đường đi", r"⚠ Nối tiếp: $I$ như nhau qua mọi điện trở"),
  (r"&quot;R1 = 15&nbsp;Ω … R2 = 25&nbsp;Ω&quot;", r"$R_1=15\ \Omega$; $R_2=25\ \Omega$", r"Điện trở tương đương của đoạn nối tiếp tính thế nào?"),
  (r"&quot;Vôn kế mắc giữa A và B chỉ 12&nbsp;V&quot;", r"$U_{AB}=12\ \text{V}$", r"Vôn kế đo $U$ của cả đoạn $AB$"),
  (r"&quot;Coi nguồn điện lí tưởng, điện trở của dây nối và ampe kế không đáng kể&quot;", r"Chỉ tính hai điện trở", r"⚠ Điều kiện để dùng $R_{td}$ của riêng hai điện trở"),
  (r"&quot;Ampe kế chỉ bao nhiêu?&quot;", r"Cần $I$", r"$I=\dfrac{U_{AB}}{R_{td}}$"),
  (r"&quot;hiệu điện thế giữa hai đầu mỗi điện trở&quot;", r"Cần $U_1$, $U_2$", r"$U=IR$ cho từng điện trở")],
 [(r"&quot;mắc song song&quot;", r"Hai đầu nối chung $A$, $B$", r"⚠ Song song: $U$ như nhau ở mọi nhánh"),
  (r"&quot;R1 = 40&nbsp;Ω … R2 = 60&nbsp;Ω&quot;", r"$R_1=40\ \Omega$; $R_2=60\ \Omega$", r"Điện trở tương đương của đoạn song song tính thế nào? Nhớ lật ngược."),
  (r"&quot;Vôn kế mắc giữa A và B chỉ 12&nbsp;V&quot;", r"$U_{AB}=12\ \text{V}$", r"Mỗi nhánh nhận hiệu điện thế bao nhiêu?"),
  (r"&quot;Coi nguồn điện lí tưởng, điện trở của dây nối và ampe kế không đáng kể&quot;", r"Chỉ tính hai điện trở", r"⚠ Điều kiện để $U$ hai nhánh bằng $U_{AB}$"),
  (r"&quot;cường độ dòng điện qua mỗi điện trở&quot;", r"Cần $I_1$, $I_2$", r"$I=\dfrac{U}{R}$ cho từng nhánh"),
  (r"&quot;Ampe kế ở mạch chính chỉ bao nhiêu?&quot;", r"Cần $I$", r"$I=I_1+I_2$")],
 [(r"&quot;R2 = 15&nbsp;Ω song song R3 = 30&nbsp;Ω (giữa hai điểm M, N)&quot;", r"$R_2=15\ \Omega$; $R_3=30\ \Omega$", r"⚠ Hai điện trở có chung hai đầu $M$, $N$ mới là song song: gộp cụm này trước"),
  (r"&quot;R1 = 5&nbsp;Ω mắc nối tiếp với cụm&quot;", r"$R_1=5\ \Omega$", r"Sau khi gộp, $R_1$ và cụm mắc thế nào?"),
  (r"&quot;hai cực nguồn là 18&nbsp;V&quot;", r"$U=18\ \text{V}$", r"Nguồn lí tưởng: $U$ đặt vào cả mạch"),
  (r"&quot;Ampe kế ở mạch chính chỉ bao nhiêu?&quot;", r"Cần $I$", r"$I=\dfrac{U}{R_{td}}$"),
  (r"&quot;Vôn kế mắc giữa M và N chỉ bao nhiêu?&quot;", r"Cần $U_{MN}$", r"$U_{MN}=I\cdot R_{23}$"),
  (r"&quot;cường độ dòng điện qua R3&quot;", r"Cần $I_3$", r"Hiệu điện thế nào đặt lên $R_3$? Rồi $I=\dfrac{U}{R}$")],
 [(r"&quot;sáng bình thường khi hiệu điện thế giữa hai đầu đèn là 6&nbsp;V; khi đó điện trở của đèn là 12&nbsp;Ω&quot;", r"$U_đ=6\ \text{V}$; $R_đ=12\ \Omega$", r"Định luật Ohm cho đèn: dòng cần có qua đèn"),
  (r"&quot;Chỉ có nguồn 9&nbsp;V&quot;", r"$U=9\ \text{V}$", r"Nguồn lớn hơn $U_đ$: phần dư phải đặt lên đâu?"),
  (r"&quot;Coi nguồn lí tưởng, điện trở của đèn không đổi&quot;", r"$R_đ$ giữ nguyên", r"⚠ Điều kiện để dùng một giá trị $R_đ$ cho mọi cách mắc"),
  (r"&quot;mắc nối tiếp với đèn một điện trở R<sub>x</sub>&quot;", r"Cần $R_x$", r"Nối tiếp: $I$ chung, $R_{td}=R_đ+R_x$"),
  (r"&quot;R<sub>x</sub> song song với đèn rồi nối thẳng vào nguồn 9&nbsp;V&quot;", r"Cần $I_đ'$", r"⚠ Song song với nhau và nối thẳng vào nguồn: đèn nhận hiệu điện thế nào?"),
  (r"&quot;Đèn sẽ thế nào?&quot;", r"So dòng với mức bình thường", r"Độ sáng do dòng qua đèn quyết định.")],
]

# ───────────── Lời giải ─────────────
NT = [r"<strong>Khái niệm:</strong> đoạn mạch nối tiếp chỉ có một đường đi của dòng điện.",
      r"<strong>Tính chất:</strong> $I=I_1=I_2$.", r"$U=U_1+U_2$.",
      r"Công thức: $R_{td}=R_1+R_2$.", r"Định luật Ohm: $I=\dfrac{U}{R}$.",
      r"⚠ <strong>Điều kiện:</strong> bỏ qua điện trở dây nối, ampe kế; vôn kế điện trở rất lớn."]
SS = [r"<strong>Khái niệm:</strong> đoạn mạch song song: các điện trở chung hai đầu $A$, $B$.",
      r"<strong>Tính chất:</strong> $U=U_1=U_2$.", r"$I=I_1+I_2$.",
      r"Công thức: $\dfrac{1}{R_{td}}=\dfrac{1}{R_1}+\dfrac{1}{R_2}$, hai điện trở: $R_{td}=\dfrac{R_1R_2}{R_1+R_2}$.",
      r"⚠ <strong>Điều kiện:</strong> bỏ qua điện trở dây nối, ampe kế; vôn kế điện trở rất lớn."]
SOLS = [
 sol(NT, [
  ("Điện trở tương đương", [M(r"R_{td}=R_1+R_2"), M(r"R_{td}=15+25"), A(r"R_{td}=40\ \Omega")]),
  ("Số chỉ ampe kế", [P("Nối tiếp nên ampe kế đo dòng chung:"), M(r"I=\dfrac{U_{AB}}{R_{td}}=\dfrac{12}{40}"), A(r"I=0{,}3\ \text{A}")]),
  ("Hiệu điện thế trên $R_1$", [M(r"U_1=I\cdot R_1=0{,}3\cdot15"), A(r"U_1=4{,}5\ \text{V}")]),
  ("Hiệu điện thế trên $R_2$", [M(r"U_2=I\cdot R_2=0{,}3\cdot25"), A(r"U_2=7{,}5\ \text{V}")]),
  ("Kiểm tra", [M(r"U_1+U_2=4{,}5+7{,}5=12\ \text{V}=U_{AB}\ ✓"), P("$R_2$ lớn hơn nhận hiệu điện thế lớn hơn: hợp lí.")])],
  [r"a) $R_{td}=40\ \Omega$", r"b) $I=0{,}3\ \text{A}$", r"c) $U_1=4{,}5\ \text{V}$", r"$U_2=7{,}5\ \text{V}$"],
  "Nhận dạng: đề cho <strong>mắc nối tiếp</strong> và $U$ cả đoạn → cộng $R$, tính $I$ chung, rồi $U=IR$ từng cái."),
 sol(SS, [
  ("Điện trở tương đương", [P("Tích chia tổng:"), M(r"R_{td}=\dfrac{R_1R_2}{R_1+R_2}=\dfrac{40\cdot60}{40+60}"), A(r"R_{td}=24\ \Omega")]),
  ("Dòng qua $R_1$", [P("Mỗi nhánh nhận đủ $U_{AB}=12$ V:"), M(r"I_1=\dfrac{U_{AB}}{R_1}=\dfrac{12}{40}"), A(r"I_1=0{,}3\ \text{A}")]),
  ("Dòng qua $R_2$", [M(r"I_2=\dfrac{U_{AB}}{R_2}=\dfrac{12}{60}"), A(r"I_2=0{,}2\ \text{A}")]),
  ("Số chỉ ampe kế mạch chính", [M(r"I=I_1+I_2=0{,}3+0{,}2"), A(r"I=0{,}5\ \text{A}")]),
  ("Kiểm tra", [M(r"\dfrac{U_{AB}}{R_{td}}=\dfrac{12}{24}=0{,}5\ \text{A}\ ✓"), P("$R_{td}=24\\ \\Omega$ nhỏ hơn cả $40\\ \\Omega$ và $60\\ \\Omega$: hợp lí.")])],
  [r"a) $R_{td}=24\ \Omega$", r"b) $I_1=0{,}3\ \text{A}$", r"$I_2=0{,}2\ \text{A}$", r"c) $I=0{,}5\ \text{A}$"],
  "Nhận dạng: đề cho <strong>mắc song song</strong> → mỗi nhánh nhận đủ $U$; $I$ mạch chính bằng tổng các nhánh."),
 sol([r"<strong>Khái niệm:</strong> mạch hỗn hợp: gộp từng cụm, cụm nằm giữa hai điểm chung gộp trước.",
      r"Song song: $R_{23}=\dfrac{R_2R_3}{R_2+R_3}$.", r"Trong cụm song song: $U_2=U_3$.",
      r"Nối tiếp: $R_{td}=R_1+R_{23}$, dòng qua $R_1$ bằng dòng qua cụm.",
      r"Định luật Ohm: $I=\dfrac{U}{R}$, $U=IR$.",
      r"⚠ <strong>Điều kiện:</strong> nguồn lí tưởng, bỏ qua điện trở dây nối, ampe kế."], [
  ("Gộp cụm song song", [M(r"R_{23}=\dfrac{R_2R_3}{R_2+R_3}=\dfrac{15\cdot30}{15+30}"), A(r"R_{23}=10\ \Omega")]),
  ("Điện trở tương đương", [M(r"R_{td}=R_1+R_{23}=5+10"), A(r"R_{td}=15\ \Omega")]),
  ("Số chỉ ampe kế", [M(r"I=\dfrac{U}{R_{td}}=\dfrac{18}{15}"), A(r"I=1{,}2\ \text{A}")]),
  ("Số chỉ vôn kế", [P("Dòng $I$ qua cả cụm $MN$:"), M(r"U_{MN}=I\cdot R_{23}=1{,}2\cdot10"), A(r"U_{MN}=12\ \text{V}")]),
  ("Dòng qua $R_3$", [P("$R_3$ nhận đúng $U_{MN}$:"), M(r"I_3=\dfrac{U_{MN}}{R_3}=\dfrac{12}{30}"), A(r"I_3=0{,}4\ \text{A}")]),
  ("Kiểm tra", [M(r"I_2=\dfrac{12}{15}=0{,}8\ \text{A}"), M(r"I_2+I_3=0{,}8+0{,}4=1{,}2\ \text{A}=I\ ✓"), M(r"U_1=1{,}2\cdot5=6\ \text{V}"), M(r"U_1+U_{MN}=6+12=18\ \text{V}\ ✓")])],
  [r"a) $R_{td}=15\ \Omega$", r"b) $I=1{,}2\ \text{A}$", r"c) $U_{MN}=12\ \text{V}$", r"d) $I_3=0{,}4\ \text{A}$"],
  "Nhận dạng: thấy <strong>cụm hai điện trở chung hai đầu</strong> nằm nối tiếp với điện trở khác → gộp cụm, cộng nối tiếp, rồi tính ngược."),
 sol([r"Định luật Ohm: $I=\dfrac{U}{R}$.",
      r"Nối tiếp: $I$ chung.", r"$R_{td}=R_đ+R_x$.",
      r"Song song: các nhánh cùng hiệu điện thế.",
      r"Đèn sáng bình thường khi đúng $U_đ$ (và đúng $I_đ$) ghi trong đề.",
      r"⚠ <strong>Điều kiện:</strong> nguồn lí tưởng, điện trở đèn coi như không đổi."], [
  ("Dòng qua đèn khi sáng bình thường", [M(r"I_đ=\dfrac{U_đ}{R_đ}=\dfrac{6}{12}"), A(r"I_đ=0{,}5\ \text{A}")]),
  ("Điện trở tương đương cần có", [P("Nối tiếp nên dòng cả mạch cũng phải bằng $I_đ$:"), M(r"R_{td}=\dfrac{U}{I_đ}=\dfrac{9}{0{,}5}"), A(r"R_{td}=18\ \Omega")]),
  ("Điện trở cần mắc thêm", [M(r"R_x=R_{td}-R_đ=18-12"), A(r"R_x=6\ \Omega")]),
  ("Dòng qua đèn khi mắc nhầm", [P("Đèn song song với $R_x$ và nối thẳng vào nguồn: đèn nhận đủ $9$ V."), M(r"I_đ'=\dfrac{U}{R_đ}=\dfrac{9}{12}"), A(r"I_đ'=0{,}75\ \text{A}")]),
  ("Đèn thế nào", [A("T:Dòng lớn hơn $0{,}5$ A: đèn sáng quá mức bình thường, có thể hỏng.")]),
  ("Kiểm tra", [P("Câu b: hiệu điện thế trên $R_x$:"), M(r"U_x=0{,}5\cdot6=3\ \text{V}"), M(r"U_đ+U_x=6+3=9\ \text{V}\ ✓"), P("Mắc nối tiếp thì $R_x$ \"gánh\" phần $3$ V dư: hợp lí.")])],
  [r"a) $I_đ=0{,}5\ \text{A}$", r"b) $R_x=6\ \Omega$", r"c) $I_đ'=0{,}75\ \text{A}$", r"Đèn sáng quá mức, có thể hỏng"],
  "Nhận dạng: <strong>nguồn lớn hơn hiệu điện thế đèn cần</strong> → mắc thêm điện trở nối tiếp để nó nhận phần hiệu điện thế dư."),
]

# ───────────── Tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>mắc nối tiếp</b> và $U$ của cả đoạn → cộng điện trở, tìm $I$ chung, rồi $U=IR$ từng cái.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điện trở tương đương", "Điện trở tương đương của đoạn mạch bằng bao nhiêu?", 40, "Ω", 0.3,
       loi=r"Hay dùng nhầm công thức tích chia tổng của mạch song song. Nối tiếp thì điện trở cộng lại."),
  buoc("Số chỉ ampe kế", "Ampe kế chỉ bao nhiêu ampe?", 0.3, "A", 0.01,
       loi=r"Hay chia $U_{AB}$ cho một điện trở. Ampe kế đo dòng chung, phải chia cho điện trở của cả đoạn.",
       ke=[(r"$I=\dfrac{U_{AB}}{R_{td}}$", True),
           (r"$I=\dfrac{U_{AB}}{R_1}$", r"$U_{AB}$ đặt lên cả hai điện trở, không riêng $R_1$."),
           (r"$I=U_{AB}\cdot R_{td}$", r"Định luật Ohm là chia, không nhân; nhân thì sai cả đơn vị.")]),
  buoc("Hiệu điện thế trên $R_1$", "Hiệu điện thế giữa hai đầu $R_1$ bằng bao nhiêu?", 4.5, "V", 0.05,
       loi=r"Hay chia đôi $U_{AB}$ cho hai điện trở. Hai điện trở khác nhau nhận hiệu điện thế khác nhau.",
       ke=[(r"$U_1=I\cdot R_1$ với $I$ vừa tìm", True),
           (r"$U_1=\dfrac{U_{AB}}{2}$", r"Chỉ đúng khi $R_1=R_2$; ở đây hai điện trở khác nhau."),
           (r"$U_1=U_{AB}$ vì nối tiếp", r"Nối tiếp thì $I$ như nhau, còn $U$ chia ra cho từng điện trở.")]),
  buoc("Hiệu điện thế trên $R_2$", "Hiệu điện thế giữa hai đầu $R_2$ bằng bao nhiêu?", 7.5, "V", 0.05,
       loi=r"Hay lấy lại dòng khác cho $R_2$. Nối tiếp thì $R_2$ có cùng dòng với $R_1$.",
       ke=[(r"$U_2=I\cdot R_2$ hoặc $U_2=U_{AB}-U_1$", True),
           (r"$U_2=U_1$ vì cùng dòng điện", r"Cùng $I$ nhưng khác $R$ thì $U=IR$ khác nhau."),
           (r"$U_2=U_{AB}+U_1$", r"Nối tiếp: $U_{AB}=U_1+U_2$, nên phần còn lại là hiệu, không phải tổng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>mắc song song</b> → mỗi nhánh nhận đủ $U$; dòng mạch chính = tổng các nhánh.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Điện trở tương đương", "Điện trở tương đương của đoạn mạch bằng bao nhiêu?", 24, "Ω", 0.3,
       loi=r"Hay cộng hai điện trở như nối tiếp, hoặc tính $\dfrac{1}{R_1}+\dfrac{1}{R_2}$ rồi quên lật ngược. Song song thì $R_{td}$ nhỏ hơn mỗi điện trở."),
  buoc("Dòng qua $R_1$", "Cường độ dòng điện qua $R_1$ bằng bao nhiêu?", 0.3, "A", 0.01,
       loi=r"Hay chia đôi $U_{AB}$ cho hai nhánh. Song song thì mỗi nhánh nhận đủ $U_{AB}$.",
       ke=[(r"$I_1=\dfrac{U_{AB}}{R_1}$", True),
           (r"$I_1=\dfrac{U_{AB}/2}{R_1}$", r"Song song không chia hiệu điện thế: mỗi nhánh nhận đủ $U_{AB}$."),
           (r"$I_1=\dfrac{U_{AB}}{R_1+R_2}$", r"Đó là cách tính của mạch nối tiếp, ở đây hai điện trở song song.")]),
  buoc("Dòng qua $R_2$", "Cường độ dòng điện qua $R_2$ bằng bao nhiêu?", 0.2, "A", 0.01,
       loi=r"Hay cho rằng dòng hai nhánh bằng nhau. Nhánh điện trở lớn hơn có dòng nhỏ hơn.",
       ke=[(r"$I_2=\dfrac{U_{AB}}{R_2}$", True),
           (r"$I_2=I_1$ vì song song", r"Song song thì $U$ bằng nhau, còn $I$ phụ thuộc điện trở từng nhánh."),
           (r"$I_2=I_1\cdot\dfrac{R_2}{R_1}$", r"Tỉ số bị lật: nhánh điện trở lớn hơn phải có dòng nhỏ hơn.")]),
  buoc("Số chỉ ampe kế mạch chính", "Ampe kế ở mạch chính chỉ bao nhiêu ampe?", 0.5, "A", 0.01,
       loi=r"Hay lấy dòng của một nhánh làm dòng mạch chính. Dòng tới $A$ rẽ ra hai nhánh nên mạch chính là tổng.",
       ke=[(r"$I=I_1+I_2$", True),
           (r"$I=I_1$ vì nối tiếp với ampe kế", r"Ampe kế ở mạch chính đo dòng trước khi rẽ nhánh, gồm cả hai nhánh."),
           (r"$I=\dfrac{U_{AB}}{R_1+R_2}$", r"Cộng điện trở là của mạch nối tiếp; song song phải dùng $R_{td}$ tích chia tổng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hai điện trở chung hai đầu</b> nối tiếp với điện trở khác → gộp cụm trước, rồi tính ngược.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Gộp cụm song song", "Điện trở của cụm $R_2$ song song $R_3$ bằng bao nhiêu?", 10, "Ω", 0.1,
       loi=r"Hay cộng $R_2+R_3$. Hai điện trở chung hai đầu $M$, $N$ là song song: tích chia tổng."),
  buoc("Điện trở tương đương", "Điện trở tương đương của cả mạch bằng bao nhiêu?", 15, "Ω", 0.1,
       loi=r"Hay gộp $R_1$ với $R_2$ trước. $R_1$ không chung hai đầu với $R_2$, nên không gộp với riêng $R_2$ được.",
       ke=[(r"Cộng $R_1$ với điện trở của cụm", True),
           (r"Cộng cả ba điện trở", r"$R_2$, $R_3$ song song, không nối tiếp với nhau."),
           (r"Gộp $R_1$ với $R_2$ trước, rồi song song với $R_3$", r"$R_1$ nằm ngoài cụm $MN$, nối tiếp với cả cụm chứ không với riêng $R_2$.")]),
  buoc("Số chỉ ampe kế", "Ampe kế ở mạch chính chỉ bao nhiêu ampe?", 1.2, "A", 0.02,
       loi=r"Hay chia $U$ nguồn cho $R_1$ hoặc cho điện trở cụm. Dòng mạch chính đi qua cả mạch: chia cho $R_{td}$.",
       ke=[(r"$I=\dfrac{U}{R_{td}}$", True),
           (r"$I=\dfrac{U}{R_1}$", r"$U$ nguồn đặt lên cả mạch, không riêng $R_1$."),
           (r"$I=\dfrac{U}{R_2}+\dfrac{U}{R_3}$", r"Làm vậy là coi $R_2$, $R_3$ nhận đủ $U$ nguồn, quên phần hiệu điện thế trên $R_1$.")]),
  buoc("Số chỉ vôn kế", "Vôn kế giữa $M$ và $N$ chỉ bao nhiêu vôn?", 12, "V", 0.1,
       loi=r"Hay lấy luôn $U$ nguồn cho cụm $MN$. Một phần hiệu điện thế đã đặt lên $R_1$.",
       ke=[(r"$U_{MN}=I\cdot R_{23}$", True),
           (r"$U_{MN}=U$ của nguồn", r"$R_1$ nối tiếp với cụm nên cũng nhận một phần hiệu điện thế."),
           (r"$U_{MN}=I\cdot R_2$", r"Dòng $I$ mạch chính không chạy hết qua $R_2$; với cả cụm phải dùng $R_{23}$.")]),
  buoc("Dòng qua $R_3$", "Cường độ dòng điện qua $R_3$ bằng bao nhiêu?", 0.4, "A", 0.01,
       loi=r"Hay chia đôi dòng mạch chính cho hai nhánh. Hai nhánh khác điện trở thì không chia đều.",
       ke=[(r"$I_3=\dfrac{U_{MN}}{R_3}$", True),
           (r"$I_3=\dfrac{I}{2}$", r"Chỉ đúng khi $R_2=R_3$; ở đây hai nhánh khác nhau."),
           (r"$I_3=\dfrac{U}{R_3}$ với $U$ của nguồn", r"$R_3$ chỉ nhận $U_{MN}$, không nhận cả $U$ nguồn.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>nguồn lớn hơn hiệu điện thế đèn cần</b> → mắc thêm điện trở <b>nối tiếp</b> để nhận phần dư.",
  cap_do=4, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Dòng qua đèn khi sáng bình thường", "Khi đèn sáng bình thường, dòng qua đèn bằng bao nhiêu?", 0.5, "A", 0.01,
       loi=r"Hay chia hiệu điện thế nguồn cho điện trở đèn. Đèn sáng bình thường khi chính nó nhận đúng hiệu điện thế ghi trong đề."),
  buoc("Điện trở tương đương cần có", "Điện trở tương đương của cả mạch phải bằng bao nhiêu?", 18, "Ω", 0.2,
       loi=r"Hay chia hiệu điện thế của đèn cho dòng. Cả mạch nhận hiệu điện thế của nguồn.",
       ke=[(r"$R_{td}=\dfrac{U_{nguồn}}{I_đ}$ vì nối tiếp có dòng chung", True),
           (r"$R_{td}=\dfrac{U_đ}{I_đ}$", r"Đó lại chính là điện trở của đèn; cả mạch nhận $U$ nguồn."),
           (r"$R_{td}=U_{nguồn}\cdot I_đ$", r"Định luật Ohm cho $R=\dfrac{U}{I}$, không phải tích.")]),
  buoc("Điện trở cần mắc thêm", "Điện trở $R_x$ phải bằng bao nhiêu?", 6, "Ω", 0.1,
       loi=r"Hay lấy luôn điện trở tương đương làm $R_x$, quên rằng đèn cũng là một phần của mạch nối tiếp.",
       ke=[(r"$R_x=R_{td}-R_đ$", True),
           (r"$R_x=R_{td}$", r"$R_{td}$ gồm cả đèn và $R_x$; phải trừ điện trở của đèn."),
           (r"$R_x=R_{td}+R_đ$", r"Nối tiếp thì $R_{td}=R_đ+R_x$, nên $R_x$ là hiệu, không phải tổng.")]),
  buoc("Dòng qua đèn khi mắc nhầm", "Khi mắc nhầm, dòng qua đèn bằng bao nhiêu?", 0.75, "A", 0.01,
       loi=r"Hay tưởng $R_x$ vẫn làm giảm dòng qua đèn. Mắc song song thì $R_x$ là một nhánh khác, đèn vẫn nhận đủ hiệu điện thế nguồn.",
       ke=[(r"Đèn nhận đủ $U$ nguồn: $I_đ'=\dfrac{U}{R_đ}$", True),
           (r"Tính $R_{td}$ của đèn song song $R_x$ rồi lấy $\dfrac{U}{R_{td}}$ làm dòng qua đèn", r"Đó là dòng mạch chính, gồm cả nhánh $R_x$, không phải dòng qua đèn."),
           (r"Dòng qua đèn vẫn như câu a vì vẫn có $R_x$", r"Song song không chia hiệu điện thế; $R_x$ không còn gánh phần dư cho đèn.")]),
  buoc("Đèn thế nào", "Khi mắc nhầm, đèn sẽ thế nào?",
       loi=r"Hay nghĩ thêm điện trở thì đèn yếu đi. Ở đây đèn nhận hiệu điện thế lớn hơn mức cần.",
       lua_chon=[(r"Sáng quá mức bình thường, có thể hỏng", True),
                 (r"Sáng yếu hơn bình thường", r"Đèn nhận hiệu điện thế lớn hơn $6$ V nên dòng qua đèn lớn hơn khi sáng bình thường."),
                 (r"Sáng bình thường", r"Đèn chỉ sáng bình thường khi nhận đúng $6$ V; ở đây nó nhận nhiều hơn.")],
       ke=[(r"So dòng qua đèn với dòng khi đèn sáng bình thường", True),
           (r"So điện trở của đèn với $R_x$", r"Độ sáng do dòng qua đèn quyết định, so điện trở không trả lời được."),
           (r"So dòng mạch chính với dòng qua $R_x$", r"Hai dòng này không nói gì về dòng qua đèn.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Ghi JSON ─────────────
d = {"lesson_id": 90, "lesson_title": "Bài 12. Đoạn mạch nối tiếp, song song", "generated_at": "2026-10-12",
     "review": {"checked": False, "notes": "Soạn 12/10/2026 (chặng 3). Kiểm chéo kiem-code vòng 1: 0 lỗi chặn, đã sửa các mục nên-sửa (đổi số dạng 3, tách dòng). Chờ thầy duyệt; chưa đếm ngân hàng topic 91/92."},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DE]}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
assert all(len(s["buoc"]) == SOLS[i].count('class="bt-step"') for i, s in enumerate(STEPS))
inject(J, BUILD, ANALYSIS, SOLS, STEPS)

raw = open(J, encoding="utf8").read()
assert not re.search(r"\\u000[0-8bcef]|\\t", raw.replace("\\\\t", "")), "ký tự điều khiển trong JSON"
assert "marker-end" not in raw
for q in json.load(open(J))["dang_bai"]:
    for f in ("problem_html", "analysis_html", "solution_html"):
        h_ = re.sub(r"<svg.*?</svg>", "", q[f], flags=re.S)
        ms = re.findall(r"\$\$(.+?)\$\$", h_, flags=re.S)
        ms += re.findall(r"\$([^$]+)\$", re.sub(r"\$\$.+?\$\$", "", h_, flags=re.S))
        for m in ms:
            assert "<" not in m and ">" not in m, (f, m)
    for fm in re.findall(r"<figure.*?</figure>", q["problem_html"] + q["analysis_html"], flags=re.S):
        assert len(fm.encode()) < 6200, (q["label"], len(fm.encode()))
print("xong 90.json")
