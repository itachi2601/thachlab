"""Bài 62 · Bài 17. Trọng lực và lực căng (Vật lí 10, chương 3) — dựng scripts/data/bai-tap-mau/62.json từ đầu (write()).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-62.py   (mẫu cấu trúc: build-hinh-57.py)
Quy ước theo lý thuyết bài 62: P = mg; g = 9,8 m/s² khi bàn về nơi đặt vật (Trái Đất, Sao Hoả), g = 10 m/s² ở bài hệ vật/vật treo;
dây nhẹ, không dãn, ròng rọc nhẹ nhẵn: cùng độ lớn gia tốc, cùng lực căng; mỗi vật viết F = ma riêng, chiều dương theo chiều chuyển động."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "62.json")
OLD = json.load(open(os.path.join(HERE, "old/62.json")))["questions"]
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
T125 = "Trọng lực, trọng lượng và trọng tâm"
T126 = "Lực căng dây — hệ vật nối dây, ròng rọc"

# ═════════════ KIỂM SỐ LIỆU (tự giải lại độc lập, in ra) ═════════════
def CHECK():
    def ok(name, got, want, tol=1e-9):
        bad = abs(got - want) > tol * max(1, abs(want))
        print(f"  {name}: {got:g}" + (f"  <-- LỆCH, cần {want}" if bad else ""))
        if bad: sys.exit(f"CHECK hỏng: {name}")
    # Dạng 1
    ok("D1 P_TĐ", 90 * 9.8, 882); ok("D1 P_SH", 90 * 3.7, 333); ok("D1 tỉ số", 333 / 882, 3.7 / 9.8)
    # Dạng 2 (g = 10, m = 800)
    m, g = 800, 10
    ok("D2 a) T", m * g, 8000); ok("D2 b) T", m * (g + 1.5), 9200); ok("D2 c) T", m * (g - 1.2), 7040)
    assert 9200 > 9000 > 8000 > 7040, "chỉ khởi động vượt 9000"
    assert abs(m * g * 0.004 - 32) < 1e-9          # độ dài mũi tên P (px) khi k = 0,004 px/N
    # Dạng 3 (A = 1,5 kg trên bàn nhẵn, B = 1,0 kg treo)
    mA, mB = 1.5, 1.0
    a = mB * g / (mA + mB); T = mA * a
    ok("D3 a", a, 4); ok("D3 T", T, 6); ok("D3 kiểm B", mB * g - T, mB * a)
    # lựa chọn sai của bước 2/3 cho kết quả khác đáp án đúng
    assert abs(mB * g / mB - a) > 1e-6 and abs(g - a) > 1e-6        # a = P_B/m_B ; a = g
    assert abs(mB * g - T) > 1e-6 and abs(mB * a - T) > 1e-6        # T = P_B ; T = m_B a
    # Dạng 4 (5,0 kg và 3,0 kg)
    m1, m2 = 5.0, 3.0
    a4 = (m1 - m2) * g / (m1 + m2); T4 = m2 * (g + a4)
    ok("D4 a", a4, 2.5); ok("D4 T", T4, 37.5); ok("D4 T qua m1", m1 * (g - a4), 37.5)
    assert 30 < T4 < 50
    assert abs((m1 - m2) * g / m1 - a4) > 1e-6 and abs((m1 * g + m2 * g) / 2 - T4) > 1e-6 and abs(m1 * g - T4) > 1e-6
    # Dạng 5 (A = 2,0 kg, dây tối đa 12 N)
    mA5, Tmax = 2.0, 12.0
    amax = Tmax / mA5; mBmax = Tmax / (g - amax)
    ok("D5 a_max", amax, 6); ok("D5 m_B max", mBmax, 3); ok("D5 thế ngược a", mBmax * g / (mA5 + mBmax), 6)
    ok("D5 thế ngược T", mA5 * (mBmax * g / (mA5 + mBmax)), 12)
    assert abs(Tmax / g - mBmax) > 1e-6 and abs(Tmax / amax - mBmax) > 1e-6     # hai cách sai khác 3
    # mô phỏng: quãng đường khi chạy
    ok("D2 tổng quãng đường", 0.75 * 4 + 6 + (3 * 2.5 - 0.6 * 2.5 ** 2), 12.75)
CHECK()

# ═════════════ HÌNH ═════════════
C_P = "g"     # trọng lực: xanh lá (đúng bảng màu svg_lib), N: xanh dương
def ct(x, y, s, c="currentColor", size=13, anchor="start", weight="600"):
    return lbl(x, y, s, c, size, anchor, weight)

def anim_tr(vals, dur):
    """animateTransform translate chạy MỘT lần khi bấm; vals = [(dx, dy)…]."""
    v = ";".join(f"{x:.1f} {y:.1f}" for x, y in vals)
    return f'<animateTransform attributeName="transform" type="translate" values="{v}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'

def group(inner, vals=None, dur=0):
    if vals is None:
        return f"<g>{inner}</g>"
    return f"<g>{anim_tr(vals, dur)}{inner}</g>"

# ───────────── Dạng 1: lực kế ở hai nơi ─────────────
def f_damp(t, w=2 * math.pi * 0.9, gm=2.2):
    """Lò xo có cản, thả nhẹ từ độ dãn 0: độ dãn(t)/độ dãn cuối."""
    return 1 - math.exp(-gm * t) * (math.cos(w * t) + gm / w * math.sin(w * t))

SPR = " ".join(f"{x},{y:.4f}" for x, y in [(0, 0)] + [((1 if i % 2 == 0 else -1), (i + 0.5) / 7) for i in range(7)] + [(0, 1)])

def lucke(cx, name, gtxt, P, k, sao_hoa=False):
    C1, L0, Y0 = 0.12, 34, 36                 # độ dãn thêm vẽ = 0,12 px cho mỗi N
    ext = C1 * P
    n, T = 36, 3.0
    fs = [f_damp(T * i / n) for i in range(n)] + [1.0]
    b = seg(cx - 36, Y0, cx + 36, Y0, "currentColor", 3) + ct(cx, 18, f"{name}: g = {gtxt} m/s²", "currentColor", 13, "middle", "700")
    if k == 0:
        Ls = [L0 + ext * f for f in fs]
        sc = ";".join(f"8 {L:.2f}" for L in Ls)
        b += (f'<g transform="translate({cx},{Y0})"><polyline points="{SPR}" fill="none" stroke="currentColor" stroke-width="2" '
              f'vector-effect="non-scaling-stroke" transform="scale(8 {L0})"><animateTransform attributeName="transform" type="scale" '
              f'values="{sc}" dur="{T:.2f}s" begin="indefinite" fill="freeze"/></polyline></g>')
    else:
        b += (f'<g transform="translate({cx},{Y0})"><polyline points="{SPR}" fill="none" stroke="currentColor" stroke-width="2" '
              f'vector-effect="non-scaling-stroke" transform="scale(8 {L0 + ext:.2f})"/></g>')
    top = Y0 + L0
    inner = seg(cx, top, cx, top + 8, "currentColor", 2)
    inner += f'<rect x="{cx - 28}" y="{top + 8}" width="56" height="24" rx="4" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    inner += dot(cx - 16, top + 32, 5, "none").replace('fill="none"', 'fill="none" stroke="currentColor" stroke-width="2"')
    inner += dot(cx + 16, top + 32, 5, "none").replace('fill="none"', 'fill="none" stroke="currentColor" stroke-width="2"')
    inner += ct(cx, top + 25, "90 kg", "currentColor", 13, "middle", "700")
    if sao_hoa:
        inner += ct(cx + 34, top + 20, "P′ = ?", ORG, 13, "start", "700") + ct(cx + 34, top + 40, "m′ = ?", ORG, 13, "start", "700")
    else:
        inner += ct(cx + 34, top + 25, "P = ?", ORG, 13, "start", "700")
    if k == 0:
        vals = [(0, ext * f) for f in fs]
        b += group(inner, vals, T)
    else:
        b += f'<g transform="translate(0 {ext:.2f})">{inner}</g>'
    return b

def d1(k):
    b = lucke(105, "Trái Đất", "9,8", 882, k) + lucke(315, "Sao Hoả", "3,7", 333, k, True)
    if k == 0:
        return fig("d1-0", "0 0 420 232", "Cùng một xe 90 kg treo vào lực kế: ở Trái Đất lò xo dãn nhiều, ở Sao Hoả dãn ít hơn",
                   b, "Mô phỏng: cùng một xe được treo vào lực kế ở hai nơi, lò xo dãn dần rồi đứng yên. Độ dãn vẽ tỉ lệ với số chỉ; lực kế không có thang chia.")
    return fig("d1-2", "0 0 420 232", "Xe 90 kg ở hai nơi có gia tốc rơi tự do khác nhau, cần tìm trọng lượng ở mỗi nơi và khối lượng ở Sao Hoả", b,
               "Dữ kiện: khối lượng xe, gia tốc rơi tự do của từng nơi; dấu ? là các đại lượng cần tìm. " + NOTE)

# ───────────── Dạng 2: tời nâng thùng 800 kg, ba giai đoạn ─────────────
def pos2(t):
    if t <= 2: return 0.75 * t * t                 # a = 1,5 m/s² trong 2 s
    if t <= 4: return 3 + 3 * (t - 2)               # v = 3 m/s đều trong 2 s
    return 9 + 3 * (t - 4) - 0.6 * (t - 4) ** 2     # chậm dần a = 1,2 m/s² trong 2,5 s (dừng ở 12,75 m)

def d2(k):
    cx = 150
    if k == 0:
        S = 12                                       # px mỗi mét (chỉ để vẽ)
        ts = [0.25 * i for i in range(27)]           # 0 … 6,5 s
        dy = [-S * pos2(t) for t in ts]
        dur = 6.5
        top0, h, w, base = 218, 34, 60, 252
        b = seg(100, base, 200, base, "currentColor", 2.4) + seg(120, 18, 180, 18, "currentColor", 4) + ct(188, 22, "tời", "currentColor", 12, "start", "400")
        b += (f'<line x1="{cx}" y1="18" x2="{cx}" y2="{top0}" stroke="currentColor" stroke-width="2">'
              + smil("y2", [top0 + d for d in dy], dur) + '</line>')
        crate = f'<rect x="{cx - w // 2}" y="{top0}" width="{w}" height="{h}" rx="3" fill="none" stroke="currentColor" stroke-width="2.2"/>'
        crate += ct(cx, top0 + 14, "800 kg", "currentColor", 13, "middle", "700")
        svg, _ = vec_luc(C_P, cx, top0 + 22, 0, 1, 8000, 0.004, 3)
        crate += svg + ct(cx + 9, top0 + 52, "P", GRN, 13, "start", "700")
        b += group(crate, [(0, d) for d in dy], dur)
        # thang các giai đoạn: vị trí đáy thùng lúc đầu mỗi giai đoạn
        yb = [base - S * h_ for h_ in (0, 3, 9, 12.75)]
        b += seg(206, yb[0], 206, yb[3], "currentColor", 1.2, "4 4", .7)
        for y in yb: b += seg(200, y, 212, y, "currentColor", 1.6)
        b += ct(216, (yb[0] + yb[1]) / 2 + 4, "① nhanh dần, a = 1,5 m/s²", ORG, 12, "start", "700")
        b += ct(216, (yb[1] + yb[2]) / 2 + 4, "② thẳng đều", BLUE, 12, "start", "700")
        b += ct(216, (yb[2] + yb[3]) / 2 + 4, "③ chậm dần, a = 1,2 m/s²", ORG, 12, "start", "700")
        return fig("d2-0", "0 0 420 280", "Thùng 800 kg treo dưới cáp thẳng đứng đi lên qua ba giai đoạn: nhanh dần, thẳng đều, chậm dần", b,
                   "Mô phỏng ba giai đoạn, chạy đúng thời gian thật (6,5 s); thời gian mỗi giai đoạn chọn để minh hoạ. Mũi tên P có độ dài tỉ lệ với trọng lượng, thùng không đúng tỉ lệ.")
    b = ""
    for cxx, tt, extra in ((70, "① nhanh dần", "độ lớn a = 1,5 m/s²"), (210, "② thẳng đều", ""), (350, "③ chậm dần", "độ lớn a = 1,2 m/s²")):
        b += seg(cxx - 24, 22, cxx + 24, 22, "currentColor", 4) + seg(cxx, 22, cxx, 90, "currentColor", 2)
        b += f'<rect x="{cxx - 30}" y="90" width="60" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="2.2"/>'
        b += ct(cxx, 104, "800 kg", "currentColor", 13, "middle", "700")
        b += vec_luc(C_P, cxx, 112, 0, 1, 8000, 0.004, 3)[0] + ct(cxx + 8, 150, "P", GRN, 13, "start", "700")
        b += arrow("", "b", cxx + 46, 124, cxx + 46, 86, 3) + ct(cxx + 52, 108, "v", BLUE, 13, "start", "700")
        b += ct(cxx + 8, 62, "T = ?", ORG, 13, "start", "700")
        b += ct(cxx, 176, tt, "currentColor", 13, "middle", "700")
        if extra: b += ct(cxx, 194, extra, "currentColor", 12, "middle", "400")
    return fig("d2-2", "0 0 420 204", "Ba giai đoạn của thùng đi lên: nhanh dần, thẳng đều, chậm dần; lực căng cáp chưa biết", b,
               "Dữ kiện: ba giai đoạn, thùng đều đi lên (mũi tên v). Mũi tên P có độ dài tỉ lệ với trọng lượng; mũi tên v chỉ chiều chuyển động, không theo tỉ lệ.")

# ───────────── Dạng 3 và 5: vật trên bàn nhẵn nối vật treo ─────────────
PCX, PCY, PR = 306, 114, 14
XA0, WA, YA, HA = 90, 66, 80, 40
XB, WB, YB0, HB = 320, 64, 150, 40

def table_scene(a=None, tsec=0.5, slow=4, forces=False, labB="B", limit=False):
    S = 160                                        # px mỗi mét (chỉ để vẽ)
    n = 20
    ss = [S * 0.5 * a * (tsec * i / n) ** 2 for i in range(n + 1)] if a else None
    dur = tsec * slow
    b = f'<rect x="20" y="120" width="270" height="14" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    b += ct(30, 154, "mặt bàn nhẵn", "currentColor", 12, "start", "400")
    # dây ngang, cung quanh ròng rọc, dây đứng
    x1 = XA0 + WA
    if ss:
        b += (f'<line x1="{x1}" y1="100" x2="{PCX}" y2="100" stroke="currentColor" stroke-width="1.8">' + smil("x1", [x1 + s for s in ss], dur) + '</line>')
    else:
        b += seg(x1, 100, PCX, 100, "currentColor", 1.8)
    b += f'<path d="M{PCX},100 A{PR},{PR} 0 0 1 {PCX + PR},{PCY}" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    if ss:
        b += (f'<line x1="{XB}" y1="{PCY}" x2="{XB}" y2="{YB0}" stroke="currentColor" stroke-width="1.8">' + smil("y2", [YB0 + s for s in ss], dur) + '</line>')
    else:
        b += seg(XB, PCY, XB, YB0, "currentColor", 1.8)
    spoke = seg(PCX, PCY, PCX, PCY - PR + 3, "currentColor", 1.6)
    if ss:
        rot = ";".join(f"{math.degrees(s / PR):.1f} {PCX} {PCY}" for s in ss)
        spoke = f'<g>{spoke}<animateTransform attributeName="transform" type="rotate" values="{rot}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></g>'
    b += f'<circle cx="{PCX}" cy="{PCY}" r="{PR}" fill="none" stroke="currentColor" stroke-width="2.2"/>' + spoke + dot(PCX, PCY, 2.5)
    # vật A, B
    A = f'<rect x="{XA0}" y="{YA}" width="{WA}" height="{HA}" rx="3" fill="none" stroke="currentColor" stroke-width="2.2"/>' + ct(XA0 + 11, YA + 24, "A", "currentColor", 14, "middle", "700")
    Bx = XB - WB // 2
    B = f'<rect x="{Bx}" y="{YB0}" width="{WB}" height="{HB}" rx="3" fill="none" stroke="currentColor" stroke-width="2.2"/>' + ct(Bx + 12, YB0 + 25, labB, "currentColor", 14, "middle", "700")
    if forces:
        cxA, cyA = XA0 + WA / 2, YA + HA / 2
        A += vec_luc(C_P, cxA, cyA, 0, 1, 15, 3.5, 3)[0] + ct(cxA + 8, cyA + 56, "P_A", GRN, 13, "start", "700")
        A += vec_luc("b", cxA, cyA, 0, -1, 15, 3.5, 3)[0] + ct(cxA + 8, cyA - 40, "N", BLUE, 13, "start", "700")
        B += vec_luc(C_P, XB, YB0 + HB / 2, 0, 1, 10, 3.5, 3)[0] + ct(XB + 8, YB0 + HB / 2 + 36, "P_B", GRN, 13, "start", "700")
        A = A.replace("P_A", "P<tspan dy=\"4\" font-size=\"10\">A</tspan>").replace("P_B", "P<tspan dy=\"4\" font-size=\"10\">B</tspan>")
        B = B.replace("P_B", "P<tspan dy=\"4\" font-size=\"10\">B</tspan>")
    if ss:
        b += group(A, [(s, 0) for s in ss], dur) + group(B, [(0, s) for s in ss], dur)
    else:
        b += A + B
    if limit:
        b += ct(236, 88, "dây chịu tối đa 12 N", ORG, 12, "start", "700")
    return b

def d3(k):
    leg = ct(20, 28, "A: 1,5 kg", "currentColor", 13, "start", "700") + ct(20, 48, "B: 1,0 kg", "currentColor", 13, "start", "700")
    if k == 0:
        b = leg + table_scene(a=4.0, tsec=0.5, slow=4)
        return fig("d3-0", "0 0 420 290", "Khối A trên bàn nhẵn nối qua ròng rọc ở mép bàn với vật B treo; thả ra thì A trượt về phía ròng rọc còn B đi xuống", b,
                   "Mô phỏng: hệ thả từ nghỉ, chạy chậm 4 lần, chỉ minh hoạ chuyển động. " + NOTE)
    b = leg + table_scene(forces=True)
    return fig("d3-2", "0 0 420 290", "Các lực đã biết: trọng lực và phản lực lên A, trọng lực lên B; lực căng của dây chưa biết", b,
               "Dữ kiện: mũi tên P và N vẽ cùng tỉ lệ 3,5 px cho mỗi N (hai lực lên A bằng độ lớn); lực căng chưa vẽ. Kích thước vật không đúng tỉ lệ.")

def d5(k):
    leg = ct(20, 28, "A: 2,0 kg", "currentColor", 13, "start", "700") + ct(20, 48, "B: ? kg", ORG, 13, "start", "700")
    if k == 0:
        a = 1.0 * 10 / (2.0 + 1.0)                 # một lần thử với B nhẹ hơn mức cần tìm
        b = leg + table_scene(a=a, tsec=0.5, slow=4, labB="B", limit=True)
        return fig("d5-0", "0 0 420 290", "Khối A trên bàn nhẵn nối với vật B treo qua ròng rọc, dây chỉ chịu được một lực căng tối đa", b,
                   "Mô phỏng một lần thử với vật B nhẹ (dây không đứt), chạy chậm 4 lần; khối lượng B cần tìm. " + NOTE)
    b = leg + table_scene(labB="B", limit=True)
    b += ct(236, 70, "đứt khi T vượt mức này", "currentColor", 12, "start", "400")
    return fig("d5-2", "0 0 420 290", "Dữ kiện: A 2,0 kg trên bàn nhẵn, B chưa biết khối lượng, dây chịu tối đa 12 N", b,
               "Dữ kiện: khối lượng A, giới hạn của dây; khối lượng B chưa biết. " + NOTE)

# ───────────── Dạng 4: hai vật treo hai bên ròng rọc cố định ─────────────
def d4(k):
    cx, cy, R = 210, 68, 36
    xa, xb = cx - R, cx + R
    yA0, hA, wA = 156, 36, 70
    wB, hB = 60, 32
    a, tsec, slow, S = 2.5, 0.9, 3, 40
    n = 18
    ss = [S * 0.5 * a * (tsec * i / n) ** 2 for i in range(n + 1)] if k == 0 else None
    dur = tsec * slow
    b = seg(150, 14, 270, 14, "currentColor", 4) + seg(cx, 14, cx, cy - R, "currentColor", 2)
    if ss:
        b += f'<line x1="{xa}" y1="{cy}" x2="{xa}" y2="{yA0}" stroke="currentColor" stroke-width="1.8">' + smil("y2", [yA0 + s for s in ss], dur) + '</line>'
        b += f'<line x1="{xb}" y1="{cy}" x2="{xb}" y2="{yA0}" stroke="currentColor" stroke-width="1.8">' + smil("y2", [yA0 - s for s in ss], dur) + '</line>'
    else:
        b += seg(xa, cy, xa, yA0, "currentColor", 1.8) + seg(xb, cy, xb, yA0, "currentColor", 1.8)
    spoke = seg(cx, cy, cx, cy - R + 5, "currentColor", 1.6)
    if ss:
        rot = ";".join(f"{-math.degrees(s / R):.1f} {cx} {cy}" for s in ss)
        spoke = f'<g>{spoke}<animateTransform attributeName="transform" type="rotate" values="{rot}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></g>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="currentColor" stroke-width="2.2"/>' + spoke + dot(cx, cy, 2.5)
    A = f'<rect x="{xa - wA // 2}" y="{yA0}" width="{wA}" height="{hA}" rx="3" fill="none" stroke="currentColor" stroke-width="2.2"/>' + sub(xa - wA // 2 + 6, yA0 + 24, "m", "1", "currentColor", 14)
    B = f'<rect x="{xb - wB // 2}" y="{yA0}" width="{wB}" height="{hB}" rx="3" fill="none" stroke="currentColor" stroke-width="2.2"/>' + sub(xb - wB // 2 + 6, yA0 + 22, "m", "2", "currentColor", 14)
    if k == 2:
        A += vec_luc(C_P, xa, yA0 + hA / 2, 0, 1, 50, 1.3, 3)[0] + sub(xa + 8, yA0 + hA / 2 + 62, "P", "1", GRN, 13)
        B += vec_luc(C_P, xb, yA0 + hB / 2, 0, 1, 30, 1.3, 3)[0] + sub(xb + 8, yA0 + hB / 2 + 36, "P", "2", GRN, 13)
    if ss:
        b += group(A, [(0, s) for s in ss], dur) + group(B, [(0, -s) for s in ss], dur)
    else:
        b += A + B
    leg = ct(16, 40, "m₁ = 5,0 kg", "currentColor", 13, "start", "700") + ct(16, 60, "m₂ = 3,0 kg", "currentColor", 13, "start", "700")
    b += leg
    if k == 0:
        return fig("d4-0", "0 0 420 250", "Hai vật treo hai đầu dây vắt qua ròng rọc cố định, thả từ cùng độ cao thì vật bên trái đi xuống, vật bên phải đi lên", b,
                   "Mô phỏng chỉ để đối chiếu sau khi đã tự xác định chuyển động của từng vật; chạy chậm 3 lần. " + NOTE)
    return fig("d4-2", "0 0 420 250", "Các lực đã biết: trọng lực của hai vật; lực căng của dây chưa biết", b,
               "Dữ kiện: mũi tên P vẽ cùng tỉ lệ 1,3 px cho mỗi N; lực căng chưa vẽ. Kích thước vật không đúng tỉ lệ.")

BUILD = [d1, d2, d3, d4, d5]

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Khối lượng, trọng lượng và gia tốc rơi tự do của từng nơi", topic=T125,
      problem_html=r'<p>Một xe tự hành thám hiểm có khối lượng $90\ \text{kg}$ được kiểm tra trên Trái Đất ($g=9{,}8\ \text{m/s}^2$) rồi chuyển lên Sao Hoả, nơi gia tốc rơi tự do là $3{,}7\ \text{m/s}^2$. Mỗi nơi, xe được treo đứng yên vào một lực kế (hình dưới).</p><ol type="a"><li>Tính trọng lượng của xe trên Trái Đất.</li><li>Khối lượng của xe trên Sao Hoả là bao nhiêu?</li><li>Tính trọng lượng của xe trên Sao Hoả.</li></ol>'),
 dict(label="Dạng 2 · Trung bình · Vật treo thẳng đứng: lực căng khi đứng yên và khi có gia tốc", topic=T126,
      problem_html=r'<p>Một tời điện nâng thùng hàng khối lượng $800\ \text{kg}$ lên cao bằng sợi cáp thép nhẹ, thẳng đứng (hình dưới). Lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Thùng đang đi lên thẳng đều. Tính lực căng của cáp.</li><li>Lúc khởi động, thùng đi lên nhanh dần với gia tốc có độ lớn $1{,}5\ \text{m/s}^2$. Tính lực căng của cáp.</li><li>Sắp tới nơi, thùng đi lên chậm dần với gia tốc có độ lớn $1{,}2\ \text{m/s}^2$. Tính lực căng của cáp.</li><li>Cáp chịu được lực căng tối đa $9\,000\ \text{N}$. Trong ba giai đoạn trên, cáp có bị đứt không? Nếu có thì ở giai đoạn nào?</li></ol>'),
 dict(label="Dạng 3 · Trung bình · Vật trên bàn nhẵn nối vật treo qua ròng rọc", topic=T126,
      problem_html=r'<p>Khối $A$ khối lượng $1{,}5\ \text{kg}$ nằm trên mặt bàn nằm ngang nhẵn, được nối bằng sợi dây nhẹ, không dãn vắt qua ròng rọc nhẹ ở mép bàn với vật $B$ khối lượng $1{,}0\ \text{kg}$ treo thẳng đứng (hình dưới). Thả cho hệ chuyển động từ nghỉ. Bỏ qua mọi ma sát, lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Tính gia tốc của hệ.</li><li>Tính lực căng của dây.</li><li>So sánh lực căng của dây với trọng lượng của $B$.</li></ol>'),
 dict(label="Dạng 4 · Khó · Hai vật treo hai bên ròng rọc cố định", topic=T126,
      problem_html=r'<p>Hai vật có khối lượng $m_1=5{,}0\ \text{kg}$ và $m_2=3{,}0\ \text{kg}$ được buộc vào hai đầu một sợi dây nhẹ, không dãn, vắt qua ròng rọc cố định nhẹ, không ma sát (hình dưới). Giữ hai vật ở cùng độ cao rồi thả nhẹ. Lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Tính độ lớn gia tốc của mỗi vật.</li><li>Tính lực căng của dây.</li><li>Lực căng lớn hơn, nhỏ hơn hay nằm giữa trọng lượng của hai vật?</li></ol>'),
 dict(label="Dạng 5 · Khó · Bài ngược: dây chỉ chịu lực căng tối đa", topic=T126,
      problem_html=r'<p>Khối $A$ khối lượng $2{,}0\ \text{kg}$ nằm trên mặt bàn nằm ngang nhẵn, được nối bằng sợi dây nhẹ, không dãn vắt qua ròng rọc nhẹ ở mép bàn với vật $B$ treo thẳng đứng (hình dưới). Dây này chỉ chịu được lực căng tối đa $12\ \text{N}$; vượt mức đó dây đứt. Thả cho hệ chuyển động từ nghỉ, bỏ qua mọi ma sát, lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Gia tốc lớn nhất của hệ để dây không đứt bằng bao nhiêu?</li><li>Vật $B$ có thể có khối lượng lớn nhất bao nhiêu kilôgam để dây không đứt?</li></ol>'),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 3 chỉ khái niệm/điều kiện; hàng cần tìm: “Đại lượng cần tìm”) ═════════════
CT = "Đại lượng cần tìm"
ANALYSIS = [
 [("“xe tự hành … khối lượng $90$ kg”", "$m=90$ kg", "Khối lượng (kg): lượng chất của vật"),
  ("“trên Trái Đất ($g=9{,}8$ m/s²)”", "$g_1=9{,}8$ m/s²", "Trọng lực, trọng lượng (N)"),
  ("“chuyển lên Sao Hoả … $3{,}7$ m/s²”", "$g_2=3{,}7$ m/s²", "⚠ Gia tốc rơi tự do phụ thuộc nơi đặt vật; xe đứng yên trên mặt hành tinh đó"),
  ("“trọng lượng … trên Trái Đất”", "$P_1=\\,?$", CT),
  ("“khối lượng … trên Sao Hoả”", "$m_2=\\,?$", CT),
  ("“trọng lượng … trên Sao Hoả”", "$P_2=\\,?$", CT)],
 [("“tời … nâng thùng hàng khối lượng $800$ kg”", "$m=800$ kg", "Vật treo chịu trọng lực và lực căng của cáp"),
  ("“cáp thép nhẹ, thẳng đứng”", "cáp nhẹ, thẳng đứng", "⚠ Cáp nhẹ: lực căng như nhau ở mọi điểm; cáp chỉ kéo, không đẩy"),
  ("“lấy $g=10$ m/s²”", "$g=10$ m/s²", "Trọng lực của thùng"),
  ("“đi lên thẳng đều”", "$v$ không đổi", "Chuyển động thẳng đều"),
  ("“nhanh dần … $1{,}5$ m/s²”", "$|a|=1{,}5$ m/s²", "Chiều của gia tốc so với vận tốc: nhanh dần hay chậm dần"),
  ("“chậm dần … $1{,}2$ m/s²”", "$|a|=1{,}2$ m/s²", "Chiều của gia tốc so với vận tốc: nhanh dần hay chậm dần"),
  ("“cáp chịu được lực căng tối đa $9\\,000$ N”", "$T_{max}=9\\,000$ N", "⚠ Cáp đứt khi lực căng vượt mức tối đa"),
  ("“tính lực căng của cáp”", "$T=\\,?$ ở ba giai đoạn", CT),
  ("“cáp có bị đứt không … giai đoạn nào”", "so $T$ với $T_{max}$", CT)],
 [("“khối $A$ … $1{,}5$ kg”", "$m_A=1{,}5$ kg", "Vật thứ nhất của hệ, nằm trên mặt ngang"),
  ("“mặt bàn nằm ngang nhẵn”", "không ma sát", "⚠ Không ma sát: mặt bàn chỉ tác dụng lực vuông góc với mặt"),
  ("“dây nhẹ, không dãn … ròng rọc nhẹ”", "dây nhẹ, không dãn", "⚠ Dây nhẹ, không dãn, ròng rọc nhẹ nhẵn: các vật nối dây cùng độ lớn gia tốc; lực căng hai bên bằng nhau"),
  ("“vật $B$ … $1{,}0$ kg treo thẳng đứng”", "$m_B=1{,}0$ kg", "Vật thứ hai của hệ, chịu trọng lực và lực căng"),
  ("“thả … từ nghỉ”", "$v_0=0$", "Chuyển động bắt đầu từ trạng thái nghỉ"),
  ("“lấy $g=10$ m/s²”", "$g=10$ m/s²", "Trọng lực của từng vật"),
  ("“gia tốc của hệ”, “lực căng của dây”", "$a=\\,?$; $T=\\,?$", CT),
  ("“so sánh lực căng … với trọng lượng của $B$”", "$T$ so với $P_B$", CT)],
 [("“hai vật $m_1=5{,}0$ kg và $m_2=3{,}0$ kg”", "$m_1=5{,}0$ kg; $m_2=3{,}0$ kg", "Hai vật nối dây; mỗi vật chịu trọng lực và lực căng"),
  ("“dây nhẹ, không dãn … ròng rọc cố định nhẹ, không ma sát”", "dây nhẹ, không dãn", "⚠ Dây nhẹ, không dãn, ròng rọc nhẹ nhẵn: hai vật cùng độ lớn gia tốc; lực căng hai bên bằng nhau"),
  ("“cùng độ cao rồi thả nhẹ”", "$v_0=0$", "Chuyển động bắt đầu từ trạng thái nghỉ"),
  ("“lấy $g=10$ m/s²”", "$g=10$ m/s²", "Trọng lực của từng vật"),
  ("“độ lớn gia tốc của mỗi vật”", "$a=\\,?$", CT),
  ("“lực căng của dây”", "$T=\\,?$", CT),
  ("“lớn hơn, nhỏ hơn hay nằm giữa trọng lượng”", "$T$ so với $P_1$, $P_2$", CT)],
 [("“khối $A$ … $2{,}0$ kg … mặt bàn nằm ngang nhẵn”", "$m_A=2{,}0$ kg; không ma sát", "⚠ Không ma sát: mặt bàn chỉ tác dụng lực vuông góc với mặt"),
  ("“dây nhẹ, không dãn … ròng rọc nhẹ”", "dây nhẹ, không dãn", "⚠ Dây nhẹ, không dãn, ròng rọc nhẹ nhẵn: các vật nối dây cùng độ lớn gia tốc; lực căng hai bên bằng nhau"),
  ("“vật $B$ treo thẳng đứng”", "$m_B$ chưa biết", "Vật thứ hai của hệ, chịu trọng lực và lực căng"),
  ("“chỉ chịu được lực căng tối đa $12$ N”", "$T\\le12$ N", "⚠ Dây đứt khi lực căng vượt giới hạn; bài hỏi mức lớn nhất vẫn an toàn"),
  ("“thả … từ nghỉ”; “lấy $g=10$ m/s²”", "$v_0=0$; $g=10$ m/s²", "Chuyển động bắt đầu từ nghỉ; trọng lực của B"),
  ("“gia tốc lớn nhất của hệ”", "$a_{max}=\\,?$", CT),
  ("“khối lượng lớn nhất” của $B$", "$m_{B,max}=\\,?$", CT)],
]

# ═════════════ LỜI GIẢI ═════════════
RN1 = [r"Khối lượng $m$ (kg): lượng chất của vật, không đổi khi đổi nơi",
       r"Trọng lượng $P$ (N): độ lớn trọng lực, $P=mg$, đổi theo $g$ của nơi đặt vật",
       r"Điều kiện: vật đứng yên so với mặt đất của hành tinh đang xét"]
RN2 = [r"Vật treo chịu trọng lực $\vec P$ (hướng xuống) và lực căng $\vec T$ (hướng lên)",
       r"Định luật II Newton theo phương thẳng đứng; chọn chiều dương hướng lên",
       r"$a=0$ (đứng yên, thẳng đều) thì $T=P$; có gia tốc thì $T\ne P$",
       r"Điều kiện: cáp nhẹ, thẳng đứng"]
RN3 = [r"Mỗi vật viết $F=ma$ riêng, chiều dương theo chiều chuyển động của vật đó",
       r"Dây nhẹ, không dãn; ròng rọc nhẹ, nhẵn: hai vật cùng độ lớn $a$, lực căng hai bên như nhau",
       r"Mặt bàn nhẵn: theo phương ngang không có ma sát",
       r"Điều kiện: bỏ qua ma sát, thả từ nghỉ"]
RN4 = [r"Dây nhẹ, không dãn: hai vật cùng độ lớn gia tốc $a$; ròng rọc nhẹ, nhẵn: hai bên cùng lực căng $T$",
       r"Mỗi vật chịu trọng lực và lực căng; viết $F=ma$ riêng, chiều dương theo chiều chuyển động của vật đó",
       r"Thả từ nghỉ: vật nặng hơn đi xuống, vật nhẹ hơn đi lên",
       r"Điều kiện: bỏ qua ma sát, khối lượng của dây và ròng rọc"]
RN5 = [r"Hệ vật nối dây: cùng $a$, cùng $T$; viết $F=ma$ riêng cho từng vật",
       r"Mặt bàn nhẵn: theo phương ngang A chỉ chịu lực căng $T$",
       r"Dây không đứt khi $T\le T_{max}$; $T$ tăng khi $a$ tăng",
       r"Điều kiện: bỏ qua ma sát, thả từ nghỉ"]

SOLS = [
 sol(RN1, [
  ("Trọng lượng trên Trái Đất", [P(r"Dùng $g$ của Trái Đất:"), M(r"P=mg=90\cdot9{,}8"), A(r"P=882\ \text{N}")]),
  ("Khối lượng trên Sao Hoả", [P("Khối lượng là lượng chất của xe, không phụ thuộc nơi đặt:"), A(r"m'=m=90\ \text{kg}")]),
  ("Trọng lượng trên Sao Hoả", [P(r"Dùng $g'$ của Sao Hoả, khối lượng vẫn $90$ kg:"), M(r"P'=mg'=90\cdot3{,}7"), A(r"P'=333\ \text{N}")]),
  ("Kiểm tra", [P(r"$\dfrac{P'}{P}=\dfrac{333}{882}\approx0{,}378=\dfrac{g'}{g}$ ✓ (cùng một xe nên tỉ số trọng lượng bằng tỉ số $g$)."), P("Đơn vị: kg·m/s² = N ✓")])],
  [r"a) $P=882\ \text{N}$", r"b) $m'=90\ \text{kg}$", r"c) $P'=333\ \text{N}$"],
  "Nhận dạng: đề cho <strong>khối lượng</strong> và <strong>g của từng nơi</strong> → khối lượng giữ nguyên, trọng lượng nhân với $g$ của nơi đang xét."),
 sol(RN2, [
  ("Thùng đi lên thẳng đều", [P(r"$a=0$ nên hợp lực bằng $0$. Chiều dương hướng lên:"), M(r"T-P=0"), M(r"T=P=mg=800\cdot10"), A(r"T=8000\ \text{N}")]),
  ("Khởi động: nhanh dần đi lên", [P(r"Đang đi lên mà nhanh dần nên $\vec a$ hướng lên (cùng chiều dương):"), M(r"T-P=ma"), M(r"T=m(g+a)=800\cdot(10+1{,}5)"), A(r"T=9200\ \text{N}")]),
  ("Sắp dừng: chậm dần đi lên", [P(r"Đang đi lên mà chậm dần nên $\vec a$ hướng xuống (ngược chiều dương):"), M(r"T-P=-ma"), M(r"T=m(g-a)=800\cdot(10-1{,}2)"), A(r"T=7040\ \text{N}")]),
  ("So với giới hạn của cáp", [P(r"Ba lực căng: $8000$ N, $9200$ N, $7040$ N. Chỉ lúc khởi động mới vượt mức $9000$ N:"), A(r"T:Cáp <strong>đứt ở lúc khởi động</strong> ($9200\ \text{N}\gt9000\ \text{N}$)."), P("Đơn vị: kg·m/s² = N ✓. Lực căng lớn nhất khi gia tốc hướng lên, nhỏ nhất khi gia tốc hướng xuống.")])],
  [r"a) $T=8000\ \text{N}$", r"b) $T=9200\ \text{N}$", r"c) $T=7040\ \text{N}$", r"d) Có: cáp đứt ở lúc khởi động ($9200\ \text{N}\gt9000\ \text{N}$)"],
  r"Nhận dạng: đề cho <strong>vật treo nhanh dần hoặc chậm dần</strong> → xác định chiều của $\vec a$ trước, rồi mới viết $T-P=\pm ma$."),
 sol(RN3, [
  ("Vật A (phương ngang)", [P(r"Chiều dương về phía ròng rọc. Theo phương thẳng đứng $N$ cân bằng $P_A$; bàn nhẵn nên theo phương ngang chỉ còn $T$:"), M(r"T=m_Aa\quad(1)")]),
  ("Vật B và gia tốc", [P("Chiều dương hướng xuống:"), M(r"P_B-T=m_Ba\quad(2)"), M(r"P_B=m_Bg=1{,}0\cdot10=10\ \text{N}"), P("Cộng (1) và (2) để khử $T$:"), M(r"P_B=(m_A+m_B)a"), M(r"a=\dfrac{P_B}{m_A+m_B}=\dfrac{10}{1{,}5+1{,}0}"), A(r"a=4\ \text{m/s}^2")]),
  ("Lực căng dây", [P("Thế vào (1):"), M(r"T=m_Aa=1{,}5\cdot4"), A(r"T=6\ \text{N}"), P(r"Kiểm tra với B: $P_B-T=10-6=4\ \text{N}=m_Ba=1{,}0\cdot4$ ✓")]),
  (r"So sánh $T$ với $P_B$", [M(r"T=6\ \text{N}\lt P_B=10\ \text{N}"), P(r"B đi xuống nhanh dần nên hợp lực lên B hướng xuống: $P_B\gt T$. Chỉ khi hệ đứng yên mới có $T=P_B$.")])],
  [r"a) $a=4\ \text{m/s}^2$", r"b) $T=6\ \text{N}$", r"c) $T\lt P_B$ ($6\ \text{N}\lt10\ \text{N}$)"],
  r"Nhận dạng: đề có <strong>dây nối hai vật qua ròng rọc</strong> → viết $F=ma$ riêng cho từng vật (cùng $a$, cùng $T$) rồi cộng để khử $T$."),
 sol(RN4, [
  ("Phương trình cho từng vật", [P(r"$m_1$ nặng hơn nên đi xuống, $m_2$ đi lên. Chiều dương của mỗi vật theo chiều chuyển động của nó:"), M(r"P_1-T=m_1a\quad(1)"), M(r"T-P_2=m_2a\quad(2)"), M(r"P_1=m_1g=50\ \text{N};\quad P_2=m_2g=30\ \text{N}")]),
  ("Gia tốc", [P("Cộng (1) và (2) để khử $T$:"), M(r"P_1-P_2=(m_1+m_2)a"), M(r"a=\dfrac{P_1-P_2}{m_1+m_2}=\dfrac{50-30}{5{,}0+3{,}0}"), A(r"a=2{,}5\ \text{m/s}^2")]),
  ("Lực căng dây", [P("Thế vào (2):"), M(r"T=P_2+m_2a=30+3{,}0\cdot2{,}5"), A(r"T=37{,}5\ \text{N}"), P(r"Kiểm tra bằng (1): $P_1-m_1a=50-5{,}0\cdot2{,}5=37{,}5\ \text{N}$ ✓")]),
  (r"So sánh $T$ với hai trọng lượng", [M(r"P_2=30\ \text{N}\lt T=37{,}5\ \text{N}\lt P_1=50\ \text{N}"), P(r"$m_1$ đi xuống nhanh dần nên $T\lt P_1$; $m_2$ đi lên nhanh dần nên $T\gt P_2$.")])],
  [r"a) $a=2{,}5\ \text{m/s}^2$", r"b) $T=37{,}5\ \text{N}$", r"c) $P_2\lt T\lt P_1$ ($30\ \text{N}\lt37{,}5\ \text{N}\lt50\ \text{N}$)"],
  "Nhận dạng: đề có <strong>hai vật treo hai bên ròng rọc</strong> → vật nặng đi xuống, vật nhẹ đi lên; viết $F=ma$ cho từng vật rồi cộng."),
 sol(RN5, [
  ("Gia tốc lớn nhất cho phép", [P(r"Vật A (chiều dương về phía ròng rọc) chỉ chịu $T$:"), M(r"T=m_Aa"), P(r"Dây không đứt khi $T\le12\ \text{N}$:"), M(r"a\le\dfrac{T_{max}}{m_A}=\dfrac{12}{2{,}0}"), A(r"a_{max}=6\ \text{m/s}^2")]),
  ("Khối lượng lớn nhất của B", [P(r"Vật B (chiều dương hướng xuống), khi $T=T_{max}$ và $a=a_{max}$:"), M(r"m_Bg-T_{max}=m_Ba_{max}"), M(r"m_B(g-a_{max})=T_{max}"), M(r"m_{B}=\dfrac{T_{max}}{g-a_{max}}=\dfrac{12}{10-6}"), A(r"m_{B,max}=3\ \text{kg}")]),
  ("Kiểm tra", [P(r"Thế ngược: $a=\dfrac{m_Bg}{m_A+m_B}=\dfrac{3\cdot10}{2+3}=6\ \text{m/s}^2$ ✓ và $T=m_Aa=2\cdot6=12\ \text{N}$ ✓."), P(r"B nặng hơn thì $a$ lớn hơn, $T=m_Aa$ lớn hơn $12$ N nên dây đứt: $3$ kg đúng là giá trị lớn nhất.")])],
  [r"a) $a_{max}=6\ \text{m/s}^2$", r"b) $m_{B,max}=3\ \text{kg}$"],
  "Nhận dạng: đề cho <strong>giới hạn lực căng của dây</strong> và hỏi khối lượng lớn nhất → đi ngược từ giới hạn của dây trở lại."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang="Thấy <b>khối lượng</b> cùng <b>g của từng nơi</b> → nghĩ tới trọng lượng đổi theo g, khối lượng giữ nguyên.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Trọng lượng trên Trái Đất", "Trọng lượng của xe trên Trái Đất bằng bao nhiêu N?", 882, "N", 1,
       loi=r"Chia thay vì nhân ($m/g$), hoặc lấy số kilôgam làm trọng lượng vì quên rằng khối lượng (kg) chưa phải lực (N)."),
  buoc("Khối lượng trên Sao Hoả", "Khối lượng của xe trên Sao Hoả bằng bao nhiêu kg?", 90, "kg", 0.5,
       loi=r"Nhân khối lượng với $\dfrac{g'}{g}$.",
       ke=[("Xét xem khối lượng có phụ thuộc $g$ của nơi đặt vật không", True),
           (r"Khối lượng giảm theo $g$: $m'=m\cdot\dfrac{g'}{g}$", "Đó là cách tính của trọng lượng. Khối lượng là lượng chất của xe, đổi nơi cũng không mất bớt chất."),
           (r"Tính $m'=\dfrac{P}{g'}$ với $P$ là trọng lượng trên Trái Đất", "Trọng lượng trên Trái Đất không dùng được cho Sao Hoả; khối lượng cũng không phụ thuộc $g$ nên không cần tính lại.")]),
  buoc("Trọng lượng trên Sao Hoả", "Trọng lượng của xe trên Sao Hoả bằng bao nhiêu N?", 333, "N", 1,
       loi=r"Dùng $g=9{,}8$ của Trái Đất cho cả hai nơi, hoặc chia khối lượng cho $g$ thay vì nhân.",
       ke=[("Dùng $g$ của nơi vật đang đứng để tính trọng lượng", True),
           (r"$P'=mg$ với $g=9{,}8$ vì khối lượng không đổi", "Trọng lượng phụ thuộc $g$ của nơi đặt vật; $g$ ở Sao Hoả khác nên $P'$ khác."),
           (r"$P'=P\cdot\dfrac{g}{g'}$", "Tỉ số bị lật: trọng lượng tỉ lệ thuận với $g'$, không phải với $g/g'$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>vật treo nhanh dần hoặc chậm dần</b> → xét <b>chiều gia tốc</b> trước, vì khi đó lực căng khác trọng lượng.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Thùng đi lên thẳng đều", "Lực căng của cáp khi thùng đi lên thẳng đều bằng bao nhiêu N?", 8000, "N", 20,
       loi=r"Cộng thêm $ma$ dù thẳng đều ($a=0$), hoặc quên nhân $g$ nên ra khối lượng chứ không phải lực."),
  buoc("Khởi động: nhanh dần đi lên", "Lực căng của cáp lúc khởi động, nhanh dần đi lên, bằng bao nhiêu N?", 9200, "N", 20,
       loi=r"Lấy $T=m(g-a)$ (nhầm chiều gia tốc), hoặc $T=ma$ (quên trọng lực).",
       ke=[(r"Xác định chiều của $\vec a$ so với chiều chuyển động rồi viết $F=ma$", True),
           (r"$T=P$ như lúc thẳng đều", "Chỉ đúng khi $a=0$; ở đây vật có gia tốc nên $T$ khác $P$."),
           (r"$P-T=ma$", "Dấu của phương trình phụ thuộc chiều của $\\vec a$; phải đối chiếu với đề (nhanh dần hay chậm dần) trước khi chọn.")]),
  buoc("Sắp dừng: chậm dần đi lên", "Lực căng của cáp lúc sắp dừng, chậm dần đi lên, bằng bao nhiêu N?", 7040, "N", 20,
       loi=r"Dùng lại phương trình của giai đoạn nhanh dần mà không xét lại chiều của $\vec a$, hoặc kết luận $T=P$ vì thùng vẫn đi lên.",
       ke=[(r"Xác định chiều của $\vec a$ so với chiều chuyển động rồi viết $F=ma$", True),
           (r"Giống bước trước: $T-P=ma$", r"Mỗi giai đoạn phải xác định lại chiều của $\vec a$; không sao chép phương trình từ giai đoạn khác."),
           (r"$T=P$ vì thùng vẫn đi lên", r"Đi lên không làm $T=P$; chỉ khi $a=0$ mới như vậy, mà vận tốc đang đổi.")]),
  buoc("So với giới hạn của cáp", "Cáp chịu tối đa $9\\,000\\ \\text{N}$. Cáp có bị đứt không, và ở giai đoạn nào?",
       loi=r"So mức $9\,000$ N với trọng lượng của thùng thay vì với lực căng đã tìm cho từng giai đoạn.",
       lua_chon=[("Đứt, ở lúc khởi động nhanh dần đi lên", True),
                 (r"Không đứt: trọng lượng nhỏ hơn mức tối đa của cáp", "Chỉ khi $a=0$ lực căng mới bằng trọng lượng. Nhanh dần đi lên thì $T$ lớn hơn $P$ (kết quả bước 2), nên đã vượt mức tối đa."),
                 ("Đứt, ở lúc sắp dừng, chậm dần đi lên", "Lúc này hợp lực hướng xuống nên lực căng nhỏ hơn cả lúc thẳng đều, chưa tới mức tối đa.")],
       ke=[("So từng lực căng vừa tìm với mức tối đa của cáp", True),
           ("Chỉ so trọng lượng của thùng với mức tối đa", "Trọng lượng chỉ bằng lực căng khi $a=0$; khi có gia tốc thì $T$ khác $P$."),
           ("Chọn giai đoạn có vận tốc lớn nhất", "Lực căng phụ thuộc gia tốc, không phụ thuộc vận tốc.")])]),
 dict(nhan_dang="Thấy <b>dây nối hai vật qua ròng rọc</b> → nghĩ tới cùng gia tốc, cùng lực căng, viết phương trình cho từng vật.",
  cap_do=3, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Vật A (phương ngang)", "Theo phương ngang, hợp lực tác dụng lên A là:",
       loi=r"Đưa $P_A$ hoặc $N$ vào phương trình ngang, hoặc nghĩ bàn có ma sát dù đề cho bàn nhẵn.",
       lua_chon=[(r"chỉ có lực căng $T$ của dây", True),
                 (r"$T-P_A$", "$P_A$ thẳng đứng nên không có mặt trong phương trình theo phương ngang."),
                 (r"$T-N$", "$N$ cũng thẳng đứng và cân bằng với $P_A$; không có thành phần theo phương ngang.")]),
  buoc("Vật B và gia tốc", "Gia tốc của hệ bằng bao nhiêu m/s²?", 4, "m/s²", 0.05,
       loi=r"Chia cho $m_B$ thay vì cho $m_A+m_B$, hoặc quên đổi $P_B=m_Bg$.",
       ke=[("Viết thêm phương trình của B rồi cộng với phương trình của A để khử $T$", True),
           (r"Lấy $a=\dfrac{P_B}{m_B}$ (chỉ xét B)", "Dây kéo cả A nên khối lượng cần gia tốc là $m_A+m_B$, không chỉ $m_B$."),
           (r"Lấy $a=g$ vì B đang đi xuống", "B bị dây giữ nên không rơi tự do; $a$ nhỏ hơn $g$ vì còn phải kéo A.")]),
  buoc("Lực căng dây", "Lực căng của dây bằng bao nhiêu N?", 6, "N", 0.1,
       loi=r"Lấy $T=P_B$ (nhầm hệ đứng yên), hoặc $T=m_Ba$ (đó là hợp lực lên B, không phải lực căng).",
       ke=[("Thế $a$ vào phương trình của vật A", True),
           (r"$T=P_B$ vì B treo vào dây", "Chỉ đúng khi B đứng yên hoặc đi đều; B đang có gia tốc nên $T$ khác $P_B$."),
           (r"$T=m_Ba$", r"$m_Ba$ là hợp lực lên B, không phải $T$; hợp lực lên B là $P_B-T$.")]),
  buoc(r"So sánh $T$ với $P_B$", r"So với trọng lượng $P_B$ của vật B, lực căng của dây:",
       loi=r"Coi $T=P_B$ ở mọi lúc, hoặc coi $T=P_A$ vì dây nối với A.",
       lua_chon=[("nhỏ hơn $P_B$, vì B đi xuống nhanh dần", True),
                 ("bằng $P_B$, vì dây treo B", "$T=P$ chỉ khi B đứng yên hoặc đi thẳng đều; ở đây B có gia tốc hướng xuống."),
                 ("lớn hơn $P_B$, vì dây còn kéo cả A", "Nếu $T\\gt P_B$ thì hợp lực lên B hướng lên, B không thể đi xuống nhanh dần.")],
       ke=[("Xét hợp lực lên B", True),
           (r"Coi $T=P_B$ vì B treo vào dây", r"Đúng khi B đứng yên hoặc đi đều; B đang có gia tốc nên $T\ne P_B$."),
           (r"Coi $T=P_A$ vì dây nối với A", r"$P_A$ đã cân bằng với $N$, không kéo dây; lực căng chỉ làm A tăng tốc theo phương ngang.")])]),
 dict(nhan_dang="Thấy <b>hai vật treo hai bên ròng rọc</b> → nghĩ tới vật nặng đi xuống, vật nhẹ đi lên, cùng độ lớn gia tốc.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Phương trình cho từng vật", "Hai vật thả nhẹ từ cùng độ cao. Cách viết $F=ma$ đúng là:",
       loi=r"Chỉ viết cho một vật, hoặc dùng một chiều dương chung cho cả hai vật.",
       lua_chon=[(r"Chọn chiều dương theo chuyển động của từng vật rồi viết $F=ma$ riêng cho mỗi vật", True),
                 (r"Dùng một chiều dương chung hướng xuống cho cả hai vật", "Một chiều dương chung chỉ hợp lý khi hai vật chuyển động cùng chiều; phải xét chiều chuyển động của từng vật."),
                 (r"Chỉ viết $F=ma$ cho vật nặng hơn, vì vật nhẹ bị kéo theo", "Lực căng chưa biết nên cần hai phương trình; phải viết cho cả hai vật.")]),
  buoc("Gia tốc", "Gia tốc của mỗi vật bằng bao nhiêu m/s²?", 2.5, "m/s²", 0.05,
       loi=r"Chia hiệu trọng lượng cho một khối lượng ($m_1$ hoặc $m_2$) thay vì cho tổng, hoặc lấy tổng trọng lượng ở tử số.",
       ke=[("Cộng hai phương trình để khử $T$, rồi chia cho cả hai khối lượng", True),
           (r"Lấy $a=\dfrac{P_1-P_2}{m_1}$", "Cả hai vật cùng được gia tốc nên khối lượng chuyển động là $m_1+m_2$, không chỉ $m_1$."),
           (r"Lấy $a=g$ vì có một vật đang đi xuống", "$m_1$ bị dây giữ nên không rơi tự do; $a$ nhỏ hơn $g$ vì còn phải nâng $m_2$.")]),
  buoc("Lực căng dây", "Lực căng của dây bằng bao nhiêu N?", 37.5, "N", 0.3,
       loi=r"Lấy $T=P_1$ hoặc $T=\dfrac{P_1+P_2}{2}$ cho nhanh, bỏ qua gia tốc.",
       ke=[("Thế $a$ vào phương trình của một vật", True),
           (r"$T=\dfrac{P_1+P_2}{2}$", "Trung bình cộng hai trọng lượng không phải lực căng; $T$ xác định từ phương trình chuyển động của từng vật."),
           (r"$T=P_1$ vì dây treo $m_1$", "$T=P$ chỉ khi không có gia tốc; hệ đang có gia tốc nên $T$ khác $P_1$.")]),
  buoc("So sánh $T$ với hai trọng lượng", "Lực căng của dây so với trọng lượng của hai vật:",
       loi=r"Coi $T$ bằng trọng lượng của vật nặng, hoặc coi $T$ nhỏ hơn cả hai trọng lượng.",
       lua_chon=[(r"$P_2\lt T\lt P_1$", True),
                 (r"$T=P_1=P_2$", "Hai trọng lượng khác nhau nên không thể cùng bằng $T$; hệ có gia tốc nên $T$ cũng khác từng trọng lượng."),
                 (r"$T\gt P_1$", r"$m_1$ đi xuống nhanh dần nên hợp lực lên $m_1$ hướng xuống, tức $P_1\gt T$.")],
       ke=[("Xét hợp lực lên từng vật theo chiều chuyển động của nó", True),
           ("Coi $T$ bằng trọng lượng của vật nặng vì nó kéo dây", "Chỉ đúng khi vật đứng yên; hệ đang có gia tốc nên $T$ khác trọng lượng."),
           ("Coi $T$ bằng trọng lượng của vật nhẹ vì nó được dây nâng", "Chỉ đúng khi vật đứng yên; vật nhẹ cũng đang có gia tốc.")])]),
 dict(nhan_dang="Thấy <b>dây chịu lực căng tối đa</b> và hỏi <b>khối lượng lớn nhất</b> → nghĩ tới bài ngược: đi từ giới hạn của dây.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Gia tốc lớn nhất cho phép", "Gia tốc lớn nhất của hệ để dây không đứt (dây chịu tối đa $12\\ \\text{N}$) bằng bao nhiêu m/s²?", 6, "m/s²", 0.1,
       loi=r"Chia $T_{max}$ cho $m_B$ (chưa biết) hoặc cho tổng khối lượng; lực căng chỉ làm A tăng tốc nên phải chia cho $m_A$."),
  buoc("Khối lượng lớn nhất của B", "Khối lượng lớn nhất của vật B bằng bao nhiêu kg?", 3, "kg", 0.05,
       loi=r"Lấy $T_{max}=P_B$ (coi B đứng yên), hoặc $T_{max}=m_Ba$ (quên trọng lực của B).",
       ke=[("Viết phương trình của B với $T=T_{max}$, $a=a_{max}$ rồi rút $m_B$", True),
           (r"Lấy $m_B=\dfrac{T_{max}}{g}$ (dây đỡ cả trọng lượng B)", "Chỉ đúng khi B đứng yên. B đang có gia tốc nên dây không chịu cả trọng lượng; cách này cho kết quả khác thực tế."),
           (r"Lấy $m_B=\dfrac{T_{max}}{a_{max}}$ (coi $T=m_Ba$)", r"$m_Ba$ là hợp lực lên B chứ không phải $T$; hợp lực lên B là $P_B-T$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ VÍ DỤ CŨ → tự luận ═════════════
# Ví dụ 1 (đèn treo, dây giới hạn 5,5 N): tính lại T = 0,5·9,8 = 4,9 N < 5,5 N → giữ (Dễ).
# Ví dụ 3 (áo treo giữa dây, hai nửa dây hợp 120°): T = mg/(2cos60°) = 4,9 N → giữ (Trung bình).
# Ví dụ 2, 4 (vật trên mặt phẳng nghiêng giữ bằng dây): phương dây so với mặt nghiêng chỉ có trong hình, và cần phân tích lực lên hai trục
# (lý thuyết bài 17 không dạy) → BỎ.
assert abs(0.5 * 9.8 - 4.9) < 1e-9 and 4.9 < 5.5
assert abs(0.5 * 9.8 / (2 * math.cos(math.radians(60))) - 4.9) < 1e-9

def _sach_alt(h):
    return re.sub(r'alt="[^"]*"', 'alt="Hình minh hoạ"', h)
OLD2 = [dict(o, body_html=_sach_alt(o["body_html"])) for o in OLD]
_x = "đang ở trạng thái cân bằng.</strong> <br />a)"
assert _x in OLD2[0]["body_html"]
OLD2[0]["body_html"] = OLD2[0]["body_html"].replace(_x, r"đang ở trạng thái cân bằng. Lấy $g=9,8\ \text{m/s}^2$.</strong> <br />a)", 1)
TU_LUAN = tu_luan_tu(OLD2, [0, 2], {0: "Dễ", 2: "Trung bình"})

def _sua_latex(h):
    """Sửa NHẸ lỗi chuỗi của ví dụ cũ (không đổi nội dung vật lí): thập phân thiếu {,}."""
    parts = h.replace("$$", "\x00").split("$")
    for i in range(1, len(parts), 2):
        parts[i] = re.sub(r"(?<=\d),(?=\d)", "{,}", parts[i])
        parts[i] = re.sub(r"(?<![\\a-z])cos", lambda m: "\\cos", parts[i]).replace("=>", "\\Rightarrow ")
        parts[i] = re.sub(r"(\d)N$", lambda m: m.group(1) + "\\ \\text{N}", parts[i])
    return "$".join(parts).replace("\x00", "$$")
TU_LUAN["body_html"] = _sua_latex(TU_LUAN["body_html"])

write(J, 62, "Bài 17. Trọng lực và lực căng", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J)); d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
