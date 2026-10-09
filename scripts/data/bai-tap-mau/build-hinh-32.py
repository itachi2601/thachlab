"""Bài 32 (Bài 13. Sóng dừng, Vật lí 11): 6 dạng bài tập mẫu, mỗi dạng có buoc[] tự giải từng bước.
Hình tính thật (sóng dừng = tích sin(không gian) × cos(thời gian); sóng tới/phản xạ = hình sin tịnh tiến), chạy MỘT lần khi bấm.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-32.py   (sinh scripts/data/bai-tap-mau/32.json)
Đối chiếu số: python3 scripts/data/bai-tap-mau/build-hinh-32.py --kiem"""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "32.json")
T173 = "Nút, bụng sóng và điều kiện có sóng dừng"
T174 = "Tính bước sóng, tốc độ truyền sóng từ sóng dừng"
TAU = 2 * math.pi
NOTE = "Hình minh hoạ, không đúng tỉ lệ."

# ───────────── Số liệu từng dạng (tự giải lại độc lập ở --kiem) ─────────────
# D1: l=0,6 m, v=24 m/s, f=60 Hz | D2: l=0,9 m, v=18 m/s, f=30 và 45 Hz | D3: l=1,5 m, f=40 Hz, 4 điểm đứng yên giữa
# D4: l=1,5 m, f1=42 Hz 7 nút, 5 nút | D5: l=90 cm, 3 bó, Ab=4 cm, d=5 cm, 2√3 cm | D6: l=0,75 m, 150 và 200 Hz liên tiếp

# ───────────── Hình: các mảnh dựng sẵn ─────────────
def sd_pl(pts, yc, amp, c="currentColor", w=2.6, dash="", op=1, rel=False):
    """Đường gấp khúc từ (x, s): s là li độ chuẩn hoá; y_pixel = yc - s*amp (rel: y = -s*amp, dùng trong nhóm đã tịnh tiến tới yc)."""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    base = 0 if rel else yc
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" stroke-linejoin="round" points="'
            + " ".join(f"{x:.1f},{base - s * amp:.1f}" for x, s in pts) + '"/>')

def sd_curve(fn, xa, xb, n):
    return [(xa + (xb - xa) * i / n, fn(xa + (xb - xa) * i / n)) for i in range(n + 1)]

def sd_osc(cyc, T, spp=24, phase=0.0):
    """Hệ số co giãn theo trục y của li độ: cos(2πt/T), `cyc` chu kì (có thể lẻ), lấy mẫu spp điểm/chu kì."""
    n = int(round(cyc * spp)); dur = cyc * T
    vals = ";".join(f"1 {math.cos(TAU * j / spp + phase):.3f}" for j in range(n + 1))
    return f'<animateTransform attributeName="transform" type="scale" values="{vals}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'

def sd_slide(dx, cyc, T):
    return f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{dx:.1f} 0" dur="{cyc * T:.2f}s" begin="indefinite" fill="freeze"/>'

def sd_wall(x, y, side=-1, h=34):
    """Tường cố định; side=-1: dây ở bên phải tường (vạch chéo hướng sang trái)."""
    s = seg(x, y - h, x, y + h, "currentColor", 3)
    for i in range(-3, 4):
        yy = y + i * h / 3.5
        s += seg(x, yy, x + 9 * side, yy + 9, "currentColor", 1.6)
    return s

def sd_ring(x, y, amp_px, cyc, T, spp=24, h=46):
    """Cọc thẳng đứng + vòng nhẹ trượt (đầu tự do), vòng dao động cùng đầu dây (bụng, cực đại ở t=0)."""
    n = int(round(cyc * spp)); dur = cyc * T
    vals = ";".join(f"{y - amp_px * math.cos(TAU * j / spp):.1f}" for j in range(n + 1))
    return (seg(x, y - h, x, y + h, "currentColor", 3)
            + f'<circle cx="{x}" cy="{y - amp_px:.1f}" r="5.5" fill="none" stroke="{ORG}" stroke-width="2.6">'
              f'<animate attributeName="cy" values="{vals}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></circle>')

def sd_shape(kind, k, x0, x1):
    L = x1 - x0
    if kind == "cc":
        return (lambda x: math.sin(k * math.pi * (x - x0) / L)), 24 * k
    return (lambda x: math.sin((2 * k + 1) * math.pi * (x - x0) / (2 * L))), 12 * (2 * k + 1)

def sd_nodes(kind, k, x0, x1):
    L = x1 - x0
    sp = L / k if kind == "cc" else 2 * L / (2 * k + 1)
    return [x0 + j * sp for j in range(k + 1)]

def sd_string(kind, k, x0, x1, yc, amp, live=False, cyc=3, T=1.2, dots=True, env=True, c="currentColor", w=2.8, dash="", op=1):
    """Dây sóng dừng: kind 'cc' (hai đầu cố định, k bó) hoặc 'ct' (A cố định ở x0, đầu tự do ở x1, l=(2k+1)λ/4).
    live: dây dao động (một lần khi bấm), dừng ở lúc li độ cực đại. Đường bao nét đứt, nút là chấm."""
    fn, n = sd_shape(kind, k, x0, x1)
    pts = sd_curve(fn, x0, x1, n)
    out = seg(x0, yc, x1, yc, "currentColor", 1, "2 5", 0.45)
    if env:
        out += sd_pl([(x, abs(s)) for x, s in pts], yc, amp, c, 1.4, "5 4", 0.45) + sd_pl([(x, -abs(s)) for x, s in pts], yc, amp, c, 1.4, "5 4", 0.45)
    if live:
        out += f'<g transform="translate(0,{yc})"><g>{sd_osc(cyc, T)}{sd_pl(pts, yc, amp, c, w, dash, op, rel=True)}</g></g>'
    else:
        out += sd_pl(pts, yc, amp, c, w, dash, op)
    if dots:
        for xn in sd_nodes(kind, k, x0, x1):
            out += dot(xn, yc, 4.2, "currentColor")
    return out

def sd_trav_row(p, x0, x1, yc, amp, lam, shape, direction, c, cyc, T, w=2.4, clip=None):
    """Sóng chạy: hình sin tĩnh tịnh tiến (đúng vật lí), cắt vào [x0, x1] bằng clipPath `clip`."""
    ext = lam * (cyc + 1)
    pts = sd_curve(shape, x0 - ext, x1 + ext, int(24 * (x1 - x0 + 2 * ext) / lam))
    dx = direction * lam * cyc
    return (f'<g clip-path="url(#{clip})"><g>{sd_slide(dx, cyc, T)}{sd_pl(pts, yc, amp, c, w)}</g></g>')

def sd_clip(cid, x0, x1, y0, y1):
    return f'<defs><clipPath id="{cid}"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/></clipPath></defs>'

def sd_reflect(p, kind, x0=48, x1=400, lam=108, a=24, cyc=2.125, T=2.2):
    """Hai hàng: (1) sóng tới (xanh) và sóng phản xạ (cam) chạy ngược chiều; (2) tổng hợp = sóng dừng.
    kind 'fixed': đầu cố định bên trái (ngược pha → nút); 'free': đầu tự do bên phải (cùng pha → bụng)."""
    y1, y2 = 66, 176
    kap = TAU / lam
    b = sd_clip(p + "-c1", x0, x1, y1 - a - 8, y1 + a + 8) + sd_clip(p + "-c2", x0, x1, 0, 260)
    b += seg(x0, y1, x1, y1, "currentColor", 1, "2 5", 0.45) + seg(x0, y2, x1, y2, "currentColor", 1, "2 5", 0.45)
    if kind == "fixed":
        sh = lambda x: -math.sin(kap * (x - x0))                 # t=0: tới và phản xạ trùng nhau, li độ -a·sin(κu)
        b += sd_trav_row(p, x0, x1, y1, a, lam, sh, -1, BLUE, cyc, T, 3.2, p + "-c1")      # tới: về phía tường (sang trái)
        b += sd_trav_row(p, x0, x1, y1, a, lam, sh, +1, ORG, cyc, T, 2.0, p + "-c1")       # phản xạ: rời tường (sang phải)
        sum_pts = sd_curve(lambda x: -2 * math.sin(kap * (x - x0)), x0, x1, int(24 * (x1 - x0) / lam))
        nodes = [x0 + j * lam / 2 for j in range(int((x1 - x0) / (lam / 2)) + 1)]
        b += sd_wall(x0, y2, -1) + sd_wall(x0, y1, -1)
    else:
        sh = lambda x: math.cos(kap * (x1 - x))
        b += sd_trav_row(p, x0, x1, y1, a, lam, sh, +1, BLUE, cyc, T, 3.2, p + "-c1")      # tới: về phía đầu tự do (sang phải)
        b += sd_trav_row(p, x0, x1, y1, a, lam, sh, -1, ORG, cyc, T, 2.0, p + "-c1")       # phản xạ: rời đầu tự do (sang trái)
        sum_pts = sd_curve(lambda x: 2 * math.cos(kap * (x1 - x)), x0, x1, int(24 * (x1 - x0) / lam))
        nodes = [x1 - lam / 4 - j * lam / 2 for j in range(int((x1 - x0 - lam / 4) / (lam / 2)) + 1)]
    b += f'<g transform="translate(0,{y2})"><g>{sd_osc(cyc, T)}{sd_pl(sum_pts, 0, a, "currentColor", 3.2, rel=True)}</g></g>'
    if kind == "fixed":
        for xn in nodes: b += dot(xn, y2, 4.2, GRN)
        b += lbl(x0 + 8, 16, "sóng tới", BLUE, 13, "start", "700") + lbl(x0 + 100, 16, "sóng phản xạ", ORG, 13, "start", "700")
        b += lbl(x0 + 4, 252, "sóng tổng hợp", "currentColor", 13, "start", "700")
        b += lbl(x1 - 4, 252, "chấm xanh: các điểm đứng yên", GRN, 12, "end", "400")
        b += lbl(4, 26, "A", "currentColor", 14, "start", "700") + lbl(4, 120, "cố định", "currentColor", 11, "start", "400")
    else:
        for xn in nodes: b += dot(xn, y2, 4.2, GRN)
        b += sd_ring(x1, y2, 2 * a, cyc, T)
        b += lbl(x0 + 8, 16, "sóng tới", BLUE, 13, "start", "700") + lbl(x0 + 100, 16, "sóng phản xạ", ORG, 13, "start", "700")
        b += lbl(x0 + 4, 252, "sóng tổng hợp", "currentColor", 13, "start", "700")
        b += lbl(x1 - 4, 252, "chấm xanh: các điểm đứng yên", GRN, 12, "end", "400")
        b += lbl(x1 + 6, 24, "B", "currentColor", 14, "start", "700") + lbl(x1 - 4, 120, "tự do", "currentColor", 11, "end", "400")
    return b

