"""Hình cho bài tập mẫu Bài 18 (Vật lí 12) "An toàn phóng xạ", lesson_id 19.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Hình chỉ vẽ cảnh và dữ kiện của đề (nguồn, người đứng, thước, đồng hồ), mọi đại lượng cần tìm ghi "?"; liều kế không có thang, không vạch giới hạn."""
import math, os, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
YEL = "#facc15"
GREY = "#94a3b8"


def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, op=1, fop=None):
    f = f' fill-opacity="{fop}"' if fop is not None else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{f} stroke="{c}" '
            f'stroke-width="{sw}" opacity="{op}"/>')

def tissue(x, y, w, h, anim, rx=8, dur=4):
    """Khối mô: tô xanh; khi chạy sáng dần (hấp thụ năng lượng)."""
    if not anim:
        return R(x, y, w, h, GRN, 2.2, GRN, rx, fop=0.3)
    return (R(x, y, w, h, GRN, 2.2, GRN, rx, fop=0.15)[:-2] + f'><animate attributeName="fill-opacity" values=".15;.55" dur="{dur}s" begin="indefinite" fill="freeze"/></rect>')

def rich(s, size=13):
    """`H_1` → H với chỉ số dưới 1."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def trefoil(cx, cy, r):
    """Biển ba cánh: ba cánh quạt vàng, tâm chấm."""
    b = ""
    for k in range(3):
        a = 90 + 120 * k
        p0 = (cx + r * math.cos(math.radians(a - 30)), cy - r * math.sin(math.radians(a - 30)))
        p1 = (cx + r * math.cos(math.radians(a + 30)), cy - r * math.sin(math.radians(a + 30)))
        b += (f'<path d="M{cx},{cy} L{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 0 0 {p1[0]:.1f},{p1[1]:.1f} Z" fill="{YEL}" stroke="currentColor" stroke-width="1.2"/>')
    return b + f'<circle cx="{cx}" cy="{cy}" r="{r * 0.2:.1f}" fill="currentColor"/>'

def ray(x1, y1, x2, y2, c=BLUE, w=1.8):
    """Tia: nét đứt + đầu V 30° (không dùng marker)."""
    return seg(x1, y1, x2, y2, c, w, "6 4") + chevron(x2, y2, x2 - x1, y2 - y1, c, w, 10)

def glide(x0, y0, x1, y1, a, b, dur, r=3.4, c=BLUE):
    """Hạt xuất hiện lúc a (phần của dur), tới (x1,y1) lúc b rồi biến mất."""
    kt = f"0;{a:.3f};{b:.3f};1"
    an = lambda at, v0, v1: (f'<animate attributeName="{at}" values="{v0};{v0};{v1};{v1}" keyTimes="{kt}" dur="{dur}s" begin="indefinite" fill="freeze"/>')
    return (f'<circle cx="{x0}" cy="{y0}" r="{r}" fill="{c}" opacity="0">{an("cx", x0, x1)}{an("cy", y0, y1)}'
            f'<animate attributeName="opacity" values="0;1;0;0" keyTimes="{kt}" calcMode="discrete" dur="{dur}s" begin="indefinite" fill="freeze"/></circle>')

def ring(cx, cy, r0, r1, a, b, dur, c=BLUE):
    """Vòng sóng toả ra từ nguồn, hiện lúc a, tắt lúc b."""
    kt = f"0;{a:.3f};{a + 0.001:.3f};{b:.3f};1"
    return (f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="none" stroke="{c}" stroke-width="1.8" stroke-dasharray="6 4" opacity="0">'
            f'<animate attributeName="r" values="{r0};{r0};{r0};{r1};{r1}" keyTimes="{kt}" dur="{dur}s" begin="indefinite" fill="freeze"/>'
            f'<animate attributeName="opacity" values="0;0;.85;0;0" keyTimes="{kt}" dur="{dur}s" begin="indefinite" fill="freeze"/></circle>')

def man(x, gy, s=1.0):
    """Người đứng dạng que, chân tại gy."""
    hy = gy - 62 * s; ty = gy - 36 * s
    b = f'<circle cx="{x}" cy="{hy:.1f}" r="{8 * s:.1f}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    b += seg(x, hy + 8 * s, x, ty, "currentColor", 2.2) + seg(x, ty, x - 9 * s, gy, "currentColor", 2.2) + seg(x, ty, x + 9 * s, gy, "currentColor", 2.2)
    b += seg(x, hy + 16 * s, x - 11 * s, ty + 4 * s, "currentColor", 2.2) + seg(x, hy + 16 * s, x + 11 * s, ty + 4 * s, "currentColor", 2.2)
    return b

def clock(cx, cy, r, turn_deg=None, dur=4, label=None):
    """Mặt đồng hồ 60 phút; kim quay `turn_deg` độ khi chạy (None = đứng yên ở số 12)."""
    b = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="2"/>'
    for k in range(12):
        a = math.radians(30 * k)
        b += seg(cx + (r - 4) * math.sin(a), cy - (r - 4) * math.cos(a), cx + r * math.sin(a), cy - r * math.cos(a), "currentColor", 1.4)
    h = f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r + 6}" stroke="{RED}" stroke-width="2.4" stroke-linecap="round">'
    if turn_deg:
        h += f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};{turn_deg} {cx} {cy}" dur="{dur}s" begin="indefinite" fill="freeze"/>'
    b += h + "</line>" + dot(cx, cy, 2.6, "currentColor")
    return b

def meter(x, y, w, h, fill_to=None, dur=4):
    """Liều kế: ống chứa không thang, không vạch giới hạn; thanh dâng lên khi chạy."""
    b = R(x, y, w, h, sw=2, rx=5)
    if fill_to is not None:
        b += (f'<rect x="{x + 3}" y="{y + h - 3}" width="{w - 6}" height="1" fill="{ORG}">'
              f'{smil("y", [y + h - 3, y + h - 3 - fill_to], dur)}{smil("height", [1, fill_to], dur)}</rect>')
    return b


# ───────────── Dạng 1 · ống tia X chiếu vào 12 kg mô ngực, E = 1,2 mJ ─────────────
def d1(kk):
    anim = kk == 0
    b = R(20, 82, 54, 36, rx=6, sw=2.2) + txt(47, 104, "X", "currentColor", 16, "middle")
    b += txt(47, 138, "Ống tia X", "currentColor", 12, "middle", "400")
    ys = (88, 100, 112)
    b += tissue(232, 56, 96, 88, anim, 10)
    if anim:
        for i in range(6):
            y1 = ys[i % 3]; a = 0.02 + 0.13 * i
            b += glide(74, y1, 230, y1, a, min(a + 0.32, 0.98), 4)
    else:
        for y1 in ys:
            b += ray(74, y1, 228, y1)
    b += txt(280, 94, "m = 12 kg", "currentColor", 13, "middle") + txt(280, 118, "E = 1,2 mJ", "currentColor", 13, "middle")
    b += txt(280, 48, "Mô ngực", "currentColor", 12, "middle", "400")
    b += txt(344, 90, "D = ?", ORG, 14) + txt(344, 114, "H = ?", ORG, 14)
    b += txt(16, 28, "Tia X: w_R = 1", "currentColor", 13) + txt(16, 184, "Năng lượng chia đều trong khối mô", "currentColor", 12, "start", "400")
    if anim:
        return fig("d1-0", "0 0 420 200", "Ống tia X chiếu các photon vào khối mô ngực, khối mô hấp thụ dần và sáng lên", b,
                   "Mô phỏng: các photon tia X đi vào khối mô và bị hấp thụ, mô sáng dần trong 4 s. " + NOTE)
    return fig("d1-2", "0 0 420 200", "Dữ kiện: khối mô ngực 12 kilôgam hấp thụ 1,2 mili jun từ chùm tia X, hệ số chất lượng bằng 1", b,
               "Dữ kiện: khối lượng mô, năng lượng hấp thụ và hệ số chất lượng của tia X; D và H chưa biết. " + NOTE)


# ───────────── Dạng 2 · hai mẫu mô 0,50 kg, cùng E = 2,0 mJ: gamma (A) và alpha (B) ─────────────
def d2(kk):
    anim = kk == 0
    b = trefoil(24, 100, 10) + trefoil(234, 100, 10)
    b += txt(136, 40, "Mẫu A · tia gamma", "currentColor", 13, "middle") + txt(344, 40, "Mẫu B · tia alpha", "currentColor", 13, "middle")
    b += tissue(100, 62, 72, 76, anim) + tissue(310, 62, 72, 76, anim)
    b += txt(136, 82, "0,50 kg", "currentColor", 13, "middle") + txt(346, 82, "0,50 kg", "currentColor", 13, "middle")
    if anim:
        for i in range(5):
            a = 0.02 + 0.14 * i
            b += glide(38, 100 + (i - 2) * 9, 200, 100 + (i - 2) * 9, a, min(a + 0.36, 0.98), 4)           # gamma xuyên qua mẫu A
            b += glide(248, 100 + (i - 2) * 9, 318, 100 + (i - 2) * 9, a, min(a + 0.3, 0.98), 4, 4.6, RED)  # alpha dừng ở mặt mẫu B
    else:
        for dy in (-9, 0, 9):
            b += ray(38, 100 + dy, 200, 100 + dy) + seg(248, 100 + dy, 316, 100 + dy, RED, 1.8, "6 4")
        b += chevron(316, 100, 1, 0, RED, 1.8, 10)
    b += txt(136, 160, "D = ?   H = ?", ORG, 13, "middle") + txt(346, 160, "D = ?   H = ?", ORG, 13, "middle")
    b += txt(210, 188, "Mỗi mẫu hấp thụ E = 2,0 mJ", "currentColor", 13, "middle")
    if anim:
        return fig("d2-0", "0 0 420 200", "Tia gamma đi xuyên mẫu A, hạt alpha dừng ngay ở mặt mẫu B, hai mẫu cùng sáng dần", b,
                   "Mô phỏng: tia gamma (xanh) xuyên qua mẫu A, hạt alpha (đỏ) dừng ở mặt mẫu B; cả hai mẫu hấp thụ cùng một năng lượng, coi chia đều trong mẫu. " + NOTE)
    return fig("d2-2", "0 0 420 200", "Dữ kiện: hai mẫu mô 0,50 kilôgam, mẫu A chiếu tia gamma, mẫu B chiếu tia alpha, mỗi mẫu hấp thụ 2,0 mili jun", b,
               "Dữ kiện: khối lượng mỗi mẫu, năng lượng hấp thụ chung (coi chia đều trong mẫu) và loại tia; D và H chưa biết. " + NOTE)


# ───────────── Dạng 3 · 72 µSv/h tại 0,50 m; hỏi tại 1,5 m và khoảng cách để còn 2,0 µSv/h ─────────────
def d3(kk):
    anim = kk == 0
    X0, S = 40, 120                       # nguồn ở x = 40; 120 px mỗi mét
    gy = 150
    X = lambda m: X0 + S * m
    b = trefoil(X0, 96, 14) + seg(X0, 110, X0, gy, "currentColor", 2)
    b += seg(X0, gy, X(2.5), gy, "currentColor", 2.2)
    for m, t in ((0, "0"), (0.5, "0,5"), (1, "1,0"), (1.5, "1,5"), (2, "2,0"), (2.5, "2,5")):
        b += seg(X(m), gy - 5, X(m), gy + 5, "currentColor", 1.6) + txt(X(m), gy + 20, t, "currentColor", 12, "middle", "400")
    b += txt(X(2.5) + 12, gy + 20, "m", "currentColor", 12, "start", "400")
    for m, label, c in ((0.5, "72 µSv/h", "currentColor"), (1.5, "? µSv/h", ORG)):
        b += R(X(m) - 11, gy - 36, 22, 16, c, 2, rx=3) + seg(X(m), gy - 20, X(m), gy, c, 2) + txt(X(m), gy - 44, label, c, 13, "middle")
    b += txt(X0, 56, "Nguồn gamma nhỏ", "currentColor", 12, "start", "400") + txt(X(2.5) + 6, 34, "Tìm r để còn 2,0 µSv/h: r = ?", ORG, 12, "end")
    if anim:
        for k in range(3):
            a = 0.03 + 0.26 * k
            b += ring(X0, 96, 14, 270, a, min(a + 0.7, 0.99), 4)
        return fig("d3-0", "0 0 420 200", "Các vòng bức xạ toả ra từ nguồn, đi qua máy đo ở 0,5 mét rồi tới điểm cách 1,5 mét", b,
                   "Mô phỏng: bức xạ toả đều theo mọi hướng, các vòng lan ra xa nguồn trong 4 s. Thước vẽ đúng tỉ lệ; vòng sóng chỉ minh hoạ.")
    for dy in (-36, -12):
        b += ray(X0 + 16, 96 + dy / 3, X(2.3), 96 + dy)
    return fig("d3-2", "0 0 420 200", "Dữ kiện: nguồn gamma nhỏ, máy đo cách 0,5 mét cho 72 micrô xi-vơ trên giờ, cần tìm suất liều ở 1,5 mét", b,
               "Dữ kiện: thước vẽ đúng tỉ lệ; suất liều tại 0,5 m cho trước, các đại lượng còn lại chưa biết.")


# ───────────── Dạng 4 · 250 µSv/h tại 1,0 m; người đứng cách 2,5 m; 12 phút; liều ≤ 20 µSv ─────────────
def _canh(kind, anim):
    """Cảnh nguồn – máy đo (1,0 m) – người đứng; kind 4: người ở 2,5 m, 6: ở 2,0 m. 100 px mỗi mét."""
    X0, S, gy = 40, 100, 172
    X = lambda m: X0 + S * m
    d_ng = 2.5 if kind == 4 else 2.0
    b = trefoil(X0, 140, 14) + seg(X0, 154, X0, gy, "currentColor", 2) + seg(X0 - 18, gy, X(d_ng) + 40, gy, "currentColor", 2.4)
    mdo = "250 µSv/h" if kind == 4 else "160 µSv/h"
    b += R(X(1) - 12, 138, 24, 16, "currentColor", 2, rx=3) + seg(X(1), 154, X(1), gy, "currentColor", 2) + txt(X(1), 128, mdo, "currentColor", 12, "middle")
    b += txt(X(1), 192, "1,0 m", "currentColor", 12, "middle", "400") + txt(X(d_ng), 192, ("2,5 m" if kind == 4 else "2,0 m"), "currentColor", 12, "middle", "400")
    b += man(X(d_ng), gy, 1.05)
    b += txt(X(d_ng), 82, "suất liều: ?", ORG, 12, "middle")
    cx, cy = 372, 46
    if anim:
        b += clock(cx, cy, 24, 72 if kind == 4 else 1800, 4)
        b += meter(354, 100, 36, 62, 30 if kind == 4 else 26, 4)
        for i in range(6):
            a = 0.02 + 0.14 * i
            b += glide(58, 140, X(d_ng) - 14, 140, a, min(a + 0.3, 0.98), 4)
    else:
        b += clock(cx, cy, 24) + meter(354, 100, 36, 62)
        b += ray(58, 140, X(d_ng) - 14, 140)
    b += txt(372, 84, "12 phút" if kind == 4 else "2 000 giờ", "currentColor", 12, "middle", "400")
    b += txt(372, 180, "Liều kế", "currentColor", 12, "middle", "400")
    return b

def d4(kk):
    anim = kk == 0
    b = _canh(4, anim)
    if anim:
        return fig("d4-0", "0 0 420 200", "Nguồn gamma, người đứng cách 2,5 mét, đồng hồ chạy 12 phút và liều kế dâng dần", b,
                   "Mô phỏng: kim đồng hồ quay 12 phút trong 4 s (mặt đồng hồ chia 60 phút); thanh liều kế chỉ minh hoạ liều tăng theo thời gian, không có thang. " + NOTE)
    return fig("d4-2", "0 0 420 200", "Dữ kiện: máy đo cách nguồn 1,0 mét cho 250 micrô xi-vơ trên giờ, người đứng cách nguồn 2,5 mét", b,
               "Dữ kiện: thước vẽ đúng tỉ lệ; suất liều tại 1,0 m cho trước, suất liều tại chỗ đứng và liều chưa biết.")


# ───────────── Dạng 5 · hai biện pháp (khoảng cách, thời gian) và hai tấm chắn; 40 phút, 1,0 m ─────────────
def d5(kk):
    anim = kk == 0
    gy = 96
    b = trefoil(40, 62, 12) + seg(40, 74, 40, gy, "currentColor", 2) + seg(22, gy, 190, gy, "currentColor", 2.4)
    b += man(140, gy, 0.82) + txt(140, 20, "cách nguồn 1,0 m", "currentColor", 12, "middle", "400")
    cx, cy = 340, 56
    b += txt(cx, 20, "40 phút/ca", "currentColor", 12, "middle", "400")
    if anim:
        b += clock(cx, cy, 26, 240, 4)
        for i in range(6):
            a = 0.02 + 0.14 * i
            b += glide(56, 62, 124, 62, a, min(a + 0.3, 0.98), 4)
        return fig("d5-0", "0 0 420 110", "Nguồn gamma, kỹ thuật viên đứng cách 1,0 mét, đồng hồ chạy 40 phút trong một ca", b,
                   "Mô phỏng: một ca 40 phút (kim quay 40 phút trong 4 s; mặt đồng hồ chia 60 phút) khi chưa có biện pháp giảm liều nào. " + NOTE)
    b += clock(cx, cy, 26)
    b += ray(56, 62, 124, 62)
    rows = ("A  lùi ra xa: 1,0 m → 3,0 m (giữ 40 phút)", "B  rút thời gian: 40 → 10 phút (giữ 1,0 m)",
            "C  chèn chì 5 mm: 360 → 154 xung/phút", "D  chèn nhôm 3 mm: 360 → 335 xung/phút")
    b2 = b
    for i, r_ in enumerate(rows):
        b2 += txt(16, 138 + 22 * i, r_, "currentColor", 13, "start", "600")
    return fig("d5-2", "0 0 420 226", "Dữ kiện: bốn biện pháp giảm liều A lùi xa, B rút thời gian, C chèn chì, D chèn nhôm, kèm số liệu của đề", b2,
               "Dữ kiện: bốn biện pháp, mỗi biện pháp áp dụng riêng; số đếm do máy đo ghi trước và sau khi chèn tấm chắn. " + NOTE)


# ───────────── Dạng 6 · 160 µSv/h tại 1,0 m; người đứng cách 2,0 m; 2 000 giờ/năm; giới hạn 20 mSv/năm ─────────────
def d6(kk):
    anim = kk == 0
    b = _canh(6, anim)
    if anim:
        return fig("d6-0", "0 0 420 200", "Nguồn gamma, người đứng cách 2,0 mét, đồng hồ quay nhiều vòng và liều kế dâng dần trong một năm làm việc", b,
                   "Mô phỏng: kim đồng hồ quay nhiều vòng để biểu thị 2 000 giờ làm việc trong năm; thanh liều kế chỉ minh hoạ liều tích luỹ, không có thang. " + NOTE)
    return fig("d6-2", "0 0 420 200", "Dữ kiện: máy đo cách nguồn 1,0 mét cho 160 micrô xi-vơ trên giờ, người làm việc đứng cách nguồn 2,0 mét", b,
               "Dữ kiện: thước vẽ đúng tỉ lệ; suất liều tại 1,0 m cho trước, suất liều tại chỗ đứng và liều cả năm chưa biết.")
