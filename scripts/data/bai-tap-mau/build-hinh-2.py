"""Bài tập mẫu Bài 1 "Sự chuyển thể" (Vật lí 12) — lesson_id 2. Quét 5 dạng: scripts/logs/batch-ra-soat/ket-qua/2.quet-dang.json
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-2.py   (idempotent)
Mọi chuyển động tính từ số liệu của đề (nhiệt kế/điểm chạy theo đúng bảng, hạt khí nảy đàn hồi); không để lộ đáp số."""
import json, math, os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

J = os.path.join(HERE, "2.json")
GREY = "#94a3b8"

# ───────────── tiện ích hình ─────────────
def fm(v, nd=2):
    s = f"{v:.{nd}f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"

def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{";".join(fm(x) for x in kt)}"' if kt else ""
    return (f'<animate attributeName="{attr}" values="{";".join(fm(v, 1) for v in vals)}"{k} dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')

def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, op=1, extra=""):
    return (f'<rect x="{fm(x)}" y="{fm(y)}" width="{fm(w)}" height="{fm(h)}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}" opacity="{op}"{">" if extra else "/>"}{extra + "</rect>" if extra else ""}')

def C(x, y, r, c="currentColor", fill="none", sw=2, extra="", op=1):
    return (f'<circle cx="{fm(x)}" cy="{fm(y)}" r="{fm(r)}" fill="{fill}" stroke="{c}" stroke-width="{sw}" opacity="{op}"'
            f'{">" + extra + "</circle>" if extra else "/>"}')

def hat(cx, cy, r, fill, offs, dur):
    """Hạt tròn chuyển động theo các độ dời `offs` (dx, dy) so với vị trí đầu; một <animateTransform> mỗi hạt."""
    v = ";".join(f"{fm(dx, 1)} {fm(dy, 1)}" for dx, dy in offs)
    return (f'<circle cx="{fm(cx, 1)}" cy="{fm(cy, 1)}" r="{r}" fill="{fill}" stroke="currentColor" stroke-width="1.4">'
            f'<animateTransform attributeName="transform" type="translate" values="{v}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></circle>')

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, s, c, size, anchor, weight)

def stopwatch(cx, cy, r, ang_total, dur):
    """Đồng hồ bấm giờ: kim quay đều từ 0 đến ang_total độ (1 phút = 24°, mặt đồng hồ 15 phút)."""
    hand = (f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r + 7}" stroke="{RED}" stroke-width="3" stroke-linecap="round">'
            f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};{fm(ang_total)} {cx} {cy}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></line>')
    ticks = "".join(seg(cx + (r - 1) * math.sin(math.radians(a)), cy - (r - 1) * math.cos(math.radians(a)),
                        cx + (r - 6) * math.sin(math.radians(a)), cy - (r - 6) * math.cos(math.radians(a)), "currentColor", 1.6)
                    for a in range(0, 360, 90))
    return C(cx, cy, r, "currentColor", "none", 2.4) + ticks + hand + dot(cx, cy, 3.5, "currentColor")

def thermo(x, ytop, ybot, Tmax, T0, vals, dur, kt=None, step=50, lab=100):
    """Nhiệt kế: cột thuỷ ngân cao theo T. vals = các nhiệt độ lấy mẫu (nội suy tuyến tính)."""
    Y = lambda T: ybot - T / Tmax * (ybot - ytop)
    b = R(x - 6, ytop - 4, 12, ybot - ytop + 8, "currentColor", 2.2, "none", 6)
    b += C(x, ybot + 12, 11, "currentColor", RED, 2.2)
    for T in range(0, Tmax + 1, step):
        big = T % lab == 0
        b += seg(x - 6 - (9 if big else 5), Y(T), x - 6, Y(T), "currentColor", 1.6 if big else 1.2)
        if big:
            b += txt(x - 20, Y(T) + 4, str(T), "currentColor", 12, "end", "400")
    ys = [Y(v) for v in vals]
    b += (f'<rect x="{x - 2.5}" y="{fm(Y(T0))}" width="5" height="{fm(ybot + 4 - Y(T0))}" fill="{RED}">'
          f'{anim("y", ys, dur, kt)}{anim("height", [ybot + 4 - y for y in ys], dur, kt)}</rect>')
    b += txt(x + 12, ytop + 6, "°C", "currentColor", 12, "start", "400")
    return b

def graph(pts, tmax, Tmax, tstep, Tgrid, Tlab, x0=54, y0=222, w=346, h=186, marks=(), dot_run=None, dur=0):
    """Đồ thị T–t vẽ từ các điểm gãy `pts`; `marks` = [(t, T, nhãn, dx, dy)]; dot_run: điểm chạy dọc đồ thị (một lần khi bấm)."""
    X = lambda t: x0 + t / tmax * w
    Y = lambda T: y0 - T / Tmax * h
    b = ""
    for t in range(0, tmax + 1, tstep):
        b += seg(X(t), y0, X(t), y0 - h, GREY, 1, "", .35) + txt(X(t), y0 + 17, str(t), "currentColor", 12, "middle", "400")
    for T in range(0, Tmax + 1, Tgrid):
        b += seg(x0, Y(T), x0 + w, Y(T), GREY, 1, "", .35)
        if T % Tlab == 0:
            b += txt(x0 - 7, Y(T) + 4, str(T), "currentColor", 12, "end", "400")
    b += seg(x0, y0, x0 + w + 10, y0, "currentColor", 2) + chevron(x0 + w + 10, y0, 1, 0, "currentColor", 2, 9)
    b += seg(x0, y0, x0, y0 - h - 10, "currentColor", 2) + chevron(x0, y0 - h - 10, 0, -1, "currentColor", 2, 9)
    b += txt(x0 + w + 10, y0 + 34, "t (phút)", "currentColor", 12, "end", "700") + txt(x0 + 6, y0 - h - 14, "T (°C)", "currentColor", 12, "start", "700")
    b += poly([(X(t), Y(T)) for t, T in pts], GRN, 2.8)
    for t, T, nm, dx, dy in marks:
        b += dot(X(t), Y(T), 4, "currentColor") + (txt(X(t) + dx, Y(T) + dy, nm, "currentColor", 13, "middle") if nm else "")
    if dot_run:
        ts = [p[0] for p in pts]; kt = [t / tmax for t in ts]
        b += (f'<circle cx="{fm(X(ts[0]))}" cy="{fm(Y(pts[0][1]))}" r="6.5" fill="{ORG}" stroke="currentColor" stroke-width="1.6">'
              f'{anim("cx", [X(t) for t in ts], dur, kt)}{anim("cy", [Y(T) for _, T in pts], dur, kt)}</circle>')
    return b


# ═════════════ HÌNH ═════════════
# ── Dạng 1: cốc nước đá, đĩa nước, giọt nước ngoài thành cốc ──
def d1(kk):
    p = f"d1{kk}"; run = kk == 0; DUR = 6
    wallx = lambda y: 50 + 8 * (y - 62) / 106
    b = defs(p) + ground(170, 16, 410)
    b += poly([(50, 62), (58, 168), (126, 168), (134, 62)], "currentColor", 2.4)
    # nước trong cốc: dâng nhẹ
    wy = (108, 103) if run else (103, 103); wh = (58, 63) if run else (63, 63)
    b += (f'<rect x="59" y="{wy[0]}" width="66" height="{wh[0]}" fill="{BLUE}" opacity=".28">'
          + (anim("y", wy, DUR) + anim("height", wh, DUR) if run else "") + '</rect>')
    # ba viên đá nhỏ dần (scale quanh tâm)
    for cx, cy, s in ((78, 100, 20), (98, 98, 22), (116, 101, 18)):
        cube = R(-s / 2, -s / 2, s, s, "currentColor", 2, "#e0f2fe", 2, .9)
        if run:
            b += f'<g transform="translate({cx},{cy})"><g><animateTransform attributeName="transform" type="scale" values="1;.35" dur="{DUR}s" begin="indefinite" fill="freeze"/>{cube}</g></g>'
        else:
            b += f'<g transform="translate({cx},{cy}) scale(.35)">{cube}</g>'
    # giọt nước bám ngoài thành cốc, xuất hiện dần
    drops = [(0, 92), (0, 118), (0, 144), (1, 100), (1, 130), (1, 152), (0, 104), (1, 116)]
    for k, (side, y) in enumerate(drops):
        x = wallx(y) - 4.5 if side == 0 else 134 - 8 * (y - 62) / 106 + 4.5
        s0 = .12 + .09 * k
        if run:
            b += C(x, y, 3.4, BLUE, BLUE, 1, f'<animate attributeName="r" values="0;0;3.4" keyTimes="0;{fm(s0)};1" dur="{DUR}s" begin="indefinite" fill="freeze"/>')
        else:
            b += C(x, y, 3.4, BLUE, BLUE, 1)
    # đĩa nước cạn bớt
    b += poly([(250, 168), (262, 154), (328, 154), (340, 168), (250, 168)], "currentColor", 2.4)
    dy = (158, 164) if run else (164, 164); dh = (10, 4) if run else (4, 4)
    b += (f'<rect x="262" y="{dy[0]}" width="66" height="{dh[0]}" fill="{BLUE}" opacity=".35">'
          + (anim("y", dy, DUR) + anim("height", dh, DUR) if run else "") + '</rect>')
    b += txt(92, 80, "(1)", ORG, 14, "middle") + txt(22, 124, "(2)", ORG, 14, "start") + txt(295, 138, "(3)", ORG, 14, "middle")
    b += txt(16, 24, "Phòng nóng ẩm", "currentColor", 13, "start", "400") + txt(16, 193, "Tên quá trình: (1) ?   (2) ?   (3) ?", "currentColor", 13, "start", "700")
    cap = ("Mô phỏng: 30 phút được rút gọn thành 6 giây. Đá nhỏ dần, giọt nước nhỏ bám ngoài thành cốc, nước ở đĩa cạn bớt." if run else
           "Dữ kiện: ba hiện tượng quan sát được sau 30 phút. Hình minh hoạ, không đúng tỉ lệ.")
    return fig(f"c2-1-{kk}", "0 0 420 204", "Cốc nước ngọt có đá và một đĩa nước cạn đặt trên bàn trong phòng nóng ẩm", b, cap)