def sd_dimh(p, c, x1, x2, y, label, ly=None, dx=0):
    return dim(p, c, x1, y, x2, y, label, (x1 + x2) / 2 - 24 + dx, (ly if ly is not None else y + 18))

def sd_ab(x0, x1, yc, a="A", b_="B"):
    return lbl(x0 - 4, yc + 20, a, "currentColor", 14, "end", "700") + lbl(x1 + 4, yc + 20, b_, "currentColor", 14, "start", "700")

# ───────────── Dạng 1: hai đầu cố định, l=0,6; v=24; f=60 ─────────────
def d1(k):
    p = f"s1{k}"
    if k == 0:
        b = defs(p) + sd_reflect(p, "fixed")
        return fig("sd1-0", "0 0 420 262", "Sóng tới và sóng phản xạ chạy ngược chiều ở đầu A cố định, tổng hợp lại có điểm đứng yên ở A và cách đều nhau", b,
                   "Mô phỏng chậm nhiều lần: sóng tới (xanh) và sóng phản xạ (cam) ngược pha ở A nên tổng luôn bằng 0 tại A. " + NOTE)
    b = defs(p)
    x0, x1 = 56, 276
    for i, kk in enumerate((1, 2, 3)):
        yc = 40 + i * 62
        b += sd_string("cc", kk, x0, x1, yc, 20, dots=True)
        b += lbl(x1 + 16, yc - 2, f"k = {kk}", "currentColor", 13, "start", "700") + lbl(x1 + 16, yc + 16, f"l = {kk}·λ/2" if kk > 1 else "l = λ/2", ORG, 13, "start", "700")
    b += lbl(x0 - 6, 22, "A", "currentColor", 14, "end", "700") + lbl(x1 + 6, 22, "B", "currentColor", 14, "start", "700")
    b += dim(p, "b", x0, 214, x1, 214, "l = 0,6 m", (x0 + x1) / 2 - 36, 234)
    b += lbl(14, 252, "Hai đầu là nút: mỗi bó dài λ/2", "currentColor", 12, "start", "400")
    return fig("sd1-2", "0 0 420 262", "Ba dạng sóng dừng đầu tiên trên dây hai đầu cố định, hai đầu luôn là nút, mỗi bó dài nửa bước sóng", b, "Dữ kiện: mọi hình sóng dừng đều có nút ở A và B. " + NOTE)

# ───────────── Dạng 2: một đầu cố định, một đầu tự do; l=0,9; v=18; f=30, 45 ─────────────
def d2(k):
    p = f"s2{k}"
    if k == 0:
        b = defs(p) + sd_reflect(p, "free")
        return fig("sd2-0", "0 0 420 262", "Sóng tới và sóng phản xạ cùng pha ở đầu B tự do, tổng hợp có bụng ở B", b,
                   "Mô phỏng chậm nhiều lần: ở B tự do, sóng tới và sóng phản xạ cùng pha nên biên độ gấp đôi (bụng). " + NOTE)
    b = defs(p)
    x0, x1 = 56, 276
    for i, kk in enumerate((0, 1, 2)):
        yc = 40 + i * 62
        b += sd_string("ct", kk, x0, x1, yc, 20, dots=True)
        b += lbl(x1 + 16, yc - 2, f"k = {kk}", "currentColor", 13, "start", "700") + lbl(x1 + 16, yc + 16, ["l = λ/4", "l = 3·λ/4", "l = 5·λ/4"][kk], ORG, 13, "start", "700")
        b += seg(x1, yc - 28, x1, yc + 28, "currentColor", 2.4)
    b += lbl(x0 - 6, 22, "A (nút)", "currentColor", 13, "end", "700") + lbl(x1 + 6, 22, "B (bụng)", "currentColor", 13, "start", "700")
    b += dim(p, "b", x0, 214, x1, 214, "l = 0,9 m", (x0 + x1) / 2 - 36, 234)
    b += lbl(14, 252, "Chiều dài dây là số lẻ lần λ/4", "currentColor", 12, "start", "400")
    return fig("sd2-2", "0 0 420 262", "Ba dạng sóng dừng đầu tiên trên dây một đầu cố định một đầu tự do, đầu tự do luôn là bụng", b, "Dữ kiện: A luôn là nút, B luôn là bụng. " + NOTE)

# ───────────── Dạng 3: l=1,5 m, f=40 Hz, 4 điểm đứng yên giữa → k=5 ─────────────
def d3(k):
    p = f"s3{k}"
    x0, x1, yc = 48, 372, 96
    b = defs(p)
    if k == 0:
        b += sd_wall(x0, yc, -1) + sd_wall(x1, yc, +1) + sd_string("cc", 3, x0, x1, yc, 40, live=True, cyc=3, T=1.2, dots=True)
        b += lbl(x0 - 6, yc - 46, "A", "currentColor", 14, "end", "700") + lbl(x1 + 6, yc - 46, "B", "currentColor", 14, "start", "700")
        b += dim(p, "b", x0, 176, x1, 176, "l = 1,5 m", (x0 + x1) / 2 - 34, 198)
        b += lbl(x0, 18, "f = 40 Hz", RED, 13, "start", "700") + lbl(x1, 18, "v = ?", ORG, 13, "end", "700")
        b += lbl(x0, 222, "Chấm đen: các điểm luôn đứng yên", "currentColor", 12, "start", "400")
        return fig("sd3-0", "0 0 420 234", "Sợi dây hai đầu cố định rung với tần số 40 Hz tạo sóng dừng", b,
                   "Mô phỏng minh hoạ dây rung (vẽ mẫu số bó khác đề, không phải đáp số; chạy chậm khoảng 48 lần so với thực tế). Mô phỏng: dây rung ổn định (chạy chậm khoảng 48 lần so với thực tế). " + NOTE)
    b += sd_wall(x0, yc, -1) + sd_wall(x1, yc, +1) + sd_string("cc", 5, x0, x1, yc, 40, dots=False)
    nd = sd_nodes("cc", 5, x0, x1)
    for j, xn in enumerate(nd):
        b += dot(xn, yc, 5, GRN if 0 < j < 5 else "currentColor")
    b += lbl(nd[1], yc + 56, "nút", GRN, 13, "middle", "700")
    b += sd_dimh(p, "o", nd[2], nd[3], yc - 52, "một bó = λ/2", yc - 58, dx=-20)
    b += dim(p, "b", x0, 176, x1, 176, "l = 1,5 m", (x0 + x1) / 2 - 34, 198)
    b += lbl(x0 - 6, yc - 46, "A", "currentColor", 14, "end", "700") + lbl(x1 + 6, yc - 46, "B", "currentColor", 14, "start", "700")
    b += lbl(x0, 222, "Chấm xanh: 4 điểm đứng yên nằm giữa A và B", GRN, 12, "start", "400")
    return fig("sd3-2", "0 0 420 234", "Dây có bốn điểm đứng yên nằm giữa hai đầu cố định, hai nút liên tiếp cách nhau nửa bước sóng", b, "Dữ kiện: 4 nút ở giữa, chưa kể A và B. " + NOTE)

# ───────────── Dạng 4: l=1,5; f1=42 Hz 7 nút; 5 nút ─────────────
def d4(k):
    p = f"s4{k}"
    x0, x1 = 48, 372
    b = defs(p)
    if k == 0:
        y1, y2 = 56, 160
        b += sd_wall(x0, y1, -1, 26) + sd_wall(x1, y1, +1, 26) + sd_string("cc", 6, x0, x1, y1, 30, live=True, cyc=3, T=1.2, dots=True)
        b += sd_wall(x0, y2, -1, 26) + sd_wall(x1, y2, +1, 26) + sd_string("cc", 4, x0, x1, y2, 30, live=False, dots=True, c=ORG, w=2.2, dash="6 4", op=0.9)
        b += lbl(x0, 14, "f₁ = 42 Hz · 7 nút", RED, 13, "start", "700") + lbl(x0, 118, "f₂ = ? · 5 nút", ORG, 13, "start", "700")
        b += dim(p, "b", x0, 214, x1, 214, "cùng một dây, l = 1,5 m", (x0 + x1) / 2 - 78, 236)
        return fig("sd4-0", "0 0 420 244", "Cùng một sợi dây hai đầu cố định: ở tần số 42 Hz có 7 nút; muốn có 5 nút phải đổi tần số", b,
                   "Mô phỏng: dây trên rung ở 42 Hz (chạy chậm khoảng 50 lần); dây dưới (nét đứt) là trạng thái cần có, chưa rung. " + NOTE)
    y1, y2 = 56, 160
    b += sd_wall(x0, y1, -1, 26) + sd_wall(x1, y1, +1, 26) + sd_string("cc", 6, x0, x1, y1, 30, dots=True)
    b += sd_wall(x0, y2, -1, 26) + sd_wall(x1, y2, +1, 26) + sd_string("cc", 4, x0, x1, y2, 30, dots=True, c=ORG)
    b += lbl(x0, 14, "f₁ = 42 Hz · 7 nút", RED, 13, "start", "700") + lbl(x0, 118, "f₂ = ? · 5 nút", ORG, 13, "start", "700")
    b += lbl(x0, 214, "v và l không đổi, chỉ đổi số bó", "currentColor", 13, "start", "700")
    return fig("sd4-2", "0 0 420 244", "Hai trạng thái sóng dừng trên cùng một dây: bảy nút ở tần số f1 và năm nút ở tần số f2", b, "Dữ kiện: cùng v, cùng l; số nút khác nhau thì tần số khác nhau. " + NOTE)

