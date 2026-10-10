"""Hình cho bài tập mẫu Bài 12 "Hiện tượng cảm ứng điện từ" (Vật lí 12), lesson_id 13.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mọi chuyển động tính từ số liệu của đề (khung quay đều, B đổi đều, điểm chạy dọc đồ thị Φ–t), không vẽ dòng cảm ứng
và không ghi kết quả. Vectơ B/n: đầu mũi tên chữ V 30° (arrow() của svg_lib); đường sức nét đứt (field_line)."""
import math, os, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import field_line, chevron

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


# ───────────── tiện ích ─────────────
def rich(s, size=13):
    """`p_N` → p với chỉ số dưới N."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def rot(cx, cy, dphi, dur, inner):
    """Nhóm quay quanh (cx,cy) góc dphi độ (dương = cùng chiều kim đồng hồ trên màn hình), đều theo thời gian; chạy một lần khi bấm."""
    return (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};{dphi:.1f} {cx} {cy}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>')

def cross(x, y, op=None, anim=None, r=6, c=BLUE):
    """Dấu ⊗ (từ trường hướng VÀO mặt giấy). anim = (op_đầu, op_cuối, t_bắt_đầu, t_kết_thúc, dur): mờ dần / hiện dần theo keyTimes."""
    body = (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c}" stroke-width="1.8"/>'
            f'<path d="M{x - 3.6},{y - 3.6}l7.2,7.2m0,-7.2l-7.2,7.2" stroke="{c}" stroke-width="1.8" fill="none"/>')
    if anim is None:
        return body
    a0, a1, t0, t1, dur = anim
    return (f'<g opacity="{a0}">{body}<animate attributeName="opacity" values="{a0};{a0};{a1};{a1}" keyTimes="0;{t0:.2f};{t1:.2f};1" '
            f'dur="{dur}s" begin="indefinite" fill="freeze"/></g>')

def square_frame(x, y, w, h, c="currentColor", sw=2.6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{c}" stroke-width="{sw}"/>'

def bfield_h(x0, x1, ys, c=BLUE):
    return "".join(field_line(x0, y, x1, y, c, 1.5, "6 4", 11) for y in ys)


# ───────────── Khung nhìn ngang (dùng cho Dạng 1 và Dạng 4): đường sức nằm ngang, khung quay quanh trục ⟂ hình ─────────────
CX, CY = 200, 112
YS = (40, 80, 144, 184)          # đường sức tránh y = CY để nhãn góc không đè lên

def side(kk, tag, nturn, rx, ry, dphi, dur, cap0, cap2, alt0, alt2, data, unknown, offs=(0,), start0=0):
    """kk=0: khung quay từ vuông góc đường sức (pháp tuyến ∥ B) tới vị trí đề cho (mặt khung hợp với B góc 30°).
    kk=2: khung ở vị trí cuối, có cung 30° (đề cho) và α = ? (cần tìm)."""
    b = bfield_h(30, 392, YS) + txt(396, 22, "B", BLUE, 14, "end")
    ell = "".join(f'<ellipse cx="{CX + o}" cy="{CY}" rx="{rx}" ry="{ry}" fill="none" stroke="{ORG}" stroke-width="2.4"/>' for o in offs)
    nlen = 46
    narr0 = arrow("", "g", CX, CY, CX + nlen, CY, 2.4)                    # pháp tuyến ban đầu ∥ B
    a30 = math.radians(30)
    gx, gy = math.cos(a30) * (ry + 10), math.sin(a30) * (ry + 10)          # đầu mút đoạn "mặt khung" ở vị trí cuối
    ref = seg(CX, CY, CX + 78, CY, GREY, 1.3, "4 4")                       # đường sức tham chiếu qua tâm (nét xám)
    ang = arc(CX, CY, 62, 0, 30, RED, 1.9) + txt(CX + 66, CY - 9, "30°", RED, 13)
    if kk == 0:
        ghost = seg(CX - gx, CY + gy, CX + gx, CY - gy, GREY, 1.5, "5 4")
        b += ghost + ref + ang + rot(CX, CY, dphi + start0, dur, (f'<g transform="rotate({-start0} {CX} {CY})">{ell}{narr0}</g>' if start0 else ell + narr0)) + circ(CX, CY, 3, "currentColor", 1.5, "currentColor")
        b += txt(30, 22, data, "currentColor", 13) + txt(30, 214, "xanh lá: pháp tuyến n · chấm ở tâm: trục quay", "currentColor", 11, "start", "400")
        b += txt(CX + 118, CY + 56, unknown, ORG, 13)
        return fig(f"{tag}-0", "0 0 420 224", alt0, b, cap0)
    # kk == 2: vị trí cuối
    nx, ny = math.cos(math.radians(60)) * nlen, math.sin(math.radians(60)) * nlen
    fr = f'<g transform="rotate({dphi:.1f} {CX} {CY})">{ell}</g>'
    b += ref + ang + fr + arrow("", "g", CX, CY, CX + nx, CY + ny, 2.4) + circ(CX, CY, 3, "currentColor", 1.5, "currentColor")
    b += arc(CX, CY, 26, -60, 0, ORG, 1.9) + txt(CX + 32, CY + 22, "α = ?", ORG, 13)
    b += txt(CX + nx + 6, CY + ny + 14, "n", GRN, 14)
    b += txt(30, 22, data, "currentColor", 13) + txt(30, 214, "30°: góc của MẶT khung (đề cho) · α: góc của pháp tuyến", "currentColor", 11, "start", "400")
    b += txt(CX + 118, CY + 56, unknown, ORG, 13)
    return fig(f"{tag}-2", "0 0 420 224", alt2, b, cap2)


# ───────────── Dạng 1 · khung tròn r = 5,0 cm, B = 0,40 T, mặt khung hợp đường sức 30° ─────────────
def d1(kk):
    return side(kk, "d1", 1, 7, 44, 60, 4,
                "Mô phỏng: khung quay đều trong 4 s tới vị trí đề cho (nét đứt xám). Nhìn ngang, khung tròn hiện thành elip hẹp. " + NOTE,
                "Dữ kiện: khung ở vị trí đề cho; 30° là góc của mặt khung, α cần tìm là góc của pháp tuyến. " + NOTE,
                "Khung tròn quay trong từ trường đều tới vị trí mặt khung hợp với đường sức góc 30 độ",
                "Khung ở vị trí đề cho, góc 30 độ của mặt khung và góc alpha chưa biết giữa pháp tuyến và cảm ứng từ",
                "r = 5,0 cm · B = 0,40 T", "Φ = ?", start0=25)


# ───────────── Dạng 2 · vòng dây kín trong mặt giấy, B ⊗ tăng đều (không vẽ dòng cảm ứng) ─────────────
GX = (40, 92, 144, 196, 248)
GY = (30, 72, 114, 156, 198)
LC, LR = (144, 114), 66          # tâm, bán kính vòng dây

def d2(kk):
    anim = kk == 0
    b = ""
    k = 0
    for i, (y, x) in enumerate([(y, x) for y in GY for x in GX]):
        if anim and i % 3 != 0:                      # 9 dấu có sẵn; 16 dấu hiện dần (B tăng)
            t0 = 0.06 + 0.045 * k; k += 1
            b += cross(x, y, anim=(0, 1, t0, t0 + 0.2, 5))
        else:
            b += cross(x, y)
    b += circ(LC[0], LC[1], LR, "currentColor", 3.2)
    if anim:
        b += (f'<rect x="352" y="168" width="22" height="40" fill="{BLUE}" opacity=".8">{smil("height", [40, 130], 5)}{smil("y", [168, 78], 5)}</rect>')
    else:
        b += f'<rect x="352" y="168" width="22" height="40" fill="{BLUE}" opacity=".35"/>'
    b += seg(352, 208, 374, 208, "currentColor", 2) + txt(363, 224, "B", BLUE, 14, "middle")
    b += txt(292, 24, "⊗: B vào giấy", BLUE, 12, "start", "700")
    if kk == 0:
        return fig("d2-0", "0 0 420 232", "Vòng dây kín nằm trong mặt giấy, từ trường đều hướng vào giấy có độ lớn tăng dần, số dấu nhân tăng lên", b,
                   "Mô phỏng: B tăng đều trong 5 s (dấu ⊗ nhiều dần, cột xanh cao dần). Hình không vẽ dòng cảm ứng. " + NOTE)
    b += txt(292, 64, "Chiều quay: nhìn từ", "currentColor", 12, "start", "400") + txt(292, 80, "phía người đọc", "currentColor", 12, "start", "400")
    return fig("d2-2", "0 0 420 232", "Dữ kiện: vòng dây kín trong mặt giấy, từ trường đều vuông góc và hướng vào giấy, chiều quay theo người đọc", b,
               "Dữ kiện: vòng dây kín, B vuông góc mặt giấy hướng vào. Cột xanh: B lớn dần theo thời gian. " + NOTE)


# ───────────── Dạng 3 · khung vuông cạnh 6,0 cm, R = 0,30 Ω, B giảm đều 0,50 T → 0,20 T trong 15 ms ─────────────
G3X = (44, 92, 140, 188, 236)
G3Y = (36, 84, 132, 180)
FADE3 = {1, 2, 3, 5, 6, 8, 10, 11, 13, 14, 16, 18}

def d3(kk):
    anim = kk == 0
    b = ""
    idx = 0; k = 0
    for y in G3Y:
        for x in G3X:
            if anim and idx in FADE3:                # 12 dấu mờ dần (B giảm còn 40 %), 8 dấu còn lại
                t0 = 0.05 + 0.05 * k; k += 1
                b += cross(x, y, anim=(1, 0, t0, t0 + 0.2, 5))
            else:
                b += cross(x, y)
            idx += 1
    b += square_frame(80, 60, 96, 96)
    b += arrow("", "o", 80, 204, 176, 204, 1.8) + arrow("", "o", 176, 204, 80, 204, 1.8) + txt(128, 222, "a = 6,0 cm", ORG, 13, "middle")
    # cột đo B: 0,50 T cao 150 px, 0,20 T cao 60 px (300 px/T)
    b += f'<rect x="300" y="40" width="26" height="150" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" opacity=".6"/>'
    if anim:
        b += f'<rect x="300" y="40" width="26" height="150" fill="{BLUE}" opacity=".8">{smil("height", [150, 60], 5)}{smil("y", [40, 130], 5)}</rect>'
    else:
        b += f'<rect x="300" y="40" width="26" height="150" fill="{BLUE}" opacity=".35"/><rect x="300" y="130" width="26" height="60" fill="{BLUE}" opacity=".8"/>'
    b += seg(326, 40, 336, 40, "currentColor", 1.4) + txt(340, 44, "0,50 T", "currentColor", 12, "start", "700")
    b += seg(326, 130, 336, 130, "currentColor", 1.4) + txt(340, 134, "0,20 T", "currentColor", 12, "start", "700")
    b += seg(300, 190, 326, 190, "currentColor", 2) + txt(313, 208, "B", BLUE, 14, "middle")
    b += txt(30, 22, "R = 0,30 Ω · Δt = 15 ms", "currentColor", 13) + txt(410, 236, "e_c = ?   i = ?", ORG, 13, "end")
    if anim:
        return fig("d3-0", "0 0 420 240", "Khung dây vuông trong từ trường đều hướng vào giấy; cảm ứng từ giảm từ 0,50 xuống 0,20 tesla, các dấu nhân thưa dần", b,
                   "Mô phỏng: B giảm đều từ 0,50 T xuống 0,20 T, chạy 5 s thay cho 15 ms (dấu ⊗ thưa dần, cột xanh thấp dần). " + NOTE)
    return fig("d3-2", "0 0 420 240", "Dữ kiện: khung vuông cạnh 6,0 cm trong từ trường đều vuông góc mặt khung; cảm ứng từ giảm từ 0,50 xuống 0,20 tesla", b,
               "Dữ kiện: mặt khung vuông góc đường sức; cột xanh nhạt là B lúc đầu, cột đậm là B lúc sau. " + NOTE)


# ───────────── Dạng 4 · cuộn 100 vòng, B = 0,40 T, quay 0,050 s tới vị trí mặt cuộn dây hợp B 30° ─────────────
def d4(kk):
    return side(kk, "d4", 3, 5, 44, 60, 5,
                "Mô phỏng: cuộn dây quay đều trong 5 s thay cho 0,050 s (chậm 100 lần) từ vị trí mặt cuộn dây vuông góc đường sức tới vị trí đề cho (nét đứt xám). Cuộn dẹt 100 vòng vẽ thu gọn thành 3 vòng. " + NOTE,
                "Dữ kiện: cuộn dây ở vị trí cuối; 30° là góc của MẶT cuộn dây, α cần tìm là góc của pháp tuyến. Cuộn dẹt 100 vòng vẽ thu gọn. " + NOTE,
                "Cuộn dây dẹt quay trong từ trường đều tới vị trí mặt cuộn dây hợp với đường sức góc 30 độ",
                "Cuộn dây ở vị trí cuối, góc 30 độ của mặt cuộn dây và góc alpha chưa biết giữa pháp tuyến và cảm ứng từ",
                "N = 100 vòng · B = 0,40 T", "e_c = ?   i = ?", offs=(-5, 0, 5))


# ───────────── Dạng 5 · đồ thị Φ–t: 0→20 mWb (0–0,10 s), giữ (0,10–0,30 s), về 0 (0,30–0,35 s) ─────────────
def d5(kk):
    anim = kk == 0
    O = (56, 188); kx, ky = 800, 6.5           # 800 px/s ; 6,5 px/mWb
    X = lambda t: O[0] + kx * t
    Y = lambda f: O[1] - ky * f
    pts = [(X(0), Y(0)), (X(0.10), Y(20)), (X(0.30), Y(20)), (X(0.35), Y(0))]
    b = arrow("", "g", O[0], O[1], 400, O[1], 2) + arrow("", "g", O[0], O[1], O[0], 44, 2)
    b += txt(398, O[1] + 18, "t (s)", GRN, 12, "end") + txt(O[0] + 6, 44, "Φ (mWb)", GRN, 12, "start") + txt(O[0] - 8, O[1] + 14, "O", "currentColor", 13, "end")
    b += poly(pts, ORG, 2.8)
    b += seg(O[0], Y(20), X(0.10), Y(20), "currentColor", 1.2, "4 4", .6)
    for t, s in ((0.10, "0,10"), (0.30, "0,30"), (0.35, "0,35")):
        b += seg(X(t), Y(20) if t < 0.35 else O[1], X(t), O[1], "currentColor", 1.2, "4 4", .6) if t < 0.35 else ""
        b += seg(X(t), O[1] - 4, X(t), O[1] + 4, "currentColor", 1.6) + txt(X(t), O[1] + 18, s, "currentColor", 12, "middle", "400")
    b += seg(O[0] - 4, Y(20), O[0] + 4, Y(20), "currentColor", 1.6) + txt(O[0] - 8, Y(20) + 4, "20", "currentColor", 12, "end", "400")
    b += txt(X(0.05) - 4, Y(10) - 12, "(1)", ORG, 13, "end") + txt((X(0.10) + X(0.30)) / 2, Y(20) - 8, "(2)", ORG, 13, "middle") + txt(X(0.35) + 6, Y(10), "(3)", ORG, 13, "start")
    b += txt(160, 100, "R = 0,50 Ω", "currentColor", 13) + txt(160, 120, "B ⊗ vào giấy,", "currentColor", 12, "start", "400") + txt(160, 136, "n cùng chiều B", "currentColor", 12, "start", "400")
    if anim:
        ts = [0.01 * i for i in range(36)]
        f = lambda t: 200 * t if t <= 0.10 + 1e-9 else (20 if t <= 0.30 + 1e-9 else 20 - 400 * (t - 0.30))
        xs = [X(t) for t in ts]; ys = [Y(f(t)) for t in ts]
        b += (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
              f'{smil("cx", xs, 7)}{smil("cy", ys, 7)}</circle>')
        return fig("d5-0", "0 0 420 214", "Điểm biểu diễn từ thông chạy dọc đồ thị: tăng đều, giữ nguyên, rồi giảm đều về không", b,
                   "Mô phỏng: điểm chạy dọc đồ thị Φ–t trong 7 s thay cho 0,35 s (chậm 20 lần). Hình vẽ theo tỉ lệ. ")
    b += txt(160, 160, "i = ?", ORG, 13)
    return fig("d5-2", "0 0 420 214", "Dữ kiện: đồ thị từ thông theo thời gian gồm ba đoạn (1), (2), (3)", b,
               "Dữ kiện: đồ thị Φ–t của vòng dây, chia thành ba đoạn (1), (2), (3). Hình vẽ theo tỉ lệ. ")


BUILD = [d1, d2, d3, d4, d5]
