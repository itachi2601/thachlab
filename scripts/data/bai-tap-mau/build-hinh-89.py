"""Bài tập mẫu bài 89 — Bài 11. Điện trở. Định luật Ohm (KHTN 9). Dựng 4 dạng + hình + lời giải + buoc[] → 89.json.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-89.py   (idempotent: ghi lại toàn bộ 89.json, review.checked=false)
Danh sách dạng: scripts/data/bai-tap-mau/89.dang.md. Mọi số liệu tính ở đầu file, có assert."""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "89.json")
T1 = "Định luật Ohm cho một điện trở"
T2 = "Điện trở phụ thuộc kích thước và vật liệu dây dẫn"

# ───────────── Số liệu (tính + kiểm) ─────────────
# Dạng 1: U = 6,0 V, I = 240 mA; rồi U' = 9,0 V
U1, I1mA, U1b = 6.0, 240, 9.0
I1 = I1mA / 1000
R1 = U1 / I1
I1b = U1b / R1
assert abs(I1 - 0.24) < 1e-12 and abs(R1 - 25) < 1e-9 and abs(I1b - 0.36) < 1e-9
# cách sai cho số khác đáp án
assert abs(U1 / I1mA - R1) > 1 and abs(U1 * I1 - R1) > 1          # quên đổi mA (0,025) · nhân U·I (1,44)
assert abs(I1 * U1 / U1b * 1000 - 360) > 50                        # đảo tỉ số (160 mA)
assert abs(I1 * U1b / U1 * 1000 - 360) < 1e-6                      # kiểm tra bằng tỉ lệ

# Dạng 2: đồ thị I–U, R_a = 15 Ω (đường 1), R_b = 40 Ω (đường 2); U ≤ 12 V; hỏi U để I_b = 0,5 A
Ra, Rb, Imax_b = 15.0, 40.0, 0.5
pa, pb = (6, 6 / Ra), (8, 8 / Rb)                                  # điểm đọc ở giao lưới
assert abs(pa[1] - 0.4) < 1e-12 and abs(pb[1] - 0.2) < 1e-12
assert abs(12 / Ra - 0.8) < 1e-12 and abs(12 / Rb - 0.3) < 1e-12
U2c = Imax_b * Rb
assert abs(U2c - 20) < 1e-9
assert abs(pb[1] / pb[0] - Rb) > 1 and abs(Imax_b / Rb - U2c) > 1 and abs(Rb / Imax_b - U2c) > 1   # I/U · I/R · R/I

# Dạng 3: hai dây constantan; dây 1: 2 m, 0,4 mm², 2,5 Ω; dây 2: 6 m, 0,5 mm²; U = 4,5 V
RHO_C = 0.5e-6
l31, S31, R31 = 2.0, 0.4, 2.5
l32, S32, U3 = 6.0, 0.5, 4.5
assert abs(RHO_C * l31 / (S31 * 1e-6) - R31) < 1e-9                 # khớp bảng ρ của bài
R3a = R31 * l32 / l31                                              # chỉ đổi chiều dài
R32 = R3a * S31 / S32
I3 = U3 / R32
assert abs(R3a - 7.5) < 1e-9 and abs(R32 - 6) < 1e-9 and abs(I3 - 0.75) < 1e-9
assert abs(RHO_C * l32 / (S32 * 1e-6) - R32) < 1e-9
assert abs(R3a * S32 / S31 - R32) > 1 and abs(R3a - R32) > 1        # nhân ngược tỉ số tiết diện (9,375) · bỏ tiết diện (7,5)
assert abs(U3 / R31 - I3) > 0.5 and abs(U3 * R32 - I3) > 1           # dùng R dây 1 (1,8 A) · nhân (27)

# Dạng 4: dây 20 m, 0,5 mm²; U = 11 V; I = 250 mA → R, ρ, vật liệu (nichrome); gập đôi → R', I'
# (khác quiz Câu 7 của lý thuyết: constantan 4 m, 0,5 mm², 12 V)
l4, S4, U4, I4mA = 20.0, 0.5, 11.0, 250
I4 = I4mA / 1000
R4 = U4 / I4
rho4 = R4 * S4 * 1e-6 / l4
R4g = R4 / 4                                                       # dây hai sợi chập nhau: dài ½, hai sợi cùng dẫn
I4g = U4 / R4g
assert abs(R4 - 44) < 1e-9 and abs(rho4 - 1.1e-6) < 1e-15 and abs(R4g - 11) < 1e-9 and abs(I4g - 1.0) < 1e-9
assert abs(rho4 * (l4 / 2) / (2 * S4 * 1e-6) - R4g) < 1e-9
RHO = {"đồng": 1.7e-8, "constantan": 0.5e-6, "nichrome": 1.1e-6}
best = min(RHO, key=lambda k: abs(math.log(RHO[k] / rho4)))
assert best == "nichrome"
R_dong = RHO["đồng"] * l4 / (S4 * 1e-6); R_cons = RHO["constantan"] * l4 / (S4 * 1e-6)
assert abs(R_dong - 0.68) < 1e-9 and abs(R_cons - 20) < 1e-9          # vi_sao: ~0,7 Ω và 20 Ω so với 44 Ω
assert abs(R4 * S4 / l4 - rho4) > 1e-3                              # quên đổi mm²
assert abs(U4 / (R4 / 2) - I4g) > 0.3 and abs(I4 / 4 - I4g) > 0.5 and abs(I4 * 2 - I4g) > 0.3   # R/2 (0,5 A) · I/4 · 2I
assert abs(I4 * 4 - I4g) < 1e-9

# ───────────── Hình ─────────────
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'

def path_pts(corners, n):
    """n điểm cách đều theo chiều dài trên đường gấp khúc kín `corners`."""
    segs = list(zip(corners, corners[1:] + corners[:1]))
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
    tot = sum(lens); out = []
    for k in range(n):
        s = tot * k / n
        for (a, b), L in zip(segs, lens):
            if s <= L:
                out.append((a[0] + (b[0] - a[0]) * s / L, a[1] + (b[1] - a[1]) * s / L)); break
            s -= L
    return out

def flow(corners, ndots=6, dur=6.0):
    """Chấm chạy theo chiều dòng điện quy ước, MỘT vòng khi bấm (begin=indefinite, fill=freeze).
    Chỉ ghi các góc của mạch + keyTimes theo chiều dài (đúng tốc độ đều, hình nhỏ ~5 KB)."""
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