# ── Dạng 2: ba chất, ba trạng thái hạt ──
def d2(kk):
    p = f"d2{kk}"; run = kk == 0
    rnd = random.Random(7)
    if run:
        DUR = 4; N = 16; b = defs(p)
        # (1) sáp: mạng 3x3 dao động tại chỗ
        b += R(26, 46, 88, 88, "currentColor", 2.4, "#fde68a", 3, .35)
        for i in range(3):
            for j in range(3):
                cx0, cy0 = 44 + i * 26, 64 + j * 26
                ph = rnd.uniform(0, 6.28); ph2 = rnd.uniform(0, 6.28)
                offs = [(2.6 * math.sin(2 * math.pi * 2 * u / N + ph), 2.6 * math.sin(2 * math.pi * 2 * u / N + ph2)) for u in range(N + 1)]
                b += hat(cx0, cy0, 6, GRN, offs, DUR)
        # (2) dầu: lớp lỏng trong ca, hạt trượt quanh vị trí luôn đổi
        b += poly([(156, 50), (156, 134), (264, 134), (264, 50)], "currentColor", 2.4)
        b += R(158, 86, 104, 46, ORG, 0, ORG, 0, .22)
        b += seg(158, 86, 262, 86, ORG, 1.4, "5 4", .8)
        for i in range(3):
            for j in range(3):
                cx0, cy0 = 176 + i * 33 + rnd.uniform(-4, 4), 98 + j * 15
                a1, a2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
                offs = [(11 * math.sin(2 * math.pi * 1.2 * u / N + a1), 3.5 * math.sin(2 * math.pi * 2 * u / N + a2)) for u in range(N + 1)]
                b += hat(cx0, cy0, 5.5, BLUE, offs, DUR)
        # (3) helium: 5 hạt nảy đàn hồi trong quả bóng (tính thật)
        bx, by, br = 350, 92, 42
        b += C(bx, by, br, "currentColor", "none", 2.4) + seg(bx, by + br, bx - 2, by + br + 10, "currentColor", 1.6)
        parts = []
        for k in range(5):
            ang = rnd.uniform(0, 6.28); rr = rnd.uniform(0, 26); sp = rnd.uniform(34, 52)
            parts.append([bx + rr * math.cos(ang), by + rr * math.sin(ang), sp * math.cos(ang + 2.0 * k), sp * math.sin(ang + 2.0 * k)])
        rp = 5.5; sub_n = 40; dt = DUR / N / sub_n * 6
        trace = [[(p0[0], p0[1])] for p0 in parts]
        for u in range(N):
            for _ in range(sub_n):
                for p0, tr in zip(parts, trace):
                    p0[0] += p0[2] * dt; p0[1] += p0[3] * dt
                    dx, dy = p0[0] - bx, p0[1] - by; dist = math.hypot(dx, dy)
                    if dist > br - rp - 1:
                        nx, ny = dx / dist, dy / dist; vn = p0[2] * nx + p0[3] * ny
                        if vn > 0:
                            p0[2] -= 2 * vn * nx; p0[3] -= 2 * vn * ny
                        p0[0] = bx + nx * (br - rp - 1); p0[1] = by + ny * (br - rp - 1)
            for p0, tr in zip(parts, trace):
                tr.append((p0[0], p0[1]))
        for tr in trace:
            b += hat(tr[0][0], tr[0][1], rp, RED, [(t[0] - tr[0][0], t[1] - tr[0][1]) for t in tr], DUR)
        b += txt(70, 158, "khối sáp", "currentColor", 13, "middle") + txt(70, 175, "0,30 L", ORG, 13, "middle")
        b += txt(210, 158, "dầu ăn trong ca", "currentColor", 13, "middle") + txt(210, 175, "0,30 L", ORG, 13, "middle")
        b += txt(350, 158, "khí helium", "currentColor", 13, "middle") + txt(350, 175, "0,30 L", ORG, 13, "middle")
        b += txt(16, 24, "Mỗi hạt tròn là một phân tử (phóng to rất nhiều).", "currentColor", 12, "start", "400")
        b += txt(16, 198, "Vào bình trống 1,5 L: V sáp = ?  V dầu = ?  V helium = ?", "currentColor", 13, "start", "700")
        return fig("c2-2-0", "0 0 420 210", "Ba chất ở trạng thái ban đầu: khối sáp, dầu trong ca, khí helium trong quả bóng", b,
                   "Mô phỏng: các phân tử của từng chất trong 4 giây (hạt khí nảy đàn hồi, hạt rắn dao động tại chỗ).")
    # k=2: ba bình trống 1,5 L cần điền
    b = defs(p)
    for i, nm in enumerate(("bình 1", "bình 2", "bình 3")):
        x = 28 + i * 132
        b += poly([(x, 38), (x, 138), (x + 96, 138), (x + 96, 38)], "currentColor", 2.4) + R(x - 4, 30, 104, 8, "currentColor", 2.4)
        b += txt(x + 48, 90, "V = ?", ORG, 14, "middle") + txt(x + 48, 160, nm + " · 1,5 L", "currentColor", 13, "middle")
    b += txt(16, 20, "Ba bình rỗng giống nhau, đậy kín", "currentColor", 12, "start", "400")
    return fig("c2-2-2", "0 0 420 176", "Ba bình thuỷ tinh rỗng dung tích 1,5 lít", b, "Dữ kiện: ba bình giống nhau, mỗi bình 1,5 lít, đậy kín. Hình minh hoạ.")


# ── Dạng 3: bảng nhiệt độ – thời gian của chất X (thiếc) ──
T3 = [52, 82, 112, 142, 172, 202, 232, 232, 232, 232, 232, 232, 257, 282, 307]   # t = 0..14 phút

def d3(kk):
    if kk == 0:
        p = "d30"; DUR = 11.2
        b = defs(p) + R(24, 184, 150, 10, ORG, 2, ORG, 0, .5)
        b += poly([(46, 92), (46, 180), (152, 180), (152, 92)], "currentColor", 2.4)
        kt = [0, 6 / 14, 11 / 14, 1]
        b += (f'<rect x="48" y="180" width="102" height="0" fill="{ORG}" opacity=".35">{anim("y", [180, 180, 134, 134], DUR, kt)}'
              f'{anim("height", [0, 0, 46, 46], DUR, kt)}</rect>')
        b += R(66, 140, 62, 40, "currentColor", 2.2, GREY, 3, .8, anim("opacity", [.8, .8, 0, 0], DUR, kt))
        b += txt(97, 165, "chất X", "currentColor", 13, "middle")
        b += txt(16, 24, "Đun đều mẫu chất X", "currentColor", 13, "start", "400")
        b += thermo(236, 36, 170, 350, T3[0], T3, DUR)
        b += stopwatch(338, 96, 40, 336, DUR) + txt(338, 156, "đồng hồ bấm giờ", "currentColor", 12, "middle", "400")
        b += txt(16, 218, "T nóng chảy = ?    thời gian nóng chảy = ?", "currentColor", 13, "start", "700")
        return fig("c2-3-0", "0 0 420 228", "Mẫu chất rắn X được đun đều trên bếp, có nhiệt kế và đồng hồ bấm giờ", b,
                   "Mô phỏng: 1 phút thật được rút gọn thành 0,8 giây (14 phút chạy trong 11,2 giây). Nhiệt kế chạy đúng theo bảng số liệu.")
    pts = [(t, T) for t, T in enumerate(T3)]
    b = defs("d32") + graph(pts, 14, 320, 2, 40, 40, marks=[(t, T, "", 0, 0) for t, T in pts])
    return fig("c2-3-2", "0 0 420 258", "Đồ thị nhiệt độ theo thời gian vẽ từ bảng số liệu của chất X", b,
               "Dữ kiện: mỗi chấm là một dòng của bảng. Nhiệt độ lặp lại ở các dòng liên tiếp thì các chấm nằm trên một đoạn ngang.")