# ───────────── Dạng 5: l=90 cm, 3 bó, Ab=4 cm, d=5 cm ─────────────
def d5(k):
    p = f"s5{k}"
    x0, x1, yc = 52, 388, 100
    sc = (x1 - x0) / 90.0
    b = defs(p) + sd_wall(x0, yc, -1, 30) + sd_wall(x1, yc, +1, 30)
    live = (k == 0)
    b += sd_string("cc", 3, x0, x1, yc, 42, live=live, cyc=3, T=1.2, dots=True)
    xm = x0 + 5 * sc
    b += seg(xm, yc + 6, xm, yc + 40, ORG, 2) + lbl(xm, yc + 56, "M", ORG, 14, "middle", "700")
    b += lbl(x0 - 6, yc - 40, "A", "currentColor", 14, "end", "700") + lbl(x1 + 6, yc - 40, "B", "currentColor", 14, "start", "700")
    if k == 0:
        b += seg(x0, 182, xm, 182, ORG, 3) + lbl(xm + 12, 186, "d = 5 cm (từ A tới M)", ORG, 13, "start", "700")
        b += lbl(x0, 18, "3 bó sóng · biên độ bụng 4 cm", RED, 13, "start", "700")
        b += lbl(x0, 226, "Biên độ của M = ?", ORG, 13, "start", "700")
        return fig("sd5-0", "0 0 420 238", "Dây AB hai đầu cố định có sóng dừng với ba bó, điểm M cách đầu A năm xentimét", b,
                   "Mô phỏng: sóng dừng 3 bó, đường nét đứt là đường bao biên độ (chạy chậm nhiều lần). " + NOTE)
    b += lbl(x0, 18, "Hai đầu A, B là nút", "currentColor", 13, "start", "700")
    b += seg(x0, 182, xm, 182, ORG, 3) + lbl(xm + 12, 186, "d (đo từ nút A)", ORG, 13, "start", "700")
    xb = x0 + 2.5 * (x1 - x0) / 3
    b += arrow(p, "b", xb, yc, xb, yc - 42, 2) + lbl(xb + 8, yc - 18, "A_b", BLUE, 13, "start", "700")
    b += lbl(x0, 226, "Biên độ tăng dần từ nút (0) tới bụng (A_b)", "currentColor", 12, "start", "400")
    return fig("sd5-2", "0 0 420 238", "Dây ba bó, điểm M gần nút A, biên độ tăng dần từ nút tới bụng", b, "Dữ kiện: biên độ phụ thuộc khoảng cách tới nút gần nhất. " + NOTE)

# ───────────── Dạng 6: l=0,75; 150 và 200 Hz liên tiếp ─────────────
def d6(k):
    p = f"s6{k}"
    b = defs(p)
    if k == 0:
        x0, x1, yc, lam, a, cyc, T = 52, 330, 100, 56, 30, 3, 1.1
        b += sd_clip(p + "-c", x0, x1, yc - a - 8, yc + a + 8)
        sh = lambda x: math.cos(TAU * (x - x0) / lam)
        b += seg(x0, yc, x1, yc, "currentColor", 1, "2 5", 0.45) + sd_trav_row(p, x0, x1, yc, a, lam, sh, +1, BLUE, cyc, T, 3.0, p + "-c")
        vals = ";".join(f"{yc - a * math.cos(TAU * j / 24):.1f}" for j in range(int(cyc * 24) + 1))
        b += (f'<rect x="12" y="{yc - 14}" width="26" height="28" rx="4" fill="none" stroke="currentColor" stroke-width="2.4"/>'
              f'<circle cx="{x0}" cy="{yc - a}" r="5.5" fill="{RED}"><animate attributeName="cy" values="{vals}" dur="{cyc * T:.2f}s" begin="indefinite" fill="freeze"/></circle>')
        b += seg(38, yc, x0, yc, "currentColor", 2)
        b += lbl(10, yc + 36, "cần rung", "currentColor", 13, "start", "700") + lbl(10, yc + 54, "f thay đổi", RED, 13, "start", "700")
        b += lbl(x1 + 10, yc - 6, "≈", "currentColor", 18, "start", "700") + lbl(x1 + 26, yc - 6, "≈", "currentColor", 18, "start", "700")
        b += sd_wall(398, yc, +1, 34) + lbl(392, yc - 46, "B", "currentColor", 14, "end", "700")
        b += seg(x1 + 36, yc, 398, yc, "currentColor", 1, "2 5", 0.45)
        b += lbl(x0 + 6, 28, "sóng truyền tới đầu B cố định", BLUE, 13, "start", "700")
        b += lbl(x0 + 6, 196, "Chỉ một số tần số cho sóng dừng", "currentColor", 12, "start", "400")
        return fig("sd6-0", "0 0 420 210", "Cần rung phát sóng truyền dọc dây tới đầu B cố định, sóng phản xạ quay lại và có thể tạo sóng dừng ở một số tần số", b,
                   "Mô phỏng: cần rung đẩy sóng đi tới B (chạy chậm nhiều lần, đoạn dây không vẽ hết chiều dài). " + NOTE)
    ax_y = 100
    b += seg(40, ax_y, 392, ax_y, "currentColor", 2) + lbl(396, ax_y + 5, "f", "currentColor", 14, "start", "700")
    for xx, t in ((120, "150 Hz"), (268, "200 Hz")):
        b += seg(xx, ax_y - 12, xx, ax_y + 12, RED, 3) + lbl(xx, ax_y + 34, t, RED, 14, "middle", "700")
    b += sd_dimh(p, "b", 120, 268, 58, "hiệu = ?", 46, dx=0)
    b += lbl(40, 18, "Hai tần số liên tiếp: ứng với k và k + 1", "currentColor", 13, "start", "700")
    b += lbl(40, 166, "f₀ = ?", ORG, 14, "start", "700") + lbl(40, 186, "Mọi tần số sóng dừng là bội nguyên của f₀", "currentColor", 12, "start", "400")
    return fig("sd6-2", "0 0 420 198", "Trục tần số có hai điểm 150 Hz và 200 Hz là hai tần số liên tiếp cho sóng dừng", b, "Dữ kiện: hai tần số ứng với k và k + 1; trục không vẽ đúng tỉ lệ. " + NOTE)

BUILD = [d1, d2, d3, d4, d5, d6]

# ───────────── Đề (điều kiện đầu bài) ─────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Dây hai đầu cố định: tần số nhỏ nhất, số bó và số nút", topic=T173,
      problem_html=("<p>Sợi dây đàn hồi AB dài $l=0{,}6\\ \\text{m}$, hai đầu A và B cố định. Tốc độ truyền sóng trên dây là $v=24\\ \\text{m/s}$.</p>"
                    "<p>a) Tính bước sóng dài nhất và tần số nhỏ nhất để trên dây có sóng dừng.</p>"
                    "<p>b) Cho dây rung với tần số $f=60\\ \\text{Hz}$. Trên dây có sóng dừng không? Nếu có, trên dây có bao nhiêu bó sóng, bao nhiêu bụng sóng, bao nhiêu nút sóng (kể cả hai đầu)?</p>")),
 dict(label="Dạng 2 · Trung bình · Dây một đầu cố định, một đầu tự do", topic=T173,
      problem_html=("<p>Dây AB dài $l=0{,}9\\ \\text{m}$, đầu A cố định, đầu B gắn vào vòng nhẹ trượt trên cọc thẳng đứng (đầu B tự do). Tốc độ truyền sóng trên dây là $v=18\\ \\text{m/s}$.</p>"
                    "<p>a) Tính tần số nhỏ nhất để trên dây có sóng dừng.</p>"
                    "<p>b) Cho dây rung với $f=30\\ \\text{Hz}$. Trên dây có sóng dừng không? Giải thích.</p>"
                    "<p>c) Cho dây rung với $f=45\\ \\text{Hz}$. Trên dây có sóng dừng không? Nếu có, trên dây có bao nhiêu bụng, bao nhiêu nút (kể cả A và B)?</p>")),
 dict(label="Dạng 3 · Trung bình · Từ số nút tìm bước sóng và tốc độ truyền sóng", topic=T174,
      problem_html=("<p>Một sợi dây đàn hồi dài $l=1{,}5\\ \\text{m}$, hai đầu cố định, có sóng dừng khi nguồn rung với tần số $f=40\\ \\text{Hz}$. Quan sát thấy ngoài hai đầu dây còn có 4 điểm khác trên dây luôn đứng yên.</p>"
                    "<p>a) Trên dây có bao nhiêu bó sóng?</p>"
                    "<p>b) Tính bước sóng.</p>"
                    "<p>c) Tính tốc độ truyền sóng trên dây.</p>")),
 dict(label="Dạng 4 · Khó · Đổi tần số trên cùng một sợi dây", topic=T173,
      problem_html=("<p>Sợi dây đàn hồi AB dài $l=1{,}5\\ \\text{m}$, hai đầu cố định, tốc độ truyền sóng $v$ không đổi. Khi nguồn rung với tần số $f_1=42\\ \\text{Hz}$ thì trên dây có sóng dừng với 7 nút (kể cả hai đầu).</p>"
                    "<p>a) Tính tần số nhỏ nhất để trên dây có sóng dừng.</p>"
                    "<p>b) Muốn trên dây có sóng dừng với 5 nút (kể cả hai đầu) thì phải rung với tần số $f_2$ bằng bao nhiêu?</p>"
                    "<p>c) Tính tốc độ truyền sóng trên dây.</p>")),
 dict(label="Dạng 5 · Khó · Biên độ của một điểm trên dây có sóng dừng", topic="Sóng dừng",
      problem_html=("<p>Sợi dây AB dài $90\\ \\text{cm}$, hai đầu cố định, đang có sóng dừng với 3 bó sóng. Biên độ dao động tại bụng sóng là $4\\ \\text{cm}$. Điểm M trên dây cách đầu A một đoạn $5\\ \\text{cm}$.</p>"
                    "<p>a) Tính bước sóng.</p>"
                    "<p>b) Tính biên độ dao động của M.</p>"
                    "<p>c) Tìm khoảng cách nhỏ nhất từ A tới điểm có biên độ $2\\sqrt{3}\\ \\text{cm}$.</p>"
                    "<p>d) Tính bề rộng vùng dao động của một bụng sóng (khoảng cách giữa hai vị trí biên của bụng).</p>")),
 dict(label="Dạng 6 · Khó · Hai tần số liên tiếp cùng cho sóng dừng", topic=T173,
      problem_html=("<p>Sợi dây AB dài $l=0{,}75\\ \\text{m}$, hai đầu cố định. Thay đổi dần tần số nguồn rung thì thấy sóng dừng chỉ xuất hiện ở một số tần số; hai tần số liên tiếp cho sóng dừng (giữa chúng không còn tần số nào khác) là $150\\ \\text{Hz}$ và $200\\ \\text{Hz}$.</p>"
                    "<p>a) Tính tần số nhỏ nhất để trên dây có sóng dừng.</p>"
                    "<p>b) Tính tốc độ truyền sóng trên dây.</p>"
                    "<p>c) Khi dây rung với $f=200\\ \\text{Hz}$, trên dây có bao nhiêu bó sóng, bao nhiêu nút sóng (kể cả hai đầu)?</p>")),
]

