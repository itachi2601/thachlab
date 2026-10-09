"""Bài 24 · Bài 5. Động năng. Thế năng. Sự chuyển hoá giữa động năng và thế năng trong dao động điều hoà
(Vật lí 11, chương 1 Dao động) — dựng file scripts/data/bai-tap-mau/24.json từ đầu (bài chưa có dạng cũ, không có tu_luan).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-24.py        (mẫu cấu trúc: build-hinh-57.py, đồ thị/sóng: build-hinh-33.py)

Quy ước theo lý thuyết bài 24: mốc thế năng tại VTCB · Et = ½kx² = ½mω²x² · Ed = ½mv² = ½k(A²−x²) · W = Et + Ed = ½kA² (không phụ thuộc m)
· Et, Ed biến thiên tần số góc 2ω, chu kì T/2, ngược pha · Ed = n·Et ⇒ x = ±A/√(n+1) · Ed = Et tại x = ±A/√2 (4 lần/chu kì) · ω = √(k/m).
Màu: Et cam · Ed xanh dương · W xanh lá (đúng hình 2, 3 của bài lý thuyết).

QUÉT SỐ DẠNG (bước 0, tự làm trong đầu từ lý thuyết bài + question-topics.json; ngân hàng bị RLS với anon nên không đếm được số câu):
chủ đề con của bài (question-topics.json, lesson_id 24): 160 «Động năng, thế năng của vật dao động» · 161 «Bảo toàn cơ năng trong dao động điều hoà».
5 dạng, cấp không giảm:
  1 (cấp 1, topic 160) Cơ năng, thế năng, động năng, tốc độ tại một li độ — nền tảng, áp dụng trực tiếp W = ½kA², Et = ½kx², Ed = W − Et.
  2 (cấp 2, topic 160) Động năng bằng n lần thế năng: tìm |x|, |v|, số lần/chu kì — thêm điều kiện W = (n+1)Et (bẫy A/√2 và A/2).
  3 (cấp 2, topic 161) Biết x và v cùng lúc → W = Et + Ed → A, v_max — thêm đổi đơn vị cm, cm/s và bảo toàn cơ năng (A chưa biết).
  4 (cấp 3, topic 160) Chu kì của năng lượng T/2, khoảng giữa hai lần Ed = Et, Ed theo thời gian khi thả từ biên — kết hợp nhiều bước.
  5 (cấp 4, topic 161) Đọc đồ thị Ed(x) → W, A, k, v_max, li độ khi Ed cho trước — tình huống mới (dữ kiện nằm trong đồ thị).
Không đưa vào: va chạm, ma sát, con lắc đơn, lò xo treo đứng (ngoài bài hoặc chưa có trong lý thuyết bài này)."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "24.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
PI = math.pi
FLOOR, BH, BW = 150, 36, 40          # mặt sàn, chiều cao và bề rộng vật
VB = "0 0 420 200"


# ───────────── helper hình ─────────────
def rich(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: viết E_{t} → E với t nhỏ, hạ xuống."""
    out, after = "", False
    for part in re.split(r"(_\{.*?\})", s):
        if part.startswith("_{"):
            out += f'<tspan dy="4" font-size="{size - 3}">{part[2:-1]}</tspan>'; after = True
        elif part:
            out += f'<tspan dy="-4">{part}</tspan>' if after else part
            after = False
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{out}</text>'


def smil_s(attr, vals, dur):
    return f'<animate attributeName="{attr}" values="{";".join(vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def spring(x1, x0=24, y=FLOOR - BH / 2, n=8, amp=8, lead=6):
    pts = [(x0, y), (x0 + lead, y)]
    L = (x1 - lead) - (x0 + lead)
    for i in range(n):
        pts.append((x0 + lead + L * (i + .5) / n, y + (amp if i % 2 == 0 else -amp)))
    pts += [(x1 - lead, y), (x1, y)]
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)


def wall():
    return f'<rect x="14" y="{FLOOR - 62}" width="10" height="62" fill="none" stroke="currentColor" stroke-width="2.2"/>'


def block_static(Xc, up):
    bx = Xc + up - BW / 2
    return (f'<polyline fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" points="{spring(bx)}"/>'
            f'<rect x="{bx:.1f}" y="{FLOOR - BH}" width="{BW}" height="{BH}" fill="none" stroke="currentColor" stroke-width="2.4"/>')


def block_anim(Xc, ups, dur):
    rx = [Xc + u - BW / 2 for u in ups]; pts = [spring(x) for x in rx]
    return (f'<polyline fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" points="{pts[0]}">{smil_s("points", pts, dur)}</polyline>'
            f'<rect x="{rx[0]:.1f}" y="{FLOOR - BH}" width="{BW}" height="{BH}" fill="none" stroke="currentColor" stroke-width="2.4">{smil("x", rx, dur)}</rect>')


def ruler(marks):
    b = ""
    for px, txt, c in marks:
        b += seg(px, FLOOR + 8, px, FLOOR + 18, c, 2) + lbl(px, FLOOR + 34, txt, c, 12, "middle", "700")
    return b


def samples(w, ncyc=2, per=24):
    T = 2 * PI / w
    return T, [i * T / per for i in range(ncyc * per + 1)]


def bars(x0, hpx, ts, w, dur):
    """Hai cột Et (cam), Ed (xanh): chiều cao tỉ lệ năng lượng, tổng luôn bằng hpx (= W)."""
    out = seg(x0 - 8, FLOOR, x0 + 62, FLOOR, "currentColor", 1.6)
    for xb, f, c in ((x0, lambda t: math.cos(w * t) ** 2, ORG), (x0 + 34, lambda t: math.sin(w * t) ** 2, BLUE)):
        hs = [hpx * f(t) for t in ts]; ys = [FLOOR - h for h in hs]
        out += (f'<rect x="{xb}" y="{ys[0]:.1f}" width="22" height="{hs[0]:.1f}" fill="{c}" fill-opacity=".8" stroke="{c}" stroke-width="1.5">'
                f'{smil("y", ys, dur)}{smil("height", hs, dur)}</rect>')
    out += rich(x0 + 11, FLOOR + 20, "E_{t}", ORG, 13, "middle") + rich(x0 + 45, FLOOR + 20, "E_{d}", BLUE, 13, "middle")
    return out


# ═════════════ Dạng 1 · cơ năng, Et, Ed, tốc độ tại x = 6 cm: k = 50 N/m, m = 0,5 kg, A = 10 cm ═════════════
K1, M1, A1, X1 = 50.0, 0.5, 0.10, 0.06
W1 = math.sqrt(K1 / M1)
XC1, S1 = 205, 11.5          # px/cm


def d1(k):
    p = f"d1{k}"
    xm = XC1 + S1 * 6
    if k == 0:
        T, ts = samples(W1)
        dur = 4 * ts[-1]        # chạy chậm 4 lần
        ups = [S1 * 10 * math.cos(W1 * t) for t in ts]
        b = defs(p) + wall() + ground(FLOOR, 24, 410)
        b += seg(xm, 92, xm, FLOOR, ORG, 1.6, "5 4") + lbl(xm, 86, "x = 6,0 cm", ORG, 13, "middle", "700")
        b += block_anim(XC1, ups, dur)
        b += ruler([(XC1 - S1 * 10, "−A", "currentColor"), (XC1, "O", "currentColor"), (XC1 + S1 * 10, "A = 10 cm", "currentColor")])
        b += rich(40, 30, "Cần tìm: W, E_{t}, E_{d}, |v|", "currentColor", 13, "start")
        return fig("d1-0", VB, "Con lắc lò xo nằm ngang, kéo vật ra 10 cm rồi thả; vật dao động quanh vị trí cân bằng O, có đánh dấu li độ 6 cm", b,
                   "Mô phỏng: kéo ra biên độ A rồi thả (chạy chậm 4 lần, 2 chu kì). Chuyển động tính theo công thức. Vạch cam: li độ x = 6,0 cm.")
    b = defs(p) + wall() + ground(FLOOR, 24, 410) + block_static(XC1, S1 * 6)
    b += seg(XC1, 66, XC1, FLOOR, "currentColor", 1.2, "4 4", .6)
    b += dim(p, "o", XC1, 72, XC1 + S1 * 10, 72, "", 0, 0) + lbl(XC1 + S1 * 5, 64, "A", ORG, 13, "middle", "700")
    b += dim(p, "b", XC1, 98, xm, 98, "", 0, 0) + lbl(XC1 + S1 * 3, 90, "x", BLUE, 13, "middle", "700")
    b += seg(XC1 + S1 * 10, 66, XC1 + S1 * 10, 80, ORG, 1.2, "4 4", .8) + seg(xm, 92, xm, FLOOR - BH, BLUE, 1.2, "4 4", .8)
    b += ruler([(XC1, "O", "currentColor")])
    b += rich(40, 30, "W = ½kA²", GRN) + rich(40, 50, "E_{t} = ½kx²", ORG) + rich(40, 70, "E_{d} = W − E_{t}", BLUE)
    return fig("d1-2", VB, "Biên độ A và li độ x đo từ vị trí cân bằng O; từ A tính cơ năng, từ x tính thế năng", b, "Dữ kiện: A và x đều đo từ VTCB. " + NOTE)


