"""Hình cho bài tập mẫu Bài 17 "Hiện tượng phóng xạ" (Vật lí 12), lesson_id 18.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng dùng chất/mẫu MINH HOẠ khác đề (ghi rõ trong chú thích), đường cong và thời điểm phân rã TÍNH THẬT từ định luật
phóng xạ N = N0·2^(−t/T); hình dữ kiện chỉ có dữ kiện đề cho và dấu "?" ở đại lượng cần tìm."""
import math, os, random, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

GREY = "#94a3b8"
NOTE = "Hình minh hoạ, trục không ghi số."


# ───────────── tiện ích vẽ ─────────────
def rich(s, size=13):
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out


def tx(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)


def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')


def circ(x, y, r, c="currentColor", sw=2, fill="none", extra=""):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}">{extra}</circle>'


def nuc(x, y, A, Z, sym, c="currentColor", size=20):
    """Kí hiệu hạt nhân: A ở trên, Z ở dưới, kí hiệu nguyên tố bên phải; (x, y) = góc trái, đường cơ sở của kí hiệu."""
    fi = round(size * 0.55)
    wi = max(len(str(A)), len(str(Z))) * fi * 0.6
    b = lbl(x + wi, y - size * 0.55, str(A), c, fi, "end", "700") + lbl(x + wi, y + size * 0.05 + fi * 0.5, str(Z), c, fi, "end", "700")
    b += lbl(x + wi + 2, y + size * 0.3, sym, c, size, "start", "700")
    return b, wi + 2 + len(sym) * size * 0.62


def anim(attr, vals, kts, T):
    v = ";".join(f"{x:.1f}" if isinstance(x, float) else str(x) for x in vals)
    k = ";".join(f"{t:.3f}" for t in kts)
    return f'<animate attributeName="{attr}" values="{v}" keyTimes="{k}" dur="{T:.2f}s" begin="indefinite" fill="freeze"/>'


def smilf(attr, vals, dur, nd=1):
    return f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def runner(pts, dur):
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
            f'{smilf("cx", [p[0] for p in pts], dur)}{smilf("cy", [p[1] for p in pts], dur)}</circle>')


def axes_t(ox, oy, wpx, apx, vlab, up=16):
    b = arrow("", "g", ox - 8, oy, ox + wpx, oy, 2) + arrow("", "g", ox, oy + 8, ox, oy - apx - up, 2)
    b += tx(ox + wpx, oy + 17, "t", GRN, 13, "end") + tx(ox + 8, oy - apx - up + 8, vlab, GRN, 13)
    return b


