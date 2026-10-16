"""Bài tập mẫu CĐ12 "Nhiệt học nâng cao: cân bằng nhiệt và chuyển thể" (lesson 153) — Dạng 4–6 (phần khó).
Module được build-hinh-153.py import. Dàn ý: content/hsg9/cd12-nhiet-hoc/nguon.md mục "Bài tập mẫu" (số liệu dùng nguyên).
Dạng sau dùng lại cách làm dạng trước:
  D4 hiệu suất bếp gas (Q = mcΔt của D1 + Q = Lm của D2, rồi H = Q_{\text{í}}ch/Q_tp, Q_tp = q·m)
  D5 rót qua lại hai bình (phương trình cân bằng nhiệt của D1, viết cho cả hệ và cho từng lần rót)
  D6 cơ năng thành nhiệt năng (Q = H·W, rồi Q = mcΔt + λm của D2).
Xuất DANG, BUILD, ANALYSIS, SOLS, STEPS (3 phần tử mỗi list) và kiem_so()."""
import math, os, re, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *  # noqa: F401,F403  (fig, seg, lbl, dot, poly, chevron, arrow, sol, M, P, A, buoc …)

T_CB = "Nhiệt độ và cân bằng nhiệt"
T_Q = "Tính nhiệt lượng theo nhiệt dung riêng"
T_NN = "Nội năng và hai cách làm biến đổi nội năng"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
WAT = "#38bdf8"

# ═════════════ SỐ LIỆU (mọi đáp số tính ở đây, kiem_so() kiểm lại) ═════════════
CN, CAL, CPB = F(4200), F(880), F(130)          # J/(kg·K): nước, nhôm, chì
LHH = F(23 * 10**5)                             # J/kg nhiệt hoá hơi nước
QG = F(44 * 10**6)                              # J/kg năng suất toả nhiệt gas
LAM_PB, TNC_PB = F(25000), F(327)               # chì
G = F(10)
# D4
VN4 = F(2)                                      # lít
MN4 = VN4 * F(1000) / 1000                      # 2 lít = 2 dm³ = 0,002 m³ → 2 kg
MAL4, T04, TS4, H4 = F(1, 2), F(20), F(100), F(2, 5)
QN4 = MN4 * CN * (TS4 - T04)                    # 672 000 J
QAL4 = MAL4 * CAL * (TS4 - T04)                 # 35 200 J
QICH4 = QN4 + QAL4                              # 707 200 J
QTP4 = QICH4 / H4                               # 1 768 000 J
MG4 = QTP4 / QG * 1000                          # ≈ 40,18 g
QHH4 = F(1, 10) * MN4 * LHH                     # 460 000 J
QTP4B = QHH4 / H4                               # 1 150 000 J
MG4B = QTP4B / QG * 1000                        # ≈ 26,14 g
# D5
M1, T1, M2, T2 = F(2), F(60), F(1), F(20)
T1C = F(56)                                     # nhiệt độ cuối bình 1 (cho)
T2C = (M1 * T1 + M2 * T2 - M1 * T1C) / M2      # 28 °C (cả hệ cách nhiệt)
MR = M2 * (T2C - T2) / (T1 - T2C)               # 0,25 kg
T2L3 = (M2 * T2C + MR * T1C) / (M2 + MR)        # 33,6 °C (lần rót thứ ba)
# D6
H6 = F(100)
DT6A = G * H6 / CN                              # 1/4,2 ≈ 0,238 °C
V6, T06, K6 = F(300), F(27), F(3, 5)
DT6B = K6 * V6**2 / 2 / CPB                     # ≈ 207,7 °C
T6B = T06 + DT6B                                # ≈ 234,7 °C
Q6C = CPB * (TNC_PB - T06) + LAM_PB             # 64 000 J/kg
V6C = math.sqrt(float(2 * Q6C / K6))            # ≈ 461,9 m/s


def rich(s, size=14):
    """Nhãn SVG có chỉ số dưới: 'v_{kk}' → tspan dy (chỉ số Unicode hiện như dấu phẩy ở một số máy)."""
    ms = list(re.finditer(r"_\{([^}]+)\}", s))
    if not ms:
        return s
    out = s[:ms[0].start()]
    for k, m in enumerate(ms):
        out += f'<tspan dy="4" font-size="{max(12, size - 2)}">{m.group(1)}</tspan>'
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        out += f'<tspan dy="-4">{s[m.end():nxt]}</tspan>' if s[m.end():nxt] else '<tspan dy="-4"></tspan>'
    return out

def txt(x, y, s, c="currentColor", size=14, anchor="start", weight="700", extra=""):
    size = max(size, 14)                                   # quy ước cỡ chữ: nhãn ≥ 14, không chữ nào < 12
    t = lbl(x, y, rich(s, size), c, size, anchor, weight)
    return t.replace("<text ", f"<text {extra} ", 1) if extra else t

def show_at(t, dur):
    """Hiện (opacity 0 → 1) đúng lúc t trong mô phỏng dài dur giây — chạy một lần khi bấm."""
    k = max(0.001, min(0.999, t / dur))
    return (f'<animate attributeName="opacity" values="0;1" keyTimes="0;{k:.4f}" calcMode="discrete" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')

def show_between(k0, k1, dur):
    """Hiện trong khoảng [k0, k1] (phân số của dur) rồi ẩn lại."""
    return (f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{k0:.4f};{k1:.4f}" calcMode="discrete" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def anim_kt(attr, vals, kts, dur):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.1f}" for v in vals)}" '
            f'keyTimes="{";".join(f"{k:.4f}" for k in kts)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')

def rect(x, y, w, h, c="currentColor", sw=2, fill="none", op=1, rx=0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" '
            f'stroke="{c}" stroke-width="{sw}"/>')

def timed(t, s, x, y, c="currentColor", size=14, anchor="start", weight="700", k1=None, dur=None):
    """Nhãn hiện từ phân số t (tới k1 nếu có) của mô phỏng dài dur."""
    a = show_between(t, k1, dur) if k1 is not None else show_at(t * dur, dur)
    return txt(x, y, s, c, size, anchor, weight, 'opacity="0"').replace("</text>", a + "</text>", 1)

def beaker(x0, x1, ytop, ybot, c="currentColor"):
    return f'<path d="M{x0},{ytop} L{x0},{ybot} L{x1},{ybot} L{x1},{ytop}" fill="none" stroke="{c}" stroke-width="2.6"/>'

def box(x, y, w, h, lines, c="currentColor", fill="none", op=.12):
    b = rect(x, y, w, h, c, 2, fill, op, 6)
    for k, (s, col) in enumerate(lines):
        b += txt(x + w / 2, y + 22 + 20 * k, s, col, 14, "middle", "600")
    return b