# ═════════════ Dạng 2 · Ed = 8Et: m = 0,25 kg, k = 25 N/m (ω = 10), A = 12 cm ═════════════
K2, M2, A2 = 25.0, 0.25, 0.12
W2 = math.sqrt(K2 / M2)
XC2, AP2 = 190, 100


def d2(k):
    p = f"d2{k}"
    if k == 0:
        T, ts = samples(W2)
        dur = 4 * ts[-1]
        ups = [AP2 * math.cos(W2 * t) for t in ts]
        xend = XC2 + AP2 + BW / 2 + 16
        b = defs(p) + wall() + ground(FLOOR, 24, xend) + block_anim(XC2, ups, dur)
        b += ruler([(XC2 - AP2, "−A", "currentColor"), (XC2, "O", "currentColor"), (XC2 + AP2, "A = 12 cm", "currentColor")])
        b += bars(xend + 22, 80, ts, W2, dur)
        b += rich(40, 30, "Tại lúc E_{d} = 8E_{t}:", "currentColor", 13) + lbl(40, 52, "|x| = ?     |v| = ?", RED, 13, "start", "700")
        return fig("d2-0", VB, "Con lắc lò xo nằm ngang dao động với biên độ 12 cm; hai cột bên phải là thế năng và động năng, tổng chiều cao không đổi", b,
                   "Mô phỏng: hai cột cam (thế năng) và xanh (động năng) đổi chỗ cho nhau, tổng luôn là W (chạy chậm 4 lần, 2 chu kì). Tính theo công thức.")
    X0, SA, YB, HW = 210, 150, 170, 110
    us = [i / 20 for i in range(-20, 21)]
    b = defs(p) + seg(50, YB, 372, YB, "currentColor", 1.6) + seg(X0, YB, X0, 44, "currentColor", 1.2, "4 4", .5)
    b += poly([(X0 + SA * u, YB - HW * u * u) for u in us], ORG, 2.6) + poly([(X0 + SA * u, YB - HW * (1 - u * u)) for u in us], BLUE, 2.6)
    b += seg(60, YB - HW, 360, YB - HW, GRN, 2, "6 4") + lbl(52, YB - HW + 5, "W", GRN, 13, "end", "700")
    for px, txt in ((X0 - SA, "−A"), (X0, "O"), (X0 + SA, "A")):
        b += seg(px, YB, px, YB + 6, "currentColor", 1.6) + lbl(px, YB + 22, txt, "currentColor", 12, "middle", "700")
    b += lbl(378, YB + 5, "x", "currentColor", 13, "start", "700")
    b += rich(X0 + 30, YB - 14, "E_{t}", ORG, 13, "start") + rich(X0 - SA * .9 - 6, YB - HW * .19 - 8, "E_{d}", BLUE, 13, "end")
    b += rich(X0, 28, "W = E_{t} + E_{d}", GRN, 13, "middle")
    return fig("d2-2", "0 0 420 196", "Hai parabol thế năng và động năng theo li độ; tổng của chúng ở mọi li độ bằng cơ năng W", b, "Dữ kiện: ở mọi li độ, thế năng cộng động năng luôn bằng cơ năng W. " + NOTE)


# ═════════════ Dạng 3 · x = 3,0 cm, |v| = 40 cm/s, m = 0,25 kg, k = 25 N/m (A chưa biết) ═════════════
K3, M3 = 25.0, 0.25
W3 = math.sqrt(K3 / M3)
XC3, AP3 = 190, 100


def d3(k):
    p = f"d3{k}"
    if k == 0:
        T, ts = samples(W3)
        dur = 4 * ts[-1]
        ups = [AP3 * math.cos(W3 * t) for t in ts]
        xm = XC3 + AP3 * .5
        b = defs(p) + wall() + ground(FLOOR, 24, 410)
        b += seg(xm, 104, xm, FLOOR, ORG, 1.6, "5 4") + lbl(xm, 76, "x = 3,0 cm", ORG, 13, "middle", "700") + lbl(xm, 94, "|v| = 40 cm/s", RED, 13, "middle", "700")
        b += block_anim(XC3, ups, dur)
        b += ruler([(XC3, "O", "currentColor"), (xm, "3,0 cm", ORG)])
        b += dim(p, "g", XC3, 52, XC3 + AP3, 52, "", 0, 0) + lbl(XC3 + AP3 / 2, 44, "A = ?", GRN, 13, "middle", "700")
        b += rich(40, 28, "Cần tìm: W, A, v_{max}", "currentColor", 13, "start")
        return fig("d3-0", VB, "Con lắc lò xo nằm ngang dao động; khi vật qua li độ 3 cm thì tốc độ 40 cm trên giây, biên độ chưa biết", b,
                   "Mô phỏng: vật dao động quanh O (chạy chậm 4 lần, 2 chu kì). Đề chưa cho A nên biên độ trong hình chỉ để minh hoạ, không theo tỉ lệ.")
    X0, X1, Y0, H = 60, 360, 96, 30
    fe = .36
    b = defs(p) + rich(X0, 66, "W = E_{t} + E_{d}", GRN, 13, "start")
    b += arrow(p, "g", X0, 80, X1, 80, 2) + arrow(p, "g", X1, 80, X0, 80, 2)
    b += f'<rect x="{X0}" y="{Y0}" width="{(X1 - X0) * fe:.1f}" height="{H}" fill="{ORG}" fill-opacity=".8" stroke="{ORG}" stroke-width="1.5"/>'
    b += f'<rect x="{X0 + (X1 - X0) * fe:.1f}" y="{Y0}" width="{(X1 - X0) * (1 - fe):.1f}" height="{H}" fill="{BLUE}" fill-opacity=".8" stroke="{BLUE}" stroke-width="1.5"/>'
    b += rich(X0 + (X1 - X0) * fe / 2, Y0 + H + 22, "E_{t} = ½kx²", ORG, 13, "middle") + rich(X0 + (X1 - X0) * (fe + (1 - fe) / 2), Y0 + H + 22, "E_{d} = ½mv²", BLUE, 13, "middle")
    b += rich(X0, 168, "W = ½kA² → A", GRN, 13, "start")
    return fig("d3-2", "0 0 420 184", "Cơ năng bằng tổng thế năng và động năng tại cùng một thời điểm, thế năng tính từ li độ, động năng tính từ tốc độ", b, "Dữ kiện: x và v cùng một thời điểm nên cộng được hai năng lượng. " + NOTE)


# ═════════════ Dạng 4 · m = 0,1 kg, k = 40 N/m (ω = 20), A = 5 cm, thả từ biên ═════════════
K4, M4, A4 = 40.0, 0.1, 0.05
W4 = math.sqrt(K4 / M4)
XC4, AP4 = 190, 100


