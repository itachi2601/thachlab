"""Hình cho bài tập mẫu Bài 13 "Tổng hợp và phân tích lực. Cân bằng lực" (Vật lí 10), lesson_id 58.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Quy tắc vectơ lực (thầy chốt 10/10/2026): đầu mũi tên chữ V 30°, độ dài = k·F với MỘT hệ số k cho cả hình (vec_luc), không marker.
KHÔNG vẽ hợp lực, thành phần, lực căng hay bất kỳ vectơ nào là đáp án; lực căng chỉ ghi "= ?" trên dây.
Mô phỏng: D1/D2 quay lực F₂ quanh O (không vẽ hợp lực); D3/D5 lực đề cho tăng dần từ 15 % lên đủ; D4 nâng dốc 0→40°;
D6 đèn thả vào giữa dây, dao động tắt dần rồi đứng yên ở đúng độ võng của đề."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import vec_luc, chevron, field_line

GREY = "#94a3b8"
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}
NOTE = "Hình minh hoạ."


def rad(a):
    return math.radians(a)


def an(attr, vals, dur, nd=1):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def vec_anim(c, tails, tips, step, w=3.0):
    """Vectơ lực chạy theo các mẫu (đuôi, ngọn) cách đều `step` giây: đường thẳng + đầu V 30° (path trượt theo)."""
    col = COL[c]
    ww = min(w, 2.8)
    n = len(tips)
    dur = step * (n - 1)
    lens = [math.hypot(t[0] - s[0], t[1] - s[1]) for s, t in zip(tails, tips)]
    L = max(5, min(3.4 * ww + 2, 0.6 * min(lens)))
    ds = [re.search(r'd="([^"]+)"', chevron(t[0], t[1], t[0] - s[0], t[1] - s[1], col, ww, L)).group(1) for s, t in zip(tails, tips)]
    const_tail = all(abs(s[0] - tails[0][0]) < 1e-9 and abs(s[1] - tails[0][1]) < 1e-9 for s in tails)
    line = (f'<line x1="{tails[0][0]:.1f}" y1="{tails[0][1]:.1f}" x2="{tips[0][0]:.1f}" y2="{tips[0][1]:.1f}" '
            f'stroke="{col}" stroke-width="{ww}">')
    if not const_tail:
        line += an("x1", [s[0] for s in tails], dur) + an("y1", [s[1] for s in tails], dur)
    line += an("x2", [t[0] for t in tips], dur) + an("y2", [t[1] for t in tips], dur) + "</line>"
    path = (f'<path d="{ds[0]}" fill="none" stroke="{col}" stroke-width="{ww}" stroke-linejoin="miter" stroke-miterlimit="10" '
            f'stroke-linecap="butt"><animate attributeName="d" values="{";".join(ds)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></path>')
    return line + path


def ramp(x, y, ang, F, k, n=14, hold=6):
    """Ngọn vectơ tăng từ 15 % tới đủ k·F theo hướng ang (độ, Oy lên), rồi giữ."""
    dx, dy = math.cos(rad(ang)), -math.sin(rad(ang))
    full = k * F
    tips = [(x + dx * full * (0.15 + 0.85 * i / (n - 1)), y + dy * full * (0.15 + 0.85 * i / (n - 1))) for i in range(n)]
    tips += [tips[-1]] * hold
    assert abs(math.hypot(tips[-1][0] - x, tips[-1][1] - y) - full) < 0.05
    return tips


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: base_sb tail."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


def ring(x, y, r=6):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="currentColor" stroke-width="2"/>'


def hatch(x0, y0, x1, y1, n=8):
    """Tường (đoạn thẳng đứng, vạch hướng sang trái) hoặc trần (đoạn nằm ngang, vạch hướng lên)."""
    out = seg(x0, y0, x1, y1, "currentColor", 2.4)
    for i in range(n + 1):
        px, py = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n
        out += seg(px, py, px - 8, py + 8, "currentColor", 1.2, "", .7) if x0 == x1 else seg(px, py, px + 8, py - 8, "currentColor", 1.2, "", .7)
    return out


def sweep(poses, hold, step_deg):
    seq = [poses[0]] * hold
    a = poses[0]
    for p in poses[1:]:
        n = max(1, int(round(abs(p - a) / step_deg)))
        seq += [a + (p - a) * i / n for i in range(1, n + 1)]
        seq += [p] * hold
        a = p
    return seq


# ───────────── Dạng 1: F1 = 5,0 N, F2 = 12 N, α = 0°, 180°, 90°, 60° ─────────────
def d1(kk):
    O = (150, 160); k = 8.0; F1, F2 = 5.0, 12.0
    s1, _ = vec_luc("b", O[0], O[1], 1, 0, F1, k)
    b = ""
    if kk == 0:
        for a, lab, anch, dxl, dyl in ((0, "α = 0°", "start", 6, 4), (60, "α = 60°", "start", 6, -2), (90, "α = 90°", "start", 6, -2), (180, "α = 180°", "middle", 0, 18)):
            ex, ey = O[0] + 112 * math.cos(rad(a)), O[1] - 112 * math.sin(rad(a))
            b += seg(O[0], O[1], ex, ey, GREY, 1.2, "4 4", .8) + lbl(ex + dxl, ey + dyl, lab, GREY, 12, anch, "600")
        angs = sweep([0, 60, 90, 180], 4, 5)
        tips = [(O[0] + k * F2 * math.cos(rad(a)), O[1] - k * F2 * math.sin(rad(a))) for a in angs]
        b += s1 + vec_anim("o", [O] * len(tips), tips, 0.15) + ring(*O)
    else:
        a = 60
        tip = (O[0] + k * F2 * math.cos(rad(a)), O[1] - k * F2 * math.sin(rad(a)))
        s2, _ = vec_luc("o", O[0], O[1], math.cos(rad(a)), -math.sin(rad(a)), F2, k)
        b += s1 + s2 + ring(*O) + arc(O[0], O[1], 28, 0, a, RED) + lbl(O[0] + 34, O[1] - 16, "α", RED, 14, "start", "700")
    b += lbl(O[0] - 12, O[1] + 20, "O", "currentColor", 13, "end", "700")
    b += ts(290, 48, "F", "1", " = 5,0 N", BLUE) + ts(290, 70, "F", "2", " = 12 N", ORG) + lbl(290, 94, "Hợp lực F = ?", "currentColor", 13, "start", "700")
    if kk == 0:
        return fig("d1-0", "0 0 420 196", "Vòng nhẫn O chịu hai lực: F1 nằm ngang, F2 quay quanh O qua các góc 0, 60, 90 và 180 độ", b,
                   "Mô phỏng: hai lực vẽ cùng tỉ lệ (1 N ứng với 8 px). F₂ quay quanh O qua bốn vị trí của đề, dừng ở mỗi vị trí (khoảng 8 s). Không vẽ hợp lực.")
    return fig("d1-2", "0 0 420 196", "Hai lực F1 và F2 chung gốc O hợp nhau góc alpha", b,
               "Dữ kiện: hai lực chung gốc O, vẽ cùng tỉ lệ (1 N ứng với 8 px); đang vẽ α = 60° (ý d). Không dựng hình bình hành.")


# ───────────── Dạng 2: F1 = 7,0 N, F2 = 15 N, F = 20 N → α = ? ─────────────
def d2(kk):
    O = (110, 160); k = 6.0; F1, F2 = 7.0, 15.0
    s1, _ = vec_luc("b", O[0], O[1], 1, 0, F1, k)
    b = ""
    if kk == 0:
        R = k * F2
        b += f'<path d="M{O[0] + R:.1f},{O[1]:.1f} A{R:.1f},{R:.1f} 0 0 0 {O[0] - R:.1f},{O[1]:.1f}" fill="none" stroke="{GREY}" stroke-width="1.2" stroke-dasharray="4 4"/>'
        angs = [5 * i for i in range(0, 37)] + [180] * 4
        tips = [(O[0] + R * math.cos(rad(a)), O[1] - R * math.sin(rad(a))) for a in angs]
        b += s1 + vec_anim("o", [O] * len(tips), tips, 0.18) + ring(*O)
        b += lbl(O[0] + 4, O[1] + 30, "α tăng dần từ 0° đến 180°", GREY, 12, "start", "600")
    else:
        a = 120
        s2, _ = vec_luc("o", O[0], O[1], math.cos(rad(a)), -math.sin(rad(a)), F2, k)
        b += s1 + s2 + ring(*O) + arc(O[0], O[1], 24, 0, a, RED) + lbl(O[0] + 20, O[1] - 30, "α = ?", RED, 13, "start", "700")
    b += lbl(O[0] - 12, O[1] + 20, "O", "currentColor", 13, "end", "700")
    b += ts(290, 48, "F", "1", " = 7,0 N", BLUE) + ts(290, 70, "F", "2", " = 15 N", ORG) + lbl(290, 94, "Hợp lực F = 20 N", "currentColor", 13, "start", "700")
    if kk == 0:
        return fig("d2-0", "0 0 420 196", "Vòng quay F2 quanh điểm O từ hướng cùng chiều F1 đến hướng ngược chiều F1", b,
                   "Mô phỏng: hai lực vẽ cùng tỉ lệ (1 N ứng với 6 px). F₂ quay đều quanh O từ 0° đến 180° (khoảng 7 s). Góc cần tìm không được đánh dấu và không vẽ hợp lực.")
    return fig("d2-2", "0 0 420 196", "Hai lực F1 và F2 chung gốc O hợp nhau góc alpha chưa biết", b,
               "Dữ kiện: hai lực chung gốc O, vẽ cùng tỉ lệ (1 N ứng với 6 px). Góc vẽ chỉ để đặt tên α, không phải đáp số.")


# ───────────── Dạng 3: kéo thùng, dây hợp ngang 40°, F = 45 N ─────────────
def d3(kk):
    gy = 170; R = (200, 148); k = 2.4; F = 45.0; a = 40
    b = ground(gy, 16, 410) + f'<rect x="130" y="126" width="70" height="44" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    H = (R[0] + 160 * math.cos(rad(a)), R[1] - 160 * math.sin(rad(a)))
    b += seg(R[0], R[1], H[0], H[1], "currentColor", 1.4, "", .8) + f'<circle cx="{H[0]:.1f}" cy="{H[1]:.1f}" r="5" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    b += lbl(H[0] + 9, H[1] + 4, "tay", "currentColor", 12, "start", "400")
    b += seg(R[0], R[1], R[0] + 124, R[1], GREY, 1.2, "4 4", .8) + arc(R[0], R[1], 40, 0, a, RED) + lbl(R[0] + 48, R[1] - 8, "α = 40°", RED, 13, "start", "700")
    tip = (R[0] + k * F * math.cos(rad(a)), R[1] - k * F * math.sin(rad(a)))
    b += lbl(tip[0] - 12, tip[1] - 6, "F = 45 N", ORG, 13, "end", "700") + lbl(165, 193, "thùng", "currentColor", 12, "middle", "400")
    if kk == 0:
        tips = ramp(R[0], R[1], a, F, k)
        b += vec_anim("o", [R] * len(tips), tips, 0.22)
        return fig("d3-0", "0 0 420 200", "Một bạn kéo thùng trên sàn bằng dây hợp với phương ngang góc 40 độ", b,
                   "Mô phỏng: lực kéo tăng dần từ 15 % lên đủ 45 N (khoảng 4 s), vẽ theo tỉ lệ 1 N ứng với 2,4 px. Thùng đứng yên trong hình minh hoạ.")
    s, _ = vec_luc("o", R[0], R[1], math.cos(rad(a)), -math.sin(rad(a)), F, k)
    b += s + field_line(R[0], R[1], R[0] + 90, R[1], GRN, 1.6, "5 4", 10) + lbl(R[0] + 94, R[1] + 5, "Ox", GRN, 13, "start", "700")
    b += field_line(R[0], R[1], R[0], R[1] - 98, GRN, 1.6, "5 4", 10) + lbl(R[0] + 5, R[1] - 100, "Oy", GRN, 13, "start", "700")
    return fig("d3-2", "0 0 420 200", "Lực kéo F hợp với trục Ox nằm ngang góc 40 độ; trục Oy thẳng đứng hướng lên", b,
               "Dữ kiện: hai trục vuông góc Ox (ngang), Oy (đứng lên) đặt tại điểm buộc dây; lực F vẽ theo tỉ lệ 1 N ứng với 2,4 px. Chưa vẽ thành phần nào.")


# ───────────── Dạng 4: thùng trên dốc nghiêng 40°, trọng lực P ─────────────
PV = (50, 200)
C0 = (180, 175)          # tâm thùng khi dốc nằm ngang


def d4_centre(th):
    dx, dy = C0[0] - PV[0], C0[1] - PV[1]
    ca, sa = math.cos(rad(-th)), math.sin(rad(-th))
    return (PV[0] + dx * ca - dy * sa, PV[1] + dx * sa + dy * ca)


def d4(kk):
    k = 1.2; P = 80.0; th = 40
    body = (f'<rect x="50" y="192" width="250" height="8" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            f'<rect x="150" y="158" width="60" height="34" fill="none" stroke="currentColor" stroke-width="2.2"/>')
    b = seg(16, 200, 410, 200, "currentColor", 2) + dot(*PV, 4.5, "currentColor")
    if kk == 0:
        ths = [2 * i for i in range(0, 21)] + [th] * 6
        step = 0.15; dur = step * (len(ths) - 1)
        vals = ";".join(f"{-t} {PV[0]} {PV[1]}" for t in ths)
        b += f'<g>{body}<animateTransform attributeName="transform" type="rotate" values="{vals}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></g>'
        tails = [d4_centre(t) for t in ths]
        tips = [(c[0], c[1] + k * P) for c in tails]
        b += vec_anim("r", tails, tips, step)
        op = [0] * (len(ths) - 8) + [0, 0.3, 0.6, 1, 1, 1, 1, 1]
        b += (f'<g opacity="0">{arc(PV[0], PV[1], 60, 0, th, RED)}{lbl(PV[0] + 66, PV[1] + 22, "α = 40°", RED, 13, "start", "700")}'
              f'{an("opacity", op[:len(ths)], dur, 1)}</g>')
        return fig("d4-0", "0 0 420 232", "Thùng nằm trên mặt dốc được nâng dần từ nằm ngang đến nghiêng 40 độ; mũi tên trọng lực luôn thẳng đứng xuống", b,
                   "Mô phỏng: mặt dốc nâng dần từ 0° đến 40° (khoảng 4 s), thùng nằm yên nhờ ma sát đủ lớn; trọng lực vẽ thẳng đứng xuống. Chưa vẽ thành phần nào.")
    C = d4_centre(th)
    b += f'<g transform="rotate({-th} {PV[0]} {PV[1]})">{body}</g>'
    s, tip = vec_luc("r", C[0], C[1], 0, 1, P, k)
    ux, uy = math.cos(rad(th)), -math.sin(rad(th))
    nx, ny = -math.sin(rad(th)), -math.cos(rad(th))
    b += s + lbl(tip[0] + 8, tip[1] - 2, "P = mg", RED, 13, "start", "700")
    b += field_line(C[0], C[1], C[0] + 70 * ux, C[1] + 70 * uy, GRN, 1.6, "5 4", 10) + lbl(C[0] + 70 * ux + 6, C[1] + 70 * uy - 4, "Ox", GRN, 13, "start", "700")
    b += field_line(C[0], C[1], C[0] + 70 * nx, C[1] + 70 * ny, GRN, 1.6, "5 4", 10) + lbl(C[0] + 70 * nx - 6, C[1] + 70 * ny - 4, "Oy", GRN, 13, "end", "700")
    b += arc(PV[0], PV[1], 60, 0, th, RED) + lbl(PV[0] + 66, PV[1] + 22, "α = 40°", RED, 13, "start", "700")
    return fig("d4-2", "0 0 420 232", "Thùng trên dốc nghiêng 40 độ với hai trục: Ox dọc mặt dốc, Oy vuông góc mặt dốc; trọng lực P thẳng đứng xuống", b,
               "Dữ kiện: hai trục vuông góc đặt tại tâm thùng (Ox dọc dốc, Oy vuông góc dốc); trọng lực vẽ thẳng đứng xuống, chưa vẽ thành phần nào.")


# ───────────── Dạng 5: vòng nhẫn O, vật 3,0 kg, OA ngang, OB hợp thẳng đứng 30° ─────────────
def d5(kk):
    O = (190, 130); k = 2.0; P = 30.0; beta = 30
    lenOB = (O[1] - 30) / math.cos(rad(beta))
    B = (O[0] + lenOB * math.sin(rad(beta)), 30.0)
    A = (40.0, O[1])
    b = hatch(A[0], 70, A[0], 200, 8) + hatch(150, 30, 340, 30, 10)
    b += seg(A[0], A[1], O[0], O[1], "currentColor", 2.4) + seg(O[0], O[1], B[0], B[1], "currentColor", 2.4)
    b += seg(O[0], O[1], O[0], 192, "currentColor", 1.4, "", .8)
    b += f'<rect x="165" y="192" width="50" height="34" fill="none" stroke="currentColor" stroke-width="2.2"/>' + lbl(190, 214, "3,0 kg", "currentColor", 12, "middle", "600")
    b += seg(O[0], O[1], O[0], O[1] - 62, GREY, 1.2, "4 4", .8) + arc(O[0], O[1], 54, 90 - beta, 90, RED) + lbl(O[0] - 6, O[1] - 44, "30°", RED, 13, "end", "700")
    b += ts(52, O[1] - 8, "T", "OA", " = ?", ORG, 13, "start") + ts(O[0] + 48, 86, "T", "OB", " = ?", ORG, 13, "start")
    b += lbl(O[0] - 12, O[1] + 20, "O", "currentColor", 13, "end", "700") + lbl(A[0] + 8, O[1] + 18, "A", "currentColor", 13, "start", "700") + lbl(B[0] + 8, B[1] + 18, "B", "currentColor", 13, "start", "700")
    if kk == 0:
        tips = ramp(O[0], O[1], -90, P, k)
        b += vec_anim("r", [O] * len(tips), tips, 0.22) + ring(*O)
        return fig("d5-0", "0 0 420 240", "Vật 3,0 kg treo vào vòng nhẫn O; dây OA nằm ngang buộc vào tường, dây OB hợp với phương thẳng đứng góc 30 độ buộc vào trần", b,
                   "Mô phỏng: trọng lực của vật treo tăng dần từ 15 % lên đủ (khoảng 4 s). Lực căng hai dây chưa vẽ.")
    s, _ = vec_luc("r", O[0], O[1], 0, 1, P, k)
    b += s + ring(*O) + field_line(O[0], O[1], O[0] + 84, O[1], GRN, 1.6, "5 4", 10) + lbl(O[0] + 88, O[1] + 5, "Ox", GRN, 13, "start", "700")
    b += field_line(O[0], O[1], O[0], O[1] - 62, GRN, 1.6, "5 4", 10) + lbl(O[0] + 6, O[1] - 66, "Oy", GRN, 13, "start", "700")
    return fig("d5-2", "0 0 420 240", "Vòng nhẫn O với hai trục Ox nằm ngang và Oy thẳng đứng lên, trọng lực P hướng xuống, hai dây OA và OB", b,
               "Dữ kiện: hai trục Ox (ngang), Oy (thẳng đứng lên) đặt tại O; chỉ vẽ trọng lực, lực căng hai dây chưa vẽ.")


# ───────────── Dạng 6: dây dài 6,0 m, võng 0,50 m, đèn 4,0 kg ─────────────
def d6(kk):
    A = (34.0, 70.0); B = (386.0, 70.0); s = (B[0] - A[0]) / 6.0; S = 0.5 * s; k = 2.0; P = 40.0
    mid = (A[0] + B[0]) / 2
    b = seg(A[0], 30, A[0], 205, "currentColor", 3) + seg(B[0], 30, B[0], 205, "currentColor", 3)
    b += seg(A[0], A[1], B[0], B[1], GREY, 1.2, "5 4", .8)
    b += dim("", "b", A[0], 46, B[0], 46, "6,0 m", mid - 20, 40)
    b += lbl(A[0] + 8, A[1] - 6, "A", "currentColor", 13, "start", "700") + lbl(B[0] - 8, B[1] - 6, "B", "currentColor", 13, "end", "700")
    b += lbl(mid + 12, 196, "đèn 4,0 kg", "currentColor", 12, "start", "600")
    Lf = (mid, A[1] + S)
    if kk == 0:
        n = 38; step = 0.1
        sag = [S * (1 - math.exp(-2.4 * i * step) * math.cos(2 * math.pi * 0.8 * i * step)) for i in range(n)]
        sag[-1] = S
        Ls = [(mid, A[1] + g) for g in sag]
        dur = step * (n - 1)
        b += (f'<line x1="{A[0]}" y1="{A[1]}" x2="{Ls[0][0]:.1f}" y2="{Ls[0][1]:.1f}" stroke="currentColor" stroke-width="2.4">{an("x2", [p[0] for p in Ls], dur)}{an("y2", [p[1] for p in Ls], dur)}</line>'
              f'<line x1="{Ls[0][0]:.1f}" y1="{Ls[0][1]:.1f}" x2="{B[0]}" y2="{B[1]}" stroke="currentColor" stroke-width="2.4">{an("x1", [p[0] for p in Ls], dur)}{an("y1", [p[1] for p in Ls], dur)}</line>')
        tips = [(p[0], p[1] + k * P) for p in Ls]
        b += vec_anim("r", Ls, tips, step)
        b += (f'<circle cx="{Ls[0][0]:.1f}" cy="{Ls[0][1]:.1f}" r="6" fill="none" stroke="currentColor" stroke-width="2">{an("cy", [p[1] for p in Ls], dur)}</circle>')
        b += dim("", "o", mid, A[1], mid, Lf[1] - 7, "", 0, 0) + lbl(mid + 10, A[1] + 17, "0,50 m", ORG, 12, "start", "700")
        return fig("d6-0", "0 0 420 240", "Đèn 4,0 kg được thả vào chính giữa dây điện nằm ngang dài 6,0 m, dây võng xuống 0,50 m rồi đứng yên", b,
                   "Mô phỏng: đèn thả vào giữa dây, dao động tắt dần (chỉ minh hoạ) rồi đứng yên ở độ võng 0,50 m của đề (khoảng 4 s). Chỉ vẽ trọng lực; lực căng chưa vẽ.")
    b += seg(A[0], A[1], Lf[0], Lf[1], "currentColor", 2.4) + seg(Lf[0], Lf[1], B[0], B[1], "currentColor", 2.4) + ring(*Lf, 6)
    sv, tip = vec_luc("r", Lf[0], Lf[1], 0, 1, P, k)
    b += sv + dim("", "o", mid, A[1], mid, Lf[1] - 7, "", 0, 0) + lbl(mid + 10, A[1] + 17, "0,50 m", ORG, 12, "start", "700")
    th = math.degrees(math.atan2(S, 3.0 * s))
    b += arc(A[0], A[1], 60, -th, 0, RED) + lbl(A[0] + 70, A[1] + 28, "θ = ?", RED, 13, "start", "700")
    return fig("d6-2", "0 0 420 240", "Dây điện nằm ngang dài 6,0 m võng xuống 0,50 m ở chính giữa, đèn treo ở điểm giữa, trọng lực hướng xuống", b,
               "Dữ kiện: nhịp 6,0 m và độ võng 0,50 m vẽ đúng tỉ lệ độ dài; chỉ vẽ trọng lực đèn, lực căng chưa vẽ.")


BUILD = [d1, d2, d3, d4, d5, d6]