# Sơ đồ mạch chung: nguồn (dây dưới), khoá K (trái), ampe kế (trên), R (phải), vôn kế song song với R
X0, X1, Y0, Y1 = 40, 250, 70, 240
PX, NX = 140, 154            # bản + (dài) và − (ngắn, đậm) của nguồn
AX, RA = 145, 20
RT, RB = 125, 185
J1, J2 = 100, 215
VX, VY = 360, 157
KT, KB = 140, 180

def circuit(p, a_txt, v_txt, r_txt, anim, r_name="R"):
    W = 2.4
    b = poly([(PX, Y1), (X0, Y1), (X0, KB)], "currentColor", W)
    b += poly([(X0, KT), (X0, Y0), (AX - RA, Y0)], "currentColor", W)
    b += poly([(AX + RA, Y0), (X1, Y0), (X1, RT)], "currentColor", W)
    b += poly([(X1, RB), (X1, Y1), (NX, Y1)], "currentColor", W)
    b += dot(X0, KT, 4) + dot(X0, KB, 4) + seg(X0, KB, X0, KT, "currentColor", 3) + lbl(X0 + 12, (KT + KB) / 2 + 6, "K", "currentColor", 16, "start", "700")
    b += seg(PX, Y1 - 18, PX, Y1 + 18, "currentColor", 2.4) + seg(NX, Y1 - 9, NX, Y1 + 9, "currentColor", 5)
    b += lbl(PX - 6, Y1 - 22, "+", "currentColor", 18, "end", "700") + lbl(NX + 6, Y1 - 22, "−", "currentColor", 18, "start", "700")
    b += f'<circle cx="{AX}" cy="{Y0}" r="{RA}" fill="none" stroke="currentColor" stroke-width="2.4"/>' + lbl(AX, Y0 + 7, "A", "currentColor", 19, "middle", "700")
    b += lbl(AX - RA - 3, Y0 - 8, "+", "currentColor", 16, "end", "700") + lbl(AX + RA + 3, Y0 - 8, "−", "currentColor", 16, "start", "700")
    b += f'<rect x="{X1 - 11}" y="{RT}" width="22" height="{RB - RT}" fill="rgba(251,146,60,.2)" stroke="currentColor" stroke-width="2.4"/>'
    b += lbl(X1 - 18, (RT + RB) / 2 + 6, it_(r_name), "currentColor", 19, "end", "700")
    b += dot(X1, J1, 3.5) + dot(X1, J2, 3.5)
    b += poly([(X1, J1), (VX, J1), (VX, VY - RA)], "currentColor", W) + poly([(VX, VY + RA), (VX, J2), (X1, J2)], "currentColor", W)
    b += f'<circle cx="{VX}" cy="{VY}" r="{RA}" fill="none" stroke="currentColor" stroke-width="2.4"/>' + lbl(VX, VY + 7, "V", "currentColor", 19, "middle", "700")
    b += lbl(VX + RA + 3, VY - RA + 4, "+", "currentColor", 16, "start", "700") + lbl(VX + RA + 3, VY + RA + 6, "−", "currentColor", 16, "start", "700")
    # chiều dòng điện quy ước (đỏ): từ + sang trái → lên → phải → xuống qua R → trái về −
    b += chevron(95, Y1, -1, 0, RED, 2.6, 12) + chevron(X0, 105, 0, -1, RED, 2.6, 12) + chevron(205, Y0, 1, 0, RED, 2.6, 12)
    b += chevron(X1, 207, 0, 1, RED, 2.6, 12) + chevron(205, Y1, -1, 0, RED, 2.6, 12)
    # số chỉ / dữ kiện
    b += lbl(AX, Y0 - 30, a_txt, BLUE, 16, "middle", "700")
    b += lbl(VX, J2 + 26, v_txt, BLUE, 16, "middle", "700")
    b += lbl(X1 + 16, J1 + 50, r_txt, ORG, 16, "start", "700")
    if anim:
        b += flow([(PX, Y1), (X0, Y1), (X0, Y0), (X1, Y0), (X1, Y1), (NX, Y1)])
    assert PX < NX and 95 < PX and 205 > NX       # mũi tên dây dưới: bên trái chỉ ra xa (+), bên phải chỉ về (−)
    return b

VBC = "0 0 420 262"
CAP_FLOW = "Chấm cam chạy theo chiều dòng điện quy ước: từ cực (+), qua ampe kế, qua điện trở, về cực (−).<br>Tốc độ chấm chỉ để minh hoạ, không tỉ lệ với cường độ dòng điện."

def d1(k):
    if k == 0:
        b = circuit("d1", "240 mA", "6,0 V", "R = ?", True)
        return fig("d1-0", VBC, "Mạch điện: nguồn, khoá K, ampe kế chỉ 240 miliampe mắc nối tiếp với điện trở R, vôn kế chỉ 6 vôn mắc song song với R", b,
                   "Mô phỏng (bấm Chạy mô phỏng).<br>" + CAP_FLOW)
    b = circuit("d1a", "I = 240 mA", "U = 6,0 V", "R = ?", False)
    b += lbl(16, 22, "Đổi mA ra A trước khi chia", RED, 15, "start", "700")
    return fig("d1-2", VBC, "Sơ đồ mạch với dữ kiện: số chỉ ampe kế tính bằng miliampe, số chỉ vôn kế tính bằng vôn, điện trở R cần tìm", b,
               "Dữ kiện: ampe kế đo I của R, vôn kế đo U giữa hai đầu R.")

# Đồ thị I–U (dạng 2)
OX, OY, KX, KY = 64, 252, 25.0, 250.0
def gx(u): return OX + KX * u
def gy(i): return OY - KY * i
def graph(p):
    b = seg(OX, OY, 398, OY, "currentColor", 2) + chevron(398, OY, 1, 0, "currentColor", 2, 11)
    b += seg(OX, OY, OX, 30, "currentColor", 2) + chevron(OX, 30, 0, -1, "currentColor", 2, 11)
    b += lbl(398, OY + 44, it_("U") + " (V)", "currentColor", 17, "end", "700") + lbl(OX + 10, 38, it_("I") + " (A)", "currentColor", 17, "start", "700")
    b += lbl(OX - 8, OY + 20, "O", "currentColor", 16, "end", "700")
    for u in range(2, 13, 2):
        b += seg(gx(u), OY, gx(u), OY + 6, "currentColor", 2) + seg(gx(u), OY, gx(u), gy(0.85), "currentColor", 1, "3 5", .3)
        b += lbl(gx(u), OY + 24, str(u), "currentColor", 17, "middle", "600")
    for kk in range(1, 9):
        i = kk / 10
        b += seg(OX - 6, gy(i), OX, gy(i), "currentColor", 2) + seg(OX, gy(i), gx(13), gy(i), "currentColor", 1, "3 5", .3)
        b += lbl(OX - 10, gy(i) + 6, f"0,{kk}", "currentColor", 17, "end", "600")
    b += seg(gx(0), gy(0), gx(12), gy(12 / Ra), RED, 2.8) + seg(gx(0), gy(0), gx(12), gy(12 / Rb), BLUE, 2.8)
    b += lbl(gx(9) - 12, gy(9 / Ra) - 4, "(1)", RED, 17, "end", "700") + lbl(gx(12) - 2, gy(12 / Rb) - 12, "(2)", BLUE, 17, "end", "700")
    assert gy(12 / Ra) >= 40 and gx(12) <= 380
    # các điểm đọc nằm đúng giao lưới
    assert abs(gy(pa[1]) - gy(0.4)) < 1e-9 and abs(gy(pb[1]) - gy(0.2)) < 1e-9
    return b