# ── Dạng 4: đồ thị chất Y qua nhiều giai đoạn ──
P4 = [(0, 20), (2, 60), (7, 60), (12, 200), (20, 200), (22, 280)]   # A B C D E F

def d4(kk):
    names = dict(zip(range(6), "ABCDEF"))
    offs = [(12, 4), (-13, -9), (-3, 18), (-13, -8), (4, 20), (14, 4)]
    marks = [(t, T, names[i], offs[i][0], offs[i][1]) for i, (t, T) in enumerate(P4)]
    if kk == 0:
        b = defs("d40") + graph(P4, 22, 300, 2, 20, 40, y0=224, h=190, marks=marks, dot_run=True, dur=11)
        return fig("c2-4-0", "0 0 420 262", "Đồ thị nhiệt độ theo thời gian của chất X khi đun nóng đều", b,
                   "Mô phỏng: điểm cam chạy dọc đồ thị, 1 phút thật được rút gọn thành 0,5 giây (22 phút chạy trong 11 giây).")
    b = defs("d42") + graph(P4, 22, 300, 2, 20, 40, y0=224, h=190, marks=marks)
    return fig("c2-4-2", "0 0 420 262", "Đồ thị nhiệt độ theo thời gian với các điểm A, B, C, D, E, F", b,
               "Dữ kiện: sáu điểm gãy của đồ thị (lưới 20 °C × 2 phút). Hình vẽ theo số liệu của đề.")


# ── Dạng 5: rót chì lỏng vào khuôn, để nguội ──
def d5(kk):
    p = f"d5{kk}"; DUR = 3
    b = defs(p)
    b += R(20, 176, 160, 12, "currentColor", 2.4, GREY, 0, .5)
    b += poly([(40, 100), (52, 172), (148, 172), (160, 100)], "currentColor", 2.6)
    b += poly([(52, 118), (55, 170), (145, 170), (148, 118)], ORG, 0, 0) if False else ""
    b += f'<polygon points="53,118 55,170 145,170 147,118" fill="{ORG}" opacity=".45" stroke="none"/>'
    b += txt(100, 150, "chì lỏng", "currentColor", 13, "middle")
    b += txt(16, 24, "Khuôn đúc, để nguội trong phòng", "currentColor", 13, "start", "400")
    if kk == 0:
        T0, T1 = 397, 397 - 14 * 3
        b += thermo(236, 36, 160, 450, T0, [T0, T1], DUR)
        b += stopwatch(338, 90, 40, 72, DUR) + txt(338, 150, "đồng hồ bấm giờ", "currentColor", 12, "middle", "400")
        b += txt(16, 218, "T đông đặc = ?    bắt đầu đông đặc sau ? phút", "currentColor", 13, "start", "700")
        return fig("c2-5-0", "0 0 420 228", "Chì lỏng nóng đỏ trong khuôn đúc, nhiệt kế đo nhiệt độ", b,
                   "Mô phỏng 3 phút đầu, 1 phút thật là 1 giây: nhiệt kế giảm đều theo tốc độ nguội ghi trong đề. Phần sau của quá trình để em tự suy ra.")
    b += txt(205, 60, "Dữ kiện đã cho", ORG, 13, "start") + txt(205, 84, "rót ở 397 °C", "currentColor", 13, "start", "400")
    b += txt(205, 106, "nguội đều 14 °C mỗi phút (khi lỏng)", "currentColor", 13, "start", "400")
    b += txt(205, 128, "lúc đun: nóng chảy hết 4 phút", "currentColor", 13, "start", "400")
    b += txt(205, 150, "cùng tốc độ trao đổi nhiệt", "currentColor", 13, "start", "400")
    b += txt(205, 190, "cần tìm: nhiệt độ đông đặc và các mốc thời gian", RED, 13, "start")
    return fig("c2-5-2", "0 0 420 204", "Sơ đồ dữ kiện của bài làm nguội chì lỏng", b, "Dữ kiện của đề tóm tắt cạnh khuôn đúc. Hình minh hoạ.")


BUILD = [d1, d2, d3, d4, d5]


# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Gọi tên quá trình chuyển thể trong hiện tượng đời sống",
      topic="Nóng chảy, đông đặc, hoá hơi, ngưng tụ",
      problem_html=r"""<p>Một cốc nước ngọt có đá được đặt trên bàn trong phòng nóng ẩm, bên cạnh có một đĩa nông đựng ít nước. Sau $30$ phút, em quan sát được:</p><ol><li>Các viên đá trong cốc nhỏ đi, nước trong cốc nhiều lên.</li><li>Mặt ngoài thành cốc phủ một lớp giọt nước nhỏ.</li><li>Nước trong đĩa cạn bớt, nhưng nước không hề sủi bọt.</li></ol><ol type="a"><li>Gọi tên quá trình chuyển thể ở mỗi hiện tượng và nêu chiều chuyển thể.</li><li>Trong ba hiện tượng trên, có mấy hiện tượng mà chất toả nhiệt?</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Thể tích và hình dạng của chất rắn, lỏng, khí trong bình",
      topic="Cấu trúc chất rắn, lỏng, khí theo mô hình động học phân tử",
      problem_html=r"""<p>Ba chất ở nhiệt độ phòng, lúc đầu mỗi chất chiếm $0{,}30$ lít: một khối sáp nến đặc; $0{,}30$ lít dầu ăn đựng trong ca; $0{,}30$ lít khí helium chứa trong một quả bóng nhỏ. Cho từng chất vào ba bình thuỷ tinh rỗng giống nhau, mỗi bình có dung tích $1{,}5$ lít, rồi đậy kín. Khối sáp đặt nằm dưới đáy bình thứ nhất; dầu rót từ ca vào bình thứ hai; bình thứ ba đã hút hết không khí, rồi bơm toàn bộ khí helium vào. Nhiệt độ giữ không đổi, các chất không chuyển thể.</p><ol type="a"><li>Trong bình, mỗi chất chiếm thể tích bao nhiêu? Hình dạng của nó ra sao?</li><li>Dùng mô hình động học phân tử, giải thích kết quả của khí helium.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Đọc bảng nhiệt độ – thời gian của chất rắn kết tinh",
      topic="Nóng chảy, đông đặc, hoá hơi, ngưng tụ",
      problem_html=r"""<p>Đun nóng đều một mẫu chất rắn kết tinh $X$, ghi nhiệt độ sau mỗi phút:</p><div class="table-scroll"><table class="tl-table"><tbody><tr><th>$t$ (phút)</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th></tr><tr><td>$T$ (°C)</td><td>52</td><td>82</td><td>112</td><td>142</td><td>172</td><td>202</td><td>232</td><td>232</td></tr><tr><th>$t$ (phút)</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th><th>13</th><th>14</th><th></th></tr><tr><td>$T$ (°C)</td><td>232</td><td>232</td><td>232</td><td>232</td><td>257</td><td>282</td><td>307</td><td></td></tr></tbody></table></div><p>Bảng tra nhiệt độ nóng chảy: nước đá $0\ ^\circ\text{C}$ · thiếc $232\ ^\circ\text{C}$ · chì $327\ ^\circ\text{C}$ · nhôm $660\ ^\circ\text{C}$.</p><ol type="a"><li>Xác định nhiệt độ nóng chảy của $X$. $X$ là chất nào?</li><li>Chất nóng chảy trong bao lâu?</li><li>Ở phút thứ $9$, chất ở thể nào?</li><li>Sau khi đã nóng chảy hết, nhiệt độ tăng bao nhiêu độ mỗi phút?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Đọc đồ thị nhiệt độ – thời gian qua nhiều giai đoạn",
      topic="Nóng chảy, đông đặc, hoá hơi, ngưng tụ",
      problem_html=r"""<p>Một chất $X$ lúc đầu ở thể rắn, $20\ ^\circ\text{C}$, được đun nóng đều. Đồ thị nhiệt độ theo thời gian có các điểm $A, B, C, D, E, F$ như hình, trong đó $BC$ và $DE$ là hai đoạn nằm ngang.</p><ol type="a"><li>Xác định nhiệt độ nóng chảy và nhiệt độ sôi của $X$.</li><li>Ở phút thứ $16$, $X$ ở thể nào?</li><li>Quá trình sôi kéo dài bao lâu?</li><li>Ở đoạn $CD$, nhiệt độ tăng bao nhiêu độ mỗi phút?</li></ol>"""),
 dict(label="Dạng 5 · Nâng cao · Làm nguội kim loại đúc: dữ kiện ẩn về đông đặc",
      topic="Nóng chảy, đông đặc, hoá hơi, ngưng tụ",
      problem_html=r"""<p>Thợ đúc rót chì lỏng ở $397\ ^\circ\text{C}$ vào khuôn rồi để nguội trong phòng. Khi còn lỏng, chì nguội đều $14\ ^\circ\text{C}$ mỗi phút. Cũng thanh chì ấy, lúc đun thì nóng chảy hoàn toàn mất $4$ phút; coi tốc độ toả nhiệt khi nguội bằng đúng tốc độ nhận nhiệt lúc đun. Bảng tra nhiệt độ nóng chảy: nước đá $0\ ^\circ\text{C}$ · thiếc $232\ ^\circ\text{C}$ · chì $327\ ^\circ\text{C}$ · nhôm $660\ ^\circ\text{C}$.</p><ol type="a"><li>Chì đông đặc ở nhiệt độ nào?</li><li>Sau bao nhiêu phút kể từ lúc rót thì chì bắt đầu đông đặc?</li><li>Chì đông đặc hoàn toàn vào phút thứ mấy?</li><li>Ở phút thứ $7$, nhiệt độ chì là bao nhiêu?</li><li>Một mẫu thuỷ tinh nóng cũng nguội đều, nhiệt kế giảm đều, không lúc nào đứng yên. Mẫu thuỷ tinh thuộc loại chất rắn nào?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 [(r'"các viên đá nhỏ đi, nước nhiều lên"', r"Đá (nước rắn) mất dần; nước lỏng tăng", r"Gọi tên theo chiều chuyển thể: rắn → lỏng · lỏng → rắn · lỏng → khí · khí → lỏng"),
  (r'"mặt ngoài thành cốc phủ giọt nước nhỏ"', r"Giọt nước bám ngoài cốc lạnh", r"⚠ Thành cốc kín, nước không rỉ ra được ; xét xem giọt nước đến từ đâu"),
  (r'"nước trong đĩa cạn bớt, không sủi bọt"', r"Nước cạn ở nhiệt độ phòng, không có bọt hơi", r"⚠ Bay hơi: ở mặt thoáng, mọi nhiệt độ ; sôi: cả trong lòng, nhiệt độ xác định"),
  (r'"gọi tên quá trình chuyển thể … chiều chuyển thể"', r"Cần tên và chiều của (1), (2), (3)", r"Tên quá trình ghép với thể đầu và thể cuối"),
  (r'"mấy hiện tượng mà chất toả nhiệt"', r"Cần đếm", r"Phân loại từng quá trình: nhận nhiệt hay toả nhiệt")],
 [(r'"khối sáp nến đặc … đặt dưới đáy bình"', r"Chất rắn, $0{,}30$ lít", r"Rắn: hạt rất gần, trật tự, dao động tại chỗ"),
  (r'"dầu ăn … rót từ ca vào bình"', r"Chất lỏng, $0{,}30$ lít", r"Lỏng: hạt gần nhau, kém trật tự, vị trí cân bằng luôn đổi"),
  (r'"khí helium … bơm toàn bộ vào bình đã hút hết không khí"', r"Chất khí, $0{,}30$ lít ; bình $1{,}5$ lít", r"Khí: hạt rất xa, hỗn loạn"),
  (r'"nhiệt độ giữ không đổi, các chất không chuyển thể"', r"Không đổi thể", r"⚠ Chỉ khi không chuyển thể mới so sánh thể tích như vậy ; khí không có thể tích riêng"),
  (r'"mỗi chất chiếm thể tích bao nhiêu, hình dạng ra sao"', r"Cần $V$ và hình dạng", r"Thể tích riêng hay theo bình ; hình dạng riêng hay theo bình"),
  (r'"dùng mô hình động học phân tử giải thích"', r"Cần lí giải cho khí", r"Khoảng cách phân tử · lực liên kết · chuyển động hỗn loạn")],
 [(r'"chất rắn kết tinh $X$, đun nóng đều"', r"Kết tinh ; mỗi phút nhận nhiệt như nhau", r"⚠ Chất kết tinh có nhiệt độ nóng chảy xác định nên bảng có các dòng nhiệt độ không đổi"),
  (r'"ghi nhiệt độ sau mỗi phút"', r"$t=0$ đến $14$ phút ; một dòng mỗi phút", r"Nhiệt độ lặp lại liên tiếp: đoạn nằm ngang, đang chuyển thể"),
  (r'"bảng tra nhiệt độ nóng chảy"', r"Bốn chất và nhiệt độ nóng chảy", r"Đối chiếu số đo với bảng tra"),
  (r'"nhiệt độ nóng chảy của $X$ … chất nào"', r"Cần $T_{nc}$ và tên chất", r"Độ cao đoạn nằm ngang là nhiệt độ chuyển thể"),
  (r'"nóng chảy trong bao lâu"', r"Mốc đầu và mốc cuối của đoạn không đổi", r"$t_{nc}=t_{\text{cuối}}-t_{\text{đầu}}$ ; không đếm số dòng"),
  (r'"ở phút thứ $9$, chất ở thể nào"', r"$t=9$ phút", r"So $t$ với đoạn nóng chảy: đang chuyển thể thì hai thể cùng tồn tại"),
  (r'"sau khi nóng chảy hết, nhiệt độ tăng bao nhiêu độ mỗi phút"', r"Các dòng sau đoạn không đổi", r"$\dfrac{\Delta T}{\Delta t}$ ở đoạn dốc")],
 [(r'"lúc đầu ở thể rắn, $20\ ^\circ\text{C}$, đun nóng đều"', r"Điểm xuất phát $A$ ; mỗi phút nhận nhiệt như nhau", r"Thứ tự khi đun: rắn → nóng chảy → lỏng → sôi → hơi"),
  (r'"$BC$ và $DE$ là hai đoạn nằm ngang"', r"Hai đoạn nằm ngang, thấp và cao", r"⚠ Phân biệt hai đoạn bằng nhiệt độ và thứ tự, không bằng độ dài đoạn"),
  (r'"nhiệt độ nóng chảy và nhiệt độ sôi"', r"Cần hai nhiệt độ", r"Độ cao của đoạn nằm ngang"),
  (r'"ở phút thứ $16$, $X$ ở thể nào"', r"$t=16$ phút", r"Phút thuộc đoạn nằm ngang nào thì hai thể ở hai đầu cùng tồn tại"),
  (r'"quá trình sôi kéo dài bao lâu"', r"Hai mốc của đoạn $DE$", r"Độ dài đoạn ngang = thời gian chuyển thể"),
  (r'"ở đoạn $CD$, nhiệt độ tăng bao nhiêu độ mỗi phút"', r"Hai đầu đoạn dốc $C$, $D$", r"$\dfrac{\Delta T}{\Delta t}$ ở đoạn dốc")],
 [(r'"rót chì lỏng ở $397\ ^\circ\text{C}$ … để nguội"', r"Lỏng ở $397\ ^\circ\text{C}$ ; quá trình toả nhiệt", r"Làm nguội đi ngược chiều lúc đun: lỏng nguội → đông đặc → rắn nguội"),
  (r'"chì lỏng nguội đều $14\ ^\circ\text{C}$ mỗi phút"', r"Tốc độ nguội khi còn lỏng", r"⚠ Chỉ dùng tốc độ này khi chì còn lỏng ; lúc đang đông đặc nhiệt độ không đổi"),
  (r'"lúc đun thì nóng chảy hoàn toàn mất $4$ phút … tốc độ toả bằng tốc độ nhận"', r"Thời gian nóng chảy ; cùng tốc độ trao đổi nhiệt", r"Cùng tốc độ trao đổi nhiệt nên thời gian đông đặc bằng thời gian nóng chảy"),
  (r'"bảng tra nhiệt độ nóng chảy"', r"Bốn chất và nhiệt độ nóng chảy", r"Chất kết tinh đông đặc ở nhiệt độ nào?"),
  (r'"chì đông đặc ở nhiệt độ nào"', r"Đề không ghi nhiệt độ đông đặc (dữ kiện ẩn)", r"Dữ kiện ẩn nằm ở bảng tra"),
  (r'"sau bao nhiêu phút … bắt đầu đông đặc"', r"Từ $397$ xuống nhiệt độ đông đặc", r"Thời gian = độ giảm nhiệt độ chia tốc độ nguội"),
  (r'"đông đặc hoàn toàn vào phút thứ mấy"', r"Mốc bắt đầu và thời gian đông đặc", r"Mốc kết thúc = mốc bắt đầu + thời gian đông đặc"),
  (r'"thuỷ tinh … nhiệt kế giảm đều"', r"Không có đoạn nằm ngang", r"Chất kết tinh và chất vô định hình khác nhau ở đâu")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> chuyển thể là chất đổi từ thể này sang thể khác khi nhiệt độ (hoặc áp suất) đổi.",
      r"<strong>Bốn quá trình:</strong> nóng chảy (rắn → lỏng) · đông đặc (lỏng → rắn) · hoá hơi (lỏng → khí, gồm bay hơi và sôi) · ngưng tụ (khí → lỏng).",
      r"Bay hơi: ở mặt thoáng, mọi nhiệt độ · Sôi: cả trong lòng chất lỏng, nhiệt độ xác định.",
      r"Nóng chảy và hoá hơi nhận nhiệt ; đông đặc và ngưng tụ toả nhiệt.",
      r"⚠ <strong>Điều kiện:</strong> gọi tên theo thể đầu và thể cuối của chính chất đó ; giọt nước ngoài cốc là hơi nước của không khí, không phải nước rỉ ra từ trong cốc."]
