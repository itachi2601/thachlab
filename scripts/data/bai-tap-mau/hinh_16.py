"""Hình cho bài tập mẫu Bài 15 (Vật lí 12) "Năng lượng liên kết hạt nhân", lesson_id 16.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng chỉ vẽ cấu trúc (nuclôn, thanh khối lượng) từ số liệu của đề, không ghi đáp số; mọi đại lượng cần tìm ghi "?"."""
import math, os, random, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def rich(s, size=13):
    """`E_lkr` → E với chỉ số dưới lkr."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def op_anim(vals, keys, dur):
    return (f'<animate attributeName="opacity" values="{";".join(str(v) for v in vals)}" keyTimes="{";".join(str(k) for k in keys)}" '
            f'dur="{dur}s" begin="indefinite" fill="freeze"/>')

def cluster(n, cx, cy, d):
    """n điểm xếp lưới lục giác bước d, gần tâm (cx,cy) nhất."""
    pts = [(i * d + j * d / 2, j * d * 0.866) for i in range(-8, 9) for j in range(-8, 9)]
    pts.sort(key=lambda p: (round(math.hypot(*p), 3), p[1], p[0]))
    pts = pts[:n]
    mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
    return [(cx + x - mx, cy + y - my) for x, y in pts]

def nucleon(x, y, r, c):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1"/>'

def moving(p0, p1, r, c, dur):
    return (f'<circle cx="{p0[0]:.1f}" cy="{p0[1]:.1f}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1">'
            f'{smil("cx", [p0[0], p1[0]], dur)}{smil("cy", [p0[1], p1[1]], dur)}</circle>')

def legend(x, y):
    return (nucleon(x, y, 5.5, RED) + txt(x + 11, y + 4, "prôtôn", "currentColor", 12, "start", "400")
            + nucleon(x + 78, y, 5.5, BLUE) + txt(x + 89, y + 4, "nơtron", "currentColor", 12, "start", "400"))

def colors(n):
    """Tên màu xen kẽ prôtôn / nơtron theo đúng số lượng: trả danh sách n màu, nửa đầu theo thứ tự xen kẽ."""
    return [RED if i % 2 == 0 else BLUE for i in range(n)]


# ───────────── Dạng 1 · N-14 từ 7 prôtôn + 7 nơtron, m_X = 13,999231 u ─────────────
def d1(kk):
    anim = kk == 0
    cl = cluster(14, 290, 112, 15); col = colors(14); rnd = random.Random(5)
    b = legend(16, 24)
    b += txt(16, 48, "7 prôtôn + 7 nơtron", "currentColor", 13) + txt(16, 66, "tạo thành hạt nhân N-14", "currentColor", 13)
    b += txt(16, 186, "m_X = 13,999231 u", "currentColor", 13)
    b += txt(250, 24, "Δm = ?", ORG, 13) + txt(330, 24, "E_lk = ?", ORG, 13)
    if anim:
        for i in range(14):
            st = (rnd.uniform(26, 160), rnd.uniform(84, 170))
            b += moving(st, cl[i], 6.5, col[i], 4)
        wave = [(340 + k * 2.2, 112 - 14 * math.sin(k * 0.55)) for k in range(30)]
        b += f'<g opacity="0">{op_anim([0, 0, 1], [0, 0.75, 1], 4)}{poly(wave, ORG, 2.2)}</g>'
        b += f'<g opacity="0">{op_anim([0, 0, 1], [0, 0.75, 1], 4)}{txt(372, 86, "γ", ORG, 15, "middle")}</g>'
        return fig("d1-0", "0 0 420 200", "Bảy prôtôn và bảy nơtron rời bay vào nhau tạo hạt nhân nitơ 14, có tia gamma phát ra",
                   b, "Mô phỏng: 14 nuclôn rời kết hợp thành hạt nhân trong 4 s, cuối cùng có bức xạ γ phát ra. " + NOTE)
    for i in range(14):
        b += nucleon(cl[i][0], cl[i][1], 6.5, col[i])
    return fig("d1-2", "0 0 420 200", "Dữ kiện: hạt nhân nitơ 14 gồm bảy prôtôn và bảy nơtron, khối lượng hạt nhân cho trước", b,
               "Dữ kiện: số prôtôn, số nơtron và khối lượng hạt nhân. " + NOTE)


# ───────────── Dạng 2 · Ne-20 bị tách thành 20 nuclôn rời; m_X = 19,986950 u ─────────────
def d2(kk):
    anim = kk == 0
    cx, cy = 140, 100
    cl = cluster(20, cx, cy, 14); col = colors(20)
    b = ""
    if anim:
        for i in range(20):
            x, y = cl[i]
            end = (cx + (x - cx) * 3.7 + 6 * math.cos(i), cy + (y - cy) * 1.9 + 4 * math.sin(2 * i))
            b += moving((x, y), end, 6, col[i], 4.5)
    else:
        for i in range(20):
            b += nucleon(cl[i][0], cl[i][1], 6, col[i])
    b += legend(16, 24)
    b += txt(290, 60, "Hạt nhân Ne-20", "currentColor", 13) + txt(290, 80, "10 prôtôn + 10 nơtron", "currentColor", 12, "start", "400")
    b += txt(290, 100, "m_X = 19,986950 u", "currentColor", 12, "start", "400") + txt(290, 130, "E_lkr = ?", ORG, 14)
    if anim:
        return fig("d2-0", "0 0 420 200", "Hạt nhân neon 20 bị tách dần thành hai mươi nuclôn rời", b,
                   "Mô phỏng: hạt nhân bị tách thành 20 nuclôn rời trong 4,5 s. " + NOTE)
    # hình dữ kiện: thang năng lượng liên kết riêng với hai mốc đã biết, Ne-20 chưa biết
    b = legend(16, 24)
    X = lambda v: 36 + 34 * v
    b += seg(X(0), 120, X(10), 120, "currentColor", 2.4)
    for v in range(0, 11, 2):
        b += seg(X(v), 114, X(v), 126, "currentColor", 1.6) + txt(X(v), 142, str(v), "currentColor", 12, "middle", "400")
    b += txt(X(10) + 2, 160, "MeV/nuclôn", "currentColor", 12, "end", "400")
    b += seg(X(7.07), 120, X(7.07), 84, GRN, 2) + dot(X(7.07), 120, 4.5, GRN) + txt(X(7.07), 76, "He-4: 7,07", GRN, 12, "middle")
    b += seg(X(8.79), 120, X(8.79), 54, ORG, 2) + dot(X(8.79), 120, 4.5, ORG) + txt(X(8.79), 46, "Fe-56: 8,79", ORG, 12, "middle")
    b += txt(16, 74, "Ne-20: ?", BLUE, 14)
    return fig("d2-2", "0 0 420 200", "Dữ kiện: thang năng lượng liên kết riêng với mốc heli 4 là 7,07 và sắt 56 là 8,79 mega electron vôn trên nuclôn",
               b, "Dữ kiện: hai mốc đã biết trên thang MeV/nuclôn; vị trí của neon chưa biết. Thang vẽ đúng tỉ lệ.")


# ───────────── Dạng 3 · bốn hạt nhân, E_lk cho trước, thanh dài tỉ lệ E_lk ─────────────
def d3(kk):
    anim = kk == 0
    rows = [("Be-9", 9, 58.16), ("Ne-20", 20, 160.64), ("Sr-90", 90, 782.63), ("Pb-208", 208, 1636.43)]
    K = 0.07; x0 = 112          # 0,07 px / MeV
    b = txt(16, 24, "Thanh dài tỉ lệ E_lk", "currentColor", 12, "start", "400")
    for i, (nm, A, E) in enumerate(rows):
        y = 44 + i * 36; w = K * E
        b += txt(16, y + 17, nm, "currentColor", 14) + txt(60, y + 17, f"A = {A}", "currentColor", 12, "start", "400")
        if anim:
            b += f'<rect x="{x0}" y="{y}" width="1" height="24" rx="3" fill="{BLUE}" opacity=".85">{smil("width", [1, w], 4)}</rect>'
        else:
            b += f'<rect x="{x0}" y="{y}" width="{w:.1f}" height="24" rx="3" fill="{BLUE}" opacity=".85"/>'
        b += txt(x0 + w + 6 if w < 150 else x0 + w - 6, y + 17, f"{E:.2f}".replace(".", ",") + " MeV", "currentColor" if w < 150 else "#0f172a", 12, "start" if w < 150 else "end")
    b += txt(330, 24, "E_lkr = ?", ORG, 13)
    cap = "Thanh dài tỉ lệ với năng lượng liên kết của mỗi hạt nhân (1 px ≈ 14 MeV)."
    if anim:
        return fig("d3-0", "0 0 420 200", "Bốn hạt nhân với thanh biểu diễn năng lượng liên kết dài dần", b, "Mô phỏng: bốn thanh dài dần trong 4 s. " + cap)
    return fig("d3-2", "0 0 420 200", "Dữ kiện: bốn hạt nhân, số khối và năng lượng liên kết của từng hạt nhân", b, "Dữ kiện: số khối và năng lượng liên kết cho trước. " + cap)


# ───────────── Dạng 4 · nguyên tử Ca-40, 20 êlectron, m_nguyên tử = 39,962591 u ─────────────
def d4(kk):
    anim = kk == 0
    cx, cy = 130, 100
    shells = [(30, 2, 5, 1), (48, 8, 8, -1), (66, 8, 11, 1), (84, 2, 14, -1)]
    b = ""
    for r, n, T, sgn in shells:
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GREY}" stroke-width="1" stroke-dasharray="3 4"/>'
        dots_ = "".join(f'<circle cx="{cx + r * math.cos(2 * math.pi * k / n):.1f}" cy="{cy + r * math.sin(2 * math.pi * k / n):.1f}" r="3.6" fill="{BLUE}"/>' for k in range(n))
        if anim:
            b += (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};{sgn * 360} {cx} {cy}" '
                  f'dur="{T}s" begin="indefinite" fill="freeze"/>{dots_}</g>')
        else:
            b += f"<g>{dots_}</g>"
    b += f'<circle cx="{cx}" cy="{cy}" r="14" fill="{RED}" stroke="currentColor" stroke-width="1.4"/>'
    b += txt(cx, cy + 4, "Ca-40", "#0f172a", 9, "middle")
    b += txt(240, 52, "Nguyên tử Ca-40", "currentColor", 13) + txt(240, 72, "m_nt = 39,962591 u", "currentColor", 12, "start", "400")
    b += txt(240, 92, "nguyên tử Ca-40", "currentColor", 12, "start", "400")
    b += txt(240, 124, "Δm = ?", ORG, 13) + txt(240, 144, "E_lk = ?   E_lkr = ?", ORG, 13)
    if anim:
        return fig("d4-0", "0 0 420 200", "Nguyên tử canxi 40: hạt nhân ở giữa, hai mươi êlectron chuyển động trên bốn lớp quanh hạt nhân", b,
                   "Mô phỏng: êlectron quay quanh hạt nhân (một vòng mỗi lớp, tốc độ khác nhau). Êlectron vẽ rất to so với thực tế. " + NOTE)
    return fig("d4-2", "0 0 420 200", "Dữ kiện: nguyên tử canxi 40 gồm hạt nhân và hai mươi êlectron; khối lượng cho trước là khối lượng cả nguyên tử", b,
               "Dữ kiện: khối lượng đề cho là của cả nguyên tử. " + NOTE)


# ───────────── Dạng 5 · bài ngược: Kr-84, E_lkr = 8,72 MeV/nuclôn, cần Δm và m_X ─────────────
def d5(kk):
    anim = kk == 0
    x0, W, WS = 40, 330, 302          # độ chênh vẽ phóng đại
    b = txt(x0, 30, "Tổng khối lượng nuclôn rời : ?", "currentColor", 13)
    b += f'<rect x="{x0}" y="38" width="{W * 36 / 84:.1f}" height="26" fill="{RED}" opacity=".9"/><rect x="{x0 + W * 36 / 84:.1f}" y="38" width="{W * 48 / 84:.1f}" height="26" fill="{BLUE}" opacity=".9"/>'
    b += txt(x0 + 6, 56, "36 p", "#0f172a", 12) + txt(x0 + W * 36 / 84 + 6, 56, "48 n", "#0f172a", 12)
    b += txt(x0, 98, "Hạt nhân Kr-84 : m_X = ?", "currentColor", 13)
    if anim:
        b += f'<rect x="{x0}" y="106" width="{W}" height="26" fill="{GRN}" opacity=".9">{smil("width", [W, WS], 3.5)}</rect>'
        b += (f'<rect x="{x0 + WS}" y="106" width="{W - WS}" height="26" fill="none" stroke="{ORG}" stroke-width="2" stroke-dasharray="4 3" opacity="0">'
              f'{op_anim([0, 0, 1], [0, 0.8, 1], 3.5)}</rect>')
        b += f'<g opacity="0">{op_anim([0, 0, 1], [0, 0.8, 1], 3.5)}{txt(x0 + WS + (W - WS) / 2, 150, "Δm = ?", ORG, 13, "middle")}</g>'
    else:
        b += f'<rect x="{x0}" y="106" width="{WS}" height="26" fill="{GRN}" opacity=".9"/>'
        b += f'<rect x="{x0 + WS}" y="106" width="{W - WS}" height="26" fill="none" stroke="{ORG}" stroke-width="2" stroke-dasharray="4 3"/>'
        b += txt(x0 + WS + (W - WS) / 2, 150, "Δm = ?", ORG, 13, "middle")
    b += txt(x0, 186, "Cho: E_lkr = 8,72 MeV/nuclôn", "currentColor", 13)
    if anim:
        return fig("d5-0", "0 0 420 200", "Thanh khối lượng hạt nhân kripton ngắn lại so với thanh tổng khối lượng nuclôn rời, phần hụt hiện ra", b,
                   "Mô phỏng: so hai khối lượng trong 3,5 s. Độ chênh vẽ phóng đại nhiều lần so với thực tế. " + NOTE)
    return fig("d5-2", "0 0 420 200", "Dữ kiện: hạt nhân kripton 84 gồm 36 prôtôn và 48 nơtron, cho trước năng lượng liên kết riêng", b,
               "Dữ kiện: số p, số n và năng lượng liên kết riêng cho trước; hai khối lượng chưa biết. Độ chênh vẽ phóng đại. " + NOTE)


# ───────────── Dạng 6 · 3,0 g C-12, Δm = 0,098940 u → năng lượng cả lượng chất, so với than ─────────────
def d6(kk):
    anim = kk == 0
    rnd = random.Random(11)
    bx, by, bw, bh = 24, 52, 150, 100
    b = R(bx, by, bw, bh, sw=2.4, rx=10)
    b += txt(bx, 36, "3,0 g cacbon-12", "currentColor", 13) + txt(bx, 176, "N hạt nhân = ?", ORG, 13)
    for i in range(24):
        x = rnd.uniform(bx + 12, bx + bw - 12); y = rnd.uniform(by + 12, by + bh - 12)
        if anim:
            t = round(rnd.uniform(0.15, 0.9), 2)
            b += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5.5" fill="{GREY}"><animate attributeName="fill" values="{GREY};{ORG};{ORG}" keyTimes="0;{t};1" '
                  f'calcMode="discrete" dur="4s" begin="indefinite" fill="freeze"/></circle>')
        else:
            b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5.5" fill="{GREY}"/>'
    # thanh năng lượng (không ghi số)
    ex, ey, eh = 250, 52, 100
    b += R(ex, ey, 40, eh, sw=2.2, rx=4)
    if anim:
        b += f'<rect x="{ex + 2}" y="{ey + eh - 2}" width="36" height="1" fill="{ORG}">{smil("y", [ey + eh - 2, ey + 22], 4)}{smil("height", [1, eh - 24], 4)}</rect>'
    else:
        b += txt(ex + 20, ey + 56, "?", ORG, 22, "middle")
    b += txt(ex + 20, 36, "E toả ra = ?", ORG, 13, "middle") + txt(ex + 20, 176, "so với than đá", "currentColor", 12, "middle", "400")
    b += txt(310, 80, "Δm = 0,098940 u", "currentColor", 12, "start", "400") + txt(310, 100, "(mỗi hạt nhân)", "currentColor", 12, "start", "400")
    b += txt(310, 124, "q than = 2,9·10⁷ J/kg", "currentColor", 12, "start", "400")
    if anim:
        return fig("d6-0", "0 0 420 200", "Các hạt nhân cacbon 12 trong mẫu lần lượt tạo thành, thanh năng lượng toả ra dâng dần", b,
                   "Mô phỏng: mẫu 3,0 g, từng hạt nhân (rút gọn còn 24 chấm) lần lượt tạo thành trong 4 s, thanh năng lượng dâng lên. " + NOTE)
    return fig("d6-2", "0 0 420 200", "Dữ kiện: mẫu ba gam cacbon 12, độ hụt khối mỗi hạt nhân và năng suất toả nhiệt của than", b,
               "Dữ kiện: khối lượng mẫu, Δm của một hạt nhân, năng suất toả nhiệt của than. " + NOTE)