def d2(k):
    b = graph(f"d2{k}")
    if k == 0:
        n = 41; dur = 5.0
        for R_, c in ((Ra, RED), (Rb, BLUE)):
            xs = [gx(12 * j / (n - 1)) for j in range(n)]; ys = [gy(12 * j / (n - 1) / R_) for j in range(n)]
            b += (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="5.5" fill="{c}" stroke="currentColor" stroke-width="1.2">'
                  f'{smil("cx", xs, dur)}{smil("cy", ys, dur)}</circle>')
        return fig("d2-0", "0 0 420 304", "Đồ thị cường độ dòng điện theo hiệu điện thế của hai điện trở: đường 1 màu đỏ dốc hơn đường 2 màu xanh, cả hai đi qua gốc toạ độ", b,
                   "Mô phỏng: tăng dần U từ 0 đến 12 V, mỗi chấm chạy trên đồ thị của một điện trở (bấm Chạy mô phỏng).<br>Đường (1) màu đỏ, đường (2) màu xanh.")
    for (u, i), c in ((pa, RED),):
        b += seg(gx(u), gy(i), gx(u), OY, c, 1.6, "5 4") + seg(gx(u), gy(i), OX, gy(i), c, 1.6, "5 4")
        b += f'<circle cx="{gx(u):.1f}" cy="{gy(i):.1f}" r="6" fill="none" stroke="{c}" stroke-width="2.4"/>'
    return fig("d2-2", "0 0 420 304", "Gióng mẫu trên đường 1: điểm nằm đúng giao của vạch lưới, gióng xuống trục U và sang trục I; đường 2 để học sinh tự chọn điểm", b,
               "Dữ kiện: gióng mẫu cho đường 1.<br>Đường 2: tự chọn một điểm nằm đúng giao lưới.")

def lsub(x, y, base, idx, rest, c="currentColor", size=18):
    """Nhãn ký hiệu nghiêng có chỉ số dưới bằng tspan (chữ số chỉ số Unicode trông như dấu phẩy cạnh chữ nghiêng)."""
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="700">{it_(base)}'
            f'<tspan dy="4" font-size="{size - 4}">{idx}</tspan><tspan dy="-4">{rest}</tspan></text>')

def wire(x, y, L, th):
    return f'<rect x="{x}" y="{y - th / 2:.1f}" width="{L:.1f}" height="{th:.1f}" rx="2" fill="rgba(251,146,60,.35)" stroke="currentColor" stroke-width="1.6"/>'

def d3(k):
    s = 50.0                                     # px/m (chiều dài đúng tỉ lệ)
    t = 20.0                                     # px bề dày / mm² (minh hoạ tiết diện)
    xa = 40; ya, yb = 70, 172
    b = wire(xa, ya, s * l31, t * S31) + wire(xa, yb, s * l32, t * S32)
    b += lbl(xa, ya - 18, "Dây 1", "currentColor", 16, "start", "700") + lbl(xa, yb - 18, "Dây 2", "currentColor", 16, "start", "700")
    col = 175
    b += lsub(col, ya - 22, "l", "1", " = 2 m")
    b += lsub(col, ya + 4, "S", "1", " = 0,4 mm²")
    b += lsub(col, ya + 30, "R", "1", " = 2,5 Ω", ORG)
    b += lsub(xa, yb + 32, "l", "2", " = 6 m")
    b += lsub(xa + 105, yb + 32, "S", "2", " = 0,5 mm²")
    b += lsub(xa + 262, yb + 32, "R", "2", " = ?", ORG)
    b += lbl(xa, 238, "Cùng làm bằng constantan", BLUE, 15, "start", "700")
    assert xa + s * l32 <= 400
    if k == 0:
        # bóng dây 1 (nét đứt) trượt xuống, kéo dài, rồi to ra → trùng dây 2 (chỉ minh hoạ dữ kiện, không có số R)
        h1, h2 = t * S31, t * S32
        ys = [ya - h1 / 2, yb - h1 / 2, yb - h1 / 2, yb - h2 / 2]
        ws = [s * l31, s * l31, s * l32, s * l32]
        hs = [h1, h1, h1, h2]
        b += (f'<rect x="{xa}" y="{ys[0]:.1f}" width="{ws[0]:.1f}" height="{hs[0]:.1f}" rx="2" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="5 3">'
              f'{smil("y", ys, 4.5)}{smil("width", ws, 4.5)}{smil("height", hs, 4.5)}</rect>')
        return fig("d3-0", "0 0 420 250", "Hai dây constantan: dây 1 ngắn, mảnh hơn; dây 2 dài hơn và to hơn một chút", b,
                   "Mô phỏng (bấm Chạy mô phỏng): bóng nét đứt của dây 1 trượt xuống, kéo dài, rồi to ra thành dây 2.<br>Chiều dài vẽ đúng tỉ lệ.<br>Bề dày nét chỉ minh hoạ tiết diện, không đo trên hình.")
    b += lbl(xa, 266, it_("l") + " đổi bao nhiêu lần?", RED, 15, "start", "700")
    b += lbl(xa, 288, it_("S") + " đổi bao nhiêu lần?", RED, 15, "start", "700")
    return fig("d3-2", "0 0 420 298", "Hai dây cùng vật liệu, so chiều dài và tiết diện của dây 2 với dây 1", b,
               "Dữ kiện: cùng vật liệu nên chỉ cần so chiều dài và tiết diện.")

