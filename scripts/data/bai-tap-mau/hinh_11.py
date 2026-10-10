"""Hình cho bài tập mẫu Bài 10 (Vật lí 12) "Lực từ. Cảm ứng từ", lesson_id 11.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Quy ước: đường sức (B) xanh dương, nét đứt, đầu V 30° (field_line); dòng điện cam; ⊙ = hướng ra khỏi mặt phẳng hình, ⊗ = hướng vào.
KHÔNG vẽ lực từ trong hình đề (các câu hỏi đều hỏi chiều/độ lớn lực), không ghi kết quả."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


# ───────────── tiện ích ─────────────
def sym_out(x, y, r=6.5, c=BLUE):
    """⊙ hướng ra khỏi mặt phẳng hình."""
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{c}" stroke-width="1.5"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="{c}"/>')

def sym_in(x, y, r=6.5, c=BLUE):
    """⊗ hướng vào mặt phẳng hình."""
    k = r * 0.68
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{c}" stroke-width="1.5"/>'
            f'<path d="M{x - k:.1f},{y - k:.1f} L{x + k:.1f},{y + k:.1f} M{x - k:.1f},{y + k:.1f} L{x + k:.1f},{y - k:.1f}" stroke="{c}" stroke-width="1.5"/>')

def box(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" opacity=".45"/>'

def fl(x1, y, x2, c=BLUE, w=1.5, L=10):
    """Đường sức nằm ngang chiều sang phải (nét đứt, đầu V 30°)."""
    return field_line(x1, y, x2, y, c, w, "6 4", L)

def rotg(cx, cy, a0, a1, dur, inner):
    """Nhóm quay quanh (cx,cy) từ a0 đến a1 độ (dương = cùng chiều kim đồng hồ), đều theo thời gian, chạy một lần khi bấm."""
    return (f'<g transform="rotate({a0} {cx} {cy})"><animateTransform attributeName="transform" type="rotate" '
            f'values="{a0} {cx} {cy};{a1} {cx} {cy}" dur="{dur}s" begin="indefinite" fill="freeze"/>{inner}</g>')

def tick_dim(x1, x2, y, label, lx, c="currentColor"):
    return (seg(x1, y, x2, y, c, 1.6) + seg(x1, y - 6, x1, y + 6, c, 1.6) + seg(x2, y - 6, x2, y + 6, c, 1.6)
            + lbl(lx, y - 8, label, c, 13, "middle", "700"))


# ───────────── Dạng 1 · bàn tay trái: dây MN trong mặt phẳng hình, B ⊙, I từ M đến N ─────────────
def d1(kk):
    b = box(24, 22, 372, 140)
    for x in range(52, 361, 44):
        for y in (46, 74, 128, 150):
            b += sym_out(x, y)
    b += seg(120, 100, 300, 100, "currentColor", 6, "", .35) + arrow("d1", "o", 150, 100, 272, 100, 3)
    b += lbl(104, 105, "M", "currentColor", 15, "end", "700") + lbl(316, 105, "N", "currentColor", 15, "start", "700")
    b += lbl(211, 92, "I", ORG, 15, "middle", "700")
    b += lbl(210, 14, "lên", "currentColor", 11, "middle", "400") + lbl(210, 184, "xuống", "currentColor", 11, "middle", "400")
    b += lbl(16, 198, "⊙ : đường sức hướng ra khỏi hình", BLUE, 11, "start", "400")
    b += lbl(404, 198, "trái ← → phải", "currentColor", 11, "end", "400")
    if kk == 0:
        for i, x0 in enumerate((124, 150, 176, 202)):
            b += (f'<circle cx="{x0}" cy="100" r="4" fill="currentColor" stroke="{ORG}" stroke-width="1.2">'
                  f'{smil("cx", [x0, x0 + 84], 3.2)}</circle>')
        return fig("d1-0", "0 0 420 204", "Dây dẫn MN trong từ trường hướng ra khỏi hình, các điện tích dương chạy từ M sang N", b,
                   "Mô phỏng: các điện tích dương chạy từ M đến N dọc dây (chiều quy ước của dòng điện); chưa vẽ lực từ. " + NOTE)
    return fig("d1-2", "0 0 420 204", "Dữ kiện: dây MN nằm ngang trong mặt phẳng hình, dòng điện từ M đến N, đường sức hướng ra khỏi hình", b,
               "Dữ kiện: dây MN trong mặt phẳng hình; đường sức ⊙ vuông góc mặt phẳng hình; chưa vẽ lực từ. " + NOTE)


# ───────────── Dạng 2 · F = BIl sinα: dây quay từ song song tới vuông góc đường sức ─────────────
def _wire_panel(cx, cy, ang, ln=70, arc_r=0, tag="", c=BLUE):
    """Một ô: 3 đường sức nằm ngang, dây qua (cx,cy) hợp đường sức góc `ang` (độ, đo ngược chiều kim đồng hồ từ chiều B)."""
    s = ""
    for dy in (-42, 0, 42):
        s += fl(cx - 46, cy + dy, cx + 46, c, 1.4, 9)
    a = math.radians(ang)
    s += seg(cx - ln / 2 * math.cos(a), cy + ln / 2 * math.sin(a), cx + ln / 2 * math.cos(a), cy - ln / 2 * math.sin(a), "currentColor", 5)
    if arc_r:
        s += arc(cx, cy, arc_r, 0, ang, GRN, 1.8)
        m = math.radians(ang / 2)
        s += lbl(cx + (arc_r + 6) * math.cos(m), cy - (arc_r + 6) * math.sin(m) + 4, f"{ang}°", GRN, 12, "start", "700")
    return s

def d2(kk):
    if kk == 0:
        cx, cy = 210, 100
        b = ""
        for dy in (-56, 0, 56):
            b += fl(40, cy + dy, 380, BLUE, 1.6, 11)
        b += lbl(386, cy - 52, "B", BLUE, 14, "start", "700")
        b += arc(cx, cy, 68, 0, 90, GRN, 1.8) + lbl(cx + 60, cy - 70, "α", GRN, 14, "start", "700")
        b += rotg(cx, cy, 0, -90, 4, seg(cx - 60, cy, cx + 60, cy, "currentColor", 6))
        b += dot(cx, cy, 3.5, "currentColor")
        b += lbl(16, 22, "I = 4,0 A ; l = 15 cm ; B = 0,25 T", "currentColor", 12, "start", "700")
        return fig("d2-0", "0 0 420 176", "Đoạn dây quay quanh trung điểm từ vị trí song song đến vuông góc với đường sức", b,
                   "Mô phỏng: dây quay đều quanh trung điểm, α tăng từ 0° đến 90° trong 4 s; chưa vẽ lực từ. " + NOTE)
    b = ""
    for cx, ang, tag in ((52, 90, "a) vuông góc"), (152, 30, "b) 30°"), (252, 150, "c) 150°"), (352, 0, "d) dọc đường sức")):
        b += _wire_panel(cx, 82, ang, 70, 24 if ang not in (0, 90) else 0)
        b += lbl(cx, 160, tag, "currentColor", 12, "middle", "600")
    b += lbl(16, 16, "α : góc giữa dây và đường sức", GRN, 12, "start", "700")
    return fig("d2-2", "0 0 420 172", "Bốn vị trí của dây so với đường sức: vuông góc, hợp 30 độ, hợp 150 độ, dọc theo đường sức", b,
               "Bốn vị trí của dây trong cùng một từ trường đều; chưa vẽ lực từ. " + NOTE)


# ───────────── Dạng 3 · tìm B: đồ thị F–I tính từ số liệu đề (dây 12 cm, 30°, 2,5 A, 15 mN) ─────────────
def d3(kk):
    ox, oy = 50, 170
    px, py = 200, 70            # điểm (2,5 A ; 15 mN)
    b = seg(ox, oy, 236, oy, "currentColor", 2) + chevron(236, oy, 1, 0, "currentColor", 2, 9)
    b += seg(ox, oy, ox, 34, "currentColor", 2) + chevron(ox, 34, 0, -1, "currentColor", 2, 9)
    b += lbl(244, oy + 4, "I (A)", "currentColor", 12, "start", "700") + lbl(ox + 6, 28, "F (mN)", "currentColor", 12, "start", "700")
    b += seg(ox, oy, px, py, GRN, 2.6)
    b += seg(px, py, px, oy, "currentColor", 1.2, "4 4", .6) + seg(px, py, ox, py, "currentColor", 1.2, "4 4", .6)
    b += lbl(px, oy + 16, "2,5", "currentColor", 12, "middle", "700") + lbl(ox - 6, py + 4, "15", "currentColor", 12, "end", "700")
    b += dot(ox, oy, 3.5, "currentColor") + lbl(ox - 8, oy + 14, "O", "currentColor", 12, "end", "700")
    # ô nhỏ: dây hợp đường sức 30°
    cx, cy = 340, 100
    for dy in (-40, 0, 40):
        b += fl(cx - 62, cy + dy, cx + 62, BLUE, 1.4, 9)
    a = math.radians(30)
    b += seg(cx - 36 * math.cos(a), cy + 36 * math.sin(a), cx + 36 * math.cos(a), cy - 36 * math.sin(a), "currentColor", 5)
    b += arc(cx, cy, 28, 0, 30, GRN, 1.8) + lbl(cx + 32, cy - 8, "30°", GRN, 12, "start", "700")
    b += lbl(cx, 160, "dây l = 12 cm", "currentColor", 12, "middle", "600")
    if kk == 0:
        b += (f'<circle cx="{ox}" cy="{oy}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
              f'{smil("cx", [ox, px], 3.5)}{smil("cy", [oy, py], 3.5)}</circle>')
        return fig("d3-0", "0 0 420 196", "Điểm biểu diễn lực từ chạy theo dòng điện tăng từ 0 đến 2,5 ampe trên đồ thị F theo I", b,
                   "Mô phỏng: dòng điện tăng đều từ 0 đến 2,5 A trong 3,5 s; điểm chạy từ gốc O đến vị trí (2,5 A ; 15 mN). " + NOTE)
    return fig("d3-2", "0 0 420 196", "Dữ kiện: dòng 2,5 ampe ứng với lực từ 15 mN, dây hợp đường sức 30 độ", b,
               "Dữ kiện: ở dòng 2,5 A đo được lực 15 mN; dây dài 12 cm hợp đường sức góc 30°. " + NOTE)


# ───────────── Dạng 4 · dây treo hai sợi chỉ, B ⊙; lực căng giảm khi dòng tăng (tính T/P = 1 − I/I₀) ─────────────
def d4(kk):
    I0, N = 4.0, 8
    b = box(46, 58, 330, 112)
    for x in (74, 170, 218, 266, 346):
        for y in (72, 150):
            b += sym_out(x, y)
    b += seg(60, 22, 360, 22, "currentColor", 3)
    for x in range(66, 360, 20):
        b += seg(x, 22, x - 8, 12, "currentColor", 1.2, "", .6)
    for x in (130, 290):
        b += f'<line x1="{x}" y1="22" x2="{x}" y2="110" stroke="currentColor" stroke-width="2"/>'
    if kk == 0:   # ampe kế, thang không ghi số: kim quay khi dòng điện tăng từ 0
        b += '<circle cx="388" cy="34" r="22" fill="none" stroke="currentColor" stroke-width="2"/>' + lbl(388, 70, "ampe kế", "currentColor", 11, "middle", "400")
        b += rotg(388, 34, -60, 40, 3, seg(388, 34, 388, 18, RED, 2.4)) + dot(388, 34, 3, "currentColor")
    b += seg(100, 110, 320, 110, "currentColor", 7)
    b += lbl(88, 115, "M", "currentColor", 15, "end", "700") + lbl(332, 115, "N", "currentColor", 15, "start", "700")
    b += lbl(210, 98, "m = 8,0 g", "currentColor", 13, "middle", "700")
    b += tick_dim(100, 320, 192, "l = 20 cm", 210)
    b += lbl(16, 216, "⊙ : đường sức hướng ra khỏi hình ; B = 0,10 T", BLUE, 11, "start", "400")
    if kk == 0:
        return fig("d4-0", "0 0 420 222", "Dây MN treo bằng hai sợi chỉ trong từ trường hướng ra khỏi hình; dòng điện tăng dần", b,
                   "Mô phỏng: dòng điện qua dây tăng dần từ 0 (kim ampe kế quay, thang không ghi số); chưa vẽ lực. " + NOTE)
    b += lbl(210, 132, "chiều và độ lớn của I : cần tìm", ORG, 12, "middle", "700")
    return fig("d4-2", "0 0 420 222", "Dữ kiện: dây MN dài 20 cm khối lượng 8 gam treo ngang bằng hai sợi chỉ, đường sức hướng ra khỏi hình", b,
               "Dữ kiện: dây MN treo ngang, đường sức ⊙ vuông góc mặt phẳng hình; chưa vẽ lực. " + NOTE)


# ───────────── Dạng 5 · khung dây nhìn dọc cạnh AB: AB (⊙) bên trái, CD (⊗) bên phải, B nằm ngang sang phải ─────────────
def d5(kk):
    C = (210, 105)
    xl, xr = 130, 290
    b = ""
    for y in (45, 105, 165):
        b += fl(30, y, 392, BLUE, 1.5, 10)
    b += lbl(396, 40, "B", BLUE, 14, "start", "700")
    frame = seg(xl, 105, xr, 105, "currentColor", 5) + sym_out(xl, 105, 9, ORG) + sym_in(xr, 105, 9, ORG)
    if kk == 0:
        b += rotg(C[0], C[1], 0, 90, 4, frame)
    else:
        b += frame
        b += tick_dim(xl, xr, 140, "BC = 4,0 cm", 164)
        b += lbl(xl, 84, "AB", "currentColor", 13, "middle", "700") + lbl(xr, 84, "CD", "currentColor", 13, "middle", "700")
        # khung quay để pháp tuyến hợp B góc 30° (nét đứt) và pháp tuyến n
        a = math.radians(120)
        pl = (C[0] + 80 * math.cos(a), C[1] - 80 * math.sin(a)); pr = (C[0] - 80 * math.cos(a), C[1] + 80 * math.sin(a))
        b += seg(pl[0], pl[1], pr[0], pr[1], "currentColor", 2.4, "5 4", .7)
        b += sym_out(pl[0], pl[1], 7, ORG) + sym_in(pr[0], pr[1], 7, ORG)
        n = math.radians(30)
        tip = (C[0] + 72 * math.cos(n), C[1] - 72 * math.sin(n))
        b += arrow("d5", "g", C[0], C[1], round(tip[0], 1), round(tip[1], 1), 2.6) + lbl(tip[0] + 6, tip[1] + 2, "n", GRN, 14, "start", "700")
        b += arc(C[0], C[1], 42, 0, 30, GRN, 1.8) + lbl(C[0] + 46, C[1] - 6, "30°", GRN, 12, "start", "700")
    b += dot(C[0], C[1], 3.5, "currentColor")
    b += lbl(16, 202, "⊙ ⊗ : dòng điện trong cạnh AB ra khỏi hình, trong cạnh CD vào hình", "currentColor", 11, "start", "400")
    if kk == 0:
        return fig("d5-0", "0 0 420 210", "Khung dây nhìn dọc cạnh AB quay quanh trục qua tâm từ vị trí mặt phẳng song song đến vuông góc đường sức", b,
                   "Mô phỏng minh hoạ: khung quay từ vị trí mặt phẳng song song đường sức đến vị trí mặt phẳng vuông góc đường sức (thời gian chỉ mang tính minh hoạ); chưa vẽ lực từ. " + NOTE)
    return fig("d5-2", "0 0 420 210", "Dữ kiện: khung dây nhìn dọc cạnh AB, mặt phẳng khung song song đường sức; nét đứt là vị trí pháp tuyến hợp đường sức 30 độ", b,
               "Dữ kiện: nét liền là vị trí đầu (mặt phẳng khung song song đường sức); nét đứt là vị trí ở câu d (pháp tuyến n hợp đường sức 30°); chưa vẽ lực từ. " + NOTE)