# ───────────── Dạng 1 · chuỗi phân rã α, β⁻, β⁻ (mô phỏng: bốn hạt nhân nối tiếp, hạt phóng ra bay lên) ─────────────
def d1(kk):
    p = f"d1{kk}"
    if kk == 0:
        T = 9.0; xs = [58, 158, 258, 358]; cy = 118; r = 21
        b = ""
        stage = [(0.8, 2.4), (3.4, 5.0), (6.0, 7.6)]
        for i, x in enumerate(xs):
            if i == 0:
                b += circ(x, cy, r, BLUE, 2.2, BLUE + "30")
            else:
                t_on = stage[i - 1][1]
                b += circ(x, cy, r, BLUE, 2.2, BLUE + "30",
                          anim("opacity", [0.25, 0.25, 1, 1], [0, t_on / T, (t_on + 0.3) / T, 1], T))
        sy, _ = nuc(xs[0] - 27, 176, 238, 92, "U", "currentColor", 20)
        b += sy + tx(xs[1], 176, "X ?", ORG, 15, "middle") + tx(xs[2], 176, "Y ?", ORG, 15, "middle") + tx(xs[3], 176, "W ?", ORG, 15, "middle")
        for i, nm in enumerate(["α", "β⁻", "β⁻"]):
            b += arrow(p, "g", xs[i] + 25, cy, xs[i + 1] - 25, cy, 2) + tx((xs[i] + xs[i + 1]) / 2, cy - 10, nm, GRN, 14, "middle")
        for i, (t0, t1) in enumerate(stage):
            x = xs[i]; ex, ey = x + 44, 34
            col, rr = (BLUE, 6.5) if i == 0 else (ORG, 4)
            kt = [0, t0 / T, t1 / T, 1]
            b += (f'<circle cx="{x}" cy="{cy}" r="{rr}" fill="{col}" stroke="currentColor" stroke-width="1.2" opacity="0">'
                  + anim("cx", [x, x, ex, ex], kt, T) + anim("cy", [cy, cy, ey, ey], kt, T)
                  + anim("opacity", [0, 0, 1, 1], [0, t0 / T, (t0 + 0.05) / T, 1], T) + "</circle>")
        b += circ(26, 204, 6.5, BLUE, 1.2, BLUE) + tx(38, 208, "tia α", "currentColor", 12, "start", "400")
        b += circ(130, 204, 4, ORG, 1.2, ORG) + tx(142, 208, "electron (tia β⁻)", "currentColor", 12, "start", "400")
        return fig("d1-0", "0 0 420 216", "Hạt nhân urani lần lượt phóng ra một hạt anpha rồi hai electron; các hạt nhân con X, Y, W chưa biết", b,
                   "Mô phỏng: mỗi lần phân rã, hạt nhân phóng một hạt bay lên rồi hạt nhân con sáng lên. Hạt nhân con ghi dấu ? vì chưa biết. Hình minh hoạ, không theo tỉ lệ.")
    b = ""
    x0s = [12, 118, 224, 330]; w = 76; y0 = 46; h = 44
    for i, x0 in enumerate(x0s):
        b += R(x0, y0, w, h, "currentColor", 2, rx=8)
        if i == 0:
            sy, wd = nuc(x0 + 12, y0 + 30, 238, 92, "U", "currentColor", 24)
            b += sy
        else:
            b += tx(x0 + w / 2, y0 + 29, "XYW"[i - 1], ORG, 22, "middle")
            b += tx(x0 + w / 2, y0 + h + 22, "A = ?", ORG, 13, "middle") + tx(x0 + w / 2, y0 + h + 42, "Z = ?", ORG, 13, "middle")
    for i, nm in enumerate(["α", "β⁻", "β⁻"]):
        xa, xb = x0s[i] + w + 3, x0s[i + 1] - 3
        b += arrow(p, "g", xa, y0 + h / 2, xb, y0 + h / 2, 2) + tx((xa + xb) / 2, y0 + h / 2 - 9, nm, GRN, 14, "middle")
    b += tx(12, 160, "Cần tìm: A, Z của X, Y, W và vị trí của W so với U", ORG, 13)
    return fig("d1-2", "0 0 420 176", "Dữ kiện: chuỗi ba phân rã bắt đầu từ urani 238, các hạt nhân con X, Y, W chưa biết", b,
               "Dữ kiện: hạt nhân mẹ và loại tia ở mỗi phân rã; các ô có dấu ? là đại lượng cần tìm. Hình minh hoạ, không theo tỉ lệ.")


# ───────────── Dạng 2 · hàm mũ N(t) (mô phỏng: điểm chạy trên đường cong, trục chia theo chu kì T) ─────────────
def d2(kk):
    p = f"d2{kk}"
    if kk == 0:
        ox, oy, wT, apx = 76, 192, 90, 152
        f = lambda x: 2 ** (-x)
        pts = [(ox + wT * x / 20, oy - apx * f(x / 20)) for x in range(0, 61)]
        b = axes_t(ox, oy, wT * 3.3, apx, "N") + poly(pts, BLUE, 2.6)
        b += tx(ox - 6, oy - apx + 4, "N₀", "currentColor", 12, "end")
        for k in (1, 2, 3):
            y = oy - apx * f(k); x = ox + wT * k
            b += seg(ox, y, x, y, GREY, 1.4, "5 4") + seg(x, y, x, oy, GREY, 1.4, "5 4") + dot(x, y, 3.5, BLUE)
            b += tx(ox - 6, y + 4, ["", "N₀/2", "N₀/4", "N₀/8"][k], "currentColor", 12, "end")
            b += tx(x, oy + 17, ["", "T", "2T", "3T"][k], "currentColor", 12, "middle")
        b += tx(ox - 6, oy + 17, "O", "currentColor", 12, "end")
        run = [(ox + wT * x / 10, oy - apx * f(x / 10)) for x in range(0, 31)]
        b += runner(run, 6.0)
        return fig("d2-0", "0 0 420 220", "Đường cong số hạt nhân còn lại N theo thời gian, trục thời gian chia theo chu kì bán rã T", b,
                   "Mô phỏng: điểm chạy trên đường cong số hạt nhân còn lại, một chu kì T ứng với 2 s mô phỏng. " + NOTE)
    b = ""
    b += R(12, 14, 190, 30, BLUE, 1.8, rx=8) + tx(107, 34, "T = 138 ngày", BLUE, 14, "middle")
    b += R(218, 14, 190, 30, BLUE, 1.8, rx=8) + tx(313, 34, "N₀ = 6,4·10¹⁸ hạt", BLUE, 14, "middle")
    b += arrow(p, "g", 20, 116, 396, 116, 2) + tx(396, 136, "t", GRN, 13, "end") + dot(20, 116, 4, "currentColor") + tx(20, 136, "0", "currentColor", 12, "middle")
    b += dot(138, 116, 5, ORG) + tx(138, 100, "t₁ = 552 ngày", ORG, 13, "middle")
    b += dot(300, 116, 5, ORG) + tx(300, 100, "t₂ = 759 ngày", ORG, 13, "middle")
    b += tx(12, 166, "Tại t₁: N = ? · đã phân rã ?%", ORG, 13) + tx(12, 188, "Tại t₂: còn lại ?%", ORG, 13)
    return fig("d2-2", "0 0 420 202", "Dữ kiện: chu kì bán rã, số hạt nhân ban đầu và hai thời điểm khảo sát t₁, t₂ trên trục thời gian", b,
               "Dữ kiện: T, N₀ và hai thời điểm t₁, t₂ của đề; các vị trí trên trục không theo tỉ lệ. Dấu ? là đại lượng cần tìm.")