def d4(k):
    if k == 0:
        b = circuit("d4", "250 mA", "11 V", "R = ?", True, "R")
        return fig("d4-0", VBC, "Mạch điện: nguồn, khoá K, ampe kế chỉ 250 miliampe mắc nối tiếp với cuộn dây, vôn kế chỉ 11 vôn mắc song song với cuộn dây", b,
                   "Mô phỏng (bấm Chạy mô phỏng).<br>" + CAP_FLOW)
    b = lbl(20, 28, "Trước khi gập:", "currentColor", 15, "start", "700")
    b += wire(20, 52, 300, 8) + lbl(330, 57, it_("l") + " = 20 m", "currentColor", 15, "start", "700")
    b += lbl(20, 82, it_("S") + " = 0,5 mm²", "currentColor", 15, "start", "700")
    b += lbl(20, 122, "Gập đôi: dây hai sợi chập nhau", "currentColor", 15, "start", "700")
    b += wire(20, 144, 150, 8) + wire(20, 153, 150, 8)
    b += f'<path d="M170,140 A8.5,8.5 0 0 1 170,157" fill="none" stroke="currentColor" stroke-width="1.6"/>'
    b += lbl(190, 152, it_("l") + "′ = ?", RED, 15, "start", "700")
    b += lbl(20, 184, "hai sợi cùng dẫn điện", RED, 15, "start", "700")
    return fig("d4-2", "0 0 420 200", "Cuộn dây trước khi gập và sau khi gập đôi thành dây hai sợi chập nhau", b,
               "Dữ kiện: dây hai sợi dài một nửa, hai sợi cùng dẫn điện.<br>Hình minh hoạ, không đúng tỉ lệ.")

BUILD = [d1, d2, d3, d4]

# ───────────── Đề ─────────────
DE = [
 dict(label="Dạng 1 · Tính điện trở và cường độ dòng điện bằng định luật Ohm", topic=T1,
      problem_html=r"<p>Mắc một điện trở $R$ vào mạch như hình. Vôn kế chỉ $6{,}0\ \text{V}$, ampe kế chỉ $240\ \text{mA}$. Coi điện trở không đổi khi hiệu điện thế thay đổi.</p>"
                   r"<ol type=\"a\"><li>Tính điện trở $R$.</li><li>Tăng hiệu điện thế giữa hai đầu $R$ lên $9{,}0\ \text{V}$. Khi đó ampe kế chỉ bao nhiêu miliampe?</li></ol>"),
 dict(label="Dạng 2 · Đọc đồ thị I theo U của hai điện trở", topic=T1,
      problem_html=r"<p>Hình dưới là đồ thị cường độ dòng điện $I$ theo hiệu điện thế $U$ của hai điện trở: $R_1$ (đường 1) và $R_2$ (đường 2). Coi $R_2$ không đổi khi $U$ tăng.</p>"
                   r"<ol type=\"a\"><li>Từ đồ thị, tính $R_1$ và $R_2$.</li><li>Điện trở nào cản trở dòng điện nhiều hơn?</li>"
                   r"<li>Phải đặt vào hai đầu $R_2$ hiệu điện thế bao nhiêu để dòng điện qua nó là $0{,}5\ \text{A}$?</li></ol>"),
 dict(label="Dạng 3 · Điện trở thay đổi theo chiều dài và tiết diện", topic=T2,
      problem_html=r"<p>Hai dây dẫn cùng làm bằng constantan.</p>"
                   r"<p>Dây 1 dài $2\ \text{m}$, tiết diện $0{,}4\ \text{mm}^2$, điện trở $2{,}5\ \Omega$.</p>"
                   r"<p>Dây 2 dài $6\ \text{m}$, tiết diện $0{,}5\ \text{mm}^2$.</p>"
                   r"<ol type=\"a\"><li>Không dùng điện trở suất, tính điện trở của dây 2.</li><li>Mắc dây 2 vào hiệu điện thế $4{,}5\ \text{V}$. Tính cường độ dòng điện qua dây.</li></ol>"),
 dict(label="Dạng 4 · Tổng hợp: tìm vật liệu dây, rồi gập đôi dây", topic=T2,
      problem_html=r"<p>Một cuộn dây dẫn dài $20\ \text{m}$, tiết diện $0{,}5\ \text{mm}^2$, mắc vào mạch như hình. Vôn kế chỉ $11\ \text{V}$, ampe kế chỉ $250\ \text{mA}$. Coi nhiệt độ dây không đổi.</p>"
                   r"<p>Điện trở suất ở $20\ ^\circ\text{C}$:</p>"
                   r"<p>đồng: $1{,}7 \cdot 10^{-8}\ \Omega\cdot\text{m}$</p>"
                   r"<p>constantan: $0{,}5 \cdot 10^{-6}\ \Omega\cdot\text{m}$</p>"
                   r"<p>nichrome: $1{,}1 \cdot 10^{-6}\ \Omega\cdot\text{m}$</p>"
                   r"<ol type=\"a\"><li>Tính điện trở của cuộn dây.</li><li>Tính điện trở suất của dây. Dây làm bằng vật liệu nào?</li>"
                   r"<li>Gập đôi dây thành dây hai sợi chập nhau (dài một nửa, hai sợi cùng dẫn điện). Mắc dây này vào hiệu điện thế $11\ \text{V}$ như trước. Ampe kế chỉ bao nhiêu?</li></ol>"),
]
for d_ in DE:
    d_["problem_html"] = d_["problem_html"].replace('\\"', '"')

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [(r"&quot;vôn kế chỉ $6{,}0$ V&quot;", r"$U=6{,}0\ \text{V}$", r"Vôn kế mắc song song với $R$: đo $U$ giữa hai đầu $R$"),
  (r"&quot;ampe kế chỉ $240$ mA&quot;", r"$I=240\ \text{mA}$", r"⚠ Công thức dùng $U$ (V), $I$ (A), $R$ ($\Omega$): đổi mA ra A trước"),
  (r"&quot;tính điện trở $R$&quot;", r"Cần $R$", r"$R=\dfrac{U}{I}$"),
  (r"&quot;coi điện trở không đổi&quot;", r"$R$ giữ nguyên", r"⚠ Điều kiện: $R$ do dây quyết định, không đổi theo $U$"),
  (r"&quot;Tăng hiệu điện thế giữa hai đầu $R$ lên $9{,}0\ \text{V}$. Khi đó ampe kế chỉ bao nhiêu miliampe?&quot;", r"$U'=9{,}0\ \text{V}$; cần $I'$", r"Định luật Ohm: $I'=\dfrac{U'}{R}$")],
 [(r"&quot;đồ thị $I$ theo $U$&quot;", r"Trục đứng $I$ (A), trục ngang $U$ (V)", r"⚠ Đọc đúng trục trước khi chia: $R=\dfrac{U}{I}$, không phải $\dfrac{I}{U}$"),
  (r"&quot;đường 1&quot;, &quot;đường 2&quot;", r"Hai đường thẳng qua gốc $O$", r"Mỗi đường là một điện trở theo định luật Ohm"),
  (r"&quot;tính $R_1$ và $R_2$&quot;", r"Cần $R_1$, $R_2$", r"Chọn một điểm nằm đúng giao lưới trên mỗi đường; $R=\dfrac{U}{I}$"),
  (r"&quot;cản trở dòng điện nhiều hơn&quot;", r"So sánh $R_1$, $R_2$", r"Điện trở cho biết mức cản trở dòng điện"),
  (r"&quot;Phải đặt vào hai đầu $R_2$ hiệu điện thế bao nhiêu để dòng điện qua nó là $0{,}5\ \text{A}$?&quot;", r"$I=0{,}5\ \text{A}$; cần $U$", r"Tìm $U$ này trên đồ thị được không? Nếu không, dùng công thức nào?")],
 [(r"&quot;cùng làm bằng constantan&quot;", r"Cùng $\rho$", r"⚠ Điều kiện để chỉ so $l$ và $S$: cùng vật liệu"),
  (r"&quot;dây 1 dài $2$ m … $2{,}5\ \Omega$&quot;", r"$l_1=2\ \text{m}$; $S_1=0{,}4\ \text{mm}^2$; $R_1=2{,}5\ \Omega$", r"$R=\rho\dfrac{l}{S}$: $R$ tỉ lệ thuận với $l$, tỉ lệ nghịch với $S$"),
  (r"&quot;dây 2 dài $6$ m, tiết diện $0{,}5$ mm²&quot;", r"$l_2=6\ \text{m}$; $S_2=0{,}5\ \text{mm}^2$", r"Chiều dài đổi mấy lần? Tiết diện đổi mấy lần?"),
  (r"&quot;không dùng điện trở suất&quot;", r"Cần $R_2$", r"Lần lượt đổi $l$ rồi đổi $S$ từ $R_1$"),
  (r"&quot;Mắc dây 2 vào hiệu điện thế $4{,}5\ \text{V}$. Tính cường độ dòng điện qua dây.&quot;", r"$U=4{,}5\ \text{V}$; cần $I$", r"$I=\dfrac{U}{R}$ với điện trở của dây 2")],
 [(r"&quot;Vôn kế chỉ $11\ \text{V}$, ampe kế chỉ $250\ \text{mA}$&quot;", r"$U=11\ \text{V}$; $I=250\ \text{mA}$", r"⚠ Đổi mA ra A; $R=\dfrac{U}{I}$"),
  (r"&quot;dài $20\ \text{m}$, tiết diện $0{,}5\ \text{mm}^2$&quot;", r"$l=20\ \text{m}$; $S=0{,}5\ \text{mm}^2$", r"⚠ $R=\rho\dfrac{l}{S}$ dùng $S$ (m²): $1\ \text{mm}^2=10^{-6}\ \text{m}^2$"),
  (r"&quot;Tính điện trở suất của dây. Dây làm bằng vật liệu nào?&quot;", r"Cần $\rho$", r"Rút $\rho$ từ $R=\rho\dfrac{l}{S}$, rồi so với bảng của đề"),
  (r"&quot;coi nhiệt độ dây không đổi&quot;", r"$\rho$ không đổi", r"⚠ Điều kiện: gập đôi vẫn là dây đó, cùng vật liệu"),
  (r"&quot;Gập đôi dây thành dây hai sợi chập nhau (dài một nửa, hai sợi cùng dẫn điện)&quot;", r"Dây mới dài $10\ \text{m}$, gồm hai sợi", r"Gập đôi làm đổi những đại lượng nào trong $R=\rho\dfrac{l}{S}$?"),
  (r"&quot;Mắc dây này vào hiệu điện thế $11\ \text{V}$ như trước. Ampe kế chỉ bao nhiêu?&quot;", r"$U=11\ \text{V}$; cần $I'$", r"$I'=\dfrac{U}{R'}$")],
]

