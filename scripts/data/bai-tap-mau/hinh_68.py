"""Hình cho bài tập mẫu Bài 23 "Năng lượng. Công cơ học" (Vật lí 10), lesson_id 68.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Quy tắc vectơ lực (thầy chốt 10/10/2026): đầu mũi tên chữ V 30°, độ dài = k·F với MỘT hệ số k cho cả hình (vec_luc), không marker.
KHÔNG vẽ vectơ nào là đáp án (lực cản, N, F_ms, công, độ cao h) — chỉ ghi "?" ở đại lượng cần tìm.
Mô phỏng: D1 hai cột năng lượng tăng đều (cột thứ ba chưa vẽ); D2 xe chạy đều 12 m; D3 ba tình huống chạy song song;
D4 thùng kéo đều lên 6,0 m rồi trượt xuống (a = g·sinθ − F_ms/m tính thật); D5 thùng nhanh dần từ nghỉ (a tính thật từ F, μ, m)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import vec_luc, chevron, field_line

GREY = "#94a3b8"


def rad(a):
    return math.radians(a)


def an(attr, vals, dur, nd=1, key=None):
    kt = f' keyTimes="{";".join(f"{k:.4f}" for k in key)}"' if key else ""
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}"{kt} dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def tr_anim(pairs, dur, key=None):
    """Tịnh tiến nhóm theo các mẫu (dx, dy). key = keyTimes (0..1) nếu mẫu không cách đều thời gian."""
    vals = ";".join(f"{dx:.1f} {dy:.1f}" for dx, dy in pairs)
    kt = f' keyTimes="{";".join(f"{k:.4f}" for k in key)}"' if key else ""
    return (f'<animateTransform attributeName="transform" type="translate" values="{vals}"{kt} dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: base_sb tail."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


def rect(x, y, w, h, c="currentColor", sw=2.4, fill="none", op=1):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{c}" stroke-width="{sw}" opacity="{op}"/>'


# ───────────── Dạng 1: máy xay sinh tố — 300 J/s vào, 240 J/s thành động năng ─────────────
def d1(kk):
    b = ""
    if kk == 0:
        base, H, W = 190, 130, 70
        b += seg(20, base, 400, base, "currentColor", 2)
        T = 4.0                                     # 4 s đầu: điện năng 300·4 = 1200 J, động năng 240·4 = 960 J
        for x, h, c in ((40, H, BLUE), (160, H * 960 / 1200, ORG)):
            b += (f'<rect x="{x}" y="{base}" width="{W}" height="0" fill="{c}" fill-opacity=".35" stroke="{c}" stroke-width="2">'
                  + an("y", [base, base - h], T) + an("height", [0, h], T) + "</rect>")
        b += (rect(280, base - 26, W, 26, GREY, 1.6) .replace('fill="none"', 'fill="none" stroke-dasharray="5 4"')
              + lbl(280 + W / 2, base - 5, "?", GREY, 20, "middle", "700"))
        for x, l1, l2, c in ((40, "Điện năng", "nhận vào", BLUE), (160, "Động năng", "lưỡi dao, hoa quả", ORG), (280, "Nhiệt năng", "+ âm thanh", GREY)):
            b += lbl(x + W / 2, base + 18, l1, c, 13, "middle", "700") + lbl(x + W / 2, base + 35, l2, c, 12, "middle", "600")
        b += lbl(210, 30, "4 s đầu sau khi bật máy", "currentColor", 13, "middle", "700")
        return fig("d1-0", "0 0 420 232", "Hai cột năng lượng tăng dần: điện năng nhận vào và động năng của lưỡi dao; cột nhiệt năng và âm thanh chưa vẽ", b,
                   "Mô phỏng đúng thời gian thật (4 s): cột điện năng tăng 300 J mỗi giây, cột động năng tăng 240 J mỗi giây, cùng một thang chiều cao. Cột nhiệt năng và âm thanh chưa vẽ.")
    b += rect(165, 70, 90, 70, "currentColor", 2.4).replace('fill="none"', 'fill="none" rx="8"')
    b += lbl(210, 100, "Máy xay", "currentColor", 13, "middle", "700") + lbl(210, 119, "sinh tố", "currentColor", 13, "middle", "700")
    b += arrow("", "b", 24, 105, 165, 105, 3) + lbl(24, 90, "Điện năng vào", BLUE, 13, "start", "700") + lbl(24, 130, "300 J mỗi giây", BLUE, 12, "start", "600")
    b += arrow("", "o", 255, 90, 310, 56, 3) + lbl(316, 52, "Động năng", ORG, 13, "start", "700") + lbl(316, 69, "240 J mỗi giây", ORG, 12, "start", "600")
    b += arrow("", "r", 255, 122, 310, 158, 3) + lbl(316, 156, "Nhiệt năng", RED, 13, "start", "700") + lbl(316, 173, "+ âm thanh", RED, 13, "start", "700") + lbl(316, 190, "? J mỗi giây", RED, 12, "start", "600")
    return fig("d1-2", "0 0 420 204", "Sơ đồ chuyển hoá: điện năng vào máy xay, ra là động năng và phần nhiệt năng cộng âm thanh chưa biết", b,
               "Dữ kiện: số liệu của một giây. Mũi tên chỉ hướng chuyển hoá năng lượng, độ dài mũi tên không biểu diễn độ lớn.")


# ───────────── Dạng 2: xe chở hàng đi đều 12 m, F = 25 N ─────────────
D2_X0, D2_PX = 60.0, 25.0          # vị trí tâm xe ở s = 0; px mỗi mét


def cart(cx, gy):
    """Xe chở hàng nhìn ngang, tâm cx, mặt sàn gy; tay đẩy ở phía sau (bên trái). Trả (svg, điểm đặt lực)."""
    s = rect(cx - 24, gy - 46, 48, 26, "currentColor", 2.2)
    s += seg(cx - 24, gy - 46, cx - 36, gy - 64, "currentColor", 2.2)
    for wx in (cx - 14, cx + 14):
        s += f'<circle cx="{wx:.1f}" cy="{gy - 8:.1f}" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    s += f'<circle cx="{cx - 36:.1f}" cy="{gy - 64:.1f}" r="4" fill="none" stroke="currentColor" stroke-width="2"/>'
    return s, (cx - 36, gy - 64)


def d2(kk):
    gy = 140; k = 1.2; F = 25.0
    b = ground(gy, 16, 410)
    c0, hand = cart(D2_X0, gy)
    fv, _ = vec_luc("o", hand[0] + 5, hand[1], 1, 0, F, k)
    if kk == 0:
        yr = gy + 30
        b += seg(D2_X0, yr, D2_X0 + 12 * D2_PX, yr, "currentColor", 1.6)
        for m in range(0, 13, 2):
            x = D2_X0 + m * D2_PX
            b += seg(x, yr - 5, x, yr + 5, "currentColor", 1.6) + lbl(x, yr + 22, str(m), "currentColor", 12, "middle", "600")
        b += lbl(D2_X0 + 12 * D2_PX + 22, yr + 22, "m", "currentColor", 12, "start", "600")
        grp = c0 + fv + lbl(hand[0], hand[1] - 14, "F = 25 N", ORG, 13, "start", "700")
        dur = 6.0                                    # 12 m ở 2,0 m/s (tốc độ minh hoạ)
        b += f'<g>{grp}{tr_anim([(0, 0), (12 * D2_PX, 0)], dur)}</g>'
        b += lbl(410, 20, "Lực cản của sàn: ?", GREY, 13, "end", "700") + lbl(410, 38, "Xe chuyển động thẳng đều", GREY, 12, "end", "600")
        return fig("d2-0", "0 0 420 204", "Xe chở hàng được đẩy đi thẳng đều 12 mét trên sàn nằm ngang, lực đẩy 25 niutơn hướng theo chiều chuyển động", b,
                   "Mô phỏng: xe chạy đều dọc thước 12 m với tốc độ minh hoạ 2,0 m/s (đề không cho tốc độ), mất 6 s; lực đẩy vẽ 1 N ứng với 1,2 px. Lực cản chưa vẽ.")
    xe = D2_X0 + 12 * D2_PX
    ghost, _ = cart(xe, gy)
    b += f'<g opacity=".3">{ghost}</g>' + c0 + fv + lbl(hand[0], hand[1] - 14, "F = 25 N", ORG, 13, "start", "700")
    b += seg(D2_X0, gy + 4, D2_X0, gy + 36, GREY, 1.2, "4 4", .8) + seg(xe, gy + 4, xe, gy + 36, GREY, 1.2, "4 4", .8)
    b += dim("", "g", D2_X0, gy + 30, xe, gy + 30, "s = 12 m", (D2_X0 + xe) / 2, gy + 52, "middle")
    b += lbl(D2_X0 - 40, 26, "Lực cản của sàn: ?", GREY, 13, "start", "700")
    return fig("d2-2", "0 0 420 204", "Xe chở hàng ở vị trí đầu và cuối đoạn đường 12 mét, lực đẩy F cùng hướng chuyển động", b,
               "Dữ kiện: xe ở vị trí đầu (nét đậm) và cuối đoạn đường (nét mờ); lực đẩy vẽ 1 N ứng với 1,2 px. Lực cản chưa vẽ.")


# ───────────── Dạng 3: F = 70 N, s = 8,0 m, α = 60°, vuông góc, 120° ─────────────
def d3(kk):
    k = 0.6; F = 70.0
    if kk == 0:
        gys = [84, 168, 252]; cx0 = 130.0; px = 30.0; s = 8.0
        b = lbl(8, 20, "Cả ba tình huống: F = 70 N", ORG, 13, "start", "700")
        b += seg(cx0, 36, cx0, 268, GREY, 1.2, "4 4", .6) + seg(cx0 + s * px, 36, cx0 + s * px, 268, GREY, 1.2, "4 4", .6)
        for gy, name, a in zip(gys, ("a) α = 60°", "b) thẳng đứng", "c) α = 120°"), (60, 90, 120)):
            b += seg(110, gy, 412, gy, "currentColor", 2) + lbl(8, gy - 4, name, "currentColor", 12, "start", "700")
            box = rect(cx0 - 20, gy - 26, 40, 26, "currentColor", 2.2)
            v, _ = vec_luc("o", cx0, gy - 13, math.cos(rad(a)), -math.sin(rad(a)), F, k)
            b += f'<g>{box}{v}{tr_anim([(0, 0), (s * px, 0)], 4.0)}</g>'
        b += dim("", "g", cx0, 280, cx0 + s * px, 280, "s = 8,0 m", cx0 + s * px / 2, 298, "middle")
        return fig("d3-0", "0 0 420 304", "Ba thùng cùng trượt 8,0 mét trên sàn nằm ngang, mỗi thùng chịu lực 70 niutơn theo một hướng khác nhau", b,
                   "Mô phỏng: ba thùng cùng trượt 8,0 m trong 4 s (tốc độ minh hoạ 2,0 m/s). Lực vẽ cùng tỉ lệ ở cả ba hàng (1 N ứng với 0,6 px).")
    gy = 130; c = (170.0, gy - 13)
    b = seg(40, gy, 400, gy, "currentColor", 2) + rect(c[0] - 20, gy - 26, 40, 26, "currentColor", 2.2)
    kk2 = 0.9
    sv, tip = vec_luc("o", c[0], c[1], math.cos(rad(60)), -math.sin(rad(60)), F, kk2)
    b += sv + arrow("", "g", c[0], c[1], c[0] + 110, c[1], 3) + lbl(c[0] + 116, c[1] + 5, "d = 8,0 m", GRN, 13, "start", "700")
    b += arc(c[0], c[1], 34, 0, 60, RED) + lbl(c[0] + 42, c[1] - 10, "α = 60°", RED, 13, "start", "700")
    b += lbl(tip[0] + 8, tip[1] - 2, "F = 70 N", ORG, 13, "start", "700")
    return fig("d3-2", "0 0 420 160", "Lực F hợp với độ dịch chuyển d góc 60 độ khi thùng trượt trên sàn nằm ngang", b,
               "Dữ kiện: hình vẽ minh hoạ tình huống a (α = 60°). Lực vẽ 1 N ứng với 0,9 px; vectơ d chỉ hướng chuyển động, không theo tỉ lệ.")


# ───────────── Dạng 4: thùng 40 kg, dốc 30°, s = 6,0 m, F_ms = 40 N ─────────────
D4_B = (36.0, 225.0); D4_TH = 30; D4_PX = 40.0            # 40 px mỗi mét dọc dốc


def sp(s_px, off=0.0):
    """Điểm cách chân dốc B một đoạn s_px dọc mặt dốc, cộng độ lệch off theo pháp tuyến hướng lên-trái (ra ngoài dốc)."""
    c, s = math.cos(rad(D4_TH)), math.sin(rad(D4_TH))
    return (D4_B[0] + s_px * c - off * s, D4_B[1] - s_px * s - off * c)


def d4_geometry():
    T = sp(280)
    C = (T[0], D4_B[1])
    b = seg(16, D4_B[1], 340, D4_B[1], "currentColor", 2) + seg(D4_B[0], D4_B[1], T[0], T[1], "currentColor", 2.8)
    b += arc(D4_B[0], D4_B[1], 52, 0, D4_TH, RED) + lbl(D4_B[0] + 60, D4_B[1] - 6, "30°", RED, 13, "start", "700")
    return b, T, C


def d4(kk):
    b, T, C = d4_geometry()
    b += ts(410, 28, "F", "ms", " = 40 N", ORG, 13, "end") + lbl(410, 48, "m = 40 kg", "currentColor", 13, "end", "700")
    if kk == 0:
        s0 = 20.0
        a = 5.0 - 40.0 / 40.0                                   # g·sinθ − F_ms/m = 4 m/s² (m/s²)
        tdown = math.sqrt(2 * 6.0 / a)
        times, pos = [], []                                     # pos = vị trí (m) dọc dốc tính từ điểm đầu
        for i in range(25):
            times.append(0.25 * i); pos.append(1.0 * 0.25 * i)  # kéo đều lên, 1,0 m/s
        times.append(6.5); pos.append(6.0)                      # dừng ở đỉnh 0,5 s
        for j in range(1, 17):
            tau = 0.1 * j; times.append(6.5 + tau); pos.append(6.0 - 0.5 * a * tau * tau)
        times.append(6.5 + tdown); pos.append(0.0)
        assert abs(pos[-2] - (6.0 - 0.5 * a * 1.6 ** 2)) < 1e-9 and pos[-2] > 0.4
        dur = times[-1]
        key = [t / dur for t in times]; key[0] = 0.0; key[-1] = 1.0
        pairs = [(m * D4_PX * math.cos(rad(D4_TH)), -m * D4_PX * math.sin(rad(D4_TH))) for m in pos]
        P0 = sp(s0)
        crate = f'<g transform="translate({P0[0]:.1f} {P0[1]:.1f}) rotate({-D4_TH})">{rect(-18, -24, 36, 24, "currentColor", 2.2)}</g>'
        b += f'<g>{crate}{tr_anim(pairs, dur, key)}</g>'
        A1, A2 = sp(s0, 40), sp(s0 + 6 * D4_PX, 40)
        b += dim("", "b", A1[0], A1[1], A2[0], A2[1], "6,0 m", sp(s0 + 3 * D4_PX, 58)[0] - 10, sp(s0 + 3 * D4_PX, 58)[1], "start")
        return fig("d4-0", "0 0 420 250", "Thùng 40 kg được kéo đều lên 6,0 mét dọc mặt dốc nghiêng 30 độ, dừng ở đỉnh rồi trượt xuống về chỗ cũ", b,
                   "Mô phỏng đúng thời gian thật (khoảng 8,2 s): kéo đều lên với tốc độ minh hoạ 1,0 m/s, dừng 0,5 s ở đỉnh, rồi buông cho thùng trượt xuống về chỗ cũ.")
    sc = 150.0
    Pc = sp(sc, 12)
    crate = f'<g transform="translate({sp(sc)[0]:.1f} {sp(sc)[1]:.1f}) rotate({-D4_TH})">{rect(-18, -24, 36, 24, "currentColor", 2.2)}</g>'
    b += crate
    sv, tip = vec_luc("r", Pc[0], Pc[1], 0, 1, 400.0, 0.18)
    b += sv + lbl(tip[0] + 8, tip[1] - 2, "P = mg", RED, 13, "start", "700")
    b += arrow("", "g", Pc[0], Pc[1], sp(sc + 70, 12)[0], sp(sc + 70, 12)[1], 3) + lbl(sp(sc + 70, 12)[0] + 6, sp(sc + 70, 12)[1] - 8, "d", GRN, 13, "start", "700")
    b += seg(C[0], C[1], T[0], T[1], GREY, 1.3, "5 4", .9) + lbl(C[0] + 8, (C[1] + T[1]) / 2 + 4, "h = ?", ORG, 13, "start", "700")
    A1, A2 = sp(20, 34), sp(260, 34)
    b += dim("", "b", A1[0], A1[1], A2[0], A2[1], "6,0 m", sp(140, 52)[0] - 10, sp(140, 52)[1], "start")
    return fig("d4-2", "0 0 420 250", "Thùng trên mặt dốc nghiêng 30 độ: trọng lực P thẳng đứng xuống, độ dịch chuyển d dọc dốc hướng lên, độ cao h chưa biết", b,
               "Dữ kiện: trọng lực vẽ 1 N ứng với 0,18 px; lực ma sát (nhỏ hơn nhiều) không vẽ cùng tỉ lệ nên chỉ ghi trị số trên hình; vectơ d chỉ hướng chuyển động.")


# ───────────── Dạng 5: thùng 25 kg, F = 100 N chếch lên 30°, μ = 0,20, s = 12 m ─────────────
D5_PX = 20.0


def d5_crate(cx, gy):
    """Thùng + dây chếch lên 30° buộc ở mép trước. Trả (svg, điểm buộc, điểm tay)."""
    att = (cx + 25, gy - 20)
    hand = (att[0] + 90 * math.cos(rad(30)), att[1] - 90 * math.sin(rad(30)))
    s = rect(cx - 25, gy - 32, 50, 32, "currentColor", 2.4) + seg(att[0], att[1], hand[0], hand[1], "currentColor", 1.4, "", .8)
    s += f'<circle cx="{hand[0]:.1f}" cy="{hand[1]:.1f}" r="5" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    return s, att, hand


def d5(kk):
    gy = 140; k = 0.6; F = 100.0; m = 25.0; mu = 0.20; s = 12.0
    al = math.radians(30)
    a = (F * math.cos(al) - mu * (m * 10 - F * math.sin(al))) / m
    T = math.sqrt(2 * s / a)
    if kk == 0:
        x0 = 50.0
        b = ground(gy, 16, 410)
        yr = gy + 28
        b += seg(x0, yr, x0 + s * D5_PX, yr, "currentColor", 1.6)
        for mm in range(0, 13, 2):
            x = x0 + mm * D5_PX
            b += seg(x, yr - 5, x, yr + 5, "currentColor", 1.6) + lbl(x, yr + 20, str(mm), "currentColor", 12, "middle", "600")
        b += lbl(x0 + s * D5_PX + 18, yr + 20, "m", "currentColor", 12, "start", "600")
        c0, att, hand = d5_crate(x0, gy)
        v, _ = vec_luc("o", att[0], att[1], math.cos(al), -math.sin(al), F, k)
        n = 30
        pairs = [(0.5 * a * (T * i / n) ** 2 * D5_PX, 0) for i in range(n + 1)]
        assert abs(pairs[-1][0] - s * D5_PX) < 1e-6
        b += f'<g>{c0}{v}{lbl(x0, gy - 12, "25 kg", "currentColor", 12, "middle", "600")}{tr_anim(pairs, T)}</g>'
        b += lbl(10, 22, "Lực kéo F = 100 N, dây chếch lên", ORG, 13, "start", "700") + lbl(10, 42, "Hệ số ma sát trượt μ = 0,20", "currentColor", 13, "start", "700")
        return fig("d5-0", "0 0 420 190", "Thùng 25 kg được kéo bằng dây chếch lên 30 độ trên sàn nằm ngang, đi thẳng 12 mét", b,
                   f"Mô phỏng đúng thời gian thật (khoảng {str(round(T,1)).replace('.',',')} s): thùng bắt đầu từ nghỉ rồi nhanh dần; lực kéo vẽ 1 N ứng với 0,6 px. Các lực khác chưa vẽ.")
    gy = 130; cx = 110.0
    b = ground(gy, 16, 410)
    c0, att, hand = d5_crate(cx, gy)
    v, _ = vec_luc("o", att[0], att[1], math.cos(al), -math.sin(al), F, k)
    b += f'<g opacity=".3">{rect(cx + s * D5_PX - 25, gy - 32, 50, 32, "currentColor", 2.4)}</g>' + c0 + v
    b += seg(att[0], att[1], att[0] + 110, att[1], GREY, 1.2, "4 4", .8) + arc(att[0], att[1], 40, 0, 30, RED) + lbl(att[0] + 66, att[1] - 6, "α = 30°", RED, 13, "start", "700")
    b += lbl(hand[0] + 10, hand[1] - 2, "F = 100 N", ORG, 13, "start", "700") + lbl(cx, gy - 12, "25 kg", "currentColor", 12, "middle", "600")
    b += seg(cx, gy + 4, cx, gy + 34, GREY, 1.2, "4 4", .8) + seg(cx + s * D5_PX, gy + 4, cx + s * D5_PX, gy + 34, GREY, 1.2, "4 4", .8)
    b += dim("", "g", cx, gy + 28, cx + s * D5_PX, gy + 28, "s = 12 m", cx + s * D5_PX / 2, gy + 50, "middle")
    b += lbl(10, 22, "μ = 0,20", "currentColor", 13, "start", "700")
    return fig("d5-2", "0 0 420 190", "Thùng 25 kg ở vị trí đầu và cuối đoạn đường 12 mét, dây kéo chếch lên hợp với phương ngang góc 30 độ", b,
               "Dữ kiện: thùng ở vị trí đầu (nét đậm) và cuối (nét mờ); lực kéo vẽ 1 N ứng với 0,6 px. Trọng lực, phản lực, ma sát chưa vẽ.")


BUILD = [d1, d2, d3, d4, d5]