# ───────────── Dạng 3 · lượng chất mẹ (mô phỏng: 24 hạt nhân phân rã ngẫu nhiên theo phân vị của định luật phóng xạ) ─────────────
def d3(kk):
    p = f"d3{kk}"
    if kk == 0:
        NN, Tm = 24, 2.0; dur = 4 * Tm                 # 1 chu kì T ứng với 2 s mô phỏng, chạy tới 4T
        order = list(range(NN)); random.Random(18).shuffle(order)   # hạt nhân nào phân rã thứ mấy
        b = ""
        for idx in range(NN):
            rank = order[idx]
            t = Tm * math.log2(1 / (1 - (rank + 0.5) / NN))   # đúng phân vị của N = N0·2^(−t/T): sau T còn đúng một nửa
            col, row = idx % 6, idx // 6
            x, y = 34 + col * 26, 34 + row * 26
            if t >= dur:
                b += f'<circle cx="{x}" cy="{y}" r="8" fill="{BLUE}" stroke="{BLUE}" stroke-width="1.5"/>'
            else:
                k0 = t / dur
                b += f'<circle cx="{x}" cy="{y}" r="8" fill="{BLUE}" stroke="{BLUE}" stroke-width="1.5"><animate attributeName="fill-opacity" values="1;1;0;0" keyTimes="0;{k0:.3f};{min(1, k0 + .01):.3f};1" dur="{dur:.0f}s" begin="indefinite" fill="freeze"/></circle>'
        bx, by, bl = 232, 70, 160
        b += R(bx, by, bl, 12, "currentColor", 1.6, rx=3)
        b += f'<rect x="{bx}" y="{by}" width="0" height="12" rx="3" fill="{GRN}">{smilf("width", [0, bl], dur)}</rect>'
        for k in range(1, 5):
            b += seg(bx + bl * k / 4, by + 12, bx + bl * k / 4, by + 20, "currentColor", 1.6) + tx(bx + bl * k / 4, by + 35, ["", "T", "2T", "3T", "4T"][k], "currentColor", 12, "middle")
        b += tx(bx, by - 10, "thời gian →", GRN, 12)
        b += circ(240, 128, 7, BLUE, 1, BLUE) + tx(254, 132, "chưa phân rã", "currentColor", 12, "start", "400")
        b += circ(240, 150, 7, BLUE, 1.4, BLUE + "1a") + tx(254, 154, "đã phân rã", "currentColor", 12, "start", "400")
        return fig("d3-0", "0 0 420 170", "Hai mươi bốn hạt nhân của một mẫu minh hoạ phân rã dần, thanh thời gian chia theo chu kì T", b,
                   "Mô phỏng: mẫu minh hoạ 24 hạt nhân, một chu kì T ứng với 2 s mô phỏng; thời điểm mỗi hạt phân rã tính từ định luật phóng xạ (khác chất trong đề). Hình minh hoạ.")
    b = ""
    bx, by, bw = 22, 48, 360
    pw = bw * 56 / 64
    b += tx(bx, by - 14, "m₀ = 64 μg (lúc đầu)", BLUE, 14)
    b += R(bx, by, pw, 28, ORG, 2, ORG + "30") + R(bx + pw, by, bw - pw, 28, BLUE, 2, "none", dash="5 4")
    b += tx(bx + pw / 2, by + 19, "đã phân rã: 56 μg", ORG, 13, "middle") + tx(bx + pw + (bw - pw) / 2, by + 52, "còn lại: ?", BLUE, 13, "middle")
    b += arrow(p, "g", bx, by + 62, bx + bw, by + 62, 2) + tx(bx + bw, by + 82, "t", GRN, 13, "end") + dot(bx, by + 62, 4, "currentColor")
    b += dot(bx + pw, by + 62, 5, ORG) + tx(bx + pw, by + 82, "24 ngày", ORG, 13, "middle")
    b += tx(bx, by + 118, "T = ?   ·   sau 40 ngày: m = ?   ·   thời gian để m < 0,1 μg: ?", ORG, 13)
    return fig("d3-2", "0 0 420 186", "Dữ kiện: khối lượng iốt-131 ban đầu 64 microgam, sau 24 ngày đã phân rã 56 microgam", b,
               "Dữ kiện: phần cam là khối lượng đã phân rã sau 24 ngày, vẽ đúng tỉ lệ với 64 μg; phần nét đứt là khối lượng còn lại cần tìm.")