# ───────────── Lời giải ─────────────
RO = [r"<strong>Khái niệm:</strong> điện trở $R$ cho biết vật dẫn cản trở dòng điện nhiều hay ít.",
      r"<strong>Định luật Ohm:</strong> $I$ tỉ lệ thuận với $U$, tỉ lệ nghịch với $R$.",
      r"Công thức: $I=\dfrac{U}{R}$ và $R=\dfrac{U}{I}$.",
      r"Đơn vị: $U$ (V), $I$ (A), $R$ ($\Omega$); $1\ \text{A}=1\,000\ \text{mA}$.",
      r"⚠ <strong>Điều kiện:</strong> nhiệt độ không đổi thì $R$ của dây không đổi khi $U$ đổi."]
RL = [r"<strong>Khái niệm:</strong> điện trở của dây phụ thuộc chiều dài, tiết diện, vật liệu.",
      r"Công thức: $R=\rho\dfrac{l}{S}$.",
      r"Cùng vật liệu: $R$ tỉ lệ thuận với $l$, tỉ lệ nghịch với $S$.",
      r"Đơn vị: $\rho$ ($\Omega\cdot\text{m}$), $l$ (m), $S$ (m²); $1\ \text{mm}^2=10^{-6}\ \text{m}^2$.",
      r"⚠ <strong>Điều kiện:</strong> so hai dây chỉ bằng $l$ và $S$ khi cùng vật liệu, cùng nhiệt độ."]

