"""Hình cho bài tập mẫu Bài 33 "Biến dạng của vật rắn" (Vật lí 10), lesson_id 78.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Lò xo vẽ bằng đường gấp khúc co giãn (animateTransform scale, nét không co theo: vector-effect) nên mỗi mẫu chỉ tốn 1 số.
Quy tắc vectơ lực (thầy chốt 10/10/2026): đầu mũi tên chữ V 30°, độ dài = k·F với MỘT hệ số k cho cả hình (vec_luc), không marker.
KHÔNG vẽ đáp số: lực đàn hồi không được vẽ; hình D3 minh hoạ chiều biến dạng, độ lớn KHÔNG theo số liệu đề.
Mô phỏng: D1 kéo lò xo tăng dần 2→10 N theo đúng bảng số liệu của đề; D2 kéo 0→6,0 N, độ dãn tỉ lệ (Hooke thật, k=150);
D3 kéo rồi nén (minh hoạ); D4 thả vật 120 g từ chiều dài tự nhiên (dao động tắt dần thật, k=40, m=0,12);
D5 treo thêm vật cho tổng 480 g (dao động tắt dần thật quanh vị trí cân bằng mới, k=80, m=0,48)."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import vec_luc, chevron, field_line

GREY = "#94a3b8"
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}


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


def show(inner, t0, t1, total):
    """Nhóm hiện trong khoảng [t0, t1) giây của đoạn mô phỏng dài `total` giây (t1=None: hiện tới hết)."""
    if t1 is None or t1 >= total - 1e-9:
        v, k = "0;1", f"0;{t0 / total:.4f}"
    else:
        v, k = "0;1;0", f"0;{t0 / total:.4f};{t1 / total:.4f}"
    return (f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="{v}" keyTimes="{k}" '
            f'dur="{total:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>')


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


def hatch(x0, y0, x1, y1, n=8):
    """Tường (đoạn thẳng đứng, vạch hướng sang trái) hoặc trần (đoạn nằm ngang, vạch hướng lên)."""
    out = seg(x0, y0, x1, y1, "currentColor", 2.4)
    for i in range(n + 1):
        px, py = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n
        out += seg(px, py, px - 8, py + 8, "currentColor", 1.2, "", .7) if x0 == x1 else seg(px, py, px + 8, py - 8, "currentColor", 1.2, "", .7)
    return out


def _zig(n=9, amp=7, lead=0.07):
    pts = [(0.0, 0.0), (lead, 0.0)]
    m = 2 * n
    for i in range(m):
        pts.append((lead + (1 - 2 * lead) * (i + 0.5) / m, amp if i % 2 == 0 else -amp))
    return pts + [(1 - lead, 0.0), (1.0, 0.0)]


def spring_h(x0, y, lens, dur=None, n=9, amp=7, col="currentColor", w=2.2):
    """Lò xo nằm ngang, đầu trái cố định tại (x0, y); lens = các chiều dài (px) theo mẫu thời gian."""
    p = " ".join(f"{a:.4f},{b:.1f}" for a, b in _zig(n, amp))
    anim = ""
    if len(lens) > 1:
        anim = (f'<animateTransform attributeName="transform" type="scale" values="{";".join(f"{L:.2f} 1" for L in lens)}" '
                f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')
    return (f'<g transform="translate({x0:.1f},{y:.1f})"><polyline points="{p}" fill="none" stroke="{col}" stroke-width="{w}" '
            f'stroke-linejoin="round" vector-effect="non-scaling-stroke" transform="scale({lens[0]:.2f} 1)">{anim}</polyline></g>')


def spring_v(x, y0, lens, dur=None, n=9, amp=7, col="currentColor", w=2.2):
    """Lò xo thẳng đứng, đầu trên cố định tại (x, y0)."""
    p = " ".join(f"{b:.1f},{a:.4f}" for a, b in _zig(n, amp))
    anim = ""
    if len(lens) > 1:
        anim = (f'<animateTransform attributeName="transform" type="scale" values="{";".join(f"1 {L:.2f}" for L in lens)}" '
                f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')
    return (f'<g transform="translate({x:.1f},{y0:.1f})"><polyline points="{p}" fill="none" stroke="{col}" stroke-width="{w}" '
            f'stroke-linejoin="round" vector-effect="non-scaling-stroke" transform="scale(1 {lens[0]:.2f})">{anim}</polyline></g>')


def block(x, y, w, h, label, ys=None, dur=None, size=12):
    """Vật (hình chữ nhật có nhãn); ys = các toạ độ y của cạnh trên theo mẫu thời gian."""
    ya = smil("y", ys, dur) if ys else ""
    yt = smil("y", [v + h / 2 + 4.5 for v in ys], dur) if ys else ""
    y0 = ys[0] if ys else y
    return (f'<rect x="{x:.1f}" y="{y0:.1f}" width="{w}" height="{h}" fill="none" stroke="currentColor" stroke-width="2.2">{ya}</rect>'
            f'<text x="{x + w / 2:.1f}" y="{y0 + h / 2 + 4.5:.1f}" fill="currentColor" font-size="{size}" font-weight="600" text-anchor="middle">{label}{yt}</text>')


def damped(l_start, l_eq, omega, zeta, t):
    """Chiều dài lò xo (cm) sau thời gian t (s) khi thả từ trạng thái nghỉ ở l_start, cân bằng ở l_eq (dao động tắt dần)."""
    wd = omega * math.sqrt(1 - zeta ** 2)
    return l_eq + (l_start - l_eq) * math.exp(-zeta * omega * t) * (math.cos(wd * t) + zeta * omega / wd * math.sin(wd * t))


# ───────────── Dạng 1: lò xo l0 = 20 cm kéo 2, 4, 6, 8, 10 N (bảng của đề) ─────────────
D1_L = {0: 20, 2: 22, 4: 24, 6: 26, 8: 28, 10: 33}      # chiều dài khi có lực (cm) — đúng bảng của đề


def d1_l(F):
    xs = sorted(D1_L)
    for a, b in zip(xs, xs[1:]):
        if a <= F <= b:
            return D1_L[a] + (D1_L[b] - D1_L[a]) * (F - a) / (b - a)


def d1(kk):
    WX, sc, yS, k = 30, 6.0, 75, 12.0
    nat = WX + sc * 20
    b = hatch(WX, 40, WX, 110, 7) + seg(nat, 56, nat, 126, GREY, 1.2, "4 4", .8)
    b += lbl(nat, 48, "l₀ = 20 cm", "currentColor", 12, "middle", "700")
    if kk == 0:
        dt = 0.2
        Fs = [0.0] * 3
        starts = []
        prev = 0.0
        for T in (2, 4, 6, 8, 10):
            starts.append(len(Fs))
            first = 1.0 if T == 2 else prev
            ramp = [first + (T - first) * j / 2 for j in range(3)] if T == 2 else [prev + (T - prev) * (j + 1) / 3 for j in range(3)]
            Fs += ramp + [T] * 6
            prev = T
        ends = [WX + sc * d1_l(F) for F in Fs]
        n = len(Fs); dur = dt * (n - 1)
        b += spring_h(WX, yS, [e - WX for e in ends], dur)
        tails = [(e, yS) for e in ends]
        tips = [(e + k * (F if F > 0 else 2.0), yS) for e, F in zip(ends, Fs)]
        arrow_g = vec_anim("o", tails, tips, dt)
        b += show(arrow_g, starts[0] * dt, None, dur)
        for i, T in enumerate(("2", "4", "6", "8", "10")):
            t0 = starts[i] * dt
            t1 = starts[i + 1] * dt if i + 1 < len(starts) else None
            b += show(lbl(412, 28, f"F = {T} N", ORG, 14, "end", "700"), t0, t1, dur)
        cap = "Mô phỏng: lực kéo tăng lần lượt qua năm mức của bảng, dừng ở mỗi mức (khoảng 10 s); độ dài mũi tên tỉ lệ với F (1 N ứng với 12 px). Chỉ vẽ lúc có lực, không vẽ lúc thôi lực."
    else:
        F = 6
        e = WX + sc * d1_l(F)
        b += spring_h(WX, yS, [e - WX])
        s, _ = vec_luc("o", e, yS, 1, 0, F, k)
        b += s + dim("", "b", nat, 110, e, 110, "", 0, 0) + lbl((nat + e) / 2, 126, "Δl", BLUE, 13, "middle", "700")
        b += lbl(e + k * F + 8, yS + 5, "F = 6 N", ORG, 13, "start", "700")
    # thước cm
    b += seg(WX, 140, WX + sc * 36, 140, "currentColor", 1.4)
    for c in range(0, 37):
        h = 7 if c % 5 == 0 else 4
        b += seg(WX + sc * c, 140, WX + sc * c, 140 + h, "currentColor", 1.2)
    for c in range(0, 36, 5):
        b += lbl(WX + sc * c, 162, str(c), "currentColor", 12, "middle", "400")
    b += lbl(WX + sc * 36 + 6, 150, "cm", "currentColor", 12, "start", "400")
    vb = "0 0 420 172"
    if kk == 0:
        return fig("d1-0", vb, "Lò xo gắn vào tường được kéo bằng lực tăng dần từ 2 đến 10 niutơn, thước đo chiều dài bên dưới", b, cap)
    return fig("d1-2", vb, "Lò xo gắn vào tường, chiều dài tự nhiên 20 cm, đang chịu lực kéo 6 niutơn", b,
               "Dữ kiện: một lần thử trong bảng (F = 6 N); vạch đứt đánh dấu đầu lò xo khi chưa có lực, Δl là phần dài thêm. Thước vẽ đúng tỉ lệ.")


# ───────────── Dạng 2: kéo 6,0 N, lò xo dãn 4,0 cm (k = 150 N/m) ─────────────
D2_K, D2_F, D2_DL = 150.0, 6.0, 0.040


def d2(kk):
    WX, yS, sc, k = 30, 82, 8.0, 8.0
    nat = WX + sc * 15
    b = hatch(WX, 46, WX, 118, 7) + seg(nat, 58, nat, 112, GREY, 1.2, "4 4", .8)
    fin = nat + sc * D2_DL * 100
    if kk == 0:
        dt = 0.2
        Fs = [D2_F * (0.15 + 0.85 * j / 13) for j in range(14)] + [D2_F] * 6
        ends = [nat + sc * (F / D2_K) * 100 for F in Fs]
        n = len(Fs); dur = dt * (n - 1)
        b += spring_h(WX, yS, [e - WX for e in ends], dur)
        tails = [(e, yS) for e in ends]
        tips = [(e + k * F, yS) for e, F in zip(ends, Fs)]
        b += vec_anim("o", tails, tips, dt)
        b += show(dim("", "b", nat, 106, fin, 106, "", 0, 0) + lbl((nat + fin) / 2, 126, "Δl = 4,0 cm", BLUE, 13, "middle", "700"), dt * 14, None, dur)
        cap = "Mô phỏng: lực kéo tăng dần tới 6,0 N (khoảng 4 s), độ dãn tăng theo; 1 N ứng với 8 px, 1 cm ứng với 8 px. Số đo Δl chỉ hiện khi lò xo dừng."
    else:
        b += spring_h(WX, yS, [fin - WX])
        s, _ = vec_luc("o", fin, yS, 1, 0, D2_F, k)
        b += s + dim("", "b", nat, 106, fin, 106, "", 0, 0) + lbl((nat + fin) / 2, 126, "Δl = 4,0 cm", BLUE, 13, "middle", "700")
        cap = "Dữ kiện: lực kéo 6,0 N (1 N ứng với 8 px) làm lò xo dãn thêm 4,0 cm; vạch đứt là đầu lò xo khi chưa kéo."
    b += lbl(fin + k * D2_F + 8, yS + 5, "F = 6,0 N", ORG, 13, "start", "700")
    b += lbl(70, 52, "k = ?", "currentColor", 14, "start", "700")
    vb = "0 0 420 140"
    return fig("d2-0" if kk == 0 else "d2-2", vb, "Lò xo nằm ngang, một đầu cố định, bị kéo bằng lực 6,0 niutơn và dãn thêm 4,0 xentimét", b, cap)


# ───────────── Dạng 3: l0 = 24 cm, k = 120 N/m (hình minh hoạ chiều biến dạng, độ lớn không theo số đề) ─────────────
def d3(kk):
    WX, yS, sc = 30, 85, 5.0
    nat = WX + sc * 24
    b = hatch(WX, 50, WX, 120, 7)
    if kk == 0:
        dt = 0.15
        ease = lambda u: 0.5 - 0.5 * math.cos(math.pi * u)
        disp = [0.0] * 3
        marks = {}
        marks["pull0"] = len(disp)
        disp += [28 * ease((j + 1) / 8) for j in range(8)] + [28.0] * 5
        marks["pull1"] = len(disp)
        disp += [28 * (1 - ease((j + 1) / 6)) for j in range(6)] + [0.0] * 3
        marks["push0"] = len(disp)
        disp += [-28 * ease((j + 1) / 8) for j in range(8)] + [-28.0] * 5
        marks["push1"] = len(disp)
        disp += [-28 * (1 - ease((j + 1) / 6)) for j in range(6)] + [0.0] * 3
        n = len(disp); dur = dt * (n - 1)
        ends = [nat + d for d in disp]
        b += seg(nat, 62, nat, 112, GREY, 1.2, "4 4", .8) + lbl(nat, 54, "chưa biến dạng", "currentColor", 12, "middle", "600")
        b += spring_h(WX, yS, [e - WX for e in ends], dur)
        ln = [max(16.0, 2.0 * abs(d)) for d in disp]
        tails_p = [(e, yS) for e in ends]
        tips_p = [(e + L, yS) for e, L in zip(ends, ln)]
        b += show(vec_anim("o", tails_p, tips_p, dt), marks["pull0"] * dt, marks["pull1"] * dt, dur)
        tails_n = [(e + L, yS) for e, L in zip(ends, ln)]
        tips_n = [(e, yS) for e in ends]
        b += show(vec_anim("o", tails_n, tips_n, dt), marks["push0"] * dt, marks["push1"] * dt, dur)
        b += show(lbl(330, 40, "lực kéo", ORG, 13, "start", "700"), marks["pull0"] * dt, marks["pull1"] * dt, dur)
        b += show(lbl(330, 40, "lực đẩy", ORG, 13, "start", "700"), marks["push0"] * dt, marks["push1"] * dt, dur)
        cap = "Mô phỏng: kéo rồi đẩy một lò xo (khoảng 7 s). Hình chỉ minh hoạ chiều biến dạng; độ lớn lực và độ biến dạng không theo số liệu của đề."
        return fig("d3-0", "0 0 420 140", "Lò xo nằm ngang gắn vào tường, lần lượt bị kéo dài ra rồi bị đẩy ngắn lại", b, cap)
    b += spring_h(WX, yS, [nat - WX]) + seg(nat, 62, nat, 112, GREY, 1.2, "4 4", .8)
    b += dim("", "b", WX, 52, nat, 52, "", 0, 0) + lbl((WX + nat) / 2, 44, "l₀ = 24 cm", BLUE, 13, "middle", "700")
    b += lbl(200, 78, "k = 120 N/m", "currentColor", 13, "start", "700")
    b += lbl(200, 102, "kéo 3,6 N → l = ?", ORG, 13, "start", "700") + lbl(200, 124, "đẩy 4,8 N → l = ?", ORG, 13, "start", "700")
    return fig("d3-2", "0 0 420 140", "Lò xo nằm ngang ở chiều dài tự nhiên 24 xentimét, độ cứng 120 niutơn trên mét", b,
               "Dữ kiện: lò xo ở chiều dài tự nhiên (chưa có lực); ba ý a, b, c của đề đều dùng cùng lò xo này.")


# ───────────── Dạng 4: l0 = 20 cm, vật 120 g, đứng yên ở 23 cm (k = 40 N/m) ─────────────
D4_K, D4_M, D4_L0, D4_L1 = 40.0, 0.120, 20.0, 23.0


def d4(kk):
    cx, y0, sc, bw, bh = 200, 24, 5.0, 46, 32
    b = hatch(150, y0, 250, y0, 10)
    b += dim("", "b", 140, y0, 140, y0 + sc * D4_L0, "", 0, 0) + lbl(134, y0 + sc * D4_L0 / 2 + 4, "l₀ = 20 cm", BLUE, 13, "end", "700")
    b += seg(120, y0 + sc * D4_L0, 250, y0 + sc * D4_L0, GREY, 1.2, "4 4", .8)
    if kk == 0:
        step, slow, tmax = 0.048, 3.0, 1.6
        ts_real = [j * step / slow for j in range(int(round(tmax / (step / slow))) + 1)]
        om = math.sqrt(D4_K / D4_M)
        ls = [damped(D4_L0, D4_L1, om, 0.18, t) for t in ts_real]
        ls[-1] = D4_L1
        n = len(ls); dur = step * (n - 1)
        lens = [sc * l for l in ls]
        b += spring_v(cx, y0, lens, dur)
        b += block(cx - bw / 2, 0, bw, bh, "120 g", [y0 + L for L in lens], dur)
        yf = y0 + sc * D4_L1
        b += show(dim("", "o", 262, y0, 262, yf, "", 0, 0) + lbl(270, y0 + sc * D4_L1 / 2 + 4, "l = 23 cm", ORG, 13, "start", "700"), dur - 0.4, None, dur)
        cap = "Mô phỏng: thả vật 120 g từ chiều dài tự nhiên; lò xo dao động tắt dần rồi đứng yên (tính theo k, m; chạy chậm 3 lần, khoảng 5 s)."
    else:
        yf = y0 + sc * D4_L1
        b += spring_v(cx, y0, [sc * D4_L1])
        b += block(cx - bw / 2, yf, bw, bh, "120 g")
        b += dim("", "o", 262, y0, 262, yf, "", 0, 0) + lbl(270, y0 + sc * D4_L1 / 2 + 4, "l = 23 cm", ORG, 13, "start", "700")
        b += lbl(236, yf + bh / 2 + 5, "k = ?", "currentColor", 14, "start", "700")
        cap = "Dữ kiện: vật 120 g đứng yên, lò xo dài 23 cm; vạch đứt là đầu dưới lò xo khi chưa treo vật. Thước chiều dài vẽ đúng tỉ lệ."
    return fig("d4-0" if kk == 0 else "d4-2", "0 0 420 214", "Lò xo thẳng đứng, đầu trên cố định, treo vật 120 gam ở đầu dưới", b, cap)


# ───────────── Dạng 5: vật 160 g → 23 cm; tổng 480 g → 27 cm (k = 80 N/m, l0 = 22 cm) ─────────────
D5_K, D5_L0, D5_M1, D5_M2, D5_L1, D5_L2 = 80.0, 22.0, 0.160, 0.480, 24.0, 28.0


def d5(kk):
    y0, sc, bw, bh = 24, 5.0, 56, 30
    if kk == 0:
        cx = 190
        b = hatch(130, y0, 250, y0, 10)
        step, slow, tmax, n1 = 0.06, 2.5, 2.6, 20
        om = math.sqrt(D5_K / D5_M2)
        real = [(j + 1) * step / slow for j in range(int(round(tmax / (step / slow))))]
        ls = [D5_L1] * n1 + [damped(D5_L1, D5_L2, om, 0.18, t) for t in real]
        ls[-1] = D5_L2
        n = len(ls); dur = step * (n - 1)
        lens = [sc * l for l in ls]
        b += spring_v(cx, y0, lens, dur)
        top = [y0 + L for L in lens]
        b += block(cx - bw / 2, 0, bw, bh, "160 g", top, dur)
        b += show(block(cx - bw / 2, 0, bw, bh, "+ 320 g", [t + bh for t in top], dur), n1 * step, None, dur)
        y1, y2 = y0 + sc * D5_L1, y0 + sc * D5_L2
        b += show(dim("", "o", 110, y0, 110, y1, "", 0, 0) + lbl(104, y0 + sc * D5_L1 / 2 + 4, "l₁ = 24 cm", ORG, 13, "end", "700"), 0, n1 * step, dur)
        b += show(dim("", "o", 110, y0, 110, y2, "", 0, 0) + lbl(104, y0 + sc * D5_L2 / 2 + 4, "l₂ = 28 cm", ORG, 13, "end", "700"), dur - 0.4, None, dur)
        cap = "Mô phỏng: treo vật 160 g, rồi treo thêm một vật nữa; lò xo dao động tắt dần quanh vị trí cân bằng mới (tính theo k, m; chạy chậm 2,5 lần, khoảng 8 s)."
        return fig("d5-0", "0 0 420 250", "Lò xo thẳng đứng treo vật 160 gam, sau đó treo thêm vật nữa cho tổng khối lượng 480 gam", b, cap)
    b = hatch(60, y0, 380, y0, 16)
    for cx, m, L, nm in ((150, "160 g", D5_L1, "l₁"), (310, "480 g", D5_L2, "l₂")):
        yf = y0 + sc * L
        b += spring_v(cx, y0, [sc * L]) + block(cx - bw / 2, yf, bw, bh, m)
        b += dim("", "o", cx - 62, y0, cx - 62, yf, "", 0, 0) + lbl(cx - 68, y0 + sc * L / 2 + 4, f"{nm} = {int(L)} cm", ORG, 13, "end", "700")
    return fig("d5-2", "0 0 420 214", "Hai lần treo cùng một lò xo: vật 160 gam làm lò xo dài 24 xentimét, tổng 480 gam làm lò xo dài 28 xentimét", b,
               "Dữ kiện: hai trạng thái của cùng một lò xo (hai hình vẽ cạnh nhau). Chiều dài tự nhiên chưa biết nên không vẽ.")


BUILD = [d1, d2, d3, d4, d5]