# ───────────── Bảng phân tích đề ─────────────
ANALYSIS = [
 [("\"hai đầu A và B cố định\"", "Hai đầu là nút", "⚠ Hai đầu cố định: $l=k\\dfrac{\\lambda}{2}$, $k=1,2,3,\\dots$ (mỗi bó dài $\\dfrac{\\lambda}{2}$)"),
  ("\"$l=0{,}6$ m\" ... \"$v=24$ m/s\"", "$l=0{,}6$ m; $v=24$ m/s", "$\\lambda=\\dfrac{v}{f}$"),
  ("\"bước sóng dài nhất\"", "Cần $\\lambda_{max}$", "$k$ nhỏ nhất ($k=1$) cho $\\lambda$ lớn nhất"),
  ("\"tần số nhỏ nhất\"", "Cần $f_0$", "$f_0=\\dfrac{v}{\\lambda_{max}}$"),
  ("\"$f=60$ Hz ... có sóng dừng không?\"", "$f=60$ Hz", "$\\lambda=\\dfrac{v}{f}$, rồi $k=\\dfrac{2l}{\\lambda}$ phải là số nguyên"),
  ("\"bao nhiêu bó, bụng, nút\"", "Cần $k$, số bụng, số nút", "Số bụng $=k$; số nút $=k+1$ (kể cả hai đầu)")],
 [("\"đầu A cố định, đầu B ... vòng nhẹ trượt\"", "A là nút; B là bụng", "⚠ Một đầu cố định, một đầu tự do: $l=(2k+1)\\dfrac{\\lambda}{4}$, $k=0,1,2,\\dots$ (không dùng $l=k\\dfrac{\\lambda}{2}$)"),
  ("\"$l=0{,}9$ m\" ... \"$v=18$ m/s\"", "$l=0{,}9$ m; $v=18$ m/s", "$\\lambda=\\dfrac{v}{f}$"),
  ("\"tần số nhỏ nhất\"", "Cần $f_0$", "$k=0$: $l=\\dfrac{\\lambda}{4}$, suy ra $f_0=\\dfrac{v}{4l}$"),
  ("\"$f=30$ Hz ... có sóng dừng không?\"", "$f=30$ Hz", "Tính $\\dfrac{l}{\\lambda/4}$: phải là số <strong>lẻ</strong>"),
  ("\"$f=45$ Hz\"", "$f=45$ Hz", "Cùng cách: $\\dfrac{l}{\\lambda/4}=2k+1$"),
  ("\"bao nhiêu bụng, bao nhiêu nút\"", "Cần số bụng, số nút", "Số bụng = số nút $=k+1$ (kể cả A và B)")],
 [("\"hai đầu cố định\"", "Hai đầu là nút", "⚠ Hai đầu cố định: $l=k\\dfrac{\\lambda}{2}$; $k$ bó có $k+1$ nút <strong>kể cả hai đầu</strong>"),
  ("\"$l=1{,}5$ m\" ... \"$f=40$ Hz\"", "$l=1{,}5$ m; $f=40$ Hz", "$\\lambda=\\dfrac{2l}{k}$; $v=\\lambda f$"),
  ("\"ngoài hai đầu dây còn có 4 điểm khác ... luôn đứng yên\"", "4 nút ở giữa, chưa kể hai đầu", "Số nút kể cả hai đầu = số điểm đứng yên ở giữa + 2, rồi $k=$ số nút $-1$"),
  ("\"có bao nhiêu bó sóng?\"", "Cần $k$", "Giữa hai nút liên tiếp là một bó"),
  ("\"tính bước sóng\"", "Cần $\\lambda$", "$\\lambda=\\dfrac{2l}{k}$"),
  ("\"tốc độ truyền sóng\"", "Cần $v$", "$v=\\lambda f$")],
 [("\"hai đầu cố định, ... $v$ không đổi\"", "$v$, $l$ không đổi", "⚠ Hai đầu cố định, $v$ và $l$ không đổi: $f=k\\dfrac{v}{2l}$, nên $f$ tỉ lệ với số bó $k$"),
  ("\"$f_1=42$ Hz ... 7 nút (kể cả hai đầu)\"", "$f_1=42$ Hz; $n_1=7$ nút", "Số bó $k_1=n_1-1$"),
  ("\"tần số nhỏ nhất\"", "Cần $f_0$", "$f_0=\\dfrac{f_1}{k_1}$ (ứng với $k=1$)"),
  ("\"5 nút (kể cả hai đầu) ... tần số $f_2$\"", "$n_2=5$ nút; cần $f_2$", "$k_2=n_2-1$; $\\dfrac{f_2}{f_1}=\\dfrac{k_2}{k_1}$"),
  ("\"$l=1{,}5$ m\" ... \"tốc độ truyền sóng\"", "$l=1{,}5$ m; cần $v$", "$f_0=\\dfrac{v}{2l}$, suy ra $v=2lf_0$")],
 [("\"hai đầu cố định ... 3 bó sóng\"", "$l=90$ cm; $k=3$", "⚠ Hai đầu là nút: $l=k\\dfrac{\\lambda}{2}$; khoảng cách $d$ đo từ <strong>nút</strong> gần nhất"),
  ("\"biên độ tại bụng sóng là 4 cm\"", "$A_b=4$ cm", "Biên độ bụng $A_b=2A$ ($A$ là biên độ sóng tới)"),
  ("\"M cách đầu A ... 5 cm\"", "$d=5$ cm (A là nút)", "$A_M=A_b\\left|\\sin\\dfrac{2\\pi d}{\\lambda}\\right|$"),
  ("\"biên độ $2\\sqrt{3}$ cm ... khoảng cách nhỏ nhất\"", "$A_M=2\\sqrt{3}$ cm", "$\\sin\\varphi=\\dfrac{A_M}{A_b}$, lấy $\\varphi$ nhỏ nhất; $d=\\dfrac{\\varphi}{2\\pi}\\lambda$"),
  ("\"bề rộng vùng dao động của một bụng\"", "Cần bề rộng", "Bụng vung từ $+A_b$ xuống $-A_b$: bề rộng $=2A_b$ ($=4A$)")],
 [("\"hai đầu cố định\"", "Hai đầu là nút", "⚠ $f=k\\dfrac{v}{2l}$, $k=1,2,3,\\dots$: các tần số sóng dừng cách đều nhau một khoảng $f_0=\\dfrac{v}{2l}$"),
  ("\"hai tần số liên tiếp ... 150 Hz và 200 Hz\"", "$f_k=150$ Hz; $f_{k+1}=200$ Hz (chưa biết $k$)", "Hai tần số liên tiếp ứng với $k$ và $k+1$: $f_{k+1}-f_k=f_0$"),
  ("\"tần số nhỏ nhất\"", "Cần $f_0$", "$f_0=f_{k+1}-f_k$ (ứng với $k=1$)"),
  ("\"$l=0{,}75$ m ... tốc độ truyền sóng\"", "$l=0{,}75$ m; cần $v$", "$v=2lf_0$"),
  ("\"$f=200$ Hz ... bao nhiêu bó, bao nhiêu nút\"", "$f=200$ Hz", "$k=\\dfrac{f}{f_0}$; số nút $=k+1$ (kể cả hai đầu)")],
]

# ───────────── Kiến thức cần gọi lại ─────────────
R_CC = ["<strong>Khái niệm:</strong> sóng dừng do sóng tới và sóng phản xạ ngược chiều tạo ra; nút đứng yên, bụng dao động mạnh nhất.",
        "<strong>Hai đầu cố định:</strong> hai đầu đều là nút, nên $l=k\\dfrac{\\lambda}{2}$ với $k=1,2,3,\\dots$ ($k$ là số bó).",
        "<strong>Đếm:</strong> $k$ bó có $k$ bụng và $k+1$ nút (kể cả hai đầu).",
        "<strong>Công thức:</strong> $\\lambda=\\dfrac{v}{f}$ · $f_0=\\dfrac{v}{2l}$ · $v=\\lambda f$."]