SOLS = [
 sol(RO, [
  ("Đổi đơn vị", [P("Đổi mA ra A:"), M(r"I=240\ \text{mA}=\dfrac{240}{1\,000}\ \text{A}"), A(r"I=0{,}24\ \text{A}")]),
  ("Tính điện trở", [P("Công thức:"), M(r"R=\dfrac{U}{I}"), M(r"R=\dfrac{6{,}0}{0{,}24}"), A(r"R=25\ \Omega")]),
  ("Cường độ dòng điện mới", [P("$R$ không đổi, $U'=9{,}0$ V:"), M(r"I'=\dfrac{U'}{R}"), M(r"I'=\dfrac{9{,}0}{25}=0{,}36\ \text{A}"), A(r"I'=360\ \text{mA}")]),
  ("Kiểm tra", [P("$U$ tăng $\\dfrac{9{,}0}{6{,}0}=1{,}5$ lần thì $I$ cũng tăng $1{,}5$ lần."), M(r"240\cdot1{,}5=360\ \text{mA}"), P("Khớp. Đơn vị: V : A = Ω ✓")])],
  [r"a) $R=25\ \Omega$", r"b) $I'=360\ \text{mA}$"],
  "Nhận dạng: đề cho <strong>số chỉ vôn kế, ampe kế</strong> → đổi mA ra A, $R=\\dfrac{U}{I}$; đổi $U$ thì giữ $R$, tính lại $I$."),
 sol(RO[1:] + [r"Đồ thị $I$ theo $U$ của một điện trở: đường thẳng qua gốc $O$."], [
  ("Điện trở $R_1$", [P("Trên đường 1, điểm ở giao lưới: $U=6$ V, $I=0{,}4$ A."), M(r"R_1=\dfrac{U}{I}=\dfrac{6}{0{,}4}"), A(r"R_1=15\ \Omega")]),
  ("Điện trở $R_2$", [P("Trên đường 2, điểm ở giao lưới: $U=8$ V, $I=0{,}2$ A."), M(r"R_2=\dfrac{U}{I}=\dfrac{8}{0{,}2}"), A(r"R_2=40\ \Omega")]),
  ("So sánh", [M(r"R_2=40\ \Omega\gt R_1=15\ \Omega"), A(r"T:$R_2$ cản trở dòng điện nhiều hơn."), P("Đường 2 thoải hơn: cùng $U$, dòng qua $R_2$ nhỏ hơn.")]),
  ("Hiệu điện thế cần đặt vào $R_2$", [P("Từ $I=\\dfrac{U}{R}$:"), M(r"U=I\cdot R_2"), M(r"U=0{,}5\cdot40"), A(r"U=20\ \text{V}")]),
  ("Kiểm tra", [P("Trên đồ thị, $U=12$ V cho $I=0{,}3$ A."), P("Muốn $0{,}5$ A thì cần $U$ lớn hơn $12$ V ✓"), M(r"\dfrac{20}{40}=0{,}5\ \text{A}\ ✓")])],
  [r"a) $R_1=15\ \Omega$", r"$R_2=40\ \Omega$", r"b) $R_2$ cản trở dòng điện nhiều hơn", r"c) $U=20\ \text{V}$"],
  "Nhận dạng: đề cho <strong>đồ thị $I$ theo $U$</strong> → chọn điểm ở giao lưới, $R=\\dfrac{U}{I}$; đường thoải hơn có $R$ lớn hơn."),
 sol(RL[1:] + [r"Định luật Ohm: $I=\dfrac{U}{R}$."], [
  ("Chỉ đổi chiều dài", [P("Giữ $S=0{,}4\\ \\text{mm}^2$, chiều dài tăng:"), M(r"\dfrac{l_2}{l_1}=\dfrac{6}{2}=3"), P("Dây dài $6$ m, tiết diện $0{,}4\\ \\text{mm}^2$:"), M(r"R'=3R_1=3\cdot2{,}5"), A(r"R'=7{,}5\ \Omega")]),
  ("Đổi tiết diện", [P("Tiết diện tăng:"), M(r"\dfrac{S_2}{S_1}=\dfrac{0{,}5}{0{,}4}=1{,}25"), P("Tiết diện lớn hơn thì $R$ nhỏ hơn bấy nhiêu lần:"), M(r"R_2=\dfrac{R'}{1{,}25}=\dfrac{7{,}5}{1{,}25}"), A(r"R_2=6\ \Omega")]),
  ("Cường độ dòng điện", [M(r"I=\dfrac{U}{R_2}=\dfrac{4{,}5}{6}"), A(r"I=0{,}75\ \text{A}")]),
  ("Kiểm tra", [P("Cách kiểm khác, $\\rho$ constantan tra ở bài: $0{,}5\\cdot10^{-6}\\ \\Omega\\cdot\\text{m}$."), P("Tính thẳng điện trở dây 2:"), M(r"R_2=0{,}5\cdot10^{-6}\cdot\dfrac{6}{0{,}5\cdot10^{-6}}=6\ \Omega\ ✓")])],
  [r"a) $R_2=6\ \Omega$", r"b) $I=0{,}75\ \text{A}$"],
  "Nhận dạng: <strong>cùng vật liệu</strong>, đề cho một dây đã biết $R$ → so $l$ (nhân) và $S$ (chia), không cần $\\rho$."),
 sol([RO[0], r"Định luật Ohm: $I=\dfrac{U}{R}$, suy ra $R=\dfrac{U}{I}$.", RL[1], r"Đổi đơn vị: $1\ \text{A}=1\,000\ \text{mA}$; $1\ \text{mm}^2=10^{-6}\ \text{m}^2$.", r"⚠ <strong>Điều kiện:</strong> cùng nhiệt độ thì $\rho$ của vật liệu không đổi."], [
  ("Điện trở cuộn dây", [M(r"I=250\ \text{mA}=0{,}25\ \text{A}"), M(r"R=\dfrac{U}{I}=\dfrac{11}{0{,}25}"), A(r"R=44\ \Omega")]),
  ("Điện trở suất", [P("Đổi tiết diện:"), M(r"S=0{,}5\ \text{mm}^2=0{,}5\cdot10^{-6}\ \text{m}^2"), P("Rút $\\rho$ từ $R=\\rho\\dfrac{l}{S}$:"), M(r"\rho=\dfrac{R\cdot S}{l}=\dfrac{44\cdot0{,}5\cdot10^{-6}}{20}"), A(r"\rho=1{,}1\cdot10^{-6}\ \Omega\cdot\text{m}")]),
  ("Vật liệu", [P("So với bảng của đề:"), A("T:Trùng với nichrome: dây làm bằng <strong>nichrome</strong>.")]),
  ("Điện trở sau khi gập đôi", [P("Dây hai sợi chập nhau dài một nửa: $R$ giảm 2 lần."), P("Hai sợi cùng dẫn điện, như một dây có tiết diện gấp đôi: $R$ giảm thêm 2 lần."), M(r"R'=\dfrac{R}{4}=\dfrac{44}{4}"), A(r"R'=11\ \Omega")]),
  ("Số chỉ ampe kế", [M(r"I'=\dfrac{U}{R'}=\dfrac{11}{11}"), A(r"I'=1{,}0\ \text{A}")]),
  ("Kiểm tra", [P("$R$ giảm 4 lần thì $I$ tăng 4 lần:"), M(r"0{,}25\cdot4=1{,}0\ \text{A}\ ✓"), P("Dây ngắn hơn, hai sợi cùng dẫn thì cản ít hơn, dòng lớn hơn: hợp lí.")])],
  [r"a) $R=44\ \Omega$", r"b) $\rho=1{,}1\cdot10^{-6}\ \Omega\cdot\text{m}$", r"Dây làm bằng nichrome", r"c) $I'=1{,}0\ \text{A}$"],
  "Nhận dạng: đề cho <strong>số đo U, I</strong> và <strong>kích thước dây</strong> → $R=\\dfrac{U}{I}$ rồi rút $\\rho$; <strong>gập đôi</strong> thì dài một nửa, hai sợi cùng dẫn: $R$ giảm 4 lần."),
]

