"""Bài tập mẫu Chuyên đề 10 "Lực: tổng hợp lực, cân bằng, ma sát, đòn bẩy" (khoá Vật lí HSG & chuyên, KHTN 9) — lesson_id 155.
Ký hiệu khớp content/hsg9/cd10-luc/theory.src.html: F_msn, F_mst, μ_n, μ_t, N, F_đh = kΔl, M = F·d.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-155.py   (idempotent; in phần tự giải lại bằng Python)"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

J = os.path.join(HERE, "155.json")

# ═════════════ TỰ GIẢI LẠI BẰNG PYTHON (độc lập với lời giải viết tay) ═════════════
g = 10
# D1
assert 30 + 40 == 70 and 40 - 30 == 10 and math.hypot(30, 40) == 50
R60 = math.sqrt(21 ** 2 + 24 ** 2 + 2 * 21 * 24 * math.cos(math.radians(60))); assert abs(R60 - 39) < 1e-9
# D2
P2 = 10 * 6; S2, C2 = 0.6, 0.8; TM2 = 55                      # sinθ = 0,6 (θ ≈ 36,9° ≈ 37°), T_max = 55 N
T2 = P2 / (2 * S2); assert abs(T2 - 50) < 1e-9 and T2 != P2
th_min = math.degrees(math.asin(P2 / (2 * TM2))); assert abs(th_min - 33.06) < 0.01
T60 = P2 / (2 * math.sin(math.radians(60)))
# mọi cách làm sai đều cho kết luận khác đáp án đúng (T < T_max, nhưng P > T_max và 2T > T_max)
assert T2 < TM2 < P2 and TM2 < 2 * T2
assert P2 / TM2 > 1                                          # T_max·sinθ = P vô nghiệm
th_cos = math.degrees(math.acos(P2 / (2 * TM2))); assert abs(th_cos - 56.94) < 0.01   # nhầm cos cho góc khác hẳn 33,1°
assert abs(P2 / (2 * C2) - 37.5) < 1e-9                      # nhầm 2T·cosθ = P cho T = 37,5 N ≠ 50 N
assert S2 > P2 / (2 * TM2)                                   # θ của đề (sinθ = 0,6) lớn hơn θ_min (sinθ = 0,5455)
# D3
N3 = 10 * 50; Fn3 = 0.4 * N3; Ft3 = 0.3 * N3; assert (N3, Fn3, Ft3) == (500, 200, 150) and 120 < Fn3
# D4 (3-4-5)
s4, c4 = 3 / 5, 4 / 5; P4 = 100; Pp4 = P4 * s4; N4 = P4 * c4; Fn4 = 0.8 * N4
assert (Pp4, N4, Fn4) == (60, 80, 64) and Pp4 < Fn4
F4 = Pp4 + 0.6 * N4; assert abs(F4 - 108) < 1e-9
a4 = math.degrees(math.atan(0.8)); assert abs(a4 - 38.66) < 0.01
# D5
Pt, Pv = 20, 30
F5 = (Pt * 0.5 + Pv * 0.8) / 1.0; R5 = Pt + Pv - F5; x5 = (28 * 1.0 - Pt * 0.5) / Pv
assert (F5, R5) == (34, 16) and abs(x5 - 0.6) < 1e-9
assert abs(R5 * 1.0 - (Pt * 0.5 + Pv * 0.2)) < 1e-9          # kiểm bằng moment đối với B
# D6
P6 = 40; Pp6 = P6 * 0.6; N6 = P6 * 0.8; Fn6 = 0.5 * N6
Fdh_min = Pp6 - Fn6; Fdh_max = Pp6 + Fn6
assert (Pp6, N6, Fn6, Fdh_min, Fdh_max) == (24, 32, 16, 8, 40)
dl_min, dl_max = Fdh_min / 200 * 100, Fdh_max / 200 * 100; assert (dl_min, dl_max) == (4, 20)
Fms6 = Pp6 - 200 * 0.10; assert Fms6 == 4 and 0 <= Fms6 <= Fn6 and 0.75 > 0.5
print("tự giải: D1 R60=%.1f | D2 T=%.1f θmin=%.2f T60=%.1f | D3 %s | D4 F=%.0f αmax=%.2f | D5 F=%s R=%s x=%.2f | D6 Δl %s–%s cm, Fms=%s" %
      (R60, T2, th_min, T60, (N3, Fn3, Ft3), F4, a4, F5, R5, x5, dl_min, dl_max, Fms6))

# ═════════════ TIỆN ÍCH HÌNH ═════════════
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def mover(dx, dy, dur, inner):
    """Nhóm tịnh tiến thẳng đều: chạy MỘT lần khi bấm, dừng ở khung cuối."""
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{dx:.1f} {dy:.1f}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>')

def sampled(pts, dur):
    vals = ";".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return f'<animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'

import re as _re
def rich(s, size=13):
    """`F_ms` → F với chỉ số dưới ms."""
    parts = _re.split(r"_([A-Za-zđ0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def tri(pts, c="currentColor", sw=2.4, fill="none"):
    return '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="{fill}" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>'

def zig(xa, xb, y, n=9, amp=7):
    """Lò xo dạng răng cưa từ xa tới xb, cùng cấu trúc đường dẫn để SMIL nội suy `d`."""
    L = xb - xa
    pts = [(xa, y), (xa + L * 0.08, y)]
    for i in range(n):
        pts.append((xa + L * (0.08 + 0.84 * (i + 0.5) / n), y + (amp if i % 2 == 0 else -amp)))
    pts += [(xa + L * 0.92, y), (xb, y)]
    return "M" + " L".join(f"{x:.1f},{yy:.1f}" for x, yy in pts)


# ───────────── Dạng 1 · hai lực đồng quy 30 N và 40 N ─────────────
def d1(kk):
    p = f"d1{kk}"; K = 2
    if kk == 0:
        cx, cy, W, H = 70, 172, 50, 30
        b = defs(p) + R(cx - W / 2, cy - H / 2, W, H, sw=1.4, dash="5 4", op=.45)
        inner = R(cx - W / 2, cy - H / 2, W, H, sw=2.4)
        inner += vec_luc("r", cx + W / 2, cy, 1, 0, 40, K, 3)[0] + txt(cx + W / 2 + 40 * K + 6, cy + 5, "F₂ = 40 N", RED)
        inner += vec_luc("o", cx, cy - H / 2, 0, -1, 30, K, 3)[0] + txt(cx + 8, cy - H / 2 - 30 * K - 6, "F₁ = 30 N", ORG)
        b += mover(80, -60, 4, inner)
        b += txt(16, 24, "Hai lực vuông góc", "currentColor", 13) + txt(16, 44, "R = ?", BLUE)
        return fig("c1-0", "0 0 420 206", "Một vật nhỏ chịu hai lực vuông góc, 30 niutơn hướng lên và 40 niutơn hướng sang phải, và chuyển động theo hướng của hợp lực",
                   b, "Mô phỏng: vật chuyển động theo hướng của hợp lực (hướng vẽ đúng tỉ lệ hai lực, quãng đường minh hoạ). Chạy 4 s.")
    b = defs(p)
    b += txt(16, 22, "Cùng chiều: R = F₁ + F₂", "currentColor", 13, "start", "400") + txt(222, 22, "Ngược chiều: R = |F₂ − F₁|", "currentColor", 13, "start", "400")
    b += vec_luc("r", 30, 46, 1, 0, 40, K, 3)[0] + txt(30 + 40 * K + 6, 50, "F₂", RED)
    b += vec_luc("o", 30, 62, 1, 0, 30, K, 3)[0] + txt(30 + 30 * K + 6, 66, "F₁", ORG)
    b += vec_luc("r", 270, 54, 1, 0, 40, K, 3)[0] + txt(270 + 40 * K + 6, 58, "F₂", RED)
    b += vec_luc("o", 270, 54, -1, 0, 30, K, 3)[0] + txt(270 - 30 * K - 6, 58, "F₁", ORG, 13, "end")
    b += txt(16, 108, "Vuông góc:", "currentColor", 13, "start", "400") + txt(16, 126, "R² = F₁² + F₂²", "currentColor", 13, "start", "400")
    ox, oy = 40, 200
    b += seg(ox, oy - 30 * K, ox + 40 * K, oy - 30 * K, GREY, 1.6, "5 4") + seg(ox + 40 * K, oy - 30 * K, ox + 40 * K, oy, GREY, 1.6, "5 4")
    b += seg(ox, oy, ox + 40 * K, oy - 30 * K, BLUE, 1.8, "5 4")
    b += vec_luc("r", ox, oy, 1, 0, 40, K, 3)[0] + txt(ox + 40 * K + 8, oy + 5, "F₂", RED)
    b += vec_luc("o", ox, oy, 0, -1, 30, K, 3)[0] + txt(ox - 8, oy - 30 * K / 2 + 4, "F₁", ORG, 13, "end")
    b += txt(ox + 40 * K + 8, oy - 30 * K + 4, "R = ?", BLUE, 13)
    qx, qy = 262, 200
    a1 = (21 * K * math.cos(math.radians(60)), -21 * K * math.sin(math.radians(60)))
    b += txt(222, 108, "Hợp góc α:", "currentColor", 13, "start", "400") + txt(222, 126, "R² = F₁² + F₂² + 2F₁F₂cosα", "currentColor", 12, "start", "400")
    b += seg(qx + 24 * K, qy, qx + 24 * K + a1[0], qy + a1[1], GREY, 1.6, "5 4") + seg(qx + a1[0], qy + a1[1], qx + 24 * K + a1[0], qy + a1[1], GREY, 1.6, "5 4")
    b += seg(qx, qy, qx + 24 * K + a1[0], qy + a1[1], BLUE, 1.8, "5 4")
    b += vec_luc("r", qx, qy, 1, 0, 24, K, 3)[0] + txt(qx + 24 * K + 8, qy + 5, "F₂", RED)
    b += vec_luc("o", qx, qy, math.cos(math.radians(60)), -math.sin(math.radians(60)), 21, K, 3)[0] + txt(qx + a1[0] - 6, qy + a1[1] - 6, "F₁", ORG, 13, "end")
    b += arc(qx, qy, 18, 0, 60, "currentColor", 1.6) + txt(qx + 22, qy - 8, "α", "currentColor", 13)
    return fig("c1-2", "0 0 420 216", "Hợp lực của hai lực cùng chiều, ngược chiều, vuông góc và hợp góc anpha được dựng theo quy tắc hình bình hành",
               b, "Dữ kiện: quy tắc hình bình hành cho từng trường hợp (cùng một tỉ lệ cho mọi lực; riêng hình hợp góc dùng hai lực khác của câu c). " + NOTE)


# ───────────── Dạng 2 · đèn 6 kg treo bằng hai dây hợp phương ngang θ (sinθ = 0,6) ─────────────
def d2(kk):
    p = f"d2{kk}"; CX, CE, L = 210, 52, 130; TH2 = math.degrees(math.asin(0.6))   # ≈ 36,9°
    def geom(th):
        r = math.radians(th); return CX - L * math.cos(r), CX + L * math.cos(r), CE + L * math.sin(r)
    lax, rax, ly1 = geom(TH2)
    def lamp(ly, op=1):
        return (R(CX - 8, ly, 16, 9, sw=2.2) + circ(CX, ly + 22, 13, "currentColor", 2.4))
    b = defs(p) + seg(16, CE, 404, CE, "currentColor", 3)
    if kk == 0:
        N = 15; dur = 4
        ths = [75 + (TH2 - 75) * i / N for i in range(N + 1)]
        G = [geom(t) for t in ths]
        ly0 = G[0][2]
        # dây và điểm treo đứng ở vị trí cuối, mờ, kèm cung θ
        b += seg(lax, CE, CX, ly1, "currentColor", 2, "5 4", .35) + seg(rax, CE, CX, ly1, "currentColor", 2, "5 4", .35)
        b += arc(lax, CE, 30, -30, 0, "currentColor", 1.6) + arc(rax, CE, 30, 180, 210, "currentColor", 1.6)
        b += txt(lax + 38, CE + 12, "θ", "currentColor", 13) + txt(rax - 38, CE + 12, "θ", "currentColor", 13, "end")
        b += (f'<line x1="{G[0][0]:.1f}" y1="{CE}" x2="{CX}" y2="{ly0:.1f}" stroke="currentColor" stroke-width="2.4">'
              f'{smil("x1", [g_[0] for g_ in G], dur)}{smil("y2", [g_[2] for g_ in G], dur)}</line>')
        b += (f'<line x1="{G[0][1]:.1f}" y1="{CE}" x2="{CX}" y2="{ly0:.1f}" stroke="currentColor" stroke-width="2.4">'
              f'{smil("x1", [g_[1] for g_ in G], dur)}{smil("y2", [g_[2] for g_ in G], dur)}</line>')
        b += f'<g>{sampled([(0, g_[2] - ly0) for g_ in G], dur)}{lamp(ly0)}</g>'
        b += txt(16, 22, "đèn m = 6 kg", "currentColor", 13) + txt(222, 22, "θ giảm dần tới 37°", "currentColor", 13, "start", "400")
        b += txt(lax + 52, ly1 + 30, "T = ?", RED, 13, "end") + txt(rax - 52, ly1 + 30, "T = ?", RED, 13, "start")
        return fig("c2-0", "0 0 420 236", "Đèn treo bằng hai dây, hai điểm treo dang rộng dần nên dây thoải dần đến góc xấp xỉ 37 độ so với phương ngang",
                   b, "Mô phỏng: hai điểm treo dang rộng dần, độ dài mỗi dây giữ nguyên, dây thoải dần tới θ ≈ 37° (sinθ = 0,6) so với phương ngang. Chạy 4 s.")
    b += seg(lax, CE, CX, ly1, "currentColor", 2.6) + seg(rax, CE, CX, ly1, "currentColor", 2.6) + lamp(ly1)
    b += arc(lax, CE, 30, -30, 0, "currentColor", 1.6) + arc(rax, CE, 30, 180, 210, "currentColor", 1.6)
    b += txt(lax + 38, CE + 12, "θ", "currentColor", 13) + txt(rax - 38, CE + 12, "θ", "currentColor", 13, "end")
    b += vec_luc("g", CX, ly1 + 22, 0, 1, 60, 0.9, 3)[0] + txt(CX + 10, ly1 + 22 + 38, "P", GRN)
    b += txt(16, 22, "θ ≈ 37° (sinθ = 0,6) so với phương ngang", "currentColor", 13, "start", "400")
    b += txt(16, 232, "Đèn đứng yên: ΣF = 0", "currentColor", 13, "start", "400") + txt(16, 252, "Thành phần ngang: hai lực triệt tiêu", "currentColor", 13, "start", "400")
    b += txt(16, 272, "Thành phần đứng: 2T·sinθ = P", "currentColor", 13, "start", "400")
    return fig("c2-2", "0 0 420 282", "Đèn treo bằng hai dây đối xứng hợp với phương ngang góc xấp xỉ 37 độ; trọng lực P hướng xuống",
               b, "Dữ kiện: góc θ đo với phương ngang nên thành phần đứng của lực căng là T·sinθ. " + NOTE)


# ───────────── Dạng 3 · thùng 50 kg, ma sát nghỉ / trượt trên sàn ngang ─────────────
def d3(kk):
    p = f"d3{kk}"
    if kk == 0:
        FL, S, X0, W, H = 118, 40, 24, 64, 40
        b = defs(p) + ground(FL, 16, 410) + R(X0, FL - H, W, H, sw=1.4, dash="5 4", op=.45)
        crate = R(X0, FL - H, W, H, sw=2.4) + txt(X0 + W / 2, FL - H / 2 + 5, "m = 50 kg", "currentColor", 12, "middle")
        crate += seg(X0 + W, FL - H / 2, X0 + W + 40, FL - H / 2, "currentColor", 2.4)
        crate += R(X0 + W + 40, FL - H / 2 - 12, 56, 24, "currentColor", 2.2, "none", 3) + txt(X0 + W + 68, FL - H / 2 + 5, "lực kế", "currentColor", 12, "middle")
        crate += txt(X0 + W + 68, FL - H / 2 - 20, "F = ?", RED, 13, "middle")
        b += mover(3 * S, 0, 3, crate)
        b += seg(X0, 146, X0 + 3 * S, 146, "currentColor", 1.6)
        for i in range(4):
            b += seg(X0 + i * S, 140, X0 + i * S, 152, "currentColor", 1.6) + txt(X0 + i * S, 168, ("0", "1", "2", "3 m")[i], "currentColor", 12, "middle", "400")
        b += txt(16, 22, "trượt đều", "currentColor", 13) + txt(16, 42, "μ_t = 0,3", "currentColor", 13, "start", "400")
        return fig("c3-0", "0 0 420 180", "Thùng hàng được kéo trượt đều ba mét trên sàn nằm ngang bằng lực kéo nằm ngang đo bằng lực kế",
                   b, "Mô phỏng: thùng trượt đều 3 m trên thước (tốc độ minh hoạ 1 m/s, chạy 3 s). Số chỉ lực kế là đại lượng cần tìm.")
    FL = 170; cx, W, H = 100, 64, 40; cy = FL - H / 2; K = 0.16
    b = defs(p) + ground(FL, 16, 220) + R(cx - W / 2, FL - H, W, H, sw=2.4)
    b += vec_luc("b", cx, cy, 0, -1, 500, K, 3)[0] + txt(cx + 8, cy - 80 + 8, "N", BLUE)
    b += vec_luc("g", cx, cy, 0, 1, 500, K, 3)[0] + txt(cx + 8, cy + 76, "P", GRN)
    b += vec_luc("r", cx + W / 2, cy, 1, 0, 120, K, 3)[0] + txt(cx + W / 2 + 120 * K + 6, cy - 6, "F", RED)
    b += vec_luc("o", cx - W / 2, cy, -1, 0, 120, K, 3)[0] + txt(cx - W / 2 - 120 * K - 6, cy - 6, "F_ms", ORG, 13, "end")
    b += txt(16, 16, "Chưa trượt: F_ms = F", "currentColor", 12, "start", "400") + txt(16, 33, "Sắp trượt: F_ms = μ_n·N", "currentColor", 12, "start", "400") + txt(16, 50, "Đang trượt: F_ms = μ_t·N", "currentColor", 12, "start", "400")
    ox, oy = 262, 214
    b += arrow(p, "g", ox, oy, 408, oy, 2) + txt(408, oy + 16, "F", GRN, 13, "end") + arrow(p, "g", ox, oy, ox, 76, 2) + txt(ox + 6, 80, "F_ms", GRN)
    px, py, fy = 336, 118, 150
    b += poly([(ox, oy), (px, py)], BLUE, 2.6) + poly([(px, fy), (404, fy)], ORG, 2.6) + seg(px, py, px, fy, GREY, 1.6, "4 4")
    b += seg(ox, py, px, py, GREY, 1.4, "5 4") + seg(ox, fy, px, fy, GREY, 1.4, "5 4")
    b += txt(ox - 6, py + 4, "μ_n·N", BLUE, 12, "end") + txt(ox - 6, fy + 4, "μ_t·N", ORG, 12, "end")
    b += txt(ox + 52, oy - 8, "ma sát nghỉ", BLUE, 12, "start", "400") + txt(px + 4, fy + 20, "ma sát trượt", ORG, 12, "start", "400")
    return fig("c3-2", "0 0 420 240", "Bên trái các lực tác dụng lên thùng khi chưa trượt; bên phải đồ thị lực ma sát theo lực kéo: tăng dần tới cực đại rồi giảm xuống giá trị trượt",
               b, "Dữ kiện: ma sát nghỉ tăng theo lực kéo tới cực đại μ<sub>n</sub>·N, thùng trượt thì ma sát tụt về μ<sub>t</sub>·N (đồ thị không ghi số). " + NOTE)


# ───────────── mặt phẳng nghiêng 5 m × 3 m dùng chung cho Dạng 4 và 6 ─────────────
OX, OY, S = 40, 190, 50
TH = math.degrees(math.atan2(3, 4)); TR = math.radians(TH)
TOPX, TOPY = OX + 4 * S, OY - 3 * S

def wp(lx, ly):
    """Toạ độ trong khung nghiêng (lx dọc dốc đi lên, ly<0 là phía trên mặt dốc) → toạ độ hình."""
    return OX + lx * math.cos(TR) + ly * math.sin(TR), OY - lx * math.sin(TR) + ly * math.cos(TR)

def incline(p, hlabel=True):
    b = tri([(OX, OY), (TOPX, OY), (TOPX, TOPY)], "currentColor", 2.8)
    b += arc(OX, OY, 34, 0, TH, RED, 1.8) + txt(OX + 40, OY - 8, "α", RED)
    mx, my = (OX + TOPX) / 2, (OY + TOPY) / 2
    b += txt(mx + 8, my + 30, "l = 5 m", BLUE, 13, "start")
    if hlabel:
        b += dim(p, "o", TOPX + 20, TOPY + 3, TOPX + 20, OY - 3, "", 0, 0) + txt(TOPX + 32, (TOPY + OY) / 2 + 4, "h = 3 m", ORG)
    return b


# ───────────── Dạng 4 · vật 10 kg trên dốc 5 m × 3 m có ma sát ─────────────
def d4(kk):
    p = f"d4{kk}"; X0, W, H = 30, 44, 30
    b = defs(p) + incline(p)
    if kk == 0:
        trav = 100
        ghost = R(X0, -H, W, H, sw=1.4, dash="5 4", op=.45)
        veh = R(X0, -H, W, H, sw=2.4) + seg(X0 + W, -H / 2, X0 + W + 46, -H / 2, RED, 2.8)
        b += f'<g transform="translate({OX} {OY}) rotate({-TH:.2f})">{ghost}{mover(trav, 0, 4, veh)}</g>'
        lx, ly = wp(X0 + W + 52, -H / 2 - 4)
        b += mover(trav * math.cos(TR), -trav * math.sin(TR), 4, txt(lx, ly - 6, "F = ?", RED))
        b += txt(300, 40, "m = 10 kg", "currentColor", 13) + txt(300, 62, "μ_n = 0,8", "currentColor", 13, "start", "400") + txt(300, 84, "μ_t = 0,6", "currentColor", 13, "start", "400")
        b += txt(300, 106, "g = 10 m/s²", "currentColor", 13, "start", "400")
        return fig("c4-0", "0 0 420 206", "Vật được kéo đều lên dốc dài năm mét, cao ba mét bằng dây song song mặt dốc",
                   b, "Mô phỏng: vật được kéo đều lên dốc bằng dây song song mặt dốc (tốc độ minh hoạ, chạy 4 s). Lực kéo F là đại lượng cần tìm.")
    lx, ly = X0 + 70, -H / 2
    cx, cy = wp(lx, ly)
    b += f'<g transform="translate({OX} {OY}) rotate({-TH:.2f})">{R(X0 + 70 - W / 2, -H, W, H, sw=2.4)}</g>'
    K = 0.6
    b += vec_luc("g", cx, cy, 0, 1, 100, K, 3)[0] + txt(cx + 8, cy + 100 * K + 6, "P", GRN)
    b += vec_luc("b", cx, cy, -math.cos(TR), math.sin(TR), 60, K, 2.4, "5 4")[0] + txt(cx - 60 * K * math.cos(TR) - 6, cy + 60 * K * math.sin(TR) + 14, "P∥", BLUE, 12, "end")
    b += vec_luc("o", cx, cy, math.sin(TR), math.cos(TR), 80, K, 2.4, "5 4")[0] + txt(cx + 80 * K * math.sin(TR) + 6, cy + 80 * K * math.cos(TR) + 6, "P⊥", ORG, 12)
    b += seg(cx - 60 * K * math.cos(TR), cy + 60 * K * math.sin(TR), cx, cy + 100 * K, GREY, 1.3, "3 4") + seg(cx + 80 * K * math.sin(TR), cy + 80 * K * math.cos(TR), cx, cy + 100 * K, GREY, 1.3, "3 4")
    b += txt(300, 40, "P∥ = P·sinα", BLUE, 13) + txt(300, 62, "P⊥ = P·cosα", ORG, 13) + txt(300, 84, "N = P⊥", "currentColor", 13, "start", "400")
    return fig("c4-2", "0 0 420 210", "Trọng lực P của vật trên dốc được phân tích thành thành phần dọc mặt dốc P song song và thành phần vuông góc mặt dốc P vuông góc",
               b, "Dữ kiện: dốc dài 5 m, cao 3 m nên sinα = 0,6 và cosα = 0,8; P phân tích theo hai phương dọc dốc và vuông góc dốc. " + NOTE)


# ───────────── Dạng 5 · thanh AB 2 kg, bản lề A, lực kế B, vật 3 kg ở C ─────────────
AX, BX, BY, SC = 40, 340, 132, 300

def beam_scene(p):
    b = seg(AX, BY, BX, BY, "currentColor", 7)
    b += R(AX - 22, BY - 40, 8, 90, "currentColor", 2.4) + tri([(AX, BY + 4), (AX - 12, BY + 22), (AX + 12, BY + 22)], "currentColor", 2.2) + circ(AX, BY, 4, "currentColor", 2, "currentColor")
    b += seg(BX - 40, 22, BX + 40, 22, "currentColor", 3) + seg(BX, 22, BX, 54, "currentColor", 2) + seg(BX, 96, BX, BY, "currentColor", 2)
    b += R(BX - 13, 54, 26, 42, "currentColor", 2.2)
    b += txt(AX + 8, BY - 14, "A", "currentColor", 13, "start") + txt(BX + 14, BY + 20, "B", "currentColor", 13)
    return b

def d5(kk):
    p = f"d5{kk}"; Xc = AX + SC * 0.8
    b = defs(p) + beam_scene(p)
    b += txt(Xc, BY - 14, "C", "currentColor", 13, "middle") + seg(Xc, BY - 8, Xc, BY - 4, "currentColor", 1.6)
    if kk == 0:
        x0 = AX + SC * 0.1; dur = 4
        F0, F1 = 10 + 30 * 0.1, 10 + 30 * 0.8
        y_of = lambda F: 58 + 34 * F / 50
        for i in range(1, 5):
            b += seg(BX - 13, 58 + 34 * i / 5, BX - 6, 58 + 34 * i / 5, "currentColor", 1.2, "", .6)
        b += (f'<line x1="{BX - 11}" y1="{y_of(F0):.1f}" x2="{BX + 11}" y2="{y_of(F0):.1f}" stroke="{RED}" stroke-width="3">'
              f'{smil("y1", [y_of(F0), y_of(F1)], dur)}{smil("y2", [y_of(F0), y_of(F1)], dur)}</line>')
        wt = seg(x0, BY + 4, x0, BY + 22, "currentColor", 2) + R(x0 - 15, BY + 22, 30, 26, sw=2.4) + txt(x0, BY + 40, "3 kg", "currentColor", 12, "middle")
        b += mover(SC * 0.7, 0, dur, wt)
        b += txt(16, 22, "thanh AB: 2 kg, dài 1 m", "currentColor", 13, "start", "400") + txt(16, 42, "g = 10 m/s²", "currentColor", 13, "start", "400")
        b += txt(BX - 22, 70, "F = ?", RED, 13, "end")
        b += dim(p, "b", AX, 214, Xc, 214, "", 0, 0) + txt((AX + Xc) / 2, 232, "AC = 0,8 m", BLUE, 13, "middle")
        return fig("c5-0", "0 0 420 244", "Thanh nằm ngang tựa bản lề ở A, treo vào lực kế ở B; vật 3 kg được dời dần từ gần A tới điểm C, kim lực kế dịch xuống",
                   b, "Mô phỏng: vật dời chậm từ gần A tới C (AC = 0,8 m), thanh luôn nằm ngang; kim lực kế dịch xuống dần (thang đo không ghi số). Chạy 4 s.")
    Xg = AX + SC * 0.5
    b += txt(Xg, BY - 14, "G", "currentColor", 13, "middle")
    b += vec_luc("g", Xg, BY, 0, 1, 20, 1.5, 3)[0] + txt(Xg + 8, BY + 38, "P_t", GRN)
    b += vec_luc("g", Xc, BY, 0, 1, 30, 1.5, 3)[0] + txt(Xc + 8, BY + 52, "P_v", GRN)
    b += txt(BX - 22, 70, "F = ?", RED, 13, "end") + txt(AX + 18, BY + 38, "R = ?", RED, 13, "start")
    for yy, x2, lab in ((190, Xg, "AG = 0,5 m"), (208, Xc, "AC = 0,8 m"), (226, BX, "AB = 1 m")):
        b += dim(p, "b", AX, yy, x2, yy, "", 0, 0) + txt(x2 + 8, yy + 4, lab, BLUE, 12)
    b += txt(16, 22, "Trục quay: bản lề A", "currentColor", 13, "start", "400") + txt(16, 42, "Σ moment đối với A = 0", "currentColor", 13, "start", "400")
    return fig("c5-2", "0 0 420 244", "Thanh AB chịu trọng lực của thanh ở trung điểm G, trọng lực của vật ở C, lực kéo của lực kế ở B và lực của bản lề ở A",
               b, "Dữ kiện: cánh tay đòn tính từ trục quay A; lực của lực kế và bản lề chưa biết nên chỉ ghi nhãn. " + NOTE)


# ───────────── Dạng 6 · vật 4 kg trên dốc 5 m × 3 m, lò xo k = 200 N/m, μ = 0,5 ─────────────
def d6(kk):
    p = f"d6{kk}"; W, H = 44, 32; XP = 232; ya = -16
    b = defs(p) + incline(p, hlabel=(kk == 0))
    peg = R(XP, -42, 6, 42, "currentColor", 2.4, "currentColor")
    if kk == 0:
        xv0, d = 88, 40
        spring = (f'<path d="{zig(xv0 + W, XP, ya)}" fill="none" stroke="{GRN}" stroke-width="2.4" stroke-linejoin="round">'
                  f'<animate attributeName="d" values="{zig(xv0 + W, XP, ya)};{zig(xv0 - d + W, XP, ya)}" dur="4s" begin="indefinite" fill="freeze"/></path>')
        ghost = R(xv0, -H, W, H, sw=1.4, dash="5 4", op=.45)
        veh = R(xv0, -H, W, H, sw=2.4) + txt(0, 0, "", "currentColor", 12)
        b += f'<g transform="translate({OX} {OY}) rotate({-TH:.2f})">{peg}{ghost}{spring}{mover(-d, 0, 4, veh)}</g>'
        b += txt(300, 40, "m = 4 kg", "currentColor", 13) + txt(300, 62, "k = 200 N/m", "currentColor", 13, "start", "400") + txt(300, 84, "μ = 0,5", "currentColor", 13, "start", "400")
        b += txt(300, 106, "g = 10 m/s²", "currentColor", 13, "start", "400")
        b += txt(300, 150, "Δl = 10 cm", ORG, 13) + txt(300, 170, "(ở cuối mô phỏng)", "currentColor", 12, "start", "400")
        return fig("c6-0", "0 0 420 206", "Vật được hạ chậm xuống dốc, lò xo nối với điểm cố định ở phía trên giãn dần rồi vật nằm yên",
                   b, "Mô phỏng: vật được hạ chậm xuống dốc, lò xo giãn dần tới 10 cm rồi vật nằm yên (độ giãn vẽ phóng đại). Chạy 4 s.")
    xv = 70
    cx, cy = wp(xv + W / 2, -H / 2)
    b += f'<g transform="translate({OX} {OY}) rotate({-TH:.2f})">{peg}{R(xv, -H, W, H, sw=2.4)}<path d="{zig(xv + W, XP, ya)}" fill="none" stroke="{GRN}" stroke-width="2.4" stroke-linejoin="round"/></g>'
    b += vec_luc("g", cx, cy, 0, 1, 40, 1.2, 3)[0] + txt(cx + 8, cy + 54, "P", GRN)
    b += txt(300, 40, "F_đh = k·Δl", GRN, 13) + txt(300, 62, "0 ≤ F_ms ≤ μ·N", ORG, 13) + txt(300, 90, "Hai biên:", "currentColor", 13, "start", "400")
    b += txt(300, 108, "sắp trượt xuống", "currentColor", 12, "start", "400") + txt(300, 126, "sắp trượt lên", "currentColor", 12, "start", "400")
    return fig("c6-2", "0 0 420 206", "Vật trên dốc nối với lò xo giãn có trục song song mặt dốc, đầu trên của lò xo cố định",
               b, "Dữ kiện: lò xo giãn kéo vật lên dốc; ma sát nghỉ ngược xu hướng trượt, tối đa μN. " + NOTE + " Độ giãn vẽ phóng đại.")


BUILD = [d1, d2, d3, d4, d5, d6]

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Tổng hợp hai lực đồng quy: cùng chiều, ngược chiều, vuông góc, hợp góc α",
      topic="Tổng hợp hai lực đồng quy",
      problem_html=r"""<p>Hai lực $\vec F_1$ và $\vec F_2$ cùng đặt vào một vật nhỏ, có độ lớn $F_1=30\ \text{N}$ và $F_2=40\ \text{N}$.</p><ol type="a"><li>Tính độ lớn hợp lực khi hai lực cùng phương, cùng chiều; rồi khi cùng phương, ngược chiều.</li><li>Tính độ lớn hợp lực khi hai lực vuông góc với nhau.</li><li>Hai lực khác có độ lớn $21\ \text{N}$ và $24\ \text{N}$ hợp với nhau góc $60^\circ$. Tính độ lớn hợp lực.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Cân bằng ba lực: vật treo bằng hai dây, lực căng và giới hạn đứt dây",
      topic="Điều kiện cân bằng của chất điểm",
      problem_html=r"""<p>Một chiếc đèn khối lượng $m=6\ \text{kg}$ được treo vào trần nhà bằng hai sợi dây nhẹ giống nhau. Hai dây đối xứng qua phương thẳng đứng, mỗi dây hợp với phương ngang góc $\theta$ với $\sin\theta=0{,}6$ và $\cos\theta=0{,}8$ (khi đó $\theta\approx37^\circ$). Lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Tính lực căng của mỗi dây.</li><li>Mỗi dây chịu được lực căng tối đa $55\ \text{N}$. Dây có bị đứt không? Muốn dây không đứt thì góc $\theta$ phải không nhỏ hơn bao nhiêu độ?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Ma sát nghỉ và ma sát trượt trên sàn ngang",
      topic="Lực ma sát nghỉ, ma sát trượt và hệ số ma sát",
      problem_html=r"""<p>Một thùng hàng khối lượng $m=50\ \text{kg}$ đặt trên sàn nằm ngang. Hệ số ma sát nghỉ cực đại giữa thùng và sàn là $\mu_n=0{,}4$, hệ số ma sát trượt là $\mu_t=0{,}3$. Người ta kéo thùng bằng lực $\vec F$ nằm ngang. Lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Khi $F=120\ \text{N}$, thùng có chuyển động không? Tính lực ma sát tác dụng lên thùng.</li><li>Lực kéo nhỏ nhất để thùng bắt đầu trượt là bao nhiêu (tính xấp xỉ, coi thùng bắt đầu trượt khi lực kéo vừa tới ma sát nghỉ cực đại)?</li><li>Khi thùng đã trượt, phải kéo bằng lực bao nhiêu để thùng trượt đều?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Mặt phẳng nghiêng có ma sát: đứng yên hay trượt, lực kéo đều, góc nghiêng giới hạn",
      topic="Vật trượt trên mặt phẳng nghiêng có ma sát",
      problem_html=r"""<p>Vật khối lượng $m=10\ \text{kg}$ đặt trên mặt phẳng nghiêng dài $5\ \text{m}$, cao $3\ \text{m}$ (khi đó $\sin\alpha=0{,}6$ và $\cos\alpha=0{,}8$). Hệ số ma sát nghỉ cực đại giữa vật và mặt phẳng nghiêng là $\mu_n=0{,}8$, hệ số ma sát trượt là $\mu_t=0{,}6$. Lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Thả nhẹ vật, vật có tự trượt xuống không? Tính lực ma sát tác dụng lên vật.</li><li>Tính lực kéo $F$ song song với mặt phẳng nghiêng, hướng lên, để kéo vật đi lên đều.</li><li>Nâng dần mặt phẳng nghiêng (giữ nguyên bề mặt). Vật bắt đầu trượt khi góc nghiêng đạt bao nhiêu độ (tính xấp xỉ, coi vật bắt đầu trượt khi ma sát nghỉ vừa đạt cực đại)?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Đòn bẩy: quy tắc moment với thanh có khối lượng và nhiều lực",
      topic="Moment lực và quy tắc moment",
      problem_html=r"""<p>Thanh AB đồng chất, tiết diện đều, dài $1\ \text{m}$, khối lượng $2\ \text{kg}$, nằm ngang. Đầu A tựa vào bản lề gắn vào tường (thanh quay tự do quanh A). Đầu B được giữ bằng một lực kế treo thẳng đứng. Một vật khối lượng $3\ \text{kg}$ được treo vào điểm C của thanh, với $AC=0{,}8\ \text{m}$. Lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Tính số chỉ của lực kế khi thanh nằm ngang.</li><li>Tính lực của bản lề tác dụng lên thanh tại A (độ lớn và chiều).</li><li>Thay lực kế bằng một lực kế khác chỉ đo được tối đa $28\ \text{N}$. Vật phải treo cách A tối đa bao nhiêu để lực kế không vượt thang đo?</li></ol>"""),
 dict(label="Dạng 6 · Nâng cao · Lực đàn hồi kết hợp ma sát nghỉ: khoảng độ giãn để vật nằm yên trên dốc",
      topic="Định luật Hooke và lực đàn hồi của lò xo",
      problem_html=r"""<p>Một vật khối lượng $m=4\ \text{kg}$ đặt trên mặt phẳng nghiêng dài $5\ \text{m}$, cao $3\ \text{m}$ (khi đó $\sin\alpha=0{,}6$ và $\cos\alpha=0{,}8$). Vật được nối với một lò xo nhẹ có độ cứng $k=200\ \text{N/m}$; trục lò xo song song với mặt phẳng nghiêng, đầu kia của lò xo cố định ở phía trên. Hệ số ma sát nghỉ cực đại giữa vật và mặt phẳng nghiêng là $\mu=0{,}5$. Lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Nếu không có lò xo, vật có nằm yên được trên mặt phẳng nghiêng không?</li><li>Với lò xo (đang giãn), vật nằm yên. Tìm độ giãn nhỏ nhất và lớn nhất của lò xo.</li><li>Khi lò xo giãn $10\ \text{cm}$, tính độ lớn lực ma sát tác dụng lên vật và cho biết chiều của nó.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 [(r'"hai lực … cùng đặt vào một vật nhỏ"', r"Hai lực đồng quy tại vật", r"⚠ Hợp lực chỉ có nghĩa khi hai lực cùng tác dụng lên một vật"),
  (r'"$F_1=30$ N và $F_2=40$ N"', r"$F_1=30$ N ; $F_2=40$ N", r"Lực là đại lượng vectơ : có độ lớn, phương, chiều"),
  (r'"cùng phương, cùng chiều … ngược chiều"', r"$\alpha=0^\circ$ rồi $\alpha=180^\circ$", r"Cùng chiều : $R=F_1+F_2$ ; ngược chiều : $R=|F_1-F_2|$"),
  (r'"vuông góc với nhau"', r"$\alpha=90^\circ$", r"Hợp lực là đường chéo hình chữ nhật : $R^2=F_1^2+F_2^2$"),
  (r'"hợp với nhau góc $60^\circ$"', r"$F_1=21$ N ; $F_2=24$ N ; $\alpha=60^\circ$", r"⚠ $\alpha$ là góc giữa hai vectơ vẽ cùng gốc : $R^2=F_1^2+F_2^2+2F_1F_2\cos\alpha$"),
  (r'"tính độ lớn hợp lực"', r"Cần $R$", r"Kiểm tra bằng $|F_1-F_2|\le R\le F_1+F_2$")],
 [(r'"đèn khối lượng $m=6$ kg"', r"$m=6$ kg", r"$P=10m$ ; trọng lực hướng xuống"),
  (r'"hai sợi dây nhẹ giống nhau, đối xứng"', r"Hai lực căng bằng nhau $T_1=T_2=T$", r"⚠ Dây nhẹ nên lực căng như nhau suốt dây ; đối xứng nên hai thành phần ngang triệt tiêu"),
  (r'"mỗi dây hợp với phương ngang góc $\theta$, $\sin\theta=0{,}6$"', r"$\sin\theta=0{,}6$ ; $\theta\approx37^\circ$ so với phương ngang", r"Thành phần đứng của lực căng là $T\sin\theta$ (góc đo với phương ngang)"),
  (r'"tính lực căng"', r"Cần $T$", r"Đèn đứng yên nên $\sum\vec F=0$ : $2T\sin\theta=P$"),
  (r'"chịu được lực căng tối đa $55$ N"', r"$T_{max}=55$ N", r"⚠ Giới hạn áp dụng cho từng dây ; dây đứt khi $T\gt T_{max}$"),
  (r'"$\theta$ không nhỏ hơn bao nhiêu độ"', r"Cần $\theta_{min}$", r"Cho $T=T_{max}$ : $\sin\theta_{min}=\dfrac{P}{2T_{max}}$")],
 [(r'"khối lượng $m=50$ kg … sàn nằm ngang"', r"$m=50$ kg ; sàn ngang", r"$P=10m$ ; ⚠ trên sàn ngang, không có lực thẳng đứng nào khác : $N=P$"),
  (r'"ma sát nghỉ cực đại $\mu_n=0{,}4$, ma sát trượt $\mu_t=0{,}3$"', r"$\mu_n=0{,}4$ ; $\mu_t=0{,}3$", r"$F_{msn,\max}=\mu_nN$ ; $F_{mst}=\mu_tN$ ; ⚠ ma sát nghỉ biến thiên từ $0$ đến $\mu_nN$, chỉ cực đại khi vật sắp trượt"),
  (r'"khi $F=120$ N, thùng có chuyển động không"', r"$F=120$ N", r"So $F$ với $F_{msn,\max}$ : nhỏ hơn thì thùng đứng yên và $F_{ms}=F$"),
  (r'"lực kéo nhỏ nhất để thùng bắt đầu trượt"', r"Cần $F_{min}$", r"Thùng trượt khi $F$ vượt ma sát nghỉ cực đại"),
  (r'"khi thùng đã trượt … trượt đều"', r"Hợp lực bằng 0", r"⚠ Đang trượt thì dùng ma sát trượt : $F=F_{mst}=\mu_tN$ (không dùng $\mu_n$)")],
 [(r'"mặt phẳng nghiêng dài $5$ m, cao $3$ m"', r"$l=5$ m ; $h=3$ m ; $\sin\alpha=0{,}6$ ; $\cos\alpha=0{,}8$", r"Phân tích $\vec P$ : $P_\parallel=P\sin\alpha$ (dọc dốc), $P_\perp=P\cos\alpha$ (vuông góc dốc)"),
  (r'"vật khối lượng $m=10$ kg"', r"$m=10$ kg", r"$P=10m$ ; phản lực $N=P\cos\alpha$"),
  (r'"$\mu_n=0{,}8$, $\mu_t=0{,}6$"', r"$\mu_n=0{,}8$ ; $\mu_t=0{,}6$", r"⚠ Hai hệ số dùng ở hai tình huống khác nhau : $\mu_nN$ khi sắp trượt, $\mu_tN$ khi đang trượt"),
  (r'"thả nhẹ vật, có tự trượt xuống không"', r"So $P_\parallel$ với $\mu_nN$", r"⚠ Đứng yên khi $P_\parallel\le\mu_nN$ ; lúc đó $F_{ms}=P_\parallel$ (không phải $\mu_nN$)"),
  (r'"kéo … đi lên đều"', r"Hợp lực bằng 0, vật trượt lên", r"⚠ Vật đi lên thì ma sát trượt hướng xuống dốc : $F=P_\parallel+\mu_tN$"),
  (r'"nâng dần … bắt đầu trượt"', r"Lúc vừa trượt : $P_\parallel=\mu_nN$", r"Suy ra $\tan\alpha=\mu_n$")],
 [(r'"thanh AB đồng chất … dài $1$ m, khối lượng $2$ kg"', r"$AB=1$ m ; $m_t=2$ kg", r"Trọng lực thanh đặt tại trung điểm G : $AG=\dfrac{AB}{2}$ ; $P_t=10m_t$"),
  (r'"đầu A tựa vào bản lề"', r"Trục quay qua A", r"⚠ Chọn trục quay tại A để moment của lực bản lề bằng 0 (cánh tay đòn bằng 0)"),
  (r'"đầu B được giữ bằng lực kế treo thẳng đứng"', r"Lực $\vec F$ vuông góc thanh tại B", r"$M_F=F\cdot AB$ (lực vuông góc thanh nên cánh tay đòn là $AB$)"),
  (r'"vật $3$ kg treo vào C, $AC=0{,}8$ m"', r"$m_v=3$ kg ; $AC=0{,}8$ m", r"$P_v=10m_v$ ; $M_v=P_v\cdot AC$"),
  (r'"thanh nằm ngang" (cân bằng)', r"Thanh cân bằng", r"⚠ Hai điều kiện : $\sum M=0$ (chọn trục A) và $\sum\vec F=0$ (để tìm lực bản lề)"),
  (r'"số chỉ của lực kế"', r"Cần $F$", r"$F\cdot AB=P_t\cdot AG+P_v\cdot AC$"),
  (r'"lực của bản lề"', r"Cần $R$", r"$R+F=P_t+P_v$"),
  (r'"lực kế đo tối đa $28$ N … vật cách A tối đa"', r"$F_{max}=28$ N ; cần $x$", r"$F_{max}\cdot AB=P_t\cdot AG+P_v\cdot x$")],
 [(r'"vật $4$ kg … mặt phẳng nghiêng dài $5$ m, cao $3$ m"', r"$m=4$ kg ; $\sin\alpha=0{,}6$ ; $\cos\alpha=0{,}8$", r"$P=10m$ ; $P_\parallel=P\sin\alpha$ ; $N=P\cos\alpha$"),
  (r'"hệ số ma sát nghỉ cực đại $\mu=0{,}5$"', r"$\mu=0{,}5$", r"$F_{msn,\max}=\mu N$ ; ⚠ ma sát nghỉ nằm trong $0\le F_{ms}\le\mu N$, ngược xu hướng trượt"),
  (r'"lò xo nhẹ, $k=200$ N/m, trục song song mặt phẳng nghiêng"', r"$k=200$ N/m", r"$F_{đh}=k\,\Delta l$ ($\Delta l$ đổi ra mét) ; lò xo giãn thì kéo vật về phía đầu cố định, tức lên dốc"),
  (r'"nếu không có lò xo"', r"Chỉ còn $P_\parallel$ và ma sát", r"⚠ Nằm yên chỉ khi $P_\parallel\le\mu N$ (hay $\tan\alpha\le\mu$)"),
  (r'"vật nằm yên … độ giãn nhỏ nhất và lớn nhất"', r"Hai trạng thái biên của ma sát nghỉ", r"⚠ Biên một : vật sắp trượt xuống ; biên hai : vật sắp trượt lên (ma sát nghỉ đạt cực đại, đổi chiều)"),
  (r'"lò xo giãn $10$ cm … lực ma sát"', r"$\Delta l=10$ cm", r"$F_{đh}=k\,\Delta l$ ; cân bằng dọc dốc : $F_{đh}+F_{ms}=P_\parallel$ nếu $F_{đh}\lt P_\parallel$")],
]