# ───────────── Dạng 4 · độ phóng xạ H (mô phỏng: kim đồng hồ đo H giảm theo hàm mũ, mẫu minh hoạ chạy 3T) ─────────────
def d4(kk):
    p = f"d4{kk}"
    if kk == 0:
        cx, cy, Rr = 130, 138, 92
        b = f'<path d="M{cx - Rr},{cy} A{Rr},{Rr} 0 0 1 {cx + Rr},{cy}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
        for k in range(11):
            a = math.radians(180 - 18 * k)
            b += seg(cx + Rr * math.cos(a), cy - Rr * math.sin(a), cx + (Rr - 9) * math.cos(a), cy - (Rr - 9) * math.sin(a), "currentColor", 1.8)
        b += tx(cx - Rr, cy + 18, "0", "currentColor", 13, "middle") + tx(cx + Rr, cy + 18, "H₀", "currentColor", 13, "middle") + tx(cx, cy - 36, "H", GRN, 15, "middle")
        dur = 6.0; n = 30
        vals = [-180 * (1 - 2 ** (-3 * k / n)) for k in range(n + 1)]
        b += (f'<g><animateTransform attributeName="transform" type="rotate" values="{";".join(f"{v:.1f} {cx} {cy}" for v in vals)}" dur="{dur:.1f}s" begin="indefinite" fill="freeze"/>'
              + seg(cx, cy, cx + Rr - 14, cy, RED, 3) + '</g>')
        b += circ(cx, cy, 6, "currentColor", 2, "currentColor")
        b += R(262, 56, 138, 82, "currentColor", 2.4, rx=6, fill="none") + R(290, 76, 82, 42, GREY, 2, GREY + "30", rx=4)
        b += tx(331, 102, "Co-60", "currentColor", 14, "middle") + tx(331, 156, "nguồn trong hộp chì", "currentColor", 12, "middle", "400")
        for k in range(3):
            b += arrow(p, "o", 262 + 0, 70 + k * 30, 232 - 0, 54 + k * 38, 1.6)
        return fig("d4-0", "0 0 420 180", "Đồng hồ đo độ phóng xạ H của một nguồn: kim quay dần về phía vạch không", b,
                   "Mô phỏng: kim tụt dần trong 3 chu kì (một chu kì ứng với 2 s mô phỏng); thang chia đều không ghi số, nguồn minh hoạ khác đề. Hình minh hoạ.")
    b = ""
    b += R(20, 40, 100, 96, "currentColor", 2.4, rx=6) + R(40, 66, 60, 44, GREY, 2, GREY + "30", rx=4)
    b += tx(70, 94, "Co-60", "currentColor", 14, "middle") + tx(70, 30, "m = 4,0 g", BLUE, 13, "middle")
    b += tx(150, 52, "T = 5,27 năm", BLUE, 13) + tx(150, 74, "1 năm = 365 ngày", "currentColor", 12, "start", "400")
    b += tx(150, 108, "N₀ = ?   ·   λ = ?", ORG, 13) + tx(150, 130, "H₀ = ? Bq = ? Ci", ORG, 13) + tx(150, 152, "t = 10,54 năm: H = ? Ci", ORG, 13)
    return fig("d4-2", "0 0 420 172", "Dữ kiện: nguồn coban-60 khối lượng 4,0 gam, chu kì bán rã 5,27 năm", b,
               "Dữ kiện: khối lượng, chu kì bán rã và thời điểm khảo sát của đề; dấu ? là đại lượng cần tìm. Hình minh hoạ, không theo tỉ lệ.")