R2 = [r"<strong>Khái niệm:</strong> khoảng cách giữa các hạt và lực liên kết quyết định thể tích và hình dạng của từng thể.",
      r"<strong>Rắn:</strong> hạt rất gần, trật tự, dao động quanh vị trí cố định → hình dạng và thể tích riêng.",
      r"<strong>Lỏng:</strong> hạt gần nhau, kém trật tự, vị trí cân bằng luôn đổi → thể tích xác định, hình dạng theo bình.",
      r"<strong>Khí:</strong> hạt rất xa, hỗn loạn → thể tích và hình dạng đều theo bình.",
      r"⚠ <strong>Điều kiện:</strong> nhiệt độ không đổi, các chất không chuyển thể ; khí không có “thể tích riêng”."]
R3 = [r"<strong>Khái niệm:</strong> chất rắn kết tinh có nhiệt độ nóng chảy xác định ; đang nóng chảy thì nhiệt độ không đổi dù vẫn nhận nhiệt.",
      r"<strong>Đọc bảng:</strong> các dòng nhiệt độ lặp lại liên tiếp là đoạn nằm ngang ; giá trị là nhiệt độ chuyển thể, mốc đầu và mốc cuối cho thời gian chuyển thể.",
      r"<strong>Công thức:</strong> $t_{nc}=t_{\text{cuối}}-t_{\text{đầu}}$ · tốc độ tăng nhiệt $=\dfrac{\Delta T}{\Delta t}$.",
      r"Nhiệt độ nóng chảy tra bảng để biết chất.",
      r"⚠ <strong>Điều kiện:</strong> đun đều (mỗi phút nhận nhiệt như nhau) ; thời gian là hiệu hai mốc, không đếm số dòng."]
R4 = [r"<strong>Khái niệm:</strong> đun đều nên mỗi phút nhận nhiệt như nhau ; đoạn nằm ngang là đang chuyển thể, đoạn dốc là đang nóng lên.",
      r"<strong>Thứ tự khi đun:</strong> rắn → nóng chảy (đoạn ngang thấp) → lỏng → sôi (đoạn ngang cao) → hơi.",
      r"Độ cao đoạn nằm ngang là nhiệt độ chuyển thể ; độ dài là thời gian chuyển thể.",
      r"Tốc độ tăng nhiệt $=\dfrac{\Delta T}{\Delta t}$ ở đoạn dốc.",
      r"⚠ <strong>Điều kiện:</strong> không phân biệt hai đoạn nằm ngang bằng độ dài ; nhiệt độ thấp hơn là nóng chảy, cao hơn là sôi."]
R5 = [r"<strong>Khái niệm:</strong> đông đặc ngược với nóng chảy ; chất kết tinh đông đặc đúng ở nhiệt độ nóng chảy.",
      r"<strong>Khi nguội:</strong> lỏng nguội dần → đông đặc (nhiệt độ không đổi) → rắn nguội tiếp.",
      r"Cùng tốc độ trao đổi nhiệt thì thời gian đông đặc bằng thời gian nóng chảy.",
      r"Thời gian nguội $=\dfrac{\text{độ giảm nhiệt độ}}{\text{tốc độ nguội}}$.",
      r"⚠ <strong>Điều kiện:</strong> tốc độ nguội $14\ ^\circ\text{C/phút}$ chỉ đúng khi chì còn lỏng ; chất vô định hình không có đoạn nằm ngang."]

