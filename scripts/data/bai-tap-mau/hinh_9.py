"""Hình cho bài tập mẫu Bài 8 "Áp suất - động năng của phân tử khí" (Vật lí 12), lesson_id 9.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Phân tử chuyển động thẳng, phản xạ đàn hồi ở thành (lấy mẫu cách đều thời gian rồi nội suy tuyến tính); nhiệt kế dâng tuyến tính.
Không nhãn kết quả, không đồ thị vẽ sẵn: hình chỉ mang dữ kiện của đề."""
import math, os, random, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


# ───────────── tiện ích ─────────────
def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def rich(s, size=13):
    """`p_N` → p với chỉ số dưới N (tspan hạ dòng rồi trả lại)."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def smil0(attr, vals, dur):
    return f'<animate attributeName="{attr}" values="{";".join(f"{v:.0f}" for v in vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'

def refl(u, lo, hi):
    """Toạ độ sau khi phản xạ đàn hồi ở hai thành lo, hi (đường đi gấp khúc)."""
    w = hi - lo; u = (u - lo) % (2 * w)
    return lo + (u if u <= w else 2 * w - u)

def mols(xa, ya, xb, yb, n, seed, dur, speed, samples=36, r=3.6, c=BLUE, acc=None, fade=None, op=".9"):
    """n phân tử chuyển động trong hộp [xa,xb]×[ya,yb]; phản xạ đàn hồi ở thành.
    acc(t) → hệ số nhân tốc độ tại thời điểm t (None = 1): quãng đường là tích phân của speed·acc.
    fade[i] = thời điểm (s) phân tử i biến mất (None = ở lại). Trả (chuỗi chạy, chuỗi tĩnh)."""
    rnd = random.Random(seed); out = ""; static = ""
    for i in range(n):
        x0 = rnd.uniform(xa + r, xb - r); y0 = rnd.uniform(ya + r, yb - r)
        th = rnd.uniform(0, 2 * math.pi); v = speed * rnd.uniform(0.6, 1.2)
        vx, vy = v * math.cos(th), v * math.sin(th)
        X = []; Y = []; s = 0.0
        for k in range(samples + 1):
            t = dur * k / samples
            if k:
                t0 = dur * (k - 1) / samples
                s += (acc((t + t0) / 2) if acc else 1.0) * dur / samples
            X.append(refl(x0 + vx * s, xa + r, xb - r)); Y.append(refl(y0 + vy * s, ya + r, yb - r))
        fd = ""
        if fade and fade[i] is not None:
            f = fade[i] / dur
            fd = (f'<animate attributeName="opacity" values="{op};{op};0;0" keyTimes="0;{f:.3f};{min(f + 0.06, 0.99):.3f};1" '
                  f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')
        out += f'<circle cx="{X[0]:.0f}" cy="{Y[0]:.0f}" r="{r}" fill="{c}" opacity="{op}">{smil0("cx", X, dur)}{smil0("cy", Y, dur)}{fd}</circle>'
        static += f'<circle cx="{x0:.0f}" cy="{y0:.0f}" r="{r}" fill="{c}" opacity="{op}"/>'
    return out, static

def thermo(x, ytop, h, t_low, t_high, t0, t1, anim, labs, dur=5):
    """Nhiệt kế: cột chất lỏng dâng tuyến tính từ t0 đến t1 (chia độ t_low..t_high); labs = các nhiệt độ ghi bên cạnh."""
    yb = ytop + h; l0 = h * (t0 - t_low) / (t_high - t_low); l1 = h * (t1 - t_low) / (t_high - t_low)
    out = R(x - 6, ytop, 12, h, sw=2, rx=6) + circ(x, yb + 10, 10, RED, 2, RED)
    if anim:
        out += (f'<rect x="{x - 3}" y="{yb - l0:.1f}" width="6" height="{l0:.1f}" fill="{RED}">'
                f'{smil("y", [yb - l0, yb - l1], dur)}{smil("height", [l0, l1], dur)}</rect>')
    else:
        out += f'<rect x="{x - 3}" y="{yb - l1:.1f}" width="6" height="{l1:.1f}" fill="{RED}"/>'
    for t in labs:
        lv = h * (t - t_low) / (t_high - t_low)
        out += seg(x + 6, yb - lv, x + 14, yb - lv, "currentColor", 1.4) + txt(x + 18, yb - lv + 4, f"{t} °C", "currentColor", 12)
    return out

def box(xa, ya, xb, yb, sw=2.6):
    return R(xa - 4, ya - 4, xb - xa + 8, yb - ya + 8, sw=sw, rx=14)


# ───────────── Dạng 1 · hydrogen + oxygen cùng bình, 47 °C ─────────────
def d1(kk):
    anim = kk == 0; xa, ya, xb, yb = 36, 46, 226, 146
    h_m, h_s = mols(xa + 6, ya + 6, xb - 6, yb - 6, 6, 5, 6, 80, 36, 3.2, BLUE)
    o_m, o_s = mols(xa + 6, ya + 6, xb - 6, yb - 6, 4, 11, 6, 20, 36, 5.4, ORG)
    b = box(xa, ya, xb, yb) + (h_m + o_m if anim else h_s + o_s)
    b += dot(46, 172, 3.2, BLUE) + txt(56, 177, "H₂", BLUE, 14) + dot(100, 172, 5.4, ORG) + txt(112, 177, "O₂", ORG, 14)
    b += thermo(330, 40, 100, 0, 100, 47, 47, False, [47])
    b += txt(268, 30, "Bình kín, hai khí trộn lẫn", "currentColor", 12, "start", "600")
    if kk == 0:
        return fig("d1-0", "0 0 420 190", "Hai loại phân tử hydrogen và oxygen chuyển động hỗn loạn trong một bình kín ở 47 độ C", b,
                   "Mô phỏng: chuyển động nhiệt hỗn loạn của hai loại phân tử trong 6 s, va chạm đàn hồi với thành bình. Hình chỉ minh hoạ chuyển động, chưa so sánh động năng. " + NOTE)
    b += txt(250, 186, "Ē_d của H₂ = ?", ORG, 13)
    return fig("d1-2", "0 0 420 190", "Dữ kiện: bình chứa hydrogen và oxygen ở cùng nhiệt độ 47 độ C", b,
               "Dữ kiện: hai khí trong cùng một bình nên cùng nhiệt độ. " + NOTE)


# ───────────── Dạng 2 · heli nung từ 27 °C lên 147 °C trong bình kín ─────────────
T2_LO, T2_HI = 27, 147
def d2(kk):
    anim = kk == 0; xa, ya, xb, yb = 36, 46, 226, 146; DUR = 6
    acc = lambda t: math.sqrt((300 + 120 * t / DUR) / 300)          # tốc độ ∝ √T, T tăng đều từ 300 K lên 420 K
    mv, st = mols(xa + 6, ya + 6, xb - 6, yb - 6, 8, 3, DUR, 55, 36, 3.6, BLUE, acc=acc)
    b = box(xa, ya, xb, yb) + (mv if anim else st)
    b += txt(131, 166, "khí heli, V không đổi", "currentColor", 12, "middle", "400")
    b += thermo(330, 40, 100, 0, 160, T2_LO, T2_HI, anim, [T2_LO, T2_HI], DUR)
    if anim:
        return fig("d2-0", "0 0 420 190", "Khí heli trong bình kín được hơ nóng từ 27 độ C lên 147 độ C, các phân tử chuyển động nhanh dần", b,
                   "Mô phỏng: hơ nóng đều trong 6 s; tốc độ phân tử vẽ tăng dần theo nhiệt độ. " + NOTE)
    b += txt(268, 30, "Hơ nóng; V, N không đổi", "currentColor", 12, "start", "600")
    return fig("d2-2", "0 0 420 190", "Dữ kiện: khí heli trong bình kín, nhiệt độ ban đầu 27 độ C và nhiệt độ cuối 147 độ C", b,
               "Dữ kiện: bình kín, thể tích và lượng khí không đổi. " + NOTE)


# ───────────── Dạng 3 · neon, ρ = 0,90 kg/m³, √(v²) = 600 m/s ─────────────
def d3(kk):
    anim = kk == 0; xa, ya, xb, yb = 36, 46, 226, 146
    mv, st = mols(xa + 6, ya + 6, xb - 6, yb - 6, 10, 21, 6, 70, 36, 3.6, BLUE)
    b = box(xa, ya, xb, yb) + (mv if anim else st)
    b += txt(131, 166, "khí neon trong bình kín", "currentColor", 12, "middle", "400")
    b += txt(250, 62, "ρ = 0,90 kg/m³", "currentColor", 13) + txt(250, 84, "√(v̄²) = 600 m/s", "currentColor", 13)
    b += txt(250, 124, "p = ?", ORG, 14)
    if anim:
        return fig("d3-0", "0 0 420 190", "Phân tử neon chuyển động hỗn loạn và va chạm với thành bình", b,
                   "Mô phỏng: chuyển động nhiệt của phân tử trong 6 s, va chạm đàn hồi với thành. " + NOTE)
    return fig("d3-2", "0 0 420 190", "Dữ kiện: khối lượng riêng và căn bậc hai của trung bình bình phương tốc độ của khí neon", b,
               "Dữ kiện: khối lượng riêng và tốc độ căn quân phương của khí. " + NOTE)


# ───────────── Dạng 4 · argon, M = 40 g/mol, 77 °C ─────────────
def d4(kk):
    anim = kk == 0; xa, ya, xb, yb = 36, 46, 226, 146
    mv, st = mols(xa + 6, ya + 6, xb - 6, yb - 6, 8, 8, 6, 62, 36, 5.0, GRN)
    b = box(xa, ya, xb, yb) + (mv if anim else st)
    b += txt(131, 166, "khí argon (Ar)", "currentColor", 12, "middle", "400")
    b += thermo(330, 40, 100, 0, 100, 77, 77, False, [77])
    b += txt(250, 30, "M = 40 g/mol", "currentColor", 12, "start", "600")
    if anim:
        return fig("d4-0", "0 0 420 190", "Phân tử argon chuyển động hỗn loạn trong bình kín ở 77 độ C", b,
                   "Mô phỏng: chuyển động nhiệt của phân tử argon trong 6 s. " + NOTE)
    return fig("d4-2", "0 0 420 190", "Dữ kiện: khí argon trong bình kín ở 77 độ C, khối lượng mol 40 gam trên mol", b,
               "Dữ kiện: một khí, một nhiệt độ; câu c đổi sang khí khác ở cùng nhiệt độ. " + NOTE)


# ───────────── Dạng 5 · heli μ = 2,4·10²⁵ m⁻³, p = 1,0·10⁵ Pa → hút bớt một nửa, nung lên 117 °C ─────────────
def d5(kk):
    anim = kk == 0; xa, ya, xb, yb = 36, 46, 226, 146; DUR = 6
    fade = [None, None, 2.0, None, 3.0, 4.0, None, 5.0, 3.5, None, 2.5, None]      # 6 trong 12 phân tử bị hút ra
    mv, st = mols(xa + 6, ya + 6, xb - 6, yb - 6, 12, 14, DUR, 60, 36, 3.6, BLUE, fade=fade)
    b = box(xa, ya, xb, yb) + (mv if anim else st)
    b += txt(131, 166, "khí heli, bình cố định", "currentColor", 12, "middle", "400")
    b += seg(226, 96, 262, 96, "currentColor", 3) + R(262, 88, 16, 16, sw=2, rx=3) + txt(270, 124, "van hút", "currentColor", 11, "middle", "400")
    b += txt(296, 52, "Đầu: μ = 2,4·10²⁵ m⁻³", "currentColor", 12, "start", "700") + txt(296, 72, "p = 1,0·10⁵ Pa", "currentColor", 12, "start", "700")
    b += txt(296, 150, "Sau: còn μ/2 ; 117 °C", ORG, 12, "start", "700") + txt(296, 170, "p' = ?", ORG, 13, "start", "700")
    if anim:
        return fig("d5-0", "0 0 420 190", "Một nửa số phân tử heli được hút ra khỏi bình qua van", b,
                   "Mô phỏng: 6 trong 12 phân tử vẽ được hút ra qua van; hình chỉ biểu diễn số phân tử giảm một nửa. " + NOTE)
    return fig("d5-2", "0 0 420 190", "Dữ kiện: mật độ phân tử và áp suất ban đầu của khí heli; sau đó số phân tử còn một nửa và nhiệt độ 117 độ C", b,
               "Dữ kiện: bình cố định nên thể tích không đổi; nét vẽ chỉ minh hoạ. " + NOTE)