R_CT = ["<strong>Khái niệm:</strong> đầu cố định luôn là nút; đầu tự do luôn là bụng.",
        "<strong>Một đầu cố định, một đầu tự do:</strong> $l=(2k+1)\\dfrac{\\lambda}{4}$ với $k=0,1,2,\\dots$ (số lẻ lần $\\dfrac{\\lambda}{4}$).",
        "<strong>Đếm:</strong> số bụng = số nút $=k+1$ (kể cả hai đầu).",
        "<strong>Công thức:</strong> $\\lambda=\\dfrac{v}{f}$ · $f_0=\\dfrac{v}{4l}$."]
R_BIEN = R_CC[:2] + ["<strong>Biên độ:</strong> điểm cách nút gần nhất đoạn $d$ có $A_M=A_b\\left|\\sin\\dfrac{2\\pi d}{\\lambda}\\right|$; $A_b=2A$ là biên độ bụng.",
                     "<strong>Bề rộng:</strong> bụng vung từ $+A_b$ xuống $-A_b$, bề rộng $=2A_b=4A$."]

SOLS = [
 sol(R_CC, [
  ("Bước sóng dài nhất (câu a)", [P("Hai đầu cố định: $l=k\\dfrac{\\lambda}{2}$. $\\lambda$ lớn nhất khi $k$ nhỏ nhất, tức $k=1$:"), M(r"\lambda_{max}=2l=2\cdot0{,}6"), A(r"\lambda_{max}=1{,}2\ \text{m}")]),
  ("Tần số nhỏ nhất", [M(r"f_0=\dfrac{v}{\lambda_{max}}=\dfrac{24}{1{,}2}"), A(r"f_0=20\ \text{Hz}")]),
  ("Bước sóng ở 60 Hz (câu b)", [M(r"\lambda=\dfrac{v}{f}=\dfrac{24}{60}"), A(r"\lambda=0{,}4\ \text{m}")]),
  ("Số bó", [P("Có sóng dừng khi $k$ là số nguyên:"), M(r"k=\dfrac{2l}{\lambda}=\dfrac{2\cdot0{,}6}{0{,}4}"), A(r"k=3"), P("$k$ nguyên nên có sóng dừng với 3 bó, tức 3 bụng.")]),
  ("Số nút (kể cả hai đầu)", [P("Hai đầu A, B đều là nút; $k$ bó thì có $k-1$ nút ở giữa:"), M(r"\text{số nút}=k+1=3+1"), A(r"4\ \text{nút (kể cả A và B)}")]),
  ("Kiểm tra", [P("3 bó dài $3\\cdot\\dfrac{0{,}4}{2}=0{,}6$ m, đúng bằng $l$ ✓."), P("$60=3\\cdot20$: tần số là bội nguyên $k=3$ của $f_0$ ✓.")])],
  ["a) $\\lambda_{max}=1{,}2\\ \\text{m}$; $f_0=20\\ \\text{Hz}$", "b) Có sóng dừng: 3 bó, 3 bụng, 4 nút"],
  "Nhận dạng: đề cho <strong>hai đầu cố định</strong>, hỏi tần số hoặc đếm bó, nút → viết $l=k\\dfrac{\\lambda}{2}$, tìm $k$ nguyên rồi đếm."),
 sol(R_CT, [
  ("Chọn điều kiện sóng dừng", [P("Đếm số đầu cố định: ở đây chỉ có một (A). B tự do nên là bụng, ứng với $\\dfrac{\\lambda}{4}$ từ nút gần nhất:"), M(r"l=(2k+1)\dfrac{\lambda}{4},\quad k=0,1,2,\dots")]),
  ("Tần số nhỏ nhất (câu a)", [P("$f$ nhỏ nhất khi $\\lambda$ lớn nhất, tức $k=0$, $l=\\dfrac{\\lambda}{4}$:"), M(r"\lambda_{max}=4l=4\cdot0{,}9=3{,}6\ \text{m}"), M(r"f_0=\dfrac{v}{\lambda_{max}}=\dfrac{18}{3{,}6}"), A(r"f_0=5\ \text{Hz}")]),
  ("Xét $f=30$ Hz (câu b)", [M(r"\lambda=\dfrac{v}{f}=\dfrac{18}{30}=0{,}6\ \text{m}\ \Rightarrow\ \dfrac{\lambda}{4}=0{,}15\ \text{m}"), M(r"\dfrac{l}{\lambda/4}=\dfrac{0{,}9}{0{,}15}"), A(r"=6")]),
  ("Kết luận ở 30 Hz", [P("$6$ là số <strong>chẵn</strong>, không có $k$ nguyên để $2k+1=6$: đầu B không thể là bụng."), A("T:Không có sóng dừng.")]),
  ("Xét $f=45$ Hz (câu c)", [M(r"\lambda=\dfrac{18}{45}=0{,}4\ \text{m}\ \Rightarrow\ \dfrac{\lambda}{4}=0{,}1\ \text{m}"), M(r"\dfrac{l}{\lambda/4}=\dfrac{0{,}9}{0{,}1}"), A(r"=9=2k+1\ \Rightarrow\ k=4")]),
  ("Số bụng và số nút", [P("Một đầu tự do: số bụng = số nút $=k+1$:"), M(r"k+1=4+1"), A(r"5\ \text{bụng và 5 nút (kể cả A và B)}")]),
  ("Kiểm tra", [P("Các tần số có sóng dừng: $(2k+1)f_0=5;\\,15;\\,25;\\,35;\\,45;\\dots$ Hz. $45$ có trong dãy, $30$ không ✓."), P("Nếu dùng nhầm $l=k\\dfrac{\\lambda}{2}$ thì $f=30$ cho $k=3$ — kết luận sai.")])],
  ["a) $f_0=5\\ \\text{Hz}$", "b) $f=30\\ \\text{Hz}$: không có sóng dừng", "c) $f=45\\ \\text{Hz}$: có sóng dừng, 5 bụng, 5 nút"],
  "Nhận dạng: <strong>một đầu tự do</strong> (vòng trượt, đầu để lỏng) → $l=(2k+1)\\dfrac{\\lambda}{4}$; kiểm tra số lần $\\dfrac{\\lambda}{4}$ có <strong>lẻ</strong> không."),
 sol(R_CC, [
  ("Số bó (câu a)", [P("Số nút kể cả hai đầu $=4+2=6$. Mà $k$ bó có $k+1$ nút:"), M(r"k+1=6\ \Rightarrow\ k=5"), A(r"k=5\ \text{bó}")]),
  ("Bước sóng (câu b)", [M(r"l=k\dfrac{\lambda}{2}\ \Rightarrow\ \lambda=\dfrac{2l}{k}=\dfrac{2\cdot1{,}5}{5}"), A(r"\lambda=0{,}6\ \text{m}")]),
  ("Tốc độ truyền sóng (câu c)", [M(r"v=\lambda f=0{,}6\cdot40"), A(r"v=24\ \text{m/s}")]),
  ("Kiểm tra", [P("Hai nút liên tiếp cách $\\dfrac{\\lambda}{2}=0{,}3$ m; $5$ bó dài $5\\cdot0{,}3=1{,}5$ m, đúng bằng $l$ ✓."), P("Đơn vị: m · Hz = m/s ✓.")])],
  ["a) 5 bó", "b) $\\lambda=0{,}6\\ \\text{m}$", "c) $v=24\\ \\text{m/s}$"],
  "Nhận dạng: đề cho <strong>số nút hoặc điểm đứng yên</strong> → đổi sang số bó $k$ (nút kể cả hai đầu $-1$), rồi $\\lambda=\\dfrac{2l}{k}$, $v=\\lambda f$."),
 sol(R_CC + ["<strong>Cùng dây, cùng $v$:</strong> $f=k\\dfrac{v}{2l}=kf_0$, nên $\\dfrac{f_2}{f_1}=\\dfrac{k_2}{k_1}$."], [
  ("Số bó ở $f_1$", [P("7 nút kể cả hai đầu, mà $k$ bó có $k+1$ nút:"), M(r"k_1=7-1"), A(r"k_1=6")]),
  ("Tần số nhỏ nhất (câu a)", [P("$f_1=k_1f_0$, tần số nhỏ nhất ứng với $k=1$:"), M(r"f_0=\dfrac{f_1}{k_1}=\dfrac{42}{6}"), A(r"f_0=7\ \text{Hz}")]),
  ("Tần số $f_2$ (câu b)", [P("5 nút kể cả hai đầu nên $k_2=4$. $v$ và $l$ không đổi:"), M(r"\dfrac{f_2}{f_1}=\dfrac{k_2}{k_1}\ \Rightarrow\ f_2=k_2f_0=4\cdot7"), A(r"f_2=28\ \text{Hz}")]),
  ("Tốc độ truyền sóng (câu c)", [M(r"f_0=\dfrac{v}{2l}\ \Rightarrow\ v=2lf_0=2\cdot1{,}5\cdot7"), A(r"v=21\ \text{m/s}")]),
  ("Kiểm tra", [P("Ở $f_2$: $\\lambda_2=\\dfrac{2l}{k_2}=\\dfrac{2\\cdot1{,}5}{4}=0{,}75$ m; $v=\\lambda_2f_2=0{,}75\\cdot28=21$ m/s ✓."), P("Ít nút hơn thì tần số thấp hơn ($28\\lt42$) ✓.")])],
  ["a) $f_0=7\\ \\text{Hz}$", "b) $f_2=28\\ \\text{Hz}$", "c) $v=21\\ \\text{m/s}$"],
  "Nhận dạng: <strong>cùng một dây</strong>, đổi tần số hoặc đổi số nút → $v$, $l$ không đổi nên $f$ tỉ lệ với số bó $k$ (không phải số nút)."),
 sol(R_BIEN, [
  ("Bước sóng (câu a)", [M(r"l=k\dfrac{\lambda}{2}\ \Rightarrow\ \lambda=\dfrac{2l}{k}=\dfrac{2\cdot90}{3}"), A(r"\lambda=60\ \text{cm}")]),
  ("Biên độ của M (câu b)", [P("A là nút, $d=5$ cm:"), M(r"A_M=A_b\left|\sin\dfrac{2\pi d}{\lambda}\right|=4\cdot\left|\sin\dfrac{2\pi\cdot5}{60}\right|=4\sin30^\circ"), A(r"A_M=2\ \text{cm}")]),
  ("Góc cần có (câu c)", [P("Cần $A_M=2\\sqrt{3}$ cm:"), M(r"\sin\varphi=\dfrac{2\sqrt{3}}{4}=\dfrac{\sqrt{3}}{2}"), P("Góc nhỏ nhất (điểm gần A nhất):"), A(r"\varphi=\dfrac{2\pi d}{\lambda}=60^\circ")]),
  ("Khoảng cách tới A", [M(r"d=\dfrac{\varphi}{360^\circ}\lambda=\dfrac{60}{360}\cdot60"), A(r"d=10\ \text{cm}")]),
  ("Bề rộng của bụng (câu d)", [P("Bụng vung từ $+A_b$ xuống $-A_b$ (bề rộng không phải biên độ):"), M(r"\text{bề rộng}=2A_b=2\cdot4"), A(r"8\ \text{cm}")]),
  ("Kiểm tra", [P("$d=10$ cm nằm trong bó đầu (dài $\\dfrac{\\lambda}{2}=30$ cm) ✓."), P("$A_M\\lt A_b$ và M gần nút nên $A_M$ nhỏ ($2\\lt4$) ✓.")])],
  ["a) $\\lambda=60\\ \\text{cm}$", "b) $A_M=2\\ \\text{cm}$", "c) $d=10\\ \\text{cm}$", "d) Bề rộng $8\\ \\text{cm}$"],
  "Nhận dạng: đề cho <strong>biên độ bụng</strong> và <strong>khoảng cách tới đầu cố định</strong> → $A_M=A_b|\\sin(2\\pi d/\\lambda)|$ với $d$ đo từ nút."),
 sol(R_CC + ["<strong>Hiệu hai tần số liên tiếp:</strong> $f_{k+1}-f_k=f_0=\\dfrac{v}{2l}$."], [
  ("Tần số nhỏ nhất (câu a)", [P("Hai tần số liên tiếp ứng với $k$ và $k+1$, chưa biết $k$. Hiệu của chúng bằng $f_0$:"), M(r"f_0=f_{k+1}-f_k=200-150"), A(r"f_0=50\ \text{Hz}")]),
  ("Tốc độ truyền sóng (câu b)", [M(r"f_0=\dfrac{v}{2l}\ \Rightarrow\ v=2lf_0=2\cdot0{,}75\cdot50"), A(r"v=75\ \text{m/s}")]),
  ("Số bó ở 200 Hz (câu c)", [M(r"f=kf_0\ \Rightarrow\ k=\dfrac{f}{f_0}=\dfrac{200}{50}"), A(r"k=4")]),
  ("Số nút (kể cả hai đầu)", [M(r"\text{số nút}=k+1=4+1"), A(r"5\ \text{nút}")]),
  ("Kiểm tra", [P("Ở 150 Hz: $k=3$; ở 200 Hz: $k=4$ — hai số bó liên tiếp ✓."), P("$\\lambda=\\dfrac{2l}{k}=\\dfrac{1{,}5}{4}=0{,}375$ m; $v=\\lambda f=0{,}375\\cdot200=75$ m/s ✓.")])],
  ["a) $f_0=50\\ \\text{Hz}$", "b) $v=75\\ \\text{m/s}$", "c) 4 bó, 5 nút"],
  "Nhận dạng: đề cho <strong>hai tần số liên tiếp</strong> mà không cho số bó → hiệu hai tần số là $f_0=\\dfrac{v}{2l}$, rồi $k=\\dfrac{f}{f_0}$."),
]

