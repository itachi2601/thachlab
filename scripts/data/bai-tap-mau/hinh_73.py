"""Hình cho bài tập mẫu Bài 28 "Động lượng" (Vật lí 10), lesson_id 73.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Quy tắc vectơ (thầy chốt 10/10/2026): đầu mũi tên chữ V 30°, độ dài = k·(độ lớn) với MỘT hệ số k cho cả hình (vec_luc), không marker.
Chỉ vẽ vận tốc/lực mà đề cho; KHÔNG vẽ động lượng, độ biến thiên động lượng hay hợp lực (đáp án).
Mô phỏng: D1 hai xe ngược chiều (đúng thời gian thật); D2 đạn trong nòng (chậm 2000 lần, x ~ t²); D3 ba cặp xe trên sàn;
D4 bóng đập vách rồi bật ngược (chậm 5 lần); D5 hai lần bắt bóng (chậm 40 lần, quãng dừng tính thật từ s = v·Δt/2)."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import vec_luc, chevron, field_line

GREY = "#94a3b8"


def rad(a):
    return math.radians(a)


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: base_sb tail."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


def a_tr(vals, dur, kt=None, extra=""):
    k = f' keyTimes="{kt}"' if kt else ""
    return (f'<animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s"{k}{extra} '
            f'begin="indefinite" fill="freeze"/>')


def a_op(vals, dur, kt):
    return (f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def hatch_v(x, y0, y1, n=8, side=1):
    """Vách thẳng đứng, vạch gạch chéo về phía side (+1 sang phải)."""
    out = seg(x, y0, x, y1, "currentColor", 2.6)
    for i in range(n + 1):
        py = y0 + (y1 - y0) * i / n
        out += seg(x, py, x + 8 * side, py + 8, "currentColor", 1.2, "", .7)
    return out


# ───────────── Dạng 1: xe tải 1,5 tấn 54 km/h →, ô tô 750 kg 72 km/h ← ─────────────
def veh_shape(kind, d):
    """Hình xe, gốc ở giữa đáy xe, hướng d = +1 (phải) / −1 (trái)."""
    if kind == "tai":
        s = ('<rect x="-30" y="-26" width="40" height="22" fill="none" stroke="currentColor" stroke-width="2.2"/>'
             '<path d="M10,-4 V-18 H24 L30,-10 V-4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'
             '<circle cx="-18" cy="-3" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/>'
             '<circle cx="20" cy="-3" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/>')
    else:
        s = ('<path d="M-20,-4 V-12 H-11 L-5,-20 H8 L14,-12 H20 V-4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'
             '<circle cx="-11" cy="-3" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/>'
             '<circle cx="11" cy="-3" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/>')
    return f'<g transform="scale({d},1)">{s}</g>'


def d1(kk):
    y1, y2 = 84, 154            # đáy xe tải (→) và đáy ô tô (←)
    kv = 3.0                    # px cho 1 m/s, dùng chung cho cả hai mũi tên vận tốc
    sc = 2.5                    # px cho 1 m (hình minh hoạ, 4 s thật)
    T = 4.0
    x1, x2 = 60.0, 350.0
    b = seg(14, y1 + 8, 406, y1 + 8, "currentColor", 1.6, "", .6) + seg(14, y2 + 8, 406, y2 + 8, "currentColor", 1.6, "", .6)
    b += field_line(24, 22, 104, 22, GRN, 1.8, "5 4", 10) + lbl(112, 27, "chiều dương", GRN, 13, "start", "700")

    def one(kind, d, x, y, col, v_ms, lab, vlab, dx):
        sv, _ = vec_luc("b" if col == BLUE else "o", d * (31 if kind == "tai" else 21), -14, d, 0, v_ms, kv)
        g = (veh_shape(kind, d) + sv + lbl(d * (31 if kind == "tai" else 21) + d * kv * v_ms / 2, -26, vlab, col, 12, "middle", "700")
             + lbl(0, -36, lab, "currentColor", 12, "middle", "600"))
        anim = a_tr(f"0 0;{dx:.1f} 0", T) if kk == 0 else ""
        return f'<g transform="translate({x:.1f},{y})"><g>{g}{anim}</g></g>'

    b += one("tai", 1, x1, y1, BLUE, 15, "xe tải · 1,5 tấn", "54 km/h", sc * 15 * T)
    b += one("oto", -1, x2, y2, ORG, 20, "ô tô con · 750 kg", "72 km/h", -sc * 20 * T)
    if kk == 0:
        return fig("d1-0", "0 0 420 180", "Xe tải 1,5 tấn chạy 54 km/h sang phải và ô tô con 750 kg chạy 72 km/h sang trái trên hai làn đường thẳng", b,
                   "Mô phỏng: hai xe chạy thẳng đều đúng thời gian thật (4 s). Mũi tên vận tốc vẽ cùng tỉ lệ (1 m/s ứng với 3 px). Chiều dương là chiều chuyển động của xe tải. Không vẽ động lượng.")
    return fig("d1-2", "0 0 420 180", "Hai xe chạy ngược chiều trên hai làn; chiều dương là chiều xe tải", b,
               "Dữ kiện: chiều dương là chiều xe tải (sang phải). Mũi tên vận tốc cùng tỉ lệ (1 m/s ứng với 3 px). Chưa vẽ động lượng.")


# ───────────── Dạng 2: đạn 10 g, F = 9000 N, Δt = 1,0 ms trong nòng ─────────────
def d2(kk):
    Fk = 0.006                  # px cho 1 N
    F = 9000.0
    x_back0, L_px = 100.0, 270.0
    yc = 86
    b = (f'<rect x="40" y="{yc - 28}" width="332" height="8" fill="none" stroke="currentColor" stroke-width="2.2"/>'
         f'<rect x="40" y="{yc + 20}" width="332" height="8" fill="none" stroke="currentColor" stroke-width="2.2"/>'
         + seg(40, yc - 28, 40, yc + 28, "currentColor", 3))

    def bullet():
        return ('<path d="M0,-6 H10 L18,0 L10,6 H0 Z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>')

    n = 20
    dur = 2.0
    sv = arrow("", "o", -Fk * F, 0, 0, 0, 3)           # từ lưng đạn lùi ra sau: đuôi ở −54, ngọn ở 0; độ dài = Fk·F
    grp = bullet() + sv + lbl(-Fk * F, 52, "F = 9000 N", ORG, 13, "start", "700")
    vals = ";".join(f"{L_px * (i / n) ** 2:.1f} 0" for i in range(n + 1))
    anim = a_tr(vals, dur) if kk == 0 else ""
    b += f'<g transform="translate({x_back0},{yc})"><g>{grp}{anim}</g></g>'
    b += lbl(40, 20, "Đạn 10 g, đứng yên trước khi bắn", "currentColor", 13, "start", "600")
    b += lbl(40, 40, "Lực đẩy của khí thuốc súng tác dụng trong 1,0 ms", "currentColor", 13, "start", "600")
    if kk == 0:
        return fig("d2-0", "0 0 420 160", "Viên đạn 10 g chạy trong nòng súng nằm ngang dưới lực đẩy trung bình 9000 N trong 1,0 ms", b,
                   "Mô phỏng chậm 2000 lần: 1,0 ms thật ứng với 2 s trên hình. Đạn đi trong nòng dưới lực không đổi, nên đường đi tăng theo bình phương thời gian. Không vẽ tốc độ.")
    return fig("d2-2", "0 0 420 160", "Đạn đứng yên trong nòng, lực đẩy 9000 N hướng theo trục nòng", b,
               "Dữ kiện: đạn bắt đầu từ trạng thái đứng yên; lực đẩy trung bình vẽ theo tỉ lệ 1000 N ứng với 6 px. Thời gian đẩy 1,0 ms.")


# ───────────── Dạng 3: hai xe đẩy m1 = 50 kg (6,0 m/s), m2 = 80 kg (5,0 m/s) ─────────────
def d3(kk):
    kv = 3.0
    v1, v2 = 6.0, 5.0
    sc = 4.0                    # px cho 1 m/s trong 2 s mô phỏng minh hoạ (không theo tỉ lệ độ dài thật)
    stop = 32.0
    if kk == 2:
        O = (130, 150); k = 12.0
        s1, t1 = vec_luc("b", O[0], O[1], 1, 0, v1, k)
        s2, t2 = vec_luc("o", O[0], O[1], math.cos(rad(60)), -math.sin(rad(60)), v2, k)
        b = s1 + s2 + dot(O[0], O[1], 4) + arc(O[0], O[1], 34, 0, 60, RED) + lbl(O[0] + 42, O[1] - 14, "α = 60°", RED, 13, "start", "700")
        b += ts(t1[0] + 8, t1[1] + 5, "v", "1", " = 6,0 m/s", BLUE, 13) + ts(t2[0] + 8, t2[1] + 2, "v", "2", " = 5,0 m/s", ORG, 13)
        b += lbl(20, 28, "Trường hợp c): hai vectơ vận tốc chung gốc", "currentColor", 13, "start", "600")
        b += lbl(20, 50, "xe 1: 50 kg · xe 2: 80 kg · sàn nhẵn", "currentColor", 13, "start", "600")
        return fig("d3-2", "0 0 420 190", "Hai vectơ vận tốc của hai xe chung gốc O hợp nhau góc 60 độ", b,
                   "Dữ kiện: v₁ và v₂ chung gốc, vẽ cùng tỉ lệ (1 m/s ứng với 12 px). Ý a) và b) có α = 180° và α = 90°. Chưa vẽ động lượng.")
    panels = [(5.0, "a) ngược chiều", (1, 0), (-1, 0)), (143.0, "b) vuông góc", (1, 0), (0, -1)), (281.0, "c) hợp 60°", (1, 0), (0.5, -math.sqrt(3) / 2))]
    b = ""
    for x0, tit, u1, u2 in panels:
        O = (x0 + 72.0, 100.0)
        b += f'<rect x="{x0}" y="30" width="134" height="150" rx="6" fill="none" stroke="{GREY}" stroke-width="1.3"/>' + lbl(x0 + 6, 22, tit, "currentColor", 12, "start", "700")
        for u, v, col, c in ((u1, v1, "b", BLUE), (u2, v2, "o", ORG)):
            D = stop + v * sc
            sx, sy = O[0] - u[0] * D, O[1] - u[1] * D
            sv, _ = vec_luc(col, u[0] * 12, u[1] * 12, u[0], u[1], v, kv, 2.6, "", 8)
            body = (f'<rect x="-10" y="-6" width="20" height="12" fill="none" stroke="{c}" stroke-width="2.4"/>' + sv)
            anim = a_tr(f"0 0;{u[0] * v * sc * 2 / 2:.1f} {u[1] * v * sc:.1f}", 2.0) if kk == 0 else ""
            b += f'<g transform="translate({sx:.1f},{sy:.1f})"><g>{body}{anim}</g></g>'
    b += lbl(8, 202, "xe 1 (xanh): 50 kg, 6,0 m/s", BLUE, 13, "start", "700") + lbl(8, 220, "xe 2 (cam): 80 kg, 5,0 m/s", ORG, 13, "start", "700")
    return fig("d3-0", "0 0 420 232", "Ba cặp xe đẩy chạy về cùng một điểm theo ba cách: ngược chiều, vuông góc, hợp nhau 60 độ", b,
               "Mô phỏng minh hoạ (2 s): quãng đường mỗi xe vẽ tỉ lệ với tốc độ (6,0 : 5,0), độ dài tuyệt đối không theo tỉ lệ thật. Mũi tên vận tốc cùng tỉ lệ (1 m/s ứng với 4 px). Không vẽ động lượng.")


# ───────────── Dạng 4: bóng 0,10 kg đập vách cứng, 4,0 m/s tới, bật ngược lại ─────────────
def d4(kk):
    xw, yb, r = 380.0, 100.0, 12.0
    kv = 10.0
    xa, xc = 60.0, xw - r
    b = hatch_v(xw, 30, 114, 10) + ground(yb + r, 16, xw) + lbl(xw - 8, 140, "vách cứng", "currentColor", 12, "end", "600")
    b += lbl(30, 30, "Bóng 0,10 kg trên sàn nhẵn", "currentColor", 13, "start", "600")
    b += lbl(30, 50, "Tốc độ tới vách: 4,0 m/s", "currentColor", 13, "start", "600")
    if kk == 0:
        sR, _ = vec_luc("b", r + 3, 0, 1, 0, 4.0, kv)
        sL, _ = vec_luc("o", -(r + 3), 0, -1, 0, 4.0, kv)
        dur = 2.0
        ball = f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
        g = (ball + f'<g opacity="1">{sR}{a_op("1;0;0", dur, "0;0.5;1")}</g>' + f'<g opacity="0">{sL}{a_op("0;1;1", dur, "0;0.5;1")}</g>')
        b += f'<g transform="translate({xa},{yb})"><g>{g}{a_tr(f"0 0;{xc - xa:.1f} 0;0 0", dur)}</g></g>'
        b += field_line(30, 160, 110, 160, GRN, 1.8, "5 4", 10) + lbl(118, 165, "chiều dương (ý a): chiều tới vách", GRN, 12, "start", "700")
        return fig("d4-0", "0 0 420 180", "Quả bóng 0,10 kg lăn tới vách cứng với tốc độ 4,0 m/s rồi bật ngược lại cùng tốc độ", b,
                   "Mô phỏng chậm 5 lần (ý a): bóng tới vách rồi bật ngược lại cùng tốc độ. Mũi tên vận tốc cùng tỉ lệ (1 m/s ứng với 10 px). Chưa vẽ độ biến thiên động lượng.")
    sR, _ = vec_luc("b", 190 + r + 3, yb, 1, 0, 4.0, kv)
    sL, _ = vec_luc("o", 120 - r - 3, yb + 0, -1, 0, 4.0, kv)
    b += (f'<circle cx="190" cy="{yb}" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>' + sR
          + f'<circle cx="120" cy="{yb}" r="{r}" fill="none" stroke="{GREY}" stroke-width="2" stroke-dasharray="4 3"/>' + sL)
    b += lbl(190, yb - 24, "trước", "currentColor", 12, "middle", "600") + lbl(120, yb - 24, "sau", GREY, 12, "middle", "600")
    b += field_line(30, 160, 110, 160, GRN, 1.8, "5 4", 10) + lbl(118, 165, "chiều dương (ý a): chiều tới vách", GRN, 12, "start", "700")
    return fig("d4-2", "0 0 420 180", "Bóng trước và sau va chạm với vách; chiều dương là chiều bóng tới vách", b,
               "Dữ kiện: hai vị trí của bóng (trước: nét liền, sau: nét đứt); mũi tên vận tốc cùng tỉ lệ (1 m/s ứng với 10 px). Chưa vẽ độ biến thiên động lượng.")


# ───────────── Dạng 5: thủ môn bắt bóng 0,40 kg, 20 m/s; Δt = 0,010 s và 0,050 s ─────────────
def d5(kk):
    r = 10.0
    scp = 100.0                  # px cho 1 m
    v = 20.0
    approach = 1.0 * scp         # bóng đi 1,0 m trước khi chạm tay
    K = 40.0                     # chậm 40 lần
    ta, tb = 0.010, 0.050
    lanes = [(70.0, ta, "a) tay giữ cứng", "Δt = 0,010 s"), (150.0, tb, "b) tay co lại theo bóng", "Δt = 0,050 s")]
    xs = 50.0
    b = ""
    for y, dt, lab, dlab in lanes:
        s_stop = v * dt / 2 * scp                     # quãng dừng = v·Δt/2 (giảm tốc đều)
        t_app = (approach / scp) / v * K              # 2,0 s
        t_stop = dt * K
        dur = t_app + t_stop
        kt = f"0;{t_app / dur:.4f};1"
        if kk != 0 and y != 70.0:
            continue
        b += lbl(14, y - 36, lab, "currentColor", 12, "start", "700")
        hand_x = xs + approach + r                     # mép trái bàn tay khi chạm
        hand = (f'<rect x="{hand_x:.1f}" y="{y - 20}" width="14" height="40" rx="4" fill="none" stroke="currentColor" stroke-width="2.4"/>'
                + seg(hand_x + 14, y - 8, hand_x + 24, y - 8, "currentColor", 2) + seg(hand_x + 14, y + 8, hand_x + 24, y + 8, "currentColor", 2))
        ball = f'<circle cx="{xs}" cy="{y}" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
        sv = arrow("", "b", -22, -22, 22, -22, 2.6)          # vận tốc: dài 44 px, đặt trên quả bóng
        if kk == 0:
            bg = (f'<g transform="translate({xs},{y})"><g><circle cx="0" cy="0" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
                  f'<g opacity="1">{sv}{a_op("1;0;0", dur, kt)}</g>'
                  f'{a_tr(f"0 0;{approach:.1f} 0;{approach + s_stop:.1f} 0", dur, kt)}</g></g>')
            hg = f'<g><g>{hand}{a_tr(f"0 0;0 0;{s_stop:.1f} 0", dur, kt)}</g></g>'
            b += bg + hg
        else:
            b += f'<g transform="translate({xs},{y})"><circle cx="0" cy="0" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>{sv}</g>' + hand
        b += lbl(280, y + 5, dlab, "currentColor", 13, "start", "700")
    b += lbl(14, 16, "Bóng 0,40 kg bay ngang 20 m/s tới tay thủ môn", "currentColor", 13, "start", "600")
    if kk == 0:
        return fig("d5-0", "0 0 420 200", "Thủ môn bắt quả bóng 0,40 kg bay ngang với tốc độ 20 m/s theo hai cách: tay giữ cứng và tay co lại theo bóng", b,
                   "Mô phỏng chậm 40 lần: bóng bay 1,0 m rồi dừng hẳn trong tay. Quãng dừng của bóng tính từ giảm tốc đều. Mũi tên xanh là vận tốc của bóng khi bay (chưa vẽ lực).")
    b += field_line(30, 118, 110, 118, GRN, 1.8, "5 4", 10) + lbl(118, 123, "chiều dương: chiều bay của bóng", GRN, 12, "start", "700")
    return fig("d5-2", "0 0 420 140", "Bóng bay ngang tới tay thủ môn; chiều dương là chiều bay của bóng", b,
               "Dữ kiện: bóng bay ngang 20 m/s tới tay thủ môn; chiều dương là chiều bay của bóng. Chưa vẽ lực của tay.")


BUILD = [d1, d2, d3, d4, d5]