def d4(k):
    p = f"d4{k}"
    if k == 0:
        T, ts = samples(W4)
        dur = 8 * ts[-1]
        ups = [AP4 * math.cos(W4 * t) for t in ts]
        xend = XC4 + AP4 + BW / 2 + 16
        b = defs(p) + wall() + ground(FLOOR, 24, xend) + block_anim(XC4, ups, dur)
        b += ruler([(XC4 - AP4, "−A", "currentColor"), (XC4, "O", "currentColor"), (XC4 + AP4, "A = 5,0 cm", "currentColor")])
        b += bars(xend + 22, 80, ts, W4, dur)
        b += lbl(40, 30, "Thả từ biên lúc t = 0", "currentColor", 13, "start", "700") + rich(40, 52, "T = ?   T′ = ?   Δt = ?", RED, 13, "start")
        return fig("d4-0", VB, "Con lắc lò xo nằm ngang thả từ biên độ 5 cm lúc t bằng 0; hai cột bên phải là thế năng và động năng biến thiên theo thời gian", b,
                   "Mô phỏng: thả từ biên, hai cột cam và xanh thay nhau cao lên thấp xuống (chạy chậm 8 lần, 2 chu kì). Tính theo công thức.")
    CX, CY, R = 210, 110, 70
    ang = math.radians(50)
    px, py = CX + R * math.cos(ang), CY - R * math.sin(ang)
    b = defs(p) + seg(CX - R - 24, CY, CX + R + 40, CY, "currentColor", 1.6) + seg(CX, CY - R - 14, CX, CY + R + 14, "currentColor", 1.2, "5 4")
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="currentColor" stroke-width="1.6" opacity=".6"/>'
    b += seg(CX, CY, CX + R, CY, GRN, 2.4) + f'<circle cx="{CX + R}" cy="{CY}" r="4.5" fill="{GRN}"/>'
    b += lbl(CX + R - 20, CY + 20, "t = 0 (biên)", GRN, 12, "start", "700")
    b += seg(CX, CY, px, py, RED, 2.2, "5 4") + f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{RED}"/>'
    b += lbl(px + 8, py - 6, "t = T/6", RED, 12, "start", "700")
    b += f'<path d="M {CX + 26} {CY} A 26 26 0 0 0 {CX + 26 * math.cos(ang):.1f} {CY - 26 * math.sin(ang):.1f}" fill="none" stroke="{RED}" stroke-width="1.6"/>'
    b += lbl(CX + 34, CY - 12, "ωt = ?", RED, 12, "start", "700") + lbl(CX + R + 34, CY - 8, "x", "currentColor", 13, "start", "700")
    b += rich(40, 24, "x = A cos ωt", "currentColor", 13, "start")
    return fig("d4-2", "0 0 420 214", "Chất điểm quay đều trên đường tròn bán kính A, xuất phát từ biên lúc t bằng 0; đánh dấu vị trí lúc t bằng T chia 6 và góc ωt chưa biết", b, "Dữ kiện: thả từ biên lúc t = 0; đề hỏi tại t = T/6. " + NOTE)


# ═════════════ Dạng 5 · đồ thị Ed(x): W = 0,040 J, A = 4,0 cm, m = 0,5 kg ═════════════
K5, M5 = 50.0, 0.5
W5 = math.sqrt(K5 / M5)
X05, SX5, Y05, SY5 = 225, 33, 190, 3200


def px5(xcm): return X05 + SX5 * xcm
def py5(e): return Y05 - SY5 * e
def ed5(xcm): return 25 * (0.0016 - (xcm / 100) ** 2)


def frame5():
    b = ""
    for xc in (-4, -2, 0, 2, 4):
        b += seg(px5(xc), 30, px5(xc), Y05, "currentColor", 1, "", .12) + seg(px5(xc), Y05, px5(xc), Y05 + 5, "currentColor", 1.4)
        b += lbl(px5(xc), Y05 + 21, ("−" if xc < 0 else "") + str(abs(xc)), "currentColor", 12, "middle", "400")
    for e, t in ((0, "0"), (.01, "0,01"), (.02, "0,02"), (.03, "0,03"), (.04, "0,04")):
        b += seg(60, py5(e), 390, py5(e), "currentColor", 1, "", .12) + seg(55, py5(e), 60, py5(e), "currentColor", 1.4) + lbl(52, py5(e) + 4, t, "currentColor", 12, "end", "400")
    b += seg(60, Y05, 392, Y05, "currentColor", 1.6) + seg(X05, 28, X05, Y05, "currentColor", 1.6)
    b += rich(60, 18, "E_{d} (J)", "currentColor", 12, "start") + lbl(392, Y05 + 42, "x (cm)", "currentColor", 12, "end", "700")
    return b


def curve5():
    return poly([(px5(x / 5), py5(ed5(x / 5))) for x in range(-20, 21)], BLUE, 2.8)


def d5(k):
    p = f"d5{k}"; vb = "0 0 420 240"
    b = defs(p) + frame5() + curve5()
    if k == 0:
        T, ts = samples(W5)
        dur = 4 * ts[-1]
        xs = [4 * math.cos(W5 * t) for t in ts]
        cx = [px5(x) for x in xs]; cy = [py5(ed5(x)) for x in xs]
        b += (f'<line x1="{cx[0]:.1f}" y1="{cy[0]:.1f}" x2="{cx[0]:.1f}" y2="{Y05}" stroke="{GRN}" stroke-width="1.4" stroke-dasharray="4 3">'
              f'{smil("x1", cx, dur)}{smil("x2", cx, dur)}{smil("y1", cy, dur)}</line>')
        b += (f'<circle cx="{cx[0]:.1f}" cy="{cy[0]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{smil("cx", cx, dur)}{smil("cy", cy, dur)}</circle>')
        return fig("d5-0", vb, "Đồ thị động năng theo li độ là parabol quay xuống, cực đại ở li độ 0 và bằng 0 tại li độ cộng trừ 4 cm; một chấm chạy trên đồ thị khi vật dao động", b,
                   "Mô phỏng: vật dao động qua lại, chấm xanh lá chạy trên đồ thị động năng theo li độ (chạy chậm 4 lần, 2 chu kì). Tính theo công thức.")
    b += seg(px5(0), py5(.04), 392, py5(.04), GRN, 1.8, "6 4")
    b += dot(px5(0), py5(.04), 5, GRN) + rich(px5(0) + 12, py5(.04) - 8, "E_{d,max} = W", GRN, 13, "start")
    b += dot(px5(-4), Y05, 5, RED) + dot(px5(4), Y05, 5, RED)
    b += rich(px5(0), Y05 - 30, "E_{d} = 0 ở biên: x = ±A", RED, 12, "middle")
    b += rich(px5(2.5), py5(.032), "E_{d} = ½k(A² − x²)", BLUE, 12, "start")
    return fig("d5-2", vb, "Đồ thị động năng theo li độ: giá trị lớn nhất tại li độ 0 là cơ năng, hai điểm động năng bằng 0 cho biên độ", b, "Dữ kiện: đọc W ở x = 0, đọc A ở chỗ động năng bằng 0. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ───────────────────────── Đề + bảng phân tích ─────────────────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Cơ năng, thế năng, động năng và tốc độ tại một li độ",
      topic="Động năng, thế năng của vật dao động",
      problem_html=r'<p>Một con lắc lò xo nằm ngang gồm lò xo nhẹ có độ cứng $k=50\ \text{N/m}$ và vật nhỏ khối lượng $m=500\ \text{g}$. Kéo vật khỏi vị trí cân bằng $10\ \text{cm}$ rồi thả nhẹ. Bỏ qua ma sát.</p>'
                   r'<ol type="a"><li>Tính cơ năng $W$ của con lắc.</li><li>Khi vật ở li độ $x=6{,}0\ \text{cm}$, tính thế năng $E_t$ và động năng $E_d$.</li><li>Tính tốc độ của vật ở li độ đó.</li></ol>'),
 dict(label="Dạng 2 · Trung bình · Động năng bằng n lần thế năng: li độ, tốc độ, số lần trong một chu kì",
      topic="Động năng, thế năng của vật dao động",
      problem_html=r'<p>Một con lắc lò xo nằm ngang gồm vật nhỏ khối lượng $m=250\ \text{g}$ gắn với lò xo nhẹ có độ cứng $k=25\ \text{N/m}$, dao động điều hoà với biên độ $A=12\ \text{cm}$. Bỏ qua ma sát. Tại một thời điểm, động năng của vật gấp $8$ lần thế năng.</p>'
                   r'<ol type="a"><li>Tính độ lớn li độ của vật lúc đó.</li><li>Tính tốc độ của vật lúc đó.</li><li>Trong một chu kì, có bao nhiêu lần động năng bằng $8$ lần thế năng?</li></ol>'),
 dict(label="Dạng 3 · Trung bình · Biết li độ và tốc độ tại một thời điểm: tìm cơ năng, biên độ",
      topic="Bảo toàn cơ năng trong dao động điều hoà",
      problem_html=r'<p>Một con lắc lò xo nằm ngang gồm vật nhỏ khối lượng $m=250\ \text{g}$ và lò xo nhẹ có độ cứng $k=25\ \text{N/m}$. Vật dao động điều hoà, bỏ qua ma sát. Tại thời điểm vật có li độ $x=3{,}0\ \text{cm}$ thì tốc độ của nó là $40\ \text{cm/s}$.</p>'
                   r'<ol type="a"><li>Tính cơ năng của con lắc.</li><li>Tính biên độ dao động.</li><li>Tính tốc độ cực đại của vật.</li></ol>'),
 dict(label="Dạng 4 · Khó · Chu kì của năng lượng và động năng theo thời gian khi thả từ biên",
      topic="Động năng, thế năng của vật dao động",
      problem_html=r'<p>Một con lắc lò xo nằm ngang gồm vật nhỏ khối lượng $m=100\ \text{g}$ và lò xo nhẹ có độ cứng $k=40\ \text{N/m}$. Kéo vật tới li độ $A=5{,}0\ \text{cm}$ rồi thả nhẹ vào lúc $t=0$. Bỏ qua ma sát. Lấy $\pi=3{,}14$.</p>'
                   r'''<ol type="a"><li>Tính chu kì dao động $T$ của vật.</li><li>Thế năng và động năng biến thiên tuần hoàn với chu kì $T'$ bằng bao nhiêu?</li><li>Khoảng thời gian ngắn nhất giữa hai lần liên tiếp động năng bằng thế năng là bao nhiêu?</li><li>Tính động năng của vật tại thời điểm $t=\dfrac{T}{6}$.</li></ol>'''),
 dict(label="Dạng 5 · Khó · Đọc đồ thị động năng theo li độ: cơ năng, độ cứng, tốc độ cực đại, li độ",
      topic="Bảo toàn cơ năng trong dao động điều hoà",
      problem_html=r'<p>Một con lắc lò xo nằm ngang gồm vật nhỏ khối lượng $m=500\ \text{g}$ dao động điều hoà, bỏ qua ma sát. Đồ thị trong hình biểu diễn động năng $E_d$ của vật (đơn vị J) theo li độ $x$ (đơn vị cm).</p>'
                   r'<ol type="a"><li>Đọc đồ thị để tìm cơ năng $W$ và biên độ $A$ của dao động.</li><li>Tính độ cứng $k$ của lò xo.</li><li>Tính tốc độ cực đại của vật.</li><li>Tại li độ nào thì động năng bằng $0{,}030\ \text{J}$?</li></ol>'),
]