def curve_arrow(x1, y1, cx, cy, x2, y2, c=ORG, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    tx, ty = x2 - cx, y2 - cy
    n = math.hypot(tx, ty)
    return (f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" stroke="{c}" stroke-width="2.2"{d}/>'
            + chevron(x2, y2, tx / n, ty / n, c, 2.2, 10))


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 4 · bếp gas đun nồi nước ─────────────
def d4(kk):
    b = ""
    if kk == 0:
        TT, K1 = 7.0, 0.55
        b += txt(16, 22, "Bếp gas đun nồi nhôm chứa nước", "currentColor", 14)
        b += rect(110, 186, 160, 10, "currentColor", 2.2, "none", 1, 2)                      # bếp
        for fx in (150, 175, 200, 225):
            b += f'<path d="M{fx - 7},184 Q{fx},166 {fx + 7},184 Z" fill="{ORG}" fill-opacity=".55" stroke="{ORG}" stroke-width="1.6"/>'
        b += f'<path d="M104,92 L112,176 L268,176 L276,92" fill="none" stroke="currentColor" stroke-width="2.8"/>'  # nồi
        b += f'<path d="M110,108 L114,172 L266,172 L270,108 Z" fill="{WAT}" fill-opacity=".22" stroke="none"/>'
        for k, (bx, by) in enumerate([(140, 156), (172, 146), (205, 160), (236, 150), (190, 130), (156, 126)]):
            b += (f'<circle cx="{bx}" cy="{by}" r="{4 + k % 2}" fill="none" stroke="{WAT}" stroke-width="1.8" opacity="0">'
                  f'{show_at(K1 * TT + .15 * k, TT)}</circle>')
        for k, sx in enumerate((160, 192, 224)):
            b += (f'<path d="M{sx},84 C{sx - 10},72 {sx + 10},62 {sx},48" fill="none" stroke="{GREY}" stroke-width="2" '
                  f'stroke-dasharray="4 4" opacity="0">{show_at(K1 * TT + .3 + .2 * k, TT)}</path>')
        # nhiệt kế: 20 °C → 100 °C rồi đứng yên
        ytc = lambda T: 168 - 1.1 * T
        b += rect(330, 48, 14, 128, "currentColor", 2, "none", 1, 7)
        b += f'<circle cx="337" cy="182" r="10" fill="{RED}" stroke="currentColor" stroke-width="2"/>'
        y20, y100 = ytc(20), ytc(100)
        b += (f'<rect x="333" y="{y20:.1f}" width="8" height="{180 - y20:.1f}" fill="{RED}">'
              f'{anim_kt("y", [y20, y100, y100], [0, K1, 1], TT)}{anim_kt("height", [180 - y20, 180 - y100, 180 - y100], [0, K1, 1], TT)}</rect>')
        for T in (20, 100):
            b += seg(346, ytc(T), 354, ytc(T), "currentColor", 1.6) + txt(358, ytc(T) + 5, f"{T} °C", "currentColor", 14, "start", "600")
        b += timed(0, "đang nóng lên", 16, 214, ORG, 14, "start", "700", K1, TT)
        b += timed(K1, "sôi: nhiệt độ đứng yên, nước hoá hơi dần", 16, 214, BLUE, 14, "start", "700", None, TT)
        return fig("c12-4-0", "0 0 420 224", "Bếp gas đun nồi nước: nhiệt kế tăng từ 20 °C tới 100 °C rồi đứng yên khi nước sôi",
                   b, "Mô phỏng: chạy nhanh hơn thật rất nhiều lần. Nhiệt kế tăng tới 100 °C rồi đứng yên trong lúc nước sôi và hoá hơi.")
    # hình dữ kiện: dòng năng lượng của bếp (độ rộng dải theo tỉ lệ phần trăm đề cho)
    b += txt(16, 18, "Nhiệt lượng gas toả ra đi về đâu?", "currentColor", 14)
    b += rect(20, 50, 170, 60, ORG, 2, ORG, .22, 4)
    b += txt(105, 76, "gas cháy toả ra", "currentColor", 14, "middle", "600") + txt(105, 96, "Q_{tp} (100 %)", "currentColor", 14, "middle")
    b += (f'<polygon points="190,50 300,50 300,44 326,62 300,80 300,74 190,74" fill="{GRN}" fill-opacity=".3" '
          f'stroke="{GRN}" stroke-width="2"/>')
    b += (f'<polygon points="190,74 240,124 300,124 300,112 330,142 300,172 300,160 240,160 190,110" fill="{GREY}" '
          f'fill-opacity=".25" stroke="{GREY}" stroke-width="2"/>')
    b += txt(196, 38, "có ích: 40 % (nước + nồi)", GRN, 14, "start", "700")
    b += txt(246, 192, "hao phí: 60 %", "currentColor", 14, "start", "600")
    b += txt(16, 140, "nước: 2 lít", "currentColor", 14, "start", "600")
    b += txt(16, 158, "20 °C → 100 °C", "currentColor", 14, "start", "600")
    b += txt(16, 176, "nồi nhôm 0,5 kg", "currentColor", 14, "start", "600")
    b += txt(16, 200, "m_{gas} = ?", RED, 14, "start", "700")
    return fig("c12-4-2", "0 0 420 210", "Sơ đồ dòng nhiệt: gas cháy toả nhiệt lượng toàn phần, 40 % có ích cho nước và nồi, 60 % hao phí",
               b, "Dữ kiện: độ rộng mỗi dải theo phần trăm đề cho; phần có ích gồm cả nước và nồi.")


# ───────────── Dạng 5 · rót qua lại hai bình ─────────────
B1X, B2X, BT, BB = (40, 170), (250, 380), 70, 190

def ladle():
    return (rect(-14, -10, 28, 20, "currentColor", 2.2, "none", 1, 3)
            + seg(14, -10, 32, -34, "currentColor", 2.6))

def d5(kk):
    b = ""
    if kk == 0:
        TT = 9.0
        b += timed(0, "Lần 1: múc m từ bình 1 sang bình 2", 16, 22, ORG, 14, "start", "700", .50, TT)
        b += timed(.50, "Chờ cân bằng nhiệt", 16, 22, "currentColor", 14, "start", "700", .64, TT)
        b += timed(.64, "Lần 2: múc m từ bình 2 về bình 1", 16, 22, BLUE, 14, "start", "700", .97, TT)
        b += timed(.97, "Bình 1 cuối: 56 °C; bình 2 cuối: ?", 16, 22, RED, 14, "start", "700", None, TT)
        # mực nước (không theo tỉ lệ)
        y1a, y1b = 100.0, 114.0
        y2a, y2b = 145.0, 131.0
        b += (f'<rect x="{B1X[0] + 2}" y="{y1a}" width="{B1X[1] - B1X[0] - 4}" height="{BB - y1a}" fill="{ORG}" fill-opacity=".25">'
              f'{anim_kt("y", [y1a, y1a, y1b, y1b, y1a, y1a], [0, .05, .09, .90, .94, 1], TT)}'
              f'{anim_kt("height", [BB - y1a, BB - y1a, BB - y1b, BB - y1b, BB - y1a, BB - y1a], [0, .05, .09, .90, .94, 1], TT)}</rect>')
        b += (f'<rect x="{B2X[0] + 2}" y="{y2a}" width="{B2X[1] - B2X[0] - 4}" height="{BB - y2a}" fill="{BLUE}" fill-opacity=".25">'
              f'{anim_kt("y", [y2a, y2a, y2b, y2b, y2a, y2a], [0, .37, .41, .66, .70, 1], TT)}'
              f'{anim_kt("height", [BB - y2a, BB - y2a, BB - y2b, BB - y2b, BB - y2a, BB - y2a], [0, .37, .41, .66, .70, 1], TT)}</rect>')
        b += beaker(*B1X, BT, BB) + beaker(*B2X, BT, BB)
        # ca múc: đi theo các mốc (phân số thời gian, x, y)
        YL = 66                                          # ca đi ở độ cao này: tay cầm (cao 34) không chạm dòng chữ y = 22
        kp = [(0, 105, YL), (.08, 105, 112), (.16, 105, YL), (.34, 315, YL), (.40, 315, 118), (.46, 315, 118), (.52, 315, YL),
              (.62, 315, YL), (.68, 315, 136), (.74, 315, YL), (.88, 105, YL), (.94, 105, 106), (1, 105, YL)]
        vals = ";".join(f"{x} {y}" for _, x, y in kp)
        kts = ";".join(f"{k:.4f}" for k, _, _ in kp)
        full = (f'<rect x="-12" y="-4" width="24" height="12" fill="{WAT}" fill-opacity=".8" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;0;1;0" keyTimes="0;.08;.42;.68;.94" calcMode="discrete" '
                f'dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></rect>')
        b += (f'<g transform="translate(105 {YL})">{full}{ladle()}<animateTransform attributeName="transform" type="translate" '
              f'values="{vals}" keyTimes="{kts}" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += txt(105, 210, "Bình 1", "currentColor", 14, "middle") + txt(105, 226, "2 kg, 60 °C", "currentColor", 14, "middle", "600")
        b += txt(315, 210, "Bình 2", "currentColor", 14, "middle") + txt(315, 226, "1 kg, 20 °C", "currentColor", 14, "middle", "600")
        return fig("c12-5-0", "0 0 420 236", "Ca múc nước từ bình 1 sang bình 2, chờ cân bằng, rồi múc cùng lượng từ bình 2 về bình 1",
                   b, "Mô phỏng: hai lần múc cùng một lượng m. Mực nước và cỡ ca không theo tỉ lệ; khung cuối chỉ ghi số đề cho.")
    # hình dữ kiện
    b += f'<rect x="{B1X[0] + 2}" y="100" width="{B1X[1] - B1X[0] - 4}" height="{BB - 100}" fill="{ORG}" fill-opacity=".22"/>'
    b += f'<rect x="{B2X[0] + 2}" y="145" width="{B2X[1] - B2X[0] - 4}" height="{BB - 145}" fill="{BLUE}" fill-opacity=".22"/>'
    b += beaker(*B1X, BT, BB) + beaker(*B2X, BT, BB)
    b += curve_arrow(120, 64, 210, 0, 300, 64, ORG) + txt(210, 22, "lần 1: m", ORG, 14, "middle")
    b += curve_arrow(300, 86, 210, 44, 120, 86, BLUE, "6 4") + txt(210, 100, "lần 2: m", BLUE, 14, "middle")
    b += txt(48, 130, "m_{1} = 2 kg", "currentColor", 14, "start", "600") + txt(48, 148, "t_{1} = 60 °C", "currentColor", 14, "start", "600")
    b += txt(258, 166, "m_{2} = 1 kg", "currentColor", 14, "start", "600") + txt(258, 182, "t_{2} = 20 °C", "currentColor", 14, "start", "600")
    b += txt(105, 212, "cuối: t_{1}' = 56 °C", "currentColor", 14, "middle", "700")
    b += txt(315, 212, "cuối: t_{2}' = ?", RED, 14, "middle", "700")
    b += txt(210, 236, "m = ?", RED, 14, "middle")
    return fig("c12-5-2", "0 0 420 246", "Hai bình nước: múc lượng m từ bình 1 sang bình 2, cân bằng, rồi múc lượng m từ bình 2 về bình 1",
               b, "Dữ kiện: bình cách nhiệt, bỏ qua nhiệt dung của bình và ca; hai lần múc cùng lượng m. " + NOTE)


# ───────────── Dạng 6 · cơ năng thành nhiệt năng ─────────────
def d6(kk):
    b = ""
    if kk == 0:
        TT = 6.0
        # thác nước
        b += rect(16, 40, 50, 160, "currentColor", 2.2, GREY, .15)
        b += seg(16, 40, 80, 40, WAT, 3) + rect(20, 196, 130, 12, WAT, 2, WAT, .25)
        b += seg(100, 40, 100, 196, "currentColor", 1.4) + chevron(100, 40, 0, -1, "currentColor", 1.4, 8) + chevron(100, 196, 0, 1, "currentColor", 1.4, 8)
        b += txt(106, 122, "h = 100 m", ORG, 14, "start", "700")
        n = 24
        ys = [44 + 150 * (i / n) ** 2 for i in range(n + 1)]
        kts = [0.55 * i / n for i in range(n + 1)] + [1]
        b += (f'<circle cx="76" cy="44" r="5" fill="{WAT}" stroke="currentColor" stroke-width="1.4">'
              f'{anim_kt("cy", ys + [ys[-1]], kts, TT)}</circle>')
        b += timed(.55, "nóng hơn: Δt = ?", 20, 226, RED, 14, "start", "700", None, TT)
        # viên đạn chì bay vào tường
        b += rect(380, 70, 22, 130, "currentColor", 2.2)
        for yy in range(80, 200, 14):
            b += seg(380, yy + 10, 402, yy, "currentColor", 1.2, "", .7)
        b += txt(196, 100, "v = 300 m/s", "currentColor", 14, "start", "700") + txt(196, 154, "t_{0} = 27 °C", "currentColor", 14, "start", "600")
        bull = lambda c, op: f'<ellipse cx="0" cy="0" rx="10" ry="5" fill="{c}" fill-opacity="{op}" stroke="currentColor" stroke-width="1.6"/>'
        hot = f'<g opacity="0">{bull(ORG, .9)}{show_at(.75 * TT, TT)}</g>'
        b += (f'<g transform="translate(196 124)">{bull(GREY, .6)}{hot}<animateTransform attributeName="transform" type="translate" '
              f'values="196 124;196 124;370 124;370 124" keyTimes="0;.6;.75;1" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += timed(.75, "đạn nóng lên: t = ?", 404, 226, RED, 14, "end", "700", None, TT)
        b += txt(16, 22, "Nước rơi từ đỉnh thác; đạn chì cắm vào tường", "currentColor", 14)
        return fig("c12-6-0", "0 0 420 236", "Giọt nước rơi từ đỉnh thác cao 100 m xuống chân thác; viên đạn chì bay 300 m/s cắm vào tường",
                   b, "Mô phỏng: không theo thời gian thật, không theo tỉ lệ. Khung cuối không ghi kết quả.")
    # hình dữ kiện: hai chuỗi chuyển hoá năng lượng
    b += txt(16, 22, "Năng lượng chuyển từ dạng nào sang dạng nào?", "currentColor", 14)
    b += box(10, 36, 146, 56, [("thế năng của nước", "currentColor"), ("h = 100 m", ORG)], ORG, ORG)
    b += arrow("", "o", 160, 64, 214, 64, 2.2) + txt(187, 54, "100 %", ORG, 14, "middle", "700")
    b += box(218, 36, 196, 56, [("nhiệt làm nóng nước", "currentColor"), ("Δt = ?", RED)], RED, RED, .08)
    b += box(10, 112, 146, 56, [("động năng của đạn", "currentColor"), ("v = 300 m/s", ORG)], ORG, ORG)
    b += arrow("", "o", 160, 130, 214, 130, 2.2) + txt(187, 122, "60 %", ORG, 14, "middle", "700")
    b += box(218, 108, 196, 56, [("làm nóng riêng viên đạn", "currentColor"), ("27 °C → t = ?", RED)], RED, RED, .08)
    b += f'<g opacity=".7">{arrow("", "o", 160, 154, 214, 184, 1.8, "5 4")}</g>' + txt(222, 190, "40 %: tường, âm, …", "currentColor", 14, "start", "600")
    b += txt(10, 216, "chì: c = 130 J/(kg·K); nóng chảy ở 327 °C", "currentColor", 14, "start", "600")
    b += (txt(10, 240, "λ = 2,5·10", "currentColor", 14, "start", "600")
          .replace("</text>", '<tspan dy="-6" font-size="12">4</tspan><tspan dy="6"> J/kg</tspan></text>', 1))
    return fig("c12-6-2", "0 0 420 252", "Sơ đồ: thế năng của nước chuyển hết thành nhiệt; 60 % động năng của đạn làm nóng viên đạn, phần còn lại sang tường và âm",
               b, "Dữ kiện: phần trăm ghi trên mũi tên là phần năng lượng chuyển sang nhiệt của vật đang xét. " + NOTE)


BUILD = [d4, d5, d6]

# ═════════════ ĐỀ ═════════════
DANG = [
dict(label="Dạng 4 · Nâng cao · Hiệu suất bếp nhiên liệu: đun sôi rồi cho nước hoá hơi",
     topic=T_Q,
     problem_html=r"""<p>Một nồi nhôm khối lượng $0{,}5\ \text{kg}$ chứa $2$ lít nước ở 20 °C được đun bằng bếp gas. Hiệu suất của bếp là $40\,\%$: chỉ $40\,\%$ nhiệt lượng do gas cháy toả ra được nồi và nước hấp thụ. Cho nhiệt dung riêng của nước là $4200\ \text{J/(kg·K)}$, của nhôm là $880\ \text{J/(kg·K)}$; khối lượng riêng của nước là $1000\ \text{kg/m}^3$; nước sôi ở 100 °C; nhiệt hoá hơi riêng của nước là $2{,}3\cdot10^6\ \text{J/kg}$; năng suất toả nhiệt của gas là $4{,}4\cdot10^7\ \text{J/kg}$.</p><ol type="a"><li>Tính nhiệt lượng nồi và nước cần nhận để nước bắt đầu sôi.</li><li>Tính khối lượng gas cần đốt để đun nước tới sôi (theo gam).</li><li>Đun tiếp cho tới khi $10\,\%$ lượng nước trong nồi hoá hơi. Coi hiệu suất của bếp vẫn là $40\,\%$. Phải đốt thêm bao nhiêu gam gas?</li></ol>"""),
dict(label="Dạng 5 · Nâng cao · Rót qua lại hai bình: tìm lượng nước đã rót",
     topic=T_CB,
     problem_html=r"""<p>Bình 1 chứa $2\ \text{kg}$ nước ở 60 °C, bình 2 chứa $1\ \text{kg}$ nước ở 20 °C. Dùng một ca múc một lượng nước $m$ từ bình 1 đổ sang bình 2. Khi bình 2 đã cân bằng nhiệt, lại múc đúng lượng $m$ từ bình 2 đổ về bình 1. Khi cân bằng, nhiệt độ của bình 1 là 56 °C. Coi các bình cách nhiệt hoàn toàn với môi trường, bỏ qua nhiệt dung của các bình và của ca múc, bỏ qua sự trao đổi nhiệt khi đang múc.</p><ol type="a"><li>Tính nhiệt độ của bình 2 sau lần múc thứ nhất.</li><li>Tính lượng nước $m$ đã múc mỗi lần.</li><li>Từ trạng thái cuối, múc thêm một lần lượng $m$ từ bình 1 đổ sang bình 2. Tính nhiệt độ của bình 2 khi cân bằng.</li></ol>"""),
dict(label="Dạng 6 · Vận dụng cao · Mở rộng HSG: Cơ năng chuyển thành nhiệt năng",
     topic=T_NN,
     problem_html=r"""<p>Lấy $g=10\ \text{m/s}^2$. Nhiệt dung riêng của nước là $4200\ \text{J/(kg·K)}$, của chì là $130\ \text{J/(kg·K)}$; chì nóng chảy ở 327 °C với nhiệt nóng chảy riêng $2{,}5\cdot10^4\ \text{J/kg}$.</p><ol type="a"><li>Nước chảy từ đỉnh một thác cao $100\ \text{m}$ xuống chân thác. Giả sử toàn bộ thế năng của nước chuyển thành nhiệt làm nóng chính lượng nước đó. Nước ở chân thác nóng hơn ở đỉnh thác bao nhiêu độ?</li><li>Một viên đạn chì đang ở 27 °C bay với tốc độ $300\ \text{m/s}$ thì cắm vào một bức tường và dừng lại. Có $60\,\%$ động năng của viên đạn chuyển thành nhiệt làm nóng riêng viên đạn, phần còn lại truyền cho tường và không khí. Tính nhiệt độ của viên đạn ngay sau va chạm. Viên đạn có bị nóng chảy không?</li><li>Vẫn với viên đạn ở 27 °C và tỉ lệ $60\,\%$ như câu b, viên đạn phải bay với tốc độ tối thiểu bằng bao nhiêu để nó nóng chảy hoàn toàn khi cắm vào tường?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 1 nguyên văn đề ; cột 2 chỉ dữ liệu có trong đề ; cột 3 kiến thức nền + câu hỏi gợi) ═════════════
ANALYSIS = [
 # Dạng 4
 [(r'"Một nồi nhôm khối lượng $0{,}5\ \text{kg}$ chứa $2$ lít nước ở 20 °C"', r"$m_{nh}=0{,}5\ \text{kg}$ ; $V=2$ lít ; $t_0=20$ °C", r"Vật nào nhận nhiệt ? Đổi lít ra kilôgam bằng khối lượng riêng : $m=DV$"),
  (r'"chỉ $40\,\%$ nhiệt lượng do gas cháy toả ra được nồi và nước hấp thụ"', r"$H=40\,\%$", r"⚠ phần có ích gồm những vật nào ? Hiệu suất : $H=\dfrac{Q_{\text{ích}}}{Q_{tp}}$"),
  (r'"nhiệt dung riêng của nước là $4200\ \text{J/(kg·K)}$, của nhôm là $880\ \text{J/(kg·K)}$"', r"$c_n=4200$ ; $c_{nh}=880\ \text{J/(kg·K)}$", r"$Q=mc\Delta t$ cho từng vật"),
  (r'"nhiệt hoá hơi riêng của nước là $2{,}3\cdot10^6\ \text{J/kg}$; năng suất toả nhiệt của gas là $4{,}4\cdot10^7\ \text{J/kg}$"', r"$L=2{,}3\cdot10^6\ \text{J/kg}$ ; $q=4{,}4\cdot10^7\ \text{J/kg}$", r"Hoá hơi : $Q=Lm$ ; đốt nhiên liệu : $Q_{tp}=q\,m_{gas}$"),
  (r'"Tính khối lượng gas cần đốt để đun nước tới sôi (theo gam)"', r"$m_{gas}=?$", r"Nhiệt lượng nào do gas toả ra : $Q_{\text{ích}}$ hay $Q_{tp}$ ?"),
  (r'"Đun tiếp cho tới khi $10\,\%$ lượng nước trong nồi hoá hơi"', r"$m_{\text{hơi}}=10\,\%\,m_n$", r"⚠ trong lúc sôi, nhiệt độ của nước và nồi có tăng nữa không ? Nồi còn cần nhận nhiệt không ?"),
  (r'"Coi hiệu suất của bếp vẫn là $40\,\%$. Phải đốt thêm bao nhiêu gam gas?"', r"$H=40\,\%$ ; $\Delta m_{gas}=?$", r"Đề hỏi lượng gas thêm hay tổng lượng gas ?")],
 # Dạng 5
 [(r'"Bình 1 chứa $2\ \text{kg}$ nước ở 60 °C, bình 2 chứa $1\ \text{kg}$ nước ở 20 °C"', r"$m_1=2\ \text{kg}$, $t_1=60$ °C ; $m_2=1\ \text{kg}$, $t_2=20$ °C", r"Nhiệt lượng : $Q=mc\Delta t$ ; cùng là nước nên $c$ như nhau"),
  (r'"Coi các bình cách nhiệt hoàn toàn với môi trường, bỏ qua nhiệt dung của các bình và của ca múc"', r"không mất nhiệt ra ngoài", r"⚠ điều kiện để viết $Q_{\text{toả}}=Q_{thu}$ cho cả hệ hai bình, qua mọi lần múc"),
  (r'"múc một lượng nước $m$ từ bình 1 đổ sang bình 2"', r"lần 1 : $m$ ở $t_1$ sang bình 2", r"Sau lần 1, bình 2 có bao nhiêu nước, cân bằng ở nhiệt độ nào (ẩn) ?"),
  (r'"lại múc đúng lượng $m$ từ bình 2 đổ về bình 1"', r"lần 2 : $m$ ở nhiệt độ của bình 2", r"⚠ khi múc bớt nước ra, nhiệt độ phần còn lại trong bình 2 có đổi không ?"),
  (r'"Khi cân bằng, nhiệt độ của bình 1 là 56 °C"', r"$t_1'=56$ °C", r"Lúc cuối, mỗi bình có bao nhiêu nước ? So với lúc đầu, nước của bình 1 toả ra bao nhiêu nhiệt ?"),
  (r'"Tính lượng nước $m$ đã múc mỗi lần"', r"$m=?$", r"Viết cân bằng nhiệt cho lần múc nào thì chỉ còn ẩn $m$ ?"),
  (r'"múc thêm một lần lượng $m$ từ bình 1 đổ sang bình 2"', r"$t_2''=?$", r"Lúc đó mỗi bình có bao nhiêu nước, ở nhiệt độ nào ?")],
 # Dạng 6
 [(r'"Giả sử toàn bộ thế năng của nước chuyển thành nhiệt làm nóng chính lượng nước đó"', r"$H=100\,\%$, nhiệt chỉ vào nước", r"⚠ điều kiện : không có nhiệt toả ra không khí, đá. Thế năng : $W_t=mgh$"),
  (r'"Nước chảy từ đỉnh một thác cao $100\ \text{m}$"', r"$h=100\ \text{m}$ ; $g=10\ \text{m/s}^2$", r"Đề không cho khối lượng nước : có cần không ?"),
  (r'"Nước ở chân thác nóng hơn ở đỉnh thác bao nhiêu độ?"', r"$\Delta t_n=?$", r"$Q=mc\Delta t$ ; nối $Q$ với thế năng"),
  (r'"Một viên đạn chì đang ở 27 °C bay với tốc độ $300\ \text{m/s}$"', r"$t_0=27$ °C ; $v=300\ \text{m/s}$", r"Động năng : $W_{\text{đ}}=\dfrac12mv^2$"),
  (r'"Có $60\,\%$ động năng của viên đạn chuyển thành nhiệt làm nóng riêng viên đạn"', r"$H=60\,\%$", r"⚠ chỉ phần $60\,\%$ vào viên đạn ; tường và không khí nhận phần còn lại"),
  (r'"Viên đạn có bị nóng chảy không?"', r"$t_{nc}=327$ °C", r"So sánh đại lượng nào với nhiệt độ nóng chảy ?"),
  (r'"phải bay với tốc độ tối thiểu bằng bao nhiêu để nó nóng chảy hoàn toàn"', r"$\lambda=2{,}5\cdot10^4\ \text{J/kg}$ ; $v_{min}=?$", r"Để chảy hết, chì phải qua những giai đoạn nào ? Mỗi giai đoạn cần nhiệt lượng tính bằng công thức nào ?")],
]

# ═════════════ LỜI GIẢI ═════════════
R4 = [r"<strong>Nhiệt lượng:</strong> làm nóng $Q=mc\Delta t$ ; hoá hơi ở nhiệt độ sôi $Q=Lm$.",
      r"<strong>Nhiên liệu:</strong> đốt $m_{gas}$ toả ra $Q_{tp}=q\,m_{gas}$.",
      r"<strong>Hiệu suất:</strong> $H=\dfrac{Q_{\text{ích}}}{Q_{tp}}$, $Q_{\text{ích}}$ là nhiệt mà nồi và nước nhận.",
      r"<strong>Điều kiện:</strong> trong lúc sôi nhiệt độ không đổi ; $1$ lít nước $=0{,}001\ \text{m}^3$ nặng $1\ \text{kg}$."]
R5 = [r"<strong>Nguyên lí:</strong> nhiệt truyền từ vật nóng sang vật lạnh tới khi bằng nhiệt độ.",
      r"<strong>Phương trình cân bằng nhiệt:</strong> $Q_{\text{toả}}=Q_{thu}$, với $Q=mc\Delta t$.",
      r"<strong>Múc bớt nước:</strong> phần nước còn lại giữ nguyên nhiệt độ.",
      r"<strong>Điều kiện:</strong> bình cách nhiệt, bỏ qua nhiệt dung bình và ca ; mọi nước cùng $c$."]
R6 = [r"<strong>Hai cách làm biến đổi nội năng:</strong> thực hiện công (va chạm, ma sát) và truyền nhiệt.",
      r"<strong>Cơ năng:</strong> $W_t=mgh$ ; $W_{\text{đ}}=\dfrac12mv^2$.",
      r"<strong>Phần thành nhiệt:</strong> $Q=H\cdot W$ ; làm nóng $Q=mc\Delta t$ ; nóng chảy $Q=\lambda m$.",
      r"<strong>Điều kiện:</strong> chì chỉ bắt đầu chảy khi đã tới 327 °C ; nhiệt chỉ vào vật đang xét."]

SOLS = [
 sol(R4, [
  ("Nhiệt lượng có ích tới khi sôi", [P(r"Khối lượng nước : $m_n=DV=1000\cdot0{,}002=2\ \text{kg}$. Cả nồi và nước nóng từ 20 °C tới 100 °C :"),
     M(r"Q_{\text{ích}}=m_nc_n\Delta t+m_{nh}c_{nh}\Delta t"), M(r"Q_{\text{ích}}=2\cdot4200\cdot80+0{,}5\cdot880\cdot80"),
     M(r"Q_{\text{ích}}=672\,000+35\,200"), A(r"Q_{\text{ích}}=707\,200\ \text{J}")]),
  ("Nhiệt lượng gas toả ra", [P(r"Chỉ $40\,\%$ nhiệt của gas là có ích :"), M(r"Q_{tp}=\dfrac{Q_{\text{ích}}}{H}=\dfrac{707\,200}{0{,}4}"), A(r"Q_{tp}=1\,768\,000\ \text{J}")]),
  ("Khối lượng gas", [M(r"m_{gas}=\dfrac{Q_{tp}}{q}=\dfrac{1\,768\,000}{4{,}4\cdot10^7}\approx0{,}0402\ \text{kg}"), A(r"m_{gas}\approx40{,}2\ \text{g}")]),
  ("Nhiệt lượng để $10\,\%$ nước hoá hơi", [P(r"Đang sôi : nồi và nước giữ 100 °C nên không cần nhiệt để làm nóng thêm ; chỉ cần nhiệt hoá hơi :"),
     M(r"Q'=L\cdot0{,}1\,m_n=2{,}3\cdot10^6\cdot0{,}2"), A(r"Q'=460\,000\ \text{J}")]),
  ("Lượng gas đốt thêm", [M(r"\Delta m_{gas}=\dfrac{Q'}{H\,q}=\dfrac{460\,000}{0{,}4\cdot4{,}4\cdot10^7}\approx0{,}0261\ \text{kg}"), A(r"\Delta m_{gas}\approx26{,}1\ \text{g}")]),
  ("Kiểm tra", [P(r"Đơn vị : $\dfrac{\text{J}}{\text{J/kg}}=\text{kg}$ ✓."),
     P(r"Làm $0{,}2\ \text{kg}$ nước hoá hơi tốn $460\,000\ \text{J}$, cỡ $\tfrac23$ nhiệt đun $2\ \text{kg}$ nước từ 20 °C tới sôi : nhiệt hoá hơi riêng rất lớn ✓."),
     P(r"Nồi nhôm chỉ chiếm khoảng $5\,\%$ nhiệt có ích, nhưng bỏ qua thì đáp số lệch ✓ (đề có cho thì phải tính).")])],
  [r"a) $Q_{\text{ích}}=707\,200\ \text{J}$", r"b) $m_{gas}\approx40{,}2\ \text{g}$", r"c) đốt thêm khoảng $26{,}1\ \text{g}$ gas"],
  r"Nhận dạng: thấy <strong>bếp có hiệu suất H</strong> và <strong>năng suất toả nhiệt q</strong> → tính $Q_{\text{ích}}$ cho mọi vật nhận nhiệt, chia $H$ ra $Q_{tp}$, rồi $m=Q_{tp}/q$ ; lúc sôi chỉ còn $Q=Lm$."),
 sol(R5, [
  ("Nhiệt độ bình 2 sau lần múc thứ nhất", [P(r"Lần múc thứ hai chỉ lấy bớt nước nên bình 2 vẫn ở nhiệt độ $t_2'$ sau lần 1. Lúc cuối : bình 1 có $2\ \text{kg}$ ở 56 °C, bình 2 có $1\ \text{kg}$ ở $t_2'$."),
     P(r"Cả hệ cách nhiệt : nhiệt $2\ \text{kg}$ nước của bình 1 toả ra bằng nhiệt $1\ \text{kg}$ nước của bình 2 thu vào :"),
     M(r"m_1c(t_1-t_1')=m_2c(t_2'-t_2)"), M(r"2\cdot(60-56)=1\cdot(t_2'-20)"), A(r"t_2'=28\ ^\circ\text{C}")]),
  ("Lượng nước $m$", [P(r"Lần 1 : lượng $m$ ở 60 °C nguội tới $t_2'$, $1\ \text{kg}$ nước bình 2 nóng từ 20 °C tới $t_2'$ :"),
     M(r"mc(t_1-t_2')=m_2c(t_2'-t_2)"), M(r"m\cdot(60-28)=1\cdot(28-20)\ \Rightarrow\ m=\dfrac{8}{32}"), A(r"m=0{,}25\ \text{kg}")]),
  ("Nhiệt độ bình 2 sau lần múc thứ ba", [P(r"Lúc đó bình 2 có $1\ \text{kg}$ ở 28 °C, nhận thêm $0{,}25\ \text{kg}$ ở 56 °C :"),
     M(r"t_2''=\dfrac{m_2t_2'+m\,t_1'}{m_2+m}=\dfrac{1\cdot28+0{,}25\cdot56}{1{,}25}"), A(r"t_2''=33{,}6\ ^\circ\text{C}")]),
  ("Kiểm tra", [P(r"Lần 2 : bình 1 còn $1{,}75\ \text{kg}$ ở 60 °C, nhận $0{,}25\ \text{kg}$ ở 28 °C :"),
     M(r"\dfrac{1{,}75\cdot60+0{,}25\cdot28}{2}=\dfrac{105+7}{2}=56\ ^\circ\text{C}\ ✓"),
     P(r"$t_2''$ nằm giữa 28 °C và 56 °C, gần 28 °C hơn vì bình 2 nhiều nước hơn ✓.")])],
  [r"a) $t_2'=28$ °C", r"b) $m=0{,}25\ \text{kg}$", r"c) $t_2''=33{,}6$ °C"],
  r"Nhận dạng: thấy <strong>rót qua lại</strong> giữa hai bình cách nhiệt → viết cân bằng nhiệt cho <strong>cả hệ</strong> (đầu và cuối) để ra nhiệt độ, rồi cân bằng cho <strong>một lần rót</strong> để ra $m$."),
 sol(R6, [
  ("Nước nóng thêm ở chân thác", [P(r"Toàn bộ thế năng thành nhiệt của chính lượng nước đó :"), M(r"mgh=mc_n\Delta t_n\ \Rightarrow\ \Delta t_n=\dfrac{gh}{c_n}"),
     M(r"\Delta t_n=\dfrac{10\cdot100}{4200}"), A(r"\Delta t_n\approx0{,}24\ ^\circ\text{C}")]),
  ("Đạn nóng thêm", [P(r"$60\,\%$ động năng làm nóng viên đạn ; $m$ ở hai vế giản ước :"), M(r"0{,}6\cdot\dfrac12mv^2=mc\,\Delta t\ \Rightarrow\ \Delta t=\dfrac{0{,}3\,v^2}{c}"),
     M(r"\Delta t=\dfrac{0{,}3\cdot300^2}{130}"), A(r"\Delta t\approx208\ ^\circ\text{C}")]),
  ("Nhiệt độ đạn sau va chạm", [M(r"t=t_0+\Delta t\approx27+207{,}7"), A(r"t\approx235\ ^\circ\text{C}"),
     A(r"T:$t\lt327$ °C nên viên đạn chưa nóng chảy.")]),
  ("Nhiệt lượng cho mỗi kilôgam chì chảy hết", [P(r"Hai giai đoạn : nóng từ 27 °C tới 327 °C, rồi nóng chảy ở 327 °C :"),
     M(r"\dfrac{Q}{m}=c\,(t_{nc}-t_0)+\lambda=130\cdot300+25\,000"), A(r"\dfrac{Q}{m}=64\,000\ \text{J/kg}")]),
  ("Tốc độ tối thiểu", [M(r"0{,}6\cdot\dfrac12v^2=\dfrac{Q}{m}\ \Rightarrow\ v=\sqrt{\dfrac{2\cdot64\,000}{0{,}6}}"), A(r"v_{min}\approx462\ \text{m/s}")]),
  ("Kiểm tra", [P(r"Câu a không cần khối lượng nước : $m$ giản ước ✓ ; thực tế nước còn toả nhiệt, bay hơi nên nóng thêm ít hơn $0{,}24$ °C."),
     P(r"$v_{min}\gt300\ \text{m/s}$, đúng với câu b (ở $300\ \text{m/s}$ đạn chưa chảy) ✓."),
     P(r"Đơn vị : $\dfrac{(\text{m/s})^2}{\text{J/(kg·K)}}=\text{K}$ vì $1\ \text{J/kg}=1\ (\text{m/s})^2$ ✓.")])],
  [r"a) nước ở chân thác nóng hơn khoảng $0{,}24$ °C", r"b) $t\approx235$ °C, chưa nóng chảy", r"c) $v_{min}\approx462\ \text{m/s}$"],
  r"Nhận dạng: thấy <strong>rơi, va chạm, cắm vào tường</strong> kèm <strong>phần trăm chuyển thành nhiệt</strong> → $H\cdot W_{\text{cơ}}=Q$ ; muốn chảy hết thì $Q$ gồm làm nóng tới $t_{nc}$ cộng $\lambda m$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>hiệu suất bếp</b>, <b>năng suất toả nhiệt</b> → <b>Q có ích chia H, rồi chia q</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Nhiệt lượng có ích tới khi sôi", "Nồi và nước cần nhận bao nhiêu jun để nước bắt đầu sôi?", float(QICH4), "J", 1000,
       loi=r"Chỉ tính nhiệt cho nước, quên nồi nhôm cũng nóng lên ; hoặc lấy $2$ lít là $2000\ \text{kg}$ vì đổi sai thể tích."),
  buoc("Nhiệt lượng gas toả ra", "Gas cháy phải toả ra bao nhiêu jun?", float(QTP4), "J", 5000,
       loi=r"Nhân $Q_{\text{ích}}$ với $H$ : kết quả nhỏ hơn nhiệt có ích là vô lí, vì gas phải toả nhiều hơn phần nồi và nước nhận.",
       ke=[(r"$Q_{tp}=\dfrac{Q_{\text{ích}}}{H}$", True),
           (r"$Q_{tp}=H\cdot Q_{\text{ích}}$", r"Như vậy nhiệt gas toả ra còn ít hơn nhiệt có ích ; phải chia cho $H$ mới đúng định nghĩa $H=Q_{\text{ích}}/Q_{tp}$."),
           (r"$Q_{tp}=Q_{\text{ích}}$", r"Bỏ qua hiệu suất : $60\,\%$ nhiệt của gas bị hao phí nên gas phải toả nhiều hơn nhiệt có ích.")]),
  buoc("Khối lượng gas", "Cần đốt bao nhiêu gam gas?", float(MG4), "g", 0.3,
       loi=r"Chia nhiệt có ích cho $q$ (quên hiệu suất), hoặc để kết quả theo kilôgam mà đề hỏi gam.",
       ke=[(r"$m_{gas}=\dfrac{Q_{tp}}{q}$ rồi đổi ra gam", True),
           (r"$m_{gas}=\dfrac{Q_{\text{ích}}}{q}$", r"Gas toả ra $Q_{tp}$, không phải $Q_{\text{ích}}$ ; chia $Q_{\text{ích}}$ cho $q$ là coi bếp không hao phí."),
           (r"$m_{gas}=\dfrac{H\cdot Q_{\text{ích}}}{q}$", r"Nhân thêm $H$ làm lượng gas còn nhỏ hơn cả khi không hao phí ; hiệu suất phải làm tăng lượng gas.")]),
  buoc("Nhiệt lượng để $10\,\%$ nước hoá hơi", "Để 10 % lượng nước hoá hơi, nồi và nước cần nhận thêm bao nhiêu jun?", float(QHH4), "J", 2000,
       loi=r"Cộng thêm nhiệt làm nóng nồi và nước như đoạn trước, hoặc cho toàn bộ nước hoá hơi.",
       ke=[(r"$Q'=L\cdot0{,}1\,m_n$ vì nồi và nước giữ nhiệt độ sôi", True),
           (r"$Q'=L\cdot0{,}1\,m_n+(m_nc_n+m_{nh}c_{nh})\Delta t$", r"Khi sôi nhiệt độ đứng yên nên nồi và nước không cần nhận nhiệt để nóng thêm."),
           (r"$Q'=L\cdot m_n$", r"Đề chỉ cho $10\,\%$ lượng nước hoá hơi, không phải toàn bộ nước.")]),
  buoc("Lượng gas đốt thêm", "Phải đốt thêm bao nhiêu gam gas?", float(MG4B), "g", 0.3,
       loi=r"Quên chia hiệu suất lần nữa, hoặc trả lời tổng lượng gas từ đầu thay vì lượng đốt thêm.",
       ke=[(r"$\Delta m_{gas}=\dfrac{Q'}{H\,q}$", True),
           (r"$\Delta m_{gas}=\dfrac{Q'}{q}$", r"Hiệu suất vẫn là $40\,\%$ khi đun tiếp ; gas phải toả $Q'/H$."),
           (r"$\Delta m_{gas}=\dfrac{Q_{\text{ích}}+Q'}{H\,q}$", r"Đó là tổng lượng gas từ đầu ; đề hỏi lượng đốt thêm.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>rót qua lại</b> hai bình → <b>cân bằng cả hệ</b>, rồi <b>cân bằng một lần rót</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Nhiệt độ bình 2 sau lần múc thứ nhất", "Sau lần múc thứ nhất, bình 2 cân bằng ở bao nhiêu độ C?", float(T2C), "°C", 0.2,
       loi=r"Lấy trung bình cộng nhiệt độ, hoặc nghĩ bình 2 đổi nhiệt độ khi múc bớt nước ra ; cũng hay quên lúc cuối bình 1 lại có đủ $2\ \text{kg}$."),
  buoc("Lượng nước $m$", "Mỗi lần múc bao nhiêu kilôgam nước?", float(MR), "kg", 0.01,
       loi=r"Cho lượng $m$ nguội tới nhiệt độ cuối của bình 1, hoặc lấy bên thu nhiệt là cả nước bình 2 lẫn $m$.",
       ke=[(r"Cân bằng lần 1 : $m\,c\,(t_1-t_2')=m_2c\,(t_2'-t_2)$", True),
           (r"$m\,c\,(t_1-t_2')=(m_2+m)\,c\,(t_2'-t_2)$", r"Lượng $m$ là bên toả nhiệt ; bên thu chỉ là $1\ \text{kg}$ nước ban đầu của bình 2."),
           (r"$m\,c\,(t_1-t_1')=m_2c\,(t_2'-t_2)$", r"Ở lần 1, lượng $m$ nguội tới $t_2'$ của bình 2, không phải tới nhiệt độ cuối của bình 1.")]),
  buoc("Nhiệt độ bình 2 sau lần múc thứ ba", "Sau lần múc thứ ba, bình 2 cân bằng ở bao nhiêu độ C?", float(T2L3), "°C", 0.1,
       loi=r"Quên bình 2 đã múc về một lượng $m$ nên chỉ còn $1\ \text{kg}$, hoặc lấy nước múc sang ở 60 °C như lúc đầu.",
       ke=[(r"Trộn $1\ \text{kg}$ ở $t_2'$ với $m$ ở $t_1'$", True),
           (r"Trộn $(m_2+m)$ ở $t_2'$ với $m$ ở $t_1'$", r"Lần 2 đã múc $m$ từ bình 2 về bình 1, nên bình 2 chỉ còn $1\ \text{kg}$."),
           (r"Trộn $1\ \text{kg}$ ở $t_2'$ với $m$ ở 60 °C", r"Bình 1 đã nguội còn 56 °C ; nước múc sang lần này ở nhiệt độ đó.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>rơi, va chạm</b> và <b>phần trăm thành nhiệt</b> → <b>H·W = Q</b>, chảy hết thì cộng <b>λm</b>",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Nước nóng thêm ở chân thác", "Nước ở chân thác nóng hơn ở đỉnh bao nhiêu độ?", float(DT6A), "°C", 0.01,
       loi=r"Cho rằng thiếu khối lượng nên không giải được ; thật ra $m$ có ở cả thế năng lẫn nhiệt lượng nên giản ước."),
  buoc("Đạn nóng thêm", "Viên đạn nóng thêm bao nhiêu độ?", float(DT6B), "°C", 1,
       loi=r"Dùng cả động năng làm nóng đạn (bỏ $60\,\%$), hoặc viết động năng là $mv^2$ (quên $\tfrac12$).",
       ke=[(r"$0{,}6\cdot\dfrac12mv^2=mc\,\Delta t$", True),
           (r"$\dfrac12mv^2=mc\,\Delta t$", r"Chỉ $60\,\%$ động năng vào viên đạn ; phần còn lại sang tường và không khí."),
           (r"$0{,}6\cdot mv^2=mc\,\Delta t$", r"Động năng là $\dfrac12mv^2$ ; thiếu $\dfrac12$ làm độ tăng nhiệt độ gấp đôi.")]),
  buoc("Nhiệt độ đạn sau va chạm", "Ngay sau va chạm, viên đạn có nhiệt độ bao nhiêu độ C?", float(T6B), "°C", 1,
       loi=r"Lấy độ tăng nhiệt độ làm nhiệt độ cuối, quên cộng nhiệt độ ban đầu của viên đạn.",
       ke=[(r"$t=t_0+\Delta t$, rồi so với $t_{nc}$", True),
           (r"$t=\Delta t$", r"$\Delta t$ là độ tăng ; viên đạn ban đầu đã ở 27 °C."),
           (r"So $\Delta t$ với $t_{nc}$ để kết luận", r"Phải so nhiệt độ cuối, không phải độ tăng nhiệt độ, với nhiệt độ nóng chảy.")]),
  buoc("Nhiệt lượng cho mỗi kilôgam chì chảy hết", "Mỗi kilôgam chì cần nhận bao nhiêu jun để từ 27 °C nóng chảy hoàn toàn?", float(Q6C), "J/kg", 500,
       loi=r"Chỉ tính nhiệt nóng chảy, quên phải đưa chì lên nhiệt độ nóng chảy trước ; hoặc tính độ tăng từ 0 °C.",
       ke=[(r"$\dfrac{Q}{m}=c\,(t_{nc}-t_0)+\lambda$", True),
           (r"$\dfrac{Q}{m}=\lambda$", r"Chì ở 27 °C chưa chảy được ; phải nóng tới 327 °C trước rồi mới nóng chảy."),
           (r"$\dfrac{Q}{m}=c\,t_{nc}+\lambda$", r"Chì bắt đầu từ 27 °C, không phải từ 0 °C ; độ tăng nhiệt độ là $t_{nc}-t_0$.")]),
  buoc("Tốc độ tối thiểu", "Tốc độ tối thiểu của viên đạn là bao nhiêu m/s?", V6C, "m/s", 1.5,
       loi=r"Lại bỏ $60\,\%$ hoặc quên $\tfrac12$ trong động năng như câu b ; quên lấy căn bậc hai.",
       ke=[(r"$0{,}6\cdot\dfrac12v^2=\dfrac{Q}{m}$ rồi lấy căn", True),
           (r"$\dfrac12v^2=\dfrac{Q}{m}$", r"Vẫn chỉ $60\,\%$ động năng làm nóng đạn ; bỏ hệ số này sẽ ra tốc độ nhỏ hơn thực tế cần."),
           (r"$0{,}6\cdot v^2=\dfrac{Q}{m}$", r"Động năng có $\dfrac12$ ; thiếu nó làm tốc độ tìm được nhỏ đi.")]),
  buoc("Kiểm tra")]),
]


# KaTeX: chỉ số dưới có dấu tiếng Việt → \text{…} (Q_{\text{ích}} → Q_{\text{ích}})
_SUBVN = re.compile(r"_\{([^{}\\]*[^\x00-\x7f][^{}\\]*)\}")
_SUBVN1 = re.compile(r"_([^\x00-\x7f])")                     # W_đ → W_{\text{đ}}
def _tx(x):
    if isinstance(x, str):
        if x.lstrip().startswith("<figure"):
            return x
        x = _SUBVN.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
        return _SUBVN1.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
    if isinstance(x, list):
        return [_tx(v) for v in x]
    if isinstance(x, tuple):
        return tuple(_tx(v) for v in x)
    if isinstance(x, dict):
        return {k: _tx(v) for k, v in x.items()}
    return x
_RAW_DANG, _RAW_ANALYSIS = DANG, ANALYSIS
DANG, ANALYSIS, SOLS, STEPS = _tx(DANG), _tx(ANALYSIS), _tx(SOLS), _tx(STEPS)


def kiem_so():
    # D4
    assert MN4 == 2 and QN4 == 672000 and QAL4 == 35200 and QICH4 == 707200 and QTP4 == 1768000 and QHH4 == 460000 and QTP4B == 1150000
    assert abs(float(MG4) - 40.18) < 0.01 and abs(float(MG4B) - 26.14) < 0.01
    assert round(float(MG4), 1) == 40.2 and round(float(MG4B), 1) == 26.1
    assert QN4 != QICH4 and abs(float(QN4 - QICH4)) > 1000                         # quên nồi → sai ngoài sai số
    assert H4 * QICH4 != QTP4 and QICH4 != QTP4                                     # hai cách sai bước 2
    assert abs(float(QICH4 / QG * 1000 - MG4)) > 0.3 and abs(float(H4 * QICH4 / QG * 1000 - MG4)) > 0.3   # bước 3
    assert QHH4 + (MN4 * CN + MAL4 * CAL) * (TS4 - T04) != QHH4 and MN4 * LHH != QHH4                    # bước 4
    assert abs(float(QHH4 / QG * 1000 - MG4B)) > 0.3 and abs(float((QICH4 + QHH4) / (H4 * QG) * 1000 - MG4B)) > 0.3   # bước 5
    # D5
    assert T2C == 28 and MR == F(1, 4) and T2L3 == F(168, 5)
    assert ((M1 - MR) * T1 + MR * T2C) / M1 == T1C                                  # nghiệm lại lần 2
    assert (M2 * T2 + MR * T1) / (M2 + MR) == T2C                                   # nghiệm lại lần 1
    assert (M1 * T1 + M2 * T2) / (M1 + M2) != T2C and (T1 + T2) / 2 != T2C          # trung bình không phải đáp số
    m_sai1 = M2 * (T2C - T2) / ((T1 - T2C) - (T2C - T2))                            # m(t1−t2') = (m2+m)(t2'−t2)
    m_sai2 = M2 * (T2C - T2) / (T1 - T1C)                                           # nguội tới 56 °C
    assert abs(float(m_sai1 - MR)) > 0.01 and abs(float(m_sai2 - MR)) > 0.01
    t_sai1 = ((M2 + MR) * T2C + MR * T1C) / (M2 + 2 * MR)
    t_sai2 = (M2 * T2C + MR * T1) / (M2 + MR)
    assert abs(float(t_sai1 - T2L3)) > 0.1 and abs(float(t_sai2 - T2L3)) > 0.1
    # D6
    assert DT6A == F(5, 21) and abs(float(DT6A) - 0.238) < 0.001 and round(float(DT6A), 2) == 0.24
    assert abs(float(DT6B) - 207.69) < 0.01 and round(float(T6B)) == 235 and T6B < TNC_PB and round(float(DT6B)) == 208
    assert Q6C == 64000 and abs(V6C - 461.88) < 0.01 and round(V6C) == 462 and V6C > V6
    assert abs(float(V6**2 / 2 / CPB - DT6B)) > 1 and abs(float(K6 * V6**2 / CPB - DT6B)) > 1             # bước 2
    assert abs(float(DT6B - T6B)) > 1 and DT6B < TNC_PB                                                     # bước 3 (Δt < 327 cũng ra "chưa chảy" nhưng là cách so sai)
    assert LAM_PB != Q6C and abs(float(CPB * TNC_PB + LAM_PB - Q6C)) > 500                                  # bước 4
    assert abs(math.sqrt(float(2 * Q6C)) - V6C) > 1.5 and abs(math.sqrt(float(Q6C / K6)) - V6C) > 1.5      # bước 5
    # bảng phân tích: cột 1 trích nguyên văn đề
    for n, rows in enumerate(_RAW_ANALYSIS):
        for r in rows:
            assert r[0].strip('"') in _RAW_DANG[n]["problem_html"], (n, r[0])
    # không lộ đáp số trong đề, hình, bảng phân tích, câu hỏi, lựa chọn, lỗi hay gặp
    lo = {0: ["707", "1768", "1 768", "40,2", "40,18", "460", "26,1", "26,14"],
          1: ["28", "0,25", "33,6", "25 kg"],
          2: ["0,24", "0,238", "208", "207", "235", "234", "64", "462", "461"]}
    for n in range(3):
        figs = re.sub(r"<[^>]+>", " ", BUILD[n](0) + BUILD[n](2))           # chỉ chữ hiện trên hình, bỏ toạ độ
        blob = DANG[n]["problem_html"] + figs + str(ANALYSIS[n]) + STEPS[n]["nhan_dang"]
        for s in STEPS[n]["buoc"]:
            blob += s.get("tieu_de", "") + s.get("hoi", "") + s.get("loi_hay_gap", "")
            for c in s.get("chon_buoc_ke", []) + s.get("lua_chon", []):
                blob += c["text"] + c.get("vi_sao", "")
        for x in lo[n]:
            assert x not in blob, (n, x)
    for n, s in enumerate(STEPS):
        assert s["cap_do"] in (3, 4) and len(s["buoc"]) == SOLS[n].count('class="bt-step"'), n
    print("btm153_d456: kiểm số liệu đạt")


if __name__ == "__main__":
    kiem_so()
