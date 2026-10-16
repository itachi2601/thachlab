"""Bài tập mẫu CĐ16 "Truyền nhiệt và sự nở vì nhiệt" (lesson 164) — Dạng 1–3. Module được build-hinh-164.py import.
Dàn ý + số liệu: content/hsg9/cd16-truyen-nhiet-no-vi-nhiet/nguon.md mục "Bài tập mẫu" D1–D3 (dùng nguyên số đã tính).
Nước c = 4200 J/(kg·K), 1 lít = 1 kg ; hao phí ghi rõ giả thiết (không đổi / tỉ lệ hiệu nhiệt độ) ; dẫn nhiệt P ~ SΔt/d.
Mọi đáp số + mọi lựa chọn sai của chon_buoc_ke tính lại bằng Python trong kiem_so()."""
import math
import re
from fractions import Fraction as Fr
from dung import *   # sol, buoc, M/P/A, fig, seg, lbl, poly, arrow, chevron, RED/BLUE/ORG/GRN

GREY = "#94a3b8"
T_NHIET = "Nhiệt độ và cân bằng nhiệt"
T_NL = "Tính nhiệt lượng theo nhiệt dung riêng"
C_NUOC = 4200


def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animate attributeName="{attr}" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def anim_tr(vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animateTransform attributeName="transform" type="translate" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def tx(x, y, s, c="currentColor", size=13, anchor="start", weight="600"):
    """Nhãn SVG; "_{..}" thành chỉ số dưới bằng <tspan dy> (chỉ số Unicode hiện như dấu phẩy)."""
    size = max(size, 14)                 # ≥ 14 đơn vị: viewBox 420 → ≈ 12,5 px ở 375 px
    sm = max(size - 2, 12)
    s = re.sub(r"_\{([^}]*)\}", lambda m: f'<tspan dy="4" font-size="{sm}">{m.group(1)}</tspan><tspan dy="-4">​</tspan>', s)
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'


def wall_box(x, y, w, h, t):
    """Hộp có thành dày t px (vành tô xám, tô kiểu evenodd)."""
    p = (f'M{x},{y} h{w} v{h} h{-w} Z M{x + t},{y + t} v{h - 2 * t} h{w - 2 * t} v{-(h - 2 * t)} Z')
    return (f'<path d="{p}" fill="{GREY}" fill-opacity="0.35" fill-rule="evenodd" stroke="currentColor" stroke-width="1.6"/>')


def keyt(n):
    return ";".join(f"{k / n:.3f}" for k in range(n + 1))


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 1 · hộp xốp đựng đá ─────────────
def d1(kk):
    b = ""
    if kk == 0:
        DUR = 6.0                                   # 1 s mô phỏng = 1 h thật, hộp 1 tan hết sau 6 h
        Y0, H = 52, 110
        # hộp 1: thành 2 cm → 10 px ; hộp 2: thành 3 cm → 15 px (tỉ lệ 2 : 3)
        b += wall_box(30, Y0, 150, H, 10) + wall_box(240, Y0, 150, H, 15)
        b += tx(105, 22, "Hộp 1 · phòng 30 °C", "currentColor", 13, "middle", "700")
        b += tx(315, 22, "Hộp 2 · phòng 25 °C", "currentColor", 13, "middle", "700")
        b += tx(105, 40, "đá 0 °C", BLUE, 12, "middle", "600") + tx(315, 40, "đá 0 °C", BLUE, 12, "middle", "600")
        # đá hộp 1 nhỏ dần: thể tích giảm đều theo thời gian (công suất không đổi) ⇒ cạnh ∝ (1 − u)^(1/3)
        S0, BOT, CX = 56, Y0 + H - 10, 105
        n = 24
        ss = [S0 * (1 - k / n) ** (1 / 3) for k in range(n + 1)]
        b += (f'<rect x="{CX - S0 / 2}" y="{BOT - S0}" width="{S0}" height="{S0}" rx="4" fill="{BLUE}" fill-opacity="0.3" stroke="{BLUE}" stroke-width="2">'
              + anim("width", ";".join(f"{s:.1f}" for s in ss), DUR, keyt(n))
              + anim("height", ";".join(f"{s:.1f}" for s in ss), DUR, keyt(n))
              + anim("x", ";".join(f"{CX - s / 2:.1f}" for s in ss), DUR, keyt(n))
              + anim("y", ";".join(f"{BOT - s:.1f}" for s in ss), DUR, keyt(n)) + "</rect>")
        S2, BOT2 = 56, Y0 + H - 15
        b += f'<rect x="{315 - S2 / 2}" y="{BOT2 - S2}" width="{S2}" height="{S2}" rx="4" fill="{BLUE}" fill-opacity="0.3" stroke="{BLUE}" stroke-width="2"/>'
        # nhiệt từ phòng vào qua thành (mũi tên cùng độ dài, KHÔNG tỉ lệ công suất)
        for xa, xb in ((10, 44), (200, 166), (220, 259), (410, 371)):
            b += arrow("", "o", xa, Y0 + 36, xb, Y0 + 36, 2.2)
        b += tx(105, Y0 + H + 20, "thành 2 cm", "currentColor", 12, "middle", "600")
        b += tx(315, Y0 + H + 20, "thành 3 cm", "currentColor", 12, "middle", "600")
        # trục thời gian của hộp 1
        X0, X1, YT = 40, 170, 212
        b += seg(X0, YT, X1, YT, "currentColor", 1.6)
        for h in range(7):
            x = X0 + (X1 - X0) * h / 6
            b += seg(x, YT - 4, x, YT + 4, "currentColor", 1.2)
        b += tx(X0, YT + 18, "0", "currentColor", 11, "middle", "400") + tx(X1, YT + 18, "6 h", "currentColor", 11, "middle", "400")
        b += f'<circle cx="{X0}" cy="{YT}" r="5" fill="{GRN}">{anim("cx", f"{X0};{X1}", DUR)}</circle>'
        b += tx(315, YT + 4, "tan hết sau ? h", GRN, 13, "middle", "700")
        return fig("c16-1-0", "0 0 420 240", "Hai hộp xốp đựng đá: hộp 1 thành mỏng trong phòng 30 độ, hộp 2 thành dày hơn trong phòng 25 độ; nhiệt từ phòng truyền qua thành vào đá",
                   b, "Mô phỏng chạy nhanh: 1 s = 1 h thật. Chỉ chạy hộp 1: khối đá nhỏ dần đều rồi tan hết sau 6 h. "
                      "Hộp 2 là điều cần tìm nên không chạy. Độ dày thành vẽ theo tỉ lệ 2 : 3 ; mũi tên cam chỉ chiều truyền nhiệt, không chỉ độ lớn.")
    # hình dữ kiện: hai vách cắt ngang
    for x0, dpx, d_lab, dt_lab, plab, tout in ((40, 30, "d_{1} = 2 cm", "Δt_{1} = 30 − 0 = 30 °C", "P_{1}", "30 °C"),
                                                 (240, 45, "d_{2} = 3 cm", "Δt_{2} = 25 − 0 = 25 °C", "P_{2} = ?", "25 °C")):
        xm = x0 + 70
        b += f'<rect x="{xm - dpx / 2}" y="40" width="{dpx}" height="100" fill="{GREY}" fill-opacity="0.35" stroke="currentColor" stroke-width="1.6"/>'
        b += tx(xm - dpx / 2 - 8, 60, tout, ORG, 12, "end", "700") + tx(xm - dpx / 2 - 8, 76, "phòng", ORG, 11, "end", "400")
        b += tx(xm + dpx / 2 + 8, 60, "0 °C", BLUE, 12, "start", "700") + tx(xm + dpx / 2 + 8, 76, "đá", BLUE, 11, "start", "400")
        b += arrow("", "o", xm - dpx / 2 - 30, 104, xm + dpx / 2 + 30, 104, 2.4)
        b += tx(xm, 124, plab, ORG, 12, "middle", "700")
        b += arrow("", "g", xm, 152, xm - dpx / 2, 152, 1.4) + arrow("", "g", xm, 152, xm + dpx / 2, 152, 1.4)
        b += tx(xm, 170, d_lab, GRN, 12, "middle", "700")
        b += tx(xm, 190, dt_lab, "currentColor", 12, "middle", "600")
    b += tx(16, 218, "Cùng vật liệu, cùng diện tích S, cùng lượng đá.", "currentColor", 12, "start", "400")
    return fig("c16-1-2", "0 0 420 228", "Hai vách cắt ngang: vách 1 dày 2 cm, chênh 30 độ; vách 2 dày 3 cm, chênh 25 độ; mũi tên nhiệt đi từ phòng vào đá",
               b, "Dữ kiện: độ chênh nhiệt độ hai mặt vách = nhiệt độ phòng − 0 °C ; mũi tên không vẽ theo độ lớn công suất.")


# ───────────── Dạng 2 · ấm điện đun hai lần ─────────────
def kettle(x, base, liters, color=BLUE):
    """Ấm nhìn nghiêng, đáy tại y = base, vòi bên trái, quai bên phải ; mực nước theo số lít."""
    w0, w1, h = 70, 50, 70
    body = (f'<path d="M{x - w0 / 2},{base} L{x + w0 / 2},{base} L{x + w1 / 2},{base - h} L{x - w1 / 2},{base - h} Z" '
            f'fill="none" stroke="currentColor" stroke-width="2.4"/>')
    lid = seg(x - 12, base - h - 6, x + 12, base - h - 6, "currentColor", 3)
    spout = (f'<path d="M{x - w0 / 2 + 6},{base - 22} L{x - w0 / 2 - 14},{base - 50}" fill="none" stroke="currentColor" stroke-width="2.4"/>')
    handle = (f'<path d="M{x + w1 / 2 - 2},{base - h + 10} Q{x + w0 / 2 + 18},{base - h + 14} {x + w0 / 2 - 2},{base - 18}" '
              f'fill="none" stroke="currentColor" stroke-width="2.4"/>')
    lv = 17 * liters                                 # px mực nước
    wl = w0 - (w0 - w1) * lv / h
    water = (f'<path d="M{x - w0 / 2 + 3},{base - 2} L{x + w0 / 2 - 3},{base - 2} L{x + wl / 2 - 3},{base - lv} L{x - wl / 2 + 3},{base - lv} Z" '
             f'fill="{color}" fill-opacity="0.3" stroke="none"/>')
    return water + body + lid + spout + handle


def thermo(x, base, dur=None):
    """Nhiệt kế đứng cạnh ấm: 20 °C → 100 °C tăng đều (công suất làm nóng không đổi)."""
    ytop, yb = base - 92, base
    y20, y100 = yb - 8, yb - 88
    out = f'<rect x="{x - 4}" y="{ytop}" width="8" height="{yb - ytop}" rx="4" fill="none" stroke="currentColor" stroke-width="1.6"/>'
    out += seg(x + 6, y100, x + 12, y100, "currentColor", 1.2) + tx(x + 14, y100 + 4, "100", "currentColor", 10, "start", "400")
    out += seg(x + 6, y20, x + 12, y20, "currentColor", 1.2) + tx(x + 14, y20 + 4, "20", "currentColor", 10, "start", "400")
    rect = f'<rect x="{x - 2.5}" y="{y20}" width="5" height="{yb - y20}" fill="{RED}"'
    if dur:
        out += rect + f'>{anim("y", f"{y20};{y100}", dur)}{anim("height", f"{yb - y20};{yb - y100}", dur)}</rect>'
    else:
        out += rect + "/>"
    return out


def d2(kk):
    b = ""
    if kk == 0:
        BASE = 156
        b += tx(210, 18, "Cùng ấm, cùng nguồn điện, hao phí không đổi", "currentColor", 14, "middle", "600")
        b += tx(210, 38, "Đun từ 20 °C tới sôi (100 °C)", "currentColor", 14, "middle", "600")
        for x, L, dur, t_lab in ((54, 1, 5.0, "10 phút"), (184, 2, 9.0, "18 phút"), (314, 3, None, "? phút")):
            b += kettle(x, BASE, L) + thermo(x + 50, BASE, dur)
            b += tx(x, BASE + 22, f"{L} lít", BLUE, 13, "middle", "700")
            b += tx(x, BASE + 42, t_lab, GRN if dur is None else "currentColor", 13, "middle", "700")
        return fig("c16-2-0", "0 0 420 210", "Ba ấm điện giống nhau đựng 1 lít, 2 lít và 3 lít nước; nhiệt kế cạnh mỗi ấm chỉ nhiệt độ nước tăng từ 20 lên 100 độ",
                   b, "Mô phỏng chạy nhanh: 1 s = 2 phút thật. Cột đỏ là nhiệt độ nước, tăng đều từ 20 °C tới 100 °C. "
                      "Ấm 3 lít là điều cần tìm nên không chạy.")
    # hình dữ kiện: điện năng chia ba phần
    b += f'<rect x="16" y="64" width="120" height="56" rx="8" fill="none" stroke="currentColor" stroke-width="2"/>'
    b += tx(76, 88, "Điện năng", "currentColor", 13, "middle", "700") + tx(76, 108, "P·t", "currentColor", 13, "middle", "700")
    for yy, c, ch, s1, s2 in ((34, BLUE, "b", "Nước nóng lên", "m·c·Δt"), (92, ORG, "o", "Vỏ ấm nóng lên", "C·Δt"),
                              (150, RED, "r", "Ra môi trường", "P_{hp}·t")):
        b += arrow("", ch, 138, 92, 222, yy, 2.2)
        b += f'<rect x="226" y="{yy - 22}" width="178" height="44" rx="8" fill="none" stroke="{c}" stroke-width="2"/>'
        b += tx(236, yy - 4, s1, c, 12, "start", "700") + tx(236, yy + 14, s2, c, 12, "start", "700")
    b += tx(16, 198, "Lần 1: m = 1 kg, t_{1} = 600 s · Lần 2: m = 2 kg, t_{2} = 1080 s", "currentColor", 12, "start", "400")
    b += tx(16, 218, "Cả nước và vỏ ấm nóng từ 20 °C lên 100 °C: Δt = 80 °C", "currentColor", 12, "start", "400")
    return fig("c16-2-2", "0 0 420 230", "Sơ đồ điện năng của ấm chia thành ba phần: làm nóng nước, làm nóng vỏ ấm, hao phí ra môi trường",
               b, "Dữ kiện: điện năng ấm nhận chia ba phần ; phần hao phí tỉ lệ với thời gian đun vì công suất hao phí không đổi.")


# ───────────── Dạng 3 · máy sưởi, nhiệt độ ổn định ─────────────
def d3(kk):
    b = ""
    if kk == 0:
        DUR, n = 6.0, 30
        us = [k / n for k in range(n + 1)]
        T = [10 + 12 * (1 - math.exp(-4 * u)) for u in us]          # minh hoạ định tính, tiệm cận 22 °C
        kt = keyt(n)
        # căn phòng
        b += f'<rect x="20" y="44" width="170" height="130" fill="none" stroke="currentColor" stroke-width="3"/>'
        b += tx(105, 30, "ngoài trời 10 °C", BLUE, 12, "middle", "700")
        b += f'<rect x="34" y="124" width="36" height="42" rx="3" fill="none" stroke="{RED}" stroke-width="2"/>'
        zz = " ".join(f"{40 + 6 * i},{134 if i % 2 == 0 else 156}" for i in range(5))
        b += f'<polyline points="{zz}" fill="none" stroke="{RED}" stroke-width="1.8"/>'
        b += tx(52, 116, "1200 W", RED, 12, "middle", "700")
        # nhiệt kế trong phòng: y = 166 − 3·T
        XT = 150
        b += f'<rect x="{XT - 4}" y="66" width="8" height="100" rx="4" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        ys = [166 - 3 * t for t in T]
        b += (f'<rect x="{XT - 2.5}" y="{ys[0]:.1f}" width="5" height="{166 - ys[0]:.1f}" fill="{RED}">'
              + anim("y", ";".join(f"{y:.1f}" for y in ys), DUR, kt)
              + anim("height", ";".join(f"{166 - y:.1f}" for y in ys), DUR, kt) + "</rect>")
        b += tx(XT - 10, 62, "phòng", "currentColor", 11, "end", "400")
        # nhiệt mất ra ngoài: mũi tên dài tỉ lệ (t − 10)
        YA, XW = 100, 192
        Ls = [4 * (t - 10) for t in T]
        b += (f'<line x1="{XW}" y1="{YA}" x2="{XW}" y2="{YA}" stroke="{ORG}" stroke-width="2.4">'
              + anim("x2", ";".join(f"{XW + L:.1f}" for L in Ls), DUR, kt) + "</line>")
        b += (f'<g>{anim_tr(";".join(f"{L:.1f},0" for L in Ls), DUR, kt)}{chevron(XW, YA, 1, 0, ORG, 2.4, 10)}</g>')
        b += tx(198, 124, "nhiệt", ORG, 11, "start", "600") + tx(198, 138, "mất ra", ORG, 11, "start", "600")
        # đồ thị t(°C) theo thời gian: y = 176 − 4·T
        OX, OY, XE = 276, 176, 410
        b += seg(OX, OY, XE, OY, "currentColor", 1.6) + chevron(XE, OY, 1, 0, "currentColor", 1.6, 8)
        b += seg(OX, OY, OX, 50, "currentColor", 1.6) + chevron(OX, 50, 0, -1, "currentColor", 1.6, 8)
        b += tx(OX + 6, 52, "t (°C)", "currentColor", 11, "start", "400") + tx(XE, OY + 16, "thời gian", "currentColor", 11, "end", "400")
        for tv in (10, 22):
            yv = OY - 4 * tv
            b += seg(OX, yv, XE - 6, yv, GREY, 1.2, "5 4") + tx(OX - 4, yv + 4, str(tv), "currentColor", 11, "end", "400")
        pts = [(OX + (XE - 12 - OX) * u, OY - 4 * t) for u, t in zip(us, T)]
        cum = [0.0]
        for (xa, ya), (xb2, yb2) in zip(pts, pts[1:]):
            cum.append(cum[-1] + math.hypot(xb2 - xa, yb2 - ya))
        Lc = cum[-1]
        b += poly(pts, RED, 2.6).replace("/>", f' stroke-dasharray="{Lc + 2:.1f}" stroke-dashoffset="{Lc + 2:.1f}">'
                                          + anim("stroke-dashoffset", ";".join(f"{Lc + 2 - c:.1f}" for c in cum), DUR, kt) + "</polyline>")
        return fig("c16-3-0", "0 0 420 196", "Căn phòng có máy sưởi; nhiệt độ phòng tăng dần rồi dừng ở 22 độ, mũi tên nhiệt mất ra ngoài dài dần",
                   b, "Mô phỏng định tính, thời gian không theo tỉ lệ (giả sử lúc bật máy phòng đang 10 °C): nhiệt độ phòng tăng nhanh rồi chậm dần, "
                      "dừng ở 22 °C. Mũi tên cam dài dần vì phòng càng ấm hơn ngoài trời thì nhiệt mất ra ngoài càng nhanh.")
    # hình dữ kiện: hai đường công suất theo nhiệt độ phòng (không số)
    OX, OY = 50, 180
    b += seg(OX, OY, 404, OY, "currentColor", 1.6) + chevron(404, OY, 1, 0, "currentColor", 1.6, 8)
    b += seg(OX, OY, OX, 26, "currentColor", 1.6) + chevron(OX, 26, 0, -1, "currentColor", 1.6, 8)
    b += tx(OX + 6, 30, "công suất", "currentColor", 11, "start", "400") + tx(404, OY + 18, "nhiệt độ phòng t", "currentColor", 11, "end", "400")
    X0L = 100
    b += tx(X0L, OY + 18, "t_{0}", BLUE, 12, "middle", "700")
    x2, y2 = 390, 50
    b += seg(X0L, OY, x2, y2, ORG, 2.4) + tx(x2 - 4, y2 - 8, "P_{hp} = k(t − t_{0})", ORG, 12, "end", "700")
    YP = 110
    b += seg(OX, YP, 396, YP, RED, 2.4) + tx(OX + 6, YP - 8, "P máy sưởi", RED, 12, "start", "700")
    xi = X0L + (OY - YP) * (x2 - X0L) / (OY - y2)
    b += seg(xi, YP, xi, OY, GREY, 1.4, "5 4") + f'<circle cx="{xi:.1f}" cy="{YP}" r="5" fill="{GRN}"/>'
    b += tx(xi, OY + 18, "t ổn định", GRN, 12, "middle", "700")
    b += tx(xi - 12, 164, "phòng nóng lên", "currentColor", 11, "end", "400")
    b += tx(xi + 12, 164, "phòng nguội đi", "currentColor", 11, "start", "400")
    return fig("c16-3-2", "0 0 420 206", "Đồ thị định tính: công suất hao phí tăng theo nhiệt độ phòng, cắt đường công suất máy sưởi tại nhiệt độ ổn định",
               b, "Hình định tính, không theo số của đề: bên trái giao điểm, máy sưởi cấp nhiều hơn phần mất đi ; bên phải thì ngược lại.")


BUILD = [d1, d2, d3]


# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Dẫn nhiệt qua vách: tỉ số công suất theo độ dày và độ chênh nhiệt độ",
      topic=T_NHIET,
      problem_html=r"""<p>Một hộp xốp kín đựng một khối đá ở $0\ ^\circ\text{C}$. Thành hộp dày $2\ \text{cm}$ ; để hộp trong phòng $30\ ^\circ\text{C}$ thì đá tan hết sau $6$ giờ. Trong khi đá tan, bên trong hộp luôn ở $0\ ^\circ\text{C}$ ; đá chỉ nhận nhiệt truyền qua thành hộp từ không khí trong phòng. Biết công suất nhiệt truyền qua một vách tỉ lệ thuận với diện tích vách và với độ chênh nhiệt độ hai mặt vách, tỉ lệ nghịch với độ dày vách.</p><ol type="a"><li>Một hộp thứ hai cùng vật liệu, cùng diện tích thành, đựng cùng lượng đá ở $0\ ^\circ\text{C}$ nhưng thành dày $3\ \text{cm}$ và để trong phòng $25\ ^\circ\text{C}$. Sau bao lâu thì đá trong hộp thứ hai tan hết?</li><li>Muốn một hộp cùng vật liệu, cùng diện tích thành, đựng cùng lượng đá, để trong phòng $25\ ^\circ\text{C}$ mà đá tan hết sau đúng $6$ giờ thì thành hộp phải dày bao nhiêu?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Hao phí không đổi: đun hai lần để khử nhiệt dung chưa biết của ấm",
      topic=T_NL,
      problem_html=r"""<p>Dùng một ấm điện đun nước từ $20\ ^\circ\text{C}$ tới sôi ($100\ ^\circ\text{C}$). Đun $1$ lít nước mất $10$ phút ; đun $2$ lít nước (cùng ấm, cùng nguồn điện, cùng nhiệt độ ban đầu) mất $18$ phút. Coi công suất điện của ấm và công suất hao phí ra môi trường không đổi trong mọi lần đun. Vỏ ấm có nhiệt dung $C$ (nhiệt lượng để vỏ ấm nóng thêm $1\ ^\circ\text{C}$) chưa biết ; lần nào vỏ ấm cũng nóng từ $20\ ^\circ\text{C}$ lên $100\ ^\circ\text{C}$ cùng với nước. Nước có $c=4200\ \text{J/(kg·K)}$ ; $1$ lít nước có khối lượng $1\ \text{kg}$.</p><ol type="a"><li>Tìm phần công suất dùng để làm nóng nước và vỏ ấm, $P_{ci}=P-P_{hp}$.</li><li>Tìm nhiệt dung $C$ của vỏ ấm.</li><li>Đun $3$ lít nước từ $20\ ^\circ\text{C}$ tới sôi thì mất bao nhiêu phút?</li><li>Trên ấm ghi $875\ \text{W}$ (coi là công suất điện ấm tiêu thụ). Tìm công suất hao phí $P_{hp}$ và hiệu suất của lần đun $1$ lít nước nếu chỉ tính nhiệt lượng nước nhận là có ích.</li></ol>"""),
 dict(label="Dạng 3 · Khá · Hao phí tỉ lệ hiệu nhiệt độ: nhiệt độ ổn định của căn phòng có máy sưởi",
      topic=T_NHIET,
      problem_html=r"""<p>Một căn phòng được sưởi bằng máy sưởi điện công suất $1200\ \text{W}$ ; máy biến toàn bộ điện năng thành nhiệt và phòng chỉ nhận nhiệt từ máy sưởi. Công suất nhiệt phòng mất ra ngoài trời tỉ lệ thuận với hiệu nhiệt độ trong phòng và ngoài trời : $P_{hp}=k\,(t-t_0)$, với $t$ là nhiệt độ phòng, $t_0$ là nhiệt độ ngoài trời, $k$ không đổi. Khi ngoài trời $10\ ^\circ\text{C}$, bật máy sưởi liên tục thì nhiệt độ phòng tăng dần rồi ổn định ở $22\ ^\circ\text{C}$.</p><ol type="a"><li>Tìm hệ số $k$.</li><li>Một hôm ngoài trời $4\ ^\circ\text{C}$. Muốn giữ phòng ở $22\ ^\circ\text{C}$ thì máy sưởi phải có công suất bao nhiêu?</li><li>Nếu hôm đó vẫn dùng máy sưởi $1200\ \text{W}$ thì nhiệt độ phòng ổn định ở bao nhiêu?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1 (mo_het)
 [(r'"Thành hộp dày $2\ \text{cm}$ ; để hộp trong phòng $30\ ^\circ\text{C}$ thì đá tan hết sau $6$ giờ"', r"$d_1=2\ \text{cm}$ ; $\Delta t_1=30-0=30\ ^\circ\text{C}$ ; $t_1=6\ \text{h}$", r"Nhiệt tự truyền từ không khí nóng hơn vào đá lạnh hơn<br>Công suất truyền nhiệt $P$ : nhiệt lượng truyền qua trong $1\ \text{s}$"),
  (r'"bên trong hộp luôn ở $0\ ^\circ\text{C}$ ; đá chỉ nhận nhiệt truyền qua thành hộp"', r"$\Delta t$ giữ nguyên suốt lúc đá tan", r"⚠ $\Delta t$ không đổi nên $P$ không đổi : $Q=P\,t$<br>⚠ không có đường nhận nhiệt nào khác"),
  (r'"tỉ lệ thuận với diện tích vách và với độ chênh nhiệt độ … tỉ lệ nghịch với độ dày vách"', r"$P\sim\dfrac{S\,\Delta t}{d}$", r"Cùng vật liệu, cùng $S$ : chỉ còn $\Delta t$ và $d$ quyết định tỉ số công suất"),
  (r'"thành dày $3\ \text{cm}$ và để trong phòng $25\ ^\circ\text{C}$ … cùng lượng đá"', r"$d_2=3\ \text{cm}$ ; $\Delta t_2=25\ ^\circ\text{C}$ ; cùng $Q$", r"Cùng lượng đá ở $0\ ^\circ\text{C}$ : nhiệt lượng cần để tan hết như nhau"),
  (r'"Sau bao lâu thì đá trong hộp thứ hai tan hết?"', r"Cần $t_2$", r"$P_1t_1=P_2t_2$"),
  (r'"phòng $25\ ^\circ\text{C}$ mà đá tan hết sau đúng $6$ giờ thì thành hộp phải dày bao nhiêu?"', r"$\Delta t=25\ ^\circ\text{C}$ ; $t=6\ \text{h}$ ; cần $d$", r"Cùng $Q$, cùng thời gian thì công suất so với hộp nào?")],
 # Dạng 2 (giau_buoc_cuoi: bước hiệu suất bị giấu)
 [(r'"Đun $1$ lít nước mất $10$ phút"', r"$m_1=1\ \text{kg}$ ; $t_1=600\ \text{s}$ ; $\Delta t=80\ ^\circ\text{C}$", r"Nước nhận $Q=m\,c\,\Delta t$<br>⚠ đổi phút ra giây trước khi tính công suất"),
  (r'"đun $2$ lít nước … mất $18$ phút"', r"$m_2=2\ \text{kg}$ ; $t_2=1080\ \text{s}$", r"Hai lần đun khác nhau đúng $1$ lít nước"),
  (r'"công suất điện của ấm và công suất hao phí ra môi trường không đổi"', r"$P$, $P_{hp}$ như nhau mọi lần", r"⚠ hao phí tỉ lệ với thời gian : $Q_{hp}=P_{hp}\,t$<br>Phần còn lại $P_{ci}=P-P_{hp}$ làm nóng nước và vỏ ấm"),
  (r'"Vỏ ấm có nhiệt dung $C$ … chưa biết"', r"Vỏ ấm nhận $C\,\Delta t$, lần nào cũng như nhau", r"Nhiệt dung : nhiệt lượng làm vật nóng thêm $1\ ^\circ\text{C}$ (J/K)<br>$P_{ci}\,t=(mc+C)\,\Delta t$"),
  (r'"Đun $3$ lít nước … mất bao nhiêu phút?"', r"$m_3=3\ \text{kg}$ ; cần $t_3$", r"$t_3=\dfrac{(m_3c+C)\,\Delta t}{P_{ci}}$"),
  (r'"Trên ấm ghi $875\ \text{W}$ … công suất hao phí"', r"$P=875\ \text{W}$", r"$P_{hp}=P-P_{ci}$"),
  (r'"hiệu suất của lần đun $1$ lít nước nếu chỉ tính nhiệt lượng nước nhận là có ích"', r"Cần $H$", r"Phần có ích là nhiệt lượng nào? Điện năng toàn phần tính trong thời gian của lần đun nào?")],
 # Dạng 3 (giau_tu_buoc_2: bước 2–4 bị giấu → cột 3 viết câu hỏi gợi)
 [(r'"máy biến toàn bộ điện năng thành nhiệt và phòng chỉ nhận nhiệt từ máy sưởi"', r"$P=1200\ \text{W}$ là toàn bộ nhiệt phòng nhận mỗi giây", r"⚠ bỏ qua nhiệt từ người, đèn, nắng chiếu vào"),
  (r'"tỉ lệ thuận với hiệu nhiệt độ trong phòng và ngoài trời : $P_{hp}=k\,(t-t_0)$"', r"$k$ không đổi", r"⚠ không phải hao phí không đổi : phòng càng ấm hơn ngoài trời thì mất nhiệt càng nhanh"),
  (r'"ngoài trời $10\ ^\circ\text{C}$ … ổn định ở $22\ ^\circ\text{C}$"', r"$t_0=10\ ^\circ\text{C}$ ; $t=22\ ^\circ\text{C}$", r"Nhiệt độ không đổi nữa thì nhiệt lượng vào và ra mỗi giây so với nhau thế nào?"),
  (r'"Tìm hệ số $k$"', r"Cần $k$ (W/°C)", r"Phương trình nào nối $P$, $k$ và hiệu nhiệt độ lúc ổn định?"),
  (r'"ngoài trời $4\ ^\circ\text{C}$. Muốn giữ phòng ở $22\ ^\circ\text{C}$"', r"$t_0'=4\ ^\circ\text{C}$ ; $t=22\ ^\circ\text{C}$ ; cần $P'$", r"$k$ có đổi khi trời lạnh hơn không? Hiệu nhiệt độ mới là bao nhiêu?"),
  (r'"vẫn dùng máy sưởi $1200\ \text{W}$"', r"$P=1200\ \text{W}$ ; $t_0'=4\ ^\circ\text{C}$ ; cần $t'$", r"Trong phương trình cân bằng, đại lượng nào bây giờ là ẩn?")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> nhiệt tự truyền từ vật nóng hơn sang vật lạnh hơn ; công suất truyền nhiệt $P$ là nhiệt lượng truyền qua trong $1\ \text{s}$.",
      r"<strong>Dẫn nhiệt qua vách:</strong> $P\sim\dfrac{S\,\Delta t}{d}$ (tỉ lệ thuận với diện tích và độ chênh nhiệt độ, tỉ lệ nghịch với độ dày).",
      r"<strong>Công thức:</strong> $P$ không đổi thì $Q=P\,t$.",
      r"<strong>Điều kiện:</strong> trong hộp giữ $0\ ^\circ\text{C}$ suốt lúc đá tan nên $\Delta t$ và $P$ không đổi ; đá chỉ nhận nhiệt qua thành."]
R2 = [r"<strong>Khái niệm:</strong> nhiệt dung $C$ của một vật là nhiệt lượng làm vật nóng thêm $1\ ^\circ\text{C}$ (đơn vị J/K).",
      r"<strong>Công thức:</strong> nước nhận $Q=m\,c\,\Delta t$ ; vỏ ấm nhận $C\,\Delta t$ ; hao phí $Q_{hp}=P_{hp}\,t$.",
      r"<strong>Bảo toàn năng lượng:</strong> $P\,t=m\,c\,\Delta t+C\,\Delta t+P_{hp}\,t$, tức $P_{ci}\,t=(mc+C)\,\Delta t$ với $P_{ci}=P-P_{hp}$.",
      r"<strong>Hiệu suất:</strong> $H=\dfrac{Q_{ci}}{P\,t}$.",
      r"<strong>Điều kiện:</strong> $P$ và $P_{hp}$ không đổi ; thời gian đổi ra giây."]
R3 = [r"<strong>Khái niệm:</strong> nhiệt độ phòng ổn định khi nhiệt lượng nhận vào và nhiệt lượng mất đi trong mỗi giây bằng nhau.",
      r"<strong>Giả thiết hao phí:</strong> $P_{hp}=k\,(t-t_0)$ ; phòng càng ấm hơn ngoài trời thì mất nhiệt càng nhanh.",
      r"<strong>Phương trình cân bằng:</strong> $P=k\,(t-t_0)$.",
      r"<strong>Điều kiện:</strong> phòng chỉ nhận nhiệt từ máy sưởi ; máy biến toàn bộ điện năng thành nhiệt ; $k$ không đổi."]

SOLS = [
 sol(R1, [
  ("Tỉ số công suất truyền nhiệt vào hai hộp", [P(r"Cùng vật liệu, cùng $S$ nên chỉ còn $\Delta t$ và $d$ khác nhau :"),
     M(r"\dfrac{P_1}{P_2}=\dfrac{\Delta t_1}{\Delta t_2}\cdot\dfrac{d_2}{d_1}"), M(r"\dfrac{P_1}{P_2}=\dfrac{30}{25}\cdot\dfrac{3}{2}"), A(r"\dfrac{P_1}{P_2}=1{,}8")]),
  ("Thời gian đá tan hết ở hộp thứ hai", [P(r"Cùng lượng đá ở $0\ ^\circ\text{C}$ nên cần cùng nhiệt lượng $Q$ để tan hết :"),
     M(r"Q=P_1t_1=P_2t_2"), M(r"t_2=t_1\cdot\dfrac{P_1}{P_2}=6\cdot1{,}8"), A(r"t_2=10{,}8\ \text{h}")]),
  ("Độ dày thành để đá tan hết sau 6 giờ", [P(r"Cùng $Q$, cùng thời gian $6\ \text{h}$ như hộp đầu nên công suất phải bằng $P_1$ :"),
     M(r"\dfrac{\Delta t_2}{d}=\dfrac{\Delta t_1}{d_1}"), M(r"d=d_1\cdot\dfrac{\Delta t_2}{\Delta t_1}=2\cdot\dfrac{25}{30}"), A(r"d\approx1{,}67\ \text{cm}")]),
  ("Kiểm tra", [P(r"Hộp thứ hai thành dày hơn và phòng mát hơn, cả hai điều đều làm nhiệt vào chậm hơn : $t_2\gt6\ \text{h}$ là hợp lí ✓."),
     P(r"Phòng mát hơn thì thành mỏng hơn vẫn giữ được $6\ \text{h}$ : $d\lt2\ \text{cm}$ ✓."),
     P(r"Tỉ số công suất không có đơn vị ; $d$ cùng đơn vị cm với $d_1$ ✓.")])],
  [r"a) $t_2=10{,}8\ \text{h}$ (10 giờ 48 phút)", r"b) $d\approx1{,}67\ \text{cm}$"],
  r"Nhận dạng: thấy <strong>cùng vật liệu, đổi độ dày thành hoặc nhiệt độ bên ngoài</strong> → lập tỉ số $P\sim\dfrac{S\,\Delta t}{d}$ ; cùng $Q$ thì thời gian tỉ lệ nghịch với $P$."),
 sol(R2, [
  ("Nhiệt lượng cho một lít nước thêm", [P(r"Lần 2 hơn lần 1 đúng $1$ lít nước ; vỏ ấm và $\Delta t=80\ ^\circ\text{C}$ như nhau :"),
     M(r"Q_n=m\,c\,\Delta t=1\cdot4200\cdot80"), A(r"Q_n=336\,000\ \text{J}")]),
  ("Công suất làm nóng nước và vỏ ấm", [P(r"Trừ phương trình lần 1 khỏi lần 2 : phần vỏ ấm $C\,\Delta t$ triệt tiêu."),
     M(r"P_{ci}\,(t_2-t_1)=Q_n"), M(r"P_{ci}=\dfrac{336\,000}{1080-600}=\dfrac{336\,000}{480}"), A(r"P_{ci}=700\ \text{W}")]),
  ("Nhiệt dung của vỏ ấm", [P(r"Phương trình lần 1 :"), M(r"P_{ci}\,t_1=(m_1c+C)\,\Delta t"), M(r"700\cdot600=(4200+C)\cdot80"),
     M(r"4200+C=5250"), A(r"C=1050\ \text{J/K}")]),
  ("Thời gian đun 3 lít nước", [M(r"t_3=\dfrac{(m_3c+C)\,\Delta t}{P_{ci}}"), M(r"t_3=\dfrac{(3\cdot4200+1050)\cdot80}{700}"),
     A(r"t_3=1560\ \text{s}=26\ \text{phút}")]),
  ("Công suất hao phí", [M(r"P_{hp}=P-P_{ci}=875-700"), A(r"P_{hp}=175\ \text{W}")]),
  ("Hiệu suất lần đun 1 lít", [P(r"Có ích chỉ là nhiệt lượng nước nhận ; điện năng toàn phần tính trong $t_1=600\ \text{s}$ :"),
     M(r"H=\dfrac{m_1c\,\Delta t}{P\,t_1}=\dfrac{336\,000}{875\cdot600}"), A(r"H=0{,}64=64\ \%")]),
  ("Kiểm tra", [P(r"Mỗi lít thêm cần thêm $8$ phút : $18+8=26$ phút, khớp câu c ✓."),
     P(r"Lần 1 : nước $336\,000\ \text{J}$ + vỏ ấm $1050\cdot80=84\,000\ \text{J}$ + hao phí $175\cdot600=105\,000\ \text{J}$ $=525\,000\ \text{J}=875\cdot600$ ✓."),
     P(r"Đơn vị : $\dfrac{\text{J}}{\text{s}}=\text{W}$ ; $C$ tính bằng $\dfrac{\text{J}}{\text{K}}$ ✓.")])],
  [r"a) $P_{ci}=700\ \text{W}$", r"b) $C=1050\ \text{J/K}$", r"c) $t_3=26$ phút", r"d) $P_{hp}=175\ \text{W}$ ; $H=64\ \%$"],
  r"Nhận dạng: thấy <strong>đun hai lượng nước khác nhau, hao phí không đổi</strong> → trừ hai phương trình năng lượng để khử nhiệt dung chưa biết của ấm."),
 sol(R3, [
  ("Điều kiện nhiệt độ ổn định", [P(r"Nhiệt độ phòng không đổi nữa nên nhiệt lượng vào bằng nhiệt lượng ra trong mỗi giây :"),
     M(r"P=P_{hp}=k\,(t-t_0)"), P(r"Máy vẫn sưởi, phòng vẫn mất nhiệt ; hai dòng nhiệt bằng nhau.")]),
  ("Hệ số k", [M(r"k=\dfrac{P}{t-t_0}=\dfrac{1200}{22-10}"), A(r"k=100\ \text{W/}^\circ\text{C}")]),
  ("Công suất cần khi ngoài trời 4 °C", [P(r"$k$ chỉ phụ thuộc căn phòng (tường, cửa), không đổi :"),
     M(r"P'=k\,(22-4)=100\cdot18"), A(r"P'=1800\ \text{W}")]),
  ("Nhiệt độ ổn định mới với máy 1200 W", [M(r"1200=k\,(t'-4)"), M(r"t'-4=\dfrac{1200}{100}=12"), A(r"t'=16\ ^\circ\text{C}")]),
  ("Kiểm tra", [P(r"Với máy $1200\ \text{W}$, hiệu nhiệt độ trong – ngoài lúc ổn định luôn là $\dfrac{P}{k}=12\ ^\circ\text{C}$ : $10+12=22$ ✓ ; $4+12=16$ ✓."),
     P(r"Phòng vẫn ấm hơn ngoài trời ($16\gt4$) nhưng không giữ được $22\ ^\circ\text{C}$ ✓."),
     P(r"Đơn vị : $\dfrac{\text{W}}{^\circ\text{C}}\cdot{}^\circ\text{C}=\text{W}$ ✓.")])],
  [r"a) $k=100\ \text{W/}^\circ\text{C}$", r"b) $P'=1800\ \text{W}$", r"c) $t'=16\ ^\circ\text{C}$"],
  r"Nhận dạng: thấy <strong>nhiệt độ ổn định</strong> và <strong>hao phí tỉ lệ hiệu nhiệt độ</strong> → cân bằng $P=k\,(t-t_0)$ ; hiệu nhiệt độ lúc ổn định là $P/k$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>cùng vật liệu, đổi độ dày thành hoặc nhiệt độ ngoài</b> → lập tỉ số $P\sim\dfrac{S\,\Delta t}{d}$, cùng $Q$ thì $t\sim\dfrac{1}{P}$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Tỉ số công suất truyền nhiệt vào hai hộp", "Công suất nhiệt truyền vào hộp đầu gấp bao nhiêu lần hộp thứ hai?", 1.8, "lần", 0.02,
       loi=r"Chỉ xét độ dày mà quên độ chênh nhiệt độ cũng đổi, hoặc nhân tỉ số độ dày theo chiều thuận (coi vách dày thì nhiệt vào nhanh)."),
  buoc("Thời gian đá tan hết ở hộp thứ hai", "Đá trong hộp thứ hai tan hết sau bao nhiêu giờ?", 10.8, "h", 0.1,
       loi=r"Đặt ngược tỉ số công suất : cùng nhiệt lượng thì thời gian tỉ lệ nghịch với công suất, không tỉ lệ thuận.",
       ke=[(r"Cùng nhiệt lượng $Q$ : $P_1t_1=P_2t_2$, rồi giải $t_2$", True),
           (r"Lấy $t_2=t_1\cdot\dfrac{P_2}{P_1}$", r"Công suất nhỏ thì phải lâu mới đủ nhiệt lượng ; thời gian tỉ lệ nghịch với công suất nên tỉ số phải là $\dfrac{P_1}{P_2}$."),
           (r"Lấy $t_2=t_1\cdot\dfrac{\Delta t_2}{\Delta t_1}$", r"Bỏ mất ảnh hưởng của độ dày thành ; hơn nữa chênh nhiệt độ nhỏ thì nhiệt vào chậm, thời gian phải tỉ lệ nghịch với $\Delta t$.")]),
  buoc("Độ dày thành để đá tan hết sau 6 giờ", "Thành hộp phải dày bao nhiêu xentimét?", 1.67, "cm", 0.02,
       loi=r"Đặt tỉ số độ chênh nhiệt độ theo chiều ngược, hoặc so với hộp thứ hai thay vì hộp đầu (hộp đã biết thời gian 6 giờ).",
       ke=[(r"Cùng $Q$, cùng thời gian nên $P$ bằng $P_1$ : $\dfrac{\Delta t_2}{d}=\dfrac{\Delta t_1}{d_1}$", True),
           (r"Lấy $d=d_1\cdot\dfrac{\Delta t_1}{\Delta t_2}$", r"$P$ tỉ lệ thuận với $\Delta t$, tỉ lệ nghịch với $d$ ; giữ $P$ không đổi thì $d$ phải tỉ lệ thuận với $\Delta t$, không phải tỉ lệ nghịch."),
           (r"Lấy $d=d_2\cdot\dfrac{\Delta t_2}{\Delta t_1}$", r"Hộp thứ hai không tan hết sau 6 giờ ; mốc so sánh phải là hộp đầu (dày $d_1$, tan hết sau đúng 6 giờ).")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>đun hai lần, hao phí không đổi, ấm có nhiệt dung chưa biết</b> → trừ hai phương trình năng lượng.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhiệt lượng cho một lít nước thêm", "Nhiệt lượng để đun 1 lít nước từ 20 °C tới sôi là bao nhiêu jun?", 336000, "J", 1000,
       loi=r"Lấy độ tăng nhiệt độ bằng 100 °C, quên nước bắt đầu từ 20 °C."),
  buoc("Công suất làm nóng nước và vỏ ấm", "Phần công suất làm nóng nước và vỏ ấm là bao nhiêu oát?", 700, "W", 5,
       loi=r"Chia nhiệt lượng của 1 lít nước cho thời gian lần đun đầu, quên rằng trong lần đó ấm còn làm nóng vỏ ấm.",
       ke=[(r"Chia nhiệt lượng đó cho hiệu thời gian $t_2-t_1$ (đổi ra giây)", True),
           (r"Chia nhiệt lượng đó cho $t_1=600\ \text{s}$", r"Trong $600\ \text{s}$ đầu, phần công suất này làm nóng cả nước lẫn vỏ ấm ; nhiệt lượng của riêng 1 lít nước không ứng với $600\ \text{s}$."),
           (r"Chia nhiệt lượng đó cho $t_2-t_1=8$ (để nguyên phút)", r"Oát là jun trên giây ; để thời gian theo phút thì kết quả lớn gấp $60$ lần.")]),
  buoc("Nhiệt dung của vỏ ấm", "Nhiệt dung C của vỏ ấm là bao nhiêu J/K?", 1050, "J/K", 10,
       loi=r"Quên trừ phần nhiệt lượng của nước, coi toàn bộ phần làm nóng là của vỏ ấm.",
       ke=[(r"Viết $P_{ci}\,t_1=(m_1c+C)\,\Delta t$ cho lần 1 rồi giải ra $C$", True),
           (r"Lấy $C=\dfrac{P_{ci}\,t_1}{\Delta t}$", r"Đó là nhiệt dung của cả nước lẫn vỏ ấm ; phải trừ phần của nước $m_1c$."),
           (r"Viết phương trình lần 1 với $\Delta t=100\ ^\circ\text{C}$", r"Nước và vỏ ấm nóng từ $20\ ^\circ\text{C}$ lên $100\ ^\circ\text{C}$ ; độ tăng nhiệt độ không phải $100\ ^\circ\text{C}$.")]),
  buoc("Thời gian đun 3 lít nước", "Đun 3 lít nước tới sôi mất bao nhiêu phút?", 26, "phút", 0.2,
       loi=r"Cho thời gian tỉ lệ thuận với lượng nước, quên rằng vỏ ấm chỉ có một và nhận nhiệt lượng như nhau mọi lần.",
       ke=[(r"Tính $t_3=\dfrac{(m_3c+C)\,\Delta t}{P_{ci}}$ rồi đổi ra phút", True),
           (r"Lấy $t_3=3\,t_1$ vì nước gấp 3 lần", r"Nhiệt lượng làm nóng vỏ ấm không tăng theo lượng nước nên thời gian không tỉ lệ thuận với khối lượng nước."),
           (r"Tính $t_3=\dfrac{m_3c\,\Delta t}{P_{ci}}$", r"Quên phần nhiệt lượng làm nóng vỏ ấm $C\,\Delta t$.")]),
  buoc("Công suất hao phí", "Công suất hao phí của ấm là bao nhiêu oát?", 175, "W", 2,
       loi=r"Lấy công suất ghi trên ấm trừ phần chỉ làm nóng nước, coi phần làm nóng vỏ ấm là hao phí ra môi trường.",
       ke=[(r"$P_{hp}=P-P_{ci}$", True),
           (r"$P_{hp}=P-\dfrac{m_1c\,\Delta t}{t_1}$", r"Phần $\dfrac{m_1c\,\Delta t}{t_1}$ chỉ tính nước ; vỏ ấm nóng lên không phải là hao phí ra môi trường."),
           (r"$P_{hp}=(P-P_{ci})\cdot t_1$", r"Nhân với thời gian cho ra nhiệt lượng hao phí (đơn vị J), không phải công suất.")]),
  buoc("Hiệu suất lần đun 1 lít", "Hiệu suất của lần đun 1 lít nước là bao nhiêu phần trăm?", 64, "%", 0.5,
       loi=r"Coi phần làm nóng vỏ ấm cũng là có ích, hoặc lấy thời gian của lần đun 2 lít.",
       ke=[(r"$H=\dfrac{m_1c\,\Delta t}{P\,t_1}$", True),
           (r"$H=\dfrac{P_{ci}}{P}$", r"Tỉ số này coi cả phần làm nóng vỏ ấm là có ích ; đề chỉ tính nhiệt lượng nước nhận."),
           (r"$H=\dfrac{m_1c\,\Delta t}{P\,t_2}$", r"Lần đun 1 lít kéo dài $t_1$ ; $t_2$ là thời gian của lần đun 2 lít.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>nhiệt độ ổn định</b> và <b>hao phí tỉ lệ hiệu nhiệt độ</b> → cân bằng $P=k\,(t-t_0)$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Điều kiện nhiệt độ ổn định", "Khi nhiệt độ phòng đã ổn định, phát biểu nào đúng?",
       lua_chon=[(r"Công suất máy sưởi bằng công suất nhiệt phòng mất ra ngoài", True),
                 (r"Máy sưởi đã ngừng truyền nhiệt cho phòng", r"Máy vẫn chạy và vẫn cấp nhiệt ; nhiệt độ đứng yên vì nhiệt mất ra ngoài nhanh đúng bằng thế."),
                 (r"Phòng không còn mất nhiệt ra ngoài trời", r"Phòng còn ấm hơn ngoài trời thì nhiệt vẫn truyền ra ngoài.")],
       loi=r"Nghĩ rằng nhiệt độ đứng yên vì không còn nhiệt truyền vào hoặc ra."),
  buoc("Hệ số k", "Hệ số k bằng bao nhiêu W/°C?", 100, "W/°C", 1,
       loi=r"Chia công suất cho nhiệt độ phòng hoặc nhiệt độ ngoài trời thay vì cho hiệu hai nhiệt độ.",
       ke=[(r"Dùng $P=k\,(t-t_0)$ với $t-t_0$ là hiệu nhiệt độ lúc ổn định", True),
           (r"Lấy $k=\dfrac{P}{t}$ với $t$ là nhiệt độ phòng", r"Hao phí tỉ lệ với hiệu nhiệt độ trong – ngoài, không phải với nhiệt độ phòng."),
           (r"Lấy $k=P\cdot(t-t_0)$", r"$P=k\,(t-t_0)$ nên $k$ là thương chứ không phải tích ; đơn vị của $k$ phải là W/°C.")]),
  buoc("Công suất cần khi ngoài trời 4 °C", "Máy sưởi phải có công suất bao nhiêu oát?", 1800, "W", 10,
       loi=r"Áp giả thiết hao phí không đổi, giữ nguyên công suất cũ.",
       ke=[(r"Giữ $k$, tính $P'=k\,(22-4)$", True),
           (r"Vẫn $1200\ \text{W}$ vì vẫn giữ phòng $22\ ^\circ\text{C}$", r"Hao phí phụ thuộc hiệu nhiệt độ trong – ngoài ; hiệu này đã đổi nên công suất cần cũng đổi."),
           (r"Lấy $P'=1200\cdot\dfrac{10}{4}$", r"Hao phí tỉ lệ với hiệu nhiệt độ, không tỉ lệ nghịch với nhiệt độ ngoài trời.")]),
  buoc("Nhiệt độ ổn định mới với máy 1200 W", "Phòng ổn định ở bao nhiêu °C?", 16, "°C", 0.2,
       loi=r"Quên cộng nhiệt độ ngoài trời, lấy luôn hiệu nhiệt độ làm nhiệt độ phòng.",
       ke=[(r"Cân bằng $1200=k\,(t'-4)$ rồi giải $t'$", True),
           (r"Lấy $t'=\dfrac{P}{k}$", r"$\dfrac{P}{k}$ là hiệu nhiệt độ trong – ngoài, chưa phải nhiệt độ phòng."),
           (r"Lấy $t'=22\cdot\dfrac{4}{10}$", r"Nhiệt độ phòng không tỉ lệ thuận với nhiệt độ ngoài trời ; mốc $0\ ^\circ\text{C}$ là quy ước nên tỉ số hai nhiệt độ không có ý nghĩa.")]),
  buoc("Kiểm tra")]),
]


def kiem_so():
    F = Fr
    # D1
    r = F(30, 25) * F(3, 2); assert r == F(9, 5)
    t2 = 6 * r; assert t2 == F(54, 5) and abs(float(t2) - 10.8) < 1e-12
    d = 2 * F(25, 30); assert abs(float(d) - 1.6667) < 1e-3 and abs(float(d) - 1.67) <= 0.02
    # lựa chọn sai D1 cho số khác đáp án (ngoài sai số)
    for w in (6 * F(5, 9), 6 * F(25, 30)):              # đặt ngược tỉ số ; chỉ xét Δt
        assert abs(float(w) - 10.8) > 0.1
    for w in (2 * F(30, 25), 3 * F(25, 30)):            # tỉ lệ nghịch Δt ; so với hộp 2
        assert abs(float(w) - 1.67) > 0.02
    for w in (F(3, 2), F(30, 25), F(2, 3)):             # lỗi bước 1: chỉ xét d, chỉ xét Δt, nhân thuận độ dày
        assert abs(float(w) - 1.8) > 0.02
    assert abs(float(F(30, 25) * F(2, 3)) - 1.8) > 0.02
    # D2
    dT = 80
    Qn = 1 * C_NUOC * dT; assert Qn == 336000
    Pci = F(Qn, 1080 - 600); assert Pci == 700
    Cv = Pci * 600 / dT - C_NUOC; assert Cv == 1050
    assert Pci * 1080 == (2 * C_NUOC + Cv) * dT          # lần 2 khớp
    t3 = (3 * C_NUOC + Cv) * dT / Pci; assert t3 == 1560 and t3 / 60 == 26 and 18 + 8 == 26
    Php = 875 - Pci; assert Php == 175
    H = F(Qn, 875 * 600); assert H == F(16, 25)
    assert Qn + Cv * dT + Php * 600 == 875 * 600         # bảo toàn năng lượng lần 1
    assert Qn + Cv * dT + Php * 1080 + C_NUOC * dT == 875 * 1080
    # lựa chọn sai D2
    assert abs(float(F(Qn, 600)) - 700) > 5 and abs(float(F(Qn, 8)) - 700) > 5            # chia t1 ; để phút
    assert abs(float(Pci * 600 / dT) - 1050) > 10 and abs(float(Pci * 600 / 100 - C_NUOC) - 1050) > 10   # quên trừ nước ; Δt = 100
    assert abs(3 * 10 - 26) > 0.2 and abs(float(3 * C_NUOC * dT / Pci / 60) - 26) > 0.2               # tỉ lệ thuận ; quên vỏ ấm
    assert abs(float(875 - F(Qn, 600)) - 175) > 2 and abs(float((875 - Pci) * 600) - 175) > 2         # gộp vỏ ấm ; ra jun
    assert abs(float(Pci / 875) * 100 - 64) > 0.5 and abs(float(F(Qn, 875 * 1080)) * 100 - 64) > 0.5   # tính cả vỏ ấm ; dùng t2
    assert abs(1 * C_NUOC * 100 - 336000) > 1000                                                       # lỗi bước 1: Δt = 100
    # D3
    k = F(1200, 22 - 10); assert k == 100
    P2 = k * (22 - 4); assert P2 == 1800
    t_ = 4 + F(1200) / k; assert t_ == 16 and 22 - (10 - 4) == t_      # cách tắt (dời cùng một lượng) cũng ra 16
    assert abs(float(F(1200, 22)) - 100) > 1 and abs(1200 * 12 - 100) > 1 and abs(float(F(1200, 10)) - 100) > 1
    assert abs(1200 - 1800) > 10 and abs(1200 * 10 / 4 - 1800) > 10
    assert abs(float(F(1200) / k) - 16) > 0.2 and abs(22 * 4 / 10 - 16) > 0.2
    print("kiểm số liệu CĐ16 D1–D3: đạt")