# ═════════════ LỜI GIẢI (mỗi bước một khối, mỗi công thức một dòng) ═════════════
R1 = [r"<strong>Khái niệm:</strong> hợp lực là một lực thay thế hai lực cùng tác dụng lên vật mà gây ra tác dụng như hai lực đó.",
      r"<strong>Quy tắc:</strong> hợp lực là đường chéo của hình bình hành dựng trên hai lực vẽ cùng gốc.",
      r"<strong>Công thức:</strong> $R^2=F_1^2+F_2^2+2F_1F_2\cos\alpha$ ($\alpha$ là góc giữa hai lực).",
      r"Trường hợp riêng : cùng chiều ($\alpha=0^\circ$), ngược chiều ($\alpha=180^\circ$), vuông góc ($\alpha=90^\circ$).",
      r"⚠ <strong>Điều kiện:</strong> hai lực cùng đặt vào một vật ; luôn có $|F_1-F_2|\le R\le F_1+F_2$."]
R2 = [r"<strong>Khái niệm:</strong> vật cân bằng khi đứng yên hoặc chuyển động thẳng đều ; khi đó hợp lực tác dụng lên vật bằng 0.",
      r"<strong>Điều kiện:</strong> $\sum\vec F=0$, tức tổng các thành phần theo mỗi phương bằng 0.",
      r"<strong>Công thức:</strong> lực căng $T$ có thành phần đứng $T\sin\theta$ và thành phần ngang $T\cos\theta$ ($\theta$ đo với phương ngang) ; $P=10m$.",
      r"⚠ <strong>Điều kiện:</strong> dây nhẹ nên lực căng hai đầu dây bằng nhau ; giới hạn đứt tính cho từng dây ; đổi góc đo thì sin và cos đổi chỗ (lý thuyết đo góc giữa hai dây hoặc với phương thẳng đứng thì dùng $\cos$ ; đề này đo với phương ngang nên dùng $\sin$)."]