# ───────────── Từng bước tự giải ─────────────
STEPS = [
 dict(nhan_dang="Thấy <b>hai đầu cố định</b> và hỏi tần số, bó, nút → nghĩ tới <b>$l=k\\lambda/2$</b>, số nút $=k+1$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Bước sóng dài nhất", "Bước sóng dài nhất $\\lambda_{max}$ bằng bao nhiêu?", 1.2, "m", 0.02,
       loi="Lấy $\\lambda_{max}=l$ — nhưng hai đầu cố định thì $l=k\\dfrac{\\lambda}{2}$, nên với $k=1$ ra $\\lambda=2l$ (một bó chỉ dài nửa bước sóng)."),
  buoc("Tần số nhỏ nhất", "Tần số nhỏ nhất $f_0$ bằng bao nhiêu?", 20, "Hz", 0.5,
       loi="Chia $v$ cho $l$ thay vì cho $\\lambda_{max}$; $f=\\dfrac{v}{\\lambda}$ với $\\lambda$ lớn nhất ứng với $k=1$.",
       ke=[("$f_0=\\dfrac{v}{\\lambda_{max}}$ với $\\lambda_{max}$ vừa tìm", True),
           ("$f_0=\\dfrac{v}{l}$", "Chia cho $l$ là coi $\\lambda=l$; nhưng $\\lambda_{max}=2l$ vì một bó chỉ chiếm $\\dfrac{\\lambda}{2}$."),
           ("$f_0=v\\cdot\\lambda_{max}$", "Tích $v\\cdot\\lambda$ không có đơn vị Hz; tần số là $f=\\dfrac{v}{\\lambda}$.")]),
  buoc("Bước sóng khi rung 60 Hz", "Khi rung với tần số 60 Hz, bước sóng $\\lambda$ bằng bao nhiêu?", 0.4, "m", 0.01,
       loi="Dùng lại $\\lambda_{max}$ của câu a; câu b đổi tần số nên phải tính $\\lambda=\\dfrac{v}{f}$ mới.",
       ke=[("$\\lambda=\\dfrac{v}{f}$ với $f$ mới", True),
           ("Giữ nguyên $\\lambda_{max}$ vì cùng một dây", "$\\lambda$ phụ thuộc $f$ ($\\lambda=\\dfrac{v}{f}$); $v$ giữ nguyên nhưng $f$ đã đổi nên $\\lambda$ đổi."),
           ("$\\lambda=v\\cdot f$", "Tích $v\\cdot f$ không phải độ dài; $\\lambda=\\dfrac{v}{f}$.")]),
  buoc("Số bó", "Số bó sóng $k$ trên dây bằng bao nhiêu?", 3, "bó", 0,
       loi="Lấy $k=\\dfrac{l}{\\lambda}$ (quên mỗi bó chỉ dài $\\dfrac{\\lambda}{2}$) hoặc làm tròn khi $k$ không nguyên; ở đây $k=\\dfrac{2l}{\\lambda}$ và phải là số nguyên.",
       ke=[("$k=\\dfrac{2l}{\\lambda}$, và $k$ phải nguyên", True),
           ("$k=\\dfrac{l}{\\lambda}$", "Mỗi bó dài $\\dfrac{\\lambda}{2}$ chứ không phải $\\lambda$, nên $l=k\\dfrac{\\lambda}{2}$."),
           ("$k=\\dfrac{\\lambda}{2l}$", "Ngược tử và mẫu: $\\lambda$ càng ngắn thì số bó càng nhiều.")]),
  buoc("Số nút (kể cả hai đầu)", "Kể cả hai đầu A, B, trên dây có bao nhiêu nút sóng?", 4, "nút", 0,
       loi="Lấy số nút bằng số bó (quên hai đầu cũng là nút) hoặc nhân đôi cho mỗi bó; hai bó kề nhau dùng chung một nút, nên số nút $=k+1$.",
       ke=[("Số nút $=k+1$ vì hai bó kề nhau dùng chung một nút", True),
           ("Số nút $=k$", "Quên hai đầu: A và B cũng là nút (cố định), nên thêm 1."),
           ("Số nút $=2k$", "Hai bó kề nhau dùng chung nút ở giữa, không phải mỗi bó có riêng 2 nút.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>một đầu tự do</b> (vòng trượt, đầu để lỏng) → nghĩ tới <b>$l=(2k+1)\\lambda/4$</b>; xét số lần $\\lambda/4$ có lẻ không.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Chọn điều kiện sóng dừng", "Dây có một đầu cố định, một đầu tự do. Điều kiện sóng dừng nào đúng?",
       lua_chon=[("$l=(2k+1)\\dfrac{\\lambda}{4}$, $k=0,1,2,\\dots$", True),
                 ("$l=k\\dfrac{\\lambda}{2}$, $k=1,2,3,\\dots$", "Đó là điều kiện của dây hai đầu cố định (hai đầu đều là nút)."),
                 ("$l=k\\dfrac{\\lambda}{4}$ với mọi $k$ nguyên", "Cho $k$ chẵn thì đầu B lại thành nút, trái với đầu tự do luôn là bụng.")],
       loi="Dùng $l=k\\dfrac{\\lambda}{2}$ vì quen với dây đàn; cách chọn đúng là đếm số đầu cố định — ở đây chỉ có một."),
  buoc("Tần số nhỏ nhất", "Tần số nhỏ nhất $f_0$ để có sóng dừng bằng bao nhiêu?", 5, "Hz", 0.1,
       loi="Dùng $f_0=\\dfrac{v}{2l}$ của hai đầu cố định (ra gấp đôi); đầu tự do chỉ cần $l=\\dfrac{\\lambda}{4}$ nên $f_0=\\dfrac{v}{4l}$.",
       ke=[("$k=0$: $l=\\dfrac{\\lambda}{4}$, nên $f_0=\\dfrac{v}{4l}$", True),
           ("$l=\\dfrac{\\lambda}{2}$, nên $f_0=\\dfrac{v}{2l}$", "Đó là công thức hai đầu cố định; dây này có đầu tự do."),
           ("$l=\\dfrac{3\\lambda}{4}$, nên $f_0=\\dfrac{3v}{4l}$", "Đó là tần số kế tiếp ($k=1$), không phải nhỏ nhất.")]),
  buoc("Xét 30 Hz: chứa bao nhiêu lần λ/4", "Ở 30 Hz, chiều dài dây chứa bao nhiêu lần $\\dfrac{\\lambda}{4}$?", 6, None, 0,
       loi="Chia $l$ cho $\\dfrac{\\lambda}{2}$ như dây hai đầu cố định (ra 3, tưởng có 3 bó); với đầu tự do đơn vị đo là $\\dfrac{\\lambda}{4}$.",
       ke=[("Tính $\\lambda=\\dfrac{v}{f}$ rồi $\\dfrac{l}{\\lambda/4}$", True),
           ("Tính $\\dfrac{l}{\\lambda/2}$ như hai đầu cố định", "Dây này có đầu tự do: chiều dài đo bằng $\\dfrac{\\lambda}{4}$ và phải là số lẻ lần."),
           ("Lấy $\\dfrac{f}{f_0}$ rồi xem có nguyên không", "Nguyên chưa đủ: $\\dfrac{f}{f_0}$ phải là số <b>lẻ</b>.")]),
  buoc("Kết luận ở 30 Hz", "Ở 30 Hz có sóng dừng không?",
       lua_chon=[("Không — vì số lần $\\dfrac{\\lambda}{4}$ là số chẵn", True),
                 ("Có — vì số lần đó là số nguyên", "Nguyên chưa đủ: số lẻ lần $\\dfrac{\\lambda}{4}$ mới làm đầu B là bụng; số chẵn thì B thành nút, mâu thuẫn với đầu tự do."),
                 ("Có — vì 30 Hz chia hết cho $f_0$", "Chia hết chưa đủ; ví dụ 10 Hz cũng chia hết cho $f_0$ nhưng dây không có sóng dừng ở 10 Hz.")],
       loi="Thấy số nguyên là kết luận có sóng dừng; phải là số LẺ lần $\\dfrac{\\lambda}{4}$.",
       ke=[("Số lần $\\dfrac{\\lambda}{4}$ chẵn: đầu B không thể là bụng", True),
           ("Số nguyên là đủ vì $k$ nguyên", "Điều kiện là $2k+1$ lẻ chứ không chỉ nguyên."),
           ("Kết luận theo tần số lớn hơn $f_0$", "Lớn hơn $f_0$ chưa đủ; phải thuộc dãy $(2k+1)f_0$.")]),
  buoc("Xét 45 Hz: chứa bao nhiêu lần λ/4", "Ở 45 Hz, chiều dài dây chứa bao nhiêu lần $\\dfrac{\\lambda}{4}$?", 9, None, 0,
       loi="Quên đổi $f$ mới: dùng lại $\\lambda$ của câu trước; $\\lambda=\\dfrac{v}{f}$ phải tính lại.",
       ke=[("Tính lại $\\lambda=\\dfrac{v}{f}$ với $f$ mới rồi $\\dfrac{l}{\\lambda/4}$", True),
           ("Dùng lại $\\lambda$ của câu trước", "$f$ đã đổi nên $\\lambda=\\dfrac{v}{f}$ đổi theo."),
           ("Lấy $\\dfrac{l}{\\lambda/2}$", "Dây có đầu tự do nên đo bằng $\\dfrac{\\lambda}{4}$.")]),
  buoc("Số bụng và số nút", "Ở 45 Hz, trên dây có bao nhiêu bụng sóng (kể cả B)?", 5, "bụng", 0,
       loi="Dùng số bụng $=k$ của dây hai đầu cố định; một đầu tự do thì $2k+1$ là số lần $\\dfrac{\\lambda}{4}$ và số bụng = số nút $=k+1$.",
       ke=[("$2k+1$ bằng số lần vừa tìm, suy ra $k$, số bụng $=k+1$", True),
           ("Số bụng bằng số lần vừa tìm", "Mỗi bó (một bụng) chiếm $\\dfrac{\\lambda}{2}$ tức hai lần $\\dfrac{\\lambda}{4}$, nên số bụng gần bằng một nửa."),
           ("Số bụng $=k$ như hai đầu cố định", "Dây có đầu tự do: B là bụng thêm vào, nên số bụng $=k+1$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Đề cho <b>số nút hoặc điểm đứng yên</b> rồi hỏi $\\lambda$, $v$ → đổi sang số bó $k$, dùng $\\lambda=2l/k$, $v=\\lambda f$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Số bó", "Số bó sóng $k$ trên dây bằng bao nhiêu?", 5, "bó", 0,
       loi="Lấy $k$ bằng số điểm đứng yên ở giữa — quên hai đầu A, B cũng là nút; số nút kể cả hai đầu rồi mới trừ 1 ra số bó."),
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu?", 0.6, "m", 0.01,
       loi="Dùng $\\lambda=\\dfrac{l}{k}$ (quên mỗi bó dài $\\dfrac{\\lambda}{2}$) nên ra một nửa.",
       ke=[("$\\lambda=\\dfrac{2l}{k}$ vì $l=k\\dfrac{\\lambda}{2}$", True),
           ("$\\lambda=\\dfrac{l}{k}$", "Một bó dài $\\dfrac{\\lambda}{2}$ chứ không phải $\\lambda$."),
           ("$\\lambda=\\dfrac{v}{f}$ rồi so với $l$", "Chưa biết $v$, không dùng được; phải dùng số bó và chiều dài dây.")]),
  buoc("Tốc độ truyền sóng", "Tốc độ truyền sóng $v$ bằng bao nhiêu?", 24, "m/s", 0.5,
       loi="Dùng $v=\\dfrac{\\lambda}{f}$ hoặc $v=\\dfrac{f}{\\lambda}$; $v=\\lambda f$.",
       ke=[("$v=\\lambda f$", True),
           ("$v=\\dfrac{\\lambda}{f}$", "Sai: $\\dfrac{\\lambda}{f}=\\lambda T$ có đơn vị m·s, không phải m/s; $v=\\lambda f=\\dfrac{\\lambda}{T}$."),
           ("$v=\\dfrac{2l}{k}\\cdot\\dfrac{1}{f}$", "Thừa phép chia cho $f$: $\\dfrac{2l}{k}$ đã là $\\lambda$, chỉ cần nhân với $f$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>cùng một dây, đổi tần số hoặc số nút</b> → $v$, $l$ không đổi nên <b>$f$ tỉ lệ số bó $k$</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Số bó ở f₁", "Với 7 nút (kể cả hai đầu), trên dây có bao nhiêu bó?", 6, "bó", 0,
       loi="Lấy số bó bằng số nút (7); hai đầu cũng là nút, nên số bó $=$ số nút $-1$."),
  buoc("Tần số nhỏ nhất", "Tần số nhỏ nhất $f_0$ để có sóng dừng bằng bao nhiêu?", 7, "Hz", 0.1,
       loi="Lấy $f_0=f_1$ hoặc chia cho số nút; $f_1=k_1f_0$ nên chia cho số bó $k_1$.",
       ke=[("$f_0=\\dfrac{f_1}{k_1}$ với $k_1$ là số bó", True),
           ("$f_0=\\dfrac{f_1}{n_1}$ với $n_1$ là số nút", "$f$ tỉ lệ số bó chứ không phải số nút (số nút $=$ số bó $+1$)."),
           ("$f_0=f_1\\cdot k_1$", "Nhân là sai chiều: $f_1=k_1f_0$ nên $f_0$ nhỏ hơn $f_1$.")]),
  buoc("Tần số f₂", "Tần số $f_2$ để dây có sóng dừng với 5 nút (kể cả hai đầu) bằng bao nhiêu?", 28, "Hz", 0.5,
       loi="Lấy $f_2=f_1\\cdot\\dfrac{n_2}{n_1}$ bằng số nút; phải dùng số bó $k_2=n_2-1$.",
       ke=[("$f_2=k_2f_0$ với $k_2$ là số bó mới", True),
           ("$f_2=f_1\\cdot\\dfrac{n_2}{n_1}$ với $n$ là số nút", "Số nút chưa tỉ lệ với $f$; phải đổi sang số bó trước ($k=n-1$)."),
           ("$f_2=f_1-(n_1-n_2)$", "Tần số không giảm theo kiểu trừ: $f=kf_0$ tỉ lệ nhân với số bó.")]),
  buoc("Tốc độ truyền sóng", "Tốc độ truyền sóng $v$ bằng bao nhiêu?", 21, "m/s", 0.3,
       loi="Dùng $v=lf_0$ (quên hệ số 2) vì $f_0=\\dfrac{v}{2l}$, nên $v=2lf_0$.",
       ke=[("$v=2lf_0$ vì $f_0=\\dfrac{v}{2l}$", True),
           ("$v=lf_0$", "Bước sóng lớn nhất là $2l$ chứ không phải $l$, nên có hệ số 2."),
           ("$v=\\dfrac{f_0}{2l}$", "Ngược: $f_0=\\dfrac{v}{2l}$ nên $v$ nằm ở tử số.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>biên độ</b> của một điểm cách đầu cố định đoạn $d$ → nghĩ tới <b>$A_M=A_b|\\sin(2\\pi d/\\lambda)|$</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Bước sóng", "Bước sóng $\\lambda$ bằng bao nhiêu?", 60, "cm", 1,
       loi="Lấy $\\lambda=\\dfrac{l}{k}$ (ra một nửa); mỗi bó dài $\\dfrac{\\lambda}{2}$ nên $\\lambda=\\dfrac{2l}{k}$."),
  buoc("Biên độ của M", "Biên độ dao động của M bằng bao nhiêu?", 2, "cm", 0.05,
       loi="Dùng $A_M=A_b\\cdot\\dfrac{d}{\\lambda}$ hoặc $\\cos$ thay vì $\\sin$; $d$ đo từ nút nên hàm là $\\sin$ và tại nút biên độ phải bằng 0.",
       ke=[("$A_M=A_b\\left|\\sin\\dfrac{2\\pi d}{\\lambda}\\right|$ với $d$ tính từ nút", True),
           ("$A_M=A_b\\cdot\\dfrac{d}{\\lambda}$", "Biên độ không tăng đều theo $d$ mà theo hàm sin: tăng nhanh gần nút, chậm dần gần bụng."),
           ("$A_M=A_b\\left|\\cos\\dfrac{2\\pi d}{\\lambda}\\right|$", "Tại nút $d=0$ biên độ phải bằng 0 nhưng $\\cos0=1$; đo từ nút thì dùng $\\sin$.")]),
  buoc("Góc cần có", "Biên độ $2\\sqrt{3}$ cm ứng với góc $\\varphi=\\dfrac{2\\pi d}{\\lambda}$ nhỏ nhất bằng bao nhiêu độ?", 60, "°", 0.5,
       loi="Lấy $\\varphi=\\dfrac{A_M}{A_b}$ rồi đổi sang độ (tỉ số biên độ là giá trị của $\\sin\\varphi$, không phải góc).",
       ke=[("Giải $\\sin\\varphi=\\dfrac{A_M}{A_b}$, lấy góc nhỏ nhất", True),
           ("Lấy $\\varphi=\\dfrac{A_M}{A_b}$ rồi đổi sang độ", "Tỉ số biên độ là giá trị của $\\sin\\varphi$; phải lấy $\\arcsin$ mới ra góc."),
           ("Cộng thêm $180^\\circ$ cho chắc", "Cộng $180^\\circ$ sẽ sang bó kế tiếp, xa A hơn; đề hỏi điểm gần A nhất.")]),
  buoc("Khoảng cách tới A", "Khoảng cách nhỏ nhất từ A tới điểm đó bằng bao nhiêu?", 10, "cm", 0.2,
       loi="Đổi góc sang độ dài sai: $d=\\dfrac{\\varphi}{360^\\circ}\\lambda$ (góc $360^\\circ$ ứng một bước sóng), không phải $\\dfrac{\\varphi}{180^\\circ}$ hay nhân với $l$.",
       ke=[("$d=\\dfrac{\\varphi}{360^\\circ}\\lambda$", True),
           ("$d=\\dfrac{\\varphi}{180^\\circ}\\lambda$", "Góc $180^\\circ$ ứng nửa bước sóng, $360^\\circ$ mới ứng một bước sóng."),
           ("$d=\\dfrac{\\varphi}{360^\\circ}l$", "Phải nhân với bước sóng $\\lambda$ (pha ứng với $\\lambda$), không phải chiều dài dây.")]),
  buoc("Bề rộng của bụng", "Bề rộng vùng dao động của một bụng sóng bằng bao nhiêu?", 8, "cm", 0.1,
       loi="Lấy bề rộng bằng biên độ bụng; bụng vung từ $+A_b$ xuống $-A_b$ nên bề rộng $=2A_b$.",
       ke=[("Bề rộng $=2A_b$ (từ biên này sang biên kia)", True),
           ("Bề rộng $=A_b$", "$A_b$ chỉ là nửa khoảng vung (từ vị trí cân bằng ra biên)."),
           ("Bề rộng $=\\dfrac{\\lambda}{2}$", "$\\dfrac{\\lambda}{2}$ là chiều dài một bó dọc theo dây, không phải bề rộng dao động.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>hai tần số liên tiếp</b> mà không cho số bó → <b>hiệu của chúng là $f_0=v/2l$</b>, rồi $k=f/f_0$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Tần số nhỏ nhất", "Tần số nhỏ nhất $f_0$ để có sóng dừng bằng bao nhiêu?", 50, "Hz", 0.5,
       loi="Cho tần số nhỏ hơn trong hai tần số đã cho là $f_0$ — đề không nói nó ứng với $k=1$. Hai tần số liên tiếp ứng với $k$ và $k+1$, nên hiệu của chúng mới bằng $f_0$."),
  buoc("Tốc độ truyền sóng", "Tốc độ truyền sóng $v$ bằng bao nhiêu?", 75, "m/s", 1,
       loi="Dùng $v=lf_0$ (quên hệ số 2); $f_0=\\dfrac{v}{2l}$ nên $v=2lf_0$.",
       ke=[("$v=2lf_0$ vì $f_0=\\dfrac{v}{2l}$", True),
           ("$v=lf_0$", "Bước sóng lớn nhất là $2l$ chứ không phải $l$, nên có hệ số 2."),
           ("$v=\\dfrac{f_0}{2l}$", "Ngược: $f_0=\\dfrac{v}{2l}$ nên $v$ nằm ở tử số.")]),
  buoc("Số bó ở tần số lớn", "Ở tần số lớn hơn trong hai tần số trên, trên dây có bao nhiêu bó?", 4, "bó", 0,
       loi="Lấy $k=\\dfrac{f}{f_0}-1$ hoặc đoán bằng 2 vì 'hai tần số'; $f=kf_0$ nên $k=\\dfrac{f}{f_0}$.",
       ke=[("$k=\\dfrac{f}{f_0}$", True),
           ("$k=\\dfrac{f-f_0}{f_0}$", "Trừ $f_0$ làm lệch một bó: $f=kf_0$ nên $k=\\dfrac{f}{f_0}$."),
           ("$k=\\dfrac{2l}{f}$", "Chia chiều dài cho tần số không có nghĩa vật lí (đơn vị m/Hz).")]),
  buoc("Số nút", "Kể cả hai đầu, trên dây có bao nhiêu nút sóng?", 5, "nút", 0,
       loi="Lấy số nút bằng số bó; hai đầu cũng là nút nên số nút $=k+1$.",
       ke=[("Số nút $=k+1$", True),
           ("Số nút $=k$", "Quên hai đầu A, B cũng là nút."),
           ("Số nút $=2k$", "Hai bó kề nhau dùng chung một nút, không phải mỗi bó có hai nút riêng.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Đối chiếu số bằng Python độc lập ─────────────
def kiem():
    ok = True
    def chk(name, got, want, tol=1e-9):
        nonlocal ok
        good = abs(got - want) <= tol
        ok &= good
        print(("OK  " if good else "LỆCH"), name, got, want)
    # D1
    l, v = 0.6, 24
    chk("D1 λmax", 2 * l, 1.2); chk("D1 f0", v / (2 * l), 20); lam = v / 60; chk("D1 λ@60", lam, 0.4)
    k = 2 * l / lam; chk("D1 k", k, 3, 1e-9); chk("D1 nút", k + 1, 4)
    # D2: một đầu tự do
    l, v = 0.9, 18
    chk("D2 f0", v / (4 * l), 5)
    for f, expect_odd in ((30, False), (45, True)):
        lam = v / f; n = l / (lam / 4); chk(f"D2 l/(λ/4)@{f}", n, 6 if f == 30 else 9, 1e-9)
        assert (round(n) % 2 == 1) == expect_odd
    n = 9; kk = (n - 1) // 2; chk("D2 bụng=nút", kk + 1, 5)
    # liệt kê tần số có sóng dừng: (2k+1) f0
    print("D2 dãy f:", [(2 * j + 1) * 5 for j in range(6)])
    # D3
    l, f = 1.5, 40; nodes = 4 + 2; k = nodes - 1; chk("D3 k", k, 5); lam = 2 * l / k; chk("D3 λ", lam, 0.6); chk("D3 v", lam * f, 24)
    # D4
    l, f1 = 1.5, 42; k1 = 7 - 1; f0 = f1 / k1; chk("D4 f0", f0, 7); chk("D4 f2", (5 - 1) * f0, 28); v = 2 * l * f0; chk("D4 v", v, 21)
    chk("D4 kiểm λ2·f2", (2 * l / 4) * 28, 21); chk("D4 λ1 f1", (v / f1) * k1, 2 * l)  # λ1=v/f1, k1 λ1/2 = l
    # D5
    l, k, Ab, d = 90, 3, 4, 5; lam = 2 * l / k; chk("D5 λ", lam, 60)
    chk("D5 A_M", Ab * abs(math.sin(TAU * d / lam)), 2, 1e-9)
    phi = math.degrees(math.asin(2 * math.sqrt(3) / 4)); chk("D5 φ", phi, 60, 1e-9); chk("D5 d", phi / 360 * lam, 10, 1e-9)
    chk("D5 A@10cm", Ab * math.sin(TAU * 10 / lam), 2 * math.sqrt(3), 1e-9); chk("D5 bề rộng", 2 * Ab, 8)
    # D6
    l, fa, fb = 0.75, 150, 200; f0 = fb - fa; chk("D6 f0", f0, 50); v = 2 * l * f0; chk("D6 v", v, 75)
    chk("D6 k@200", fb / f0, 4); chk("D6 k@150", fa / f0, 3); chk("D6 λ·f", (2 * l / 4) * fb, 75)
    # D6: không có tần số nào nằm giữa 150 và 200 cho sóng dừng
    assert [j * f0 for j in range(1, 8) if fa < j * f0 < fb] == []
    print("TẤT CẢ KHỚP" if ok else "CÓ LỆCH")
    return ok

if "--kiem" in sys.argv:
    sys.exit(0 if kiem() else 1)

write(J, 32, "Bài 13. Sóng dừng", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J)); d["generated_at"] = "2026-10-09"
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
