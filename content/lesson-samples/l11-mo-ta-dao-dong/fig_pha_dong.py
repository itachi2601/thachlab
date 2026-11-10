"""Hình 5 (động, SMIL): M chạy đều trên vòng tròn, P là hình chiếu; dừng ở pha 0, π/3, π/2, π, −π/2, −π/3.
Bấm nút "▶ Chạy" mới chạy MỘT vòng rồi dừng ở pha 0 (V10). Chạy độc lập: python3 fig_pha_dong.py"""
import math
import importlib.util as _iu
import pathlib as _pl
from svg_lib import RED, BLUE, ORG, GRN, text, wrap
_sp = _iu.spec_from_file_location("svg_lib_skill", _pl.Path(__file__).resolve().parents[3]
                                  / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py")
_sk = _iu.module_from_spec(_sp); _sp.loader.exec_module(_sk)
chevron = _sk.chevron

FS, FS2 = 15, 14
cx, cy, R = 220, 105, 68
OMEGA_A = 46.0            # ω·A quy ra đơn vị viewBox: mũi tên dài nhất
ID = "l11pd"

# (góc độ theo chiều quay, nhãn pha, dòng 1, dòng 2)
STOPS = [
    (0,   "0",    "x = +A (biên dương)", "v = 0"),
    (60,  "π/3",  "x = A/2", "đi theo chiều âm"),
    (90,  "π/2",  "x = 0 (VTCB)", "đi theo chiều âm, tốc độ cực đại"),
    (180, "π",    "x = −A (biên âm)", "v = 0"),
    (270, "−π/2 (≡ 3π/2)", "x = 0 (VTCB)", "đi theo chiều dương, tốc độ cực đại"),
    (300, "−π/3 (≡ 5π/3)", "x = A/2", "đi theo chiều dương"),
]

def pos(deg):
    a = math.radians(deg)
    return cx + R * math.cos(a), cy - R * math.sin(a)

def f(v): return f"{v:.1f}"

# ---- kiểm vật lí: x = A cos φ, v = −ωA sin φ (A = 1, ω = 1)
for deg, lab, l1, l2 in STOPS:
    a = math.radians(deg)
    x, v = math.cos(a), -math.sin(a)
    Mx, My = pos(deg)
    assert abs((Mx - cx) / R - x) < 1e-9                       # P = hình chiếu: OP = A cos φ
    assert (My < cy - 1e-6) == (v < -1e-6)                     # M nửa trên <=> v < 0
    assert (My > cy + 1e-6) == (v > 1e-6)                      # M nửa dưới <=> v > 0
    if abs(x - 0.5) < 1e-9: assert "A/2" in l1
    if abs(x) < 1e-9: assert "VTCB" in l1 and "tốc độ cực đại" in l2 and abs(abs(v) - 1) < 1e-9
    if abs(abs(x) - 1) < 1e-9: assert "v = 0" in l2 and abs(v) < 1e-9
    if x == 1 or abs(x - 1) < 1e-9: assert "+A" in l1
    if abs(x + 1) < 1e-9: assert "−A" in l1
    if v < -1e-9: assert "chiều âm" in l2
    if v > 1e-9: assert "chiều dương" in l2

def vel_arrow(deg):
    """Mũi tên v của P, vẽ dưới trục (y = cy+38): dx = −ωA sin φ (dương = sang phải)."""
    Px, _ = pos(deg)
    dx = -OMEGA_A * math.sin(math.radians(deg))
    if abs(dx) < 1e-6: return "", 0.0
    y = cy + 46
    x2 = Px + dx
    s = (f'<line x1="{f(Px)}" y1="{y}" x2="{f(x2)}" y2="{y}" stroke="{ORG}" stroke-width="3"/>'
         + chevron(x2, y, dx, 0, ORG, 3, 11)
         + text(f(x2 + (13 if dx > 0 else -13)), y + 5, "v", ORG, FS, "middle", "700"))
    return s, dx

ARR = [vel_arrow(d[0]) for d in STOPS]
for (deg, *_), (s, dx) in zip(STOPS, ARR):
    v = -math.sin(math.radians(deg))
    assert (dx < 0) == (v < -1e-6) and (dx > 0) == (v > 1e-6)  # chiều mũi tên = dấu v
    assert abs(abs(dx) - OMEGA_A * abs(math.sin(math.radians(deg)))) < 1e-9
    if abs(v) < 1e-6: assert s == ""                           # ở biên: không mũi tên

# ---- dòng thời gian
HOLD, HOLD0, TAIL = 1.4, 1.0, 0.3
SEG = [0.6, 0.3, 0.9, 0.9, 0.3, 0.6]             # thời gian đi tới điểm dừng kế: quay ĐỀU 100°/s
angs = [s[0] for s in STOPS] + [360]
for i in range(6): assert abs((angs[i+1] - angs[i]) / SEG[i] - 100) < 1e-9
keys = [(0.0, 0)]
holds = []                                       # (t_bắt_đầu, t_kết_thúc) của từng điểm dừng
t = 0.0
for i in range(6):
    h = HOLD0 if i == 0 else HOLD
    holds.append((t, t + h)); t += h; keys.append((t, angs[i]))
    n = max(2, round((angs[i+1] - angs[i]) / 15))
    for k in range(1, n + 1):
        keys.append((t + SEG[i] * k / n, angs[i] + (angs[i+1] - angs[i]) * k / n))
    t += SEG[i]
T_ARR = t                                        # tới lại pha 0 (360°)
D = T_ARR + TAIL + 0.02
# điểm "nhảy" arc từ 360 về 0 sau khi tới nơi
def kt(ts): return ";".join(f"{x / D:.4f}" for x in ts)
tk = [k[0] for k in keys] + [T_ARR + 0.02, D]
ak = [k[1] for k in keys] + [360, 360]           # góc M: 360° ≡ 0°

def anim(attr, vals, times=None, discrete=False):
    times = times or tk
    cm = ' calcMode="discrete"' if discrete else ""
    return (f'<animate attributeName="{attr}" values="{";".join(vals)}" keyTimes="{kt(times)}"{cm} '
            f'dur="{D:.2f}s" begin="indefinite" fill="freeze"/>')

MX = [pos(a)[0] for a in ak]; MY = [pos(a)[1] for a in ak]
RA = 28
assert abs(tk[-3] - T_ARR) < 1e-9                       # tk[:-2] đã kết thúc đúng ở T_ARR
arc_times = tk[:-2] + [T_ARR + 0.02, D]                 # khoá cuối phải đúng 1, không trùng khoá
arc_vals = [f"{k[1]:.0f} 360" for k in keys] + ["0 360", "0 360"]
assert len(arc_times) == len(arc_vals) and len(set(arc_times)) == len(arc_times)
ev = []                                          # khoá thưa cho phép quay đều từng đoạn
for i in range(6): ev += [(holds[i][0], angs[i]), (holds[i][1], angs[i])]
ev.append((T_ARR, 360))
rot_t = [e[0] for e in ev] + [D]; rot_a = [e[1] for e in ev] + [360]

b = ""
# nửa trên / nửa dưới (gợi nhớ)
b += (f'<path d="M{cx-R},{cy} A{R},{R} 0 0 1 {cx+R},{cy} Z" fill="{RED}" opacity="0.13"/>'
      f'<path d="M{cx-R},{cy} A{R},{R} 0 0 0 {cx+R},{cy} Z" fill="{BLUE}" opacity="0.13"/>')
b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="currentColor" stroke-width="1.8"/>'
x2 = cx + R + 34
b += (f'<line x1="{cx-R-24}" y1="{cy}" x2="{x2}" y2="{cy}" stroke="currentColor" stroke-width="1.6"/>'
      + chevron(x2, cy, 1, 0, "currentColor", 1.6, 10)
      + text(x2 + 4, cy + 5, "x", "currentColor", FS, "start", "700"))
b += text(cx - R - 4, cy + 30, "−A", "currentColor", FS, "end", "700")
b += text(cx + R + 4, cy + 30, "+A", "currentColor", FS, "start", "700")
b += text(cx - 6, cy + 18, "O", "currentColor", FS, "end", "700")
RP = R + 12
g0, g1 = math.radians(125), math.radians(160)
pa = [(cx + RP * math.cos(g0 + (g1 - g0) * i / 20), cy - RP * math.sin(g0 + (g1 - g0) * i / 20)) for i in range(21)]
b += (f'<polyline fill="none" stroke="{GRN}" stroke-width="2.2" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pa) + '"/>'
      + chevron(pa[-1][0], pa[-1][1], -math.sin(g1), -math.cos(g1), GRN, 2.2, 10)
      + text(14, 62, "chiều tăng pha", GRN, FS2, "start", "700"))
b += (f'<path d="M{cx+RA},{cy} A{RA},{RA} 0 1 0 {cx-RA},{cy} A{RA},{RA} 0 1 0 {cx+RA},{cy}" pathLength="360" fill="none" '
      f'stroke="{GRN}" stroke-width="2.4" stroke-dasharray="0 360">'
      f'<animate attributeName="stroke-dasharray" values="{";".join(arc_vals)}" keyTimes="{kt(arc_times)}" dur="{D:.2f}s" '
      f'begin="indefinite" fill="freeze"/></path>')
# bán kính OM + M: nhóm quay đều quanh O (SVG quay dương = thuận chiều kim, nên dùng góc âm)
rv = ";".join(f"{-a:.0f} {cx} {cy}" for a in rot_a)
b += (f'<g><animateTransform attributeName="transform" type="rotate" values="{rv}" keyTimes="{kt(rot_t)}" '
      f'dur="{D:.2f}s" begin="indefinite" fill="freeze"/>'
      f'<line x1="{cx}" y1="{cy}" x2="{cx+R}" y2="{cy}" stroke="{RED}" stroke-width="2.4"/>'
      f'<circle cx="{cx+R}" cy="{cy}" r="5.5" fill="{RED}"/></g>')
b += f'<circle cx="{cx}" cy="{cy}" r="3" fill="currentColor"/>'
# P + đường gióng + nhãn P: nhóm tịnh tiến theo x (x = A cos φ), đường gióng đổi y1
tv = ";".join(f"{v - MX[0]:.1f} 0" for v in MX)
b += (f'<g><animateTransform attributeName="transform" type="translate" values="{tv}" keyTimes="{kt(tk)}" '
      f'dur="{D:.2f}s" begin="indefinite" fill="freeze"/>'
      f'<line x1="{f(MX[0])}" y1="{f(MY[0])}" x2="{f(MX[0])}" y2="{cy}" stroke="{ORG}" stroke-width="1.5" stroke-dasharray="4 3">'
      + anim("y1", [f(v) for v in MY]) + '</line>'
      f'<circle cx="{f(MX[0])}" cy="{cy}" r="4.5" fill="{ORG}"/>'
      + text(f(MX[0] + 8), cy + 18, "P", ORG, FS, "start", "700") + '</g>')
LX = [pos(a)[0] + 19 * math.cos(math.radians(a)) for a in ak]
LY = [pos(a)[1] - 19 * math.sin(math.radians(a)) - 3 for a in ak]
b += (f'<text x="{f(LX[0])}" y="{f(LY[0])}" fill="{RED}" font-size="{FS}" font-weight="700" text-anchor="middle">M'
      + anim("x", [f(v) for v in LX]) + anim("y", [f(v) for v in LY]) + '</text>')

# bảng chú thích + mũi tên v theo từng điểm dừng (hiện khi M dừng)
for i, ((deg, lab, l1, l2), (arr, _)) in enumerate(zip(STOPS, ARR)):
    g = text(14, 26, f"pha = {lab}", GRN, 17, "start", "700")
    g += text(cx, 212, l1, "currentColor", FS, "middle", "700")
    g += text(cx, 234, l2, "currentColor", FS, "middle", "700")
    g += arr
    # i=0: [0..holds0 end] bật, tắt, rồi bật lại ở T_ARR
    if i == 0:
        ts, vs = [0.0, holds[0][1], T_ARR + 0.02], ["1", "0", "1"]
    else:
        ts, vs = [0.0, holds[i][0], holds[i][1]], ["0", "1", "0"]
    b += (f'<g opacity="{vs[0]}"><animate attributeName="opacity" values="{";".join(vs)}" keyTimes="{kt(ts)}" '
          f'calcMode="discrete" dur="{D:.2f}s" begin="indefinite" fill="freeze"/>{g}</g>')

# gợi nhớ cố định, mỗi ý một dòng
b += f'<line x1="14" y1="248" x2="426" y2="248" stroke="currentColor" stroke-width="1" opacity="0.3"/>'
b += text(cx, 270, "M ở nửa trên → P đi theo chiều âm", "currentColor", FS2, "middle", "600")
b += text(cx, 292, "M ở nửa dưới → P đi theo chiều dương", "currentColor", FS2, "middle", "600")

def build():
    return wrap("0 0 440 302",
                "Hình động: điểm M quay ngược chiều kim đồng hồ trên vòng tròn, P là hình chiếu lên trục Ox; "
                "dừng ở các pha 0, pi trên 3, pi trên 2, pi, trừ pi trên 2, trừ pi trên 3, mỗi lần ghi li độ và chiều chuyển động của P",
                b, "Hình 3. M quay đều; P là hình chiếu dao động trên Ox. Bấm ▶ Chạy để xem sáu pha đặc biệt.").replace(
        "</svg><figcaption>", '</svg><button type="button" class="bt-run" data-bt-run="1">▶ Chạy</button><figcaption>', 1)

if __name__ == "__main__":
    s = build()
    print(len(s.encode()), "byte; D =", round(D, 2), "s")
    assert s.count("data-bt-run") == 1 and ".click" not in s   # nút HTML: ContentHtml gọi beginElement()
    for bad in ("<script", "<style", " on", "base64", "href"):
        assert bad not in s, bad
    assert len(s.encode()) <= 15000
    print("assert OK")