R3 = [r"<strong>Khái niệm:</strong> ma sát nghỉ giữ vật đứng yên khi có lực kéo ; ma sát trượt xuất hiện khi vật đang trượt.",
      r"<strong>Công thức:</strong> ma sát nghỉ $0\le F_{msn}\le\mu_nN$ ; ma sát trượt $F_{mst}=\mu_tN$ ; thường $\mu_n\ge\mu_t$.",
      r"Trên sàn ngang, không có lực thẳng đứng nào khác : $N=P=10m$.",
      r"⚠ <strong>Điều kiện:</strong> chưa trượt thì $F_{msn}=F$ (không phải $\mu_nN$) ; đang trượt đều thì $F=F_{mst}$."]
R4 = [r"<strong>Khái niệm:</strong> trên mặt phẳng nghiêng, trọng lực $\vec P$ phân tích thành $P_\parallel=P\sin\alpha$ (dọc dốc) và $P_\perp=P\cos\alpha$ (vuông góc dốc).",
      r"Phản lực pháp tuyến $N=P\cos\alpha$ (không phải $N=P$).",
      r"<strong>Công thức:</strong> $F_{msn,\max}=\mu_nN$ ; $F_{mst}=\mu_tN$.",
      r"⚠ <strong>Điều kiện:</strong> vật nằm yên khi $P_\parallel\le\mu_nN$, tức $\tan\alpha\le\mu_n$ ; khi đó $F_{ms}=P_\parallel$.",
      r"Vật đi lên : ma sát trượt hướng xuống dốc. Vật đi xuống : ma sát hướng lên dốc."]