ANALYSIS = [
 [(r"“con lắc lò xo nằm ngang … bỏ qua ma sát”", "Không có ma sát", r"⚠ Bỏ qua ma sát thì cơ năng $W$ không đổi; mốc thế năng đặt tại VTCB ($E_t=0$ khi $x=0$)"),
  (r"“$k=50$ N/m … $m=500$ g”", r"$k=50$ N/m; $m=0{,}500$ kg", "Đổi gam sang kilôgam trước khi thế số"),
  (r"“kéo vật khỏi VTCB $10$ cm rồi thả nhẹ”", r"$A=0{,}10$ m (thả nhẹ: $v=0$ ở biên)", r"$W=\dfrac{1}{2}kA^2$"),
  (r"“thế năng và động năng khi $x=6{,}0$ cm”", r"$x=0{,}060$ m", r"$E_t=\dfrac{1}{2}kx^2$ · $E_d=W-E_t$"),
  (r"“tốc độ của vật ở li độ đó”", r"Cần $|v|$", r"$E_d=\dfrac{1}{2}mv^2$")],
 [(r"“con lắc lò xo nằm ngang … bỏ qua ma sát”", "Không có ma sát", r"⚠ Bỏ qua ma sát thì $W$ không đổi; mốc thế năng đặt tại VTCB"),
  (r"“$m=250$ g … $k=25$ N/m … biên độ $A=12$ cm”", r"$m=0{,}250$ kg; $k=25$ N/m; $A=0{,}12$ m", r"$W=\dfrac{1}{2}kA^2$; đổi g, cm sang kg, m"),
  (r"“động năng của vật gấp $8$ lần thế năng”", r"$E_d=8E_t$", r"⚠ $W=E_t+E_d$ nên chia $W$ theo tỉ lệ; đây không phải trường hợp $E_d=E_t$ ($x=\pm\dfrac{A}{\sqrt{2}}$)"),
  (r"“tính độ lớn li độ”", r"Cần $|x|$", r"$E_t=\dfrac{1}{2}kx^2$"),
  (r"“tính tốc độ”", r"Cần $|v|$", r"$E_d=\dfrac{1}{2}mv^2$"),
  (r"“trong một chu kì, có bao nhiêu lần”", "Cần đếm số lần", r"⚠ Mỗi li độ $\pm|x|$ vật đi qua hai lần trong một chu kì (lúc đi ra và lúc quay về)")],
 [(r"“con lắc lò xo nằm ngang … bỏ qua ma sát”", "Không có ma sát", r"⚠ Bỏ qua ma sát thì $W$ không đổi, nên $W=E_t+E_d$ tại bất kì thời điểm nào; mốc thế năng tại VTCB"),
  (r"“$m=250$ g … $k=25$ N/m”", r"$m=0{,}250$ kg; $k=25$ N/m", "Đổi gam sang kilôgam"),
  (r"“li độ $x=3{,}0$ cm thì tốc độ là $40$ cm/s”", r"$x=0{,}030$ m; $|v|=0{,}40$ m/s", r"⚠ Đổi cm, cm/s sang m, m/s; chưa biết $A$ nên chưa dùng được $W=\dfrac{1}{2}kA^2$ ngay. $E_t=\dfrac{1}{2}kx^2$ · $E_d=\dfrac{1}{2}mv^2$"),
  (r"“tính cơ năng”", r"Cần $W$", r"$W=E_t+E_d$"),
  (r"“tính biên độ”", r"Cần $A$", r"$W=\dfrac{1}{2}kA^2$"),
  (r"“tốc độ cực đại”", r"Cần $v_{max}$", r"$v_{max}=\omega A$ với $\omega=\sqrt{\dfrac{k}{m}}$")],
 [(r"“$m=100$ g … $k=40$ N/m”", r"$m=0{,}100$ kg; $k=40$ N/m", r"$\omega=\sqrt{\dfrac{k}{m}}$ · $T=\dfrac{2\pi}{\omega}$; đổi g sang kg"),
  (r"“kéo vật tới li độ $A=5{,}0$ cm rồi thả nhẹ vào lúc $t=0$”", r"$A=0{,}050$ m; $x(0)=A$, $v(0)=0$", r"⚠ Thả từ biên nên $x=A\cos\omega t$, suy ra $E_t=W\cos^2\omega t$ và $E_d=W\sin^2\omega t$; $W=\dfrac{1}{2}kA^2$"),
  (r"“bỏ qua ma sát”", "Không có ma sát", r"⚠ $W$ không đổi theo thời gian"),
  (r"“tính chu kì dao động $T$”", r"Cần $T$", r"$T=\dfrac{2\pi}{\omega}$"),
  (r"“thế năng và động năng biến thiên tuần hoàn với chu kì $T'$”", r"Cần $T'$", r"Hạ bậc $\cos^2$ và $\sin^2$ để tìm tần số góc của $E_t$, $E_d$"),
  (r"“khoảng thời gian ngắn nhất giữa hai lần liên tiếp động năng bằng thế năng”", r"Điều kiện $E_d=E_t$", r"⚠ $E_d=E_t$ tại $x=\pm\dfrac{A}{\sqrt{2}}$ (không phải $\pm\dfrac{A}{2}$); xét các lần liên tiếp trong một chu kì"),
  (r"“động năng tại thời điểm $t=\dfrac{T}{6}$”", r"$t=\dfrac{T}{6}$", r"Đổi $t$ thành góc $\omega t$; $E_d=W-E_t$")],
 [(r"“con lắc lò xo nằm ngang … bỏ qua ma sát”", "Không có ma sát", r"⚠ Bỏ qua ma sát thì $W$ không đổi; $E_t+E_d=W$ ở mọi li độ"),
  (r"“$m=500$ g”", r"$m=0{,}500$ kg", "Đổi gam sang kilôgam trước khi thế số"),
  (r"“đồ thị biểu diễn động năng $E_d$ theo li độ $x$”", "Đọc từ đồ thị: giá trị tại $x=0$ và hai điểm $E_d=0$", r"⚠ $E_d$ lớn nhất ở $x=0$ (lúc đó $E_t=0$) nên $E_{d,max}=W$; $E_d=0$ ở biên $x=\pm A$; đổi cm sang m"),
  (r"“đọc đồ thị để tìm cơ năng và biên độ”", r"Cần $W$, $A$", r"$W=E_{d,max}$ · $A=|x|$ tại chỗ $E_d=0$"),
  (r"“tính độ cứng $k$”", r"Cần $k$", r"$W=\dfrac{1}{2}kA^2$"),
  (r"“tính tốc độ cực đại”", r"Cần $v_{max}$", r"$W=\dfrac{1}{2}mv_{max}^2$"),
  (r"“động năng bằng $0{,}030$ J”", r"$E_d=0{,}030$ J", r"$E_t=W-E_d$ · $E_t=\dfrac{1}{2}kx^2$")],
]

