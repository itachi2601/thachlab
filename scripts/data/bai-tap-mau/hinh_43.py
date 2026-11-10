"""Hình cho bài tập mẫu Bài 24 "Nguồn điện" (Vật lí 11), lesson_id 43.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng dùng nguồn/bộ nguồn MẪU, số liệu khác đề (không lộ đáp số). Điện tích chạy theo chiều dòng điện quy ước
(ngoài nguồn từ cực + về cực −, trong nguồn từ − lên +). Chữ ℰ = suất điện động (khớp lý thuyết bài). Mọi hình: "không đúng tỉ lệ".
Mũi tên dòng điện là chevron 30° (hàm chevron của svg_lib), không dùng marker."""
import math, os, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
MINUS = "−"
EM = "ℰ"


def rich(s, size=13):
    """`I_dm` → I với chỉ số dưới dm (tspan dy), không dùng chỉ số Unicode."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out


def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)


def anim(attr, vals, dur, keytimes=None, discrete=False):
    v = ";".join(f"{x:.1f}" if isinstance(x, float) and not discrete else (f"{x}" if discrete else f"{x:.1f}") for x in vals)
    kt = f' keyTimes="{";".join(f"{k:.3f}" for k in keytimes)}"' if keytimes else ""
    cm = ' calcMode="discrete"' if discrete else ""
    return f'<animate attributeName="{attr}" values="{v}"{kt}{cm} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


# ───────────── đường đi của điện tích ─────────────
def along(vs, s):
    """Điểm cách điểm đầu một đoạn s (độ dài cung) dọc đường gấp khúc vs."""
    for (x0, y0), (x1, y1) in zip(vs, vs[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        if s <= d or (x1, y1) == vs[-1]:
            u = min(s / d, 1.0) if d else 0
            return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        s -= d
    return vs[-1]


def plen(vs):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(vs, vs[1:]))


def runner(paths, dur, N=60, hold=0.0, r=5.5, c=GRN):
    """Các hạt chạy MỘT lần, cùng tốc độ (đường ngắn dừng sớm ở khung cuối). `hold` = tỉ lệ thời gian đứng yên đầu tiên."""
    T = max(plen(p) for p in paths)
    out = ""
    for vs in paths:
        pts = [along(vs, T * i / N) for i in range(N + 1)]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        if hold:
            kt = [0.0] + [hold + (1 - hold) * i / N for i in range(N + 1)]
            xs = [xs[0]] + xs; ys = [ys[0]] + ys
        else:
            kt = None
        out += (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1.5">'
                f'{anim("cx", xs, dur, kt)}{anim("cy", ys, dur, kt)}</circle>')
    return out


# ───────────── mạch kín một vòng ─────────────
LX, RX, TY, BY = 110, 370, 44, 154
BC = (TY + BY) // 2


def pin_v(x, yc):
    """Pin (nguồn) đặt dọc: vạch dài (+) ở trên, vạch ngắn (−) ở dưới; dây nối lên/xuống."""
    b = seg(x, TY, x, yc - 9, "currentColor", 2.4) + seg(x, yc + 9, x, BY, "currentColor", 2.4)
    b += seg(x - 15, yc - 9, x + 15, yc - 9, "currentColor", 3.2) + seg(x - 8, yc + 9, x + 8, yc + 9, "currentColor", 3.2)
    b += txt(x + 24, yc - 3, "+", "currentColor", 15, "middle") + txt(x + 24, yc + 20, MINUS, "currentColor", 15, "middle")
    return b


def loop_static(r_box=True, volt=False, rlabel="R", em_label=None):
    """Khung mạch: nguồn bên trái (hộp nét đứt = có điện trở trong), điện trở R bên phải, (tuỳ chọn) vôn kế mắc ở hai cực nguồn."""
    b = seg(LX, TY, RX, TY, "currentColor", 2.4) + seg(LX, BY, RX, BY, "currentColor", 2.4)
    b += pin_v(LX, BC)
    if r_box:
        b += f'<rect x="{LX - 28}" y="{BC - 26}" width="62" height="52" rx="6" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" opacity=".6"/>'
    b += seg(RX, TY, RX, BC - 22, "currentColor", 2.4) + seg(RX, BC + 22, RX, BY, "currentColor", 2.4)
    b += f'<rect x="{RX - 8}" y="{BC - 22}" width="16" height="44" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    if rlabel:
        b += txt(RX - 16, BC + 5, rlabel, "currentColor", 14, "end")
    b += chevron(270, TY, 1, 0, "currentColor", 2.2, 11) + chevron(270, BY, -1, 0, "currentColor", 2.2, 11)
    b += txt(262, TY - 9, "I", "currentColor", 14, "middle")
    if volt:
        VX = 200
        b += seg(VX, TY, VX, BC - 16, "currentColor", 2) + seg(VX, BC + 16, VX, BY, "currentColor", 2)
        b += f'<circle cx="{VX}" cy="{BC}" r="15" fill="none" stroke="currentColor" stroke-width="2"/>' + txt(VX, BC + 5, "V", "currentColor", 14, "middle")
        b += dot(VX, TY, 3.5) + dot(VX, BY, 3.5)
    if em_label:
        b += txt(LX - 36 if r_box else LX - 22, BC + 5, em_label, "currentColor", 14, "end")
    return b


LOOP_PATH = [(230, TY), (RX, TY), (RX, BY), (LX, BY), (LX, TY), (230, TY)]   # xuất phát trên dây trên (không đè ký hiệu pin)


# ───────────── Dạng 1 · suất điện động ℰ = A/q ─────────────
def d1(kk):
    if kk == 0:
        b = loop_static(r_box=False, volt=False, rlabel="R", em_label=EM + " = 3,0 V")
        b += runner([LOOP_PATH], 6.0, 70)
        b += txt(20, 184, "Trong nguồn: lực lạ đưa điện tích từ cực − lên cực +", "currentColor", 12, "start", "600")
        b += txt(20, 202, "● điện tích dương mẫu chạy một vòng (nguồn mẫu 3,0 V)", GRN, 12, "start", "600")
        return fig("d1-0", "0 0 420 212", "Mạch kín gồm một nguồn điện và một điện trở; một điện tích dương chạy một vòng: ngoài nguồn từ cực dương về cực âm, trong nguồn từ cực âm lên cực dương",
                   b, "Mô phỏng: điện tích dương mẫu đi hết một vòng của mạch kín; nguồn mẫu có số liệu khác đề; chạy chậm hơn thật. " + NOTE)
    b = loop_static(r_box=False, volt=False, rlabel="R", em_label=EM + " = 12 V")
    b = b.replace(txt(262, TY - 9, "I", "currentColor", 14, "middle"), txt(262, TY - 9, "I = 0,50 A", "currentColor", 13, "middle"))
    b += txt(20, 184, "Lực lạ làm công A = 1,8·10³ J trong nguồn", RED, 13, "start", "600")
    b += txt(20, 204, "Cần tìm: q, t, và công A′ của pin 1,5 V", ORG, 13)
    return fig("d1-2", "0 0 420 214", "Mạch kín có ắc quy suất điện động 12 vôn, dòng điện không đổi 0,50 ampe; lực lạ trong nguồn làm công 1,8 nhân 10 mũ 3 jun", b,
               "Dữ kiện: nguồn, dòng điện và công của lực lạ. " + NOTE)


# ───────────── Dạng 2 · hở mạch U = ℰ; có dòng U < ℰ; tìm I, r, I_đm ─────────────
def d2(kk):
    if kk == 0:
        b = loop_static(r_box=True, volt=True, rlabel="R = 12 Ω", em_label=EM + ", r")
        # khoá trên dây trên: mở rồi đóng. Thuộc tính gốc = khung CUỐI (đóng).
        b += (f'<line x1="290" y1="{TY}" x2="340" y2="{TY}" stroke="currentColor" stroke-width="2.4" opacity="1">'
              f'{anim("opacity", [0, 1], 6.0, [0, 0.3], True)}</line>')
        b += (f'<line x1="290" y1="{TY}" x2="334" y2="{TY - 22}" stroke="currentColor" stroke-width="2.4" opacity="0">'
              f'{anim("opacity", [1, 0], 6.0, [0, 0.3], True)}</line>')
        b += dot(290, TY, 3.5) + dot(340, TY, 3.5) + txt(315, TY + 20, "khoá", "currentColor", 12, "middle", "600")
        b += runner([LOOP_PATH], 6.0, 70, hold=0.35)
        b += (f'<text x="20" y="184" fill="currentColor" font-size="13" font-weight="700" opacity="0">Khoá mở: vôn kế chỉ 4,5 V{anim("opacity", [1, 0], 6.0, [0, 0.3], True)}</text>')
        b += (f'<text x="20" y="184" fill="currentColor" font-size="13" font-weight="700" opacity="1">Khoá đóng: vôn kế chỉ 3,6 V{anim("opacity", [0, 1], 6.0, [0, 0.3], True)}</text>')
        b += txt(20, 204, "● pin mẫu ℰ = 4,5 V (số liệu khác đề)", GRN, 12, "start", "600")
        return fig("d2-0", "0 0 420 214", "Pin có điện trở trong nối với một điện trở qua một khoá; vôn kế mắc ở hai cực pin chỉ giá trị lớn khi khoá mở và giá trị nhỏ hơn khi khoá đóng",
                   b, "Mô phỏng: pin mẫu (số liệu khác đề). Khoá mở thì vôn kế chỉ một số, đóng khoá thì dòng chạy và số chỉ đổi; chạy chậm hơn thật. " + NOTE)
    b = loop_static(r_box=True, volt=True, rlabel="R = 30 Ω", em_label=EM + " = ?, r = ?")
    b += txt(20, 184, "Khoá mở: vôn kế 9,0 V · khoá đóng: vôn kế 7,5 V", "currentColor", 13, "start", "600")
    b += txt(20, 204, "Cần tìm: ℰ, I, r và dòng khi nối tắt hai cực", ORG, 13)
    return fig("d2-2", "0 0 420 214", "Pin có điện trở trong nối với điện trở 30 ôm, vôn kế mắc ở hai cực pin chỉ 9,0 vôn khi mạch hở và 7,5 vôn khi nối điện trở", b,
               "Dữ kiện: hai số chỉ của vôn kế ở hai cực pin. Đường nét đứt bao quanh nguồn: nguồn có điện trở trong. " + NOTE)


# ───────────── Dạng 3 · hai lần đo (R, U) → ℰ và r ─────────────
def mini(x0, tag, rtxt, utxt):
    """Mạch nhỏ: nguồn (hộp nét đứt) bên trái, R bên phải, vôn kế ở hai cực nguồn."""
    L, R_, T, B = x0, x0 + 150, 66, 146
    c = (T + B) // 2
    b = seg(L, T, R_, T, "currentColor", 2.2) + seg(L, B, R_, B, "currentColor", 2.2)
    b += seg(L, T, L, c - 8, "currentColor", 2.2) + seg(L, c + 8, L, B, "currentColor", 2.2)
    b += seg(L - 13, c - 8, L + 13, c - 8, "currentColor", 3) + seg(L - 7, c + 8, L + 7, c + 8, "currentColor", 3)
    b += f'<rect x="{L - 20}" y="{c - 22}" width="40" height="44" rx="5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="5 4" opacity=".6"/>'
    b += seg(R_, T, R_, c - 20, "currentColor", 2.2) + seg(R_, c + 20, R_, B, "currentColor", 2.2)
    b += f'<rect x="{R_ - 7}" y="{c - 20}" width="14" height="40" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    VX = L + 70
    b += seg(VX, T, VX, c - 14, "currentColor", 1.8) + seg(VX, c + 14, VX, B, "currentColor", 1.8)
    b += f'<circle cx="{VX}" cy="{c}" r="14" fill="none" stroke="currentColor" stroke-width="1.8"/>' + txt(VX, c + 5, "V", "currentColor", 13, "middle")
    b += dot(VX, T, 3) + dot(VX, B, 3)
    b += txt(L + 75, T - 24, tag + ": " + rtxt, "currentColor", 13, "middle") + txt(L + 22, c - 2, "+", "currentColor", 13, "middle")
    b += txt(L + 75, B + 24, utxt, "currentColor", 13, "middle", "600")
    return b


def d3(kk):
    if kk == 0:
        E_s, r_s = 1.2, 0.3                     # pin MẪU: ℰ = 1,5 V, r = 0,50 Ω → I_đm = 4,0 A
        ox, oy, sx, sy = 70, 150, 75.0, 90.0   # px/A, px/V
        b = seg(ox, oy, ox + 4.4 * sx, oy, "currentColor", 2) + seg(ox, oy, ox, oy - 1.5 * sy, "currentColor", 2)
        b += chevron(ox + 4.4 * sx, oy, 1, 0, "currentColor", 2, 10) + chevron(ox, oy - 1.5 * sy, 0, -1, "currentColor", 2, 10)
        for I in (1, 2, 3, 4):
            b += seg(ox + I * sx, oy - 4, ox + I * sx, oy + 4, "currentColor", 1.6) + txt(ox + I * sx, oy + 19, str(I), "currentColor", 12, "middle", "600")
        for U, s in ((0.4, "0,4"), (0.8, "0,8"), (1.2, "1,2")):
            b += seg(ox - 4, oy - U * sy, ox + 4, oy - U * sy, "currentColor", 1.6) + txt(ox - 9, oy - U * sy + 4, s, "currentColor", 12, "end", "600")
        b += txt(ox + 4.4 * sx + 4, oy + 19, "I (A)", "currentColor", 12, "end") + txt(ox + 8, oy - 1.5 * sy + 6, "U (V)", "currentColor", 12, "start")
        b += seg(ox, oy - E_s * sy, ox + (E_s / r_s) * sx, oy, BLUE, 2.2, "", 1)
        b += dot(ox, oy - E_s * sy, 4, BLUE) + dot(ox + (E_s / r_s) * sx, oy, 4, BLUE)
        b += txt(ox + 12, oy - E_s * sy - 8, EM + " = 1,2 V (hở mạch)", BLUE, 12, "start", "600")
        b += txt(ox + 4.0 * sx - 4, oy - 42, "đoản mạch ↓", BLUE, 12, "end", "600")
        n = 60; I_end = 3.2
        pts = [(ox + (I_end * i / n) * sx, oy - (E_s - r_s * I_end * i / n) * sy) for i in range(n + 1)]
        b += (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
              f'{anim("cx", [p[0] for p in pts], 5.0)}{anim("cy", [p[1] for p in pts], 5.0)}</circle>')
        b += txt(20, 190, "● điểm đo (I, U) của pin mẫu, dòng tăng dần", GRN, 12, "start", "600")
        return fig("d3-0", "0 0 420 202", "Đồ thị hiệu điện thế hai cực pin theo cường độ dòng: đường thẳng đi xuống từ giá trị suất điện động trên trục tung tới trục hoành; một điểm chạy dọc đường thẳng khi dòng tăng",
                   b, "Mô phỏng: pin mẫu (ℰ = 1,2 V, r khác đề), điểm (I, U) chạy dọc đồ thị khi dòng tăng; đường thẳng cắt hai trục. " + NOTE)
    b = mini(30, "Lần 1", "R_1 = 3,0 Ω", "vôn kế chỉ U_1 = 3,6 V") + mini(240, "Lần 2", "R_2 = 10 Ω", "vôn kế chỉ U_2 = 5,0 V")
    b += txt(20, 20, "Cùng một nguồn (ℰ, r không đổi), hai lần đo", "currentColor", 13, "start", "600")
    b += txt(20, 212, "Cần tìm: I_1, I_2, ℰ, r và dòng khi nối tắt", ORG, 13)
    return fig("d3-2", "0 0 420 224", "Hai lần đo cùng một nguồn: nối điện trở 3,0 ôm thì vôn kế ở hai cực chỉ 3,6 vôn, nối điện trở 10 ôm thì vôn kế chỉ 5,0 vôn", b,
               "Dữ kiện: hai lần đo trên cùng một nguồn; vôn kế mắc ở hai cực nguồn. " + NOTE)


# ───────────── Dạng 4 · bộ nguồn hỗn hợp đối xứng (n dãy song song, mỗi dãy m pin nối tiếp) ─────────────
BL, BR = 60, 350


def pin_h(x, y):
    """Pin nằm ngang: vạch ngắn (−) bên trái, vạch dài (+) bên phải; dòng quy ước đi trong nguồn từ − sang +."""
    return seg(x - 6, y - 7, x - 6, y + 7, "currentColor", 3) + seg(x + 6, y - 13, x + 6, y + 13, "currentColor", 3.2)


def bank(rows_y, m, bot_y, rlabel):
    b = seg(BL, rows_y[0], BL, bot_y, "currentColor", 2.4) + seg(BR, rows_y[0], BR, bot_y, "currentColor", 2.4)
    step = (BR - BL) / m
    for y in rows_y:
        xs = [BL]
        for i in range(m):
            cx = BL + step * (i + 0.5)
            b += seg(xs[-1], y, cx - 6, y, "currentColor", 2.4) + pin_h(cx, y)
            xs.append(cx + 6)
        b += seg(xs[-1], y, BR, y, "currentColor", 2.4)
    rx0 = (BL + BR) / 2 - 30
    b += seg(BL, bot_y, rx0, bot_y, "currentColor", 2.4) + seg(rx0 + 60, bot_y, BR, bot_y, "currentColor", 2.4)
    b += f'<rect x="{rx0}" y="{bot_y - 8}" width="60" height="16" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    b += txt((BL + BR) / 2, bot_y + 28, rlabel, "currentColor", 13, "middle")
    for y in rows_y + (bot_y,):
        b += dot(BL, y, 3.2) + dot(BR, y, 3.2)
    return b


def d4(kk):
    if kk == 0:
        rows = (48, 92, 136); bot = 178; m = 2
        b = bank(rows, m, bot, "R")
        for y in rows:
            b += chevron(BL + (BR - BL) / m * 0.5 + (BR - BL) / m * 0.5, y, 1, 0, "currentColor", 2.2, 10)
        b += chevron(120, bot, -1, 0, "currentColor", 2.2, 10)
        paths = [[(BL, y), (BR, y), (BR, bot), (BL, bot), (BL, y)] for y in rows]
        b += runner(paths, 6.0, 70)
        b += txt(BL, 20, "bộ mẫu: 3 dãy song song, mỗi dãy 2 pin nối tiếp", "currentColor", 12, "start", "600")
        b += txt(20, 228, "● ba điện tích dương, mỗi điện tích đi qua một dãy rồi qua R", GRN, 12, "start", "600")
        return fig("d4-0", "0 0 420 238", "Bộ nguồn gồm ba dãy pin song song, mỗi dãy hai pin nối tiếp, nối với một điện trở; ba điện tích dương chạy qua ba dãy rồi cùng qua điện trở",
                   b, "Mô phỏng: bộ nguồn mẫu 3 dãy × 2 pin (khác đề); ba điện tích đi qua ba dãy rồi trở về qua điện trở R; chạy chậm hơn thật. " + NOTE)
    rows = (60, 112); bot = 164; m = 4
    b = bank(rows, m, bot, "R = 3,0 Ω")
    for y in rows:
        b += chevron(BL + (BR - BL) / m, y, 1, 0, "currentColor", 2.2, 10)
    b += chevron(120, bot, -1, 0, "currentColor", 2.2, 10) + txt(120, bot - 10, "I = ?", "currentColor", 13, "middle")
    b += txt(BR + 10, rows[0] + 5, "dãy 1", "currentColor", 12, "start", "600") + txt(BR + 10, rows[1] + 5, "dãy 2", "currentColor", 12, "start", "600")
    b += txt(BL, 22, "mỗi pin: ℰ_0 = 1,5 V; r_0 = 0,50 Ω", "currentColor", 13, "start", "600")
    b += txt(20, 212, "Cần tìm: ℰ_b, r_b, I, U hai cực bộ, dòng qua mỗi pin", ORG, 13)
    return fig("d4-2", "0 0 420 222", "Bộ nguồn gồm hai dãy song song, mỗi dãy bốn pin giống nhau nối tiếp, nối với điện trở 3,0 ôm", b,
               "Dữ kiện: cách ghép 8 pin giống nhau; vạch dài của pin là cực +; mũi tên là chiều dòng điện quy ước (trong nguồn từ cực − sang cực +). " + NOTE)