# ───────────── Dạng 5 · định tuổi bằng carbon-14 (mô phỏng: cây chết rồi H riêng giảm; mẫu MINH HOẠ khác đề) ─────────────
def d5(kk):
    p = f"d5{kk}"
    if kk == 0:
        ox, oy, apx, wT = 56, 176, 118, 92
        xd = ox + 78
        n_show = 1.2                                      # mẫu minh hoạ: cổ 1,2 chu kì (khác đề)
        f = lambda x: 2 ** (-x)
        b = axes_t(ox, oy, 330, apx, "h")
        b += seg(ox, oy - apx, xd, oy - apx, BLUE, 2.6) + poly([(xd + wT * x / 20, oy - apx * f(x / 20)) for x in range(0, 53)], BLUE, 2.6)
        b += seg(xd, oy - apx - 8, xd, oy + 6, GREY, 1.6, "5 4") + tx(xd, oy + 20, "cây chết (t = 0)", "currentColor", 12, "middle")
        b += tx(ox - 6, oy - apx + 4, "h₀", "currentColor", 12, "end") + tx(ox + 26, oy - apx - 8, "cây sống: h₀ = 0,226 Bq/g", BLUE, 12)
        xe, ye = xd + wT * n_show, oy - apx * f(n_show)
        b += seg(ox, ye, xe, ye, GREY, 1.4, "5 4") + seg(xe, ye, xe, oy, GREY, 1.4, "5 4")
        b += tx(ox - 6, ye + 4, "h = ?", ORG, 12, "end")
        b += arrow(p, "o", xd, oy + 34, xe, oy + 34, 1.8) + arrow(p, "o", xe, oy + 34, xd, oy + 34, 1.8) + tx((xd + xe) / 2, oy + 53, "tuổi t = ?", ORG, 13, "middle")
        run = [(xd + wT * n_show * k / 24, oy - apx * f(n_show * k / 24)) for k in range(25)]
        b += runner(run, 5.0)
        return fig("d5-0", "0 0 420 238", "Độ phóng xạ riêng của carbon-14 không đổi khi cây sống, rồi giảm dần từ lúc cây chết", b,
                   "Mô phỏng: điểm chạy từ lúc cây chết tới lúc đo; h là độ phóng xạ riêng (Bq trên mỗi gam carbon). Mẫu minh hoạ khác đề, trục thời gian không chia vạch.")
    b = ""
    b += R(14, 40, 180, 78, BLUE, 2, rx=8) + tx(104, 64, "cây còn sống", BLUE, 14, "middle")
    b += tx(104, 88, "mỗi gam carbon:", "currentColor", 13, "middle", "400") + tx(104, 108, "0,226 Bq", "currentColor", 14, "middle")
    b += R(226, 40, 180, 78, ORG, 2, rx=8) + tx(316, 64, "mẩu than gỗ cổ", ORG, 14, "middle")
    b += tx(316, 88, "5,0 g carbon:", "currentColor", 13, "middle", "400") + tx(316, 108, "đo được 0,360 Bq", "currentColor", 14, "middle")
    b += tx(14, 150, "T = 5730 năm · tuổi mẫu t = ?", ORG, 13)
    return fig("d5-2", "0 0 420 166", "Dữ kiện: độ phóng xạ của carbon-14 trên mỗi gam carbon ở cây sống và độ phóng xạ đo được của mẩu than gỗ cổ", b,
               "Dữ kiện: hai số đo ở hai khối lượng carbon khác nhau; dấu ? là đại lượng cần tìm. Hình minh hoạ, không theo tỉ lệ.")
