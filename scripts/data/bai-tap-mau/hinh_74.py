"""Hình cho bài tập mẫu Bài 29 "Định luật bảo toàn động lượng" (Vật lí 10), lesson_id 74.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Quy tắc: vectơ vận tốc đầu V 30°, độ dài = k·v với MỘT hệ số k cho cả hình (vec_luc); không marker.
KHÔNG lộ đáp số: mô phỏng va chạm mềm/ngược chiều dừng ngay lúc chạm (phần sau va chạm là cái cần tính);
chỉ D3 chạy hết vì mọi vận tốc sau va chạm đã cho trong đề. D5 chỉ mô phỏng viên đạn rời nòng (vẽ đúng tỉ lệ vận tốc)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import vec_luc, chevron, field_line

GREY = "#94a3b8"
N = 30                       # số mẫu thời gian (cách đều)


def an(attr, vals, dur, nd=1):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def mover(content, dxs, dur):
    """Nhóm `content` tịnh tiến theo các độ dời dxs (px, cách đều thời gian), chạy một lần khi bấm."""
    vals = ";".join(f"{d:.1f} 0" for d in dxs)
    return (f'<g>{content}<animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/></g>')


def fade_in(content, frac, dur):
    """Hiện dần `content` từ lúc t = frac·dur (frac ∈ (0,1))."""
    a = max(0.0, min(0.98, frac))
    return (f'<g opacity="0">{content}<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{a:.3f};{min(1.0, a + 0.02):.3f};1" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></g>')


def cart(x, gy, w, text, h=34, c="currentColor"):
    """Xe/goòng: thân chữ nhật + 2 bánh; đáy bánh chạm đường ray tại y = gy."""
    return (f'<rect x="{x:.1f}" y="{gy - 8 - h:.1f}" width="{w}" height="{h}" fill="none" stroke="{c}" stroke-width="2.4"/>'
            f'<circle cx="{x + 11:.1f}" cy="{gy - 4:.1f}" r="4" fill="none" stroke="{c}" stroke-width="2"/>'
            f'<circle cx="{x + w - 11:.1f}" cy="{gy - 4:.1f}" r="4" fill="none" stroke="{c}" stroke-width="2"/>'
            + lbl(x + w / 2, gy - 8 - h / 2 + 5, text, c, 12, "middle", "700"))


def rail(gy, x0=14, x1=406):
    return seg(x0, gy, x1, gy, "currentColor", 2.4)


def burst(cx, cy, r=9):
    pts = []
    for i in range(16):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.pi * i / 8
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{ORG}" stroke="{ORG}" stroke-width="1" opacity=".9"/>'


def varrow(x, y, dirn, v, k, c):
    """Vectơ vận tốc nằm ngang bắt đầu tại (x,y); dirn = +1 sang phải, −1 sang trái; độ dài = k·v."""
    s, tip = vec_luc(c, x, y, dirn, 0, v, k)
    return s, tip


# ───────────── Dạng 1: xe 1 (0,30 kg; 0,60 m/s) đẩy xe 2 (0,20 kg) đứng yên; sau va chạm xe 2 chạy 0,45 m/s ─────────────
def d1(kk):
    m1, v1, m2, v2p = 0.30, 0.60, 0.20, 0.45
    S = 200.0                       # px mỗi mét
    gy = 128; w1, w2 = 70, 58
    x1, x2 = 40.0, 250.0
    top = gy - 8 - 34
    k = 60.0                        # px mỗi m/s
    if kk == 0:
        gap = x2 - (x1 + w1)
        t_hit = gap / (S * v1); T = t_hit + 0.5
        ts_ = [T * i / (N - 1) for i in range(N)]
        dxs = [S * v1 * min(t, t_hit) for t in ts_]
        a1, _ = varrow(x1 + 8, top - 14, 1, v1, k, "b")
        c1 = cart(x1, gy, w1, "0,30 kg") + a1 + lbl(x1 + w1, top - 26, "v₁ = 0,60 m/s", BLUE, 12, "end", "700")
        c2 = cart(x2, gy, w2, "0,20 kg") + lbl(x2 + 14, top - 26, "v₂ = 0", GREY, 12, "start", "700")
        fl = burst(x2, top) + lbl(x2, gy + 24, "va chạm", ORG, 12, "middle", "700")
        b = rail(gy) + mover(c1, dxs, T) + c2 + fade_in(fl, t_hit / T, T)
        b += lbl(16, 28, "Cần tìm: vận tốc xe 1 ngay sau va chạm", "currentColor", 13, "start", "700")
        return fig("d1-0", "0 0 420 160", "Xe 1 chạy trên đệm khí tới đẩy xe 2 đang đứng yên", b,
                   "Mô phỏng: xe 1 chạy tới xe 2 đúng thời gian thật (1 m ứng với 200 px), dừng ngay lúc hai xe chạm nhau. Phần sau va chạm là phần cần tính.")
    # tĩnh: hàng Trước / Sau
    g1, g2 = 92, 202
    tp = lambda g: g - 8 - 34
    b = rail(g1) + lbl(16, g1 + 24, "Trước", "currentColor", 13, "start", "700")
    s1, _ = varrow(48, tp(g1) - 14, 1, v1, k, "b")
    b += cart(40, g1, w1, "0,30 kg") + cart(250, g1, w2, "0,20 kg") + s1
    b += lbl(40, tp(g1) - 28, "v₁ = 0,60 m/s", BLUE, 12, "start", "700") + lbl(254, tp(g1) - 28, "v₂ = 0", GREY, 12, "start", "700")
    b += rail(g2) + lbl(16, g2 + 24, "Sau", "currentColor", 13, "start", "700")
    s2, _ = varrow(232, tp(g2) - 14, 1, v2p, k, "o")
    b += cart(100, g2, w1, "0,30 kg") + cart(220, g2, w2, "0,20 kg") + s2
    b += lbl(100, tp(g2) - 28, "v₁′ = ?", RED, 13, "start", "700") + lbl(224, tp(g2) - 28, "v₂′ = 0,45 m/s", ORG, 12, "start", "700")
    b += field_line(300, g2 + 20, 392, g2 + 20, GRN, 1.6, "5 4", 10) + lbl(300, g2 + 40, "chiều dương", GRN, 12, "start", "700")
    return fig("d1-2", "0 0 420 250", "Hai xe trước và sau va chạm; vận tốc xe 1 sau va chạm chưa biết", b,
               "Dữ kiện: chiều dương theo chiều chuyển động của xe 1; mũi tên vận tốc vẽ cùng tỉ lệ (1 m/s ứng với 60 px). Vận tốc xe 1 sau va chạm chưa vẽ.")


# ───────────── Dạng 2: xe A 150 kg (2,0 m/s) va xe B 250 kg, móc dính ─────────────
def d2(kk):
    S = 40.0; gy = 128; wA, wB = 70, 100
    xA, xB = 20.0, 210.0
    top = gy - 8 - 34; k = 25.0; vA = 2.0
    if kk == 0:
        gap = xB - (xA + wA)
        t_hit = gap / (S * vA); T = t_hit + 0.5
        ts_ = [T * i / (N - 1) for i in range(N)]
        dxs = [S * vA * min(t, t_hit) for t in ts_]
        aa, _ = varrow(xA + 8, top - 14, 1, vA, k, "b")
        cA = cart(xA, gy, wA, "150 kg") + aa + lbl(xA + wA, top - 26, "v_A = 2,0 m/s", BLUE, 12, "end", "700")
        cB = cart(xB, gy, wB, "250 kg") + lbl(xB + 14, top - 26, "v_B = 0", GREY, 12, "start", "700")
        fl = burst(xB, top) + lbl(xB, gy + 24, "va chạm, móc dính", ORG, 12, "middle", "700")
        b = rail(gy) + mover(cA, dxs, T) + cB + fade_in(fl, t_hit / T, T)
        b += lbl(16, 28, "Cần tìm: vận tốc hai xe ngay sau va chạm", "currentColor", 13, "start", "700")
        return fig("d2-0", "0 0 420 160", "Xe A chạy tới va vào xe B đứng yên rồi hai xe móc dính", b,
                   "Mô phỏng: xe A chạy tới xe B đúng thời gian thật (1 m ứng với 40 px), dừng ngay lúc chạm. Chuyển động sau va chạm là phần cần tính.")
    g1, g2 = 92, 202
    tp = lambda g: g - 8 - 34
    b = rail(g1) + lbl(16, g1 + 24, "a)", "currentColor", 13, "start", "700")
    s1, _ = varrow(28, tp(g1) - 14, 1, vA, k, "b")
    b += cart(20, g1, wA, "150 kg") + cart(210, g1, wB, "250 kg") + s1
    b += lbl(20, tp(g1) - 28, "v_A = 2,0 m/s", BLUE, 12, "start", "700") + lbl(214, tp(g1) - 28, "v_B = 0", GREY, 12, "start", "700")
    b += rail(g2) + lbl(16, g2 + 24, "b)", "currentColor", 13, "start", "700")
    s1, _ = varrow(28, tp(g2) - 14, 1, vA, k, "b"); s2, _ = varrow(218, tp(g2) - 14, 1, 0.4, k, "o")
    b += cart(20, g2, wA, "150 kg") + cart(210, g2, wB, "250 kg") + s1 + s2
    b += lbl(20, tp(g2) - 28, "v_A = 2,0 m/s", BLUE, 12, "start", "700") + lbl(214, tp(g2) - 28, "v_B = 0,40 m/s", ORG, 12, "start", "700")
    b += field_line(300, g2 + 20, 392, g2 + 20, GRN, 1.6, "5 4", 10) + lbl(300, g2 + 40, "chiều dương", GRN, 12, "start", "700")
    return fig("d2-2", "0 0 420 250", "Hai xe trước va chạm trong hai trường hợp: xe B đứng yên và xe B chạy cùng chiều", b,
               "Dữ kiện: hai trường hợp a) và b), mũi tên vận tốc vẽ cùng tỉ lệ (1 m/s ứng với 25 px). Sau va chạm hai xe dính nhau, vận tốc chung chưa vẽ.")


# ───────────── Dạng 3: xe 1 (0,30 kg; 0,80 m/s) va xe 2 (0,10 kg) đứng yên; sau: 0,40 và 1,2 m/s ─────────────
def d3(kk):
    m1, v1, m2, v1p, v2p = 0.30, 0.80, 0.10, 0.40, 1.2
    S = 120.0; gy = 128; w1, w2 = 62, 46
    x1, x2 = 30.0, 152.0
    k = 40.0
    if kk == 0:
        gap = x2 - (x1 + w1)
        t_hit = gap / (S * v1); t_after = 1.0; T_real = t_hit + t_after
        T = 2 * T_real                               # chạy chậm 2 lần
        ts_ = [T_real * i / (N - 1) for i in range(N)]
        d1_ = [S * (v1 * t if t <= t_hit else v1 * t_hit + v1p * (t - t_hit)) for t in ts_]
        d2_ = [0.0 if t <= t_hit else S * v2p * (t - t_hit) for t in ts_]
        c1 = cart(x1, gy, w1, "0,30 kg"); c2 = cart(x2, gy, w2, "0,10 kg")
        b = rail(gy) + mover(c1, d1_, T) + mover(c2, d2_, T)
        b += lbl(16, 28, "Trước: v₁ = 0,80 m/s · v₂ = 0", BLUE, 13, "start", "700")
        b += fade_in(lbl(16, 50, "Sau: v₁′ = 0,40 m/s · v₂′ = 1,2 m/s", ORG, 13, "start", "700"), t_hit / T_real + 0.05, T)
        return fig("d3-0", "0 0 420 160", "Xe 1 va vào xe 2 đứng yên rồi hai xe tách nhau, cùng chạy theo chiều ban đầu", b,
                   "Mô phỏng: chạy chậm 2 lần so với thật (1 m ứng với 120 px). Các vận tốc sau va chạm đều là số liệu của đề.")
    g1, g2 = 92, 202
    tp = lambda g: g - 8 - 34
    b = rail(g1) + lbl(16, g1 + 24, "Trước", "currentColor", 13, "start", "700")
    s1, _ = varrow(40, tp(g1) - 14, 1, v1, k, "b")
    b += cart(30, g1, w1, "0,30 kg") + cart(190, g1, w2, "0,10 kg") + s1
    b += lbl(30, tp(g1) - 28, "v₁ = 0,80 m/s", BLUE, 12, "start", "700") + lbl(194, tp(g1) - 28, "v₂ = 0", GREY, 12, "start", "700")
    b += rail(g2) + lbl(16, g2 + 24, "Sau", "currentColor", 13, "start", "700")
    s1, _ = varrow(110, tp(g2) - 14, 1, v1p, k, "b"); s2, _ = varrow(236, tp(g2) - 14, 1, v2p, k, "o")
    b += cart(100, g2, w1, "0,30 kg") + cart(226, g2, w2, "0,10 kg") + s1 + s2
    b += lbl(100, tp(g2) - 28, "v₁′ = 0,40 m/s", BLUE, 12, "start", "700") + lbl(226, tp(g2) - 28, "v₂′ = 1,2 m/s", ORG, 12, "start", "700")
    return fig("d3-2", "0 0 420 230", "Hai xe trước và sau va chạm với vận tốc cho trong đề", b,
               "Dữ kiện: mũi tên vận tốc vẽ cùng tỉ lệ (1 m/s ứng với 40 px); hai xe tách nhau sau va chạm, cùng chiều chuyển động ban đầu của xe 1.")


# ───────────── Dạng 4: goòng A 900 kg (2,0 m/s) và goòng B 600 kg (1,0 m/s) ngược chiều, móc dính ─────────────
def d4(kk):
    S = 40.0; gy = 128; wA, wB = 76, 60
    xA, xB = 20.0, 216.0
    top = gy - 8 - 34; k = 25.0; vA, vB = 2.0, 1.0
    if kk == 0:
        gap = xB - (xA + wA)
        t_hit = gap / (S * (vA + vB)); T = t_hit + 0.5
        ts_ = [T * i / (N - 1) for i in range(N)]
        dA = [S * vA * min(t, t_hit) for t in ts_]
        dB = [-S * vB * min(t, t_hit) for t in ts_]
        aA, _ = varrow(xA + 8, top - 14, 1, vA, k, "b")
        aB, _ = varrow(xB + wB - 8, top - 14, -1, vB, k, "o")
        cA = cart(xA, gy, wA, "900 kg") + aA + lbl(xA + wA, top - 26, "v_A = 2,0 m/s", BLUE, 12, "end", "700")
        cB = cart(xB, gy, wB, "600 kg") + aB + lbl(xB, top - 42, "v_B = 1,0 m/s", ORG, 12, "start", "700")
        x_hit = xA + wA + S * vA * t_hit
        fl = burst(x_hit, top) + lbl(x_hit, gy + 24, "va chạm, móc dính", ORG, 12, "middle", "700")
        b = rail(gy) + mover(cA, dA, T) + mover(cB, dB, T) + fade_in(fl, t_hit / T, T)
        b += lbl(16, 28, "Cần tìm: vận tốc hai goòng ngay sau va chạm", "currentColor", 13, "start", "700")
        return fig("d4-0", "0 0 420 160", "Hai goòng chạy ngược chiều tới đâm vào nhau", b,
                   "Mô phỏng: hai goòng chạy tới nhau đúng thời gian thật (1 m ứng với 40 px), dừng ngay lúc chạm. Chuyển động sau va chạm là phần cần tính.")
    g1, g2 = 92, 202
    tp = lambda g: g - 8 - 34
    b = rail(g1) + lbl(16, g1 + 24, "a)", "currentColor", 13, "start", "700")
    s1, _ = varrow(28, tp(g1) - 14, 1, vA, k, "b"); s2, _ = varrow(268, tp(g1) - 14, -1, vB, k, "o")
    b += cart(20, g1, wA, "900 kg") + cart(216, g1, wB, "600 kg") + s1 + s2
    b += lbl(20, tp(g1) - 28, "v_A = 2,0 m/s", BLUE, 12, "start", "700") + lbl(276, tp(g1) - 28, "v_B = 1,0 m/s", ORG, 12, "end", "700")
    b += rail(g2) + lbl(16, g2 + 24, "b)", "currentColor", 13, "start", "700")
    s1, _ = varrow(28, tp(g2) - 14, 1, vA, k, "b")
    b += cart(20, g2, wA, "900 kg") + cart(216, g2, wB, "600 kg") + s1
    b += lbl(20, tp(g2) - 28, "v_A = 2,0 m/s", BLUE, 12, "start", "700") + lbl(276, tp(g2) - 28, "v_B = ?", RED, 13, "end", "700")
    return fig("d4-2", "0 0 420 230", "Hai goòng chạy ngược chiều trước va chạm trong hai trường hợp a) và b)", b,
               "Dữ kiện: hai trường hợp, mũi tên vận tốc vẽ cùng tỉ lệ (1 m/s ứng với 25 px). Chiều dương chọn theo chiều chuyển động của goòng A; ở b) tốc độ goòng B chưa biết nên chưa vẽ.")


# ───────────── Dạng 5: súng bắn đạn (hệ đứng yên) + tên lửa mô hình phụt khí ─────────────
def d5(kk):
    if kk == 0:
        # viên đạn 400 m/s; súng 2,5 kg giật lùi theo định luật bảo toàn — quãng giật = (m/M)·quãng bay của đạn (vẽ thật)
        M, m, v = 2.5, 0.010, 400.0
        gy = 120
        gx, gw = 40.0, 78.0
        tube_y = gy - 44
        fly = 190.0                                         # px đạn bay được
        ts_ = [i / (N - 1) for i in range(N)]
        bullet = [fly * t for t in ts_]
        recoil = [-(m / M) * fly * t for t in ts_]
        T = 2.5
        gun = (f'<rect x="{gx}" y="{gy - 40}" width="{gw}" height="22" fill="none" stroke="currentColor" stroke-width="2.4"/>'
               f'<rect x="{gx + gw}" y="{tube_y + 6}" width="46" height="8" fill="none" stroke="currentColor" stroke-width="2.2"/>'
               f'<path d="M{gx + 14},{gy - 18} L{gx + 8},{gy - 2} L{gx + 28},{gy - 2} L{gx + 30},{gy - 18}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
               + lbl(gx + gw / 2, gy - 25, "2,5 kg", "currentColor", 12, "middle", "700"))
        bl = f'<circle cx="{gx + gw + 46 + 4}" cy="{tube_y + 10}" r="4.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{an("cx", [gx + gw + 50 + d for d in bullet], T)}</circle>'
        label = lbl(16, 28, "Cần tìm: tốc độ giật lùi của súng", "currentColor", 13, "start", "700")
        label2 = lbl(gx + gw + 56, tube_y - 8, "viên đạn 10 g, 400 m/s", GRN, 12, "start", "700")
        b = rail(gy, 14, 406) + mover(gun, recoil, T) + bl + label + label2
        return fig("d5-0", "0 0 420 160", "Súng đặt tự do trên mặt phẳng nhẵn bắn viên đạn theo phương ngang", b,
                   "Mô phỏng: viên đạn rời nòng, chuyển động của súng vẽ đúng tỉ lệ vận tốc (chạy chậm hàng nghìn lần). Phần cần tính là tốc độ giật của súng.")
    k1 = 0.15                                               # px mỗi m/s (đạn 400 m/s)
    k2 = 2.0                                                # px mỗi m/s (khí 30 m/s)
    gy1, gy2 = 100, 228
    b = rail(gy1) + lbl(16, 22, "a) Súng", "currentColor", 13, "start", "700")
    b += (f'<rect x="150" y="{gy1 - 40}" width="78" height="22" fill="none" stroke="currentColor" stroke-width="2.4"/>'
          f'<rect x="228" y="{gy1 - 34}" width="46" height="8" fill="none" stroke="currentColor" stroke-width="2.2"/>'
          + lbl(189, gy1 - 25, "2,5 kg", "currentColor", 12, "middle", "700"))
    s, _ = varrow(282, gy1 - 30, 1, 400.0, k1, "o"); b += s + lbl(282, gy1 - 44, "đạn 10 g · 400 m/s", ORG, 12, "start", "700")
    b += lbl(100, gy1 - 25, "V = ?", RED, 13, "middle", "700") + lbl(16, gy1 + 24, "ban đầu đứng yên", GREY, 12, "start", "600")
    b += rail(gy2) + lbl(16, 152, "b) Tên lửa mô hình", "currentColor", 13, "start", "700")
    b += (f'<rect x="170" y="{gy2 - 36}" width="90" height="22" rx="8" fill="none" stroke="currentColor" stroke-width="2.4"/>'
          + lbl(215, gy2 - 21, "0,60 kg", "currentColor", 12, "middle", "700"))
    s, _ = varrow(166, gy2 - 25, -1, 30.0, k2, "o"); b += s + lbl(166, gy2 - 44, "khí 0,10 kg · 30 m/s", ORG, 12, "end", "700")
    b += lbl(290, gy2 - 21, "V = ?", RED, 13, "start", "700") + lbl(16, gy2 + 24, "ban đầu đứng yên; khối lượng 0,60 kg gồm cả khí phụt ra", GREY, 12, "start", "600")
    return fig("d5-2", "0 0 420 258", "Hệ đứng yên: súng bắn đạn và tên lửa phụt khí", b,
               "Dữ kiện: vận tốc vẽ theo tỉ lệ riêng của từng tình huống (đạn 1 m/s ứng với 0,15 px, khí 1 m/s ứng với 2 px). Vận tốc của súng và của tên lửa chưa vẽ.")


BUILD = [d1, d2, d3, d4, d5]