SOLS = [
 sol(R1, [
  ("Viên đá nhỏ đi", [P("Thể đầu là nước đá (rắn), thể cuối là nước trong cốc (lỏng)."), A("T:Nóng chảy (rắn → lỏng), chất nhận nhiệt"),
     P("Không phải thăng hoa: đá không biến thành hơi mà thành nước lỏng ngay trong cốc.")]),
  ("Giọt nước ngoài thành cốc", [P("Thành cốc lạnh vì có đá bên trong. Hơi nước trong không khí nóng ẩm gặp mặt lạnh thì chuyển thành giọt nước."),
     A("T:Ngưng tụ (khí → lỏng), chất toả nhiệt"), P("Nước không rỉ qua thành cốc kín, nên đây không phải nước từ trong cốc thấm ra.")]),
  ("Nước trong đĩa cạn bớt", [P("Thể đầu là nước (lỏng), thể cuối là hơi nước (khí). Nước không sủi bọt và vẫn ở nhiệt độ phòng, thấp hơn nhiệt độ sôi."),
     A("T:Bay hơi (một dạng hoá hơi, lỏng → khí), chất nhận nhiệt"), P("Sôi cần bọt hơi hình thành ngay trong lòng chất lỏng ở nhiệt độ sôi.")]),
  ("Đếm quá trình toả nhiệt", [P("Nhận nhiệt: nóng chảy (1), bay hơi (3). Toả nhiệt: ngưng tụ (2)."), M(r"N_{\text{toả}}=1"), A(r"N_{\text{toả}}=1\ \text{hiện tượng}")]),
  ("Kiểm tra", [P("Có 2 quá trình nhận nhiệt (nóng chảy, bay hơi) và 1 quá trình toả nhiệt (ngưng tụ), tổng 3 hiện tượng ✓."),
     P("Cảm giác mát ở cốc là do đá và nước bay hơi lấy nhiệt từ xung quanh, tức là nhận nhiệt chứ không phải toả nhiệt.")])],
  [r"a) (1) nóng chảy (rắn → lỏng) · (2) ngưng tụ (khí → lỏng) · (3) bay hơi (lỏng → khí)", r"b) $1$ hiện tượng toả nhiệt (ngưng tụ)"],
  r"Nhận dạng: đề kể <strong>hiện tượng đời sống</strong> → xác định thể đầu và thể cuối rồi gọi tên ; <strong>không sủi bọt</strong> thì là bay hơi, không phải sôi."),
 sol(R2, [
  ("Khối sáp", [P("Chất rắn có hình dạng và thể tích riêng. Đặt xuống đáy bình, khối sáp không đổi:"), M(r"V_{\text{sáp}}=0{,}30\ \text{lít}"),
     A(r"V_{\text{sáp}}=0{,}30\ \text{lít}"), P("Hình dạng: giữ nguyên hình khối, không theo hình bình.")]),
  ("Dầu ăn", [P("Chất lỏng có thể tích xác định nhưng hình dạng theo bình: dầu trải thành lớp ở đáy, mặt thoáng nằm ngang."),
     M(r"V_{\text{dầu}}=0{,}30\ \text{lít}"), A(r"V_{\text{dầu}}=0{,}30\ \text{lít}")]),
  ("Khí helium", [P("Phân tử khí ở rất xa nhau và chuyển động hỗn loạn nên khí dàn ra chiếm toàn bộ bình:"), M(r"V_{\text{He}}=V_{\text{bình}}"),
     A(r"V_{\text{He}}=1{,}5\ \text{lít}"), P("Hình dạng: đúng hình của bình.")]),
  ("Giải thích bằng mô hình phân tử", [P("Khoảng cách giữa các phân tử khí rất lớn, lực liên kết yếu, phân tử chuyển động hỗn loạn nên bay khắp bình."),
     P("Phân tử không to ra, chỉ xa nhau hơn so với lúc ở trong quả bóng."), A("T:Khí không có thể tích riêng: luôn chiếm hết bình chứa")]),
  ("Kiểm tra", [P("Bơm thêm khí vào bình $20$ lít đã chứa $20$ lít oxygen thì thể tích vẫn $20$ lít, chỉ có áp suất tăng ✓."),
     P(r"Sáp và dầu chỉ chiếm $0{,}30$ lít, nhỏ hơn dung tích bình $1{,}5$ lít nên hoàn toàn nằm gọn trong bình.")])],
  [r"a) Sáp $0{,}30$ lít, giữ hình khối · dầu $0{,}30$ lít, hình theo đáy bình · helium $1{,}5$ lít, hình của bình", r"b) Khí không có thể tích riêng: phân tử ở rất xa nhau, chuyển động hỗn loạn nên chiếm hết bình"],
  r"Nhận dạng: đề <strong>cho chất vào bình rỗng</strong> → rắn, lỏng giữ thể tích riêng ; khí chiếm hết bình."),
 sol(R3, [
  ("Nhiệt độ nóng chảy", [P("Nhiệt độ đứng yên ở cùng một giá trị từ phút $6$ đến phút $11$ — đó là đoạn nằm ngang:"), M(r"T=232\ ^\circ\text{C}\quad(t=6\to11)"), A(r"T_{nc}=232\ ^\circ\text{C}")]),
  ("Tra bảng", [P(r"Đối chiếu bảng: $232\ ^\circ\text{C}$ là nhiệt độ nóng chảy của thiếc ; chì $327\ ^\circ\text{C}$, nhôm $660\ ^\circ\text{C}$, nước đá $0\ ^\circ\text{C}$ đều khác."), A("T:X là thiếc")]),
  ("Thời gian nóng chảy", [P("Đếm khoảng giữa hai mốc, không đếm số dòng (có $6$ dòng nhưng chỉ có $5$ khoảng một phút):"), M(r"t_{nc}=t_{\text{cuối}}-t_{\text{đầu}}=11-6"), A(r"t_{nc}=5\ \text{phút}")]),
  ("Thể ở phút thứ 9", [P("Phút $9$ nằm trong đoạn nóng chảy (từ phút $6$ đến phút $11$): chất đang chảy, chưa chảy hết."), A("T:Rắn và lỏng cùng tồn tại")]),
  ("Tốc độ tăng nhiệt sau khi chảy hết", [P("Lấy hai mốc sau phút $11$, ví dụ phút $11$ và phút $14$:"), M(r"\dfrac{\Delta T}{\Delta t}=\dfrac{T_{14}-T_{11}}{14-11}"), M(r"\dfrac{307-232}{3}"), A(r"25\ ^\circ\text{C/phút}")]),
  ("Kiểm tra", [P(r"Mỗi phút ở thể lỏng nhiệt độ tăng đều: $232\to257\to282\to307$ ✓."),
     P(r"Lúc còn rắn, nhiệt độ tăng $30\ ^\circ\text{C}$ mỗi phút: thể rắn và thể lỏng tăng nhiệt độ với tốc độ khác nhau (số liệu của đề)."),
     P("Cả bảng chỉ có một đoạn nằm ngang, tức một lần chuyển thể (nóng chảy).")])],
  [r"a) $T_{nc}=232\ ^\circ\text{C}$, chất $X$ là thiếc", r"b) $5$ phút", r"c) rắn và lỏng cùng tồn tại", r"d) $25\ ^\circ\text{C}$ mỗi phút"],
  r"Nhận dạng: đề cho <strong>bảng nhiệt độ theo thời gian</strong> → tìm các dòng nhiệt độ không đổi: đó là nhiệt độ nóng chảy ; thời gian là hiệu hai mốc."),
 sol(R4, [
  ("Nhiệt độ nóng chảy", [P("Đoạn nằm ngang thấp $BC$ (từ phút $2$ đến phút $7$) ứng với nóng chảy:"), A(r"T_{nc}=60\ ^\circ\text{C}")]),
  ("Nhiệt độ sôi", [P("Đun nóng thì nóng chảy trước, sôi sau nên đoạn nằm ngang cao $DE$ ứng với sôi, dù nó dài hơn đoạn $BC$:"), A(r"T_s=200\ ^\circ\text{C}")]),
  ("Thể ở phút thứ 16", [P("Phút $16$ thuộc đoạn $DE$ (từ phút $12$ đến phút $20$): chất đang sôi, chưa sôi hết."), A("T:Lỏng và hơi cùng tồn tại")]),
  ("Thời gian sôi", [P("Hai mốc của đoạn $DE$ là phút $12$ và phút $20$:"), M(r"t_s=20-12"), A(r"t_s=8\ \text{phút}")]),
  ("Tốc độ tăng nhiệt ở đoạn CD", [P(r"Đoạn $CD$ từ $(7;\,60)$ đến $(12;\,200)$:"), M(r"\dfrac{\Delta T}{\Delta t}=\dfrac{T_D-T_C}{t_D-t_C}"), M(r"\dfrac{200-60}{12-7}"), A(r"28\ ^\circ\text{C/phút}")]),
  ("Kiểm tra", [P(r"Đoạn $AB$: $\dfrac{60-20}{2}=20\ ^\circ\text{C}$ mỗi phút ; đoạn $EF$: $\dfrac{280-200}{2}=40\ ^\circ\text{C}$ mỗi phút."),
     P("Ba đoạn dốc có độ dốc khác nhau: rắn, lỏng, hơi nóng lên với tốc độ khác nhau, hợp với đồ thị."),
     P("Đồ thị có hai đoạn nằm ngang nên có hai lần chuyển thể (nóng chảy rồi sôi).")])],
  [r"a) $T_{nc}=60\ ^\circ\text{C}$ · $T_s=200\ ^\circ\text{C}$", r"b) lỏng và hơi cùng tồn tại", r"c) $8$ phút", r"d) $28\ ^\circ\text{C}$ mỗi phút"],
  r"Nhận dạng: đồ thị có <strong>hai đoạn nằm ngang</strong> → đoạn thấp là nóng chảy, đoạn cao là sôi ; đoạn dốc là đang nóng lên."),
 sol(R5, [
  ("Nhiệt độ đông đặc (dữ kiện ẩn)", [P("Đề không ghi nhiệt độ đông đặc. Chì là chất kết tinh nên đông đặc đúng ở nhiệt độ nóng chảy, tra bảng:"), A(r"T_{đđ}=T_{nc}=327\ ^\circ\text{C}")]),
  ("Mốc bắt đầu đông đặc", [P(r"Chì lỏng nguội từ $397\ ^\circ\text{C}$ xuống $327\ ^\circ\text{C}$ với tốc độ không đổi:"), M(r"t_1=\dfrac{397-327}{14}"), A(r"t_1=5\ \text{phút}")]),
  ("Mốc đông đặc hoàn toàn", [P("Cùng tốc độ trao đổi nhiệt nên thời gian đông đặc bằng thời gian nóng chảy, $4$ phút:"), M(r"t_2=t_1+4=5+4"), A(r"t_2=9\ \text{phút}")]),
  ("Nhiệt độ ở phút thứ 7", [P("Phút $7$ nằm giữa phút $5$ và phút $9$: chì đang đông đặc, vừa lỏng vừa rắn, nhiệt độ không đổi:"), A(r"T=327\ ^\circ\text{C}")]),
  ("Mẫu thuỷ tinh", [P("Nhiệt kế giảm đều, không có lúc nào đứng yên: không có đoạn nằm ngang, tức không có nhiệt độ đông đặc xác định."), A("T:Thuỷ tinh là chất rắn vô định hình")]),
  ("Kiểm tra", [P(r"Nếu tính nhầm $397-14\cdot7=299\ ^\circ\text{C}$ thì thấp hơn nhiệt độ đông đặc: vô lí, vì lúc ấy chì còn đang đông đặc, chưa nguội sâu hơn."),
     P(r"Đồ thị làm nguội của chì có một đoạn nằm ngang duy nhất từ phút $5$ đến phút $9$ ở $327\ ^\circ\text{C}$."),
     P(r"Chiều ngược: lúc đun, chì cũng nóng chảy ở $327\ ^\circ\text{C}$ trong $4$ phút ✓.")])],
  [r"a) $327\ ^\circ\text{C}$", r"b) $5$ phút", r"c) phút thứ $9$", r"d) $327\ ^\circ\text{C}$ (vừa lỏng vừa rắn)", r"e) chất rắn vô định hình"],
  r"Nhận dạng: đề <strong>làm nguội</strong> và không ghi nhiệt độ đông đặc → nhiệt độ đông đặc bằng nhiệt độ nóng chảy ; cùng tốc độ trao đổi nhiệt thì cùng thời gian."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>hiện tượng đời sống</b> → xác định <b>thể đầu → thể cuối</b> rồi gọi tên ; <b>không sủi bọt</b> thì là bay hơi.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Viên đá nhỏ đi", "Viên đá nhỏ đi và nước trong cốc nhiều lên là quá trình nào?",
       loi=r"Chỉ nói “đá tan” mà không gọi đúng tên quá trình, hoặc nhầm chiều với đông đặc vì cốc đang lạnh.",
       lua_chon=[("Nóng chảy", True),
                 ("Thăng hoa", "Thăng hoa là rắn → hơi ; ở đây đá thành nước lỏng ngay trong cốc."),
                 ("Đông đặc", "Đông đặc là lỏng → rắn, ngược với hiện tượng : đá đang tan chứ không đóng thêm.")]),
  buoc("Giọt nước ngoài thành cốc", "Giọt nước bám ngoài thành cốc hình thành bằng quá trình nào?",
       loi=r"Cho rằng nước rỉ từ trong cốc ra ngoài qua thành cốc, nên không gọi tên được quá trình.",
       lua_chon=[("Ngưng tụ", True),
                 ("Nước thấm từ trong cốc ra, không có chuyển thể", "Thành cốc kín không cho nước thấm ; giọt nước là hơi nước của không khí gặp mặt lạnh."),
                 ("Bay hơi", "Bay hơi là lỏng → khí, còn ở đây hơi nước biến thành giọt nước lỏng : chiều ngược lại.")],
       ke=[("Xét giọt nước đến từ hơi nước trong không khí hay từ nước trong cốc", True),
           ("Coi giọt nước là nước rỉ ra vì trong cốc có nước", "Cốc nguyên vẹn không rỉ nước ; đề không nói cốc nứt."),
           ("Bỏ qua vì giọt nước nhỏ, không đáng kể", "Đề hỏi cả ba hiện tượng ; giọt nước vẫn là một lần chuyển thể cần gọi tên.")]),
  buoc("Nước trong đĩa cạn bớt", "Nước trong đĩa cạn bớt bằng quá trình nào?",
       loi=r"Nghĩ rằng nước muốn mất đi thì phải sôi, nên gọi nhầm là sôi dù không có bọt.",
       lua_chon=[("Bay hơi", True),
                 ("Sôi", "Sôi chỉ xảy ra ở nhiệt độ sôi và có bọt hơi trong lòng chất lỏng ; đề nói nước không sủi bọt."),
                 ("Ngưng tụ", "Ngưng tụ làm lượng nước tăng, trái với nước cạn bớt.")],
       ke=[("Dựa vào chi tiết “không sủi bọt” để chọn giữa bay hơi và sôi", True),
           ("Coi “cạn bớt” nghĩa là nước đã sôi", "Nước ở nhiệt độ phòng, thấp hơn nhiệt độ sôi ; bay hơi xảy ra ở mọi nhiệt độ."),
           ("Chỉ xét thể cuối là hơi, bỏ qua thể đầu", "Phải xét cả thể đầu lẫn thể cuối mới biết chiều chuyển thể.")]),
  buoc("Đếm quá trình toả nhiệt", "Có mấy hiện tượng mà chất toả nhiệt?", 1, "hiện tượng", 0,
       loi=r"Đếm 2 hoặc 3 vì nghĩ “cốc lạnh nên quá trình nào cũng toả nhiệt”, hoặc quên rằng bay hơi phải nhận nhiệt.",
       ke=[("Phân loại từng quá trình đã gọi tên thành nhận nhiệt hay toả nhiệt rồi đếm", True),
           ("Tính hiện tượng làm cốc mát là toả nhiệt", "Đá tan làm nước lạnh vì đá nhận nhiệt của nước, không phải toả nhiệt."),
           ("Coi mọi quá trình “mất đi” như tan, bay hơi đều toả nhiệt", "Cảm giác mát là do chất lấy nhiệt từ xung quanh, tức nhận nhiệt.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>chất cho vào bình rỗng</b> → rắn, lỏng giữ <b>thể tích riêng</b> ; khí <b>chiếm hết bình</b>.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Khối sáp", "Khối sáp chiếm thể tích bao nhiêu lít trong bình?", 0.30, "lít", 0.01,
       loi=r"Cho rằng sáp dàn ra chiếm cả bình như khí, hoặc nghĩ thể tích đổi vì bình rộng hơn."),
  buoc("Dầu ăn", "Dầu ăn chiếm thể tích bao nhiêu lít trong bình?", 0.30, "lít", 0.01,
       loi=r"Cho rằng dầu “chảy” nên dàn ra chiếm hết bình ; thực ra chỉ hình dạng đổi, thể tích vẫn như cũ.",
       ke=[("Chất lỏng có thể tích xác định, chỉ đổi hình dạng theo bình", True),
           ("Chất lỏng chảy được nên dàn ra chiếm hết bình", "Lỏng chảy được vì vị trí cân bằng của hạt đổi, nhưng khoảng cách giữa các hạt vẫn gần như chất rắn nên thể tích không đổi."),
           ("Dầu giữ nguyên hình dạng như trong ca", "Hình dạng của lỏng theo bình chứa, không giữ hình ca cũ.")]),
  buoc("Khí helium", "Khí helium chiếm thể tích bao nhiêu lít trong bình?", 1.5, "lít", 0.05,
       loi=r"Lấy thể tích khí bằng lúc ở trong quả bóng vì lượng khí không đổi ; thực ra khí chiếm toàn bộ bình.",
       ke=[("Khí không có thể tích riêng, dàn ra khắp bình", True),
           ("Thể tích khí vẫn như lúc đầu vì lượng khí không đổi", "Lượng khí không đổi nhưng thể tích khí là phần không gian nó chiếm ; khí dàn ra khắp bình."),
           ("Khí chỉ chiếm phần phía trên của bình", "Phân tử khí chuyển động hỗn loạn bay khắp bình, không dồn về một phía.")]),
  buoc("Giải thích bằng mô hình phân tử", "Mô hình phân tử giải thích thể tích khí như vậy thế nào?",
       loi=r"Cho rằng phân tử khí to ra khi bơm vào bình ; thực ra phân tử không đổi, chỉ khoảng cách giữa chúng đổi.",
       lua_chon=[("Phân tử ở rất xa nhau, lực liên kết yếu, chuyển động hỗn loạn nên bay khắp bình", True),
                 ("Phân tử khí nở to ra khi bơm vào bình", "Phân tử không đổi kích thước ; chỉ khoảng cách giữa các phân tử thay đổi."),
                 ("Khí bị nén lại nên chiếm thể tích rất nhỏ", "Bình rỗng và lớn, khí không bị nén mà dàn ra chiếm hết bình.")],
       ke=[("Dùng khoảng cách phân tử và chuyển động hỗn loạn để giải thích", True),
           ("Dùng khối lượng riêng của khí so với dầu", "Khối lượng riêng không giải thích được vì sao khí chiếm hết bình."),
           ("Nói khí nhẹ nên bay lên khắp bình", "Khí chiếm hết bình do chuyển động hỗn loạn của phân tử chứ không phải do nhẹ.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>bảng nhiệt độ theo thời gian</b> → tìm các <b>dòng nhiệt độ không đổi</b> : nhiệt độ và thời gian nóng chảy.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhiệt độ nóng chảy", "Nhiệt độ nóng chảy của $X$ bằng bao nhiêu độ C?", 232, "°C", 1,
       loi=r"Chọn giá trị cuối bảng hoặc giá trị đầu bảng vì tưởng nhiệt độ nóng chảy là số lớn nhất hay số xuất phát."),
  buoc("Tra bảng", "Đối chiếu với bảng tra, $X$ là chất nào?",
       loi=r"Chọn chất theo độ lớn hoặc theo số cuối bảng thay vì đối chiếu đúng nhiệt độ nóng chảy.",
       lua_chon=[("Thiếc", True),
                 ("Chì", "Chì nóng chảy ở nhiệt độ cao hơn nhiệt độ đo được ; hai số phải khớp nhau."),
                 ("Nhôm", "Nhôm nóng chảy ở nhiệt độ cao hơn nhiều so với nhiệt độ đo được.")],
       ke=[("Đối chiếu nhiệt độ nóng chảy vừa tìm với bảng tra", True),
           ("Chọn chất có nhiệt độ nóng chảy lớn nhất trong bảng", "Phải khớp với số đo được, không chọn theo độ lớn."),
           ("Chọn theo nhiệt độ cuối bảng số liệu", "Nhiệt độ cuối bảng là lúc ngừng ghi, không phải nhiệt độ nóng chảy.")]),
  buoc("Thời gian nóng chảy", "Chất nóng chảy trong bao nhiêu phút?", 5, "phút", 0.1,
       loi=r"Đếm số dòng nhiệt độ không đổi thay vì lấy hiệu hai mốc, nên ra 6 phút.",
       ke=[("Lấy mốc cuối trừ mốc đầu của đoạn nhiệt độ không đổi", True),
           ("Đếm số dòng có nhiệt độ không đổi", "Số dòng luôn nhiều hơn số khoảng một phút giữa chúng một đơn vị, nên đếm dòng cho kết quả lớn hơn thực tế."),
           ("Lấy toàn bộ thời gian ghi bảng", "Bảng ghi cả giai đoạn còn rắn và đã lỏng ; chỉ đoạn nhiệt độ không đổi là nóng chảy.")]),
  buoc("Thể ở phút thứ 9", "Ở phút thứ $9$, chất ở thể nào?",
       loi=r"Cho rằng nhiệt độ đã bằng nhiệt độ nóng chảy thì chất đã lỏng hết ; thực ra phải hết đoạn nằm ngang mới chảy xong.",
       lua_chon=[("Rắn và lỏng cùng tồn tại", True),
                 ("Hoàn toàn rắn", "Phút 9 nằm trong đoạn nóng chảy : một phần chất đã chảy."),
                 ("Hoàn toàn lỏng", "Chất chưa chảy hết vì còn nằm trong đoạn nhiệt độ không đổi.")],
       ke=[("So thời điểm đã cho với khoảng nóng chảy vừa tìm", True),
           ("Chỉ nhìn nhiệt độ ở phút 9 rồi kết luận", "Nhiệt độ bằng nhiệt độ nóng chảy chưa đủ ; phải biết thời điểm nằm trong hay ngoài đoạn nóng chảy."),
           ("Tính số phút từ lúc bắt đầu đun", "Số phút từ lúc đun không cho biết thể ; cần so với đoạn nóng chảy.")]),
  buoc("Tốc độ tăng nhiệt sau khi chảy hết", "Sau khi chảy hết, nhiệt độ tăng bao nhiêu độ C mỗi phút?", 25, "°C/phút", 0.5,
       loi=r"Lấy 232 → 307 chia cho tổng 14 phút, hoặc dùng 30 °C/phút của đoạn còn rắn.",
       ke=[("Chọn hai mốc sau khi chảy hết, lấy độ tăng chia thời gian", True),
           ("Lấy hiệu hai đầu bảng chia tổng thời gian", "Cách này lẫn cả đoạn rắn và đoạn đang nóng chảy, không phải đoạn lỏng."),
           ("Dùng luôn tốc độ tăng nhiệt lúc còn rắn", "Hai giai đoạn tăng nhiệt với tốc độ khác nhau ; phải đọc riêng đoạn sau.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>hai đoạn nằm ngang</b> → đoạn thấp là <b>nóng chảy</b>, đoạn cao là <b>sôi</b> ; đoạn dốc là đang nóng lên.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Nhiệt độ nóng chảy", "Nhiệt độ nóng chảy của $X$ bằng bao nhiêu độ C?", 60, "°C", 1,
       loi=r"Chọn điểm xuất phát (20) hoặc điểm cuối đồ thị (280) thay vì độ cao đoạn nằm ngang thấp."),
  buoc("Nhiệt độ sôi", "Nhiệt độ sôi của $X$ bằng bao nhiêu độ C?", 200, "°C", 1,
       loi=r"Chọn đoạn nằm ngang dài hơn làm nóng chảy, hoặc lấy điểm cuối đồ thị làm nhiệt độ sôi.",
       ke=[("Nhận đoạn nằm ngang cao hơn là sôi vì đun nóng thì nóng chảy trước, sôi sau", True),
           ("Chọn đoạn nằm ngang dài hơn là sôi", "Độ dài chỉ cho biết thời gian chuyển thể, không cho biết đó là quá trình nào."),
           ("Lấy điểm cuối đồ thị làm nhiệt độ sôi", "Điểm cuối nằm trên đoạn dốc : hơi đang nóng lên, không phải đang sôi.")]),
  buoc("Thể ở phút thứ 16", "Ở phút thứ $16$, $X$ ở thể nào?",
       loi=r"Cho rằng chất đã hoá hơi hết vì nhiệt độ rất cao, hoặc vẫn là lỏng vì chưa đến cuối đoạn nằm ngang.",
       lua_chon=[("Lỏng và hơi cùng tồn tại", True),
                 ("Hoàn toàn lỏng", "Phút 16 nằm trong đoạn sôi : một phần chất đã thành hơi."),
                 ("Hoàn toàn hơi", "Chất chỉ hoá hơi hoàn toàn khi hết đoạn nằm ngang, ở thời điểm sau đó.")],
       ke=[("Xét phút đã cho thuộc đoạn nào của đồ thị", True),
           ("Chỉ nhìn nhiệt độ rồi gọi tên thể", "Cùng một nhiệt độ có thể ứng với hai thể cùng tồn tại ; phải xét phút thuộc đoạn nào."),
           ("Tính nhiệt lượng cần để hoá hơi hết", "Bài không cho khối lượng hay nhiệt hoá hơi riêng ; chỉ cần xét vị trí trên đồ thị.")]),
  buoc("Thời gian sôi", "Quá trình sôi kéo dài bao nhiêu phút?", 8, "phút", 0.2,
       loi=r"Lấy mốc cuối đoạn nằm ngang làm thời gian sôi, quên trừ mốc đầu.",
       ke=[("Lấy mốc cuối trừ mốc đầu của đoạn nằm ngang cao", True),
           ("Lấy mốc cuối của đoạn làm thời gian sôi", "Mốc cuối chỉ là thời điểm kết thúc ; thời gian là hiệu hai mốc."),
           ("Đếm số ô lưới của đoạn rồi nhân với nhiệt độ", "Thời gian đọc trên trục thời gian, không liên quan tới nhiệt độ.")]),
  buoc("Tốc độ tăng nhiệt ở đoạn CD", "Ở đoạn $CD$, nhiệt độ tăng bao nhiêu độ C mỗi phút?", 28, "°C/phút", 0.5,
       loi=r"Chia độ tăng nhiệt cho 12 (cả thời gian từ gốc) thay vì cho thời gian của riêng đoạn CD.",
       ke=[("Lấy độ tăng nhiệt độ giữa hai đầu đoạn chia khoảng thời gian của đoạn", True),
           ("Chia nhiệt độ ở điểm D cho thời điểm của D", "Phải dùng độ tăng nhiệt độ của đoạn, không phải nhiệt độ từ gốc tọa độ."),
           ("Lấy nhiệt độ sôi trừ nhiệt độ ban đầu chia tổng thời gian", "Cách này lẫn nhiều đoạn có độ dốc khác nhau ; chỉ xét riêng đoạn CD.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>làm nguội</b>, không ghi nhiệt độ đông đặc → <b>đông đặc = nóng chảy</b> ; cùng tốc độ thì cùng thời gian.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Nhiệt độ đông đặc (dữ kiện ẩn)", "Chì đông đặc ở nhiệt độ nào (độ C)?", 327, "°C", 1,
       loi=r"Dùng 397 (nhiệt độ lúc rót) hoặc nhiệt độ nóng chảy của chất khác trong bảng ; đề không ghi nhiệt độ đông đặc."),
  buoc("Mốc bắt đầu đông đặc", "Sau bao nhiêu phút kể từ lúc rót thì chì bắt đầu đông đặc?", 5, "phút", 0.1,
       loi=r"Lấy 397 chia 14 (cho nguội về 0 °C) hoặc nhân thay vì chia ; thực ra chỉ nguội tới nhiệt độ đông đặc.",
       ke=[("Lấy độ giảm nhiệt độ từ lúc rót đến nhiệt độ đông đặc chia tốc độ nguội", True),
           ("Chia nhiệt độ lúc rót cho tốc độ nguội", "Chì không nguội tới 0 °C mà dừng lại ở nhiệt độ đông đặc."),
           ("Nhân độ giảm nhiệt độ với tốc độ nguội", "Tốc độ là độ giảm trong mỗi phút ; muốn ra số phút phải chia, không nhân.")]),
  buoc("Mốc đông đặc hoàn toàn", "Chì đông đặc hoàn toàn vào phút thứ mấy (kể từ lúc rót)?", 9, "phút", 0.1,
       loi=r"Tưởng thời gian đông đặc tính bằng độ giảm nhiệt độ chia 14 ; hoặc quên cộng mốc bắt đầu vào thời gian đông đặc.",
       ke=[("Cộng thời gian đông đặc (bằng thời gian nóng chảy lúc đun) vào mốc bắt đầu", True),
           ("Tính thời gian đông đặc bằng tốc độ nguội khi còn lỏng", "Đang đông đặc, nhiệt độ không đổi nên không dùng được tốc độ độ C mỗi phút."),
           ("Lấy luôn thời gian đông đặc làm mốc kết thúc", "Thời gian đông đặc đo từ lúc bắt đầu đông đặc, không phải từ lúc rót ; phải cộng với mốc bắt đầu.")]),
  buoc("Nhiệt độ ở phút thứ 7", "Ở phút thứ $7$, nhiệt độ chì bằng bao nhiêu độ C?", 327, "°C", 1,
       loi=r"Tính 397 − 14·7 = 299 °C như thể vẫn nguội đều .",
       ke=[("Xét phút 7 nằm giữa mốc bắt đầu và mốc kết thúc đông đặc", True),
           ("Tính tiếp theo tốc độ nguội 14 °C mỗi phút", "Kết quả sẽ thấp hơn nhiệt độ đông đặc, vô lí vì chì đang đông đặc, nhiệt độ không đổi."),
           ("Cho rằng chì đã rắn hẳn nên nhiệt độ thấp hơn", "Chì chưa đông đặc xong ở phút 7 ; đang vừa lỏng vừa rắn.")]),
  buoc("Mẫu thuỷ tinh", "Nhiệt kế giảm đều, không lúc nào đứng yên : mẫu thuỷ tinh thuộc loại nào?",
       loi=r"Cho rằng chất nào đông đặc cũng có nhiệt độ đông đặc xác định, nên gọi nhầm là chất kết tinh.",
       lua_chon=[("Chất rắn vô định hình", True),
                 ("Chất rắn kết tinh", "Chất kết tinh làm nguội phải có đoạn nhiệt độ không đổi lúc đông đặc."),
                 ("Chưa kết luận được", "Tiêu chí đã đủ : không có đoạn nhiệt độ không đổi nghĩa là không có nhiệt độ đông đặc xác định.")],
       ke=[("Dựa vào việc có hay không có đoạn nhiệt độ không đổi", True),
           ("Dựa vào việc thuỷ tinh có toả nhiệt hay không", "Mọi chất khi nguội đều toả nhiệt ; điều đó không phân biệt được kết tinh và vô định hình."),
           ("Dựa vào nhiệt độ ban đầu cao hay thấp", "Nhiệt độ ban đầu không phân biệt hai loại chất rắn.")]),
  buoc("Kiểm tra")]),
]

write(J, 2, "Bài 1. Sự chuyển thể", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo độc lập (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