R5 = [r"<strong>Khái niệm:</strong> moment của lực đối với trục quay $M=F\,d$ ; $d$ là cánh tay đòn, khoảng cách từ trục quay tới đường tác dụng của lực.",
      r"<strong>Quy tắc moment:</strong> vật có trục quay cân bằng khi tổng moment làm vật quay thuận chiều kim đồng hồ bằng tổng moment làm vật quay ngược lại.",
      r"Thanh đồng chất : trọng lực đặt tại trung điểm. Cân bằng còn đòi $\sum\vec F=0$ để tìm lực của trục.",
      r"⚠ <strong>Điều kiện:</strong> chọn trục quay tại điểm có lực chưa biết (bản lề) để moment của lực đó bằng 0 ; cánh tay đòn đo vuông góc với đường tác dụng của lực."]
R6 = [r"<strong>Khái niệm:</strong> lực đàn hồi của lò xo chống lại biến dạng và tỉ lệ với độ biến dạng (định luật Hooke).",
      r"<strong>Công thức:</strong> $F_{đh}=k\,\Delta l$ ($\Delta l$ đổi ra mét) ; $P_\parallel=P\sin\alpha$ ; $N=P\cos\alpha$.",
      r"Ma sát nghỉ : $0\le F_{ms}\le\mu N$, ngược chiều xu hướng trượt.",
      r"⚠ <strong>Điều kiện:</strong> vật nằm yên khi các lực dọc dốc cân bằng ; hai biên của độ giãn ứng với lúc ma sát nghỉ đạt cực đại, một lần hướng lên dốc, một lần hướng xuống dốc."]