# ───────────────────────── Lời giải ─────────────────────────
RN = [r"<strong>Khái niệm:</strong> thế năng đo từ VTCB ($E_t=0$ khi $x=0$) · $E_d=\dfrac{1}{2}mv^2$ · $W=E_t+E_d$.",
      r"<strong>Định luật:</strong> bỏ qua ma sát thì cơ năng $W$ không đổi.",
      r"<strong>Công thức:</strong> $E_t=\dfrac{1}{2}kx^2$ · $W=\dfrac{1}{2}kA^2$ · $E_d=W-E_t$.",
      r"<strong>Điều kiện:</strong> ⚠ không ma sát; $x$ tính từ VTCB; đổi g sang kg, cm sang m."]

SOLS = [
 sol(RN, [
  ("Cơ năng", [P(r"Đổi đơn vị: $A=0{,}10\ \text{m}$, $m=0{,}500\ \text{kg}$."), M(r"W=\dfrac{1}{2}kA^2=\dfrac{1}{2}\cdot50\cdot0{,}10^2"), A(r"W=0{,}25\ \text{J}")]),
  (r"Thế năng tại $x=6{,}0$ cm", [M(r"E_t=\dfrac{1}{2}kx^2=\dfrac{1}{2}\cdot50\cdot0{,}060^2"), A(r"E_t=0{,}090\ \text{J}")]),
  ("Động năng", [P(r"Bỏ qua ma sát nên $W$ không đổi:"), M(r"E_d=W-E_t=0{,}25-0{,}090"), A(r"E_d=0{,}16\ \text{J}")]),
  ("Tốc độ", [M(r"E_d=\dfrac{1}{2}mv^2\Rightarrow |v|=\sqrt{\dfrac{2E_d}{m}}=\sqrt{\dfrac{2\cdot0{,}16}{0{,}500}}=\sqrt{0{,}64}"), A(r"|v|=0{,}80\ \text{m/s}")]),
  ("Kiểm tra", [P(r"$E_t+E_d=0{,}090+0{,}16=0{,}25\ \text{J}=W$ ✓"), P(r"$|x|=6{,}0\ \text{cm}\lt A=10\ \text{cm}$ nên vật chưa tới biên, $E_d\gt0$ ✓")])],
  [r"a) $W=0{,}25\ \text{J}$", r"b) $E_t=0{,}090\ \text{J}$ · $E_d=0{,}16\ \text{J}$", r"c) $|v|=0{,}80\ \text{m/s}$"],
  r"Nhận dạng: đề cho <strong>$k$, biên độ và một li độ</strong> → $W=\dfrac{1}{2}kA^2$, $E_t=\dfrac{1}{2}kx^2$, $E_d=W-E_t$."),
 sol(RN + [r"Chia cơ năng: $E_d=nE_t$ thì $W=(n+1)E_t$."], [
  ("Cơ năng", [P(r"Đổi $A=0{,}12\ \text{m}$."), M(r"W=\dfrac{1}{2}kA^2=\dfrac{1}{2}\cdot25\cdot0{,}12^2"), A(r"W=0{,}18\ \text{J}")]),
  ("Chia cơ năng theo tỉ lệ", [P(r"$E_d=8E_t$ và $W=E_t+E_d$ nên $W=9E_t$:"), M(r"E_t=\dfrac{W}{9}=\dfrac{0{,}18}{9}"), A(r"E_t=0{,}020\ \text{J}"), M(r"E_d=8E_t=0{,}16\ \text{J}")]),
  ("Độ lớn li độ", [M(r"E_t=\dfrac{1}{2}kx^2\Rightarrow |x|=\sqrt{\dfrac{2E_t}{k}}=\sqrt{\dfrac{2\cdot0{,}020}{25}}=\sqrt{0{,}0016}"), A(r"|x|=0{,}040\ \text{m}=4{,}0\ \text{cm}"),
                    P(r"Kiểm tra bằng công thức tổng quát $|x|=\dfrac{A}{\sqrt{n+1}}=\dfrac{12}{\sqrt{9}}=4{,}0\ \text{cm}$ ✓")]),
  ("Tốc độ", [M(r"E_d=\dfrac{1}{2}mv^2\Rightarrow |v|=\sqrt{\dfrac{2E_d}{m}}=\sqrt{\dfrac{2\cdot0{,}16}{0{,}250}}=\sqrt{1{,}28}"), A(r"|v|\approx1{,}13\ \text{m/s}"),
              P(r"Kiểm tra: $v_{max}=\omega A=\sqrt{\dfrac{k}{m}}A=10\cdot0{,}12=1{,}2\ \text{m/s}$ và $|v|\lt v_{max}$ ✓")]),
  ("Số lần trong một chu kì", [P(r"Có hai li độ thoả mãn: $x=+4{,}0\ \text{cm}$ và $x=-4{,}0\ \text{cm}$."), P("Mỗi li độ vật đi qua hai lần trong một chu kì (lúc đi ra và lúc quay về)."), A("T:Số lần $=2\\times2=4$ lần.")])],
  [r"a) $|x|=4{,}0\ \text{cm}$", r"b) $|v|\approx1{,}13\ \text{m/s}$", "c) 4 lần trong một chu kì"],
  r"Nhận dạng: đề cho <strong>tỉ số động năng : thế năng</strong> → chia cơ năng theo tỉ lệ, rồi tìm $x$ từ $E_t$."),
 sol(RN + [r"Biết $x$ và $v$ cùng lúc thì $W=\dfrac{1}{2}kx^2+\dfrac{1}{2}mv^2$, từ đó suy ra $A$."], [
  ("Động năng lúc đó", [P(r"Đổi đơn vị: $v=40\ \text{cm/s}=0{,}40\ \text{m/s}$; $x=0{,}030\ \text{m}$."), M(r"E_d=\dfrac{1}{2}mv^2=\dfrac{1}{2}\cdot0{,}250\cdot0{,}40^2"), A(r"E_d=0{,}020\ \text{J}")]),
  ("Thế năng lúc đó", [M(r"E_t=\dfrac{1}{2}kx^2=\dfrac{1}{2}\cdot25\cdot0{,}030^2"), A(r"E_t=0{,}01125\ \text{J}")]),
  ("Cơ năng", [P(r"Bỏ qua ma sát nên $W=E_t+E_d$ ở mọi thời điểm:"), M(r"W=0{,}01125+0{,}020"), A(r"W=0{,}03125\ \text{J}")]),
  ("Biên độ", [M(r"W=\dfrac{1}{2}kA^2\Rightarrow A=\sqrt{\dfrac{2W}{k}}=\sqrt{\dfrac{2\cdot0{,}03125}{25}}=\sqrt{0{,}0025}"), A(r"A=0{,}050\ \text{m}=5{,}0\ \text{cm}")]),
  ("Tốc độ cực đại", [P(r"$\omega=\sqrt{\dfrac{k}{m}}=\sqrt{\dfrac{25}{0{,}250}}=10\ \text{rad/s}$"), M(r"v_{max}=\omega A=10\cdot0{,}050"), A(r"v_{max}=0{,}50\ \text{m/s}"),
                      P(r"Kiểm tra: $A\gt|x|$ và $v_{max}\gt|v|$ ✓")])],
  [r"a) $W\approx0{,}031\ \text{J}$ (chính xác $0{,}03125\ \text{J}$)", r"b) $A=5{,}0\ \text{cm}$", r"c) $v_{max}=0{,}50\ \text{m/s}$"],
  r"Nhận dạng: đề cho <strong>li độ và tốc độ cùng lúc</strong> mà chưa cho $A$ → cộng $E_t+E_d$ ra $W$, rồi suy $A$."),
 sol(RN + [r"Chu kì: $T=\dfrac{2\pi}{\omega}$, $\omega=\sqrt{\dfrac{k}{m}}$ · thả từ biên: $x=A\cos\omega t$, $E_t=W\cos^2\omega t$, $E_d=W\sin^2\omega t$."], [
  ("Chu kì $T$", [P(r"Đổi $m=0{,}100\ \text{kg}$."), M(r"\omega=\sqrt{\dfrac{k}{m}}=\sqrt{\dfrac{40}{0{,}100}}=20\ \text{rad/s}"), M(r"T=\dfrac{2\pi}{\omega}=\dfrac{2\cdot3{,}14}{20}"), A(r"T=0{,}314\ \text{s}")]),
  ("Chu kì của năng lượng", [P(r"Hạ bậc: $E_t=\dfrac{W}{2}(1+\cos2\omega t)$, $E_d=\dfrac{W}{2}(1-\cos2\omega t)$ có tần số góc $2\omega$."), M(r"T'=\dfrac{T}{2}=\dfrac{0{,}314}{2}"), A(r"T'=0{,}157\ \text{s}")]),
  (r"Hai lần liên tiếp $E_d=E_t$", [P(r"$E_d=E_t$ tại $x=\pm\dfrac{A}{\sqrt{2}}$: bốn lần mỗi chu kì, cách đều nhau."), M(r"\Delta t_{min}=\dfrac{T}{4}=\dfrac{0{,}314}{4}"), A(r"\Delta t_{min}\approx0{,}0785\ \text{s}")]),
  ("Cơ năng", [P(r"Đổi $A=0{,}050\ \text{m}$."), M(r"W=\dfrac{1}{2}kA^2=\dfrac{1}{2}\cdot40\cdot0{,}050^2"), A(r"W=0{,}050\ \text{J}")]),
  (r"Động năng lúc $t=\dfrac{T}{6}$", [P(r"Góc pha: $\omega t=\dfrac{2\pi}{T}\cdot\dfrac{T}{6}=\dfrac{\pi}{3}$."), M(r"x=A\cos\dfrac{\pi}{3}=\dfrac{A}{2}\Rightarrow E_t=\dfrac{1}{2}k\left(\dfrac{A}{2}\right)^2=\dfrac{W}{4}"), M(r"E_d=W-E_t=\dfrac{3W}{4}=\dfrac{3}{4}\cdot0{,}050"), A(r"E_d=0{,}0375\ \text{J}"),
                                    P(r"Kiểm tra: tại $x=\dfrac{A}{2}$ thì $E_d=3E_t$ ✓")])],
  [r"a) $T=0{,}314\ \text{s}$", r"b) $T'=0{,}157\ \text{s}$", r"c) $\Delta t_{min}\approx0{,}0785\ \text{s}$", r"d) $E_d=0{,}0375\ \text{J}$"],
  r"Nhận dạng: <strong>thả từ biên</strong> và hỏi theo <strong>thời gian</strong> → $E_t=W\cos^2\omega t$; chu kì năng lượng là $\dfrac{T}{2}$."),
 sol(RN + [r"Đồ thị $E_d(x)$: lớn nhất ở $x=0$ và bằng $W$; bằng $0$ ở biên $x=\pm A$."], [
  ("Cơ năng và biên độ từ đồ thị", [P(r"Ở $x=0$ thế năng bằng $0$ nên $E_d$ cực đại và bằng cơ năng."), A(r"W=E_{d,max}=0{,}040\ \text{J}"), P(r"$E_d=0$ ở hai biên, đọc được $x=\pm4{,}0\ \text{cm}$."), A(r"A=4{,}0\ \text{cm}=0{,}040\ \text{m}")]),
  ("Độ cứng", [M(r"W=\dfrac{1}{2}kA^2\Rightarrow k=\dfrac{2W}{A^2}=\dfrac{2\cdot0{,}040}{0{,}040^2}"), A(r"k=50\ \text{N/m}")]),
  ("Tốc độ cực đại", [P(r"Tại VTCB $E_d=W$:"), M(r"W=\dfrac{1}{2}mv_{max}^2\Rightarrow v_{max}=\sqrt{\dfrac{2W}{m}}=\sqrt{\dfrac{2\cdot0{,}040}{0{,}500}}=\sqrt{0{,}16}"), A(r"v_{max}=0{,}40\ \text{m/s}"),
                      P(r"Kiểm tra: $\omega=\sqrt{\dfrac{k}{m}}=10\ \text{rad/s}$ và $\omega A=10\cdot0{,}040=0{,}40\ \text{m/s}$ ✓")]),
  (r"Li độ khi $E_d=0{,}030$ J", [M(r"E_t=W-E_d=0{,}040-0{,}030=0{,}010\ \text{J}"), M(r"E_t=\dfrac{1}{2}kx^2\Rightarrow |x|=\sqrt{\dfrac{2E_t}{k}}=\sqrt{\dfrac{2\cdot0{,}010}{50}}=\sqrt{0{,}0004}"), A(r"|x|=0{,}020\ \text{m}=2{,}0\ \text{cm}")]),
  ("Kiểm tra", [P(r"$E_d=0{,}030\ \text{J}$ nằm giữa $0$ và $0{,}040\ \text{J}$ nên $|x|\lt A$ ✓"), P(r"$E_t+E_d=0{,}010+0{,}030=0{,}040\ \text{J}=W$ ✓")])],
  [r"a) $W=0{,}040\ \text{J}$ · $A=4{,}0\ \text{cm}$", r"b) $k=50\ \text{N/m}$", r"c) $v_{max}=0{,}40\ \text{m/s}$", r"d) $x=\pm2{,}0\ \text{cm}$"],
  r"Nhận dạng: đề cho <strong>đồ thị $E_d(x)$</strong> → giá trị lớn nhất là $W$, chỗ $E_d=0$ cho $A$, rồi suy $k$, $v_{max}$."),
]

