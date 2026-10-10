"""Hình cho bài tập mẫu Bài 2 "Thang nhiệt độ" (Vật lí 12), lesson_id 3.
Mỗi hàm d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng dùng số liệu MẪU khác đề (không lộ đáp số); chuyển động tính từ công thức (nhiệt kế: hai khối nước bằng nhau, T = 40 ± 20·e^(−6u)).
Vectơ không dùng ở bài này nên không có mũi tên tỉ lệ; mũi tên đơn dùng arrow() (đầu V 30°)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


# ───────────── tiện ích ─────────────
def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1, fop=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{fop}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none", fop=1):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" fill-opacity="{fop}" stroke="{c}" stroke-width="{sw}"/>'

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, s, c, size, anchor, weight)

UNIT = {"C": "°C", "K": "K", "F": "°F"}
NAME = {"C": "Celsius", "K": "Kelvin", "F": "Fahrenheit"}

def val(scale, tc):
    """Số đọc của nhiệt độ tc (°C) trên thang scale (làm tròn 273 như bài giảng)."""
    return {"C": tc, "K": tc + 273, "F": 1.8 * tc + 32}[scale]

TF = 't<tspan dy="4" font-size="9">F</tspan>'

def fmt(v):
    return f"{v:g}".replace(".", ",")


# ───────────── nhiệt kế đặt trong hai khối nước ngăn bởi vách dẫn nhiệt ─────────────
Y_TOP, Y_BOT = 62, 168           # ống nhiệt kế: 100 °C ở Y_TOP, 0 °C ở Y_BOT
def yT(tc):
    return Y_BOT - (Y_BOT - Y_TOP) * tc / 100.0

def thermometer(cx, scale, y_merc, merc_anim=""):
    b = R(cx - 7, Y_TOP - 6, 14, Y_BOT - Y_TOP + 12, sw=2, rx=7) + circ(cx, Y_BOT + 12, 10, "currentColor", 2, RED, .85)
    for tc in (0, 50, 100):
        y = yT(tc)
        b += seg(cx + 7, y, cx + 14, y, "currentColor", 1.6) + txt(cx + 17, y + 4, fmt(val(scale, tc)), "currentColor", 12, "start", "500")
    b += txt(cx, Y_TOP - 16, UNIT[scale], "currentColor", 13, "middle")
    b += (f'<rect x="{cx - 3.5}" y="{y_merc:.1f}" width="7" height="{Y_BOT - y_merc + 4:.1f}" fill="{RED}">{merc_anim}</rect>')
    return b

def mix(p, kk, sl, sr, t_hot=60, t_cold=20):
    """Hai khối nước bằng nhau, ngăn bởi vách dẫn nhiệt. kk=0: nhiệt kế hội tụ về cùng mức; kk=2 không dùng."""
    n = 25; us = [i / (n - 1) for i in range(n)]
    th = [40 + (t_hot - 40) * math.exp(-6 * u) for u in us]
    tc = [40 + (t_cold - 40) * math.exp(-6 * u) for u in us]
    dur = 5.0
    cl, cr = 100, 320
    b = defs(p)
    b += R(30, 28, 174, 170, "currentColor", 2, RED, 0, "", 1, .10) + R(216, 28, 174, 170, "currentColor", 2, BLUE, 0, "", 1, .10)
    b += R(204, 22, 12, 182, "currentColor", 1.6, GREY, 0, "", 1, .5)
    def anim(series):
        ys = [yT(t) for t in series]
        return smil("y", ys, dur) + smil("height", [Y_BOT - y + 4 for y in ys], dur)
    b += thermometer(cl, sl, yT(t_hot), anim(th)) + thermometer(cr, sr, yT(t_cold), anim(tc))
    b += txt(117, 216, "nước nóng", RED, 13, "middle") + txt(303, 216, "nước lạnh", BLUE, 13, "middle")
    b += txt(210, 16, "vách dẫn nhiệt", "currentColor", 12, "middle", "500")
    return fig("m-0" if sl == sr else "m5-0", "0 0 420 226",
               "Hai khối nước bằng nhau, một nóng một lạnh, ngăn bởi vách dẫn nhiệt; hai nhiệt kế dần chỉ cùng một mức",
               b, f"Mô phỏng mẫu (số liệu khác đề): hai khối nước bằng nhau, {fmt(val(sl, t_hot))} {UNIT[sl]} và {fmt(val(sr, t_cold))} {UNIT[sr]} lúc đầu. "
                  "Thời gian rút gọn, chạy 5 s. Mức thuỷ ngân là mức nóng, không phụ thuộc thang đọc.")


# ───────────── các thang đặt song song, con trỏ / đoạn chênh ─────────────
def y_scale(tc):
    return 200 - 1.6 * tc            # 0 °C ở y=200, 100 °C ở y=40

def scales(p, kinds, mode, t0, t1, cid):
    """mode='marker': con trỏ chạy từ t0 đến t1 (°C). mode='span': đoạn chênh t0→t1 'mọc' dần trên mọi thang."""
    xs = {2: [150, 270], 3: [90, 210, 330]}[len(kinds)]
    b = defs(p)
    for ax, k in zip(xs, kinds):
        b += seg(ax, y_scale(0), ax, y_scale(100), "currentColor", 2.4)
        b += txt(ax, 22, f"{NAME[k]} ({UNIT[k]})" if len(kinds) == 2 else NAME[k], "currentColor", 12, "middle")
        for tc in (0, 25, 50, 75, 100):
            y = y_scale(tc)
            b += seg(ax - 5, y, ax + 5, y, "currentColor", 1.6) + txt(ax - 9, y + 4, fmt(val(k, tc)), "currentColor", 12, "end", "500")
    dur = 4.0; m = 13
    ts = [t0 + (t1 - t0) * i / (m - 1) for i in range(m)]
    if mode == "marker":
        for i in range(len(xs) - 1):                     # đoạn nối hai trục, dừng trước nhãn của trục kế
            xa, xb = xs[i] + 6, xs[i + 1] - 44
            ys = [y_scale(t) for t in ts]
            b += (f'<line x1="{xa}" y1="{ys[0]:.1f}" x2="{xb}" y2="{ys[0]:.1f}" stroke="{ORG}" stroke-width="2" stroke-dasharray="4 3">'
                  f'{smil("y1", ys, dur)}{smil("y2", ys, dur)}</line>')
        for ax in xs:
            ys = [y_scale(t) for t in ts]
            b += (f'<circle cx="{ax}" cy="{ys[0]:.1f}" r="6" fill="{ORG}" stroke="currentColor" stroke-width="1.5">{smil("cy", ys, dur)}</circle>')
        cap = (f"Mô phỏng mẫu: cùng một nhiệt độ chạy từ {fmt(t0)} °C đến {fmt(t1)} °C, đọc trên các thang song song "
               f"(tại {fmt(t1)} °C: " + " = ".join(f"{fmt(val(k, t1))} {UNIT[k]}" for k in kinds) + "). Chạy 4 s.")
    else:
        for ax, k in zip(xs, kinds):
            ytop, ybot = y_scale(t1), y_scale(t0)
            b += (f'<rect x="{ax - 6}" y="{ybot:.1f}" width="12" height="0" fill="{ORG}" fill-opacity=".55" stroke="{ORG}" stroke-width="1.5">'
                  f'{smil("y", [ybot, ytop], dur)}{smil("height", [0, ybot - ytop], dur)}</rect>')
            dv = val(k, t1) - val(k, t0)
        cap = (f"Mô phỏng mẫu: khoảng nóng lên từ {fmt(t0)} °C đến {fmt(t1)} °C (số liệu khác đề), đọc trên ba thang. "
               "Đọc khoảng nóng lên trên ba thang. Chạy 4 s.")
    alt = {"marker": "Các thang nhiệt độ đặt song song, một con trỏ chạy lên cho thấy cùng một nhiệt độ ở mỗi thang",
           "span": "Ba thang nhiệt độ song song, một đoạn nóng lên mọc dần cho thấy độ lớn khoảng chênh ở mỗi thang"}[mode]
    return fig(cid, "0 0 420 214", alt, b, cap)


# ───────────── thẻ "cho → ?" (dữ kiện dạng đổi thang) ─────────────
def cards(p, rows, cid, alt, cap):
    n = len(rows); H = 20 + n * 54
    b = defs(p)
    for i, (l, r) in enumerate(rows):
        y = 18 + i * 54
        b += R(14, y, 190, 34, "currentColor", 2, "none", 6) + txt(109, y + 22, l, "currentColor", 13, "middle")
        b += arrow(p, "o", 210, y + 17, 242, y + 17, 2.4)
        b += R(248, y, 158, 34, ORG, 2, "none", 6) + txt(327, y + 22, r, ORG, 13, "middle")
    return fig(cid, f"0 0 420 {H}", alt, b, cap)


# ───────────── Dạng 1 · bi thép 120 °C thả vào bể nước 25 °C ─────────────
def d1(kk):
    p = f"d1{kk}"
    if kk == 0:
        return mix(p, kk, "C", "C")
    b = defs(p)
    b += R(40, 100, 340, 90, "currentColor", 2, BLUE, 0, "", 1, .14) + txt(210, 178, "bể nước 25 °C (rất lớn)", BLUE, 13, "middle")
    b += circ(210, 56, 16, RED, 2.4, RED, .55) + txt(236, 52, "bi thép 120 °C", RED, 13, "start")
    b += txt(236, 72, "vừa thả vào bể", "currentColor", 12, "start", "400")
    b += txt(40, 24, "Nhiệt năng truyền: ?", ORG, 13, "start")
    return fig("c1-2", "0 0 420 204", "Viên bi thép nóng 120 độ C sắp thả vào bể nước lớn 25 độ C",
               b, "Dữ kiện: hai nhiệt độ cùng thang Celsius; bể nhiều nhiệt năng hơn nhưng lạnh hơn. " + NOTE)


# ───────────── Dạng 2 · °C ↔ K ─────────────
def d2(kk):
    p = f"d2{kk}"
    if kk == 0:
        return scales(p, ["C", "K"], "marker", 0, 80, "c2-0")
    return cards(p, [("37 °C (thân nhiệt)", "? K"), ("4,22 K (heli sôi)", "? °C"), ("−39 °C (thuỷ ngân)", "? K"), ("−300 °C (đo được?)", "đáng tin không?")],
                 "c2-2", "Bốn nhiệt độ cho ở một thang, cần đổi sang thang còn lại", "Dữ kiện: mỗi thẻ là một giá trị nhiệt độ cần đổi. " + NOTE)


# ───────────── Dạng 3 · °F, K, °C ─────────────
def d3(kk):
    p = f"d3{kk}"
    if kk == 0:
        return scales(p, ["C", "K", "F"], "marker", 0, 60, "c3-0")
    return cards(p, [("374 °F (nướng bánh)", "? °C"), ("98,6 °F (nhiệt kế y tế)", "? °C rồi ? K"), ("293 K (nhiệt độ phòng)", "? °F")],
                 "c3-2", "Ba nhiệt độ cho ở thang Fahrenheit hoặc Kelvin, cần đổi sang thang khác", "Dữ kiện: mỗi thẻ là một giá trị cần đổi. " + NOTE)


# ───────────── Dạng 4 · khoảng chênh 17 → 29 °C ─────────────
def d4(kk):
    p = f"d4{kk}"
    if kk == 0:
        return scales(p, ["C", "K", "F"], "span", 20, 50, "c4-0")
    b = defs(p)
    def y(t): return 190 - (t - 10) * 6
    b += seg(100, y(10), 100, y(35), "currentColor", 2.4)
    for t in (17, 29):
        b += seg(92, y(t), 108, y(t), "currentColor", 2.4) + txt(86, y(t) + 4, f"{t} °C", "currentColor", 13, "end")
    b += arrow(p, "o", 140, y(17), 140, y(29), 2.4) + arrow(p, "o", 140, y(29), 140, y(17), 2.4)
    b += txt(156, (y(17) + y(29)) / 2 + 4, "chênh lệch ?", ORG, 13, "start")
    b += txt(250, 60, "Δ (°C) = ?", "currentColor", 13) + txt(250, 100, "Δ (K) = ?", "currentColor", 13) + txt(250, 140, "Δ (°F) = ?", "currentColor", 13)
    return fig("c4-2", "0 0 420 214", "Nhiệt độ thấp nhất 17 độ C và cao nhất 29 độ C; cần chênh lệch trên ba thang",
               b, "Dữ kiện: hai nhiệt độ cùng thang Celsius; hỏi khoảng chênh trên ba thang. " + NOTE)


# ───────────── Dạng 5 · ba vật, ba thang ─────────────
def d5(kk):
    p = f"d5{kk}"
    if kk == 0:
        return mix(p, kk, "K", "F", 70, 10)
    b = defs(p)
    for cx, name, rd in ((80, "Vật A", "68 °F"), (210, "Vật B", "293 K"), (340, "Vật C", "25 °C")):
        b += txt(cx, 30, name, "currentColor", 13, "middle") + R(cx - 52, 40, 104, 56, "currentColor", 2, "none", 6) + txt(cx, 74, rd, "currentColor", 15, "middle")
        b += txt(cx, 124, "= ? °C" if name != "Vật C" else "đã ở °C", ORG, 13, "middle")
    b += txt(210, 160, "tiếp xúc nhau, không trao đổi nhiệt với bên ngoài", "currentColor", 12, "middle", "400")
    return fig("c5-2", "0 0 420 174", "Ba vật A, B, C với số đọc ở ba thang khác nhau, cho tiếp xúc với nhau",
               b, "Dữ kiện: ba số đọc ở ba thang khác nhau, chưa so thẳng được. " + NOTE)


# ───────────── Dạng 6 · đồ thị tF theo t ─────────────
def gx(t): return 40 + (t + 10) * 2.8
def gy(f): return 186 - f * 0.74

def graph_base(p):
    b = defs(p)
    b += arrow(p, "g", gx(-10), gy(0), 400, gy(0), 2) + arrow(p, "g", gx(0), gy(0), gx(0), 18, 2)
    b += txt(396, gy(0) - 8, "t (°C)", GRN, 12, "end") + txt(gx(0) + 8, 22, TF + " (°F)", GRN, 12, "start")
    for t in (0, 50, 100):
        b += seg(gx(t), gy(0) - 4, gx(t), gy(0) + 4, "currentColor", 1.6) + txt(gx(t), gy(0) + 20, str(t), "currentColor", 12, "middle", "500")
    for f in (32, 122, 212):
        b += seg(gx(0) - 4, gy(f), gx(0) + 4, gy(f), "currentColor", 1.6) + txt(gx(0) - 8, gy(f) + 4, str(f), "currentColor", 12, "end", "500")
    b += circ(gx(0), gy(32), 4, ORG, 2, ORG) + circ(gx(100), gy(212), 4, ORG, 2, ORG)
    b += txt(gx(0) + 10, gy(32) + 16, "nước đá tan", ORG, 12, "start", "500") + txt(gx(100) + 8, gy(212) + 4, "nước sôi", ORG, 12, "start", "500")
    return b

def d6(kk):
    p = f"d6{kk}"
    b = graph_base(p)
    if kk == 0:
        dur = 4.0; m = 11
        ts = [100 * i / (m - 1) for i in range(m)]
        xs_ = [gx(t) for t in ts]; ys_ = [gy(1.8 * t + 32) for t in ts]
        b += (f'<line x1="{xs_[0]:.1f}" y1="{ys_[0]:.1f}" x2="{xs_[0]:.1f}" y2="{ys_[0]:.1f}" stroke="{RED}" stroke-width="2.6">'
              f'{smil("x2", xs_, dur)}{smil("y2", ys_, dur)}</line>')
        b += (f'<circle cx="{xs_[0]:.1f}" cy="{ys_[0]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
              f'{smil("cx", xs_, dur)}{smil("cy", ys_, dur)}</circle>')
        return fig("c6-0", "0 0 420 214", "Đồ thị số đọc Fahrenheit theo số đọc Celsius là một đường thẳng đi qua hai mốc của nước",
                   b, "Mô phỏng: điểm chạy từ mốc nước đá tan đến mốc nước sôi, vẽ dần đường thẳng số đọc °F theo số đọc °C (tính từ công thức đổi). Chạy 4 s.")
    b += seg(gx(0), gy(32), gx(100), gy(212), RED, 2.6)
    b += txt(gx(56), gy(78), TF + " = 1,8t + 32", RED, 13, "start")
    return fig("c6-2", "0 0 420 214", "Đồ thị số đọc Fahrenheit theo số đọc Celsius, đường thẳng qua hai mốc của nước",
               b, "Dữ kiện: hai thang liên hệ bậc nhất; mỗi nhiệt độ có một số đọc ở mỗi thang. " + NOTE)