SOLS = [
 sol(R1, [
  ("Hai lực cùng chiều", [P(r"Cùng phương, cùng chiều ($\alpha=0^\circ$, $\cos\alpha=1$) : độ lớn cộng lại."), M(r"R=F_1+F_2=30+40"), A(r"R=70\ \text{N}")]),
  ("Hai lực ngược chiều", [P(r"Ngược chiều ($\alpha=180^\circ$, $\cos\alpha=-1$) : lấy hiệu hai độ lớn, hợp lực cùng chiều với lực lớn hơn."), M(r"R=F_2-F_1=40-30"), A(r"R=10\ \text{N}")]),
  ("Hai lực vuông góc", [P("Hợp lực là đường chéo của hình chữ nhật dựng trên hai lực :"), M(r"R=\sqrt{F_1^2+F_2^2}=\sqrt{30^2+40^2}=\sqrt{2500}"), A(r"R=50\ \text{N}")]),
  ("Hai lực hợp góc $60^\\circ$", [P(r"Dùng công thức tổng quát với $\cos60^\circ=0{,}5$ :"), M(r"R^2=21^2+24^2+2\cdot21\cdot24\cdot\cos60^\circ"), M(r"R^2=441+576+504=1521"), A(r"R=\sqrt{1521}=39\ \text{N}")]),
  ("Kiểm tra", [P(r"Với $30\ \text{N}$ và $40\ \text{N}$ : $10\ \text{N}\le R\le70\ \text{N}$ ; các kết quả $70$, $10$, $50\ \text{N}$ đều thoả."),
                P(r"Với $21\ \text{N}$ và $24\ \text{N}$ : $3\ \text{N}\le R\le45\ \text{N}$ ; $R=39\ \text{N}$ thoả.")])],
  [r"a) cùng chiều $R=70\ \text{N}$ ; ngược chiều $R=10\ \text{N}$", r"b) $R=50\ \text{N}$", r"c) $R=39\ \text{N}$"],
  r"Nhận dạng: <strong>hai lực cùng đặt vào một vật</strong> → hợp lực phụ thuộc góc giữa hai lực ; luôn kiểm tra $R$ nằm giữa $|F_1-F_2|$ và $F_1+F_2$."),
 sol(R2, [
  ("Trọng lượng của đèn", [M(r"P=10m=10\cdot6"), A(r"P=60\ \text{N}")]),
  ("Lực căng mỗi dây", [P("Đèn đứng yên nên hợp lực bằng 0. Hai thành phần ngang của lực căng bằng nhau và ngược chiều nên triệt tiêu ; theo phương thẳng đứng :"),
                        M(r"2T\sin\theta=P"), M(r"T=\dfrac{P}{2\sin\theta}=\dfrac{60}{2\cdot0{,}6}"), A(r"T=50\ \text{N}")]),
  ("Dây có đứt không?", [P("So lực căng vừa tìm với giới hạn của từng dây :"), M(r"T=50\ \text{N}\lt T_{max}=55\ \text{N}"), A("T:Dây không bị đứt."),
                             P(r"Lưu ý : trọng lượng $P=60\ \text{N}$ lớn hơn $55\ \text{N}$, nhưng mỗi dây chỉ chịu lực căng $T=50\ \text{N}$ của chính nó.")]),
  ("Góc nhỏ nhất để dây không đứt", [P(r"Cho lực căng bằng đúng giới hạn $T=T_{max}$ :"), M(r"\sin\theta_{min}=\dfrac{P}{2T_{max}}=\dfrac{60}{2\cdot55}\approx0{,}545"),
                                   A(r"\theta_{min}\approx33{,}1^\circ")]),
  ("Kiểm tra", [P(r"Với $\theta=33{,}1^\circ$ : $T=\dfrac{60}{2\cdot0{,}545}=55\ \text{N}$, đúng bằng giới hạn ✓ ; góc của đề ($36{,}9^\circ$) lớn hơn $33{,}1^\circ$ nên dây an toàn ✓"),
                P(r"Dây càng thoải thì lực căng càng lớn : với $\theta=60^\circ$ chỉ cần $T=\dfrac{60}{2\cdot0{,}866}\approx34{,}6\ \text{N}$.")])],
  [r"a) $T=50\ \text{N}$", r"b) dây không bị đứt ; $\theta\ge33{,}1^\circ$ (khoảng $33^\circ$)"],
  r"Nhận dạng: <strong>vật treo đứng yên bằng nhiều dây</strong> → $\sum\vec F=0$, chiếu lên phương thẳng đứng : $2T\sin\theta=P$ ($\theta$ đo với phương ngang)."),
 sol(R3, [
  ("Phản lực của sàn", [P("Thùng cân bằng theo phương thẳng đứng :"), M(r"N=P=10m=10\cdot50"), A(r"N=500\ \text{N}")]),
  ("Ma sát nghỉ cực đại (câu b)", [M(r"F_{msn,\max}=\mu_nN=0{,}4\cdot500"), A(r"F_{msn,\max}=200\ \text{N}"),
                                    P(r"Thùng bắt đầu trượt khi $F\gt200\ \text{N}$, tức lực kéo nhỏ nhất xấp xỉ $200\ \text{N}$.")]),
  ("Ma sát khi $F=120\\ \\text{N}$ (câu a)", [P(r"$F=120\ \text{N}\lt200\ \text{N}$ nên thùng đứng yên, ma sát nghỉ cân bằng với lực kéo :"), M(r"F_{ms}=F"), A(r"F_{ms}=120\ \text{N}")]),
  ("Kéo đều khi đang trượt (câu c)", [P("Thùng đã trượt nên dùng ma sát trượt. Trượt đều thì hợp lực bằng 0 :"), M(r"F=F_{mst}=\mu_tN=0{,}3\cdot500"), A(r"F=150\ \text{N}")]),
  ("Kiểm tra", [P(r"$F_{msn,\max}=200\ \text{N}\gt F_{mst}=150\ \text{N}$ : lúc bắt đầu trượt phải kéo mạnh hơn lúc đã trượt."),
                P(r"Nếu kéo $220\ \text{N}$ thì thùng trượt nhanh dần, nhưng ma sát vẫn là $\mu_tN=150\ \text{N}$ (không phụ thuộc $F$).")])],
  [r"a) thùng đứng yên, $F_{ms}=120\ \text{N}$", r"b) $F_{min}\approx200\ \text{N}$", r"c) $F=150\ \text{N}$"],
  r"Nhận dạng: <strong>ma sát nghỉ / bắt đầu trượt / trượt đều</strong> → chưa trượt : $F_{ms}=F$ ; sắp trượt : $\mu_nN$ ; đang trượt : $\mu_tN$."),
 sol(R4, [
  ("Thành phần trọng lực dọc dốc", [M(r"P=10m=100\ \text{N}"), M(r"P_\parallel=P\sin\alpha=100\cdot0{,}6"), A(r"P_\parallel=60\ \text{N}")]),
  ("Phản lực của mặt phẳng nghiêng", [P("Vuông góc mặt dốc vật cân bằng :"), M(r"N=P\cos\alpha=100\cdot0{,}8"), A(r"N=80\ \text{N}")]),
  ("Ma sát nghỉ cực đại", [M(r"F_{msn,\max}=\mu_nN=0{,}8\cdot80"), A(r"F_{msn,\max}=64\ \text{N}")]),
  ("Vật có trượt không? (câu a)", [P(r"$P_\parallel=60\ \text{N}\lt64\ \text{N}$ nên vật đứng yên. Ma sát nghỉ chỉ cần cân bằng $P_\parallel$, hướng lên dốc :"),
                                    M(r"F_{ms}=P_\parallel"), A(r"F_{ms}=60\ \text{N}")]),
  ("Lực kéo lên đều (câu b)", [P(r"Vật đi lên nên ma sát trượt hướng xuống dốc, cùng chiều $P_\parallel$. Hợp lực bằng 0 :"), M(r"F=P_\parallel+\mu_tN=60+0{,}6\cdot80"), A(r"F=108\ \text{N}")]),
  ("Góc nghiêng giới hạn (câu c)", [P(r"Vừa trượt khi $P\sin\alpha=\mu_nP\cos\alpha$ ; khối lượng triệt tiêu :"), M(r"\tan\alpha=\mu_n=0{,}8"), A(r"\alpha\approx38{,}7^\circ")]),
  ("Kiểm tra", [P(r"Đề cho $\tan\alpha=\dfrac{0{,}6}{0{,}8}=0{,}75\lt0{,}8=\mu_n$ nên vật đứng yên, khớp câu a ✓"),
                P(r"Dốc $\alpha=45^\circ$ ($\tan\alpha=1\gt0{,}8$) thì vật trượt ; góc $38{,}7^\circ$ lớn hơn góc của đề ($36{,}9^\circ$) ✓.")])],
  [r"a) vật đứng yên, $F_{ms}=60\ \text{N}$ (hướng lên dốc)", r"b) $F=108\ \text{N}$", r"c) $\alpha\approx38{,}7^\circ$"],
  r"Nhận dạng: <strong>vật trên dốc có ma sát</strong> → so $P_\parallel$ với $\mu_nN$ (hay $\tan\alpha$ với $\mu_n$) ; đi lên cộng $\mu_tN$, đi xuống trừ."),
 sol(R5, [
  ("Moment của trọng lực thanh", [P(r"Thanh đồng chất nên $G$ là trung điểm, $AG=0{,}5\ \text{m}$ ; $P_t=10\cdot2=20\ \text{N}$ :"), M(r"M_t=P_t\cdot AG=20\cdot0{,}5"), A(r"M_t=10\ \text{N·m}")]),
  ("Moment của trọng lực vật", [P(r"$P_v=10\cdot3=30\ \text{N}$ ; cánh tay đòn tính từ trục quay A đến C :"), M(r"M_v=P_v\cdot AC=30\cdot0{,}8"), A(r"M_v=24\ \text{N·m}")]),
  ("Số chỉ lực kế (câu a)", [P("Cân bằng moment đối với trục A (lực bản lề có cánh tay đòn bằng 0) :"), M(r"F\cdot AB=M_t+M_v=10+24"), M(r"F=\dfrac{34}{1}"), A(r"F=34\ \text{N}")]),
  ("Lực của bản lề (câu b)", [P("Cân bằng lực theo phương thẳng đứng, gọi $R$ là lực bản lề hướng lên :"), M(r"R+F=P_t+P_v"), M(r"R=20+30-34"), A(r"R=16\ \text{N}"), P("Dấu dương : lực bản lề hướng lên.")]),
  ("Vị trí tối đa của vật (câu c)", [P(r"Cho lực kế đạt giá trị lớn nhất $F_{max}=28\ \text{N}$, gọi $x$ là khoảng cách từ A tới vật :"), M(r"F_{max}\cdot AB=P_t\cdot AG+P_v\cdot x"), M(r"28=10+30x"), A(r"x=0{,}6\ \text{m}")]),
  ("Kiểm tra", [P(r"Moment đối với B : $R\cdot AB=P_t\cdot BG+P_v\cdot BC=20\cdot0{,}5+30\cdot0{,}2=16\ \text{N·m}$, khớp $R=16\ \text{N}$ ✓"),
                P(r"Vật càng xa A, lực kế càng lớn : ở A thì $F=10\ \text{N}$, ở B thì $F=40\ \text{N}$.")])],
  [r"a) $F=34\ \text{N}$", r"b) $R=16\ \text{N}$, hướng lên", r"c) $x_{max}=0{,}6\ \text{m}$"],
  r"Nhận dạng: <strong>thanh có khối lượng, bản lề, nhiều lực</strong> → chọn trục tại bản lề, viết $\sum M=0$ rồi $\sum\vec F=0$ để tìm lực bản lề."),
 sol(R6, [
  ("Thành phần trọng lực dọc dốc", [M(r"P=10m=40\ \text{N}"), M(r"P_\parallel=P\sin\alpha=40\cdot0{,}6"), A(r"P_\parallel=24\ \text{N}")]),
  ("Ma sát nghỉ cực đại", [P(r"$N=P\cos\alpha=40\cdot0{,}8=32\ \text{N}$ :"), M(r"F_{msn,\max}=\mu N=0{,}5\cdot32"), A(r"F_{msn,\max}=16\ \text{N}")]),
  ("Không lò xo, vật có nằm yên? (câu a)", [P(r"So $P_\parallel$ với ma sát nghỉ cực đại :"), M(r"P_\parallel=24\ \text{N}\gt F_{msn,\max}=16\ \text{N}"),
                                         A("T:Vật không nằm yên được, trượt xuống (cũng vì tanα = 0,75 lớn hơn μ = 0,5).")]),
  ("Độ giãn nhỏ nhất (câu b)", [P(r"Biên một : vật sắp trượt xuống, ma sát nghỉ cực đại hướng lên dốc cùng với lực đàn hồi giữ vật :"), M(r"F_{đh}+F_{msn,\max}=P_\parallel\Rightarrow F_{đh}=24-16=8\ \text{N}"),
                                M(r"\Delta l_{min}=\dfrac{F_{đh}}{k}=\dfrac{8}{200}=0{,}04\ \text{m}"), A(r"\Delta l_{min}=4\ \text{cm}")]),
  ("Độ giãn lớn nhất (câu b)", [P(r"Biên hai : vật sắp trượt lên, ma sát nghỉ cực đại hướng xuống dốc :"), M(r"F_{đh}=P_\parallel+F_{msn,\max}=24+16=40\ \text{N}"),
                               M(r"\Delta l_{max}=\dfrac{40}{200}=0{,}2\ \text{m}"), A(r"\Delta l_{max}=20\ \text{cm}")]),
  ("Ma sát khi $\\Delta l=10\\ \\text{cm}$ (câu c)", [M(r"F_{đh}=k\,\Delta l=200\cdot0{,}1=20\ \text{N}"), P(r"$F_{đh}=20\ \text{N}\lt P_\parallel=24\ \text{N}$ : lò xo chưa đủ giữ vật, ma sát nghỉ phải bù phần còn thiếu, hướng lên dốc :"),
                                                       M(r"F_{ms}=P_\parallel-F_{đh}=24-20"), A(r"F_{ms}=4\ \text{N}"), P("Dấu dương : ma sát nghỉ hướng lên dốc.")]),
  ("Kiểm tra", [P(r"$\Delta l=10\ \text{cm}$ nằm trong đoạn từ $4\ \text{cm}$ đến $20\ \text{cm}$ ✓"), P(r"$F_{ms}=4\ \text{N}\le F_{msn,\max}=16\ \text{N}$ nên vật nằm yên ✓")])],
  [r"a) vật không nằm yên được (trượt xuống)", r"b) $4\ \text{cm}\le\Delta l\le20\ \text{cm}$", r"c) $F_{ms}=4\ \text{N}$, hướng lên dốc"],
  r"Nhận dạng: <strong>lò xo + ma sát nghỉ + dốc, hỏi khoảng nằm yên</strong> → viết hai biên $F_{đh}=P_\parallel\mp\mu N$ rồi chia cho $k$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>hai lực cùng đặt vào một vật</b> → nghĩ tới <b>hợp lực</b> : cộng, trừ hay dùng cosα tuỳ góc giữa hai lực.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Hợp lực cùng chiều", "Hợp lực của hai lực cùng phương, cùng chiều?", 70, "N", 0.5,
       loi=r"Dùng căn bậc hai tổng bình phương cho mọi trường hợp — công thức đó chỉ đúng khi hai lực vuông góc."),
  buoc("Hợp lực ngược chiều", "Hợp lực của hai lực cùng phương, ngược chiều?", 10, "N", 0.5,
       loi=r"Cộng hai độ lớn như khi cùng chiều ; ngược chiều thì lực này triệt tiêu bớt lực kia.",
       ke=[(r"$R=|F_2-F_1|$ : ngược chiều thì lấy hiệu hai độ lớn", True),
           (r"$R=F_1+F_2$", r"Cộng độ lớn chỉ khi cùng chiều ; ngược chiều thì hai lực triệt tiêu bớt."),
           (r"$R=\sqrt{F_2^2-F_1^2}$", r"Không có quy tắc nào dùng căn của hiệu bình phương ; hai lực cùng phương thì chỉ cần lấy hiệu độ lớn.")]),
  buoc("Hợp lực vuông góc", "Hợp lực khi hai lực vuông góc?", 50, "N", 0.5,
       loi=r"Cộng thẳng độ lớn hai lực ; quên rằng hợp lực là đường chéo hình chữ nhật, ngắn hơn tổng.",
       ke=[(r"$R=\sqrt{F_1^2+F_2^2}$ (đường chéo hình chữ nhật)", True),
           (r"$R=F_1+F_2$", r"Cộng độ lớn chỉ khi cùng chiều. Hai lực vuông góc là hai cạnh, hợp lực là đường chéo nên ngắn hơn tổng."),
           (r"$R=|F_2-F_1|$", r"Hiệu độ lớn chỉ đúng khi hai lực ngược chiều.")]),
  buoc("Hợp lực khi hợp góc $60^\\circ$", "Độ lớn hợp lực của hai lực $21\\ \\text{N}$ và $24\\ \\text{N}$ hợp góc $60^\\circ$?", 39, "N", 0.5,
       loi=r"Dùng $R=\sqrt{F_1^2+F_2^2}$ (chỉ đúng khi vuông góc), hoặc viết dấu trừ trước số hạng $2F_1F_2\cos\alpha$.",
       ke=[(r"$R^2=F_1^2+F_2^2+2F_1F_2\cos\alpha$", True),
           (r"$R^2=F_1^2+F_2^2$", r"Công thức đó ứng với $\cos\alpha=0$, tức hai lực vuông góc ; ở đây $\alpha=60^\circ$."),
           (r"$R^2=F_1^2+F_2^2-2F_1F_2\cos\alpha$", r"Dấu trừ ứng với góc ngoài ; $\alpha$ là góc giữa hai vectơ cùng gốc, kiểm tra bằng $\alpha=0^\circ$ phải ra tổng $F_1+F_2$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>vật treo đứng yên bằng hai dây nghiêng</b> → nghĩ tới <b>ΣF = 0</b>, chiếu lên phương đứng : 2T·sinθ = P.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Trọng lượng của đèn", "Trọng lượng P của đèn?", 60, "N", 0.5,
       loi=r"Ghi $P=6\ \text{N}$ (lấy $P=m$, quên $g=10$) hoặc coi khối lượng là một lực."),
  buoc("Lực căng mỗi dây", "Lực căng T của mỗi dây?", 50, "N", 1,
       loi=r"Lấy $T=\dfrac{P}{2}$ vì tưởng hai dây chia đều trọng lượng mà quên góc nghiêng ; hoặc dùng cosθ thay cho sinθ. ⚠ Đổi quy ước góc : bài lý thuyết đo góc giữa hai dây (hay với phương thẳng đứng) nên dùng cos, còn đề này đo với phương ngang nên dùng sin.",
       ke=[(r"$2T\sin\theta=P$ : hai dây cùng đỡ đèn, góc đo với phương ngang", True),
           (r"$2T\cos\theta=P$", r"$\theta$ đo với phương ngang nên thành phần đứng của lực căng là $T\sin\theta$ ; $\cos\theta$ là thành phần ngang."),
           (r"$T=\dfrac{P}{2}$", r"Chỉ đúng khi hai dây thẳng đứng. Dây nghiêng thì mỗi dây phải căng hơn để thành phần đứng đủ đỡ đèn.")]),
  buoc("Dây có đứt không?", "Dây có bị đứt không?",
       loi=r"So trọng lượng đèn (thay vì lực căng) với giới hạn, hoặc cộng hai lực căng rồi so với giới hạn của một dây.",
       ke=[(r"So lực căng mỗi dây tìm được ở câu a với giới hạn $55\ \text{N}$", True),
           (r"So trọng lượng đèn với giới hạn $55\ \text{N}$", r"Mỗi dây chỉ chịu lực căng của chính nó, không chịu cả trọng lượng : $P=60\ \text{N}$ vượt $55\ \text{N}$ nhưng mỗi dây chỉ căng $50\ \text{N}$, nên so như vậy sẽ kết luận sai là dây đứt."),
           (r"Cộng hai lực căng rồi so với giới hạn $55\ \text{N}$", r"Giới hạn $55\ \text{N}$ áp dụng cho từng dây, không phải cho tổng hai dây ($2T=100\ \text{N}$ sẽ cho kết luận sai là dây đứt).")],
       lua_chon=[(r"Không : lực căng mỗi dây nhỏ hơn giới hạn", True),
                 (r"Có : lực căng mỗi dây vượt giới hạn", r"Lực căng tìm được ở câu a là $50\ \text{N}$, nhỏ hơn giới hạn $55\ \text{N}$ nên dây chưa đứt."),
                 (r"Chưa kết luận được vì không biết chiều dài dây", r"Lực căng chỉ phụ thuộc trọng lượng và góc nghiêng, không phụ thuộc chiều dài dây.")]),
  buoc("Góc nhỏ nhất để dây không đứt", "Góc θ nhỏ nhất để dây không đứt (độ)?", 33.1, "độ", 0.5,
       loi=r"Dùng $T_{max}\sin\theta=P$ (một dây chịu hết ; ra $\sin\theta\gt1$, vô lý) hoặc dùng cosθ — ra góc $57^\circ$ thay vì $33^\circ$.",
       ke=[(r"Cho $T=T_{max}$ trong $2T\sin\theta=P$ rồi tìm $\theta$", True),
           (r"$2T_{max}\cos\theta=P$", r"$\theta$ đo với phương ngang nên thành phần đứng là $T\sin\theta$."),
           (r"$T_{max}\sin\theta=P$", r"Có hai dây cùng đỡ đèn nên tổng thành phần đứng là $2T\sin\theta$ ; viết như vậy còn ra $\sin\theta=60/55\gt1$, vô lý.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>kéo thùng, hỏi lực để trượt / trượt đều</b> → phân biệt <b>μₙ, μₜ</b> ; chưa trượt thì F_ms = F.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Phản lực của sàn", "Phản lực N của sàn lên thùng?", 500, "N", 5,
       loi=r"Lấy $N=m=50$ (quên hệ số $g=10$)."),
  buoc("Ma sát nghỉ cực đại", "Lực ma sát nghỉ cực đại?", 200, "N", 2,
       loi=r"Dùng hệ số ma sát trượt $\mu_t$ thay cho $\mu_n$ ; hoặc nhân với trọng lượng thay vì phản lực (ở sàn ngang hai số trùng nhưng ý khác).",
       ke=[(r"$F_{msn,\max}=\mu_nN$", True),
           (r"$F_{msn,\max}=\mu_tN$", r"$\mu_t$ dùng khi thùng đã trượt ; lúc sắp trượt dùng hệ số ma sát nghỉ cực đại $\mu_n$."),
           (r"$F_{msn,\max}=F$", r"$F$ là lực kéo, còn ma sát nghỉ cực đại do bề mặt quyết định, không phụ thuộc lực kéo.")]),
  buoc("Ma sát khi thùng chưa trượt", "Lực ma sát tác dụng lên thùng ở câu a?", 120, "N", 1,
       loi=r"Ghi luôn $\mu_nN$ vì tưởng ma sát nghỉ luôn cực đại ; hoặc ghi $0$ vì thùng không chuyển động.",
       ke=[(r"Lực kéo nhỏ hơn ma sát nghỉ cực đại nên thùng đứng yên và $F_{ms}=F$", True),
           (r"$F_{ms}=\mu_nN$ vì ma sát nghỉ luôn bằng cực đại", r"Ma sát nghỉ chỉ đạt cực đại khi thùng sắp trượt ; còn nhỏ hơn thì chỉ cần cân bằng lực kéo."),
           (r"$F_{ms}=0$ vì thùng không chuyển động", r"Thùng đứng yên chính vì ma sát nghỉ cân bằng với lực kéo ; không có ma sát thì thùng đã bị kéo đi.")]),
  buoc("Kéo đều khi đang trượt", "Lực kéo F để thùng trượt đều?", 150, "N", 2,
       loi=r"Dùng $\mu_nN$ (đã đổi ra số lớn hơn) vì quên rằng khi đã trượt phải dùng hệ số ma sát trượt.",
       ke=[(r"Trượt đều thì $F=F_{mst}=\mu_tN$", True),
           (r"$F=F_{msn,\max}=\mu_nN$", r"Đó là lực cần để bắt đầu trượt ; khi đã trượt, ma sát giảm về $\mu_tN$."),
           (r"$F\gt\mu_tN$ để thùng chuyển động", r"Muốn trượt đều (vận tốc không đổi) hợp lực phải bằng 0 ; $F$ lớn hơn ma sát sẽ làm thùng nhanh dần.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>vật trên dốc có ma sát</b> → so <b>P∥ với μₙN</b> ; kéo lên đều thì ma sát hướng xuống dốc.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Thành phần trọng lực dọc dốc", "Thành phần trọng lực dọc mặt phẳng nghiêng $P_\\parallel$?", 60, "N", 0.5,
       loi=r"Dùng $P\cos\alpha$ (thành phần vuông góc) cho lực kéo vật xuống dốc, hoặc lấy cả $P$."),
  buoc("Phản lực của mặt phẳng nghiêng", "Phản lực N của mặt phẳng nghiêng?", 80, "N", 0.5,
       loi=r"Lấy $N=P$ như trên mặt ngang ; mặt phẳng nghiêng chỉ chịu thành phần vuông góc $P\cos\alpha$.",
       ke=[(r"$N=P\cos\alpha$", True),
           (r"$N=P$", r"Chỉ đúng khi mặt phẳng nằm ngang ; trên dốc chỉ thành phần vuông góc mặt dốc ép vào mặt phẳng."),
           (r"$N=P\sin\alpha$", r"$P\sin\alpha$ là thành phần dọc dốc, kéo vật xuống chứ không ép vào mặt phẳng.")]),
  buoc("Ma sát nghỉ cực đại", "Lực ma sát nghỉ cực đại?", 64, "N", 0.5,
       loi=r"Dùng $\mu_nP$ (áp lực là $N$, không phải $P$) hoặc dùng $\mu_t$.",
       ke=[(r"$F_{msn,\max}=\mu_nN$", True),
           (r"$F_{msn,\max}=\mu_nP$", r"Ma sát tỉ lệ với áp lực $N$ vuông góc mặt dốc, không phải với trọng lượng."),
           (r"$F_{msn,\max}=\mu_tN$", r"Lúc sắp trượt dùng hệ số ma sát nghỉ cực đại $\mu_n$.")]),
  buoc("Ma sát thực tế khi vật đứng yên", "Lực ma sát thực tế tác dụng lên vật (câu a)?", 60, "N", 0.5,
       loi=r"Ghi luôn ma sát nghỉ cực đại làm lực ma sát đang có ; ma sát nghỉ chỉ bằng đúng lực cần để cân bằng.",
       ke=[(r"Vật đứng yên nên $F_{ms}=P_\parallel$, miễn là $P_\parallel\le F_{msn,\max}$", True),
           (r"$F_{ms}=\mu_nN$", r"Đó chỉ là giá trị tối đa của ma sát nghỉ ; ma sát thực tế chỉ lớn bằng mức cần để vật đứng yên."),
           (r"$F_{ms}=\mu_tN$", r"Ma sát trượt chỉ có khi vật đang trượt, mà vật này đứng yên.")]),
  buoc("Lực kéo lên đều", "Lực kéo F song song dốc để kéo vật đi lên đều?", 108, "N", 1,
       loi=r"Trừ ma sát (cho rằng ma sát hướng lên) hoặc dùng $\mu_n$ thay cho $\mu_t$.",
       ke=[(r"$F=P_\parallel+\mu_tN$ (ma sát trượt hướng xuống dốc)", True),
           (r"$F=P_\parallel-\mu_tN$", r"Vật đi lên nên ma sát trượt hướng xuống, cùng chiều $P_\parallel$ ; phải cộng."),
           (r"$F=P_\parallel+\mu_nN$", r"Đang chuyển động đều dùng ma sát trượt $\mu_t$, không phải $\mu_n$.")]),
  buoc("Góc nghiêng giới hạn", "Góc nghiêng lớn nhất để vật còn đứng yên (độ)?", 38.7, "độ", 0.3,
       loi=r"Viết $\sin\alpha=\mu_n$ hoặc $\cos\alpha=\mu_n$ — quên chia hai vế cho $P\cos\alpha$.",
       ke=[(r"Lúc vừa trượt $P\sin\alpha=\mu_nP\cos\alpha$, suy ra $\tan\alpha=\mu_n$", True),
           (r"$\sin\alpha=\mu_n$", r"Đẳng thức $P\sin\alpha=\mu_nP\cos\alpha$ chia hai vế cho $P\cos\alpha$ cho $\tan\alpha=\mu_n$, không phải $\sin\alpha$."),
           (r"$\cos\alpha=\mu_n$", r"Chia hai vế cho $P\cos\alpha$ mới ra $\tan\alpha$ ; không có đẳng thức $\cos\alpha=\mu_n$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>thanh có khối lượng, bản lề, lực kế, vật treo</b> → chọn <b>trục tại bản lề</b>, ΣM = 0 rồi ΣF = 0.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Moment trọng lực thanh", "Moment của trọng lực thanh đối với trục quay tại A?", 10, "N·m", 0.2,
       loi=r"Lấy cánh tay đòn bằng cả chiều dài thanh thay vì tới trung điểm, hoặc bỏ qua khối lượng thanh."),
  buoc("Moment trọng lực vật", "Moment của trọng lực vật đối với trục tại A?", 24, "N·m", 0.5,
       loi=r"Dùng khối lượng (kg) thay cho trọng lượng, hoặc lấy cánh tay đòn $CB$ thay vì $AC$.",
       ke=[(r"$M_v=P_v\cdot AC$ (cánh tay đòn tính từ trục quay A)", True),
           (r"$M_v=P_v\cdot CB$", r"Cánh tay đòn tính từ trục quay A đến đường tác dụng của lực, không phải từ C đến B."),
           (r"$M_v=P_v\cdot AB$", r"$AB$ là chiều dài thanh ; vật treo ở C nên cánh tay đòn là $AC$.")]),
  buoc("Số chỉ lực kế", "Số chỉ F của lực kế?", 34, "N", 0.5,
       loi=r"Cộng thẳng trọng lượng thanh và vật (ra lực không đúng) vì quên rằng các lực ở xa trục phải tính theo moment ; hoặc quên moment của thanh.",
       ke=[(r"$F\cdot AB=M_t+M_v$ (cân bằng moment đối với A)", True),
           (r"$F=P_t+P_v$", r"Các lực đặt ở những điểm khác nhau nên không cộng thẳng được để cân bằng moment ; điều kiện cân bằng lực dùng để tìm lực bản lề."),
           (r"$F\cdot AB=M_v$", r"Thanh có khối lượng nên trọng lực thanh cũng tạo moment, không được bỏ.")]),
  buoc("Lực của bản lề", "Độ lớn lực của bản lề tác dụng lên thanh?", 16, "N", 0.5,
       loi=r"Cho rằng bản lề đỡ toàn bộ trọng lượng ; lực kế cũng kéo thanh lên nên bản lề chỉ đỡ phần còn lại.",
       ke=[(r"$R+F=P_t+P_v$ (cân bằng lực theo phương đứng)", True),
           (r"$R=P_t+P_v$", r"Lực kế cũng kéo thanh lên nên bản lề chỉ đỡ phần còn lại."),
           (r"$R=F$", r"Hai lực này không đối nhau : tổng lực lên phải bằng tổng trọng lượng của thanh và vật.")]),
  buoc("Vị trí tối đa của vật", "Khoảng cách tối đa x từ A tới vật để lực kế không vượt thang?", 0.6, "m", 0.01,
       loi=r"Quên moment của trọng lực thanh hoặc dùng $AB$ thay cho $x$ làm cánh tay đòn của vật.",
       ke=[(r"$F_{max}\cdot AB=M_t+P_v\cdot x$", True),
           (r"$F_{max}=P_v\cdot x$", r"Quên moment của trọng lực thanh và quên chia cho cánh tay đòn $AB$ của lực kế."),
           (r"$F_{max}\cdot x=M_t+P_v\cdot AB$", r"Cánh tay đòn của lực kế là $AB$, của vật là $x$ ; đổi chỗ sẽ sai.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>lò xo + ma sát nghỉ trên dốc, hỏi khoảng nằm yên</b> → viết hai biên <b>F_đh = P∥ ∓ μN</b> rồi chia k.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Thành phần trọng lực dọc dốc", "Thành phần trọng lực dọc mặt phẳng nghiêng?", 24, "N", 0.5,
       loi=r"Dùng $P\cos\alpha$ cho thành phần dọc dốc, hoặc quên hệ số $g=10$."),
  buoc("Ma sát nghỉ cực đại", "Lực ma sát nghỉ cực đại?", 16, "N", 0.5,
       loi=r"Dùng $\mu P$ thay cho $\mu N$ (áp lực lên dốc là $P\cos\alpha$).",
       ke=[(r"$F_{msn,\max}=\mu\,P\cos\alpha$", True),
           (r"$F_{msn,\max}=\mu\,P$", r"Áp lực lên mặt phẳng nghiêng là $P\cos\alpha$, không phải $P$."),
           (r"$F_{msn,\max}=\mu\,P\sin\alpha$", r"Thành phần dọc dốc không ép vật vào mặt phẳng nên không tạo ma sát.")]),
  buoc("Không lò xo, vật có nằm yên?", "Nếu không có lò xo, vật có nằm yên được không?",
       loi=r"Thấy có ma sát và $\mu\lt1$ nên kết luận vật đứng yên mà không so $P_\parallel$ với $\mu N$.",
       ke=[(r"So $P_\parallel$ với $F_{msn,\max}$", True),
           (r"Tính ngay độ giãn của lò xo", r"Câu này hỏi khi không có lò xo, chưa liên quan đến lò xo."),
           (r"Chỉ nhìn $\mu\lt1$ rồi kết luận", r"Hệ số ma sát nhỏ hơn $1$ chưa đủ để kết luận ; phải so thành phần dọc dốc với $\mu N$.")],
       lua_chon=[(r"Không : thành phần dọc dốc lớn hơn ma sát nghỉ cực đại, vật trượt xuống", True),
                 (r"Có : vì có ma sát nên vật luôn đứng yên", r"Ma sát nghỉ có giới hạn $\mu N$ ; vượt giới hạn thì vật vẫn trượt."),
                 (r"Có : vì $\mu$ nhỏ hơn $1$", r"Phải so $P_\parallel$ với $\mu N$ (hay $\tan\alpha$ với $\mu$) ; $\mu\lt1$ chưa kết luận được.")]),
  buoc("Độ giãn nhỏ nhất", "Độ giãn nhỏ nhất của lò xo (cm)?", 4, "cm", 0.1,
       loi=r"Bỏ qua ma sát nghỉ (cho lò xo đỡ cả $P_\parallel$) hoặc quên đổi mét ra xentimét.",
       ke=[(r"Vật sắp trượt xuống : $F_{đh}+F_{msn,\max}=P_\parallel$", True),
           (r"$F_{đh}=P_\parallel$", r"Bỏ qua ma sát nghỉ ; thực tế ma sát cũng giúp giữ vật nên lò xo không phải đỡ cả $P_\parallel$."),
           (r"$F_{đh}=P_\parallel+F_{msn,\max}$", r"Dấu cộng ứng với lúc vật sắp trượt lên (ma sát hướng xuống) — đó là biên lớn nhất, không phải nhỏ nhất.")]),
  buoc("Độ giãn lớn nhất", "Độ giãn lớn nhất của lò xo (cm)?", 20, "cm", 0.5,
       loi=r"Dùng chung một chiều ma sát cho cả hai biên ; biên lớn nhất cần ma sát hướng xuống dốc.",
       ke=[(r"Vật sắp trượt lên : $F_{đh}=P_\parallel+F_{msn,\max}$", True),
           (r"$F_{đh}=P_\parallel-F_{msn,\max}$", r"Đó là biên nhỏ nhất ; biên lớn nhất khi ma sát nghỉ cực đại hướng cùng chiều $P_\parallel$."),
           (r"$F_{đh}=\mu P$", r"Ma sát nghỉ không phải lực đàn hồi, và áp lực không phải $P$.")]),
  buoc("Ma sát khi lò xo giãn $10\\ \\text{cm}$", "Độ lớn lực ma sát nghỉ khi lò xo giãn $10\\ \\text{cm}$ (N)?", 4, "N", 0.2,
       loi=r"Ghi luôn $\mu N$ (ma sát cực đại) hoặc lấy ma sát bằng lực đàn hồi.",
       ke=[(r"$F_{đh}\lt P_\parallel$ nên ma sát nghỉ hướng lên dốc và bù phần thiếu", True),
           (r"$F_{ms}=\mu N$ vì ma sát nghỉ luôn đạt cực đại", r"Ma sát nghỉ chỉ lớn bằng mức cần để vật đứng yên, không phải lúc nào cũng cực đại."),
           (r"$F_{ms}=k\,\Delta l$", r"$k\,\Delta l$ là lực đàn hồi của lò xo, không phải lực ma sát.")]),
  buoc("Kiểm tra")]),
]


# ═════════════ BÀI TỰ LUẬN (dễ → khó, đã tự giải lại bằng Python) ═════════════
def L(*lines):
    return "".join(f"<p>{x}</p>" for x in lines)

# kiểm lại số liệu các bài tự luận
assert (9 + 12, 12 - 9, math.hypot(9, 12)) == (21, 3, 15)
assert abs(0.3 * 80 - 24) < 1e-9 and abs(80 * 0.25 - 20) < 1e-9 and 15 < 24
assert abs(4 / 0.04 - 100) < 1e-9 and abs(7 / 100 * 100 - 7) < 1e-9 and 20 + 7 == 27
assert 240 * 0.3 / 0.6 == 120 and abs((240 * 0.3 - 30 * 0.15) / 0.6 - 112.5) < 1e-9
assert abs(30 / 0.8 - 37.5) < 1e-9 and abs(30 * 0.75 - 22.5) < 1e-9
assert (200 * 0.6, 0.5 * 160, 120 - 80, 120 + 80) == (120, 80, 40, 200)
assert abs(0.75 * 200 / (0.8 + 0.75 * 0.6) - 120) < 1e-9 and abs(0.75 * 200 / (0.6 + 0.75 * 0.8) - 125) < 1e-9
Nt = 200 * 1.5 / 4; assert Nt == 75 and Nt / 200 == 0.375
Nt2 = (200 * 1.5 + 600 * 1.8) / 4; assert Nt2 == 345 and abs(Nt2 / 800 - 0.43125) < 1e-9

TL = [
 ("Dễ", L(r"Hai lực $9\ \text{N}$ và $12\ \text{N}$ cùng đặt vào một vật. Tính độ lớn hợp lực khi hai lực :", r"a) cùng phương, cùng chiều ;", r"b) cùng phương, ngược chiều ;", r"c) vuông góc với nhau."),
        L(r"a) $R=9+12=21\ \text{N}$.", r"b) $R=12-9=3\ \text{N}$.", r"c) $R=\sqrt{9^2+12^2}=\sqrt{225}=15\ \text{N}$.", r"Kiểm tra : $3\ \text{N}\le R\le21\ \text{N}$ ✓.")),
 ("Dễ", L(r"Một hộp khối lượng $8\ \text{kg}$ đặt trên sàn nằm ngang. Hệ số ma sát nghỉ cực đại là $0{,}3$, hệ số ma sát trượt là $0{,}25$. Lấy $g=10\ \text{m/s}^2$.", r"a) Đẩy hộp bằng lực nằm ngang $15\ \text{N}$ : hộp có trượt không ? Tính lực ma sát.", r"b) Tính lực đẩy nằm ngang nhỏ nhất để hộp bắt đầu trượt.", r"c) Tính lực đẩy ngang để hộp trượt đều."),
        L(r"$N=P=10\cdot8=80\ \text{N}$.", r"a) $F_{msn,\max}=0{,}3\cdot80=24\ \text{N}$ và $15\ \text{N}\lt24\ \text{N}$ : hộp đứng yên, $F_{ms}=15\ \text{N}$.", r"b) Hộp bắt đầu trượt khi lực đẩy vượt $24\ \text{N}$ nên lực đẩy nhỏ nhất xấp xỉ $24\ \text{N}$.", r"c) $F=F_{mst}=0{,}25\cdot80=20\ \text{N}$.")),
 ("Dễ", L(r"Một lò xo có chiều dài tự nhiên $20\ \text{cm}$. Treo vào lò xo một vật khối lượng $0{,}4\ \text{kg}$ thì lò xo dài $24\ \text{cm}$ (vật đứng yên). Lấy $g=10\ \text{m/s}^2$.", r"a) Tính độ cứng của lò xo.", r"b) Treo vật $0{,}7\ \text{kg}$ thì lò xo dài bao nhiêu ? (coi chưa vượt giới hạn đàn hồi)."),
        L(r"a) $\Delta l=24-20=4\ \text{cm}=0{,}04\ \text{m}$ ; $F_{đh}=P=10\cdot0{,}4=4\ \text{N}$ ; $k=\dfrac{F_{đh}}{\Delta l}=\dfrac{4}{0{,}04}=100\ \text{N/m}$.", r"b) $F_{đh}=10\cdot0{,}7=7\ \text{N}$ ; $\Delta l=\dfrac{7}{100}=0{,}07\ \text{m}=7\ \text{cm}$ ; chiều dài $20+7=27\ \text{cm}$.")),
 ("Trung bình", L(r"Một thanh AB đồng chất, dài $90\ \text{cm}$, khối lượng $3\ \text{kg}$, đặt trên điểm tựa O cách đầu A $30\ \text{cm}$. Treo vào A một vật khối lượng $24\ \text{kg}$. Cần tác dụng vào đầu B một lực $F$ hướng xuống, vuông góc với thanh, để thanh nằm ngang cân bằng. Lấy $g=10\ \text{m/s}^2$.", r"a) Tính $F$ nếu bỏ qua khối lượng thanh.", r"b) Tính $F$ khi kể đến khối lượng thanh."),
        L(r"Trọng lượng vật $P_v=240\ \text{N}$, cánh tay đòn $OA=0{,}3\ \text{m}$ ; $OB=0{,}6\ \text{m}$.", r"a) $F\cdot OB=P_v\cdot OA\Rightarrow F=\dfrac{240\cdot0{,}3}{0{,}6}=120\ \text{N}$.", r"b) Trọng tâm G cách A $45\ \text{cm}$ nên cách O $15\ \text{cm}$, về phía B ; $P_t=30\ \text{N}$.", r"$F\cdot OB+P_t\cdot OG=P_v\cdot OA\Rightarrow F\cdot0{,}6=72-30\cdot0{,}15=67{,}5$.", r"$F=\dfrac{67{,}5}{0{,}6}=112{,}5\ \text{N}$ (nhỏ hơn câu a vì trọng lực thanh cũng giúp quay về phía B).")),
 ("Trung bình", L(r"Một quả cầu khối lượng $3\ \text{kg}$ được treo vào tường thẳng đứng nhẵn bằng một sợi dây. Dây hợp với tường góc $\alpha$ có $\cos\alpha=0{,}8$ và $\tan\alpha=0{,}75$. Lấy $g=10\ \text{m/s}^2$. Tính lực căng dây và lực nén của quả cầu lên tường."),
        L(r"Quả cầu chịu ba lực : trọng lực $P=30\ \text{N}$, lực căng $T$ (dọc dây), phản lực $N$ của tường (vuông góc tường, tức nằm ngang).", r"Theo phương thẳng đứng : $T\cos\alpha=P\Rightarrow T=\dfrac{30}{0{,}8}=37{,}5\ \text{N}$.", r"Theo phương ngang : $N=T\sin\alpha=P\tan\alpha=30\cdot0{,}75=22{,}5\ \text{N}$.", r"Lực nén lên tường có độ lớn bằng $N$ (định luật III), tức $22{,}5\ \text{N}$.")),
 ("Khó", L(r"Vật khối lượng $20\ \text{kg}$ đặt trên mặt phẳng nghiêng dài $10\ \text{m}$, cao $6\ \text{m}$ (nên $\sin\alpha=0{,}6$ và $\cos\alpha=0{,}8$). Coi hệ số ma sát nghỉ cực đại và hệ số ma sát trượt cùng bằng $0{,}5$. Lấy $g=10\ \text{m/s}^2$.", r"a) Vật có tự đứng yên được không ?", r"b) Tính lực nhỏ nhất, song song mặt dốc và hướng lên, để giữ vật đứng yên.", r"c) Tính lực song song mặt dốc, hướng lên, để kéo vật đi lên đều."),
        L(r"$P=200\ \text{N}$ ; $P_\parallel=200\cdot0{,}6=120\ \text{N}$ ; $N=200\cdot0{,}8=160\ \text{N}$ ; $\mu N=0{,}5\cdot160=80\ \text{N}$.", r"a) $P_\parallel=120\ \text{N}\gt80\ \text{N}$ (cũng vì $\tan\alpha=0{,}75\gt0{,}5$) : vật không tự đứng yên.", r"b) Lực nhỏ nhất khi ma sát nghỉ cực đại hướng lên dốc : $F+80=120\Rightarrow F=40\ \text{N}$.", r"c) Đi lên đều, ma sát hướng xuống : $F=120+80=200\ \text{N}$.")),
 ("Khó", L(r"Một thùng khối lượng $20\ \text{kg}$ trên sàn nằm ngang, hệ số ma sát trượt $\mu=0{,}75$. Lấy $g=10\ \text{m/s}^2$. Kéo thùng trượt đều :", r"a) bằng lực nằm ngang ; tính lực kéo.", r"b) bằng lực hợp với phương ngang góc $\alpha$ hướng lên, với $\cos\alpha=0{,}8$ và $\sin\alpha=0{,}6$ ; tính lực kéo.", r"c) bằng lực hợp góc $\alpha$ với $\cos\alpha=0{,}6$ và $\sin\alpha=0{,}8$ ; tính lực kéo và so sánh ba kết quả."),
        L(r"$P=200\ \text{N}$.", r"a) $F=\mu P=0{,}75\cdot200=150\ \text{N}$.", r"b) Phản lực $N=P-F\sin\alpha$ ; trượt đều : $F\cos\alpha=\mu(P-F\sin\alpha)$, suy ra $F=\dfrac{\mu P}{\cos\alpha+\mu\sin\alpha}=\dfrac{150}{0{,}8+0{,}75\cdot0{,}6}=\dfrac{150}{1{,}25}=120\ \text{N}$.", r"c) $F=\dfrac{150}{0{,}6+0{,}75\cdot0{,}8}=\dfrac{150}{1{,}2}=125\ \text{N}$.", r"So sánh : $120\ \text{N}\lt125\ \text{N}\lt150\ \text{N}$. Kéo xiên lên thì lực nén của sàn giảm nên ma sát giảm ; lực kéo nhỏ nhất khi $\tan\alpha=\mu$ (đúng với câu b, $\tan\alpha=0{,}75$).")),
 ("Nâng cao", L(r"Thang AB đồng chất, dài $5\ \text{m}$, khối lượng $20\ \text{kg}$. Đầu A tựa vào tường thẳng đứng nhẵn, đầu B đặt trên sàn nằm ngang ; chân thang cách tường $3\ \text{m}$ (A cao $4\ \text{m}$). Lấy $g=10\ \text{m/s}^2$.", r"a) Tính phản lực của tường, lực ma sát nghỉ của sàn tác dụng lên thang và hệ số ma sát nghỉ tối thiểu của sàn để thang đứng yên.", r"b) Một người khối lượng $60\ \text{kg}$ leo lên điểm cách chân thang $3\ \text{m}$ (đo dọc thang). Tính lại hệ số ma sát nghỉ tối thiểu."),
        L(r"Lực tác dụng lên thang : trọng lực thang $P=200\ \text{N}$ tại trung điểm ; phản lực tường $N_t$ (nằm ngang, tại A) ; phản lực sàn $N_s$ (thẳng đứng) và ma sát nghỉ $F_{ms}$ (nằm ngang) tại B.", r"Chọn trục quay tại B để loại $N_s$ và $F_{ms}$. Khoảng cách ngang từ B tới điểm cách B một đoạn $s$ dọc thang là $0{,}6s$ ; độ cao của A là $4\ \text{m}$.", r"a) Trọng tâm cách B $2{,}5\ \text{m}$ nên cánh tay đòn ngang $1{,}5\ \text{m}$ : $N_t\cdot4=200\cdot1{,}5\Rightarrow N_t=75\ \text{N}$.", r"Theo phương ngang : $F_{ms}=N_t=75\ \text{N}$ ; theo phương đứng : $N_s=P=200\ \text{N}$ ; $\mu_{min}=\dfrac{75}{200}=0{,}375$.", r"b) Người cách B $3\ \text{m}$ nên cánh tay đòn ngang $1{,}8\ \text{m}$ ; trọng lượng người $600\ \text{N}$ : $N_t\cdot4=200\cdot1{,}5+600\cdot1{,}8=1380\Rightarrow N_t=345\ \text{N}$.", r"$F_{ms}=345\ \text{N}$ ; $N_s=200+600=800\ \text{N}$ ; $\mu_{min}=\dfrac{345}{800}\approx0{,}43$ (người leo càng cao thì càng dễ trượt).")),
]

def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>" + "".join(parts))

# ═════════════ GHI FILE ═════════════
write(J, 155, "Chuyên đề 10. Lực: tổng hợp lực, cân bằng, ma sát, đòn bẩy", DANG, BUILD, ANALYSIS, SOLS, tu_luan())
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "Soạn 10/10/2026; đã tự giải lại bằng Python (assert trong build). Chờ kiểm chéo độc lập (kiem-code) rồi đặt checked=true."}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
