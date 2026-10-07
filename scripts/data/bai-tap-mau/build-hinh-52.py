"""Bài 52 "Bài 7. Đồ thị độ dịch chuyển - thời gian" (Vật lí 10, chương 2): 4 dạng + tự luận.
Mô phỏng = điểm chạy trên đồ thị d–t (hoặc x–t) + vạch thời gian đứng + vật chạy trên trục, TÍNH THẬT từ các đoạn thẳng
(mẫu cách đều thời gian, nội suy tuyến tính). Chạy: python3 scripts/data/bai-tap-mau/build-hinh-52.py"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "52.json")
OLD = json.load(open(os.path.join(HERE, "old/52.json")))["questions"]
NOTE = "Hình minh hoạ, không đúng tỉ lệ."

# ───────────── thư viện riêng của bài: khung đồ thị, trục vị trí, mô phỏng ─────────────
GX0, GX1, GY0, GY1 = 58, 398, 26, 170

def fv(v):
    return str(int(v)) if abs(v - round(v)) < 1e-9 else f"{v:.1f}".replace(".", ",")

def pos(bps, t):
    """Nội suy tuyến tính theo các điểm gãy bps=[(t,d),…]; ngoài đoạn thì giữ giá trị biên."""
    if t <= bps[0][0]: return bps[0][1]
    for (t1, d1), (t2, d2) in zip(bps, bps[1:]):
        if t <= t2 + 1e-9:
            return d1 + (d2 - d1) * (t - t1) / (t2 - t1) if t2 > t1 else d2
    return bps[-1][1]

class Fr:
    """Khung đồ thị: trục ngang t, trục đứng d (hoặc x); lưới theo bước, nhãn ≥ 12."""
    def __init__(s, T, Ts, Dmin, Dmax, Ds, tl, dl):
        s.T, s.Ts, s.Dmin, s.Dmax, s.Ds, s.tl, s.dl = T, Ts, Dmin, Dmax, Ds, tl, dl
    def gx(s, t): return GX0 + t / s.T * (GX1 - GX0)
    def gy(s, d): return GY1 - (d - s.Dmin) / (s.Dmax - s.Dmin) * (GY1 - GY0)
    def sx(s, d): return GX0 + (d - s.Dmin) / (s.Dmax - s.Dmin) * (GX1 - GX0)
    def svg(s):
        b = ""
        n = int(round(s.T / s.Ts))
        for i in range(n + 1):
            t = i * s.Ts
            b += seg(s.gx(t), GY0, s.gx(t), GY1, "currentColor", 1, "", .13) + lbl(s.gx(t), GY1 + 17, fv(t), "currentColor", 12, "middle", "400")
        m = int(round((s.Dmax - s.Dmin) / s.Ds))
        for j in range(m + 1):
            d = s.Dmin + j * s.Ds
            b += seg(GX0, s.gy(d), GX1, s.gy(d), "currentColor", 1, "", .13) + lbl(GX0 - 7, s.gy(d) + 4, fv(d), "currentColor", 12, "end", "400")
        b += seg(GX0, GY0, GX0, GY1, "currentColor", 2) + seg(GX0, s.gy(max(s.Dmin, 0)), GX1, s.gy(max(s.Dmin, 0)), "currentColor", 2)
        b += lbl(GX1, GY1 + 36, s.tl, "currentColor", 13, "end", "700") + lbl(GX0 - 4, GY0 - 9, s.dl, "currentColor", 13, "start", "700")
        return b
    def line(s, bps, c, w=2.8, dash="", op=1):
        return poly([(s.gx(t), s.gy(d)) for t, d in bps], c, w, dash, op)

def strip_y(lanes): return 244 + 30 * (lanes - 1)

def strip(fr, lanes):
    """Trục vị trí nằm ngang dưới đồ thị (cùng thang d)."""
    y = strip_y(lanes) + 24
    b = seg(GX0, y, GX1, y, "currentColor", 2)
    m = int(round((fr.Dmax - fr.Dmin) / fr.Ds))
    for j in range(m + 1):
        d = fr.Dmin + j * fr.Ds
        b += seg(fr.sx(d), y - 4, fr.sx(d), y + 4, "currentColor", 1.6) + lbl(fr.sx(d), y + 20, fv(d), "currentColor", 12, "middle", "400")
    return b + lbl(GX1, y + 38, fr.dl, "currentColor", 13, "end", "700"), y + 46

def icon(x, y, kind, c, tag):
    if kind == "car":
        g = (f'<rect x="{x - 12:.1f}" y="{y - 9}" width="24" height="10" rx="3" fill="none" stroke="{c}" stroke-width="2.2"/>'
             f'<circle cx="{x - 6:.1f}" cy="{y + 2}" r="3.2" fill="{c}"/><circle cx="{x + 6:.1f}" cy="{y + 2}" r="3.2" fill="{c}"/>')
    else:
        g = f'<circle cx="{x:.1f}" cy="{y - 4}" r="7" fill="{c}" stroke="currentColor" stroke-width="1.5"/>'
    return g + lbl(x, y - 16, tag, c, 12, "middle", "700")

def simbody(fr, objs, T, N, secs):
    """objs = [dict(bps, c, lane, kind, tag)]; mô phỏng chạy MỘT lần khi bấm: điểm trên đồ thị, vạch đứng và vật trên trục."""
    ts = [T * i / N for i in range(N + 1)]
    lanes = max(o["lane"] for o in objs) + 1
    sb, ymax = strip(fr, lanes)
    b = ""
    vx = [fr.gx(t) for t in ts]
    b += f'<line y1="{GY0}" y2="{GY1}" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 4" opacity=".55" x1="{vx[0]:.1f}" x2="{vx[0]:.1f}">{smil("x1", vx, secs)}{smil("x2", vx, secs)}</line>'
    for o in objs:
        ds = [pos(o["bps"], t) for t in ts]
        gxs, gys = vx, [fr.gy(d) for d in ds]
        b += f'<circle r="5.5" fill="{o["c"]}" stroke="currentColor" stroke-width="1.5" cx="{gxs[0]:.1f}" cy="{gys[0]:.1f}">{smil("cx", gxs, secs)}{smil("cy", gys, secs)}</circle>'
    b += sb
    for o in objs:
        ds = [pos(o["bps"], t) for t in ts]
        y = strip_y(lanes) - 30 * (lanes - 1) + 30 * o["lane"]
        vals = ";".join(f"{fr.sx(d) - fr.sx(ds[0]):.1f} 0" for d in ds)
        b += (f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{secs:.2f}s" begin="indefinite" fill="freeze"/>'
              + icon(fr.sx(ds[0]), y, o["kind"], o["c"], o["tag"]) + "</g>")
    return b, ymax

def vbox(h): return f"0 0 420 {h}"

# ───────────── Dạng 1: xe đồ chơi, đọc đồ thị ─────────────
B1 = [(0, 0), (2, 4), (4, 4), (8, 0), (9, -1), (10, -1)]
F1 = Fr(10, 1, -2, 4, 1, "t (s)", "d (m)")
def d1(k):
    b = F1.svg()
    if k == 0:
        b += F1.line(B1, BLUE)
        sb, h = simbody(F1, [dict(bps=B1, c=ORG, lane=0, kind="car", tag="xe")], 10, 20, 10)
        return fig("d1-0", vbox(h), "Đồ thị độ dịch chuyển thời gian của xe đồ chơi; điểm cam chạy trên đồ thị còn xe chạy trên trục d ngay bên dưới", b + sb,
                   "Mô phỏng: điểm cam chạy trên đồ thị, xe chạy trên trục d bên dưới (đúng thời gian thật, 10 s). " + "Quỹ đạo tính theo đồ thị.")
    b += F1.line(B1, BLUE)
    for (t, d, s_, dx, dy) in [(1, 2, "① lên", 10, 20), (3, 4, "② ngang", -10, -10), (6, 2, "③ xuống", 12, -6), (9.5, -1, "④ ngang", -20, -10)]:
        b += lbl(F1.gx(t) + dx, F1.gy(d) + dy, s_, ORG, 13, "start", "700")
    b += lbl(260, 40, "Mỗi đoạn thẳng: một vận tốc", "currentColor", 12, "start", "400")
    return fig("d1-2", vbox(h := 216), "Đồ thị chia thành bốn đoạn: đi lên, nằm ngang, đi xuống, nằm ngang", b, "Dữ kiện: chia đồ thị tại các điểm gãy. " + NOTE)

# ───────────── Dạng 2: người đi bộ, độ dốc, vận tốc trung bình ─────────────
B2 = [(0, 0), (10, 20), (20, 20), (50, 5)]
F2 = Fr(50, 10, 0, 20, 5, "t (s)", "d (m)")
def d2(k):
    b = F2.svg() + F2.line(B2, BLUE)
    if k == 0:
        sb, h = simbody(F2, [dict(bps=B2, c=ORG, lane=0, kind="dot", tag="người")], 50, 25, 10)
        return fig("d2-0", vbox(h), "Đồ thị độ dịch chuyển thời gian của người đi bộ gồm ba đoạn thẳng", b + sb,
                   "Mô phỏng: chạy nhanh 5 lần (50 s thật chạy trong 10 s); điểm cam trên đồ thị cùng người trên trục d. Quỹ đạo tính theo đồ thị.")
    x1, y1, x2, y2 = F2.gx(0), F2.gy(0), F2.gx(10), F2.gy(20)
    b += seg(x1, y1, x2, y1, ORG, 2, "5 4") + seg(x2, y1, x2, y2, ORG, 2, "5 4")
    b += lbl((x1 + x2) / 2, y1 - 6, "Δt", ORG, 13, "middle", "700") + lbl(x2 + 6, (y1 + y2) / 2 + 4, "Δd", ORG, 13, "start", "700")
    b += seg(GX0, F2.gy(10), GX1, F2.gy(10), RED, 1.8, "6 4")
    b += lbl(GX1, F2.gy(10) - 6, "d = 10 m", RED, 13, "end", "700")
    for t in (5, 40):
        b += dot(F2.gx(t), F2.gy(10), 5, RED) + lbl(F2.gx(t), F2.gy(10) + 20, "?", RED, 14, "middle", "700")
    return fig("d2-2", vbox(212), "Tam giác độ dốc trên đoạn đầu và đường ngang d bằng 10 m cắt đồ thị tại hai điểm", b, "Dữ kiện: độ dốc = Δd / Δt; đường d = 10 m cắt đồ thị. " + NOTE)

# ───────────── Dạng 3: hai xe, đồ thị thẳng, phương trình, gặp nhau ─────────────
B3a = [(0, 0), (2.5, 100)]
B3b = [(0, 150), (2.5, 0)]
F3 = Fr(2.5, 0.5, 0, 150, 50, "t (h)", "x (km)")
def d3(k):
    b = F3.svg() + F3.line(B3a, BLUE) + F3.line(B3b, ORG)
    if k == 0:
        b += lbl(F3.gx(2.5) - 4, F3.gy(100) - 8, "xe I", BLUE, 13, "end", "700") + lbl(F3.gx(0.6), F3.gy(138), "xe II", ORG, 13, "start", "700")
        sb, h = simbody(F3, [dict(bps=B3a, c=BLUE, lane=0, kind="car", tag="I"), dict(bps=B3b, c=ORG, lane=1, kind="car", tag="II")], 2.5, 25, 10)
        return fig("d3-0", vbox(h), "Đồ thị toạ độ thời gian của hai xe: xe I đi lên từ gốc, xe II đi xuống từ 150 km; hai điểm chạy trên đồ thị và hai xe chạy ngược chiều trên trục x", b + sb,
                   "Mô phỏng: 1 h trong mô phỏng = 4 s (2,5 h chạy trong 10 s). Quỹ đạo tính theo đồ thị.")
    b += lbl(F3.gx(0.1), F3.gy(46), "x₀ đọc tại t = 0", "currentColor", 12, "start", "400")
    b += lbl(F3.gx(1.42), F3.gy(63), "gặp nhau", RED, 13, "end", "700")
    b += dot(F3.gx(1.5), F3.gy(60), 5.5, RED) + lbl(F3.gx(2.5) - 4, F3.gy(100) - 8, "xe I", BLUE, 13, "end", "700") + lbl(F3.gx(0.6), F3.gy(138), "xe II", ORG, 13, "start", "700")
    return fig("d3-2", vbox(212), "Hai đoạn thẳng cắt nhau tại một điểm; chỗ cắt là lúc hai xe cùng toạ độ", b, "Dữ kiện: cắt nhau nghĩa là cùng toạ độ cùng lúc. " + NOTE)

# ───────────── Dạng 4: xuất phát lệch giờ, bài ngược (thử v = 3 km/h) ─────────────
B4a = [(0, 0), (1.5, 4.5)]
B4b = [(0, 10), (0.5, 10), (1.5, 7)]
F4 = Fr(1.5, 0.5, 0, 10, 2, "t (h)", "x (km)")
def d4(k):
    b = F4.svg() + F4.line(B4a, BLUE, 2.4, "6 4") + F4.line(B4b, ORG, 2.4, "6 4")
    if k == 0:
        b += lbl(F4.gx(0.9), F4.gy(1.2), "A (thử 3 km/h)", BLUE, 12, "start", "700") + lbl(GX0 + 6, F4.gy(8.3), "B (xuất phát muộn)", ORG, 12, "start", "700")
        sb, h = simbody(F4, [dict(bps=B4a, c=BLUE, lane=0, kind="dot", tag="A"), dict(bps=B4b, c=ORG, lane=1, kind="dot", tag="B")], 1.5, 15, 7.5)
        return fig("d4-0", vbox(h), "Một lần đi thử: hai người cùng đi với tốc độ 3 km/h, B xuất phát muộn nửa giờ, sau khi B đi một giờ vẫn chưa gặp nhau", b + sb,
                   "Mô phỏng thử với tốc độ 3 km/h cho cả hai người: chưa gặp nhau, phải tìm tốc độ đúng (1 h = 5 s). Đồ thị nét đứt là lần thử.")
    b += seg(F4.gx(0.5), GY0, F4.gx(0.5), GY1, GRN, 1.6, "5 4") + seg(F4.gx(1.5), GY0, F4.gx(1.5), GY1, RED, 1.6, "5 4")
    b += lbl(F4.gx(0.5) + 4, GY0 + 40, "B xuất phát", GRN, 12, "start", "700") + lbl(F4.gx(1.5) - 4, GY0 + 14, "gặp: B đi 1 h", RED, 12, "end", "700")
    b += lbl(F4.gx(0.05), F4.gy(1.8), "A: t₀ = 0", BLUE, 12, "start", "700")
    return fig("d4-2", vbox(212), "Người A xuất phát lúc t bằng 0, người B xuất phát lúc 0,5 giờ; lúc gặp nhau B đã đi một giờ", b, "Dữ kiện: hai mốc thời gian, cùng một gốc thời gian. " + NOTE)

BUILD = [d1, d2, d3, d4]

# ───────────── Bảng phân tích ─────────────
ANALYSIS = [
 [("\"đồ thị độ dịch chuyển – thời gian … chiều dương là chiều xe chạy lúc đầu\"", "Trục đứng $d$ (m), trục ngang $t$ (s)", "⚠ Đồ thị cho <strong>vị trí</strong> theo thời gian, không phải hình đường đi"),
  ("\"mô tả chuyển động của xe trong từng khoảng thời gian\"", "Chia đồ thị tại các điểm gãy", "Dốc lên: $v\\gt0$ · nằm ngang: đứng yên · dốc xuống: $v\\lt0$"),
  ("\"vị trí … tại thời điểm t = 2 s, 4 s, 8 s và 10 s\"", "Cần $d$ tại $t=2;4;8;10$ s", "Đọc $d$ trên trục đứng tại $t$ tương ứng"),
  ("\"độ dịch chuyển sau 10 s\"", "Điểm đầu $t=0$, điểm cuối $t=10$ s", "$d=d_{\\text{cuối}}-d_{\\text{đầu}}$ (có dấu)"),
  ("\"quãng đường đi được\"", "Cần $s$", "$s=\\sum|\\Delta d|$ của từng đoạn (không âm)"),
  ("\"vì sao hai giá trị này không bằng nhau\"", "So sánh $s$ và $|d|$", "⚠ Có đổi chiều thì $s\\gt|d|$; đi một chiều thì $s=|d|$")],
 [("\"đồ thị độ dịch chuyển – thời gian\" (độ dịch chuyển tính từ O)", "Các đoạn thẳng: 0–10 s; 10–20 s; 20–50 s", "⚠ Chỉ lấy hai điểm trên <strong>cùng một</strong> đoạn thẳng; đoạn nằm ngang có $v=0$"),
  ("\"tính vận tốc trên từng đoạn\"", "Hai điểm đọc trên mỗi đoạn", "Độ dốc: $v=\\dfrac{\\Delta d}{\\Delta t}=\\dfrac{d_2-d_1}{t_2-t_1}$"),
  ("\"những lúc nào người đó cách O 10 m\"", "$d=10$ m", "Đường ngang $d=10$ m cắt đồ thị ở những điểm nào? Đọc $t$ ở từng giao điểm"),
  ("\"vận tốc trung bình trong cả 50 s\"", "$d_{\\text{đầu}}$, $d_{\\text{cuối}}$, $\\Delta t=50$ s", "$v_{tb}=\\dfrac{d}{\\Delta t}$ (có dấu)"),
  ("\"tốc độ trung bình\"", "Cần $s$ cả quá trình", "$\\text{tốc độ}_{tb}=\\dfrac{s}{\\Delta t}$; $s=\\sum|\\Delta d|$"),
  ("\"cả 50 s\" (có đoạn đi ngược)", "Nhiều đoạn, vận tốc khác nhau", "⚠ Không lấy trung bình cộng các vận tốc từng đoạn")],
 [("\"gốc toạ độ O tại bến A, chiều dương từ A đến B, gốc thời gian lúc hai xe cùng xuất phát\"", "Cùng gốc toạ độ, cùng gốc thời gian", "⚠ Chỉ khi cùng gốc mới đặt $x_1=x_2$ được"),
  ("\"đồ thị toạ độ – thời gian của hai xe\"", "Hai đoạn thẳng: I đi lên, II đi xuống", "Đường thẳng: chuyển động thẳng đều; độ dốc dương → $v\\gt0$; độ dốc âm → $v\\lt0$"),
  ("\"vận tốc của mỗi xe\"", "Hai điểm đọc trên mỗi đường", "$v=\\dfrac{x_2-x_1}{t_2-t_1}$"),
  ("\"phương trình chuyển động của mỗi xe\"", "$x_0$ đọc tại $t=0$; $v$ vừa tìm", "$x=x_0+vt$"),
  ("\"gặp nhau lúc nào\"", "Cùng toạ độ cùng lúc", "$x_1=x_2$ → giải $t$ (giao điểm hai đường)"),
  ("\"vị trí cách A bao nhiêu km\"", "Cần $x$ lúc gặp", "Thế $t$ vào một phương trình")],
 [("\"AB dài 10 km … đi ngược chiều\" (gốc tại A, chiều dương A→B)", "$x_{0A}=0$; $x_{0B}=10$ km; $v_A\\gt0$, $v_B\\lt0$", "Đi ngược chiều dương thì $v\\lt0$"),
  ("\"người ở A xuất phát trước người ở B 0,5 h\"", "A: $t_0=0$; B: $t_0=0{,}5$ h", "⚠ Cùng một gốc thời gian cho cả hai: $x=x_0+v(t-t_0)$, $t_0$ là lúc xuất phát"),
  ("\"sau khi người ở B đi được 1 h thì gặp nhau\"", "Lúc gặp: B đã đi 1 h", "Đi ngược chiều gặp nhau: $s_A+s_B=AB$"),
  ("\"đi nhanh như nhau\"", "$|v_A|=|v_B|=v$", "$s=v\\,\\Delta t$ cho từng người → tìm $v$"),
  ("\"vẽ đồ thị … trên cùng một hệ trục\"", "Hai đoạn thẳng; B bắt đầu từ $t=0{,}5$ h", "Điểm cắt hai đường là chỗ gặp"),
  ("\"vị trí và thời điểm hai người gặp nhau\"", "Cần $t$ và $x$ lúc gặp", "$x_A=x_B$ → $t$; thế vào một phương trình")],
]

# ───────────── Lời giải ─────────────
R1 = ["<strong>Khái niệm:</strong> đồ thị $d$–$t$ cho <em>vị trí</em> theo thời gian, không phải hình đường đi.",
      "<strong>Định luật:</strong> độ dốc là vận tốc: dốc lên $v\\gt0$ · nằm ngang đứng yên · dốc xuống $v\\lt0$.",
      "Độ dịch chuyển: $d=d_{\\text{cuối}}-d_{\\text{đầu}}$ (có dấu).",
      "Quãng đường: $s=\\sum|\\Delta d|$ (cộng từng đoạn).",
      "⚠ <strong>Điều kiện:</strong> chia đồ thị tại các điểm gãy; mỗi đoạn thẳng một vận tốc."]
R2 = ["<strong>Khái niệm:</strong> vận tốc là độ dốc đồ thị $d$–$t$: $v=\\dfrac{\\Delta d}{\\Delta t}$ (có dấu).",
      "Vận tốc trung bình: $v_{tb}=\\dfrac{d}{\\Delta t}$ · tốc độ trung bình: $\\dfrac{s}{\\Delta t}$.",
      "Phương trình mỗi đoạn thẳng: $d=d_1+v(t-t_1)$.",
      "⚠ <strong>Điều kiện:</strong> hai điểm lấy trên cùng một đoạn thẳng."]
R3 = ["<strong>Khái niệm:</strong> đồ thị $x$–$t$ thẳng là chuyển động thẳng đều; độ dốc là $v$.",
      "Phương trình: $x=x_0+vt$ ($x_0$ là toạ độ lúc $t=0$; $v\\lt0$ nếu đi ngược chiều dương).",
      "Hai vật gặp nhau: $x_1=x_2$ (giao điểm hai đường).",
      "⚠ <strong>Điều kiện:</strong> cùng gốc toạ độ, cùng chiều dương, cùng gốc thời gian."]
R4 = R3[:2] + ["Xuất phát muộn: $x=x_0+v(t-t_0)$ với $t_0$ là lúc xuất phát.",
               "Đi ngược chiều gặp nhau: $s_A+s_B=AB$; lúc gặp $x_A=x_B$.",
               "⚠ <strong>Điều kiện:</strong> một gốc thời gian chung; $t\\ge t_0$ mới dùng phương trình."]

SOLS = [
 sol(R1, [
  ("Mô tả từng giai đoạn", [P("0–2 s: $d$ tăng từ 0 lên 4 m, đi theo chiều dương."), P("2–4 s: nằm ngang ở 4 m, xe đứng yên."),
                            P("4–9 s: $d$ giảm từ 4 m xuống $-1$ m, xe đổi chiều, đi ngược chiều dương; lúc $t=8$ s xe qua điểm xuất phát."),
                            P("9–10 s: nằm ngang ở $-1$ m, xe đứng yên.")]),
  ("Vị trí ở các giây", [P("Đọc $d$ trên trục đứng:"), M(r"d(2)=4\ \text{m}"), M(r"d(4)=4\ \text{m}"), M(r"d(8)=0\ \text{m}"), M(r"d(10)=-1\ \text{m}")]),
  ("Độ dịch chuyển sau 10 s", [M(r"d=d_{10}-d_0=-1-0"), A(r"d=-1\ \text{m}")]),
  ("Quãng đường sau 10 s", [P("Cộng độ lớn dịch chuyển từng đoạn:"), M(r"s=|4-0|+|4-4|+|-1-4|+|-1-(-1)|=4+0+5+0"), A(r"s=9\ \text{m}")]),
  ("Vì sao $s\\neq|d|$", [P("Xe đổi chiều ở $t=4$ s: $d$ chỉ so điểm cuối với điểm đầu, còn $s$ cộng cả đoạn đi ngược."), P("Kiểm tra: $s\\ge|d|$ ($9\\ge1$) ✓")])],
  ["a) đi tới (0–2 s) · đứng (2–4 s) · đi ngược (4–9 s) · đứng (9–10 s)", "b) $4\\ \\text{m}$; $4\\ \\text{m}$; $0\\ \\text{m}$; $-1\\ \\text{m}$", "c) $s=9\\ \\text{m}$; $d=-1\\ \\text{m}$"],
  "Nhận dạng: đề cho <strong>đồ thị $d$–$t$ gấp khúc</strong> → chia đoạn, đọc dốc từng đoạn; $d$ lấy ở điểm cuối, $s$ cộng từng đoạn."),
 sol(R2, [
  ("Vận tốc trên từng đoạn", [M(r"v_1=\dfrac{20-0}{10-0}"), A(r"v_1=2\ \text{m/s}"), M(r"v_2=\dfrac{20-20}{20-10}"), A(r"v_2=0"), M(r"v_3=\dfrac{5-20}{50-20}"), A(r"v_3=-0{,}5\ \text{m/s}")]),
  ("Những lúc cách O 10 m", [P("Đường $d=10$ m cắt đồ thị ở đoạn 1 và đoạn 3 (đoạn 2 nằm ở 20 m)."), P("Đoạn 1:"), M(r"d=2t=10"), A(r"t_1=5\ \text{s}"),
                             P("Đoạn 3: $d=20+v_3(t-20)$:"), M(r"d=20-0{,}5(t-20)=30-0{,}5t"), M(r"10=30-0{,}5t"), A(r"t_2=40\ \text{s}")]),
  ("Độ dịch chuyển và quãng đường cả 50 s", [M(r"d=5-0=5\ \text{m}"), M(r"s=|20-0|+|20-20|+|5-20|=20+0+15"), A(r"s=35\ \text{m}")]),
  ("Vận tốc và tốc độ trung bình", [M(r"v_{tb}=\dfrac{d}{\Delta t}=\dfrac{5}{50}"), A(r"v_{tb}=0{,}1\ \text{m/s}"), M(r"\text{tốc độ}_{tb}=\dfrac{s}{\Delta t}=\dfrac{35}{50}"), A(r"0{,}7\ \text{m/s}"),
                                  P("Kiểm tra: không lấy trung bình cộng $\\dfrac{2+0-0{,}5}{3}=0{,}5$ — sai vì ba đoạn kéo dài khác nhau."), P("$\\text{tốc độ}_{tb}\\ge|v_{tb}|$ ✓")])],
  ["a) $v_1=2$; $v_2=0$; $v_3=-0{,}5\\ \\text{m/s}$", "b) $t=5\\ \\text{s}$ và $t=40\\ \\text{s}$", "c) $v_{tb}=0{,}1\\ \\text{m/s}$; tốc độ trung bình $0{,}7\\ \\text{m/s}$"],
  "Nhận dạng: đề hỏi <strong>vận tốc / lúc nào ở vị trí …</strong> trên đồ thị nhiều đoạn → độ dốc từng đoạn; trung bình lấy $\\dfrac{d}{\\Delta t}$ và $\\dfrac{s}{\\Delta t}$, không trung bình cộng."),
 sol(R3, [
  ("Vận tốc mỗi xe từ độ dốc", [P("Xe I đi qua $(0;\\,0)$ và $(2{,}5\\ \\text{h};\\,100\\ \\text{km})$:"), M(r"v_I=\dfrac{100-0}{2{,}5-0}"), A(r"v_I=40\ \text{km/h}"),
                               P("Xe II đi qua $(0;\\,150)$ và $(2{,}5;\\,0)$:"), M(r"v_{II}=\dfrac{0-150}{2{,}5-0}"), A(r"v_{II}=-60\ \text{km/h}"), P("Dấu trừ: xe II đi ngược chiều dương.")]),
  ("Phương trình chuyển động", [P("Dùng $x=x_0+vt$ với $x_0$ đọc tại $t=0$:"), A(r"x_I=40t\ \ (\text{km})"), A(r"x_{II}=150-60t\ \ (\text{km})")]),
  ("Lúc hai xe gặp nhau", [M(r"x_I=x_{II}"), M(r"40t=150-60t"), M(r"100t=150"), A(r"t=1{,}5\ \text{h}")]),
  ("Vị trí gặp nhau", [M(r"x=40\cdot1{,}5"), A(r"x=60\ \text{km}"), P("Kiểm tra: $x_{II}=150-60\\cdot1{,}5=60$ km ✓; giao điểm nằm trong $0\\le t\\le2{,}5$ h ✓")])],
  ["a) $v_I=40\\ \\text{km/h}$; $v_{II}=-60\\ \\text{km/h}$", "b) $x_I=40t$; $x_{II}=150-60t$", "c) gặp lúc $t=1{,}5\\ \\text{h}$, cách A $60\\ \\text{km}$"],
  "Nhận dạng: đề cho <strong>đồ thị thẳng của hai vật</strong> → đọc $x_0$, $v$ lập phương trình, đặt $x_1=x_2$ tìm chỗ gặp."),
]

# Dạng 4: lời giải có hình đồ thị đáp án (chèn trước ô Đáp số)
def hinh_giai():
    fr = Fr(2, 0.5, 0, 10, 2, "t (h)", "x (km)")
    A_ = [(0, 0), (2, 8)]; B_ = [(0.5, 10), (2, 4)]
    b = fr.svg() + fr.line(A_, BLUE) + fr.line(B_, ORG)
    b += dot(fr.gx(1.5), fr.gy(6), 5.5, RED) + lbl(GX0 + 8, fr.gy(5.2), "gặp: t = 1,5 h; x = 6 km", RED, 12, "start", "700")
    b += lbl(fr.gx(2) - 4, fr.gy(8) - 8, "A", BLUE, 13, "end", "700") + lbl(fr.gx(0.5) + 6, fr.gy(10) + 16, "B", ORG, 13, "start", "700")
    return fig("d4-3", vbox(212), "Đồ thị đáp án: đường A đi lên từ gốc, đường B bắt đầu từ 0,5 giờ tại 10 km đi xuống, hai đường cắt nhau tại t bằng 1,5 giờ, x bằng 6 km", b,
               "Đồ thị hai người: B bắt đầu từ $t=0{,}5$ h. " + NOTE)

s4 = sol(R4, [
  ("Vận tốc hai người", [P("Lúc gặp: A đã đi $1{,}5$ h, B đi $1$ h. Đi ngược chiều gặp nhau nên tổng quãng đường bằng $AB$:"), M(r"1{,}5v+1\cdot v=10"), M(r"v=\dfrac{10}{2{,}5}"), A(r"v=4\ \text{km/h}"),
                         P("A đi theo chiều dương, B đi ngược chiều dương:"), A(r"v_A=4\ \text{km/h};\quad v_B=-4\ \text{km/h}")]),
  ("Phương trình chuyển động", [P("A: $x_{0A}=0$, $t_0=0$:"), A(r"x_A=4t\ \ (\text{km})"), P("B: $x_{0B}=10$ km, xuất phát lúc $t_0=0{,}5$ h:"), M(r"x_B=10-4(t-0{,}5)"), A(r"x_B=12-4t\ \ (\text{km},\ t\ge0{,}5\ \text{h})")]),
  ("Lúc và chỗ gặp nhau", [M(r"x_A=x_B"), M(r"4t=12-4t"), A(r"t=1{,}5\ \text{h}"), M(r"x=4\cdot1{,}5"), A(r"x=6\ \text{km}"), P("Kiểm tra: B đi $1{,}5-0{,}5=1$ h được $4$ km, nên cách A còn $10-4=6$ km ✓")]),
  ("Đồ thị", [P("Đường A đi lên từ $(0;\\,0)$. Đường B bắt đầu tại $(0{,}5\\ \\text{h};\\,10\\ \\text{km})$ rồi đi xuống. Hai đường cắt nhau tại $(1{,}5\\ \\text{h};\\,6\\ \\text{km})$ (hình dưới).")])],
  ["a) $v_A=4$; $v_B=-4\\ \\text{km/h}$", "b) $x_A=4t$; $x_B=12-4t$ ($t\\ge0{,}5$)", "c) gặp lúc $t=1{,}5\\ \\text{h}$ (kể từ lúc A xuất phát), cách A $6\\ \\text{km}$"],
  "Nhận dạng: hai vật <strong>xuất phát lệch giờ</strong> → một gốc thời gian chung, người đến sau có $(t-t_0)$; điều kiện gặp cho phương trình hoặc quãng đường.")
SOLS.append(s4.replace('<div class="bt-final">', hinh_giai() + '<div class="bt-final">', 1))

# ───────────── Các dạng ─────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Đọc đồ thị: mô tả chuyển động, vị trí, quãng đường và độ dịch chuyển",
      topic="Đọc đồ thị độ dịch chuyển – thời gian",
      problem_html="<p>Một xe ô tô đồ chơi điều khiển từ xa chạy trên đường thẳng; chọn chiều dương là chiều xe chạy lúc đầu. Đồ thị độ dịch chuyển – thời gian của xe vẽ ở hình dưới.</p>"
                   "<p>a) Mô tả chuyển động của xe trong từng khoảng thời gian.</p><p>b) Xác định vị trí của xe so với điểm xuất phát tại thời điểm $t=2$ s, $4$ s, $8$ s và $10$ s.</p>"
                   "<p>c) Tính quãng đường đi được và độ dịch chuyển của xe sau 10 s. Vì sao hai giá trị này không bằng nhau?</p>"),
 dict(label="Dạng 2 · Trung bình · Độ dốc đồ thị: vận tốc từng đoạn, vận tốc trung bình và tốc độ trung bình",
      topic="Tính vận tốc từ độ dốc đồ thị",
      problem_html="<p>Một người đi bộ trên đường thẳng; chọn chiều dương là chiều ra xa cột mốc O, gốc thời gian lúc bắt đầu đi. Đồ thị độ dịch chuyển – thời gian (độ dịch chuyển tính từ O) vẽ ở hình dưới.</p>"
                   "<p>a) Tính vận tốc của người đó trên từng đoạn của đồ thị.</p><p>b) Những lúc nào người đó cách O 10 m?</p><p>c) Tính vận tốc trung bình và tốc độ trung bình trong cả 50 s.</p>"),
 dict(label="Dạng 3 · Trung bình · Hai đồ thị thẳng: lập phương trình và tìm chỗ hai xe gặp nhau",
      topic="Tính vận tốc từ độ dốc đồ thị",
      problem_html="<p>Hai ô tô chạy trên đường thẳng nối hai bến A và B; xe I xuất phát từ A, xe II xuất phát từ B. Chọn gốc toạ độ O tại bến A, chiều dương từ A đến B, gốc thời gian lúc hai xe cùng xuất phát. Đồ thị toạ độ – thời gian của hai xe I và II vẽ ở hình dưới.</p>"
                   "<p>a) Tính vận tốc của mỗi xe.</p><p>b) Lập phương trình chuyển động của mỗi xe.</p><p>c) Hai xe gặp nhau lúc nào, ở vị trí cách A bao nhiêu km?</p>"),
 dict(label="Dạng 4 · Khó · Xuất phát lệch giờ: tìm vận tốc từ điều kiện gặp nhau, phương trình và đồ thị",
      topic="Đọc đồ thị độ dịch chuyển – thời gian",
      problem_html="<p>Hai người đi bộ ở hai đầu một đoạn đường thẳng AB dài 10 km, đi ngược chiều để gặp nhau. Người ở A xuất phát trước người ở B 0,5 h. Sau khi người ở B đi được 1 h thì hai người gặp nhau. Biết hai người đi nhanh như nhau. "
                   "Chọn gốc toạ độ tại A, chiều dương từ A đến B, gốc thời gian lúc người ở A xuất phát.</p>"
                   "<p>a) Tính vận tốc của mỗi người.</p><p>b) Lập phương trình chuyển động của mỗi người.</p>"
                   "<p>c) Vẽ đồ thị toạ độ – thời gian của hai người trên cùng một hệ trục, rồi xác định vị trí và thời điểm hai người gặp nhau.</p>"),
]

# Ví dụ cũ chưa biên tập → tự luận (xếp dễ → khó). Đã dùng: VD6→Dạng 1, VD13→Dạng 3, VD17→Dạng 4 (chỉ số 5, 12, 16 bỏ).
ORDER = [10, 9, 11, 2, 3, 14, 13, 15, 1, 0, 7, 8]   # bỏ 4 (VD5: thiếu bảng số liệu) và 6 (VD7: không có hướng dẫn giải)
MUC = {10: "Dễ", 9: "Dễ", 11: "Dễ", 2: "Dễ", 3: "Trung bình", 14: "Trung bình", 13: "Trung bình", 15: "Trung bình", 1: "Trung bình", 0: "Khó", 7: "Khó", 8: "Khó"}
TU_LUAN = tu_luan_tu(OLD, ORDER, MUC)
TU_LUAN["body_html"] = TU_LUAN["body_html"].replace("t=2,67(h)", r"t=2,67\ \text{s}").replace("sau 2,67 h kể từ", "sau 2,67 s kể từ")

write(J, 52, "Bài 7. Đồ thị độ dịch chuyển - thời gian", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
