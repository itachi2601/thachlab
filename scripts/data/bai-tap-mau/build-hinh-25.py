"""Bài 25 · Bài 6. Dao động tắt dần. Dao động cưỡng bức. Hiện tượng cộng hưởng (Vật lí 11, chương 1 Dao động)
— dựng file scripts/data/bai-tap-mau/25.json từ đầu.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-25.py        (mẫu cấu trúc: build-hinh-57.py, build-hinh-33.py)

Quy ước theo lý thuyết bài 25: tắt dần = biên độ, cơ năng giảm (lực cản, cơ năng → nhiệt), A = A0·e^(−βt) · duy trì = bù đúng phần mất mỗi chu kì,
biên độ không đổi, chu kì riêng · cưỡng bức = ngoại lực tuần hoàn liên tục, ổn định f_vật = f_lực (có thể ≠ f0) · cộng hưởng f = f0 (ω = ω0, T = T0),
mô hình A(f) = A_r·b/√((f−f0)²+b²), cản nhỏ: đỉnh cao, hẹp · bảng quét tần số có sai số đọc ±0,2 cm.
Cơ năng ∝ A² lấy từ bài năng lượng dao động điều hoà (bài trước trong chương). v = L/T (xe qua gờ) là kiến thức chuyển động đều lớp 10.

Quét số dạng (bước 0, tự làm — ngân hàng bị RLS với anon nên lấy YCCĐ từ scripts/data/question-topics.json; lesson 25 có chủ đề cha 41
"Dao động tắt dần. Dao động cưỡng bức. Cộng hưởng" và 2 chủ đề con: 162 "Dao động tắt dần và nguyên nhân", 163 "Dao động cưỡng bức và hiện tượng cộng hưởng").
5 dạng, cấp 1–4 không giảm:
  1 (cấp 1, ly_thuyet, 162) Phân biệt tắt dần – duy trì – cưỡng bức từ nguyên nhân; chu kì lúc ổn định của dao động cưỡng bức   · nền tảng
  2 (cấp 2, ly_thuyet, 163) Cộng hưởng qua bảng quét tần số: tìm f0, f_vật = f_lực, so biên độ với sai số đọc                  · thêm: đọc bảng, so với sai số
  3 (cấp 2, bai_tap,   162) Tắt dần định lượng: A = A0·e^(−βt), thời điểm còn một nửa biên độ, cơ năng ∝ A²                     · thêm: tính toán, bẫy A²
  4 (cấp 3, bai_tap,   163) Xe qua gờ giảm tốc: T = L/v, đổi km/h, điều kiện T = T0, so hai vận tốc bằng |f − f0|              · thêm: kết hợp 4 bước
  5 (cấp 4, bai_tap,   163) Chọn đệm chống rung: A(f) ở tần số chạy ổn định và lúc khởi động đi qua f0, chọn theo hai ngưỡng      · thêm: nhiều ý, dữ kiện ẩn
Không đưa vào: tần số góc, độ lệch pha tắt dần-cưỡng bức (bài không dạy); bài toán lực cản/ma sát tính quãng đường (ngoài phạm vi bài, ngân hàng cùng chủ đề không có)."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "25.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
PI = math.pi


def curve(d, c=GRN, w=2.6, op=1.0, dash=""):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" opacity="{op}"{ds}/>'


def path_d(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def clip_grow(cid, x, y, w, h, dur):
    """clipPath có chiều rộng 0 → w khi bấm chạy: phần đường cong đã vẽ hiện dần."""
    return f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="0" height="{h}">{smil("width", [0, w], dur)}</rect></clipPath>'


def runner(pts, dur, c=ORG, r=5.5):
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cx", [q[0] for q in pts], dur)}{smil("cy", [q[1] for q in pts], dur)}</circle>')


def fmt(x, nd=1):
    s = f"{x:.{nd}f}".replace(".", ",")
    return s.rstrip("0").rstrip(",") if "," in s else s


def xy_anim(vals, dur):
    return (f'<animateTransform attributeName="transform" type="translate" values="{";".join(f"{x:.1f} {y:.1f}" for x, y in vals)}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')


# ═════════════ Dạng 1 · ba con lắc: tắt dần (β = 0,5 /s), duy trì, cưỡng bức (f = 1,5 Hz, A = 2,5 cm) · T0 = 1,0 s ═════════════
T0_1, B1, A1, F3, A3 = 1.0, 0.5, 4.0, 1.5, 2.5
X0_1, SXT1, TMAX1 = 56, 85.0, 4.0
CY1, SYC1 = [52, 140, 228], 9.0


def u1(i, t):
    return [A1 * math.exp(-B1 * t) * math.cos(2 * PI * t / T0_1), A1 * math.cos(2 * PI * t / T0_1), A3 * math.cos(2 * PI * F3 * t)][i]


def frame1():
    b = ""
    for i, cy in enumerate(CY1):
        b += seg(X0_1, cy, X0_1 + SXT1 * TMAX1, cy, "currentColor", 1, "", .35)
        b += seg(X0_1, cy - 40, X0_1, cy + 40, "currentColor", 1.6)
        for uu in (4, -4):
            b += seg(X0_1, cy - SYC1 * uu, X0_1 + SXT1 * TMAX1, cy - SYC1 * uu, "currentColor", 1, "5 4", .3)
        b += lbl(10, cy + 5, f"({i + 1})", "currentColor", 14, "start", "700")
    for tt in range(int(TMAX1) + 1):
        x = X0_1 + SXT1 * tt
        b += seg(x, CY1[0] - 40, x, CY1[2] + 40, "currentColor", 1, "", .13) + seg(x, CY1[2] + 40, x, CY1[2] + 46, "currentColor", 1.4)
        b += lbl(x, CY1[2] + 62, str(tt), "currentColor", 12, "middle", "400")
    b += seg(X0_1, CY1[2] + 40, X0_1 + SXT1 * TMAX1, CY1[2] + 40, "currentColor", 1.6)
    b += lbl(X0_1 + SXT1 * TMAX1 + 20, CY1[2] + 80, "t (s)", "currentColor", 12, "end", "700") + lbl(X0_1 + 6, CY1[0] - 42, "x (cm), nét đứt: ±4 cm", "currentColor", 12, "start", "700")
    return b


def d1(k):
    p = f"d1{k}"; VB = "0 0 420 316"
    b = defs(p) + frame1()
    dt = 0.025; n = int(round(TMAX1 / dt)); dur = TMAX1
    for i in range(3):
        pts = [(X0_1 + SXT1 * j * dt, CY1[i] - SYC1 * u1(i, j * dt)) for j in range(n + 1)]
        if k == 0:
            cid = f"{p}c{i}"
            b += clip_grow(cid, X0_1, CY1[i] - 42, SXT1 * TMAX1, 84, dur)
            b += curve(path_d(pts), GRN, 2.6, .22) + f'<g clip-path="url(#{cid})">{curve(path_d(pts), GRN, 2.8)}</g>' + runner(pts, dur)
        else:
            b += curve(path_d(pts), GRN, 2.8)
    if k == 0:
        return fig("d1-0", VB, "Ba đồ thị li độ theo thời gian của ba con lắc trong 4 giây đầu", b,
                   "Mô phỏng: ba con lắc dao động (đúng thời gian thật, 4 s). Đồ thị tính theo công thức.")
    return fig("d1-2", VB, "Ba đồ thị li độ theo thời gian: (1) thả rồi để mặc, (2) có cơ cấu bù năng lượng, (3) đặt trên bệ rung", b,
               "Dữ kiện: T₀ = 1,0 s; (3) đặt trên bệ rung 1,5 Hz. " + NOTE)


# ═════════════ Dạng 2 · biển quảng cáo trên bàn rung: f0 = 3,5 Hz, b = 1,0 Hz, A_r = 6,0 cm ═════════════
F02, B2, AR2 = 3.5, 1.0, 6.0
TAB2 = [(2.0, 3.3), (3.0, 5.4), (3.5, 6.0), (4.0, 5.4), (5.0, 3.3), (6.0, 2.2)]


def amp(f, f0, b, ar):
    return ar * b / math.sqrt((f - f0) ** 2 + b * b)


def d2(k):
    p = f"d2{k}"
    if k == 0:
        VB = "0 0 420 206"; GY, XC, YT = 172, 210, 66
        f_try, slow, ncyc, per = 4.5, 10, 3, 24
        a_px = amp(f_try, F02, B2, AR2) * 5.0            # vẽ phóng đại 5 px/cm
        n = ncyc * per; dtr = 1.0 / (f_try * per); dur = n * dtr * slow
        dxs = [a_px * math.sin(2 * PI * f_try * j * dtr) for j in range(n + 1)]
        b = defs(p) + ground(GY, 40, 380)
        b += seg(XC, 18, XC, GY, "currentColor", 1.2, "5 4", .45) + lbl(XC + 6, 16, "vị trí cân bằng", "currentColor", 12, "start", "600")
        b += (f'<polyline fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" points="{XC},{GY} {XC},{YT}">'
              f'<animate attributeName="points" values="{";".join(f"{XC},{GY} {XC + d:.1f},{YT}" for d in dxs)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></polyline>')
        b += (f'<g transform="translate(0 0)"><rect x="{XC - 44}" y="{YT - 44}" width="88" height="40" rx="4" fill="none" stroke="{ORG}" stroke-width="2.6"/>'
              f'<text x="{XC}" y="{YT - 18}" fill="{ORG}" font-size="13" font-weight="700" text-anchor="middle">QUẢNG CÁO</text>'
              f'<animateTransform attributeName="transform" type="translate" values="{";".join(f"{d:.1f} 0" for d in dxs)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += arrow(p, "r", 60, GY + 22, 104, GY + 22, 2.4) + arrow(p, "r", 104, GY + 22, 60, GY + 22, 2.4) + lbl(112, GY + 27, "mặt đất rung đều", RED, 12, "start", "700")
        b += lbl(XC + 56, YT - 22, "biên độ A = ?", ORG, 13, "start", "700")
        return fig("d2-0", VB, "Biển quảng cáo trên cột dao động ngang khi mặt đất rung", b,
                   "Mô phỏng: cột rung ở một tần số thử 4,5 Hz (chạy chậm 10 lần, 3 chu kì), biên độ vẽ phóng đại. Biên độ tính theo mô hình của bài.")
    VB = "0 0 420 250"; X0, SX, YB, SY = 56, 68.0, 196, 20.0
    px = lambda f: X0 + SX * (f - 1.5); py = lambda a: YB - SY * a
    b = defs(p) + seg(X0, YB, X0 + SX * 5, YB, "currentColor", 1.6) + seg(X0, YB, X0, py(7), "currentColor", 1.6)
    for ff in range(2, 7):
        b += seg(px(ff), YB, px(ff), YB + 5, "currentColor", 1.4) + lbl(px(ff), YB + 22, str(ff), "currentColor", 12, "middle", "400")
    for aa in (2, 4, 6):
        b += seg(X0, py(aa), X0 + SX * 5, py(aa), "currentColor", 1, "", .13) + lbl(X0 - 6, py(aa) + 4, str(aa), "currentColor", 12, "end", "400")
    b += lbl(X0 + 6, py(7) + 4, "A (cm)", "currentColor", 12, "start", "700") + lbl(X0 + SX * 5 + 20, YB + 40, "f (Hz)", "currentColor", 12, "end", "700")
    for f, a in TAB2:
        b += seg(px(f), py(a + .2), px(f), py(a - .2), ORG, 3.5) + dot(px(f), py(a), 3, "currentColor")
    return fig("d2-2", VB, "Đồ thị các điểm đo biên độ theo tần số của bàn rung, mỗi điểm có thanh sai số 0,2 cm", b,
               "Dữ kiện: sáu điểm đo, thanh dọc là sai số đọc ±0,2 cm. " + NOTE)


# ═════════════ Dạng 3 · con lắc trong không khí: A0 = 5,0 cm, β = 0,20 /s, T ≈ 1,0 s ═════════════
A03, B3, T3 = 5.0, 0.20, 1.0
X0_3, SXT3, TMAX3, CY3, SYC3 = 56, 110.0, 3.0, 100, 14.0


def u3(t):
    return A03 * math.exp(-B3 * t) * math.cos(2 * PI * t / T3)


def d3(k):
    p = f"d3{k}"; VB = "0 0 420 224"
    b = defs(p)
    for tt in range(int(TMAX3) + 1):
        x = X0_3 + SXT3 * tt
        b += seg(x, CY3 - 76, x, CY3 + 76, "currentColor", 1, "", .13) + seg(x, CY3 + 76, x, CY3 + 82, "currentColor", 1.4) + lbl(x, CY3 + 100, str(tt), "currentColor", 12, "middle", "400")
    b += seg(X0_3, CY3, X0_3 + SXT3 * TMAX3, CY3, "currentColor", 1.2, "", .5) + seg(X0_3, CY3 - 76, X0_3, CY3 + 76, "currentColor", 1.6) + seg(X0_3, CY3 + 76, X0_3 + SXT3 * TMAX3, CY3 + 76, "currentColor", 1.6)
    b += lbl(X0_3 + 6, CY3 - 80, "x (cm)", "currentColor", 12, "start", "700") + lbl(X0_3 + SXT3 * TMAX3 + 20, CY3 + 118, "t (s)", "currentColor", 12, "end", "700")
    dt = 0.025; n = int(round(TMAX3 / dt))
    pts = [(X0_3 + SXT3 * j * dt, CY3 - SYC3 * u3(j * dt)) for j in range(n + 1)]
    if k == 0:
        cid = f"{p}c"
        b += clip_grow(cid, X0_3, CY3 - 78, SXT3 * TMAX3, 156, TMAX3)
        b += curve(path_d(pts), GRN, 2.6, .22) + f'<g clip-path="url(#{cid})">{curve(path_d(pts), GRN, 2.8)}</g>' + runner(pts, TMAX3)
        return fig("d3-0", VB, "Đồ thị li độ theo thời gian của con lắc dao động tắt dần trong 3 giây đầu", b,
                   "Mô phỏng: con lắc trong không khí, 3 s đầu (đúng thời gian thật). Đồ thị tính theo công thức của đề.")
    b += curve(path_d(pts), GRN, 2.8)
    b += dim(p, "o", X0_3 - 18, CY3, X0_3 - 18, CY3 - SYC3 * A03, "", 0, 0)
    b += lbl(X0_3 + 40, CY3 - SYC3 * A03 + 6, "A₀ = 5,0 cm", ORG, 13, "start", "700")
    return fig("d3-2", VB, "Đồ thị li độ theo thời gian của con lắc tắt dần, biên độ ban đầu A₀ = 5,0 cm", b,
               "Dữ kiện: A₀ = 5,0 cm; chu kì xấp xỉ 1,0 s; chỉ vẽ 3 s đầu. " + NOTE)


# ═════════════ Dạng 4 · xe qua gờ giảm tốc: L = 6,0 m, T0 = 0,80 s ═════════════
L4, T04 = 6.0, 0.80
F04 = 1 / T04
PXM = 80.0 / L4                     # 80 px ứng với L = 6,0 m
GY4, WR, BUMPS = 140, 7, [120, 200, 280, 360]


def road_h(x):
    return sum(8 * math.sqrt(1 - ((x - xb) / 12) ** 2) for xb in BUMPS if abs(x - xb) < 12)


def road(c="currentColor"):
    pts = [(x, GY4 - road_h(x)) for x in range(16, 405, 2)]
    return curve(path_d(pts), c, 2.4)


def car_body(x, y, c=GRN):
    return (f'<g transform="translate({x:.1f} {y:.1f})"><rect x="-32" y="-22" width="64" height="22" rx="5" fill="none" stroke="{c}" stroke-width="2.6"/>'
            f'<path d="M-16,-22 L-10,-34 L12,-34 L20,-22" fill="none" stroke="{c}" stroke-width="2.6" stroke-linejoin="round"/>')


def wheel(x, y):
    return f'<g transform="translate({x:.1f} {y:.1f})"><circle r="{WR}" fill="none" stroke="currentColor" stroke-width="2.4"/><circle r="2" fill="currentColor"/>'


def d4(k):
    p = f"d4{k}"; VB = "0 0 420 206"
    b = defs(p) + road()
    if k == 0:
        v_try = 5.0; vpx = v_try * PXM; f_try = v_try / L4
        a_px = amp(f_try, F04, 0.5, 6.0) * 3.0         # biên độ mô hình, vẽ phóng đại 3 px/cm
        xs, dtr = 40.0, 0.06; tend = (390 - xs) / vpx; n = int(tend / dtr) + 1; dur = n * dtr
        tc = (BUMPS[0] - xs) / vpx                       # lúc thân xe ở ngay trên gờ đầu: thân xe lên cao nhất (f ≪ f0, cùng pha với lực)
        body = [(xs + vpx * j * dtr, GY4 - 18 - a_px * math.cos(2 * PI * f_try * (j * dtr - tc))) for j in range(n + 1)]
        wh1 = [(xs + vpx * j * dtr - 18, GY4 - WR - road_h(xs + vpx * j * dtr - 18)) for j in range(n + 1)]
        wh2 = [(xs + vpx * j * dtr + 18, GY4 - WR - road_h(xs + vpx * j * dtr + 18)) for j in range(n + 1)]
        b += car_body(*body[0]) + xy_anim(body, dur) + "</g>"
        b += wheel(*wh1[0]) + xy_anim(wh1, dur) + "</g>" + wheel(*wh2[0]) + xy_anim(wh2, dur) + "</g>"
        b += dim(p, "o", BUMPS[1], 166, BUMPS[2], 166, "", 0, 0) + lbl((BUMPS[1] + BUMPS[2]) / 2, 186, "L = 6,0 m", ORG, 13, "middle", "700")
        b += lbl(BUMPS[3], 162, "gờ giảm tốc", "currentColor", 12, "middle", "600")
        b += lbl(24, 40, "thử ở 18 km/h", "currentColor", 13, "start", "700") + lbl(24, 60, "thân xe: biên độ vẽ phóng đại", "currentColor", 12, "start", "400")
        return fig("d4-0", VB, "Xe con chạy qua bốn gờ giảm tốc cách đều nhau, thân xe nhấp nhô", b,
                   "Mô phỏng: xe chạy thử 18 km/h qua các gờ cách đều (đúng thời gian thật). Biên độ nhấp nhô tính theo mô hình của bài, vẽ phóng đại.")
    b += car_body(70, GY4 - 18) + "</g>" + wheel(52, GY4 - WR) + "</g>" + wheel(88, GY4 - WR) + "</g>"
    b += arrow(p, "r", 110, GY4 - 40, 168, GY4 - 40, 3) + lbl(114, GY4 - 48, "v = ?", RED, 13, "start", "700")
    b += dim(p, "o", BUMPS[1], 166, BUMPS[2], 166, "", 0, 0) + lbl((BUMPS[1] + BUMPS[2]) / 2, 186, "L = 6,0 m", ORG, 13, "middle", "700")
    b += lbl(BUMPS[3], 162, "gờ giảm tốc", "currentColor", 12, "middle", "600") + lbl(26, 40, "T₀ = 0,80 s (chu kì riêng của xe)", "currentColor", 13, "start", "700")
    return fig("d4-2", VB, "Xe chạy với vận tốc v qua các gờ cách đều nhau L = 6,0 m; chu kì dao động riêng của xe T₀ = 0,80 s", b,
               "Dữ kiện: gờ cách đều L = 6,0 m, T₀ = 0,80 s. " + NOTE)


# ═════════════ Dạng 5 · máy bơm trên đệm chống rung: 20 Hz, f0 = 5,0 Hz; X (7,5 cm; 0,40 Hz), Y (2,0 cm; 1,5 Hz) ═════════════
X0_5, SXF5, FMAX5, YB5, SYA5 = 50, 17.0, 20.0, 176, 38.0


def frame5(p):
    b = seg(X0_5, YB5, X0_5 + SXF5 * FMAX5, YB5, "currentColor", 1.6) + seg(X0_5, YB5, X0_5, YB5 - SYA5 * 4.0, "currentColor", 1.6)
    for ff in (0, 5, 10, 15, 20):
        b += seg(X0_5 + SXF5 * ff, YB5, X0_5 + SXF5 * ff, YB5 + 5, "currentColor", 1.4) + lbl(X0_5 + SXF5 * ff, YB5 + 22, str(ff), "currentColor", 12, "middle", "400")
    for aa in (1, 2, 3):
        b += seg(X0_5, YB5 - SYA5 * aa, X0_5 + SXF5 * FMAX5, YB5 - SYA5 * aa, "currentColor", 1, "", .13) + lbl(X0_5 - 6, YB5 - SYA5 * aa + 4, str(aa), "currentColor", 12, "end", "400")
    return b + lbl(X0_5 + 6, YB5 - SYA5 * 4.0 + 2, "A (cm)", "currentColor", 12, "start", "700") + lbl(X0_5 + SXF5 * FMAX5 + 20, YB5 + 40, "f (Hz)", "currentColor", 12, "end", "700")


def d5(k):
    p = f"d5{k}"; VB = "0 0 420 230"
    b = defs(p) + frame5(p)
    if k == 0:
        f0t, bt, art = 8.0, 1.0, 3.0                       # đệm thử Z (không phải X, Y)
        n = 200; pts = [(X0_5 + SXF5 * 20.0 * j / n, YB5 - SYA5 * amp(20.0 * j / n, f0t, bt, art)) for j in range(n + 1)]
        dur = 6.0; cid = f"{p}c"
        b += clip_grow(cid, X0_5, YB5 - SYA5 * 4.0, SXF5 * FMAX5, SYA5 * 4.0 + 4, dur)
        b += curve(path_d(pts), GRN, 2.6, .22) + f'<g clip-path="url(#{cid})">{curve(path_d(pts), GRN, 2.8)}</g>' + runner(pts, dur)
        b += lbl(X0_5 + 6, YB5 - SYA5 * 4.0 + 22, "đệm thử (không phải X, Y)", "currentColor", 12, "start", "700")
        return fig("d5-0", VB, "Biên độ rung của bệ theo tần số lực khi máy khởi động, tần số tăng đều từ 0 đến 20 hertz", b,
                   "Mô phỏng: một đệm thử, tần số lực tăng đều 0 → 20 Hz trong 6 s (nhanh hơn thật). Đồ thị tính theo mô hình A(f) của bài.")
    xf = lambda f: X0_5 + SXF5 * f
    b += seg(xf(5), YB5, xf(5), YB5 - SYA5 * 3.6, ORG, 2, "5 4") + lbl(xf(5) + 6, YB5 - SYA5 * 3.6 + 6, "f₀ = 5,0 Hz", ORG, 13, "start", "700")
    b += seg(xf(20), YB5, xf(20), YB5 - SYA5 * 2.2, RED, 2, "5 4") + lbl(xf(20) - 6, YB5 - SYA5 * 2.2 - 6, "chạy ổn định 20 Hz", RED, 13, "end", "700")
    b += arrow(p, "b", xf(0.6), YB5 - SYA5 * 0.5, xf(19), YB5 - SYA5 * 0.5, 3) + lbl(xf(6.5), YB5 - SYA5 * 0.5 - 8, "khởi động: tần số lực tăng dần", BLUE, 13, "start", "700")
    return fig("d5-2", VB, "Trục tần số: khi khởi động, tần số lực tăng từ 0 lên 20 hertz và đi qua tần số riêng 5,0 hertz của đệm", b,
               "Dữ kiện: f₀ = 5,0 Hz của cả hai đệm; máy chạy ổn định ở 20 Hz. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ───────────────────────── Đề + bảng phân tích ─────────────────────────
TB2 = ('<div class="table-scroll"><table class="tl-table"><thead><tr><th>$f$ (Hz)</th><th>$2{,}0$</th><th>$3{,}0$</th><th>$3{,}5$</th><th>$4{,}0$</th><th>$5{,}0$</th><th>$6{,}0$</th></tr></thead>'
       '<tbody><tr><td>$A$ (cm)</td><td>$3{,}3$</td><td>$5{,}4$</td><td>$6{,}0$</td><td>$5{,}4$</td><td>$3{,}3$</td><td>$2{,}2$</td></tr></tbody></table></div>')

DANG = [
 dict(form="ly_thuyet", label="Dạng 1 · Dễ · Phân biệt dao động tắt dần, duy trì, cưỡng bức",
      topic="Dao động tắt dần và nguyên nhân",
      problem_html=(r"<p>Ba con lắc lò xo giống nhau, mỗi con lắc có chu kì riêng $T_0=1{,}0\ \text{s}$. Đồ thị li độ theo thời gian của cả ba trong $4\ \text{s}$ đầu như hình vẽ.</p>"
                    r"<ul><li>(1): kéo lệch $4{,}0\ \text{cm}$ rồi thả, để mặc trong không khí.</li>"
                    r"<li>(2): như (1), nhưng có cơ cấu cấp thêm năng lượng cho vật, mỗi chu kì cấp đúng phần năng lượng đã mất vì ma sát.</li>"
                    r"<li>(3): đặt trên một bệ rung; bệ rung với tần số $1{,}5\ \text{Hz}$, tác dụng lực tuần hoàn lên vật liên tục, vật đã dao động ổn định.</li></ul>"
                    r"<ol type='a'><li>Mỗi con lắc dao động tắt dần, duy trì hay cưỡng bức?</li><li>Chu kì dao động của con lắc (3) là bao nhiêu?</li></ol>")),
 dict(form="ly_thuyet", label="Dạng 2 · Trung bình · Cộng hưởng qua bảng quét tần số: tìm $f_0$, tần số dao động, so biên độ với sai số",
      topic="Dao động cưỡng bức và hiện tượng cộng hưởng",
      problem_html=(r"<p>Một biển quảng cáo gắn trên cột cao cạnh đường. Để kiểm tra, người ta đặt cột lên bàn rung, cho bàn rung với các tần số $f$ khác nhau nhưng cùng một lực, chờ dao động ổn định rồi đọc biên độ $A$ của đỉnh cột (sai số đọc $\pm0{,}2\ \text{cm}$):</p>"
                    + TB2 +
                    r"<ol type='a'><li>Tìm tần số riêng $f_0$ của cột.</li>"
                    r"<li>Ngoài đường, xe tải chạy qua làm mặt đất rung đều với tần số $5{,}0\ \text{Hz}$. Khi đã ổn định, cột dao động với tần số bao nhiêu?</li>"
                    r"<li>Xe tải chạy chậm lại, mặt đất rung với tần số $4{,}0\ \text{Hz}$. Biên độ của cột tăng hay giảm so với lúc $5{,}0\ \text{Hz}$? Chênh lệch có vượt sai số đọc không?</li></ol>")),
 dict(form="bai_tap", label="Dạng 3 · Trung bình · Dao động tắt dần: biên độ theo thời gian, lúc còn một nửa biên độ, phần cơ năng còn lại",
      topic="Dao động tắt dần và nguyên nhân",
      problem_html=(r"<p>Một con lắc đơn nhỏ dao động trong không khí, chu kì xấp xỉ $1{,}0\ \text{s}$, biên độ ban đầu $A_0=5{,}0\ \text{cm}$. Biên độ giảm dần theo $A=A_0e^{-\beta t}$ với $\beta=0{,}20\ \text{s}^{-1}$ (bỏ qua việc lực cản làm đổi chu kì).</p>"
                    r"<ol type='a'><li>Tính biên độ sau $t=5{,}0\ \text{s}$.</li>"
                    r"<li>Sau bao lâu kể từ lúc thả thì biên độ chỉ còn một nửa biên độ ban đầu?</li>"
                    r"<li>Lúc đó, cơ năng của con lắc còn bao nhiêu phần trăm cơ năng ban đầu?</li></ol>")),
 dict(form="bai_tap", label="Dạng 4 · Khó · Xe qua gờ giảm tốc: chu kì ngoại lực, vận tốc cộng hưởng, so hai vận tốc",
      topic="Dao động cưỡng bức và hiện tượng cộng hưởng",
      problem_html=(r"<p>Một xe con chạy trên đường có các gờ giảm tốc cách đều nhau $L=6{,}0\ \text{m}$. Hệ thân xe và lò xo treo dao động theo phương thẳng đứng với chu kì riêng $T_0=0{,}80\ \text{s}$. "
                    r"Mỗi lần bánh xe qua một gờ, xe bị đẩy một lần; các gờ liên tiếp làm thành ngoại lực tuần hoàn tác dụng lên thân xe.</p>"
                    r"<ol type='a'><li>Xe chạy $36\ \text{km/h}$. Chu kì của ngoại lực là bao nhiêu?</li>"
                    r"<li>Xe phải chạy với vận tốc bao nhiêu km/h để thân xe rung mạnh nhất?</li>"
                    r"<li>Với hai vận tốc $36\ \text{km/h}$ và $54\ \text{km/h}$ (lực và lực cản như nhau), vận tốc nào làm thân xe rung mạnh hơn? Vì sao?</li></ol>")),
 dict(form="bai_tap", label="Dạng 5 · Nâng cao · Chọn đệm chống rung: biên độ lúc chạy ổn định và lúc khởi động đi qua cộng hưởng",
      topic="Dao động cưỡng bức và hiện tượng cộng hưởng",
      problem_html=(r"<p>Một máy bơm đặt trên bệ có đệm chống rung. Khi chạy ổn định, máy tạo lực tuần hoàn tác dụng lên bệ với tần số $20\ \text{Hz}$. Khi khởi động, tần số lực tăng dần từ $0$ lên $20\ \text{Hz}$ nên đi qua tần số riêng $f_0$ của bệ. "
                    r"Với lực cùng độ lớn, biên độ rung của bệ ở tần số lực $f$ tính gần đúng theo $A(f)=\dfrac{A_r\,b}{\sqrt{(f-f_0)^2+b^2}}$.</p>"
                    r"<p>Hai loại đệm đều có $f_0=5{,}0\ \text{Hz}$: đệm X có $A_r=7{,}5\ \text{cm}$, $b=0{,}40\ \text{Hz}$; đệm Y có $A_r=2{,}0\ \text{cm}$, $b=1{,}5\ \text{Hz}$. "
                    r"Yêu cầu: lúc chạy ổn định, $A\le0{,}30\ \text{cm}$; lúc đi qua cộng hưởng khi khởi động, $A\le3{,}0\ \text{cm}$.</p>"
                    r"<ol type='a'><li>Tính biên độ lúc chạy ổn định của từng đệm.</li><li>Tìm biên độ lớn nhất của từng đệm lúc khởi động.</li><li>Nên chọn đệm nào? Vì sao?</li></ol>")),
]

ANALYSIS = [
 [("\"kéo lệch $4{,}0$ cm rồi thả, để mặc trong không khí\"  (con lắc 1)", "Chỉ có lực cản; không có gì cấp thêm", "Có ngoại lực hay cơ cấu cấp năng lượng nào tác dụng thêm không?"),
  ("\"cơ cấu cấp … đúng phần năng lượng đã mất vì ma sát\"  (con lắc 2)", "Bù năng lượng sau mỗi chu kì", "Cấp một phần chu kì hay suốt chu kì? Khác gì ngoại lực liên tục?"),
  ("\"bệ rung … $1{,}5$ Hz, tác dụng lực tuần hoàn lên vật liên tục\"  (con lắc 3)", "$f_{lực}=1{,}5$ Hz; $T_0=1{,}0$ s", "⚠ Phân loại theo cách năng lượng được cấp, không chỉ nhìn biên độ trên đồ thị"),
  ("\"tắt dần, duy trì hay cưỡng bức?\"", "Gọi tên cả ba con lắc", "Tắt dần · duy trì · cưỡng bức: mỗi loại khác nhau ở đâu?"),
  ("\"chu kì dao động của con lắc (3)\"", "Cần $T$ của (3)", "$T=\\dfrac{1}{f}$ — $f$ của đại lượng nào khi đã ổn định?")],
 [("\"cho bàn rung … nhưng cùng một lực, chờ dao động ổn định\"", "Lực không đổi; đọc lúc ổn định", "⚠ Chỉ so các biên độ với nhau khi lực như nhau và đã ổn định"),
  ("\"bảng $f$ và $A$ (sai số đọc $\\pm0{,}2$ cm)\"", "Sáu cặp $(f;A)$; sai số $\\pm0{,}2$ cm", "Hai số đọc khác nhau thật khi hiệu của chúng vượt sai số"),
  ("\"tìm tần số riêng $f_0$\"", "Cần $f_0$", "Cộng hưởng: biên độ cực đại khi $f=f_0$"),
  ("\"mặt đất rung đều với tần số $5{,}0$ Hz\"", "$f_{lực}=5{,}0$ Hz", "Dao động cưỡng bức ổn định theo nhịp của đại lượng nào?"),
  ("\"rung với tần số $4{,}0$ Hz … tăng hay giảm … vượt sai số?\"", "$f=4{,}0$ Hz và $f=5{,}0$ Hz", "Biên độ phụ thuộc $|f-f_0|$; so hiệu hai biên độ với sai số đọc")],
 [("\"dao động trong không khí … $A=A_0e^{-\\beta t}$, $\\beta=0{,}20$ s$^{-1}$\"", "$A_0=5{,}0$ cm; $\\beta=0{,}20\\ \\text{s}^{-1}$", "⚠ Mô hình bỏ qua việc lực cản đổi chu kì; $\\beta t$ không có đơn vị"),
  ("\"tính biên độ sau $t=5{,}0$ s\"", "$t=5{,}0$ s", "$A=A_0e^{-\\beta t}$"),
  ("\"biên độ chỉ còn một nửa\"", "$A=\\dfrac{A_0}{2}$", "Giải $e^{-\\beta t}=\\dfrac12$ bằng logarit"),
  ("\"cơ năng còn bao nhiêu phần trăm\"", "Cần $\\dfrac{W}{W_0}$", "⚠ Cơ năng tỉ lệ $A^2$, không tỉ lệ $A$; $\\dfrac{W}{W_0}=\\left(\\dfrac{A}{A_0}\\right)^2$")],
 [("\"gờ giảm tốc cách đều nhau $L=6{,}0$ m\"", "$L=6{,}0$ m", "Ngoại lực tuần hoàn có chu kì bằng thời gian xe đi giữa hai gờ liên tiếp"),
  ("\"chu kì riêng $T_0=0{,}80$ s\"", "$T_0=0{,}80$ s", "Cộng hưởng khi $T=T_0$ (hay $f=f_0$)"),
  ("\"xe chạy $36$ km/h\"", "$v=36$ km/h", "⚠ Đổi km/h sang m/s (chia $3{,}6$) trước khi dùng $T=\\dfrac{L}{v}$"),
  ("\"chu kì của ngoại lực\"", "Cần $T$", "$T=\\dfrac{L}{v}$"),
  ("\"vận tốc để thân xe rung mạnh nhất\"", "Cần $v$ khi cộng hưởng", "$T=T_0$, rồi $v=\\dfrac{L}{T}$ (đổi sang km/h)"),
  ("\"$36$ km/h và $54$ km/h … lực và lực cản như nhau … rung mạnh hơn\"", "Hai vận tốc, so hai biên độ", "⚠ Biên độ lớn hơn khi $|f-f_0|$ nhỏ hơn, không phải khi xe chạy nhanh hơn")],
 [("\"khi chạy ổn định … lực tần số $20$ Hz\"", "$f_{ổn}=20$ Hz", "Dao động cưỡng bức ổn định: $f_{vật}=f_{lực}$"),
  ("\"khi khởi động, tần số lực tăng dần từ $0$ lên $20$ Hz\"", "$f$ quét từ $0$ đến $20$ Hz, đi qua $f_0=5{,}0$ Hz", "⚠ Có lúc $f=f_0$ ngay trong khi khởi động: cộng hưởng"),
  ("\"$A(f)=\\dfrac{A_r\\,b}{\\sqrt{(f-f_0)^2+b^2}}$ (lực cùng độ lớn)\"", "Mô hình đề cho", "Khi $f=f_0$: $A=A_r$ · khi $f$ xa $f_0$: xét $|f-f_0|$ so với $b$"),
  ("\"đệm X: $A_r=7{,}5$ cm, $b=0{,}40$ Hz; đệm Y: $A_r=2{,}0$ cm, $b=1{,}5$ Hz\"", "Hai bộ $(A_r;b)$", "Cản nhỏ: đỉnh cao, hẹp · cản lớn: đỉnh thấp, thoải"),
  ("\"lúc chạy ổn định $A\\le0{,}30$ cm; lúc qua cộng hưởng $A\\le3{,}0$ cm\"", "Hai ngưỡng", "So biên độ tính được với từng ngưỡng"),
  ("\"nên chọn đệm nào?\"", "Cần chọn", "Đệm thoả cả hai yêu cầu")],
]

R1 = ["<strong>Khái niệm:</strong> tắt dần – biên độ giảm vì lực cản; duy trì – bù đúng phần mất, chỉ một phần chu kì; cưỡng bức – lực tuần hoàn tác dụng liên tục.",
      "<strong>Công thức:</strong> $T=\\dfrac{1}{f}$.",
      "Duy trì: chu kì là chu kì riêng · cưỡng bức ổn định: $f_{vật}=f_{lực}$, có thể khác $f_0$.",
      "⚠ <strong>Điều kiện:</strong> phân loại theo cách năng lượng được cấp, không chỉ theo biên độ."]
R2 = ["<strong>Khái niệm:</strong> cộng hưởng – biên độ cưỡng bức cực đại khi $f=f_0$.",
      "Lực và lực cản không đổi: $|f-f_0|$ càng nhỏ, biên độ càng lớn.",
      "Cưỡng bức ổn định: $f_{vật}=f_{lực}$.",
      "⚠ <strong>Điều kiện:</strong> hai số đọc chỉ khác nhau thật khi hiệu của chúng vượt sai số đọc."]
R3 = ["<strong>Khái niệm:</strong> tắt dần – biên độ và cơ năng giảm dần, cơ năng thành nhiệt.",
      "<strong>Công thức:</strong> $A=A_0e^{-\\beta t}$ · cơ năng $W\\sim A^2$ (bài năng lượng dao động điều hoà) nên $\\dfrac{W}{W_0}=\\left(\\dfrac{A}{A_0}\\right)^2$.",
      "Giải $e^{-x}=\\dfrac12$ bằng logarit (Toán 11): $x=\\ln2\\approx0{,}693$.",
      "⚠ <strong>Điều kiện:</strong> $\\beta t$ không có đơn vị; $\\beta$ (s$^{-1}$) nhân với $t$ (s)."]
R4 = ["<strong>Khái niệm:</strong> các gờ cách đều làm thành ngoại lực tuần hoàn; cộng hưởng khi $T=T_0$ (hay $f=f_0$).",
      "<strong>Công thức:</strong> $T=\\dfrac{L}{v}$ · $f=\\dfrac{v}{L}$ · $1\\ \\text{m/s}=3{,}6\\ \\text{km/h}$.",
      "Lực và cản như nhau: biên độ lớn hơn khi $|f-f_0|$ nhỏ hơn.",
      "⚠ <strong>Điều kiện:</strong> $L$, $v$ cùng hệ đơn vị (m, m/s)."]
R5 = ["<strong>Khái niệm:</strong> cưỡng bức ổn định: $f_{vật}=f_{lực}$ · cộng hưởng khi $f=f_0$.",
      "<strong>Công thức:</strong> $A(f)=\\dfrac{A_r\\,b}{\\sqrt{(f-f_0)^2+b^2}}$ · $A(f_0)=A_r$.",
      "Cản nhỏ: đỉnh cao, hẹp · cản lớn: đỉnh thấp, thoải.",
      "⚠ <strong>Điều kiện:</strong> máy khởi động thì tần số lực quét qua mọi giá trị từ $0$ đến tần số chạy ổn định."]

SOLS = [
 sol(R1, [
  ("Con lắc (1)", [P("Kéo lệch rồi thả trong không khí: chỉ có lực cản, không có gì cấp thêm năng lượng."), P("Cơ năng thành nhiệt nên biên độ giảm dần, đúng như đồ thị (1)."), A("T:(1) dao động <strong>tắt dần</strong>.")]),
  ("Con lắc (2)", [P("Cơ cấu cấp đúng phần năng lượng mất đi sau mỗi chu kì, chỉ một phần của chu kì, không đẩy suốt."), P("Biên độ giữ nguyên, chu kì vẫn là chu kì riêng $T_0=1{,}0$ s."), A("T:(2) dao động <strong>duy trì</strong>.")]),
  ("Con lắc (3)", [P("Bệ tác dụng lực tuần hoàn lên vật suốt thời gian, không phải chỉ một phần chu kì."), P("Dao động ổn định theo nhịp của lực, không theo nhịp riêng của vật."), A("T:(3) dao động <strong>cưỡng bức</strong>.")]),
  ("Chu kì của con lắc (3)", [P("Lúc ổn định, tần số vật bằng tần số lực:"), M(r"f_{vật}=f_{lực}=1{,}5\ \text{Hz}"), M(r"T=\dfrac{1}{f}=\dfrac{1}{1{,}5}"), A(r"T\approx0{,}67\ \text{s}")]),
  ("Kiểm tra", [P("Trong $4$ s đồ thị (3) có $\\dfrac{4}{0{,}67}\\approx6$ chu kì ✓, dày hơn (1) và (2) là $4$ chu kì."), P("$T_0=1{,}0$ s chỉ là chu kì riêng; không phải chu kì của (3).")])],
  ["a) (1) tắt dần · (2) duy trì · (3) cưỡng bức", r"b) $T\approx0{,}67\ \text{s}$"],
  "Nhận dạng: đề cho <strong>cách năng lượng được cấp</strong> cho dao động → xếp loại; cưỡng bức ổn định thì lấy tần số của <strong>lực</strong>, không lấy $f_0$."),
 sol(R2, [
  ("Tần số riêng $f_0$", [P("$A$ lớn nhất là $6{,}0$ cm tại $f=3{,}5$ Hz."), P("Hai bên đối xứng: $3{,}0$ Hz và $4{,}0$ Hz cùng $5{,}4$ cm; $2{,}0$ Hz và $5{,}0$ Hz cùng $3{,}3$ cm."), P("Hiệu đỉnh với hàng kề: $6{,}0-5{,}4=0{,}6$ cm, lớn hơn $0{,}2$ cm nên đỉnh không nhầm."), A(r"f_0=3{,}5\ \text{Hz}")]),
  ("Tần số dao động của cột", [P("Dao động cưỡng bức đã ổn định thì tần số vật bằng tần số lực:"), A(r"f_{vật}=f_{lực}=5{,}0\ \text{Hz}")]),
  ("Biên độ ở $4{,}0$ Hz so với $5{,}0$ Hz", [M(r"|4{,}0-3{,}5|=0{,}5\ \text{Hz}"), M(r"|5{,}0-3{,}5|=1{,}5\ \text{Hz}"), A("T:$4{,}0$ Hz gần $f_0$ hơn nên biên độ <strong>tăng</strong>: từ $3{,}3$ cm lên $5{,}4$ cm.")]),
  ("Chênh lệch so với sai số", [M(r"5{,}4-3{,}3"), A(r"\Delta A=2{,}1\ \text{cm}"), P("Lớn hơn nhiều so với sai số $0{,}2$ cm nên chênh lệch thật, không do đọc số.")]),
  ("Kiểm tra", [P("Bảng đối xứng quanh $3{,}5$ Hz: $3{,}0$ và $4{,}0$ cùng $5{,}4$; $2{,}0$ và $5{,}0$ cùng $3{,}3$ ✓."), P("Lực không đổi, nên chỉ $|f-f_0|$ làm biên độ đổi ✓.")])],
  [r"a) $f_0=3{,}5\ \text{Hz}$", r"b) $5{,}0\ \text{Hz}$", r"c) tăng $2{,}1\ \text{cm}$, vượt sai số đọc"],
  "Nhận dạng: đề cho <strong>bảng quét tần số kèm sai số đọc</strong> → đỉnh bảng là $f_0$; tần số cột lấy theo lực; so biên độ qua $|f-f_0|$ và sai số."),
 sol(R3, [
  ("Biên độ sau $5{,}0$ s", [P("Thế vào mô hình, $\\beta t=0{,}20\\cdot5{,}0=1{,}0$ (không đơn vị):"), M(r"A=A_0e^{-\beta t}=5{,}0\,e^{-1{,}0}"), A(r"A\approx1{,}8\ \text{cm}")]),
  ("Lúc còn một nửa biên độ", [P("Đặt $A=\\dfrac{A_0}{2}$:"), M(r"e^{-\beta t}=\dfrac12\ \Rightarrow\ \beta t=\ln2"), M(r"t=\dfrac{\ln2}{\beta}=\dfrac{0{,}693}{0{,}20}"), A(r"t\approx3{,}5\ \text{s}")]),
  ("Cơ năng còn lại", [P("Cơ năng tỉ lệ bình phương biên độ:"), M(r"\dfrac{W}{W_0}=\left(\dfrac{A}{A_0}\right)^2=\left(\dfrac12\right)^2"), A(r"\dfrac{W}{W_0}=0{,}25=25\%")]),
  ("Kiểm tra", [P("Biên độ còn một nửa lúc $3{,}5$ s, trước $5{,}0$ s; ở $5{,}0$ s biên độ $1{,}8$ cm nhỏ hơn $2{,}5$ cm ✓."), P("Cơ năng lúc $5{,}0$ s: $\\left(\\dfrac{1{,}84}{5{,}0}\\right)^2\\approx13{,}5\\%$, nhỏ hơn $25\\%$ ✓.")])],
  [r"a) $A\approx1{,}8\ \text{cm}$", r"b) $t\approx3{,}5\ \text{s}$", r"c) còn $25\%$ cơ năng"],
  "Nhận dạng: đề cho <strong>biên độ giảm theo hàm mũ</strong> và hỏi <strong>cơ năng</strong> → biên độ theo $e^{-\\beta t}$, cơ năng theo bình phương biên độ."),
 sol(R4, [
  ("Đổi đơn vị", [M(r"v=\dfrac{36}{3{,}6}"), A(r"v=10\ \text{m/s}")]),
  ("Chu kì ngoại lực", [P("Hai gờ liên tiếp cách $L$, xe đi hết thời gian:"), M(r"T=\dfrac{L}{v}=\dfrac{6{,}0}{10}"), A(r"T=0{,}60\ \text{s}")]),
  ("Vận tốc gây cộng hưởng", [P("Cộng hưởng khi $T=T_0=0{,}80$ s:"), M(r"v=\dfrac{L}{T_0}=\dfrac{6{,}0}{0{,}80}=7{,}5\ \text{m/s}"), M(r"v=7{,}5\cdot3{,}6"), A(r"v=27\ \text{km/h}")]),
  ("So $36$ km/h và $54$ km/h", [P("$f_0=\\dfrac{1}{T_0}=1{,}25$ Hz. Ở $36$ km/h ($10$ m/s): $f=\\dfrac{v}{L}=\\dfrac{10}{6{,}0}\\approx1{,}67$ Hz."), P("Ở $54$ km/h ($15$ m/s): $f=\\dfrac{15}{6{,}0}=2{,}5$ Hz."), M(r"|1{,}67-1{,}25|=0{,}42\ \text{Hz}\ \lt\ |2{,}5-1{,}25|=1{,}25\ \text{Hz}"), A("T:<strong>36 km/h</strong> làm thân xe rung mạnh hơn, vì tần số lực gần $f_0$ hơn.")]),
  ("Kiểm tra", [P("$7{,}5\\ \\text{m/s}\\cdot0{,}80\\ \\text{s}=6{,}0$ m đúng bằng $L$ ✓."), P("Cách khác: $|v-27|$ là $9$ km/h và $27$ km/h, cũng cho $36$ km/h gần cộng hưởng hơn ✓.")])],
  [r"a) $T=0{,}60\ \text{s}$", r"b) $v=27\ \text{km/h}$", r"c) $36\ \text{km/h}$ rung mạnh hơn (tần số lực gần $f_0$ hơn)"],
  "Nhận dạng: đề cho <strong>các gờ cách đều và chu kì riêng của xe</strong> → $T=\\dfrac{L}{v}$, cộng hưởng khi $T=T_0$; so vận tốc bằng độ lệch tần số, không bằng độ nhanh."),
 sol(R5, [
  ("Hai tần số cần kiểm", [P("Chạy ổn định: tần số lực $20$ Hz."), P("Khởi động: tần số lực quét từ $0$ đến $20$ Hz nên có lúc đúng $f=f_0=5{,}0$ Hz."), A("T:Kiểm hai biên độ: tại <strong>20 Hz</strong> và tại <strong>$f_0$</strong>.")]),
  ("Đệm X lúc chạy ổn định", [M(r"A_X=\dfrac{A_r\,b}{\sqrt{(f-f_0)^2+b^2}}=\dfrac{7{,}5\cdot0{,}40}{\sqrt{(20-5{,}0)^2+0{,}40^2}}"), M(r"A_X=\dfrac{3{,}0}{15{,}005}"), A(r"A_X\approx0{,}20\ \text{cm}")]),
  ("Đệm Y lúc chạy ổn định", [M(r"A_Y=\dfrac{2{,}0\cdot1{,}5}{\sqrt{(20-5{,}0)^2+1{,}5^2}}=\dfrac{3{,}0}{15{,}075}"), A(r"A_Y\approx0{,}20\ \text{cm}"), P("Xa $f_0$ thì mẫu số gần bằng $|f-f_0|$, lực cản hầu như không đổi kết quả; hai đệm cùng đạt $A\\le0{,}30$ cm.")]),
  ("Lúc khởi động qua $f_0$", [P("Khi $f=f_0$ thì $A=A_r$:"), M(r"A_X=7{,}5\ \text{cm}\ \gt\ 3{,}0\ \text{cm}"), M(r"A_Y=2{,}0\ \text{cm}\ \lt\ 3{,}0\ \text{cm}"), A("T:Chỉ đệm Y đạt yêu cầu khi khởi động.")]),
  ("Chọn đệm", [P("Hai đệm bằng nhau lúc chạy ổn định; khác nhau ở lúc đi qua cộng hưởng. Lực cản lớn hạ đỉnh cộng hưởng."), A("T:Chọn <strong>đệm Y</strong> (cản lớn).")]),
  ("Kiểm tra", [P("Cả hai đệm có $A_r\\,b=3{,}0$ cm·Hz (cùng lực) nên $A$ lúc chạy ổn định gần bằng nhau ✓."), P("$A_r$ gấp $3{,}75$ lần, $b$ nhỏ đi $3{,}75$ lần ✓ ($7{,}5/2{,}0$ và $1{,}5/0{,}40$).")])],
  [r"a) $A_X\approx A_Y\approx0{,}20\ \text{cm}$", r"b) $A_X=7{,}5\ \text{cm}$, $A_Y=2{,}0\ \text{cm}$", "c) chọn đệm Y: ổn định như nhau, khởi động đạt yêu cầu"],
  "Nhận dạng: đề có <strong>khởi động (tần số quét từ 0)</strong> và tần số chạy ổn định → kiểm hai chỗ: $f=f_{ổn}$ và $f=f_0$."),
]

# ───────────────────────── Tự giải từng bước (9/10/2026) ─────────────────────────
LOAI = ("Tắt dần", "Duy trì", "Cưỡng bức")


def loai_choices(dung, vi_sao):
    """3 lựa chọn loại dao động; `dung` là chỉ số đúng; vi_sao: dict chỉ số → lí do sai."""
    return [(LOAI[i], True if i == dung else vi_sao[i]) for i in range(3)]


STEPS = [
 dict(nhan_dang="Thấy <b>cách cấp năng lượng</b> cho dao động → xếp loại; cưỡng bức ổn định lấy tần số của <b>lực</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Con lắc (1)", "Con lắc (1) thuộc loại dao động nào?",
       loi="Thấy con lắc vẫn đang dao động nên gọi là duy trì; duy trì cần có cơ cấu bù năng lượng, ở (1) không có gì cấp thêm.",
       lua_chon=loai_choices(0, {1: "Duy trì phải được cấp thêm năng lượng đúng phần mất; ở (1) chỉ thả rồi để mặc.",
                                 2: "Cưỡng bức cần ngoại lực tuần hoàn tác dụng liên tục; ở (1) không có lực nào như vậy."})),
  buoc("Con lắc (2)", "Con lắc (2) thuộc loại dao động nào?",
       loi="Cho rằng cơ cấu cấp năng lượng thì là cưỡng bức; cưỡng bức là lực tuần hoàn tác dụng suốt, còn duy trì chỉ bù một phần chu kì.",
       lua_chon=loai_choices(1, {0: "Biên độ không giảm vì phần mất đã được bù, nên không phải tắt dần.",
                                 2: "Cơ cấu chỉ bù phần đã mất sau mỗi chu kì, không đẩy suốt chu kì và không đặt nhịp mới."}),
       ke=[("So cách cấp năng lượng của (2) với (1): có bù sau mỗi chu kì không", True),
           ("Chỉ nhìn đồ thị (2) rồi gọi tên theo biên độ không đổi", "Biên độ không đổi cũng gặp ở cưỡng bức; phải xét năng lượng được cấp bằng cách nào."),
           ("Dùng kết quả của (1) vì cùng là con lắc lò xo", "Mỗi con lắc có điều kiện riêng; (2) có thêm cơ cấu bù nên khác (1).")]),
  buoc("Con lắc (3)", "Con lắc (3) thuộc loại dao động nào?",
       loi="Thấy biên độ không đổi giống (2) nên gọi là duy trì; ở (3) lực tuần hoàn từ bệ tác dụng liên tục và áp đặt nhịp của bệ.",
       lua_chon=loai_choices(2, {0: "Biên độ không giảm vì có lực tuần hoàn liên tục từ bệ, nên không phải tắt dần.",
                                 1: "Duy trì chỉ bù một phần chu kì và giữ chu kì riêng; ở (3) lực tác dụng suốt chu kì và vật theo nhịp của bệ."}),
       ke=[("Xét lực từ bệ: tác dụng suốt hay chỉ một phần chu kì, tần số của lực là bao nhiêu", True),
           ("Gọi tên theo biên độ: không đổi thì là duy trì", "Cả duy trì và cưỡng bức đều có biên độ không đổi; phải xét lực."),
           ("Gọi tên theo chu kì riêng $T_0$ của con lắc", "Cưỡng bức ổn định thì vật theo nhịp của lực, không theo $T_0$.")]),
  buoc("Chu kì của con lắc (3)", "Chu kì dao động của con lắc (3) bằng bao nhiêu giây?", 0.67, "s", 0.01,
       loi="Lấy $T_0=1{,}0$ s vì \"là con lắc ấy\"; lúc ổn định, tần số vật bằng tần số của lực nên $T=\\dfrac{1}{f_{lực}}$.",
       ke=[("Lấy tần số của lực rồi $T=\\dfrac{1}{f}$", True),
           ("Lấy chu kì riêng $T_0$ của con lắc", "$T_0$ chỉ là chu kì khi con lắc dao động tự do; lúc ổn định, vật theo nhịp của lực."),
           ("Cộng $T_0$ với chu kì của lực", "Không có quy tắc cộng chu kì; chu kì ổn định chỉ bằng chu kì của lực.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang="Đề cho <b>bảng quét tần số</b> → đỉnh bảng là $f_0$; tần số vật theo lực; so biên độ qua $|f-f_0|$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tần số riêng $f_0$", "Tần số riêng $f_0$ của cột bằng bao nhiêu Hz?", 3.5, "Hz", 0.05,
       loi="Lấy $5{,}0$ Hz (tần số xe tải gây ra) hoặc lấy số $6{,}0$ ở hàng biên độ; $f_0$ là tần số ở hàng có $A$ lớn nhất."),
  buoc("Tần số dao động của cột", "Khi mặt đất rung đều ở $5{,}0$ Hz và đã ổn định, cột dao động với tần số bao nhiêu Hz?", 5, "Hz", 0.05,
       loi="Trả lời $f_0$ vì \"cột có tần số riêng\"; lúc ổn định, vật theo nhịp của lực nên tần số là của mặt đất.",
       ke=[("Lúc ổn định, tần số vật bằng tần số lực", True),
           ("Cột chỉ dao động ở tần số riêng $f_0$", "Tần số riêng chỉ là chỗ biên độ lớn nhất; lúc ổn định vật dao động theo tần số lực."),
           ("Trung bình cộng của $f_0$ và tần số lực", "Không có quy tắc lấy trung bình; tần số vật ổn định bằng đúng tần số lực.")]),
  buoc("Biên độ ở $4{,}0$ Hz so với $5{,}0$ Hz", "Từ $5{,}0$ Hz xuống $4{,}0$ Hz, biên độ của cột thay đổi thế nào?",
       loi="Cho rằng tần số giảm thì biên độ giảm; biên độ không đơn điệu theo $f$, nó phụ thuộc $|f-f_0|$.",
       lua_chon=[("Tăng, vì $|f-f_0|$ nhỏ đi", True),
                 ("Giảm, vì tần số lực nhỏ đi", "Biên độ không tăng giảm theo $f$; nó lớn khi $f$ gần $f_0$, nên phải xét $|f-f_0|$."),
                 ("Không đổi, vì lực không đổi", "Lực không đổi nhưng biên độ vẫn đổi khi $|f-f_0|$ đổi.")],
       ke=[("So $|f-f_0|$ ở hai tần số", True),
           ("So thẳng hai tần số: lớn hơn thì biên độ lớn hơn", "Biên độ lớn nhất ở $f_0$, hai bên đều giảm; so thẳng tần số bỏ qua điều đó."),
           ("So biên độ với tần số riêng của bàn rung", "Bàn rung không có tần số riêng cần xét; điều kiện là độ lệch khỏi $f_0$ của cột.")]),
  buoc("Chênh lệch so với sai số", "Hiệu hai biên độ (lớn trừ nhỏ) bằng bao nhiêu cm?", 2.1, "cm", 0.05,
       loi="Lấy hiệu hai tần số thay cho hiệu hai biên độ, hoặc cho rằng hiệu nhỏ hơn sai số.",
       ke=[("Lấy hiệu hai biên độ trong bảng rồi so với sai số đọc", True),
           ("Lấy hiệu hai tần số rồi so với sai số đọc", "Sai số đọc là của biên độ (cm), phải so với hiệu hai biên độ."),
           ("Bỏ qua sai số vì số đọc đã làm tròn", "Hai số đọc chỉ khác nhau thật khi hiệu vượt sai số; phải so.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang="Đề cho <b>biên độ giảm theo $e^{-\\beta t}$</b> và hỏi <b>cơ năng</b> → biên độ theo hàm mũ; cơ năng theo bình phương biên độ.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Biên độ sau $5{,}0$ s", "Biên độ sau $5{,}0$ s bằng bao nhiêu cm?", 1.8, "cm", 0.05,
       loi="Quên rằng $\\beta t$ không có đơn vị và nhân $\\beta$ với $A_0$; hoặc lấy $e^{\\beta t}$ (lớn lên) thay cho $e^{-\\beta t}$ (nhỏ đi)."),
  buoc("Lúc còn một nửa biên độ", "Sau bao nhiêu giây thì biên độ còn một nửa $A_0$?", 3.5, "s", 0.1,
       loi="Cho rằng biên độ giảm đều theo thời gian nên lấy $t=\\dfrac{A_0}{2\\beta}$; đây là hàm mũ, phải dùng logarit.",
       ke=[("Giải $e^{-\\beta t}=\\dfrac12$ bằng logarit", True),
           ("Lấy $t=\\dfrac{A_0}{2\\beta}$", "Biên độ giảm theo hàm mũ chứ không giảm đều theo thời gian, nên công thức này không đúng."),
           ("Lấy $t$ bằng nửa thời gian ở câu a", "Biên độ không giảm tuyến tính theo thời gian nên một nửa thời gian không cho một nửa biên độ.")]),
  buoc("Cơ năng còn lại", "Cơ năng còn bao nhiêu phần trăm cơ năng ban đầu?", 25, "%", 0.5,
       loi="Cho rằng cơ năng tỉ lệ với biên độ nên còn một nửa; cơ năng tỉ lệ với bình phương biên độ.",
       ke=[("Cơ năng tỉ lệ $A^2$: lấy bình phương tỉ số biên độ", True),
           ("Cơ năng tỉ lệ $A$: cũng giảm một nửa", "Cơ năng $W=\\dfrac12kA^2$ tỉ lệ bình phương biên độ, không tỉ lệ bậc nhất."),
           ("Cơ năng tỉ lệ $e^{-\\beta t}$ như biên độ", "Cơ năng tỉ lệ $A^2$ nên theo $e^{-2\\beta t}$, hệ số mũ gấp đôi.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang="Đề cho <b>gờ cách đều và chu kì riêng của xe</b> → $T=\\dfrac{L}{v}$, cộng hưởng khi $T=T_0$; so vận tốc bằng độ lệch tần số.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi đơn vị", "Xe chạy $36$ km/h, tốc độ này bằng bao nhiêu m/s?", 10, "m/s", 0.1,
       loi="Nhân với $3{,}6$ thay vì chia, hoặc quên đổi và dùng $36$ cùng $L=6{,}0$ m."),
  buoc("Chu kì ngoại lực", "Chu kì của ngoại lực bằng bao nhiêu giây?", 0.6, "s", 0.01,
       loi="Lấy $T=T_0$ (chu kì riêng của xe) thay cho chu kì của lực, hoặc nhân $L\\cdot v$.",
       ke=[("Chu kì là thời gian xe đi giữa hai gờ liên tiếp: $T=\\dfrac{L}{v}$", True),
           ("Lấy $T=T_0$ vì xe có chu kì riêng", "$T_0$ là của xe; chu kì của ngoại lực phụ thuộc vận tốc và khoảng cách gờ."),
           ("Lấy $T=L\\cdot v$", "Tích $L\\cdot v$ có đơn vị m²/s, không phải giây.")]),
  buoc("Vận tốc gây cộng hưởng", "Xe chạy bao nhiêu km/h thì thân xe rung mạnh nhất?", 27, "km/h", 0.5,
       loi="Dùng lại $T$ ở bước trước (ứng với $36$ km/h); cộng hưởng cần $T=T_0$. Hoặc quên đổi m/s sang km/h ở bước cuối.",
       ke=[("Đặt $T=T_0$ rồi $v=\\dfrac{L}{T_0}$, đổi sang km/h", True),
           ("Dùng $v=\\dfrac{L}{T}$ với $T$ vừa tìm ở bước trước", "$T$ đó ứng với $36$ km/h, chưa phải cộng hưởng; cộng hưởng cần $T$ bằng $T_0$."),
           ("Dùng $v=\\dfrac{T_0}{L}$", "Thương $\\dfrac{T_0}{L}$ có đơn vị s/m, không phải vận tốc.")]),
  buoc("So $36$ km/h và $54$ km/h", "Ở vận tốc nào thân xe rung mạnh hơn?",
       loi="Cho rằng xe chạy nhanh hơn thì rung mạnh hơn; biên độ lớn khi tần số lực gần $f_0$, không phải khi xe nhanh.",
       lua_chon=[("$36$ km/h, vì tần số lực gần $f_0$ hơn", True),
                 ("$54$ km/h, vì xe nhanh thì gờ đến dồn dập nên rung mạnh hơn", "Biên độ không tăng theo vận tốc; ở $54$ km/h tần số lực là $2{,}5$ Hz, lệch xa $f_0=1{,}25$ Hz."),
                 ("Như nhau, vì lực và lực cản như nhau", "Lực và cản như nhau nhưng $|f-f_0|$ khác nhau, nên biên độ khác nhau.")],
       ke=[("Tính tần số lực ở hai vận tốc rồi so $|f-f_0|$", True),
           ("So thẳng hai vận tốc: lớn hơn thì rung mạnh hơn", "Biên độ lớn nhất ở cộng hưởng, giảm cả khi vận tốc quá lớn."),
           ("Chỉ so hai chu kì ngoại lực rồi chọn chu kì nhỏ hơn", "Tiêu chí là độ lệch khỏi cộng hưởng ($|T-T_0|$ hay $|f-f_0|$), không phải chu kì lớn hay nhỏ.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang="Đề có <b>khởi động (tần số quét từ 0)</b> và tần số chạy ổn định → kiểm hai chỗ: $f=f_{ổn}$ và $f=f_0$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Hai tần số cần kiểm", "Hai biên độ cần kiểm tra ứng với những tần số lực nào?",
       loi="Chỉ kiểm lúc chạy ổn định mà quên lúc khởi động tần số lực quét qua $f_0$.",
       lua_chon=[("Tần số chạy ổn định, và $f=f_0$ lúc khởi động đi qua", True),
                 ("Chỉ tần số chạy ổn định, vì khởi động máy chưa chạy hết công suất", "Tần số lực quét qua mọi giá trị từ $0$ lên tần số chạy ổn định nên chắc chắn đi qua $f_0$."),
                 ("$f_0$ và $2f_0$", "Máy chạy ở tần số cho trước; $2f_0$ không có ý nghĩa trong bài.")]),
  buoc("Đệm X lúc chạy ổn định", "Đệm X có biên độ bao nhiêu cm lúc máy chạy ổn định?", 0.2, "cm", 0.01,
       loi="Lấy $A=A_r$ vì \"máy đang chạy\"; $A_r$ chỉ là biên độ khi $f=f_0$, còn máy chạy ở tần số khác.",
       ke=[("Thế tần số chạy ổn định vào $A(f)$", True),
           ("Lấy $A=A_r$ của đệm X", "$A_r$ chỉ ứng với $f=f_0$; máy chạy ở tần số lệch xa $f_0$."),
           ("Lấy $A=b$ vì $b$ cũng đo bằng đơn vị tần số", "$b$ là độ rộng đỉnh theo tần số (Hz), không phải biên độ.")]),
  buoc("Đệm Y lúc chạy ổn định", "Đệm Y có biên độ bao nhiêu cm lúc máy chạy ổn định?", 0.2, "cm", 0.01,
       loi="Cho rằng cản lớn thì biên độ luôn nhỏ hơn nhiều; xa $f_0$ thì lực cản gần như không ảnh hưởng, hãy tính số.",
       ke=[("Thế số như đệm X", True),
           ("Đệm Y có cản lớn nên biên độ nhỏ hơn hẳn đệm X", "Xa $f_0$, mẫu số gần bằng $|f-f_0|$ nên cản hầu như không đổi kết quả; hai đệm gần bằng nhau, phải tính."),
           ("Lấy $A=A_r$ của đệm Y vì $A_r$ nhỏ hơn", "$A_r$ chỉ ứng với $f=f_0$.")]),
  buoc("Lúc khởi động qua $f_0$", "Lúc khởi động đi qua $f_0$, đệm nào vượt giới hạn $3{,}0$ cm?",
       loi="Dùng lại biên độ lúc chạy ổn định cho cả khởi động; tại $f=f_0$ biên độ là $A_r$.",
       lua_chon=[("Chỉ đệm X, vì tại $f=f_0$ thì $A=A_r$ lớn hơn giới hạn", True),
                 ("Cả hai, vì biên độ ổn định của hai đệm bằng nhau", "Biên độ lúc khởi động tính tại $f=f_0$, không phải tại tần số chạy ổn định."),
                 ("Chỉ đệm Y, vì cản lớn thì rung lớn", "Cản lớn làm đỉnh cộng hưởng thấp đi, không cao lên.")],
       ke=[("Thế $f=f_0$ vào $A(f)$ cho từng đệm", True),
           ("Dùng biên độ lúc chạy ổn định của từng đệm", "Đó là biên độ ở tần số khác; lúc khởi động phải xét tại $f=f_0$."),
           ("Chỉ so $b$ của hai đệm", "$b$ chỉ cho biết độ rộng đỉnh; phải so biên độ $A(f_0)=A_r$ với giới hạn.")]),
  buoc("Chọn đệm", "Nên chọn đệm nào?",
       loi="Chỉ nhìn lúc chạy ổn định (hai đệm bằng nhau) rồi chọn đệm có $A_r$ lớn; còn điều kiện lúc khởi động.",
       lua_chon=[("Đệm Y: ổn định như đệm X, khởi động đạt yêu cầu", True),
                 ("Đệm X, vì cản nhỏ ít tốn năng lượng", "Đệm X vượt giới hạn lúc khởi động nên không đạt yêu cầu."),
                 ("Cả hai đều đạt vì biên độ ổn định bằng nhau", "Còn yêu cầu lúc đi qua cộng hưởng; đệm X không đạt.")],
       ke=[("Đối chiếu từng đệm với cả hai yêu cầu", True),
           ("Chọn đệm có $A_r$ lớn hơn", "$A_r$ lớn nghĩa là đỉnh cộng hưởng cao, tức rung mạnh hơn lúc khởi động."),
           ("Chọn đệm theo biên độ lúc chạy ổn định thôi", "Hai đệm bằng nhau ở đó; phải xét thêm yêu cầu lúc khởi động.")]),
  buoc("Kiểm tra")]),
]

d = {"lesson_id": 25, "lesson_title": "Bài 6. Dao động tắt dần. Dao động cưỡng bức. Hiện tượng cộng hưởng", "generated_at": "2026-10-09",
     "review": {"checked": True, "notes": "Kiểm chéo 9/10/2026: tự giải 5 dạng bằng Python, mọi đáp số và dap_so từng bước khớp; đã sửa 4 lựa chọn/lời nhắc (D1 bước 3, D3 gọi lại ln2, D4 lựa chọn T lớn hơn trùng đáp án, D5 lựa chọn đệm Y nhỏ hơn thật sự đúng)."},
     "dang_bai": [dict(solution_html="", **x) for x in DANG]}      # bài chưa có dạng cũ trong DB → không có tu_luan
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
