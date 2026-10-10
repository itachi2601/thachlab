"""Hình cho bài tập mẫu Bài 15 "Định luật 2 Newton" (Vật lí 10), lesson_id 60.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Chuyển động trong mô phỏng tính thật từ công thức (x = ½at², hoặc v₀t + ½at²), KHÔNG vẽ gia tốc, KHÔNG vẽ hợp lực đáp án,
KHÔNG ghi kết quả lên hình. Vectơ lực dùng vec_luc: độ dài = k·F với cùng k cho mọi lực trong một hình (đầu mũi tên chữ V 30°)."""
import math, os, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


def rich(s, size=13):
    """`F_ms` → F với chỉ số dưới ms."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out


def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)


def rect(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def line_g(x0, x1, y):
    return seg(x0, y, x1, y, "currentColor", 2)


def cart(xl, gy, w=56, load=False, load_txt=""):
    """Xe đẩy nhìn nghiêng: thân từ xl đến xl+w, bánh chạm nền y=gy. load=True: thêm kiện hàng trên xe."""
    s = rect(xl, gy - 26, w, 20, "currentColor", 2.2, rx=3)
    for cx in (xl + 12, xl + w - 12):
        s += f'<circle cx="{cx:.1f}" cy="{gy - 5:.1f}" r="5" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    if load:
        s += rect(xl + 8, gy - 52, w - 16, 26, GREY, 2, rx=2) + lbl(xl + w / 2, gy - 34, load_txt, GREY, 12, "middle", "700")
    return s


def crate(xl, gy, w=60, h=40, label=""):
    return rect(xl, gy - h, w, h, "currentColor", 2.2, rx=2) + lbl(xl + w / 2, gy - h / 2 + 4, label, "currentColor", 13, "middle", "700")


def car(xf, gy, w=64, c="currentColor"):
    """Ô tô nhìn nghiêng, mũi quay phải: mũi tại xf, bánh chạm đường y=gy."""
    s = f'<rect x="{xf - w:.1f}" y="{gy - 19:.1f}" width="{w}" height="13" rx="3" fill="none" stroke="{c}" stroke-width="2.2"/>'
    s += f'<path d="M{xf - w * 0.62:.1f},{gy - 19:.1f} l5,-8 h{w * 0.28:.1f} l5,8" fill="none" stroke="{c}" stroke-width="2.2"/>'
    for cx in (xf - w + 11, xf - 11):
        s += f'<circle cx="{cx:.1f}" cy="{gy - 4.5:.1f}" r="4.5" fill="none" stroke="{c}" stroke-width="2.2"/>'
    return s


def move_g(content, dxs, dur):
    """Nhóm chạy một lần khi bấm: tịnh tiến theo dxs (px, lấy mẫu cách đều thời gian), nội suy tuyến tính."""
    vals = ";".join(f"{d:.2f} 0" for d in dxs)
    return (f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>{content}</g>')


def track(pos, T, dxmax, n=48):
    """pos(t): quãng đường theo công thức; trả dx (px) tại n+1 mẫu cách đều thời gian, dx(T) = dxmax."""
    end = pos(T)
    return [dxmax * pos(T * i / n) / end for i in range(n + 1)]


def force(c, x, y, dx, dy, F, k, label, lx, ly, anchor="start"):
    svg, _ = vec_luc(c, x, y, dx, dy, F, k, 3)
    return svg + txt(lx, ly, label, {"r": RED, "o": ORG, "b": BLUE, "g": GRN}[c], 13, anchor)


# ───────────── Dạng 1 · xe điều khiển từ xa 250 g, F = 0,8 N, bàn nhẵn ─────────────
def d1(kk):
    gy, xl, k = 110, 60, 60                                   # k = 60 px mỗi N
    a, T = 3.2, 1.0                                           # chạy 1,0 s theo công thức x = ½at²
    b = line_g(20, 405, gy) + txt(405, gy + 20, "mặt bàn nhẵn", "currentColor", 12, "end", "400")
    inner = cart(xl, gy) + force("r", xl + 56, gy - 16, 1, 0, 0.8, k, "F = 0,8 N", xl + 62, gy - 26)
    b += txt(14, 22, "m = 250 g") + txt(406, 22, "a = ?", ORG, 13, "end")
    if kk == 0:
        dxs = track(lambda t: 0.5 * a * t * t, T, 170)
        b += move_g(inner, dxs, 2 * T)
        return fig("d1-0", "0 0 420 140", "Xe điều khiển từ xa 250 gam đứng yên trên mặt bàn nhẵn, bị lực kéo ngang 0,8 N làm chuyển động nhanh dần", b,
                   "Mô phỏng: xe xuất phát từ nghỉ (thời gian phát chậm hơn thật; bấm Chạy mô phỏng). Vị trí tính theo công thức. Hình không ghi kết quả.")
    b += inner
    return fig("d1-2", "0 0 420 140", "Xe điều khiển từ xa 250 gam chịu lực kéo ngang 0,8 N trên mặt bàn nhẵn", b,
               "Dữ kiện: khối lượng ở đơn vị gam, lực kéo ngang 0,8 N, bàn nhẵn nên không có ma sát. " + NOTE)


# ───────────── Dạng 2 · thùng 35 kg, F = 120 N, F_ms = 50 N ─────────────
def d2(kk):
    gy, xl, k = 120, 80, 0.6
    a, T = 2.0, 3.0
    b = line_g(20, 405, gy) + txt(405, gy + 20, "sàn kho", "currentColor", 12, "end", "400")
    inner = (crate(xl, gy, 60, 42, "35 kg")
             + force("r", xl + 60, gy - 28, 1, 0, 120, k, "F = 120 N", xl + 62, gy - 38)
             + force("o", xl, gy - 10, -1, 0, 50, k, "F_ms = 50 N", xl + 2, gy - 52, "end"))
    b += txt(406, 22, "a = ?  hướng?", ORG, 13, "end")
    if kk == 0:
        dxs = track(lambda t: 0.5 * a * t * t, T, 120)
        b += move_g(inner, dxs, T)
        return fig("d2-0", "0 0 420 160", "Thùng hàng 35 kg trượt trên sàn kho, bị kéo bằng dây ngang 120 N, lực ma sát 50 N cản lại", b,
                   "Mô phỏng: thùng bắt đầu trượt từ nghỉ (bấm Chạy mô phỏng). Hai lực vẽ cùng tỉ lệ độ dài. Hình không ghi kết quả.")
    b += inner
    b += txt(14, 22, "chiều chuyển động →", "currentColor", 12, "start", "400")
    return fig("d2-2", "0 0 420 160", "Thùng 35 kg chịu lực kéo ngang 120 N về bên phải và lực ma sát 50 N về bên trái", b,
               "Dữ kiện: hai lực nằm ngang ngược chiều, vẽ cùng tỉ lệ độ dài. Hai lực thẳng đứng không vẽ. " + NOTE)


# ───────────── Dạng 3 · xe đẩy rỗng (15 N, 0,5 m/s²) và xe chở thêm hàng 40 kg (28 N) ─────────────
def d3(kk):
    g1, g2, xl, k = 70, 166, 40, 3.0
    a1, T = 0.5, 6.0
    b = line_g(20, 405, g1) + line_g(20, 405, g2)
    b += txt(14, 16, "xe rỗng:  a_1 = 0,5 m/s²", "currentColor", 12) + txt(14, 100, "xe chở hàng 40 kg:  a_2 = ?", ORG, 12)
    top = cart(xl, g1) + force("r", xl + 56, g1 - 16, 1, 0, 15, k, "F_1 = 15 N", xl + 62, g1 - 26)
    bot = cart(xl, g2, 56, True, "40 kg") + force("r", xl + 56, g2 - 16, 1, 0, 28, k, "F_2 = 28 N", xl + 62, g2 - 26)
    if kk == 0:
        dxs = track(lambda t: 0.5 * a1 * t * t, T, 170)
        b += move_g(top, dxs, T) + bot
        return fig("d3-0", "0 0 420 190", "Xe đẩy siêu thị rỗng đang tăng tốc với gia tốc 0,5 m/s² dưới lực đẩy 15 N; bên dưới là xe đã chất hàng 40 kg chịu lực đẩy 28 N", b,
                   "Mô phỏng: chỉ xe rỗng (dữ kiện của đề) chuyển động (bấm Chạy mô phỏng). Xe chở hàng là trường hợp cần tìm nên đứng yên. Hai lực vẽ cùng tỉ lệ độ dài.")
    b += top + bot
    return fig("d3-2", "0 0 420 190", "Hai trường hợp của xe đẩy: xe rỗng với lực đẩy 15 N và gia tốc 0,5 m/s², xe chở hàng 40 kg với lực đẩy 28 N", b,
               "Dữ kiện: hai lực đẩy vẽ cùng tỉ lệ độ dài. Hai trường hợp là cùng một xe. " + NOTE)


# ───────────── Dạng 4 · thùng 12 kg, F = 54 N, F_ms = 18 N, t = 6 s ─────────────
def d4(kk):
    gy, xl, k = 120, 80, 1.0
    a, T = 3.0, 6.0
    b = line_g(20, 405, gy) + txt(405, gy + 20, "sàn nằm ngang", "currentColor", 12, "end", "400")
    inner = (crate(xl, gy, 60, 42, "12 kg")
             + force("r", xl + 60, gy - 28, 1, 0, 54, k, "F = 54 N", xl + 62, gy - 38)
             + force("o", xl, gy - 10, -1, 0, 18, k, "F_ms = 18 N", xl + 2, gy - 52, "end"))
    b += txt(14, 22, "bắt đầu từ nghỉ", "currentColor", 12, "start", "400") + txt(406, 22, "sau 6 s:  v = ?  s = ?", ORG, 13, "end")
    if kk == 0:
        dxs = track(lambda t: 0.5 * a * t * t, T, 190)
        b += move_g(inner, dxs, T)
        return fig("d4-0", "0 0 420 160", "Thùng hàng 12 kg đứng yên trên sàn ngang bị kéo bằng lực 54 N, lực ma sát 18 N, bắt đầu trượt", b,
                   "Mô phỏng: thùng bắt đầu trượt từ nghỉ rồi chạy 6 s đúng thời gian thật (bấm Chạy mô phỏng). Vị trí tính theo công thức. Hình không ghi kết quả.")
    b += inner
    b += seg(xl + 30, gy + 14, xl + 30 + 190, gy + 14, GRN, 2, "5 4") + txt(xl + 30 + 95, gy + 32, "quãng đường s sau 6 s", GRN, 12, "middle")
    return fig("d4-2", "0 0 420 160", "Thùng 12 kg chịu lực kéo 54 N và lực ma sát 18 N ngược chiều; sau 6 s cần tìm vận tốc và quãng đường", b,
               "Dữ kiện: hai lực nằm ngang vẽ cùng tỉ lệ độ dài; nét đứt xanh chỉ quãng đường cần tìm (chưa biết độ dài). " + NOTE)


# ───────────── Dạng 5 · ô tô 1,4 tấn, 108 km/h, phanh dừng sau 90 m ─────────────
def d5(kk):
    gy, xf0, px = 100, 100, 3.0                                # 3 px ứng 1 m
    s_end = 90 * px
    b = line_g(20, 405, gy) + txt(14, 22, "m = 1,4 tấn   v₀ = 108 km/h", "currentColor", 13) + txt(406, 22, "lực hãm = ?", ORG, 13, "end")
    b += seg(xf0, gy, xf0, gy + 30, "currentColor", 1.4, "3 3") + seg(xf0 + s_end, gy, xf0 + s_end, gy + 30, "currentColor", 1.4, "3 3")
    b += dim("", "b", xf0, gy + 24, xf0 + s_end, gy + 24, "vết phanh 90 m", xf0 + s_end / 2 - 56, gy + 46)
    if kk == 0:
        a, v0 = -5.0, 30.0
        T = 6.0
        dxs = track(lambda t: v0 * t + 0.5 * a * t * t, T, s_end)
        b += move_g(car(xf0, gy, 64), dxs, 9)
        return fig("d5-0", "0 0 420 156", "Ô tô 1,4 tấn đang chạy 108 km/h phanh gấp, để lại vết phanh dài 90 m rồi dừng; ô tô chậm dần rồi đứng yên", b,
                   "Mô phỏng: ô tô phanh đều tới khi dừng (thời gian phát không ứng với thời gian thật; bấm Chạy mô phỏng); tỉ lệ 3 px ứng 1 m. Vị trí tính theo công thức. Hình không ghi kết quả.")
    b += car(xf0, gy, 64) + car(xf0 + s_end, gy, 64, GRN)
    v_svg = arrow("", "b", xf0 + 4, gy - 38, xf0 + 4 + 2 * 30, gy - 38, 3)           # độ dài tỉ lệ vận tốc: 2 px mỗi m/s
    b += v_svg + txt(xf0 + 4, gy - 46, "v₀", BLUE, 13) + txt(xf0 + s_end - 16, gy - 28, "v = 0", GRN, 13)
    return fig("d5-2", "0 0 420 156", "Ô tô lúc bắt đầu phanh với vận tốc 108 km/h và lúc dừng sau vết phanh 90 m", b,
               "Dữ kiện: vị trí bắt đầu phanh (đen) và vị trí dừng (xanh lá) cách nhau 90 m; vận tốc đầu vẽ theo tỉ lệ 2 px mỗi m/s. " + NOTE)


# ───────────── Dạng 6 · ô tô 1,8 tấn chạy đều 90 km/h, F_k = 900 N; tắt máy tại O ─────────────
def d6(kk):
    gy, xf0 = 100, 100
    v0, a = 25.0, -0.5
    T = 50.0
    sx = 0.44                                                  # px mỗi m (hình không ghi tỉ lệ)
    s_end = v0 * T + 0.5 * a * T * T
    b = line_g(20, 405, gy) + txt(14, 22, "m = 1,8 tấn   v₀ = 90 km/h (chạy đều)", "currentColor", 13) + txt(406, 22, "t = ?  s = ?", ORG, 13, "end")
    b += seg(xf0, gy, xf0, gy + 30, "currentColor", 1.4, "3 3") + txt(xf0, gy + 46, "O: tắt máy", "currentColor", 12, "middle")
    if kk == 0:
        dxs = track(lambda t: v0 * t + 0.5 * a * t * t, T, s_end * sx)
        b += move_g(car(xf0, gy, 64), dxs, 10)
        return fig("d6-0", "0 0 420 156", "Ô tô 1,8 tấn tắt máy tại điểm O khi đang chạy đều 90 km/h, chạy chậm dần rồi dừng", b,
                   "Mô phỏng: từ lúc tắt máy tại O đến khi xe dừng (thời gian phát không ứng với thời gian thật; bấm Chạy mô phỏng). Vị trí tính theo công thức. Hình không ghi kết quả, không vẽ tỉ lệ khoảng cách.")
    b += car(xf0, gy, 64)
    b += force("r", xf0, gy - 14, 1, 0, 900, 0.06, "F_k = 900 N", xf0 + 4, gy - 28)
    b += arrow("", "b", xf0 - 60, gy - 58, xf0 - 60 + 2 * v0, gy - 58, 3) + txt(xf0 - 60, gy - 64, "v₀", BLUE, 13)
    return fig("d6-2", "0 0 420 156", "Ô tô chạy đều với vận tốc 90 km/h và lực kéo động cơ 900 N trước khi tắt máy tại O", b,
               "Dữ kiện: lực kéo của động cơ và vận tốc vẽ theo tỉ lệ riêng của từng loại; lực cản không vẽ vì chưa biết. " + NOTE)


BUILD = [d1, d2, d3, d4, d5, d6]