# ───────────── Tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>vôn kế chỉ … V, ampe kế chỉ … mA</b> → đổi mA ra A, rồi $R=\dfrac{U}{I}$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đổi đơn vị", "Cường độ dòng điện $I$ bằng bao nhiêu ampe?", 0.24, "A", 0.005,
       loi=r"Hay chia cho $100$ hoặc nhân với $1\,000$. Vì $1\ \text{A}=1\,000\ \text{mA}$ nên đổi mA ra A là chia cho $1\,000$."),
  buoc("Tính điện trở", "Điện trở $R$ bằng bao nhiêu?", 25, "Ω", 0.3,
       loi=r"Để nguyên số mA khi chia sẽ ra $R$ rất nhỏ, vô lí. Nhân $U\cdot I$ cũng sai: $R$ là thương $\dfrac{U}{I}$.",
       ke=[(r"$R=\dfrac{U}{I}$ với $I$ đã đổi ra A", True),
           (r"$R=U\cdot I$", r"Điện trở là thương của $U$ và $I$, không phải tích."),
           (r"$R=\dfrac{U}{I}$ với $I$ để nguyên mA", r"Công thức dùng $I$ (A); để mA thì $R$ nhỏ đi $1\,000$ lần.")]),
  buoc("Cường độ dòng điện mới", "Khi $U=9{,}0$ V, ampe kế chỉ bao nhiêu miliampe?", 360, "mA", 3,
       loi=r"Hay giữ nguyên số chỉ ampe kế vì nghĩ $R$ tăng theo $U$. Thật ra $R$ không đổi, $I$ tăng theo $U$.",
       ke=[(r"Giữ $R$, tính $I'=\dfrac{U'}{R}$", True),
           (r"Tính $R$ mới bằng $\dfrac{U'}{I}$, coi $I$ không đổi", r"$R$ do dây quyết định, không đổi khi $U$ đổi; chính $I$ đổi theo $U$."),
           (r"$I'=I\cdot\dfrac{U}{U'}$", r"Tỉ số bị lật: $U$ tăng mà $I$ lại giảm, trái với định luật Ohm ($I$ tỉ lệ thuận với $U$).")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>đồ thị $I$ theo $U$</b> → chọn điểm ở giao lưới, $R=\dfrac{U}{I}$; đường <b>thoải</b> hơn thì $R$ lớn hơn.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điện trở $R_1$", "Điện trở $R_1$ bằng bao nhiêu?", 15, "Ω", 0.3,
       loi=r"Lấy $\dfrac{I}{U}$ (độ dốc) thay vì $\dfrac{U}{I}$ sẽ ra một số rất nhỏ. Đọc đúng trục: trục đứng là $I$."),
  buoc("Điện trở $R_2$", "Điện trở $R_2$ bằng bao nhiêu?", 40, "Ω", 0.5,
       loi=r"Chọn điểm không nằm trên giao lưới rồi đọc ước chừng, hoặc đọc nhầm sang đường 1.",
       ke=[(r"Chọn một điểm ở giao lưới trên đường 2, $R_2=\dfrac{U}{I}$", True),
           (r"Lấy độ dốc $\dfrac{I}{U}$ của đường 2 làm $R_2$", r"Trục đứng là $I$ nên $\dfrac{I}{U}$ là $\dfrac{1}{R}$, không phải $R$."),
           (r"Đường 2 thoải hơn nên $R_2$ nhỏ hơn $R_1$, chỉ cần ước lượng", r"Ngược chiều: cùng $U$, đường thoải cho $I$ nhỏ hơn, tức cản nhiều hơn; và đề hỏi giá trị nên phải tính.")]),
  buoc("So sánh", "Điện trở nào cản trở dòng điện nhiều hơn?",
       loi=r"Hay nghĩ đường dốc hơn có điện trở lớn hơn. Ở đồ thị $I$ theo $U$, dốc hơn là dòng lớn hơn ở cùng $U$.",
       lua_chon=[(r"$R_2$", True),
                 (r"$R_1$, vì đường 1 dốc hơn", r"Cùng $U$, đường 1 cho $I$ lớn hơn, tức $R_1$ cản ít hơn."),
                 (r"Bằng nhau, vì cùng đi qua gốc $O$", r"Đi qua gốc chỉ cho biết cả hai tuân theo định luật Ohm, không cho biết $R$ bằng nhau.")],
       ke=[(r"So hai giá trị $R$ vừa tính", True),
           (r"Đọc $U$ lớn nhất của mỗi đường rồi so", r"Hai đường cùng dừng ở $12$ V nên $U$ lớn nhất bằng nhau, không so được gì."),
           (r"So độ dốc: dốc hơn thì cản nhiều hơn", r"Trục đứng là $I$: dốc hơn là dòng lớn hơn, tức cản ít hơn.")]),
  buoc("Hiệu điện thế cần đặt vào $R_2$", "Cần đặt vào $R_2$ hiệu điện thế bao nhiêu vôn?", 20, "V", 0.3,
       loi=r"Hay tìm trên đồ thị và không thấy vì $0{,}5$ A nằm ngoài khung; phải tính bằng định luật Ohm. Chia $\dfrac{I}{R}$ hoặc $\dfrac{R}{I}$ cũng sai.",
       ke=[(r"$U=I\cdot R_2$ (từ $I=\dfrac{U}{R}$)", True),
           (r"$U=\dfrac{I}{R_2}$", r"Từ $I=\dfrac{U}{R}$ suy ra $U=I\cdot R$, không phải chia."),
           (r"$U=\dfrac{R_2}{I}$", r"Sai đơn vị: $\Omega$ chia A không ra V. Đúng là $U=I\cdot R$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>cùng vật liệu</b> và <b>một dây đã biết điện trở</b> → so chiều dài (nhân), so tiết diện (chia).",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Chỉ đổi chiều dài", r"Một dây constantan dài $6$ m, tiết diện $0{,}4\ \text{mm}^2$ có điện trở bao nhiêu?", 7.5, "Ω", 0.1,
       loi=r"Hay chia cho tỉ số chiều dài. Dây dài hơn thì cản nhiều hơn: $R$ tỉ lệ thuận với $l$."),
  buoc("Đổi tiết diện", "Điện trở của dây 2 bằng bao nhiêu?", 6, "Ω", 0.1,
       loi=r"Hay nhân thêm tỉ số tiết diện như với chiều dài. Tiết diện lớn hơn thì dòng điện có đường đi rộng hơn, $R$ nhỏ hơn: chia cho tỉ số tiết diện.",
       ke=[(r"Chia cho $\dfrac{S_2}{S_1}$ vì $R$ tỉ lệ nghịch với $S$", True),
           (r"Nhân với $\dfrac{S_2}{S_1}$ như với chiều dài", r"$R$ tỉ lệ nghịch với $S$: tiết diện lớn hơn thì $R$ nhỏ hơn, phải chia."),
           (r"Bỏ qua tiết diện vì hai dây cùng vật liệu", r"Cùng vật liệu chỉ cho cùng $\rho$; $R$ vẫn phụ thuộc $l$ và $S$.")]),
  buoc("Cường độ dòng điện", "Cường độ dòng điện qua dây 2 bằng bao nhiêu?", 0.75, "A", 0.01,
       loi=r"Hay dùng nhầm điện trở của dây 1. Đề hỏi dây 2 nên dùng $R_2$.",
       ke=[(r"$I=\dfrac{U}{R_2}$", True),
           (r"$I=\dfrac{U}{R_1}$", r"Dây mắc vào nguồn là dây 2, phải dùng $R_2$."),
           (r"$I=U\cdot R_2$", r"Định luật Ohm: $I=\dfrac{U}{R}$; nhân sẽ sai cả đơn vị.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>số đo U, I</b> kèm <b>chiều dài, tiết diện</b> → rút $\rho$; <b>gập đôi</b> → $R$ giảm 4 lần.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Điện trở cuộn dây", "Điện trở của cuộn dây bằng bao nhiêu?", 44, "Ω", 0.5,
       loi=r"Quên đổi mA ra A nên chia cho $250$, ra $R$ nhỏ hơn $1\ \Omega$, vô lí với dây dài $20$ m."),
  buoc("Điện trở suất", r"Điện trở suất $\rho$ bằng bao nhiêu (đơn vị $10^{-6}\ \Omega\cdot\text{m}$)?", 1.1, "·10⁻⁶ Ω·m", 0.02,
       loi=r"Để nguyên $S$ theo $\text{mm}^2$ thì $\rho$ lớn gấp một triệu lần. Rút ngược $\dfrac{R\cdot l}{S}$ cũng sai. Đổi $S$ ra m² trước.",
       ke=[(r"$\rho=\dfrac{R\cdot S}{l}$ với $S$ đổi ra m²", True),
           (r"$\rho=\dfrac{R\cdot l}{S}$", r"Rút sai: từ $R=\rho\dfrac{l}{S}$ nhân hai vế với $S$ rồi chia cho $l$."),
           (r"$\rho=\dfrac{R\cdot S}{l}$ với $S$ để nguyên mm²", r"$\rho$ trong bảng tính theo $\Omega\cdot\text{m}$ nên $S$ phải ở m².")]),
  buoc("Vật liệu", "Dây làm bằng vật liệu nào?",
       loi=r"Hay so nhầm bậc luỹ thừa: $10^{-6}$ khác $10^{-8}$ một trăm lần.",
       lua_chon=[("Nichrome", True),
                 ("Đồng", r"Thế $\rho$ của đồng vào $R=\rho\dfrac{l}{S}$: dây chỉ cản khoảng $0{,}7\ \Omega$, nhỏ hơn nhiều so với $44\ \Omega$."),
                 ("Constantan", r"Thế $\rho$ của constantan vào $R=\rho\dfrac{l}{S}$: $R=20\ \Omega$, chưa bằng một nửa $44\ \Omega$.")],
       ke=[(r"So $\rho$ vừa tính với bảng điện trở suất của đề", True),
           (r"Chọn vật liệu có $\rho$ nhỏ nhất vì dây dẫn điện", r"Dây nào cũng dẫn điện; phải so đúng giá trị $\rho$ vừa tính."),
           (r"So $R$ vừa tính với bảng", r"Bảng cho $\rho$ (đặc trưng vật liệu), không cho $R$; $R$ còn phụ thuộc $l$ và $S$.")]),
  buoc("Điện trở sau khi gập đôi", "Điện trở của dây sau khi gập đôi bằng bao nhiêu?", 11, "Ω", 0.2,
       loi=r"Hay chỉ chia đôi vì dây dài một nửa, quên rằng hai sợi cùng dẫn điện làm $R$ giảm thêm.",
       ke=[(r"Dài một nửa và hai sợi cùng dẫn điện: $R'=\dfrac{R}{4}$", True),
           (r"$R'=\dfrac{R}{2}$ vì dây dài một nửa", r"Hai sợi chập nhau cùng dẫn điện, như tiết diện gấp đôi, nên $R$ giảm thêm 2 lần."),
           (r"$R'=R$ vì vẫn là dây đó", r"Vật liệu giữ nguyên nhưng chiều dài và cách dẫn điện đã đổi, nên $R$ đổi.")]),
  buoc("Số chỉ ampe kế", "Sau khi gập đôi, ampe kế chỉ bao nhiêu ampe?", 1.0, "A", 0.02,
       loi=r"Hay chia số chỉ cũ cho 4 vì $R$ giảm 4 lần. $I$ tỉ lệ nghịch với $R$: $R$ giảm thì $I$ tăng.",
       ke=[(r"$I'=\dfrac{U}{R'}$", True),
           (r"$I'=\dfrac{I}{4}$ vì $R$ giảm 4 lần", r"Lật ngược: $I$ tỉ lệ nghịch với $R$, $R$ giảm thì $I$ tăng."),
           (r"$I'=2I$ vì hai sợi cùng dẫn", r"Chỉ tính hai sợi, bỏ quên dây cũng ngắn đi một nửa.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Ghi JSON ─────────────
d = {"lesson_id": 89, "lesson_title": "Bài 11. Điện trở. Định luật Ohm", "generated_at": "2026-10-11",
     "review": {"checked": False, "notes": "Soạn 11/10/2026 (chặng 3). Kiểm chéo vòng 1 xong, đã sửa 15 mục nên-sửa; chờ kiểm lại. Chưa đối chiếu ngân hàng câu hỏi (topic 89/90)."},
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
print("xong 89.json")
