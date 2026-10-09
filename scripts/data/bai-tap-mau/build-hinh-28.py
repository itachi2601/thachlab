"""Bài 28 (Bài 9. Sóng ngang, sóng dọc, sự truyền năng lượng của sóng cơ, Vật lí 11): 6 dạng bài tập mẫu.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-28.py  → ghi scripts/data/bai-tap-mau/28.json (review.checked=False)
Hình tính thật: sóng dọc (lớp khí lệch u = a·sin(ωt − kx′)), sóng ngang (tịnh tiến rigid y = A·sin(kx − ωt)), sóng tròn (r = v·t),
nón sóng cầu (cung r = v·t), hai mép sóng P, S (x = v·t)."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

_fig = fig
def fig(*a, **k):
    return re.sub(r'<text[^>]*></text>', '', _fig(*a, **k))

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "28.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
MUTE = "#94a3b8"

def anim_t(vals, dur, typ="translate"):
    return (f'<animateTransform attributeName="transform" type="{typ}" values="{";".join(vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def A_(attr, vals, dur):
    return f'<animate attributeName="{attr}" values="{";".join(vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'

# ───────────── Dạng 1: phân biệt sóng ngang / sóng dọc (đề chỉ vẽ NGUỒN và mép sóng; không vẽ chuyển động phần tử) ─────────────
def d1(k):
    p = f"d1{k}"; VB = "0 0 420 262"; b = defs(p)
    YD = 66; YT = 196
    b += lbl(16, 22, "(1) Dây thép căng ngang", "currentColor", 13, "start", "700")
    b += seg(52, YD, 400, YD, "currentColor", 2.2)
    b += lbl(16, 140, "(2) Ống chứa không khí, pit-tông ở đầu ống", "currentColor", 13, "start", "700")
    b += f'<rect x="64" y="{YT - 20}" width="336" height="40" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    hand = f'<rect x="30" y="{YD - 10}" width="18" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    pist = f'<rect x="52" y="{YT - 20}" width="12" height="40" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    if k == 0:
        cyc = 6; T = 0.8; dur = cyc * T
        hv = []; pv = []
        for i in range(cyc * 8 + 1):
            ph = 2 * math.pi * i / 8
            hv.append(f"0 {-12 * math.sin(ph):.1f}"); pv.append(f"{9 * math.sin(ph):.1f} 0")
        b += f'<g>{anim_t(hv, dur)}{hand}</g>' + f'<g>{anim_t(pv, dur)}{pist}</g>'
        fr = f'<line x1="0" y1="{YD - 14}" x2="0" y2="{YD + 14}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="4 3"/>'
        b += f'<g transform="translate(58 0)">{anim_t(["58 0", "400 0"], dur)}{fr}</g>'
        fr2 = f'<line x1="0" y1="{YT - 26}" x2="0" y2="{YT + 26}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="4 3"/>'
        b += f'<g transform="translate(66 0)">{anim_t(["66 0", "400 0"], dur)}{fr2}</g>'
    else:
        b += hand + pist
    b += lbl(39, YD - 16, "A", "currentColor", 13, "middle", "700")
    b += dim(p, "o", 20, YD - 24, 20, YD + 24, "", 0, 0) + lbl(26, YD + 40, "tay rung đầu A", ORG, 12, "start", "700")
    b += dim(p, "o", 40, YT + 36, 80, YT + 36, "", 0, 0) + lbl(88, YT + 40, "pit-tông đẩy – kéo", ORG, 12, "start", "700")
    b += arrow(p, "b", 130, YD - 22, 280, YD - 22, 3) + lbl(205, YD - 30, "dao động lan dọc dây", BLUE, 12, "middle", "700")
    b += arrow(p, "b", 230, YT - 36, 380, YT - 36, 3) + lbl(305, YT - 44, "dao động lan dọc ống", BLUE, 12, "middle", "700")
    if k == 0:
        return fig("d1-0", VB, "Tay rung đầu dây lên xuống và pit-tông đẩy kéo trong ống, dao động lan dọc dây và dọc ống", b,
                   "Mô phỏng: nguồn rung và mép sóng lan dọc dây, dọc ống (chạy chậm hàng trăm lần). Trường hợp (3) mặt hồ không vẽ. " + NOTE)
    b += lbl(210, 256, "Cần so: phương dao động với phương truyền = ?", "currentColor", 12, "middle", "700")
    return fig("d1-2", VB, "Hai trường hợp với phương dao động của nguồn (cam) và phương lan truyền (xanh dương)", b,
               "Dữ kiện: cam là phương nguồn dao động, xanh dương là phương lan truyền. " + NOTE)

# ───────────── Dạng 2: sóng tròn trên mặt hồ, v = 0,80 m/s, phao 6,0 m, lá 9,6 m ─────────────
def d2(k):
    p = f"d2{k}"; VB = "0 0 420 250"; O = (52, 112); sc = 15.0
    xp = O[0] + 6.0 * sc; xl = O[0] + 9.6 * sc; b = defs(p)
    b += seg(O[0], O[1], xl + 10, O[1], MUTE, 1.2, "4 4")
    if k == 0:
        dur = 5.0   # 20 s thật chạy trong 5 s (nhanh 4 lần)
        b += (f'<circle cx="{O[0]}" cy="{O[1]}" r="0" fill="none" stroke="{BLUE}" stroke-width="3">{A_("r", ["0", f"{0.8 * 20 * sc:.1f}"], dur)}</circle>')
    b += dot(*O, 4.5, "currentColor") + lbl(O[0] - 6, O[1] - 12, "O (sỏi rơi)", "currentColor", 12, "start", "700")
    b += dot(xp, O[1], 5.5, RED) + lbl(xp, O[1] - 14, "phao", RED, 13, "middle", "700")
    b += f'<ellipse cx="{xl}" cy="{O[1]}" rx="8" ry="4.5" fill="{GRN}" stroke="currentColor" stroke-width="1.4"/>' + lbl(xl + 4, O[1] - 14, "lá", GRN, 13, "middle", "700")
    b += dim(p, "b", O[0], 164, xp, 164, "6,0 m", (O[0] + xp) / 2 - 18, 182)
    b += dim(p, "o", O[0], 204, xl, 204, "9,6 m", (O[0] + xl) / 2 - 18, 222)
    b += lbl(16, 26, "Tốc độ sóng v = 0,80 m/s", "currentColor", 13, "start", "700")
    if k == 0:
        b += lbl(16, 48, "t₁ = ?   t₂ = ?", ORG, 13, "start", "700") + lbl(16, 70, "s(20 s) = ?   phao dời = ?", ORG, 13, "start", "700")
        return fig("d2-0", VB, "Sóng tròn lan ra từ chỗ hòn sỏi rơi, đi qua phao rồi qua chiếc lá nằm xa hơn", b,
                   "Mô phỏng: nhìn từ trên xuống, gợn sóng đầu tiên lan ra với v = 0,80 m/s (20 s thật chạy trong 5 s, nhanh 4 lần). " + NOTE)
    b += lbl(16, 48, "Hỏi: t₁ (phao), t₂ (lá)", ORG, 13, "start", "700") + lbl(16, 70, "Hỏi: s sau 20 s; độ dời của phao", ORG, 13, "start", "700")
    return fig("d2-2", VB, "Chỗ sỏi rơi, phao và lá thẳng hàng; khoảng cách từ chỗ sỏi rơi tới phao và tới lá", b,
               "Dữ kiện: hai khoảng cách tính từ chỗ sỏi rơi. " + NOTE)

# ───────────── Dạng 3: sóng âm trong ống, f = 1700 Hz, v = 340 m/s → λ = 0,2 m ─────────────
LAM3 = 96.0; X03 = 64.0; NL3 = 27; STEP3 = 12.0; TP3 = 1.0; A3 = 0.5 * LAM3 / (2 * math.pi)
def u3(i, t):
    xr = (i * STEP3 + 6.0)                    # khoảng cách từ mặt loa tới lớp i (px)
    tt = t - xr / (LAM3 / TP3)
    return 0.0 if tt < 0 else A3 * math.sin(2 * math.pi * tt / TP3)
def tube3(p, snapshot=None):
    b = f'<rect x="{X03}" y="96" width="{NL3 * STEP3 + 12:.0f}" height="60" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    sp = (f'<rect x="20" y="108" width="14" height="36" fill="none" stroke="currentColor" stroke-width="2.2"/>'
          f'<polygon points="34,108 58,92 58,160 34,144" fill="none" stroke="currentColor" stroke-width="2.2"/>')
    return b, sp
def d3(k):
    p = f"d3{k}"; VB = "0 0 420 232"; b = defs(p)
    tb, sp = tube3(p)
    b += tb
    tot = 4.4; dt = TP3 / 10; n = int(round(tot / dt))
    if k == 0:
        cone = "".join(f"{A3 * math.sin(2 * math.pi * (j * dt) / TP3) * 0.6:.1f} 0;" for j in range(n + 1))[:-1].split(";")
        b += f'<g>{anim_t(cone, tot)}{sp}</g>'
        for i in range(NL3):
            x0 = X03 + 6.0 + i * STEP3
            vals = [f"{x0 + u3(i, j * dt) - 1.2:.1f}" for j in range(n + 1)]
            b += f'<rect x="{x0 - 1.2:.1f}" y="100" width="2.4" height="52" fill="{GRN}">{A_("x", vals, tot)}</rect>'
        b += lbl(46, 184, "loa", "currentColor", 13, "middle", "700")
        b += arrow(p, "b", 150, 74, 300, 74, 3) + lbl(225, 66, "sóng âm lan theo trục ống", BLUE, 12, "middle", "700")
        b += lbl(16, 210, "f = 1700 Hz · v = 340 m/s", "currentColor", 13, "start", "700") + lbl(250, 210, "d₁ = ?  d₂ = ?", ORG, 13, "start", "700")
        return fig("d3-0", VB, "Loa phát âm vào một ống dài chứa không khí", b,
                   "Mô phỏng: các lớp khí trong ống (chạy chậm hàng nghìn lần, độ lệch phóng to; vị trí lớp khí tính theo sóng). " + NOTE)
    # k == 2: ảnh chụp tại t = tot, đánh dấu vùng nén / dãn
    b += sp
    ts = tot; xs = []
    for i in range(NL3):
        x0 = X03 + 6.0 + i * STEP3
        xs.append(x0 + u3(i, ts))
        b += f'<rect x="{xs[-1] - 1.2:.1f}" y="100" width="2.4" height="52" fill="{GRN}"/>'
    kk = 2 * math.pi / LAM3; w = 2 * math.pi / TP3
    comp = []; rare = []
    for nn in range(-3, 6):
        xr = (w * ts - 2 * math.pi * nn) / kk       # u = 0, đồ thị đi xuống → nén
        if 40 < xr < 300: comp.append(X03 + xr)
        xr2 = (w * ts - math.pi - 2 * math.pi * nn) / kk
        if 40 < xr2 < 300: rare.append(X03 + xr2)
    comp.sort(); rare.sort()
    c1, c2 = comp[0], comp[1]
    r1 = min(rare, key=lambda r: abs(r - c2) if r > c2 else 1e9)
    for c in (c1, c2):
        b += f'<polygon points="{c - 5:.1f},164 {c + 5:.1f},164 {c:.1f},156" fill="{BLUE}"/>' + lbl(c, 178, "nén", BLUE, 12, "middle", "700")
    b += f'<polygon points="{r1 - 5:.1f},164 {r1 + 5:.1f},164 {r1:.1f},156" fill="{ORG}"/>' + lbl(r1, 178, "dãn", ORG, 12, "middle", "700")
    b += dim(p, "b", c1, 54, c2, 54, "d₁ = ?", (c1 + c2) / 2 - 22, 44)
    b += dim(p, "o", c2 + 2, 86, r1, 86, "d₂ = ?", (c2 + r1) / 2 - 22, 76)
    b += lbl(16, 210, "Đề cho: f, v → cần λ rồi d₁, d₂", "currentColor", 13, "start", "700")
    return fig("d3-2", VB, "Ảnh chụp các lớp khí tại một lúc, đánh dấu hai vùng nén liên tiếp và một vùng dãn", b,
               "Dữ kiện: hỏi khoảng cách hai vùng nén liên tiếp và khoảng cách giữa vùng nén với vùng dãn kề nó. " + NOTE)

# ───────────── Dạng 4: bốn lần vẩy dây, v = 2,0 m/s ─────────────
LANS = [(5.0, 1.0), (15.0, 1.0), (5.0, 0.5), (3.0, 2.5)]       # (A cm, f Hz)
YC4 = [60, 130, 202, 268]; PXCM = 1.8; PXM = 40.0; V4 = 2.0
def sine_path(x_a, x_b, lam, amp, yc):
    """Đường sin y = yc − amp·sin(2π(x − x_a)/λ) bằng các cung Bézier bậc 3 (mỗi nửa bước sóng một cung), từ x_a tới ≥ x_b."""
    h = lam / 2; d = f"M{x_a:.1f},{yc:.1f}"; x = x_a; s = 1
    H = 4 / 3 * amp; a = 4 / 3 * h / math.pi
    while x < x_b:
        d += f" C{x + a:.1f},{yc - s * H:.1f} {x + h - a:.1f},{yc - s * H:.1f} {x + h:.1f},{yc:.1f}"
        x += h; s = -s
    return d
def d4(k):
    p = f"d4{k}"; VB = "0 0 420 292"; b = defs(p); XL, XR = 20.0, 400.0; run = 4.0
    names = ["Lần 1", "Lần 2", "Lần 3", "Lần 4"]
    for j, ((A, f), yc) in enumerate(zip(LANS, YC4)):
        lam = V4 / f * PXM; amp = A * PXCM
        lab = f"{names[j]} · A = {str(A).replace('.', ',')} cm · f = {str(f).replace('.', ',')} Hz"
        b += lbl(XL, yc - 32, lab, "currentColor", 12, "start", "700")
        b += seg(XL, yc, XR, yc, MUTE, 1, "4 4")
        xa = XL - math.ceil(V4 * PXM * run / (lam / 2)) * (lam / 2)
        path = sine_path(xa, XR + lam, lam, amp, yc)
        cid = f"{p}-c{j}"
        if k == 0:
            b += (f'<clipPath id="{cid}"><rect x="{XL}" y="{yc - 36}" width="{XR - XL}" height="72"/></clipPath>'
                  f'<g clip-path="url(#{cid})"><g>{anim_t(["0 0", f"{V4 * PXM * run:.1f} 0"], run)}<path d="{path}" fill="none" stroke="{GRN}" stroke-width="2.4"/></g></g>')
        else:
            b += (f'<clipPath id="{cid}"><rect x="{XL}" y="{yc - 36}" width="{XR - XL}" height="72"/></clipPath>'
                  f'<g clip-path="url(#{cid})"><path d="{path}" fill="none" stroke="{GRN}" stroke-width="2.4"/></g>')
    if k == 0:
        return fig("d4-0", VB, "Bốn lần vẩy dây với biên độ và tần số khác nhau; sóng lan cùng tốc độ trên cùng một sợi dây", b,
                   "Mô phỏng: sóng chạy sang phải với v = 2,0 m/s đúng thời gian thật (4 s); biên độ vẽ phóng to khoảng 4 lần cho dễ nhìn. " + NOTE)
    b += lbl(XR, 284, "Hỏi: E₂/E₁, E₃/E₁, E₄/E₁; A để E gấp 4", ORG, 12, "end", "700")
    return fig("d4-2", VB, "Bốn lần vẩy dây với các cặp biên độ và tần số cho trước", b,
               "Dữ kiện: mỗi lần là một cặp (A, f); tốc độ truyền như nhau. " + NOTE)

# ───────────── Dạng 5: nguồn điểm, nón sóng cầu ─────────────
def d5(k):
    p = f"d5{k}"; VB = "0 0 420 232"; O = (36, 108); sc = 42.0; th = math.radians(20); rmax = 7.0 * sc
    b = defs(p)
    for sgn in (-1, 1):
        b += seg(O[0], O[1], O[0] + rmax * math.cos(th), O[1] + sgn * rmax * math.sin(th), MUTE, 1.4, "5 4")
    b += seg(O[0], O[1], O[0] + rmax, O[1], MUTE, 1, "3 4")
    xM = O[0] + 3.0 * sc; xN = O[0] + 6.0 * sc
    if k == 0:
        fr = 14; vals = []
        for j in range(fr + 1):
            r = max(4.0, rmax * j / fr)
            x2 = O[0] + r * math.cos(th); y1 = O[1] + r * math.sin(th); y2 = O[1] - r * math.sin(th)
            vals.append(f"M{x2:.1f},{y1:.1f} A{r:.1f},{r:.1f} 0 0 0 {x2:.1f},{y2:.1f}")
        b += (f'<path d="{vals[0]}" fill="none" stroke="{BLUE}" stroke-width="3">{A_("d", vals, 3.0)}</path>')
    b += dot(*O, 5, RED) + lbl(O[0] - 4, O[1] + 24, "nguồn O", RED, 12, "start", "700")
    b += dot(xM, O[1], 4.5, "currentColor") + lbl(xM + 6, O[1] - 8, "M", "currentColor", 13, "start", "700")
    b += dot(xN, O[1], 4.5, "currentColor") + lbl(xN + 6, O[1] - 8, "N", "currentColor", 13, "start", "700")
    b += seg(xM, O[1] - 22, xM, O[1] + 22, ORG, 4) + lbl(xM + 6, O[1] + 40, "tấm S", ORG, 12, "start", "700")
    b += dim(p, "b", O[0], 172, xM, 172, "3,0 m", (O[0] + xM) / 2 - 18, 190)
    b += dim(p, "o", O[0], 204, xN, 204, "6,0 m", (O[0] + xN) / 2 - 18, 222)
    b += lbl(16, 16, "I₁ = 0,020 W/m² tại M", "currentColor", 12, "start", "700") + lbl(16, 34, "I₂ = ? tại N", ORG, 12, "start", "700") + lbl(16, 52, "P = ?", ORG, 12, "start", "700")
    if k == 0:
        return fig("d5-0", VB, "Sóng từ nguồn điểm lan ra mọi phía; trong một nón nhỏ, mặt sóng là cung tròn ngày càng dài", b,
                   "Mô phỏng: mặt sóng (một nón nhỏ) lan ra, cung càng dài khi càng xa nguồn (chạy chậm hàng trăm lần). " + NOTE)
    b += lbl(16, 88, "Tấm S = 0,50 m², t = 10 phút", "currentColor", 12, "start", "700")
    return fig("d5-2", VB, "Nguồn điểm O, hai điểm M và N cùng phương, tấm hứng S đặt tại M vuông góc phương truyền", b,
               "Dữ kiện: I₁ tại M, hỏi P, I₂ tại N, năng lượng qua tấm. " + NOTE)

# ───────────── Dạng 6: sóng P, S từ cùng tâm chấn, d = 252 km ─────────────
def d6(k):
    p = f"d6{k}"; VB = "0 0 420 214"; X0 = 36.0; sc = 1.2; xs_ = X0 + 252 * sc; YP, YS = 70, 122; b = defs(p)
    for y in (YP, YS):
        b += seg(X0, y, xs_, y, MUTE, 1.4, "4 4")
    b += seg(xs_, YP - 14, xs_, YS + 14, "currentColor", 2.2) + lbl(xs_, YS + 36, "trạm đo", "currentColor", 13, "middle", "700")
    b += dot(X0, (YP + YS) / 2, 6, RED) + lbl(X0 + 2, YS + 36, "tâm chấn", RED, 13, "middle", "700")
    b += lbl(X0 + 6, YP - 12, "sóng P (dọc) · 6,0 km/s", BLUE, 12, "start", "700") + lbl(X0 + 6, YS - 12, "sóng S (ngang) · 3,5 km/s", ORG, 12, "start", "700")
    b += dim(p, "g", X0, 176, xs_, 176, "d = ?", (X0 + xs_) / 2 - 16, 196)
    if k == 0:
        n = 12; ts = [0.5 * j for j in range(n + 1)]                     # 12 s mô phỏng... 6 s sim = 72 s thật
        def pos(v, ts_):
            return [X0 + min(v * 12 * t, 252) * sc for t in ts_]
        px = pos(6.0, ts); sx = pos(3.5, ts)
        b += f'<circle cx="{px[0]:.1f}" cy="{YP}" r="6" fill="{BLUE}" stroke="currentColor" stroke-width="1.4">{A_("cx", [f"{v:.1f}" for v in px], 6.0)}</circle>'
        b += f'<circle cx="{sx[0]:.1f}" cy="{YS}" r="6" fill="{ORG}" stroke="currentColor" stroke-width="1.4">{A_("cx", [f"{v:.1f}" for v in sx], 6.0)}</circle>'
        b += lbl(xs_ + 10, (YP + YS) / 2 + 4, "Δt = 30 s", "currentColor", 12, "start", "700")
        return fig("d6-0", VB, "Hai mép sóng P và S rời tâm chấn cùng lúc; sóng P nhanh hơn nên tới trạm đo trước", b,
                   "Mô phỏng: hai mép sóng đi cùng một quãng (vẽ tách hai hàng cho dễ nhìn); nhanh 12 lần (72 s thật chạy trong 6 s). " + NOTE)
    b += lbl(xs_ + 10, (YP + YS) / 2 + 4, "Δt = 30 s", "currentColor", 12, "start", "700")
    b += lbl(210, 20, "Đề cho: vP, vS, Δt", "currentColor", 13, "middle", "700")
    return fig("d6-2", VB, "Tâm chấn và trạm đo; sóng P và sóng S đi cùng quãng d với hai tốc độ khác nhau", b,
               "Dữ kiện: hai sóng đi cùng quãng d, tới trạm cách nhau Δt. " + NOTE)

BUILD = [d1, d2, d3, d4, d5, d6]

# ───────────── đề (xếp dễ → khó) ─────────────
T166 = "Phân biệt sóng ngang và sóng dọc"
T167 = "Sóng truyền năng lượng, không truyền phần tử môi trường"
DANG = [
 dict(label="Dạng 1 · Dễ · Phân biệt sóng ngang và sóng dọc", topic=T166,
      problem_html=("<p>Xét ba trường hợp sóng cơ lan truyền:</p>"
        "<ol><li>Một sợi dây thép dài căng ngang. Tay rung đầu A của dây lên – xuống theo phương thẳng đứng, dao động lan dọc theo dây.</li>"
        "<li>Một ống dài chứa không khí, đầu ống có pit-tông. Pit-tông đẩy – kéo qua lại dọc theo trục ống, dao động lan dọc theo ống.</li>"
        "<li>Mặt hồ yên lặng. Hòn sỏi rơi xuống, gợn tròn lan ra mọi phía; chiếc phao trên mặt hồ nhấp nhô lên – xuống.</li></ol>"
        "<p>a) Với mỗi trường hợp, phương dao động của phần tử môi trường so với phương truyền sóng là vuông góc hay trùng nhau? Đó là sóng ngang hay sóng dọc?</p>"
        "<p>b) Trong lòng một khối khí, truyền được sóng ở trường hợp (1) hay ở trường hợp (2)? Vì sao?</p>"
        "<p>c) Tay rung đầu A nhanh gấp đôi. Sóng ở trường hợp (1) có chuyển thành sóng dọc không? Vì sao?</p>")),
 dict(label="Dạng 2 · Trung bình · Sóng truyền đi cái gì, phần tử môi trường ở lại", topic=T167,
      problem_html=("<p>Hòn sỏi rơi xuống mặt hồ yên lặng tại điểm O, tạo sóng tròn lan ra với tốc độ $v=0{,}80\\ \\text{m/s}$. "
        "Chiếc phao câu cách O $6{,}0\\ \\text{m}$; chiếc lá cách O $9{,}6\\ \\text{m}$ (O, phao, lá thẳng hàng, cùng một phía). Bỏ qua sự yếu dần của sóng.</p>"
        "<p>a) Kể từ lúc sỏi rơi, sau bao lâu phao bắt đầu nhấp nhô? Sau bao lâu thì lá bắt đầu nhấp nhô?</p>"
        "<p>b) Sau $20\\ \\text{s}$ kể từ lúc sỏi rơi, sóng đã lan tới cách O bao xa? Phao đã dời xa O thêm bao nhiêu theo phương truyền sóng?</p>"
        "<p>c) Từ O tới phao, sóng đã truyền đi nước ở O hay năng lượng dao động?</p>")),
 dict(label="Dạng 3 · Trung bình · Sóng dọc: vùng nén, vùng dãn và bước sóng", topic=T166,
      problem_html=("<p>Một loa nhỏ phát âm tần số $f=1700\\ \\text{Hz}$ vào một ống dài chứa không khí. Tốc độ truyền âm trong không khí $v=340\\ \\text{m/s}$. Coi sóng chỉ truyền dọc theo trục ống.</p>"
        "<p>a) Sóng âm trong ống là sóng ngang hay sóng dọc? Tính bước sóng.</p>"
        "<p>b) Tính khoảng cách giữa hai vùng nén liên tiếp, và giữa một vùng nén với vùng dãn gần nó nhất.</p>"
        "<p>c) Tính khoảng cách từ vùng nén thứ nhất đến vùng nén thứ sáu.</p>"
        "<p>d) Tại một lúc, lớp khí ở điểm M lệch cực đại theo chiều truyền sóng so với vị trí cân bằng của nó (li độ $u=+A$). M thuộc vùng nén, vùng dãn, hay không thuộc vùng nào trong hai vùng đó?</p>")),
 dict(label="Dạng 4 · Trung bình · Năng lượng sóng tỉ lệ $A^2$ và $f^2$", topic=T167,
      problem_html=("<p>Người ta vẩy đầu một sợi dây dài, mềm để tạo sóng ngang lan trên dây. Tốc độ truyền sóng trên dây không đổi, $v=2{,}0\\ \\text{m/s}$. "
        "Năng lượng sóng truyền qua một điểm của dây trong mỗi giây tỉ lệ với $A^2$ và $f^2$ (trên cùng một sợi dây). "
        "Lần 1: $A_1=5{,}0\\ \\text{cm}$, $f_1=1{,}0\\ \\text{Hz}$.</p>"
        "<p>Năng lượng sóng truyền qua mỗi giây ở các lần sau gấp bao nhiêu lần lần 1?</p>"
        "<p>a) Lần 2: $A_2=15\\ \\text{cm}$, $f_2=1{,}0\\ \\text{Hz}$.</p>"
        "<p>b) Lần 3: $A_3=5{,}0\\ \\text{cm}$, $f_3=0{,}50\\ \\text{Hz}$.</p>"
        "<p>c) Lần 4: $A_4=3{,}0\\ \\text{cm}$, $f_4=2{,}5\\ \\text{Hz}$.</p>"
        "<p>d) Giữ $f=1{,}0\\ \\text{Hz}$, cần biên độ bao nhiêu để năng lượng truyền qua mỗi giây gấp 4 lần lần 1?</p>")),
 dict(label="Dạng 5 · Khó · Cường độ sóng: nguồn điểm và tấm hứng", topic=T167,
      problem_html=("<p>Một nguồn âm điểm phát đều theo mọi phương trong không khí. Bỏ qua sự hấp thụ âm của môi trường. "
        "Tại điểm M cách nguồn $r_1=3{,}0\\ \\text{m}$, cường độ âm là $I_1=0{,}020\\ \\text{W/m}^2$.</p>"
        "<p>a) Tính công suất của nguồn.</p>"
        "<p>b) Tính cường độ âm tại điểm N cách nguồn $r_2=6{,}0\\ \\text{m}$ (N và M cùng phương truyền).</p>"
        "<p>c) Một tấm phẳng diện tích $S=0{,}50\\ \\text{m}^2$ đặt tại M, vuông góc với phương truyền sóng. Tính năng lượng sóng truyền qua tấm trong $10$ phút.</p>")),
 dict(label="Dạng 6 · Nâng cao · Sóng P và sóng S từ cùng tâm chấn", topic=T166,
      problem_html=("<p>Một trận động đất phát ra đồng thời hai loại sóng địa chấn, cùng truyền theo một đường trong lớp vỏ Trái Đất: "
        "sóng P (sóng dọc) với $v_P=6{,}0\\ \\text{km/s}$ và sóng S (sóng ngang) với $v_S=3{,}5\\ \\text{km/s}$. "
        "Một trạm đo ghi được sóng P tới trước sóng S $\\Delta t=30\\ \\text{s}$ (số minh hoạ).</p>"
        "<p>a) Lõi ngoài của Trái Đất ở thể lỏng. Sóng nào trong hai sóng trên không truyền qua được lõi ngoài? Vì sao?</p>"
        "<p>b) Tâm chấn cách trạm đo bao nhiêu kilômét?</p>"
        "<p>c) Kể từ lúc xảy ra động đất, sóng P tới trạm sau bao lâu?</p>")),
]
FORMS = ["ly_thuyet", "ly_thuyet", "ly_thuyet", "ly_thuyet", "bai_tap", "ly_thuyet"]

# ───────────── bảng phân tích đề ─────────────
ANALYSIS = [
 [("\"sóng cơ lan truyền\"", "Ba trường hợp cần gọi tên", "Sóng cơ: dao động cơ lan truyền trong môi trường vật chất"),
  ("\"phương dao động … so với phương truyền sóng\"", "Hai phương cần so sánh", "⚠ Gọi tên bằng cách so phương dao động của phần tử với phương truyền sóng; không so với mặt đất, không so với hướng của dây"),
  ("\"(1) … rung đầu A lên – xuống … lan dọc theo dây\"", "Dao động: thẳng đứng. Truyền: dọc dây", "Sóng ngang: dao động vuông góc phương truyền · Sóng dọc: dao động trùng phương truyền"),
  ("\"(2) … đẩy – kéo … dọc theo trục ống\"", "Dao động: dọc trục. Truyền: dọc ống", "So hai phương như trên"),
  ("\"(3) … gợn tròn lan ra … phao nhấp nhô lên – xuống\"", "Dao động: lên – xuống. Truyền: ngang mặt hồ", "So hai phương như trên"),
  ("\"trong lòng một khối khí\"", "Môi trường khí", "Mỗi loại sóng cần lực đàn hồi nào của môi trường: khi trượt hay khi nén – dãn?"),
  ("\"rung nhanh gấp đôi\"", "Tần số tăng gấp đôi", "Loại sóng do đại lượng nào quyết định: tần số hay hai phương?")],
 [("\"sóng tròn lan ra với tốc độ $v=0{,}80$ m/s\"", "$v=0{,}80$ m/s", "Sóng lan đều: quãng sóng đi $s=vt$"),
  ("\"phao … cách O 6,0 m; lá … cách O 9,6 m\"", "$s_1=6{,}0$ m; $s_2=9{,}6$ m (đều tính từ O)", "Sóng tới một điểm sau $t=\\dfrac{s}{v}$"),
  ("\"bỏ qua sự yếu dần của sóng\"", "Sóng vẫn đủ mạnh làm phao, lá nhấp nhô", "⚠ Phân biệt quãng đường của sóng với quãng đường của phần tử môi trường"),
  ("\"bắt đầu nhấp nhô\"", "Mốc: lúc sóng tới", "Phần tử chỉ dao động khi sóng tới nó"),
  ("\"sau 20 s kể từ lúc sỏi rơi\"", "$t=20$ s, tính từ lúc sỏi rơi", "⚠ Gốc thời gian là lúc sỏi rơi, không phải lúc sóng tới phao"),
  ("\"phao đã dời xa O thêm bao nhiêu\"", "Độ dời theo phương truyền sóng", "Vị trí cân bằng của phần tử; độ dời so với vị trí ban đầu"),
  ("\"truyền đi nước … hay năng lượng dao động\"", "Chọn thứ được truyền", "Sóng truyền đi những gì, và những gì ở lại tại chỗ")],
 [("\"loa … tần số $f=1700$ Hz\"", "$f=1700$ Hz", "Bước sóng $\\lambda=\\dfrac{v}{f}$"),
  ("\"tốc độ truyền âm … $v=340$ m/s\"", "$v=340$ m/s; môi trường là khí", "⚠ Môi trường khí: lực đàn hồi xuất hiện theo kiểu nào? Từ đó xét loại sóng"),
  ("\"hai vùng nén liên tiếp\"", "Cần khoảng cách d₁", "Hai vùng nén liên tiếp cùng trạng thái: cách nhau mấy lần λ?"),
  ("\"vùng nén với vùng dãn gần nó nhất\"", "Cần khoảng cách d₂", "Vùng nén và vùng dãn gần nhất: trạng thái giống hay ngược nhau, cách nhau mấy phần λ?"),
  ("\"vùng nén thứ nhất đến vùng nén thứ sáu\"", "Cần khoảng cách d₃", "⚠ Đếm số khoảng $\\lambda$ giữa hai vùng nén, không đếm số vùng"),
  ("\"li độ $u=+A$ … điểm M\"", "Độ lệch cực đại của riêng lớp khí M", "⚠ Điều gì quyết định một chỗ là nén hay dãn?")],
 [("\"năng lượng … tỉ lệ với $A^2$ và $f^2$\"", "$E\\sim A^2f^2$", "$\\dfrac{E_n}{E_1}=\\left(\\dfrac{A_n}{A_1}\\right)^2\\left(\\dfrac{f_n}{f_1}\\right)^2$"),
  ("\"trên cùng một sợi dây\"; \"tốc độ … không đổi $v=2{,}0$ m/s\"", "$v=2{,}0$ m/s (dữ kiện không dùng)", "⚠ Tỉ lệ chỉ so trong cùng một môi trường; $v$ không có mặt trong tỉ số"),
  ("\"Lần 2: $A_2=15$ cm, $f_2=1{,}0$ Hz\"", "$\\dfrac{A_2}{A_1}=3$; $\\dfrac{f_2}{f_1}=1$", "Chỉ một đại lượng đổi: tỉ số bình phương của đại lượng đó"),
  ("\"Lần 3: $A_3=5{,}0$ cm, $f_3=0{,}50$ Hz\"", "$\\dfrac{A_3}{A_1}=1$; $\\dfrac{f_3}{f_1}=0{,}5$", "Chỉ một đại lượng đổi: tỉ số bình phương của đại lượng đó"),
  ("\"Lần 4: $A_4=3{,}0$ cm, $f_4=2{,}5$ Hz\"", "$\\dfrac{A_4}{A_1}=0{,}6$; $\\dfrac{f_4}{f_1}=2{,}5$", "⚠ Hai đại lượng cùng đổi: nhân hai tỉ số bình phương, không cộng"),
  ("\"giữ $f=1{,}0$ Hz … gấp 4 lần\"", "$\\dfrac{E}{E_1}=4$, $f$ không đổi", "Còn lại $\\left(\\dfrac{A}{A_1}\\right)^2=4$; cần $A$")],
 [("\"nguồn âm điểm phát đều theo mọi phương\"", "Sóng lan trên mặt cầu bán kính $r$", "⚠ Chỉ dùng $S=4\\pi r^2$ khi nguồn điểm, phát đều mọi hướng"),
  ("\"bỏ qua sự hấp thụ âm\"", "Năng lượng không mất đi", "⚠ Công suất qua mọi mặt cầu quanh nguồn đều bằng $P$"),
  ("\"tại M cách nguồn 3,0 m, cường độ $I_1=0{,}020$ W/m²\"", "$r_1=3{,}0$ m; $I_1=0{,}020$ W/m²", "Cường độ sóng $I=\\dfrac{P}{S}$; $P=I\\cdot S$"),
  ("\"công suất của nguồn\"", "Cần $P$", "$P=I_1\\cdot4\\pi r_1^2$"),
  ("\"tại N cách nguồn 6,0 m\"", "$r_2=6{,}0$ m", "$I=\\dfrac{P}{4\\pi r^2}$: $I$ tỉ lệ nghịch với $r^2$"),
  ("\"tấm … vuông góc với phương truyền … trong 10 phút\"", "$S=0{,}50$ m²; $t=10$ phút", "⚠ Tấm vuông góc phương truyền mới dùng $I$ trực tiếp; đổi phút ra giây; $E=I\\,S\\,t$")],
 [("\"sóng P (dọc) … sóng S (ngang)\"", "$v_P=6{,}0$ km/s; $v_S=3{,}5$ km/s", "Sóng dọc, sóng ngang cần lực đàn hồi khác nhau của môi trường"),
  ("\"lõi ngoài … thể lỏng\"", "Môi trường lỏng", "⚠ Môi trường lỏng: nhớ lại sóng dọc, sóng ngang mỗi loại cần môi trường nào"),
  ("\"đồng thời … cùng truyền theo một đường\"", "Cùng quãng $d$, cùng gốc thời gian", "$t=\\dfrac{d}{v}$ cho từng sóng"),
  ("\"P tới trước S $\\Delta t=30$ s\"", "$\\Delta t=30$ s", "⚠ $\\Delta t$ là hiệu hai thời gian truyền: $t_S-t_P=\\Delta t$"),
  ("\"tâm chấn cách trạm đo bao nhiêu km\"", "Cần $d$", "Thay $t=\\dfrac{d}{v}$ vào hiệu hai thời gian, giải ra $d$"),
  ("\"sóng P tới trạm sau bao lâu\"", "Cần $t_P$", "$t_P=\\dfrac{d}{v_P}$")],
]

# ───────────── lời giải ─────────────
NGANG_DOC = ["Sóng ngang: phần tử dao động vuông góc phương truyền · sóng dọc: phần tử dao động trùng phương truyền",
             "Sóng ngang truyền trong chất rắn và trên mặt chất lỏng · sóng dọc truyền trong rắn, lỏng, khí"]
SOLS = [
 sol(["Sóng cơ là dao động cơ lan truyền trong môi trường vật chất"] + NGANG_DOC +
     ["⚠ Điều kiện: gọi tên sóng bằng cách so hai phương; không dựa vào hướng của dây, của ống hay vào tần số"], [
  ("Trường hợp (1): dây căng ngang", [P("Phương truyền: dọc dây (nằm ngang). Phương dao động của phần tử dây: thẳng đứng."), P("Hai phương vuông góc."), A("T:(1) là sóng ngang")]),
  ("Trường hợp (2): ống khí", [P("Phương truyền: dọc ống. Phương dao động của lớp khí: dọc trục ống."), P("Hai phương trùng nhau."), A("T:(2) là sóng dọc")]),
  ("Trường hợp (3): mặt hồ", [P("Phương truyền: nằm ngang trên mặt nước. Phao nhấp nhô lên – xuống: dao động thẳng đứng."), P("Hai phương vuông góc."), A("T:(3) là sóng ngang")]),
  ("Môi trường khí", [P("Sóng ngang cần lực đàn hồi khi lớp này trượt lên lớp kia. Khí không có lực đó."), P("Khí chỉ có lực đàn hồi khi bị nén – dãn."), A("T:Khối khí truyền được sóng ở (2), không truyền được sóng ở (1)")]),
  ("Đổi tần số", [P("Rung nhanh hơn đổi chu kì và bước sóng. Phương dao động vẫn thẳng đứng, phương truyền vẫn dọc dây."), A("T:Sóng ở (1) vẫn là sóng ngang")])],
  ["a) (1) sóng ngang; (2) sóng dọc; (3) sóng ngang", "b) Sóng ở (2); khí chỉ có lực đàn hồi khi nén – dãn", "c) Không; loại sóng do hai phương quyết định, không do tần số"],
  "Nhận dạng: đề cho <strong>phương dao động</strong> và <strong>phương truyền</strong> → so hai phương: vuông góc là sóng ngang, trùng là sóng dọc."),

 sol(["Sóng lan đều: quãng sóng đi được $s=vt$, sóng tới một điểm cách nguồn $s$ sau $t=\\dfrac{s}{v}$",
      "Phần tử môi trường dao động quanh vị trí cân bằng, không đi theo sóng",
      "Sóng truyền đi năng lượng và trạng thái dao động",
      "⚠ Điều kiện: $s=vt$ là quãng của sóng; gốc thời gian là lúc sỏi rơi"], [
  ("Thời gian sóng tới phao", [P("Sóng đi đều từ O:"), M(r"t_1=\dfrac{s_1}{v}=\dfrac{6{,}0}{0{,}80}"), A(r"t_1=7{,}5\ \text{s}")]),
  ("Thời gian sóng tới lá", [M(r"t_2=\dfrac{s_2}{v}=\dfrac{9{,}6}{0{,}80}"), A(r"t_2=12\ \text{s}")]),
  ("Quãng sóng đi sau 20 s", [P("Gốc thời gian là lúc sỏi rơi:"), M(r"s=vt=0{,}80\cdot20"), A(r"s=16\ \text{m}")]),
  ("Độ dời của phao", [P("Phao chỉ nhấp nhô lên – xuống quanh vị trí cũ, không đi theo sóng."), A("T:Độ dời theo phương truyền: gần như bằng 0")]),
  ("Sóng truyền đi cái gì", [P("Phao nhấp nhô tức là nhận được năng lượng dao động từ O. Nước ở O không chảy tới phao."), A("T:Truyền năng lượng (và trạng thái dao động)")]),
  ("Kiểm tra", [P("Lá xa O hơn phao nên nhận sóng muộn hơn: $12\\ \\text{s}\\gt7{,}5\\ \\text{s}$ ✓"), P("Sóng đã vượt qua cả phao lẫn lá sau $20\\ \\text{s}$: $16\\ \\text{m}\\gt9{,}6\\ \\text{m}$ ✓")])],
  ["a) $t_1=7{,}5\\ \\text{s}$; $t_2=12\\ \\text{s}$", "b) Sóng cách O $16\\ \\text{m}$; phao gần như không dời", "c) Năng lượng dao động"],
  "Nhận dạng: đề có <strong>phao nhấp nhô khi sóng tới</strong> → $s=vt$ là quãng của sóng; phao ở lại chỗ cũ."),

 sol(["Sóng âm trong không khí là sóng dọc: lớp khí dao động dọc theo phương truyền",
      "Bước sóng $\\lambda=\\dfrac{v}{f}$",
      "Hai vùng nén liên tiếp cách nhau $\\lambda$; vùng nén và vùng dãn gần nhất cách nhau $\\dfrac{\\lambda}{2}$",
      "⚠ Điều kiện: vùng nén, vùng dãn do khoảng cách giữa các lớp khí kề nhau quyết định, không do độ lệch của riêng một lớp"], [
  ("Loại sóng và bước sóng", [P("Âm truyền trong khí nên là sóng dọc."), M(r"\lambda=\dfrac{v}{f}=\dfrac{340}{1700}"), A(r"\lambda=0{,}2\ \text{m}")]),
  ("Hai vùng nén liên tiếp", [P("Cách nhau đúng một bước sóng:"), A(r"d_1=\lambda=0{,}2\ \text{m}")]),
  ("Vùng nén – vùng dãn gần nhất", [M(r"d_2=\dfrac{\lambda}{2}=\dfrac{0{,}2}{2}"), A(r"d_2=0{,}1\ \text{m}")]),
  ("Từ nén thứ nhất đến nén thứ sáu", [P("Từ vùng 1 đến vùng 6 có $6-1=5$ khoảng, mỗi khoảng $\\lambda$:"), M(r"d_3=5\lambda=5\cdot0{,}2"), A(r"d_3=1{,}0\ \text{m}")]),
  ("Điểm M có $u=+A$", [P("Tại M, lớp khí lệch xa nhất, nhưng hai lớp ngay hai bên M cũng lệch gần bằng thế. Khoảng cách giữa chúng gần như không đổi."), A("T:M không thuộc vùng nén lẫn vùng dãn (nén, dãn đều ở chỗ $u=0$)")]),
  ("Kiểm tra", [P("$d_2=\\dfrac{d_1}{2}$ ✓"), P("Đơn vị: m/s ÷ Hz = m ✓")])],
  ["a) Sóng dọc; $\\lambda=0{,}2\\ \\text{m}$", "b) $d_1=0{,}2\\ \\text{m}$; $d_2=0{,}1\\ \\text{m}$", "c) $d_3=1{,}0\\ \\text{m}$", "d) Không thuộc vùng nén lẫn vùng dãn"],
  "Nhận dạng: đề hỏi <strong>khoảng cách các vùng nén, dãn</strong> → tìm $\\lambda=v/f$ trước, rồi đếm số khoảng $\\lambda$ và $\\dfrac{\\lambda}{2}$."),

 sol(["Năng lượng sóng truyền qua mỗi giây tỉ lệ $A^2$ và $f^2$ (cùng một môi trường)",
      "Tỉ số: $\\dfrac{E_n}{E_1}=\\left(\\dfrac{A_n}{A_1}\\right)^2\\left(\\dfrac{f_n}{f_1}\\right)^2$",
      "⚠ Điều kiện: so trong cùng một sợi dây; $v$ không có mặt trong tỉ số"], [
  ("Lần 2: đổi biên độ", [P("$f$ giữ nguyên, chỉ còn tỉ số biên độ:"), M(r"\dfrac{E_2}{E_1}=\left(\dfrac{A_2}{A_1}\right)^2=\left(\dfrac{15}{5{,}0}\right)^2=3^2"), A(r"\dfrac{E_2}{E_1}=9")]),
  ("Lần 3: đổi tần số", [P("$A$ giữ nguyên, chỉ còn tỉ số tần số:"), M(r"\dfrac{E_3}{E_1}=\left(\dfrac{f_3}{f_1}\right)^2=\left(\dfrac{0{,}50}{1{,}0}\right)^2"), A(r"\dfrac{E_3}{E_1}=0{,}25")]),
  ("Lần 4: đổi cả hai", [M(r"\dfrac{A_4}{A_1}=\dfrac{3{,}0}{5{,}0}=0{,}6\qquad\dfrac{f_4}{f_1}=\dfrac{2{,}5}{1{,}0}=2{,}5"), M(r"\dfrac{E_4}{E_1}=0{,}6^2\cdot2{,}5^2=0{,}36\cdot6{,}25"), A(r"\dfrac{E_4}{E_1}=2{,}25")]),
  ("Tìm biên độ để năng lượng gấp 4", [P("$f$ giữ nguyên:"), M(r"\left(\dfrac{A}{A_1}\right)^2=4\Rightarrow\dfrac{A}{A_1}=2"), M(r"A=2\cdot5{,}0"), A(r"A=10\ \text{cm}")]),
  ("Kiểm tra", [P("Lần 2 và 4 lớn hơn 1 vì $A$ hoặc $f$ tăng đủ nhiều; lần 3 nhỏ hơn 1 vì $f$ giảm."), P("$v=2{,}0\\ \\text{m/s}$ không xuất hiện trong kết quả.")])],
  ["a) Gấp $9$ lần", "b) Gấp $0{,}25$ lần", "c) Gấp $2{,}25$ lần", "d) $A=10\\ \\text{cm}$"],
  "Nhận dạng: đề so <strong>năng lượng</strong> ở hai lần vẩy → lập tỉ số $\\left(\\dfrac{A_2}{A_1}\\right)^2\\left(\\dfrac{f_2}{f_1}\\right)^2$."),

 sol(["Cường độ sóng $I=\\dfrac{P}{S}$ (W/m²): công suất truyền qua một đơn vị diện tích vuông góc phương truyền",
      "Nguồn điểm, phát đều: sóng trải trên mặt cầu $S=4\\pi r^2$, nên $I=\\dfrac{P}{4\\pi r^2}$",
      "Năng lượng qua tấm: $E=I\\,S\\,t$",
      "⚠ Điều kiện: nguồn điểm đều mọi hướng, không hấp thụ; tấm vuông góc phương truyền; $t$ đổi ra giây"], [
  ("Công suất của nguồn", [M(r"P=I_1\cdot4\pi r_1^2=0{,}020\cdot4\pi\cdot3{,}0^2"), A(r"P\approx2{,}26\ \text{W}")]),
  ("Cường độ âm tại N", [P("Cùng nguồn, cùng $P$:"), M(r"\dfrac{I_2}{I_1}=\left(\dfrac{r_1}{r_2}\right)^2=\left(\dfrac{3{,}0}{6{,}0}\right)^2=\dfrac{1}{4}"), M(r"I_2=\dfrac{0{,}020}{4}"), A(r"I_2=0{,}0050\ \text{W/m}^2")]),
  ("Năng lượng qua tấm", [P("$10\\ \\text{phút}=600\\ \\text{s}$. Công suất qua tấm là $I_1S$:"), M(r"E=I_1\,S\,t=0{,}020\cdot0{,}50\cdot600"), A(r"E=6{,}0\ \text{J}")]),
  ("Kiểm tra", [P("Kiểm lại $I_2$ từ $P$:"), M(r"\dfrac{P}{4\pi r_2^2}=\dfrac{2{,}26}{4\pi\cdot6{,}0^2}\approx0{,}0050\ \text{W/m}^2\ ✓"), P("Đơn vị: W/m² · m² · s = J ✓")])],
  ["a) $P\\approx2{,}26\\ \\text{W}$", "b) $I_2=0{,}0050\\ \\text{W/m}^2$", "c) $E=6{,}0\\ \\text{J}$"],
  "Nhận dạng: đề cho <strong>cường độ tại một điểm</strong> của nguồn điểm → tìm $P=I\\cdot4\\pi r^2$ rồi suy ra $I$ ở chỗ khác hoặc $E=ISt$."),

 sol(["Sóng P là sóng dọc, sóng S là sóng ngang; sóng ngang không truyền được trong chất lỏng, sóng dọc truyền được",
      "Sóng đi đều: thời gian truyền $t=\\dfrac{d}{v}$",
      "⚠ Điều kiện: hai sóng cùng quãng $d$, cùng gốc thời gian; $\\Delta t$ là hiệu hai thời gian truyền, không phải thời gian của riêng một sóng"], [
  ("Sóng nào không qua lõi lỏng", [P("Sóng S là sóng ngang, cần lực đàn hồi khi lớp này trượt lên lớp kia. Chất lỏng không có lực đó."), P("Sóng P là sóng dọc, chỉ cần nén – dãn."), A("T:Sóng S không truyền qua lõi ngoài lỏng")]),
  ("Khoảng cách từ tâm chấn đến trạm", [P("Lập hiệu thời gian truyền của hai sóng:"), M(r"t_S-t_P=\Delta t\Rightarrow\dfrac{d}{v_S}-\dfrac{d}{v_P}=\Delta t"), M(r"d\left(\dfrac{1}{3{,}5}-\dfrac{1}{6{,}0}\right)=30"), M(r"\dfrac{1}{3{,}5}-\dfrac{1}{6{,}0}=\dfrac{2}{7}-\dfrac{1}{6}=\dfrac{5}{42}"), M(r"d=\dfrac{30\cdot42}{5}"), A(r"d=252\ \text{km}")]),
  ("Thời gian sóng P tới trạm", [M(r"t_P=\dfrac{d}{v_P}=\dfrac{252}{6{,}0}"), A(r"t_P=42\ \text{s}")]),
  ("Kiểm tra", [P("Sóng S tới sau $\\dfrac{252}{3{,}5}=72\\ \\text{s}$."), P("$72-42=30\\ \\text{s}$ đúng bằng $\\Delta t$ ✓")])],
  ["a) Sóng S: sóng ngang không truyền được trong chất lỏng", "b) $d=252\\ \\text{km}$", "c) $t_P=42\\ \\text{s}$"],
  "Nhận dạng: đề cho <strong>hai sóng cùng đường, tới lệch nhau Δt</strong> → lập $\\dfrac{d}{v_S}-\\dfrac{d}{v_P}=\\Delta t$."),
]

# ───────────── tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang="Thấy <b>phương dao động</b> và <b>phương truyền</b> → so hai phương: vuông góc là sóng ngang, trùng là sóng dọc.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Trường hợp (1): dây căng ngang", "Ở (1), phương dao động của phần tử dây so với phương truyền sóng thế nào?",
       lua_chon=[("Vuông góc với phương truyền", True), ("Trùng với phương truyền", "Tay rung lên – xuống còn sóng chạy dọc dây nằm ngang, hai phương không trùng nhau.")],
       loi="Gọi tên theo hướng của dây (\"dây nằm ngang nên sóng ngang\") thay vì so hai phương. Kết quả có thể đúng do trùng hợp, sang dây treo thẳng đứng sẽ sai."),
  buoc("Trường hợp (2): ống khí", "Ở (2), lớp khí dao động theo phương nào so với phương truyền sóng?",
       lua_chon=[("Trùng với phương truyền", True), ("Vuông góc với phương truyền", "Pit-tông đẩy – kéo dọc trục ống nên lớp khí dao động dọc trục, cùng phương với sóng lan.")],
       loi="Thấy ống nằm ngang rồi kết luận \"sóng ngang\". Tên sóng không so với mặt đất mà so phương dao động với phương truyền.",
       ke=[("So phương dao động của lớp khí với phương truyền, như ở (1)", True),
           ("Gọi tên theo vị trí của ống: nằm ngang thì là sóng ngang", "Tên sóng không phụ thuộc ống đặt thế nào so với mặt đất."),
           ("Gọi tên theo vật tạo sóng: pit-tông thì là sóng ngang", "Vật tạo sóng không quyết định tên; phải xét cách phần tử môi trường dao động.")]),
  buoc("Trường hợp (3): mặt hồ", "Ở (3), phao dao động theo phương nào so với phương lan của gợn sóng?",
       lua_chon=[("Vuông góc: phao lên – xuống, gợn sóng lan ngang trên mặt nước", True), ("Trùng: phao bị sóng đẩy trôi theo", "Phao chỉ nhấp nhô tại chỗ, không trôi theo sóng; phương dao động là thẳng đứng.")],
       loi="Cho rằng phao trôi theo sóng nên phương dao động trùng phương truyền.",
       ke=[("So phương dao động của phao với phương lan của gợn sóng", True),
           ("Dùng lại kết quả của (2) vì cũng là chất lỏng – chất khí", "Mỗi trường hợp phải so lại hai phương; môi trường khác nhau thì kết quả có thể khác."),
           ("Chỉ cần xem sóng lan nhanh hay chậm", "Tốc độ lan không quyết định loại sóng.")]),
  buoc("Môi trường khí", "Trong lòng khối khí, truyền được sóng ở (1) hay sóng ở (2)?",
       lua_chon=[("Sóng ở (2)", True), ("Sóng ở (1)", "Sóng ở (1) là sóng ngang, cần lực đàn hồi khi lớp này trượt lên lớp kia; khí không có lực đó.")],
       loi="Cho rằng khí truyền được mọi loại sóng. Phải hỏi môi trường có lực đàn hồi nào.",
       ke=[("Xét lực đàn hồi của khí xuất hiện khi nào", True),
           ("Xét khí nhẹ hơn dây nên truyền chậm hơn", "Nặng nhẹ chỉ ảnh hưởng tốc độ; câu hỏi là truyền được hay không."),
           ("Lấy luôn loại sóng của (1) cho khí", "Loại sóng ở (1) cần lực đàn hồi khác với lực của khí; không thể lấy luôn.")]),
  buoc("Đổi tần số", "Rung đầu A nhanh gấp đôi, sóng ở (1) có đổi thành sóng dọc không?",
       lua_chon=[("Không: phương dao động vẫn vuông góc phương truyền", True), ("Có: rung nhanh hơn thì thành sóng dọc", "Tần số chỉ đổi chu kì và bước sóng; loại sóng do phương dao động so với phương truyền quyết định.")],
       loi="Cho rằng tần số quyết định loại sóng.",
       ke=[("Xét xem hai phương có đổi không khi rung nhanh hơn", True),
           ("Tần số lớn thì sóng dọc, tần số nhỏ thì sóng ngang", "Không có quy tắc như vậy; loại sóng không do tần số quyết định."),
           ("Rung nhanh hơn thì phải đổi môi trường", "Môi trường là sợi dây, không đổi khi chỉ rung nhanh hơn.")])]),

 dict(nhan_dang="Thấy <b>phao nhấp nhô khi sóng tới</b> → $s=vt$ là quãng của sóng; phao ở lại chỗ cũ.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Thời gian sóng tới phao", "Kể từ lúc sỏi rơi, sau bao nhiêu giây phao bắt đầu nhấp nhô?", 7.5, "s", 0.1,
       loi="Nhân $v\\cdot s$ thay vì chia $s/v$, hoặc lấy thời gian theo khoảng cách tới lá."),
  buoc("Thời gian sóng tới lá", "Sau bao nhiêu giây lá bắt đầu nhấp nhô?", 12, "s", 0.1,
       loi="Cộng thêm thời gian của phao, tính trùng đoạn O – phao; $9{,}6$ m đã tính từ O.",
       ke=[("Dùng cùng công thức $t=\\dfrac{s}{v}$ với $s=9{,}6$ m tính từ O", True),
           ("Lấy thời gian của phao cộng $\\dfrac{9{,}6}{0{,}80}$", "9,6 m đã là khoảng cách tính từ O, cộng vào thời gian của phao là tính trùng đoạn O – phao."),
           ("Lấy bằng thời gian của phao vì cùng một gợn sóng", "Cùng một gợn nhưng lá ở xa hơn, gợn phải đi thêm quãng nữa mới tới lá.")]),
  buoc("Quãng sóng đi sau 20 s", "Sau 20 s kể từ lúc sỏi rơi, sóng đã lan tới cách O bao nhiêu mét?", 16, "m", 0.2,
       loi="Trừ thời gian tới phao khỏi 20 s trước khi nhân với $v$, trong khi mốc 20 s đã tính từ lúc sỏi rơi.",
       ke=[("$s=vt$ với $t=20$ s tính từ lúc sỏi rơi", True),
           ("$s=v(20-t_1)$ vì chỉ tính từ lúc sóng tới phao", "Mốc 20 s đã tính từ lúc sỏi rơi; sóng đi từ O ngay lúc đó, không đợi tới phao."),
           ("Sóng dừng ở lá nên $s=9{,}6$ m", "Lá chỉ là một điểm trên đường truyền; sóng vẫn lan tiếp qua lá.")]),
  buoc("Độ dời của phao", "Sau 20 s, phao đã dời xa O thêm bao nhiêu theo phương truyền sóng?",
       lua_chon=[("Gần như bằng 0: phao chỉ nhấp nhô quanh chỗ cũ", True),
                 ("Bằng quãng sóng đã đi, vì phao bị sóng đẩy ra xa", "Phao chỉ nhận năng lượng dao động rồi nhấp nhô tại chỗ; quãng sóng đi và độ dời của phao là hai đại lượng khác nhau."),
                 ("Bằng quãng sóng đi được kể từ lúc tới phao, vì phao theo sóng từ lúc đó", "Sóng đi qua phao rồi tiếp tục lan, phao không theo sóng ở thời điểm nào.")],
       loi="Gán quãng sóng đi cho phao (\"sóng chở phao đi theo\"); đây là bẫy 1 của bài.",
       ke=[("Hỏi phần tử môi trường có đi theo sóng không", True),
           ("Lấy $s=vt$ làm độ dời của phao", "$vt$ là quãng của sóng, không phải quãng của phần tử môi trường."),
           ("Tính độ dời bằng biên độ nhân số lần nhấp nhô", "Biên độ là độ lệch quanh chỗ cân bằng, không cộng dồn thành độ dời.")]),
  buoc("Sóng truyền đi cái gì", "Từ O tới phao, sóng đã truyền đi thứ gì?",
       lua_chon=[("Năng lượng dao động (và trạng thái dao động)", True),
                 ("Nước ở O chảy tới phao", "Nếu nước chảy tới thì phao phải trôi theo; phao chỉ nhấp nhô tại chỗ."),
                 ("Cả nước lẫn năng lượng", "Phần tử môi trường chỉ dao động quanh vị trí cân bằng, không chạy theo sóng.")],
       loi="Nghĩ sóng truyền vật chất của môi trường.",
       ke=[("Dựa vào việc phần tử nước ở lại và vẫn dao động khi sóng tới", True),
           ("Dựa vào việc sóng lan được xa nên phải có nước chảy", "Sóng lan xa không đòi hỏi nước chảy; nước chỉ dao động tại chỗ."),
           ("Dựa vào quãng $s=vt$ bằng quãng nước đi", "$s=vt$ là quãng của sóng, không phải của nước.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang="Thấy <b>khoảng cách các vùng nén, dãn</b> → tìm $\\lambda=v/f$ trước, rồi đếm số khoảng $\\lambda$ và $\\dfrac{\\lambda}{2}$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Loại sóng và bước sóng", "Bước sóng của sóng âm trong ống là bao nhiêu mét?", 0.2, "m", 0.01,
       loi="Dùng $\\lambda=\\dfrac{f}{v}$ (đảo ngược) hoặc $\\lambda=vf$; bước sóng là $\\dfrac{v}{f}$."),
  buoc("Hai vùng nén liên tiếp", "Khoảng cách giữa hai vùng nén liên tiếp là bao nhiêu mét?", 0.2, "m", 0.01,
       loi="Lấy nửa bước sóng cho hai vùng nén liên tiếp.",
       ke=[("Hai vùng nén liên tiếp là hai điểm cùng trạng thái liền nhau: cách nhau một bước sóng", True),
           ("Cách nhau nửa bước sóng", "Nửa bước sóng là khoảng cách giữa một vùng nén và một vùng dãn gần nhất."),
           ("Cách nhau hai bước sóng", "Hai bước sóng là hai vùng nén cách nhau một vùng nén ở giữa.")]),
  buoc("Vùng nén – vùng dãn gần nhất", "Khoảng cách giữa vùng nén và vùng dãn gần nó nhất là bao nhiêu mét?", 0.1, "m", 0.005,
       loi="Lấy bằng một bước sóng hoặc một phần tư bước sóng.",
       ke=[("Nén và dãn gần nhất ngược trạng thái: cách nhau nửa bước sóng", True),
           ("Cách nhau một bước sóng", "Một bước sóng là khoảng cách giữa hai vùng nén liên tiếp."),
           ("Cách nhau một phần tư bước sóng", "Một phần tư bước sóng không ứng với cặp nén – dãn nào trong sóng này.")]),
  buoc("Từ nén thứ nhất đến nén thứ sáu", "Khoảng cách từ vùng nén thứ nhất đến vùng nén thứ sáu là bao nhiêu mét?", 1.0, "m", 0.02,
       loi="Đếm số vùng thay vì số khoảng: nhân 6 thay vì 5.",
       ke=[("Đếm số khoảng giữa hai vùng, rồi nhân với một bước sóng", True),
           ("Nhân bước sóng với số vùng nén", "Từ vùng 1 đến vùng 6 chỉ có 5 khoảng, không phải 6."),
           ("Nhân nửa bước sóng với số vùng nén", "Giữa hai vùng nén liền nhau là một bước sóng, không phải nửa.")]),
  buoc("Điểm M có $u=+A$", "Lớp khí ở M có li độ cực đại theo chiều truyền. M thuộc vùng nào?",
       lua_chon=[("Không thuộc vùng nén lẫn vùng dãn", True),
                 ("Vùng nén, vì lớp khí lệch về phía trước nhiều nhất", "Lệch nhiều nhưng hai lớp ngay hai bên M cũng lệch gần bằng thế nên khoảng cách giữa chúng không đổi; chưa phải nén."),
                 ("Vùng dãn, vì M xa vị trí cân bằng nhất", "Xa vị trí cân bằng không có nghĩa là các lớp thưa ra; dãn cần các lớp xa nhau hơn bình thường.")],
       loi="Gán nén hoặc dãn cho điểm có li độ cực đại (bẫy 2 của bài).",
       ke=[("Xét khoảng cách giữa các lớp khí kề M, không xét độ lệch của riêng M", True),
           ("Xét độ lệch của riêng M: lệch nhiều thì nén", "Độ lệch của một lớp không cho biết nó nén hay dãn; phải so với các lớp bên cạnh."),
           ("Dùng lại $d=\\lambda/2$ của bước trước", "Đó là khoảng cách giữa hai vùng, không trả lời M thuộc vùng nào.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang="Đề so <b>năng lượng</b> ở các lần vẩy khác nhau → lập tỉ số $\\left(\\dfrac{A_2}{A_1}\\right)^2\\left(\\dfrac{f_2}{f_1}\\right)^2$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Lần 2: đổi biên độ", "Biên độ tăng 3 lần, tần số giữ nguyên. Năng lượng gấp bao nhiêu lần?", 9, None, 0.05,
       loi="Lấy 3 lần (quên bình phương biên độ) hoặc $\\sqrt3$ lần (lấy căn thay vì bình phương)."),
  buoc("Lần 3: đổi tần số", "Tần số giảm còn một nửa, biên độ giữ nguyên. Năng lượng gấp bao nhiêu lần?", 0.25, None, 0.005,
       loi="Lấy 0,5 (quên bình phương tần số) hoặc cho là không đổi vì biên độ không đổi.",
       ke=[("Tỉ số tần số rồi bình phương, vì $E\\sim f^2$", True),
           ("Lấy luôn tỉ số tần số, vì $E\\sim f$", "Đề cho $E\\sim f^2$ nên phải bình phương tỉ số tần số."),
           ("Giữ nguyên vì biên độ không đổi", "Năng lượng phụ thuộc cả $A$ và $f$; đổi $f$ thì năng lượng đổi.")]),
  buoc("Lần 4: đổi cả hai", "Biên độ còn 0,6 lần, tần số tăng 2,5 lần. Năng lượng gấp bao nhiêu lần?", 2.25, None, 0.02,
       loi="Cộng hai tỉ số rồi bình phương, hoặc chỉ tính theo tần số vì tần số thay đổi nhiều hơn.",
       ke=[("Nhân hai tỉ số đã bình phương: $(A_4/A_1)^2\\cdot(f_4/f_1)^2$", True),
           ("Cộng hai tỉ số bình phương", "Năng lượng tỉ lệ với tích $A^2f^2$, nên nhân chứ không cộng."),
           ("Chỉ xét tần số vì tần số tăng nhiều hơn", "Biên độ giảm cũng làm năng lượng giảm; phải tính cả hai đại lượng.")]),
  buoc("Biên độ để năng lượng gấp 4", "Giữ nguyên tần số, biên độ phải bằng bao nhiêu centimét để năng lượng gấp 4 lần?", 10, "cm", 0.1,
       loi="Cho $A$ gấp 4 lần (quên rằng năng lượng tỉ lệ $A^2$) nên ra 20 cm.",
       ke=[("Đặt $(A/A_1)^2=4$ rồi suy ra $A$", True),
           ("Lấy $A=4A_1$", "Năng lượng tỉ lệ $A^2$ nên biên độ chỉ cần gấp $\\sqrt4$ lần, không gấp 4 lần."),
           ("Lấy $A=16A_1$", "Bình phương thừa: $A^2$ gấp 4 chứ không phải $A$ gấp $4^2$.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang="Đề cho <b>cường độ tại một điểm</b> của nguồn điểm → tìm $P=I\\cdot4\\pi r^2$, rồi suy ra $I$ ở chỗ khác hoặc $E=ISt$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Công suất của nguồn", "Công suất của nguồn bằng bao nhiêu oát?", 2.26, "W", 0.03,
       loi="Dùng diện tích hình tròn $\\pi r^2$ thay vì mặt cầu $4\\pi r^2$, hoặc quên bình phương $r$."),
  buoc("Cường độ âm tại N", "Cường độ âm tại N bằng bao nhiêu W/m²?", 0.005, "W/m²", 0.0002,
       loi="Cho $I$ tỉ lệ nghịch với $r$ (giảm 2 lần), trong khi diện tích mặt cầu tăng theo $r^2$.",
       ke=[("Xa gấp đôi thì diện tích mặt cầu gấp bốn, nên $I$ giảm 4 lần", True),
           ("Xa gấp đôi thì $I$ giảm 2 lần", "$I$ tỉ lệ nghịch với $r^2$ vì diện tích mặt cầu là $4\\pi r^2$, không phải $r$."),
           ("Cường độ không đổi vì công suất nguồn không đổi", "Công suất không đổi nhưng trải trên diện tích lớn hơn nên cường độ giảm.")]),
  buoc("Năng lượng qua tấm", "Năng lượng sóng truyền qua tấm trong 10 phút bằng bao nhiêu jun?", 6, "J", 0.1,
       loi="Quên đổi 10 phút ra giây, hoặc quên nhân diện tích tấm (cường độ chưa phải năng lượng).",
       ke=[("Công suất qua tấm $=I\\,S$, nhân với thời gian đã đổi ra giây", True),
           ("Lấy $E=I\\cdot t$ vì cường độ đã là năng lượng", "Cường độ là công suất trên mỗi mét vuông; còn phải nhân diện tích tấm."),
           ("Đổi 10 phút thành 10 s rồi nhân", "10 phút là 600 s; số giây phải đúng đơn vị của công suất.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang="Đề cho <b>hai sóng cùng đường, tới lệch nhau Δt</b> → lập $\\dfrac{d}{v_S}-\\dfrac{d}{v_P}=\\Delta t$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Sóng nào không qua lõi lỏng", "Sóng nào trong hai sóng P, S không truyền qua được lõi ngoài ở thể lỏng?",
       lua_chon=[("Sóng S, vì là sóng ngang và chất lỏng không có lực đàn hồi khi các lớp trượt lên nhau", True),
                 ("Sóng P, vì sóng dọc chỉ truyền trong chất rắn", "Sóng dọc truyền được cả trong chất lỏng và khí (nén – dãn); chỉ sóng ngang bị hạn chế."),
                 ("Cả hai sóng đều truyền được vì lõi cũng là vật chất", "Có vật chất chưa đủ; loại lực đàn hồi của môi trường quyết định sóng nào truyền được.")],
       loi="Cho rằng sóng dọc mới bị chặn bởi chất lỏng, hoặc cho rằng mọi sóng cơ đều truyền được qua mọi môi trường vật chất."),
  buoc("Khoảng cách tâm chấn – trạm", "Tâm chấn cách trạm đo bao nhiêu kilômét?", 252, "km", 2,
       loi="Dùng $d=(v_P-v_S)\\Delta t$, hoặc coi $\\Delta t$ là thời gian truyền của một sóng.",
       ke=[("Lập $t_S-t_P=\\Delta t$ với $t=\\dfrac{d}{v}$ của từng sóng", True),
           ("Lấy $d=(v_P-v_S)\\,\\Delta t$", "Hai sóng đi cùng quãng $d$ nhưng mất thời gian khác nhau; hiệu tốc độ nhân $\\Delta t$ không cho quãng đó."),
           ("Lấy $d=v_S\\,\\Delta t$", "$\\Delta t$ là hiệu hai thời gian truyền, không phải thời gian truyền của sóng S.")]),
  buoc("Thời gian sóng P tới trạm", "Kể từ lúc động đất, sóng P tới trạm sau bao nhiêu giây?", 42, "s", 0.5,
       loi="Lấy $t_P=\\Delta t$ vì sóng P tới đầu tiên, hoặc chia khoảng cách cho tốc độ của sóng S.",
       ke=[("Dùng $t_P=\\dfrac{d}{v_P}$ với $d$ vừa tìm", True),
           ("Lấy $t_P=\\Delta t$ vì sóng P tới trước", "$\\Delta t$ là thời gian sóng S tới sau sóng P; sóng P đã đi mất $\\dfrac{d}{v_P}$ từ trước."),
           ("Dùng $t_P=\\dfrac{d}{v_S}$", "Đó là thời gian của sóng S; sóng P nhanh hơn nên tới sớm hơn.")]),
  buoc("Kiểm tra")]),
]

write(J, 28, "Bài 9. Sóng ngang, sóng dọc, sự truyền năng lượng của sóng cơ", DANG, BUILD, ANALYSIS, SOLS)
d_ = json.load(open(J))
for q, f in zip(d_["dang_bai"], FORMS): q["form"] = f
json.dump(d_, open(J, "w"), ensure_ascii=False, indent=1)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