# ───────────────────────── Tự giải từng bước (9/10/2026) ─────────────────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>$k$, biên độ và một li độ</b> rồi hỏi $E_t$, $E_d$ → $W=\dfrac{1}{2}kA^2$, $E_t=\dfrac{1}{2}kx^2$, $E_d=W-E_t$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Cơ năng", r"Cơ năng $W$ của con lắc bằng bao nhiêu?", 0.25, "J", 0.005,
       loi=r"Quên đổi $10\ \text{cm}$ sang mét (thế $A=10$ ra số rất lớn), hoặc dùng $\dfrac{1}{2}mA^2$ — cơ năng của lò xo là $\dfrac{1}{2}kA^2$."),
  buoc(r"Thế năng tại $x=6{,}0$ cm", r"Thế năng $E_t$ tại $x=6{,}0$ cm bằng bao nhiêu?", 0.09, "J", 0.003,
       loi=r"Dùng $A$ thay cho $x$ (ra đúng cơ năng): $x$ là li độ lúc đang xét, $A$ là biên độ.",
       ke=[(r"$E_t=\dfrac{1}{2}kx^2$ với $x$ là li độ lúc đang xét", True),
           (r"$E_t=\dfrac{1}{2}kA^2$", r"Đó là cơ năng (thế năng ở biên); tại li độ $x$ đang xét thì dùng $x$."),
           (r"$E_t=\dfrac{1}{2}mx^2$", r"Thiếu độ cứng: thế năng đàn hồi là $\dfrac{1}{2}kx^2$, không có khối lượng.")]),
  buoc("Động năng", r"Động năng $E_d$ lúc đó bằng bao nhiêu?", 0.16, "J", 0.004,
       loi=r"Coi $E_d=E_t$ (hai năng lượng chỉ bằng nhau ở $x=\pm\dfrac{A}{\sqrt{2}}$) hoặc dùng công thức thế năng cho động năng.",
       ke=[(r"$E_d=W-E_t$ vì bỏ qua ma sát nên cơ năng không đổi", True),
           (r"$E_d=E_t$ vì hai năng lượng đổi chỗ cho nhau", r"Hai năng lượng chỉ bằng nhau ở $x=\pm\dfrac{A}{\sqrt{2}}$; ở li độ khác thì khác nhau."),
           (r"$E_d=\dfrac{1}{2}kx^2$", r"Đó là công thức thế năng; động năng là phần còn lại $W-E_t$.")]),
  buoc("Tốc độ", r"Tốc độ $|v|$ của vật ở li độ đó bằng bao nhiêu?", 0.8, "m/s", 0.01,
       loi=r"Quên nhân $2$ hoặc quên khai căn; và phải đổi $500\ \text{g}$ sang kg trước.",
       ke=[(r"$|v|=\sqrt{\dfrac{2E_d}{m}}$ từ $E_d=\dfrac{1}{2}mv^2$", True),
           (r"$|v|=\sqrt{\dfrac{E_d}{m}}$", r"Thiếu hệ số $2$: từ $E_d=\dfrac{1}{2}mv^2$ suy ra $v^2=\dfrac{2E_d}{m}$."),
           (r"$|v|=\dfrac{2E_d}{m}$", r"Thiếu dấu căn: đó mới là $v^2$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>động năng gấp n lần thế năng</b> → $W=(n+1)E_t$, rồi tìm $x$ từ $E_t=\dfrac{1}{2}kx^2$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Cơ năng", r"Cơ năng $W$ bằng bao nhiêu?", 0.18, "J", 0.005,
       loi=r"Quên đổi $12\ \text{cm}$ sang mét, hoặc quên bình phương biên độ."),
  buoc("Chia cơ năng theo tỉ lệ", r"Thế năng $E_t$ lúc đó bằng bao nhiêu?", 0.02, "J", 0.001,
       loi=r"Chia $W$ cho $8$ (quên cộng phần thế năng) hoặc cho $2$ (chỉ đúng khi $E_d=E_t$).",
       ke=[(r"Từ $E_d=8E_t$ và $W=E_t+E_d$ suy ra $W=9E_t$", True),
           (r"$E_t=\dfrac{W}{8}$", r"Cơ năng gồm cả thế năng lẫn động năng, không chỉ phần động năng."),
           (r"$E_t=\dfrac{W}{2}$ vì hai năng lượng chia đôi", r"Chia đôi chỉ khi $E_d=E_t$; ở đây động năng lớn hơn thế năng rất nhiều.")]),
  buoc("Độ lớn li độ", r"Độ lớn li độ $|x|$ bằng bao nhiêu cm?", 4, "cm", 0.1,
       loi=r"Lấy $\dfrac{A}{\sqrt{2}}$ (chỉ đúng khi $E_d=E_t$) hoặc chia thẳng $A$ cho $8$.",
       ke=[(r"Từ $E_t=\dfrac{1}{2}kx^2$ rút $|x|$", True),
           (r"$|x|=\dfrac{A}{\sqrt{2}}$", r"Đó là li độ lúc $E_d=E_t$; ở đây tỉ số khác $1$."),
           (r"$|x|=\dfrac{A}{8}$", r"Thế năng tỉ lệ với $x^2$ chứ không tỉ lệ với $x$, nên không chia thẳng $A$ cho số $8$ của đề.")]),
  buoc("Tốc độ", r"Tốc độ $|v|$ lúc đó bằng bao nhiêu?", 1.13, "m/s", 0.02,
       loi=r"Dùng $|v|=\omega|x|$ hoặc lấy $v_{max}$; tốc độ tại li độ $x$ phải tính từ động năng.",
       ke=[(r"Có $E_d=W-E_t$, rồi $|v|=\sqrt{\dfrac{2E_d}{m}}$", True),
           (r"$|v|=\omega|x|$", r"Công thức này cho tốc độ bằng $0$ ở VTCB và lớn nhất ở biên, ngược thực tế; tốc độ là $\omega\sqrt{A^2-x^2}$ và lớn nhất ở VTCB."),
           (r"$|v|=v_{max}$ vì $E_d$ lớn hơn $E_t$", r"$v_{max}$ chỉ ở VTCB ($x=0$); ở $|x|\ne0$ thì $|v|\lt v_{max}$.")]),
  buoc("Số lần trong một chu kì", r"Trong một chu kì, $E_d=8E_t$ xảy ra mấy lần?",
       loi=r"Đếm thiếu hoặc đếm thừa: mỗi li độ tìm được phải xét xem vật đi qua bao nhiêu lần trong một chu kì.",
       lua_chon=[("4 lần: hai li độ, mỗi li độ đi qua hai lần", True),
                 (r"2 lần, ứng với $x=+|x|$ và $x=-|x|$", "Mỗi li độ vật đi qua hai lần (lúc đi ra và lúc quay về), không phải một lần."),
                 (r"8 lần, vì tỉ số trong đề là $8$", "Số lần không phụ thuộc giá trị của tỉ số; nó chỉ phụ thuộc số li độ thoả mãn và số lần đi qua mỗi li độ.")],
       ke=[("Đếm số li độ thoả mãn rồi nhân với số lần đi qua mỗi li độ", True),
           ("Lấy chu kì chia cho khoảng thời gian giữa hai lần", "Đề không cho thời gian; hơn nữa các lần không cách đều nhau."),
           ("Lấy luôn hệ số của đề làm số lần", "Hệ số $8$ chỉ cho biết li độ, không cho biết vật đi qua bao nhiêu lần.")])]),
 dict(nhan_dang=r"Thấy <b>li độ và tốc độ cùng một lúc</b> mà chưa cho $A$ → cộng $E_t+E_d$ ra $W$, rồi suy $A$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Động năng lúc đó", r"Động năng $E_d$ của vật lúc đó bằng bao nhiêu?", 0.02, "J", 0.0005,
       loi=r"Quên đổi $40\ \text{cm/s}$ sang $\text{m/s}$ (thế $40$ ra số lớn gấp vạn lần)."),
  buoc("Thế năng lúc đó", r"Thế năng $E_t$ lúc đó bằng bao nhiêu?", 0.01125, "J", 0.0004,
       loi=r"Dùng $x=3{,}0$ (cm) thay vì $0{,}030$ (m), hoặc dùng công thức $\dfrac{1}{2}mx^2$.",
       ke=[(r"$E_t=\dfrac{1}{2}kx^2$ với $x$ đã đổi sang mét", True),
           (r"$E_t=\dfrac{1}{2}kA^2$", r"$A$ chưa biết (đó là điều cần tìm); thế năng lúc này tính bằng li độ $x$ đã cho."),
           (r"$E_t=\dfrac{1}{2}mx^2$", r"Thiếu độ cứng: thế năng đàn hồi là $\dfrac{1}{2}kx^2$.")]),
  buoc("Cơ năng", r"Cơ năng $W$ bằng bao nhiêu?", 0.03125, "J", 0.0005,
       loi=r"Lấy $W=E_d$ vì thấy vật đang chuyển động, hoặc $W=E_t$; phải cộng cả hai.",
       ke=[(r"$W=E_t+E_d$ tại thời điểm đã cho", True),
           (r"$W=E_d$ vì vật đang chuyển động", r"Vật vẫn có li độ $x\ne0$ nên còn thế năng; $W=E_t+E_d$."),
           (r"$W=\dfrac{1}{2}kx^2$", r"Đó mới là thế năng tại li độ $x$; cơ năng phải cộng thêm động năng.")]),
  buoc("Biên độ", r"Biên độ $A$ bằng bao nhiêu cm?", 5, "cm", 0.1,
       loi=r"Quên dấu căn ($A^2=\dfrac{2W}{k}$) hoặc quên đổi kết quả từ mét sang cm.",
       ke=[(r"$A=\sqrt{\dfrac{2W}{k}}$ từ $W=\dfrac{1}{2}kA^2$", True),
           (r"$A=\dfrac{2W}{k}$", r"Thiếu dấu căn: đó mới là $A^2$."),
           (r"$A=\sqrt{\dfrac{2W}{m}}$", r"Mẫu số phải là độ cứng $k$; công thức có $m$ là của tốc độ cực đại.")]),
  buoc("Tốc độ cực đại", r"Tốc độ cực đại $v_{max}$ bằng bao nhiêu?", 0.5, "m/s", 0.01,
       loi=r"Lấy $\omega=\dfrac{k}{m}$ (quên căn) hoặc nhân với li độ $x$ thay vì biên độ $A$.",
       ke=[(r"$v_{max}=\omega A$ với $\omega=\sqrt{\dfrac{k}{m}}$", True),
           (r"$v_{max}=\omega x$", r"Phải dùng biên độ $A$: $v_{max}=\omega A$ khi qua VTCB; $\omega x$ không phải tốc độ cực đại."),
           (r"$v_{max}=\sqrt{\dfrac{2W}{k}}$", r"Đó là biên độ $A$ (đơn vị mét), không phải tốc độ.")])]),
 dict(nhan_dang=r"Thấy <b>thả từ biên</b> và hỏi theo <b>thời gian</b> → $E_t=W\cos^2\omega t$; chu kì năng lượng là $\dfrac{T}{2}$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc(r"Chu kì $T$", r"Chu kì dao động $T$ bằng bao nhiêu?", 0.314, "s", 0.005,
       loi=r"Quên đổi $100\ \text{g}$ sang kg, hoặc lật tỉ số: $T=2\pi\sqrt{\dfrac{m}{k}}$ (khối lượng ở tử)."),
  buoc("Chu kì của năng lượng", r"Chu kì $T'$ của thế năng và động năng bằng bao nhiêu?", 0.157, "s", 0.003,
       loi=r"Nhầm chu kì năng lượng với chu kì li độ $T$ — hay chọn $T'=T$.",
       ke=[(r"$E_t$, $E_d$ có tần số góc $2\omega$ nên $T'=\dfrac{T}{2}$", True),
           (r"$T'=T$ vì cùng chu kì với li độ", "Mỗi chu kì của li độ, thế năng đạt cực đại hai lần (ở hai biên), nên chu kì của năng lượng ngắn hơn."),
           (r"$T'=2T$", "Năng lượng đổi nhanh gấp đôi li độ chứ không chậm hơn.")]),
  buoc(r"Hai lần liên tiếp $E_d=E_t$", r"Khoảng thời gian ngắn nhất giữa hai lần liên tiếp $E_d=E_t$ là bao nhiêu?", 0.0785, "s", 0.002,
       loi=r"Lấy $\Delta t=T'$ hoặc $\dfrac{T}{8}$; phải đếm xem $E_d=E_t$ xảy ra mấy lần trong một chu kì rồi xét các lần liên tiếp.",
       ke=[(r"Bốn lần mỗi chu kì, cách đều nhau nên $\Delta t=\dfrac{T}{4}$", True),
           (r"$\Delta t=\dfrac{T}{2}$ vì chu kì của năng lượng là $\dfrac{T}{2}$", "Trong mỗi chu kì năng lượng, $E_d=E_t$ xảy ra hai lần chứ không phải một lần."),
           (r"$\Delta t=\dfrac{T}{8}$ vì $x=\dfrac{A}{\sqrt{2}}$ ứng với góc $45^\circ$", "Đó là thời gian từ biên tới chỗ $E_d=E_t$ lần đầu, không phải giữa hai lần liên tiếp.")]),
  buoc("Cơ năng", r"Cơ năng $W$ bằng bao nhiêu?", 0.05, "J", 0.001,
       loi=r"Quên đổi $5{,}0\ \text{cm}$ sang mét hoặc quên bình phương $A$.",
       ke=[(r"$W=\dfrac{1}{2}kA^2$ với $A$ đã đổi sang mét", True),
           (r"$W=\dfrac{1}{2}mv^2$", r"Chưa biết $v$; hơn nữa đó chỉ là động năng tại thời điểm xét."),
           (r"$W=\dfrac{1}{2}kA$", r"Thiếu bình phương biên độ: $W=\dfrac{1}{2}kA^2$.")]),
  buoc(r"Động năng lúc $t=\dfrac{T}{6}$", r"Động năng $E_d$ tại $t=\dfrac{T}{6}$ bằng bao nhiêu?", 0.0375, "J", 0.001,
       loi=r"Đảo $\sin$ và $\cos$: thả từ biên thì $E_t=W\cos^2\omega t$, $E_d=W\sin^2\omega t$; hoặc đổi $t=\dfrac{T}{6}$ thành $\dfrac{\pi}{6}$ thay vì $\dfrac{\pi}{3}$.",
       ke=[(r"Đổi $t$ ra góc $\omega t$, suy ra $x$ rồi $E_t$, sau đó $E_d=W-E_t$", True),
           (r"$E_d=W\cos^2\omega t$", r"Thả từ biên nên $x=A\cos\omega t$, do đó $\cos^2$ đi với thế năng, $\sin^2$ mới đi với động năng."),
           (r"$E_d=\dfrac{W}{2}$ vì $t$ nằm giữa", r"$E_d=\dfrac{W}{2}$ chỉ tại $t=\dfrac{T}{8}$ ($x=\dfrac{A}{\sqrt{2}}$).")])]),
 dict(nhan_dang=r"Thấy <b>đồ thị $E_d(x)$</b> → giá trị lớn nhất là $W$, chỗ $E_d=0$ cho $A$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Cơ năng và biên độ từ đồ thị", r"Cơ năng $W$ (đọc từ đồ thị) bằng bao nhiêu?", 0.04, "J", 0.001,
       loi=r"Đọc $E_d$ ở một li độ bất kì thay vì ở $x=0$; cơ năng bằng động năng cực đại, tức giá trị tại VTCB."),
  buoc("Độ cứng", r"Độ cứng $k$ của lò xo bằng bao nhiêu?", 50, "N/m", 1,
       loi=r"Dùng $A=4{,}0$ (cm) thay vì $0{,}040$ (m), hoặc quên bình phương $A$.",
       ke=[(r"$k=\dfrac{2W}{A^2}$ với $A$ đọc ở chỗ $E_d=0$, đổi sang mét", True),
           (r"$k=\dfrac{2W}{A}$", r"Thiếu bình phương biên độ: $W=\dfrac{1}{2}kA^2$."),
           (r"$k=m\omega^2$ với $\omega$ đọc từ đồ thị", r"Đồ thị $E_d(x)$ không cho $\omega$ trực tiếp; đã biết $W$ và $A$ thì tính $k$ từ $W=\dfrac{1}{2}kA^2$.")]),
  buoc("Tốc độ cực đại", r"Tốc độ cực đại $v_{max}$ bằng bao nhiêu?", 0.4, "m/s", 0.01,
       loi=r"Dùng $m=500$ (g) không đổi sang kg, hoặc lấy $\omega$ làm tốc độ.",
       ke=[(r"$v_{max}=\sqrt{\dfrac{2W}{m}}$ vì tại VTCB $E_d=W$", True),
           (r"$v_{max}=\sqrt{\dfrac{2W}{k}}$", r"Đó là biên độ $A$; tốc độ cần khối lượng: $W=\dfrac{1}{2}mv_{max}^2$."),
           (r"$v_{max}=\sqrt{\dfrac{k}{m}}$", r"Đó là $\omega$ (rad/s); còn phải nhân với biên độ: $v_{max}=\omega A$.")]),
  buoc(r"Li độ khi $E_d=0{,}030$ J", r"Khi $E_d=0{,}030\ \text{J}$ thì $|x|$ bằng bao nhiêu cm?", 2, "cm", 0.05,
       loi=r"Thế $E_d$ vào công thức thế năng $\dfrac{1}{2}kx^2$ (nhầm động năng với thế năng).",
       ke=[(r"Tính $E_t=W-E_d$ rồi $|x|=\sqrt{\dfrac{2E_t}{k}}$", True),
           (r"$|x|=\sqrt{\dfrac{2E_d}{k}}$", r"Đó là li độ mà thế năng bằng $0{,}030$ J; đề cho động năng nên thế năng là phần còn lại $W-E_d$."),
           (r"$|x|=A\sqrt{\dfrac{E_d}{W}}$", r"Đó là mối liên hệ của tốc độ ($|v|=v_{max}\sqrt{E_d/W}$), không phải của li độ; li độ liên hệ với $E_t$.")]),
  buoc("Kiểm tra")]),
]

d = {"lesson_id": 24, "lesson_title": "Bài 5. Động năng. Thế năng. Sự chuyển hoá giữa động năng và thế năng trong dao động điều hoà",
     "generated_at": "2026-10-09",
     "review": {"checked": True, "notes": "Kiểm chéo 9/10: 5 dạng đáp số độc lập khớp; đã đổi hình phân tích dạng 4 (bỏ đồ thị Et,Ed theo t lộ chu kì T/2) sang đường tròn pha, bỏ caption/loi_hay_gap lộ đáp số."},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DANG]}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
